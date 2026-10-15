# Robotic SDL Automation — Edison Literature Review

**Date:** 2026-04-14
**Edison Task ID:** 9c0e015b-3302-45f0-8a5f-d554b01079cf

---

Question: Survey the current state of robotic integration in self-driving laboratories (SDLs) for structural materials discovery and additive manufacturing. Specifically address:

1. What self-driving laboratory platforms exist for metals/alloys discovery that include physical robotic automation (not just AI-directed experiment selection)?
2. How far has any lab progressed toward fully automated powder-to-mechanical-property pipelines for additive manufacturing (LPBF, DED, etc.)?
3. What are the most challenging physical automation steps in a materials discovery pipeline? Consider: powder dispensing/mixing, loading into AM machines, post-build cleaning of AM systems, specimen extraction from build plates (wire EDM, machining), transfer between instruments (atomizer → printer → testing machine → SEM), automated polishing for metallographic prep, and automated mechanical testing.
4. How do existing SDL platforms (A-Lab at LBNL, ORNL Peregrine, Radical AI, Emerald Cloud Lab, CMU Cloud Lab) distinguish between AI-autonomous decision-making and physically autonomous robotic execution?
5. What is the typical TRL progression from human-operated-AI-directed (Phase I scale) to fully robotic SDL (Phase II+ scale) in DOE/NSF-funded materials programs?
6. Are there any examples of labs that have achieved fully autonomous (no human physical intervention) closed-loop materials discovery for structural/mechanical properties (not just thin films, catalysts, or organic synthesis)?

## Technical Survey: Robotic integration in self‑driving laboratories (SDLs) for structural materials discovery and additive manufacturing

This survey focuses on *physically embodied* automation (robotic execution of synthesis/processing/characterization), and distinguishes it from AI/ML that only recommends experiments. Evidence in the retrieved corpus is strongest for (i) a fully robotic solid‑state powder synthesis SDL (A‑Lab), (ii) an in‑progress robotic alloy/AM SDL (APEX), (iii) AM “digital thread”/monitoring autonomy (Peregrine), and (iv) individual automated modules (robotic mechanical testing, closed‑loop AM repair), rather than any fully automated powder‑to‑mechanical‑property pipeline for metal AM.

