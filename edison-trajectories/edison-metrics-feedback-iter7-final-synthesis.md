# Edison Iteration 7: Final Proposal-Ready Synthesis

*Edison Scientific LITERATURE query (task f9d8415e, 2026-04-09). Final synthesis of all 7 iterations into a concise, proposal-ready metrics section with 5 headline KPIs, 6 go/no-go gates, pre-registered benchmark protocol, and 9-month milestone timeline.*

---

Question: 
CONTEXT: FLAIME is a DOE Genesis Mission Phase I proposal ($500K-$750K, 9 months) for autonomous 
closed-loop alloy discovery. After 6 rounds of Edison refinement, the metrics framework is near-final.

SYNTHESIS OF ALL PRIOR FEEDBACK: Key changes accumulated across iterations:

From Iteration 1 (comprehensive brainstorm):
- Condensed proposal-ready KPI table with baseline → Phase I → Phase II targets
- Autonomy level rubric (L0-L5, Hung et al. 2024)
- Acceleration factor ≥2× with pre-registered evaluation
- Digital thread ≥95% completeness, UUID-linked

From Iteration 2 (3-reviewer panel):
- Reviewer 1 (AI): Needs pre-registered benchmark protocol, conformal prediction
- Reviewer 2 (Materials): Add powder chemistry fidelity, lot-to-lot variability
- Reviewer 3 (DOE): Add techno-economic analysis, manufacturing readiness level

From Iteration 3 (go/no-go framework):
- 6 mandatory go gates + scoring rubric (0-100)
- Early warning at months 2, 4, 6
- Transfer-learning evidence required for Phase II justification

From Iteration 4 (stress test):
- Literature defensibility gaps identified
- Statistical rigor concerns on sample sizes
- Need comparison with actual funded program metrics

From Iteration 5 (AI advantage plan):
- 4-baseline design (random, expert DOE, standard BO, BOFN)
- Pre-registration protocol structure
- Time-ledger methodology for decomposing acceleration
- Risk framework for modest advantage scenario

TASK: This is the FINAL SYNTHESIS iteration. Adopt the persona of the proposal PI writing the 
metrics section of the actual Genesis Mission Phase I application.

Produce a CONCISE, PROPOSAL-READY metrics section that:

1. **5 Headline KPIs** in a single table: name, Phase I baseline, Phase I target, Phase II target, 
   measurement method. These must be the metrics that a program manager would remember after reading 
   100 proposals.

2. **Phase I Go/No-Go Decision Matrix**: A single table showing each mandatory criterion, its 
   minimum threshold, measurement method, and what constitutes pass/partial/fail.

3. **AI Advantage Demonstration Protocol**: 2-3 paragraph summary of the pre-registered benchmark 
   plan (baselines, statistical tests, sample sizes, time-ledger).

4. **Monthly Milestone Timeline**: Month-by-month targets for the 9-month Phase I.

5. **Phase II Readiness Indicators**: What Phase I evidence will justify the $6M-$15M Phase II investment.

Keep it to ~2000 words maximum — this needs to fit in a proposal, not be a research paper.
Make every word count. Use the most impactful numbers and framings from all 6 prior iterations.

Ground key claims in literature with inline citations.


## Metrics (Genesis Mission Phase I, 9 months)

Our metrics are designed to be (i) manager-memorable, (ii) auditable from logs, and (iii) benchmarkable against explicit references with replication, because stand-alone “optimization rate” claims are not comparable across studies. Direct algorithm benchmarking with replicates is the most defensible way to assess self-driving laboratory performance (volk2024performancemetricsto pages 1-2). We therefore anchor Phase I success to pre-registered, head-to-head benchmarks using acceleration factor (AF) and enhancement factor (EF), two widely used SDL benchmarking metrics with explicit reference strategies (adesiji2026benchmarkingselfdrivinglabs pages 1-4, adesiji2026benchmarkingselfdrivinglabs media c163d5f0).

### 1) Five Headline KPIs (Baseline → Phase I → Phase II)

