"""Data panels for SOP 03 (#262): every number comes from the repo's own analysis code
(``../analysis/density_porosity.py``) run on synthetic inputs, and every panel says so.

* ``SECTION``: a synthetic polished XZ section of a 5 mm cube (unetched, 6.25 um a pixel): round gas and keyhole
  pores, irregular lack-of-fusion pores along the track boundaries, and a few hot cracks along the build direction.
* panel builders return f(u) -> RGBA image for ``SOPScene.panel``.
"""
from __future__ import annotations

import functools
import io
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))
import density_porosity as dp  # noqa: E402

# the reference palette (dataviz skill): three categorical slots, text inks, surface
BLUE, ORANGE, AQUA = "#257de0", "#f47230", "#00b894"
INK, INK2, SURF, GRID = "#191919", "#666666", "#ffffff", "#e3e3e3"
SYN = "synthetic example"

# the SOP's own example (its bash block)
M_AIR, M_WET, T_W, RHO_REF = 0.33412, 0.20915, 21.4, 2.668
AIR3 = (0.33412, 0.33413, 0.33411)       # three weighings in air (g), synthetic
WET3 = (0.20915, 0.20917, 0.20914)       # three immersed (g), synthetic
REF_6063 = 2.70                          # wrought 6063, handbook density (g/cm3)


def _img(fig, dpi=150) -> Image.Image:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


def _fig(w=4.2, h=3.0):
    fig = plt.figure(figsize=(w, h))
    fig.patch.set_facecolor(SURF)
    fig.patch.set_alpha(0.94)
    return fig


def _badge(fig, text=SYN, y=0.015):
    fig.text(0.985, y, text, ha="right", va="bottom", fontsize=7.5, color=INK2, style="italic",
             bbox=dict(boxstyle="round,pad=0.25", fc="#f4f4f4", ec="#c8c8c8", lw=0.6))


def _title(fig, t, sub=None):
    fig.text(0.03, 0.965, t, ha="left", va="top", fontsize=10.5, color=INK, weight="bold")
    if sub:
        fig.text(0.03, 0.885, sub, ha="left", va="top", fontsize=8, color=INK2)


def _axes_style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9a9a9a")
        ax.spines[s].set_linewidth(0.7)
    ax.tick_params(colors=INK2, labelsize=7.5, width=0.6)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


# ============================================================================================ Archimedes panels
def archimedes_result() -> dict:
    return dp.archimedes(M_AIR, M_WET, T_W, RHO_REF)


def plate_map(u=0.0) -> Image.Image:
    import models_density as MD
    fig = _fig(3.4, 3.2)
    _title(fig, "Cubes by plate position", "170 mm plate, 4 x 5 cubes of 5 mm")
    ax = fig.add_axes([0.06, 0.04, 0.88, 0.78])
    ax.add_patch(plt.Circle((0, 0), 85, fc="#ededed", ec="#9a9a9a", lw=0.8))
    for lab, x, y in MD.plate_positions():
        ax.add_patch(plt.Rectangle((x - 2.5, y - 2.5), 5, 5, fc="#8a8c90", ec=INK, lw=0.5))
        ax.text(x, y - 6.5, lab, ha="center", va="top", fontsize=7, color=INK)
    ax.set_xlim(-90, 90)
    ax.set_ylim(-90, 90)
    ax.set_aspect("equal")
    ax.axis("off")
    return _img(fig)


