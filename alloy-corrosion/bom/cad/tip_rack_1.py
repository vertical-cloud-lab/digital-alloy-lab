"""Ben's tip rack 1 (the 20 uL rack on the CubXL deck now) as a printable STEP, and where its key
pockets put the PandaDeck's slot grid in CubOS coordinates. CadQuery 2.8.

Ben asked on #180 (2026-11-10) for the Onshape document "20uL tip rack" (vcl-shared > CubXL) as a
printable STEP, and to use where its key pills sit to judge where the rest of the deck sits.

**The Onshape document could not be opened from the runner.** The link goes to Onshape's sign-in
page, its API answers 403, and the runner has no Onshape login or API keys. So this file rebuilds the
rack that rack 1 was most likely made from:

- Cubware's 2 x 15 tip rack for 300 uL tips (Ursa-Laboratories/Cubware,
  cubxl_plus/labware/tip_rack_holder/TipRack.stl at 352aa95). Its envelope, hole grid and key
  pockets were measured from the mesh (`measure()`, numbers in STOCK below). Ben's deck files call
  rack 1 `panda_2x15_tip_rack`, this rack's model name.
- re-bored for 20 uL tips to Ben's profile on byu-vcl#151 (2026-08-01): a 5.0 -> 4.6 mm taper over
  16 mm, then a 3.1 mm exit bore (byu-vcl branch claude/issue-151-20260801-0017, f25e2ed). That
  re-bore changed nothing below the tip plate, so the key pockets are Cubware's.

The solid is drawn here from those dimensions; no mesh is copied. It leaves out the stock part's
end gussets. Cubware has no licence file.

The deck frame is CubOS's (origin front-left, +X right, +Y back, +Z up, mm). Rack 1's A1 and A2 are
Ben's taught positions, unchanged from 2026-10-02 to the 2026-11-05 stir-module deck
(byu-vcl cubos/configs/deck/stir_module_trial.yaml at 88fc07a).

    python tip_rack_1.py                      # STEP/STL, tip_rack_1.json, tip-rack-1.png
    python tip_rack_1.py --measure TipRack.stl  # re-measure Cubware's mesh (needs trimesh, shapely, networkx)
    python tip_rack_1.py --compare TipRack20uL.stl  # and compare with byu-vcl's 20 uL mesh (also manifold3d)
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cadquery as cq

import deck_keys as keys

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------ the stock rack, measured
# Cubware TipRack.stl is drawn 21 (x) x 66 (y, up) x 138 (z) mm, top face y = 0, underside y = -66.
# Sections of the mesh (measure()) give:
STOCK = {
    "source": "Ursa-Laboratories/Cubware cubxl_plus/labware/tip_rack_holder/TipRack.stl at 352aa95",
    "envelope_xyz_mm": [21.0, 66.0, 138.0],
    "hole_x": [6.25, 14.75],                         # two columns, 8.5 mm apart
    "hole_z": [-5.0 - 8.5 * k for k in range(15)],   # fifteen rows, -5 ... -124
    "pocket_x": 10.128,                              # mean of 10.136 and 10.119
    "pocket_z": [-34.867, -124.867],                 # 90.00 mm apart
    "pocket_corner": "toward -z (the row-A end)",
    "pocket_span_mm": [7.43, 6.73],                  # across two corners, corner to flat (mesh)
    "pocket_depth_mm": 2.05,
    "top_plate_mm": 18.0, "side_wall_mm": 2.0, "base_mm": 5.0,
    "stock_bore": "6.98 -> 6.42 mm over 16 mm, then 4.32 mm (300 uL)",
}

# ------------------------------------------------------------------ the rebuilt rack, rack frame
# Rack frame = deck orientation, origin at the rack's front-left-bottom corner. Row A is the row
# 14 mm from the front end (the stock rack's z = -124 row), and A1 is the right-hand column. That is
# the only way round that puts the pockets near the slot rows the other taught labware implies
# (turned 180 degrees they would sit 16 mm off). Mapping: X = 21 - x, Y = z + 138, Z = y + 66.
W, L, H = 21.0, 138.0, 66.0
PLATE_T, WALL_T, BASE_T = 18.0, 2.0, 5.0
PITCH = 8.5
COL_X = {"1": 21.0 - 6.25, "2": 21.0 - 14.75}     # A1 column x 14.75, A2 column x 6.25
ROW_Y0 = -124.0 + 138.0                           # row A at y 14, row O at y 133
ROWS = "ABCDEFGHIJKLMNO"
POCKETS_RACK = [(21.0 - STOCK["pocket_x"], z + 138.0) for z in sorted(STOCK["pocket_z"])]  # (10.872, 13.133), (10.872, 103.133)
POCKET_CORNER_DEG = -90.0                         # a corner toward -Y, as the stir module's

# Ben's 20 uL bore (byu-vcl#151, 2026-08-01): taper from the top face, then the exit bore.
BORE_TOP_D, BORE_TAPER_END_D, TAPER_L = 5.0, 4.6, 16.0
EXIT_D, EXIT_L = 3.1, 2.0

# ------------------------------------------------------------------ rack 1 on the deck (taught)
A1 = (291.332, 89.0)
A2 = (282.832, 89.0)
PICKUP_Z = 59.0


def hole_xy():
    return {f"{r}{c}": (COL_X[c], ROW_Y0 + PITCH * i) for i, r in enumerate(ROWS) for c in ("1", "2")}


def bore():
    """One bore's cutter, on the Z axis: one revolved profile, so the 30 cutters never overlap each other.
    The taper runs from the top face (z 66) down to z 50, then the exit bore down into the cavity. The
    taper is carried 0.5 mm past the top face at the same slope, so the cut is clean."""
    z_taper = H - TAPER_L
    slope = (BORE_TOP_D - BORE_TAPER_END_D) / 2 / TAPER_L
    over = 0.5
    pts = [(0.0, z_taper - EXIT_L - 0.5), (EXIT_D / 2, z_taper - EXIT_L - 0.5), (EXIT_D / 2, z_taper),
           (BORE_TAPER_END_D / 2, z_taper), (BORE_TOP_D / 2 + slope * over, H + over), (0.0, H + over)]
    s = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()
    bb = s.BoundingBox()
    assert abs(bb.zmin - (z_taper - EXIT_L - 0.5)) < 1e-6 and abs(bb.zmax - (H + over)) < 1e-6, (bb.zmin, bb.zmax)
    return s


def rack():
    """Print orientation: base on the bed, bores up. 21 x 138 x 66 mm."""
    body = cq.Workplane("XY").box(W, L, H, centered=False).val()
    cavity = cq.Solid.makeBox(W - 2 * WALL_T, L + 2.0, H - PLATE_T - BASE_T,
                              cq.Vector(WALL_T, -1.0, BASE_T))
    body = body.cut(cavity)
    body = body.cut(cq.Compound.makeCompound([bore().translate(cq.Vector(x, y, 0)) for x, y in hole_xy().values()]))
    for x, y in POCKETS_RACK:
        body = body.cut(keys.pocket_cutter(x, y, POCKET_CORNER_DEG, 0.0))
    return body.clean()


def to_deck(x, y, a1=A1):
    """Rack frame -> CubOS deck frame, from the taught A1 (the rack is square to the deck: A1 and A2 share y)."""
    return (a1[0] - COL_X["1"] + x, a1[1] - ROW_Y0 + y)


def grid_from_rack():
    pk = [to_deck(x, y) for x, y in POCKETS_RACK]
    x0 = sum(p[0] for p in pk) / 2 % keys.PITCH_X
    y0 = pk[0][1] % keys.PITCH_Y
    y0_signed = y0 - keys.PITCH_Y if y0 > keys.PITCH_Y / 2 else y0
    return pk, x0, y0, y0_signed


def keyed_parts(dx, dy):
    """Where each keyed part of the plan lands if the real grid is the planned one shifted by (dx, dy)."""
    out = {}
    for name, pts in keys.POCKETS.items():
        out[name] = {"planned_pockets": [[p[0], p[1]] for p in pts],
                     "pockets_land_at": [[round(p[0] + dx, 2), round(p[1] + dy, 2)] for p in pts]}
    return out


def deck_check(x0, y0):
    """The stirrer deck (../../stirrers/deck_stir.py, the current plan) with every keyed part on the slot grid
    rack 1's pockets set, and both tip racks drawn at their real outline (21 x 138, from 14 mm in front of
    row A). Rack 1 and the 9-position holder stay where Ben taught them; rack 2 is a second print of rack 1,
    keyed one slot column left. Reruns the rigid-head check and the 24 staged well fills."""
    import importlib.util
    import sys

    stir_path = HERE.parents[1] / "stirrers" / "deck_stir.py"
    spec = importlib.util.spec_from_file_location("deck_stir_rack1", stir_path)
    st = importlib.util.module_from_spec(spec)
    sys.modules["deck_stir_rack1"] = st
    spec.loader.exec_module(st)
    base, cu = st.base, st.cu
    dx, dy = x0 - keys.GRID_X0, (y0 - keys.PITCH_Y if y0 > keys.PITCH_Y / 2 else y0) - keys.GRID_Y0
    planned = {"stations": [[x, base.STATION_Y] for x in base.STATION_X], "cups": {k: list(v) for k, v in cu.CUPS.items()},
               "tubes_x": list(base.TUBE_X), "tubes_y": list(base.TUBE_Y), "tip_waste": list(cu.TIP_WASTE["c"]),
               "stirred_vials": {k: list(v) for k, v in st.stirred().items()}, "tip_rack_2": dict(st.TIP_RACK_2)}

    st.TIP_RACK_2 = {"a1": (A1[0] - keys.PITCH_X, A1[1]), "a2": (A2[0] - keys.PITCH_X, A2[1]), "pickup_z": PICKUP_Z}
    st.apply_layout()
    sh = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    r = base.TRAY["rect"]
    base.TRAY = {**base.TRAY, "rect": (r[0] + dx, r[1] + dy, r[2] + dx, r[3] + dy)}
    base.STATION_X = [x + dx for x in base.STATION_X]
    base.STATION_Y = base.STATION_Y + dy
    base.CUPS = {k: sh(v) for k, v in base.CUPS.items()}
    r = base.TUBE_RACK["rect"]
    base.TUBE_RACK = {**base.TUBE_RACK, "rect": (r[0] + dx, r[1] + dy, r[2] + dx, r[3] + dy)}
    base.TUBE_X = [x + dx for x in base.TUBE_X]
    base.TUBE_Y = [y + dy for y in base.TUBE_Y]
    base.TIP_WASTE = {**base.TIP_WASTE, "c": sh(base.TIP_WASTE["c"])}
    # stir modules: vial midway between two slot columns, on a slot row
    st.STIR_X = x0 + 2.5 * keys.PITCH_X
    st.STIR_Y = [(y0 % keys.PITCH_Y) + keys.PITCH_Y * k for k in range(4)]
    st.WELLS = {f"S{i}": (x, base.STATION_Y) for i, x in enumerate(base.STATION_X[:3], start=1)}
    st.TUBE = (base.TUBE_X[0], base.TUBE_Y[0])
    st.TIP_WASTE = base.TIP_WASTE["c"]
    base.rack_rect = lambda rk: (rk["a1"][0] - COL_X["1"], rk["a1"][1] - ROW_Y0, rk["a1"][0] - COL_X["1"] + W, rk["a1"][1] - ROW_Y0 + L)

    summary = base.check()
    moves, _ = st.move_check()
    r2 = lambda p: [round(p[0], 2), round(p[1], 2)]  # noqa: E731
    return {
        "shift_of_keyed_parts_mm": [round(dx, 3), round(dy, 3)],
        "planned": planned,
        "lands_at": {"stations": [r2((x, base.STATION_Y)) for x in base.STATION_X], "cups": {k: r2(v) for k, v in base.CUPS.items()},
                     "tubes_x": [round(x, 2) for x in base.TUBE_X], "tubes_y": [round(y, 2) for y in base.TUBE_Y],
                     "tip_waste": r2(base.TIP_WASTE["c"]), "stirred_vials": {k: r2(v) for k, v in st.stirred().items()},
                     "tip_rack_2": {"a1": r2(st.TIP_RACK_2["a1"]), "a2": r2(st.TIP_RACK_2["a2"])},
                     "tip_rack_outlines": {"rack 1": [round(v, 2) for v in base.rack_rect(base.TIP_RACK_1)],
                                           "rack 2": [round(v, 2) for v in base.rack_rect(st.TIP_RACK_2)]}},
        "not_moved": "tip rack 1 and the 9-position holder (taught); the potentiostat box (off the deck)",
        "rigid_head": {k: summary[k] for k in ("events_checked", "events_with_problems", "tightest_pass_mm")},
        "rigid_head_problems": [(e["event"], e["problems"]) for e in summary["events"] if e["problems"]],
        "staged_fills": {k: moves["staged"][k] for k in ("fills", "fills_passing", "worst_tip", "worst_carried_cap")},
        "unstaged_fills": {k: moves["unstaged"][k] for k in ("fills", "fills_passing")},
    }


def checks(shape):
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped, box, False, False)
    x0, y0, z0, x1, y1, z1 = box.Get()
    res = {"bbox_mm": [round(x1 - x0, 3), round(y1 - y0, 3), round(z1 - z0, 3)],
           "volume_mm3": round(shape.Volume(), 1), "solids": len(shape.Solids()), "valid": shape.isValid()}
    # each bore: open at the top at 5.0 mm, 4.6 at the end of the taper, 3.1 below; probe with thin discs
    probes = {}
    mid = (BORE_TOP_D + BORE_TAPER_END_D) / 2
    for label, z, d_open, d_closed in (("mouth, z 65.9", 65.9, BORE_TOP_D - 0.02, BORE_TOP_D + 0.03),
                                       ("mid taper, z 58", 58.0, mid - 0.02, mid + 0.03),
                                       ("taper end, z 50.05", 50.05, BORE_TAPER_END_D - 0.02, BORE_TAPER_END_D + 0.03),
                                       ("exit bore, z 49", 49.0, EXIT_D - 0.02, EXIT_D + 0.03)):
        empty = filled = 0
        for x, y in hole_xy().values():
            inner = cq.Solid.makeCylinder(d_open / 2, 0.05, cq.Vector(x, y, z))
            ring = cq.Solid.makeCylinder(d_closed / 2, 0.05, cq.Vector(x, y, z)).cut(inner)
            empty += shape.intersect(inner).Volume() < 1e-6
            filled += shape.intersect(ring).Volume() > 0.5 * ring.Volume()
        probes[label] = {"bores_open_at_d": d_open, "open": empty, "walled_by_d": d_closed, "walled": filled}
    res["bore_probes"] = probes
    res["pockets"] = []
    for x, y in POCKETS_RACK:
        pocket = keys.rounded_triangle(keys.POCKET_R, 0.0, keys.POCKET_DEPTH, x, y, POCKET_CORNER_DEG)
        res["pockets"].append({"x": round(x, 3), "y": round(y, 3),
                               "empty_mm3": round(shape.intersect(pocket).Volume(), 4),
                               "pocket_mm3": round(pocket.Volume(), 2)})
    return res


def measure(stl_path):
    """Re-measure Cubware's TipRack.stl (the source of STOCK): hole and pocket centres, from mesh sections."""
    import numpy as np
    import trimesh
    from shapely.geometry import Polygon

    m = trimesh.load(stl_path)

    def rings(y):
        s = m.section(plane_origin=[0, y, 0], plane_normal=[0, 1, 0])
        p, T = s.to_2D()
        out = []
        for poly in p.polygons_full:
            for ring in poly.interiors:
                pts = np.array(ring.coords)
                xyz = (T @ np.c_[pts, np.zeros(len(pts)), np.ones(len(pts))].T).T[:, :3]
                pg = Polygon(xyz[:, [0, 2]])
                out.append({"x": round(pg.centroid.x, 3), "z": round(pg.centroid.y, 3), "area": round(pg.area, 2),
                            "x_span": round(float(np.ptp(xyz[:, 0])), 3), "z_span": round(float(np.ptp(xyz[:, 2])), 3)})
        return out

    top, bottom = rings(-0.05), rings(-65.5)
    return {"bounds": m.bounds.round(3).tolist(), "n_holes_top": len(top),
            "hole_x": sorted({h["x"] for h in top}), "hole_z": sorted({h["z"] for h in top}),
            "pockets": bottom}


