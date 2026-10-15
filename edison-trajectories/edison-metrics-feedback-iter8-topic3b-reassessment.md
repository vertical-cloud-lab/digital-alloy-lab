# Edison Iteration 8: Topic 3B Metrics Reassessment

*Edison Scientific LITERATURE_HIGH query (task 9763811e, 2026-04-11). Comprehensive reassessment of all FLAIME metrics for Topic 3B "AI-Enabled Materials Discovery — Reducing Demand for Critical Minerals" (AMMTO). Includes revised headline KPIs, go/no-go gates, material performance targets, Phase II readiness indicators, benchmarking update, and new Critical Mineral Impact metric category.*

---

Question: CONTEXT: FLAIME is a DOE Genesis Mission Phase I proposal ($500-750K, 9 months) for an autonomous closed-loop alloy discovery platform (CALPHAD → ultrasonic atomization → LPBF → ASTM E8 tensile testing → BOFN optimization). The proposal has switched from Topic 12F to Topic 3B: "AI-Enabled Materials Discovery and Engineering — Reducing Demand for Critical Minerals" (AMMTO).

KEY 3B REQUIREMENTS:
- Deploy automated discovery platforms to accelerate material discovery, manufacturing, and qualification through closed-loop systems that integrate hypothesis, experiment, validation, and manufacturing, REDUCING DEMAND for critical minerals
- Material strategy: Al-Zr and Al-Mn-Cr-Zr families PRIMARY (~80% Phase I effort, avoiding Mg/Sc/REE critical minerals), Cu-Cr-Zr COMPLEMENT (~20% stretch, replacing Be-Cu)
- AlSi10Mg is baseline for benchmarking only
- BOFN with mineral-burden objective (scalarization or MOBO extension, per Mulukutla et al. 2024)
- Phase II: Cu-Cr-Zr full optimization + expanded Al alloy families

EXISTING METRICS (from 7 Edison iterations for Topic 12F):
- 5 Headline KPIs: Discovery Yield, AI Acceleration Factor, Throughput, Autonomy Level, Digital Thread Completeness
- 8 go/no-go gates (closed-loop autonomy, printable process window, mechanical properties, predictive capability, optimization advantage, workflow improvement, scaling evidence, generalization)
- Pre-registered benchmark: 4 baselines (random, expert DOE, standard BO, BOFN), ≥20 seeds, bootstrap CI
- Material targets: YS≥250 MPa AND EL≥5% (currently framed for generic Al alloys)
- Phase II narrative: temperature upgrade to 1500°C for 316H/IN718 (NOT relevant to 3B)

TASK: Reassess ALL metrics for Topic 3B. Provide:

1. **REVISED HEADLINE KPIs** (5-6 total): Which existing KPIs survive? What new critical-mineral-specific KPIs are needed? For each KPI provide: name, definition, Phase I baseline, Phase I target (9 mo), Phase II target, measurement method. Consider:
   - Critical Mineral Demand Reduction as a quantifiable KPI (kg displaced, compositions discovered that avoid Mg/Sc/REE, supply risk index)
   - Whether Discovery Yield definition should change (threshold adjusted for Al-Zr family properties?)
   - Whether BOFN mineral-burden objective demonstration belongs as a headline KPI

2. **REVISED GO/NO-GO GATES** (6-8 gates): Adapt for 3B. Consider adding:
   - Critical mineral displacement demonstration gate (must show at least one alloy meeting performance threshold WITHOUT Mg/Sc/REE/Be)
   - Mineral-burden objective gate (BOFN must demonstrate optimization toward lower critical mineral content)
   - Keep/adjust: closed-loop autonomy, process window, mechanical properties, AI advantage, digital thread

3. **REVISED MATERIAL PERFORMANCE TARGETS**: Al-Zr and Al-Mn-Cr-Zr property targets (not Al-Ce-X). What are realistic Phase I targets for:
   - Al-Zr binary/ternary YS, UTS, elongation (literature baselines?)
   - Al-Mn-Cr-Zr YS, UTS, elongation (literature baselines?)
   - Cu-Cr-Zr stretch targets (conductivity + strength for Be-Cu replacement)

4. **REVISED PHASE II READINESS INDICATORS**: What Phase I evidence justifies Phase II for 3B? (Not temperature upgrade — instead: expanded critical mineral displacement, Cu-Cr-Zr full optimization, multi-alloy-family mineral-lean discovery)

5. **BENCHMARKING UPDATE**: Compare FLAIME against programs relevant to 3B (CMI Hub Al-Ce, ULTIMATE/BIRDSHOT for MOBO, Mulukutla supply-risk-aware alloy BO). Update state-of-art table.

6. **NEW METRIC CATEGORY**: "Critical Mineral Impact" metrics — quantified displacement potential, supply risk reduction, mineral-lean compositions discovered, comparison to incumbent alloys

Cite all sources with full author/year/journal format (no placeholder keys with '...').

# FLAIME Metrics Reassessment for DOE Genesis Topic 3B: AI-Enabled Materials Discovery — Reducing Demand for Critical Minerals

## 1. Revised Headline KPIs

The transition from Topic 12F to Topic 3B necessitates reframing FLAIME's headline KPIs to foreground critical-mineral demand reduction alongside the existing autonomous-discovery metrics. Of the original five KPIs, three survive with modification (Discovery Yield, AI Acceleration Factor, Throughput), one survives as-is (Digital Thread Completeness), one is retired (Autonomy Level, folded into go/no-go gates), and two new KPIs are introduced (Critical Mineral Demand Reduction Index, Mineral-Burden Optimization Efficacy).

**Discovery Yield** is redefined as "Mineral-Lean Discovery Yield"—the fraction of BOFN-proposed alloys that simultaneously meet the performance threshold (YS ≥ 250 MPa AND EL ≥ 5%) and the critical-mineral avoidance constraint (0 wt% Mg/Sc/REE/Be). The original Topic 12F definition applied to generic Al alloys; the revised definition enforces a compositional constraint that is central to Topic 3B. The Phase I target of ≥30% is calibrated against literature showing that Al-Zr-based LPBF alloys can achieve YS of 279–395 MPa with ductility ranging from 0.9% to 16% depending on composition and heat treatment, indicating that discovering compositions meeting both criteria is feasible but non-trivial (ge2025highstrengthadditivelymanufacturable pages 1-2).