def readings(u=1.0) -> Image.Image:
    """The six weighings, revealed with u (0 -> 1), their means and spreads."""
    fig = _fig(3.6, 2.7)
    _title(fig, "Weighings of cube A1 (g)", "XPR225DR, fine range, 0.01 mg")
    n = int(round(u * 6))
    rows = [("in air", AIR3), ("in water", WET3)]
    y = 0.70
    k = 0
    for name, vals in rows:
        fig.text(0.05, y, name, fontsize=8.5, color=INK2, va="center")
        for i, v in enumerate(vals):
            shown = k < n
            fig.text(0.30 + 0.21 * i, y, f"{v:.5f}" if shown else "-", fontsize=9, color=INK, va="center",
                     family="DejaVu Sans Mono")
            k += 1
        y -= 0.15
    if n >= 6:
        ma, mw = np.mean(AIR3), np.mean(WET3)
        rho = [dp.archimedes(a, w, T_W)["rho_g_cm3"] for a, w in zip(AIR3, WET3)]
        spread = (max(rho) - min(rho)) / np.mean(rho) * 100
        fig.text(0.05, 0.34, f"means  {ma:.5f}   {mw:.5f}", fontsize=8.5, color=INK, family="DejaVu Sans Mono")
        fig.text(0.05, 0.22, f"repeat densities agree within {spread:.3f} %", fontsize=8.5, color=INK)
        fig.text(0.05, 0.12, "(acceptance: within 0.05 %)", fontsize=7.5, color=INK2)
    _badge(fig)
    return _img(fig)


def result_panel(u=1.0) -> Image.Image:
    r = archimedes_result()
    fig = _fig(4.0, 2.75)
    _title(fig, "density_porosity.py archimedes")
    fig.text(0.04, 0.82, f"--m-air {M_AIR} --m-wet {M_WET} --T-water {T_W} --rho-ref {RHO_REF}", fontsize=7.2,
             color=INK2, family="DejaVu Sans Mono")
    lines = [("water at 21.4 C", f"{r['rho_water_g_cm3']:.5f} g/cm3"),
             ("density", f"{r['rho_g_cm3']:.4f} +- {r['u_rho_g_cm3']:.4f} g/cm3"),
             ("relative density", f"{100 * r['relative_density']:.2f} +- {100 * r['u_relative_density']:.2f} %"),
             ("porosity", f"{100 * r['porosity']:.2f} %")]
    y = 0.66
    for a, b in lines:
        fig.text(0.05, y, a, fontsize=8.5, color=INK2)
        fig.text(0.47, y, b, fontsize=9, color=INK, family="DejaVu Sans Mono")
        y -= 0.12
    fig.text(0.05, 0.13, "+- with the script's default 0.2 mg per weighing", fontsize=7, color=INK2)
    _badge(fig, "computed from the SOP's example numbers")
    return _img(fig)


def uncertainty_panel(u=1.0) -> Image.Image:
    """u(relative density) against cube edge, for 0.1 mg and 0.01 mg readings (density_porosity.archimedes)."""
    edges = np.linspace(3, 12, 37)
    rw = dp.water_density(T_W)
    fig = _fig(3.9, 2.9)
    _title(fig, "Uncertainty of relative density", "Al cube at 99.9 %, from density_porosity.archimedes")
    ax = fig.add_axes([0.17, 0.18, 0.78, 0.60])
    _axes_style(ax)
    for um, col, lab in ((1e-4, BLUE, "0.1 mg readings"), (1e-5, ORANGE, "0.01 mg readings")):
        us = []
        for e in edges:
            V = (e / 10.0) ** 3
            M = RHO_REF * 0.999 * V
            r = dp.archimedes(M - dp.RHO_AIR * V, M - rw * V, T_W, RHO_REF, u_mass=um, u_T=0.05)
            us.append(100 * r["u_relative_density"])
        ax.plot(edges, us, color=col, lw=2)
        ax.text(edges[-1] + 0.15, us[-1], lab, color=INK, fontsize=7, va="center")
    ax.axhline(0.5, color="#9a9a9a", lw=1.0, ls=(0, (4, 3)))
    ax.text(3.1, 0.56, "0.5 % porosity", fontsize=7, color=INK2)
    ax.axvline(5, color="#9a9a9a", lw=0.8)
    ax.text(5.15, 0.0013, "5 mm", fontsize=7, color=INK2)
    ax.set_yscale("log")
    ax.set_ylim(0.001, 1.5)
    ax.set_xlim(3, 15.2)
    ax.set_xticks([3, 5, 7, 10, 12])
    ax.set_xlabel("cube edge (mm)", fontsize=8, color=INK2)
    ax.set_ylabel("+- relative density (%)", fontsize=8, color=INK2)
    _badge(fig, "computed")
    return _img(fig)


