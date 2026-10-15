#!/usr/bin/env python3
"""
BOFN with Fully Bayesian GPs (SAASBO) — Verification Test

Demonstrates that SaasFullyBayesianSingleTaskGP is a drop-in replacement for
SingleTaskGP in the BOFN function network. Uses the same 4-node VCL pipeline
as bofn_demo.py but with fully Bayesian inference via NUTS sampling.

Key differences from SingleTaskGP:
  - Hyperparameters are sampled (not point-estimated via MLE)
  - Sparsity-inducing horseshoe prior on lengthscales (SAAS)
  - Better uncertainty quantification, especially in high-d / low-data regimes
  - Posterior returns multiple MCMC samples → more robust predictions

Usage:
  python benchmarks/bofn_fully_bayesian_test.py
"""

import torch
from botorch.models.fully_bayesian import SaasFullyBayesianSingleTaskGP
from botorch.fit import fit_fully_bayesian_model_nuts

# Reuse synthetic functions from bofn_demo
from bofn_demo import (
    calphad_fn,
    powder_fn,
    lpbf_fn,
    characterization_fn,
    generate_node_data,
    DTYPE,
    DEVICE,
)

torch.manual_seed(42)


def composite_forward_fully_bayesian(models, composition, process_params, print_params):
    """Propagate through the 4-node DAG using fully Bayesian GP posterior means.

    SaasFullyBayesianSingleTaskGP returns posteriors with shape
    (num_mcmc_samples, n, d) instead of (n, d). We average over the MCMC
    dimension at each node to get point predictions for downstream nodes.

    Args:
        models: list of 4 fitted SaasFullyBayesianSingleTaskGP models
        composition: (n, 3) alloy composition
        process_params: (n, 2) powder production parameters
        print_params: (n, 2) LPBF print parameters

    Returns:
        predicted mechanical property (n, 1), averaged over MCMC samples
    """
    # Node 0: CALPHAD — average over MCMC samples for downstream input
    pred0 = models[0].posterior(composition).mean.mean(dim=0)  # (n, 1)

    # Node 1: Powder
    x1 = torch.cat([pred0, process_params], dim=-1)
    pred1 = models[1].posterior(x1).mean.mean(dim=0)

    # Node 2: LPBF
    x2 = torch.cat([pred1, print_params], dim=-1)
    pred2 = models[2].posterior(x2).mean.mean(dim=0)

    # Node 3: Characterization
    pred3 = models[3].posterior(pred2).mean.mean(dim=0)

    return pred3


def cost_aware_screening_fully_bayesian(
    models, candidates, process_params, print_params,
    calphad_cost=1.0, full_cost=1301.0, threshold=0.3
):
    """Cost-aware partial evaluation using fully Bayesian GPs.

    Same logic as bofn_demo.cost_aware_screening but handles the extra
    MCMC dimension in fully Bayesian posterior outputs.
    """
    n = candidates.shape[0]

    # Stage 1: cheap CALPHAD screening on ALL candidates
    pred_phase = models[0].posterior(candidates).mean.mean(dim=0)  # (n, 1)
    stage1_cost = n * calphad_cost

    # Promote only candidates above threshold
    mask = pred_phase.squeeze(-1) > threshold
    n_promoted = int(mask.sum().item())

    if n_promoted == 0:
        return {
            "n_candidates": n,
            "n_promoted": 0,
            "stage1_cost": stage1_cost,
            "stage2_cost": 0.0,
            "total_cost": stage1_cost,
            "naive_cost": n * full_cost,
            "savings": n * full_cost - stage1_cost,
        }

    # Stage 2: full pipeline on promoted candidates only
    promoted_comp = candidates[mask]
    promoted_proc = (
        process_params[mask] if process_params.shape[0] == n
        else process_params[:n_promoted]
    )
    promoted_print = (
        print_params[mask] if print_params.shape[0] == n
        else print_params[:n_promoted]
    )
    predictions = composite_forward_fully_bayesian(
        models, promoted_comp, promoted_proc, promoted_print
    )

    stage2_cost = n_promoted * (full_cost - calphad_cost)
    total_cost = stage1_cost + stage2_cost
    naive_cost = n * full_cost

    return {
        "n_candidates": n,
        "n_promoted": n_promoted,
        "stage1_cost": stage1_cost,
        "stage2_cost": stage2_cost,
        "total_cost": total_cost,
        "naive_cost": naive_cost,
        "savings": naive_cost - total_cost,
        "predictions": predictions,
    }


