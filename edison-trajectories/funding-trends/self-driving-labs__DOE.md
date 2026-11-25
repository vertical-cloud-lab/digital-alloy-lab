# Funding trends: self driving labs — DOE

*Edison `LITERATURE` task `6ce7289b-27bb-43e3-a42f-c08da45ecb34` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
self-driving laboratories for materials/alloys to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: self-driving laboratories and autonomous experimentation for materials and metallic alloy discovery (closed-loop AI/robot-controlled synthesis-characterization-design loops, autonomous formulation, autonomous additive manufacturing)

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


## Executive summary (DOE funding posture, 2020–2026)
DOE support for self-driving laboratories (SDLs) and autonomous experimentation in materials/alloys (as evidenced in 2020–2026 paper acknowledgements) is dominated by (i) ARPA‑E project awards that explicitly underwrite autonomous/closed-loop alloy design methods and (ii) Office of Science mechanisms—especially Basic Energy Sciences (BES) awards, Energy Frontier Research Centers (EFRCs), and ubiquitous user-facility access statements at DOE light sources and nanoscience centers. (kavalsky2023byhowmuch pages 23-27, stach2021autonomousexperimentationsystems pages 20-21, kalinin2024designingworkflowsfor pages 28-31, katz2026jewelerinthelooppersonalizedalloy pages 7-9, maguire2025goodenoughis pages 10-11)
Within ARPA‑E, ULTIMATE appears repeatedly across multiple alloy-design/autonomy papers (DE‑AR0001427), and a newer ARPA‑E program (CHADWICK) appears in 2026 alloy optimization work (DE‑AR0001988), indicating continued ARPA‑E interest in AI-enabled alloy development workflows. (khatamsaz2023aphysicsinformed pages 11-11, katz2026jewelerinthelooppersonalizedalloy pages 7-9, maguire2025goodenoughis pages 10-11)
BES support appears both as direct awards to academic PIs and as center-scale support (EFRCs) tied to autonomous characterization/workflow efforts, alongside national-lab enabling contracts and LDRD that directly fund “robotic beamline scientist” concepts. (stach2021autonomousexperimentationsystems pages 20-21, kalinin2024designingworkflowsfor pages 28-31, maffettone2023whatismissing pages 11-11, kalinin2024designingworkflowsfor pages 1-6)
In this literature-derived sample, explicit acknowledgements of DOE EERE/AMMTO, NETL/FECM, and manufacturing-focused DOE programs are sparse or absent in the autonomous alloy discovery papers with retrievable full text, suggesting either underrepresentation in publications or a gap/opportunity for more visible programmatic investment (or publication practices) in closed-loop metallic alloy SDLs. (kavalsky2023byhowmuch pages 23-27, maguire2025goodenoughis pages 10-11, kalinin2024designingworkflowsfor pages 28-31)

