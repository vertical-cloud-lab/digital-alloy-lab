"""SOP 04's models (#262, PR #263): hardness, eddy-current conductivity and an aging series.

``REGISTRY`` (what ``stage.get(key)`` builds), ``MATERIALS``, ``SPECS`` (every figure with its source; estimates say
so), ``ANCHORS`` / ``FREE`` / ``CHECKS`` (register.py's view of a model, as in byu-vcl's instruments.py).

* ``eddy_meter``: a handheld eddy-current conductivity meter with its pencil probe and two conductivity standards.
* ``laser_flash``: a xenon-flash thermal diffusivity analyser, drawn as at the contract lab.
* ``aging_rack``: a stainless tray with five boats, one per aging time, each carrying one coupon of every alloy.
* ``quench_bath``: a stainless water bath with a lift-out mesh basket, for the water quench by hand.
* ``hv_manual``: byu-vcl's Mitutoyo HM-220 (instruments_r7.hardness: the same body, column, head, turret and
  objectives, sized from Mitutoyo's catalogue) with the stage as a person uses it: the elevating screw lowers the
  stage to load a sample by hand, the XY table steps the sample, the turret swings the indenter or an objective over
  it. The robot loading slide and holder of byu-vcl's round-8 version are left out.

Small props (coupons, tongs, the timer, the cube row, the standards, the discs) are ``Model`` builders below; the SOP
script turns them into scene entries with ``stage.props``.

Frame, as everywhere here: x to the right, y away from you facing the front, z up from what it stands on, origin at
the centre of the footprint, millimetres.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import cadquery as cq
import numpy as np

HERE = Path(__file__).resolve().parent
for _p in (str(HERE / "vl"), str(HERE / "vl" / "lab_models")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common import Model, box, cyl, hose, rbox, tube  # noqa: E402
from instruments import Instrument, Joint, _piece, _xcyl, _ycyl  # noqa: E402

# (r, g, b, opacity, shininess 0-1)
MATERIALS = {
    "p4_steel": (0.72, 0.73, 0.75, 1.0, 0.55),          # stainless sheet (tray, boats, bath)
    "p4_steel_dk": (0.50, 0.51, 0.53, 1.0, 0.45),       # stainless in shadow, wire mesh
    "p4_tongs": (0.66, 0.67, 0.70, 1.0, 0.60),          # plated steel tongs
    "p4_coupon": (0.72, 0.73, 0.75, 1.0, 0.45),         # a cut Al-alloy coupon (saw / wire EDM face)
    "p4_coupon_6063": (0.80, 0.81, 0.83, 1.0, 0.60),    # wrought 6063 bar stock, machined
    "p4_asbuilt": (0.58, 0.59, 0.61, 1.0, 0.15),        # as-printed AlSi10Mg skin: matte grey
    "p4_plate": (0.52, 0.53, 0.55, 1.0, 0.35),          # the build plate
    "p4_white": (0.93, 0.93, 0.92, 1.0, 0.20),
    "p4_offwhite": (0.86, 0.86, 0.84, 1.0, 0.20),
    "p4_light": (0.76, 0.77, 0.79, 1.0, 0.25),
    "p4_grey": (0.52, 0.54, 0.56, 1.0, 0.30),
    "p4_dark": (0.22, 0.23, 0.25, 1.0, 0.30),
    "p4_black": (0.08, 0.08, 0.09, 1.0, 0.30),
    "p4_lcd": (0.66, 0.72, 0.64, 1.0, 0.15),            # a grey-green LCD
    "p4_lcd_text": (0.14, 0.16, 0.14, 1.0, 0.10),
    "p4_screen": (0.10, 0.14, 0.20, 1.0, 0.55),         # a colour display, off-white UI drawn over it
    "p4_screen_ui": (0.80, 0.86, 0.90, 1.0, 0.10),
    "p4_red": (0.75, 0.14, 0.12, 1.0, 0.30),
    "p4_blue": (0.10, 0.33, 0.62, 1.0, 0.30),
    "p4_yellow": (0.96, 0.78, 0.18, 1.0, 0.25),
    "p4_rubber": (0.12, 0.12, 0.13, 1.0, 0.10),
    "p4_water": (0.55, 0.72, 0.86, 0.35, 0.80),         # tap water, see-through
    "p4_graphite": (0.13, 0.13, 0.14, 1.0, 0.08),       # a graphite-sprayed face
    "p4_brass": (0.80, 0.64, 0.30, 1.0, 0.60),
    "p4_copper": (0.80, 0.50, 0.33, 1.0, 0.60),
    "p4_glass": (0.82, 0.90, 0.95, 0.25, 0.90),
    "p4_hot": (0.92, 0.42, 0.12, 1.0, 0.10),            # dull orange: the flash lamp's glow, a hot element
    "p4_mitu": (0.90, 0.90, 0.88, 1.0, 0.30),           # Mitutoyo's off-white (as instruments_r7's r7_mitu)
    "p4_mitu_dk": (0.25, 0.27, 0.30, 1.0, 0.35),
    "p4_diamond": (0.55, 0.56, 0.60, 1.0, 0.80),
    "p4_label": (0.98, 0.98, 0.96, 1.0, 0.05),
    "p4_ptfe": (0.95, 0.95, 0.93, 1.0, 0.10),
    "p4_netzsch": (0.86, 0.87, 0.88, 1.0, 0.30),        # NETZSCH's light grey housings
    "p4_netzsch_dk": (0.30, 0.32, 0.35, 1.0, 0.30),
    "p4_netzsch_green": (0.00, 0.47, 0.40, 1.0, 0.30),  # NETZSCH's green accent
    "p4_sic": (0.20, 0.21, 0.23, 1.0, 0.25),            # SiC sample-holder plate
    "p4_glow_lamp": (1.00, 0.90, 0.70, 1.0, 0.10),      # the xenon flash, drawn only at the flash
}

SPECS: dict = {}          # key -> [(figure, value, source)]
ANCHORS: dict = {}
FREE: dict = {}
CHECKS: dict = {}


# ===================================================================================================== small props
COUPON = (10.0, 10.0, 3.0)        # SOP 04: flat coupons at least 10 x 10 mm and at least 2 mm thick


def coupon(mat: str = "p4_coupon") -> Model:
    """A flat aging / conductivity coupon, 10 x 10 x 3 mm, standing on z = 0, centred."""
    m = Model("p4_coupon", "Coupon 10 x 10 x 3 mm (SOP 04)")
    cx, cy, cz = COUPON
    m.add("coupon", box(-cx / 2, -cy / 2, 0, cx / 2, cy / 2, cz).edges("|Z").chamfer(0.3), mat)
    return m


# the aging rack: a tray that stays in the furnace for the batch, and five boats, one per aging time
RACK = dict(W=160.0, D=120.0, H=14.0, t=1.2, boat_w=26.0, boat_d=110.0, boat_h=5.0, pitch=30.0, tab_z=15.0,
            tab_l=20.0, coupon_y=(-39.0, -13.0, 13.0, 39.0))
BOAT_X = tuple(RACK["pitch"] * (i - 2) for i in range(5))        # -60 .. 60
TRAY_TAB_Z = 8.0                  # the tray's tab, bottom face over the tray's bottom
TIMES_H = (0.25, 1.0, 4.0, 16.0, 64.0)
ALLOYS = ("candidate", "AlSi10Mg", "6063", "Scalmalloy-type")


def boat(i: int, coupons: bool = True) -> Model:
    """Boat i (0-4) on its own: a folded stainless strip with walls and a tab that runs forward over the tray's rim,
    for the tongs; four coupons on it (one per alloy). In the tray's frame (the tray's floor top at z = t)."""
    r = RACK
    m = Model(f"p4_boat{i}", f"Aging boat {i + 1}, {TIMES_H[i]:g} h")
    x = BOAT_X[i]
    w, d, h, t = r["boat_w"], r["boat_d"], r["boat_h"], 0.8
    z0 = r["t"]
    shell = box(x - w / 2, -d / 2, z0, x + w / 2, d / 2, z0 + h).cut(
        box(x - w / 2 + t, -d / 2 + t, z0 + t, x + w / 2 - t, d / 2 - t, z0 + h + 1))
    # the tab: up the front wall, then forward 20 mm at tab_z, 10 mm wide, with a 5 mm hole
    tz = r["tab_z"]
    tab = box(x - 5, -d / 2 - t, z0, x + 5, -d / 2, tz + t).union(
        box(x - 5, -d / 2 - r["tab_l"], tz, x + 5, -d / 2, tz + t))
    tab = tab.cut(cyl(5.0, 4, x=x, y=-d / 2 - r["tab_l"] + 7, z=tz - 1))
    m.add("boat", shell.union(tab), "p4_steel")
    if coupons:
        cx, cy, cz = COUPON
        for k, y in enumerate(r["coupon_y"]):
            mat = "p4_coupon_6063" if ALLOYS[k] == "6063" else "p4_coupon"
            m.add(f"coupon {ALLOYS[k]}", box(x - cx / 2, y - cy / 2, z0 + t, x + cx / 2, y + cy / 2, z0 + t + cz)
                  .edges("|Z").chamfer(0.3), mat)
    return m


def aging_rack() -> Instrument:
    r = RACK
    W, D, H, t = r["W"], r["D"], r["H"], r["t"]
    inst = Instrument("aging_rack", "Aging rack: tray, five boats, 20 coupons", "Stainless tray and boats (our layout)",
                      (W, D + 22.0, r["tab_z"] + t), "sized to the NAT 15/65's chamber (about 300 x 340 x 150 mm) "
                      "and to 10 x 10 x 3 mm coupons; our layout")
    body = _piece(inst, "body")
    tray = box(-W / 2, -D / 2, 0, W / 2, D / 2, H).cut(box(-W / 2 + t, -D / 2 + t, t, W / 2 - t, D / 2 - t, H + 1))
    for i in range(4):                     # drain slots in the floor, between the boats
        x = (BOAT_X[i] + BOAT_X[i + 1]) / 2
        tray = tray.cut(box(x - 1.5, -D / 2 + 12, -1, x + 1.5, D / 2 - 12, t + 1))
    # the tray's own tab: forward from the front wall at mid-height, between boats 2 and 3, for the tongs
    tray = tray.union(box(-21, -D / 2 - 22, TRAY_TAB_Z, -9, -D / 2, TRAY_TAB_Z + t)).cut(
        cyl(6.0, 4, x=-15, y=-D / 2 - 15, z=TRAY_TAB_Z - 1))
    body.add("tray", tray, "p4_steel")
    for i in range(5):
        b = boat(i)
        piece = _piece(inst, f"boat{i}")
        for p in b.parts:
            piece.add(p.name, cq.Workplane().add(p.shape), p.material)
    inst.labels = [("aging tray, 160 x 120 mm", (W / 2, 0, H), (0.80, 0.30))]
    return inst


SPECS["aging_rack"] = [
    ("tray", "160 x 120 x 14 mm, 1.2 mm stainless sheet", "our layout, sized to fit the NAT 15/65 chamber "
     "(300 W x 340 D x 150 H mm as modelled in byu-vcl's furnace; 15 L) with room for the tongs"),
    ("boats", "5 x (26 x 110 x 5 mm), 0.8 mm sheet, a forward tab for the tongs", "our layout: one boat per aging "
     "time (0.25, 1, 4, 16, 64 h), so each time point is one pick with the tongs"),
    ("coupons", "10 x 10 x 3 mm; 4 per boat (candidate, AlSi10Mg, 6063, Scalmalloy-type)", "SOP 04 Samples: flat "
     "coupons >= 10 x 10 mm and >= 2 mm thick; references through the same matrix"),
]


# ------------------------------------------------------------------------------------------------- tongs
TONGS = dict(L=372.0, pivot=280.0, jaw=26.0, bend=20.0, bar_w=9.0, bar_t=3.0, open_deg=-7.0)


def tongs_jaw_mid() -> tuple:
    """The middle of the closed jaws, in the tongs' frame: what the SOP script puts on a tab."""
    p = TONGS
    b = math.radians(p["bend"])
    return (p["L"] + 0.5 * p["jaw"] * math.cos(b), 0.0, 0.5 * p["jaw"] * math.sin(b))


