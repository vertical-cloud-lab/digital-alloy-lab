#!/usr/bin/env python3
"""Brute-force check of the Pareto front of ``FiveNodeMOFunctionNetwork`` (issue #265).

The module docstring of ``five_node_mo_network.py`` derives the front analytically:
``f2 = 1 - sqrt(f1)`` for ``f1`` in ``[0, 1]`` (both objectives minimized). This script
finds the front numerically from the 20 network inputs, without using that derivation, in
three independent ways, and only then compares the result with the analytic curve:

1. Dense sampling. ``2^27`` (134 million) scrambled-Sobol inputs in ``feasible_bounds``.
   It keeps their non-dominated set, the smallest gap ``f2 - (1 - sqrt(f1))`` in each of
   1,000 bins of ``f1``, and the smallest gap of any input.
2. Slice minimization. At 101 values of ``x1`` (``f1 = x1``), it minimizes ``f2`` over
   x2..x20 with L-BFGS-B (exact gradients by autograd), from 128 random starts each, each
   start a separate run.
3. A black-box multi-objective optimizer. NSGA-II (pymoo) on all 20 inputs, 5 seeds of
   500 generations of 200, so 100,000 evaluations each.

A negative gap would be an input that beats the analytic front; a gap that stays well
above 0 over some range of ``f1`` would be a part of the curve the network can't reach.

Usage (from the repository root, about 7 minutes on 4 CPU cores):

    python benchmarks/eifn_synthetic/brute_force_pareto_front.py

Writes ``brute_force_pareto_front.json`` (the numbers) and
``figures/brute_force_pareto_front.png`` next to this file. Needs ``pymoo`` for step 3.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
from scipy.optimize import minimize  # noqa: E402
from torch.quasirandom import SobolEngine  # noqa: E402

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from benchmarks.eifn_synthetic import FiveNodeMOFunctionNetwork  # noqa: E402

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "brute_force_pareto_front.json")
OUT_PNG = os.path.join(HERE, "figures", "brute_force_pareto_front.png")

# reference palette (light surface), first three categorical slots
SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"

GAP_FLOOR = 1e-16  # gaps at or below this (rounding) are drawn at this value on the log axis


def analytic_f2(f1: torch.Tensor) -> torch.Tensor:
    """The analytic front, used only to score what the searches found."""
    return 1 - f1.clamp(min=0).sqrt()


def pareto_filter(F: torch.Tensor) -> torch.Tensor:
    """Non-dominated rows of ``F`` (n x 2, both minimized), sorted by f1."""
    F = F[torch.argsort(F[:, 1], stable=True)]
    F = F[torch.argsort(F[:, 0], stable=True)]  # by f1, ties by f2
    best_before = torch.cummin(F[:, 1], dim=0).values
    best_before = torch.cat([best_before.new_full((1,), math.inf), best_before[:-1]])
    return F[F[:, 1] < best_before]


def hypervolume_2d(F: torch.Tensor, ref=(11.0, 11.0)) -> float:
    """Hypervolume (minimization) of a 2-objective set."""
    P = pareto_filter(F)
    P = P[(P[:, 0] < ref[0]) & (P[:, 1] < ref[1])]
    if len(P) == 0:
        return 0.0
    right = torch.cat([P[1:, 0], P.new_full((1,), ref[0])])
    return float(((right - P[:, 0]) * (ref[1] - P[:, 1])).sum())


# --------------------------------------------------------------- 1. sampling


def dense_sampling(problem, log2_n: int, log2_chunk: int = 20, n_bins: int = 1000, seed: int = 0):
    lo, hi = problem.feasible_bounds
    engine = SobolEngine(problem.dim, scramble=True, seed=seed)
    n_chunks = 2 ** max(log2_n - log2_chunk, 0)
    chunk = 2 ** min(log2_chunk, log2_n)
    bin_gap = torch.full((n_bins,), math.inf, dtype=torch.double)
    archive = torch.empty(0, 2, dtype=torch.double)
    min_gap, min_gap_point = math.inf, None
    n_within = {1e-2: 0, 1e-3: 0, 1e-4: 0}
    cloud = None
    for i in range(n_chunks):
        X = lo + (hi - lo) * engine.draw(chunk, dtype=torch.double)
        with torch.no_grad():
            F = problem(X)
        gap = F[:, 1] - analytic_f2(F[:, 0])
        k = int(gap.argmin())
        if gap[k] < min_gap:
            min_gap, min_gap_point = float(gap[k]), F[k].tolist()
        for eps in n_within:
            n_within[eps] += int((gap <= eps).sum())
        b = (F[:, 0] * n_bins).long().clamp(0, n_bins - 1)
        bin_gap = bin_gap.scatter_reduce(0, b, gap, reduce="amin")
        archive = pareto_filter(torch.cat([archive, pareto_filter(F)]))
        if cloud is None:
            cloud = F[:4000].clone()
    n = n_chunks * chunk
    return {
        "n_inputs": n,
        "archive": archive,
        "bin_gap": bin_gap,
        "cloud": cloud,
        "min_gap": min_gap,
        "min_gap_point": min_gap_point,
        "fraction_within": {f"{eps:g}": c / n for eps, c in n_within.items()},
    }


# ------------------------------------------------------- 2. slice minimization


def slice_minimization(problem, n_slices: int, n_starts: int, seed: int = 0):
    """At each of ``n_slices`` values of x1, minimize f2 over x2..x20 from ``n_starts``
    random starts. Each start is its own L-BFGS-B run: one run over all starts at once
    (BoTorch's batch trick) shares one line search, and a single stiff start then stalls
    the rest."""
    lo, hi = problem.feasible_bounds[0, 1:], problem.feasible_bounds[1, 1:]
    d = problem.dim - 1
    gen = torch.Generator().manual_seed(seed)
    scipy_bounds = list(zip(lo.tolist(), hi.tolist()))
    n_threads = torch.get_num_threads()
    torch.set_num_threads(1)  # one 20-D point at a time: threads only add overhead
    rows = []
    for t in torch.linspace(0, 1, n_slices, dtype=torch.double).tolist():
        # sqrt(f1 / g) in ZDT4 has an infinite derivative at f1 = 0, so x1 = 0 is run at 1e-12
        x1 = torch.tensor([max(t, 1e-12)], dtype=torch.double)

        def f2(z: np.ndarray):
            Z = torch.from_numpy(z).requires_grad_(True)
            value = problem(torch.cat([x1, Z]).unsqueeze(0))[0, 1]
            (grad,) = torch.autograd.grad(value, Z)
            return value.detach().item(), grad.numpy()

        Z0 = lo + (hi - lo) * torch.rand(n_starts, d, generator=gen, dtype=torch.double)
        ends, n_evals = [], 0
        for z0 in Z0.numpy():
            res = minimize(f2, z0, jac=True, method="L-BFGS-B", bounds=scipy_bounds,
                           options={"maxiter": 1000, "ftol": 1e-15, "gtol": 1e-11})
            ends.append(res.x)
            n_evals += res.nfev
        X = torch.cat([x1.expand(n_starts, 1), torch.from_numpy(np.stack(ends))], dim=-1)
        with torch.no_grad():
            F = problem(X)
        gap = F[:, 1] - analytic_f2(F[:, 0])
        k = int(gap.argmin())
        rows.append(
            {
                "x1": float(x1),
                "f1": float(F[k, 0]),
                "f2": float(F[k, 1]),
                "gap": float(gap[k]),
                "starts_within_1e-6": int((gap <= 1e-6).sum()),
                "evaluations": n_evals,
            }
        )
    torch.set_num_threads(n_threads)
    return rows


# ------------------------------------------------------------- 3. NSGA-II


def nsga2(problem, seeds, n_gen: int, pop_size: int):
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.config import Config
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize as pymoo_minimize

    Config.warnings["not_compiled"] = False
    lo, hi = problem.feasible_bounds.numpy()

    class Network(Problem):
        def __init__(self):
            super().__init__(n_var=problem.dim, n_obj=2, xl=lo, xu=hi)

        def _evaluate(self, x, out, *args, **kwargs):
            with torch.no_grad():
                out["F"] = problem(torch.from_numpy(np.ascontiguousarray(x))).numpy()

    runs = []
    for seed in seeds:
        res = pymoo_minimize(Network(), NSGA2(pop_size=pop_size), ("n_gen", n_gen), seed=seed, verbose=False)
        F = pareto_filter(torch.from_numpy(np.asarray(res.F, dtype=np.float64)))
        gap = F[:, 1] - analytic_f2(F[:, 0])
        runs.append({"seed": seed, "front": F, "gap": gap})
    return runs


# ------------------------------------------------------------------- figure


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


def plot(dense, slices, runs, out=OUT_PNG):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.2), gridspec_kw={"width_ratios": [1, 1.15]})
    fig.patch.set_facecolor(SURFACE)
    n_m = dense["n_inputs"] / 1e6

    # left: what the brute force finds in objective space
    style(ax1)
    y_max = 1.6
    cloud = dense["cloud"][dense["cloud"][:, 1] <= y_max]
    ax1.scatter(cloud[:, 0], cloud[:, 1], s=6, color=MUTED, alpha=0.35, linewidths=0, zorder=1,
                label=f"random feasible inputs ({len(cloud):,} of the first 4,000, $f_2 \\leq$ {y_max:g})")
    A = dense["archive"]
    ax1.scatter(A[:, 0], A[:, 1], s=9, color=BLUE, linewidths=0, zorder=2,
                label=f"non-dominated set of all {n_m:,.0f} million inputs ({len(A):,} points)")
    t = torch.linspace(0, 1, 400, dtype=torch.double)
    ax1.plot(t, analytic_f2(t), color=INK, lw=1.2, ls=(0, (4, 3)), zorder=3,
             label=r"analytic front $f_2 = 1 - \sqrt{f_1}$")
    ax1.set_xlim(-0.02, 1.02)
    ax1.set_ylim(-0.05, y_max)
    ax1.set_xlabel("objective 1, $f_1 = x_1$ (minimized)", color=INK, fontsize=10)
    ax1.set_ylabel("objective 2, $f_2$ (minimized)", color=INK, fontsize=10)
    ax1.set_title("Brute-force front vs. the analytic front", color=INK, fontsize=11, loc="left")
    leg = ax1.legend(loc="upper left", bbox_to_anchor=(0.0, -0.14), fontsize=8.5, frameon=False)
    for text in leg.get_texts():
        text.set_color(INK)

    # right: how far above the analytic front each search's best points are
    style(ax2)
    edges = torch.linspace(0, 1, len(dense["bin_gap"]) + 1, dtype=torch.double)
    centers = (edges[:-1] + edges[1:]) / 2
    ax2.plot(centers, dense["bin_gap"].clamp(min=GAP_FLOOR), color=BLUE, lw=1.2, zorder=2,
             label=f"dense sampling: best of each 0.001-wide bin of $f_1$ ({n_m:,.0f} M inputs)")
    run = runs[0]
    ax2.scatter(run["front"][:, 0], run["gap"].clamp(min=GAP_FLOOR), s=14, color=AQUA, linewidths=0, zorder=3,
                label=f"NSGA-II, seed {run['seed']}: its final non-dominated set ({len(run['front'])} points)")
    s_f1 = [r["f1"] for r in slices]
    s_gap = [max(r["gap"], GAP_FLOOR) for r in slices]
    ax2.scatter(s_f1, s_gap, s=30, color=ORANGE, edgecolors=SURFACE, linewidths=1.2, zorder=4,
                label=f"L-BFGS-B at {len(slices)} fixed values of $x_1$: best of each")
    ax2.set_yscale("log")
    ax2.set_ylim(GAP_FLOOR / 3, 3)
    ax2.set_xlim(-0.02, 1.02)
    ax2.set_xlabel("$f_1$", color=INK, fontsize=10)
    ax2.set_ylabel(r"gap above the analytic front, $f_2 - (1 - \sqrt{f_1})$", color=INK, fontsize=10)
    ax2.set_title("No point lands below the front, and every part of it is reached",
                  color=INK, fontsize=11, loc="left")
    ax2.text(0.99, GAP_FLOOR * 1.6, f"gaps $\\leq$ {GAP_FLOOR:g} (rounding) drawn here", ha="right",
             va="bottom", color=INK_2, fontsize=8)
    leg = ax2.legend(loc="upper left", bbox_to_anchor=(0.0, -0.14), fontsize=8.5, frameon=False)
    for text in leg.get_texts():
        text.set_color(INK)

    fig.tight_layout()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=160, facecolor=SURFACE)
    return out


# --------------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--log2-samples", type=int, default=27, help="dense sampling: 2^N inputs")
    parser.add_argument("--slices", type=int, default=101, help="slice minimization: values of x1")
    parser.add_argument("--starts", type=int, default=128, help="slice minimization: starts per slice")
    parser.add_argument("--nsga-seeds", type=int, default=5)
    parser.add_argument("--nsga-gens", type=int, default=500)
    parser.add_argument("--nsga-pop", type=int, default=200)
    args = parser.parse_args()

    torch.set_num_threads(os.cpu_count() or 1)
    problem = FiveNodeMOFunctionNetwork()  # objectives minimized
    max_hv = float(problem.max_hv)
    summary = {"analytic_front": "f2 = 1 - sqrt(f1), f1 in [0, 1]", "ref_point": [11.0, 11.0],
               "max_hv": max_hv}

    t0 = time.time()
    dense = dense_sampling(problem, args.log2_samples)
    bins = dense["bin_gap"]
    summary["dense_sampling"] = {
        "n_inputs": dense["n_inputs"],
        "min_gap_any_input": dense["min_gap"],
        "min_gap_point_f1_f2": dense["min_gap_point"],
        "best_gap_per_f1_bin": {"n_bins": len(bins), "median": float(bins.median()),
                                "worst": float(bins.max()),
                                "worst_bin_f1": [float(bins.argmax()) / len(bins),
                                                 float(bins.argmax() + 1) / len(bins)]},
        "fraction_of_inputs_within_gap": dense["fraction_within"],
        "non_dominated_points": len(dense["archive"]),
        "hypervolume": hypervolume_2d(dense["archive"]),
        "hv_regret": max_hv - hypervolume_2d(dense["archive"]),
        "seconds": round(time.time() - t0, 1),
    }
    print("dense sampling:", json.dumps(summary["dense_sampling"], indent=1), flush=True)

    t0 = time.time()
    slices = slice_minimization(problem, args.slices, args.starts)
    gaps = [r["gap"] for r in slices]
    f1s = torch.tensor([r["f1"] for r in slices], dtype=torch.double)
    F_found = torch.tensor([[r["f1"], r["f2"]] for r in slices], dtype=torch.double)
    F_exact = torch.stack([f1s, analytic_f2(f1s)], dim=-1)
    summary["slice_minimization"] = {
        "n_slices": len(slices),
        "starts_per_slice": args.starts,
        "min_gap": min(gaps),
        "max_gap": max(gaps),
        "median_starts_within_1e-6": float(np.median([r["starts_within_1e-6"] for r in slices])),
        "hypervolume_found": hypervolume_2d(F_found),
        "hypervolume_of_analytic_points_at_same_f1": hypervolume_2d(F_exact),
        "seconds": round(time.time() - t0, 1),
        "slices": slices,
    }
    print("slice minimization: min gap %.3g, max gap %.3g, HV %.12f vs %.12f (same f1 on the curve)"
          % (min(gaps), max(gaps), hypervolume_2d(F_found), hypervolume_2d(F_exact)), flush=True)

    t0 = time.time()
    runs = nsga2(problem, range(args.nsga_seeds), args.nsga_gens, args.nsga_pop)
    summary["nsga2"] = {
        "evaluations_per_seed": args.nsga_gens * args.nsga_pop,
        "seconds": round(time.time() - t0, 1),
        "runs": [
            {
                "seed": r["seed"],
                "non_dominated_points": len(r["front"]),
                "f1_range": [float(r["front"][:, 0].min()), float(r["front"][:, 0].max())],
                "min_gap": float(r["gap"].min()),
                "median_gap": float(r["gap"].median()),
                "max_gap": float(r["gap"].max()),
                "hv_regret": max_hv - hypervolume_2d(r["front"]),
            }
            for r in runs
        ],
    }
    print("NSGA-II:", json.dumps(summary["nsga2"], indent=1), flush=True)

    with open(OUT_JSON, "w") as fh:
        json.dump(summary, fh, indent=1)
        fh.write("\n")
    print("saved", OUT_JSON)
    print("saved", plot(dense, slices, runs))


if __name__ == "__main__":
    main()
