"""Scale references for the build animation (render_build.py): things everyone knows the size of, and dimension lines.

A machinist watching the first animation couldn't tell how big the chamber was ("the size and scale aren't immediately
apparent from the video"). Every chapter now puts one of these next to the work:

  soda can     a US 12 fl oz (355 mL) can: Ø66 x 122 mm (the "211" body; the "202" end is Ø54)
  steel rule   a 300 mm (12 in.) rule, 25 mm wide, ticks every 10 mm, longer every 50 and 100 mm
  person       a 1750 mm adult (ANSUR II proportions), for the tray and the kit layout
  dims         dimension lines with extension lines, end ticks and a label in mm and inches

The meshes are plain pyvista (the person's sections are interpolated with scipy's PCHIP); colours are neutral so
nothing reads as a brand.
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


def _smooth(z, zs, vals):
    """Shape-preserving cubic (PCHIP) interpolation through (zs, vals) at z: no overshoot between stations."""
    from scipy.interpolate import PchipInterpolator
    return PchipInterpolator(zs, vals)(z)


def _loft(centres, ax_u, ax_v, ra, rb, n_theta=40, cap0=True, cap1=True, p=2.0):
    """Closed tube through `centres` (k x 3) with elliptical (superelliptical, exponent p) sections of half-axes ra (along
    ax_u) and rb (along ax_v) at each station; ends closed by fans to the end centres."""
    centres = np.asarray(centres, float)
    k = len(centres)
    th = np.linspace(0, 2 * math.pi, n_theta, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    cu = np.sign(c) * np.abs(c) ** (2.0 / p)
    sv = np.sign(s) * np.abs(s) ** (2.0 / p)
    pts = []
    for i in range(k):
        u, v = np.asarray(ax_u[i], float), np.asarray(ax_v[i], float)
        ring = centres[i] + np.outer(ra[i] * cu, u) + np.outer(rb[i] * sv, v)
        pts.append(ring)
    pts = np.concatenate(pts)
    faces = []
    for i in range(k - 1):
        for j in range(n_theta):
            a, b = i * n_theta + j, i * n_theta + (j + 1) % n_theta
            faces += [4, a, b, b + n_theta, a + n_theta]
    extra = []
    if cap0:
        extra.append(centres[0])
        ic = len(pts)
        for j in range(n_theta):
            faces += [3, ic, (j + 1) % n_theta, j]
    if cap1:
        extra.append(centres[-1])
        ic = len(pts) + (1 if cap0 else 0)
        base = (k - 1) * n_theta
        for j in range(n_theta):
            faces += [3, ic, base + j, base + (j + 1) % n_theta]
    if extra:
        pts = np.concatenate([pts, np.asarray(extra)])
    return pv.PolyData(pts, faces=np.asarray(faces)).triangulate().compute_normals(auto_orient_normals=True)


def _limb(p0, p1, radii, n=24):
    """Tapered round limb from p0 to p1, radii = [(t, r)] along it (t from 0 to 1), with a rounded cap at each end."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    ax = p1 - p0
    L = np.linalg.norm(ax)
    ax /= L
    ref = np.array([0, 0, 1.0]) if abs(ax[2]) < 0.9 else np.array([1.0, 0, 0])
    u = np.cross(ax, ref)
    u /= np.linalg.norm(u)
    v = np.cross(ax, u)
    ts_, rs_ = zip(*radii)
    r0, r1 = rs_[0], rs_[-1]
    t_in = np.linspace(0, 1, n)
    r_in = _smooth(t_in, ts_, rs_)
    cap_n = 6
    stations, rads = [], []
    for a in np.linspace(0.12, math.pi / 2, cap_n, endpoint=False):         # start cap, from the tip inward
        stations.append(p0 - ax * r0 * math.cos(a))
        rads.append(r0 * math.sin(a))
    for t, r in zip(t_in, r_in):
        stations.append(p0 + ax * L * t)
        rads.append(r)
    for a in np.linspace(math.pi / 2, 0.12, cap_n + 1)[1:]:                # end cap, outward to the tip
        stations.append(p1 + ax * r1 * math.cos(a))
        rads.append(r1 * math.sin(a))
    k = len(stations)
    return _loft(stations, [u] * k, [v] * k, rads, rads, n_theta=28)


