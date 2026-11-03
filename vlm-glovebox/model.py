"""A low-profile, automation-first inert glovebox that rides on one tray of the vertical lift module (VLM).

The VLM is the Kardex Shuttle XP 500 of byu-vcl #303 (model: byu-vcl ``vertical-lab/vlm.py``). Its trays are
2450 x 864 mm, and Kardex's order sheet allows 727.5 mm of product height through the access opening, so a
stock glovebox (about 1.8-2 m tall with its stand) can't go in. This one is drawn to that envelope:

* a 1360 mm wide main chamber, 675 mm tall, with a full-width window and two 8 in glove ports that are capped
  while the box runs on its own;
* a ceiling-hung XYZ gantry with a two-finger gripper, so nothing inside needs a person;
* an automatic antechamber (load-lock) on the right, about 19 L, with a pallet that runs on rails through its
  inner and outer doors. The pallet comes out to the side, onto a landing inside the tray's footprint, where the
  UR10e reaches it from above. Nothing crosses the opening's front plane;
* a services bay on the left (dual-column purifier, blower, O2/H2O analysers, PLC, HMI) and a dry pump under
  the antechamber;
* a gas dock on the tray's back rim next to its power socket, for argon in and exhaust out.

Frame: the tray's own frame (byu-vcl vlm.tray): origin at the centre of the tray floor's underside, x to the
right and y away from you when you face the opening, z up. Millimetres. Every part is
``name -> (cadquery shape, material, group)``. The animation moves the groups.

    python model.py            # checks the envelope and writes exports/vlm_glovebox.step and out/mass_budget.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent

# ----------------------------------------------------------------------------------------- the tray (byu-vcl vlm.py)
TRAY_W, TRAY_D = 2450.0, 864.0       # Kardex Shuttle XP 500-2450x864
T_FLOOR = 3.0                        # tray floor top above the tray's underside
T_RIM = 50.0                         # rim on the back and both sides, 12 mm thick
MAX_GOODS_H = 727.5                  # Kardex: maximum product height through the opening, over the tray floor
TRAY_SOCKET = (975.0, 1075.0, 382.0, 420.0)   # x0, x1, y0, y1 of the tray's power socket (back right)

# ----------------------------------------------------------------------------------------- layout
Z0 = T_FLOOR                         # tray floor top
TOP = Z0 + 715.0                     # top of everything: 12.5 mm under Kardex's limit
SKID_H = 40.0                        # aluminium extrusion skid on anti-vibration pads
ZD = Z0 + SKID_H                     # top of the skid
WALL = 4.0                           # shell sheet (drawn); 3 mm 304 stainless with folded stiffeners in practice

CH = dict(x0=-770.0, x1=590.0, y0=-395.0, y1=345.0, z0=ZD, z1=TOP)      # main chamber, outside
DECK = ZD + WALL                     # inside floor
SV = dict(x0=-1195.0, x1=-790.0, y0=-392.0, y1=345.0, z0=ZD, z1=TOP - 15)   # services bay

PORT_X = (-340.0, 160.0)             # glove-port centres: 500 mm apart, centred on the chamber
PORT_Z = Z0 + 370.0                  # 1227 mm above the floor at the opening (tray underside at 854 mm)
PORT_R = 110.0                       # 8 in port: ~203 mm clear, ~220 mm ring
COVER_R = 124.0
RING_OUT = 12.0                      # port ring proud of the front wall
COVER_T = 18.0

# antechamber (load-lock): a box on the chamber's right wall, its axis along x
AC = dict(x0=CH["x1"], x1=CH["x1"] + 340.0, y0=-345.0, y1=-75.0, z0=Z0 + 267.0, z1=Z0 + 497.0)
AC_WALL = 8.0
DOOR_T = 14.0
# pallet: runs along x on rails through both doors (centre x when inside, in the lock, and out on the landing)
PAL = dict(w=230.0, d=200.0, t=14.0, y=-210.0)
RAIL_TOP = AC["z0"] + AC_WALL + 14.0
PAL_Z = RAIL_TOP                     # underside of the pallet
X_IN, X_LOCK, X_OUT = 440.0, 760.0, 1085.0
NEST = (-55.0, 55.0)                 # the pallet's two nests, along x from its centre

# gantry: x on two ceiling rails, y along the bridge, z down, a two-finger gripper
GX = (CH["x0"] + 95.0, CH["x1"] - 95.0)       # travel of the bridge's centre
GY = (-300.0, 260.0)
Z_RAIL = TOP - WALL - 40.0           # underside of the ceiling rails
Z_BRIDGE = Z_RAIL - 34.0             # underside of the bridge
Z_CAR = Z_BRIDGE - 50.0              # underside of the carriage
Z_HOUSING = Z_CAR - 160.0            # underside of the z housing; a two-stage telescopic z hangs from it
PAD_UP = 400.0                       # gripper pad centre with the z retracted (stroke 300 mm, down to z = 100)
STAGE = 160.0                        # length of each telescopic stage

# what is on the deck (centres)
HOTEL = dict(x=-650.0, y=90.0)       # sample hotel: 2 columns x 4 rows
HOTEL_X = (-695.0, -605.0)
HOTEL_Y = (-60.0, 40.0, 140.0, 240.0)
HOTEL_TOP = DECK + 70.0
BAL = dict(x=-330.0, y=170.0)        # automation weigh module
BAL_PAN = DECK + 118.0
STN = dict(x=-60.0, y=110.0)         # dome station: the XRD air-sensitive holder is sealed here
STN_TOP = DECK + 60.0
DOME_POST = (60.0, 110.0)            # where the dome waits
DOME_POST_TOP = DECK + 92.0

# small things (powder jar, XRD air-sensitive holder)
JAR = dict(r=22.0, h=58.0, cap_h=14.0)
HOLDER = dict(r=25.0, h=12.0, dome_r=21.0)

MATERIALS = {                        # name -> (r, g, b, opacity, specular)
    "gb_shell": (0.80, 0.81, 0.83, 1.0, 0.45),         # brushed 304 stainless
    "gb_shell_ghost": (0.80, 0.81, 0.83, 0.18, 0.2),
    "gb_frame": (0.23, 0.24, 0.26, 1.0, 0.3),          # anthracite, as the VLM's posts
    "gb_window": (0.70, 0.82, 0.90, 0.22, 0.9),        # polycarbonate
    "gb_port": (0.70, 0.71, 0.73, 1.0, 0.6),           # anodised aluminium port rings
    "gb_cover": (0.16, 0.36, 0.64, 1.0, 0.4),          # blue port covers
    "gb_glove": (0.10, 0.10, 0.11, 1.0, 0.25),         # butyl
    "gb_bay": (0.88, 0.89, 0.88, 1.0, 0.25),           # services bay cover, light grey
    "gb_bay_ghost": (0.88, 0.89, 0.88, 0.20, 0.1),
    "gb_purifier": (0.16, 0.36, 0.64, 1.0, 0.45),
    "gb_dark": (0.17, 0.17, 0.19, 1.0, 0.3),
    "gb_screen": (0.06, 0.20, 0.35, 1.0, 0.8),
    "gb_led": (0.98, 0.97, 0.88, 1.0, 0.1),
    "gb_green": (0.20, 0.80, 0.35, 1.0, 0.3),
    "gb_amber": (0.98, 0.70, 0.10, 1.0, 0.3),
    "gb_red": (0.85, 0.13, 0.10, 1.0, 0.3),
    "gb_yellow": (0.97, 0.80, 0.18, 1.0, 0.3),
    "gb_alu": (0.74, 0.75, 0.77, 1.0, 0.6),
    "gb_rail": (0.60, 0.61, 0.64, 1.0, 0.7),
    "gb_white": (0.93, 0.93, 0.92, 1.0, 0.2),
    "gb_pallet": (0.93, 0.55, 0.15, 1.0, 0.3),         # orange PEEK-look pallet: easy to follow
    "gb_glass": (0.62, 0.78, 0.90, 0.45, 0.7),
    "gb_powder": (0.55, 0.56, 0.58, 1.0, 0.05),
    "gb_cap_al": (0.75, 0.76, 0.78, 1.0, 0.5),
    "gb_cap_mg": (0.30, 0.62, 0.35, 1.0, 0.3),
    "gb_cap_si": (0.35, 0.36, 0.45, 1.0, 0.3),
    "gb_dome": (0.95, 0.80, 0.45, 0.55, 0.8),          # Kapton-amber dome
    "gb_brass": (0.80, 0.65, 0.30, 1.0, 0.6),
}


# ----------------------------------------------------------------------------------------- helpers
def box(x0, y0, z0, x1, y1, z1) -> cq.Workplane:
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl(r, h, x=0.0, y=0.0, z=0.0, axis="z") -> cq.Workplane:
    """Cylinder of radius r and length h; its axis along `axis`, starting at (x, y, z)."""
    plane = {"z": "XY", "y": "XZ", "x": "YZ"}[axis]
    c = cq.Workplane(plane).circle(r).extrude(h)
    if axis == "y":                  # XZ extrudes along -y
        c = c.mirror("XZ")
    return c.translate((x, y, z))


def tube(ro, ri, h, x=0.0, y=0.0, z=0.0, axis="z") -> cq.Workplane:
    dx, dy, dz = {"x": (-1, 0, 0), "y": (0, -1, 0), "z": (0, 0, -1)}[axis]
    return cyl(ro, h, x, y, z, axis).cut(cyl(ri, h + 2, x + dx, y + dy, z + dz, axis))


def hollow(b, t) -> cq.Workplane:
    x0, y0, z0, x1, y1, z1 = b
    return box(*b).cut(box(x0 + t, y0 + t, z0 + t, x1 - t, y1 - t, z1 - t))


def sphere_cap(r, x, y, z) -> cq.Workplane:
    s = cq.Workplane("XY").sphere(r).translate((x, y, z))
    return s.cut(box(x - r - 1, y - r - 1, z - r - 1, x + r + 1, y + r + 1, z))


# ----------------------------------------------------------------------------------------- parts
def skid(p):
    x0, x1, y0, y1 = SV["x0"], CH["x1"] + 610.0, CH["y0"], CH["y1"]
    rails = None
    for y in (y0 + 20, y1 - 20, (y0 + y1) / 2):
        r = box(x0, y - 20, Z0 + 8, x1, y + 20, ZD)
        rails = r if rails is None else rails.union(r)
    for x in (x0 + 20, -780.0, CH["x1"] - 10, x1 - 20):
        rails = rails.union(box(x - 20, y0, Z0 + 8, x + 20, y1, ZD))
    p["skid"] = (rails, "gb_frame", "gb_skid")
    pads = None
    for x in (x0 + 40, -780.0, CH["x1"] - 10, x1 - 40):
        for y in (y0 + 30, y1 - 30):
            c = cyl(28, 8, x, y, Z0)
            pads = c if pads is None else pads.union(c)
    p["skid pads"] = (pads, "gb_dark", "gb_skid")


def chamber(p):
    b = (CH["x0"], CH["y0"], CH["z0"], CH["x1"], CH["y1"], CH["z1"])
    shell = hollow(b, WALL)
    # window opening in the front wall, the inner-door opening in the right wall, purifier ports in the left wall
    wx0, wx1, wz0, wz1 = CH["x0"] + 45, CH["x1"] - 45, CH["z0"] + 70, CH["z1"] - 45
    shell = shell.cut(box(wx0, CH["y0"] - 1, wz0, wx1, CH["y0"] + WALL + 1, wz1))
    shell = shell.cut(box(CH["x1"] - WALL - 1, AC["y0"] + AC_WALL, AC["z0"] + AC_WALL, CH["x1"] + 1,
                          AC["y1"] - AC_WALL, AC["z1"] - AC_WALL))
    p["chamber shell"] = (shell, "gb_shell", "gb_chamber")
    # the front frame around the window (clamping ring with its bolts read as a dark band)
    fr = box(wx0 - 22, CH["y0"] - 10, wz0 - 22, wx1 + 22, CH["y0"], wz1 + 22).cut(
        box(wx0 + 10, CH["y0"] - 11, wz0 + 10, wx1 - 10, CH["y0"] + 1, wz1 - 10))
    p["window frame"] = (fr, "gb_frame", "gb_chamber")
    win = box(wx0, CH["y0"] + 2, wz0, wx1, CH["y0"] + 12, wz1)
    for x in PORT_X:
        win = win.cut(cyl(PORT_R + 2, 30, x, CH["y0"] - 5, PORT_Z, axis="y"))
    p["window"] = (win, "gb_window", "gb_window")
    # glove-port rings
    rings = None
    for x in PORT_X:
        r = tube(PORT_R + 18, PORT_R - 6, RING_OUT + WALL + 16, x, CH["y0"] - RING_OUT, PORT_Z, axis="y")
        rings = r if rings is None else rings.union(r)
    p["glove ports"] = (rings, "gb_port", "gb_chamber")
    # inside: deck plate, LED bar under the front of the ceiling, camera in the top front right corner
    p["LED bar"] = (box(CH["x0"] + 60, CH["y0"] + 40, CH["z1"] - WALL - 14, CH["x1"] - 60, CH["y0"] + 70,
                        CH["z1"] - WALL), "gb_led", "gb_chamber")
    cam = box(CH["x1"] - 90, CH["y0"] + 20, CH["z1"] - WALL - 45, CH["x1"] - 30, CH["y0"] + 80, CH["z1"] - WALL)
    cam = cam.union(cyl(14, 12, CH["x1"] - 60, CH["y0"] + 50, CH["z1"] - WALL - 57))
    p["camera"] = (cam, "gb_dark", "gb_chamber")
    # purifier and pressure-control ports on the left wall (into the services bay) and two KF40 feedthroughs at the back
    kf = None
    for y, z in ((250.0, TOP - 140), (250.0, ZD + 120), (120.0, ZD + 120)):
        c = cyl(32, 22, CH["x0"] - 18, y, z, axis="x")
        kf = c if kf is None else kf.union(c)
    for x in (-300.0, 0.0):
        kf = kf.union(cyl(30, 24, x, CH["y1"], TOP - 120, axis="y"))
    p["feedthroughs"] = (kf, "gb_alu", "gb_chamber")


def port_covers(p):
    """Each cover hinges on its outboard side and swings flat against the window to open."""
    for side, x in zip("LR", PORT_X):
        c = cyl(COVER_R, COVER_T, x, CH["y0"] - RING_OUT - COVER_T, PORT_Z, axis="y")
        sx = -1 if side == "L" else 1
        c = c.cut(box(x - sx * 70 - 22, CH["y0"] - RING_OUT - COVER_T - 1, PORT_Z - 40, x - sx * 70 + 22,
                      CH["y0"] - RING_OUT - COVER_T + 8, PORT_Z + 40))            # recessed pull
        p[f"port cover {side}"] = (c, "gb_cover", f"gb_cover_{side}")
        hx = x + sx * (COVER_R + 6)
        p[f"port hinge {side}"] = (cyl(7, 70, hx, CH["y0"] - RING_OUT - 9, PORT_Z - 35), "gb_frame", "gb_chamber")
        # the cover's interlock sensor: "cover on" goes to the box's PLC and to the VLM's controller
        p[f"port sensor {side}"] = (box(x - 12, CH["y0"] - 14, PORT_Z + PORT_R + 24, x + 12, CH["y0"],
                                        PORT_Z + PORT_R + 44), "gb_green", f"gb_sensor_{side}")


def gloves(p):
    """A glove in its own frame: port ring centre at the origin, reaching along +y. The animation scales it from
    stowed (folded against the port) to in use."""
    for side in "LR":
        cuff = cyl(PORT_R - 8, 120, 0, 0, 0, axis="y")
        arm = cq.Workplane("XZ").circle(PORT_R - 12).workplane(offset=-330).circle(58).loft().translate((0, 120, 0))
        hand = cq.Workplane("XY").sphere(60).translate((0, 470, 0))
        g = cuff.union(hand)
        try:
            g = g.union(arm)
        except Exception:      # noqa: BLE001  (a loft that won't fuse is still drawn on its own)
            pass
        p[f"glove {side}"] = (g, "gb_glove", f"gb_glove_{side}")


def gantry(p):
    # ceiling rails, front and back
    rails = None
    for y in (CH["y0"] + 60, CH["y1"] - 50):
        r = box(CH["x0"] + 30, y - 18, Z_RAIL, CH["x1"] - 30, y + 18, TOP - WALL)
        rails = r if rails is None else rails.union(r)
    p["gantry rails"] = (rails, "gb_rail", "gb_chamber")
    # the bridge (moves in x): its frame has x = 0 at the bridge centre
    br = box(-35, CH["y0"] + 40, Z_BRIDGE, 35, CH["y1"] - 30, Z_RAIL)
    br = br.union(box(-45, CH["y0"] + 42, Z_RAIL, 45, CH["y0"] + 78, Z_RAIL + 30))
    br = br.union(box(-45, CH["y1"] - 68, Z_RAIL, 45, CH["y1"] - 32, Z_RAIL + 30))
    p["gantry bridge"] = (br, "gb_alu", "gb_gx")
    p["gantry cable chain"] = (box(-10, CH["y1"] - 30, Z_BRIDGE + 4, 10, CH["y1"] - 12, Z_RAIL + 24), "gb_dark",
                               "gb_gx")
    # the carriage (moves in y along the bridge) and the telescopic z housing under it; y = 0 at the z axis
    p["gantry carriage"] = (box(-55, -50, Z_CAR, 55, 50, Z_BRIDGE), "gb_dark", "gb_gy")
    p["z housing"] = (box(-36, -36, Z_HOUSING, 36, 36, Z_CAR), "gb_alu", "gb_gy")
    # middle stage (moves half the stroke), built retracted
    p["z stage 1"] = (box(-29, -29, Z_HOUSING + 5, 29, 29, Z_HOUSING + 5 + STAGE - 10), "gb_rail", "gb_gz1")
    # inner stage with the gripper, built with the pad centre at z = 0
    inner = box(-22, -22, 40, 22, 22, 40 + STAGE).union(box(-42, -26, 14, 42, 26, 40))
    p["z stage 2 and gripper"] = (inner, "gb_alu", "gb_gz")
    for side in "LR":
        p[f"finger {side}"] = (box(-7, -13, -30, 7, 13, 16), "gb_dark", f"gb_finger_{side}")


def stations(p):
    # sample hotel: a two-column rack with eight seats
    h = box(HOTEL["x"] - 85, HOTEL_Y[0] - 45, DECK, HOTEL["x"] + 85, HOTEL_Y[-1] + 45, HOTEL_TOP)
    for x, depth in zip(HOTEL_X, (20.0, 6.0)):
        for y in HOTEL_Y:
            h = h.cut(cyl(26, 30, x, y, HOTEL_TOP - depth))
    p["sample hotel"] = (h, "gb_white", "gb_stations")
    # automation weigh module with a draft ring and its terminal
    b = box(BAL["x"] - 95, BAL["y"] - 140, DECK, BAL["x"] + 95, BAL["y"] + 140, DECK + 100)
    p["weigh module"] = (b, "gb_white", "gb_stations")
    p["weigh pan"] = (cyl(42, 6, BAL["x"], BAL["y"], BAL_PAN - 6).union(cyl(8, 18, BAL["x"], BAL["y"], DECK + 100)),
                      "gb_alu", "gb_stations")
    p["draft ring"] = (tube(70, 66, 52, BAL["x"], BAL["y"], DECK + 100), "gb_window", "gb_stations")
    p["weigh display"] = (box(BAL["x"] - 60, BAL["y"] - 141, DECK + 40, BAL["x"] + 60, BAL["y"] - 139, DECK + 80),
                          "gb_screen", "gb_stations")
    # dome station: a nest for the holder and a post for the dome
    s = box(STN["x"] - 70, STN["y"] - 70, DECK, STN["x"] + 70, STN["y"] + 70, STN_TOP)
    s = s.cut(cyl(HOLDER["r"] + 1.5, 8, STN["x"], STN["y"], STN_TOP - 7))
    p["dome station"] = (s, "gb_alu", "gb_stations")
    p["dome post"] = (cyl(14, DOME_POST_TOP - DECK, DOME_POST[0], DOME_POST[1], DECK), "gb_alu", "gb_stations")
    # landing inside the chamber, where the pallet stops under the gantry
    ld = None
    for y in (PAL["y"] - 80, PAL["y"] + 80):
        r = box(X_IN - 125, y - 10, RAIL_TOP - 14, CH["x1"] - WALL - 26, y + 10, RAIL_TOP)
        ld = r if ld is None else ld.union(r)
    for x in (X_IN - 110, CH["x1"] - 60):
        ld = ld.union(box(x - 10, PAL["y"] - 90, DECK, x + 10, PAL["y"] + 90, RAIL_TOP - 14))
    p["inner landing"] = (ld, "gb_rail", "gb_stations")


def antechamber(p):
    b = (AC["x0"], AC["y0"], AC["z0"], AC["x1"], AC["y1"], AC["z1"])
    body = hollow(b, AC_WALL)
    body = body.cut(box(AC["x0"] - 1, AC["y0"] + AC_WALL, AC["z0"] + AC_WALL, AC["x0"] + AC_WALL + 1,
                        AC["y1"] - AC_WALL, AC["z1"] - AC_WALL))
    body = body.cut(box(AC["x1"] - AC_WALL - 1, AC["y0"] + AC_WALL, AC["z0"] + AC_WALL, AC["x1"] + 1,
                        AC["y1"] - AC_WALL, AC["z1"] - AC_WALL))
    p["antechamber"] = (body, "gb_shell", "gb_ante")
    # flanges at both ends, the outer door's guide housing behind the outer end
    fl = box(AC["x1"], AC["y0"] - 12, AC["z0"] - 12, AC["x1"] + 16, AC["y1"] + 290, AC["z1"] + 12).cut(
        box(AC["x1"] - 1, AC["y0"] + AC_WALL, AC["z0"] + AC_WALL, AC["x1"] + 17, AC["y1"] - AC_WALL,
            AC["z1"] - AC_WALL))
    p["outer door guide"] = (fl, "gb_alu", "gb_ante")
    # rails through the lock
    rl = None
    for y in (PAL["y"] - 80, PAL["y"] + 80):
        r = box(AC["x0"] + 14, y - 10, AC["z0"] + AC_WALL, AC["x1"] - 14, y + 10, RAIL_TOP)
        rl = r if rl is None else rl.union(r)
    p["lock rails"] = (rl, "gb_rail", "gb_ante")
    # valves, gauge and a status ring on top
    v = cyl(20, 50, AC["x0"] + 90, AC["y0"] + 90, AC["z1"]).union(cyl(20, 50, AC["x0"] + 90, AC["y1"] - 60, AC["z1"]))
    v = v.union(box(AC["x0"] + 70, AC["y0"] + 70, AC["z1"] + 50, AC["x0"] + 110, AC["y1"] - 40, AC["z1"] + 75))
    p["lock valves"] = (v, "gb_alu", "gb_ante")
    p["lock gauge"] = (cyl(38, 22, AC["x0"] + 230, -210.0, AC["z1"] + 40, axis="y").union(
        cyl(8, 40, AC["x0"] + 230, -210.0, AC["z1"])), "gb_dark", "gb_ante")
    p["lock gauge face"] = (cyl(32, 2, AC["x0"] + 230, -212.0 - 1, AC["z1"] + 40, axis="y"), "gb_white", "gb_ante")
    p["lock lamp"] = (box(AC["x1"] - 40, AC["y0"] - 14, AC["z1"] - 60, AC["x1"] - 10, AC["y0"] - 4, AC["z1"] - 20),
                      "gb_green", "gb_lock_lamp")
    # supports down to the skid
    legs = None
    for x in (AC["x0"] + 30, AC["x1"] - 30):
        for y in (AC["y0"] + 20, AC["y1"] - 20):
            l_ = box(x - 15, y - 15, ZD, x + 15, y + 15, AC["z0"])
            legs = l_ if legs is None else legs.union(l_)
    p["lock legs"] = (legs, "gb_frame", "gb_ante")
    # landing outside, on the right: where the pallet comes out to the side
    ld = None
    for y in (PAL["y"] - 80, PAL["y"] + 80):
        r = box(AC["x1"] + 16 + DOOR_T + 6, y - 10, RAIL_TOP - 14, X_OUT + 112, y + 10, RAIL_TOP)
        ld = r if ld is None else ld.union(r)
    for x in (AC["x1"] + 50, X_OUT + 96):
        ld = ld.union(box(x - 12, PAL["y"] - 92, ZD, x + 12, PAL["y"] + 92, RAIL_TOP - 14))
    ld = ld.union(box(X_OUT + 112, PAL["y"] - 92, RAIL_TOP - 14, X_OUT + 120, PAL["y"] + 92, RAIL_TOP + 26))  # end stop
    p["outer landing"] = (ld, "gb_rail", "gb_ante")
    # light-grid posts on the landing's corners: the pallet only moves when the space over it is clear
    lg = None
    for y in (PAL["y"] - 118, PAL["y"] + 118):
        c = box(X_OUT + 102, y - 9, RAIL_TOP - 14, X_OUT + 120, y + 9, RAIL_TOP + 150)
        lg = c if lg is None else lg.union(c)
    p["landing light grid"] = (lg, "gb_amber", "gb_ante")


def doors(p):
    """Two sliding gates that move along +y to open. The inner one rides inside the chamber, the outer one in its
    guide on the antechamber's right end."""
    oy0, oy1 = AC["y0"] + 2, AC["y1"] - 2
    inner = box(CH["x1"] - WALL - DOOR_T - 4, oy0, AC["z0"] + 2, CH["x1"] - WALL - 4, oy1, AC["z1"] - 2)
    p["inner door"] = (inner, "gb_frame", "gb_door_in")
    p["inner door guide"] = (box(CH["x1"] - WALL - DOOR_T - 10, oy0 - 6, AC["z1"] - 2, CH["x1"] - WALL, oy1 + 290,
                                 AC["z1"] + 14), "gb_rail", "gb_chamber")
    outer = box(AC["x1"] + 16, oy0, AC["z0"] + 2, AC["x1"] + 16 + DOOR_T, oy1, AC["z1"] - 2)
    outer = outer.union(box(AC["x1"] + 16 + DOOR_T, -150, AC["z0"] + 90, AC["x1"] + 16 + DOOR_T + 18, -120,
                            AC["z1"] - 90))       # handle for a manual opening in service
    p["outer door"] = (outer, "gb_frame", "gb_door_out")


