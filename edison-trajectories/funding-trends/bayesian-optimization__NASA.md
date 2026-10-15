# Funding trends: bayesian optimization — NASA

*Edison `LITERATURE` task `d63d8807-41fc-434d-b47c-bbe344cdad37` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
Bayesian optimization for alloy/materials design to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: Bayesian optimization, active learning, and multi-objective acquisition functions applied to alloy/materials design and process optimization (including BoTorch, GP surrogates, BO with constraints, network/function-of-network BO)

FUNDING SOURCE OF INTEREST: the U.S. National Aeronautics and Space Administration (NASA), including STMD (Space Technology Mission Directorate), Early Career Faculty (ECF), Early Stage Innovations (ESI), SBIR/STTR, ULI, EPSCoR, and NASA center programs (Marshall, Glenn, Langley, JPL) related to additive manufacturing, advanced metallic alloys, and AI for materials

TASK:

1. From the published scientific literature (2020-2026), inspect the *Acknowledgements / Funding*
   sections of recent papers in this topic area. Extract every grant/award acknowledged from the
   funding source above.

2. For EACH funded project found, report (one row per project):
   - PI name(s) and institution
   - Grant program (e.g., "NSF CAREER", "DOE ARPA-E ULTIMATE", "DARPA AMD")
   - Award number(s)
   - Award amount IF stated (otherwise "not stated"; do NOT make one up)
   - Project title or short description (1-2 sentences)
   - Year started / period of performance if known
   - Citation key(s) of the paper(s) where this funding was acknowledged

3. Identify FUNDING TRENDS for this (topic, agency) combination:
   - Which sub-programs within the agency are growing vs. shrinking in this topic?
   - Which institutions and PIs are dominating funding in this area?
   - What new agency programs (launched 2022+) are funding this topic?
   - Are there visible gaps where the agency is NOT funding this topic but could?

4. Provide a brief (3-5 sentence) executive summary at the top describing the overall funding
   posture of NASA in this topic.

OUTPUT FORMAT: markdown. Start with the executive summary, then a markdown table of funded
projects, then a "Trends" subsection. Be precise about award numbers. Do not invent data.


## Executive summary (NASA posture in this topic, 2020–2026)
NASA’s explicit, literature-visible funding for Bayesian optimization (BO)/active learning in metallic materials and manufacturing appears dispersed across (i) capacity-building programs (EPSCoR) that underwrite dataset generation for additively manufactured alloys, (ii) flagship university programs (University Leadership Initiative, ULI) supporting BO/GP-based design workflows, and (iii) mission/center-aligned efforts combining Space Technology Mission Directorate (STMD), Science Mission Directorate Biological & Physical Sciences (SMD/BPS), Marshall internal funds, and Flight Opportunities to mature microgravity manufacturing capabilities. (bhandari2023machinelearningbasedthermalconductivity pages 11-13, dharmadhikari2023afullyautomatedframework pages 15-16, oconnor2024acombinedcomputational pages 34-38)
NASA Aeronautics also supports BO methodology development/benchmarking through the Transformative Aeronautics Concepts Program, indicating interest in formalizing BO best practices for materials discovery and autonomous labs. (stuckner2026benchmarkingbayesianoptimization pages 1-6)
Small-business pathways are visible via a T3 portfolio document citing an SBIR Phase I contract number, but the project metadata is not fully specified in the excerpt. (arnold20252040visionstudy pages 9-13)
Across the retrieved 2020–2026 literature, award numbers are often present (EPSCoR/ULI/CAN/SBIR), but award amounts and detailed periods of performance are usually not stated in the papers themselves, limiting quantitative trend inference from publications alone. (bhandari2023machinelearningbasedthermalconductivity pages 11-13, dharmadhikari2023afullyautomatedframework pages 15-16, arnold20252040visionstudy pages 9-13)

## NASA-funded projects acknowledged in 2020–2026 literature

