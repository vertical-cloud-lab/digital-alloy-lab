"""One slide (16:9) on the data the Vertical Cloud Lab collected in its first year, built around
alloy discovery and qualification.

    python make_infographic.py        # writes infographic.png (200 dpi) and infographic.pdf

Every chart is drawn from data in this repo:
- ../tensile-alsi10mg-utah/raw/        raw MTS exports (analysed with ../tensile-alsi10mg-utah/analyze_tensile.py)
- ../eds-standards-alsi10mg-utah/raw/  raw EDAX .msa spectra, and results.csv for the quantification
- ../sem-eds-atomized-powders/         SEM of bronze lot k7m2q9
- data/ and img/                       compact copies from other branches and repos (sources in README.md)

The counts (header tiles and the bottom band) are in COUNTS below; each one is sourced in
../DATA-INVENTORY.md.
"""

import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
PD = HERE.parent
sys.path.insert(0, str(PD / "tensile-alsi10mg-utah"))
from analyze_tensile import analyse, read_mts  # noqa: E402

W, H = 13.333, 7.5  # inches, 16:9

# Reference palette (validated categorical slots 1-3) and text inks
BLUE, ORANGE, AQUA = "#257de0", "#f47230", "#00b894"
INK, INK2, INK3 = "#191919", "#555555", "#9c9c9c"
GRID, CARD, RULE = "#e6e6e6", "#f4f5f7", "#d9dce1"

plt.rcParams.update({
    "font.family": "Lato",
    "font.size": 7,
    "axes.edgecolor": INK3,
    "axes.labelcolor": INK2,
    "axes.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2,
    "ytick.major.size": 2,
    "xtick.labelsize": 6.2,
    "ytick.labelsize": 6.2,
    "axes.labelsize": 6.6,
    "pdf.fonttype": 42,
})

# ---------------------------------------------------------------------------------------------
# Counts. Sources and method are in ../DATA-INVENTORY.md; "~" marks an estimate.
# ---------------------------------------------------------------------------------------------
COUNTS = {
    "kpi": [
        ("~41,000", "files in six lab repos\n(all branches, each once)"),
        ("~12,000", "images: camera stills, SEM,\nvideo frames, plots"),
        ("~2,700 h", "of video, mostly\narchived livestreams"),
        ("~500,000", "sensor and\nbalance readings"),
        ("~4,300", "physical tests and runs\n(3,660 of them drop tests)"),
        ("1,267", "issues and PRs,\n10,655 comments"),
    ],
    "tiles": [],  # filled in below, after the bottom-band helpers
}


# ---------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------
def ax_at(fig, x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])


def text(fig, x, y, s, **kw):
    kw.setdefault("color", INK)
    return fig.text(x / W, y / H, s, **kw)


def box(fig, x, y, w, h, color=CARD, ec="none", lw=0.0, z=-10):
    p = FancyBboxPatch((x / W, y / H), w / W, h / H, transform=fig.transFigure,
                       boxstyle="round,pad=0,rounding_size=0.008", mutation_aspect=W / H,
                       facecolor=color, edgecolor=ec, linewidth=lw, zorder=z)
    fig.patches.append(p)


def style(ax, grid="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(pad=1.5)
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.6)
        ax.set_axisbelow(True)
    ax.patch.set_alpha(0)


def show_img(ax, path, w_in, h_in, center=(0.5, 0.5), zoom=1.0, gray=False):
    """Crop an image to the axes' aspect ratio around `center` (fractions) and show it."""
    im = Image.open(path).convert("L" if gray else "RGB")
    iw, ih = im.size
    target = w_in / h_in
    cw, ch = (ih * target, ih) if iw / ih > target else (iw, iw / target)
    cw, ch = cw / zoom, ch / zoom
    left = min(max(center[0] * iw - cw / 2, 0), iw - cw)
    top = min(max(center[1] * ih - ch / 2, 0), ih - ch)
    im = im.crop((int(left), int(top), int(left + cw), int(top + ch)))
    ax.imshow(im, cmap="gray" if gray else None, interpolation="lanczos")
    ax.set_axis_off()
    return im.size


