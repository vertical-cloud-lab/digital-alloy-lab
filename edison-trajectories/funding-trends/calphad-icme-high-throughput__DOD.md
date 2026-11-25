# Funding trends: calphad icme high throughput — DOD

*Edison `LITERATURE` task `169cf02a-e19e-46bc-b8d8-85ead864cb63` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
CALPHAD/ICME/high-throughput alloy design to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: CALPHAD thermodynamic modeling, ICME (integrated computational materials engineering), and high-throughput experimental alloy design for accelerated alloy discovery

FUNDING SOURCE OF INTEREST: the U.S. Department of Defense (DOD, recently being renamed Department of War / DOW), including ARO (Army Research Office), AFOSR (Air Force Office of Scientific Research), ONR (Office of Naval Research), DARPA (incl. DSO programs like Make-It, AMD, Materials Architectures and Characterization for Hypersonics), ARL (Army Research Laboratory, including HTMDEC), AFRL, NRL — and DOD-wide programs such as DURIP, MURI, YIP, Vannevar Bush Faculty Fellowship, NDSEG

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
   posture of DOD/DOW in this topic.

OUTPUT FORMAT: markdown. Start with the executive summary, then a markdown table of funded
projects, then a "Trends" subsection. Be precise about award numbers. Do not invent data.


## Executive summary (DoD/DOW posture, 2020–2026 literature)
Recent DoD-acknowledged funding in CALPHAD/ICME/high-throughput alloy discovery is concentrated in (i) AFOSR MURI-scale investments supporting autonomous/ML-enabled, high-throughput characterization and phase mapping, and (ii) ONR support spanning both infrastructure (DURIP) and more recent computational/alloy-design awards. (yu2025automatedphasemapping pages 7-8, ament2021autonomousmaterialssynthesis pages 11-12, vecchio2021highthroughputrapidexperimental pages 11-13, krajewski2024efficientmaterialsinformatics pages 20-24)
Across the sampled 2021–2025 papers, explicit DARPA visibility is limited (one paper naming DARPA+ARO with a single award), while AFRL appears mainly through facility/network support (MSN-C at CHESS) rather than multiple topic-specific PI awards. (ament2021autonomousmaterialssynthesis pages 11-12, lee2022acomparisonof pages 14-15)
The dominant funded themes are: automated/high-throughput experimentation and characterization (XRD/EBSD/indentation), autonomous experiment–analysis loops, and data/ML infrastructure that can be coupled to CALPHAD/ICME workflows; fewer acknowledgements explicitly target CALPHAD database development itself. (vecchio2021highthroughputrapidexperimental pages 11-13, olson2024genomicmaterialsdesign pages 34-40, yu2025automatedphasemapping pages 7-8)
Overall, DoD’s literature-visible posture emphasizes enabling autonomous closed-loop discovery via high-throughput measurement + ML/optimization and computational screening, with ONR and AFOSR as the most consistently named sponsors in these topic-adjacent papers. (yu2025automatedphasemapping pages 7-8, qi2024integrateddesignof pages 14-14, krajewski2024efficientmaterialsinformatics pages 20-24)

