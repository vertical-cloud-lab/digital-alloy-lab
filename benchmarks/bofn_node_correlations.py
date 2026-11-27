"""Node-vs-node correlation grid for the 6-node ExtendedManufacturingGPNetwork.

Generates a grid of scatter plots (parity-style) between every pair of node
outputs over a noiseless Sobol grid of the full input space, with Pearson R²
annotated on each off-diagonal panel. Useful for diagnosing whether the DAG
topology (0→1, 2, (1,2)→3, (x4,3)→4, (3,4)→5) is producing downstream nodes
that are largely linear functions of their parents (in which case BOFN's
per-node decomposition buys little over vanilla GP-EI on the final node).

Run::

    python benchmarks/bofn_node_correlations.py

Writes ``benchmarks/figures/node_correlations.png`` and a JSON summary of
all pairwise R² values next to it.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from botorch.utils.sampling import draw_sobol_samples

from benchmarks.partial_kgfn.manufacturing_problem import (
    ExtendedManufacturingGPNetwork,
)


def r_squared(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation squared (coefficient of determination for a
    least-squares linear fit y ≈ a·x + b)."""
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    r = np.corrcoef(x, y)[0, 1]
    return float(r * r)


def main(
    n_samples: int = 4096,
    seed: int = 0,
    out_png: str = "benchmarks/figures/node_correlations.png",
    out_json: str = "benchmarks/figures/node_correlations.json",
) -> None:
    problem = ExtendedManufacturingGPNetwork(
        node_costs=[5, 10, 10, 45, 20, 30], seed=0, noise_std=0.0,
        coupling=[0.0, 0.0, 0.0, 0.6, 0.8, 0.7],
    )
    bounds = problem.bounds
    grid = draw_sobol_samples(bounds=bounds, n=n_samples, q=1, seed=seed).squeeze(-2)
    with torch.no_grad():
        Y = problem.evaluate(grid, noiseless=True).cpu().numpy()  # (n_samples, 6)

    n_nodes = Y.shape[1]
    node_labels = [
        "y0 (CALPHAD)",
        "y1 (Powder)",
        "y2 (LPBF-in)",
        "y3 (LPBF-out)",
        "y4 (HT)",
        "y5 (Char)",
    ]

    fig, axes = plt.subplots(n_nodes, n_nodes, figsize=(14, 14))
    r2_matrix = np.full((n_nodes, n_nodes), np.nan)
    for i in range(n_nodes):
        for j in range(n_nodes):
            ax = axes[i, j]
            if i == j:
                ax.hist(Y[:, i], bins=40, color="steelblue", alpha=0.8)
                ax.set_yticks([])
                ax.text(
                    0.02, 0.95, node_labels[i],
                    transform=ax.transAxes, fontsize=9,
                    va="top", ha="left",
                )
            else:
                r2 = r_squared(Y[:, j], Y[:, i])
                r2_matrix[i, j] = r2
                ax.scatter(Y[:, j], Y[:, i], s=3, alpha=0.35, color="steelblue")
                # Least-squares fit line for visual reference.
                if np.std(Y[:, j]) > 0:
                    coef = np.polyfit(Y[:, j], Y[:, i], 1)
                    xs = np.linspace(Y[:, j].min(), Y[:, j].max(), 50)
                    ax.plot(xs, np.polyval(coef, xs), color="crimson", lw=1.0)
                ax.text(
                    0.02, 0.95, f"R²={r2:.3f}",
                    transform=ax.transAxes, fontsize=9,
                    va="top", ha="left",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none",
                              alpha=0.7),
                )
            if i == n_nodes - 1:
                ax.set_xlabel(node_labels[j], fontsize=8)
            else:
                ax.set_xticklabels([])
            if j == 0:
                ax.set_ylabel(node_labels[i], fontsize=8)
            else:
                ax.set_yticklabels([])
            ax.tick_params(labelsize=7)

    fig.suptitle(
        f"Node-vs-node correlations (ExtendedManufacturingGPNetwork, "
        f"n={n_samples} noiseless Sobol samples)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.975])

    out_png_path = Path(out_png)
    out_png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png_path, dpi=150)
    plt.close(fig)
    print(f"Wrote {out_png_path}")

    # Persist R² matrix + per-edge parent/child R² summaries.
    parents_of = problem.parent_nodes
    parent_child_r2 = {}
    for child, parents in enumerate(parents_of):
        for p in parents:
            key = f"y{p}->y{child}"
            parent_child_r2[key] = float(r2_matrix[child, p])

    payload = {
        "n_samples": int(n_samples),
        "seed": int(seed),
        "node_labels": node_labels,
        "r2_matrix": r2_matrix.tolist(),
        "parent_child_r2": parent_child_r2,
        "r2_y5_vs_each_node": {
            node_labels[j]: float(r2_matrix[5, j]) for j in range(n_nodes - 1)
        },
    }
    out_json_path = Path(out_json)
    out_json_path.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {out_json_path}")

    # Short console summary: R² of each node vs. the final output y5.
    print("\nR² of y5 (final) vs. each upstream node:")
    for j in range(n_nodes - 1):
        print(f"  {node_labels[j]:<14s}  R²={r2_matrix[5, j]:.3f}")
    print("\nParent→child R² (edges in the DAG):")
    for k, v in parent_child_r2.items():
        print(f"  {k:<8s}  R²={v:.3f}")


if __name__ == "__main__":
    main()
