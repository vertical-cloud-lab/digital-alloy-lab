"""Models for SOP 05 (composition by ICP-OES and O/N/H by inert gas fusion, #262, PR #263).

Each instrument follows byu-vcl's pattern (vl/instruments.py): an ``Instrument`` of named pieces (``body`` stays put;
doors, electrodes, probes, samples move) with a ``Joint`` per moving piece, its envelope from the maker's published
W x D x H (``SPECS``, every figure with its source; estimates say so), its layout read off the maker's photos and
video frames, and ``ANCHORS`` / ``FREE`` / ``CHECKS`` so ``fit.py`` can register it to those frames (refs/<key>/).

* ``icp_oes``: Agilent 5900 ICP-OES (synchronous vertical dual view) with its SPS 4 autosampler beside it; the sample
  introduction bay (peristaltic pump, concentric nebulizer, cyclonic spray chamber), the vertical torch and load coil
  in the torch compartment behind the black door, the radial and axial light paths, the plasma.
* ``onh_analyzer``: LECO ONH836 inert-gas-fusion analyzer: the loading head and its sample drop, the electrode
  (impulse) furnace with the graphite crucible on the lower electrode, which drops to open, and the detection (NDIR
  cells for CO and CO2, a thermal-conductivity cell for N2 and H2) inside the cabinet.
* ``microwave_digester``: CEM MARS 6 with its turntable of PTFE-lined vessels.
* ``heat_sealer``: a hand impulse heat sealer, for bags flushed with argon.
* ``ship_box``: a corrugated shipper with a foam insert and a hinged lid.
* ``bench_drill``: a small bench drill press, for dry-cut chips (no coolant) from printed cubes and feedstock.

Small props (vials, bags, the argon nozzle, labels, the chain-of-custody form, the CRM bottle, crucibles, capsules,
baskets, digestion vessels) are Models from the ``prop_*`` functions, for ``stage.props``.

Frame: x right, y away from the front, z up from the surface it stands on, mm, origin at the centre of the footprint.
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

MATERIALS = {
    "ag_white": (0.93, 0.94, 0.94, 1.0, 0.20),        # Agilent's white panels
    "ag_glass": (0.07, 0.08, 0.10, 1.0, 0.55),        # the 5900's black glass door
    "ag_navy": (0.13, 0.16, 0.24, 1.0, 0.25),         # the sample introduction bay's dark navy panels
    "ag_blue": (0.10, 0.55, 0.82, 1.0, 0.25),         # the Agilent badge
    "ag_cover": (0.84, 0.90, 0.93, 0.22, 0.85),       # the SPS 4's clear cover
    "quartz": (0.88, 0.93, 0.96, 0.35, 0.90),         # torch, spray chamber, nebulizer
    "pump_tube": (0.95, 0.93, 0.80, 0.85, 0.20),      # PVC pump tubing (tab colours aside)
    "icp_plasma": (0.93, 0.89, 0.97, 0.55, 0.00),     # a pale argon plasma (drawn muted, not as a glow)
    "icp_core": (0.97, 0.95, 0.99, 0.80, 0.00),
    "light_path": (0.98, 0.88, 0.45, 0.55, 0.00),     # the radial and axial views, drawn as thin pale beams
    "leco_white": (0.90, 0.91, 0.91, 1.0, 0.20),      # LECO's light grey-white cabinet
    "leco_grey": (0.70, 0.72, 0.73, 1.0, 0.30),
    "leco_screen": (0.08, 0.10, 0.14, 1.0, 0.50),
    "leco_ui": (0.80, 0.66, 0.30, 1.0, 0.10),         # Cornerstone's gold-on-dark rows
    "graphite_cr": (0.16, 0.16, 0.17, 1.0, 0.25),     # graphite crucible
    "tin": (0.78, 0.79, 0.80, 1.0, 0.60),
    "nickel": (0.66, 0.66, 0.62, 1.0, 0.60),
    "cell_body": (0.55, 0.57, 0.60, 1.0, 0.45),       # detector cells
    "cell_gold": (0.85, 0.70, 0.35, 1.0, 0.60),       # gold-plated IR cell bores
    "reagent": (0.88, 0.86, 0.80, 0.60, 0.30),        # reagent tubes (glass with granules)
    "cem_grey": (0.86, 0.87, 0.88, 1.0, 0.25),        # MARS 6 body
    "cem_dark": (0.20, 0.21, 0.23, 1.0, 0.30),
    "tfm": (0.94, 0.94, 0.92, 1.0, 0.15),             # PTFE/TFM vessel liners
    "vessel_sleeve": (0.55, 0.48, 0.38, 1.0, 0.25),   # composite sleeves
    "acid": (0.92, 0.95, 0.80, 0.45, 0.60),           # digest (pale)
    "hdpe": (0.95, 0.95, 0.93, 0.80, 0.20),           # HDPE vial body (translucent white)
    "pp_cap": (0.95, 0.95, 0.94, 1.0, 0.15),
    "poly_bag": (0.90, 0.92, 0.94, 0.30, 0.70),       # 4-mil poly bag
    "kraft": (0.70, 0.56, 0.38, 1.0, 0.05),
    "foam": (0.22, 0.22, 0.24, 1.0, 0.05),
    "label_w": (0.98, 0.98, 0.96, 1.0, 0.05),
    "label_ink": (0.15, 0.15, 0.18, 1.0, 0.05),
    "amber": (0.55, 0.32, 0.10, 0.75, 0.70),
    "chips": (0.74, 0.75, 0.77, 1.0, 0.55),
    "al_part": (0.70, 0.71, 0.73, 1.0, 0.45),         # a printed Al cube (matte as-built)
    "build_plate": (0.62, 0.64, 0.66, 1.0, 0.50),
    "sealer_blue": (0.30, 0.45, 0.70, 1.0, 0.25),
    "drill_green": (0.25, 0.40, 0.30, 1.0, 0.30),
    "cast_grey": (0.42, 0.44, 0.46, 1.0, 0.30),
    "hose_black": (0.12, 0.12, 0.13, 1.0, 0.20),
    "regulator": (0.78, 0.78, 0.76, 1.0, 0.60),
    "clip_board": (0.55, 0.40, 0.25, 1.0, 0.15),
    "gauge_face": (0.97, 0.97, 0.95, 1.0, 0.10),
}

SPECS: dict = {}
ANCHORS: dict = {}
FREE: dict = {}
CHECKS: dict = {}


def _zcyl_at(d, h, x, y, z):
    return cyl(d, h, x=x, y=y, z=z)


# ==================================================================================================== ICP-OES
# Agilent 5900 ICP-OES (synchronous vertical dual view, SVDV) with an Agilent SPS 4 autosampler at its right, as in
# ASU's Core Research Facilities video "Agilent 5900 ICP-OES" (youtu.be/VkMy6cp2-Y0, 0:04-0:06 the whole instrument
# from the front left; 0:09-0:16 the torch compartment door opened; 0:18-0:26 the sample introduction bay; 0:27-0:33
# the SPS 4). Look: a white upper housing the full width of the instrument, most of its front a black glass door
# (the torch compartment behind its left part); the Agilent badge top left. Under it, set back on the left, a white
# pedestal, and to its right the open sample introduction bay with dark navy walls: the peristaltic pump low on the
# right, the cyclonic spray chamber high on the left with the concentric nebulizer entering it from the side, the
# vertical torch above it, through the compartment's floor. The proportions are fractions of the front read off the
# 0:05.6 frame, fitted with register.py (refs/icp_oes/); W x D x H are Agilent's (SPECS).
ICP = dict(W=887.0, D=740.0, H=625.0, split_k=0.40, ped_x0=0.19, ped_x1=0.39, bay_x1=0.97, bay_d=260.0,
           win_x0=0.12, win_x1=0.91, win_z0=0.50, win_z1=0.84, torch_k=0.52, sps_gap=60.0, sps_W=600.0,
           sps_D=363.0, sps_H=510.0, top_r=22.0)
SPECS["icp_oes"] = {
    "model": "Agilent 5900 ICP-OES (SVDV) with SPS 4 autosampler",
    "size": "W x D x H filled in from Agilent's published figures (see notes/icp_oes.md); until checked: estimate",
    "sps4": "SPS 4: 600 x 363 x 510 mm, 15 kg (Agilent 7800/7900 ICP-MS site preparation checklist G8400-90020, "
            "the autosampler table; byu-vcl notes/icpms.md A1)",
    "look": "ASU Core Research Facilities video youtu.be/VkMy6cp2-Y0 (0:04-0:33)",
    "estimates": "the front's split, window, pedestal and bay fractions are read off the 0:05.6 frame and fitted; "
                 "the bay's depth (260 mm), the torch's x, the pump head (90 mm) and spray chamber are estimates",
}


def _icp(p) -> dict:
    W, D, H = p["W"], p["D"], p["H"]
    x0 = -W / 2
    zs = p["split_k"] * H
    g = dict(W=W, D=D, H=H, x0=x0, yf=-D / 2, zs=zs,
             ped0=x0 + p["ped_x0"] * W, ped1=x0 + p["ped_x1"] * W, bay1=x0 + p["bay_x1"] * W,
             wx0=x0 + p["win_x0"] * W, wx1=x0 + p["win_x1"] * W, wz0=p["win_z0"] * H, wz1=p["win_z1"] * H,
             tx=x0 + p["torch_k"] * W)
    g["ty"] = g["yf"] + 150.0                                   # the torch's axis, 150 mm behind the front
    g["sps_x"] = W / 2 + p["sps_gap"] + p["sps_W"] / 2
    g["sps_y"] = g["yf"] + p["sps_D"] / 2
    g["tz0"] = zs - 80.0                                        # the torch's foot, in the bay's top
    g["pz"] = g["tz0"] + 172.0                                  # the plasma's foot, in the torch's mouth
    g["rz"] = g["pz"] + 50.0                                    # the radial view's height
    g["sz"] = g["tz0"] - 75.0                                   # the spray chamber's foot
    g["px"], g["pzp"] = g["bay1"] - 95.0, 135.0                 # the pump head's centre
    sx, sy, sw, sd, sh = g["sps_x"], g["sps_y"], p["sps_W"], p["sps_D"], p["sps_H"]
    g["rack_x0"] = sx - sw / 2 + 80.0                           # rack 0's centre
    g["probe"] = (sx + sw / 2 - 50.0, sy - 20.0)                # the probe parks over the rinse station
    g["probe_tip"] = sh - 300.0                                 # its tip at rest, 25 mm over the tubes
    g["tgt"] = (g["rack_x0"], sy - sd / 2 + 45.0 + 30.0 * 3)    # the tube it samples (rack 0, middle column, row 3)
    g["tube_floor"] = 67.5
    return g


def icp_anchors(p, pose=None) -> dict:
    g = _icp(p)
    W, H, yf, x0, zs = g["W"], g["H"], g["yf"], g["x0"], g["zs"]
    x1 = W / 2
    a = {"top front left": (x0, yf, H - p["top_r"] * 0.3), "top front right": (x1, yf, H - p["top_r"] * 0.3),
         "upper bottom left": (x0, yf, zs), "upper bottom right": (x1, yf, zs),
         "window tl": (g["wx0"], yf, g["wz1"]), "window tr": (g["wx1"], yf, g["wz1"]),
         "window bl": (g["wx0"], yf, g["wz0"]), "window br": (g["wx1"], yf, g["wz0"]),
         "pedestal foot left": (g["ped0"], yf + 15.0, 0.0), "pedestal top left": (g["ped0"], yf + 15.0, zs),
         "bay foot right": (g["bay1"], yf, 0.0),
         "top back left": (x0, -yf, H - p["top_r"] * 0.3),
         "badge left": (g["wx0"], yf, H - 0.085 * H)}
    sx, sy, sw, sd, sh = g["sps_x"], g["sps_y"], p["sps_W"], p["sps_D"], p["sps_H"]
    a.update({"sps base front left": (sx - sw / 2, sy - sd / 2, 0.0), "sps base front right": (sx + sw / 2, sy - sd / 2, 0.0),
              "sps cover top front left": (sx - sw / 2, sy - sd / 2, sh)})
    return a


def icp_oes() -> Instrument:
    p = ICP
    g = _icp(p)
    W, D, H, yf, x0, zs = g["W"], g["D"], g["H"], g["yf"], g["x0"], g["zs"]
    inst = Instrument("icp_oes", "ICP-OES with autosampler", "Agilent 5900 ICP-OES (SVDV) + SPS 4", (W, D, H),
                      "Agilent's published W x D x H; look from ASU's 5900 video (youtu.be/VkMy6cp2-Y0), fitted "
                      "with register.py; SPS 4 from Agilent's site preparation checklist",
                      props=("sps", "sps_arm", "sps_probe", "tubes", "plasma", "beam", "sample", "flow", "glow"))
    body = _piece(inst, "body")
    shell = _piece(inst, "shell")
    # --- the upper housing: white, full width; a shell (front, top, sides, back) around the torch compartment and
    # the optics, so it can be made see-through for the cutaway
    t = 6.0
    up = rbox(W, D, H - zs, 18.0, x=0, y=0, z=zs).edges(">Z and <Y").fillet(p["top_r"])
    inner = box(x0 + t, yf + t, zs + t, W / 2 - t, -yf - t, H - t)
    win = box(g["wx0"], yf - 2, g["wz0"], g["wx1"], yf + t + 2, g["wz1"])
    shell.add("upper housing", up.cut(inner).cut(win), "ag_white")
    shell.add("badge", box(g["wx0"], yf - 1.0, H - 0.105 * H, g["wx0"] + 0.15 * W, yf, H - 0.065 * H), "ag_blue")
    shell.add("model label", box(g["wx0"] + 0.18 * W, yf - 0.6, H - 0.095 * H, g["wx0"] + 0.28 * W, yf, H - 0.080 * H),
              "inst_grey")
    # --- the lower body: the white pedestal (gas box, power) and the bay's frame; set back on the left
    lower = box(g["ped0"], yf + 15.0, 0, W / 2, -yf, zs)
    bay = box(g["ped1"], yf - 1, 30.0, g["bay1"], yf + p["bay_d"], zs + 1)
    body.add("lower body", lower.cut(bay), "ag_white")
    body.add("bay walls", box(g["ped1"], yf + p["bay_d"] - 6, 30.0, g["bay1"], yf + p["bay_d"], zs)
             .union(box(g["ped1"], yf + 15, 30.0, g["ped1"] + 6, yf + p["bay_d"], zs))
             .union(box(g["bay1"] - 6, yf, 30.0, g["bay1"], yf + p["bay_d"], zs))
             .union(box(g["ped1"], yf, 30.0, g["bay1"], yf + p["bay_d"], 36.0)), "ag_navy")
    body.add("power LED", box(g["ped0"] + 0.45 * (g["ped1"] - g["ped0"]) - 4, yf + 14.0, 14.0,
                              g["ped0"] + 0.45 * (g["ped1"] - g["ped0"]) + 4, yf + 15.0, 18.0), "led_green")
    body.add("feet", box(g["ped0"] + 10, yf + 30, -0.0, W / 2 - 10, -yf - 20, 1.0), "inst_dark")
    # --- the torch compartment (behind the door's left part): stainless walls, the torch box floor
    tx, ty = g["tx"], g["ty"]
    cx0, cx1 = g["wx0"] + 10, tx + 150.0
    comp = box(cx0, yf + t, zs + t, cx1, yf + 300, H - 60).cut(box(cx0 + 3, yf + t - 1, zs + t + 3, cx1 - 3, yf + 297,
                                                                     H - 63))
    body.add("torch compartment", comp, "stainless")
    body.add("optics housing", box(cx1 + 10, yf + 40, zs + 40, W / 2 - 30, -yf - 40, H - 50), "inst_dark")
    body.add("radial view port", _xcyl(40, 12, x=cx1 - 12, y=ty, z=zs + 175), "inst_black")
    body.add("axial interface", cyl(70, 22, x=tx, y=ty, z=zs + 280).union(cyl(30, 40, x=tx, y=ty, z=zs + 302)),
             "copper")
    # --- the torch: quartz tubes, the load coil, standing through the compartment's floor
    tz0 = g["tz0"]
    torch = _piece(inst, "torch")
    torch.add("torch outer tube", tube(20, 18, 150, x=tx, y=ty, z=tz0 + 60), "quartz")
    torch.add("torch inner tubes", tube(13, 11.5, 120, x=tx, y=ty, z=tz0 + 60).union(
        tube(4, 2, 115, x=tx, y=ty, z=tz0 + 60)), "quartz")
    torch.add("torch base", cyl(36, 60, x=tx, y=ty, z=tz0), "inst_black")
    coil = None
    for k in range(3):
        c = tube(34, 28, 4.5, x=tx, y=ty, z=tz0 + 175 + 7.0 * k)
        coil = c if coil is None else coil.union(c)
    torch.add("load coil", coil.union(box(tx + 14, ty - 3, tz0 + 175, tx + 60, ty + 3, tz0 + 197)), "copper")
    plasma = _piece(inst, "plasma")
    pz = g["pz"]
    plasma.add("plasma", cq.Workplane("XY").ellipse(9.0, 9.0).workplane(offset=34).ellipse(8.5, 8.5).loft()
               .union(cq.Workplane("XY").sphere(8.6).translate((0, 0, 34))).union(
                   cq.Workplane("XY").workplane(offset=40).circle(7.5).workplane(offset=26).circle(2.0).loft())
               .translate((tx, ty, pz)), "icp_plasma")
    plasma.add("plasma core", cyl(6.0, 30.0, x=tx, y=ty, z=pz + 4), "icp_core")
    beam = _piece(inst, "beam")
    # radial: sideways from the plasma's normal analytical zone to the port; axial: up the plasma's axis to the
    # interface, then over to the optics (the 5900's DSC combines the two)
    rz = g["rz"]
    beam.add("radial view", hose([(tx + 6, ty, rz), (cx1 - 14, ty, rz)], 5.0), "light_path")
    beam.add("axial view", hose([(tx, ty, pz + 70), (tx, ty, zs + 300)], 5.0), "light_path")
    beam.add("to optics", hose([(cx1 - 14, ty, rz), (cx1 + 60, ty, rz), (cx1 + 60, ty, zs + 330)], 4.0)
             .union(hose([(tx, ty, zs + 330), (cx1 + 60, ty, zs + 330), (cx1 + 200, ty + 60, zs + 330)], 4.0)),
             "light_path")
    # --- the sample introduction: spray chamber under the torch, nebulizer from the right, pump low right
    sz = g["sz"]
    body.add("spray chamber", cyl(46, 70, x=tx, y=ty, z=sz).union(
        cq.Workplane("XY").circle(23).workplane(offset=-30).circle(6).loft().translate((tx, ty, sz))), "quartz")
    body.add("chamber to torch", tube(12, 9, 6, x=tx, y=ty, z=sz + 70), "quartz")
    body.add("nebulizer", _xcyl(9, 90, x=tx + 18, y=ty - 14, z=sz + 52), "quartz")
    body.add("nebulizer gas line", hose([(tx + 108, ty - 14, sz + 52), (tx + 140, ty - 14, sz + 70),
                                         (tx + 160, ty + 60, zs - 20)], 4.0), "pump_tube")
    body.add("chamber drain", hose([(tx, ty, sz - 30), (tx, ty, 80.0), (tx + 20, ty + 20, 40.0)], 6.0), "pump_tube")
    body.add("spray chamber clamp", box(tx - 30, ty + 20, sz + 20, tx + 30, ty + 30, sz + 55), "inst_dark")
    px, pzp = g["px"], g["pzp"]
    body.add("pump body", box(px - 75, yf + 90, pzp - 70, px + 75, yf + p["bay_d"] - 6, pzp + 70), "inst_black")
    rotor = _piece(inst, "pump_rotor")
    head = _ycyl(92, 40, x=px, y=yf + 50, z=pzp)
    for k in range(8):
        a = 2 * math.pi * k / 8
        head = head.union(_ycyl(12, 42, x=px + 36 * math.cos(a), y=yf + 49, z=pzp + 36 * math.sin(a)))
    rotor.add("pump head", head, "inst_dark")
    rotor.add("pump rollers", _ycyl(14, 2, x=px, y=yf + 48, z=pzp), "stainless")
    body.add("pump clamps", box(px - 70, yf + 46, pzp + 50, px + 70, yf + 92, pzp + 62), "inst_grey")
    body.add("pump tubing", hose([(px - 70, yf + 60, pzp + 52), (px - 20, yf + 58, pzp + 50), (px + 40, yf + 58, pzp + 50),
                                  (px + 70, yf + 60, pzp + 52)], 3.0).union(
        hose([(px - 70, yf + 60, pzp + 52), (tx + 60, yf + 70, sz + 30), (tx + 108, ty - 14, sz + 52)], 2.5)), "pump_tube")
    # --- the door: the black glass front, hinged at its left edge
    door = _piece(inst, "door")
    door.add("door glass", box(g["wx0"], yf - 8, g["wz0"], g["wx1"], yf + 2, g["wz1"]), "ag_glass")
    door.add("door grip", box(g["wx1"] - 30, yf - 10, g["wz0"] + 10, g["wx1"] - 4, yf - 8, g["wz0"] + 16), "inst_grey")
    # --- the SPS 4 at the right
    sx, sy, sw, sd, sh = g["sps_x"], g["sps_y"], p["sps_W"], p["sps_D"], p["sps_H"]
    sps = _piece(inst, "sps")
    sps.add("SPS 4 base", rbox(sw, sd, 60, 10, x=sx, y=sy, z=0), "ag_white")
    sps.add("SPS 4 tray", box(sx - sw / 2 + 15, sy - sd / 2 + 15, 60, sx + sw / 2 - 90, sy + sd / 2 - 70, 66), "inst_light")
    sps.add("SPS 4 rinse station", rbox(60, 110, 70, 6, x=sx + sw / 2 - 50, y=sy - 20, z=60), "ag_white")
    sps.add("SPS 4 tower", box(sx + sw / 2 - 40, sy + sd / 2 - 60, 60, sx + sw / 2 - 5, sy + sd / 2 - 5, sh - 30), "ag_white")
    sps.add("SPS 4 beam", box(sx - sw / 2 + 10, sy + sd / 2 - 60, sh - 80, sx + sw / 2 - 5, sy + sd / 2 - 25, sh - 40),
            "ag_white")
    sps.add("SPS 4 badge", box(sx - 60, sy + sd / 2 - 61, sh - 70, sx + 20, sy + sd / 2 - 60, sh - 55), "ag_blue")
    cover = box(sx - sw / 2, sy - sd / 2, 60, sx + sw / 2, sy + sd / 2, sh).cut(
        box(sx - sw / 2 + 4, sy - sd / 2 + 4, 59, sx + sw / 2 - 4, sy + sd / 2 - 4, sh - 4))
    sps.add("SPS 4 cover", cover, "ag_cover")
    # racks: four racks of 50 mL tubes (3 x 7 each at 30 mm)
    tubes = _piece(inst, "tubes")
    rack_parts, tube_parts = None, None
    for r in range(4):
        cx = g["rack_x0"] + r * 112
        rk = box(cx - 50, sy - sd / 2 + 25, 60, cx + 50, sy + sd / 2 - 80, 96).cut(
            box(cx - 44, sy - sd / 2 + 31, 66, cx + 44, sy + sd / 2 - 86, 97))
        rack_parts = rk if rack_parts is None else rack_parts.union(rk)
        for i in range(3):
            for j in range(7):
                xx, yy = cx - 30 + 30 * i, sy - sd / 2 + 45 + 30 * j
                tb = tube(28, 26, 113, x=xx, y=yy, z=67.5).union(cyl(28, 1.5, x=xx, y=yy, z=66.0))
                tube_parts = tb if tube_parts is None else tube_parts.union(tb)
    sps.add("SPS 4 racks", rack_parts, "pp_white")
    tubes.add("sample tubes", tube_parts, "polypropylene")
    arm = _piece(inst, "sps_arm")
    ax0, ay0 = g["probe"]
    tip = g["probe_tip"]
    arm.add("SPS 4 carriage", box(ax0 - 22, sy + sd / 2 - 60, sh - 92, ax0 + 22, sy + sd / 2 - 26, sh - 30), "inst_light")
    arm.add("SPS 4 probe arm", box(ax0 - 10, ay0 - 60, sh - 62, ax0 + 10, sy + sd / 2 - 60, sh - 48), "ag_white")
    probe = _piece(inst, "sps_probe")
    probe.add("SPS 4 probe holder", box(ax0 - 9, ay0 - 9, tip + 150, ax0 + 9, ay0 + 9, sh - 62), "inst_dark")
    probe.add("SPS 4 probe", cyl(2.5, 150, x=ax0, y=ay0, z=tip), "stainless")
    tgt = g["tgt"]
    dip = tip - (g["tube_floor"] + 8.0)
    inst.joints = {
        "door": Joint("hinge", axis=(0, 0, 1), pivot=(g["wx0"], yf - 8, 0), deg=-100.0),
        "pump_rotor": Joint("spin", axis=(0, 1, 0), pivot=(px, 0, pzp), deg=-1440.0),
        "plasma": Joint("fade"), "beam": Joint("fade"),
        "sps_arm": Joint("slide", vec=(tgt[0] - ax0, 0.0, 0.0)),
        "sps_probe": Joint("path", path=((0, 0, 0), (0, tgt[1] - ay0, 0), (0, tgt[1] - ay0, -dip)), parent="sps_arm"),
    }
    inst.anchors = icp_anchors(p)
    inst.labels = [("Agilent 5900 ICP-OES", (x0, yf, H * 0.9), (0.10, 0.20)),
                   ("SPS 4 autosampler", (sx, sy - sd / 2, sh), (0.85, 0.20))]
    inst.notes = ["torch at x %.0f, y %.0f; spray chamber top z %.0f" % (tx, ty, sz + 70)]
    inst.cam = (0.6, -1.6, 0.7)
    return inst


def icp_geom() -> dict:
    return _icp(ICP)
ANCHORS["icp_oes"] = (ICP, icp_anchors)
FREE["icp_oes"] = ["split_k", "ped_x0", "ped_x1", "win_x0", "win_x1", "win_z0", "win_z1", "bay_x1"]
CHECKS["icp_oes"] = lambda p: [p["win_z0"] - p["split_k"] - 0.03, p["win_z1"] - p["win_z0"] - 0.15,
                               p["ped_x1"] - p["ped_x0"] - 0.08, p["bay_x1"] - p["ped_x1"] - 0.3,
                               0.99 - p["win_z1"], p["win_x1"] - p["win_x0"] - 0.5]


# ==================================================================================================== ONH836
# LECO ONH836 (oxygen, nitrogen, hydrogen by inert gas fusion), as in LECO's "ONH836 Series" video
# (youtu.be/W5IGSUMWQq8: renders at 0:13-0:29, the electrode at 1:31-1:35, the infrared cells at 1:37-1:55) and a
# dealer's demonstration (youtu.be/SJcUGXPb1Dw: the whole analyzer square-on at 0:34-1:57, the furnace at 2:02-3:30),
# and LECO's own talk-through (youtu.be/bmuEksg945g: the lower electrode with a graphite crucible, 0:18-0:27). Look: a
# light grey cabinet; on the front left a portrait touchscreen standing proud; on the right the furnace: the
# electrode housing ("LECO") with the loading head on top (a round black port, a black handle on its right), under it
# a lit bay with the lower electrode (a black cylinder, steel rim and crucible pedestal) that drops to open, the
# electrode cleaner's brush beside it on the left, and a rounded plinth below; a lid over the whole top.
ONH = dict(W=762.0, D=724.0, H=813.0, scr_x0=0.05, scr_x1=0.52, scr_z0=0.19, scr_z1=0.74, head_x0=0.55,
           head_x1=0.86, head_z0=0.53, head_z1=0.82, bay_z0=0.30, plinth_x1=0.88, head_proud=60.0, scr_proud=35.0,
           lid_h=30.0)
SPECS["onh_analyzer"] = {
    "model": "LECO ONH836 (oxygen/nitrogen/hydrogen by inert gas fusion)",
    "size": "W x D x H filled in from LECO's published figures (see notes/onh_analyzer.md); until checked: estimate",
    "look": "LECO 'ONH836 Series' video youtu.be/W5IGSUMWQq8 (renders 0:13-0:29); dealer video youtu.be/SJcUGXPb1Dw "
            "(0:34-3:30); LECO talk youtu.be/bmuEksg945g (0:18-0:27)",
    "estimates": "the front's screen, head and bay fractions are read off the frames and fitted; the lower "
                 "electrode's travel (70 mm), the crucible (12 mm bore x 22 mm OD x 25 mm, a standard graphite "
                 "crucible's size class) and the cells' sizes are estimates",
}


def _onh(p) -> dict:
    W, D, H = p["W"], p["D"], p["H"]
    x0, yf = -W / 2, -D / 2
    g = dict(W=W, D=D, H=H, x0=x0, yf=yf,
             sx0=x0 + p["scr_x0"] * W, sx1=x0 + p["scr_x1"] * W, sz0=p["scr_z0"] * H, sz1=p["scr_z1"] * H,
             hx0=x0 + p["head_x0"] * W, hx1=x0 + p["head_x1"] * W, hz0=p["head_z0"] * H, hz1=p["head_z1"] * H,
             bz0=p["bay_z0"] * H, px1=x0 + p["plinth_x1"] * W)
    g["yh"] = yf - p["head_proud"]                              # the electrode housing's front
    g["fx"] = 0.5 * (g["hx0"] + g["hx1"])                       # the furnace axis, under the loading head
    g["fy"] = g["yh"] + 90.0
    g["tip"] = g["hz0"] - 45.0                                  # the upper electrode's tip
    g["travel"] = 60.0                                          # the lower electrode's drop to open (estimate)
    g["cru_h"], g["ped_h"], g["body_h"] = 25.0, 12.0, 100.0
    g["ped_top"] = g["tip"] - g["cru_h"]                        # closed: the crucible clamped against the tip
    g["body_top"] = g["ped_top"] - g["ped_h"]
    g["cx"] = g["fx"] - 115.0                                   # the electrode cleaner, left of the furnace
    g["port"] = (g["fx"], g["fy"], g["hz1"] + 22.0)            # the loading head's sample port (its top)
    g["smp_z0"] = g["hz1"] + 4.0                                # the sample waits in the loading head
    return g


def onh_geom() -> dict:
    return _onh(ONH)


def onh_anchors(p, pose=None) -> dict:
    g = _onh(p)
    W, H, yf, x0 = g["W"], g["H"], g["yf"], g["x0"]
    yp = yf - p["scr_proud"]
    yh = g["yh"]
    a = {"screen tl": (g["sx0"], yp, g["sz1"]), "screen tr": (g["sx1"], yp, g["sz1"]),
         "screen bl": (g["sx0"], yp, g["sz0"]), "screen br": (g["sx1"], yp, g["sz0"]),
         "top front left": (x0, yf, H), "top front right": (W / 2, yf, H),
         "foot front left": (x0, yp, 0.0),
         "head top left": (g["hx0"], yh, g["hz1"]), "head top right": (g["hx1"], yh, g["hz1"]),
         "head bottom left": (g["hx0"], yh, g["hz0"]), "head bottom right": (g["hx1"], yh, g["hz0"]),
         "port": g["port"],
         "bay floor right": (g["px1"], yf - 40.0, g["bz0"]),
         "top back right": (W / 2, -yf, H)}
    return a


def onh_analyzer() -> Instrument:
    p = ONH
    g = _onh(p)
    W, D, H, x0, yf = g["W"], g["D"], g["H"], g["x0"], g["yf"]
    inst = Instrument("onh_analyzer", "Inert gas fusion O/N/H analyzer", "LECO ONH836", (W, D, H),
                      "LECO's published W x D x H; look from LECO's and a dealer's ONH836 videos, fitted with "
                      "register.py",
                      props=("crucible", "sample", "glow", "gas", "detect", "flow"))
    body = _piece(inst, "body")
    shell = _piece(inst, "shell")
    housing = _piece(inst, "housing")
    bay_x0 = g["hx0"] - 20
    t = 5.0
    fx, fy, yh, hz0, hz1, bz0 = g["fx"], g["fy"], g["yh"], g["hz0"], g["hz1"], g["bz0"]
    # the cabinet: a box, its furnace bay cut from the front right; a lid over the top
    cab = box(x0, yf, 15.0, W / 2, -yf, H - p["lid_h"])
    bay = box(bay_x0, yf - 1, bz0, W / 2 - 30, yf + 230, hz0 + 30)
    hollow = box(x0 + t, yf + t, 15 + t, W / 2 - t, -yf - t, H - p["lid_h"] - t)
    shell.add("cabinet", cab.cut(bay).cut(hollow), "leco_white")
    shell.add("lid", rbox(W + 10, D + 10, p["lid_h"], 12, x=0, y=0, z=H - p["lid_h"]).edges(">Z").fillet(8),
              "leco_white")
    body.add("bay back", box(bay_x0, yf + 225, bz0, W / 2 - 30, yf + 232, hz0 + 30), "label_w")
    well_d = 124.0
    floor = box(bay_x0, yf - 40, bz0 - 8, W / 2 - 30, yf + 230, bz0).cut(cyl(well_d, 20, x=fx, y=fy, z=bz0 - 10))
    body.add("bay floor", floor, "leco_grey")
    body.add("well ring", tube(well_d + 14, well_d, 14, x=fx, y=fy, z=bz0), "stainless")
    body.add("feet", box(x0 + 20, yf + 20, 0, W / 2 - 20, -yf - 20, 15.0), "inst_dark")
    # the screen panel, proud of the front on the left
    yp = yf - p["scr_proud"]
    body.add("screen panel", box(x0 + 8, yp, 15.0, g["sx1"] + 14, yf + 1, H - p["lid_h"] - 40), "leco_white")
    body.add("screen bezel", box(g["sx0"] - 8, yp - 3, g["sz0"] - 10, g["sx1"] + 8, yp, g["sz1"] + 10), "inst_dark")
    body.add("touchscreen", box(g["sx0"], yp - 4, g["sz0"], g["sx1"], yp - 3, g["sz1"]), "leco_screen")
    rows = None
    for k in range(9):
        z = g["sz1"] - 25 - k * 18
        r_ = box(g["sx0"] + 15, yp - 4.6, z, g["sx1"] - 15, yp - 4.0, z + 5)
        rows = r_ if rows is None else rows.union(r_)
    body.add("screen rows", rows, "leco_ui")
    # the plinth under the bay, its front rounded, with the electrode's well
    plinth = cq.Workplane("XY").center(0.5 * (bay_x0 + g["px1"]), yf + 60).ellipse(0.5 * (g["px1"] - bay_x0), 100) \
        .extrude(bz0 - 23).translate((0, 0, 15)).intersect(box(bay_x0, yf - 45, 15, g["px1"], -yf, bz0 - 8))
    well_bot = g["body_top"] - g["travel"] - g["body_h"] - 10.0
    plinth = plinth.cut(cyl(well_d, bz0 - well_bot + 1, x=fx, y=fy, z=well_bot))
    body.add("plinth", plinth, "leco_white")
    body.add("well", cyl(well_d, 2, x=fx, y=fy, z=well_bot), "inst_dark")
    body.add("plinth label", box(fx - 40, yf - 46, bz0 - 70, fx + 40, yf - 44, bz0 - 58), "inst_grey")
    body.add("gas knobs", cyl(22, 34, x=W / 2 - 70, y=yf + 40, z=bz0).union(cyl(22, 34, x=W / 2 - 115, y=yf + 40,
                                                                              z=bz0)), "inst_black")
    # the electrode housing and loading head, proud of the front at the top right (its own piece: see-through when
    # the sample drops)
    head = rbox(g["hx1"] - g["hx0"], 220, hz1 - hz0, 30, x=fx, y=yh + 110, z=hz0)
    housing.add("electrode housing", head.edges(">Z").fillet(12), "leco_white")
    housing.add("housing band", box(g["hx0"] + 2, yh - 1, hz0, g["hx1"] - 2, yh + 200, hz0 + 18), "inst_black")
    housing.add("LECO badge", box(fx - 35, yh - 1.0, hz0 + 70, fx + 35, yh, hz0 + 92), "inst_dark")
    housing.add("loading head", cyl(70, 18, x=fx, y=fy, z=hz1).union(tube(28, 12, 4, x=fx, y=fy, z=hz1 + 18)),
                "inst_black")
    housing.add("loading head dial", tube(70, 58, 4, x=fx, y=fy, z=hz1 + 14), "stainless")
    housing.add("handle", hose([(g["hx1"] - 5, yh + 120, hz0 + 40), (g["hx1"] + 30, yh + 115, hz0 + 38),
                                (g["hx1"] + 70, yh + 110, hz0 + 30)], 24.0), "inst_black")
    body.add("upper electrode", cyl(60, 30, x=fx, y=fy, z=hz0 - 30).union(cyl(36, 15, x=fx, y=fy, z=g["tip"])),
             "stainless")
    # the electrode cleaner's brush beside it (left), on its black body with the brass collar
    cx = g["cx"]
    body.add("cleaner body", cyl(80, 60, x=cx, y=fy + 10, z=bz0 + 60), "inst_black")
    body.add("cleaner post", cyl(40, 60, x=cx + 30, y=fy + 10, z=bz0), "inst_black")
    body.add("cleaner collar", cyl(40, 14, x=cx, y=fy + 10, z=bz0 + 120), "brass")
    body.add("cleaner brush", cyl(14, 46, x=cx, y=fy + 10, z=bz0 + 134), "stainless")
    # the lower electrode: v 0 closed (the crucible clamped against the upper electrode's tip), v 1 open (dropped
    # `travel` mm into its well, the crucible pedestal clear for loading)
    low = _piece(inst, "lower_electrode")
    bt = g["body_top"]
    low.add("lower electrode body", cyl(110, g["body_h"] - 8, x=fx, y=fy, z=bt - g["body_h"]), "inst_black")
    low.add("lower electrode rim", cyl(116, 8, x=fx, y=fy, z=bt - 8), "stainless")
    low.add("crucible pedestal", cyl(26, g["ped_h"], x=fx, y=fy, z=bt), "stainless")
    cru = _piece(inst, "crucible")
    pt = g["ped_top"]
    cru.add("graphite crucible", tube(22, 12, g["cru_h"] - 0.5, x=fx, y=fy, z=pt).union(cyl(22, 4, x=fx, y=fy, z=pt)),
            "graphite_cr")
    glow = _piece(inst, "glow")
    glow.add("crucible at fusion", tube(22.8, 11.6, g["cru_h"] - 0.2, x=fx, y=fy, z=pt - 0.2), "hot")
    # the sample: a tin capsule in a nickel basket, dropped from the loading head into the crucible
    smp = _piece(inst, "sample")
    s0 = g["smp_z0"]
    smp.add("nickel basket", tube(9.0, 8.4, 9.0, x=fx, y=fy, z=s0).union(cyl(9.0, 0.4, x=fx, y=fy, z=s0)), "nickel")
    smp.add("tin capsule", cyl(7.6, 8.0, x=fx, y=fy, z=s0 + 0.5), "tin")
    drop = [(0, 0, 0), (0, 0, -(s0 - (pt + 4.0)))]
    # detection, inside the cabinet behind the screen (seen in the cutaway): two NDIR cells (CO, CO2), the catalyst
    # heater (rare-earth copper oxide, CO -> CO2 and H2 -> H2O), reagent tubes, and the thermal-conductivity cell
    det = _piece(inst, "detect")
    dz = 0.5 * H
    det.add("IR cell CO", _xcyl(46, 260, x=x0 + 60, y=0.0, z=dz + 70), "cell_body")
    det.add("IR cell CO2", _xcyl(46, 260, x=x0 + 60, y=0.0, z=dz + 10), "cell_body")
    det.add("IR cell windows", _xcyl(48, 6, x=x0 + 54, y=0.0, z=dz + 70).union(_xcyl(48, 6, x=x0 + 54, y=0.0,
                                                                                    z=dz + 10)), "cell_gold")
    det.add("catalyst heater", cyl(70, 160, x=x0 + 390, y=60, z=dz - 40), "inst_grey")
    det.add("reagent tubes", cyl(36, 200, x=x0 + 460, y=-60, z=dz - 120).union(cyl(36, 200, x=x0 + 510, y=-60,
                                                                                  z=dz - 120)), "reagent")
    det.add("TC cell", box(x0 + 330, -150, dz - 150, x0 + 430, -70, dz - 80), "cell_body")
    gas = _piece(inst, "gas")
    gas.add("gas path", hose([(fx, fy + 40, hz0 - 15), (fx, 80, hz0 - 15), (x0 + 390, 80, dz + 130),
                              (x0 + 340, 0, dz + 70), (x0 + 330, 0, dz + 70)], 6.0).union(
        hose([(x0 + 60, 0, dz + 70), (x0 + 30, 0, dz + 40), (x0 + 60, 0, dz + 10)], 6.0)).union(
        hose([(x0 + 330, 0, dz + 10), (x0 + 460, -60, dz + 90), (x0 + 510, -60, dz + 90), (x0 + 430, -110, dz - 80)],
             6.0)), "light_path")
    inst.joints = {
        "lower_electrode": Joint("slide", vec=(0, 0, -g["travel"]), v0=1.0),
        "crucible": Joint("fade", parent="lower_electrode"),
        "glow": Joint("fade", parent="lower_electrode"),
        "sample": Joint("path", path=tuple(drop)),
        "gas": Joint("fade"),
    }
    inst.anchors = onh_anchors(p)
    inst.cam = (0.6, -1.6, 0.6)
    return inst



ANCHORS["onh_analyzer"] = (ONH, onh_anchors)
FREE["onh_analyzer"] = ["scr_x0", "scr_x1", "scr_z0", "scr_z1", "head_x0", "head_x1", "head_z0", "head_z1", "bay_z0",
                        "head_proud", "scr_proud"]
CHECKS["onh_analyzer"] = lambda p: [p["scr_x1"] - p["scr_x0"] - 0.3, p["head_x0"] - p["scr_x1"] - 0.01,
                                    p["head_z1"] - p["head_z0"] - 0.15, p["head_z0"] - p["bay_z0"] - 0.12,
                                    0.97 - p["head_x1"], p["scr_z1"] - p["scr_z0"] - 0.3]


# ==================================================================================================== MARS 6
MARS = dict(W=560.0, D=610.0, H=660.0, door_w=420.0, door_h=330.0, door_z0=150.0)
SPECS["microwave_digester"] = {
    "model": "CEM MARS 6 microwave digestion system",
    "size": "W x D x H from CEM's published figures (see notes/microwave_digester.md); until checked: estimate",
    "estimates": "door and cavity proportions from CEM's product photos; the 12-vessel rotor and the vessels' sizes",
}


def microwave_digester() -> Instrument:
    p = MARS
    W, D, H = p["W"], p["D"], p["H"]
    x0, yf = -W / 2, -D / 2
    inst = Instrument("microwave_digester", "Microwave digestion system", "CEM MARS 6", (W, D, H),
                      "CEM's published W x D x H; look from CEM's product photos", props=("vessels", "carousel"))
    body = _piece(inst, "body")
    dx0, dx1 = x0 + 25, x0 + 25 + p["door_w"]
    dz0, dz1 = p["door_z0"], p["door_z0"] + p["door_h"]
    cav = box(dx0 + 20, yf + 30, dz0 + 15, dx1 - 20, yf + 30 + 400, dz1 - 15)
    shell = rbox(W, D, H, 20, x=0, y=0, z=0).edges(">Z").fillet(15)
    body.add("cabinet", shell.cut(cav).cut(box(dx0 + 20, yf - 1, dz0 + 15, dx1 - 20, yf + 31, dz1 - 15)), "cem_grey")
    body.add("cavity", box(dx0 + 20, yf + 30, dz0 + 15, dx1 - 20, yf + 34, dz1 - 15).translate((0, 400, 0)), "stainless")
    body.add("cavity floor", box(dx0 + 20, yf + 30, dz0 + 10, dx1 - 20, yf + 430, dz0 + 15), "stainless")
    body.add("control panel", box(dx1 + 10, yf - 2, dz0 + 40, W / 2 - 15, yf, dz1), "cem_dark")
    body.add("touchscreen", box(dx1 + 20, yf - 3, dz1 - 110, W / 2 - 25, yf - 2, dz1 - 20), "screen_on")
    body.add("base band", box(x0, yf - 1, 0, W / 2, yf, 60), "cem_dark")
    body.add("exhaust duct", cyl(100, 50, x=0, y=D / 2 - 120, z=H - 5), "steel")
    door = _piece(inst, "door")
    door.add("door", box(dx0, yf - 40, dz0, dx1, yf - 2, dz1), "cem_dark")
    door.add("door window", box(dx0 + 60, yf - 41, dz0 + 60, dx1 - 60, yf - 39, dz1 - 60), "window")
    door.add("door handle", box(dx1 - 40, yf - 70, dz0 + 80, dx1 - 20, yf - 40, dz1 - 80), "steel")
    car = _piece(inst, "carousel")
    ccx, ccy, ccz = 0.5 * (dx0 + dx1), yf + 230, dz0 + 15
    car.add("turntable", cyl(330, 10, x=ccx, y=ccy, z=ccz), "tfm")
    ves = _piece(inst, "vessels")
    vs = None
    for k in range(12):
        a = 2 * math.pi * k / 12
        v = cyl(40, 120, x=ccx + 130 * math.cos(a), y=ccy + 130 * math.sin(a), z=ccz + 10)
        vs = v if vs is None else vs.union(v)
    ves.add("vessel sleeves", vs, "vessel_sleeve")
    inst.joints = {"door": Joint("hinge", axis=(0, 0, 1), pivot=(dx0, yf - 40, 0), deg=-100.0),
                   "carousel": Joint("spin", axis=(0, 0, 1), pivot=(ccx, ccy, 0), deg=360.0),
                   "vessels": Joint("spin", axis=(0, 0, 1), pivot=(ccx, ccy, 0), deg=360.0)}
    return inst


def mars_geom() -> dict:
    p = MARS
    W, D = p["W"], p["D"]
    x0, yf = -W / 2, -D / 2
    dx0, dx1 = x0 + 25, x0 + 25 + p["door_w"]
    return dict(cx=0.5 * (dx0 + dx1), cy=yf + 230, cz=p["door_z0"] + 15, dx0=dx0, dx1=dx1, dz0=p["door_z0"],
                dz1=p["door_z0"] + p["door_h"], yf=yf, r=130.0)


# ==================================================================================================== impulse sealer
SEAL = dict(W=330.0, D=95.0, H=150.0, L=200.0)
SPECS["heat_sealer"] = {
    "model": "hand impulse heat sealer, 8 in (200 mm) seal",
    "size": "W x D x H from the maker's published figures (see notes/heat_sealer.md); until checked: estimate",
}


def heat_sealer() -> Instrument:
    p = SEAL
    W, D, H, L = p["W"], p["D"], p["H"], p["L"]
    inst = Instrument("heat_sealer", "Impulse heat sealer", "hand impulse sealer, 8 in", (W, D, H),
                      "the maker's published size; look from product photos", props=("bag",))
    body = _piece(inst, "body")
    x0, yf = -W / 2, -D / 2
    body.add("base", box(x0, yf, 0, W / 2, -yf, 60).union(box(x0, yf + 20, 60, x0 + 70, -yf, 110)), "sealer_blue")
    body.add("lower jaw", box(x0 + 80, yf + 8, 60, x0 + 80 + L, yf + 30, 66), "ptfe")
    body.add("timer dial", _ycyl(30, 10, x=x0 + 35, y=yf - 10, z=60), "inst_black")
    body.add("lamp", _ycyl(8, 4, x=x0 + 35, y=yf - 4, z=90), "led_red")
    arm = _piece(inst, "arm")
    arm.add("arm", box(x0 + 70, yf + 4, 66, W / 2, -yf - 5, 92), "sealer_blue")
    arm.add("upper jaw", box(x0 + 80, yf + 8, 64, x0 + 80 + L, yf + 30, 67), "pp_black")
    arm.add("arm grip", box(W / 2 - 60, yf + 4, 92, W / 2, -yf - 5, 104), "inst_black")
    inst.joints = {"arm": Joint("hinge", axis=(1, 0, 0), pivot=(0, -yf - 5, 66), deg=-35.0, v0=0.0)}
    return inst


def seal_geom() -> dict:
    p = SEAL
    x0, yf = -p["W"] / 2, -p["D"] / 2
    return dict(jaw_x0=x0 + 80, jaw_x1=x0 + 80 + p["L"], jaw_y=yf + 19, jaw_z=66.0)


# ==================================================================================================== shipping box
BOX = dict(W=305.0, D=230.0, H=150.0)


def ship_box() -> Instrument:
    p = BOX
    W, D, H = p["W"], p["D"], p["H"]
    inst = Instrument("ship_box", "Insulated shipper", "corrugated box with a foam insert", (W, D, H),
                      "a standard 12 x 9 x 6 in box (estimate)")
    body = _piece(inst, "body")
    body.add("box", box(-W / 2, -D / 2, 0, W / 2, D / 2, H - 4).cut(box(-W / 2 + 4, -D / 2 + 4, 4, W / 2 - 4, D / 2 - 4, H)),
             "kraft")
    foam = box(-W / 2 + 4, -D / 2 + 4, 4, W / 2 - 4, D / 2 - 4, 90)
    for i in range(4):
        foam = foam.cut(cyl(30, 70, x=-90 + 60 * i, y=-40, z=25))
    foam = foam.cut(box(-120, 15, 25, 120, 85, 95))
    body.add("foam insert", foam, "foam")
    lid = _piece(inst, "lid")
    lid.add("lid", box(-W / 2, -D / 2, H - 4, W / 2, D / 2, H), "kraft")
    lid.add("lid flap", box(-W / 2, -D / 2 - 3, H - 40, W / 2, -D / 2, H), "kraft")
    inst.joints = {"lid": Joint("hinge", axis=(1, 0, 0), pivot=(0, D / 2, H), deg=-110.0, v0=1.0)}
    return inst


# ==================================================================================================== bench drill
DRILL = dict(W=230.0, D=360.0, H=560.0)


def bench_drill() -> Instrument:
    p = DRILL
    W, D, H = p["W"], p["D"], p["H"]
    inst = Instrument("bench_drill", "Bench drill press", "small bench drill press (8 in class)", (W, D, H),
                      "estimate from 8 in bench drill presses' catalogue sizes", props=("chips",))
    body = _piece(inst, "body")
    yb = D / 2 - 60
    body.add("base", box(-W / 2, -D / 2, 0, W / 2, D / 2, 30), "cast_grey")
    body.add("column", cyl(46, H - 120, x=0, y=yb, z=30), "chrome")
    body.add("table", cyl(170, 18, x=0, y=-40, z=180).union(box(-20, -40, 170, 20, yb, 198)), "cast_grey")
    body.add("vise", box(-50, -80, 198, 50, 0, 225).union(box(-50, -80, 225, -38, 0, 250)).union(
        box(38, -80, 225, 50, 0, 250)), "drill_green")
    body.add("head", rbox(150, 260, 150, 30, x=0, y=yb - 90, z=H - 170), "drill_green")
    body.add("motor", cyl(110, 150, x=0, y=yb + 75, z=H - 175), "drill_green")
    body.add("feed handles", _xcyl(14, 160, x=75, y=yb - 60, z=H - 100).union(
        hose([(150, yb - 60, H - 100), (190, yb - 60, H - 60)], 10)), "chrome")
    quill = _piece(inst, "quill")
    qx, qy = 0, -40
    quill.add("quill", cyl(40, 50, x=qx, y=qy, z=H - 210), "chrome")
    quill.add("chuck", cyl(36, 50, x=qx, y=qy, z=H - 260).union(
        cq.Workplane("XY").circle(18).workplane(offset=-15).circle(8).loft().translate((qx, qy, H - 260))), "steel")
    quill.add("drill bit", cyl(6, 80, x=qx, y=qy, z=H - 355), "inst_dark")
    chips = _piece(inst, "chips")
    rng = np.random.default_rng(3)
    ch = None
    for k in range(18):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(4, 30)
        c = box(-2, -0.6, 0, 2, 0.6, 0.6).rotate((0, 0, 0), (0, 0, 1), rng.uniform(0, 180)).translate(
            (qx + r * math.cos(a), qy + r * math.sin(a) - 20, 226))
        ch = c if ch is None else ch.union(c)
    chips.add("chips", ch, "chips")
    inst.joints = {"quill": Joint("slide", vec=(0, 0, -45.0)), "chips": Joint("fade")}
    return inst


def drill_geom() -> dict:
    return dict(bit_x=0.0, bit_y=-40.0, bit_tip=DRILL["H"] - 355, vise_top=225.0, vise_y=-40.0)


# ==================================================================================================== props
def prop_vial(label: bool = True, fill: float = 0.35) -> Model:
    """A new 20 mL HDPE screw-cap vial (28 x 61 mm), with a little grey powder and a label."""
    m = Model("vial20", "20 mL HDPE screw-cap vial")
    m.add("vial", tube(28, 26, 52, z=0).union(cyl(28, 1.2)), "hdpe")
    m.add("cap", cyl(29.5, 13, z=50).edges(">Z").fillet(1.5), "pp_cap")
    if fill > 0:
        m.add("powder", cyl(25.6, 50 * fill, z=1.2), "al_powder")
    if label:
        m.add("label", tube(28.6, 28.0, 22, z=14).intersect(box(-20, -20, 0, 20, 2, 60)), "label_w")
        m.add("label text", tube(28.8, 28.5, 3, z=26).intersect(box(-12, -20, 0, 12, 0, 60)).union(
            tube(28.8, 28.5, 2, z=20).intersect(box(-12, -20, 0, 8, 0, 60))), "label_ink")
    return m


def prop_vial_cap() -> Model:
    m = Model("vial_cap", "vial cap")
    m.add("cap", cyl(29.5, 13).edges(">Z").fillet(1.5), "pp_cap")
    return m


def prop_vial_open(fill: float = 0.35) -> Model:
    m = Model("vial_open", "vial without its cap")
    m.add("vial", tube(28, 26, 52).union(cyl(28, 1.2)), "hdpe")
    if fill > 0:
        m.add("powder", cyl(25.6, 50 * fill, z=1.2), "al_powder")
    m.add("label", tube(28.6, 28.0, 22, z=14).intersect(box(-20, -20, 0, 20, 2, 60)), "label_w")
    return m


def prop_bag(sealed: bool = False) -> Model:
    """A 3 x 4 in (76 x 102 mm) 4-mil poly bag lying flat, with powder in it; sealed: the heat seal across its mouth."""
    m = Model("bag", "4-mil poly bag, 76 x 102 mm")
    m.add("bag", box(-38, -51, 0, 38, 51, 3.0), "poly_bag")
    m.add("powder", cq.Workplane("XY").ellipse(22, 26).extrude(4.0).translate((0, -14, 0.4)), "al_powder")
    if sealed:
        m.add("seal", box(-38, 38, -0.2, 38, 41, 3.2), "inst_grey")
    m.add("label", box(-30, 8, 3.0, 30, 30, 3.3), "label_w")
    return m


def prop_ar_nozzle() -> Model:
    """An argon flushing nozzle: a stainless needle on a short PE tube's end, held like a pen."""
    m = Model("ar_nozzle", "argon flushing nozzle")
    m.add("grip", cyl(10, 70, z=0), "inst_dark")
    m.add("needle", cyl(2.0, 60, z=-60), "stainless")
    m.add("hose stub", cyl(6, 20, z=70), "hose_black")
    return m


