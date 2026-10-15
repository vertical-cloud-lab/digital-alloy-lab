# FLAIME Proposal Figure Evaluation: Edison Scientific Feedback + Sustainability/Cost Integration

*Edison Scientific LITERATURE_HIGH task `e9107472-4728-45e1-9edb-8e46a1c24eac` (2026-04-04). Query evaluated 8 proposed figures for the FLAIME Genesis Mission Phase I proposal, with explicit focus on incorporating sustainability, raw material cost, and critical materials avoidance as alloy design objectives.*

## Key Edison Recommendations Summary

1. **Add a Sustainability/Cost/Performance Pareto front (new Figure 9)** — rated ESSENTIAL. Most impactful single addition.
2. **Add a Critical Materials Radar/Scorecard (new Figure 10)** — rated IMPORTANT. Can be merged as inset into Figure 9.
3. **Embed sustainability filters at CALPHAD screening (Node 0)** — computationally free, shows cost/criticality awareness pervades the workflow from first screening step.
4. **Frame Ce as earth-abundant byproduct** — turns a potential "rare earth" concern into a supply-chain resilience advantage.
5. **Merge Figure 7 (Gantt) into Figure 1 or work plan** to save figure space.
6. **All experimental figures (2, 4, 5, 8) must use real data** — no simulated powder/print/tensile results.

## Figure Priority Stack (6–8 figure budget)

| Priority | Figure | Rating | Notes |
|---|---|---|---|
| 1 | Fig 1: FLAIME DAG Overview | ESSENTIAL | Add sustainability objectives to decision engine |
| 2 | Fig 3: CALPHAD Screening + Cost/Sustainability Filters | ESSENTIAL | Transform into decision funnel with cost/criticality filters |
| 3 | Fig 8: End-to-End 3-Composition Demo | ESSENTIAL | Strongest credibility figure; all data must be real |
| 4 | Fig 5: ASTM E8/E8M Tensile Testing | ESSENTIAL | Qualification anchor; replace Ashby plot with target property window |
| 5 | Fig 9 (NEW): Sustainability/Cost/Performance Pareto | ESSENTIAL | Performance vs raw cost, colored by supply risk |
| 6 | Fig 2: Ultrasonic Atomization PoC | IMPORTANT | Add D10/D50/D90, sphericity, AM yield metrics |
| 7 | Fig 6: BOFN Retrospective Demo | IMPORTANT | Map to real 4-node costs; "best found vs $ spent" |
| 8 | Fig 4: LPBF Microstructure | IMPORTANT | Merge into Fig 8 if space tight |
| Cut | Fig 7: Throughput Gantt | NICE-TO-HAVE | Merge into Fig 1 or project management section |
| Merge | Fig 10 (NEW): Criticality Radar | IMPORTANT | Merge as inset into Fig 9 |

## Refined Figure Descriptions and Captions

### Figure 1: FLAIME Autonomous Powder-to-Part Discovery Platform

**Content:** 4-node directed acyclic graph showing Node 0 (CALPHAD/Thermo-Calc, ~$1/eval) → Node 1 (Ultrasonic Atomization, ~$200/batch) → Node 2 (LPBF at U of U, ~$500/build) → Node 3 (ASTM E8/E8M Tensile + Characterization, ~$300/composition). Central "BOFN Decision Engine" box with multi-objective targets: {YS, UTS, elongation} × {raw $/kg} × {supply risk}. Cost-aware p-KGFN arrows showing partial evaluation routing. Mon–Sat weekly cadence annotation. Optional: throughput inset from former Figure 7.

**Caption:** "FLAIME integrates CALPHAD-guided screening, rapid ultrasonic atomization, LPBF fabrication, and ASTM-standard qualification in a cost-aware function-network architecture. The BOFN decision engine with p-KGFN acquisition allocates experimental budget across nodes of varying cost, optimizing a multi-objective target spanning structural performance, raw material cost, and elemental supply-chain resilience. The platform sustains ~15 unique compositions per week in closed-loop operation."

**Data:** Workflow architecture, node costs, and facility access are real. BOFN routing arrows are schematic but reflect planned decision logic.

---

### Figure 2: Ultrasonic Atomization Proof-of-Concept — AM-Suitable Al Alloy Powder

**Content:** (a) Low-magnification SEM showing powder population morphology. (b) High-magnification SEM showing individual particle sphericity. (c) Cumulative and differential PSD with D10/D50/D90 annotations and shaded 15–63 μm AM-suitable window. (d) EDS composition verification confirming target Ce/Cu content retention. Inset table: sphericity (0.85–0.92), AM-suitable yield (%), span.

**Caption:** "Ultrasonic atomization of Al-[Ce/Cu]-X alloys using the BYU AMAZEMET rePOWDER (induction module) produces highly spherical powder with narrow particle-size distribution and AM-suitable yield in the 15–63 μm fraction. EDS confirms compositional fidelity through the atomization process. Powder quality metrics meet or exceed published benchmarks for LPBF feedstock, de-risking the powder synthesis node of the autonomous discovery loop."

