# BOFN + LLM-BO Synthesis: Toward LLM-Augmented Function Network Optimization for Alloy Discovery

## Overview

This document synthesizes three research threads into a unified framework for VCL's alloy discovery pipeline:

1. **BOFN in BoTorch** (§1) — Verified working implementation of Bayesian Optimization over Function Networks
2. **Meta AE LLM+BO Literature** (§2) — Survey of LLM integration methods for Bayesian optimization
3. **The Union: LLM-BOFN** (§3) — Proposed architecture combining LLM priors with function network optimization
4. **Benchmark Task Design** (§4) — What benchmarks are needed to build confidence before deployment

---

## §1. BOFN in BoTorch — Verified Working

### Implementation

A 4-node function network modeling the VCL alloy discovery pipeline has been implemented and verified working in BoTorch:

```
Node 0: CALPHAD screening     (composition → phase fractions)         Cost: ~$1
Node 1: Powder production      (phase fractions + params → quality)    Cost: ~$200
Node 2: LPBF printing          (powder quality + params → density)     Cost: ~$800
Node 3: Characterization       (part density → mechanical properties)  Cost: ~$300
                                                                  Full: ~$1,301
```

**Per-node GP models**: Each node uses a `SingleTaskGP` with:
- `Normalize` input transform (maps inputs to [0, 1] for numerical stability)
- `Standardize` outcome transform (zero mean, unit variance)
- Hyperparameters optimized via `ExactMarginalLogLikelihood`

**Composite forward pass**: GP posterior means are propagated through the DAG. For uncertainty quantification, Monte Carlo samples from each node's posterior can be propagated through downstream nodes.

**Tested configuration**:
- `botorch==0.17.2`, `torch==2.10.0`
- 30 training points per node
- Predictions closely match synthetic ground truth
- See `benchmarks/bofn_demo.py` for complete implementation

### Cost-Aware Partial Evaluation (p-KGFN Concept)

The cost-aware variant demonstrates the economic advantage of partial evaluation:

| Metric                                 | Value             |
| :------------------------------------- | :---------------- |
| Candidates screened (CALPHAD only)     | 50                |
| Promoted to full pipeline              | 6                 |
| CALPHAD screening cost                 | $50               |
| Downstream cost (promoted only)        | $7,800            |
| **Total cost with screening**          | **$7,850**        |
| Naive cost (all through full pipeline) | $65,050           |
| **Savings**                            | **$57,200 (88%)** |

The key insight: running 44 extra CALPHAD screens costs $44 (vs. $57,200 if those had been full pipeline evaluations). The downstream cost for promoted candidates excludes the already-paid CALPHAD cost to avoid double-counting. CALPHAD's 1000× lower cost per evaluation makes aggressive upstream screening highly cost-effective.

### Dimensionality Reduction

Standard BO on this pipeline would operate in $d = 3 + 2 + 2 = 7$ dimensions (composition + process params + print params). BOFN decomposes this into four GPs operating in 3, 3, 3, and 1 dimensions respectively, dramatically improving sample efficiency.

---

## §1b. Expanded DAG — Realistic LPBF Parameter Dimensionality

*Updated based on Edison Scientific reviews (tasks `d0ad1eea`, `6025bdcf`, `98edd2c3`) and developments in PR #20 (LPBF 36-parameter dimensionality), PR #26 (GA scale-up), PR #30 (AM test structures).*

### The Problem

PR #20 established that LPBF involves ~36 processing parameters across 7 categories (beam/energy, scan strategy, layer/build, powder/feedstock, atmosphere, thermal management, machine-specific). Our initial 4-node demo used only 2 LPBF parameters (laser power and scan speed) — a gross oversimplification that would not support real alloy discovery.

### Refined Architecture: Sub-Node Decomposition of LPBF (v2, Edison-reviewed)

