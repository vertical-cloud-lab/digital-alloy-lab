"""Models for SOP 01 (DSC melting and freezing of atomized powder, #262): the micro riffle splitter, the microbalance,
the high-temperature STA/DSC, and the small things handled at them (alumina crucibles and lids, tweezers, a
micro-spatula, the pure-metal calibration standards, an ethanol wash bottle).

Same pattern as byu-vcl's ``vl/instruments.py``: each model is an ``Instrument`` of named pieces (CadQuery solids with
materials; ``body`` stays put) and a ``Joint`` per moving piece, sized from the maker's published dimensions (``SPECS``
gives the source of every figure and marks the estimates). ``REGISTRY`` is what ``stage.get(key)`` builds;
``ANCHORS``/``FREE``/``CHECKS`` are what ``fit.py`` (register.py) fits to frames of the real machines.

Frame: x to the right and y away from you when you face the front, z up from the bench, origin at the centre of the
footprint, millimetres.
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

from common import Model, box, cyl, rbox, tube  # noqa: E402
from instruments import Instrument, Joint, _piece  # noqa: E402

# name: (r, g, b, opacity, shininess 0-1)
MATERIALS = {
    "dsc_stainless": (0.74, 0.75, 0.77, 1.0, 0.70),        # brushed stainless sheet
    "dsc_stainless_dk": (0.55, 0.56, 0.58, 1.0, 0.60),     # stainless in shadow / anodized aluminium chute plates
    "dsc_al_powder": (0.58, 0.59, 0.61, 1.0, 0.05),        # grey Al-alloy powder (20-63 um), matte
    "dsc_alumina": (0.95, 0.94, 0.90, 1.0, 0.15),           # sintered alumina (crucibles, carrier tube)
    "dsc_white": (0.93, 0.93, 0.92, 1.0, 0.20),             # instrument white
    "dsc_lightgrey": (0.80, 0.81, 0.82, 1.0, 0.25),
    "dsc_grey": (0.56, 0.58, 0.60, 1.0, 0.30),
    "dsc_dark": (0.20, 0.21, 0.23, 1.0, 0.30),
    "dsc_black": (0.08, 0.08, 0.09, 1.0, 0.30),
    "dsc_blue": (0.10, 0.30, 0.58, 1.0, 0.30),
    "dsc_glass": (0.80, 0.88, 0.93, 0.25, 0.90),            # draft-shield glass
    "dsc_screen": (0.10, 0.16, 0.24, 1.0, 0.60),
    "dsc_screen_ui": (0.55, 0.72, 0.86, 1.0, 0.10),
    "dsc_pt": (0.86, 0.86, 0.84, 1.0, 0.85),                # platinum (sensor discs, thermocouple wires)
    "dsc_brass": (0.80, 0.64, 0.30, 1.0, 0.60),
    "dsc_cyl_grey": (0.40, 0.43, 0.46, 1.0, 0.40),          # gas cylinder (argon: grey body, colours vary by country)
    "dsc_cyl_green": (0.18, 0.42, 0.30, 1.0, 0.40),         # argon shoulder band (EN 1089-3: dark green)
    "dsc_hot": (0.92, 0.38, 0.10, 1.0, 0.10),               # dull orange: a hot furnace inside, a glowing melt
    "dsc_ethanol_bottle": (0.95, 0.95, 0.93, 0.80, 0.20),  # LDPE wash bottle
    "dsc_ethanol_cap": (0.15, 0.45, 0.80, 1.0, 0.25),
    "dsc_indium": (0.72, 0.73, 0.76, 1.0, 0.60),
    "dsc_zinc": (0.66, 0.68, 0.70, 1.0, 0.55),
    "dsc_gold": (0.85, 0.68, 0.28, 1.0, 0.80),
    "dsc_silver": (0.84, 0.84, 0.86, 1.0, 0.85),
    "dsc_bead": (0.78, 0.79, 0.81, 1.0, 0.80),              # the solidified bead
    "dsc_paper": (0.97, 0.97, 0.95, 1.0, 0.02),
    "dsc_steel_chain": (0.45, 0.46, 0.48, 1.0, 0.60),
    "dsc_blue_navy": (0.10, 0.17, 0.27, 1.0, 0.35),          # the F5's navy panel and badge
    "dsc_teal": (0.05, 0.52, 0.53, 1.0, 0.30),               # its teal band
    "dsc_copper": (0.72, 0.45, 0.30, 1.0, 0.60),             # the sensor flange
    "dsc_green": (0.20, 0.55, 0.42, 1.0, 0.30),              # the solenoid valves
    "dsc_glassy": (0.78, 0.82, 0.84, 0.70, 0.80),            # the furnace's top gas fitting (glass and metal)
}

SPECS: dict = {}
ANCHORS: dict = {}
FREE: dict = {}
CHECKS: dict = {}


def _loft_rect(w0, d0, z0, w1, d1, z1, x=0.0, y=0.0) -> cq.Workplane:
    """A solid between a w0 x d0 rectangle at z0 and a w1 x d1 rectangle at z1 (centred on x, y)."""
    return (cq.Workplane("XY").workplane(offset=z0).rect(w0, d0).workplane(offset=z1 - z0).rect(w1, d1).loft(ruled=True)
            .translate((x, y, 0)))


# ============================================================================================ micro riffle splitter
# Humboldt H-3971C Micro Riffle Splitter (Jones type, for ASTM B215 powder sampling): 16 chutes 0.125 in (3.2 mm)
# wide; hopper 4.5 x 4.5 in (114 x 114 mm); a stainless hopper, a stainless and anodized-aluminium riffle bank and a
# stainless frame; two stainless "Hy-Back" (notched L-shape) pans (humboldtmfg.com/microriffle--splitter.html, read
# 2026-11-28). Humboldt publishes no overall size; its look and proportions are taken from Gilson's photos of the
# same design (SP-171/SP-171X Jones micro splitter, 14 x 1/8 in chutes, 1.8 kg shipping weight, ASTM B215:
# globalgilson.com/jones-micro-splitters): a square funnel hopper on top, the riffle bank between two bolted upright
# plates with feet, a pan each side under the chutes, the pans' backs higher than their fronts. Heights and pan sizes
# are scaled from those photos (overall height about 1.3 x the hopper's width) and are estimates.
RIFFLE = dict(hopper=114.0, hopper_h=38.0, slot_w=20.0, n=16, chute=3.2, wall=0.8, bank_w=40.0, bank_z0=56.0,
              bank_z1=112.0, plate_w=28.0, plate_t=2.0, foot=20.0, pan_x0=21.0, pan_x1=55.0, pan_d=84.0, pan_h=40.0,
              pan_back=88.0, sheet=0.8)
SPECS["riffle_splitter"] = {
    "model": "Humboldt H-3971C Micro Riffle Splitter (Jones type)",
    "chutes": "16 x 0.125 in (3.2 mm): humboldtmfg.com/microriffle--splitter.html",
    "hopper": "4.5 x 4.5 in (114 x 114 mm): same page",
    "pans": "2, stainless 'Hy-Back' (notched L-shape): same page",
    "standard": "ASTM B215 (sampling metal powders): Gilson SP-171 page, globalgilson.com/jones-micro-splitters",
    "look": "Gilson SP-171X product photos (same design): hopper, bank between bolted plates with feet, two pans",
    "estimates": "overall height 150 mm (1.3 x hopper width, from the photos), hopper depth 38 mm, bank 56-112 mm "
                 "high and 40 mm across, pans 34 x 84 mm with 40 mm fronts and 88 mm backs",
}


def riffle_splitter() -> Instrument:
    """Humboldt H-3971C micro riffle splitter with its two pans.

    Pieces: ``body`` (hopper, the riffle bank's 16 chutes and 17 dividers, the two upright plates with their feet and
    acorn nuts); ``pan_l`` and ``pan_r`` (the receiving pans, standing on the bench under the chutes' left and right
    exits); ``feed`` (a heap of powder in the hopper), ``stream`` (the curtain of powder falling through the chutes),
    ``split_l`` / ``split_r`` (the halves in the pans; they ride on their pans).

    Joints: ``pan_l`` / ``pan_r`` slide 90 mm straight out to the side (-x / +x) at v = 1, to be lifted off from there;
    ``feed``, ``stream``, ``split_l``, ``split_r`` are fades (0 hidden, 1 shown).

    Useful points (``RIFFLE_POINTS``): the hopper's rim centre, each pan's floor centre (pan frame, v = 0).
    """
    p = RIFFLE
    inst = Instrument("riffle_splitter", "Micro riffle splitter", "Humboldt H-3971C (Jones type, 16 x 3.2 mm chutes)",
                      (2 * p["pan_x1"], p["hopper"], p["bank_z1"] + p["hopper_h"]),
                      "Humboldt H-3971C page (chutes, hopper, pans); Gilson SP-171X photos for the look")
    body = _piece(inst, "body")
    n, ch, wl = p["n"], p["chute"], p["wall"]
    pitch = ch + wl
    L = n * pitch + wl                                           # the bank's length along y
    bw, z0, z1 = p["bank_w"], p["bank_z0"], p["bank_z1"]
    y0 = -L / 2
    # the dividers (thin plates across y) and between them the chutes' sloped floors, alternately to -x and +x
    divs = None
    for k in range(n + 1):
        d = box(-bw / 2, y0 + k * pitch, z0, bw / 2, y0 + k * pitch + wl, z1)
        divs = d if divs is None else divs.union(d)
    body.add("riffle dividers", divs, "dsc_stainless_dk")
    slope = math.degrees(math.atan2(z1 - z0 - 8.0, bw))
    flo = None
    for k in range(n):
        yc = y0 + k * pitch + wl + ch / 2
        s = 1.0 if k % 2 == 0 else -1.0                         # even chutes run down to +x, odd to -x
        Lf = math.hypot(bw, z1 - z0 - 8.0)
        f = box(-Lf / 2, yc - ch / 2, -wl / 2, Lf / 2, yc + ch / 2, wl / 2)
        f = f.rotate((0, 0, 0), (0, 1, 0), s * slope).translate((0, 0, (z0 + z1) / 2 - 4.0))
        flo = f if flo is None else flo.union(f)
    body.add("chute floors", flo, "dsc_stainless_dk")
    # the two upright plates (front and back of the bank), with feet bent out along y and acorn nuts on their faces
    pw, pt, ft = p["plate_w"], p["plate_t"], p["foot"]
    zt = z1 + 3.0                                               # up to the hopper's foot, where it is welded on
    for sy in (-1, 1):
        ya, yb = sorted((sy * L / 2, sy * (L / 2 + pt)))
        plate = box(-pw / 2, ya, 0.0, pw / 2, yb, zt)
        yfa, yfb = sorted((sy * (L / 2 + pt), sy * (L / 2 + pt + ft)))
        plate = plate.union(box(-pw / 2, yfa, 0.0, pw / 2, yfb, pt))
        body.add(f"upright {'front' if sy < 0 else 'back'}", plate, "dsc_stainless")
        nuts = None
        for (xx, zz) in ((-7, z0 + 6), (7, z0 + 6), (-7, z1 - 6), (7, z1 - 6), (0, 22)):
            yy = sy * (L / 2 + pt)
            nut = cq.Workplane("XZ").circle(3.0).extrude(-sy * 3.0).translate((xx, yy, zz))
            nut = nut.union(cq.Workplane("XY").sphere(2.6).translate((xx, yy + sy * 3.0, zz)))
            nuts = nut if nuts is None else nuts.union(nut)
        body.add(f"acorn nuts {'front' if sy < 0 else 'back'}", nuts, "dsc_stainless")
    # the bank's end walls between the dividers and the uprights
    for sy in (-1, 1):
        ya, yb = sorted((sy * (L / 2 - wl), sy * L / 2))
        body.add(f"bank end {sy:+d}", box(-bw / 2, ya, z0, bw / 2, yb, z1), "dsc_stainless_dk")
    # the hopper: a square funnel from a 114 x 114 mm rim down to a slot over the chutes
    H, hh, sw, t = p["hopper"], p["hopper_h"], p["slot_w"], p["sheet"]
    outer = _loft_rect(sw + 2 * t, L + 2 * t, z1, H, H, z1 + hh)
    inner = _loft_rect(sw, L, z1 - 0.01, H - 2 * t, H - 2 * t, z1 + hh + 0.01)
    hopper = outer.cut(inner)
    rim = box(-H / 2, -H / 2, z1 + hh - 3.0, H / 2, H / 2, z1 + hh).cut(
        box(-H / 2 + 5, -H / 2 + 5, z1 + hh - 4, H / 2 - 5, H / 2 - 5, z1 + hh + 1))
    body.add("hopper", hopper.union(rim), "dsc_stainless")
    # the pans: open boxes under the chutes' exits, fronts low and backs high ("Hy-Back")
    pd, ph, pb = p["pan_d"], p["pan_h"], p["pan_back"]
    xi, xo = p["pan_x0"], p["pan_x1"]
    for side, sx in (("pan_l", -1.0), ("pan_r", 1.0)):
        pan = _piece(inst, side)
        xa, xb = sorted((sx * xi, sx * xo))
        floor = box(xa, -pd / 2, 0.0, xb, pd / 2, t)
        xiw = sorted((sx * xi, sx * (xi + t)))
        xow = sorted((sx * (xo - t), sx * xo))
        wall_in = box(xiw[0], -pd / 2, 0.0, xiw[1], pd / 2, ph)
        wall_out = box(xow[0], -pd / 2, 0.0, xow[1], pd / 2, pb)
        # side walls: trapezoids rising from the low inner wall to the high back
        pts = [(sx * xi, 0.0), (sx * xo, 0.0), (sx * xo, pb), (sx * xi, ph)]
        side_f = cq.Workplane("XZ").polyline(pts).close().extrude(-t).translate((0, -pd / 2, 0))
        side_b = cq.Workplane("XZ").polyline(pts).close().extrude(t).translate((0, pd / 2, 0))
        pan.add(f"{side} sheet", floor.union(wall_in).union(wall_out).union(side_f).union(side_b), "dsc_stainless")
        split = _piece(inst, f"split_{side[-1]}")
        hx = (xi + xo) / 2
        heap = (cq.Workplane("XY").rect(xo - xi - 2 * t - 2, pd - 2 * t - 4).workplane(offset=6.0)
                .rect(xo - xi - 14, pd - 30).loft(ruled=True).translate((sx * hx, 0, t)))
        split.add(f"powder in {side}", heap, "dsc_al_powder")
    # the feed heap in the hopper and the falling curtain through the chutes
    feed = _piece(inst, "feed")
    zf = z1 + 6.0
    feed.add("powder in the hopper", _loft_rect(sw + 6, L - 4, zf, H * 0.62, H * 0.62, z1 + hh * 0.62), "dsc_al_powder")
    stream = _piece(inst, "stream")
    cur = None
    Lf = math.hypot(bw, z1 - z0 - 8.0)
    for k in range(n):
        yc = y0 + k * pitch + wl + ch / 2
        s = 1.0 if k % 2 == 0 else -1.0
        # a thin layer sliding down the chute's floor, then the drop from its exit into the pan
        lay = box(-Lf / 2 + 2, yc - ch / 2 + 0.5, wl / 2 + 0.2, Lf / 2 - 1, yc + ch / 2 - 0.5, wl / 2 + 1.2)
        lay = lay.rotate((0, 0, 0), (0, 1, 0), s * slope).translate((0, 0, (z0 + z1) / 2 - 4.0))
        drop = box(min(s * (bw / 2 + 2.5), s * (bw / 2 + 4.5)), yc - ch / 2 + 0.6, 6.0,
                   max(s * (bw / 2 + 2.5), s * (bw / 2 + 4.5)), yc + ch / 2 - 0.6, z0 - 1.0)
        cur = lay.union(drop) if cur is None else cur.union(lay).union(drop)
    stream.add("falling powder", cur, "dsc_al_powder")
    inst.joints = {
        "pan_l": Joint("slide", vec=(-90.0, 0.0, 0.0)),
        "pan_r": Joint("slide", vec=(90.0, 0.0, 0.0)),
        "split_l": Joint("fade", parent="pan_l"),
        "split_r": Joint("fade", parent="pan_r"),
        "feed": Joint("fade"),
        "stream": Joint("fade"),
    }
    inst.actions = [
        ("Powder poured into the hopper.", 1.4, {"feed": (0.0, 1.0)}),
        ("It runs through the 16 chutes, half to each pan.", 2.0, {"feed": (1.0, 0.0), "stream": (0.0, 1.0),
                                                                  "split_l": (0.0, 1.0), "split_r": (0.0, 1.0)}),
        ("", 0.6, {"stream": (1.0, 0.0)}),
        ("A pan slides out.", 1.2, {"pan_r": (0.0, 1.0)}),
    ]
    inst.labels = [("hopper 114 x 114 mm", (H / 2, 0, z1 + hh), (0.80, 0.20)),
                   ("16 chutes, 3.2 mm", (bw / 2, -L / 2, (z0 + z1) / 2), (0.82, 0.50)),
                   ("receiving pan", (-xo, -pd / 2, ph), (0.15, 0.70))]
    inst.props = ("feed", "stream", "split_l", "split_r")
    inst.cam = (0.9, -1.6, 0.8)
    inst.notes = ["Humboldt H-3971C: chutes and hopper published; heights and pans scaled from Gilson's SP-171X photos"]
    return inst


RIFFLE_POINTS = dict(hopper_rim=(0.0, 0.0, RIFFLE["bank_z1"] + RIFFLE["hopper_h"]),
                     pan_l_floor=(-(RIFFLE["pan_x0"] + RIFFLE["pan_x1"]) / 2, 0.0, RIFFLE["sheet"]),
                     pan_r_floor=((RIFFLE["pan_x0"] + RIFFLE["pan_x1"]) / 2, 0.0, RIFFLE["sheet"]))


# ============================================================================================ small things (props)
# The crucible: NETZSCH's Al2O3 crucible for the STA 449/509 TG-DSC sensor, 85 uL, 6.8 mm across, with its lid.
CRUCIBLE = dict(od=6.8, h=4.0, wall=0.4, floor=0.5, lid_od=6.8, lid_t=0.4, lid_plug=5.8, lid_hole=0.8)
SPECS["crucible"] = {
    "model": "Al2O3 crucible 85 uL with lid (NETZSCH, for the TG-DSC sensor)",
    "od": "6.8 mm (the brief; labware.py's TA/NETZSCH notes)",
    "h": "4.0 mm (estimate: 85 uL inside a 6.0 mm bore needs 3.0 mm, plus a 0.5 mm floor)",
}


def _revolve(pts) -> cq.Workplane:
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))


def crucible_model(material: str = "dsc_alumina") -> Model:
    """The 85 uL crucible, base at z = 0."""
    c = CRUCIBLE
    r, ri = c["od"] / 2, c["od"] / 2 - c["wall"]
    m = Model("crucible_85ul", "Al2O3 crucible 85 uL, 6.8 mm")
    m.add("crucible", _revolve([(0, 0), (r, 0), (r, c["h"]), (ri, c["h"]), (ri, c["floor"]), (0, c["floor"])]),
          material)
    return m


def lid_model(material: str = "dsc_alumina") -> Model:
    """Its lid: a 0.4 mm disc with a short plug and a pinhole, base of the plug at z = 0 (sits on the rim)."""
    c = CRUCIBLE
    m = Model("crucible_lid", "Al2O3 lid, 6.8 mm, pierced")
    disc = cyl(c["lid_od"], c["lid_t"], z=0.0).cut(cyl(c["lid_hole"], 2, z=-0.5))
    m.add("lid", disc, material)
    return m


def tweezers_model() -> Model:
    """Straight stainless tweezers, 120 mm, fine tips: tips at the origin pointing -x, the joint at x = +120."""
    m = Model("tweezers", "Stainless tweezers, 120 mm")
    L = 120.0
    for sy in (-1, 1):
        leg = (cq.Workplane("XY").polyline([(0.0, sy * 0.4), (L, sy * 4.0), (L, sy * 1.2), (0.0, sy * 0.1)]).close()
               .extrude(1.2).translate((0, 0, -0.6)))
        m.add(f"leg {sy:+d}", leg, "dsc_stainless")
    m.add("joint", box(L - 12, -4.0, -0.6, L, 4.0, 0.6), "dsc_stainless")
    return m


def spatula_model() -> Model:
    """A stainless micro-spatula, 150 mm: a 3 mm spoon at the tip (origin), the handle along +x."""
    m = Model("micro_spatula", "Micro-spatula, 150 mm, 3 mm spoon")
    rod = cq.Workplane("YZ").circle(1.0).extrude(140.0).translate((8.0, 0, 0.8))
    spoon = cq.Workplane("XY").ellipse(4.5, 1.8).extrude(0.6).translate((3.0, 0, 0))
    m.add("spatula", rod.union(spoon).union(box(5.0, -0.8, 0.0, 9.0, 0.8, 1.2)), "dsc_stainless")
    return m


def wash_bottle_model() -> Model:
    """A 250 mL LDPE wash bottle (ethanol): 66 mm across, 160 mm tall with its bent spout."""
    m = Model("wash_bottle", "Ethanol wash bottle, 250 mL")
    m.add("bottle", cyl(66, 120).edges(">Z").fillet(12).union(cyl(30, 10, z=118)), "dsc_ethanol_bottle")
    m.add("cap", cyl(34, 14, z=126), "dsc_ethanol_cap")
    pts = [(0, 0, 140), (0, 0, 165), (0, -30, 172), (0, -48, 160)]
    sp = None
    for a, b in zip(pts[:-1], pts[1:]):
        v = cq.Vector(*b) - cq.Vector(*a)
        seg = cq.Workplane().add(cq.Solid.makeCylinder(2.2, v.Length, cq.Vector(*a), v.normalized()))
        sp = seg if sp is None else sp.union(seg)
    m.add("spout", sp, "dsc_ethanol_bottle")
    m.add("label", box(-20, -33.6, 40, 20, -32.6, 80), "dsc_paper")
    return m


STANDARDS = [("In", "156.6 C", "dsc_indium"), ("Zn", "419.5 C", "dsc_zinc"), ("Al", "660.3 C", "al_metal"),
             ("Ag", "961.8 C", "dsc_silver"), ("Au", "1064.2 C", "dsc_gold")]


def standards_model() -> Model:
    """The calibration set: five pure-metal pieces (In, Zn, Al, Ag, Au, about 5 x 5 x 1 mm) in a 100 x 40 mm box."""
    m = Model("calib_set", "Pure-metal calibration standards In, Zn, Al, Ag, Au")
    tray = box(-50, -20, 0, 50, 20, 8).cut(box(-48, -18, 1.5, 48, 18, 9))
    for i in range(5):
        tray = tray.cut(cyl(12, 3, x=-38 + 19 * i, y=0, z=5.5))
    m.add("box", tray, "dsc_dark")
    for i, (_, _, mat) in enumerate(STANDARDS):
        m.add(f"piece {i}", box(-38 + 19 * i - 2.5, -2.5, 5.5, -38 + 19 * i + 2.5, 2.5, 6.6), mat)
    return m


def chip_model() -> Model:
    """A chip cut from a printed cube: about 3 x 3 x 1 mm (15 mg of Al), flat side down."""
    m = Model("chip", "Chip from a printed cube, ground flat on one side")
    chip = box(-1.6, -1.5, 0.0, 1.6, 1.5, 1.1).edges("|Z").fillet(0.4)
    m.add("chip", chip, "al_metal")
    return m


def cube_model() -> Model:
    """A 10 mm printed cube (SOP 02/03 coupon) on its stub of support."""
    m = Model("cube10", "Printed cube 10 mm")
    m.add("cube", box(-5, -5, 0, 5, 5, 10), "dsc_grey")
    return m


def monitor_model() -> Model:
    """The instrument PC's 24 in monitor (531 x 299 mm active) on its stand, and a keyboard."""
    m = Model("pc_screen", "Instrument PC: 24 in monitor and keyboard")
    m.add("stand", box(-110, -10, 0, 110, 170, 8).union(box(-25, 120, 8, 25, 140, 260)), "dsc_dark")
    m.add("monitor", box(-275, 100, 150, 275, 120, 470), "dsc_black")
    m.add("screen", box(-265, 99.0, 160, 265, 100.0, 460), "dsc_screen")
    m.add("keyboard", box(-220, -170, 0, 220, -30, 18).edges(">Z").chamfer(4), "dsc_dark")
    return m


