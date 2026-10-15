# Funding trends: ml materials informatics — DOE

*Edison `LITERATURE` task `06e94589-9247-4927-92a6-fdecb4e3f129` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
machine learning for materials informatics to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: machine learning for materials informatics, property prediction, and inverse alloy design (graph neural networks, transformers, foundation models, generative models for materials)

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


## Executive summary (DOE posture, 2020–2026 sample)
Across the 2020–2026 materials-informatics literature sampled here, DOE support for ML-enabled materials discovery appears in three dominant forms: (i) ARPA‑E awards supporting closed-loop/accelerated discovery workflows, including repeated acknowledgements of a single ARPA‑E award across multiple ML+autonomy papers; (ii) Office of Science/BES awards supporting materials property/transport characterization and data-driven modeling in compositionally complex alloys; and (iii) DOE user-facility and computing allocations (NERSC, APS, NSLS‑II) that underpin the compute and characterization backbone required for modern data-centric materials discovery. (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11, deng2020semiconductinghighentropychalcogenide pages 6-8, chen2023ultrasmallamorphouszirconia pages 13-13, maffettone2023whatismissing pages 11-11)
National-lab internal investment is visible via Laboratory Directed Research and Development (LDRD), with a specific Brookhaven LDRD project explicitly titled around a “robotic beamline scientist” for self-driving scattering studies, consistent with DOE’s emphasis on autonomy-enabling infrastructure. (maffettone2023whatismissing pages 11-11)
Within this sampled corpus, explicit acknowledgements to BES DMSE, EFRCs, Office of Science Early Career, EERE/AMMTO, and NETL/FECM awards were sparse/absent, suggesting either (a) they are less frequently used in this narrow subtopic slice, or (b) additional targeted literature sampling is needed for those mechanisms. (zhu2024differentiablemodelingand pages 11-11, kavalsky2023byhowmuch pages 23-27, deng2020semiconductinghighentropychalcogenide pages 6-8)