| NASA program/subprogram | Award/contract number | PI(s) and institution(s) | Award amount | Period of performance/start year | Project title/short description (1–2 sentences) | Evidence papers (citation keys) |
|---|---|---|---|---|---|---|
| NASA Established Program to Stimulate Competitive Research (EPSCoR) | 80NSSC19M0149 | Shengmin Guo and Paul R. Gradl; institution(s) inferable from paper affiliations: Louisiana State University and NASA Marshall Space Flight Center | not stated | start year inferable as 2019 from award number; exact period not stated | Partial support for experimental data generation used to train and validate machine-learning models for thermal conductivity prediction of additively manufactured alloys including Inconel 718 and GRCop-42. The paper positions the dataset for future optimization of alloy compositions toward target thermal conductivity. (bhandari2023machinelearningbasedthermalconductivity pages 13-15, bhandari2023machinelearningbasedthermalconductivity pages 11-13) | bhandari2023machinelearningbasedthermalconductivity |
| NASA University Leadership Initiative (ULI) | 80NSSC21M0068 | Karen A. Thole, Amrita Basak, Reid A. Berdanier; institution inferable from paper affiliations: Pennsylvania State University | not stated | start year inferable as 2021 from award number; exact period not stated | Funding for a Gaussian-process plus Bayesian-optimization framework to design additively manufacturable pin-fin arrays. The study uses CFD-coupled BO for pressure-drop minimization and notes future extension to multi-objective optimization for heat transfer and pressure loss. (dharmadhikari2023afullyautomatedframework pages 15-16) | dharmadhikari2023afullyautomatedframework |
| NASA Cooperative Agreement Notice (CAN), with Marshall Space Flight Center internal funds; related NASA support also from Science Mission Directorate Biological and Physical Sciences Division and Space Technology Mission Directorate | 80NSSC22M0209 | not stated; Ohio State University support is explicitly noted, and paper authors are A. O'Connor, J.M. Bonebrake, and T.C. Bryan with NASA Marshall Space Flight Center-led work | not stated | start year inferable as 2022 from award number; exact period not stated | “Integration and Demonstration of Self-contained Laser Welding System for Microgravity Experiments.” The acknowledged support is tied to in-space laser welding/manufacturing maturation, validation datasets, and microgravity manufacturing experiments; additional support includes NASA Flight Opportunities. (oconnor2024acombinedcomputational pages 34-38, oconnor2024acombinedcomputational media 5c1680cc) | oconnor2024acombinedcomputational |
| NASA Transformative Aeronautics Concepts Program | not stated | Joshua Stuckner, Peter Toma, Brandon Hearley (NASA Glenn Research Center); Jacob Goodin (University of Akron); Stephen Xie (KBR, Inc.) | not stated | not stated | Sponsorship for benchmarking Bayesian optimization frameworks and acquisition strategies for materials discovery and autonomous laboratories. The NASA technical memorandum compares GP-, RF-, NN-, and TPE-based BO strategies across benchmark materials-design tasks. (stuckner2026benchmarkingbayesianoptimization pages 1-6) | stuckner2026benchmarkingbayesianoptimization |
| NASA SBIR 2023 Phase I | 80NSSC23PB480 | not stated | not stated | 2023 Phase I (completed) | SBIR Phase I contract identified in NASA T3 portfolio materials as a synergistic SBIR activity associated with 2040 Vision / Transformational Tools and Technology implementation. The excerpt provides the contract number but not a full project title or PI details. (arnold20252040visionstudy pages 9-13) | arnold20252040visionstudy |


*Table: This table compiles the distinct NASA awards, contracts, and program sponsorships that were explicitly acknowledged in the retrieved 2020–2026 literature and adjacent NASA technical materials relevant to Bayesian optimization, active learning, and data-driven materials/process design. It is useful as a project-level inventory of NASA support, with missing fields left as 'not stated' to avoid overclaiming.*

## Trends (NASA programs, PIs/institutions, new efforts, gaps)

