# spotcheck-q1-inner-kg-fantasies

_task_id: da0e968a-25cc-4f91-bc37-0cbad1140a07; status: success_

I audited the remaining `PartialKnowledgeGradientFN` logic in your local `partial_kgfn.py`, compared it to the surrounding call sites in `bofn_pkgfn_demo.py` / `gp_network.py`, and did a small executable smoke after installing BoTorch / Torch. Short version: A1/A2/A3 fixed real issues, but there are still two material correctness / robustness problems and one likely source of apparent node-selection bias.

Findings

1. q-dim handling is only correct for `q=1`, and the code does not enforce that.
   - In `partial_kgfn.py:202`, `x_i = X[i : i + 1]` has shape `(1, q, d_k)`.
   - In `partial_kgfn.py:212` and `partial_kgfn.py:222`, the code uses `x_i.squeeze(1)`.
   - That is correct only when `q == 1`. If `q > 1`, `squeeze(1)` is a no-op, leaving shape `(1, q, d_k)`, which is not what `node_GPs[k].posterior(...)` / `condition_on_observations(...)` expect here.
   - The docstring says “currently only q=1 supported” (`partial_kgfn.py:96`), but `__init__` never validates `q == 1`.
   - So the current logic is fine for the present usage path, because `pkgfn_step` passes `q=1` (`bofn_pkgfn_demo.py:271`), but it is brittle and can silently misbehave if reused elsewhere.
   - Recommendation: hard fail in `__init__` with `if q != 1: raise NotImplementedError(...)`.

2. Inner KG optimisation is not using `optimize_acqf` at all here.
   - I checked the local call sites. `PartialKnowledgeGradientFN` itself does not call `optimize_acqf`; it evaluates a discrete set and takes a max over `self.X_fantasies_candidates` in `partial_kgfn.py:229-233`.
   - Outer node-selection in `pkgfn_step` also does not call `optimize_acqf`; it evaluates `pkgfn` on `raw_cands.unsqueeze(1)` and picks `argmax` (`bofn_pkgfn_demo.py:281-292`).
   - The `optimize_acqf` calls I found are for EI baselines only, not p-KGFN.
   - So for this code path, the question is really whether the discrete candidate sets live in the right space:
     - inner max grid: full `x` space, because `_network_posterior_mean(fantasy_model, self.X_fantasies_candidates)` expects full-network inputs and `GaussianProcessNetwork.posterior(X)` consumes full `d`-dimensional designs (`partial_kgfn.py:230-232`, `gp_network.py:104-108`). This is correct.
     - outer candidate set: per-node input space, because `pkgfn(raw_cands.unsqueeze(1))` feeds node-local candidate inputs into the fantasized node GP only (`bofn_pkgfn_demo.py:281-289`). This is also correct.
   - On ratios: the local benchmark defaults are fairly small but not crazy for a smoke setting.
     - demo default: `n_fantasies=64`, `n_grid=200`, `n_raw=128` (`bofn_pkgfn_demo.py:203`, `:245`, `:251`, `:281`).
     - benchmark full default: `num_fantasies=32`, `n_raw=64` for pKGFN (`bofn_actions_benchmark.py:491-498`, from prior file inspection).
   - My take: `num_fantasies=32` or `64` is reasonable for a discrete smoke, but after A2 the estimator variance is now dominated by the inner SAA in `_network_posterior_mean`, not just by the outer fantasy count. So the effective MC budget is thinner than those numbers suggest.

3. `_network_posterior_mean` is using fresh random samples every call. No CRN / paired base samples.
   - The new A2 code is:
     - `posterior = model.posterior(X)` (`partial_kgfn.py:57`)
     - `samples = posterior.rsample(sample_shape=torch.Size([n_saa]))` (`partial_kgfn.py:58`)
     - `return samples[..., -1].mean(dim=0)` (`partial_kgfn.py:60`)
   - There is no sampler object, no fixed base samples, and no `rsample_from_base_samples` call.
   - In executable checks on a fitted tiny 4-node manufacturing model, two consecutive calls on the same `(model, X)` gave:
     - max absolute difference `0.01098`
     - mean absolute difference `0.00402`
     for `n_saa=64`.
   - That is enough to perturb seed-level rankings when per-node KG-per-cost values are close.
   - This directly explains why estimated KG can become slightly negative even though true KG is non-negative. In my smoke run, with `current_value` computed the same way as the demo, node-0 KG values were about `-0.0012` to `-0.0017`, and node-3 KG values about `-0.0012` to `-0.0020`. That is pure MC estimation noise, not true negative KG.
   - So yes: fresh sampling each call is still a real issue after A2. It inflates seed std and can distort node rankings when values are close.

