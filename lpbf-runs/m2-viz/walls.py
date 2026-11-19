"""The M2 wall build (../m2-single-track-schedule.md §4, "Walls on stepped parts") as seven 3-D animations, from the
job file to the comparison with the AM Module, in the style of steps.py (same machine, bench and Scene framework).

The build is the final sheet for 2026-11-20 (../m2-track-design/out/wall_sheet.csv, commit e094d8e): 2 squares x 3
parts x 7 walls = 42 walls, all along the recoater's travel; 33 sets, 32 Sobol settings in power, speed, spot and
trace spacing plus the 316L hatch as a control, 8 settings printed on both squares. The other two panels went to
another group and are drawn blank. Everything about the walls (colours, labels, the hottest walls) is read from the
sheet, so a new sheet only needs a re-render.

* ``m2w_1_setup``: B2 panels into the plate; A1 the job file (6 parts, 42 walls, 33 sets); B3 powder
* ``m2w_2_print``: B4 close and inert; B5 the bases, then the walls, layer by layer; one layer slowed down; what to
  watch (the hottest walls)
* ``m2w_3_unload``: B6 cool and depowder; B7 panels out and photographed; C1 number the parts, bandsaw them off
* ``m2w_4_section``: C2 part 1.1 on the precision saw, lengthwise 1.5 mm off its centreline, then between walls 4
  and 5; the section plane
* ``m2w_5_mount``: C3 hot-mount, cut face down (12 mounts); C4 grind 1.5 mm to the centreline, polish
* ``m2w_6_sem``: C5 SEM unetched for porosity; C4 etch; C5 the last layer's melt pools
* ``m2w_7_results``: C6 segment pores; C7 the map against the AM Module, what each wall records, the next build

The animation follows part 1.1 (square 1, part 1). The part's size is from
Carl's drawing and numbers (1.75 x 0.5 in base, 7 walls 0.05 in thick, 0.3 in tall; 0.4 in overall is read as the
total height, so the base is 0.1 in). Positions on the panels, the machine and the bench are illustrative.

    xvfb-run -a -s "-screen 0 1920x1080x24" python walls.py setup print unload section mount sem results
    PREVIEW=1 xvfb-run -a -s "-screen 0 1920x1080x24" python walls.py print    # last frame of each sub-step -> /tmp
    python walls.py full                                    # out/mp4/m2w_full.mp4 and its chapter list
"""
from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from functools import reduce
from pathlib import Path

import numpy as np
import pyvista as pv

import model as M
import scene as SC
import steps as ST
import walls_screens
from scene import R, S, Scene, T, mix, window

HERE = Path(__file__).resolve().parent
OUT = SC.OUT
FPS = SC.FPS
TITLE = "M2 wall build (#100)"
SHEET = HERE.parent / "m2-track-design" / "out" / "wall_sheet.csv"

# ------------------------------------------------------------------------------------------- the part (mm)
BASE_L, BASE_W, BASE_H = 44.45, 12.7, 2.54     # 1.75 x 0.5 in; 0.1 in thick if 0.4 in is the overall height
WALL_T, WALL_L, WALL_H = 1.27, 12.7, 7.62      # 0.05 in thick, across the 0.5 in width, 0.3 in tall
TOP = BASE_H + WALL_H
N_WALL = 7
PITCH = (BASE_L - WALL_T) / (N_WALL - 1)       # 7.20 mm with the end walls flush with the base's ends
WALL_X = [-BASE_L / 2 + WALL_T / 2 + i * PITCH for i in range(N_WALL)]
PART_GAP = 20.0                                # part centres on a panel (illustrative)
PANEL_OF = {1: "A", 2: "B"}                    # square -> panel; C and D went to another group (drawn blank)
SQUARES = tuple(PANEL_OF)
CUT_Y = 1.5                                    # the lengthwise cut, this far off the centreline
KERF = 0.6                                     # precision saw
X45 = (WALL_X[3] + WALL_X[4]) / 2              # the cut between walls 4 and 5
INF = 1e9

PART_C = (0.60, 0.61, 0.63)                    # as-built, matte
PANEL_C = M.INSERT_STEEL
CONTROL_C = (0.30, 0.30, 0.30)
HOT = (1.0, 0.70, 0.30)
PLANE_C = ST.PLANE_C
LASER_C = ST.LASER_C
POWDER_C = (0.45, 0.46, 0.48)
UP = (0, 0, 1)
A_C = np.array(M.INSERT_C["A"], float)
B_C = np.array(M.INSERT_C["B"], float)
P11 = (A_C[0] - PART_GAP, A_C[1])              # part 1.1's centre on the plate

CAM = dict(ST.CAM)
CAM.update({
    "plate_hi": [(-120, -330, 260), (0, -5, 0), UP],
    "top_hi": [(-10, -205, 250), (0, -2, 0), UP],
    "part11": [(P11[0] - 52, P11[1] - 70, 62), (P11[0], P11[1] - 2, 4), UP],
    "sq1": [(A_C[0] - 40, A_C[1] - 120, 95), (A_C[0], A_C[1], -2), UP],
    "sq1_top": [(P11[0] - 24, P11[1] - 21.6 - 30, 22), (P11[0], P11[1] - 21.6, -1), UP],
    "sq12": [(-20, -235, 150), (0, -60, -4), UP],                      # squares 1 and 2 (panels A and B)
    "deck_cut": [(-200, -500, 330), (0, 0, -40), UP],
    "tray_hi": [(1385, -430, 120), (1420, -170, -92), UP],
    "bandsaw": [(1610, -235, 120), (1708, -10, 20), UP],
    "bandsaw_far": [(1630, -300, 170), (1720, -20, 10), UP],
    "psaw_w": [(1990, -92, 50), (2050, -2, 30), UP],
    "psaw_x": [(1992, -88, 46), (2046, 0, 28), UP],
    "piece": [(2082, 52, 2), (2125, 110, -36), UP],
    "row24": [(2380, -660, 240), (2430, -240, -80), UP],
    "mon": [(M.MON_C[0], -880, 168), (M.MON_C[0], 40, 168), UP],   # lower than steps.py's: room for a caption warning
})


def rows() -> dict:
    with SHEET.open() as f:
        return {(int(r["square"]), int(r["part"]), int(r["wall"])): r for r in csv.DictReader(f)}


SETS = rows()


EA_LO, EA_HI = 1.0, 6.1                         # the design's range of energy per area P/(v h), J/mm^2
HOT_EA = 4.5                                   # "hottest walls": the top of that range


def ea(r) -> float:
    return float(r["E_area_J_mm2"])


def set_text(r, sep=", ") -> str:
    """'W011: 348 W, 705 mm/s, 140 µm, 0.13 mm' (the four fields Carl types)."""
    name = "control" if r["set"] == "C" else r["set"]
    return (f"{name}: {float(r['power_W']):.0f} W{sep}{float(r['speed_mm_s']):.0f} mm/s{sep}"
            f"{float(r['spot_um']):.0f} µm{sep}{float(r['trace_spacing_mm']):g} mm")


def wall_color(r) -> tuple:
    if r["set"] == "C":
        return CONTROL_C
    E = ea(r)
    f = (math.log(E) - math.log(EA_LO)) / (math.log(EA_HI) - math.log(EA_LO))
    x = min(max(f, 0.0), 0.999) * (len(ST.BLUE_RAMP) - 1)
    i = min(int(x), len(ST.BLUE_RAMP) - 2)
    return mix(ST.hex_rgb(ST.BLUE_RAMP[i]), ST.hex_rgb(ST.BLUE_RAMP[i + 1]), x - i)


# ------------------------------------------------------------------------------------------ geometry
def comb_boxes(xlo=-INF, xhi=INF, ylo=-INF, yhi=INF, h=TOP, walls=True, base=True):
    """The part's boxes (part coordinates: x along the base, y across it, z up from the panel), clipped and grown."""
    out = []

    def clip(b):
        x0, x1 = max(b[0], xlo), min(b[1], xhi)
        y0, y1 = max(b[2], ylo), min(b[3], yhi)
        z0, z1 = b[4], min(b[5], h)
        return (x0, x1, y0, y1, z0, z1) if (x1 - x0 > 1e-3 and y1 - y0 > 1e-3 and z1 - z0 > 1e-3) else None

    if base:
        out.append(clip((-BASE_L / 2, BASE_L / 2, -BASE_W / 2, BASE_W / 2, 0.0, BASE_H)))
    if walls:
        for x in WALL_X:
            out.append(clip((x - WALL_T / 2, x + WALL_T / 2, -WALL_L / 2, WALL_L / 2, BASE_H, TOP)))
    return [b for b in out if b is not None]


