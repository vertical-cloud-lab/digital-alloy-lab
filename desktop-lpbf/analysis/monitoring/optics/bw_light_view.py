#!/usr/bin/env python3
"""Two views of the BW light as drawn (cad/monitoring_parts.py _bw_light(); monitoring/optics.md §4.1), from the full model with
the monitoring parts: from the front-left across the light's axis, and from above and behind. The clamp and bracket are drawn
see-through so the lens tube and asphere show; the red line is the BW sight line to the plate centre.

    /tmp/heavy 3 xvfb-run -a -s "-screen 0 1920x1080x24" python bw_light_view.py      (~1 min; builds the model)
Writes analysis/out/monitoring/optics/bw_light_view.png.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "analysis" / "out" / "monitoring" / "optics"
sys.path.insert(0, str(ROOT / "cad"))
import cadquery as cq  # noqa: E402
import pyvista as pv  # noqa: E402

import lpbf_low as M  # noqa: E402
import monitoring_spec as MS  # noqa: E402

KEEP = ("BW LED", "Process chamber body", "BW window clamp frame", "BW light window", "BW window gasket", "Recoater sensor posts",
        "Recoater sensor clamps", "Recoater home", "Cross-flow inlet plenum", "Chamber lid", "Chamber floor plate", "Inlet plenum port")
VIEWS = [((-345, -60, 120), (-150, 135, 40), "from the front-left, across the light's axis"),
         ((-330, 330, 210), (-150, 140, 35), "from behind and above")]


def main():
    parts = M.build(monitoring=True)
    box = cq.Solid.makeBox(230, 200, 220, cq.Vector(-240, 60, -60))
    meshes = []
    for p in parts:
        if not p.name.startswith(KEEP):
            continue
        sh = p.shape if p.name.startswith("BW LED") else p.shape.intersect(box)
        vs, ts = sh.tessellate(0.1, 0.3)
        if not ts:
            continue
        v = np.array([(q.x, q.y, q.z) for q in vs])
        f = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
        see = p.name.startswith(("BW LED clamp", "BW LED bracket"))
        meshes.append((pv.PolyData(v, f), p.color, 0.35 if see else getattr(p, "opacity", 1.0) or 1.0))
    pl = pv.Plotter(off_screen=True, window_size=(2000, 760), shape=(1, 2), border=False)
    c = MS.VIEWPORTS["BW"]["centre"]
    for k, (pos, foc, title) in enumerate(VIEWS):
        pl.subplot(0, k)
        pl.set_background("white")
        for m, col, op in meshes:
            pl.add_mesh(m, color=col, opacity=op, smooth_shading=False)
        pl.add_mesh(pv.Line(tuple(c), (0.0, 0.0, 0.0)), color="#d22b2b", line_width=3)
        pl.add_text(title, position="upper_left", font_size=11, color="#191919")
        pl.camera_position = [pos, foc, (0, 0, 1)]
        pl.camera.zoom(1.5 if k == 0 else 1.2)
    OUT.mkdir(parents=True, exist_ok=True)
    pl.screenshot(str(OUT / "bw_light_view.png"))
    print("wrote", OUT / "bw_light_view.png")


if __name__ == "__main__":
    main()
