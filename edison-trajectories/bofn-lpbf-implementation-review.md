# BOFN LPBF Implementation — Edison Scientific Follow-Up Review

*Edison task `6025bdcf-6c58-46d0-b891-6a1bc68e610e` | LITERATURE_HIGH | 2026-04-09*
*~44K chars, 25+ citations*

Topics: Composition-process coupling (Option A), multi-fidelity within BOFN nodes,
constraint handling for LPBF physical limits, batch evaluation, BoTorch/Ax implementation.

---

Question: This is a follow-up to our previous analysis of Bayesian Optimization over Function Networks
(BOFN, Astudillo & Frazier 2021) for LPBF alloy discovery. Based on the first review, we are
converging on the following refined architecture:

**Refined BOFN DAG for VCL alloy discovery** (7+ nodes):
- Node 0: CALPHAD screening (composition d=3-5 → phase fractions + solidification range d=2)
- Node 1a-c: Ultrasonic atomization → 3 key powder properties (PSD D50, flowability, apparent density)
- Node 2a: Energy delivery (powder props + power + speed + spot_size d=6 → melt pool geometry d=2)
- Node 2b: Scan strategy (melt pool + hatch + rotation + contour d=5 → layer quality d=1)
- Node 2c: Thermal management (layer quality + preheat + dwell d=3 → residual stress d=1)
- Node 2d: Integration (melt pool + layer quality + stress d=4 → part density d=1)
- Node 3: Mechanical characterization (part density d=1 → YS + elongation d=2)

Key design decisions from first review:
1. SAASBO (SaasFullyBayesianSingleTaskGP) at each sub-node for automatic variable selection
2. RGPE for transfer learning across alloy compositions
3. Parameter tiering: 6-8 actively optimized (Tier A), rest fixed per alloy/machine
4. Multiple scalar-output nodes preferred over multi-output GPs

FOLLOW-UP QUESTIONS:

(a) **Composition-process coupling in BOFN**: The standard BOFN formulation assumes node inputs
    are either decision variables (set by the optimizer) or parent node outputs. But in our
    pipeline, LPBF process parameters (Node 2) should ideally be CO-OPTIMIZED alongside
    composition (Node 0). The optimal laser power depends on which alloy you're printing.
    How should we handle this joint composition-process optimization in a BOFN DAG?
    Specifically:
    - Option A: Treat composition AND all process params as a single flat decision vector,
      but use BOFN structure for the intermediate observables (phase fractions, powder quality).
    - Option B: Run a nested optimization where the outer loop selects composition and the
      inner loop optimizes process params for each composition via BOFN.
    - Option C: Define "conditional" decision variables at each node that depend on the
      decision at upstream nodes (e.g., scan speed as a function of alloy thermal conductivity).
    Which of these is best supported by theory and implementation?

(b) **BOFN with multi-fidelity**: Single-track experiments (Stage 1 in AM validation) provide
    low-fidelity melt-pool data at ~$10/eval, while full density cubes (Stage 3) provide
    high-fidelity density data at ~$200/eval. Can multi-fidelity BO (e.g., Knowledge Gradient
    for Multi-Fidelity, Poloczek et al. 2017; or continuous-fidelity BO, Kandasamy et al. 2017)
    be integrated within individual BOFN nodes? This would allow Node 2 to learn from cheap
    single-track experiments and expensive density cubes simultaneously.

(c) **Constraint handling**: LPBF has hard physical constraints that must be respected:
    - No keyholing: melt pool depth/width ratio < 1.5
    - No balling: melt track length/width > 2.3
    - No lack-of-fusion: minimum overlap between adjacent tracks
    - Hot cracking susceptibility depends on composition (from Node 0 output)
    How should these constraints be incorporated into the BOFN acquisition function?
    Can we use constrained BO (Letham et al. 2019; Daulton et al. 2022) within the
    function network, where constraints at downstream nodes inform upstream decisions?

(d) **Batch evaluation in BOFN**: In practice, LPBF builds evaluate multiple compositions
    simultaneously on one build plate (Weaver et al. 2021 demonstrated 24 columns per build).
    How should batch BO (e.g., q-EI, Thompson sampling batch) be adapted for BOFN where
    different candidates may be at different pipeline stages? This connects to the p-KGFN
    partial evaluation concept — in a single build, some candidates are at Node 2a (SST)
    while others are at Node 2d (density cubes).

(e) **Practical implementation**: What is the recommended way to implement this expanded
    DAG in BoTorch/Ax? The Ax platform has a `GenerationStrategy` and `Models` framework.
    Can the BOFN structure be expressed as an Ax experiment with custom `Model` bridges?
    Or should this be implemented purely in BoTorch with manual acquisition function
    optimization? What about the Ax `BenchmarkProblem` interface for our tiered benchmarks?

Please provide specific citations and implementation guidance. Focus on what is practically
achievable with BoTorch 0.17+ and Ax.

## BOFN Architecture for VCL Alloy Discovery via LPBF: Follow-Up Analysis

This report addresses five follow-up questions on implementing Bayesian Optimization over Function Networks (BOFN) for laser powder bed fusion (LPBF) alloy discovery, building on the refined 7+ node DAG architecture with SAASBO, RGPE, and parameter tiering.

The following table provides a high-level summary of recommendations for each question:

| Question | Topic | Recommended Approach | Key Methods/References | Implementation Priority | Notes |
|---|---|---|---|---|---|
| (a) | Composition-process coupling in BOFN | Use **Option A**: a single global decision vector containing composition and Tier-A process variables, while preserving the BOFN DAG for intermediate observables. | BOFN natively allows each node to take a subset of the global decision vector plus parent outputs, so composition and process parameters can be jointly optimized without nesting; SAASBO at node level for sparsity; RGPE for cross-alloy warm start (astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 4-6, astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 6-8, feurer2018scalablemetalearningfor pages 6-8, feurer2018scalablemetalearningfor pages 3-6, eriksson2021highdimensionalbayesianoptimization pages 3-4, eriksson2021highdimensionalbayesianoptimization pages 2-3) | **Highest** | Best aligned with BOFN theory and most practical in BoTorch. Option B is defensible for engineering workflow decomposition but not the cleanest BOFN formulation; Option C is better interpreted as learned feature engineering or contextual modeling than as the primary BO decision parameterization. |
| (b) | BOFN with multi-fidelity | Add a **fidelity variable inside selected nodes**, especially Node 2 melt-pool / density submodels, and optimize node queries with cost-aware KG such as **cfKG** or related KG-style multi-fidelity policies. | Continuous-fidelity KG selects design and fidelity jointly using value of information per cost; grey-box BO literature treats multi-fidelity and function-network structure as complementary; practical trace-aware KG is useful when low-fidelity experiments produce partial traces (astudillo2021thinkinginsidethe pages 8-10, wu2018continuousfidelitybayesianoptimization pages 4-7, wu2018continuousfidelitybayesianoptimization pages 1-3, wu2018continuousfidelitybayesianoptimization pages 3-4, wu2020practicalmultifidelitybayesian pages 2-3, wu2020practicalmultifidelitybayesian pages 1-2) | **High** | Most achievable near-term is node-local multi-fidelity, not a fully end-to-end multi-fidelity BOFN acquisition over the whole DAG. For LPBF, single-track and cube-density tests map naturally to fidelity controls or discrete information sources inside Node 2. |
| (c) | Constraint handling | Model hard physics constraints as **separate surrogate outputs / nodes** and use **feasibility-weighted EI-FN** or noisy constrained EI-style acquisition. | Constrained BO commonly multiplies EI by probability of feasibility; noisy constrained EI and related methods support uncertain constraint observations; downstream constraints can be represented as predicted network quantities such as keyholing, balling, overlap, and cracking susceptibility (wang2025constrainedcompositebayesian pages 1-4, ungredda2024bayesianoptimisationfor pages 1-3, letham2019constrainedbayesianoptimization pages 3-6, letham2019constrainedbayesianoptimization pages 1-3, eriksson2021scalableconstrainedbayesian pages 2-3, eriksson2021scalableconstrainedbayesian pages 1-2) | **Highest** | In practice, some constraints should be enforced twice: as search-space bounds or deterministic filters when known analytically, and as learned probabilistic feasibility models when uncertain. Hot-cracking can enter through CALPHAD-derived upstream descriptors feeding a constraint GP. |
| (d) | Batch evaluation in BOFN | Use **q-EI-FN / MC batch acquisition** for same-stage batch proposals, and use **partial-evaluation KG** ideas when candidates can be advanced to different DAG stages. | Batch BO uses Monte Carlo joint posterior sampling with SAA; constituent-evaluation KG jointly values which candidate and which partial evaluation to perform next; this is the closest available theory to p-KGFN-style stage-aware LPBF scheduling (alabed2025towardsefficienttuning pages 108-111, astudillo2021thinkinginsidethe pages 12-14, astudillo2021thinkinginsidethe pages 10-12, balandat2019botorchprogrammablebayesian pages 6-7, astudillo2021thinkinginsidethe pages 6-8) | **Medium** | For one build plate, a pragmatic scheduler is mixed-stage asynchronous BO: some arms receive cheap Node 2a/2b evaluations while a few promising arms are promoted to Node 2d/3. Full p-KGFN may require custom research code rather than stock Ax. |
| (e) | Practical implementation in BoTorch/Ax | Implement the DAG **primarily in BoTorch** with custom node models, posterior propagation, and acquisition optimization; wrap this in Ax only for orchestration via **GenerationStrategy / custom GenerationNodes** if needed. | BoTorch provides the needed programmable abstractions: custom Model, Posterior, MC acquisition, reparameterized sampling, optimize_acqf; Ax supplies experiment management, modular generators, SurrogateSpec/ModelConfig, and custom generation strategies (balandat2019botorchprogrammablebayesian pages 6-7, chang2019bayesianhyperparameteroptimization pages 4-9, kashtelyan2025axaplatform pages 17-22, kashtelyan2025axaplatform pages 6-8, kashtelyan2025axaplatform pages 22-25, kashtelyan2025axaplatform pages 3-6, kashtelyan2025axaplatform pages 1-3) | **Highest** | Recommended split: BoTorch for BOFN logic, Ax for trial lifecycle, logging, benchmarking, and deployment. Ax alone is not the natural place to express full BOFN posterior propagation across a custom DAG. For benchmarks, Ax BenchmarkProblem is useful after the BoTorch BOFN core exists. |