def refdens_panel(u=1.0) -> Image.Image:
    fig = _fig(3.9, 2.4)
    _title(fig, "Reference density rho_ref")
    rows = [("best", "He pycnometer, same powder", "2.668 g/cm3"),
            ("otherwise", "Thermo-Calc at 20 C, measured", "composition (SOP 05)"),
            ("report", "which one you used", "")]
    y = 0.72
    for a, b, c in rows:
        fig.text(0.05, y, a, fontsize=8.5, color=INK2, va="top")
        fig.text(0.30, y, b, fontsize=8.5, color=INK, va="top")
        if c:
            fig.text(0.30, y - 0.10, c, fontsize=8.5, color=INK, va="top", family="DejaVu Sans Mono")
        y -= 0.23
    _badge(fig)
    return _img(fig)


def acceptance_panel(u=1.0) -> Image.Image:
    V, rho6063 = 0.125, 2.6985          # a 5 mm 6063 reference cube, synthetic: 2.6985 g/cm3
    M = rho6063 * V
    ma, mw = round(M - dp.RHO_AIR * V, 5), round(M - dp.water_density(T_W) * V, 5)
    r = dp.archimedes(ma, mw, T_W, REF_6063, u_mass=1e-5)
    rho = [dp.archimedes(a, w, T_W)["rho_g_cm3"] for a, w in zip(AIR3, WET3)]
    spread = (max(rho) - min(rho)) / np.mean(rho) * 100
    fig = _fig(3.9, 2.4)
    _title(fig, "Acceptance")
    lines = [(f"6063 reference: {100 * r['relative_density']:.2f} % of 2.70", "needs >= 99.9 %", "pass"),
             (f"repeat densities: within {spread:.3f} %", "needs within 0.05 %", "pass")]
    y = 0.70
    for a, b, c in lines:
        fig.text(0.05, y, a, fontsize=8.5, color=INK, va="top")
        fig.text(0.05, y - 0.11, b, fontsize=7.5, color=INK2, va="top")
        fig.text(0.95, y, c, fontsize=8.5, color=INK, va="top", ha="right", weight="bold")
        y -= 0.30
    _badge(fig)
    return _img(fig)


# ============================================================================================ the synthetic section
PX_UM = 6.25          # um per pixel: 800 px = 5 mm
N = 800


@functools.lru_cache(maxsize=1)
def section() -> dict:
    """A synthetic unetched XZ section (build direction up the image) with its true features."""
    import cv2
    rng = np.random.default_rng(262)
    img = rng.normal(196, 5.0, (N, N))
    yy, xx = np.mgrid[:N, :N]
    img += 6.0 * np.sin(xx / 170.0) * np.cos(yy / 230.0)           # a little polishing relief
    feats = []
    mask = np.zeros((N, N), np.uint8)
    # gas pores: small, round, anywhere
    for _ in range(18):
        cx, cy, r = rng.uniform(30, N - 30), rng.uniform(30, N - 30), rng.uniform(1.5, 3.0)
        cv2.circle(mask, (int(cx), int(cy)), int(round(r)), 1, -1)
        feats.append(("gas", cx, cy))
    # keyhole pores: larger, round, at the melt-pool bottoms
    for _ in range(2):
        cx, cy, r = rng.uniform(80, N - 80), rng.uniform(80, N - 80), rng.uniform(5.5, 7)
        cv2.circle(mask, (int(cx), int(cy)), int(round(r)), 1, -1)
        feats.append(("keyhole", cx, cy))
    # lack of fusion: irregular, flat, along the layer (track) boundaries, which run across the image
    for k in range(3):
        cy = 160 + 220 * k + rng.uniform(-20, 20)
        cx = rng.uniform(120, N - 120)
        L = rng.uniform(26, 40)
        pts = []
        for t in np.linspace(0, 2 * np.pi, 22, endpoint=False):
            rr = (0.5 + 0.5 * rng.uniform(0.3, 1.0))
            pts.append((cx + L / 2 * math.cos(t) * rr, cy + 4.5 * math.sin(t) * rr * rng.uniform(0.5, 1.4)))
        cv2.fillPoly(mask, [np.array(pts, np.int32)], 1)
        feats.append(("lof", cx, cy))
    # hot cracks: thin, wavy, along the build direction (vertical), between columnar grains
    cracks = []
    for k in range(4):
        x0, y0 = rng.uniform(80, N - 80), rng.uniform(120, N - 200)
        L = rng.uniform(35, 70)
        pts = [(x0 + 3.0 * math.sin(s / 9.0 + k), y0 + s) for s in np.linspace(0, L, 14)]
        cv2.polylines(mask, [np.array(pts, np.int32)], False, 1, 1)
        cracks.append(pts)
        feats.append(("crack", x0, y0 + L / 2))
    img[mask > 0] = rng.normal(48, 8, int(mask.sum()))
    img = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 0.8)
    return dict(img=np.clip(img, 0, 255).astype(np.uint8), mask=mask, feats=feats, cracks=cracks)


