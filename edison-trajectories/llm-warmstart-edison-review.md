# Edison ANALYSIS Review of LLAMBO-Style Warmstart POC

**Task ID**: 12c6e2d1-004c-465f-94a1-2266814b276d
**Mode**: ANALYSIS (with 5 file uploads: script, figure, data, cache, visualization)
**Date**: 2026-04-10

---


# LLAMBO-Style Warmstart PoC for BOFN — Technical Review

## Implementation Quality Rating: 4/10

The code is well-structured and readable, with good software engineering practices (caching, fallbacks, seeding, separate visualization), but contains several critical methodological flaws that invalidate the experimental conclusions.

---

## 1. Is the Implementation Methodology Correct for a LLAMBO-Style Warmstart Comparison?

**Partially, but with critical flaws.**

The high-level design—query an LLM for domain-informed initial points, compare against random initialization—faithfully captures the LLAMBO concept. However, three critical implementation issues undermine the comparison:

### Issue 1: This is NOT Bayesian Optimization over Function Networks (BOFN)
The implementation fits a **single GP on Node 0 (CALPHAD) only** (line 390). Nodes 1–3 have no GP models, no network-aware acquisition function, and no ability to selectively evaluate individual nodes. The code evaluates the full pipeline end-to-end each iteration, treating it as a black-box composite function. This is standard single-task BO on one node's output, not BOFN (Astudillo & Frazier, 2021).

### Issue 2: Acquisition Function is Greedy Mean, Not Thompson Sampling
The code (lines 399–409) claims a "Thompson-sampling-like strategy" but implements: (1) generate 50 random candidates, (2) evaluate GP **posterior mean** at each, (3) pick the highest. This is pure greedy exploitation with **zero exploration**. True Thompson sampling draws a sample function from the GP posterior and optimizes over that sample. The greedy approach combined with only 50 candidates (extremely sparse in 3D) makes the BO loop nearly ineffective at finding new optima.

### Issue 3: Process/Print Parameters Are Randomized, Not Optimized
Each iteration draws random process_params and print_params (lines 356–357, 412–413). These are **not controlled or optimized**, yet sensitivity analysis shows they are 2.75× more influential on the final objective (σ=0.0165) than composition (σ=0.0060). This adds substantial unmodeled noise, drowning out the composition signal the BO loop is trying to optimize.

---

## 2. Experimental Design Issues

### Seed Sharing Leads to Degenerate Comparison
The same seed controls both the BO candidate pool AND the process/print params in both arms. Because the GP posterior converges once enough data is accumulated, **36 out of 50 BO iterations (72%) produce identical candidates and objectives** between LLM and Random arms. For seeds 1 and 2, the final objectives are bit-for-bit identical. The experiment effectively measures only whether the initial 15 points contain a good sample, not BO convergence behavior.

