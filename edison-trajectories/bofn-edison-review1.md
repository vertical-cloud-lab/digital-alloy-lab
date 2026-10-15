Question: I am developing a Bayesian Optimization over Function Networks (BOFN) framework for alloy discovery 
via Laser Powder Bed Fusion (LPBF). Please review my implementation and provide critical feedback.

## Context
We are building the FLAIME (Federated Laboratory for AI-driven Materials Engineering) pipeline:
CALPHAD screening → powder atomization → LPBF printing → mechanical characterization.

The key challenge is jointly optimizing alloy composition (3 elements) AND LPBF process parameters 
(power, speed, hatch spacing, etc.) within a single BOFN framework. No published work does this.

## Architecture
9-node DAG decomposing the pipeline:
- Node 0: CALPHAD (d=3→2, composition → phase fraction + solidification range)
- Nodes 1a-c: Powder properties (PSD, flowability, apparent density, each d=3→1)
- Nodes 2a-d: LPBF sub-nodes (energy delivery d=5→2, scan strategy d=4→1, thermal mgmt d=3→1, integration d=3→1)
- Node 3: Characterization (d=1→1, part density → yield strength)

Global decision vector: d=14 (composition 3 + atomization 2 + LPBF Tier-A 8 + passthrough 1)
Max per-node d=5 (SAASBO compatible)

## Key Design Decisions (to review)
1. **Joint composition-process optimization (Option A)**: BOFN discovers composition-dependent optimal LPBF 
   params through the DAG structure, rather than a two-stage approach
2. **LPBF sub-node decomposition**: 4 sub-nodes (energy, scan, thermal, integration) keep per-node d≤5
3. **Independent GPs for multi-output nodes**: CALPHAD and energy delivery use separate GPs per output dimension
4. **Constraint modeling**: Keyholing (depth/width > 1.5) and balling (width < 0.2) as constraint functions
5. **Multi-stage screening**: CALPHAD first ($1/ea), then powder+LPBF ($750/ea), then characterization ($300/ea)

## Results
- All 9 nodes fit with SingleTaskGP + Normalize/Standardize transforms
- Composite forward pass propagates correctly through the DAG
- Predicted vs ground truth: close agreement (in-sample R² > 0.95 for most nodes)
- Multi-stage screening achieves ~62-68% cost savings vs naive evaluation
- Fully Bayesian variant (SaasFullyBayesianSingleTaskGP) verified compatible

## Raw Screening Data
{
  "dag_nodes": 9,
  "global_dim": 14,
  "max_per_node_dim": 5,
  "n_training": 30,
  "n_screening": 50,
  "screening_result": {
    "n_total": 50,
    "stages": [
      {
        "name": "CALPHAD screening",
        "n_in": 50,
        "n_out": 19,
        "cost": 50.0
      },
      {
        "name": "Powder + LPBF",
        "n_in": 19,
        "n_out": 19,
        "cost": 14250.0
      },
      {
        "name": "Mechanical characterization",
        "n_in": 19,
        "n_out": 19,
        "cost": 5700.0
      }
    ],
    "total_cost": 20000.0,
    "naive_cost": 52550.0,
    "savings": 32550.0,
    "savings_pct": 61.94100856327307
  },
  "node_costs": {
    "calphad": 1.0,
    "powder_psd": 50.0,
    "powder_flow": 30.0,
    "powder_dens": 20.0,
    "energy": 100.0,
    "scan": 100.0,
    "thermal": 50.0,
    "density": 200.0,
    "mech": 300.0
  },
  "full_pipeline_cost": 1051.0
}

## Questions for review
1. Is the sub-node decomposition of LPBF physically reasonable? Should energy delivery inputs include 
   apparent density alongside PSD and flowability?
2. For the scan strategy node, is melt pool width the correct upstream input, or should it also receive depth?
3. The thermal management node uses layer_quality + preheat + dwell. Should it also receive melt pool geometry?
4. Are the synthetic ground-truth functions (sigmoid-based) adequate for validating the framework, or 
   should we use physics-based models (e.g., Rosenthal solution for melt pool)?
5. The constraint functions use simple threshold logic. For real LPBF, keyholing depends on normalized 
   enthalpy (P/(v*σ*h_sl)), not just depth/width ratio. How should we improve this?
6. Is 30 training points per node sufficient for d=5 (energy delivery), or should we scale to ~50-100?
7. For the cost model: are the node costs realistic? ($1 CALPHAD, $50 PSD, $100 single-track, $200 density cube, $300 tensile test)
8. What is missing from this framework that would be needed before deploying it on real alloy discovery campaigns?

## Implementation Code (key sections)