| Platform (institution) | Materials domain | Physical robotic automation (what hardware executes) | AI/autonomy layer (what decisions automated) | Demonstrated closed-loop target property | Key manual interventions/limitations |
|---|---|---|---|---|---|
| APEX (LLNL/Cornell) | Structural alloys / metal AM via directed-energy deposition | Robotics executes DED 3D printing, grinding/polishing, microscopy, hardness indentation, and compression testing; vibration sensors added to emulate human “feel” during grinding (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) | ML agent learns from prior experiments; MAP integrates models (e.g., hardness/ductility) and updates designs autonomously for next alloy builds (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) | Mechanical-response-focused loop: hardness, compression behavior, and broader alloy-property optimization are explicit targets (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) | Strongest evidence for robotic structural-alloy SDL in context, but evidence is program/profile level rather than a peer-reviewed end-to-end validation paper; no evidence yet of fully autonomous powder handling, AM machine cleaning, or specimen extraction from build plates (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) |
| A-Lab (LBNL) | Inorganic powders (oxides, phosphates); relevant to powder robotics, not structural metals/alloys | Quantos dispenser-balance for powder dosing; dual asymmetric centrifuge for mixing; automated pipettor; Mitsubishi robot arm + UR5e arms for transfer; furnaces for heating; automated powder recovery/XRD loading and measurement (szymanski2024automatingthesynthesis pages 78-80, szymanski2023anautonomouslaboratory pages 7-7, szymanski2024automatingthesynthesis pages 80-83, szymanski2023anautonomouslaboratory pages 2-3) | ML/text-mined recipe generation, active learning (ARROWS), CNN/Rietveld analysis, API-driven job submission; sustained autonomous campaigns over 17 days (szymanski2023anautonomouslaboratory pages 1-2, szymanski2023anautonomouslaboratory pages 2-3) | Closed loop is on synthesis success / phase purity from XRD, not structural or mechanical properties (szymanski2023anautonomouslaboratory pages 1-2, szymanski2023anautonomouslaboratory pages 2-3) | Manual precursor/consumable loading before campaigns; XRD holder cleaning/refill; some poor-fit analyses require manual review; limited to air-stable targets (szymanski2023anautonomouslaboratory pages 7-7, szymanski2024automatingthesynthesis pages 80-83) |
| Peregrine (ORNL) | Powder-bed AM monitoring / digital thread for AM qualification | Primarily software-driven acquisition/analysis of layer-wise imaging and metadata; may trigger UI macros for interventions, but no evidence here of robot manipulators or physical workcell automation (scime2020developmentofmonitoring pages 35-39, scime2020developmentofmonitoring pages 30-35, cooper2023unifiedsoftwarearchitecture pages 6-10) | Autonomous/real-time anomaly detection, data capture, metadata tracking, image analysis, remote monitoring; some potential for process intervention via software macros (scime2020developmentofmonitoring pages 35-39, scime2020developmentofmonitoring pages 30-35, scime2020developmentofmonitoring pages 25-30) | Closed-loop target is process quality/anomaly detection during AM, not a demonstrated no-human powder-to-mechanical-property loop (scime2020developmentofmonitoring pages 35-39, scime2020developmentofmonitoring pages 30-35) | Primarily software/analytics platform; evidence does not support robotic execution of loading, cleaning, extraction, polishing, or mechanical testing (scime2020developmentofmonitoring pages 35-39, cooper2023unifiedsoftwarearchitecture pages 6-10, scime2020developmentofmonitoring pages 39-42) |
| HT-READ (UC San Diego) | High-throughput alloy development using AM-built discrete libraries | AM prints ring-shaped discrete sample libraries in a metallurgical mount sized for downstream XRD, SEM/EDS, EBSD; automation-friendly geometry emphasized, but specific robotic post-processing hardware is not detailed in the cited excerpt (vecchio2021highthroughputrapidexperimental pages 1-4) | AI agent connects composition to properties and uses new experimental data in a closed-loop screening framework (vecchio2021highthroughputrapidexperimental pages 1-4) | Closed-loop alloy screening/property mapping concept is explicit, but cited excerpt does not provide a specific demonstrated mechanical-property optimization result (vecchio2021highthroughputrapidexperimental pages 1-4) | Evidence is limited on robot hardware for polishing/testing/extraction; excerpt supports integrated closed-loop framework more than a fully robotic autonomous lab (vecchio2021highthroughputrapidexperimental pages 1-4) |
| Emerald Cloud Lab / CMU Cloud Lab | General cloud-lab automation; not specific to structural materials or metal AM | Robotic instruments perform physical execution such as liquid transfers, sequencing, X-ray measurements, repetitive sample handling, and purification; researchers program remotely (castellanosUnknownyearcarnegiemellonsclouda pages 1-4, castellanosUnknownyearcarnegiemellonscloud pages 1-4, arias2024scientificdiscoveryat pages 1-2) | Humans or AI can specify protocols/experiment selection; cloud-lab robots execute them; current cloud labs are often open-loop because humans still specify protocol details, though AI-driven optimization can sit above the execution layer (frisby2021asynchronousparallelbayesian pages 1-2, tobias2025autonomousselfdrivinglaboratoriesab pages 1-2, arias2024scientificdiscoveryat pages 1-2) | No structural-materials/mechanical-property closed loop shown in context; role is best understood as remote robotic execution infrastructure (frisby2021asynchronousparallelbayesian pages 1-2, arias2024scientificdiscoveryat pages 1-2) | On-site staff may still handle equipment/manual tasks; not evidence for autonomous powder AM, metallography, or structural-property pipelines (zilgalvis2025yingchiangjeffreylee pages 6-9, zilgalvis2025yingchiangjeffreyleea pages 6-9) |
| Robot-assisted mechanical testing (Roth et al.) | AM structural materials (SLM/cast AlSi10Mg) | Robot-assisted universal testing machine with 6-axis robot, specimen stacks, pneumatic wedge grips, and imaging system; >360 experiments on extracted flat specimens (roth2021plasticityandfracture pages 2-3, roth2021plasticityandfracture pages 1-2, roth2021plasticityandfracture pages 10-12) | Automation is in specimen handling/testing throughput and data collection; no evidence in context that AI autonomously selected next AM builds (roth2021plasticityandfracture pages 2-3, roth2021plasticityandfracture pages 1-2) | Mechanical properties directly measured at scale (uniaxial tension, shear/tension fracture; build-height dependent hardening characterized) (roth2021plasticityandfracture pages 1-2, roth2021plasticityandfracture pages 10-12) | Important downstream module rather than full SDL: specimen extraction from AM parts occurred upstream, and no closed-loop build→test→redesign autonomy is shown in cited evidence (roth2021plasticityandfracture pages 1-2, roth2021plasticityandfracture pages 10-12) |


*Table: This table compares the main platforms and modules relevant to structural materials discovery and additive manufacturing, separating physical robotic execution from AI/autonomy layers. It is useful for identifying which systems are truly robotic SDLs, which are mainly analytics or cloud-execution infrastructure, and where key manual gaps remain.*

