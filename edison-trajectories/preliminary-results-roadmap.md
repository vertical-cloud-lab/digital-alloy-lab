# Preliminary Results Roadmap for FLAIME Genesis Mission Phase I Proposal

*Assessment of what preliminary results to collect by April 28, 2026*

## Overview

This document synthesizes input from three Edison Scientific queries — (1) mock PO/reviewer panel feedback, (2) asset readiness assessment, and (3) experimental capability evidence assessment — combined with the existing body of work across 17+ open PRs and the DOE Genesis Mission (DE-FOA-0003612) **Topic 3B (Critical Minerals and Materials — AI-Enabled Materials Discovery, AMMTO)** requirements. It identifies the highest-impact preliminary results to generate in the 19 days before the April 28 deadline, specifying exactly what would appear in the proposal: figures, figure captions, tables, and narrative text placement. Four rounds of Edison mock review informed this roadmap: two rounds (tasks `567c7816`, `97b09434`) refined structure and content, a third round (task `1e791f42`, score 7.0/10) incorporated after the comprehensive partnership and evidence update, and a fourth round (task `a039dc08`, score 8.0/10) harmonized figure numbering and reconciled cross-references.

> **Terminology note**: FLAIME uses **Bayesian Optimization over Function Networks (BOFN)** as the decision-making framework, with the **partial Knowledge Gradient for Function Networks (pKGFN)** as the primary acquisition function. In this document, "pKGFN" refers to the specific acquisition function implementation, while "BOFN" refers to the broader framework. Both are used throughout; they are not interchangeable but are complementary.

### Partnership Structure

**Letters of Collaboration (formal team members):**
- **Valimet** (Stockton, CA) — gas atomization service contract for Phase I scale-up powders
- **AMAZEMET** (Warsaw, Poland) — ultrasonic atomization equipment and rePOWDER service; returning atomized powder batches with controlled composition adjustments
- **Thermo-Calc** (McMurray, PA / Stockholm) — CALPHAD screening via TC-Python/TCAl10 and AM Module simulations; providing sample AM Module calculations and advisory support

**Letters of Support:**
- **Ames National Laboratory** — CMI Hub expertise, Phase II GARS pathway
- **Fehrmann Alloys** — feedstock validation and alloy supply chain
- **Taylor Sparks** (University of Utah) — LPBF printing capability; printed AlSi10Mg tensile specimens for baseline characterization
- **Ashley Speer** — characterization and materials science expertise
- **Adam Clare** (University of British Columbia / University of Nottingham, FREng) — additive manufacturing process expertise
- **Chris Stiles** (JHU/APL connection) — AM process engineering
- **Jae Hattrick-Simpers** — autonomous experimentation and SDL methodology
- **Keith Brown** (Boston University) — SDL validation and Bayesian optimization expertise

### Phase I Target Alloy System

**Phase I will focus on Al alloys processed by LPBF, targeting critical-mineral-lean compositions in the Al-Zr and Al-Mn-Cr-Zr families.** The primary objective is to discover and qualify printable Al alloys that eliminate dependence on critical minerals (Mg, Sc, REE) commonly used in high-performance Al-alloy feedstocks. AlSi10Mg serves as the baseline for benchmarking and initial BOFN validation because it is the most commercially mature and data-rich LPBF aluminum alloy — baseline tensile specimens have been printed at the University of Utah and by 3D Powder Tech, with tensile data collected. Novel compositions explored via CALPHAD-guided search will target the Al-Zr-X and Al-Mn-Cr-Zr spaces, where Zr provides grain refinement and Mn/Cr contribute corrosion resistance and strength. While Mn, Cr, and Zr appear on the 2022 USGS Critical Minerals List, they generally carry lower supply-chain risk than Sc and REE — which often exhibit high single-nation supply concentration (USGS, *2022 Final List of Critical Minerals*, 87 FR 10381) — and are typically used at lower concentrations than many Mg-based or Sc-bearing alloy formulations. FLAIME's mineral-burden objective uses a weighted criticality index that accounts for both supply-risk severity and required mass fraction, enabling the optimizer to quantitatively minimize aggregate critical mineral exposure rather than treating all listed minerals as equivalent. **Cu-Cr-Zr alloys are a secondary complement (~20% Phase I effort)** for Be-Cu replacement in high-conductivity applications, demonstrating platform generality. This alloy strategy aligns with AMMTO's Critical Minerals Strategy (CMS) Pillars 2 (Secure and Diversify Supply) and 5 (Invest in Workforce and Innovation), and with collaborator capabilities (U of Utah LPBF printing, Thermo-Calc CALPHAD/AM Module, AMAZEMET ultrasonic atomization, Valimet gas atomization) and available CALPHAD databases (TCAl10, Scheil-Gulliver solidification modeling on BYU HPC).

### Proposal Narrative Arc

The proposal argues that **autonomous, cost-aware closed-loop experimentation can substantially accelerate the discovery and qualification of critical-mineral-lean LPBF alloys, reducing dependence on supply-chain-vulnerable elements (Mg, Sc, REE) in structural aluminum applications**. The evidence chain is: (1) BOFN selects experiments that maximize information per dollar across a multi-stage workflow → (2) CALPHAD-informed constraints prevent exploration of unprintable compositions and enforce mineral-efficiency objectives → (3) stage-gated characterization (SEM, EDS, tensile) provides the physical ground truth that updates the surrogate → (4) the loop closes when qualification-relevant properties meet targets with minimal critical mineral content. The key differentiator is cost-aware multi-fidelity optimization over the full powder-to-property chain (not just process parameters) with an explicit mineral-burden objective. The Phase I deliverable is a validated closed-loop framework demonstrated on Al alloys with real experimental data, producing a shortlist of critical-mineral-lean compositions ready for Phase II scale-up. Preliminary results already in hand include: baseline AlSi10Mg tensile data from University of Utah and 3D Powder Tech printed specimens, SEM/EDS characterization of precursor powders and AMAZEMET-atomized powder, high-temperature tensile data on a standard aluminum specimen, Thermo-Calc AM Module simulations, CALPHAD screening runs on BYU HPC, a full pKGFN (partial Knowledge Gradient for Function Networks) pipeline implementation, and a demonstration of automated powder dispensing. *(ACTION ITEM: Insert quantified acceleration factor (X× fewer experiments, Y× lower cost vs. EI/random baselines) from closed-loop demo. Target: Day 9. Owner: Computational lead. If demo incomplete, state 'projected' with confidence interval.)*

### Page Budget Strategy

DOE Genesis Mission Phase I Project Narrative is capped at **5 pages** (§IV.C). Figures and tables count against this limit. Appendices (Facilities, Equipment, etc.) do not count. Preliminary results must be impactful but extremely concise — every figure and sentence must earn its space.

| Proposal Section | Target Pages | Max Figures/Tables |
|---|:---:|:---:|
| Background/Intro | ~1.0 | 1 figure |
| Project Objectives | ~0.5 | — |
| Proposed Research/Methods | ~1.5 | 1 figure |
| Milestones | ~1.0 | 1 table |
| Data Sources/Models | ~0.5 | — |
| Decision Gate Metrics | ~0.5 | 1 table |
| **Total (narrative)** | **5.0** | **~4 figures/tables** |
| *Appendix 2: Facilities (≤0.5p)* | *0.5* | *1 figure (atomizer)* |
| *Appendix 3: Equipment (≤0.5p)* | *0.5* | *1 table* |

Given the 5-page limit, preliminary results must be woven into Background/Intro and Research/Methods sections rather than occupying a dedicated section. The figure triage below identifies which evidence items to include in the narrative vs. appendices.

### Figure Triage for Preliminary Results (within 5-page narrative)

Given the extremely tight 5-page narrative limit, a maximum of 3 figures and 1 table fit in the narrative itself (~1.5 pages). The remaining experimental evidence is described in text with quantitative metrics, and supporting images go to Appendices (Facilities, Equipment).

| Figure # | Content | Proposal Section | Size |
|---|---|---|---|
| **Fig. 1** | Closed-loop pKGFN pipeline schematic + convergence plot | Research/Methods | Full-width, ~0.5 page |
| **Fig. 2** | Combined CALPHAD screening funnel + SEM/EDS multi-panel (2×3 compact) | Background/Prelim Results | Full-width, ~0.5 page |
| **Fig. 3** | Tensile data summary (stress–strain + YS/UTS/elongation bar chart) | Research/Methods | Half-width, ~0.25 page |
| **Table 1** | KPI/go-no-go dashboard (5 KPIs, triggered actions) | Milestones | Full-width, ~0.25 page |

**Moved to Appendices:** BOFN ablation (reference in text, full figure in supplementary); atomizer photo → Facilities appendix; detailed EDS maps → Facilities/Equipment appendix.
**Described in text only:** Real-data benchmark results (report MAE and cost-to-target numbers inline); automated powder dispensing (one sentence + metric); high-T tensile (report numbers in text alongside ambient tensile figure).

### Existing Assets (already completed across PRs)

