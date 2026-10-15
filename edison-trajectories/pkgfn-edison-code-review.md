
# Grade: C+

## Comprehensive Code Review: p-KGFN Implementation

### Overall Assessment

The implementation demonstrates competent understanding of the p-KGFN framework and function network structure, with correct DAG propagation, cost accounting, and partial evaluation logic. However, a critical bug in the fantasy model conditioning renders the p-KGFN acquisition function unreliable, and a secondary bug wastes the Sobol sampler infrastructure. These issues together explain the observed results where p-KGFN fails to outperform Random.

---

### CONFIRMED BUGS

**Bug #1 [HIGH SEVERITY]: Double Input Normalization in Fantasy Models**
- **Location**: `gp_network.py`, line 123
- **Code**: `fantasy_model = self.node_GPs[k].condition_on_observations(X=self.node_GPs[k].transform_inputs(X[k]), Y=Y[k], noise=Yvar_k)`
- **Problem**: `transform_inputs()` normalizes X[k] via the `Normalize` input transform. Then `condition_on_observations()` (inherited from `GPyTorchModel`) internally calls `transform_inputs()` again on the already-normalized input (verified in BoTorch 0.17.2 source: `GPyTorchModel.condition_on_observations` contains `X = self.transform_inputs(X)`). The conditioning point is therefore **double-normalized**.
- **Empirically verified**: With a manufacturing-like GP (2D, [-1,1], 9 training points), the double normalization causes a **posterior mean error of up to 41.65% of the posterior range** (max absolute error 0.94, mean error 0.16). This is not a subtle numerical issue — it fundamentally corrupts the fantasy model.
- **Impact**: All p-KGFN fantasy models have incorrect posteriors. The KG values computed in `partial_kgfn.py` `forward()` are based on wrong fantasy models, making node/input selection essentially meaningless. This is the primary cause of p-KGFN's failure to outperform Random.
- **Fix**: Remove the explicit `transform_inputs()` call: `fantasy_model = self.node_GPs[k].condition_on_observations(X=X[k], Y=Y[k], noise=Yvar_k)`

**Bug #2 [MODERATE SEVERITY]: Sobol Sampler Created but Never Used**
- **Location**: `partial_kgfn.py`, lines 144-147 (creation) vs. lines 227-230 (usage)
- **Problem**: `__init__` creates `SobolQMCNormalSampler` objects (line 144-147) and stores them as `self.sampler`, but `forward()` draws fantasy observations via `post_k.rsample()` (line 230) — plain pseudo-random sampling — instead of using the Sobol samplers. Additionally, fantasies are drawn one-at-a-time in a loop (`for f in range(self.num_fantasies)`) rather than batch-sampled.
- **Impact**: The KG estimator has higher variance than intended. With only `num_fantasies=4`, pseudo-random sampling produces noisier estimates than Sobol quasi-random sampling, further degrading acquisition quality.

**Bug #3 [LOW SEVERITY]: Missing `super().__init__()` in GaussianProcessNetwork**
- **Location**: `gp_network.py`, line 49
- **Problem**: `GaussianProcessNetwork` inherits from `botorch.models.model.Model` (which is `torch.nn.Module`) but never calls `super().__init__()`. The Module is not properly initialized. Node GPs are stored as a plain Python list, not `nn.ModuleList`.
- **Impact**: Parameters aren't tracked, `model.to(device)` won't propagate, state dict operations fail. Doesn't affect correctness in current CPU-only usage.

**Bug #4 [LOW SEVERITY]: `self.X` Mutation in `rsample_from_base_samples`**
- **Location**: `gp_network.py`, line 271
- **Code**: `self.X = torch.broadcast_to(self.X, batch_shape + self.X.shape[-2:])`
- **Problem**: Mutates the posterior object's `self.X` in-place. If the posterior is reused with different sample shapes, results would be incorrect. Not triggered in current code.

---

### WHAT IS CORRECTLY IMPLEMENTED