# ============================================================================================ gas supply and vacuum pump
# Argon >= 99.999 % (grade 5.0) in a US size 300 cylinder: 9.25 in (235 mm) across, 55 in (1397 mm) tall without the
# valve (gas suppliers' cylinder charts, e.g. Airgas "Cylinder sizes": size 300, 49.9 L water volume). Body grey with a
# dark green shoulder (EN 1089-3's argon colour; US colours vary by supplier), a CGA 580 valve under a two-stage brass
# regulator with its two 63 mm gauges, chained to a floor stand.
GAS = dict(od=235.0, h=1397.0, neck=60.0, valve_h=110.0)
SPECS["gas_supply"] = {
    "cylinder": "US size 300: 9.25 x 55 in (235 x 1397 mm), 49.9 L water volume (gas suppliers' cylinder charts)",
    "argon": ">= 99.999 % (grade 5.0, the SOP)",
    "colours": "grey body, dark green shoulder (EN 1089-3 argon; US practice varies)",
    "regulator": "two-stage brass, two 2.5 in (63 mm) gauges (typical; estimate)",
}


def gas_supply() -> Instrument:
    """The argon cylinder on the floor with its regulator. Pieces: ``body``. Points: GAS_POINTS["outlet"]."""
    p = GAS
    inst = Instrument("gas_supply", "Argon cylinder and regulator", "Ar 5.0, US size 300 cylinder",
                      (p["od"] + 120, p["od"] + 40, p["h"] + p["valve_h"] + 140), "cylinder charts (size 300)")
    body = _piece(inst, "body")
    r = p["od"] / 2
    H = p["h"]
    cylb = _revolve([(0, 0), (r - 8, 0), (r, 8), (r, H - 160), (r - 30, H - 70), (p["neck"] / 2, H - 20),
                     (p["neck"] / 2, H), (0, H)])
    body.add("cylinder", cylb.cut(cyl(2 * r + 2, 220, z=H - 250)), "dsc_cyl_grey")
    body.add("shoulder", _revolve([(0, H - 250), (r, H - 250), (r, H - 160), (r - 30, H - 70), (p["neck"] / 2, H - 20),
                                   (p["neck"] / 2, H), (0, H)]), "dsc_cyl_green")
    body.add("valve", cyl(40, p["valve_h"], z=H).union(cyl(56, 18, z=H + 70)), "dsc_brass")
    zr = H + 60
    body.add("regulator", cq.Workplane("XZ").circle(32).extrude(-60).translate((0, -20, zr)).union(
        box(-12, -20, zr - 12, 12, 30, zr + 12)), "dsc_brass")
    for gx in (-48, 48):
        body.add(f"gauge {gx}", cq.Workplane("XZ").circle(31).extrude(-22).translate((gx, -30, zr + 50)).union(
            box(gx * 0.5 - 6, -30, zr, gx * 0.5 + 6, -18, zr + 40)), "dsc_lightgrey")
        body.add(f"gauge face {gx}", cq.Workplane("XZ").circle(27).extrude(1.0).translate((gx, -30.5, zr + 50)),
                 "dsc_white")
    body.add("outlet valve", box(-8, 30, zr - 8, 8, 70, zr + 8), "dsc_brass")
    body.add("stand", box(-r - 40, -r - 40, 0, r + 40, r + 40, 12).cut(cyl(2 * r + 4, 14, z=-1)).union(
        box(-r - 40, r + 20, 0, r + 40, r + 40, 900)), "dsc_dark")
    body.add("chain", _revolve([(r + 0.5, 880), (r + 6, 880), (r + 6, 888), (r + 0.5, 888)]), "dsc_steel_chain")
    return inst


