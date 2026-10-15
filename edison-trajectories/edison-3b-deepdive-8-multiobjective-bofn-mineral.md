# Edison Scientific LITERATURE_HIGH Output — Multi-Objective BOFN with Critical Mineral Content

**Task ID:** `3c1b2b3d-7d9d-4b5f-9da0-b2137069b186`
**Mode:** LITERATURE_HIGH | **Date:** 2026-04-10 | **Size:** ~41K chars
**Part of:** Topic 3B Deep-Dive Series (10 queries, ~331K chars total)

> *Raw Edison Scientific output below. The query prompt appears first, followed by the model's structured response.*

---

Question: 
RESEARCH QUESTION: What is the technical feasibility of incorporating critical mineral content as an objective in Bayesian Optimization of Function Networks (BOFN)?

Context: Topic 3B requires "reducing demand for critical minerals." FLAIME uses BOFN (9-node DAG of GP models) for optimization. Need to assess whether "minimize critical mineral content" can be rigorously incorporated as an optimization objective alongside mechanical performance.

Investigate:
1. Multi-objective Bayesian optimization (MOBO) for materials: state of the art, key references
2. How to quantify "critical mineral content" as an objective — by mass fraction? by supply risk index? by cost?
3. Pareto optimization for alloy composition: {UTS, elongation, critical_mineral_content} — has this been done?
4. Astudillo & Frazier (2021) BOFN paper: does it support multi-objective extensions?
5. Buathong et al. (2024) partial KG for function networks: multi-objective capability?
6. Constrained vs. multi-objective formulation: which is better for "minimize Be content while maintaining performance"?
7. How to handle compositional constraints in BOFN (e.g., "total critical mineral ppm ≤ X")?
8. Published examples of materials BO with supply chain/cost/sustainability objectives
9. CALPHAD integration: can Thermo-Calc provide critical mineral content as a computed property?
10. What would the BOFN DAG look like with a critical mineral objective node?

Cite all sources.


## Technical feasibility assessment

Incorporating “minimize critical mineral content” as an objective in a BOFN-style Bayesian optimization workflow is technically feasible, but **not “out-of-the-box” in the original BOFN formulation**. Astudillo & Frazier’s BOFN and Buathong et al.’s partial-evaluation extension (p-KGFN) are both formulated for **a single scalar leaf objective** (maximize the final node output), so adding a rigorous critical-mineral objective requires either (i) **scalarizing** mineral burden into a single utility so BOFN can remain single-objective, or (ii) **extending BOFN to multiple leaf nodes** and adopting **multi-objective Bayesian optimization (MOBO)** acquisition functions such as EHVI/qEHVI. The broader MOBO literature and multiple materials case studies (including supply-risk-aware alloy design) demonstrate that sustainability- and supply-risk-type objectives can be rigorously optimized alongside mechanical performance using GP surrogates and Pareto/hypervolume-based acquisitions.

