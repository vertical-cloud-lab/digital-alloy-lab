
# v3 LLAMBO-Style Warmstart for BOFN — Edison ANALYSIS Review

**Edison task**: `11e2d390-832c-4c47-841f-91c80dfe3c73` (ANALYSIS mode)
**Rating**: 7/10 (up from 6/10 in v2, 4/10 in v1)
**Files reviewed**: warmstart script v3, 3-panel convergence figure, results JSON, visualization script

---

## What v3 Fixed (Improvements Over v2)

1. **CRITICAL FIX: Paired process/print params** — All 3 arms per seed now share identical non-composition inputs (lines 724-727). This ensures composition initialization is the ONLY variable differing between arms. This was the most important fairness correction.

2. **Per-seed LLM perturbation** — `perturb_compositions(base_comps, seed, noise_scale=0.03)` creates meaningful per-seed variation. LLM initial_best std = 0.256, comparable to Random (0.219). No longer a constant set across seeds.

3. **Harder benchmark** — CALPHAD scale=15 (vs 8), softplus (vs sigmoid), noise_std=0.01. These make the problem more discriminative.

4. **Reduced n_initial=8** (from 15) — Extends the cold-start regime. BOFN standard is 2(d+1)=16 for 7D, so 8 is deliberately low, which is appropriate for testing warmstart.

5. **Diversity diagnostics** — Reports mean pairwise distance (LLM=0.193, Random=0.373, LHS=0.550) and min distances. Honest about LLM clustering.

6. **More honest reporting** — Win rates of 55% candidly reported.

---

## Quantitative Results Summary

### Cold-Start Advantage (Strong, Significant)
- LLM vs Random initial best: Δ = +0.356, t(19) = 6.00, **p < 0.00001**, Cohen's d = **1.34** (very large)
- LLM vs LHS initial best: Δ = +0.321, t(19) = 5.56, **p = 0.00002**, Cohen's d = **1.24**
- LLM compositions yield 75.6% of initial points with CALPHAD phase fraction > 0.5, vs 10.0% for Random and 13.8% for LHS

### Convergence Advantage (Negligible, Not Significant)
- LLM vs Random final best: Δ = +0.028, t(19) = 0.32, **p = 0.756**, Cohen's d = 0.07
- LLM vs LHS final best: Δ = +0.082, t(19) = 0.85, **p = 0.406**, Cohen's d = 0.19
- Win rate 55% (11/20) vs both baselines — binomial test p = 0.412, consistent with chance
- Would require ~1,600 seeds to detect d=0.07 at 80% power — the convergence effect is negligible

### Advantage Dissipation Timeline
- Significant (p<0.05) through **iteration 8** (8 BO iterations after init)
- Non-significant at iteration 9 (p=0.18) and iteration 10 (p=0.76)
- Effect size decays from d=1.34 (init) → d=0.07 (final) — complete dissipation

### Sample Efficiency (The Real Story)
- **AUC (Area Under Cumulative Best)**: LLM=21.04, Random=18.11, LHS=17.88
  - LLM vs Random: **+16.2%**, t(19)=3.99, **p=0.0008**, Cohen's d=0.89
  - LLM vs LHS: **+17.7%**, t(19)=4.20, **p=0.0005**, Cohen's d=0.94
- **Iterations to Y≥2.0**: LLM=2.6 (mean among reached), Random=6.5, LHS=6.2
  - LLM reaches threshold **~4 iterations sooner** than baselines

---

## Top 3 Remaining Issues

### Issue 1: Synthetic Benchmark Circularity (HIGH Severity)
The ground-truth optimum [0.7, 0.2, 0.1] is suspiciously aligned with well-known Al-Si-Mg alloy compositions. The fallback LLM compositions include points at L2 distance 0.071 from the optimum (CALPHAD output = 0.928). This creates a circular argument: the optimum was designed to match real metallurgy → the LLM suggests real metallurgical compositions → the LLM "wins" because the optimum was placed where domain knowledge would direct it. This cannot distinguish "LLM warmstart is useful" from "the benchmark was designed to reward LLM knowledge."