def prop_regulator() -> Model:
    """A two-stage argon regulator on a wall bracket (the lab's argon line), with its outlet valve."""
    m = Model("ar_regulator", "argon regulator on the line")
    m.add("bracket", box(-60, 0, 0, 60, 10, 160), "steel")
    m.add("body", cyl(55, 70, z=0).rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, 90)), "regulator")
    m.add("gauges", _ycyl(55, 22, x=-55, y=-20, z=110).union(_ycyl(55, 22, x=55, y=-20, z=110)), "regulator")
    m.add("gauge faces", _ycyl(46, 1, x=-55, y=-43, z=110).union(_ycyl(46, 1, x=55, y=-43, z=110)), "gauge_face")
    m.add("knob", _ycyl(40, 30, x=0, y=-70, z=90), "inst_black")
    m.add("pipe", box(-8, 0, 160, 8, 10, 400), "copper")
    return m


def prop_coc_form() -> Model:
    """A chain-of-custody form on a clipboard (letter size, 216 x 279 mm)."""
    m = Model("coc", "chain-of-custody form on a clipboard")
    m.add("board", box(-115, -160, 0, 115, 160, 3), "clip_board")
    m.add("form", box(-108, -140, 3, 108, 139, 3.4), "paper")
    lines = None
    for k in range(12):
        ln = box(-95, 110 - 20 * k, 3.4, 95, 111.5 - 20 * k, 3.6)
        lines = ln if lines is None else lines.union(ln)
    m.add("lines", lines.union(box(-95, 125, 3.4, 20, 132, 3.7)), "label_ink")
    m.add("clip", box(-40, 140, 3, 40, 160, 12), "steel")
    return m


