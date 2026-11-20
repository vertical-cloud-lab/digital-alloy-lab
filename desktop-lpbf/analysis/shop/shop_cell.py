"""A hypothetical robot machine shop that makes the desktop LPBF's parts (issue #260, PR #266): two UR12e arms on
MiR250s (byu-vcl PR 318's arm, gripper, wrist camera and cabinet, through analysis/robot/cell.py) working a receiving
area, a horizontal bandsaw, a Haas VF-4 with a vise and an HRT210 4th axis, a Haas ST-20-class lathe, a deburr and wash
station, a measuring station, racks and an assembly bench.

Frames: the shop frame is mm, z up, floor at z = 0. Every station has its own local frame: origin on the floor at the
middle of the face the robot works from, +y into the station (away from the aisle), x to the right as you face it.
A station's pose in the shop is (x, y, yaw in degrees).

The MiR250 + cabinet are PR 318's (800 x 580 x 300 mm, 480 mm cabinet, 20 mm plate, arm base 800 mm above the floor,
arm 130 mm towards the side it works on). One change for the shop: the arm's mounting plate is moved 190 mm towards
one end of the cabinet, which leaves a 380 x 520 mm deck on the cabinet top for the part being carried (PR 318's arm
is centred because it carries nothing). A MiR docks with its long side parallel to a station's face, `DOCK_GAP` from it.

Equipment sizes are published numbers where the source gives them (robot-shop-equipment.csv lists the sources), else
estimates marked `est`. Nothing here is a layout of a real BYU room.
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROBOT = HERE.parent / "robot"
if str(ROBOT) not in sys.path:
    sys.path.insert(0, str(ROBOT))
import cell as C  # noqa: E402  (analysis/robot/cell.py: Arm, Checker, Body, Group, box_mesh, ...)
from cell import Arm, Body, Checker, Group, Tm, box_mesh, merge, rot  # noqa: E402,F401

INCH = 25.4

# ----------------------------------------------------------------------------------------------- published numbers
# Haas VF-4 (haascnc.com VF-4 page and the VF-3/4 machine layout drawing; see robot-shop-equipment.csv)
VF4 = dict(
    travel=(50 * INCH, 20 * INCH, 25 * INCH),       # X, Y, Z: 1270 / 508 / 635 mm (Haas VF-4 page and layout drawing)
    table_L=52 * INCH, table_W=19.5 * INCH,          # 1321 x 495 mm (VF-4 page)
    nose_to_table=(107.0, 742.0),                    # spindle nose to table, min / max (VF-4 page)
    table_z=940.0,                                   # table top above the floor, standard table (VF-4 layout drawing p.3)
    table_t=95.0,                                    # table plate thickness (est)
    spindle_y=838.0,                                 # spindle centre line behind the enclosure's front face (layout drawing)
    table_front_y=341.0,                             # table's front edge behind the front face, Y nearest the door (drawing)
    door_w=1588.0,                                   # front aperture ~62.5 in: VF-3/SS layout drawing 2/2023 (same enclosure);
                                                     # the 2014 enclosure's drawing gives 49.25 in (1251 mm): checked too
    sill_z=880.0,                                    # bottom edge of the door opening (est)
    door_top_z=1900.0,                               # top edge of the door opening (est; enclosure top 2004 mm)
    front_t=60.0,                                    # front panel + door track depth (est)
    W=3128.0, D=2314.0, H=2004.0,                    # operational width, depth; enclosure top (layout drawing)
    atc_pockets=20, tool_to_tool_s=4.2,              # carousel ATC (VF-4 page)
    load_dx=-150.0,                                  # table centre at X = -150 mm at the load position (choice)
    vise_dx=450.0,                                   # vise on the table's right half, 450 mm right of its centre (choice)
)
# Haas HRT210 (haascnc.com HRT210 page, fetched 2026-11-20 22:31 UTC by the coordinator)
HRT210 = dict(platter_d=210.0, centre_h=152.4, kg_tailstock=77.1, kg_unsupported=38.6, price=17295,
              body=(430.0, 178.0, 300.0))        # along the axis x width x height (HRT210 layout drawing: 470 x 178 x 315 overall)
# 6 in. vise, Kurt DX6 class (est sizes; the pneumatic robot vise of the equipment list has the same envelope)
VISE = dict(jaw_w=6 * INCH, jaw_h=1.75 * INCH, body_L=420.0, body_h=100.0, open_max=9 * INCH)
# Haas ST-20-class lathe (est until the layout drawing is read)
# Haas ST-10 layout drawing (rev 12/2024): spindle centre line 991 mm above the floor, door opening 592 mm wide from a
# 680 mm sill, 915 mm tall (the door wraps into the roof), enclosure top 1842 mm, 1596 mm deep. Where the opening sits
# along the spindle axis and the centre line's depth behind the front are estimates (`est`).
LATHE = dict(cl_z=991.0, cl_y=450.0, chuck_d=210.0, chuck_L=100.0, door_x=(-120.0, 472.0), door_z=(680.0, 1595.0),
             front_t=60.0, W=2600.0, D=1596.0, H=1842.0, turret_d=380.0)
DOCK_GAP = 80.0             # MiR side face to the station face (PR 318 parks 80 mm from the VLM's face)
ARM_DX = -190.0             # arm base along the MiR's long axis from its centre (deck at the other end)
ARM_DY = 130.0              # arm base towards the station side (PR 318)
MIR = C.MIR                 # L, W, H, cab_h, plate
ARM_Z = MIR["H"] + MIR["cab_h"] + MIR["plate"]      # 800
DECK_Z = MIR["H"] + MIR["cab_h"] + 15.0             # deck top, 795

COL = dict(machine="#c9ced3", haas="#d8dde1", haas_dark="#5c6670", table="#8a939b", vise="#2f6db5", chuck="#7d868e",
           part="#e0a040", alu="#c7ccd1", wood="#b8925a", box="#c8a46e", rack="#e07b28", mir="#3b4148", granite="#4a4d52",
           floor="#eceff1", steel="#9aa3ab", turret="#b0b6bc", saw="#3d7f4f", wash="#5f8fb5")


# ----------------------------------------------------------------------------------------------- mesh helpers
def box(x0, x1, y0, y1, z0, z1):
    return box_mesh(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1))


def cyl(r, p0, p1, n=28):
    """Closed cylinder of radius r from p0 to p1."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    ax = p1 - p0
    z = ax / np.linalg.norm(ax)
    x = np.cross(z, [0.0, 0.0, 1.0]) if abs(z[2]) < 0.9 else np.cross(z, [1.0, 0.0, 0.0])
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ring = np.cos(t)[:, None] * x + np.sin(t)[:, None] * y
    v = np.vstack([p0 + r * ring, p1 + r * ring, p0, p1])
    f = []
    for i in range(n):
        j = (i + 1) % n
        f += [[i, j, n + j], [i, n + j, n + i], [2 * n, j, i], [2 * n + 1, n + i, n + j]]
    return v, np.array(f, np.int32)


