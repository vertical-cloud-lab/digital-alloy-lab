#!/usr/bin/env python3
"""
Visualizations for the BOFN demo results.

Generates 4 figures:
  1. Function network DAG with per-node dimensionality
  2. GP prediction accuracy — predicted vs ground truth at each node
  3. CALPHAD phase-fraction landscape over the composition simplex
  4. Cost-aware screening comparison (bar chart)

Usage:
  python benchmarks/bofn_visualize.py          # saves PNGs to benchmarks/figures/
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import torch

# Reuse functions from the demo
sys.path.insert(0, os.path.dirname(__file__))
from bofn_demo import (
    DTYPE, DEVICE,
    calphad_fn, powder_fn, lpbf_fn, characterization_fn,
    generate_node_data, build_node_gps, composite_forward,
    cost_aware_screening,
)

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

# Consistent style
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})


# ── Figure 1: Function Network DAG ─────────────────────────────────────────

def plot_dag(save_path):
    """Draw the 4-node function network DAG with cost annotations."""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1.5, 2.5)
    ax.axis("off")
    fig.suptitle("BOFN Function Network — VCL Alloy Discovery Pipeline", fontsize=14, fontweight="bold")

    nodes = [
        {"x": 0.5, "y": 0.5, "label": "Node 0\nCALPHAD", "dim": "d=3 → 1", "cost": "$1", "color": "#4CAF50"},
        {"x": 3.5, "y": 0.5, "label": "Node 1\nPowder", "dim": "d=3 → 1", "cost": "$100", "color": "#2196F3"},
        {"x": 6.5, "y": 0.5, "label": "Node 2\nLPBF", "dim": "d=3 → 1", "cost": "$500", "color": "#FF9800"},
        {"x": 9.5, "y": 0.5, "label": "Node 3\nCharacterization", "dim": "d=1 → 1", "cost": "$700", "color": "#E91E63"},
    ]

    for nd in nodes:
        box = mpatches.FancyBboxPatch(
            (nd["x"] - 0.9, nd["y"] - 0.7), 1.8, 1.4,
            boxstyle="round,pad=0.15", facecolor=nd["color"], alpha=0.25,
            edgecolor=nd["color"], linewidth=2,
        )
        ax.add_patch(box)
        ax.text(nd["x"], nd["y"] + 0.15, nd["label"], ha="center", va="center",
                fontsize=10, fontweight="bold", color=nd["color"])
        ax.text(nd["x"], nd["y"] - 0.35, nd["dim"], ha="center", va="center",
                fontsize=8, color="gray")
        ax.text(nd["x"], nd["y"] + 0.85, nd["cost"], ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=nd["color"],
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=nd["color"], alpha=0.8))

    # Arrows between nodes
    for i in range(len(nodes) - 1):
        ax.annotate(
            "", xy=(nodes[i+1]["x"] - 1.0, nodes[i+1]["y"]),
            xytext=(nodes[i]["x"] + 1.0, nodes[i]["y"]),
            arrowprops=dict(arrowstyle="-|>", color="#555", lw=2),
        )

    # External inputs
    ext_inputs = [
        {"node_x": 0.5, "label": "Alloy\ncomposition\n(3 components)", "y_off": -1.5, "target_idx": 0},
        {"node_x": 3.5, "label": "Process\nparams (2)", "y_off": -1.5, "target_idx": 1},
        {"node_x": 6.5, "label": "Print\nparams (2)", "y_off": -1.5, "target_idx": 2},
    ]
    for ext in ext_inputs:
        target_node = nodes[ext["target_idx"]]
        ax.annotate(
            "", xy=(target_node["x"], target_node["y"] - 0.7),
            xytext=(ext["node_x"], ext["y_off"] + 0.3),
            arrowprops=dict(arrowstyle="-|>", color="#999", lw=1.5, ls="--"),
        )
        ax.text(ext["node_x"], ext["y_off"], ext["label"],
                ha="center", va="top", fontsize=8, color="#666")

    # Final output label
    ax.text(9.5, -0.9, "Mechanical\nproperty\n(objective)", ha="center", va="top",
            fontsize=9, fontweight="bold", color="#E91E63",
            bbox=dict(boxstyle="round,pad=0.2", fc="#FCE4EC", ec="#E91E63"))
    ax.annotate(
        "", xy=(9.5, -0.55),
        xytext=(9.5, nodes[0]["y"] - 0.7),
        arrowprops=dict(arrowstyle="-|>", color="#E91E63", lw=1.5),
    )

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 2: GP Prediction Accuracy ───────────────────────────────────────

def plot_gp_accuracy(models, node_data, save_path):
    """Scatter predicted vs ground truth for each node's GP."""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=False)
    fig.suptitle("Per-Node GP Prediction Accuracy (30 training points)", fontsize=14, fontweight="bold")

    node_names = ["CALPHAD", "Powder", "LPBF", "Characterization"]
    colors = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63"]

    # Generate fresh test data for each node
    n_test = 50
    torch.manual_seed(99)

    for i, (ax, name, color) in enumerate(zip(axes, node_names, colors)):
        X_train, Y_train = node_data[i]
        model = models[i]

        # Generate test inputs in the same range as training
        if i == 0:
            X_test = torch.rand(n_test, 3, dtype=DTYPE, device=DEVICE)
            X_test = X_test / X_test.sum(dim=1, keepdim=True)
            Y_true = calphad_fn(X_test)
        elif i == 1:
            pf = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
            pp = torch.rand(n_test, 2, dtype=DTYPE, device=DEVICE)
            X_test = torch.cat([pf, pp], dim=-1)
            Y_true = powder_fn(pf, pp)
        elif i == 2:
            pq = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
            prp = torch.rand(n_test, 2, dtype=DTYPE, device=DEVICE)
            X_test = torch.cat([pq, prp], dim=-1)
            Y_true = lpbf_fn(pq, prp)
        else:
            X_test = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
            Y_true = characterization_fn(X_test)

        with torch.no_grad():
            posterior = model.posterior(X_test)
            Y_pred = posterior.mean
            Y_std = posterior.variance.sqrt()

        y_true = Y_true.squeeze().numpy()
        y_pred = Y_pred.squeeze().numpy()
        y_std = Y_std.squeeze().numpy()

        ax.errorbar(y_true, y_pred, yerr=1.96 * y_std, fmt="o", ms=4,
                     color=color, alpha=0.6, ecolor="lightgray", elinewidth=0.8,
                     capsize=2, label="Predictions")
        lims = [min(y_true.min(), y_pred.min()) - 0.05,
                max(y_true.max(), y_pred.max()) + 0.05]
        ax.plot(lims, lims, "k--", lw=1, alpha=0.5, label="y = x")
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_xlabel("Ground Truth")
        ax.set_ylabel("GP Predicted")
        ax.set_title(f"Node {i}: {name}", color=color, fontweight="bold")
        ax.set_aspect("equal", adjustable="box")

        # R² annotation
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - y_true.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        ax.text(0.05, 0.95, f"R² = {r2:.3f}", transform=ax.transAxes,
                fontsize=9, va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 3: CALPHAD Composition Landscape ────────────────────────────────

def plot_calphad_landscape(model, save_path):
    """Ternary-style heatmap of GP-predicted phase fraction over composition simplex."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("CALPHAD Phase-Fraction Landscape (Composition Simplex)",
                 fontsize=14, fontweight="bold")

    # Generate grid on the simplex (barycentric → Cartesian for plotting)
    resolution = 80
    coords = []
    vals_true = []

    for i in range(resolution + 1):
        for j in range(resolution + 1 - i):
            k = resolution - i - j
            c = torch.tensor([[i / resolution, j / resolution, k / resolution]],
                             dtype=DTYPE, device=DEVICE)
            coords.append(c)
            vals_true.append(calphad_fn(c).item())

    X_grid = torch.cat(coords, dim=0)
    vals_true = np.array(vals_true)

    # GP predictions
    with torch.no_grad():
        posterior = model.posterior(X_grid)
        vals_pred = posterior.mean.squeeze().numpy()
        vals_std = posterior.variance.sqrt().squeeze().numpy()

    # Barycentric → 2D Cartesian
    def bary_to_cart(c):
        x = 0.5 * (2 * c[:, 1] + c[:, 2]) / (c[:, 0] + c[:, 1] + c[:, 2])
        y = (np.sqrt(3) / 2) * c[:, 2] / (c[:, 0] + c[:, 1] + c[:, 2])
        return x, y

    c_np = X_grid.numpy()
    xc, yc = bary_to_cart(c_np)

    for ax, vals, title, cmap in [
        (axes[0], vals_true, "Ground Truth", "viridis"),
        (axes[1], vals_pred, "GP Predicted (Mean)", "viridis"),
    ]:
        sc = ax.tricontourf(xc, yc, vals, levels=30, cmap=cmap)
        plt.colorbar(sc, ax=ax, label="Phase Fraction")
        ax.set_title(title, fontweight="bold")
        ax.set_aspect("equal")

        # Draw simplex triangle
        tri_x = [0, 1, 0.5, 0]
        tri_y = [0, 0, np.sqrt(3)/2, 0]
        ax.plot(tri_x, tri_y, "k-", lw=1.5)

        # Vertex labels
        ax.text(-0.05, -0.05, "Comp A", ha="center", fontsize=9, fontweight="bold")
        ax.text(1.05, -0.05, "Comp B", ha="center", fontsize=9, fontweight="bold")
        ax.text(0.5, np.sqrt(3)/2 + 0.05, "Comp C", ha="center", fontsize=9, fontweight="bold")

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.0)
        ax.axis("off")

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 4: Cost-Aware Screening Comparison ──────────────────────────────

def plot_cost_comparison(result, save_path):
    """Bar chart comparing cost-aware screening vs naive evaluation."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Cost-Aware Partial Evaluation (p-KGFN Concept)", fontsize=14, fontweight="bold")

    # Left: cost breakdown
    ax = axes[0]
    categories = ["CALPHAD\nScreening", "Downstream\n(promoted)", "Total\n(screening)", "Naive\n(no screening)"]
    costs = [result["stage1_cost"], result["stage2_cost"], result["total_cost"], result["naive_cost"]]
    colors = ["#4CAF50", "#FF9800", "#2196F3", "#E91E63"]
    bars = ax.bar(categories, costs, color=colors, alpha=0.8, edgecolor="white", linewidth=1.5)

    for bar, cost in zip(bars, costs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 500,
                f"${cost:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylabel("Cost ($)")
    ax.set_title("Cost Breakdown", fontweight="bold")
    ax.set_ylim(0, result["naive_cost"] * 1.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Right: pipeline funnel
    ax2 = axes[1]
    n_total = result["n_candidates"]
    n_promoted = result["n_promoted"]
    n_rejected = n_total - n_promoted
    savings_pct = result["savings"] / result["naive_cost"] * 100

    stages = ["All Candidates", "CALPHAD\nScreened", "Promoted to\nFull Pipeline"]
    counts = [n_total, n_total, n_promoted]
    funnel_colors = ["#78909C", "#4CAF50", "#2196F3"]

    bars2 = ax2.barh(stages[::-1], counts[::-1], color=funnel_colors[::-1],
                      alpha=0.8, edgecolor="white", linewidth=1.5, height=0.6)

    for bar, count in zip(bars2, counts[::-1]):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{count}", ha="left", va="center", fontsize=11, fontweight="bold")

    ax2.set_xlabel("Number of Candidates")
    ax2.set_title(f"Screening Funnel — {savings_pct:.0f}% Cost Savings", fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_xlim(0, n_total * 1.2)

    # Savings annotation
    ax2.text(0.95, 0.05,
             f"Savings: ${result['savings']:,.0f}\n"
             f"({n_rejected} candidates rejected\nat CALPHAD stage)",
             transform=ax2.transAxes, fontsize=10, va="bottom", ha="right",
             bbox=dict(boxstyle="round,pad=0.4", fc="#E8F5E9", ec="#4CAF50", alpha=0.9))

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("BOFN Visualization — Generating Figures")
    print("=" * 70)

    # 1. Generate data and fit models (same as demo)
    print("\n[1/5] Generating data and fitting GP models...")
    torch.manual_seed(42)
    node_data = generate_node_data(n_train=30)
    models = build_node_gps(node_data)

    # 2. DAG diagram
    print("\n[2/5] Drawing function network DAG...")
    plot_dag(os.path.join(FIGURE_DIR, "bofn_dag.png"))

    # 3. GP accuracy
    print("\n[3/5] Plotting GP prediction accuracy...")
    plot_gp_accuracy(models, node_data, os.path.join(FIGURE_DIR, "gp_accuracy.png"))

    # 4. CALPHAD landscape
    print("\n[4/5] Plotting CALPHAD composition landscape...")
    plot_calphad_landscape(models[0], os.path.join(FIGURE_DIR, "calphad_landscape.png"))

    # 5. Cost comparison
    print("\n[5/5] Plotting cost-aware screening comparison...")
    torch.manual_seed(42)
    n_screen = 50
    screen_comp = torch.rand(n_screen, 3, dtype=DTYPE, device=DEVICE)
    screen_comp = screen_comp / screen_comp.sum(dim=1, keepdim=True)
    screen_proc = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)
    screen_print = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)
    result = cost_aware_screening(
        models, screen_comp, screen_proc, screen_print,
        calphad_cost=1.0, full_cost=1301.0, threshold=0.7,
    )
    plot_cost_comparison(result, os.path.join(FIGURE_DIR, "cost_screening.png"))

    print(f"\n{'=' * 70}")
    print(f"All figures saved to {FIGURE_DIR}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
