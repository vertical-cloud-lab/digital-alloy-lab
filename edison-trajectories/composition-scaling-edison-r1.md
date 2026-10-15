# Edison Review: Composition Scaling Analysis (Round 1)

Task ID: f6c3ee31-dcf7-4d2e-b805-e51c82236177


# Review of CALPHAD Composition Space Scaling Analysis

## Overall Grade: A−

This is a strong, well-structured analysis that demonstrates genuine expertise in both CALPHAD thermodynamics and scalable Bayesian optimization. The core framework (tiered surrogates, Two-Shot vs. Hybrid vs. Fully Adaptive decision tree, async BO for rate-limited HPC) is methodologically sound. The analysis correctly identifies the key scaling transitions and provides practical, implementable recommendations. However, it contains a few numerical errors, is missing several important references, and omits a number of considerations critical for high-dimensional composition spaces.

---

## 1. Combinatorial Calculations (9/10)

**Al-rich region (Al ≥ 85%, 1 at.% resolution): ALL CORRECT ✓**
The stars-and-bars formula N = C(15 + d−1, d−1) is correctly stated and all 8 rows in the scaling table are verified:
- 3 components → 136 ✓
- 4 components → 816 ✓
- 5 components → 3,876 ✓
- 6 components → 15,504 ✓
- 7 components → 54,264 ✓
- 8 components → 170,544 ✓
- 9 components → 490,314 ✓
- 10 components → 1,307,504 ✓

**0.5 at.% resolution: ALL CORRECT ✓** (S=30 integer steps, all 4 rows verified)

**Full simplex (no Al-rich constraint): 1 of 3 WRONG ✗**
- d=4: claimed 176,851, correct C(103,3) = 176,851 ✓
- d=5: claimed 4,421,275, correct C(104,4) = **4,598,126** ✗ (off by 176,851 = 3.8%)
- d=6: claimed 91,962,520, correct C(105,5) = **96,560,646** ✗ (off by 4,598,126 = 4.8%)

The error pattern: the document used C(103, k) for d=5 and C(104, k) for d=6, suggesting an off-by-one in the first argument of the binomial coefficient (using n=99+d−1 instead of n=100+d−1 for d≥5). The qualitative conclusion that "full simplex numbers are much larger" still holds.

**Cross-document inconsistency:** thermocalc-scaling-strategy.md claims 3,476 compositions for 4-component, 0.5 at.% resolution. The correct value is **5,456** = C(33,3). The value 3,476 doesn't correspond to any standard combinatorial formula with integer parameters. The composition-scaling-analysis.md has the correct number (5,456).

---

## 2. Surrogate Tier Thresholds (8/10)

**Thresholds are reasonable but need clarification.** The document proposes:
- n < 5K → Exact GP (SingleTaskGP)
- 5K < n < 50K → SVDKL
- n > 50K → SVDKL + minibatch or RF + conformal

These thresholds are sensible, supported by the computational analysis:
- At 5K points: kernel matrix = 0.2 GB, Cholesky ≈ 1s → comfortable for exact GP
- At 50K points: kernel matrix = 20 GB, Cholesky ≈ 14 min → infeasible for iterative retraining

**Key ambiguity:** The surrogate tier labels in the main scaling table are assigned based on *composition count*, not total training points (compositions × temperatures). This matters critically:
- 5-component system: 3,876 compositions but 38,760 total sims (×10 temps). Labeled "Exact GP (upper limit)" based on compositions, but at 38,760 total training points, the kernel matrix is ~12 GB and Cholesky takes ~6.5 min. This should be labeled "Borderline → SVDKL" if temperature is a GP input.
- If the plan is to model at each temperature independently or use temperature as a structured input, the composition count is the right metric. This architectural choice needs to be made explicit.

**Recommendation:** Add a note specifying whether the surrogate operates over (composition) or (composition × temperature), and adjust tier labels accordingly.

---

## 3. Decision Tree Calibration (8/10)

**The three-regime structure is well-calibrated:**
- **3–5 components → Two-Shot:** Correct. ≤3,876 compositions can be exhaustively enumerated in 2–39 days on BYU HPC with rate limiting. This is the practical sweet spot for "free compute."
- **6 components → Hybrid:** Correct. 15,504 compositions = 1–4 weeks. Dense coverage is borderline feasible but adaptive infill improves efficiency.
- **7+ components → Fully Adaptive:** Correct. 54,264+ compositions → months for exhaustive coverage. Adaptive sampling is the only practical path.

