#!/usr/bin/env python3
"""
p-KGFN Benchmark — Expanded 9-Node LPBF Function Network

Runs the p-KGFN acquisition function on the physics-based 9-node LPBF
alloy development pipeline.  Supports checkpointed multi-seed runs.

Algorithms:
  - pKGFN:  partial Knowledge Gradient for Function Networks (cost-aware
            partial evaluation — selects which node to evaluate)
  - TSFN:   Thompson Sampling over the Function Network (full evaluations)
  - Random: random baseline (full evaluations)

Usage:
  # Single quick test (1 seed, small budget)
  python benchmarks/bofn_expanded_pkgfn_demo.py --quick

  # Full benchmark (20 seeds, $5000 budget, checkpointed)
  python benchmarks/bofn_expanded_pkgfn_demo.py --full

  # Resume from checkpoint
  python benchmarks/bofn_expanded_pkgfn_demo.py --full --resume

References:
  - Buathong et al. (2024) "BO of Function Networks with Partial Evaluations"
  - Buathong & Frazier (2025) "Fast BO of Function Networks"
  - Edison Scientific reviews: d0ad1eea, 6025bdcf, 98edd2c3
"""

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message=".*Non-strict enforcement.*")
warnings.filterwarnings(
    "ignore", message=".*Could not update.*GenericDeterministicModel.*"
)

import torch
from botorch.acquisition.objective import GenericMCObjective
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.utils.sampling import draw_sobol_samples

sys.path.insert(0, ".")

from benchmarks.partial_kgfn.dag import DAG
from benchmarks.partial_kgfn.gp_network import (
    GaussianProcessNetwork,
    fit_gp_network,
)
from benchmarks.partial_kgfn.expanded_problem import ExpandedLPBFProblem
from benchmarks.partial_kgfn.partial_kgfn import PartialKnowledgeGradientFN
from benchmarks.partial_kgfn.thompson_sampling import ThompsonSamplingFN
from benchmarks.partial_kgfn.utils import (
    compute_posterior_mean_network,
    construct_obs_set,
)

torch.set_default_dtype(torch.double)
DEVICE = torch.device("cpu")

RESULTS_DIR = Path("benchmarks/results")
CHECKPOINT_FILE = RESULTS_DIR / "expanded_pkgfn_checkpoint.json"


# ---------------------------------------------------------------------------
# BO loop components
# ---------------------------------------------------------------------------


def generate_initial_data(problem, n_init=15):
    """Generate initial observations by evaluating the full network."""
    bounds = problem.bounds
    X_init = draw_sobol_samples(bounds=bounds, n=n_init, q=1).squeeze(-2)
    # Normalize compositions to simplex
    X_init[:, :3] = X_init[:, :3] / X_init[:, :3].sum(dim=1, keepdim=True)
    Y_init = problem.evaluate(X_init)
    return X_init, Y_init


def build_gp_network(train_X_nodes, train_Y_nodes, problem):
    """Construct and fit a GaussianProcessNetwork from per-node observations."""
    model = GaussianProcessNetwork(
        train_X=train_X_nodes,
        train_Y=train_Y_nodes,
        dag=problem.dag,
        active_input_indices=problem.active_input_indices,
        node_groups=problem.node_groups,
        node_dims=problem.node_dims,
    )
    fit_gp_network(model)
    return model


def ts_fn_step(model, bounds, objective, n_candidates=2048):
    """One Thompson sampling step."""
    ts_acqf = ThompsonSamplingFN(model=model, objective=objective)
    candidates = draw_sobol_samples(bounds=bounds, n=n_candidates, q=1).squeeze(-2)
    # Normalize compositions to simplex
    candidates[:, :3] = candidates[:, :3] / candidates[:, :3].sum(dim=1, keepdim=True)
    with torch.no_grad():
        ts_vals = ts_acqf(candidates.unsqueeze(1))
    best_idx = ts_vals.argmax()
    return candidates[best_idx].unsqueeze(0)