def tongs() -> Instrument:
    """Long crucible tongs, about 400 mm (16 in), the usual length for a benchtop furnace. Local frame: the handles'
    end at x = 0, the arms along +x to the jaw bases at x = L, the jaws bent up `bend` degrees (so they are level
    when the tongs point 20 deg down, as a person holds them), closing in the x-z plane, one above the other. The
    lower arm is the body; 'arm_a' (the upper jaw) opens about the pivot (a hinge about y)."""
    p = TONGS
    L, xp, bw, bt, jw = p["L"], p["pivot"], p["bar_w"], p["bar_t"], p["jaw"]
    b = math.radians(p["bend"])
    inst = Instrument("tongs", "Furnace tongs", "Crucible tongs, 16 in (400 mm), plated steel", (400.0, 30.0, 40.0),
                      "a common 16 in crucible / furnace tongs; proportions estimated")
    lo = _piece(inst, "body")
    up = _piece(inst, "arm_a")
    for piece, s in ((up, 1.0), (lo, -1.0)):
        z_h = -s * 14.0                   # scissors: the upper jaw's handle is the lower one
        pts = [(0.0, 0.0, z_h), (90.0, 0.0, z_h * 0.9), (xp - 30, 0.0, -s * 2.5), (xp, 0.0, 0.0),
               (L - 30, 0.0, s * 3.2), (L, 0.0, s * 3.2)]
        piece.add("arm", hose(pts, 5.0), "p4_tongs")
        # the jaw: a flat pad from the arm's end, bent up by `bend`; its gripping face 0.6 mm off the middle plane
        z0, z1 = (0.6, 0.6 + bt) if s > 0 else (-0.6 - bt, -0.6)
        pad = box(0.0, -bw / 2, z0, jw, bw / 2, z1).rotate((0, 0, 0), (0, 1, 0), -p["bend"]).translate((L, 0, 0))
        piece.add("jaw", pad.union(box(-6, -2.5, min(z0, s * 3.2 - 2.5), 2, 2.5, max(z1, s * 3.2 + 2.5))
                                   .translate((L, 0, 0))), "p4_tongs")
        piece.add("bow", tube(28, 20, 5, x=40.0, y=0.0, z=z_h - 2.5).rotate((40, 0, z_h), (41, 0, z_h), 90), "p4_tongs")
    lo.add("pivot rivet", _ycyl(9, 13, x=xp, y=-6.5, z=0.0), "p4_steel_dk")
    inst.joints = {"arm_a": Joint("hinge", axis=(0, 1, 0), pivot=(xp, 0, 0), deg=p["open_deg"])}
    return inst