### 1. Robotic SDL platforms for metals/alloys discovery (physical automation present)

**APEX (LLNL/Cornell) — autonomous alloy discovery with DED and automated mechanical characterization.**  
The strongest structural‑metals example in the retrieved set is APEX (Autonomous Alloy Prediction and EXperimentation), described as a self‑driving laboratory that uses **robotics + ML** to design, additively manufacture via **directed energy deposition (DED)**, and then **grind/polish and mechanically characterize** alloy coupons (microscopy, hardness indentation, compression testing), targeting high throughput (e.g., “upwards of 48 samples/day”). (conn2025selfdrivinglabto pages 1-8) The description explicitly frames a closed-loop design→build→test concept in which results are fed into a Materials Acceleration Platform (MAP) to design subsequent alloys. (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8)

**HT-READ — integrated closed-loop alloy development framework using AM-built sample libraries.**  
HT‑READ (High‑Throughput Rapid Experimental Alloy Development) describes an integrated closed‑loop screening workflow in which additive manufacturing is used to produce **libraries of discrete alloy specimens** (e.g., ring of 16 specimens in a single metallographic mount) sized to enable high‑throughput downstream characterization (XRD, SEM/EDS, EBSD). (vecchio2021highthroughputrapidexperimental pages 1-4) The excerpt supports an integrated framework linking AM sample creation and property mapping with an AI agent, but it does not provide detailed evidence of robotic post-processing hardware or a fully unattended pipeline in the cited section. (vecchio2021highthroughputrapidexperimental pages 1-4)

**A‑Lab is highly relevant as a *powder‑robotics* SDL, but it is not an alloys/mechanical‑property SDL.**  
A‑Lab demonstrates a “fully automated sequence” from solid precursors through processing and XRD characterization, including robotic powder dosing/mixing/heating and ML interpretation, but its materials domain is oxides/phosphates (not structural alloys) and its loop targets phase formation/purity rather than mechanical properties. (szymanski2023anautonomouslaboratory pages 1-2, szymanski2023anautonomouslaboratory pages 2-3)

### 2. Progress toward fully automated powder‑to‑mechanical‑property pipelines for metal AM (LPBF, DED, etc.)

**No retrieved source demonstrates a fully automated, no-human-physical-intervention, powder→AM build→specimen prep→mechanical test→model update loop for metal AM.**  
The closest conceptually is APEX, which targets an autonomous design→DED printing→surface preparation→mechanical characterization loop for alloys. (conn2025selfdrivinglabto pages 1-8) However, the same description makes clear it is still being developed and monitored during runs (not demonstrated as a fully unattended pipeline), and it does not document automation of notoriously difficult AM shop‑floor steps such as powder logistics, AM machine cleaning, or build‑plate specimen extraction. (conn2025selfdrivinglabto pages 1-8)

**Peregrine at ORNL is “autonomous” mainly in sensing/analytics, not in full powder-to-property execution.**  
Peregrine is documented as an ORNL **Python software tool** that performs layer-wise anomaly detection and, in its “fullest implementation,” can autonomously collect/analyze layer-wise imaging data, issue alerts, and potentially execute UI macros for “process interventions.” (scime2020developmentofmonitoring pages 35-39) The evidence supports a **digital-thread / monitoring autonomy** capability rather than robotic handling, post-build extraction, or mechanical testing automation. (scime2020developmentofmonitoring pages 35-39, cooper2023unifiedsoftwarearchitecture pages 6-10)

**Downstream mechanical testing can be automated at scale once specimens exist.**  
A concrete, high-maturity downstream module is robot-assisted mechanical testing for AM materials: a robot-assisted testing system executed **>360** mechanical experiments on specimens extracted from cast and selective-laser-melted (SLM) AlSi10Mg, demonstrating that high-throughput *testing* can be robotized even if upstream specimen extraction remains separate. (roth2021plasticityandfracture pages 1-2, roth2021plasticityandfracture pages 2-3)

**Closed-loop AM control/repair can improve mechanical properties in non-metal (extrusion) demonstrations.**  
A robotic layer-wise closed-loop AM system (extrusion) with in-situ inspection and repair reduced defect volume and increased breaking load from 4.77 kN to 6.31 kN. (singh2023towardclosedloopadditive pages 1-2) This is a compelling demonstration of physical closed-loop AM improving a mechanical metric, but it is not a powder-metal AM (LPBF/DED) powder-to-property pipeline. (singh2023towardclosedloopadditive pages 1-2)

### 3. Most challenging physical automation steps in a structural materials discovery pipeline (evidence-based)