## Funded projects (extracted from acknowledgements)
| Agency/program | Award/contract number(s) | PI(s) & institution | Amount | Project title/short description | Start/period | Papers acknowledging it |
|---|---|---|---|---|---|---|
| DOE ARPA-E | DE-AR0001211 | Venkatasubramanian Viswanathan and coauthors; institution not stated in acknowledgement, paper authors affiliated with Carnegie Mellon University and collaborators | not stated | Supported machine-learning-driven closed-loop materials discovery workflows and robotic electrolyte optimization. In the cited papers, it enabled benchmark studies of how much closed-loop frameworks accelerate computational materials discovery and differentiable geometric deep learning for electrolyte optimization. (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11) | not stated | kavalsky2023byhowmuch; zhu2024differentiablemodelingand (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11) |
| DOE ARPA-E | DE-AR-0001541 | not stated in paper; alloy paper authors are Matthew Taryn Vigil, Caleb Hatler, Bochuan Sun, Ishtiaque K. Robin, Skye Supakul, Saryu Fensin, Osman El Atwani, Enrique Martinez, Dan J. Thoma; institutions not explicitly given in acknowledgement | not stated | Financial support for computational screening, fabrication, and characterization of WTaCrV-Hf refractory multi-principal element alloys. The project used order-disorder transition temperature as a high-throughput alloy-design metric to down-select promising high-temperature compositions. (vigil2026designprocessingand pages 13-14) | not stated | vigil2026designprocessingand (vigil2026designprocessingand pages 13-14) |
| DOE Office of Basic Energy Sciences | DE-SC-00018941 | not stated in paper; thermoelectric measurements support in paper by Zihao Deng, Alan Olvera, Joseph Casamento, Juan S. Lopez, Logan Williams, Ruiming Lu, Guangsha Shi, Pierre F. P. Poudeu, Emmanouil Kioupakis (University of Michigan authorship context) | not stated | Supported thermoelectric properties measurements for semiconducting high-entropy chalcogenide alloys. The work combined high-throughput DFT and machine learning with experiment to establish ambipolar doping and transport behavior in entropy-stabilized chalcogenides. (deng2020semiconductinghighentropychalcogenide pages 6-8) | not stated | deng2020semiconductinghighentropychalcogenide (deng2020semiconductinghighentropychalcogenide pages 6-8) |
| DOE Office of Science User Facility, National Synchrotron Light Source II (Brookhaven National Laboratory) | DE-SC0012704 | not stated in paper; facility operated by Brookhaven National Laboratory; user explicitly identified as P.M. = Phillip M. Maffettone | not stated | User-facility support for autonomous discovery / self-driving laboratory work, specifically real-time and self-driving total scattering / beamline studies. The acknowledgement is to use of NSLS-II resources rather than a PI award. (maffettone2023whatismissing pages 11-11) | not stated | maffettone2023whatismissing (maffettone2023whatismissing pages 11-11) |
| Brookhaven National Laboratory LDRD | 23-039 | not stated in paper; associated user/author is Phillip M. Maffettone, Brookhaven-linked acknowledgement | not stated | Project titled “Extensible robotic beamline scientist for self-driving total scattering studies.” It supported autonomous beamline and self-driving materials characterization capabilities discussed in the perspective on autonomous discovery. (maffettone2023whatismissing pages 11-11) | not stated | maffettone2023whatismissing (maffettone2023whatismissing pages 11-11) |
| DOE Office of Science User Facility, Advanced Photon Source (Argonne National Laboratory) | AC02-06CH11357 | not stated in paper; acknowledgement ties use to authors L.F., T.L., and B.L.; facility operated by Argonne National Laboratory | not stated | User-facility support for synchrotron characterization in catalysis/materials research. In the cited paper it enabled Advanced Photon Source measurements associated with data-rich study of ultrasmall amorphous zirconia nanoparticles and their catalytic behavior. (chen2023ultrasmallamorphouszirconia pages 13-13) | not stated | chen2023ultrasmallamorphouszirconia (chen2023ultrasmallamorphouszirconia pages 13-13) |
| DOE Office of Science User Facility, NERSC | DE-AC02-05CH11231 | not stated in paper; in chen2023ultrasmallamorphouszirconia tied to K.-E.Y., S.C.A., and A.H.; in deng2020semiconductinghighentropychalcogenide tied to DFT calculations by authors including Zihao Deng and Emmanouil Kioupakis | not stated | User-facility computational support for DOE-funded materials modeling. Across the cited papers, NERSC enabled DFT and large-scale computation for high-entropy chalcogenide alloy property prediction and for catalytic/materials simulations. (chen2023ultrasmallamorphouszirconia pages 13-13, deng2020semiconductinghighentropychalcogenide pages 6-8) | not stated | chen2023ultrasmallamorphouszirconia; deng2020semiconductinghighentropychalcogenide (chen2023ultrasmallamorphouszirconia pages 13-13, deng2020semiconductinghighentropychalcogenide pages 6-8) |
| DOE National Nuclear Security Administration | DE-NA0004196 | not stated in paper; additional support acknowledged by Matthew Taryn Vigil in the alloy paper; institution not stated in acknowledgement | not stated | Additional support for refractory multi-principal element alloy design and characterization reported in the WTaCrV-Hf study. The acknowledgement does not provide a project title beyond the NNSA award number. (vigil2026designprocessingand pages 13-14) | not stated | vigil2026designprocessingand (vigil2026designprocessingand pages 13-14) |
| DOE National Nuclear Security Administration | DE-NA0003921 | not stated in paper; additional support acknowledged by Matthew Taryn Vigil in the alloy paper; institution not stated in acknowledgement | not stated | Additional support for refractory multi-principal element alloy design and characterization reported in the WTaCrV-Hf study. The acknowledgement does not provide a project title beyond the NNSA award number. (vigil2026designprocessingand pages 13-14) | not stated | vigil2026designprocessingand (vigil2026designprocessingand pages 13-14) |


*Table: This table compiles distinct DOE-related awards and facility contracts explicitly acknowledged in the retrieved materials-ML and alloy-design literature. It is useful as a de-duplicated starting point for mapping DOE programs, award numbers, and associated investigators/institutions for this topic area.*

## Trends (evidence-backed from extracted acknowledgements)