def pkgfn_step(model, problem, objective, n_fantasies=8, n_grid=100, cost_power=1.0):
    """One p-KGFN step with group-aware cost.

    Evaluates p-KGFN for each node group, using the GROUP cost for
    cost-adjusted comparison.  Returns the best node and its input.

    Args:
        cost_power: Exponent for cost adjustment.  Classic VOI/cost uses 1.0.
            Values < 1 (e.g. 0.5 → VOI/√cost) reduce the advantage of cheap
            nodes.  Combined with the problem's group_fidelity discount:
                effective_cost = (base_cost / fidelity) ** cost_power
    """
    bounds = problem.bounds
    best_val = -torch.inf
    best_x = None
    best_node = None
    best_node_input = None

    # Current best posterior mean
    X_grid = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)
    X_grid[:, :3] = X_grid[:, :3] / X_grid[:, :3].sum(dim=1, keepdim=True)
    with torch.no_grad():
        current_vals = compute_posterior_mean_network(model, X_grid, objective)
    current_value = current_vals.max()

    # Fantasy candidates
    X_fant = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)
    X_fant[:, :3] = X_fant[:, :3] / X_fant[:, :3].sum(dim=1, keepdim=True)

    for node_group in problem.node_groups:
        k = node_group[0]  # Representative node for this group
        active_idx = problem.active_input_indices[k]
        parents = problem.parent_nodes[k]
        node_dim = problem.node_dims[k]
        group_cost, _ = problem.get_group_for_node(k)

        mask = torch.zeros(problem.n_nodes, dtype=torch.long)
        mask[k] = 1

        pkgfn = PartialKnowledgeGradientFN(
            model=model,
            d=problem.dim,
            q=1,
            node_dim=node_dim,
            problem_bounds=bounds,
            X_fantasies_candidates=X_fant,
            X_evaluation_mask=mask,
            num_fantasies=n_fantasies,
            objective=objective,
            current_value=current_value,
        )

        # Generate candidates
        n_raw = 32
        if len(parents) == 0 and len(active_idx) > 0:
            # Root node: sample from active variable bounds
            node_bounds = bounds[:, active_idx]
            raw_cands = node_bounds[0] + (node_bounds[1] - node_bounds[0]) * torch.rand(
                n_raw, len(active_idx), dtype=torch.double
            )
        elif len(parents) > 0:
            parent_bounds = problem.parent_bounds[k]
            if parent_bounds is not None:
                raw_cands = parent_bounds[0] + (
                    parent_bounds[1] - parent_bounds[0]
                ) * torch.rand(n_raw, node_dim, dtype=torch.double)
            else:
                continue
        else:
            continue

        try:
            with torch.no_grad():
                acq_vals = pkgfn(raw_cands.unsqueeze(1))
            best_raw_idx = acq_vals.argmax()
            acq_val = acq_vals[best_raw_idx].item()
            candidates = raw_cands[best_raw_idx].unsqueeze(0)
        except (RuntimeError, ValueError, torch.linalg.LinAlgError) as e:
            print(f"  p-KGFN failed for node {k} ({problem.node_names[k]}): {e}")
            continue

        # Cost-fidelity adjusted value
        g = problem._node_to_group[k]
        fidelity = problem.group_fidelity[g]
        effective_cost = group_cost / fidelity
        cost_adjusted = acq_val / (effective_cost ** cost_power)

        if cost_adjusted > best_val:
            best_val = cost_adjusted
            best_node = k
            best_node_input = candidates
            if len(active_idx) > 0:
                x_full = torch.zeros(1, problem.dim, dtype=torch.double)
                if len(parents) > 0:
                    # Non-root: candidate has [parent_outputs, active_inputs]
                    x_full[0, active_idx] = candidates.squeeze()[len(parents) :]
                else:
                    # Root: candidate is exactly the active inputs
                    x_full[0, active_idx] = candidates.squeeze()
                for d_idx in range(problem.dim):
                    if d_idx not in active_idx:
                        x_full[0, d_idx] = bounds[0, d_idx] + (
                            bounds[1, d_idx] - bounds[0, d_idx]
                        ) * torch.rand(1, dtype=torch.double)
                # Re-normalize compositions
                x_full[0, :3] = x_full[0, :3] / x_full[0, :3].sum()
                best_x = x_full
            else:
                best_x = bounds[0] + (bounds[1] - bounds[0]) * torch.rand(
                    1, problem.dim, dtype=torch.double
                )
                best_x[0, :3] = best_x[0, :3] / best_x[0, :3].sum()

    return best_x, best_node, best_node_input


