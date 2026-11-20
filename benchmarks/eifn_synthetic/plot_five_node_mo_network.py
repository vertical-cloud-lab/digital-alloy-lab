#!/usr/bin/env python3
"""Figure for the 5-node multi-objective function network (issue #265).

Left: the objectives of 2,000 random feasible inputs (those with f2 <= 4.5),
the known Pareto front f2 = 1 - sqrt(f1), three of ZDT4's local fronts, and the
objectives of 15 inputs from ``gen_pareto_set``.
Right: hypervolume regret of Sobol random search against the number of
evaluations (mean of 5 seeds, reference point (11, 11)).

Usage (from the repository root):

    python benchmarks/eifn_synthetic/plot_five_node_mo_network.py
"""

from __future__ import annotations

import math
import os
import sys
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import torch  # noqa: E402

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from botorch.utils.multi_objective.hypervolume import Hypervolume  # noqa: E402
from botorch.utils.multi_objective.pareto import is_non_dominated  # noqa: E402
from botorch.utils.sampling import draw_sobol_samples  # noqa: E402

from benchmarks.eifn_synthetic import FiveNodeMOFunctionNetwork  # noqa: E402

warnings.filterwarnings("ignore")

# reference palette (light surface), first three categorical slots
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"

OUT = os.path.join(os.path.dirname(__file__), "figures", "five_node_mo_network.png")


def random_search_regret(problem, sizes, seeds=range(5)):
    hv = Hypervolume(ref_point=problem.ref_point)
    regret = []
    for n in sizes:
        values = []
        for seed in seeds:
            X = draw_sobol_samples(problem.feasible_bounds, n=n, q=1, seed=seed).squeeze(-2)
            F = problem(X)
            values.append(problem.max_hv - hv.compute(F[is_non_dominated(F)]))
        regret.append(sum(values) / len(values))
    return regret


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_2)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=INK_2, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def main() -> None:
    problem = FiveNodeMOFunctionNetwork()  # minimisation, for plotting
    X = draw_sobol_samples(problem.feasible_bounds, n=2000, q=1, seed=0).squeeze(-2)
    F = problem(X)
    front = problem.gen_pareto_front(400)
    F_set = problem(problem.gen_pareto_set(15))

    sizes = [21, 42, 100, 300, 1000, 4096, 20000]
    regret = random_search_regret(FiveNodeMOFunctionNetwork(negate=True), sizes)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 5.0), gridspec_kw={"width_ratios": [1.25, 1]})
    fig.patch.set_facecolor(SURFACE)

    # left: objective space
    style(ax1)
    y_max = 4.5  # the front and the first local fronts; most random inputs sit higher
    t = torch.linspace(0, 1, 200, dtype=torch.double)
    for g in (1.25, 2.0, 3.25):  # ZDT4 local fronts (u2 near +-0.5, +-1, +-1.5)
        ax1.plot(t, g - (t * g).sqrt(), color=INK_2, lw=0.8, ls=(0, (3, 3)), zorder=1)
    ax1.text(0.02, 3.25 - 0.02, "ZDT4 local fronts", color=INK_2, fontsize=8.5, va="bottom")
    shown = F[:, 1] <= y_max
    ax1.scatter(F[shown, 0], F[shown, 1], s=7, color=BLUE, alpha=0.45, linewidths=0, zorder=2,
                label=f"2,000 random feasible inputs ({int((~shown).sum()):,} with $f_2$ > {y_max:g} not shown)")
    ax1.plot(front[:, 0], front[:, 1], color=ORANGE, lw=2, zorder=3, label=r"known Pareto front $f_2 = 1 - \sqrt{f_1}$")
    ax1.scatter(F_set[:, 0], F_set[:, 1], s=36, color=AQUA, edgecolors=SURFACE, linewidths=1.5, zorder=4,
                label="15 inputs from gen_pareto_set")
    ax1.set_xlim(-0.02, 1.02)
    ax1.set_ylim(-0.1, y_max)
    ax1.set_xlabel("objective 1, $f_1 = x_1$ (minimized)", color=INK, fontsize=10)
    ax1.set_ylabel("objective 2, $f_2$ (minimized)", color=INK, fontsize=10)
    ax1.set_title("Node 5 outputs: random inputs vs. the known front", color=INK, fontsize=11, loc="left")
    leg = ax1.legend(loc="upper left", bbox_to_anchor=(0.0, -0.17), fontsize=8.5, frameon=False, ncol=1)
    for text in leg.get_texts():
        text.set_color(INK)

    # right: random-search regret
    style(ax2)
    ax2.plot(sizes, regret, color=BLUE, lw=2, marker="o", ms=5, markeredgecolor=SURFACE, markeredgewidth=1.2)
    for n, r in zip(sizes, regret):
        if n in (42, 1000, 20000):
            ax2.annotate(f"{r:.2f}", (n, r), textcoords="offset points", xytext=(6, 6), color=INK, fontsize=8.5)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("random feasible inputs evaluated", color=INK, fontsize=10)
    ax2.set_ylabel("hypervolume regret", color=INK, fontsize=10)
    ax2.set_title("Random search, ref. point (11, 11), max HV 120.67", color=INK, fontsize=11, loc="left")

    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, dpi=160, facecolor=SURFACE)
    print(f"saved {OUT}")
    print("regret:", {n: round(r, 3) for n, r in zip(sizes, regret)})


if __name__ == "__main__":
    main()