4. Residual node-selection bias: yes, but it does not look like “rounding”. It looks like variance-driven winner’s curse under cost division.
   - Cost adjustment is plain division, `cost_adjusted = acq_val / problem.node_costs[k]` at `bofn_pkgfn_demo.py:299`. I did not find any rounding / floor / integer cast.
   - So if `min_cost` is equal or very close to the root-node cost, cost normalization does not meaningfully regularize low-cost nodes against MC noise.
   - Combined with A2’s noisy SAA inner mean, the selected node is whichever low-cost node got the luckiest positive error that iteration.
   - That can look like persistent over-selection of node 0 if node 0 has either:
     - slightly larger mean KG-per-cost, or
     - larger estimator variance than its peers.
   - In my tiny 4-node smoke with uniform costs, I did not reproduce node-0 over-selection. Across 8 tiny refits, selected nodes were `[2, 2, 3, 1, 3, 2, 2, 2]` with counts `{2: 5, 3: 2, 1: 1, 0: 0}`. So I cannot honestly claim node-0 bias from my local smoke.
   - But I can say the mechanism for residual bias is still there: if several nodes have near-tied KG-per-cost, fresh inner SAA noise can decide the winner. That is consistent with the concern you raised.

5. One more robustness issue in the fantasy sampler wiring.
   - In `__init__`, if `sampler is None`, the code builds a list of samplers of length `int(X_evaluation_mask.sum())` (`partial_kgfn.py:122-125`).
   - In `forward`, it always uses `self.sampler[0]` (`partial_kgfn.py:214`).
   - That is OK only because this implementation always fantasizes exactly one node at a time. If someone ever passes a multi-node mask, the sampler list length and access pattern diverge from intent.
   - Given the current usage path, this is not a live bug, but it is another place where the API advertises more flexibility than the code actually supports.

Executable smoke test

I was able to install the requested stack:
- `torch 2.10.0+cu128`
- `botorch 0.17.2`
- `gpytorch 1.15.2`

Limitation: the workspace did not actually contain the expected `benchmarks/partial_kgfn/` package tree. The local files were flat (`partial_kgfn.py`, `gp_network.py`, `manufacturing_problem.py`), while imports in the demo expected `benchmarks.partial_kgfn.*`. Also `dag.py`, `utils.py`, and `thompson_sampling.py` were absent. To exercise the code, I created minimal local package scaffolding and small stubs for those missing modules. That means the smoke test is a sanity check of the p-KGFN plumbing, not a clean repo-native execution.

What I ran
- Built a tiny 4-node `ManufacturingGPNetwork` model with 2 Sobol init points.
- Fit `GaussianProcessNetwork` with per-node `Normalize(bounds=...)` as in A3.
- Evaluated `PartialKnowledgeGradientFN` on small batches for node 0 and node 3.
- Ran a few `pkgfn_step(...)` calls with `n_fantasies=4`, `n_grid=20`, `n_raw=8`.

What happened
- The acquisition code itself ran without shape errors for `q=1`.
- Candidate batch shapes were consistent with expectations:
  - root node candidate batch: `(b, 1, d_k)` with `d_k=2`
  - parent-only node candidate batch: `(b, 1, d_k)` with `d_k=2`
- Sample KG outputs for node 0 were about `0.5174` to `0.5182` before subtracting a proper `current_value`, and then around `-0.0012` to `-0.0017` after subtracting `current_value` computed the same way as the demo.
- So “KG values monotone non-negative” did not hold in the noisy finite-sample estimator. They became slightly negative, which is evidence of MC noise from A2, not of a theoretical negative KG.
- Repeated `pkgfn_step` calls on a fixed fitted model returned successfully and selected the same node repeatedly in one setup (`[2,2,2,2,2]`), but that is on a very small synthetic run and not evidence about the production benchmark distribution.

