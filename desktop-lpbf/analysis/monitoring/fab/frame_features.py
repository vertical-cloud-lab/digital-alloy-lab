"""The monitoring ports as machined features of the chamber frame, in the form setup C can cut (issue #260, PR 281).

cad/monitoring_spec.py puts a left-wall viewport (LW) and a back-wall light window (BW) on lines of sight to the plate
centre. Setup C holds the frame on the HRT210 with A along the frame's z (machining.md, setup C). Turning about A brings
any horizontal direction up to the spindle, so a port's azimuth (its turn about z away from the wall's normal) is free.
Its elevation (the tilt down toward the plate) is a turn about an axis across A: a 4th axis can't take it out. So this
script draws each port so a vertical tool at one A index cuts it, and checks that the optics still get their clear
aperture through the whole wall:
  * LW, at A90 (the left wall up, as setup C has it): a bore normal to the wall, opened from the clear Ø25 to the circle
    that holds the Ø25 cylinder on the sight line across the 16 mm wall; the window seat, flat gasket and clamp-ring
    holes concentric with it, flat on the wall; an SAE-4 port and Ø4 passage for the argon purge. The window then sits at
    the angle between the sight line and the wall's normal (computed here; the optics cost is in fabrication.md).
  * BW, at A180 (the back wall up): the sight line is ~49 deg off the back wall's normal, so a round normal bore would
    have to be ~49 mm across. It is a slot normal to the wall, shaped to the projection of the clear Ø20 cylinder
    across the wall (an obround), with a rectangular window seat over it, flat on the wall, and four clamp holes.
    The A131.6 alternative (the rotary takes out the 49 deg azimuth) is checked in cam_monitoring.py's notes, not cut.
It also checks each new cut against the frame's existing holes (wall left between them), the outer R8 corners, the floor
screws under the back wall, and the liners (the hole or notch each liner needs).

Inputs: the frame as inventory.py writes it (process_chamber_body_*.brep, model frame: plate centre at the origin,
powder surface z 0, walls 16 mm, outer faces x +-156, y +-111), monitoring_spec.py read at run time.
Outputs: $MON_CAM_IN/frame.brep and frame.stl (the frame with the ports cut), frame_orig.brep/.stl (as before), and
desktop-lpbf/analysis/out/monitoring/fab/frame_features.json (every feature, the checks).

Run:  OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/frame_features.py \
          [--frame /tmp/fab-e/parts/process_chamber_body_...brep] [--cam-in /tmp/fab-e/cam-in]
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import pathlib
import shutil
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[4]
CAD = REPO / "desktop-lpbf" / "cad"
OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "monitoring" / "fab"
sys.path.insert(0, str(CAD))
import monitoring_spec as MS  # noqa: E402

import cadquery as cq  # noqa: E402

V = cq.Vector
# the frame (lpbf_low P: inside 280 x 190, walls 16, R8 outer corners) and its liners (lpbf_low LINER: 0.5 mm 316L,
# 0.1 mm off the wall; side liners z 16..104; back liner in two bands, the lower z 16..32, its left piece x -130.5..-0.5)
OUTER = dict(x=156.0, y=111.0)
INNER = dict(x=140.0, y=95.0)
CORNER_R = 8.0
FLAT_X = OUTER["x"] - CORNER_R      # the back wall's outer face is flat for |x| <= 148
LINER = dict(side_z=(16.0, 104.0), back_lo_z=(16.0, 32.0), back_lo_left_x=(-130.5, -0.5), gap=0.1, t=0.5)
SAE4 = dict(thread_d=11.11, depth=11.5, csk_d=12.9, csk_depth=1.6, drill_d=4.0)   # lpbf_low sae_port (SAE J1926 -4)
# the plate-height through-beam's fibre head on the left wall's outer face (lpbf_low section 5: M6 head with a Ø13 x 2.5 flange at
# y 0, z 5). With the Ø40 window the LW clamp ring is Ø58 and reaches it, so the ring gets a flat toward it, 1 mm clear, and its
# four holes start at 60 deg (were 45, which left 0.6 mm between the flat and a hole; mechanics.md §2)
FIBRE_HEAD = dict(yz=(0.0, 5.0), flange_r=6.5, clear=1.0)
LW_HOLE0_DEG = 60.0
# the BW window clamp frame as cad/monitoring_parts._bw draws it: a rounded rectangle 18 x 22 mm bigger than the seat, R6, from
# 3/16 in. plate with Ø4.5 clearance holes, trimmed to the back wall's flat face (x >= -147.5) and bottom edge (z >= -3.4), and 1 mm
# clear of the cross-flow inlet plenum's bolting flange (lpbf_low: x -78..78, z up to 40, on the back wall's outer face). The trim
# left 1.2 mm of metal outside the third screw's hole (mechanics.md §6), so that hole is placed by bw_hole3() below
BW_FRAME = dict(grow_L=18.0, grow_W=22.0, r=6.0, x_min=-FLAT_X + 0.5, z_min=-3.4, plenum_x=-78.0, plenum_z_top=40.0, trim=1.0,
                hole_clear_r=2.25)
M4_MAJOR_R = 2.0     # an M4 thread's major radius: the wall to a pocket is measured from it
GASKET = 0.75        # squeezed FKM flat gasket under the window and flat ring over it (the layer camera's window, lpbf_low)
LAND_MIN = 3.0       # flat gasket land wanted round an opening (mm)
SEAT_SHIFT = 1.0     # BW: the seat's centre moved this far toward +x along the slot (keeps it off the R8 corner)
WALL_MIN = 1.5       # wall wanted between a new cut and an existing hole (mm)
FLOOR_SCREW_TOP = 5.5  # the 18 M4 floor screws go up into the walls from z -3.9 to z 5.5 at mid-wall (r 2)


def clear_points(c, d, rc, axis, lo, hi, n_t=161, n_phi=96):
    """points on the clear cylinder (radius rc, axis through c along d) whose coordinate `axis` lies in [lo, hi]"""
    d = np.asarray(d, float)
    d /= np.linalg.norm(d)
    e1 = np.cross(d, [0, 0, 1.0])
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.cross(d, [1.0, 0, 0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(d, e1)
    # t range that covers the slab (with the circle's spread)
    t0 = (lo - c[axis]) / d[axis]
    t1 = (hi - c[axis]) / d[axis]
    pad = 2 * rc / max(abs(d[axis]), 1e-3)
    ts = np.linspace(min(t0, t1) - pad, max(t0, t1) + pad, n_t)
    ph = np.linspace(0, 2 * math.pi, n_phi, endpoint=False)
    T, Phi = np.meshgrid(ts, ph, indexing="ij")
    P = (np.asarray(c, float)[None, None, :] + T[..., None] * d[None, None, :]
         + rc * (np.cos(Phi)[..., None] * e1 + np.sin(Phi)[..., None] * e2))
    P = P.reshape(-1, 3)
    m = (P[:, axis] >= lo) & (P[:, axis] <= hi)
    return P[m]


def axis_at(c, d, axis, val):
    d = np.asarray(d, float) / np.linalg.norm(d)
    t = (val - c[axis]) / d[axis]
    return np.asarray(c, float) + t * d


def ceil_to(v, step=0.25):
    return math.ceil(v / step - 1e-9) * step


def cyl(r, p0, dirn, length):
    return cq.Solid.makeCylinder(r, length, V(*p0), V(*dirn))


def stadium_face_y(p1, p2, r, y):
    """an obround in the plane y = const: end centres p1, p2 given as (x, z), radius r"""
    p1, p2 = np.asarray(p1, float), np.asarray(p2, float)
    u = (p2 - p1) / np.linalg.norm(p2 - p1)
    n = np.array([-u[1], u[0]])

    def P(q):
        return V(float(q[0]), y, float(q[1]))
    e = [cq.Edge.makeLine(P(p1 + r * n), P(p2 + r * n)),
         cq.Edge.makeThreePointArc(P(p2 + r * n), P(p2 + r * u), P(p2 - r * n)),
         cq.Edge.makeLine(P(p2 - r * n), P(p1 - r * n)),
         cq.Edge.makeThreePointArc(P(p1 - r * n), P(p1 - r * u), P(p1 + r * n))]
    return cq.Face.makeFromWires(cq.Wire.assembleEdges(e))


def rrect_face_y(c, u, L, W, rad, y):
    """a rounded rectangle in the plane y = const: centre c (x, z), long axis u (unit, in x-z), L x W, corner radius rad"""
    c, u = np.asarray(c, float), np.asarray(u, float)
    n = np.array([-u[1], u[0]])
    a, b = L / 2 - rad, W / 2 - rad

    def P(q):
        return V(float(q[0]), y, float(q[1]))
    corners = [(+1, +1), (-1, +1), (-1, -1), (+1, -1)]
    edges = []
    pts = []
    for sx, sz in corners:
        cc = c + sx * a * u + sz * b * n
        pts.append(cc)
    # walk: right side up, top, left side, bottom (corner arcs between)
    seq = [(0, u, n), (1, n, -u), (2, -u, -n), (3, -n, u)]
    for k, (i, out1, out2) in enumerate(seq):
        cc = pts[i]
        start = cc + rad * out1
        mid = cc + rad * (out1 + out2) / math.sqrt(2)
        end = cc + rad * out2
        edges.append(cq.Edge.makeThreePointArc(P(start), P(mid), P(end)))
        nxt = pts[(i + 1) % 4] + rad * out2
        edges.append(cq.Edge.makeLine(P(end), P(nxt)))
    return cq.Face.makeFromWires(cq.Wire.assembleEdges(edges))


def _rrect_poly(c, u, L, W, rad):
    """a rounded rectangle in the x-z plane (shapely), as rrect_face_y draws it"""
    from shapely import affinity
    from shapely.geometry import box as sbox
    core = sbox(-(L / 2 - rad), -(W / 2 - rad), L / 2 - rad, W / 2 - rad).buffer(rad, quad_segs=32)
    core = affinity.rotate(core, math.degrees(math.atan2(u[1], u[0])), origin=(0.0, 0.0))
    return affinity.translate(core, float(c[0]), float(c[1]))


def bw_clamp_outline(sc, u, L_seat, W_seat):
    """the BW clamp frame's outline in the x-z plane (shapely), trimmed as monitoring_parts._bw trims it (BW_FRAME)"""
    from shapely.geometry import box as sbox
    f = BW_FRAME
    fr = _rrect_poly(sc, u, L_seat + f["grow_L"], W_seat + f["grow_W"], f["r"])
    fr = fr.intersection(sbox(f["x_min"], f["z_min"], 0.0, 200.0))
    return fr.difference(sbox(f["plenum_x"] - f["trim"], -50.0, 0.0, f["plenum_z_top"] + f["trim"]))


