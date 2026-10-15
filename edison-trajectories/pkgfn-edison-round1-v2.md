# Edison ANALYSIS Round 1 (v2) — p-KGFN Implementation Review

# p-KGFN Implementation Review: Comprehensive Analysis

## Executive Summary

The p-KGFN implementation is **functionally correct** — I found no bugs in the current code. Both previous reviews contain significant errors (the Edison review's 4 "bugs" are all false positives; the first review's stale-model bug was already fixed). The root-only evaluation limitation is correctly identified by both reviews as the key issue, but its consequences are deeper than either review articulates. Increasing the budget will not help. The fundamental problem is a structural observation imbalance that creates a biased model at the optimum.

---

## Question 1: Bugs and Correctness Issues

**VERDICT: No correctness bugs exist in the current code.**

### Verified correct:
- **Fantasy model conditioning** (`gp_network.py:126`): Does NOT call `transform_inputs()`. The comment at lines 124–125 explicitly documents this: "Do NOT call transform_inputs() here — condition_on_observations() applies the input transform internally." I verified empirically that the correct approach (passing raw X) produces posterior means within 0.001 of the conditioning value at the conditioning point, while the double-normalized approach produces errors of 0.59 (41% of posterior range).
- **Sobol sampler usage** (`partial_kgfn.py:230`): `self.sampler[0](post_k)` IS called; the Sobol QMC sampler is used as intended.
- **`super().__init__()`** (`gp_network.py:49`): IS called — the line is present in the source.
- **`self.X` mutation** (`gp_network.py:275`): Assigns to LOCAL variable `X`, not `self.X`.
- **KG computation**: Manual step-by-step recreation matches `forward()` output to 4 decimal places (0.028196 vs 0.028210).
- **Cost accounting**: Init = 9 × $70 = $630; partial evals charged at $5 or $10; full evals at $70.
- **Partial evaluation data updates**: Only the selected node's GP training data is updated; no information leakage from the "free" full evaluation (line 317), which is used only for verbose printing.
- **Best-value tracking**: The model IS refitted after adding new observations (lines 344–357), then posterior mean is computed on the updated model.

### Edison review assessment (Grade C+): **All 4 claimed bugs are false positives.**
- Bug #1 (double normalization): The code explicitly avoids this with a comment explaining why.
- Bug #2 (unused sampler): The sampler IS used at line 230.
- Bug #3 (missing super().__init__): Present at line 49.
- Bug #4 (self.X mutation): Local variable `X`, not `self.X`.

### First review assessment (Grade B): Stale-model bug was already fixed in the current code.

### Minor code quality issues (non-bugs):
- `node_GPs` stored as a Python list instead of `nn.ModuleList` — prevents proper parameter tracking by PyTorch, but doesn't affect correctness in CPU-only, non-serialized usage.
- Sequential candidate loop in `forward()` is slow (O(b × num_fantasies)) but correct.

---

## Question 2: Root-Only Evaluation vs. Intermediate Nodes

**VERDICT: Root-only evaluation is NOT the correct approach. It's a major limitation that fundamentally cripples p-KGFN's advantage.**

### What happens with root-only evaluation:
The code (`bofn_pkgfn_demo.py:134`) skips all non-root nodes: `if len(parents) > 0: continue`. This means p-KGFN only evaluates nodes 0 ($5) and 2 ($10), never nodes 1 ($10) or 3 ($45).

### Why this matters — quantitative evidence:
At $2,730 budget, the observation counts are:

| Node | Baseline (30 full) | p-KGFN (~280 root) |
|------|-------------------|-------------------|
| 0 (root, $5) | 39 | ~149 |
| 1 (intermediate, $10) | 39 | **9 (init only)** |
| 2 (root, $10) | 39 | ~143 |
| 3 (final, $45) | 39 | **9 (init only)** |

Nodes 1 and 3 are **data-starved** in p-KGFN. With only 9 observations, their GP models remain inaccurate, creating a structural bias in the network posterior.

### The flat KG surface:
I measured the KG acquisition values across 32 candidate locations for node 0 with 64 fantasies. The coefficient of variation is only **1.6%** (range: 0.0270–0.0291, mean: 0.0283). The KG surface is essentially flat — the acquisition function provides no useful guidance on WHERE to evaluate.

This flatness occurs because:
1. The best grid value (0.9454) is virtually identical across all fantasy observations (range: 0.9452–0.9455), even when fantasy y-values range from 0.96 to 1.42.
2. The same grid point (index 41) achieves the maximum in every fantasy model.
3. Root node observations have an attenuated effect on the network output — they must propagate through 2+ nodes to affect the objective (node 3).

### The paper's approach:
The paper's p-KGFN evaluates ANY node by sampling parent outputs from the posterior to create inputs for intermediate nodes. This is the core technical contribution and is NOT implemented here.

---

## Question 3: Would Increasing Budget Help p-KGFN?

**VERDICT: No. The root-only limitation is fundamental, not a budget issue.**

### Quantitative evidence (controlled experiment, seed=0):

I simulated adding increasing numbers of root-only observations (matching p-KGFN behavior) and compared with full evaluations (matching baseline behavior):

**Root-only observations (p-KGFN-style):**
| Extra root obs | Cost | Pred best | True val at rec | Gap from optimum |
|----------------|------|-----------|-----------------|-----------------|
| 0 | $630 | 1.020 | 0.897 | 0.209 |
| 30 | $855 | 1.042 | 1.106 | 0.000 |
| 70 | $1,155 | 1.054 | 1.106 | 0.000 |
| 280 | $2,730 | 1.050 | 1.106 | 0.000 |

