# spotcheck-q5-harness-fairness

_task_id: 16d341db-a17b-4715-acfc-22343599dd9e; status: success_

I audited `bofn_actions_benchmark.py` against the attached per-seed JSONs and attempted to exercise the code. Short version: the fairness story is mixed, and one result is flat-out broken in the attached artifact.

Findings

- `best_y5` is tracked from a GP-network posterior-mean max over a Sobol grid, not from noisy observations.
  - Evidence: `bofn_actions_benchmark.py:311-326` defines `_current_best`, which fits `GaussianProcessNetwork`, draws a Sobol grid, and returns `compute_posterior_mean_network(...).max()`. `best_vals` is initialized and updated from this tracker at `:327` and `:580-589`.
  - So the seed-to-seed std in `best_vals` is not direct observation-noise contamination from taking maxima of noisy `y5`. Good.
  - But the tracker itself is noisy because it uses a finite Sobol grid and Monte Carlo posterior averaging. In a smoke reconstruction on the shipped code, at fixed model and fixed `n_grid=200`, the tracker max had SAA Monte Carlo std about 0.15 across 20 repeats; across independently scrambled Sobol grids, the max at `n_grid=200` had std about 0.26. That is large enough to materially inflate reported seed stds.

- The 200-point Sobol grid is not converged for this problem.
  - The attached artifact is not `d=4`; the extended benchmark problem has `dim=5` input dimensions. Evidence: `ExtendedManufacturingGPNetwork` sets `self.dim = 5` at `manufacturing_problem.py` in the `ExtendedManufacturingGPNetwork.__init__` block, and `run_single` constructs that class at `bofn_actions_benchmark.py:246-248`.
  - The benchmark uses `n_grid = 200` in full mode at `bofn_actions_benchmark.py:237`.
  - In a small executable smoke setup, using the same tracker logic, the estimated posterior-mean max changed meaningfully with grid size: mean tracker max was about 16.06 at `n_grid=200` and about 16.41 at `n_grid=2000`, with across-grid std still nontrivial. That 0.35 shift is bigger than some inter-algorithm gaps in `bofn_actions_summary.json`.
  - Recommendation: for reporting a “final mean” tracker, use at least 2,000 to 8,192 Sobol points for this 5-D problem, or better, a nested quasi-MC scheme with fixed common random numbers across algorithms and seeds. Best practice here is to separate:
    1. optimization randomness across seeds,
    2. tracker discretization error from finite candidate grids,
    3. tracker Monte Carlo error from posterior sampling.
  - If runtime is a concern, precompute a large fixed Sobol design once and reuse it for all tracker evaluations. That removes one big variance source.

- `error_fallback` is not 0% in the attached JSONs. It is 100% for pKGFN.
  - I grepped all 140 per-seed JSONs by parsing `node_selections`.
  - Counts from the attached artifact:
    - Random: 0 / 220 fallback iterations
    - Sobol: 0 / 220
    - LowFidOnly: 0 / 5280
    - Node2Only: 0 / 2640
    - HighFidOnly: 0 / 220
    - TSFN: 0 / 220
    - pKGFN: 220 / 220 = 100%
  - Every one of the 20 `pKGFN_seed*.json` files has 11/11 `node_selections == "error_fallback"`.
  - Worse, `pKGFN`’s final results are exactly identical to `Random` for all 20 seeds. Same per-seed final values, same traces. This follows from the exception handler at `bofn_actions_benchmark.py:508-517`, which falls back to a random full evaluation.
  - So the attached pKGFN summary is not a pKGFN result. It is Random in disguise.

- Init-point sharing is fair and paired across algorithms.
  - Evidence in code: initial design is drawn once per run with `draw_sobol_samples(..., seed=seed)` at `bofn_actions_benchmark.py:287`, before branching by algorithm. Since each `(algo, seed)` run uses the same benchmark seed, all 7 algorithms get the same 9 Sobol init points for a given seed.
  - Evidence in data: all 7 algorithms have identical initial tracker distribution in the attached JSONs, with init mean about 16.928 and init std about 0.533 across 20 seeds.
  - So paired CRN for the initial design is present.

- Partial-run handling is unsafe in `combine`, though there are no `partial:true` files in the attached artifact.
  - Checkpointing writes `partial: True` every iteration at `bofn_actions_benchmark.py:597-625`.
  - Final clean completion returns a dict without `partial` at `:627-643`, then overwrites the output JSON at `:843-844`.
  - In the attached 140 JSONs, zero files have `partial:true`. So this artifact contains only clean-finish files.
  - But `combine` does not exclude partial runs. It loads every JSON at `:692-697` and includes them in summaries at `:714-729` with no filter on `partial`. If timed-out partial pKGFN files are present in another run, they would be treated as completed runs and bias `final_mean` downward.
  - So I cannot verify your “6 pkgfn-32/64 cells timed out at 24h” claim from this artifact, because no partial files are present here. But the combine code would mishandle them if they were present.

