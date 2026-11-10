"""Schematic CadQuery model for the M2 single-track process animation (steps.py).

Millimetres, z up, the M2's build plane at z = 0. The build plate follows Nathan C.'s photo of it (PR #243; sizes in
layout.py): about 10 in square, with four removable square panels in pockets and a hole near each corner. Its
thickness (about 1 in) is read off the same photo; the panels' thickness (1/2 in) and what their four holes are for
(counterbored screws are drawn) are assumptions. Nothing else is measured on BYU's machine or tools: the M2 is a box
with a process chamber, dose / build / overflow wells, a recoater, a scanner window and a gas inlet and outlet, laid out
like a Concept Laser machine; the bench tools are generic shapes. What comes from the plan
(../m2-single-track-schedule.md): two rows of nine 8 mm tracks per insert at 2 mm pitch (a 25 mm block at each panel's
centre), the cut sequence (block out of the panel, top slab off, split per row, final face 1-2 mm from mid-length,
grind to it), 1.25 in hot-mount pucks, the grit and polish sequence, and SEM.

``meshes()`` tessellates everything into PyVista and caches it in ``.cache/`` keyed on this file's hash.
"""
from __future__ import annotations

import hashlib
import pickle
from pathlib import Path

import cadquery as cq
import numpy as np
import pyvista as pv

import layout as L

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"

# ------------------------------------------------------------------------------------------------ layout
FLOOR_Z = -1000.0
CAB = dict(x=(-720.0, 1000.0), y=(-430.0, 520.0), z=(FLOOR_Z, 980.0))
CHAMBER = dict(x=(-500.0, 500.0), y=(-300.0, 300.0), z=(-20.0, 520.0))     # deck top is z = 0
FRONT_OPEN = dict(x=(-470.0, 470.0), z=(30.0, 480.0))
DOSE = dict(x=(-435.0, -175.0), y=(-130.0, 130.0))
BUILD = dict(x=(-130.0, 130.0), y=(-130.0, 130.0))
OVER = dict(x=(185.0, 265.0), y=(-130.0, 130.0))
WELL_Z = -430.0
PLATE_T = 25.4                         # about 1 in, read off the photo
PLATE_R = 16.0                         # corner radius, from the photo
PLATE_HOLE_R = 5.5
POCKET_R = 8.0
PANEL_T = 12.7                         # assumed (1/2 in): the pockets are drawn blind, as deep as a panel
PANEL_R = 6.0
PANEL_HOLE_R, PANEL_CB_R, PANEL_CB_D = 2.75, 4.75, 5.5     # through hole, counterbore radius and depth (assumed)
_h = L.POCKET_PITCH / 2
INSERT_C = {"A": (-_h, -_h), "B": (_h, -_h), "C": (-_h, _h), "D": (_h, _h)}   # panel centres; outlet side is -y
PANEL_LO, PANEL_HI = L.BLOCK / 2 - L.PANEL / 2, L.BLOCK / 2 + L.PANEL / 2     # the panel in block coordinates
RECOATER_PARK = -472.0
RECOATER_END = 292.0
SCANNER = np.array([0.0, 0.0, 520.0])
DOOR_HINGE = np.array([-492.0, -436.0, 0.0])

BENCH_Z = -100.0                       # bench top
BENCH = dict(x=(1300.0, 3850.0), y=(-380.0, 380.0))
TRAY_C = (1420.0, -175.0)               # 2 x 2 tray for the four panels
COPY_C = (1420.0, 140.0)               # copy stand for the top-view images
SAW_X = 1700.0                         # bandsaw blade plane (x = SAW_X)
SAW_TABLE_Z = -20.0
PSAW_X = 2050.0                        # precision saw disc plane
PSAW_C = (PSAW_X, 0.0, -18.0)          # disc centre
PSAW_R = 63.5                          # 5 in blade
PSAW_SAMPLE_Z = 60.0                   # bottom of the sample in the chuck, before the cut
PRESS_C = (2380.0, 0.0)
PRESS_TOP = 120.0
POL_C = (2720.0, 0.0)
POL_Z = 14.0                           # pad surface
SEM_C = (3120.0, 0.0)
SEM_STAGE_Z = 15.0
MON_C = (3560.0, 40.0)                 # monitor: screen centre x, y
MON_W, MON_H, MON_Z0 = 560.0, 350.0, 30.0