**Critical Mineral Demand Reduction Index (CMDRI)** is a new headline KPI that quantifies the supply-risk improvement of FLAIME-discovered alloys versus incumbents. It is computed as the percentage reduction in the Helbig-style 12-indicator supply risk index (SRmean), following the methodology of Mulukutla et al. (2024), who demonstrated that integrating a supply-risk objective into multi-objective batch Bayesian optimization steered the search toward lower-risk compositions without degrading performance (mulukutla2024supplyriskawarealloy pages 2-5, mulukutla2024supplyriskawarealloy pages 16-18, mulukutla2024supplyriskawarealloy pages 12-16).

**Mineral-Burden Optimization Efficacy** is a new KPI that measures whether BOFN with a mineral-burden objective produces demonstrably better Pareto frontiers than performance-only BO, quantified via hypervolume ratio. Mulukutla et al. showed that including supply risk as a MOBBO objective achieved faster convergence (6 vs. 7 iterations) and shifted Pareto-optimal compositions toward lower-risk regions (mulukutla2024supplyriskawarealloy pages 12-16, mulukutla2024supplyriskawarealloy pages 10-12).

The complete revised KPI framework is presented below:

| KPI Name | Definition | Phase I Baseline | Phase I Target (9 mo) | Phase II Target | Measurement Method |
|---|---|---|---|---|---|
| Discovery Yield (Mineral-Lean) | Fraction of BOFN-proposed alloys meeting both the performance threshold (YS ≥ 250 MPa and EL ≥ 5%) and the critical-mineral avoidance constraint (0 wt% Mg/Sc/REE/Be) | 0 (no iterations) | ≥30% of tested compositions | ≥50% | ASTM E8 tensile testing + ICP-OES composition verification (ge2025highstrengthadditivelymanufacturable pages 1-2, arena2024novelaluminumalloy pages 4-6) |
| Critical Mineral Demand Reduction Index (CMDRI) | Composite supply-risk score reduction versus incumbent alloy (AlSi10Mg or Be-Cu), computed as weighted-mean Helbig supply-risk index (SRmean) | SRmean of incumbent (AlSi10Mg) | ≥25% SRmean reduction in best-performing alloy vs. incumbent | ≥40% reduction across 3+ alloy families | Helbig 12-indicator supply-risk index calculation, normalized 0-100 (mulukutla2024supplyriskawarealloy pages 2-5, mulukutla2024supplyriskawarealloy pages 16-18) |
| AI Acceleration Factor | Iterations to reach performance threshold versus baselines (random, expert DOE, standard BO) | Random search iterations | ≥3× fewer iterations than random, ≥1.5× vs. standard BO | ≥5× vs. random | Pre-registered benchmark with ≥20 seeds, bootstrap CI (hastings2024aninteroperablemulti pages 1-2, hastings2024aninteroperablemulti pages 13-15) |
| Closed-Loop Throughput | Alloy compositions tested per month through the full CALPHAD → atomization → LPBF → tensile pipeline | 0 (manual workflow) | ≥8 compositions/month | ≥20 compositions/month | Timestamped digital-thread records (mulukutla2024illustratinganeffective pages 20-23, mulukutla2024illustratinganeffective pages 5-7) |
| Mineral-Burden Optimization Efficacy | Demonstrated Pareto improvement when a mineral-burden objective is added to BOFN versus performance-only BO, measured as hypervolume ratio | Standard BO (performance-only) | Hypervolume ratio ≥1.15 for BOFN+mineral vs. BOFN-only | Multi-objective Pareto with ≥3 performance + mineral-burden objectives | Pareto hypervolume indicator comparison, ≥20 seeds (mulukutla2024supplyriskawarealloy pages 10-12, mulukutla2024supplyriskawarealloy pages 12-16) |
| Digital Thread Completeness | Percentage of alloy iterations with full provenance from CALPHAD prediction through tensile result in machine-readable format | 0% | ≥90% | 100% with FAIR compliance | Automated schema-validation audit (mulukutla2024illustratinganeffective pages 20-23) |


*Table: This table defines the six revised headline KPIs for FLAIME under DOE Topic 3B, emphasizing mineral-lean discovery, supply-risk reduction, closed-loop autonomy, and benchmarked AI advantage. It is useful as a proposal-ready metrics artifact aligned to critical-mineral-demand reduction objectives.*

## 2. Revised Go/No-Go Gates

The gate structure is revised from 8 to 7 gates, with two critical-mineral-specific gates added (Gates 2 and 4) and the Phase II temperature-upgrade gate eliminated entirely. The remaining gates (closed-loop autonomy, process window, mechanical properties, AI advantage, digital thread) are adapted to reflect mineral-lean alloy families rather than generic Al alloys.

**Gate 2 (Critical Mineral Displacement)** is the most consequential addition: it requires demonstrating at least one mineral-lean alloy meeting the performance threshold by Month 6, directly addressing Topic 3B's mandate to reduce demand for critical minerals. This gate draws on literature evidence that Al-Mn-Cr-Zr alloys (containing no Mg/Sc/REE) achieve YS of 250 MPa as-printed and ~350 MPa after aging at 375°C (arena2024novelaluminumalloy pages 4-6), and that Al-Zr family alloys can reach YS of 279 MPa as-built with elongation up to 16% (ge2025highstrengthadditivelymanufacturable pages 1-2).

**Gate 4 (Mineral-Burden BOFN Demonstration)** requires demonstrating Pareto improvement when the mineral-burden objective is activated, validated by hypervolume comparison with ≥20 random seeds. This gate is inspired by the BIRDSHOT program's approach of using expected hypervolume improvement (EHVI) as the acquisition function for multi-objective alloy discovery (hastings2024aninteroperablemulti pages 1-2, hastings2024aninteroperablemulti pages 13-15).

**Gate 5 (Mechanical Property Threshold)** is now alloy-family-specific rather than generic: Al-Zr family targets YS ≥ 200 MPa / EL ≥ 5%, while Al-Mn-Cr-Zr targets YS ≥ 250 MPa / EL ≥ 4%. These are set below the literature peak values to account for the constraint that FLAIME will explore novel compositions autonomously rather than reproducing known optima. The as-printed Al-Mn-Cr-Zr hardness of ~103 HV corresponds to the lower end of the achievable strength range, while peak-aged hardness of 130–144 HV supports the higher aged YS targets (mehta2021highperformancealuminium pages 33-36, arena2024novelaluminumalloy pages 4-6).

