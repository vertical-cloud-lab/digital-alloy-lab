#!/usr/bin/env python3
"""
p-KGFN Demo — Partial Knowledge Gradient for Function Networks

Demonstrates the p-KGFN acquisition function from Buathong et al. (2024)
ported to modern BoTorch (>=0.12). Runs a complete BO loop on the
manufacturing test problem from the original paper.

This script:
  1. Sets up the 4-node manufacturing function network
  2. Generates initial observations via full network evaluation
  3. Fits a GaussianProcessNetwork (per-node GPs)
  4. Runs a BO loop comparing three acquisition strategies:
     - Thompson Sampling over the Function Network (TSFN)
     - p-KGFN (partial knowledge gradient for function networks)
     - Random baseline
  5. Reports optimization progress (best observed final-node output)

References:
  - Buathong et al. (2024) "Bayesian Optimization of Function Networks
    with Partial Evaluations", ICML 2024
  - Buathong & Frazier (2025) "Fast Bayesian Optimization of Function
    Networks with Partial Evaluations", AutoML 2025 (PMLR 293)
  - Original implementation: https://github.com/frazier-lab/partial_kgfn

Usage:
  python benchmarks/bofn_pkgfn_demo.py
"""

import sys
import time
import warnings

# Suppress non-strict tensor dimension warnings from GP fantasy models
warnings.filterwarnings("ignore", message=".*Non-strict enforcement.*")
warnings.filterwarnings("ignore", message=".*Could not update.*GenericDeterministicModel.*")

import torch
from botorch.acquisition.objective import GenericMCObjective
from botorch.fit import fit_gpytorch_mll
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.utils.sampling import draw_sobol_samples
from gpytorch.mlls import ExactMarginalLogLikelihood

sys.path.insert(0, ".")

from benchmarks.partial_kgfn.dag import DAG
from benchmarks.partial_kgfn.gp_network import (
    GaussianProcessNetwork,
    fit_gp_network,
)
from benchmarks.partial_kgfn.manufacturing_problem import ManufacturingGPNetwork
from benchmarks.partial_kgfn.partial_kgfn import PartialKnowledgeGradientFN
from benchmarks.partial_kgfn.thompson_sampling import ThompsonSamplingFN
from benchmarks.partial_kgfn.utils import (
    compute_posterior_mean_network,
    construct_obs_set,
)

torch.set_default_dtype(torch.double)
DEVICE = torch.device("cpu")


def generate_initial_data(problem, n_init=9):
    """Generate initial observations by evaluating the full network."""
    bounds = problem.bounds
    # Sobol samples in [lb, ub] for each dimension
    X_init = draw_sobol_samples(bounds=bounds, n=n_init, q=1).squeeze(-2)
    Y_init = problem.evaluate(X_init)  # n_init × n_nodes
    return X_init, Y_init


def build_gp_network(X, Y, problem):
    """Construct and fit a GaussianProcessNetwork from observation data."""
    train_X, train_Y = construct_obs_set(
        X=X,
        Y=Y,
        parent_nodes=problem.parent_nodes,
        active_input_indices=problem.active_input_indices,
    )
    model = GaussianProcessNetwork(
        train_X=train_X,
        train_Y=train_Y,
        dag=problem.dag,
        active_input_indices=problem.active_input_indices,
        node_groups=problem.node_groups,
        node_dims=problem.node_dims,
    )
    fit_gp_network(model)
    return model


def ts_fn_step(model, bounds, objective, n_candidates=2048):
    """One Thompson sampling step: score random candidates, pick the best."""
    ts_acqf = ThompsonSamplingFN(model=model, objective=objective)
    candidates = draw_sobol_samples(bounds=bounds, n=n_candidates, q=1).squeeze(-2)
    with torch.no_grad():
        ts_vals = ts_acqf(candidates.unsqueeze(1))
    best_idx = ts_vals.argmax()
    return candidates[best_idx].unsqueeze(0)


