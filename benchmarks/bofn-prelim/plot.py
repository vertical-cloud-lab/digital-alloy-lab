"""Slide figures for the BOFN preliminary results (Aptos, red = pKGFN, grays = baselines)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

from analyze import GRID, NAMES, cost_to, curves, load, optimum
from policies import N_FULL0

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
    "pkgfn_la": dict(color=RED, lw=2.0, z=5, ls=(0, (4, 2))),
    "pkgfn_free": dict(color="#E06666", lw=2.4, z=5, ls=(0, (4, 2))),
    "eifn": dict(color="#404040", lw=2.0, z=4, ls="-"),
    "eifn_reuse": dict(color="#595959", lw=2.0, z=4, ls=(0, (4, 2))),
    "tiered": dict(color="#8C8C8C", lw=2.0, z=3, ls="-"),
    "tiered_naive": dict(color="#8C8C8C", lw=2.0, z=3, ls=(0, (4, 2))),
    "ei": dict(color="#B4B4B4", lw=2.0, z=2, ls="-"),
    "random": dict(color="#D0D0D0", lw=2.0, z=1, ls="-"),
}
SHORT = {
    "pkgfn": "pKGFN: picks the stage",
    "pkgfn_la": "pKGFN + lookahead",
    "pkgfn_free": "pKGFN, any alloy",
    "eifn": "BOFN, full pipeline",
    "eifn_reuse": "BOFN + powder reuse",
    "tiered": "Tiered screening",
    "tiered_naive": "Tiered, no powder reuse",
    "ei": "Standard BO",
    "random": "Random",
}


def main_curve(kappa=1.0, metric="best_validated", kinds=("pkgfn", "eifn", "tiered", "ei", "random"), out=None, annotate=True, style=None, short=None):
    style = {**STYLE, **(style or {})}
    short = {**SHORT, **(short or {})}
    ys = optimum(kappa)
    data = load(kappa)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    x = GRID / 1e3
    finals, C = {}, {}
    for k in kinds:
        if k not in data:
            continue
        c = curves(data[k], metric, ys) * 100
        C[k] = c
        m = np.nanmean(c, 0)
        se = np.nanstd(c, 0) / np.sqrt(c.shape[0])
        st = style[k]
        ax.fill_between(x, m - se, m + se, color=st["color"], alpha=0.14 if st["color"] == RED else 0.07, lw=0, zorder=st["z"])
        ax.plot(x, m, color=st["color"], lw=st["lw"], ls=st["ls"], zorder=st["z"] + 0.5, solid_capstyle="round")
        finals[k] = m[-1]
    # direct labels at the right end, nudged apart only if they collide
    order = sorted(finals, key=lambda k: finals[k])
    ypos, last = {}, -1e9
    for k in order:
        y = max(finals[k], last + 4.2)
        ypos[k], last = y, y
    for k in finals:
        ax.annotate(
            short[k], (x[-1], finals[k]), xytext=(x[-1] + 1.5, ypos[k]), textcoords="data",
            va="center", ha="left", fontsize=14, color=INK if style[k]["color"] == RED else "#404040",
            fontweight="bold" if style[k]["color"] == RED else "normal", annotation_clip=False,
        )
    ax.set_xlim(0, 100)
    ax.set_xlabel("New spend on experiments and simulations ($k)")
    ax.set_ylabel("Best alloy demonstrated\n(% of true optimum)")
    ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
    ax.set_axisbelow(True)
    if annotate and "pkgfn" in C:
        _speedup_arrow(ax, C, x)
    fig.tight_layout()
    fig.subplots_adjust(right=0.74)
    out = out or HERE / f"bofn_best_vs_spend_k{kappa:g}_{metric}.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def _speedup_arrow(ax, C, x, base="tiered"):
    """Arrow at the level `base` reaches by $100k, back to where pKGFN got there."""
    if base not in C:
        return
    target = np.nanmean(C[base][:, -1])
    mp = np.nanmean(C["pkgfn"], 0)
    mb = np.nanmean(C[base], 0)
    if not (mp >= target).any():
        return
    xp = x[np.argmax(mp >= target)]
    xb = x[np.argmax(mb >= target - 1e-9)]
    ax.annotate("", xy=(xp + 0.8, target), xytext=(xb - 0.8, target), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3, shrinkA=0, shrinkB=0), zorder=10)
    ax.text((xp + xb) / 2, target - 1.2, f"{xb / xp:.1f}× less spend", ha="center", va="top", fontsize=15, color=INK)


if __name__ == "__main__":
    kap = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    for m in ("best_validated", "rec_printed"):
        print(main_curve(kap, m))
    if kap == 1.0:
        print(slide_figure(1.0))
        (HERE / "variants").mkdir(exist_ok=True)
        print(slide_figure(1.0, out=HERE / "variants" / "bofn_best_vs_spend_k1_partial_vs_full_all_bands.png", bands="all"))


STAGE_COLORS = {"C": "#D9D9D9", "A": "#A6A6A6", "L": "#595959", "T": RED}
STAGE_NAMES = {"C": "CALPHAD", "A": "Atomize", "L": "Print (LPBF)", "T": "Tensile"}


def allocation(kappa=1.0, kinds=("pkgfn", "eifn", "tiered"), out=None):
    """How many of each stage every policy bought with the same budget (mean over seeds)."""
    from bofn_alloy import COSTS

    data = load(kappa)
    kinds = [k for k in kinds if k in data]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, grp in zip(axes, ("A", "L", "T")):
        # counts include the 5 shared seed alloys; report new purchases only
        vals = [np.mean([run["counts"][grp] for run in data[k]]) - N_FULL0 for k in kinds]
        y = np.arange(len(kinds))[::-1]
        ax.barh(y, vals, height=0.55, color=[STYLE[k]["color"] for k in kinds])
        for yi, v in zip(y, vals):
            ax.text(v + 0.4, yi, f"{v:.0f}", va="center", fontsize=14, color=INK)
        ax.set_title(f"{STAGE_NAMES[grp]} (${COSTS[grp]:,.0f})", fontsize=15, color=INK, loc="left")
        ax.set_yticks(y, [SHORT[k] for k in kinds])
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
    fig.tight_layout()
    out = out or HERE / f"bofn_allocation_k{kappa:g}.png"
    fig.savefig(out)
    plt.close(fig)
    return out



def dag_strip(out=None):
    """The benchmark network as a one-line chain: what each stage costs and returns."""
    from matplotlib.patches import FancyBboxPatch

    stages = [
        ("CALPHAD", "$10", "phase fraction,\nfreezing range,\nnucleant fraction"),
        ("Atomization", "$1,500", "powder quality\n(ultrasonic)"),
        ("LPBF print", "$2,500", "dense,\ncrack-free fraction"),
        ("Tensile test", "$200", "strength"),
    ]
    inputs = ["Zn+Mg, Cu, Zr, Sc", "atomizer setting", "laser power, scan speed", ""]
    fig, ax = plt.subplots(figsize=(12, 2.9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 2.9)
    ax.axis("off")
    w, h, gap = 2.3, 1.05, 0.75
    x0 = 0.35
    for i, ((name, cost, outp), inp) in enumerate(zip(stages, inputs)):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.95), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F2F2F2", ec="#A6A6A6", lw=1.2))
        ax.text(x + w / 2, 0.95 + h * 0.62, name, ha="center", va="center", fontsize=15, color=INK, linespacing=1.0)
        ax.text(x + w / 2, 0.95 + h * 0.2, cost, ha="center", va="center", fontsize=15, color=RED, fontweight="bold")
        ax.text(x + w / 2, 0.82, outp, ha="center", va="top", fontsize=12, color=MUTED, linespacing=1.05)
        if inp:
            ax.text(x + w / 2, 2.35, inp, ha="center", va="center", fontsize=12.5, color="#404040")
            ax.annotate("", xy=(x + w / 2, 0.95 + h), xytext=(x + w / 2, 2.18), arrowprops=dict(arrowstyle="->", color="#A6A6A6", lw=1.1))
        if i < 3:
            ax.annotate("", xy=(x + w + gap - 0.05, 0.95 + h / 2), xytext=(x + w + 0.05, 0.95 + h / 2), arrowprops=dict(arrowstyle="->", color="#595959", lw=1.6))
    out = out or HERE / "bofn_network_strip.png"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return out


def sensitivity(kappas=(0.0, 0.5, 1.0), at=50_000, kinds=("pkgfn", "eifn", "tiered", "ei"), metric="best_validated", out=None):
    """Value at a fixed spend as the CALPHAD screen gets more wrong (kappa)."""
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    i_at = int(np.searchsorted(GRID, at))
    xs = np.arange(len(kappas))
    ends = {}
    for k in kinds:
        m_, s_ = [], []
        for kap in kappas:
            data = load(kap)
            if k not in data:
                m_.append(np.nan), s_.append(np.nan)
                continue
            c = curves(data[k], metric, optimum(kap))[:, i_at] * 100
            m_.append(np.nanmean(c)), s_.append(np.nanstd(c) / np.sqrt(len(c)))
        st = STYLE[k]
        ax.errorbar(xs, m_, yerr=s_, color=st["color"], lw=st["lw"], marker="o", ms=8, mec="white", mew=2, capsize=0, zorder=st["z"])
        ends[k] = m_[-1]
    order = sorted(ends, key=lambda k: ends[k])
    last = -1e9
    for k in order:
        y = max(ends[k], last + 5)
        last = y
        ax.text(xs[-1] + 0.12, y, SHORT[k], va="center", fontsize=13.5, color=INK, fontweight="bold" if k == "pkgfn" else "normal")
    ax.set_xticks(xs, ["none", "half", "full"])
    ax.set_xlim(-0.25, len(kappas) - 0.75 + 0.1)
    ax.set_xlabel("Cracking effect of Zr/Sc that CALPHAD screening misses")
    ax.set_ylabel(f"Best alloy demonstrated at ${at / 1e3:.0f}k\n(% of true optimum)")
    ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.subplots_adjust(right=0.7)
    out = out or HERE / f"bofn_sensitivity_{metric}.png"
    fig.savefig(out)
    plt.close(fig)
    return out

# --------------------------------------------------------------------------- the headline figure
PV_KINDS = ("pkgfn", "eifn_reuse", "eifn", "ei", "tiered")
PV_STYLE = {"eifn_reuse": dict(color=RED, lw=2.4, z=5, ls=(0, (4, 2)))}
PV_SHORT = {"pkgfn": "Partial: pKGFN", "eifn_reuse": "Partial: BOFN + reuse", "eifn": "Full: BOFN", "ei": "Full: standard BO", "tiered": "Tiered screening"}


def partial_vs_full(kappa=1.0, out=None):
    """The slide figure as first posted (Oct 4): partial evaluation in red, full pipeline in gray, legend at the right."""
    return main_curve(kappa, "best_validated", PV_KINDS, out or HERE / f"bofn_best_vs_spend_k{kappa:g}_partial_vs_full.png", style=PV_STYLE, short=PV_SHORT)

# --------------------------------------------------------------------------- slide figure, Oct 5 restyle
FADE = {RED: "#E6B3B3", "#404040": "#BDBDBD", "#8C8C8C": "#CFCFCF", "#B4B4B4": "#D9D9D9", "#595959": "#C4C4C4", "#E06666": "#F2CCCC", "#D0D0D0": "#E6E6E6"}


def slide_figure(kappa=1.0, metric="best_validated", kinds=PV_KINDS, out=None, style=None, short=None, base="tiered", ref="pkgfn",
                 size=22, bands="highlight", figsize=(11, 6), right=0.655):
    """Best alloy vs spend for a slide: large type, leader lines instead of a legend (no arrowheads),
    a horizontal left-aligned y label, and ticks only at the axis ends plus the two called-out values
    (the spend at which `ref` reaches `base`'s $100k level, and that level)."""
    style = {**STYLE, **PV_STYLE, **(style or {})}
    short = {**PV_SHORT, **(short or {})}
    ys = optimum(kappa)
    data = load(kappa)
    x = GRID / 1e3
    C = {k: curves(data[k], metric, ys) * 100 for k in kinds if k in data}
    M = {k: np.nanmean(c, 0) for k, c in C.items()}
    SE = {k: np.nanstd(c, 0) / np.sqrt(c.shape[0]) for k, c in C.items()}
    # the two called-out values
    target = float(np.nanmean(C[base][:, -1]))
    x_ref = x[np.argmax(M[ref] >= target)]
    x_base = x[np.argmax(M[base] >= target - 1e-9)]
    start = float(M[ref][0])
    top = float(max(m[-1] for m in M.values()))
    y_lo, y_hi = start - 9, top + 4
    tick_lc, lab_c, ink = "#404040", "#404040", INK

    fig, ax = plt.subplots(figsize=figsize)
    for k in kinds:
        if k not in C:
            continue
        st = style[k]
        if bands == "all" or (bands == "highlight" and (st["color"] == RED or k == base)):
            ax.fill_between(x, M[k] - SE[k], M[k] + SE[k], color=st["color"], alpha=0.13 if st["color"] == RED else 0.07, lw=0, zorder=st["z"])
        ax.plot(x, M[k], color=st["color"], lw=st["lw"] + 0.4, ls=st["ls"], zorder=st["z"] + 0.5, solid_capstyle="round")
    # guides from the axes to the called-out point, then the spend line (no arrowheads)
    guide = dict(color="#BFBFBF", lw=0.9, ls=(0, (1.5, 2.5)), zorder=1)
    ax.plot([0, x_ref], [target, target], **guide)
    ax.plot([x_ref, x_ref], [y_lo, target], **guide)
    ax.plot([x_ref, x_base], [target, target], color=ink, lw=1.4, zorder=9, solid_capstyle="butt")
    ax.plot([x_ref], [target], "o", color=ink, ms=6, zorder=10)
    ax.text(x_base - 14, target + 1.4, f"{x_base / x_ref:.1f}× less spend", ha="center", va="bottom", fontsize=size + 2, color=ink, zorder=10)
    # leader lines to labels in the right margin, stacked so they never collide
    finals = {k: M[k][-1] for k in C}
    axes_h_pt = figsize[1] * (0.86 - 0.21) * 72  # must match subplots_adjust below
    gap = size * 1.35 * (y_hi - y_lo) / axes_h_pt  # one line of text plus leading, in data units
    order = sorted(finals, key=lambda k: finals[k])
    ypos, last = {}, -1e9
    for k in order:
        ypos[k] = max(finals[k], last + gap)
        last = ypos[k]
    # pull the stack down so it is centred on the traces it points to
    shift = (np.mean([ypos[k] - finals[k] for k in order]))
    for k in order:
        ypos[k] -= shift
    x_lab = 103.2
    for k in order:
        col = style[k]["color"]
        ax.plot([100.3, x_lab - 0.9], [finals[k], ypos[k]], color=FADE.get(col, "#CCCCCC"), lw=1.8, clip_on=False, zorder=1, solid_capstyle="round")
        ax.text(x_lab, ypos[k], short[k], ha="left", va="center", fontsize=size, color=RED if col == RED else lab_c, clip_on=False)
    # axes: ends plus the called-out values only
    ax.set_xlim(0, 100)
    ax.set_ylim(y_lo, y_hi)
    ax.set_xticks([0, x_ref, 100], ["0", f"{x_ref:g}", "100"])
    ax.set_yticks([start, target, top], [f"{start:.0f}", f"{target:.0f}", f"{top:.0f}"])
    ax.tick_params(axis="both", which="major", length=6, width=0.8, color="#8C8C8C", labelsize=size, labelcolor=tick_lc, pad=6)
    for side in ("left", "bottom"):  # detached spines that stop at the outermost tick
        ax.spines[side].set_position(("outward", 12))
    ax.spines["left"].set_bounds(start, top)
    ax.spines["bottom"].set_bounds(0, 100)
    ax.yaxis.grid(False)
    ax.set_xlabel("New spend ($k)", fontsize=size, color=lab_c, labelpad=10)
    ax.set_ylabel("")
    ax.text(-0.095, 1.03, "Best alloy demonstrated\n(% of true optimum)", transform=ax.transAxes, ha="left", va="bottom", fontsize=size, color=lab_c, linespacing=0.95)
    fig.subplots_adjust(left=0.095, right=right, top=0.86, bottom=0.21)
    out = out or HERE / f"bofn_best_vs_spend_k{kappa:g}_partial_vs_full.png"
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
        # sample densely along the polyline in display space
        pts = ax.transData.transform(xy)
        seg = np.concatenate([np.linspace(pts[k], pts[k + 1], 12) for k in range(len(pts) - 1)])
        for name, bb in boxes:
            if ((seg[:, 0] > bb.x0) & (seg[:, 0] < bb.x1) & (seg[:, 1] > bb.y0) & (seg[:, 1] < bb.y1)).any():
                out.append(f"a line ({ln.get_color()}, lw {ln.get_linewidth()}) passes through '{name}'")
    return out