| Asset | Source PR | Status | Proposal Use |
|---|---|---|---|
| BOFN 4-node/9-node verified implementations | #14 | ✅ Complete | Preliminary Results; Technical Approach |
| Full pKGFN (partial Knowledge Gradient for Function Networks) pipeline | #14 | ✅ Complete | Preliminary Results (lead computational result) |
| LLM-warmstart POC (LLAMBO-style) | #14 | ✅ Complete | Preliminary Results (supporting) |
| LPBF parameter space visualization (8/10) | #20 | ✅ Complete | Background; Technical Approach |
| AM test structure schematics (A-grade) | #30 | ✅ Complete | Technical Approach—Characterization |
| 5 headline KPIs + 8 go/no-go gates + 18 metrics | #26, #34 | ✅ Complete | Objectives; Milestones |
| LaTeX proposal template (DOE-compliant, 5-page narrative) | #38 | ✅ Complete | Submission vehicle |
| Phase I budget ($600K–$750K, 2 scenarios) | #26 | ✅ Complete | Budget Justification |
| Topic fit analysis (3B primary) | #26, #28 | ✅ Complete | Background; framing guidance |
| Project naming (FLAIME selected) | #28 | ✅ Complete | Throughout proposal |
| Edison-refined figures (multiple) | #14, #20, #30 | ✅ Complete | Multiple sections |
| Ultrasonic atomizer installed in lab | — | ✅ Complete | Facilities/Equipment; Preliminary Results |
| AlSi10Mg tensile specimen (U of Utah LPBF) + tensile data | — | ✅ Complete | Preliminary Results (baseline property endpoint) |
| AlSi10Mg tensile specimen (3D Powder Tech) | — | ✅ Complete | Preliminary Results (second baseline source) |
| SEM/EDS of precursor powders (AlSi10Mg, Si powder) | — | ✅ Complete | Preliminary Results (input QC evidence) |
| SEM/EDS of AMAZEMET-atomized mixture | — | ✅ Complete | Preliminary Results (synthesis QC evidence) |
| High-temperature tensile data (standard Al specimen) | — | ✅ Complete | Preliminary Results (elevated-T capability) |
| Thermo-Calc AM Module simulations (provided by TC) | — | ✅ Complete | Preliminary Results; Technical Approach |
| Thermo-Calc CALPHAD simulations on BYU HPC | — | ✅ Complete | Preliminary Results; Technical Approach |
| Automated powder dispensing demonstration | — | ✅ Complete | Preliminary Results (workflow automation) |

---

## Asset Readiness Assessment

*See Edison provenance log at end of document for query details.*

Key reviewer-facing interpretation: The BOFN synthetic MAE and cost-savings are *necessary but not sufficient*. Without a real-data benchmark and at least one closed-loop pilot, they will be perceived as algorithm development decoupled from LPBF reality. The test-structure/validation schematic and parameter-space structuring are already strong because they signal execution readiness and digital-thread thinking. The LLM warmstart is the highest-risk preliminary result: unless it demonstrates it does *not* collapse exploration into known-alloy neighborhoods, reviewers may interpret it as novelty-harming.

### Asset-by-Asset Proposal Readiness

| Asset | Recommendation | Readiness (1–10) | Key Upgrade Needed |
|---|---|:---:|---|
| BOFN DAG (4-node/9-node) | **Include, Improve heavily** | 6 | Re-run on real LPBF data; add ablation vs. standard GP/BO; quantify sample efficiency + cost savings under realistic fidelity costs; add constraint handling for printability/defects |
| Full pKGFN pipeline | **Include as lead computational result** | 8 | Connect to real data from U of Utah tensile + AMAZEMET powder; demonstrate cost-aware acquisition on realistic alloy/LPBF surrogate; show mineral-burden objective integration |
| LLM warmstart POC | **Mention briefly, demote to supporting** | 4 | Benchmark against random/LHS/expert-seeded starts; measure novelty/diversity; add metallurgical filter; show warmstart reduces iterations without collapsing exploration |
| LPBF parameter space + 3-panel viz | **Include, Improve to reviewer-facing** | 7 | Convert to causal/functional network mapping controllables → melt pool → defects → properties; indicate which parameters are measured/controlled/inferred/fixed; overlay sensor streams + fidelity levels |
| AM test structures 8-stage schematic | **Include** | 8 | Show ≥1 printed-and-characterized pilot structure; annotate what each stage measures; add go/no-go decision logic with where BOFN intervenes; tie stages to cost/cycle time |
| Project metrics / KPIs + go/no-go | **Include selectively, Improve presentation** | 7 | Reduce to 3–5 reviewer-salient metrics; define AI Acceleration Factor numerator/denominator; map each gate to observable artifact; include benchmark comparator |
| Thermo-Calc AM Module simulations | **Include as CALPHAD evidence** | 8 | Annotate melt pool predictions, printability windows, solidification parameters; cross-reference with experimental LPBF results; show how AM Module outputs feed BOFN surrogate |
| Thermo-Calc CALPHAD on BYU HPC | **Include in screening funnel** | 7 | Show screening throughput (calcs/hour), Al-Zr/Al-Mn-Cr-Zr phase diagrams, Scheil curves; connect to mineral-burden ranking |
| AlSi10Mg tensile data (U of Utah + 3D Powder Tech) | **Include as property endpoint** | 9 | Present stress–strain curves, YS/UTS/elongation; compare two sources; note build orientation and conditions |
| SEM/EDS (precursors + AMAZEMET-atomized powder) | **Include as input QC evidence** | 8 | Multi-panel with scale bars; show composition shift from AlSi10Mg baseline through Al wire + Si addition; quantify PSD |
| High-T tensile data | **Include as elevated-temperature capability** | 7 | Show stress–strain at elevated temperature; note test standard; connect to qualification relevance for high-T Al applications |
| Automated powder dispensing demo | **Include as workflow automation** | 7 | Show dispensing accuracy, repeatability; connect to closed-loop automation narrative (BOFN selects composition → dispenser prepares feedstock) |
| Ultrasonic atomizer (installed) | **Include in Facilities** | 9 | Annotated photo showing installed and operational system; label components; note first atomized batch |

### Metallurgical Grounding Requirements (from Materials Science Reviewer Perspective)

A materials science reviewer (not just ML) needs to see:

1. **CALPHAD/solidification criteria as constraints or objectives**: Freezing range, predicted solidification path, phase fractions, eutectic fraction, hot-cracking susceptibility indicator (Kou 2003 *Acta Materialia* 51:4321–4332). These should be explicit BOFN feasibility constraints, not post-hoc interpretation. Show how grain-refinement and eutectic-solidification strategies prune unprintable alloy regions before printing (Uba et al. 2025 *Materials* 18:5089). CALPHAD calculations should use established thermodynamic databases and Scheil-Gulliver solidification modeling (Lukas et al. 2007 *Computational Thermodynamics: The Calphad Method*, Cambridge University Press). **Thermo-Calc AM Module** simulations (provided by Thermo-Calc as collaborator) provide melt pool shape, printability windows, and G/R solidification parameters that directly constrain the BOFN search space. Additional CALPHAD screening has been run on BYU HPC using TCAl10 for Al-Zr and Al-Mn-Cr-Zr phase stability.

2. **Experimental validation chain**: Single tracks → cubes for density/crack screening → micro-CT/SEM/metallography → EDS/XRD on selected candidates. Link predicted CALPHAD/BOFN rankings to observed porosity, crack density, grain structure, and phase constitution in real LPBF specimens.

3. **Defect-mechanism linkage, not black-box prediction**: Connect model variables to known LPBF failure modes — wide freezing range → hot cracking; insufficient energy → lack-of-fusion porosity; unstable melt pool → defect-prone processing. Show at least one example where an in situ anomaly matched ex situ defect evidence (Kavas et al. 2025 *ArXiv* 2406.19096).

4. **Constrained multi-objective framing**: Show BOFN avoids infeasible regions and guards against underexposure/lack-of-fusion while seeking improved alloy-performance combinations. For Topic 3B, include a mineral-burden objective (e.g., minimize total critical mineral mass fraction or weighted criticality index subject to property targets) via scalarization or constrained multi-objective acquisition.

### Proposal-Ready Preliminary Results Section Opener (Draft)

> **⚠️ NEAR-FINAL — Experimental evidence (tensile, SEM/EDS, CALPHAD, atomizer, dispensing) is in hand. Verify specific numerical claims (MAE, cost reduction %, convergence iterations) against actual computational demo outputs before inserting into proposal. Version A is the target; Version B is the fallback if computational demo is incomplete.**

**Version A (Full Results Available — all computational + experimental evidence collected):**

> *We present preliminary results demonstrating each stage of the FLAIME closed-loop workflow on real materials. A full partial Knowledge Gradient for Function Networks (pKGFN) pipeline has been implemented, enabling cost-aware experiment selection across the multi-stage alloy discovery workflow (Figure 1). Thermo-Calc CALPHAD screening on BYU HPC clusters and AM Module simulations establish printability constraints and solidification parameters for Al-Zr and Al-Mn-Cr-Zr candidate spaces; SEM and EDS characterization of precursor powders (AlSi10Mg, Si) and ultrasonically atomized mixtures returned by AMAZEMET — with controlled composition adjustment through Al wire and Si addition — confirm that designed feedstock modifications are achievable and detectable (Figure 2). Baseline tensile data from AlSi10Mg specimens printed at the University of Utah and by 3D Powder Tech, together with high-temperature tensile results on a standard aluminum specimen, establish that the platform connects to qualification-relevant mechanical properties at both ambient and elevated temperatures (Figure 3). Autonomous experiment selection reaches the target feasible region in [X]× fewer iterations and at [Y]% lower cost than random/EI baselines (full ablation in supplementary materials). An automated powder dispensing demonstration shows that BOFN-selected compositions can be physically prepared without manual bottlenecks. Decision-ready go/no-go criteria with triggered actions are summarized in Table 1. These results collectively demonstrate that FLAIME is not an algorithm-only concept but a partially-closed physical loop ready for Phase I execution, with the mineral-burden optimization objective distinguishing this work from all existing autonomous alloy discovery efforts.*

