#!/usr/bin/env python3
"""
Visualization for LLAMBO-Style Warmstart A/B/C Comparison (v3)

Generates convergence plots comparing LLM-initialized vs random-initialized
vs LHS-initialized BOFN on the Tier 1 synthetic benchmark.

v3: Adds diversity panel, updated layout, summary statistics.

Usage:
  python benchmarks/bofn_llm_warmstart_visualize.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS_FILE = Path(__file__).parent / "llm_warmstart_results.json"
FIGURES_DIR = Path(__file__).parent / "figures"


def plot_convergence(results: dict):
    """Plot convergence curves: LLM vs random vs LHS initialization."""
    FIGURES_DIR.mkdir(exist_ok=True)

    llm_results = results["llm_results"]
    random_results = results["random_results"]
    lhs_results = results.get("lhs_results", [])
    n_seeds = len(llm_results)
    n_points = len(llm_results[0]["cumulative_best"])
    iterations = list(range(n_points))

    # Compute means and std
    llm_curves = np.array([r["cumulative_best"] for r in llm_results])
    rand_curves = np.array([r["cumulative_best"] for r in random_results])

    llm_mean = llm_curves.mean(axis=0)
    llm_std = llm_curves.std(axis=0)
    rand_mean = rand_curves.mean(axis=0)
    rand_std = rand_curves.std(axis=0)

    has_lhs = len(lhs_results) > 0
    if has_lhs:
        lhs_curves = np.array([r["cumulative_best"] for r in lhs_results])
        lhs_mean = lhs_curves.mean(axis=0)
        lhs_std = lhs_curves.std(axis=0)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: Convergence curves
    ax1 = axes[0]
    ax1.plot(iterations, llm_mean, "o-", color="#2196F3", label="LLM-initialized",
             linewidth=2, markersize=5, zorder=3)
    ax1.fill_between(iterations, llm_mean - llm_std, llm_mean + llm_std,
                     alpha=0.2, color="#2196F3")

    ax1.plot(iterations, rand_mean, "s-", color="#FF9800", label="Random-initialized",
             linewidth=2, markersize=5, zorder=3)
    ax1.fill_between(iterations, rand_mean - rand_std, rand_mean + rand_std,
                     alpha=0.2, color="#FF9800")

    if has_lhs:
        ax1.plot(iterations, lhs_mean, "^-", color="#4CAF50", label="LHS-initialized",
                 linewidth=2, markersize=5, zorder=3)
        ax1.fill_between(iterations, lhs_mean - lhs_std, lhs_mean + lhs_std,
                         alpha=0.2, color="#4CAF50")

    ax1.set_xlabel("BO Iteration", fontsize=12)
    ax1.set_ylabel("Best Objective Found", fontsize=12)
    version = results.get("summary", {}).get("version", "v2")
    ax1.set_title(f"BOFN Convergence ({n_seeds} seeds, {version})", fontsize=12)
    ax1.legend(fontsize=9, loc="lower right")
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(iterations)
    ax1.set_xticklabels(["init"] + [str(i) for i in range(1, n_points)])

    # Annotate the cold-start advantage
    delta_init = llm_mean[0] - rand_mean[0]
    if delta_init > 0:
        ax1.annotate(
            f"Cold-start\nadvantage\nΔ={delta_init:.4f}",
            xy=(0, llm_mean[0]),
            xytext=(2, llm_mean[0] - 0.02),
            fontsize=9,
            ha="center",
            arrowprops=dict(arrowstyle="->", color="#2196F3", lw=1.5),
            color="#2196F3",
        )

    # Panel 2: Initial phase fraction quality
    ax2 = axes[1]

    # LLM initial phase fractions
    llm_phases = []
    for r in llm_results:
        llm_phases.extend(r["initial_phase_fractions"])
    rand_phases = []
    for r in random_results:
        rand_phases.extend(r["initial_phase_fractions"])

    bins = np.linspace(0, 1, 25)
    ax2.hist(llm_phases, bins=bins, alpha=0.6, color="#2196F3",
             label="LLM-initialized", density=True, edgecolor="white")
    ax2.hist(rand_phases, bins=bins, alpha=0.6, color="#FF9800",
             label="Random-initialized", density=True, edgecolor="white")

    if has_lhs:
        lhs_phases = []
        for r in lhs_results:
            lhs_phases.extend(r["initial_phase_fractions"])
        ax2.hist(lhs_phases, bins=bins, alpha=0.4, color="#4CAF50",
                 label="LHS-initialized", density=True, edgecolor="white")

    ax2.axvline(x=0.5, color="red", linestyle="--", alpha=0.5, label="Threshold (0.5)")
    ax2.set_xlabel("CALPHAD Phase Fraction (Node 0 output)", fontsize=12)
    ax2.set_ylabel("Density", fontsize=12)
    ax2.set_title("Initial CALPHAD Screening Quality", fontsize=12)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    # Add text summary
    llm_above = sum(1 for p in llm_phases if p > 0.5)
    rand_above = sum(1 for p in rand_phases if p > 0.5)
    summary_text = (f"LLM: {llm_above}/{len(llm_phases)} above threshold\n"
                    f"Random: {rand_above}/{len(rand_phases)} above threshold")
    if has_lhs:
        lhs_above = sum(1 for p in lhs_phases if p > 0.5)
        summary_text += f"\nLHS: {lhs_above}/{len(lhs_phases)} above threshold"
    ax2.text(
        0.02, 0.95,
        summary_text,
        transform=ax2.transAxes,
        fontsize=8,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
    )

    # Panel 3: P3 Diversity diagnostics
    ax3 = axes[2]
    diversity = results.get("diversity_stats", {})
    if diversity:
        arms = list(diversity.keys())
        mpd_vals = [diversity[a]["mean_pairwise_distance"] for a in arms]
        mmd_vals = [diversity[a]["mean_min_distance"] for a in arms]
        x = np.arange(len(arms))
        width = 0.35
        bars1 = ax3.bar(x - width/2, mpd_vals, width, label="Mean pairwise dist",
                        color=["#2196F3", "#FF9800", "#4CAF50"][:len(arms)], alpha=0.7)
        bars2 = ax3.bar(x + width/2, mmd_vals, width, label="Mean min dist",
                        color=["#2196F3", "#FF9800", "#4CAF50"][:len(arms)], alpha=0.4)
        ax3.set_xticks(x)
        ax3.set_xticklabels([a.upper() for a in arms])
        ax3.set_ylabel("Distance", fontsize=12)
        ax3.set_title("P3: Composition Diversity", fontsize=12)
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3, axis="y")
        # Add value labels
        for bar in bars1:
            h = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2, h + 0.005,
                     f"{h:.3f}", ha="center", fontsize=8)
        for bar in bars2:
            h = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2, h + 0.005,
                     f"{h:.3f}", ha="center", fontsize=8)
    else:
        ax3.text(0.5, 0.5, "No diversity data\n(run v3)", ha="center",
                 va="center", transform=ax3.transAxes, fontsize=14, color="gray")
        ax3.set_title("P3: Composition Diversity", fontsize=12)

    plt.tight_layout()
    outpath = FIGURES_DIR / "llm_warmstart_convergence.png"
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    print(f"Saved convergence plot to {outpath}")
    plt.close()

    return outpath


def main():
    if not RESULTS_FILE.exists():
        print(f"Results file not found: {RESULTS_FILE}")
        print("Run bofn_llm_warmstart.py --run-comparison first")
        return

    with open(RESULTS_FILE) as f:
        results = json.load(f)

    print("Generating LLAMBO warmstart visualization (v3)...")
    plot_convergence(results)

    # Print summary
    summary = results["summary"]
    print(f"\nSummary:")
    print(f"  LLM final mean: {summary['llm_final_mean']:.4f}")
    print(f"  Random final mean: {summary['random_final_mean']:.4f}")
    if "lhs_final_mean" in summary:
        print(f"  LHS final mean: {summary['lhs_final_mean']:.4f}")
    print(f"  LLM vs Random advantage: {summary.get('llm_vs_random_advantage', summary.get('advantage', 0)):+.4f}")
    if "llm_vs_lhs_advantage" in summary:
        print(f"  LLM vs LHS advantage: {summary['llm_vs_lhs_advantage']:+.4f}")
    print(f"  LLM vs Random win rate: "
          f"{summary.get('llm_vs_random_win_rate', summary.get('win_rate', 0))*100:.0f}%")


if __name__ == "__main__":
    main()
