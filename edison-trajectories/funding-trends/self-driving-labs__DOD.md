# Funding trends: self driving labs — DOD

*Edison `LITERATURE` task `9d958c04-69ef-4779-bd79-7c38ecf020c9` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
self-driving laboratories for materials/alloys to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: self-driving laboratories and autonomous experimentation for materials and metallic alloy discovery (closed-loop AI/robot-controlled synthesis-characterization-design loops, autonomous formulation, autonomous additive manufacturing)

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


## Executive summary (DoD/DOW posture, 2020–2026 literature slice)
Across the 2020–2026 self-driving laboratory / autonomous experimentation literature retrieved and inspected here, DoD support is visible but concentrated in a small number of agencies and award lines: AFOSR appears most frequently (including both standard grants and an AFOSR LRIR), AFRL appears both as direct award support and as infrastructure support (e.g., CHESS MSN-C), ONR appears intermittently through materials/characterization-focused awards, and DARPA appears in at least one contract acknowledged by a key materials-autonomy community perspective paper. (stanev2021artificialintelligencefor pages 10-11, ament2021autonomousmaterialssynthesis pages 11-12, stach2021autonomousexperimentationsystems pages 20-21, alu2025roadmaponembodying pages 72-74, myung2025multiobjectivebayesianoptimization pages 11-12, kunka2021decodingdefectstatistics pages 8-9)
A notable pattern is that DoD funding shows up strongly in “autonomy-enabling” capabilities (autonomous experimentation systems, active learning for synthesis/phase mapping, and autonomous/closed-loop manufacturing experimentation) rather than being tightly labeled by specific SDL-for-alloys program names in acknowledgements. (ament2021autonomousmaterialssynthesis pages 11-12, stach2021autonomousexperimentationsystems pages 20-21, myung2025multiobjectivebayesianoptimization pages 11-12)
In this corpus, newer (2022+) evidence is clearest for AFOSR awards with FY23-style numbering (e.g., FA9550-23-1-0466), while other DoD-wide mechanisms of interest (MURI, DURIP, YIP, NDSEG, Vannevar Bush) were not explicitly acknowledged in the inspected papers. (alu2025roadmaponembodying pages 72-74, ament2021autonomousmaterialssynthesis pages 11-12, stach2021autonomousexperimentationsystems pages 20-21)

## DoD-funded projects acknowledged in recent literature (2020–2026)
| PI(s) and institution | DoD agency/program | Award / contract number(s) | Award amount | Project title / short description | Start year / period | Citation key(s) |
|---|---|---|---|---|---|---|
| Valentin Stanev, Kamal Choudhary, Aaron Gilad Kusne, Johnpierre Paglione, Ichiro Takeuchi; institution not stated in acknowledgement excerpt | ONR; AFOSR | N00014-13-1-0635; N00014-15-1-2222; FA9550-14-10332 | not stated | AI for search and discovery of quantum materials, including data-driven and autonomous-experiment concepts for rapid materials discovery. The paper is a review/perspective rather than a single project report, so this row aggregates the DoD awards explicitly acknowledged there. | not stated | (stanev2021artificialintelligencefor pages 10-11, stanev2021artificialintelligencefor media 076ed439, stanev2021artificialintelligencefor media c61b45de) |
| Sebastian Ament, Maximilian Amsler, Duncan R. Sutherland, Ming-Chiang Chang, Dan Guevarra, Aine B. Connolly, John M. Gregoire, Michael O. Thompson, Carla P. Gomes, R. Bruce van Dover; institution not stated in acknowledgement excerpt | AFOSR; AFRL | FA9550-18-1-0136; FA8650-19-2-5220 | not stated | Autonomous materials synthesis via hierarchical active learning of nonequilibrium phase diagrams (SARA). The work couples robotic synthesis, rapid characterization, and nested active learning to map synthesis phase boundaries and accelerate discovery of metastable oxides. | not stated | (ament2021autonomousmaterialssynthesis pages 11-12) |
| Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, Benji Maruyama; institution not stated in acknowledgement excerpt | AFRL support; AFOSR LRIR; AFOSR grant; DARPA contract | 19RXCOR322; FA9550-18-1-0144; HR001118C0036 | not stated | Community perspective on autonomous experimentation systems for materials development. The acknowledged DoD support underwrites enabling infrastructure, software/licensing context, and research on autonomous experimentation for materials development. | not stated | (stach2021autonomousexperimentationsystems pages 20-21) |
| Kon-Well Wang; institution not stated in acknowledgement excerpt | AFOSR | FA9550-23-1-0466 | not stated | Roadmap on embodying mechano-intelligence and computing in functional materials and structures. The acknowledged AFOSR support appears in a section linking intelligent materials/structures, robotics, and additive-manufacturing-enabled autonomy. | not stated | (alu2025roadmaponembodying pages 72-74) |
| Mark A. Pitt and Jay I. Myung; institution not stated in acknowledgement excerpt | AFOSR | FA9550-21-1-0176 | not stated | Multi-objective Bayesian optimization for AM-ARES material extrusion. The project develops autonomous experimentation and multi-objective optimization for material extrusion as part of an autonomous research system. | not stated | (myung2025multiobjectivebayesianoptimization pages 11-12) |
| Surya R. Kalidindi; Georgia Institute of Technology inferred from acknowledgement text mentioning PACE at Georgia Institute of Technology | ONR | N00014-18-1-2879 | not stated | Machine-learning decoding of defect statistics from diffractograms. The acknowledged ONR support backs autonomous/adaptive materials characterization methods linking simulated diffraction data to defect statistics. | not stated | (kunka2021decodingdefectstatistics pages 8-9, kunka2021decodingdefectstatistics pages 9-9) |
| Ioannis G. Kevrekidis, Nikolaos Evangelou, Noah Wichrowski; institution not stated in acknowledgement excerpt | AFOSR | not stated | not stated | Active learning of ternary alloy structures and energies. The work uses active learning and graph neural-network models to accelerate exploration of ternary alloy/high-entropy-alloy configuration space. | not stated | (deshmukh2024activelearningof pages 10-11) |