def bw_hole3(sc, u, n, L_seat, W_seat, seat_r):
    """the third clamp screw, past the seat's +x end: the point that leaves the most metal round the clamp frame's Ø4.5 hole
    (to the trimmed outline), keeping WALL_MIN between the M4 thread and the seat pocket and staying off the floor screws.
    Searched on a 0.1 mm grid along the seat's +x end, from its middle down (the other two screws are above the seat)."""
    from shapely.geometry import Point
    seat = _rrect_poly(sc, u, L_seat, W_seat, seat_r)
    frame = bw_clamp_outline(sc, u, L_seat, W_seat)
    best = None
    for a in np.arange(L_seat / 2, L_seat / 2 + 8.0 + 1e-9, 0.1):
        for b in np.arange(-W_seat / 2, 1e-9, 0.1):
            p = sc + a * u + b * n
            wall = seat.exterior.distance(Point(*p)) - M4_MAJOR_R
            if wall < WALL_MIN - 1e-9 or p[1] - M4_MAJOR_R < FLOOR_SCREW_TOP + WALL_MIN or not frame.contains(Point(*p)):
                continue
            web = frame.exterior.distance(Point(*p)) - BW_FRAME["hole_clear_r"]
            if best is None or web > best[0] + 1e-6:
                best = (web, p, a, b, wall)
    web, p, a, b, wall = best
    return tuple(p.tolist()), dict(along_slot_mm=round(a - (L_seat / 2 + 4.5), 2), across_mm=round(b, 2),
                                   web_mm=round(web, 2), wall_to_seat_mm=round(wall, 2))


