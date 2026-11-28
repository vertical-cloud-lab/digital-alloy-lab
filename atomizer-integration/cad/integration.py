#!/usr/bin/env python3
"""The #151 integration hardware, as CadQuery parts placed on the rePowder model (viz3d/model.py).

What it adds to the machine (millimetres, z up from the floor, the operator at -y, as in model.py):

* HMI camera: matte anti-glare film on the 15.6 in Weintek cMT2166X; a super clamp on the HMI's own top edge, so the
  camera swings with the HMI; an articulating arm; a printed case for a Camera Module 3 Wide with a flip-down shutter
  (closed while anyone types a password); the existing HMI camera Pi in a case on the HMI's back.
* GU 500 panel camera: film on the furnace controller's LCD; a magnetic base on the blue cabinet's face; a Camera
  Module 3 in the same printed case; the existing panel camera Pi on the cabinet's top.
* HMI Ethernet: a 5-port switch on the HMI's back, the HMI's existing cable moved into it, and two short patch cables
  (switch to HMI, switch to the HMI camera Pi). Only if AMAZEMET agrees, and only if that port is already taken.
* STG1 tap: the right-hand side door opened onto an approximate interior (the STG1 ultrasonic generator, DIN rails,
  PLC), a DB15 pass-through breakout between the STG1's X3 port and its existing cable, two wires to a small printed
  box holding the isolated ADC (ADS1115 + MCP2221A + USB isolator), and a USB cable out to the HMI camera Pi.

Everything AMAZEMET's is approximate: the interior behind the right-hand door is placed from one 720p frame of
training video 1 (9:58), and the HMI's ports and the STG1's connector positions are guesses. The camera poses follow
from the screens' sizes and the lenses' fields of view (see README.md, "Camera framing").

    python integration.py      # builds the parts, caches their meshes in viz3d/.cache/, prints the framing check
"""
from __future__ import annotations

import hashlib
import math
import pickle
import sys
from pathlib import Path

import cadquery as cq
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "viz3d"))
import model as M  # noqa: E402  (viz3d/model.py, copied unchanged from PR #173)

V = cq.Vector
box, rbox, cyl, sphere, fuse, compound, frame, Part = M.box, M.rbox, M.cyl, M.sphere, M.fuse, M.compound, M.frame, M.Part

# ----------------------------------------------------------------------------------------------- colours
FILM = (0.78, 0.90, 0.99)
PRINTED = (0.93, 0.47, 0.13)        # PETG, printed
PRINTED_DK = (0.80, 0.36, 0.08)
CLAMP = (0.13, 0.13, 0.14)
ARM = (0.20, 0.20, 0.22)
PI_RED = (0.80, 0.10, 0.17)
PI_LID = (0.96, 0.96, 0.96)
SWITCH_WHITE = (0.93, 0.93, 0.94)
PCB_GREEN = (0.05, 0.42, 0.20)
PCB_BLUE = (0.10, 0.20, 0.50)
DSUB = (0.76, 0.77, 0.80)
TERMINAL = (0.15, 0.55, 0.25)
STG1 = (0.20, 0.21, 0.23)
PLATE = (0.80, 0.81, 0.82)          # galvanised mounting plate
DIN = (0.70, 0.71, 0.73)
MODULE = (0.86, 0.86, 0.84)
LENS = (0.05, 0.05, 0.07)
ETH_OLD = (0.40, 0.41, 0.44)
ETH_NEW = (0.13, 0.45, 0.88)
USB_BLACK = (0.09, 0.09, 0.10)
RIBBON = (0.93, 0.92, 0.86)
WIRE_RED = (0.86, 0.12, 0.10)
WIRE_BLACK = (0.10, 0.10, 0.11)
FOV = (1.00, 0.80, 0.10)

# ------------------------------------------------------------------------------------------- HMI frame
# model.py builds the HMI at the origin (x across, -y = screen side, z up), turns it -25 deg about z and moves it to
# HMI_C. Parts that ride on the HMI are built in the same local frame and moved the same way.
HMI_ANG = -25.0
HMI_W, HMI_H, HMI_T = 400.0, 262.0, 28.0
SCREEN_C_L = np.array([0.0, -18.0, 0.0])          # screen centre, local
ACTIVE = (344.0, 194.0)                           # cMT2166X active area (1920 x 1080 at 0.179 mm)