SPECS["tongs"] = [("length", "about 400 mm (16 in)", "common furnace / crucible tongs lengths are 9-20 in; estimate"),
                  ("jaws", "bent up 20 deg, so they are level with the tongs held 20 deg down", "our drawing")]


# ------------------------------------------------------------------------------------------------- furnace
def furnace_hinged() -> Instrument:
    """byu-vcl's Nabertherm NAT 15/65 (instruments.furnace, fitted to Nabertherm's video), with its two hinge blocks
    drawn as hinges: a knuckle round the door's pivot and a leaf on the cabinet's side for each, and a leaf on the
    door's front. The blocks were solid across the door's swing, so the door passed through them as it opened. The
    chamber floor's front edge is 3 mm shorter, clear of the door plug. Everything else is byu-vcl's."""
    import instruments as I
    inst = I.furnace()
    p = I.FURNACE
    W, D = p["W"], p["D"]
    yf = -D / 2
    y1 = yf + p["panel_t"]
    mz0, mh = p["mouth_z0"], p["mouth_h"]
    cz = mz0 + (mh - p["ch_h"]) / 2
    body = inst.pieces["body"]
    body.parts = [q for q in body.parts if not q.name.startswith("hinge") and q.name != "chamber floor"]
    mx, cw, cd = p["mouth_x"], p["ch_w"], p["ch_d"]
    body.add("chamber floor", box(mx - cw / 2, y1 + 23, cz - 3, mx + cw / 2, y1 + cd, cz), "steel")
    px, py = W / 2 + 2, yf                       # the door's pivot (instruments.furnace's hinge joint)
    door = inst.pieces["door"]
    for zh in (mz0 + 18, mz0 + mh - 18):
        body.add(f"hinge knuckle {zh:.0f}", cyl(12, 20, x=px, y=py, z=zh), "stainless")
        body.add(f"hinge leaf {zh:.0f}", box(W / 2, py + 4, zh, W / 2 + 2.5, py + 60, zh + 20), "stainless")
        door.add(f"hinge knuckle {zh:.0f}", cyl(12, 20, x=px, y=py, z=zh - 22), "stainless")
        door.add(f"hinge leaf {zh:.0f}", box(px - 60, py - 2.5, zh - 22, px - 5, py, zh - 2), "stainless")
    inst.key = "furnace_hinged"
    return inst