def read_msa(path):
    e, c, on = [], [], False
    for line in Path(path).read_text(errors="replace").splitlines():
        if line.startswith("#SPECTRUM"):
            on = True
            continue
        if line.startswith("#ENDOFDATA"):
            break
        if on and line.strip():
            a, b = line.split(",")[:2]
            e.append(float(a))
            c.append(float(b))
    return np.array(e) / 1000.0, np.array(c)  # keV, counts


# ---------------------------------------------------------------------------------------------
# Panels of the five pipeline columns
# ---------------------------------------------------------------------------------------------
def panel_bo(ax):
    d = pd.read_csv(HERE / "data/bofn_k1_best_vs_spend.csv")
    x = d["spend_usd"] / 1000
    series = [
        ("tiered", "Tiered screening", ORANGE, 1.4, "-"),
        ("ei", "Standard BO", INK3, 1.1, "-"),
        ("pkgfn", "Network BO, partial\nevaluation (pKGFN)", BLUE, 1.8, "-"),
    ]
    for key, label, color, lw, ls in series:
        ax.plot(x, d[f"{key}_mean"], color=color, lw=lw, ls=ls, solid_capstyle="round")
    # where pKGFN first reaches screening's $100k level
    target = float(d["tiered_mean"].iloc[-1])
    i = int(np.argmax(d["pkgfn_mean"].to_numpy() >= target))
    x0 = float(x.iloc[i])
    x1 = float(x[d["tiered_mean"] >= target - 1e-9].iloc[0])
    ax.annotate("", xy=(x0, target), xytext=(x1, target),
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, target + 2.0, f"{x1 / x0:.1f}× less spend", ha="center", va="bottom",
            fontsize=6.6, color=INK, fontweight="bold")
    ends = {"pkgfn": 88.5, "ei": 79.0, "tiered": 58.5}
    for key, label, color, lw, ls in series:
        ax.text(101.5, ends[key], label, fontsize=5.9, color=INK2, va="center", ha="left",
                linespacing=0.95)
    ax.set_xlim(0, 100)
    ax.set_ylim(35, 95)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["$0", "25k", "50k", "75k", "$100k"])
    ax.set_yticks([40, 60, 80])
    ax.set_ylabel("Best alloy found\n(% of optimum)", linespacing=0.95)
    ax.set_xlabel("Simulated spend on make-print-test", labelpad=1)
    style(ax)


def panel_runs(ax):
    r = pd.read_csv(HERE / "data/atomizer_runs.csv", parse_dates=["date"])
    for _, row in r.iterrows():
        color = BLUE if row["family"] == "Al" else ORANGE
        g = row["powder_g"]
        basis = str(row["powder_basis"])
        if pd.notna(g) and g > 0:
            weighed = basis.startswith("weighed")
            ax.bar(row["date"], g, width=2.2, color=color if weighed else "white",
                   edgecolor=color, lw=1.0, hatch=None if weighed else "/////", zorder=3)
        elif pd.isna(g):
            ax.plot(row["date"], 60, marker="o", ms=4.5, mfc="white", mec=color, mew=1.0, zorder=3)
            ax.text(row["date"], 120, "not\nweighed", ha="center", va="bottom", fontsize=5.2,
                    color=INK2, linespacing=0.9)
        else:
            ax.plot(row["date"], 12, marker="o", ms=3.6, color=color, zorder=3)
    ax.text(pd.Timestamp("2026-10-27"), 1010, "985 g", ha="center", va="bottom", fontsize=6.4,
            fontweight="bold", color=INK)
    ax.text(pd.Timestamp("2026-11-10"), 640, "~610 g\n(est.)", ha="center", va="bottom",
            fontsize=5.6, color=INK2, linespacing=0.95)
    ax.text(pd.Timestamp("2026-10-12"), 230, "5 aluminium runs:\nlittle or no powder",
            ha="center", va="bottom", fontsize=5.9, color=INK2, linespacing=0.95)
    ax.text(pd.Timestamp("2026-11-07"), 1000, "5 bronze runs", ha="center", va="bottom",
            fontsize=5.9, color=INK2)
    ax.set_xlim(pd.Timestamp("2026-09-29"), pd.Timestamp("2026-11-16"))
    ax.set_ylim(0, 1150)
    ax.set_yticks([0, 500, 1000])
    ax.set_xticks(pd.to_datetime(["2026-10-01", "2026-10-15", "2026-11-01", "2026-11-15"]))
    ax.set_xticklabels(["Oct 1", "Oct 15", "Nov 1", "Nov 15"])
    ax.set_ylabel("Powder collected (g)")
    style(ax)