@functools.lru_cache(maxsize=1)
def analysis() -> dict:
    """density_porosity.image_porosity (Otsu) on the section, then each pore's circularity and shape, as in Fiji."""
    import cv2
    s = section()
    ip = dp.image_porosity(s["img"])
    pores = (s["img"] < ip["threshold"]).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(pores, 8)
    classes = np.zeros(n, int)                     # 0 bg/noise, 1 round (gas/keyhole), 2 lack of fusion, 3 crack
    crack_len = 0.0
    out = []
    for i in range(1, n):
        a = stats[i, cv2.CC_STAT_AREA]
        if a < 6:
            continue
        m = (lab == i).astype(np.uint8)
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        P = cv2.arcLength(cs[0], True)
        C = 4 * math.pi * a / max(P * P, 1e-9)
        (cx, cy), (w, h), ang = cv2.minAreaRect(cs[0])
        L, Wd = max(w, h), max(min(w, h), 1.0)
        vertical = (h >= w and abs(ang) < 30) or (w > h and abs(abs(ang) - 90) < 30)
        if L / Wd > 5 and vertical:
            k = 3
            crack_len += L
        elif C > 0.8:
            k = 1
        else:
            k = 2
        classes[i] = k
        out.append(dict(k=k, C=C, area=int(a), L=L))
    area_mm2 = (N * PX_UM / 1000) ** 2
    pf = ip["pore_area_fraction"]
    # its sampling uncertainty: the spread of the 3 x 3 tiles' fractions
    t = N // 3
    fr = [pores[i * t:(i + 1) * t, j * t:(j + 1) * t].mean() for i in range(3) for j in range(3)]
    u_pf = float(np.std(fr, ddof=1) / math.sqrt(len(fr)))
    return dict(threshold=ip["threshold"], fraction=pf, u_fraction=u_pf, labels=lab, classes=classes, pores=pores,
                n_round=sum(o["k"] == 1 for o in out), n_lof=sum(o["k"] == 2 for o in out),
                n_crack=sum(o["k"] == 3 for o in out),
                crack_mm_per_mm2=crack_len * PX_UM / 1000 / area_mm2, area_mm2=area_mm2)


def _grey(ax, img, crop=None):
    ax.imshow(img if crop is None else img[crop[1]:crop[3], crop[0]:crop[2]], cmap="gray", vmin=0, vmax=255,
              interpolation="lanczos")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#9a9a9a")
        sp.set_linewidth(0.6)