- TSFN / pKGFN optimizer pairing is not matched.
  - TSFN at `bofn_actions_benchmark.py:465-474` evaluates a Thompson sampler on `n_ts_candidates = 2048` full-space Sobol candidates (`:238`, `:467-472`).
  - HighFidOnly / single-node EI use `optimize_acqf` with `num_restarts = 5`, `raw_samples = 256` at `:239-240`, `:429-435`, and `:455-461`.
  - pKGFN uses `pkgfn_step` with default full-mode `n_fantasies = 32`, `n_raw = 64` from env or defaults at `:491-498`. Inside `pkgfn_step`, each node gets a reachable-manifold raw candidate set of size `n_raw`, then uses direct argmax over acquisition values (`bofn_pkgfn_demo.py:281-292`), not the same optimizer settings as EI and not the same candidate count as TSFN.
  - So no, TSFN is not using the same `num_restarts/raw_samples` as pKGFN. The acquisition optimization budgets differ substantially. TSFN gets 2048 candidates in the full design space; pKGFN gets 64 raw candidates per node on node-specific manifolds.

Attempt to exercise the code

- Install step succeeded in this sandbox.
  - Installed/imported versions: `botorch 0.17.2`, `torch 2.10.0`, `gpytorch 1.15.2`.

- I could not run the attached code as-is because the artifact is incomplete.
  - Missing source files referenced by the benchmark stack: `dag.py`, `utils.py`, and `thompson_sampling.py`.
  - Those are imported by the benchmark path:
    - `bofn_actions_benchmark.py:138-142`
    - `bofn_pkgfn_demo.py:47-58`
    - `gp_network.py:28`
    - `manufacturing_problem.py` also depends on `DAG`
  - Because those files are absent from the attached workspace, I cannot verify the exact runtime error that produced the shipped pKGFN fallbacks.

- I then did a constrained smoke exercise by supplying minimal stubs for the missing modules, strictly to test whether the shipped `pkgfn_step` / `partial_kgfn.py` logic basically runs.
  - Tiny setup: `ExtendedManufacturingGPNetwork`, 2 Sobol init points, then 2-3 pKGFN iterations with very small `n_fantasies` and `n_raw`.
  - Result: `pkgfn_step` ran without raising; returned shapes matched expectations (`x_new` shape `(1, 5)`, valid node index, valid `node_input` shape).
  - In one verbose step, all six per-node KG values were non-negative:
    - node 0: +0.02152
    - node 1: +0.01735
    - node 2: +0.00734
    - node 3: +0.01605
    - node 4: +0.01686
    - node 5: +0.01953
  - Cost-adjusted selection picked node 0 in that run.
  - In a 3-iteration smoke loop, the code continued to run and selected valid nodes.
  - This is only a smoke sanity check, not a faithful end-to-end reproduction of the missing-module environment.

Important mismatch with the numbers in your prompt

- The attached artifact does not match your quoted scale.
  - Your prompt says init about 1.026 and true max about 1.297-1.370 depending on seed.
  - The attached JSONs show init mean about 16.928 and `true_max` exactly 18.023 for every seed.
  - That is consistent with the current code, which fixes the problem seed to 0 at `bofn_actions_benchmark.py:243-248`, so `true_max` should not vary by benchmark seed.
  - So either your prompt is referring to an older benchmark version, or the attached files are from a different run/config. I can only audit the files provided.

Bottom line

- `best_y5` is not updated from noisy observations. It is updated from a GP posterior-mean max on a finite Sobol grid.
- That tracker is itself quite noisy at `n_grid=200`, enough to inflate seed std materially.
- The current attached pKGFN results are invalid: all 20 seeds are 100% `error_fallback`, and the reported pKGFN curve is exactly Random.
- Initial designs are paired fairly across algorithms.
- `combine()` would incorrectly include partial timed-out runs if they existed.
- TSFN and pKGFN do not use matched acquisition-optimization budgets.

What I’d fix before trusting any benchmark table

1. Exclude `partial:true` files in `combine()`.
2. Add an explicit `n_error_fallback` field per run and fail the combine step if it is nonzero for any non-baseline method.
3. Replace the 200-point tracker with a fixed shared QMC grid of at least 2,000 points, ideally 8,192 if runtime allows.
4. Report tracker Monte Carlo error separately from seed variance.
5. Do not report the attached pKGFN numbers as pKGFN. They are Random fallback traces.
6. Match acquisition search budgets more closely across TSFN / pKGFN / EI baselines, or at least disclose the asymmetry.

- Discretionary analytical decisions made during the analysis
  - Counted `error_fallback` by parsing `node_selections` in each per-seed JSON rather than relying on summary files, because the summary does not expose fallback counts.
  - Treated the attached JSON artifact as the ground truth for verification, even when its numerical scale conflicted with the user’s prompt, because fabricating reconciliation would be wrong.
  - Used a constrained smoke test with minimal stub modules for missing files solely to exercise the shipped `pkgfn_step` and `partial_kgfn.py` logic after the as-is run proved impossible from the incomplete artifact.
  - Assessed tracker convergence by varying Sobol grid size and repeating with different scrambled Sobol seeds, since the benchmark’s reported metric is a grid maximum rather than an analytic quantity.
  - Quantified tracker Monte Carlo noise at fixed grid by repeated reevaluation of `compute_posterior_mean_network`, because that function uses posterior sampling and therefore adds stochastic error beyond grid discretization.
  - Did not run formal hypothesis tests comparing algorithms, because the attached pKGFN results are invalidated by 100% fallback and because the benchmark summary mixes optimization variability with tracker noise.
  - Interpreted fairness of init-point sharing using both static code inspection and empirical equality of initial `best_vals` distributions across algorithms, to verify paired CRN rather than assuming it from code alone.
