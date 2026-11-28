"""Will the deck cassette fit through the cube's face? (round 3, 2026-11-28)

FT-1 -> FT-1V moves the deck cassette (the 245 mm deck plate MK-01 and everything bolted on it) from the box into the
Ideal Vacuum 12 in. cube (step 9 of the sequence in README.md). By then the heater plate and its rod are out (step 4),
the cables and gas lines are unplugged and the deck screws are not in yet. Ideal Vacuum does not publish the cube's
face opening; ft_model draws an estimate (266 mm, square, sharp corners). This script works out what the cassette
needs, from the model's solids:

1. Envelope: the cassette's solids, tessellated (0.2 mm), in the cube's frame (x, y from the cube's axis, z above its
   floor): width, depth, height and the tallest part, with the hopper at each park.
2. Passing one face at a fixed orientation: a body translated through a prismatic opening passes if and only if its
   projection along the motion fits the opening's cross-section, so each way in is a 2D problem on the projection's
   convex hull: the smallest square (sharp or with radiused corners) over every roll angle about the insertion axis,
   and the smallest round hole (linear programs on the hull's support function, 1440 directions).
3. Sitting in the cube: ft_model draws the frame as one billet with a through-pocket from each face (the openings), as
   a billet frame with interchangeable plates has to be, so the deck rests in the bottom face's pocket, which is as
   big as the face opening. The deck's footprint against that pocket (side, corner radius).
4. A 3D check with python-fcl: the frame redrawn with a parametric opening (side s, corner radius r) on all six faces
   and the five closed plates' bosses, the cassette lifted over the door's sill, slid in along +y in 2 mm steps and
   lowered onto the floor in 1 mm steps (to 0.5 mm above it); bisection on s for the smallest opening that passes.
   And the rolled passage through a 19.4 mm wall with a square hole (a welded box with a smaller door), to check 2.

Run:  python desktop-lpbf/fast-track/cad/ft_cassette.py     # out/cassette.json, out/cassette.md (~3 min)
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

import cadquery as cq
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ft_model as M  # noqa: E402

P = M.P
OUT = HERE / "out"
F = P["cube_frame"]                                  # 304.8 frame
HALF_IN = P["cube_in"] / 2                           # 144.8: plate boss to the cube's centre
LOOSE = ("Deck screws", "Well-block heater and TC leads", "Recoater M8", "Argon feed tube", "Exhaust hose")
ON_DECK = ("Slot nozzle", "Exhaust collector", "Well-block thermocouple")
PARKS = {"right park (hx 37.5, where it waits while lasing)": 37.5, "left park (hx -33.1)": -33.1,
         "left end of travel (hx -45.8)": P["rc_x0"] - P["rc_travel"] / 2}
OFF = [("as it is", ()),
       ("hopper, arm, cord, clamp and vibration motor off (MK-08, M3)",
        ("Carriage bracket and arm", "Hopper", "Silicone-cord blade", "Cord clamp", "Vibration motor")),
       ("... and the stage shield (MK-12)", ("Stage shield",)),
       ("... and the X-LSM100B with its carriage (M1c)", ("Zaber X-LSM100B", "X-LSM carriage")),
       ("... and the nozzle and collector (MK-11): deck, standoffs, well block, cup", ("Slot nozzle", "Exhaust collector")),
       ("bare deck plate", ("Macor", "Well block", "Well-block", "Overflow cup"))]
WAYS = {"door (front face), along +y": (0, 2), "side plate, along x": (1, 2), "top plate off, lowered flat": (0, 1)}
DIRS = np.array([(math.cos(t), math.sin(t)) for t in np.linspace(0.0, 2 * math.pi, 1440, endpoint=False)])
RADII = (0.0, 6.35, 12.7, 19.05, 25.4, 38.1)         # opening corner radii tried (0, 1/4, 1/2, 3/4, 1, 1.5 in.)


# --------------------------------------------------------------------------------------------------
# 1. The cassette
# --------------------------------------------------------------------------------------------------
def cassette(hx=None, drop=()):
    """The cassette's parts in FT-1V with the hopper at hx, in the cube's frame (x, y from the cube's axis, z above
    its floor): list of (name, vertices, triangles)."""
    L = M.levels("FT-1V")
    xc, yc = P["deck_c"]
    out = []
    for p in M.build("FT-1V", hx=hx):
        if p.group == "piston" or p.name.startswith(LOOSE):
            continue
        if not (p.sub in ("cassette", "recoater") or p.name.startswith(ON_DECK)):
            continue
        all_drop = [d for grp in drop for d in (grp if isinstance(grp, tuple) else (grp,))]
        if any(p.name.startswith(d) for d in all_drop):
            continue
        vs, ts = p.shape.tessellate(0.2, 0.2)
        V = np.array([(v.x - xc, v.y - yc, v.z - L["floor_top"]) for v in vs], float)
        out.append((p.name, V, np.array(ts, np.int32)))
    return out


def envelope(parts):
    V = np.vstack([v for _, v, _ in parts])
    tall = max(parts, key=lambda q: q[1][:, 2].max())
    return dict(x_mm=[round(V[:, 0].min(), 1), round(V[:, 0].max(), 1)],
                y_mm=[round(V[:, 1].min(), 1), round(V[:, 1].max(), 1)],
                width_x_mm=round(np.ptp(V[:, 0]), 1), depth_y_mm=round(np.ptp(V[:, 1]), 1),
                height_mm=round(V[:, 2].max(), 1), tallest_part=tall[0],
                tops_mm={n: round(v[:, 2].max(), 1) for n, v, _ in parts})


# --------------------------------------------------------------------------------------------------
# 2. 2D fits on the projection's convex hull
# --------------------------------------------------------------------------------------------------
def hull2(parts, cols):
    pts = np.vstack([v[:, cols] for _, v, _ in parts])
    return pts[ConvexHull(pts).vertices]


def _rot(H, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return H @ np.array([[c, -s], [s, c]]).T


def square_side(H, r=0.0):
    """Smallest side of an axis-aligned square with corner radius r (square(side - 2r) + disc(r)) that contains H."""
    if r <= 0:
        return float(max(np.ptp(H[:, 0]), np.ptp(H[:, 1])))
    h = (H @ DIRS.T).max(0)
    w = (np.abs(DIRS[:, 0]) + np.abs(DIRS[:, 1])) / 2
    res = linprog([1, 0, 0], A_ub=np.column_stack([-w, -DIRS[:, 0], -DIRS[:, 1]]), b_ub=r - h,
                  bounds=[(0, None), (None, None), (None, None)], method="highs")
    return float(res.x[0] + 2 * r)


def circle_d(H):
    """Smallest round hole (diameter) that contains H (minimum enclosing circle, as an LP)."""
    h = (H @ DIRS.T).max(0)
    res = linprog([1, 0, 0], A_ub=np.column_stack([-np.ones(len(DIRS)), -DIRS[:, 0], -DIRS[:, 1]]), b_ub=-h,
                  bounds=[(0, None), (None, None), (None, None)], method="highs")
    return float(2 * res.x[0])


def best_roll(H, r=0.0):
    """The roll angle (deg, about the insertion axis) that needs the smallest square, and that square's side."""
    grid = np.arange(0.0, 90.0, 1.0)
    sides = [square_side(_rot(H, d), r) for d in grid]
    d0 = grid[int(np.argmin(sides))]
    fine = np.arange(d0 - 1.0, d0 + 1.0 + 1e-9, 0.05)
    sides_f = [square_side(_rot(H, d), r) for d in fine]
    k = int(np.argmin(sides_f))
    return float(sides_f[k]), float(fine[k] % 90.0)