PUCK_R = 31.75 / 2                     # 1.25 in
PUCK_H = 18.0
SLAB_T = 7.0                           # top slab thickness taken off on the bandsaw
SPLIT_X = 12.5                         # between the rows
FINAL_CUT_X = 8.5                      # 1.5 mm past row 1's mid-length (x = 7)
TARGET_X = 7.0                         # row 1 mid-length: the section plane
KERF = 0.9

# colours
STEEL = (0.74, 0.75, 0.77)
INSERT_STEEL = (0.80, 0.81, 0.83)
DARK = (0.22, 0.23, 0.25)
PAINT = (0.90, 0.91, 0.92)
PAINT_DARK = (0.55, 0.58, 0.62)
ACCENT = (0.16, 0.36, 0.64)
GLASS = (0.70, 0.82, 0.92)
POWDER = (0.50, 0.51, 0.53)
BAKELITE = (0.13, 0.13, 0.14)
WOOD = (0.86, 0.80, 0.70)
FLOOR = (0.965, 0.965, 0.96)


def bx(x0, x1, y0, y1, z0, z1) -> cq.Workplane:
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl_z(cx, cy, z0, z1, r) -> cq.Workplane:
    return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((cx, cy, z0))


def cyl_x(x0, x1, cy, cz, r) -> cq.Workplane:
    return cq.Workplane("YZ").circle(r).extrude(x1 - x0).translate((x0, cy, cz))


def cyl_y(y0, y1, cx, cz, r) -> cq.Workplane:
    return cq.Workplane("XZ").circle(r).extrude(-(y1 - y0)).translate((cx, y0, cz))


