# Funding trends: ml materials informatics — NASA

*Edison `LITERATURE` task `afc1edf8-a12b-4ee2-b203-b52bed37aabc` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
machine learning for materials informatics to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: machine learning for materials informatics, property prediction, and inverse alloy design (graph neural networks, transformers, foundation models, generative models for materials)

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


## Executive summary (NASA posture in ML for materials informatics, 2020–2026)
NASA’s visible open-literature funding footprint in ML for metallic materials informatics and alloy property prediction appears concentrated in (i) Aeronautics Research Mission Directorate (ARMD) tool-development portfolios (notably the Transformational Tools and Technology / “T3” ecosystem) and (ii) targeted external mechanisms such as EPSCoR and STMD’s Early Stage Innovations (ESI) grants, with SBIR Phase I awards used to seed enabling software/tool capabilities. (arnold20252040visionstudy pages 9-13, bhandari2023machinelearningbasedthermalconductivity pages 13-15, wu2022ml4lmmachinelearning pages 3-5)
Across the accessible 2020–2026 papers inspected, only a small number of peer-reviewed materials-ML alloy papers explicitly list NASA award numbers; NASA support is often acknowledged at a program level (e.g., ARMD Transformative Aeronautics Concepts / T3) without an award identifier, or appears in NASA technical memoranda and portfolio documents rather than standard journal funding statements. (stuckner2022designofmaterials pages 1-5, arnold20252040visionstudy pages 9-13)
Within NASA’s own portfolio summaries, T3 reports sustained NRA activity (~14 awards totaling ~US$3.5M/year) with substantial AI/ML participation (43% of proposals), and explicit SBIR Phase I activity (contract 80NSSC23PB480), indicating a consistent emphasis on ML-enabled tools for qualification/certification, multiscale modeling, and AM-relevant materials workflows. (arnold20252040visionstudy pages 9-13, arnold20252040visionstudyc pages 9-13)
STMD also supports larger institute-scale funding vehicles for additive-manufacturing certification (Space Technology Research Institute; “up to $3M/year” for 5 years), consistent with a push toward model-based certification and digital-thread concepts adjacent to autonomous/closed-loop discovery themes. (vickers2022nasaadvisorycounciltechnology media ab2601d1)

## NASA-funded projects acknowledged in the inspected literature (2020–2026)
| NASA funding source/program | Award/contract/solicitation number | PI(s) | Institution(s) | Award amount | Period of performance / start year | Short project description | Paper(s)/document(s) acknowledging the funding |
|---|---|---|---|---|---|---|---|
| NASA EPSCoR (Established Program to Stimulate Competitive Research) | 80NSSC19M0149 | not stated | Authors: Univ. of Louisiana at Lafayette / collaborators; paper authors include Paul R. Gradl (NASA) and Shengmin Guo | not stated | not stated | Partial support for generating experimental data used to train ML models for predicting thermal conductivity of additively manufactured alloys, including validation on Inconel 718 and GRCop-42. | *Machine-Learning-Based Thermal Conductivity Prediction for Additively Manufactured Alloys* (Bhandari et al., 2023) (bhandari2023machinelearningbasedthermalconductivity pages 11-13, bhandari2023machinelearningbasedthermalconductivity pages 13-15) |
| NASA STMD Early Stage Innovations Space Technology Research Grants Program | 80NSSC22K0257 | not stated in excerpt | not stated in excerpt | not stated | not stated | Funds ML research for safe Mars landing; the retrieved document is not a materials-informatics paper, but it is the clearest STMD/ESI award identifier found in the searched corpus. Included here as a NASA ESI comparator award with explicit identifier. | *ML4LM: Machine Learning for Safely Landing on Mars* (Wu et al., 2022) (wu2022ml4lmmachinelearning pages 3-5) |
| NASA SBIR Phase I under ARMD T3 portfolio | 80NSSC23PB480 | not stated for this SBIR item | not stated | not stated | 2023 Phase I; completed | SBIR activity within NASA Transformational Tools and Technology (T3) portfolio; Arnold’s 2025 portfolio summary places it alongside ML/AI-heavy multiscale modeling and materials-informatics efforts relevant to additive manufacturing and qualification. | *2040 Vision Study: NASA’s T3 Implementation Activities* (Arnold, 2025) (arnold20252040visionstudy pages 9-13, arnold20252040visionstudya pages 9-13, arnold20252040visionstudyb pages 9-13, arnold20252040visionstudyc pages 9-13) |
| NASA ARMD Transformative Aeronautics Concepts Program / Transformational Tools and Technologies project | not stated | Joshua Stuckner; Othmane Benafan; Steven M. Arnold | NASA Glenn Research Center; Intellegens | not stated | not stated | Internal NASA/ARMD support for evaluating Alchemite for inverse materials design on shape memory alloy and heat-exchanger datasets. The work focuses on sparse-data ML for inverse design but does not provide an external award number. | *Design of Materials With Alchemite* (Stuckner et al., 2022 NASA/TM-20220008637) (stuckner2022designofmaterials pages 1-5) |