def pallet(p):
    """The pallet in its own frame: centre of its underside at the origin. Two nests along x."""
    w, d, t = PAL["w"], PAL["d"], PAL["t"]
    pl = box(-w / 2, -d / 2, 0, w / 2, d / 2, t)
    for nx in NEST:
        pl = pl.cut(cyl(HOLDER["r"] + 3, 6, nx, 0, t - 5))
    p["pallet"] = (pl, "gb_pallet", "gb_pallet")
    p["pallet RFID tag"] = (box(w / 2 - 30, -d / 2 + 10, t, w / 2 - 10, -d / 2 + 40, t + 1), "gb_dark", "gb_pallet")


def services(p):
    b = (SV["x0"], SV["y0"], SV["z0"], SV["x1"], SV["y1"], SV["z1"])
    cover = hollow(b, 3.0)
    p["services cover"] = (cover, "gb_bay", "gb_services")
    # front: HMI, e-stop, status LEDs
    hmi = box(SV["x0"] + 45, SV["y0"] - 8, SV["z1"] - 220, SV["x1"] - 45, SV["y0"], SV["z1"] - 45)
    p["HMI"] = (hmi, "gb_dark", "gb_services")
    p["HMI screen"] = (box(SV["x0"] + 55, SV["y0"] - 9, SV["z1"] - 210, SV["x1"] - 55, SV["y0"] - 8, SV["z1"] - 55),
                       "gb_screen", "gb_services")
    p["e-stop base"] = (box(SV["x1"] - 110, SV["y0"] - 18, SV["z1"] - 330, SV["x1"] - 40, SV["y0"], SV["z1"] - 260),
                        "gb_yellow", "gb_services")
    p["e-stop"] = (cyl(24, 14, SV["x1"] - 75, SV["y0"] - 32, SV["z1"] - 295, axis="y"), "gb_red", "gb_services")
    for i, (mat, name) in enumerate((("gb_green", "running"), ("gb_amber", "attention"), ("gb_red", "fault"))):
        p[f"status {name}"] = (box(SV["x0"] + 45 + i * 40, SV["y0"] - 6, SV["z1"] - 30, SV["x0"] + 75 + i * 40,
                                   SV["y0"], SV["z1"] - 15), mat, "gb_services")
    # internals (shown through the cover in the cutaway)
    cols = cyl(75, 520, SV["x0"] + 105, 175, ZD + 30).union(cyl(75, 520, SV["x1"] - 105, 175, ZD + 30))
    cols = cols.union(cyl(80, 25, SV["x0"] + 105, 175, ZD + 30 + 520)).union(cyl(80, 25, SV["x1"] - 105, 175,
                                                                                     ZD + 30 + 520))
    p["purifier columns"] = (cols, "gb_purifier", "gb_services_in")
    p["blower"] = (cyl(85, 150, SV["x0"] + 120, -170, ZD + 20).union(
        box(SV["x0"] + 200, -200, ZD + 60, SV["x1"] - 20, -140, ZD + 120)), "gb_dark", "gb_services_in")
    p["analysers"] = (box(SV["x0"] + 30, -330, ZD + 260, SV["x1"] - 30, -200, ZD + 380), "gb_white", "gb_services_in")
    p["PLC and drives"] = (box(SV["x0"] + 30, -60, ZD + 260, SV["x1"] - 30, 60, ZD + 460), "gb_alu",
                           "gb_services_in")
    p["argon buffer"] = (cyl(60, 300, SV["x0"] + 200, 40, ZD + 30, axis="y").translate((0, 0, 60)), "gb_brass",
                         "gb_services_in")