**Full observations (baseline-style):**
| Extra full obs | Cost | Pred best | True val at rec | Gap from optimum |
|----------------|------|-----------|-----------------|-----------------|
| 0 | $630 | 1.020 | 0.897 | 0.209 |
| 10 | $1,330 | 1.109 | 1.062 | 0.044 |
| 20 | $2,030 | 1.109 | 1.106 | 0.000 |
| 30 | $2,730 | 1.108 | 1.106 | 0.000 |

Key findings:
1. **Root GPs saturate by ~30 extra observations ($855)**. Adding 250 more observations provides no benefit.
2. **The predicted value at the optimum plateaus at ~1.05** for root-only, vs ~1.11 for full evaluations. This 5% bias is structural — it cannot be reduced by adding more root observations.
3. p-KGFN actually finds the true optimum LOCATION earlier ($855 vs $2,030), but its MODEL of the optimum's value is persistently inaccurate due to data-starved nodes 1 and 3.

### The metric matters:
This reveals an important nuance: p-KGFN has an **exploration advantage** (finds the optimum location faster) but an **estimation disadvantage** (can't accurately value what it found). Since the benchmark tracks posterior mean (the only practical metric), p-KGFN appears to underperform despite actually solving the exploration problem.

---

## Question 4: Figure Quality Assessment

### DAG figure (pkgfn_dag.png): **Good**
- Clear node structure, cost annotations, color coding, input/output dimensions
- Minor: "Assembly"/"Forming" labels are arbitrary (not from paper)

### Cost efficiency figure (pkgfn_cost_efficiency.png): **Adequate but has metadata inconsistencies**
- Good: Primary comparison metric, equal-budget, mean ± 1 std, init cost marked
- Bad: Title says "$1,190 budget" and "5 seeds" but prompt describes $2,730 and 3 seeds — likely from an earlier run
- The error bands overlap completely — no statistical difference visible
- p-KGFN (pink) trend is flat while others improve, which correctly shows the problem but needs interpretation

### Convergence figure (pkgfn_convergence.png): **Potentially misleading**
- Comparing algorithms with different per-iteration costs on the same x-axis creates a visual bias
- p-KGFN's ~75 iterations at ~$7/iter vs baselines' 8 iterations at $70/iter are not comparable per iteration
- The title disclaimer "per-iteration costs differ" is good but easily missed
- The pink error band spans 0.4–1.0, suggesting high inter-seed variance or a data issue

### Node selection figure (pkgfn_node_selection.png): **Informative**
- Correctly reveals root-only limitation (52% node 0, 48% node 2, 0% nodes 1 and 3)
- Cost analysis panel is useful
- The 52/48 split emerges from diminishing returns as node 0 saturates

### Recommended improvements:
1. Match figure titles to actual experimental configuration
2. Add a dual-metric figure showing both posterior mean AND simple regret (true value at recommendation)
3. Add per-node GP quality metrics over the BO loop
4. Make cost efficiency the primary figure; demote convergence-vs-iteration

---

## Question 5: Improvements for Rigorous Benchmarking

### Critical (required for valid comparison):
1. **Implement intermediate node evaluation** — This is the paper's core contribution. Without it, the benchmark evaluates a crippled version of p-KGFN that can never outperform baselines in posterior-mean tracking.
2. **Add simple regret tracking** — Report `true_best - true_val_at_recommendation` alongside posterior mean. This reveals whether p-KGFN's exploration advantage is real.
3. **Increase seeds to ≥10** with statistical tests (e.g., paired Wilcoxon signed-rank) for performance comparisons. 3–5 seeds with overlapping error bands is insufficient.

### Important (improves reliability):
4. **Increase inner optimization grids**: 50 grid points for 4D optimization is very sparse. Use 200+ for posterior mean evaluation and 128+ for candidate selection.
5. **Increase num_fantasies to 16–32**: While the KG surface is genuinely flat (the issue is not noise), higher fantasy counts are standard practice and eliminate this as a confound.
6. **Validate against original implementation**: Compare a few iterations with the original `frazier-lab/partial_kgfn` repo to confirm numerical agreement.

### Desirable (improves interpretability):
7. **Add ablation: mixed evaluation strategy** — e.g., "p-KGFN with mandatory full eval every N iterations" to test whether periodically updating all node GPs rescues performance.
8. **Track per-node GP quality** (RMSE, correlation) over the BO loop to visualize the data imbalance effect.
9. **Add a KGFN baseline** — Full Knowledge Gradient for Function Networks (evaluating the complete network) to separate the value of intelligent evaluation selection from the partial evaluation mechanism.

---

## Discretionary Analytical Decisions

- Used 500-point Sobol test grid for posterior quality evaluation; different grid sizes would give slightly different RMSE/correlation values
- Used seed=0 for the single-seed controlled experiments (root saturation analysis); results may vary slightly across seeds though the qualitative conclusions are robust
- Chose coefficient of variation (CV) as the metric for KG surface flatness; alternatives like range/mean or interquartile range would yield similar conclusions
- Classified the Edison review's claimed bugs as false positives based on reading the actual source code rather than the Edison review's quoted code, which appeared to reference a different (possibly earlier) version of the files
- Used 32 fantasies for the KG distribution analysis (panel c of summary figure) as a compromise between computational cost and estimate quality
- Assessed root GP saturation at "~30 extra observations" based on the inflection point where both gap-from-optimum and predicted-best-value plateaued; this threshold is approximate
- Tested intermediate node evaluation feasibility by analyzing the node input structure rather than implementing it, to stay within the code review scope
- Used the same problem seed (seed=0) throughout the deep-dive analysis for consistency, while noting that the BO loop results used seeds 100–102 (or 100–104 in figures)