| Topic | Reference | What it shows (1 sentence) | Relevance to BOFN+critical-mineral objective (1 sentence) | Citation ID placeholder |
|---|---|---|---|---|
| MOBO method | Daulton et al. 2020, qEHVI | qEHVI provides a differentiable expected hypervolume improvement acquisition for parallel and constrained multi-objective BO, directly targeting Pareto-front quality. | This is the clearest acquisition-function template if BOFN is extended from one scalar objective to multiple leaf objectives including critical-mineral minimization. | (daulton2020differentiableexpectedhypervolume pages 1-2) |
| MOBO method | Daulton et al. 2022, MORBO | MORBO scales MOBO to higher-dimensional spaces using local trust regions and hypervolume-based selection while still optimizing Pareto fronts under black-box objectives/constraints. | If BOFN inputs include many composition and process variables, MORBO-like locality ideas could help a multi-objective BOFN remain tractable. | (daulton2022multiobjectivebayesianoptimization pages 2-3, daulton2022multiobjectivebayesianoptimization pages 9-10, daulton2022multiobjectivebayesianoptimization pages 1-2) |
| MOBO method | Suzuki et al. 2020, PFES | PFES is an entropy-based MOBO criterion that reduces uncertainty in the Pareto frontier rather than using scalarization or raw hypervolume only. | It shows BOFN need not be tied to EHVI alone if a multi-objective extension is pursued and frontier-learning is preferred. | (suzuki2020multiobjectivebayesianoptimization pages 1-2) |
| MOBO / constrained formulation | Tran et al. 2022, srMO-BO-3GP | srMO-BO-3GP combines scalarization, a GP for unknown constraints, and a Pareto classifier, demonstrating a practical constrained-MOBO architecture. | This supports a formulation where mechanical requirements are treated as constraints and critical-mineral burden is optimized either as an objective or via scalarized trade-offs. | (tran2022srmobo3gpasequential pages 12-13) |
| BOFN core method | Astudillo & Frazier 2021, BOFN | BOFN models each DAG node with a GP and optimizes a single scalar leaf-node objective via expected improvement under the implied posterior. | It confirms current BOFN is rigorously single-objective, so adding a critical-mineral objective requires a true methodological extension rather than a parameter tweak. | (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 9-11, astudillo2021bayesianoptimizationof pages 21-23) |
| BOFN partial evaluations | Buathong et al. 2023/2024, p-KGFN | p-KGFN extends BOFN to cost-aware partial evaluations by selecting which node/input to measure based on expected gain in the final-node posterior mean per unit cost. | It improves evaluation efficiency for BOFN workflows, but still assumes a single final objective, so multi-objective capability would need to be added on top of p-KGFN. | (buathong2506fastbayesianoptimization pages 2-4, buathong2023bayesianoptimizationof pages 1-2, buathong2023bayesianoptimizationof pages 12-15, buathong2023bayesianoptimizationof pages 7-8) |
| Criticality metric | Cimprich et al. 2019, GeoPolRisk / ESP / ESSENZ | Product-level supply-risk assessment can be computed by applying material-specific characterization factors to inventory flows and BOM data, including critical materials used in small amounts. | This provides a rigorous route to define a critical-mineral objective from alloy composition rather than using only raw wt.%. | (cimprich2019rawmaterialcriticality pages 1-2, cimprich2019rawmaterialcriticality pages 8-9, cimprich2019rawmaterialcriticality pages 2-3) |
| Criticality metric | Mancini et al. 2018, supply-risk CFs | Supply-risk characterization factors can be used directly, exponentially transformed, or normalized by production to emphasize small-market specialty metals in LCA-style assessments. | This gives multiple defensible scalarizations for a critical-mineral objective node, depending on whether FLAIME wants mass sensitivity or scarcity sensitivity. | (mancini2018characterizationofraw pages 1-2) |
| Alloy criticality metric | Ferro & Bonollo 2019, alloy critical index | The alloy criticality index (CIA) and abundance-risk scoring aggregate elemental criticality into an alloy-level score per unit mass and per unit function. | This is especially relevant if the program wants an alloy-centric critical-mineral metric instead of a full product-system LCA metric. | (ferro2019materialsselectionin pages 1-2, ferro2019materialsselectionin pages 9-9) |
| Alloy supply-risk aggregation | Helbig et al. 2020, Ni-based superalloys | Twelve elemental indicators are aggregated into alloy-level supply-risk scores using multiple schemes, including cost-share weighting that changes rankings substantially. | It shows that aggregation choice matters and supports testing several objective definitions for critical-mineral burden before operationalizing one in BOFN. | (helbig2020supplyriskconsiderations pages 1-3) |
| Product vulnerability / criticality metric | Lütkehaus et al. 2022, EPI | Economic Product Importance (EPI) combines material flow, cost share, substitutability, and supply disruption probability into product-specific overall criticality. | This offers a stronger alternative to simple mass fraction when the intent is to minimize functional dependence on critical minerals, not just their presence. | (lutkehaus2022measuringrawmaterialcriticality pages 1-2) |
| Materials example | Mulukutla et al. 2024, supply-risk-aware alloy MOBBO | Multi-objective batch BO was used to identify Pareto-optimal HEAs that balance performance with minimized supply risk, with CALPHAD/ROM constraints and discrete composition screening. | This is the closest direct precedent showing that a supply-risk or critical-mineral objective can be rigorously optimized alongside materials performance. | (mulukutla2024supplyriskawarealloy pages 1-2, mulukutla2024supplyriskawarealloy pages 6-8, mulukutla2024supplyriskawarealloy pages 10-12) |
| Sustainability example | Ament et al. 2023, sustainable concrete MOBO | Multi-objective BO was used to trade off compressive strength against global warming potential using GP surrogates and EHVI. | It demonstrates that sustainability-type objectives are already handled naturally within MOBO and can coexist with performance objectives. | (ament2310sustainableconcretevia pages 1-3) |
| Sustainability / cost example | Vincent et al. 2025, carbon-footprint CBO | Contextual BO reduced carbon footprint and cost while maintaining quality, showing BO can optimize sustainability metrics under varying external conditions. | This supports the practicality of adding non-mechanical objectives such as critical-mineral burden, cost, or supply risk in an engineering BO workflow. | (vincent2025optimizingprocessparameters pages 1-2) |
| CALPHAD integration / simplex handling | Hastings et al. 2026, Thermo-Calc data + discretized simplex BO | Thermo-Calc-generated property libraries were explored with batch BO over explicitly discretized composition simplices, using barycentric/affine projections and clustering for batch selection. | This gives an implementation pattern for enforcing sum-to-one composition constraints and adding a composition-derived critical-mineral metric as a cheap computed property. | (hastings2026leveragingdomainknowledge pages 2-3) |
| CALPHAD-based MOBO | Sundar et al. 2025, CALPHAD-based alloy MOBO | High-throughput CALPHAD outputs were used directly as multiple BO objectives, and MOBO found good alloys after exploring only a small fraction of composition space. | It shows Thermo-Calc/CALPHAD properties can be objective nodes in an active optimization loop, so a critical-mineral score computed from composition can be added similarly. | (sundar2025calphadbasedbayesianoptimization pages 1-2) |