The most consistently cited physical bottlenecks in SDL literature are **solids handling, dexterous/reactive motor tasks, and instrument integration**, which map directly onto many of the AM pipeline steps highlighted in the question.

#### 3.1 Powder dispensing/mixing and other solids handling
* **Low-mass solid dispensing is repeatedly identified as a major bottleneck**, especially below ~20 mg, often requiring substantial calibration/testing and motivating workarounds such as using stock solutions instead of powders. (seifrid2022autonomouschemicalexperiments pages 8-9, tom2024selfdrivinglaboratoriesfor pages 4-5)
* Community challenge syntheses emphasize that **powders have diverse flow properties** and may require specific geometries (flat surfaces, capillaries, packed columns), making them “perhaps the most challenging” for automation. (maffettone2023whatismissing pages 4-5, maffettoneUnknownyearwhatismissing pages 6-7)
* A-Lab illustrates that solids can be robotized with purpose-built tooling (gravimetric powder dosing, mixing into slurries, automated transfer), but it still requires manual replenishment/cleaning of consumables and precursors. (szymanski2023anautonomouslaboratory pages 7-7, szymanski2024automatingthesynthesis pages 80-83)

**Implication for AM:** powder dispensing/mixing/feeding into AM systems is likely among the hardest steps to robustly automate because it combines mass metrology, contamination control, electrostatics/moisture sensitivity, and variable flowability—exactly the class of “tactile/adaptive manipulation” challenges emphasized in SDL bottleneck analyses. (sadeghi2024engineeringasustainable pages 3-4, maffettone2023whatismissing pages 4-5)

#### 3.2 Loading into AM machines; post-build cleaning of AM systems
The retrieved SDL literature strongly supports “solids handling” and “integration” as hard problems, but **it does not provide direct, step-by-step evidence** on robotic AM powder loading, recoater cleaning, powder sieving/recycling, or post-build LPBF/DED machine cleaning. This absence itself is informative: in the cited SDL corpus, these shop-floor tasks are not yet documented as routinely automated components of SDL loops for structural AM.

#### 3.3 Specimen extraction from build plates (wire EDM, machining)
The retrieved SDL/autonomy papers do not give direct evidence of robotic wire-EDM extraction integrated into SDL loops. What is present is (i) a recognition that sample form factors and instrument-specific constraints are major automation barriers, and (ii) extensive emphasis on the gap between automated measurement and the hard physical steps that connect instruments. (maffettone2023whatismissing pages 4-5, maffettoneUnknownyearwhatismissing pages 6-7)

#### 3.4 Transfer between instruments (atomizer → printer → testing machine → SEM)
Multiple sources emphasize that **integrating disparate hardware is often harder than building any one automated module**, because instruments have nonstandard interfaces and sample form factors. (maffettone2023whatismissing pages 4-5, maffettoneUnknownyearwhatismissing pages 6-7) Further, “few manufacturers develop their software to consider self-driving laboratories,” often lacking APIs, requiring custom code or “hacking.” (seifrid2022autonomouschemicalexperiments pages 8-9)

This aligns with the AM context where multiple vendor ecosystems (powder handling, AM machine, CNC/EDM, heat treat, polishing, SEM, mechanical test) must be orchestrated.

#### 3.5 Automated polishing / metallographic preparation
Direct metallography automation evidence in the retrieved corpus is limited for structural metals. However, APEX explicitly includes robotic grinding/polishing and highlights that capturing tacit grinding “feel” required additional sensing (vibration sensors) to convert a human skill into a machine-controllable signal. (conn2025selfdrivinglabto pages 1-8) This illustrates why polishing is hard: it is a contact-rich, condition-dependent task where closed-loop sensing is critical.

#### 3.6 Automated mechanical testing
Automated mechanical testing is one of the more mature “physical autonomy” modules:
* Robot-assisted mechanical testing (robot + specimen stacks + tester) enabling hundreds of tests for AM AlSi10Mg shows that once specimens are prepared, robotic throughput can be high. (roth2021plasticityandfracture pages 2-3, roth2021plasticityandfracture pages 1-2)
* More generally, autonomous experimentation systems include robotic fabrication + mechanical testing loops (e.g., BEAR optimizing toughness under compression). (stach2021autonomousexperimentationsystems pages 9-11)

### 4. Distinguishing AI-autonomous decision-making vs physically autonomous execution across platforms

A useful and explicit lens is a **two-dimensional autonomy framework** separating (i) *hardware autonomy* (robotic execution) from (ii) *software autonomy* (decision-making/closed-loop experimentation). Hardware autonomy ranges from isolated automated tasks (L1) to automated workflows (L2) to fully automated labs requiring only restocking/maintenance (L3). (tobias2025autonomousselfdrivinglaboratoriesa pages 3-4)