def panel_psd(ax):
    p = pd.read_csv(HERE / "data/k7m2q9_particles.csv")
    d, wt = p["ecd_um"].to_numpy(), p["weight"].to_numpy()
    bins = np.logspace(np.log10(10), np.log10(400), 34)
    num, _ = np.histogram(d, bins=bins, weights=wt)
    vol, _ = np.histogram(d, bins=bins, weights=wt * d**3)
    num, vol = num / num.sum() * 100, vol / vol.sum() * 100
    ax.axvspan(50, 200, color="#eef0f3", zorder=0, lw=0)
    ax.text(100, 25.3, "DED cut 50-200 um".replace("um", "µm"), ha="center", va="top",
            fontsize=5.6, color=INK2)
    ax.bar(bins[:-1], num, width=np.diff(bins), align="edge", color=BLUE, edgecolor="white",
           lw=0.4, zorder=2)
    ax.step(bins[:-1], vol, where="post", color=ORANGE, lw=1.3, zorder=3)
    ax.text(30.5, 17.5, "by number\nD50 47 µm", fontsize=6.0, color=INK, ha="right",
            va="center", linespacing=0.95)
    ax.text(118, 15.5, "by volume\nD50 104 µm", fontsize=6.0, color=INK, ha="left",
            va="center", linespacing=0.95)
    ax.set_xscale("log")
    ax.set_xlim(12, 400)
    ax.set_ylim(0, 26)
    ax.set_xticks([20, 50, 100, 200])
    ax.set_xticklabels(["20", "50", "100", "200"])
    ax.minorticks_off()
    ax.set_xlabel("Particle diameter (µm)", labelpad=1)
    ax.set_ylabel("Share per bin (%)")
    style(ax)


def panel_spectrum(ax):
    e, c = read_msa(PD / "eds-standards-alsi10mg-utah/raw/unknowns/sobol_exp_1_1.msa")
    keep = (e > 0.15) & (e < 2.3)
    ax.fill_between(e[keep], 1, np.maximum(c[keep], 1), color=BLUE, alpha=0.18, lw=0)
    ax.plot(e[keep], np.maximum(c[keep], 1), color=BLUE, lw=0.9)
    ax.set_yscale("log")
    peaks = [("O", 0.525), ("Mg", 1.254), ("Al", 1.487), ("Si", 1.740)]
    for el, en in peaks:
        i = np.argmin(abs(e - en))
        top = c[max(i - 3, 0): i + 4].max()
        ax.text(en, top * 1.6, el, ha="center", va="bottom", fontsize=6.6, fontweight="bold",
                color=INK)
    ax.set_xlim(0.15, 2.3)
    ax.set_ylim(80, c[keep].max() * 25)
    ax.set_xlabel("X-ray energy (keV)", labelpad=1)
    ax.set_ylabel("Counts (log)")
    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(numticks=4))
    style(ax, grid=None)