GAS_POINTS = {"outlet": (0.0, 70.0, GAS["h"] + 60.0)}

# Edwards RV5 two-stage rotary vane pump: 430 x 158 x 225 mm (A, B and C of the dimension table in Edwards' RV
# brochure, read as length, width and height), 25 kg; a NW25 inlet on top at the motor's far end, an oil-level window.
PUMP = dict(L=430.0, W=158.0, H=225.0)
SPECS["vacuum_pump"] = {"model": "Edwards RV5 (two-stage rotary vane)",
                        "size": "430 x 158 x 225 mm, 25 kg: Edwards RV brochure dimension table (A, B, C) and weights",
                        "estimates": "motor and pump split, inlet position, from Edwards' product photos"}


def vacuum_pump() -> Instrument:
    """The rotary vane pump for evacuating the STA. Pieces: ``body``, ``led`` (fade: running). PUMP_POINTS["inlet"]."""
    p = PUMP
    L, W, H = p["L"], p["W"], p["H"]
    inst = Instrument("vacuum_pump", "Rotary vane vacuum pump", "Edwards RV5", (L, W, H), "Edwards RV brochure")
    body = _piece(inst, "body")
    body.add("feet", box(-L / 2 + 20, -W / 2 + 10, 0, L / 2 - 20, W / 2 - 10, 12), "dsc_black")
    body.add("motor", cq.Workplane("YZ").circle(70).extrude(200).translate((-L / 2, 0, 95)), "dsc_dark")
    body.add("fan cowl", cq.Workplane("YZ").circle(66).extrude(30).translate((-L / 2 - 10, 0, 95)), "dsc_black")
    body.add("pump block", box(-L / 2 + 200, -W / 2, 12, L / 2, W / 2, 190).edges("|X").fillet(20), "dsc_grey")
    body.add("handle", box(-40, -10, 190, 120, 10, H - 6).cut(box(-25, -11, 195, 105, 11, H - 18)), "dsc_dark")
    body.add("inlet", cyl(40, 30, x=L / 2 - 60, z=190).union(cyl(55, 6, x=L / 2 - 60, z=214)), "dsc_stainless")
    body.add("oil window", cq.Workplane("XZ").circle(14).extrude(2).translate((L / 2 - 90, -W / 2, 80)), "dsc_glass")
    led = _piece(inst, "led")
    led.add("running lamp", box(-L / 2 + 230, -W / 2 - 1.5, 150, -L / 2 + 244, -W / 2 + 0.2, 160), "led_green")
    inst.joints = {"led": Joint("fade")}
    return inst