def frame_ring(x0, x1, y0, y1, z0, z1, ix0, ix1, iy0, iy1):
    """A rectangular frame (box with a rectangular through-opening along z) as four boxes merged."""
    return merge([box(x0, x1, y0, iy0, z0, z1), box(x0, x1, iy1, y1, z0, z1),
                  box(x0, ix0, iy0, iy1, z0, z1), box(ix1, x1, iy0, iy1, z0, z1)])


def pocketed_block(x0, x1, y0, y1, z0, z1, wall, floor):
    """A block with a pocket open at the top (walls `wall` thick, floor `floor` thick)."""
    return merge([box(x0, x1, y0, y1, z0, z0 + floor),
                  frame_ring(x0, x1, y0, y1, z0 + floor, z1, x0 + wall, x1 - wall, y0 + wall, y1 - wall)])


def pose_matrix(pose):
    x, y, yaw = pose
    return Tm(rot((0, 0, 1), yaw), (x, y, 0.0))


def xf(vf, M):
    v, f = vf
    v = np.asarray(v, float) @ M[:3, :3].T + M[:3, 3]
    return v, f


# ----------------------------------------------------------------------------------------------- stations
class Station:
    """Equipment in its local frame + where MiRs dock to it."""

    def __init__(self, name, pose, items, docks, note=""):
        self.name, self.pose, self.note = name, pose, note
        self.items = items              # [(name, (v, f), colour)] in the local frame
        self.docks = docks              # {dock name: x of the MiR centre along the face (local)}
        self.M = pose_matrix(pose)

    def world_items(self):
        return [(f"{self.name}/{n}", xf(vf, self.M), c) for n, vf, c in self.items]

    def to_world(self, p):
        return (self.M @ np.r_[np.asarray(p, float), 1.0])[:3]

    def R(self):
        return self.M[:3, :3]


