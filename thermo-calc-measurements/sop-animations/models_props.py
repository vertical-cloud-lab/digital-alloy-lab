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


def tc_reader() -> Model:
    """A handheld type K thermocouple reader, 75 x 32 x 150 mm, on its tilt stand; the display faces -y."""
    m = Model("p4_tc_reader", "Thermocouple reader")
    m.add("case", rbox(75, 32, 150, 8).edges(">Z").fillet(5), "p4_yellow")
    m.add("lcd", box(-28, -16.6, 92, 28, -16.0, 132), "p4_lcd")
    for i, x in enumerate((-18, 0, 18)):
        m.add(f"key {i}", _ycyl(10, 2.0, x=x, y=-16.0, z=60), "p4_dark")
    m.add("socket", box(-12, -6, 150, 12, 6, 158), "p4_dark")
    return m


def thermometer() -> Model:
    """A digital room thermometer / hygrometer, 100 x 25 x 100 mm, on its stand; the display faces -y."""
    m = Model("p4_thermometer", "Room thermometer")
    m.add("case", rbox(100, 22, 100, 8).edges(">Z").fillet(6), "p4_white")
    m.add("lcd", box(-42, -11.6, 26, 42, -11.0, 88), "p4_lcd")
    m.add("stand", box(-40, 8, 0, 40, 30, 3), "p4_white")
    return m


def tweezers() -> Model:
    """Straight lab tweezers, 120 mm: the tips at the origin, the handle towards +x."""
    m = Model("p4_tweezers", "Tweezers, 120 mm")
    for s_ in (-1, 1):
        blade = (cq.Workplane("XY").polyline([(0, 0.2 * s_), (0, 1.2 * s_), (118, 4.5 * s_), (118, 1.0 * s_)]).close()
                 .extrude(1.0).translate((0, 0, -0.5)))
        m.add(f"blade {s_}", blade, "p4_steel")
    m.add("hinge", box(110, -4.5, -0.6, 120, 4.5, 0.6), "p4_steel")
    return m


def lfa_disc(coated: bool = False) -> Model:
    """A laser-flash disc, 12.7 mm x 2.5 mm (NETZSCH's reference size), bare or sprayed with graphite."""
    m = Model("p4_disc", "LFA disc 12.7 x 2.5 mm")
    m.add("disc", cyl(12.7, 2.5), "p4_graphite" if coated else "p4_coupon")
    return m


def spray_can() -> Model:
    """A 400 mL aerosol can of graphite spray, 65 x 200 mm."""
    m = Model("p4_spray", "Graphite spray")
    m.add("can", cyl(65, 170).edges(">Z").fillet(8), "p4_black")
    m.add("shoulder", cq.Workplane("XY").circle(31).workplane(offset=18).circle(14).loft().translate((0, 0, 170)),
          "p4_grey")
    m.add("cap", cyl(18, 12, z=188), "p4_white")
    m.add("label", tube(65.4, 64.6, 70, z=50), "p4_white")
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
    base = rbox(w, d, p["base_h"], 24).edges(">Z").fillet(10).cut(cyl(96, p["base_h"] + 2, x=ax, y=ay, z=-1))
    body.add("base", base, "p4_mitu")
    body.add("base panel", box(-110, -d / 2 - 1, 40, 110, -d / 2, 110), "p4_mitu_dk")
    body.add("screw collar", tube(110, 96, 6, x=ax, y=ay, z=p["base_h"]), "p4_mitu_dk")
    body.add("column", rbox(200, 255, h - 35 - p["base_h"], 30, y=d / 2 - 127.5, z=p["base_h"]), "p4_mitu")
    body.add("head", rbox(230, 586, 180, 30, y=d / 2 - 293, z=380).edges(">Z").fillet(14), "p4_mitu")
    body.add("head band", box(-116, -251, 470, 116, d / 2 - 30, 480), "p4_mitu_dk")
    body.add("camera", rbox(50, 60, 35, 8, x=ax, y=ay, z=560), "p4_mitu_dk")
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
    sz.add("elevating screw", cyl(90, 120, x=ax, y=ay, z=p["base_h"] - 60), "p4_mitu_dk")
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