*Table: This table summarizes the recommended practical approach for each follow-up question on BOFN for LPBF/VCL alloy discovery. It links each recommendation to supporting BOFN, constrained BO, multi-fidelity BO, and BoTorch/Ax implementation references.*

---

### (a) Composition-Process Coupling in BOFN

**Recommendation: Option A is the correct and best-supported approach.**

The BOFN formulation of Astudillo and Frazier explicitly supports the scenario where different subsets of a global decision vector x are assigned to different nodes in the DAG. Each node function f_k takes as input a (possibly empty) subset I(k) of the components of x together with the outputs of its parent nodes: h_k(x) = f_k(x_{I(k)}, h_{J(k)}(x)) (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 4-6). Optimization is performed over the entire global decision vector x jointly, using expected improvement computed with respect to the non-Gaussian posterior induced by the network structure (astudillo2021bayesianoptimizationof pages 1-2). The Fetch-and-Reach example in the original BOFN paper explicitly demonstrates nodes that accept both per-node decision variables and parent outputs simultaneously (astudillo2021bayesianoptimizationof pages 6-8).

For the VCL alloy discovery pipeline, this means composition variables (e.g., V, Cr, L fractions) are components of x assigned to Node 0 (CALPHAD), while laser power, scan speed, and spot size are additional components of x assigned to Node 2a. The BOFN acquisition function (EI-FN) optimizes all of these jointly using sample average approximation (SAA), which creates a deterministic, differentiable proxy via fixed Monte Carlo base samples and reparameterized GP sampling (astudillo2021bayesianoptimizationof pages 4-6). Because the posterior is computed recursively through the network, the optimizer naturally discovers that optimal laser power depends on which alloy is being printed—this coupling emerges from the DAG structure without requiring explicit conditional parameterization.

**Option B (nested optimization)** lacks direct support in the BOFN formulation: it converts the problem into a bilevel objective where the inner optimization is itself expensive and uncertain, negating the sample-efficiency advantages of the network structure (astudillo2021bayesianoptimizationof pages 2-4). **Option C (conditional decision variables)** can be viewed as a learned policy overlaid on BOFN, but it risks imposing incorrect inductive biases and has weaker off-the-shelf support (astudillo2021bayesianoptimizationof pages 2-4).

The following table provides a detailed comparison of the three options:

| Option | Description | Theory Support (from BOFN formulation) | Implementation Complexity | Key Advantages | Key Limitations | Recommendation |
|---|---|---|---|---|---|---|
| A | Treat composition and Tier-A LPBF parameters as one global decision vector \(x\); assign subsets of \(x\) to the relevant BOFN nodes, while preserving the DAG for intermediate observables such as CALPHAD outputs, powder properties, melt-pool geometry, stress, and density. | **Strong / direct support.** BOFN explicitly allows each node \(f_k\) to depend on a subset of the global decision vector and parent outputs, and optimizes the full \(x\) jointly via EI-FN / SAA. This is exactly the native BOFN formulation, not a workaround. (astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 4-6, astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 6-8) | **Moderate.** Requires a custom BoTorch implementation of the DAG posterior and acquisition, but no extra bilevel machinery beyond BOFN itself. SAASBO can reduce active-dimensional burden; RGPE can warm-start across alloys. (balandat2019botorchprogrammablebayesian pages 6-7, kashtelyan2025axaplatform pages 17-22, eriksson2021highdimensionalbayesianoptimization pages 3-4, feurer2018scalablemetalearningfor pages 1-3) | Theoretically clean; captures alloy-specific process optima directly; supports transfer across compositions; avoids decomposition error from decoupling composition and process; compatible with constraints, batch BO, and multi-fidelity extensions at node level. (astudillo2021bayesianoptimizationof pages 2-4, letham2019constrainedbayesianoptimization pages 3-6, wu2018continuousfidelitybayesianoptimization pages 4-7) | High-dimensional search if too many process variables are left active; requires careful parameter tiering and good transforms; full BOFN is easier in BoTorch than in Ax-native abstractions. (eriksson2021highdimensionalbayesianoptimization pages 3-4, eriksson2021highdimensionalbayesianoptimization pages 4-5, kashtelyan2025axaplatform pages 6-8) | **Recommended default.** Use Option A with parameter tiering: jointly optimize composition + 6–8 Tier-A process variables, keep remaining machine/setup variables fixed or condition-specific. |
| B | Nested optimization: outer loop proposes composition; inner BOFN (or separate BO) optimizes LPBF parameters for that composition before returning a value to the outer loop. | **Weak / indirect support.** This is not the BOFN formulation in Astudillo & Frazier; it converts the problem into a bilevel black-box objective over composition where the inner optimum is itself expensive and uncertain. The grey-box literature supports KG-style lookahead and partial evaluations, but not this nested structure as the standard BOFN treatment. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021thinkinginsidethe pages 4-6, astudillo2021thinkinginsidethe pages 12-14) | **High to very high.** Requires solving an inner optimization repeatedly, managing uncertainty propagation from inner to outer loop, and deciding stopping rules for inner BO per composition. Hard to do robustly in Ax/BoTorch without substantial custom logic. | Conceptually aligns with “optimize process for each alloy”; can be attractive if compositions are few and process optimization is operationally separable. | Sample-inefficient; duplicates modeling effort; outer model sees a noisy, nonstationary “value of best process for alloy” objective; difficult to exploit intermediate observables jointly across alloys/processes; hard to batch fairly. | **Not recommended as primary architecture.** Consider only as a pragmatic fallback if organizational workflow forces strict stage-wise optimization. |
| C | Use conditional decision variables or parameterized policies, e.g., scan speed chosen as a function of upstream alloy descriptors or inferred latent properties. | **Partial / indirect support.** BOFN supports node inputs that include decision-variable subsets and parent outputs, but “decision variables as functions of upstream outputs” is not the standard BOFN decision model. This becomes contextual / policy optimization or structured reparameterization layered on top of BOFN rather than BOFN itself. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 6-8, astudillo2021thinkinginsidethe pages 4-6) | **High.** Requires designing a policy class or conditional parameterization, then optimizing policy parameters rather than raw process variables. Additional modeling assumptions are needed to avoid over-constraining the search. | Can encode metallurgical intuition; may reduce dimensionality; can improve operational interpretability if strong causal heuristics are known. | Risks imposing the wrong inductive bias; may exclude optimal alloy-specific settings; more difficult to validate and debug than direct joint optimization; weaker off-the-shelf support in BoTorch/Ax. | **Use only as a later refinement.** Most useful after collecting data with Option A, when you can fit interpretable policy surrogates or reduce to a learned contextual parameterization. |


