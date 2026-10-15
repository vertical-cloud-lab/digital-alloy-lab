#!/usr/bin/env python3
"""
Visualizations for the p-KGFN demo results.

Generates 4 figures with multi-seed runs and equal-cost comparison:
  1. Manufacturing function network DAG with node costs
  2. BO convergence vs cost — mean ± 1 std over multiple seeds
  3. BO convergence vs iteration — mean ± 1 std over multiple seeds
  4. Node selection frequency — aggregated across seeds

All algorithms run to the same total cost budget for fair comparison.
p-KGFN uses more iterations (cheap partial evals) within the same budget.

Usage:
  python benchmarks/bofn_pkgfn_visualize.py    # saves PNGs to benchmarks/figures/
"""

import json
import os
import sys
import warnings
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Suppress non-strict tensor dimension warnings from GP fantasy models
warnings.filterwarnings("ignore", message=".*Non-strict enforcement.*")
warnings.filterwarnings("ignore", message=".*Could not update.*GenericDeterministicModel.*")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────
# Clean, publication-quality aesthetic (Doumont/Tufte inspired):
# minimal chartjunk, left-aligned labels, desaturated palette, no top/right spines.

ALGO_STYLE = {
    "Random": {"color": "#546E7A", "marker": "s", "ls": "-"},   # darker gray
    "TSFN":   {"color": "#1E88E5", "marker": "^", "ls": "-"},
    "pKGFN":  {"color": "#D81B60", "marker": "o", "ls": "-"},
}
NODE_COLORS = {0: "#43A047", 1: "#1E88E5", 2: "#FB8C00", 3: "#D81B60"}

# Default node costs for the manufacturing problem (used in labels)
node_costs_default = [5, 10, 10, 45]

plt.rcParams.update({
    "figure.dpi": 180,
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
})


# ── Utility: interpolate traces to common cost grid ──────────────────────

def _interpolate_to_cost_grid(cost_traces, best_val_traces, grid):
    """Linearly interpolate best-val traces onto a common cost grid.

    Args:
        cost_traces: list of 1-D arrays (per seed), cumulative costs.
        best_val_traces: list of 1-D arrays (per seed), best values.
        grid: 1-D array of cost values to interpolate onto.

    Returns:
        2-D array of shape (n_seeds, len(grid)).
    """
    n_seeds = len(cost_traces)
    out = np.full((n_seeds, len(grid)), np.nan)
    for i in range(n_seeds):
        c = np.asarray(cost_traces[i])
        v = np.asarray(best_val_traces[i])
        # Extend to the right: if the trace ended before the grid ends,
        # hold the last value.
        out[i] = np.interp(grid, c, v, left=np.nan, right=v[-1])
    return out


# ── Figure 1: Manufacturing DAG ──────────────────────────────────────────