Edison review #1 (`98edd2c3`, 60K chars, 30+ citations) identified critical gaps in the initial expanded DAG. The v2 architecture incorporates all critical and high-priority fixes:

```
Node 0:  CALPHAD screening      (composition d=3 → phase_frac + solid_range + CSC d=3) [$1]
Node 1a: Powder PSD             (phase_frac + solid_range + atom_params d=4 → D50 d=1) [$50]
Node 1b: Powder flowability     (phase_frac + atom_params d=3 → Hausner_ratio d=1)     [$30]
Node 1c: Powder apparent density (phase_frac + atom_params d=3 → density d=1)          [$20]
Node 2a: Energy delivery        (D50 + app_dens + P + v + σ d=5 → melt_pool d=2)      [$100]
Node 2b: Scan strategy          (mp_W + mp_D + hatch + rot + contour d=5 → quality d=1) [$100]
Node 2c: Thermal management     (quality + mp_D + preheat + dwell d=4 → stress d=1)    [$50]
Node 2d: Integration            (melt_pool_depth + quality + stress d=3 → density d=1) [$200]
Node 3:  Characterization       (part_density d=1 → YS + elongation d=2)               [$300]
```

**v2 changes** (all from Edison review `98edd2c3`):
- **Node 0**: +CSC output (Clyne-Davies cracking susceptibility) — printability metric
- **Node 1a**: +solidification range input from CALPHAD (alloy thermodynamics → atomization)
- **Node 2a**: apparent density replaces flowability (Field et al. 2020, packing/absorptivity proxy)
- **Node 2b**: +melt_pool_depth (CRITICAL — LOF criteria need both W and D, Wang et al. 2021)
- **Node 2c**: +melt_pool_depth (thermal gradient/intensity proxy, Bergmueller et al. 2023)
- **Node 3**: +elongation output (strength-ductility tradeoff for alloy qualification)
- **Constraints**: physics-informed (δ>0.8 keyholing, πw/l<1 balling, H²/W²+L²/D²>1 LOF)

**Global decision vector**: d=14 (composition=3, atomization=2, LPBF Tier-A=8, passthrough=1)
**Max per-node input dimensionality**: 5 (Nodes 2a, 2b) — well within SAASBO comfort zone

### Parameter Tiering (from Edison review)

| Tier                           | Count | Scope         | Examples                                                  |
| :----------------------------- | :---- | :------------ | :-------------------------------------------------------- |
| **A (actively optimized)**     | 6-8   | Per candidate | Power, speed, hatch, layer thickness, spot size, rotation |
| **B (fixed per alloy family)** | 8-10  | Per alloy     | Gas type, recoater type, baseplate temp                   |
| **C (fixed per machine)**      | 15-18 | Per facility  | Wavelength, beam profile, chamber pressure                |

### Key Design Decisions (Edison-informed)

1. **Joint composition-process optimization (Option A)**: Treat composition AND Tier-A process params as a single global decision vector. BOFN's EI-FN acquisition naturally discovers that optimal laser power depends on which alloy is being printed — this coupling emerges from the DAG without explicit conditional parameterization.

2. **SAASBO at each sub-node**: `SaasFullyBayesianSingleTaskGP` with horseshoe priors for automatic variable selection. Can identify relevant dimensions in ~20-30 evaluations (Eriksson & Jankowiak 2021, 290 citations).

3. **RGPE for cross-alloy transfer**: Ranking-weighted GP Ensemble (Feurer, Letham, Hutter & Bakshy 2018) for warm-starting new alloy compositions from previously optimized ones. Available in Ax.

4. **Multiple scalar-output nodes** for powder properties (Strategy 1 from Kiroriwal et al. 2025): decompose into 3 parallel scalar GPs rather than one multi-output GP.