def random_step(bounds):
    """One random baseline step."""
    x = bounds[0] + (bounds[1] - bounds[0]) * torch.rand(
        1, bounds.shape[-1], dtype=torch.double
    )
    x[0, :3] = x[0, :3] / x[0, :3].sum()
    return x


# ---------------------------------------------------------------------------
# BO loop with group-aware evaluation
# ---------------------------------------------------------------------------


def run_bo_loop(
    problem,
    algo="TSFN",
    n_init=15,
    cost_budget=5000,
    seed=0,
    verbose=True,
    n_fantasies=8,
    n_grid=100,
    cost_power=1.0,
):
    """Run a complete BO loop on the expanded LPBF problem.

    Supports group co-evaluation: when p-KGFN selects a node that belongs
    to a multi-node group, ALL nodes in the group are evaluated and
    the group cost is charged once.

    Args:
        problem: ExpandedLPBFProblem instance.
        algo: "pKGFN", "TSFN", or "Random".
        n_init: Number of initial full evaluations.
        cost_budget: Total cost budget (including initialisation).
        seed: Random seed.
        verbose: Print per-iteration progress.
        n_fantasies: Fantasy samples for p-KGFN.
        n_grid: Grid size for p-KGFN inner optimisation.
        cost_power: Exponent for p-KGFN cost adjustment.

    Returns:
        dict with results.
    """
    torch.manual_seed(seed)
    # Reset noise RNG so each algo with the same seed gets the same noise
    # on the same initial data (noise RNG is independent of global seed).
    problem._noise_rng = torch.Generator(device=DEVICE).manual_seed(seed + 2**16)
    objective = GenericMCObjective(lambda Y, X=None: Y[..., -1])
    bounds = problem.bounds
    full_cost = sum(problem._group_costs)

    # Initial data — full evaluations (noisy observations for GP, noiseless
    # ground truth for best-value tracking).
    X, Y = generate_initial_data(problem, n_init=n_init)
    Y_true = problem.evaluate(X, noisy=False)
    train_X_nodes, train_Y_nodes = construct_obs_set(
        X=X,
        Y=Y,
        parent_nodes=problem.parent_nodes,
        active_input_indices=problem.active_input_indices,
    )

    best_vals = [Y_true[..., -1].max().item()]
    total_cost = full_cost * n_init
    cost_trace = [total_cost]
    node_selections = []

    if verbose:
        print(f"\n{'='*65}")
        print(
            f"  {algo} | seed={seed} | init_best={best_vals[0]:.4f} "
            f"| init_cost=${total_cost:.0f} | budget=${cost_budget}"
        )
        print(f"{'='*65}")

    it = 0
    max_iters = 1000

    while total_cost < cost_budget and it < max_iters:
        t0 = time.time()

        # Fit GP network
        model = build_gp_network(train_X_nodes, train_Y_nodes, problem)

        # Select next point
        if algo == "TSFN":
            x_new = ts_fn_step(model, bounds, objective)
            node_selected = "full"
            iter_cost = full_cost
        elif algo == "pKGFN":
            x_new, node_selected, node_input = pkgfn_step(
                model,
                problem,
                objective,
                n_fantasies=n_fantasies,
                n_grid=n_grid,
                cost_power=cost_power,
            )
            if x_new is None:
                x_new = random_step(bounds)
                node_selected = "fallback"
                iter_cost = full_cost
            else:
                group_cost, group_nodes = problem.get_group_for_node(node_selected)
                iter_cost = group_cost
        elif algo == "Random":
            x_new = random_step(bounds)
            node_selected = "full"
            iter_cost = full_cost
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

        # Check budget
        if total_cost + iter_cost > cost_budget:
            break

        # Evaluate and update observations.
        # y_final is set below (noiseless at x_new for full evals;
        # noiseless at the posterior-mean recommendation for partial evals).
        y_final = float("-inf")  # safe sentinel in case tracking block is skipped

        if algo == "pKGFN" and isinstance(node_selected, int):
            # Group-aware partial evaluation
            group_cost, group_nodes = problem.get_group_for_node(node_selected)
            active_idx = problem.active_input_indices[node_selected]
            parents = problem.parent_nodes[node_selected]

            if len(parents) == 0 and len(active_idx) > 0:
                x_node_input = x_new[:, active_idx]
            elif node_input is not None:
                x_node_input = node_input
            else:
                x_node_input = x_new[:, active_idx] if active_idx else x_new

            # Evaluate ALL nodes in the group (they share the same input structure)
            for gk in group_nodes:
                y_gk = problem.evaluate(x_node_input, idx=[gk])
                train_X_nodes[gk] = torch.cat([train_X_nodes[gk], x_node_input], dim=0)
                train_Y_nodes[gk] = torch.cat([train_Y_nodes[gk], y_gk], dim=0)
            # y_final will be set by the posterior-mean recommender block below.
        else:
            # Full evaluation (noisy observations for GP training)
            y_new = problem.evaluate(x_new)
            y_true = problem.evaluate(x_new, noisy=False)
            X = torch.cat([X, x_new], dim=0)
            Y = torch.cat([Y, y_new], dim=0)
            new_train_X, new_train_Y = construct_obs_set(
                X=x_new,
                Y=y_new,
                parent_nodes=problem.parent_nodes,
                active_input_indices=problem.active_input_indices,
            )
            for k in range(problem.n_nodes):
                train_X_nodes[k] = torch.cat([train_X_nodes[k], new_train_X[k]], dim=0)
                train_Y_nodes[k] = torch.cat([train_Y_nodes[k], new_train_Y[k]], dim=0)
            y_final = y_true[0, -1].item()

        total_cost += iter_cost
        node_selections.append(
            node_selected
            if isinstance(node_selected, str)
            else problem.node_names[node_selected]
        )

        # Track best via noiseless ground truth.
        # For full evaluations, y_final is the noiseless value at x_new — valid.
        # For partial evaluations (pKGFN), x_new has random fill for non-active
        # dims, so we find the posterior-mean maximiser and evaluate it noiseless.
        if algo == "pKGFN" and isinstance(node_selected, int):
            model_rec = build_gp_network(train_X_nodes, train_Y_nodes, problem)
            with torch.no_grad():
                rec_grid = draw_sobol_samples(bounds=bounds, n=2048, q=1).squeeze(-2)
                rec_grid[:, :3] = rec_grid[:, :3] / rec_grid[:, :3].sum(
                    dim=1, keepdim=True
                )
                rec_vals = compute_posterior_mean_network(
                    model_rec, rec_grid, objective
                )
                x_rec = rec_grid[rec_vals.argmax()].unsqueeze(0)
            y_rec = problem.evaluate(x_rec, noisy=False)
            y_final = y_rec[0, -1].item()
        best_so_far = max(best_vals[-1], y_final)
        best_vals.append(best_so_far)
        cost_trace.append(total_cost)
        dt = time.time() - t0
        it += 1

        if verbose:
            node_str = (
                node_selected
                if isinstance(node_selected, str)
                else problem.node_names[node_selected]
            )
            print(
                f"  iter {it:3d} | "
                f"node={node_str:>16s} | "
                f"y={y_final:+.4f} | "
                f"best={best_so_far:.4f} | "
                f"cost=${total_cost:.0f} | "
                f"{dt:.1f}s"
            )

    return {
        "algo": algo,
        "seed": seed,
        "best_vals": best_vals,
        "total_cost": total_cost,
        "cost_trace": cost_trace,
        "node_selections": node_selections,
        "n_iters": it,
    }