**Missing from the decision tree:**
1. **Temperature grid resolution:** The tree assumes 10 temperatures throughout. For Scheil solidification paths (which the strategy document itself recommends), 50–100 temperature steps may be needed. A 5-component system with 50 temps = 193,800 total points — this shifts it from "Two-Shot viable" to "Fully adaptive required." The decision tree should include temperature resolution as a second axis.
2. **Dimension screening:** For 7+ component systems, a preliminary screening step (e.g., Morris method or Sobol sensitivity analysis on an initial TC surrogate) could identify the 2–4 active composition dimensions, effectively reducing the problem back to the Two-Shot regime. This could save months of adaptive sampling.

---

## 4. Missing Considerations for High-Dimensional Composition Spaces (6/10)

The document correctly identifies the curse of dimensionality, lengthscale estimation challenges, and increased phase boundary complexity. However, seven important topics are missing:

1. **Simplex-aware sampling:** The document recommends "Sobol sequence on the (d−1)-simplex" for initialization, but standard Sobol/LHS does NOT naturally respect the simplex constraint. Projecting Sobol points onto the simplex via normalization destroys the space-filling property. Need simplex-specific designs: Dirichlet sampling, simplex LHS (Petelet et al. 2010), or Sobol + softmax transformation.

2. **Phase diagram topology scaling:** The Gibbs phase rule (F = C − P + 2) means that with 8 components at fixed T and P, up to 8 phases can coexist simultaneously. The number of distinct phase regions and the complexity of phase boundaries grow combinatorially. The document should quantify how this affects minimum inducing point count for SVDKL and minimum training set size per phase region.

3. **Compositional symmetry/exchangeability:** Many minor alloying elements (e.g., Ti, Zr, Hf) have similar thermodynamic roles. Exploiting partial exchangeability via group-invariant kernels or parameter tying could substantially reduce effective dimensionality.

4. **Sparsity of interesting regions:** In high-dimensional spaces, the fraction of compositions satisfying target properties (single-phase FCC, low cracking susceptibility) becomes very small. The document should discuss trust-region methods (TuRBO is mentioned briefly but uncited) for efficiently navigating sparse objective landscapes.

5. **Boundary effects in the Al-rich corner:** The Al ≥ 85% constraint creates a simplex corner, not a full simplex. The ILR transform, designed for the simplex interior, performs poorly near zero-composition boundaries where log(0) is undefined. The drop-one-variable approach may actually be preferable for this constrained corner geometry.

6. **Multi-output correlation validation:** With 7+ components, the correlation structure between TC outputs (ΔT_solidification, f_primary_phase, CSC) may be non-stationary across composition space. The document recommends MultiOutputGP if "correlations are strong" but provides no protocol for validating this.

7. **CALPHAD database validity boundaries:** As more elements are added, the fraction of the composition space relying on extrapolated (unassessed) thermodynamic parameters increases dramatically. The surrogate may be learning database extrapolation artifacts rather than real physics. This should be quantified and addressed.

---

## 5. Async BO Strategy for BYU HPC (8/10)

**The core strategy is sound and well-referenced:**
- ✓ Async > sync for variable-runtime TC sims (correctly identified)
- ✓ Fantasization via model.fantasize() (standard BoTorch approach)
- ✓ aphBO-2GP-3B reference (designed for HPC batch BO with fairshare)
- ✓ Warm-start SVDKL retraining (computationally sensible)
- ✓ Rate-limit awareness and fairshare-aware batch sizing

**Missing elements:**
1. **Cost-aware acquisition:** TC runtime varies by orders of magnitude across compositions (seconds for simple equilibria, hours for complex multi-phase regions). The async BO should maximize information gain per unit compute time, not just information gain per query. BoTorch supports cost-weighted acquisition functions.

2. **Stopping criteria:** No convergence criterion is discussed. For the "free compute" scenario, suggest: stop when max(EI) < ε for N consecutive iterations, or when max(σ_posterior) in the design region drops below a target threshold.

3. **Fantasization overhead:** With 50–100 concurrent pending TC jobs, fantasization becomes expensive. The document should specify a maximum concurrent pending count and discuss when to fall back to cheaper methods (Kriging Believer, local penalization).

