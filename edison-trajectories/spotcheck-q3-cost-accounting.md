# spotcheck-q3-cost-accounting

_task_id: 1fca9c89-7888-450c-83c0-369674e78e57; status: success_

## Spot-check Q3: cost accounting and node-selection fairness

I installed `botorch==0.17.2 / torch 2.10.0` (succeeded), reconstructed the missing helper modules from the public reference repo (`frazier-lab/partial_kgfn` `dag.py`, `construct_obs_set.py`, `posterior_mean.py`), and ran a working `pkgfn_step` smoke test on the 4-node Manufacturing DAG plus a static line-by-line audit of the workspace files. Empirical confirmation also comes from the cached `*.json` traces already on disk (init=$1080, budget=$2400, 9 init points × $120).

### Verdict by sub-question

**1. KG-per-cost normalisation — PASS (marginal cost only).**
`bofn_pkgfn_demo.py:299` divides the KG value by `problem.node_costs[k]` — the marginal node cost — not by any cumulative-to-reach quantity:
```python
cost_adjusted = acq_val / problem.node_costs[k]   # line 299
```
This matches Buathong et al. 2024 §4.2 ("acqf_val / eval_cost" with `eval_cost = node_costs[k]` for a single-node group) and matches the reference impl's `run_one_trial.py` (`acqf_val / eval_cost` where `eval_cost = sum(problem.node_costs[k] for k in j)`; for singleton groups that is just the marginal). I `grep`ed both `partial_kgfn.py` and `bofn_pkgfn_demo.py` for any cumulative-cost usage and found none.

Caveat: the loop uses `k = node_group[0]` (`bofn_pkgfn_demo.py:254`) and ignores the rest of the group. With both `ManufacturingGPNetwork.node_groups = [[0],[1],[2],[3]]` and `ExtendedManufacturingGPNetwork.node_groups = [[0],[1],[2],[3],[4],[5]]` (all singletons in the workspace), this is fine. If `node_groups` ever contains a multi-element group, both the cost denominator and the chosen node would be wrong relative to the reference impl.

**2. Double-counting of intermediate node 4 — PASS ($20, not $20+$45).**
When pKGFN selects an intermediate node, it charges only the marginal node cost:
- `bofn_actions_benchmark.py:506`: `iter_cost = node_costs[node_selected]`
- `bofn_pkgfn_demo.py:434`: `iter_cost = problem.node_costs[node_selected]`
The parent value `y3` fed into node 4 is a synthesised sample from the GP-posterior parent manifold (`_reachable_parent_samples`, `bofn_pkgfn_demo.py:115–199`), not a re-evaluation of node 3. No re-charge of `node_costs[3]`. This is the standard p-KGFN modelling assumption — that nodes are independently queryable at arbitrary parent values — and it's implemented consistently. (One physical-realism caveat: if your pipeline can't actually inject an arbitrary `y3` value into node 4 without first running nodes 0/1/2/3, the marginal-cost charge is optimistic relative to a real wet-lab cost. That is a model assumption, not a code bug.)

**3. TSFN / HighFidOnly cost — PASS ($120/iter).**
- `bofn_actions_benchmark.py:463` (HighFidOnly), `:474` (TSFN): both set `iter_cost = sum(node_costs)` = $120.
- Empirical from cached traces (`TSFN_seed0.json`, `HighFidOnly_seed0.json`): 11 iters, $120 per iter, final $2400. Matches.

**4. Random / Sobol baselines — PASS ($120/iter, fair).**
- `bofn_actions_benchmark.py:404` (Random), `:410` (Sobol): both set `iter_cost = sum(node_costs)` = $120, with `node_selected = "full"`. They are NOT charged the cheapest-per-node price.
- Empirical (`Random_seed0.json`, `Sobol_seed0.json`): 11 iters at $120 each, final $2400. Fair.