```python
#!/usr/bin/env python3
"""
BOFN Expanded DAG — Realistic LPBF Parameter Dimensionality

Implements the refined BOFN architecture based on Edison Scientific review
(tasks d0ad1eea, 6025bdcf) incorporating:

1. Sub-node decomposition of LPBF (Node 2) into 4 sub-nodes (2a-2d)
2. Multi-dimensional powder properties (3 key properties instead of 1 scalar)
3. Parameter tiering: 6 actively optimized Tier-A LPBF params, rest fixed
4. Joint composition-process optimization (Option A from Edison review)
5. SAASBO compatibility at each sub-node for automatic variable selection
6. Constraint modeling for LPBF physical limits (keyholing, balling, lack-of-fusion)

DAG topology:
  Node 0:  CALPHAD screening (composition d=3 → phase_fraction + solidification_range d=2)
  Node 1a: Powder PSD (phase_frac + atomization_params d=4 → D50 d=1)
  Node 1b: Powder flowability (phase_frac + atomization_params d=4 → Hausner_ratio d=1)
  Node 1c: Powder density (phase_frac + atomization_params d=4 → apparent_density d=1)
  Node 2a: Energy delivery (D50 + flowability + power + speed + spot_size d=5 → melt_pool_geom d=2)
  Node 2b: Scan strategy (melt_pool_width + hatch + rotation + contour d=4 → layer_quality d=1)
  Node 2c: Thermal mgmt (layer_quality + preheat + dwell d=3 → residual_stress d=1)
  Node 2d: Integration (melt_pool_depth + layer_quality + stress d=3 → part_density d=1)
  Node 3:  Characterization (part_density d=1 → yield_strength d=1)

Global decision vector x = [composition(3), atomization_params(2), power, speed,
                            spot_size, hatch, rotation, contour, preheat, dwell]
Total d=14, of which composition=3, atomization=2, LPBF Tier-A=8, plus 1 passthrough.

References:
  - Astudillo & Frazier (2021), "Bayesian Optimization of Function Networks", NeurIPS
  - Buathong & Frazier (2025), "Fast Bayesian Optimization of Function Networks"
  - Eriksson & Jankowiak (2021), "SAASBO", UAI (290 citations)
  - Edison task d0ad1eea: BOFN LPBF dimensionality review
  - Edison task 6025bdcf: BOFN LPBF implementation review

Usage:
  python benchmarks/bofn_expanded_demo.py
"""

import torch
from botorch.models import SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood

torch.manual_seed(42)
DTYPE = torch.double
DEVICE = torch.device("cpu")

# ---------------------------------------------------------------------------
# Per-node costs (USD) — from VCL pipeline estimates
# ---------------------------------------------------------------------------
NODE_COSTS = {
    "calphad": 1.0,       # Node 0: CALPHAD evaluation
    "powder_psd": 50.0,   # Node 1a: PSD measurement
    "powder_flow": 30.0,  # Node 1b: Flowability test
    "powder_dens": 20.0,  # Node 1c: Apparent density
    "energy": 100.0,      # Node 2a: Single-track experiments
    "scan": 100.0,        # Node 2b: Multi-track pads
    "thermal": 50.0,      # Node 2c: Thermal monitoring
    "density": 200.0,     # Node 2d: Density cube
    "mech": 300.0,        # Node 3: Tensile testing
}
ATOMIZATION_COST = 200.0  # Ultrasonic atomization per composition
FULL_PIPELINE_COST = sum(NODE_COSTS.values()) + ATOMIZATION_COST


# ---------------------------------------------------------------------------
# Synthetic ground-truth functions for each node
# ---------------------------------------------------------------------------

def calphad_fn(composition):
    """Node 0: CALPHAD screening.
    composition (n, 3) → [phase_fraction, solidification_range] (n, 2).
    """
    center = torch.tensor([0.7, 0.2, 0.1], dtype=DTYPE, device=DEVICE)
    dist_sq = ((composition - center) ** 2).sum(dim=-1, keepdim=True)
    phase_frac = torch.exp(-8.0 * dist_sq)
    # Solidification range: narrower near optimal composition
    solid_range = 0.3 + 0.7 * (1.0 - phase_frac)
    return torch.cat([phase_frac, solid_range], dim=-1)


def powder_psd_fn(phase_frac, atom_params):
    """Node 1a: Powder PSD D50.
    phase_frac (n,1) + atomization_params (n,2) → D50 (n,1).
    D50 in normalized [0,1] range (0=fine, 1=coarse).
    """
    x = torch.cat([phase_frac, atom_params], dim=-1)
    return torch.sigmoid(0.5 * x[..., 0:1] + 0.8 * x[..., 1:2] - 0.3 * x[..., 2:3])


def powder_flow_fn(phase_frac, atom_params):
    """Node 1b: Powder flowability (Hausner ratio proxy).
    phase_frac (n,1) + atomization_params (n,2) → flowability (n,1).
    Higher = better flowability (normalized [0,1]).
    """
    x = torch.cat([phase_frac, atom_params], dim=-1)
    return 0.4 + 0.3 * torch.cos(x[..., 1:2]) + 0.2 * x[..., 0:1] + 0.1 * x[..., 2:3]


def powder_density_fn(phase_frac, atom_params):
    """Node 1c: Powder apparent density.
    phase_frac (n,1) + atomization_params (n,2) → apparent_density (n,1).
    Normalized [0,1].
    """
    x = torch.cat([phase_frac, atom_params], dim=-1)
    return 0.5 + 0.2 * x[..., 0:1] + 0.15 * x[..., 1:2] + 0.1 * torch.sin(3 * x[..., 2:3])


def energy_delivery_fn(d50, flowability, power, speed, spot_size):
    """Node 2a: Energy delivery → melt pool geometry.
    d50 (n,1) + flowability (n,1) + power (n,1) + speed (n,1) + spot_size (n,1)
    → [melt_pool_width, melt_pool_depth] (n,2).
    """
    # Melt pool width: primarily power/speed/spot dependent
    width = torch.sigmoid(2.0 * power - 1.5 * speed + 0.8 * spot_size
                          - 0.3 * d50 + 0.2 * flowability)
    # Melt pool depth: power/speed dominant, powder has less effect
    depth = torch.sigmoid(2.5 * power - 2.0 * speed + 0.3 * spot_size
                          - 0.1 * d50)
    return torch.cat([width, depth], dim=-1)


def scan_strategy_fn(melt_pool_width, hatch, rotation, contour):
    """Node 2b: Scan strategy → layer quality.
    melt_pool_width (n,1) + hatch (n,1) + rotation (n,1) + contour (n,1)
    → layer_quality (n,1).
    """
    # Layer quality depends on overlap (width vs hatch) and strategy
    overlap = melt_pool_width / hatch.clamp(min=0.01)  # avoid div by zero
    quality = torch.sigmoid(overlap - 0.5 + 0.3 * rotation + 0.2 * contour)
    return quality


def thermal_mgmt_fn(layer_quality, preheat, dwell):
    """Node 2c: Thermal management → residual stress.
    layer_quality (n,1) + preheat (n,1) + dwell (n,1) → residual_stress (n,1).
    Lower stress is better (normalized [0,1]).
    """
    # Residual stress reduced by preheat and dwell time
    stress = torch.sigmoid(1.0 - 0.5 * preheat - 0.3 * dwell
                           - 0.4 * layer_quality + 0.2)
    return stress


def integration_fn(melt_pool_depth, layer_quality, stress):
    """Node 2d: Integration → part density.
    melt_pool_depth (n,1) + layer_quality (n,1) + stress (n,1) → part_density (n,1).
    """
    # Part density depends on all upstream LPBF factors
    density = torch.sigmoid(1.5 * melt_pool_depth + 1.0 * layer_quality
                            - 0.8 * stress)
    return density


def characterization_fn(part_density):
    """Node 3: Characterization.
    part_density (n,1) → yield_strength (n,1).
    """
    return 0.7 * part_density + 0.3 * torch.sin(4.0 * part_density)


# ---------------------------------------------------------------------------
# Constraint functions for LPBF physical limits
# ---------------------------------------------------------------------------

def keyhole_constraint(melt_pool_geom):
    """Keyholing constraint: depth/width ratio must be < 1.5.
    Returns: negative = feasible, positive = infeasible.
    """
    width = melt_pool_geom[..., 0:1].clamp(min=0.01)
    depth = melt_pool_geom[..., 1:2]
    ratio = depth / width
    return ratio - 1.5  # feasible when < 0


def balling_constraint(melt_pool_geom):
    """Balling constraint: track must be stable (width > threshold).
    Returns: negative = feasible, positive = infeasible.
    """
    width = melt_pool_geom[..., 0:1]
    return 0.2 - width  # feasible when width > 0.2


# -----
```

## Visualization Code (key sections)

```python
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
    keyhole_constraint, balling_constraint,
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
    fig.suptitle("BOFN Expanded DAG — VCL Pipeline with LPBF Sub-Node Decomposition",
                 fontsize=14, fontweight="bold")

    # Node definitions: (x, y, label, dim, cost, color)
    nodes = {
        "calphad": (1, 3, "Node 0\nCALPHAD", "d=3→2", "$1", "#4CAF50"),
        "psd":     (4.5, 5, "Node 1a\nPSD", "d=3→1", "$50", "#2196F3"),
        "flow":    (4.5, 3, "Node 1b\nFlowability", "d=3→1", "$30", "#2196F3"),
        "dens":    (4.5, 1, "Node 1c\nDensity", "d=3→1", "$20", "#2196F3"),
        "energy":  (8, 5, "Node 2a\nEnergy", "d=5→2", "$100", "#FF9800"),
        "scan":    (8, 3, "Node 2b\nScan", "d=4→1", "$100", "#FF9800"),
        "thermal": (11, 3, "Node 2c\nThermal", "d=3→1", "$50", "#FF9800"),
        "density": (11, 5, "Node 2d\nIntegration", "d=3→1", "$200", "#FF9800"),
        "mech":    (14.5, 3, "Node 3\nCharacterization", "d=1→1", "$300", "#E91E63"),
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
        ("psd", "energy"), ("flow", "energy"),
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
   
```