def pkgfn_step(model, problem, objective, n_fantasies=4, n_grid=50):
    """One p-KGFN step: evaluate each node, pick the best node+input.

    For each root node, evaluates p-KGFN on discrete candidates.
    This implements the cost-aware partial evaluation strategy from
    Buathong et al. (2024): p-KGFN selects both which node to evaluate
    AND what input to provide, maximising information gain per unit cost.

    Returns the best (X_full, node_idx) — the network input and node selected.
    """
    bounds = problem.bounds
    best_val = -torch.inf
    best_x = None
    best_node = None

    # Current best value from posterior mean
    X_grid = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)
    with torch.no_grad():
        current_vals = compute_posterior_mean_network(model, X_grid, objective)
    current_value = current_vals.max()

    # Fantasy candidates for inner optimisation
    X_fant_candidates = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)

    for node_group in problem.node_groups:
        k = node_group[0]
        active_idx = problem.active_input_indices[k]
        parents = problem.parent_nodes[k]

        # For this demo, only optimise over root nodes (nodes with active inputs
        # and no parent dependencies to enumerate)
        if len(parents) > 0:
            continue
        if len(active_idx) == 0:
            continue

        mask = torch.zeros(problem.n_nodes, dtype=torch.long)
        mask[k] = 1

        node_dim = problem.node_dims[k]

        pkgfn = PartialKnowledgeGradientFN(
            model=model,
            d=problem.dim,
            q=1,
            node_dim=node_dim,
            problem_bounds=bounds,
            X_fantasies_candidates=X_fant_candidates,
            X_evaluation_mask=mask,
            num_fantasies=n_fantasies,
            objective=objective,
            current_value=current_value,
        )

        # Discrete optimisation: evaluate p-KGFN on random candidates
        # (consistent with original paper's discrete approach)
        node_bounds = bounds[:, active_idx]
        n_raw = 32
        raw_cands = (
            node_bounds[0]
            + (node_bounds[1] - node_bounds[0])
            * torch.rand(n_raw, len(active_idx), dtype=torch.double)
        )
        try:
            with torch.no_grad():
                acq_vals = pkgfn(raw_cands.unsqueeze(1))
            best_raw_idx = acq_vals.argmax()
            acq_val = acq_vals[best_raw_idx].item()
            candidates = raw_cands[best_raw_idx].unsqueeze(0)
        except (RuntimeError, ValueError, torch.linalg.LinAlgError) as e:
            print(f"  p-KGFN evaluation failed for node {k}: {e}")
            continue

        # Cost-adjusted value
        cost_adjusted = acq_val / problem.node_costs[k]

        if cost_adjusted > best_val:
            best_val = cost_adjusted
            best_node = k
            # Build a full-dimensional X from the node's active inputs
            x_full = torch.zeros(1, problem.dim, dtype=torch.double)
            x_full[0, active_idx] = candidates.squeeze()
            # Fill non-active dims with random values
            for d_idx in range(problem.dim):
                if d_idx not in active_idx:
                    x_full[0, d_idx] = bounds[0, d_idx] + (
                        bounds[1, d_idx] - bounds[0, d_idx]
                    ) * torch.rand(1, dtype=torch.double)
            best_x = x_full

    return best_x, best_node


def random_step(bounds):
    """One random baseline step."""
    x = bounds[0] + (bounds[1] - bounds[0]) * torch.rand(1, bounds.shape[-1], dtype=torch.double)
    return x


