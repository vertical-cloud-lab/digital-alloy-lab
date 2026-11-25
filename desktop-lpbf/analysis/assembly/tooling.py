"""Assembly tooling for the two-arm UR12e cell (issue #260, PR #266): dimensioned CadQuery CAD of the custom tools and
fixtures, and envelopes of the bought end effectors at their published sizes (sources in ../../assembly-tooling.csv).

Frames (mm). An end effector (screwdriver, vacuum gripper, roller) is drawn in its mounting frame: origin on the tool
side of the tool changer, +z along the tool axis away from the arm; TCP gives the working point in that frame. A
hand tool the 2F-85 picks up (cone, pusher, bullet, loader) is drawn in its working frame with GRASP, the point between
the 2F-85's pads (the fingers close along the frame's x).

Custom tools (all new designs for this cell, nothing here has been made):
  spigot_mandrel  acetal cone + 0.45 mm sleeve that caps the M50 spigot so the 2-238 ring never meets its top edge
  spigot_pusher   tube that pushes the ring off the mandrel into the spigot groove (stops on the mandrel top)
  rod_bullet      PEEK nose plugged into the hollow rod so it enters the two 2-114 rod O-rings over a 15 deg lead-in
  ring_loader     slotted tube that carries a folded 2-114 through the gland plate's Ø15.93 throat into its groove
  roller          compliant PTFE wheel on a fork: rolls cord into a face groove (3.2 mm wheel for the 3.53 mm lid cord,
                  1.4 mm wheel for the 1.78 mm cord under a half-dovetail lip)
  ring_caps       2F-85 fingertip caps with two Ø2 pins that hold a small ring from inside (internal two-point grip)
Fixtures: fixture_C (chamber upside down on its top face, outside the lid gland), fixture_B (open stand that holds the
process base plate by its ends so the arms can reach under it), nest_stack, nest_body_inv, nest_body_up (module),
tool_stand (on each MiR's cabinet, as byu-vcl PR 318's finger stand).
"""
from __future__ import annotations

import hashlib
import math
import os
import pathlib
import pickle

import cadquery as cq
import numpy as np

V = cq.Vector
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "assembly" / "tooling"
CACHE = pathlib.Path(os.environ.get("ASM_DIR", "/tmp/asm")) / "tool-mesh-cache"

# ------------------------------------------------------------------------------------------------ bought tools (envelopes)
# Published numbers (vendor pages read 2026-11-20 22:18-22:43 UTC; every source is in assembly-tooling.csv):
#   ATI QC-21: pneumatic, 25 kg, Mxy 56.5 N m, Mz 35 N m, coupled 42.4 mm, body Ø63, 0.794 kg (+ a ~16 mm UR interface plate,
#     inferred from ATI's 52.4 mm QC-11 stack on a UR). The QC-11 (16 kg, Mxy 20.3 N m) is too weak in moment for the
#     two-arm lifts (up to ~15 N m per wrist), so QC-21.
#   OnRobot Screwdriver: 0.15-5 N m, M1.6-M6, screws <= 50 mm, 55 mm shank stroke, 2.5 kg, 308.5 x 86 x 114 mm, nose Ø49 x 60.4,
#     bit holder +13.5 mm; side-mounted (screw axis ~80 mm from the mounting face: scaled from OnRobot's drawing, an
#     estimate); works downward or sideways only, not upward; magnetic screws only (316 screws need a retaining bit).
#   Inline nutrunner for M6 (5.9-7.4 N m) and for anything driven upward: Kolver PLUTO 10CA/N class, 1.5-10 N m, 0.5 kg
#     (Brera 2022 via the Edison review); its envelope (Ø40 x 250 mm + 20 mm bit) is an ESTIMATE, not a vendor drawing.
#   OnRobot VGC10: 0.814 kg, 100 x 100 footprint, 101.5 mm to the cup faces, 6 kg with standard cups, 15 kg custom.
TC = dict(name="ATI QC-21 automatic tool changer (master + tool) on a UR interface plate", d=63.0, h=58.7, mass=0.794 + 0.10)
SCREWDRIVER = dict(name="OnRobot Screwdriver (side-mounted)", body_l=248.1, body_w=86.0, body_d=114.0, axis_z=80.0, nose_d=49.0,
                   nose_l=60.4, holder_d=16.0, holder_l=13.5, bit_d=6.35, bit_l=15.0, mass=2.5, torque=(0.15, 5.0), sizes="M1.6-M6",
                   stroke=55.0, mount_x=0.0)
