"""Shared contract for the robot-built desktop LPBF video (issue #260, PR #266, round 7).

Sterling, 2026-11-25: "we should see the assembly being carried out **by** two UR12e units each on a MiR250 using the
full set of parts spread across a really long table", with running cost (new against used), lead times and time
estimates on screen, and a person only where one is really needed.

Several renderers draw chapters in parallel (machining, assembly, the parts table). Each writes raw 3-D frames plus one
line of metadata per frame; `compose.py` then draws the on-screen panels (captions, who is working, clocks, cost and
lead-time panels) over the frames and joins the chapters into one MP4. So the panels can change without re-rendering
the 3-D, and every chapter shares one look.

Frames
------
* `HALL`: mm, z up, floor z = 0. It is the frame of analysis/assembly/cell2.py (the two-arm assembly bench runs along x,
  arm A docks on the front, y = -640, arm B on the back, y = +640), extended with the long parts table in line with the
  bench (`LONG_TABLE`), so both MiRs reach it from their own lane.
* The robot shop of analysis/shop/shop_cell.py (VF-4, lathe, saw, wash, measuring, receiving) sits beside it:
  hall = shop + `SHOP_IN_HALL` (a pure translation). Chapters may be drawn in either frame; overview shots use the hall.

Per-frame metadata (`meta.jsonl`, one JSON object per frame, in frame order), all keys optional except `caption`:
    caption     str   the line at the top: what is happening
    sub         str   a second, smaller line (numbers, sources)
    who         list  of "robot A", "robot B", "person", "machine", "outsourced", "supplier": who is working now
    step        str   the step id (assembly M01..., machining part/setup id) or ""
    status      str   "pass" | "fail" | "redesign" | "person" | "" : shown as a coloured badge
    proc_s      float real-world seconds this frame stands for (1/FPS for real time; more in a time-lapse)
    add         dict  increments to the counters: {"machine_h", "robot_h", "person_h", "cam_h", "outsourced_d"}
    cost        dict  the cost panel's state (kit chapter): {"cat", "new", "used", "run_new", "run_used", "items": [...]}
    lead        dict  the lead-time panel's state: {"highlight": [names]}
    labels      list  of [x_px, y_px, text] screen labels (computed by the renderer from 3-D points)
    chapter     str   the chapter title (the compositor makes the YouTube chapter list from changes in it)

Files: /tmp/robotbuild/frames/<NN-chapter>/<00000>.png (W x H, RGB) and meta.jsonl beside them. Never commit frames.
"""
from __future__ import annotations

import json
import os
import pathlib

import numpy as np

W, H = 1280, 720                     # every 3-D frame
FPS = 12                             # playback rate of the final MP4
ROOT = pathlib.Path(os.environ.get("ROBOTBUILD", "/tmp/robotbuild"))
FRAMES = ROOT / "frames"
TRAJ = ROOT / "traj"
DATA = ROOT / "data"
REPO = pathlib.Path(__file__).resolve().parents[3]
LPBF = REPO / "desktop-lpbf"

# ------------------------------------------------------------------ the hall (cell2's frame)
BENCH_X = (-1550.0, 1600.0)          # cell2's stations and docks span this along x
LANE_Y = {"A": -640.0, "B": 640.0}   # arm bases (cell2.ARM_Y); the MiRs drive along these lines
LONG_TABLE = dict(x0=2600.0, x1=14600.0, y0=-450.0, y1=450.0, top=860.0, t=40.0,
                  note="12 m x 0.9 m, phenolic top on steel legs, 860 mm high: in line with the assembly bench, so both "
                       "MiRs reach it from their own lane (a UR12e reaches 1300 mm)")
SHOP_IN_HALL = np.array([0.0, -12000.0, 0.0])  # shop_cell: north row (VF-4, lathe, wash, measuring, bench) at shop
                                               # y 7000-9314 -> hall y -5000 to -2686, 1.6 m behind MiR A's lane;
                                               # its aisle (shop y 4000-7000) -> hall y -8000 to -5000

