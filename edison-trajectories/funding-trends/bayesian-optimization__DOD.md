# Funding trends: bayesian optimization — DOD

*Edison `LITERATURE` task `fe76063c-9a5e-46f6-8a95-fdb0ca9b2480` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
Bayesian optimization for alloy/materials design to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: Bayesian optimization, active learning, and multi-objective acquisition functions applied to alloy/materials design and process optimization (including BoTorch, GP surrogates, BO with constraints, network/function-of-network BO)

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


## Executive summary (DoD/DOW posture; 2020–2026 literature sample)
Across recent (2020–2026) Bayesian optimization/active learning literature relevant to autonomous materials/process optimization, DoD funding appears concentrated in (i) DARPA programs explicitly targeting autonomous closed-loop discovery/optimization platforms (notably Make-It and Accelerated Molecular Discovery), and (ii) service/lab basic and applied research lines supporting autonomous materials synthesis/characterization infrastructure and algorithmic work (AFOSR, AFRL, ARL). (nambiar2022bayesianoptimizationof pages 9-10, breen2021readysetflow! pages 11-12, ament2021autonomousmaterialssynthesis pages 11-12, khatamsaz2023aphysicsinformed pages 11-11)
Within alloy/materials design specifically, the clearest “award-number-level” signal in this corpus is ARL cooperative-agreement funding for physics-informed Bayesian optimization applied to NiTi alloy design and associated accelerated materials discovery workflow development. (khatamsaz2023aphysicsinformed pages 11-11, mulukutla2024illustratinganeffective pages 23-26)
AFOSR/AFRL also appear as direct sponsors of autonomous materials synthesis/active learning systems (with explicit award numbers) and as partial supporters of alloy active-learning work (sometimes without award numbers in acknowledgements). (ament2021autonomousmaterialssynthesis pages 11-12, deshmukh2024activelearningof pages 10-11)
In this sampled corpus, explicit ONR, NRL, AFRL (beyond one infrastructure award), DoD-wide fellowships (NDSEG), and flagship faculty programs (Vannevar Bush, YIP) are not prominently visible in acknowledgements for Bayesian optimization applied to alloy design, suggesting either under-representation in the sampled literature or a potential funding/reporting gap for this niche. (ament2021autonomousmaterialssynthesis pages 11-12, deshmukh2024activelearningof pages 10-11, khatamsaz2023aphysicsinformed pages 11-11)

