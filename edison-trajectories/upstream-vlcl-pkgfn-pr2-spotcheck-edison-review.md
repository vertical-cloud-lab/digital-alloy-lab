# Edison spot-check review: our pKGFN port vs `vertical-cloud-lab/partial_kgfn` PR #2

- **Task ID**: `653fe70e-8a0e-4464-8948-5ed874832b63`
- **Job**: `job-futurehouse-data-analysis-crow-high`
- **Status**: `success`
- **Submitted**: 2026-05-08T04:12:49Z
- **Fetched**: 2026-05-08T14:05Z (~10 h)
- **Spot-check input**: `edison-trajectories/upstream-vlcl-pkgfn-pr2-spotcheck.md` + 7 code/figure files

---

### 1. Inconsistency Table Re-Derivation (Scored)

Based on a detailed, independent walk of both code-bases, here is the confirmation status for the spot-check table items.

#### Pass 1 — `PartialKnowledgeGradientFN.forward()`
*   **1.1 Vectorised fantasy**: **Confirmed**. Upstream (`partial_kgfn.py:191-196`) uses a single batched `.fantasize()`. Our port (`partial_kgfn.py:246-262`) loops `for f in range(self.num_fantasies)` calling `condition_on_observations`.
*   **1.2 Inner posterior eval**: **Confirmed**. Upstream (`partial_kgfn.py:197-202`) evaluates `fantasy_post_at_X` once. Our port (`partial_kgfn.py:264-269`) loops and calls `_network_posterior_mean` per fantasy.
*   **1.3 `inner_sampler` arg honoured?**: **Confirmed** (Bug). Upstream uses it (`partial_kgfn.py:200`). Our port stores it (`partial_kgfn.py:193`) but ignores it in `forward()`, instead constructing a fresh `SobolQMCNormalSampler` (`partial_kgfn.py:232-234`).
*   **1.4 `observation_noise` on fantasy obs**: **Confirmed**. Upstream passes it (`partial_kgfn.py:194`) but BoTorch's `fantasize()` ignores it silently. Our port injects noise explicitly (`partial_kgfn.py:246-248`).
*   **1.5 Reduction order**: **Confirmed**. Different paths but mathematically equivalent.
*   **1.6 t-batch decorator**: **Confirmed**. Both use `@t_batch_mode_transform()`.
*   **1.7 `use_posterior_mean` flag**: **Confirmed**. Stored but never read in our `forward()`.
*   **1.8 `current_value` subtraction**: **Confirmed**. Both subtract it at the end to get KG.
*   **1.9 `X_fantasies_candidates` default**: **Confirmed**. Both fall back to $50d$ unanchored Sobol points.

#### Pass 2 — `pkgfn_step` driver vs `run_one_trial.py`
*   **2.1 `X_fantasies_candidates` set**: **Confirmed** (Major Regression). Upstream (`run_one_trial.py:716-732`) dynamically anchors fantasies on `best_design` (radius + TS optima + incumbent). Our port (`bofn_pkgfn_demo.py:251`) uses fixed, unanchored global Sobol points.
*   **2.2 `num_fantasies`**: **Confirmed**. Upstream hardcodes 8 (`run_one_trial.py:749`). Our benchmarks set it to 32-64.
*   **2.3 `inner_sampler`**: **Confirmed**. Upstream passes 64-SAA (`run_one_trial.py:754`). Ours is dropped (see 1.3).
*   **2.4 Acquisition optimiser**: **Confirmed**. Upstream uses `optimize_discrete_acqf_for_function_network` with continuous L-BFGS refinement (`run_one_trial.py:757`). Our port evaluates `pkgfn(raw_cands)` once and takes the `argmax` (`bofn_pkgfn_demo.py:281-295`).
*   **2.5 `impose_assump` (upstream-downstream)**: **Confirmed**. Handled upstream (`discrete_kgfn_optim.py:57+`), absent in our port.
*   **2.6 `current_value` / `best_post_mean`**: **Confirmed**. Upstream does multi-restart L-BFGS (`run_one_trial.py:530-536`). We use `compute_posterior_mean_network` over 200 Sobol points (`bofn_pkgfn_demo.py:246`).
*   **2.7-2.10 (Various ops)**: All **Confirmed** and judged OK as noted in the original table.

#### Pass 3 — GP Networks
*   **3.1 `fantasize()` observation noise**: **Confirmed**. Upstream ignores it; we explicitly add it.
*   **3.2 Per-node `Normalize` bounds**: **Confirmed**. Intentional improvement in our `gp_network.py`.
*   **3.3 `Standardize` outcome**: **Confirmed**.
*   **3.4 `MultivariateNormalNetwork.rsample`**: **Confirmed**.
*   **3.5 DAG topo walk**: **Confirmed**.
*   **3.6 `condition_on_observations` shape dance**: **Confirmed**. In upstream `run_one_trial.py:495` vs our `gp_network.py`. (BoTorch ≥0.13 API shift handled correctly in our port).