def prop_crm_bottle() -> Model:
    """A certified reference material: Al alloy chips in a 60 mm amber glass bottle with a white cap and label."""
    m = Model("crm", "CRM bottle (Al alloy chips)")
    m.add("bottle", tube(60, 56, 95, z=0).union(cyl(60, 3)).union(tube(32, 28, 14, z=95)), "amber")
    m.add("chips", cyl(55, 55, z=3), "chips")
    m.add("cap", cyl(36, 18, z=104), "pp_cap")
    m.add("label", tube(61, 60, 50, z=25).intersect(box(-40, -40, 0, 40, 5, 100)), "label_w")
    return m


def prop_cube(on_plate: bool = True) -> Model:
    """A printed 10 mm Al cube (as built), on its piece of build plate if on_plate."""
    m = Model("cube", "printed cube, 10 mm")
    m.add("cube", box(-5, -5, 0, 5, 5, 10), "al_part")
    return m


def prop_feedstock() -> Model:
    """Feedstock: a piece of 3/4 in (19 mm) bar, 40 mm long, lying down, and two master alloy pieces."""
    m = Model("feedstock", "feedstock bar and master alloys")
    m.add("bar", _xcyl(19, 40, x=-20, y=0, z=9.5), "al_metal")
    m.add("master alloy", box(30, -8, 0, 46, 6, 9).union(box(34, 12, 0, 46, 24, 7)), "al_part")
    return m