| Gate # | Gate Name | Criterion | Evidence Required | Timing |
|---|---|---|---|---|
| 1 | Closed-Loop Autonomy | Platform completes ≥3 autonomous CALPHAD→atomization→LPBF→tensile→BOFN cycles without manual intervention (mulukutla2024illustratinganeffective pages 20-23, mulukutla2024illustratinganeffective pages 5-7) | Timestamped logs showing end-to-end autonomous execution | Month 4 |
| 2 | Critical Mineral Displacement | At least 1 Al-Zr or Al-Mn-Cr-Zr alloy meets YS≥250 MPa AND EL≥5% with 0 wt% Mg/Sc/REE/Be verified by ICP-OES (ge2025highstrengthadditivelymanufacturable pages 1-2, arena2024novelaluminumalloy pages 4-6) | Tensile test certificate + composition analysis report | Month 6 |
| 3 | Printable Process Window | Achieve ≥99.0% relative density for at least 2 distinct mineral-lean compositions via LPBF (ge2025highstrengthadditivelymanufacturable pages 7-8, arena2024novelaluminumalloy pages 4-6) | Archimedes density or CT scan data for ≥2 compositions | Month 5 |
| 4 | Mineral-Burden BOFN Demonstration | BOFN with supply-risk objective demonstrates Pareto improvement over performance-only BO, with hypervolume ratio ≥1.10 (mulukutla2024supplyriskawarealloy pages 10-12, mulukutla2024supplyriskawarealloy pages 12-16) | Benchmark comparison plot with ≥20 random seeds and bootstrap CI | Month 7 |
| 5 | Mechanical Property Threshold | At least 2 mineral-lean compositions meet alloy-family-specific targets: Al-Zr family YS≥200 MPa/EL≥5%; Al-Mn-Cr-Zr family YS≥250 MPa/EL≥4% (ge2025highstrengthadditivelymanufacturable pages 1-2, arena2024novelaluminumalloy pages 4-6) | ASTM E8 tensile data with ≥3 replicates per composition | Month 7 |
| 6 | AI Optimization Advantage | BOFN reaches performance threshold in ≥2× fewer iterations than random baseline and ≥1.3× fewer than standard BO (hastings2024aninteroperablemulti pages 1-2, hastings2024aninteroperablemulti pages 13-15) | Pre-registered benchmark statistical analysis | Month 8 |
| 7 | Digital Thread & Scaling Evidence | ≥85% digital thread completeness demonstrated; documented pathway showing Phase II scale-up to Cu-Cr-Zr and expanded Al families (arroyave2024ultimatebirdshot.final pages 16-19, mulukutla2024illustratinganeffective pages 20-23) | Schema validation report + Phase II scaling plan document | Month 9 |


*Table: This table defines seven revised Phase I go/no-go gates for FLAIME under DOE Topic 3B. It ties each gate to a measurable criterion, required evidence package, and milestone timing aligned with autonomous discovery and critical-mineral-demand reduction.*

## 3. Revised Material Performance Targets

### Al-Zr Family (Primary, ~40% of Phase I effort)

The Al-Zr system is attractive for mineral-lean LPBF because Al₃Zr L1₂ nanoprecipitates provide potent precipitation strengthening without requiring Sc or REE. Ge et al. (2025) reported that an ICME-optimized Al-Zr-Er-Ni composition achieved YS of 279 MPa as-built with 16% elongation (a 1600% ductility increase over the benchmark), while peak-aged conditions (400°C/8h) reached YS of 395 MPa with 4.0% elongation (ge2025highstrengthadditivelymanufacturable pages 1-2). The high as-built ductility was attributed to controlling the Al₃Zr phase fraction via the guideline Zr = 1.07 × Er (ge2025highstrengthadditivelymanufacturable pages 1-2). For FLAIME Phase I, we target the as-built regime (YS ≥ 200 MPa, EL ≥ 5%) as readily achievable, with aged targets (YS ≥ 280 MPa) representing BOFN-guided optimization. Note that FLAIME's Al-Zr compositions will avoid Er (also an REE), focusing on binary Al-Zr and ternary Al-Zr-X where X is a non-critical element (e.g., Fe, Si, Ti).

### Al-Mn-Cr-Zr Family (Primary, ~40% of Phase I effort)

This family is uniquely suited to Topic 3B because all constituent elements (Al, Mn, Cr, Zr) are non-critical. Mehta et al. (2022) demonstrated crack-free LPBF processing of Al-5Mn-0.8Cr-0.6Zr with relative density ~99.5% and as-printed hardness of 98.9–103.4 HV, which increased to 130–144 HV after direct aging at 678 K (mehta2021highperformancealuminium pages 33-36). Arena et al. (2024) reported that the Al-HS1 variant (Al-5Mn-0.8Cr-0.6Zr-0.17Fe-0.24Si) achieved YS of 250 MPa as-printed and ~350 MPa after aging at 375°C, with static properties described as "superior" to AlSi10Mg in the plasticization regime (arena2024novelaluminumalloy pages 4-6). Martucci et al. (2022) confirmed microstructural stability across a range of laser powers (100–170 W), finding consistently ~104 HV hardness and low precipitation levels (<0.3 vol%) in the as-built condition, indicating a supersaturated state amenable to controlled aging (martucci2022theinfluenceof pages 2-4). The Phase I YS target of ≥250 MPa (aged) is therefore well-supported by literature, while the EL target of ≥4% is set conservatively given limited published tensile ductility data for this system.

### Cu-Cr-Zr (Stretch, ~20% of Phase I effort)

Cu-Cr-Zr is positioned as a Be-Cu replacement pathway. Biffi et al. (2024) reported LPBF Cu-Cr-Zr (99.3% density) with as-built YS of 167 MPa, UTS of 230 MPa, and EL of 31%; after solution annealing + aging, UTS increased to 265 MPa with 22% elongation (biffi2024cucrzralloymanufactured pages 4-8). Fiedler et al. (2024) achieved peak hardness of 180 HV after aging laser-remelted CuCr1Zr at 400°C (fiedler2024highconductivecopper pages 4-6). Phase I stretch targets (YS ≥ 200 MPa, conductivity ≥ 50% IACS) represent feasibility demonstration, with Phase II targeting the full Be-Cu replacement envelope (YS ≥ 400 MPa, conductivity ≥ 75% IACS).