# Critical Review: BOFN Framework for Alloy Discovery via LPBF

## 1. Overall Assessment

The FLAIME pipeline represents an ambitious and largely well-motivated application of Bayesian Optimization of Function Networks (BOFN) to a joint composition–process optimization problem that, as the user correctly notes, has no direct precedent in the published literature. The BOFN framework is correctly grounded: each node function is modeled with an independent Gaussian process, intermediate observations are leveraged to improve sample efficiency, and the DAG structure enables cost-aware partial evaluations (astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 2-4). The recent work by Buathong & Frazier (2025) on fast BOFN with partial evaluations (p-KGFN) is directly relevant, as it enables cost-aware node selection—exactly what the staged screening pipeline requires (buathong2506fastbayesianoptimization pages 2-4, buathong2506fastbayesianoptimization pages 8-9).

The 9-node DAG decomposition is a creative engineering contribution. Keeping per-node dimensionality ≤5 is well-motivated for SAASBO compatibility, as the sparse axis-aligned subspace prior can effectively identify active dimensions and achieve strong optimization performance in high-dimensional settings (kudva2024efficientperformancebasedmpc pages 3-4, eriksson2021highdimensionalbayesianoptimization pages 7-9). However, several physics-critical gaps must be addressed before the framework can be deployed on real alloy discovery campaigns. Below, I address each of the eight review questions in detail.

The following table provides a comprehensive question-by-question assessment:

| Question Number | Topic | Assessment (strengths/weaknesses) | Recommendation | Priority |
|---|---|---|---|---|
| 1 | LPBF sub-node decomposition; apparent density as energy-delivery input | **Strength:** the 4-way LPBF split is physically plausible and keeps node dimensionality SAASBO-friendly. **Weakness:** Node 2a currently omits apparent density even though powder-bed state affects effective absorptivity, layer thickness, and melt behavior; however, literature is mixed on whether apparent density directly predicts final density, with PSD/coarse fraction often more predictive than bulk density alone. Your present choice of `D50 + flowability + power + speed + spot_size` is reasonable for a first surrogate, but it likely under-models powder-bed coupling. (field2020theeffectof pages 1-2, ziri2022combinedeffectof pages 1-2, ziri2022combinedeffectof pages 15-17, haferkamp2021effectofbimodal pages 7-9, haferkamp2021effectofbimodal pages 1-2) | Keep the 4-sub-node LPBF decomposition. Add **apparent density or powder-layer-density proxy** to Node 2a *if* you can measure it reproducibly; otherwise prefer a richer powder descriptor set: `PSD metrics + flowability + absorptivity/packing proxy`. If dimensionality is tight, replace single `D50` with two descriptors such as `D50` and `packing/absorptivity proxy`. | High |
| 2 | Scan strategy node inputs: width only vs width + depth | **Weakness:** using melt-pool width alone is not physically sufficient. Hatch overlap is width-driven, but lack-of-fusion and remelting depend jointly on width and depth. Analytical LOF criteria explicitly couple hatch spacing and layer thickness with melt-pool width and depth via a geometry condition, so omitting depth loses key failure physics. (wang2021analyticalpredictionof pages 4-6, wang2021analyticalpredictionof pages 6-7, bergmueller2023systematicapproachto pages 6-8) | Feed **both melt-pool width and depth** into the scan node. Minimum revision: `scan_strategy_fn(width, depth, hatch, rotation, contour)`. Better still, pass a derived overlap/remelt feature such as `overlap = width/hatch` and `penetration = depth/layer_thickness`. | Critical |
| 3 | Thermal management node should receive melt-pool geometry? | **Strength:** separating thermal management from scan strategy is sensible. **Weakness:** `layer_quality + preheat + dwell` is too compressed; residual stress depends on thermal gradients, heat accumulation, and melt-pool geometry/history, not just a scalar quality proxy. Literature shows residual heat, hatch spacing, scan length, and melt-pool depth evolve together and influence downstream quality/stress. (astudillo2021bayesianoptimizationof pages 6-8, bergmueller2023systematicapproachto pages 8-10, bergmueller2023systematicapproachto pages 6-8) | Add at least one melt-pool geometry input to thermal management, ideally `depth` and/or a thermal-intensity surrogate from Node 2a. A good minimal redesign is: `thermal_mgmt(layer_quality, melt_pool_depth, preheat, dwell)`; a better one is to include `width` too or a derived `β·L_th`-style thermal descriptor. | High |
| 4 | Synthetic ground-truth functions: sigmoid-based vs physics-based | **Strength:** sigmoids are fine for smoke-testing tensor plumbing, GP fitting, and DAG propagation. **Weakness:** they are too smooth, too monotone, and too forgiving to validate LPBF BOFN behavior under regime transitions, defect boundaries, and heteroscedasticity. Rosenthal-based models are more physical and cheap, but classical Rosenthal has limited fidelity because it assumes a point source, steady state, and neglects convection/radiation; normalized-enthalpy/scaling-law models capture conduction→transition→keyhole behavior better. (keeley2025adevelopmentof pages 14-16, plotkowski2017verificationandvalidation pages 5-8, keeley2025adevelopmentof pages 2-4, keeley2025adevelopmentof pages 7-9, keeley2025adevelopmentof pages 9-14, yang2020theanalyticalprediction pages 8-11) | Use a **tiered benchmark strategy**: (i) retain sigmoids for unit tests only; (ii) switch the LPBF synthetic truth to a **semi-physical model** combining Rosenthal/Eagar-Tsai-style melt-pool trends with normalized-enthalpy regime transitions and noise; (iii) inject discontinuities or sharp nonlinearities near LOF/keyhole boundaries. | Critical |
| 5 | Constraint functions: simple thresholds vs normalized enthalpy | **Weakness:** `depth/width > 1.5` and `width < 0.2` are too crude for real LPBF. Keyholing depends on absorbed-energy scaling, normalized enthalpy, and thermal diffusion length; balling is better tied to track geometry such as `πw/l > 1`; LOF depends on width, depth, hatch spacing, and layer thickness. Simple thresholds are acceptable for toy demos but not for deployment claims. (wang2021analyticalpredictionof pages 4-6, naderi2023onthefidelity pages 3-5, naderi2023onthefidelity pages 2-3, simonds2021thecausalrelationship pages 6-7, hanemann2020dimensionlessenthalpyas pages 1-2, wang2021analyticalpredictionof pages 6-7, wang2021analyticalpredictionof pages 7-10) | Replace hardcoded constraints with **physics-informed surrogate constraints**: keyholing via normalized enthalpy `ΔH/h_s` or `β·L_th` with threshold near the conduction→keyhole transition (~25–30 in the cited scaling-law framing), balling via `πw/l > 1`, and LOF via `H²/W² + L²/D² ≤ 1`. Model each as a noisy latent constraint GP, not deterministic threshold logic. | Critical |
| 6 | Training points: 30 per node for d=5 | **Strength:** 30 points is enough to prove code compatibility and get optimistic in-sample fits on smooth synthetic functions. **Weakness:** for a 5D node with nonlinear interactions and constraints, 30 is marginal and likely underpowered, especially if you move to more physical synthetic truths or real data. SAASBO can help when only a few variables are active, but it does not eliminate the need for more informative data. (kudva2024efficientperformancebasedmpc pages 3-4, kudva2024efficientperformancebasedmpc pages 2-3, eriksson2021highdimensionalbayesianoptimization pages 7-9) | Treat **30 as a minimum debugging dataset**, not a realistic modeling budget. For Node 2a target **~50 points minimum**, preferably **50–100** if you expect regime changes or noisy measurements. Use sequential DoE/BO to enrich high-curvature regions rather than uniform sampling only. | High |
| 7 | Cost model realism | **Strength:** the staged screening logic is directionally right and the cost funnel is one of the strongest parts of the framework. **Weakness:** some absolute costs appear optimistic or incomplete: `$1` for CALPHAD is only believable as marginal compute cost with existing infrastructure, not total labor/database/license cost; `$200` atomization per composition is likely understated for experimental alloy campaigns; downstream costs may also omit machine setup, coupons, polishing, CT/metallography, failed builds, and repeat measurements. No strong literature benchmark was found for universal cost values. (buathong2506fastbayesianoptimization pages 2-4, buathong2506fastbayesianoptimization pages 8-9) | Keep the cost-aware BOFN structure, but present costs as **scenario assumptions** with uncertainty bands: optimistic / nominal / conservative. Separate **marginal node cost** from **campaign overhead** and from **one-time infrastructure cost**. Add failure/rework probability and batching economics. | Medium |
| 8 | Missing elements before real deployment | **Strength:** the DAG and staged evaluation concept are strong foundations. **Weakness:** several deployment-critical pieces are missing: uncertainty propagation through the DAG; explicit composition-simplex constraints (`x_i ≥ 0`, `Σx_i = 1` or bounded sub-simplex); real CALPHAD/Scheil integration; hot-cracking susceptibility outputs (CSC / freezing range / stage-III solidification metrics); microstructure node(s); multi-fidelity structure; observation-noise models; experiment replication; batch/federated effects across labs; and qualification metrics beyond density→yield only. In its current form the network is a good research prototype, not yet a campaign-ready optimizer. (buathong2506fastbayesianoptimization pages 2-4, astudillo2021bayesianoptimizationof pages 2-4, wang2025calphadguidedinterlayerdesign pages 8-10, WO2024092273A2 pages 46-48, wang2025calphadguidedinterlayerdesign pages 4-5, keller2017applicationoffinite pages 20-23, keller2017applicationoffinite pages 3-5, wang2020uncertaintyquantificationand pages 1-4) | Add, in order: **(1)** composition constraints and physically meaningful domains, **(2)** CALPHAD/Scheil outputs including freezing range and CSC, **(3)** microstructure/intermediate-property nodes, **(4)** uncertainty-aware constrained acquisition, **(5)** multi-fidelity simulation/experiment coupling, **(6)** noise/replicate models and domain shift handling across labs, **(7)** richer terminal objectives such as strength-ductility-printability tradeoffs. | Critical |


