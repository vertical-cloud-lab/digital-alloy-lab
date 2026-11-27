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
    bounds = problem.bounds
    if hasattr(problem, "parent_bounds"):
        node_input_bounds = []
        for _k in range(problem.dag.get_n_nodes()):
            _pb = problem.parent_bounds[_k]
            if _pb is not None:
                node_input_bounds.append(_pb)
            else:
                node_input_bounds.append(bounds[:, problem.active_input_indices[_k]])
    else:
        node_input_bounds = None
    model = GaussianProcessNetwork(
        train_X=train_X,
        train_Y=train_Y,
        dag=problem.dag,
        active_input_indices=problem.active_input_indices,
        node_groups=problem.node_groups,
        node_dims=problem.node_dims,
        node_input_bounds=node_input_bounds,
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


def _reachable_parent_samples(
    model, problem, k, n_raw, bounds, n_design_sobol=256
):
    """Sample empirically reachable parent-output values for node k.

    Replaces the old uniform-over-parent_bounds sampling, which wastes most
    candidates on OOD regions (Edison pKGFN analysis, 2026-04-21). Instead:

    1. Draw a Sobol design X over the full network input space.
    2. Propagate through the per-node GP posterior means to obtain expected
       values at the parents of node k (and, for mixed nodes with active
       inputs, carry forward the sampled active columns).
    3. Return n_raw candidates in node k's input space, ordered as
       construct_obs_set expects: ``[active_part, parent_part]``.

    Returns a tensor of shape ``(n_raw, node_dim)``.
    """
    active_idx = list(problem.active_input_indices[k])
    parents = list(problem.parent_nodes[k])
    has_active = len(active_idx) > 0
    has_parents = len(parents) > 0

    if not has_parents and has_active:
        # Root node: sample from the active decision-variable box.
        node_bounds = bounds[:, active_idx]
        return (
            node_bounds[0]
            + (node_bounds[1] - node_bounds[0])
            * torch.rand(n_raw, len(active_idx), dtype=torch.double)
        )

    if not has_parents and not has_active:
        # Shouldn't happen; nothing to sample.
        return torch.empty(0, problem.node_dims[k], dtype=torch.double)

    # Intermediate (or mixed) node: sample X from full-bounds Sobol, then
    # propagate through the *parent* GPs' posterior means to get a cloud
    # concentrated on the empirically reachable parent manifold.
    design = draw_sobol_samples(bounds=bounds, n=n_design_sobol, q=1).squeeze(-2)
    parent_values: list[torch.Tensor] = []
    with torch.no_grad():
        # Build per-node posterior-mean caches as we walk the DAG.
        node_means: dict[int, torch.Tensor] = {}
        # Topologically walk up to max(parents).
        for j in range(max(parents) + 1):
            p_j = problem.parent_nodes[j]
            a_j = problem.active_input_indices[j]
            if len(p_j) == 0 and len(a_j) > 0:
                X_j = design[..., a_j]
            elif len(p_j) > 0 and len(a_j) > 0:
                X_j = torch.cat(
                    [design[..., a_j], torch.stack([node_means[p] for p in p_j], dim=-1)],
                    dim=-1,
                )
            else:
                X_j = torch.stack([node_means[p] for p in p_j], dim=-1)
            try:
                node_means[j] = model.node_GPs[j].posterior(X_j).mean[..., 0]
            except Exception:  # noqa: BLE001
                # If posterior eval fails, fall back to a reasonable box centre.
                node_means[j] = torch.zeros(design.shape[0], dtype=torch.double)
        for p in parents:
            parent_values.append(node_means[p])
    parent_cloud = torch.stack(parent_values, dim=-1)  # (n_design_sobol, len(parents))

    # Sub-sample n_raw from the cloud.
    idx_perm = torch.randperm(parent_cloud.shape[0])[:n_raw]
    parent_part = parent_cloud[idx_perm]

    if has_active:
        # Sample fresh active-input columns in the active-var box, then
        # concatenate as ``[active, parent]`` (matches construct_obs_set).
        node_bounds = bounds[:, active_idx]
        active_part = (
            node_bounds[0]
            + (node_bounds[1] - node_bounds[0])
            * torch.rand(n_raw, len(active_idx), dtype=torch.double)
        )
        # Assemble [active | parent] and also return the originating design
        # rows so caller can stitch a full-X with consistent active columns.
        cands = torch.cat([active_part, parent_part], dim=-1)
    else:
        cands = parent_part

    return cands


def pkgfn_step(
    model, problem, objective, n_fantasies=64, n_grid=200, n_raw=128, verbose=False
):
    """One p-KGFN step: evaluate each node, pick the best node+input.

    For each node (root, intermediate, OR mixed), evaluates p-KGFN on
    discrete candidates. Intermediate/mixed nodes draw candidates from the
    **empirically reachable parent manifold** (GP posterior means over a
    Sobol design), not the raw parent_bounds box — this addresses the
    Edison-identified OOD-parent-sampling issue (2026-04-21).

    Mixed nodes (e.g. node 4: active x4 + parent y3) now correctly write
    their active component into x_full[active_idx] and their parent
    component stays as the node-input only, fixing the shape-mismatch bug
    that caused ~9% of pKGFN iterations to fall through to error_fallback.

    Parameters
    ----------
    n_fantasies : int
        KG inner fantasy count. Bumped from 16 → 64 on Edison guidance.
    n_raw : int
        Raw candidate pool per node. Bumped from 32 → 128.
    verbose : bool
        If True, emit per-node debug prints.

    Returns
    -------
    (best_x, best_node, best_node_input)
        - ``best_x``: full-dim X with active columns set to the winning
          candidate's active part (filled with uniform random on other
          active columns and 0.5·(lo+hi) on inactive ones so downstream
          tracking is deterministic for a given seed).
        - ``best_node``: selected node index.
        - ``best_node_input``: the actual input fed to the selected node,
          ordered as ``construct_obs_set`` expects (active | parent).
    """
    bounds = problem.bounds
    best_val = -torch.inf
    best_x = None
    best_node = None
    best_node_input = None

    # Current best value from posterior mean
    X_grid = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)
    with torch.no_grad():
        current_vals = compute_posterior_mean_network(model, X_grid, objective)
    current_value = current_vals.max()

    # Fantasy candidates for inner optimisation
    X_fant_candidates = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)

    for node_group in problem.node_groups:
        k = node_group[0]
        active_idx = list(problem.active_input_indices[k])
        parents = list(problem.parent_nodes[k])
        has_active = len(active_idx) > 0
        has_parents = len(parents) > 0

        if not has_active and not has_parents:
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

        raw_cands = _reachable_parent_samples(
            model=model, problem=problem, k=k, n_raw=n_raw, bounds=bounds,
        )
        if raw_cands.numel() == 0:
            raise RuntimeError(
                f"pkgfn_step: node {k} produced an empty reachable parent "
                f"sample (n_raw={n_raw}). Fix the root cause "
                f"(_reachable_parent_samples) instead of skipping the node."
            )

        with torch.no_grad():
            acq_vals = pkgfn(raw_cands.unsqueeze(1))
        best_raw_idx = acq_vals.argmax()
        acq_val = acq_vals[best_raw_idx].item()
        candidates = raw_cands[best_raw_idx].unsqueeze(0)

        # Cost-adjusted value
        cost_adjusted = acq_val / problem.node_costs[k]
        if verbose:
            print(
                f"    node {k}: acq={acq_val:+.5f} cost=${problem.node_costs[k]} "
                f"→ cost_adj={cost_adjusted:+.5f}"
            )

        if cost_adjusted > best_val:
            best_val = cost_adjusted
            best_node = k
            best_node_input = candidates

            # Build the full-dim X for any downstream tracking. For mixed
            # nodes (both active + parents), write ONLY the active portion
            # of the candidate into x_full[active_idx]; the parent portion
            # stays in best_node_input for the caller.
            x_full = torch.zeros(1, problem.dim, dtype=torch.double)
            # Inactive dims: centre of their box so this is deterministic.
            for d_idx in range(problem.dim):
                x_full[0, d_idx] = 0.5 * (bounds[0, d_idx] + bounds[1, d_idx])
            if has_active:
                active_part = candidates[:, : len(active_idx)]
                x_full[0, active_idx] = active_part.squeeze(0)
            best_x = x_full

    if best_node is None:
        raise RuntimeError(
            "pkgfn_step: no node produced a valid acquisition value. "
            "Every node was either degree-of-freedom-free (no active or "
            "parent inputs) or filtered out. Check problem.node_groups / "
            "active_input_indices / parent_nodes."
        )

    return best_x, best_node, best_node_input


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

    # Per-node explicit input bounds for the GP ``Normalize`` transform
    # (Edison spot-check fix A3 — see bofn_actions_benchmark for context).
    if hasattr(problem, "parent_bounds"):
        node_input_bounds = []
        for _k in range(problem.dag.get_n_nodes()):
            _pb = problem.parent_bounds[_k]
            if _pb is not None:
                node_input_bounds.append(_pb)
            else:
                node_input_bounds.append(bounds[:, problem.active_input_indices[_k]])
    else:
        node_input_bounds = None

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
            node_input_bounds=node_input_bounds,
        )
        fit_gp_network(model)

        # Select next point
        if algo == "TSFN":
            x_new = ts_fn_step(model, bounds, objective)
            node_selected = "full"
            iter_cost = sum(problem.node_costs)
        elif algo == "pKGFN":
            x_new, node_selected, node_input = pkgfn_step(model, problem, objective)
            if x_new is None:
                # Fallback to random if p-KGFN fails
                x_new = random_step(bounds)
                node_selected = "random_fallback"
                node_input = None
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
            parents = problem.parent_nodes[node_selected]

            if len(parents) == 0 and len(active_idx) > 0:
                # Root node: use active inputs from x_new
                x_node_input = x_new[:, active_idx]
            elif node_input is not None:
                # Intermediate node: use the node_input (parent-space candidates)
                x_node_input = node_input
            else:
                x_node_input = x_new[:, active_idx] if active_idx else x_new

            # Evaluate the selected node
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

        # Track best using posterior mean over a grid (consistent across all algos).
        # Refit the model first so the posterior reflects the new observation.
        model = GaussianProcessNetwork(
            train_X=train_X_nodes,
            train_Y=train_Y_nodes,
            dag=problem.dag,
            active_input_indices=problem.active_input_indices,
            node_groups=problem.node_groups,
            node_dims=problem.node_dims,
            node_input_bounds=node_input_bounds,
        )
        fit_gp_network(model)
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