def plot_manufacturing_dag(save_path):
    """Draw the 4-node manufacturing function network DAG."""
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set_xlim(-1.2, 11)
    ax.set_ylim(-2.5, 3.5)
    ax.axis("off")
    fig.suptitle(
        "Manufacturing Function Network (Buathong et al. 2024)",
        fontsize=13, fontweight="bold", y=0.97,
    )

    # Node positions and metadata
    nodes = [
        {"x": 0.5, "y": 1.0, "label": "Node 0\nDesign", "dim": "d=2",
         "cost": "$5", "color": NODE_COLORS[0], "inputs": "x₁, x₂"},
        {"x": 3.5, "y": 2.0, "label": "Node 1\nForming", "dim": "d=1",
         "cost": "$10", "color": NODE_COLORS[1], "inputs": "y₀"},
        {"x": 3.5, "y": 0.0, "label": "Node 2\nAssembly", "dim": "d=2",
         "cost": "$10", "color": NODE_COLORS[2], "inputs": "x₃, x₄"},
        {"x": 7.0, "y": 1.0, "label": "Node 3\nTesting", "dim": "d=2",
         "cost": "$45", "color": NODE_COLORS[3], "inputs": "y₁, y₂"},
    ]

    for nd in nodes:
        box = mpatches.FancyBboxPatch(
            (nd["x"] - 0.9, nd["y"] - 0.65), 1.8, 1.3,
            boxstyle="round,pad=0.12", facecolor=nd["color"], alpha=0.15,
            edgecolor=nd["color"], linewidth=2,
        )
        ax.add_patch(box)
        ax.text(nd["x"], nd["y"] + 0.18, nd["label"], ha="center", va="center",
                fontsize=9, fontweight="bold", color=nd["color"])
        ax.text(nd["x"], nd["y"] - 0.3, f'{nd["dim"]}  |  {nd["inputs"]}',
                ha="center", va="center", fontsize=7.5, color="gray")
        ax.text(nd["x"], nd["y"] + 0.85, nd["cost"], ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=nd["color"],
                bbox=dict(boxstyle="round,pad=0.15", fc="white",
                          ec=nd["color"], alpha=0.85, lw=1.2))

    edges = [
        (nodes[0], nodes[1], "y₀"),
        (nodes[1], nodes[3], "y₁"),
        (nodes[2], nodes[3], "y₂"),
    ]
    for src, dst, label in edges:
        ax.annotate(
            "", xy=(dst["x"] - 1.0, dst["y"]),
            xytext=(src["x"] + 1.0, src["y"]),
            arrowprops=dict(arrowstyle="-|>", color="#666", lw=1.8),
        )
        mx = (src["x"] + dst["x"]) / 2
        my = (src["y"] + dst["y"]) / 2
        ax.text(mx, my + 0.2, label, ha="center", va="bottom",
                fontsize=8.5, color="#555", fontstyle="italic")

    # External inputs
    for ext_x, ext_label, target in [
        (0.5, "x₁, x₂ ∈ [-1, 1]", nodes[0]),
        (3.5, "x₃, x₄ ∈ [-1, 1]", nodes[2]),
    ]:
        ax.annotate(
            "", xy=(target["x"], target["y"] - 0.65),
            xytext=(ext_x, -1.5 + 0.25),
            arrowprops=dict(arrowstyle="-|>", color="#aaa", lw=1.3, ls="--"),
        )
        ax.text(ext_x, -1.5, f"Decision vars\n{ext_label}",
                ha="center", va="top", fontsize=7.5, color="#777")

    # Output annotation
    ax.text(7.0, -0.45, "Network output y₃\n(optimisation objective)",
            ha="center", va="top", fontsize=8.5, fontweight="bold",
            color=NODE_COLORS[3],
            bbox=dict(boxstyle="round,pad=0.25", fc="#FCE4EC",
                      ec=NODE_COLORS[3], lw=1.2))
    ax.annotate(
        "", xy=(7.0, -0.2),
        xytext=(7.0, nodes[3]["y"] - 0.65),
        arrowprops=dict(arrowstyle="-|>", color=NODE_COLORS[3], lw=1.3),
    )

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 2: Cost-efficiency (mean ± std over seeds) ────────────────────

def plot_cost_efficiency(all_results, cost_budget, n_seeds, save_path):
    """Best value vs cumulative cost — all algorithms to the same budget."""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Start grid from the minimum init cost (where all algorithms have data)
    min_init_cost = min(
        r["cost_trace"][0]
        for algo in all_results
        for r in all_results[algo]
    )
    grid = np.linspace(min_init_cost, cost_budget, 300)

    for algo in ["Random", "TSFN", "pKGFN"]:
        style = ALGO_STYLE[algo]
        costs_all = [r["cost_trace"] for r in all_results[algo]]
        vals_all = [r["best_vals"] for r in all_results[algo]]

        interp = _interpolate_to_cost_grid(costs_all, vals_all, grid)
        mean = np.nanmean(interp, axis=0)
        std = np.nanstd(interp, axis=0)

        ax.plot(grid, mean, color=style["color"], ls=style["ls"], lw=2,
                label=algo, zorder=3)
        ax.fill_between(grid, mean - std, mean + std,
                        color=style["color"], alpha=0.15, zorder=2)

    # Add vertical dashed line at init cost
    ax.axvline(min_init_cost, color="#777", ls="--", lw=1.5, zorder=1)
    ylim = ax.get_ylim()
    ax.text(min_init_cost + 15, ylim[0] + 0.05 * (ylim[1] - ylim[0]),
            f"Init\n${min_init_cost:,.0f}", fontsize=8, color="#555",
            va="bottom", ha="left", fontweight="bold")

    ax.set_xlim(min_init_cost, cost_budget)
    ax.set_xlabel("Cumulative evaluation cost ($)")
    ax.set_ylabel("Best network output (GP posterior mean)")
    ax.set_title(f"(a)  Cost Efficiency — equal ${cost_budget:,} budget\n"
                 f"(mean ± 1 std, {n_seeds} seeds)",
                 fontweight="bold")
    ax.legend(loc="lower right", framealpha=0.9)

    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 3: Iteration convergence (mean ± std over seeds) ──────────────