*Table: This table compares the three candidate architectures for joint composition-process optimization in BOFN for LPBF alloy discovery. It highlights that Option A is the only approach directly supported by BOFN theory and is the most practical path in BoTorch/Ax.*

**Practical recommendation for parameter tiering with Option A:** Combine composition (3 variables) with 6–8 Tier-A process parameters (power, speed, hatch, layer thickness, preheat, spot size) into a global decision vector of dimension ~9–11. Use SAASBO's sparsity-inducing hierarchical half-Cauchy prior on inverse length-scales to automatically identify which variables matter most at each node (eriksson2021highdimensionalbayesianoptimization pages 3-4, eriksson2021highdimensionalbayesianoptimization pages 2-3). Fix remaining Tier-B parameters (gas flow, recoater speed) per machine/alloy configuration. Use RGPE to warm-start across alloy compositions by maintaining base GPs from prior optimization campaigns on different alloys (feurer2018scalablemetalearningfor pages 3-6, feurer2018scalablemetalearningfor pages 1-3).

---

### (b) BOFN with Multi-Fidelity

**Multi-fidelity BO can be integrated within individual BOFN nodes, though a fully end-to-end multi-fidelity BOFN acquisition does not yet exist as a unified framework.**

The grey-box BO framework described by Astudillo and Frazier classifies both function-network BO and multi-fidelity BO as complementary grey-box methods that exploit known structure of the objective evaluation (astudillo2021thinkinginsidethe pages 8-10, astudillo2021thinkinginsidethe pages 1-2). The continuous-fidelity knowledge gradient (cfKG) of Wu and Frazier models evaluations as g(x, s) where s ∈ [0,1]^m controls fidelity, selects the (x, s) pair that maximizes expected reduction in posterior minimum per unit cost, and extends naturally to batch settings via q-cfKG (wu2018continuousfidelitybayesianoptimization pages 4-7, wu2018continuousfidelitybayesianoptimization pages 1-3, wu2018continuousfidelitybayesianoptimization pages 3-4). The trace-aware variant (taKG) further leverages partial evaluation traces and multiple continuous fidelity controls (wu2020practicalmultifidelitybayesian pages 2-3, wu2020practicalmultifidelitybayesian pages 1-2).

**For the LPBF pipeline**, the most practical integration is node-local multi-fidelity:

1. **Node 2a (Energy delivery):** Model as g_2a(x, s) where s represents fidelity: s=0 for single-track experiments (~$10/eval) and s=1 for multi-track pads. The cfKG acquisition jointly selects process parameters and whether to run a single-track or multi-track experiment, balancing information gain against cost.

2. **Node 2d (Integration/density):** Similarly, s could distinguish between small-cube density measurements (medium fidelity, ~$50) and full density cubes (~$200). A separate GP on log-cost can model the cost function (wu2018continuousfidelitybayesianoptimization pages 4-7).

3. **Practical implementation:** Within each multi-fidelity node, use BoTorch's `SingleTaskMultiFidelityGP` (kashtelyan2025axaplatform pages 17-22) together with a cost-aware acquisition. The node-level multi-fidelity GP feeds into the BOFN DAG posterior propagation as if it were a standard node, with the fidelity control being an additional decision variable at that node.

The knowledge gradient for constituent evaluations (KG_n(x,w)) already values partial/intermediate evaluations by their expected improvement in the posterior best objective (astudillo2021thinkinginsidethe pages 10-12, astudillo2021thinkinginsidethe pages 12-14), providing a natural bridge between multi-fidelity and function-network concepts. A unified multi-fidelity BOFN acquisition would extend this to select (x, w, s) jointly—the design point, which network constituent to evaluate, and at what fidelity—but this is currently a research frontier rather than available off-the-shelf.

---

### (c) Constraint Handling

**LPBF constraints should be incorporated using a combination of deterministic enforcement and probabilistic feasibility weighting within the BOFN acquisition function.**