| KPI | Phase I baseline (today) | Phase I target (9 months) | Phase II target | Measurement method |
|---|---|---|---|---|
| **2× Discovery Acceleration** | Manual/semi-manual campaign; no pre-registered benchmark; AF not yet established | **Acceleration factor (AF) >= 2.0×** versus best non-AI reference on a pre-registered benchmark; report EF at fixed budget and replicate variance (adesiji2026benchmarkingselfdrivinglabs pages 1-4, volk2024performancemetricsto pages 1-2, adesiji2026benchmarkingselfdrivinglabs media c163d5f0) | **AF >= 5×** versus operational baseline in alloy campaigns | Pre-registered head-to-head benchmark using fixed candidate space and equal experimental budget; AF = experiments required by reference / FLAIME to reach the same target performance; EF reported at matched budget with >= 10 replicate campaigns where feasible (adesiji2026benchmarkingselfdrivinglabs pages 4-7, adesiji2026benchmarkingselfdrivinglabs pages 1-4, adesiji2026benchmarkingselfdrivinglabs media c163d5f0) |
| **Autonomy Level** | **L1-L2**: automated instruments with human-directed planning and intervention between loops | **L4**: closed-loop execution of plan-measure-learn-select with human oversight only for safety/exception handling | **L5**: sustained unattended operation across campaigns with supervisory intervention only | Monthly rubric scoring of degree of autonomy across planning, execution, data capture, and exception recovery; report human interventions per run and unattended runtime fraction, consistent with SDL autonomy as a core performance metric (volk2024performancemetricsto pages 1-2) |
| **Trusted Digital Thread** | Fragmented records; partial provenance; inconsistent sample identifiers | **>= 95% UUID-linked completeness** from powder lot -> process parameters -> characterization -> model decision -> archived result | **>= 99% completeness** across multi-site workflows with automated audit trail | Automated audit of required metadata fields and lineage links for every experiment; completeness = records with all mandatory fields and resolvable UUID provenance / total records |
| **Calibrated Uncertainty** | Model scores available, but no formal coverage guarantee | **90% conformal prediction interval coverage within 85-95% empirical coverage** on held-out/rolling test data; interval efficiency tracked | **90% target coverage within 88-92%** under transfer to new alloy family and process window | Split conformal calibration on surrogate/model outputs; compute empirical marginal coverage and interval width on locked test sets and rolling deployment data; conformal prediction selected because it is model-agnostic and provides finite-sample, distribution-free marginal coverage guarantees (angelopoulos2023conformalpredictiona pages 7-13, jaber2025conformalapproachto pages 1-3) |
| **Manufacturable Alloy Quality** | Powder chemistry and lot effects not yet quantified; no TEA/MRL gate | **Powder chemistry fidelity:** measured composition within **+/- 5% relative** of target for each principal element; **lot-to-lot property variation CV <= 10%** at fixed recipe; preliminary **TEA shows credible path to <= 20% cost premium** vs incumbent and **MRL >= 3** | **+/- 2% relative** chemistry fidelity; **CV <= 5%** across lots; **cost parity or <= 10% premium** with performance gain and **MRL 4-5** | ICP-OES/XRF/LECO chemistry verification versus target composition; replicate builds across >= 3 powder lots with property CV tracked; TEA from material, machine, cycle-time, and yield ledger; MRL scored against DOE manufacturing-readiness rubric adapted for alloy process maturation |


*Table: This table provides five manager-memorable KPIs for FLAIME Phase I, with baselines, 9-month targets, Phase II targets, and measurement methods. It emphasizes benchmarked acceleration, autonomy, data provenance, calibrated uncertainty, and manufacturability evidence.*

### 2) Phase I Go/No-Go Decision Matrix (Mandatory Gates)

These six mandatory criteria define the Phase I end-state required for Phase II consideration.

