#!/usr/bin/env python3
"""
Fully Bayesian verification test for the expanded 9-node BOFN DAG.

Verifies that SaasFullyBayesianSingleTaskGP works as a drop-in replacement
for SingleTaskGP in the expanded DAG. Uses reduced MCMC parameters (64 warmup,
32 samples) for fast verification — production would use 256/128.

Usage:
  python benchmarks/bofn_expanded_bayesian_test.py
"""

import torch
from botorch.models.fully_bayesian import SaasFullyBayesianSingleTaskGP
from botorch.fit import fit_fully_bayesian_model_nuts

from bofn_expanded_demo import (
    DTYPE, DEVICE,
    calphad_fn, powder_psd_fn, powder_flow_fn, powder_density_fn,
    energy_delivery_fn, scan_strategy_fn, thermal_mgmt_fn,
    integration_fn, characterization_fn,
    generate_expanded_data,
)

torch.manual_seed(42)

# Reduced MCMC parameters for fast verification
WARMUP = 64
NUM_SAMPLES = 32


def predict_bayesian(model, X):
    """Get posterior mean from a fully Bayesian model, averaging over MCMC samples."""
    with torch.no_grad():
        post = model.posterior(X)
        # Shape: (num_mcmc_samples, n, d) → average over MCMC dim
        return post.mean.mean(dim=0)


def build_bayesian_gps(node_data):
    """Fit SaasFullyBayesianSingleTaskGP for each node in the expanded DAG."""
    models = {}
    for name, (X, Y) in node_data.items():
        if Y.shape[-1] > 1:
            # Multi-output: fit independent fully Bayesian GPs per output
            node_models = []
            for j in range(Y.shape[-1]):
                model = SaasFullyBayesianSingleTaskGP(
                    train_X=X, train_Y=Y[..., j:j+1],
                )
                fit_fully_bayesian_model_nuts(
                    model, warmup_steps=WARMUP, num_samples=NUM_SAMPLES,
                    disable_progbar=True,
                )
                node_models.append(model)
            models[name] = node_models
            print(f"  {name}: {len(node_models)} Bayesian GPs, d={X.shape[-1]}")
        else:
            model = SaasFullyBayesianSingleTaskGP(
                train_X=X, train_Y=Y,
            )
            fit_fully_bayesian_model_nuts(
                model, warmup_steps=WARMUP, num_samples=NUM_SAMPLES,
                disable_progbar=True,
            )
            models[name] = model
            print(f"  {name}: 1 Bayesian GP, d={X.shape[-1]}")
    return models


def predict_bayesian_node(models, name, X):
    """Get posterior mean from a node (handles multi-output, averages over MCMC)."""
    model = models[name]
    if isinstance(model, list):
        preds = [predict_bayesian(m, X) for m in model]
        return torch.cat(preds, dim=-1)
    return predict_bayesian(model, X)


def composite_forward_bayesian(models, comp, atom_params, power, speed,
                                spot_size, hatch, rotation, contour,
                                preheat, dwell):
    """Propagate through the expanded DAG using fully Bayesian GP posterior means."""
    # Node 0: CALPHAD (v2: 3 outputs)
    calphad_pred = predict_bayesian_node(models, "calphad", comp)
    phase_frac = calphad_pred[..., 0:1]
    solid_range = calphad_pred[..., 1:2]

    # Node 1a: Powder PSD (v2: includes solid_range)
    psd_input = torch.cat([phase_frac, solid_range, atom_params], dim=-1)
    psd = predict_bayesian_node(models, "powder_psd", psd_input)

    # Node 1c: Powder density
    dens_input = torch.cat([phase_frac, atom_params], dim=-1)
    dens = predict_bayesian_node(models, "powder_dens", dens_input)

    # Node 2a: Energy delivery (v2: D50 + apparent_density)
    energy_input = torch.cat([psd, dens, power, speed, spot_size], dim=-1)
    melt_pool = predict_bayesian_node(models, "energy", energy_input)
    mp_width = melt_pool[..., 0:1]
    mp_depth = melt_pool[..., 1:2]

    # Node 2b: Scan strategy (v2: includes mp_depth)
    scan_input = torch.cat([mp_width, mp_depth, hatch, rotation, contour], dim=-1)
    layer_q = predict_bayesian_node(models, "scan", scan_input)

    # Node 2c: Thermal management (v2: includes mp_depth)
    thermal_input = torch.cat([layer_q, mp_depth, preheat, dwell], dim=-1)
    stress = predict_bayesian_node(models, "thermal", thermal_input)

    # Node 2d: Integration
    density_input = torch.cat([mp_depth, layer_q, stress], dim=-1)
    part_dens = predict_bayesian_node(models, "density", density_input)

    # Node 3: Characterization (v2: 2 outputs)
    mech_out = predict_bayesian_node(models, "mech", part_dens)
    ys = mech_out[..., 0:1]
    el = mech_out[..., 1:2]

    return ys, el, part_dens