The standard approach in constrained BO models each constraint c_j(x) with a separate GP and multiplies the acquisition function by the probability of feasibility: α_constrained(x) = α_EI(x) · ∏_j P(c_j(x) ≤ 0) (letham2019constrainedbayesianoptimization pages 3-6, ungredda2024bayesianoptimisationfor pages 1-3, eriksson2021scalableconstrainedbayesian pages 1-2). Letham et al. extended this to handle noisy constraint observations by integrating over the posterior using quasi-Monte Carlo approximation, which is critical for LPBF where density and defect measurements are inherently noisy (letham2019constrainedbayesianoptimization pages 1-3, letham2019constrainedbayesianoptimization pages 3-6). Eriksson and Poloczek's SCBO further extends constrained BO to high-dimensional, batch settings using Thompson sampling with trust regions (eriksson2021scalableconstrainedbayesian pages 2-3).

**For the LPBF DAG, constraints map naturally to the network structure:**

1. **Keyholing (depth/width < 1.5):** This is a function of melt pool geometry, which is the output of Node 2a. Add a constraint GP at Node 2a that models the depth-to-width ratio. When this ratio is deterministically computable from simulation (e.g., Rosenthal equation), it can be enforced as a hard search-space bound rather than a learned constraint.

2. **Balling (track length/width > 2.3):** Similarly modeled as a constraint output at Node 2a, informed by single-track experimental data.

3. **Lack-of-fusion (minimum overlap):** This is a function of both melt pool width (Node 2a output) and hatch spacing (Node 2b input), making it a constraint at Node 2b. It can be computed deterministically given melt pool width and hatch distance.

4. **Hot cracking susceptibility:** This depends on composition through solidification range and phase fractions from Node 0 (CALPHAD). Model this as a constraint GP that takes CALPHAD outputs as inputs, or use known susceptibility criteria (e.g., Kou criterion) as deterministic constraints.

**Implementation approach:** Extend EI-FN to constrained EI-FN by multiplying the MC-estimated expected improvement by feasibility probabilities computed from constraint GPs at the relevant nodes. Because BOFN uses SAA with reparameterized sampling (astudillo2021bayesianoptimizationof pages 4-6), the constraint probabilities can be evaluated on the same posterior samples, maintaining differentiability. Wang et al. demonstrate this pattern for composite constrained BO, where a variational GP classifier models feasibility and its output is factored into the acquisition function (wang2025constrainedcompositebayesian pages 1-4). In BoTorch, this is achievable via `ConstrainedMCObjective` composed with the BOFN network posterior (balandat2019botorchprogrammablebayesian pages 6-7).

**Key principle:** Enforce constraints at the earliest possible node where the relevant physics is observable. Constraints at downstream nodes (e.g., hot cracking from Node 0 outputs) naturally propagate backward through the BOFN acquisition optimization because the global decision vector x is optimized jointly.

---

### (d) Batch Evaluation in BOFN

**Batch BOFN for LPBF build plates requires combining q-EI-FN for same-stage parallel proposals with KG-style partial evaluation for mixed-stage scheduling.**

Batch BO in function networks proceeds by jointly sampling from the posterior over all candidate points in the batch using Monte Carlo estimation with the reparameterization trick, making the acquisition function differentiable with respect to all batch members simultaneously (alabed2025towardsefficienttuning pages 108-111). The SAA approach used in BOFN—fixing base samples to create a deterministic objective—naturally extends to batch settings where q candidates are evaluated simultaneously (astudillo2021bayesianoptimizationof pages 4-6, alabed2025towardsefficienttuning pages 108-111).

**For the mixed-stage LPBF scenario** (some candidates at single-track, others at density cubes on the same build plate):

1. **Constituent-evaluation KG:** Toscano-Palmerin and Frazier propose a KG variant that jointly selects which candidate x and which constituent w (i.e., which DAG node) to evaluate: KG_n(x,w) = E_n[μ*_{n+1} − μ*_n | (x_{n+1},w_{n+1})=(x,w)] (astudillo2021thinkinginsidethe pages 10-12, astudillo2021thinkinginsidethe pages 12-14). This naturally handles the decision of whether to run a cheap single-track experiment on a new composition or to advance a promising candidate to density-cube evaluation.

2. **Batch extension:** For a build plate with q slots, the optimizer selects q (x_i, w_i) pairs where each w_i specifies the DAG stage (Node 2a single-track, Node 2b scan strategy pad, Node 2d density cube, or Node 3 tensile bar). The batch q-KG acquisition values the joint information gain from all q evaluations (astudillo2021thinkinginsidethe pages 12-14).

3. **Practical scheduling for LPBF:** On a single build plate, allocate slots as follows: a fraction (e.g., 60%) to cheap exploratory evaluations (single-track or small pads for new or uncertain compositions at Nodes 2a–2b), and the remainder (e.g., 40%) to confirmatory evaluations (density cubes and tensile bars at Nodes 2d–3 for promising compositions). The KG-based acquisition naturally balances this allocation because exploratory evaluations at early nodes provide high information per cost, while confirmatory evaluations at late nodes directly improve the estimate of the final objective.

4. **Asynchronous handling:** BoTorch supports pending-point conditioning via the `@concatenate_pending_points` decorator (balandat2019botorchprogrammablebayesian pages 6-7), which is essential when builds at different stages complete at different times.

---

### (e) Practical Implementation in BoTorch/Ax

