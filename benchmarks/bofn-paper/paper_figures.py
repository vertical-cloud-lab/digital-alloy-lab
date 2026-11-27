"""Figures for the BOFN methods write-ups (issue #121), drawn from the paper set.

    python paper_stats.py      # first: writes paper-stats/*.csv
    python paper_figures.py    # then: writes ../../bofn-methods-article/figures/*.{pdf,png}

Print-oriented: identity never rests on color alone. In the curve figures, hue is
the acquisition family (blue: KG per $, orange: EI per $, aqua: standard BO, grays:
screening and random) and the dash is the evaluation mode (solid: partial, dashed:
full chain); every line also ends in its own marker shape. In the interval figures
the bias level kappa is a light-to-dark gray ramp plus a marker shape.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from analyze import GRID, curve, optimum
from paper_stats import KAPPAS, LABEL, OUT as STATS, POLICIES, load_paper

HERE = Path(__file__).parent
FIG = HERE.parent.parent / "bofn-methods-article" / "figures"
TEXT, TEXT2, GRIDC = "#191919", "#666666", "#e6e6e6"
BLUE, ORANGE, AQUA = "#257de0", "#f47230", "#00b894"
STYLE = {
    "pkgfn": dict(color=BLUE, ls="-", marker="o"),
    "kgfn": dict(color=BLUE, ls=(0, (4, 2)), marker="o"),
    "eifn_reuse": dict(color=ORANGE, ls="-", marker="s"),
    "eifn": dict(color=ORANGE, ls=(0, (4, 2)), marker="s"),
    "ei": dict(color=AQUA, ls="-", marker="D"),
    "tiered": dict(color="#404040", ls="-", marker="^"),
    "tiered_naive": dict(color="#404040", ls=(0, (4, 2)), marker="^"),
    "random": dict(color="#a6a6a6", ls="-", marker="v"),
}
KSTYLE = {0.0: dict(color="#a6a6a6", marker="o"), 0.5: dict(color="#666666", marker="s"), 1.0: dict(color="#191919", marker="D")}
KNAME = {0.0: "κ = 0 (screen right)", 0.5: "κ = 0.5", 1.0: "κ = 1 (screen misses the inoculant effect)"}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "axes.edgecolor": "#8c8c8c", "axes.linewidth": 0.6, "axes.labelcolor": TEXT, "text.color": TEXT,
    "xtick.color": TEXT2, "ytick.color": TEXT2, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 300, "pdf.fonttype": 42,
    "lines.solid_capstyle": "round", "lines.dash_capstyle": "round",
})


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"{name}.{ext}", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {FIG / name}.pdf/png")


def read_csv(name):
    with open(STATS / f"{name}.csv") as f:
        return list(csv.DictReader(f))


def matched_curves(kappa):
    runs = load_paper(kappa)
    seeds = sorted(set.intersection(*(set(v) for v in runs.values())))
    ys = optimum(kappa)
    return {p: np.stack([curve(runs[p][s]["rows"], "best_validated") / ys for s in seeds]) for p in POLICIES}, seeds


def fig_curves(kinds, name, bands=("pkgfn", "eifn_reuse", "tiered"), labels=LABEL, xlab="New spend ($k)", ylab="Best alloy demonstrated\n(% of optimum)"):
    """Best alloy demonstrated vs new spend, one panel per kappa (mean over matched seeds).
    Bands: 95% bootstrap interval of the mean (seeds resampled), for the policies in `bands`."""
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.55), sharey=True)
    rng = np.random.default_rng(0)
    for ax, k in zip(axes, KAPPAS):
        C, seeds = matched_curves(k)
        x = GRID / 1000
        idx = rng.integers(0, len(seeds), size=(2000, len(seeds)))
        for p in kinds:
            st = STYLE[p]
            m = 100 * C[p].mean(0)
            if p in bands:
                bs = 100 * C[p][idx].mean(1)
                lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
                ax.fill_between(x, lo, hi, color=st["color"], alpha=0.10, lw=0, zorder=1)
            ax.plot(x, m, color=st["color"], ls=st["ls"], lw=1.4, zorder=3, label=labels[p])
            ax.plot(x[-1], m[-1], marker=st["marker"], ms=4.5, color=st["color"], mec="white", mew=0.8, zorder=4, ls="none")
        sub = {0.0: "screen right", 0.5: "screen half wrong", 1.0: "screen misses the effect"}[k]
        ax.set_title(f"κ = {k:g}: {sub}\n{len(seeds)} matched seeds", color=TEXT, loc="left", fontsize=8)
        ax.set_xlim(0, 101)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel(xlab)
        ax.grid(axis="y", color=GRIDC, lw=0.6)
        ax.set_axisbelow(True)
    axes[0].set_ylabel(ylab)
    handles = [plt.Line2D([], [], color=STYLE[p]["color"], ls=STYLE[p]["ls"], lw=1.4, marker=STYLE[p]["marker"], ms=4.5, mec="white", mew=0.8, label=labels[p]) for p in kinds]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=min(4, len(kinds)), frameon=False, handlelength=2.8, columnspacing=1.4, numpoints=1)
    save(fig, name)


def fig_contrasts(name="fig-contrasts"):
    """Forest plot: the four contrasts of the 2 x 2 at $25k, $100k and over the whole budget."""
    rows = read_csv("contrasts")
    names = ["partial - full, KG", "partial - full, EI", "KG - EI, partial", "KG - EI, full chain"]
    nice = {"partial - full, KG": "Partial − full chain\nunder KG per $\n(pKGFN − KGFN)",
            "partial - full, EI": "Partial − full chain\nunder EI per $\n(BOFN+reuse − BOFN)",
            "KG - EI, partial": "KG − EI per $,\npartial\n(pKGFN − BOFN+reuse)",
            "KG - EI, full chain": "KG − EI per $,\nfull chain\n(KGFN − BOFN)"}
    metrics = (("v25", "At $25k"), ("v100", "At $100k"), ("auc", "Anytime ($0–100k mean)"))
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 3.1), sharey=True)
    for ax, (m, title) in zip(axes, metrics):
        for i, c in enumerate(names):
            for j, k in enumerate(KAPPAS):
                r = next(r for r in rows if r["contrast"] == c and float(r["kappa"]) == k)
                y = i + (j - 1) * 0.22
                d, lo, hi = (100 * float(r[f"{m}_{s}"]) for s in ("diff", "lo", "hi"))
                st = KSTYLE[k]
                ax.plot([lo, hi], [y, y], color=st["color"], lw=1.2, solid_capstyle="butt", zorder=2)
                ax.plot(d, y, marker=st["marker"], ms=4.2, color=st["color"], mec="white", mew=0.7, zorder=3, ls="none")
        ax.axvline(0, color="#8c8c8c", lw=0.7, zorder=1)
        ax.set_title(title, loc="left", color=TEXT)
        ax.set_xlabel("Difference (percentage points)")
        ax.grid(axis="x", color=GRIDC, lw=0.6)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(names)))
    axes[0].set_yticklabels([nice[c] for c in names], fontsize=7)
    axes[0].invert_yaxis()
    handles = [plt.Line2D([], [], color=KSTYLE[k]["color"], marker=KSTYLE[k]["marker"], ms=4.2, mec="white", mew=0.7, lw=1.2, label=KNAME[k]) for k in KAPPAS]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.55, 1.06), ncol=3, frameon=False, numpoints=1)
    save(fig, name)


def fig_speedup(name="fig-speedup", over="tiered", labels=LABEL, base=None):
    """Spend the baseline needs to reach its own $100k mean, over the policy's spend; 95% matched CI."""
    rows = [r for r in read_csv("speedup") if r["over"] == over]
    kinds = [p for p in POLICIES if p != over]
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    lo_edge = 0.2
    for i, p in enumerate(kinds):
        for j, k in enumerate(KAPPAS):
            r = next(r for r in rows if r["policy"] == p and float(r["kappa"]) == k)
            y = i + (j - 1) * 0.22
            est, lo, hi = float(r["est"]), float(r["lo95"]), float(r["hi95"])
            st = KSTYLE[k]
            lo_p, hi_p = max(lo, lo_edge), max(hi, lo_edge)
            ax.plot([lo_p, hi_p], [y, y], color=st["color"], lw=1.2, solid_capstyle="butt", zorder=2)
            if est > 0:
                ax.plot(est, y, marker=st["marker"], ms=4.2, color=st["color"], mec="white", mew=0.7, zorder=3, ls="none")
            else:  # mean curve never reached the target within $100k
                ax.plot(lo_edge, y, marker="<", ms=4.2, color=st["color"], zorder=3, ls="none")
    ax.set_xscale("log")
    ax.set_xlim(lo_edge * 0.9, 10)
    ax.set_xticks([0.25, 0.5, 1, 2, 4, 8])
    ax.set_xticklabels(["0.25×", "0.5×", "1×", "2×", "4×", "8×"])
    ax.axvline(1, color="#8c8c8c", lw=0.7, zorder=1)
    ax.set_yticks(range(len(kinds)))
    ax.set_yticklabels([labels[p] for p in kinds], fontsize=7)
    ax.invert_yaxis()
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRIDC, lw=0.6)
    ax.set_axisbelow(True)
    base = base or ("tiered screening" if over == "tiered" else "standard BO")
    ax.set_xlabel(f"Speed-up over {base} (spend ratio to reach {base}'s $100k level)")
    handles = [plt.Line2D([], [], color=KSTYLE[k]["color"], marker=KSTYLE[k]["marker"], ms=4.2, mec="white", mew=0.7, lw=1.2, label=f"κ = {k:g}") for k in KAPPAS]
    handles.append(plt.Line2D([], [], color=TEXT2, marker="<", ms=4.2, lw=0, label="mean never reached it"))
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.35, 1.0), ncol=4, frameon=False, fontsize=7, numpoints=1, handlelength=1.6, columnspacing=1.0)
    save(fig, name)