*Table: This table compiles the NASA-funded projects (one row per award) identified in the retrieved evidence. Solicitation/program-mechanism records (i.e., funding-opportunity announcements or program vehicles without a tied awarded project) are kept separate below to avoid overstating NASA's project-level footprint relative to other (topic, agency) cells.*

### Adjacent NASA solicitations and program mechanisms (not awarded-project rows)

The following items appeared in the retrieved corpus but are *solicitations* or
*program-mechanism descriptions* rather than identifiable funded projects, so they are
listed here separately and **not counted** in the project table above. They are useful as
funding-pipeline context for the FLAIME proposal but should not be tallied alongside
awarded projects.

| NASA mechanism | Solicitation/program identifier | Description | Source document |
|---|---|---|---|
| NASA ARMD University Leadership Initiative (ULI) solicitation | NNH18ZEA001N-ULI2 | Identifier for NASA's second ULI call (2018 solicitation; paper published 2020). In the retrieved evidence it is not tied to a specific materials-ML alloy award; it documents the ULI funding vehicle under which later ML/AM university work proceeded. | *Putting Universities in Charge Yields Early Success for NASA Aeronautics* (Datta et al., 2020) (datta2020puttinguniversitiesin pages 11-12) |
| NASA EPSCoR Rapid Response Research (R3) NOFO | NNH24ZHA002C | FY2024 solicitation/NOFO for Rapid Response Research topics, including digital transformation and related ML topics. This is a funding-opportunity announcement, not an awarded project. | *NASA EPSCoR Rapid Response Research (R3)–FY24 Research Topics* (Valco, FY24 topics document) (valcoUnknownyearnasaepscorrapid pages 6-9, valcoUnknownyearnasaepscorrapid pages 60-63) |
| NASA STMD Space Technology Research Institute (STRI) | program mechanism (no award number) | STMD institute-scale funding vehicle for interdisciplinary research combining computational tools and experimentation to advance model-based certification of AM aerospace products. Award size up to $3M/year for an expected 5-year duration is described, but no specific award is identified in the excerpt. | *NASA Advisory Council—Technology, Innovation, and Engineering Committee—Advanced Manufacturing* (Vickers, 2022) (vickers2022nasaadvisorycounciltechnologya pages 13-19, vickers2022nasaadvisorycounciltechnology media ab2601d1) |

**Notes on completeness.** This table reflects only what is explicitly recoverable from the Acknowledgements/Funding sections (or equivalent award listings) in the retrieved full texts. Several documents mention NASA programs but do not provide award numbers (e.g., ARMD Transformative Aeronautics Concepts Program support in a NASA/TM), and at least one peer-reviewed AM/ML paper mentions NASA ULI support but the grant number is truncated in the retrieved excerpt (so it is not included as an award-numbered row). (stuckner2022designofmaterials pages 1-5, jiang2024deeplearningapproaches pages 13-13)