**The BOFN DAG should be implemented primarily in BoTorch, with Ax serving as the orchestration and experiment-management layer.**

**BoTorch layer (core BOFN logic):**

BoTorch provides the necessary programmable abstractions for BOFN: the `Model` API requires only a `posterior()` method returning a `Posterior` object, and `Posterior` requires `rsample()` for MC sampling (chang2019bayesianhyperparameteroptimization pages 4-9). The recommended implementation path is:

1. **`FunctionNetworkModel`:** A custom BoTorch `Model` that wraps K independent node GPs (each a `SingleTaskGP` or `SaasFullyBayesianSingleTaskGP`). The `posterior()` method propagates samples recursively through the DAG using reparameterized sampling: for each node k, draw ĥ_k(x) = μ_{n,k}(x_{I(k)}, ĥ_{J(k)}(x)) + σ_{n,k}(...)·Z_k (astudillo2021bayesianoptimizationof pages 4-6).

2. **`EI_FN` acquisition function:** Subclass `MCAcquisitionFunction`. In `forward()`, draw M posterior samples through the network, compute improvement over the best observed objective, and average. SAA (fixing base normal draws Z) makes this deterministic for quasi-second-order optimizers (astudillo2021bayesianoptimizationof pages 4-6, alabed2025towardsefficienttuning pages 108-111).

3. **Constraint integration:** Use `ConstrainedMCObjective` or multiply EI-FN by feasibility probabilities computed from constraint-node GPs on the same posterior samples.

4. **Optimization:** Use `optimize_acqf()` with multi-start L-BFGS-B over the global decision vector x (balandat2019botorchprogrammablebayesian pages 6-7).

5. **SAASBO at nodes:** For each node GP, use `SaasFullyBayesianSingleTaskGP` with the hierarchical half-Cauchy prior (τ ~ HC(α), ρ_i ~ HC(τ)) and NUTS inference (eriksson2021highdimensionalbayesianoptimization pages 3-4, eriksson2021highdimensionalbayesianoptimization pages 2-3). Average the acquisition over posterior hyperparameter samples (eriksson2021highdimensionalbayesianoptimization pages 4-5).

6. **RGPE for transfer learning:** Maintain serialized base GPs from prior alloy campaigns. At optimization time, construct an RGPE ensemble for each node GP, computing ranking-loss-based weights to blend base and target models (feurer2018scalablemetalearningfor pages 3-6, feurer2018practicaltransferlearning pages 8-11, feurer2018scalablemetalearningfor pages 1-3).

**Ax layer (orchestration):**

Ax provides experiment lifecycle management through its `Client` API, `GenerationStrategy`, and `GenerationNode` abstractions (kashtelyan2025axaplatform pages 6-8, kashtelyan2025axaplatform pages 3-6). The recommended integration:

1. **Custom `GenerationNode`:** Define a `BOFNGenerationNode` that wraps the BoTorch `FunctionNetworkModel` and `EI_FN` acquisition. This node produces candidate suggestions via BoTorch's `optimize_acqf()` and returns them to Ax's trial system (kashtelyan2025axaplatform pages 17-22, kashtelyan2025axaplatform pages 6-8).

2. **`GenerationStrategy`:** Compose with standard Ax initialization (Sobol warm-start) followed by transition to the BOFN generation node: e.g., `[SobolNode(num_trials=2*d), BOFNGenerationNode()]` with `TransitionCriteria` based on trial count (kashtelyan2025axaplatform pages 6-8).

3. **`SurrogateSpec` / `ModelConfig`:** While Ax's Modular BoTorch Generator (MBG) can dispatch to `SingleTaskMultiFidelityGP` for fidelity features and `MultiTaskGP` for task features automatically (kashtelyan2025axaplatform pages 17-22), the BOFN DAG requires a custom `Model` that is not covered by MBG's default dispatch logic. Therefore, the BOFN model must be provided explicitly via a custom `Surrogate` wrapper or a fully custom `GenerationNode`.

4. **Benchmarking:** Ax's `BenchmarkProblem` interface (kashtelyan2025axaplatform pages 17-22) can be used to evaluate the BOFN architecture on synthetic LPBF-like test problems (e.g., nested Rosenbrock or Alpine2 function networks from Astudillo & Frazier) before deploying on real experiments.

5. **Experiment management:** Use Ax's ask-tell loop (`get_next_trials()` / `complete_trial()`) for integration with physical LPBF experiments, with `Runner` and `Metric` abstractions for automated deployment if connected to a machine control system (kashtelyan2025axaplatform pages 3-6).

**What is practically achievable with BoTorch 0.17+ and Ax today:**

- SAASBO node GPs: Available via `SaasFullyBayesianSingleTaskGP` in BoTorch.
- Constrained MC acquisition functions: Available via `ConstrainedMCObjective` and log-transformed variants (kashtelyan2025axaplatform pages 22-25).
- Multi-fidelity GPs: Available via `SingleTaskMultiFidelityGP` in BoTorch and supported in Ax's MBG.
- RGPE: Available in the Ax codebase (feurer2018scalablemetalearningfor pages 6-8, feurer2018scalablemetalearningfor pages 13-15).
- BOFN DAG posterior propagation and EI-FN: Astudillo & Frazier's reference implementation exists at [github.com/RaulAstudillo06/BOFN](https://github.com/RaulAstudillo06/BOFN), but there is no off-the-shelf `FunctionNetworkModel` class in BoTorch's standard API as of current releases. The reference implementation can serve as a starting point for integration into BoTorch's modular framework.
- Partial-evaluation KG for function networks: **Requires custom research code**, adapting the KG constituent-evaluation framework to the specific DAG topology. Buathong et al. (2024) extend BOFN to partial evaluations with their p-KGFN acquisition function.