def mesh_of(boxes):
    if not boxes:
        return pv.Box((0, 0.01, 0, 0.01, 0, 0.01))
    return reduce(lambda a, b: a + b, [pv.Box(b) for b in boxes])


def wall_box(j, h=TOP):
    x = WALL_X[j]
    return (x - WALL_T / 2, x + WALL_T / 2, -WALL_L / 2, WALL_L / 2, BASE_H, max(BASE_H + 0.01, min(TOP, h)))


def base_box(h=TOP):
    return (-BASE_L / 2, BASE_L / 2, -BASE_W / 2, BASE_W / 2, 0.0, max(0.01, min(BASE_H, h)))


def part_pose(s, p):
    """Part s.p in its panel's centred coordinates: walls along x (the blade's travel), the base along y."""
    off = (p - 2) * PART_GAP
    return T((off, 0, 0)) @ R((0, 0, 1), 90)


def panel_world(k, dz=0.0):
    cx, cy = M.INSERT_C[k]
    return T((cx, cy, dz))


def on_tray(k):
    sx, sy = M.tray_slots()["ABCD".index(k)]
    return T((sx, sy, M.BENCH_Z + 6 + M.PANEL_T))


def bandsaw_pose(yf):
    """Panel A stood on its edge on the bandsaw table, its face toward the blade; the cut runs 1 mm into the panel
    (below the bases), with the panel fed so that its centre is at world y = yf."""
    return T((M.SAW_X + 1.0, yf, M.SAW_TABLE_Z + 44.0)) @ R((0, 1, 0), 90)


def psaw_len(dz=0.0):
    """Part 1.1 in the precision saw: the lengthwise cut (y = CUT_Y) in the disc plane, base down, lowered by dz."""
    return T((M.PSAW_X, 0.0, M.PSAW_SAMPLE_Z - dz)) @ R((0, 0, 1), -90) @ T((0, -CUT_Y, 0))


def psaw_cross(dz=0.0):
    """The kept half turned a quarter turn: the cut between walls 4 and 5 (x = X45) in the disc plane."""
    return T((M.PSAW_X, 0.0, M.PSAW_SAMPLE_Z - dz)) @ T((-X45, 0, 0))


# piece-local -> puck-local: the section face (part y = y_face) goes to the puck face z = 0, the piece's length along
# the puck's x, its height along the puck's y, the material up into the puck (0.2 mm proud so the faces don't fight)
def piece_in_puck(xc, y_face=CUT_Y):
    return np.array([[1, 0, 0, -xc], [0, 0, 1, -TOP / 2], [0, -1, 0, y_face - 0.2], [0, 0, 0, 1]], float)