## DoD/DOW-funded projects acknowledged in 2020–2026 topic literature
| DoD component / program | Award number(s) | PI name(s) and institution | Award amount | Project title / short description | Period of performance / year started | Paper(s) acknowledging | Evidence citation IDs |
|---|---|---|---|---|---|---|---|
| AFOSR MURI | FA9550-18-1-0136 | Sean D. Griesemer and Chris Wolverton, Northwestern University (authors S.G. and C.W. explicitly tied to the award in one paper); also acknowledged in the Cornell/Cornell-Caltech autonomous synthesis work without PI attribution in the funding line | not stated | Supported automated phase mapping of high-throughput XRD data using thermodynamics/crystallography-informed algorithms for combinatorial materials libraries; also supported autonomous nonequilibrium phase-diagram mapping and closed-loop synthesis/characterization workflows. | started by 2018 (from award number); exact period not stated | yu2025automatedphasemapping; ament2021autonomousmaterialssynthesis | (yu2025automatedphasemapping pages 7-8, ament2021autonomousmaterialssynthesis pages 11-12) |
| AFRL support for Materials Solutions Network at CHESS (MSN-C) | FA8650-19-2-5220 | Materials Solutions Network at CHESS (facility support; specific PI not stated in funding excerpt) | not stated | Facility/infrastructure support for the Materials Solutions Network at CHESS used in autonomous materials synthesis and active-learning mapping of nonequilibrium phase diagrams. | started by 2019 (from award number); exact period not stated | ament2021autonomousmaterialssynthesis | (ament2021autonomousmaterialssynthesis pages 11-12) |
| DARPA + Army Research Office | W911NF-20-1-0289 | Not explicitly named in funding line; conservatively attributable to Prasanna V. Balachandran, University of Virginia, as corresponding author on the paper | not stated | Sponsored machine-learning research on phase classification of multi-principal element alloys, specifically explainable-AI methods for interpreting alloy phase predictions. | started by 2020 (from award number); exact period not stated | lee2022acomparisonof | (lee2022acomparisonof pages 14-15) |
| ONR DURIP | N00014-16-1-2983 | Kenneth S. Vecchio, University of California San Diego (corresponding author; funding statement ties award to development of customized Formalloy DED chamber used in the lab) | not stated | Equipment award supporting development of a customized Formalloy blown-powder directed energy deposition chamber used for high-throughput rapid experimental alloy development (HT-READ). | started by 2016 (from award number); exact period not stated | vecchio2021highthroughputrapidexperimental | (vecchio2021highthroughputrapidexperimental pages 11-13, vecchio2021highthroughputrapidexperimental media ce192088) |
| DoD NDSEG fellowship | not stated | Kevin R. Kaufmann, University of California San Diego | not stated | Graduate fellowship support for K.R.K. contributing to HT-READ, an integrated closed-loop bulk alloy screening and characterization workflow. | not stated | vecchio2021highthroughputrapidexperimental | (vecchio2021highthroughputrapidexperimental pages 11-13) |
| ONR | N00014-17-1-2567; N00014-23-2721 | Not stated in funding excerpt; dissertation author Adam M. Krajewski, Pennsylvania State University, acknowledges these ONR awards | not stated | Supported CALPHAD/AI-enabled materials informatics infrastructure for refractory high-entropy alloys, functionally graded materials, and hypersonics-oriented alloy design. | started by 2017 and 2023 respectively (from award numbers); exact periods not stated | krajewski2024efficientmaterialsinformatics | (krajewski2024efficientmaterialsinformatics pages 20-24) |
| ONR | N00014-21-1-2608 | Z.K. Liu, Pennsylvania State University | not stated | Supported computational materials design/CALPHAD research discussed in a perspective on genomic materials design and CALPHAD-based materials genome methods. | started by 2021 (from award number); exact period not stated | olson2024genomicmaterialsdesign | (olson2024genomicmaterialsdesign pages 34-40) |
| ONR (support acknowledged, no program specified) | not stated | G.B. Olson, MIT and QuesTek Innovations | not stated | Support for computational materials design research in CALPHAD/genomic materials design. | not stated | olson2024genomicmaterialsdesign | (olson2024genomicmaterialsdesign pages 34-40) |
| Army Research Lab + Air Force Research Office/Air Force Research Office (named, no award numbers provided) | not stated | Z.K. Liu, Pennsylvania State University | not stated | General support for CALPHAD/database/tool development research noted in the genomic materials design perspective; no specific project title or award number given in the acknowledgement excerpt. | not stated | olson2024genomicmaterialsdesign | (olson2024genomicmaterialsdesign pages 34-40) |
| ONR | N00014-23-1-2441 | Jie Qi, Diego Ibarra Hoyos, and Joseph Poon, University of Virginia (explicitly associated in funding statement) | not stated | Supported integrated high-throughput/ICME design of aluminum-enriched refractory B2 high-entropy alloys with improved strength-ductility synergy. | started by 2023 (from award number); exact period not stated | qi2024integrateddesignof | (qi2024integrateddesignof pages 14-14) |
| Army Research Office / DoD-related awards cited in funding statement | FA9550-23-1-0503; W911NF-13-1-0438; W911NF-19-2-0049 | Xuesong Fan and Peter K. Liaw, University of Tennessee (explicitly associated in funding statement) | not stated | Supported alloy-design and characterization work related to refractory high-entropy alloys and ICME-guided high-throughput design. The paper groups these awards with X.F. and P.K.L.; the exact sub-program names are not stated in the excerpt. | started by 2013, 2019, and 2023 respectively (from award numbers); exact periods not stated | qi2024integrateddesignof | (qi2024integrateddesignof pages 14-14) |


*Table: This table consolidates distinct DoD-funded awards acknowledged in the gathered 2020–2026 CALPHAD/ICME/high-throughput alloy-design literature. It deduplicates repeated awards and records the exact award numbers, conservative PI/institution attribution, and the papers where each award was acknowledged.*