def plot_iteration_convergence(all_results, n_seeds, save_path):
    """Best value vs iteration number — shows how many BO steps each
    algorithm gets within the same budget (p-KGFN gets more).
    
    Note: per-iteration costs differ (~$7.74 for p-KGFN vs $70 for baselines),
    so cost-efficiency (Fig a) is the primary comparison metric.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    for algo in ["Random", "TSFN", "pKGFN"]:
        style = ALGO_STYLE[algo]
        # Collect iteration-indexed traces (different lengths for p-KGFN)
        all_vals = [r["best_vals"] for r in all_results[algo]]
        max_len = max(len(v) for v in all_vals)

        # Pad shorter traces with their last value
        padded = np.full((n_seeds, max_len), np.nan)
        for i, v in enumerate(all_vals):
            padded[i, : len(v)] = v
            if len(v) < max_len:
                padded[i, len(v):] = v[-1]

        iters = np.arange(max_len)
        mean = np.nanmean(padded, axis=0)
        std = np.nanstd(padded, axis=0)

        # Compute marginal cost per iteration
        all_sels = []
        for r in all_results[algo]:
            all_sels.extend(r.get("node_selections", []))
        if algo == "pKGFN" and all_sels:
            cost_per_it = np.mean([
                node_costs_default[s] if isinstance(s, int) else sum(node_costs_default)
                for s in all_sels
            ])
            cost_label = f"~${cost_per_it:.0f}/iter"
        else:
            cost_label = f"${sum(node_costs_default)}/iter"

        # Marker every few steps to keep it clean
        marker_every = max(1, max_len // 12)
        # Report average iterations (not max) for consistency with node selection panel
        avg_iters = np.mean([len(v) - 1 for v in all_vals])
        ax.plot(iters, mean, color=style["color"], ls=style["ls"], lw=2,
                marker=style["marker"], markevery=marker_every,
                markersize=5, label=f"{algo} (avg {avg_iters:.0f} iters, {cost_label})",
                zorder=3)
        ax.fill_between(iters, mean - std, mean + std,
                        color=style["color"], alpha=0.15, zorder=2)

    ax.set_xlim(0, None)
    ax.set_xlabel("BO iteration (0 = after initialisation)")
    ax.set_ylabel("Best network output (GP posterior mean)")
    ax.set_title(f"(b)  Convergence vs Iteration — same cost budget\n"
                 f"(mean ± 1 std, {n_seeds} seeds; "
                 f"caution: per-iteration costs differ)",
                 fontweight="bold")
    ax.legend(loc="lower right", framealpha=0.9)

    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 4: Node Selection Frequency ───────────────────────────────────

def plot_node_selection(all_results, node_costs, n_seeds, save_path):
    """Aggregated node selection frequency across all seeds."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5),
                                    gridspec_kw={"width_ratios": [1.6, 1]})
    fig.suptitle(f"(c)  p-KGFN Node Selection Pattern  ({n_seeds} seeds)",
                 fontsize=12, fontweight="bold", y=0.98)

    # Aggregate selections across seeds
    all_sel = []
    total_costs = []
    for r in all_results["pKGFN"]:
        all_sel.extend(r["node_selections"])
        total_costs.append(r["total_cost"])

    counts = Counter()
    for sel in all_sel:
        if isinstance(sel, int):
            counts[sel] += 1
        else:
            counts["full"] += 1
    total_sel = sum(counts.values())

    # Left: bar chart of selection frequency
    node_labels = {0: "Node 0\nDesign ($5)", 1: "Node 1\nForming ($10)",
                   2: "Node 2\nAssembly ($10)", 3: "Node 3\nTesting ($45)",
                   "full": "Full eval\n($70)"}
    bars_x = []
    bars_h = []
    bars_c = []
    bars_l = []
    for k in [0, 1, 2, 3, "full"]:
        bars_x.append(len(bars_x))
        bars_h.append(counts.get(k, 0))
        bars_c.append(NODE_COLORS.get(k, "#999"))
        bars_l.append(node_labels[k])

    rects = ax1.bar(bars_x, bars_h, color=bars_c, alpha=0.75,
                    edgecolor="white", linewidth=1.5, width=0.7)
    for rect, h in zip(rects, bars_h):
        if h > 0:
            pct = h / total_sel * 100
            ax1.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 0.5,
                     f"{h}\n({pct:.0f}%)", ha="center", va="bottom", fontsize=8,
                     fontweight="bold")

    ax1.set_xticks(bars_x)
    ax1.set_xticklabels(bars_l, fontsize=8)
    ax1.set_ylabel("Times selected")
    ax1.set_title("Selection frequency", fontweight="bold")

    # Right: marginal cost summary (not amortized)
    marginal_costs = []
    for sel in all_sel:
        if isinstance(sel, int):
            marginal_costs.append(node_costs[sel])
        else:
            marginal_costs.append(sum(node_costs))
    marginal_mean = np.mean(marginal_costs) if marginal_costs else 0
    marginal_std = np.std(marginal_costs) if marginal_costs else 0

    summary = (
        f"Marginal cost / BO iteration:\n"
        f"  p-KGFN: ${marginal_mean:.1f} ± ${marginal_std:.1f}\n"
        f"  Baselines: ${sum(node_costs)} (full eval)\n\n"
        f"p-KGFN: avg {total_sel / n_seeds:.0f} partial evals\n"
        f"Baselines: {len(all_results['TSFN'][0]['best_vals']) - 1} full evals\n"
        f"Budget: ${sum(node_costs) * (9 + len(all_results['TSFN'][0]['best_vals']) - 1):,}\n"
        f"({total_sel} total selections / {n_seeds} seeds)\n\n"
        f"Nodes 1 and 3 are never directly\n"
        f"evaluated — their posteriors are\n"
        f"updated indirectly via the DAG."
    )
    ax2.text(0.05, 0.95, summary, transform=ax2.transAxes,
             ha="left", va="top", fontsize=9, color="#333",
             bbox=dict(boxstyle="round,pad=0.5", fc="#F5F5F5", ec="#ccc", lw=0.8))
    ax2.axis("off")
    ax2.set_title("Cost analysis", fontweight="bold")

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Main ──────────────────────────────────────────────────────────────────