def compare(stl_path, ours_stl):
    """Our rack against byu-vcl's TipRack20uL.stl (f25e2ed), the 20 uL re-bore of the stock mesh: volumes of
    the two differences, after moving ours into the stock frame (x = 21 - X, y = Z - 66, z = Y - 138)."""
    import numpy as np
    import trimesh

    theirs = trimesh.load(stl_path)
    ours = trimesh.load(ours_stl)
    T = np.array([[-1, 0, 0, 21.0], [0, 0, 1, -66.0], [0, 1, 0, -138.0], [0, 0, 0, 1.0]])
    ours.apply_transform(T)
    only_theirs = trimesh.boolean.difference([theirs, ours], engine="manifold")
    only_ours = trimesh.boolean.difference([ours, theirs], engine="manifold")
    pieces = sorted((round(float(c.volume), 2), [round(float(v), 2) for v in c.bounds[0]], [round(float(v), 2) for v in c.bounds[1]])
                    for c in only_theirs.split(only_watertight=False) if abs(c.volume) > 1.0)[::-1]
    return {"theirs": str(stl_path), "theirs_watertight": bool(theirs.is_watertight), "theirs_volume_mm3": round(float(theirs.volume), 1),
            "ours_volume_mm3": round(float(ours.volume), 1),
            "in_theirs_not_ours_mm3": round(float(only_theirs.volume), 2),
            "in_ours_not_theirs_mm3": round(float(only_ours.volume), 2),
            "largest_pieces_in_theirs_not_ours (volume, min xyz, max xyz in their frame)": pieces[:6]}