*Table: This table compiles the key methodological and application references needed to assess whether a critical-mineral objective can be added rigorously to BOFN. It links MOBO methods, criticality metrics, BOFN limitations, and CALPHAD-enabled materials examples to the specific feasibility question.*

## 1. MOBO for materials: state of the art and key references

**Main MOBO families used in materials/engineering**:

1. **Hypervolume-based acquisitions** (most common in modern MOBO toolchains): Expected Hypervolume Improvement (EHVI) and parallel/batch versions (qEHVI), including differentiable Monte-Carlo gradient approaches (daulton2020differentiableexpectedhypervolume pages 1-2). These methods explicitly target high-quality coverage of the Pareto frontier and are widely benchmarked and used in materials-focused MOBO studies (mamun2025accelerateddevelopmentof pages 1-4).

2. **Scalarization-based MOBO**: Convert multiple objectives to one (e.g., weighted sum, weighted Tchebycheff; ParEGO is a classic approach). Tran et al. describe a constrained design MOBO framework using a regularized Tchebycheff scalarization and separate GP models for constraints and Pareto classification (tran2022srmobo3gpasequential pages 12-13). Reviews in materials informatics emphasize that scalarization can bias solutions and can return a single Pareto point per weight setting (xu2025multiobjectiveoptimizationin pages 7-9).

3. **Information/entropy-based MOBO**: PFES (Pareto-frontier entropy search) targets uncertainty reduction in the Pareto frontier itself and can handle settings like decoupled observations (suzuki2020multiobjectivebayesianoptimization pages 1-2).

4. **Scalable/high-dimensional MOBO**: MORBO uses trust regions and hypervolume-based acquisition to scale to high dimensions and many evaluations, addressing typical GP cubic-scaling limitations (daulton2022multiobjectivebayesianoptimization pages 2-3, daulton2022multiobjectivebayesianoptimization pages 1-2).

**Materials-specific evidence**: A materials-alloy MOBO benchmarking study reports strong performance of qEHVI for 1–3 objective aluminum-alloy problems under tight evaluation budgets (mamun2025accelerateddevelopmentof pages 1-4). A sustainability materials study uses multi-objective BO with EHVI to trade off compressive strength and global warming potential in concrete mix design (ament2310sustainableconcretevia pages 1-3).

## 2. Quantifying “critical mineral content” as an objective

“Critical mineral content” can be quantified at multiple rigor levels, depending on whether Topic 3B interprets “reduce demand for critical minerals” as (a) directly reducing mass usage, or (b) reducing exposure to supply disruption risk/criticality.

### A. Direct composition-based metrics (simple, auditable)

- **Mass fraction / wt.% / at.%** of a designated set of critical elements (e.g., sum of wt.% for {Co, Nb, Ta, W, Re, …}) is straightforward, differentiable/cheap to compute, and naturally fits BO objectives or constraints.
- **ppm caps** (e.g., “total Be ppm ≤ X”) are constraints that can be enforced directly in the feasible domain X (see §7 and §6). BOFN already treats constraints by restricting X (astudillo2021bayesianoptimizationof pages 21-23).

### B. Supply-risk / criticality-weighted metrics (more rigorous for “criticality”)

Product-level “supply risk” methods in industrial ecology treat criticality as a set of characterization factors (CFs) applied to the bill of materials (BOM) / inventory flows:

- **GeoPolRisk, ESP, ESSENZ** are explicitly reviewed as product-level supply risk/criticality methods that compute supply-risk metrics via CFs applied to inventory flows, and the authors caution not to overlook small-mass but functionally important materials (cimprich2019rawmaterialcriticality pages 1-2, cimprich2019rawmaterialcriticality pages 2-3). Differences include whether CFs effectively cancel out mass magnitude (GeoPolRisk) versus scaling with amounts used (ESP/ESSENZ) (cimprich2019rawmaterialcriticality pages 8-9).
- **Supply-risk characterization factor design choices** include using supply risk “as is,” exponential transforms (to spread values), or **supply risk / production** ratios to emphasize small-market specialty metals, proposed as potentially better reflecting CRM importance in EU LCA contexts (mancini2018characterizationofraw pages 1-2).

### C. Alloy-level indices and cost-share weightings