5. **Constraint handling**: LPBF physical constraints modeled with physics-informed criteria (Edison review `98edd2c3`):
   - **Keyholing**: aspect ratio δ=depth/width > 0.8 (Bergmueller et al. 2023, conduction-to-keyhole transition)
   - **Balling**: πw/l < 1 track stability criterion (Wang et al. 2021)
   - **LOF**: H²/W² + L²/D² > 1 geometric overlap (Wang et al. 2021)
   Each modeled as constraint GPs at relevant sub-nodes, composed via `ConstrainedMCObjective`.

6. **Multi-fidelity within LPBF nodes**: Single-track experiments ($10/eval, low fidelity) and density cubes ($200/eval, high fidelity) can be handled via `SingleTaskMultiFidelityGP` within Node 2a/2d using continuous-fidelity KG (Wu & Frazier 2018, 246 citations).

### High-D BO Method Comparison (for LPBF Tier-A parameters)

| Method      | Best For                                         | BoTorch Support                          | Recommendation                               |
| :---------- | :----------------------------------------------- | :--------------------------------------- | :------------------------------------------- |
| **SAASBO**  | Sparse variable selection, d=6-10                | Native (`SaasFullyBayesianSingleTaskGP`) | **Default choice** for per-node GPs          |
| **TuRBO**   | Local process window search                      | Native                                   | Alternative when process windows are narrow  |
| **MORBO**   | Multi-objective (density + roughness + strength) | Research code                            | Use if Pareto optimization needed            |
| REMBO/HeSBO | Very high-d (d>20)                               | Custom implementation                    | Not needed: sub-node decomposition keeps d≤5 |

### Verified Implementation

See `benchmarks/bofn_expanded_demo.py` (v2):
- 9-node DAG with Edison-reviewed LPBF sub-node decomposition
- All GPs fit and propagate correctly through the DAG
- Multi-stage screening: 50 candidates → 17 after CALPHAD → 17 to characterization
- **66% cost savings** vs naive full-pipeline evaluation
- Max per-node input d=5 (Nodes 2a, 2b), compatible with SAASBO
- Fully Bayesian verification: `SaasFullyBayesianSingleTaskGP` passes with 0.2% error
- Physics-informed LPBF constraints (keyhole, balling, LOF) produce realistic feasible regions

### Integration with PR #30 (AM Test Structures)

The expanded DAG maps directly to the 8-stage AM validation progression from PR #30:

| AM Validation Stage          | BOFN Node                 | Fidelity     |
| :--------------------------- | :------------------------ | :----------- |
| Single tracks                | Node 2a (energy)          | Low ($10)    |
| Thin walls / crack screening | Node 2b (scan)            | Medium ($50) |
| Density cubes                | Node 2d (integration)     | High ($200)  |
| Tensile bars                 | Node 3 (characterization) | Full ($300)  |

This enables multi-fidelity BO within the BOFN framework: the acquisition function can select whether to run a cheap single-track experiment on a new composition or advance a promising candidate to density-cube evaluation, using constituent-evaluation KG (Toscano-Palmerin & Frazier).

---

## §2. Meta AE LLM+BO Literature

The full literature review is in `edison-trajectories/llm_bayesian_optimization.md`. Key findings:

### The Meta AE Paper: LILO

The Meta Adaptive Experimentation team's key contribution is **LILO** (Language-in-the-Loop Optimization, Kobalczyk, Lin, Letham, Zhao, Balandat, Bakshy 2025). LILO converts natural-language expert feedback into pairwise preferences for a GP utility model. Deployed in production at Meta for A/B testing, it achieves 30–50% convergence acceleration by incorporating expert knowledge without requiring mathematical formalization.

### Other Key Methods