def vacuum_and_dock(p):
    # dry scroll pump under the antechamber
    p["dry pump"] = (box(AC["x0"] + 40, -330, ZD + 6, AC["x1"] - 40, -110, AC["z0"] - 45), "gb_dark", "gb_ante")
    p["pump inlet"] = (cyl(16, 45, AC["x0"] + 170, -220, AC["z0"] - 45), "gb_alu", "gb_ante")
    # gas dock on the tray's back rim beside its power socket: argon in, exhaust out (dry-break couplings)
    d = box(TRAY_SOCKET[0] - 150, 300, ZD, TRAY_SOCKET[0] - 20, 412, ZD + 100)
    p["gas dock"] = (d, "gb_frame", "gb_dock")
    p["gas dock couplings"] = (cyl(14, 7, TRAY_SOCKET[0] - 115, 412, ZD + 55, axis="y").union(
        cyl(14, 7, TRAY_SOCKET[0] - 55, 412, ZD + 55, axis="y")), "gb_brass", "gb_dock")
    # argon and exhaust lines along the back, from the dock to the services bay
    lines = None
    for z, y in ((ZD + 30, 360.0), (ZD + 70, 380.0)):
        l_ = cyl(9, TRAY_SOCKET[0] - 150 - SV["x1"], SV["x1"], y, z, axis="x")
        lines = l_ if lines is None else lines.union(l_)
    p["gas lines"] = (lines, "gb_alu", "gb_dock")


