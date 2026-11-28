"""End-of-arm tooling for tending the desktop LPBF with a UR12e (the UR10e, renamed) and a Robotiq 2F-85 (issue #260, PR #266).

The tools follow byu-vcl PR 318's practice (round 11's specimen fingers, round 14's loading tong and the atomizer's vacuum
wand): no tool changer on the flange; the 2F-85 stays on, and each tool is either
  * a pair of caps that slip over the 2F-85's own fingertips (a spring plunger in each holds it on; a fork stand on the MiR250
    pulls them off again), or
  * a tool with a grip fin that the stock pads hold, parked in a holster on the MiR250 or beside the machine.

Tools (all ours, drawn here; the bought parts they use are in robot-tooling.csv):
  PLATE_FINGERS  cranked long caps. Each blade leaves the pad level, runs 40 mm forward, steps 45 mm down (towards the tool's
                 +y) and runs 80 mm on to a 2 mm lip at its lower inner edge. The lips take the build plate's 3 x 1.5 mm rim groove
                 (S25, M50 and L75 plates), the blade cartridge's grip fin, the reservoir's handle fin and the liners' tabs. The
                 step keeps the 2F-85's housing above the open door (its top face at z -2 when it hangs at 95 deg) while the lips
                 work 1-4 mm above the chamber floor, and puts the housing above the optics bridge for the reservoir.
  WAND           an ATEX vacuum wand (Nilfisk-type 38 mm wand with a crevice tool) wearing a clamp collar with a 30 mm grip fin,
                 as byu-vcl PR 318's atom_vacuum.md does it: nothing drilled into the certified wand.

Frames: a fingertip frame is ur_arm.gripper_fk()'s "left_finger_tip" / "right_finger_tip" (z along the finger, the stock pad's
face at x = -25.26 on the left tip and +25.26 on the right, the pad 27 mm tall along y). With the tool frame cell.frame(z=approach,
x=closing) and a level approach, the tool's +y points down, so the crank drops the lips below the pads.
"""
from __future__ import annotations

import numpy as np

PAD_X, PAD_Z = 25.26, 31.9          # ur_arm._PAD: the stock pad's face |x| and centre z in the fingertip frame

PLATE_FINGERS = dict(
    name="plate fingers (cranked caps over the 2F-85 fingertips)",
    wall=2.0,            # cap wall over the pad's face
    t=6.0,               # blade thickness (x)
    hA=7.0,              # upper blade half-height (y), level with the pads
    reach=120.0,         # pad centre -> lip centre, along the finger (z)
    drop=45.0,           # lip centre below the pad centre, along the tool's +y
    L_B=72.0,            # lower blade: crank -> lip centre (80 put the crank's corner into the front wall in a 15 deg bayonet twist)
    hB=10.0,             # lower blade height (y), its bottom edge 1.2 mm below the lip centre
    lip_d=2.0,           # the lip stands 2 mm proud of the blade's inner face (the plate groove is 1.5 deep)
    lip_h=2.4,           # lip height (the groove is 3 mm)
    lip_len=30.0,        # lip length along the finger
    mass_kg=0.18,        # both caps, 6061 (estimate from the drawn volume)
    color="#d9b23a",
)


def _box(x0, x1, y0, y1, z0, z1):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    z0, z1 = min(z0, z1), max(z0, z1)
    v = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float)
    f = np.array([[0, 1, 3], [0, 3, 2], [4, 6, 7], [4, 7, 5], [0, 4, 5], [0, 5, 1], [2, 3, 7], [2, 7, 6],
                  [0, 2, 6], [0, 6, 4], [1, 5, 7], [1, 7, 3]], np.int32)
    return v, f


def _merge(meshes):
    vs, fs, n = [], [], 0
    for v, f in meshes:
        vs.append(v)
        fs.append(f + n)
        n += len(v)
    return np.vstack(vs), np.vstack(fs)


RESERVOIR_FINGERS = dict(PLATE_FINGERS, name="straight long caps (the plate fingers without the step)", drop=0.0, mass_kg=0.15,
                         color="#c9a227")
# for the reservoir the 2F-85's knuckles have to pass over the optics bridge (its slot is 56 mm wide) and the wrist camera under the
# guard's top rail: the lips at the handle fin (z 248..258) with the pads level with them