# ----------------------------------------------------------------------------------------------- the M2
def m2_parts() -> dict:
    p = {}
    cab = bx(CAB["x"][0], CAB["x"][1], CAB["y"][0], CAB["y"][1], CAB["z"][0], CAB["z"][1])
    cab = cab.cut(bx(*CHAMBER["x"], *CHAMBER["y"], *CHAMBER["z"]))
    cab = cab.cut(bx(FRONT_OPEN["x"][0], FRONT_OPEN["x"][1], CAB["y"][0] - 1, CHAMBER["y"][0] + 1, *FRONT_OPEN["z"]))
    for w in (DOSE, BUILD, OVER):
        cab = cab.cut(bx(w["x"][0] - 3, w["x"][1] + 3, w["y"][0] - 3, w["y"][1] + 3, WELL_Z, 0.0))
    p["cabinet"] = (cab, PAINT, "m2", 1.0)
    p["cabinet_stripe"] = (bx(CAB["x"][0], CAB["x"][1], CAB["y"][0] - 2, CAB["y"][0], 600, 640), ACCENT, "m2", 1.0)
    p["plinth"] = (bx(CAB["x"][0] + 10, CAB["x"][1] - 10, CAB["y"][0] - 2, CAB["y"][0], FLOOR_Z, FLOOR_Z + 90),
                   PAINT_DARK, "m2", 1.0)
    p["hmi"] = (bx(640, 940, CAB["y"][0] - 40, CAB["y"][0], 230, 470), DARK, "m2", 1.0)
    p["hmi_screen"] = (bx(655, 925, CAB["y"][0] - 42, CAB["y"][0] - 39, 245, 455), (0.30, 0.52, 0.74), "m2", 1.0)
    # deck with the three openings
    deck = bx(-500, 500, -300, 300, -20, 0)
    for w in (DOSE, BUILD, OVER):
        deck = deck.cut(bx(w["x"][0] - 3, w["x"][1] + 3, w["y"][0] - 3, w["y"][1] + 3, -21, 1))
    p["deck"] = (deck, STEEL, "m2", 1.0)
    for s in (-1, 1):
        p[f"rail_{s}"] = (bx(-500, 500, s * 240 - 12, s * 240 + 12, 0, 12), DARK, "m2", 1.0)
    # gas inlet (back) and outlet (front)
    inlet = bx(-260, 260, 282, 300, 6, 50)
    outlet = bx(-260, 260, -300, -282, 6, 50)
    for i in range(12):
        x = -240 + i * 40
        inlet = inlet.cut(bx(x, x + 28, 281, 284, 14, 42))
        outlet = outlet.cut(bx(x, x + 28, -284, -281, 14, 42))
    p["gas_inlet"] = (inlet, (0.45, 0.60, 0.78), "m2", 1.0)
    p["gas_outlet"] = (outlet, DARK, "m2", 1.0)
    p["scanner_window"] = (cyl_z(0, 0, 512, 520, 46), (0.12, 0.14, 0.18), "m2", 1.0)
    p["scanner_ring"] = (cyl_z(0, 0, 508, 520, 60).cut(cyl_z(0, 0, 507, 521, 47)), DARK, "m2", 1.0)
    # build platform (moves) and its piston rod; plate rides on it
    p["platform"] = (bx(-127, 127, -127, 127, -75, -PLATE_T), PAINT_DARK, "platform", 1.0)
    p["platform_rod"] = (cyl_z(0, 0, WELL_Z, -75, 32), STEEL, "platform", 1.0)
    p["plate"] = (plate_shape(), (0.62, 0.64, 0.67), "platform", 1.0)
    # pocket floors a shade darker, so an empty pocket and the gap round a panel read as recessed (as in the photo)
    q = L.POCKET / 2
    floors = None
    for cx, cy in INSERT_C.values():
        f = bx(cx - q, cx + q, cy - q, cy + q, -PANEL_T, -PANEL_T + 0.2).edges("|Z").fillet(POCKET_R)
        floors = f if floors is None else floors.union(f)
    p["pocket_floors"] = (floors, (0.36, 0.37, 0.39), "platform", 1.0)
    # dose: piston, and the powder column above it (scaled in z by the animation)
    p["dose_piston"] = (bx(-433, -177, -128, 128, -330, -300), PAINT_DARK, "m2", 1.0)
    p["dose_powder"] = (bx(-433, -177, -128, 128, -300, 0), POWDER, "dose_powder", 1.0)
    p["overflow_powder"] = (bx(187, 263, -128, 128, -330, -300), POWDER, "m2", 1.0)
    # recoater carriage (group moves along x)
    rec = bx(-22, 22, -252, 252, 14, 70).union(bx(-14, 14, -150, 150, 10, 16))
    p["recoater"] = (rec, ACCENT, "recoater", 1.0)
    p["recoater_blade"] = (bx(-3, 3, -146, 146, 0.0, 12), DARK, "recoater", 1.0)
    # door: glass in a frame, hinged at its left edge
    fx0, fx1, fz0, fz1 = -492, 492, 18, 492
    frame = bx(fx0, fx1, -442, -432, fz0, fz1).cut(bx(fx0 + 26, fx1 - 26, -443, -431, fz0 + 26, fz1 - 26))
    p["door_frame"] = (frame, DARK, "door", 1.0)
    p["door_glass"] = (bx(fx0 + 26, fx1 - 26, -439, -435, fz0 + 26, fz1 - 26), GLASS, "door", 0.22)
    p["door_handle"] = (bx(fx1 - 60, fx1 - 40, -470, -442, 200, 320), STEEL, "door", 1.0)
    return p


def plate_shape() -> cq.Workplane:
    """Nathan C.'s plate (top at z = 0): rounded corners, a through hole near each corner, four blind pockets."""
    a = L.PLATE / 2
    plate = bx(-a, a, -a, a, -PLATE_T, 0).edges("|Z").fillet(PLATE_R)
    c = a - L.PLATE_HOLE_IN
    for sx in (-1, 1):
        for sy in (-1, 1):
            plate = plate.cut(cyl_z(sx * c, sy * c, -PLATE_T - 1, 1, PLATE_HOLE_R))
    q = L.POCKET / 2
    for cx, cy in INSERT_C.values():
        plate = plate.cut(bx(cx - q, cx + q, cy - q, cy + q, -PANEL_T, 1).edges("|Z").fillet(POCKET_R))
    return plate