def fig_allocation(name="fig-allocation"):
    """Where the money went: mean new spend per stage, per policy and kappa."""
    rows = read_csv("allocation")
    costs = {"C": 10, "A": 1500, "L": 2500, "T": 200}
    stage = {"C": "CALPHAD", "A": "Atomize", "L": "Print", "T": "Tensile"}
    ramp = {"C": "#d9d9d9", "A": "#a6a6a6", "L": "#666666", "T": "#262626"}
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.7), sharey=True)
    for ax, k in zip(axes, KAPPAS):
        for i, p in enumerate(POLICIES):
            r = next(r for r in rows if r["policy"] == p and float(r["kappa"]) == k)
            left = 0.0
            for g in "CALT":
                w = float(r[f"{g}_mean"]) * costs[g] / 1000
                if w > 0:
                    ax.barh(i, max(w - 0.35, 0.05), left=left, height=0.62, color=ramp[g], lw=0)
                left += w
        ax.set_title(f"κ = {k:g}", loc="left", color=TEXT)
        ax.set_xlim(0, 102)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("Mean new spend ($k)")
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(POLICIES)))
    axes[0].set_yticklabels([LABEL[p] for p in POLICIES], fontsize=7)
    axes[0].invert_yaxis()
    handles = [plt.Rectangle((0, 0), 1, 1, color=ramp[g], label=f"{stage[g]} (${costs[g]:,})") for g in "CALT"]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.6, 1.07), ncol=4, frameon=False)
    save(fig, name)