The primary development effort is in adapting the existing EI-FN implementation from Astudillo's BOFN repo into BoTorch's modular framework and extending it for our VCL-specific DAG. Once this core exists, integration with Ax for experiment management, SAASBO for per-node variable selection, RGPE for cross-alloy transfer, and constrained/batch extensions all compose naturally through BoTorch's modular design.

References

1. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

2. (astudillo2021bayesianoptimizationof pages 4-6): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

3. (astudillo2021bayesianoptimizationof pages 2-4): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

4. (astudillo2021bayesianoptimizationof pages 6-8): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

5. (feurer2018scalablemetalearningfor pages 6-8): M Feurer, B Letham, and E Bakshy. Scalable meta-learning for bayesian optimization using ranking-weighted gaussian process ensembles. Unknown journal, 2018.

6. (feurer2018scalablemetalearningfor pages 3-6): M Feurer, B Letham, and E Bakshy. Scalable meta-learning for bayesian optimization using ranking-weighted gaussian process ensembles. Unknown journal, 2018.

7. (eriksson2021highdimensionalbayesianoptimization pages 3-4): David Eriksson and Martin Jankowiak. High-dimensional bayesian optimization with sparse axis-aligned subspaces. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2103.00349, doi:10.48550/arxiv.2103.00349. This article has 290 citations.

8. (eriksson2021highdimensionalbayesianoptimization pages 2-3): David Eriksson and Martin Jankowiak. High-dimensional bayesian optimization with sparse axis-aligned subspaces. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2103.00349, doi:10.48550/arxiv.2103.00349. This article has 290 citations.

9. (astudillo2021thinkinginsidethe pages 8-10): Raul Astudillo and Peter I. Frazier. Thinking inside the box: a tutorial on grey-box bayesian optimization. 2021 Winter Simulation Conference (WSC), pages 1-15, Dec 2021. URL: https://doi.org/10.48550/arxiv.2201.00272, doi:10.48550/arxiv.2201.00272. This article has 79 citations.

10. (wu2018continuousfidelitybayesianoptimization pages 4-7): J Wu and PI Frazier. Continuous-fidelity bayesian optimization with knowledge gradient. Unknown journal, 2018.

11. (wu2018continuousfidelitybayesianoptimization pages 1-3): J Wu and PI Frazier. Continuous-fidelity bayesian optimization with knowledge gradient. Unknown journal, 2018.

12. (wu2018continuousfidelitybayesianoptimization pages 3-4): J Wu and PI Frazier. Continuous-fidelity bayesian optimization with knowledge gradient. Unknown journal, 2018.

13. (wu2020practicalmultifidelitybayesian pages 2-3): Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier, and Andrew Gordon Wilson. Practical multi-fidelity bayesian optimization for hyperparameter tuning. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.1903.04703, doi:10.48550/arxiv.1903.04703. This article has 246 citations.

14. (wu2020practicalmultifidelitybayesian pages 1-2): Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier, and Andrew Gordon Wilson. Practical multi-fidelity bayesian optimization for hyperparameter tuning. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.1903.04703, doi:10.48550/arxiv.1903.04703. This article has 246 citations.

15. (wang2025constrainedcompositebayesian pages 1-4): Fanjin Wang, Maryam Parhizkar, Anthony Harker, and Mohan Edirisinghe. Constrained composite bayesian optimization for rational synthesis of polymeric particles. ArXiv, Nov 2025. URL: https://doi.org/10.48550/arxiv.2411.10471, doi:10.48550/arxiv.2411.10471. This article has 4 citations.

16. (ungredda2024bayesianoptimisationfor pages 1-3): Juan Ungredda and Juergen Branke. Bayesian optimisation for constrained problems. ACM Transactions on Modeling and Computer Simulation, 34:1-26, Apr 2024. URL: https://doi.org/10.1145/3641544, doi:10.1145/3641544. This article has 41 citations and is from a peer-reviewed journal.

17. (letham2019constrainedbayesianoptimization pages 3-6): Benjamin Letham, Brian Karrer, Guilherme Ottoni, and Eytan Bakshy. Constrained bayesian optimization with noisy experiments. Bayesian Analysis, Jun 2019. URL: https://doi.org/10.1214/18-ba1110, doi:10.1214/18-ba1110. This article has 484 citations and is from a domain leading peer-reviewed journal.

18. (letham2019constrainedbayesianoptimization pages 1-3): Benjamin Letham, Brian Karrer, Guilherme Ottoni, and Eytan Bakshy. Constrained bayesian optimization with noisy experiments. Bayesian Analysis, Jun 2019. URL: https://doi.org/10.1214/18-ba1110, doi:10.1214/18-ba1110. This article has 484 citations and is from a domain leading peer-reviewed journal.

19. (eriksson2021scalableconstrainedbayesian pages 2-3): David Eriksson and Matthias Poloczek. Scalable constrained bayesian optimization. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2002.08526, doi:10.48550/arxiv.2002.08526. This article has 203 citations.