def _ring_flat(cen, r_out, bc_r, holes):
    """the flat on the LW clamp ring toward the through-beam's fibre head: its distance from the ring's centre, its direction (y, z),
    and the metal left between it and the nearest clearance hole (Ø4.5)"""
    fy, fz = FIBRE_HEAD["yz"]
    v = np.array([fy - cen[1], fz - cen[2]])
    dist = float(np.linalg.norm(v))
    u = v / dist
    d_flat = dist - FIBRE_HEAD["flange_r"] - FIBRE_HEAD["clear"]
    if d_flat >= r_out:
        return None
    web = min(d_flat - float(np.dot(np.array([y - cen[1], z - cen[2]]), u)) - 2.25 for y, z in holes)
    return dict(dist_mm=round(d_flat, 2), dir_yz=[round(float(u[0]), 4), round(float(u[1]), 4)], web_to_hole_mm=round(web, 2))


def lw_features(frame):
    """left-wall viewport, cut at A90 with the tool along x"""
    s = MS.VIEWPORTS["LW"]
    c = np.array(s["centre"])
    d = np.array(MS.axis_to_target(s["centre"]))
    rc = s["clear_d"] / 2
    x_out, x_in = -OUTER["x"], -INNER["x"]
    x_lin0, x_lin1 = x_in + LINER["gap"], x_in + LINER["gap"] + LINER["t"]
    tilt = math.degrees(math.acos(abs(d[0])))
    azim = math.degrees(math.atan2(d[1], d[0]))
    elev = -math.degrees(math.asin(d[2]))
    pts = clear_points(c, d, rc, 0, x_out - 0.5, x_lin1 + 0.2)
    a_out, a_in = axis_at(c, d, 0, x_out), axis_at(c, d, 0, x_in)
    cen = 0.5 * (a_out + a_in)            # the bore's axis (along x) through the sight line's mid-wall point
    yz = pts[:, 1:] - cen[1:]
    r_need = float(np.max(np.hypot(yz[:, 0], yz[:, 1])))
    R = ceil_to(r_need + 0.25)
    win = s["window"]
    r_seat = (win["d"] + 0.2) / 2
    seat_depth = GASKET + win["t"] + GASKET
    land = r_seat - 0.1 - R               # gasket land between the bore and the window's edge
    bc_r = ceil_to(r_seat + 1.65 + 3.0, 0.5)   # M4 tap drill 3.3 with 3 mm of wall outside the seat
    holes = [(float(cen[1] + bc_r * math.cos(math.radians(LW_HOLE0_DEG + 90 * k))),
              float(cen[2] + bc_r * math.sin(math.radians(LW_HOLE0_DEG + 90 * k)))) for k in range(4)]
    ring_od = 2 * (bc_r + 4.0)
    # argon purge: SAE-4 port above the clamp ring (its fitting's 9/16 in. hex is ~16.5 mm across the corners)
    purge = (float(cen[1]), float(cen[2] + ring_od / 2 + 8.3 + 1.0))
    # liner hole (left liner at x -139.9..-139.4)
    lp = clear_points(c, d, rc, 0, x_lin0, x_lin1)
    lc = 0.5 * (axis_at(c, d, 0, x_lin0) + axis_at(c, d, 0, x_lin1))
    r_lin = ceil_to(float(np.max(np.hypot(lp[:, 1] - lc[1], lp[:, 2] - lc[2]))) + 0.5, 0.5)
    cuts = [("LW bore", cyl(R, (x_out - 1, cen[1], cen[2]), (1, 0, 0), (x_in - x_out) + 2.0)),
            ("LW window seat", cyl(r_seat, (x_out - 1, cen[1], cen[2]), (1, 0, 0), seat_depth + 1.0))]
    for k, (y, z) in enumerate(holes):
        cuts.append((f"LW clamp-ring hole {k + 1} (M4 x 0.7, 8 deep; drawn at 4.0 x 10)", cyl(2.0, (x_out - 1, y, z), (1, 0, 0), 11.0)))
    py, pz = purge
    sae = cyl(SAE4["thread_d"] / 2, (x_out - 1, py, pz), (1, 0, 0), SAE4["depth"] + 1)
    sae = sae.fuse(cq.Solid.makeCone(SAE4["csk_d"] / 2, SAE4["thread_d"] / 2, SAE4["csk_depth"], V(x_out - 0.01, py, pz), V(1, 0, 0)))
    sae = sae.fuse(cyl(SAE4["drill_d"] / 2, (x_out + SAE4["depth"] - 0.1, py, pz), (1, 0, 0), (x_in - x_out) - SAE4["depth"] + 1.2))
    cuts.append(("LW purge port (SAE-4, 7/16-20, and its Ø4 passage)", sae))
    info = dict(
        port="LW", index_deg=90, tool_axis="x (wall normal)", spec_centre=c.tolist(), sight_axis=d.round(4).tolist(),
        sight_vs_wall_normal_deg=round(tilt, 2), azimuth_deg=round(azim, 2), elevation_deg=round(elev, 2),
        index_that_removes_the_azimuth_deg=round(math.degrees(math.atan2(d[0], d[1])) % 360, 2),
        bore=dict(centre_yz=[round(float(cen[1]), 2), round(float(cen[2]), 2)], d=2 * R, needed_d=round(2 * r_need, 2),
                  through=f"x {x_out}..{x_in}",
                  note="normal to the wall; holds the clear Ø%.0f cylinder on the sight line across the 16 mm wall" % s["clear_d"]),
        seat=dict(d=round(2 * r_seat, 2), depth=round(seat_depth, 2), window=win, gasket_land_mm=round(land, 2),
                  note="concentric with the bore, flat on the wall: %.2f mm gasket, %.1f mm window, %.2f mm flat ring; "
                       "the clamp ring bottoms on the wall face" % (GASKET, win["t"], GASKET)),
        clamp_ring=dict(bolt_circle_d=2 * bc_r, od=ring_od, id=2 * R, screws="4 x M4 x 0.7, tapped 8 deep (3.3 drill 10 deep)",
                        hole0_deg=LW_HOLE0_DEG, flat=_ring_flat(cen, ring_od / 2, bc_r, holes),
                        holes_yz=[[round(y, 2), round(z, 2)] for y, z in holes]),
        purge_port=dict(yz=[round(py, 2), round(pz, 2)], kind="SAE-4 (7/16-20 UNF) O-ring boss + Ø4 passage through"),
        liner_hole=dict(liner="Lift-out wall liner, left", centre_yz=[round(float(lc[1]), 2), round(float(lc[2]), 2)], d=2 * r_lin),
        sight_at_outer_face=a_out.round(2).tolist(), sight_at_inner_face=a_in.round(2).tolist())
    return cuts, info, dict(c=c, d=d, rc=rc, axis=0, lo=x_out, hi=x_in)