def hmi_pt(p) -> np.ndarray:
    a = math.radians(HMI_ANG)
    c, s = math.cos(a), math.sin(a)
    x, y, z = p
    return np.array([c * x - s * y, s * x + c * y, z]) + M.HMI_C


def hmi_vec(v) -> np.ndarray:
    return hmi_pt(v) - M.HMI_C


def hmi_world(shape: cq.Shape) -> cq.Shape:
    return shape.rotate(V(0, 0, 0), V(0, 0, 1), HMI_ANG).translate(V(*M.HMI_C))


# ------------------------------------------------------------------------------------------- cameras
# Camera Module 3 Wide: 102 x 67 deg; Camera Module 3: 66 x 41 deg (Raspberry Pi's product briefs).
WIDE_FOV = (102.0, 67.0)
STD_FOV = (66.0, 41.0)
HMI_CAM_DIST, HMI_CAM_TILT = 260.0, 50.0          # from the screen centre, degrees above the screen's normal
PANEL_CAM_DIST, PANEL_CAM_TILT = 200.0, 30.0

# HMI camera pose, local to the HMI
_d = np.array([0.0, math.cos(math.radians(HMI_CAM_TILT)), -math.sin(math.radians(HMI_CAM_TILT))])
HMI_CAM_C_L = SCREEN_C_L - _d * HMI_CAM_DIST      # lens centre (case centre ~ 12 mm behind it, see head())
HMI_CAM_DIR_L = _d

# GU 500 panel: LCD centre and normal (model.py: LCD x 429-541, y 190-193, z 1365-1423)
LCD_C = np.array([485.0, 190.0, 1394.0])
LCD_SIZE = (112.0, 58.0)
PANEL_C = np.array([485.0, 193.0, 1347.5])        # whole GU 500 panel (140 x 195)
_pd = np.array([0.0, math.cos(math.radians(PANEL_CAM_TILT)), -math.sin(math.radians(PANEL_CAM_TILT))])
PANEL_CAM_C = LCD_C - _pd * PANEL_CAM_DIST
PANEL_CAM_DIR = _pd


def cam_axes(d):
    """Right-handed camera frame for a camera looking along d with x kept horizontal: (ex, ey = d, ez = up)."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    ex = np.cross(d, np.array([0.0, 0.0, 1.0]))
    ex /= np.linalg.norm(ex)
    ez = np.cross(ex, d)
    return ex, d, ez


def head(shutter_open=True):
    """Printed camera case with its lens along +y, centred on the lens's front face at the origin. Returns
    (case, lens, shutter, hinge point, hinge axis), all in this local frame. The shutter is modelled closed (over the
    lens) and hinges about the case's top front edge; `shutter_open` is only used for the static stills."""
    case = rbox(-20, 20, -30, -6, -20, 20, 3).cut(cyl(7.5, 10, (0, -8, 0), (0, 1, 0)))
    boss = cyl(7, 6, (0, -36, 0), (0, 1, 0))                     # 1/4-20 insert boss on the back
    case = fuse(case, boss)
    lens = fuse(cyl(6.5, 6, (0, -6, 0), (0, 1, 0)), cyl(4.5, 0.6, (0, 0, 0), (0, 1, 0)))
    shutter = fuse(box(-19, 19, 0.5, 2.5, -19, 19), box(-6, 6, 0.5, 6.5, -21, -17))   # flap + finger tab
    hinge_p = np.array([0.0, 1.5, 20.0])
    return case, lens, shutter, hinge_p, np.array([1.0, 0.0, 0.0])


def ribbon(pts, w=16.0, t=0.4):
    """A flat cable along a polyline (PyVista, not CadQuery): returned as points for scene tubes."""
    return np.array(pts, float)


# ------------------------------------------------------------------------------------- right-hand door
FX0, FX1 = M.FR_X
FY0, FY1 = M.FR_Y
FZ0, FZ1 = M.FR_Z
CAV = dict(x=(330.0, FX1 + 1.0), y=(215.0, 615.0), z=(245.0, 1530.0))   # compartment behind the right-hand door
DOOR_HINGE = np.array([FX1 + 1.5, FY1 - 40.0])                          # vertical axis at the door's back edge
DOOR_OPEN = 100.0                                                       # degrees about +z: swings out to +x
BACK_X = CAV["x"][0] + 3.0                                              # face of the mounting plate