def vf4_items(P=VF4, vise_open=None, door_open=True, spindle_z=None, with_hrt=True, with_vise=True, fixture=None):
    """Haas VF-4 at the load position: table nearest the door in Y, shifted +X by load_dx, spindle at Z home."""
    out = []
    W, D, H = P["W"], P["D"], P["H"]
    ft, dw, s0, s1 = P["front_t"], P["door_w"], P["sill_z"], P["door_top_z"]
    # front panel round the door opening (the open sliding doors are stacked inside the side parts)
    out.append(("front panel below the door", box(-W / 2, W / 2, 0, ft, 0, s0), COL["haas"]))
    out.append(("front panel above the door", box(-W / 2, W / 2, 0, ft, s1, H), COL["haas"]))
    out.append(("front panel left of the door", box(-W / 2, -dw / 2, 0, ft, s0, s1), COL["haas"]))
    out.append(("front panel right of the door", box(dw / 2, W / 2, 0, ft, s0, s1), COL["haas"]))
    if not door_open:
        out.append(("doors (closed)", box(-dw / 2, dw / 2, ft * 0.3, ft * 0.6, s0, s1), "#9fb7c9"))
    out.append(("left wall", box(-W / 2, -W / 2 + 25, ft, D, 0, H), COL["haas"]))
    out.append(("right wall", box(W / 2 - 25, W / 2, ft, D, 0, H), COL["haas"]))
    out.append(("back wall", box(-W / 2, W / 2, D - 25, D, 0, H), COL["haas"]))
    out.append(("roof", box(-W / 2, W / 2, ft, D, H - 25, H), COL["haas"]))
    # base and chip trough in front of the table, up to the sill
    tf = P["table_front_y"]
    out.append(("base / chip trough", box(-W / 2 + 25, W / 2 - 25, ft, tf - 30, 0, s0 - 30), COL["haas_dark"]))
    # table at the load position and the saddle under it
    tz, tL, tW, tt = P["table_z"], P["table_L"], P["table_W"], P["table_t"]
    xc = P["load_dx"]
    yc = tf + tW / 2
    out.append(("table", box(xc - tL / 2, xc + tL / 2, tf, tf + tW, tz - tt, tz), COL["table"]))
    out.append(("saddle and way covers", box(-W / 2 + 60, W / 2 - 60, tf - 10, D - 700, 300, tz - tt), COL["haas_dark"]))
    # column, head, spindle; the spindle centre line is above the table centre at mid Y travel
    ysp = P["spindle_y"]
    nose = tz + (P["nose_to_table"][1] if spindle_z is None else spindle_z)
    out.append(("spindle nose", cyl(85.0, (0, ysp, nose), (0, ysp, nose + 160)), COL["steel"]))
    out.append(("tool in spindle (holder + 3/4 in. end mill)", cyl(32.0, (0, ysp, nose - 160), (0, ysp, nose)), "#6c757d"))
    out.append(("spindle head", box(-260, 260, ysp - 230, ysp + 520, nose + 160, nose + 1300), COL["haas_dark"]))
    out.append(("column", box(-520, 520, ysp + 520, D - 60, 300, nose + 1300), COL["haas_dark"]))
    # 20-pocket carousel (umbrella) tool changer, parked at the left of the head (est size)
    out.append(("carousel tool changer (20 tools)", cyl(330.0, (-620, ysp, nose + 120), (-620, ysp, nose + 330)), COL["haas_dark"]))
    # 6 in. vise on the table's right half, jaws closing along y (fixed jaw at the back); the HRT210 on the left half
    V = VISE
    vo = V["open_max"] if vise_open is None else vise_open
    vy0 = yc - V["body_L"] / 2
    xt = xc                                                  # table centre
    xc = xt + P["vise_dx"]                                   # vise centre
    jaw_back_y = yc + 60.0                                   # fixed jaw's clamping face
    if with_vise:
        out.append(("vise body", box(xc - 85, xc + 85, vy0, vy0 + V["body_L"], tz, tz + V["body_h"]), COL["vise"]))
        out.append(("vise fixed jaw", box(xc - V["jaw_w"] / 2, xc + V["jaw_w"] / 2, jaw_back_y, jaw_back_y + 40,
                                          tz + V["body_h"], tz + V["body_h"] + V["jaw_h"]), COL["vise"]))
        out.append(("vise moving jaw", box(xc - V["jaw_w"] / 2, xc + V["jaw_w"] / 2, jaw_back_y - vo - 40, jaw_back_y - vo,
                                           tz + V["body_h"], tz + V["body_h"] + V["jaw_h"]), COL["vise"]))
    if fixture is not None:                                  # (L, W, H) fixture plate on the table centre (e.g. vacuum)
        fL, fW, fH = fixture
        out.append(("fixture plate", box(xt - fL / 2, xt + fL / 2, yc - fW / 2, yc + fW / 2, tz, tz + fH), "#6a4c93"))
    if with_hrt:
        hx = xt - tL / 2 + 10
        bx, by, bz = HRT210["body"]
        ch = HRT210["centre_h"]
        out.append(("HRT210 body", box(hx, hx + bx, yc - by / 2, yc + by / 2, tz, tz + bz), "#3f4a55"))
        out.append(("HRT210 platter", cyl(HRT210["platter_d"] / 2, (hx + bx, yc, tz + ch), (hx + bx + 40, yc, tz + ch)), COL["steel"]))
        out.append(("HRT210 tailstock", box(hx + bx + 260, hx + bx + 400, yc - 70, yc + 70, tz, tz + ch + 40), "#3f4a55"))
    meta = dict(table_centre=(xt, yc, tz), vise_centre=(xc, yc, tz), vise_jaw_back_y=jaw_back_y, vise_top_z=tz + V["body_h"] + V["jaw_h"],
                vise_floor_z=tz + V["body_h"], spindle=(0.0, ysp, nose), door=(dw, s0, s1))
    return out, meta


