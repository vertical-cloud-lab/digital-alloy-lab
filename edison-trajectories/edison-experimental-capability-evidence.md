> **⚠️ Archived/Raw Output (Pre-Pivot):** This file is a raw Edison Scientific output generated before the Topic 3B pivot. It was originally framed for "Topic 12 Focus Area F: Advanced Materials for Extreme Environments" and references partners/assumptions (e.g., University of Wisconsin) that no longer apply. The current roadmap targets **Topic 3B (Critical Minerals — AI-Enabled Materials Discovery, AMMTO)** with updated partnerships and evidence. Treat this as a historical input artifact, not current guidance. See `preliminary-results-roadmap.md` for the current synthesized roadmap.

Question: We are preparing a DOE Genesis Mission Phase I proposal (DE-FOA-0003612) for an AI-accelerated alloy discovery and qualification platform called FLAIME (targeting Topic 12 Focus Area F: Advanced Materials for Extreme Environments). The proposal deadline is April 28, 2026.

We need to strengthen our preliminary results section with EXPERIMENTAL CAPABILITY EVIDENCE to demonstrate that:
1. We won't have a steep learning curve — we already have hands-on experience with the key equipment and workflows.
2. We are capable of executing the proposed experimental plan.
3. We have infrastructure in place (not just computational/algorithmic work).

Specifically, we are planning to include the following experimental evidence that we expect to collect before the deadline:

A. **Ultrasonic atomizer setup**: Photos of the ultrasonic atomizer installed and operational in our lab. This is for custom powder production of novel alloy compositions.

B. **SEM (Scanning Electron Microscopy) images**: 
   - Powder morphology before and after ultrasonic atomization (showing sphericity, particle size distribution, satellite content)
   - Microstructure of solid LPBF-printed samples (showing grain structure, porosity, phase distribution)

C. **EDS (Energy-Dispersive X-ray Spectroscopy) data**: 
   - Compositional analysis and elemental mapping of powder and printed samples
   - Verification that target compositions are achieved

D. **Tensile test results**: 
   - Mechanical property data from 3D-printed (LPBF) samples produced at collaborating institutions (University of Utah, University of Wisconsin)
   - Stress-strain curves, yield strength, UTS, elongation data for baseline alloys (e.g., AlSi10Mg)

Please provide a detailed assessment structured as follows:

1. **Why experimental evidence matters for this type of proposal**: How DOE/AMMTO reviewers weigh lab-readiness and hands-on capability vs. purely computational preliminary results. What impression does it give when a proposal shows only algorithmic work vs. algorithmic + experimental evidence?

2. **Best practices for presenting each type of experimental evidence** (A through D above) in a DOE proposal preliminary results section:
   - What should each figure/image show and how should it be annotated?
   - What are the key quality indicators reviewers look for?
   - How to caption each figure for maximum impact?
   - Common pitfalls to avoid?

3. **How to frame experimental + computational integration**: How to narratively connect these experimental results to the BOFN/AI optimization framework — i.e., showing these aren't just standalone experiments but are inputs/outputs of the proposed closed-loop platform.

4. **Figure specifications**: For each of the 4 evidence types (A–D), specify:
   - Recommended figure layout (panels, annotations, scale bars)
   - Draft figure caption
   - Where it should appear in the proposal (which section)

5. **Priority ranking**: Rank these 4 experimental evidence types by their impact on proposal credibility and reviewer confidence, with reasoning.

6. **Risk assessment**: For each evidence type, what is the risk of NOT including it, and what is the minimum viable version if time/resources are constrained?

## Plan status
All objectives in the plan are completed, including a proposal-ready summary table artifact.

## 1) Why experimental evidence matters for this type of proposal
For AI-accelerated alloy discovery and qualification, experimental evidence is not “nice to have”; it is the credibility anchor that de-risks feasibility. Closed-loop discovery frameworks (Bayesian optimization/active learning) are fundamentally *data-driven*—the surrogate models are trained and updated from experimental synthesis and measurement, and the cycle fails without reliable, timely ground-truth data streams (bukkapatnam2023autonomousmaterialsdiscovery pages 7-8, priyadarshini2025machinelearningdrivenclosedloop pages 1-3). Reviews of autonomous materials discovery emphasize that purely computational approaches routinely fall short because (i) many computationally predicted materials are never physically realized and (ii) characterization/property estimation remains a central bottleneck; therefore proposals that demonstrate existing experimental infrastructure and validation are viewed as markedly more feasible (bukkapatnam2023autonomousmaterialsdiscovery pages 12-13, bukkapatnam2023autonomousmaterialsdiscovery pages 11-12).