PUMP_POINTS = {"inlet": (PUMP["L"] / 2 - 60.0, 0.0, 220.0)}


# ============================================================================================ microbalance (provisional)
BALANCE = dict(W=128.0, D=290.0, H=110.0, ch_w=100.0, ch_d=110.0, ch_h=95.0, ch_y=-60.0, pan_d=27.0, pan_z=40.0,
               term_w=240.0, term_d=170.0, term_h=60.0)
SPECS["microbalance"] = {"model": "provisional", "estimates": "all"}


def microbalance() -> Instrument:
    p = BALANCE
    inst = Instrument("microbalance", "Microbalance", "provisional", (p["W"], p["D"], p["H"] + p["ch_h"]), "provisional")
    body = _piece(inst, "body")
    W, D = p["W"], p["D"]
    body.add("base", box(-W / 2, -D / 2, 0, W / 2, D / 2, 30), "dsc_lightgrey")
    cy = -D / 2 + p["ch_d"] / 2 + 10
    body.add("pan", cyl(p["pan_d"], 1.0, y=cy, z=p["pan_z"] - 1).union(cyl(4, p["pan_z"] - 31, y=cy, z=30)), "dsc_stainless")
    body.add("tower", box(-W / 2, cy + p["ch_d"] / 2, 0, W / 2, D / 2, 30 + p["ch_h"] + 20), "dsc_lightgrey")
    body.add("front glass", box(-W / 2 + 5, cy - p["ch_d"] / 2 - 3, 30, W / 2 - 5, cy - p["ch_d"] / 2, 30 + p["ch_h"]), "dsc_glass")
    body.add("top frame", box(-W / 2, cy - p["ch_d"] / 2 - 3, 30 + p["ch_h"], W / 2, cy + p["ch_d"] / 2, 30 + p["ch_h"] + 6).cut(
        box(-W / 2 + 8, cy - p["ch_d"] / 2 + 5, 30 + p["ch_h"] - 1, W / 2 - 8, cy + p["ch_d"] / 2 - 5, 30 + p["ch_h"] + 7)), "dsc_lightgrey")
    for nm, sx in (("door_l", -1), ("door_r", 1)):
        d = _piece(inst, nm)
        d.add(nm, box(sx * W / 2 + sx * 0.5 - 2 + 2 * sx, cy - p["ch_d"] / 2, 31, sx * W / 2 + sx * 0.5 + 2 + 2 * sx, cy + p["ch_d"] / 2, 30 + p["ch_h"] - 1), "dsc_glass")
        d.add(nm + " grip", box(sx * W / 2 - 3 + sx * 3, cy - p["ch_d"] / 2 + 5, 60, sx * W / 2 + 3 + sx * 3, cy - p["ch_d"] / 2 + 15, 100), "dsc_grey")
    term = _piece(inst, "terminal")
    term.add("terminal", box(-p["term_w"] / 2, -D / 2 - p["term_d"] - 20, 0, p["term_w"] / 2, -D / 2 - 20, p["term_h"]), "dsc_lightgrey")
    inst.joints = {"door_l": Joint("slide", vec=(0, p["ch_d"] * 0.8, 0)), "door_r": Joint("slide", vec=(0, p["ch_d"] * 0.8, 0)),
                   "terminal": Joint("fade", v0=1.0)}
    return inst


