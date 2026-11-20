"""pyvista renders for the robot shop (offscreen; run under xvfb-run). Used by shop_checks.py.

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python desktop-lpbf/analysis/shop/shop_render.py   # layout only
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pyvista as pv

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import shop_cell as S  # noqa: E402

OUT = HERE.parent / "out" / "shop"
pv.OFF_SCREEN = True


def poly(v, f):
    return pv.PolyData(np.asarray(v, float), np.c_[np.full(len(f), 3), np.asarray(f)].ravel())


def add_items(p, items, opacity=1.0, skip=(), alpha_names=()):
    for name, (v, f), color in items:
        if any(s in name for s in skip):
            continue
        op = 0.25 if any(s in name for s in alpha_names) else opacity
        p.add_mesh(poly(v, f), color=color, opacity=op, smooth_shading=False, show_edges=False)


def add_body(p, b, color=None, opacity=1.0):
    v = b.v @ b.M[:3, :3].T + b.M[:3, 3]
    p.add_mesh(poly(v, b.f), color=color or b.color, opacity=opacity, smooth_shading=True)


def add_arm(p, arm, held_color=S.COL["part"]):
    for b in arm.bodies():
        if arm.held is not None and b is arm.held[0]:
            add_body(p, b, held_color)
        else:
            add_body(p, b)


def snap(path, items, arms=(), cam=None, title="", size=(1100, 760), extra=(), alpha_names=(), skip=(), marks=()):
    p = pv.Plotter(off_screen=True, window_size=size)
    p.set_background("white")
    add_items(p, items, alpha_names=alpha_names, skip=skip)
    for a in arms:
        add_arm(p, a)
    for b, color in extra:
        add_body(p, b, color)
    for pt, color in marks:
        p.add_mesh(pv.Sphere(radius=12, center=pt), color=color)
    if title:
        p.add_text(title, font_size=10, color="black", position="upper_left")
    if cam is not None:
        p.camera_position = cam
    p.enable_anti_aliasing("ssaa") if hasattr(p, "enable_anti_aliasing") else None
    p.screenshot(str(path))
    p.close()


def layout(shop, path, arms=(), extra_items=(), routes=()):
    """Plan view of the whole shop, stations labelled, plus a 3/4 view."""
    items = list(extra_items)
    for st in shop.values():
        items += st.world_items()
    floor = ("floor", S.box(0, 16000, 1000, 10000, -20, 0), S.COL["floor"])
    aisle = ("aisle", S.box(0, 16000, 4000, 7000, -19, 0.5), "#dfe6ea")
    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.set_background("white")
    add_items(p, [floor, aisle] + items, skip=("roof",))
    for a in arms:
        add_arm(p, a)
    for st in shop.values():
        c = st.to_world((0, 900 if st.pose[2] == 0 else 900, 2900))
        p.add_point_labels([c], [st.name], font_size=14, point_size=1, shape_opacity=0.6, always_visible=True)
    for poly in routes:
        pts = np.array([[x, y, 30.0] for x, y in poly], float)
        p.add_mesh(pv.lines_from_points(pts), color="#d62828", line_width=4)
        p.add_mesh(pv.Sphere(radius=90, center=pts[-1]), color="#d62828")
    p.view_xy()
    p.camera.zoom(1.25)
    p.screenshot(str(path))
    p.close()
    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.set_background("white")
    add_items(p, [floor, aisle] + items, skip=("roof",))
    for a in arms:
        add_arm(p, a)
    p.camera_position = [(7500, -8500, 13500), (7500, 5200, 0), (0, 0, 1)]
    p.screenshot(str(path).replace(".png", "_3d.png"))
    p.close()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    shop = S.build_shop()
    layout(shop, OUT / "shop_layout.png")
    print("wrote", OUT / "shop_layout.png")
