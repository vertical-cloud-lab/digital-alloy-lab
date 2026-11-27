"""Tessellation and pyvista rendering helpers shared by render.py and the analysis scripts."""

import numpy as np
import pyvista as pv


def to_mesh(shape, tol=0.25, ang=0.3):
    verts, tris = shape.tessellate(tol, ang)
    v = np.array([(p.x, p.y, p.z) for p in verts], dtype=float)
    if len(tris) == 0:
        return None
    f = np.hstack([np.full((len(tris), 1), 3), np.array(tris, dtype=np.int64)]).ravel()
    return pv.PolyData(v, f).clean()


def plotter(size=(1600, 1200), bg="white"):
    pv.global_theme.allow_empty_mesh = True
    pl = pv.Plotter(off_screen=True, window_size=size)
    pl.set_background(bg)
    pl.enable_anti_aliasing("ssaa")
    return pl


def add_parts(pl, parts, opacity=None, clip=None, tol=0.25, edge=False):
    """parts: list of (name, cq shape, rgb, material). clip: 'y' to cut away y < 0 (section view)."""
    meshes = []
    for name, shape, col, mat in parts:
        m = to_mesh(shape, tol)
        if m is None or m.n_points == 0:
            continue
        if clip == "y":
            m = m.clip(normal=(0, -1, 0), origin=(0, 0, 0), invert=False)
            if m.n_points == 0:
                continue
        op = 1.0
        if opacity and name in opacity:
            op = opacity[name]
        elif "glass" in name or "quartz" in name:
            op = 0.35
        pl.add_mesh(m, color=col, opacity=op, smooth_shading=True, specular=0.4, specular_power=20,
                    show_edges=edge, edge_color=(0.3, 0.3, 0.3), line_width=0.5)
        meshes.append((name, m))
    return meshes