# ===================================================================================================== eddy current
# Foerster SIGMATEST 2.070, a handheld eddy-current conductivity meter (README section 5.1). Foerster's datasheet:
# 211 x 102 x 40 mm (H x W x D), 0.62 kg; 60/120/240/480/960 kHz; 0.5-65 MS/m (1-112 %IACS); +-0.7 % of reading
# (60 kHz, 14 mm probe); lift-off compensation to 750 um; readings normalised to 20 C from the probe's own temperature
# sensor; probes with 5, 8 and 14 mm heads. The look and the proportions in between (the waisted bumper, the screen,
# the F1-F4 row, the navigation block round the F key, the 4 x 3 number block, the connector block at the top end) are
# read off Foerster's "SIGMATEST Unpacking and Setup" video (youtu.be/l8calAolJpM, 4:32-4:38, top down) and fitted
# with register.py (refs/eddy_meter/). Frame: the meter lying face up, its display end towards +y.
EDDY = dict(W=102.0, L=211.0, T=40.0, taper=7.0, waist_hw=40.9, waist_y=-18.6, bot_hw=50.0, face_hw=36.0, face_t=3.0,
            bez_w=69.0, bez_h=78.0, bez_y=61.0, scr_w=57.1, scr_h=73.7, scr_y=56.4, key_px=14.5, f_row_y=6.4,
            nav_y=-23.8, num_y0=-53.0, num_dy=15.2, conn_w=60.0, conn_x=4.3, conn_l=12.0, probe_head=8.0)


def _eddy_hw(p, y):
    """The bumper's half-width at y (the waisted outline)."""
    top, w, b = p["W"] / 2, p["waist_hw"], p["bot_hw"]
    y0 = p["waist_y"]
    if y >= y0 + 40:
        return top
    if y >= y0 + 6:
        t = (y - (y0 + 6)) / 34.0
        return w + (top - w) * (0.5 - 0.5 * math.cos(math.pi * t))
    if y >= y0 - 6:
        return w
    if y >= y0 - 60:
        t = ((y0 - 6) - y) / 54.0
        return w + (b - w) * (0.5 - 0.5 * math.cos(math.pi * t))
    return b


def _eddy_outline(p, r=12.0, n=60):
    L = p["L"]
    pts = []
    ys = np.linspace(L / 2 - r, -L / 2 + r, n)
    for y in ys:                                          # right side, top to bottom
        pts.append((_eddy_hw(p, y), y))
    hb = _eddy_hw(p, -L / 2 + r)
    for a in np.linspace(0, -90, 7)[1:]:                  # bottom right corner
        t = math.radians(a)
        pts.append((hb - r + r * math.cos(t), -L / 2 + r + r * math.sin(t)))
    for a in np.linspace(-90, -180, 7)[1:]:               # bottom left
        t = math.radians(a)
        pts.append((-hb + r + r * math.cos(t), -L / 2 + r + r * math.sin(t)))
    for y in ys[::-1][1:]:                                # left side, bottom to top
        pts.append((-_eddy_hw(p, y), y))
    ht = _eddy_hw(p, L / 2 - r)
    for a in np.linspace(180, 90, 7)[1:]:                 # top left
        t = math.radians(a)
        pts.append((-ht + r + r * math.cos(t), L / 2 - r + r * math.sin(t)))
    for a in np.linspace(90, 0, 7)[1:-1]:                 # top right
        t = math.radians(a)
        pts.append((ht - r + r * math.cos(t), L / 2 - r + r * math.sin(t)))
    return pts