def jar(cap="gb_cap_al"):
    """A capped powder jar, base centre at the origin."""
    g = tube(JAR["r"], JAR["r"] - 2, JAR["h"] - JAR["cap_h"] + 4, 0, 0, 0)
    g = g.union(cyl(JAR["r"], 2, 0, 0, 0))
    return {"glass": (g, "gb_glass"), "powder": (cyl(JAR["r"] - 2.5, 26, 0, 0, 2), "gb_powder"),
            "cap": (cyl(JAR["r"] + 1.5, JAR["cap_h"], 0, 0, JAR["h"] - JAR["cap_h"]), cap)}


def holder():
    """An XRD air-sensitive holder base (base centre at the origin) with its powder well."""
    b = cyl(HOLDER["r"], HOLDER["h"], 0, 0, 0)
    return {"base": (b, "gb_alu"), "powder": (cyl(10, 0.8, 0, 0, HOLDER["h"]), "gb_powder")}


def dome():
    """The holder's dome, its rim at the origin."""
    d = sphere_cap(HOLDER["dome_r"], 0, 0, 0).cut(sphere_cap(HOLDER["dome_r"] - 1.5, 0, 0, 0))
    d = d.union(tube(HOLDER["r"], HOLDER["dome_r"] - 1.5, 4, 0, 0, 0))
    return {"dome": (d, "gb_dome")}