def prop_weigh_boat() -> Model:
    m = Model("boat", "PS weigh boat 41 mm")
    solid = cq.Workplane("XY").rect(29, 29).workplane(offset=8).rect(41, 41).loft()
    m.add("boat", solid.faces(">Z").shell(-0.4), "pp_white")
    return m


def prop_chip_pile(n: int = 40, r: float = 12.0, seed: int = 5) -> Model:
    rng = np.random.default_rng(seed)
    m = Model("chips", "chips")
    ch = None
    for k in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = r * math.sqrt(rng.uniform(0, 1))
        c = box(-1.8, -0.5, 0, 1.8, 0.5, 0.5).rotate((0, 0, 0), (0, 0, 1), rng.uniform(0, 180)).translate(
            (rr * math.cos(a), rr * math.sin(a), rng.uniform(0, 1.5)))
        ch = c if ch is None else ch.union(c)
    m.add("chips", ch, "chips")
    return m


def prop_spatula() -> Model:
    """A stainless micro spatula (150 mm), lying along x, its scoop at +x."""
    m = Model("spatula", "stainless micro spatula")
    m.add("spatula", box(-75, -2.5, 0, 50, 2.5, 1.2).union(
        cq.Workplane("XY").ellipse(12, 5).extrude(1.2).translate((62, 0, 0))), "steel")
    return m