# ------------------------------------------------------------------------------------------------- timer
def lab_timer() -> Model:
    """A digital lab timer, 70 x 20 x 75 mm, on its stand; the LCD faces -y."""
    m = Model("p4_timer", "Digital lab timer")
    m.add("case", rbox(70, 20, 75, 6, z=0).edges(">Z").fillet(4), "p4_white")
    m.add("lcd", box(-28, -10.6, 38, 28, -10.0, 66), "p4_lcd")
    for i, x in enumerate((-20, 0, 20)):
        m.add(f"key {i}", _ycyl(11, 2.0, x=x, y=-12.0, z=18).union(_ycyl(11, 2.0, x=x, y=-12.0, z=18)),
              ("p4_red", "p4_dark", "p4_dark")[i])
    m.add("stand", box(-30, 6, 0, 30, 24, 3), "p4_white")
    return m


def thermometer() -> Model:
    """A digital room thermometer / hygrometer, 100 x 25 x 100 mm, on its stand; the display faces -y."""
    m = Model("p4_thermometer", "Room thermometer")
    m.add("case", rbox(100, 22, 100, 8).edges(">Z").fillet(6), "p4_white")
    m.add("lcd", box(-42, -11.6, 26, 42, -11.0, 88), "p4_lcd")
    m.add("stand", box(-40, 8, 0, 40, 30, 3), "p4_white")
    return m