def parts() -> dict:
    p = {}
    for f in (skid, chamber, port_covers, gantry, stations, antechamber, doors, services, vacuum_and_dock):
        f(p)
    return p


def frames() -> dict:
    """Parts drawn in their own frames (the animation places them): gloves, pallet."""
    p = {}
    gloves(p)
    pallet(p)
    return p


# ----------------------------------------------------------------------------------------- checks
def bbox(shape) -> tuple:
    bb = (shape.val() if isinstance(shape, cq.Workplane) and len(shape.vals()) == 1 else
          cq.Compound.makeCompound(shape.vals())).BoundingBox()
    return bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax


LOCAL = {"gb_gz": (0.0, 0.0, PAD_UP), "gb_finger_L": (-40.0, 0.0, PAD_UP), "gb_finger_R": (40.0, 0.0, PAD_UP)}


def envelope(ps: dict) -> tuple:
    """Bounding box of every part, the gantry's gripper at its home height (x and y home are inside the chamber)."""
    bbs = []
    for s, _, g in ps.values():
        b = bbox(s)
        if g in LOCAL:
            dx, dy, dz = LOCAL[g]
            b = (b[0] + dx, b[1] + dy, b[2] + dz, b[3] + dx, b[4] + dy, b[5] + dz)
        bbs.append(b)
    return tuple(min(b[i] for b in bbs) for i in range(3)) + tuple(max(b[i] for b in bbs) for i in range(3, 6))