def panel_composition(axs):
    res = pd.read_csv(PD / "eds-standards-alsi10mg-utah/results.csv").set_index("run")
    good = res.loc["sobol_exp_1_1"]
    rows = {  # (spec_lo, spec_hi, standardless feedstock, standards-based, sd, xlim, ticks)
        "Mg": (0.20, 0.45, 1.4, good["Mg_wt_norm"], good["Mg_sd"], (0, 1.6), [0, 0.5, 1.0, 1.5]),
        "Si": (9.0, 11.0, 7.9, good["Si_wt_norm"], good["Si_sd"], (6.5, 12.5), [7, 9, 11]),
    }
    for ax, (el, (lo, hi, sl, sb, sd, xl, ticks)) in zip(axs, rows.items()):
        ax.axvspan(lo, hi, color="#e3e6ea", lw=0, zorder=0)
        ax.plot([sl], [1], marker="o", ms=5.5, mfc="white", mec=INK2, mew=1.1, zorder=3)
        ax.errorbar([sb], [0], xerr=[2 * sd], fmt="o", ms=5.5, color=BLUE, mec="white", mew=0.8,
                    elinewidth=1.0, capsize=0, zorder=3)
        ax.set_ylim(-0.7, 1.7)
        ax.set_xlim(*xl)
        ax.set_xticks(ticks)
        ax.set_yticks([])
        ax.text(xl[0] + 0.03 * (xl[1] - xl[0]), 1.62, f"{el} (wt %)", fontsize=6.4,
                fontweight="bold", va="top", color=INK)
        ax.text((lo + hi) / 2, -0.62, "spec", fontsize=5.4, color=INK2, ha="center", va="bottom")
        style(ax, grid=None)
        ax.spines["left"].set_visible(False)
    axs[0].text(1.30, 1.0, "standardless", fontsize=5.6, color=INK2, ha="right", va="center")
    axs[0].text(0.47, 0.0, " with standards", fontsize=5.6, color=INK, ha="left", va="center")


def panel_tensile(ax):
    res = pd.read_csv(PD / "tensile-alsi10mg-utah/results.csv").set_index("test")
    for t in (1, 2, 3, 4, 5):
        df = read_mts(PD / "tensile-alsi10mg-utah" / res.loc[t, "csv"])
        r = analyse(df, res.loc[t, "area_mm2"])
        eps, s, i_f = r["_eps"], r["_stress"], r["_i_f"]
        first = int(np.nonzero(s >= 0)[0][0])
        x, y = eps[first: i_f + 1], s[first: i_f + 1]
        if t == 5:
            ax.plot(x, y, color=BLUE, lw=1.7, zorder=5)
        elif t == 4:
            ax.plot(x, y, color=INK3, lw=0.9, ls=(0, (3, 2)), zorder=3)
        else:
            ax.plot(x, y, color=INK3, lw=0.9, zorder=3)
    ds = pd.read_csv(PD / "tensile-alsi10mg-utah/datasheet-values.csv")
    pts = [
        ("EOS", "horizontal", "machined", "EOS, machined"),
        ("Nikon SLM Solutions", "vertical", "near-net-shape (as built)", "Nikon, as built"),
    ]
    for src, orient, surf, label in pts:
        row = ds[(ds["source"] == src) & (ds["orientation"] == orient)
                 & ds["specimen_surface"].str.startswith(surf)].iloc[0]
        ax.plot(row["elongation_pct"], row["uts_MPa"], marker="D", ms=4.5, mfc="white", mec=ORANGE,
                mew=1.2, zorder=6)
        if src == "EOS":
            ax.text(row["elongation_pct"] + 0.3, row["uts_MPa"] - 40, label, fontsize=5.7,
                    color=INK2, ha="right", va="top")
        else:
            ax.text(row["elongation_pct"] - 0.3, row["uts_MPa"] + 30, label, fontsize=5.7,
                    color=INK2, ha="right", va="bottom")
    ax.text(6.0, 285, "ours (Utah):\n5 tests", fontsize=5.9, color=INK, ha="left", va="center",
            linespacing=0.95)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 540)
    ax.set_yticks([0, 200, 400])
    ax.set_xlabel("Strain (%)", labelpad=1)
    ax.set_ylabel("Stress (MPa)")
    style(ax)