# ------------------------------------------------------------------------------------------------- cube row
CUBE = 10.0


def cube_row(n: int = 8, cut: bool = False) -> Model:
    """A row of n 10 mm cubes on a 100 x 100 mm build plate's strip (as-built, on 2 mm supports), x along the row."""
    m = Model("p4_cube_row", "One cube row on the build plate")
    pitch = 13.0
    x0 = -pitch * (n - 1) / 2
    m.add("plate strip", box(x0 - 14, -14, -12, -x0 + 14, 14, 0), "p4_plate")
    for i in range(n):
        x = x0 + i * pitch
        m.add(f"support {i}", box(x - CUBE / 2 + 1, -CUBE / 2 + 1, 0, x + CUBE / 2 - 1, CUBE / 2 - 1, 2.0),
              "p4_asbuilt")
        m.add(f"cube {i}", box(x - CUBE / 2, -CUBE / 2, 2.0, x + CUBE / 2, CUBE / 2, 2.0 + CUBE), "p4_asbuilt")
    return m


# ------------------------------------------------------------------------------------------------- quench bath
BATH = dict(W=240.0, D=200.0, H=210.0, t=1.5, water=165.0, basket_h=60.0, mesh=3.0)


def quench_bath() -> Instrument:
    """A stainless water bath (the size of byu-vcl's quench tank, 240 x 200 x 210 mm) with a lift-out basket of
    stainless mesh on the floor and a bail handle: the coupons drop into the water from the tongs and are lifted out
    together at the end of the batch."""
    q = BATH
    W, D, H, t = q["W"], q["D"], q["H"], q["t"]
    inst = Instrument("quench_bath", "Water quench bath", "Stainless bath with a lift-out basket (our layout)",
                      (W, D, H), "byu-vcl's quench tank's 240 x 200 x 210 mm, filled to 165 mm with tap water; the "
                      "basket and its bail are ours, for a quench by hand")
    body = _piece(inst, "body")
    body.add("bath", box(-W / 2, -D / 2, 0, W / 2, D / 2, H).cut(box(-W / 2 + t, -D / 2 + t, t, W / 2 - t, D / 2 - t,
                                                                   H + 1)).edges(">Z").fillet(0.7), "p4_steel")
    body.add("rim", box(-W / 2 - 4, -D / 2 - 4, H - 6, W / 2 + 4, D / 2 + 4, H).cut(
        box(-W / 2 + t, -D / 2 + t, H - 7, W / 2 - t, D / 2 - t, H + 1)), "p4_steel")
    body.add("water", box(-W / 2 + t + 0.3, -D / 2 + t + 0.3, t, W / 2 - t - 0.3, D / 2 - t - 0.3, q["water"]),
             "p4_water")
    bk = _piece(inst, "basket")
    bw, bd, bh = W - 24, D - 24, q["basket_h"]
    z0 = t + 4.0
    frame = box(-bw / 2, -bd / 2, z0, bw / 2, bd / 2, z0 + bh).cut(
        box(-bw / 2 + 2, -bd / 2 + 2, z0 + 2, bw / 2 - 2, bd / 2 - 2, z0 + bh + 1))
    # the mesh: open windows in the walls, slots in the floor
    for sx in (-1, 1):
        frame = frame.cut(box(sx * bw / 2 - 3, -bd / 2 + 12, z0 + 10, sx * bw / 2 + 3, bd / 2 - 12, z0 + bh - 8))
    for sy in (-1, 1):
        frame = frame.cut(box(-bw / 2 + 12, sy * bd / 2 - 3, z0 + 10, bw / 2 - 12, sy * bd / 2 + 3, z0 + bh - 8))
    for i in range(-6, 7):
        frame = frame.cut(box(i * 15 - 3, -bd / 2 + 10, z0 - 1, i * 15 + 3, bd / 2 - 10, z0 + 3))
    bk.add("basket", frame, "p4_steel_dk")
    for sx in (-1, 1):
        xa, xb = sorted((sx * (bw / 2 - 1), sx * (bw / 2 + 3)))
        bk.add(f"bail lug {sx}", box(xa, -6, z0 + bh - 14, xb, 6, z0 + bh), "p4_steel_dk")
    bail = hose([(-bw / 2 - 2, 0, z0 + bh - 6), (-bw / 2 + 10, 0, H + 45), (bw / 2 - 10, 0, H + 45),
                 (bw / 2 + 2, 0, z0 + bh - 6)], 5.0)
    bk.add("bail", bail, "p4_steel")
    inst.joints = {"basket": Joint("slide", vec=(0, 0, 1.0))}       # v in mm up
    inst.labels = [("water bath, tap water", (W / 2, -D / 2, H - 20), (0.84, 0.40))]
    return inst