**Version B (Fallback — computational demo incomplete):**

> *We present preliminary results demonstrating the computational and experimental infrastructure of the FLAIME closed-loop workflow. A full pKGFN pipeline implementation shows cost-aware experiment selection across the multi-stage alloy discovery workflow (Figure 1). Thermo-Calc CALPHAD screening and AM Module simulations establish printability constraints for critical-mineral-lean Al alloys; SEM and EDS characterization confirms feedstock quality and composition control through the atomization process (Figure 2). Available baseline tensile data from AlSi10Mg specimens provide the property-assessment endpoint (Figure 3), with expanded testing and critical-mineral-lean alloy screening planned as Milestone 1 deliverables. Decision-ready go/no-go criteria are summarized in Table 1.*

---

## Section A: Mock Program Officer (AMMTO) Feedback

**Selection logic**: DOE/AMMTO Phase I reviewers for Topic 3B (Critical Minerals) most reward evidence that (i) the proposed approach addresses critical mineral supply chain vulnerability through material substitution or elimination, (ii) the full closed loop is credible (the "software brain ↔ hardware body" cyberphysical framing), (iii) the optimization is cost-aware and robust to real/noisy data, and (iv) the experimental plan is scoped and qualification-relevant. Topic 3B explicitly calls for "AI-Enabled Materials Discovery, Development, and Qualification" of materials that reduce dependence on critical minerals. Bukkapatnam (2023) *IISE Transactions* 55:75–93 frames AMDM as an integrated cyberphysical system with an "intelligent software brain" coupled to a "hardware body" of synthesis/manufacturing and measurement equipment; the need is driven by iterative, expensive experiments in high-dimensional design spaces, making closed-loop decision-making central to accelerating discovery and qualification.

### A1. Top 5 Preliminary Results That Would Most Strengthen the Proposal

| # | Result | Why AMMTO Cares | Impact | Feasibility (19 days) |
|---|---|---|:---:|:---:|
| 1 | **End-to-end closed-loop digital demonstration** on a realistic alloy/LPBF surrogate: CALPHAD → BOFN selects next experiments under cost constraints → simulated characterization feedback → convergence to target property region with minimal critical mineral content | Most directly shows the core Phase I claim: autonomous decision-making across the full FLAIME workflow, not isolated model components. Aligns with AMMTO/3B emphasis on accelerated discovery of critical-mineral-lean alloys and reduced experimental burden. | 10/10 | 8/10 |
| 2 | **Retrospective BOFN benchmark using real alloy/process data** with multi-fidelity and multi-objective targets (e.g., density, crack tendency, hardness) | Demonstrates BOFN relevance to real alloy/process data, not only synthetic functions. Chawla et al. (2025) *ArXiv* 2511.16930 show cost-aware BO yields order-of-magnitude efficiency improvements in real indentation workflows. | 10/10 | 7/10 |
| 3 | **CALPHAD-to-print shortlist** for 3–5 candidate compositions with phase stability, solidification range, crack susceptibility proxies, and atomization/LPBF screening criteria, prioritizing Al-Zr and Al-Mn-Cr-Zr systems that minimize critical mineral content | Converts the concept into an actionable experimental starting set and shows manufacturability-aware down-selection aligned with critical mineral substitution goals. | 9/10 | 9/10 |
| 4 | **BOFN ablation study** comparing 4-node vs 9-node function networks, with and without cost-awareness, on a surrogate matching FLAIME workflow nodes | Builds on existing BoTorch verification and shows why the proposed architecture is necessary; strengthens technical originality. | 8/10 | 9/10 |
| 5 | **Decision-ready KPI/go-no-go dashboard** wired to autonomous actions (optimizer/experiment triggers) | In closed-loop systems, gates should not be passive "reporting" — they must be machine-actionable decisions that manage risk and cost. | 8/10 | 10/10 |

### A2. Most Compelling Figures and Captions

> **Note:** The figure numbers below reflect the full set of candidate figures developed during brainstorming. The **Figure Triage section** (above) establishes the final narrative allocation: **Figs 1–3 + Table 1** in the 5-page narrative (~1.5 pages). Remaining figures are described in text with quantitative metrics or placed in appendices.

**Figure 1 (highest value): End-to-end closed-loop + convergence (pKGFN pipeline)**
- *Content*: Two panels. (a) Function-network workflow diagram: CALPHAD screen → powder/atomization constraints → LPBF controllables → characterization outputs → pKGFN decision engine. (b) Convergence: cost-to-target vs. iteration, pKGFN vs. random/EI baselines.
- *Draft caption*: "FLAIME closed-loop autonomous discovery and qualification workflow for critical-mineral-lean alloys, implemented as a full pKGFN (partial Knowledge Gradient for Function Networks) pipeline consistent with AMDM cyberphysical 'software brain' + 'hardware body' architectures (Bukkapatnam 2023 *IISE Transactions*). pKGFN-guided, cost-aware experiment selection reaches the target feasible region faster and at lower total cost than baseline policies under matched budgets, while minimizing critical mineral content."
- *Maps to narrative Fig. 1.*

**Figure 2 (candidate): Real-data retrospective benchmark**
- *Content*: (a) Dataset summary; (b) learning curves/hypervolume; (c) overlay of suggested next points.
- *Draft caption*: "Retrospective evaluation on a noisy real-world dataset, demonstrating that cost-aware BO in closed-loop experimental systems yields significant efficiency improvements (Chawla et al. 2025 *ArXiv*)."
- *Triage: reported as quantitative metrics in text (MAE, cost-to-target numbers). Full figure in supplementary materials if needed.*

**Figure 3 (candidate): Cost model tied to workflow nodes**
- *Content*: Node-cost table/diagram showing relative cost of CALPHAD/cheap proxies vs. printing vs. characterization, and how BOFN uses cost information.
- *Draft caption*: "Cost-aware autonomy: BOFN weights information gain by the true workflow cost, favoring inexpensive computational queries for broad exploration and reserving expensive experimental evaluations for targeted exploitation (Alvi et al. 2026 *npj Computational Materials*)."
- *Triage: integrated into Fig. 1 as a cost annotation on the pipeline diagram, or described in text.*

**Figure 4: CALPHAD screening + SEM/EDS combined (→ narrative Fig. 2)**
- *Content*: Left half: screening funnel from broad composition space to 3–5 candidates + AM Module melt pool inset. Right half: 2×3 compact SEM/EDS multi-panel (precursor, atomized, composition verification).
- *Draft caption*: "Thermodynamics- and manufacturability-aware down-selection to an actionable Phase I candidate set of critical-mineral-lean Al alloys (left), grounded by SEM and EDS characterization confirming feedstock quality and composition control through the atomization process (right). CALPHAD screening on BYU HPC using TCAl10 + Thermo-Calc AM Module simulations (provided by Thermo-Calc as collaborator) predict melt pool geometry and printability windows."
- *Maps to narrative Fig. 2.*

**Table 1: KPI/go-no-go dashboard with triggered actions**
- *Content*: 5 KPIs + 8 gates + thresholds + measurement method + "optimizer action."
- *Draft caption*: "Decision-ready success criteria. Gates are tied to autonomous next actions (e.g., shift exploration between composition/process subspaces; request replicates; terminate unpromising branches), enabling efficient sequential experimentation in costly, high-dimensional settings."
- *Maps to narrative Table 1.*

### A3. Narrative Sections That Benefit Most from Additional Preliminary Data

1. **Preliminary Results**: Needs at least one end-to-end closed-loop result to establish cyberphysical integration credibility. Recent precedent: Priyadarshini et al. (2025) *ChemRxiv* demonstrated ML-driven closed-loop discovery of hard multiple principal element alloys, showing this paradigm is being adopted across material families.
2. **Technical Approach—Optimization and cost-awareness**: Strengthened by a real-data retrospective benchmark and explicit cost model, reflecting demonstrated gains of cost-aware BO in real experimental loops.
3. **Technical Approach—Experimental scope**: Strengthened by parameter reduction and test-structure/characterization matrix to prove tractability.
4. **Milestones/Risk management**: Strengthened by KPI/go-no-go dashboard that triggers clear decisions.

---

## Section B: Mock Enthusiastic Reviewer

### B1. What Pushes This from "Good" to "Must-Fund"

1. **Real-data BOFN win with strong baselines**: Clear learning-curve advantage and/or large cost-to-target reduction, mirroring real closed-loop cost-aware BO success stories (Chawla et al. 2025 *ArXiv*; Alvi et al. 2026 *npj Computational Materials*).
2. **End-to-end autonomy demonstration** showing a genuine "brain/body" loop and disciplined sequential experimentation under cost constraints.
3. **Explicit cost model + decision logic** that matches the realities of AM campaigns (cheap computations vs. expensive builds/characterization).

### B2. Strongest vs. Weakest Existing Results

**Strongest (keep and build upon):**
- BOFN implementations and cost-aware savings (the synthetic benchmark showed large cost reductions; however, this must be re-validated on real data before quoting specific percentages in the proposal)
- LPBF parameter mapping and test-structure progression: strong feasibility and experimental realism signals
- KPI/go-no-go gates: strong execution discipline

**Weakest / most vulnerable:**
- LLM warm-start POC: Reviewers may see it as peripheral unless quantified benefit is demonstrated on the same benchmark used to justify BOFN
- Any claims not tied to a closed-loop demonstration: AMDM reviewers expect integrated cyberphysical evidence, not modular proofs

---

## Section C: Mock Skeptical Reviewer

