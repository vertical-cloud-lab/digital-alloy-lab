# Edison Persona Mock-Review Result — TMS 2027 "Fatigue in Materials" Symposium

**Task:** `fc7c6405-877b-4794-9ab7-cae8eb9bd63d` (`LITERATURE_HIGH`) · **Status:** success
**Verdict:** SUBMIT-IF-RETAILORED (confidence ~60%) · votes 3 Reject / 2 Conditional-Accept

---

Question: ROLE: You are a panel of five TMS 2027 symposium organizers conducting a mock peer review of a submitted abstract. For each organizer, give feedback IN THEIR VOICE, grounded in their actual research expertise (summarized below), then converge on a committee recommendation. Use real literature (with DOIs/arXiv IDs) to support claims about microstructure-sensitive fatigue, defect-driven fatigue in additively manufactured (AM) aluminum, characterization for fatigue-critical microstructure, and AI/autonomous characterization.

THE SYMPOSIUM (TMS 2027; sponsored by the TMS Materials Processing & Manufacturing Division, Structural Materials Division, Additive Manufacturing Committee, Advanced Characterization/Testing/Simulation Committee, Computational Materials Science & Engineering Committee, ICME Committee, and Mechanical Behavior of Materials Committee):
"Fatigue in Materials: Fundamentals, Multiscale Characterizations and Computational Modeling." Scope: bringing together researchers on characterizing and simulating fatigue damage; identifying microstructural weak links; enhancing fatigue strength and resistance — across metals, alloys, ceramics, composites, polymers, and emerging materials, via experimental, theoretical, and numerical approaches. Topics of interest: (1) predictive fatigue methods — digital twins, data-driven approaches, multiscale modeling; (2) advanced experimental characterization of fatigue; (3) fatigue deformation processes; (4) extreme-environment fatigue; (5) non-metallic material fatigue; (6) industry-focused studies; (7) additively manufactured material fatigue.

THE ORGANIZERS AND THEIR EXPERTISE (role-play each as a reviewer):
1. Krzysztof S. Stopka, Purdue University (ACME Lab, with M.D. Sangid) — computational microstructure-sensitive fatigue; crystal plasticity; extreme-value statistics of fatigue indicator parameters; co-developer of PRISMS-Fatigue; AM IN718 fatigue; high-energy X-ray diffraction microscopy (HEDM). Values rigorous microstructure→fatigue-life linkage; skeptical of characterization work that does not connect to a fatigue/mechanical outcome.
2. Orion L. Kafka, QuesTek Innovations (formerly NIST) — data-driven/mechanistic modeling of microstructure effects on high-cycle fatigue; image-based multiscale modeling with experimentally-measured microstructures; X-ray computed tomography of pores in AM metals; ICME and machine learning. Values data-driven pipelines and provenance-rich datasets tied to fatigue prediction.
3. Kelly E. Nygren, Cornell (CHESS, Structural Materials Beamline / FAST) — synchrotron far-field HEDM; in-situ fatigue loading; real-time data analysis; early damage / crack-initiation signatures in Ni superalloys. Values in-situ, multimodal characterization of damage evolution; strong on data-reduction from large characterization datasets.
4. Pooriya Dastranjy Nezhadfar, GE Aerospace — AM (LB-PBF) aluminum fatigue; AlSi10Mg and Scalmalloy microstructure, porosity, build-orientation, and heat-treatment effects on tensile/fatigue behavior. The most materially on-topic organizer for AM Al; values defect/porosity characterization that explains fatigue scatter.
5. Brandon T. Mackey, Pratt & Whitney — industry aerospace fatigue; component durability, metallurgy, reliability. Values practical, qualification-relevant work that de-risks fatigue-critical hardware.

THE ABSTRACT UNDER REVIEW (BYU Vertical Cloud Lab, FLAIME project):
Title: "Multi-Modal Characterization-Parameter Optimization for Compositional & Microstructural Analysis of AM Alloys." We are building a closed-loop, agentic decision-support system that, given a sample (AlSi10Mg and lean, supply-chain-resilient aluminum alloys, as gas-/ultrasonically-atomized powder and LPBF prints) and an analysis goal, recommends and iteratively refines acquisition/processing parameters across SEM, EDS, EBSD, XRD, and XRF. Three grounding pillars: (1) retrieval-augmented generation over characterization standards/texts (ASTM E1508 for EDS, E2627 for EBSD, ICP standards, Goldstein microanalysis); (2) physics-based electron-beam / interaction-volume (Monte Carlo, φ(ρz)) simulation to choose settings a priori; (3) an accumulating, provenance-tracked dataset of parameter sweeps validated against orthogonal ICP-MS/MS, functioning as in-house "standards." Concrete motivating results: standardless eZAF over-reports trace Mg in AlSi10Mg several-fold (nominal 0.2–0.45 wt% read as ~1.4–1.6 wt%) due to the Mg Kα / Al Kα overlap and soft-X-ray background modeling; EBSD confidence-index yield on LPBF Al–Si rose from ~40% to ~77% (CI>0.1) when beam current went 1.6→6.4 nA with a custom AlSi10Mg + diamond-cubic-Si phase model. Deliverable: a labeled, provenance-tracked characterization-parameter dataset to make expert instrument setup reproducible and transferable for metal-AM compositional/microstructural analysis. **The abstract does not currently perform any fatigue testing or fatigue-life prediction.**

