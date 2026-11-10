"""Deck keys for the corrosion setup's printed deck parts, and the pockets they press into. CadQuery 2.8.

Ben asked on #180 (2026-11-09) for key slots under every printed part that goes on the CubXL deck,
with matching deck keys, using the stir modules' press fit. The key is the stir module's
(byu-vcl hardware/vial-stirrer-cubxl, README "The key nub and pocket", at 4d5446c):

- a pill, 9.8 x 24.8 x 10 mm with R4.9 ends, long axis along deck Y, that drops into one of the
  PandaDeck's 10 x 25 mm slots with 0.1 mm of play a side and is held by gravity;
- on top of it a 2.0 mm rounded-triangle nub (equilateral, 3.1 mm circumradius before rounding,
  0.3 mm x 45 degree lead-in round its top) that presses into a 2.1 mm pocket under the part.
  The pocket's corners are R1.1; the nub's are R1.1 + KEY_PRESS. Ben's fit test on 2026-10-22
  (0.05, 0.10 and 0.15 mm a side, PETG on the A1 mini) picked 0.05 mm, so KEY_PRESS is 0.05.
- dimples in the pill's top face at the end away from the nub's corner, one per 0.05 mm of
  press, so the keys can be told apart.

The PandaDeck (Cubware PandaDeck.step at 352aa95) has its slots on a 25 mm (X) x 45 mm (Y) grid.
Where that grid sits in the CubOS frame of Ben's 2026-10-02 calibration is inferred from three
keyed things he taught (GRID_EVIDENCE); they agree to about 1 mm in X and 2 mm in Y. GRID_X0 and
GRID_Y0 are a best estimate, not a measurement: every part lands within about 2 mm of its planned
position, and each position is taught on the deck once the parts are in, like any new labware.

Each part's pockets sit at slot centres under the part, in the deck (D) frame the part is drawn
in, so a keyed part lands where the deck plan puts it. POCKETS lists them; the CAD scripts
(../../copper/cad/cad_cu_cell.py for the tray, cad_build_parts.py for the rest) cut them.

    python deck_keys.py      # writes deck_key*.step/.stl and checks every part's pockets
                             # (run cad_build_parts.py and ../../copper/cad/cad_cu_cell.py first)
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------ the deck
PITCH_X, PITCH_Y = 25.0, 45.0      # PandaDeck slot grid
SLOT_W, SLOT_L = 10.0, 25.0        # pill slots, R5 ends, long axis along Y
DECK_T = 10.0                      # plate thickness in the STEP (not measured on the CubXL)
GRID_X0, GRID_Y0 = 12.5, 0.0       # slot centres at X = 12.5 + 25 n, Y = 45 m (CubOS frame, best estimate)
GRID_EVIDENCE = [
    {"what": "Ben's 2026-10-02 deck: vial_1 of the Cubware 9-vial holder at (136.668, 45)",
     "why": "Cubware's 9VialHolder.step has a key pocket directly under its first vial (and one 225 mm along)",
     "slot_x_mod_25": 11.67, "slot_y_mod_45": 0.0},
    {"what": "Ben's tip rack 1 (panda_2x15_tip_rack, Cubware TipRack.stl): A1 (291.332, 89), A2 (282.832, 89)",
     "why": "TipRack.stl has two pockets 90 mm apart, 3.86 mm from the A1 column toward A2 and 0.86 mm "
            "past the A1 row; tip pick-up needs about 1 mm, so this is the most precisely taught of the three",
     "slot_x_mod_25": 12.45, "slot_y_mod_45": 43.14},
    {"what": "Ben's 2026-11-05 stir-module trial: the stirred vial at (126, 45)",
     "why": "the compact stirrer's two keys are 12.5 mm either side of its vial, on the vial's row",
     "slot_x_mod_25": 13.5, "slot_y_mod_45": 0.0},
]

# ------------------------------------------------------------------ the key (byu-vcl's stir-module key)
PILL_W, PILL_L, PILL_H = 9.8, 24.8, 10.0
TRI_R = 3.1                        # sharp triangle's circumradius
POCKET_R = 1.1                     # pocket corner radius (Cubware's)
POCKET_DEPTH = 2.1
NUB_H, NUB_LEAD = 2.0, 0.3         # nub height; 45 degree lead-in round its top
KEY_PRESS = 0.05                   # nub = pocket grown this much all round (Ben's pick, 2026-10-22)
FIT_TEST = (0.10, 0.15)            # the other two sizes from the fit test
DIMPLE_D, DIMPLE_DEPTH, DIMPLE_Y = 1.2, 0.4, 8.5
CORNER_DEG = -90.0                 # the triangle's reference corner points toward -Y

# Walls the checks ask for round each pocket: in the part's plane, and above the pocket's ceiling.
MIN_WALL, MIN_CEILING = 1.5, 0.8

# ------------------------------------------------------------------ the pockets, deck (D) frame
# name: (x, y, corner direction in degrees, z of the part's underside). corner -90: a corner toward -Y,
# as the stir module's; +90: turned round, with a flat toward -Y where a part's front edge is close.
POCKETS = {
    "coupon_tray": [(187.5, 225.0, 90.0, 0.0), (262.5, 225.0, 90.0, 0.0)],
    "cup_block_3": [(37.5, 225.0, -90.0, 0.0), (87.5, 225.0, -90.0, 0.0)],
    "tube_rack_2x8": [(187.5, 45.0, -90.0, 0.0), (237.5, 45.0, -90.0, 0.0)],
    "tip_waste_cup": [(387.5, 135.0, 90.0, 0.0)],
    "tip_rack_2x15": [(262.5, 90.0, -90.0, 0.0), (262.5, 180.0, -90.0, 0.0)],
}


def on_grid(x, y, tol=1e-6):
    nx, ny = (x - GRID_X0) / PITCH_X, (y - GRID_Y0) / PITCH_Y
    return abs(nx - round(nx)) < tol and abs(ny - round(ny)) < tol


def tri_points(corner_deg=CORNER_DEG, r=TRI_R):
    return [(r * math.cos(math.radians(corner_deg + 120 * k)), r * math.sin(math.radians(corner_deg + 120 * k)))
            for k in range(3)]


def rounded_triangle(radius, z0, h, x=0.0, y=0.0, corner_deg=CORNER_DEG):
    """The sharp triangle grown by `radius` (round corners, straight flats), from z0 up h, centred on (x, y)."""
    wp = cq.Workplane("XY").workplane(offset=z0).center(x, y)
    return wp.polyline(tri_points(corner_deg)).close().offset2D(radius, "arc").extrude(h).val()


def pocket_cutter(x, y, corner_deg=CORNER_DEG, z0=0.0):
    """The solid to cut from a part whose underside is at z0: the pocket, plus 1 mm below so the cut is clean."""
    return rounded_triangle(POCKET_R, z0 - 1.0, POCKET_DEPTH + 1.0, x, y, corner_deg)


def cut_pockets(shape, name):
    for x, y, corner, z0 in POCKETS[name]:
        shape = shape.cut(pocket_cutter(x, y, corner, z0))
    return shape.clean()


def key(press=KEY_PRESS):
    """Print orientation: pill on the bed (z 0-10), nub up (z 10-12), nub's corner toward -Y."""
    pill = (cq.Workplane("XY").slot2D(PILL_L, PILL_W, angle=90).extrude(PILL_H)).val()
    nub = rounded_triangle(POCKET_R + press, PILL_H - 0.01, NUB_H + 0.01)
    nub = cq.Workplane().add(nub).faces(">Z").edges().chamfer(NUB_LEAD).val()
    k = pill.fuse(nub).clean()
    n = max(1, round(press / 0.05))
    for i in range(n):
        dx = (i - (n - 1) / 2) * 2.0
        k = k.cut(cq.Solid.makeCylinder(DIMPLE_D / 2, DIMPLE_DEPTH + 1, cq.Vector(dx, DIMPLE_Y, PILL_H - DIMPLE_DEPTH)))
    return k.clean()