def lathe_items(P=LATHE, door_open=True, jaw_r=55.0):
    """ST-20-class slant-bed lathe: chuck face at x = 0, spindle axis along +x, turret behind and above the centre line."""
    out = []
    W, D, H, ft = P["W"], P["D"], P["H"], P["front_t"]
    dx0, dx1 = P["door_x"]
    dz0, dz1 = P["door_z"]
    xl, xr = -1100.0, W - 1100.0
    out.append(("front panel below the door", box(xl, xr, 0, ft, 0, dz0), COL["haas"]))
    out.append(("front panel above the door", box(xl, xr, 0, ft, dz1, H), COL["haas"]))
    out.append(("front panel left of the door", box(xl, dx0, 0, ft, dz0, dz1), COL["haas"]))
    out.append(("front panel right of the door", box(dx1, xr, 0, ft, dz0, dz1), COL["haas"]))
    if not door_open:
        out.append(("door (closed)", box(dx0, dx1, ft * 0.3, ft * 0.6, dz0, dz1), "#9fb7c9"))
    out.append(("left wall", box(xl, xl + 25, ft, D, 0, H), COL["haas"]))
    out.append(("right wall", box(xr - 25, xr, ft, D, 0, H), COL["haas"]))
    out.append(("back wall", box(xl, xr, D - 25, D, 0, H), COL["haas"]))
    out.append(("roof", box(xl, xr, ft, D, H - 25, H), COL["haas"]))
    zc, yc, cd, cL = P["cl_z"], P["cl_y"], P["chuck_d"], P["chuck_L"]
    out.append(("headstock", box(xl + 25, -cL - 30, ft + 40, D - 200, 300, zc + 260), COL["haas_dark"]))
    out.append(("chuck (8 in.)", cyl(cd / 2, (-cL, yc, zc), (0, yc, zc)), COL["chuck"]))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        u = np.array([0.0, math.cos(a), math.sin(a)])
        jv, jf = box(0, 45, -14, 14, jaw_r, jaw_r + 45)       # a jaw in a frame whose +z is radial
        R = np.column_stack([[1.0, 0, 0], np.cross(u, [1.0, 0, 0]), u])
        out.append((f"chuck jaw {k + 1}", (jv @ R.T + np.array([0.0, yc, zc]), jf), COL["steel"]))
    out.append(("slant bed and chip pan", box(-cL, xr - 60, ft + 30, D - 200, 0, zc - 230), COL["haas_dark"]))
    tx, ty, tz = 520.0, yc + 330.0, zc + 170.0               # turret at its home (retracted) position
    out.append(("turret", cyl(P["turret_d"] / 2, (tx - 60, ty, tz), (tx + 60, ty, tz)), COL["turret"]))
    out.append(("turret tools (OD tool, boring bar)", box(tx - 25, tx + 25, ty - 210, ty - 160, tz - 40, tz + 40), "#6c757d"))
    out.append(("cross-slide", box(tx - 150, tx + 150, ty + 60, D - 200, tz - 250, tz + 250), COL["haas_dark"]))
    meta = dict(chuck_face=(0.0, yc, zc), door=(dx0, dx1, dz0, dz1))
    return out, meta