## Trends (NASA × ML for materials informatics / alloys)

### 1) Sub-programs growing vs. shrinking (as visible in 2020–2026 acknowledgements)
- **Growing/active: ARMD T3 + associated NRAs and SBIRs.** A NASA ARMD portfolio document reports an NRA award stream of “14 awards” totaling “approx. $3.5M/year” and notes “43%” of proposals have significant ML/AI activities, alongside “Synergistic SBIR Activities” with an explicit 2023 SBIR Phase I contract number (80NSSC23PB480). (arnold20252040visionstudy pages 9-13, arnold20252040visionstudyc pages 9-13)
- **Active: NASA EPSCoR as a feeder for materials datasets and ML model development.** A peer-reviewed AM-alloy ML paper explicitly acknowledges NASA EPSCoR grant 80NSSC19M0149 supporting experimental data generation used for ML training/validation. (bhandari2023machinelearningbasedthermalconductivity pages 13-15)
- **Active/newer STMD mechanisms (2022+): ESI and institute-scale STRI.** A 2022 document explicitly lists an ESI Space Technology Research Grants Program award number (80NSSC22K0257). (wu2022ml4lmmachinelearning pages 3-5) Separately, STMD’s Space Technology Research Institute mechanism is described with an “expected duration” of 5 years and “award amount” up to $3M/year (without a specific award number in the excerpt). (vickers2022nasaadvisorycounciltechnology media ab2601d1)

### 2) Dominant institutions and PIs (from explicit award-linked mentions)
- **University consortia linked to ARMD T3 NRAs** include University of Massachusetts Lowell (PIs Marianna Maiaru; Scott E. Stapleton; with collaborators Greg Odegard at Michigan Tech and Farhad Pourkamali Anaraki at UMass Lowell) and University of Texas at Austin (PI Karen Wilcox). These are presented in a T3 multiscale modeling/ML context relevant to materials, structures, and AM qualification workflows. (arnold20252040visionstudy pages 9-13)
- **NASA center involvement visible in technical memoranda**: NASA Glenn Research Center personnel (e.g., Joshua Stuckner, Othmane Benafan, Steven M. Arnold) are explicitly associated with inverse-design software evaluation under ARMD Transformative Aeronautics Concepts/T3 support (no award number provided). (stuckner2022designofmaterials pages 1-5)

### 3) New NASA programs (launched 2022+) funding adjacent capability
- **STMD Early Stage Innovations (ESI) Space Technology Research Grants Program** appears with an explicit 80NSSC22K0257 award identifier in a 2022 ML paper (not materials-focused), demonstrating the identifiable grant line used by STMD to fund early-stage AI/ML research. (wu2022ml4lmmachinelearning pages 3-5)
- **STMD Space Technology Research Institutes** are documented as 5-year, up-to-$3M/year institute awards aimed at model-based certification for additive manufacturing aerospace products (relevant to alloy qualification and digital-thread/digital-twin approaches). (vickers2022nasaadvisorycounciltechnology media ab2601d1)

### 4) Visible gaps / opportunities for a DOE Genesis Mission (FLAIME) narrative
- **Sparse paper-level award metadata in alloy/MI-ML journals**: even when NASA programs (e.g., ULI) are mentioned, award numbers are often absent or truncated in accessible full-text excerpts, limiting visibility into PI-level NASA funding from the open literature alone. (jiang2024deeplearningapproaches pages 13-13)
- **Opportunity: tighter coupling to closed-loop autonomy**: ARMD T3 materials informatics documents emphasize informatics tools, digital-thread management, and multiscale modeling/qualification; fewer explicit, award-numbered examples are visible that fund *autonomous closed-loop alloy discovery* as an end-to-end experimental loop, suggesting a gap NASA could fill (or partner with DOE) for autonomous materials labs and foundation-model-driven inverse design specifically for metallic alloys. (arnold20252040visionstudy pages 9-13, stuckner2022designofmaterials pages 1-5)
- **Opportunity: bridge STMD institute-scale AM certification with alloy discovery**: STMD’s STRI mechanism is explicitly sized for multi-year, multi-institution programs (up to $3M/year for 5 years) and is framed around model-based certification of AM aerospace products, creating a plausible on-ramp for autonomous, ML-driven alloy/process co-design and qualification workflows. (vickers2022nasaadvisorycounciltechnology media ab2601d1)