| Alloy Family | Property | Literature Baseline (Source) | Phase I Target (9 mo) | Phase II Target |
|---|---|---|---|---|
| Al-Zr family | Yield strength (YS) | 279 MPa as-built; 395 MPa peak-aged in LPBF Al-Zr-Er-Ni (ge2025highstrengthadditivelymanufacturable pages 1-2) | ≥200 MPa as-built; ≥280 MPa aged | ≥350 MPa aged |
| Al-Zr family | Ultimate tensile strength (UTS) | ~400 MPa indicated by Ge et al. fracture-modeling/strength context for LPBF Al-Zr-Er-Ni (ge2025highstrengthadditivelymanufacturable pages 7-8, ge2025highstrengthadditivelymanufacturable pages 1-2) | ≥250 MPa as-built; ≥320 MPa aged | ≥400 MPa |
| Al-Zr family | Elongation (EL) | 0.9–16% depending on composition/condition in LPBF Al-Zr-Er-Ni (ge2025highstrengthadditivelymanufacturable pages 1-2) | ≥5% | ≥8% |
| Al-Zr family | Relative density | >99.5% and up to >99.95% reported for optimized LPBF Al-Zr-Er-Ni processing (ge2025highstrengthadditivelymanufacturable pages 7-8) | ≥99.0% | ≥99.5% |
| Al-Mn-Cr-Zr family | Yield strength (YS) | 250 MPa as-printed and ~350 MPa after aging for Al-HS1/Al-Mn-Cr-Zr (arena2024novelaluminumalloy pages 4-6) | ≥250 MPa aged | ≥350 MPa |
| Al-Mn-Cr-Zr family | Ultimate tensile strength (UTS) | Reported as comparable to AlSi10Mg; proposal-relevant working baseline ~350–400 MPa (arena2024novelaluminumalloy pages 4-6) | ≥300 MPa | ≥400 MPa |
| Al-Mn-Cr-Zr family | Elongation (EL) | Limited direct tensile data; working estimate ≥3–5% based on available hardness/strength outcomes and qualification framing (mehta2021highperformancealuminium pages 33-36, arena2024novelaluminumalloy pages 4-6) | ≥4% | ≥6% |
| Al-Mn-Cr-Zr family | Hardness | ~103–104 HV as-built; peak-aged ~130–144 HV (mehta2021highperformancealuminium pages 33-36) | ≥110 HV as-built; ≥130 HV aged | ≥140 HV |
| Cu-Cr-Zr (stretch, 20% effort) | Yield strength (YS) | 141–167 MPa for LPBF Cu-Cr-Zr depending on condition (biffi2024cucrzralloymanufactured pages 4-8) | ≥200 MPa aged | ≥400 MPa |
| Cu-Cr-Zr (stretch, 20% effort) | Ultimate tensile strength (UTS) | 230–265 MPa for LPBF Cu-Cr-Zr depending on condition (biffi2024cucrzralloymanufactured pages 4-8) | ≥300 MPa | ≥500 MPa |
| Cu-Cr-Zr (stretch, 20% effort) | Elongation (EL) | 22–31% for LPBF Cu-Cr-Zr depending on condition (biffi2024cucrzralloymanufactured pages 4-8) | ≥15% | ≥10% |
| Cu-Cr-Zr (stretch, 20% effort) | Electrical conductivity | Wrought Cu-Cr-Zr commonly ~80% IACS; LPBF thermal-conductivity improvement shown after heat treatment, but %IACS not reported in retrieved LPBF excerpts (biffi2024cucrzralloymanufactured pages 4-8) | ≥50% IACS | ≥75% IACS |
| AlSi10Mg (benchmark only) | Yield strength (YS) | ~250–300 MPa (T6 / benchmark framing) (arena2024novelaluminumalloy pages 4-6) | Benchmark only | Benchmark only |
| AlSi10Mg (benchmark only) | Ultimate tensile strength (UTS) | ~350–400 MPa (T6 / benchmark framing) (arena2024novelaluminumalloy pages 4-6) | Benchmark only | Benchmark only |
| AlSi10Mg (benchmark only) | Elongation (EL) | ~5–10% benchmark range (arena2024novelaluminumalloy pages 4-6) | Benchmark only | Benchmark only |


*Table: This table summarizes proposal-ready Phase I and Phase II material performance targets for the primary Al-Zr and Al-Mn-Cr-Zr families, the Cu-Cr-Zr stretch goal, and the AlSi10Mg benchmark. It ties each target to the literature baselines available in the retrieved evidence.*

## 4. Revised Phase II Readiness Indicators

The original Phase II narrative—a temperature upgrade to 1500°C for 316H/IN718—is entirely replaced for Topic 3B. The revised Phase II readiness indicators are:

**4.1. Expanded Critical Mineral Displacement.** Phase I must demonstrate ≥3 mineral-lean compositions meeting performance thresholds across at least 2 alloy families (Al-Zr and Al-Mn-Cr-Zr). Phase II readiness requires evidence that the BOFN optimization engine can generalize across families, supported by the digital thread showing convergence trajectories for each family.

**4.2. Cu-Cr-Zr Full Optimization Pathway.** Phase I must deliver printability demonstration (≥99.0% density) and initial BOFN-guided property data for Cu-Cr-Zr. Phase II readiness requires a documented CALPHAD model for the Cu-Cr-Zr phase space and a BOFN configuration incorporating conductivity as an additional objective, following the BIRDSHOT paradigm of adding objectives iteratively (arroyave2024ultimatebirdshot.final pages 16-19, hastings2024aninteroperablemulti pages 2-3).

**4.3. Multi-Alloy-Family Mineral-Lean Discovery.** The Phase I digital thread must demonstrate that the FLAIME platform is alloy-system-agnostic—i.e., the CALPHAD → atomization → LPBF → tensile → BOFN pipeline can switch between Al-Zr, Al-Mn-Cr-Zr, and Cu-Cr-Zr without architectural changes. This is validated by successful execution of at least one closed-loop cycle in each family.

**4.4. Supply-Risk Pareto Portfolio.** Phase I BOFN runs must produce a Pareto frontier in (performance, supply-risk) space, demonstrating that the mineral-burden objective is technically functional and that trade-offs are quantifiable. Phase II will extend this to ≥3 performance objectives + 1 supply-risk objective in a full MOBO configuration, analogous to the four-scenario comparison in Mulukutla et al. (mulukutla2024supplyriskawarealloy pages 8-10, mulukutla2024supplyriskawarealloy pages 12-16).

**4.5. Scaling Evidence.** Phase I must document atomization batch sizes, LPBF build rates, and tensile testing throughput sufficient to project Phase II scale-up to ≥20 compositions/month. Workflow bottlenecks must be identified and mitigation plans documented.

## 5. Benchmarking Update

FLAIME's positioning within the Topic 3B landscape is clarified by comparison against five relevant programs. The BIRDSHOT/ULTIMATE program at Texas A&M represents the current state-of-the-art in closed-loop multi-objective Bayesian alloy optimization, having demonstrated 3-objective Pareto optimization on FCC HEAs with only 0.15% design-space sampling across 5 iterations, and a 54% Pareto hypervolume increase in a two-shot refractory alloy campaign (hastings2024aninteroperablemulti pages 1-2, paramore2025twoshotoptimizationof pages 16-18, paramore2025twoshotoptimizationof pages 1-3). However, BIRDSHOT does not incorporate an explicit supply-risk objective and operates on HEA systems via vacuum arc melting rather than LPBF.