*Table: This table gives a question-by-question technical review of the BOFN implementation, highlighting where the current design is strong, where it is physically incomplete, and which changes should be prioritized before moving toward real LPBF alloy discovery campaigns.*

## 2. Detailed Responses to Review Questions

### Q1: LPBF Sub-Node Decomposition and Apparent Density

The 4-node LPBF decomposition (energy, scan, thermal, integration) is physically reasonable as a first approximation. However, the energy delivery node currently receives D50 and flowability but omits apparent density. The literature presents a nuanced picture: Field et al. (2020) showed that plasma-spheroidized powder with higher packing density (57% vs 50% theoretical density) produced parts with substantially higher density (97.3% vs 88.5%) and 80% deeper laser penetration, directly linking powder-bed state to effective absorptivity and melt behavior (field2020theeffectof pages 1-2). Ziri et al. (2022) found that an effective volumetric energy density accounting for powder properties predicted porosity better than generalized energy density, with effective layer thickness (dependent on powder packing density) being the single most significant predictor (ziri2022combinedeffectof pages 15-17). However, Haferkamp et al. (2021) found that final part density was independent of measured bulk powder density and flowability for their tested conditions, instead correlating with coarse particle fraction and melt-pool fluctuation (haferkamp2021effectofbimodal pages 7-9, haferkamp2021effectofbimodal pages 1-2).

**Recommendation:** Add apparent density or a powder-layer-density proxy to Node 2a, replacing flowability if dimensionality is tight. The physically most important powder descriptors for the energy node are PSD (D50) and a packing/absorptivity proxy, as these govern effective layer thickness and laser coupling.

### Q2: Scan Strategy Node—Width Only vs. Width + Depth

This is a critical gap. The current implementation feeds only melt-pool width into the scan strategy node, but lack-of-fusion criteria explicitly depend on both width and depth. Wang et al. (2021) derived the analytical threshold H²/W² + L²/D² ≤ 1, where H is hatch spacing, L is layer thickness, W is melt-pool width, and D is melt-pool depth (wang2021analyticalpredictionof pages 4-6). Bergmueller et al. (2023) further showed that the transition from conduction to keyhole mode—and thus the available process window for hatch optimization—depends on aspect ratio δc = depth/width, with thresholds at δc = 0.5 (conduction-to-transition) and δc = 0.8 (transition-to-keyhole) (bergmueller2023systematicapproachto pages 6-8).

**Recommendation:** Feed both melt-pool width and depth into Node 2b. The revised node signature should be `scan_strategy_fn(width, depth, hatch, rotation, contour)` at d=5, which remains SAASBO-compatible.

### Q3: Thermal Management Node and Melt Pool Geometry

The thermal management node currently uses `layer_quality + preheat + dwell`, but residual stress in LPBF depends fundamentally on thermal gradients, which are governed by melt-pool geometry and energy input. Shrestha & Chou (2022) demonstrated that residual heat effects on melt-pool geometry vary with scan length, hatch spacing, and laser-turn regions, showing that melt-pool depth increases with track number while height decreases. The thermal management of the build is inherently coupled to melt-pool penetration depth and thermal intensity.

**Recommendation:** Add melt-pool depth as an input to Node 2c: `thermal_mgmt(layer_quality, melt_pool_depth, preheat, dwell)` at d=4. This gives the stress model a compact proxy for local thermal intensity without excessive dimensionality.

### Q4: Synthetic Ground-Truth Functions

The sigmoid-based synthetic functions are adequate for verifying tensor plumbing, GP fitting, and DAG propagation, but they are insufficient for validating the BOFN framework under realistic LPBF conditions. The Rosenthal equation provides a more physical baseline but has well-documented limitations: it assumes a point heat source, steady-state conditions, and temperature-independent properties, and it neglects convection, radiation, and latent heat (keeley2025adevelopmentof pages 14-16, plotkowski2017verificationandvalidation pages 5-8, keeley2025adevelopmentof pages 2-4). Keeley et al. (2025) showed that Rosenthal accurately predicted melt-pool width trends but systematically mispredicted length and cooling rates, with errors depending on the choice of thermal conductivity (keeley2025adevelopmentof pages 9-14). Plotkowski et al. (2017) noted that while Rosenthal has negligible computational cost and is suitable for generating steady-state process maps, it cannot represent transient effects, complex boundary conditions, or vaporization (plotkowski2017verificationandvalidation pages 5-8).