def saw_items():
    """Automatic horizontal bandsaw, HE&M H90A / Hyd-Mech S-20A class (est envelope): bed at 760 mm, infeed rollers."""
    out = [("saw base", box(-700, 700, 150, 900, 0, 700), COL["saw"]),
           ("saw bed / vise", box(-250, 250, 150, 700, 700, 760), COL["steel"]),
           ("saw vise jaws", box(-250, 250, 640, 700, 760, 940), COL["saw"]),
           ("saw head (raised)", box(-650, 650, 450, 820, 1150, 1700), COL["saw"]),
           ("saw head posts", box(-700, -620, 600, 820, 760, 1700), COL["saw"]),
           ("infeed roller table", box(-2000, -260, 250, 650, 0, 760), COL["steel"])]
    return out, dict(bed_z=760.0)


def bench_items(w=1830.0, d=760.0, h=900.0, vise=True):
    out = [("bench top", box(-w / 2, w / 2, 0, d, h - 40, h), COL["wood"]),
           ("bench legs and shelf", box(-w / 2 + 30, w / 2 - 30, 60, d - 60, 0, 150), COL["steel"])]
    for sx in (-1, 1):
        for y in (40, d - 40):
            out.append((f"bench leg {sx}{y}", box(sx * (w / 2 - 50) - 25, sx * (w / 2 - 50) + 25, y - 25, y + 25, 0, h - 40),
                        COL["steel"]))
    if vise:
        out.append(("bench vise (6 in.)", box(w / 2 - 420, w / 2 - 200, 120, 420, h, h + 160), COL["vise"]))
    return out, dict(top_z=h)


def wash_items():
    out, m = bench_items(w=1800, d=760, h=860, vise=False)
    out += [("ultrasonic cleaner tank (lid open)", pocketed_block(-820, -200, 150, 520, 860, 1160, 12.0, 60.0), COL["wash"]),
            ("parts basket in the tank", pocketed_block(-760, -260, 190, 480, 940, 1060, 4.0, 4.0), "#9aa3ab"),
            ("basket handle", box(-520, -500, 190, 480, 1060, 1110), "#9aa3ab"),
            ("ultrasonic lid (open, upright)", box(-820, -200, 520, 545, 1160, 1530), COL["wash"]),
            ("deburr brush spindle", box(60, 360, 250, 560, 860, 1120), "#7b5ea7"),
            ("brush wheel", cyl(75.0, (0, 330, 1050), (60, 330, 1050)), "#a58bd0"),
            ("drying air-knife box", box(480, 860, 200, 620, 860, 1150), "#6d7a86")]
    m.update(tank=(-510, 335, 1160))
    return out, m