def _eddy_keys(p):
    """(name, x, y, w, h) of every key, in the meter's frame."""
    k = p["key_px"]
    keys = [(f"F{i + 1}", (i - 1.5) * k, p["f_row_y"], 9.0, 8.0) for i in range(4)]
    ny = p["nav_y"]
    keys += [("home", -1.5 * k, ny + 14.0, 9.0, 8.0), ("power", 1.5 * k, ny + 14.0, 9.0, 8.0),
             ("up", 0.0, ny + 13.0, 9.0, 7.0), ("left", -1.0 * k, ny, 8.0, 9.0), ("F", 0.0, ny, 11.0, 10.0),
             ("right", 1.0 * k, ny, 8.0, 9.0), ("help", -1.5 * k, ny - 14.0, 9.0, 8.0),
             ("down", 0.0, ny - 13.0, 9.0, 7.0), ("lamp", 1.5 * k, ny - 14.0, 9.0, 8.0)]
    labels = ("1 2 3 0", "4 5 6 -", "7 8 9 .")
    for r_, row in enumerate(labels):
        for c_, lab in enumerate(row.split()):
            keys.append((f"key {lab}", (c_ - 1.5) * k * 1.03, p["num_y0"] - r_ * p["num_dy"], 9.0, 8.0))
    return keys


def eddy_anchors(p, pose=None) -> dict:
    L, T = p["L"], p["T"]
    zf = T
    a = {}
    for nm, sx, sy in (("tl", -1, 1), ("tr", 1, 1), ("bl", -1, -1), ("br", 1, -1)):
        a[f"screen {nm}"] = (sx * p["scr_w"] / 2, p["scr_y"] + sy * p["scr_h"] / 2, zf + 0.6)
        a[f"bezel {nm}"] = (sx * p["bez_w"] / 2, p["bez_y"] + sy * p["bez_h"] / 2, zf + 0.4)
    for name, x, y, w, h in _eddy_keys(p):
        a[name if name.startswith("key") else f"key {name}"] = (x, y, zf + 1.5)
    a["waist left"] = (-p["waist_hw"], p["waist_y"], T - 3)
    a["waist right"] = (p["waist_hw"], p["waist_y"], T - 3)
    a["top edge"] = ("line", (-p["W"] / 2 + 14, L / 2, T - 3), (p["W"] / 2 - 14, L / 2, T - 3))
    a["bottom edge"] = ("line", (-p["bot_hw"] + 14, -L / 2, T - 3), (p["bot_hw"] - 14, -L / 2, T - 3))
    a["left side top"] = ("line", (-p["W"] / 2, L / 2 - 14, T - 3), (-p["W"] / 2, p["waist_y"] + 42, T - 3))
    a["right side top"] = ("line", (p["W"] / 2, L / 2 - 14, T - 3), (p["W"] / 2, p["waist_y"] + 42, T - 3))
    a["left side bottom"] = ("line", (-p["bot_hw"], -L / 2 + 14, T - 3), (-p["bot_hw"], p["waist_y"] - 62, T - 3))
    a["right side bottom"] = ("line", (p["bot_hw"], -L / 2 + 14, T - 3), (p["bot_hw"], p["waist_y"] - 62, T - 3))
    a["bottom left base"] = (-p["bot_hw"] + 4, -L / 2 + 4, 0.0)
    a["bottom right base"] = (p["bot_hw"] - 4, -L / 2 + 4, 0.0)
    a["connector"] = (p["conn_x"] + p["conn_w"] / 2 - 12, L / 2 + p["conn_l"], T / 2)
    return a


def probe_model(head: float = 8.0, mat_body: str = "p4_black") -> list:
    """The pencil probe's parts [(name, Workplane, material)], its measuring face at the origin, axis +z: a steel
    head `head` mm across, a ribbed black grip 19 mm across, a strain relief, as in Foerster's video (the 14 mm head)."""
    parts = [("probe head", cyl(head, 3.0).union(cq.Workplane("XY").circle(head / 2).workplane(offset=9.0)
                                                    .circle(8.0).loft().translate((0, 0, 3.0))), "p4_steel"),
             ("probe grip", cyl(19.0, 62.0, z=12.0), mat_body)]
    for i in range(6):
        parts.append((f"probe rib {i}", tube(20.5, 18.0, 3.0, z=30.0 + 7.0 * i), mat_body))
    relief = cq.Workplane("XY").circle(6.0).workplane(offset=24.0).circle(3.5).loft().translate((0, 0, 74.0))
    parts.append(("probe relief", relief, mat_body))
    return parts


PROBE_LEN = 98.0           # the probe's measuring face to the end of its strain relief