| Method                                             | Key Mechanism                                            | Relevance to VCL                                                |
| :------------------------------------------------- | :------------------------------------------------------- | :-------------------------------------------------------------- |
| **LLAMBO** (Liu et al. 2024, ICLR, ~166 citations) | LLM warmstarting + zero-shot surrogate + guided sampling | Initialize composition search with LLM-suggested alloy families |
| **BORA** (Cissé et al. 2025)                       | Trust-weighted LLM intervention; calibrated reliability  | Stage selection for partial evaluations; graceful fallback      |
| **Reasoning BO** (Yang et al. 2025)                | Multi-agent LLM + knowledge graphs                       | Structured encoding of process-structure-property relationships |
| **LMABO** (Ngo et al. 2025)                        | LLM-based adaptive acquisition function selection        | Per-node acquisition function tuning                            |
| **AlloyGPT** (CMU 2025)                            | Domain-specific materials LLM                            | Alloy-specific warmstarting and prior specification             |

### Critical Gap

**No published work combines LLM priors with BOFN.** All LLM+BO methods assume a single-stage optimization problem. All BOFN methods use standard GP priors without LLM augmentation. This intersection is VCL's open frontier.

---

## §3. The Union: LLM-BOFN

### Proposed Architecture

Five integration points where LLMs can augment BOFN, ordered by implementation complexity:

#### Integration 1: LLAMBO-Style Warmstarting of Alloy Compositions

**Mechanism**: Before any experiments, query an LLM to generate initial alloy compositions.

**Prompt template**:
```
Given target properties [UTS > 400 MPa, elongation > 8%, LPBF-printable],
suggest 10 alloy compositions (Al-Si-Mg system) with rationale.
Consider: solidification range, cracking susceptibility, known LPBF literature.
```

**Integration with BOFN**: LLM-suggested compositions become the initial training set for Node 0 (CALPHAD). This bypasses the cold-start problem — instead of random compositions, the initial CALPHAD evaluations are on compositions the LLM deems promising based on literature knowledge.

**Risk**: LLM suggestions may be biased toward well-studied compositions, reducing exploration of novel alloys. Mitigated by including diversity constraints (e.g., at least 3 of 10 compositions must be >2σ from known alloys).

**POC Results v3** (see `benchmarks/bofn_llm_warmstart.py`, iterated through 3 Edison ANALYSIS reviews: v1 rated 4/10 → v2 rated 6/10 → v3 rated 7/10):

Queried Edison Scientific (1-credit LITERATURE, task `16953cd8`) for 15 Al-Si-Mg compositions. Edison returned compositions clustered around AlSi10Mg variants (83–92% Al, 7–16% Si, 0–1% Mg), all with scientific rationale citing solidification cracking literature. v3 improvements: harder benchmark (scale=15, softplus, noise=0.01), paired process/print params across arms, 2000 Thompson candidates, per-seed LLM perturbation (σ=0.015) + min-distance diversity filtering (0.06), 3-panel visualization with diversity diagnostics.

A/B/C comparison (20 seeds × 10 BO iterations, harder Tier 1 benchmark, per-node GPs, Thompson sampling):