### Sub-program signals (growing vs. shrinking)
* **Space manufacturing / microgravity manufacturing maturity**: A 2024 NASA Marshall-related work explicitly acknowledges multi-source NASA support spanning Marshall internal funds, SMD/BPS, STMD, and Flight Opportunities, consistent with a posture of integrating modeling + experimentation + flight-like testing for manufacturing technology maturation. (oconnor2024acombinedcomputational pages 34-38, oconnor2024acombinedcomputational media 5c1680cc)
* **Aeronautics methods/benchmarking**: A 2026 NASA Technical Memorandum on BO benchmarking is explicitly sponsored by the **Transformative Aeronautics Concepts Program**, suggesting continued (and possibly increasing) interest in codifying BO practices for materials discovery/autonomous laboratories within Aeronautics. (stuckner2026benchmarkingbayesianoptimization pages 1-6)
* **EPSCoR as an enabling mechanism**: The 2023 AM alloy thermal-conductivity work ties experimental dataset generation to **NASA EPSCoR** (80NSSC19M0149), indicating NASA’s use of EPSCoR to seed data infrastructure that can later support optimization (including BO-guided compositional/process exploration). (bhandari2023machinelearningbasedthermalconductivity pages 11-13)
* **SBIR visibility in this topic**: A NASA T3 portfolio/vision document includes an **SBIR 2023 Phase I** contract number (80NSSC23PB480), but without enough detail in the excerpt to assess topic depth or trajectory. (arnold20252040visionstudy pages 9-13)

Because the evidence here is limited to what is explicitly acknowledged in a small set of retrieved papers, **strong “growing vs shrinking” claims cannot be made from publications alone**; additional validation would typically require querying NSPIRES/SBIR award databases or NASA center procurement data (not part of the provided evidence set).

### Dominant institutions and PIs (in the extracted corpus)
* **Pennsylvania State University (ULI)**: The BO/GP pin-fin design work is explicitly funded by **NASA ULI 80NSSC21M0068**; senior authors include Karen A. Thole, Amrita Basak, and Reid A. Berdanier (Penn State). (dharmadhikari2023afullyautomatedframework pages 15-16)
* **NASA Glenn Research Center (Aeronautics BO benchmarking)**: Stuckner, Toma, and Hearley (NASA Glenn) appear as authors on the Transformative Aeronautics Concepts-sponsored BO benchmarking report, indicating Glenn leadership in comparative evaluation of BO frameworks for materials/autonomy. (stuckner2026benchmarkingbayesianoptimization pages 1-6)
* **NASA Marshall Space Flight Center ecosystem (space manufacturing)**: O’Connor et al. acknowledge MSFC internal funds and STMD/SMD/BPS support, and identify an OSU-linked cooperative agreement award number (80NSSC22M0209) for a microgravity laser welding system demonstration. (oconnor2024acombinedcomputational pages 34-38, oconnor2024acombinedcomputational media 5c1680cc)
* **EPSCoR-funded AM data generation**: Bhandari et al. explicitly cite NASA EPSCoR (80NSSC19M0149) supporting experimental data generation for AM alloy thermal conductivity modeling. (bhandari2023machinelearningbasedthermalconductivity pages 11-13)

### New programs (launched 2022+) seen funding this topic
Within the extracted evidence, the clearest **post-2022 award** is a **2022-numbered cooperative agreement** (80NSSC22M0209) under a NASA CAN tied to microgravity laser welding system integration/demonstration. (oconnor2024acombinedcomputational pages 34-38, oconnor2024acombinedcomputational media 5c1680cc)
The 2025 T3 implementation document also shows an **SBIR 2023 Phase I** contract number (80NSSC23PB480). (arnold20252040visionstudy pages 9-13)

