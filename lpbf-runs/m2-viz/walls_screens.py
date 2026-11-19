"""Monitor screens for the wall-build animation (walls.py): what the SEM sections of the walls show and how they are
analysed. 1600 x 1000 px each (the monitor's 560 x 350 aspect).

Real numbers: the 33 settings (power, speed, spot, trace spacing) and Gan et al.'s keyhole number Ke from
../m2-track-design/out/wall_sheet.csv, and, where present, published 316L data
(../m2-track-design/out/literature_316l_data.csv) and the CALPHAD-based keyhole criterion
(../m2-track-design/out/calphad_316l_keyhole.csv). Every pore, melt pool and porosity value on these screens is drawn
by hand to show what will be measured, and each screen says so.
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


def _f(r, k):
    return float(r[k])


def picks():
    """Three walls for the BSE screens: the least energy per area (lack of fusion likely), the control, and the
    highest keyhole number (keyhole pores likely). Labels from the sheet; the pores drawn on them are not data."""
    data = [r for r in rows()]
    lo = min((r for r in data if r["set"] != "C"), key=lambda r: _f(r, "E_area_J_mm2"))
    hi = max((r for r in data if r["set"] != "C"), key=lambda r: _f(r, "Ke"))
    ctl = next(r for r in data if r["set"] == "C")
    out = []
    for kind, r in (("lof", lo), ("ok", ctl), ("key", hi)):
        name = "control" if r["set"] == "C" else r["set"]
        top = (f"{name}: {_f(r, 'power_W'):.0f} W, {_f(r, 'speed_mm_s'):.0f} mm/s\n"
               f"{_f(r, 'spot_um'):.0f} µm, {_f(r, 'trace_spacing_mm'):g} mm")
        sub = f"{_f(r, 'E_area_J_mm2'):.1f} J/mm², Ke {_f(r, 'Ke'):.1f}"
        out.append((kind, top, sub))
    return out


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
        if segment and in_core:                         # ring each counted pore so it reads at monitor scale
            ax.add_patch(Ellipse((x, y), 0.17, 0.17, fill=False, ec=c, lw=2.4, zorder=4))
    ax.add_patch(Rectangle((CORE_IN, CORE_END), WALL_T - 2 * CORE_IN, WALL_H - 2 * CORE_END, fill=False,
                           ls=(0, (4, 3)), lw=2.2, ec="#2a78d6", zorder=4))
    ax.set_xlim(-0.35, WALL_T + 0.35)
    ax.set_ylim(-0.8, WALL_H + 0.25)
    ax.set_aspect("equal")
    ax.axis("off")
    name, setting = title.split(": ")
    ax.text(WALL_T / 2, WALL_H + 1.55, name, ha="center", va="bottom", fontsize=21, color=INK, fontweight="bold")
    ax.text(WALL_T / 2, WALL_H + 0.35, setting, ha="center", va="bottom", fontsize=15, color=INK2,
            linespacing=1.15)
    ax.text(WALL_T / 2, -1.0, sub, ha="center", va="top", fontsize=17, color=INK2)


def bse(path: Path, segment=False):
    rng = np.random.default_rng(4)
    fig = _fig("BSE, unetched: porosity first" if not segment else "Segment pores in each wall's core band")
    specs = picks()
    for i, (kind, t, s) in enumerate(specs):
        ax = fig.add_axes([0.04 + i * 0.205, 0.11, 0.19, 0.61])
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
                 ("about 250 fields for 42 walls", INK2, 19, None)]
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
    heads = ["If the hatch runs along the wall (vectors 12.7 mm long)", "If it runs across the wall (vectors about 1 mm)"]
    subs = ["arcs side by side: the last track's pool is whole; each earlier one is cut by the next track",
            "the plane runs along one track: a flat fusion line, which gives the depth but not the width"]
    for i in range(2):
        y_ax = 0.555 if i == 0 else 0.145
        fig.text(0.04, y_ax + 0.315, heads[i], fontsize=22, color=INK, fontweight="bold", va="bottom")
        ax = fig.add_axes([0.04, y_ax, 0.62, 0.30])
        top, w = 0.0, WALL_T
        _bse_background(ax, rng, w, 0.17, y0=-0.17, grey=0.70)
        d = 0.075
        if i == 0:
            xs = np.arange(0.11 + 0.045, w - 0.11, 0.09)
            t = np.linspace(-1, 1, 80)
            for j, x in enumerate(xs):                      # each new track cuts the one before it
                half = 0.065
                xx = x + half * t
                keep = xx >= (x - half) if j == len(xs) - 1 else xx <= xs[j + 1] - half * 0.55
                ax.plot(xx[keep], (top - d * np.sqrt(1 - t ** 2))[keep], color="#3b3a37", lw=1.8, zorder=3)
            for x in (0.05, w - 0.05):                      # contour pools at the faces: narrower and deeper
                ax.plot(x + 0.04 * t, top - 0.13 * np.sqrt(1 - t ** 2), color="#3b3a37", lw=1.8, zorder=3)
            xm = xs[-1]
            ax.annotate("", xy=(xm, top - d), xytext=(xm, top), zorder=5,
                        arrowprops=dict(arrowstyle="<->", color="#2a78d6", lw=2.6))
            ax.annotate("", xy=(xm - 0.065, top + 0.018), xytext=(xm + 0.065, top + 0.018), zorder=5,
                        arrowprops=dict(arrowstyle="<->", color="#2a78d6", lw=2.6))
            ax.text(xm - 0.02, top - d - 0.012, "last track: depth and width", color="#2a78d6", fontsize=18,
                    ha="right", va="top", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.25", fc="#f4f4f2", ec="none", alpha=0.85))
            ax.text(0.10, top - 0.135, "contour", color=INK2, fontsize=16, ha="left", va="center", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.2", fc="#f4f4f2", ec="none", alpha=0.85))
        else:
            x = np.linspace(0.11, w - 0.11, 120)
            ax.plot(x, top - d + 0.006 * np.sin(x * 60), color="#3b3a37", lw=1.8, zorder=3)
            ax.annotate("", xy=(w / 2, top - d), xytext=(w / 2, top), zorder=5,
                        arrowprops=dict(arrowstyle="<->", color="#2a78d6", lw=2.6))
            ax.text(w / 2 + 0.03, top - d * 0.55, "depth only", color="#2a78d6", fontsize=18, ha="left",
                    va="center", zorder=5)
        ax.set_xlim(-0.03, w + 0.03)
        ax.set_ylim(-0.17, 0.04)
        ax.set_aspect("auto")
        ax.axis("off")
        fig.text(0.04, y_ax - 0.012, subs[i], fontsize=16.5, color=INK2, va="top")
    ax = fig.add_axes([0.70, 0.13, 0.28, 0.72])
    ax.axis("off")
    lines = [("Check first in", INK, 21, "bold"), ("WRX's layer view", INK, 21, "bold"),
             ("which way the hatch runs,", INK2, 18, None), ("and whether it turns", INK2, 18, None),
             ("from layer to layer", INK2, 18, None), ("", INK, 10, None),
             ("The top layers", INK, 21, "bold"), ("are the upskin, set to the", INK2, 18, None),
             ("wall's own four values:", INK2, 18, None), ("7-17 tracks in 1.05 mm", INK2, 18, None),
             ("", INK, 10, None),
             ("The AM Module's", INK, 21, "bold"), ("steady-state pool is the", INK2, 18, None),
             ("last track's arc (top)", INK2, 18, None)]
    y = 0.97
    for t_, c, fs, fw in lines:
        ax.text(0.0, y, t_, color=c, fontsize=fs, fontweight=fw or "normal", va="top", transform=ax.transAxes)
        y -= 0.022 if fs < 12 else 0.062
    _note(fig)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def _optional_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


LIT = HERE.parent / "m2-track-design" / "out" / "literature_316l_data.csv"
KEYHOLE = HERE.parent / "m2-track-design" / "out" / "calphad_316l_keyhole.csv"
KE_C = {"transition": "#1baf7a", "keyhole": "#6250d6"}       # Gan et al.'s bands: 1.4-6 transition, 6-16 stable


def _m2_published() -> list[tuple[float, float, float, str]]:
    """(v, P, relative density %, source) for published 316L on Concept Laser M2 machines, from the literature check."""
    out = []
    for q in _optional_csv(LIT):
        if "M2" not in q.get("machine", "") or not q.get("power_W") or not q.get("speed_mm_s"):
            continue
        m = q.get("measure", "")
        try:
            P, v, val = float(q["power_W"]), float(q["speed_mm_s"]), float(q["value"])
        except ValueError:
            continue
        if m.startswith("relative_density"):
            dens = val
        elif m.startswith("porosity"):
            dens = 100.0 - val
        else:
            continue
        if 250 <= v <= 3200 and 130 <= P <= 395:
            out.append((v, P, dens, q["source_doi"]))
    return out


KING_C = {"conduction": "#2a78d6", "transition": "#1baf7a", "keyhole": "#6250d6"}
KING_LAB = {"conduction": "conduction (ΔH/h_s < 26)", "transition": "transition (26–30)",
            "keyhole": "keyhole (ΔH/h_s ≥ 30)"}


def pmap(path: Path):
    """The 33 settings (real) on the power-speed plane: spot as marker size, King et al.'s keyhole criterion as
    colour (if calphad_316l.py has run), repeats ringed, published M2 316L densities as grey squares."""
    data = rows()
    king = {q["set"].split("_")[0]: q for q in _optional_csv(KEYHOLE)}
    fig = _fig("What the 42 walls test: 32 settings + the control")
    ax = fig.add_axes([0.08, 0.15, 0.56, 0.70], facecolor=SURFACE)
    seen, done = {}, set()
    reps = {r["set"] for r in data if r.get("repeat") == "yes"}
    n_key, spots_key = 0, []
    for r in data:
        if r["set"] in done:
            continue
        done.add(r["set"])
        P, v, d, ke = _f(r, "power_W"), _f(r, "speed_mm_s"), _f(r, "spot_um"), _f(r, "Ke")
        size = 60 + 340 * (d - 50.0) / 150.0           # marker area grows with the spot, 50-200 um
        if r["set"] == "C":
            ax.scatter([v], [P], s=520, marker="*", color=INK, edgecolor=SURFACE, lw=2, zorder=6)
            continue
        if king:
            q = king.get(r["set"])
            dh = float(q["dH_hs_King_constants"]) if q else 3.73 * ke
            band = "keyhole" if dh >= 30 else ("transition" if dh >= 26 else "conduction")
        else:
            band = "keyhole" if ke >= 6.0 else "transition"
        if band == "keyhole":
            n_key += 1
            spots_key.append(d)
        col = KING_C.get(band, KE_C.get(band, MUTED))
        lab = KING_LAB[band] if king else {"transition": "transition (Ke 1.4–6)", "keyhole": "keyhole (Ke 6–15)"}[band]
        ax.scatter([v], [P], s=size, marker="o", color=col, alpha=0.85, edgecolor=SURFACE, lw=1.5, zorder=4,
                   label=None if band in seen else lab)
        seen[band] = 1
        if r["set"] in reps:
            ax.scatter([v], [P], s=size * 1.9 + 160, marker="o", facecolor="none", edgecolor=INK2, lw=1.6, zorder=3)
    pub = _m2_published()
    if pub:
        hi = [(v, P) for v, P, dd, _ in pub if dd >= 99.0]
        lo = [(v, P) for v, P, dd, _ in pub if dd < 99.0]
        if hi:
            ax.scatter(*zip(*hi), s=46, marker="s", color="#c9c8c2", edgecolor="#8a8984", lw=0.8, zorder=2,
                       label="published M2 316L, ≥ 99 %")
        if lo:
            ax.scatter(*zip(*lo), s=46, marker="s", facecolor=SURFACE, edgecolor="#8a8984", lw=1.0, zorder=2,
                       label="published M2 316L, < 99 %")
    vv = np.linspace(300, 3000, 50)
    ax.plot(vv, 0.274 * vv, color=MUTED, lw=1.5, ls=(0, (5, 4)), zorder=1)
    ax.text(560, 141, "P/v of the 316L hatch", color=INK2, fontsize=15)
    ax.set_xscale("log")
    ax.set_xticks([400, 700, 1000, 2000, 3000])
    ax.set_xticklabels(["400", "700", "1000", "2000", "3000"])
    ax.set_xlim(280, 3200)
    ax.set_ylim(130, 395)
    ax.set_xlabel("Scan speed (mm/s)", fontsize=20, color=INK)
    ax.set_ylabel("Laser power (W)", fontsize=20, color=INK)
    ax.tick_params(labelsize=17, colors=INK2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(MUTED)
    ax.grid(True, color="#e6e5e0", lw=1)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    leg = ax.legend(loc="lower left", bbox_to_anchor=(1.03, -0.02), fontsize=15, frameon=True,
                    title="King et al.'s criterion" if king else "colour: keyhole number", title_fontsize=15)
    for h in leg.legend_handles:
        if hasattr(h, "set_sizes"):
            h.set_sizes([120])
    leg.get_frame().set_edgecolor("#d8d7d2")
    ax2 = fig.add_axes([0.67, 0.15, 0.31, 0.70])
    ax2.axis("off")
    txt = [("★  control: 370 W, 1350 mm/s,", INK, 18, "bold"),
           ("     130 µm, 0.09 mm; on both squares", INK2, 17, None),
           ("◯  on both squares (8 settings)", INK, 18, "bold"),
           ("●  marker size: spot, 50–200 µm", INK, 18, "bold"),
           ("     trace spacing 0.06–0.14 mm", INK2, 17, None),
           ("", INK, 8, None)]
    if king and spots_key:
        txt += [(f"{n_key} of 32 at or over King's", INK, 18, "bold"),
                (f"threshold, all at {min(spots_key):.0f}–{max(spots_key):.0f} µm spots", INK, 18, "bold"),
                ("", INK, 8, None)]
    txt += [("Next: the AM Module's boundaries,", INK2, 17, None),
            ("then each wall's porosity", INK2, 17, None)]
    for j, (t, c, fs, fw) in enumerate(txt):
        ax2.text(0.0, 1.0 - 0.058 * j, t, color=c, fontsize=fs, fontweight=fw or "normal", va="top",
                 transform=ax2.transAxes)
    _note(fig, "Real settings on the P-v plane. Colour: King et al. 2014 (σ = D4σ/4). Grey: published M2 316L. "
               "Not the AM Module")
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def record(path: Path):
    """What each wall hands the model, and how the next build's settings get picked."""
    fig = _fig("Per wall, for the AM Module, and the next build")
    ax = fig.add_axes([0.03, 0.12, 0.50, 0.74])
    ax.axis("off")
    cols = ["field", "example"]
    r = next(q for q in rows() if (q["square"], q["part"], q["wall"]) == ("1", "1", "1"))
    data = [("wall", "1.1.1 (square.part.wall)"),
            ("set", f"{r['set']}: {_f(r, 'power_W'):.0f} W, {_f(r, 'speed_mm_s'):.0f} mm/s"),
            ("spot, trace spacing", f"{_f(r, 'spot_um'):.0f} µm, {_f(r, 'trace_spacing_mm'):g} mm"),
            ("porosity in the band", "0.4 %   (illustration)"),
            ("pores by class", "LoF 2, keyhole 7   (illustration)"), ("last-layer pool depth", "75 µm   (illustration)"),
            ("wall thickness", "1.31 mm   (illustration)"),
            ("build record", "layer, powder lot, O₂, layer time")]
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
    ax.set_title("Batch BO: next settings where the model is unsure", fontsize=16, color=INK, pad=10)
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