- ✓ **DAG structure** (`dag.py`): Simple, correct representation of the 4-node DAG.
- ✓ **Manufacturing problem** (`manufacturing_problem.py`): GP-sampled functions with proper seeding. `get_matheron_path_model` with `sample_shape=None` is correct for BoTorch 0.17.2. Lengthscale setting on `covar_module.lengthscale` is correct (SingleTaskGP uses RBFKernel directly, no ScaleKernel wrapper in this version).
- ✓ **Thompson sampling** (`thompson_sampling.py`): Correct network propagation, proper handling of empty active_input_indices via `X[..., []]` → `(n, 0)` tensor → correct concatenation.
- ✓ **Observation set construction** (`utils.py`): Correctly builds per-node training data with active inputs and parent outputs.
- ✓ **Posterior mean propagation** (`utils.py`, `partial_kgfn.py`): Correctly propagates means through DAG for non-root nodes with proper broadcasting.
- ✓ **Cost accounting**: Init = 9 × $70 = $630 (correct). Full-eval = $70/iter. pKGFN = $5 or $10/iter depending on node. Budget check (`total_cost + iter_cost > cost_budget`) prevents overshoot.
- ✓ **Partial evaluation data update** (`bofn_pkgfn_demo.py`, lines 308-312): Only the selected node's GP training data is updated — other nodes' GPs stay unchanged. Correct.
- ✓ **Best value tracking** (`bofn_pkgfn_demo.py`, lines 342-357): Uses GP posterior mean over a grid, no information leak from the free full evaluation (which is only used for printing).
- ✓ **Cost-adjusted KG** (`bofn_pkgfn_demo.py`, line 177): `acq_val / node_cost` correctly implements the KG-per-unit-cost formulation.

---

### ANSWERS TO SPECIFIC QUESTIONS

**Q1 (Bugs)**: YES — two significant bugs found. The double normalization (Bug #1, `gp_network.py:123`) corrupts all fantasy models used in p-KGFN. The unused sampler (Bug #2, `partial_kgfn.py:227-230`) adds unnecessary noise to KG estimates.

**Q2 (Partial evaluation correctness)**: The BO loop's partial evaluation update is **correct** — only the selected node's GP data is updated (`bofn_pkgfn_demo.py:308-312`). However, the p-KGFN **acquisition function** that decides *which* node to evaluate uses corrupted fantasy models (Bug #1), so while the data management is correct, the selection mechanism is broken.

**Q3 (Cost accounting)**: **Correct**. Init = 9 × $70 = $630. Then TSFN/Random get $70/iter (8 more iterations to reach $1,190). pKGFN gets $5-$10/iter (~69 cheap iterations). The budget check on line 297 prevents overshoot. The `main()` function uses `n_iters=15` (not cost-fair), but the cost-efficiency figure was generated with `cost_budget=1190`.

**Q4 (Results interpretation)**: The user's interpretation — "partial root-only evaluations don't propagate enough information through the DAG" — is **partially correct but incomplete and premature**. The primary cause of p-KGFN's underperformance is Bug #1 (double normalization), which produces fantasy posterior mean errors of up to 41.65% of the posterior range. This renders p-KGFN's node selection essentially random. The root-only limitation (only nodes 0 and 2 are candidates, leaving nodes 1 and 3 at their initial 9 observations) is a valid secondary concern, but one cannot draw conclusions about partial evaluation's inherent value from these results until the bugs are fixed. The results (Random 0.70±0.30, TSFN 0.71±0.32, pKGFN 0.67±0.28) are consistent with p-KGFN operating as a random selector due to corrupted acquisition values.

**Q5 (Determinism)**: **YES**, the seeding is sufficient. `ManufacturingGPNetwork(seed=0)` calls `torch.manual_seed(0 * 7919 + 42)` and then reseeds at each `get_matheron_path_model` call (seeds 88, 112, 11, 185 for seed=0). All algorithms optimize the same function network when the problem seed is the same. The BO loop seed (`torch.manual_seed(seed)` in `run_bo_loop`) provides deterministic initialization. Sobol samples (used for initial data) are quasi-random with deterministic sequences, ensuring identical initial data across algorithms within the same seed.

---

### Discretionary Analytical Decisions

- Tested the double normalization bug using a manufacturing-like GP setup (2D, [-1,1] domain, 9 training points) rather than attempting to run the full p-KGFN pipeline end-to-end, to isolate the bug's impact.
- Classified the missing `super().__init__()` as LOW severity since it doesn't affect correctness in the current CPU-only, non-serialized usage pattern, though it would be HIGH in a production context.
- Classified the unused sampler as MODERATE rather than HIGH because the KG estimator remains unbiased (just noisier) — it degrades efficiency rather than correctness.
- Assessed the root-only restriction as a design choice rather than a bug, since nodes 1 and 3 have no exogenous inputs and thus cannot be independently evaluated without first evaluating their parents.
- Verified BoTorch version-specific behavior (0.17.2) for SingleTaskGP kernel structure (RBFKernel, no ScaleKernel wrapper) and condition_on_observations transform handling, recognizing these may differ in other BoTorch versions.
- Used BoTorch 0.17.2 for verification, which was the latest version available via pip at analysis time.
