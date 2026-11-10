"""The M2 single-track pilot (../m2-single-track-schedule.md) as six 3-D animations that follow the run sheet, in the
style of atomizer-training/viz3d and sieving/viz3d (CadQuery parts in PyVista, scene.py's captions and labels).

* ``m2_1_setup``: B2 panels into Nathan C.'s plate and flushness; A1 the job file (one vector per track); B3 powder
* ``m2_2_print``: B4 close up and inert; B5 recoat one layer and expose the 72 tracks
* ``m2_3_unload``: B6-B7 cool, depowder, photograph, unscrew and remove the panels; C1 top-view images
* ``m2_4_cut``: C2 bandsaw (a 10 mm strip holding the target plane out of the panel, then two pieces of nine tracks)
  and the fine wet saw (through piece 1, 0.5 mm from the plane)
* ``m2_5_sem``: C2 grind to the plane; C3 hot-mount; C4 grind, polish, etch; C5 SEM
* ``m2_6_results``: C5 the SEM images; C6 measure; C7 compare with the AM Module (on the monitor; illustrations)

The animations follow panel A (insert A in the plan), as the plan does ("section insert A first, all the way through
SEM"). Six short GIFs rather than one long one keep each under GitHub's ~5 MB; ``full`` joins the six MP4s into one
video with chapters.

    xvfb-run -a -s "-screen 0 1920x1080x24" python steps.py setup print unload cut sem results   # out/<name>.gif etc.
    PREVIEW=1 xvfb-run -a -s "-screen 0 1920x1080x24" python steps.py cut    # last frame of each sub-step -> /tmp
    python steps.py full                       # out/mp4/m2_full.mp4 (all six) and its chapter list
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pyvista as pv

import layout as L
import model as M
import scene as SC
import screens
from scene import R, S, Scene, T, mix, window

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
FPS = SC.FPS
TITLE = "M2 single-track pilot (#100)"

BLUE_RAMP = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281",
             "#0d366b"]                       # the static figure's P/v colours (sequential blue, light = low P/v)
CONTROL_C = (0.32, 0.32, 0.31)
HOT = (1.0, 0.86, 0.45)
TRACK_C = (1.0, 0.94, 0.78)                   # a fresh track: bright, lightly heat-tinted
POWDER_LAYER = (0.40, 0.41, 0.43)             # the spread layer, a little darker than the dose so tracks stand out
TRACK_W_SCALE = 2.5                           # tracks drawn 2.5x the illustrative width so they show
TRACK_AMB = 0.8
LASER_C = (1.0, 0.22, 0.10)
PLANE_C = (0.86, 0.16, 0.14)                  # the target plane: every track's mid-length
GAS_C = (0.35, 0.62, 0.92)
OPEN_DEG = -100.0


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def pv_color(E):
    if E is None:
        return CONTROL_C
    f = (math.log(E) - math.log(0.05)) / (math.log(1.5) - math.log(0.05))
    x = f * (len(BLUE_RAMP) - 1)
    i = min(int(x), len(BLUE_RAMP) - 2)
    return mix(hex_rgb(BLUE_RAMP[i]), hex_rgb(BLUE_RAMP[i + 1]), x - i)


# ------------------------------------------------------------------------------------------- pose helpers
def quat(Rm):
    m = Rm[:3, :3]
    tr = m.trace()
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2
        q = [0.25 * s, (m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s]
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        q = [(m[2, 1] - m[1, 2]) / s, 0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s]
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        q = [(m[0, 2] - m[2, 0]) / s, (m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s]
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        q = [(m[1, 0] - m[0, 1]) / s, (m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s]
    q = np.array(q)
    return q / np.linalg.norm(q)


def quat_mat(q):
    w, x, y, z = q
    m = np.eye(4)
    m[:3, :3] = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                 [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                 [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    return m


def slerp(q0, q1, u):
    d = float(np.dot(q0, q1))
    if d < 0:
        q1, d = -q1, -d
    if d > 0.9995:
        q = q0 + (q1 - q0) * u
        return q / np.linalg.norm(q)
    th = math.acos(d)
    return (math.sin((1 - u) * th) * q0 + math.sin(u * th) * q1) / math.sin(th)


def blend(M0, M1, u, c_local, lift=0.0):
    """Pose between M0 and M1 (local -> world): the local point c_local travels in a line (raised by `lift` at
    mid-way) and the orientation turns by slerp about it."""
    c = np.r_[c_local, 1.0]
    c0, c1 = (M0 @ c)[:3], (M1 @ c)[:3]
    p = c0 + (c1 - c0) * u + np.array([0, 0, lift * math.sin(math.pi * u)])
    return T(p) @ quat_mat(slerp(quat(M0), quat(M1), u)) @ T(-np.asarray(c_local, float))


def cam_via(cams, u):
    """Camera through a list of [position, focus, up] waypoints, equal time and smoothstep easing per leg."""
    n = len(cams) - 1
    k = min(int(u * n), n - 1)
    f = u * n - k
    f = f * f * (3 - 2 * f)
    a, b = cams[k], cams[k + 1]
    return [tuple(np.array(a[j], float) + (np.array(b[j], float) - np.array(a[j], float)) * f) for j in range(3)]


def via(Ms, u, c_local, lifts=None):
    """Through a list of poses, equal time per leg."""
    n = len(Ms) - 1
    k = min(int(u * n), n - 1)
    lifts = lifts or [0.0] * n
    return blend(Ms[k], Ms[k + 1], u * n - k, c_local, lifts[k])


# piece-local (block coordinates) -> puck-local: the section face x = TARGET_X goes to the puck face z = 0, piece 1's
# 22.5 mm side along the puck's x, the material up into the puck
PIECE_YC = sum(M.PIECE_Y) / 2
MP = np.array([[0, 1, 0, -PIECE_YC], [0, 0, -1, -M.PANEL_T / 2], [-1, 0, 0, M.TARGET_X - 0.2], [0, 0, 0, 1]], float)
# (the face stands 0.2 mm proud of the puck so the two coplanar faces don't z-fight)
CUBE_C = (L.CENTRE, L.CENTRE, -M.PANEL_T / 2)  # the panel's centre (block coordinates)
STRIP_C = (sum(M.STRIP_X) / 2, L.CENTRE, -M.PANEL_T / 2)
PIECE_C = (sum(M.STRIP_X) / 2, PIECE_YC, -M.PANEL_T / 2)
PUCK_C = (0.0, 0.0, M.PUCK_H / 2)
A_XY = M.INSERT_C["A"]
PANEL_HALF = L.PANEL / 2
XA = M.STRIP_X[1] + M.KERF / 2          # the first bandsaw cut's kerf centre, 3.5 mm past the target plane
XB = M.STRIP_X[0] - M.KERF / 2          # the second, 7.5 mm before it
FENCE_A = M.SAW_X - (XA - M.PANEL_LO)   # the fence's face against the panel's left edge, for each cut
FENCE_B = M.SAW_X - (XB - M.PANEL_LO)
CROSS_C = [(a + b) / 2 for a, b in M.CROSS_Y]


def at_plate(k, dz=0.0):
    cx, cy = M.INSERT_C[k]
    return T((cx - 12.5, cy - 12.5, dz))


def in_tray(i):
    sx, sy = M.tray_slots()[i]
    return T((sx - 12.5, sy - 12.5, M.BENCH_Z + 6 + M.PANEL_T))


def on_copy():
    cx, cy = M.COPY_C
    return T((cx - 12.5, cy - 12.5, M.BENCH_Z + 14 + M.PANEL_T))


def flat(anchor, y, rot=0.0):
    """Panel or block flat on the bandsaw table, tracks up; the block-coordinate point `anchor` (x, y) in the blade
    plane at world y = `y`, turned `rot` degrees about z."""
    return (T((M.SAW_X, y, M.SAW_TABLE_Z + M.PANEL_T)) @ R((0, 0, 1), rot)
            @ T((-anchor[0], -anchor[1], 0)))


def saw_flat(xcut, y):
    """Panel A flat on the bandsaw table, tracks up, its x = xcut in the blade plane and its centre at world y."""
    return flat((xcut, L.CENTRE), y)


def saw_cross(ycut, y):
    """The strip turned a quarter turn (its y along world x, the tracks pointing at the operator), y = ycut in the
    blade plane, its centre line at world y."""
    return flat((STRIP_C[0], ycut), y, -90.0)


def psaw(dz=0.0):
    """Piece 1 in the precision saw's chuck: the fine cut's kerf centre in the disc plane, lowered by dz."""
    return T((M.PSAW_X - M.FINAL_CUT_X - M.FINE_KERF / 2, -PIECE_YC, M.PSAW_SAMPLE_Z + M.PANEL_T - dz))


def face_down(p, h=0.0):
    return T((p[0], p[1], p[2] + h))


def face_up(p):
    return T((p[0], p[1], p[2] + M.PUCK_H)) @ R((1, 0, 0), 180)


POL_SPOT = (M.POL_C[0] + 70.0, M.POL_C[1], M.POL_Z)
ETCH_SPOT = (2905.0, -190.0, M.BENCH_Z)
PRESS_SEAT = (M.PRESS_C[0], M.PRESS_C[1], M.PRESS_TOP + 4.0)
ROW_SPOTS = [(2275.0 + 46.0 * i, -250.0, M.BENCH_Z) for i in range(8)]
STAGE = (M.SEM_C[0], M.SEM_C[1], M.SEM_STAGE_Z)

# --------------------------------------------------------------------------------------------- cameras
UP = (0, 0, 1)
CAM = {
    "m2_wide": [(-1300, -2950, 760), (180, 0, 60), UP],
    "plate": [(-170, -475, 270), (0, -15, -10), UP],
    "inserts": [(-150, -390, 250), (0, -12, 0), UP],
    "top": [(-30, -200, 310), (0, -6, 0), UP],
    "deck": [(-330, -940, 560), (-90, 0, -40), UP],
    "deck_in": [(-250, -285, 300), (-60, 30, -20), UP],
    "door": [(-520, -1650, 470), (-20, -200, 110), UP],
    "a_close": [(A_XY[0] - 10, A_XY[1] - 66, 34), (A_XY[0], A_XY[1] - 17, 0), UP],
    "inserts_high": [(-40, -186, 142), (0, -4, 0), UP],
    "bench": [(1500, -1450, 600), (1550, 0, -100), UP],
    "tray": [(1290, -560, 290), (1440, -40, -70), UP],
    "saw_panel": [(1585, -290, 160), (1702, -15, -15), UP],
    "saw_block": [(1615, -215, 105), (1704, -12, -14), UP],
    "saw": [(1625, -175, 70), (1702, -20, -12), UP],
    "saw_strip": [(1590, -265, 150), (1712, 0, -12), UP],
    "saw_x": [(1648, -165, 98), (1712, -2, -10), UP],
    "saws": [(1860, -470, 360), (1880, 0, -30), UP],
    "psaw": [(2186, -152, 186), (2050, 0, 16), UP],
    "pol": [(2655, -215, 130), (2785, -5, 12), UP],
    "press": [(2235, -310, 330), (2380, -40, 120), UP],
    "row": [(2380, -620, 220), (2440, -230, -80), UP],
    "etch": [(2850, -300, 25), (2905, -190, -78), UP],
    "sem": [(2860, -760, 520), (3120, 0, 110), UP],
    "mon": [(M.MON_C[0], -810, 182), (M.MON_C[0], 40, 182), UP],
}


# ------------------------------------------------------------------------------------------- the model
class World:
    """Every actor, and the state the update functions share."""

    def __init__(self, sc: Scene):
        self.sc = sc
        self.ms = M.meshes()
        self.tm = L.track_map()
        self.flash = 0.0
        self.spatter = np.zeros((0, 3))
        self.spatter_v = np.zeros((0, 3))
        self.chips = np.zeros((0, 3))
        self.chips_v = np.zeros((0, 3))
        self.rng = np.random.default_rng(1)
        self.t_done: dict[int, float] = {}
        self.frame = 0
        sc.inset = self.inset
        for name, e in self.ms["parts"].items():
            kw = {}
            if name in ("floor",):
                kw = dict(ambient=1.0, diffuse=0.0, specular=0.0, smooth_shading=False)
            sc.add(name, e["mesh"], e["color"], e["group"], opacity=e["opacity"], **kw)
        sc.color["pol_pad"] = (0.30, 0.30, 0.31)
        # panels B-D (whole) and panel A as its pieces
        for k in "BCD":
            sc.add(f"ins_{k}", self.ms["inserts"][k], M.INSERT_STEEL, f"g_{k}")
            sc.parent[f"g_{k}"] = "platform"
            sc.gmat[f"g_{k}"] = at_plate(k)
        for piece, mesh in self.ms["pieces"].items():
            sc.add(f"A_{piece}", mesh, M.INSERT_STEEL, "g_A", shown=(piece == "panel"))
        sc.parent["g_A"] = "platform"
        sc.gmat["g_A"] = at_plate("A")
        # each panel's four cap screws (group s_<k>, riding on the platform)
        for k in "ABCD":
            for j, (x, y) in enumerate(M.screw_xy()):
                sc.add(f"scr_{k}_{j}", self.ms["screw"].translate((x, y, 0), inplace=False), M.DARK, f"s_{k}",
                       shown=False)
            sc.parent[f"s_{k}"] = "platform"
            sc.gmat[f"s_{k}"] = at_plate(k)
        # the target plane on panel A (every track's mid-length), across the strip and on piece 1 only
        for n, (y0, y1) in (("target_plane", (M.CROSS_Y[0][1], M.CROSS_Y[2][0])), ("target_plane_p1", M.PIECE_Y)):
            sc.add(n, pv.Box((M.TARGET_X - 0.08, M.TARGET_X + 0.08, y0, y1, -M.PANEL_T - 0.4, 1.2)), PLANE_C, "g_A",
                   opacity=0.5, ambient=0.6, specular=0.0, shown=False)
        sc.gmat["fence"] = T((FENCE_A, 0, 0))
        # powder: the spread layer over the build area, and the heap in front of the blade
        sc.add("powder_layer", pv.Box((-130, 130, -128, 128, -1.0, 0.03)), POWDER_LAYER, "powder_layer",
               specular=0.0, ambient=0.3, smooth_shading=False, shown=False)
        sc.add("powder_heap", pv.Box((4, 11, -140, 140, 0, 4.5)), M.POWDER, "recoater", specular=0.0,
               smooth_shading=False, shown=False)
        # tracks and their job-file vectors
        for i, t in enumerate(self.tm):
            k = t["insert"]
            g = f"g_{k}"
            sc.add(f"trk_{i}", self.track_mesh(t), TRACK_C, g, shown=False, specular=0.6, specular_power=30)
            (x0, y), (x1, _) = t["start"], t["end"]
            vec = pv.Line((x0, y, 3.0), (x1, y, 3.0)).tube(radius=0.28, n_sides=10)
            sc.add(f"vec_{i}", vec, pv_color(t["E"]), g, shown=False, ambient=0.6, specular=0.0)
        # panel A's tracks after the bandsaw (cut 3 mm past the target plane); piece 1's after the fine saw (0.5 mm
        # past it), on the sliver, and at the target plane after grinding
        for i, t in enumerate(self.tm):
            if t["insert"] != "A":
                continue
            sc.add(f"trkstrip_{i}", self.track_mesh(t, x1=M.STRIP_X[1]), TRACK_C, "g_A", shown=False, specular=0.6)
            sc.add(f"trkhi_{i}", self.track_mesh(t, x0=M.STRIP_X[1] + M.KERF), TRACK_C, "g_A", shown=False,
                   specular=0.6)                                    # the tracks' ends, on the first offcut
            if t["group"] == 1:
                sc.add(f"trkcut_{i}", self.track_mesh(t, x1=M.FINAL_CUT_X), TRACK_C, "g_A", shown=False,
                       specular=0.6)
                sc.add(f"trksec_{i}", self.track_mesh(t, x1=M.TARGET_X), TRACK_C, "g_A", shown=False, specular=0.6)
                sc.add(f"trkoff_{i}", self.track_mesh(t, x0=M.FINAL_CUT_X + M.FINE_KERF, x1=M.STRIP_X[1]), TRACK_C,
                       "g_A", shown=False, specular=0.6)
        # laser, melt glow, spatter, chips
        sc.add("beam", pv.Line((0, 0, 520), (0, 0, 0)).tube(radius=0.6), LASER_C, "fx", opacity=0.8, ambient=1.0,
               diffuse=0.0, specular=0.0, shown=False)
        sc.add("glow", pv.Sphere(radius=0.45, center=(0, 0, 0)), (1.0, 0.97, 0.8), "fx", ambient=1.0, diffuse=0.0,
               specular=0.0, shown=False)
        sc.add("halo", pv.Sphere(radius=1.4, center=(0, 0, 0)), (1.0, 0.55, 0.15), "fx", opacity=0.35, ambient=1.0,
               diffuse=0.0, specular=0.0, shown=False)
        sc.add("spatter", pv.PolyData(np.zeros((1, 3))), (1.0, 0.62, 0.2), "fx", style="points", point_size=5,
               render_points_as_spheres=True, ambient=1.0, diffuse=0.0, shown=False)
        sc.add("chips", pv.PolyData(np.zeros((1, 3))), (0.75, 0.77, 0.80), "fx", style="points", point_size=4,
               render_points_as_spheres=True, shown=False)
        # gas-flow arrows
        self.gas = []
        for j, x in enumerate((-85.0, 0.0, 85.0)):
            for m in range(3):
                n = f"gas_{j}_{m}"
                arrow = pv.Arrow(start=(0, 0, 0), direction=(0, -1, 0), scale=46, tip_length=0.32, tip_radius=0.16,
                                 shaft_radius=0.06)
                sc.add(n, arrow, GAS_C, n, opacity=0.55, ambient=0.5, specular=0.0, shown=False)
                self.gas.append((n, x, m / 3.0))
        # dial indicator (tip at the group origin)
        ind = {
            "ind_base": (pv.Box((-15, 15, -80, -50, 0, 28)), (0.12, 0.12, 0.13)),
            "ind_column": (pv.Cylinder(center=(0, -65, 40), direction=(0, 0, 1), radius=5, height=24), M.STEEL),
            "ind_arm": (pv.Box((-3.5, 3.5, -68, -4, 44, 50)), M.STEEL),
            "ind_dial": (pv.Cylinder(center=(0, 0, 34), direction=(0, 1, 0), radius=18, height=10), (0.2, 0.2, 0.22)),
            "ind_face": (pv.Cylinder(center=(0, -5.2, 34), direction=(0, 1, 0), radius=16.5, height=0.6),
                         (0.97, 0.97, 0.95)),
            "ind_stylus": (pv.Cylinder(center=(0, 0, 8.5), direction=(0, 0, 1), radius=0.8, height=15), M.STEEL),
            "ind_tip": (pv.Sphere(radius=1.4, center=(0, 0, 1.4)), (0.9, 0.2, 0.15)),
        }
        for n, (mesh, c) in ind.items():
            sc.add(n, mesh, c, "indicator", shown=False)
        sc.add("ind_needle", pv.Box((-0.6, 0.6, -5.8, -5.5, 34, 48)), (0.85, 0.12, 0.10), "needle", shown=False)
        sc.parent["needle"] = "indicator"
        # puck (the piece is re-parented to it), the other seven pucks, compound granules, etch drop and film
        sc.add("puck", pv.Cylinder(center=(0, 0, M.PUCK_H / 2), direction=(0, 0, 1), radius=M.PUCK_R - 0.05,
                                   height=M.PUCK_H, resolution=60), M.BAKELITE, "puck", shown=False, specular=0.25)
        for i in range(1, 8):
            x, y, z = ROW_SPOTS[i]
            sc.add(f"puck_{i}", pv.Cylinder(center=(x, y, z + M.PUCK_H / 2), direction=(0, 0, 1),
                                            radius=M.PUCK_R, height=M.PUCK_H, resolution=60), M.BAKELITE,
                   "static", shown=False, specular=0.25)
            hw, ht = (M.PIECE_Y[1] - M.PIECE_Y[0]) / 2, M.PANEL_T / 2
            sc.add(f"puckface_{i}", pv.Box((x - hw, x + hw, y - ht, y + ht, z + M.PUCK_H, z + M.PUCK_H + 0.05)),
                   M.INSERT_STEEL, "static", shown=False)
        sc.add("granules", pv.PolyData(np.zeros((1, 3))), (0.10, 0.10, 0.11), "fx", style="points", point_size=4,
               render_points_as_spheres=True, shown=False)
        sc.add("drop", pv.Sphere(radius=2.2, center=(0, 0, 0)), (0.95, 0.75, 0.25), "drop", ambient=0.5,
               shown=False)
        sc.add("film", pv.Cylinder(center=(0, 0, 0.15), direction=(0, 0, 1), radius=13, height=0.3),
               (0.95, 0.78, 0.30), "film", opacity=0.5, shown=False)
        sc.parent["film"] = "puck"
        sc.add("sem_beam", pv.Line((0, 0, 110), (0, 0, 33)).tube(radius=0.7), (0.55, 0.78, 1.0), "fx",
               opacity=0.85, ambient=1.0, diffuse=0.0, specular=0.0, shown=False)
        # the monitor's three screens
        files = screens.make_all(M.CACHE)
        mx, my = M.MON_C
        x0, x1, z0, z1, y = mx - M.MON_W / 2, mx + M.MON_W / 2, M.MON_Z0, M.MON_Z0 + M.MON_H, my - 0.8
        for key, path in files.items():
            quad = pv.PolyData(np.array([[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1]], float),
                               np.array([4, 0, 1, 2, 3]))
            quad.active_texture_coordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
            from PIL import Image
            tex = pv.numpy_to_texture(np.asarray(Image.open(path).convert("RGB")))
            actor = sc.pl.add_mesh(quad, texture=tex, ambient=1.0, diffuse=0.0, specular=0.0)
            n = f"screen_{key}"
            sc.actors[n] = actor
            sc.group_of[n] = "static"
            sc.base_alpha[n] = 1.0
            sc.alpha[n] = 0.0
        # initial state: door open, dose empty, recoater parked
        sc.gmat["door"] = R((0, 0, 1), OPEN_DEG, pivot=M.DOOR_HINGE)
        sc.gmat["recoater"] = T((M.RECOATER_PARK, 0, 0))
        sc.gmat["dose_powder"] = S((1, 1, 0.02), pivot=(0, 0, -300))
        sc.gmat["powder_layer"] = S((0.001, 1, 1), pivot=(-130, 0, 0))
        sc.gmat["indicator"] = T((-65, -45, 0))
        sc.show(["dropper_tube", "dropper_bulb"], 0.0)

    # ---------------------------------------------------------------------------------------- tracks
    def track_dims(self, t):
        E = t["E"] if t["E"] is not None else 0.25
        w = 0.30 * math.sqrt(E) * TRACK_W_SCALE
        return w, 0.28 * w, L.regime(t["E"])

    def track_mesh(self, t, x0=None, x1=None):
        (a, y), (b, _) = t["start"], t["end"]
        x0 = a if x0 is None else max(a, x0)
        x1 = b if x1 is None else min(b, x1)
        w, h, reg = self.track_dims(t)
        if x1 - x0 < 0.05:
            x1 = x0 + 0.05
        if reg.startswith("balling"):
            rng = np.random.default_rng(int(t["order"]))
            beads, x = [], a + rng.uniform(0.0, 0.3)
            while x < b:
                r = w * rng.uniform(0.55, 0.85)
                if x0 <= x <= x1:
                    beads.append(pv.Sphere(radius=r, center=(x, y, 0.15 * r), theta_resolution=10, phi_resolution=8))
                x += rng.uniform(0.45, 0.9)
            if not beads:
                beads = [pv.Sphere(radius=0.02, center=(x0, y, -1.0))]
            return pv.merge(beads)
        m = pv.Line((x0, y, 0.0), (x1, y, 0.0)).tube(radius=w / 2, n_sides=14, capping=True)
        m.points[:, 2] *= h / (w / 2)
        return m.compute_normals(auto_orient_normals=True)

    def spot_world(self, t, x):
        return (self.sc.world(f"g_{t['insert']}") @ np.r_[x, t["start"][1], 0.05, 1.0])[:3]

    # ------------------------------------------------------------------------------------- effects
    def inset(self, base):
        if self.flash > 0.01:
            a = min(1.0, self.flash)
            base = (base.astype(np.float32) * (1 - 0.85 * a) + 255 * 0.85 * a).astype(np.uint8)
        return base

    def laser(self, on, spot=None, radius=0.6):
        sc = self.sc
        for n in ("beam", "glow", "halo"):
            sc.alpha[n] = 1.0 if on else 0.0
        if on:
            sc.set_mesh("beam", pv.Line(tuple(M.SCANNER), tuple(spot)).tube(radius=radius, n_sides=10))
            sc.set_mesh("glow", pv.Sphere(radius=0.45, center=spot, theta_resolution=12, phi_resolution=12))
            sc.set_mesh("halo", pv.Sphere(radius=1.4, center=spot, theta_resolution=12, phi_resolution=12))

    def particles(self, spawn_at=None, n=5, dt=1.0 / FPS, kind="spatter"):
        pos, vel = (self.spatter, self.spatter_v) if kind == "spatter" else (self.chips, self.chips_v)
        if spawn_at is not None:
            r = self.rng
            if kind == "spatter":
                v = np.c_[r.normal(0, 6, n), r.normal(-14, 6, n), r.uniform(10, 26, n)]
            else:
                v = np.c_[r.normal(0, 25, n), r.uniform(-90, -40, n), r.uniform(10, 60, n)]
            pos = np.vstack([pos, np.tile(spawn_at, (n, 1)) + r.normal(0, 0.2, (n, 3))])
            vel = np.vstack([vel, v])
        g = np.array([0, -10.0 if kind == "spatter" else 0.0, -40.0 if kind == "spatter" else -260.0])
        vel = vel + g * dt
        pos = pos + vel * dt
        floor = 0.0 if kind == "spatter" else M.BENCH_Z
        keep = pos[:, 2] > floor
        pos, vel = pos[keep][-400:], vel[keep][-400:]
        name = "spatter" if kind == "spatter" else "chips"
        self.sc.alpha[name] = 1.0 if len(pos) else 0.0
        if len(pos):
            self.sc.set_mesh(name, pv.PolyData(pos.copy()))
        if kind == "spatter":
            self.spatter, self.spatter_v = pos, vel
        else:
            self.chips, self.chips_v = pos, vel

    def gas_flow(self, on_alpha):
        self.frame += 1
        for n, x, ph in self.gas:
            f = (ph + self.frame / (FPS * 2.4)) % 1.0
            y = 150 - 300 * f
            self.sc.gmat[n] = T((x, y, 28))
            self.sc.alpha[n] = on_alpha * min(1.0, 4 * f, 4 * (1 - f))

    def track_color(self, i, now):
        if i not in self.t_done:
            return
        f = min(1.0, max(0.0, (now - self.t_done[i]) / 0.7))
        self.sc.color[f"trk_{i}"] = mix(HOT, TRACK_C, f)
        self.sc.ambient[f"trk_{i}"] = 1.0 + (TRACK_AMB - 1.0) * f

    def show_track_done(self, i):
        self.sc.alpha[f"trk_{i}"] = 1.0
        self.sc.set_mesh(f"trk_{i}", self.track_mesh(self.tm[i]))
        self.sc.color[f"trk_{i}"] = TRACK_C
        self.sc.ambient[f"trk_{i}"] = TRACK_AMB

    def a_pieces(self, *show):
        for p in self.ms["pieces"]:
            self.sc.alpha[f"A_{p}"] = 1.0 if p in show else 0.0


def a_tracks(w: World, groups=(1, 2), kind="trk"):
    """Panel A's track actors of one kind; group 1 is the nine tracks that end up in piece 1."""
    return [f"{kind}_{i}" for i, t in enumerate(w.tm) if t["insert"] == "A" and t["group"] in groups]