NUTRUNNER = dict(name="inline nutrunner (Kolver PLUTO 10 class; envelope estimated)", body_d=40.0, body_l=250.0, bit_d=8.0, bit_l=20.0,
                 mass=0.5 + 0.3, torque=(1.5, 10.0))
NUT_ANGLE = dict(name="angle-head nutrunner (Atlas Copco / Kolver angle-head class; envelope estimated)", body_d=40.0, body_l=230.0,
                 head=(44.0, 40.0, 46.0), bit_d=8.0, bit_l=16.0, mass=1.1, torque=(0.5, 10.0))
VAC = dict(name="OnRobot VGC10", w=100.0, d=100.0, h=71.5, cup_d=30.0, cup_h=30.0, pitch=60.0, mass=0.814, payload=15.0)


def _cyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, z1 - z0, V(x, y, z0), V(0, 0, 1))


def _box(x0, x1, y0, y1, z0, z1):
    x0, x1, y0, y1, z0, z1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1)
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def _cone(r0, r1, z0, z1):
    return cq.Solid.makeCone(r0, r1, z1 - z0, V(0, 0, z0), V(0, 0, 1))


def _fuse(*s):
    out = s[0]
    for x in s[1:]:
        out = out.fuse(x)
    return out.clean()


# ------------------------------------------------------------------------------------------------ custom hand tools
# M50 spigot (module_params): port Ø96.0, spigot OD 95.8 (0.10 radial fit), bore Ø50.8, groove root Ø90.5 x 4.8 from 3.6 mm
# above the floor's underside: its top edge 11.6 mm below the spigot top. 2-238: ID 88.49, CS 3.53.
SPIGOT = dict(od=95.8, bore=50.8, groove_top=-11.6, groove_bot=-16.4, root=90.5)
MANDREL = dict(sleeve_od=96.7, sleeve_id=95.9, sleeve_l=10.6, cone_l=40.0, cone_tip_d=82.0, plug_d=50.4, plug_l=12.0,
               knob_d=24.0, knob_l=25.0)


def spigot_mandrel():
    """Origin: spigot top face on the axis, +z up (module upright). The sleeve's lower end stops 1 mm above the groove."""
    m = MANDREL
    sleeve = _cyl(m["sleeve_od"] / 2, -m["sleeve_l"], 0.0).cut(_cyl(m["sleeve_id"] / 2, -m["sleeve_l"] - 1, 0.01))
    cone = _cone(m["sleeve_od"] / 2, m["cone_tip_d"] / 2, 0.0, m["cone_l"])
    plug = _cyl(m["plug_d"] / 2, -m["plug_l"], 0.0)
    knob = _cyl(m["knob_d"] / 2, m["cone_l"], m["cone_l"] + m["knob_l"])
    return _fuse(sleeve, cone, plug, knob)


MANDREL_GRASP = (0.0, 0.0, MANDREL["cone_l"] + MANDREL["knob_l"] - 10.0)
PUSHER = dict(id=97.6, od=104.0, stroke_end=-12.0, top_t=8.0, boss_d=40.0, pocket_d=28.0, knob_d=24.0, knob_l=25.0)


def spigot_pusher():
    """Working frame = the mandrel's: drawn at the end of its stroke, its bottom edge 0.4 mm above the groove's top edge,
    its top plate resting on the mandrel's cone top (z = 40) round the knob."""
    p, m = PUSHER, MANDREL
    z_top = m["cone_l"]
    tube = _cyl(p["od"] / 2, p["stroke_end"], z_top).cut(_cyl(p["id"] / 2, p["stroke_end"] - 1, z_top + 0.01))
    plate = _cyl(p["od"] / 2, z_top, z_top + p["top_t"])
    boss = _cyl(p["boss_d"] / 2, z_top, z_top + m["knob_l"] + 6.0)
    body = _fuse(tube, plate, boss).cut(_cyl(p["pocket_d"] / 2, z_top - 1, z_top + m["knob_l"] + 2.0))
    knob = _cyl(p["knob_d"] / 2, z_top + m["knob_l"] + 6.0, z_top + m["knob_l"] + 6.0 + p["knob_l"])
    return _fuse(body, knob)