def eddy_meter() -> Instrument:
    p = EDDY
    L, T = p["L"], p["T"]
    inst = Instrument("eddy_meter", "Eddy-current conductivity meter", "Foerster SIGMATEST 2.070",
                      (p["W"], L, T), "Foerster datasheet (211 x 102 x 40 mm, 0.62 kg); the look from Foerster's "
                      "setup video, fitted with register.py")
    body = _piece(inst, "body")
    outline = _eddy_outline(p)
    # the bumper tapers towards the back (the three-quarter photo's silhouette): the back outline inset `taper` mm
    k = (p["W"] / 2 - p["taper"]) / (p["W"] / 2)
    back = [(x * k, y * (L / 2 - p["taper"] / 2) / (L / 2)) for x, y in outline]
    shell = (cq.Workplane("XY").polyline(back).close().workplane(offset=T - p["face_t"]).polyline(outline).close()
             .loft(ruled=True))
    body.add("bumper", shell, "p4_dark")
    fw = 2 * p["face_hw"]
    face = rbox(fw, L - 12.0, p["face_t"] + 0.01, 8.0, y=2.0, z=T - p["face_t"])
    body.add("face", face, "p4_light")
    body.add("display window", box(-p["bez_w"] / 2, p["bez_y"] - p["bez_h"] / 2, T, p["bez_w"] / 2,
                                   p["bez_y"] + p["bez_h"] / 2, T + 0.4), "p4_offwhite")
    body.add("screen", box(-p["scr_w"] / 2, p["scr_y"] - p["scr_h"] / 2, T + 0.4, p["scr_w"] / 2,
                           p["scr_y"] + p["scr_h"] / 2, T + 0.6), "p4_screen_ui")
    keys = None
    for name, x, y, w, h in _eddy_keys(p):
        k = rbox(w, h, 1.5, 1.5, x=x, y=y, z=T)
        keys = k if keys is None else keys.union(k)
    body.add("keys", keys, "p4_grey")
    cx = p["conn_x"]
    body.add("connector block", box(cx - p["conn_w"] / 2, L / 2 - 2, 8.0, cx + p["conn_w"] / 2, L / 2 + p["conn_l"],
                                    T - 8.0), "p4_dark")
    lx = cx + p["conn_w"] / 2 - 12
    body.add("LEMO socket", _ycyl(11.0, 9.0, x=lx, y=L / 2 + p["conn_l"], z=T / 2), "p4_steel")
    body.add("SD and RJ45", box(cx - p["conn_w"] / 2 + 6, L / 2 + p["conn_l"] - 0.5, 14, cx + 4, L / 2 + p["conn_l"]
                                + 0.3, T - 14), "p4_black")
    # the probe, on its own piece: placed by the scene (its face at the piece's origin, axis +z)
    pr = _piece(inst, "probe")
    for name, w, mat in probe_model(p["probe_head"]):
        pr.add(name, w, mat)
    # the standards: a black carrier with two discs, as in Foerster's photo; values to bracket 25-60 %IACS
    st = _piece(inst, "standards")
    car = cq.Workplane("XY").slot2D(96.0, 48.0).extrude(10.0)
    car = car.cut(cyl(33.0, 4.0, x=-23.0, z=7.0)).cut(cyl(33.0, 4.0, x=23.0, z=7.0))
    st.add("carrier", car, "p4_black")
    st.add("standard low", cyl(32.0, 3.0, x=-23.0, z=7.0), "p4_brass")
    st.add("standard high", cyl(32.0, 3.0, x=23.0, z=7.0), "p4_coupon_6063")
    inst.anchors = eddy_anchors(p)
    inst.props = ("probe", "standards")
    return inst


def eddy_lemo(p=None):
    p = p or EDDY
    return (p["conn_x"] + p["conn_w"] / 2 - 12, p["L"] / 2 + p["conn_l"] + 9.0, p["T"] / 2)


ANCHORS["eddy_meter"] = (EDDY, eddy_anchors)
FREE["eddy_meter"] = ["waist_hw", "waist_y", "bot_hw", "bez_w", "bez_h", "bez_y", "scr_w", "scr_h", "scr_y",
                      "key_px", "f_row_y", "nav_y", "num_y0", "num_dy"]