SPECS["quench_bath"] = [
    ("bath", "240 x 200 x 210 mm stainless, water to 165 mm (7.3 L)", "byu-vcl r8_test.QUENCH (240 x 200 x 210 mm, "
     "our design); the basket is ours"),
]


# ------------------------------------------------------------------------------------------------- micro-Vickers
# byu-vcl's Mitutoyo HM-220 (instruments_r7.HM; Mitutoyo catalogue section K: HM-210/220 main unit 315 x 671 x 595 mm,
# 43 kg, motorized turret for up to 4 objectives and 2 indenters; Type D adds the motorized XY stage 50 x 50 mm on a
# 130 x 130 mm table, motorized focus 1.4 mm and AVPAK). The same body, column, head, camera, turret and objectives;
# here the stage is the person's: an elevating screw (the handwheel at the left) lowers the whole stage 30 mm to load a
# sample by hand; the XY table carries it; the turret's angle is a joint in degrees (0: the 50x objective over the
# sample, +90: the 10x, -90: the indenter); the indenter rides on the turret and comes down `press` mm onto the face.
HV = dict(W=315.0, D=671.0, H=595.0, base_h=140.0, ax=(0.0, -170.0), tur_c=(0.0, -120.0), tur_r=50.0, tip_z=280.0,
          table=252.0, wd=3.0)