PUSHER_GRASP = (0.0, 0.0, MANDREL["cone_l"] + MANDREL["knob_l"] + 6.0 + PUSHER["knob_l"] - 10.0)
# hollow rod 5/8 x 0.065 in. (15.875 x 12.7); 2-114 rings (ID 15.54, CS 2.62) in Ø20.0 grooves, throat Ø15.93
BULLET = dict(plug_d=12.6, plug_l=15.0, bore=8.0, shoulder_d=15.85, shoulder_l=3.0, nose_d=11.0, half_angle=15.0)


def rod_bullet():
    """Origin: the rod's lower end face on its axis, +z down the rod's axis away from the rod (the direction of travel
    through the gland when the stack goes in from the top). Nose 15 deg (Parker: 15-20 deg, >= 1.1 mm for 2.62 mm)."""
    b = BULLET
    nose_l = (b["shoulder_d"] - b["nose_d"]) / 2 / math.tan(math.radians(b["half_angle"]))
    plug = _cyl(b["plug_d"] / 2, -b["plug_l"], 0.0)
    sh = _cyl(b["shoulder_d"] / 2, 0.0, b["shoulder_l"])
    nose = _cone(b["shoulder_d"] / 2, b["nose_d"] / 2, b["shoulder_l"], b["shoulder_l"] + nose_l)
    grip = _cyl(b["nose_d"] / 2, b["shoulder_l"] + nose_l, b["shoulder_l"] + nose_l + 20.0)
    return _fuse(plug, sh, nose, grip).cut(_cyl(b["bore"] / 2, -b["plug_l"] - 1, b["shoulder_l"] + nose_l + 21.0))


LOADER = dict(tube_od=15.6, tube_id=12.4, tube_l=72.0, slot_w=3.0, slot_l=28.0, block=(30.0, 30.0, 28.0))


def ring_loader():
    """Origin: tube tip on its axis, +z back along the tube toward the grip block (the tube goes in along -z)."""
    L = LOADER
    tube = _cyl(L["tube_od"] / 2, 0.0, L["tube_l"]).cut(_cyl(L["tube_id"] / 2, -1.0, L["tube_l"] - 4.0))
    tube = tube.cut(_box(-L["slot_w"] / 2, L["slot_w"] / 2, 0.0, 10.0, -1.0, L["slot_l"]))
    bx, by, bz = L["block"]
    block = _box(-bx / 2, bx / 2, -by / 2, by / 2, L["tube_l"], L["tube_l"] + bz)
    return _fuse(tube, block)


LOADER_GRASP = (0.0, 0.0, LOADER["tube_l"] + LOADER["block"][2] / 2)
ROLLER = dict(plate_d=63.0, plate_t=8.0, spring_d=44.0, spring_l=50.0, stem=(16.0, 12.0, 40.0), wheel_d=30.0, cheek_t=3.0,
              cheek_l=26.0, travel=15.0, force_N=(8.0, 25.0))


def roller(wheel_w=3.2):
    """End effector. Wheel in the frame's x-z plane, rolling along x; TCP at the wheel's lowest point."""
    R = ROLLER
    z = 0.0
    plate = _cyl(R["plate_d"] / 2, z, z + R["plate_t"])
    z += R["plate_t"]
    spring = _cyl(R["spring_d"] / 2, z, z + R["spring_l"])
    z += R["spring_l"]
    sx, sy, sl = R["stem"]
    stem = _box(-sx / 2, sx / 2, -sy / 2, sy / 2, z, z + sl)
    z += sl
    gap = wheel_w / 2 + 0.4
    cheeks = [_box(-10.0, 10.0, s * gap, s * (gap + R["cheek_t"]), z - 2.0, z + R["cheek_l"]) for s in (1, -1)]
    zc = z + R["cheek_l"] - 6.0                       # axle 6 mm above the cheek ends; wheel bottom 9 mm below them
    wheel = cq.Solid.makeCylinder(R["wheel_d"] / 2, wheel_w, V(0, -wheel_w / 2, zc), V(0, 1, 0))
    axle = cq.Solid.makeCylinder(2.0, 2 * (gap + R["cheek_t"]), V(0, -(gap + R["cheek_t"]), zc), V(0, 1, 0))
    L = zc + R["wheel_d"] / 2
    return _fuse(plate, spring, stem, *cheeks, wheel, axle), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]], float)


