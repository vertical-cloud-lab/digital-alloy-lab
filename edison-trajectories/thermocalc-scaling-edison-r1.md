# Edison Review: Thermo-Calc Scaling Strategy (Round 1)

Task ID: 1cfb7464-dd88-4c45-ac08-3bdecfce475b


# Critical Evaluation of thermocalc-scaling-strategy.md

## OVERALL GRADE: B+ (7/10)

The strategy document is a well-structured starting point with sound high-level architecture (tiered surrogates, phased ramp-up, BOFN framework preservation), but has significant gaps in literature grounding, dimensionality analysis, and several technical details that need correction before implementation.

---

## Answers to the 8 Specific Questions

### Q1: Is SVGP the right choice for the TC node?

**Verdict: Good but not optimal. SVDKL (Stochastic Variational Deep Kernel Learning) should be the primary recommendation.**

SVGP is the *safest* choice due to native BoTorch/GPyTorch integration, but CALPHAD data has sharp phase boundaries (derivative discontinuities) that are poorly captured by stationary kernels (Matérn, RBF). The strategy lists DKL as "Option A" but then recommends SVGP as primary — this is backwards. SVDKL (Wilson et al., NeurIPS 2016, arXiv:1611.00336) combines a neural network feature extractor with inducing-point GP, handling non-stationarity via learned features while preserving the GP posterior interface needed by BOFN acquisition functions. It scales to 100K+ with minibatch training and is native to GPyTorch.

Additionally, the published CALPHAD ML surrogate literature (which the strategy cites none of) shows that Random Forests trained on 480 million CALPHAD data points outperform DNNs for interpolation (npj Comp. Mat. 2024, DOI:10.1038/s41524-024-01335-1). For a fast initial surrogate, RF + conformal prediction intervals is a practical "fast track" before implementing SVDKL.

**Recommendation:** PRIMARY: SVDKL → SECONDARY: SVGP with anisotropic Matérn → FAST TRACK: RF + conformal for initial phases.

### Q2: Published works on scaling BO surrogates for CALPHAD data?

**Verdict: Yes — substantial literature exists, but the strategy cites NONE of it.**

Key missing references:
- npj Comp. Mat. (2024): 480M CALPHAD data points comparing RF vs DNN for phase fraction prediction (DOI:10.1038/s41524-024-01335-1)
- Sundar et al. (2025): Directly combines CALPHAD with BO for alloy discovery (DOI:10.1557/s43578-024-01489-0)
- Liu, An & Sun (2023): "Large CALPHAD Model" — 97% accuracy for FeNiCrMn system (arXiv:2311.07174)
- Conway & Ghassemali (2022): HT-CALPHAD review with grid sizing (DOI:10.3389/fmats.2022.889771)
- Klaver et al. (2018): Brute-force CALPHAD scanning with Thermo-Calc (DOI:10.3390/e20120911)

The 100K scale proposed in the strategy is modest compared to published 480M-point datasets. The strategy should cite these works to demonstrate field awareness.

### Q3: Is multi-fidelity the right framing?

**Verdict: Partially correct — two critical flaws.**

**Flaw 1: CALPHAD is deterministic.** Standard MF-GPs assume noise at all fidelity levels. CALPHAD returns the exact same answer every time. The strategy should use the Kennedy-O'Hagan autoregressive model: y_exp(x) = ρ·y_TC(x) + δ(x) + ε, which naturally separates the deterministic TC output from the stochastic experimental residual. In BoTorch, set train_Yvar ≈ 1e-8 for the TC fidelity.

**Flaw 2: MFBO doesn't always help.** Sabanza Gil et al. (Nature Comp. Sci. 2025, DOI:10.1038/s43588-025-00822-9) systematically show that MFBO benefits depend critically on the correlation between fidelities and the cost ratio. The strategy should warn that if TC predictions don't correlate well with experimental outcomes (e.g., because equilibrium CALPHAD ≠ rapid solidification), MF may not help. Additionally, the "fidelity gap" here is not just noise — it's fundamentally different physics (equilibrium thermodynamics vs. far-from-equilibrium solidification).