### Gaps/opportunities for a DOE Genesis Mission Phase I (autonomous closed-loop alloy discovery)
* **Sparse explicit acknowledgement of BO toolchains for alloy composition discovery**: In this retrieved set, NASA acknowledgements appear more frequently tied to **manufacturing/process and dataset generation** (AM thermal conductivity; microgravity welding systems) than to autonomous, closed-loop alloy composition discovery pipelines (e.g., constrained/multi-objective BO over high-dimensional composition spaces). (bhandari2023machinelearningbasedthermalconductivity pages 11-13, oconnor2024acombinedcomputational media 5c1680cc)
* **Limited publication-level transparency on award scope**: Award amounts and periods of performance are rarely stated in acknowledgements, complicating portfolio sizing/trend inference from papers alone and suggesting an opportunity for a proposal to emphasize measurable deliverables, benchmarks, and open datasets for closed-loop discovery that align with NASA’s autonomy interests. (bhandari2023machinelearningbasedthermalconductivity pages 11-13, dharmadhikari2023afullyautomatedframework pages 15-16)
* **Cross-directorate integration opportunity**: The microgravity manufacturing work explicitly spans STMD + SMD/BPS + Flight Opportunities + center internal funds, indicating NASA’s receptiveness to cross-cutting efforts; an autonomous closed-loop alloy discovery thrust could be positioned as enabling both **ground-based AM qualification** and **space manufacturing** needs, while leveraging BO best practices reflected in NASA’s BO benchmarking activities. (oconnor2024acombinedcomputational pages 34-38, stuckner2026benchmarkingbayesianoptimization pages 1-6)


References

1. (bhandari2023machinelearningbasedthermalconductivity pages 11-13): Uttam Bhandari, Yehong Chen, Huan Ding, Congyuan Zeng, Selami Emanet, Paul R. Gradl, and Shengmin Guo. Machine-learning-based thermal conductivity prediction for additively manufactured alloys. Journal of Manufacturing and Materials Processing, 7:160, Sep 2023. URL: https://doi.org/10.3390/jmmp7050160, doi:10.3390/jmmp7050160. This article has 27 citations.

2. (dharmadhikari2023afullyautomatedframework pages 15-16): Susheel Dharmadhikari, Reid A. Berdanier, Karen A. Thole, and Amrita Basak. A fully-automated framework integrating gaussian process regression and bayesian optimization to design pin-fins. ArXiv, Jan 2023. URL: https://doi.org/10.48550/arxiv.2301.13118, doi:10.48550/arxiv.2301.13118. This article has 4 citations.

3. (oconnor2024acombinedcomputational pages 34-38): A O'Connor, JM Bonebrake, and TC Bryan. A combined computational, experimental, and technology development approach to in-space laser manufacturing maturation at nasa marshall space flight …. Unknown journal, 2024.

4. (stuckner2026benchmarkingbayesianoptimization pages 1-6): J. Stuckner, P. Toma, Jacob T. Goodin, Brandon L. Hearley, and Stephen Xie. Benchmarking Bayesian Optimization Frameworks and Acquisition Strategies for Materials Discovery and Autonomous Laboratories. National Aeronautics and Space Administration, Mar 2026. URL: https://doi.org/10.64631/zkvt6687, doi:10.64631/zkvt6687.

5. (arnold20252040visionstudy pages 9-13): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

6. (bhandari2023machinelearningbasedthermalconductivity pages 13-15): Uttam Bhandari, Yehong Chen, Huan Ding, Congyuan Zeng, Selami Emanet, Paul R. Gradl, and Shengmin Guo. Machine-learning-based thermal conductivity prediction for additively manufactured alloys. Journal of Manufacturing and Materials Processing, 7:160, Sep 2023. URL: https://doi.org/10.3390/jmmp7050160, doi:10.3390/jmmp7050160. This article has 27 citations.

7. (oconnor2024acombinedcomputational media 5c1680cc): A O'Connor, JM Bonebrake, and TC Bryan. A combined computational, experimental, and technology development approach to in-space laser manufacturing maturation at nasa marshall space flight …. Unknown journal, 2024.