## DOE-funded projects identified in 2020–2026 literature (acknowledgements/funding extraction)
| PI(s) & institution | DOE program/sub-program | Award/contract/project number | Award amount | Project title / short description | Period of performance / start year | Paper citation key(s) where acknowledged |
|---|---|---|---|---|---|---|
| Venkatasubramanian Viswanathan and coauthors, Carnegie Mellon University / Citrine Informatics / collaborators (inferable from author list) | DOE ARPA-E | DE-AR0001211 | not stated | Closed-loop computational materials discovery benchmarking for autonomous search workflows, including single-atom alloy discovery and broader automated materials design loops. The paper evaluates how much autonomous computational frameworks can accelerate discovery. (kavalsky2023byhowmuch pages 23-27) | not stated | `kavalsky2023byhowmuch` |
| Raymundo Arróyave, Brent Vela, Danial Khatamsaz and collaborators, Texas A&M University / Ames National Laboratory collaborators (inferable from author lists) | DOE ARPA-E ULTIMATE | DE-AR0001427 | not stated | Autonomous/Bayesian alloy design for constrained multi-objective optimization, including Mo-Nb-Ti-V-W alloy design and NiTi shape-memory-alloy optimization. Multiple papers position this support as enabling autonomous or closed-loop alloy discovery methods. (khatamsaz2023aphysicsinformed pages 11-11, khatamsaz2023bayesianoptimizationwith pages 14-14, maguire2025goodenoughis pages 10-11) | not stated | `khatamsaz2023aphysicsinformed`; `khatamsaz2023bayesianoptimizationwith`; `maguire2025goodenoughis` |
| Raymundo Arróyave, Brent Vela and collaborators, Texas A&M University (inferable from author list) | DOE ARPA-E CHADWICK | DE-AR0001988 | not stated | Preference-based Bayesian optimization for personalized alloy color optimization (“jeweler-in-the-loop”). The work extends autonomous alloy design ideas into human-in-the-loop multi-objective alloy selection. (katz2026jewelerinthelooppersonalizedalloy pages 7-9) | not stated | `katz2026jewelerinthelooppersonalizedalloy` |
| John M. Gregoire (Caltech) and Carla P. Gomes (Cornell), explicitly tied in acknowledgements as J.M.G. and C.P.G. | DOE Office of Science, Basic Energy Sciences | DE-SC0020383 | not stated | Community perspective on autonomous experimentation systems for materials development, covering closed-loop experimentation and AI-enabled materials workflows. The award is explicitly acknowledged as support for J.M.G. and C.P.G. (stach2021autonomousexperimentationsystems pages 20-21) | not stated | `stach2021autonomousexperimentationsystems` |
| Sergei V. Kalinin / Oak Ridge National Laboratory and collaborators; center for 3D Ferroelectric Microelectronics | DOE Office of Science, Basic Energy Sciences, EFRC (3DFeM) | DE-SC0021118 | not stated | Workflow design for materials characterization in autonomous and distributed materials science. The acknowledged center, 3DFeM, is identified as an Energy Frontier Research Center supporting the work. (kalinin2024designingworkflowsfor pages 28-31) | not stated | `kalinin2024designingworkflowsfor` |
| not stated; Advanced Light Source user facility, Lawrence Berkeley National Laboratory | DOE Office of Science User Facility contract | DE-AC02-05CH11231 | not stated | Use of Advanced Light Source resources in the autonomous experimentation community-perspective paper. The contract number is tied to the DOE Office of Science user facility rather than a standalone research grant. (stach2021autonomousexperimentationsystems pages 20-21) | not stated | `stach2021autonomousexperimentationsystems` |
| P. M. Maffettone / Brookhaven National Laboratory user of NSLS-II resources | DOE Office of Science user-facility operating contract (NSLS-II at Brookhaven) | DE-SC0012704 | not stated | Use of National Synchrotron Light Source II resources in work on open challenges for autonomous discovery. The acknowledgement ties the work to Brookhaven’s DOE user-facility operations contract. (maffettone2023whatismissing pages 11-11) | not stated | `maffettone2023whatismissing` |
| P. M. Maffettone / Brookhaven National Laboratory | Brookhaven National Laboratory LDRD | 23-039 | not stated | “Extensible robotic beamline scientist for self-driving total scattering studies.” This LDRD project directly aligns with autonomous experimentation infrastructure for materials characterization. (maffettone2023whatismissing pages 11-11) | 2023 (inferable from project number) | `maffettone2023whatismissing` |
| UT-Battelle, LLC / Oak Ridge National Laboratory | DOE national-lab operating contract | DE-AC0500OR22725 | not stated | Materials characterization workflow paper authored under the UT-Battelle management-and-operations contract for ORNL. This is a lab operating contract acknowledgement rather than a competed project award. (kalinin2024designingworkflowsfor pages 1-6) | not stated | `kalinin2024designingworkflowsfor` |
| Ames National Laboratory / Iowa State University | DOE national-lab operating contract | DE-AC02-07CH11358 | not stated | Ames operating contract acknowledged in alloy-design work that also cites BES support for theory development at Ames. The associated papers focus on Bayesian and autonomous alloy design under uncertainty. (khatamsaz2023bayesianoptimizationwith pages 14-14) | not stated | `khatamsaz2023bayesianoptimizationwith` |
| not stated; follow-on funding listed in ARPA-E final report | DOE Office of Science, Basic Energy Sciences (follow-on) | not stated | $400k | Follow-on BES funding reported in the ARPA-E final report for “Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments.” The report does not provide a BES award number in the table excerpt. (zhang2025finalarpaereport pages 19-20, zhang2025finalarpaereport media a9a7cf99) | not stated | `zhang2025finalarpaereport` |
| not stated; follow-on funding listed in ARPA-E final report | DOE Nuclear Energy (follow-on) | not stated | $675k | Follow-on DOE-NE funding reported in the same ARPA-E final report, described as “DOE-NE INM rod-to-tube.” No award number is given in the available table/image excerpt. (zhang2025finalarpaereport pages 19-20, zhang2025finalarpaereport media a9a7cf99) | not stated | `zhang2025finalarpaereport` |