Mulukutla et al. (2024) provided the first demonstration of supply-risk-aware alloy BO, using a 12-indicator Helbig-style index as an explicit MOBBO objective on the MoNbTiVW system (mulukutla2024supplyriskawarealloy pages 2-5, mulukutla2024supplyriskawarealloy pages 1-2). Their key finding—that including supply risk steered the search to lower-risk regions without performance degradation—directly motivates FLAIME's mineral-burden BOFN extension. However, their work was computational only; FLAIME will close the loop experimentally.

The CMI Hub Al-Ce program developed high-performance aluminum-cerium alloys achieving UTS of ~400 MPa in cast/extruded forms and 459 MPa UTS / 274 MPa YS / 4.4% EL via SLM for Al-7Cu-3Ce (czerwinski2020ceriuminaluminum pages 26-28, sims2017highperformancealuminum–cerium pages 1-3). While this addresses critical-mineral supply chains by consuming Ce (an REE coproduct), it does not reduce REE demand per se—FLAIME avoids REEs entirely.

| Program/Approach | Institution | Alloy System | Closed-Loop? | Supply Risk Integration? | Key Results | FLAIME Differentiator |
|---|---|---|---|---|---|---|
| BIRDSHOT/ULTIMATE | Texas A&M / Arróyave group | CoCrFeNiVAl FCC HEA; MoNbTiVW refractory HEA | Yes — multi-iteration closed-loop, including 5 optimization iterations | No explicit mineral-burden objective | 3-objective Pareto optimization; sampled only 0.15% of design space in FCC campaign; two-shot refractory campaign delivered 54% Pareto hypervolume increase (hastings2024aninteroperablemulti pages 1-2, arroyave2024ultimatebirdshot.final pages 16-19, paramore2025twoshotoptimizationof pages 16-18, paramore2025twoshotoptimizationof pages 1-3, hastings2024aninteroperablemulti pages 13-15) | FLAIME adds explicit mineral-burden objective, LPBF manufacturing, and mineral-lean Al-alloy focus |
| Mulukutla et al. 2024 Supply-Risk-Aware BO | Texas A&M / Arróyave group | MoNbTiVW refractory HEA | Computational only | Yes — 12-indicator Helbig-style supply-risk index used as MOBBO objective | Supply-risk objective steered search toward lower-risk compositions without performance degradation and with faster convergence in some cases (mulukutla2024supplyriskawarealloy pages 10-12, mulukutla2024supplyriskawarealloy pages 8-10, mulukutla2024supplyriskawarealloy pages 2-5, mulukutla2024supplyriskawarealloy pages 16-18, mulukutla2024supplyriskawarealloy pages 12-16) | FLAIME closes the loop experimentally, validates supply-risk-aware optimization on hardware, and targets Al/Cu LPBF alloys |
| CMI Hub Al-Ce Alloys | Ames Laboratory / ORNL / CMI | Al-Ce binary/ternary; Al-7Cu-3Ce AM variant | No — conventional alloy development, casting, extrusion, and separate AM studies | Indirect — increases demand for Ce as a rare-earth coproduct rather than reducing REE dependence | Al-Ce family reached ~400 MPa UTS in cast/extruded forms; Al-7Cu-3Ce SLM reached 459 MPa UTS, 274 MPa YS, 4.4% elongation; good thermal stability to ~300°C (czerwinski2020ceriuminaluminum pages 26-28, sims2017highperformancealuminum–cerium pages 1-3, sims2016ceriumbasedintermetallicstrengthenedaluminum pages 10-12) | FLAIME avoids REEs entirely, uses autonomous closed-loop discovery, and optimizes explicitly for mineral burden |
| Burns et al. 2024 MOBO | Idaho National Laboratory | Ni/Co-free replacement alloys | Partial — computational plus experimental replacement-material workflow | Indirect — targets substitution away from Ni/Co critical minerals | Demonstrated MOBO for replacement-material development without Ni and Co, showing promise for critical-mineral-free alloy design (mulukutla2024supplyriskawarealloy pages 16-18) | FLAIME proposes a full physical CALPHAD→atomization→LPBF→tensile→BOFN loop with explicit supply-risk scalarization and Al/Cu focus |
| AlSi10Mg LPBF (Commercial Baseline) | Various commercial / academic users | AlSi10Mg | No | No | Benchmark LPBF alloy with typical YS ~250–300 MPa, UTS ~350–400 MPa, elongation ~5–10% in common heat-treated benchmarks (arena2024novelaluminumalloy pages 4-6) | FLAIME uses AlSi10Mg only as benchmark and shifts discovery toward mineral-lean, autonomous, multi-alloy optimization |
| Scalmalloy® (Sc-containing) | APWorks / Airbus ecosystem | Al-Mg-Sc-Zr | No | No — depends on critical Sc | High-performance AM alloy; reported UTS ~496 MPa after aging/heat treatment (knoop2020atailoredalsimg pages 8-10) | FLAIME aims to eliminate Sc dependence entirely while approaching useful strength-ductility performance in Al-Zr and Al-Mn-Cr-Zr families |


*Table: This table compares FLAIME against the most relevant state-of-the-art programs and baselines for Topic 3B, emphasizing where competitors have demonstrated closed-loop optimization, supply-risk awareness, or strong alloy performance. It is useful for positioning FLAIME's unique combination of autonomous experimentation, LPBF integration, and explicit critical-mineral-demand reduction.*

## 6. New Metric Category: Critical Mineral Impact

A dedicated "Critical Mineral Impact" metric category is introduced to quantify the central deliverable of Topic 3B. This category comprises six metrics spanning compositional discovery, supply-risk reduction, mass displacement, incumbent replacement potential, search efficiency, and performance parity.

The **Supply Risk Index Reduction (ΔSR)** metric is anchored in the Mulukutla et al. (2024) framework, which computes SRmean as a weighted mean of 12 indicators across four groups: supply reduction (S1–S3), demand-driven risks (D1–D4), market concentration (C1–C2), and political risks (P1–P3), normalized to 0–100 (mulukutla2024supplyriskawarealloy pages 2-5). The USGS 2025 critical minerals methodology provides complementary validation through its GDP-impact-based assessment across 84 mineral commodities, classified into five risk tiers from "negligible" to "high" using Jenks natural breaks optimization (nassar2025methodologyandtechnical pages 9-10, nassar2025methodologyandtechnical pages 25-26). The Graedel et al. (2012) three-axis criticality framework (Supply Risk, Environmental Implications, Vulnerability to Supply Restriction) offers additional theoretical grounding, with Supply Risk composed of geological/technological/economic, social/regulatory, and geopolitical components including the Herfindahl-Hirschman Index for production concentration (graedel2012methodologyofmetal pages 1-5, graedel2012methodologyofmetal pages 26-32).