def ring_caps(pin_d=2.0, pin_l=6.0):
    """2F-85 fingertip caps (fingertip frames, as cell.Arm.set_caps): a 2 mm wall over the stock pad and a Ø2 pin hanging
    6 mm below the tip on the outer side, so two pins open inside a ring hold it by its ID."""
    out = {}
    for tip, s in (("left_finger_tip", -1.0), ("right_finger_tip", 1.0)):
        shell = _box(min(s * 23.0, s * 29.0), max(s * 23.0, s * 29.0), -11.0, 11.0, 10.0, 55.0)
        pin = cq.Solid.makeCylinder(pin_d / 2, pin_l, V(s * 27.0, 0.0, 55.0), V(0, 0, 1))
        out[tip] = _fuse(shell, pin)
    return out


# ------------------------------------------------------------------------------------------------ bought tools as solids
def changer():
    return _cyl(TC["d"] / 2, -TC["h"], 0.0)                 # z -h..0 below the tool-side face (drawn on the arm side)


def screwdriver(extra_bit=0.0, tip_d=3.0, tip_l=14.0):
    """OnRobot Screwdriver, side-mounted: mounting face at z = 0 (the tool side of the changer), the body above it, the
    screw axis along +x at z = axis_z. Returns (solid, T_tcp): TCP at the bit's tip, its z along the screw axis (into the
    screw)."""
    s = SCREWDRIVER
    L, a = s["body_l"], s["axis_z"]
    x0 = -L / 2 + s["mount_x"]
    body = _box(x0, x0 + L, -s["body_w"] / 2, s["body_w"] / 2, 0.0, s["body_d"])
    x1 = x0 + L
    nose = cq.Solid.makeCylinder(s["nose_d"] / 2, s["nose_l"], V(x1, 0, a), V(1, 0, 0))
    x2 = x1 + s["nose_l"]
    holder = cq.Solid.makeCylinder(s["holder_d"] / 2, s["holder_l"], V(x2, 0, a), V(1, 0, 0))
    x3 = x2 + s["holder_l"]
    shank = cq.Solid.makeCylinder(s["bit_d"] / 2, s["bit_l"] + extra_bit, V(x3, 0, a), V(1, 0, 0))
    x4 = x3 + s["bit_l"] + extra_bit
    tip = cq.Solid.makeCylinder(tip_d / 2, tip_l, V(x4, 0, a), V(1, 0, 0))      # the hex tip (across corners) ahead of the 1/4 in. shank
    x5 = x4 + tip_l
    T = np.array([[0, 0, 1, x5], [0, 1, 0, 0], [-1, 0, 0, a], [0, 0, 0, 1]], float)     # TCP z = +x, x = -z
    return _fuse(body, nose, holder, shank, tip), T


def nutrunner(extra_bit=0.0, tip_d=5.8, tip_l=14.0):
    """Inline spindle on the changer's axis; TCP at the bit's tip, z along the flange axis. A long bit for the legs' bores
    is a Ø9 extension (in the Ø11 bore) ahead of the hex tip."""
    n = NUTRUNNER
    body = _cyl(n["body_d"] / 2, 0.0, n["body_l"])
    z = n["body_l"]
    shank = _cyl(n["bit_d"] / 2, z, z + n["bit_l"])
    z += n["bit_l"]
    parts = [body, shank]
    if extra_bit:
        parts.append(_cyl(4.5, z, z + extra_bit))
        z += extra_bit
    parts.append(_cyl(tip_d / 2, z, z + tip_l))
    L = z + tip_l
    return _fuse(*parts), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]], float)


def nutrunner_angle(extra_bit=0.0, tip_d=5.8, tip_l=12.0):
    """Angle-head spindle: body along the flange axis, a 90 deg head at its end, the bit along +x. For screws driven upward
    from under a plate: the head is only ~46 mm tall, so the wrist stays 250 mm away. TCP at the bit tip, its z along +x."""
    n = NUT_ANGLE
    body = _cyl(n["body_d"] / 2, 0.0, n["body_l"])
    hx, hy, hz = n["head"]
    z0 = n["body_l"]
    head = _box(-hx / 2, hx / 2, -hy / 2, hy / 2, z0, z0 + hz)
    zc = z0 + hz / 2
    x = hx / 2
    bit = cq.Solid.makeCylinder(n["bit_d"] / 2, n["bit_l"] + extra_bit, V(x, 0, zc), V(1, 0, 0))
    x += n["bit_l"] + extra_bit
    tip = cq.Solid.makeCylinder(tip_d / 2, tip_l, V(x, 0, zc), V(1, 0, 0))
    x += tip_l
    T = np.array([[0, 0, 1, x], [0, 1, 0, 0], [-1, 0, 0, zc], [0, 0, 0, 1]], float)
    return _fuse(body, head, bit, tip), T