#### Pass 4 — ThompsonSamplingFN
*   **4.1 - 4.3**: All **Confirmed**. Faithful port using `get_matheron_path_model`.

---

### 2. Newly Caught Inconsistencies (What You Missed)

1. **Latent Bug in `rsample_from_base_samples` Shape Contract**: Upstream preserves the trailing base-sample dimension for root nodes (`base_samples[..., [k]]` at `decoupled_gp_network.py:403`). Our port flattens it (`base_samples[..., k]` at `gp_network.py:310`). Additionally, for non-root nodes, upstream attempts to propagate base-samples (`decoupled_gp_network.py:440`), whereas our port falls back to `rsample` without base samples (`gp_network.py:330`), breaking CRN across the network. *Note: This is currently masked because `partial_kgfn.py` uses SAA (`_network_posterior_mean`) rather than `rsample_from_base_samples`, but will break if the API is used elsewhere.*
2. **Four More Dropped Arguments in `partial_kgfn.py`**: Beyond `inner_sampler`, our port stores but never references `self.objective`, `self.posterior_transform`, `self.cost_aware_utility`, and `self.cost_sampler` in `forward()`. The `objective` drop is particularly dangerous: `_network_posterior_mean` hardcodes `samples[..., -1].mean(dim=0)`, rendering any user-provided scalarisation or target-node override a silent no-op.
3. **Upstream KGFN Cost-Accounting Bug**: Upstream `run_one_trial.py:404` categorizes KGFN as a "full eval" algorithm, making the partial-eval KGFN branch at `407` unreachable. Our port does not replicate this bug, but it indicates upstream KGFN comparisons may be flawed.

---

### 3. Quantitative Impact & Priorities

I successfully ran a smoke test of our port with logging injected. **Fix 2.1 is unquestionably the dominant issue.** Without anchoring `X_fantasies_candidates` on the incumbent, the inner fantasy optimization space is globally random and regularly fails to include the current best point. 

**Empirical Evidence:**
*   **Unanchored (current port)**: `current_value` = 1.0003, but `fant_vals.max()` = 0.9903. Because the fantasy space doesn't contain the incumbent, the Knowledge Gradient is algebraically **negative** (max across all nodes ranged from -0.003 to -0.011).
*   **Anchored (Fix 2.1 applied)**: I injected a radius=0.2 anchored candidate set around the best design. `fant_vals.max()` shifted to 1.0354. KG values became strictly **positive** (+0.037 to +0.039) and the ranking flipped to favor the cheapest node.

#### Prioritised Fixes for Maximum Lift

1.  **Fix 2.1 (Anchor `X_fantasies_candidates`)**  
    *Expected Lift: High.* Moving from a negative-biased KG to a positive, cost-responsive KG is essential for pKGFN to beat random search. Implement upstream's `generate_X_fantasies_candidates_RaLo`.
2.  **Fix 2.2 (Drop `num_fantasies` to 8)**  
    *Expected Lift: Wall-clock multiplier.* With anchored candidates, the MC noise drops substantially relative to the KG signal ($\sigma / \mu \approx 0.05$ at $n=8$). Dropping from 32/64 to 8 fantasies cut per-node evaluation time from 16.7s to 4.3s in my smoke test (a ~4x speedup) with no meaningful loss in ranking fidelity.
3.  **Fix 1.3 + Objective Drop (Wire `inner_sampler` & `objective`)**  
    *Expected Lift: Moderate/Hygiene.* Wire `self.inner_sampler` into the `SobolQMCNormalSampler` fallback in `forward()`, and replace the hardcoded `samples[..., -1]` in `_network_posterior_mean` with `self.objective(samples)`. 
4.  **Fix 2.4 (Continuous L-BFGS refinement)**  
    *Expected Lift: Moderate.* Refining the discrete argmax via L-BFGS over `problem.bounds` recovers the last ~10-20% of acquisition signal in non-linear regions.
5.  **Fix 2.5 (`impose_assump`) and Vectorised Fantasy (1.1/1.2)**  
    *Expected Lift: Low/Deferred.* The DAG structure is shallow enough that upstream-downstream constraint violations are edge cases, and wall-time should be acceptable once Fix 2.2 lands.

### Discretionary Decisions
- Validated CRN behaviour computationally rather than purely statically; empirical tests confirmed that `inner_saa_sampler` instance reuse provides sufficient CRN stability ($\sim 5\%$ relative noise floor) even without `rsample_from_base_samples` being fully hooked up.
- Treated the upstream `run_one_trial.py` KGFN unreachable-branch bug as a non-issue for our port, as we rely on our own benchmark driver (`bofn_actions_benchmark.py`), which correctly isolates `iter_cost = node_costs[node_selected]` inside the pKGFN block.
- Diagnosed the shape mismatch in `rsample_from_base_samples` as latent/unreachable rather than critical, given that SAA currently bypasses it.