#!/usr/bin/env python3
"""
BOFN Expanded DAG — Realistic LPBF Parameter Dimensionality (v2)

Implements the refined BOFN architecture based on Edison Scientific reviews:
  - Tasks d0ad1eea, 6025bdcf: initial LPBF dimensionality + implementation
  - Task 98edd2c3: critical review with physics-informed recommendations

v2 changes (from Edison review 98edd2c3):
  - Node 2a: swap flowability for apparent_density (packing/absorptivity proxy)
  - Node 2b: add melt_pool_depth alongside width (LOF/remelting physics, CRITICAL)
  - Node 2c: add melt_pool_depth (thermal gradient/intensity proxy, HIGH)
  - Node 3: multi-output (yield_strength + elongation)
  - Constraints: physics-informed (normalized enthalpy keyholing, πw/l balling,
    H²/W²+L²/D²≤1 LOF) replacing simple threshold logic
  - Training data: n=50 for d=5 nodes (was 30, per Q6 recommendation)
  - CALPHAD: add CSC (cracking susceptibility coefficient) output

DAG topology (v2):
  Node 0:  CALPHAD screening (composition d=3 → phase_frac + solidif_range + CSC d=3)
  Node 1a: Powder PSD (phase_frac + solidif_range + atom_params d=5 → D50 d=1)
  Node 1b: Powder flowability (phase_frac + atom_params d=3 → Hausner_ratio d=1)
  Node 1c: Powder density (phase_frac + atom_params d=3 → apparent_density d=1)
  Node 2a: Energy delivery (D50 + apparent_density + power + speed + spot_size d=5 → melt_pool d=2)
  Node 2b: Scan strategy (mp_width + mp_depth + hatch + rotation + contour d=5 → layer_quality d=1)
  Node 2c: Thermal mgmt (layer_quality + mp_depth + preheat + dwell d=4 → residual_stress d=1)
  Node 2d: Integration (mp_depth + layer_quality + stress d=3 → part_density d=1)
  Node 3:  Characterization (part_density d=1 → yield_strength + elongation d=2)

Global decision vector x = [composition(3), atomization_params(2), power, speed,
                            spot_size, hatch, rotation, contour, preheat, dwell]
Total d=14, of which composition=3, atomization=2, LPBF Tier-A=8, plus 1 passthrough.

References:
  - Astudillo & Frazier (2021), "Bayesian Optimization of Function Networks", NeurIPS
  - Buathong & Frazier (2025), "Fast Bayesian Optimization of Function Networks"
  - Eriksson & Jankowiak (2021), "SAASBO", UAI (290 citations)
  - Wang et al. (2021), "Analytical Prediction of Balling, LOF, Keyholing", Appl Sci
  - Bergmueller et al. (2023), "Systematic Approach to Process Parameter Optimization"
  - Edison tasks d0ad1eea, 6025bdcf, 98edd2c3

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
    composition (n, 3) → [phase_fraction, solidification_range, CSC] (n, 3).

    CSC = cracking susceptibility coefficient (Clyne-Davies style).
    Low CSC = low cracking risk = good printability.
    Edison review 98edd2c3 Q8: CALPHAD should output printability-relevant
    thermodynamic descriptors including CSC.
    """
    center = torch.tensor([0.7, 0.2, 0.1], dtype=DTYPE, device=DEVICE)
    dist_sq = ((composition - center) ** 2).sum(dim=-1, keepdim=True)
    phase_frac = torch.exp(-8.0 * dist_sq)
    # Solidification range: narrower near optimal composition
    solid_range = 0.3 + 0.7 * (1.0 - phase_frac)
    # CSC: cracking susceptibility (lower = better, correlates with narrow freezing range)
    csc = 0.2 + 0.6 * solid_range + 0.1 * torch.sin(5.0 * composition[..., 1:2])
    return torch.cat([phase_frac, solid_range, csc], dim=-1)