**A‑Lab (LBNL):** tightly coupled AI+robotics.  
A‑Lab combines software autonomy (ML recipe generation, active learning, automated interpretation of XRD with Rietveld refinement) with extensive hardware autonomy (powder dosing, mixing, transfer, furnace loading, grinding, XRD loading). (szymanski2023anautonomouslaboratory pages 1-2, szymanski2023anautonomouslaboratory pages 2-3) Nonetheless, it still needs physical human actions: loading precursor bottles/consumables and cleaning/refilling XRD holders. (szymanski2023anautonomouslaboratory pages 7-7, szymanski2024automatingthesynthesis pages 80-83)

**ORNL Peregrine:** primarily software autonomy without robot execution.  
Peregrine is a monitoring/analytics tool for powder-bed AM, providing automated layer-wise anomaly detection and a mechanism for alerts/macros. (scime2020developmentofmonitoring pages 35-39) The evidence does not support a physically autonomous workcell around the AM machine (powder handling, part removal, post-processing, testing). (scime2020developmentofmonitoring pages 35-39, cooper2023unifiedsoftwarearchitecture pages 6-10)

**Emerald Cloud Lab / CMU Cloud Lab:** physical execution autonomy provided “as a service,” while decision-making remains external.  
Cloud labs provide robotic physical execution of protocols specified remotely: researchers “code experiments” and cloud-lab automation performs the physical work. (arias2024scientificdiscoveryat pages 1-2) Importantly, cloud labs are often *open-loop* in that “humans must specify every detail of the experimental protocols to be executed by the robots,” while AI optimization can be layered on top (experiment selection/parameter tuning) without changing the underlying execution infrastructure. (frisby2021asynchronousparallelbayesian pages 1-2)

**Radical AI:** not evidenced in the retrieved corpus.  
No citable primary source describing “Radical AI” as a specific SDL platform for structural materials discovery/AM was retrieved with the current tool searches; therefore, no evidence-based comparison is possible here.

### 5. Typical “TRL-like” progression from AI-directed/human-executed to fully robotic SDLs (and what is supported here)

The retrieved corpus does **not** provide DOE/NSF program documents that explicitly define “Phase I” vs “Phase II+” SDL scales for materials programs. What it does provide are two widely used autonomy progressions that can be mapped onto a TRL-like maturation:

1) **Six-level lab-autonomy rubric (L0–L5)**: L0–L2 correspond to assistive automation (execution automated, interpretation/decisions remain human), while L3–L5 correspond to increasing autonomy in interpretation and decision-making, with humans commonly “on-the-loop” as supervisors. (hung2024autonomouslaboratoriesfor pages 4-5)

2) **Two-dimensional hardware vs software autonomy**: hardware autonomy L0–L3 and software autonomy defined by whether humans vs computers define the search space and select experiments across closed-loop cycles; “Level‑5” (highest autonomy) is described as not yet achieved. (tobias2025autonomousselfdrivinglaboratoriesa pages 3-4)

**Practical interpretation for DOE/NSF-style programs (evidence-aligned):**
* Early-stage programs commonly implement **software autonomy** (Bayesian optimization/active learning selecting experiments) while relying on humans or partially automated stations for execution (L0–L2 overall in the six-level rubric). (hung2024autonomouslaboratoriesfor pages 4-5)
* Mid-stage programs move toward **workflow automation** (hardware L2) and single-loop or limited-loop autonomy (software autonomy where experiment selection can be computer-driven), but still require restocking/maintenance and exception handling. (tobias2025autonomousselfdrivinglaboratoriesa pages 3-4, szymanski2023anautonomouslaboratory pages 7-7)
* The frontier (hardware L3 + software L3) would correspond to sustained, unattended operation with autonomous decisioning; the autonomy frameworks state this “full” level is not yet achieved broadly. (tobias2025autonomousselfdrivinglaboratoriesa pages 3-4, hung2024autonomouslaboratoriesfor pages 4-5)

### 6. Fully autonomous (no human physical intervention) closed-loop discovery for structural/mechanical properties: what exists vs what does not

**Closed-loop mechanical-property optimization with robotics exists, but “no human physical intervention” is not documented for metal powder AM pipelines.**

* **BEAR (Bayesian Experimental Autonomous Researcher)** is an explicit example of a robotic closed-loop system optimizing a **mechanical property (toughness under uniaxial compression)** for additively manufactured structural polymer components; Bayesian optimization selected experiments, while the robotic system fabricated and mechanically tested parts and fed the measured toughness back into the loop. (stach2021autonomousexperimentationsystems pages 9-11)

