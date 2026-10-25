"""Figures for the copper/DED benchmark (Aptos, red = partial evaluation, grays = baselines), named bofn_cu_*.

    python plot.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

from analyze import CELLS, GRID, SHORT, at, curves, load

HERE = Path(__file__).parent
for f in (Path.home() / ".local/share/fonts/aptos").glob("Aptos*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update(
    {
        "font.family": "Aptos",
        "font.size": 15,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#8C8C8C",
        "axes.linewidth": 0.8,
        "xtick.color": "#595959",
        "ytick.color": "#595959",
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "axes.labelcolor": "#404040",
        "savefig.dpi": 220,
    }
)
INK, MUTED = "#262626", "#7F7F7F"
RED = "#C00000"
STYLE = {
    "pkgfn": dict(color=RED, lw=3.0, z=5, ls="-"),
    "eifn_reuse": dict(color=RED, lw=2.4, z=5, ls=(0, (4, 2))),
    "pkgfn_screen": dict(color="#E06666", lw=2.2, z=5, ls=(0, (1.5, 1.5))),
    "pkgfn_audit": dict(color="#E06666", lw=2.2, z=5, ls="-"),
    "mines_only": dict(color="#E06666", lw=2.2, z=5, ls=(0, (4, 2))),
    "eifn": dict(color="#404040", lw=2.0, z=4, ls="-"),
    "tiered": dict(color="#8C8C8C", lw=2.0, z=3, ls="-"),
    "funnel": dict(color="#8C8C8C", lw=2.0, z=3, ls=(0, (4, 2))),
    "ei": dict(color="#B4B4B4", lw=2.0, z=2, ls="-"),
    "random": dict(color="#D0D0D0", lw=2.0, z=1, ls="-"),
}
FADE = {RED: "#E6B3B3", "#404040": "#BDBDBD", "#8C8C8C": "#CFCFCF", "#B4B4B4": "#D9D9D9", "#595959": "#C4C4C4", "#E06666": "#F2CCCC", "#D0D0D0": "#E6E6E6"}
HEAD = (1.0, 1.0)


def main_curve(cell=HEAD, kinds=("pkgfn", "pkgfn_audit", "pkgfn_screen", "mines_only", "eifn_reuse", "eifn", "tiered", "funnel", "ei", "random"), out=None):
    """Every policy's best alloy demonstrated against spend, with direct labels."""
    data = load(cell)
    fig, ax = plt.subplots(figsize=(10, 5.8))
    x = GRID / 1e3
    finals = {}
    for k in kinds:
        if k not in data:
            continue
        c = curves(data[k], cell) * 100
        m, se = np.nanmean(c, 0), np.nanstd(c, 0) / np.sqrt(c.shape[0])
        st = STYLE[k]
        ax.fill_between(x, m - se, m + se, color=st["color"], alpha=0.12 if st["color"] in (RED, "#E06666") else 0.07, lw=0, zorder=st["z"])
        ax.plot(x, m, color=st["color"], lw=st["lw"], ls=st["ls"], zorder=st["z"] + 0.5, solid_capstyle="round")
        finals[k] = m[-1]
    ypos, last = {}, -1e9
    for k in sorted(finals, key=lambda k: finals[k]):
        ypos[k] = max(finals[k], last + 4.4)
        last = ypos[k]
    for k in finals:
        red = STYLE[k]["color"] in (RED, "#E06666")
        ax.annotate(f"{SHORT[k]} (n = {len(data[k])})", (x[-1], finals[k]), xytext=(x[-1] + 1.5, ypos[k]), textcoords="data", va="center", ha="left", fontsize=13,
                    color=INK if red else "#404040", fontweight="bold" if k == "pkgfn" else "normal", annotation_clip=False)
    ax.set_xlim(0, 100)
    ax.set_xlabel("New spend on experiments and simulations ($k)")
    ax.set_ylabel("Best alloy demonstrated\n(% of true optimum)")
    ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.subplots_adjust(right=0.68)
    out = out or HERE / f"bofn_cu_best_vs_spend_k{cell[0]:g}e{cell[1]:g}_all_policies.png"
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- the proposal's Fig. fig:sim
PV_KINDS = ("pkgfn", "eifn_reuse", "eifn", "ei", "tiered")
PV_SHORT = {"pkgfn": "Partial: pKGFN", "eifn_reuse": "Partial: BOFN + reuse", "eifn": "Full: BOFN", "ei": "Full: standard BO", "tiered": "Tiered screening"}