For structural/alloy systems, this reviewer instinct is stronger: credible progress requires integrated synthesis + characterization + property measurement, because microstructure, composition, and defects mediate performance and are not reliably captured by purely in-silico surrogates at proposal time (miracle2021emergingcapabilitiesfor pages 2-4, miracle2021emergingcapabilitiesfor pages 24-26). High-throughput characterization reviews explicitly frame autonomous/closed-loop iteration as requiring multimodal experimental workflows (SEM/EBSD/EDS, etc.) with rapid feedback so that models can be updated frequently; they also highlight that moving closed-loop ideas from “easy-to-synthesize” systems into bulk structural alloys becomes plausible largely because of AM—*but only if defects and bulk-representative testing are addressed* (miracle2021emergingcapabilitiesfor pages 26-27).

**Reviewer impression delta:**
- **Algorithmic-only prelim results** tend to read like: “We have a promising optimizer/model; we still need to stand up the lab.” In closed-loop materials contexts, that triggers feasibility concerns because the core risk often lies in powder quality, print defects, composition drift/segregation, throughput, and property-testing latency—not the acquisition function (bukkapatnam2023autonomousmaterialsdiscovery pages 11-12).
- **Algorithmic + experimental prelim results** read like: “The loop is already partially closed; we can generate feedstock, print/characterize parts, and produce property endpoints.” This directly answers readiness and execution risk—especially when the evidence demonstrates traceability and measurement competence rather than one-off images (miracle2021emergingcapabilitiesfor pages 26-27, bukkapatnam2023autonomousmaterialsdiscovery pages 12-13).

## 2) Best practices for presenting each type of experimental evidence (A–D)
### General principles (apply to all A–D)
1. **Traceability is a feature:** Every figure should include sample IDs, dates/batch numbers, and a short “conditions box” (e.g., atomization atmosphere; LPBF key parameters; tensile standard/orientation). Reviewers read traceability as “this group runs experiments like a qualification program.”
2. **Quantify alongside images:** For powders and microstructures, pair “representative images” with at least 2–4 quantitative metrics (PSD d10/d50/d90; sphericity/circularity; satellite fraction; relative density/porosity). Powder studies emphasize that morphology and PSD influence flow/spreadability and can map into part density and properties (brika2020influenceofparticle pages 1-5, brika2020influenceofparticle pages 5-8).
3. **Show the whole chain at least once:** Even if each evidence type is separate, reviewers gain confidence when a single mini-story connects “powder → print → characterize → property.” Autonomous discovery reviews emphasize integrated workflows as the credibility core (miracle2021emergingcapabilitiesfor pages 26-27, miracle2021emergingcapabilitiesfor pages 24-26).

### A. Ultrasonic atomizer setup (photos)
**What it should show / annotations**
- A wide shot proving installation in your lab (not vendor stock), plus at least one labeled close-up of the working zone (melt delivery/nozzle/transducer), powder collection, and inerting/safety enclosure.
- Add a small text box with: “Installed (date), operational (Y/N), first alloy run (planned/complete), atmosphere (Ar/N2), collection method.”

**Key quality indicators reviewers look for**
- Operational readiness (installed, plumbed, inert gas, collection, safety) rather than “unboxed.”
- Evidence you understand powder risks (oxidation, fines, contamination control), which strongly affect downstream LPBF properties (meier2022influenceofpowder pages 1-3).

**Caption tactics**
- Make the caption explicitly about *risk reduction and cycle time*: “enables custom powders for rapid AI-guided iterations.”

**Common pitfalls**
- Unannotated glamour photo.
- No explicit statement that it is operational (or what “operational” means).

### B. SEM images (powder + printed microstructure)
**What it should show / annotations**
- Powder before/after atomization: identical magnification (or clearly stated) with scale bars; annotate satellites/agglomerates and typical particle shapes.
- Printed microstructure: at least one cross-section at low magnification showing porosity/melt-track features plus one higher-magnification region; add scale bars and build direction indicator.