## DoD-funded projects acknowledged in recent papers (2020–2026)
| DoD agency | Program / subprogram name | Award / contract number(s) | PI(s) and institution | Award amount | Start year / period of performance | Short project description | Citation IDs of acknowledging papers |
|---|---|---|---|---|---|---|---|
| AFOSR | LRIR | 19RXCOR322 | not stated in acknowledgements; inferred from corresponding author list: Chiwoo Park, University of Pennsylvania | not stated | not stated | Supported autonomous experimentation for materials development/community infrastructure discussed in *Matter*; the paper frames Bayesian optimization and active learning as core methods in autonomous materials R&D. (stach2021autonomousexperimentationsystems pages 20-21) | (stach2021autonomousexperimentationsystems pages 20-21) |
| AFOSR | AFOSR grant | FA9550-18-1-0144 | not stated in acknowledgements; acknowledged specifically for “C.P.” and inferred from author list as Chiwoo Park, University of Pennsylvania | not stated | not stated | Supports autonomous experimentation and materials development work in which Bayesian optimization and active learning are presented as enabling methods for self-driving materials research. (stach2021autonomousexperimentationsystems pages 20-21) | (stach2021autonomousexperimentationsystems pages 20-21) |
| DARPA | not stated; DARPA contract acknowledged in autonomous experimentation community paper | HR001118C0036 | Joshua Schrier, Fordham University (initials “J.S.” in acknowledgements; inferred from author list) | not stated | not stated | DARPA-supported work connected to autonomous experimentation for materials development, including community-building and software/algorithm ecosystems relevant to Bayesian optimization-guided materials campaigns. (stach2021autonomousexperimentationsystems pages 20-21) | (stach2021autonomousexperimentationsystems pages 20-21) |
| DARPA / ARO | DARPA Make-It | ARO W911NF-16-2-0023 | Klavs F. Jensen, MIT; Timothy F. Jamison, MIT; not stated in acknowledgements, inferred from author list and ASKCOS report | not stated | Agreement / contract active by 2016; exact period not stated in paper excerpts | Funded robotic flow synthesis and multistep process optimization using Bayesian optimization in a closed-loop automated platform; directly relevant to autonomous experimentation and multi-objective BO. (nambiar2022bayesianoptimizationof pages 9-10, breen2021readysetflow! pages 11-12, jensen2021automatedsystemfor pages 1-3) | (nambiar2022bayesianoptimizationof pages 9-10, breen2021readysetflow! pages 11-12, jensen2021automatedsystemfor pages 1-3) |
| DARPA | Accelerated Molecular Discovery | HR00111920025 | Klavs F. Jensen, MIT; Timothy F. Jamison, MIT; not stated in acknowledgements, inferred from author list | not stated | not stated | Supported Bayesian optimization of computer-proposed multistep synthetic routes on an automated robotic flow platform, extending closed-loop optimization beyond route planning into execution. (nambiar2022bayesianoptimizationof pages 9-10) | (nambiar2022bayesianoptimizationof pages 9-10) |
| ARL | Cooperative Agreement | W911NF-22-2-0106 | Raymundo Arróyave, Texas A&M University; Danial Khatamsaz also explicitly acknowledges related work in the paper; PI not stated in acknowledgements, inferred from author list | not stated | not stated | Sponsored physics-informed Bayesian optimization for NiTi shape-memory alloy design and, in related center work, broader accelerated materials discovery workflows using batch BO and active learning for alloy development. (khatamsaz2023aphysicsinformed pages 11-11, mulukutla2024illustratinganeffective pages 23-26) | (khatamsaz2023aphysicsinformed pages 11-11, mulukutla2024illustratinganeffective pages 23-26) |
| AFOSR | AFOSR award | FA9550-18-1-0136 | Carla P. Gomes, Cornell University; Michael O. Thompson / R. Bruce van Dover team at Cornell also associated via author list; PI not explicitly stated in acknowledgements | not stated | not stated | Supported SARA, a hierarchical active-learning platform for autonomous materials synthesis and nonequilibrium phase-diagram mapping; closely aligned with closed-loop materials discovery. (ament2021autonomousmaterialssynthesis pages 11-12) | (ament2021autonomousmaterialssynthesis pages 11-12) |
| AFRL | Materials Solutions Network at CHESS (MSN-C) support | FA8650-19-2-5220 | not stated in acknowledgements; inferred from author list as Cornell experimental team associated with CHESS, including Michael O. Thompson and R. Bruce van Dover | not stated | not stated | AFRL support for the experimental infrastructure enabling autonomous materials synthesis and hierarchical active learning in the SARA platform. (ament2021autonomousmaterialssynthesis pages 11-12) | (ament2021autonomousmaterialssynthesis pages 11-12) |
| AFOSR | US AFOSR support (program not specified) | not stated | Ioannis G. Kevrekidis, Johns Hopkins University / University of Patras; Nikolaos Evangelou and Noah J. Wichrowski, inferred from author list as “IGK, NE and NW” | not stated | not stated | Partial AFOSR support for active learning of ternary alloy structures and energies, using uncertainty-aware surrogate modeling to identify stable high-entropy alloy compositions with reduced DFT budgets. (deshmukh2024activelearningof pages 10-11) | (deshmukh2024activelearningof pages 10-11) |


*Table: This table consolidates distinct DoD-funded projects identified from acknowledgements in recent 2020–2026 literature on Bayesian optimization, active learning, and autonomous materials/process discovery. It is useful as a project-level funding map linking agencies, award numbers, inferred PIs/institutions, and the papers that acknowledge each award.*

## Trends (from extracted acknowledgements; qualitative, corpus-limited)