- Ferro & Bonollo define an **Alloy Criticality Index (CIA)** and abundance-risk scoring (ARL based on crustal abundance), aiming to quantify raw-material criticality per unit alloy mass and then per unit function (ferro2019materialsselectionin pages 1-2, ferro2019materialsselectionin pages 9-9).
- Helbig et al. assess elemental supply risk with multiple indicators and aggregate to alloy-level risk using multiple schemes; a **cost-share aggregation** strongly affects rankings (e.g., Re drives higher risk when present), showing aggregation choice is consequential (helbig2020supplyriskconsiderations pages 1-3).
- Lütkehaus et al. propose **economic product importance (EPI)** combining material flows, cost share, substitutability and then combining with supply disruption probability to yield product-specific overall criticality (lutkehaus2022measuringrawmaterialcriticality pages 1-2).

**Implication for BO**: any of these can be used as an objective node because they are (i) computed deterministically from composition and external CF tables, or (ii) predicted by a model (e.g., supply-risk predictor). Deterministic computation makes this objective “cheap,” which can be exploited in constrained-MOBO settings where expensive constraints dominate (mathern2021multiobjectiveconstrainedbayesian pages 1-2).

## 3. Pareto optimization for alloy composition with strength/ductility and criticality: precedent

- Multi-objective BO for alloy design optimizing mechanical performance (e.g., strength and ductility) is demonstrated in Mg alloy design using GP surrogates and a MOBO loop (ghorbani2024anactivemachine pages 1-2) and in a batch-MOBO HEA experimental workflow producing multi-objective Pareto sets in composition space (hastings2024aninteroperablemulti pages 1-2, hastings2024aninteroperablemulti pages 7-8).
- Most directly aligned with “critical minerals/supply risk”: Mulukutla et al. explicitly incorporate **supply risk indices as objectives** in a multi-objective batch Bayesian optimization workflow to identify Pareto-optimal HEAs balancing performance and minimized supply risk (mulukutla2024supplyriskawarealloy pages 1-2, mulukutla2024supplyriskawarealloy pages 6-8). This provides strong precedent that an objective like “critical mineral burden/supply risk” can be optimized jointly with performance.

## 4. Astudillo & Frazier (2021) BOFN: multi-objective support?

BOFN is formulated as optimization over a **directed acyclic function network** where each node is modeled by an independent GP, and the **single leaf node output** is the scalar objective to maximize over X (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2). Their acquisition is expected improvement (EI) computed under the induced posterior on the objective, optimized via sample-average approximation due to non-Gaussianity (astudillo2021bayesianoptimizationof pages 1-2).

In the examined sections, **multi-objective optimization is not addressed**; constraints are represented by restricting the feasible domain X (e.g., simplex-like Σxi≤1 constraints appear in examples) rather than via explicit constraint models/acquisitions (astudillo2021bayesianoptimizationof pages 21-23). Thus, BOFN supports adding a critical-mineral signal only through scalarization into a single objective, unless BOFN is extended.

## 5. Buathong et al. partial KG for function networks: multi-objective capability?

Buathong et al. (p-KGFN) extend BOFN to permit **partial evaluations** and **cost-aware** selection of which node to evaluate. The acquisition is knowledge-gradient-like: it estimates the expected increase in the **maximum posterior mean of the final-node objective** per unit evaluation cost (buathong2506fastbayesianoptimization pages 2-4, buathong2023bayesianoptimizationof pages 12-15). The objective remains a **single scalar final-node output yK(x)** (buathong2023bayesianoptimizationof pages 7-8).

No multi-objective extension is described in the provided excerpts; consequently, critical-mineral optimization would again require scalarization or a new multi-leaf MOBOFN variant.

## 6. Constrained vs multi-objective formulation for “minimize Be while maintaining performance”

Both are feasible; the best choice depends on the program’s decision-making needs.

### Option 6A: Constrained BO (recommended when performance thresholds are non-negotiable)

Formulate:
- Minimize: critical-mineral burden M(x)
- Subject to: UTS(x) ≥ UTS_min, elongation(x) ≥ e_min, etc.

This aligns with engineering practice: constraints often represent mandatory requirements and objectives represent what you optimize after feasibility. Structural-design BO explicitly motivates **expensive constraints + cheap objectives**, a pattern likely applicable if mechanical testing/simulation is expensive while M(x) is computed cheaply from composition (mathern2021multiobjectiveconstrainedbayesian pages 1-2).

The materials-optimization review notes **ε-constraint** / thresholding approaches are common: objectives can be treated as constraints to define a feasible set and reduce to single-objective search, but may yield only one Pareto solution per setting (xu2025multiobjectiveoptimizationin pages 7-9).

### Option 6B: Multi-objective BO (recommended when explicit trade-off curves are needed)

Formulate a 3-objective problem:
- Maximize UTS(x), maximize elongation(x), minimize M(x)

MOBO then returns a **Pareto set**; hypervolume-based acquisition is a standard approach (daulton2020differentiableexpectedhypervolume pages 1-2, mamun2025accelerateddevelopmentof pages 1-4). This is directly aligned with studies trading off performance vs sustainability (e.g., strength vs GWP) (ament2310sustainableconcretevia pages 1-3) and performance vs supply risk in alloys (mulukutla2024supplyriskawarealloy pages 1-2).

