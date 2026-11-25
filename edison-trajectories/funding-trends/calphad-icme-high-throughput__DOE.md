# Funding trends: calphad icme high throughput — DOE

*Edison `LITERATURE` task `27c4fa1f-7a50-4e35-8d96-13dd99a8b669` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
CALPHAD/ICME/high-throughput alloy design to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: CALPHAD thermodynamic modeling, ICME (integrated computational materials engineering), and high-throughput experimental alloy design for accelerated alloy discovery

FUNDING SOURCE OF INTEREST: the U.S. Department of Energy (DOE), including ARPA-E (e.g., ULTIMATE, DIFFERENTIATE), Office of Science / Basic Energy Sciences (BES, including DMSE, Early Career Research Program, EFRCs, DMREF-style programs), AMMTO and EERE (e.g., DuAlumin-3D, HPC4Mfg), FECM, NETL, ORNL/Ames Lab/LANL/LLNL/Sandia/Argonne/PNNL/INL national-lab LDRD programs

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
   posture of DOE in this topic.

OUTPUT FORMAT: markdown. Start with the executive summary, then a markdown table of funded
projects, then a "Trends" subsection. Be precise about award numbers. Do not invent data.


# Executive summary (DOE posture, 2020–2026)
Across the mined 2020–2026 CALPHAD/ICME/high‑throughput (HT) alloy-discovery literature, DOE support that is *explicitly acknowledged with award identifiers* clusters strongly into (i) **ARPA‑E** awards for autonomous/closed‑loop refractory/high‑entropy alloy discovery and (ii) **Office of Science / BES** support via **Early Career** (FWP mechanisms at national labs) and **BES Chemical Sciences** computational-infrastructure projects (FWP mechanisms at PNNL). (arroyave2024ultimatebirdshot.final pages 1-5, khatamsaz2023bayesianoptimizationwith pages 14-14, wang2021accelerateddiscoveryof pages 17-18, duong2021afirstprinciplesbasedapproach pages 11-12, gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)
ARPA‑E’s **ULTIMATE** program appears as the most visible, repeated program in this topical slice, including an end‑to‑end closed‑loop alloy discovery effort (ULTIMATE: BIRDSHOT) with a clearly stated period of performance. (arroyave2024ultimatebirdshot.final pages 1-5, khatamsaz2023bayesianoptimizationwith pages 14-14)
BES appears primarily through **national-lab FWPs and operating contracts** rather than university DE‑SC awards in the extracted acknowledgements, emphasizing lab-centered execution and user-facility enablement (e.g., ALS support statements; PNNL contract language). (gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)
Within this evidence set, **EERE/AMMTO/HPC4Mfg/NETL/FECM and lab LDRD** are not prominently/explicitly acknowledged with award numbers, suggesting either (a) these programs are funding adjacent work that is not captured by the current literature slice, or (b) acknowledgements frequently omit program identifiers for these sources. (wang2021accelerateddiscoveryof pages 17-18, duong2021afirstprinciplesbasedapproach pages 11-12, gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)