def _ellipsoid(c, r, res=32):
    """Axis-aligned ellipsoid centred on c with semi-axes r."""
    s = pv.Sphere(radius=1.0, theta_resolution=res, phi_resolution=res)
    s.points = s.points * np.asarray(r, float) + np.asarray(c, float)
    return s.compute_normals(auto_orient_normals=True)


def person(at=(0.0, 0.0, 0.0), h=1750.0, facing=(0.0, -1.0, 0.0)):
    """[(mesh, colour)]: a 1.75 m adult in a shirt and trousers, standing on `at` and facing `facing` (xy).

    Replaced the 2026-11-20 mannequin (a cylinder with a ball on top) on 2026-11-23, after "human looks weird". The body is
    lofted from superelliptical sections and tapered limbs, with heights and breadths close to the ANSUR II (2012) US Army
    male means at this stature: shoulder (acromion) 1436 mm, elbow 1100, wrist 850, crotch 836, knee 490; biacromial
    breadth ~404 (deltoids ~500), chest 350 x 245, hip 345; head 155 wide, 199 long, chin to crown 225; foot 280 long."""
    s = h / 1750.0
    # built facing -y with its left side at +x, then turned to `facing`
    parts = []

    def add(mesh, col):
        parts.append((mesh, col))

    SHIRT, TROUSERS, SHOES, SKIN, HAIR, BELT = "#5d7fa3", "#3b4350", "#25282d", "#c8a58a", "#3a2f28", "#2b2b2b"
    ux, uy, uz = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
    # ---- torso: lofted superellipses from the crotch to the base of the neck
    zs = np.array([828, 845, 875, 915, 960, 1010, 1080, 1180, 1270, 1340, 1395, 1430, 1458, 1482, 1496])
    ha = np.array([40, 105, 160, 172, 166, 156, 146, 154, 166, 174, 176, 160, 118, 78, 60])      # half-breadth (x)
    hb = np.array([40, 82, 112, 122, 117, 111, 107, 115, 123, 121, 112, 96, 80, 64, 56])         # half-depth (y)
    yc = np.array([8, 8, 12, 16, 9, 2, -2, -8, -14, -12, -6, 0, 6, 10, 10])                     # centre; + = back
    z = np.linspace(zs[0], zs[-1], 60)
    A, B, Y = _smooth(z, zs, ha), _smooth(z, zs, hb), _smooth(z, zs, yc)
    belt = 1010.0

    def tors(mask, colr):
        idx = np.where(mask)[0]
        cen = np.stack([np.zeros(len(idx)), Y[idx], z[idx]], axis=1)
        add(_loft(cen, [ux] * len(idx), [uy] * len(idx), A[idx], B[idx], n_theta=56, p=2.3), colr)

    tors(z <= belt + 9.0, TROUSERS)
    tors(z >= belt - 9.0, SHIRT)
    zb = np.array([belt - 11, belt + 11])                                                         # belt
    add(_loft(np.stack([[0, 0], _smooth(zb, zs, yc), zb], axis=1), [ux] * 2, [uy] * 2,
              _smooth(zb, zs, ha) + 3.0, _smooth(zb, zs, hb) + 3.0, n_theta=56, p=2.3), BELT)
    # ---- neck and head
    add(_limb((0, 12, 1460), (0, 8, 1590), [(0, 60), (1, 55)]), SKIN)
    head_c = np.array([0.0, -6.0, 1640.0])
    # head: lofted from the chin to the crown, the chin forward of the skull (ANSUR II: head breadth 155, length 199,
    # chin to crown ~230)
    hz = np.array([-114, -104, -84, -56, -24, 10, 42, 70, 92, 104, 111])
    hx = np.array([16, 40, 56, 65, 71, 76, 77, 72, 58, 38, 12])
    hy = np.array([22, 44, 66, 82, 92, 97, 98, 92, 76, 50, 16])
    hc = np.array([-36, -30, -20, -10, -4, 0, 2, 4, 6, 6, 6])
    zz = np.linspace(hz[0], hz[-1], 34)
    cen = np.stack([np.zeros_like(zz), _smooth(zz, hz, hc), zz], axis=1) + head_c
    add(_loft(cen, [ux] * len(zz), [uy] * len(zz), _smooth(zz, hz, hx), _smooth(zz, hz, hy), n_theta=48, p=2.1), SKIN)
    # hair: the same loft 5 mm proud, cut at a hairline that runs from the forehead down to the nape
    hz2 = np.append(hz[:-1], hz[-1] + 5.0)
    zz2 = np.linspace(hz2[0], hz2[-1], 60)
    cen2 = np.stack([np.zeros_like(zz2), _smooth(zz2, hz2, hc + np.r_[0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2]), zz2], axis=1) + head_c
    hair = _loft(cen2, [ux] * len(zz2), [uy] * len(zz2), _smooth(zz2, hz2, hx + 5.0), _smooth(zz2, hz2, hy + 5.0), n_theta=96, p=2.1)
    hair = hair.clip(normal=(0, -0.8, -1), origin=head_c + np.array([0, 0, 24]), invert=True)
    add(hair, HAIR)
    add(_ellipsoid(head_c + np.array([0, -96, -12]), (10, 14, 20)), SKIN)                       # nose
    for sg in (-1, 1):
        add(_ellipsoid(head_c + np.array([sg * 75, 8, -6]), (8, 17, 27)), SKIN)                 # ears
    # ---- shoulders, arms and hands: relaxed, slightly away from the body, elbows a little bent
    for sg in (-1, 1):
        sh = np.array([sg * 188, 6, 1386])                       # shoulder joint
        el = np.array([sg * 222, 24, 1098])                      # elbow
        wr = np.array([sg * 232, -12, 848])                      # wrist
        add(_ellipsoid(sh + np.array([-sg * 16, 0, -14]), (66, 60, 80)), SHIRT)                 # deltoid
        add(_limb(sh, el, [(0, 52), (0.35, 50), (1, 40)]), SHIRT)
        add(_limb(el, wr, [(0, 40), (0.3, 41), (0.85, 31), (1, 30)]), SHIRT)
        add(_limb(wr + np.array([0, 0, 16]), wr + np.array([0, 0, -6]), [(0, 26), (1, 26)]), SKIN)
        d = (wr - el) / np.linalg.norm(wr - el)
        add(_ellipsoid(wr + d * 86, (19, 43, 88)), SKIN)                                         # palm and fingers
        add(_ellipsoid(wr + d * 42 + np.array([-sg * 6, -34, 0]), (12, 12, 32)), SKIN)          # thumb
    # ---- legs
    for sg in (-1, 1):
        hip = np.array([sg * 86, 12, 930])
        kn = np.array([sg * 94, -2, 492])
        an = np.array([sg * 102, 16, 84])
        add(_limb(hip, kn, [(0, 84), (0.2, 82), (0.7, 67), (1, 58)]), TROUSERS)
        add(_limb(kn, an, [(0, 58), (0.28, 60), (0.62, 50), (1, 44)]), TROUSERS)
        # shoe, lofted heel to toe, flat sole on the floor, toes turned out ~6 deg
        ys = np.array([72, 62, 30, -30, -100, -160, -196, -210])
        wa = np.array([22, 38, 44, 45, 51, 49, 36, 14])
        hb_ = np.array([30, 44, 50, 46, 38, 32, 25, 12])
        tw = math.radians(6.0 * sg)
        cx = sg * 102 + (-ys) * math.sin(tw)
        cen = np.stack([cx, ys * math.cos(tw), hb_ + 1.0], axis=1)
        k = len(ys)
        ush = np.array([math.cos(tw), math.sin(tw), 0.0])
        add(_loft(cen, [ush] * k, [uz] * k, wa, hb_, n_theta=40, p=2.6), SHOES)
    # ---- turn from facing -y to `facing`, scale to h, and move to `at`
    f = np.asarray(facing, float)
    f[2] = 0.0
    f /= np.linalg.norm(f)
    ang = math.atan2(f[1], f[0]) - math.atan2(-1.0, 0.0)
    c, s_ = math.cos(ang), math.sin(ang)
    Rz = np.array([[c, -s_, 0], [s_, c, 0], [0, 0, 1.0]])
    by_col = {}
    for mesh, col in parts:                                       # one mesh per colour: 6 actors instead of ~30
        m = mesh.copy()
        m.points = (m.points * s) @ Rz.T + np.asarray(at, float)
        by_col.setdefault(col, []).append(m)
    out = []
    for col, ms in by_col.items():
        m = ms[0].append_polydata(*ms[1:]) if len(ms) > 1 else ms[0]
        out.append((m.compute_normals(auto_orient_normals=False, split_vertices=False), col))
    return out


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