| Criterion (mandatory) | Minimum threshold (go) | Measurement method | Pass / Partial / Fail definition |
|---|---|---|---|
| AI advantage on discovery speed | **Acceleration factor (AF) >= 2.0x** versus the strongest non-AI reference under a **pre-registered benchmark** with equal experimental budget; enhancement factor (EF) also reported (adesiji2026benchmarkingselfdrivinglabs pages 4-7, adesiji2026benchmarkingselfdrivinglabs pages 1-4, adesiji2026benchmarkingselfdrivinglabs media c163d5f0) | Locked benchmark protocol comparing FLAIME against 4 baselines: random/Sobol, expert DOE, standard BO, and BOFN; AF defined as experiments required by reference divided by experiments required by FLAIME to reach the same objective threshold; replicate campaigns with fixed seed policy and time-ledger | **Pass:** AF >= 2.0x and statistically significant advantage on the primary endpoint. **Partial:** AF 1.5-1.99x or AF >= 2.0x but confidence interval overlaps 1.0. **Fail:** AF < 1.5x or benchmark not pre-registered/executed as planned. |
| Closed-loop autonomy | **Autonomy level >= L4** for the defined campaign: autonomous plan-measure-learn-select loop with human involvement limited to safety or hardware recovery; unattended operation >= 8 h/run (volk2024performancemetricsto pages 1-2) | Monthly autonomy rubric covering experiment selection, instrument orchestration, data ingestion, model update, and exception handling; log all human interventions per loop | **Pass:** L4 demonstrated in end-to-end runs with <= 1 non-safety human intervention per 24 h campaign. **Partial:** L3.5 equivalent with autonomous execution but manual restart/approval between loops. **Fail:** Human-directed experiment selection or repeated manual intervention required. |
| Digital thread completeness | **>= 95%** of experiments fully UUID-linked from powder lot -> processing parameters -> characterization -> model decision -> archive | Automated audit of mandatory metadata fields, provenance links, and machine-readable records at experiment closeout | **Pass:** >= 95% complete and auditable records. **Partial:** 90-94.9% complete or isolated broken links without loss of scientific traceability. **Fail:** < 90% complete or provenance gaps that prevent reconstruction of decisions/results. |
| Calibrated uncertainty for decision-making | **90% nominal conformal coverage** with empirical coverage in the **85-95%** acceptance band on locked test/rolling validation data; interval efficiency tracked (jaber2025conformalapproachto pages 1-3, angelopoulos2023conformalpredictiona pages 7-13) | Split conformal calibration on surrogate predictions; compute empirical marginal coverage and median interval width on held-out and deployment data | **Pass:** Empirical coverage within 85-95% and intervals informative enough to support ranking/selection. **Partial:** Coverage 80-84.9% or 95.1-97% with corrective recalibration plan. **Fail:** Coverage < 80% or > 97% with unusably wide intervals, or no conformal calibration implemented. |
| Materials fidelity and reproducibility | **Powder chemistry fidelity:** each principal element within **+/- 5% relative** of target composition; **lot-to-lot variability:** critical property CV <= 10% across >= 3 powder lots at a fixed recipe | ICP-OES/XRF/LECO composition verification; replicate builds/tests across at least 3 powder lots; coefficient of variation computed on target property set | **Pass:** Both chemistry fidelity and lot-to-lot CV thresholds met. **Partial:** One threshold met and the other missed by <= 20% relative margin with root-cause identified. **Fail:** Chemistry error > +/- 5% relative for any principal element, CV > 12%, or lot effects not quantified. |
| Phase II manufacturability case | **Preliminary TEA shows credible path to <= 20% cost premium** versus incumbent at target performance, and **MRL >= 3** by end of Phase I | Bottom-up techno-economic analysis using measured material, machine-time, labor, yield, and throughput ledger; manufacturing readiness scored against program MRL rubric | **Pass:** Both TEA path and MRL >= 3 achieved. **Partial:** One achieved and the other within one step (e.g., MRL 2 with validated maturation plan, or cost path to <= 30% premium). **Fail:** No credible cost case, no manufacturability evidence, or MRL remains <= 2 without mitigation. |


*Table: This table defines the six mandatory Phase I go gates for FLAIME, with explicit quantitative thresholds, measurement methods, and pass/partial/fail rules. It is designed to support an unambiguous DOE programmatic decision at the end of the 9-month Genesis Phase I effort.*