def panel_shape(letter: str) -> cq.Workplane:
    """One removable 316L panel in block coordinates (the track block's top face [0,25]^2 at z = 0, at the panel's
    centre): rounded corners, four counterbored holes, the ID engraved on the front (-y) side and an orientation notch
    on that side near its left end."""
    lo, hi = PANEL_LO, PANEL_HI
    b = bx(lo, hi, lo, hi, -PANEL_T, 0).edges("|Z").fillet(PANEL_R)
    c = L.BLOCK / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = c + sx * L.PANEL_HOLE, c + sy * L.PANEL_HOLE
            b = b.cut(cyl_z(hx, hy, -PANEL_T - 1, 1, PANEL_HOLE_R)).cut(cyl_z(hx, hy, -PANEL_CB_D, 1, PANEL_CB_R))
    b = b.cut(bx(lo + 14, lo + 16, lo - 1, lo + 1.2, -PANEL_T - 1, 1))
    txt = cq.Workplane("XZ", origin=(c, lo, -PANEL_T / 2)).text(letter, 8, -0.6, combine=False, halign="center",
                                                                 valign="center")
    return b.cut(txt)


# --------------------------------------------------------------------------------------------- the bench
def tray_slots():
    """Centres of the tray's four recesses, in the plate's order: A, B at the front, C, D behind."""
    tx, ty = TRAY_C
    return [(tx - 47, ty - 47), (tx + 47, ty - 47), (tx - 47, ty + 47), (tx + 47, ty + 47)]