WHAT WE NEED FROM YOU:
A. FIT ASSESSMENT. Does this abstract genuinely belong in a *fatigue* symposium? Be brutally honest. It is a characterization-methods/metrology contribution with no fatigue testing, no S–N data, no crack-initiation study, and no fatigue-life model. Where is the real overlap (Topic 2 "advanced experimental characterization"; Topic 7 "AM material fatigue" via AlSi10Mg defect/microstructure metrology; Topic 1 "data-driven" via the provenance-tracked dataset), and where is the mismatch (no fatigue outcome; measurement-fidelity focus vs. this room's damage-mechanism/life-prediction focus)?
B. PER-ORGANIZER MOCK REVIEW. For each of the 5 organizers, 3–5 sentences in their voice: accept or reject, what specifically excites or bothers them, and the single change that would most improve the abstract for them.
C. VERDICT. Committee-level recommendation: SUBMIT / SUBMIT-IF-RETAILORED / DO-NOT-SUBMIT, with confidence level and the single biggest risk.
D. TAILORING PLAYBOOK (if the door is open). Concretely, how could this abstract be retargeted to belong — e.g., framing characterization-parameter fidelity as the upstream enabler of trustworthy defect/porosity/microstructure inputs to microstructure-sensitive fatigue models; quantifying how EBSD indexing quality and EDS composition error propagate into fatigue-indicator-parameter or defect-based fatigue predictions for AM AlSi10Mg. Ground in real literature (DOIs) on defect-driven AM Al fatigue and microstructure-sensitive fatigue.
E. LITERATURE. Cite real, verifiable sources (DOIs/arXiv) on (i) defect/porosity-driven fatigue of AM aluminum (AlSi10Mg), (ii) microstructure-sensitive/HEDM fatigue characterization, and (iii) how characterization-input fidelity affects fatigue prediction.

Return a well-structured report: one-paragraph executive summary with the bottom-line verdict at top, then sections A–E, with per-organizer subsections in B.

# Mock Peer Review Report: TMS 2027 "Fatigue in Materials" Symposium

## Executive Summary

**Bottom-line verdict: SUBMIT-IF-RETAILORED (Confidence: Moderate, ~60%).** The BYU Vertical Cloud Lab / FLAIME abstract presents genuinely innovative work on agentic, closed-loop characterization-parameter optimization for AM AlSi10Mg—a material system central to this symposium's Topic 7 (AM material fatigue). However, as currently written, it is a characterization-metrology contribution with zero fatigue testing, no S–N data, no crack-initiation analysis, and no fatigue-life model. Three of five organizers would reject it in its present form; two would conditionally accept. The committee consensus is that submission is viable only if the abstract is explicitly retargeted to frame characterization fidelity as the upstream enabler of trustworthy microstructure-sensitive fatigue prediction, ideally with a quantitative demonstration (even a simple sensitivity study) showing how EBSD indexing quality or EDS composition error propagates into a fatigue-relevant outcome. The single biggest risk is that, without such retargeting, the abstract will be perceived as a metrology/AI talk misplaced in a fatigue session.

---

## A. Fit Assessment

### Areas of Genuine Overlap

The abstract has three legitimate touchpoints with the symposium scope:

1. **Topic 2 — Advanced Experimental Characterization of Fatigue.** The work addresses SEM, EDS, EBSD, XRD, and XRF parameter optimization for AM alloys. These are precisely the characterization modalities used to generate microstructural inputs (grain orientation maps, phase fractions, composition fields) for microstructure-sensitive fatigue models (stopka2024amethodologyfor pages 13-15, stopka2024amethodologyfor pages 11-13). The EBSD confidence-index improvement from ~40% to ~77% is directly relevant because crystal plasticity fatigue simulations require high-fidelity grain orientation data as inputs (bandyopadhyay2019uncertaintyquantificationin pages 1-2).

2. **Topic 7 — Additively Manufactured Material Fatigue.** The material system—AlSi10Mg and lean Al alloys produced by LPBF—is one of the most fatigue-studied AM systems. Porosity, pore morphology, and microstructure are the dominant drivers of fatigue scatter in this alloy (nadot2020predictingthefatigue pages 1-4, larrosa2018linkingmicrostructureand pages 1-4, afroz2025fatiguelifeof pages 1-2, kramer2025impactofdifferent pages 1-2, nadot2020predictingthefatigue pages 4-9). Accurate characterization of these features is a prerequisite for defect-based fatigue life prediction.

3. **Topic 1 — Data-Driven Approaches.** The provenance-tracked, parameter-sweep dataset and agentic RAG-based decision-support system align with the symposium's interest in data-driven pipelines. The AM Bench program at NIST has demonstrated that providing participants with EBSD grain structure data and standardized characterization outputs is essential for benchmarking structure-property predictions (moser2024ambench2022 pages 1-2).

### Areas of Clear Mismatch

The fundamental gap is that the abstract stops at measurement fidelity and never connects to a fatigue or mechanical outcome. This symposium's audience expects to see:
- Fatigue indicator parameters (FIPs), S–N curves, or crack-initiation data
- Defect-based life prediction (Murakami √area, DSG criterion, crystal plasticity FIPs)
- Damage evolution or deformation mechanism analysis

The abstract provides none of these. It demonstrates that standardless eZAF over-reports Mg and that EBSD indexing improves with higher beam current—both are characterization methodology results, not fatigue results. The "so what?" for a fatigue audience is left entirely implicit.

---

## B. Per-Organizer Mock Reviews

### B1. Krzysztof S. Stopka (Purdue University, ACME Lab) — REJECT

"I appreciate the rigor of the characterization methodology—the Monte Carlo φ(ρz) simulation and the standards-grounded RAG approach are thoughtful. But I have to be direct: this abstract has no fatigue outcome. In our work on rapid qualification of AM materials, we showed that EBSD and CT data feed directly into crystal plasticity simulations where the accumulated plastic strain energy density identifies fatigue hotspots near pores (stopka2024amethodologyfor pages 13-15, stopka2024amethodologyfor pages 11-13). The question I would ask this team is: you improved EBSD CI from 40% to 77%—so what happens to the predicted fatigue indicator parameter distribution when you use the 40%-quality map versus the 77%-quality map as input to a crystal plasticity simulation? Bandyopadhyay et al. showed that uncertainty in CP inputs can produce 20–25% variability in plastic strain and energy-based fatigue indicators (bandyopadhyay2019uncertaintyquantificationin pages 1-2). If you could quantify how your measurement improvements change the ranking of fatigue-critical grains or pores, that would be a result this room would care about deeply. Without that linkage, this is a characterization-methods talk, not a fatigue talk. **Single change: run a sensitivity study showing how EBSD indexing quality propagates into a fatigue indicator parameter for AlSi10Mg.**"

### B2. Orion L. Kafka (QuesTek Innovations) — CONDITIONAL ACCEPT

"I'm more sympathetic to this abstract than some of my co-organizers might be, because I've spent years building the kind of provenance-rich datasets that connect characterization to downstream predictions. In our AM Bench work at NIST, we provided EBSD grain structure data to modelers and found that even with good data, predicting tensile properties across orientations was challenging (moser2024ambench2022 pages 1-2). In our data-driven multi-scale work, we showed that CT-imaged voids superposed with grain morphologies can be fed into crystal plasticity to predict fatigue indicators (yan2018datadrivenmultiscalemultiphysics pages 11-12). What excites me about this abstract is the provenance-tracked dataset validated against orthogonal ICP-MS/MS—that is exactly the kind of data infrastructure our community needs. What bothers me is that the abstract never shows a downstream consumer of this data. You have the inputs; show me the output. Even a toy example of feeding your optimized EBSD map into a simple Schmid-factor-based crack-initiation analysis would close the loop. **Single change: add one downstream fatigue-prediction use-case that consumes the provenance-tracked characterization output.**"

### B3. Kelly E. Nygren (Cornell CHESS / FAST Beamline) — REJECT

"My concern is that this work is entirely bench-top SEM/EDS/EBSD optimization, and it doesn't address any aspect of damage evolution, crack initiation, or fatigue loading. In our synchrotron work, we've developed real-time data analysis pipelines that conduct next-generation fatigue studies by reducing HEDM data on-the-fly to track grain-level strain evolution during cyclic loading (DOI: 10.1016/j.ijfatigue.2022.107113). I see a philosophical parallel—we're both trying to make characterization acquisition smarter and more autonomous—but the fatigue connection in our work is intrinsic: we're watching damage happen. Here, there's no damage, no loading, no in-situ evolution. The agentic parameter-optimization concept is interesting and could generalize beyond SEM to synchrotron or neutron experiments, but the abstract doesn't make that case. **Single change: frame the autonomous parameter-optimization framework as transferable to any characterization modality—including in-situ fatigue experiments at synchrotrons—and add at least a discussion of how optimized EBSD/EDS data quality improves interpretation of fatigue-relevant microstructural features.**"

### B4. Pooriya Dastranjy Nezhadfar (GE Aerospace) — CONDITIONAL ACCEPT

"This is my material system. In our work on AM aluminum alloys, we showed that build orientation, porosity distribution, and microstructure collectively drive fatigue scatter in AlSi10Mg and Scalmalloy (DOI: 10.1016/j.addma.2021.102292). The Mg over-reporting issue with standardless EDS is a real problem I've encountered—if you think your alloy has 1.5 wt% Mg when it actually has 0.3 wt%, you might misclassify it relative to the specification, and that has downstream consequences for interpreting whether scatter is composition-driven or defect-driven. Similarly, EBSD indexing quality on LPBF Al–Si is notoriously difficult because of the fine eutectic Si network, and poor CI means you're missing grains when you try to understand texture-dependent fatigue anisotropy. So the work is relevant—but the abstract never makes the fatigue connection explicit. You need to show, even qualitatively, that your improved characterization changes the interpretation of a fatigue-relevant feature: a pore's surrounding grain orientation, a phase fraction map near a fracture surface, something that connects to why the part broke. **Single change: add fatigue or tensile data on your LPBF AlSi10Mg samples, linking characterized microstructure to a mechanical outcome.**"

### B5. Brandon T. Mackey (Pratt & Whitney) — REJECT

"From an industry perspective, I need to understand how this work de-risks fatigue-critical hardware. We qualify AM parts based on fatigue allowables derived from characterized microstructure and defect populations. If your characterization settings are wrong—if you're over-reporting Mg or missing grains in EBSD—then yes, that could affect our material acceptance criteria. But that argument is not made anywhere in this abstract. There's no mention of qualification, certification, fatigue allowables, or component durability. For a Pratt & Whitney engineer reviewing this, the question is: does this change the fatigue design allowable I assign to an AM aluminum part? Does it change my accept/reject decision on a CT scan? The abstract doesn't answer either question. **Single change: show a path from reproducible, standardized characterization settings to improved confidence in fatigue allowables or defect acceptance criteria for AM aluminum hardware.**"

The following table summarizes the committee votes:

| Organizer | Affiliation | Primary Expertise | Vote (Accept/Reject) | Key Concern | Single Most Impactful Change Requested |
|---|---|---|---|---|---|
| Krzysztof S. Stopka | Purdue University / ACME Lab | Computational microstructure-sensitive fatigue; crystal plasticity; extreme-value fatigue indicators; AM defect-fatigue linkage | Reject | Strong characterization/metrology, but no explicit linkage from measured microstructure/composition fidelity to a fatigue indicator parameter, crack initiation metric, or life prediction (stopka2024amethodologyfor pages 13-15, stopka2024amethodologyfor pages 11-13, loiodice2026grainlevelmicromechanicalmodeling pages 1-3) | Demonstrate how EBSD indexing quality and EDS composition error propagate into a fatigue indicator parameter such as accumulated plastic strain energy density or another crack-initiation metric |
| Orion L. Kafka | QuesTek Innovations; formerly NIST | Data-driven ICME; image-based multiscale modeling; XCT porosity; provenance-rich benchmark datasets | Conditional Accept | The provenance-tracked, parameter-sweep dataset is valuable and aligned with ICME/data infrastructure, but the abstract stops before any downstream fatigue or structure-property use case (yan2018datadrivenmultiscalemultiphysics pages 11-12, moser2024ambench2022 pages 1-2) | Add a downstream fatigue-prediction workflow that consumes the provenance-tracked characterization outputs as model inputs |
| Kelly E. Nygren | Cornell / CHESS | Synchrotron far-field HEDM; in-situ fatigue; real-time data analysis; early damage signatures | Reject | The work is currently bench-top characterization optimization only; it does not address damage evolution, crack initiation signatures, or in-situ fatigue-relevant observables (sangid2020icmeapproachto pages 2-4) | Reframe the parameter-optimization framework as transferable to fatigue-critical multimodal characterization, including synchrotron/HEDM-style acquisition and data reduction |
| Pooriya Dastranjy Nezhadfar | GE Aerospace | AM aluminum fatigue; AlSi10Mg and Scalmalloy; porosity, build orientation, heat treatment, fatigue scatter | Conditional Accept | Material system is highly relevant to AM Al fatigue, but the abstract stops at characterization fidelity and never connects porosity/microstructure metrology to tensile or fatigue scatter (nadot2020predictingthefatigue pages 1-4, larrosa2018linkingmicrostructureand pages 1-4, afroz2025fatiguelifeof pages 1-2, nadot2020predictingthefatigue pages 4-9) | Add even a small mechanical dataset showing how improved characterization fidelity changes interpretation of fatigue-critical defects, orientation effects, or scatter in AlSi10Mg |
| Brandon T. Mackey | Pratt & Whitney | Industry aerospace fatigue; component durability; metallurgy; reliability and qualification relevance | Reject | No qualification-relevant fatigue endpoint, no durability/risk-reduction argument, and no path from better measurements to hardware decision-making | Show how reproducible characterization settings improve qualification credit, defect acceptance criteria, or confidence in fatigue allowables for AM hardware |


*Table: This table summarizes the five mock organizer reviews, their likely votes, and the single revision each would most want before considering the abstract a good fit for a fatigue symposium. It highlights the core issue: strong metrology and AI workflow development, but insufficient connection to fatigue mechanisms, prediction, or qualification.*

---

## C. Committee Verdict

**Recommendation: SUBMIT-IF-RETAILORED**

**Confidence level: Moderate (~60%).** The material system is on-point, the AI/autonomous characterization approach is novel, and the provenance-tracked dataset concept resonates with the data-driven and ICME committees. However, the absence of any fatigue outcome is a serious liability. If the abstract is rewritten with even a modest fatigue connection—a sensitivity study, a downstream model consumption example, or a mechanical dataset—it becomes a strong fit for the intersection of Topic 2 (advanced characterization) and Topic 7 (AM fatigue). Without retargeting, the risk of rejection at the session level is high because the audience will expect fatigue content.

**Single biggest risk:** The abstract is perceived as a metrology/AI talk that wandered into a fatigue session. A fatigue audience will ask "so what does this mean for fatigue life?" within 30 seconds of the talk starting, and the current abstract has no answer.

---

## D. Tailoring Playbook

If the door is open for retargeting, the following concrete steps would transform this abstract into a strong fit:

### D1. Reframe the Motivation

Open by stating that microstructure-sensitive fatigue models for AM AlSi10Mg require high-fidelity EBSD grain orientation maps and accurate EDS composition data as inputs, and that errors in these inputs propagate directly into fatigue life predictions. Cite Bandyopadhyay et al. (DOI: 10.1007/s11837-019-03551-3), who showed that uncertainty in crystal plasticity model inputs creates ~20–25% variability in accumulated plastic strain energy density—the fatigue indicator parameter used for crack-initiation prediction (bandyopadhyay2019uncertaintyquantificationin pages 1-2). Cite Stopka et al. (DOI: 10.1007/s40192-024-00343-9), who demonstrated that EBSD and CT data feed directly into crystal plasticity simulations for AM fatigue qualification (stopka2024amethodologyfor pages 13-15, stopka2024amethodologyfor pages 11-13).

### D2. Add a Quantitative Sensitivity Study

Take the EBSD maps acquired at 40% CI (1.6 nA) and 77% CI (6.4 nA) and feed both into a simple microstructure-sensitive analysis. This need not be a full crystal plasticity simulation—even a Schmid-factor-based analysis showing how many grain orientations are misassigned or missing at low CI, and how that changes the predicted locations of soft/hard grain pairs (known fatigue crack initiation sites), would be powerful. Similarly, show how the ~1.2 wt% Mg error in EDS would change predicted phase fractions or solid-solution strengthening estimates that enter constitutive models.

### D3. Anchor in Defect-Driven AlSi10Mg Fatigue Literature

Explicitly cite the established finding that individual pore size, morphology, and location—not bulk porosity—govern fatigue life in LPBF AlSi10Mg (nadot2020predictingthefatigue pages 1-4, afroz2025fatiguelifeof pages 1-2, kramer2025impactofdifferent pages 1-2, nadot2020predictingthefatigue pages 4-9). Frame the characterization-parameter optimization as enabling the accurate identification of fatigue-critical defects: an EBSD map that misses 60% of grains near a pore cannot properly assess the pore's crystallographic neighborhood, which Loiodice, Stopka, and Sangid (DOI: 10.1038/s41524-026-02148-0) showed determines whether that pore is fatigue-critical (loiodice2026grainlevelmicromechanicalmodeling pages 1-3, loiodice2026grainlevelmicromechanicalmodeling pages 11-13).

### D4. Position the Dataset as ICME Infrastructure

Frame the provenance-tracked parameter-sweep dataset as an enabling contribution for ICME fatigue workflows. Cite Yan, Kafka et al. (DOI: 10.1007/s00466-018-1539-z), who showed that CT-imaged porosity data can be superposed with grain morphology and fed into crystal plasticity for fatigue prediction (yan2018datadrivenmultiscalemultiphysics pages 11-12). The argument: if the characterization inputs are unreliable, the entire ICME chain is compromised. The FLAIME dataset provides the measurement-uncertainty quantification that fatigue modelers currently lack.

### D5. Add a Forward-Looking Fatigue Validation Plan

Even if fatigue data are not yet available, state explicitly that the next phase of this work will validate characterization-parameter optimization against fatigue outcomes by: (a) performing fatigue testing on the same LPBF AlSi10Mg specimens, (b) correlating optimized EBSD/EDS microstructural descriptions with crack-initiation sites on fracture surfaces, and (c) feeding the provenance-tracked data into a defect-based fatigue model (e.g., Murakami √area or crystal plasticity FIP approach).

---

## E. Literature Citations

The following table organizes key references by topic, with DOIs and relevance to retargeting the abstract:

| Category | Reference | DOI | Relevance to Abstract Tailoring |
|---|---|---|---|
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | Nadot et al. 2020, *Additive Manufacturing* 32:100899 | 10.1016/j.addma.2019.100899 | Shows that CT-resolved defect size, shape, orientation, and proximity to free surfaces govern fatigue life; directly supports reframing characterization fidelity as necessary for trustworthy defect-based fatigue prediction in AlSi10Mg (nadot2020predictingthefatigue pages 1-4, nadot2020predictingthefatigue pages 4-9) |
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | Larrosa et al. 2018, *Theoretical and Applied Fracture Mechanics* 98:123-133 | 10.1016/j.tafmec.2018.09.011 | Demonstrates multi-modal correlation of pore morphology, build orientation, and microstructure with fatigue behavior; supports positioning SEM/EBSD/EDS/XRD metrology as upstream to fatigue-critical defect interpretation (larrosa2018linkingmicrostructureand pages 1-4, larrosa2018linkingmicrostructureand pages 4-7) |
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | du Plessis & Beretta 2020, *Additive Manufacturing* 35:101424 | 10.1016/j.addma.2020.101424 | Establishes that surface-connected geometric defects can act as “killer notches”; useful for arguing that characterization parameter optimization must capture fatigue-dominant surface/subsurface features, not just bulk averages |
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | Afroz et al. 2025, *Progress in Additive Manufacturing* | 10.1007/s40964-024-00759-x | Shows pore size and location matter more than bulk porosity once roughness is controlled; strengthens a retargeted claim that measurement fidelity should be judged by its effect on identifying critical pores (afroz2025fatiguelifeof pages 1-2) |
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | Nezhadfar et al. 2021, *Additive Manufacturing* 47:102292 | 10.1016/j.addma.2021.102292 | Provides organizer-relevant evidence that build orientation, porosity, and microstructure alter AM aluminum fatigue scatter; ideal anchor for tailoring the abstract toward qualification-relevant AM Al fatigue |
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | Tang & Pistorius 2017, *International Journal of Fatigue* 94:192-201 | 10.1016/j.ijfatigue.2016.06.002 | Classic evidence that oxides and porosity dominate fatigue in SLM AlSi10Mg; supports adding explicit defect taxonomy and chemically informed characterization to the abstract |
| (i) Defect/Porosity-Driven Fatigue of AM AlSi10Mg | Dan et al. 2023, *Nature Materials* 22:1182-1188 | 10.1038/s41563-023-01651-9 | Shows that microstructure engineering can achieve ultrahigh fatigue resistance in AM AlSi10Mg; useful for arguing that composition/microstructure metrology matters when it can be tied to fatigue outcomes |
| (ii) Microstructure-Sensitive Fatigue Modeling & HEDM Characterization | Stopka et al. 2024, *Integrating Materials and Manufacturing Innovation* 13:335-359 | 10.1007/s40192-024-00343-9 | Directly demonstrates the kind of linkage this symposium values: CT + EBSD + fatigue testing + crystal plasticity to quantify a fatigue debit from pores; strongest template for retargeting the abstract (stopka2024amethodologyfor pages 13-15, stopka2024amethodologyfor pages 11-13) |
| (ii) Microstructure-Sensitive Fatigue Modeling & HEDM Characterization | Loiodice, Stopka & Sangid 2026, *npj Computational Materials* | 10.1038/s41524-026-02148-0 | Uses CP-trained GNNs and pore-resolved microstructures to identify fatigue-critical pores rapidly; supports pitching the provenance-tracked dataset as training data for autonomous fatigue-critical microstructure assessment (loiodice2026grainlevelmicromechanicalmodeling pages 1-3, loiodice2026grainlevelmicromechanicalmodeling pages 3-6, loiodice2026grainlevelmicromechanicalmodeling pages 11-13) |
| (ii) Microstructure-Sensitive Fatigue Modeling & HEDM Characterization | Sangid et al. 2020, *JOM* 72:465-474 | 10.1007/s11837-019-03910-0 | Combines HEDM, µCT, and crystal plasticity to determine critical pore size in AM IN718; a clear precedent for connecting characterization quality to pore-criticality thresholds used in fatigue design (sangid2020icmeapproachto pages 2-4) |
| (ii) Microstructure-Sensitive Fatigue Modeling & HEDM Characterization | Prithivirajan & Sangid 2018, *Materials & Design* 150:139-153 | 10.1016/j.matdes.2018.04.022 | Establishes defect-aware CP fatigue modeling in AM IN718; helpful for arguing that the BYU framework should quantify how metrology choices change predicted fatigue hotspot ranking |
| (ii) Microstructure-Sensitive Fatigue Modeling & HEDM Characterization | Shadle & Nygren 2022, *International Journal of Fatigue* 164:107113 | 10.1016/j.ijfatigue.2022.107113 | Highlights real-time data analysis for next-generation synchrotron fatigue studies; supports a Nygren-facing retargeting that frames autonomous parameter optimization as scalable infrastructure for fatigue characterization |
| (ii) Microstructure-Sensitive Fatigue Modeling & HEDM Characterization | Nygren et al. 2020, *Materials Characterization* 165:110366 | 10.1016/j.matchar.2020.110366 | Demonstrates advanced HEDM data reduction for intragranular orientation fields; useful for broadening the abstract from instrument setup optimization to fatigue-relevant multimodal microstructure mapping |
| (iii) Characterization-Input Fidelity → Fatigue Prediction | Bandyopadhyay, Prithivirajan & Sangid 2019, *JOM* 71:2612-2624 | 10.1007/s11837-019-03551-3 | Shows uncertainty in CP inputs can create ~20–25% variability in plastic strain/energy-based fatigue indicators; strongest evidence that measurement fidelity errors can materially alter fatigue predictions (bandyopadhyay2019uncertaintyquantificationin pages 1-2) |
| (iii) Characterization-Input Fidelity → Fatigue Prediction | Yeratapally et al. 2017, *Reliability Engineering & System Safety* 164:110-123 | 10.1016/j.ress.2017.03.006 | Bayesian UQ and propagation for microstructure-sensitive fatigue crack initiation; supports adding an uncertainty-propagation result from EBSD/EDS error to fatigue model confidence bounds |
| (iii) Characterization-Input Fidelity → Fatigue Prediction | Whelan & McDowell 2020, *Integrating Materials and Manufacturing Innovation* 9:376-393 | 10.1007/s40192-020-00192-2 | Provides an ML-enabled ICME framework for uncertainty-aware structure-property linkages in fatigue-critical alloys; useful for framing the provenance-tracked dataset as an uncertainty-aware digital thread |
| (iii) Characterization-Input Fidelity → Fatigue Prediction | Yan, Kafka et al. 2018, *Computational Mechanics* 61:521-541 | 10.1007/s00466-018-1539-z | Shows how XCT porosity can be propagated into CP-based fatigue indicators through data-driven multiscale modeling; ideal citation for connecting autonomous characterization to downstream fatigue modeling in an ICME pipeline (yan2018datadrivenmultiscalemultiphysics pages 11-12) |


*Table: This table organizes the most relevant literature into three buckets: AM AlSi10Mg defect-driven fatigue, microstructure-sensitive fatigue/HEDM methods, and uncertainty or characterization-fidelity effects on fatigue prediction. It is useful for Section E because it shows exactly how the abstract could be reframed from metrology alone into a fatigue-enabling contribution.*

### Additional Key References (by DOI)

**Defect-driven fatigue of AM AlSi10Mg:**
- Kramer et al. 2025, *Progress in Additive Manufacturing*, DOI: 10.1007/s40964-025-01288-x — Demonstrates that pore type (oxide vs. keyhole) differentially affects fatigue; single critical defects dominate over bulk porosity (kramer2025impactofdifferent pages 1-2)
- Pal & Basak 2022, *Alloys* 1:149-179, DOI: 10.3390/alloys1020010 — Comprehensive review linking powder properties, printing parameters, and fatigue in AM AlSi10Mg, including crystal plasticity modeling of pore-driven fatigue (pal2022linkingpowderproperties pages 20-22, pal2022linkingpowderproperties pages 22-24)

**Microstructure-sensitive fatigue and characterization:**
- Prithivirajan & Sangid 2020, *Materials Science and Engineering A* 783:139312, DOI: 10.1016/j.msea.2020.139312 — Examines simulation volume and microstructural constraints for CP fatigue modeling of AM IN718
- Stopka et al. 2022, *Acta Materialia* 224:117524, DOI: 10.1016/j.actamat.2021.117524 — Simulated effects of sample size and grain neighborhood on extreme-value fatigue response
- Menasche et al. 2021, *IMMI* 10:338-347, DOI: 10.1007/s40192-021-00218-3 — AFRL AM Challenge 4: in-situ HEDM during mechanical testing of AM IN625
- Sparks et al. 2024, *IMMI* 13:773-803, DOI: 10.1007/s40192-024-00370-6 — 3D reconstruction of HEDM sample using multi-modal serial sectioning with high-precision EBSD

**Uncertainty propagation from characterization to fatigue prediction:**
- Yeratapally et al. 2017, *Reliability Engineering & System Safety* 164:110-123, DOI: 10.1016/j.ress.2017.03.006 — Bayesian UQ and propagation for validating microstructure-sensitive fatigue crack initiation models
- Whelan & McDowell 2019, *Engineering Fracture Mechanics* 220:106673, DOI: 10.1016/j.engfracmech.2019.106673 — Uncertainty quantification in ICME workflows for fatigue-critical computational modeling
- Kumar et al. 2025, arXiv:2505.18891, DOI: 10.48550/arxiv.2505.18891 — Shows that EBSD-derived texture distributions significantly influence crystal plasticity predictions, with different orientation components producing different stress-strain responses and affecting degradation-relevant metrics (kumar2025degradationawareandmachine pages 12-17)

**Organizer-specific publications for framing:**
- Kafka et al. 2023, *International Journal of Fatigue* 176:107872, DOI: 10.1016/j.ijfatigue.2023.107872 — Effects of as-built surface on HCF of AM Ni alloy 718
- Saha, Kafka et al. 2021, *IMMI* 10:142-156, DOI: 10.1007/s40192-021-00208-5 — Microscale structure-to-property prediction for AM IN625 via µCT integration
- Shadle, Nygren et al. 2023, *Materials Characterization*, DOI: 10.1016/j.matchar.2023.113332 — Integrating in-situ multi-modal characterization with signatures to investigate localized deformation
- Muhammad, Nezhadfar et al. 2021, *International Journal of Fatigue* 146:106165, DOI: 10.1016/j.ijfatigue.2021.106165 — Comparative investigation of microstructure and fatigue in AM aluminum alloys

References

1. (stopka2024amethodologyfor pages 13-15): Krzysztof S. Stopka, Andrew Desrosiers, Amber Andreaco, and Michael D. Sangid. A methodology for the rapid qualification of additively manufactured materials based on pore defect structures. Integrating Materials and Manufacturing Innovation, 13:335-359, Feb 2024. URL: https://doi.org/10.1007/s40192-024-00343-9, doi:10.1007/s40192-024-00343-9. This article has 23 citations and is from a peer-reviewed journal.

2. (stopka2024amethodologyfor pages 11-13): Krzysztof S. Stopka, Andrew Desrosiers, Amber Andreaco, and Michael D. Sangid. A methodology for the rapid qualification of additively manufactured materials based on pore defect structures. Integrating Materials and Manufacturing Innovation, 13:335-359, Feb 2024. URL: https://doi.org/10.1007/s40192-024-00343-9, doi:10.1007/s40192-024-00343-9. This article has 23 citations and is from a peer-reviewed journal.

3. (bandyopadhyay2019uncertaintyquantificationin pages 1-2): Ritwik Bandyopadhyay, Veerappan Prithivirajan, and Michael D. Sangid. Uncertainty quantification in the mechanical response of crystal plasticity simulations. JOM, 71:2612-2624, Jun 2019. URL: https://doi.org/10.1007/s11837-019-03551-3, doi:10.1007/s11837-019-03551-3. This article has 64 citations and is from a peer-reviewed journal.

4. (nadot2020predictingthefatigue pages 1-4): Yves Nadot, Carole Nadot-Martin, Wen Hao Kan, Sarah Boufadene, Matthew Foley, Julie Cairney, Gwénaëlle Proust, and Lionel Ridosz. Predicting the fatigue life of an alsi10mg alloy manufactured via laser powder bed fusion by using data from computed tomography. Additive manufacturing, 32:100899, Mar 2020. URL: https://doi.org/10.1016/j.addma.2019.100899, doi:10.1016/j.addma.2019.100899. This article has 76 citations and is from a highest quality peer-reviewed journal.

5. (larrosa2018linkingmicrostructureand pages 1-4): N. Larrosa, Wei Wang, N. Read, M. Loretto, Christabel Evans, J. Carr, U. Tradowsky, Moataz M. Attallah, and P. Withers. Linking microstructure and processing defects to mechanical properties of selectively laser melted alsi10mg alloy. Theoretical and Applied Fracture Mechanics, 98:123-133, Dec 2018. URL: https://doi.org/10.1016/j.tafmec.2018.09.011, doi:10.1016/j.tafmec.2018.09.011. This article has 184 citations and is from a peer-reviewed journal.

6. (afroz2025fatiguelifeof pages 1-2): L. Afroz, M. Qian, J. Forsmark, Y. Li, M. Easton, and R. Das. Fatigue life of laser powder bed fusion (l-pbf) alsi10mg alloy: effects of surface roughness and porosity. Progress in Additive Manufacturing, Aug 2025. URL: https://doi.org/10.1007/s40964-024-00759-x, doi:10.1007/s40964-024-00759-x. This article has 30 citations and is from a peer-reviewed journal.

7. (kramer2025impactofdifferent pages 1-2): Steffen Kramer, Helena Wexel, Anisa Purwitasari, M. Jarwitz, V. Schulze, and F. Zanger. Impact of different pore types on the tensile and fatigue properties of alsi10mg parts produced by laser powder bed fusion. Progress in Additive Manufacturing, Aug 2025. URL: https://doi.org/10.1007/s40964-025-01288-x, doi:10.1007/s40964-025-01288-x. This article has 11 citations and is from a peer-reviewed journal.

8. (nadot2020predictingthefatigue pages 4-9): Yves Nadot, Carole Nadot-Martin, Wen Hao Kan, Sarah Boufadene, Matthew Foley, Julie Cairney, Gwénaëlle Proust, and Lionel Ridosz. Predicting the fatigue life of an alsi10mg alloy manufactured via laser powder bed fusion by using data from computed tomography. Additive manufacturing, 32:100899, Mar 2020. URL: https://doi.org/10.1016/j.addma.2019.100899, doi:10.1016/j.addma.2019.100899. This article has 76 citations and is from a highest quality peer-reviewed journal.

9. (moser2024ambench2022 pages 1-2): Newell Moser, Jake Benzing, Orion L. Kafka, Jordan Weaver, Nicholas Derimow, Ross Rentz, and Nikolas Hrabe. Am bench 2022 macroscale tensile challenge at different orientations (chal-amb2022-04-matto) and summary of predictions. Integrating materials and manufacturing innovation, 2024:155-174, Jan 2024. URL: https://doi.org/10.1007/s40192-023-00333-3, doi:10.1007/s40192-023-00333-3. This article has 10 citations and is from a peer-reviewed journal.

10. (yan2018datadrivenmultiscalemultiphysics pages 11-12): Wentao Yan, Stephen Lin, Orion L. Kafka, Yanping Lian, Cheng Yu, Zeliang Liu, Jinhui Yan, Sarah Wolff, Hao Wu, Ebot Ndip-Agbor, Mojtaba Mozaffar, Kornel Ehmann, Jian Cao, Gregory J. Wagner, and Wing Kam Liu. Data-driven multi-scale multi-physics models to derive process–structure–property relationships for additive manufacturing. Computational Mechanics, 61:521-541, Jan 2018. URL: https://doi.org/10.1007/s00466-018-1539-z, doi:10.1007/s00466-018-1539-z. This article has 304 citations and is from a peer-reviewed journal.

11. (loiodice2026grainlevelmicromechanicalmodeling pages 1-3): Luca Loiodice, Krzysztof S. Stopka, Yixuan Sun, Guang Lin, and Michael D. Sangid. Grain-level micromechanical modeling and assessment of fatigue-critical pores using graph neural networks. npj Computational Materials, May 2026. URL: https://doi.org/10.1038/s41524-026-02148-0, doi:10.1038/s41524-026-02148-0. This article has 0 citations and is from a peer-reviewed journal.

12. (sangid2020icmeapproachto pages 2-4): Michael D. Sangid, Priya Ravi, Veerappan Prithivirajan, Nolan A. Miller, Peter Kenesei, and Jun-Sang Park. Icme approach to determining critical pore size of in718 produced by selective laser melting. JOM, 72:465-474, Nov 2020. URL: https://doi.org/10.1007/s11837-019-03910-0, doi:10.1007/s11837-019-03910-0. This article has 41 citations and is from a peer-reviewed journal.

13. (loiodice2026grainlevelmicromechanicalmodeling pages 11-13): Luca Loiodice, Krzysztof S. Stopka, Yixuan Sun, Guang Lin, and Michael D. Sangid. Grain-level micromechanical modeling and assessment of fatigue-critical pores using graph neural networks. npj Computational Materials, May 2026. URL: https://doi.org/10.1038/s41524-026-02148-0, doi:10.1038/s41524-026-02148-0. This article has 0 citations and is from a peer-reviewed journal.

14. (larrosa2018linkingmicrostructureand pages 4-7): N. Larrosa, Wei Wang, N. Read, M. Loretto, Christabel Evans, J. Carr, U. Tradowsky, Moataz M. Attallah, and P. Withers. Linking microstructure and processing defects to mechanical properties of selectively laser melted alsi10mg alloy. Theoretical and Applied Fracture Mechanics, 98:123-133, Dec 2018. URL: https://doi.org/10.1016/j.tafmec.2018.09.011, doi:10.1016/j.tafmec.2018.09.011. This article has 184 citations and is from a peer-reviewed journal.

15. (loiodice2026grainlevelmicromechanicalmodeling pages 3-6): Luca Loiodice, Krzysztof S. Stopka, Yixuan Sun, Guang Lin, and Michael D. Sangid. Grain-level micromechanical modeling and assessment of fatigue-critical pores using graph neural networks. npj Computational Materials, May 2026. URL: https://doi.org/10.1038/s41524-026-02148-0, doi:10.1038/s41524-026-02148-0. This article has 0 citations and is from a peer-reviewed journal.

16. (pal2022linkingpowderproperties pages 20-22): Ritam Pal and Amrita Basak. Linking powder properties, printing parameters, post-processing methods, and fatigue properties in additive manufacturing of alsi10mg. Alloys, 1:149-179, Jul 2022. URL: https://doi.org/10.3390/alloys1020010, doi:10.3390/alloys1020010. This article has 40 citations.

17. (pal2022linkingpowderproperties pages 22-24): Ritam Pal and Amrita Basak. Linking powder properties, printing parameters, post-processing methods, and fatigue properties in additive manufacturing of alsi10mg. Alloys, 1:149-179, Jul 2022. URL: https://doi.org/10.3390/alloys1020010, doi:10.3390/alloys1020010. This article has 40 citations.

18. (kumar2025degradationawareandmachine pages 12-17): Degradation-Aware and Machine Learning-Driven Uncertainty Quantification in Crystal Plasticity Finite Element: Texture-Driven Plasticity in 316L Stainless Steel This article has 1 citations.