# DOE-funded projects acknowledged in recent literature
| PI name(s) and institution | DOE agency/sub-program & program name | Award/contract/FWP number(s) | Award amount | Period of performance / start year | Short project title / description | Citing paper(s) |
|---|---|---|---|---|---|---|
| Dr. Raymundo Arróyave, Texas A&M University | DOE ARPA-E ULTIMATE Program | DE-AR0001427 | not stated | 4/26/2021–7/25/2023 | **ULTIMATE: BIRDSHOT**. Closed-loop Bayesian alloy design for refractory high-entropy alloys aimed at turbine-relevant operation above 1300°C, coupling high-throughput CALPHAD, synthesis, and characterization. (arroyave2024ultimatebirdshot.final pages 1-5) | arroyave2024ultimatebirdshot.final; khatamsaz2023bayesianoptimizationwith |
| not stated | DOE ARPA-E | DE-AR0001050 | not stated | not stated | Accelerated discovery of molten-salt corrosion-resistant alloys using high-throughput experiments, thermodynamic/kinetic modeling, and data analytics. (wang2021accelerateddiscoveryof pages 17-18) | wang2021accelerateddiscoveryof |
| not stated | DOE ARPA-E | PRJ1007310 | not stated | not stated | First-principles/Bayesian CALPHAD screening of corrosion-resistant high-entropy alloys, using DFT and hypothesis-based high-throughput selection. (duong2021afirstprinciplesbasedapproach pages 11-12) | duong2021afirstprinciplesbasedapproach |
| not stated | DOE Office of Science, Office of Basic Energy Sciences, Materials Sciences and Engineering Division, Early Career Research Program | FWP 76052 | not stated | not stated | PNNL work on oxidation mechanisms in CoCrFeNiMn high-entropy alloys, combining in-situ/advanced characterization with thermodynamic interpretation of oxide growth. (gwalani2024mechanisticunderstandingof pages 9-10) | gwalani2024mechanisticunderstandingof |
| not stated | PNNL operating contract for the U.S. DOE | DE-AC05-76RLO1830 | not stated | not stated | PNNL operating contract acknowledged in support of the above Early Career/BES-supported HEA oxidation study. (gwalani2024mechanisticunderstandingof pages 9-10) | gwalani2024mechanisticunderstandingof |
| not stated | DOE Office of Science, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences, and Biosciences, TEC4 project | FWP 82037 | not stated | not stated | **TEC4**: “Transferring exascale computational chemistry to cloud computing environment and emerging hardware technologies,” acknowledged in a paper on uncertainty quantification for neural-network interatomic potentials relevant to high-entropy materials. (bilbrey2025uncertaintyquantificationfor pages 7-8) | bilbrey2025uncertaintyquantificationfor |
| not stated | DOE Office of Science, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences & Biosciences | FWP 47319 | not stated | not stated | DOE-supported simulation data generation used in the same PNNL study on uncertainty quantification for machine-learning interatomic potentials and HEA datasets. (bilbrey2025uncertaintyquantificationfor pages 7-8) | bilbrey2025uncertaintyquantificationfor |
| not stated | PNNL operating contract for the U.S. DOE | DE-AC05-76RL0-1830 | not stated | not stated | PNNL operating contract acknowledged in support of the TEC4 / simulation-data work underlying the computational materials study. (bilbrey2025uncertaintyquantificationfor pages 7-8) | bilbrey2025uncertaintyquantificationfor |
| not stated | DOE Office of Science, Basic Energy Sciences, Materials Science and Engineering Department; Ames National Laboratory operating contract | DE-AC02-07CH11358 | not stated | not stated | Ames National Laboratory theory development (KKR-CPA and SCRAPs by DDJ/PS) supporting constrained Bayesian optimization for alloy design in the ARPA-E ULTIMATE context. (khatamsaz2023bayesianoptimizationwith pages 14-14) | khatamsaz2023bayesianoptimizationwith |
| not stated | DOE ARPA-E | DE-AR-0001541 | not stated | not stated | Funding acknowledged in a paper on design, processing, and properties of WTaCrV-Hf multi-principal-element alloys. (vigil2026designprocessingand pages 13-14) | vigil2026designprocessingand |
| Matthew Taryn Vigil (MTV), institution not explicitly stated in the cited evidence | DOE / NNSA | DE-NA0004196 | not stated | not stated | Additional DOE/NNSA support acknowledged by MTV in the WTaCrV-Hf alloy study. (vigil2026designprocessingand pages 13-14) | vigil2026designprocessingand |
| Matthew Taryn Vigil (MTV), institution not explicitly stated in the cited evidence | DOE / NNSA | DE-NA0003921 | not stated | not stated | Additional DOE/NNSA support acknowledged by MTV in the WTaCrV-Hf alloy study. (vigil2026designprocessingand pages 13-14) | vigil2026designprocessingand |


*Table: This table compiles DOE-related funded projects explicitly acknowledged in recent CALPHAD/ICME/high-throughput alloy-design papers and reports, with exact award identifiers, any explicitly stated PI/institution details, and the citing papers that acknowledged each award.*