* For **metals/alloys**, APEX is the clearest robotic SDL aimed at autonomous alloy discovery with mechanical testing, but the retrieved evidence presents it as a developing platform with human monitoring during test runs, not as a demonstrated fully unattended closed loop. (conn2025selfdrivinglabto pages 1-8)

* A‑Lab achieves sustained autonomous operation for **inorganic powder synthesis**, but (i) it targets synthesis/phase outcomes rather than mechanical properties and (ii) it still requires manual precursor/consumable loading and, in some cases, manual follow-up steps such as regrinding/reheating to recover targets. (szymanski2024automatingthesynthesis pages 76-78, szymanski2024automatingthesynthesis pages 80-83)

**Conclusion supported by retrieved evidence:** within this corpus, there is **no definitive example** of a fully autonomous, closed-loop, *powder-to-structural/mechanical-property* discovery pipeline with **zero human physical intervention** for metal AM (LPBF/DED). The strongest evidence points to partial pipelines (APEX) and to fully closed-loop mechanical optimization in other material/process classes (BEAR polymers; extrusion closed-loop repair improving breaking load). (conn2025selfdrivinglabto pages 1-8, stach2021autonomousexperimentationsystems pages 9-11, singh2023towardclosedloopadditive pages 1-2)

## Summary of key takeaways for structural AM SDLs

1. **Physical robotics exists for alloy/AM discovery, but end-to-end autonomy is still incomplete.** APEX demonstrates the most explicit robotics for alloys + AM + mechanical characterization in the retrieved set. (conn2025selfdrivinglabto pages 1-8)
2. **AM autonomy is currently stronger on the “digital thread/monitoring/analytics” side** (e.g., Peregrine) than on full robotic execution of powder logistics and post-processing. (scime2020developmentofmonitoring pages 35-39)
3. **Hard physical bottlenecks are concentrated in solids/powder handling, dexterous contact tasks (prep/polishing), and cross-instrument integration**, exacerbated by vendor interface limitations and sample form-factor constraints. (seifrid2022autonomouschemicalexperiments pages 8-9, maffettone2023whatismissing pages 4-5)
4. **Mechanical testing is comparatively automatable** (robot-assisted UTM demonstrated at scale), suggesting a practical strategy is to prioritize automation of upstream specimen preparation/extraction and transfer between machines to unlock end-to-end pipelines. (roth2021plasticityandfracture pages 1-2)



References

1. (conn2025selfdrivinglabto pages 1-8): Shelby Conn and Alex Baker. Self-driving lab to automate the discovery of novel alloys. Office of Scientific and Technical Information (OSTI), Aug 2025. URL: https://doi.org/10.2172/2584738, doi:10.2172/2584738.

2. (conn2025selfdrivinglabto pages 8-8): Shelby Conn and Alex Baker. Self-driving lab to automate the discovery of novel alloys. Office of Scientific and Technical Information (OSTI), Aug 2025. URL: https://doi.org/10.2172/2584738, doi:10.2172/2584738.

3. (szymanski2024automatingthesynthesis pages 78-80): N Szymanski. Automating the synthesis and characterization of inorganic materials. Unknown journal, 2024.

4. (szymanski2023anautonomouslaboratory pages 7-7): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1070 citations and is from a highest quality peer-reviewed journal.

5. (szymanski2024automatingthesynthesis pages 80-83): N Szymanski. Automating the synthesis and characterization of inorganic materials. Unknown journal, 2024.

6. (szymanski2023anautonomouslaboratory pages 2-3): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1070 citations and is from a highest quality peer-reviewed journal.

7. (szymanski2023anautonomouslaboratory pages 1-2): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1070 citations and is from a highest quality peer-reviewed journal.

8. (scime2020developmentofmonitoring pages 35-39): Luke Scime, William Halsey, J. Haley, Ashutosh Kumar Singh, Michael Sprayberry, Amir K. Ziabari, and V. Paquit. Development of monitoring techniques for laser powder bed additive manufacturing of metal structures (progress report). ArXiv, Sep 2020. URL: https://doi.org/10.2172/1675044, doi:10.2172/1675044. This article has 3 citations.

9. (scime2020developmentofmonitoring pages 30-35): Luke Scime, William Halsey, J. Haley, Ashutosh Kumar Singh, Michael Sprayberry, Amir K. Ziabari, and V. Paquit. Development of monitoring techniques for laser powder bed additive manufacturing of metal structures (progress report). ArXiv, Sep 2020. URL: https://doi.org/10.2172/1675044, doi:10.2172/1675044. This article has 3 citations.