CHECKS["eddy_meter"] = lambda p: [p["W"] / 2 - p["waist_hw"] - 3, p["face_hw"] - p["bez_w"] / 2, p["bez_w"] - p["scr_w"],
                                  p["bez_h"] - p["scr_h"], p["L"] / 2 - (p["bez_y"] + p["bez_h"] / 2) - 3,
                                  p["bez_y"] - p["bez_h"] / 2 - p["f_row_y"] - 5]
SPECS["eddy_meter"] = [
    ("housing", "211 x 102 x 40 mm (H x W x D), 0.62 kg", "Foerster SIGMATEST datasheet, "
     "https://www.foerstergroup.com/web2print/en/mobile-testing/SIGMATEST.pdf p.3"),
    ("display", "LCD 240 x 320 px; window about 69 x 78 mm, active about 54 x 65 mm", "datasheet p.3 (pixels); mm "
     "measured off youtu.be/l8calAolJpM at 4:32-4:38 with the 102 mm width as the scale (estimate, then fitted)"),
    ("frequencies", "60 / 120 / 240 / 480 / 960 kHz", "datasheet p.3"),
    ("range", "0.5-65 MS/m (1-112 %IACS)", "datasheet p.3"),
    ("accuracy", "+-0.7 % of reading at 60 kHz with the 14 mm probe; resolution 0.1 %", "datasheet p.3"),
    ("lift-off compensation", "automatic, to 750 um", "datasheet p.2-3"),
    ("temperature", "normalised to 20 C from the probe's built-in sensor (or an external one)", "datasheet p.1"),
    ("probes", "heads 5, 8 and 14 mm; the 14 mm shielded probe reads a 14 mm bar's end face", "Foerster SIGMATEST "
     "PROBES sheet p.1-2; SIGMATEST 2.069 manual p.65 (bergeng.com)"),
    ("minimum thickness", "3 delta, delta [mm] = 503 / sqrt(sigma [MS/m] f [Hz])", "SIGMATEST 2.069 manual p.62"),
    ("probe body", "19 mm grip, ~98 mm long, ribbed, black", "estimate from the video (4:32-4:38, 2:08)"),
    ("standards", "two discs in a black stadium-shaped carrier (Foerster: NPL-traceable); disc size 32 mm estimated",
     "Foerster REFERENCE STANDARD CONDUCTIVITY sheet p.1 (photo); values chosen to bracket 25-60 %IACS"),
]



# ===================================================================================================== laser flash
# NETZSCH LFA 717 HyperFlash (successor of the LFA 467; README section 5.1), drawn as at the contract lab. NETZSCH's
# specification sheet: -100 to 500 C (LN2 cooling to -100 C); xenon flash lamp, up to 10 J a pulse, 10-1500 us; InSb
# or MCT detector, LN2-cooled; sample changer of 4 holders x 4 samples (16 x 12.7 mm round or 10 mm square, or 4 x
# 25.4 mm); samples 0.01-6 mm thick; vertical layout, the flash at the bottom, the sample in the middle, the detector
# on top (LFA 467 brochure p.4). NETZSCH publishes no external dimensions: the width (620 mm) is an estimate from the
# operator beside a HyperFlash in NETZSCH's e-learning video (youtu.be/vkHcL_8jTZE, 1:35), and the proportions are read
# off NETZSCH's LFA 717 product video (youtu.be/vxowKxtTS0A, 0:06 front, 0:52 three-quarter), then fitted with
# register.py (refs/laser_flash/). Look: a white box on a dark grey plinth, a dark front panel with the touch display
# wrapping over the front edge, teal light strips along the top edges, the detector's white tower with a grey collar
# left of centre on top, a block behind it; the loading opening in the top cover in front of the tower.
LFA = dict(W=620.0, D=626.1, base_h=349.0, plinth_h=49.9, panel_w=296.4, panel_h=134.7, panel_x=0.0,
           disp_w=175.0, disp_h=50.0, tower_d=147.6, tower_h=191.1, collar_d=148.0, collar_h=36.5, tower_x=-99.4,
           tower_y=40.0, block_w=222.2, block_h=139.7, block_d=150.0, open_w=160.0, open_d=120.0, open_y=-150.0)