*Table: This table compiles distinct DOE-related awards, contracts, and lab/internal project identifiers acknowledged in the retrieved 2020–2026 literature on self-driving laboratories and autonomous materials/alloy discovery. It is useful as a grant-level evidence base for identifying active DOE sub-programs, institutions, and recurrent award numbers in the field.*

## Trends (DOE sub-programs, PIs/institutions, new programs, gaps)

### 1) Sub-program signals (within DOE) visible in paper acknowledgements
- **ARPA‑E is a recurring direct sponsor** of autonomous/closed-loop alloy design methods via project awards, with repeated appearance of **ULTIMATE (DE‑AR0001427)** and at least one other ARPA‑E award (DE‑AR0001211) supporting closed-loop computational materials discovery benchmarking. (maguire2025goodenoughis pages 10-11, kavalsky2023byhowmuch pages 23-27, khatamsaz2023aphysicsinformed pages 11-11)
- **Newer ARPA‑E program signal (2022+): CHADWICK** appears explicitly in a 2026 Digital Discovery paper (DE‑AR0001988), indicating ARPA‑E diversification into additional alloy-related thrusts beyond ULTIMATE in the 2022+ timeframe. (katz2026jewelerinthelooppersonalizedalloy pages 7-9)
- **BES appears persistently through multiple channels:** direct BES research awards to academic PIs (e.g., DE‑SC0020383), EFRC support (DE‑SC0021118), and user-facility contracts for synchrotron resources (ALS, NSLS‑II) and nanoscience centers (CNMS). (stach2021autonomousexperimentationsystems pages 20-21, kalinin2024designingworkflowsfor pages 28-31, maffettone2023whatismissing pages 11-11)
- **ASCR+BES center-scale enabling investment** is exemplified by CAMERA, described as jointly funded by ASCR and BES and explicitly oriented toward autonomous control of experiments and real-time feedback at DOE light sources, suggesting an Office-of-Science pathway for SDL-enabling infrastructure beyond single-PI awards. (noack2021autonomousdiscoveryin pages 1-9)

**Caveat on “growing vs shrinking”:** acknowledgements alone do not provide year-by-year budget trajectories; therefore, growth/decline is assessed here only as *presence/recurrence* of sub-program signals in 2020–2026 publications, not as a quantitative funding trendline.