**Data:** ALL REAL — SEM images, PSD measurements, EDS from BYU atomization runs.

---

### Figure 3: CALPHAD-Guided Composition Screening with Sustainability-Aware Down-Selection

**Content:** (a) Thermo-Calc Scheil solidification paths for representative Al-Ce-X compositions showing freezing range and phase fractions vs temperature. (b) Ternary composition map with cracking susceptibility index (hot color = high risk, cool = low risk). (c) **Decision funnel**: ~200 CALPHAD compositions → printability filters (freezing range < threshold, cracking susceptibility < threshold) → **cost/criticality filters** (raw elemental cost < $/kg target, supply risk score < threshold) → 15–20 candidates for experimental evaluation. Three alloy family tracks shown: Al-Ce-X (primary), Al-Cu-X, Al-Si (baseline).

**Caption:** "Physics-informed CALPHAD screening prunes large composition spaces through sequential printability and sustainability filters before expensive powder-to-part evaluation. Scheil solidification analysis identifies compositions with favorable freezing ranges and low hot-cracking susceptibility, while cost and criticality filters exclude compositions requiring expensive or supply-vulnerable elements. This computationally inexpensive screening stage ($~1/evaluation) embeds sustainability awareness from the first step of the autonomous discovery workflow, aligning alloy chemistry with DOE domestic manufacturing competitiveness goals."

**Data:** CALPHAD outputs are computational but from the real FLAIME screening workflow. Cost/criticality filters use published commodity pricing and DOE critical materials lists.

---

### Figure 4: LPBF Build Feasibility from BYU-Produced Powder

**Content:** (a) Optical micrograph cross-section with relative density annotation (target >99.5%). (b) SEM-BSE microstructure showing solidification features. (c) EBSD IPF map. (d) EDS elemental maps. Inset: process parameter window (VED, power, speed) explored at U of U.

**Caption:** "Preliminary LPBF builds at the University of Utah using BYU-atomized Al-Ce powder confirm that the powder-to-part pipeline produces dense, crack-limited structures. Relative density of [X]% and [absence/presence] of solidification cracking establish feasibility for downstream mechanical qualification. Microstructural features (Al₁₁Ce₃ intermetallics, grain morphology) are consistent with literature values for LPBF-processed Al-Ce alloys."

**Data:** ALL REAL — from BYU powder printed at U of U. Even limited data (1–2 compositions) is acceptable.

---

### Figure 5: Qualification-Relevant Tensile Properties — Full-Size ASTM E8/E8M Specimens

**Content:** (a) Representative engineering stress-strain curves for FLAIME compositions vs AlSi10Mg baseline. (b) **Target property window** plot: YS vs elongation with minimum qualification thresholds shaded, FLAIME data points, AlSi10Mg baseline, and literature Al-Ce-X benchmarks (Wei et al. 2025: YS 321 MPa / UTS 429 MPa / EL 10.9%) as open markers. Orientation, build direction, replicate count annotated.

**Caption:** "Full-size ASTM E8/E8M tensile testing links autonomous alloy discovery directly to qualification-relevant mechanical validation. FLAIME-discovered compositions are evaluated against both commercial AlSi10Mg baseline performance and published Al-Ce-X property targets. The use of full-size dogbone specimens (not sub-size) ensures direct comparability to qualification standards, accelerating the path from discovery to deployable structural performance."

**Data:** ALL REAL tensile data. Even 1 composition + baseline is stronger than many simulated curves.

---

### Figure 6: BOFN Cost-Aware Optimization — Retrospective Demonstration

**Content:** (a) "Best property found vs cumulative dollars spent" — BOFN/p-KGFN vs standard BO (full pipeline every iteration) vs random search. Real 4-node cost ratios: CALPHAD ~$1, atomization ~$200, LPBF ~$500, tensile ~$300. (b) Node evaluation frequency showing BOFN heavily exploiting cheap CALPHAD screening. (c) Cost savings: fewer expensive downstream evaluations for equivalent or better final performance. Optional inset: LLAMBO warmstarting effect on early iterations.

**Caption:** "Retrospective demonstration of Bayesian Optimization over Function Networks (BOFN) with cost-aware p-KGFN acquisition on a 4-node alloy discovery network matching FLAIME's architecture. The cost-aware strategy allocates experimental budget preferentially to inexpensive CALPHAD screening nodes, reserving costly powder synthesis, printing, and qualification evaluations for the most promising candidates. This cost-aware routing reaches equivalent performance with [X]% fewer expensive downstream evaluations compared to standard Bayesian optimization."

**Data:** Retrospective/simulated is acceptable. Node costs and DAG structure must match real FLAIME architecture.

---

### Figure 7: *(Merged into Figure 1 — see throughput annotation)*

---

### Figure 8: End-to-End Workflow Validation — 3 Compositions Through the Full Discovery Loop