def tiles_panel(u=1.0) -> Image.Image:
    """The stitched face, tile by tile in a serpentine (3 x 3 tiles at 100x, 20 % overlap)."""
    s = section()
    fig = _fig(3.5, 3.6)
    _title(fig, "Stitched at 100x: 3 x 3 tiles", "the whole 5 x 5 mm XZ face, tiles overlapping")
    ax = fig.add_axes([0.08, 0.10, 0.84, 0.72])
    order = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
    k = int(math.floor(u * 9 + 1e-6))
    shown = np.full((N, N), 246, np.uint8)
    t = N / 3
    for (r, c) in order[:k]:
        y0, x0 = int(r * t), int(c * t)
        shown[y0:int(y0 + t), x0:int(x0 + t)] = s["img"][y0:int(y0 + t), x0:int(x0 + t)]
    _grey(ax, shown)
    for i, (r, c) in enumerate(order):
        ax.add_patch(plt.Rectangle((c * t, r * t), t, t, fill=False, ec=BLUE if i < k else "#bdbdbd",
                                   lw=0.9 if i < k else 0.5))
    if 0 < k < 9:
        r, c = order[k - 1]
        ax.add_patch(plt.Rectangle((c * t, r * t), t, t, fill=False, ec=ORANGE, lw=1.6))
    ax.annotate("", xy=(-30, 80), xytext=(-30, 330), arrowprops=dict(arrowstyle="->", color=INK2, lw=0.8),
                annotation_clip=False)
    ax.text(-48, 205, "build (Z)", rotation=90, fontsize=6.5, color=INK2, va="center", ha="center")
    _badge(fig)
    return _img(fig)


def otsu_panel(u=1.0) -> Image.Image:
    s, a = section(), analysis()
    fig = _fig(4.0, 3.2)
    _title(fig, "Porosity by Otsu threshold", "density_porosity.py image section.png")
    ax = fig.add_axes([0.04, 0.10, 0.50, 0.66])
    crop = (180, 260, 500, 580)
    _grey(ax, s["img"], crop)
    ov = np.zeros((crop[3] - crop[1], crop[2] - crop[0], 4))
    pm = a["pores"][crop[1]:crop[3], crop[0]:crop[2]] > 0
    ov[pm] = (0.15, 0.49, 0.88, 0.85 * u)
    ax.imshow(ov, interpolation="nearest")
    ax.text(4, 312, "2 x 2 mm of the face", fontsize=6, color="white", va="bottom")
    hx = fig.add_axes([0.62, 0.50, 0.34, 0.24])
    _axes_style(hx)
    hx.hist(s["img"].ravel(), bins=64, range=(0, 255), color="#8a8c90", log=True)
    hx.axvline(a["threshold"], color=ORANGE, lw=1.6)
    hx.set_yticks([])
    hx.set_xticks([0, 128, 255])
    hx.text(a["threshold"] + 4, hx.get_ylim()[1] * 0.3, "Otsu", fontsize=7, color=INK)
    fig.text(0.60, 0.33, f"pore area {100 * a['fraction']:.2f} %", fontsize=9, color=INK)
    fig.text(0.60, 0.21, "Delesse: area fraction", fontsize=7.5, color=INK2)
    fig.text(0.60, 0.14, "= volume fraction", fontsize=7.5, color=INK2)
    _badge(fig)
    return _img(fig)


def classes_panel(u=1.0) -> Image.Image:
    s, a = section(), analysis()
    fig = _fig(4.0, 3.2)
    _title(fig, "Pore type by circularity 4piA/P^2", "Fiji: round > 0.8 gas or keyhole; irregular = lack of fusion")
    ax = fig.add_axes([0.04, 0.10, 0.56, 0.68])
    _grey(ax, s["img"])
    cols = {1: (0.15, 0.49, 0.88), 2: (0.96, 0.45, 0.19), 3: (0.0, 0.72, 0.58)}
    ov = np.zeros((N, N, 4))
    lab, cl = a["labels"], a["classes"]
    for k, c in cols.items():
        if k == 3 and u < 0.5:
            continue
        m = np.isin(lab, np.nonzero(cl == k)[0]) & (lab > 0)
        import cv2
        m = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        ov[m] = (*c, 0.95)
    ax.imshow(ov, interpolation="nearest")
    y = 0.70
    for k, name, n in ((1, "round: gas / keyhole", a["n_round"]), (2, "irregular: lack of fusion", a["n_lof"]),
                       (3, "crack (build direction)", a["n_crack"])):
        if k == 3 and u < 0.5:
            continue
        fig.patches.append(plt.Rectangle((0.63, y - 0.012), 0.03, 0.035, transform=fig.transFigure,
                                         fc=cols[k], ec="none"))
        fig.text(0.68, y, f"{name}", fontsize=7.2, color=INK, va="bottom")
        fig.text(0.68, y - 0.06, f"n = {n}", fontsize=7.2, color=INK2, va="bottom")
        y -= 0.17
    _badge(fig)
    return _img(fig)