# ------------------------------------------------------------------ look
BG_TOP, BG_BOTTOM = "#f4f6f8", "#d9dee3"
FLOOR = "#b9bdb8"
COL = dict(
    ur="#cfd5db", ur_joint="#3d4b5c", mir="#4a4f55", mir_top="#2f3338", cabinet="#5e656d",
    gripper="#2b2f33", tool="#e0a526", tool_dark="#6b5a2c", fixture="#2f7fbf", fixture_soft="#6fa8d6",
    person_shirt="#3b6ea5", person_trousers="#2e3440", skin="#d9a982",
    table="#d8d2c4", table_leg="#6b7078", haas="#d8dde1", haas_dark="#47515b", haas_red="#c8102e",
    held="#f2c14e", fail="#d1495b", ok="#2a9d8f", redesign="#e9a23b",
)
MAT = dict(smooth_shading=True, specular=0.25, specular_power=20, ambient=0.25, diffuse=0.8)
WHO_COL = {"robot A": "#2a7fff", "robot B": "#8e44ad", "person": "#e67e22", "machine": "#5d6d7e",
           "outsourced": "#16a085", "supplier": "#7f8c8d"}


def plotter(size=(W, H)):
    """An off-screen pyvista plotter with the shared background and lights (call under xvfb-run)."""
    import pyvista as pv
    pl = pv.Plotter(off_screen=True, window_size=size, lighting="none")
    pl.set_background(BG_BOTTOM, top=BG_TOP)
    pl.add_light(pv.Light(position=(1, -1, 1.6), focal_point=(0, 0, 0), intensity=0.75, positional=False,
                          light_type="scene light"))
    pl.add_light(pv.Light(position=(-1, 0.6, 0.9), focal_point=(0, 0, 0), intensity=0.35, positional=False,
                          light_type="scene light"))
    pl.add_light(pv.Light(position=(0, 0, 1), focal_point=(0, 0, 0), intensity=0.25, positional=False,
                          light_type="scene light"))
    try:
        pl.enable_anti_aliasing("ssaa")
    except Exception:
        pass
    return pl


class Chapter:
    """Writes one chapter's frames and meta.jsonl. `name` like "30-assembly-module"; chapters sort by name."""

    def __init__(self, name, title):
        self.dir = FRAMES / name
        self.dir.mkdir(parents=True, exist_ok=True)
        for f in self.dir.glob("*.png"):
            f.unlink()
        self.meta = open(self.dir / "meta.jsonl", "w")
        self.n = 0
        self.title = title

    def frame(self, img, caption, **meta):
        """img: an HxWx3 uint8 array (pyvista screenshot) or a PIL image."""
        from PIL import Image
        im = img if hasattr(img, "save") else Image.fromarray(np.asarray(img)[:, :, :3])
        if im.size != (W, H):
            im = im.resize((W, H))
        im.save(self.dir / f"{self.n:05d}.png", compress_level=1)
        meta = dict(meta)
        meta["caption"] = caption
        meta.setdefault("chapter", self.title)
        meta.setdefault("proc_s", 1.0 / FPS)
        self.meta.write(json.dumps(meta) + "\n")
        self.n += 1

    def close(self):
        self.meta.close()
        (self.dir / "done").write_text(str(self.n))


def project(pl, pts):
    """3-D points (N x 3, mm) to pixel positions (x right, y down) in the current camera, for `labels`."""
    import vtk
    pts = np.atleast_2d(np.asarray(pts, float))
    ren = pl.renderer
    out = []
    coord = vtk.vtkCoordinate()
    coord.SetCoordinateSystemToWorld()
    for p in pts:
        coord.SetValue(*p)
        x, y = coord.GetComputedDisplayValue(ren)
        out.append((float(x), float(pl.window_size[1] - y)))
    return out