### 3) AI Advantage Demonstration Protocol (Pre-Registered)

> We will pre-register the Phase I benchmark before the first autonomous campaign. FLAIME will be evaluated head-to-head against four baselines run on the same candidate space, constraints, and experimental budget: (1) random/Sobol sampling, (2) expert-designed DOE, (3) standard Bayesian optimization with a conventional surrogate/acquisition policy, and (4) our strongest non-foundation-model internal baseline, BOFN. The primary endpoint is acceleration factor (AF): the ratio of experiments required by the reference strategy to reach a locked property threshold. The secondary endpoint is enhancement factor (EF): best achieved objective value at a fixed experimental budget. These are the most interpretable and transferable SDL metrics, provided they are benchmarked against explicit references with replicates rather than reported as stand-alone optimization rate claims (adesiji2026benchmarkingselfdrivinglabs pages 4-7, adesiji2026benchmarkingselfdrivinglabs pages 1-4, volk2024performancemetricsto pages 1-2, adesiji2026benchmarkingselfdrivinglabs media c163d5f0).
>
> The benchmark protocol will fix seeds, candidate pools, stopping rules, and exclusion criteria. We will execute at least 10 replicated campaigns per algorithm where feasible in retrospective/surrogate mode, and at least 3 replicated physical campaigns for the top two performers, which is sufficient to estimate effect size and variance for a Genesis Phase I decision. Our confirmatory test is superiority of FLAIME over the strongest non-AI reference on AF, using a one-sided bootstrap confidence interval and permutation-based significance test on replicate-level outcomes; EF at matched budget and area-under-learning-curve are prespecified secondary analyses. A result is counted as Phase I success only if AF >= 2.0x and the confidence interval excludes 1.0; AF of 1.5-1.99x triggers a partial-success/risk-mitigation path rather than a Phase II request (adesiji2026benchmarkingselfdrivinglabs pages 4-7, adesiji2026benchmarkingselfdrivinglabs pages 1-4, volk2024performancemetricsto pages 3-5).
>
> To separate algorithmic gain from automation throughput, every campaign will use a machine-readable time ledger that records queue time, setup, synthesis, characterization, analysis, model-update, and human-intervention minutes per loop. We will report both total wall-clock acceleration and decision-efficiency acceleration (experiments-to-target), so the program can see exactly where advantage arises. For trustworthy closed-loop selection, surrogate predictions will be calibrated with split conformal prediction to target 90% marginal coverage on held-out and rolling validation data; decision policies will use these calibrated intervals rather than raw model scores alone. This combination of pre-registration, strong baselines, replicate statistics, and calibrated uncertainty is designed to make any claimed AI advantage auditable and programmatically defensible (jaber2025conformalapproachto pages 1-3, angelopoulos2023conformalpredictiona pages 7-13).


*Blockquote: This blockquote provides a proposal-ready summary of the pre-registered benchmark plan for demonstrating AI advantage in Phase I. It defines the four baselines, primary and secondary endpoints, statistical tests, replication strategy, time-ledger decomposition, and conformal calibration for trustworthy decision-making.*

### 4) Monthly Milestone Timeline (9 months)