def vacuum():
    v = VAC
    body = _box(-v["w"] / 2, v["w"] / 2, -v["d"] / 2, v["d"] / 2, 0.0, v["h"])
    cups = [_cyl(v["cup_d"] / 2, v["h"], v["h"] + v["cup_h"], x=sx * v["pitch"] / 2, y=sy * v["pitch"] / 2)
            for sx in (-1, 1) for sy in (-1, 1)]
    L = v["h"] + v["cup_h"]
    return _fuse(body, *cups), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]], float)


# ------------------------------------------------------------------------------------------------ fixtures (machine-frame aware)
def fixture_C():
    """Chamber upside down. Frame: the chamber's top face (machine z = 120) at z = 0, machine -x along x and machine y along
    y (the chamber turned 180 deg about y). Four 6 mm strips touch the 9 mm band outside the lid gland (O-ring to +-147 x
    +-102, body to +-156 x +-111), with Ø10 reliefs round the 20 lid inserts; two Ø4.9 pins in two diagonal inserts."""
    base = _box(-200.0, 200.0, -150.0, 150.0, -45.0, -25.0)
    strips = [_box(149.5, 155.5, -96.0, 96.0, -25.0, 0.0), _box(-155.5, -149.5, -96.0, 96.0, -25.0, 0.0),
              _box(-148.0, 148.0, 104.0, 110.0, -25.0, 0.0), _box(-148.0, 148.0, -110.0, -104.0, -25.0, 0.0)]
    f = _fuse(base, *strips)
    holes = []
    by = 106.8
    for x in (-140.0, -100.0, -60.0, -20.0, 20.0, 60.0, 100.0, 140.0):
        for y in (-by, by):
            xx = math.copysign(42.0, x) if (y < 0 and abs(x) < 40) else x       # turned over about y: the drawer side stays at -y
            holes.append(_cyl(5.0, -26.0, 1.0, x=xx, y=y))
    for x in (-151.8, 151.8):
        for y in (-35.6, 35.6):
            holes.append(_cyl(5.0, -26.0, 1.0, x=x, y=y))
    f = f.cut(*holes)
    pins = [_cyl(2.45, -25.0, 6.0, x=-140.0, y=by), _cyl(2.45, -25.0, 6.0, x=140.0, y=-by)]
    return _fuse(f, *pins)


def fixture_B(z_top, x0=-420.0, x1=310.0, y0=-265.0, y1=215.0):
    """Stand for the process base plate, machine frame with the floor at z_top below the plate's underside (z = -175): two
    120 x 200 columns under the plate (x -300..-180 and 200..300, y -100..100), clear of the legs' and posts' base screws and
    the Z actuator, on a floor plate. Nothing stands beside or above the plate, so the arms reach the chamber's side walls
    and the plate's whole underside (run 1 had end frames that blocked the right-wall screws: F16, F23, F52)."""
    zb = -175.0
    zf = zb - z_top
    cols = [_box(xa, xb, -100.0, 100.0, zf + 20.0, zb) for xa, xb in ((-300.0, -180.0), (200.0, 300.0))]
    foot = _box(-340.0, 340.0, -160.0, 160.0, zf, zf + 20.0)
    return _fuse(*cols, foot)


TRUNNION = dict(h_axis=1000.0, half_span=330.0, stand=(90.0, 260.0), shaft_d=50.0, jaw=(12.0, 90.0, 70.0), jaw_y=-20.0, jaw_z=60.0)


def trunnion_stands():
    """Turn-over positioner (a motorized trunnion, e.g. a geared stepper with a brake on one stand): two stands on the floor
    and the axis bearings, in a frame whose origin is the axis point (x along the axis)."""
    t = TRUNNION
    h, hs = t["h_axis"], t["half_span"]
    sx, sy = t["stand"]
    parts = []
    for s_ in (-1, 1):
        xa = s_ * hs
        parts.append(_box(min(xa, xa + s_ * sx), max(xa, xa + s_ * sx), -sy / 2, sy / 2, -h, 60.0))
        parts.append(_box(min(xa, xa + s_ * sx), max(xa, xa + s_ * sx), -sy, sy, -h, -h + 20.0))
    return _fuse(*parts)