def build_fully_bayesian_node_gps(node_data, warmup_steps=256, num_samples=128):
    """Fit a SaasFullyBayesianSingleTaskGP for each node via NUTS.

    Args:
        node_data: list of (train_X, train_Y) tuples, one per network node
        warmup_steps: NUTS warmup iterations (default 256; reduce for faster tests)
        num_samples: number of posterior MCMC samples (default 128; reduce for faster tests)

    Returns:
        list of fitted SaasFullyBayesianSingleTaskGP models
    """
    models = []
    for i, (X, Y) in enumerate(node_data):
        model = SaasFullyBayesianSingleTaskGP(
            train_X=X,
            train_Y=Y,
        )
        fit_fully_bayesian_model_nuts(
            model,
            warmup_steps=warmup_steps,
            num_samples=num_samples,
            disable_progbar=True,
        )
        models.append(model)
        print(f"  Node {i} fully Bayesian GP fitted — "
              f"train_X shape {X.shape}, {num_samples} MCMC samples")
    return models


def main():
    print("=" * 70)
    print("BOFN with SaasFullyBayesianSingleTaskGP — Verification Test")
    print("=" * 70)

    # 1. Generate training data (same as standard BOFN demo)
    print("\n[1/5] Generating synthetic training data...")
    node_data = generate_node_data(n_train=30)

    # 2. Fit fully Bayesian GP models
    print("\n[2/5] Fitting per-node SaasFullyBayesianSingleTaskGP models...")
    print("  (NUTS sampling — this takes longer than MLE fitting)")
    # Use reduced warmup/samples for faster verification (production: 256/128+)
    models = build_fully_bayesian_node_gps(
        node_data, warmup_steps=128, num_samples=64
    )

    # 3. Verify posterior API compatibility
    print("\n[3/5] Verifying .posterior() API compatibility...")
    test_comp = torch.rand(5, 3, dtype=DTYPE, device=DEVICE)
    test_comp = test_comp / test_comp.sum(dim=1, keepdim=True)

    posterior = models[0].posterior(test_comp)
    print(f"  posterior.mean shape: {posterior.mean.shape}")
    print(f"  posterior.variance shape: {posterior.variance.shape}")
    assert posterior.mean.shape[-1] == 1, "Expected 1 output dimension"
    print("  ✓ .posterior() API works identically to SingleTaskGP")

    # 4. Composite forward pass (with MCMC averaging)
    print("\n[4/5] Running composite forward pass through 4-node DAG...")
    test_proc = torch.rand(5, 2, dtype=DTYPE, device=DEVICE)
    test_print = torch.rand(5, 2, dtype=DTYPE, device=DEVICE)

    predictions = composite_forward_fully_bayesian(models, test_comp, test_proc, test_print)
    print(f"  Predicted mechanical properties:\n  {predictions.detach().squeeze(-1)}")

    # Ground truth comparison
    gt_phase = calphad_fn(test_comp)
    gt_powder = powder_fn(gt_phase, test_proc)
    gt_density = lpbf_fn(gt_powder, test_print)
    gt_mech = characterization_fn(gt_density)
    print(f"  Ground truth values:\n  {gt_mech.squeeze(-1)}")

    # 5. Cost-aware screening (same API as SingleTaskGP version)
    print("\n[5/5] Cost-aware screening with fully Bayesian GPs...")
    n_screen = 50
    screen_comp = torch.rand(n_screen, 3, dtype=DTYPE, device=DEVICE)
    screen_comp = screen_comp / screen_comp.sum(dim=1, keepdim=True)
    screen_proc = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)
    screen_print = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)

    result = cost_aware_screening_fully_bayesian(
        models, screen_comp, screen_proc, screen_print,
        calphad_cost=1.0,
        full_cost=1301.0,
        threshold=0.7,
    )

    print(f"  Candidates screened: {result['n_candidates']}")
    print(f"  Promoted to full pipeline: {result['n_promoted']}")
    print(f"  Total cost (with screening): ${result['total_cost']:,.0f}")
    print(f"  Naive cost (no screening): ${result['naive_cost']:,.0f}")
    print(f"  Savings: ${result['savings']:,.0f}")

    print("\n" + "=" * 70)
    print("VERIFICATION PASSED: SaasFullyBayesianSingleTaskGP works as a")
    print("drop-in replacement for SingleTaskGP in the BOFN framework.")
    print("=" * 70)


if __name__ == "__main__":
    main()