References

1. (arnold20252040visionstudy pages 9-13): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

2. (bhandari2023machinelearningbasedthermalconductivity pages 13-15): Uttam Bhandari, Yehong Chen, Huan Ding, Congyuan Zeng, Selami Emanet, Paul R. Gradl, and Shengmin Guo. Machine-learning-based thermal conductivity prediction for additively manufactured alloys. Journal of Manufacturing and Materials Processing, 7:160, Sep 2023. URL: https://doi.org/10.3390/jmmp7050160, doi:10.3390/jmmp7050160. This article has 27 citations.

3. (wu2022ml4lmmachinelearning pages 3-5): DD Wu, WT Chung, and M Ihme. Ml4lm: machine learning for safely landing on mars. Unknown journal, 2022.

4. (stuckner2022designofmaterials pages 1-5): J Stuckner, TM Whitehead, RC Parini, and GJ Conduit. Design of materials with alchemite. Unknown journal, 2022.

5. (arnold20252040visionstudyc pages 9-13): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

6. (vickers2022nasaadvisorycounciltechnology media ab2601d1): J Vickers. Nasa advisory council-technology, innovation, and engineering committee-advanced manufacturing. Unknown journal, 2022.

7. (bhandari2023machinelearningbasedthermalconductivity pages 11-13): Uttam Bhandari, Yehong Chen, Huan Ding, Congyuan Zeng, Selami Emanet, Paul R. Gradl, and Shengmin Guo. Machine-learning-based thermal conductivity prediction for additively manufactured alloys. Journal of Manufacturing and Materials Processing, 7:160, Sep 2023. URL: https://doi.org/10.3390/jmmp7050160, doi:10.3390/jmmp7050160. This article has 27 citations.

8. (arnold20252040visionstudya pages 9-13): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

9. (arnold20252040visionstudyb pages 9-13): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

10. (datta2020puttinguniversitiesin pages 11-12): Koushik Datta, John A. Cavolowsky, and Richard Barhydt. Putting universities in charge yields early success for nasa aeronautics. 2020 AIAA/IEEE Electric Aircraft Technologies Symposium (EATS), pages 1-12, Aug 2020. URL: https://doi.org/10.2514/6.2020-3570, doi:10.2514/6.2020-3570. This article has 1 citations.

11. (valcoUnknownyearnasaepscorrapid pages 6-9): MJ Valco. Nasa epscor rapid response research (r3)–fy24 research topics. Unknown journal, Unknown year.

12. (valcoUnknownyearnasaepscorrapid pages 60-63): MJ Valco. Nasa epscor rapid response research (r3)–fy24 research topics. Unknown journal, Unknown year.

13. (vickers2022nasaadvisorycounciltechnologya pages 13-19): J Vickers. Nasa advisory council-technology, innovation, and engineering committee-advanced manufacturing. Unknown journal, 2022.

14. (jiang2024deeplearningapproaches pages 13-13): Runbo Jiang, John Smith, Yu-Tsen Yi, Tao Sun, Brian J. Simonds, and Anthony D. Rollett. Deep learning approaches for instantaneous laser absorptance prediction in additive manufacturing. npj Computational Materials, 10:1-13, Jan 2024. URL: https://doi.org/10.1038/s41524-023-01172-8, doi:10.1038/s41524-023-01172-8. This article has 14 citations and is from a peer-reviewed journal.
