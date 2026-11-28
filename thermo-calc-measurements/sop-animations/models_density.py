"""Models for SOP 03 (Archimedes density, porosity and crack density of printed cubes, #262 / #144): the analytical
balance with its density kit, the ultrasonic cleaner, the drying oven, a helium pycnometer, and the small things handled
at them (the cubes, the reference cube, tweezers, a fine brush, the wetting agent, a digital thermometer, wipes).

Same pattern as byu-vcl's ``vl/instruments.py``: each model is an ``Instrument`` of named pieces (CadQuery solids with
materials; ``body`` stays put) and a ``Joint`` per moving piece, sized from the maker's published dimensions. ``SPECS``
gives the source of every figure and marks the estimates; ``REGISTRY`` is what ``stage.get(key)`` builds;
``ANCHORS``/``FREE``/``CHECKS`` are what ``fit.py`` (register.py) fits to frames of the real machines (refs/<key>/).

* ``density_balance``: Mettler Toledo XPR225DR analytical balance (220 g x 0.1 mg, fine range 121 g x 0.01 mg) with
  the density kit for XPR/XSR analytical balances (30460852): the support plate that replaces the weighing pan and
  carries the beaker's pan off the weighing path, the bracket hung on the pan suspension (with its two small pans for
  the weighing in air), the holder for sinking solids hung on the bracket (the top dish and the immersed basket), the
  80 mm beaker of water and the thermometer clipped in it; the draft shield's side and top doors slide back.
* ``ultrasonic_bath``: Branson Bransonic CPX2800H (2.8 L, 40 kHz) with its tank cover and a mesh basket.
* ``drying_oven``: Memmert UN30 universal oven (32 L, natural convection), its door hinged on the right.
* ``he_pycnometer``: Micromeritics AccuPyc II 1345 (analysis module), its chamber cap and a 10 cm3 cup.

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

from common import Model, box, cyl, hose, rbox, tube  # noqa: E402
from instruments import Instrument, Joint, _piece, _xcyl, _ycyl  # noqa: E402

# name: (r, g, b, opacity, shininess 0-1)
MATERIALS = {
    "d3_white": (0.94, 0.94, 0.93, 1.0, 0.20),          # instrument white (XPR, Branson housing)
    "d3_light": (0.82, 0.83, 0.84, 1.0, 0.25),          # light grey trims, the XPR's door grips and corner caps
    "d3_grey": (0.55, 0.57, 0.59, 1.0, 0.30),           # the XPR's base and the sides of its rear housing
    "d3_dark": (0.22, 0.23, 0.25, 1.0, 0.30),
    "d3_black": (0.08, 0.08, 0.09, 1.0, 0.30),
    "d3_glass": (0.82, 0.90, 0.95, 0.20, 0.90),         # draft-shield glass
    "d3_beaker": (0.84, 0.91, 0.95, 0.26, 0.90),        # borosilicate beaker
    "d3_water": (0.64, 0.80, 0.92, 0.38, 0.80),         # distilled water
    "d3_ethanol": (0.80, 0.86, 0.90, 0.30, 0.80),
    "d3_steel": (0.74, 0.75, 0.77, 1.0, 0.75),          # stainless (kit parts, tweezers, oven inside, lids)
    "d3_steel_dk": (0.52, 0.53, 0.55, 1.0, 0.55),       # stainless mesh, in shadow
    "d3_brushed": (0.70, 0.71, 0.72, 1.0, 0.45),        # Memmert's brushed stainless case
    "d3_screen": (0.13, 0.15, 0.19, 1.0, 0.60),         # a dark touchscreen
    "d3_screen_ui": (0.36, 0.38, 0.72, 1.0, 0.10),      # the XPR terminal's violet bottom bar
    "d3_display": (0.30, 0.42, 0.48, 1.0, 0.30),        # an LCD (oven, thermometer)
    "d3_blue": (0.10, 0.36, 0.74, 1.0, 0.30),           # Branson's blue membrane panel and badge
    "d3_red": (0.78, 0.10, 0.14, 1.0, 0.30),            # the thermometer's red liquid
    "d3_cube": (0.58, 0.59, 0.61, 1.0, 0.15),           # as-built AlSi10Mg skin: matte grey
    "d3_cube_cut": (0.72, 0.73, 0.75, 1.0, 0.45),       # a saw-cut face
    "d3_ref": (0.80, 0.81, 0.83, 1.0, 0.60),            # wrought 6063, machined
    "d3_plate": (0.52, 0.53, 0.55, 1.0, 0.35),          # the build plate
    "d3_paper": (0.97, 0.97, 0.95, 1.0, 0.02),          # labels, wipes
    "d3_sic": (0.17, 0.19, 0.27, 1.0, 0.05),            # SiC paper
    "d3_hair": (0.82, 0.74, 0.58, 1.0, 0.10),           # a fine brush's bristles
    "d3_wood": (0.62, 0.44, 0.26, 1.0, 0.15),
    "d3_pe": (0.93, 0.93, 0.90, 0.85, 0.20),            # LDPE dropper bottle
    "d3_cap_blue": (0.15, 0.40, 0.75, 1.0, 0.25),
    "d3_cap_red": (0.70, 0.12, 0.12, 1.0, 0.25),
    "d3_al_dish": (0.78, 0.79, 0.81, 1.0, 0.70),        # an aluminium weighing dish
    "d3_mpurple": (0.10, 0.12, 0.30, 1.0, 0.40),        # Micromeritics' dark blue
}

SPECS: dict = {}
ANCHORS: dict = {}
FREE: dict = {}
CHECKS: dict = {}

XPR_RM = ("Mettler Toledo, Reference Manual XPR Analytical Balances and Comparators (30419844), 9.4.1 'XPR analytical "
          "balances, full-height draft shield' drawing (PDF p. 206, printed 204), which lists the XPR225DR, and the "
          "technical data (PDF p. 203): https://www.mt.com/dam/P5/labtec/02_Analytical_Balances/10_Excellence_Line/"
          "RM_XPR_Analytical_and_Comparators_EN.pdf")
DK_RM = ("Mettler Toledo, Reference Manual 'Density Kit for Analytical Balances, XPR, XPR Essential' (30419895C): "
         "https://www.mt.com/dam/P5/labtec/13_Accessories/Density_determination/03_Documentation/"
         "RM_DensityKit_XPR-XSR-analytical_en.pdf")
DK_VIDEO = "Mettler Toledo, 'How to mount XPR/XSR Analytical density kit' (youtu.be/b9Lm_9UVVzQ)"


# ===================================================================================================== the balance
# Mettler Toledo XPR225DR. The drawing (XPR_RM, 9.4.1): 336 mm deep without the terminal (486 with it, the terminal
# 150), 195 wide overall (the draft shield's glass box about 170, read off the front view: 160 clear inside; the door
# grips stand out at the sides), 292 high (282 to the top frame, the top door's handle to 292); a 57 mm base; the rear housing 170.5
# deep, 154 wide, 194 high; the chamber 165.5 deep, 160 wide clear, 150 deep clear at the top (134 at the floor, where
# the weighing cell's housing comes forward), 235 usable above the pan; the pan 78.5 x 73.5 (a grid), its top 42 above
# the bench and its centre (the weighing hook's axle) 80.5 behind the front; front feet 39 behind the front and 130
# apart, rear feet 32 from the back. The density kit (DK_RM 3.1-3.3, 4.2.2; DK_VIDEO 0:04-0:56): a support plate
# replaces the weighing pan; the bracket hangs on the pan suspension (it is weighed) and carries the holder; the pan
# goes into the support plate and carries the beaker (not weighed); the sample is weighed in air on one of the
# bracket's two small pans, and in the liquid in the holder's basket. Heights of the kit parts are read off the video
# (the 80 mm beaker sets the scale) and fitted (refs/density_balance).
XPR = dict(W=170.0, W_all=195.0, Wb=190.0, D=336.0, Hf=282.0, Hcap=292.0, base_h=57.0, floor_z=36.0, pan_top=42.0, rear_w=154.0,
           rear_d=170.5, rear_h=194.0, ch_d=165.5, clear_w=160.0, clear_d=150.0, glass=4.0, foot_y=39.0, foot_r=32.0,
           foot_x=65.0, pan_x=0.0, pan_dy=80.5, pan_w=78.5, pan_d=73.5, term_w=195.0, term_d=150.0, term_h0=20.0,
           term_h1=44.0, term_gap=6.0, label_x=-38.0, label_z=138.0, door_travel=150.0,
           kit_pan_d=88.0, kit_pan_h=10.0, beaker_d=80.0, beaker_h=74.0, water_h=56.0, arm_z=155.0, dish_d=42.0,
           basket_d=46.0, basket_z=53.0, susp_dy=44.0, susp_w=56.0, susp_h=64.0, bpan_x=62.0, bpan_dy=-18.0,
           bpan_d=34.0)

SPECS["density_balance"] = {
    "model": "Mettler Toledo XPR225DR analytical balance with the density kit for XPR/XSR analytical balances "
             "(30460852)",
    "published": {
        "capacity / readability": ("220 g x 0.1 mg; fine range 121 g x 0.01 mg", XPR_RM + " (technical data)"),
        "W x D x H": ("195 x 485 x 292 mm (with the terminal; the drawing gives 486 = 150 terminal + 336)", XPR_RM),
        "pan": ("78 x 73 mm (drawing 78.5 x 73.5), top 42 above the bench, centre 80.5 behind the front", XPR_RM),
        "usable height above the pan": ("235 mm", XPR_RM),
        "chamber clear": ("160 wide, 150 deep (134 at the floor)", XPR_RM),
        "base / rear housing": ("base 57 high; rear housing 170.5 deep, 154 wide, 194 high; top frame 282", XPR_RM),
        "feet": ("front feet 39 mm behind the front, 130 apart; rear feet 32 from the back", XPR_RM),
        "kit part number": ("30460852 'Density Kit (Analytical)'", "https://www.mt.com/shop/in/en/product/30460852/"
                                                                   "density-kit-analytical"),
        "kit contents": ("glass beaker 80 mm dia, high; pan; holder for sinking and floating solids; bracket; "
                         "support plate; wetting agent; precision thermometer with holder", DK_RM + " 3.1 p. 6"),
        "kit mounting": ("remove the weighing pan; insert the support plate; hang the bracket on the pan suspension; "
                         "insert the pan into the support plate", DK_RM + " 3.3 p. 7"),
        "weighing": ("sample in air on one of the two weighing pans of the bracket (on the holder's top pan if over "
                     "20 g); immersed in the holder's basket; remove bubbles with a fine brush; liquid at least 1 cm "
                     "over the sample; a few drops of wetting agent", DK_RM + " 4.2.2 pp. 9-11"),
        "holder wire": ("stainless steel, 0.6 mm", DK_RM + " 5.1 p. 15"),
    },
    "estimates": {
        "beaker height 85 mm": "the frame at 0:52 of " + DK_VIDEO + ", scaled by the 80 mm beaker; fitted",
        "kit pan 100 x 10 mm, bracket arm 168 mm over the bench, holder dish 38 mm, basket 56 mm": DK_VIDEO +
            " 0:31-0:58, scaled by the beaker; fitted",
        "pan suspension U 56 x 64 mm, 44 mm behind the pan centre": DK_VIDEO + " 0:05 (grid pan in place)",
        "terminal 20-44 mm thick": "drawing side view (not dimensioned)",
        "door travel 150 mm": "drawing side view (the dashed doors over the rear housing)",
    },
}


def _xpr(p) -> dict:
    yf = -p["D"] / 2
    py = yf + p["pan_dy"]                                  # the pan's centre (the weighing hook's axle)
    yt = yf + p["ch_d"]                                     # the chamber's back (the rear housing's front)
    ywall = yf + p["glass"] + p["clear_d"]                  # the back wall's face in the chamber
    return dict(yf=yf, py=py, yt=yt, ywall=ywall, yb=p["D"] / 2, hw=p["W"] / 2,
                kit_z0=p["floor_z"] + 2.0,                  # the support plate's top
                beaker_z0=p["floor_z"] + 2.0 + 2.0,         # the beaker stands on the kit pan's floor
                water_top=p["floor_z"] + 4.0 + 2.0 + p["water_h"])


def balance_points(p=None) -> dict:
    """Where things are in the balance's frame, for the SOP script: the bracket's left pan (a cube weighed in air sits
    on it), the holder's basket (a cube weighed in water), the water's surface, the beaker's rim, the doors' grips."""
    p = p or XPR
    g = _xpr(p)
    py = g["py"]
    return dict(air_pan=(-p["bpan_x"], py + p["bpan_dy"], p["pan_top"] + 3.0),
                basket=(0.0, py, p["basket_z"] + 3.0), water=g["water_top"],
                beaker_rim=(0.0, py, g["beaker_z0"] + p["beaker_h"]), pan=(0.0, py, p["pan_top"]),
                grip_left=(-g["hw"] - 6.0, g["yf"] + 20.0, p["base_h"] + 25.0),
                grip_top=(0.0, g["yf"] + 14.0, p["Hf"] + 6.0),
                terminal=(0.0, g["yf"] - p["term_gap"] - p["term_d"] / 2, p["term_h1"] - 6.0),
                door_open=(-g["hw"] - 2.0, g["yf"] + 70.0, 150.0), dish=(0.0, py, p["arm_z"] + 8.0))


def density_balance_anchors(p, pose=None) -> dict:
    g = _xpr(p)
    pose = pose or {}
    yf, hw, py = g["yf"], g["hw"], g["py"]
    dl = p["door_travel"] * float(pose.get("door_left", 0.0))
    a = {"cap front left": (-hw + 8, yf + 8, p["Hf"] + 4), "cap front right": (hw - 8, yf + 8, p["Hf"] + 4),
         "frame front left bottom": (-hw + 2, yf, p["base_h"]), "frame front right bottom": (hw - 2, yf, p["base_h"]),
         "base front left": (-p["Wb"] / 2, yf, 30.0), "base front right": (p["Wb"] / 2, yf, 30.0),
         "foot front left": (-p["foot_x"], yf + p["foot_y"], 0.0), "foot front right": (p["foot_x"], yf + p["foot_y"], 0.0),
         "top back left": (-hw + 2, g["yt"], p["Hf"]), "top back right": (hw - 2, g["yt"], p["Hf"]),
         "rear top back left": (-p["rear_w"] / 2, g["yb"], p["rear_h"]),
         "rear top back right": (p["rear_w"] / 2, g["yb"], p["rear_h"]),
         "door left top back": (-hw + 1, -6.0 + dl, p["Hf"] - 7), "door left bottom back": (-hw + 1, -6.0 + dl, p["base_h"] + 1),
         "label tl": (p["label_x"] - 30, g["ywall"], p["label_z"] + 11), "label tr": (p["label_x"] + 30, g["ywall"], p["label_z"] + 11),
         "label bl": (p["label_x"] - 30, g["ywall"], p["label_z"] - 11), "label br": (p["label_x"] + 30, g["ywall"], p["label_z"] - 11),
         "kit pan rim": ("circle", (0.0, py, g["kit_z0"] + p["kit_pan_h"]), p["kit_pan_d"] / 2),
         "beaker rim": ("circle", (0.0, py, g["beaker_z0"] + p["beaker_h"]), p["beaker_d"] / 2),
         "holder dish": ("circle", (0.0, py, p["arm_z"] + 11.0), p["dish_d"] / 2),
         "arm top": (0.0, py + 16.0, p["arm_z"] + 1.5),
         "bracket pan left": ("circle", (-p["bpan_x"], py + p["bpan_dy"], p["pan_top"] + 3.8), p["bpan_d"] / 2),
         "basket rim": ("circle", (0.0, py, p["basket_z"] + 3.0), p["basket_d"] / 2),
         "thermo top": (4.0, py - 27.0, g["beaker_z0"] + 146.0),
         "grid front left": (-p["pan_w"] / 2, py - p["pan_d"] / 2, p["pan_top"]),
         "grid front right": (p["pan_w"] / 2, py - p["pan_d"] / 2, p["pan_top"]),
         "susp top left": (-p["susp_w"] / 2, py + p["susp_dy"], p["pan_top"] + p["susp_h"]),
         "susp top right": (p["susp_w"] / 2, py + p["susp_dy"], p["pan_top"] + p["susp_h"])}
    return a


def _xpr_body(inst: Instrument, p: dict, g: dict):
    W, yf, yt, yb, hw = p["W"], g["yf"], g["yt"], g["yb"], g["hw"]
    body = _piece(inst, "body")
    # feet: two levelling feet at the front, two at the back
    for sx in (-1, 1):
        body.add(f"front foot {sx:+d}", cyl(26, 8, x=sx * p["foot_x"], y=yf + p["foot_y"]).union(
            cyl(10, 12, x=sx * p["foot_x"], y=yf + p["foot_y"], z=6)), "d3_light")
        body.add(f"rear foot {sx:+d}", cyl(18, 8, x=sx * p["foot_x"], y=yb - p["foot_r"]), "d3_dark")
    # the base: a grey plinth under a light top that holds the chamber floor
    body.add("plinth", box(-p["Wb"] / 2 + 8, yf + 10, 8, p["Wb"] / 2 - 8, yb - 6, 30).edges("|Z").fillet(6), "d3_grey")
    top = box(-p["Wb"] / 2, yf, 30, p["Wb"] / 2, yt, p["base_h"]).edges("|Z and <Y").fillet(5)
    top = top.cut(box(-p["clear_w"] / 2, yf + p["glass"] + 2, p["floor_z"], p["clear_w"] / 2, g["ywall"] - 1,
                      p["base_h"] + 1))
    body.add("base", top, "d3_light")
    body.add("chamber floor", box(-p["clear_w"] / 2, yf + p["glass"] + 2, p["floor_z"] - 1, p["clear_w"] / 2,
                                  g["ywall"] - 1, p["floor_z"]), "d3_grey")
    # the rear housing (electronics), its back finned; white with grey sides
    rw = p["rear_w"] / 2
    body.add("rear housing", box(-rw + 3, yt, 8, rw - 3, yb, p["rear_h"]).edges("|Y and >Z").fillet(8), "d3_white")
    for sx in (-1, 1):
        body.add(f"rear side {sx:+d}", box(min(sx * rw, sx * (rw - 3)), yt + 4, 12, max(sx * rw, sx * (rw - 3)),
                                           yb - 4, p["rear_h"] - 10), "d3_grey")
    for i in range(7):
        x = -rw + 18 + i * (p["rear_w"] - 36) / 6
        body.add(f"rear fin {i}", box(x - 2, yb - 1, 30, x + 2, yb + 2, p["rear_h"] - 25), "d3_light")
    # the chamber's back wall (the weighing cell's tower), white, with the model plate; the cell housing at its foot
    body.add("back wall", box(-hw + 6, g["ywall"], p["base_h"] - 2, hw - 6, yt + 6, p["Hf"]), "d3_white")
    body.add("cell housing", box(-p["clear_w"] / 2 + 6, g["ywall"] - 16, p["floor_z"], p["clear_w"] / 2 - 6,
                                 g["ywall"] + 1, p["floor_z"] + 34), "d3_white")
    lx, lz = p["label_x"], p["label_z"]
    body.add("model plate", box(lx - 30, g["ywall"] - 1.0, lz - 11, lx + 30, g["ywall"], lz + 11), "d3_light")
    body.add("model text", box(lx - 26, g["ywall"] - 1.3, lz - 3, lx - 2, g["ywall"] - 0.9, lz + 3), "d3_dark")
    # the pan suspension: a stainless U standing out of the cell housing behind the pan
    sy, sw, sh = g["py"] + p["susp_dy"], p["susp_w"], p["susp_h"]
    u = box(-sw / 2, sy - 1.5, p["floor_z"] + 6, -sw / 2 + 4, sy + 1.5, p["pan_top"] + sh).union(
        box(sw / 2 - 4, sy - 1.5, p["floor_z"] + 6, sw / 2, sy + 1.5, p["pan_top"] + sh)).union(
        box(-sw / 2, sy - 1.5, p["pan_top"] + sh - 4, sw / 2, sy + 1.5, p["pan_top"] + sh))
    body.add("pan suspension", u, "d3_steel")
    # the draft shield: the fixed front glass, the corner posts, the top frame with its corner caps
    body.add("front glass", box(-hw + 4, yf, p["base_h"], hw - 4, yf + p["glass"], p["Hf"] - 4), "d3_glass")
    for sx in (-1, 1):
        xa, xb = sorted((sx * hw, sx * (hw - 5)))
        body.add(f"front post {sx:+d}", box(xa, yf, p["base_h"], xb, yf + 6, p["Hf"] - 4), "d3_light")
        body.add(f"back post {sx:+d}", box(xa, yt - 8, p["base_h"], xb, yt, p["Hf"] - 4), "d3_light")
        body.add(f"side rail {sx:+d}", box(xa, yf, p["Hf"] - 5, xb, yb - 20, p["Hf"]), "d3_light")
        body.add(f"corner cap {sx:+d}", box(xa - (2 if sx < 0 else 0), yf - 2, p["Hf"] - 6, xb + (2 if sx > 0 else 0),
                                            yf + 16, p["Hf"] + 7), "d3_grey")
        body.add(f"door track {sx:+d}", box(xa, yf + 6, p["base_h"] - 3, xb, yb - 20, p["base_h"]), "d3_light")
    body.add("front rail", box(-hw, yf, p["Hf"] - 5, hw, yf + 6, p["Hf"]), "d3_light")
    body.add("back rail", box(-hw, yb - 26, p["Hf"] - 5, hw, yb - 20, p["Hf"]), "d3_light")


def density_balance() -> Instrument:
    """Mettler Toledo XPR225DR with the density kit (see XPR and SPECS). Pieces and joints:

    ``door_left`` / ``door_right`` / ``top_door``: slide back 0 -> 1 (150 mm); ``terminal``: the touch terminal (fixed;
    a piece of its own so a script can hide it); ``grid_pan``: the weighing pan, path 0 (in place) -> 1 (out through
    the left door); ``kit_plate``, ``kit_pan``, ``bracket``, ``beaker``: the kit, each a path 0 (installed) -> 1 (out to
    the left); ``water`` (fade, rides on the beaker); ``thermo``: the thermometer clip and probe (fade); ``holder``: the
    holder and basket, path 0 (hung on the bracket) -> 1 (lifted out); ``bubbles`` (fade, ride on the holder)."""
    p = XPR
    g = _xpr(p)
    inst = Instrument("density_balance", "Analytical balance with an Archimedes density kit",
                      "Mettler Toledo XPR225DR + density kit 30460852", (p["W"], p["D"] + p["term_d"], p["Hcap"]),
                      XPR_RM + "; " + DK_RM + "; the look from " + DK_VIDEO)
    yf, yt, hw, py = g["yf"], g["yt"], g["hw"], g["py"]
    _xpr_body(inst, p, g)
    # the terminal: a white tablet in front, its screen dark with a violet bar along the bottom
    term = _piece(inst, "terminal")
    ty1 = yf - p["term_gap"]
    ty0 = ty1 - p["term_d"]
    prof = [(ty0, 4.0), (ty1, 4.0), (ty1, p["term_h1"]), (ty0 + 6, p["term_h0"]), (ty0, p["term_h0"] - 4)]
    shell = cq.Workplane("YZ").polyline(prof).close().extrude(p["term_w"] / 2, both=True)
    term.add("terminal", shell.edges("|X").fillet(3), "d3_white")
    ang = math.atan2(p["term_h1"] - p["term_h0"], p["term_d"] - 6)
    for nm, (u0, u1, w, mat, dz) in {"screen": (18, p["term_d"] - 14, p["term_w"] - 26, "d3_screen", 0.6),
                                     "screen bar": (19, 30, p["term_w"] - 30, "d3_screen_ui", 0.9)}.items():
        u = (u0 + u1) / 2
        org = (0.0, ty0 + 6 + u, p["term_h0"] + u * math.tan(ang))
        pl = cq.Plane(origin=org, xDir=(1, 0, 0), normal=(0, -math.sin(ang), math.cos(ang)))
        term.add(nm, cq.Workplane(pl).rect(w, (u1 - u0) / math.cos(ang)).extrude(dz), mat)
    for sx in (-1, 1):
        term.add(f"terminal foot {sx:+d}", box(sx * 70 - 12, ty1 - 30, 0, sx * 70 + 12, ty1 - 10, 4), "d3_dark")
    # the doors: side doors (glass with a grey grip at the bottom front) and the top door, sliding back
    for side, sx in (("door_left", -1), ("door_right", 1)):
        d = _piece(inst, side)
        x0, x1 = sorted((sx * (hw - 1), sx * (hw - 1 - p["glass"])))
        d.add("door glass", box(x0, yf + 7, p["base_h"] + 1, x1, -6.0, p["Hf"] - 7), "d3_glass")
        ga, gb = sorted((sx * (hw - 1), sx * (p["W_all"] / 2 - 1)))
        d.add("door grip", box(ga, yf + 8, p["base_h"] + 1, gb, yf + 30, p["base_h"] + 42).union(
            box(ga, yf + 8, p["base_h"] + 1, gb + (0 if sx < 0 else 0), yf + 44, p["base_h"] + 10)), "d3_grey")
        d.add("door top strip", box(x0, yf + 7, p["Hf"] - 12, x1, -6.0, p["Hf"] - 7), "d3_light")
    top = _piece(inst, "top_door")
    top.add("top glass", box(-hw + 8, yf + 8, p["Hf"] - 4, hw - 8, -8.0, p["Hf"] - 1), "d3_glass")
    top.add("top grip", box(-22, yf + 8, p["Hf"] - 1, 22, yf + 22, p["Hcap"]), "d3_grey")
    # the weighing pan (a grid), as it is before the kit goes in
    gp = _piece(inst, "grid_pan")
    grid = box(-p["pan_w"] / 2, py - p["pan_d"] / 2, p["pan_top"] - 2, p["pan_w"] / 2, py + p["pan_d"] / 2, p["pan_top"])
    for i in range(9):
        y = py - p["pan_d"] / 2 + 6 + i * (p["pan_d"] - 12) / 8
        grid = grid.cut(box(-p["pan_w"] / 2 + 5, y - 2.4, p["pan_top"] - 3, p["pan_w"] / 2 - 5, y + 2.4, p["pan_top"] + 1))
    gp.add("grid pan", grid, "d3_steel")
    gp.add("grid pan stem", box(-8, py + p["pan_d"] / 2 - 2, p["pan_top"] - 2, 8, py + p["susp_dy"] - 1.5,
                                p["pan_top"] + 1), "d3_steel")
    # ------------------------------------------------------------------------------------------ the density kit
    k0 = g["kit_z0"]
    plate = _piece(inst, "kit_plate")
    sp = box(-p["clear_w"] / 2 + 3, yf + p["glass"] + 5, p["floor_z"], p["clear_w"] / 2 - 3, g["ywall"] - 18, k0)
    sp = sp.cut(cyl(p["kit_pan_d"] - 10, 6, y=py, z=p["floor_z"] - 1))
    sp = sp.cut(box(-p["susp_w"] / 2 - 6, py + p["susp_dy"] - 10, p["floor_z"] - 1, p["susp_w"] / 2 + 6,
                    g["ywall"], k0 + 1))
    plate.add("support plate", sp, "d3_grey")
    kp = _piece(inst, "kit_pan")
    pan = cyl(p["kit_pan_d"], p["kit_pan_h"], y=py, z=k0).cut(cyl(p["kit_pan_d"] - 4, p["kit_pan_h"], y=py, z=k0 + 2))
    kp.add("beaker pan", pan.union(cyl(p["kit_pan_d"] - 12, 4, y=py, z=p["floor_z"] - 0.5)), "d3_steel")
    # the bracket: hung on the suspension's crossbar, a plate rising behind the beaker to the arm that carries the
    # holder over the beaker's centre; its foot bar carries the two small pans (the in-air weighing) left and right
    br = _piece(inst, "bracket")
    sy = py + p["susp_dy"]
    sz = p["pan_top"] + p["susp_h"]
    br.add("hook", box(-14, sy - 4, sz - 2, 14, sy + 4, sz + 2).union(box(-14, sy - 4, sz - 12, 14, sy - 2.5, sz + 2)),
           "d3_steel")
    rear = py + p["beaker_d"] / 2 + 10.0                    # the bracket's plate, 10 mm behind the beaker
    br.add("drop plate", box(-10, sy - 2.5, p["pan_top"] - 1, 10, sy - 1.0, sz - 2), "d3_steel")
    br.add("foot bar", box(-p["bpan_x"], sy - 2.5, p["pan_top"] - 1, p["bpan_x"], sy + 0.5, p["pan_top"] + 1.5), "d3_steel")
    for sx in (-1, 1):
        x = sx * p["bpan_x"]
        br.add(f"pan arm {sx:+d}", box(x - 2, py + p["bpan_dy"], p["pan_top"] - 1, x + 2, sy, p["pan_top"] + 1.5),
               "d3_steel")
        br.add(f"small pan {sx:+d}", cyl(p["bpan_d"], 1.2, x=x, y=py + p["bpan_dy"], z=p["pan_top"] + 0.8).union(
            tube(p["bpan_d"], p["bpan_d"] - 2.4, 3.0, x=x, y=py + p["bpan_dy"], z=p["pan_top"] + 0.8)), "d3_steel")
    ry = py + 8.0                                            # the riser's plane, just behind the holder's wires
    az = p["arm_z"]
    pts = [(-p["bpan_x"] - 2.0, p["pan_top"] + 13.0), (-p["bpan_x"] + 12.0, p["pan_top"] + 13.0), (-18.0, az),
           (-32.0, az)]
    br.add("riser", cq.Workplane("XZ").polyline(pts).close().extrude(-1.5).translate((0, ry, 0)), "d3_steel")
    br.add("riser foot", box(-p["bpan_x"] - 2.0, ry, p["pan_top"] - 1, -p["bpan_x"] + 12.0, sy + 0.5, p["pan_top"] + 13.0)
           .cut(box(-p["bpan_x"] - 3.0, ry + 1.5, p["pan_top"] + 0.5, -p["bpan_x"] + 13.0, sy - 2.5, p["pan_top"] + 14.0)),
           "d3_steel")
    arm = box(-32.0, py - 6, az, 10.0, ry + 1.5, az + 1.5).cut(cyl(5, 4, y=py, z=az - 1))
    arm = arm.cut(box(-2.5, py - 7, az - 1, 2.5, py, az + 3))
    br.add("arm", arm, "d3_steel")
    # the beaker, its water and the thermometer (clip on the rim, probe down the back)
    bk = _piece(inst, "beaker")
    bz0 = g["beaker_z0"]
    bk.add("beaker", tube(p["beaker_d"], p["beaker_d"] - 3.2, p["beaker_h"], y=py, z=bz0).union(
        cyl(p["beaker_d"], 2.0, y=py, z=bz0)), "d3_beaker")
    wat = _piece(inst, "water")
    wat.add("water", cyl(p["beaker_d"] - 3.4, p["water_h"], y=py, z=bz0 + 2.0), "d3_water")
    th = _piece(inst, "thermo")
    tx, ty = 4.0, py - 27.0                                     # the kit's precision thermometer, in front of the holder
    th.add("thermometer", cyl(6.0, 130.0, x=tx, y=ty, z=bz0 + 16).edges(">Z").fillet(2.5), "d3_beaker")
    th.add("bulb", cyl(4.0, 12.0, x=tx, y=ty, z=bz0 + 17), "d3_red")
    th.add("column", cyl(1.2, 70.0, x=tx, y=ty - 2.2, z=bz0 + 28), "d3_red")
    yb_ = py - p["beaker_d"] / 2                                # the beaker's front wall
    th.add("clip", box(tx - 5, yb_ - 3, bz0 + p["beaker_h"] - 14, tx + 5, ty + 4, bz0 + p["beaker_h"] + 4).cut(
        box(tx - 6, yb_ - 0.5, bz0 + p["beaker_h"] - 15, tx + 6, yb_ + 2.5, bz0 + p["beaker_h"])).cut(
        cyl(6.4, 40, x=tx, y=ty, z=bz0 + p["beaker_h"] - 20)), "d3_light")
    # the holder: the top dish, its stem through the arm, two wires down to the basket (a perforated dish)
    hd = _piece(inst, "holder")
    az = p["arm_z"]
    hd.add("dish", cyl(p["dish_d"], 1.2, y=py, z=az + 8.0).union(
        tube(p["dish_d"], p["dish_d"] - 2.0, 3.0, y=py, z=az + 8.0)), "d3_steel")
    hd.add("collar", cyl(9.0, 6.0, y=py, z=az + 1.6).union(cyl(3.0, 2.0, y=py, z=az + 7.0)), "d3_steel")
    bz = p["basket_z"]
    wx = p["basket_d"] / 2 - 4.0
    wires = None
    for sx in (-1, 1):
        w = hose([(0.0, py, az + 2.0), (0.0, py, az - 22.0), (sx * wx, py, az - 46.0), (sx * wx, py, bz + 14.0),
                  (sx * (wx + 1.5), py, bz + 4.0)], 1.2)
        wires = w if wires is None else wires.union(w)
    hd.add("wires", wires, "d3_steel")
    for sx in (-1, 1):
        hd.add(f"clip {sx:+d}", box(sx * wx - 2.5, py - 2.0, bz + 6.0, sx * wx + 2.5, py + 2.0, bz + 16.0), "d3_steel")
    basket = cyl(p["basket_d"], 1.0, y=py, z=bz).union(tube(p["basket_d"], p["basket_d"] - 2.0, 3.0, y=py, z=bz))
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i * i + j * j <= 5:
                basket = basket.cut(cyl(3.0, 3.0, x=i * 8.0, y=py + j * 8.0, z=bz - 1.0))
    hd.add("basket", basket, "d3_steel_dk")
    bub = _piece(inst, "bubbles")
    rng = np.random.default_rng(3)
    bb = None
    for k in range(9):
        a_ = rng.uniform(0, 2 * math.pi)
        r_ = rng.uniform(8, p["basket_d"] / 2 - 4)
        s = cq.Workplane("XY").sphere(rng.uniform(0.7, 1.3)).translate(
            (r_ * math.cos(a_), py + r_ * math.sin(a_), bz + 1.6))
        bb = s if bb is None else bb.union(s)
    for k in range(5):
        sx = 1 if k % 2 else -1
        s = cq.Workplane("XY").sphere(0.9).translate((sx * (wx + 1.0), py, bz + 20.0 + 9.0 * k))
        bb = bb.union(s)
    bub.add("air bubbles", bb, "d3_glass")
    out_l = (-hw - 120.0, 0.0, 30.0)
    inst.joints = {
        "door_left": Joint("slide", vec=(0, p["door_travel"], 0)),
        "door_right": Joint("slide", vec=(0, p["door_travel"], 0)),
        "top_door": Joint("slide", vec=(0, p["door_travel"], 0)),
        "grid_pan": Joint("path", path=((0, 0, 0), (0, 0, 14.0), (out_l[0], 0, 14.0))),
        "kit_plate": Joint("path", path=((0, 0, 0), (0, 0, 10.0), (out_l[0], 0, 10.0))),
        "kit_pan": Joint("path", path=((0, 0, 0), (0, 0, 12.0), (out_l[0], 0, 12.0))),
        "bracket": Joint("path", path=((0, 0, 0), (0, 0, 8.0), (0, -30.0, 8.0), (out_l[0], -30.0, 30.0))),
        "beaker": Joint("path", path=((0, 0, 0), (0, 0, 6.0), (out_l[0] - 60, 0, 6.0))),
        "water": Joint("fade", parent="beaker", v0=1.0),
        "thermo": Joint("fade", parent="beaker", v0=1.0),
        "holder": Joint("path", path=((0, 0, 0), (0, 0, p["beaker_h"] + 6.0), (out_l[0] - 40, -20.0,
                                                                                p["beaker_h"] + 30.0))),
        "bubbles": Joint("fade", parent="holder", v0=0.0),
    }
    inst.labels = [("XPR225DR: 0.01 mg (121 g range)", (hw, yf, 200.0), (0.80, 0.25)),
                   ("holder: dish over the basket", (0.0, py, p["arm_z"] + 10), (0.80, 0.42)),
                   ("80 mm beaker of water", (p["beaker_d"] / 2, py, g["beaker_z0"] + 60), (0.80, 0.62))]
    inst.anchors = density_balance_anchors(p)
    inst.cam = (0.6, -1.7, 0.7)
    return inst


ANCHORS["density_balance"] = (XPR, density_balance_anchors)
FREE["density_balance"] = ["beaker_h", "arm_z", "kit_pan_h", "label_x", "label_z", "base_h", "susp_h", "susp_dy",
                           "basket_z", "dish_d"]
CHECKS["density_balance"] = lambda p: [p["arm_z"] - (p["floor_z"] + 4 + p["beaker_h"]) - 25,
                                       p["Hf"] - 5 - p["arm_z"] - 30, p["basket_z"] - p["floor_z"] - 12,
                                       p["floor_z"] + 6 + p["water_h"] - p["basket_z"] - 25,
                                       p["base_h"] - p["pan_top"] - 5, 120 - p["beaker_h"]]


# ===================================================================================================== ultrasonic bath
# Branson Bransonic CPX2800H. Spec sheet BCL-0002-12 p. 2 (https://www.branson.emerson.com/is/content/emerson/en/
# corporate/branson/documents/bransonic-ultrasonic-cleaner-cpx-specification-sheet.pdf): 2.8 L tank 230 x 140 x 100 mm
# (L x W x D); overall 337 x 304 x 302 mm (13.3 x 12 x 11.9 in, L x W x H); 40 kHz; tank cover included. Operator's
# manual 100-214-294 Rev 10 (PDF p. 25): the axes of those figures. The look (Branson's CPX overview video,
# youtu.be/iGkhh2gYXN4, 0:17-0:41): a white housing; the control tower at the back, its sloped front a blue membrane
# panel with the display; a blue BRANSON badge low on the right of the front. Mesh basket 100-916-334 (sold
# separately), 8 x 4 x 3 in by a reseller's listing.
BATH = dict(L=337.0, W=304.0, H=302.0, tank_l=230.0, tank_w=140.0, tank_d=100.0, deck=190.0, front_t=26.0,
            lip_h=11.0, lip_out=5.0, tower_w=300.0, tower_d=118.0, slope_d=74.0, tower_r=70.0, panel_w=150.0,
            badge_w=136.0, badge_h=150.0, badge_x=12.0, recess_w=170.0, water=45.0, basket=(203.0, 102.0, 76.0))

SPECS["ultrasonic_bath"] = {
    "model": "Branson Bransonic CPX2800H ultrasonic cleaner (2.8 L, 40 kHz)",
    "published": {
        "tank": ("2.8 L; 230 x 140 x 100 mm (L x W x D)", "Branson spec sheet BCL-0002-12 p. 2"),
        "overall": ("337 x 304 x 302 mm (13.3 x 12 x 11.9 in, L x W x H)", "Branson spec sheet BCL-0002-12 p. 2; "
                    "axes from manual 100-214-294 Rev 10 PDF p. 25"),
        "frequency": ("40 kHz", "spec sheet"), "cover": ("tank cover included", "spec sheet"),
        "basket": ("mesh basket 100-916-334, sold separately", "Branson accessory sheet p. 2 (hosted by a reseller: "
                   "static.qsource.com/documents/Branson/Bransonic_Accessories.pdf)"),
    },
    "estimates": {
        "basket 203 x 102 x 76 mm": "a reseller's listing (tequipment.net), not Branson's",
        "deck 190 mm, tower 270 x 118 mm with a 70 mm slope": "Branson's CPX video, fitted (refs/ultrasonic_bath)",
        "badge 96 x 34 mm": "the video",
    },
}


def _cpx(p) -> dict:
    yf = -p["W"] / 2
    ty0 = yf + p["front_t"]                                   # the tank's front edge
    return dict(yf=yf, yb=p["W"] / 2, ty0=ty0, ty1=ty0 + p["tank_w"], tcy=ty0 + p["tank_w"] / 2,
                tw0=p["W"] / 2 - p["tower_d"])


def bath_points(p=None) -> dict:
    p = p or BATH
    g = _cpx(p)
    return dict(tank=(0.0, g["tcy"], p["deck"] - p["tank_d"]), water=p["deck"] - p["tank_d"] + p["water"],
                deck=p["deck"], lid_knob=(0.0, g["tcy"], p["deck"] + 16.0),
                panel=(0.0, g["tw0"] + p["slope_d"] * 0.55, p["deck"] + (p["H"] - p["deck"]) * 0.55))


def ultrasonic_bath_anchors(p, pose=None) -> dict:
    g = _cpx(p)
    L, yf, dk, H = p["L"], g["yf"], p["deck"], p["H"]
    tw, tw0 = p["tower_w"], g["tw0"]
    a = {"front top left": (-L / 2, yf, dk), "front top right": (L / 2, yf, dk),
         "front bottom left": (-L / 2, yf, 0.0), "front bottom right": (L / 2, yf, 0.0),
         "back top right": (L / 2, g["yb"], dk),
         "tank front left": (-p["tank_l"] / 2, g["ty0"], dk), "tank front right": (p["tank_l"] / 2, g["ty0"], dk),
         "tank back left": (-p["tank_l"] / 2, g["ty1"], dk), "tank back right": (p["tank_l"] / 2, g["ty1"], dk),
         "tower top left": (-tw / 2, tw0 + p["slope_d"], H), "tower top right": (tw / 2, tw0 + p["slope_d"], H),
         "tower foot left": (-tw / 2, tw0, dk), "tower foot right": (tw / 2, tw0, dk),
         "badge tl": (L / 2 - p["badge_x"] - p["badge_w"], yf + p["lip_out"], dk - p["lip_h"] - 4),
         "badge tr": (L / 2 - p["badge_x"], yf + p["lip_out"], dk - p["lip_h"] - 4),
         "badge bl": (L / 2 - p["badge_x"] - p["badge_w"], yf + p["lip_out"], dk - p["lip_h"] - 4 - p["badge_h"]),
         "badge br": (L / 2 - p["badge_x"], yf + p["lip_out"], dk - p["lip_h"] - 4 - p["badge_h"]),
         "lip front bottom left": (-L / 2, yf, dk - p["lip_h"]), "lip front bottom right": (L / 2, yf, dk - p["lip_h"])}
    return a


def ultrasonic_bath() -> Instrument:
    """Branson CPX2800H. Pieces: ``body``; ``lid`` (the tank cover, path 0 on -> 1 lifted off to the right);
    ``basket`` (the mesh basket, slide 0 in -> 1 lifted 110 mm); ``water`` (fade); ``ripple`` (fade: the 40 kHz
    cavitation shown as a faint disturbed surface)."""
    p = BATH
    g = _cpx(p)
    L, W, H, dk = p["L"], p["W"], p["H"], p["deck"]
    yf, yb, tw0 = g["yf"], g["yb"], g["tw0"]
    inst = Instrument("ultrasonic_bath", "Ultrasonic cleaner", "Branson Bransonic CPX2800H", (L, W, H),
                      "Branson spec sheet BCL-0002-12; manual 100-214-294; the look from Branson's CPX video")
    body = _piece(inst, "body")
    lo, lh = p["lip_out"], p["lip_h"]
    tz0 = dk - p["tank_d"]
    shell = rbox(L - 2 * lo, W - 2 * lo, dk - lh, 18, y=0.0, z=0.0)
    body.add("housing", shell, "d3_white")
    lip = rbox(L, W, lh, 22, y=0.0, z=dk - lh).edges(">Z").fillet(4)
    lip = lip.cut(box(-p["tank_l"] / 2 - 4, g["ty0"] - 4, dk - lh - 1, p["tank_l"] / 2 + 4, g["ty1"] + 4, dk + 1))
    body.add("collar", lip, "d3_white")
    tank = box(-p["tank_l"] / 2 - 4, g["ty0"] - 4, tz0 - 2, p["tank_l"] / 2 + 4, g["ty1"] + 4, dk).cut(
        box(-p["tank_l"] / 2, g["ty0"], tz0, p["tank_l"] / 2, g["ty1"], dk + 1))
    body.add("tank", tank, "d3_steel")
    body.add("tank rim", box(-p["tank_l"] / 2 - 8, g["ty0"] - 8, dk - 1, p["tank_l"] / 2 + 8, g["ty1"] + 8, dk + 1.5)
             .cut(box(-p["tank_l"] / 2, g["ty0"], dk - 2, p["tank_l"] / 2, g["ty1"], dk + 3)), "d3_steel")
    # the front: a recessed panel at the left, the blue BRANSON badge at the right
    yfr = yf + lo
    body.add("recess", box(-L / 2 + lo + 16, yfr - 0.8, 24, -L / 2 + lo + 16 + p["recess_w"], yfr + 0.2, dk - lh - 8)
             .cut(box(-L / 2 + lo + 20, yfr - 1.0, 28, -L / 2 + lo + 12 + p["recess_w"], yfr + 0.4, dk - lh - 12)),
             "d3_light")
    bx1 = L / 2 - p["badge_x"]
    bz1 = dk - lh - 4
    body.add("badge", box(bx1 - p["badge_w"], yfr - 0.8, bz1 - p["badge_h"], bx1, yfr + 0.2, bz1), "d3_blue")
    body.add("badge text", box(bx1 - p["badge_w"] + 12, yfr - 1.2, bz1 - 26, bx1 - 12, yfr - 0.6, bz1 - 12), "d3_white")
    # the control tower: a loaf behind the tank, its front sloped back, the blue panel on the slope
    tw = p["tower_w"]
    prof = [(tw0, dk - 1), (yb - 6, dk - 1), (yb - 6, H), (tw0 + p["slope_d"], H), (tw0, dk + 26)]
    tower = cq.Workplane("YZ").polyline(prof).close().extrude(tw / 2, both=True)
    tower = tower.edges("|Y and >Z").fillet(p["tower_r"])
    body.add("tower", tower, "d3_white")
    ang = math.atan2(H - dk - 26, p["slope_d"])
    u0, u1 = 0.10, 0.80
    for nm, (w, mat, a0, a1, dz) in {"panel": (p["panel_w"], "d3_blue", u0, u1, 0.8),
                                     "display": (64.0, "d3_display", 0.40, 0.72, 1.3)}.items():
        s_ = math.hypot(p["slope_d"], H - dk - 26)
        uc = (a0 + a1) / 2
        org = (0.0, tw0 + p["slope_d"] * uc, dk + 26 + (H - dk - 26) * uc)
        pl = cq.Plane(origin=org, xDir=(1, 0, 0), normal=(0, -math.sin(ang), math.cos(ang)))
        body.add(nm, cq.Workplane(pl).rect(w, s_ * (a1 - a0)).extrude(dz), mat)
    for i in range(5):                                         # the keys under the display
        uc = 0.24
        org = (-44.0 + 22.0 * i, tw0 + p["slope_d"] * uc, dk + 26 + (H - dk - 26) * uc)
        pl = cq.Plane(origin=org, xDir=(1, 0, 0), normal=(0, -math.sin(ang), math.cos(ang)))
        body.add(f"key {i}", cq.Workplane(pl).rect(15, 12).extrude(1.6), "d3_white")
    for sx in (-1, 1):
        for sy in (-1, 1):
            body.add(f"foot {sx}{sy}", cyl(22, 6, x=sx * (L / 2 - 30), y=sy * (W / 2 - 30), z=-5.5), "d3_dark")
    # the tank cover: stainless, a lip all round and a knob
    lid = _piece(inst, "lid")
    lid.add("cover", box(-p["tank_l"] / 2 - 10, g["ty0"] - 10, dk + 1.5, p["tank_l"] / 2 + 10, g["ty1"] + 10, dk + 3.5)
            .union(box(-p["tank_l"] / 2 + 1, g["ty0"] + 1, dk - 8, p["tank_l"] / 2 - 1, g["ty1"] - 1, dk + 2)
                   .cut(box(-p["tank_l"] / 2 + 2.5, g["ty0"] + 2.5, dk - 9, p["tank_l"] / 2 - 2.5, g["ty1"] - 2.5,
                            dk + 1))), "d3_steel")
    lid.add("knob", cyl(26, 10, y=g["tcy"], z=dk + 3.5).union(cyl(14, 8, y=g["tcy"], z=dk + 13)), "d3_dark")
    bw, bd, bh = p["basket"]
    bas = _piece(inst, "basket")
    bz0 = tz0 + 10.0
    frame = box(-bw / 2, g["tcy"] - bd / 2, bz0, bw / 2, g["tcy"] + bd / 2, bz0 + bh).cut(
        box(-bw / 2 + 1.2, g["tcy"] - bd / 2 + 1.2, bz0 + 1.2, bw / 2 - 1.2, g["tcy"] + bd / 2 - 1.2, bz0 + bh + 1))
    for i in range(1, 12):
        x = -bw / 2 + i * bw / 12
        frame = frame.cut(box(x - 4, g["tcy"] - bd / 2 - 1, bz0 + 6, x + 4, g["tcy"] + bd / 2 + 1, bz0 + bh - 6))
    bas.add("mesh basket", frame, "d3_steel_dk")
    for sx in (-1, 1):
        bas.add(f"handle {sx:+d}", hose([(sx * (bw / 2 - 2), g["tcy"] - 20, bz0 + bh), (sx * (bw / 2 - 2), g["tcy"] - 20,
                                                                                      bz0 + bh + 14),
                                         (sx * (bw / 2 - 2), g["tcy"] + 20, bz0 + bh + 14),
                                         (sx * (bw / 2 - 2), g["tcy"] + 20, bz0 + bh)], 3.0), "d3_steel")
    wat = _piece(inst, "water")
    wat.add("water", box(-p["tank_l"] / 2 + 0.5, g["ty0"] + 0.5, tz0 + 0.5, p["tank_l"] / 2 - 0.5, g["ty1"] - 0.5,
                         tz0 + p["water"]), "d3_water")
    rip = _piece(inst, "ripple")
    rr = None
    for i in range(7):
        x = -p["tank_l"] / 2 + 20 + i * (p["tank_l"] - 40) / 6
        s = box(x - 9, g["ty0"] + 6, tz0 + p["water"] - 0.4, x + 9, g["ty1"] - 6, tz0 + p["water"] + 0.6)
        rr = s if rr is None else rr.union(s)
    rip.add("cavitation", rr, "d3_glass")
    inst.joints = {
        "lid": Joint("path", path=((0, 0, 0), (0, 0, 40.0), (L / 2 + 140.0, 0, 20.0), (L / 2 + 160.0, 0, -dk + 9.0))),
        "basket": Joint("slide", vec=(0, 0, 110.0)),
        "water": Joint("fade", v0=1.0),
        "ripple": Joint("fade", v0=0.0),
    }
    inst.anchors = ultrasonic_bath_anchors(p)
    inst.cam = (0.6, -1.6, 0.9)
    return inst


ANCHORS["ultrasonic_bath"] = (BATH, ultrasonic_bath_anchors)
FREE["ultrasonic_bath"] = ["lip_h", "tower_w", "slope_d", "badge_w", "badge_x"]
CHECKS["ultrasonic_bath"] = lambda p: [p["deck"] - p["tank_d"] - 30, p["H"] - p["deck"] - 60,
                                       p["W"] - p["front_t"] - p["tank_w"] - p["tower_d"] - 8,
                                       p["L"] - p["tower_w"] - 10, p["tower_d"] - p["slope_d"] - 25,
                                       p["L"] / 2 - p["badge_x"] - p["badge_w"] - 20, p["lip_h"] - 6]


# ===================================================================================================== drying oven
# Memmert UN30 universal oven (natural convection), Memmert's product page and its generated PDF
# (https://www.memmert.com/en/products/heating-drying-ovens/universal-oven/un30-2/pdf): 32 L; interior 400 x 320 x 250
# mm (w x h x d); exterior 585 x 704 x 434 mm (w x h x d, +56 mm for the door handle); +20 to +300 C; one stainless
# grid supplied, three at most; the drawing (p. 1): 93 mm of wall each side of the interior, its floor 120 mm over the
# bench, feet 30 mm, a 57 mm vent in the back, the interior 88 mm behind the front; the door hinged on the right, its
# handle a vertical bar at the left; the ControlCOCKPIT along the top (a display at the left, the turn-push knob in the
# middle, the logo at the right). Panel and handle positions are read off that drawing.
OVEN = dict(W=585.0, H=704.0, D=434.0, handle=56.0, feet=30.0, ch_w=400.0, ch_h=320.0, ch_d=250.0, ch_z0=120.0,
            ch_y=88.0, door_t=39.0, door_z0=28.0, door_z1=540.0, panel_x0=-234.0, panel_x1=237.0, panel_z0=592.0,
            disp_x0=-185.0, disp_x1=-90.0, disp_z0=639.0, disp_z1=693.0, knob_x=3.5, knob_z=603.5, knob_d=56.0,
            handle_x=-216.0, handle_z0=40.0, handle_z1=550.0, grid_z=250.0)

SPECS["drying_oven"] = {
    "model": "Memmert UN30 universal oven (32 L, natural convection)",
    "published": {
        "volume": ("32 L", "memmert.com UN30 PDF p. 2"),
        "interior": ("400 x 320 x 250 mm (w x h x d)", "memmert.com UN30 PDF p. 2"),
        "exterior": ("585 x 704 x 434 mm (w x h x d), d + 56 mm door handle", "memmert.com UN30 PDF p. 3"),
        "temperature": ("+20 to +300 C", "memmert.com UN30 PDF p. 2"),
        "grids": ("1 stainless steel grid supplied, max. 3", "memmert.com UN30 PDF pp. 2-3"),
        "drawing": ("93 mm each side of the interior; interior floor 120 mm over the bench; feet 30 mm; rear vent "
                    "57 mm; interior 88 mm behind the front", "memmert.com UN30 PDF p. 1"),
    },
    "estimates": {
        "door 39 mm thick, 28-540 mm high; panel 592-704 mm; display, knob and handle positions":
            "read off the drawing (memmert.com UN30 PDF p. 1), not dimensioned there; fitted (refs/drying_oven)",
        "grid at 250 mm": "the middle rail (photos)",
    },
}


def oven_points(p=None) -> dict:
    p = p or OVEN
    yf = -p["D"] / 2
    yc0 = yf + p["ch_y"]
    return dict(grid=(0.0, yc0 + p["ch_d"] / 2, p["grid_z"] + 6.0), handle=(p["handle_x"], yf - p["handle"] + 10,
                                                                             (p["handle_z0"] + p["handle_z1"]) / 2),
                knob=(p["knob_x"], yf - 12.0, p["knob_z"]), hinge=(p["W"] / 2, yf, 0.0), yf=yf, yc0=yc0)


def drying_oven_anchors(p, pose=None) -> dict:
    W, H, yf = p["W"], p["H"], -p["D"] / 2
    yb = p["D"] / 2
    yc0 = yf + p["ch_y"]
    a = {"top front left": (-W / 2, yf, H), "top front right": (W / 2, yf, H), "top back left": (-W / 2, yb, H),
         "top back right": (W / 2, yb, H), "bottom front left": (-W / 2, yf, p["feet"]),
         "bottom front right": (W / 2, yf, p["feet"]), "bottom back left": (-W / 2, yb, p["feet"]),
         "panel bottom left": (-W / 2, yf, p["door_z1"]), "panel bottom right": (W / 2, yf, p["door_z1"]),
         "display tl": (p["disp_x0"], yf, p["disp_z1"]), "display tr": (p["disp_x1"], yf, p["disp_z1"]),
         "display bl": (p["disp_x0"], yf, p["disp_z0"]), "display br": (p["disp_x1"], yf, p["disp_z0"]),
         "knob": (p["knob_x"], yf - 10.0, p["knob_z"]),
         "handle top": (p["handle_x"], yf - p["handle"], p["handle_z1"]),
         "handle bottom": (p["handle_x"], yf - p["handle"], p["handle_z0"]),
         "chamber tl": (-p["ch_w"] / 2, yc0, p["ch_z0"] + p["ch_h"]), "chamber tr": (p["ch_w"] / 2, yc0, p["ch_z0"] + p["ch_h"]),
         "chamber bl": (-p["ch_w"] / 2, yc0, p["ch_z0"]), "chamber br": (p["ch_w"] / 2, yc0, p["ch_z0"]),
         "chamber back bl": (-p["ch_w"] / 2, yc0 + p["ch_d"], p["ch_z0"]),
         "chamber back tr": (p["ch_w"] / 2, yc0 + p["ch_d"], p["ch_z0"] + p["ch_h"])}
    return a


def drying_oven() -> Instrument:
    """Memmert UN30. Pieces: ``body``; ``door`` (hinge on the right front edge, 0 shut -> 1 open 100 degrees);
    ``grid`` (the shelf, slide 0 in -> 1 out 120 mm); ``warm`` (fade: a dull glow on the display when heating)."""
    p = OVEN
    W, H, D = p["W"], p["H"], p["D"]
    yf, yb = -D / 2, D / 2
    yc = yf + p["door_t"]                                     # the cabinet's front, behind the door
    yc0 = yf + p["ch_y"]
    inst = Instrument("drying_oven", "Drying oven", "Memmert UN30", (W, D + p["handle"], H),
                      "memmert.com UN30 product PDF (dimensions and drawing); the look from frames of a UN30 video")
    body = _piece(inst, "body")
    cab = box(-W / 2, yc, p["feet"], W / 2, yb, H).edges("|Y").fillet(4)
    cab = cab.cut(box(-p["ch_w"] / 2, yc - 1, p["ch_z0"], p["ch_w"] / 2, yc0 + p["ch_d"], p["ch_z0"] + p["ch_h"]))
    body.add("case", cab, "d3_brushed")
    body.add("chamber", box(-p["ch_w"] / 2 - 2, yc0 + p["ch_d"], p["ch_z0"] - 2, p["ch_w"] / 2 + 2, yc0 + p["ch_d"] + 2,
                            p["ch_z0"] + p["ch_h"] + 2).union(
        box(-p["ch_w"] / 2 - 2, yc0, p["ch_z0"] - 2, p["ch_w"] / 2 + 2, yc0 + p["ch_d"], p["ch_z0"])), "d3_steel")
    for side in (-1, 1):                                       # the grid's rails on the side walls
        for z in (p["ch_z0"] + 90.0, p["grid_z"], p["ch_z0"] + 230.0):
            xa, xb = sorted((side * p["ch_w"] / 2, side * (p["ch_w"] / 2 - 6)))
            body.add(f"rail {side:+d} {z:.0f}", box(xa, yc0 + 10, z - 3, xb, yc0 + p["ch_d"] - 10, z), "d3_steel")
    body.add("gasket", box(-p["ch_w"] / 2 - 18, yc - 1.5, p["ch_z0"] - 18, p["ch_w"] / 2 + 18, yc, p["ch_z0"] + p["ch_h"] + 18)
             .cut(box(-p["ch_w"] / 2, yc - 2, p["ch_z0"], p["ch_w"] / 2, yc + 1, p["ch_z0"] + p["ch_h"])), "d3_dark")
    # the ControlCOCKPIT along the top front: a black band, the display at the left, the knob in the middle
    body.add("panel", box(-W / 2, yf, p["door_z1"] + 2, W / 2, yc, H).edges("|Y and >Z").fillet(4), "d3_brushed")
    body.add("cockpit", box(p["panel_x0"], yf - 1.0, p["panel_z0"], p["panel_x1"], yf + 2, H - 8), "d3_black")
    body.add("display", box(p["disp_x0"], yf - 1.6, p["disp_z0"], p["disp_x1"], yf, p["disp_z1"]), "d3_display")
    body.add("knob", _ycyl(p["knob_d"], 14, x=p["knob_x"], y=yf - 14, z=p["knob_z"]).union(
        _ycyl(p["knob_d"] + 10, 3, x=p["knob_x"], y=yf - 2, z=p["knob_z"])), "d3_steel")
    body.add("logo", box(p["panel_x1"] - 90, yf - 1.4, p["panel_z0"] + 12, p["panel_x1"] - 20, yf, p["panel_z0"] + 24),
             "d3_red")
    body.add("switch", box(p["panel_x0"] + 6, yf - 1.4, p["panel_z0"] + 6, p["panel_x0"] + 36, yf, p["panel_z0"] + 18),
             "d3_light")
    for sx in (-1, 1):
        for sy in (-1, 1):
            body.add(f"foot {sx}{sy}", box(sx * (W / 2 - 50) - 45, sy * (D / 2 - 60) - 45, 0, sx * (W / 2 - 50) + 45,
                                           sy * (D / 2 - 60) + 45, p["feet"]), "d3_dark")
    body.add("vent", _ycyl(57, 20, x=-W / 2 + 140, y=yb, z=400.0), "d3_dark")
    for z in (p["door_z0"] + 20, p["door_z1"] - 20):
        body.add(f"hinge {z:.0f}", box(W / 2 - 50, yf - 4, z - 14, W / 2 + 4, yf + 4, z + 14), "d3_steel")
    door = _piece(inst, "door")
    door.add("door", box(-W / 2, yf, p["door_z0"], W / 2, yc - 2, p["door_z1"]).edges("|Y").fillet(3), "d3_brushed")
    door.add("door inner", box(-p["ch_w"] / 2 + 4, yc - 2, p["ch_z0"] + 4, p["ch_w"] / 2 - 4, yc + 6,
                               p["ch_z0"] + p["ch_h"] - 4), "d3_steel")
    hx = p["handle_x"]
    door.add("handle", box(hx - 12, yf - p["handle"], p["handle_z0"] + 30, hx + 12, yf - p["handle"] + 16,
                           p["handle_z1"] - 30), "d3_black")
    for z in (p["handle_z0"], p["handle_z1"] - 30):
        door.add(f"handle mount {z:.0f}", box(hx - 30, yf - p["handle"], z, hx + 60, yf, z + 30), "d3_black")
    grid = _piece(inst, "grid")
    gz = p["grid_z"]
    gr = box(-p["ch_w"] / 2 + 6, yc0 + 12, gz, p["ch_w"] / 2 - 6, yc0 + p["ch_d"] - 12, gz + 6)
    gr = gr.cut(box(-p["ch_w"] / 2 + 10, yc0 + 16, gz - 1, p["ch_w"] / 2 - 10, yc0 + p["ch_d"] - 16, gz + 7))
    for i in range(1, 20):
        x = -p["ch_w"] / 2 + 6 + i * (p["ch_w"] - 12) / 20
        gr = gr.union(box(x - 1.2, yc0 + 14, gz + 1, x + 1.2, yc0 + p["ch_d"] - 14, gz + 4))
    grid.add("grid", gr, "d3_steel")
    warm = _piece(inst, "warm")
    warm.add("display lit", box(p["disp_x0"] + 4, yf - 2.0, p["disp_z0"] + 4, p["disp_x1"] - 4, yf - 1.5,
                                p["disp_z1"] - 4), "d3_screen_ui")
    inst.joints = {
        "door": Joint("hinge", axis=(0, 0, 1), pivot=(W / 2, yf, 0.0), deg=100.0),
        "grid": Joint("slide", vec=(0, -120.0, 0)),
        "warm": Joint("fade", v0=0.0),
    }
    inst.anchors = drying_oven_anchors(p)
    inst.cam = (0.7, -1.6, 0.6)
    return inst


ANCHORS["drying_oven"] = (OVEN, drying_oven_anchors)
FREE["drying_oven"] = ["door_z1", "panel_x0", "panel_x1", "panel_z0", "disp_x0", "disp_x1", "disp_z0", "disp_z1",
                       "knob_x", "knob_z", "handle_x", "handle_z0", "handle_z1"]
CHECKS["drying_oven"] = lambda p: [p["door_z1"] - p["ch_z0"] - p["ch_h"] - 40, p["H"] - p["door_z1"] - 100,
                                   p["disp_z1"] - p["disp_z0"] - 20, p["handle_z1"] - p["handle_z0"] - 250,
                                   p["disp_x1"] - p["disp_x0"] - 40]


# ===================================================================================================== He pycnometer
# Micromeritics AccuPyc II 1345, operator manual Rev B (Sep 2022), https://downloads.micromeritics.com/Guides/
# AccuPyc-II-1345-Operator-Manual-Rev-B-Sep-2022.pdf: the analysis module (1, 10 and 100 cm3 versions) 20 cm H x 22.2 cm
# W x 36.2 cm D (PDF p. 28); cups: 10 cm3 chamber 1.85 cm ID x 3.95 cm deep (PDF p. 30); repeatability typically
# +-0.01 % of the nominal full-scale volume, accuracy 0.03 % of reading + 0.03 % of the sample capacity (PDF p. 30).
# Not registered to footage: drawn to the published envelope, the chamber cap on the top near the front (manual).
PYC = dict(W=222.0, D=362.0, H=200.0, cap_d=64.0, cap_y=-90.0, cup_id=18.5, cup_h=39.5)

SPECS["he_pycnometer"] = {
    "model": "Micromeritics AccuPyc II 1345 helium pycnometer (analysis module, 10 cm3)",
    "published": {
        "analysis module": ("20 cm H x 22.2 cm W x 36.2 cm D", "AccuPyc II 1345 operator manual Rev B, PDF p. 28"),
        "10 cm3 cup": ("1.85 cm ID x 3.95 cm deep", "operator manual PDF p. 30"),
        "repeatability / accuracy": ("+-0.01 % of full scale; 0.03 % of reading + 0.03 % of capacity",
                                     "operator manual PDF p. 30"),
    },
    "estimates": {"cap 64 mm, 90 mm in front of the centre": "not registered; the layout from the manual's figures"},
}


def he_pycnometer() -> Instrument:
    p = PYC
    W, D, H = p["W"], p["D"], p["H"]
    inst = Instrument("he_pycnometer", "Helium gas pycnometer", "Micromeritics AccuPyc II 1345", (W, D, H),
                      "AccuPyc II 1345 operator manual Rev B (envelope and cups); not registered")
    body = _piece(inst, "body")
    body.add("case", rbox(W, D, H, 14, z=0.0).edges(">Z").fillet(8), "d3_light")
    body.add("front", box(-W / 2 + 6, -D / 2 - 1, 20, W / 2 - 6, -D / 2 + 2, H - 30), "d3_mpurple")
    body.add("chamber well", cyl(p["cap_d"] + 16, 3, y=p["cap_y"], z=H), "d3_dark")
    cap = _piece(inst, "cap")
    cap.add("chamber cap", cyl(p["cap_d"], 26, y=p["cap_y"], z=H + 3).union(cyl(30, 10, y=p["cap_y"], z=H + 29)),
            "d3_steel")
    cup = _piece(inst, "cup")
    cup.add("sample cup", tube(p["cup_id"] + 3, p["cup_id"], p["cup_h"], y=p["cap_y"], z=H - p["cup_h"] + 2).union(
        cyl(p["cup_id"] + 3, 1.5, y=p["cap_y"], z=H - p["cup_h"] + 2)), "d3_steel")
    cup.add("powder", cyl(p["cup_id"] - 0.4, p["cup_h"] * 0.6, y=p["cap_y"], z=H - p["cup_h"] + 3.6), "d3_cube")
    inst.joints = {"cap": Joint("path", path=((0, 0, 0), (0, 0, 40.0), (90.0, 0, 40.0), (110.0, 0, -H + 30))),
                   "cup": Joint("slide", vec=(0, 0, 60.0))}
    return inst


# ===================================================================================================== small things
CUBE = 5.0


def cube(size: float = CUBE, remnant: float = 0.0, mat: str = "d3_cube") -> Model:
    """A printed cube standing on the bench (z = 0 its underside), with `remnant` mm of support stubs below it."""
    m = Model("cube", f"{size:g} mm printed cube")
    m.add("cube", box(-size / 2, -size / 2, remnant, size / 2, size / 2, remnant + size), mat)
    if remnant > 0:
        st = None
        for i in range(4):
            for j in range(4):
                x, y = -size / 2 + (i + 0.5) * size / 4, -size / 2 + (j + 0.5) * size / 4
                s = box(x - 0.25, y - 0.25, 0.0, x + 0.25, y + 0.25, remnant + 0.1)
                st = s if st is None else st.union(s)
        m.add("support stubs", st, "d3_cube_cut")
    return m


def ref_cube(size: float = CUBE) -> Model:
    m = Model("ref_cube", "wrought 6063 reference cube")
    m.add("cube", box(-size / 2, -size / 2, 0, size / 2, size / 2, size).edges().chamfer(0.2), "d3_ref")
    return m


PLATE = dict(d=170.0, t=15.0, rows=4, cols=5, pitch=22.0, support=1.5)


def plate_positions(p=None) -> list:
    """[(label, x, y)] of the cubes on the plate (label A1.. by row and column, A at the front)."""
    p = p or PLATE
    out = []
    for r in range(p["rows"]):
        for c in range(p["cols"]):
            out.append((f"{'ABCD'[r]}{c + 1}", (c - (p["cols"] - 1) / 2) * p["pitch"],
                        (r - (p["rows"] - 1) / 2) * p["pitch"]))
    return out


def build_plate(with_cubes: bool = True, skip=()) -> Model:
    """The build plate (170 mm, as SOP 02's Aconity MIDI) with a 4 x 5 grid of 5 mm cubes on 1.5 mm supports."""
    p = PLATE
    m = Model("build_plate", "build plate with 5 mm cubes")
    m.add("plate", cyl(p["d"], p["t"]), "d3_plate")
    if with_cubes:
        for lab, x, y in plate_positions():
            if lab in skip:
                continue
            m.add(f"supports {lab}", box(x - 2.4, y - 2.4, p["t"], x + 2.4, y + 2.4, p["t"] + p["support"]), "d3_cube_cut")
            m.add(f"cube {lab}", box(x - CUBE / 2, y - CUBE / 2, p["t"] + p["support"], x + CUBE / 2, y + CUBE / 2,
                                     p["t"] + p["support"] + CUBE), "d3_cube")
    return m


def plate_strip() -> Model:
    """A strip cut from the plate (22 x 8 x 10 mm) with one cube on its supports on the +x face: as clamped in the
    saw's vise, the build direction along +x. Origin at the strip's +x face centre (the plate's top surface)."""
    m = Model("plate_strip", "plate strip with a cube")
    m.add("strip", box(-8.0, -11.0, -5.0, 0.0, 11.0, 5.0), "d3_plate")
    m.add("supports", box(0.0, -2.4, -2.4, PLATE["support"], 2.4, 2.4), "d3_cube_cut")
    return m


def strip_cube() -> Model:
    """The cube of plate_strip(), lying on its side (build direction +x), with 0.4 mm of support stub left on it."""
    m = Model("strip_cube", "cut cube")
    s = PLATE["support"]
    m.add("cube", box(s, -CUBE / 2, -CUBE / 2, s + CUBE, CUBE / 2, CUBE / 2), "d3_cube")
    m.add("stub", box(s - 0.4, -2.4, -2.4, s, 2.4, 2.4), "d3_cube_cut")
    return m


def tweezers() -> Model:
    """Stainless tweezers, 120 mm: the tips at the origin, pointing -x, the joint at +x; the tips 1.2 mm apart."""
    m = Model("tweezers", "stainless tweezers, 120 mm")
    for sy in (-1, 1):
        leg = cq.Workplane("XY").polyline([(0.0, sy * 0.6), (40.0, sy * 1.2), (110.0, sy * 4.5), (120.0, sy * 1.5),
                                           (120.0, sy * 0.6), (110.0, sy * 3.3), (40.0, sy * 0.7),
                                           (0.0, sy * 0.4)]).close().extrude(2.2).translate((0, 0, -1.1))
        m.add(f"leg {sy:+d}", leg, "d3_steel")
    m.add("joint", box(116, -1.6, -1.2, 124, 1.6, 1.2), "d3_steel")
    return m


def brush() -> Model:
    """A fine artist's brush (size 0): the bristle tip at the origin, the handle along +x."""
    m = Model("brush", "fine brush")
    m.add("bristles", cq.Workplane("YZ").circle(0.3).workplane(offset=9.0).circle(1.3).loft(), "d3_hair")
    m.add("ferrule", _xcyl(2.8, 14.0, x=9.0), "d3_steel")
    m.add("handle", cq.Workplane("YZ").circle(1.6).workplane(offset=90.0).circle(2.6).loft().translate((23.0, 0, 0)),
          "d3_wood")
    return m


def dropper_bottle() -> Model:
    m = Model("dropper", "30 mL dropper bottle of wetting agent")
    m.add("bottle", rbox(30, 30, 62, 6).edges(">Z").fillet(5), "d3_pe")
    m.add("neck", cyl(14, 8, z=62), "d3_pe")
    m.add("dropper tip", cq.Workplane("XY").circle(6.0).workplane(offset=18).circle(1.5).loft().translate((0, 0, 70)),
          "d3_pe")
    m.add("label", box(-15.3, -10, 14, -15.0, 10, 44), "d3_paper")
    return m


def water_bottle() -> Model:
    m = Model("water_btl", "250 mL bottle of distilled water")
    m.add("bottle", cyl(70, 118).edges(">Z").fillet(14), "d3_beaker")
    m.add("water", cyl(66, 100, z=2), "d3_water")
    m.add("neck", cyl(34, 14, z=118), "d3_beaker")
    m.add("cap", cyl(38, 18, z=128), "d3_cap_blue")
    m.add("label", tube(71, 70, 36, z=40).cut(box(-40, 0, 30, 40, 40, 90)), "d3_paper")
    return m


def thermometer_digital() -> Model:
    """A digital probe thermometer (0.1 C), lying on the bench: body along -x, the probe's tip at +x."""
    m = Model("thermo_dig", "digital thermometer, 0.1 C")
    m.add("body", rbox(70, 34, 16, 8, x=-35), "d3_white")
    m.add("display", box(-58, -12, 16, -22, 12, 16.6), "d3_display")
    m.add("probe", _xcyl(3.5, 110, x=0, z=8), "d3_steel")
    return m


def beaker_small(liquid: bool = True) -> Model:
    """A 50 mL beaker (42 x 60 mm), with ethanol to 30 mm."""
    m = Model("beaker50", "50 mL beaker")
    m.add("beaker", tube(42, 39.6, 60).union(cyl(42, 1.5)), "d3_beaker")
    if liquid:
        m.add("ethanol", cyl(39.2, 28, z=1.5), "d3_ethanol")
    return m


def al_dish() -> Model:
    m = Model("al_dish", "aluminium weighing dish, 57 mm")
    outer = cq.Workplane("XY").circle(24.0).workplane(offset=14.0).circle(28.5).loft()
    inner = cq.Workplane("XY").circle(23.6).workplane(offset=14.2).circle(28.1).loft().translate((0, 0, 0.4))
    m.add("dish", outer.cut(inner), "d3_al_dish")
    return m


def wipes_box() -> Model:
    m = Model("wipes", "box of lint-free wipes")
    m.add("box", box(-60, -110 / 2, 0, 60, 110 / 2, 60), "d3_white")
    m.add("slot", box(-30, -6, 59.6, 30, 6, 60.4), "d3_dark")
    m.add("wipe", cq.Workplane("XZ").polyline([(-22, 60), (22, 60), (14, 92), (-14, 88)]).close().extrude(0.6),
          "d3_paper")
    return m


def cube_tray() -> Model:
    """A 4 x 5 tray of wells (12 mm pitch), one per plate position, labelled on the rim."""
    m = Model("cube_tray", "labelled tray of wells")
    t = box(-36, -30, 0, 36, 30, 8)
    for r in range(4):
        for c in range(5):
            t = t.cut(box(-30 + 12 * c - 4.5, -18 + 12 * r - 4.5, 3, -30 + 12 * c + 4.5, -18 + 12 * r + 4.5, 9))
    m.add("tray", t, "d3_white")
    m.add("label strip", box(-36, -30.6, 1, 36, -30, 7), "d3_paper")
    return m


def sic_paper() -> Model:
    m = Model("sic", "320-grit SiC paper on a glass plate")
    m.add("glass", box(-70, -50, 0, 70, 50, 5), "d3_beaker")
    m.add("paper", box(-65, -45, 5, 65, 45, 5.4), "d3_sic")
    return m


def section_mount() -> Model:
    """A 32 mm mount with an XZ section of a cube (5 x 5 mm) in it, polished face up."""
    m = Model("mount", "mounted XZ section")
    m.add("mount", cyl(31.75, 20).cut(box(-2.5, -2.5, 19.6, 2.5, 2.5, 21)), "mount")
    m.add("section", box(-2.5, -2.5, 15.0, 2.5, 2.5, 20.0), "d3_cube_cut")
    return m


REGISTRY = {
    "density_balance": density_balance,
    "ultrasonic_bath": ultrasonic_bath,
    "drying_oven": drying_oven,
    "he_pycnometer": he_pycnometer,
}