### 1) Programs/sub-programs visibly active in this topic slice
- **ARPA‑E as a recurring funder of ML-enabled closed-loop discovery**: The same ARPA‑E award number (**DE‑AR0001211**) is acknowledged in both a closed-loop computational acceleration study and a differentiable geometric-deep-learning + robotic optimization electrolyte study, indicating continued ARPA‑E investment in autonomy/closed-loop paradigms that are highly relevant to self-driving alloy discovery. (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11)
- **ARPA‑E appears in alloy-relevant “high-throughput alloy design” work**: A refractory multi-principal element alloy paper explicitly acknowledges DOE/ARPA‑E **DE‑AR‑0001541**, showing ARPA‑E reach into compositionally complex alloy design workflows (screening + fabrication + validation). (vigil2026designprocessingand pages 13-14)
- **Office of Science/BES supports compositionally complex alloy property work**: A high-entropy chalcogenide alloy paper acknowledges BES support via **DE‑SC‑00018941**, tied specifically to thermoelectric properties measurement and accompanying DFT+ML modeling. (deng2020semiconductinghighentropychalcogenide pages 6-8)

### 2) Institutions and PIs dominating (as can be inferred from this sample)
- **Venkatasubramanian Viswanathan’s group and collaborators** are repeatedly associated with the ARPA‑E award **DE‑AR0001211** across multiple papers on closed-loop acceleration and differentiable modeling/optimization, indicating a concentration of ARPA‑E-supported autonomy work in that network. (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11)
- **Brookhaven National Laboratory (BNL)** appears as a hub for autonomy-enabling infrastructure via explicit acknowledgement of NSLS‑II user-facility support (contract **DE‑SC0012704**) and a named **BNL LDRD project 23‑039** on a robotic beamline scientist for self-driving total scattering. (maffettone2023whatismissing pages 11-11)
- **Argonne National Laboratory and Lawrence Berkeley National Laboratory** appear primarily as enabling facilities/resources (APS contract **AC02‑06CH11357**; NERSC contract **DE‑AC02‑05CH11231**) rather than as direct “PI award” sources in these acknowledgements. (chen2023ultrasmallamorphouszirconia pages 13-13)

### 3) New agency programs (launched 2022+) visible in the acknowledgements
- **BNL LDRD 23‑039** (explicitly titled around “robotic beamline scientist”) is a FY23-numbered internal project aligned with self-driving characterization; it is a concrete example of post‑2022 autonomy-focused internal investment at a DOE lab. (maffettone2023whatismissing pages 11-11)
- The sampled acknowledgements did **not** explicitly mention ARPA‑E programs by name such as “ULTIMATE” or “DIFFERENTIATE” (even when papers discussed related themes), so program-level mapping (ULTIMATE/DIFFERENTIATE) could not be confirmed from acknowledgement text in this evidence set. (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11)

### 4) Visible gaps / opportunities (inferred cautiously from what was *not* acknowledged)
- **BES DMSE, EFRCs, and Office of Science Early Career**: none were explicitly acknowledged in the extracted materials-ML/alloy-design papers here, despite strong topical alignment. This may indicate that these mechanisms are either underrepresented in this small literature sample or are being acknowledged in different sub-literatures (e.g., DMSE-led alloy datasets, EFRC autonomy platforms) not captured by the current retrieval. (deng2020semiconductinghighentropychalcogenide pages 6-8, kavalsky2023byhowmuch pages 23-27)
- **EERE/AMMTO and NETL/FECM**: no explicit award numbers from these offices were found in the acknowledgements extracted here, suggesting an opportunity area if DOE wishes to expand autonomy/ML into manufacturing-relevant alloy processing (AMMTO) or carbon/materials systems (NETL) with closed-loop design. (deng2020semiconductinghighentropychalcogenide pages 6-8, kavalsky2023byhowmuch pages 23-27)

### Notes on scope/limitations
This summary is strictly based on explicit acknowledgement/funding statements recoverable in the retrieved full texts and therefore reflects the biases of the sampled corpus (and of what authors choose to acknowledge). Quantitative statements about program growth/shrinkage across all DOE funding cannot be made from these acknowledgements alone without a broader, systematic corpus plus award-database triangulation. (kavalsky2023byhowmuch pages 23-27, zhu2024differentiablemodelingand pages 11-11, deng2020semiconductinghighentropychalcogenide pages 6-8)