def hv_manual() -> Instrument:
    p = HV
    inst = Instrument("hv_manual", "Micro-Vickers hardness tester", "Mitutoyo HM-220 Type D (AVPAK)",
                      (533.0, 672.0, 595.0), "byu-vcl's HM-220 (instruments_r7): Mitutoyo catalogue section K "
                      "(main unit 315 x 671 x 595 mm, 43 kg) and Mitutoyo's photos; the stage made manual here")
    w, d, h = p["W"], p["D"], p["H"]
    ax, ay = p["ax"]
    tx, ty = p["tur_c"]
    body = _piece(inst, "body")
    base = rbox(w, d, p["base_h"], 24).edges(">Z").fillet(10).cut(cyl(96, 60, x=ax, y=ay, z=p["base_h"] - 50))
    body.add("base", base, "p4_mitu")
    body.add("base panel", box(-110, -d / 2 - 1, 40, 110, -d / 2, 110), "p4_mitu_dk")
    body.add("screw collar", tube(110, 96, 6, x=ax, y=ay, z=p["base_h"]), "p4_mitu_dk")
    body.add("column", rbox(200, 255, h - 35 - p["base_h"], 30, y=d / 2 - 127.5, z=p["base_h"]), "p4_mitu")
    body.add("head", rbox(230, 586, 180, 30, y=d / 2 - 293, z=380).edges(">Z").fillet(14), "p4_mitu")
    body.add("head band", box(-116, -251, 470, 116, d / 2 - 30, 480), "p4_mitu_dk")
    body.add("camera", rbox(50, 60, 35, 8, x=ax, y=ay, z=560), "p4_mitu_dk")
    body.add("lens tube", cyl(40, 0.5 + 380 - 360, x=tx, y=ty, z=360), "p4_mitu_dk")
    # the AVPAK PC, its monitor and the joystick box at the right (estimate, as byu-vcl's)
    body.add("PC", box(185, 0, 0, 355, 335, 330), "p4_dark")
    body.add("PC light", box(250, -1.5, 280, 290, 0, 286), "p4_blue")
    body.add("monitor stand", box(235, 120, 330, 305, 170, 345).union(box(262, 140, 345, 278, 155, 420)), "p4_black")
    body.add("monitor", box(130, 120, 410, 410, 145, 590), "p4_black")
    body.add("monitor screen", box(138, 119.4, 418, 402, 120.0, 582), "p4_screen")
    body.add("joystick box", box(205, -320, 0, 335, -200, 45).edges(">Z").fillet(8), "p4_mitu_dk")
    body.add("joystick", cyl(14, 50, x=290, y=-260, z=45).union(cq.Workplane("XY").sphere(11).translate((290, -260, 98))),
             "p4_black")
    hw = _piece(inst, "handwheel")
    wheel = _xcyl(110, 16, x=-w / 2 - 20, y=ay + 40, z=90).cut(_xcyl(84, 20, x=-w / 2 - 22, y=ay + 40, z=90))
    wheel = wheel.union(_xcyl(30, 22, x=-w / 2 - 22, y=ay + 40, z=90))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        spoke = box(-w / 2 - 18, -4, 0, -w / 2 - 6, 4, 50).rotate((0, 0, 0), (1, 0, 0), math.degrees(a) - 90)
        wheel = wheel.union(spoke.translate((0, ay + 40, 90)))
    wheel = wheel.union(_xcyl(14, 30, x=-w / 2 - 50, y=ay + 40, z=90 + 46))
    hw.add("handwheel", wheel, "p4_mitu_dk")
    sz = _piece(inst, "stage_z")
    sz.add("elevating screw", cyl(90, 110, x=ax, y=ay, z=p["base_h"] - 50), "p4_mitu_dk")
    sz.add("Y carriage", box(-90, ay - 90, 200, 90, ay + 90, 222), "p4_mitu_dk")
    sy = _piece(inst, "stage_y")
    sy.add("X carriage", box(-75, ay - 65, 222, 75, ay + 65, 244), "p4_mitu_dk")
    sx = _piece(inst, "stage_x")
    sx.add("table", rbox(130, 130, 8, 6, x=ax, y=ay, z=244), "p4_steel")
    tur = _piece(inst, "turret")
    tur.add("turret", cyl(150, 25, x=tx, y=ty, z=355), "p4_mitu_dk")
    r = p["tur_r"]
    for nm, ang, dia in (("objective 50x", -90.0, 26.0), ("objective 10x", 180.0, 28.0),
                         ("objective 100x", 90.0, 24.0)):
        ox, oy = tx + r * math.cos(math.radians(ang)), ty + r * math.sin(math.radians(ang))
        tur.add(nm, cyl(dia, 355 - p["tip_z"], x=ox, y=oy, z=p["tip_z"]), "p4_steel")
        tur.add(nm + " band", cyl(dia + 2, 8, x=ox, y=oy, z=330), "p4_mitu_dk")
    ind = _piece(inst, "indenter")
    ix, iy = tx + r, ty
    ind.add("indenter", cyl(24, 60, x=ix, y=iy, z=p["tip_z"] + 15), "p4_steel")
    ind.add("diamond mount", cyl(8, 15, x=ix, y=iy, z=p["tip_z"] + 1.5), "p4_steel_dk")
    # the Vickers diamond: a square pyramid, 136 deg between opposite faces, point down at tip_z
    hgt = 1.5
    half = hgt * math.tan(math.radians(68.0))
    pyr = cq.Workplane("XY").add(cq.Solid.makeLoft([
        cq.Wire.makePolygon([cq.Vector(ix - half, iy, p["tip_z"] + hgt), cq.Vector(ix, iy - half, p["tip_z"] + hgt),
                             cq.Vector(ix + half, iy, p["tip_z"] + hgt), cq.Vector(ix, iy + half, p["tip_z"] + hgt)],
                            close=True),
        cq.Wire.makePolygon([cq.Vector(ix - 0.01, iy, p["tip_z"]), cq.Vector(ix, iy - 0.01, p["tip_z"]),
                             cq.Vector(ix + 0.01, iy, p["tip_z"]), cq.Vector(ix, iy + 0.01, p["tip_z"])], close=True)],
        True))
    ind.add("diamond", pyr, "p4_diamond")
    inst.joints = {
        "handwheel": Joint("hinge", axis=(1, 0, 0), pivot=(0, ay + 40, 90), deg=-1.0),     # v in degrees
        "stage_z": Joint("slide", vec=(0, 0, -1.0)),                                        # v in mm down
        "stage_y": Joint("slide", vec=(0, 1.0, 0), parent="stage_z"),                       # v in mm
        "stage_x": Joint("slide", vec=(1.0, 0, 0), parent="stage_y"),                       # v in mm
        "turret": Joint("hinge", axis=(0, 0, 1), pivot=(tx, ty, 0), deg=1.0),               # v in degrees
        "indenter": Joint("slide", vec=(0, 0, -1.0), parent="turret"),                      # v in mm down
    }
    inst.labels = [("motorized turret: indenter, 10x, 50x", (tx - 75, ty, 367), (0.12, 0.30)),
                   ("XY table, 130 x 130 mm", (-65, ay - 65, 252), (0.12, 0.70)),
                   ("AVPAK PC, monitor, joystick", (270, 120, 500), (0.86, 0.30))]
    return inst