4. **Checkpoint and recovery:** Weeks-long adaptive campaigns on HPC require explicit checkpoint/recovery for surrogate state, pending job tracking, and partial batch completions.

5. **p-KGFN computational cost:** p-KGFN is theoretically optimal for function networks but computationally expensive. For the async HPC scenario, the document should compare against simpler alternatives (per-node Thompson Sampling, BONSAI) and justify the added complexity.

---

## 6. Literature Coverage (7/10)

**All 11 cited references verified correct** via CrossRef and arXiv APIs. One minor author order issue: "Conway & Ghassemali (2022)" should be "Ghassemali & Conway (2022)" per the published paper.

**9 important missing references:**

| Reference | Why it should be cited |
|:---|:---|
| Balandat et al. (2020), BoTorch, NeurIPS, arXiv:1910.06403 | Core framework used throughout; SingleTaskGP, optimize_acqf are BoTorch APIs |
| Gardner et al. (2018), GPyTorch, NeurIPS, arXiv:1809.11165 | Used in SVDKL code; ApproximateGP, VariationalStrategy are GPyTorch classes |
| Eriksson et al. (2019), TuRBO, NeurIPS, arXiv:1910.01739 | "turbo-like trust region" referenced but paper uncited |
| Kennedy & O'Hagan (2001), JRSS-B, DOI:10.1111/1467-9868.00294 | Autoregressive MF model explicitly referenced but paper uncited |
| Astudillo & Frazier (2019), arXiv:1906.01537 | BOFN foundational paper — the DAG-based BO framework is central |
| Aitchison (1986), Springer, DOI:10.1007/978-94-009-4109-0 | Foundational work for ILR transform discussed in both documents |
| Sundman et al. (1985), Calphad, DOI:10.1016/0364-5916(85)90021-5 | Thermo-Calc foundational paper — the central simulation tool |
| Otis & Liu (2017), JORS, DOI:10.5334/jors.140 | pycalphad mentioned as COST507 fallback but uncited |
| Lookman et al. (2019), npj Comp. Mat., DOI:10.1038/s41524-019-0153-8 | Foundational review on active learning for materials |

Additionally recommended: Honarmandi et al. (2019) for Bayesian UQ with CALPHAD, Talapatra et al. (2019) for experiment design frameworks.

---

## Top 5 Priority Improvements

1. **Clarify compositions vs. total sims** in surrogate tier assignment. Add explicit note about whether temperature is a GP input dimension or handled separately.

2. **Add simplex-aware sampling** discussion. Replace "Sobol sequence on the (d−1)-simplex" with a specific valid method (Dirichlet sampling, simplex LHS, or Sobol + softmax).

3. **Add dimension screening** for 7+ components. Morris method or Sobol sensitivity analysis on an initial TC surrogate to identify active dimensions before committing to high-dimensional BO.

4. **Add cost-aware acquisition** for async BO. TC runtime varies by orders of magnitude; maximize information per unit compute time.

5. **Add stopping criteria** and checkpoint/recovery protocol for adaptive campaigns running weeks on HPC.

---

## Discretionary Analytical Decisions

- Assessed GP computational feasibility using approximate 50 GFLOPS throughput for dense Cholesky factorization on a single modern CPU — actual performance varies with hardware, BLAS implementation, and numerical conditioning
- Used 32 GB as a practical RAM threshold for kernel matrix storage based on typical HPC node specifications; BYU HPC may have larger memory nodes available
- Evaluated the "Exact GP (upper limit)" label for 5-component systems as optimistic rather than wrong, since the appropriateness depends on whether temperature is included as a GP input dimension (an architectural choice not fully specified in the document)
- Classified the full-simplex count errors (3.8% and 4.8%) as minor rather than critical because they don't change the qualitative conclusions about the full simplex being orders of magnitude larger than the Al-rich corner
- Identified the 3,476 figure in thermocalc-scaling-strategy.md as an error based on failure to match any standard combinatorial formula, though it could potentially correspond to a deliberately different constraint set not documented
- Weighted missing references by importance: framework papers (BoTorch, GPyTorch) ranked higher than domain-specific papers because the analysis explicitly uses those APIs
- Assessed surrogate tier boundaries using a single-GP-over-all-data model as the default interpretation; the analysis could also be interpreted as recommending one GP per temperature bin, which would shift all thresholds upward