The **Critical Element Mass Displacement** metric translates compositional avoidance into tangible impact: for example, Scalmalloy® contains ~0.7 wt% Sc—one of the most supply-critical elements (lusty2021ukcriticalityassessment pages 26-28, knoop2020atailoredalsimg pages 8-10)—meaning each metric ton of Scalmalloy® production requires ~7 kg of scandium. A FLAIME Al-Zr alloy achieving comparable performance with 0 wt% Sc displaces this entire demand.

The **Beryllium Elimination Potential** metric addresses the Cu-Cr-Zr stretch goal specifically, quantifying how close LPBF Cu-Cr-Zr approaches the strength × conductivity product of Be-Cu. This is measured as a percentage of the Be-Cu performance envelope, with Phase I targeting ≥30% (feasibility) and Phase II targeting ≥70% (application viability) (biffi2024cucrzralloymanufactured pages 4-8).

| Metric Name | Definition | Calculation Method | Phase I Target | Phase II Target |
|---|---|---|---|---|
| Mineral-Lean Compositions Discovered | Count of unique compositions meeting performance thresholds with 0 wt% Mg/Sc/REE/Be; for Al families, qualifying means YS≥250 MPa and EL≥5%; for Cu-Cr-Zr, qualifying means jointly meeting predefined conductivity and strength thresholds (arena2024novelaluminumalloy pages 4-6, biffi2024cucrzralloymanufactured pages 4-8, nassar2025methodologyandtechnical pages 9-10) | ICP-OES-verified composition plus ASTM E8 tensile data for Al families; for Cu-Cr-Zr, composition verification plus tensile and conductivity measurements; count only unique compositions that satisfy both chemistry and performance criteria (arena2024novelaluminumalloy pages 4-6, biffi2024cucrzralloymanufactured pages 4-8) | ≥3 compositions | ≥15 compositions across 3+ families |
| Supply Risk Index Reduction (ΔSR) | Percentage reduction in alloy-level Helbig-style supply risk index relative to incumbent alloy (AlSi10Mg for Al benchmarking, Be-Cu for Cu benchmarking) (mulukutla2024supplyriskawarealloy pages 2-5, mulukutla2024supplyriskawarealloy pages 16-18) | Compute alloy-level SRmean using the 12-indicator Helbig framework as implemented by Mulukutla et al. 2024, then report ΔSR = [1 − SRmean(FLAIME alloy) / SRmean(incumbent)] × 100% (mulukutla2024supplyriskawarealloy pages 10-12, mulukutla2024supplyriskawarealloy pages 2-5, mulukutla2024supplyriskawarealloy pages 12-16) | ≥25% reduction for best alloy | ≥40% mean reduction across portfolio |
| Critical Element Mass Displacement | Estimated kg of Sc/Mg/REE/Be displaced per metric ton of FLAIME alloy produced relative to an incumbent that contains those elements or depends on them in the use case (nassar2025methodologyandtechnical pages 9-10, fortier2018draftcriticalmineral pages 9-10, lusty2021ukcriticalityassessment pages 26-28) | Mass balance: Σ[(wt% critical element in incumbent − wt% in FLAIME alloy) × production tonnage scenario]; report by element and as total critical-element displacement for stated production scenario (mulukutla2024supplyriskawarealloy pages 2-5, nassar2025methodologyandtechnical pages 9-10) | Calculate displacement for 1 MT production scenario | Validated displacement for 10 MT scenario |
| Beryllium Elimination Potential (Cu-Cr-Zr specific) | Fraction of Be-Cu application performance envelope reached by FLAIME Cu-Cr-Zr using a strength-conductivity product as the comparison basis (biffi2024cucrzralloymanufactured pages 4-8, nassar2025methodologyandtechnical pages 9-10) | Be-elimination potential = [(YS × conductivity)<sub>Cu-Cr-Zr</sub> / (YS × conductivity)<sub>Be-Cu</sub>] × 100%; use consistent conductivity units, e.g., %IACS, and matched test conditions (biffi2024cucrzralloymanufactured pages 4-8) | ≥30% of Be-Cu performance product | ≥70% |
| Compositional Search Space Efficiency | Fraction of tested mineral-lean compositions that yield qualifying alloys, measuring how effectively BOFN navigates the constrained mineral-lean search space (hastings2024aninteroperablemulti pages 1-2, hastings2024aninteroperablemulti pages 13-15) | Search-space efficiency = qualifying compositions / total mineral-lean compositions tested; report over pre-registered benchmark runs and confidence intervals where applicable (hastings2024aninteroperablemulti pages 1-2, hastings2024aninteroperablemulti pages 13-15) | ≥15% hit rate | ≥30% |
| Incumbent Parity Index | Number of key properties where a FLAIME mineral-lean alloy matches or exceeds the relevant incumbent benchmark, e.g., AlSi10Mg for Al families or Be-Cu for Cu applications (arena2024novelaluminumalloy pages 4-6, biffi2024cucrzralloymanufactured pages 4-8) | Count property-wise comparisons where FLAIME ≥ incumbent; for Al families use YS, UTS, EL; for Cu family use strength, conductivity, and ductility or thermal/electrical proxy as pre-registered for the application (arena2024novelaluminumalloy pages 4-6, biffi2024cucrzralloymanufactured pages 4-8) | Parity in ≥2 of 3 key properties for Al families | Full parity in all key properties for ≥2 alloy families |


*Table: This table defines a dedicated Topic 3B metric set for quantifying critical-mineral-demand reduction, supply-risk improvement, and incumbent replacement value. It is useful because it translates the proposal’s mineral-lean materials strategy into measurable Phase I and Phase II outcomes.*

## Summary of Key Changes from Topic 12F to Topic 3B

The metrics reassessment introduces three fundamental shifts: (1) every KPI and gate now includes a critical-mineral-avoidance or supply-risk-reduction dimension; (2) material performance targets are alloy-family-specific rather than generic, calibrated against the best available LPBF literature for Al-Zr (Ge et al. 2025), Al-Mn-Cr-Zr (Mehta et al. 2022; Arena et al. 2024), and Cu-Cr-Zr (Biffi et al. 2024); and (3) the Phase II narrative is reoriented from temperature upgrade to expanded mineral-lean discovery and Cu-Cr-Zr full optimization. The BOFN mineral-burden objective—implemented as supply-risk scalarization or MOBO extension per Mulukutla et al. (2024)—is elevated to both a headline KPI and a go/no-go gate, reflecting its centrality to Topic 3B's mandate of reducing demand for critical minerals.