### Practical note
EHVI/qEHVI are powerful but can be computationally expensive as the number of objectives grows, and scaling issues are acknowledged in MOBO literature (daulton2020differentiableexpectedhypervolume pages 1-2, daulton2022multiobjectivebayesianoptimization pages 2-3). For 3 objectives ({UTS, elongation, criticality}) EHVI-family methods are commonly used in practice.

## 7. Handling compositional constraints in BOFN (including “total critical mineral ppm ≤ X”)

BOFN’s base formulation can encode constraints by restricting X (feasible domain) (astudillo2021bayesianoptimizationof pages 21-23). In alloy design, composition constraints typically include:

- **Simplex constraints**: xi ≥ 0, Σxi = 1 (and sometimes additional bounds xi ∈ [li, ui]).
- **Element caps**: e.g., Be ≤ X ppm (a linear inequality on composition variables).

Evidence from CALPHAD+BO alloy workflows shows two common implementation patterns:

1. **Discrete candidate library on a simplex grid**: Discretize composition space at fixed increments and optimize over this set; Hastings et al. discretize multi-component composition spaces at increments (e.g., 0.05) producing ~50,000 candidates and then run batch BO with EHVI (hastings2026leveragingdomainknowledge pages 2-3). Mulukutla et al. similarly discretize at 5 at.% increments and filter feasibility (mulukutla2024supplyriskawarealloy pages 10-12).

2. **Constraint filtering using cheap models**: Use CALPHAD/rule-of-mixtures to filter infeasible compositions cheaply before expensive evaluation, supporting constrained optimization in practice (mulukutla2024supplyriskawarealloy pages 10-12).

These patterns naturally accommodate ppm caps: the filter step simply removes candidates violating “critical mineral ppm ≤ X,” or the feasible domain definition forbids them.

## 8. Published examples of materials BO with supply chain/cost/sustainability objectives

- **Supply risk objective in alloy MOBO**: Mulukutla et al. embed supply risk indices as objectives in MOBBO to identify Pareto-optimal HEAs balancing performance and minimized supply risk (mulukutla2024supplyriskawarealloy pages 1-2, mulukutla2024supplyriskawarealloy pages 10-12).
- **Environmental impact objective in MOBO**: Sustainable concrete work optimizes strength vs global warming potential using MOBO with EHVI (ament2310sustainableconcretevia pages 1-3).
- **Carbon footprint and cost**: Contextual BO reduces carbon footprint and cost in additive manufacturing while maintaining quality (vincent2025optimizingprocessparameters pages 1-2).
- **Sustainability as explicit objective** in constrained MOBO: structural design with sustainability/buildability/performance objectives (mathern2021multiobjectiveconstrainedbayesian pages 1-2).

These collectively demonstrate that “non-traditional” objectives like sustainability, carbon, and supply risk are compatible with GP-based BO and MOBO.

## 9. CALPHAD integration: can Thermo-Calc provide critical mineral content as a computed property?

Thermo-Calc/CALPHAD is used to generate objective properties for BO loops (e.g., CTE and sigma dissolution temperature) in multi-objective alloy discovery (sundar2025calphadbasedbayesianoptimization pages 1-2). In other workflows, Thermo-Calc-generated property libraries are used as BO datasets with simplex discretization and geometry-aware batching (hastings2026leveragingdomainknowledge pages 2-3).

However, **critical mineral content itself is not a thermodynamic property**; it is a deterministic function of the composition vector (and possibly a CF table). Therefore, in a CALPHAD-integrated BOFN workflow:

- Compute M(x) directly from x (cheap, exact) using chosen definition (wt.% sum, CIA-like, CF-weighted supply risk, etc.) (cimprich2019rawmaterialcriticality pages 8-9, mancini2018characterizationofraw pages 1-2, ferro2019materialsselectionin pages 1-2).
- Optionally combine with CALPHAD-derived feasibility constraints/properties (e.g., phase constitution constraints) as in prior workflows (mulukutla2024supplyriskawarealloy pages 10-12, sundar2025calphadbasedbayesianoptimization pages 1-2).

## 10. What the BOFN DAG could look like with a critical-mineral objective node

Because BOFN is a DAG of node functions with a single scalar leaf objective by default (astudillo2021bayesianoptimizationof pages 2-4), there are two implementable designs:

### Design A (single-objective BOFN via scalarization; simplest)

- Keep one leaf node “utility” U(x) = scalarized objective.
- Add a cheap deterministic node for mineral burden M(x) computed from composition (using supply-risk CFs or alloy criticality index), and then define U(x) as a known deterministic function of predicted performance and M(x) (e.g., U = performance − λ·M, or a Tchebycheff/Chimera-like scalarization). Scalarization is a standard MO-to-SO technique (tran2022srmobo3gpasequential pages 12-13, xu2025multiobjectiveoptimizationin pages 5-7).