More importantly, the normalized enthalpy scaling laws offer a regime-transition-aware model: Rubenchik et al. and others showed that normalized melt-pool depth d/(2σ) scales linearly with normalized enthalpy β·L_th through an empirical constant K₀ ≈ 0.6 (naderi2023onthefidelity pages 3-5), and Fabbro's analysis placed the conduction-to-keyhole transition at ΔH/h_s ≈ 25–30 (naderi2023onthefidelity pages 2-3).

**Recommendation:** Adopt a tiered benchmarking strategy: (i) retain sigmoids for unit tests only; (ii) implement a semi-physical synthetic truth using Rosenthal/Eagar-Tsai melt-pool trends augmented with normalized enthalpy regime transitions; (iii) inject sharp nonlinearities near defect boundaries to test BOFN's ability to handle regime changes.

### Q5: Constraint Functions

The current `depth/width > 1.5` keyholing constraint and `width < 0.2` balling constraint are physically oversimplified. For keyholing, the literature strongly supports using normalized enthalpy as the governing parameter: ΔH is defined in terms of laser power, scan speed, absorption coefficient, beam diameter, and melting enthalpy h_s = ρC_pT_m, with keyholing onset predicted when ΔH/h_s exceeds a temperature-dependent threshold (wang2021analyticalpredictionof pages 4-6, yang2020theanalyticalprediction pages 11-14). King et al. and Bergmueller et al. showed that normalized enthalpy predicts the conduction-to-keyhole transition independently of specific processing parameters and machine type (hanemann2020dimensionlessenthalpyas pages 1-2, bergmueller2023systematicapproachto pages 8-10). For balling, the analytical criterion is πw/l > 1, where w and l are melt-pool width and length—when unsatisfied, balling occurs (wang2021analyticalpredictionof pages 4-6, wang2021analyticalpredictionof pages 7-10). For lack-of-fusion, the geometric criterion H²/W² + L²/D² ≤ 1 provides a physics-informed threshold (wang2021analyticalpredictionof pages 4-6).

**Recommendation:** Replace hardcoded thresholds with physics-informed constraint models: keyholing via normalized enthalpy ΔH/h_s with appropriate threshold, balling via πw/l stability criterion, and LOF via the geometric overlap condition. Ideally, model each as a probabilistic constraint GP rather than deterministic threshold logic.

### Q6: Training Data Sufficiency (30 Points for d=5)

For standard GP regression with d=5, a common guideline is ~10d = 50 training points as a minimum, though SAASBO can be more efficient when the effective dimensionality is lower. Eriksson & Jankowiak (2021) demonstrated that SAASBO quickly focuses on the most relevant parameters and outperforms baselines in high-dimensional settings (eriksson2021highdimensionalbayesianoptimization pages 7-9), while Kudva et al. (2024) noted that the SAAS prior can automatically identify important parameters from relatively small observation sets, but cautioned that problems with many sensitive parameters remain difficult and require larger budgets (kudva2024efficientperformancebasedmpc pages 3-4, kudva2024efficientperformancebasedmpc pages 2-3). The reported in-sample R² > 0.95 with 30 points on smooth sigmoid functions is expected and not informative about real-data performance.

**Recommendation:** Treat 30 points as a debugging dataset. For Node 2a (the highest-dimensional at d=5), target 50–100 training points, especially if moving to physics-based synthetic functions or real data with noise and regime transitions. Use sequential BO to enrich high-curvature regions rather than relying solely on uniform initial sampling.

### Q7: Cost Model Realism

The staged cost structure is one of the framework's strengths, and the 62% savings estimate is a compelling demonstration of cost-aware BOFN's value. However, some absolute costs appear optimistic: $1 per CALPHAD evaluation is reasonable only as marginal compute cost assuming existing software licenses and databases; $200 for atomization per composition likely understates the true cost for experimental alloy campaigns; and downstream costs may omit machine setup, specimen preparation, metallography, and failed-build rework. No universal cost benchmarks exist in the LPBF literature, so these values are necessarily scenario-specific.

**Recommendation:** Present costs as scenario assumptions with uncertainty bands (optimistic/nominal/conservative). Separate marginal node cost from campaign overhead and one-time infrastructure costs. Add failure/rework probability factors, as LPBF builds can fail, especially when exploring novel compositions.

### Q8: Missing Elements for Real Deployment

Several deployment-critical elements are absent from the current framework:

1. **Composition constraints:** The simplex constraint (x_i ≥ 0, Σx_i = 1 or bounded sub-simplex) is not implemented but is essential for alloy composition optimization.

2. **CALPHAD integration:** The current CALPHAD node uses a synthetic Gaussian-based function. Real deployment requires integration with Thermo-Calc, DICTRA, or equivalent tools that compute Scheil solidification paths, freezing ranges, and cracking susceptibility coefficients (wang2025calphadguidedinterlayerdesign pages 8-10, WO2024092273A2 pages 46-48, wang2025calphadguidedinterlayerdesign pages 4-5, keller2017applicationoffinite pages 20-23, keller2017applicationoffinite pages 3-5). Wang & Xiong (2020) demonstrated CALPHAD-based ICME frameworks that combine phase predictions, strengthening models, and weldability criteria for AM composition optimization (wang2020uncertaintyquantificationand pages 1-4).

3. **Hot-cracking susceptibility:** The Clyne-Davies CSC model—which quantifies cracking risk from the ratio of vulnerable-to-healing time during solidification—should be a key output of the CALPHAD node (WO2024092273A2 pages 46-48, wang2025calphadguidedinterlayerdesign pages 4-5).

4. **Microstructure node:** A node linking thermal history to grain morphology, texture, and precipitation would bridge the gap between process parameters and mechanical properties.

5. **Uncertainty propagation:** The BOFN framework models each node with an independent GP, but the implied posterior on the composite output is non-Gaussian (astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 2-4). Proper uncertainty propagation through the DAG is essential for credible acquisition function optimization and for quantifying prediction confidence.

6. **Multi-fidelity structure:** Rosenthal/analytical models are cheap (seconds), FEA/CFD simulations are moderate ($10–100), and physical experiments are expensive ($100–1000+). A multi-fidelity BOFN would dramatically improve efficiency.

7. **Noise models and replication:** Real LPBF data are noisy due to powder batch variability, environmental fluctuations, and measurement uncertainty. The current implementation does not address heteroscedastic noise or the need for experimental replication.

8. **Multi-objective terminal outputs:** Yield strength alone is insufficient; strength-ductility-printability tradeoffs are standard in alloy qualification.

## 3. Recommended Revised DAG Architecture

The following table summarizes the recommended revisions to each node, maintaining SAASBO compatibility (d ≤ 5 per node) while improving physical fidelity:

| Node | Current Design (inputs→outputs, dimension) | Recommended Revision | Physics Rationale |
|---|---|---|---|
| Node 0 — CALPHAD | composition → phase fraction + solidification range, `d=3→2` | composition → phase fraction + solidification range + CSC, `d=3→3` | Add a cracking susceptibility coefficient derived from Scheil/Clyne-Davies-style solidification metrics; freezing range and late-stage solid fraction evolution are directly tied to LPBF hot-cracking risk, so CALPHAD should output printability-relevant thermodynamic descriptors, not just phase fraction and range (wang2025calphadguidedinterlayerdesign pages 8-10, WO2024092273A2 pages 46-48, wang2025calphadguidedinterlayerdesign pages 4-5, wang2020uncertaintyquantificationand pages 1-4) |
| Node 1a — Powder PSD | phase fraction + atomization params → D50, `d≈3/4→1` | phase fraction + solidification range + atomization params → D50, `d≈4/5→1` | Include solidification range because alloy thermodynamics can influence atomization response, segregation tendency, and resulting particle-size behavior; this gives the powder branch a more physically meaningful link to composition-dependent printability (wang2025calphadguidedinterlayerdesign pages 8-10, wang2020uncertaintyquantificationand pages 1-4) |
| Node 1b — Flowability | phase fraction + atomization params → Hausner-ratio proxy, `d≈3/4→1` | Keep structure; use standardized flow metric (Hausner ratio or equivalent), `d≈3/4→1` | Flowability metrics such as Hausner ratio, apparent/tap density relations, and standard powder tests are common and interpretable; this node is already physically sensible as a distinct powder-processability descriptor (spurek2022influenceofthe pages 4-6, spurek2022influenceofthe pages 10-10) |
| Node 1c — Powder Density | phase fraction + atomization params → apparent density, `d≈3/4→1` | Keep structure; retain apparent density / powder-layer-density proxy, `d≈3/4→1` | Apparent density is a standard measurable powder descriptor and is useful as an upstream packing/absorptivity proxy even if it is not always the strongest direct predictor of final part density (ziri2022combinedeffectof pages 15-17, spurek2022influenceofthe pages 10-10) |
| Node 2a — Energy Delivery | D50 + flowability + power + speed + spot size → melt-pool width + depth, `d=5→2` | Preferred: D50 + apparent density + power + speed + spot size → width + depth, `d=5→2`; Alternative: add apparent density as 6th input if using SAAS/Fully Bayesian model can tolerate it, `d=6→2` | Powder-bed state changes effective absorptivity, packing, layer thickness, and melt behavior. Literature supports incorporating powder density/packing proxies into effective energy-delivery models, though PSD is often more predictive than bulk flowability alone (field2020theeffectof pages 1-2, ziri2022combinedeffectof pages 1-2, ziri2022combinedeffectof pages 15-17, xue2023effectofparticle pages 1-2) |
| Node 2b — Scan Strategy | melt-pool width + hatch + rotation + contour → layer quality, `d=4→1` | melt-pool width + melt-pool depth + hatch + rotation + contour → layer quality, `d=5→1` | Width controls overlap, but depth controls remelting and lack-of-fusion risk. LOF criteria explicitly depend on both width and depth relative to hatch spacing and layer thickness, so scan quality should not ignore depth (wang2021analyticalpredictionof pages 4-6, wang2021analyticalpredictionof pages 6-7) |
| Node 2c — Thermal Management | layer quality + preheat + dwell → residual stress, `d=3→1` | layer quality + melt-pool depth + preheat + dwell → residual stress, `d=4→1` | Residual stress depends on thermal gradients, heat accumulation, and melt-pool geometry; depth is a compact proxy for thermal penetration and local heat concentration, improving physical realism without excessive dimensionality (astudillo2021bayesianoptimizationof pages 6-8, bergmueller2023systematicapproachto pages 8-10) |
| Node 2d — Integration | melt-pool depth + layer quality + stress → part density, `d=3→1` | Keep as melt-pool depth + layer quality + stress → part density, `d=3→1` | This node already combines the main integration variables needed for final densification: penetration/remelt, layer continuity, and thermo-mechanical penalty. It is one of the more physically coherent parts of the current DAG (bergmueller2023systematicapproachto pages 6-8, ziri2022combinedeffectof pages 1-2) |
| Node 3 — Characterization | part density → yield strength, `d=1→1` | part density → yield strength + elongation, `d=1→2` | A single strength output is too narrow for real alloy discovery. LPBF qualification is inherently multi-property, and strength-ductility tradeoffs matter; expanding to multi-output characterization makes the terminal node more campaign-relevant (wang2020uncertaintyquantificationand pages 1-4, field2020theeffectof pages 1-2) |


*Table: This table summarizes a physics-informed revision of the 9-node BOFN DAG, showing how each node can be updated to better reflect LPBF and alloy-discovery mechanisms. It is useful for deciding which node changes improve realism while preserving manageable per-node dimensionality.*

## 4. Conclusions

The BOFN framework for joint composition–LPBF process optimization is a sound conceptual contribution with no direct published precedent. The 9-node DAG, cost-aware staged screening, and SAASBO compatibility are well-conceived design decisions. However, three categories of changes are needed before the framework can be considered deployment-ready:

**Critical fixes** (must address): (i) Add melt-pool depth to the scan strategy node (wang2021analyticalpredictionof pages 4-6); (ii) replace sigmoid synthetic functions with semi-physical models incorporating regime transitions; (iii) replace simple threshold constraints with normalized-enthalpy-based keyholing criteria and geometric LOF/balling criteria (wang2021analyticalpredictionof pages 4-6, bergmueller2023systematicapproachto pages 8-10); (iv) implement composition simplex constraints; (v) integrate real CALPHAD outputs including CSC (WO2024092273A2 pages 46-48).

**High-priority improvements**: (i) Add apparent density or packing proxy to the energy delivery node (field2020theeffectof pages 1-2, ziri2022combinedeffectof pages 15-17); (ii) add melt-pool depth to the thermal management node; (iii) increase training data to ≥50 points for d=5 nodes (kudva2024efficientperformancebasedmpc pages 3-4); (iv) implement uncertainty propagation through the DAG.

**Medium-priority enhancements**: (i) Expand the characterization node to multi-output; (ii) develop cost uncertainty bands; (iii) add multi-fidelity integration; (iv) implement heteroscedastic noise models for real data deployment.

References

1. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

2. (astudillo2021bayesianoptimizationof pages 2-4): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

3. (buathong2506fastbayesianoptimization pages 2-4): Poompol Buathong and Peter I. Frazier. Fast bayesian optimization of function networks with partial evaluations. ArXiv, Jun 2506. URL: https://doi.org/10.48550/arxiv.2506.11456, doi:10.48550/arxiv.2506.11456. This article has 0 citations.

4. (buathong2506fastbayesianoptimization pages 8-9): Poompol Buathong and Peter I. Frazier. Fast bayesian optimization of function networks with partial evaluations. ArXiv, Jun 2506. URL: https://doi.org/10.48550/arxiv.2506.11456, doi:10.48550/arxiv.2506.11456. This article has 0 citations.

5. (kudva2024efficientperformancebasedmpc pages 3-4): Akshay Kudva, Melanie T. Huynh, Ali Mesbah, and Joel A. Paulson. Efficient performance-based mpc tuning in high dimensions using bayesian optimization over sparse subspaces. IFAC-PapersOnLine, 58:458-463, Jan 2024. URL: https://doi.org/10.1016/j.ifacol.2024.08.379, doi:10.1016/j.ifacol.2024.08.379. This article has 11 citations and is from a peer-reviewed journal.