def slide_figure(cell=HEAD, kinds=PV_KINDS, out=None, base="tiered", ref="pkgfn", size=24, bands="highlight", figsize=(11, 6.2), right=0.64):
    """Best alloy vs spend in the bofn-prelim slide style: leader lines instead of a legend, a horizontal
    y label, and ticks only at the axis ends plus the two called-out values (the spend at which `ref`
    reaches `base`'s $100k level, and that level). Placed 3.1 in wide in the proposal."""
    data = load(cell)
    x = GRID / 1e3
    C = {k: curves(data[k], cell) * 100 for k in kinds if k in data}
    M = {k: np.nanmean(c, 0) for k, c in C.items()}
    SE = {k: np.nanstd(c, 0) / np.sqrt(c.shape[0]) for k, c in C.items()}
    target = float(np.nanmean(C[base][:, -1])) if base in C else float("nan")
    x_ref = x[np.argmax(M[ref] >= target)] if base in C and (M[ref] >= target).any() else None
    x_base = x[np.argmax(M[base] >= target - 1e-9)] if base in C else None
    if x_ref is not None and not (0 < x_ref < x_base):  # no callout when the baseline never improves on the seed alloys
        x_ref = None
    start = float(min(m[0] for m in M.values()))
    top = float(max(m[-1] for m in M.values()))
    y_lo, y_hi = start - 9, top + 4
    fig, ax = plt.subplots(figsize=figsize)
    for k in kinds:
        if k not in C:
            continue
        st = STYLE[k]
        if bands == "all" or (bands == "highlight" and (st["color"] == RED or k == base)):
            ax.fill_between(x, M[k] - SE[k], M[k] + SE[k], color=st["color"], alpha=0.13 if st["color"] == RED else 0.07, lw=0, zorder=st["z"])
        ax.plot(x, M[k], color=st["color"], lw=st["lw"] + 0.4, ls=st["ls"], zorder=st["z"] + 0.5, solid_capstyle="round")
    if x_ref is not None:
        guide = dict(color="#BFBFBF", lw=0.9, ls=(0, (1.5, 2.5)), zorder=1)
        ax.plot([0, x_ref], [target, target], **guide)
        ax.plot([x_ref, x_ref], [y_lo, target], **guide)
        ax.plot([x_ref, x_base], [target, target], color=INK, lw=1.4, zorder=9, solid_capstyle="butt")
        ax.plot([x_ref], [target], "o", color=INK, ms=6, zorder=10)
        ax.text((x_ref + x_base) / 2, target - 1.6, f"{x_base / x_ref:.1f}× less spend", ha="center", va="top", fontsize=size + 2, color=INK, zorder=10)
    finals = {k: M[k][-1] for k in C}
    axes_h_pt = figsize[1] * (0.86 - 0.21) * 72  # must match subplots_adjust below
    gap = size * 1.35 * (y_hi - y_lo) / axes_h_pt
    order = sorted(finals, key=lambda k: finals[k])
    ypos, last = {}, -1e9
    for k in order:
        ypos[k] = max(finals[k], last + gap)
        last = ypos[k]
    shift = np.mean([ypos[k] - finals[k] for k in order])
    for k in order:
        ypos[k] -= shift
    x_lab = 103.2
    for k in order:
        col = STYLE[k]["color"]
        ax.plot([100.3, x_lab - 0.9], [finals[k], ypos[k]], color=FADE.get(col, "#CCCCCC"), lw=1.8, clip_on=False, zorder=1, solid_capstyle="round")
        ax.text(x_lab, ypos[k], PV_SHORT.get(k, SHORT[k]), ha="left", va="center", fontsize=size, color=RED if col == RED else "#404040", clip_on=False)
    ax.set_xlim(0, 100)
    ax.set_ylim(y_lo, y_hi)
    xt = [0, 100] if x_ref is None else [0, x_ref, 100]
    ax.set_xticks(xt, [f"{v:g}" for v in xt])
    yt = [start, top] if x_ref is None else [start, target, top]
    ax.set_yticks(yt, [f"{v:.0f}" for v in yt])
    ax.tick_params(axis="both", which="major", length=6, width=0.8, color="#8C8C8C", labelsize=size, labelcolor="#404040", pad=6)
    for side in ("left", "bottom"):
        ax.spines[side].set_position(("outward", 12))
    ax.spines["left"].set_bounds(start, top)
    ax.spines["bottom"].set_bounds(0, 100)
    ax.set_xlabel("New spend ($k)", fontsize=size, color="#404040", labelpad=10)
    ax.text(-0.11, 1.03, "Best alloy demonstrated\n(% of true optimum)", transform=ax.transAxes, ha="left", va="bottom", fontsize=size, color="#404040", linespacing=0.95)
    fig.subplots_adjust(left=0.11, right=right, top=0.86, bottom=0.21)
    out = out or HERE / f"bofn_cu_best_vs_spend_k{cell[0]:g}_partial_vs_full.png"
    fig.savefig(out, dpi=300)
    problems = check_overlaps(fig, ax)
    plt.close(fig)
    if problems:
        print(f"{Path(out).name}: {len(problems)} text/line overlaps:\n  " + "\n  ".join(problems))
    return out