STG1_BOX = dict(x=(BACK_X, BACK_X + 69.5), y=(420.0, 601.0), z=(1262.0, 1504.5))   # 181 x 242.5 face, 69.5 deep
X3_C = np.array([BACK_X + 36.0, 470.0, STG1_BOX["z"][0]])                         # DB15 on the underside
DIN_Z = (1000.0, 760.0)
ADC_BOX = dict(x=(BACK_X + 3.0, BACK_X + 38.0), y=(262.0, 352.0), z=(DIN_Z[0] - 35.0, DIN_Z[0] + 35.0))
BREAKOUT_DROP = 92.0           # how far the existing X3 plug moves down when the pass-through goes in
GLAND = np.array([560.0, 300.0, FZ1])                                   # cable entry on the cabinet's top (assumed)


def dsub(n_rows=2, w=31.0, h=12.5, depth=8.0, male=True):
    """D-sub shell facing -z, centred at the origin's face (z=0), body going up (+z)."""
    shell = (cq.Workplane("XY").polyline([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2 - 2.5, h / 2),
                                          (-w / 2 + 2.5, h / 2)]).close().extrude(depth)).val()
    flange = box(-w / 2 - 8, w / 2 + 8, -h / 2 - 2.5, h / 2 + 2.5, depth, depth + 1.0)
    return fuse(shell.translate(V(0, 0, 0)), flange)


# --------------------------------------------------------------------------------------------- parts
def hmi_parts() -> list[Part]:
    P = []
    # anti-glare film over the active area, in front of the screen and its widgets
    film = box(-ACTIVE[0] / 2, ACTIVE[0] / 2, -21.0, -20.5, -ACTIVE[1] / 2, ACTIVE[1] / 2)
    P.append(Part("film_hmi", hmi_world(film), FILM, "film_hmi", opacity=0.45, cut=False, tol=0.3))

    # super clamp over the HMI's top edge (28 mm housing), rubber-padded, at mid-width
    zt = HMI_H / 2
    clamp = fuse(box(-24, 24, -27, 27, zt, zt + 22),
                 box(-24, 24, -27, -16, zt - 14, zt),                # front jaw, on the bezel above the screen
                 box(-24, 24, 16, 27, zt - 26, zt),                  # back jaw with the screw
                 cyl(11, 22, (0, 27, zt - 14), (0, 1, 0)),            # wing screw
                 box(-30, 30, 49, 52, zt - 20, zt - 8))
    pads = compound(box(-22, 22, -16, -14, zt - 13, zt - 1), box(-22, 22, 14, 16, zt - 25, zt - 1))
    P.append(Part("hmicam_clamp", hmi_world(clamp), CLAMP, "hmicam_clamp", cut=False))
    P.append(Part("hmicam_pads", hmi_world(pads), (0.25, 0.25, 0.26), "hmicam_clamp", cut=False, tol=0.2))

    # articulating arm: clamp top -> elbow -> ball behind the camera case
    ex, ey, ez = cam_axes(HMI_CAM_DIR_L)
    case_back = HMI_CAM_C_L - ey * 36.0
    j = case_back - ey * 6.0
    base = np.array([0.0, 0.0, zt + 22.0])
    elbow = np.array([0.0, -105.0, zt + 150.0])
    arm = fuse(sphere(10, base + np.array([0, 0, 8])), M.along(cyl(8, float(np.linalg.norm(elbow - base))), base, elbow - base),
               sphere(10, elbow), M.along(cyl(8, float(np.linalg.norm(j - elbow))), elbow, j - elbow), sphere(9, j))
    knob = M.along(cyl(16, 14), elbow + np.array([-7, 0, 0]), (1, 0, 0))
    P.append(Part("hmicam_arm", hmi_world(arm), ARM, "hmicam_arm", cut=False))
    P.append(Part("hmicam_knob", hmi_world(knob), CLAMP, "hmicam_arm", cut=False))

    # camera head, aimed at the screen centre
    case, lens, shutter, _, _ = head()
    place = lambda s: hmi_world(frame(s, HMI_CAM_C_L, ex, ey, ez))
    P.append(Part("hmicam_case", place(case), PRINTED, "hmicam_head", cut=False))
    P.append(Part("hmicam_lens", place(lens), LENS, "hmicam_head", cut=False, tol=0.2))
    P.append(Part("hmicam_shutter", place(shutter), PRINTED_DK, "hmicam_shutter", cut=False, tol=0.2))

    # the existing HMI camera Pi, in a case on the HMI's back (upper right), USB/Ethernet edge down
    pi = fuse(rbox(60, 123, 14, 42, 8, 102, 4), box(64, 119, 42, 45, 30, 90))
    P.append(Part("hmipi_case", hmi_world(pi), PI_RED, "hmipi", cut=False))
    P.append(Part("hmipi_lid", hmi_world(box(63, 120, 41, 43, 12, 98)), PI_LID, "hmipi", cut=False, tol=0.2))
    # 5-port switch (USB-C powered) below it
    sw = rbox(-34, 73, 14, 35, -128, -58, 5)
    ports = compound(*[box(-28 + 18 * k, -16 + 18 * k, 26, 36, -60, -50) for k in range(5)])
    P.append(Part("switch", hmi_world(sw), SWITCH_WHITE, "switch", cut=False))
    P.append(Part("switch_ports", hmi_world(ports), (0.25, 0.26, 0.28), "switch", cut=False, tol=0.2))
    return P