*Table: This table normalizes the DoD-related awards explicitly acknowledged in the retrieved 2020–2026 literature on autonomous experimentation and materials discovery. It is useful as a project-level evidence base for identifying agencies, award numbers, and the types of self-driving-lab activities being supported.*

## Trends (from acknowledged awards in this corpus)

### 1) Which sub-programs are growing vs. shrinking (as evidenced here)
- **AFOSR appears to be the most consistently acknowledged DoD funder** across multiple autonomous-experimentation and materials-automation papers, spanning awards with year-codes consistent with 2014, 2018, 2021, and 2023 awards (e.g., FA9550-14-10332; FA9550-18-1-0136; FA9550-21-1-0176; FA9550-23-1-0466). (stanev2021artificialintelligencefor pages 10-11, ament2021autonomousmaterialssynthesis pages 11-12, myung2025multiobjectivebayesianoptimization pages 11-12, alu2025roadmaponembodying pages 72-74)
- **AFOSR intramural mechanism signal:** AFOSR LRIR no. **19RXCOR322** appears in a widely cited community perspective on autonomous experimentation systems, suggesting continued investment in internal exploratory autonomy/infrastructure themes. (stach2021autonomousexperimentationsystems pages 20-21)
- **AFRL as an enabling-infrastructure backer:** AFRL is acknowledged both as broader support (including the Materials & Manufacturing Directorate) and via an award supporting CHESS’s MSN-C capability (**FA8650-19-2-5220**), consistent with DoD investment in shared experimental infrastructure feeding autonomous/HTE pipelines. (stach2021autonomousexperimentationsystems pages 20-21, ament2021autonomousmaterialssynthesis pages 11-12)
- **ONR is present but less frequent** in this slice, with awards spanning older-start lines (e.g., N00014-13-1-0635; N00014-15-1-2222; N00014-18-1-2879). This pattern could indicate a stable but smaller footprint relative to AFOSR in the specific SDL/autonomy-for-materials papers retrieved here. (stanev2021artificialintelligencefor pages 10-11, kunka2021decodingdefectstatistics pages 8-9)
- **DARPA is visible but sparse** in acknowledgements in this slice (e.g., HR001118C0036 acknowledged in a field-defining community perspective). (stach2021autonomousexperimentationsystems pages 20-21)

**Interpretation caveat:** this is a literature-acknowledgement-derived view; it does not measure total DoD spend or solicitation volume, and “shrinking vs. growing” is inferred only from the limited sample and award-year patterns seen in acknowledgements. (alu2025roadmaponembodying pages 72-74)

