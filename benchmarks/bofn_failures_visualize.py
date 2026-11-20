#!/usr/bin/env python3
"""Figure for the #274 toy study (bofn_failures_demo.py).

Two small multiples, node 0 with 2 inputs and with 6: simple regret against BO run for the five
ways of handling a failed run, as the median over seeds with an interquartile band.

    python benchmarks/bofn_failures_visualize.py
reads benchmarks/bofn_failures_results.json and bofn_failures_results_dim6.json and writes
benchmarks/figures/bofn_failures_regret.png.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
INPUTS = [
    (HERE / "bofn_failures_results.json", "Node 0 takes 2 inputs"),
    (HERE / "bofn_failures_results_dim6.json", "Node 0 takes 6 inputs"),
]
OUT = HERE / "figures" / "bofn_failures_regret.png"

# Reference categorical palette, light mode, slots 1-5 in fixed order (validated with the
# dataviz skill's validate_palette.js: all gates pass; aqua, yellow and magenta are below 3:1
# on the surface, so every line also carries a direct label and the note has a table).
SERIES = {
    "drop": ("#2a78d6", "drop: whole run discarded (Ax ≤ 1.2.3 FAILED)"),
    "abandon": ("#eb6834", "abandon: discarded, pending for good"),
    "partial": ("#1baf7a", "partial: node 0 data kept (Ax ≥ 1.2.4)"),
    "viability_x": ("#eda100", "viability_x: P(viable | x), Ax 1.3"),
    "viability_node": ("#e87ba4", "viability_node: P(viable | node 1 inputs)"),
}
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e6e5e1"


def curves(path: Path) -> tuple[dict, dict]:
    data = json.loads(path.read_text())
    n_init = data["settings"]["N_INIT"]
    out = {}
    for s in SERIES:
        runs = [r for r in data["runs"] if r["strategy"] == s]
        # regret after the initial design and after each BO run (index 0 = end of the design)
        R = np.array([r["regret_curve"][n_init - 1 :] for r in runs], dtype=float)
        out[s] = R
    return out, data["settings"]


def spread_labels(ys: list[float], min_gap: float) -> list[float]:
    """Nudge label positions (in log10 units) apart so no two are closer than min_gap."""
    order = np.argsort(ys)
    placed = np.array(ys, dtype=float)[order]
    for i in range(1, len(placed)):
        placed[i] = max(placed[i], placed[i - 1] + min_gap)
    shift = (placed.mean() - np.array(ys)[order].mean())  # keep the group centred
    placed -= shift
    res = np.empty_like(placed)
    res[order] = placed
    return list(res)


def main() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.edgecolor": GRID, "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_SECONDARY, "ytick.color": TEXT_SECONDARY,
    })
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), sharey=True, facecolor=SURFACE)
    for ax, (path, title) in zip(axes, INPUTS):
        cs, settings = curves(path)
        ax.set_facecolor(SURFACE)
        ends = {}
        for s, (color, _) in SERIES.items():
            R = np.clip(cs[s], 1e-4, None)
            x = np.arange(R.shape[1])
            med = np.median(R, axis=0)
            lo, hi = np.percentile(R, 25, axis=0), np.percentile(R, 75, axis=0)
            ax.fill_between(x, lo, hi, color=color, alpha=0.10, linewidth=0)
            ax.plot(x, med, color=color, linewidth=2, solid_capstyle="round", solid_joinstyle="round")
            ax.plot(x[-1], med[-1], "o", markersize=8, color=color,
                    markeredgecolor=SURFACE, markeredgewidth=2, zorder=5)
            ends[s] = med[-1]
        # direct labels at the line ends, nudged apart, in text ink with the colored dot beside
        names = list(ends)
        ys = spread_labels([np.log10(ends[s]) for s in names], min_gap=0.11)
        xmax = len(next(iter(cs.values()))[0]) - 1
        for s, y in zip(names, ys):
            ax.annotate(f"{s}  {ends[s]:.3f}", xy=(xmax, ends[s]), xytext=(xmax + 1.2, 10**y),
                        va="center", fontsize=8.5, color=TEXT_PRIMARY, annotation_clip=False,
                        arrowprops=dict(arrowstyle="-", color=GRID, linewidth=1))
        ax.set_yscale("log")
        ax.set_xlim(0, xmax)
        ax.set_ylim(2e-3, 1.0)
        ax.grid(True, which="major", color=GRID, linewidth=1, linestyle="-")
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_title(f"{title} (initial design {settings['N_INIT']} runs)",
                     fontsize=10.5, color=TEXT_PRIMARY, loc="left")
        ax.set_xlabel("BO runs after the initial design")
    axes[0].set_ylabel("simple regret (f* − best feasible y1)")
    handles = [plt.Line2D([], [], color=c, linewidth=2, marker="o", markersize=7,
                          markeredgecolor=SURFACE, markeredgewidth=1.5) for c, _ in SERIES.values()]
    fig.legend(handles, [lab for _, lab in SERIES.values()], loc="upper center", ncol=3,
               frameon=False, fontsize=9, labelcolor=TEXT_PRIMARY, bbox_to_anchor=(0.5, 0.995))
    fig.text(0.01, 0.005,
             "Toy 2-node network, node 1 fails when y0 > 0.7; 15% transient failures per node. "
             "Lines: median over 12 seeds; bands: interquartile range. Lower is better.",
             fontsize=8, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.07, right=0.87, top=0.80, bottom=0.14, wspace=0.40)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=160, facecolor=SURFACE)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