**Fix**: Add 2-3 benchmarks where the optimum is NOT aligned with domain knowledge (randomly shifted/rotated CALPHAD peaks, multi-modal objectives, or use Astudillo & Frazier's original benchmarks).

### Issue 2: No True BOFN Acquisition Function (MEDIUM-HIGH Severity)
The implementation uses Thompson sampling with 2000 random candidates, NOT the EI-FN or KG-FN acquisition functions from Astudillo & Frazier (2021). Thompson sampling over random candidates in 7D is weak (2000^(1/7) ≈ 3 points per dimension). Seeds 9 and 15 show complete exploration failure (stuck at ~1.5 for all 10 iterations). The original BOFN uses gradient-based optimization of EI-FN. You cannot claim to show "LLM warmstart helps BOFN" when you're running a different (simpler) algorithm. Additionally, the code comment on line 19 says "5000 candidates" while the actual code uses 2000.

**Fix**: Implement EI-FN from the BOFN paper, or at minimum use gradient-based Thompson sampling (L-BFGS-B on the Thompson sample). Use BoTorch's infrastructure for function networks.

### Issue 3: Results Framing — "Convergence Advantage" is Misleading (MEDIUM Severity)
The claimed "persistent advantage at convergence" (+0.028, 55% win rate) is statistically indistinguishable from zero. The honest finding is that LLM warmstart provides a **large, significant sample efficiency gain** (d=0.89 on AUC, d=1.34 on cold-start) that fully dissipates by iteration 10. This is actually a good and publishable result — it matches LLAMBO's theoretical prediction. But it must be framed as "sample efficiency" not "convergence advantage."

**Fix**: Report AUC and iterations-to-threshold as primary metrics. Frame the contribution as sample efficiency gain in the cold-start regime, consistent with LLAMBO's findings.

---

## Comparison to Astudillo & Frazier (2021)

Per the original BOFN paper and literature confirmation:
- BOFN uses **2(d+1) uniformly random** initial points (uninformed design)
- BOFN uses **EI-FN / KG-FN** acquisition functions with gradient-based optimization
- BOFN uses structured GPs that exploit the DAG to capture inter-node correlations

This v3 correctly implements: per-node GPs, DAG propagation through posteriors.
This v3 does NOT implement: BOFN's acquisition function, structured covariance, gradient-based candidate optimization.

The concept of replacing BOFN's random initialization with LLM-informed compositions is well-motivated and aligns with LLAMBO's framework. However, the BO loop itself is a simplified approximation of BOFN, not BOFN itself.

---

## Recommended Next Steps (Publication Priority)

**Required**: (A) Implement proper EI-FN acquisition function; (B) Add non-circular benchmarks; (C) Frame results as sample efficiency gain
**Strongly recommended**: (D) Increase BO iterations to 20-30; (E) Use gradient-based TS optimization; (F) Fix comment discrepancy (line 19); (G) Report AUC and time-to-threshold as primary metrics
**Nice to have**: (H) Test with actual Edison/LLM compositions; (I) Ablation over n_initial; (J) Pair BO exploration seeds across arms

---

## Discretionary Analytical Decisions

- Used paired t-tests (rather than unpaired or nonparametric) as the primary comparison method, justified by the paired experimental design (shared process/print params per seed)
- Also reported Wilcoxon signed-rank tests as nonparametric confirmation
- Used one-sided p-values for per-iteration significance analysis (H1: LLM > baseline), two-sided for overall final comparison
- Computed Cohen's d using the standard deviation of paired differences (paired d), not pooled SD
- Used AUC via trapezoidal integration (np.trapz) as the sample efficiency metric rather than alternatives like mean rank or regret
- Set the "never reached" censoring value at 11 (one beyond max iterations) for iterations-to-threshold analysis
- Used 95% confidence intervals (±1.96 SE) for convergence curve visualization
- Assessed power using normal approximation to the paired t-test
- Interpreted the 55% win rate against a null of 50% using an exact binomial test (one-sided)