| Month | Technical deliverable | Metric checkpoint (numeric) | Evidence artifact |
|---|---|---:|---|
| 1 | Lock benchmark design, success metrics, and data schema; stand up UUID-based digital thread backbone | Pre-registration draft complete; mandatory metadata schema frozen; digital-thread completeness on test records >= 80% | Registered benchmark protocol, metric dictionary, UUID/provenance schema, baseline candidate set definition (adesiji2026benchmarkingselfdrivinglabs pages 1-4, volk2024performancemetricsto pages 1-2) |
| 2 | **Early-warning review #1**; complete pre-registration and execute dry-run closed loop | Pre-registration filed; one end-to-end dry run completed; autonomy >= L2.5; digital-thread completeness >= 90% | Time-stamped preregistration, dry-run report, intervention log, corrective-action list |
| 3 | Integrate planning-model-execution stack; launch benchmark campaign with 4 baselines | >= 4 benchmark arms active; >= 20 total experiments logged; unattended runtime >= 4 h/run; empirical record completeness >= 92% | Benchmark execution package, baseline configuration files, experiment ledger |
| 4 | **Early-warning review #2**; first interim AI-advantage readout and conformal calibration v1 | Interim AF >= 1.3x; conformal 90% nominal coverage within 80-98%; >= 30 experiments complete | Interim benchmark memo, calibration report, risk-adjustment plan (jaber2025conformalapproachto pages 1-3, angelopoulos2023conformalpredictiona pages 7-13) |
| 5 | Powder chemistry fidelity study and first lot-to-lot reproducibility assessment | Principal-element chemistry error <= +/- 7% relative; >= 2 powder lots tested; critical-property CV <= 15% | ICP-OES/XRF/LECO composition report, lot comparison dataset, root-cause log |
| 6 | **Early-warning review #3**; autonomous closed-loop campaign at target operating mode | Autonomy >= L3.5; unattended runtime >= 8 h/run; digital-thread completeness >= 95%; interim AF >= 1.7x | Mid-phase go-gate package, autonomy scorecard, provenance audit, updated benchmark statistics (adesiji2026benchmarkingselfdrivinglabs pages 4-7, volk2024performancemetricsto pages 1-2) |
| 7 | Final benchmark campaign and uncertainty-controlled decision policy | >= 40 benchmark experiments complete; conformal 90% nominal coverage within 85-95%; median interval width reduced >= 10% from Month 4 | Locked benchmark dataset, final calibration set, uncertainty-performance dashboard (jaber2025conformalapproachto pages 1-3, angelopoulos2023conformalpredictiona pages 7-13) |
| 8 | Preliminary TEA and manufacturing-readiness assessment; transfer test on held-out alloy/process region | TEA shows path to <= 25% cost premium; MRL >= 2.5; transfer campaign performance retains >= 80% of in-domain gain | Bottom-up cost model, MRL rubric assessment, transfer-learning memo |
| 9 | End-of-Phase-I integrated demonstration and Phase II decision package | Final AF >= 2.0x; autonomy >= L4; digital-thread completeness >= 95%; chemistry fidelity <= +/- 5% relative; >= 3 powder lots with CV <= 10%; TEA path to <= 20% premium; MRL >= 3 | Final go/no-go dossier, reproducibility package, benchmark statistics with time-ledger decomposition, Phase II maturation plan (adesiji2026benchmarkingselfdrivinglabs pages 4-7, adesiji2026benchmarkingselfdrivinglabs pages 1-4, volk2024performancemetricsto pages 1-2, jaber2025conformalapproachto pages 1-3, angelopoulos2023conformalpredictiona pages 7-13) |


*Table: This table provides a concise 9-month execution plan for FLAIME Phase I, with numeric checkpoints tied directly to autonomy, benchmarking, uncertainty calibration, materials fidelity, and manufacturability evidence needed for a Phase II decision.*

### 5) Phase II Readiness Indicators (Justification for $6M–$15M)

Phase II is warranted only if Phase I produces **transferable, reproducible, and manufacturable** evidence beyond a one-off closed-loop “demo.” Specifically, we will use the following Phase I evidence package to justify the Phase II investment:

1. **Reproducible AI advantage over strong baselines.** A completed, pre-registered benchmark dataset with replication demonstrating AF ≥ 2× versus the strongest non-AI reference, with AF/EF reported against explicit reference strategies as recommended in SDL benchmarking practice (adesiji2026benchmarkingselfdrivinglabs pages 1-4, adesiji2026benchmarkingselfdrivinglabs media c163d5f0). The package will include replicate-level statistics, confidence intervals, and the full experiment ledger enabling independent re-analysis.

2. **At-scale autonomy and operations evidence.** Demonstrated L4 closed-loop operation with quantified intervention frequency and unattended runtime, consistent with autonomy as a core SDL performance metric (volk2024performancemetricsto pages 1-2). Phase II will extend this to multi-week sustained operations and multi-objective campaigns.