References

1. (ge2025highstrengthadditivelymanufacturable pages 1-2): Zhaoxuan Ge, Shaolou Wei, Zehua Liu, Tomasz Choma, Lukasz Zrodowski, Marc De Graef, A. John Hart, and S. Mohadeseh Taheri-Mousavi. High-strength additively manufacturable al-zr-er-ni alloys with high as-built ductility and thermal stability. May 2025. URL: https://doi.org/10.21203/rs.3.rs-6558867/v1, doi:10.21203/rs.3.rs-6558867/v1.

2. (mulukutla2024supplyriskawarealloy pages 2-5): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

3. (mulukutla2024supplyriskawarealloy pages 16-18): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

4. (mulukutla2024supplyriskawarealloy pages 12-16): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

5. (mulukutla2024supplyriskawarealloy pages 10-12): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

6. (arena2024novelaluminumalloy pages 4-6): Maurizio Arena, Bharat Mehta, Tommaso Tirelli, Paolo Ambrogiani, Martina Castaldo, Sven Bengtsson, and Lars Nyborg. Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives. Applied Sciences, 14:4647, May 2024. URL: https://doi.org/10.3390/app14114647, doi:10.3390/app14114647. This article has 0 citations.

7. (hastings2024aninteroperablemulti pages 1-2): Trevor Hastings, Mrinalini Mulukutla, Danial Khatamsaz, Daniel Salas, Wenle Xu, Daniel Lewis, Nicole Person, Matthew Skokan, Braden Miller, James Paramore, Brady Butler, Douglas Allaire, Ibrahim Karaman, George Pharr, Ankit Srivastava, and Raymundo Arroyave. An interoperable multi objective batch bayesian optimization framework for high throughput materials discovery. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2405.08900, doi:10.48550/arxiv.2405.08900. This article has 1 citations.

8. (hastings2024aninteroperablemulti pages 13-15): Trevor Hastings, Mrinalini Mulukutla, Danial Khatamsaz, Daniel Salas, Wenle Xu, Daniel Lewis, Nicole Person, Matthew Skokan, Braden Miller, James Paramore, Brady Butler, Douglas Allaire, Ibrahim Karaman, George Pharr, Ankit Srivastava, and Raymundo Arroyave. An interoperable multi objective batch bayesian optimization framework for high throughput materials discovery. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2405.08900, doi:10.48550/arxiv.2405.08900. This article has 1 citations.

9. (mulukutla2024illustratinganeffective pages 20-23): Mrinalini Mulukutla, A. Nicole Person, Sven Voigt, Lindsey Kuettner, Branden Kappes, Danial Khatamsaz, Robert Robinson, Daniel Salas Mula, Wenle Xu, Daniel Lewis, Hongkyu Eoh, Kailu Xiao, Haoren Wang, Jaskaran Singh Saini, Raj Mahat, Trevor Hastings, Matthew Skokan, Vahid Attari, Michael Elverud, James D. Paramore, Brady Butler, Kenneth Vecchio, Surya R. Kalidindi, Douglas Allaire, Ibrahim Karaman, Edwin L. Thomas, George Pharr, Ankit Srivastava, and Raymundo Arróyave. Illustrating an effective workflow for accelerated materials discovery. Integrating Materials and Manufacturing Innovation, 13:453-473, Jun 2024. URL: https://doi.org/10.1007/s40192-024-00357-3, doi:10.1007/s40192-024-00357-3. This article has 17 citations and is from a peer-reviewed journal.

10. (mulukutla2024illustratinganeffective pages 5-7): Mrinalini Mulukutla, A. Nicole Person, Sven Voigt, Lindsey Kuettner, Branden Kappes, Danial Khatamsaz, Robert Robinson, Daniel Salas Mula, Wenle Xu, Daniel Lewis, Hongkyu Eoh, Kailu Xiao, Haoren Wang, Jaskaran Singh Saini, Raj Mahat, Trevor Hastings, Matthew Skokan, Vahid Attari, Michael Elverud, James D. Paramore, Brady Butler, Kenneth Vecchio, Surya R. Kalidindi, Douglas Allaire, Ibrahim Karaman, Edwin L. Thomas, George Pharr, Ankit Srivastava, and Raymundo Arróyave. Illustrating an effective workflow for accelerated materials discovery. Integrating Materials and Manufacturing Innovation, 13:453-473, Jun 2024. URL: https://doi.org/10.1007/s40192-024-00357-3, doi:10.1007/s40192-024-00357-3. This article has 17 citations and is from a peer-reviewed journal.

11. (mehta2021highperformancealuminium pages 33-36): B Mehta. High performance aluminium alloys for laser powder bed fusion: alloy design and development. Unknown journal, 2021.

12. (ge2025highstrengthadditivelymanufacturable pages 7-8): Zhaoxuan Ge, Shaolou Wei, Zehua Liu, Tomasz Choma, Lukasz Zrodowski, Marc De Graef, A. John Hart, and S. Mohadeseh Taheri-Mousavi. High-strength additively manufacturable al-zr-er-ni alloys with high as-built ductility and thermal stability. May 2025. URL: https://doi.org/10.21203/rs.3.rs-6558867/v1, doi:10.21203/rs.3.rs-6558867/v1.

13. (arroyave2024ultimatebirdshot.final pages 16-19): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

14. (martucci2022theinfluenceof pages 2-4): Alessandra Martucci, Bharat Mehta, Mariangela Lombardi, and Lars Nyborg. The influence of processing parameters on the al-mn enriched nano-precipitates formation in a novel al-mn-cr-zr alloy tailored for power bed fusion-laser beam process. Metals, 12:1387, Aug 2022. URL: https://doi.org/10.3390/met12081387, doi:10.3390/met12081387. This article has 5 citations.

15. (biffi2024cucrzralloymanufactured pages 4-8): Carlo Alberto Biffi, Jacopo Fiocchi, Stefano Boldrini, and Ausonio Tuissi. Cucrzr alloy manufactured by lpbf process: correlation between microstructure, mechanical and thermal properties. Lasers in Manufacturing and Materials Processing, 11:143-153, Jan 2024. URL: https://doi.org/10.1007/s40516-023-00240-7, doi:10.1007/s40516-023-00240-7. This article has 19 citations and is from a peer-reviewed journal.