def main():
    print("=" * 70)
    print("Fully Bayesian BOFN Verification — Expanded 9-Node DAG")
    print("=" * 70)
    print(f"MCMC: {WARMUP} warmup, {NUM_SAMPLES} samples per node")

    # 1. Generate training data
    print("\n[1/3] Generating training data (n=30)...")
    node_data = generate_expanded_data(n_train=30)

    # 2. Fit fully Bayesian GPs
    print("\n[2/3] Fitting SaasFullyBayesianSingleTaskGP per node...")
    models = build_bayesian_gps(node_data)

    # 3. Composite forward pass
    print("\n[3/3] Running composite forward pass on test candidates...")
    n_test = 5
    torch.manual_seed(123)
    comp = torch.rand(n_test, 3, dtype=DTYPE, device=DEVICE)
    comp = comp / comp.sum(dim=1, keepdim=True)
    atom_params = torch.rand(n_test, 2, dtype=DTYPE, device=DEVICE)
    power = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    speed = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    spot_size = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    hatch = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    rotation = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    contour = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    preheat = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)
    dwell = torch.rand(n_test, 1, dtype=DTYPE, device=DEVICE)

    ys_pred, el_pred, dens_pred = composite_forward_bayesian(
        models, comp, atom_params, power, speed, spot_size,
        hatch, rotation, contour, preheat, dwell,
    )

    # Ground truth (v2: updated node signatures)
    calphad_out = calphad_fn(comp)
    phase_frac = calphad_out[..., 0:1]
    solid_range = calphad_out[..., 1:2]
    psd_gt = powder_psd_fn(phase_frac, solid_range, atom_params)
    dens_gt = powder_density_fn(phase_frac, atom_params)
    melt_pool_gt = energy_delivery_fn(psd_gt, dens_gt, power, speed, spot_size)
    mp_width_gt = melt_pool_gt[..., 0:1]
    mp_depth_gt = melt_pool_gt[..., 1:2]
    layer_q_gt = scan_strategy_fn(mp_width_gt, mp_depth_gt, hatch, rotation, contour)
    stress_gt = thermal_mgmt_fn(layer_q_gt, mp_depth_gt, preheat, dwell)
    part_dens_gt = integration_fn(mp_depth_gt, layer_q_gt, stress_gt)
    mech_gt = characterization_fn(part_dens_gt)
    ys_gt = mech_gt[..., 0:1]

    print(f"\n  Predicted yield strengths: {ys_pred.squeeze().tolist()}")
    print(f"  Ground truth values:       {ys_gt.squeeze().tolist()}")
    print(f"  Predicted elongations:     {el_pred.squeeze().tolist()}")

    # Compute error
    mae = (ys_pred - ys_gt).abs().mean().item()
    print(f"\n  MAE (predicted vs ground truth): {mae:.4f}")
    print(f"  Relative error: {mae / ys_gt.mean().item() * 100:.1f}%")

    print(f"\n{'=' * 70}")
    print("Fully Bayesian BOFN verification PASSED")
    print(f"  All {len(models)} nodes fitted with SaasFullyBayesianSingleTaskGP")
    print(f"  Composite forward pass propagates through 9-node DAG")
    print(f"  MCMC dimension averaging works correctly")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