def _load_cached_results(cache_path):
    """Load results from a cached JSON file."""
    with open(cache_path) as f:
        cache = json.load(f)
    config = cache["config"]
    all_results = {}
    for algo in ["Random", "TSFN", "pKGFN"]:
        all_results[algo] = []
        for entry in cache[algo]:
            # Restore node_selections: convert string ints back to int
            sels = []
            for s in entry.get("node_selections", []):
                if isinstance(s, int):
                    sels.append(s)
                elif isinstance(s, str) and s.isdigit():
                    sels.append(int(s))
                else:
                    sels.append(s)
            all_results[algo].append({
                "best_vals": entry["best_vals"],
                "total_cost": entry["total_cost"],
                "cost_trace": entry["cost_trace"],
                "node_selections": sels,
            })
    return all_results, config


def main():
    print("=" * 70)
    print("p-KGFN Visualization — Multi-Seed, Equal-Cost Comparison")
    print("=" * 70)

    cache_path = os.path.join(os.path.dirname(__file__), "pkgfn_results.json")
    use_cache = "--from-cache" in sys.argv and os.path.exists(cache_path)

    if use_cache:
        print("\n  Loading cached results...")
        all_results, config = _load_cached_results(cache_path)
        node_costs = config["node_costs"]
        cost_budget = config["cost_budget"]
        n_seeds = config["n_seeds"]
        print(f"  Loaded {n_seeds} seeds × 3 algorithms from cache")
    else:
        import torch
        torch.set_default_dtype(torch.double)

        from benchmarks.bofn_pkgfn_demo import run_bo_loop
        from benchmarks.partial_kgfn.manufacturing_problem import ManufacturingGPNetwork

        node_costs = [5, 10, 10, 45]
        n_init = 9
        full_cost_per_iter = sum(node_costs)  # $70
        n_iters_baseline = 8  # baseline algorithms get 8 full-eval iterations
        cost_budget = full_cost_per_iter * n_init + full_cost_per_iter * n_iters_baseline  # $1,190
        n_seeds = 5

        print(f"\n  Config: {n_seeds} seeds × 3 algorithms")
        print(f"  Cost budget: ${cost_budget:,}  ({n_init} init + {n_iters_baseline} full-eval iters)")
        print(f"  p-KGFN runs more iterations within the same budget\n")

        # Run all seeds
        all_results = {"Random": [], "TSFN": [], "pKGFN": []}
        for seed_idx in range(n_seeds):
            seed = 100 + seed_idx
            for algo in ["Random", "TSFN", "pKGFN"]:
                problem = ManufacturingGPNetwork(node_costs=node_costs, seed=seed_idx)
                res = run_bo_loop(
                    problem, algo=algo, n_init=n_init, seed=seed,
                    cost_budget=cost_budget, verbose=(seed_idx == 0),
                )
                all_results[algo].append(res)
            print(f"  Seed {seed_idx + 1}/{n_seeds} complete.")

        # Save results cache
        cache = {"config": {
            "n_seeds": n_seeds, "cost_budget": cost_budget,
            "n_init": n_init, "node_costs": node_costs,
        }}
        for algo in all_results:
            cache[algo] = []
            for res in all_results[algo]:
                cache[algo].append({
                    "best_vals": res["best_vals"],
                    "total_cost": res["total_cost"],
                    "cost_trace": res["cost_trace"],
                    "node_selections": [
                        str(s) if not isinstance(s, int) else s
                        for s in res.get("node_selections", [])
                    ],
                })
        with open(cache_path, "w") as f:
            json.dump(cache, f, indent=2)
        print(f"\n  Results cached: {cache_path}")

    # ── Generate figures ──────────────────────────────────────────────
    print("\n[1/4] Drawing manufacturing DAG...")
    plot_manufacturing_dag(os.path.join(FIGURE_DIR, "pkgfn_dag.png"))

    print("[2/4] Plotting cost efficiency (mean ± std)...")
    plot_cost_efficiency(all_results, cost_budget, n_seeds,
                         os.path.join(FIGURE_DIR, "pkgfn_cost_efficiency.png"))

    print("[3/4] Plotting iteration convergence (mean ± std)...")
    plot_iteration_convergence(all_results, n_seeds,
                               os.path.join(FIGURE_DIR, "pkgfn_convergence.png"))

    print("[4/4] Plotting node selection frequency...")
    plot_node_selection(all_results, node_costs, n_seeds,
                        os.path.join(FIGURE_DIR, "pkgfn_node_selection.png"))

    # ── Summary ───────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print(f"Summary ({n_seeds} seeds, ${cost_budget:,} budget):")
    for algo in all_results:
        finals = [r["best_vals"][-1] for r in all_results[algo]]
        costs = [r["total_cost"] for r in all_results[algo]]
        n_iters_avg = np.mean([len(r["best_vals"]) - 1 for r in all_results[algo]])
        print(f"  {algo:>10s}: best={np.mean(finals):+.4f} ± {np.std(finals):.4f}"
              f"  cost=${np.mean(costs):,.0f}  iters={n_iters_avg:.0f}")
    print(f"\nAll figures saved to {FIGURE_DIR}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
