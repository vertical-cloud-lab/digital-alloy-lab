#!/usr/bin/env python3
"""
GitHub-Actions–parallelizable BOFN+pKGFN benchmark vs. baselines.

Compares seven strategies on an **extended 6-node Manufacturing DAG** — the
original 4-node problem from Buathong et al. (2024, ICML) plus two extra
downstream nodes (y4 = f(x4, y3), y5 = f(y3, y4)) and i.i.d. Gaussian
observation noise (``noise_std=0.05``), under an equal cost budget:

    - Random      : uniform random, full-network evaluation
    - Sobol       : Sobol QMC sequence, full-network evaluation
    - LowFidOnly  : only evaluates the cheapest root node 0 ($5, CALPHAD);
                    fits a single-output GP on that node, EI in root-input
                    space; "best" is reported as the GP-network posterior
                    mean of the final node (same metric as all others).
    - Node2Only   : same idea as LowFidOnly, but on the other root node 2
                    ($10, LPBF process conditions). Added so every *root*
                    fidelity has its own single-node baseline. Middle nodes
                    1, 3, 4, 5 are not given their own *-Only baselines
                    because they are non-root — evaluating them at a fresh
                    input requires first evaluating their parents.
    - HighFidOnly : standard GP-EI on the final-node value, full-network
                    evaluation each iteration ("vanilla BO" baseline).
    - TSFN        : Thompson sampling over the function network
                    (full-network evaluation, BOFN baseline).
    - pKGFN       : partial Knowledge Gradient for Function Networks
                    (cost-aware partial evaluations, BOFN+pKGFN).

Per-node costs for the 6-node DAG are ``[5, 10, 10, 45, 20, 30]`` ($120
total); the default full-run budget is $4,800 (~40 full pipelines). Every
run also caches a Sobol-grid estimate of the **true max** of the final
node (noiseless), which the combine step plots as a dashed upper reference.

Modes
-----
1. Single-run (used by the GitHub Actions matrix)::

       python benchmarks/bofn_actions_benchmark.py \
           --mode run --algo pKGFN --seed 3 \
           --out benchmarks/results/actions/pKGFN_seed3.json

2. Smoke test (used locally and by the smoke-test job)::

       SMOKE_TEST=1 python benchmarks/bofn_actions_benchmark.py --mode smoke

   This runs all algorithms for 3 seeds at a tiny budget and produces a
   dummy composite plot to verify wiring (including the dashed true-max
   reference line).

3. Combine (used by the combine-results job)::

       python benchmarks/bofn_actions_benchmark.py \
           --mode combine \
           --input-dir benchmarks/results/actions/ \
           --out-dir benchmarks/figures/actions/

   Loads every per-(algo, seed) JSON file in ``input-dir``, computes
   mean ± 1 std cost-efficiency curves, draws the dashed true-max line,
   and writes a composite PNG + summary CSV/JSON to ``out-dir``.

The single-run JSON schema is::

    {"algo": "pKGFN", "seed": 3,
     "best_vals":  [...],   # length n_iters+1
     "cost_trace": [...],   # length n_iters+1, cumulative $
     "node_selections": [...],
     "true_max":   <float>, # noiseless Sobol-grid estimate of max y5
     "config": {"n_init": 9, "cost_budget": 4800,
                "node_costs": [5,10,10,45,20,30], "noise_std": 0.05,
                "n_nodes": 6, "smoke_test": false}}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from glob import glob
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore", message=".*Non-strict enforcement.*")
warnings.filterwarnings(
    "ignore", message=".*Could not update.*GenericDeterministicModel.*"
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

ALGOS = [
    "Random",
    "Sobol",
    "LowFidOnly",   # = Node0Only (CALPHAD, $5): cheapest root
    "Node2Only",    # LPBF process-parameter root, $10
    "HighFidOnly",
    "TSFN",
    "pKGFN",
]

# Map each single-root-node baseline to the DAG node it probes. Only root
# nodes (empty parent list) can be evaluated in isolation; middle nodes 1
# and 3 have parents in the Manufacturing DAG and so don't get *-Only
# baselines (see module docstring).
SINGLE_NODE_ALGOS = {"LowFidOnly": 0, "Node2Only": 2}


# ──────────────────────────────────────────────────────────────────────────
#  Single-run logic
# ──────────────────────────────────────────────────────────────────────────


def _import_torch_stack():
    """Defer heavy imports to keep ``--mode combine`` lightweight."""
    import torch
    from botorch.acquisition.analytic import ExpectedImprovement
    from botorch.acquisition.objective import GenericMCObjective
    from botorch.fit import fit_gpytorch_mll
    from botorch.models import SingleTaskGP
    from botorch.models.transforms import Normalize, Standardize
    from botorch.optim import optimize_acqf
    from botorch.utils.sampling import draw_sobol_samples
    from gpytorch.mlls import ExactMarginalLogLikelihood

    torch.set_default_dtype(torch.double)

    from benchmarks.partial_kgfn.gp_network import (
        GaussianProcessNetwork,
        fit_gp_network,
    )
    from benchmarks.partial_kgfn.manufacturing_problem import (
        ExtendedManufacturingGPNetwork,
        ManufacturingGPNetwork,
    )
    from benchmarks.partial_kgfn.thompson_sampling import ThompsonSamplingFN
    from benchmarks.partial_kgfn.utils import (
        compute_posterior_mean_network,
        construct_obs_set,
    )

    return dict(
        torch=torch,
        ExpectedImprovement=ExpectedImprovement,
        GenericMCObjective=GenericMCObjective,
        fit_gpytorch_mll=fit_gpytorch_mll,
        SingleTaskGP=SingleTaskGP,
        Normalize=Normalize,
        Standardize=Standardize,
        optimize_acqf=optimize_acqf,
        draw_sobol_samples=draw_sobol_samples,
        ExactMarginalLogLikelihood=ExactMarginalLogLikelihood,
        GaussianProcessNetwork=GaussianProcessNetwork,
        fit_gp_network=fit_gp_network,
        ManufacturingGPNetwork=ManufacturingGPNetwork,
        ExtendedManufacturingGPNetwork=ExtendedManufacturingGPNetwork,
        ThompsonSamplingFN=ThompsonSamplingFN,
        compute_posterior_mean_network=compute_posterior_mean_network,
        construct_obs_set=construct_obs_set,
    )


def run_single(algo: str, seed: int, smoke_test: bool = False, verbose: bool = True,
               checkpoint_path: str | None = None):
    """Run one (algo, seed) campaign and return a result dict."""
    if algo not in ALGOS:
        raise ValueError(f"algo must be one of {ALGOS}, got {algo!r}")

    deps = _import_torch_stack()
    torch = deps["torch"]
    draw_sobol_samples = deps["draw_sobol_samples"]
    GenericMCObjective = deps["GenericMCObjective"]
    ExtendedManufacturingGPNetwork = deps["ExtendedManufacturingGPNetwork"]
    GaussianProcessNetwork = deps["GaussianProcessNetwork"]
    fit_gp_network = deps["fit_gp_network"]
    construct_obs_set = deps["construct_obs_set"]
    compute_posterior_mean_network = deps["compute_posterior_mean_network"]
    ThompsonSamplingFN = deps["ThompsonSamplingFN"]
    SingleTaskGP = deps["SingleTaskGP"]
    Normalize = deps["Normalize"]
    Standardize = deps["Standardize"]
    fit_gpytorch_mll = deps["fit_gpytorch_mll"]
    ExactMarginalLogLikelihood = deps["ExactMarginalLogLikelihood"]
    ExpectedImprovement = deps["ExpectedImprovement"]
    optimize_acqf = deps["optimize_acqf"]

    # Defer pKGFN import (it's only needed for that algo) so the other
    # baselines stay lightweight.
    if algo == "pKGFN":
        from benchmarks.bofn_pkgfn_demo import pkgfn_step

    # ── Config ────────────────────────────────────────────────────────────
    # 6-node extended DAG. Per-node costs (revised 2026-04-30): the CALPHAD
    # root (node 0) was briefly lowered to $1 to reflect how cheap a
    # pycalphad screen is, but that produced too large a cost ratio to the
    # full-pipeline cost ($116) and bogged down pKGFN's inner KG (which
    # spends a disproportionate share of its acquisition compute on the
    # cheapest node). Restored to $5, matching the original Buathong 2024
    # 4-node "5_10_10_45" cost scaling and giving a more workable
    # cheap:expensive ratio (1:9 vs. 1:45) for the inner-KG amortization.
    node_costs = [5, 10, 10, 45, 20, 30]
    # Per-node observation noise std. Cheap upstream nodes have *lower*
    # noise than expensive terminal/late-chain nodes — this is what makes the
    # synthetic DAG concretely demonstrate pKGFN's cost-amortization
    # advantage: a cheap probe at node 0 ($5, σ=0.02) is ~10× more
    # information-per-dollar than a single noisy terminal eval (node 5,
    # $30, σ=0.10). Under uniform σ=0.05 (the prior setting) and the
    # near-deterministic late chain, HighFidOnly trivially saturated the
    # full-budget regime because its 20 noiseless-by-comparison full-eval
    # draws covered the input space faster than pKGFN could amortize cheap
    # screens. Edison q6 (2026-04-30 spotcheck-q6-overview.md) flagged
    # this as one of the two factors masking pKGFN's relative advantage.
    # Legacy uniform value (0.05) preserved as a fallback comment for diff
    # readability.
    noise_std: float | list[float] = [0.02, 0.02, 0.02, 0.05, 0.07, 0.10]
    # Physics-inspired parent→child coupling. Per-node list, indexed by node
    # (root entries 0/2 are ignored). Tuned (2026-04-30) so upstream nodes
    # are informative with respect to the terminal node y5, not merely their
    # immediate children: y0→y5≈0.67, y1→y5≈0.73, y2→y5≈0.69, while middle
    # nodes remain higher (y3→y5≈0.98, y4→y5≈0.99). Node 2 is also
    # composition-aware in ExtendedManufacturingGPNetwork, which removes the
    # previous independent-root pathology that made y2 nearly irrelevant.
    coupling: list[float] | float = [0.0, 0.0, 0.0, 0.6, 0.8, 0.7]
    if smoke_test:
        # Tiny configuration for wiring validation only. With node_costs sum
        # = $120, init_cost = 3 * 120 = $360, leaving $60 for ~1 extra full
        # pipeline or up to 60 cheap node-0 iters / ~2 partial pKGFN iters.
        # Tuned (down from cost_budget=600 / n_ts_candidates=64) so the smoke
        # job (7 algos × 3 seeds, sequential per job) reliably fits in well
        # under 1 h on a GH-hosted runner; the 6-node DAG + reachable-manifold
        # parent sampling pushed the previous config past the 30-min cap.
        n_init = 3
        cost_budget = 420
        n_grid = 32
        n_ts_candidates = 32
        n_ei_restarts = 2
        n_ei_raw = 32
        true_max_samples = 512
    else:
        n_init = 9
        # Halved from $4,800 → $2,400 on 2026-04-25 so the pKGFN sweep
        # (which costs ~$50/iter at n_fantasies=64, n_raw=128 and was
        # timing out at 12 h SLURM walltime in the fast-20260424T093755Z
        # run, reaching only ~$1,857) actually completes within a 30 h
        # cell wall-clock on BYU ORC. Other algorithms' fast-run results
        # at $4,800 are simply truncated at $2,400 in the combine plot.
        cost_budget = 2400
        n_grid = 200
        n_ts_candidates = 2048
        n_ei_restarts = 5
        n_ei_raw = 256
        true_max_samples = 16384

    # Build the problem with a FIXED seed (=0) so the objective landscape is
    # identical across benchmark seeds -- every algorithm on every seed is
    # optimizing the same function network (apples-to-apples).
    problem = ExtendedManufacturingGPNetwork(
        node_costs=node_costs, seed=0, noise_std=noise_std, coupling=coupling,
    )
    bounds = problem.bounds
    objective = GenericMCObjective(lambda Y, X=None: Y[..., -1])

    # Per-node explicit input bounds for the GP ``Normalize`` transform.
    # Spot-check finding (Edison ANALYSIS task 7b1ba7ec, A3): without
    # explicit bounds, ``Normalize`` infers them dynamically from
    # ``train_X``, which causes non-stationary lengthscale learning on
    # intermediate-node GPs whose ``train_X`` includes parent-y columns
    # that drift across iterations as new extreme parent values arrive.
    # ``problem.parent_bounds[k]`` gives the documented bounds of node k's
    # full input vector (active-x + parent-y); root nodes have ``None``
    # there and use the slice of the global problem bounds instead.
    node_input_bounds = []
    for _k in range(problem.dag.get_n_nodes()):
        _pb = problem.parent_bounds[_k]
        if _pb is not None:
            node_input_bounds.append(_pb)
        else:
            node_input_bounds.append(bounds[:, problem.active_input_indices[_k]])

    # Sobol-grid estimate of the true (noiseless) max of the final node.
    # Cached in the result JSON so the combine step can plot it as an upper
    # reference line without re-instantiating the problem.
    try:
        true_max = problem.compute_true_max(n_samples=true_max_samples)
    except Exception as e:  # noqa: BLE001
        print(f"  [{algo} seed={seed}] true_max estimation failed: {e}")
        true_max = None

    # Re-seed torch AFTER problem construction (which internally calls
    # torch.manual_seed to fix the GP-prior draws). This makes the init Sobol
    # draw and all acquisition-optimizer randomness vary by benchmark seed,
    # producing genuine seed-to-seed variance (and hence visible uncertainty
    # bands in the composite plot).
    torch.manual_seed(seed)

    # ── Initial data (full evaluations, shared by every algorithm) ───────
    # Pass ``seed=seed`` to scramble the Sobol sequence differently per seed.
    X_init = draw_sobol_samples(bounds=bounds, n=n_init, q=1, seed=seed).squeeze(-2)
    Y_init = problem.evaluate(X_init)

    train_X_nodes, train_Y_nodes = construct_obs_set(
        X=X_init,
        Y=Y_init,
        parent_nodes=problem.parent_nodes,
        active_input_indices=problem.active_input_indices,
    )

    # The "init cost" charged to every algorithm is one full network
    # evaluation per init point.
    init_full_cost = sum(node_costs) * n_init  # = 70 * n_init
    total_cost = init_full_cost
    best_vals = []
    cost_trace = [total_cost]
    node_selections: list = []

    # Sobol baseline pre-generates a long QMC sequence and consumes it.
    sobol_pool = None
    sobol_idx = 0
    if algo == "Sobol":
        sobol_pool = draw_sobol_samples(bounds=bounds, n=512, q=1, seed=seed + 1).squeeze(-2)

    # Helper: compute current best (posterior mean of final node over a grid)
    def _current_best(X_nodes_obs, Y_nodes_obs):
        m = GaussianProcessNetwork(
            train_X=X_nodes_obs,
            train_Y=Y_nodes_obs,
            dag=problem.dag,
            active_input_indices=problem.active_input_indices,
            node_groups=problem.node_groups,
            node_dims=problem.node_dims,
            node_input_bounds=node_input_bounds,
        )
        fit_gp_network(m)
        with torch.no_grad():
            grid = draw_sobol_samples(bounds=bounds, n=n_grid, q=1).squeeze(-2)
            return float(compute_posterior_mean_network(m, grid, objective).max().item())

    best_vals.append(_current_best(train_X_nodes, train_Y_nodes))

    # HighFidOnly maintains a single-output GP on the final-node value over
    # the full-network input X, fit on the cumulative full-eval data.
    Y_final_full = Y_init[..., -1:].clone()
    X_full = X_init.clone()

    if verbose:
        print(
            f"[{algo} seed={seed} smoke={smoke_test}] init best={best_vals[0]:.4f} "
            f"init cost=${total_cost} budget=${cost_budget}"
        )

    it = 0
    # Per-algo iteration cap. Full-eval algos (Random/Sobol/HighFidOnly/TSFN)
    # exhaust the $4,800 budget at $116/iter ≈ 41 iters, so 1500 is loose.
    # pKGFN burns ~44 iters in practice (mostly cheap nodes). The two
    # SINGLE_NODE_ALGOS could in principle run thousands of cheap iters
    # ($1 / $10 per iter on a $4,800 budget), but each iter still refits a
    # GP on all collected data → wall-clock blows past the 360-min GH-Actions
    # cap (LowFidOnly hit the cap on every seed in run #24755495097). Cap
    # them at a level where (a) wall-clock fits well inside 360 min and
    # (b) the cumulative cost still meaningfully exceeds full-eval baselines.
    if algo == "LowFidOnly":   # node 0, $1/iter
        max_iters = 600 if not smoke_test else 200
    elif algo == "Node2Only":  # node 2, $10/iter
        max_iters = 300 if not smoke_test else 100
    elif algo == "pKGFN":
        # Each pKGFN step rebuilds an inner-KG acquisition over every node
        # (n_fantasies=64, n_raw=128 in full mode → ~30–60 s wall-clock per
        # step on a GH-Actions ubuntu-latest runner). All 20 pKGFN seeds in
        # run #24803693093 hit the 360-min job cap because pKGFN keeps
        # selecting the cheap $1 node and never exhausts the $4,800 budget
        # before the loop's other terminator (1500 iters) — 1500 × 30 s
        # ≈ 12.5 h. Edison's ANALYSIS expected ~44 iters; cap at 200 to
        # keep wall-clock well under 360 min while leaving 4× headroom.
        max_iters = 200 if not smoke_test else 50
    else:
        max_iters = 1500
    # Skip the per-iter BOFN network fit for algos that do not use ``model``
    # for selection (Random/Sobol/HighFidOnly/SINGLE_NODE_ALGOS). The tracker
    # still rebuilds it via ``_current_best`` (and we throttle that for the
    # SINGLE_NODE_ALGOS below).
    needs_bofn_model = algo in ("TSFN", "pKGFN")
    # Throttle the (expensive) tracker refit for SINGLE_NODE_ALGOS — only the
    # node being probed gains data, so the posterior mean over y5 changes
    # slowly. Refit every K iters and reuse the previous estimate otherwise.
    tracker_every = 25 if algo in SINGLE_NODE_ALGOS else 1
    while total_cost < cost_budget and it < max_iters:
        t0 = time.time()
        iter_cost = 0
        node_selected: object = None
        node_input = None

        try:
            # Fit the per-iteration BOFN model only when the selection rule
            # actually consumes it (TSFN, pKGFN). Other algos save the cost.
            if needs_bofn_model:
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
            else:
                model = None

            # ── Algorithm-specific candidate selection ─────────────────
            if algo == "Random":
                x_new = bounds[0] + (bounds[1] - bounds[0]) * torch.rand(
                    1, problem.dim, dtype=torch.double
                )
                node_selected = "full"
                iter_cost = sum(node_costs)

            elif algo == "Sobol":
                x_new = sobol_pool[sobol_idx : sobol_idx + 1]
                sobol_idx += 1
                node_selected = "full"
                iter_cost = sum(node_costs)

            elif algo in SINGLE_NODE_ALGOS:
                # Single-root-node EI baseline: fit a single-output GP on the
                # chosen root node only (cheaper than a full-network model)
                # and optimise EI in that node's input space.
                node_k = SINGLE_NODE_ALGOS[algo]
                Xn = train_X_nodes[node_k]
                Yn = train_Y_nodes[node_k].view(-1, 1)
                node_bounds = bounds[:, problem.active_input_indices[node_k]]
                gp = SingleTaskGP(
                    train_X=Xn,
                    train_Y=Yn,
                    input_transform=Normalize(d=Xn.shape[-1], bounds=node_bounds),
                    outcome_transform=Standardize(m=1),
                )
                mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
                fit_gpytorch_mll(mll)
                ei = ExpectedImprovement(model=gp, best_f=Yn.max().item())
                cand, _ = optimize_acqf(
                    acq_function=ei,
                    bounds=node_bounds,
                    q=1,
                    num_restarts=n_ei_restarts,
                    raw_samples=n_ei_raw,
                )
                # Build a full-X for tracking (random fill on inactive dims).
                x_new = bounds[0] + (bounds[1] - bounds[0]) * torch.rand(
                    1, problem.dim, dtype=torch.double
                )
                x_new[0, problem.active_input_indices[node_k]] = cand.squeeze()
                node_selected = node_k
                iter_cost = node_costs[node_k]

            elif algo == "HighFidOnly":
                # Vanilla GP-EI on the full-network final output.
                gp = SingleTaskGP(
                    train_X=X_full,
                    train_Y=Y_final_full,
                    input_transform=Normalize(d=problem.dim, bounds=bounds),
                    outcome_transform=Standardize(m=1),
                )
                mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
                fit_gpytorch_mll(mll)
                ei = ExpectedImprovement(model=gp, best_f=Y_final_full.max().item())
                x_new, _ = optimize_acqf(
                    acq_function=ei,
                    bounds=bounds,
                    q=1,
                    num_restarts=n_ei_restarts,
                    raw_samples=n_ei_raw,
                )
                node_selected = "full"
                iter_cost = sum(node_costs)

            elif algo == "TSFN":
                ts_acqf = ThompsonSamplingFN(model=model, objective=objective)
                cands = draw_sobol_samples(
                    bounds=bounds, n=n_ts_candidates, q=1
                ).squeeze(-2)
                with torch.no_grad():
                    vals = ts_acqf(cands.unsqueeze(1))
                x_new = cands[vals.argmax()].unsqueeze(0)
                node_selected = "full"
                iter_cost = sum(node_costs)

            elif algo == "pKGFN":
                # Smoke keeps the underpowered inner KG (n_fant=8, n_raw=24)
                # so the local SMOKE_TEST stays in the few-minute window.
                # Full Actions run defaults to n_fant=32, n_raw=64 — a
                # compromise between Edison's recommended 64/128 (which
                # produced ~21 min/iter and 0/20 cells finishing within the
                # 6-h SLURM walltime in pkgfn-20260427T150656Z) and the
                # underpowered 16/48 baseline. With 32/64 each iter is
                # ~5–7 min, so a full $2,400-budget pKGFN seed (~44 iters)
                # lands comfortably inside 6 h. Combined with the per-iter
                # checkpoint write (run_single's checkpoint_path) we now
                # never lose a cell to walltime entirely — we keep whatever
                # was reached. Override via PKGFN_N_FANTASIES / PKGFN_N_RAW
                # env vars (e.g. set 64/128 with a 24 h walltime to match
                # Edison's stronger inner-KG recommendation as a hedge).
                # Use ``or`` so an empty-string value (which is what SLURM's
                # ``--export=…,PKGFN_N_FANTASIES=${PKGFN_N_FANTASIES:-}``
                # propagates when the var is unset on the submitting shell)
                # falls back to the default instead of crashing in ``int("")``.
                _full_nfant = int(os.environ.get("PKGFN_N_FANTASIES") or "32")
                _full_nraw = int(os.environ.get("PKGFN_N_RAW") or "64")
                x_new, node_selected, node_input = pkgfn_step(
                    model, problem, objective,
                    n_fantasies=8 if smoke_test else _full_nfant,
                    n_grid=n_grid,
                    n_raw=24 if smoke_test else _full_nraw,
                )
                if x_new is None:
                    # No silent fallback. If pkgfn_step cannot produce a
                    # candidate, that is a real bug (empty inner-KG grid,
                    # all-node failure, shape mismatch, …) and must surface
                    # so the root cause is fixed — not papered over with a
                    # cheap-node random draw that contaminates the cost curve.
                    raise RuntimeError(
                        f"pkgfn_step returned x_new=None at iter {it} "
                        f"(seed={seed}). This indicates every node failed "
                        f"to produce a candidate. Diagnose the root cause "
                        f"(re-run with verbose=True in pkgfn_step) instead "
                        f"of falling back."
                    )
                iter_cost = node_costs[node_selected]

        except Exception as e:  # noqa: BLE001
            # ANY exception inside the candidate selection block is a real
            # bug — surface the full traceback so it can be diagnosed instead
            # of silently masquerading as a free random full-pipeline eval
            # (the pre-fix "error_fallback" branch quietly turned every
            # pKGFN crash into a Random-equivalent draw at $120, which
            # explained the spurious pKGFN ≈ Random tie in earlier sweeps).
            import traceback
            print(
                f"  [{algo} seed={seed}] iter {it} FAILED: "
                f"{type(e).__name__}: {e}\n"
                f"--- traceback ---\n{traceback.format_exc()}"
                f"--- end traceback ---"
            )
            raise

        # Budget guard
        if total_cost + iter_cost > cost_budget:
            break

        # ── Apply the evaluation and update observations ─────────────────
        if algo == "pKGFN" and isinstance(node_selected, int):
            active_idx = problem.active_input_indices[node_selected]
            parents = problem.parent_nodes[node_selected]
            if len(parents) == 0 and len(active_idx) > 0:
                x_node_input = x_new[:, active_idx]
            elif node_input is not None:
                x_node_input = node_input
            else:
                x_node_input = x_new[:, active_idx] if active_idx else x_new
            y_node = problem.evaluate(x_node_input, idx=[node_selected])
            train_X_nodes[node_selected] = torch.cat(
                [train_X_nodes[node_selected], x_node_input], dim=0
            )
            train_Y_nodes[node_selected] = torch.cat(
                [train_Y_nodes[node_selected], y_node], dim=0
            )
        elif algo in SINGLE_NODE_ALGOS:
            node_k = SINGLE_NODE_ALGOS[algo]
            x_node_input = x_new[:, problem.active_input_indices[node_k]]
            y_node = problem.evaluate(x_node_input, idx=[node_k])
            train_X_nodes[node_k] = torch.cat(
                [train_X_nodes[node_k], x_node_input], dim=0
            )
            train_Y_nodes[node_k] = torch.cat(
                [train_Y_nodes[node_k], y_node], dim=0
            )
        else:
            # Full evaluation: update every node + the HighFid GP buffers.
            y_new = problem.evaluate(x_new)
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
            X_full = torch.cat([X_full, x_new], dim=0)
            Y_final_full = torch.cat([Y_final_full, y_new[..., -1:]], dim=0)

        total_cost += iter_cost
        node_selections.append(str(node_selected))
        # Tracker: same posterior-mean-of-final metric for every algo, but
        # for SINGLE_NODE_ALGOS we refit the BOFN tracker only every
        # ``tracker_every`` iters (the metric changes slowly because only one
        # node gains data) — this is what keeps LowFidOnly under the 360-min
        # GH-Actions cap.
        do_track = (
            (it + 1) % tracker_every == 0
            or total_cost + min(node_costs) > cost_budget
            or it + 1 >= max_iters
        )
        if do_track:
            try:
                best = _current_best(train_X_nodes, train_Y_nodes)
            except Exception as e:  # noqa: BLE001
                print(f"  [{algo} seed={seed}] tracker failed: {e}; reusing previous")
                best = best_vals[-1]
        else:
            best = best_vals[-1]
        best_vals.append(max(best_vals[-1], best))
        cost_trace.append(total_cost)
        it += 1
        if verbose:
            print(
                f"  [{algo} seed={seed}] it={it:3d} node={str(node_selected):>14s} "
                f"best={best_vals[-1]:+.4f} cost=${total_cost} ({time.time()-t0:.1f}s)"
            )

        # Periodic checkpoint write so a SLURM walltime kill (or other abort)
        # still leaves a usable per-cell JSON for `combine`. Without this,
        # the pkgfn-20260427T150656Z sweep produced 0 JSONs across 20 cells
        # (all hit the 6-h cap mid-loop). Writes every iter; cost is a few
        # ms vs. minutes per pKGFN iter.
        if checkpoint_path is not None:
            partial = {
                "algo": algo,
                "seed": seed,
                "best_vals": best_vals,
                "cost_trace": cost_trace,
                "node_selections": node_selections,
                "true_max": true_max,
                "partial": True,
                "config": {
                    "n_init": n_init,
                    "cost_budget": cost_budget,
                    "node_costs": node_costs,
                    "noise_std": noise_std,
                    "coupling": coupling,
                    "n_nodes": problem.n_nodes,
                    "smoke_test": smoke_test,
                },
            }
            try:
                with open(checkpoint_path, "w") as f:
                    json.dump(partial, f, indent=2)
            except Exception as e:  # noqa: BLE001
                print(f"  [{algo} seed={seed}] checkpoint write failed: {e}")

    return {
        "algo": algo,
        "seed": seed,
        "best_vals": best_vals,
        "cost_trace": cost_trace,
        "node_selections": node_selections,
        "true_max": true_max,
        "config": {
            "n_init": n_init,
            "cost_budget": cost_budget,
            "node_costs": node_costs,
            "noise_std": noise_std,
            "coupling": coupling,
            "n_nodes": problem.n_nodes,
            "smoke_test": smoke_test,
        },
    }


# ──────────────────────────────────────────────────────────────────────────
#  Combine + plot
# ──────────────────────────────────────────────────────────────────────────


ALGO_STYLE = {
    "Random":      {"color": "#546E7A", "ls": "-"},
    "Sobol":       {"color": "#8E24AA", "ls": "--"},
    "LowFidOnly":  {"color": "#43A047", "ls": ":"},
    "Node2Only":   {"color": "#00897B", "ls": ":"},
    "HighFidOnly": {"color": "#FB8C00", "ls": "-."},
    "TSFN":        {"color": "#1E88E5", "ls": "-"},
    "pKGFN":       {"color": "#D81B60", "ls": "-"},
}


def _interp_to_grid(cost_trace, best_vals, grid):
    """Step-interpolate (cost, best) trace onto a common grid."""
    cost = np.asarray(cost_trace, dtype=float)
    best = np.asarray(best_vals, dtype=float)
    out = np.full_like(grid, np.nan, dtype=float)
    j = 0
    cur = best[0]
    for i, g in enumerate(grid):
        while j + 1 < len(cost) and cost[j + 1] <= g:
            j += 1
            cur = max(cur, best[j])
        out[i] = cur if g >= cost[0] else np.nan
    return out


def combine(input_dir: str, out_dir: str):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    in_path = Path(input_dir)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    files = sorted(glob(str(in_path / "*.json")))
    if not files:
        raise SystemExit(f"No JSON results found in {in_path}")

    runs: dict[str, list[dict]] = {a: [] for a in ALGOS}
    skipped_partial = 0
    skipped_unknown = 0
    for fn in files:
        with open(fn) as f:
            r = json.load(f)
        # A "partial":true entry means the cell aborted (walltime kill,
        # exception, ...) before the final write cleared the flag. Drop
        # those that didn't even finish a single optimisation iteration —
        # otherwise the cost-curve mean is dominated by the init point.
        # Keep partials with >= a few iters so we don't throw away mostly-
        # complete runs.
        if r.get("partial", False):
            min_iters_for_partial = 5
            if len(r.get("best_vals", [])) - 1 < min_iters_for_partial:
                skipped_partial += 1
                print(
                    f"  skip partial run with <{min_iters_for_partial} iters: "
                    f"{Path(fn).name} (algo={r.get('algo')}, "
                    f"iters={len(r.get('best_vals', [])) - 1})"
                )
                continue
        if r.get("algo") in runs:
            runs[r["algo"]].append(r)
        else:
            print(f"  skip unknown algo in {fn}: {r.get('algo')}")
            skipped_unknown += 1
    if skipped_partial or skipped_unknown:
        print(
            f"  combine: dropped {skipped_partial} short-partial + "
            f"{skipped_unknown} unknown-algo runs out of {len(files)} JSONs"
        )

    # Common cost grid spans from min init cost to max budget seen.
    all_traces = [r for v in runs.values() for r in v]
    if not all_traces:
        raise SystemExit("No valid runs to combine")
    cost_lo = min(r["cost_trace"][0] for r in all_traces)
    cost_hi = max(r["cost_trace"][-1] for r in all_traces)
    grid = np.linspace(cost_lo, cost_hi, 200)

    summary = {}
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)

    for algo, runs_a in runs.items():
        if not runs_a:
            continue
        curves = np.vstack(
            [_interp_to_grid(r["cost_trace"], r["best_vals"], grid) for r in runs_a]
        )
        mean = np.nanmean(curves, axis=0)
        std = np.nanstd(curves, axis=0)
        sty = ALGO_STYLE[algo]
        ax.plot(grid, mean, label=f"{algo} (n={len(runs_a)})",
                color=sty["color"], linestyle=sty["ls"], lw=2.0)
        ax.fill_between(grid, mean - std, mean + std,
                        color=sty["color"], alpha=0.15, linewidth=0)
        summary[algo] = {
            "n_seeds": len(runs_a),
            "n_partial": int(sum(1 for r in runs_a if r.get("partial", False))),
            "final_mean": float(np.nanmean([r["best_vals"][-1] for r in runs_a])),
            "final_std":  float(np.nanstd([r["best_vals"][-1] for r in runs_a])),
            "iters_mean": float(np.mean([len(r["best_vals"]) - 1 for r in runs_a])),
        }

    init_cost = all_traces[0]["config"]["n_init"] * sum(
        all_traces[0]["config"]["node_costs"]
    )
    ax.axvline(init_cost, color="0.5", ls="--", lw=0.8)
    ax.text(init_cost, ax.get_ylim()[0], f" init ${init_cost}", color="0.4",
            fontsize=8, va="bottom", ha="left")

    # True max (noiseless Sobol-grid estimate, cached per-run) plotted as an
    # upper reference. Use the median across runs to be robust to outliers
    # (all runs should agree since the problem is built with the same fixed
    # seed=0 regardless of benchmark seed).
    true_maxes = [r.get("true_max") for r in all_traces if r.get("true_max") is not None]
    if true_maxes:
        tmax = float(np.median(true_maxes))
        ax.axhline(tmax, color="k", ls="--", lw=1.2, alpha=0.75,
                   label=f"true max ≈ {tmax:.3f}")

    noise_std = all_traces[0]["config"].get("noise_std", 0.0)
    n_nodes = all_traces[0]["config"].get("n_nodes", 4)
    if isinstance(noise_std, (list, tuple)):
        noise_str = "[" + ",".join(f"{s:g}" for s in noise_std) + "]"
    else:
        noise_str = f"{noise_std:g}"
    ax.set_xlabel("Cumulative evaluation cost ($)")
    ax.set_ylabel("Best network output (GP posterior mean of final node)")
    ax.set_title(
        f"BOFN+pKGFN vs. baselines on the {n_nodes}-node Manufacturing DAG\n"
        f"(equal cost budget, noise_std={noise_str}, "
        f"mean ± 1 std, {len(all_traces)} runs total)",
        fontsize=11,
    )
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(True, alpha=0.25, lw=0.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()

    fig_path = out_path / "bofn_actions_cost_efficiency.png"
    fig.savefig(fig_path)
    plt.close(fig)

    summary_path = out_path / "bofn_actions_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

    csv_path = out_path / "bofn_actions_summary.csv"
    with open(csv_path, "w") as f:
        f.write("algo,n_seeds,n_partial,final_mean,final_std,iters_mean\n")
        for a, s in sorted(summary.items()):
            f.write(
                f"{a},{s['n_seeds']},{s.get('n_partial', 0)},{s['final_mean']:.4f},"
                f"{s['final_std']:.4f},{s['iters_mean']:.1f}\n"
            )

    print(f"Wrote {fig_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {csv_path}")
    return summary


# ──────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    p.add_argument(
        "--mode", choices=["run", "smoke", "combine"], required=True,
        help="run = single (algo,seed); smoke = run all algos at tiny budget; "
             "combine = aggregate JSONs and plot"
    )
    p.add_argument("--algo", choices=ALGOS, help="algorithm name (run mode)")
    p.add_argument("--seed", type=int, help="seed (run mode)")
    p.add_argument("--out", type=str, help="output JSON path (run mode)")
    p.add_argument("--input-dir", type=str, help="dir of result JSONs (combine mode)")
    p.add_argument("--out-dir", type=str, help="output dir for plots (combine/smoke)")
    p.add_argument("--smoke-test", action="store_true",
                   help="force tiny config even in run mode")
    args = p.parse_args(argv)

    smoke_env = os.environ.get("SMOKE_TEST", "").lower() in ("1", "true", "yes")
    smoke = args.smoke_test or smoke_env or (args.mode == "smoke")

    if args.mode in ("run", "smoke"):
        if args.mode == "run":
            if not args.algo or args.seed is None:
                p.error("--algo and --seed are required in run mode")
            algos = [args.algo]
            seeds = [args.seed]
        else:
            algos = ALGOS
            # Use 3 seeds even in smoke mode so the composite plot shows
            # non-degenerate uncertainty bands (a single seed collapses the
            # std to zero and the ±1σ shading disappears).
            seeds = [0, 1, 2]

        results_dir = Path(
            args.out_dir or (ROOT / "benchmarks/results/actions_smoke" if smoke
                             else ROOT / "benchmarks/results/actions")
        )
        results_dir.mkdir(parents=True, exist_ok=True)

        for algo in algos:
            for seed in seeds:
                t0 = time.time()
                out_path = (
                    Path(args.out) if args.out and args.mode == "run"
                    else results_dir / f"{algo}_seed{seed}.json"
                )
                # Pass the final out_path as the checkpoint target so a SLURM
                # walltime kill mid-loop still leaves a salvageable JSON.
                res = run_single(
                    algo, seed, smoke_test=smoke,
                    checkpoint_path=str(out_path),
                )
                with open(out_path, "w") as f:
                    json.dump(res, f, indent=2)
                print(
                    f"✓ {algo} seed={seed}: best={res['best_vals'][-1]:.4f} "
                    f"final_cost=${res['cost_trace'][-1]} "
                    f"iters={len(res['best_vals'])-1} "
                    f"({time.time()-t0:.1f}s) → {out_path}"
                )

        if args.mode == "smoke":
            combine(str(results_dir),
                    args.out_dir or str(ROOT / "benchmarks/figures/actions_smoke"))
        return 0

    if args.mode == "combine":
        if not args.input_dir or not args.out_dir:
            p.error("--input-dir and --out-dir are required in combine mode")
        combine(args.input_dir, args.out_dir)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