HMI_PIVOT_L = np.array([-57.0, 40.0])       # local (x, y) of the arm's pivot post, moved behind the HMI's back


def hmi_arm_part() -> Part:
    """model.py's HMI arm, with its pivot post moved from inside the screen (local y = -14) to behind the HMI's back,
    so it no longer shows through the screen in close-ups. Bracket and tube as in model.py."""
    fx1, fy0 = FX1, FY0
    piv = hmi_pt((HMI_PIVOT_L[0], HMI_PIVOT_L[1], -65.0))
    start = np.array([fx1 + 20.0, fy0 + 30.0, 1410.0])
    tube_end = np.array([piv[0], piv[1], 1410.0])
    arm = fuse(box(fx1, fx1 + 30, fy0 + 10, fy0 + 50, 1380, 1440),
               M.along(cyl(14, float(np.linalg.norm(tube_end - start))), start, tube_end - start),
               cyl(20, 50, (piv[0], piv[1], 1385.0)),
               hmi_world(box(HMI_PIVOT_L[0] - 15, HMI_PIVOT_L[0] + 15, 13.0, HMI_PIVOT_L[1], -55, -15)))
    return Part("hmi_arm2", arm, M.BLACK, "static", cut=False)


def panel_parts() -> list[Part]:
    P = []
    lx, ly, lz = LCD_C
    film = box(lx - LCD_SIZE[0] / 2 - 6, lx + LCD_SIZE[0] / 2 + 6, 188.6, 189.1, lz - LCD_SIZE[1] / 2 - 6,
               lz + LCD_SIZE[1] / 2 + 6)
    P.append(Part("film_panel", film, FILM, "film_panel", opacity=0.45, cut=False, tol=0.3))
    # magnetic base on the cabinet's face above the recess (painted steel), switch knob on its side
    y0 = FY0
    mag = fuse(rbox(lx - 25, lx + 25, y0 - 58, y0, 1500, 1556, 4), cyl(10, 14, (lx + 25, y0 - 30, 1528), (1, 0, 0)))
    P.append(Part("panelcam_base", mag, CLAMP, "panelcam_base", cut=False))
    ex, ey, ez = cam_axes(PANEL_CAM_DIR)
    case_back = PANEL_CAM_C - ey * 36.0
    j = case_back - ey * 6.0
    base = np.array([lx, y0 - 58.0, 1540.0])
    elbow = np.array([lx, y0 - 130.0, 1575.0])
    arm = fuse(sphere(9, base), M.along(cyl(7, float(np.linalg.norm(elbow - base))), base, elbow - base), sphere(9, elbow),
               M.along(cyl(7, float(np.linalg.norm(j - elbow))), elbow, j - elbow), sphere(8, j))
    P.append(Part("panelcam_arm", arm, ARM, "panelcam_arm", cut=False))
    case, lens, shutter, _, _ = head()
    place = lambda s: frame(s, PANEL_CAM_C, ex, ey, ez)
    P.append(Part("panelcam_case", place(case), PRINTED, "panelcam_head", cut=False))
    P.append(Part("panelcam_lens", place(lens), LENS, "panelcam_head", cut=False, tol=0.2))
    P.append(Part("panelcam_shutter", place(shutter), PRINTED_DK, "panelcam_shutter", cut=False, tol=0.2))
    # the existing panel camera Pi, on the cabinet's top, held by magnets
    pi = rbox(lx - 47, lx + 47, 205, 268, FZ1, FZ1 + 28, 4)
    P.append(Part("panelpi_case", pi, PI_RED, "panelpi", cut=False))
    P.append(Part("panelpi_lid", box(lx - 44, lx + 44, 208, 265, FZ1 + 27, FZ1 + 29), PI_LID, "panelpi", cut=False,
                  tol=0.2))
    return P


