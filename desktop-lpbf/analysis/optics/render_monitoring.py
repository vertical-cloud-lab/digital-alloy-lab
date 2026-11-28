#!/usr/bin/env python3
"""Render where the monitoring.md sensors go on the current model (issue #260).

Process module in the lasing state (recoater at the end of its stroke), guard hidden, chamber walls, lid and door see-through.
Added as overlays, not as model parts:
  - sight cones from the Ø20 windows to the L75 plate: the existing layer camera (lid, 33° off vertical), the proposed left-wall
    port at (-156, -20, 40) (14° elevation) and a steep lid port at (-60, -80, 136) (54°, needs a cut-out in the optics bridge);
  - a Chronos 2.1-HD-sized camera (155 x 96 x 67 mm) behind a Ø60 x 60 lens on the left-wall line of sight;
  - the coaxial camera branch (a 30 mm cage cube, tube lens and an IMX296 board) off the photodiode chain above the bridge;
  - an acoustic-emission waveguide from the plate's underside down the hollow rod.
Writes analysis/out/monitoring/sensors.png and sensors-chamber.png.

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python desktop-lpbf/analysis/optics/render_monitoring.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pyvista as pv
import trimesh
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "monitoring"
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import lpbf_low as M  # noqa: E402
import render_low as R  # noqa: E402

STATE = {"recoater": M.MOTION["recoater"]["hi"]}
GLASSY = ("Process chamber body", "Chamber lid", "Chamber door", "Chamber floor plate", "Lift-out wall liner", "Cover-slide drawer",
          "Window flange", "Window retaining ring", "Camera viewport adapter")
HIDE = R.SECTION_HIDE + ("Optics bridge", "Optics-bridge screws", "Rack", "19 in.", "UPS", "Fiber laser", "Scan + laser",
                         "DIN-rail drawer", "Process fiber", "Gas-loop", "Argon line", "O2 sample", "Vacuum line", "Vacuum isolation",
                         "AprilTag", "Guard-position switch", "Guard-door handle", "Base plate", "base plate", "Leveling", "levelling")
L75_R = 76.2 / 2


def rot_to(d):
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(z, d)
    s, c = np.linalg.norm(v), float(z @ d)
    if s < 1e-9:
        return np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    k = v / s
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + s * K + (1 - c) * K @ K


def disc(c, n, r, k=32):
    a = np.cross(n, [0.0, 0.0, 1.0])
    if np.linalg.norm(a) < 1e-6:
        a = np.cross(n, [1.0, 0.0, 0.0])
    a /= np.linalg.norm(a)
    b = np.cross(n, a)
    t = np.linspace(0, 2 * math.pi, k, endpoint=False)
    return c + r * (np.outer(np.cos(t), a) + np.outer(np.sin(t), b))


def hull_mesh(points):
    h = trimesh.convex.convex_hull(points)
    faces = np.hstack([np.full((len(h.faces), 1), 3), h.faces]).ravel()
    return pv.PolyData(np.asarray(h.vertices), faces)


def sight_cone(port, ap_r=10.0, plate_r=L75_R):
    port = np.asarray(port, float)
    tgt = np.array([0.0, 0.0, 0.3])
    d = (tgt - port) / np.linalg.norm(tgt - port)
    return hull_mesh(np.vstack([disc(port, d, ap_r), disc(tgt, np.array([0.0, 0.0, 1.0]), plate_r, 64)]))


def on_axis(mesh, port, start, length_axis_centre=0.0):
    """Place a mesh built along +z (centred on z = length_axis_centre) on the port's outward line of sight, `start` mm out."""
    port = np.asarray(port, float)
    d = port - np.array([0.0, 0.0, 0.3])
    d /= np.linalg.norm(d)
    T = np.eye(4)
    T[:3, :3] = rot_to(d)
    T[:3, 3] = port + d * (start + length_axis_centre)
    return mesh.transform(T, inplace=False)