# ------------------------------------------------------------------ checks
def check_part(name, shape):
    """Each pocket: on the grid, the right depth, walled all round by at least MIN_WALL, roofed by at least
    MIN_CEILING, and nothing else of the part's own cuts inside that wall. Pairs: whole slot pitches apart."""
    out = []
    pts = POCKETS[name]
    for x, y, corner, z0 in pts:
        assert on_grid(x, y), f"{name}: pocket at ({x}, {y}) is not on a slot centre"
        pocket = rounded_triangle(POCKET_R, z0, POCKET_DEPTH, x, y, corner)
        hollow = shape.intersect(pocket).Volume()
        guard = rounded_triangle(POCKET_R + MIN_WALL, z0, POCKET_DEPTH + MIN_CEILING, x, y, corner)
        solid_guard = guard.cut(pocket)
        filled = shape.intersect(solid_guard).Volume()
        rec = {"x": x, "y": y, "corner_deg": corner, "underside_z": z0,
               "pocket_volume_mm3": round(pocket.Volume(), 2), "part_inside_pocket_mm3": round(hollow, 3),
               "wall_and_ceiling_solid_pct": round(100 * filled / solid_guard.Volume(), 2)}
        assert hollow < 1e-3, f"{name}: the pocket at ({x}, {y}) is not empty"
        assert rec["wall_and_ceiling_solid_pct"] > 99.9, f"{name}: thin wall or ceiling round the pocket at ({x}, {y}): {rec}"
        # the part's underside reaches the deck round the pocket: the nub's base ring is fully covered
        ring = rounded_triangle(POCKET_R + MIN_WALL, z0, 0.2, x, y, corner).cut(rounded_triangle(POCKET_R, z0 - 1, 2, x, y, corner))
        rec["underside_on_deck_pct"] = round(100 * shape.intersect(ring).Volume() / ring.Volume(), 2)
        assert rec["underside_on_deck_pct"] > 99.9, f"{name}: the part doesn't sit on the deck round ({x}, {y})"
        out.append(rec)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx, dy = abs(pts[i][0] - pts[j][0]), abs(pts[i][1] - pts[j][1])
            assert abs(dx / PITCH_X - round(dx / PITCH_X)) < 1e-9 and abs(dy / PITCH_Y - round(dy / PITCH_Y)) < 1e-9
    return out