# --------------------------------------------------------------------------------------------------
# 4. 3D: python-fcl through a parametric opening
# --------------------------------------------------------------------------------------------------
def _bvh(V, Fc):
    import fcl
    g = fcl.BVHModel()
    g.beginModel(len(V), len(Fc))
    g.addSubModel(np.ascontiguousarray(V, np.float64), np.ascontiguousarray(Fc, np.int32))
    g.endModel()
    return g


def _merge(meshes):
    Vs, Fs, n = [], [], 0
    for V, Fc in meshes:
        Vs.append(V)
        Fs.append(Fc + n)
        n += len(V)
    return np.vstack(Vs), np.vstack(Fs)


def _tess(shape, tol=0.05):
    vs, ts = shape.tessellate(tol, 0.1)
    return np.array([(v.x, v.y, v.z) for v in vs], float), np.array(ts, np.int32)


def _rprism(s, r, L, axis):
    w = cq.Workplane("XY").rect(s, s).extrude(L / 2, both=True)
    if r > 0:
        w = w.edges("|Z").fillet(r)
    sh = w.val()
    if axis == "x":
        sh = sh.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90)
    elif axis == "y":
        sh = sh.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90)
    return sh


def cube_frame(s, r):
    """Obstacles in the cube's frame (origin at its centre): the billet frame with a through-pocket of side s and
    corner radius r from each face, and the bosses (1 mm smaller) of the five closed plates, 7.6 mm deep; the front
    (-y) face is open (the door swung away)."""
    bs = P["cube_boss"]
    fr = cq.Workplane("XY").box(F, F, F).val()
    for ax in "xyz":
        fr = fr.cut(_rprism(s, r, F + 2, ax))
    meshes = [_tess(fr)]
    b = _rprism(s - 2.0, max(r - 1.0, 0.0), bs, "z")
    for axis, sign in (("z", -1), ("z", 1), ("x", -1), ("x", 1), ("y", 1)):
        c = F / 2 - bs / 2
        if axis == "z":
            sh = b.translate(cq.Vector(0, 0, sign * c))
        elif axis == "x":
            sh = b.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90).translate(cq.Vector(sign * c, 0, 0))
        else:
            sh = b.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90).translate(cq.Vector(0, sign * c, 0))
        meshes.append(_tess(sh))
    return _merge(meshes)