def screws(w: World, a: float):
    for k in "ABCD":
        w.sc.show([f"scr_{k}_{j}" for j in range(4)], a)


def a_world(t, x, z=0.0):
    """World position of a point on panel A's track t, at block-coordinate x, while A sits in the plate."""
    return tuple((at_plate("A") @ np.r_[x, t["start"][1], z, 1.0])[:3])


# ================================================================================================ set up
def chapter_setup():
    """B2, A1, B3: panels into the plate, flushness, the job file's vectors, powder into the dose chamber."""
    sc = Scene("m2_1_setup", f"{TITLE}: 1/6 set up")
    w = World(sc)
    sc.cam = CAM["m2_wide"]
    for k in "ABCD":
        sc.gmat[f"g_{k}"] = at_plate(k, 140)
        sc.show([f"ins_{k}"] if k != "A" else ["A_panel"], 0.0)

    def drop_in(u):
        for j, k in enumerate("ABCD"):
            v = window(u, 0.08 + 0.15 * j, 0.33 + 0.15 * j)
            sc.gmat[f"g_{k}"] = at_plate(k, 140 * (1 - v))
            sc.alpha[f"ins_{k}" if k != "A" else "A_panel"] = min(1.0, v * 4)
            s_in = window(u, 0.74 + 0.05 * j, 0.86 + 0.05 * j)       # then four screws each
            sc.gmat[f"s_{k}"] = at_plate(k, 25 * (1 - s_in))
            sc.show([f"scr_{k}_{jj}" for jj in range(4)], s_in)

    sc.step("B2 · panels into the plate",
            "Nathan C.'s plate: about 10 in square, with four removable panels. Four fresh 316L panels (about 88 mm "
            "square, ID-marked on the side) go into its pockets and are screwed down. The plate itself is never "
            "lasered, so it needs no resurfacing between runs, and nothing is welded on, so no wire EDM.",
            6.0, drop_in, hold=1.2, cam_to=CAM["plate"],
            labels=[("panel A (ID and notch on its side)", (A_XY[0] - 20, A_XY[1] - 20, 0), (0.06, 0.30)),
                    ("plate, about 10 in square:\nnever lasered", (110, -60, 0), (0.95, 0.68))])

    stops = []
    for k in "ABCD":
        cx, cy = M.INSERT_C[k]
        stops += [(cx - 48, cy, 3.0), (cx - 48, cy, 0.0), (cx - 36, cy, 0.0), (cx - 36, cy, 3.0)]
    readings = []

    def indicate(u):
        sc.show([n for n in sc.actors if n.startswith("ind_")], min(1.0, u * 8))
        v = window(u, 0.08, 1.0)
        x = v * (len(stops) - 1)
        i = min(int(x), len(stops) - 2)
        p = np.array(stops[i]) + (np.array(stops[i + 1]) - np.array(stops[i])) * (x - i)
        sc.gmat["indicator"] = T(p)
        on_insert = (i % 4) == 1 and x - i > 0.5
        sc.gmat["needle"] = R((0, 1, 0), 14 * math.sin(6 * x) if on_insert else 0, pivot=(0, -5.6, 34))
        done = int(x // 4)
        sc.gauges = [("flush", "dial-indicate vs. plate")] + [(f"panel {k}", "offset logged")
                                                             for k in "ABCD"[:min(4, done + (1 if x % 4 > 2 else 0))]]

    sc.step("B2 · flushness",
            "Dial-indicate each panel against the plate across the pocket gap and record the offset: it becomes that "
            "panel's layer-thickness input to the model. Flushness is the critical tolerance (about 10 µm, 10–20 % "
            "of a layer).",
            6.5, indicate, hold=1.0, cam_to=CAM["inserts"],
            labels=[("dial indicator on a magnetic base", (M.INSERT_C["D"][0] - 36, M.INSERT_C["D"][1], 37),
                     (0.06, 0.30))])

    vecs = [f"vec_{i}" for i in range(len(w.tm))]

    def job(u):
        sc.show([n for n in sc.actors if n.startswith("ind_")], max(0.0, 1 - u * 5))
        sc.gauges = []
        for i in range(len(w.tm)):
            sc.alpha[vecs[i]] = window(u, 0.15 + 0.6 * i / len(w.tm), 0.25 + 0.6 * i / len(w.tm))

    ctl = next(t for t in w.tm if t["insert"] == "D" and t["E"] is None)
    first = next(t for t in w.tm if t["insert"] == "A" and t["k"] == 0)
    first_xyz = a_world(first, first["start"][0] + 1.5, 3.0)
    ctl_xyz = (M.INSERT_C["D"][0] - 12.5 + (ctl["start"][0] + ctl["end"][0]) / 2,
               M.INSERT_C["D"][1] - 12.5 + ctl["start"][1], 3)
    sc.step("A1 · job file",
            "Job file: each track is its own part carrying its own power–speed setting (on each panel, one 16-point "
            "block of the Sobol design plus 2 controls), in a random order in one row across the panel. The dry run "
            "must show one scan vector per track. The AM Module predictions for all 65 settings are committed before "
            "printing (A2).",
            5.0, job, hold=2.0, cam_to=CAM["top"], still=True,
            labels=[("darker = higher P/v (J/mm)", first_xyz, (0.06, 0.30)),
                    ("grey = control (machine's standard set)", ctl_xyz, (0.95, 0.20))])

    def powder(u):
        for n in vecs:
            sc.alpha[n] = max(0.0, 1 - u * 4)
        sc.gmat["dose_powder"] = S((1, 1, 0.02 + 0.98 * window(u, 0.25, 1.0)), pivot=(0, 0, -300))

    sc.step("B3 · powder",
            "Load and sieve 316L powder into the dose chamber; record the lot, its certificate and the particle size "
            "distribution.",
            4.0, powder, hold=0.8, cam_to=CAM["deck"],
            labels=[("dose chamber", (-305, -60, 0), (0.06, 0.30)), ("build plate", (60, -100, 0), (0.95, 0.60)),
                    ("overflow", (225, 60, 0), (0.95, 0.30))])
    return sc.save()


def chapter_print():
    """B4-B5: close up and inert, recoat one layer, expose the 72 tracks. Starts where m2_1_setup ends."""
    sc = Scene("m2_2_print", f"{TITLE}: 2/6 print")
    w = World(sc)
    screws(w, 1.0)
    sc.gmat["dose_powder"] = S((1, 1, 1.0), pivot=(0, 0, -300))
    sc.cam = CAM["deck"]

    def inert(u):
        sc.gmat["door"] = R((0, 0, 1), OPEN_DEG * (1 - window(u, 0.0, 0.45)), pivot=M.DOOR_HINGE)
        v = window(u, 0.45, 1.0)
        o2 = 20.9 * math.exp(-6.5 * v)
        sc.gauges = [("O₂", f"{o2:5.1f} %" if v < 0.98 else "at setpoint"), ("gas", "N₂ or Ar (kickoff)")]
        w.gas_flow(window(u, 0.5, 0.8))

    sc.step("B4 · close up and inert",
            "Close the door and purge to the O₂ setpoint. The gas flows across the plate from the inlet to the "
            "outlet; the direction drawn here is assumed, so note the real one.",
            4.5, inert, hold=1.0, cam_to=CAM["door"], live=True,
            labels=[("gas inlet (assumed back)", (0, 290, 40), (0.95, 0.22)),
                    ("outlet", (150, -290, 30), (0.95, 0.62))])

    def recoat(u):
        w.gas_flow(1.0)
        v = window(u, 0.0, 0.7)
        x = M.RECOATER_PARK + (M.RECOATER_END - M.RECOATER_PARK) * v
        if u > 0.75:
            x = M.RECOATER_END + (M.RECOATER_PARK - M.RECOATER_END) * window(u, 0.75, 1.0)
        sc.gmat["recoater"] = T((x, 0, 0))
        sc.alpha["powder_heap"] = 1.0 if (-430 < x < 265 and u < 0.75) else 0.0
        f = min(1.0, max(0.0, (x + 130) / 260)) if u <= 0.75 else 1.0
        sc.alpha["powder_layer"] = 1.0 if f > 0.002 else 0.0
        sc.gmat["powder_layer"] = S((max(f, 0.001), 1, 1), pivot=(-130, 0, 0))

    sc.step("B5 · recoat one layer",
            "One layer: the build platform drops one layer thickness and the recoater spreads powder over the plate "
            "and the panels; the excess falls into the overflow.",
            4.5, recoat, hold=0.6, cam_to=CAM["deck_in"], live=True)

    order = sorted(range(len(w.tm)), key=lambda i: w.tm[i]["order"])
    slow = order[:4]
    rest = order[4:]
    clock = {"t": 0.0}

    def draw(seq, u, frac_per_track, radius):
        """Laser along seq[] at constant speed; u in [0, 1] over the whole sequence."""
        clock["t"] += 1.0 / FPS
        n = len(seq)
        x = min(u * n, n - 1e-6)
        j = int(x)
        f = x - j
        for jj in range(j):
            i = seq[jj]
            if i not in w.t_done:
                w.show_track_done(i)
                w.t_done[i] = clock["t"]
                sc.color[f"trk_{i}"] = HOT
                sc.ambient[f"trk_{i}"] = 1.0
        for i in seq[:j]:
            w.track_color(i, clock["t"])
        i = seq[j]
        t = w.tm[i]
        g = min(1.0, f / frac_per_track)
        if g < 1.0:
            xs = t["start"][0] + (t["end"][0] - t["start"][0]) * g
            sc.alpha[f"trk_{i}"] = 1.0
            sc.set_mesh(f"trk_{i}", w.track_mesh(t, x1=xs))
            sc.color[f"trk_{i}"] = HOT
            sc.ambient[f"trk_{i}"] = 1.0
            spot = w.spot_world(t, xs)
            w.laser(True, spot, radius)
            w.particles(spot, n=4)
        else:
            w.laser(False)
            w.particles(None)

    def expose_slow(u):
        w.gas_flow(0.0)
        if sc.u >= 1.0:
            clock["t"] += 1.0 / FPS
            for i in slow:
                if i not in w.t_done:
                    w.show_track_done(i)
                    w.t_done[i] = clock["t"]
                w.track_color(i, clock["t"])
            w.laser(False)
            w.particles(None)
            return
        draw(slow, sc.u, 0.8, 0.5)

    sc.step("B5 · expose (slowed down)",
            "The laser draws each track once, every track in the same direction, starting on the gas-outlet side "
            "so spatter lands on finished tracks rather than on fresh powder.",
            6.5, expose_slow, hold=0.6, cam_to=CAM["a_close"], live=True,
            labels=[("powder layer over panel A", (A_XY[0] + 10, A_XY[1] + 13, 0.03), (0.95, 0.25)),
                    ("scan direction →", a_world(w.tm[order[0]], w.tm[order[0]]["start"][0]), (0.06, 0.62))])

    def expose_rest(u):
        w.gas_flow(0.0)
        if sc.u >= 1.0:
            for i in rest:
                if i not in w.t_done:
                    w.show_track_done(i)
                    w.t_done[i] = clock["t"]
            clock["t"] += 1.0 / FPS
            for i in rest:
                w.track_color(i, clock["t"])
            w.laser(False)
            w.particles(None)
            return
        draw(rest, window(sc.u, 0.0, 0.92), 0.7, 1.0)

    sc.step("B5 · 72 tracks",
            "72 tracks in one row across each panel: one 16-point block of a Sobol sequence that covers the whole "
            "power–speed window, plus 2 controls, in random positions; the controls measure position effects. The "
            "exposure takes seconds; the whole step is under 15 minutes.",
            7.5, expose_rest, hold=1.8, cam_to=CAM["inserts_high"], live=True, still=True,
            labels=[(k, (M.INSERT_C[k][0], M.INSERT_C[k][1] + (-12.5 if k in "AB" else 12.5), 0),
                     (0.06 if k in "AC" else 0.95, 0.62 if k in "AB" else 0.22)) for k in "ABCD"])
    return sc.save()


# ------------------------------------------------------------------------------- shared state after printing
def printed(w: World):
    sc = w.sc
    screws(w, 1.0)
    sc.gmat["door"] = np.eye(4)
    sc.gmat["dose_powder"] = S((1, 1, 0.98), pivot=(0, 0, -300))
    sc.alpha["powder_layer"] = 1.0
    sc.gmat["powder_layer"] = np.eye(4)
    for i in range(len(w.tm)):
        w.show_track_done(i)


# ============================================================================================== unload
def chapter_unload():
    """B6-B7, C1: cool, de-inert, depowder, photograph, lift the panels out; top-view images. Starts where m2_2_print
    ends."""
    sc = Scene("m2_3_unload", f"{TITLE}: 3/6 unload")
    w = World(sc)
    printed(w)
    sc.cam = CAM["inserts_high"]
    for n, x, ph in w.gas:
        sc.alpha[n] = 0.0

    def unload(u):
        v = window(u, 0.0, 0.25)
        sc.gauges = [("O₂", "rising: de-inert" if v < 1 else "air"), ("plate", "cool")]
        sc.gmat["door"] = R((0, 0, 1), OPEN_DEG * window(u, 0.2, 0.45), pivot=M.DOOR_HINGE)
        sc.alpha["powder_layer"] = 1.0 - window(u, 0.45, 0.62)
        w.flash = max(0.0, 1 - abs(u - 0.66) * 25)
        out = window(u, 0.69, 0.8)                                     # four screws out of each panel
        for k in "ABCD":
            sc.gmat[f"s_{k}"] = at_plate(k, 30 * out)
        screws(w, 1.0 - out)
        lift = window(u, 0.8, 1.0)
        for k in "ABCD":
            sc.gmat[f"g_{k}"] = at_plate(k, 45 * lift)

    sc.step("B6–B7 · cool, depowder, unscrew",
            "Cool and de-inert, depowder gently, photograph the plate in place, then take out each panel's four "
            "screws and lift the panels out. The plate only needs the powder blown out of the pocket gaps and screw "
            "holes before the next run.",
            6.0, unload, hold=0.8, cam_to=CAM["plate"],
            labels=[("pocket gaps: blow the powder out", (A_XY[0] - 45, A_XY[1] + 10, 0), (0.06, 0.30))])

    # panels leave the chamber through the door and go to the bench: A under the copy stand, B-D to the tray
    starts = {k: sc.world(f"g_{k}") for k in "ABCD"}
    for k in "ABCD":
        del sc.parent[f"g_{k}"]
        sc.gmat[f"g_{k}"] = starts[k]
    ends = {"A": on_copy(), "B": in_tray(1), "C": in_tray(2), "D": in_tray(3)}

    def to_bench(u):
        sc.gauges = []
        for j, k in enumerate("ABCD"):
            s0 = starts[k]
            out = T((0, -700, 180)) @ s0
            over = T((ends[k][0, 3] - s0[0, 3], 0, 0)) @ out
            above = T((0, 0, 140)) @ ends[k]
            v = window(u, 0.04 * j, 0.80 + 0.04 * j)
            sc.gmat[f"g_{k}"] = via([s0, out, over, above, ends[k]], v, CUBE_C)
        w.flash = max(0.0, 1 - abs(u - 0.97) * 30)

    sc.step("C1 · top-view images",
            "Each panel gets top-view images (are the tracks continuous, which ones balled up?). Panel A goes "
            "first, all the way through SEM, to catch problems early: track mapping, etch, SEM charging.",
            6.5, to_bench, hold=1.2, cam_to=CAM["tray"], still=True,
            labels=[("copy stand + camera", (M.COPY_C[0], M.COPY_C[1], M.BENCH_Z + 300), (0.95, 0.22)),
                    ("B, C, D wait in the tray", (M.tray_slots()[1][0], M.tray_slots()[1][1] - 30,
                                                  M.BENCH_Z + 6 + M.PANEL_T), (0.06, 0.68))])
    return sc.save()


def lin(u, t0, t1):
    return min(1.0, max(0.0, (u - t0) / max(t1 - t0, 1e-6)))


# ================================================================================================= cut
def chapter_cut():
    """C2: the bandsaw takes a 10 mm strip holding the target plane out of panel A and cuts it into two pieces of nine
    tracks; the fine wet saw cuts through piece 1, 0.5 mm from the plane. Starts where m2_3_unload ends."""
    sc = Scene("m2_4_cut", f"{TITLE}: 4/6 cut")
    w = World(sc)
    printed(w)
    screws(w, 0.0)
    sc.gmat["door"] = R((0, 0, 1), OPEN_DEG, pivot=M.DOOR_HINGE)
    sc.alpha["powder_layer"] = 0.0
    for n, x, ph in w.gas:
        sc.alpha[n] = 0.0
    for k in "ABCD":
        del sc.parent[f"g_{k}"]
    sc.gmat["g_A"] = on_copy()
    for i, k in enumerate("BCD"):
        sc.gmat[f"g_{k}"] = in_tray(i + 1)
    sc.cam = CAM["tray"]

    a_start = on_copy()
    F0, F1 = -78.0, 74.0              # panel centre (world y) before and after a pass through the blade
    table_top = M.SAW_TABLE_Z + M.PANEL_T

    def chips(on, z=M.SAW_TABLE_Z + 0.6 * M.PANEL_T):
        w.particles(np.array([M.SAW_X, -7.0, z]) if on else None, n=6, kind="chips")

    def cut_a(u):
        sc.alpha["target_plane"] = window(u, 0.05, 0.25)
        if u < 0.3:
            sc.gmat["g_A"] = via([a_start, T((0, 0, 120)) @ saw_flat(XA, F0), saw_flat(XA, F0)], window(u, 0.0, 0.3),
                                 CUBE_C, [60, 0])
            return
        y = F0 + (F1 - F0) * window(u, 0.32, 0.85)
        sc.gmat["g_A"] = saw_flat(XA, y)
        chips(0.32 < u < 0.85 and abs(y) < PANEL_HALF + 7)
        if u >= 0.85:
            w.a_pieces("strip_side", "scrap_hi")
            for n in a_tracks(w):
                sc.alpha[n] = 0.0
            for n in a_tracks(w, kind="trkstrip"):
                sc.alpha[n] = 1.0
            sc.group_of["A_scrap_hi"] = "a_hi"
            for n in a_tracks(w, kind="trkhi"):
                sc.group_of[n] = "a_hi"
                sc.alpha[n] = 1.0
            sc.gmat["a_hi"] = T((12 * window(u, 0.86, 1.0), 0, 0)) @ saw_flat(XA, F1)

    sc.step("C2 · bandsaw: across the panel",
            "Bandsaw (bi-metal blade, coolant for stainless). The panel lies flat against the fence, tracks up. The "
            "first cut goes across it 3 mm past the target plane (red), the line where every track is at mid-length. "
            "A bandsaw face is rough, so no bandsaw cut comes closer.",
            6.5, cut_a, hold=0.6, cam_to=CAM["saw_strip"],
            labels=[("target plane: every track's mid-length", (M.SAW_X - XA + M.TARGET_X, F1 + 12, table_top + 1.2),
                     (0.06, 0.24)),
                    ("fence", (FENCE_A - 6, F1 - 30, M.SAW_TABLE_Z + 16), (0.06, 0.62)),
                    ("blade", (M.SAW_X, -2, 50), (0.95, 0.22))])

    def cut_b(u):
        sc.alpha["A_scrap_hi"] = 1.0 - window(u, 0.05, 0.3)
        for n in a_tracks(w, kind="trkhi"):
            sc.alpha[n] = 1.0 - window(u, 0.05, 0.3)
        sc.gmat["a_hi"] = T((12 + 60 * window(u, 0.0, 0.3), 0, 0)) @ saw_flat(XA, F1)
        if u < 0.3:
            v = window(u, 0.0, 0.3)
            sc.gmat["g_A"] = blend(saw_flat(XA, F1), saw_flat(XB, F0), v, CUBE_C, 30)
            sc.gmat["fence"] = T((FENCE_A + (FENCE_B - FENCE_A) * v, 0, 0))
            chips(False)
            return
        y = F0 + (F1 - F0) * window(u, 0.32, 0.85)
        sc.gmat["g_A"] = saw_flat(XB, y)
        chips(0.32 < u < 0.85 and abs(y) < PANEL_HALF + 7)
        if u >= 0.85:
            w.a_pieces("strip", "scrap_lo")
            sc.group_of["A_scrap_lo"] = "a_lo"
            sc.gmat["a_lo"] = T((-12 * window(u, 0.86, 1.0), 0, 0)) @ saw_flat(XB, F1)

    sc.step("C2 · bandsaw: a strip holding every section",
            "The second cut goes 7 mm on the other side of the plane. That frees a strip about 10 mm wide that holds "
            "every track's mid-length, which is all we section. The rest of the panel is scrap.",
            6.0, cut_b, hold=0.8, cam_to=CAM["saw_strip"],
            labels=[("strip: 3 mm and 7 mm either side of the plane", (M.SAW_X + 5.5, F1 + 20, table_top),
                     (0.95, 0.24)),
                    ("scrap", (M.SAW_X - 40, F1 - 10, table_top), (0.06, 0.62))])

    # the strip, turned a quarter turn, is cut three times: the two blank ends, then between the two groups of nine
    strip_end = saw_flat(XB, F1)
    passes = [0, 2, 1]                                  # indices into CROSS_C
    G0, G1 = -32.0, 26.0                                # strip centre line (world y) before and after a pass
    P2_C = (STRIP_C[0], (M.CROSS_Y[1][1] + M.CROSS_Y[2][0]) / 2, -M.PANEL_T / 2)

    def at_pass(j, y):
        return saw_cross(CROSS_C[passes[j]], y)

    def cross(u):
        sc.alpha["A_scrap_lo"] = 1.0 - window(u, 0.0, 0.2)
        sc.gmat["a_lo"] = T((-12 - 60 * window(u, 0.0, 0.2), 0, 0)) @ saw_flat(XB, F1)
        sc.gmat["fence"] = T((FENCE_B - 70 * window(u, 0.0, 0.2), 0, 0))     # crosscuts use the mitre gauge
        if u < 0.2:
            sc.gmat["g_A"] = blend(strip_end, at_pass(0, G0), window(u, 0.0, 0.2), STRIP_C, 40)
            chips(False)
            return
        j = min(2, int((u - 0.2) / 0.26))
        v = (u - 0.2 - 0.26 * j) / 0.26
        prev = at_pass(j - 1, G1) if j > 0 else at_pass(0, G0)
        if v < 0.25:
            sc.gmat["g_A"] = blend(prev, at_pass(j, G0), window(v, 0.0, 0.25), STRIP_C, 25 if j else 0)
            chips(False)
        else:
            y = G0 + (G1 - G0) * window(v, 0.28, 0.8)
            sc.gmat["g_A"] = at_pass(j, y)
            chips(0.28 < v < 0.8 and abs(y) < 12, table_top - 3)
        if j >= 1 or v >= 0.8:                          # end 1 is off (on the -x side of the blade)
            if sc.group_of.get("A_end1") != "a_e1":
                w.a_pieces("end1", "piece1", "piece2", "end2")
                sc.group_of["A_end1"] = "a_e1"
            sep = window(u, 0.408, 0.46)
            sc.gmat["a_e1"] = T((-25 * sep, 20 * sep, 0)) @ at_pass(0, G1)
            sc.alpha["A_end1"] = 1.0 - window(u, 0.5, 0.62)
        if j >= 2 or (j == 1 and v >= 0.8):             # end 2 is off (+x side)
            sc.group_of["A_end2"] = "a_e2"
            sep = window(u, 0.668, 0.72)
            sc.gmat["a_e2"] = T((25 * sep, 20 * sep, 0)) @ at_pass(1, G1)
            sc.alpha["A_end2"] = 1.0 - window(u, 0.76, 0.88)
        if j == 2 and v >= 0.8:                         # the split: piece 2 (+x side) comes away with its tracks
            sc.group_of["A_piece2"] = "a_p2"
            for n in a_tracks(w, (2,), "trkstrip"):
                sc.group_of[n] = "a_p2"
            sc.gmat["a_p2"] = T((10 * window(u, 0.928, 0.98), 0, 0)) @ at_pass(2, G1)
            sc.alpha["target_plane"] = 0.0
            sc.alpha["target_plane_p1"] = 1.0

    sc.step("C2 · bandsaw: two pieces of nine",
            "Then the strip is cut into two pieces of nine tracks, about 22 mm long, one per mount, and its blank ends "
            "come off. (If the panels are thicker than about 12 mm, the strip is first cut down to about 10 mm.)",
            7.5, cross, hold=0.8, cam_to=CAM["saw_x"],
            labels=[("piece 1: tracks 1–9", (M.SAW_X - 11, G1, table_top), (0.06, 0.30)),
                    ("piece 2: tracks 10–18", (M.SAW_X + 21, G1, table_top), (0.95, 0.30))])

    p1_end = at_pass(2, G1)
    p2_end = T((10, 0, 0)) @ at_pass(2, G1)
    p2_tray = in_tray(0) @ T((L.CENTRE - P2_C[0], L.CENTRE - P2_C[1], 0))
    sliver_c = ((M.FINAL_CUT_X + M.FINE_KERF + M.STRIP_X[1]) / 2, PIECE_YC, -M.PANEL_T / 2)

    def final(u):
        sc.gmat["a_p2"] = blend(p2_end, p2_tray, window(u, 0.0, 0.3), P2_C, 80)
        sc.cam = cam_via([CAM["saw_x"], CAM["saws"], CAM["psaw"]], window(u, 0.0, 0.34))   # over the bench
        if u < 0.3:
            sc.gmat["g_A"] = via([p1_end, T((0, 0, 140)) @ psaw(), psaw()], window(u, 0.0, 0.3), PIECE_C, [80, 0])
            sc.gmat["psaw_arm"] = np.eye(4)
            chips(False)
            return
        dz = M.PSAW_DROP * window(u, 0.32, 0.7) * (1 - window(u, 0.9, 1.0))
        sc.gmat["psaw_disc"] = R((1, 0, 0), -2200 * u, pivot=M.PSAW_C)
        sc.gmat["psaw_arm"] = T((0, 0, -dz))
        sc.gmat["g_A"] = psaw(dz)
        w.particles(np.array([M.PSAW_X, -14.0, M.PSAW_SAMPLE_Z - dz + 1]) if 0.4 < u < 0.7 else None, n=3,
                    kind="chips")
        if u >= 0.7:
            w.a_pieces("piece_cut", "offcut")
            for n in a_tracks(w, (1,), "trkstrip"):
                sc.alpha[n] = 0.0
            for n in a_tracks(w, (1,), "trkcut") + a_tracks(w, (1,), "trkoff"):
                sc.alpha[n] = 1.0
            sc.group_of["A_offcut"] = "a_off"
            for n in a_tracks(w, (1,), "trkoff"):
                sc.group_of[n] = "a_off"
            f = window(u, 0.72, 0.88)
            tip = R((0, 1, 0), 90 * f, pivot=sliver_c)          # it tips away from the disc as it drops
            sc.gmat["a_off"] = T((20 * f, 0, -69 * f * f)) @ psaw(M.PSAW_DROP) @ tip

    sc.step("C2 · fine wet saw: through the piece",
            "Fine wet saw (abrasive cut-off or low-speed precision saw, with coolant). It cuts all the way through the "
            "piece, 0.5 mm from the target plane, and a sliver 1.5–2 mm thick drops off. The new face is flat and "
            "barely deformed, so grinding removes only the last 0.5 mm.",
            7.5, final, hold=1.2, still=True,
            labels=[("target plane (mid-length)", (M.PSAW_X - 0.75, -6, M.PSAW_SAMPLE_Z + M.PANEL_T + 1.2),
                     (0.06, 0.24)),
                    ("cut 0.5 mm from the plane", (M.PSAW_X, -11.25, M.PSAW_SAMPLE_Z + 4), (0.06, 0.62)),
                    ("sliver drops off", (M.PSAW_X + 21, -6, -33), (0.95, 0.70))])
    return sc.save()


# ================================================================================================== sem
def chapter_sem():
    sc = Scene("m2_5_sem", f"{TITLE}: 5/6 mount, polish, SEM")
    w = World(sc)
    printed(w)
    for k in "ABCD":
        del sc.parent[f"g_{k}"]
    for i, k in enumerate("BCD"):
        sc.gmat[f"g_{k}"] = in_tray(i + 1)
    # panel A as piece 1, cut 0.5 mm past the target plane, in the precision saw's chuck
    screws(w, 0.0)
    w.a_pieces("piece_cut")
    for n in a_tracks(w):
        sc.alpha[n] = 0.0
    for n in a_tracks(w, (1,), "trkcut"):
        sc.alpha[n] = 1.0
    sc.alpha["target_plane_p1"] = 1.0
    sc.gmat["g_A"] = psaw(0)
    sc.cam = CAM["psaw"]
    start = psaw(0)
    pad_pose = MP.copy()

    def grind(u):
        if u < 0.4:
            M_end = face_down(POL_SPOT, 0.7) @ pad_pose
            sc.gmat["g_A"] = via([start, T((0, 0, 120)) @ M_end, M_end], window(u, 0.0, 0.4), PIECE_C, [150, 0])
            return
        sc.gmat["pol_platen"] = R((0, 0, 1), -900 * (u - 0.4), pivot=(M.POL_C[0], M.POL_C[1], 0))
        h = 0.7 * (1 - window(u, 0.45, 0.9))
        sc.gmat["g_A"] = face_down(POL_SPOT, h) @ pad_pose
        sc.alpha["target_plane_p1"] = 1.0 - window(u, 0.8, 0.9)
        if u >= 0.9:
            w.a_pieces("piece")
            for n in a_tracks(w, (1,), "trkcut"):
                sc.alpha[n] = 0.0
            for n in a_tracks(w, (1,), "trksec"):
                sc.alpha[n] = 1.0

    sc.step("C2 · grind to the target plane",
            "Then grind the last 0.5 mm down to the target plane: the mid-length of the piece's nine tracks, where "
            "the section is taken.",
            4.5, grind, hold=0.5, cam_to=CAM["pol"])

    # the piece rides on the puck from here on
    sc.parent["g_A"] = "puck"
    sc.gmat["g_A"] = MP.copy()
    seat = face_down(PRESS_SEAT)
    above = T((0, 0, 110)) @ seat
    pol_now = face_down(POL_SPOT)

    def mount(u):
        sc.gmat["pol_platen"] = np.eye(4)
        cap = max(window(u, 0.05, 0.2) * (1 - window(u, 0.58, 0.64)), window(u, 0.7, 0.76))
        sc.gmat["press_cap"] = T((0, 0, 70 * cap))
        if u < 0.36:
            sc.gmat["puck"] = via([pol_now, T((0, 0, 140)) @ above, above, seat], window(u, 0.0, 0.36), PUCK_C)
        elif u < 0.76:
            sc.gmat["puck"] = seat
        # compound granules into the mould
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
                sc.gmat["puck"] = blend(T((0, 0, 50)) @ seat, face_up(ROW_SPOTS[0]), window(u, 0.84, 1.0), PUCK_C,
                                        90)
        for i in range(1, 8):
            a = window(u, 0.86 + 0.015 * i, 0.9 + 0.015 * i)
            sc.alpha[f"puck_{i}"] = a
            sc.alpha[f"puckface_{i}"] = a

    sc.step("C3 · hot-mount",
            "Hot-mount face down in conductive compound, so the SEM does not charge. A piece about 22 × 13 mm in "
            "section fits a 1.25 in puck: eight pucks per run, two per panel.",
            7.0, mount, hold=0.4, cam_to=CAM["press"],
            labels=[("mounting press: mould, ram, cap", (M.PRESS_C[0] - 26, 0, M.PRESS_TOP + 30), (0.06, 0.25))])

    sc.step("C3 · eight pucks",
            "Eight pucks per run, two per panel, each showing nine tracks cut at mid-length.",
            2.5, None, hold=1.0, cam_to=CAM["row"],
            labels=[("panel A, tracks 1–9", (ROW_SPOTS[0][0], ROW_SPOTS[0][1], M.BENCH_Z + M.PUCK_H), (0.06, 0.30)),
                    ("A tracks 10–18, then B to D", (ROW_SPOTS[4][0], ROW_SPOTS[4][1], M.BENCH_Z + M.PUCK_H),
                     (0.95, 0.30))])

    pads = [("320 grit", (0.36, 0.34, 0.31)), ("800 grit", (0.55, 0.53, 0.50)), ("3 µm diamond", (0.93, 0.93, 0.91)),
            ("0.05 µm alumina", (0.80, 0.87, 0.97))]
    up0 = face_up(ROW_SPOTS[0])
    down = face_down(POL_SPOT)

    def polish(u):
        if u < 0.22:
            sc.gmat["puck"] = blend(up0, down, window(u, 0.0, 0.22), PUCK_C, 120)
            return
        sc.gmat["puck"] = down
        sc.gmat["pol_platen"] = R((0, 0, 1), -1300 * (u - 0.22), pivot=(M.POL_C[0], M.POL_C[1], 0))
        k = min(3, int((u - 0.22) / 0.78 * 4))
        sc.color["pol_pad"] = pads[k][1]
        sc.gauges = [("▶ " if j == k else "  ", name) for j, (name, _) in enumerate(pads)]

    sc.step("C4 · grind and polish",
            "Grind with 320, then 800 grit; polish with 3 µm diamond, then 0.05 µm alumina (MIT's sequence).",
            6.0, polish, hold=0.6, cam_to=CAM["pol"])

    etch_pose = face_up(ETCH_SPOT)

    def etch(u):
        sc.gauges = []
        sc.gmat["pol_platen"] = np.eye(4)
        sc.gmat["puck"] = blend(down, etch_pose, window(u, 0.0, 0.3), PUCK_C, 100)
        x, y, z = ETCH_SPOT
        top = z + M.PUCK_H
        d = window(u, 0.3, 0.5) * (1 - window(u, 0.85, 1.0))
        sc.alpha["dropper_tube"] = d
        sc.alpha["dropper_bulb"] = d
        sc.gmat["dropper"] = T((x, y, top + 18 + 120 * (1 - d)))
        fall = window(u, 0.5, 0.62)
        sc.alpha["drop"] = 1.0 if 0.5 < u < 0.62 else 0.0
        sc.gmat["drop"] = T((x, y, top + 16 - 14 * fall))
        sc.alpha["film"] = 0.9 * window(u, 0.6, 0.7) * (1 - window(u, 0.85, 0.97))
        sc.gmat["film"] = T((0, 0, -0.32))
        if u > 0.7:
            sc.color["A_piece"] = mix(M.INSERT_STEEL, (0.62, 0.60, 0.58), window(u, 0.7, 0.9))

    sc.step("C4 · etch",
            "Etch right after polishing, because 316 passivates fast: dilute aqua regia for 30–45 s in a fume hood, "
            "or 10 % oxalic acid electrolytically. Check the etch and the track order under the optical microscope.",
            5.0, etch, hold=0.6, cam_to=CAM["etch"],
            labels=[("section face: nine tracks at mid-length", (ETCH_SPOT[0], ETCH_SPOT[1], ETCH_SPOT[2] + M.PUCK_H),
                     (0.95, 0.30))])

    stage_pose = face_up(STAGE)

    def sem(u):
        door = window(u, 0.05, 0.25) * (1 - window(u, 0.55, 0.7))
        sc.gmat["sem_door"] = T((0, -230 * door, 0))
        sc.gmat["puck"] = via([etch_pose, T((0, -260, 160)) @ stage_pose, T((0, 0, 40)) @ stage_pose, stage_pose],
                              window(u, 0.2, 0.55), PUCK_C)
        g = window(u, 0.6, 0.75)
        sc.alpha["sem_chamber"] = 1.0 - 0.75 * g
        sc.alpha["sem_door"] = 1.0 - 0.75 * g
        sc.alpha["sem_door_handle"] = 1.0 - 0.75 * g
        if u > 0.75:
            sx, sy = M.SEM_C
            k = int(u * 400) % 20
            tx = sx - 10 + (u * 4000 % 20)
            ty = sy - 3 + 0.3 * k
            sc.alpha["sem_beam"] = 1.0
            sc.set_mesh("sem_beam", pv.Line((sx, sy, 110), (tx, ty, STAGE[2] + M.PUCK_H)).tube(radius=0.8))
        else:
            sc.alpha["sem_beam"] = 0.0

    sc.step("C5 · SEM",
            "SEM: secondary-electron images of every track at two fixed magnifications, plus EDS spots on a few "
            "keyhole tracks to check for Mn and Cr lost to evaporation.",
            6.0, sem, hold=0.8, cam_to=CAM["sem"], still=True,
            labels=[("electron column", (M.SEM_C[0] + 58, 0, 420), (0.95, 0.22)),
                    ("puck on the stage", (M.SEM_C[0], -10, STAGE[2] + M.PUCK_H), (0.06, 0.62))])

    return sc.save()


# ============================================================================================== results
def chapter_results():
    """The monitor: SEM images, measurement, comparison with the AM Module (C5-C7). Starts where m2_5_sem ends."""
    sc = Scene("m2_6_results", f"{TITLE}: 6/6 measure and compare")
    w = World(sc)
    printed(w)
    for k in "ABCD":
        del sc.parent[f"g_{k}"]
    for i, k in enumerate("BCD"):
        sc.gmat[f"g_{k}"] = in_tray(i + 1)
    screws(w, 0.0)
    w.a_pieces("piece")
    for n in a_tracks(w):
        sc.alpha[n] = 0.0
    for n in a_tracks(w, (1,), "trksec"):
        sc.alpha[n] = 1.0
    sc.color["A_piece"] = (0.62, 0.60, 0.58)
    sc.parent["g_A"] = "puck"
    sc.gmat["g_A"] = MP.copy()
    sc.gmat["puck"] = face_up(STAGE)
    sc.alpha["puck"] = 1.0
    for i in range(1, 8):
        sc.show([f"puck_{i}", f"puckface_{i}"], 1.0)
    sc.show(["sem_chamber", "sem_door", "sem_door_handle"], 0.25)
    sx, sy = M.SEM_C
    sc.alpha["sem_beam"] = 1.0
    sc.set_mesh("sem_beam", pv.Line((sx, sy, 110), (sx, sy, STAGE[2] + M.PUCK_H)).tube(radius=0.8))
    sc.cam = CAM["sem"]

    def to_screen(u):
        sc.alpha["sem_beam"] = 0.0
        sc.alpha["screen_sem"] = window(u, 0.4, 0.8)

    sc.step("C5 · SEM images",
            "Each track's cross-section, imaged at the same magnification. (The shapes here are illustrations "
            "drawn from P/v, not data.)",
            3.0, to_screen, hold=2.2, cam_to=CAM["mon"])

    def to_measure(u):
        sc.alpha["screen_measure"] = window(u, 0.0, 0.5)
        sc.alpha["screen_sem"] = 1.0 - window(u, 0.5, 0.6)

    sc.step("C6 · measure",
            "Measure each track's width, depth below the substrate surface, height above it and fused area, and "
            "classify the regime.",
            1.5, to_measure, hold=3.0)

    def to_parity(u):
        sc.alpha["screen_parity"] = window(u, 0.0, 0.5)
        sc.alpha["screen_measure"] = 1.0 - window(u, 0.5, 0.6)

    sc.step("C7 · compare with the AM Module",
            "Compare with the AM Module predictions committed before printing: calibrate on part of the tracks, "
            "validate on the held-out rest. The pilot's timing log then sizes the campaign.",
            1.5, to_parity, hold=3.5, still=True)
    return sc.save()


CHAPTERS = [("m2_1_setup", "Set up: panels into the plate, flushness, job file, powder (B2, A1, B3)"),
            ("m2_2_print", "Print: inert, recoat one layer, expose 72 tracks (B4, B5)"),
            ("m2_3_unload", "Unload: depowder, unscrew the panels, top-view images (B6, B7, C1)"),
            ("m2_4_cut", "Cut: a strip holding every section, two pieces, the fine wet saw (C2)"),
            ("m2_5_sem", "Mount, polish, etch, SEM (C2 to C5)"),
            ("m2_6_results", "Measure and compare with the AM Module (C5 to C7)")]


def join():
    """out/mp4/m2_full.mp4: the six chapters joined, with chapter marks in the file and a YouTube chapter list."""
    parts = [OUT / "mp4" / f"{n}.mp4" for n, _ in CHAPTERS]
    lst = OUT / "mp4" / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    meta = OUT / "mp4" / "chapters.ffmeta"
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
                    str(OUT / "mp4" / "m2_full.mp4")], check=True)
    lst.unlink()
    meta.unlink()
    (OUT / "mp4" / "m2_full_chapters.txt").write_text("\n".join(yt) + "\n")
    print("wrote out/mp4/m2_full.mp4,", f"{t / FPS:.1f} s;", "chapters:", *yt, sep="\n  ")


if __name__ == "__main__":
    which = sys.argv[1:] or ["setup", "print", "unload", "cut", "sem", "results"]
    for name in which:
        {"setup": chapter_setup, "print": chapter_print, "unload": chapter_unload, "cut": chapter_cut,
         "sem": chapter_sem, "results": chapter_results, "full": join}[name]()