| Metric                           | LLM-initialized                                | Random-initialized         | LHS-initialized |
| :------------------------------- | :--------------------------------------------- | :------------------------- | :-------------- |
| Cold-start advantage (Cohen's d) | **+0.356 vs Random** (d=1.49, p<0.0001)        | —                          | —               |
| Final best advantage             | +0.028 vs Random (d=0.07, p=0.756, n.s.)       | —                          | —               |
| AUC (sample efficiency)          | **23.06** (+15.7% vs Random, d=1.28, p=0.0002) | 19.94                      | 19.70           |
| Iterations to Y≥2.0              | **3.4** (~3.6 iters sooner)                    | 7.0                        | 7.2             |
| Win rate (final best)            | —                                              | 55% (11/20, p=0.412, n.s.) | 55% (11/20)     |
| Initial phase quality >0.5       | **75.6%**                                      | 10.0%                      | 13.8%           |

**Key finding (v3, per Edison review `11e2d390`, rated 7/10)**: LLM warmstarting provides a **large, statistically significant sample efficiency gain** (d=1.28 on AUC, d=1.49 on cold-start) that fully dissipates by iteration 10. This matches LLAMBO's theoretical prediction: LLM initialization improves the cold-start regime but does not change the convergence point. The contribution should be framed as **sample efficiency** (reaching good solutions ~3.6 iterations sooner, +15.7% AUC) rather than convergence advantage.

**Edison-identified remaining issues for publication readiness**:
1. **Benchmark circularity** (HIGH): Optimum [0.7, 0.2, 0.1] is aligned with known Al-Si-Mg alloys — need non-circular benchmarks where optimum ≠ domain knowledge
2. **No true BOFN acquisition function** (~~MEDIUM-HIGH~~ **RESOLVED**): Thompson sampling over random candidates was a simplified approximation. We have now ported the Frazier lab's [`partial_kgfn`](https://github.com/frazier-lab/partial_kgfn) to modern BoTorch (>=0.12), including the p-KGFN acquisition function (Buathong et al. 2024, ICML), GaussianProcessNetwork model, Thompson sampling baseline, and the manufacturing test problem. Multi-seed benchmark results (5 seeds, $1,190 equal budget): **Random 0.70±0.30, TSFN 0.71±0.32, pKGFN 0.67±0.28** — all within each other's error bands. p-KGFN gets ~69 cheap partial evaluations vs 8 full-network evaluations within the same budget. Root-only partial evaluations don't propagate enough information through the DAG to outperform full evaluations at this budget scale; the original paper shows advantages at larger budgets and higher cost ratios. Key API changes from the original (botorch 0.8.4): `FixedNoiseGP`→`SingleTaskGP`, `fit_gpytorch_model`→`fit_gpytorch_mll`, `covar_module.base_kernel`→`covar_module` (modern GPyTorch). Remaining work: gradient-based acquisition optimization (currently uses discrete candidate evaluation), larger budget experiments, and full batch p-KGFN support.
3. **Results framing** (MEDIUM): Report AUC and iterations-to-threshold as primary metrics, not convergence advantage

#### Integration 2: LLM-Informed GP Priors per Pipeline Node

**Mechanism**: Use LLM outputs to set informative GP prior mean functions and lengthscale priors for each node's GP.

**Example for Node 2 (LPBF)**:
```
LLM knowledge: "Part density in LPBF typically follows a Gaussian-like response
surface centered on the volumetric energy density optimum (~60-80 J/mm³).
Density drops sharply below 40 J/mm³ (lack of fusion) and above 120 J/mm³
(keyhole porosity)."

→ GP prior mean: Gaussian centered at VED=70 J/mm³
→ Lengthscale prior: shorter in VED dimension (sharp transitions)
                      longer in hatch spacing dimension (smoother)
```

**Integration with BOFN**: Each node's GP gets a different LLM-informed prior, reflecting the distinct physics at each pipeline stage. Node 0 (CALPHAD) priors encode thermodynamic intuition; Node 1 (powder) priors encode atomization physics; etc.

#### Integration 3: BORA-Style Stage Selection

**Mechanism**: When p-KGFN must decide which node to evaluate next for a candidate, consult a trust-weighted LLM agent.

**Decision flow**:
1. p-KGFN computes the information value per dollar for evaluating each node
2. LLM agent suggests which node to evaluate, with justification
3. Trust weight (calibrated from LLM's track record) blends the two recommendations
4. If LLM and p-KGFN agree, proceed with high confidence
5. If they disagree, the trust weight determines the blend (early iterations favor p-KGFN; as LLM proves reliable, its weight increases)

**Example**: After observing that a composition has a narrow solidification range (good for LPBF) but unusual powder morphology, the LLM might recommend skipping directly to LPBF (Node 2) with conservative print parameters rather than optimizing powder quality (Node 1) further.

#### Integration 4: LILO-Style Natural-Language Interpretation of Intermediate Outputs

**Mechanism**: Convert intermediate experimental outputs (powder PSD distributions, SEM micrographs, XRD patterns) into natural-language descriptions, then use LILO-style preference learning.

**Example flow**:
1. Node 1 produces powder with bimodal PSD
2. LLM interprets: "Bimodal powder size distribution with peaks at 20μm and 60μm suggests agglomeration during atomization. This may reduce flowability but could improve packing density in LPBF."
3. LLM generates pairwise preferences: "Composition A (unimodal PSD) is preferred over Composition B (bimodal PSD) for standard LPBF, but Composition B may outperform for high-density applications."
4. Preferences update the Node 2 GP's prior

**Key innovation**: This bridges the gap between multimodal experimental data (images, spectra, distributions) and the scalar/vector inputs required by standard GPs.

#### Integration 5: RAG over Edison Trajectories for Hypothesis Generation

**Mechanism**: Use Retrieval-Augmented Generation (RAG) over the VCL's Edison trajectory database to generate hypotheses about alloy behavior at each pipeline stage.

**Implementation**:
1. Embed all Edison trajectory documents (`edison-trajectories/*.md`) into a vector database
2. At each BO iteration, retrieve relevant passages based on the current experimental state
3. LLM generates hypotheses: "Based on CALPHAD literature (edison-trajectories/calphad_alloy_design.md), this composition's Al₃Mg₂ intermetallic may cause hot tearing during LPBF solidification."
4. Hypotheses inform the acquisition function by biasing exploration toward compositions where the LLM is uncertain

### Implementation Roadmap

| Phase                                         | Duration    | Deliverable                                                                                                                                                                                                                                                                                                                                                            | Dependencies                     |
| :-------------------------------------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- |
| **Phase 1: BOFN baseline**                    | Complete    | Working 4-node function network with per-node GPs                                                                                                                                                                                                                                                                                                                      | BoTorch 0.17.2 ✅                 |
| **Phase 2: LLAMBO warmstart**                 | Complete    | LLM-initialized composition search; A/B comparison vs random init                                                                                                                                                                                                                                                                                                      | Edison Scientific ✅              |
| **Phase 2b: P3 diversity + validation**       | Complete    | Per-seed perturbation, min-distance filtering, harder benchmark, 3 Edison review rounds (4/10 → 6/10 → 7/10)                                                                                                                                                                                                                                                           | Phase 2 ✅                        |
| **Phase 3: Non-circular benchmarks + p-KGFN** | In progress | Add benchmarks with non-domain-aligned optima; ~~port p-KGFN~~ **p-KGFN ported** (`benchmarks/partial_kgfn/`, `benchmarks/bofn_pkgfn_demo.py`) — multi-seed results show algorithms within error bands at $1,190 budget; p-KGFN advantages expected at larger budgets. Remaining: non-circular benchmarks, gradient-based acqf optimization, larger-budget experiments | Phase 2b complete, p-KGFN port ✅ |
| **Phase 4: LLM priors**                       | 3 weeks     | Per-node GP priors from LLM; ablation study on each node                                                                                                                                                                                                                                                                                                               | Phase 3 complete                 |
| **Phase 5: Full LLM-BOFN**                    | 4 weeks     | BORA-style stage selection + LILO-style NL feedback + RAG                                                                                                                                                                                                                                                                                                              | Phases 3–4 complete              |

---

## §4. Benchmark Task Design

### Motivation

Before deploying LLM-BOFN on real alloy experiments (where each full-pipeline evaluation costs ~$1,301 and takes days), we need synthetic and semi-synthetic benchmarks to build confidence in the framework's decisions.

### Benchmark Tier 1: Synthetic Function Network (Available Now)

**Task**: Optimize a 4-node synthetic function network with known ground truth.

**Setup** (implemented in `benchmarks/bofn_demo.py`):
- Node 0: Gaussian peak at optimal composition (3D input → 1D output)
- Node 1: Cosine + linear mixing model (3D → 1D)
- Node 2: Sigmoid response surface (3D → 1D)
- Node 3: Quasi-linear with sinusoidal perturbation (1D → 1D)

**Metrics**:
- Simple regret (gap between best found and true optimum) vs. iteration count
- Cost-weighted regret (regret per dollar spent)
- Node evaluation frequency (how often each node is queried)
- Wall-clock time per iteration (LLM overhead)

**Comparisons**:
1. **BOFN** (no LLM) — baseline function network BO
2. **Flat BO** — standard BO treating the pipeline as a black box
3. **Random search** — uniform random sampling
4. **LLM-BOFN** variants — with each integration point enabled individually and in combination

**What this validates**: Basic algorithmic correctness. Does the composite GP posterior propagate accurately? Does cost-aware screening reduce total cost? Does LLM warmstarting improve early-iteration performance?

### Benchmark Tier 2: CALPHAD-Grounded Synthetic Network (1–2 Weeks to Build)

**Task**: Replace Node 0 (CALPHAD) with actual pycalphad evaluations while keeping Nodes 1–3 synthetic.

**Setup**:
- Node 0: `pycalphad` equilibrium calculation with COST507 database (Al-Si-Mg system)
  - Input: composition (3D: Al, Si, Mg fractions)
  - Output: solidification range ΔT (liquidus − solidus) — real thermodynamic data
- Nodes 1–3: Synthetic functions calibrated to realistic ranges
  - Node 1 output in [0, 1] (flowability score)
  - Node 2 output in [95, 100] (% theoretical density)
  - Node 3 output in [200, 500] (MPa UTS)

**Metrics**: Same as Tier 1, plus:
- CALPHAD call count (verify screening reduces expensive calls to downstream nodes)
- Discovery of known-good compositions (AlSi10Mg, AlSi12 — does the optimizer find them?)

**What this validates**: Realistic CALPHAD physics at Node 0. Tests whether LLM priors about phase stability align with actual thermodynamic calculations. Validates that BOFN's dimensionality reduction helps when Node 0 has genuinely nonlinear, multi-modal structure.

### Benchmark Tier 3: Literature-Derived Multi-Stage (2–4 Weeks to Build)

**Task**: Reconstruct a published multi-stage alloy discovery dataset as a function network.

**Candidate datasets**:
1. **Barrionuevo et al. (Harvard Dataverse)**: LPBF process parameters → density → mechanical properties for multiple alloy compositions. Can be split into a 3-node network (composition+process → density → properties).
2. **FatigueData-CMA2022 (Figshare)**: Processing → microstructure → fatigue life for various alloy systems.
3. **AFLOW/OQMD**: Composition → DFT energy → predicted stability. Can serve as a "computational Node 0" for testing BOFN with real data.

**Setup**: Use published data to fit "ground truth" models at each node, then evaluate how efficiently BOFN+LLM discovers the optimal compositions compared to standard BO.

**What this validates**: Realistic multi-stage correlations. Tests whether LLM-BOFN can exploit known process-structure-property relationships that humans find intuitive but standard BO would need many evaluations to learn.

### Benchmark Tier 4: Live Pipeline Pilot (Deployment Phase)

**Task**: Run LLM-BOFN on VCL's actual alloy discovery pipeline for a limited campaign.

**Setup**:
- 5 CALPHAD-screened compositions → 3 atomized → 2 printed → 2 characterized
- Compare against expert-selected compositions (PI's domain knowledge baseline)
- Run with and without LLM augmentation to measure marginal value

**Success criteria**:
- LLM-BOFN identifies at least one composition that the expert baseline missed
- Cost-aware screening reduces total campaign cost by ≥30% vs. sequential evaluation
- No catastrophic failures (e.g., suggesting compositions that damage equipment)

**What this validates**: Real-world integration. Can LLM-BOFN handle noisy, multimodal, heterogeneous data from real equipment? Does the LLM's metallurgical knowledge actually help, or is it noise?

### Recommended Evaluation Sequence

```
Tier 1 (now) → verify algorithmic correctness
    ↓
Tier 2 (weeks 1-2) → validate with real CALPHAD physics
    ↓
Tier 3 (weeks 3-6) → test on published multi-stage datasets
    ↓
Tier 4 (month 2+) → pilot on VCL pipeline
```

### Key Metrics Across All Tiers

| Metric                   | What It Measures                      | Target                                                  |
| :----------------------- | :------------------------------------ | :------------------------------------------------------ |
| **Simple regret**        | Optimization performance              | < flat BO by 2× at same iteration count                 |
| **Cost-weighted regret** | Economic efficiency                   | < flat BO by 5× (leveraging cheap CALPHAD)              |
| **LLM overhead**         | Computational cost of LLM integration | < 10% of total wall-clock time                          |
| **Warmstart gain**       | Improvement from LLM initialization   | > 50% regret reduction in first 5 iterations            |
| **Trust calibration**    | BORA trust weight accuracy            | Correlation > 0.7 between trust and actual LLM accuracy |
| **Robustness**           | Handling of LLM hallucinations        | No worse than baseline BOFN when LLM gives bad advice   |

### What Would Build Confidence for Deployment

1. **Tier 1 passes**: BOFN composite forward pass matches ground truth; cost-aware screening shows 90%+ savings
2. **Tier 2 passes**: CALPHAD-grounded network discovers known alloys (AlSi10Mg) within 20 iterations; LLM warmstarting finds them in ≤5 iterations
3. **Tier 3 passes**: On published datasets, LLM-BOFN matches or exceeds the original authors' optimization performance with fewer evaluations
4. **Tier 4 pilot**: LLM-BOFN suggests at least one novel composition validated by characterization, at lower cost than expert-driven exploration

---

## Summary

| Deliverable                    | Status                 | Location                                                      |
| :----------------------------- | :--------------------- | :------------------------------------------------------------ |
| BOFN in BoTorch (4-node)       | ✅ Verified working     | `benchmarks/bofn_demo.py`                                     |
| **BOFN expanded DAG (9-node)** | **✅ Verified working** | **`benchmarks/bofn_expanded_demo.py`**                        |
| Fully Bayesian BOFN (SAASBO)   | ✅ Verified compatible  | `benchmarks/bofn_fully_bayesian_test.py`                      |
| Function networks literature   | ✅ Complete             | `edison-trajectories/function_networks_bo.md`                 |
| LLM+BO literature              | ✅ Complete             | `edison-trajectories/llm_bayesian_optimization.md`            |
| **LPBF dimensionality review** | **✅ Complete**         | **`edison-trajectories/bofn-lpbf-dimensionality-review.md`**  |
| **LPBF implementation review** | **✅ Complete**         | **`edison-trajectories/bofn-lpbf-implementation-review.md`**  |
| LLM-BOFN synthesis             | ✅ Proposed             | This document (§3)                                            |
| Benchmark task design          | ✅ Designed             | This document (§4)                                            |
| Tier 1 benchmark               | ✅ Implemented          | `benchmarks/bofn_demo.py`, `benchmarks/bofn_expanded_demo.py` |
| Tier 2–4 benchmarks            | ⏳ Future work          | —                                                             |

### Edison Scientific Task IDs

| Task ID                                | Type            | Query                                                                                                                                                   |
| :------------------------------------- | :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `d0ad1eea-6b3b-42af-93cf-0b293b001986` | LITERATURE_HIGH | BOFN LPBF parameter dimensionality — sub-node decomposition, SAASBO vs TuRBO, RGPE transfer, powder properties, LPBF BO literature                      |
| `6025bdcf-6c58-46d0-b891-6a1bc68e610e` | LITERATURE_HIGH | Follow-up — composition-process coupling (Option A), multi-fidelity within BOFN nodes, constraint handling, batch evaluation, BoTorch/Ax implementation |