### C1. Biggest Gaps in Preliminary Results

1. **No proof on real/noisy data**: The field has examples where cost-aware BO is validated on real instruments; reviewers will ask for analogous evidence for this setting.
2. **Closed-loop integration risk**: AMDM is defined as an integrated brain/body system; without end-to-end evidence, the proposal looks like a set of disconnected components.
3. **Cost realism**: Reviewers will demand an explicit cost model and evidence that the method uses it effectively, since cost-awareness is central in the literature.

### C2. What Would Be Needed to Believe BOFN Works for Real Alloys

- **Retrospective on real dataset with noise handling**: At minimum, repeated runs, baselines, and uncertainty calibration.
- **Cost-aware advantage** demonstrated under a realistic cost model, consistent with prior cost-aware BO successes in real experimental loops.
- **Ablations**: Show where BOFN's gain comes from (function-network structure vs. standard BO), to avoid "overfit architecture" concerns.

### C3. Concerns About the 19-Day Timeline

- The only truly schedule-threatening items are (i) acquiring/cleaning a defensible real dataset and (ii) building a polished end-to-end demo; these should dominate the sprint.
- Attempting new atomization + LPBF printing purely for prelims is high risk unless machine time/powder logistics are guaranteed.
- The existing computational results (BOFN code, parameter maps, figures) are solid — the gap is in validation against real-world data.

---

## Section D: Mock Moderate Reviewer — Prioritized Results

| Rank | Preliminary Result | Figure/Table | Draft Caption Intent | Proposal Section |
|---|---|---|---|---|
| 1 | End-to-end closed-loop demo | Architecture + convergence (2-panel) | AMDM brain/body framing + cost/time advantage | Preliminary Results (lead) |
| 2 | Real-data retrospective benchmark | Learning curves + robustness (3-panel) | Real-world cost-aware BO value | Preliminary Results (second) |
| 3 | Cost model + cost-aware acquisition behavior | Node cost table + query selection frequency | Cheap exploration / expensive exploitation | Approach—Optimization |
| 4 | BOFN ablation (4-node vs. 9-node; cost-aware vs. not) | Cost-to-target + performance bars | Architecture justification | Preliminary Results—Algorithm Validation |
| 5 | CALPHAD-to-print shortlist | Screening funnel + candidate table | Actionable candidate space definition | Background + Prelims |
| 6 | LPBF parameter-space reduction to Phase I controllables | Pruning/Sankey diagram | Experimental tractability | Approach—Experimental Design Space |
| 7 | Test-structure/characterization matrix tied to gates | Matrix: structures × observables × decisions | Characterization matched to decision-making | Approach—Qualification/Characterization |
| 8 | KPI/go-no-go dashboard (instantiated) | Dashboard table: thresholds + actions | Operational readiness | Milestones/Work Plan |
| 9 | Data schema/interoperability | Dataflow/entity diagram | Robust data plumbing for autonomy | Approach—Data Management |
| 10 | Execution cadence + cost-to-data yield | Week-by-week Gantt table | Realistic operational planning | Management Plan/Budget |

---

## Section E: Synthesis and Action Plan

### E1. Top 5 "Must-Have" Results (Core, Achievable in 19 Days)

> **Note:** The specifications below describe the full set of must-have results. Per the **Figure Triage**, only the pKGFN closed-loop demo (narrative Fig. 1), CALPHAD screening + SEM/EDS combined (narrative Fig. 2), and tensile data (narrative Fig. 3) appear as narrative figures (~1.5 pages). The BOFN ablation and benchmark are reported as quantitative metrics in text, with full figures in supplementary materials. The KPI dashboard occupies ~0.25 pages as narrative Table 1.

1. **End-to-end closed-loop demo (full pKGFN pipeline)** — Uses the implemented pKGFN code + realistic alloy/LPBF surrogate. Shows the full CALPHAD → atomization → LPBF → characterization → optimizer loop with convergence curves. *This is the single most important new computational result, and the pipeline is already implemented.*
2. **Real-data retrospective benchmark** — Apply pKGFN to existing AlSi10Mg tensile data (U of Utah + 3D Powder Tech). Run against random/EI baselines. Even a small, noisy dataset is better than none — and we now have real tensile data.
3. **BOFN ablation study** — Systematic comparison of 4-node vs. 9-node, cost-aware vs. not. Leverages existing verified code. Minimal new development needed.
4. **CALPHAD-to-print shortlist** — Use Thermo-Calc (TCAl10 on BYU HPC + AM Module simulations provided by Thermo-Calc) to screen 3–5 candidate Al alloy compositions in the Al-Zr and Al-Mn-Cr-Zr spaces with printability heuristics and mineral-burden ranking, targeting critical-mineral-lean formulations.
5. **KPI/go-no-go dashboard instantiated on real + mock data** — Take the existing 5 KPIs + 8 gates and populate with actual tensile, SEM/EDS, and benchmark outputs. Show how thresholds trigger autonomous decisions.

### E2. Top 3 "Stretch" Results (High Impact but Time-Risky)

1. **Minimal experimental pilot coupons** — Only if machine time/powder logistics are already guaranteed. Even a single printed coupon with density measurement would be powerful.
2. **Multi-fidelity demonstration** — Show BOFN using cheap CALPHAD queries to guide expensive experimental evaluations. Requires clean implementation but builds on existing cost-aware code.
3. **Automated data plumbing demo** — End-to-end data flow from CALPHAD output → BOFN input → experiment suggestion → result ingestion. More integration engineering than science, but reviewers value it.

### E3. Figure Specifications for Must-Have Results

| Must-Have | Size | Content | Caption Approach | Key Citation |
|---|---|---|---|---|
| 1. Closed-loop demo | Full-width, ~0.5 page | (a) Function-network workflow; (b) cost-to-target; (c) constraint satisfaction probability | AMDM brain/body framing | Bukkapatnam (2023) *IISE Transactions* |
| 2. Real-data benchmark | Full-width, ~0.5 page, 3 panels | Dataset summary + learning curves + qualitative overlay | Real-world cost-aware BO | Chawla et al. (2025) *ArXiv* |
| 3. BOFN ablation | Quarter- to half-page | Regret/performance + cost-to-target bars | Architecture justification | (Self-generated) |
| 4. CALPHAD shortlist | Quarter-page figure + table | Screening funnel + ranked candidates | Actionable starting set | (Self-generated) |
| 5. KPI dashboard | Full-width table | KPI, gate, threshold, measurement, cadence, triggered action | Sequential experimentation under cost | Bukkapatnam (2023) *IISE Transactions* |

### E4. Mapping to Proposal Sections