### Edison Composition Diversity is Near-Zero
The 15 Edison-parsed compositions have:
- Mean pairwise distance: 0.049 (vs 0.500 for random — **10× less diverse**)
- 2 exact duplicates (compositions #6 and #7)
- All compositions clustered in [83–92% Al, 7–16% Si, 0–1% Mg]
- Mg range of only 0–1 wt% (the prompt asked for "exploratory" compositions)

This extreme clustering means the GP fitted on LLM data has almost no information about the composition space outside a tiny AlSi10Mg neighborhood.

### Sample Size and Statistical Power
With only n=5 seeds:
- Initial best advantage: LLM mean = 0.5297 vs Random mean = 0.5203 (paired t-test p=0.298, not significant)
- Final best: LLM mean = 0.5355 vs Random mean = 0.5393 (paired t-test p=0.317, not significant)
- LLM win rate: 1/5 = 20%
- Neither the cold-start advantage nor the convergence disadvantage is statistically significant

### Missing Baselines
The comparison only tests LLM vs uniform random. Proper baselines should include Latin Hypercube Sampling (LHS) or Sobol sequences, which would likely outperform both by providing better space coverage than the clustered LLM compositions while being more systematic than random.

---

## 3. Is the Convergence Behavior Expected and Interpretable?

**The pattern (LLM starts better, random catches up) is qualitatively expected for warmstarting, but the quantitative details are artifacts of implementation flaws.**

The LLM cold-start advantage (+0.009 mean, ~94% of 1σ of the objective distribution, ~14% of full range) reflects a genuine signal: domain-informed compositions cluster near regions with higher CALPHAD phase fractions (100% above 0.5 threshold vs 24% for random). This is the core value proposition of LLAMBO-style warmstarting.

However, the random catch-up and eventual surpassing is NOT due to superior BO exploration. It occurs because:
1. The BO loop is nearly non-functional (greedy mean on 50 candidates = essentially random search)
2. Random initialization covers a wider space, and some random seeds happen to sample near the true optimum [0.70, 0.20, 0.10]
3. The process/print noise dominates, so getting lucky with random params matters more than composition quality
4. After 2–6 iterations, both arms select identical candidates (same seed → same candidate pool → same greedy pick)

The claim that "random catches up by iteration 4–5" is misleading—what actually happens is both arms converge to the same degenerate BO behavior, and the random arm occasionally got lucky in its initial 15 samples.

---

## 4. Implementation Quality: 4/10

**Positives (+):**
- Clean module structure with separation of concerns
- Good docstrings and CLI interface
- Edison caching mechanism for reproducibility
- Robust parsing with fallback compositions
- Reproducible seeding strategy
- Results saved to JSON for post-hoc analysis
- Separate visualization script (good practice)
- Proper use of botorch/gpytorch APIs for GP fitting
- Composition normalization (sum-to-1 constraint respected)

**Critical Issues (−):**
- Not actually BOFN (only 1 of 4 nodes modeled)
- Greedy mean acquisition mislabeled as Thompson sampling
- Uncontrolled nuisance parameters dominate the objective
- 50 candidates far too few for acquisition optimization
- 72% of BO iterations are identical between arms
- n=5 seeds insufficient for reliable inference
- No statistical tests reported in original output
- Fallback compositions include the exact CALPHAD optimum [0.70, 0.20, 0.10]
- The 0.5 phase-fraction threshold appears cherry-picked to flatter the LLM arm

---

## 5. Next Steps Evaluation

### Phase 3: Diversity Constraints — **HIGH PRIORITY ✓**
This is the most well-motivated next step given the results. Edison compositions have 10× less diversity than random, with 2 exact duplicates. The proposed ">2σ from known alloys" constraint directly addresses this. **Recommendation:** Supplement with a structured space-filling component (Sobol/LHS hybrid) rather than purely distance-based constraints.

### Phase 3: LLM-Informed GP Priors — **PREMATURE**
Setting GP priors on a broken BO loop provides no useful signal. First fix: (a) the acquisition function, (b) the multi-node GP structure, and (c) the nuisance parameter handling. Only then can GP prior quality be meaningfully evaluated.

### Phase 4: BORA-Style Trust-Weighted Stage Selection — **PREMATURE**
Requires a working BOFN with per-node models and selective evaluation capability, neither of which exist in the current implementation.

### Recommended Priority Order:
1. **P0 (CRITICAL):** Fix BO loop — proper acquisition function (EI/UCB), increase candidates to 500+, or use gradient-based acquisition optimization
2. **P1 (CRITICAL):** Implement actual BOFN — GP per node, network-aware acquisition
3. **P2 (HIGH):** Fix experimental design — add LHS/Sobol baselines, increase to 20+ seeds, add standard benchmarks (Hartmann6) for calibration
4. **P3 (HIGH):** Edison composition diversity (the proposed constraint)
5. **P4 (MEDIUM):** LLM-informed GP priors (after P0–P2)
6. **P5 (LOW):** BORA-style trust weighting (after P0–P4)

---

## Key Quantitative Findings

| Metric | Value |
|--------|-------|
| LLM initial best (mean ± std) | 0.5297 ± 0.0087 |
| Random initial best (mean ± std) | 0.5203 ± 0.0149 |
| Cold-start advantage | +0.0094 (p=0.298, n.s.) |
| LLM final best (mean ± std) | 0.5355 ± 0.0062 |
| Random final best (mean ± std) | 0.5393 ± 0.0068 |
| Final advantage | −0.0038 (p=0.317, n.s.) |
| LLM win rate (final) | 1/5 = 20% |
| BO iteration identity rate | 36/50 = 72% |
| Edison pairwise distance (mean) | 0.049 |
| Random pairwise distance (mean) | 0.500 |
| Edison exact duplicates | 2 (compositions #6=#7) |
| Global optimum (10K samples) | ~0.554 |
| Best found by any method | 0.550 |
| Process/print σ vs composition σ | 0.0165 vs 0.0060 (2.75×) |

---

## Discretionary Analytical Decisions

- Used paired t-test rather than unpaired t-test for the A/B comparison, since each seed provides a matched pair between LLM and Random arms
- Used Wilcoxon signed-rank test as a non-parametric complement to the paired t-test (noted that n=5 is at the lower boundary for this test)
- Set the "near-duplicate" threshold at pairwise distance < 0.01 for identifying Edison composition duplicates
- Used 10,000 random samples to estimate the global optimum (0.554) and objective distribution
- Used Dirichlet(1,1,1) for generating random simplex samples in the diversity comparison (equivalent to uniform sampling on the simplex)
- Computed Cohen's d for effect size using the pooled standard deviation formula
- Chose σ (standard deviation) of the full-pipeline objective as the normalization factor for contextualizing effect sizes
- In the sensitivity analysis, fixed process/print parameters at 0.5 (midpoint) rather than at another value