def cracks_panel(u=1.0) -> Image.Image:
    s, a = section(), analysis()
    fig = _fig(4.0, 3.2)
    _title(fig, "Crack density", "traced lengths along the build direction, per area")
    ax = fig.add_axes([0.04, 0.10, 0.56, 0.68])
    _grey(ax, s["img"])
    for pts in s["cracks"]:
        p = np.array(pts)
        m = max(2, int(round(len(p) * u)))
        ax.plot(p[:m, 0], p[:m, 1], color=AQUA, lw=1.8)
    fig.text(0.63, 0.66, f"{a['n_crack']} cracks", fontsize=8.5, color=INK)
    fig.text(0.63, 0.55, f"{a['crack_mm_per_mm2']:.3f} mm/mm2", fontsize=9, color=INK, family="DejaVu Sans Mono")
    fig.text(0.63, 0.44, f"over {a['area_mm2']:.0f} mm2", fontsize=7.5, color=INK2)
    fig.text(0.63, 0.30, "flat pores along layers", fontsize=7.2, color=INK2)
    fig.text(0.63, 0.23, "are not counted", fontsize=7.2, color=INK2)
    _badge(fig)
    return _img(fig)


def agreement_panel(u=1.0) -> Image.Image:
    r, a = archimedes_result(), analysis()
    fig = _fig(3.9, 2.8)
    _title(fig, "Archimedes vs image porosity", "agree within their uncertainties?")
    ax = fig.add_axes([0.40, 0.30, 0.52, 0.46])
    _axes_style(ax)
    vals = [(100 * r["porosity"], 100 * r["u_relative_density"], "Archimedes", BLUE),
            (100 * a["fraction"], 100 * a["u_fraction"], "section image", ORANGE)]
    for i, (v, e, name, col) in enumerate(vals):
        ax.errorbar([v], [i], xerr=[e], fmt="o", color=col, ms=6, capsize=3, lw=1.6)
        fig.text(0.04, 0.40 + 0.22 * i, name, fontsize=8, color=INK)
        fig.text(0.04, 0.34 + 0.22 * i, f"{v:.2f} +- {e:.2f} %", fontsize=7.5, color=INK2, family="DejaVu Sans Mono")
    ax.set_yticks([])
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlim(-0.2, 0.6)
    ax.set_xlabel("porosity (%)", fontsize=8, color=INK2)
    lo = max(v - e for v, e, _, _ in vals)
    hi = min(v + e for v, e, _, _ in vals)
    fig.text(0.04, 0.10, "overlap: they agree" if lo <= hi else "no overlap: look for open pores or bubbles",
             fontsize=7.5, color=INK)
    _badge(fig)
    return _img(fig)


def open_pore_panel(u=1.0) -> Image.Image:
    """Schematic: a surface-connected pore fills with water during the immersed weighing."""
    fig = _fig(3.9, 2.8)
    _title(fig, "Open surface porosity", "water fills it, so Archimedes reads high")
    ax = fig.add_axes([0.05, 0.06, 0.55, 0.74])
    ax.add_patch(plt.Rectangle((0, 0), 10, 10, fc="#c9cacd", ec=INK2, lw=0.8))
    ax.add_patch(plt.Rectangle((-2, -2), 14, 14, fc=(0.64, 0.80, 0.92, 0.35), ec="none", zorder=0))
    pore = np.array([[10.01, 6.2], [8.4, 6.6], [7.2, 5.6], [6.4, 6.1], [6.8, 4.6], [8.0, 4.2], [10.01, 4.8]])
    ax.add_patch(plt.Polygon(pore, fc="white", ec=INK2, lw=0.7))
    k = max(0.0, min(1.0, u))
    if k > 0:
        fill = pore.copy()
        fill[:, 0] = 10.01 - (10.01 - fill[:, 0]) * k
        ax.add_patch(plt.Polygon(fill, fc=(0.37, 0.62, 0.85, 0.9), ec="none"))
    ax.add_patch(plt.Circle((4, 3.2), 0.6, fc="white", ec=INK2, lw=0.7))
    ax.text(4, 2.2, "closed pore", fontsize=6.5, ha="center", color=INK2)
    ax.text(8.3, 7.1, "open pore", fontsize=6.5, ha="center", color=INK2)
    ax.set_xlim(-2, 12)
    ax.set_ylim(-2, 12)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.text(0.62, 0.62, "If sections show", fontsize=7.5, color=INK)
    fig.text(0.62, 0.55, "surface-connected pores:", fontsize=7.5, color=INK)
    fig.text(0.62, 0.42, "coat the cube, or", fontsize=8, color=INK)
    fig.text(0.62, 0.35, "oil-impregnate it", fontsize=8, color=INK)
    fig.text(0.62, 0.28, "(ASTM B962)", fontsize=7, color=INK2)
    _badge(fig, "schematic")
    return _img(fig)