**Key quality indicators**
- Scale bars, representative fields of view, and a quantitative tie-in to powder suitability: studies connect spherical morphology and controlled fine fraction to improved flowability/packing and ultimately printed density (brika2020influenceofparticle pages 1-5, brika2020influenceofparticle pages 5-8).
- If you can, include density/porosity quantification or a simple “porosity class” statement.

**Caption tactics**
- Use the caption to assert that SEM is a *measurement node* in the closed loop, not just imagery. Closed-loop alloy discovery papers explicitly treat SEM/EDS as part of the loop’s validation and model updating (priyadarshini2025machinelearningdrivenclosedloop pages 1-3).

**Common pitfalls**
- Missing scale bars, unclear sample state (powder vs part), or cherry-picked “best-looking” micrographs.

### C. EDS data (composition + mapping)
**What it should show / annotations**
- A target-vs-measured composition summary (bar chart/table) for both powder and printed samples.
- At least one elemental map (or RGB overlay) that addresses a reviewer’s immediate question: segregation? contamination? element loss?

**Key quality indicators**
- Acknowledge and manage EDS limitations: some features/phases (e.g., nanoscale precipitates) cannot be fully identified/quantified by EDS alone; this is explicitly noted in AM microstructure work (dryepondt2023prioritizationofexisting pages 44-49).
- If you report quantitative values, include a short note on whether results are standardless or calibrated and what uncertainty you expect.

**Caption tactics**
- Make explicit that composition verification is what prevents “optimizer hallucination” and provides ground truth for the surrogate model (bukkapatnam2023autonomousmaterialsdiscovery pages 7-8, bukkapatnam2023autonomousmaterialsdiscovery pages 12-13).

**Common pitfalls**
- Overclaiming phase ID from EDS maps.
- No comparison to targets (reviewers cannot tell if it’s “good”).

### D. Tensile test results (from Utah/Wisconsin partners)
**What it should show / annotations**
- At least one stress–strain curve and a summary table with YS/UTS/elongation. If possible, show replicate curves or error bars.
- Explicitly state: printing site, build orientation, post-processing, and test standard. (Even if not all details fit in the figure, include them in caption/footnote.)

**Key quality indicators**
- Traceability and context: orientation and heat treatment matter; tensile results are influenced by chemistry (e.g., oxygen) and defects, which is why connecting tensile endpoints back to powder and microstructure is powerful (meier2022influenceofpowder pages 1-3).

**Caption tactics**
- Emphasize “qualification-relevant endpoint” and that this closes the loop from composition/process to property (miracle2021emergingcapabilitiesfor pages 26-27, miracle2021emergingcapabilitiesfor pages 24-26).

**Common pitfalls**
- Single specimen with no context.
- Presenting collaborator data without clearly defining what you controlled vs what they controlled.

## 3) How to frame experimental + computational integration (closed-loop narrative)
A strong narrative is to treat each evidence type as a **contracted interface** in the closed loop:

1. **Design / BOFN step (computational):** BOFN proposes (composition, process window, uncertainty-aware next experiments). Autonomous discovery reviews highlight that BO/GPR-type surrogates are effective precisely in low-data, high-cost experimental regimes (bukkapatnam2023autonomousmaterialsdiscovery pages 7-8, priyadarshini2025machinelearningdrivenclosedloop pages 1-3).
2. **Synthesis (A):** ultrasonic atomizer produces powders for candidate compositions—this is how the design becomes physically realizable and repeatable.
3. **Qualification of inputs (B,C):** SEM + EDS verify that the *intended* inputs to LPBF are real (powder morphology, composition) and detect failure modes early (satellites, contamination, segregation), preventing wasted build/test cycles. Powder morphology/PSD and chemistry are repeatedly linked to downstream print quality and properties (brika2020influenceofparticle pages 1-5, brika2020influenceofparticle pages 5-8).
4. **LPBF build + microstructure QC (B,C):** printed coupons are assessed for porosity/microstructural state and composition integrity; this data populates the process–structure part of the PSP mapping that AMDM reviews emphasize (bukkapatnam2023autonomousmaterialsdiscovery pages 7-8, bukkapatnam2023autonomousmaterialsdiscovery pages 11-12).
5. **Property endpoint (D):** tensile tests provide the “objective function” for optimization and the reviewer-legible evidence that the platform can move toward qualification. Structural-alloys closed-loop reviews emphasize that property testing is essential to make AI-guided discovery credible (miracle2021emergingcapabilitiesfor pages 26-27, miracle2021emergingcapabilitiesfor pages 24-26).