# Trends (from the extracted acknowledgements)
## 1) Which DOE sub-programs are growing vs. shrinking (as visible in acknowledgements)
- **Growing/most visible:** **DOE ARPA‑E** for HT/closed‑loop alloy discovery and ICME-style optimization loops, with multiple distinct award identifiers appearing across alloy discovery and screening papers (DE‑AR0001427; DE‑AR0001050; PRJ1007310; DE‑AR‑0001541). (arroyave2024ultimatebirdshot.final pages 1-5, wang2021accelerateddiscoveryof pages 17-18, duong2021afirstprinciplesbasedapproach pages 11-12, vigil2026designprocessingand pages 13-14)
- **Visible in lab-executed foundational work:** **DOE Office of Science / BES** via **FWP-funded efforts** at PNNL (e.g., Early Career FWP 76052; BES Chemical Sciences FWPs 82037 and 47319), indicating sustained support for enabling science and computational workflows relevant to thermodynamics/ML potentials that feed CALPHAD/ICME pipelines. (gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)
- **Not inferable from this corpus:** growth/shrinkage for **EERE/AMMTO**, **NETL/FECM**, or **national-lab LDRD** in CALPHAD/ICME/HT alloy design, because explicit award acknowledgements for those programs did not appear in the extracted funding sections. (wang2021accelerateddiscoveryof pages 17-18, duong2021afirstprinciplesbasedapproach pages 11-12, bilbrey2025uncertaintyquantificationfor pages 7-8)

## 2) Which institutions and PIs are dominating (within the extracted set)
- **Texas A&M University / Raymundo Arróyave** is the clearest repeatedly identified PI/institution pair in this slice, tied to ARPA‑E ULTIMATE **DE‑AR0001427** and the ULTIMATE: BIRDSHOT final report. (arroyave2024ultimatebirdshot.final pages 1-5, khatamsaz2023bayesianoptimizationwith pages 14-14)
- **PNNL** appears repeatedly as the execution site for BES-funded work through FWPs and with explicit lab operating-contract language, indicating strong national-lab participation in enabling computational/materials‑informatics infrastructure relevant to alloy design. (gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)
- **Ames National Laboratory** appears in the context of theory development supporting alloy design frameworks, with explicit BES/MSE support and the Ames operating contract **DE‑AC02‑07CH11358**. (khatamsaz2023bayesianoptimizationwith pages 14-14)

## 3) New agency programs (launched 2022+) funding this topic (as visible here)
- The most explicit *program-branded* appearance is **ARPA‑E ULTIMATE** (active during 2021–2023 performance for BIRDSHOT) as a funding vehicle for autonomous/HT alloy discovery tied to refractory/high‑entropy alloy design constraints. (arroyave2024ultimatebirdshot.final pages 1-5, khatamsaz2023bayesianoptimizationwith pages 14-14)
- In the BES space, the evidence shows **FWP-structured support** (e.g., **FWP 76052** Early Career; **FWP 82037/47319** Chemical Sciences) rather than a new named “program launch”; these mechanisms indicate continued and potentially expanding support for data and compute infrastructure that can be leveraged in closed-loop alloy discovery. (gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)

## 4) Gaps/opportunities for DOE (based on what is *not* showing up in acknowledgements)
- **Limited explicit DE‑SC university awards**: within this extracted set, DOE Office of Science support appears mostly via lab FWPs/contracts rather than explicit DE‑SC grant numbers; proposals emphasizing university–lab teaming with clear DE‑SC alignment (e.g., DMSE) may fill a visibility and coordination gap. (gwalani2024mechanisticunderstandingof pages 9-10, bilbrey2025uncertaintyquantificationfor pages 7-8)
- **Sparse explicit AMMTO/EERE/NETL/FECM/LDRD identifiers**: the absence of these sources in the mined acknowledgements suggests an opportunity to position autonomous CALPHAD/ICME/HT alloy discovery more directly toward manufacturing deployment (AMMTO/EERE) or energy‑sector alloy needs (NETL/FECM), with explicit program tagging and publication acknowledgement practices to improve traceability. (wang2021accelerateddiscoveryof pages 17-18, duong2021afirstprinciplesbasedapproach pages 11-12, bilbrey2025uncertaintyquantificationfor pages 7-8)

## Notes on completeness
This report is **strictly limited to awards explicitly acknowledged with identifiers** in the retrievable full text available in this run. Several relevant technical papers in this topic area were retrieved but did not include funding text in the available chunks or were unobtainable; consequently, the table should be treated as a **high-precision, incomplete** map of DOE funding (not an exhaustive census). (sauceda2022highthroughputexploration pages 40-43, olson2024genomicmaterialsdesign pages 44-45, vazquez2023adeepneural pages 13-14)

References

1. (arroyave2024ultimatebirdshot.final pages 1-5): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