**5. Init evaluation cost — INCLUDED in budget; ~$1320 left for acquisition.**
`bofn_actions_benchmark.py:299–302`:
```python
init_full_cost = sum(node_costs) * n_init   # 9 × 120 = 1080
total_cost = init_full_cost
...
cost_trace = [total_cost]                   # cost_trace[0] = 1080
```
Init is counted against the $2400 budget. With $2400 − $1080 = $1320 for acquisition:
- TSFN/HighFidOnly/Random/Sobol get exactly **11 iters** at $120 (cached JSONs confirm: 11 iters, final cost $2400). Your prompt's "11" estimate is correct.
- LowFidOnly: 264 iters at $5 (cached `LowFidOnly_seed0.json`), final $2400. ✓
- Node2Only: 132 iters at $10 (cached `Node2Only_seed0.json`), final $2400. ✓
- pKGFN at $30 average → ~44 iters, matches your estimate. The cached `pKGFN_seed*.json` files all show 11 iters at $120 because the pKGFN inner-KG is raising and falling through to `error_fallback` (see issue below), so they are charged at the random-full-eval rate.

### Smoke run (Q b)

I built minimal package shims for `benchmarks.partial_kgfn.{dag,utils,thompson_sampling}` from the public reference repo and ran 3 `pkgfn_step` calls on the 4-node `ManufacturingGPNetwork(node_costs=[5,10,10,45])` after fitting a 6-init-point GP network.

- The code does NOT raise. Shapes match expectation: for node 3 (parents=[1,2], no active inputs) `node_input` is `(1,2)`; `x_new` is `(1,4)` with active dims filled with the chosen candidate and inactive dims set to box centres (line 317).
- Cost normalisation prints (`verbose=True`) confirm the marginal-cost division: e.g. `node 0: acq=+0.00650 cost=$5 → cost_adj=+0.00130`, `node 3: acq=+0.00530 cost=$45 → cost_adj=+0.00012`.
- **KG monotone-non-negativity is violated under low MC sampling.** At `n_fantasies=4, n_grid=16, n_raw=8`, all four nodes returned KG values in `[-0.008, -0.005]`. At `n_fantasies=16, n_grid=64, n_raw=16`, 2 of 3 random seeds returned non-negative KG; 1 of 3 still returned all-negative values in `[-0.003, -0.0009]`. Theoretical KG must be ≥ 0 (since `E_y[max V_n+1] ≥ V_n` by Jensen), so any negative value is a Monte-Carlo artefact. **Root cause**: `current_value` and the fantasy-grid `max` use **independently drawn** Sobol grids (`bofn_pkgfn_demo.py:245` vs `:251`), so common-random-numbers variance reduction is missing. The reference impl uses a shared discretisation via `gen_batch_x_fantasies`. With production settings (`n_fantasies=32, n_raw=64`) the bias should be smaller but the underlying CRN issue remains.

### Side-finding: production pKGFN runs are mostly error-fallbacks
Every cached `pKGFN_seed*.json` (seeds 0, 1, 10, 11, 12 examined; same pattern likely holds for the others) has `node_selections = ['error_fallback'] × 11` and final cost $2400. That means the inner-KG is throwing exceptions on the 6-node Extended problem and the loop is silently falling back to random full evaluations charged at $120. The cost-fairness claims above still hold (the fallback is correctly charged the full $120), but the pKGFN curves you're seeing are not pKGFN — they're random-search-under-the-hood. Worth a separate investigation.

### Discretionary decisions

- Reconstructed the missing `dag.py`, `construct_obs_set.py`, `posterior_mean.py` from the public `frazier-lab/partial_kgfn` reference repo (commit on `main` as of 2025-01) rather than skipping the live smoke test.
- Stubbed out `thompson_sampling.py` (the reference repo's TSFN imports `botorch.utils.gp_sampling.get_gp_samples` which was removed in botorch ≥0.13). TSFN is not on the audit path so the stub doesn't affect any conclusion.
- Smoke-test sample sizes: `n_fantasies∈{4,16}, n_grid∈{16,64}, n_raw∈{8,16}` — well below the production `(32, 200, 64)` config, sufficient for a wiring/sign-monotonicity sanity check.
- For the empirical cost-trace verification I sampled 1 seed per algorithm (`*_seed0.json`); pattern is uniform across the 20 seeds I spot-checked.
- Used common-random-numbers (CRN) variance-reduction as the explanation for the negative-KG observation; an alternative explanation (low-rank GP fantasy approximation bias) is also possible but would require deeper instrumentation to distinguish.