_bcy = -BALANCE["D"] / 2 + BALANCE["ch_d"] / 2 + 10
BAL_POINTS = {"pan": (0.0, _bcy, BALANCE["pan_z"]), "top": (0.0, 0.0, 30 + BALANCE["ch_h"] + 6),
              "display": (0.0, -BALANCE["D"] / 2 - 100, BALANCE["term_h"]),
              "door_r_grip": (BALANCE["W"] / 2 + 6, _bcy - BALANCE["ch_d"] / 2 + 10, 80.0)}


# ============================================================================================ the STA
# NETZSCH STA 449 F5 Jupiter (TG-DSC, RT to 1600 C with the SiC furnace): 600 x 700 x 650 mm, 900 mm with the furnace
# raised, 83 kg without the PC (NETZSCH "Key technical data STA 449 F5 Jupiter", p. 1; brochure p. 14); vacuum-tight
# to 1e-2 mbar with automatic evacuation; three mass-flow controllers (one protective gas, two purge gases); an
# optional 20-position automatic sample changer (system version II); a motorized hoist that lifts the furnace, which
# then swings to the left or the right. NETZSCH does not label the axes: 600 is read as the width and 700 the depth,
# which the footage agrees with. Its successor, the STA 509 Jupiter Classic, has the same key data.
# Look and proportions from NETZSCH's product video (youtu.be/XDOAhT8CybU, 0:08 three-quarter, 0:45 square-on with the
# furnace raised, 0:29 the sensor head) and a lab's operating video of an F5 (youtu.be/mmuGqG-1LNE: 1:04 front-on,
# 3:04-3:18 raise and swing, 3:29 loading the sample crucible on the front position with tweezers): a light grey body
# whose front bulges in one smooth curve from the foot to the deck; a navy control panel with a teal band under the
# furnace ("lifting device" open/close, purge 1, purge 2, protective, power); the NETZSCH badge at the front right; a
# round grey plate on the deck centred on the sensor; the sensor carrier (a copper flange, a stack of white alumina
# radiation shields, a thin carrier tube and the sensor on top) inside a wire guard; the furnace, 150 mm across, light
# grey with a dark middle band and a gas fitting on top, on an arm from a white housing that rides up on a stainless
# lifting column behind it; green solenoid valves and gas fittings on the left side.
STA_P = dict(W=600.0, D=700.0, deck=320.0, feet=10.0, xs=-90.0, ys=-70.0, plate_d=380.0, f_d=150.0, f_h=250.0,
             band_lo=70.0, band_dark=110.0, cap_h=15.0, fit_h=62.0, lift=250.0, arm_r=175.0, swing=70.0,
             sens_h=140.0, shield_d=26.0, n_shield=8, col_w=100.0, house_w=150.0, house_h=220.0,
             pan_x0=-175.0, pan_x1=-5.0, pan_z0=60.0, pan_z1=292.0, logo_x=210.0)
