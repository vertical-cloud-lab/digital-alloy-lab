"""Scale references for the build animation (render_build.py): things everyone knows the size of, and dimension lines.

A machinist watching the first animation couldn't tell how big the chamber was ("the size and scale aren't immediately
apparent from the video"). Every chapter now puts one of these next to the work:

  soda can     a US 12 fl oz (355 mL) can: Ø66 x 122 mm (the "211" body; the "202" end is Ø54)
  steel rule   a 300 mm (12 in.) rule, 25 mm wide, ticks every 10 mm, longer every 50 and 100 mm
  person       a 1750 mm mannequin, for the tray and the shop
  dims         dimension lines with extension lines, end ticks and a label in mm and inches

The meshes are plain pyvista; colours are neutral so nothing reads as a brand.
"""
from __future__ import annotations

import math

import numpy as np
import pyvista as pv

INCH = 25.4
INK = "#1d2733"
CAN = dict(d=66.0, h=122.0, end_d=54.0, neck=9.0)
RULE = dict(L=300.0, w=25.0, t=1.0)


def soda_can(at=(0.0, 0.0, 0.0)):
    """[(mesh, colour)]: a 12 fl oz can standing on `at` (its base centre)."""
    x, y, z = map(float, at)
    r, h, re, nk = CAN["d"] / 2, CAN["h"], CAN["end_d"] / 2, CAN["neck"]
    body = pv.Cylinder(center=(x, y, z + nk + (h - 2 * nk) / 2), direction=(0, 0, 1), radius=r, height=h - 2 * nk, resolution=48)
    top = pv.Cylinder(center=(x, y, z + h - nk / 2), direction=(0, 0, 1), radius=(r + re) / 2, height=nk, resolution=48)
    bot = pv.Cylinder(center=(x, y, z + nk / 2), direction=(0, 0, 1), radius=(r + re) / 2, height=nk, resolution=48)
    lid = pv.Disc(center=(x, y, z + h + 0.2), inner=0.0, outer=re, normal=(0, 0, 1), c_res=48)
    band = pv.Cylinder(center=(x, y, z + h * 0.52), direction=(0, 0, 1), radius=r + 0.3, height=h * 0.34, resolution=48)
    return [(body, "#c8323a"), (top, "#c9ced3"), (bot, "#c9ced3"), (lid, "#aeb4ba"), (band, "#f2f2f2")]


def steel_rule(at=(0.0, 0.0, 0.0), axis=(1.0, 0.0, 0.0), L=RULE["L"]):
    """([(mesh, colour)], [(point, label)]): a steel rule lying flat from `at` along `axis` (in the xy plane)."""
    a = np.asarray(axis, float)
    a /= np.linalg.norm(a)
    n = np.array([-a[1], a[0], 0.0])               # across the rule
    p0 = np.asarray(at, float)
    w, t = RULE["w"], RULE["t"]
    corners = [p0, p0 + a * L, p0 + a * L + n * w, p0 + n * w]
    base = pv.PolyData(np.array(corners), faces=[4, 0, 1, 2, 3]).extrude((0, 0, t), capping=True)
    ticks = []
    for mm in range(0, int(L) + 1, 10):
        ln = 12.0 if mm % 100 == 0 else 8.0 if mm % 50 == 0 else 5.0
        q = p0 + a * mm + np.array([0, 0, t + 0.05])
        ticks.append(pv.Line(q, q + n * ln))
    labels = [(p0 + a * mm + n * (w * 0.75) + np.array([0, 0, t + 1]), "0" if mm == 0 else f"{mm // 10} cm") for mm in (0, 100, 200, 300) if mm <= L]
    tick = ticks[0].merge(ticks[1:]) if len(ticks) > 1 else ticks[0]
    return [(base, "#d5d9dd"), (tick.tube(radius=0.45), INK)], labels