def bw_features(frame, z_shift=0.0):
    """back-wall light window, cut at A180 with the tool along y: obround slot + rectangular seat"""
    s = MS.VIEWPORTS["BW"]
    c = np.array(s["centre"]) + np.array([0, 0, z_shift])
    d = np.array(MS.axis_to_target(tuple(c)))
    rc = s["clear_d"] / 2
    y_out, y_in = OUTER["y"], INNER["y"]
    y_lin1, y_lin0 = y_in - LINER["gap"], y_in - LINER["gap"] - LINER["t"]
    tilt = math.degrees(math.acos(abs(d[1])))
    azim = math.degrees(math.atan2(-d[0], -d[1]))
    elev = -math.degrees(math.asin(d[2]))
    pts = clear_points(c, d, rc, 1, y_lin0 - 0.2, y_out + 0.5)
    a_out, a_in = axis_at(c, d, 1, y_out), axis_at(c, d, 1, y_in)
    p_out, p_in = a_out[[0, 2]], a_in[[0, 2]]
    u = (p_in - p_out) / np.linalg.norm(p_in - p_out)
    n = np.array([-u[1], u[0]])
    xz = pts[:, [0, 2]]
    mid = 0.5 * (p_out + p_in)
    along = (xz - mid) @ u
    perp = (xz - mid) @ n
    r_s = ceil_to(float(np.max(np.abs(perp))) + 0.25)
    half = float(np.max(np.abs(along)))
    e1, e2 = mid - (half - r_s) * u, mid + (half - r_s) * u     # stadium end centres
    L_slot, W_slot = 2 * half + 0.5, 2 * r_s
    win_t = 3.0
    seat_depth = GASKET + win_t + GASKET
    L_seat, W_seat = math.ceil(L_slot + 2 * LAND_MIN), math.ceil(W_slot + 2 * LAND_MIN)
    seat_r = 4.0                            # corner radius (1/4 in. end mill: R3.2 or more)
    # where the seat reaches: corners of the rounded rectangle
    # the seat sits SEAT_SHIFT along +u from the slot's middle, so its -x end stays clear of the outer R8 corner (flat to
    # x -148): the gasket land is LAND_MIN - SEAT_SHIFT at the -x end and LAND_MIN + SEAT_SHIFT at the +x end
    sc = mid + SEAT_SHIFT * u
    corners = [sc + sx * (L_seat / 2) * u + sz * (W_seat / 2) * n for sx in (-1, 1) for sz in (-1, 1)]
    xmin = min(p[0] for p in corners)
    zmin = min(p[1] for p in corners)
    # three clamp screws: two above the seat and one past its +x end (below the seat are the floor screws, past the -x end
    # the R8 corner). The third was 4.5 mm past the seat's end on its centre line; the clamp frame's trim at the inlet plenum's
    # flange left 1.2 mm of metal outside its hole there, so bw_hole3() moves it (2026-11-27)
    holes = [tuple((sc + sx * (L_seat / 2 - 6.0) * u + (W_seat / 2 + 4.5) * n).tolist()) for sx in (-1, 1)]
    hole3_was = tuple((sc + (L_seat / 2 + 4.5) * u).tolist())
    hole3, hole3_info = bw_hole3(sc, u, n, L_seat, W_seat, seat_r)
    holes.append(hole3)
    from shapely.geometry import Point
    outline = bw_clamp_outline(sc, u, L_seat, W_seat)
    seat_poly = _rrect_poly(sc, u, L_seat, W_seat, seat_r)
    webs = [round(outline.exterior.distance(Point(*h_)) - BW_FRAME["hole_clear_r"], 2) for h_ in holes]
    walls = [round(seat_poly.exterior.distance(Point(*h_)) - M4_MAJOR_R, 2) for h_ in holes]
    web_was = round(outline.exterior.distance(Point(*hole3_was)) - BW_FRAME["hole_clear_r"], 2)
    # the slot stops at the inner face (y 95): past it, x < -140 is the left wall's material, not air
    slot = cq.Solid.extrudeLinear(stadium_face_y(e1, e2, r_s, y_out + 1.0), V(0, -(y_out - y_in) - 1.5, 0))
    slot = slot.cut(cq.Solid.makeBox(60.0, 10.0, 300.0, V(-INNER["x"] - 60.0, y_in - 10.0, -100.0)))
    seat = cq.Solid.extrudeLinear(rrect_face_y(sc, u, L_seat, W_seat, seat_r, y_out + 1.0), V(0, -(1.0 + seat_depth), 0))
    cuts = [("BW slot (obround through the back wall)", slot), ("BW window seat (rounded rectangle)", seat)]
    for k, (x, z) in enumerate(holes):
        cuts.append((f"BW clamp-frame hole {k + 1} (M4 x 0.7, 8 deep; drawn at 4.0 x 10)", cyl(2.0, (x, y_out + 1, z), (0, -1, 0), 11.0)))
    # lower back liner, left piece (x -130.5..-0.5, z 16..32) at y 94.4..94.9
    lp = clear_points(c, d, rc, 1, y_lin0, y_lin1)
    info = dict(
        port="BW", index_deg=180, tool_axis="y (wall normal)", spec_centre=list(MS.VIEWPORTS["BW"]["centre"]),
        centre_used=c.tolist(), z_shift_mm=z_shift, sight_axis=d.round(4).tolist(),
        sight_vs_wall_normal_deg=round(tilt, 2), azimuth_deg=round(azim, 2), elevation_deg=round(elev, 2),
        index_that_removes_the_azimuth_deg=round(math.degrees(math.atan2(d[0], d[1])) % 360, 2),
        slot=dict(kind="obround, normal to the wall, through", length=round(L_slot, 2), width=round(W_slot, 2),
                  end_centres_xz=[np.round(e1, 2).tolist(), np.round(e2, 2).tolist()], radius=r_s,
                  long_axis_deg_from_x=round(math.degrees(math.atan2(u[1], u[0])), 2),
                  round_bore_needed_d=round(2 * float(np.max(np.hypot(*(xz - mid).T))), 1)),
        seat=dict(L=L_seat, W=W_seat, corner_r=seat_r, depth=round(seat_depth, 2), window=f"{L_seat - 0.3:.1f} x {W_seat - 0.3:.1f} x {win_t} mm, "
                  "corners chamfered 2 mm (rectangular N-BK7 or fused silica)", x_min=round(xmin, 2), z_min=round(zmin, 2),
                  on_flat_face=bool(xmin >= -FLAT_X + 0.5), clear_of_floor_screws=bool(zmin >= FLOOR_SCREW_TOP + WALL_MIN)),
        clamp_frame=dict(holes_xz=[[round(x, 2), round(z, 2)] for x, z in holes], screws="3 x M4 x 0.7, tapped 8 deep",
                         web_to_trimmed_edge_mm=webs, thread_wall_to_seat_mm=walls,
                         hole3=dict(was_xz=[round(hole3_was[0], 2), round(hole3_was[1], 2)], web_was_mm=web_was,
                                    moved_xz=[round(hole3[0] - hole3_was[0], 2), round(hole3[1] - hole3_was[1], 2)], **hole3_info),
                         outline_bbox_xz=[round(v, 2) for v in outline.bounds],
                         note="webs: metal between each Ø4.5 clearance hole and the clamp frame's outline as monitoring_parts._bw "
                              "trims it (BW_FRAME); walls: between each M4 thread (major Ø4) and the seat pocket"),
        liner=dict(liner="Lift-out wall liner, back lower left (z 16..32, x -130.5..-0.5)",
                   x_range=[round(float(lp[:, 0].min()) - 0.5, 1), round(float(lp[:, 0].max()) + 0.5, 1)],
                   z_range=[round(float(lp[:, 2].min()) - 0.5, 1), round(float(lp[:, 2].max()) + 0.5, 1)]),
        sight_at_outer_face=a_out.round(2).tolist(), sight_at_inner_face=a_in.round(2).tolist())
    zr = info["liner"]["z_range"]
    info["liner"]["what"] = ("the opening spans the band's full height (z 16..32): start the piece at x %.1f (was -130.5)"
                             % info["liner"]["x_range"][1] if zr[0] <= LINER["back_lo_z"][0] and zr[1] >= LINER["back_lo_z"][1]
                             else "a notch")
    return cuts, info, dict(c=c, d=d, rc=rc, axis=1, lo=y_in, hi=y_out)