def cabinet_parts() -> list[Part]:
    """The blue cabinet again (model.py's), with the compartment behind the right-hand door hollowed out, the door as
    its own part, and an approximate interior from training video 1 at 9:58."""
    P = []
    fx0, fx1, fy0, fy1 = FX0, FX1, FY0, FY1
    body = rbox(fx0, fx1, fy0, fy1, FZ0, FZ1, 12)
    nx0, nx1, nz0, nz1 = fx1 - 250, fx1 - 40, FZ1 - 130 - 355, FZ1 - 130
    body = body.cut(box(nx0, nx1, fy0 - 5, fy0 + 40, nz0, nz1))
    body = body.cut(box(*CAV["x"], *CAV["y"], *CAV["z"]))
    P.append(Part("cabinet_open", body, M.BLUE, "static", cut=False, tol=0.8))
    door = fuse(box(fx1, fx1 + 3, CAV["y"][0] - 8, CAV["y"][1] + 8, CAV["z"][0] - 8, CAV["z"][1] + 8),
                box(fx1 + 3, fx1 + 9, fy0 + 70, fy0 + 90, 1020, 1120))
    P.append(Part("door_r", door, (0.07, 0.20, 0.55), "door_r", cut=False))
    # interior: mounting plate, STG1, DIN rails with PLC, terminals, PSU and relays, a stainless vessel
    P.append(Part("int_plate", box(CAV["x"][0], BACK_X, CAV["y"][0] + 5, CAV["y"][1] - 5, CAV["z"][0] + 5,
                                   CAV["z"][1] - 5), PLATE, "interior", cut=False))
    s = STG1_BOX
    P.append(Part("stg1", rbox(*s["x"], *s["y"], *s["z"], 4), STG1, "interior", cut=False))
    P.append(Part("stg1_label", box(s["x"][1], s["x"][1] + 0.6, s["y"][0] + 30, s["y"][1] - 30, s["z"][1] - 60,
                                    s["z"][1] - 25), (0.85, 0.85, 0.86), "interior", cut=False, tol=0.2))
    # STG1 underside connectors: X3 DB15 (the tap), X5/X6 RJ45, X1 mains, X2 HV LEMO
    x3 = dsub().rotate(V(0, 0, 0), V(1, 0, 0), 180).translate(V(*X3_C))
    x3 = x3.rotate(V(*X3_C), V(0, 0, 1), 90)
    others = compound(box(X3_C[0] - 8, X3_C[0] + 8, 520, 536, s["z"][0] - 13, s["z"][0]),
                      box(X3_C[0] - 8, X3_C[0] + 8, 542, 558, s["z"][0] - 13, s["z"][0]),
                      box(X3_C[0] - 12, X3_C[0] + 12, 568, 592, s["z"][0] - 15, s["z"][0]),
                      cyl(7, 20, (X3_C[0], 436, s["z"][0]), (0, 0, -1)))
    P.append(Part("stg1_x3", x3, DSUB, "interior", cut=False, tol=0.2))
    P.append(Part("stg1_ports", others, (0.30, 0.31, 0.33), "interior", cut=False, tol=0.2))
    for k, z in enumerate(DIN_Z):
        P.append(Part(f"din_{k}", box(BACK_X, BACK_X + 8, 240, 605, z - 17.5, z + 17.5), DIN, "interior", cut=False))
    duct = box(BACK_X, BACK_X + 60, 240, 605, 870, 905)
    P.append(Part("duct", duct, (0.55, 0.56, 0.58), "interior", cut=False))
    plc = fuse(box(BACK_X + 8, BACK_X + 78, 420, 520, DIN_Z[0] - 45, DIN_Z[0] + 45))
    P.append(Part("plc", plc, MODULE, "interior", cut=False))
    P.append(Part("plc_terminals", compound(box(BACK_X + 78, BACK_X + 82, 425, 515, DIN_Z[0] + 28, DIN_Z[0] + 40),
                                            box(BACK_X + 78, BACK_X + 82, 425, 515, DIN_Z[0] - 40, DIN_Z[0] - 28)),
                  TERMINAL, "interior", cut=False, tol=0.2))
    terms = compound(*[box(BACK_X + 8, BACK_X + 58, 530 + 6.5 * k, 535.5 + 6.5 * k, DIN_Z[0] - 30, DIN_Z[0] + 30)
                       for k in range(11)])
    P.append(Part("terminals", terms, (0.62, 0.63, 0.66), "interior", cut=False, tol=0.2))
    psu = box(BACK_X + 8, BACK_X + 98, 420, 500, DIN_Z[1] - 55, DIN_Z[1] + 55)
    relays = compound(*[box(BACK_X + 8, BACK_X + 70, 510 + 16 * k, 524 + 16 * k, DIN_Z[1] - 40, DIN_Z[1] + 40)
                        for k in range(6)])
    P.append(Part("psu", psu, (0.72, 0.73, 0.75), "interior", cut=False))
    P.append(Part("relays", relays, (0.30, 0.32, 0.36), "interior", cut=False, tol=0.2))
    vessel = fuse(cyl(52, 170, (BACK_X + 110, 330, 560)), cyl(9, 60, (BACK_X + 110, 330, 730)))
    P.append(Part("vessel", vessel, (0.82, 0.83, 0.84), "interior", cut=False))
    P.append(Part("gland", fuse(cyl(13, 6, (GLAND[0], GLAND[1], FZ1)), cyl(9, 10, (GLAND[0], GLAND[1], FZ1 + 6))),
                  (0.15, 0.15, 0.16), "interior", cut=False, tol=0.2))
    return P