## Trends (DoD components/programs, PIs/institutions, new programs, and gaps)

### 1) Sub-program signals (growing vs. shrinking)
* **AFOSR MURI** appears as a persistent, multi-paper backbone funding line for autonomous/high-throughput characterization and algorithmic phase mapping, via award **FA9550-18-1-0136** (acknowledged in both autonomous synthesis/active-learning work and high-throughput XRD phase mapping). (yu2025automatedphasemapping pages 7-8, ament2021autonomousmaterialssynthesis pages 11-12)
* **ONR** shows breadth across time: older infrastructure enabling awards such as **ONR-DURIP N00014-16-1-2983** (equipment for DED/HT-READ) and newer ONR awards in **FY2021–FY2023** series (e.g., **N00014-21-1-2608**, **N00014-23-2721**, **N00014-23-1-2441**) supporting computational/ICME/high-throughput alloy design and informatics. (vecchio2021highthroughputrapidexperimental pages 11-13, olson2024genomicmaterialsdesign pages 34-40, qi2024integrateddesignof pages 14-14, krajewski2024efficientmaterialsinformatics pages 20-24)
* **DARPA (plus ARO)** is visible but not program-resolved in acknowledgements (award **W911NF-20-1-0289** is cited without a DARPA program name such as Make-It/AMD). This suggests either (i) DARPA materials autonomy investments often do not surface as “DARPA program X” in alloy/CALPHAD papers, or (ii) this specific topic slice is more strongly represented in AFOSR/ONR portfolios in the sampled literature. (lee2022acomparisonof pages 14-15)
* **AFRL** appears in the sampled set primarily as **facility/network support** (MSN-C at CHESS, **FA8650-19-2-5220**), rather than multiple distinct PI awards directly naming hypersonics/materials autonomy sub-programs in acknowledgements. (ament2021autonomousmaterialssynthesis pages 11-12)

### 2) Institutions and PIs most visible in acknowledgements
* **Northwestern University (Wolverton/Griesemer)**: explicitly tied to the AFOSR MURI award in high-throughput XRD phase mapping. (yu2025automatedphasemapping pages 7-8)
* **Cornell + Caltech (Gomes/van Dover/Gregoire ecosystem)**: autonomous materials synthesis and hierarchical active learning for nonequilibrium phase diagrams, acknowledging AFOSR and AFRL facility/network support. (ament2021autonomousmaterialssynthesis pages 11-12)
* **Penn State (Zi-Kui Liu lab ecosystem)**: ONR award **N00014-21-1-2608** and ONR acknowledgements in CALPHAD-genomic materials design perspectives; also ONR awards appear in a 2024 dissertation from the same institutional ecosystem. (olson2024genomicmaterialsdesign pages 34-40, krajewski2024efficientmaterialsinformatics pages 20-24)
* **UC San Diego (Vecchio group)**: ONR-DURIP equipment award enabling high-throughput alloy development infrastructure; NDSEG fellowship support. (vecchio2021highthroughputrapidexperimental pages 11-13, vecchio2021highthroughputrapidexperimental media ce192088)
* **University of Virginia / University of Tennessee (Qi/Poon; Liaw/Fan)**: ONR and ARO/DoD-associated awards acknowledged for high-throughput/ICME-driven refractory HEA design. (qi2024integrateddesignof pages 14-14)

### 3) New (2022+) agency programs funding this topic (as visible in literature)
* In the sampled acknowledgement text, the clearest “newer” signals are **new award vintages** rather than explicitly named “new programs”: ONR awards with **FY2023** identifiers (e.g., **N00014-23-2721**, **N00014-23-1-2441**) and DoD-associated awards with **2023** identifiers (e.g., **FA9550-23-1-0503**). (qi2024integrateddesignof pages 14-14, krajewski2024efficientmaterialsinformatics pages 20-24)
* **Program-name visibility is limited**: beyond AFOSR **MURI** and ONR **DURIP**, the acknowledgements rarely name specific DARPA DSO programs (e.g., Make-It, AMD). This is an important practical finding for literature-based portfolio mapping: many DoD awards surface only as agency + award number, not as program title. (lee2022acomparisonof pages 14-15, vecchio2021highthroughputrapidexperimental pages 11-13)