def key_sizes(press):
    s = math.sqrt(3) * TRI_R
    r = POCKET_R + press
    return {"press_each_side_mm": press, "corner_radius_mm": round(r, 3),
            "A_corner_to_flat_mm": round(1.5 * TRI_R + 2 * r, 3), "B_across_corners_mm": round(s + 2 * r, 3),
            "dimples": max(1, round(press / 0.05))}


def export(name, shape, tol=0.01):
    cq.exporters.export(cq.Workplane().add(shape), str(HERE / f"{name}.step"))
    cq.exporters.export(cq.Workplane().add(shape), str(HERE / f"{name}.stl"), tolerance=tol, angularTolerance=0.1)


def main():
    keys = {}
    for press, name in [(KEY_PRESS, "deck_key")] + [(p, f"deck_key_fit_{p:.2f}") for p in FIT_TEST]:
        k = key(press)
        export(name, k)
        bb = k.BoundingBox()
        keys[name] = {"step": f"{name}.step", "stl": f"{name}.stl", **key_sizes(press),
                      "bbox_mm": [round(v, 2) for v in (bb.xlen, bb.ylen, bb.zlen)], "volume_mm3": round(k.Volume(), 1)}
    pocket = {"corner_radius_mm": POCKET_R, "depth_mm": POCKET_DEPTH, **{k: v for k, v in key_sizes(0.0).items()
                                                                        if k.startswith(("A_", "B_"))}}
    parts = {}
    sources = {"coupon_tray": HERE.parents[1] / "copper" / "cad" / "coupon_tray.step"}
    for name in POCKETS:
        src = sources.get(name, HERE / f"{name}.step")
        shape = cq.importers.importStep(str(src)).val()
        parts[name] = {"file": str(src.relative_to(HERE.parents[1])), "pockets": check_part(name, shape)}
    out = {
        "made_by": "deck_keys.py (CadQuery " + cq.__version__ + ")", "units": "mm",
        "deck": {"slot_pitch_x": PITCH_X, "slot_pitch_y": PITCH_Y, "slot_w": SLOT_W, "slot_l": SLOT_L,
                 "plate_t_in_step": DECK_T, "slot_centres": f"X = {GRID_X0} + {PITCH_X} n, Y = {GRID_Y0} + {PITCH_Y} m "
                 "(CubOS frame of Ben's 2026-10-02 calibration; best estimate, about +/-1 mm in X and +/-2 mm in Y)",
                 "evidence": GRID_EVIDENCE},
        "key": {"pill_mm": [PILL_W, PILL_L, PILL_H], "nub_h_mm": NUB_H, "nub_lead_in_mm": NUB_LEAD,
                "triangle_circumradius_mm": TRI_R, "print": "pill on the bed, nub up, as the STLs are", "files": keys},
        "pocket": pocket, "checks": {"min_wall_mm": MIN_WALL, "min_ceiling_mm": MIN_CEILING}, "parts": parts,
        "keys_needed": {n: len(v) for n, v in POCKETS.items()},
    }
    (HERE / "deck_keys.json").write_text(json.dumps(out, indent=1) + "\n")
    for n, v in parts.items():
        print(n, [(p["x"], p["y"], p["wall_and_ceiling_solid_pct"], p["underside_on_deck_pct"]) for p in v["pockets"]])
    print(json.dumps(keys, indent=1))


if __name__ == "__main__":
    main()