In text, explicitly state that **every experiment updates the surrogate** (with uncertainty), and that QC thresholds (e.g., composition deviation, porosity limits, satellite fraction) become feasibility constraints in BOFN (constraint-aware optimization), consistent with literature emphasizing constraints and feasibility in closed-loop alloy discovery (priyadarshini2025machinelearningdrivenclosedloop pages 1-3).

## 4) Figure specifications (layout, captions, placement)
The table below provides proposal-ready figure specs, captions, and placement suggestions for A–D.

| Evidence type | Purpose / reviewer question answered | What to show (minimum) | Key quality indicators / QC | Suggested layout | Draft caption (1–2 sentences) | Proposal placement | MVP if constrained | Risk if omitted |
|---|---|---|---|---|---|---|---|---|
| A. Ultrasonic atomizer setup | Demonstrates hands-on infrastructure is already installed and being operated; answers “Do they actually have the hardware and know how to use it, or is this still aspirational?” Closed-loop AMDM platforms require real synthesis hardware, not only algorithms (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11, bukkapatnam2023autonomousmaterialsdiscovery pages 12-13, bukkapatnam2023autonomousmaterialsdiscovery pages 11-12). | 1 installed full-system photo; 1 close-up of crucible/nozzle/transducer; labels for powder feed path, inert gas, collection chamber, safety enclosure; if possible, one image of first powder batch collected. | Clear operational status; labeled components; evidence of in-lab installation; date/sample ID; if available, first operating conditions (e.g., atmosphere, power, alloy feedstock) and safe enclosed setup. | 2–3 panels: (a) full setup, (b) labeled close-up, (c) optional first powder batch vial/tray. Use arrows and short callouts, not dense text. | `Ultrasonic atomization capability now installed and operational in the FLAIME experimental workflow. This in-house powder-production node enables rapid generation of custom alloy feedstocks for AI-guided design iterations and reduces execution risk at project start.` | Preliminary Results or Facilities/Resources; also reference in Technical Approach workflow figure. | One strong annotated photo of installed system plus one sentence stating operational status and intended first alloy. | Reviewers may infer a steep startup curve, dependence on future procurement/training, or that powder production is not yet real. |
| B. SEM images | Shows ability to characterize powder quality and printed microstructure; answers “Can they evaluate whether their powders and builds are actually suitable for LPBF?” SEM-based morphology/microstructure data are core to structural-materials screening and closed-loop downselection (miracle2021emergingcapabilitiesfor pages 26-27, miracle2021emergingcapabilitiesfor pages 2-4, miracle2021emergingcapabilitiesfor pages 24-26, sutton2017powdercharacterisationtechniques pages 1-3). | Powder-before vs powder-after SEM images with scale bars; at least one solid-sample cross-section image from LPBF coupon showing melt tracks/grains/porosity; annotate spherical particles, satellites, pores, or representative microstructural regions. | Scale bars; good contrast/focus; representative fields of view; sample IDs; quantitative companion metrics if possible: PSD d10/d50/d90, sphericity/circularity, satellite fraction, relative density/porosity estimate; note orientation and sample prep. | 4 panels: (a) precursor powder, (b) atomized powder, (c) low-mag printed cross-section, (d) higher-mag microstructure/defect region. Add small inset with 2–3 bullet metrics. | `SEM confirms that FLAIME can both assess feedstock quality and interrogate as-built LPBF microstructures. The observed particle sphericity/satellite content and printed microstructural features establish readiness for powder-to-part experimental iterations.` | Preliminary Results, immediately after workflow overview; cross-reference Experimental Plan task on characterization. | One powder SEM and one printed-sample SEM with scale bars and concise annotations. | Without SEM evidence, the proposal can look algorithm-heavy and weak on materials characterization, especially for extreme-environment alloy qualification. |
| C. EDS data | Demonstrates composition verification and elemental-mapping capability; answers “Can they confirm that designed compositions were actually made and identify segregation/contamination?” Quantitative composition mapping is essential to ground-truth model inputs/outputs (bukkapatnam2023autonomousmaterialsdiscovery pages 7-8, miracle2021emergingcapabilitiesfor pages 2-4, kennedy2019additivemanufacturingassessing pages 13-13). | At minimum, one quantitative spectrum/table for powder and one for printed sample; one elemental map set (or RGB overlay) showing key alloying elements; include target vs measured composition comparison. | Report acquisition conditions or note standardless/standardized method; sample IDs; map scale; clear elemental labels; quantify deviation from target composition; mention uncertainty/caveats for light elements and small features; avoid overclaiming nanoscale phase ID from EDS alone (dryepondt2023prioritizationofexisting pages 44-49). | 3 panels: (a) target vs measured composition bar/table, (b) powder elemental map, (c) printed coupon elemental map/overlay. Keep color legend consistent across maps. | `EDS verifies that designed alloy chemistries are being achieved in both powder and printed states and provides elemental distributions for model updating. These data form a direct experimental input to FLAIME’s Bayesian optimization loop by distinguishing successful synthesis from composition drift or segregation.` | Preliminary Results, paired directly with SEM figure or as a combined SEM/EDS figure. | One target-vs-measured composition table and one elemental overlay map from a representative sample. | If omitted, reviewers may doubt that nominal AI-suggested compositions can be manufactured reproducibly or that the team can detect chemistry drift/segregation. |
| D. Tensile tests | Provides property evidence and qualification relevance; answers “Can the team connect process/composition to mechanical performance, not just microstructure?” High-throughput/closed-loop structural-alloy discovery ultimately requires property validation, and tensile data are the most reviewer-legible proof point (miracle2021emergingcapabilitiesfor pages 26-27, miracle2021emergingcapabilitiesfor pages 24-26, meier2022influenceofpowder pages 1-3). | At minimum, 1–2 representative stress–strain curves from LPBF baseline alloy specimens (e.g., AlSi10Mg) plus summary table of YS, UTS, elongation; state printing site, specimen orientation, post-processing, and test standard if known. | Replicates if possible; orientation and heat-treatment traceability; specimen geometry/standard (e.g., ASTM E8/E8M if applicable); sample count; error bars/range; identify collaborating institution and who generated data; avoid unsupported claims from a single specimen. | 2 panels: (a) stress–strain curves, (b) bar chart/table of YS/UTS/elongation by material/orientation/site. Include concise footnote with processing/test conditions. | `Baseline LPBF tensile data from collaborating institutions establish that FLAIME is anchored to measurable qualification-relevant properties, not solely predicted rankings. These results provide the property-assessment endpoint for the proposed closed-loop composition–process–microstructure–performance optimization.` | Preliminary Results near end of section, or Validation/Qualification subsection; also cite in Team/Partnerships section. | One stress–strain curve plus a 3-metric summary table from a trusted collaborator for a baseline alloy. | Highest credibility loss if omitted: reviewers may conclude the platform is discovery-only, not qualification-capable, and lacks evidence of property-measurement execution. |