### 4) Visible gaps / opportunities for DoD in this topic area
* **CALPHAD database development and uncertainty quantification**: while CALPHAD/ICME is discussed and supported (e.g., in the genomic materials design perspective), few acknowledgements in the sampled set clearly indicate **DoD-targeted programs specifically for open thermodynamic database expansion, calibration, and UQ** (as distinct from general “materials design” support). (olson2024genomicmaterialsdesign pages 34-40)
* **Explicit autonomous closed-loop alloy discovery with CALPHAD-in-the-loop**: autonomy is strongly represented (AFOSR MURI) and high-throughput alloy experimentation is strongly represented (ONR DURIP + NDSEG-supported work), but there is room for more explicit DoD portfolio emphasis on **end-to-end autonomous closed-loop structural alloy discovery** where CALPHAD acts as a real-time model within the loop (a Genesis/FLAIME-like framing). (ament2021autonomousmaterialssynthesis pages 11-12, vecchio2021highthroughputrapidexperimental pages 11-13)
* **DARPA program attribution**: acknowledgements that include DARPA do not specify DSO program names in the sampled papers, limiting traceability. A portfolio gap for proposal positioning is therefore a **traceable, program-branded autonomy + alloy discovery effort** with explicit links to operationally relevant alloy classes (e.g., hypersonics/refractory systems) and digitally traceable datasets/models. (lee2022acomparisonof pages 14-15, krajewski2024efficientmaterialsinformatics pages 20-24)

### Methodological note (scope limits)
This extraction is limited to DoD awards explicitly acknowledged in the sampled 2021–2025 CALPHAD/ICME/high-throughput alloy literature retrieved here; it should be treated as a **high-precision, not comprehensive** map of DoD funding because acknowledgements are incomplete and program names are often omitted even when awards are present. (olson2024genomicmaterialsdesign pages 34-40, lee2022acomparisonof pages 14-15)

References

1. (yu2025automatedphasemapping pages 7-8): Dongfang Yu, Sean D. Griesemer, Tzu-chen Liu, Chris Wolverton, and Yizhou Zhu. Automated phase mapping of high-throughput x-ray diffraction data encoded with domain-specific materials science knowledge. npj Computational Materials, Nov 2025. URL: https://doi.org/10.1038/s41524-025-01837-6, doi:10.1038/s41524-025-01837-6. This article has 2 citations and is from a peer-reviewed journal.

2. (ament2021autonomousmaterialssynthesis pages 11-12): Sebastian Ament, Maximilian Amsler, Duncan R. Sutherland, Ming-Chiang Chang, Dan Guevarra, Aine B. Connolly, John M. Gregoire, Michael O. Thompson, Carla P. Gomes, and R. Bruce van Dover. Autonomous materials synthesis via hierarchical active learning of nonequilibrium phase diagrams. Science Advances, Dec 2021. URL: https://doi.org/10.1126/sciadv.abg4930, doi:10.1126/sciadv.abg4930. This article has 107 citations and is from a highest quality peer-reviewed journal.

3. (vecchio2021highthroughputrapidexperimental pages 11-13): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.

4. (krajewski2024efficientmaterialsinformatics pages 20-24): Adam M. Krajewski. Efficient materials informatics between rockets and electrons. ArXiv, Jul 2024. URL: https://doi.org/10.48550/arxiv.2407.04648, doi:10.48550/arxiv.2407.04648. This article has 1 citations.

5. (lee2022acomparisonof pages 14-15): Kyungtae Lee, Mukil V. Ayyasamy, Yangfeng Ji, and Prasanna V. Balachandran. A comparison of explainable artificial intelligence methods in the phase classification of multi-principal element alloys. Scientific Reports, Jul 2022. URL: https://doi.org/10.1038/s41598-022-15618-4, doi:10.1038/s41598-022-15618-4. This article has 40 citations and is from a peer-reviewed journal.

6. (olson2024genomicmaterialsdesign pages 34-40): G.B. Olson and Z.K. Liu. Genomic materials design: calculation of phase dynamics. Calphad, 82:102590, Sep 2024. URL: https://doi.org/10.1016/j.calphad.2023.102590, doi:10.1016/j.calphad.2023.102590. This article has 29 citations.

7. (qi2024integrateddesignof pages 14-14): Jie Qi, Xuesong Fan, Diego Ibarra Hoyos, Michael Widom, Peter K. Liaw, and Joseph Poon. Integrated design of aluminum-enriched high-entropy refractory b2 alloys with synergy of high strength and ductility. Science Advances, Dec 2024. URL: https://doi.org/10.1126/sciadv.adq0083, doi:10.1126/sciadv.adq0083. This article has 47 citations and is from a highest quality peer-reviewed journal.

8. (vecchio2021highthroughputrapidexperimental media ce192088): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.