This requires no fundamental change to BOFN, only a revised objective definition.

### Design B (multi-leaf “MOBOFN”; more complex but yields Pareto sets)

- Create multiple leaf nodes representing objectives: y1(x)=UTS, y2(x)=elongation, y3(x)=M(x).
- Replace BOFN’s EI acquisition (single scalar) with an MO acquisition such as EHVI/qEHVI over the joint predictive distribution of objective leaves (daulton2020differentiableexpectedhypervolume pages 1-2, mamun2025accelerateddevelopmentof pages 1-4).

This is conceptually aligned with MOBO practice but is a genuine algorithmic extension beyond the BOFN paper, because BOFN’s implied posterior on a scalar objective already requires Monte Carlo/SAA; extending to EHVI would similarly require Monte Carlo integration over the induced joint posterior.

## Overall conclusion

**Technical feasibility is high**: critical-mineral minimization can be added rigorously to FLAIME’s BOFN-based optimization by defining a defensible mineral-burden metric (mass-based or criticality-weighted) and either (i) incorporating it into a single-objective scalar utility to retain BOFN/p-KGFN unchanged, or (ii) extending BOFN to multi-objective outputs and using established MOBO acquisitions (EHVI/qEHVI) to identify Pareto-optimal trade-offs. There is strong precedent in the broader materials BO literature for optimizing sustainability, carbon footprint, and supply risk alongside performance, including a direct supply-risk-aware alloy MOBBO case study. The main limitation is that BOFN and p-KGFN, as published, are single-objective; therefore a multi-objective BOFN implementation is an extension project rather than a configuration option (astudillo2021bayesianoptimizationof pages 2-4, buathong2506fastbayesianoptimization pages 2-4, mulukutla2024supplyriskawarealloy pages 1-2, ament2310sustainableconcretevia pages 1-3).

References

1. (daulton2020differentiableexpectedhypervolume pages 1-2): Samuel Daulton, Maximilian Balandat, and Eytan Bakshy. Differentiable expected hypervolume improvement for parallel multi-objective bayesian optimization. Text, Jan 2020. URL: https://doi.org/10.48550/arxiv.2006.05078, doi:10.48550/arxiv.2006.05078. This article has 506 citations and is from a peer-reviewed journal.

2. (daulton2022multiobjectivebayesianoptimization pages 2-3): Samuel Daulton, David Eriksson, Maximilian Balandat, and Eytan Bakshy. Multi-objective bayesian optimization over high-dimensional search spaces. Preprint, Jan 2022. URL: https://doi.org/10.48550/arxiv.2109.10964, doi:10.48550/arxiv.2109.10964. This article has 229 citations.

3. (daulton2022multiobjectivebayesianoptimization pages 9-10): Samuel Daulton, David Eriksson, Maximilian Balandat, and Eytan Bakshy. Multi-objective bayesian optimization over high-dimensional search spaces. Preprint, Jan 2022. URL: https://doi.org/10.48550/arxiv.2109.10964, doi:10.48550/arxiv.2109.10964. This article has 229 citations.

4. (daulton2022multiobjectivebayesianoptimization pages 1-2): Samuel Daulton, David Eriksson, Maximilian Balandat, and Eytan Bakshy. Multi-objective bayesian optimization over high-dimensional search spaces. Preprint, Jan 2022. URL: https://doi.org/10.48550/arxiv.2109.10964, doi:10.48550/arxiv.2109.10964. This article has 229 citations.

5. (suzuki2020multiobjectivebayesianoptimization pages 1-2): Shinya Suzuki, Shion Takeno, Tomoyuki Tamura, Kazuki Shitara, and Masayuki Karasuyama. Multi-objective bayesian optimization using pareto-frontier entropy. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.1906.00127, doi:10.48550/arxiv.1906.00127. This article has 130 citations.

6. (tran2022srmobo3gpasequential pages 12-13): Anh Tran, Michael S. Eldred, Scott McCann, and Yan Wang. Srmo-bo-3gp: a sequential regularized multi-objective bayesian optimization for constrained design applications using an uncertain pareto classifier. Journal of Mechanical Design, pages 1-15, Sep 2022. URL: https://doi.org/10.1115/1.4052445, doi:10.1115/1.4052445. This article has 12 citations and is from a domain leading peer-reviewed journal.

7. (astudillo2021bayesianoptimizationof pages 2-4): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

8. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

9. (astudillo2021bayesianoptimizationof pages 9-11): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

10. (astudillo2021bayesianoptimizationof pages 21-23): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

11. (buathong2506fastbayesianoptimization pages 2-4): Poompol Buathong and Peter I. Frazier. Fast bayesian optimization of function networks with partial evaluations. ArXiv, Jun 2506. URL: https://doi.org/10.48550/arxiv.2506.11456, doi:10.48550/arxiv.2506.11456. This article has 0 citations.