| Proposal Section | Must-Have Results | Existing Assets to Incorporate |
|---|---|---|
| **Background/Motivation** | CALPHAD shortlist (context), mineral-burden framing | LPBF parameter space visualization (#20), literature reviews (#6), Topic 3B alignment |
| **Preliminary Results** | pKGFN closed-loop demo (lead), real-data benchmark, BOFN ablation, CALPHAD shortlist (TC on HPC + AM Module), tensile tests (U of Utah + 3D Powder Tech + high-T), SEM/EDS data (precursors + AMAZEMET-atomized powder), automated powder dispensing demo | BOFN implementations (#14), pKGFN pipeline (#14), LLM-warmstart POC (#14) |
| **Technical Approach** | References from all must-haves; TC AM Module simulation results | Test structure schematics (#30), parameter space map (#20), welding data (#18) |
| **Objectives/Go-No-Go** | KPI dashboard | 5 KPIs + 8 gates (#26, #34), metrics v4 (#34) |
| **Management/Schedule** | Execution cadence table | Budget breakdown (#26), team chart (#26), partnership letters |
| **Facilities/Equipment** | Atomizer setup photo (installed), SEM/EDS capability, BYU HPC (Thermo-Calc), automated dispensing hardware | Thermo-Calc analysis (#24), company landscape (#16) |

---

## Section F: Experimental Capability Evidence (Must-Have)

*See Edison provenance log at end of document for query details.*

Purely computational preliminary results trigger feasibility concerns among DOE/AMMTO reviewers — particularly for Topic 3B, where the core risks in closed-loop alloy discovery include powder quality, print defects, composition drift, throughput, and property-testing latency, in addition to demonstrating that the platform can actually produce critical-mineral-lean alloys that meet performance targets (Bukkapatnam 2023 *IISE Transactions* 55:75–93; note: this inference about reviewer behavior is based on the AMDM literature's emphasis on integrated cyberphysical systems, not direct evidence about reviewer scoring). Proposals that demonstrate existing experimental infrastructure and validation are viewed as markedly more feasible (Miracle et al. 2021 *Annual Review of Materials Research* 51:131–164). The following experimental evidence items have been collected or are in hand, demonstrating that FLAIME has a partially-closed physical loop — not algorithm-only.

### F1. Experimental Evidence Priority Ranking

| Rank | Evidence Type | Impact on Credibility | Reviewer Question Answered | Status |
|---|---|:---:|---|---|
| 1 | **D. Tensile tests** (AlSi10Mg from U of Utah + 3D Powder Tech; high-T standard Al) | Highest | "Can the team connect process/composition to mechanical performance — not just microstructure?" | ✅ Data in hand |
| 2 | **B. SEM images** (precursor AlSi10Mg + Si powder + AMAZEMET-atomized mixture + printed microstructure) | High | "Can they evaluate whether their powders and builds are suitable for LPBF?" | ✅ Data in hand |
| 3 | **C. EDS data** (composition verification of precursor + atomized powder, elemental mapping) | High | "Can they confirm that designed compositions were achieved and detect segregation/contamination?" | ✅ Data in hand |
| 4 | **A. Ultrasonic atomizer photos** (lab setup, installed and operational) | Moderate | "Do they actually have the hardware, or is powder production still aspirational?" | ✅ Installed |
| 5 | **E. Automated powder dispensing** demonstration | Moderate | "Can the workflow automate feedstock preparation, or is it manual?" | ✅ Demo complete |
| 6 | **F. Thermo-Calc AM Module simulations** (provided by TC) | Moderate–High | "Does the team have access to state-of-the-art CALPHAD tools for AM?" | ✅ Simulations in hand |

### F2. Evidence-by-Evidence Specifications

#### A. Ultrasonic Atomizer Setup Photos (Installed)

**What to show:**
- Wide shot proving installation in your lab with labeled components — **atomizer is installed and operational**
- Close-up of crucible/nozzle/transducer, powder collection chamber, inert gas system, safety enclosure
- First powder batch collected in vial/tray (from AMAZEMET rePOWDER service)

**Key quality indicators (reviewers look for):**
- Operational readiness (installed, plumbed, inert gas, collection, safety) — demonstrated
- Evidence of understanding powder risks: oxidation, fines, contamination control (Meier et al. 2022 *Int. J. Adv. Manuf. Technol.* 123:1577–1588)

**Draft figure caption:**
> "Ultrasonic atomization capability installed and operational in the FLAIME laboratory (AMAZEMET system). This in-house powder-production node enables rapid generation of custom alloy feedstocks for AI-guided design iterations. First atomized batches (AlSi10Mg base with controlled Al wire + Si composition adjustment) have been produced and characterized by SEM/EDS (see narrative Fig. 2)."

**Layout:** 2–3 panels: (a) full setup, (b) labeled close-up, (c) optional first powder batch. Use arrows and short callouts.

**Proposal placement:** Preliminary Results or Facilities/Resources; cross-reference in Technical Approach workflow figure.

**MVP if constrained:** One annotated photo of installed system + one sentence stating operational status and planned first alloy.

**Risk if omitted:** Reviewers infer a steep startup curve, dependence on future procurement/training, or that powder production is not yet real.

#### B. SEM Images (Precursor Powders + Atomized Mixture + Printed Microstructure)

**What to show:**
- Precursor powders: commercial AlSi10Mg powder and Si powder at identical magnification with scale bars
- AMAZEMET-atomized mixture: powder returned from AMAZEMET after ultrasonic atomization with controlled composition change (original AlSi10Mg + Al wire + Si addition), showing modified particle morphology
- At least one LPBF-printed cross-section at low magnification showing melt tracks/porosity + one higher-magnification region showing grain structure/defects; build direction indicator

**Key quality indicators:**
- Scale bars, representative fields of view, sample IDs
- Quantitative companion metrics: PSD d10/d50/d90, sphericity/circularity, satellite fraction, relative density/porosity estimate
- Powder morphology and PSD directly influence flow/spreadability and map to part density (Brika et al. 2020 *Additive Manufacturing* 31:100929; 529 citations)

**Draft figure caption:**
> "SEM demonstrates FLAIME's feedstock-to-build characterization capability. (a) Commercial AlSi10Mg precursor powder, (b) Si powder additive, (c) ultrasonically atomized mixture returned by AMAZEMET (AlSi10Mg base + Al wire + Si addition, producing a controlled composition shift from the original AlSi10Mg), (d) LPBF-printed cross-section with melt-track boundaries and porosity assessment. The composition change from (a) to (c) demonstrates that the atomization node can modify alloy feedstock chemistry — a prerequisite for the BOFN-guided composition search. Quantitative PSD and porosity metrics are reported inline in the figure inset and accompanying text."

**Layout:** 4+ panels: (a) AlSi10Mg precursor powder, (b) Si powder, (c) AMAZEMET-atomized mixture, (d) LPBF-printed cross-section. Small inset with 2–3 bullet metrics.

**Proposal placement:** Preliminary Results, immediately after workflow overview.

**MVP if constrained:** Precursor AlSi10Mg + atomized mixture SEM comparison + one printed-sample SEM with scale bars and concise annotations.

**Risk if omitted:** Proposal reads as algorithm-heavy with weak materials characterization capability.

#### C. EDS Data (Composition Verification + Elemental Mapping)

**What to show:**
- Target-vs-measured composition summary (bar chart/table) for precursor powders (AlSi10Mg, Si), AMAZEMET-atomized mixture, and printed samples
- At least one elemental map set (or RGB overlay) showing key alloying elements — addresses segregation and contamination questions
- Highlight the controlled composition shift: original AlSi10Mg → atomized mixture (Al wire + Si addition changes Al/Si/Mg ratios)

**Key quality indicators:**
- Report acquisition conditions or note standardless/standardized method
- Quantify deviation from target composition with uncertainty/caveats for light elements
- Avoid overclaiming phase ID from EDS alone (Dryepondt et al. 2023, DOE/ORNL report doi:10.2172/2345330)

**Draft figure caption:**
> "EDS verifies that designed alloy chemistries are achieved and that composition modifications through atomization are detectable. (a) Target vs. measured composition for key alloying elements across precursor AlSi10Mg, Si additive, and AMAZEMET-atomized mixture (note controlled shift from original AlSi10Mg through Al wire + Si addition), (b) elemental map of atomized powder, (c) elemental map of LPBF cross-section. These data form a direct experimental input to FLAIME's Bayesian optimization loop by distinguishing successful synthesis from composition drift or segregation."

**Layout:** 3 panels: (a) target vs. measured composition bar/table, (b) powder elemental map, (c) printed coupon elemental map. Consistent color legend across maps.

**Proposal placement:** Preliminary Results, paired with SEM figure (or combined SEM/EDS figure).

**MVP if constrained:** One target-vs-measured composition table and one elemental overlay map from a representative sample.

**Risk if omitted:** Reviewers doubt that AI-suggested compositions can be manufactured reproducibly or that the team can detect chemistry drift.

#### D. Tensile Test Results (AlSi10Mg from University of Utah + 3D Powder Tech; High-T Standard Al)

**What to show:**
- Stress–strain curves from AlSi10Mg LPBF specimens: (1) printed at University of Utah using sourced AlSi10Mg powder, (2) from 3D Powder Tech
- Summary table with YS, UTS, elongation; state printing site, build orientation, post-processing, and test standard (ASTM E8/E8M)
- High-temperature tensile data from a standard aluminum tensile specimen (demonstrates elevated-T testing capability)
- Replicate curves or error bars if available

**Key quality indicators:**
- Traceability: orientation, heat treatment, specimen geometry, sample count
- Collaborator attribution: clearly define what you controlled vs. what partners controlled (e.g., U of Utah printed the specimen, BYU/collaborator performed tensile testing)
- Two independent AlSi10Mg sources (U of Utah and 3D Powder Tech) provide cross-validation of the baseline
- High-T data demonstrates capability for applications requiring elevated-temperature performance
- Tensile results tie chemistry and defects back to qualification-relevant properties (Meier et al. 2022 *Int. J. Adv. Manuf. Technol.* 123:1577–1588)

**Draft figure caption:**
> "Baseline LPBF tensile data establishing that FLAIME is anchored to measurable, qualification-relevant mechanical properties. (a) Representative stress–strain curves for AlSi10Mg specimens printed at the University of Utah (Taylor Sparks, letter of support) and sourced from 3D Powder Tech, demonstrating reproducible baseline properties from independent sources. (b) High-temperature tensile data on a standard aluminum specimen, demonstrating elevated-temperature testing capability. (c) Summary of yield strength, ultimate tensile strength, and elongation by condition and source. These results provide the property-assessment endpoint for the proposed closed-loop composition–process–microstructure–performance optimization, targeting critical-mineral-lean alloys."

**Layout:** 3 panels: (a) stress–strain curves (U of Utah + 3D Powder Tech), (b) high-T stress–strain, (c) bar chart/table of YS/UTS/elongation by material/source/temperature. Concise footnote with processing/test conditions.

**Proposal placement:** Preliminary Results (near end of section) or Validation/Qualification subsection; also cite in Team/Partnerships to highlight Taylor Sparks (letter of support) and 3D Powder Tech.

**MVP if constrained:** One stress–strain curve + 3-metric summary table for AlSi10Mg from a named source.

**Risk if omitted:** Highest credibility loss — reviewers may conclude the platform is discovery-only, not qualification-capable.

### F3. Framing Experimental + Computational Integration

Each evidence type maps to a **contracted interface** in the closed-loop FLAIME platform:

| Loop Stage | Evidence Type | Role in Closed Loop |
|---|---|---|
| **Design / pKGFN** (computational) | Full pKGFN pipeline | pKGFN proposes compositions, process windows, and uncertainty-aware next experiments using cost-aware multi-fidelity acquisition |
| **CALPHAD Screening** | Thermo-Calc on BYU HPC + AM Module | Phase stability, solidification paths, printability windows, melt pool predictions — constraints and cheap fidelity for pKGFN |
| **Synthesis** | A. Atomizer (installed) + automated powder dispensing | Ultrasonic atomizer produces powders for candidate compositions; automated dispensing enables BOFN-selected feedstock preparation without manual bottlenecks |
| **Input QC** | B. SEM + C. EDS (precursors + AMAZEMET-atomized powder) | Verify that *intended* inputs to LPBF are real (powder morphology, composition); detect failure modes early (satellites, contamination, segregation); confirm composition shift through atomization |
| **Build + Microstructure QC** | B. SEM + C. EDS (printed cross-sections) | Printed coupons assessed for porosity, microstructural state, composition integrity; populates process–structure mapping |
| **Property Endpoint** | D. Tensile tests (ambient: U of Utah + 3D Powder Tech; elevated-T: standard Al) | Provides the objective function for optimization and qualification-relevant evidence at multiple temperature conditions |
| **Model Update** | All → pKGFN | Every experimental result (with uncertainty) updates the surrogate; QC thresholds become feasibility constraints |

**Key narrative point:** Explicitly state in the proposal that every experiment updates the BOFN surrogate with uncertainty, and that QC thresholds (composition deviation, porosity limits, satellite fraction) become feasibility constraints in the optimizer. This transforms standalone experimental evidence into demonstration of a partially-closed loop.

### F4. Updated Figure Specifications for Experimental Evidence

| Evidence | Size | Content | Caption Approach | Key Citation |
|---|---|---|---|---|
| A. Atomizer setup (installed) | Quarter-page, 2–3 panels | (a) Full setup; (b) labeled close-up; (c) first AMAZEMET powder batch | Infrastructure readiness, operational status | Bukkapatnam (2023) *IISE Transactions* |
| B. SEM images | Full-width, 4+ panels | (a) AlSi10Mg precursor; (b) Si powder; (c) AMAZEMET-atomized mixture; (d) printed cross-section | Feedstock-to-build characterization, composition modification capability | Brika et al. (2020) *Additive Manufacturing*; Sutton et al. (2017) *Virtual & Physical Prototyping* |
| C. EDS data | Half- to full-width, 3 panels | (a) Target vs. measured composition (precursor → atomized → printed); (b) powder map; (c) printed map | Composition verification, ground truth for optimizer | Kennedy et al. (2019) *JMEP* |
| D. Tensile tests | Half-width, 3 panels + table | (a) AlSi10Mg stress–strain (U of Utah + 3D Powder Tech); (b) high-T stress–strain; (c) YS/UTS/elongation summary | Qualification-relevant endpoint at ambient + elevated T | Miracle et al. (2021) *Ann. Rev. Mater. Res.* |
| E. Automated powder dispensing | Quarter-page, 1–2 panels | (a) Dispensing setup; (b) accuracy/repeatability data | Workflow automation, closed-loop feedstock preparation | (Self-generated) |
| F. TC AM Module simulations | Quarter-page, 2 panels | (a) Melt pool prediction; (b) printability window | CALPHAD-informed process constraints for BOFN | Thermo-Calc AM Module documentation |

### F5. Risk Assessment Summary

| Evidence | Status | Risk if Omitted | Minimum Viable Version |
|---|---|---|---|
| A. Atomizer photos | ✅ Installed | Steep-startup concern; powder production looks aspirational | One annotated in-lab photo + "installed and operational" statement |
| B. SEM images | ✅ Data in hand | Algorithm-heavy impression; weak materials characterization | Precursor vs. atomized comparison + one printed cross-section, all with scale bars |
| C. EDS data | ✅ Data in hand | Doubt about composition reproducibility and drift detection | Target-vs-measured table for precursor + atomized + one elemental overlay |
| D. Tensile tests | ✅ Data in hand | **Highest risk** — perceived as discovery-only, not qualification-capable | One stress–strain curve + YS/UTS/elongation table from U of Utah or 3D Powder Tech |
| E. Powder dispensing demo | ✅ Demo complete | Reviewers assume manual workflow, undermining autonomy claim | One photo/screenshot + accuracy metric |
| F. TC AM Module sims | ✅ Simulations in hand | Miss opportunity to show state-of-the-art CALPHAD integration | One melt pool prediction + one printability window for Al-Zr candidate |

### F6. Contingency Plans for External Dependencies

| Dependency | Status | Original Trigger Date | Contingency (if needed) |
|---|---|---|---|
| Tensile data from U of Utah | ✅ **Resolved** — AlSi10Mg specimen printed by Taylor Sparks (letter of support), tensile data collected | Day 8 (Apr 16) | N/A — data in hand |
| Tensile specimen from 3D Powder Tech | ✅ **Resolved** — AlSi10Mg specimen received | Day 8 (Apr 16) | N/A — specimen in hand |
| High-T tensile data | ✅ **Resolved** — standard aluminum specimen tested | Day 10 (Apr 18) | N/A — data in hand |
| SEM/EDS for precursor powders | ✅ **Resolved** — AlSi10Mg and Si powder characterized | Day 6 (Apr 14) | N/A — data in hand |
| SEM/EDS for AMAZEMET-atomized powder | ✅ **Resolved** — atomized mixture returned and characterized | Day 8 (Apr 16) | N/A — data in hand |
| Atomizer installation | ✅ **Resolved** — installed and operational | Day 3 (Apr 11) | N/A — installed |
| Thermo-Calc AM Module simulations | ✅ **Resolved** — provided by Thermo-Calc (letter of collaboration) | Day 10 (Apr 18) | N/A — simulations in hand |
| Thermo-Calc CALPHAD on BYU HPC | ✅ **Resolved** — simulations completed | Day 7 (Apr 15) | N/A — runs complete |
| pKGFN pipeline implementation | ✅ **Resolved** — full pipeline implemented | Day 6 (Apr 14) | N/A — code complete |
| Automated powder dispensing | ✅ **Resolved** — demonstration complete | Day 8 (Apr 16) | N/A — demo complete |
| Real LPBF dataset for benchmark | Day 5 (Apr 13) | **Active** | Use AlSi10Mg tensile data from U of Utah + 3D Powder Tech as benchmark dataset; supplement with Trevisan et al. (2017) or Li et al. (2020) published data |
| Letters of collaboration (Valimet, AMAZEMET, Thermo-Calc) | Day 15 (Apr 23) | **Active — in progress** | Draft letters prepared; follow up by Day 18 |
| Letters of support (Ames, Fehrmann, Sparks, Speer, Clare, Stiles, Hattrick-Simpers, Brown) | Day 15 (Apr 23) | **Active — in progress** | Prioritize based on responsiveness; minimum 5 of 8 needed |

---

## 19-Day Sprint Plan

| Day Range | Task | Lead | Output Artifact | Dependencies | Risk/Mitigation |
|---|---|---|---|---|---|
| **D1–2** (Apr 9–10) | Lock proposal thesis, freeze scope; assign owners; **contingency triage** — confirm all external dependencies or activate fallbacks | PI | Evidence matrix mapping each result to claim, figure, section | Existing KPI/gates, topic-fit analysis | Scope creep → limit to must-haves and require every task to map to a proposal claim |
| **D1–4** (Apr 9–12) | Build end-to-end FLAIME digital closed-loop demo using full pKGFN pipeline + realistic alloy/LPBF surrogate | Computational lead | **Narrative Fig. 1**: pipeline schematic + convergence plot vs. random/EI | pKGFN pipeline (✅ complete), surrogate definition | Integration bugs → use mock interfaces/CSV handoffs first, polish visuals later |
| **D2–5** (Apr 10–13) | Run BOFN ablation: 4-node vs. 9-node, cost-aware vs. not, common budget and stopping criteria | Computational lead | **Supplementary**: regret/cost/hypervolume comparison; quantitative metrics reported in narrative text | Existing verified BoTorch implementations | Unclear advantage → predefine success metrics; emphasize cost-to-target if absolute performance is similar |
| **D2–6** (Apr 10–14) | Assemble retrospective real-data benchmark using AlSi10Mg tensile data (U of Utah + 3D Powder Tech) + literature data; clean, normalize, define objectives/constraints | Computational lead | **Supplementary or text**: retrospective benchmark learning curves; MAE and cost-to-target numbers reported inline | AlSi10Mg tensile data (✅ in hand), property/process labels | Dataset size → supplement with published AlSi10Mg data and state limitations |
| **D4–7** (Apr 12–15) | Produce CALPHAD-to-print shortlist for 3–5 candidate compositions in Al-Zr and Al-Mn-Cr-Zr spaces using Thermo-Calc on BYU HPC (✅ runs complete) + AM Module simulations (✅ provided by TC), targeting critical-mineral-lean formulations with mineral-burden ranking | Domain expert / PI | **Narrative Fig. 2 (left half)**: screening funnel + candidate table + AM Module melt pool/printability insets | TC CALPHAD results (✅), AM Module sims (✅), alloy system choice | Weak differentiation → rank with transparent criteria including mineral burden and include uncertainty |
| **D5–8** (Apr 13–16) | Reduce LPBF search space from 130+ to defendable Phase I subset linked to test structures/sensors (dimensionality grounded in DebRoy et al. 2018 *Prog. Mater. Sci.*) | PI | Supporting text for Technical Approach | Existing parameter map (#20), test-structure plan (#30) | Arbitrary appearance → classify by controllability, sensitivity, information value |
| **D6–9** (Apr 14–17) | Convert test-structure progression into decision-ready characterization matrix tied to KPIs and go/no-go gates | Experimental lead | Supporting text for Technical Approach | Existing 8-stage validation (#30), KPI framework (#34) | Too many structures → highlight minimum informative build set |
| **D7–10** (Apr 15–18) | Instantiate KPI/go-no-go dashboard on real data (AlSi10Mg tensile, SEM/EDS metrics) + mock data for remaining KPIs; connect thresholds to pKGFN next-step decisions | Computational lead | **Narrative Table 1**: dashboard with 5 KPIs, 8 gates, thresholds, triggered actions | Existing KPI definitions (#34), tensile/SEM data (✅) | Feels managerial → explicitly link each gate to experimental/algorithmic decisions |
| **D1–8** (Apr 9–16) | **Prepare all experimental evidence figures**: (1) annotated atomizer photo (✅ installed); (2) SEM multi-panel (precursor AlSi10Mg + Si + AMAZEMET-atomized mixture + printed cross-section) (✅ data in hand); (3) EDS panels (target vs. measured + elemental maps) (✅ data in hand); (4) tensile figure (U of Utah + 3D Powder Tech stress–strain + high-T + summary table) (✅ data in hand); (5) automated powder dispensing demo photo/data (✅ demo complete); (6) TC AM Module simulation figures (✅ simulations in hand) | Experimental lead + PI | **Narrative Fig. 2 (right half)**: SEM/EDS compact panels; **Narrative Fig. 3**: tensile data; **Facilities appendix**: atomizer photo + dispensing | All data in hand | Figure quality → allocate D7–8 for polish and annotation |
| **D9–12** (Apr 17–20) | Draft and polish all preliminary-results captions, methods snippets, and section text around new figures; incorporate partnership framing (Valimet, AMAZEMET, Thermo-Calc as collaborators; 8 support letter providers) | PI + all leads | Proposal-ready captions + 1–2 paragraphs per figure | Completion of core analyses/figures | Weak narrative → write claim-evidence-impact text while results are fresh |
| **D11–14** (Apr 19–22) | Integrate schedule, staffing, and budget with preliminary evidence; create execution table tied to milestones; finalize partnership letters | PI | Gantt/execution table + revised budget justification + draft letters | Core technical figures, budget scenarios, go/no-go gates | Early-career credibility → show narrow scope with collaborator roles and fallbacks |
| **D15–17** (Apr 23–25) | Red-team review by skeptical colleague/mentor focusing on feasibility, real-data validation, overclaiming; collect outstanding letters of collaboration/support | External reviewer | Annotated review memo; revised figures/captions; signed letters | Near-final draft with all core artifacts | Late discovery of holes → ask reviewers to score novelty, feasibility, evidence sufficiency |
| **D18–19** (Apr 26–28) | Final compliance pass: DOE formatting, 5-page narrative limit, references, figure readability, consistency; verify all letters received | PI | Submission-ready PDF + compliance checklist signoff | Full draft, template, all figures/tables, all letters | Last-minute errors → freeze technical content by D17; reserve D18–19 strictly for QA |

---

## Key Literature Informing This Assessment

1. Bukkapatnam, S.T.S. (2023). Autonomous materials discovery and manufacturing (AMDM): a review and perspectives. *IISE Transactions*, 55:75–93. doi:10.1080/24725854.2022.2089785. (26 citations)
2. Chawla, V., Puplampu, S., Zhu, H., Rack, P.D., Penumadu, D., and Kalinin, S.V. (2025). Accelerated materials discovery through cost-aware Bayesian optimization of real-world indentation workflows. *ArXiv*, 2511.16930. doi:10.48550/arxiv.2511.16930. (2 citations)
3. Alvi, S.M.A.A., Vela, B., Attari, V., Janssen, J., Perez, D., Allaire, D.L., and Arróyave, R. (2026). Deep Gaussian process-based cost-aware batch Bayesian optimization for complex materials design campaigns. *npj Computational Materials*. doi:10.1038/s41524-026-01981-7. (2 citations; advance online publication — verify publication status before proposal submission.)
4. Kavas, B., Balta, E.C., Tucker, M., Krishnadas, R., Rupenyan, A., Lygeros, J., and Bambach, M. (2025). In-situ controller autotuning by Bayesian optimization for closed-loop feedback control of laser powder bed fusion process. *ArXiv*, 2406.19096. doi:10.48550/arxiv.2406.19096. (18 citations)
5. Sabanza-Gil, V., Barbano, R., Pacheco Gutiérrez, D., Luterbacher, J.S., Hernández-Lobato, J.M., Schwaller, P., and Roch, L. (2025). Best practices for multi-fidelity Bayesian optimization in materials and molecular research. *Nature Computational Science*, 5(7):572–581. doi:10.48550/arxiv.2410.00544. (25 citations)
6. Uba, C.U., Ding, H., Chen, Y., Guo, S., and Raush, J.R. (2025). Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. *Materials*, 18:5089. doi:10.3390/ma18225089. (2 citations)
7. Papatheodorou, A., Papadimitriou, N., Stathatos, E., Benardos, P., and Vosniakos, G.-C. (2025). Recent advances in sensor fusion monitoring and control strategies in laser powder bed fusion: a review. *Machines*, 13:820. doi:10.3390/machines13090820. (6 citations)
8. Miracle, D.B., Li, M., Zhang, Z., Mishra, R., and Flores, K.M. (2021). Emerging capabilities for the high-throughput characterization of structural materials. *Annual Review of Materials Research*, 51:131–164. doi:10.1146/annurev-matsci-080619-022100. (79 citations)
9. Brika, S.E., Letenneur, M., Dion, C.A., and Brailovski, V. (2020). Influence of particle morphology and size distribution on the powder flowability and laser powder bed fusion manufacturability of Ti-6Al-4V alloy. *Additive Manufacturing*, 31:100929. doi:10.1016/j.addma.2019.100929. (529 citations)
10. Meier, B., Warchomicka, F., Petrusa, J., Angerer, P., Wosik, J., Kaindl, R., Petrovic, V., Waldhauser, W., and Sommitsch, C. (2022). Influence of powder production process and properties on material properties of Ti6Al4V manufactured by L-PBF. *International Journal of Advanced Manufacturing Technology*, 123:1577–1588. doi:10.1007/s00170-022-10250-y. (13 citations)
11. Sutton, A.T., Kriewall, C.S., Leu, M.C., and Newkirk, J.W. (2017). Powder characterisation techniques and effects of powder characteristics on part properties in powder-bed fusion processes. *Virtual and Physical Prototyping*, 12:29–35. doi:10.1080/17452759.2016.1250605. (462 citations)
12. Kennedy, S.K., Dalley, A.M., and Kotyk, G.J. (2019). Additive manufacturing: assessing metal powder quality through characterizing feedstock and contaminants. *Journal of Materials Engineering and Performance*, 28:728–740. doi:10.1007/s11665-018-3841-5. (19 citations)
13. Priyadarshini, M.S., Gienger, E., Ren, J., Piloseno, B., Pogue, E.A., Lambert, P.K., Ko, J.S., and Clancy, P. (2025). Machine learning-driven closed-loop discovery of hard multiple principal element alloys. *ChemRxiv*. doi:10.26434/chemrxiv-2025-klz0c. (0 citations)
14. Dryepondt, S. et al. (2023). Prioritization of existing reactor materials. DOE/ORNL report. doi:10.2172/2345330. (2 citations)
15. Kou, S. (2003). A criterion for cracking during solidification. *Acta Materialia*, 51(8):4321–4332. doi:10.1016/S1359-6454(03)00266-5. (Foundational hot-cracking susceptibility index for alloy screening in welding and AM.)
16. Lukas, H.L., Fries, S.G., and Sundman, B. (2007). *Computational Thermodynamics: The Calphad Method*. Cambridge University Press. (Foundational CALPHAD reference.)
17. DebRoy, T., Wei, H.L., Zuback, J.S., Mukherjee, T., Elmer, J.W., Milewski, J.O., Beese, A.M., Wilson-Heid, A., De, A., and Zhang, W. (2018). Additive manufacturing of metallic components — process, structure and properties. *Progress in Materials Science*, 92:112–224. doi:10.1016/j.pmatsci.2017.10.001. (Comprehensive LPBF parameter space review; >4000 citations.)

---

## Summary: What to Prioritize

**Available evidence in hand (no longer aspirational):**
1. Full pKGFN pipeline implementation — *end-to-end closed-loop demo ready to run*
2. AlSi10Mg tensile data from U of Utah (Taylor Sparks) and 3D Powder Tech — *two independent baseline sources*
3. High-temperature tensile data (standard Al specimen) — *elevated-T capability demonstrated*
4. SEM/EDS of precursor powders (AlSi10Mg, Si) and AMAZEMET-atomized mixture — *feedstock QC evidence*
5. Thermo-Calc AM Module simulations (provided by TC) + CALPHAD screening on BYU HPC — *CALPHAD integration evidence*
6. Ultrasonic atomizer installed and operational — *synthesis capability*
7. Automated powder dispensing demonstration — *workflow automation*

**Computational results still needed:**
1. End-to-end closed-loop demo (Fig. 1) — *non-negotiable; pKGFN pipeline ready, need to run on surrogate and produce convergence plots*
2. BOFN ablation study (Supplementary fallback) — *leverages existing code*
3. Real-data retrospective benchmark (supplementary/text) — *can now use U of Utah / 3D Powder Tech tensile data*
4. CALPHAD-to-print screening funnel figure (Fig. 2) — *TC data in hand, need to produce funnel visualization with mineral-burden ranking*
5. KPI/go-no-go dashboard instantiated (Table 1) — *fastest to produce, high PO impact; can now populate with real data*

**If bandwidth-constrained, prioritize figures in this order:**
1. Narrative Fig. 1 (pKGFN closed-loop demo + convergence) → Narrative Fig. 3 (tensile: 2 sources + high-T) → Narrative Fig. 2 (CALPHAD screening + SEM/EDS combined) → Narrative Table 1 (KPI dashboard) → Supplementary: benchmark/ablation full figures

**Experimental evidence priority order** (from Edison iteration 3, updated with current status):
1. **Tensile tests** ✅ — qualification-relevant endpoint; highest credibility impact; data in hand from two sources plus high-T
2. **SEM images** ✅ — fastest reviewer-recognizable proof of characterization capability; precursor + atomized + printed
3. **EDS data** ✅ — composition verification across atomization step; ground truth for surrogate model
4. **Atomizer photos** ✅ — installed and operational; quick to annotate
5. **Automated powder dispensing** ✅ — workflow automation evidence; novel for alloy SDL
6. **TC AM Module simulations** ✅ — state-of-the-art CALPHAD/AM integration

**What to deprioritize:**
- LLM warm-start: Keep existing POC but don't invest more time unless it produces a quantified gain on the same benchmark as pKGFN
- Data plumbing automation: Important for execution but less visible in the proposal itself

**Key framing insight:** Each experimental evidence item maps to a node in the FLAIME closed loop — atomizer + dispensing = synthesis, SEM/EDS = input/build QC, tensile = property endpoint, TC CALPHAD/AM Module = computational screening. Present them as contracted interfaces in the autonomous workflow, not standalone experiments. Explicitly state that every experimental result updates the pKGFN surrogate with uncertainty and that QC thresholds become feasibility constraints. The mineral-burden objective — missing from all competing efforts — is the Topic 3B differentiator.

---

## FOA Evaluation Criteria Mapping

DOE Genesis Mission proposals for Topic 3B (Critical Minerals) are scored on four criteria. Each must-have preliminary result should demonstrably address at least one:

| FOA Criterion | Must-Have Results That Address It | Key Evidence |
|---|---|---|
| **Scientific/Technical Merit** | pKGFN closed-loop demo, BOFN ablation, real-data benchmark, TC AM Module sims | Novel cost-aware multi-fidelity BO over full powder-to-property chain; architecture justified by ablation; mineral-burden objective; Thermo-Calc CALPHAD integration |
| **Impact vs. State of Art** | pKGFN closed-loop demo, CALPHAD shortlist, tensile tests, automated dispensing | Accelerated discovery of critical-mineral-lean alloys; qualification pathway vs. traditional sequential campaigns; real material properties from multiple sources, not just predicted; workflow automation |
| **Team Qualifications/Resources** | SEM/EDS data, atomizer photos, tensile tests, TC sims, dispensing demo, partnership letters | Existing infrastructure (atomizer installed, SEM/EDS in-house, BYU HPC), established characterization data, 3 letters of collaboration (Valimet, AMAZEMET, Thermo-Calc) + 8 letters of support spanning AM, SDL, materials, and qualification expertise; platform applies to multiple alloy systems |
| **Proposed Work Plan** | KPI dashboard, sprint plan, contingency table | Machine-actionable go/no-go gates; realistic timeline with most contingencies already resolved; clear Phase II scale-up path via Valimet GA + AMAZEMET UA |

---

## Phase II Vision (Results That De-Risk Phase II)

Even for Phase I, DOE reviewers want to see that Phase I results enable a credible Phase II (verify exact ceiling in DE-FOA-0003612 §II.A; typical Genesis Mission Phase II awards are $2M–$5M over 2–3 years). Each Phase I preliminary result should point forward to scaled critical mineral substitution:

| Phase I Result | Phase II Capability It Enables |
|---|---|
| pKGFN closed-loop demo (digital) | Phase II: closed-loop with real hardware, including in-situ monitoring integration; applied to multiple critical-mineral-lean alloy families |
| Real-data benchmark | Phase II: validated surrogate models enabling transfer to new alloy systems (Al-Ce, Cu-Cr-Zr, other critical-mineral substitutes) |
| BOFN ablation | Phase II: optimized network architecture for multi-objective qualification campaigns with mineral-burden constraints |
| CALPHAD shortlist (TC on HPC + AM Module) | Phase II: expanded alloy search space across Al-Zr, Al-Mn-Cr-Zr, and Cu-Cr-Zr families with multi-fidelity screening at scale; full Thermo-Calc AM Module integration for process-composition co-optimization |
| Tensile/SEM/EDS data (U of Utah + 3D Powder Tech + high-T) | Phase II: multi-property qualification (fatigue, corrosion, creep) with autonomous characterization; data feeds national critical minerals databases |
| Atomizer setup (installed) + automated dispensing | Phase II: on-demand custom powder production enabling rapid alloy iteration; gas atomization scale-up via Valimet (letter of collaboration); automated feedstock preparation for high-throughput campaigns |
| TC AM Module simulations | Phase II: real-time CALPHAD-AM co-optimization with Thermo-Calc (letter of collaboration) integrated into pKGFN decision engine |

---

## Competitive Differentiation Notes

The proposal must distinguish FLAIME from related efforts by cited groups and others in the autonomous materials discovery space. Under Topic 3B (Critical Minerals), the key differentiator is that FLAIME is purpose-built for discovering critical-mineral-lean alloys through autonomous closed-loop experimentation — no competing effort integrates powder production, AM processing, multi-modal characterization, and qualification-relevant testing under a single AI-driven workflow targeting supply chain resilience:

- **vs. Arróyave et al. (TAMU, Alvi et al. 2026)**: Their deep GP-based cost-aware batch BO handles heterogeneous per-property evaluation costs through cost-weighted acquisition and heterotopic querying, but models the experimental campaign as a **single-stage multi-output problem** — all properties are measured on the same candidate, with cost variation across property types but not across sequential workflow stages. FLAIME's function-network models a fundamentally different cost structure: a **multi-stage directed acyclic graph (DAG)** where upstream decisions (CALPHAD screening at ~$0, powder atomization at ~$50–$200, LPBF builds at ~$500–$2,000) sequentially constrain downstream outcomes and where the optimizer can route queries through cheap computational stages before committing to expensive physical experiments. Their framework also does not capture how upstream process choices (composition, powder morphology) propagate uncertainty to downstream property measurements — the DAG structure of FLAIME explicitly models this multi-stage information flow. Additionally, their work does not address critical mineral substitution as an optimization objective.
- **vs. Roch et al. (Sabanza-Gil et al. 2025)**: Their multi-fidelity BO framework assumes a **single linear fidelity hierarchy** (low → medium → high). FLAIME handles a **DAG of fidelity sources** where multiple parallel characterization modalities (SEM, EDS, tensile) feed the same surrogate at different costs and precisions. Additionally, their work targets molecular/chemical systems where synthesis-to-measurement turnaround is minutes-to-hours; LPBF alloy campaigns have turnaround times of days-to-weeks, making cost-aware batch selection significantly more consequential.
- **vs. Priyadarshini et al. (2025)**: Their closed-loop MPEA discovery demonstrates the paradigm on a different alloy family using different characterization modalities. FLAIME's differentiation is the **explicit qualification pathway** — mechanical testing (tensile, fatigue) as optimization endpoints rather than hardness alone — and the integration of manufacturing constraints (printability, defect avoidance) as feasibility constraints in the optimizer. For Topic 3B, FLAIME additionally embeds **mineral-burden as an optimization objective**, directly targeting supply chain resilience rather than treating composition as unconstrained.
- **vs. general BO-for-AM**: Most existing work optimizes LPBF *process parameters* for a fixed alloy (e.g., Kavas et al. 2025). FLAIME jointly optimizes *composition and process* across the full manufacturing chain, which is a fundamentally harder problem requiring the multi-stage function-network architecture to tractably decompose.
- **vs. CMI Hub (Ames, ORNL)**: The Critical Materials Innovation Hub has demonstrated high-TRL success (e.g., Al-Ce alloys to TRL 9) using traditional experimental campaigns. FLAIME's contribution is **AI-accelerated discovery speed** — the closed-loop approach can explore the combinatorial alloy space significantly faster than manual sequential experimentation, while the pKGFN cost-awareness ensures efficient use of experimental budgets. *(ACTION ITEM: Insert quantified speed advantage from closed-loop demo. Target: Day 9. Owner: Computational lead.)*

---

## Edison Provenance Log

| Iteration | Task ID | Mode | Output Size | Citations | Purpose |
|---|---|---|---|---|---|
| 1 | `4a24aac6-6250-40d2-82a4-3ba76d08e682` | LITERATURE | ~35K chars | 6 | Mock PO/reviewer panel feedback |
| 2 | `5fc74ff4-cfcf-4053-93aa-c8652639060e` | LITERATURE | ~29K chars | 8 | Asset readiness assessment |
| 3 | `e494d39b-2540-400f-8a2b-8e7915a5b766` | LITERATURE | ~32K chars | 14 | Experimental capability evidence |
| 4 | `567c7816-efe8-4bfd-8385-1801cf48190d` | ANALYSIS | ~23K chars | — | Mock review round 1 (6.5/10 → improvements incorporated) |
| 5 | `97b09434-a1f8-4199-9de5-07bef9dbe976` | ANALYSIS | ~11K chars | — | Mock review round 2 (8.0/10 → final improvements incorporated) |
| 6 | `1e791f42-5ef6-4f93-8140-b1652f5fecbd` | ANALYSIS | ~16K chars | — | Mock review round 3 (7.0/10 → 5 issues addressed: Alvi mischaracterization fixed, figure budget corrected, critical minerals framing qualified, placeholders updated, Phase II budget verified) |
| 7 | `a039dc08-3e40-4964-8002-46e63b0e46b7` | ANALYSIS | ~8.5K chars | — | Mock review round 4 (8.0/10 → confirmed 5 prior issues resolved; 3 remaining issues addressed: figure numbering harmonized across all sections, Version A text updated to match Fig 1–3 + Table 1, reconciliation notes added) |
