#!/usr/bin/env python3
"""
Visualizations for the expanded 9-node BOFN DAG results.

Generates 4 figures:
  1. Expanded function network DAG (9 nodes with sub-node decomposition)
  2. Per-node GP prediction accuracy (9 nodes)
  3. LPBF process window heatmap (power × speed → density)
  4. Multi-stage cost screening funnel

Usage:
  python benchmarks/bofn_expanded_visualize.py
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from bofn_expanded_demo import (
    DTYPE, DEVICE, NODE_COSTS, FULL_PIPELINE_COST,
    calphad_fn, powder_psd_fn, powder_flow_fn, powder_density_fn,
    energy_delivery_fn, scan_strategy_fn, thermal_mgmt_fn,
    integration_fn, characterization_fn,
    keyhole_constraint, balling_constraint, lof_constraint,
    generate_expanded_data, build_expanded_gps,
    composite_forward_expanded, staged_screening,
    predict_node,
)

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})


# ── Figure 1: Expanded 9-Node DAG ──────────────────────────────────────────

def plot_expanded_dag(save_path):
    """Draw the expanded 9-node BOFN DAG with sub-node decomposition."""
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(-1, 17)
    ax.set_ylim(-3, 7)
    ax.axis("off")
    fig.suptitle("BOFN Expanded DAG v2 — Edison-Reviewed VCL Pipeline",
                 fontsize=14, fontweight="bold")

    # Node definitions: (x, y, label, dim, cost, color)
    nodes = {
        "calphad": (1, 3, "Node 0\nCALPHAD", "d=3→3", "$1", "#4CAF50"),
        "psd":     (4.5, 5, "Node 1a\nPSD", "d=4→1", "$50", "#2196F3"),
        "flow":    (4.5, 3, "Node 1b\nFlowability", "d=3→1", "$30", "#2196F3"),
        "dens":    (4.5, 1, "Node 1c\nDensity", "d=3→1", "$20", "#2196F3"),
        "energy":  (8, 5, "Node 2a\nEnergy", "d=5→2", "$100", "#FF9800"),
        "scan":    (8, 3, "Node 2b\nScan", "d=5→1", "$100", "#FF9800"),
        "thermal": (11, 3, "Node 2c\nThermal", "d=4→1", "$50", "#FF9800"),
        "density": (11, 5, "Node 2d\nIntegration", "d=3→1", "$200", "#FF9800"),
        "mech":    (14.5, 3, "Node 3\nCharacterization", "d=1→2", "$300", "#E91E63"),
    }

    # Draw nodes
    for key, (x, y, label, dim, cost, color) in nodes.items():
        w, h = 2.0, 1.2
        box = mpatches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.12", facecolor=color, alpha=0.2,
            edgecolor=color, linewidth=2,
        )
        ax.add_patch(box)
        ax.text(x, y + 0.1, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=color)
        ax.text(x, y - 0.38, dim, ha="center", va="center",
                fontsize=7.5, color="gray")
        ax.text(x, y + h/2 + 0.15, cost, ha="center", va="bottom",
                fontsize=8, fontweight="bold", color=color,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=color, alpha=0.8))

    # Edges (from_node, to_node)
    edges = [
        ("calphad", "psd"), ("calphad", "flow"), ("calphad", "dens"),
        ("psd", "energy"), ("dens", "energy"),
        ("energy", "scan"), ("energy", "density"),
        ("scan", "thermal"), ("scan", "density"),
        ("thermal", "density"),
        ("density", "mech"),
    ]

    for src, dst in edges:
        sx, sy = nodes[src][0], nodes[src][1]
        dx, dy = nodes[dst][0], nodes[dst][1]
        ax.annotate(
            "", xy=(dx - 0.9, dy), xytext=(sx + 0.9, sy),
            arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5,
                            connectionstyle="arc3,rad=0.1"),
        )

    # External decision inputs
    ext_inputs = [
        (1, -1.5, "Alloy composition\n(3 components)", "calphad"),
        (4.5, -1.5, "Atomization params\n(2 params)", "flow"),
        (8, -1.5, "LPBF Tier-A params\nP, v, σ, h, θ, c, T₀, t", "energy"),
    ]
    for ex, ey, label, target_key in ext_inputs:
        tx, ty = nodes[target_key][0], nodes[target_key][1]
        ax.annotate(
            "", xy=(tx, ty - 0.6), xytext=(ex, ey + 0.4),
            arrowprops=dict(arrowstyle="-|>", color="#999", lw=1.2, ls="--"),
        )
        ax.text(ex, ey, label, ha="center", va="top", fontsize=8, color="#666")

    # Output label
    mx, my = nodes["mech"][0], nodes["mech"][1]
    ax.text(mx, my - 1.5, "Yield strength\n(objective)", ha="center", va="top",
            fontsize=10, fontweight="bold", color="#E91E63",
            bbox=dict(boxstyle="round,pad=0.2", fc="#FCE4EC", ec="#E91E63"))
    ax.annotate("", xy=(mx, my - 0.95), xytext=(mx, my - 0.6),
                arrowprops=dict(arrowstyle="-|>", color="#E91E63", lw=1.5))

    # Stage grouping boxes
    for label, x_range, color in [
        ("CALPHAD\nStage", (-0.2, 2.2), "#4CAF50"),
        ("Powder\nStage", (3.2, 5.8), "#2196F3"),
        ("LPBF\nStage", (6.7, 12.3), "#FF9800"),
        ("Characterization\nStage", (13.2, 15.8), "#E91E63"),
    ]:
        rect = mpatches.FancyBboxPatch(
            (x_range[0], -0.3), x_range[1] - x_range[0], 6.6,
            boxstyle="round,pad=0.2", facecolor=color, alpha=0.04,
            edgecolor=color, linewidth=1, linestyle="--",
        )
        ax.add_patch(rect)
        ax.text((x_range[0] + x_range[1]) / 2, 6.5, label, ha="center",
                va="top", fontsize=8, color=color, fontstyle="italic")

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 2: Per-Node GP Accuracy ─────────────────────────────────────────

def plot_expanded_gp_accuracy(models, node_data, save_path):
    """Per-node GP prediction accuracy for the expanded 9-node DAG.

    Evaluates on held-out test data generated through the full DAG
    (not training inputs) to avoid overstating predictive performance.
    """
    node_configs = [
        ("calphad", "CALPHAD", "#4CAF50", calphad_fn, 3, 3),
        ("powder_psd", "Powder PSD", "#2196F3", None, 4, 1),
        ("powder_flow", "Powder Flow", "#2196F3", None, 3, 1),
        ("powder_dens", "Powder Density", "#2196F3", None, 3, 1),
        ("energy", "Energy Delivery", "#FF9800", None, 5, 2),
        ("scan", "Scan Strategy", "#FF9800", None, 5, 1),
        ("thermal", "Thermal Mgmt", "#FF9800", None, 4, 1),
        ("density", "Integration", "#FF9800", None, 3, 1),
        ("mech", "Characterization", "#E91E63", None, 1, 2),
    ]

    n_train = next(iter(node_data.values()))[0].shape[0]

    # Generate held-out test data through the full DAG with a different seed
    n_test = 40
    torch.manual_seed(99)
    test_data = generate_expanded_data(n_train=n_test)

    fig, axes = plt.subplots(3, 3, figsize=(15, 13))
    fig.suptitle(
        f"Per-Node GP Prediction Accuracy — Expanded 9-Node DAG\n"
        f"({n_train} train, {n_test} held-out test points per node)",
        fontsize=14, fontweight="bold",
    )

    for idx, (name, title, color, _, d_in, d_out) in enumerate(node_configs):
        ax = axes[idx // 3][idx % 3]
        model = models[name]

        # Use held-out test data from the DAG
        X_eval, Y_true_eval = test_data[name]

        with torch.no_grad():
            if isinstance(model, list):
                # Multi-output
                preds = []
                stds = []
                for m in model:
                    post = m.posterior(X_eval)
                    preds.append(post.mean)
                    stds.append(post.variance.sqrt())
                Y_pred = torch.cat(preds, dim=-1)
                Y_std = torch.cat(stds, dim=-1)
                # Use first output for scatter plot
                y_true = Y_true_eval[:, 0].numpy()
                y_pred = Y_pred[:, 0].numpy()
                y_std = Y_std[:, 0].numpy()
            else:
                post = model.posterior(X_eval)
                Y_pred = post.mean
                Y_std = post.variance.sqrt()
                y_true = Y_true_eval.squeeze().numpy()
                y_pred = Y_pred.squeeze().numpy()
                y_std = Y_std.squeeze().numpy()

        ax.errorbar(y_true, y_pred, yerr=1.96 * y_std, fmt="o", ms=4,
                     color=color, alpha=0.6, ecolor="lightgray", elinewidth=0.8,
                     capsize=2)
        lims = [min(y_true.min(), y_pred.min()) - 0.05,
                max(y_true.max(), y_pred.max()) + 0.05]
        ax.plot(lims, lims, "k--", lw=1, alpha=0.5)
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_xlabel("Ground Truth", fontsize=9)
        ax.set_ylabel("GP Predicted", fontsize=9)
        ax.set_title(f"{title} (d={d_in}→{d_out})", color=color,
                     fontweight="bold", fontsize=10)
        ax.set_aspect("equal", adjustable="box")

        # R²
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - y_true.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        ax.text(0.05, 0.95, f"R² = {r2:.3f}", transform=ax.transAxes,
                fontsize=8, va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 3: LPBF Process Window ──────────────────────────────────────────

def plot_lpbf_process_window(models, save_path):
    """Power × Speed process window showing predicted part density + constraints."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("LPBF Process Window — Power × Speed at Fixed Composition",
                 fontsize=14, fontweight="bold")

    resolution = 40
    power_grid = torch.linspace(0.05, 0.95, resolution, dtype=DTYPE)
    speed_grid = torch.linspace(0.05, 0.95, resolution, dtype=DTYPE)
    P, V = torch.meshgrid(power_grid, speed_grid, indexing="ij")
    P_flat = P.reshape(-1, 1)
    V_flat = V.reshape(-1, 1)
    n = P_flat.shape[0]

    # Fixed parameters for this slice
    fixed_comp = torch.tensor([[0.7, 0.2, 0.1]], dtype=DTYPE).expand(n, -1)
    fixed_atom = torch.tensor([[0.5, 0.5]], dtype=DTYPE).expand(n, -1)
    fixed_spot = torch.full((n, 1), 0.5, dtype=DTYPE)
    fixed_hatch = torch.full((n, 1), 0.5, dtype=DTYPE)
    fixed_rot = torch.full((n, 1), 0.5, dtype=DTYPE)
    fixed_contour = torch.full((n, 1), 0.5, dtype=DTYPE)
    fixed_preheat = torch.full((n, 1), 0.5, dtype=DTYPE)
    fixed_dwell = torch.full((n, 1), 0.5, dtype=DTYPE)

    # Forward pass through DAG
    with torch.no_grad():
        results = composite_forward_expanded(
            models, fixed_comp, fixed_atom, P_flat, V_flat, fixed_spot,
            fixed_hatch, fixed_rot, fixed_contour, fixed_preheat, fixed_dwell,
        )

    density = results["part_density"].reshape(resolution, resolution).numpy()
    ys = results["yield_strength"].reshape(resolution, resolution).numpy()
    melt_pool = results["melt_pool"]
    keyhole = keyhole_constraint(melt_pool).reshape(resolution, resolution).numpy()
    balling = balling_constraint(melt_pool).reshape(resolution, resolution).numpy()
    lof = lof_constraint(melt_pool, fixed_hatch.expand(n, -1)).reshape(
        resolution, resolution).numpy()

    P_np = P.numpy()
    V_np = V.numpy()

    # Panel 1: Part Density
    ax = axes[0]
    c = ax.contourf(P_np, V_np, density, levels=20, cmap="viridis")
    plt.colorbar(c, ax=ax, label="Part Density")
    ax.set_xlabel("Laser Power (normalized)")
    ax.set_ylabel("Scan Speed (normalized)")
    ax.set_title("Predicted Part Density", fontweight="bold")

    # Panel 2: Yield Strength
    ax = axes[1]
    c = ax.contourf(P_np, V_np, ys, levels=20, cmap="plasma")
    plt.colorbar(c, ax=ax, label="Yield Strength")
    ax.set_xlabel("Laser Power (normalized)")
    ax.set_ylabel("Scan Speed (normalized)")
    ax.set_title("Predicted Yield Strength", fontweight="bold")

    # Panel 3: Constraint Map (now with LOF)
    ax = axes[2]
    # Feasible = all constraints < 0
    feasible = ((keyhole < 0) & (balling < 0) & (lof < 0)).astype(float)
    ax.contourf(P_np, V_np, feasible, levels=[0, 0.5, 1.0],
                colors=["#FFCDD2", "#C8E6C9"], alpha=0.7)
    ax.contour(P_np, V_np, keyhole, levels=[0], colors=["red"],
               linewidths=2, linestyles="--")
    ax.contour(P_np, V_np, balling, levels=[0], colors=["blue"],
               linewidths=2, linestyles="--")
    ax.contour(P_np, V_np, lof, levels=[0], colors=["orange"],
               linewidths=2, linestyles=":")

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        mpatches.Patch(facecolor="#C8E6C9", label="Feasible region"),
        Line2D([0], [0], color="red", ls="--", lw=2, label="Keyhole (δ>0.8)"),
        Line2D([0], [0], color="blue", ls="--", lw=2, label="Balling (πw/l<1)"),
        Line2D([0], [0], color="orange", ls=":", lw=2, label="LOF (H²/W²+L²/D²>1)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8)
    ax.set_xlabel("Laser Power (normalized)")
    ax.set_ylabel("Scan Speed (normalized)")
    ax.set_title("LPBF Constraint Map", fontweight="bold")

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 4: Multi-Stage Cost Screening ───────────────────────────────────

def plot_expanded_cost_screening(screening_result, save_path):
    """Multi-stage screening funnel with cost breakdown for the expanded DAG."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Multi-Stage Cost-Aware Screening — 9-Node Expanded DAG",
                 fontsize=14, fontweight="bold")

    stages = screening_result["stages"]

    # Left: cost breakdown by stage
    ax = axes[0]
    stage_names = [s["name"] for s in stages]
    stage_costs = [s["cost"] for s in stages]
    colors = ["#4CAF50", "#FF9800", "#E91E63"][:len(stages)]

    bars = ax.bar(stage_names, stage_costs, color=colors, alpha=0.8,
                  edgecolor="white", linewidth=1.5)
    for bar, cost in zip(bars, stage_costs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                f"${cost:,.0f}", ha="center", va="bottom", fontsize=10,
                fontweight="bold")

    # Add naive cost bar
    ax.bar(["Naive\n(no screening)"], [screening_result["naive_cost"]],
           color="#9E9E9E", alpha=0.5, edgecolor="white", linewidth=1.5)
    ax.text(len(stages), screening_result["naive_cost"] + 200,
            f"${screening_result['naive_cost']:,.0f}", ha="center",
            va="bottom", fontsize=10, fontweight="bold", color="#666")

    ax.set_ylabel("Cost ($)")
    ax.set_title("Cost Breakdown by Stage", fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Right: screening funnel
    ax2 = axes[1]
    funnel_stages = [f"Start\n(n={screening_result['n_total']})"]
    funnel_counts = [screening_result["n_total"]]
    funnel_colors = ["#78909C"]

    for i, s in enumerate(stages):
        funnel_stages.append(f"After {s['name']}\n(n={s['n_out']})")
        funnel_counts.append(s["n_out"])
        funnel_colors.append(colors[i % len(colors)])

    bars2 = ax2.barh(funnel_stages[::-1], funnel_counts[::-1],
                      color=funnel_colors[::-1], alpha=0.8,
                      edgecolor="white", linewidth=1.5, height=0.6)

    for bar, count in zip(bars2, funnel_counts[::-1]):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{count}", ha="left", va="center", fontsize=11,
                 fontweight="bold")

    savings_pct = screening_result.get("savings_pct", 0)
    ax2.set_xlabel("Number of Candidates")
    ax2.set_title(f"Screening Funnel — {savings_pct:.0f}% Cost Savings",
                  fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # Savings annotation
    ax2.text(0.95, 0.05,
             f"Total: ${screening_result.get('total_cost', 0):,.0f}\n"
             f"Naive: ${screening_result['naive_cost']:,.0f}\n"
             f"Savings: ${screening_result.get('savings', 0):,.0f}",
             transform=ax2.transAxes, fontsize=10, va="bottom", ha="right",
             bbox=dict(boxstyle="round,pad=0.4", fc="#E8F5E9", ec="#4CAF50", alpha=0.9))

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("BOFN Expanded Visualization — Generating Figures")
    print("=" * 70)

    # 1. Generate data and fit models
    print("\n[1/5] Generating data and fitting GP models...")
    torch.manual_seed(42)
    node_data = generate_expanded_data(n_train=50)
    models = build_expanded_gps(node_data)

    # 2. Expanded DAG diagram
    print("\n[2/5] Drawing expanded 9-node DAG...")
    plot_expanded_dag(os.path.join(FIGURE_DIR, "expanded_dag.png"))

    # 3. GP accuracy for all 9 nodes
    print("\n[3/5] Plotting per-node GP prediction accuracy...")
    plot_expanded_gp_accuracy(models, node_data,
                              os.path.join(FIGURE_DIR, "expanded_gp_accuracy.png"))

    # 4. LPBF process window
    print("\n[4/5] Plotting LPBF process window...")
    plot_lpbf_process_window(models,
                             os.path.join(FIGURE_DIR, "lpbf_process_window.png"))

    # 5. Cost screening
    print("\n[5/5] Plotting multi-stage cost screening...")
    torch.manual_seed(42)
    n_screen = 50
    comp = torch.rand(n_screen, 3, dtype=DTYPE, device=DEVICE)
    comp = comp / comp.sum(dim=1, keepdim=True)
    atom_params = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)
    power = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    speed = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    spot_size = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    hatch = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    rotation = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    contour = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    preheat = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    dwell = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)

    screening = staged_screening(
        models, comp, atom_params, power, speed, spot_size,
        hatch, rotation, contour, preheat, dwell,
    )
    plot_expanded_cost_screening(screening,
                                 os.path.join(FIGURE_DIR, "expanded_cost_screening.png"))

    # Save raw data for Edison review
    first_data = next(iter(node_data.values()))
    n_training = int(first_data[0].shape[0])
    raw_data = {
        "dag_nodes": 9,
        "global_dim": 14,
        "max_per_node_dim": 5,
        "n_training": n_training,
        "n_screening": 50,
        "screening_result": {
            "n_total": screening["n_total"],
            "stages": screening["stages"],
            "total_cost": screening.get("total_cost", 0),
            "naive_cost": screening["naive_cost"],
            "savings": screening.get("savings", 0),
            "savings_pct": screening.get("savings_pct", 0),
        },
        "node_costs": NODE_COSTS,
        "full_pipeline_cost": FULL_PIPELINE_COST,
    }
    raw_path = os.path.join(FIGURE_DIR, "expanded_raw_data.json")
    with open(raw_path, "w") as f:
        json.dump(raw_data, f, indent=2, default=str)
    print(f"\n  Raw data saved: {raw_path}")

    print(f"\n{'=' * 70}")
    print(f"All figures saved to {FIGURE_DIR}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