### Q4: Batch BO strategies for rate-limited throughput?

**Verdict: Phase 3 is underdeveloped. Asynchronous BO should be the primary strategy.**

When compute is free but rate-limited by fairshare: (1) cost-aware acquisition (p-KGFN cost weighting) is irrelevant for TC-only simulations; (2) the constraint is wall-clock time, not budget; (3) the goal is maximum parallelism.

The strategy mentions async BO as a bullet point but should make it the centerpiece. Key references:
- Alvi et al. (ICML 2019): Async batch BO with improved local penalization — handles jobs finishing at different times
- aphBO-2GP-3B (arXiv:2003.09436): Specifically designed for HPC batch BO with fairshare constraints
- Fantasy-based async: Treat pending evaluations as fantasies via model.fantasize(), condition on both completed and fantasized observations

TC simulations have variable runtime (seconds to hours depending on phase complexity), so synchronous batching wastes time waiting for the slowest job. Async BO reclaims this time.

### Q5: Major gaps or incorrect assumptions?

Six significant gaps identified:

1. **CALPHAD outputs are multi-dimensional** (CRITICAL): The strategy implies a single-output surrogate, but TC produces phase fractions (vector), liquidus/solidus, Scheil paths, driving forces, etc. Each needs its own surrogate or a multi-task learning approach. Recommend reducing to 2-3 key scalars: ΔT_solidification, f_primary_phase, CSC.

2. **TC simulation failures are systematic, not random** (HIGH): Failures cluster at complex phase boundaries — exactly where the surrogate needs to be most accurate. "Impute with nearest-neighbor" would mask the most physically interesting regions. Recommend modeling convergence as a separate binary classifier.

3. **No validation protocol** (HIGH): "Monitor CRPS" is too vague. Need: 10% held-out test set, specific alarm thresholds, retraining triggers, and fresh-evaluation checks.

4. **The "Core Insight" is overstated** (MEDIUM): Node-level surrogates are just how BOFN works. The actual insight is: CALPHAD node data will grow 100× faster than other nodes, creating a heterogeneous-scale network.

5. **Temperature treated as "just another dimension"** (MEDIUM): Phase boundaries are much sharper in temperature than composition. Consider separate surrogates for temperature regimes or anisotropic kernels.

6. **No data storage architecture** (MEDIUM): "HDF5 or Parquet" is insufficient for 100K+ multi-output evaluations with provenance tracking.

### Q6: Alternatives to GP-based BOFN?

**Verdict: GP-based BOFN is the right framework. No published work validates non-GP surrogates within function networks.**

The closest alternative is BONSAI (Kudva & Paulson, 2025, arXiv:2510.03893), which uses Thompson sampling-based acquisition for networked systems. This scales better than KG for large networks and is worth considering if p-KGFN proves too expensive for the 9-node DAG.

A compelling alternative given free compute: the "Two-Shot" approach (Paramore et al. 2024, arXiv:2405.07130) — run CALPHAD exhaustively on the full 170K grid first, then use the complete dataset as a deterministic lookup table for Node 0 (no surrogate needed). Apply BO only to the experimental nodes downstream.

### Q7: Simplex handling for compositions?

**Verdict: Drop-one-variable approach (Al = balance, optimize Mn, Cr, Zr) is standard and acceptable.**

Improvements to consider:
- **ILR (Isometric Log-Ratio) transform** (Egozcue et al. 2003): Maps simplex to unconstrained R^(d-1), eliminating boundary effects. Worth testing as an ablation.
- **Xian et al. (Digital Discovery 2025, DOI:10.1039/D5DD00080G)**: Feature gradient approach for efficient acquisition function maximization on composition spaces — scales linearly with component count.
- **Ax linear constraints**: Native support for sum_i x_i ≤ 1, most practical BoTorch/Ax-native approach.

### Q8: Practical dimensionality and TC simulation coverage for Al-Mn-Cr-Zr?