Line-specific conclusions

- `partial_kgfn.py:202, 212, 222`
  - `x_i.squeeze(1)` is only safe for `q=1`. Add an explicit guard.

- `partial_kgfn.py:229-233`
  - Inner maximization over full `X_fantasies_candidates` is the right space for the network-level posterior mean objective.
  - But because `_network_posterior_mean` is stochastic now, the inner argmax is noisy.

- `partial_kgfn.py:33-60`
  - A2 fixed Jensen bias, but there is no CRN / fixed base-sample mechanism. This is now the main remaining statistical issue.

- `bofn_pkgfn_demo.py:268-279, 281-292, 299`
  - Outer node-local candidate evaluation space is correct.
  - No `optimize_acqf` here.
  - Cost adjustment is simple division; no rounding artifact found.

Bottom line

- Batch-shape logic: OK for the only live mode (`q=1`), unsafe otherwise because there is no validation.
- Inner optimization bounds: correct in the current discrete implementation. Full `x` for inner network max, per-node input space for outer node evaluation.
- `n_fantasies` / candidate counts: reasonable for smoke runs, but after A2 they are not enough to suppress inner SAA noise when node KG-per-cost values are close.
- CRN variance reduction: not implemented. `_network_posterior_mean` uses fresh samples each call, and this is the biggest remaining source of seed instability.
- Node-0 over-selection: I did not reproduce it in my tiny executable smoke, so I won’t claim it from data I don’t have. But there is still a residual low-cost-node selection bias mechanism from noisy KG-per-cost estimates, and it does not require any rounding bug.

What I would change next

1. Enforce `q == 1` in `PartialKnowledgeGradientFN.__init__`.
2. Make `_network_posterior_mean` optionally accept a sampler or fixed base samples, so repeated evaluations use paired randomness where possible.
3. Clamp reported KG at `max(value, 0)` only for ranking / logging if you want numerical sanity, but not as a substitute for fixing the estimator variance.
4. If the benchmark still shows node-0 over-selection, log per-node raw `acq_val`, cost-adjusted value, and repeated-evaluation variance on the same fitted model. That will tell you fast whether the issue is mean bias or variance-driven selection.

Sources
- Local audited files: `partial_kgfn.py`, `gp_network.py`, `bofn_pkgfn_demo.py`, `manufacturing_problem.py` in `/workspace/da0e968a-25cc-4f91-bc37-0cbad1140a07/`
- Original repo reference cited in file header: `https://github.com/frazier-lab/partial_kgfn`
- Astudillo & Frazier 2021, BOFN: arXiv:2112.15311
- Buathong et al. 2024, p-KGFN: arXiv:2311.02146
- Buathong & Frazier 2025, Fast p-KGFN: arXiv:2506.11456

- Discretionary analytical decisions made during the analysis
- Installed the requested Python stack in-place and proceeded with a smoke test after successful install rather than doing static audit only.
- Because the expected `benchmarks/partial_kgfn/` package tree was absent from the workspace, created minimal local scaffolding and stubs (`dag.py`, `utils.py`, `thompson_sampling.py`) solely to exercise the acquisition path; treated resulting execution as a smoke test, not a definitive repo-native validation.
- Used a tiny 4-node manufacturing problem with 2 Sobol initial points, `n_fantasies=4`, `n_grid=20`, and `n_raw=8` for executable sanity to keep runtime under the requested budget.
- Assessed inner-SAA instability by repeated calls to `_network_posterior_mean` on the same fitted model and candidate set, using absolute differences as an empirical measure of estimator noise.
- Interpreted small negative estimated KG values as Monte Carlo estimation error rather than true negative KG, based on KG non-negativity theory and observed replicate variability.
- For the node-selection-bias check, used a small multi-seed uniform-cost experiment as a quick diagnostic for residual low-cost-node bias, while treating it as underpowered and not generalizable to the full benchmark.