def plot(shape_info, pk, grid, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Polygon as MPoly, Rectangle

    x0, y0 = grid
    fig, (a, b) = plt.subplots(1, 2, figsize=(11.5, 6.6), gridspec_kw={"width_ratios": [1, 2.1]})

    def tri(ax, cx, cy, r, **kw):
        pts = [(cx + r * math.cos(math.radians(POCKET_CORNER_DEG + 120 * k)),
                cy + r * math.sin(math.radians(POCKET_CORNER_DEG + 120 * k))) for k in range(3)]
        ax.add_patch(MPoly(pts, closed=True, **kw))

    # A: the rack from above, pockets dashed (they are underneath)
    a.add_patch(Rectangle((0, 0), W, L, fc="#e8edf2", ec="#334", lw=1.2))
    for name, (x, y) in hole_xy().items():
        a.add_patch(plt.Circle((x, y), BORE_TOP_D / 2, fc="white", ec="#556", lw=0.7))
        if name in ("A1", "A2", "O1", "O2"):
            a.text(x, y, name, ha="center", va="center", fontsize=5.5)
    for x, y in POCKETS_RACK:
        tri(a, x, y, keys.TRI_R + keys.POCKET_R, fc="none", ec="#c0392b", lw=1.1, ls="--")
        a.add_patch(FancyBboxPatch((x - keys.PILL_W / 2 + 2.5, y - keys.PILL_L / 2 + 2.5), keys.PILL_W - 5, keys.PILL_L - 5,
                                   boxstyle="round,pad=2.5", fc="none", ec="#c0392b", lw=0.6, ls=":"))
    a.text(W + 2, POCKETS_RACK[0][1], "pocket 3.88 mm left of\nthe A1 column, 0.87 mm\nin front of row A",
           fontsize=6.3, va="center", color="#c0392b")
    a.text(W + 2, POCKETS_RACK[1][1], "second pocket\n90.00 mm behind", fontsize=6.3, va="center", color="#c0392b")
    a.text(W / 2, L + 4, "21 x 138 x 66 mm, bores up", ha="center", fontsize=7.5)
    a.text(W / 2, -7, "front (-Y)", ha="center", fontsize=7)
    a.set_xlim(-6, W + 30)
    a.set_ylim(-11, L + 9)
    a.set_aspect("equal")
    a.axis("off")
    a.set_title("A  Rack 1, rebuilt: 30 bores, and the two\nkey pockets underneath (red, dashed)", fontsize=8.5, loc="left")

    # B: the deck around rack 1, slot grid from its pockets (solid) and the earlier estimate (grey)
    xmin, xmax, ymin, ymax = 160, 400, 20, 270
    for n in range(-1, 18):
        for m_ in range(-1, 8):
            for gx, gy, col, ls, lw in ((keys.GRID_X0, keys.GRID_Y0, "#999", ":", 0.7), (x0, y0, "#2c3e50", "-", 0.9)):
                cx, cy = gx + keys.PITCH_X * n, gy + keys.PITCH_Y * m_
                if xmin - 10 < cx < xmax + 10 and ymin - 20 < cy < ymax + 20:
                    b.add_patch(FancyBboxPatch((cx - keys.SLOT_W / 2 + 5, cy - keys.SLOT_L / 2 + 5), keys.SLOT_W - 10, keys.SLOT_L - 10,
                                               boxstyle="round,pad=5", fc="none", ec=col, lw=lw, ls=ls))
    r0 = to_deck(0, 0)
    b.add_patch(Rectangle(r0, W, L, fc="#d6e4f0", ec="#1f4e79", lw=1.2, alpha=0.9))
    b.add_patch(Rectangle((r0[0] - keys.PITCH_X, r0[1]), W, L, fc="#eaf2e3", ec="#3c763d", lw=1.0, ls="--"))
    for x, y in hole_xy().values():
        dx, dy = to_deck(x, y)
        b.add_patch(plt.Circle((dx, dy), 1.6, fc="white", ec="#1f4e79", lw=0.4))
        b.add_patch(plt.Circle((dx - keys.PITCH_X, dy), 1.6, fc="white", ec="#3c763d", lw=0.4))
    for px, py in pk:
        tri(b, px, py, keys.TRI_R + keys.POCKET_R, fc="#c0392b", ec="none")
        tri(b, px - keys.PITCH_X, py, keys.TRI_R + keys.POCKET_R, fc="#3c763d", ec="none")
    b.plot(*A1, "k+", ms=7)
    box = dict(fc="white", ec="none", alpha=0.85, pad=1.2)
    b.text(A1[0] + 9, A1[1] - 6, f"rack 1 A1, taught\n({A1[0]:.3f}, {A1[1]:.0f})", fontsize=6.5, bbox=box)
    b.text(r0[0] + W / 2, r0[1] + L + 4, "rack 1", fontsize=7, color="#1f4e79", ha="center", bbox=box)
    b.text(r0[0] - keys.PITCH_X + W / 2 - 4, r0[1] + L + 4, "rack 2: a second print,\none slot column left,\nA1 (266.332, 89)",
           fontsize=6.5, color="#3c763d", ha="right", bbox=box)
    b.set_title("B  Rack 1 on the deck: its key pockets (red) fix the slot grid\n"
                f"solid: slots from rack 1, X = {x0:.2f} + 25n, Y = {y0:.2f} + 45m.  "
                f"Dotted: the earlier estimate, {keys.GRID_X0:.1f} + 25n, {keys.GRID_Y0:.0f} + 45m",
                fontsize=8, loc="left")
    b.set_xlim(xmin, xmax)
    b.set_ylim(ymin, ymax)
    b.set_aspect("equal")
    b.set_xlabel("deck X (mm, CubOS)", fontsize=8)
    b.set_ylabel("deck Y (mm)", fontsize=8)
    b.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(out_png, dpi=170)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", help="Cubware's TipRack.stl, to re-measure STOCK")
    ap.add_argument("--compare", help="byu-vcl's TipRack20uL.stl (f25e2ed), to compare with the rebuild")
    args = ap.parse_args()
    if args.measure:
        print(json.dumps(measure(args.measure), indent=1))
        return

    shape = rack()
    name = "tip_rack_1_20ul"
    cq.exporters.export(cq.Workplane().add(shape), str(HERE / f"{name}.step"))
    cq.exporters.export(cq.Workplane().add(shape), str(HERE / f"{name}.stl"), tolerance=0.01, angularTolerance=0.1)
    chk = checks(shape)

    pk, x0, y0, y0s = grid_from_rack()
    dx, dy = x0 - keys.GRID_X0, y0s - keys.GRID_Y0
    holes = hole_xy()
    out = {
        "what": "Ben's tip rack 1, rebuilt from Cubware's TipRack and Ben's 20 uL bore (the Onshape document "
                "could not be opened from the runner); and the slot grid its key pockets imply",
        "stock_rack_measured": STOCK,
        "rebuilt": {"file": f"{name}.step", "frame": "deck orientation, origin front-left-bottom; print as is (base on the bed)",
                    "envelope_mm": [W, L, H], "plate_wall_base_mm": [PLATE_T, WALL_T, BASE_T],
                    "bore": {"top_d": BORE_TOP_D, "taper_end_d": BORE_TAPER_END_D, "taper_l": TAPER_L,
                             "exit_d": EXIT_D, "exit_l": EXIT_L},
                    "A1": list(holes["A1"]), "A2": list(holes["A2"]), "O1": list(holes["O1"]),
                    "pockets": [[round(x, 3), round(y, 3)] for x, y in POCKETS_RACK],
                    "pocket_shape": "deck_keys.py's (R1.1 rounded triangle, 2.1 deep), a corner toward -Y",
                    "left_out": "the stock part's end gussets", "checks": chk},
        "on_the_deck": {
            "taught": {"A1": list(A1), "A2": list(A2), "pickup_z": PICKUP_Z,
                       "source": "byu-vcl cubos/configs/deck/stir_module_trial.yaml at 88fc07a (unchanged since 2026-10-02)"},
            "rack_outline": [round(v, 3) for v in (*to_deck(0, 0), *to_deck(W, L))],
            "pockets": [[round(p[0], 3), round(p[1], 3)] for p in pk],
            "slot_grid": {"x0_mod_25": round(x0, 3), "y0_mod_45": round(y0, 3), "y0_signed": round(y0s, 3),
                          "slot_columns_x": [round(x0 + 25 * n, 2) for n in range(17)],
                          "slot_rows_y": [round(y0 + 45 * m - 45, 2) for m in range(8) if 0 <= y0 + 45 * m - 45 <= 330]},
            "vs_earlier_estimate": {"earlier": [keys.GRID_X0, keys.GRID_Y0], "shift_mm": [round(dx, 3), round(dy, 3)],
                                    "other_evidence": keys.GRID_EVIDENCE},
            "rack_2_as_a_second_print": {"one_column_left": {"A1": [round(A1[0] - 25, 3), A1[1]], "A2": [round(A2[0] - 25, 3), A2[1]]},
                                         "outline": [round(v, 3) for v in (to_deck(0, 0)[0] - 25, to_deck(0, 0)[1],
                                                                           to_deck(W, L)[0] - 25, to_deck(W, L)[1])]},
            "keyed_parts": keyed_parts(dx, dy),
            "deck_check": deck_check(x0, y0),
        },
    }
    if args.compare:
        out["rebuilt"]["vs_byu_vcl_TipRack20uL"] = compare(args.compare, HERE / f"{name}.stl")
        out["rebuilt"]["vs_byu_vcl_TipRack20uL"]["theirs"] = ("byu-vcl hardware/cubxl/ursa_tip_rack_20ul/TipRack20uL.stl "
                                                              "at f25e2ed (branch claude/issue-151-20260801-0017)")
    elif (HERE / "tip_rack_1.json").exists():   # keep the last comparison
        prev = json.loads((HERE / "tip_rack_1.json").read_text())["rebuilt"].get("vs_byu_vcl_TipRack20uL")
        if prev:
            out["rebuilt"]["vs_byu_vcl_TipRack20uL"] = prev
    (HERE / "tip_rack_1.json").write_text(json.dumps(out, indent=1) + "\n")
    plot(chk, pk, (x0, y0), HERE / "tip-rack-1.png")
    print(json.dumps({k: out["on_the_deck"][k] for k in ("rack_outline", "pockets", "slot_grid", "vs_earlier_estimate")}, indent=1)[:2500])
    print(json.dumps(chk, indent=1))


if __name__ == "__main__":
    main()