### 1) Sub-programs growing vs. shrinking (signals in this corpus)
- **Strong signal: DARPA Make-It → autonomous, closed-loop experimental optimization platforms**. Multiple papers in this corpus acknowledge DARPA Make-It under contract **ARO W911NF-16-2-0023**, indicating recurring support for automated experimentation with Bayesian optimization and multi-objective optimization (process optimization, route execution). (breen2021readysetflow! pages 11-12, nambiar2022bayesianoptimizationof pages 9-10, jensen2021automatedsystemfor pages 1-3)
- **Adjacency/growth signal: DARPA “Accelerated Molecular Discovery”** appears alongside Make-It in BO-driven automation, with explicit award **HR00111920025** in a 2022 paper, suggesting DARPA continued/expanded investment beyond Make-It into broader acceleration of discovery workflows. (nambiar2022bayesianoptimizationof pages 9-10)
- **AFOSR/AFRL infrastructure + internal research support**: AFOSR appears both as external research sponsor (e.g., **FA9550-18-1-0136**) and as internal-research-line support (AFOSR LRIR **19RXCOR322**) in autonomous experimentation contexts; AFRL appears funding beamline/network infrastructure (**FA8650-19-2-5220**) supporting autonomous synthesis/active learning. (ament2021autonomousmaterialssynthesis pages 11-12, stach2021autonomousexperimentationsystems pages 20-21)
- **ARL cooperative agreements for alloy-centric BO**: ARL sponsorship under **W911NF-22-2-0106** directly supports physics-informed Bayesian optimization for NiTi shape-memory alloy design and broader accelerated materials discovery workflows that employ BO/active learning. (khatamsaz2023aphysicsinformed pages 11-11, mulukutla2024illustratinganeffective pages 23-26)

*Note*: “Shrinking” cannot be robustly concluded from acknowledgements alone; absence in this corpus is not proof of declining funding.

### 2) Institutions and PIs dominating (in this corpus)
- **MIT (Jensen/Jamison group)** is repeatedly associated (via authorship on acknowledging papers and an associated report) with the DARPA Make-It contract **ARO W911NF-16-2-0023**, and with DARPA Accelerated Molecular Discovery **HR00111920025**, in Bayesian optimization-driven robotic flow chemistry/closed-loop process optimization. (breen2021readysetflow! pages 11-12, nambiar2022bayesianoptimizationof pages 9-10, jensen2021automatedsystemfor pages 1-3)
- **Texas A&M (Arróyave group and collaborators)** is repeatedly associated (via authorship on acknowledging papers) with ARL cooperative agreement **W911NF-22-2-0106** supporting Bayesian optimization methods for alloy design and accelerated discovery workflows. (khatamsaz2023aphysicsinformed pages 11-11, mulukutla2024illustratinganeffective pages 23-26)
- **Cornell (Gomes and collaborators)** is associated with AFOSR award **FA9550-18-1-0136** and an AFRL infrastructure award **FA8650-19-2-5220** supporting an autonomous synthesis/active-learning platform. (ament2021autonomousmaterialssynthesis pages 11-12)
- **University of Pennsylvania / community efforts (Park; Schrier)** appear in autonomous experimentation community-building papers acknowledging AFOSR LRIR **19RXCOR322**, AFOSR **FA9550-18-1-0144** (for “C.P.”), and a DARPA contract **HR001118C0036** (for “J.S.”). (stach2021autonomousexperimentationsystems pages 20-21)

### 3) New programs (launched 2022+) visibly funding this topic
- The clearest “newer” award-number signal in this corpus is the **ARL Cooperative Agreement W911NF-22-2-0106** (award number suggests a 2022 start) supporting Bayesian optimization applied to alloy design and associated accelerated discovery infrastructure. (khatamsaz2023aphysicsinformed pages 11-11, mulukutla2024illustratinganeffective pages 23-26)

### 4) Visible gaps / opportunities (from this corpus)
- **Sparse explicit ONR/NRL/AFRL/ARL-direct lab program labeling**: beyond AFRL’s infrastructure award and ARL’s cooperative agreement, the sampled acknowledgements contain limited ONR/NRL visibility for Bayesian optimization applied to alloy design; this may indicate an opportunity for clearer programmatic alignment and solicitations that explicitly call out Bayesian optimization/active learning for alloys and constrained/multi-objective decision-making in closed-loop labs. (ament2021autonomousmaterialssynthesis pages 11-12, khatamsaz2023aphysicsinformed pages 11-11)
- **DoD-wide talent programs (NDSEG, Vannevar Bush, YIP, MURI, DURIP)** do not appear explicitly in the acknowledgements captured here for the alloy/materials BO niche; if these mechanisms are underutilized for autonomous alloy discovery, they represent potential levers for PI recruitment and platform-building (especially multi-institution testbeds and shared experimental infrastructure). (khatamsaz2023aphysicsinformed pages 11-11, ament2021autonomousmaterialssynthesis pages 11-12)