def plate_finger_spec(s=PLATE_FINGERS):
    """cell.Arm.set_caps() spec for the plate fingers: meshes in each fingertip frame, and the grasp point (the lips' centre:
    grasp_z along the finger, grasp_y across it, inner_x the lips' faces)."""
    z_g = PAD_Z + s["reach"]                      # lip centre along the finger
    zA = z_g - s["L_B"]                           # the crank's far face
    zT = z_g + s["lip_len"] / 2 + 2.0             # blade tip
    yb1 = s["drop"] + s["lip_h"] / 2              # lower blade's bottom edge (tool +y is down)
    yb0 = yb1 - s["hB"]
    meshes = {}
    for tip, s_in in (("left_finger_tip", -1.0), ("right_finger_tip", 1.0)):
        xf = s_in * PAD_X                         # stock pad face
        xi = xf + s_in * s["wall"]                # the caps' and blades' inner face
        xo = xi - s_in * s["t"]                   # blade outer face
        xb = s_in * 16.9                          # the fingertip's back
        parts = [
            _box(xi, xf, -13.0, 13.0, 30.0, 53.5),                                  # wall over the pad
            _box(xi, xb - s_in * 2.0, -13.0, 13.0, 51.5, 53.5),                      # end plate past the fingertip
            _box(xb, xb - s_in * 2.0, -13.0, 13.0, 30.0, 53.5),                      # back wall
            _box(xi, xo, -s["hA"], s["hA"], 51.5, zA),                               # upper blade
            _box(xi, xo, -s["hA"], yb1, zA - 12.0, zA),                              # crank
            _box(xi, xo, yb0, yb1, zA - 12.0, zT),                                   # lower blade
            _box(xi, xi + s_in * s["lip_d"], yb1 - s["lip_h"], yb1, z_g - s["lip_len"] / 2, z_g + s["lip_len"] / 2),   # lip
        ]
        meshes[tip] = _merge(parts)
    return dict(name=s["name"], meshes=meshes, grasp_z=z_g, grasp_y=s["drop"], inner_x=PAD_X + s["wall"] + s["lip_d"],
                color=s["color"], mass_kg=s["mass_kg"])


# ------------------------------------------------------------------------------------------------ the vacuum wand
WAND = dict(
    name="ATEX vacuum wand with a clamp collar and grip fin (collar and fin ours, as byu-vcl PR 318 atom_vacuum.md)",
    tube_d=38.0, fin_t=30.0, fin_h=34.0, fin_l=60.0, collar_d=54.0, collar_l=60.0,
    axis_y=52.0,          # wand axis below the TCP (tool +y): the fin sits on top of the collar
    back=-70.0,           # hose cuff end, behind the TCP
    straight=230.0,       # a short wand section, level, ahead of the TCP (the 508 mm wand puts the TCP over the arm's base)
    nozzle=40.0,          # a short down-turned floor nozzle at its end: the chamber is 120 mm tall and its door opening 92 mm, so a
    nozzle_deg=90.0,      # level wand 43 mm over the floor (its collar clears the open door) with the nozzle turned down reaches every lane
    slot=(34.0, 11.0),    # crevice slot
    mass_kg=1.1,          # wand + crevice tool + collar (estimate) plus ~0.5 kg of hose hanging from the cuff
)


def _tube_mesh(p0, p1, r, n=16):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    a = p1 - p0
    L = np.linalg.norm(a)
    a = a / L
    u = np.cross(a, [1.0, 0, 0])
    if np.linalg.norm(u) < 1e-6:
        u = np.cross(a, [0, 1.0, 0])
    u /= np.linalg.norm(u)
    w = np.cross(a, u)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ring = np.array([r * (np.cos(t) * u + np.sin(t) * w) for t in ang])
    v = np.vstack([p0 + ring, p1 + ring, [p0, p1]])
    f = []
    for i in range(n):
        j = (i + 1) % n
        f += [[i, j, n + j], [i, n + j, n + i], [2 * n, j, i], [2 * n + 1, n + i, n + j]]
    return v, np.array(f, np.int32)


def wand_mesh(s=WAND):
    """The wand in the TCP frame (z = approach, +y down for a level approach); returns (v, f) and the nozzle tip (3,)."""
    y = s["axis_y"]
    a = np.radians(s["nozzle_deg"])
    bend = np.array([0.0, y, s["straight"]])
    tip = bend + s["nozzle"] * np.array([0.0, np.sin(a), np.cos(a)])
    parts = [
        _tube_mesh((0, y, s["back"]), bend, s["tube_d"] / 2),
        _tube_mesh(bend, tip, 12.0),                                                  # crevice tool (34 x 11 slot at the end)
        _tube_mesh((0, y, -s["collar_l"] / 2), (0, y, s["collar_l"] / 2), s["collar_d"] / 2),
        _box(-s["fin_t"] / 2, s["fin_t"] / 2, y - s["collar_d"] / 2 - s["fin_h"], y - s["collar_d"] / 2 + 2.0,
             -s["fin_l"] / 2, s["fin_l"] / 2),                                          # the fin the pads hold
    ]
    return _merge(parts), tip


# ------------------------------------------------------------------------------------------------ catalogue
# What the cell uses on the robot side. Prices and sources: robot-tooling.csv (written by ops.py from VENDOR below).
TOOLS = {
    "stock pads": "Robotiq 2F-85 as delivered: guard-door handle, chamber-door handle and face push, drawer tab and wing heads, "
                  "module handle, overflow jar",
    "plate fingers": "PLATE_FINGERS caps: build plate (S25, M50, L75), blade cartridge fin, reservoir handle fin, liner tabs",
    "wand": "WAND: chamber floor and wall cleaning with the ATEX vacuum",
}