16. (fiedler2024highconductivecopper pages 4-6): T. Fiedler, M. Jähnig Domingues, C. Winter, and J. Rösler. High conductive copper alloys for additive manufacturing. Progress in Additive Manufacturing, 9:1643-1652, Oct 2024. URL: https://doi.org/10.1007/s40964-023-00527-3, doi:10.1007/s40964-023-00527-3. This article has 9 citations and is from a peer-reviewed journal.

17. (hastings2024aninteroperablemulti pages 2-3): Trevor Hastings, Mrinalini Mulukutla, Danial Khatamsaz, Daniel Salas, Wenle Xu, Daniel Lewis, Nicole Person, Matthew Skokan, Braden Miller, James Paramore, Brady Butler, Douglas Allaire, Ibrahim Karaman, George Pharr, Ankit Srivastava, and Raymundo Arroyave. An interoperable multi objective batch bayesian optimization framework for high throughput materials discovery. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2405.08900, doi:10.48550/arxiv.2405.08900. This article has 1 citations.

18. (mulukutla2024supplyriskawarealloy pages 8-10): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

19. (paramore2025twoshotoptimizationof pages 16-18): James D. Paramore, Trevor Hastings, Brady G. Butler, Michael T. Hurst, Daniel O. Lewis, Eli Norris, Benjamin Barkai, Joshua Cline, Braden Miller, Jose Cortes, Ibrahim Karaman, George M. Pharr, and Raymundo Arróyave. Two-shot optimization of compositionally complex refractory alloys. Acta Materialia, pages 120820, Feb 2025. URL: https://doi.org/10.1016/j.actamat.2025.120820, doi:10.1016/j.actamat.2025.120820. This article has 9 citations and is from a highest quality peer-reviewed journal.

20. (paramore2025twoshotoptimizationof pages 1-3): James D. Paramore, Trevor Hastings, Brady G. Butler, Michael T. Hurst, Daniel O. Lewis, Eli Norris, Benjamin Barkai, Joshua Cline, Braden Miller, Jose Cortes, Ibrahim Karaman, George M. Pharr, and Raymundo Arróyave. Two-shot optimization of compositionally complex refractory alloys. Acta Materialia, pages 120820, Feb 2025. URL: https://doi.org/10.1016/j.actamat.2025.120820, doi:10.1016/j.actamat.2025.120820. This article has 9 citations and is from a highest quality peer-reviewed journal.

21. (mulukutla2024supplyriskawarealloy pages 1-2): Mrinalini Mulukutla, Robert Robinson, Danial Khatamsaz, Brent Vela, Nhu Vu, and Raymundo Arróyave. Supply risk-aware alloy discovery and design. ArXiv, Sep 2024. URL: https://doi.org/10.48550/arxiv.2409.15391, doi:10.48550/arxiv.2409.15391. This article has 1 citations.

22. (czerwinski2020ceriuminaluminum pages 26-28): Frank Czerwinski. Cerium in aluminum alloys. Journal of Materials Science, 55:24-72, Aug 2020. URL: https://doi.org/10.1007/s10853-019-03892-z, doi:10.1007/s10853-019-03892-z. This article has 263 citations and is from a peer-reviewed journal.

23. (sims2017highperformancealuminum–cerium pages 1-3): Zachary C. Sims, Orlando R. Rios, David Weiss, Patrice E. A. Turchi, Aurelien Perron, Jonathan R. I. Lee, Tian T. Li, Joshua A. Hammons, Michael Bagge-Hansen, Trevor M. Willey, Ke An, Yan Chen, Alex H. King, and Scott K. McCall. High performance aluminum–cerium alloys for high-temperature applications. Materials horizons, 4:1070-1078, Oct 2017. URL: https://doi.org/10.1039/c7mh00391a, doi:10.1039/c7mh00391a. This article has 290 citations and is from a domain leading peer-reviewed journal.

24. (sims2016ceriumbasedintermetallicstrengthenedaluminum pages 10-12): Zachary C. Sims, David Weiss, Scott K. McCall, Michael A. McGuire, Ryan T. Ott, Tom Geer, O. Rios, and P. Turchi. Cerium-based, intermetallic-strengthened aluminum casting alloy: high-volume co-product development. JOM, 68:1940-1947, May 2016. URL: https://doi.org/10.1007/s11837-016-1943-9, doi:10.1007/s11837-016-1943-9. This article has 202 citations and is from a peer-reviewed journal.

25. (knoop2020atailoredalsimg pages 8-10): Daniel Knoop, Andreas Lutz, Bernhard Mais, and Axel von Hehl. A tailored alsimg alloy for laser powder bed fusion. Metals, 10:514, Apr 2020. URL: https://doi.org/10.3390/met10040514, doi:10.3390/met10040514. This article has 51 citations.

26. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 18 citations.

27. (nassar2025methodologyandtechnical pages 25-26): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 18 citations.

28. (graedel2012methodologyofmetal pages 1-5): T. E. Graedel, Rachel Barr, Chelsea Chandler, Thomas Chase, Joanne Choi, Lee Christoffersen, Elizabeth Friedlander, Claire Henly, Christine Jun, Nedal T. Nassar, Daniel Schechner, Simon Warren, Man-yu Yang, and Charles Zhu. Methodology of metal criticality determination. Environmental science & technology, 46 2:1063-70, Jan 2012. URL: https://doi.org/10.1021/es203534z, doi:10.1021/es203534z. This article has 786 citations and is from a domain leading peer-reviewed journal.

29. (graedel2012methodologyofmetal pages 26-32): T. E. Graedel, Rachel Barr, Chelsea Chandler, Thomas Chase, Joanne Choi, Lee Christoffersen, Elizabeth Friedlander, Claire Henly, Christine Jun, Nedal T. Nassar, Daniel Schechner, Simon Warren, Man-yu Yang, and Charles Zhu. Methodology of metal criticality determination. Environmental science & technology, 46 2:1063-70, Jan 2012. URL: https://doi.org/10.1021/es203534z, doi:10.1021/es203534z. This article has 786 citations and is from a domain leading peer-reviewed journal.

30. (lusty2021ukcriticalityassessment pages 26-28): PAJ Lusty, RA Shaw, AG Gunn, and NE Idoine. Uk criticality assessment of technology critical minerals and metals. Unknown journal, 2021.

31. (fortier2018draftcriticalmineral pages 9-10): Steven M. Fortier, Nedal T. Nassar, Graham W. Lederer, Jamie Brainard, Joseph Gambogi, and Erin A. McCullough. Draft critical mineral list—summary of methodology and background information—u.s. geological survey technical input document in response to secretarial order no. 3359. Open-File Report, Jan 2018. URL: https://doi.org/10.3133/ofr20181021, doi:10.3133/ofr20181021. This article has 215 citations.