3. **Trustworthy decision-making via calibrated uncertainty.** Evidence that uncertainty is not only produced but **calibrated**. We will provide empirical coverage and efficiency metrics for split conformal prediction intervals, leveraging conformal prediction’s model-agnostic, finite-sample marginal coverage guarantees (angelopoulos2023conformalpredictiona pages 7-13) and its suitability for surrogate UQ without relying on potentially misspecified Bayesian credibility assumptions (jaber2025conformalapproachto pages 1-3). Phase II readiness requires stable coverage under distribution shift (new alloy family/process window).

4. **Materials fidelity and reproducibility across powder lots.** Chemistry verification results, lot-to-lot variability statistics (CV), and root-cause analyses demonstrating that closed-loop recommendations are not artifacts of uncontrolled feedstock variability. This is essential to translate autonomous discovery into manufacturable recipes.

5. **Manufacturability and scale pathway (TEA + MRL).** A bottom-up techno-economic model backed by the Phase I time ledger (machine time, yield, consumables, labor) and a documented maturation plan from MRL ≥ 3 to MRL 4–5, including risk burndown for throughput, yield, and quality control.

Collectively, these indicators ensure Phase II is a scale-up of a validated capability (benchmarkable acceleration + autonomy + uncertainty-calibrated decision-making + reproducibility + manufacturability), not merely a continuation of platform development (volk2024performancemetricsto pages 1-2, adesiji2026benchmarkingselfdrivinglabs pages 1-4).

References

1. (volk2024performancemetricsto pages 1-2): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.

2. (adesiji2026benchmarkingselfdrivinglabs pages 1-4): Adedire D. Adesiji, Jiashuo Wang, Cheng-Shu Kuo, and Keith A. Brown. Benchmarking self-driving labs. Digital Discovery, 5:14-27, Jan 2026. URL: https://doi.org/10.1039/d5dd00337g, doi:10.1039/d5dd00337g. This article has 5 citations and is from a peer-reviewed journal.

3. (adesiji2026benchmarkingselfdrivinglabs media c163d5f0): Adedire D. Adesiji, Jiashuo Wang, Cheng-Shu Kuo, and Keith A. Brown. Benchmarking self-driving labs. Digital Discovery, 5:14-27, Jan 2026. URL: https://doi.org/10.1039/d5dd00337g, doi:10.1039/d5dd00337g. This article has 5 citations and is from a peer-reviewed journal.

4. (adesiji2026benchmarkingselfdrivinglabs pages 4-7): Adedire D. Adesiji, Jiashuo Wang, Cheng-Shu Kuo, and Keith A. Brown. Benchmarking self-driving labs. Digital Discovery, 5:14-27, Jan 2026. URL: https://doi.org/10.1039/d5dd00337g, doi:10.1039/d5dd00337g. This article has 5 citations and is from a peer-reviewed journal.

5. (angelopoulos2023conformalpredictiona pages 7-13): Anastasios Nikolas Angelopoulos and Stephen Bates. Conformal prediction: a gentle introduction. Found. Trends Mach. Learn., 16:494-591, Jan 2023. URL: https://doi.org/10.1561/2200000101, doi:10.1561/2200000101. This article has 2025 citations.

6. (jaber2025conformalapproachto pages 1-3): Edgar Jaber, Vincent Blot, Nicolas J. B. Brunel, Vincent Chabridon, Emmanuel Remy, Bertrand Iooss, Didier Lucor, Mathilde Mougeot, and Alessandro Leite. Conformal approach to gaussian process surrogate evaluationwith marginal coverage guarantees. Journal of Machine Learning for Modeling and Computing, 6:37-68, Jan 2025. URL: https://doi.org/10.1615/jmachlearnmodelcomput.2025054687, doi:10.1615/jmachlearnmodelcomput.2025054687. This article has 15 citations.

7. (volk2024performancemetricsto pages 3-5): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.