SPECS["dsc_sta"] = {
    "model": "NETZSCH STA 449 F5 Jupiter (TG-DSC); successor STA 509 Jupiter Classic",
    "envelope": "600 x 700 x 650 mm, 900 mm furnace raised, 83 kg w/o PC: NETZSCH Key technical data STA 449 F5 "
                "Jupiter p. 1 (analyzing-testing.netzsch.com), brochure p. 14",
    "temperature": "RT-1600 C (SiC furnace): same",
    "vacuum": "1e-2 mbar, automatic evacuation: same",
    "gas": "3 mass-flow controllers (1 protective, 2 purge): same",
    "sample_changer": "20 positions, optional (system version II): same",
    "hoist": "motorized lift; the furnace swings left or right (operating video youtu.be/mmuGqG-1LNE at 3:13)",
    "crucible": "Al2O3 85 uL, 6.8 mm, GB399972, lid GB399973: NETZSCH accessories catalogue pp. 7, 8, 12",
    "estimates": "deck height 320 mm, furnace 150 x 250 mm + 77 mm cap and fitting, the sensor axis 0.35 W from the "
                 "left (from the 0:45 frame, width 600 mm as the scale); sensor 140 mm over the deck, lift 250 mm "
                 "(650 -> 900), arm radius 175 mm and swing 70 deg (from the 3:18 frame); everything else from the "
                 "frames",
}

_STA_FRONT = [(-330.0, 0.0), (-343.0, 40.0), (-350.0, 110.0), (-349.0, 170.0), (-341.0, 230.0), (-327.0, 275.0),
              (-312.0, 305.0), (-300.0, 320.0)]                  # (y, z) of the front's curve, foot to deck


def _sta(p) -> dict:
    """Positions the model and its anchors share."""
    zf = p["deck"] + 3.0                                           # the furnace's foot on the round plate
    return dict(zf=zf, zt=zf + p["f_h"], zc=zf + p["f_h"] + p["cap_h"], ztop=zf + p["f_h"] + p["cap_h"] + p["fit_h"],
                xc=p["xs"], yc=p["ys"] + p["arm_r"], zs=p["deck"] + p["sens_h"])


def sta_anchors(p, pose=None) -> dict:
    """Named points of the model for register.py; pose["hoist"] 0 closed, 1 raised; pose["furnace"] the swing."""
    g = _sta(p)
    pose = pose or {}
    lift = p["lift"] * float(pose.get("hoist", 0.0))
    ang = math.radians(p["swing"] * float(pose.get("furnace", 0.0)))
    W, D, dk = p["W"], p["D"], p["deck"]

    def fpt(x, y, z):                                              # a furnace point, swung about the column, lifted
        dx, dy = x - g["xc"], y - g["yc"]
        c, s_ = math.cos(ang), math.sin(ang)
        return (g["xc"] + c * dx - s_ * dy, g["yc"] + s_ * dx + c * dy, z + lift)
    r = p["f_d"] / 2
    a = {"deck front left": (-W / 2, -300.0, dk), "deck front right": (W / 2, -300.0, dk),
         "deck back left": (-W / 2, D / 2, dk), "deck back right": (W / 2, D / 2, dk),
         "foot front left": (-W / 2, -330.0, p["feet"]), "foot front right": (W / 2, -330.0, p["feet"]),
         "bulge left": (-W / 2, -350.0, 110.0), "bulge right": (W / 2, -350.0, 110.0),
         "panel top left": (p["pan_x0"], -313.0, p["pan_z1"] - 2), "panel top right": (p["pan_x1"], -313.0, p["pan_z1"] - 2),
         "panel bottom left": (p["pan_x0"], -344.0, p["pan_z0"]), "panel bottom right": (p["pan_x1"], -344.0, p["pan_z0"]),
         "logo": (p["logo_x"], -345.0, 55.0),
         "sensor": (p["xs"], p["ys"], g["zs"]),
         "plate": ("circle", (p["xs"], p["ys"], dk + 3.0), p["plate_d"] / 2),
         "furnace foot left": fpt(p["xs"] - r, p["ys"], g["zf"]), "furnace foot right": fpt(p["xs"] + r, p["ys"], g["zf"]),
         "furnace top left": fpt(p["xs"] - r, p["ys"], g["zt"]), "furnace top right": fpt(p["xs"] + r, p["ys"], g["zt"]),
         "band low left": fpt(p["xs"] - r, p["ys"], g["zf"] + p["band_lo"]),
         "band low right": fpt(p["xs"] + r, p["ys"], g["zf"] + p["band_lo"]),
         "band high left": fpt(p["xs"] - r, p["ys"], g["zf"] + p["band_lo"] + p["band_dark"]),
         "band high right": fpt(p["xs"] + r, p["ys"], g["zf"] + p["band_lo"] + p["band_dark"]),
         "fitting top": fpt(p["xs"], p["ys"], g["ztop"])}
    return a