# ---------------------------------------------------------------------------
# Checkpointed multi-seed runner
# ---------------------------------------------------------------------------


def run_checkpointed(
    n_seeds=20,
    cost_budget=5000,
    n_init=15,
    n_fantasies=8,
    n_grid=100,
    resume=False,
    noisy=False,
    cost_power=1.0,
):
    """Run multi-seed benchmark with per-seed checkpointing.

    After each seed completes for all 3 algorithms, results are saved.
    On resume, completed seeds are skipped.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing checkpoint
    if resume and CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            checkpoint = json.load(f)
        print(
            f"Resuming from checkpoint: {len(checkpoint['completed_seeds'])} "
            f"seeds done"
        )
    else:
        checkpoint = {
            "config": {
                "n_seeds": n_seeds,
                "cost_budget": cost_budget,
                "n_init": n_init,
                "n_fantasies": n_fantasies,
                "n_grid": n_grid,
                "noisy": noisy,
                "cost_power": cost_power,
                "problem": "ExpandedLPBFProblem",
                "n_nodes": 10,
                "dim": 13,
            },
            "completed_seeds": [],
            "results": {"pKGFN": [], "TSFN": [], "Random": []},
        }

    print("=" * 65)
    print("Expanded LPBF p-KGFN Benchmark (checkpointed)")
    print(f"  {n_seeds} seeds × 3 algorithms | budget=${cost_budget}")
    print(f"  n_fantasies={n_fantasies} | n_grid={n_grid} | n_init={n_init}")
    if noisy:
        print(f"  noisy=True | cost_power={cost_power}")
    print("=" * 65)

    for seed_idx in range(n_seeds):
        if seed_idx in checkpoint["completed_seeds"]:
            print(f"\nSeed {seed_idx}: already completed, skipping")
            continue

        print(f"\n{'='*65}")
        print(f"  SEED {seed_idx + 1}/{n_seeds}")
        print(f"{'='*65}")

        problem = ExpandedLPBFProblem(seed=seed_idx, noisy=noisy)
        seed_results = {}

        for algo in ["Random", "TSFN", "pKGFN"]:
            t0 = time.time()
            result = run_bo_loop(
                problem=problem,
                algo=algo,
                n_init=n_init,
                cost_budget=cost_budget,
                seed=seed_idx * 1000,
                n_fantasies=n_fantasies,
                n_grid=n_grid,
                cost_power=cost_power,
            )
            elapsed = time.time() - t0
            result["wall_time_s"] = elapsed
            seed_results[algo] = result
            checkpoint["results"][algo].append(result)
            print(
                f"  {algo} done: best={result['best_vals'][-1]:.4f}, "
                f"iters={result['n_iters']}, {elapsed:.0f}s"
            )

        checkpoint["completed_seeds"].append(seed_idx)

        # Save checkpoint
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(checkpoint, f, indent=2)
        print(
            f"\n  Checkpoint saved ({len(checkpoint['completed_seeds'])} "
            f"seeds complete)"
        )

    # Final summary
    print("\n" + "=" * 65)
    print("FINAL RESULTS SUMMARY")
    print("=" * 65)
    for algo in ["pKGFN", "TSFN", "Random"]:
        finals = [r["best_vals"][-1] for r in checkpoint["results"][algo]]
        if finals:
            mean = sum(finals) / len(finals)
            std = (
                sum((x - mean) ** 2 for x in finals) / max(len(finals) - 1, 1)
            ) ** 0.5
            times = [r.get("wall_time_s", 0) for r in checkpoint["results"][algo]]
            avg_time = sum(times) / len(times) if times else 0
            print(
                f"  {algo:>8s}: best={mean:.4f} ± {std:.4f} "
                f"(n={len(finals)}, avg {avg_time:.0f}s/seed)"
            )

    return checkpoint


# ---------------------------------------------------------------------------
# Quick single-seed test
# ---------------------------------------------------------------------------


def quick_test(noisy=False, cost_power=1.0):
    """Run a quick test with 1 seed and small budget."""
    print("=" * 65)
    print("Quick Test — Expanded LPBF p-KGFN (1 seed, small budget)")
    print("=" * 65)

    problem = ExpandedLPBFProblem(noisy=noisy)
    print(f"\nProblem: {problem.n_nodes} nodes, d={problem.dim}")
    print(f"  Node groups: {len(problem.node_groups)}")
    print(f"  Full pipeline cost: ${sum(problem._group_costs)}")
    print(f"  Optimal YS ~= {problem.optimal_value:.4f}")
    if noisy:
        print(f"  noisy=True | cost_power={cost_power}")
    print(f"\n  DAG topology:")
    for k in range(problem.n_nodes):
        parents = problem.parent_nodes[k]
        active = problem.active_input_indices[k]
        cost = problem.node_costs[k]
        p_str = f"parents={parents}" if parents else "root"
        print(
            f"    Node {k:2d} ({problem.node_names[k]:>16s}): "
            f"{p_str:30s} active={active} cost=${cost}"
        )

    results = {}
    budget = 2500  # Small budget for quick test
    n_init = 10

    for algo in ["Random", "TSFN", "pKGFN"]:
        t0 = time.time()
        results[algo] = run_bo_loop(
            problem=problem,
            algo=algo,
            n_init=n_init,
            cost_budget=budget,
            seed=42,
            n_fantasies=8,
            n_grid=100,
            cost_power=cost_power,
        )
        elapsed = time.time() - t0
        r = results[algo]
        print(
            f"\n  {algo}: best={r['best_vals'][-1]:.4f}, "
            f"iters={r['n_iters']}, cost=${r['total_cost']:.0f}, {elapsed:.0f}s"
        )

    print("\n" + "=" * 65)
    print("Convergence comparison:")
    print("=" * 65)
    max_len = max(len(r["best_vals"]) for r in results.values())
    header = f"{'Step':>4s}"
    for algo in results:
        header += f" | {algo:>10s}"
    print(header)
    for i in range(max_len):
        row = f"{i:4d}"
        for algo in results:
            bv = results[algo]["best_vals"]
            val = bv[i] if i < len(bv) else bv[-1]
            row += f" | {val:10.4f}"
        print(row)

    # Node selection analysis for p-KGFN
    if "pKGFN" in results:
        sels = results["pKGFN"]["node_selections"]
        print(f"\np-KGFN node selections ({len(sels)} steps):")
        from collections import Counter

        counts = Counter(sels)
        for node, count in counts.most_common():
            print(f"  {node}: {count} ({100*count/len(sels):.0f}%)")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Expanded LPBF p-KGFN benchmark")
    parser.add_argument(
        "--quick", action="store_true", help="Quick test (1 seed, $1000 budget)"
    )
    parser.add_argument(
        "--full", action="store_true", help="Full benchmark (20 seeds, checkpointed)"
    )
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--n-seeds", type=int, default=20)
    parser.add_argument("--budget", type=int, default=5000)
    parser.add_argument("--n-init", type=int, default=15)
    parser.add_argument("--n-fantasies", type=int, default=8)
    parser.add_argument("--n-grid", type=int, default=100)
    parser.add_argument(
        "--noisy",
        action="store_true",
        help="Add heteroscedastic observation noise (cheap nodes noisier)",
    )
    parser.add_argument(
        "--cost-power",
        type=float,
        default=1.0,
        help="Exponent for pKGFN cost adjustment (default 1.0 = VOI/eff_cost)",
    )
    args = parser.parse_args()

    if args.quick:
        quick_test(noisy=args.noisy, cost_power=args.cost_power)
    elif args.full:
        run_checkpointed(
            n_seeds=args.n_seeds,
            cost_budget=args.budget,
            n_init=args.n_init,
            n_fantasies=args.n_fantasies,
            n_grid=args.n_grid,
            resume=args.resume,
            noisy=args.noisy,
            cost_power=args.cost_power,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