10. (cooper2023unifiedsoftwarearchitecture pages 6-10): Stephanie Cooper, William Halsey, Vladimir Orlyanchik, Vincent Paquit, Luke Scime, Zackary Snow, Amir Ziabari, and Ryan Dehoff. Unified Software Architecture for Advanced Materials and Manufacturing Technologies Data Management and Processing: FY 2023 Multidimensional Data Correlation Platform. Office of Scientific and Technical Information (OSTI), Sep 2023. URL: https://doi.org/10.2172/2439894, doi:10.2172/2439894.

11. (scime2020developmentofmonitoring pages 25-30): Luke Scime, William Halsey, J. Haley, Ashutosh Kumar Singh, Michael Sprayberry, Amir K. Ziabari, and V. Paquit. Development of monitoring techniques for laser powder bed additive manufacturing of metal structures (progress report). ArXiv, Sep 2020. URL: https://doi.org/10.2172/1675044, doi:10.2172/1675044. This article has 3 citations.

12. (scime2020developmentofmonitoring pages 39-42): Luke Scime, William Halsey, J. Haley, Ashutosh Kumar Singh, Michael Sprayberry, Amir K. Ziabari, and V. Paquit. Development of monitoring techniques for laser powder bed additive manufacturing of metal structures (progress report). ArXiv, Sep 2020. URL: https://doi.org/10.2172/1675044, doi:10.2172/1675044. This article has 3 citations.

13. (vecchio2021highthroughputrapidexperimental pages 1-4): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.

14. (castellanosUnknownyearcarnegiemellonsclouda pages 1-4): S Castellanos. Carnegie mellon's cloud lab to automate labor-intensive science experiments. Unknown journal, Unknown year.

15. (castellanosUnknownyearcarnegiemellonscloud pages 1-4): S Castellanos. Carnegie mellon's cloud lab to automate labor-intensive science experiments. Unknown journal, Unknown year.

16. (arias2024scientificdiscoveryat pages 1-2): D. Sebastian Arias and Rebecca E. Taylor. Scientific discovery at the press of a button: navigating emerging cloud laboratory technology. Advanced Materials Technologies, May 2024. URL: https://doi.org/10.1002/admt.202400084, doi:10.1002/admt.202400084. This article has 7 citations and is from a peer-reviewed journal.

17. (frisby2021asynchronousparallelbayesian pages 1-2): Trevor S Frisby, Zhiyun Gong, and Christopher James Langmead. Asynchronous parallel bayesian optimization for ai-driven cloud laboratories. Bioinformatics, 37:i451-i459, Jul 2021. URL: https://doi.org/10.1093/bioinformatics/btab291, doi:10.1093/bioinformatics/btab291. This article has 19 citations and is from a highest quality peer-reviewed journal.

18. (tobias2025autonomousselfdrivinglaboratoriesab pages 1-2): AV Tobias and A Wahab. Autonomous 'self-driving'laboratories: a review of technology and policy implications. Unknown journal, 2025.

19. (zilgalvis2025yingchiangjeffreylee pages 6-9): G ZILGALVIS. Ying-chiang jeffrey lee, bria persaud, barbara del castello, allison berke. Unknown journal, 2025.

20. (zilgalvis2025yingchiangjeffreyleea pages 6-9): G ZILGALVIS. Ying-chiang jeffrey lee, bria persaud, barbara del castello, allison berke. Unknown journal, 2025.

21. (roth2021plasticityandfracture pages 2-3): Christian C. Roth, Thomas Tancogne-Dejean, and Dirk Mohr. Plasticity and fracture of cast and slm alsi10mg: high-throughput testing and modeling. Additive Manufacturing, 43:101998, Jul 2021. URL: https://doi.org/10.1016/j.addma.2021.101998, doi:10.1016/j.addma.2021.101998. This article has 113 citations and is from a highest quality peer-reviewed journal.

22. (roth2021plasticityandfracture pages 1-2): Christian C. Roth, Thomas Tancogne-Dejean, and Dirk Mohr. Plasticity and fracture of cast and slm alsi10mg: high-throughput testing and modeling. Additive Manufacturing, 43:101998, Jul 2021. URL: https://doi.org/10.1016/j.addma.2021.101998, doi:10.1016/j.addma.2021.101998. This article has 113 citations and is from a highest quality peer-reviewed journal.

23. (roth2021plasticityandfracture pages 10-12): Christian C. Roth, Thomas Tancogne-Dejean, and Dirk Mohr. Plasticity and fracture of cast and slm alsi10mg: high-throughput testing and modeling. Additive Manufacturing, 43:101998, Jul 2021. URL: https://doi.org/10.1016/j.addma.2021.101998, doi:10.1016/j.addma.2021.101998. This article has 113 citations and is from a highest quality peer-reviewed journal.