def dsc_sta() -> Instrument:
    """NETZSCH STA 449 F5 Jupiter.

    Pieces: ``body`` (base, deck plate, sensor carrier with its shields and the sensor's sample (front) and reference
    (back) positions, wire guard, gas valves, panel); ``hoist`` (the lifting column and the white housing, slides up
    250 mm); ``furnace`` (the furnace and its arm: a hinge about the column, riding on the hoist; v = 1 swung 70 deg to
    the right); ``glow`` (fade: the furnace's hot inside, dull orange); ``asc`` (fade: the optional 20-position sample
    changer); ``leds`` (fade: the purge and protective gas lamps). ``STA_POINTS``: the sample and reference positions,
    the gas inlet, the vacuum port, the panel's buttons.
    """
    p = STA_P
    g = _sta(p)
    W, D, dk = p["W"], p["D"], p["deck"]
    inst = Instrument("dsc_sta", "Simultaneous thermal analyser (TG-DSC)", "NETZSCH STA 449 F5 Jupiter",
                      (W, D, 650.0), "NETZSCH key technical data (600 x 700 x 650/900 mm); look from NETZSCH's video "
                      "and a lab's operating video, fitted with register.py")
    body = _piece(inst, "body")
    # the base: the front's curve extruded across, the back square, the vertical corners rounded
    prof = [(y, z + p["feet"]) for y, z in _STA_FRONT[:-1]] + [(-300.0, dk), (D / 2, dk), (D / 2, p["feet"])]
    base = cq.Workplane("YZ").polyline(prof).close().extrude(W).translate((-W / 2, 0, 0))
    base = base.edges("|Z").fillet(18.0)
    body.add("base", base, "dsc_lightgrey")
    for fx in (-W / 2 + 45, W / 2 - 45):
        for fy in (-280.0, D / 2 - 45):
            body.add(f"foot {fx:+.0f} {fy:+.0f}", cyl(34, p["feet"], x=fx, y=fy), "dsc_dark")
    # the navy panel with its teal band, following the front's curve
    def front_y(z):
        zz = [q[1] + p["feet"] for q in _STA_FRONT]
        yy = [q[0] for q in _STA_FRONT]
        return float(np.interp(z, zz, yy))
    zs_ = np.linspace(p["pan_z0"], p["pan_z1"], 12)
    outer = [(front_y(z) - 1.2, z) for z in zs_]
    inner = [(front_y(z) + 2.0, z) for z in zs_[::-1]]
    panel = cq.Workplane("YZ").polyline(outer + inner).close().extrude(p["pan_x1"] - p["pan_x0"]).translate((p["pan_x0"], 0, 0))
    zb = p["pan_z1"] - 42.0
    band = cq.Workplane("YZ").polyline([(front_y(z) - 1.8, z) for z in np.linspace(zb, p["pan_z1"], 5)] +
                                       [(front_y(z) + 1.0, z) for z in np.linspace(p["pan_z1"], zb, 5)]).close() \
        .extrude(p["pan_x1"] - p["pan_x0"]).translate((p["pan_x0"], 0, 0))
    body.add("panel", panel.cut(band), "dsc_blue_navy")
    body.add("panel band", band, "dsc_teal")
    for k, zb_ in enumerate((200.0, 150.0, 95.0)):                  # open/close, purge 1/2/protective, power
        xb0 = p["pan_x0"] + 70.0
        body.add(f"button row {k}", box(xb0, front_y(zb_) - 3.0, zb_ - 6, xb0 + 80, front_y(zb_) + 1.0, zb_ + 6),
                 "dsc_grey")
    body.add("logo", box(p["logo_x"] - 42, front_y(55) - 2.0, 32, p["logo_x"] + 42, front_y(55) + 2.0, 78),
             "dsc_blue_navy")
    # the deck: the round grey plate, the sensor flange, shields, carrier tube and sensor; the wire guard
    xs, ys = p["xs"], p["ys"]
    body.add("deck plate", cyl(p["plate_d"], 3.0, x=xs, y=ys, z=dk), "dsc_grey")
    body.add("flange", cyl(62, 14, x=xs, y=ys, z=dk + 3).cut(cyl(20, 20, x=xs, y=ys, z=dk)), "dsc_copper")
    body.add("carrier tube", cyl(8, 75, x=xs, y=ys, z=dk + 10), "dsc_alumina")
    for k in range(p["n_shield"]):
        body.add(f"shield {k}", cyl(p["shield_d"], 3.0, x=xs, y=ys, z=dk + 20 + 7.0 * k), "dsc_alumina")
    zr = dk + 20 + 7.0 * p["n_shield"]
    body.add("thermocouple rod", cyl(3.5, g["zs"] - 3.0 - zr, x=xs, y=ys, z=zr), "dsc_alumina")
    # the TG-DSC sensor: a Pt plate with the sample position at the front (close to the user) and the reference behind
    sp = 5.6                                                       # each position's centre from the axis, mm
    body.add("sensor plate", box(xs - 4.6, ys - sp - 4.0, g["zs"] - 3.0, xs + 4.6, ys + sp + 4.0, g["zs"] - 2.4), "dsc_pt")
    for sy in (-1, 1):
        body.add(f"sensor disc {sy:+d}", cyl(7.4, 2.4, x=xs, y=ys + sy * sp, z=g["zs"] - 2.4), "dsc_pt")
    gr = 112.0                                                     # the wire guard's ring radius (clears the furnace)
    guard = None
    for ang in (115.0, 245.0):
        gx, gy = xs + gr * math.cos(math.radians(ang)), ys + gr * math.sin(math.radians(ang))
        post = cyl(6, 150, x=gx, y=gy, z=dk + 3)
        guard = post if guard is None else guard.union(post)
    ring = cq.Workplane("XY").circle(gr + 3).circle(gr - 3).extrude(5).translate((xs, ys, dk + 150))
    ring = ring.cut(box(xs + 40, ys - 200, dk + 140, xs + 200, ys + 200, dk + 160))   # open on the right: the swing
    body.add("wire guard", guard.union(ring), "dsc_stainless")
    body.add("crucible pad", box(110, 120, dk, 270, 300, dk + 3), "dsc_dark")
    # the gas side: two green solenoid valves and their fittings on the left side, the vacuum port behind on the right
    for k, vy in enumerate((90.0, 170.0)):
        body.add(f"valve {k}", box(-W / 2 - 34, vy - 16, 150, -W / 2, vy + 16, 190), "dsc_green")
        body.add(f"fitting {k}", cq.Workplane("YZ").circle(7).extrude(-40).translate((-W / 2, vy, 120)), "dsc_brass")
    body.add("vacuum port", cq.Workplane("YZ").circle(14).extrude(40).translate((W / 2, D / 2 - 90, 150)).union(
        cq.Workplane("YZ").circle(20).extrude(6).translate((W / 2 + 34, D / 2 - 90, 150))), "dsc_stainless")
    # the hoist: column (rises out of the base) and the white housing on it
    hoist = _piece(inst, "hoist")
    xc, yc = g["xc"], g["yc"]
    cw, hw, hh = p["col_w"], p["house_w"], p["house_h"]
    body.add("column collar", box(xc - cw / 2 - 18, yc - cw / 2 - 18, dk, xc + cw / 2 + 18, yc + cw / 2 + 18, dk + 26)
             .edges("|Z").fillet(8), "dsc_dark")
    zh0 = g["ztop"] - hh                                           # the housing's foot, furnace closed
    hoist.add("lifting column", box(xc - cw / 2, yc - cw / 2, dk - 230, xc + cw / 2, yc + cw / 2, zh0 + 20)
              .edges("|Z").fillet(6), "dsc_stainless")
    hoist.add("housing", box(xc - hw / 2, yc - hw / 2 + 10, zh0, xc + hw / 2, yc + hw / 2 + 10, zh0 + hh)
              .edges("|Z").fillet(14).edges(">Z").fillet(10), "dsc_white")
    # the furnace on its arm (swings about the column's axis), its bands, cap and top fitting
    fur = _piece(inst, "furnace")
    r = p["f_d"] / 2
    zf = g["zf"]
    shell = cyl(p["f_d"], p["f_h"], x=xs, y=ys, z=zf).cut(cyl(64, p["f_h"] - 30, x=xs, y=ys, z=zf - 1))
    lo = box(xs - r - 1, ys - r - 1, zf - 1, xs + r + 1, ys + r + 1, zf + p["band_lo"])
    mid = box(xs - r - 1, ys - r - 1, zf + p["band_lo"], xs + r + 1, ys + r + 1, zf + p["band_lo"] + p["band_dark"])
    fur.add("furnace lower", shell.intersect(lo), "dsc_lightgrey")
    fur.add("furnace band", shell.intersect(mid), "dsc_dark")
    fur.add("furnace upper", shell.cut(lo).cut(mid), "dsc_lightgrey")
    fur.add("cap", cyl(p["f_d"] - 20, p["cap_h"], x=xs, y=ys, z=g["zt"]), "dsc_grey")
    fur.add("top fitting", cyl(34, p["fit_h"] - 12, x=xs, y=ys, z=g["zc"]).union(
        cyl(46, 12, x=xs, y=ys, z=g["ztop"] - 12)), "dsc_glassy")
    fur.add("protective tube", tube(40, 33, p["f_h"] - 32, x=xs, y=ys, z=zf + 2), "dsc_alumina")
    arm_y0 = ys + r - 8
    fur.add("arm", box(xs - 32, arm_y0, g["zt"] - 140, xs + 32, yc - hw / 2 + 10, g["zt"] - 20), "dsc_white")
    glow = _piece(inst, "glow")
    glow.add("hot zone", tube(33, 31, p["f_h"] - 80, x=xs, y=ys, z=zf + 40), "dsc_hot")
    # the optional sample changer: a 20-position arc tray on the deck at the right and its gripper turret
    asc = _piece(inst, "asc")
    ax_, ay_ = 150.0, -40.0
    arc = cq.Workplane("XY").circle(120).circle(84).extrude(14).translate((ax_, ay_, dk))
    arc = arc.cut(box(ax_ - 130, ay_ - 10, dk - 1, ax_ + 130, ay_ + 130, dk + 20))
    for k in range(20):
        t = math.radians(190 + 8.0 * k)
        arc = arc.cut(cyl(7.6, 10, x=ax_ + 102 * math.cos(t), y=ay_ + 102 * math.sin(t), z=dk + 6))
    asc.add("changer tray", arc, "dsc_stainless")
    asc.add("changer turret", cyl(96, 330, x=ax_, y=ay_ + 60, z=dk).union(cyl(70, 40, x=ax_ - 55, y=ay_ - 30, z=dk + 250)), "dsc_white")
    leds = _piece(inst, "leds")
    for k in range(3):
        xl = p["pan_x0"] + 82 + 26 * k
        leds.add(f"gas lamp {k}", box(xl - 5, front_y(150) - 4.0, 147, xl + 5, front_y(150) - 2.8, 153), "led_green")
    leds.add("power lamp", box(p["pan_x0"] + 130, front_y(95) - 4.0, 92, p["pan_x0"] + 142, front_y(95) - 2.8, 98),
             "led_green")
    inst.joints = {
        "hoist": Joint("slide", vec=(0, 0, p["lift"])),
        "furnace": Joint("hinge", parent="hoist", axis=(0, 0, 1), pivot=(xc, yc, 0), deg=p["swing"]),
        "glow": Joint("fade", parent="furnace"),
        "asc": Joint("fade"),
        "leds": Joint("fade", v0=1.0),
    }
    inst.props = ("glow", "asc", "leds")
    inst.labels = [("furnace (SiC, to 1600 C)", (xs + r, ys, g["zt"] - 40), (0.80, 0.20)),
                   ("TG-DSC sensor", (xs, ys, g["zs"]), (0.15, 0.40))]
    inst.anchors = sta_anchors(p)
    inst.cam = (0.8, -1.6, 0.9)
    return inst


