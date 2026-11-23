"""Machine-side features for robot tending (issue #260, PR #266): what a UR12e (the UR10e, renamed) with a Robotiq 2F-85 on a
MiR250 needs on the desktop LPBF so that every tending job works. Called from one hook line at the end of lpbf_low.build():

    automation.add_features(add, sys.modules[__name__], module)

Sizes and the products each feature stands for are in desktop-lpbf/robot-tooling.csv and robot-ops.md; the jobs that use them are
simulated in analysis/robot/ops.py. Features that would change parts other sections draw (the module's joint, the plate's drawbar,
the liners' screw slots, the overflow path) are not drawn here: robot-ops.md lists them as patch requests.

Drawn here (every part tagged "automation"):
  1. a bar handle on the sliding laser-guard door (it had none);
  2. a drive on the chamber door's hinge axis, keyed to a disc on the door: a small pneumatic rotary actuator that opens the door
     to 95 deg and closes it, at a speed its flow controls set (the robot can pull the door open, but no arm path lifts it shut
     from 95 deg past the guard's frame: analysis/robot/ops.py). A one-way damper in the same place is the passive alternative,
     if a person closes the door;
  3. a compact air cylinder above each draw latch that throws the latch's lever, so the over-centre draw latches (3.56 kN
     rated, set to >= 0.4 kN) close and open without a hand; since 2026-11-23 the latches and their cylinders ride on brackets
     on the door's ears (lpbf_low section 8), so they move with the door;
  4. wing heads on the cover-slide drawer's two quarter-turn latch studs, so the gripper's fingers drive the wings and the
     wrist turns them 90 deg (no screwdriver, no grip-friction torque);
  5. a grip fin on the front end of the recoater's blade holder (the blade cartridge), for the plate fingers' lips;
  6. a pull tab on each side wall liner, standing 12 mm off the sheet, for the plate fingers' lips (one part per liner);
  7. two AprilTag (tag36h11) plates on the laser guard's front-left post, for the wrist camera's re-registration after each
     MiR250 docking and VLM move (byu-vcl PR 318 docks at AprilTag targets with the same D405 camera).
"""
from __future__ import annotations

import math