def powder_psd_fn(phase_frac, solid_range, atom_params):
    """Node 1a: Powder PSD D50.
    phase_frac (n,1) + solid_range (n,1) + atomization_params (n,2) → D50 (n,1).
    D50 in normalized [0,1] range (0=fine, 1=coarse).

    Edison review: include solidification range because alloy thermodynamics
    influence atomization response and particle-size behavior.
    """
    x = torch.cat([phase_frac, solid_range, atom_params], dim=-1)
    return torch.sigmoid(0.5 * x[..., 0:1] + 0.3 * x[..., 1:2]
                         + 0.8 * x[..., 2:3] - 0.3 * x[..., 3:4])


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


def energy_delivery_fn(d50, apparent_density, power, speed, spot_size):
    """Node 2a: Energy delivery → melt pool geometry.
    d50 (n,1) + apparent_density (n,1) + power (n,1) + speed (n,1) + spot_size (n,1)
    → [melt_pool_width, melt_pool_depth] (n,2).

    Edison review Q1: swap flowability for apparent_density as packing/absorptivity
    proxy. Powder-bed state changes effective absorptivity and layer thickness.
    """
    # Melt pool width: primarily power/speed/spot dependent
    width = torch.sigmoid(2.0 * power - 1.5 * speed + 0.8 * spot_size
                          - 0.3 * d50 + 0.2 * apparent_density)
    # Melt pool depth: power/speed dominant, packing density affects coupling
    depth = torch.sigmoid(2.5 * power - 2.0 * speed + 0.3 * spot_size
                          - 0.1 * d50 + 0.15 * apparent_density)
    return torch.cat([width, depth], dim=-1)


def scan_strategy_fn(melt_pool_width, melt_pool_depth, hatch, rotation, contour):
    """Node 2b: Scan strategy → layer quality.
    melt_pool_width (n,1) + melt_pool_depth (n,1) + hatch (n,1) + rotation (n,1)
    + contour (n,1) → layer_quality (n,1).

    Edison review Q2 (CRITICAL): LOF criteria depend on both width AND depth.
    Wang et al. (2021): H²/W² + L²/D² ≤ 1 for lack-of-fusion avoidance.
    Bergmueller et al. (2023): aspect ratio δ=depth/width governs process regime.
    """
    # Layer quality depends on overlap (width vs hatch) and remelting (depth-dependent)
    overlap = melt_pool_width / hatch.clamp(min=0.01)
    penetration = melt_pool_depth  # proxy for remelting capability
    quality = torch.sigmoid(overlap - 0.5 + 0.4 * penetration
                            + 0.3 * rotation + 0.2 * contour)
    return quality