# rough masses: sheet and plate from the drawn volume (shells are drawn at their real thickness), bought-out items
# from typical catalogue figures for their class. Estimates, to pick the tray class, not to sign off a design.
EXTRUSION = 1.2e-6                   # aluminium extrusion, about 45 % solid
DENSITY = {"gb_shell": 7.9e-6, "gb_frame": EXTRUSION, "gb_alu": 2.7e-6, "gb_rail": EXTRUSION, "gb_window": 1.2e-6,
           "gb_port": 2.7e-6, "gb_cover": 2.7e-6, "gb_bay": 2.7e-6, "gb_pallet": 1.3e-6}   # kg / mm^3
BOUGHT = {   # part -> (kg, what)
    "purifier columns": (48.0, "two columns, Cu catalyst + 13X sieve, about 12 kg of media each, with housings"),
    "blower": (14.0, "recirculation blower, about 50 m3/h"),
    "analysers": (7.0, "O2 (zirconia/electrochemical) and H2O (capacitive) analysers"),
    "PLC and drives": (12.0, "PLC, safety relay, stepper drives, 24 V supply"),
    "argon buffer": (9.0, "10 L buffer for antechamber refills, low pressure"),
    "dry pump": (24.0, "dry scroll pump, 6 m3/h class"),
    "weigh module": (6.0, "automation weigh module, 0.1 mg class"),
    "gantry bridge": (9.0, "gantry axes with motors"),
    "HMI": (2.0, "7 in HMI"),
    "gas dock": (4.0, "dock with two dry-break couplings"),
}
# as built: 2 mm 304 stainless chamber with folded stiffeners (+10 %), 2 mm aluminium services cover, 8 mm stainless
# antechamber (it is the only part that sees vacuum)
SHEET_THICKNESS_MM = {"chamber shell": 2.0 * 1.1, "services cover": 2.0, "antechamber": 8.0}
DRAWN_MM = {"chamber shell": WALL, "services cover": 3.0, "antechamber": AC_WALL}