def wall_with_hole(s, r, t=19.4):
    """A wall of thickness t at the front face (y from -F/2 to -F/2 + t) with a hole of side s, corner radius r."""
    w = cq.Workplane("XY").box(700, 700, t).val().cut(_rprism(s, r, t + 2, "z"))
    w = w.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90).translate(cq.Vector(0, -F / 2 + t / 2, 0))
    return _merge([_tess(w)])


def _collides(cas_g, obs_g, poses):
    import fcl
    ob = fcl.CollisionObject(obs_g, fcl.Transform())
    for k, (R, t) in enumerate(poses):
        o = fcl.CollisionObject(cas_g, fcl.Transform(R, t))
        if fcl.collide(o, ob, fcl.CollisionRequest(), fcl.CollisionResult()):
            return k
    return None


def door_path(s, height, mode="centre"):
    """Poses of the cassette (z from the floor) into the cube by the front door: carried at mid-height of the opening
    (mode "centre") or slid in on the sill, 0.5 mm over it (mode "sill"), along +y in 2 mm steps to the centre, then
    lowered in 1 mm steps to 0.5 mm above the floor."""
    if mode == "sill":
        lift = max(HALF_IN - s / 2 + 0.5, 0.5)
    else:
        lift = HALF_IN - height / 2
    assert lift + height < HALF_IN + s / 2, "the cassette is taller than the opening"
    z0 = -HALF_IN
    poses = [(np.eye(3), np.array([0.0, y, z0 + lift])) for y in np.arange(-F / 2 - 125.0 - 5.0, 1e-9, 2.0)]
    poses += [(np.eye(3), np.array([0.0, 0.0, z0 + dz])) for dz in np.arange(lift, 0.5 - 1e-9, -1.0)]
    poses.append((np.eye(3), np.array([0.0, 0.0, z0 + 0.5])))
    return poses


def smallest_door_opening(cas_g, height, r, mode="centre", lo=240.0, hi=289.0, tol=0.05):
    """Bisection on the opening's side s (corner radius r) for the door path; None if even hi is blocked."""
    def ok(s):
        V, Fc = cube_frame(s, r)
        return _collides(cas_g, _bvh(V, Fc), door_path(s, height, mode)) is None
    if not ok(hi):
        return None
    assert not ok(lo), (r, lo)
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return round(hi, 2)


def rolled_path(phi_deg, centre2, y_end=F / 2):
    """The cassette rolled phi about the y axis (the motion), its hull's fit centre on the hole's axis, slid along +y
    from outside the wall to past it in 2 mm steps."""
    a = math.radians(phi_deg)
    c, s_ = math.cos(a), math.sin(a)
    R = np.array([[c, 0.0, -s_], [0.0, 1.0, 0.0], [s_, 0.0, c]])     # (x, z) rotated by phi, as _rot does
    cx, cz = centre2
    return [(R, np.array([-cx, y, -cz])) for y in np.arange(-F / 2 - 130.0, y_end + 1e-9, 2.0)]


def fit_centre(H, r=0.0):
    """Centre of the smallest axis-aligned (rounded) square around H."""
    if r <= 0:
        return (H[:, 0].min() + H[:, 0].max()) / 2, (H[:, 1].min() + H[:, 1].max()) / 2
    h = (H @ DIRS.T).max(0)
    w = (np.abs(DIRS[:, 0]) + np.abs(DIRS[:, 1])) / 2
    res = linprog([1, 0, 0], A_ub=np.column_stack([-w, -DIRS[:, 0], -DIRS[:, 1]]), b_ub=r - h,
                  bounds=[(0, None), (None, None), (None, None)], method="highs")
    return res.x[1], res.x[2]