6. (eriksson2021highdimensionalbayesianoptimization pages 7-9): David Eriksson and Martin Jankowiak. High-dimensional bayesian optimization with sparse axis-aligned subspaces. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2103.00349, doi:10.48550/arxiv.2103.00349. This article has 290 citations.

7. (field2020theeffectof pages 1-2): A. C. Field, L. N. Carter, N. J. E. Adkins, M. M. Attallah, M. J. Gorley, and M. Strangwood. The effect of powder characteristics on build quality of high-purity tungsten produced via laser powder bed fusion (lpbf). Metallurgical and Materials Transactions A, 51:1367-1378, Jan 2020. URL: https://doi.org/10.1007/s11661-019-05601-6, doi:10.1007/s11661-019-05601-6. This article has 63 citations.

8. (ziri2022combinedeffectof pages 1-2): Sabrine Ziri, Anis Hor, and Catherine Mabru. Combined effect of powder properties and process parameters on the density of 316l stainless steel obtained by laser powder bed fusion. The International Journal of Advanced Manufacturing Technology, 120:6187-6204, Apr 2022. URL: https://doi.org/10.1007/s00170-022-09160-w, doi:10.1007/s00170-022-09160-w. This article has 56 citations.

9. (ziri2022combinedeffectof pages 15-17): Sabrine Ziri, Anis Hor, and Catherine Mabru. Combined effect of powder properties and process parameters on the density of 316l stainless steel obtained by laser powder bed fusion. The International Journal of Advanced Manufacturing Technology, 120:6187-6204, Apr 2022. URL: https://doi.org/10.1007/s00170-022-09160-w, doi:10.1007/s00170-022-09160-w. This article has 56 citations.

10. (haferkamp2021effectofbimodal pages 7-9): Lukas Haferkamp, Simon Liechti, Adriaan Spierings, and Konrad Wegener. Effect of bimodal powder blends on part density and melt pool fluctuation in laser powder bed fusion. Progress in Additive Manufacturing, 6:407-416, Apr 2021. URL: https://doi.org/10.1007/s40964-021-00179-1, doi:10.1007/s40964-021-00179-1. This article has 23 citations and is from a peer-reviewed journal.

11. (haferkamp2021effectofbimodal pages 1-2): Lukas Haferkamp, Simon Liechti, Adriaan Spierings, and Konrad Wegener. Effect of bimodal powder blends on part density and melt pool fluctuation in laser powder bed fusion. Progress in Additive Manufacturing, 6:407-416, Apr 2021. URL: https://doi.org/10.1007/s40964-021-00179-1, doi:10.1007/s40964-021-00179-1. This article has 23 citations and is from a peer-reviewed journal.

12. (wang2021analyticalpredictionof pages 4-6): Wenjia Wang, Jinqiang Ning, and Steven Y. Liang. Analytical prediction of balling, lack-of-fusion and keyholing thresholds in powder bed fusion. Applied Sciences, 11:12053, Dec 2021. URL: https://doi.org/10.3390/app112412053, doi:10.3390/app112412053. This article has 36 citations.

13. (wang2021analyticalpredictionof pages 6-7): Wenjia Wang, Jinqiang Ning, and Steven Y. Liang. Analytical prediction of balling, lack-of-fusion and keyholing thresholds in powder bed fusion. Applied Sciences, 11:12053, Dec 2021. URL: https://doi.org/10.3390/app112412053, doi:10.3390/app112412053. This article has 36 citations.

14. (bergmueller2023systematicapproachto pages 6-8): Simon Bergmueller, Lukas Gerhold, Lorenz Fuchs, Lukas Kaserer, and Gerhard Leichtfried. Systematic approach to process parameter optimization for laser powder bed fusion of low-alloy steel based on melting modes. The International Journal of Advanced Manufacturing Technology, 126:4385-4398, Apr 2023. URL: https://doi.org/10.1007/s00170-023-11377-2, doi:10.1007/s00170-023-11377-2. This article has 45 citations.

15. (astudillo2021bayesianoptimizationof pages 6-8): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

16. (bergmueller2023systematicapproachto pages 8-10): Simon Bergmueller, Lukas Gerhold, Lorenz Fuchs, Lukas Kaserer, and Gerhard Leichtfried. Systematic approach to process parameter optimization for laser powder bed fusion of low-alloy steel based on melting modes. The International Journal of Advanced Manufacturing Technology, 126:4385-4398, Apr 2023. URL: https://doi.org/10.1007/s00170-023-11377-2, doi:10.1007/s00170-023-11377-2. This article has 45 citations.

17. (keeley2025adevelopmentof pages 14-16): William Keeley, Richard Turner, Bashir Mitchell, and Nils Warnken. A development of the rosenthal equation for predicting thermal profiles during additive manufacturing. Thermo, 5:16, May 2025. URL: https://doi.org/10.3390/thermo5020016, doi:10.3390/thermo5020016. This article has 3 citations.

18. (plotkowski2017verificationandvalidation pages 5-8): A. Plotkowski, M.M. Kirka, and S.S. Babu. Verification and validation of a rapid heat transfer calculation methodology for transient melt pool solidification conditions in powder bed metal additive manufacturing. Additive manufacturing, 18:256-268, Dec 2017. URL: https://doi.org/10.1016/j.addma.2017.10.017, doi:10.1016/j.addma.2017.10.017. This article has 189 citations and is from a highest quality peer-reviewed journal.

19. (keeley2025adevelopmentof pages 2-4): William Keeley, Richard Turner, Bashir Mitchell, and Nils Warnken. A development of the rosenthal equation for predicting thermal profiles during additive manufacturing. Thermo, 5:16, May 2025. URL: https://doi.org/10.3390/thermo5020016, doi:10.3390/thermo5020016. This article has 3 citations.

20. (keeley2025adevelopmentof pages 7-9): William Keeley, Richard Turner, Bashir Mitchell, and Nils Warnken. A development of the rosenthal equation for predicting thermal profiles during additive manufacturing. Thermo, 5:16, May 2025. URL: https://doi.org/10.3390/thermo5020016, doi:10.3390/thermo5020016. This article has 3 citations.

21. (keeley2025adevelopmentof pages 9-14): William Keeley, Richard Turner, Bashir Mitchell, and Nils Warnken. A development of the rosenthal equation for predicting thermal profiles during additive manufacturing. Thermo, 5:16, May 2025. URL: https://doi.org/10.3390/thermo5020016, doi:10.3390/thermo5020016. This article has 3 citations.

22. (yang2020theanalyticalprediction pages 8-11): Huadong Yang, Zhen Li, and Siqi Wang. The analytical prediction of thermal distribution and defect generation of inconel 718 by selective laser melting. Applied Sciences, 10:7300, Oct 2020. URL: https://doi.org/10.3390/app10207300, doi:10.3390/app10207300. This article has 30 citations.

23. (naderi2023onthefidelity pages 3-5): M. Naderi, J. Weaver, D. Deisenroth, N. Iyyer, and R. McCauley. On the fidelity of the scaling laws for melt pool depth analysis during laser powder bed fusion. Integrating Materials and Manufacturing Innovation, 12:11-26, Dec 2023. URL: https://doi.org/10.1007/s40192-022-00289-w, doi:10.1007/s40192-022-00289-w. This article has 35 citations and is from a peer-reviewed journal.