def bench_parts() -> dict:
    p = {}
    x0, x1 = BENCH["x"]
    y0, y1 = BENCH["y"]
    p["floor"] = (bx(-1600, 4400, -1500, 1400, FLOOR_Z - 2, FLOOR_Z), FLOOR, "static", 1.0)
    p["bench"] = (bx(x0, x1, y0, y1, BENCH_Z - 40, BENCH_Z), WOOD, "static", 1.0)
    for lx in (x0 + 30, x1 - 70):
        for ly in (y0 + 30, y1 - 70):
            p[f"bench_leg_{lx:.0f}_{ly:.0f}"] = (bx(lx, lx + 40, ly, ly + 40, FLOOR_Z, BENCH_Z - 40), PAINT_DARK,
                                                 "static", 1.0)
    # tray for the four panels, 2 x 2
    tx, ty = TRAY_C
    tray = bx(tx - 100, tx + 100, ty - 100, ty + 100, BENCH_Z, BENCH_Z + 10)
    for cx, cy in tray_slots():
        tray = tray.cut(bx(cx - 44, cx + 44, cy - 44, cy + 44, BENCH_Z + 6, BENCH_Z + 11))
    p["tray"] = (tray, (0.30, 0.42, 0.58), "static", 1.0)
    # copy stand + camera for the top-view images
    cx, cy = COPY_C
    p["copy_base"] = (bx(cx - 90, cx + 90, cy - 70, cy + 110, BENCH_Z, BENCH_Z + 14), DARK, "static", 1.0)
    p["copy_column"] = (cyl_z(cx, cy + 90, BENCH_Z + 14, BENCH_Z + 420, 12), STEEL, "static", 1.0)
    p["copy_arm"] = (bx(cx - 15, cx + 15, cy - 10, cy + 95, BENCH_Z + 330, BENCH_Z + 350), STEEL, "static", 1.0)
    p["camera_body"] = (bx(cx - 45, cx + 45, cy - 35, cy + 35, BENCH_Z + 290, BENCH_Z + 330), DARK, "static", 1.0)
    p["camera_lens"] = (cyl_z(cx, cy, BENCH_Z + 230, BENCH_Z + 290, 24), (0.12, 0.12, 0.13), "static", 1.0)
    # bandsaw (benchtop, schematic): table, column, upper arm and guide, blade in the plane x = SAW_X
    s = SAW_X
    p["saw_pedestal"] = (bx(s - 80, s + 80, -80, 160, BENCH_Z, SAW_TABLE_Z - 15), (0.25, 0.45, 0.35), "static", 1.0)
    table = bx(s - 110, s + 110, -120, 120, SAW_TABLE_Z - 15, SAW_TABLE_Z).cut(bx(s - 2, s + 2, -20, 20, -60, 10))
    p["saw_table"] = (table, STEEL, "static", 1.0)
    p["saw_column"] = (bx(s - 40, s + 40, 150, 200, SAW_TABLE_Z - 15, 330), (0.25, 0.45, 0.35), "static", 1.0)
    p["saw_arm"] = (bx(s - 40, s + 40, -40, 200, 270, 330), (0.25, 0.45, 0.35), "static", 1.0)
    p["saw_guide"] = (bx(s - 12, s + 12, -14, 30, 70, 270), DARK, "static", 1.0)
    p["saw_blade"] = (bx(s - 0.45, s + 0.45, -7, 7, SAW_TABLE_Z - 15, 70), (0.42, 0.44, 0.48), "static", 1.0)
    p["saw_coolant"] = (cyl_y(-20, 60, s + 30, 90, 3).union(cyl_z(s + 30, -20, 40, 90, 3)), (0.2, 0.5, 0.8),
                        "static", 1.0)
    # precision saw: base, trough, disc (spins about x), sample arm
    ps = PSAW_X
    p["psaw_base"] = (bx(ps - 110, ps + 110, -120, 170, BENCH_Z, -40), (0.86, 0.86, 0.84), "static", 1.0)
    trough = bx(ps - 40, ps + 40, -80, 80, -40, -10).cut(bx(ps - 34, ps + 34, -74, 74, -36, -9))
    p["psaw_trough"] = (trough, (0.80, 0.80, 0.80), "static", 0.6)
    disc = cyl_x(ps - 0.25, ps + 0.25, PSAW_C[1], PSAW_C[2], PSAW_R)
    p["psaw_disc"] = (disc, (0.55, 0.42, 0.25), "psaw_disc", 1.0)
    hub = cyl_x(ps - 4, ps + 4, PSAW_C[1], PSAW_C[2], 18).union(bx(ps - 4.5, ps + 4.5, -2, 2, PSAW_C[2], PSAW_C[2] + 30))
    p["psaw_hub"] = (hub, STEEL, "psaw_disc", 1.0)
    p["psaw_post"] = (bx(ps + 70, ps + 100, 120, 160, -40, 110), DARK, "static", 1.0)
    p["psaw_arm"] = (bx(ps - 12, ps + 100, -10, 150, 86, 100), DARK, "psaw_arm", 1.0)
    jaws = bx(ps - 8, ps - 2, -16.5, -12.6, PSAW_SAMPLE_Z + 1, 86).union(bx(ps - 8, ps - 2, 12.6, 16.5,
                                                                         PSAW_SAMPLE_Z + 1, 86))
    p["psaw_chuck"] = (jaws.union(bx(ps - 9, ps - 1, -17, 17, 78, 86)), STEEL, "psaw_arm", 1.0)
    # hot-mount press: body, mould ring, cap, ram
    px, py = PRESS_C
    p["press_body"] = (cyl_z(px, py, BENCH_Z, PRESS_TOP, 70), (0.25, 0.40, 0.62), "static", 1.0)
    p["press_panel"] = (bx(px - 40, px + 40, py - 72, py - 62, 0, 70), DARK, "static", 1.0)
    mould = cyl_z(px, py, PRESS_TOP, PRESS_TOP + 48, 26).cut(cyl_z(px, py, PRESS_TOP - 1, PRESS_TOP + 49,
                                                                    PUCK_R + 0.1))
    p["press_mould"] = (mould, STEEL, "press_mould", 0.35)
    p["press_cap"] = (cyl_z(px, py, PRESS_TOP + 48, PRESS_TOP + 62, 28), STEEL, "press_cap", 1.0)
    p["press_ram"] = (cyl_z(px, py, PRESS_TOP - 40, PRESS_TOP + 4, PUCK_R), STEEL, "press_ram", 1.0)
    # grinder-polisher: base, bowl, platen, pad (pad colour changes with the step)
    qx, qy = POL_C
    p["pol_base"] = (bx(qx - 150, qx + 150, qy - 150, qy + 170, BENCH_Z, 0), (0.88, 0.88, 0.86), "static", 1.0)
    bowl = cyl_z(qx, qy, 0, 34, 140).cut(cyl_z(qx, qy, 2, 35, 133))
    p["pol_bowl"] = (bowl, (0.80, 0.82, 0.84), "static", 1.0)
    p["pol_platen"] = (cyl_z(qx, qy, 2, POL_Z - 2, 128), STEEL, "pol_platen", 1.0)
    p["pol_pad"] = (cyl_z(qx, qy, POL_Z - 2, POL_Z, 127), (0.30, 0.30, 0.31), "pol_platen", 1.0)
    p["pol_mark"] = (bx(qx + 20, qx + 125, qy - 3, qy + 3, POL_Z, POL_Z + 0.3), (0.95, 0.95, 0.95), "pol_platen", 1.0)
    p["pol_tap"] = (cyl_z(qx - 110, qy + 120, 0, 120, 6).union(cyl_y(40, 120, qx - 110, 120, 6)), STEEL, "static", 1.0)
    # etch: dropper over the face-up puck (beside the polisher)
    p["dropper_tube"] = (cyl_z(0, 0, 0, 60, 3.0).union(cq.Workplane("XY").circle(0.6).workplane(offset=-12)
                                                       .circle(3.0).loft()), (0.85, 0.90, 0.95), "dropper", 0.55)
    p["dropper_bulb"] = (cyl_z(0, 0, 60, 85, 6.5), (0.75, 0.20, 0.18), "dropper", 1.0)
    # SEM: chamber, door, column, stage
    sx, sy = SEM_C
    p["sem_chamber"] = (bx(sx - 150, sx + 150, sy - 150, sy + 150, BENCH_Z, 190).cut(
        bx(sx - 135, sx + 135, sy - 135, sy + 135, BENCH_Z + 15, 175)).cut(
        bx(sx - 110, sx + 110, sy - 151, sy - 134, -70, 160)), (0.86, 0.87, 0.88), "sem", 1.0)
    p["sem_door"] = (bx(sx - 120, sx + 120, sy - 162, sy - 150, -80, 170), (0.80, 0.81, 0.83), "sem_door", 1.0)
    p["sem_door_handle"] = (bx(sx - 30, sx + 30, sy - 180, sy - 162, 120, 140), STEEL, "sem_door", 1.0)
    p["sem_column"] = (cyl_z(sx, sy, 190, 560, 58), (0.84, 0.85, 0.87), "sem", 1.0)
    p["sem_gun"] = (cyl_z(sx, sy, 560, 640, 42), (0.70, 0.72, 0.75), "sem", 1.0)
    pole = cq.Workplane("XY").workplane(offset=110).circle(10).workplane(offset=65).circle(46).loft()
    p["sem_pole"] = (pole.translate((sx, sy, 0)), (0.62, 0.64, 0.68), "sem", 1.0)
    p["sem_stage"] = (cyl_z(sx, sy, -10, SEM_STAGE_Z, 36).union(cyl_z(sx, sy, BENCH_Z + 15, -10, 12)), STEEL,
                      "sem", 1.0)
    # monitor
    mx, my = MON_C
    p["mon_stand"] = (bx(mx - 70, mx + 70, my + 10, my + 70, BENCH_Z, BENCH_Z + 10)
                      .union(bx(mx - 15, mx + 15, my + 40, my + 60, BENCH_Z + 10, MON_Z0 + 60)), DARK, "static", 1.0)
    p["mon_body"] = (bx(mx - MON_W / 2 - 12, mx + MON_W / 2 + 12, my, my + 25, MON_Z0 - 12, MON_Z0 + MON_H + 12), DARK,
                     "static", 1.0)
    return p


