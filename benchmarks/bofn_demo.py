#!/usr/bin/env python3
"""
BOFN (Bayesian Optimization over Function Networks) in BoTorch — Demo

Implements a 4-node function network modeling the VCL alloy discovery pipeline:
  Node 0: CALPHAD screening (composition → phase fractions)
  Node 1: Powder production (phase fractions + process params → powder quality)
  Node 2: LPBF printing (powder quality + print params → part density)
  Node 3: Characterization (part density → mechanical properties)

Each node uses a SingleTaskGP with Normalize/Standardize transforms.
A composite forward pass propagates through the DAG.
A cost-aware variant demonstrates partial evaluation savings.

References:
  - Astudillo & Frazier (2021), "Bayesian Optimization of Function Networks", NeurIPS
  - Buathong et al. (2023), "Bayesian Optimization of Function Networks with Partial
    Evaluations" (p-KGFN)
  - BoTorch: https://botorch.org/

Usage:
  python benchmarks/bofn_demo.py
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
# Synthetic ground-truth functions for each pipeline stage
# ---------------------------------------------------------------------------

def calphad_fn(composition: torch.Tensor) -> torch.Tensor:
    """Node 0: CALPHAD screening.  composition (d=3) → phase_fraction (d=1)."""
    # Synthetic: only a narrow composition region has desirable phase stability
    # Models the reality that most random compositions are thermodynamically unfavorable
    center = torch.tensor([0.7, 0.2, 0.1], dtype=DTYPE, device=DEVICE)
    dist_sq = ((composition - center) ** 2).sum(dim=-1, keepdim=True)
    return torch.exp(-8.0 * dist_sq)  # peaks at 1.0 near center, decays to ~0


def powder_fn(phase_fraction: torch.Tensor, process_params: torch.Tensor) -> torch.Tensor:
    """Node 1: Powder production.
    phase_fraction (d=1) + process_params (d=2) → powder_quality (d=1)."""
    x = torch.cat([phase_fraction, process_params], dim=-1)  # (n, 3)
    return (0.6 * x[..., 0:1] + 0.3 * torch.cos(x[..., 1:2]) + 0.1 * x[..., 2:3])


def lpbf_fn(powder_quality: torch.Tensor, print_params: torch.Tensor) -> torch.Tensor:
    """Node 2: LPBF printing.
    powder_quality (d=1) + print_params (d=2) → part_density (d=1)."""
    x = torch.cat([powder_quality, print_params], dim=-1)  # (n, 3)
    return torch.sigmoid(2.0 * x[..., 0:1] + x[..., 1:2] - 0.5 * x[..., 2:3])


def characterization_fn(part_density: torch.Tensor) -> torch.Tensor:
    """Node 3: Characterization.
    part_density (d=1) → mechanical_property (d=1) — the final objective."""
    return 0.8 * part_density + 0.2 * torch.sin(5.0 * part_density)


# ---------------------------------------------------------------------------
# Generate synthetic training data for each node
# ---------------------------------------------------------------------------

def generate_node_data(n_train: int = 20):
    """Generate training data for each node using the synthetic ground-truth."""
    # Node 0 inputs: alloy composition (3 components, normalized to sum to 1)
    X0 = torch.rand(n_train, 3, dtype=DTYPE, device=DEVICE)
    X0 = X0 / X0.sum(dim=1, keepdim=True)
    Y0 = calphad_fn(X0)

    # Node 1 inputs: phase_fraction (from Node 0) + 2 process params
    phase_frac = Y0
    proc_params = torch.rand(n_train, 2, dtype=DTYPE, device=DEVICE)
    X1 = torch.cat([phase_frac, proc_params], dim=-1)
    Y1 = powder_fn(phase_frac, proc_params)

    # Node 2 inputs: powder_quality (from Node 1) + 2 print params
    powder_q = Y1
    print_params = torch.rand(n_train, 2, dtype=DTYPE, device=DEVICE)
    X2 = torch.cat([powder_q, print_params], dim=-1)
    Y2 = lpbf_fn(powder_q, print_params)

    # Node 3 inputs: part_density (from Node 2)
    X3 = Y2
    Y3 = characterization_fn(X3)

    return [(X0, Y0), (X1, Y1), (X2, Y2), (X3, Y3)]


# ---------------------------------------------------------------------------
# Build per-node GP models
# ---------------------------------------------------------------------------

def build_node_gps(node_data):
    """Fit a SingleTaskGP with Normalize/Standardize for each node."""
    models = []
    for i, (X, Y) in enumerate(node_data):
        model = SingleTaskGP(
            train_X=X,
            train_Y=Y,
            input_transform=Normalize(d=X.shape[-1]),
            outcome_transform=Standardize(m=1),
        )
        mll = ExactMarginalLogLikelihood(model.likelihood, model)
        fit_gpytorch_mll(mll)
        models.append(model)
        print(f"  Node {i} GP fitted — train_X shape {X.shape}, train_Y shape {Y.shape}")
    return models


# ---------------------------------------------------------------------------
# Composite forward pass through the function network DAG
# ---------------------------------------------------------------------------

def composite_forward(models, composition, process_params, print_params):
    """Propagate a candidate through the 4-node DAG using GP posterior means.

    Uses posterior means for point predictions. For full uncertainty
    quantification, Monte Carlo samples from each node's posterior should
    be propagated through downstream nodes instead.

    Args:
        models: list of 4 fitted SingleTaskGP models
        composition: (n, 3) alloy composition
        process_params: (n, 2) powder production parameters
        print_params: (n, 2) LPBF print parameters

    Returns:
        predicted mechanical property (n, 1)
    """
    # Node 0: CALPHAD
    pred0 = models[0].posterior(composition).mean  # (n, 1)

    # Node 1: Powder
    x1 = torch.cat([pred0, process_params], dim=-1)
    pred1 = models[1].posterior(x1).mean

    # Node 2: LPBF
    x2 = torch.cat([pred1, print_params], dim=-1)
    pred2 = models[2].posterior(x2).mean

    # Node 3: Characterization
    pred3 = models[3].posterior(pred2).mean

    return pred3


# ---------------------------------------------------------------------------
# Cost-aware partial evaluation
# ---------------------------------------------------------------------------

def cost_aware_screening(models, candidates, process_params, print_params,
                         calphad_cost=1.0, full_cost=1301.0, threshold=0.3):
    """Demonstrate cost-aware partial evaluation (p-KGFN concept).

    Runs all candidates through the cheap CALPHAD node first, then only
    promotes candidates whose predicted phase fraction exceeds a threshold
    to the expensive downstream nodes.

    Args:
        models: list of 4 fitted GP models
        candidates: (n, 3) compositions
        process_params: (n, 2) — reused for promoted candidates
        print_params: (n, 2) — reused for promoted candidates
        calphad_cost: cost per CALPHAD evaluation ($)
        full_cost: cost per full pipeline evaluation ($)
        threshold: phase-fraction threshold for promotion

    Returns:
        dict with screening results and cost savings
    """
    n = candidates.shape[0]

    # Stage 1: cheap CALPHAD screening on ALL candidates
    pred_phase = models[0].posterior(candidates).mean  # (n, 1)
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
    promoted_proc = process_params[mask] if process_params.shape[0] == n else process_params[:n_promoted]
    promoted_print = print_params[mask] if print_params.shape[0] == n else print_params[:n_promoted]
    predictions = composite_forward(models, promoted_comp, promoted_proc, promoted_print)

    # Avoid double-counting CALPHAD: full_cost already includes Node 0, which was
    # charged for all candidates in stage1_cost. Stage 2 should only charge the
    # incremental downstream cost for promoted candidates.
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("BOFN in BoTorch — 4-Node Alloy Discovery Function Network")
    print("=" * 70)

    # 1. Generate synthetic training data
    print("\n[1/4] Generating synthetic training data...")
    node_data = generate_node_data(n_train=30)

    # 2. Fit per-node GP models
    print("\n[2/4] Fitting per-node SingleTaskGP models...")
    models = build_node_gps(node_data)

    # 3. Composite forward pass on test candidates
    print("\n[3/4] Running composite forward pass on 5 test candidates...")
    test_comp = torch.rand(5, 3, dtype=DTYPE, device=DEVICE)
    test_comp = test_comp / test_comp.sum(dim=1, keepdim=True)
    test_proc = torch.rand(5, 2, dtype=DTYPE, device=DEVICE)
    test_print = torch.rand(5, 2, dtype=DTYPE, device=DEVICE)

    predictions = composite_forward(models, test_comp, test_proc, test_print)
    print(f"  Predicted mechanical properties:\n  {predictions.detach().squeeze(-1)}")

    # Ground truth for comparison
    gt_phase = calphad_fn(test_comp)
    gt_powder = powder_fn(gt_phase, test_proc)
    gt_density = lpbf_fn(gt_powder, test_print)
    gt_mech = characterization_fn(gt_density)
    print(f"  Ground truth values:\n  {gt_mech.squeeze(-1)}")

    # 4. Cost-aware partial evaluation
    print("\n[4/4] Cost-aware partial evaluation (p-KGFN concept)...")
    n_screen = 50
    screen_comp = torch.rand(n_screen, 3, dtype=DTYPE, device=DEVICE)
    screen_comp = screen_comp / screen_comp.sum(dim=1, keepdim=True)
    screen_proc = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)
    screen_print = torch.rand(n_screen, 2, dtype=DTYPE, device=DEVICE)

    result = cost_aware_screening(
        models, screen_comp, screen_proc, screen_print,
        calphad_cost=1.0,
        full_cost=1301.0,
        threshold=0.7,
    )

    print(f"  Candidates screened: {result['n_candidates']}")
    print(f"  Promoted to full pipeline: {result['n_promoted']}")
    print(f"  CALPHAD screening cost: ${result['stage1_cost']:,.0f}")
    print(f"  Downstream cost: ${result['stage2_cost']:,.0f}")
    print(f"  Total cost (with screening): ${result['total_cost']:,.0f}")
    print(f"  Naive cost (no screening): ${result['naive_cost']:,.0f}")
    print(f"  Savings: ${result['savings']:,.0f}")

    print("\n" + "=" * 70)
    print("BOFN demo complete. All 4 nodes fitted and propagated successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