### Evidence limitations
This synthesis is limited to the set of retrieved 2020–2026 papers whose full text was accessible in-tool and where DoD awards were explicitly acknowledged; additional relevant DoD-funded work likely exists but was not captured in the current corpus. (deshmukh2024activelearningof pages 10-11, ament2021autonomousmaterialssynthesis pages 11-12, nambiar2022bayesianoptimizationof pages 9-10)

References

1. (nambiar2022bayesianoptimizationof pages 9-10): Anirudh M. K. Nambiar, Christopher P. Breen, Travis Hart, Timothy Kulesza, Timothy F. Jamison, and Klavs F. Jensen. Bayesian optimization of computer-proposed multistep synthetic routes on an automated robotic flow platform. ACS Central Science, 8:825-836, Jun 2022. URL: https://doi.org/10.1021/acscentsci.2c00207, doi:10.1021/acscentsci.2c00207. This article has 169 citations and is from a highest quality peer-reviewed journal.

2. (breen2021readysetflow! pages 11-12): Christopher P. Breen, Anirudh M.K. Nambiar, Timothy F. Jamison, and Klavs F. Jensen. Ready, set, flow! automated continuous synthesis and optimization. Trends in Chemistry, 3:373-386, May 2021. URL: https://doi.org/10.1016/j.trechm.2021.02.005, doi:10.1016/j.trechm.2021.02.005. This article has 131 citations and is from a peer-reviewed journal.

3. (ament2021autonomousmaterialssynthesis pages 11-12): Sebastian Ament, Maximilian Amsler, Duncan R. Sutherland, Ming-Chiang Chang, Dan Guevarra, Aine B. Connolly, John M. Gregoire, Michael O. Thompson, Carla P. Gomes, and R. Bruce van Dover. Autonomous materials synthesis via hierarchical active learning of nonequilibrium phase diagrams. Science Advances, Dec 2021. URL: https://doi.org/10.1126/sciadv.abg4930, doi:10.1126/sciadv.abg4930. This article has 107 citations and is from a highest quality peer-reviewed journal.

4. (khatamsaz2023aphysicsinformed pages 11-11): Danial Khatamsaz, Raymond Neuberger, Arunabha M. Roy, Sina Hossein Zadeh, Richard Otis, and Raymundo Arróyave. A physics informed bayesian optimization approach for material design: application to niti shape memory alloys. npj Computational Materials, 9:1-11, Dec 2023. URL: https://doi.org/10.1038/s41524-023-01173-7, doi:10.1038/s41524-023-01173-7. This article has 64 citations and is from a peer-reviewed journal.

5. (mulukutla2024illustratinganeffective pages 23-26): Mrinalini Mulukutla, A. Nicole Person, Sven Voigt, Lindsey Kuettner, Branden Kappes, Danial Khatamsaz, Robert Robinson, Daniel Salas Mula, Wenle Xu, Daniel Lewis, Hongkyu Eoh, Kailu Xiao, Haoren Wang, Jaskaran Singh Saini, Raj Mahat, Trevor Hastings, Matthew Skokan, Vahid Attari, Michael Elverud, James D. Paramore, Brady Butler, Kenneth Vecchio, Surya R. Kalidindi, Douglas Allaire, Ibrahim Karaman, Edwin L. Thomas, George Pharr, Ankit Srivastava, and Raymundo Arróyave. Illustrating an effective workflow for accelerated materials discovery. Integrating Materials and Manufacturing Innovation, 13:453-473, Jun 2024. URL: https://doi.org/10.1007/s40192-024-00357-3, doi:10.1007/s40192-024-00357-3. This article has 18 citations and is from a peer-reviewed journal.

6. (deshmukh2024activelearningof pages 10-11): Gaurav Deshmukh, Noah J. Wichrowski, Nikolaos Evangelou, Pushkar G. Ghanekar, Siddharth Deshpande, Ioannis G. Kevrekidis, and Jeffrey Greeley. Active learning of ternary alloy structures and energies. npj Computational Materials, 10:1-11, May 2024. URL: https://doi.org/10.1038/s41524-024-01256-z, doi:10.1038/s41524-024-01256-z. This article has 19 citations and is from a peer-reviewed journal.

7. (stach2021autonomousexperimentationsystems pages 20-21): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 372 citations and is from a peer-reviewed journal.

8. (jensen2021automatedsystemfor pages 1-3): KF Jensen. Automated system for knowledge-based continuous organic synthesis (askcos). Unknown journal, 2021.