def main():
    parts = M.build(include_tray=False, module="L75")
    parts = [p for p in parts if not any(k in p.name for k in HIDE) and p.module == "process" and "context" not in p.tags]
    sc = R.Scene(parts, (1500, 1000))
    sc.set(state=STATE, opacity=lambda p: 0.16 if any(k in p.name for k in GLASSY) else p.opacity)

    left, lid, layer = (-156.0, -20.0, 40.0), (-60.0, -80.0, 136.0), (75.0, -45.0, 136.0)
    sc.put("cone_layer", sight_cone(layer), color="#3b82f6", opacity=0.35)
    sc.put("cone_left", sight_cone(left), color="#f97316", opacity=0.45)
    sc.put("cone_lid", sight_cone(lid), color="#a855f7", opacity=0.30)
    sc.put("plate_ring", pv.Disc(center=(0, 0, 0.4), inner=0.0, outer=L75_R, normal=(0, 0, 1), c_res=64), color="#fde68a", opacity=0.9)
    # left-wall camera: Ø60 x 60 lens from 15 mm out, then a Chronos-sized body (155 long, 96 x 67)
    lens = pv.Cylinder(center=(0, 0, 0), direction=(0, 0, 1), radius=30.0, height=60.0, resolution=48)
    sc.put("lens_left", on_axis(lens, left, 15.0, 30.0), color="#1f2937", **R.MAT)
    body = pv.Box(bounds=(-48.0, 48.0, -33.6, 33.6, 0.0, 155.0))
    sc.put("body_left", on_axis(body, left, 75.0), color="#dc2626", **R.MAT)
    window = pv.Cylinder(center=(0, 0, 0), direction=(0, 0, 1), radius=14.0, height=14.0, resolution=48)
    sc.put("boss_left", on_axis(window, left, 0.0, 7.0), color="#9ca3af", **R.MAT)
    # lid steep port: a compact IMX296-class camera + 50 mm lens (Ø40 x 100), through a cut-out in the bridge
    cam2 = pv.Cylinder(center=(0, 0, 0), direction=(0, 0, 1), radius=20.0, height=100.0, resolution=48)
    sc.put("cam_lid", on_axis(cam2, lid, 30.0, 50.0), color="#7c3aed", **R.MAT)
    # coaxial branch: a 30 mm cage cube in the photodiode chain at x -215, a tube lens toward -y and an IMX296 board
    cube = pv.Box(bounds=(-235.0, -195.0, -45.0, -5.0, 246.0, 286.0))
    tube = pv.Cylinder(center=(-215.0, -85.0, 266.0), direction=(0, 1, 0), radius=13.0, height=80.0, resolution=32)
    board = pv.Box(bounds=(-234.0, -196.0, -137.0, -125.0, 247.0, 285.0))
    for k, m in (("cube", cube), ("tube", tube), ("board", board)):
        sc.put(f"coax_{k}", m, color="#16a34a", **R.MAT)
    # AE waveguide: Ø3 rod from the plate's underside down the module axis to a sensor below the rod end
    rod = pv.Cylinder(center=(6.0, 0.0, -70.0), direction=(0, 0, 1), radius=1.5, height=140.0, resolution=24)
    sensor = pv.Cylinder(center=(6.0, 0.0, -148.0), direction=(0, 0, 1), radius=9.5, height=16.0, resolution=32)
    sc.put("ae_rod", rod, color="#eab308", **R.MAT)
    sc.put("ae_sensor", sensor, color="#ca8a04", **R.MAT)

    labels = {
        "layer camera (in the design)": (110.0, -70.0, 230.0),
        "left-wall port + Chronos-sized camera (14°)": (-300.0, -60.0, 150.0),
        "steep lid port (54°): needs a bridge cut-out": (-120.0, -150.0, 270.0),
        "coaxial camera branch": (-215.0, -137.0, 300.0),
        "AE waveguide + sensor": (6.0, -20.0, -150.0),
    }
    sc.pl.add_point_labels(np.array(list(labels.values())), list(labels.keys()), font_size=13, point_size=1, shape_opacity=0.75,
                           always_visible=True, text_color="#111827", shape_color="#ffffff", name="labels")
    f = (-90.0, -20.0, 80.0)
    sc.cam(R.orbit(f, 1250, -52, 22), f)
    sc.title("In-situ monitoring: proposed sensor positions on the current model (monitoring.md)", 12)
    OUT.mkdir(parents=True, exist_ok=True)
    Image.fromarray(sc.shot()).save(OUT / "sensors.png")
    # close view into the chamber from the front-left, door see-through
    sc.pl.remove_actor("labels")
    f2 = (-30.0, 0.0, 30.0)
    sc.cam(R.orbit(f2, 560, 25, 32), f2)
    sc.title("Sight cones to the Ø75 plate: layer camera (blue), left-wall port (orange), steep lid port (purple)", 12)
    Image.fromarray(sc.shot()).save(OUT / "sensors-chamber.png")
    print("wrote", OUT / "sensors.png", OUT / "sensors-chamber.png")


if __name__ == "__main__":
    main()