def hv_focus_z(sample_h: float) -> float:
    """stage_z (mm down) that puts the face of a sample sample_h tall on the table wd under the objectives' tips."""
    p = HV
    return -(p["tip_z"] - p["wd"] - (p["table"] + sample_h))


SPECS["hv_manual"] = [
    ("main unit", "315 x 671 x 595 mm, 43 kg", "Mitutoyo catalogue section K, HM-210/220 (via byu-vcl "
     "instruments_r7.SOURCES['hardness'])"),
    ("test force", "HM-220: 0.4903 mN - 19.61 N (0.05 gf - 2 kgf)", "Mitutoyo catalogue section K"),
    ("Type D", "motorized XY stage 50 x 50 mm, table 130 x 130 mm, 25 mm/s; motorized focus 1.4 mm; AVPAK; 3 MP camera",
     "Mitutoyo catalogue section K"),
    ("stage lowered to load", "30 mm on the elevating screw", "estimate (the screw's handwheel at the left)"),
    ("PC, monitor, joystick", "beside the unit", "estimate, as byu-vcl's"),
]


# ===================================================================================================== registry
REGISTRY = {"aging_rack": aging_rack, "tongs": tongs, "quench_bath": quench_bath, "hv_manual": hv_manual,
            "furnace_hinged": furnace_hinged}
