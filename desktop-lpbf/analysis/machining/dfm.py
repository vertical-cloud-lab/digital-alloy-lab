"""Design-for-machining rules over every machined part of the desktop LPBF (issue #260, PR #266).

Reads the B-reps written by inventory.py and, per part, measures with OCP (OpenCascade):
  stock        bounding box -> the next standard bar / plate size (inch stock as McMaster and OnlineMetals list it),
               volume removed, and whether it is a lathe part (ROUND_KEYS, as cad/render_build.py turns them)
  holes        concave cylinders grouped by axis and radius; diameter -> tapped (drawn at the nominal size by joints.py),
               helical-insert STI hole (drawn at the insert's installed OD), dowel (6 mm, reamed H7), clearance,
               counterbore, or bored; depth, through/blind, depth/diameter, the web left to the nearest other face
  corners      partial concave cylinders (internal corner radii) with their height -> the largest end mill that cuts
               them and its length/diameter ratio; sharp concave edges along X/Y/Z (no radius at all)
  floors       concave tori / spheres (floor coves) -> bull-nose or ball end mill radius
  angled faces planar faces whose normal is not along X, Y or Z
  time         rough machining time from the removed volume (MRR), finished area, holes and setups (setups and
               unreachable skin come from cam_sim.py's sweep)
Writes desktop-lpbf/analysis/out/machining/dfm.json and dfm.md.

Run:  /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/machining/dfm.py [--parts /tmp/mach-work/parts]
~1 min.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
from collections import defaultdict

from OCP.BRep import BRep_Builder
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepGProp import BRepGProp, BRepGProp_Face
from OCP.BRepTools import BRepTools
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Line, GeomAbs_Plane, GeomAbs_Sphere, GeomAbs_Torus
from OCP.GProp import GProp_GProps
from OCP.gp import gp_Pnt, gp_Vec
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_IN, TopAbs_SOLID
from OCP.TopExp import TopExp, TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Shape
from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape

REPO = pathlib.Path(__file__).resolve().parents[3]
OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "machining"
INCH = 25.4
ROUND_KEYS = ("build_plate", "heater_block", "piston_head", "window_flange", "window_retaining", "field_stop", "hollow_piston_rod",
              "rod_end", "striker", "bottom_flange", "macor", "recoater_floating_bearing", "recoater_motor_standoff", "build_module")
# drawn diameters (joints.py): tapped holes at the nominal size, insert holes at d + 1.299 P, ISO 273 medium clearance
INSERT_OD = {3.08: "M2.5", 3.65: "M3", 4.909: "M4", 6.039: "M5", 7.299: "M6"}
STI_DRILL = {"M2.5": 2.64, "M3": 3.2, "M4": 4.22, "M5": 5.3, "M6": 6.3}   # STI drills (mm) listed on the McMaster 91732A insert pages
TAP = {2.5: "M2.5", 3.0: "M3", 4.0: "M4", 5.0: "M5", 6.0: "M6", 8.0: "M8"}
TAP_DRILL = {"M2.5": 2.05, "M3": 2.5, "M4": 3.3, "M5": 4.2, "M6": 5.0, "M8": 6.8}
PITCH = {"M2.5": 0.45, "M3": 0.5, "M4": 0.7, "M5": 0.8, "M6": 1.0, "M8": 1.25}
CLEAR = {2.9: "M2.5", 3.4: "M3", 4.5: "M4", 5.5: "M5", 6.6: "M6", 9.0: "M8"}
CBORE = {5.0: "M2.5", 7.0: "M3", 8.0: "M4", 10.0: "M5", 11.0: "M6"}
PLATE_IN = [0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0]
ROUND_IN = [x / 8 for x in range(2, 33)] + [4.25, 4.5, 4.75, 5.0, 5.5, 6.0, 7.0, 8.0]
# roughing metal-removal rate (cm3/min) and finishing rate (cm2/min) on a 3-axis VMC with shop-standard tooling; rough
# planning numbers (assumptions, not measured): 6061 ~1 in3/min with a 1/2 in. 3-flute, 316L ~0.2 in3/min
MRR = {"al6061": (16.0, 40.0), "mic6": (16.0, 40.0), "ss316l": (3.0, 10.0), "steel": (3.0, 10.0), "macor": (1.0, 5.0)}


def load(p):
    s = TopoDS_Shape()
    BRepTools.Read_s(s, str(p), BRep_Builder())
    return s


def solids(s):
    out, ex = [], TopExp_Explorer(s, TopAbs_SOLID)
    while ex.More():
        out.append(TopoDS.Solid_s(ex.Current()))
        ex.Next()
    return out


def faces(s):
    out, ex = [], TopExp_Explorer(s, TopAbs_FACE)
    while ex.More():
        out.append(TopoDS.Face_s(ex.Current()))
        ex.Next()
    return out


def normal_at(f, u, v):
    p, n = gp_Pnt(), gp_Vec()
    BRepGProp_Face(f).Normal(u, v, p, n)
    if n.Magnitude() > 0:
        n.Normalize()
    return p, n


def inside(solid, x, y, z):
    c = BRepClass3d_SolidClassifier(solid, gp_Pnt(x, y, z), 1e-6)
    return c.State() == TopAbs_IN


def axis_name(v, tol=0.02):
    for k, e in (("x", (1, 0, 0)), ("y", (0, 1, 0)), ("z", (0, 0, 1))):
        if abs(abs(v[0] * e[0] + v[1] * e[1] + v[2] * e[2]) - 1) < tol:
            return k
    return None


def match(d, table, tol=0.03):
    for k, v in table.items():
        if abs(d - k) <= tol:
            return v
    return None


def area(f):
    g = GProp_GProps()
    BRepGProp.SurfaceProperties_s(f, g)
    return g.Mass()


def next_size(x_mm, sizes_in):
    for s in sizes_in:
        if s * INCH >= x_mm:
            return s
    return None


def analyse(solid):
    fs = faces(solid)
    cyl_groups = defaultdict(lambda: dict(span=0.0, v0=1e9, v1=-1e9, faces=[]))
    corners, tori, angled, planar_area = [], [], [], defaultdict(float)
    for f in fs:
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        u0, u1, v0, v1 = BRepTools.UVBounds_s(f)
        if t == GeomAbs_Plane:
            _, n = normal_at(f, (u0 + u1) / 2, (v0 + v1) / 2)
            ax = axis_name((n.X(), n.Y(), n.Z()))
            a = area(f)
            if ax is None:
                angled.append(dict(n=[round(n.X(), 3), round(n.Y(), 3), round(n.Z(), 3)], area=round(a, 1)))
            else:
                sign = "+" if (n.X() + n.Y() + n.Z()) > 0 else "-"
                planar_area[sign + ax] += a
        elif t == GeomAbs_Cylinder:
            cy = ad.Cylinder()
            r = cy.Radius()
            a1 = cy.Axis()
            d, o = a1.Direction(), a1.Location()
            p, n = normal_at(f, (u0 + u1) / 2, (v0 + v1) / 2)
            # radial vector from the axis to the point
            op = gp_Vec(o, p)
            dv = gp_Vec(d)
            rad = op - dv * op.Dot(dv)
            concave = rad.Dot(n) < 0
            if not concave:
                continue
            dd = [d.X(), d.Y(), d.Z()]
            if max(range(3), key=lambda i: abs(dd[i])) is not None and dd[max(range(3), key=lambda i: abs(dd[i]))] < 0:
                dd = [-c for c in dd]
            ov = gp_Vec(o.X(), o.Y(), o.Z())
            dvv = gp_Vec(*dd)
            foot = ov - dvv * ov.Dot(dvv)            # axis point closest to the origin
            key = (round(r, 3), round(dd[0], 2), round(dd[1], 2), round(dd[2], 2), round(foot.X(), 1), round(foot.Y(), 1), round(foot.Z(), 1))
            g = cyl_groups[key]
            g["span"] += (u1 - u0)
            # axial extent: project the face's v range onto the canonical axis
            s0 = (gp_Vec(o.X(), o.Y(), o.Z()) + gp_Vec(d) * v0).Dot(dvv)
            s1 = (gp_Vec(o.X(), o.Y(), o.Z()) + gp_Vec(d) * v1).Dot(dvv)
            g["v0"], g["v1"] = min(g["v0"], s0, s1), max(g["v1"], s0, s1)
            g["r"], g["dir"], g["foot"] = r, dd, [foot.X(), foot.Y(), foot.Z()]
            g["faces"].append(f)
        elif t in (GeomAbs_Torus, GeomAbs_Sphere):
            p, n = normal_at(f, (u0 + u1) / 2, (v0 + v1) / 2)
            if t == GeomAbs_Torus:
                to = ad.Torus()
                r = to.MinorRadius()
                ax = to.Axis()
                o, d = ax.Location(), gp_Vec(ax.Direction())
                op = gp_Vec(o, p)
                radial = op - d * op.Dot(d)
                c = gp_Vec(o.X(), o.Y(), o.Z()) + radial.Normalized() * to.MajorRadius()
                away = gp_Vec(p.X(), p.Y(), p.Z()) - c
            else:
                sp = ad.Sphere()
                r = sp.Radius()
                ce = sp.Location()
                away = gp_Vec(ce, p)
            if away.Dot(n) < 0:       # material outside the tube / ball: a cove (concave fillet)
                tori.append(dict(r=round(r, 2), kind="torus" if t == GeomAbs_Torus else "sphere"))
    emap = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(solid, TopAbs_EDGE, TopAbs_FACE, emap)
    holes, partial = [], []
    for key, g in cyl_groups.items():
        r = g["r"]
        depth = g["v1"] - g["v0"]
        ax = axis_name(g["dir"])
        if g["span"] >= 2 * math.pi * 0.95:
            # through or blind: probe the axis just past each end
            o = [g["foot"][i] + g["dir"][i] * (g["v0"] - 0.3) for i in range(3)]
            e = [g["foot"][i] + g["dir"][i] * (g["v1"] + 0.3) for i in range(3)]
            blind = inside(solid, *o) or inside(solid, *e)
            mid = [g["foot"][i] + g["dir"][i] * (g["v0"] + g["v1"]) / 2 for i in range(3)]
            web = None
            try:
                hb = Bnd_Box()
                for hf in g["faces"]:
                    BRepBndLib.Add_s(hf, hb)
                hb.Enlarge(8.0)
                adj = set()
                for hf in g["faces"]:
                    ex = TopExp_Explorer(hf, TopAbs_EDGE)
                    while ex.More():
                        lst = emap.FindFromKey(ex.Current())
                        for af in lst:
                            adj.add(af.__hash__())
                        ex.Next()
                best = 1e9
                for f in fs:
                    if f.__hash__() in adj or any(f.IsSame(h) for h in g["faces"]):
                        continue
                    fb = Bnd_Box()
                    BRepBndLib.Add_s(f, fb)
                    if hb.IsOut(fb):
                        continue
                    ad2 = BRepAdaptor_Surface(f)
                    if ad2.GetType() == GeomAbs_Cylinder:
                        a2 = ad2.Cylinder().Axis()
                        dd2 = a2.Direction()
                        par = abs(dd2.X() * g["dir"][0] + dd2.Y() * g["dir"][1] + dd2.Z() * g["dir"][2])
                        if par > 0.999:
                            lo2 = a2.Location()
                            w = gp_Vec(gp_Pnt(*g["foot"]), lo2)
                            dv2 = gp_Vec(*g["dir"])
                            if (w - dv2 * w.Dot(dv2)).Magnitude() < 0.05:
                                continue          # coaxial (counterbore, screw-tip extension)
                    for hf in g["faces"]:
                        dss = BRepExtrema_DistShapeShape(hf, f)
                        if dss.IsDone() and dss.NbSolution():
                            best = min(best, dss.Value())
                web = best
            except Exception as ex_:  # noqa: BLE001
                print("web failed", ex_)
                web = None
            holes.append(dict(d=round(2 * r, 3), depth=round(depth, 2), axis=ax, blind=bool(blind), dir=[round(c, 4) for c in g["dir"]],
                              foot=[round(c, 3) for c in g["foot"]], s0=round(g["v0"], 3), s1=round(g["v1"], 3),
                              at=[round(c, 1) for c in mid], web=None if web is None or web > 1e8 else round(web, 2)))
        else:
            partial.append(dict(r=round(r, 3), height=round(depth, 2), axis=ax, span_deg=round(math.degrees(g["span"]), 0)))
    # sharp concave edges between perpendicular planar faces
    sharp = defaultdict(float)
    sharp_at = []
    for i in range(1, emap.Extent() + 1):
        e = TopoDS.Edge_s(emap.FindKey(i))
        fl = emap.FindFromIndex(i)
        if fl.Size() != 2:
            continue
        f1, f2 = [TopoDS.Face_s(x) for x in fl]
        if BRepAdaptor_Surface(f1).GetType() != GeomAbs_Plane or BRepAdaptor_Surface(f2).GetType() != GeomAbs_Plane:
            continue
        c = BRepAdaptor_Curve(e)
        if c.GetType() != GeomAbs_Line:
            continue
        m = c.Value((c.FirstParameter() + c.LastParameter()) / 2)
        L = abs(c.LastParameter() - c.FirstParameter())
        n1 = normal_at(f1, *[(a + b) / 2 for a, b in zip(BRepTools.UVBounds_s(f1)[0::2], BRepTools.UVBounds_s(f1)[1::2])])[1]
        n2 = normal_at(f2, *[(a + b) / 2 for a, b in zip(BRepTools.UVBounds_s(f2)[0::2], BRepTools.UVBounds_s(f2)[1::2])])[1]
        if abs(n1.Dot(n2)) > 0.1:
            continue
        q = gp_Vec(m.X(), m.Y(), m.Z()) + (n1 - n2) * 0.05
        if inside(solid, q.X(), q.Y(), q.Z()):
            dv = c.Line().Direction()
            ax = axis_name((dv.X(), dv.Y(), dv.Z()))
            sharp[ax or "other"] += L
            sharp_at.append(dict(axis=ax or "other", L=round(L, 1), at=[round(m.X(), 1), round(m.Y(), 1), round(m.Z(), 1)]))
    return dict(holes=holes, partial=partial, coves=tori, angled=angled, sharp={k: round(v, 1) for k, v in sharp.items()}, sharp_at=sharp_at,
                planar_area={k: round(v, 1) for k, v in planar_area.items()}, area=sum(area(f) for f in fs), n_faces=len(fs))


def classify_hole(h, pns):
    d = h["d"]
    if (m := match(d, INSERT_OD, 0.02)):
        return "sti", m
    if abs(d - 6.0) < 0.02 and any(p.startswith("93600A") for p in pns):
        return "dowel", "Ø6 H7"
    if (m := match(d, TAP, 0.005)) and (h["blind"] or d <= 8):
        # nominal-size holes are drawn tapped; a few are plain Ø4/Ø5 holes (overlap with counterbore Ø5 for M2.5 is rare)
        return "tapped", m
    if (m := match(d, CLEAR, 0.02)):
        return "clearance", m
    if (m := match(d, CBORE, 0.02)):
        return "cbore", m
    return "bored" if d > 10 else "drilled", f"Ø{d:g}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", default="/tmp/mach-work/parts")
    a = ap.parse_args()
    meta = json.load(open(pathlib.Path(a.parts) / "parts.json"))
    cam = json.loads((OUT / "cam_sim.json").read_text()) if (OUT / "cam_sim.json").exists() else {}
    sweep = cam.get("sweep", {})
    rows = []
    for p in meta["parts"]:
        if p["kind"] != "stock":
            continue
        shp = load(pathlib.Path(a.parts) / f"{p['slug']}.brep")
        sols = solids(shp)
        # pieces, not fragments: a boolean can leave slivers as loose solids (the M50 rod end's feedthrough block has eight,
        # 0-39 mm3, where its wire channel cuts between the bores; 2026-11-25), and each piece is timed in full below
        svol = [(lambda g: (BRepGProp.VolumeProperties_s(s_, g), g.Mass())[1])(GProp_GProps()) for s_ in sols]
        fragments = sum(1 for v_ in svol if v_ < 0.02 * max(svol))
        sols = [s_ for s_, v_ in zip(sols, svol) if v_ >= 0.02 * max(svol)]
        s0 = max(sols, key=lambda s: (lambda g: (BRepGProp.VolumeProperties_s(s, g), g.Mass())[1])(GProp_GProps()))
        A = analyse(s0)
        pns = sorted({pn for c in p["cuts"] for pn in c["pns"]})
        b = p["bbox"]
        if len(sols) > 1:       # compound of identical pieces: size one piece
            bb = Bnd_Box()
            BRepBndLib.Add_s(s0, bb)
            x0, y0, z0, x1, y1, z1 = bb.Get()
            b = [x0, x1, y0, y1, z0, z1]
        dims = sorted([b[1] - b[0], b[3] - b[2], b[5] - b[4]])
        is_round = any(p["slug"].startswith(k) or k in p["slug"] for k in ROUND_KEYS)
        if "posts" in p["slug"] or "hollow_piston_rod" in p["slug"]:
            stock, sv = "tube, cut to length", None
        elif "process_chamber_body" in p["slug"]:
            # through-frame (lpbf_low.FRAME): 13 x 9.5 x 5.5 in. blank; the 274 x 184 (R7) core leaves as one slug (waterjet or
            # bandsaw, FR-02), not as chips, so the stock the mill sees is the blank minus the slug
            slug_v = (274.0 * 184.0 - (4 - math.pi) * 7.0 ** 2) * 5.5 * INCH
            stock, sv = "13 x 9.5 x 5.5 in. blank (5-1/2 in. plate); the 274 x 184 core out as one slug first", 13.0 * 9.5 * 5.5 * INCH ** 3 - slug_v
        elif is_round:
            D = next_size(max(b[1] - b[0], b[3] - b[2]) + 3.0, ROUND_IN)
            L = (b[5] - b[4]) + 6.0
            stock, sv = (f"Ø{D:g} in. bar x {L:.0f} mm", math.pi * (D * INCH / 2) ** 2 * L) if D else ("over Ø8 in.: plate, waterjet blank", None)
            if "build_module" in p["slug"]:
                stock, sv = "weldment: Ø4 in. bar (spigot) + 3/4 in. plate (flange) + 2-1/2 in. tube (cylinder) + collar ring", None
        else:
            t = next_size(dims[0] + 1.5, PLATE_IN)
            stock = f"{t:g} in. plate, {dims[1] + 6:.0f} x {dims[2] + 6:.0f} mm" if t else "over 6 in.: block"
            sv = (t * INCH) * (dims[1] + 6) * (dims[2] + 6) if t else None
        vol = p["volume_mm3"] / len(sols)
        removed = (sv - vol) if sv else None
        holes = []
        for h in A["holes"]:
            k, size = classify_hole(h, pns)
            h.update(kind=k, size=size, ld=round(h["depth"] / h["d"], 1))
            holes.append(h)
        def coax(h1, h2):
            return all(abs(a - b) < 0.02 for a, b in zip(h1["dir"], h2["dir"])) and all(abs(a - b) < 0.05 for a, b in zip(h1["foot"], h2["foot"]))
        for h in holes:
            if h["kind"] in ("tapped", "cbore", "drilled", "clearance"):
                partners = [o for o in holes if o is not h and coax(h, o) and min(abs(o["s0"] - h["s1"]), abs(o["s1"] - h["s0"])) < 0.05]
                if any(o["kind"] == "sti" for o in partners) and h["kind"] == "tapped":
                    h["kind"], h["size"] = "sti-tip", h["size"]          # screw-tip extension drawn below a helical insert
                elif any(o["d"] < h["d"] and o["kind"] in ("clearance", "drilled") for o in partners) and match(h["d"], CBORE, 0.02):
                    h["kind"], h["size"] = "cbore", match(h["d"], CBORE, 0.02)
        for h in holes:
            if h["kind"] == "sti":
                tip = [o for o in holes if o["kind"] == "sti-tip" and coax(h, o)]
                h["tip_depth"] = round(sum(o["depth"] for o in tip), 2)
        counts = defaultdict(int)
        for h in holes:
            counts[f"{h['kind']} {h['size']}"] += 1
        conc = [c for c in A["partial"] if c["axis"]]
        min_r = min([c["r"] for c in conc], default=None)
        worst = max(conc, key=lambda c: c["height"] / max(2 * c["r"], 0.1), default=None)
        sw = sweep.get(p["slug"], {})
        nset = len(sw.get("setups", [])) or 2
        mat = p["mat"]
        mrr, fin = MRR.get(mat, (10.0, 20.0))
        t_rough = (removed / 1000.0 / mrr) if removed else 0.0
        t_fin = 0.5 * A["area"] / 100.0 / fin
        t_holes = sum(0.3 + (0.3 if h["kind"] == "tapped" else 0) + (2.0 if h["kind"] == "sti" else 0) + (0.5 if h["kind"] == "dowel" else 0)
                      for h in holes)
        t_setup = 20.0 * nset * (2.0 if "process_chamber_body" in p["slug"] else 1.0)
        n_pieces = len(sols) if "macor" not in p["slug"] else 1
        sti_short = [h for h in holes if h["kind"] == "sti" and h["blind"]]
        row = dict(slug=p["slug"], name=p["name"], mat=mat, n_pieces=len(sols), loose_fragments=fragments, bbox_mm=[round(x, 1) for x in dims[::-1]], volume_cm3=round(vol / 1000, 1),
                   machine="CNC lathe + VMC" if is_round else "3-axis VMC", stock=stock, stock_cm3=round(sv / 1000, 1) if sv else None,
                   removed_pct=round(100 * removed / sv, 0) if sv else None, setups=sw.get("setups"), unreachable_pct=round(100 * sw.get("unreachable_frac", 0), 2),
                   n_faces=A["n_faces"], holes=holes, hole_counts=dict(counts), min_corner_r=min_r,
                   worst_corner=worst, sharp_concave_mm=A["sharp"], coves=sorted({c["r"] for c in A["coves"]}), angled_faces=len(A["angled"]),
                   min_web_mm=min([h["web"] for h in holes if h.get("web") is not None], default=None),
                   thin_webs=[dict(d=h["d"], kind=h["kind"], size=h["size"], at=h["at"], web=h["web"]) for h in holes if h.get("web") is not None and h["web"] < 1.5],
                   sharp_at=A["sharp_at"][:60], partial=A["partial"],
                   deep_holes=[h for h in holes if h["ld"] > 5], time_min=dict(rough=round(t_rough, 0), finish=round(t_fin, 0), holes=round(t_holes, 0), setup=round(t_setup, 0)),
                   time_total_min=round((t_rough + t_fin + t_holes) * n_pieces + t_setup, 0))
        rows.append(row)
        print(f"{p['slug'][:44]:44s} {stock[:34]:34s} holes {dict(counts)} minR {min_r} sharp {A['sharp']} web {row['min_web_mm']} t {row['time_total_min']}", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "dfm.json").write_text(json.dumps(dict(parts=rows), indent=1))


if __name__ == "__main__":
    main()
