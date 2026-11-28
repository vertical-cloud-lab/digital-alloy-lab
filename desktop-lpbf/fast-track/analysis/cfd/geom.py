"""Gas-side geometry of the fast-track machines for OpenFOAM, taken from the CadQuery model (issue #260, PR 294).

The solids that bound the gas inside the enclosure are built from ``cad/ft_model.py``: its parameters ``P``, its
``levels(state)``, the vendor dimensions in ``cad/ft_vendor.py`` and, where a part can be used as drawn, the part itself
from ``build(state)``. They are fused into one solid whose faces are sorted into named regions and written as one ASCII
STL (metres) for snappyHexMesh. The enclosure's inside (box or cube) is the blockMesh background, so its walls are not in
the STL. Change the model and re-run: the case follows.

Round 3 (2026-11-28): ported to CAD v2, the round-2 model (the Saginaw SCE-16EL1208SSLP box with its dished door, the
Zaber X-LSM100B recoater, the 245 mm deck, the window stack and the Ø44 cover-slide holder at y = -11 mm, the cube's drop
tube at y = -16 mm). The round-1 version (v1) is in git history (commit a6f057d).

What is simplified, and why (all within the parts' own envelopes unless stated):
  - box: the gas goes up to the door's inner face (8.30 in. above the floor). The body's 22 mm rim lip, the poured
    gasket's inner face (8 x 4 mm section, est.) and the door's dish are one solid ('lid') round it, so the gas above
    the walls is as drawn; the concealed hinges and the latch are 'lid' too;
  - the plate stack at the start of a build fills the Ø40 bore (the 0.1 mm gap round the plate is not meshed);
  - the overflow slot through the well block is a blind pocket 7 x 44 x 39 mm (the cup below it and the 1 mm gap
    between the cup and the block are closed);
  - the deck's rod hole, its overflow pocket, its gland taps and its M6 clearance holes are filled;
  - the X-LSM100B, its carriage and the 1 mm sheet shield (MK-12) are one block, the shield's outer envelope, plus the
    stage's motor end (end plate, motor, controller box, end connector) as the vendor's boxes (ft_vendor.LSM), set
    down on the deck (the motor's 0.67 mm gap under it closed); the side M8 connectors and the cable are left out;
  - the hopper is solid (full of powder), and the silicone cord and its clamp are one 4 x 46 x 12 mm block on the bed;
  - the window stack (box: the inner clamp ring and the cover-slide holder; cube: the drop tube, its flange and the
    holder) is one solid with the holder's Ø44 bore open below the slide; the slide's underside is the 'slide' region;
    the pocket above the slide is not meshed;
  - the slot nozzle, drawn solid in the model, gets a straight 45 x 4 mm channel ``chan`` mm long whose back face is
    the inlet; the exhaust collector, drawn solid, gets a plenum behind its 50 x 6 mm opening and a 10 x 6 mm port
    (60 mm2, a 3/8 in. hose bore) whose end face is the outlet. Neither interior is designed yet (MK-11);
  - left out (each a few mm across or under ~2 cm3 of gas): the well-block heaters' stubs, the heater/TC leads and the
    recoater's M8 cable, the box-air thermocouple, the light-port and camera-port recesses in the walls and the door
    (their window rings are outside), the gas bulkheads' bores, the cube's deck screws and KF-25 port bores;
  - the purge ports (a low diffuser, a high vent) are not in the model: make_case.py carves them out of the walls
    (round 2's recommendation, parts.csv G9). geom.json's 'wall_top' keeps the vent under the box's rim lip.
Variants for the cross-flow (``--slot-h``, ``--slot-z0``, ``--col-z0``, ``--col-z1``, ``--lip``): see ``cfd_solids``.

Run (light, ~20-40 s):
    /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/geom.py --state FT-1 --out /tmp/r3-cfd/geom/ft1
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
import ft_vendor as VEN                                # noqa: E402
from lpbf_model import box, cyl                        # noqa: E402

V = cq.Vector


def enclosure(state):
    """Inside of the enclosure (x0, x1, y0, y1, z0, z1), mm: the box's inside from the floor to the door's inner face,
    or the cube's 289.6 mm plate-to-plate inside."""
    P, L = M.P, M.levels(state)
    xc, yc = P["deck_c"]
    if state == "FT-1V":
        s = P["cube_in"] / 2
        return (xc - s, xc + s, yc - s, yc + s, L["floor_top"], L["roof_in"])
    bx, by, _ = P["box_in"]
    return (xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2, L["floor_top"], L["roof_in"])