2. (khatamsaz2023bayesianoptimizationwith pages 14-14): Danial Khatamsaz, Brent Vela, Prashant Singh, Duane D. Johnson, Douglas Allaire, and Raymundo Arróyave. Bayesian optimization with active learning of design constraints using an entropy-based approach. npj Computational Materials, 9:1-14, Apr 2023. URL: https://doi.org/10.1038/s41524-023-01006-7, doi:10.1038/s41524-023-01006-7. This article has 107 citations and is from a peer-reviewed journal.

3. (wang2021accelerateddiscoveryof pages 17-18): Yafei Wang, Bonita Goh, Phalgun Nelaturu, Thien Duong, Najlaa Hassan, Raphaelle David, Michael Moorehead, Santanu Chaudhuri, Adam Creuziger, Jason Hattrick-Simpers, Dan J. Thoma, Kumar Sridharan, and Adrien Couet. Accelerated discovery of molten salt corrosion-resistant alloy by high-throughput experimental and modeling methods coupled to data analytics. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2104.10235, doi:10.48550/arxiv.2104.10235. This article has 7 citations.

4. (duong2021afirstprinciplesbasedapproach pages 11-12): Thien Duong, Yafei Wang, Xiaoli Yan, Adrien Couet, and Santanu Chaudhuri. A first-principles-based approach to the high-throughput screening of corrosion-resistant high entropy alloys. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2104.10590, doi:10.48550/arxiv.2104.10590. This article has 5 citations.

5. (gwalani2024mechanisticunderstandingof pages 9-10): Bharat Gwalani, Andrew Martin, Elizabeth Kautz, Boyu Guo, S. V. Lambeets, Matthew Olszta, Anil Krishna Battu, Aniruddha Malakar, Feipeng Yang, Jinghua Guo, Suntharampillai Thevuthasan, Ruipeng Li, Aram Amassian, Martin Thuo, and Arun Devaraj. Mechanistic understanding of speciated oxide growth in high entropy alloys. Nature Communications, Jun 2024. URL: https://doi.org/10.1038/s41467-024-49243-8, doi:10.1038/s41467-024-49243-8. This article has 44 citations and is from a highest quality peer-reviewed journal.

6. (bilbrey2025uncertaintyquantificationfor pages 7-8): Jenna A. Bilbrey, Jesun S. Firoz, Mal-Soon Lee, and Sutanay Choudhury. Uncertainty quantification for neural network potential foundation models. npj Computational Materials, Apr 2025. URL: https://doi.org/10.1038/s41524-025-01572-y, doi:10.1038/s41524-025-01572-y. This article has 18 citations and is from a peer-reviewed journal.

7. (vigil2026designprocessingand pages 13-14): Matthew Taryn Vigil, Caleb Hatler, Bochuan Sun, Ishtiaque K. Robin, Skye Supakul, Saryu Fensin, Osman El Atwani, Enrique Martinez, and Dan J. Thoma. Design, processing, and properties of wtacrv-hf multi-principal element alloys. Journal of Materials Engineering and Performance, Mar 2026. URL: https://doi.org/10.1007/s11665-026-13679-4, doi:10.1007/s11665-026-13679-4. This article has 0 citations and is from a peer-reviewed journal.

8. (sauceda2022highthroughputexploration pages 40-43): Daniel J Sauceda, Prashant Singh, Gaoyuan Ouyang, Olena Palasyuk, Matthew J Kramer, and Raymundo Arroyave. High throughput exploration of the oxidation landscape in high entropy alloys. Materials horizons, 9:2644-2663, Aug 2022. URL: https://doi.org/10.1039/d2mh00729k, doi:10.1039/d2mh00729k. This article has 18 citations and is from a domain leading peer-reviewed journal.

9. (olson2024genomicmaterialsdesign pages 44-45): G.B. Olson and Z.K. Liu. Genomic materials design: calculation of phase dynamics. Calphad, 82:102590, Sep 2024. URL: https://doi.org/10.1016/j.calphad.2023.102590, doi:10.1016/j.calphad.2023.102590. This article has 29 citations.

10. (vazquez2023adeepneural pages 13-14): G. Vazquez, S. Chakravarty, R. Gurrola, and R. Arróyave. A deep neural network regressor for phase constitution estimation in the high entropy alloy system al-co-cr-fe-mn-nb-ni. npj Computational Materials, 9:1-14, Apr 2023. URL: https://doi.org/10.1038/s41524-023-01021-8, doi:10.1038/s41524-023-01021-8. This article has 36 citations and is from a peer-reviewed journal.