def trunnion_jaws():
    """The turning part: a shaft from each stand to a 12 mm jaw that clamps the chamber's side wall (machine x = +-156) at
    machine y -20, z 60, i.e. 10 mm above the turn axis (axis at machine z 50). Frame: the axis point, x along the axis."""
    t = TRUNNION
    jt, jy, jz = t["jaw"]
    parts = []
    for s_ in (-1, 1):
        x_face = s_ * 156.0
        parts.append(_box(min(x_face, x_face + s_ * jt), max(x_face, x_face + s_ * jt), t["jaw_y"] - jy / 2, t["jaw_y"] + jy / 2,
                          t["jaw_z"] - 50.0 - jz / 2, t["jaw_z"] - 50.0 + jz / 2))
        x0 = x_face + s_ * jt
        parts.append(cq.Solid.makeCylinder(t["shaft_d"] / 2, abs(t["half_span"] - abs(x0)), V(x0, 0, 0), V(s_, 0, 0)))
    return _fuse(*parts)


def nozzle():
    """Small-part vacuum nozzle on the VGC10's adaptor plate: Ø5 x 60 stem, Ø6 silicone cup. TCP at the cup's face."""
    v = VAC
    body = _box(-v["w"] / 2, v["w"] / 2, -v["d"] / 2, v["d"] / 2, 0.0, v["h"])
    stem = _cyl(2.5, v["h"], v["h"] + 60.0)
    cup = _cyl(3.0, v["h"] + 60.0, v["h"] + 66.0)
    L = v["h"] + 66.0
    return _fuse(body, stem, cup), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]], float)


# ------------------------------------------------------------------------------------------------ round 7 tools
# Liner wand (round 7, 2026-11-25): the four back liner halves (0.5 mm 316L, 130 x 24 or 130 x 16 mm, y 94.4-94.9 on the back wall)
# cannot carry hanger tabs like the side liners: the recoater carriage block (y 53-92, z 25-99) and ball nut sweep the whole width
# 2.4 mm in front of them, so anything standing forward of the sheet is hit by the carriage. run 7's stock fingers met the module
# handle and the frame in the door opening. The wand reaches them through the door opening instead: a 12 x 12 mm aluminium bar,
# 300 mm from its changer plate to the cups, with two Ø15 bellows suction cups (Schmalz / Piab Ø15 bellows class, 1.5 folds) 50 mm
# apart on a crossbar at its tip, facing along the bar. Vacuum from an ejector on the changer's air pass-through (ATI QC-21: the
# pneumatic module E6). Two Ø15 cups at -0.6 bar hold ~2 x 10 N: the liner weighs 12 g, its spring clips need a few newtons.
WAND = dict(plate_d=63.0, plate_t=8.0, bar=12.0, L=300.0, cross=(70.0, 14.0, 8.0), cup_d=15.0, cup_h=8.0, pitch=50.0, mass=0.35)


def liner_wand():
    """End effector, mounting frame (z along the bar); TCP at the cups' faces, between the two cups."""
    w = WAND
    plate = _cyl(w["plate_d"] / 2, 0.0, w["plate_t"])
    b = w["bar"] / 2
    z1 = w["L"] - w["cup_h"] - w["cross"][2]
    bar = _box(-b, b, -b, b, w["plate_t"], z1)
    cx, cy, cz = w["cross"]
    cross = _box(-cx / 2, cx / 2, -cy / 2, cy / 2, z1, z1 + cz)
    cups = [_cyl(w["cup_d"] / 2, z1 + cz, w["L"], x=s * w["pitch"] / 2) for s in (-1, 1)]
    T = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, w["L"]], [0, 0, 0, 1]], float)
    return _fuse(plate, bar, cross, *cups), T