# --------------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    res = dict(note="cube frame: x, y from the cube's axis (= the deck's centre), z above the floor (the bottom plate's "
                    "boss); hopper at the right park unless stated", cube_inside_mm=P["cube_in"],
               cube_open_est_mm=P["cube_open"], frame_mm=round(F, 1))
    # 1. envelope, by hopper position
    res["envelope"] = {}
    for lab, hx in PARKS.items():
        res["envelope"][lab] = envelope(cassette(hx))
    base = cassette(PARKS["right park (hx 37.5, where it waits while lasing)"])
    # 2. passing one face at a fixed orientation
    res["face"] = {}
    for off_lab, drop in OFF:
        for hlab, hx in PARKS.items():
            if off_lab != "as it is" and not hlab.startswith("right"):
                continue
            parts = cassette(hx, drop=[d for k, (_, dd) in enumerate(OFF) if k <= [o[0] for o in OFF].index(off_lab)
                                       for d in dd])
            row = {}
            for way, cols in WAYS.items():
                H = hull2(parts, cols)
                flat = square_side(H)
                s0, phi0 = best_roll(H)
                row[way] = dict(flat_square_mm=round(flat, 1), rolled_square_mm=round(s0, 1), roll_deg=round(phi0, 2),
                                round_hole_mm=round(circle_d(H), 1),
                                rolled_square_r12_7_mm=round(best_roll(H, 12.7)[0], 1),
                                rolled_square_r25_4_mm=round(best_roll(H, 25.4)[0], 1))
            res["face"][f"{off_lab} | {hlab}"] = row
        print(f"face fits: {off_lab} ({time.time() - t0:.0f} s)", flush=True)
    # 3. sitting in the cube: the footprint in the bottom pocket (aligned, as the deck must be)
    Hf = hull2(base, (0, 1))
    res["floor"] = {f"r={r:g}": dict(pocket_side_needed_mm=round(square_side(Hf, r), 2)) for r in RADII}
    res["floor"]["round_pocket_mm"] = round(circle_d(Hf), 1)
    # the deck's own corners: radius it to R_d and the pocket needs 245 + 2 (r - R_d)(1 - 1/sqrt 2)
    res["floor"]["deck_corner_rule"] = "s >= 245 + 0.586 (r - R_d), R_d = the deck's corner radius (0 as drawn)"
    # 4. 3D checks with fcl
    Vc, Fcas = _merge([(v, f) for _, v, f in base])
    cas_g = _bvh(Vc, Fcas)
    height = Vc[:, 2].max()
    res["door_3d"] = {}
    for r in RADII:
        s_c = smallest_door_opening(cas_g, height, r, "centre")
        s_s = smallest_door_opening(cas_g, height, r, "sill")
        res["door_3d"][f"r={r:g}"] = dict(smallest_opening_mm=s_c, with_1mm_a_side_mm=round(s_c + 2.0, 1),
                                          slid_on_the_sill_mm=s_s if s_s is not None else "over 289")
        print(f"door 3D, r {r:g}: smallest opening {s_c} mm carried at mid-height, {s_s} mm slid on the sill "
              f"({time.time() - t0:.0f} s)", flush=True)
    V, Fc = cube_frame(P["cube_open"], 0.0)
    hit = _collides(cas_g, _bvh(V, Fc), door_path(P["cube_open"], height))
    res["door_3d"]["model_266_sharp_passes"] = hit is None
    # the rolled passage through a wall alone (a welded box whose door is smaller than its inside)
    Hd = hull2(base, (0, 2))
    s_roll, phi = best_roll(Hd)
    cx, cz = fit_centre(_rot(Hd, phi))               # the rolled profile's square centre goes on the hole's axis
    out = {}
    for ds in (+0.5, -0.5):
        s = s_roll + ds
        V, Fc = wall_with_hole(s, 0.0)
        hit = _collides(cas_g, _bvh(V, Fc), rolled_path(phi, (cx, cz)))
        out[f"hole {s:.1f} mm"] = "passes" if hit is None else f"blocked at step {hit}"
    res["rolled_wall_3d"] = dict(roll_deg=round(phi, 2), square_needed_mm=round(s_roll, 1), **out)
    res["runtime_s"] = round(time.time() - t0)
    (OUT / "cassette.json").write_text(json.dumps(res, indent=1))
    write_md(res)
    print(json.dumps(res["door_3d"], indent=1), json.dumps(res["rolled_wall_3d"], indent=1))
    print(f"wrote out/cassette.json, out/cassette.md in {time.time() - t0:.0f} s")