def measure_items():
    out = [("granite plate stand", box(-430, 430, 60, 590, 0, 750), COL["steel"]),
           ("granite surface plate 36 x 24 x 6 in.", box(-457, 457, 0, 610, 750, 902), COL["granite"]),
           ("height gauge base", box(150, 300, 300, 420, 902, 940), "#d0d4d8"),
           ("height gauge column", box(205, 245, 380, 420, 940, 1400), "#d0d4d8"),
           ("height gauge scriber arm", box(110, 230, 330, 360, 1050, 1070), "#d0d4d8"),
           ("bore gauge stand", box(-380, -300, 420, 540, 902, 1180), "#d0d4d8")]
    return out, dict(top_z=902.0)


def rack_items(w=1220.0, d=610.0, shelves=(150.0, 600.0, 1050.0, 1500.0), totes=True):
    out = []
    for sx in (-1, 1):
        for y in (0, d - 40):
            out.append((f"upright {sx} {y}", box(sx * w / 2 - 20 * (sx > 0), sx * w / 2 + 20 * (sx < 0), y, y + 40, 0, 1830),
                        COL["rack"]))
    for z in shelves:
        out.append((f"shelf {int(z)}", box(-w / 2, w / 2, 0, d, z - 30, z), COL["steel"]))
        if totes and z > 500:
            for k in (-1, 1):
                out.append((f"tote {int(z)} {k}", pocketed_block(k * 300 - 200, k * 300 + 200, 60, 360, z, z + 150, 4.0, 4.0),
                            "#2b6cb0"))
                # a robot handle on the tote's front: a 20 mm tab standing 60 mm proud (our addition)
                out.append((f"tote handle {int(z)} {k}", box(k * 300 - 10, k * 300 + 10, 0, 60, z + 60, z + 140), "#1d4e89"))
    return out, dict(shelves=shelves)