def tap_parts() -> list[Part]:
    P = []
    x, y, z = X3_C
    # the existing X3 plug (hood) and its first 60 mm of cable; moves down BREAKOUT_DROP when the breakout goes in
    hood = fuse(box(x - 9, x + 9, y - 22, y + 22, z - 46, z - 4), cyl(4.5, 30, (x, y, z - 46), (0, 0, -1)))
    P.append(Part("x3_plug", hood, (0.25, 0.26, 0.28), "x3_plug", cut=False, tol=0.3))
    # DB15 pass-through breakout: male D-sub up into X3, female D-sub down for the plug, screw terminals between
    pcb = box(x + 10, x + 11.6, y - 26, y + 26, z - BREAKOUT_DROP + 2, z - 6)
    male = box(x - 6, x + 10, y - 17, y + 17, z - 8, z - 1)
    female = box(x - 6, x + 10, y - 17, y + 17, z - BREAKOUT_DROP + 2, z - BREAKOUT_DROP + 10)
    terms = compound(*[box(x + 11.6, x + 21.6, y - 24 + 6.0 * k, y - 19 + 6.0 * k, z - 62, z - 30) for k in range(8)])
    P.append(Part("breakout_pcb", pcb, PCB_GREEN, "breakout", cut=False, tol=0.2))
    P.append(Part("breakout_dsubs", compound(male, female), DSUB, "breakout", cut=False, tol=0.2))
    P.append(Part("breakout_terms", terms, TERMINAL, "breakout", cut=False, tol=0.2))
    # isolated ADC box on the upper DIN rail: printed tray + lid (the lid fades to show the boards)
    b = ADC_BOX
    tray = box(*b["x"], *b["y"], *b["z"]).cut(box(b["x"][0] + 2, b["x"][1] + 1, b["y"][0] + 2, b["y"][1] - 2,
                                                  b["z"][0] + 2, b["z"][1] - 2))
    P.append(Part("adc_tray", tray, PRINTED, "adc", cut=False, tol=0.3))
    P.append(Part("adc_lid", box(b["x"][1], b["x"][1] + 2, *b["y"], *b["z"]), PRINTED, "adc_lid", opacity=1.0,
                  cut=False, tol=0.3))
    bx = b["x"][0] + 6
    P.append(Part("adc_isolator", box(bx, bx + 1.6, b["y"][0] + 4, b["y"][0] + 34, b["z"][0] + 6, b["z"][1] - 6),
                  PCB_GREEN, "adc", cut=False, tol=0.2))
    P.append(Part("adc_mcp2221", box(bx, bx + 1.6, b["y"][0] + 37, b["y"][0] + 58, b["z"][0] + 14, b["z"][1] - 14),
                  PCB_BLUE, "adc", cut=False, tol=0.2))
    P.append(Part("adc_ads1115", box(bx, bx + 1.6, b["y"][0] + 61, b["y"][0] + 86, b["z"][0] + 16, b["z"][1] - 16),
                  PCB_BLUE, "adc", cut=False, tol=0.2))
    P.append(Part("adc_chips", compound(box(bx + 1.6, bx + 3, b["y"][0] + 14, b["y"][0] + 24, b["z"][0] + 28,
                                            b["z"][0] + 40),
                                        box(bx + 1.6, bx + 3, b["y"][0] + 44, b["y"][0] + 51, b["z"][0] + 31,
                                            b["z"][0] + 39),
                                        box(bx + 1.6, bx + 3, b["y"][0] + 70, b["y"][0] + 77, b["z"][0] + 31,
                                            b["z"][0] + 39)), LENS, "adc", cut=False, tol=0.2))
    barrier = box(b["x"][1] + 2, b["x"][1] + 2.4, b["y"][0] + 34.5, b["y"][0] + 36.5, b["z"][0] + 2, b["z"][1] - 2)
    P.append(Part("adc_barrier", barrier, (0.85, 0.10, 0.10), "adc_lid", cut=False, tol=0.2))
    return P


