# Publication Strategy for Proposal Fundability

*Edison Scientific LITERATURE_HIGH query results (48K chars initial + 48K chars Topic 3B reassessment, 57 combined citations) + two Edison ANALYSIS reviews (tasks 13b56bed + 394ba9ab, 12K + 10K chars, scoring 70→78/100)*

*This document identifies the key publications that would most strengthen the PI's profile for competitive grant proposals. It integrates Edison Scientific literature research, mock stakeholder feedback, and the full context of the VCL research program as tracked across this repository's issues and PRs.*

> **Topic 3B Update (April 2026):** This strategy has been reassessed following the decision to target DOE Genesis Mission **Topic 3B (Critical Minerals, AMMTO)** instead of Topic 11C (AI-Accelerated Science). The project is now branded as **FLAIME (Fast-Learning AI for Mineral-Efficient Alloy Design)**. The publication portfolio emphasizes (i) critical-mineral-burden-aware optimization, (ii) substitution of Mg/Sc/REE in aluminum alloys and Be in copper alloys, and (iii) manufacturing qualification and feedstock control as enablers for critical mineral demand reduction. Material focus: **Al-Zr and Al-Mn-Cr-Zr PRIMARY (~80% Phase I), Cu-Cr-Zr COMPLEMENT (~20% stretch), AlSi10Mg baseline only.** See PR #26 and `edison-trajectories/edison-3b-deepdive-synthesis.md` for the full Topic 3B assessment.

---

## Executive Summary

A publication strategy that maximizes competitiveness for **NSF CAREER (Jul 2026), DARPA YFA/DSO, NSF DMR TMRP, and DOE Genesis Mission Topic 3B (Critical Minerals, AMMTO)** should produce (i) reusable methods with open code/benchmarks that include explicit mineral-burden metrics, (ii) credible experimental closure demonstrating critical-mineral-lean alloy substitution, and (iii) open/FAIR datasets that lower barriers for the broader community. Under Topic 3B, papers must go beyond generic AI-for-science and explicitly quantify critical mineral demand reduction, demonstrate substitution in target alloy families (Al-Zr, Al-Mn-Cr-Zr), and connect to AMMTO's emphasized gaps: upstream/midstream research, translational pathways, and manufacturability/scale-up (Kenny (2024) *AMMTO 2023 Peer Review Final Report*, Ferro and Bonollo (2019) *Materials & Design* 177:107848, Lograsso et al. (2024) *CMI Year 10 Cumulative Report* doi:10.2172/2338076).

This aligns with both community-identified priorities for self-driving labs (modular end-to-end automation, standards/interoperability, provenance-rich open data, quantitative acceleration metrics, and hybrid physics+ML integration) and DOE's 5-pillar Critical Materials Strategy — specifically Pillar 2 (Develop Alternatives), Pillar 3 (Materials & Manufacturing Efficiency), and Pillar 5 (Enabling Activities) (Abolhasani and Kumacheva (2023) *Nature Synthesis* 2:483–492, Stein and Gregoire (2019) *Chemical Science* 10:9640–9649, Trautt et al. (2024) *NIST SP 1320*, Bauer et al. (2023) *DOE Critical Materials Strategy* doi:10.2172/1998242).

The recommended portfolio of **16 publications** (14 original + 2 new 3B-native papers) is organized into three tiers:
- **Tier 1 (High ROI, submit by Q2 2026):** 9 papers leveraging current readiness — fundable differentiators before the Jul 2026 NSF CAREER deadline and April 28 Genesis Mission deadline
- **Tier 2 (Medium ROI, 2026 Q2–Q3):** 4 papers requiring more lab maturity — strengthen DARPA YFA and DOE narratives
- **Tier 3 (Capstone, 2026 Q3–Q4+):** 3 papers requiring full pipeline integration — flagship demonstrations

### Topic 3B Alignment Rubric

Each paper is now rated for 3B alignment:
- **Strong 3B-aligned:** Paper makes mineral efficiency a first-class research variable with explicit metrics (alloy criticality index, supply-risk index, CRM wt.% burden, CMDRI — Critical Mineral Demand Reduction Index) and demonstrates substitution in target alloy families
- **Medium 3B-adjacent:** Paper discusses critical-mineral avoidance in motivation/conclusion but does not use it as the organizing hypothesis
- **Weak/generic:** No explicit critical-minerals metric; optimization is only over generic properties (strength, ductility, conductivity)

---

## Context: Repository-Informed Research Program

This strategy draws on the full context of the VCL research program tracked in this repository:

**Key PRs informing publication targets:**
- PR #14 (BOFN + LLM-BO synthesis) → Publications #1, #2, #1A
- PR #4 (HT-CALPHAD/Thermo-Calc) → Publication #3
- PR #20 (LPBF parameter dimensionality) → Publications #3, #6, #14
- PR #22 (LPBF superalloy powders) → Publication #4
- PR #30 (AM scale-up test structures) → Publication #6
- PR #6 (Edison literature reviews) → Publications #10, #11
- PR #8 (Alloy databases survey) → Publication #5
- PR #18 (Welding data integration) → Publication #3
- PR #26 (Topic 3B assessment + 10-query deep-dive) → Publications #1, #1A, #3, #7, #9, #1B
- PR #34 (Genesis Mission metrics) → Publication #7
- PR #38 (LaTeX template) → All publications (proposal integration)
- PR #28 (FLAIME naming + 3B backronym) → All publications (branding)

**Key issues informing publication targets:**
- Issue #13 (LLM + BOFN integration) → Publications #1, #2, #1A
- Issue #19 (LPBF parameter dimensionality, 24+ params) → Publications #3, #14
- Issue #21 (LPBF superalloy powders) → Publication #4
- Issue #23 (Thermo-Calc AM module) → Publication #3
- Issue #29 (Scale-up validation / AM test structures) → Publication #6
- Issue #33 (Genesis Mission metrics) → Publication #7
- Issue #5 (Deep literature search) → All publications