### 2) Dominant institutions and PIs (from acknowledgements that explicitly tie awards to people)
- The **Arróyave/Vela-led alloy autonomy portfolio** (Texas A&M; collaborators) appears repeatedly with ARPA‑E ULTIMATE support (DE‑AR0001427) across multiple papers on Bayesian/physics-informed optimization for alloys, suggesting concentrated ARPA‑E investment in this PI/institution cluster for autonomous alloy design. (khatamsaz2023aphysicsinformed pages 11-11, maguire2025goodenoughis pages 10-11)
- **Gregoire (Caltech) and Gomes (Cornell)** are explicitly linked to BES award **DE‑SC0020383** in the widely cited community perspective on autonomous experimentation systems, indicating BES support for the AI/automation ecosystem around autonomous experimentation. (stach2021autonomousexperimentationsystems pages 20-21)
- **DOE national labs are central enablers** through user facilities (ALS, NSLS‑II, CNMS) and lab mechanisms (M&O contracts; LDRD). The BNL LDRD project explicitly targets an “extensible robotic beamline scientist” for self-driving scattering studies, directly aligned with SDL concepts. (maffettone2023whatismissing pages 11-11, kalinin2024designingworkflowsfor pages 28-31, kalinin2024designingworkflowsfor pages 1-6)

### 3) New (2022+) programs funding this topic (as visible in acknowledgements)
- **ARPA‑E CHADWICK (DE‑AR0001988)** is explicitly acknowledged in 2026 work on preference-based Bayesian optimization for alloy selection, representing a post-2022 program signal in this alloy autonomy literature sample. (katz2026jewelerinthelooppersonalizedalloy pages 7-9)
- The Office of Science center framing for autonomous experiments (CAMERA) emphasizes cross-facility partnerships and autonomous control/feedback workflows; while the excerpt does not list a start year or award number, it signals sustained, multi-year center-scale support for autonomy at DOE user facilities. (noack2021autonomousdiscoveryin pages 1-9)

### 4) Visible gaps / opportunities for DOE (relative to the user’s scope)
- **EERE/AMMTO and DOE manufacturing programs:** despite relevance to autonomous additive manufacturing and closed-loop process control, this corpus did not yield explicit EERE/AMMTO award numbers acknowledged in the retrievable SDL/alloy autonomy papers. This may indicate an opportunity for AMMTO/EERE to seed more *publication-visible* closed-loop alloy SDL efforts, or for investigators to more consistently cite these awards in papers. (maguire2025goodenoughis pages 10-11, kavalsky2023byhowmuch pages 23-27)
- **NETL/FECM:** similarly, no NETL/FECM award numbers were extracted from this topic-focused paper set, suggesting potential whitespace for autonomy/SDL approaches in alloys relevant to energy infrastructure and fossil-energy/industrial decarbonization materials. (kavalsky2023byhowmuch pages 23-27, kalinin2024designingworkflowsfor pages 28-31)
- **Award-number transparency for follow-on DOE funds:** the ARPA‑E final report includes follow-on DOE funding amounts (BES, DOE‑NE) but not award identifiers in the accessible table, limiting traceability; improving linkage from follow-on program names to specific award numbers would benefit portfolio mapping. (zhang2025finalarpaereport media a9a7cf99)


References

1. (kavalsky2023byhowmuch pages 23-27): Lance Kavalsky, Vinay I. Hegde, Eric Muckley, Matthew S. Johnson, Bryce Meredig, and Venkatasubramanian Viswanathan. By how much can closed-loop frameworks accelerate computational materials discovery? Digital Discovery, 2:1112-1125, Jan 2023. URL: https://doi.org/10.1039/d2dd00133k, doi:10.1039/d2dd00133k. This article has 25 citations and is from a peer-reviewed journal.

2. (stach2021autonomousexperimentationsystems pages 20-21): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 372 citations and is from a peer-reviewed journal.

3. (kalinin2024designingworkflowsfor pages 28-31): Sergei V. Kalinin, Maxim Ziatdinov, Mahshid Ahmadi, Ayana Ghosh, Kevin Roccapriore, Yongtao Liu, and Rama K. Vasudevan. Designing workflows for materials characterization. Applied Physics Reviews, Mar 2024. URL: https://doi.org/10.1063/5.0169961, doi:10.1063/5.0169961. This article has 24 citations and is from a domain leading peer-reviewed journal.

