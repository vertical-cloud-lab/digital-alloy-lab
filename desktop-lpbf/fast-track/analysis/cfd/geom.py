"""Gas-side geometry of the fast-track machines for OpenFOAM, taken from the CadQuery model (issue #260, PR 294).

The solids that bound the gas inside the enclosure are built from ``cad/ft_model.py``: its parameters ``P``, its
``levels(state)`` and, where a part can be used as drawn, the part itself from ``build(state)``. They are fused into one
solid whose faces are sorted into named regions and written as one ASCII STL (metres) for snappyHexMesh. The enclosure's
inside (box or cube) is the blockMesh background, so its walls are not in the STL. Change the model and re-run: the
case follows.

What is simplified, and why (all within the parts' own envelopes unless stated):
  - the plate stack at the start of a build fills the Ø40 bore (the 0.1 mm gap round the plate is not meshed);
  - the overflow slot through the well block is a blind pocket 7 x 44 x 39 mm (the cup below it and the 1 mm gap
    between the cup and the block are closed);
  - the deck's rod hole and its pocket for the overflow cup are filled;
  - the recoater stage, its carriage and the 1 mm sheet shield are one solid block, the shield's outer envelope;
  - the hopper is solid (full of powder), and the silicone cord and its clamp are one 4 x 46 x 12 mm block on the bed;
  - the window stack under the lid (clamp ring, cover-slide holder, slide) is one solid with the holder's Ø40 bore
    open below the slide; the slide's underside is the 'slide' region; the pocket above the slide is not meshed;
  - the slot nozzle, drawn solid in the model, gets a straight 45 x 4 mm channel ``chan`` mm long whose back face is
    the inlet; the exhaust collector, drawn solid, gets a plenum behind its 50 x 6 mm opening and a 10 x 6 mm port
    (60 mm2, a 3/8 in. hose bore) whose end face is the outlet. Neither interior is designed yet (MK-11).
  - the well-block heaters' 2 mm stubs and the lid gasket's 1 mm gap are left out.
Variants for the cross-flow (``--slot-h``, ``--slot-z0``, ``--col-z1``, ``--lip``): see ``cfd_solids``.

Run (light, ~20 s):
    /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/geom.py --state FT-1 --out /tmp/ft-cfd/geom/ft1
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import cadquery as cq
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopLoc import TopLoc_Location

HERE = pathlib.Path(__file__).resolve().parent
FT = HERE.parents[1]                                   # desktop-lpbf/fast-track
sys.path.insert(0, str(FT / "cad"))
import ft_model as M                                   # noqa: E402
from lpbf_model import box, cyl                        # noqa: E402

V = cq.Vector


def enclosure(state):
    """Inside of the enclosure (x0, x1, y0, y1, z0, z1), mm: the box's inside to its rim (as ft_checks counts it), or
    the cube's 289.6 mm plate-to-plate inside."""
    P, L = M.P, M.levels(state)
    xc, yc = P["deck_c"]
    if state == "FT-1V":
        s = P["cube_in"] / 2
        return (xc - s, xc + s, yc - s, yc + s, L["floor_top"], L["roof_in"])
    bx, by, _ = P["box_in"]
    return (xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2, L["floor_top"], L["roof_in"])