def run_bo_loop(problem, algo="TSFN", n_init=9, n_iters=15, seed=0,
                cost_budget=None, verbose=True):
    """Run a complete BO loop on the manufacturing problem.

    Args:
        problem: ManufacturingGPNetwork instance.
        algo: One of "TSFN", "pKGFN", "Random".
        n_init: Number of initial full evaluations.
        n_iters: Number of BO iterations (used if cost_budget is None).
        seed: Random seed.
        cost_budget: If set, run until this total cost is reached instead
            of using n_iters.  All algorithms stop once cumulative cost
            would exceed the budget.
        verbose: Print per-iteration progress.

    Returns:
        dict with 'best_vals', 'total_cost', 'cost_trace', and
        'node_selections'.  cost_trace[i] is cumulative cost after step i
        (including initialisation at index 0).
    """
    torch.manual_seed(seed)
    objective = GenericMCObjective(lambda Y, X=None: Y[..., -1])
    bounds = problem.bounds

    # Initial data — full evaluations for all algorithms
    X, Y = generate_initial_data(problem, n_init=n_init)

    # Per-node observation lists (for partial evaluation support)
    train_X_nodes, train_Y_nodes = construct_obs_set(
        X=X, Y=Y,
        parent_nodes=problem.parent_nodes,
        active_input_indices=problem.active_input_indices,
    )

    best_vals = [Y[..., -1].max().item()]
    total_cost = sum(problem.node_costs) * n_init  # initial full evals
    cost_trace = [total_cost]
    node_selections = []

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Algorithm: {algo}  |  seed: {seed}")
        print(f"  Initial best: {best_vals[0]:.4f}  |  init cost: ${total_cost:.0f}")
        budget_str = f"${cost_budget}" if cost_budget else f"{n_iters} iters"
        print(f"  Budget: {budget_str}")
        print(f"{'='*60}")

    it = 0
    max_iters = 500  # safety cap
    while True:
        # Stopping condition
        if cost_budget is not None:
            if total_cost >= cost_budget:
                break
        else:
            if it >= n_iters:
                break
        if it >= max_iters:
            break

        t0 = time.time()

        # Fit GP network from per-node observations
        model = GaussianProcessNetwork(
            train_X=train_X_nodes,
            train_Y=train_Y_nodes,
            dag=problem.dag,
            active_input_indices=problem.active_input_indices,
            node_groups=problem.node_groups,
            node_dims=problem.node_dims,
        )
        fit_gp_network(model)

        # Select next point
        if algo == "TSFN":
            x_new = ts_fn_step(model, bounds, objective)
            node_selected = "full"
            iter_cost = sum(problem.node_costs)
        elif algo == "pKGFN":
            x_new, node_selected = pkgfn_step(model, problem, objective)
            if x_new is None:
                # Fallback to random if p-KGFN fails
                x_new = random_step(bounds)
                node_selected = "random_fallback"
                iter_cost = sum(problem.node_costs)
            else:
                iter_cost = problem.node_costs[node_selected]
        elif algo == "Random":
            x_new = random_step(bounds)
            node_selected = "full"
            iter_cost = sum(problem.node_costs)
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

        # Check if this step would exceed the budget
        if cost_budget is not None and total_cost + iter_cost > cost_budget:
            break

        # Evaluate and update observations
        if algo == "pKGFN" and isinstance(node_selected, int):
            # Partial evaluation: only evaluate and observe the selected node
            active_idx = problem.active_input_indices[node_selected]
            x_node_input = x_new[:, active_idx] if active_idx else x_new
            # For root nodes, evaluate directly
            y_node = problem.evaluate(x_node_input, idx=[node_selected])
            # Add observation only to the selected node's GP
            train_X_nodes[node_selected] = torch.cat(
                [train_X_nodes[node_selected], x_node_input], dim=0
            )
            train_Y_nodes[node_selected] = torch.cat(
                [train_Y_nodes[node_selected], y_node], dim=0
            )
            # For progress tracking only: evaluate full network to report
            # final-node value. The cost (iter_cost) was already set above
            # to only the selected node's cost — this eval is not billed.
            y_full = problem.evaluate(x_new)
            y_final = y_full[0, -1].item()
        else:
            # Full evaluation: observe all nodes
            y_new = problem.evaluate(x_new)  # 1 × n_nodes
            X = torch.cat([X, x_new], dim=0)
            Y = torch.cat([Y, y_new], dim=0)
            # Update per-node observation lists
            new_train_X, new_train_Y = construct_obs_set(
                X=x_new, Y=y_new,
                parent_nodes=problem.parent_nodes,
                active_input_indices=problem.active_input_indices,
            )
            for k in range(problem.n_nodes):
                train_X_nodes[k] = torch.cat(
                    [train_X_nodes[k], new_train_X[k]], dim=0
                )
                train_Y_nodes[k] = torch.cat(
                    [train_Y_nodes[k], new_train_Y[k]], dim=0
                )
            y_final = y_new[0, -1].item()

        total_cost += iter_cost
        node_selections.append(node_selected)

        # Track best using posterior mean over a grid (consistent across all algos)
        with torch.no_grad():
            grid = draw_sobol_samples(bounds=bounds, n=200, q=1).squeeze(-2)
            grid_vals = compute_posterior_mean_network(model, grid, objective)
            best_so_far = max(best_vals[-1], grid_vals.max().item())
        best_vals.append(best_so_far)
        cost_trace.append(total_cost)
        dt = time.time() - t0
        it += 1

        if verbose:
            print(
                f"  iter {it:3d} | "
                f"node={node_selected!s:15s} | "
                f"y_new={y_final:+.4f} | "
                f"best={best_so_far:+.4f} | "
                f"cost=${total_cost:.0f} | "
                f"{dt:.1f}s"
            )

    return {
        "best_vals": best_vals,
        "total_cost": total_cost,
        "cost_trace": cost_trace,
        "node_selections": node_selections,
    }