def graphical_abstract(name="graphical-abstract"):
    """MethodsX graphical abstract: landscape, at least 1328 x 531 px (w x h).
    Left: the network with its step costs. Right: speed-up over tiered screening for
    the 2 x 2 of policies at each kappa (95% matched-seed intervals)."""
    import matplotlib.image as mpimg

    rows = [r for r in read_csv("speedup") if r["over"] == "tiered"]
    kinds = ("pkgfn", "eifn_reuse", "kgfn", "eifn")
    fig = plt.figure(figsize=(13.28, 5.31))
    ax0 = fig.add_axes([0.0, 0.02, 0.56, 0.86])
    ax0.imshow(mpimg.imread(FIG / "fig-network.png"))
    ax0.axis("off")
    fig.text(0.01, 0.95, "A synthetic alloy powder-to-part workflow with a known optimum", fontsize=15, color=TEXT, weight="bold")
    fig.text(0.01, 0.895, "κ sets how badly the cheap crack screen misjudges the best alloys (Zr/Sc nucleants)", fontsize=12, color=TEXT2)
    ax = fig.add_axes([0.73, 0.16, 0.255, 0.66])
    lo_edge = 0.2
    for i, p in enumerate(kinds):
        for j, k in enumerate(KAPPAS):
            r = next(r for r in rows if r["policy"] == p and float(r["kappa"]) == k)
            y = i + (j - 1) * 0.24
            est, lo, hi = float(r["est"]), float(r["lo95"]), float(r["hi95"])
            st = KSTYLE[k]
            ax.plot([max(lo, lo_edge), max(hi, lo_edge)], [y, y], color=st["color"], lw=2.2, solid_capstyle="butt")
            if est > 0:
                ax.plot(est, y, marker=st["marker"], ms=8, color=st["color"], mec="white", mew=1.2, ls="none")
            else:
                ax.plot(lo_edge, y, marker="<", ms=8, color=st["color"], ls="none")
    ax.set_xscale("log")
    ax.set_xlim(lo_edge * 0.9, 10)
    ax.set_xticks([0.25, 1, 4])
    ax.set_xticklabels(["0.25×", "1×", "4×"], fontsize=12)
    ax.axvline(1, color="#8c8c8c", lw=1.0)
    ax.set_yticks(range(len(kinds)))
    names = {"pkgfn": "pKGFN\n(KG, partial)", "eifn_reuse": "BOFN + reuse\n(EI/$, partial)", "kgfn": "KGFN\n(KG, full chain)", "eifn": "BOFN\n(EI, full chain)"}
    ax.set_yticklabels([names[p] for p in kinds], fontsize=11.5)
    ax.invert_yaxis()
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRIDC, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Speed-up over screen-then-test\n(95% matched-seed interval)", fontsize=12)
    fig.text(0.60, 0.88, "Does choosing the step pay?", fontsize=15, color=TEXT, weight="bold")
    handles = [plt.Line2D([], [], color=KSTYLE[k]["color"], marker=KSTYLE[k]["marker"], ms=8, mec="white", mew=1.2, lw=2.2,
                          label={0.0: "κ = 0: screen right", 0.5: "κ = 0.5", 1.0: "κ = 1: screen wrong"}[k]) for k in KAPPAS]
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.60, 0.80), ncol=3, frameon=False, fontsize=11, numpoints=1,
               handlelength=1.6, columnspacing=1.0)
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.png", dpi=200, facecolor="white")
    fig.savefig(FIG / f"{name}.pdf", facecolor="white")
    plt.close(fig)
    print(f"wrote {FIG / name}.png ({int(13.28 * 200)} x {int(5.31 * 200)} px)")


if __name__ == "__main__":
    main6 = ("pkgfn", "kgfn", "eifn_reuse", "eifn", "ei", "tiered")
    fig_curves(main6, "fig-curves")
    fig_curves(POLICIES, "fig-curves-all", bands=())
    fig_contrasts()
    fig_speedup()
    fig_speedup(name="fig-speedup-over-bo", over="ei")
    fig_allocation()
    graphical_abstract()
    # Advanced Materials versions: the article's wording (screen-then-test) and axis labels as "Quantity [unit]"
    am = dict(LABEL, tiered="Screen-then-test", tiered_naive="Screen-then-test, no powder reuse")
    fig_curves(main6, "fig-curves-am", labels=am, xlab="New spend [k$]", ylab="Best alloy demonstrated\n[% of optimum]")
    fig_speedup(name="fig-speedup-am", labels=am, base="screen-then-test")
