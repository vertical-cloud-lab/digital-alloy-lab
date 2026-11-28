"""Models for SOP 02 (single tracks, #262): the LECO VC50 precision saw, the LPBF build area at the plate, and the
etching props for the fume hood.

    import stage as S
    inst, ents = S.get("precision_saw")        # LECO VC50 Vari/Cut low-speed diamond saw
    inst, ents = S.get("lpbf_chamber")         # the build area at the plate (Aconity MIDI's 170 mm platform)
    inst, ents = S.get("lpbf_exterior")        # the Aconity MIDI itself, byu-vcl's model, for a context shot

Frame, as in byu-vcl's ``instruments.py``: x to the right, y away from you when you face the front, z up from the
bench, origin at the centre of the footprint, millimetres. Every published figure and its source is in ``SPECS``;
figures read off photos are marked as estimates there. Registration: ``ANCHORS``/``FREE``/``CHECKS`` (fit.py).
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
    "vc_grey": (0.80, 0.80, 0.78, 1.0, 0.20),          # the VC50's light warm-grey sheet metal (LECO's photo, 2026)
    "vc_panel": (0.56, 0.59, 0.57, 1.0, 0.20),         # its darker grey-green front panel
    "vc_meter": (0.95, 0.95, 0.92, 1.0, 0.30),         # the tachometer's dial face
    "vc_meter_band": (0.50, 0.70, 0.52, 1.0, 0.20),    # the dial's green bands
    "vc_button": (0.93, 0.93, 0.91, 1.0, 0.30),        # POWER / START / STOP
    "green_glass": (0.50, 0.78, 0.66, 0.42, 0.85),     # the green-tinted side window of the blade guard
    "clear_cover": (0.86, 0.90, 0.92, 0.22, 0.90),     # the clear acrylic cover over the arm
    "blade_core": (0.78, 0.56, 0.42, 1.0, 0.60),       # the copper-coloured blade core
    "blade_rim": (0.40, 0.36, 0.33, 1.0, 0.30),        # the diamond rim
    "cut_oil": (0.78, 0.62, 0.30, 0.55, 0.60),         # cutting oil / coolant in the tank
    "perf": (0.70, 0.71, 0.73, 1.0, 0.55),             # the perforated strainer
    # LPBF build area
    "plate_6061": (0.74, 0.75, 0.77, 1.0, 0.55),       # a ground 6061 plate
    "plate_cu": (0.78, 0.50, 0.36, 1.0, 0.55),
    "lpbf_powder": (0.55, 0.56, 0.58, 1.0, 0.03),      # grey Al powder, one layer
    "track_al": (0.86, 0.87, 0.88, 1.0, 0.80),         # a solidified track: brighter than the powder
    "track_hot": (0.95, 0.45, 0.12, 1.0, 0.10),        # the melt pool, dull orange
    "laser_beam": (0.95, 0.35, 0.20, 0.30, 0.0),       # the beam cone, faint (1070 nm is invisible; drawn faint)
    "chamber_wall": (0.78, 0.79, 0.80, 1.0, 0.35),
    "chamber_floor": (0.66, 0.67, 0.69, 1.0, 0.45),
    "recoater_blade": (0.30, 0.31, 0.33, 1.0, 0.40),
    "gas_arrow": (0.40, 0.55, 0.72, 0.45, 0.0),
    "denuded": (0.70, 0.71, 0.73, 1.0, 0.45),
    # etching props
    "hdpe_white": (0.94, 0.94, 0.91, 1.0, 0.15),
    "hdpe_amber": (0.66, 0.42, 0.18, 0.85, 0.40),
    "ptfe_white": (0.96, 0.96, 0.94, 1.0, 0.10),
    "keller": (0.90, 0.92, 0.85, 0.45, 0.70),           # Keller's reagent, colourless
    "hf_label": (0.98, 0.84, 0.10, 1.0, 0.10),         # a yellow hazard label
    "neoprene": (0.10, 0.10, 0.11, 1.0, 0.25),         # HF-rated gloves (neoprene/butyl), black
    "face_shield": (0.85, 0.92, 0.95, 0.30, 0.90),
    "gel_tube": (0.95, 0.95, 0.95, 1.0, 0.30),
    "gel_band": (0.15, 0.45, 0.80, 1.0, 0.30),
    "ethanol_btl": (0.92, 0.95, 0.97, 0.55, 0.60),
    "water_btl": (0.85, 0.92, 0.97, 0.45, 0.60),
    "dryer_body": (0.20, 0.21, 0.23, 1.0, 0.35),
    "tweezer_pp": (0.93, 0.93, 0.90, 1.0, 0.20),
    "aps_btl": (0.90, 0.88, 0.70, 0.75, 0.40),
}

SPECS: dict = {}
ANCHORS: dict = {}
FREE: dict = {}
CHECKS: dict = {}


# ===================================================================================================== precision saw
# LECO VC50 Vari/Cut, a low-speed (0-500 rpm) precision diamond saw. LECO's brochure (form 200-952, 7/26-REV12,
# https://www.leco.com/wp-content/uploads/documents/brochures/200-952-VC50.pdf): 13 in H x 17 in W x 18 in D (330 x 432
# x 457 mm), 52 lb (24 kg); a 5 in (127 mm) x 0.014 in (0.36 mm) diamond blade on a 0.5 in arbor; 0-500 rpm (50-650
# surface ft/min shown on a tachometer); a precision micrometer for the section's position; a sliding weight on the
# arm for the load; a vise for samples up to 1.5 in (38 mm); automatic shut-off. Layout from LECO's product photos
# (https://www.leco.com/instrument/vc50-precision-wafering-saw/, 2026) and two videos of the machine (refs/precision_saw):
# a control box on the left (POWER / START / STOP, the tachometer, SPEED SELECT) and, on the right, a lower base with
# the coolant tank as a drawer (knob) under the blade guard; the blade in the y-z plane on a spindle along x from the
# control box, its +x face behind a green window in the guard; the arm pivots at the back of the guard and carries the
# vise over the blade; the micrometer comes out of the right side at the back; a clear cover hinged at the back closes
# over the arm.
# fitted to LECO's photo and a front frame of the instructional video (refs/precision_saw/fit.json, 2026-11-28); D and
# the micrometer's reach are held at the published envelope
VC50 = dict(W=364.2, D=440.0, plinth=17.5, ctrl_w=252.0, ctrl_h=170.4, deck=105.0, gy0=56.7, gd=173.4, gh=108.1,
            blade_d=127.0, blade_t=0.36, blade_yk=0.50, blade_dz=22.0, piv_dz=160.0, mic_dz=70.8, mic_len=76.0,
            mic_y=133.0, cover_h=116.9, meter_x=0.70, meter_z=0.60)

SPECS["precision_saw"] = {
    "model": "LECO VC50 Vari/Cut precision diamond saw (low speed)",
    "published": {
        "H x W x D": ("330 x 432 x 457 mm (13 x 17 x 18 in)", "LECO brochure 200-952 REV12 (2026)"),
        "mass": ("24 kg (52 lb)", "LECO brochure 200-952"),
        "blade": ("5 in (127 mm) x 0.014 in (0.36 mm) diamond, 0.5 in arbor; 4 in optional", "LECO brochure 200-952"),
        "speed": ("0-500 rpm; 50-650 SFM with the 5 in blade", "LECO brochure 200-952"),
        "vise": ("samples up to 1.5 in (38 mm)", "LECO brochure 200-952; leco.com VC50 page"),
        "drive": ("1/15 hp, 50 W motor; 200 W supply", "LECO brochure 200-952"),
        "load": ("sliding counterweight on the arm", "leco.com VC50 page: 'cutting force (through a sliding counterweight)'"),
    },
    "estimates": {
        "chassis W 356": "432 overall less the micrometer's ~76 mm out of the right side (front video frame, BkWFULiNy-k 1:02)",
        "D 440": "457 overall less the knobs; fitted (fit.json)",
        "control box 247 W x 168 H, deck 102, plinth 17": "front frame BkWFULiNy-k 1:02 scaled to W 356; fitted",
        "guard, arm, cover, micrometer positions": "LECO's product photo and frames of BkWFULiNy-k / WqqdOjjtBu0; fitted",
    },
}


def _vc50(p) -> dict:
    W, D = p["W"], p["D"]
    yf = -D / 2
    xr0 = -W / 2 + p["ctrl_w"]                       # the right base's left side (control box's right side)
    gx0, gx1 = xr0 + 4.0, W / 2 - 4.0                # the blade guard spans the right base
    gy0 = yf + p["gy0"]
    gy1 = gy0 + p["gd"]
    gz0, gz1 = p["deck"], p["deck"] + p["gh"]
    bx = gx0 + 0.42 * (gx1 - gx0)                    # the blade's plane (x)
    by = gy0 + p["blade_yk"] * p["gd"]               # its centre
    bz = p["deck"] + p["blade_dz"]
    R = p["blade_d"] / 2
    mic = np.array([W / 2, yf + p["D"] - p["mic_y"], p["deck"] + p["mic_dz"]])
    piv = np.array([bx + 14.0, mic[1] - 6.0, p["deck"] + p["piv_dz"]])
    return dict(W=W, D=D, yf=yf, xr0=xr0, gx0=gx0, gx1=gx1, gy0=gy0, gy1=gy1, gz0=gz0, gz1=gz1, bx=bx, by=by, bz=bz,
                R=R, piv=piv, mic=mic, top=bz + R)


def saw_points(p=None) -> dict:
    """Where things are in the saw's own frame (mm), for scripts: the blade's centre and top, the vise jaw centre
    with the arm up (v=0), the pivot, the coolant level, the drawer's knob, the cover's hinge."""
    p = p or VC50
    g = _vc50(p)
    return dict(blade_centre=(g["bx"], g["by"], g["bz"]), blade_top=(g["bx"], g["by"], g["top"]),
                strip=(g["bx"] - 2.5, g["by"], g["top"] + 5.0 + 3.2), pivot=tuple(g["piv"]),
                oil_level=p["deck"] - 18.0,
                drawer_knob=(g["xr0"] + (g["W"] / 2 - g["xr0"]) / 2, g["yf"] - 22.0,
                             p["plinth"] + 0.55 * (p["deck"] - p["plinth"])),
                cover_hinge=(g["bx"], g["gy1"], g["gz1"]), guard=(g["gx0"], g["gx1"], g["gy0"], g["gy1"], g["gz0"],
                                                                  g["gz1"]))


def precision_saw_anchors(p, pose=None) -> dict:
    g = _vc50(p)
    W, yf, pl, ch, dk = g["W"], g["yf"], p["plinth"], p["ctrl_h"], p["deck"]
    yb = yf + p["D"]
    xr0 = g["xr0"]
    a = {"plinth front left": (-W / 2, yf, 0.0), "plinth front right": (W / 2, yf, 0.0),
         "plinth back right": (W / 2, yb, 0.0),
         "ctrl front top left": (-W / 2, yf, ch), "ctrl front top right": (xr0, yf, ch),
         "ctrl front bottom left": (-W / 2, yf, pl), "ctrl back top left": (-W / 2, yb, ch),
         "base front top right": (W / 2, yf, dk), "base back top right": (W / 2, yb, dk),
         "base front top left": (xr0, yf, dk),
         "guard front top left": (g["gx0"], g["gy0"], g["gz1"]), "guard front top right": (g["gx1"], g["gy0"], g["gz1"]),
         "guard front bottom right": (g["gx1"], g["gy0"], g["gz0"]),
         "guard back top right": (g["gx1"], g["gy1"], g["gz1"]),
         "mic end": (g["mic"][0] + p["mic_len"], g["mic"][1], g["mic"][2]),
         "mic root": (g["mic"][0], g["mic"][1], g["mic"][2])}
    mx = -W / 2 + p["meter_x"] * p["ctrl_w"]
    mz = pl + p["meter_z"] * (ch - pl)
    a.update({"meter tl": (mx - 40, yf - 3, mz + 25), "meter tr": (mx + 40, yf - 3, mz + 25),
              "meter bl": (mx - 40, yf - 3, mz - 37), "meter br": (mx + 40, yf - 3, mz - 37),
              "speed knob": (mx, yf - 12, pl + 0.20 * (ch - pl)),
              "drawer knob": (xr0 + (W / 2 - xr0) / 2, yf - 14, pl + 0.55 * (dk - pl))})
    return a


def precision_saw() -> "Instrument":
    """LECO VC50 Vari/Cut low-speed precision diamond saw (330 x 432 x 457 mm, LECO brochure 200-952).

    Pieces: ``body`` (chassis, control box with POWER/START/STOP, tachometer and SPEED SELECT knob, the blade guard
    with its green window and perforated strainer, the micrometer barrel, the spindle); ``wheel`` (the 127 mm diamond
    blade with its flanges and knurled nut); ``tank`` (the coolant drawer: front, knob, stainless trough and the oil);
    ``carriage`` (the arm's pivot bracket and the micrometer's thimble, indexed along x); ``arm`` (the arm, the vise
    with its knurled screw); ``weight`` (the sliding weight on the arm); ``specimen`` (a 10 x 22 x 6 mm Al strip in the
    vise, a prop: fade it in or out); ``slice`` (the section that falls off, a prop); ``cover`` (the clear cover).

    Joints: ``cover`` hinge about x at the guard's back top edge, 0 closed -> 1 open (105 deg up and back);
    ``arm`` hinge about the pivot (the feed): 0 = the piece 5 mm over the blade, 1 = 16 mm lower (through the 10 mm
    piece; values below 0 lift the arm, above 1 go deeper); ``wheel`` spin about the spindle (x), 0 -> 1 = 12 turns
    (scale the step time for rpm); ``carriage`` slide along -x, 0 -> 1 = 25 mm (the micrometer's travel: 0 puts the
    cut 0.5 mm from the strip's target plane); ``weight`` slide along the arm,
    0 -> 1 = 80 mm toward the vise (more load); ``tank`` slide toward you (-y), 0 -> 1 = 150 mm (the drawer out).
    ``saw_points()`` gives the blade top, the vise and the drawer knob in this frame.
    """
    p = VC50
    g = _vc50(p)
    W, D, yf, pl, ch, dk = g["W"], g["D"], g["yf"], p["plinth"], p["ctrl_h"], p["deck"]
    yb = yf + D
    xr0 = g["xr0"]
    inst = Instrument("precision_saw", "Precision sectioning saw", "LECO VC50 Vari/Cut (low-speed diamond saw)",
                      (432.0, 457.0, 330.0),
                      "LECO brochure 200-952 REV12 (2026) for the envelope, blade and speed; LECO's product photos and "
                      "two videos of the machine for the layout (refs/precision_saw)")
    body = _piece(inst, "body")
    # the plinth, the control box and the right base
    body.add("plinth", box(-W / 2, yf, 0, W / 2, yb, pl).edges("|Z").fillet(3), "vc_grey")
    body.add("control box", box(-W / 2, yf, pl, xr0, yb, ch).edges(">Z").fillet(3), "vc_grey")
    gxa, gxb, gya, gyb = xr0 + 4.0 + 1.5, W / 2 - 4.0 - 4.0, yf + p["gy0"] + 1.5, yf + p["gy0"] + p["gd"] - 1.5
    base = box(xr0, yf + 8, pl, W / 2, yb, dk).edges(">Z and >X").fillet(2)
    base = base.cut(box(xr0 + 3, yf + 6, pl + 4, W / 2 - 3, gyb, dk - 2))          # the drawer's cavity
    base = base.cut(box(gxa, gya, dk - 3, gxb, gyb, dk + 1))                      # open under the guard
    body.add("right base", base, "vc_grey")
    # the front panel, inset, with its four screws
    px0, px1, pz0, pz1 = -W / 2 + 4, xr0 - 4, pl + 3, ch - 4
    body.add("front panel", box(px0, yf - 1.2, pz0, px1, yf + 0.5, pz1), "vc_panel")
    for sx in (px0 + 8, px1 - 8):
        for sz in (pz0 + 8, pz1 - 8):
            body.add("panel screw", _ycyl(5, 1.4, x=sx, y=yf - 2.4, z=sz), "inst_black")
    # POWER / START / STOP, the tachometer, SPEED SELECT
    bz_ = pl + 0.72 * (ch - pl)
    for i in range(3):
        bx_ = -W / 2 + 0.13 * p["ctrl_w"] + i * 27
        body.add("button", box(bx_, yf - 4, bz_, bx_ + 24, yf - 1, bz_ + 17), "vc_button")
    mx = -W / 2 + p["meter_x"] * p["ctrl_w"]
    mz = pl + p["meter_z"] * (ch - pl)
    body.add("meter case", box(mx - 40, yf - 3, mz - 37, mx + 40, yf - 1, mz + 25), "inst_black")
    body.add("meter dial", box(mx - 36, yf - 3.6, mz - 8, mx + 36, yf - 2.6, mz + 22), "vc_meter")
    body.add("meter band", _ycyl(1, 1, x=mx, y=yf - 3.9, z=mz) if False else
             box(mx - 28, yf - 3.9, mz + 6, mx + 28, yf - 3.5, mz + 11), "vc_meter_band")
    kz = pl + 0.20 * (ch - pl)
    body.add("speed knob", _ycyl(24, 10, x=mx, y=yf - 11, z=kz).union(_ycyl(14, 4, x=mx, y=yf - 15, z=kz)),
             "inst_black")
    body.add("speed knob cap", _ycyl(10, 1, x=mx, y=yf - 16, z=kz), "chrome")
    body.add("LECO label", box(-W / 2 + 0.18 * p["ctrl_w"], yf - 1.6, pl + 0.42 * (ch - pl),
                               -W / 2 + 0.40 * p["ctrl_w"], yf - 1.2, pl + 0.50 * (ch - pl)), "vc_button")
    # the blade guard: three grey walls (front, left, back) and the green window on the right; the strainer
    gx0, gx1, gy0, gy1, gz0, gz1 = g["gx0"], g["gx1"], g["gy0"], g["gy1"], g["gz0"], g["gz1"]
    t = 1.5
    guard = (box(gx0, gy0, gz0, gx1, gy0 + t, gz1)                        # front wall
             .union(box(gx0, gy0, gz0, gx0 + t, gy1, gz1))               # left wall
             .union(box(gx0, gy1 - t, gz0, gx1, gy1, gz1 - 30)))         # back wall (lower: the arm passes)
    # the notch in the left wall where the spindle comes through, and in the front wall's top for the arm
    guard = guard.cut(_xcyl(34, 6, x=gx0 - 2, y=g["by"], z=g["bz"]))
    body.add("blade guard", guard, "vc_grey")
    body.add("green window", box(gx1 - 4, gy0 + t, gz0 + 2, gx1 - 1, gy1 - t, gz1 - 4), "green_glass")
    body.add("window frame", box(gx1 - 4, gy0, gz1 - 4, gx1, gy1, gz1).union(box(gx1 - 4, gy1 - 3, gz0, gx1, gy1, gz1)),
             "vc_grey")
    # the strainer at deck level, slotted for the blade
    strainer = box(gx0 + t, gy0 + t, gz0 - 1.0, gx1 - 4, gy1 - t, gz0).cut(
        box(g["bx"] - 4, g["by"] - g["R"] - 3, gz0 - 2, g["bx"] + 4, g["by"] + g["R"] + 3, gz0 + 1))
    body.add("strainer", strainer, "perf")
    # the spindle housing through the left wall, from the control box
    body.add("spindle boss", _xcyl(30, 14, x=gx0 + t, y=g["by"], z=g["bz"]).cut(
        _xcyl(17, 20, x=gx0 - 2, y=g["by"], z=g["bz"])), "vc_grey")
    # the casting at the back of the base that carries the arm's pivot and the micrometer, out of its right side
    mic = g["mic"]
    piv = g["piv"]
    cy0, cy1 = gy1 + 2, min(yb - 6, mic[1] + 30)
    body.add("pivot casting", box(gx0 + 20, cy0, dk, W / 2, cy1, mic[2] + 26).edges("|X and >Z").fillet(10), "vc_grey")
    fm = p["mic_len"] / 76.0
    body.add("micrometer ring", _xcyl(42, 12 * fm, x=W / 2, y=mic[1], z=mic[2]), "inst_black")
    body.add("micrometer sleeve", _xcyl(24, 24 * fm, x=W / 2 + 10 * fm, y=mic[1], z=mic[2]), "chrome")
    # a little knob on the base's right side (the arm-lift knob in the videos)
    body.add("side knob", _xcyl(14, 9, x=W / 2, y=yf + 0.62 * D, z=pl + 0.55 * (dk - pl)), "chrome")
    # ------------------------------------------------------------------------------------------- the coolant tank
    tank = _piece(inst, "tank")
    tx0, tx1 = xr0 + 6, W / 2 - 6
    tank.add("drawer front", box(xr0 + 2, yf, pl + 3, W / 2 - 2, yf + 8, dk - 3), "vc_grey")
    kx = (xr0 + W / 2) / 2
    tank.add("drawer knob", _ycyl(18, 12, x=kx, y=yf - 12, z=pl + 0.55 * (dk - pl)).union(
        _ycyl(10, 3, x=kx, y=yf - 15, z=pl + 0.55 * (dk - pl))), "inst_black")
    trough = (box(tx0, yf + 8, pl + 8, tx1, gy1 - 4, dk - 6)
              .cut(box(tx0 + 2, yf + 10, pl + 10, tx1 - 2, gy1 - 6, dk)))
    tank.add("trough", trough, "stainless")
    tank.add("cutting oil", box(tx0 + 2.5, yf + 10.5, pl + 10.5, tx1 - 2.5, gy1 - 6.5, dk - 18), "cut_oil")
    # ------------------------------------------------------------------------------------------- the blade
    wheel = _piece(inst, "wheel")
    bx, by, bz, R = g["bx"], g["by"], g["bz"], g["R"]
    bt = max(p["blade_t"], 0.36)
    wheel.add("blade core", _xcyl(2 * R - 6, bt, x=bx - bt / 2, y=by, z=bz), "blade_core")
    wheel.add("diamond rim", _xcyl(2 * R, bt + 0.1, x=bx - bt / 2 - 0.05, y=by, z=bz).cut(
        _xcyl(2 * R - 6, bt + 2, x=bx - bt / 2 - 1, y=by, z=bz)), "blade_rim")
    wheel.add("spindle", _xcyl(16, bx - bt / 2 - 5 - (g["gx0"] - 2), x=g["gx0"] - 2, y=by, z=bz), "steel")
    wheel.add("flange in", _xcyl(46, 5, x=bx - bt / 2 - 5, y=by, z=bz), "stainless")
    wheel.add("flange out", _xcyl(46, 5, x=bx + bt / 2, y=by, z=bz), "stainless")
    nut = _xcyl(30, 24, x=bx + bt / 2 + 5, y=by, z=bz)
    wheel.add("knurled nut", nut, "stainless")
    wheel.add("index mark", box(bx + bt / 2 + 5, by - 1.5, bz + 15.5, bx + bt / 2 + 29, by + 1.5, bz + 16.5),
              "inst_black")
    # ------------------------------------------------------------------------------------------- the arm
    car = _piece(inst, "carriage")
    ax_ = g["bx"] - 13.9                               # the arm's centre line (x), beside the blade
    car.add("pivot bracket", box(ax_ + 11, piv[1] - 16, mic[2] + 26, ax_ + 50, piv[1] + 16, piv[2] + 14), "vc_grey")
    car.add("pivot shaft", _xcyl(10, 64, x=ax_ - 12, y=piv[1], z=piv[2]), "steel")
    f = p["mic_len"] / 76.0
    car.add("micrometer thimble", _xcyl(26, 32 * f, x=W / 2 + 34 * f, y=mic[1], z=mic[2]), "chrome")
    car.add("micrometer ratchet", _xcyl(12, 10 * f, x=W / 2 + 66 * f, y=mic[1], z=mic[2]), "chrome")
    arm = _piece(inst, "arm")
    # the vise clamps the strip by its front and back ends (screw along y, knurled knob at the front); its jaws stay on
    # the -x side of the blade, and the strip sticks out 2.5 mm past them, so the blade takes a sliver off its +x side
    # and leaves the section face on the clamped piece (#243 section 3: cut 0.5 mm from the target plane)
    sx0, sx1 = bx - 7.5, bx + 2.5                      # the strip: 10 mm across the blade (x)
    sy0, sy1 = by - 11.0, by + 11.0                    # 22 mm along it (y): nine tracks at 2 mm pitch
    s_z0 = g["top"] + 5.0                              # its underside, 5 mm over the blade with the arm up
    s_z1 = s_z0 + 10.0                                 # cut ~10 mm below the tracks (#243 section 3)
    jx0, jx1 = bx - 26.0, bx - 1.8
    arm_z = piv[2] - 7.0                               # the arm bar's underside: the bar runs level through the pivot
    vtop = s_z1 + 8.0
    arm.add("vise fixed jaw", box(jx0, sy1, s_z0 + 1.0, jx1, sy1 + 10, arm_z), "stainless")
    arm.add("vise moving jaw", box(jx0, sy0 - 10, s_z0 + 1.0, jx1, sy0, vtop), "stainless")
    arm.add("vise column", box(jx0, sy0 - 12, vtop, jx1, sy0 + 6, arm_z), "stainless")
    arm.add("vise screw block", box(jx0, sy0 - 30, s_z0 - 1, jx1, sy0 - 12, s_z0 + 12), "stainless")
    arm.add("vise screw", _ycyl(10, 22, x=(jx0 + jx1) / 2, y=sy0 - 30, z=s_z0 + 5), "steel")
    arm.add("vise knob", _ycyl(24, 12, x=(jx0 + jx1) / 2, y=sy0 - 42, z=s_z0 + 5), "stainless")
    arm.add("brass insert", _xcyl(14, 10, x=jx0 - 10, y=sy0 - 22, z=s_z0 + 5), "brass")
    # the arm: a 20 x 14 mm bar from the pivot forward over the vise
    ax = (jx0 + jx1) / 2
    ay0 = sy0 - 14.0
    bore = _xcyl(11, 40, x=ax - 20, y=piv[1], z=piv[2])
    arm.add("arm bar", box(ax - 10, ay0, arm_z, ax + 10, piv[1] + 12, arm_z + 14).cut(bore), "stainless")
    arm.add("arm boss", _xcyl(22, 20, x=ax - 10, y=piv[1], z=piv[2]).cut(bore), "stainless")
    arm.add("weight rail", box(ax - 4, ay0 + 30, arm_z + 14, ax + 4, piv[1] - 20, arm_z + 18), "steel")
    wt = _piece(inst, "weight")
    wy = ay0 + 95.0                                    # back toward the pivot; it slides forward for more load
    wt.add("sliding weight", box(ax - 14, wy, arm_z + 18, ax + 14, wy + 34, arm_z + 40), "stainless")
    wt.add("weight screw", _xcyl(8, 8, x=ax + 14, y=wy + 17, z=arm_z + 30), "steel")
    spec = _piece(inst, "specimen")
    spec.add("Al strip", box(sx0, sy0, s_z0, bx - 0.2, sy1, s_z1), "sample")
    slc = _piece(inst, "slice")
    slc.add("sliver", box(bx + 0.2, sy0, s_z0, sx1, sy1, s_z1), "sample")
    # ------------------------------------------------------------------------------------------- the cover
    cov = _piece(inst, "cover")
    cx0, cx1 = gx0 - 2, gx1 + 2
    cz0, cz1 = gz1, gz1 + p["cover_h"]
    lean = 34.0                                        # the front face leans back by this much at the top (photos)
    cb = cy1 + 2                                       # the cover's back, behind the pivot casting
    ct = mic[2] + 27.0                                 # the casting's top (+1 mm): the cover's back half sits on it
    prof = [(gy0 - 2, cz0), (cy0 - 1, cz0), (cy0 - 1, ct), (cb, ct), (cb, cz1), (gy0 - 2 + lean, cz1)]
    shell = cq.Workplane("YZ").polyline(prof).close().extrude(cx1 - cx0).translate((cx0, 0, 0))
    inner = cq.Workplane("YZ").polyline([(gy0 + 1, cz0 - 1), (cy0 + 2, cz0 - 1), (cy0 + 2, ct - 1), (cb - 3, ct - 1),
                                         (cb - 3, cz1 - 3),
                                         (gy0 + 1 + lean, cz1 - 3)]).close().extrude(cx1 - cx0 - 6).translate(
        (cx0 + 3, 0, 0))
    # the step where the back half sits on the casting is only on the side walls: the arm passes under the cover
    shell = shell.cut(inner).cut(box(cx0 + 3, cy0 - 4, ct - 3, cx1 - 3, cy0 + 5, cz0 + 1))
    cov.add("clear cover", shell, "clear_cover")
    cov.add("cover top", box(cx0, gy0 - 2 + lean, cz1 - 2, cx1, cb, cz1 + 1), "vc_grey")
    cov.add("cover front strip", box(cx0 + 12, gy0 - 5, cz0 - 30, cx1 - 12, gy0 - 2, cz0 + 4), "stainless")
    # the arm's travel: the vise moves on a circle about the pivot; 24 mm down at the vise
    rv = math.hypot(piv[1] - by, piv[2] - s_z0)        # the strip's radius about the pivot
    feed_deg = math.degrees(16.0 / rv)
    hinge = (0.0, cb, ct)
    inst.joints = {
        "cover": Joint("hinge", axis=(1, 0, 0), pivot=hinge, deg=-105.0),
        "carriage": Joint("slide", vec=(-25.0, 0, 0)),
        "arm": Joint("hinge", parent="carriage", axis=(1, 0, 0), pivot=tuple(piv), deg=feed_deg),
        "weight": Joint("slide", parent="arm", vec=(0, -80.0, 0)),
        "specimen": Joint("fade", parent="arm", v0=1.0),
        "slice": Joint("fade", parent="arm", v0=1.0),
        "wheel": Joint("spin", axis=(1, 0, 0), pivot=(bx, by, bz), deg=-360.0 * 12),
        "tank": Joint("slide", vec=(0, -150.0, 0)),
    }
    inst.actions = [
        ("The LECO VC50: a 127 mm diamond blade at 0-500 rpm, the arm and its vise over it.", 1.5, {}),
        ("Cover up; the strip in the vise.", 1.5, {"cover": (0.0, 1.0)}),
        ("Cover down; the blade turns; the arm feeds the strip through.", 4.0,
         {"cover": (1.0, 0.0), "wheel": (0.0, 1.0), "arm": (0.0, 1.0)}),
    ]
    inst.labels = [("5 in (127 mm) diamond blade", (bx, by - R, bz), (0.12, 0.70)),
                   ("micrometer", (W / 2 + 70, mic[1], mic[2]), (0.86, 0.30)),
                   ("coolant tank (drawer)", (kx, yf - 12, pl + 40), (0.80, 0.82))]
    inst.anchors = precision_saw_anchors(p)
    inst.cam = (0.8, -1.6, 0.9)
    return inst


ANCHORS["precision_saw"] = (VC50, precision_saw_anchors)
# D (440: the published 457 less the knobs) and the micrometer's reach (76: the published 432 less the chassis) are
# held at the published envelope; no view pins the depth down (fit.json, notes/precision_saw.md)
FREE["precision_saw"] = ["W", "plinth", "ctrl_w", "ctrl_h", "deck", "gy0", "gd", "gh", "mic_dz", "mic_y",
                         "meter_x", "meter_z"]
CHECKS["precision_saw"] = lambda p: [p["ctrl_h"] - p["deck"] - 20, p["deck"] - p["plinth"] - 40,
                                     p["D"] - p["gy0"] - p["gd"] - 60, p["W"] - p["ctrl_w"] - 80,
                                     p["gd"] - p["blade_d"] - 20]


# ===================================================================================================== LPBF build area
# The build area at the plate, for SOP 02's tracks. The first Al tracks come from Utah's Aconity MIDI (P1, Dec 2-3):
# its build platform is 170 mm across (Aconity's configurator data, byu-vcl lab_models/equipment.py; DAL PR #169), and
# Utah's plate is 6061 (DAL PR #169). Aconity publishes no drawing of the chamber's inside, so the floor, the bores,
# the recoater and the gas manifolds are laid out as in a typical bottom-up-feed LPBF chamber (a supply cylinder in
# front of the build cylinder, an overflow behind it, gas across the plate), and are marked as such in SPECS. The
# plate, the layer and the tracks are drawn at their real sizes: tracks 12 mm long at 2 mm pitch in rows of 18 (two
# groups of nine, 10 mm apart), mid-lengths on one line (#243 section 4).
LPBF = dict(plate_d=170.0, plate_t=15.0, bore=171.0, supply_y=-215.0, overflow_y=150.0, floor_x=290.0,
            floor_y0=-330.0, floor_y1=235.0, wall_h=230.0, layer=0.040, blade_len=240.0)

SPECS["lpbf_chamber"] = {
    "model": "LPBF build area at the plate (Aconity MIDI's 170 mm platform; layout typical, not published)",
    "published": {
        "build platform": ("170 mm diameter x 200 mm build height", "Aconity configurator data via byu-vcl equipment.py"),
        "plate": ("6061, Utah's", "DAL PR #169"),
        "tracks": ("12 mm long, 2 mm pitch, rows of 18 (two groups of nine 10 mm apart)", "DAL PR #243 section 4"),
        "layer": ("one powder layer, 30-50 um (the machine's standard layer)", "SOP 02; DAL PR #243 section 4"),
        "beam": ("1/e2 radius r0 from the machine's beam profile; 40 um is the analysis demo's value",
                 "melt_pool_calibration.py DEMO_MATERIAL"),
    },
    "estimates": {
        "floor, bores, overflow, recoater, gas manifolds": "a typical bottom-up-feed chamber; Aconity publishes no inside drawing",
        "plate thickness 15 mm": "byu-vcl alloy_models.PLATE (an assumption there too)",
    },
}


def lpbf_chamber() -> "Instrument":
    """The LPBF build area at the plate (frame: origin on the build cylinder's axis at the chamber floor, z up).

    Pieces: ``body`` (the chamber floor with the build and supply bores and the overflow slot, the back and side
    walls, the gas inlet manifold on the -x wall and the outlet duct on the +x wall); ``plate`` (the 170 x 15 mm 6061
    plate on its piston); ``supply`` (the powder in the supply cylinder, in front at y = -215); ``recoater`` (the
    blade in its holder, across x); ``gas`` (flow arrows from the inlet to the outlet, +x); ``beam`` (the laser cone
    from above onto the plate centre, a prop: move it with a mover).
    Joints: ``plate`` slide in z (0 -> 1 = 15 mm up, out of the bore); ``recoater`` slide in y (0 at y = -300, behind
    the supply; 1 at y = +190, past the overflow); ``supply`` slide in z (0 -> 1 = 0.2 mm up: one layer's dose);
    ``gas`` fade.
    """
    p = LPBF
    inst = Instrument("lpbf_chamber", "LPBF build area", "Aconity MIDI build platform (170 mm), layout typical",
                      (2 * p["floor_x"], p["floor_y1"] - p["floor_y0"], p["wall_h"]),
                      "plate and tracks at real size (DAL PR #169, #243); the chamber's inside is a typical layout")
    body = _piece(inst, "body")
    fx, fy0, fy1 = p["floor_x"], p["floor_y0"], p["floor_y1"]
    floor = box(-fx, fy0, -20, fx, fy1, 0)
    floor = floor.cut(cyl(p["bore"], 30, z=-25)).cut(cyl(p["bore"], 30, y=p["supply_y"], z=-25))
    floor = floor.cut(box(-p["bore"] / 2 - 10, p["overflow_y"], -25, p["bore"] / 2 + 10, p["overflow_y"] + 30, 5))
    body.add("chamber floor", floor, "chamber_floor")
    body.add("build cylinder", tube(p["bore"] + 24, p["bore"], 180, z=-200), "stainless")
    body.add("supply cylinder", tube(p["bore"] + 24, p["bore"], 180, y=p["supply_y"], z=-200), "stainless")
    body.add("overflow chute", box(-p["bore"] / 2 - 10, p["overflow_y"], -120, p["bore"] / 2 + 10, p["overflow_y"] + 30, -20)
             .cut(box(-p["bore"] / 2 - 8, p["overflow_y"] + 2, -118, p["bore"] / 2 + 8, p["overflow_y"] + 28, -19)),
             "stainless")
    body.add("back wall", box(-fx, fy1, -20, fx, fy1 + 12, p["wall_h"]), "chamber_wall")
    # the gas inlet: a manifold along the -x wall with a row of slots; the outlet: a wide duct mouth on the +x wall
    body.add("left wall", box(-fx - 12, fy0, -20, -fx, fy1 + 12, 60), "chamber_wall")
    body.add("right wall", box(fx, fy0, -20, fx + 12, fy1 + 12, 60), "chamber_wall")
    inlet = box(-fx, -110, 8, -fx + 26, 110, 48)
    for k in range(11):
        inlet = inlet.cut(box(-fx + 20, -100 + 20 * k, 18, -fx + 30, -92 + 20 * k, 38))
    body.add("gas inlet manifold", inlet, "stainless")
    outlet = box(fx - 34, -120, 4, fx, 120, 70).cut(box(fx - 40, -105, 12, fx - 6, 105, 58))
    body.add("gas outlet duct", outlet, "stainless")
    body.add("outlet grille", box(fx - 10, -105, 12, fx - 8, 105, 58), "inst_dark")
    plate = _piece(inst, "plate")
    plate.add("6061 build plate", cyl(p["plate_d"], p["plate_t"], z=-p["plate_t"]), "plate_6061")
    plate.add("build piston", cyl(p["bore"] - 2, 40, z=-p["plate_t"] - 40), "steel")
    supply = _piece(inst, "supply")
    supply.add("supply powder", cyl(p["bore"] - 1, 40, y=p["supply_y"], z=-40.2), "lpbf_powder")
    rec = _piece(inst, "recoater")
    L = p["blade_len"]
    y0 = -300.0
    rec.add("recoater holder", box(-L / 2 - 20, y0 - 14, 6, L / 2 + 20, y0 + 14, 40), "stainless")
    rec.add("recoater blade", box(-L / 2, y0 + 8, 0.06, L / 2, y0 + 11, 12), "recoater_blade")
    rec.add("recoater riser", box(L / 2 + 20, y0 - 10, 6, L / 2 + 40, y0 + 10, 92), "stainless")
    rec.add("recoater arm", box(L / 2 + 40, y0 - 10, 78, fx - 2, y0 + 10, 92), "stainless")     # over the outlet duct
    gas = _piece(inst, "gas")
    for i, yy in enumerate((-95.0, 95.0)):
        for j, x0 in enumerate((-250.0, -70.0, 110.0)):
            shaft = box(x0, yy - 1.0, 28.0, x0 + 90, yy + 1.0, 30.0)
            head = (cq.Workplane("XY").polyline([(x0 + 90, yy - 6), (x0 + 106, yy), (x0 + 90, yy + 6)]).close()
                    .extrude(2).translate((0, 0, 28.0)))
            gas.add(f"gas arrow {i}{j}", shaft.union(head), "gas_arrow")
    beam = _piece(inst, "beam")
    beam.add("beam cone", cq.Workplane("XY").circle(0.06).workplane(offset=220).circle(6.0).loft(), "laser_beam")
    inst.joints = {
        "plate": Joint("slide", vec=(0, 0, 15.0)),
        "supply": Joint("slide", vec=(0, 0, 0.2)),
        "recoater": Joint("slide", vec=(0, 490.0, 0)),
        "gas": Joint("fade", v0=0.0),
        "beam": Joint("fade", v0=0.0),
    }
    inst.props = ("beam", "gas")
    inst.cam = (0.6, -1.6, 1.4)
    return inst


def lpbf_exterior() -> "Instrument":
    """byu-vcl's Aconity MIDI (lab_models.equipment.aconity_midi: 2450 x 1500 x 2320 mm, its 170 mm platform; layout
    from Aconity's configurator and front photos) as one ``body`` piece, for a context shot. No joints."""
    import equipment
    m = equipment.aconity_midi()
    inst = Instrument("lpbf_exterior", "Metal LPBF printer", "Aconity3D AconityMIDI (byu-vcl's model)",
                      (2450.0, 1500.0, 2320.0), m.source)
    inst.pieces["body"] = m
    return inst


# ===================================================================================================== etching props
def etch_props() -> dict:
    """{name: Model} for the hood: Keller's reagent bottle (HF), a PTFE dish, plastic tweezers, a wash bottle of water,
    an ethanol wash bottle, calcium gluconate gel, a hot-air dryer, ammonium persulfate (for Cu), a face shield, and a
    pair of HF-rated gloves laid out. Each stands on z = 0, centred on (0, 0); real sizes (catalogue-typical)."""
    out = {}
    m = Model("keller", "Keller's reagent, 250 mL HDPE bottle")
    m.add("bottle", cyl(62, 120).edges(">Z").fillet(10), "hdpe_white")
    m.add("neck", cyl(28, 16, z=120), "hdpe_white")
    m.add("cap", cyl(34, 18, z=134), "pp_black")
    m.add("liquid", cyl(58, 90, z=2), "keller")
    m.add("label", tube(62.6, 61.8, 50, z=30), "paper")
    m.add("HF band", tube(63.0, 62.4, 12, z=84), "hf_label")
    out["keller"] = m
    m = Model("ptfe_dish", "PTFE dish, 90 mm")
    m.add("dish", tube(90, 82, 25).union(cyl(90, 3)), "ptfe_white")
    m.add("etchant", cyl(82, 10, z=3), "keller")
    out["ptfe_dish"] = m
    m = Model("rinse_dish", "PP dish of water, 90 mm")
    m.add("dish", tube(90, 82, 25).union(cyl(90, 3)), "pp_white")
    m.add("water", cyl(82, 14, z=3), "water")
    out["rinse_dish"] = m
    m = Model("tweezers_pp", "plastic tweezers, 120 mm")
    for s in (-1, 1):
        m.add(f"leg {s}", box(0, s * 1.5 - 1.0 if s > 0 else -2.5, 0, 120, s * 1.5 + 1.0 if s > 0 else -0.5, 3),
              "tweezer_pp")
    m.add("joint", box(0, -3.0, 0, 16, 3.0, 3), "tweezer_pp")
    out["tweezers_pp"] = m
    m = Model("wash_water", "500 mL wash bottle, water")
    m.add("bottle", cyl(70, 150).edges(">Z").fillet(14), "water_btl")
    m.add("cap", cyl(32, 14, z=150), "pp_white")
    m.add("spout", hose([(0, 0, 164), (0, 0, 190), (30, 0, 205), (55, 0, 200)], 5), "pp_white")
    out["wash_water"] = m
    m = Model("wash_ethanol", "500 mL wash bottle, ethanol")
    m.add("bottle", cyl(70, 150).edges(">Z").fillet(14), "ethanol_btl")
    m.add("cap", cyl(32, 14, z=150), "pp_red" if False else "paint_red")
    m.add("spout", hose([(0, 0, 164), (0, 0, 190), (30, 0, 205), (55, 0, 200)], 5), "pp_white")
    out["wash_ethanol"] = m
    m = Model("ca_gluconate", "2.5 % calcium gluconate gel, 25 g tube")
    m.add("tube", cq.Workplane("YZ").circle(14).extrude(110).translate((-55, 0, 14)), "gel_tube")
    m.add("crimp", box(-62, -15, 12, -55, 15, 16), "gel_tube")
    m.add("cap", _xcyl(16, 16, x=55, y=0, z=14), "gel_band")
    m.add("band", tube(28.8, 28, 30, z=0).rotate((0, 0, 0), (0, 1, 0), 90).translate((-10, 0, 14)), "gel_band")
    out["ca_gluconate"] = m
    m = Model("hot_air_dryer", "hot-air dryer")
    m.add("body", _xcyl(60, 150, x=-60, y=0, z=150), "dryer_body")
    m.add("nozzle", _xcyl(40, 40, x=90, y=0, z=150), "dryer_body")
    m.add("handle", box(-20, -15, 0, 15, 15, 130), "dryer_body")
    m.add("foot", box(-45, -40, 0, 40, 40, 8), "dryer_body")
    out["hot_air_dryer"] = m
    m = Model("aps", "ammonium persulfate, 500 g")
    m.add("jar", cyl(80, 110), "aps_btl")
    m.add("cap", cyl(70, 20, z=110), "pp_white")
    m.add("label", tube(80.6, 79.8, 45, z=30), "paper")
    out["aps"] = m
    m = Model("face_shield", "face shield on its headband")
    m.add("visor", tube(230, 226, 200, z=0).cut(box(-130, -130, -1, 130, 10, 230)), "face_shield")
    m.add("band", tube(232, 222, 22, z=200), "pp_black")
    out["face_shield"] = m
    return out


# ===================================================================================================== registry
REGISTRY = {
    "precision_saw": precision_saw,
    "lpbf_chamber": lpbf_chamber,
    "lpbf_exterior": lpbf_exterior,
}
