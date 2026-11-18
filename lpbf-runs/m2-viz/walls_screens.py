"""Monitor screens for the wall-build animation (walls.py): what the SEM sections of the walls show and how they are
analysed. 1600 x 1000 px each (the monitor's 560 x 350 aspect).

Only the map uses real numbers: the 61 settings from ../m2-track-design/out/wall_sheet.csv, with that sheet's
Eagar-Tsai + overlap first guess of each wall's regime at 30 um layers. Every pore, melt pool and porosity value on
these screens is drawn by hand to show what will be measured, and each screen says so.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402,F401
import numpy as np  # noqa: E402
from matplotlib.patches import Ellipse, Polygon, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
SHEET = HERE.parent / "m2-track-design" / "out" / "wall_sheet.csv"
SIZE_IN = (16, 10)
SURFACE = "#fcfcfb"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"
LOF, DENSE, KEY = "#eb6834", "#1baf7a", "#6250d6"     # validated categorical slots (orange, aqua, violet)
NOTE = "Illustration: pores and pools drawn by hand to show what is measured; not data or predictions"

WALL_T, WALL_H, BASE_H = 1.27, 7.62, 2.54           # mm (base height assumed from Carl's 0.4 in overall)
CORE_IN, CORE_END = 0.2, 1.0                         # porosity band: >= 0.2 mm from the faces, 1 mm from base and top


def rows() -> list[dict]:
    with SHEET.open() as f:
        return list(csv.DictReader(f))


def _fig(title):
    fig = plt.figure(figsize=SIZE_IN, dpi=100, facecolor=SURFACE)
    fig.text(0.03, 0.955, title, fontsize=30, fontweight="bold", color=INK, va="top")
    return fig


def _note(fig, text=NOTE):
    fig.text(0.03, 0.025, text, fontsize=17, color=INK2, style="italic")


def _bse_background(ax, rng, w, h, x0=0.0, y0=0.0, grey=0.62):
    n = 260
    img = grey + 0.035 * rng.standard_normal((n, max(8, int(n * w / h))))
    ax.imshow(np.clip(img, 0, 1), cmap="gray", vmin=0, vmax=1, extent=(x0, x0 + w, y0, y0 + h),
              interpolation="bilinear", zorder=0)


def _lof_pore(ax, rng, x, y, s, color="#151515"):
    """An irregular, flat lack-of-fusion pore along a layer."""
    k = 9
    ang = np.linspace(0, 2 * math.pi, k, endpoint=False)
    r = s * (0.55 + 0.45 * rng.random(k))
    pts = np.c_[x + 2.6 * r * np.cos(ang), y + 0.75 * r * np.sin(ang)]
    ax.add_patch(Polygon(pts, closed=True, color=color, lw=0, zorder=3))


def _round_pore(ax, x, y, d, color="#151515"):
    ax.add_patch(Ellipse((x, y), d, d, color=color, lw=0, zorder=3))


def _pores(kind, rng):
    """Positions (mm, wall coordinates: x across the thickness 0..1.27, y up from the base top) and sizes."""
    if kind == "lof":
        n = 46
        return [("lof", rng.uniform(0.08, WALL_T - 0.08), rng.uniform(0.15, WALL_H - 0.1), rng.uniform(0.012, 0.03))
                for _ in range(n)]
    if kind == "key":
        n = 9
        return [("round", rng.uniform(0.3, WALL_T - 0.3), rng.uniform(0.4, WALL_H - 0.4), rng.uniform(0.04, 0.08))
                for _ in range(n)]
    n = 4
    return [("round", rng.uniform(0.2, WALL_T - 0.2), rng.uniform(0.3, WALL_H - 0.3), rng.uniform(0.008, 0.02))
            for _ in range(n)]


def _wall(ax, rng, kind, title, sub, segment=False):
    _bse_background(ax, rng, WALL_T + 0.7, 0.8, x0=-0.35, y0=-0.8)       # the base, running on both sides
    _bse_background(ax, rng, WALL_T, WALL_H, y0=0.0)                     # the wall
    for k, x, y, s in _pores(kind, rng):
        in_core = CORE_IN <= x <= WALL_T - CORE_IN and CORE_END <= y <= WALL_H - CORE_END
        c = "#151515"
        if segment and in_core:
            c = LOF if k == "lof" else KEY
        elif segment:
            c = "#9a9994"
        (_lof_pore(ax, rng, x, y, s, c) if k == "lof" else _round_pore(ax, x, y, s, c))
    ax.add_patch(Rectangle((CORE_IN, CORE_END), WALL_T - 2 * CORE_IN, WALL_H - 2 * CORE_END, fill=False,
                           ls=(0, (4, 3)), lw=2.2, ec="#2a78d6", zorder=4))
    ax.set_xlim(-0.35, WALL_T + 0.35)
    ax.set_ylim(-0.8, WALL_H + 0.25)
    ax.set_aspect("equal")
    ax.axis("off")
    name, setting = title.split(": ")
    ax.text(WALL_T / 2, WALL_H + 1.05, name, ha="center", va="bottom", fontsize=21, color=INK, fontweight="bold")
    ax.text(WALL_T / 2, WALL_H + 0.45, setting, ha="center", va="bottom", fontsize=17, color=INK2)
    ax.text(WALL_T / 2, -1.0, sub, ha="center", va="top", fontsize=17, color=INK2)


def bse(path: Path, segment=False):
    rng = np.random.default_rng(4)
    fig = _fig("BSE, unetched: porosity first" if not segment else "Segment pores in each wall's core band")
    specs = [("lof", "W014: 196 W, 1460 mm/s", "P/v 0.13 J/mm"),
             ("ok", "control: 370 W, 1350 mm/s", "P/v 0.27 J/mm"),
             ("key", "W005: 239 W, 455 mm/s", "P/v 0.53 J/mm")]
    for i, (kind, t, s) in enumerate(specs):
        ax = fig.add_axes([0.04 + i * 0.205, 0.13, 0.19, 0.66])
        _wall(ax, rng, kind, t, s, segment)
    ax = fig.add_axes([0.66, 0.10, 0.32, 0.76])
    ax.axis("off")
    if not segment:
        lines = [("Each wall's section", INK, 22, "bold"),
                 ("1.27 mm thick, 7.6 mm tall,", INK2, 19, None),
                 ("at the wall's mid-length", INK2, 19, None),
                 ("", INK, 10, None),
                 ("Dashed: the core band", "#2a78d6", 20, "bold"),
                 ("0.2 mm in from each face", INK2, 19, None),
                 ("1 mm from the base and the top", INK2, 19, None),
                 ("(contour pores stay outside it)", INK2, 19, None),
                 ("", INK, 10, None),
                 ("Image before etching:", INK, 20, "bold"),
                 ("etch pits look like pores", INK2, 19, None),
                 ("", INK, 10, None),
                 ("About 6 fields a wall at ~100x;", INK2, 19, None),
                 ("504 fields for 84 walls", INK2, 19, None)]
    else:
        lines = [("Classify by shape", INK, 22, "bold"),
                 ("irregular, flat, along layers:", INK2, 19, None),
                 ("   lack of fusion", LOF, 20, "bold"),
                 ("round, larger than gas pores:", INK2, 19, None),
                 ("   keyhole", KEY, 20, "bold"),
                 ("grey: outside the band, not counted", INK2, 19, None),
                 ("", INK, 10, None),
                 ("Per wall:", INK, 20, "bold"),
                 ("area fraction in the band,", INK2, 19, None),
                 ("pore count and size by class,", INK2, 19, None),
                 ("wall thickness at mid-height", INK2, 19, None),
                 ("", INK, 10, None),
                 ("Same threshold for every image;", INK2, 19, None),
                 ("smallest pore counted: ~5 px", INK2, 19, None)]
    y = 0.97
    for text, c, fs, fw in lines:
        ax.text(0.02, y, text, color=c, fontsize=fs, fontweight=fw or "normal", va="top", transform=ax.transAxes)
        y -= 0.068 if fs > 12 else 0.03
    _note(fig)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def etched(path: Path):
    rng = np.random.default_rng(7)
    fig = _fig("Etched: the last layer's melt pools at the top of each wall")
    titles = ["If the hatch runs along the wall", "If it runs across the wall"]
    for i in range(2):
        ax = fig.add_axes([0.04 + i * 0.36, 0.13, 0.33, 0.70])
        top, w = 0.0, WALL_T
        _bse_background(ax, rng, w, 0.32, y0=-0.32, grey=0.70)
        ax.add_patch(Rectangle((-0.2, top), w + 0.4, 0.12, color=SURFACE, zorder=1))
        d = 0.075
        if i == 0:
            xs = np.arange(0.11 + 0.045, w - 0.11, 0.09)
            for x in xs:                                    # overlapping arcs: one per hatch line in the top layer
                t = np.linspace(-1, 1, 60)
                ax.plot(x + 0.065 * t, top - d * np.sqrt(1 - t ** 2), color="#3b3a37", lw=1.6, zorder=3)
            for x in (0.05, w - 0.05):                       # contour pools at the faces: narrower and deeper
                t = np.linspace(-1, 1, 60)
                ax.plot(x + 0.04 * t, top - 0.13 * np.sqrt(1 - t ** 2), color="#3b3a37", lw=1.6, zorder=3)
            xm = xs[len(xs) // 2]
            ax.annotate("", xy=(xm, top - d), xytext=(xm, top), zorder=5,
                        arrowprops=dict(arrowstyle="<->", color="#2a78d6", lw=2.4))
            ax.text(xm, top - d - 0.03, "depth", color="#2a78d6", fontsize=19, ha="center", va="top", zorder=5)
        else:
            x = np.linspace(0.11, w - 0.11, 80)
            ax.plot(x, top - d + 0.006 * np.sin(x * 60), color="#3b3a37", lw=1.6, zorder=3)
            ax.annotate("", xy=(w / 2, top - d), xytext=(w / 2, top), zorder=5,
                        arrowprops=dict(arrowstyle="<->", color="#2a78d6", lw=2.4))
            ax.text(w / 2, top - d - 0.03, "depth only", color="#2a78d6", fontsize=19, ha="center", va="top", zorder=5)
        ax.set_xlim(-0.05, w + 0.05)
        ax.set_ylim(-0.32, 0.06)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(titles[i], fontsize=22, color=INK, fontweight="bold", pad=10)
        sub = ("arcs: depth and width of each pool" if i == 0 else "a lengthwise cut through one track:")
        sub2 = ("(the middle pools, away from the contours)" if i == 0 else "a flat fusion line, no width")
        ax.text(w / 2, -0.34, sub, ha="center", va="top", fontsize=18, color=INK2)
        ax.text(w / 2, -0.37, sub2, ha="center", va="top", fontsize=18, color=INK2)
    ax = fig.add_axes([0.76, 0.13, 0.22, 0.70])
    ax.axis("off")
    for j, (t, c, fs, fw) in enumerate([("Check first in", INK, 21, "bold"), ("WRX's layer view", INK, 21, "bold"),
                                        ("which way the", INK2, 19, None), ("hatch runs, and", INK2, 19, None),
                                        ("whether it turns", INK2, 19, None), ("layer to layer", INK2, 19, None),
                                        ("", INK, 10, None), ("The AM Module's", INK, 21, "bold"),
                                        ("steady-state pool is", INK2, 19, None), ("the arc on the left", INK2, 19, None)]):
        ax.text(0.0, 0.97 - 0.075 * j, t, color=c, fontsize=fs, fontweight=fw or "normal", va="top",
                transform=ax.transAxes)
    _note(fig)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def pmap(path: Path):
    """The 61 settings (real), with the wall sheet's first guess of each regime (Eagar-Tsai + overlap, 30 um)."""
    data = rows()
    fig = _fig("What the 84 walls test: 60 settings + the control")
    ax = fig.add_axes([0.08, 0.15, 0.56, 0.70], facecolor=SURFACE)
    seen = {}
    style = {"lack of fusion": (LOF, "v"), "dense": (DENSE, "o"), "keyhole mode": (KEY, "D")}
    pairs = {r["set"] for r in data if r["square"] == "4"}
    for r in data:
        if r["square"] == "4":
            continue
        reg = r["regime_30um"]
        c, m = style.get(reg, (MUTED, "o"))
        P, v = float(r["power_W"]), float(r["speed_mm_s"])
        if r["set"] == "C":
            ax.scatter([v], [P], s=420, marker="*", color=INK, edgecolor=SURFACE, lw=2, zorder=6)
            continue
        ax.scatter([v], [P], s=150, marker=m, color=c, edgecolor=SURFACE, lw=2, zorder=4,
                   label=None if reg in seen else reg)
        seen[reg] = 1
        if r["set"] in pairs:
            ax.scatter([v], [P], s=420, marker="o", facecolor="none", edgecolor=INK2, lw=1.6, zorder=3)
    vv = np.linspace(300, 3000, 50)
    for e, lab in ((0.274, "P/v of the 316L hatch"),):
        ax.plot(vv, e * vv, color=MUTED, lw=1.5, ls=(0, (5, 4)), zorder=1)
        ax.text(560, e * 560 - 26, lab, color=INK2, fontsize=16)
    ax.set_xscale("log")
    ax.set_xticks([400, 700, 1000, 2000, 3000])
    ax.set_xticklabels(["400", "700", "1000", "2000", "3000"])
    ax.set_xlim(300, 3200)
    ax.set_ylim(130, 395)
    ax.set_xlabel("Scan speed (mm/s)", fontsize=20, color=INK)
    ax.set_ylabel("Laser power (W)", fontsize=20, color=INK)
    ax.tick_params(labelsize=17, colors=INK2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.grid(True, color="#e6e5e0", lw=1)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    leg = ax.legend(loc="upper left", bbox_to_anchor=(1.03, 0.36), fontsize=17, frameon=True,
                    title="first guess (30 µm layers)", title_fontsize=16)
    leg.get_frame().set_edgecolor("#d8d7d2")
    ax2 = fig.add_axes([0.67, 0.15, 0.31, 0.70])
    ax2.axis("off")
    txt = [("★  control: 370 W, 1350 mm/s", INK, 19, "bold"),
           ("printed 6 times, 3 each way", INK2, 18, None),
           ("◯  printed both ways (18)", INK, 19, "bold"),
           ("on square 4, turned 90°", INK2, 18, None),
           ("", INK, 8, None),
           ("Next on this map:", INK, 20, "bold"),
           ("the AM Module's lack-of-fusion", INK2, 18, None),
           ("and keyhole boundaries (batch", INK2, 18, None),
           ("run, committed before the print),", INK2, 18, None),
           ("then each wall's measured", INK2, 18, None),
           ("porosity in the same place", INK2, 18, None),
           ("", INK, 8, None)]
    for j, (t, c, fs, fw) in enumerate(txt):
        ax2.text(0.0, 1.0 - 0.06 * j, t, color=c, fontsize=fs, fontweight=fw or "normal", va="top",
                 transform=ax2.transAxes)
    _note(fig, "Settings from the wall sheet (real). Regimes: its Eagar–Tsai + overlap first guess, not the AM Module")
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def record(path: Path):
    """What each wall hands the model, and how the next build's settings get picked."""
    fig = _fig("Per wall, for the AM Module, and the next build")
    ax = fig.add_axes([0.03, 0.12, 0.50, 0.74])
    ax.axis("off")
    cols = ["field", "example"]
    data = [("wall", "1.1.4 (square.part.wall)"), ("set, P, v", "W005: 239 W, 455 mm/s"),
            ("orientation", "along the blade"), ("porosity in the band", "0.4 %   (illustration)"),
            ("pores by class", "LoF 2, keyhole 7"), ("last-layer pool depth", "75 µm   (illustration)"),
            ("wall thickness", "1.31 mm"),
            ("build record", "layer, powder lot, O₂, spot")]
    y = 0.95
    ax.text(0.0, y, cols[0], fontsize=19, color=INK2, fontweight="bold", transform=ax.transAxes)
    ax.text(0.46, y, cols[1], fontsize=19, color=INK2, fontweight="bold", transform=ax.transAxes)
    y -= 0.04
    ax.plot([0, 0.98], [y, y], color=MUTED, lw=1.2, transform=ax.transAxes)
    for a, b in data:
        y -= 0.105
        ax.text(0.0, y, a, fontsize=19, color=INK, transform=ax.transAxes)
        ax.text(0.46, y, b, fontsize=19, color=INK, transform=ax.transAxes)
    ax = fig.add_axes([0.60, 0.17, 0.37, 0.62], facecolor=SURFACE)
    rng = np.random.default_rng(3)
    vv = np.geomspace(320, 3000, 120)
    edge = 0.16 * vv                                          # an illustrative lack-of-fusion boundary, P = e * v
    ax.fill_between(vv, edge * 0.86, edge * 1.16, color="#cde2fb", lw=0, zorder=1, label="model uncertainty")
    ax.plot(vv, edge, color="#2a78d6", lw=2.2, zorder=2, label="model's boundary")
    nv = np.geomspace(500, 2600, 16)
    ax.scatter(nv, 0.16 * nv * (1 + 0.08 * rng.standard_normal(16)), s=120, marker="o", color=INK,
               edgecolor=SURFACE, lw=2, zorder=4, label="next build's settings")
    ax.set_xscale("log")
    ax.set_xticks([400, 1000, 2000])
    ax.set_xticklabels(["400", "1000", "2000"])
    ax.set_xlim(320, 3000)
    ax.set_ylim(130, 395)
    ax.set_xlabel("Scan speed (mm/s)", fontsize=18, color=INK)
    ax.set_ylabel("Laser power (W)", fontsize=18, color=INK)
    ax.tick_params(labelsize=15, colors=INK2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_title("Batch BO: next settings where the model is unsure", fontsize=18, color=INK, pad=10)
    leg = ax.legend(loc="upper left", fontsize=15, frameon=True)
    leg.get_frame().set_edgecolor("#d8d7d2")
    _note(fig, "Illustration: the boundary, its band and the next settings are drawn, not computed")
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def make_all(folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    out = {}
    for key, fn in (("bse", lambda p: bse(p)), ("seg", lambda p: bse(p, segment=True)), ("etched", etched),
                    ("map", pmap), ("record", record)):
        p = folder / f"walls_screen_{key}.png"
        fn(p)
        out[key] = p
    return out


if __name__ == "__main__":
    import sys
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/walls_screens")
    for k, p in make_all(dest).items():
        print(k, p)