# Ring pad (round 7): the camera window's two FKM flat rings (Ø25.2 / Ø21, 0.75-1 mm) sit in the boss's Ø25.6 counterbore, where
# the 2F-85's fingertips do not fit (run 7: F48b) and the Ø6 nozzle cup is wider than the 2.1 mm ring. An annular silicone lip
# (OD 24.6, ID 21.4, 3 mm) on a Ø8 stem under the VGC10's adaptor plate, with a soft centre plug so it also seals on the window.
# run 10 (2026-11-25): stem 55 -> 100 mm: in run 9 the VGC10 body met the camera boss 63 mm along the line of sight (F48b)
RINGPAD = dict(od=24.6, id=21.4, lip=3.0, stem_d=8.0, stem_l=100.0)


def ring_pad():
    v = VAC
    r = RINGPAD
    body = _box(-v["w"] / 2, v["w"] / 2, -v["d"] / 2, v["d"] / 2, 0.0, v["h"])
    stem = _cyl(r["stem_d"] / 2, v["h"], v["h"] + r["stem_l"])
    lip = _cyl(r["od"] / 2, v["h"] + r["stem_l"], v["h"] + r["stem_l"] + r["lip"]).cut(
        _cyl(r["id"] / 2, v["h"] + r["stem_l"] - 1, v["h"] + r["stem_l"] + r["lip"] + 1))
    plug = _cyl(r["id"] / 2 - 0.5, v["h"] + r["stem_l"], v["h"] + r["stem_l"] + r["lip"] - 0.5)
    L = v["h"] + r["stem_l"] + r["lip"]
    return _fuse(body, stem, lip, plug), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]], float)


# Pin pusher (run 10, 2026-11-25): the door's two Ø5 x 44 hinge pins go in along the hinge axis, 6 mm in front of the door's front
# face, where the 2F-85's fingertips holding a pin's end meet the door (run 9: F52, F52b). A Ø4.5 x 60 push rod (smaller than the
# Ø5.2 reamed knuckle bores, so it can follow the pin to flush) with a Ø4 x 3 NdFeB disc magnet in its tip holds the pin on its
# axis by its end face; a 12 x 12 bar 150 mm long keeps the changer and wrist outside the door's width. The pins become 17-4 PH
# (magnetic, and harder than the 304 knuckles, against galling) in place of 316. A Ø4 x 3 N52 disc holds about 3 N on steel at
# contact; the pin weighs 7 g, and the push home needs a few newtons against the reamed fit (estimate).
PINROD = dict(plate_d=63.0, plate_t=8.0, bar=12.0, bar_L=150.0, rod_d=4.5, rod_L=60.0, mass=0.30)


def pin_pusher():
    """End effector, mounting frame (z along the rod); TCP at the rod's tip face (the magnet), on the pin's axis."""
    w = PINROD
    plate = _cyl(w["plate_d"] / 2, 0.0, w["plate_t"])
    b = w["bar"] / 2
    z1 = w["plate_t"] + w["bar_L"]
    bar = _box(-b, b, -b, b, w["plate_t"], z1)
    rod = _cyl(w["rod_d"] / 2, z1, z1 + w["rod_L"])
    L = z1 + w["rod_L"]
    return _fuse(plate, bar, rod), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]], float)


def fixture_P(z_top):
    """Pedestal on the floor for the chamber's floor plate (new chamber: frame + bolted floor plate). Machine frame: the
    plate's underside (z = -20) on a 240 x 150 column top, the floor z_top below it; the plate's edges, where the 18 floor
    screws go up through U-notches, overhang the column by 36-81 mm so the nutrunner and the wrist hang free under them."""
    zf = -20.0 - z_top
    # round 6 (run 7): the column stops at x 60 (was 120), so the overflow funnel, bolted to the plate on the bench, and its KF-40
    # stub (x 66.5-122) hang beside it
    col = _box(-120.0, 60.0, -75.0, 75.0, zf + 30.0, -20.0)
    foot = _box(-220.0, 220.0, -160.0, 160.0, zf, zf + 30.0)
    return _fuse(col, foot)


def nest_stack():
    """Heater block upside down: frame = the block's top face (machine z = -10) at z = 0, machine axes turned about x.
    A Ø44 pedestal (the block is Ø50.2), so the 2F-85's fingertips pass beside it; three Ø3 pins locate the block."""
    ped = _cyl(22.0, -140.0, 0.0)
    base = _box(-45.0, 45.0, -45.0, 45.0, -146.0, -140.0)
    return _fuse(ped, base)


def nest_body_inv():
    """Module upside down on its spigot face: frame = spigot top (machine z = 0) at z = 0. Central hole for the plate's
    8 mm overtravel and the rod."""
    return _cyl(65.0, -140.0, 0.0).cut(_cyl(26.5, -141.0, 0.1))