def parts() -> list[Part]:
    return [hmi_arm_part()] + hmi_parts() + panel_parts() + cabinet_parts() + tap_parts()


# ------------------------------------------------------------------------------------------ cable runs
def cable_routes() -> dict[str, dict]:
    """Centre-line polylines, drawn as tubes by PyVista. Ethernet runs on the HMI's back are local to the HMI."""
    hp = lambda *p: tuple(hmi_pt(p))
    ex, ey, ez = cam_axes(HMI_CAM_DIR_L)
    cam_back = HMI_CAM_C_L - ey * 37.0 + ex * 12.0
    pex, pey, pez = cam_axes(PANEL_CAM_DIR)
    pcam_back = PANEL_CAM_C - pey * 30.0 - pez * 12.0
    lx = LCD_C[0]
    x, y, z = X3_C
    b = ADC_BOX
    eth_hmi_port = (-110.0, 14.0, -95.0)
    arm_cab = (-201.0, 77.0, -40.0)       # where the HMI arm meets the cabinet, local
    return {
        # ribbon cables (camera -> Pi)
        # zip-tied along the arm, which stays behind and above the camera, out of its view
        "ribbon_hmi": dict(color=RIBBON, r=2.2, group="hmicam_cable",
                           pts=[tuple(hmi_pt(cam_back)), hp(12, -214, 240), hp(12, -160, 266), hp(12, -105, 296),
                                hp(12, -50, 228), hp(12, 0, 172), hp(30, 24, 152), hp(70, 40, 128), hp(92, 44, 102)]),
        "ribbon_panel": dict(color=RIBBON, r=2.0, group="panelcam_cable",
                             pts=[tuple(pcam_back), (lx, 20, 1540), (lx, 90, 1590), (lx, 160, 1606), (lx, 210, 1614)]),
        # HMI Ethernet: the existing cable (HMI port -> arm -> cabinet), the same cable moved to the switch, and patches
        "eth_old": dict(color=ETH_OLD, r=3.0, group="eth_old",
                        pts=[hp(*eth_hmi_port), hp(-112, 30, -110), hp(-150, 60, -95), hp(-180, 72, -60),
                             hp(*arm_cab), hp(-235, 95, -40)]),
        "eth_moved": dict(color=ETH_OLD, r=3.0, group="eth_moved",
                          pts=[hp(-28 + 9, 36, -55), hp(-19, 50, -40), hp(-60, 62, -60), hp(-150, 66, -80),
                               hp(-180, 72, -60), hp(*arm_cab), hp(-235, 95, -40)]),
        "patch_hmi": dict(color=ETH_NEW, r=2.6, group="patch_hmi",
                          pts=[hp(-28 + 18 + 9, 36, -55), hp(-1, 46, -30), hp(-60, 40, -60), hp(-108, 26, -85),
                               hp(*eth_hmi_port)]),
        "patch_pi": dict(color=ETH_NEW, r=2.6, group="patch_pi",
                         pts=[hp(-28 + 36 + 9, 36, -55), hp(17, 48, -30), hp(60, 50, -10), hp(78, 44, 8)]),
        # STG1 tap: power-out and 0 V wires, breakout -> ADC box; USB, ADC box -> gland -> HMI camera Pi
        "wire_sig": dict(color=WIRE_RED, r=1.3, group="wires",
                         pts=[(x + 21, y - 20, z - 40), (x + 40, y - 40, z - 45), (x + 50, 380, 1150),
                              (b["x"][1] + 10, b["y"][1] - 20, b["z"][1] + 25), (b["x"][1] - 6, b["y"][1] - 20,
                                                                                b["z"][1] - 4)]),
        "wire_gnd": dict(color=WIRE_BLACK, r=1.3, group="wires",
                         pts=[(x + 21, y - 14, z - 52), (x + 44, y - 36, z - 57), (x + 54, 384, 1145),
                              (b["x"][1] + 14, b["y"][1] - 14, b["z"][1] + 25), (b["x"][1] - 6, b["y"][1] - 14,
                                                                                 b["z"][1] - 4)]),
        "usb": dict(color=USB_BLACK, r=2.4, group="usb",
                    pts=[(b["x"][1] - 6, b["y"][0] + 20, b["z"][0] + 4), (b["x"][1] + 20, b["y"][0] + 10, b["z"][0] - 30),
                         (470, 250, 1100), (GLAND[0] - 10, GLAND[1] - 30, 1450), (GLAND[0], GLAND[1], FZ1 + 10),
                         (GLAND[0] + 30, GLAND[1] - 20, FZ1 + 22), (FX1 - 10, 190, FZ1 + 12), (FX1 + 20, 190, 1460),
                         hp(-150, 70, -20), hp(-60, 62, 0), hp(40, 50, 10), hp(70, 44, 6)]),
    }