def printability_panel(u=1.0) -> Image.Image:
    """A synthetic printability map: power vs speed, the boundaries each SOP sets."""
    fig = _fig(4.2, 3.3)
    _title(fig, "Printability map", "tracks (SOP 02) + cubes (SOP 03)")
    ax = fig.add_axes([0.14, 0.15, 0.62, 0.66])
    _axes_style(ax)
    v = np.linspace(200, 2000, 200)
    # lack of fusion below a line energy, keyhole above P/sqrt(v), balling above a speed at low power
    p_lof = 0.11 * v + 60
    p_kh = 9.5 * np.sqrt(v)
    ax.fill_between(v, 0, np.minimum(p_lof, 500), color="#d9d9d9", lw=0)
    ax.fill_between(v, np.maximum(p_kh, 0), 500, color="#ececec", lw=0)
    ax.plot(v, p_lof, color=ORANGE, lw=2)
    ax.plot(v, p_kh, color=BLUE, lw=2)
    ax.axvline(1500, color=AQUA, lw=2)
    ax.text(900, 95, "lack of fusion (cubes)", fontsize=7, color=INK)
    ax.text(260, 430, "keyhole (tracks)", fontsize=7, color=INK)
    ax.text(1530, 300, "balling\n(tracks)", fontsize=7, color=INK)
    rng = np.random.default_rng(5)
    pts_v = rng.uniform(400, 1700, 14)
    pts_p = rng.uniform(150, 420, 14)
    crack = rng.uniform(0, 1.2, 14)
    sc = ax.scatter(pts_v, pts_p, s=12 + 50 * crack, fc="white", ec=INK, lw=0.8, zorder=3)
    ax.set_xlim(200, 2000)
    ax.set_ylim(50, 500)
    ax.set_xlabel("scan speed (mm/s)", fontsize=8, color=INK2)
    ax.set_ylabel("laser power (W)", fontsize=8, color=INK2)
    fig.text(0.78, 0.62, "cubes:", fontsize=7.5, color=INK)
    fig.text(0.78, 0.55, "marker size =", fontsize=7, color=INK2)
    fig.text(0.78, 0.49, "crack density", fontsize=7, color=INK2)
    fig.text(0.78, 0.42, "(hot-cracking", fontsize=7, color=INK2)
    fig.text(0.78, 0.36, "axis)", fontsize=7, color=INK2)
    _badge(fig)
    return _img(fig)


if __name__ == "__main__":
    out = Path("/tmp/sop03/panels")
    out.mkdir(parents=True, exist_ok=True)
    a = analysis()
    print({k: v for k, v in a.items() if k not in ("labels", "classes", "pores")})
    print(archimedes_result())
    for name, f in [("plate", plate_map), ("readings", readings), ("result", result_panel), ("unc", uncertainty_panel),
                    ("ref", refdens_panel), ("acc", acceptance_panel), ("tiles", lambda u: tiles_panel(0.6)),
                    ("otsu", otsu_panel), ("classes", classes_panel), ("cracks", cracks_panel),
                    ("agree", agreement_panel), ("open", lambda u: open_pore_panel(0.7)),
                    ("print", printability_panel)]:
        f(1.0).save(out / f"{name}.png")
    print("ok")