4. (katz2026jewelerinthelooppersonalizedalloy pages 7-9): Chase Katz, Ting-Yu Yang, Parker King, Md Shafiqul Islam, Brent Vela, and Raymundo Arróyave. Jeweler-in-the-loop: personalized alloy color optimization <i>via</i> preference-based bo. Digital Discovery, 5:1700-1708, Jan 2026. URL: https://doi.org/10.1039/d6dd00009f, doi:10.1039/d6dd00009f. This article has 0 citations and is from a peer-reviewed journal.

5. (maguire2025goodenoughis pages 10-11): C. Maguire, Christofer Hardcastle, Trevor Hastings, Raymundo Arr'oyave, and Brent Vela. Good enough is better: feasibility vs. pareto-optimality in alloy design. ArXiv, Oct 2025. URL: https://doi.org/10.48550/arxiv.2510.20125, doi:10.48550/arxiv.2510.20125. This article has 1 citations.

6. (khatamsaz2023aphysicsinformed pages 11-11): Danial Khatamsaz, Raymond Neuberger, Arunabha M. Roy, Sina Hossein Zadeh, Richard Otis, and Raymundo Arróyave. A physics informed bayesian optimization approach for material design: application to niti shape memory alloys. npj Computational Materials, 9:1-11, Dec 2023. URL: https://doi.org/10.1038/s41524-023-01173-7, doi:10.1038/s41524-023-01173-7. This article has 64 citations and is from a peer-reviewed journal.

7. (maffettone2023whatismissing pages 11-11): Phillip M. Maffettone, Pascal Friederich, Sterling G. Baird, Ben Blaiszik, Keith A. Brown, Stuart I. Campbell, Orion A. Cohen, Rebecca L. Davis, Ian T. Foster, Navid Haghmoradi, Mark Hereld, Howie Joress, Nicole Jung, Ha-Kyung Kwon, Gabriella Pizzuto, Jacob Rintamaki, Casper Steinmann, Luca Torresi, and Shijing Sun. What is missing in autonomous discovery: open challenges for the community. Digital Discovery, 2:1644-1659, Apr 2023. URL: https://doi.org/10.48550/arxiv.2304.11120, doi:10.48550/arxiv.2304.11120. This article has 50 citations and is from a peer-reviewed journal.

8. (kalinin2024designingworkflowsfor pages 1-6): Sergei V. Kalinin, Maxim Ziatdinov, Mahshid Ahmadi, Ayana Ghosh, Kevin Roccapriore, Yongtao Liu, and Rama K. Vasudevan. Designing workflows for materials characterization. Applied Physics Reviews, Mar 2024. URL: https://doi.org/10.1063/5.0169961, doi:10.1063/5.0169961. This article has 24 citations and is from a domain leading peer-reviewed journal.

9. (khatamsaz2023bayesianoptimizationwith pages 14-14): Danial Khatamsaz, Brent Vela, Prashant Singh, Duane D. Johnson, Douglas Allaire, and Raymundo Arróyave. Bayesian optimization with active learning of design constraints using an entropy-based approach. npj Computational Materials, 9:1-14, Apr 2023. URL: https://doi.org/10.1038/s41524-023-01006-7, doi:10.1038/s41524-023-01006-7. This article has 107 citations and is from a peer-reviewed journal.

10. (zhang2025finalarpaereport pages 19-20): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

11. (zhang2025finalarpaereport media a9a7cf99): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

12. (noack2021autonomousdiscoveryin pages 1-9): Marcus Noack and James Sethian. Autonomous discovery in science and engineering. ArXiv, Aug 2021. URL: https://doi.org/10.2172/1818491, doi:10.2172/1818491. This article has 5 citations.