**Verdict: The strategy's "10K-50K" target may be an overestimate depending on composition bounds.**

Practical dimensionality: 3 free composition variables + 1 temperature = 4D.

Computed coverage (exact calculations):
- **Full simplex at 1 at.%**: 176,851 compositions × 10 temps = **1,768,510** → needs scalable surrogates
- **Full simplex at 2 at.%**: 23,426 × 10 temps = **234,260** → needs scalable surrogates
- **Al-rich restricted (Al ≥ 85%) at 1 at.%**: 526 × 10 temps = **5,260** → exact GP suffices!
- **Al-rich restricted at 0.5 at.%**: 3,476 × 10 temps = **34,760** → borderline, exact GP possible
- **Al-rich restricted at 0.5 at.% × 50 temps**: **173,800** → needs scalable surrogates

**Critical finding:** If this is an Al-base alloy (Al ≥ 85%), the restricted composition region may be small enough that standard exact GP suffices (n < 5K at 1 at.% resolution). The strategy MUST define composition bounds before designing the surrogate architecture.

**Recommendation:** Confirm with PI whether this is Al-rich alloy design or broader exploration. If Al-rich, start with exact GP and upgrade to SVDKL only if the composition range expands.

---

## Priority-Ordered Actionable Improvements

### PRIORITY 1 (Do immediately):
1. **Add composition bounds section** — define Al-Mn-Cr-Zr ranges; this determines whether SVGP/SVDKL is needed at all
2. **Change primary surrogate to SVDKL** — better handles phase boundary non-stationarity while preserving GP posterior interface
3. **Add multi-output handling** — specify that TC produces N outputs, each needing a surrogate (or reduce to 2-3 key scalars)
4. **Expand async BO section** — make it the primary Phase 3 strategy with citations to Alvi et al. (ICML 2019)

### PRIORITY 2 (Within 1 week):
5. **Add 6 missing literature citations** (see Q2 above)
6. **Fix multi-fidelity section** — address deterministic CALPHAD, add Sabanza Gil warning, distinguish physics mismatch from noise
7. **Add validation protocol** — 10% held-out test set, CRPS/coverage thresholds, retraining triggers
8. **Consider "Two-Shot" alternative** — exhaustive TC grid then BO only for experiments

### PRIORITY 3 (Nice to have):
9. Add ILR transform as an ablation for simplex handling
10. Mention BONSAI as alternative acquisition framework
11. Add TC failure modeling (binary classifier)
12. Specify HDF5/Parquet schema for TC output storage

---

## Discretionary Analytical Decisions

- **Scored document quality on 8 dimensions using a 1-10 scale** — the specific scores (e.g., "Literature Coverage: 3/10") reflect my judgment of how thoroughly each aspect is addressed relative to the available literature, not a standardized rubric
- **Used Al ≥ 85% as the "restricted" composition bound** — typical for wrought Al alloys, but the actual bound should come from the PI; the specific choice of 85% affects coverage calculations significantly
- **Used 10 temperature points as the baseline multiplier** — actual temperature resolution depends on the physics being captured (solidification vs. solid-state precipitation); could reasonably be 5-100 temperatures
- **Weighted SVDKL over SVGP based on the phase boundary non-stationarity argument** — this is a judgment call; if the Al-Mn-Cr-Zr system has smooth phase fields without sharp boundaries, SVGP with Matérn would be adequate
- **Rated the "Two-Shot" exhaustive grid approach as Priority 2 rather than Priority 1** — given free compute, some reviewers might argue this should be the default approach, eliminating the need for a TC node surrogate entirely
- **Classified TC simulation failures as "systematic, not random"** based on CALPHAD computational behavior — some TC databases/compositions may actually have random numerical failures, in which case imputation would be more appropriate
- **Assessed the ILR transform as "nice to have" rather than essential** — for a 4-component system, boundary effects are moderate; for 5+ components, ILR becomes more important
- **Graded the document B+ (7/10)** — the exact grade is subjective; the document has strong architectural ideas but needs significant literature grounding and technical corrections before implementation