def lfa_anchors(p, pose=None) -> dict:
    W, D, H = p["W"], p["D"], p["base_h"]
    yf = -D / 2
    a = {"base front top left": (-W / 2, yf, H), "base front top right": (W / 2, yf, H),
         "plinth front left": (-W / 2 + 8, yf + 8, p["plinth_h"]), "plinth front right": (W / 2 - 8, yf + 8, p["plinth_h"]),
         "panel bottom left": (p["panel_x"] - p["panel_w"] / 2 + 12, yf - 10, H - p["panel_h"]),
         "panel bottom right": (p["panel_x"] + p["panel_w"] / 2 - 12, yf - 10, H - p["panel_h"]),
         "display tl": (p["panel_x"] - p["disp_w"] / 2, yf - 12, H - 14), "display tr": (p["panel_x"] + p["disp_w"] / 2,
                                                                                       yf - 12, H - 14),
         "display bl": (p["panel_x"] - p["disp_w"] / 2, yf - 12, H - 14 - p["disp_h"]),
         "display br": (p["panel_x"] + p["disp_w"] / 2, yf - 12, H - 14 - p["disp_h"]),
         "tower top": ("circle", (p["tower_x"], p["tower_y"], H + p["collar_h"] + p["tower_h"]), p["tower_d"] / 2),
         "collar top": ("circle", (p["tower_x"], p["tower_y"], H + p["collar_h"]), p["collar_d"] / 2),
         "block top left": (p["tower_x"] - p["block_w"] / 2, p["tower_y"] - p["block_d"] / 2 + 40, H + p["block_h"]),
         "block top right": (p["tower_x"] + p["block_w"] / 2, p["tower_y"] - p["block_d"] / 2 + 40, H + p["block_h"]),
         "left side": ("line", (-W / 2, yf, H - 40), (-W / 2, yf, p["plinth_h"] + 30)),
         "right side": ("line", (W / 2, yf, H - 40), (W / 2, yf, p["plinth_h"] + 30)),
         "top back left": (-W / 2, D / 2, H)}
    return a