24. (singh2023towardclosedloopadditive pages 1-2): Manpreet Singh, Fujun Ruan, Albert Xu, Yuchen Wu, Archit Rungta, Luyuan Wang, Kevin Song, Howie Choset, and Lu Li. Toward closed-loop additive manufacturing: paradigm shift in fabrication, inspection, and repair. 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 10066-10073, Oct 2023. URL: https://doi.org/10.1109/iros55552.2023.10342148, doi:10.1109/iros55552.2023.10342148. This article has 8 citations.

25. (seifrid2022autonomouschemicalexperiments pages 8-9): Martin Seifrid, Robert Pollice, Andrés Aguilar-Granda, Zamyla Morgan Chan, Kazuhiro Hotta, Cher Tian Ser, Jenya Vestfrid, Tony C. Wu, and Alán Aspuru-Guzik. Autonomous chemical experiments: challenges and perspectives on establishing a self-driving lab. Accounts of Chemical Research, 55:2454-2466, Aug 2022. URL: https://doi.org/10.1021/acs.accounts.2c00220, doi:10.1021/acs.accounts.2c00220. This article has 312 citations and is from a domain leading peer-reviewed journal.

26. (tom2024selfdrivinglaboratoriesfor pages 4-5): Gary Tom, Stefan P. Schmid, Sterling G. Baird, Yang Cao, Kourosh Darvish, Han Hao, Stanley Lo, Sergio Pablo-García, Ella M. Rajaonson, Marta Skreta, Naruki Yoshikawa, Samantha Corapi, Gun Deniz Akkoc, Felix Strieth-Kalthoff, Martin Seifrid, and Alán Aspuru-Guzik. Self-driving laboratories for chemistry and materials science. Chemical Reviews, 124:9633-9732, Aug 2024. URL: https://doi.org/10.1021/acs.chemrev.4c00055, doi:10.1021/acs.chemrev.4c00055. This article has 623 citations and is from a highest quality peer-reviewed journal.

27. (maffettone2023whatismissing pages 4-5): Phillip M. Maffettone, Pascal Friederich, Sterling G. Baird, Ben Blaiszik, Keith A. Brown, Stuart I. Campbell, Orion A. Cohen, Rebecca L. Davis, Ian T. Foster, Navid Haghmoradi, Mark Hereld, Howie Joress, Nicole Jung, Ha-Kyung Kwon, Gabriella Pizzuto, Jacob Rintamaki, Casper Steinmann, Luca Torresi, and Shijing Sun. What is missing in autonomous discovery: open challenges for the community. Digital Discovery, 2:1644-1659, Apr 2023. URL: https://doi.org/10.48550/arxiv.2304.11120, doi:10.48550/arxiv.2304.11120. This article has 48 citations and is from a peer-reviewed journal.

28. (maffettoneUnknownyearwhatismissing pages 6-7): PM Maffettone, P Friederich, SG Baird, and B Blaiszik. What is missing in autonomous discovery. Unknown journal, Unknown year.

29. (sadeghi2024engineeringasustainable pages 3-4): Sina Sadeghi, Richard B. Canty, Nikolai Mukhin, Jinge Xu, Fernando Delgado-Licona, and Milad Abolhasani. Engineering a sustainable future: harnessing automation, robotics, and artificial intelligence with self-driving laboratories. ACS Sustainable Chemistry &amp; Engineering, 12:12695-12707, Aug 2024. URL: https://doi.org/10.1021/acssuschemeng.4c02177, doi:10.1021/acssuschemeng.4c02177. This article has 37 citations and is from a peer-reviewed journal.

30. (stach2021autonomousexperimentationsystems pages 9-11): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 369 citations and is from a peer-reviewed journal.

31. (tobias2025autonomousselfdrivinglaboratoriesa pages 3-4): AV Tobias and A Wahab. Autonomous 'self-driving'laboratories: a review of technology and policy implications. Unknown journal, 2025.

32. (hung2024autonomouslaboratoriesfor pages 4-5): Linda Hung, Joyce Yager, Danielle Monteverde, Dave Baiocchi, Ha-Kyung Kwon, Shijing Sun, and Santosh Suram. Autonomous laboratories for accelerated materials discovery: a community survey and practical insights. Digital Discovery, Mar 2024. URL: https://doi.org/10.1039/d4dd00059e, doi:10.1039/d4dd00059e. This article has 31 citations and is from a peer-reviewed journal.

33. (szymanski2024automatingthesynthesis pages 76-78): N Szymanski. Automating the synthesis and characterization of inorganic materials. Unknown journal, 2024.