def receiving_items(boxes):
    """Boxes over 11 kg on pallets on the floor (two rows), the rest on a scissor lift table at 760 mm;
    `boxes` = [(name, L, W, H, kg)]."""
    out = [("lift table top (760 mm)", box(-500, 500, 100, 900, 720, 760), COL["steel"]),
           ("lift table scissor base", box(-450, 450, 150, 850, 0, 720), "#5f6870")]
    heavy = [b for b in boxes if b[4] > 11.0]
    rows = [heavy[: (len(heavy) + 1) // 2], heavy[(len(heavy) + 1) // 2:]]
    for r, row in enumerate(rows):
        y0 = 150.0 + r * 900.0
        x = -700.0
        for name, L, W, H, kg in row:
            x0 = x - L
            out.append((f"pallet under {name}", box(x0 - 40, x + 40, y0 - 40, y0 + W + 40, 0, 144), COL["wood"]))
            out.append((f"box: {name}", box(x0, x, y0, y0 + W, 144, 144 + H), COL["box"]))
            x = x0 - 180.0
    xt = -480.0
    for name, L, W, H, kg in boxes:
        if kg <= 11.0:
            out.append((f"box: {name}", box(xt, xt + L, 120, 120 + W, 760, 760 + H), COL["box"]))
            xt += L + 20
    return out, dict(table_z=760.0)


def material_rack_items():
    out = [("cantilever rack column", box(-60, 60, 500, 640, 0, 1800), COL["rack"]),
           ("cantilever rack base", box(-900, 900, 450, 690, 0, 120), COL["rack"])]
    for z in (450.0, 950.0, 1450.0):
        out.append((f"cantilever arms {int(z)}", box(-900, 900, 80, 500, z - 40, z), COL["rack"]))
    out += [("bar stock (4 in. 316, 2-1/8 in. 6061, ...)", box(-850, 850, 120, 360, 450, 560), COL["steel"]),
            ("plate stock on edge (MIC-6, 6061)", box(1000, 1700, 250, 700, 0, 900), COL["alu"])]
    return out, {}


# ----------------------------------------------------------------------------------------------- MiR + arm
def mir_items(arm_dx=ARM_DX):
    """MiR250 + cabinet + plate (PR 318) + the parts deck, in the MiR's frame (centre on the floor, x along its length,
    +y towards the station it works at)."""
    L, W, H, Cb = MIR["L"], MIR["W"], MIR["H"], MIR["cab_h"]
    return [("MiR250 body", box(-L / 2, L / 2, -W / 2, W / 2, 30, H), COL["mir"]),
            ("MiR250 cabinet (UR control box)", box(-L / 2 + 40, L / 2 - 40, -W / 2 + 30, W / 2 - 30, H, H + Cb), COL["mir"]),
            ("arm mounting plate", box(arm_dx - 170, arm_dx + 170, -W / 2 + 30, W / 2 - 30, H + Cb, H + Cb + MIR["plate"] - 0.5),
             "#6b7480"),
            ("parts deck", box(arm_dx + 175, L / 2 - 40, -W / 2 + 30, W / 2 - 30, H + Cb, H + Cb + 15.0), "#8c96a0"),
            # PR 318 exchanges fingertips from a stand on the MiR deck: here beside the arm, on the aisle side
            ("finger stand", box(arm_dx - 110, arm_dx + 10, -W / 2 + 40, -W / 2 + 160, H + Cb + MIR["plate"], H + Cb + 100.0),
             "#d9b23a")]


def dock_frame(station: Station, x_mir, gap=DOCK_GAP):
    """World 4x4 of a MiR docked at a station: its centre x_mir along the face, its side `gap` from the face."""
    return station.M @ Tm(None, (x_mir, -(gap + MIR["W"] / 2), 0.0))


def arm_base_world(station, x_mir, gap=DOCK_GAP, arm_dx=ARM_DX):
    Mm = dock_frame(station, x_mir, gap)
    return (Mm @ np.r_[arm_dx, ARM_DY, ARM_Z, 1.0])[:3], math.degrees(math.atan2(Mm[1, 0], Mm[0, 0]))


def deck_point(station, x_mir, local=(110.0, 0.0), gap=DOCK_GAP, arm_dx=ARM_DX):
    """World point on the deck's top at deck-local (x from the deck's centre, y)."""
    Mm = dock_frame(station, x_mir, gap)
    x0 = (arm_dx + 175 + MIR["L"] / 2 - 40) / 2
    return (Mm @ np.r_[x0 + local[0] - 110.0, local[1], DECK_Z, 1.0])[:3]


# ----------------------------------------------------------------------------------------------- the shop
# Received shipments (estimates from bom.csv, mcmaster-parts.csv, quotes/; sizes and masses are estimates)
BOXES = [
    ("chamber block 13 x 9.5 x 6 in. 6061 (strapped to a pallet board)", 360, 270, 180, 34.0),
    ("plate bundle: 2 MIC-6 3/4 in., 1-1/4 in. 6061, 3/4 in. 6061", 720, 400, 110, 58.0),
    ("IPG YLR-500 laser (4U, 40 kg) in its crate", 760, 680, 380, 52.0),
    ("vacuum pump 4396K21", 520, 330, 420, 21.0),
    ("T-slot rail 14 x 4 ft (McMaster 5537T97)", 1300, 160, 160, 15.0),
    ("bar stock: 4 in. 316, 3-3/8 in. 316, 2-1/8 in. 6061 ...", 400, 300, 160, 16.0),
    ("galvo + f-theta (SCANLAB basiCube 20)", 420, 320, 300, 6.0),
    ("servos, drives, 24 V supply (Teknic, Mean Well)", 400, 300, 200, 5.0),
    ("seals, fasteners, inserts (McMaster)", 300, 250, 150, 4.0),
    ("fittings, valves, gauges, KF parts (McMaster)", 350, 300, 200, 6.0),
    ("Thorlabs window, eyewear, sensors", 300, 250, 150, 2.0),
]


def build_shop():
    """All stations at their shop poses. North row faces the aisle from y = 7000 (local +y = shop +y); south row from
    y = 4000 (local +y = shop -y)."""
    S = {}
    it, m = vf4_items()
    S["vf4"] = Station("Haas VF-4", (2600.0, 7000.0, 0.0), it, dict(left=-900.0, right=900.0, centre=0.0), "")
    S["vf4"].meta = m
    it, m = lathe_items()
    S["lathe"] = Station("CNC lathe (Haas ST-20 class)", (6700.0, 7000.0, 0.0), it, dict(centre=200.0))
    S["lathe"].meta = m
    it, m = wash_items()
    S["wash"] = Station("Deburr and wash", (9700.0, 7000.0, 0.0), it, dict(centre=0.0))
    S["wash"].meta = m
    it, m = measure_items()
    S["measure"] = Station("Measuring", (11900.0, 7000.0, 0.0), it, dict(centre=0.0))
    S["measure"].meta = m
    it, m = bench_items()
    S["bench"] = Station("Assembly bench", (14200.0, 7000.0, 0.0), it, dict(left=-500.0, right=500.0))
    S["bench"].meta = m
    it, m = receiving_items(BOXES)
    S["receiving"] = Station("Receiving", (2400.0, 4000.0, 180.0), it, dict(table=0.0, pallet=-1300.0))
    S["receiving"].meta = m
    it, m = material_rack_items()
    S["stock"] = Station("Stock racks", (5600.0, 4000.0, 180.0), it, dict(centre=0.0))
    S["stock"].meta = m
    it, m = saw_items()
    S["saw"] = Station("Horizontal bandsaw", (8600.0, 4000.0, 180.0), it, dict(centre=0.0))
    S["saw"].meta = m
    it, m = rack_items()
    S["kit"] = Station("Kitting rack", (11400.0, 4000.0, 180.0), it, dict(centre=0.0))
    S["kit"].meta = m
    S["charge"] = Station("MiR chargers", (14000.0, 4000.0, 180.0),
                          [("charger 1", box(-700, -400, 0, 120, 0, 450), "#2a9d8f"),
                           ("charger 2", box(400, 700, 0, 120, 0, 450), "#2a9d8f")], dict(c1=-550.0, c2=550.0))
    S["charge"].meta = {}
    return S


# ----------------------------------------------------------------------------------------------- routes
AISLE = dict(y0=4000.0, y1=7000.0, lanes=(5000.0, 6000.0))   # 3 m aisle: MiR250 spec, two robots passing 3000 mm
MIR_DRIVE = dict(v=1.0, a=0.3, turn_s=4.0)                     # cruise 1 m/s among people (MiR max 2.0 m/s), 0.3 m/s^2


def dock_xy(st, x_mir, gap=DOCK_GAP):
    return dock_frame(st, x_mir, gap)[:2, 3]


def route(shop, a, b, lane=0):
    """Polyline (shop xy, mm) from dock a to dock b ((station key, dock name)): out to a lane, along it, in."""
    sa, sb = shop[a[0]], shop[b[0]]
    pa, pb = dock_xy(sa, sa.docks[a[1]]), dock_xy(sb, sb.docks[b[1]])
    y = AISLE["lanes"][lane]
    return [tuple(pa), (pa[0], y), (pb[0], y), tuple(pb)]


def drive_time(poly, D=MIR_DRIVE):
    """Trapezoidal speed profile on each straight leg (a, v), plus a fixed time per turn."""
    t, L = 0.0, 0.0
    for p, q in zip(poly[:-1], poly[1:]):
        d = math.hypot(q[0] - p[0], q[1] - p[1]) / 1000.0
        if d < 1e-6:
            continue
        L += d
        v, a = D["v"], D["a"]
        if d >= v * v / a:
            t += d / v + v / a
        else:
            t += 2 * math.sqrt(d / a)
    turns = sum(1 for p, q in zip(poly[:-1], poly[1:]) if math.hypot(q[0] - p[0], q[1] - p[1]) > 1e-6) - 1
    return t + max(0, turns) * D["turn_s"], L


class ShopScene:
    """FCL world for one station (plus whatever else is passed in): what cell.Checker needs (`.world`)."""

    def __init__(self, items, mirs=(), others=()):
        self.world = Group()
        for name, (v, f), color in items:
            self.world.add(Body(name, v, f, kind="cell", color=color))
        for k, (Mm, arm_dx) in enumerate(mirs):
            for name, vf, color in mir_items(arm_dx):
                self.world.add(Body(f"mir{k}/{name}", *xf(vf, Mm), kind="cell", color=color))
        for arm in others:                    # another arm's links count as obstacles (they move with arm.place)
            for b in arm.bodies():
                self.world.add(b)

    def add_fixture(self, name, vf, color="#999999"):
        b = Body(name, *vf, kind="fixture", color=color)
        self.world.add(b)
        return b