def prop_graphite_crucible() -> Model:
    m = Model("crucible", "graphite crucible")
    m.add("crucible", tube(22, 12, 25).union(cyl(22, 4)), "graphite_cr")
    return m


def prop_capsule_basket() -> Model:
    """A tin capsule (powder sealed in it) inside a nickel basket (flux), 9 mm across."""
    m = Model("capsule", "tin capsule in a nickel basket")
    m.add("basket", tube(9.0, 8.4, 9.0).union(cyl(9.0, 0.4)), "nickel")
    m.add("capsule", cyl(7.6, 8.0, z=0.5), "tin")
    return m


def prop_digest_vessel(open_: bool = False) -> Model:
    """A microwave digestion vessel: TFM liner in its composite sleeve, 100 mL class, with its cap."""
    m = Model("vessel", "TFM digestion vessel")
    m.add("sleeve", tube(40, 31, 110), "vessel_sleeve")
    m.add("liner", tube(31, 27, 112).union(cyl(31, 3)), "tfm")
    m.add("digest", cyl(26.5, 18, z=3), "acid")
    if not open_:
        m.add("cap", cyl(42, 22, z=110), "tfm")
    return m


def prop_tube50(fill: float = 0.8) -> Model:
    """A 50 mL PP centrifuge tube (29 x 115 mm), the digest diluted to the mark, capped."""
    m = Model("tube50", "50 mL PP tube")
    m.add("tube", tube(29, 27, 100, z=15).union(
        cq.Workplane("XY").circle(4).workplane(offset=15).circle(14.5).loft()), "polypropylene")
    m.add("liquid", cyl(26.8, 85 * fill, z=15), "acid")
    m.add("cap", cyl(32, 14, z=113), "pp_blue")
    return m


def prop_bottle(color: str = "pp_white", d: float = 70.0, h: float = 150.0) -> Model:
    m = Model("bottle", "acid bottle")
    m.add("bottle", cyl(d, h).edges(">Z").fillet(8).union(cyl(d * 0.42, 22, z=h)), color)
    m.add("label", tube(d + 1, d, h * 0.4, z=h * 0.3).intersect(box(-d, -d, 0, d, 0, h)), "label_w")
    return m


REGISTRY = {"icp_oes": icp_oes, "onh_analyzer": onh_analyzer, "microwave_digester": microwave_digester,
            "heat_sealer": heat_sealer, "ship_box": ship_box, "bench_drill": bench_drill}