12. (buathong2023bayesianoptimizationof pages 1-2): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 11 citations.

13. (buathong2023bayesianoptimizationof pages 12-15): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 11 citations.

14. (buathong2023bayesianoptimizationof pages 7-8): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 11 citations.

15. (cimprich2019rawmaterialcriticality pages 1-2): Alexander Cimprich, Vanessa Bach, Christoph Helbig, Andrea Thorenz, Dieuwertje Schrijvers, Guido Sonnemann, Steven B. Young, Thomas Sonderegger, and Markus Berger. Raw material criticality assessment as a complement to environmental life cycle assessment: examining methods for product‐level supply risk assessment. Journal of Industrial Ecology, 23:1226-1236, Apr 2019. URL: https://doi.org/10.1111/jiec.12865, doi:10.1111/jiec.12865. This article has 123 citations and is from a domain leading peer-reviewed journal.

16. (cimprich2019rawmaterialcriticality pages 8-9): Alexander Cimprich, Vanessa Bach, Christoph Helbig, Andrea Thorenz, Dieuwertje Schrijvers, Guido Sonnemann, Steven B. Young, Thomas Sonderegger, and Markus Berger. Raw material criticality assessment as a complement to environmental life cycle assessment: examining methods for product‐level supply risk assessment. Journal of Industrial Ecology, 23:1226-1236, Apr 2019. URL: https://doi.org/10.1111/jiec.12865, doi:10.1111/jiec.12865. This article has 123 citations and is from a domain leading peer-reviewed journal.

17. (cimprich2019rawmaterialcriticality pages 2-3): Alexander Cimprich, Vanessa Bach, Christoph Helbig, Andrea Thorenz, Dieuwertje Schrijvers, Guido Sonnemann, Steven B. Young, Thomas Sonderegger, and Markus Berger. Raw material criticality assessment as a complement to environmental life cycle assessment: examining methods for product‐level supply risk assessment. Journal of Industrial Ecology, 23:1226-1236, Apr 2019. URL: https://doi.org/10.1111/jiec.12865, doi:10.1111/jiec.12865. This article has 123 citations and is from a domain leading peer-reviewed journal.

18. (mancini2018characterizationofraw pages 1-2): Lucia Mancini, Lorenzo Benini, and Serenella Sala. Characterization of raw materials based on supply risk indicators for europe. The International Journal of Life Cycle Assessment, 23:726-738, Mar 2018. URL: https://doi.org/10.1007/s11367-016-1137-2, doi:10.1007/s11367-016-1137-2. This article has 127 citations.

19. (ferro2019materialsselectionin pages 1-2): Paolo Ferro and Franco Bonollo. Materials selection in a critical raw materials perspective. Materials & Design, 177:107848, Sep 2019. URL: https://doi.org/10.1016/j.matdes.2019.107848, doi:10.1016/j.matdes.2019.107848. This article has 134 citations and is from a highest quality peer-reviewed journal.

20. (ferro2019materialsselectionin pages 9-9): Paolo Ferro and Franco Bonollo. Materials selection in a critical raw materials perspective. Materials & Design, 177:107848, Sep 2019. URL: https://doi.org/10.1016/j.matdes.2019.107848, doi:10.1016/j.matdes.2019.107848. This article has 134 citations and is from a highest quality peer-reviewed journal.

21. (helbig2020supplyriskconsiderations pages 1-3): Christoph Helbig, Alex M. Bradshaw, Andrea Thorenz, and Axel Tuma. Supply risk considerations for the elements in nickel-based superalloys. Resources, 9:106, Aug 2020. URL: https://doi.org/10.3390/resources9090106, doi:10.3390/resources9090106. This article has 25 citations.

22. (lutkehaus2022measuringrawmaterialcriticality pages 1-2): Hauke Lütkehaus, Christian Pade, Matthias Oswald, Urte Brand, Tobias Naegler, and Thomas Vogt. Measuring raw-material criticality of product systems through an economic product importance indicator: a case study of battery-electric vehicles. The International Journal of Life Cycle Assessment, 27:122-137, Dec 2022. URL: https://doi.org/10.1007/s11367-021-02002-z, doi:10.1007/s11367-021-02002-z. This article has 41 citations.

23. (mulukutla2024supplyriskawarealloy pages 1-2): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

24. (mulukutla2024supplyriskawarealloy pages 6-8): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

25. (mulukutla2024supplyriskawarealloy pages 10-12): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

26. (ament2310sustainableconcretevia pages 1-3): Sebastian Ament, Andrew Witte, Nishant Garg, and Julius Kusuma. Sustainable concrete via bayesian optimization. ArXiv, Oct 2310. URL: https://doi.org/10.48550/arxiv.2310.18288, doi:10.48550/arxiv.2310.18288. This article has 16 citations.