def lid_solid(state):
    """Box only: everything round the gas above the walls, as one solid (the rim lip, the gasket, the door's dish), and
    the seam (the gasket's inner face) for the leak runs."""
    P, L = M.P, M.levels(state)
    S = VEN.SAG
    xc, yc = P["deck_c"]
    t = S["t"]
    ix, iy = P["box_in"][0], P["box_in"][1]
    rim = L["rim"]
    lip = S["lip"]
    gw, gh = S["gasket"]
    dx, dy = S["door"]
    zt = L["roof_in"]
    gix, giy = dx / 2 - 4 - gw, dy / 2 - 4 - gw          # the gasket's inner face
    dix, diy = dx / 2 - t, dy / 2 - t                    # the door dish's inner faces
    s = box(xc - ix / 2 - 2, xc + ix / 2 + 2, yc - iy / 2 - 2, yc + iy / 2 + 2, rim - t, zt + 2)
    s = s.cut(box(xc - ix / 2 + lip, xc + ix / 2 - lip, yc - iy / 2 + lip, yc + iy / 2 - lip, rim - t - 1, rim + 0.01))
    s = s.cut(box(xc - gix, xc + gix, yc - giy, yc + giy, rim - 0.01, rim + gh + 0.01))
    s = s.cut(box(xc - dix, xc + dix, yc - diy, yc + diy, rim + gh - 0.01, zt + 3))
    seam = dict(x=(xc - gix, xc + gix), y=(yc - giy, yc + giy), z=(rim, rim + gh),
                perimeter_mm=round(4 * (gix + giy), 1), gasket_w_mm=gw, gasket_h_mm=gh)
    return s, seam, rim - t