*Table: This table summarizes the most useful proposal-ready evidence types A–D, including what each should show, the reviewer question it answers, quality indicators, suggested layout, and fallback minimum versions. It is useful for prioritizing late-stage data collection before the DOE Genesis Phase I deadline.*

## 5) Priority ranking (impact on credibility)
1. **D. Tensile tests (highest impact):** Directly demonstrates a qualification-relevant endpoint and that the team can execute (or already has executed via partners) the property measurement leg of the loop. Closed-loop structural materials reviews emphasize that property validation is essential for credible autonomous discovery (miracle2021emergingcapabilitiesfor pages 26-27, miracle2021emergingcapabilitiesfor pages 24-26).
2. **B. SEM images:** SEM is the fastest, most reviewer-recognizable proof that you can evaluate powder suitability and printed defects/microstructure—key risks in LPBF and extreme-environment alloys (miracle2021emergingcapabilitiesfor pages 26-27, brika2020influenceofparticle pages 1-5).
3. **C. EDS data:** Composition verification is critical to validate that AI-suggested alloys are actually achieved and to detect segregation/contamination; AMDM literature emphasizes experimental validation and measurement fusion (bukkapatnam2023autonomousmaterialsdiscovery pages 12-13, bukkapatnam2023autonomousmaterialsdiscovery pages 11-12).
4. **A. Atomizer setup photo:** Important feasibility signal (infrastructure exists), but it is less compelling than data showing that powders/parts/properties meet measurable targets.

## 6) Risk assessment + minimum viable versions
- **A (Atomizer photos):**
  - **Risk if omitted:** looks like powder production is aspirational; raises steep-startup concern and dependence on procurement/training.
  - **MVP:** one annotated in-lab photo + one sentence “installed and operational” + planned first alloy run.