# ------------------------------------------------------------------------------------- framing check
def fov_check(cam_c, cam_dir, corners, fov) -> dict:
    """Angles of each target corner off the camera's axis (horizontal, vertical), against the lens's half-FOV."""
    ex, ey, ez = cam_axes(cam_dir)
    out = []
    for c in corners:
        v = np.asarray(c, float) - cam_c
        h = math.degrees(math.atan2(float(v @ ex), float(v @ ey)))
        w = math.degrees(math.atan2(float(v @ ez), float(v @ ey)))
        out.append((round(h, 1), round(w, 1)))
    hmax = max(abs(h) for h, _ in out)
    vmax = max(abs(v) for _, v in out)
    return dict(corners_deg=out, h_used=round(2 * hmax, 1), v_used=round(2 * vmax, 1), fov=fov,
                fits=bool(hmax < fov[0] / 2 and vmax < fov[1] / 2), dist_mm=round(float(np.linalg.norm(
                    np.mean(np.asarray(corners), axis=0) - cam_c)), 1))


def framing() -> dict:
    a, b = ACTIVE[0] / 2, ACTIVE[1] / 2
    hmi_corners = [hmi_pt((sx * a, -20.5, sz * b)) for sx in (-1, 1) for sz in (-1, 1)]
    hmi = fov_check(hmi_pt(HMI_CAM_C_L), hmi_vec(HMI_CAM_DIR_L), hmi_corners, WIDE_FOV)
    lx, ly, lz = LCD_C
    lcd_corners = [np.array([lx + sx * LCD_SIZE[0] / 2, ly - 1, lz + sz * LCD_SIZE[1] / 2]) for sx in (-1, 1)
                   for sz in (-1, 1)]
    panel = fov_check(PANEL_CAM_C, PANEL_CAM_DIR, lcd_corners, STD_FOV)
    pan_corners = [np.array([lx + sx * 70, 193.0, PANEL_C[2] + sz * 97.5]) for sx in (-1, 1) for sz in (-1, 1)]
    whole = fov_check(PANEL_CAM_C, PANEL_CAM_DIR, pan_corners, STD_FOV)
    return dict(hmi_screen_wide=hmi, gu500_lcd_std=panel, gu500_whole_panel_std=whole)


# ------------------------------------------------------------------------------------------ meshes
CACHE = HERE / "viz3d" / ".cache"


def meshes(force=False) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha1(Path(__file__).read_bytes() + (HERE / "viz3d" / "model.py").read_bytes()).hexdigest()[:12]
    path = CACHE / f"integration_{h}.pkl"
    if path.exists() and not force:
        return pickle.loads(path.read_bytes())
    out = {}
    for p in parts():
        out[p.name] = dict(whole=M.tess(p.shape, p.tol), color=p.color, group=p.group, opacity=p.opacity)
    path.write_bytes(pickle.dumps(out))
    return out


if __name__ == "__main__":
    import json
    import time
    t = time.time()
    ms = meshes(force=True)
    print(f"{len(ms)} parts in {time.time() - t:.1f} s")
    for k, v in ms.items():
        print(f"  {k:18s} {v['group']:16s} {v['whole'].n_cells if v['whole'] is not None else 0:6d} tris")
    print(json.dumps(framing(), indent=1))