24. (naderi2023onthefidelity pages 2-3): M. Naderi, J. Weaver, D. Deisenroth, N. Iyyer, and R. McCauley. On the fidelity of the scaling laws for melt pool depth analysis during laser powder bed fusion. Integrating Materials and Manufacturing Innovation, 12:11-26, Dec 2023. URL: https://doi.org/10.1007/s40192-022-00289-w, doi:10.1007/s40192-022-00289-w. This article has 35 citations and is from a peer-reviewed journal.

25. (simonds2021thecausalrelationship pages 6-7): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Paul A. Williams, Niranjan Parab, Cang Zhao, and Tao Sun. The causal relationship between melt pool geometry and energy absorption measured in real time during laser-based manufacturing. Applied Materials Today, 23:101049, Jun 2021. URL: https://doi.org/10.1016/j.apmt.2021.101049, doi:10.1016/j.apmt.2021.101049. This article has 128 citations and is from a peer-reviewed journal.

26. (hanemann2020dimensionlessenthalpyas pages 1-2): T. Hanemann, C. Seyfert, P. Holfelder, A. Rota, and M. Heilmaier. Dimensionless enthalpy as characteristic factor for process control in laser powder bed fusion. Journal of Laser Micro Nanoengineering, 15:257, Dec 2020. URL: https://doi.org/10.2961/jlmn.2020.03.2017, doi:10.2961/jlmn.2020.03.2017. This article has 19 citations and is from a peer-reviewed journal.

27. (wang2021analyticalpredictionof pages 7-10): Wenjia Wang, Jinqiang Ning, and Steven Y. Liang. Analytical prediction of balling, lack-of-fusion and keyholing thresholds in powder bed fusion. Applied Sciences, 11:12053, Dec 2021. URL: https://doi.org/10.3390/app112412053, doi:10.3390/app112412053. This article has 36 citations.

28. (kudva2024efficientperformancebasedmpc pages 2-3): Akshay Kudva, Melanie T. Huynh, Ali Mesbah, and Joel A. Paulson. Efficient performance-based mpc tuning in high dimensions using bayesian optimization over sparse subspaces. IFAC-PapersOnLine, 58:458-463, Jan 2024. URL: https://doi.org/10.1016/j.ifacol.2024.08.379, doi:10.1016/j.ifacol.2024.08.379. This article has 11 citations and is from a peer-reviewed journal.

29. (wang2025calphadguidedinterlayerdesign pages 8-10): Liyi Wang, Luis Fernando Ladinos Pizano, Michael A. Klecka, Kelsay Neely, and Wei Xiong. Calphad-guided interlayer design for crack-free additive manufacturing of copper c18150 – inconel 625 bimetallic structures. Science and Technology of Advanced Materials, Nov 2025. URL: https://doi.org/10.1080/14686996.2025.2587393, doi:10.1080/14686996.2025.2587393. This article has 1 citations and is from a peer-reviewed journal.

30. (WO2024092273A2 pages 46-48): Seyedeh Mohadeseh TAHERI-MOUSAVI. Methodologies for formulating compositions, including aluminum alloys with high …. Patent (WO,US), 2024.

31. (wang2025calphadguidedinterlayerdesign pages 4-5): Liyi Wang, Luis Fernando Ladinos Pizano, Michael A. Klecka, Kelsay Neely, and Wei Xiong. Calphad-guided interlayer design for crack-free additive manufacturing of copper c18150 – inconel 625 bimetallic structures. Science and Technology of Advanced Materials, Nov 2025. URL: https://doi.org/10.1080/14686996.2025.2587393, doi:10.1080/14686996.2025.2587393. This article has 1 citations and is from a peer-reviewed journal.

32. (keller2017applicationoffinite pages 20-23): Trevor Keller, Greta Lindwall, Supriyo Ghosh, Li Ma, Brandon M. Lane, Fan Zhang, Ursula R. Kattner, Eric A. Lass, Jarred C. Heigel, Yaakov Idell, Maureen E. Williams, Andrew J. Allen, Jonathan E. Guyer, and Lyle E. Levine. Application of finite element, phase-field, and calphad-based methods to additive manufacturing of ni-based superalloys. Acta materialia, 139:244-253, May 2017. URL: https://doi.org/10.48550/arxiv.1705.02016, doi:10.48550/arxiv.1705.02016. This article has 504 citations and is from a highest quality peer-reviewed journal.

33. (keller2017applicationoffinite pages 3-5): Trevor Keller, Greta Lindwall, Supriyo Ghosh, Li Ma, Brandon M. Lane, Fan Zhang, Ursula R. Kattner, Eric A. Lass, Jarred C. Heigel, Yaakov Idell, Maureen E. Williams, Andrew J. Allen, Jonathan E. Guyer, and Lyle E. Levine. Application of finite element, phase-field, and calphad-based methods to additive manufacturing of ni-based superalloys. Acta materialia, 139:244-253, May 2017. URL: https://doi.org/10.48550/arxiv.1705.02016, doi:10.48550/arxiv.1705.02016. This article has 504 citations and is from a highest quality peer-reviewed journal.

34. (wang2020uncertaintyquantificationand pages 1-4): Xin Wang and Wei Xiong. Uncertainty quantification and composition optimization for alloy additive manufacturing through a calphad-based icme framework. npj Computational Materials, Dec 2020. URL: https://doi.org/10.1038/s41524-020-00454-9, doi:10.1038/s41524-020-00454-9. This article has 74 citations and is from a peer-reviewed journal.

35. (yang2020theanalyticalprediction pages 11-14): Huadong Yang, Zhen Li, and Siqi Wang. The analytical prediction of thermal distribution and defect generation of inconel 718 by selective laser melting. Applied Sciences, 10:7300, Oct 2020. URL: https://doi.org/10.3390/app10207300, doi:10.3390/app10207300. This article has 30 citations.

36. (spurek2022influenceofthe pages 4-6): Marvin A. Spurek, Lukas Haferkamp, Christian Weiss, Adriaan B. Spierings, Johannes H. Schleifenbaum, and Konrad Wegener. Influence of the particle size distribution of monomodal 316l powder on its flowability and processability in powder bed fusion. Progress in Additive Manufacturing, 7:533-542, Dec 2022. URL: https://doi.org/10.1007/s40964-021-00240-z, doi:10.1007/s40964-021-00240-z. This article has 54 citations and is from a peer-reviewed journal.

37. (spurek2022influenceofthe pages 10-10): Marvin A. Spurek, Lukas Haferkamp, Christian Weiss, Adriaan B. Spierings, Johannes H. Schleifenbaum, and Konrad Wegener. Influence of the particle size distribution of monomodal 316l powder on its flowability and processability in powder bed fusion. Progress in Additive Manufacturing, 7:533-542, Dec 2022. URL: https://doi.org/10.1007/s40964-021-00240-z, doi:10.1007/s40964-021-00240-z. This article has 54 citations and is from a peer-reviewed journal.

38. (xue2023effectofparticle pages 1-2): Muhan Xue, Xinyue Chen, Xia Ji, Xinliang Xie, Qi Chao, and Guohua Fan. Effect of particle size distribution on the printing quality and tensile properties of ti-6al-4v alloy produced by lpbf process. Metals, 13:604, Mar 2023. URL: https://doi.org/10.3390/met13030604, doi:10.3390/met13030604. This article has 34 citations.