PIECE_A = (-BASE_L / 2, X45 - KERF / 2)          # walls 1-4
PIECE_B = (X45 + KERF / 2, BASE_L / 2)           # walls 5-7
XC_A = sum(PIECE_A) / 2
PUCK_C = (0.0, 0.0, M.PUCK_H / 2)
PIECE_POSE = T((2125.0, 110.0, -40.0)) @ R((0, 0, 1), 180)     # piece A on the saw's base plate
ROW24 = [(2240.0 + 46.0 * (i % 6), -300.0 + 50.0 * (i // 6), M.BENCH_Z) for i in range(12)]


# ------------------------------------------------------------------------------------------- the world
class World:
    def __init__(self, sc: Scene, screens=False):
        self.sc = sc
        self.ms = M.meshes()
        self.rng = np.random.default_rng(3)
        self.flash = 0.0
        self.frame = 0
        sc.inset = self.inset
        for name, e in self.ms["parts"].items():
            kw = dict(ambient=1.0, diffuse=0.0, specular=0.0, smooth_shading=False) if name == "floor" else {}
            sc.add(name, e["mesh"], e["color"], e["group"], opacity=e["opacity"], **kw)
        sc.color["pol_pad"] = (0.30, 0.30, 0.31)
        sc.alpha["psaw_chuck"] = 0.0                       # sized for the track pieces; the part gets its own jaws
        # the four panels (centred), their screws
        for k in "ABCD":
            g = f"g_{k}"
            sc.add(f"pan_{k}", self.ms["inserts"][k].translate((-12.5, -12.5, 0), inplace=False), PANEL_C, g)
            sc.parent[g] = "platform"
            sc.gmat[g] = panel_world(k)
            for j, (x, y) in enumerate(M.screw_xy()):
                sc.add(f"scr_{k}_{j}", self.ms["screw"].translate((x - 12.5, y - 12.5, 0), inplace=False), M.DARK,
                       f"s_{k}", shown=False)
            sc.parent[f"s_{k}"] = "platform"
            sc.gmat[f"s_{k}"] = panel_world(k)
        # the six parts: base, seven walls, a mark at the wall-1 end; plus the job file's ghosts
        for s in SQUARES:
            for p in (1, 2, 3):
                g = f"part_{s}{p}"
                sc.parent[g] = f"g_{PANEL_OF[s]}"
                sc.gmat[g] = part_pose(s, p)
                sc.add(f"b{s}{p}", pv.Box(base_box()), PART_C, g, shown=False)
                sc.add(f"n{s}{p}", pv.Box((-BASE_L / 2 - 0.05, -BASE_L / 2 + 1.2, -1.2, 1.2, 0.6, BASE_H + 0.05)),
                       M.DARK, g, shown=False)
                sc.add(f"gb{s}{p}", pv.Box(base_box()), (0.80, 0.81, 0.83), g, opacity=0.55, shown=False)
                for j in range(N_WALL):
                    r = SETS[(s, p, j + 1)]
                    sc.add(f"w{s}{p}{j}", pv.Box(wall_box(j)), PART_C, g, shown=False)
                    sc.add(f"gw{s}{p}{j}", pv.Box(wall_box(j)), wall_color(r), g, opacity=0.9, shown=False,
                           ambient=0.45)
        # part 1.1's pieces after the saw (shown instead of b11/w11j from the section chapter on)
        pieces = {
            "half": comb_boxes(yhi=CUT_Y - KERF / 2),
            "offcut": comb_boxes(ylo=CUT_Y + KERF / 2),
            "pA": comb_boxes(xhi=PIECE_A[1], yhi=CUT_Y - KERF / 2),
            "pB": comb_boxes(xlo=PIECE_B[0], yhi=CUT_Y - KERF / 2),
            "pA0": comb_boxes(xhi=PIECE_A[1], yhi=0.0),
        }
        for n, bxs in pieces.items():
            sc.add(f"pc_{n}", mesh_of(bxs), PART_C, f"pc_{n}", shown=False)
        sc.add("plane_A", pv.Box((PIECE_A[0] + 0.2, PIECE_A[1] - 0.2, -0.05, 0.05, -0.3, TOP + 0.3)), PLANE_C, "pc_pA",
               opacity=0.55, ambient=0.6, specular=0.0, shown=False)
        # powder: the bed while building (a translucent block), the heap ahead of the blade
        sc.add("bed", pv.Box((-130, 130, -128, 128, -1.0, 0.0)), POWDER_C, "bed", opacity=0.42, specular=0.0,
               smooth_shading=False, shown=False)
        sc.add("bed_top", pv.Box((-130, 130, -128, 128, -0.06, -0.01)), POWDER_C, "static", opacity=0.55,
               specular=0.0, smooth_shading=False, shown=False)
        sc.add("powder_heap", pv.Box((4, 11, -140, 140, 0, 4.5)), M.POWDER, "recoater", specular=0.0,
               smooth_shading=False, shown=False)
        # laser, glow, spatter; gas arrows
        sc.add("beam", pv.Line((0, 0, 520), (0, 0, 0)).tube(radius=0.6), LASER_C, "fx", opacity=0.8, ambient=1.0,
               diffuse=0.0, specular=0.0, shown=False)
        sc.add("glow", pv.Sphere(radius=0.5), (1.0, 0.97, 0.8), "fx", ambient=1.0, diffuse=0.0, specular=0.0,
               shown=False)
        sc.add("trail", pv.Line((0, 0, 0), (0, 0, 0.01)).tube(radius=0.12), (1.0, 0.75, 0.35), "fx", ambient=1.0,
               diffuse=0.0, specular=0.0, shown=False)
        self.gas = []
        for j, x in enumerate((-85.0, 0.0, 85.0)):
            for m in range(3):
                n = f"gas_{j}_{m}"
                arrow = pv.Arrow(start=(0, 0, 0), direction=(0, -1, 0), scale=46, tip_length=0.32, tip_radius=0.16,
                                 shaft_radius=0.06)
                sc.add(n, arrow, ST.GAS_C, n, opacity=0.55, ambient=0.5, specular=0.0, shown=False)
                self.gas.append((n, x, m / 3.0))
        # the jaws that hold part 1.1 in the precision saw (on the arm, which lowers it)
        ps = M.PSAW_X
        jaw = pv.Box((ps - 9, ps - 2.5, -BASE_L / 2 - 4, -BASE_L / 2 - 0.05, M.PSAW_SAMPLE_Z - 2, 88)) + \
            pv.Box((ps - 9, ps - 2.5, BASE_L / 2 + 0.05, BASE_L / 2 + 4, M.PSAW_SAMPLE_Z - 2, 88)) + \
            pv.Box((ps - 10, ps - 1.5, -BASE_L / 2 - 4.5, BASE_L / 2 + 4.5, 80, 88))
        sc.add("jaws", jaw, M.STEEL, "psaw_arm", shown=False)
        # pucks: the one that follows piece A, the other 23 (12 shown in two rows)
        sc.add("puck", pv.Cylinder(center=(0, 0, M.PUCK_H / 2), direction=(0, 0, 1), radius=M.PUCK_R - 0.05,
                                   height=M.PUCK_H, resolution=60), M.BAKELITE, "puck", shown=False, specular=0.25)
        for i in range(1, 12):
            x, y, z = ROW24[i]
            sc.add(f"puck_{i}", pv.Cylinder(center=(x, y, z + M.PUCK_H / 2), direction=(0, 0, 1), radius=M.PUCK_R,
                                            height=M.PUCK_H, resolution=60), M.BAKELITE, "static", shown=False,
                   specular=0.25)
            hw = (PIECE_A[1] - PIECE_A[0]) / 2 if i % 2 == 0 else (PIECE_B[1] - PIECE_B[0]) / 2
            sc.add(f"puckface_{i}", pv.Box((x - hw, x + hw, y - TOP / 2, y + TOP / 2, z + M.PUCK_H, z + M.PUCK_H + 0.05)),
                   PANEL_C, "static", shown=False)
        sc.add("granules", pv.PolyData(np.zeros((1, 3))), (0.10, 0.10, 0.11), "fx", style="points", point_size=4,
               render_points_as_spheres=True, shown=False)
        sc.add("drop", pv.Sphere(radius=2.2), (0.95, 0.75, 0.25), "drop", ambient=0.5, shown=False)
        sc.add("film", pv.Cylinder(center=(0, 0, 0.15), direction=(0, 0, 1), radius=13, height=0.3),
               (0.95, 0.78, 0.30), "film", opacity=0.5, shown=False)
        sc.parent["film"] = "puck"
        sc.add("sem_beam", pv.Line((0, 0, 110), (0, 0, 33)).tube(radius=0.7), (0.55, 0.78, 1.0), "fx",
               opacity=0.85, ambient=1.0, diffuse=0.0, specular=0.0, shown=False)
        if screens:
            files = walls_screens.make_all(M.CACHE)
            mx, my = M.MON_C
            x0, x1, z0, z1, y = mx - M.MON_W / 2, mx + M.MON_W / 2, M.MON_Z0, M.MON_Z0 + M.MON_H, my - 0.8
            from PIL import Image
            for key, path in files.items():
                quad = pv.PolyData(np.array([[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1]], float),
                                   np.array([4, 0, 1, 2, 3]))
                quad.active_texture_coordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
                tex = pv.numpy_to_texture(np.asarray(Image.open(path).convert("RGB")))
                actor = sc.pl.add_mesh(quad, texture=tex, ambient=1.0, diffuse=0.0, specular=0.0)
                n = f"screen_{key}"
                sc.actors[n] = actor
                sc.group_of[n] = "static"
                sc.base_alpha[n] = 1.0
                sc.alpha[n] = 0.0
        # initial state: door open, dose empty, recoater parked
        sc.gmat["door"] = R((0, 0, 1), ST.OPEN_DEG, pivot=M.DOOR_HINGE)
        sc.gmat["recoater"] = T((M.RECOATER_PARK, 0, 0))
        sc.gmat["dose_powder"] = S((1, 1, 0.02), pivot=(0, 0, -300))
        sc.show(["dropper_tube", "dropper_bulb"], 0.0)

    # ----------------------------------------------------------------------------------------- helpers
    def inset(self, base):
        if self.flash > 0.01:
            a = min(1.0, self.flash)
            base = (base.astype(np.float32) * (1 - 0.85 * a) + 255 * 0.85 * a).astype(np.uint8)
        return base

    def parts(self, a=1.0, which=None):
        for s in SQUARES:
            for p in (1, 2, 3):
                if which and (s, p) not in which:
                    continue
                self.sc.show([f"b{s}{p}", f"n{s}{p}"] + [f"w{s}{p}{j}" for j in range(N_WALL)], a)

    def ghosts(self, a):
        for s in SQUARES:
            for p in (1, 2, 3):
                self.sc.show([f"gb{s}{p}"] + [f"gw{s}{p}{j}" for j in range(N_WALL)], a)

    def grow(self, h):
        sc = self.sc
        for s in SQUARES:
            for p in (1, 2, 3):
                sc.set_mesh(f"b{s}{p}", pv.Box(base_box(h)))
                sc.alpha[f"b{s}{p}"] = 1.0 if h > 0.02 else 0.0
                sc.alpha[f"n{s}{p}"] = 1.0 if h > BASE_H * 0.9 else 0.0
                for j in range(N_WALL):
                    sc.set_mesh(f"w{s}{p}{j}", pv.Box(wall_box(j, h)))
                    sc.alpha[f"w{s}{p}{j}"] = 1.0 if h > BASE_H + 0.05 else 0.0

    def screws(self, a):
        for k in "ABCD":
            self.sc.show([f"scr_{k}_{j}" for j in range(4)], a)

    def laser(self, on, spot=None):
        sc = self.sc
        sc.alpha["beam"] = sc.alpha["glow"] = 1.0 if on else 0.0
        if on:
            sc.set_mesh("beam", pv.Line(tuple(M.SCANNER), tuple(spot)).tube(radius=0.6, n_sides=10))
            sc.set_mesh("glow", pv.Sphere(radius=0.55, center=spot, theta_resolution=12, phi_resolution=12))

    def gas_flow(self, on_alpha):
        self.frame += 1
        for n, x, ph in self.gas:
            f = (ph + self.frame / (FPS * 2.4)) % 1.0
            self.sc.gmat[n] = T((x, 150 - 300 * f, 28))
            self.sc.alpha[n] = on_alpha * min(1.0, 4 * f, 4 * (1 - f))

    def world_of(self, s, p, local, h=0.0):
        """World position of a point in part s.p's coordinates while its panel sits in the plate lowered by h."""
        k = PANEL_OF[s]
        m = T((0, 0, -h)) @ panel_world(k) @ part_pose(s, p)
        return tuple((m @ np.r_[local, 1.0])[:3])

    def detach(self, s, p, world_matrix):
        g = f"part_{s}{p}"
        self.sc.parent.pop(g, None)
        self.sc.gmat[g] = world_matrix


def built(w: World):
    """State at the end of the build, before depowdering: parts complete, plate down by TOP, bed full."""
    sc = w.sc
    w.screws(1.0)
    w.grow(TOP)
    sc.gmat["door"] = np.eye(4)
    sc.gmat["dose_powder"] = S((1, 1, 0.55), pivot=(0, 0, -300))
    sc.gmat["platform"] = T((0, 0, -TOP))
    sc.gmat["bed"] = T((0, 0, 0)) @ S((1, 1, TOP), pivot=(0, 0, 0))
    sc.show(["bed", "bed_top"], 1.0)


def hot_walls(thr=HOT_EA):
    return [(s, p, j) for (s, p, jj), r in SETS.items() for j in [jj - 1] if r["set"] != "C" and ea(r) >= thr]


def repeat_twin(s, p, j):
    """Where else wall s.p.(j+1)'s setting is printed (the 8 repeats are on both squares), or None."""
    r = SETS[(s, p, j + 1)]
    for key, q in SETS.items():
        if q["set"] == r["set"] and key != (s, p, j + 1):
            return key
    return None


# =================================================================================================== 1 set up
def chapter_setup():
    sc = Scene("m2w_1_setup", f"{TITLE}: 1/7 set up")
    w = World(sc)
    sc.cam = CAM["m2_wide"]
    for k in "ABCD":
        sc.gmat[f"g_{k}"] = panel_world(k, 140)
        sc.alpha[f"pan_{k}"] = 0.0

    def drop_in(u):
        for j, k in enumerate("ABCD"):
            v = window(u, 0.08 + 0.15 * j, 0.33 + 0.15 * j)
            sc.gmat[f"g_{k}"] = panel_world(k, 140 * (1 - v))
            sc.alpha[f"pan_{k}"] = min(1.0, v * 4)
            s_in = window(u, 0.74 + 0.05 * j, 0.86 + 0.05 * j)
            sc.gmat[f"s_{k}"] = panel_world(k, 25 * (1 - s_in))
            sc.show([f"scr_{k}_{jj}" for jj in range(4)], s_in)

    sc.step("B2 · panels into the plate",
            "The 316L panels (about 88 mm square) go into Nathan C.'s plate and are screwed down. This build uses two "
            "of them, squares 1 and 2 (panels A and B here), with three parts each: 6 parts, 42 walls. The other two "
            "panels went to another group and are drawn blank.",
            5.0, drop_in, hold=0.8, cam_to=CAM["plate"],
            warn="a panel that sits proud of the plate meets the blade on the first layer. Dial-indicate every panel "
                 "flush before closing the door.")

    def job(u):
        w.ghosts(window(u, 0.05, 0.6))

    sq = {s: w.world_of(s, 2, (0, 0, TOP)) for s in SQUARES}
    n_big = len({r["set"] for r in SETS.values() if float(r["spot_um"]) > 130})
    sc.step("A1 · job file: 6 parts, 42 walls",
            "Each wall is its own part with its own set: the hatch and upskin power, speed, spot and trace spacing "
            "change, the contours stay. 33 sets: 32 Sobol settings and the 316L hatch (370 W, 1350 mm/s, 130 µm, "
            "0.09 mm) as a control. 8 settings are printed on both squares. The bases get the unchanged 316L set.",
            5.5, job, hold=2.2, cam_to=CAM["top_hi"], still=True,
            warn=f"in Carl's photos the Part parameter window greys out power and speed; make the sets under "
                 f"Parameter instead. {n_big} sets ask for a spot above 130 µm, more than his photos show: if WRX "
                 f"won't take one, ask rather than round it.",
            labels=[("square 1 (panel A)", sq[1], (0.06, 0.78)),
                    ("square 2 (panel B)", sq[2], (0.95, 0.78)),
                    ("darker blue = more energy per area\ngrey = the control", sq[2], (0.95, 0.45))])

    def one(u):
        pass

    p11 = lambda loc: w.world_of(1, 1, loc)  # noqa: E731
    jr = next(j for j in range(N_WALL) if repeat_twin(1, 1, j))      # a wall whose setting square 2 repeats
    tw = repeat_twin(1, 1, jr)
    sc.step("A1 · part 1.1",
            "Part 1.1. Its seven walls run along the blade's travel, like every wall in this build, each with its own "
            "power, speed, spot and trace spacing. Mark the wall-1 end of every base, so the wall-to-set map "
            "survives removal.",
            3.5, one, hold=2.4, cam_to=CAM["part11"],
            labels=[("wall 1, " + set_text(SETS[(1, 1, 1)]), p11((WALL_X[0], -WALL_L / 2, TOP)), (0.06, 0.25)),
                    (f"wall {jr + 1}: {SETS[(1, 1, jr + 1)]['set']}, also\nprinted as wall {tw[0]}.{tw[1]}.{tw[2]}",
                     p11((WALL_X[jr], -WALL_L / 2, TOP)), (0.95, 0.22)),
                    ("the wall-1 end: mark it", p11((-BASE_L / 2, 0, BASE_H)), (0.06, 0.60)),
                    ("base: the 316L set", p11((BASE_L / 2 - 3, -BASE_W / 2, 1.2)), (0.95, 0.66))])

    def powder(u):
        w.ghosts(1.0 - window(u, 0.0, 0.4))
        sc.gmat["dose_powder"] = S((1, 1, 0.02 + 0.98 * window(u, 0.25, 1.0)), pivot=(0, 0, -300))

    sc.step("B3 · powder",
            "Load sieved 316L powder into the dose chamber, and record the lot, its certificate and the particle size "
            "distribution: the AM Module needs them.",
            3.5, powder, hold=0.8, cam_to=CAM["deck"],
            labels=[("dose chamber", (-305, -60, 0), (0.06, 0.30)), ("build plate", (60, -100, 0), (0.95, 0.60))])
    return sc.save()


# ===================================================================================================== 2 print
def chapter_print():
    sc = Scene("m2w_2_print", f"{TITLE}: 2/7 print")
    w = World(sc)
    w.screws(1.0)
    sc.gmat["dose_powder"] = S((1, 1, 1.0), pivot=(0, 0, -300))
    sc.cam = CAM["deck"]

    def inert(u):
        sc.gmat["door"] = R((0, 0, 1), ST.OPEN_DEG * (1 - window(u, 0.0, 0.45)), pivot=M.DOOR_HINGE)
        w.gas_flow(window(u, 0.45, 0.6))
        sc.gauges = [("O₂", f"{20.9 * (1 - window(u, 0.45, 1.0)) + 0.1:4.1f} %"), ("gas", "flowing back to front")]

    sc.step("B4 · close up and inert",
            "Close the door and flood the chamber with shielding gas until the oxygen reading is under the machine's "
            "limit. Record the gas, the O₂ level and which way the gas flows across the plate.",
            4.0, inert, hold=0.5, cam_to=CAM["deck_cut"], live=True,
            warn="the gas-flow direction isn't known yet. Note it: spatter blows downstream, and it decides which "
                 "parts are exposed first.")

    n_sweeps = 5
    beds = {"h": 0.0}

    def build(h0, h1, walls, cam_pts):
        def upd(u):
            w.gas_flow(1.0 - window(u, 0.0, 0.15) if h0 == 0.0 else 0.0)
            h = h0 + (h1 - h0) * u
            beds["h"] = h
            w.grow(h)
            sc.gmat["platform"] = T((0, 0, -h))
            sc.alpha["bed"] = 1.0 if h > 0.05 else 0.0
            sc.alpha["bed_top"] = 1.0
            sc.gmat["bed"] = S((1, 1, max(h, 0.01)), pivot=(0, 0, 0))
            ph = (u * n_sweeps) % 1.0
            x = M.RECOATER_PARK + (M.RECOATER_END - M.RECOATER_PARK) * (ph / 0.5 if ph < 0.5 else (1 - ph) / 0.5)
            sc.gmat["recoater"] = T((x, 0, 0))
            sc.alpha["powder_heap"] = 1.0 if ph < 0.5 else 0.0
            # the laser flicks between parts while the blade is parked at either end
            s, p = SQUARES[int(u * 97) % len(SQUARES)], 1 + int(u * 211) % 3
            if walls:
                j = int(u * 331) % N_WALL
                loc = (WALL_X[j], -WALL_L / 2 + WALL_L * ((u * 23) % 1.0), TOP)
            else:
                loc = (-BASE_L / 2 + BASE_L * ((u * 17) % 1.0), -BASE_W / 2 + BASE_W * ((u * 29) % 1.0), BASE_H)
            spot = w.world_of(s, p, loc, h=h) if 0.55 < ph < 0.95 else None
            spot = (spot[0], spot[1], 0.02) if spot else None
            w.laser(spot is not None, spot)
            layers30, layers50 = h / 0.03, h / 0.05
            sc.gauges = [("height", f"{h:5.2f} mm"), ("layers", f"{layers30:4.0f} at 30 µm / {layers50:3.0f} at 50 µm")]
        return upd

    sc.step("B5 · the bases: the 316L set",
            "Recoat, expose, lower the platform, repeat. The bases go first, all with the 316L set, for 2.5 mm: about "
            "85 layers at 30 µm, or 51 at 50 µm.",
            6.0, build(0.0, BASE_H, False, None), hold=0.3, cam_to=CAM["plate_hi"])

    sc.step("B5 · the walls: one setting each",
            "Then the 42 walls, 7.6 mm more. Every layer the laser draws each wall's contour with the standard set and "
            "fills it with that wall's hatch. In all, roughly 340 layers at 30 µm (200 at 50 µm).",
            7.0, build(BASE_H, TOP, True, None), hold=0.3)

    # one wall layer, slowed down: contour, then the hatch, on part 1.1's wall 1
    xw = WALL_X[0]
    cont = [(xw - WALL_T / 2 + 0.03, -WALL_L / 2 + 0.03), (xw + WALL_T / 2 - 0.03, -WALL_L / 2 + 0.03),
            (xw + WALL_T / 2 - 0.03, WALL_L / 2 - 0.03), (xw - WALL_T / 2 + 0.03, WALL_L / 2 - 0.03),
            (xw - WALL_T / 2 + 0.03, -WALL_L / 2 + 0.03)]
    hatch = []
    h111 = float(SETS[(1, 1, 1)]["trace_spacing_mm"])
    xs = np.arange(xw - WALL_T / 2 + 0.11 + h111 / 2, xw + WALL_T / 2 - 0.11, h111)
    for i, x in enumerate(xs):
        y0, y1 = (-WALL_L / 2 + 0.11, WALL_L / 2 - 0.11) if i % 2 == 0 else (WALL_L / 2 - 0.11, -WALL_L / 2 + 0.11)
        hatch += [(x, y0), (x, y1)]
    path = cont + hatch
    seg = np.array([math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)])
    cum = np.r_[0, np.cumsum(seg)]

    def at(dist):
        i = min(int(np.searchsorted(cum, dist, side="right")) - 1, len(seg) - 1)
        f = (dist - cum[i]) / max(seg[i], 1e-9)
        a, b = np.array(path[i]), np.array(path[i + 1])
        return a + (b - a) * min(max(f, 0), 1)

    def slow(u):
        w.gas_flow(0.0)
        d = cum[-1] * SC.window(sc.u, 0.05, 0.95)
        p = at(d)
        spot = w.world_of(1, 1, (p[0], p[1], TOP), h=TOP)
        spot = (spot[0], spot[1], 0.06)
        w.laser(0.05 < sc.u < 0.95, spot)
        pts = [w.world_of(1, 1, (q[0], q[1], TOP + 0.06), h=TOP) for q in
               [at(x) for x in np.linspace(max(0.0, d - 6.0), d, 30)]]
        sc.set_mesh("trail", pv.Spline(np.array(pts), 60).tube(radius=0.11) if d > 0.2 else
                    pv.Line((0, 0, 0), (0, 0, 0.01)).tube(radius=0.05))
        sc.alpha["trail"] = 1.0 if 0.05 < sc.u < 0.98 else 0.0
        sc.gauges = [("wall", "1.1.1, " + set_text(SETS[(1, 1, 1)])),
                     ("now", "contour: standard set" if d < cum[len(cont) - 1] else "hatch: this wall's set")]

    sc.step("B5 · one wall layer, slowed down",
            f"One layer of wall 1.1.1, slowed down: the contour with the standard set, then the hatch, {h111:g} mm "
            "apart, with this wall's power, speed and spot. Whether the hatch runs along the wall (as drawn) or across "
            "it, and whether it turns each layer, decides what the etched section can show: check it in WRX's layer "
            "view.",
            8.0, slow, hold=0.4, cam_to=CAM["sq1_top"],
            warn="if the hatch runs across the wall, each vector is only about 1 mm long, mostly start and stop.")

    hot = hot_walls()

    def watch(u):
        w.gas_flow(0.0)
        w.laser(False)
        sc.alpha["trail"] = 0.0
        g = 0.5 + 0.5 * math.sin(sc.u * 2 * math.pi * 3)
        for s, p, j in hot:
            sc.color[f"w{s}{p}{j}"] = mix(PART_C, HOT, g)
        x = M.RECOATER_PARK + (M.RECOATER_END - M.RECOATER_PARK) * window(u, 0.25, 0.9)
        sc.gmat["recoater"] = T((x, 0, 0))
        sc.alpha["powder_heap"] = 1.0
        sc.gauges = [("watch", f"{len(hot)} walls at ≥ {HOT_EA:g} J/mm²"),
                     ("Ke", f"up to {max(float(r['Ke']) for r in SETS.values()):.0f}: the smallest spots")]

    h0 = hot[0] if hot else (1, 2, 0)
    lab_hot = w.world_of(h0[0], h0[1], (WALL_X[h0[2]], 0, TOP), h=TOP)
    ea_hot = sorted(ea(SETS[(s, p, j + 1)]) for s, p, j in hot) or [HOT_EA]
    k_small = [r for r in SETS.values() if float(r["Ke"]) >= 10]
    sc.step("B5 · what to watch",
            "Watch the first layers of the walls. A hot wall that swells above the powder can catch the blade. If one "
            "does, stop exposing that wall rather than the build, and note the layer.",
            6.0, watch, hold=0.6, cam_to=CAM["sq12"],
            warn=f"the hottest walls ({ea_hot[0]:.1f}-{ea_hot[-1]:.1f} J/mm², glowing) and the {len(k_small)} "
                 f"small-spot walls at Ke 10-15 are the likeliest to swell or spatter.",
            labels=[("hottest walls (glowing)", lab_hot, (0.06, 0.30))])
    return sc.save()


# ==================================================================================================== 3 unload
def chapter_unload():
    sc = Scene("m2w_3_unload", f"{TITLE}: 3/7 unload")
    w = World(sc)
    built(w)
    sc.cam = CAM["deck_cut"]

    def depowder(u):
        w.gas_flow(1.0 - window(u, 0.0, 0.2))
        a = 1.0 - window(u, 0.2, 0.8)
        sc.alpha["bed"] = a
        sc.alpha["bed_top"] = a
        sc.gmat["platform"] = T((0, 0, -TOP * (1 - window(u, 0.3, 0.9))))
        sc.gmat["bed"] = T((0, 0, TOP * window(u, 0.3, 0.9))) @ S((1, 1, TOP), pivot=(0, 0, 0))
        sc.gmat["door"] = R((0, 0, 1), ST.OPEN_DEG * window(u, 0.75, 1.0), pivot=M.DOOR_HINGE)

    sc.step("B6 · cool, de-inert, depowder",
            "Let it cool under gas, raise the platform, and vacuum the loose powder off (it goes back to the sieve).",
            5.0, depowder, hold=0.6, cam_to=CAM["plate_hi"])

    out = {k: on_tray(k) for k in "ABCD"}

    def lift(u):
        w.screws(1.0 - window(u, 0.0, 0.15))
        for j, k in enumerate("ABCD"):
            v = window(u, 0.15 + 0.12 * j, 0.55 + 0.12 * j)
            if v > 0:
                sc.parent.pop(f"g_{k}", None)
                sc.gmat[f"g_{k}"] = ST.blend(panel_world(k), out[k], v, (0, 0, 0), 260)
        sc.cam = ST.cam_via([CAM["plate_hi"], CAM["m2_wide"], CAM["tray_hi"]], window(u, 0.2, 1.0))
        w.flash = 1.0 - min(1.0, abs(u - 0.96) * 30) if u > 0.9 else 0.0

    sc.step("B7 · panels out, photographed",
            "Unscrew the panels and photograph squares 1 and 2 from above with their IDs, before anything is cut.",
            6.0, lift, hold=0.8)

    labs = []
    for p in (1, 2, 3):
        loc = (0, -BASE_W / 2, TOP)
        m = out["A"] @ part_pose(1, p)
        labs.append(tuple((m @ np.r_[loc, 1.0])[:3]))

    sc.step("C1 · number every part",
            "The six parts look alike. Before cutting, write square.part on each base with a paint pen (1.1 is "
            "square 1, part 1) and mark the wall-1 end. Write down which panel was square 1.",
            2.5, None, hold=2.5, cam_to=CAM["tray_hi"],
            labels=[("1.1", labs[0], (0.06, 0.25)), ("1.2", labs[1], (0.06, 0.55)),
                    ("1.3", labs[2], (0.95, 0.40))])

    rest = [T((M.SAW_X + 28 + 0 * j, -70.0 - 20 * j, M.SAW_TABLE_Z + 0.0)) @ R((0, 0, 1), 90) for j in range(3)]

    def bandsaw(u):
        # panel A from the tray onto the bandsaw table, on its edge, then fed through
        a0, a1 = out["A"], bandsaw_pose(70.0)
        if u < 0.25:
            sc.gmat["g_A"] = ST.blend(a0, a1, window(u, 0.0, 0.25), (0, 0, 0), 120)
            return
        yf = 70.0 - 140.0 * window(u, 0.28, 0.8)
        sc.gmat["g_A"] = bandsaw_pose(yf)
        for j, p in enumerate((1, 2, 3)):
            g = f"part_1{p}"
            if yf < -32 and u > 0.8:
                v = window(u, 0.8 + 0.04 * j, 0.95 + 0.0 * j)
                if g in sc.parent:
                    sc.parent.pop(g)
                start = bandsaw_pose(-70.0) @ part_pose(1, p)
                sc.gmat[g] = ST.blend(start, rest[j], v, (0, 0, TOP / 2), 10)

    sc.step("C1 · bandsaw the parts off",
            "Stand the panel on its edge and bandsaw about 1 mm into the panel, under the bases, not through them: "
            "the base is only about 2.5 mm thick, and the walls' roots must stay whole. The panel is used up.",
            8.0, bandsaw, hold=0.8, cam_to=CAM["bandsaw_far"],
            warn="the bases are only about 2.5 mm thick. Cut in the panel, not the base, so every wall's root "
                 "stays whole.",
            labels=[("blade 1 mm into the panel", (M.SAW_X, 0, 40), (0.95, 0.25))])
    return sc.save()


def removed(w: World):
    """End of chapter 3: panels in the tray, square 1's parts on the bandsaw table."""
    sc = w.sc
    w.grow(TOP)
    w.screws(0.0)
    for k in "ABCD":
        sc.parent.pop(f"g_{k}", None)
        sc.gmat[f"g_{k}"] = on_tray(k)
    sc.gmat["g_A"] = bandsaw_pose(-70.0)
    for j, p in enumerate((1, 2, 3)):
        sc.parent.pop(f"part_1{p}", None)
        sc.gmat[f"part_1{p}"] = T((M.SAW_X + 28, -70.0 - 20 * j, M.SAW_TABLE_Z)) @ R((0, 0, 1), 90)


# =================================================================================================== 4 section
def chapter_section():
    sc = Scene("m2w_4_section", f"{TITLE}: 4/7 section")
    w = World(sc)
    removed(w)
    sc.cam = CAM["bandsaw_far"]
    start = sc.gmat["part_11"].copy()
    drop = M.PSAW_DROP

    def to_saw(u):
        sc.cam = ST.cam_via([CAM["bandsaw_far"], CAM["saws"], CAM["psaw_w"]], window(u, 0.0, 0.3))
        sc.alpha["jaws"] = window(u, 0.2, 0.3)
        if u < 0.3:
            sc.gmat["part_11"] = ST.blend(start, psaw_len(0), window(u, 0.0, 0.3), (0, 0, TOP / 2), 160)
            return
        dz = drop * window(u, 0.32, 0.85)
        sc.gmat["psaw_disc"] = R((1, 0, 0), -2200 * u, pivot=M.PSAW_C)
        sc.gmat["psaw_arm"] = T((0, 0, -dz))
        sc.gmat["part_11"] = psaw_len(dz)
        if u > 0.85:
            w.parts(0.0, [(1, 1)])
            for n in ("half", "offcut"):
                sc.alpha[f"pc_{n}"] = 1.0
            sc.gmat["pc_half"] = psaw_len(drop)
            f = window(u, 0.85, 1.0)
            sc.gmat["pc_offcut"] = T((6 * f, 0, -40 * f * f)) @ psaw_len(drop)

    sc.step("C2 · lengthwise, 1.5 mm off the centreline",
            "Part 1.1 in the precision saw, its length in the blade's plane: one cut through the base and all seven "
            "walls, 1.5 mm off the centreline, on the side away from the wall-1 mark. Keep the offcut and label it: "
            "it holds a second plane through every wall.",
            8.0, to_saw, hold=0.6, cam_to=None,
            warn="clamp the part by its base and feed slowly: the 1.27 mm walls can bend or chatter in the cut.",
            labels=[("cut plane: 1.5 mm off the centreline", (M.PSAW_X, -20, 36), (0.95, 0.30))])

    def cross(u):
        sc.alpha["pc_offcut"] = 1.0 - window(u, 0.0, 0.1)
        if u < 0.3:
            sc.gmat["psaw_arm"] = T((0, 0, -drop * (1 - window(u, 0.0, 0.3))))
            sc.gmat["pc_half"] = ST.blend(psaw_len(drop), psaw_cross(0), window(u, 0.0, 0.3), (0, 0, TOP / 2), 40)
            sc.alpha["jaws"] = 1.0 - window(u, 0.0, 0.1)
            return
        dz = drop * window(u, 0.32, 0.85)
        sc.gmat["psaw_disc"] = R((1, 0, 0), -2200 * u, pivot=M.PSAW_C)
        sc.gmat["pc_half"] = psaw_cross(dz)
        if u > 0.85:
            sc.alpha["pc_half"] = 0.0
            sc.alpha["pc_pA"] = sc.alpha["pc_pB"] = 1.0
            sc.gmat["pc_pA"] = psaw_cross(drop)
            f = window(u, 0.85, 1.0)
            sc.gmat["pc_pB"] = T((5 * f, 0, -30 * f * f)) @ psaw_cross(drop)

    sc.step("C2 · between walls 4 and 5",
            "Turn the half a quarter turn and cut between walls 4 and 5, in the 5.9 mm gap: one piece with four walls "
            "(about 25 mm long) and one with three (about 19 mm). Each fits a 1.25 in mount.",
            7.0, cross, hold=0.6, cam_to=CAM["psaw_x"])

    pose = PIECE_POSE

    def show_plane(u):
        sc.gmat["pc_pA"] = ST.blend(psaw_cross(drop), pose, window(u, 0.0, 0.6), (XC_A, 0, TOP / 2), 60)
        sc.alpha["pc_pB"] = 1.0 - window(u, 0.0, 0.2)
        sc.alpha["plane_A"] = window(u, 0.6, 0.8)
        sc.gmat["plane_A"] = np.eye(4)

    sc.parent["plane_A"] = "pc_pA"
    lab_plane = tuple((pose @ np.r_[XC_A, 0.0, TOP, 1.0])[:3])
    lab_wall = tuple((pose @ np.r_[WALL_X[1], 0.0, TOP - 2, 1.0])[:3])
    sc.step("C2 · the section plane",
            "Red: the plane to grind to, the part's centreline. It crosses every wall at mid-length, through its 1.27 mm "
            "thickness and 7.6 mm height, and the base below. Grinding removes the last 1.5 mm.",
            4.0, show_plane, hold=2.4, cam_to=CAM["piece"], still=True,
            labels=[("section plane: each wall's mid-length", lab_plane, (0.95, 0.22)),
                    ("1.5 mm to grind away", lab_wall, (0.06, 0.30))])
    return sc.save()


# ===================================================================================================== 5 mount
def chapter_mount():
    sc = Scene("m2w_5_mount", f"{TITLE}: 5/7 mount and polish")
    w = World(sc)
    removed(w)
    w.parts(0.0, [(1, 1)])
    pose = PIECE_POSE
    sc.alpha["pc_pA"] = 1.0
    sc.gmat["pc_pA"] = pose
    sc.cam = CAM["piece"]
    seat = ST.face_down(ST.PRESS_SEAT)
    above = T((0, 0, 110)) @ seat
    in_puck = piece_in_puck(XC_A, CUT_Y)

    def mount(u):
        cap = max(window(u, 0.05, 0.2) * (1 - window(u, 0.58, 0.64)), window(u, 0.7, 0.76))
        sc.gmat["press_cap"] = T((0, 0, 70 * cap))
        # the piece rides to the press, then into the puck
        if u < 0.36:
            M_end = seat @ in_puck
            sc.gmat["pc_pA"] = ST.via([pose, T((0, 0, 140)) @ above @ in_puck, above @ in_puck, M_end],
                                      window(u, 0.0, 0.36), (XC_A, 0, TOP / 2))
            sc.parent.pop("pc_pA", None)
            sc.gmat["puck"] = seat
        else:
            sc.parent["pc_pA"] = "puck"
            sc.gmat["pc_pA"] = in_puck
            if u < 0.76:
                sc.gmat["puck"] = seat
        if 0.36 < u < 0.58:
            r = w.rng
            pts = np.c_[r.normal(0, 7, 50), r.normal(0, 7, 50), r.uniform(0, 1, 50)]
            f = window(u, 0.36, 0.58)
            pts[:, 0] += M.PRESS_C[0]
            pts[:, 1] += M.PRESS_C[1]
            pts[:, 2] = M.PRESS_TOP + 4 + 18 + 90 * (1 - f) * pts[:, 2]
            sc.set_mesh("granules", pv.PolyData(pts))
            sc.alpha["granules"] = 1.0
        else:
            sc.alpha["granules"] = 0.0
        sc.alpha["puck"] = window(u, 0.5, 0.66)
        heat = window(u, 0.62, 0.66) * (1 - window(u, 0.68, 0.74))
        sc.color["press_mould"] = mix(M.STEEL, (0.95, 0.45, 0.15), heat)
        if u >= 0.76:
            e = window(u, 0.76, 0.84)
            sc.gmat["press_ram"] = T((0, 0, 50 * e * (1 - window(u, 0.9, 1.0))))
            if u < 0.84:
                sc.gmat["puck"] = T((0, 0, 50 * e)) @ seat
            else:
                sc.gmat["puck"] = ST.blend(T((0, 0, 50)) @ seat, ST.face_up(ROW24[0]), window(u, 0.84, 1.0), PUCK_C, 90)

    sc.step("C3 · hot-mount, cut face down",
            "Hot-mount each piece with its cut face down, in conductive compound so the SEM doesn't charge. The walls "
            "stand up in the mould. Use a compound with good edge retention: the last layer's pools are at the very "
            "top edge of each wall.",
            7.0, mount, hold=0.4, cam_to=CAM["press"],
            warn="a rounded edge erases the last layer's pools, which sit at the very top of each wall.",
            labels=[("mounting press", (M.PRESS_C[0] - 26, 0, M.PRESS_TOP + 30), (0.06, 0.25))])

    def row(u):
        for i in range(1, 12):
            a = window(u, 0.05 * i / 1.2, 0.05 * i / 1.2 + 0.25)
            sc.alpha[f"puck_{i}"] = a
            sc.alpha[f"puckface_{i}"] = a

    sc.step("C3 · 12 mounts",
            "Two mounts a part, 12 in all. Engrave square.part.piece on the back of each mount. The parts holding the "
            "repeated settings and the controls give the first look at scatter.",
            3.0, row, hold=1.2, cam_to=CAM["row24"],
            labels=[("1.1, walls 1–4", (ROW24[0][0], ROW24[0][1], M.BENCH_Z + M.PUCK_H), (0.06, 0.30)),
                    ("1.1, walls 5–7", (ROW24[1][0], ROW24[1][1], M.BENCH_Z + M.PUCK_H), (0.95, 0.30))])

    up0 = ST.face_up(ROW24[0])
    down = ST.face_down(ST.POL_SPOT)

    def grind(u):
        if u < 0.3:
            sc.gmat["puck"] = ST.blend(up0, down, window(u, 0.0, 0.3), PUCK_C, 120)
            return
        sc.gmat["puck"] = down
        sc.gmat["pol_platen"] = R((0, 0, 1), -1100 * (u - 0.3), pivot=(M.POL_C[0], M.POL_C[1], 0))
        sc.color["pol_pad"] = (0.30, 0.28, 0.25)
        rem = 1.5 * window(u, 0.35, 0.95)
        sc.gauges = [("removed", f"{rem:4.2f} of 1.50 mm"), ("check", "puck height, micrometer")]
        if u > 0.95:
            sc.set_mesh("pc_pA", mesh_of(comb_boxes(xhi=PIECE_A[1], yhi=0.0)))

    sc.step("C4 · grind 1.5 mm to the centreline",
            "Grind away the 1.5 mm to the centreline on coarse paper. Measure the mount's height before and during, "
            "so you know when you're there; ±0.3 mm still cuts every wall near mid-length.",
            5.5, grind, hold=0.5, cam_to=CAM["pol"],
            warn="overshoot and the plane moves off mid-length. Measure the mount's height as you go.")

    pads = [("320 grit", (0.36, 0.34, 0.31)), ("800 grit", (0.55, 0.53, 0.50)), ("3 µm diamond", (0.93, 0.93, 0.91)),
            ("0.05 µm finish", (0.80, 0.87, 0.97))]

    def polish(u):
        sc.gmat["puck"] = down
        sc.gmat["pol_platen"] = R((0, 0, 1), -1300 * u, pivot=(M.POL_C[0], M.POL_C[1], 0))
        k = min(3, int(u * 4))
        sc.color["pol_pad"] = pads[k][1]
        sc.gauges = [("▶ " if j == k else "  ", name) for j, (name, _) in enumerate(pads)]

    sc.step("C4 · polish",
            "Then 320 and 800 grit, 3 µm diamond, and a 0.05 µm final polish. 316L is soft and can smear pores "
            "shut: on a few walls, re-polish and re-image to check the porosity doesn't change.",
            6.0, polish, hold=0.6,
            warn="316L smears and can close pores over. Re-grind 2-3 mounts 0.3 mm deeper and image them again: that "
                 "measures how much one section scatters.")
    return sc.save()


def mounted(w: World):
    sc = w.sc
    removed(w)
    w.parts(0.0, [(1, 1)])
    sc.alpha["pc_pA"] = 1.0
    sc.set_mesh("pc_pA", mesh_of(comb_boxes(xhi=PIECE_A[1], yhi=0.0)))
    sc.parent["pc_pA"] = "puck"
    sc.gmat["pc_pA"] = piece_in_puck(XC_A, 0.0)
    sc.alpha["puck"] = 1.0
    for i in range(1, 12):
        sc.show([f"puck_{i}", f"puckface_{i}"], 1.0)


# ======================================================================================================= 6 SEM
def chapter_sem():
    sc = Scene("m2w_6_sem", f"{TITLE}: 6/7 SEM")
    w = World(sc, screens=True)
    mounted(w)
    down = ST.face_down(ST.POL_SPOT)
    sc.gmat["puck"] = down
    sc.cam = CAM["pol"]
    stage = ST.face_up(ST.STAGE)

    def sem(u, after=None):
        door = window(u, 0.05, 0.25) * (1 - window(u, 0.55, 0.7))
        sc.gmat["sem_door"] = T((0, -230 * door, 0))
        sc.gmat["puck"] = ST.via([after if after is not None else down, T((0, -260, 160)) @ stage,
                                  T((0, 0, 40)) @ stage, stage], window(u, 0.2, 0.55), PUCK_C)
        g = window(u, 0.6, 0.75)
        for n in ("sem_chamber", "sem_door", "sem_door_handle"):
            sc.alpha[n] = 1.0 - 0.75 * g
        if u > 0.75:
            sx, sy = M.SEM_C
            k = int(u * 400) % 20
            sc.alpha["sem_beam"] = 1.0
            sc.set_mesh("sem_beam", pv.Line((sx, sy, 110), (sx - 10 + (u * 4000 % 20), sy - 3 + 0.3 * k,
                                                             ST.STAGE[2] + M.PUCK_H)).tube(radius=0.8))
        else:
            sc.alpha["sem_beam"] = 0.0

    sc.step("C5 · SEM, unetched: porosity first",
            "Into the SEM unetched: porosity is imaged before any etch, because etch pits look like pores. "
            "Backscattered electrons, about 100x, roughly six fields up each wall: about 250 fields for all 42 walls, "
            "so use the stage's automated tiling if the Apreo has it.",
            6.0, sem, hold=0.6, cam_to=CAM["sem"],
            warn="image porosity before any etch: etch pits look like pores.",
            labels=[("puck on the stage", (M.SEM_C[0], -10, ST.STAGE[2] + M.PUCK_H), (0.06, 0.62))])

    def to_screen(key, prev=None):
        def upd(u):
            sc.alpha["sem_beam"] = 0.0
            sc.alpha[f"screen_{key}"] = window(u, 0.3, 0.8)
            if prev:
                sc.alpha[f"screen_{prev}"] = 1.0 - window(u, 0.8, 0.9)
        return upd

    sc.step("C5 · each wall's section",
            "Each wall's section, 1.27 mm wide, with its core band dashed: pores are counted only there, clear of "
            "the contours. (The pores here are drawn, not data.)",
            3.0, to_screen("bse"), hold=3.2, cam_to=CAM["mon"])

    etch_pose = ST.face_up(ST.ETCH_SPOT)

    def etch(u):
        sc.alpha["screen_bse"] = 1.0 - window(u, 0.0, 0.1)
        sc.cam = ST.cam_via([CAM["mon"], CAM["sem"], CAM["etch"]], window(u, 0.0, 0.3))
        sc.gmat["puck"] = ST.blend(stage, etch_pose, window(u, 0.1, 0.35), PUCK_C, 100)
        for n in ("sem_chamber", "sem_door", "sem_door_handle"):
            sc.alpha[n] = 0.25 + 0.75 * window(u, 0.1, 0.3)
        x, y, z = ST.ETCH_SPOT
        top = z + M.PUCK_H
        d = window(u, 0.35, 0.5) * (1 - window(u, 0.85, 1.0))
        sc.alpha["dropper_tube"] = sc.alpha["dropper_bulb"] = d
        sc.gmat["dropper"] = T((x, y, top + 18 + 120 * (1 - d)))
        sc.alpha["drop"] = 1.0 if 0.5 < u < 0.62 else 0.0
        sc.gmat["drop"] = T((x, y, top + 16 - 14 * window(u, 0.5, 0.62)))
        sc.alpha["film"] = 0.9 * window(u, 0.6, 0.7) * (1 - window(u, 0.85, 0.97))
        sc.gmat["film"] = T((0, 0, -0.32))
        if u > 0.7:
            sc.color["pc_pA"] = mix(PART_C, (0.55, 0.53, 0.50), window(u, 0.7, 0.9))

    sc.step("C4 · etch",
            "Then etch to bring out the melt-pool boundaries, straight after the final polish (316 passivates "
            "fast): for example 10 % oxalic acid electrolytically, or a short dip in a mixed-acid etch in the fume hood.",
            5.0, etch, hold=0.5,
            warn="etch straight after the final polish, and lightly: over-etching pits the surface.",
            labels=[("section face: four walls", (ST.ETCH_SPOT[0], ST.ETCH_SPOT[1], ST.ETCH_SPOT[2] + M.PUCK_H),
                     (0.95, 0.30))])

    def back(u):
        sem(u, etch_pose)
        sc.alpha["film"] = 0.0

    sc.step("C5 · back in: the last layer's pools",
            "Back into the SEM (or under the optical microscope) to image the top of each wall, where the last "
            "layer's pools were never remelted.",
            4.0, back, hold=0.3, cam_to=CAM["sem"])

    sc.step("C6 · pool depth at the top",
            "The AM Module's steady-state pool is one of these arcs, if the hatch runs along the wall. If it runs "
            "across, the section shows only a flat fusion line, which gives the depth but not the width.",
            3.0, to_screen("etched"), hold=3.4, cam_to=CAM["mon"], still=True, warn_at="caption",
            warn="if the hatch runs across the wall, the section gives depth but no width.")
    return sc.save()


# =================================================================================================== 7 results
def chapter_results():
    sc = Scene("m2w_7_results", f"{TITLE}: 7/7 analyse and compare")
    w = World(sc, screens=True)
    mounted(w)
    sc.gmat["puck"] = ST.face_up(ST.STAGE)
    sc.show(["sem_chamber", "sem_door", "sem_door_handle"], 0.25)
    sc.alpha["screen_etched"] = 1.0
    sc.cam = CAM["mon"]

    def swap(new, old):
        def upd(u):
            sc.alpha[f"screen_{new}"] = window(u, 0.0, 0.5)
            sc.alpha[f"screen_{old}"] = 1.0 - window(u, 0.5, 0.6)
        return upd

    sc.step("C6 · segment and classify the pores",
            "Threshold every image the same way, keep the pores inside the core band, and sort them by shape: flat, "
            "irregular lack-of-fusion pores along the layers, round keyhole pores. Porosity is their area fraction.",
            1.5, swap("seg", "etched"), hold=4.2, warn_at="caption",
            warn="a dense wall's section holds only a few pores, so its porosity can differ by 50-100 % from one "
                 "section to the next. The pairs and the re-ground mounts measure that.")
    sc.step("C7 · on the map",
            "Each wall's porosity goes on the power–speed map, next to the AM Module's lack-of-fusion and keyhole "
            "boundaries, run in batch for all 33 settings and committed before the print. The 8 settings on both "
            "squares and the two controls show how far apart two walls at one setting come out.",
            1.5, swap("map", "seg"), hold=4.6, warn_at="caption",
            warn="a 1.27 mm wall heats up layer by layer. Run the AM Module with a substrate warmer than room "
                 "temperature as well, and compare both.")
    sc.step("C7 · per wall, and the next build",
            "Each wall gives the model a row: its four settings, porosity by class, last-layer pool depth, wall "
            "thickness, and the build record. Batch BO then puts the next build's settings where the model is "
            "least sure.",
            1.5, swap("record", "map"), hold=4.6, still=True)
    return sc.save()


# ========================================================================================================= join
CHAPTERS = [("m2w_1_setup", "Set up: panels, job file (42 walls, 33 sets), powder (B2, A1, B3)"),
            ("m2w_2_print", "Print: inert, bases then walls, one layer slowed down, what to watch (B4, B5)"),
            ("m2w_3_unload", "Unload: depowder, photograph, number the parts, bandsaw them off (B6, B7, C1)"),
            ("m2w_4_section", "Section: lengthwise off the centreline, then between walls 4 and 5 (C2)"),
            ("m2w_5_mount", "Mount and polish: 12 mounts, grind to the centreline, polish (C3, C4)"),
            ("m2w_6_sem", "SEM: porosity unetched, etch, last-layer melt pools (C5, C4, C6)"),
            ("m2w_7_results", "Analyse: pores, the map vs the AM Module, the next build (C6, C7)")]


def join():
    parts = [OUT / "mp4" / f"{n}.mp4" for n, _ in CHAPTERS]
    lst = OUT / "mp4" / "concat_w.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    meta = OUT / "mp4" / "chapters_w.ffmeta"
    lines, t, yt = [";FFMETADATA1", f"title={TITLE}"], 0, []
    for (n, title), part in zip(CHAPTERS, parts):
        frames = json.loads((OUT / f"{n}.json").read_text())["n_frames"]
        ms0, ms1 = round(t * 1000 / FPS), round((t + frames) * 1000 / FPS)
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={ms0}", f"END={ms1}", f"title={title}"]
        yt.append(f"{ms0 // 60000}:{ms0 // 1000 % 60:02d} {title}")
        t += frames
    meta.write_text("\n".join(lines) + "\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(meta),
                    "-map_metadata", "1", "-map_chapters", "1", "-c", "copy", "-movflags", "+faststart",
                    str(OUT / "mp4" / "m2w_full.mp4")], check=True)
    lst.unlink()
    meta.unlink()
    (OUT / "mp4" / "m2w_full_chapters.txt").write_text("\n".join(yt) + "\n")
    print("wrote out/mp4/m2w_full.mp4,", f"{t / FPS:.1f} s;", "chapters:", *yt, sep="\n  ")


if __name__ == "__main__":
    which = sys.argv[1:] or ["setup", "print", "unload", "section", "mount", "sem", "results"]
    for name in which:
        {"setup": chapter_setup, "print": chapter_print, "unload": chapter_unload, "section": chapter_section,
         "mount": chapter_mount, "sem": chapter_sem, "results": chapter_results, "full": join}[name]()