def laser_flash() -> Instrument:
    p = LFA
    W, D, H = p["W"], p["D"], p["base_h"]
    yf = -D / 2
    inst = Instrument("laser_flash", "Flash thermal diffusivity analyser (contract lab)", "NETZSCH LFA 717 HyperFlash",
                      (W, D, round(H + p["collar_h"] + p["tower_h"])),
                      "NETZSCH LFA 717 specification sheet (ranges, changer); dimensions not published: estimated "
                      "from NETZSCH's videos and fitted with register.py")
    body = _piece(inst, "body")
    ph = p["plinth_h"]
    body.add("feet", cyl(30, 12, x=-W / 2 + 50, y=yf + 50).union(cyl(30, 12, x=W / 2 - 50, y=yf + 50))
             .union(cyl(30, 12, x=-W / 2 + 50, y=D / 2 - 50)).union(cyl(30, 12, x=W / 2 - 50, y=D / 2 - 50)),
             "p4_black")
    body.add("plinth", box(-W / 2 + 6, yf + 6, 12, W / 2 - 6, D / 2 - 6, ph), "p4_dark")
    ox, oy, ow, od = p["tower_x"], p["open_y"], p["open_w"], p["open_d"]
    shell = box(-W / 2, yf, ph, W / 2, D / 2, H).edges("|Z").fillet(8)
    shell = shell.cut(box(ox - ow / 2, oy - od / 2, H - 70, ox + ow / 2, oy + od / 2, H + 1))   # the loading well
    zc0 = H - 58.0
    shell = shell.cut(box(ox - 76, oy - 56, zc0 - 9, ox + 76, p["tower_y"] + 62, zc0 + 13))      # the changer's run
    body.add("housing", shell, "p4_white")
    body.add("top cover", box(-W / 2 + 4, yf + 4, H, W / 2 - 4, D / 2 - 4, H + 2).cut(
        box(ox - ow / 2, oy - od / 2, H - 1, ox + ow / 2, oy + od / 2, H + 3)), "p4_light")
    for sx in (-1, 1):                                    # the teal light strips along the top front edges
        x0 = p["panel_x"] + sx * (p["panel_w"] / 2 + 8)
        x1 = sx * (W / 2 - 6)
        xa, xb = sorted((x0, x1))
        body.add(f"light strip {sx}", box(xa, yf - 1.5, H - 12, xb, yf + 0.5, H - 4), "p4_netzsch_green")
    pw, pnh = p["panel_w"], p["panel_h"]
    panel = (cq.Workplane("YZ").polyline([(yf - 14, H - pnh), (yf + 2, H - pnh), (yf + 2, H + 2), (yf + 40, H + 2),
                                          (yf + 40, H + 6), (yf - 6, H + 6), (yf - 14, H - 10)]).close()
             .extrude(pw).translate((p["panel_x"] - pw / 2, 0, 0)))
    body.add("front panel", panel, "p4_netzsch_dk")
    dw, dh = p["disp_w"], p["disp_h"]
    disp = box(-dw / 2, -1.0, -dh, dw / 2, 0.0, 0.0).rotate((0, 0, 0), (1, 0, 0), -6.0).translate(
        (p["panel_x"], yf - 12.6, H - 14))
    body.add("display", disp, "p4_screen")
    tx, ty = p["tower_x"], p["tower_y"]
    body.add("rear block", box(tx - p["block_w"] / 2, ty - p["block_d"] / 2 + 40, H, tx + p["block_w"] / 2,
                               ty + p["block_d"] / 2 + 40, H + p["block_h"]).edges("|Z").fillet(10), "p4_offwhite")
    body.add("detector collar", cyl(p["collar_d"], p["collar_h"], x=tx, y=ty, z=H), "p4_grey")
    body.add("detector tower", cyl(p["tower_d"], p["tower_h"] - 8, x=tx, y=ty, z=H + p["collar_h"])
             .edges(">Z").fillet(6), "p4_white")
    body.add("dewar cap", cyl(36, 14, x=tx, y=ty, z=H + p["collar_h"] + p["tower_h"] - 8), "p4_steel")
    # the loading lid over the well, hinged at its back edge
    lid = _piece(inst, "lid")
    lid.add("lid", box(ox - ow / 2 - 6, oy - od / 2 - 6, H + 2, ox + ow / 2 + 6, oy + od / 2 + 6, H + 12)
            .edges("|Z").fillet(6), "p4_light")
    lid.add("lid knob", cyl(26, 14, x=ox, y=oy - od / 2 + 12, z=H + 12), "p4_black")
    # the sample changer in the well: a plate with four holders, four sample places each (12.7 mm)
    ch = _piece(inst, "changer")
    zc = H - 58.0
    ch.add("holder plate", box(ox - 70, oy - 52, zc - 6, ox + 70, oy + 52, zc), "p4_steel")
    for i, (hx, hy) in enumerate(((-33, -24), (33, -24), (-33, 24), (33, 24))):
        holder = cyl(54, 8, x=ox + hx, y=oy + hy, z=zc)
        for k, (sx_, sy_) in enumerate(((-11, -11), (11, -11), (-11, 11), (11, 11))):
            holder = holder.cut(cyl(13.4, 6, x=ox + hx + sx_, y=oy + hy + sy_, z=zc + 3)).cut(
                cyl(9.0, 10, x=ox + hx + sx_, y=oy + hy + sy_, z=zc - 1))
        ch.add(f"holder {i + 1}", holder, "p4_sic")
    # inside, for the cutaway: the flash lamp under the measuring place, the furnace round it, the detector above
    ins = _piece(inst, "internals")
    mx, my = ox, p["tower_y"]                             # the measuring place: under the detector
    ins.add("xenon lamp housing", cyl(96, 70, x=mx, y=my, z=ph + 20), "p4_grey")
    ins.add("reflector", cq.Workplane("XY").circle(40).workplane(offset=30).circle(18).loft()
            .translate((mx, my, ph + 90)), "p4_steel")
    ins.add("xenon lamp", cyl(14, 22, x=mx, y=my, z=ph + 96), "p4_glow_lamp")
    ins.add("light guide", cyl(16, zc - 6 - (ph + 120) - 8, x=mx, y=my, z=ph + 120), "p4_glass")
    ins.add("furnace", tube(130, 104, 50, x=mx, y=my, z=zc - 30), "p4_hot")
    ins.add("optics", cq.Workplane("XY").circle(10).workplane(offset=H + 30 - (zc + 10)).circle(28).loft()
            .translate((mx, my, zc + 10)), "p4_glass")
    ins.add("IR detector", cyl(40, 50, x=mx, y=my, z=H + 30), "p4_dark")
    ins.add("detector dewar", cyl(100, 110, x=tx, y=ty, z=H + p["collar_h"] + 20), "p4_steel")
    inst.joints = {"lid": Joint("hinge", axis=(1, 0, 0), pivot=(0, oy + od / 2 + 6, H + 12), deg=-105.0),
                   "changer": Joint("slide", vec=(0, 1.0, 0)),          # v in mm back, to the detector
                   "internals": Joint("fade")}
    inst.anchors = lfa_anchors(p)
    inst.props = ("internals",)
    return inst