### 2) Dominant institutions and PIs (as visible in acknowledgements/author lists)
Repeatedly appearing investigators in DoD-acknowledging papers include **A. Gilad Kusne**, **Ichiro Takeuchi**, **Eric Stach**, and **Benji Maruyama** (autonomous experimentation systems and related community efforts), and **Carla P. Gomes / John M. Gregoire / R. Bruce van Dover** (autonomous synthesis/phase mapping such as SARA). (stach2021autonomousexperimentationsystems pages 20-21, ament2021autonomousmaterialssynthesis pages 11-12, stanev2021artificialintelligencefor pages 10-11)
Autonomous-manufacturing/experimentation methodology appears in DoD acknowledgements through **Mark A. Pitt** and **Jay I. Myung** (AFOSR FA9550-21-1-0176) and materials characterization/ML through **Surya R. Kalidindi** (ONR N00014-18-1-2879). (myung2025multiobjectivebayesianoptimization pages 11-12, kunka2021decodingdefectstatistics pages 8-9)

### 3) New agency programs launched 2022+ funding this topic (evidence in corpus)
The clearest “new” (2022+) signal in the inspected papers is **AFOSR award FA9550-23-1-0466**, acknowledged in a 2025 roadmap paper, indicating continuing AFOSR investment in intelligent materials/structures themes adjacent to autonomy and advanced manufacturing. (alu2025roadmaponembodying pages 72-74)
No explicit 2022+ program names (e.g., named DARPA DSO program titles) were found in the **acknowledgement text** of the inspected papers; the DARPA evidence present is an award/contract number without a named program label. (stach2021autonomousexperimentationsystems pages 20-21)

### 4) Visible gaps / opportunities (where DoD is not visible in this literature slice)
- **Sparse ARO/ARL/NRL visibility:** none of the inspected acknowledgement excerpts explicitly referenced ARO, ARL, or NRL awards, despite the topic’s relevance to defense materials and manufacturing. (ament2021autonomousmaterialssynthesis pages 11-12, stach2021autonomousexperimentationsystems pages 20-21, kunka2021decodingdefectstatistics pages 8-9)
- **DoD-wide mechanisms not visible here:** MURI, DURIP, YIP, NDSEG, and Vannevar Bush awards were not explicitly acknowledged in this retrieved set, suggesting either (i) they are funding adjacent work that did not appear in the specific SDL/autonomy papers retrieved, (ii) they are acknowledged in other papers not captured by this search, or (iii) they are underutilized/underreported for SDL-for-alloys work. (stach2021autonomousexperimentationsystems pages 20-21, alu2025roadmaponembodying pages 72-74)
- **Program labeling gap:** even when DoD funding is present, acknowledgements often list only agency + award number and not a recognizable program name (e.g., “MURI” or a named DARPA program), which makes portfolio mapping from literature alone difficult and argues for triangulation with agency award databases. (stach2021autonomousexperimentationsystems pages 20-21, ament2021autonomousmaterialssynthesis pages 11-12)

## Notes on evidence limitations
This report is based on DoD funding acknowledgements extractable from a limited set of retrieved 2020–2026 publications in the SDL/autonomous experimentation/materials domain. Additional targeted retrieval (e.g., specific DARPA program names like “Make-It,” “AMD,” or “Materials Architectures…Hypersonics,” and explicit alloy-focused autonomous synthesis papers) would likely expand the award list and improve trend resolution. (stach2021autonomousexperimentationsystems pages 20-21, alu2025roadmaponembodying pages 72-74)

References

1. (stanev2021artificialintelligencefor pages 10-11): Valentin Stanev, Kamal Choudhary, Aaron Gilad Kusne, Johnpierre Paglione, and Ichiro Takeuchi. Artificial intelligence for search and discovery of quantum materials. Communications Materials, Oct 2021. URL: https://doi.org/10.1038/s43246-021-00209-z, doi:10.1038/s43246-021-00209-z. This article has 85 citations and is from a peer-reviewed journal.

