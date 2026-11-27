# p-KGFN Implementation Code Review

**Date:** 2026-04-13
**Scope:** `benchmarks/bofn_pkgfn_demo.py`, `benchmarks/bofn_pkgfn_visualize.py`, `benchmarks/partial_kgfn/`
**Method:** Systematic code audit + diagnostic runs (Edison API unavailable from sandbox)

## Summary

The p-KGFN implementation is functionally correct but has one reporting bug and one significant design limitation that explains the unexpectedly flat performance.

**Grade: B** (correct implementation with reporting issue and known limitation)

---

## Issue 1: Stale-Model Best-Value Tracking (BUG)

**Severity:** Medium — affects reported results but not algorithm fairness

The `run_bo_loop` computes `best_vals` using the GP model fitted **before** the current iteration's observation is added:

```
Step 1: Fit model from current observations
Step 2: Select + evaluate new point → add to training data
Step 3: Compute best_vals using model from Step 1 (STALE)
```

This means the final reported best value does not include the benefit of the last observation. For baselines doing 8 iterations, the 8th observation's improvement is never captured. The issue affects all algorithms equally (no bias), but understates final performance.

**Fix:** Move best-value tracking after adding the new observation and refitting.

## Issue 2: Root-Only Partial Evaluation (DESIGN LIMITATION)

**Severity:** High — explains why p-KGFN doesn't outperform baselines

The `pkgfn_step` function skips all non-root nodes:
```python
if len(parents) > 0:
    continue  # Skip nodes 1 and 3
```

This means p-KGFN only ever evaluates nodes 0 ($5) and 2 ($10), never nodes 1 ($10) or 3 ($45). After the BO loop:

| Node | p-KGFN obs | Baseline obs |
|------|-----------|-------------|
| 0 (root) | 9 + ~35 = 44 | 17 |
| 1 (intermediate) | **9 only** | 17 |
| 2 (root) | 9 + ~34 = 43 | 17 |
| 3 (final) | **9 only** | 17 |

Nodes 1 and 3 are the bottleneck — their GPs have nearly half the training data compared to baselines. The paper's p-KGFN evaluates **any** node, including intermediates, which is key to its advantage.

**Impact on results:** Diagnostic 9 showed that even with root-only extra observations, the network posterior quality (r=0.98 vs 0.98, RMSE 0.030 vs 0.032) is comparable to baselines. The information **does** propagate through the DAG. However, the optimization loop (acquisition function + cost budget) isn't exploiting this advantage enough.

**Fix:** Not a bug — this is a documented simplification. The original paper handles intermediate node evaluation by sampling parent outputs from the posterior. This requires significant additional complexity.

## Issue 3: Noisy Acquisition Function Estimates

**Severity:** Low — acceptable for a demo

- `num_fantasies=4`: Only 4 fantasy samples for the outer expectation
- `n_grid=50`: Only 50 points for inner optimization in 4D space
- `n_raw=32`: Only 32 candidates for discrete acquisition optimization

These are small values that make the p-KGFN acquisition value noisy. The original paper uses larger values (16–64 fantasies, 200+ grid points). For the demo this is acceptable, but for a real benchmark these should be increased.

## Verified Correct

1. **Determinism:** `ManufacturingGPNetwork._build_node_functions` is fully seeded — all algorithms optimize identical function networks ✓
2. **Partial evaluation:** `problem.evaluate(x, idx=[k])` matches the corresponding output from full evaluation ✓
3. **Cost accounting:** p-KGFN charges only the selected node's cost; baselines charge full $70 ✓
4. **GP network construction:** `construct_obs_set` correctly builds per-node training data with active inputs + parent outputs ✓
5. **Posterior mean propagation:** `compute_posterior_mean_network` correctly propagates through the DAG ✓

## Recommendations

1. **Fix the stale-model tracking** (move best_vals after observation) — immediate
2. **Document the root-only limitation** in the visualization and synthesis doc
3. **Increase budget** to $3,500+ to give p-KGFN more room to compound
4. **Consider implementing intermediate node evaluation** for a more faithful comparison
