# Spot-check: our pKGFN port vs. `vertical-cloud-lab/partial_kgfn` PR #2

**Reference**: <https://github.com/vertical-cloud-lab/partial_kgfn/pull/2>
**Upstream baseline**: `partial_kgfn/main` @ `a5996011` (Buathong et al. 2024 paper-faithful reproduction; the PR layers a benchmark workflow + DAG visualizer on top, but does *not* substantially modify the core acquisition or GP-network code — that code is the paper's reference impl).

**Our port**: `benchmarks/partial_kgfn/{partial_kgfn,gp_network,thompson_sampling}.py` and the drivers `benchmarks/bofn_pkgfn_demo.py` + `benchmarks/bofn_actions_benchmark.py`.

This document is the result of two manual passes through both code-bases. The DAG used here (the 6-node `ExtendedManufacturingGPNetwork`) is intentionally different from any of the seven test networks in the paper, so DAG-level mismatches are expected; only **algorithmic and API-level** mismatches are flagged below.

---

## Pass 1 — `PartialKnowledgeGradientFN.forward()`

| # | Aspect | Upstream `acquisition/partial_kgfn.py` | Our `partial_kgfn/partial_kgfn.py` | Severity |
|---|---|---|---|---|
| 1.1 | **Vectorised fantasy** | `fantasy_model = self.model.fantasize(X=[X]*sum(mask), samplers=self.sampler, observation_noise=True, evaluation_mask=mask)` — single batched call producing a `n_f × b` fantasy model. | Loops `for i in range(b): for f in range(num_fantasies): condition_on_observations(...)` — `b·num_fantasies` separate fantasy networks, no batching. | **High** (perf + numerical path divergence) |
| 1.2 | **Inner posterior eval** | `fantasy_post_at_X = fantasy_model.posterior(self.X_fantasies_candidates)` — one batched call, shape `n_f × b × n_grid × n_nodes`. | Per-fantasy `_network_posterior_mean(fantasy_model, X_fantasies_candidates, sampler=...)` — `b·num_fantasies` separate calls. | **High** (same as 1.1) |
| 1.3 | **`inner_sampler` arg honoured?** | YES — `values = self.inner_sampler(fantasy_post_at_X)` (size 64 or 128). | NO — `self.inner_sampler` is stored on `__init__` but **never used** in `forward()`; a fresh `SobolQMCNormalSampler(n_saa=64, seed=12345)` is constructed inside `forward()` instead. | **Medium** (silent API-arg drop; passing `inner_sampler=…` from the driver is a no-op) |
| 1.4 | **observation_noise on fantasy obs** | Passed via `model.fantasize(observation_noise=True, …)` — but upstream `fantasize()` itself silently ignores it (`TODO: deal with kwargs`), so noiseless fantasies are drawn in practice. | Explicit `self.model.node_GPs[k].posterior(x_i, observation_noise=True)` then sample → noisy fantasies are drawn. | Note (we are stricter than upstream, intentionally) |
| 1.5 | **Reduction order** | `inner_sampler(fantasy_post)` → `mean(dim=0)` (SAA) → `objective` or `[..., -1]` → `max(dim=-1)` (over grid) → `mean(dim=0)` (over fantasies). | `_network_posterior_mean` already returns the SAA mean of the final node; then per-fantasy `.max()` over grid; then average across fantasies in a Python list. Same mathematical outcome but no shared base samples across the (candidate × fantasy) loop. | Note |
| 1.6 | **t-batch decorator** | `@t_batch_mode_transform()` (no `assert_output_shape`). | Same. | OK |
| 1.7 | **`use_posterior_mean` flag** | Stored, drives the inner reduction (`values[..., -1]` vs `objective`). | Stored, never read in `forward()`. | Minor (we always go through `_network_posterior_mean`) |
| 1.8 | **`current_value`** | Subtracted at the end → KG. | Same. | OK |
| 1.9 | **`X_fantasies_candidates` default** | `draw_sobol_samples(bounds, n=50*d, q=1).squeeze(-2)` if not provided. | Same. | OK (but see 2.1 — the *driver* never lets this default fire) |

**Net effect of pass 1**: math is comparable but the implementation paths diverge sharply. Most importantly:
- **1.3 (silent drop of `inner_sampler`)** is a real bug — our driver believes it can tune the inner SAA budget via `inner_sampler=…`; that argument is dead code.
- **1.1 / 1.2 (loop vs batched)** explain the wall-time gap and may also explain why we needed `n_fantasies=64` to feel stable: each fantasy sees fresh randomness because we re-`condition_on_observations` per-fantasy rather than reusing one batched fantasy posterior.

---

## Pass 2 — `pkgfn_step` driver vs upstream's `run_one_trial.py` `elif algo == "pKGFN"` block

| # | Aspect | Upstream (`run_one_trial.py:701-778`) | Our `bofn_pkgfn_demo.py:202-331` | Severity |
|---|---|---|---|---|
| 2.1 | **`X_fantasies_candidates` set** | `cat( generate_X_fantasies_candidates_TS(no_points=10, model=model, problem, objective), generate_X_fantasies_candidates_RaLo(radius=0.2, no_random=0, no_local=10, problem, best_design, include_best=True) )` → ~21 candidates *anchored on the current incumbent* (10 TS-optima + 10 local Gaussian perturbations of `best_design` + the incumbent itself). | `draw_sobol_samples(bounds, n=n_grid=200, q=1)` — 200 *global* Sobol points, **not anchored on the incumbent**. | **High** (inner KG `argmax` over a candidate set that doesn't include the current best is biased upward, and lacks the local-refinement points that drive most of the KG signal) |
| 2.2 | **`num_fantasies`** | `8` (hard-coded for pKGFN at line 749). | `64` default in `pkgfn_step`; `int(os.environ.get("PKGFN_N_FANTASIES") or "32")` in `bofn_actions_benchmark.py`. | Medium (8× over-sampling vs paper) |
| 2.3 | **`inner_sampler`** | `SobolQMCNormalSampler(torch.Size([64]))` passed in. | Not passed (would be a no-op anyway, see 1.3). | Medium (paired with 1.3) |
| 2.4 | **Acquisition optimiser** | `optimize_discrete_acqf_for_function_network(acq_function, bounds, parent_bounds, num_restarts=10*d, raw_samples=100*d, impose_assump=…)` — proper restart-and-local-optimise with parent-bounds awareness and the optional upstream-downstream restriction. | `acq_vals = pkgfn(raw_cands.unsqueeze(1)); best = raw_cands[argmax]` — single-shot evaluation of `n_raw=128` candidates from `_reachable_parent_samples`, *no continuous-space refinement*. | **High** (upstream literally L-BFGS-refines after the discrete pass; we don't) |
| 2.5 | **`impose_assump` (upstream-downstream)** | Configurable; default `True` in the paper experiments — only allows fantasizing at child node *k* if every parent of *k* has been observed at the same input. | Not implemented. | Medium (if set, would prevent some of the "node 4 picked while parent y3 has never been observed at this composition" cases we see in our histograms) |
| 2.6 | **`current_value` / `best_post_mean`** | `best_post_mean` from upstream's `posterior_mean_function` continuous-optimised over `problem.bounds` (multi-restart L-BFGS). | `current_value = compute_posterior_mean_network(model, X_grid=200 Sobol, objective).max()` — discrete max over 200 Sobol points only. | Low–Medium (200-Sobol max is biased low → KG values inflated by a constant offset, but offset cancels out in the per-node ranking) |
| 2.7 | **Cost normalisation** | `node_best_acq_vals.append(acqf_val / eval_cost)` where `eval_cost = sum(problem.node_costs[k] for k in j)` (sum across node group). | `cost_adjusted = acq_val / problem.node_costs[k]` (cost of the group leader only). | OK in our case (all our `node_groups` are singletons) |
| 2.8 | **Budget guard** | If `remaining_budget < eval_cost` → set `acqf_val = -inf` so the node is never selected. | No equivalent guard; we always pay the cost in the outer loop after `pkgfn_step` returns. | Low (last-iter could over-spend by one node-cost; our outer loop has its own budget check) |
| 2.9 | **Node iteration** | `for j in model.node_groups` (groups, not nodes). | `for node_group in problem.node_groups: k = node_group[0]` — operates on first member of each group only. | Same effect with singleton groups; would be wrong with multi-node groups. |
| 2.10 | **Skipping degree-of-freedom-free nodes** | Upstream still considers them (sets `acqf_val = -inf`). | Skips with `if not has_active and not has_parents: continue`. | OK (semantically same — `argmax` would pick the same node) |

**Net effect of pass 2**: items **2.1 and 2.4** are the structurally largest mismatches. Together they mean the *inner* KG argmax is driven by a candidate set that:
- doesn't contain the incumbent or its neighbourhood (2.1), AND
- isn't refined in continuous space afterwards (2.4).

This is consistent with our empirical observation that pKGFN is currently *tied with* — but does not beat — TSFN/HighFidOnly on the 6-node DAG, even after the noFb2/A1–A3 fixes eliminated the 100% `error_fallback` regime.

---

## Pass 3 — `GaussianProcessNetwork` and `MultivariateNormalNetwork`

| # | Aspect | Upstream `models/decoupled_gp_network.py` | Our `partial_kgfn/gp_network.py` | Severity |
|---|---|---|---|---|
| 3.1 | **`fantasize()` `observation_noise`** | Accepted via `**kwargs` then **silently ignored** (TODO comment). Drawn fantasies are noiseless. | `fantasize()` doesn't accept `observation_noise` either; per-node `posterior()` call is noiseless inside `fantasize()`. We instead inject noise in `partial_kgfn.forward()` via `node_GPs[k].posterior(x_i, observation_noise=True)`. | OK (we are *more* faithful to the paper math than upstream's own code) |
| 3.2 | **Per-node `Normalize` bounds** | Uses `Normalize(d=…)` without bounds (BoTorch infers from train_X). | Optional `node_input_bounds: list[Tensor]` threads into `Normalize(d=…, bounds=…)` for non-stationary lengthscale stability — added in our A3 fix. | Note (intentional improvement over upstream) |
| 3.3 | **`Standardize` outcome** | Used. | Used. | OK |
| 3.4 | **`MultivariateNormalNetwork.rsample`** | Joint sample by reparameterised propagation through the DAG. | Same. | OK |
| 3.5 | **DAG topo walk** | Iterative `while not all(available)` — handles arbitrary DAGs. | Same. | OK |
| 3.6 | **`condition_on_observations` shape dance** | Uses upstream's `_dummy` posterior call to stash input-transform state, then passes raw `X`. | Same idiom + our explicit `_dummy` warm-up. | OK |

---

## Pass 4 — `ThompsonSamplingFN`

| # | Aspect | Upstream `acquisition/tsfn.py` | Our `partial_kgfn/thompson_sampling.py` | Severity |
|---|---|---|---|---|
| 4.1 | **GP-sample backend** | `botorch.utils.gp_sampling.get_gp_samples` (legacy decoupled draws). | `botorch.sampling.pathwise.get_matheron_path_model` (Matheron pathwise — required by BoTorch ≥0.13). | OK (necessary modernisation) |
| 4.2 | **Forward pass** | Identical structure (root nodes first; topological while-loop). | Same. | OK |
| 4.3 | **Objective fallback** | Always passes through `self.objective(nodes_samples)`. | Same, with explicit `else: output = nodes_samples[..., -1]` if `objective is None`. | OK (defensive) |

TSFN is essentially a faithful port modulo the BoTorch-version-driven backend swap.

---

## Pass 5 — anything else that materially changes behaviour?

| # | Aspect | Upstream | Ours | Severity |
|---|---|---|---|---|
| 5.1 | **Init design size** | Per-experiment (e.g. `2*d` for AckleyS — table in paper SM). | `n_init=9` Sobol full-pipeline evals (≈ `2*(d=4)+1`). | OK |
| 5.2 | **Best-tracker (reported "best")** | `best_post_mean` — argmax of posterior mean over a continuous-optimised grid. | Same idea, but argmax over 200 Sobol points only (not L-BFGS refined). | Low |
| 5.3 | **Noise model** | Per-experiment `noisy=True/False`; when `True`, `noise_std` is per-node. | `noise_std = [0.02, 0.02, 0.02, 0.05, 0.07, 0.10]` (heteroscedastic by node). | Note (intentional, tuned to make the cheap-probe regime where pKGFN should win realistic) |
| 5.4 | **Cost grid** | Paper Table 1 splits (e.g. AckleyS `1,49`, Manufacturing `1,9,1,40`). | `[5, 10, 10, 45, 20, 30]`. | OK (custom DAG) |
| 5.5 | **Random/Sobol baseline cost** | Counts `sum(problem.node_costs)` per evaluation. | Same. | OK |
| 5.6 | **Combined-results filter** | N/A in upstream. | We added `n_partial` and skip-< 5-iter filter in our combine step. | OK |

---

## Recommendations (priority order)

These are the changes I'd most recommend Edison sanity-check before we re-spin another ORC sweep. Numbered to match the inconsistency IDs above.

1. **Fix 1.3 — actually use `inner_sampler` in `forward()`.** One-line change: replace the inline `SobolQMCNormalSampler(...)` construction with `self.inner_sampler if self.inner_sampler is not None else <default>`. Without this, every `inner_sampler=…` argument from the driver is dropped silently — which means our entire "tune inner SAA via `PKGFN_INNER_SAA`" lever has been a no-op since the CRN fix landed.
2. **Fix 2.1 — anchor `X_fantasies_candidates` on the incumbent.** Implement upstream's `generate_X_fantasies_candidates_RaLo` (10 local Gaussian perturbations of `best_design` + the incumbent itself) plus optionally `generate_X_fantasies_candidates_TS` (10 TS-optima). 21 anchored points should outperform 200 unanchored Sobol points for the inner argmax.
3. **Fix 2.2 — drop `num_fantasies` to 8** (paper default) once 2.1 is fixed. The 8× over-sampling we currently do is a wall-time tax we may not need; the upstream ratio of `n_fant=8 / inner_sampler=64` is the calibrated paper choice.
4. **Fix 2.4 — refine candidates after the discrete pass.** Even one round of `optimize_acqf` restarts seeded from the top-k discrete candidates (not the full upstream `optimize_discrete_acqf_for_function_network` machinery) would close most of the remaining gap.
5. **Defer 1.1 / 1.2 (vectorised fantasize)** unless wall-time becomes a blocker. The behaviour is mathematically equivalent up to MC noise; recovering upstream's batched code path is a substantial refactor of `forward()`.
6. **Defer 2.5 (`impose_assump`)** until we have first-pass evidence the other fixes leave us under-performing. The 6-node DAG has shallow connectivity so this restriction is unlikely to bite.

The Edison query in `submit_pr2_spotcheck.py` asks Edison to:
- Independently regenerate this list against the upstream PR #2 diff and our `partial_kgfn/*.py` files.
- Score each item as **confirmed / partially-confirmed / refuted**, citing line numbers in both code-bases.
- Suggest any inconsistency we missed.
- Recommend the smallest set of changes likely to bring our `pkgfn-noFb2` curve above `TSFN`.

Task ID will be appended to `pending-edison-tasks.json` on submission.