References

1. (kavalsky2023byhowmuch pages 23-27): Lance Kavalsky, Vinay I. Hegde, Eric Muckley, Matthew S. Johnson, Bryce Meredig, and Venkatasubramanian Viswanathan. By how much can closed-loop frameworks accelerate computational materials discovery? Digital Discovery, 2:1112-1125, Jan 2023. URL: https://doi.org/10.1039/d2dd00133k, doi:10.1039/d2dd00133k. This article has 25 citations and is from a peer-reviewed journal.

2. (zhu2024differentiablemodelingand pages 11-11): Shang Zhu, Bharath Ramsundar, Emil Annevelink, Hongyi Lin, Adarsh Dave, Pin-Wen Guan, Kevin Gering, and Venkatasubramanian Viswanathan. Differentiable modeling and optimization of non-aqueous li-based battery electrolyte solutions using geometric deep learning. Nature Communications, Oct 2024. URL: https://doi.org/10.1038/s41467-024-51653-7, doi:10.1038/s41467-024-51653-7. This article has 31 citations and is from a highest quality peer-reviewed journal.

3. (deng2020semiconductinghighentropychalcogenide pages 6-8): Zihao Deng, Alan Olvera, Joseph Casamento, Juan S. Lopez, Logan Williams, Ruiming Lu, Guangsha Shi, Pierre F. P. Poudeu, and Emmanouil Kioupakis. Semiconducting high-entropy chalcogenide alloys with ambi-ionic entropy stabilization and ambipolar doping. Chemistry of Materials, 32:6070-6077, May 2020. URL: https://doi.org/10.1021/acs.chemmater.0c01555, doi:10.1021/acs.chemmater.0c01555. This article has 66 citations and is from a highest quality peer-reviewed journal.

4. (chen2023ultrasmallamorphouszirconia pages 13-13): Shaojiang Chen, Akalanka Tennakoon, Kyung-Eun You, Alexander L. Paterson, Ryan Yappert, Selim Alayoglu, Lingzhe Fang, Xun Wu, Tommy Yunpu Zhao, Michelle P. Lapak, Mukunth Saravanan, Ryan A. Hackler, Yi-Yu Wang, Long Qi, Massimiliano Delferro, Tao Li, Byeongdu Lee, Baron Peters, Kenneth R. Poeppelmeier, Salai C. Ammal, Clifford R. Bowers, Frédéric A. Perras, Andreas Heyden, Aaron D. Sadow, and Wenyu Huang. Ultrasmall amorphous zirconia nanoparticles catalyse polyolefin hydrogenolysis. Nature Catalysis, 6:161-173, Feb 2023. URL: https://doi.org/10.1038/s41929-023-00910-x, doi:10.1038/s41929-023-00910-x. This article has 164 citations and is from a domain leading peer-reviewed journal.

5. (maffettone2023whatismissing pages 11-11): Phillip M. Maffettone, Pascal Friederich, Sterling G. Baird, Ben Blaiszik, Keith A. Brown, Stuart I. Campbell, Orion A. Cohen, Rebecca L. Davis, Ian T. Foster, Navid Haghmoradi, Mark Hereld, Howie Joress, Nicole Jung, Ha-Kyung Kwon, Gabriella Pizzuto, Jacob Rintamaki, Casper Steinmann, Luca Torresi, and Shijing Sun. What is missing in autonomous discovery: open challenges for the community. Digital Discovery, 2:1644-1659, Apr 2023. URL: https://doi.org/10.48550/arxiv.2304.11120, doi:10.48550/arxiv.2304.11120. This article has 50 citations and is from a peer-reviewed journal.

6. (vigil2026designprocessingand pages 13-14): Matthew Taryn Vigil, Caleb Hatler, Bochuan Sun, Ishtiaque K. Robin, Skye Supakul, Saryu Fensin, Osman El Atwani, Enrique Martinez, and Dan J. Thoma. Design, processing, and properties of wtacrv-hf multi-principal element alloys. Journal of Materials Engineering and Performance, Mar 2026. URL: https://doi.org/10.1007/s11665-026-13679-4, doi:10.1007/s11665-026-13679-4. This article has 0 citations and is from a peer-reviewed journal.