def check_overlaps(fig, ax):
    """Flag text boxes that overlap each other or that a plotted line passes through."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    texts = [t for t in ax.texts + [ax.xaxis.label] if t.get_text().strip()]
    boxes = [(t.get_text().replace("\n", " / "), t.get_window_extent(r).expanded(1.02, 1.1)) for t in texts]
    out = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i][1].overlaps(boxes[j][1]):
                out.append(f"text '{boxes[i][0]}' overlaps text '{boxes[j][0]}'")
    for ln in ax.lines:
        xy = ln.get_xydata()
        if len(xy) < 2:
            continue
        pts = ax.transData.transform(xy)
        seg = np.concatenate([np.linspace(pts[k], pts[k + 1], 12) for k in range(len(pts) - 1)])
        for name, bb in boxes:
            if ((seg[:, 0] > bb.x0) & (seg[:, 0] < bb.x1) & (seg[:, 1] > bb.y0) & (seg[:, 1] < bb.y1)).any():
                out.append(f"a line ({ln.get_color()}, lw {ln.get_linewidth()}) passes through '{name}'")
    return out


# --------------------------------------------------------------------------- allocation, sensitivity, network
STAGE_TITLES = {"A": "Atomize, 0.5 kg ($400)", "U": "Small DED, Utah ($500)", "M": "Large DED, Mines ($1,500+)", "I": "30-day immersion ($400)"}


def allocation(cell=HEAD, kinds=("pkgfn", "mines_only", "eifn_reuse", "eifn", "tiered"), out=None):
    """How many of the main stages every policy bought with the same $100k (mean over seeds)."""
    data = load(cell)
    kinds = [k for k in kinds if k in data]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.4), sharey=True)
    for ax, grp in zip(axes, ("A", "U", "M", "I")):
        vals = [np.mean([run["counts"][grp] for run in data[k]]) for k in kinds]
        y = np.arange(len(kinds))[::-1]
        ax.barh(y, vals, height=0.55, color=[STYLE[k]["color"] for k in kinds])
        for yi, v in zip(y, vals):
            ax.text(v + 0.4, yi, f"{v:.0f}", va="center", fontsize=13, color=INK)
        ax.set_title(STAGE_TITLES[grp], fontsize=14, color=INK, loc="left")
        ax.set_yticks(y, [SHORT[k] for k in kinds])
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
    fig.tight_layout()
    out = out or HERE / f"bofn_cu_allocation_k{cell[0]:g}e{cell[1]:g}.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def sensitivity(spend=100_000, kinds=("pkgfn", "eifn_reuse", "eifn", "tiered", "ei"), out=None):
    """Value at a fixed spend in each (kappa, eta) cell."""
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    xs = np.arange(len(CELLS))
    ends = {}
    for k in kinds:
        m_, s_ = [], []
        for c in CELLS:
            data = load(c)
            if k not in data:
                m_.append(np.nan), s_.append(np.nan)
                continue
            v = at(curves(data[k], c), spend) * 100
            m_.append(np.nanmean(v)), s_.append(np.nanstd(v) / np.sqrt(len(v)))
        st = STYLE[k]
        ax.errorbar(xs, m_, yerr=s_, color=st["color"], lw=st["lw"], ls=st["ls"], marker="o", ms=8, mec="white", mew=2, capsize=0, zorder=st["z"])
        ends[k] = next((v for v in m_[::-1] if v == v), np.nan)
    last = -1e9
    for k in sorted(ends, key=lambda k: ends[k]):
        y = max(ends[k], last + 5)
        last = y
        ax.text(xs[-1] + 0.15, y, SHORT[k], va="center", fontsize=13, color=INK, fontweight="bold" if k == "pkgfn" else "normal")
    ax.set_xticks(xs, ["both\nscreens\nbiased", "both\nscreens\nright", "crack\nscreen\nbiased", "1-hour\nscreen\nbiased"])
    ax.set_xlim(-0.3, len(CELLS) - 0.7 + 0.1)
    ax.set_ylabel(f"Best alloy demonstrated at ${spend / 1e3:.0f}k\n(% of true optimum)")
    ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.subplots_adjust(right=0.7)
    out = out or HERE / f"bofn_cu_sensitivity_at{spend / 1e3:.0f}k.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def dag_strip(out=None):
    """The copper/DED network as a one-line chain: what each stage costs and returns."""
    from matplotlib.patches import FancyBboxPatch

    stages = [
        ("CALPHAD +\nheat flow", "$10", "strengthening,\nsolidification index,\nnucleant (Fe-rich\nkappa), conductivity"),
        ("Atomize\n0.5 kg", "$400", "powder\nquality"),
        ("Small DED\n(Utah)", "$500", "dense, crack-free\nindex (power\ncapped at 0.5)"),
        ("Large DED\n(Mines)", r"\$3,100 / \$1,500", "dense, crack-free\nfraction (the first\nsession buys a 2 kg lot)"),
        ("Microscopy", "$100", "retained\nbeta-prime"),
        ("Tensile", "$200", "strength"),
        ("1-hour\nscreen", "$50", "screen index"),
        ("30-day\nimmersion", "$400", "immersion\nindex"),
    ]
    inputs = ["Ni, Al, Fe, Mn", "atomizer setting", "power, speed", "power, speed", "", "", "", ""]
    fig, ax = plt.subplots(figsize=(17, 3.3))
    ax.set_xlim(0, 17)
    ax.set_ylim(-0.25, 3.0)
    ax.axis("off")
    w, h, gap = 1.72, 1.15, 0.36
    x0 = 0.2
    for i, ((name, cost, outp), inp) in enumerate(zip(stages, inputs)):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.95), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F2F2F2", ec="#A6A6A6", lw=1.2))
        ax.text(x + w / 2, 0.95 + h * 0.64, name, ha="center", va="center", fontsize=13, color=INK, linespacing=1.0)
        ax.text(x + w / 2, 0.95 + h * 0.17, cost, ha="center", va="center", fontsize=13 if len(cost) < 8 else 11.5, color=RED, fontweight="bold")
        ax.text(x + w / 2, 0.82, outp, ha="center", va="top", fontsize=10.5, color=MUTED, linespacing=1.05)
        if inp:
            ax.text(x + w / 2, 2.5, inp, ha="center", va="center", fontsize=11.5, color="#404040")
            ax.annotate("", xy=(x + w / 2, 0.95 + h), xytext=(x + w / 2, 2.33), arrowprops=dict(arrowstyle="->", color="#A6A6A6", lw=1.1))
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + w + gap - 0.03, 0.95 + h / 2), xytext=(x + w + 0.03, 0.95 + h / 2), arrowprops=dict(arrowstyle="->", color="#595959", lw=1.5))
    out = out or HERE / "bofn_cu_network_strip.png"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(dag_strip())
    if load(HEAD):
        print(slide_figure())
        (HERE / "variants").mkdir(exist_ok=True)
        print(slide_figure(out=HERE / "variants" / "bofn_cu_best_vs_spend_k1_partial_vs_full_all_bands.png", bands="all"))
        print(main_curve())
        print(allocation())
    for s in (100_000, 50_000):
        print(sensitivity(s))