def mass_budget(ps: dict) -> dict:
    rows = {}
    for name, (shape, mat, _) in ps.items():
        if name in BOUGHT:
            rows[name] = round(BOUGHT[name][0], 1)
            continue
        if mat not in DENSITY:
            continue
        sh = shape.val() if len(shape.vals()) == 1 else cq.Compound.makeCompound(shape.vals())
        vol = sh.Volume()
        if name in SHEET_THICKNESS_MM:
            vol *= SHEET_THICKNESS_MM[name] / DRAWN_MM[name]
        rows[name] = round(vol * DENSITY[mat], 1)
    total = round(sum(rows.values()) * 1.15, 0)          # +15 % for fasteners, cabling, tubing, seals
    return {"parts_kg": rows, "allowance": "15 % on top for fasteners, cabling, tubing and seals", "total_kg": total}


def main():
    ps = parts()
    env = envelope(ps)
    h = env[5] - Z0
    print(f"envelope x {env[0]:.0f}..{env[3]:.0f}, y {env[1]:.0f}..{env[4]:.0f}, z {env[2]:.0f}..{env[5]:.0f} mm")
    print(f"  footprint {env[3] - env[0]:.0f} x {env[4] - env[1]:.0f} mm; tray inside its rim "
          f"{TRAY_W - 24:.0f} x {TRAY_D - 12:.0f} mm")
    print(f"  height over the tray floor {h:.1f} mm; Kardex allows {MAX_GOODS_H} mm")
    assert env[0] >= -TRAY_W / 2 + 12 and env[3] <= TRAY_W / 2 - 12, "wider than the tray"
    assert env[1] >= -TRAY_D / 2 + 5 and env[4] <= TRAY_D / 2 - 12, "deeper than the tray"
    assert h <= MAX_GOODS_H, "taller than the opening allows"
    # the pallet out on the landing and the gloves in use must stay inside the tray too
    assert X_OUT + PAL["w"] / 2 <= TRAY_W / 2 - 12, "pallet leaves the tray"
    mb = mass_budget(ps)
    print(f"  mass, estimated: {mb['total_kg']:.0f} kg (Shuttle XP 500 trays: light 228, medium 360, strong 490 kg)")
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    report = dict(envelope_mm=dict(x=[round(env[0], 1), round(env[3], 1)], y=[round(env[1], 1), round(env[4], 1)],
                                   z=[round(env[2], 1), round(env[5], 1)]),
                  height_over_tray_floor_mm=round(h, 1), kardex_max_product_height_mm=MAX_GOODS_H,
                  antechamber_volume_l=round((AC["x1"] - AC["x0"] - 2 * AC_WALL) * (AC["y1"] - AC["y0"] - 2 * AC_WALL)
                                             * (AC["z1"] - AC["z0"] - 2 * AC_WALL) / 1e6, 1),
                  chamber_inside_mm=[CH["x1"] - CH["x0"] - 2 * WALL, CH["y1"] - CH["y0"] - 2 * WALL,
                                     CH["z1"] - CH["z0"] - 2 * WALL],
                  chamber_volume_l=round((CH["x1"] - CH["x0"] - 2 * WALL) * (CH["y1"] - CH["y0"] - 2 * WALL)
                                         * (CH["z1"] - CH["z0"] - 2 * WALL) / 1e6, 0),
                  port_centre_height_at_opening_mm=854.0 + PORT_Z,
                  pallet_top_at_opening_mm=854.0 + PAL_Z + PAL["t"],
                  mass=mb, bought_out={k: v[1] for k, v in BOUGHT.items()})
    (out / "design.json").write_text(json.dumps(report, indent=1) + "\n")
    if "--step" in sys.argv or "--all" in sys.argv:
        asm = cq.Assembly(name="vlm_glovebox")
        allp = dict(ps)
        for name, (shape, mat, grp) in frames().items():
            if name.startswith("pallet"):
                shape = shape.translate((X_LOCK, PAL["y"], PAL_Z))
            elif name.startswith("glove"):
                continue
            allp[name] = (shape, mat, grp)
        for name, (shape, mat, _) in allp.items():
            r, g, b, a, _ = MATERIALS[mat]
            asm.add(shape, name=name.replace(" ", "_"), color=cq.Color(r, g, b, a))
        (HERE / "exports").mkdir(exist_ok=True)
        asm.save(str(HERE / "exports" / "vlm_glovebox.step"))
        print("wrote exports/vlm_glovebox.step")
    return report


if __name__ == "__main__":
    main()