# ------------------------------------------------------------------------------- the sample's pieces
def pieces() -> dict:
    """Panel A and the pieces it is cut into, in block coordinates (the track block's top face [0,25]^2 at z = 0).

    panel -> (bandsaw, four cuts: a, b along y; c, d along x) the 25 mm track block + four offcuts
    -> (bandsaw) top slab + body -> (bandsaw) row slabs 1, 2 -> (precision saw) row-1 piece + offcut
    -> (grind) the section piece, whose face x = TARGET_X is row 1's mid-length."""
    a = L.BLOCK
    lo, hi = PANEL_LO - 1, PANEL_HI + 1
    zl, zh = -PANEL_T - 1, 1
    out = {}
    panel = panel_shape("A")
    out["panel"] = panel
    out["p1"] = panel.intersect(bx(0, hi, lo, hi, zl, zh))
    out["off_a"] = panel.intersect(bx(lo, -KERF, lo, hi, zl, zh))
    out["p2"] = out["p1"].intersect(bx(-1, a, lo, hi, zl, zh))
    out["off_b"] = out["p1"].intersect(bx(a + KERF, hi, lo, hi, zl, zh))
    out["p3"] = out["p2"].intersect(bx(-1, a + 1, 0, hi, zl, zh))
    out["off_c"] = out["p2"].intersect(bx(-1, a + 1, lo, -KERF, zl, zh))
    out["off_d"] = out["p3"].intersect(bx(-1, a + 1, a + KERF, hi, zl, zh))
    # the block, with its ID scribed again on the front of what becomes the slab (the panel's ID went with off_c)
    cube = out["p3"].intersect(bx(-1, a + 1, -1, a, zl, zh))
    txt = cq.Workplane("XZ", origin=(4.0, 0, -SLAB_T / 2)).text("A", 4.5, -0.4, combine=False, halign="center",
                                                                      valign="center")
    cube = cube.cut(txt)
    out["cube"] = cube
    out["body"] = cube.intersect(bx(-1, a + 1, -1, a + 1, zl, -SLAB_T - KERF))
    slab = cube.intersect(bx(-1, a + 1, -1, a + 1, -SLAB_T, 1))
    out["slab"] = slab
    out["row1"] = slab.intersect(bx(-1, SPLIT_X - KERF / 2, -1, a + 1, -SLAB_T - 1, 1))
    out["row2"] = slab.intersect(bx(SPLIT_X + KERF / 2, a + 1, -1, a + 1, -SLAB_T - 1, 1))
    out["piece_cut"] = slab.intersect(bx(-1, FINAL_CUT_X, -1, a + 1, -SLAB_T - 1, 1))
    out["offcut"] = slab.intersect(bx(FINAL_CUT_X + 0.5, SPLIT_X - KERF / 2, -1, a + 1, -SLAB_T - 1, 1))
    out["piece"] = slab.intersect(bx(-1, TARGET_X, -1, a + 1, -SLAB_T - 1, 1))
    return out