def cfd_solids(state="FT-1", hx=None, slot_w=None, slot_h=None, slot_z0=2.0, chan=11.0, col_w=50.0, col_z0=2.0,
               col_z1=8.0, lip=0.0):
    """[(group, solid)] in mm. slot_*: nozzle slot width, height and its bottom's height above the bed (model: 45, 4, 2);
    col_*: collector opening width and z range above the bed (model: 50, 2-8); lip: a 2 mm hood that carries the
    collector's top wall this far upstream (0 = none)."""
    P, L = M.P, M.levels(state)
    hx = P["hx_default"] if hx is None else hx
    parts = {p.name: p for p in M.build(state, 0.0, hx)}

    def pick(key):
        return next(p.shape for n, p in parts.items() if n.startswith(key))

    sw, sh = P["nozzle_slot"]
    sw = sw if slot_w is None else slot_w
    sh = sh if slot_h is None else slot_h
    zb = L["dz"]                                        # powder plane
    deck_top = L["floor_top"] + P["deck_t"]
    blk_z0 = deck_top + P["so_l"]
    bw, bd, bh = P["well"]
    xc, yc = P["deck_c"]
    dx, dy = P["deck"]
    cube = state == "FT-1V"
    S = []
    # deck (rod hole, pockets, taps and holes filled); 1 mm below the floor so snappy sees it cross the boundary
    S.append(("deck", box(xc - dx / 2, xc + dx / 2, yc - dy / 2, yc + dy / 2, L["floor_top"] - 1.0, deck_top)))
    if not cube:
        for key in ("Deck clamps on the panel studs", "Stud nuts", "Panel studs"):
            S.append(("deck", pick(key)))
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
    # recoater: X-LSM100B + carriage + shield as the shield's outer envelope, the motor end as the vendor's boxes;
    # bracket and arm, vibration motor as drawn; hopper (solid), blade
    yr, x0r = P["rc_y"], P["rc_x0"]
    car_top = deck_top + P["rc_h"]
    sz = car_top + 8.0                                  # the shield's top sheet (MK-12), 1 mm thick
    xa, xb = x0r - 78.0, x0r + 88.0
    S.append(("recoater", box(xa, xb, yr - 26.0, yr + 25.0, deck_top - 0.5, sz + 1.0)))
    LS = VEN.LSM
    ep, mo, cb, ce = LS["endplate"], LS["motor"], LS["box"], LS["conn_end"]
    S.append(("recoater", box(x0r + ep[0], x0r + ep[1] + 0.5, yr - 22.2, yr + 42.8, deck_top - 0.5, deck_top + 20.75)))
    S.append(("recoater", box(x0r + mo[0], x0r + mo[1] + 0.5, yr - 10.0, yr + 10.0, deck_top - 0.5, deck_top + 20.67)))
    S.append(("recoater", box(x0r + cb[0], x0r + cb[1] + 0.5, yr + cb[2], yr + cb[3], deck_top - 0.5, deck_top + 20.75)))
    S.append(("recoater", box(x0r + ce[0], x0r + ce[1] + 0.5, yr + ce[2], yr + ce[3], deck_top + ce[4], deck_top + ce[5])))
    S.append(("recoater", pick("Carriage bracket and arm")))
    S.append(("recoater", pick("Vibration motor")))
    hl, hw, hh = P["hopper"]
    hop = (cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (hl / 2, hh), (-hl / 2, hh)]).close()
           .extrude(hw).val())
    hop = hop.fuse(cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (1.5, 2.0), (-1.5, 2.0)]).close()
                   .extrude(hw).val())
    S.append(("hopper", hop.translate(V(hx, hw / 2, zb))))
    S.append(("blade", box(hx - hl / 2 - 4, hx - hl / 2, -hw / 2, hw / 2, zb, zb + 12)))
    # window stack: one solid, the holder's Ø44 bore open below the slide (centres from the model)
    csx, csy = P["cs_c"]
    z_slide = zb + P["cs_z"]                            # the slide's lower face
    r_open = P["cs_id"] / 2
    zt = L["roof_in"]
    if not cube:
        wx, wy = M.window_centre(state)
        ws = cyl(35, (csx, csy, z_slide - 4.5), "z", zt + 1.0 - (z_slide - 4.5))          # holder, up to the ring
        ws = ws.fuse(cyl(50, (wx, wy, zt - 6.0), "z", 7.0))                               # inner clamp ring (to the door)
    else:
        dtx, dty = P["cs_drop_c"]
        cs_top = z_slide + 10.0
        ws = cyl(35, (csx, csy, z_slide - 4.5), "z", cs_top - (z_slide - 4.5) + 0.5)       # holder
        ws = ws.fuse(cyl(32, (dtx, dty, cs_top), "z", zt + 1.0 - cs_top))                 # drop tube
        ws = ws.fuse(cyl(45, (dtx, dty, zt - 5.0), "z", 6.0))                             # its flange under the plate
    ws = ws.cut(cyl(r_open, (csx, csy, z_slide - 6.0), "z", 6.0))
    S.append(("window", ws))
    wall_top = zt
    seam = None
    if cube:
        # the cube frame's 12 edge bars inside the plate-to-plate cube (frame minus the three 266 mm openings)
        S.append(("frame", pick("Ideal Vacuum 12 in. cube frame")))
    else:
        lid, seam, wall_top = lid_solid(state)
        S.append(("lid", lid))
        S.append(("lid", pick("Concealed hinges")))
        S.append(("lid", pick("Quarter-turn latch")))
    enc = enclosure(state)
    meta = dict(state=state, model="CAD v2 (round 2, ft_model.py at the round-3 head)", hx=hx, zb=zb,
                slot=dict(w=sw, h=sh, z0=slot_z0, chan=chan, y_exit=-27.0, y_inlet=-27.0 - chan),
                collector=dict(w=col_w, z0=col_z0, z1=col_z1, y_face=27.0, port=(-5.0, 5.0, pz0, pz0 + 6.0),
                               y_outlet=39.5, lip=lip),
                z_slide=z_slide, slide_r=r_open, slide_c=(csx, csy), enclosure=enc, wall_top=wall_top,
                port_margin=15.0 if cube else 3.0, seam=seam, block=(bw, bd, bh),
                plate_d=P["plate_d"], build_d=30.0, ovf=(P["ovf_x"], P["ovf_y"]), deck_top=deck_top)
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
    sx, sy = meta.get("slide_c", (0.0, 0.0))
    if near(c.z, meta["z_slide"]) and math.hypot(c.x - sx, c.y - sy) < meta["slide_r"] + 0.5 and n.z < -0.9:
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
    ap.add_argument("--col-z0", type=float, default=2.0)
    ap.add_argument("--col-z1", type=float, default=8.0)
    ap.add_argument("--col-w", type=float, default=50.0)
    ap.add_argument("--lip", type=float, default=0.0)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    S, meta = cfd_solids(a.state, slot_h=a.slot_h, slot_z0=a.slot_z0, col_z0=a.col_z0, col_z1=a.col_z1, col_w=a.col_w,
                          lip=a.lip)
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