def thermal_mgmt_fn(layer_quality, melt_pool_depth, preheat, dwell):
    """Node 2c: Thermal management → residual stress.
    layer_quality (n,1) + melt_pool_depth (n,1) + preheat (n,1) + dwell (n,1)
    → residual_stress (n,1). Lower stress is better (normalized [0,1]).

    Edison review Q3 (HIGH): Add melt-pool depth as proxy for thermal intensity.
    Residual stress depends on thermal gradients governed by melt-pool geometry.
    """
    # Residual stress reduced by preheat and dwell time, increased by deep melt pools
    stress = torch.sigmoid(1.0 - 0.5 * preheat - 0.3 * dwell
                           - 0.4 * layer_quality + 0.3 * melt_pool_depth + 0.2)
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
    part_density (n,1) → [yield_strength, elongation] (n,2).

    Edison review #2 (CRITICAL): both YS and elongation increase monotonically
    with part density in LPBF. Defects reduce BOTH properties, with elongation
    more sensitive. Wang et al. (2018, Nature Materials, 2705 citations):
    AM 316L achieves strength+ductility beyond conventional tradeoff.
    """
    # Both increase with density, elongation steeper (more defect-sensitive)
    ys = 0.3 + 0.5 * torch.sigmoid(6.0 * (part_density - 0.5))
    el = 0.1 + 0.7 * torch.sigmoid(8.0 * (part_density - 0.6))  # steeper, later onset
    return torch.cat([ys, el], dim=-1)


# ---------------------------------------------------------------------------
# Constraint functions for LPBF physical limits
# ---------------------------------------------------------------------------

def keyhole_constraint(melt_pool_geom):
    """Keyholing constraint: aspect ratio depth/width.

    Edison review Q5 (CRITICAL): Use aspect ratio as proxy for normalized enthalpy.
    Bergmueller et al. (2023): δ=0.8 is conduction-to-keyhole transition threshold.
    Returns: negative = feasible, positive = infeasible.
    """
    width = melt_pool_geom[..., 0:1].clamp(min=0.01)
    depth = melt_pool_geom[..., 1:2]
    aspect_ratio = depth / width
    # Keyhole onset at aspect ratio ~0.8 (Bergmueller threshold)
    return aspect_ratio - 0.8


def balling_constraint(melt_pool_geom):
    """Balling constraint: track stability via πw/l criterion.

    Edison review Q5 (CRITICAL): Balling when πw/l < 1, i.e. when track is
    unstable. We approximate length ≈ 2*width (typical conduction mode).
    Wang et al. (2021): πw/l > 1 for stable tracks.
    Returns: negative = feasible, positive = infeasible.
    """
    width = melt_pool_geom[..., 0:1]
    # Approximate melt pool length ≈ 2 * width (conduction mode estimate)
    length = 2.0 * width + 0.3
    stability = 3.14159 * width / length.clamp(min=0.01)
    return 1.0 - stability  # feasible when stability > 1 (i.e., πw/l > 1)


def lof_constraint(melt_pool_geom, hatch, layer_thickness=0.3):
    """Lack-of-fusion constraint: geometric overlap criterion.

    Edison review Q5 (CRITICAL): H²/W² + L²/D² ≤ 1 for LOF avoidance.
    Wang et al. (2021): analytical LOF threshold.
    Returns: negative = feasible, positive = infeasible.
    """
    width = melt_pool_geom[..., 0:1].clamp(min=0.01)
    depth = melt_pool_geom[..., 1:2].clamp(min=0.01)
    lt = torch.full_like(hatch, layer_thickness)
    lof_criterion = (hatch / width) ** 2 + (lt / depth) ** 2
    return lof_criterion - 1.0  # feasible when < 0


# ---------------------------------------------------------------------------
# Generate training data for the expanded DAG
# ---------------------------------------------------------------------------

def generate_expanded_data(n_train=50):
    """Generate training data for all nodes in the expanded DAG.

    Global decision vector:
      x = [comp(3), atom_params(2), power, speed, spot_size, hatch,
           rotation, contour, preheat, dwell] = 14 dimensions

    Edison review Q6: use n=50 for d=5 nodes (was 30).
    """
    # Sample global decision vector
    comp = torch.rand(n_train, 3, dtype=DTYPE, device=DEVICE)
    comp = comp / comp.sum(dim=1, keepdim=True)  # Simplex normalization
    atom_params = torch.rand(n_train, 2, dtype=DTYPE, device=DEVICE)
    power = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    speed = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    spot_size = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    hatch = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    rotation = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    contour = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    preheat = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)
    dwell = torch.rand(n_train, 1, dtype=DTYPE, device=DEVICE)

    # Node 0: CALPHAD (now outputs 3: phase_frac, solid_range, CSC)
    calphad_out = calphad_fn(comp)  # (n, 3)
    phase_frac = calphad_out[..., 0:1]
    solid_range = calphad_out[..., 1:2]

    # Node 1a: Powder PSD (now includes solidification range)
    psd = powder_psd_fn(phase_frac, solid_range, atom_params)
    # Node 1b-c: Powder flowability and density (unchanged inputs)
    flow = powder_flow_fn(phase_frac, atom_params)
    dens = powder_density_fn(phase_frac, atom_params)

    # Node 2a: Energy delivery (D50 + apparent_density replacing flowability)
    melt_pool = energy_delivery_fn(psd, dens, power, speed, spot_size)
    mp_width = melt_pool[..., 0:1]
    mp_depth = melt_pool[..., 1:2]

    # Node 2b: Scan strategy (now includes mp_depth)
    layer_q = scan_strategy_fn(mp_width, mp_depth, hatch, rotation, contour)

    # Node 2c: Thermal management (now includes mp_depth)
    stress = thermal_mgmt_fn(layer_q, mp_depth, preheat, dwell)

    # Node 2d: Integration (unchanged)
    part_dens = integration_fn(mp_depth, layer_q, stress)

    # Node 3: Characterization (now multi-output: YS + elongation)
    mech_out = characterization_fn(part_dens)

    # Pack node training data: (inputs, outputs) for each node
    node_data = {
        "calphad": (comp, calphad_out),
        "powder_psd": (torch.cat([phase_frac, solid_range, atom_params], dim=-1), psd),
        "powder_flow": (torch.cat([phase_frac, atom_params], dim=-1), flow),
        "powder_dens": (torch.cat([phase_frac, atom_params], dim=-1), dens),
        "energy": (torch.cat([psd, dens, power, speed, spot_size], dim=-1), melt_pool),
        "scan": (torch.cat([mp_width, mp_depth, hatch, rotation, contour], dim=-1), layer_q),
        "thermal": (torch.cat([layer_q, mp_depth, preheat, dwell], dim=-1), stress),
        "density": (torch.cat([mp_depth, layer_q, stress], dim=-1), part_dens),
        "mech": (part_dens, mech_out),
    }

    return node_data


# ---------------------------------------------------------------------------
# Build per-node GP models
# ---------------------------------------------------------------------------

def build_expanded_gps(node_data):
    """Fit a SingleTaskGP with Normalize/Standardize for each node.

    For multi-output nodes (calphad: d=2, energy: d=2), we fit independent
    GPs for each output dimension (Strategy 1 from Edison review).
    """
    models = {}
    for name, (X, Y) in node_data.items():
        if Y.shape[-1] > 1:
            # Multi-output: fit independent GPs per output
            node_models = []
            for j in range(Y.shape[-1]):
                model = SingleTaskGP(
                    train_X=X,
                    train_Y=Y[..., j:j+1],
                    input_transform=Normalize(d=X.shape[-1]),
                    outcome_transform=Standardize(m=1),
                )
                mll = ExactMarginalLogLikelihood(model.likelihood, model)
                fit_gpytorch_mll(mll)
                node_models.append(model)
            models[name] = node_models
            print(f"  {name}: {len(node_models)} GPs, input d={X.shape[-1]}")
        else:
            model = SingleTaskGP(
                train_X=X,
                train_Y=Y,
                input_transform=Normalize(d=X.shape[-1]),
                outcome_transform=Standardize(m=1),
            )
            mll = ExactMarginalLogLikelihood(model.likelihood, model)
            fit_gpytorch_mll(mll)
            models[name] = model
            print(f"  {name}: 1 GP, input d={X.shape[-1]}")
    return models


# ---------------------------------------------------------------------------
# Composite forward pass through the expanded DAG
# ---------------------------------------------------------------------------

def predict_node(models, name, X):
    """Get posterior mean from a node (handles multi-output nodes)."""
    model = models[name]
    if isinstance(model, list):
        # Multi-output: concatenate predictions from independent GPs
        preds = [m.posterior(X).mean for m in model]
        return torch.cat(preds, dim=-1)
    return model.posterior(X).mean


def composite_forward_expanded(models, comp, atom_params, power, speed,
                                spot_size, hatch, rotation, contour,
                                preheat, dwell):
    """Propagate through the expanded 9-node DAG using GP posterior means.

    v2 changes: CALPHAD→3 outputs, PSD uses solid_range, energy uses
    apparent_density, scan+thermal use mp_depth, characterization→2 outputs.

    Args:
        models: dict of fitted GP models (keyed by node name)
        comp: (n, 3) alloy composition (simplex-normalized)
        atom_params: (n, 2) atomization parameters
        power, speed, spot_size: (n, 1) each — LPBF energy params
        hatch, rotation, contour: (n, 1) each — LPBF scan strategy
        preheat, dwell: (n, 1) each — LPBF thermal management

    Returns:
        dict with predictions at every node
    """
    # Node 0: CALPHAD (now 3 outputs)
    calphad_pred = predict_node(models, "calphad", comp)  # (n, 3)
    phase_frac = calphad_pred[..., 0:1]
    solid_range = calphad_pred[..., 1:2]
    csc = calphad_pred[..., 2:3]

    # Node 1a: Powder PSD (now includes solid_range)
    psd_input = torch.cat([phase_frac, solid_range, atom_params], dim=-1)
    psd = predict_node(models, "powder_psd", psd_input)

    # Node 1b-c: Powder flowability and density
    powder_input = torch.cat([phase_frac, atom_params], dim=-1)
    flow = predict_node(models, "powder_flow", powder_input)
    dens = predict_node(models, "powder_dens", powder_input)

    # Node 2a: Energy delivery (D50 + apparent_density + LPBF params)
    energy_input = torch.cat([psd, dens, power, speed, spot_size], dim=-1)
    melt_pool = predict_node(models, "energy", energy_input)  # (n, 2)
    mp_width = melt_pool[..., 0:1]
    mp_depth = melt_pool[..., 1:2]

    # Node 2b: Scan strategy (now includes mp_depth)
    scan_input = torch.cat([mp_width, mp_depth, hatch, rotation, contour], dim=-1)
    layer_q = predict_node(models, "scan", scan_input)

    # Node 2c: Thermal management (now includes mp_depth)
    thermal_input = torch.cat([layer_q, mp_depth, preheat, dwell], dim=-1)
    stress = predict_node(models, "thermal", thermal_input)

    # Node 2d: Integration
    density_input = torch.cat([mp_depth, layer_q, stress], dim=-1)
    part_dens = predict_node(models, "density", density_input)

    # Node 3: Characterization (now 2 outputs: YS + elongation)
    mech_out = predict_node(models, "mech", part_dens)
    yield_strength = mech_out[..., 0:1]
    elongation = mech_out[..., 1:2]

    return {
        "calphad": calphad_pred,
        "phase_fraction": phase_frac,
        "solid_range": solid_range,
        "csc": csc,
        "psd": psd, "flowability": flow, "apparent_density": dens,
        "melt_pool": melt_pool,
        "layer_quality": layer_q,
        "residual_stress": stress,
        "part_density": part_dens,
        "yield_strength": yield_strength,
        "elongation": elongation,
    }


# ---------------------------------------------------------------------------
# Cost-aware staged screening
# ---------------------------------------------------------------------------

def staged_screening(models, comp, atom_params, power, speed, spot_size,
                     hatch, rotation, contour, preheat, dwell,
                     calphad_threshold=0.3, density_threshold=0.5):
    """Demonstrate multi-stage cost-aware screening through the expanded DAG.

    Stage 1: CALPHAD screening (cheap) — filter by phase stability + CSC
    Stage 2: Powder production + LPBF (moderate) — filter by part density
    Stage 3: Full mechanical characterization (expensive) — only top candidates
    """
    n = comp.shape[0]
    results = {"n_total": n, "stages": []}

    # --- Stage 1: CALPHAD screening ---
    calphad_pred = predict_node(models, "calphad", comp)
    phase_frac = calphad_pred[..., 0:1]
    solid_range = calphad_pred[..., 1:2]
    stage1_cost = n * NODE_COSTS["calphad"]

    mask1 = phase_frac.squeeze(-1) > calphad_threshold
    n_pass1 = int(mask1.sum().item())
    results["stages"].append({
        "name": "CALPHAD screening",
        "n_in": n, "n_out": n_pass1,
        "cost": stage1_cost,
    })

    if n_pass1 == 0:
        results["total_cost"] = stage1_cost
        results["naive_cost"] = n * FULL_PIPELINE_COST
        return results

    # --- Stage 2: Powder + LPBF for promoted candidates ---
    idx1 = mask1.nonzero(as_tuple=True)[0]
    pf = phase_frac[idx1]
    sr = solid_range[idx1]
    ap = atom_params[idx1]
    pw = power[idx1]
    sp = speed[idx1]
    ss = spot_size[idx1]
    ht = hatch[idx1]
    rt = rotation[idx1]
    ct = contour[idx1]
    ph = preheat[idx1]
    dw = dwell[idx1]

    # Powder PSD (now includes solid_range)
    psd_input = torch.cat([pf, sr, ap], dim=-1)
    psd = predict_node(models, "powder_psd", psd_input)
    # Powder density
    dens_input = torch.cat([pf, ap], dim=-1)
    dens = predict_node(models, "powder_dens", dens_input)

    # LPBF sub-nodes (updated signatures)
    energy_input = torch.cat([psd, dens, pw, sp, ss], dim=-1)
    melt_pool = predict_node(models, "energy", energy_input)
    mp_width = melt_pool[..., 0:1]
    mp_depth = melt_pool[..., 1:2]

    scan_input = torch.cat([mp_width, mp_depth, ht, rt, ct], dim=-1)
    layer_q = predict_node(models, "scan", scan_input)

    thermal_input = torch.cat([layer_q, mp_depth, ph, dw], dim=-1)
    stress = predict_node(models, "thermal", thermal_input)

    density_input = torch.cat([mp_depth, layer_q, stress], dim=-1)
    part_dens = predict_node(models, "density", density_input)

    stage2_per_candidate = (ATOMIZATION_COST
                            + NODE_COSTS["powder_psd"]
                            + NODE_COSTS["powder_dens"]
                            + NODE_COSTS["energy"]
                            + NODE_COSTS["scan"]
                            + NODE_COSTS["thermal"]
                            + NODE_COSTS["density"])
    stage2_cost = n_pass1 * stage2_per_candidate

    mask2 = part_dens.squeeze(-1) > density_threshold
    n_pass2 = int(mask2.sum().item())
    results["stages"].append({
        "name": "Powder + LPBF",
        "n_in": n_pass1, "n_out": n_pass2,
        "cost": stage2_cost,
    })

    if n_pass2 == 0:
        results["total_cost"] = stage1_cost + stage2_cost
        results["naive_cost"] = n * FULL_PIPELINE_COST
        return results

    # --- Stage 3: Mechanical characterization for top candidates ---
    stage3_cost = n_pass2 * NODE_COSTS["mech"]
    results["stages"].append({
        "name": "Mechanical characterization",
        "n_in": n_pass2, "n_out": n_pass2,
        "cost": stage3_cost,
    })

    total_cost = stage1_cost + stage2_cost + stage3_cost
    naive_cost = n * FULL_PIPELINE_COST
    results["total_cost"] = total_cost
    results["naive_cost"] = naive_cost
    results["savings"] = naive_cost - total_cost
    results["savings_pct"] = 100.0 * (naive_cost - total_cost) / naive_cost

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("BOFN Expanded DAG v2 — Edison-Reviewed LPBF Dimensionality")
    print("=" * 70)
    print(f"\nGlobal decision vector: d=14")
    print(f"  composition: 3, atomization: 2, LPBF Tier-A: 8, characterization: 1")
    print(f"Pipeline: 9 nodes (CALPHAD → 3×powder → 4×LPBF → characterization)")
    print(f"Full pipeline cost: ${FULL_PIPELINE_COST:,.0f}/candidate\n")
    print("v2 changes from Edison review 98edd2c3:")
    print("  - CALPHAD: +CSC output (d=3→3)")
    print("  - PSD: +solidification_range input (d=4→1)")
    print("  - Energy: apparent_density replaces flowability")
    print("  - Scan: +melt_pool_depth (d=4→5, CRITICAL)")
    print("  - Thermal: +melt_pool_depth (d=3→4)")
    print("  - Characterization: +elongation (d=1→2)")
    print("  - Constraints: physics-informed (normalized enthalpy, πw/l, LOF)")
    print("  - Training: n=50 (was 30)")

    # 1. Generate training data
    print("\n[1/4] Generating training data (n=50)...")
    node_data = generate_expanded_data(n_train=50)
    print(f"  Generated data for {len(node_data)} nodes")

    # 2. Fit per-node GPs
    print("\n[2/4] Fitting per-node SingleTaskGP models...")
    models = build_expanded_gps(node_data)

    # 3. Composite forward pass
    print("\n[3/4] Running composite forward pass on 5 test candidates...")
    n_test = 5
    test_comp = torch.rand(n_test, 3, dtype=DTYPE, device=DEVICE)
    test_comp = test_comp / test_comp.sum(dim=1, keepdim=True)
    test_atom = torch.rand(n_test, 2, dtype=DTYPE, device=DEVICE)
    test_power = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_speed = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_spot = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_hatch = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_rot = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_contour = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_preheat = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    test_dwell = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)

    preds = composite_forward_expanded(
        models, test_comp, test_atom, test_power, test_speed, test_spot,
        test_hatch, test_rot, test_contour, test_preheat, test_dwell,
    )
    print(f"  Predicted yield strengths: {preds['yield_strength'].detach().squeeze(-1)}")
    print(f"  Predicted elongations:     {preds['elongation'].detach().squeeze(-1)}")

    # Ground truth
    gt_calphad = calphad_fn(test_comp)
    gt_pf = gt_calphad[..., 0:1]
    gt_sr = gt_calphad[..., 1:2]
    gt_psd = powder_psd_fn(gt_pf, gt_sr, test_atom)
    gt_dens = powder_density_fn(gt_pf, test_atom)
    gt_mp = energy_delivery_fn(gt_psd, gt_dens, test_power, test_speed, test_spot)
    gt_lq = scan_strategy_fn(gt_mp[..., 0:1], gt_mp[..., 1:2],
                             test_hatch, test_rot, test_contour)
    gt_stress = thermal_mgmt_fn(gt_lq, gt_mp[..., 1:2], test_preheat, test_dwell)
    gt_part_dens = integration_fn(gt_mp[..., 1:2], gt_lq, gt_stress)
    gt_mech = characterization_fn(gt_part_dens)
    print(f"  Ground truth YS:           {gt_mech[..., 0].squeeze(-1)}")
    print(f"  Ground truth elongation:   {gt_mech[..., 1].squeeze(-1)}")

    # Per-node prediction quality
    print("\n  Per-node prediction quality:")
    for name in ["phase_fraction", "csc", "psd", "apparent_density",
                 "part_density", "yield_strength", "elongation"]:
        if name in preds:
            p = preds[name].detach().squeeze()
            print(f"    {name}: predicted mean = {p.mean():.4f}")

    # 4. Multi-stage cost-aware screening
    print("\n[4/4] Multi-stage cost-aware screening (n=50 candidates)...")
    n_screen = 50
    sc = torch.rand(n_screen, 3, dtype=DTYPE, device=DEVICE)
    sc = sc / sc.sum(dim=1, keepdim=True)
    sa = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)
    sp = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    ss = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    sspot = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    sh = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    sr = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    sct = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    sph = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)
    sdw = torch.rand(n_screen, 1, dtype=DTYPE, device=DEVICE)

    result = staged_screening(
        models, sc, sa, sp, ss, sspot, sh, sr, sct, sph, sdw,
        calphad_threshold=0.3,
        density_threshold=0.5,
    )

    print(f"\n  Screening funnel:")
    for stage in result["stages"]:
        print(f"    {stage['name']}: {stage['n_in']} → {stage['n_out']} "
              f"(${stage['cost']:,.0f})")

    print(f"\n  Total cost (staged): ${result['total_cost']:,.0f}")
    print(f"  Naive cost (all full pipeline): ${result['naive_cost']:,.0f}")
    if "savings" in result:
        print(f"  Savings: ${result['savings']:,.0f} ({result['savings_pct']:.0f}%)")

    # Summary of DAG structure
    print("\n" + "=" * 70)
    print("DAG Summary (v2 — Edison-reviewed):")
    print("  Node 0 (CALPHAD):     d_in=3  → d_out=3  | $1")
    print("  Node 1a (PSD):        d_in=4  → d_out=1  | $50")
    print("  Node 1b (Flowability): d_in=3 → d_out=1  | $30")
    print("  Node 1c (Density):    d_in=3  → d_out=1  | $20")
    print("  Node 2a (Energy):     d_in=5  → d_out=2  | $100")
    print("  Node 2b (Scan):       d_in=5  → d_out=1  | $100  [+depth, CRITICAL]")
    print("  Node 2c (Thermal):    d_in=4  → d_out=1  | $50   [+depth, HIGH]")
    print("  Node 2d (Integration): d_in=3 → d_out=1  | $200")
    print("  Node 3 (Mech):        d_in=1  → d_out=2  | $300  [+elongation]")
    print(f"\n  Max per-node input dimensionality: 5 (Nodes 2a, 2b)")
    print(f"  Global decision vector: d=14")
    print(f"  SAASBO compatibility: all sub-nodes have d≤5 ✓")
    print("=" * 70)


if __name__ == "__main__":
    main()