def main():
    print("=" * 70)
    print("p-KGFN Demo — Partial Knowledge Gradient for Function Networks")
    print("Buathong et al. (2024, ICML) ported to BoTorch 0.12+")
    print("=" * 70)

    # Set up the manufacturing test problem
    node_costs = [5, 10, 10, 45]  # Same as paper's "5_10_10_45" config
    problem = ManufacturingGPNetwork(node_costs=node_costs)
    print(f"\nProblem: Manufacturing GP Network")
    print(f"  Nodes: {problem.n_nodes}, Dim: {problem.dim}")
    print(f"  Node costs: {node_costs}")
    print(f"  DAG: Node 0 (x1,x2) → Node 1 → Node 3 (final)")
    print(f"       Node 2 (x3,x4) → Node 3 (final)")

    # ---- Run all three algorithms ----
    n_init = 9  # 2*dim + 1
    n_iters = 15
    seed = 42

    results = {}
    for algo in ["Random", "TSFN", "pKGFN"]:
        # Use the same seed for fair comparison
        problem_copy = ManufacturingGPNetwork(node_costs=node_costs)
        results[algo] = run_bo_loop(
            problem_copy, algo=algo, n_init=n_init, n_iters=n_iters, seed=seed
        )

    # ---- Summary ----
    print("\n" + "=" * 70)
    print("Summary: Best observed final-node value at each iteration")
    print("=" * 70)
    header = f"{'Iter':>4s}"
    for algo in results:
        header += f" | {algo:>10s}"
    print(header)
    print("-" * len(header))
    for i in range(n_iters + 1):
        row = f"{i:4d}"
        for algo in results:
            row += f" | {results[algo]['best_vals'][i]:+10.4f}"
        print(row)

    # Final values and costs
    print("\n--- Final best values and costs ---")
    for algo in results:
        r = results[algo]
        print(f"  {algo:>10s}: best={r['best_vals'][-1]:+.4f}  cost=${r['total_cost']:.0f}")

    # Check that p-KGFN and TSFN beat random
    random_final = results["Random"]["best_vals"][-1]
    for algo in ["TSFN", "pKGFN"]:
        final = results[algo]["best_vals"][-1]
        status = "✓ BEATS" if final > random_final else "✗ LOSES TO"
        print(f"  {algo} {status} Random ({final:+.4f} vs {random_final:+.4f})")

    # p-KGFN cost efficiency
    pkgfn_cost = results["pKGFN"]["total_cost"]
    tsfn_cost = results["TSFN"]["total_cost"]
    print(f"\n  p-KGFN cost: ${pkgfn_cost:.0f} ({pkgfn_cost/tsfn_cost*100:.0f}% of TSFN ${tsfn_cost:.0f})")

    print("\n✓ p-KGFN demo complete.")
    return results


if __name__ == "__main__":
    main()