def nest_body_up(depth=150.0):
    """Module upright, held under its flange (machine z = -30) on three 10 mm posts at r = 48, 20/90/160 deg (none in front,
    where the 2F-85 comes in for the turn-over): clear of
    the collar and gland plate (r 40.4), the gland screws' heads (r <= 38.4), the captive-screw tabs at x +-58..64, the
    dowel lugs at y +-54, the handle at x +-24, y -72..-28, and the 2F-85's fingertips on the tube along x."""
    zf = -30.0
    posts = []
    for a in (20.0, 90.0, 160.0):
        x, y = 48.0 * math.cos(math.radians(a)), 48.0 * math.sin(math.radians(a))
        posts.append(_box(x - 5.0, x + 5.0, y - 5.0, y + 5.0, zf - depth, zf))
    base = _box(-90.0, 90.0, -90.0, 90.0, zf - depth - 20.0, zf - depth).cut(_cyl(30.0, zf - depth - 21.0, zf - depth + 1.0))
    return _fuse(base, *posts)


def tool_stand():
    """Tool stand on the MiR's cabinet top behind the arm base (byu-vcl PR 318 keeps finger sets on a stand on the MiR):
    a 340 x 170 plate on two cheeks holding the parked tools; drawn as the parked envelope."""
    return _fuse(_box(-170.0, 170.0, -85.0, 85.0, 0.0, 12.0), _box(-170.0, 170.0, -85.0, 85.0, 12.0, 260.0))


# ------------------------------------------------------------------------------------------------ meshes
def tess(shape, tol=0.2, ang=0.3):
    vs, fs = shape.tessellate(tol, ang)
    return np.array([(p.x, p.y, p.z) for p in vs], float), np.array(fs, np.int32).reshape(-1, 3)


def _key(name, args):
    h = hashlib.sha256(pathlib.Path(__file__).read_bytes())
    h.update(f"{name}{args}{TC}{SCREWDRIVER}{NUTRUNNER}{NUT_ANGLE}{VAC}{TRUNNION}".encode())
    return h.hexdigest()[:16]


def mesh(name, *args, tol=0.2):
    """(v, f) of tooling function `name`(*args), cached under /tmp/asm (keyed by this file and the bought-tool sizes)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{name}-{_key(name, args)}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    r = globals()[name](*args)
    if isinstance(r, tuple):
        shp, extra = r
    else:
        shp, extra = r, None
    if isinstance(shp, dict):
        out = ({k: tess(s, tol) for k, s in shp.items()}, extra)
    else:
        out = (tess(shp, tol), extra)
    f.write_bytes(pickle.dumps(out))
    return out


def export_steps():
    """STEP of every custom tool and fixture, for the shop (analysis/out/assembly/tooling/)."""
    OUT.mkdir(parents=True, exist_ok=True)
    made = {}
    for name, fn in (("spigot_mandrel", spigot_mandrel), ("spigot_pusher", spigot_pusher), ("rod_bullet", rod_bullet),
                     ("ring_loader", ring_loader), ("roller_3p2", lambda: roller(3.2)[0]), ("roller_1p4", lambda: roller(1.4)[0]),
                     ("fixture_C", fixture_C), ("fixture_P", lambda: fixture_P(1000.0)), ("fixture_B", lambda: fixture_B(1000.0)),
                     ("trunnion_stands", trunnion_stands), ("trunnion_jaws", trunnion_jaws), ("nozzle", lambda: nozzle()[0]), ("pin_pusher", lambda: pin_pusher()[0]), ("ring_pad", lambda: ring_pad()[0]),
                     ("nest_stack", nest_stack), ("nest_body_inv", nest_body_inv), ("nest_body_up", nest_body_up),
                     ("ring_caps_left", lambda: ring_caps()["left_finger_tip"]), ("ring_caps_right", lambda: ring_caps()["right_finger_tip"])):
        s = fn()
        p = OUT / f"{name}.step"
        cq.exporters.export(cq.Workplane().add(s), str(p))
        bb = s.BoundingBox()
        made[name] = dict(file=p.name, size_mm=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)],
                          volume_cm3=round(s.Volume() / 1000.0, 2))
    return made


if __name__ == "__main__":
    import json
    print(json.dumps(export_steps(), indent=1))