def add_features(add, M, module):
    """Add the robot-tending features to the model being built. `add` is lpbf_low.build()'s own add(); M is lpbf_low."""
    P, C = M.P, M.C
    box, cyl, fuse, comp, tube = M.box, M.cyl, M.fuse, M.comp, M.tube
    cx, cy, ix, iy = P["cx"], P["cy"], P["ix"], P["iy"]
    lz0 = P["lid_z0"]
    tag = ("automation",)

    # ---------------------------------------------------------------- 1. guard-door handle
    # the door's front face is at y = gy0 - 1.5 - 6 = -272.5; the bar sits 46 mm in front of it at the door's left end, clear of
    # the door rails (z -160..-152 and 359.7..367.7) and of the guard-lock switch (z >= 247.7) in every position of its 515 mm travel
    gy0 = -265.0
    yf = gy0 - 1.5 - 6.0
    hx, hz0, hz1 = -312.0, 40.0, 170.0
    so = [cyl(5.0, (hx, yf, z), "-y", 40.0) for z in (hz0 + 10.0, hz1 - 10.0)]
    bar = cyl(6.0, (hx, yf - 46.0, hz0), "z", hz1 - hz0)
    add("Guard-door handle for the robot (Ø12 x 130 bar on two Ø10 standoffs, 6061)", comp(so + [bar]), C["anod"], 12, (0, -260, 0),
        group="gdoor", mat="al6061", bom="RA1", tags=tag)

    # ---------------------------------------------------------------- 2. door damper
    hy, hz = M.DOOR_HINGE
    # a rotary actuator (or the McMaster 6597K124 one-way damper, 2.0 +/- 0.4 N m, 47 x 47 x 42 mm; the door's gravity torque peaks
    # at 0.94 N m) outboard of the chamber's left side face, coaxial with the hinge; a Ø6 shaft runs in from it to a disc screwed to the door's
    # left edge (shaft and disc turn with the door about their own axis, so they sweep nothing). Its bracket is a 4 mm plate behind it,
    # flanged onto the chamber's left side face, below the left latch actuator (z <= 4)
    dmp = box(-200.0, -158.0, hy - 23.5, hy + 23.5, hz - 23.5, hz + 23.5)
    add("Door drive: pneumatic rotary actuator on the hinge axis, SMC CRQ2 size 20 class (~1.8 N m at 0.5 MPa, stroke set to 95 deg, "
        "meter-out flow controls; envelope 47 x 47 x 42 mm). Passive alternative: McMaster 6597K124 one-way damper, same envelope",
        dmp, C["black"], 8, (-120, -240, 0), mat="misc", mass_kg=0.3, bom="RA2", tags=tag)
    bracket = fuse([box(-200.0, -156.0, hy + 23.5, hy + 27.5, -32.0, 4.0), box(-160.0, -156.0, hy + 27.5, -80.0, -18.0, 4.0)])
    add("Door drive bracket (6061, 4 mm, flanged onto the chamber's left side face)", bracket, C["alu_dark"], 8, (-120, -240, 0), mat="al6061",
        bom="RA2", tags=tag)
    disc = fuse([cyl(8.0, (-128.0, hy, hz), "x", 3.9), cyl(3.0, (-158.0, hy, hz), "x", 30.0)])
    add("Door drive shaft and disc (Ø6 D-shaft keyed into a 6061 disc screwed to the door's left edge)", disc, C["alu"], 8, (0, -240, 0),
        group="door", mat="al6061", bom="RA2", tags=tag)

    # ---------------------------------------------------------------- 3. latch actuators
    # since 2026-11-23 the latches sit on brackets on the door's ears, pointing forward (lpbf_low section 8: the right one was behind the
    # front-right optics post). A Ø20 compact cylinder rides on each bracket's outer face above its latch (latch z 31.8..76.2, x 146..177.75;
    # cylinder z 78..98, x 146..166), its rod forward toward the lever at the latch's front end (y -207). They move with the door
    # (group "door"), on a coiled air line; inboard of the post (x >= 180) and clear of the door drive (z <= 11.5) in every door position.
    ex_ = M.LATCH_POS["bracket_x"][1]
    dy0 = -cy - 15.0
    acts = []
    for sx in (-1, 1):
        xc_ = sx * (ex_ + 10.0)
        body = cyl(10.0, (xc_, dy0 - 4.0, 88.0), "-y", 46.0)
        rod = cyl(4.0, (xc_, dy0 - 50.0, 88.0), "-y", 10.0)
        foot = box(min(sx * ex_, sx * (ex_ + 20.0)), max(sx * ex_, sx * (ex_ + 20.0)), dy0 - 10.0, dy0 - 4.0, 78.0, 98.0)
        acts.append(fuse([body, rod, foot]))
    add("Draw-latch actuators: 2 x Ø20 compact air cylinders (SMC CJ2/CQ2 class, 157 N at 0.5 MPa) that throw the latch levers",
        comp(acts), C["blue"], 8, (0, -240, 0), group="door", mat="misc", mass_kg=2 * 0.12, bom="RA3", tags=tag)

    # ---------------------------------------------------------------- 4. drawer wing heads
    # the quarter-turn studs' heads are Ø14 x 3.5 at x = +/-51, y -122.5..-119, z = lz0 + 8; a wing 26 x 4 x 9 mm in front of
    # each head (drawn horizontal, the unlocked position the robot sees first)
    x_qt, z_qt, yh = 51.0, lz0 + 8.0, -cy - 8.0 - 3.5
    for sx, side in ((-1, "left"), (1, "right")):
        wing = box(sx * x_qt - 13.0, sx * x_qt + 13.0, yh - 9.0, yh, z_qt - 2.0, z_qt + 2.0)
        add(f"Drawer latch wing head, {side} (26 mm wing on the quarter-turn stud: the robot turns it 90 deg)", wing, C["ss"], 7, (0, -200, 0),
            group="drawer", mat="ss304", mass_kg=0.005, bom="RA4", tags=tag)

    # ---------------------------------------------------------------- 5. blade-cartridge fin
    # the holder spans x xc-9..xc+9 (xc = park -106), y -53..61, z 3..34: a 4 mm fin on its front end, z 18..34, reaching 20 mm
    # forward, so the lips grip it without the blades' tips reaching the holder; its front face (y -73) stays 22 mm inside the
    # chamber's front wall (y -95)
    xc = P["x_park"]
    fin = box(xc - 2.0, xc + 2.0, -P["dose_y"] - 3.0 - 20.0, -P["dose_y"] - 3.0, 18.0, 34.0)
    add("Blade-cartridge grip fin (6061, 4 mm, on the holder's front end)", fin, C["anod"], 6, (0, 0, 220), group="recoater", mat="al6061",
        bom="RA5", tags=tag)

    # ---------------------------------------------------------------- 6. liner pull tabs
    # each side liner (0.5 mm 316L at x = +/-(ix - 0.6 .. ix - 0.1), y -70.5..85.5, z 16..104 since 2026-11-23) gets a 2 mm tab on two
    # 12 mm standoffs near its front top corner: z 88..104, y -70..-46. One part per liner, so each comes out with its own liner
    # (operations.md M3, robot-ops.md liner jobs)
    for sx, side in ((-1, "left"), (1, "right")):
        xl = sx * (ix - 0.6)
        xs = sx * (ix - 0.6 - 12.0)
        so_ = [box(min(xl, xs), max(xl, xs), y, y + 4.0, 90.0, 102.0) for y in (-68.0, -52.0)]
        pl = box(min(xs, xs - sx * 2.0), max(xs, xs - sx * 2.0), -70.0, -46.0, 88.0, 104.0)
        add(f"Liner pull tab, {side} (316L, 2 mm, 12 mm off the {side} side liner, spot-welded)", fuse(so_ + [pl]), C["ss"], 5, (sx * 60, 0, 160),
            mat="ss316l", mass_kg=0.01, bom="RA6", tags=tag)

    # ---------------------------------------------------------------- 7. fiducials
    # tag36h11 on 56 x 56 x 2 mm anodised plates on the front face of the guard's front-left post (x -420..-400, y -265), left of the
    # sliding door's travel (x >= -330) and 2 mm right of the rack's side panel (x <= -430)
    tags_ = [box(-428.0, -372.0, gy0 - 3.5, gy0 - 1.5, z, z + 56.0) for z in (-60.0, 200.0)]
    add("AprilTag plates (2 x tag36h11, 56 mm, on the guard's front-left post: wrist-camera re-registration)", comp(tags_), C["white"], 12,
        (0, -200, 0), mat="al6061", mass_kg=0.02, bom="RA7", tags=tag)