20. (eriksson2021scalableconstrainedbayesian pages 1-2): David Eriksson and Matthias Poloczek. Scalable constrained bayesian optimization. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2002.08526, doi:10.48550/arxiv.2002.08526. This article has 203 citations.

21. (alabed2025towardsefficienttuning pages 108-111): S Alabed. Towards efficient tuning of computer systems: auto-structured bayesian optimization from system metrics. Unknown journal, 2025.

22. (astudillo2021thinkinginsidethe pages 12-14): Raul Astudillo and Peter I. Frazier. Thinking inside the box: a tutorial on grey-box bayesian optimization. 2021 Winter Simulation Conference (WSC), pages 1-15, Dec 2021. URL: https://doi.org/10.48550/arxiv.2201.00272, doi:10.48550/arxiv.2201.00272. This article has 79 citations.

23. (astudillo2021thinkinginsidethe pages 10-12): Raul Astudillo and Peter I. Frazier. Thinking inside the box: a tutorial on grey-box bayesian optimization. 2021 Winter Simulation Conference (WSC), pages 1-15, Dec 2021. URL: https://doi.org/10.48550/arxiv.2201.00272, doi:10.48550/arxiv.2201.00272. This article has 79 citations.

24. (balandat2019botorchprogrammablebayesian pages 6-7): Maximilian Balandat, B. Karrer, Daniel R. Jiang, Sam Daulton, Benjamin Letham, A. Wilson, and E. Bakshy. Botorch: programmable bayesian optimization in pytorch. ArXiv, Oct 2019. URL: https://doi.org/10.48550/arxiv.1910.06403, doi:10.48550/arxiv.1910.06403. This article has 130 citations.

25. (astudillo2021thinkinginsidethe pages 6-8): Raul Astudillo and Peter I. Frazier. Thinking inside the box: a tutorial on grey-box bayesian optimization. 2021 Winter Simulation Conference (WSC), pages 1-15, Dec 2021. URL: https://doi.org/10.48550/arxiv.2201.00272, doi:10.48550/arxiv.2201.00272. This article has 79 citations.

26. (chang2019bayesianhyperparameteroptimization pages 4-9): Daniel T. Chang. Bayesian hyperparameter optimization with botorch, gpytorch and ax. Preprint, Jan 2019. URL: https://doi.org/10.48550/arxiv.1912.05686, doi:10.48550/arxiv.1912.05686. This article has 30 citations.

27. (kashtelyan2025axaplatform pages 17-22): E Kashtelyan, D Eriksson, and M Balandat. Ax: a platform for adaptive experimentation. Unknown journal, 2025.

28. (kashtelyan2025axaplatform pages 6-8): E Kashtelyan, D Eriksson, and M Balandat. Ax: a platform for adaptive experimentation. Unknown journal, 2025.

29. (kashtelyan2025axaplatform pages 22-25): E Kashtelyan, D Eriksson, and M Balandat. Ax: a platform for adaptive experimentation. Unknown journal, 2025.

30. (kashtelyan2025axaplatform pages 3-6): E Kashtelyan, D Eriksson, and M Balandat. Ax: a platform for adaptive experimentation. Unknown journal, 2025.

31. (kashtelyan2025axaplatform pages 1-3): E Kashtelyan, D Eriksson, and M Balandat. Ax: a platform for adaptive experimentation. Unknown journal, 2025.

32. (feurer2018scalablemetalearningfor pages 1-3): M Feurer, B Letham, and E Bakshy. Scalable meta-learning for bayesian optimization using ranking-weighted gaussian process ensembles. Unknown journal, 2018.

33. (eriksson2021highdimensionalbayesianoptimization pages 4-5): David Eriksson and Martin Jankowiak. High-dimensional bayesian optimization with sparse axis-aligned subspaces. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2103.00349, doi:10.48550/arxiv.2103.00349. This article has 290 citations.

34. (astudillo2021thinkinginsidethe pages 4-6): Raul Astudillo and Peter I. Frazier. Thinking inside the box: a tutorial on grey-box bayesian optimization. 2021 Winter Simulation Conference (WSC), pages 1-15, Dec 2021. URL: https://doi.org/10.48550/arxiv.2201.00272, doi:10.48550/arxiv.2201.00272. This article has 79 citations.

35. (astudillo2021thinkinginsidethe pages 1-2): Raul Astudillo and Peter I. Frazier. Thinking inside the box: a tutorial on grey-box bayesian optimization. 2021 Winter Simulation Conference (WSC), pages 1-15, Dec 2021. URL: https://doi.org/10.48550/arxiv.2201.00272, doi:10.48550/arxiv.2201.00272. This article has 79 citations.

36. (feurer2018practicaltransferlearning pages 8-11): Matthias Feurer, Benjamin Letham, Frank Hutter, and Eytan Bakshy. Practical transfer learning for bayesian optimization. Preprint, Jan 2018. URL: https://doi.org/10.48550/arxiv.1802.02219, doi:10.48550/arxiv.1802.02219. This article has 68 citations.

37. (feurer2018scalablemetalearningfor pages 13-15): M Feurer, B Letham, and E Bakshy. Scalable meta-learning for bayesian optimization using ranking-weighted gaussian process ensembles. Unknown journal, 2018.