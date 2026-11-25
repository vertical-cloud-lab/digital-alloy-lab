#!/usr/bin/env python3
"""Visualizations for the hard-sphere particle-packing BOFN benchmark.

Mirrors the style of ``benchmarks/bofn_pkgfn_visualize.py`` (PR #58) but for
the proposed 6-node particle-packing cascade described in
``edison-trajectories/crabnet-particle-packing-bofn-plan.md``:

  Stage 1 (FBA force-biased pack)        Stage 2 (LS Lubachevsky-Stillinger)
    Node 0  FBA-lo  (n_p=128)    -->       Node 3  LS-lo  (n_p=128)
    Node 1  FBA-mid (n_p=512)    -->       Node 4  LS-mid (n_p=512)
    Node 2  FBA-hi  (n_p=2048)   -->       Node 5  LS-hi  (n_p=2048)

Each ``(stage, n_particles)`` cell is its own DAG node; ``n_particles`` is
fixed by node identity, not a continuous knob. Per-node outputs are packing
fraction phi, runtime t, and failure probability P_fail.

Generates two artifacts under ``benchmarks/figures/particle_packing/``:

  1. ``particle_packing_dag.png`` -- 6-node DAG (3 fidelity levels per
     stage, FBA-K -> LS-K matched-fidelity edges) with cost / failure
     annotations sourced from the verified Zenodo snapshot
     (10.5281/zenodo.7513019); structurally analogous to ``pkgfn_dag.png``.
  2. ``particle_packing_emulator_diagnostics.png`` -- 2x3 parity grid for the
     six emulator targets (``fba_isna_prob``, ``ls_isna_prob``, ``fba``,
     ``ls``, ``fba_time_s``, ``ls_time_s``) trained from the cached Zenodo
     CSVs; structurally analogous to ``node_correlations.png``.

The diagnostics panel is only rendered when the cached Zenodo CSVs are
available locally (default ``$PARTICLE_PACKING_DATA`` or
``benchmarks/data/particle_packing/``). The DAG always renders.

Usage::

    python benchmarks/particle_packing_visualize.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURE_DIR = REPO_ROOT / "benchmarks" / "figures" / "particle_packing"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Mirror the PR #58 palette so this figure can sit next to pkgfn_dag.png
# without requiring a new colour key.
NODE_COLORS = {0: "#43A047", 1: "#1E88E5"}

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


# ── Figure 1: Particle-packing two-stage cascade DAG ─────────────────────

def plot_particle_packing_dag(save_path: Path) -> None:
    """Draw the 6-node 3-fidelity-per-stage DAG.

    Two stages (FBA force-biased pack, LS Lubachevsky--Stillinger refinement)
    each split into three discrete fidelity nodes at n_particles in
    {128, 512, 2048}. Each LS-K node consumes the matched-fidelity FBA-K
    output, so the DAG has 3 parallel two-node cascades.

    Cost badges show approximate per-node runtime. The n_particles=128
    timings are smoke-test values from the bundled PackingGeneration.exe in
    matsci-opt-benchmarks==0.2.3 (FBA ~0.01 s, LS ~1.6 s); the 512 / 2048
    cells scale roughly as n_particles for FBA and super-linearly for LS.
    """
    fig, ax = plt.subplots(figsize=(11, 6.0))
    ax.set_xlim(-1.2, 11)
    ax.set_ylim(-2.5, 5.6)
    ax.axis("off")
    fig.suptitle(
        "Particle-Packing BOFN Cascade — 6 nodes, 3 fidelities per stage "
        "(Baird, Issa, Sparks 2023)",
        fontsize=12, fontweight="bold", y=0.97,
    )

    # Two stages laid out left-to-right; three discrete fidelity rows
    # ordered top-to-bottom as lo / mid / hi so Node 0 = FBA-lo (matches
    # the design-doc indexing in crabnet-particle-packing-bofn-plan.md §2.2).
    fidelities = [
        ("lo",  "n_p=128",  3.6, "~0.01 s", "~1.6 s"),
        ("mid", "n_p=512",  1.4, "~0.05 s", "~25 s"),
        ("hi",  "n_p=2048", -0.8, "~5.0 s", "~600 s"),
    ]

    nodes = []
    for label_suffix, fid_label, y, fba_cost, ls_cost in fidelities:
        nodes.append({
            "x": 1.5, "y": y,
            "label": f"Node {len(nodes)}\nFBA-{label_suffix}",
            "dim": fid_label,
            "cost": fba_cost,
            "color": NODE_COLORS[0],
        })
    for label_suffix, fid_label, y, fba_cost, ls_cost in fidelities:
        nodes.append({
            "x": 6.5, "y": y,
            "label": f"Node {len(nodes)}\nLS-{label_suffix}",
            "dim": fid_label,
            "cost": ls_cost,
            "color": NODE_COLORS[1],
        })

    for nd in nodes:
        box = mpatches.FancyBboxPatch(
            (nd["x"] - 1.1, nd["y"] - 0.55), 2.2, 1.1,
            boxstyle="round,pad=0.10", facecolor=nd["color"], alpha=0.15,
            edgecolor=nd["color"], linewidth=2,
        )
        ax.add_patch(box)
        ax.text(nd["x"], nd["y"] + 0.18, nd["label"], ha="center", va="center",
                fontsize=8.5, fontweight="bold", color=nd["color"])
        ax.text(nd["x"], nd["y"] - 0.22, nd["dim"], ha="center", va="center",
                fontsize=7.5, color="gray")
        ax.text(nd["x"] + 1.05, nd["y"] + 0.7, nd["cost"],
                ha="center", va="bottom", fontsize=8, fontweight="bold",
                color=nd["color"],
                bbox=dict(boxstyle="round,pad=0.12", fc="white",
                          ec=nd["color"], alpha=0.85, lw=1.0))

    # Edges: FBA-K -> LS-K (matched-fidelity sequential cascade).
    for k in range(3):
        src, dst = nodes[k], nodes[k + 3]
        ax.annotate(
            "", xy=(dst["x"] - 1.1, dst["y"]),
            xytext=(src["x"] + 1.1, src["y"]),
            arrowprops=dict(arrowstyle="-|>", color="#666", lw=1.6),
        )
    ax.text(4.0, fidelities[0][2] + 1.05,
            "matched-fidelity FBA-K → LS-K (sequential)",
            ha="center", va="bottom", fontsize=8.5,
            color="#555", fontstyle="italic")

    # Stage headers (above the caption, above the top row of nodes).
    ax.text(1.5, fidelities[0][2] + 1.6, "Stage 1: FBA pack",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color=NODE_COLORS[0])
    ax.text(6.5, fidelities[0][2] + 1.6, "Stage 2: LS refine",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color=NODE_COLORS[1])

    # External inputs box -- 9 shared design vars enter every node.
    ax.text(4.0, -2.0,
            "Decision vars: 9 shared (mu1..3, std1..3, comp1..2, "
            "safety_factor); n_particles is fixed by node identity",
            ha="center", va="center", fontsize=8, color="#777",
            bbox=dict(boxstyle="round,pad=0.25", fc="#F5F5F5",
                      ec="#bbb", lw=0.8))

    # Output annotation: 3 candidate terminal objectives, one per fidelity.
    ax.text(9.7, fidelities[0][2],
            "Network outputs (per LS node)\nphi (max), t (min), P_fail (min)",
            ha="left", va="center", fontsize=8, fontweight="bold",
            color=NODE_COLORS[1],
            bbox=dict(boxstyle="round,pad=0.2", fc="#E3F2FD",
                      ec=NODE_COLORS[1], lw=1.0))

    # Footer: data sources
    ax.text(5, -2.4,
            "Data: Zenodo 10.5281/zenodo.7513019 (raw CSVs) and "
            "10.5281/zenodo.7696165 (surrogate); "
            "code: sparks-baird/matsci-opt-benchmarks v0.2.3",
            ha="center", va="center", fontsize=7, color="#888")

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


# ── Figure 2: Emulator diagnostics (parity grid) ─────────────────────────

def _resolve_data_dir() -> Path | None:
    explicit = os.environ.get("PARTICLE_PACKING_DATA")
    if explicit:
        return Path(explicit)
    candidate = REPO_ROOT / "benchmarks" / "data" / "particle_packing"
    if (candidate / "sobol_probability_filter.csv").exists() and (
        candidate / "sobol_regression.csv"
    ).exists():
        return candidate
    return None


def plot_emulator_diagnostics(save_path: Path, data_dir: Path) -> None:
    """Train a lightweight RF smoke emulator and render a 2x3 parity grid.

    Uses the exact target decomposition documented in
    ``matsci-opt-benchmarks/notebooks/particle_packing/1.2-ri-surrogate.ipynb``:
    common features for the P_fail filters and an extra percentile-rank
    feature for the regression targets.
    """
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error

    prob = pd.read_csv(data_dir / "sobol_probability_filter.csv")
    reg = pd.read_csv(data_dir / "sobol_regression.csv")

    common = [
        "mu1_div_mu3", "mu2_div_mu3", "std1", "std2", "std3",
        "comp1", "comp2", "num_particles", "safety_factor",
    ]

    panels = []
    for target in ("fba_isna_prob", "ls_isna_prob"):
        train = prob.sample(n=2000, random_state=13)
        test = prob.drop(train.index).sample(n=500, random_state=17)
        m = RandomForestRegressor(
            n_estimators=16, max_depth=12, random_state=13, n_jobs=1,
        )
        m.fit(train[common], train[target])
        pred = m.predict(test[common])
        mae = mean_absolute_error(test[target], pred)
        panels.append((target, np.asarray(test[target]), np.asarray(pred), mae))

    for target, rank in (
        ("fba", "fba_rank"),
        ("ls", "ls_rank"),
        ("fba_time_s", "fba_time_s_rank"),
        ("ls_time_s", "ls_time_s_rank"),
    ):
        df = reg.dropna(subset=[target])
        feats = common + [rank]
        train = df.sample(n=min(4000, len(df)), random_state=13)
        test = df.drop(train.index).sample(n=500, random_state=17)
        m = RandomForestRegressor(
            n_estimators=16, max_depth=14, random_state=13, n_jobs=1,
        )
        m.fit(train[feats], train[target])
        pred = m.predict(test[feats])
        mae = mean_absolute_error(test[target], pred)
        panels.append((target, np.asarray(test[target]), np.asarray(pred), mae))

    fig, axes = plt.subplots(2, 3, figsize=(10.5, 7))
    fig.suptitle(
        "Particle-Packing Emulator Diagnostics (RF, Zenodo 7513019 smoke test)",
        fontsize=12, fontweight="bold", y=0.98,
    )

    titles = {
        "fba_isna_prob": "P(fail | FBA)",
        "ls_isna_prob": "P(fail | LS)",
        "fba": "phi_lo (FBA packing fraction)",
        "ls": "phi_hi (LS packing fraction)",
        "fba_time_s": "t_lo (FBA runtime, s)",
        "ls_time_s": "t_hi (LS runtime, s)",
    }
    units = {
        "fba_isna_prob": "", "ls_isna_prob": "",
        "fba": "", "ls": "", "fba_time_s": " s", "ls_time_s": " s",
    }

    for ax, (target, y_true, y_pred, mae) in zip(axes.ravel(), panels):
        lo = float(np.min([y_true.min(), y_pred.min()]))
        hi = float(np.max([y_true.max(), y_pred.max()]))
        ax.scatter(y_true, y_pred, s=8, alpha=0.4, color="#1E88E5",
                   edgecolors="none")
        ax.plot([lo, hi], [lo, hi], "--", color="#888", lw=1)
        ax.set_xlabel("ground truth")
        ax.set_ylabel("emulator prediction")
        ax.set_title(titles.get(target, target), fontsize=10)
        ax.text(0.04, 0.96, f"MAE = {mae:.3g}{units.get(target, '')}",
                transform=ax.transAxes, ha="left", va="top",
                fontsize=8.5, color="#333",
                bbox=dict(boxstyle="round,pad=0.2", fc="white",
                          ec="#bbb", alpha=0.85, lw=0.8))

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {save_path}")


def main() -> int:
    plot_particle_packing_dag(FIGURE_DIR / "particle_packing_dag.png")
    data_dir = _resolve_data_dir()
    if data_dir is None:
        print(
            "  Skipping emulator diagnostics: cached Zenodo CSVs not found.\n"
            "  Set $PARTICLE_PACKING_DATA or place "
            "sobol_probability_filter.csv + sobol_regression.csv under "
            "benchmarks/data/particle_packing/.",
            file=sys.stderr,
        )
        return 0
    plot_emulator_diagnostics(
        FIGURE_DIR / "particle_packing_emulator_diagnostics.png",
        data_dir,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