_g = _sta(STA_P)
STA_POINTS = {"sample": (STA_P["xs"], STA_P["ys"] - 5.6, _g["zs"]),          # crucible bases sit here
              "ref": (STA_P["xs"], STA_P["ys"] + 5.6, _g["zs"]),
              "sensor": (STA_P["xs"], STA_P["ys"], _g["zs"]),
              "furnace_top": (STA_P["xs"], STA_P["ys"], _g["ztop"]),
              "gas_in": (-STA_P["W"] / 2 - 40.0, 90.0, 120.0),
              "vac_port": (STA_P["W"] / 2 + 40.0, STA_P["D"] / 2 - 90.0, 150.0),
              "btn_open": (STA_P["pan_x0"] + 85.0, -345.0, 200.0),
              "panel": ((STA_P["pan_x0"] + STA_P["pan_x1"]) / 2, -345.0, 180.0)}
ANCHORS["dsc_sta"] = (STA_P, sta_anchors)
FREE["dsc_sta"] = ["deck", "xs", "f_d", "f_h", "band_lo", "band_dark", "pan_x0", "pan_x1", "pan_z0", "pan_z1",
                   "logo_x", "plate_d"]
CHECKS["dsc_sta"] = lambda p: [p["deck"] - p["pan_z1"] - 15, p["pan_x1"] - p["pan_x0"] - 100,
                               p["W"] / 2 + p["xs"] - p["f_d"] / 2 - 40, p["f_h"] - p["band_lo"] - p["band_dark"] - 30,
                               650.0 - (p["deck"] + 3 + p["f_h"] + p["cap_h"] + p["fit_h"]) + 15]


REGISTRY = {"microbalance": microbalance, "dsc_sta": dsc_sta, "riffle_splitter": riffle_splitter, "gas_supply": gas_supply,
            "vacuum_pump": vacuum_pump}