**Content:** Three columns, one per composition (e.g., Al-10Ce, Al-8Ce-2Mg, AlSi10Mg baseline). Row 1: SEM powder with PSD inset. Row 2: LPBF cross-section with relative density. Row 3: Stress-strain curve. Bottom annotation: BOFN ranking showing correct prioritization of the better-performing candidate. Winner highlighted.

**Caption:** "End-to-end demonstration validates the FLAIME autonomous powder-to-part workflow on three representative alloy compositions. Each composition traverses the complete 4-node discovery loop: CALPHAD screening → ultrasonic atomization → LPBF fabrication → ASTM E8/E8M qualification. The BOFN decision engine correctly identified and prioritized [Composition X] as the highest-performing candidate, demonstrating closed-loop alloy discovery with qualification-relevant mechanical validation in a single integrated campaign."

**Data:** ALL REAL if included. This is the strongest possible preliminary data for the proposal.

---

### Figure 9 (NEW): Sustainability-Aware Pareto Front — Performance vs Cost vs Supply Risk

**Content:** (a) **Pareto front plot**: X-axis = raw alloy cost ($/kg, from elemental fractions × commodity prices). Y-axis = mechanical performance index (YS, or YS × √elongation). Color = supply risk / criticality score (green = low risk/Al-Ce-Ca; yellow = moderate/Al-Cu-X; red = high risk if Co/Ni). Markers: filled = real experimental data, hollow = CALPHAD-only candidates, connected line = Pareto-optimal set. Shaded target region: "competitive with AlSi10Mg at equal or lower cost and risk." (b) **Inset scorecard** comparing 3–5 alloy families on: raw cost, supply risk, recyclability with Al streams, embodied criticality, YS.

**Caption:** "FLAIME discovers Pareto-optimal aluminum alloys that achieve structural-alloy performance targets while minimizing raw material cost and supply-chain vulnerability. The multi-objective optimization framework treats elemental cost ($/kg), supply-risk criticality, and recyclability as first-class design objectives alongside mechanical performance. Cerium, the most abundant rare earth element and a byproduct of higher-value rare earth extraction, supports supply-chain resilience rather than threatening it. This sustainability-aware alloy selection aligns with DOE decarbonization, critical materials strategy, and domestic manufacturing competitiveness priorities."

**Data:** Mix of real and computed. Mechanical properties from real tests where available; raw cost from published commodity prices; supply risk from DOE/USGS critical materials assessments. Pareto front can include CALPHAD-only projections as prospective markers.

**Key literature:** Mulukutla et al. 2024 (supply-risk-aware alloy design), Xu et al. 2025 (multi-objective optimization), Raabe 2023 (sustainable metals), Popov et al. 2021 (critical materials in PBF-AM).

---

### Figure 10 (NEW): *(Merged as inset into Figure 9b — criticality scorecard)*

---

## Key Caption Language for DOE/AMMTO Reviewers

Per Edison feedback, use language mapping to DOE's five pillars:

| Instead of... | Use... |
|---|---|
| "cheap alloys" | "cost-effective, supply-resilient compositions" |
| "reducing cost" | "optimizing raw material affordability and supply-chain resilience as first-class design objectives" |
| "Ce is rare earth" | "Ce is the most abundant rare earth element and a byproduct of higher-value RE extraction, supporting supply-chain resilience" |
| "recyclable" | "maintains compatibility with existing aluminum recycling infrastructure, supporting circular-economy objectives" |
| "good properties" | "qualification-relevant structural performance validated via ASTM E8/E8M full-size specimens" |
| "AI-guided" | "AI-enabled accelerated discovery, consistent with AMMT Roadmap priorities for autonomous materials development" |

## Key Literature for Sustainability Integration

| Reference | Use in Proposal |
|---|---|
| Mulukutla et al. 2024, *Supply Risk-Aware Alloy Discovery and Design* | Justify adding raw cost, criticality, supply risk to optimization. Pareto figure methodology. |
| Xu et al. 2025, *Multi-objective Optimization in ML-Assisted Materials Design* | Justify Pareto front approach over single-score scalarization |
| Raabe 2023, *The Materials Science behind Sustainable Metals and Alloys* | Significance section: connect FLAIME to decarbonization and circularity |
| Popov et al. 2021, *PBF-AM Using Critical Raw Materials: A Review* | Motivate critical-material avoidance in AM feedstock selection |
| Buathong et al. 2023, *BOFN with Partial Evaluations* | Core method: cost-aware node selection in function networks |
| Buathong & Frazier 2025, *Fast BOFN* | Implementation feasibility for 9-month Phase I |
| Liu et al. 2024, *LLMs to Enhance BO (LLAMBO)* | Optional augmentation; frame conservatively |
| Wei et al. 2025, *Al-3.0Ce-xCa-yMn LPBF Optimization* | Node 0 CALPHAD screening methodology |
| Hesselmann et al. 2022, *Al-Ce Ternary Additions for LPBF* | Alloy design rationale for Al-Ce-X ternary exploration |
| Li et al. 2025, *AMMT 2025 Roadmap* | DOE alignment throughout proposal |
