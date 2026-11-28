"""Draw one FEA result off-screen with pyvista. fea.render() writes the surface (points, triangles, displacement, scalar)
and the view to an .npz and runs this script on it, in its own process: VTK's memory is freed when it exits and never adds
to a CalculiX solve, and the volume mesh is never handed to VTK.

Run:  python render_fea.py scratch.npz        (under xvfb-run on a headless runner)
"""
from __future__ import annotations

import json
import sys

import numpy as np


def main(npz):
    import pyvista as pv
    d = np.load(npz, allow_pickle=False)
    o = json.loads(str(d["opt"]))
    pts, tri, U, s = d["pts"], d["tri"], d["U"], d["s"]
    faces = np.hstack([np.full((len(tri), 1), 3, dtype=np.int64), tri.astype(np.int64)]).ravel()
    base = pv.PolyData(pts, faces)
    surf = pv.PolyData(pts + o["scale"] * U, faces)
    surf.point_data["s"] = s
    pl = pv.Plotter(off_screen=True, window_size=(1200, 820))
    pl.set_background("white")
    pl.add_mesh(surf, scalars="s", cmap=o["cmap"], clim=o["clim"], smooth_shading=True, split_sharp_edges=True,
                scalar_bar_args=dict(title=o["label"], vertical=True, fmt="%.3g", title_font_size=14, label_font_size=12, position_x=0.86, position_y=0.12))
    pl.add_mesh(base.extract_feature_edges(35), color="black", line_width=0.6, opacity=0.25)
    if o["mark"] is not None:
        pl.add_mesh(pv.Sphere(radius=0.012 * o["diag"], center=o["mark"]), color="magenta")
    pl.add_text(o["title"], font_size=10, color="black")
    pl.view_vector(o["view"], viewup=o["up"])
    pl.camera.zoom(o["zoom"])
    pl.screenshot(o["path"])
    pl.close()


if __name__ == "__main__":
    main(sys.argv[1])