def clear_check(frame_new, g):
    """volume of the frame inside the clear cylinder across the wall (should be 0)"""
    c, d, rc = g["c"], np.asarray(g["d"], float), g["rc"]
    t0 = (g["lo"] - c[g["axis"]]) / d[g["axis"]]
    t1 = (g["hi"] - c[g["axis"]]) / d[g["axis"]]
    ta, tb = sorted((t0, t1))
    pad = 3 * rc
    p0 = c + (ta - pad) * d
    clear = cyl(rc, tuple(p0), tuple(d), (tb - ta) + 2 * pad)
    inter = frame_new.intersect(clear)
    return round(inter.Volume(), 3)


def existing_gaps(frame, cuts):
    """smallest distance from each new cut to the original frame's surfaces that the cut does not run through"""
    out = {}
    for name, sol in cuts:
        # faces of the original frame near this cut, other than the big planar wall faces it opens into
        bb = sol.BoundingBox()
        near = []
        for f in frame.Faces():
            fb = f.BoundingBox()
            if fb.xmax < bb.xmin - 10 or fb.xmin > bb.xmax + 10 or fb.ymax < bb.ymin - 10 or fb.ymin > bb.ymax + 10 \
                    or fb.zmax < bb.zmin - 10 or fb.zmin > bb.zmax + 10:
                continue
            if f.geomType() == "PLANE" and f.Area() > 2000:
                continue
            near.append(f)
        best = None
        for f in near:
            try:
                dist = sol.distance(f)
            except Exception:
                continue
            if best is None or dist < best[0]:
                fb = f.BoundingBox()
                best = (dist, f.geomType(), [round(v, 1) for v in (fb.center.x, fb.center.y, fb.center.z)])
        out[name] = dict(min_gap_mm=round(best[0], 2), to=best[1], at=best[2]) if best else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", default=None)
    ap.add_argument("--cam-in", default="/tmp/fab-e/cam-in")
    ap.add_argument("--bw-z-shift", type=float, default=None,
                    help="raise the BW port by this much (mm); default: the least that clears the floor screws")
    a = ap.parse_args()
    fpath = a.frame or sorted(glob.glob("/tmp/fab-e/parts/process_chamber_body_*.brep"))[0]
    frame = cq.importers.importBrep(fpath).val()
    v0 = frame.Volume()
    cuts_lw, info_lw, g_lw = lw_features(frame)
    # BW: the least upward shift (0.5 mm steps) that puts its seat above the floor screws and keeps it on the flat face
    if a.bw_z_shift is None:
        shift, tried = 0.0, []
        while True:
            _, info_bw, _ = bw_features(frame, shift)
            tried.append(dict(z_shift=shift, seat_z_min=info_bw["seat"]["z_min"], seat_x_min=info_bw["seat"]["x_min"]))
            if info_bw["seat"]["clear_of_floor_screws"] or shift > 20:
                break
            shift += 0.5
    else:
        shift, tried = a.bw_z_shift, []
    _, info_bw0, _ = bw_features(frame, 0.0)
    cuts_bw, info_bw, g_bw = bw_features(frame, shift)
    info_bw["as_specified"] = dict(seat=info_bw0["seat"], slot=info_bw0["slot"], elevation_deg=info_bw0["elevation_deg"])
    new = frame
    for _, sol in cuts_lw + cuts_bw:
        new = new.cut(sol)
    new = new.clean()
    checks = dict(
        frame_volume_cm3=dict(before=round(v0 / 1e3, 3), after=round(new.Volume() / 1e3, 3), removed=round((v0 - new.Volume()) / 1e3, 3)),
        clear_aperture_blocked_mm3=dict(LW=clear_check(new, g_lw), BW=clear_check(new, g_bw)),
        gaps_to_existing_features=existing_gaps(frame, cuts_lw + cuts_bw),
        bw_shift_search=tried)
    cam = pathlib.Path(a.cam_in)
    cam.mkdir(parents=True, exist_ok=True)
    new.exportBrep(str(cam / "frame.brep"))
    cq.exporters.export(cq.Workplane().add(new), str(cam / "frame.stl"), tolerance=0.05, angularTolerance=0.15)
    shutil.copy(fpath, cam / "frame_orig.brep")
    stl0 = pathlib.Path(fpath).with_suffix(".stl")
    if stl0.exists():
        shutil.copy(stl0, cam / "frame_orig.stl")
    for name, sol in cuts_lw + cuts_bw:   # each cut tool, for the CAM checks' masks
        slug = name.split(" (")[0].replace(" ", "_").lower()
        sol.exportBrep(str(cam / f"cut_{slug}.brep"))
    res = dict(frame=fpath, LW=info_lw, BW=info_bw, checks=checks,
               method=__doc__.split("\n\n")[1])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "frame_features.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(dict(LW=dict(bore=info_lw["bore"], seat=info_lw["seat"], tilt=info_lw["sight_vs_wall_normal_deg"],
                                  liner=info_lw["liner_hole"], purge=info_lw["purge_port"]),
                          BW=dict(slot=info_bw["slot"], seat=info_bw["seat"], shift=shift, liner=info_bw["liner"],
                                  as_specified=info_bw["as_specified"]["seat"]),
                          checks=checks), indent=1))


if __name__ == "__main__":
    main()