- **B (SEM):**
  - **Risk if omitted:** reviewers doubt your ability to diagnose powder/LPBF defects; proposal can read as algorithm-first with weak materials characterization capability (miracle2021emergingcapabilitiesfor pages 26-27, bukkapatnam2023autonomousmaterialsdiscovery pages 11-12).
  - **MVP:** two powder micrographs (before/after) + one printed cross-section micrograph, all with scale bars.
- **C (EDS):**
  - **Risk if omitted:** reviewers may doubt you can confirm compositions and detect chemistry drift/segregation—critical in alloy discovery and qualification (bukkapatnam2023autonomousmaterialsdiscovery pages 12-13).
  - **MVP:** target-vs-measured composition table for one powder batch and one printed coupon + one elemental overlay map.
- **D (Tensile):**
  - **Risk if omitted:** highest—proposal may be perceived as discovery-only, not qualification-capable; lacks evidence that the platform reaches property endpoints (miracle2021emergingcapabilitiesfor pages 24-26).
  - **MVP:** one stress–strain curve + summary table for YS/UTS/elongation for a baseline LPBF alloy from a named collaborator, with orientation and post-processing noted.

## Implementation note (to strengthen “no steep learning curve”)
For each evidence type, explicitly add a one-line “operator competency” statement that is still technical (not narrative), e.g., “Operators have executed N sample prep runs and established a standard operating procedure for sample mounting/polishing and SEM/EDS acquisition,” plus a QC checklist. This aligns with AMDM reviews emphasizing that robust infrastructure and bottleneck-aware characterization workflows are what make closed-loop systems feasible beyond proofs-of-concept (bukkapatnam2023autonomousmaterialsdiscovery pages 11-12, miracle2021emergingcapabilitiesfor pages 26-27).

References

1. (bukkapatnam2023autonomousmaterialsdiscovery pages 7-8): Satish T.S. Bukkapatnam. Autonomous materials discovery and manufacturing (amdm): a review and perspectives. IISE Transactions, 55:75-93, Aug 2023. URL: https://doi.org/10.1080/24725854.2022.2089785, doi:10.1080/24725854.2022.2089785. This article has 26 citations.

2. (priyadarshini2025machinelearningdrivenclosedloop pages 1-3): Maitreyee Sharma Priyadarshini, Edwin Gienger, Jarett Ren, Bianca Piloseno, Elizabeth A Pogue, Paul K. Lambert, Jesse S. Ko, and Paulette Clancy. Machine learning-driven closed-loop discovery of hard multiple principal element alloys. ChemRxiv, Aug 2025. URL: https://doi.org/10.26434/chemrxiv-2025-klz0c, doi:10.26434/chemrxiv-2025-klz0c. This article has 0 citations.

3. (bukkapatnam2023autonomousmaterialsdiscovery pages 12-13): Satish T.S. Bukkapatnam. Autonomous materials discovery and manufacturing (amdm): a review and perspectives. IISE Transactions, 55:75-93, Aug 2023. URL: https://doi.org/10.1080/24725854.2022.2089785, doi:10.1080/24725854.2022.2089785. This article has 26 citations.

4. (bukkapatnam2023autonomousmaterialsdiscovery pages 11-12): Satish T.S. Bukkapatnam. Autonomous materials discovery and manufacturing (amdm): a review and perspectives. IISE Transactions, 55:75-93, Aug 2023. URL: https://doi.org/10.1080/24725854.2022.2089785, doi:10.1080/24725854.2022.2089785. This article has 26 citations.

5. (miracle2021emergingcapabilitiesfor pages 2-4): Daniel B. Miracle, Mu Li, Zhaohan Zhang, Rohan Mishra, and Katharine M. Flores. Emerging capabilities for the high-throughput characterization of structural materials. Annual Review of Materials Research, 51:131-164, Jul 2021. URL: https://doi.org/10.1146/annurev-matsci-080619-022100, doi:10.1146/annurev-matsci-080619-022100. This article has 79 citations and is from a domain leading peer-reviewed journal.

6. (miracle2021emergingcapabilitiesfor pages 24-26): Daniel B. Miracle, Mu Li, Zhaohan Zhang, Rohan Mishra, and Katharine M. Flores. Emerging capabilities for the high-throughput characterization of structural materials. Annual Review of Materials Research, 51:131-164, Jul 2021. URL: https://doi.org/10.1146/annurev-matsci-080619-022100, doi:10.1146/annurev-matsci-080619-022100. This article has 79 citations and is from a domain leading peer-reviewed journal.