**Topic 3B context (from PR #26 deep-dive series, ~671K chars, 250+ citations):**
- Topic 3B validated at 7.5/10 fit score, ~48% expected funding probability (vs 11C at 5.8/10)
- Material strategy: Al-Zr and Al-Mn-Cr-Zr PRIMARY (~80%), Cu-Cr-Zr COMPLEMENT (~20%)
- FLAIME backronym: "Fast-Learning AI for Mineral-Efficient Alloy Design"
- Key differentiator: no existing SDL integrates powder production + AM + tensile testing in one closed loop
- AMMTO precedent: CMI Hub funded Al-Ce alloys from discovery to TRL 9 (Lograsso et al. (2024) doi:10.2172/2338076)
- DOE 5-pillar alignment: Pillars 2, 3, and 5 (Bauer et al. (2023) doi:10.2172/1998242)

**Partnership structure (confirmed April 2026):**
- **Letters of Collaboration:** Valimet (gas atomization service contract), AMAZEMET (ultrasonic atomization/rePOWDER vendor), Thermo-Calc (CALPHAD/AM module advisory)
- **Letters of Support:** Ames National Laboratory (CMI Hub, Phase II GARS pathway), Fehrmann Alloys (feedstock supply), Taylor Sparks (University of Utah, LPBF printing), Ashley Speer (characterization), Adam Clare (AM process expertise), Chris Stiles (powder/AM engineering), Jae Hattrick-Simpers (autonomous materials experimentation), Keith Brown (Boston University, SDL pioneer)

**Preliminary results available for proposal and publication support:**
- **Atomizer installed:** AMAZEMET rePOWDER ultrasonic atomizer operational in BYU lab
- **3D-printed tensile specimens:** AlSi10Mg printed at University of Utah (sourced powder) + specimen from 3D Powder Tech
- **Tensile data:** Stress–strain curves, YS/UTS/elongation for U of Utah AlSi10Mg specimen
- **High-temperature tensile data:** Standard aluminum tensile specimen tested at elevated temperatures
- **SEM/EDS characterization:** Precursor powders (AlSi10Mg, Si powder) and AMAZEMET atomized mixture (slight composition change from original AlSi10Mg through addition of Al wire and Si)
- **Thermo-Calc AM Module simulations:** Sample calculations provided by Thermo-Calc for FLAIME alloy systems
- **BYU HPC Thermo-Calc runs:** CALPHAD phase equilibrium and Scheil solidification calculations executed on BYU clusters
- **Full pKGFN pipeline implementation:** Partial Knowledge Gradient over Function Networks (Buathong et al. 2024) ported to modern BoTorch 0.12+ with working end-to-end demo
- **Automated powder dispensing demonstration:** Proof-of-concept for closed-loop powder handling in the FLAIME pipeline

---

## Prioritized Publication Roadmap

### Publication #1 — BOFN for Multi-Stage Alloy Discovery ⭐ Highest Priority

| Attribute | Detail |
|---|---|
| **Working title** | "BOFN for Multi-Stage Critical-Mineral-Lean Alloy Discovery: Cost-Aware Bayesian Optimization over CALPHAD → Powder → LPBF → Characterization Function Networks" |
| **Paper type** | Methods |
| **Target journal(s)** | npj Computational Materials; Digital Discovery; APL Machine Learning |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DARPA YFA/DSO, AFOSR YIP, DOE Genesis Mission (Topic 3B) |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | PR #14 (BOFN BoTorch implementation), Issue #13 (LLM+BOFN exploration) |
| **3B alignment** | **Strong** — includes mineral-burden objective demonstration |

**Content focus:**
- Formalize the FLAIME pipeline as a function network with stagewise costs and partial evaluations
- Benchmark BOFN vs. vanilla BO/qNEHVI/random on synthetic and retrospective alloy-AM tasks
- Include constraint handling for printability, phase stability, and characterization throughput
- **3B addition:** Include a scalarized mineral-burden objective (alloy criticality index / supply-risk index) as one of the benchmark scenarios, demonstrating the platform discovers high-performance alloys while penalizing Mg/Sc/REE dependence (Mulukutla et al. (2024) *ArXiv* doi:10.48550/arxiv.2409.15391, Ferro and Bonollo (2019) *Materials & Design* 177:107848)
- **3B addition:** Primary design case on Al-Zr or Al-Mn-Cr-Zr space (not generic alloy families); maps to DOE CMS Pillar 2 (Develop Alternatives) and Pillar 5 (Enabling Activities)
- **Differentiation from #1A:** This paper focuses on the general BOFN methodology and algorithm contribution (stagewise costs, partial evaluations, constraint handling); #1A focuses on the materials-specific mineral-burden Pareto analysis and substitution trade-offs
- Release BoTorch code and benchmark protocol as open-source deliverables
- **Preliminary evidence available:** Full pKGFN pipeline implementation (BoTorch 0.12+), BYU HPC Thermo-Calc CALPHAD runs as function-network stage inputs, AlSi10Mg baseline tensile data from U of Utah (Taylor Sparks) and 3D Powder Tech as retrospective validation cases
- **Partnership leverage:** Thermo-Calc (CALPHAD stage), AMAZEMET (powder stage in function network DAG), Jae Hattrick-Simpers and Keith Brown as autonomous materials methodology advisors

**Mock PO feedback (NSF CAREER / DARPA / DOE 3B):**
> "This would read as a strong intellectual-merit paper because it turns the full FLAIME platform into a principled decision framework rather than a collection of tools. For DOE Topic 3B specifically, including a mineral-burden objective elevates this from a generic methods paper to a mission-aligned contribution — AMMTO reviewers want to see that AI tools are configured for critical mineral demand reduction, not just performance optimization." (Stein and Gregoire (2019) *Chemical Science* 10:9640–9649, Kavalsky et al. (2023) *Digital Discovery* 2:1112–1125, Trautt et al. (2024) *NIST SP 1320*, Kenny (2024) *AMMTO Peer Review*)

**Mock reviewer perspective:**
> "This fills the gap between generic BO papers and real materials workflows with stagewise costs, partial evaluations, and heterogeneous constraints. The addition of a mineral-burden objective makes it publishable in both the optimization and critical-materials literatures — reviewers in the supply-risk-aware alloy design community will recognize the connection to CIA/Helbig-style indicators." (Khatamsaz et al. (2023) *npj Computational Materials* 9:1–14, Mulukutla et al. (2024) *ArXiv* doi:10.48550/arxiv.2409.15391)

**Risk to preempt:** Reviewers may say it is only an algorithm paper with insufficient materials validation.
**Mitigation:** Include at least one retrospective alloy case on Al-Zr or Al-Mn-Cr-Zr data and one prospective experimental mini-demo tied to powder or LPBF decisions. Show the mineral-burden term changes the selected candidate vs. performance-only optimization.

---

### Publication #1A — Supply-Risk-Aware BOFN for Critical-Mineral-Lean Alloy Design ⭐ NEW for 3B

| Attribute | Detail |
|---|---|
| **Working title** | "Supply-Risk-Aware Bayesian Optimization over Function Networks: Alloy Discovery with Mineral-Burden Objectives" |
| **Paper type** | Methods / Results |
| **Target journal(s)** | Digital Discovery; npj Computational Materials; Sustainable Materials and Technologies |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | DOE Genesis Mission (Topic 3B), NSF CAREER, NSF DMR TMRP |
| **ROI before Jul 2026** | **High** — highest-leverage new paper for 3B alignment |
| **Repository basis** | PR #14 (BOFN), PR #26 (Topic 3B deep-dive), `edison-3b-deepdive-8-multiobjective-bofn-mineral.md` |
| **3B alignment** | **Strong** — paper is 3B-native |

**Content focus:**
- **Differentiation from #1:** This paper focuses on the materials-specific mineral-burden analysis — Pareto trade-offs, substitution evidence, and CIA/supply-risk frameworks — while #1 covers the general BOFN algorithm contribution
- Add alloy criticality index (CIA) / supply-risk index as a first-class objective in BOFN via scalarization (no code changes) or multi-objective extension (EHVI)
- Show Pareto trade-offs between mechanical performance (strength, ductility) and supply risk/mineral burden for Al alloy design
- Benchmark on Al-Zr and Al-Mn-Cr-Zr spaces: demonstrate optimizer rejecting high-criticality compositions (Mg-bearing, Sc-bearing) even when mechanically attractive
- Include recyclability and end-of-life considerations using EOL-RIR (End-of-Life Recycling Input Rate) metrics
- Explicit comparison: performance-only vs. performance+mineral-burden search to quantify the substitution trade-off
- Map to DOE CMS Pillar 2 (Develop Alternatives) and Pillar 5 (Enabling Activities)
- **Preliminary evidence available:** Full pKGFN pipeline with mineral-burden scalarization, BYU HPC Thermo-Calc phase stability screens for Al-Zr/Al-Mn-Cr-Zr candidates, Thermo-Calc AM Module printability simulations provided by Thermo-Calc for target alloy systems
- **Partnership leverage:** Thermo-Calc (CALPHAD screening data), Ames National Lab/CMI Hub (Al-Ce TRL 9 precedent as AMMTO validation), Fehrmann Alloys (feedstock supply chain context for mineral-burden calculations)

**Mock PO feedback (DOE 3B / NSF CAREER):**
> "This is the single highest-leverage paper for Topic 3B because it proves the AI core is 3B-native, not just repurposed from Topic 11C. AMMTO reviewers want to see tools configured for critical mineral demand reduction. A Pareto plot showing the optimizer balancing performance vs. mineral burden communicates the entire FLAIME value proposition in one figure." (Mulukutla et al. (2024) *ArXiv* doi:10.48550/arxiv.2409.15391, Ferro and Bonollo (2019) *Materials & Design* 177:107848, Graedel et al. (2022) *Nature Communications* 13:1–8)

**Mock reviewer perspective:**
> "Supply-risk-aware alloy design coupled to Bayesian optimization has direct precedent (Mulukutla et al. 2024), but extending it to multi-stage function networks (BOFN) where mineral burden is evaluated at multiple pipeline stages is genuinely novel. Reviewers will appreciate the explicit alloy criticality framework rather than ad hoc cost heuristics."

**Risk to preempt:** Reviewers may question whether scalarization is sufficient vs. true multi-objective Pareto optimization.
**Mitigation:** Present both approaches: scalarized (simpler, no code changes) and EHVI-based (richer Pareto), with clear discussion of when each is appropriate. Note the multi-objective extension as a Phase II enhancement.

---

### Publication #1B — Critical-Mineral-Lean Printable Al Alloys: A Perspective ⭐ NEW for 3B

| Attribute | Detail |
|---|---|
| **Working title** | "Critical-Mineral-Lean Printable Aluminum Alloys: Design Principles for Additive Manufacturing Without Mg, Sc, or REE Dependence" |
| **Paper type** | Perspective |
| **Target journal(s)** | Sustainable Materials and Technologies; MRS Bulletin; Additive Manufacturing |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | DOE Genesis Mission (Topic 3B), NSF CAREER, NSF DMR TMRP |
| **ROI before Jul 2026** | **Medium-High** — creates narrative bridge between criticality theory and experimental VCL |
| **Repository basis** | PR #26 (Topic 3B assessment), `edison-3b-deepdive-6-al-critical-mineral-lean.md` |
| **3B alignment** | **Strong** — establishes the intellectual foundation for 3B framing |

**Content focus:**
- Argue that minor critical alloying additions (Mg, Sc, REEs) impair recycling and should be avoided in new Al alloy design (Graedel et al. (2022) *Nature Communications* 13:1–8)
- Survey Al-Zr, Al-Mn-Cr-Zr, and Al-Ce families as critical-mineral-lean alternatives for LPBF AM
- Incorporate alloy criticality index (CIA) and EOL-RIR frameworks into alloy down-selection for AM (Ferro and Bonollo (2019) *Materials & Design* 177:107848)
- Position VCL/FLAIME as the enabling platform for rapid discovery in these composition spaces; maps to DOE CMS Pillar 2 (Develop Alternatives)
- Discuss Al-Ce AM precedent (Plotkowski et al. (2017) *Acta Materialia* 126:507–519) as validation of AMMTO-funded alloy development pathway
- **Preliminary evidence available:** BYU HPC Thermo-Calc CALPHAD phase diagrams for Al-Zr and Al-Mn-Cr-Zr families, Thermo-Calc AM Module printability window simulations, SEM/EDS data for AlSi10Mg precursor powders and AMAZEMET-atomized mixture as baseline comparison, high-temperature tensile data (relevant for thermal stability design requirements of Al-Zr alloys)
- **Partnership leverage:** Keith Brown and Jae Hattrick-Simpers (community perspective on SDL requirements for substitution alloys), Ames National Lab/CMI Hub (Al-Ce TRL 9 as AMMTO-validated scale-up precedent), Thermo-Calc (CALPHAD-screened composition maps)

**Mock PO feedback (DOE 3B / NSF CAREER):**
> "This paper creates the intellectual context for the entire FLAIME program under Topic 3B. Program officers will value the explicit connection between recycling-aware design, DOE CMS pillars, and practical LPBF alloy development. It positions the PI as a thought leader in critical-mineral-efficient AM alloy design."

**Risk to preempt:** Perspectives without experimental data may be discounted as speculative.
**Mitigation:** Publish alongside or after Publication #1 or #3 to anchor claims in VCL data. Include CALPHAD-screened composition maps as preliminary evidence.

---

### Publication #2 — LLM-Informed Priors for Bayesian Alloy Search

| Attribute | Detail |
|---|---|
| **Working title** | "LLM-Informed Priors for Bayesian Alloy Search: Warm-Starting Autonomous LPBF Alloy Discovery with Literature-Derived Knowledge" |
| **Paper type** | Methods |
| **Target journal(s)** | Digital Discovery; npj Computational Materials; Advanced Intelligent Discovery |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DARPA YFA, DARPA DSO BAA, AFOSR YIP |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | PR #14 (LLAMBO-style warmstart POC), Issue #13 |
| **3B alignment** | **Medium** — valuable for general fundability; strengthen by applying to Al-Zr/Al-Mn-Cr-Zr search |

**Content focus:**
- Show LLM-informed priors/warm starts improve sample efficiency in alloy search
- Compare prompt-derived priors, expert priors, and uninformed BO
- Quantify robustness, hallucination filtering, and uncertainty calibration
- Demonstrate on CALPHAD-screened alloy design tasks relevant to AM
- **3B addition:** Apply LLM-informed priors specifically to Al-Zr and Al-Mn-Cr-Zr composition search, demonstrating that literature-derived knowledge about critical-mineral-lean alloys improves sample efficiency in the mineral-lean design space
- **Preliminary evidence available:** LLAMBO-style warmstart POC v3 (PR #14) with cold-start advantage data, full pKGFN pipeline as the BO backbone, BYU HPC Thermo-Calc phase screens as the CALPHAD design space
- **Partnership leverage:** Thermo-Calc (CALPHAD design space for warm-start prior definition), Jae Hattrick-Simpers (autonomous materials methodology), Keith Brown (SDL warm-start best practices)

**Mock PO feedback (DARPA YFA/DSO/AFOSR):**
> "High-interest if framed carefully as decision-support that improves search efficiency without replacing uncertainty-aware BO. For NSF CAREER, it helps if the paper is rigorous about when language priors help and when they fail, rather than selling 'AI magic.'" (Hao et al. (2025) *ChemRxiv* doi:10.26434/chemrxiv-2025-fk3r7)

**Mock reviewer perspective:**
> "It fills the gap between hype around LLMs and fundable, auditable use of literature knowledge in autonomous materials discovery. Reviewers will appreciate explicit ablations against expert priors, naive warm starts, and no-prior baselines."

**Risk to preempt:** Over-claiming autonomy or novelty if the LLM is only used for heuristic initialization.
**Mitigation:** Benchmark against strong non-LLM baselines and report failure modes, hallucination filters, and calibration impacts explicitly. As shown in the LLAMBO-style POC (PR #14), LLM clusters near known alloys like AlSi10Mg and misses synthetic optima — this limitation should be reported transparently. The cold-start advantage was demonstrated (+0.009 initial best, 100% above threshold vs. 13–40% random), but random catches up by iteration 4, validating both benefit and exploration risk.

---

### Publication #3 — CALPHAD-in-the-Loop Active Learning for Printable Alloy Windows

| Attribute | Detail |
|---|---|
| **Working title** | "CALPHAD-in-the-Loop Active Learning for Critical-Mineral-Lean Printable Al Alloy Windows in LPBF" |
| **Paper type** | Results |
| **Target journal(s)** | Acta Materialia; Science and Technology of Advanced Materials; Computational Materials Science |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, NSF DMR TMRP, DOE Genesis Mission (Topic 3B), AFOSR YIP |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | PR #4 (HT-CALPHAD), PR #18 (welding data), PR #20 (LPBF parameters), Issue #3, Issue #23 |
| **3B alignment** | **Strong** — narrows to Al-Zr/Al-Mn-Cr-Zr with explicit Mg/Sc/REE exclusion |

**Content focus:**
- Use pycalphad to map phase stability/solidification constraints for **Al-Zr and Al-Mn-Cr-Zr** alloy families (not generic aluminum alloys)
- Couple thermodynamic screening to active learning over composition and process windows
- **3B addition:** Add screening rules that penalize or exclude Mg-, Sc-, and REE-bearing compositions, using alloy criticality index (CIA) as a filter (Ferro and Bonollo (2019) *Materials & Design* 177:107848)
- **3B addition:** Explicitly compare critical-mineral-lean vs. traditional candidates on both property potential and mineral burden
- Identify a small validated set of printable, high-value candidate compositions in mineral-lean design space
- Emphasize composition–process–microstructure decision logic
- Leverage the 24+ LPBF parameter dimensionality (Issue #19) as motivation for smart screening
- Use AlSi10Mg as baseline control only (not as a design target)
- **Preliminary evidence available:** BYU HPC Thermo-Calc CALPHAD runs (phase equilibria, Scheil solidification) for Al-Zr and Al-Mn-Cr-Zr families, Thermo-Calc AM Module printability/melt-pool simulations provided by Thermo-Calc, SEM/EDS of AlSi10Mg precursor and atomized powders as process baseline, high-temperature tensile data for thermal stability validation of Al-Zr candidates
- **Partnership leverage:** Thermo-Calc (CALPHAD + AM Module stage), Ames National Lab/CMI Hub (Al-Ce CALPHAD-to-manufacturing pathway as AMMTO validation precedent via Phase II GARS scale-up), Taylor Sparks/U of Utah (LPBF validation of screened candidates)

**Mock PO feedback (NSF DMR TMRP / DOE 3B / CAREER):**
> "This is exactly the kind of physics-plus-data paper that makes autonomous alloy discovery credible to conservative reviewers. Under Topic 3B, narrowing the CALPHAD screen to critical-mineral-lean Al families and showing that the approach can find printable compositions without Mg/Sc/REE strengthening directly addresses AMMTO's interest in substitution-driven alloy development. It maps to DOE CMS Pillar 2 (Develop Alternatives)." (Gao et al. (2023) *Science and Technology of Advanced Materials* doi:10.1080/14686996.2023.2196242, Liang et al. (2025) *Science Advances* doi:10.1126/sciadv.adu7426, Ferro and Bonollo (2023) *Sustainable Materials and Technologies* 35:e00543)

**Mock reviewer perspective:**
> "It fills a major gap in alloy informatics: many ML papers predict properties, but fewer close the loop with thermodynamic feasibility and targeted validation. Reviewers will view this as strong preliminary evidence that VCL can navigate realistic composition spaces rather than toy search problems."

**Risk to preempt:** Reviewers may question whether CALPHAD uncertainty and AM-specific nonequilibrium effects are being ignored.
**Mitigation:** Add sensitivity analyses, identify where CALPHAD is only a gate rather than ground truth, and experimentally validate both successes and misses. The Thermo-Calc AM module (Issue #23, PR #24) can provide Scheil solidification predictions that account for rapid cooling.

---

### Publication #4 — Custom Ultrasonic Atomization of AI-Designed Alloy Powders

| Attribute | Detail |
|---|---|
| **Working title** | "Custom Ultrasonic Atomization of Critical-Mineral-Lean Al Alloy Powders: Enabling Rapid Feedstock for Autonomous AM Substitution Campaigns" |
| **Paper type** | Results |
| **Target journal(s)** | Additive Manufacturing; Powder Technology; Progress in Additive Manufacturing |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF DMR TMRP, DOE Genesis Mission (Topic 3B), DARPA YFA/DSO, NSF CAREER |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | Issue #16 (test mixture preparation), Issue #58 (Si powder flow), PR #22 (LPBF powders) |
| **3B alignment** | **Strong** — addresses feedstock bottleneck for noncommercial substitution alloys |

**Content focus:**
- Demonstrate custom powder production via AMAZEMET rePOWDER for **Al-Zr and Al-Mn-Cr-Zr** compositions (primary) with Cu-Cr-Zr feasibility assessment (complement, ~20% effort — Be-Cu replacement pathway for Phase II)
- Quantify composition retention, PSD, sphericity, satellites, oxygen pickup, and flowability
- Compare pre-atomization blend vs. post-atomization powder chemistry
- **Cu-Cr-Zr complement:** Include feasibility section assessing ultrasonic atomization of Cu-Cr-Zr as a Be-free alternative (no published UA precedent for Cu-Cr-Zr — this is novel), framed as Phase II stretch with potential for AMMTO Be-substitution narrative
- **3B addition:** Frame as removing the powder procurement bottleneck that limits substitution alloy development — Al-Ce AM literature explicitly identifies powder access for noncommercial compositions as a key obstacle (Plotkowski et al. (2017) *Acta Materialia* 126:507–519)
- **3B addition:** Include discussion of closed-loop powder regeneration/reuse via UA as a manufacturing efficiency contribution (Bashmakova et al. (2026) *Journal of Manufacturing and Materials Processing* 10:93)
- **3B addition:** Map to DOE CMS Pillar 3 (Materials & Manufacturing Efficiency) — domestic feedstock agility for critical-mineral-lean compositions
- **Preliminary evidence available:** AMAZEMET rePOWDER atomizer installed and operational in BYU lab, SEM/EDS data for precursor powders (AlSi10Mg, Si) and AMAZEMET-returned atomized mixture (composition change from Al wire + Si addition), automated powder dispensing demonstration for closed-loop powder handling
- **Partnership leverage:** AMAZEMET (ultrasonic atomization vendor, Letter of Collaboration), Valimet (gas atomization benchmark comparison — commercial GA powder vs. UA powder for the same composition enables direct comparison of feedstock routes), Fehrmann Alloys (feedstock wire/ingot supply for UA input materials), Adam Clare (AM process expertise for powder-to-print qualification)

**Mock PO feedback (NSF DMR TMRP / DOE 3B / DARPA):**
> "Program officers would see this as a strategically critical enabling paper for Topic 3B because powder procurement is a recognized rate limiter for substitution alloy development. Showing that UA can produce non-commercial compositions with controlled chemistry directly addresses AMMTO's emphasis on translational pathways and manufacturing efficiency." (Zach et al. (2023) *EPJ Web of Conferences* 285:03002, Plotkowski et al. (2017) *Acta Materialia* 126:507–519, Kenny (2024) *AMMTO Peer Review*)

**Mock reviewer perspective:**
> "It fills the feedstock realism gap in autonomous alloy discovery and AM alloy design. Reviewers often worry that candidate compositions are not manufacturable as powders; this paper answers that directly with composition fidelity, morphology, and flowability data."

**Risk to preempt:** It could be read as a characterization note rather than a high-impact discovery paper.
**Mitigation:** Tie powder metrics to downstream LPBF relevance and emphasize reproducibility, composition retention, and design-space agility. SEM/EDS data for precursor powders (AlSi10Mg, Si) and the AMAZEMET-atomized mixture (composition shift from Al wire + Si addition) are already in hand as baseline characterization.

---

### Publication #5 — FAIR Powder-to-LPBF Dataset

| Attribute | Detail |
|---|---|
| **Working title** | "From Powder to Printability: A FAIR Dataset Linking Ultrasonic Atomization, Powder Metrics, and LPBF Outcomes for Critical-Mineral-Lean Alloy Feedstocks" |
| **Paper type** | Dataset |
| **Target journal(s)** | Scientific Data; Data in Brief; Digital Discovery |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DOE Genesis Mission (Topic 3B), NSF DMR TMRP |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | PR #8 (alloy databases survey), Issue #7 (alloy databases) |
| **3B alignment** | **Strong** — open data infrastructure enabling mineral-lean alloy development; maps to DOE CMS Pillar 5 (Enabling Activities) |

**Content focus:**
- Publish structured dataset linking feedstock origin, atomization settings, powder morphology, chemistry, LPBF settings, and outcomes for **Al-Zr and Al-Mn-Cr-Zr alloy families**
- Include schema, provenance, and interoperability metadata for autonomous labs
- **3B addition:** Include mineral-burden metadata (alloy criticality index, critical element wt.%) as dataset columns
- Provide baseline predictive tasks for printability and density
- Position dataset as a community benchmark for critical-mineral-lean AM alloy development
- **Preliminary evidence available:** SEM/EDS data for AlSi10Mg precursor powders, AMAZEMET atomized mixture with composition tracking, tensile data from U of Utah and 3D Powder Tech specimens (AlSi10Mg baseline), high-temperature tensile data, automated powder dispensing logs — all forming the seed dataset
- **Partnership leverage:** AMAZEMET (atomization metadata), Thermo-Calc (CALPHAD simulation data as linked dataset layer), Taylor Sparks/U of Utah (LPBF build metadata and tensile data provenance); maps to DOE CMS Pillar 5 (Enabling Activities)

**Mock PO feedback (NSF CAREER / DOE 3B):**
> "Highly fundable for Topic 3B if the dataset explicitly includes mineral-burden metrics alongside performance data — this creates reusable infrastructure that lets others design with criticality in mind. AMMTO peer reviewers value translational data infrastructure that enables broader community participation." (Trautt et al. (2024) *NIST SP 1320*, Silva et al. (2024) *DOE SDL Workshop Report* doi:10.2172/2481197, Kenny (2024) *AMMTO Peer Review*)

**Mock reviewer perspective:**
> "It fills the benchmark/data scarcity problem repeatedly identified in autonomous labs and PBF ML literature. Reviewers will value a dataset that links powder origin, atomization, LPBF settings, and outcomes because most published AM data are fragmented and not FAIR."

**Risk to preempt:** Reviewers may say the dataset is too small, too local to one machine, or insufficiently standardized.
**Mitigation:** Publish schema, metadata, uncertainty labels, and baselines; explicitly design the dataset for extension across machines and alloy families.

---

### Publication #6 — Rapid LPBF Validation with High-Throughput Characterization

| Attribute | Detail |
|---|---|
| **Working title** | "Rapid LPBF Validation of AI-Screened Alloys Using High-Throughput SEM/EDS/EBSD and Indentation Plastometry" |
| **Paper type** | Results |
| **Target journal(s)** | Additive Manufacturing; Materials & Design; Acta Materialia |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, NSF DMR TMRP, DOE Genesis Mission (Topic 3B), DARPA YFA |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | PR #30 (AM test structures), Issue #29 (scale-up validation), Issue #46 (mechanical testing), Issue #65 (PIP testing) |
| **3B alignment** | **Strong** — proves mineral-lean Al alloys are not just discoverable but printable and application-relevant |

**Content focus:**
- Print a focused matrix of **Al-Zr and Al-Mn-Cr-Zr** candidate alloys and process windows (AlSi10Mg as baseline only)
- Use SEM/EDS/EBSD + PIP indentation plastometry for fast process–structure–property mapping
- **3B addition:** Explicitly frame results as "critical-mineral-lean Al alloys achieving target performance without Mg/Sc/REE additions"
- **3B addition:** Include composition retention analysis — volatile solute loss creates qualification risk that directly impacts the 3B substitution narrative (Brice (2018) *Compositional Sensitivity in AM Al Alloy 2139*)
- Show ranking of alloy candidates without waiting for full mechanical campaigns
- Correlate rapid characterization outputs to BO objectives/constraints
- Use the AM test structure taxonomy from PR #30 (NIST artifact, ISO 52902, density cubes, tensile bars)
- **Preliminary evidence available:** AlSi10Mg tensile specimens printed at U of Utah (sourced powder) and from 3D Powder Tech, stress–strain data with YS/UTS/elongation, SEM/EDS microstructural analysis of precursor and atomized powders, high-temperature tensile data as mechanical baseline, Thermo-Calc AM Module simulations for printability window validation
- **Partnership leverage:** Taylor Sparks/U of Utah (LPBF printing partner), Ashley Speer (characterization support for SEM/EDS/EBSD and mechanical testing), Adam Clare (AM process validation expertise), Thermo-Calc (AM Module printability predictions for validation comparison); maps to DOE CMS Pillar 3 (Materials & Manufacturing Efficiency)

**Mock PO feedback (CAREER / TMRP / DOE 3B / DARPA):**
> "For Topic 3B, this is the most proposal-relevant credibility paper: it shows the platform can deliver not just discovery but application-facing evidence supporting substitution and qualification pathways. AMMTO reviewers want to see manufactured validation, not just computational screening." (Abolhasani and Kumacheva (2023) *Nature Synthesis* 2:483–492, Samadiani et al. (2025) *Journal of Intelligent Manufacturing* doi:10.1007/s10845-024-02490-4, Kenny (2024) *AMMTO Peer Review*)

**Mock reviewer perspective:**
> "It fills the validation gap that plagues many alloy-ML papers by showing a practical, high-throughput process–structure–property loop using SEM/EDS/EBSD and plastometry. Reviewers will see it as a pragmatic bridge between screening and full mechanical qualification."

**Risk to preempt:** Reviewers may question whether rapid proxies really predict meaningful performance.
**Mitigation:** Correlate rapid characterization outputs with at least a limited set of conventional mechanical tests and defect metrics. The ASTM E3499-25 standard (2025) for PIP testing strengthens this case. Tensile data from U of Utah and 3D Powder Tech AlSi10Mg specimens and high-temperature tensile data provide the conventional mechanical baseline for comparison.

---

### Publication #7 — Closed-Loop Benchmarking Metrics for VCL

| Attribute | Detail |
|---|---|
| **Working title** | "Closed-Loop Benchmarking Metrics for Autonomous Alloy Discovery: Time-to-Discovery, Human-Lag, and Experiment Efficiency in the Vertical Cloud Lab" |
| **Paper type** | Methods / Dataset |
| **Target journal(s)** | Digital Discovery; ACS Measurement Science Au; Nature Communications Engineering |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DARPA YFA/DSO, DOE Genesis Mission (Topic 3B) |
| **ROI before Jul 2026** | **High** |
| **Repository basis** | PR #34 (Genesis Mission metrics), Issue #33 (brainstorm metrics/measurables) |
| **3B alignment** | **Medium** — strengthen by including mineral-burden-specific acceleration metrics |

**Content focus:**
- Define benchmark metrics for autonomous materials pipelines: acceleration factor, decision latency, experiment efficiency, and cost per validated candidate
- **3B addition:** Include mineral-burden discovery rate (qualified alloys per unit mineral burden) and critical mineral substitution efficiency as benchmark metrics alongside generic acceleration factors; maps to DOE CMS Pillar 5 (Enabling Activities)
- Benchmark ablations: no LLM prior, no BOFN, no CALPHAD gate, no powder loop
- Report reproducible campaign logs and stopping criteria
- Provide benchmark suite and evaluation scripts
- **Preliminary evidence available:** Full pKGFN pipeline (end-to-end benchmark-ready), automated powder dispensing demonstration as a cycle-time data point, Thermo-Calc simulations (BYU HPC + AM Module) as CALPHAD-gate benchmarks
- **Partnership leverage:** Jae Hattrick-Simpers and Keith Brown (SDL benchmarking methodology advisors), Chris Stiles (powder/AM engineering cycle-time validation)

**Mock PO feedback (NSF CAREER / DARPA / DOE):**
> "This is a strong community-building paper because it creates measurable standards for acceleration, human-lag reduction, and experiment efficiency rather than anecdotal 'faster discovery' claims. Program officers will like it if tied to open campaign logs and reproducible evaluation." (Kavalsky et al. (2023) *Digital Discovery* 2:1112–1125)

**Mock reviewer perspective:**
> "It fills the benchmarking void identified across self-driving lab literature, where many groups claim autonomy without comparable metrics. Reviewers will appreciate ablation studies showing what BOFN, CALPHAD gates, and LLM priors each contribute."

**Risk to preempt:** It may be criticized as meta-science without enough materials novelty.
**Mitigation:** Anchor the metrics paper in one real VCL campaign and release the benchmark tooling with example datasets. The Genesis Mission go/no-go milestones (Issue #33) provide a natural evaluation framework.

---

### Publication #8 — FAIR Orchestration and Provenance for VCL

| Attribute | Detail |
|---|---|
| **Working title** | "FAIR Orchestration for Vertical Cloud Labs: Metadata, Provenance, and Interoperable Control of Alloy Discovery Workflows" |
| **Paper type** | Dataset / Methods |
| **Target journal(s)** | Digital Discovery; Science and Technology of Advanced Materials: Methods; Patterns |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DOE Genesis Mission (Topic 3B), DARPA DSO BAA |
| **ROI before Jul 2026** | **Medium-High** |
| **3B alignment** | **Medium** — strengthen by incorporating mineral-burden metadata in the data model |

**Content focus:**
- Define VCL data model spanning composition design, powder atomization, LPBF, microscopy, and plastometry
- **3B addition:** Include mineral-burden metadata schema (alloy criticality index, CRM wt.%, supply-risk index) as first-class fields in the data model; maps to DOE CMS Pillar 5 (Enabling Activities)
- Implement machine-readable metadata/provenance and APIs for stage-to-stage handoff
- Release lightweight orchestration layer or adapters for instrument interoperability
- Emphasize reproducibility and autonomous-lab readiness
- **Preliminary evidence available:** Automated powder dispensing demonstration (stage handoff example), pKGFN pipeline orchestration, BYU HPC Thermo-Calc batch job workflows, SEM/EDS data with instrument metadata
- **Partnership leverage:** Jae Hattrick-Simpers (autonomous lab interoperability standards), Thermo-Calc (CALPHAD API integration), Keith Brown (SDL orchestration methodology)

**Mock PO feedback (DOE / NSF CAREER / DARPA DSO):**
> "Program officers will view this favorably if it is presented as infrastructure enabling reproducibility, interoperation, and future federation with other labs. It is especially valuable for DOE-style ecosystem building and DARPA transition narratives." (Trautt et al. (2024) *NIST SP 1320*, Silva et al. (2024) *DOE SDL Workshop Report*)

**Mock reviewer perspective:**
> "It fills the standards/provenance gap: many autonomous labs are impressive but difficult to reproduce or interconnect. Reviewers will credit a paper that captures machine-readable metadata across design, powder, print, and characterization stages."

**Risk to preempt:** Reviewers may see it as engineering plumbing rather than science.
**Mitigation:** Pair the metadata/orchestration framework with one scientific use case showing how provenance changed model quality or campaign decisions.

---

### Publication #9 — Autonomous Multiobjective Search of Printable Alloys

| Attribute | Detail |
|---|---|
| **Working title** | "Autonomous Multiobjective Search of Critical-Mineral-Lean Printable Alloys: Joint Optimization of Composition, Process Window, Rapid Property Proxies, and Mineral Burden" |
| **Paper type** | Results |
| **Target journal(s)** | npj Computational Materials; Additive Manufacturing; Materials Horizons |
| **Estimated submission** | 2026 Q2–Q3 |
| **Grants strengthened** | DARPA YFA, DOE Genesis Mission (Topic 3B), NSF CAREER, AFOSR YIP |
| **ROI before Jul 2026** | **Medium-High** |
| **3B alignment** | **Strong** — full closed-loop demonstration with mineral-burden objective |

**Content focus:**
- **Differentiation from #1A:** #1A is a benchmark/methodology paper showing mineral-burden Pareto analysis on retrospective data; #9 is an experimental campaign paper demonstrating the full closed-loop pipeline on real alloys in the lab
- Execute a real or hybrid closed loop optimizing composition + LPBF parameters + rapid property proxies **+ mineral burden**
- Use constrained/multiobjective BOFN or qNEHVI to handle density, defect avoidance, plastometry targets, **and critical mineral content**
- Demonstrate Pareto front improvement over expert baselines **including at least one case where mineral burden changes the selected candidate**
- Include at least one experimentally compelling alloy/process result in **Al-Zr or Al-Mn-Cr-Zr** space
- **3B addition:** Show explicit comparison of performance-only vs. performance+mineral-burden Pareto fronts, with mineral-burden metrics (CIA, supply-risk index, CRM wt.%) as explicit optimization objectives; maps to DOE CMS Pillar 2 (Develop Alternatives) and Pillar 3 (Materials & Manufacturing Efficiency)
- **Preliminary evidence available:** Full pKGFN pipeline with mineral-burden scalarization, BYU HPC Thermo-Calc CALPHAD screens, AlSi10Mg baseline tensile data from U of Utah and 3D Powder Tech, SEM/EDS powder characterization, automated powder dispensing for closed-loop readiness, high-temperature tensile data for thermal stability objectives
- **Partnership leverage:** Jae Hattrick-Simpers and Keith Brown (SDL methodology), Taylor Sparks/U of Utah (LPBF validation), AMAZEMET (powder loop), Thermo-Calc (CALPHAD/AM Module), Ashley Speer (characterization), Chris Stiles (powder/AM engineering)

**Mock PO feedback (DARPA YFA / DOE 3B / CAREER):**
> "This is the flagship demonstration paper for Topic 3B: it proves the platform can autonomously discover mineral-lean alloys while navigating realistic performance-cost-mineral trade-offs. AMMTO reviewers will see this as the clearest evidence that FLAIME is configured for critical mineral demand reduction, not just alloy optimization." (Liang et al. (2025) *Science Advances*, Khatamsaz et al. (2023) *npj Computational Materials*, Mulukutla et al. (2024) *ArXiv* doi:10.48550/arxiv.2409.15391)

**Mock reviewer perspective:**
> "It fills the gap between isolated optimizer demonstrations and actual autonomous materials campaigns under realistic constraints. Reviewers will value Pareto-front reasoning, explicit feasibility constraints, and comparison to expert or one-factor-at-a-time baselines."

**Risk to preempt:** Over-claiming a "fully autonomous" pipeline when human intervention still exists.
**Mitigation:** Define the autonomy boundary clearly, document handoffs, and report which stages were automated versus supervised.

---

### Publication #10 — Perspective: Integrated Feedstock-to-Performance Loops

| Attribute | Detail |
|---|---|
| **Working title** | "Perspective: Autonomous Alloy Discovery Needs Integrated Feedstock-to-Performance Loops, Not Isolated Optimizers" |
| **Paper type** | Perspective |
| **Target journal(s)** | Nature Reviews Materials; MRS Bulletin; Joule |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DARPA YFA/DSO, DOE Genesis Mission (Topic 3B), NSF DMR TMRP |
| **ROI before Jul 2026** | **Medium** |
| **3B alignment** | **Medium** — strengthen by framing the integration argument through critical-mineral-lean manufacturing |

**Content focus:**
- Argue for integrated composition→powder→print→characterization loops in AM alloy design, framed through the lens of critical mineral demand reduction
- Position FLAIME architecture against current fragmented literature:
  - APEX (Autonomous Platform for EXperimentation) at LLNL — autonomous DED synthesis + characterization, ~48 samples/day
  - AMASE (Autonomous Materials Search Engine) at UMD/NIST — real-time closed-loop BO + CALPHAD for phase diagram mapping
  - PAL 2.0 (Predictive Autonomous Laboratory) at JHU — closed-loop ML + BO with rapid arc-melting validation
  - A-Lab (LBNL + DeepMind) — autonomous powder synthesis + XRD, but stops at powder characterization
- **3B addition:** Explicitly highlight that no existing SDL integrates powder production + AM + tensile testing — FLAIME's unique positioning for Topic 3B
- **3B addition:** Argue that integrated feedstock loops are essential for substitution alloy development because powder access is the key bottleneck (Plotkowski et al. (2017) *Acta Materialia* 126:507–519)
- Propose community benchmarks, datasets, and interoperability standards
- Co-author with Gus L.W. Hart (BYU) to amplify thought leadership
- **Preliminary evidence available:** All FLAIME sub-loop demonstrations (atomizer operational, UA powder characterized, tensile specimens from U of Utah and 3D Powder Tech, pKGFN pipeline, automated powder dispensing, Thermo-Calc AM Module simulations) as concrete examples anchoring the perspective argument
- **Partnership leverage:** Keith Brown (Boston U SDL pioneer, community voice), Jae Hattrick-Simpers (autonomous materials perspective), Ames National Lab (CMI Hub Al-Ce TRL 9 pathway as exemplar of integrated feedstock-to-performance loop), Taylor Sparks/U of Utah (LPBF validation perspective)

**Mock PO feedback (CAREER / DARPA / DOE):**
> "Program officers may like this as a thought-leadership piece, especially with a senior coauthor, because it articulates why autonomous AM alloy discovery needs integrated feedstock-to-performance loops. But it only helps if backed by real preliminary results." (Silva et al. (2024) *DOE SDL Workshop Report*, Banerjee et al. (2025) *MRS Bulletin* 50:190–207)

**Risk to preempt:** It may be discounted as speculative if published too early.
**Mitigation:** Publish only after at least two substantive methods/results papers are accepted or in review, and anchor claims in VCL data.

---

### Publication #11 — Review on ML for Alloys in Autonomous Manufacturing

| Attribute | Detail |
|---|---|
| **Working title** | "Machine Learning for Alloys in the Age of Autonomous Manufacturing: From Screening to Qualification" |
| **Paper type** | Review |
| **Target journal(s)** | Annual Review of Materials Research; Current Opinion in Solid State and Materials Science; MRS Bulletin |
| **Estimated submission** | 2026 Q1–Q2 |
| **Grants strengthened** | NSF CAREER, DOE Genesis Mission (Topic 3B), AFOSR YIP |
| **ROI before Jul 2026** | **Medium** |
| **3B alignment** | **Medium** — include critical minerals angle in the ML-for-alloys review |

**Content focus:**
- Bridge alloy informatics, CALPHAD, AM process optimization, and self-driving labs
- Highlight where alloy ML has lacked experimental closure and feedstock realism
- **3B addition:** Include section on criticality-aware alloy design: CIA, supply-risk indices, recycling-aware material selection, and how ML can integrate these metrics (Ferro and Bonollo (2019) *Materials & Design* 177:107848, Graedel et al. (2022) *Nature Communications* 13:1–8); reference AMMTO-funded alloy programs (CMI Hub Al-Ce) as validation exemplars
- Identify open problems in data scarcity, uncertainty, and certification for AM alloys
- Use FLAIME as a forward-looking organizing framework
- Co-author with Hart (BYU) for credibility
- **Preliminary evidence available:** pKGFN pipeline as illustrative case study, BYU HPC Thermo-Calc CALPHAD runs, SEM/EDS powder data as real-world ML input examples
- **Partnership leverage:** Jae Hattrick-Simpers (autonomous materials review perspective), Keith Brown (SDL validation methodology), Thermo-Calc (CALPHAD integration case study)

**Mock reviewer perspective:**
> "It fills the synthesis gap across alloy ML and autonomous manufacturing communities, which often cite different literatures and evaluate success differently. Reviewers may appreciate the PI showing command of both metallurgy and AI-enabled experimentation."

**Risk to preempt:** Spending time on a review instead of generating preliminary data before CAREER.
**Mitigation:** Keep it invited/short if possible, and do not let it displace the top seven data-bearing papers.

---

### Publication #12 — End-to-End FLAIME Demonstration (Capstone)

| Attribute | Detail |
|---|---|
| **Working title** | "End-to-End Demonstration of FLAIME for AI-Accelerated Critical-Mineral-Lean Alloy Discovery and Autonomous Additive Manufacturing" |
| **Paper type** | Results |
| **Target journal(s)** | Nature Communications; Science Advances; Matter |
| **Estimated submission** | 2026 Q3–Q4 |
| **Grants strengthened** | DARPA YFA/DSO, DOE Genesis Mission (Topic 3B), NSF CAREER (follow-on), NSF DMR TMRP |
| **ROI before Jul 2026** | **Low** (capstone) |
| **3B alignment** | **Strong** — full pipeline demo with mineral-burden objectives on Al-Zr/Al-Mn-Cr-Zr |

**Content focus:**
- Full pipeline demo from AI proposal to powder production to LPBF validation to automated characterization and model update, using **Al-Zr or Al-Mn-Cr-Zr** primary alloy families
- Quantify cycle-time reduction and validated materials outcomes **including mineral burden reduction vs. conventional alloy routes**
- **3B addition:** Include at least one example where the mineral-burden objective changes the selected candidate, with explicit mineral-burden quantification (CIA, CRM wt.%, supply-risk index) comparing FLAIME-discovered alloys to conventional routes
- **3B addition:** Compare FLAIME closed-loop to partial-loop SDL literature (A-Lab, AMASE, Nelaturu DED) to explicitly highlight the unique powder+AM+testing integration — maps to DOE CMS Pillars 2 (Develop Alternatives), 3 (Materials & Manufacturing Efficiency), and 5 (Enabling Activities); cite AMMTO 2023 Peer Review (Kenny (2024)) as programmatic validation
- **Downstream deployment context:** Reference Framatome's Browns Ferry reactor (first AM safety-critical US commercial reactor, "born-qualified" manufacturing) and JHU APL TETRA program (NAVSEA partnership) as examples of the qualification pathway FLAIME enables for mineral-lean alloys
- Include failure analysis and human-in-the-loop boundaries
- Serve as capstone proof of platform uniqueness for Topic 3B
- **Preliminary evidence available:** All sub-loop demonstrations serve as building blocks — atomizer installed, pKGFN pipeline, CALPHAD screens, tensile data, SEM/EDS, AM Module simulations, automated powder dispensing. The capstone integrates these into a single end-to-end campaign.
- **Partnership leverage:** Full partnership network — Valimet (GA powder benchmark), AMAZEMET (UA powder loop), Thermo-Calc (CALPHAD/AM Module), Taylor Sparks/U of Utah (LPBF validation), Ashley Speer (characterization), Ames National Lab (Phase II GARS scale-up transition pathway), Chris Stiles (engineering integration), Adam Clare (AM process qualification)

**Mock PO feedback (DARPA YFA/DSO / DOE 3B):**
> "This is the eventual flagship paper because it validates the unique BYU platform end to end with an explicit critical mineral demand reduction result. For Genesis Topic 3B, it proves FLAIME is the first SDL to close the powder→AM→testing loop for mineral-lean alloy discovery. It also strengthens Pillar 3 and Pillar 5 positioning simultaneously." (Szymanski et al. (2023) *Nature* 624:86–91 [1063 citations], Lograsso et al. (2024) *CMI Year 10 Report* doi:10.2172/2338076)

**Risk to preempt:** Schedule slip and underpowered demonstration if forced before the printer, powder loop, and analytics are mature.
**Mitigation:** Treat it as a post-CAREER capstone and build it from validated sub-loops that are already publishable individually.

---

### Publication #13 — Reproducibility and Transferability of LPBF Surrogates

| Attribute | Detail |
|---|---|
| **Working title** | "Reproducibility and Transferability of LPBF Surrogates Across Alloy Families and Machines in Data-Scarce Regimes" |
| **Paper type** | Methods / Results |
| **Target journal(s)** | Journal of Intelligent Manufacturing; Additive Manufacturing; APL Machine Learning |
| **Estimated submission** | 2026 Q2–Q4 |
| **Grants strengthened** | DOE Genesis Mission (Topic 3B), DARPA DSO BAA, AFOSR YIP |
| **ROI before Jul 2026** | **Low-Medium** |
| **3B alignment** | **Medium** — strengthen by testing transferability on mineral-lean Al families |

**Content focus:**
- Test whether LPBF surrogates trained on AlSi10Mg transfer to **Al-Zr and Al-Mn-Cr-Zr** families, quantifying domain shift and data efficiency
- **3B addition:** Frame transfer learning as an accelerator for critical-mineral-lean alloy qualification — fewer experiments needed per new mineral-lean composition; maps to DOE CMS Pillar 3 (Materials & Manufacturing Efficiency)
- Evaluate across machines (BYU LPBF vs. U of Utah) and alloy families
- **Preliminary evidence available:** AlSi10Mg tensile data from U of Utah and 3D Powder Tech (source domain), BYU HPC Thermo-Calc screens for Al-Zr/Al-Mn-Cr-Zr (target domain), SEM/EDS for powder characterization across compositions
- **Partnership leverage:** Taylor Sparks/U of Utah (cross-machine validation), Thermo-Calc (CALPHAD-informed domain knowledge for transfer), Adam Clare (multi-machine AM process insights)

**Mock PO feedback (DOE 3B / DARPA DSO):**
> "Transferability is a key concern for reviewers of autonomous materials platforms — can models trained on one alloy/machine generalize? Under Topic 3B, demonstrating transfer from AlSi10Mg baselines to mineral-lean Al-Zr compositions directly proves the platform's scalability for substitution campaigns."

**Mock reviewer perspective:**
> "It fills a critical gap: most ML-for-AM papers validate on one alloy on one machine. Reviewers will appreciate cross-family transfer results, especially from a well-studied baseline (AlSi10Mg) to understudied mineral-lean targets."

**Risk to preempt:** Data may be insufficient to demonstrate meaningful transfer across alloy families.
**Mitigation:** Use CALPHAD-derived thermodynamic features (Thermo-Calc BYU HPC data) as physics-informed domain knowledge to bridge the data gap between source and target alloy families.

---

### Publication #14 — Physics-Grounded Surrogate Models for LPBF Screening

| Attribute | Detail |
|---|---|
| **Working title** | "Physics-Grounded Surrogate Models for LPBF Alloy Screening Using Rapid Microstructure and Defect Proxies" |
| **Paper type** | Methods / Results |
| **Target journal(s)** | Computational Materials Science; Materials & Design; Journal of Manufacturing Systems |
| **Estimated submission** | 2026 Q1–Q3 |
| **Grants strengthened** | NSF CAREER, DOE Genesis Mission (Topic 3B), NSF DMR TMRP |
| **ROI before Jul 2026** | **Medium** |
| **3B alignment** | **Medium** — strengthen by applying surrogates to mineral-lean Al composition space |

**Content focus:**
- Develop physics-grounded surrogate models coupling Thermo-Calc AM Module outputs (melt pool geometry, G/R, printability maps) to rapid microstructure and defect predictions
- **3B addition:** Apply surrogates to **Al-Zr and Al-Mn-Cr-Zr** composition spaces specifically, framing as an accelerator for critical-mineral-lean alloy screening; maps to DOE CMS Pillar 2 (Develop Alternatives)
- Leverage the 24+ LPBF parameter dimensionality (Issue #19, PR #20) as motivation for surrogate-based screening
- Validate against SEM/EDS characterization data and rapid mechanical proxies
- **Preliminary evidence available:** Thermo-Calc AM Module simulations (provided by Thermo-Calc), BYU HPC Thermo-Calc CALPHAD + Scheil calculations, SEM/EDS microstructural data, tensile data as ground-truth validation
- **Partnership leverage:** Thermo-Calc (AM Module physics backbone), Adam Clare (AM process model validation expertise), Taylor Sparks/U of Utah (experimental LPBF data for validation)

**Mock PO feedback (NSF CAREER / DOE 3B):**
> "Physics-grounded surrogates make the autonomous pipeline more sample-efficient and interpretable — a key credibility signal for conservative metallurgy reviewers. Under Topic 3B, applying these surrogates to mineral-lean Al compositions (Al-Zr, Al-Mn-Cr-Zr) demonstrates the platform accelerates substitution alloy screening, not just generic optimization."

**Mock reviewer perspective:**
> "It fills the gap between black-box ML surrogates and physics-based process models. Reviewers will value Thermo-Calc AM Module integration as a differentiator, especially if the surrogates show interpretable composition–process–property relationships for mineral-lean alloys."

**Risk to preempt:** Surrogates may not generalize beyond the training data distribution or may lose physical fidelity at extrapolation boundaries.
**Mitigation:** Validate surrogates against Thermo-Calc AM Module ground truth and experimental SEM/EDS/tensile data. Report uncertainty estimates and identify domains where the surrogate fails.

---

## Incremental Sequencing Toward the Full Autonomous Pipeline Vision

The recommended sequence is designed to **incrementally de-risk the FLAIME story** while producing **citable preliminary evidence** for proposals. Under Topic 3B, the key sequencing principle is: **lead with 3B-native evidence** (mineral-burden-aware BOFN, critical-mineral-lean framing) so reviewers cannot dismiss the pivot as superficial (Mulukutla et al. (2024) *ArXiv* doi:10.48550/arxiv.2409.15391, Kenny (2024) *AMMTO Peer Review*).

### Phase 1: Establish 3B-Native AI Core (Software + Mineral-Burden Objectives)
**Publications #1, #1A, #2, #7**

BOFN formalizes the multi-stage pipeline as a costed decision problem; the new supply-risk-aware BOFN paper (#1A) proves the AI core is configured for critical mineral demand reduction (not generic optimization); LLM-informed priors are framed as auditable warm starts; the benchmarking paper quantifies decision-latency and time-to-discovery gains. **For Topic 3B, #1A is the highest-leverage new paper** — it demonstrates that FLAIME's optimizer naturally incorporates mineral burden as a first-class objective (Mulukutla et al. (2024) *ArXiv*, Ferro and Bonollo (2019) *Materials & Design* 177:107848).

### Phase 2: Establish the Feedstock Differentiator for Substitution Alloys
**Publication #4**

Custom ultrasonic atomization is a unique capability: it removes a common failure mode in substitution alloy development (candidate compositions that cannot be sourced as powder). Powder procurement is explicitly identified as a bottleneck for noncommercial AM alloys (Plotkowski et al. (2017) *Acta Materialia* 126:507–519). UA closed-loop powder regeneration adds a Pillar-3 manufacturing efficiency angle (Bashmakova et al. (2026) *JMMP* 10:93).

### Phase 3: Publish Physics-in-the-Loop Credibility for Mineral-Lean Alloy Selection
**Publication #3**

CALPHAD-in-the-loop screening/active learning narrowed to **Al-Zr and Al-Mn-Cr-Zr** families with explicit Mg/Sc/REE exclusion. This directly mirrors high-credibility exemplars that couple thermodynamics to autonomous experimentation and quantify experiment reductions (Liang et al. (2025) *Science Advances*, Gao et al. (2023) *Science and Technology of Advanced Materials*).

### Phase 3.5: Establish the Critical-Minerals Intellectual Framework ⭐ NEW
**Publication #1B**

The perspective paper creates the narrative bridge between criticality theory and the experimental VCL program. Publish alongside Phase 3 to anchor the 3B framing with design principles (Graedel et al. (2022) *Nature Communications* 13:1–8, Ferro and Bonollo (2019) *Materials & Design*).

### Phase 4: Publish the "Data Spine" of the Lab
**Publications #5, #8**

National and community roadmaps emphasize protocols, interoperability, automated provenance/metadata capture, and open databases by default. A powder→LPBF→characterization dataset with machine-actionable metadata **including mineral-burden columns** is strategically aligned with DOE CMS Pillar 5 (Enabling Activities) (Trautt et al. (2024) *NIST SP 1320*).

### Phase 5: Publish Fast Experimental Closure with Substitution Evidence
**Publication #6**

AM literature repeatedly notes fragmentation and lack of end-to-end demonstrations. Under Topic 3B, the validation paper must show **mineral-lean Al alloys achieving target performance without Mg/Sc/REE** — this is the most proposal-relevant credibility paper for AMMTO (Samadiani et al. (2025) *Journal of Intelligent Manufacturing*, Kenny (2024) *AMMTO Peer Review*).

### Phase 6: Attempt Mineral-Burden-Aware Multiobjective Closed-Loop Autonomy
**Publication #9**

A constrained multiobjective closed-loop campaign optimizing composition + process + properties **+ mineral burden** is the "DARPA-style" demonstration that proves the platform works end-to-end for Topic 3B, built from validated sub-loop papers (Szymanski et al. (2023) *Nature* 624:86–91).

### Phase 7: Publish the Capstone End-to-End FLAIME Demo
**Publication #12**

The flagship platform paper; sequenced after constituent sub-loops are stable enough to avoid an underpowered demo. Under Topic 3B, must include at least one example where the mineral-burden objective changes the selected candidate.

---

## Highest ROI Before Jul 2026 NSF CAREER Deadline / April 28 Genesis Mission Deadline

Given the timeline constraints, the highest ROI papers are those that (i) leverage current readiness (BOFN + LLM priors + pycalphad + pKGFN pipeline), (ii) create fundable differentiators (powder, mineral-burden objectives), and (iii) generate proposal-grade preliminary evidence and open deliverables. **For the April 28 Genesis Mission deadline, papers #1A and #1B are new highest-priority additions.**

**Realistic submission timeline:**
- **Pre-proposal (by April 28 Genesis Mission):** #1A and #1B submitted or in advanced preparation
- **By June 2026 (pre-CAREER):** #4 (atomization, data in hand) + #3 (CALPHAD, BYU HPC data ready)
- **In preparation for CAREER narrative:** #1, #2, #5, #6, #7
- **Post-award proposed work:** #8, #9, #10, #11, #12, #13, #14

**Highest ROI set (aim to submit by ~2026 Q2):**

| Priority | Paper | Why High ROI | 3B Alignment |
|---|---|---|---|
| #1A | Supply-risk-aware BOFN | **Highest-leverage 3B paper** — proves AI core is 3B-native; pKGFN pipeline + BYU HPC Thermo-Calc + AM Module sims ready | **Strong** |
| #1 | BOFN for multi-stage alloy discovery | Methods + code + benchmarking — pKGFN pipeline implemented, AlSi10Mg baseline tensile data available | **Strong** |
| #1B | Critical-mineral-lean Al perspective | Creates intellectual context for entire 3B program; Thermo-Calc CALPHAD data + SEM/EDS baseline ready | **Strong** |
| #3 | CALPHAD-in-the-loop for mineral-lean windows | Physics credibility + downselect on Al-Zr/Al-Mn-Cr-Zr; BYU HPC Thermo-Calc runs + AM Module sims available | **Strong** |
| #4 | Ultrasonic atomization of mineral-lean powders | Feedstock bottleneck solution — atomizer installed, SEM/EDS of precursor + atomized powders in hand | **Strong** |
| #2 | LLM-informed priors for alloy BO | Methods + robustness/failure modes — LLAMBO POC v3 + pKGFN pipeline ready | **Medium** |
| #7 | Closed-loop benchmarking metrics | Quantitative acceleration factors — pKGFN + automated dispensing as benchmark cases | **Medium** |
| #5 | FAIR powder→LPBF dataset | Open deliverable + community signal — seed data (SEM/EDS, tensile, powder) already collected | **Strong** |
| #6 | Rapid LPBF validation | Experimental closure — AlSi10Mg tensile from U of Utah + 3D Powder Tech, high-T tensile, SEM/EDS ready | **Strong** |

This subset directly addresses the most commonly cited community gaps: **lack of benchmarks**, **data scarcity**, **partial automation**, and **missing standards/provenance**, while building toward a credible closed-loop narrative specifically for critical mineral demand reduction (Stein and Gregoire (2019) *Chemical Science*, Trautt et al. (2024) *NIST SP 1320*, Kenny (2024) *AMMTO Peer Review*).

---

## Balancing Paper Types: Methods vs. Results vs. Perspective

A grant-optimized portfolio should be intentionally imbalanced toward **data-bearing, experimentally anchored papers**, because those most strongly de-risk proposals. Under Topic 3B, AMMTO explicitly values translational, systems-level, and supply-chain-relevant outputs rather than standalone methods (Kenny (2024) *AMMTO Peer Review*).

| Paper Type | Target % | Papers | Rationale |
|---|---|---|---|
| **Methods / Software / Dataset** | 25–35% | #1, #1A, #2, #5, #7, #8 | Align with calls for open infrastructure, interoperable protocols, and quantitative closed-loop gains; #1A adds 3B-native mineral-burden objective |
| **Results** | 50–60% | #3, #4, #6, #9, #12, #13, #14 | Autonomy claims are most credible when paired with quantitative experimental outcomes and failure-mode analysis on mineral-lean alloy families |
| **Perspective / Review** | 10–20% | #1B, #10, #11 | Amplify thought leadership **after** at least two core papers are accepted/in review; #1B creates the 3B intellectual framework |

---

## Grant-Specific Mapping

### NSF CAREER (Jul 2026)
Strongest signals: intellectually cohesive research arc + evidence of execution capability.
**Key papers:** #1, #1A, #2–#7 provide reusable methods, open infrastructure, and preliminary data consistent with NSF's emphasis on broader community value (open data/software) and rigorous science. The mineral-burden objective (#1A) adds a compelling societal impact angle.

### DARPA YFA / DARPA DSO BAA
Strongest signals: "demo-ready" autonomy, transition-relevant prototypes, and quantified performance gains.
**Key papers:** #1, #2, #6, #7, #9 provide the storyline.

### NSF DMR TMRP
Strongest signals: translational relevance and manufacturable materials.
**Key papers:** #3, #4, #5, #6 tie alloy design to real feedstocks and LPBF validation (powder-to-performance). Under 3B, Al-Zr/Al-Mn-Cr-Zr families add a compelling substitution narrative.

### DOE Genesis Mission — Topic 3B (Critical Minerals, AMMTO) ⭐ Primary Target
Strongest signals: critical mineral demand reduction, substitution evidence, manufacturing/qualification, and DOE CMS pillar alignment (Pillars 2, 3, 5).
**Partnership basis:** Letters of Collaboration from Valimet (gas atomization), AMAZEMET (ultrasonic atomization), and Thermo-Calc (CALPHAD/AM module). Letters of Support from Ames National Laboratory, Fehrmann Alloys, Taylor Sparks (U of Utah LPBF), Ashley Speer, Adam Clare, Chris Stiles, Jae Hattrick-Simpers, and Keith Brown (Boston U SDL).
**Key papers (Strong 3B-aligned):** #1A (mineral-burden-aware BOFN), #1 (BOFN with mineral objective demo), #1B (critical-mineral-lean Al perspective), #3 (CALPHAD for mineral-lean Al), #4 (UA feedstock for substitution alloys), #5 (FAIR data with mineral-burden metadata), #6 (validation of mineral-lean alloys), #9 (full multiobjective campaign with mineral burden), #12 (capstone).
**Key papers (Medium 3B-adjacent):** #2, #7, #8, #10, #11 — strengthen by tying to mineral-lean alloy families and/or including mineral-burden metrics.

**What makes a paper "3B-aligned"** (per Edison analysis):
1. Makes mineral efficiency a first-class research variable with explicit metrics (CIA, supply-risk index, CRM wt.% burden, EOL-RIR, CMDRI ≥25% vs. incumbent)
2. Demonstrates substitution: alloys that avoid Mg/Sc/REE dependence or enable Be-free Cu alloys
3. Connects to manufacturing qualification: powder access, chemistry control, process/property validation
4. Maps explicitly to DOE CMS Pillars 2/3/5

**What is NOT sufficient for 3B:** Generic AI-for-science, standalone BO methods, or AM process papers without mineral-burden metrics or substitution claims (Kenny (2024) *AMMTO Peer Review*, Ferro and Bonollo (2019) *Materials & Design* 177:107848).

### AFOSR YIP / ARO YIP
Strongest signals: fundamental mechanics and materials science with defense relevance.
**Key papers:** #1, #3, #9 emphasize novel scientific insights discovered through the autonomous pipeline.

---

## Mock Fundability Scoring

Based on community-calibrated expectations for early-career proposals in this space. **Under Topic 3B, the marginal value of a critical-minerals-framed paper is higher than a generic methods paper** because it simultaneously improves program fit AND execution credibility (Kenny (2024) *AMMTO Peer Review*).

| Publication count | NSF CAREER fundability | DARPA YFA fundability | NSF DMR TMRP fundability | DOE Genesis 3B fundability |
|---|---|---|---|---|
| **0 publications** | 3/10 — concept only, high risk perception | 2/10 — no demo capability evidence | 3/10 — no preliminary data | 2/10 — no track record |
| **2 publications** (#1 + #1A) | 5/10 — methods + mineral-burden credibility | 4/10 — algorithmic novelty shown | 5/10 — CALPHAD+AL demonstrated | **5/10 — 3B-native AI + mineral objective** ↑ |
| **5 publications** (#1, #1A, #1B, #3, #4) | 7/10 — strong methods + mineral-lean powder + data | 6/10 — approaching demo readiness | 7/10 — powder-to-print pathway clear | **7/10 — substitution + feedstock + design space** ↑ |
| **9 publications** (#1–#7, #1A, #1B) | 8/10 — comprehensive preliminary portfolio | 7/10 — quantified benchmarks + demo | 8/10 — full experimental arc | **8/10 — strong 3B story with qualification evidence** ↑ |
| **Full portfolio** (16 papers) | 9/10 — exceptional for early career | 8/10 — platform validated | 9/10 — field-defining | **9/10 — complete critical-minerals platform story** ↑ |

Note: ↑ indicates improved fundability vs. generic (non-3B-aligned) versions of the same papers. The improvement is driven by AMMTO reviewers' explicit emphasis on critical materials as a priority area, translational pathways, and systems-level impact.

---

## Cross-Cutting Advice: Three Elements Every Paper Should Include

Across the portfolio, repeatedly include three elements that are explicitly valued in autonomous-lab roadmaps:

1. **Quantified acceleration**: Report time-to-discovery, decision latency, experiment counts, and cost-aware efficiency, not just "worked better" (Kavalsky et al. (2023) *Digital Discovery* 2:1112–1125).

2. **Provenance-rich FAIR outputs**: Publish machine-actionable metadata, schema, and campaign logs so others can reproduce/compare (Trautt et al. (2024) *NIST SP 1320*).

3. **Honest failure analysis**: Exemplar platforms report both successes and failure modes to identify actionable bottlenecks, increasing credibility with skeptical reviewers (Szymanski et al. (2023) *Nature* 624:86–91).

**Topic 3B addition — two elements for every 3B-aligned paper:**

4. **Explicit mineral-burden metric**: Include at least one quantitative measure of critical mineral content or supply risk (CIA, CRM wt.%, supply-risk index, EOL-RIR, CMDRI — Critical Mineral Demand Reduction Index) alongside traditional performance metrics. This converts a "generic methods" paper to a "3B-native" paper (Ferro and Bonollo (2019) *Materials & Design* 177:107848, Mulukutla et al. (2024) *ArXiv* doi:10.48550/arxiv.2409.15391).

5. **DOE CMS Pillar mapping**: State which DOE Critical Materials Strategy pillar(s) the work addresses (Pillar 2: Develop Alternatives, Pillar 3: Materials & Manufacturing Efficiency, Pillar 5: Enabling Activities) to help reviewers see programmatic relevance (Bauer et al. (2023) *DOE Critical Materials Strategy* doi:10.2172/1998242, Lograsso et al. (2024) *CMI Year 10 Report* doi:10.2172/2338076).

---

## Target Venue Summary

| Journal | Target Publications | Impact Factor | Primary Audience |
|---|---|---|---|
| npj Computational Materials | #1, #1A, #9 | ~9.4 | NSF, computational materials |
| Digital Discovery | #1A, #2, #5, #7, #8 | ~6.2 | Self-driving labs, AI+materials |
| Acta Materialia | #3, #6 | ~8.3 | Physical metallurgy, alloy design |
| Additive Manufacturing | #4, #6, #9, #1B | ~11.0 | LPBF/AM community, DoD |
| Sustainable Materials and Technologies | #1A, #1B | ~7.1 | Critical materials, sustainability |
| Scientific Data | #5 | ~5.8 | Open data, benchmarks |
| Nature Communications | #12 | ~14.7 | Broad impact, flagship |
| Science Advances | #12 | ~11.7 | Multidisciplinary |
| Nature Reviews Materials | #10 | ~79.8 | Field-defining perspectives |
| MRS Bulletin | #1B, #10, #11 | ~5.0 | Program managers, trends |

---

## Partner × Publication Contribution Matrix

This matrix explicitly maps each partner to the publications they enable, demonstrating the partnership structure is distributed and functional across the full portfolio.

| Partner | Role | Key Publications | Contribution |
|---|---|---|---|
| **Valimet** | Letter of Collaboration (GA) | #4, #12 | Gas atomization benchmark comparison; commercial GA powder for same compositions enables direct feedstock route comparison |
| **AMAZEMET** | Letter of Collaboration (UA) | #1, #4, #5, #8, #9, #12 | Ultrasonic atomization vendor; installed rePOWDER atomizer enables custom powder production for noncommercial alloys; powder stage in function network DAG |
| **Thermo-Calc** | Letter of Collaboration (CALPHAD) | #1, #1A, #1B, #2, #3, #5, #6, #7, #8, #9, #11, #12, #13, #14 | CALPHAD/AM Module simulations, phase stability screening, printability predictions, BYU HPC batch calculations |
| **Ames National Lab** | Letter of Support (CMI Hub) | #1A, #1B, #3, #10, #12 | CMI Hub Al-Ce TRL 9 precedent as AMMTO validation; Phase II GARS scale-up transition pathway |
| **Fehrmann Alloys** | Letter of Support (feedstock) | #1A, #4 | Feedstock wire/ingot supply for UA input materials; supply chain context for mineral-burden analysis |
| **Taylor Sparks (U of Utah)** | Letter of Support (LPBF) | #1, #3, #5, #6, #9, #10, #12, #13, #14 | LPBF printing for AlSi10Mg baseline specimens; cross-machine validation; build metadata |
| **Ashley Speer** | Letter of Support (characterization) | #6, #9, #12 | SEM/EDS/EBSD characterization support; mechanical testing validation |
| **Adam Clare** | Letter of Support (AM process) | #4, #6, #12, #13, #14 | AM process qualification expertise; multi-machine process insights |
| **Chris Stiles** | Letter of Support (engineering) | #7, #9, #12 | Powder/AM engineering integration; cycle-time validation for benchmarking |
| **Jae Hattrick-Simpers** | Letter of Support (autonomous) | #1, #2, #7, #8, #9, #10, #11 | Autonomous materials experimentation methodology; SDL interoperability standards; benchmarking |
| **Keith Brown (Boston U)** | Letter of Support (SDL) | #1, #1B, #2, #7, #8, #9, #10, #11 | SDL pioneer methodology; community perspective on autonomous materials discovery |

---

## References

### Original references (from initial Edison LITERATURE_HIGH query)

1. Abolhasani and Kumacheva (2023) *Nature Synthesis* 2:483–492. "The rise of self-driving labs in chemical and materials sciences." 647 citations. doi:10.1038/s44160-022-00231-0.

2. Stein and Gregoire (2019) *Chemical Science* 10:9640–9649. "Progress and prospects for accelerating materials science with automated and autonomous workflows." 260 citations. doi:10.1039/c9sc03766g.

3. Kavalsky et al. (2023) *Digital Discovery* 2:1112–1125. "By how much can closed-loop frameworks accelerate computational materials discovery?" 25 citations. doi:10.1039/d2dd00133k.

4. Trautt et al. (2024) *NIST SP 1320*. "Driving U.S. innovation in materials and manufacturing using AI and autonomous labs." doi:10.6028/nist.sp.1320.

5. Silva et al. (2024) *DOE SDL Workshop Report*. "Shaping the future of self-driving autonomous laboratories workshop." 20 citations. doi:10.2172/2481197.

6. Gao et al. (2023) *Science and Technology of Advanced Materials*. "Accelerated discovery of high-performance Al-Si-Mg-Sc casting alloys by integrating active learning with high-throughput CALPHAD calculations." 29 citations. doi:10.1080/14686996.2023.2196242.

7. Liang et al. (2025) *Science Advances*. "Real-time experiment-theory closed-loop interaction for autonomous materials science." 19 citations. doi:10.1126/sciadv.adu7426.

8. Khatamsaz et al. (2023) *npj Computational Materials* 9:1–14. "Bayesian optimization with active learning of design constraints using an entropy-based approach." 101 citations. doi:10.1038/s41524-023-01006-7.

9. Szymanski et al. (2023) *Nature* 624:86–91. "An autonomous laboratory for the accelerated synthesis of inorganic materials." 1063 citations. doi:10.1038/s41586-023-06734-w.

10. Liu et al. (2020) *Procedia Computer Science* 176:2586–2595. "Machine learning-enabled feedback loops for metal powder bed fusion additive manufacturing." 51 citations. doi:10.1016/j.procs.2020.09.314.

11. Samadiani et al. (2025) *Journal of Intelligent Manufacturing*. "Best practices for machine learning strategies aimed at process parameter development in powder bed fusion additive manufacturing." 14 citations. doi:10.1007/s10845-024-02490-4.

12. Zach et al. (2023) *EPJ Web of Conferences* 285:03002. "Spherical powders: control over the size and morphology of powders for additive manufacturing." 3 citations. doi:10.1051/epjconf/202328503002.

13. Hao et al. (2025) *ChemRxiv*. "Autonomous materials synthesis laboratories: integrating artificial intelligence with advanced robotics for accelerated discovery." 36 citations. doi:10.26434/chemrxiv-2025-fk3r7.

14. Rahman et al. (2025) *Journal of Materials Science* 60:12189–12221. "Review: machine learning approaches for diverse alloy systems." 18 citations. doi:10.1007/s10853-025-11154-4.

15. Banerjee et al. (2025) *MRS Bulletin* 50:190–207. "Materials laboratories of the future for alloys, amorphous, and composite materials." 10 citations. doi:10.1557/s43577-024-00846-y.

### Topic 3B references (from Edison LITERATURE_HIGH 3B reassessment)

16. Ferro and Bonollo (2019) *Materials & Design* 177:107848. "Materials selection in a critical raw materials perspective." 134 citations. doi:10.1016/j.matdes.2019.107848.

17. Mulukutla et al. (2024) *ArXiv*. "Supply risk-aware alloy discovery and design." 1 citation. doi:10.48550/arxiv.2409.15391.

18. Graedel, Reck, and Miatto (2022) *Nature Communications* 13:1–8. "Alloy information helps prioritize material criticality lists." 83 citations. doi:10.1038/s41467-021-27829-w.

19. Ferro and Bonollo (2019) *Recycling* 4:44. "Design for recycling in a critical raw materials perspective." 30 citations. doi:10.3390/recycling4040044.

20. Ferro and Bonollo (2023) *Sustainable Materials and Technologies* 35:e00543. "Lightweight design versus raw materials criticalities." 23 citations. doi:10.1016/j.susmat.2022.e00543.

21. Plotkowski et al. (2017) *Acta Materialia* 126:507–519. "Evaluation of an Al-Ce alloy for laser additive manufacturing." 262 citations. doi:10.1016/j.actamat.2016.12.065.

22. Brice (2018). "Compositional sensitivity in additively manufactured aluminum alloy 2139."

23. Bashmakova et al. (2026) *Journal of Manufacturing and Materials Processing* 10:93. "On the ultrasonic atomization of SS316L parts manufactured via laser powder bed fusion for the closed-loop production." doi:10.3390/jmmp10030093.

24. Lograsso, Moyer, and Thach (2024). "Critical Materials Institute (CMI) Year 10 Cumulative Report." 1 citation. doi:10.2172/2338076.

25. Bauer et al. (2023). "2023 Critical Materials Strategy." DOE. 18 citations. doi:10.2172/1998242.

26. Kenny (2024). "AMMTO 2023 Peer Review Final Report."

27. Poblano-Salas (2009) *Powder Metallurgy* 52:124–134. "High temperature properties of Cu-Cr-Zr alloys." 5 citations. doi:10.1179/174329008x293723.

28. Morozova et al. (2018) *Reviews on Advanced Materials Science* 54:56–92. "Microstructure and properties of fine grained Cu-Cr-Zr alloys." 95 citations. doi:10.1515/rams-2018-0020.

29. Yang et al. (2020) *Science China Technological Sciences* 63:2505–2517. "High strength and high conductivity Cu alloys: a review." 188 citations. doi:10.1007/s11431-020-1633-8.

30. Tom et al. (2024) *Chemical Reviews* 124:9633–9732. "Self-driving laboratories for chemistry and materials science." 618 citations. doi:10.1021/acs.chemrev.4c00055.

31. Low et al. (2024) *npj Computational Materials* 10:1–11. "Evolution-guided Bayesian optimization for constrained multi-objective optimization in self-driving labs." 67 citations. doi:10.1038/s41524-024-01274-x.