def cfd_solids(state="FT-1", hx=None, slot_w=None, slot_h=None, slot_z0=2.0, chan=11.0, col_w=50.0, col_z0=2.0,
               col_z1=8.0, lip=0.0):
    """[(group, solid)] in mm. slot_*: nozzle slot width, height and its bottom's height above the bed (model: 45, 4, 2);
    col_*: collector opening width and z range above the bed (model: 50, 2-8); lip: a 2 mm hood that carries the
    collector's top wall this far upstream (0 = none)."""
    P, L = M.P, M.levels(state)
    parts = {p.name: p for p in M.build(state, 0.0, hx)}
    pick = lambda key: next(p.shape for n, p in parts.items() if n.startswith(key))
    hx = P["rc_travel"] / 2 if hx is None else hx
    sw, sh = P["nozzle_slot"]
    sw = sw if slot_w is None else slot_w
    sh = sh if slot_h is None else slot_h
    zb = L["dz"]                                        # powder plane
    deck_top = L["floor_top"] + P["deck_t"]
    blk_z0 = deck_top + P["so_l"]
    bw, bd, bh = P["well"]
    xc, yc = P["deck_c"]
    dx, dy = P["deck"]
    S = []
    # deck (rod hole and cup pocket filled); 1 mm below the floor so snappy sees it cross the boundary
    S.append(("deck", box(xc - dx / 2, xc + dx / 2, yc - dy / 2, yc + dy / 2, L["floor_top"] - 1.0, deck_top)))
    for sx in (-P["so_xy"], P["so_xy"]):
        for sy in (-P["so_xy"], P["so_xy"]):
            S.append(("block", cyl(P["so_d"] / 2, (sx, sy, deck_top - 0.5), "z", P["so_l"] + 1.0)))
    S.append(("block", cyl(P["rod_od"] / 2, (0, 0, deck_top - 0.5), "z", P["so_l"] + 1.0)))
    blk = box(-bw / 2, bw / 2, -bd / 2, bd / 2, blk_z0, zb)
    blk = blk.cut(box(P["ovf_x"][0], P["ovf_x"][1], -P["ovf_y"], P["ovf_y"], blk_z0 + 1.0, zb + 1.0))
    S.append(("block", blk))
    # slot nozzle: body as drawn (grown if the slot is), straight channel; feed boss and tube as drawn
    nz_top = max(8.0, slot_z0 + sh + 2.0)
    nzh = max(27.5, sw / 2 + 5.0)
    nz = box(-nzh, nzh, -46.0, -27.0, zb, zb + nz_top)
    nz = nz.cut(box(-sw / 2, sw / 2, -27.0 - chan, -26.0, zb + slot_z0, zb + slot_z0 + sh))
    S.append(("nozzle", nz))
    S.append(("nozzle", cyl(5, (0, -46, zb + 4), "-y", 6)))
    S.append(("pipes", pick("Argon feed tube to the nozzle")))
    # exhaust collector: body as drawn (grown if the opening is), plenum, 10 x 6 port; hose as drawn
    c_top = max(10.0, col_z1 + 2.0)
    ch = max(30.0, col_w / 2 + 5.0)
    col = box(-ch, ch, 27.0, 40.0, zb, zb + c_top)
    col = col.cut(box(-col_w / 2, col_w / 2, 26.0, 38.0, zb + col_z0, zb + col_z1))
    pz0 = zb + 0.5 * (col_z0 + col_z1) - 3.0
    col = col.cut(box(-5.0, 5.0, 37.9, 39.5, pz0, pz0 + 6.0))
    if lip > 0:
        col = col.fuse(box(-ch, ch, 27.0 - lip, 27.5, zb + col_z1, zb + col_z1 + 2.0))
    S.append(("collector", col))
    S.append(("pipes", pick("Exhaust hose to the HEPA")))
    # recoater: stage + carriage + shield as the shield's outer envelope; bracket and arm, hopper (solid), blade
    if state in ("FT-1", "FT-1V"):
        rl, ml, yr, rw, rh = P["rc_rail_l"], P["rc_motor_l"], P["rc_y"], P["rc_w"], P["rc_h"]
        ztop_car = deck_top + rh + P["rc_car"][2]
        S.append(("recoater", box(-rl / 2 - ml - 2, rl / 2 + 2, yr - rw / 2 - 4, yr + rw / 2 + 3, deck_top - 0.5,
                                  ztop_car + 4)))
        S.append(("recoater", pick("Carriage bracket and arm")))
        S.append(("recoater", pick("Vibration motor")))
        hl, hw, hh = P["hopper"]
        hop = (cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (hl / 2, hh), (-hl / 2, hh)]).close()
               .extrude(hw).val())
        hop = hop.fuse(cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (1.5, 2.0), (-1.5, 2.0)]).close()
                       .extrude(hw).val())
        S.append(("hopper", hop.translate(V(hx, hw / 2, zb))))
        S.append(("blade", box(hx - hl / 2 - 4, hx - hl / 2, -hw / 2, hw / 2, zb, zb + 12)))
    # window stack under the lid: one solid, the holder's bore open below the slide
    has_box = state != "FT-1V"
    cs_top = L["roof_in"] - (6.0 if has_box else 0.0)
    z_slide = cs_top - 5.5
    ws = cyl(35, (0, 0, cs_top - 10.0), "z", L["roof_in"] + 1.0 - (cs_top - 10.0))
    if has_box:
        ws = ws.fuse(cyl(50, (0, 0, L["roof_in"] - 5.0), "z", 6.0))      # inner clamp ring (z 135.5-141.5), to the rim
    ws = ws.cut(cyl(20, (0, 0, cs_top - 11.0), "z", z_slide - (cs_top - 11.0)))
    S.append(("window", ws))
    if state == "FT-1V":
        # the cube frame's 12 edge bars inside the plate-to-plate cube (frame minus the three 266 mm openings)
        S.append(("frame", pick("Ideal Vacuum 12 in. cube frame")))
    meta = dict(state=state, hx=hx, zb=zb, slot=dict(w=sw, h=sh, z0=slot_z0, chan=chan, y_exit=-27.0,
                                                    y_inlet=-27.0 - chan),
                collector=dict(w=col_w, z0=col_z0, z1=col_z1, y_face=27.0, port=(-5.0, 5.0, pz0, pz0 + 6.0),
                               y_outlet=39.5, lip=lip),
                z_slide=z_slide, slide_r=20.0, enclosure=enclosure(state), block=(bw, bd, bh),
                plate_d=P["plate_d"], build_d=30.0, ovf=(P["ovf_x"], P["ovf_y"]))
    return S, meta


def fuse_all(S):
    shapes = [s for _, s in S]
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.clean()