27. (vincent2025optimizingprocessparameters pages 1-2): Matteo C. Vincent, Markus Maier, and Konrad Wegener. Optimizing process parameters in manufacturing to reduce carbon footprint with contextual bayesian optimization. The International Journal of Advanced Manufacturing Technology, 139:3381-3390, Jul 2025. URL: https://doi.org/10.1007/s00170-025-16110-9, doi:10.1007/s00170-025-16110-9. This article has 4 citations.

28. (hastings2026leveragingdomainknowledge pages 2-3): Trevor Hastings, James D. Paramore, Brady Butler, and Raymundo Arróyave. Leveraging domain knowledge for optimal initialization in bayesian materials optimization. Digital Discovery, 5:277-289, Jan 2026. URL: https://doi.org/10.1039/d5dd00361j, doi:10.1039/d5dd00361j. This article has 0 citations and is from a peer-reviewed journal.

29. (sundar2025calphadbasedbayesianoptimization pages 1-2): Aditya Sundar, Xingru Tan, Shanshan Hu, and Michael C. Gao. Calphad-based bayesian optimization to accelerate alloy discovery for high-temperature applications. Journal of Materials Research, 40:112-122, Jan 2025. URL: https://doi.org/10.1557/s43578-024-01489-0, doi:10.1557/s43578-024-01489-0. This article has 8 citations and is from a peer-reviewed journal.

30. (mamun2025accelerateddevelopmentof pages 1-4): Osman Mamun, Markus Bause, and Bhuiyan Shameem Mahmood Ebna Hai. Accelerated development of multi-component alloys in discrete design space using bayesian multi-objective optimisation. Machine Learning: Science and Technology, 6:015001, Jan 2025. URL: https://doi.org/10.1088/2632-2153/ada47d, doi:10.1088/2632-2153/ada47d. This article has 7 citations and is from a peer-reviewed journal.

31. (xu2025multiobjectiveoptimizationin pages 7-9): Pengcheng Xu, Yingying Ma, Wencong Lu, Minjie Li, Wenyue Zhao, and Zhilong Dai. Multi-objective optimization in machine learning assisted materials design and discovery. Journal of Materials Informatics, Mar 2025. URL: https://doi.org/10.20517/jmi.2024.108, doi:10.20517/jmi.2024.108. This article has 27 citations.

32. (mathern2021multiobjectiveconstrainedbayesian pages 1-2): Alexandre Mathern, Olof Skogby Steinholtz, Anders Sjöberg, Magnus Önnheim, Kristine Ek, Rasmus Rempling, Emil Gustavsson, and Mats Jirstrand. Multi-objective constrained bayesian optimization for structural design. Structural and Multidisciplinary Optimization, 63:689-701, Sep 2021. URL: https://doi.org/10.1007/s00158-020-02720-2, doi:10.1007/s00158-020-02720-2. This article has 111 citations and is from a domain leading peer-reviewed journal.

33. (ghorbani2024anactivemachine pages 1-2): M. Ghorbani, M. Boley, P. N. H. Nakashima, and N. Birbilis. An active machine learning approach for optimal design of magnesium alloys using bayesian optimisation. Scientific Reports, Apr 2024. URL: https://doi.org/10.1038/s41598-024-59100-9, doi:10.1038/s41598-024-59100-9. This article has 25 citations and is from a peer-reviewed journal.

34. (hastings2024aninteroperablemulti pages 1-2): Trevor Hastings, Mrinalini Mulukutla, Danial Khatamsaz, Daniel Salas, Wenle Xu, Daniel Lewis, Nicole Person, Matthew Skokan, Braden Miller, James Paramore, Brady Butler, Douglas Allaire, Ibrahim Karaman, George Pharr, Ankit Srivastava, and Raymundo Arroyave. An interoperable multi objective batch bayesian optimization framework for high throughput materials discovery. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2405.08900, doi:10.48550/arxiv.2405.08900. This article has 1 citations.

35. (hastings2024aninteroperablemulti pages 7-8): Trevor Hastings, Mrinalini Mulukutla, Danial Khatamsaz, Daniel Salas, Wenle Xu, Daniel Lewis, Nicole Person, Matthew Skokan, Braden Miller, James Paramore, Brady Butler, Douglas Allaire, Ibrahim Karaman, George Pharr, Ankit Srivastava, and Raymundo Arroyave. An interoperable multi objective batch bayesian optimization framework for high throughput materials discovery. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2405.08900, doi:10.48550/arxiv.2405.08900. This article has 1 citations.

36. (xu2025multiobjectiveoptimizationin pages 5-7): Pengcheng Xu, Yingying Ma, Wencong Lu, Minjie Li, Wenyue Zhao, and Zhilong Dai. Multi-objective optimization in machine learning assisted materials design and discovery. Journal of Materials Informatics, Mar 2025. URL: https://doi.org/10.20517/jmi.2024.108, doi:10.20517/jmi.2024.108. This article has 27 citations.