2. (ament2021autonomousmaterialssynthesis pages 11-12): Sebastian Ament, Maximilian Amsler, Duncan R. Sutherland, Ming-Chiang Chang, Dan Guevarra, Aine B. Connolly, John M. Gregoire, Michael O. Thompson, Carla P. Gomes, and R. Bruce van Dover. Autonomous materials synthesis via hierarchical active learning of nonequilibrium phase diagrams. Science Advances, Dec 2021. URL: https://doi.org/10.1126/sciadv.abg4930, doi:10.1126/sciadv.abg4930. This article has 107 citations and is from a highest quality peer-reviewed journal.

3. (stach2021autonomousexperimentationsystems pages 20-21): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 372 citations and is from a peer-reviewed journal.

4. (alu2025roadmaponembodying pages 72-74): Andrea Alu, Andres F Arrieta, Emanuela Del Dottore, Michael D Dickey, Samuele Ferracin, Ryan L Harne, Helmut Hauser, Qiguang He, Jonathan Brigham Hopkins, Lance Hyatt, Suyi Li, Stefano Mariani, Barbara Mazzolai, Alessio Mondini, Aniket Pal, Daniel J Preston, Anoop Rajappan, Jordan R. Raney, Pedro Reis, Stephen Andrew Sarles, Metin Sitti, Uba K. Ubamanyu, Martin van Hecke, and Kon-Well Wang. Roadmap on embodying mechano-intelligence and computing in functional materials and structures. Smart Materials and Structures, Feb 2025. URL: https://doi.org/10.1088/1361-665x/adb7aa, doi:10.1088/1361-665x/adb7aa. This article has 0 citations and is from a peer-reviewed journal.

5. (myung2025multiobjectivebayesianoptimization pages 11-12): Jay I. Myung, James R. Deneault, Jorge Chang, Inhan Kang, Benji Maruyama, and Mark A. Pitt. Multi-objective bayesian optimization: a case study in material extrusion. Digital Discovery, 4:464-476, Jan 2025. URL: https://doi.org/10.1039/d4dd00281d, doi:10.1039/d4dd00281d. This article has 14 citations and is from a peer-reviewed journal.

6. (kunka2021decodingdefectstatistics pages 8-9): Cody Kunka, Apaar Shanker, Elton Y. Chen, Surya R. Kalidindi, and Rémi Dingreville. Decoding defect statistics from diffractograms via machine learning. npj Computational Materials, 7:1-9, May 2021. URL: https://doi.org/10.1038/s41524-021-00539-z, doi:10.1038/s41524-021-00539-z. This article has 14 citations and is from a peer-reviewed journal.

7. (stanev2021artificialintelligencefor media 076ed439): Valentin Stanev, Kamal Choudhary, Aaron Gilad Kusne, Johnpierre Paglione, and Ichiro Takeuchi. Artificial intelligence for search and discovery of quantum materials. Communications Materials, Oct 2021. URL: https://doi.org/10.1038/s43246-021-00209-z, doi:10.1038/s43246-021-00209-z. This article has 85 citations and is from a peer-reviewed journal.

8. (stanev2021artificialintelligencefor media c61b45de): Valentin Stanev, Kamal Choudhary, Aaron Gilad Kusne, Johnpierre Paglione, and Ichiro Takeuchi. Artificial intelligence for search and discovery of quantum materials. Communications Materials, Oct 2021. URL: https://doi.org/10.1038/s43246-021-00209-z, doi:10.1038/s43246-021-00209-z. This article has 85 citations and is from a peer-reviewed journal.

9. (kunka2021decodingdefectstatistics pages 9-9): Cody Kunka, Apaar Shanker, Elton Y. Chen, Surya R. Kalidindi, and Rémi Dingreville. Decoding defect statistics from diffractograms via machine learning. npj Computational Materials, 7:1-9, May 2021. URL: https://doi.org/10.1038/s41524-021-00539-z, doi:10.1038/s41524-021-00539-z. This article has 14 citations and is from a peer-reviewed journal.

10. (deshmukh2024activelearningof pages 10-11): Gaurav Deshmukh, Noah J. Wichrowski, Nikolaos Evangelou, Pushkar G. Ghanekar, Siddharth Deshpande, Ioannis G. Kevrekidis, and Jeffrey Greeley. Active learning of ternary alloy structures and energies. npj Computational Materials, 10:1-11, May 2024. URL: https://doi.org/10.1038/s41524-024-01256-z, doi:10.1038/s41524-024-01256-z. This article has 19 citations and is from a peer-reviewed journal.