def classify(face, groups, meta):
    """Region name of a face of the fused solid."""
    c = face.Center()
    try:
        n = face.normalAt() if face.geomType() == "PLANE" else V(0, 0, 0)
    except Exception:
        n = V(0, 0, 0)
    zb = meta["zb"]
    sl, co = meta["slot"], meta["collector"]
    near = lambda a, b, t=1e-3: abs(a - b) < t
    if near(c.y, sl["y_inlet"]) and abs(c.x) < sl["w"] / 2 and zb + sl["z0"] < c.z < zb + sl["z0"] + sl["h"]:
        return "inlet"
    p = co["port"]
    if near(c.y, co["y_outlet"]) and p[0] < c.x < p[1] and p[2] < c.z < p[3]:
        return "outlet"
    if near(c.z, meta["z_slide"]) and math.hypot(c.x, c.y) < meta["slide_r"] + 0.5 and n.z < -0.9:
        return "slide"
    bw, bd, _ = meta["block"]
    if near(c.z, zb) and n.z > 0.9 and abs(c.x) <= bw / 2 + 1e-6 and abs(c.y) <= bd / 2 + 1e-6:
        return "bed"
    best = None
    for g, bb in groups:
        if bb.xmin - 1e-3 <= c.x <= bb.xmax + 1e-3 and bb.ymin - 1e-3 <= c.y <= bb.ymax + 1e-3 and \
                bb.zmin - 1e-3 <= c.z <= bb.zmax + 1e-3:
            vol = (bb.xmax - bb.xmin) * (bb.ymax - bb.ymin) * (bb.zmax - bb.zmin)
            if best is None or vol < best[1]:
                best = (g, vol)
    return best[0] if best else "walls_other"


def write_stl(solid, S, meta, path, tol=0.05, ang=0.25):
    """ASCII STL in metres, one 'solid <region>' per region; returns {region: [triangles, area mm2]}."""
    groups = [(g, s.BoundingBox()) for g, s in S]
    BRepMesh_IncrementalMesh(solid.wrapped, tol, False, ang, True)
    regions = {}
    for f in solid.Faces():
        name = classify(f, groups, meta)
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(f.wrapped, loc)
        if tri is None:
            continue
        trsf = loc.Transformation()
        pts = [tri.Node(i).Transformed(trsf) for i in range(1, tri.NbNodes() + 1)]
        rev = f.wrapped.Orientation().name == "TopAbs_REVERSED"
        lst = regions.setdefault(name, [])
        for i in range(1, tri.NbTriangles() + 1):
            a, b, c = tri.Triangle(i).Get()
            if rev:
                b, c = c, b
            lst.append(tuple((pts[k - 1].X(), pts[k - 1].Y(), pts[k - 1].Z()) for k in (a, b, c)))
    info = {}
    with open(path, "w") as fh:
        for name, tris in regions.items():
            fh.write(f"solid {name}\n")
            area = 0.0
            for (p0, p1, p2) in tris:
                u = [p1[i] - p0[i] for i in range(3)]
                v = [p2[i] - p0[i] for i in range(3)]
                n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
                ln = math.sqrt(sum(x * x for x in n)) or 1.0
                area += 0.5 * ln
                fh.write("facet normal %g %g %g\n outer loop\n" % tuple(x / ln for x in n))
                for p in (p0, p1, p2):
                    fh.write("  vertex %.7g %.7g %.7g\n" % tuple(x / 1000.0 for x in p))
                fh.write(" endloop\nendfacet\n")
            fh.write(f"endsolid {name}\n")
            info[name] = dict(triangles=len(tris), area_mm2=round(area, 1))
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", default="FT-1", choices=("FT-1", "FT-1V"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--slot-h", type=float, default=None)
    ap.add_argument("--slot-z0", type=float, default=2.0)
    ap.add_argument("--col-z1", type=float, default=8.0)
    ap.add_argument("--col-w", type=float, default=50.0)
    ap.add_argument("--lip", type=float, default=0.0)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    S, meta = cfd_solids(a.state, slot_h=a.slot_h, slot_z0=a.slot_z0, col_z1=a.col_z1, col_w=a.col_w, lip=a.lip)
    solid = fuse_all(S)
    info = write_stl(solid, S, meta, out / "ft.stl")
    e = meta["enclosure"]
    v_enc = (e[1] - e[0]) * (e[3] - e[2]) * (e[5] - e[4])
    reg = box(*e)
    v_sol = reg.intersect(solid).Volume()
    meta.update(regions=info, solid_volume_in_enclosure_L=round(v_sol / 1e6, 3), enclosure_L=round(v_enc / 1e6, 3),
                gas_L=round((v_enc - v_sol) / 1e6, 3), n_solids=len(solid.Solids()))
    (out / "geom.json").write_text(json.dumps(meta, indent=1, default=float))
    print(json.dumps({k: meta[k] for k in ("state", "gas_L", "enclosure_L", "n_solids")}), {k: v["triangles"] for k, v in info.items()})


if __name__ == "__main__":
    main()