# --------------------------------------------------------------------------------------- tessellation
def to_mesh(shape, tol=0.5, ang=0.25) -> pv.PolyData:
    if isinstance(shape, cq.Workplane):
        vals = shape.vals()
        shape = vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)
    verts, tris = shape.tessellate(tol, ang)
    pts = np.array([(v.x, v.y, v.z) for v in verts], float)
    faces = np.hstack([np.r_[3, t] for t in tris]).astype(np.int64)
    m = pv.PolyData(pts, faces)
    return m.compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


def _hash() -> str:
    h = hashlib.sha256()
    for f in (Path(__file__), HERE / "layout.py"):
        h.update(f.read_bytes())
    return h.hexdigest()[:12]


def meshes() -> dict:
    """{name: dict(mesh, color, group, opacity)} for every fixed part, plus the panels' and panel A's pieces."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"meshes_{_hash()}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    out = {"parts": {}, "inserts": {}, "pieces": {}}
    for name, (shape, color, group, op) in {**m2_parts(), **bench_parts()}.items():
        tol = 2.0 if name in ("cabinet", "floor", "bench") else 0.6
        out["parts"][name] = dict(mesh=to_mesh(shape, tol), color=color, group=group, opacity=op)
    for k in L.INSERTS:
        out["inserts"][k] = to_mesh(panel_shape(k), 0.08)
    for k, shape in pieces().items():
        out["pieces"][k] = to_mesh(shape, 0.05)
    path.write_bytes(pickle.dumps(out))
    return out


if __name__ == "__main__":
    import time
    t = time.time()
    ms = meshes()
    print(len(ms["parts"]), "parts,", len(ms["pieces"]), "pieces", f"{time.time() - t:.1f} s")
    for k, v in ms["pieces"].items():
        print(k, [round(b, 2) for b in v.bounds])