7. (miracle2021emergingcapabilitiesfor pages 26-27): Daniel B. Miracle, Mu Li, Zhaohan Zhang, Rohan Mishra, and Katharine M. Flores. Emerging capabilities for the high-throughput characterization of structural materials. Annual Review of Materials Research, 51:131-164, Jul 2021. URL: https://doi.org/10.1146/annurev-matsci-080619-022100, doi:10.1146/annurev-matsci-080619-022100. This article has 79 citations and is from a domain leading peer-reviewed journal.

8. (brika2020influenceofparticle pages 1-5): Salah Eddine Brika, Morgan Letenneur, Christopher Alex Dion, and Vladimir Brailovski. Influence of particle morphology and size distribution on the powder flowability and laser powder bed fusion manufacturability of ti-6al-4v alloy. Additive manufacturing, 31:100929, Jan 2020. URL: https://doi.org/10.1016/j.addma.2019.100929, doi:10.1016/j.addma.2019.100929. This article has 529 citations and is from a highest quality peer-reviewed journal.

9. (brika2020influenceofparticle pages 5-8): Salah Eddine Brika, Morgan Letenneur, Christopher Alex Dion, and Vladimir Brailovski. Influence of particle morphology and size distribution on the powder flowability and laser powder bed fusion manufacturability of ti-6al-4v alloy. Additive manufacturing, 31:100929, Jan 2020. URL: https://doi.org/10.1016/j.addma.2019.100929, doi:10.1016/j.addma.2019.100929. This article has 529 citations and is from a highest quality peer-reviewed journal.

10. (meier2022influenceofpowder pages 1-3): Benjamin Meier, Fernando Warchomicka, Jelena Petrusa, Paul Angerer, Jaroslaw Wosik, Reinhard Kaindl, Vojislav Petrovic, Wolfgang Waldhauser, and Christof Sommitsch. Influence of powder production process and properties on material properties of ti6al4v manufactured by l-pbf. The International Journal of Advanced Manufacturing Technology, 123:1577-1588, Oct 2022. URL: https://doi.org/10.1007/s00170-022-10250-y, doi:10.1007/s00170-022-10250-y. This article has 13 citations.

11. (dryepondt2023prioritizationofexisting pages 44-49): Sebastien Dryepondt, Stephen Taller, Fred List III, Zackary Snow, Michael McMurtrey, Michael Moorehead, Michael Mulholland, Srinivas Mantri, Xuan Zhang, Subhashish Meher, Chinthaka Silva, Mohan Nartu, Ankit Roy, William Frazier, Mageswari Komarasamy, Tanvi Ajantiwalay, Shalini Tripathi, Nathan Canfield, and Isabella van Rooyen. Prioritization of existing reactor materials. ArXiv, Sep 2023. URL: https://doi.org/10.2172/2345330, doi:10.2172/2345330. This article has 2 citations.

12. (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11): Satish T.S. Bukkapatnam. Autonomous materials discovery and manufacturing (amdm): a review and perspectives. IISE Transactions, 55:75-93, Aug 2023. URL: https://doi.org/10.1080/24725854.2022.2089785, doi:10.1080/24725854.2022.2089785. This article has 26 citations.

13. (sutton2017powdercharacterisationtechniques pages 1-3): Austin T. Sutton, Caitlin S. Kriewall, Ming C. Leu, and Joseph W. Newkirk. Powder characterisation techniques and effects of powder characteristics on part properties in powder-bed fusion processes. Virtual and Physical Prototyping, 12:29-3, Jan 2017. URL: https://doi.org/10.1080/17452759.2016.1250605, doi:10.1080/17452759.2016.1250605. This article has 462 citations and is from a peer-reviewed journal.

14. (kennedy2019additivemanufacturingassessing pages 13-13): Stephen K. Kennedy, Amber M. Dalley, and Gregory J. Kotyk. Additive manufacturing: assessing metal powder quality through characterizing feedstock and contaminants. Journal of Materials Engineering and Performance, 28:728-740, Jan 2019. URL: https://doi.org/10.1007/s11665-018-3841-5, doi:10.1007/s11665-018-3841-5. This article has 19 citations and is from a peer-reviewed journal.