def person(at=(0.0, 0.0, 0.0), h=1750.0, facing=(0.0, -1.0, 0.0)):
    """[(mesh, colour)]: a plain 1.75 m mannequin standing on `at`, facing `facing` (xy)."""
    s = h / 1750.0
    f = np.asarray(facing, float)
    f /= np.linalg.norm(f)
    side = np.array([f[1], -f[0], 0.0])
    p = np.asarray(at, float)
    col = "#7f95aa"
    out = []
    for sg in (-1, 1):       # legs
        out.append(pv.Cylinder(center=p + side * sg * 95 * s + np.array([0, 0, 430 * s]), direction=(0, 0, 1), radius=62 * s,
                               height=860 * s, resolution=24))
        out.append(pv.Sphere(radius=64 * s, center=p + side * sg * 95 * s + f * 20 * s + np.array([0, 0, 40 * s])))
    out.append(pv.Cylinder(center=p + np.array([0, 0, 1150 * s]), direction=(0, 0, 1), radius=170 * s, height=580 * s, resolution=32))
    out.append(pv.Sphere(radius=170 * s, center=p + np.array([0, 0, 1440 * s])))           # shoulders
    out.append(pv.Sphere(radius=110 * s, center=p + np.array([0, 0, 1640 * s])))           # head
    for sg in (-1, 1):       # arms hanging
        c0 = p + side * sg * 215 * s + np.array([0, 0, 1430 * s])
        c1 = p + side * sg * 235 * s + f * 30 * s + np.array([0, 0, 800 * s])
        out.append(pv.Line(c0, c1).tube(radius=48 * s, n_sides=18))
    mesh = out[0].merge(out[1:])
    return [(mesh, col)]


def _fmt(mm):
    return f"{mm:.0f} mm ({mm / INCH:.1f} in.)"


def dim_line(p0, p1, off, text=None):
    """(mesh of the extension lines, dimension line and end ticks; label point; label) for the distance p0-p1, drawn
    displaced by the vector `off`."""
    p0, p1, off = (np.asarray(v, float) for v in (p0, p1, off))
    L = float(np.linalg.norm(p1 - p0))
    u = (p1 - p0) / max(L, 1e-9)
    o = off / max(np.linalg.norm(off), 1e-9)
    q0, q1 = p0 + off, p1 + off
    tk = 0.04 * max(L, 120.0)
    segs = [(p0 + o * 4.0, q0 + o * tk * 0.4), (p1 + o * 4.0, q1 + o * tk * 0.4), (q0, q1)]
    d45 = (u + o) / math.sqrt(2)
    segs += [(q0 - d45 * tk / 2, q0 + d45 * tk / 2), (q1 - d45 * tk / 2, q1 + d45 * tk / 2)]
    lines = [pv.Line(a, b) for a, b in segs]
    mesh = lines[0].merge(lines[1:])
    return mesh, (q0 + q1) / 2 + o * tk * 0.6, text or _fmt(L)


def add_dims(st, key, dims, font_size=12, color=INK):
    """dims: [(p0, p1, off, text-or-None)]; draws them on the Stage `st` under `key` (remove with remove_dims)."""
    meshes, pts, labs = [], [], []
    for p0, p1, off, text in dims:
        m, q, lab = dim_line(p0, p1, off, text)
        meshes.append(m)
        pts.append(q)
        labs.append(lab)
    mesh = meshes[0].merge(meshes[1:]) if len(meshes) > 1 else meshes[0]
    st.add(key, mesh.tube(radius=0.0035 * max(np.ptp(mesh.points, axis=0).max(), 100.0), n_sides=8), color, ambient=0.8)
    st.pl.add_point_labels(np.array(pts), labs, font_size=font_size, text_color=color, shape="rounded_rect",
                           shape_color="white", shape_opacity=0.75, show_points=False, always_visible=True, name=key + "-lab")


def remove_dims(st, key):
    st.remove(key)
    try:
        st.pl.remove_actor(key + "-lab")
    except Exception:  # noqa: BLE001
        pass


def box_dims(b, which="xyz", pad=None):
    """Dimension lines for an axis-aligned box b = (x0, x1, y0, y1, z0, z1): x along the front-bottom edge, y along the
    right-bottom edge, z up the front-left edge (so the three labels don't crowd one corner)."""
    x0, x1, y0, y1, z0, z1 = map(float, b)
    pad = pad or 0.18 * max(x1 - x0, y1 - y0, z1 - z0, 60.0)
    out = []
    if "x" in which:
        out.append(((x0, y0, z0), (x1, y0, z0), (0, -pad, 0), None))
    if "y" in which:
        out.append(((x1, y0, z0), (x1, y1, z0), (pad, 0, 0), None))
    if "z" in which:
        out.append(((x0, y0, z0), (x0, y0, z1), (-pad * 0.7, -pad * 0.7, 0), None))
    return out


def add_refs(st, key, pieces, labels=()):
    """Draw [(mesh, colour)] as one group under `key`, plus point labels."""
    st.add_multi(key, pieces)
    if labels:
        st.pl.add_point_labels(np.array([p for p, _ in labels]), [t for _, t in labels], font_size=10, text_color=INK, shape=None,
                               show_points=False, always_visible=True, name=key + "-lab")


def remove_refs(st, key):
    st.remove(key)
    try:
        st.pl.remove_actor(key + "-lab")
    except Exception:  # noqa: BLE001
        pass