def lfa_measure_xy(p=None):
    """(x, y) of the well (loading) and how far the changer runs back to the measuring place."""
    p = p or LFA
    return (p["tower_x"], p["open_y"]), p["tower_y"] - p["open_y"]


ANCHORS["laser_flash"] = (LFA, lfa_anchors)
FREE["laser_flash"] = ["D", "base_h", "plinth_h", "panel_w", "panel_h", "disp_w", "disp_h", "tower_d", "tower_h",
                       "collar_h", "tower_x", "block_w", "block_h"]
CHECKS["laser_flash"] = lambda p: [p["W"] / 2 - p["panel_w"] / 2 - 40, p["panel_w"] - p["disp_w"] - 10,
                                   p["base_h"] - p["panel_h"] - 60, p["block_w"] - p["tower_d"],
                                   p["W"] / 2 - abs(p["tower_x"]) - p["block_w"] / 2]
SPECS["laser_flash"] = [
    ("temperature", "-100 to 500 C (LN2 to -100 C, compressed air to 0 C); HT version RT-1250 C",
     "NETZSCH Technical Specifications LFA 717 HyperFlash Series (analyzing-testing.netzsch.com, PDF)"),
    ("flash", "xenon lamp, up to 10 J a pulse, 10-1500 us", "same sheet; LFA 467 sheet"),
    ("detector", "InSb (RT-500 C) or MCT (-100 to 500 C), LN2-cooled", "same sheet; LFA 467 brochure p.12"),
    ("sample changer", "4 holders x 4 samples: 16 x 12.7 mm round or 10 mm square; or 4 x 25.4 mm", "same sheet"),
    ("sample thickness", "0.01-6 mm; NETZSCH reference discs 12.7 x 2.5, 10 x 2.0 mm (diameter/thickness > 5)",
     "NETZSCH Accessories LFA brochure p.8, p.46-47"),
    ("layout", "flash at the bottom, sample in the middle, detector on top", "LFA 467 HyperFlash brochure p.4"),
    ("coating", "graphite spray, both faces, thin (about 5 um); too thick biases Al and Cu low",
     "NETZSCH tips: 'When and how must samples be coated during LFA measurements'"),
    ("width", "620 mm (estimate)", "the operator beside a HyperFlash in youtu.be/vkHcL_8jTZE at 1:35 (estimate)"),
    ("proportions", "base 287 mm, tower 131 x 171 mm on a 40 mm collar, panel 232 mm wide (estimates, fitted)",
     "NETZSCH LFA 717 video youtu.be/vxowKxtTS0A at 0:06 and 0:52"),
]


# ===================================================================================================== registry
REGISTRY = {"aging_rack": aging_rack, "tongs": tongs, "quench_bath": quench_bath, "hv_manual": hv_manual,
            "furnace_hinged": furnace_hinged, "eddy_meter": eddy_meter, "laser_flash": laser_flash}