# ---------------------------------------------------------------------------------------------
# Bottom band: the rest of the lab
# ---------------------------------------------------------------------------------------------
def sparkline_airgradient(ax):
    d = pd.read_csv(HERE / "data/airgradient_cb154_daily.csv", parse_dates=["timestamp"])
    ax.fill_between(d["timestamp"], d["rhum_corrected_min"], d["rhum_corrected_max"],
                    color=BLUE, alpha=0.18, lw=0)
    ax.plot(d["timestamp"], d["rhum_corrected_mean"], color=BLUE, lw=0.9)
    ax.set_ylim(0, 70)
    ax.set_yticks([0, 30, 60])
    ax.set_xticks(pd.to_datetime(["2026-03-01", "2026-06-01", "2026-09-01"]))
    ax.set_xticklabels(["Mar", "Jun", "Sep"])
    ax.text(0.02, 0.97, "room RH (%), daily range", transform=ax.transAxes, fontsize=5.4,
            color=INK2, va="top")
    style(ax)


def text_width_in(s, size, weight="bold"):
    """Width of a string in inches, for laying out text that sits next to it."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath
    tp = TextPath((0, 0), s, size=size, prop=FontProperties(family="Lato", weight=weight))
    return tp.get_extents().width / 72.0


LABEL_BOX = dict(facecolor="black", alpha=0.5, pad=1.6, lw=0)

# Vertical layout (inches from the bottom of the slide)
KPI_Y, KPI_H = 5.86, 0.56
COL_TOP, COL_BOT = 5.70, 2.00
UP_Y, UP_H = 3.80, 1.32        # photo / upper chart slot
LO_Y, LO_H = 2.84, 0.78        # lower chart axes (tick labels hang below)
BAND_Y, BAND_H = 0.30, 1.46    # bottom band


def draw(out_png, out_pdf):
    fig = plt.figure(figsize=(W, H), dpi=200)
    fig.patch.set_facecolor("white")

    # ---- title ------------------------------------------------------------------------------
    text(fig, 0.35, 7.16, TITLE, fontsize=21, fontweight="bold", va="top")
    text(fig, 0.35, 6.74, SUBTITLE, fontsize=10.5, color=INK2, va="top")

    # ---- KPI strip ----------------------------------------------------------------------------
    n_k = len(COUNTS["kpi"])
    kgap = 0.10
    kw = (W - 0.70 - (n_k - 1) * kgap) / n_k
    for i, (num, lab) in enumerate(COUNTS["kpi"]):
        x = 0.35 + i * (kw + kgap)
        box(fig, x, KPI_Y, kw, KPI_H, color="white", ec=RULE, lw=0.8)
        text(fig, x + 0.10, KPI_Y + KPI_H / 2, num, fontsize=14, fontweight="bold", va="center")
        text(fig, x + 0.10 + text_width_in(num, 14) + 0.08, KPI_Y + KPI_H / 2, lab,
             fontsize=6.0, color=INK2, va="center", linespacing=1.05)

    # ---- five pipeline columns ----------------------------------------------------------------
    x0, cg = 0.35, 0.095
    cw = (W - 0.70 - 4 * cg) / 5
    for k, (stage, title, num, numlab, caption) in enumerate(COLUMNS):
        x = x0 + k * (cw + cg)
        box(fig, x, COL_BOT, cw, COL_TOP - COL_BOT)
        fig.patches.append(Rectangle((x / W, (COL_TOP - 0.045) / H), cw / W, 0.045 / H,
                                     transform=fig.transFigure, color=BLUE, lw=0, zorder=-5))
        text(fig, x + 0.12, COL_TOP - 0.17, stage, fontsize=6.6, fontweight="bold", color=BLUE,
             va="center")
        text(fig, x + 0.12, COL_TOP - 0.38, title, fontsize=10, fontweight="bold", va="center")
        text(fig, x + cw - 0.12, COL_TOP - 0.19, num, fontsize=14, fontweight="bold",
             va="center", ha="right")
        text(fig, x + cw - 0.12, COL_TOP - 0.43, numlab, fontsize=5.7, color=INK2, va="center",
             ha="right", linespacing=1.0)
        text(fig, x + 0.12, COL_BOT + 0.07, caption, fontsize=6.2, color=INK, va="bottom",
             linespacing=1.12)
        if k < 4:
            text(fig, x + cw + cg / 2, COL_TOP - 0.30, "›", fontsize=17, color=INK3,
                 ha="center", va="center")
    pad = 0.12
    ch_x, ch_w = 0.47, cw - 0.60   # chart axes inset (room for y labels on the left)

    # column 1: BO curves (upper), computed-data list (lower)
    ax = ax_at(fig, x0 + ch_x, UP_Y + 0.12, cw - 1.12, UP_H - 0.12)
    panel_bo(ax)
    for j, (n, lab) in enumerate(COMPUTED):
        yy = LO_Y + LO_H - 0.12 - j * 0.165
        text(fig, x0 + 0.66, yy, n, fontsize=7.3, fontweight="bold", ha="right", va="center")
        text(fig, x0 + 0.73, yy, lab, fontsize=6.3, color=INK2, va="center")

    # column 2: spray photo (upper), runs (lower)
    x = x0 + 1 * (cw + cg)
    wa = (cw - 2 * pad - 0.05) * 0.5
    ax = ax_at(fig, x + pad, UP_Y, wa, UP_H)
    show_img(ax, HERE / "img/atomizer-2026-10-27-viewport-spray.jpg", wa, UP_H,
             center=(0.56, 0.50))
    ax.text(0.04, 0.04, "Oct 27: melt on\nthe ultrasonic plate", transform=ax.transAxes,
            fontsize=5.6, color="white", va="bottom", ha="left", bbox=LABEL_BOX,
            linespacing=1.0)
    ax = ax_at(fig, x + pad + wa + 0.05, UP_Y, wa, UP_H)
    show_img(ax, HERE / "img/k7m2q9-sieved-jars.jpg", wa, UP_H, center=(0.5, 0.55))
    ax.text(0.04, 0.04, "lot k7m2q9,\nsieved", transform=ax.transAxes, fontsize=5.6,
            color="white", va="bottom", ha="left", bbox=LABEL_BOX, linespacing=1.0)
    ax = ax_at(fig, x + ch_x, LO_Y, ch_w, LO_H)
    panel_runs(ax)

    # column 3: SEM (upper), PSD (lower)
    x = x0 + 2 * (cw + cg)
    ax = ax_at(fig, x + pad, UP_Y, cw - 2 * pad, UP_H)
    sem = PD / "sem-eds-atomized-powders/nab-c63000-k7m2q9/sem_200x.png"
    iw, ih = show_img(ax, sem, cw - 2 * pad, UP_H, center=(0.5, 0.5), zoom=1.25, gray=True)
    bar_px = 200 / 1.150  # sem_200x.png is resampled to 1.150 um/px (README of that folder)
    ax.add_patch(Rectangle((iw * 0.95 - bar_px, ih * 0.90), bar_px, ih * 0.025, color="white",
                           lw=0))
    ax.text(iw * 0.95 - bar_px / 2, ih * 0.875, "200 µm", color="white", fontsize=5.8,
            ha="center", va="bottom")
    ax.text(0.025, 0.05, "630 bronze, lot k7m2q9, SEM", transform=ax.transAxes, color="white",
            fontsize=5.8, va="bottom", bbox=LABEL_BOX)
    ax = ax_at(fig, x + ch_x, LO_Y, ch_w, LO_H)
    panel_psd(ax)

    # column 4: spectrum (upper), composition against spec (lower)
    x = x0 + 3 * (cw + cg)
    ax = ax_at(fig, x + ch_x, UP_Y + 0.14, ch_w, UP_H - 0.14)
    panel_spectrum(ax)
    ax.text(0.98, 0.97, "AlSi10Mg coupon, 5 kV", transform=ax.transAxes, fontsize=5.8,
            color=INK2, ha="right", va="top")
    half = (cw - 0.36) / 2
    axs = [ax_at(fig, x + 0.14, LO_Y, half, LO_H + 0.04),
           ax_at(fig, x + 0.22 + half, LO_Y, half, LO_H + 0.04)]
    panel_composition(axs)

    # column 5: coupon photo (upper), stress-strain (lower)
    x = x0 + 4 * (cw + cg)
    ax = ax_at(fig, x + pad, UP_Y, cw - 2 * pad, UP_H)
    show_img(ax, PD / "tensile-alsi10mg-utah/coupons-on-build-plate.jpg", cw - 2 * pad, UP_H,
             center=(0.5, 0.55))
    ax.text(0.025, 0.05, "10 AlSi10Mg coupons printed at Utah", transform=ax.transAxes,
            fontsize=5.8, color="white", va="bottom", bbox=LABEL_BOX)
    ax = ax_at(fig, x + ch_x, LO_Y, ch_w, LO_H)
    panel_tensile(ax)

    # ---- bottom band: across the lab ----------------------------------------------------------
    draw_bottom_band(fig)

    # ---- footer -------------------------------------------------------------------------------
    text(fig, 0.35, 0.10, FOOTER, fontsize=5.2, color=INK3, va="bottom")
    fig.savefig(out_png, dpi=200, facecolor="white")
    fig.savefig(out_pdf, facecolor="white")
    plt.close(fig)


def draw_bottom_band(fig):
    y0, h = BAND_Y, BAND_H
    text(fig, 0.35, y0 + h + 0.05, "ACROSS THE LAB", fontsize=6.6, fontweight="bold",
         color=BLUE, va="bottom")
    tiles = TILES
    n = len(tiles)
    tg = 0.09
    mw = 3.05  # width of the "what it shows" box
    tw = (W - 0.70 - mw - n * tg) / n
    for i, t in enumerate(tiles):
        x = 0.35 + i * (tw + tg)
        box(fig, x, y0, tw, h)
        vis_h = 0.70
        if t.get("img"):
            ax = ax_at(fig, x + 0.07, y0 + h - 0.07 - vis_h, tw - 0.14, vis_h)
            show_img(ax, HERE / t["img"], tw - 0.14, vis_h, center=t.get("center", (0.5, 0.5)),
                     zoom=t.get("zoom", 1.0))
        elif t.get("plot"):
            ax = ax_at(fig, x + 0.30, y0 + h - 0.07 - vis_h + 0.14, tw - 0.40, vis_h - 0.16)
            t["plot"](ax)
        text(fig, x + 0.09, y0 + 0.50, t["num"], fontsize=11, fontweight="bold", va="center")
        text(fig, x + 0.09, y0 + 0.27, t["label"], fontsize=5.8, color=INK2, va="center",
             linespacing=1.05)
        text(fig, x + 0.09, y0 + 0.06, t.get("repo", ""), fontsize=5.0, color=INK3, va="bottom")
    mx = W - 0.35 - mw
    box(fig, mx, y0, mw, h, color="white", ec=BLUE, lw=1.0)
    text(fig, mx + 0.13, y0 + h - 0.17, "What it shows", fontsize=9.5, fontweight="bold",
         va="center")
    text(fig, mx + 0.13, y0 + h - 0.31, MEANING, fontsize=6.25, color=INK, va="top",
         linespacing=1.2)


# ---------------------------------------------------------------------------------------------
# Words and counts
# ---------------------------------------------------------------------------------------------
TITLE = "A year of data at the Vertical Cloud Lab"
SUBTITLE = ("Alloy discovery and qualification in 2026: what we measured, simulated and "
            "recorded, and what it shows")

COLUMNS = [
    ("1  DESIGN", "Simulate, search, read", "~1,250", "simulated BO\ncampaigns",
     "Synthetic Al/LPBF benchmark, 20 seeds per policy:\nwhen CALPHAD screening misses a "
     "cracking effect,\nnetwork BO reaches screening's \\$100k result for\nabout \\$26k. No "
     "model is fitted to our data yet."),
    ("2  MAKE", "Atomize powder", "10", "atomizer runs,\n13 powder lots",
     "Aluminium gave little powder. 630 bronze worked\non Oct 27: 985 g below 250 µm, the "
     "first usable\nlot (k7m2q9). Nothing has been printed from\nour own powder yet."),
    ("3  CHARACTERIZE", "Size and shape", "5,937", "particles sized\nfrom SEM",
     "Bronze lot k7m2q9, 9 SEM fields: round (form\nfactor 0.99), D50 47 µm by number, "
     "104 µm by\nvolume. The only size distribution so far; no\naluminium lot has one yet."),
    ("4  COMPOSITION", "EDS against standards", "32", "EDS spectra,\n15 of them standards",
     "Polished AlSi10Mg coupon against pure Al, Si and\nMgO: Mg 0.35 wt %, inside the spec "
     "(standardless\nEDS read 1.4); Si 11.1 wt %, at the 11.0 limit.\nOnly 1 of 17 runs is valid "
     "so far."),
    ("5  QUALIFY", "Print and pull", "5", "tensile tests,\n10 coupons printed",
     "As-built AlSi10Mg printed at Utah from bought\npowder: UTS 376 ± 10 MPa, about 81 % "
     "of the\ndatasheets, with half their elongation (4.5 %).\nNo high-temperature tests yet."),
]

COMPUTED = [
    ("8,256", "Eagar-Tsai melt-pool evaluations"),
    ("555", "compositions on a CALPHAD grid"),
    ("59", "DEM, CFD and FEA runs"),
    ("~500", "Edison literature reviews"),
]

FOOTER = ("Counts as of 2026-11-26 from the lab's public GitHub repos (all branches), issue "
          "threads and YouTube channel; sources and method in "
          "preliminary-data/DATA-INVENTORY.md. Script: "
          "preliminary-data/infographic/make_infographic.py (digital-alloy-lab PR #288).")

TILES = [
    dict(img="img/robot-arms-piper-2026-10-15.jpg", center=(0.45, 0.70), zoom=1.7, num="~30",
         label="logged runs of the PiPER\narm; 11 camera calibrations", repo="robot-arms"),
    dict(img="img/powder-doser-mid-dose.jpg", center=(0.45, 0.5), num="~390",
         label="dosing and flow trials,\n13 powders incl. AlSi10Mg", repo="powder-doser"),
    dict(img="img/cubxl-deck-2026-09-17.jpg", center=(0.47, 0.5), num="76",
         label="CubXL runs (pipetting, stirring)\ntoward corrosion tests", repo="byu-vcl (cubos)"),
    dict(plot=sparkline_airgradient, num="62,189",
         label="5-min air-quality records,\n327,349 raw (Feb 5-Oct 28)", repo="AirGradient (byu-vcl)"),
    dict(img="img/room-stream-2026-10-01.jpg", center=(0.5, 0.5), num="~2,640 h",
         label="of archived livestreams\n(355 recordings, Jul 30-Sep 25)",
         repo="streamingLambda"),
    dict(img="img/tensegrity-specimens.jpg", center=(0.5, 0.21), zoom=1.9, num="~3,660",
         label="drop-tower tests of ~50\nprinted specimens (to Aug 19)", repo="tensegrity-optimization"),
]
MEANING = (
    "\u2022 Every step of the alloy loop has now run once: we atomize\n"
    "   (bronze), size powder, measure composition against standards\n"
    "   and pull tensile bars.\n"
    "\u2022 Not yet on one material. Tensile and standards-based EDS are\n"
    "   on AlSi10Mg printed elsewhere from bought powder; our bronze\n"
    "   powder has not been printed.\n"
    "\u2022 Alloy data are thin (5 tensile tests, 1 valid EDS run, 1 size\n"
    "   distribution); most of the volume is automation and monitoring.\n"
    "\u2022 Next: print our own powder and fit the BO model to it."
)


if __name__ == "__main__":
    draw(HERE / "infographic.png", HERE / "infographic.pdf")