def write_md(res):
    env = res["envelope"]
    md = ["# Will the deck cassette fit through the cube's face? (`ft_cassette.py`, round 3)", "",
          "Generated from `ft_model.py` (CAD v2, g3 gantry; 2026-11-28). The cassette is the deck plate and everything "
          "bolted on it, with the heater plate and rod out, cables and gas lines unplugged, deck screws not in. "
          "Coordinates: x, y from the cube's axis (the deck's centre), z above the cube's floor.", "",
          "## 1. Envelope", "", "| Hopper | x (mm) | y (mm) | Height (mm) | Tallest part |", "|---|---|---|---:|---|"]
    for k, e in env.items():
        md.append(f"| {k} | {e['x_mm'][0]} to {e['x_mm'][1]} | {e['y_mm'][0]} to {e['y_mm'][1]} | {e['height_mm']} | "
                  f"{e['tallest_part']} |")
    md += ["", "## 2. Passing one face at a fixed orientation (2D, exact for a straight slide)", "",
           "Smallest opening: a square met flat, a square met rolled to the best angle about the insertion axis (sharp "
           "corners; and with 12.7 / 25.4 mm corner radii), and a round hole. Touching sizes: add the clearance.", "",
           "| Cassette | Hopper | Way in | Square, flat | Square, rolled | Roll (deg) | Rolled, r 12.7 / 25.4 | "
           "Round hole |", "|---|---|---|---:|---:|---:|---:|---:|"]
    for k, row in res["face"].items():
        cas, hop = k.split(" | ")
        for way, r in row.items():
            md.append(f"| {cas} | {hop.split(' (hx')[0]} | {way} | {r['flat_square_mm']} | {r['rolled_square_mm']} | "
                      f"{r['roll_deg']} | {r['rolled_square_r12_7_mm']} / {r['rolled_square_r25_4_mm']} | "
                      f"{r['round_hole_mm']} |")
    fl = res["floor"]
    md += ["", "## 3. Sitting in the cube (the deck in the bottom face's pocket, aligned)", "",
           "| Pocket corner radius (mm) | Pocket side needed (mm) |", "|---:|---:|"]
    for k, v in fl.items():
        if k.startswith("r="):
            md.append(f"| {k[2:]} | {v['pocket_side_needed_mm']} |")
    md += ["", f"A round pocket would need {fl['round_pocket_mm']} mm, more than the {res['cube_inside_mm']:.1f} mm "
           "inside: a square deck cannot lie in a round-bored cube.", "", f"Deck corner rule: {fl['deck_corner_rule']}.",
           "", "## 4. 3D insertion through the door (python-fcl)", "",
           "The frame redrawn with a through-pocket of side s and corner radius r on all six faces (the five closed "
           "plates' bosses 1 mm smaller), the cassette carried in at mid-height of the door's opening (or slid in "
           "0.5 mm over its sill), along +y in 2 mm steps, then lowered onto the floor in 1 mm steps; bisection on s "
           "to 0.05 mm.", "",
           "| Corner radius r (mm) | Smallest opening, carried at mid-height (mm) | With 1 mm a side (mm) | "
           "Slid in on the sill (mm) |", "|---:|---:|---:|---:|"]
    for k, v in res["door_3d"].items():
        if k.startswith("r="):
            md.append(f"| {k[2:]} | {v['smallest_opening_mm']} | {v['with_1mm_a_side_mm']} | "
                      f"{v['slid_on_the_sill_mm']} |")
    rw = res["rolled_wall_3d"]
    md += ["", f"The model's estimated 266 mm square opening: {'passes' if res['door_3d']['model_266_sharp_passes'] else 'blocked'}.",
           "", f"Rolled {rw['roll_deg']} deg through a 19.4 mm wall with a square hole (no pocket behind it): needs "
           f"{rw['square_needed_mm']} mm in 2D; in 3D " + ", ".join(f"{k}: {v}" for k, v in rw.items()
                                                                    if k.startswith("hole")) + ".",
           "", f"Run time {res['runtime_s']} s."]
    (OUT / "cassette.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
