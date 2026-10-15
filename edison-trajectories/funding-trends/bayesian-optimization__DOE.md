# Funding trends: bayesian optimization — DOE

*Edison `LITERATURE` task `cd4555f4-bc5a-4d51-a707-1cb0765564f2` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
Bayesian optimization for alloy/materials design to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: Bayesian optimization, active learning, and multi-objective acquisition functions applied to alloy/materials design and process optimization (including BoTorch, GP surrogates, BO with constraints, network/function-of-network BO)

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


## Executive summary (DOE posture, 2020–2026)
Recent literature (2020–2026) explicitly ties Bayesian optimization (BO)/active learning for alloy design to a small set of DOE funding mechanisms, with ARPA‑E programs appearing most repeatedly in alloy-focused BO papers. In particular, ARPA‑E ULTIMATE (DE‑AR0001427) shows up across multiple alloy BO publications and a final technical report, indicating sustained project-level support for autonomous/closed-loop alloy optimization methods. DOE Office of Science/BES support is present but more episodic in this dataset (e.g., BES Data Science Initiative DE‑SC0020381 and lab/user-facility contracts), while EERE/AMO and NETL appear in at least one CALPHAD+BO alloy/coatings paper (DE‑EE0010214 plus NETL site support). Within the papers examined here, explicit LDRD award identifiers are uncommon; national-lab participation is visible mainly through management & operations contracts and user-facility acknowledgements rather than LDRD numbers. (deshmukh2024activelearningof pages 10-11, khatamsaz2023bayesianoptimizationwith pages 14-14, khatamsaz2023aphysicsinformed pages 11-11, alvi2026deepgaussianprocessbased pages 16-17, sundar2025calphadbasedbayesianoptimization pages 9-9, arroyave2024ultimatebirdshot.final pages 1-5)

## DOE-funded projects acknowledged in recent BO-for-materials/alloys papers
| PI(s) & institution | DOE program/sub-program | Award/contract number(s) | Amount (if stated) | Project title/short description | Start/period (if stated) | Paper(s) acknowledging |
|---|---|---|---|---|---|---|
| Raymundo Arróyave (Texas A&M University); coauthors Danial Khatamsaz, Brent Vela, Douglas Allaire, Prashant Singh, Duane D. Johnson on acknowledging papers | DOE ARPA-E ULTIMATE | DE-AR0001427 | not stated | Supports constrained and multi-objective Bayesian optimization for alloy design, including refractory multi-principal-element alloys and physics-informed BO for NiTi/process design; also appears in the ULTIMATE BIRDSHOT final report. (khatamsaz2023bayesianoptimizationwith pages 14-14, khatamsaz2023aphysicsinformed pages 11-11, arroyave2024ultimatebirdshot.final pages 1-5) | not stated | khatamsaz2023-npjCM; khatamsaz2023-npjCM-NiTi; khatamsaz2023-AIAA; maguire2025-arXiv; arroyave2024-OSTI (khatamsaz2023bayesianoptimizationwith pages 14-14, khatamsaz2023aphysicsinformed pages 11-11, arroyave2024ultimatebirdshot.final pages 1-5, khatamsaz2023multiobjectivebayesianoptimization pages 10-11) |
| Raymundo Arróyave / Brent Vela / Douglas Allaire collaboration; acknowledging paper includes Sk Md Ahnaf Akif Alvi, V. Attari, Jan Janssen, Danny Perez, Texas A&M + LANL-affiliated team | DOE ARPA-E CHADWICK | DE-AR0001988 | not stated | Funds deep Gaussian process-based, cost-aware batch Bayesian optimization for complex materials design campaigns, demonstrated on refractory/high-entropy alloy design under realistic experimental-cost constraints. (alvi2026deepgaussianprocessbased pages 16-17) | not stated | alvi2026-npjCM (alvi2026deepgaussianprocessbased pages 16-17) |
| Jeffrey Greeley and coauthors (Northwestern University; institution inferred from paper authors, not stated in acknowledgement) | DOE Office of Science, Office of Basic Energy Sciences, Data Science Initiative | DE-SC0020381 | not stated | Supports active learning of ternary alloy structures and energies using ML surrogates to accelerate discovery of stable high-entropy alloy compositions/structures. (deshmukh2024activelearningof pages 10-11) | not stated | deshmukh2024-npjCM (deshmukh2024activelearningof pages 10-11) |
| Michael C. Gao and coauthors (institution not stated in acknowledgement; see paper authors) | DOE EERE / Advanced Manufacturing Office | DE-EE0010214 | not stated | Project titled “High-Entropy Alloy-Based Coating to Protect Critical Components in Hydrogen Turbine Power System”; the paper uses CALPHAD-based multi-objective Bayesian optimization to minimize CTE and sigma-solvus temperature for high-temperature alloy discovery. (sundar2025calphadbasedbayesianoptimization pages 9-9) | not stated | sundar2025-JMR (sundar2025calphadbasedbayesianoptimization pages 9-9) |
| Authors of Deshmukh et al. 2024; user facility acknowledgement rather than project PI statement | DOE Office of Science, Office of Basic Energy Sciences user facility (Center for Nanoscale Materials) | DE-AC02-06CH11357 | not stated | Contract supporting the Center for Nanoscale Materials user facility acknowledged for work on active learning of ternary alloy structures and energies. (deshmukh2024activelearningof pages 10-11) | not stated | deshmukh2024-npjCM (deshmukh2024activelearningof pages 10-11) |
| Duane D. Johnson / Ames National Laboratory-Iowa State University contribution; exact PI naming not stated in acknowledgement | DOE Office of Science, Basic Energy Sciences, Materials Science and Engineering Department; Ames Lab management/operations contract | DE-AC02-07CH11358 | not stated | Ames Laboratory theory development (including KKR-CPA and SCRAPs) supporting alloy-design BO work was acknowledged under DOE Office of Science/BES support; Ames is operated by Iowa State University for DOE under this contract. (khatamsaz2023bayesianoptimizationwith pages 14-14) | not stated | khatamsaz2023-npjCM (khatamsaz2023bayesianoptimizationwith pages 14-14) |
| Ankur Kumar Gupta (institution not stated in acknowledgement; see paper authors) | DOE Office of Science, Basic Energy Sciences, Materials Sciences and Engineering Division; LBNL field work proposal | DE-AC02-05CH11231; FWP No. DAC-LBL-Long | not stated | Support acknowledged within a Bayesian optimization/materials hackathon paper; indicates BES MSE Division support connected to LBNL under a field work proposal relevant to BO in materials. (baird2025bayesianoptimizationhackathon pages 16-17) | not stated | baird2025-ChemRxiv (baird2025bayesianoptimizationhackathon pages 16-17) |
| Danny Perez / Jan Janssen / LANL-associated coauthors (institution inferred from paper authors and LANL acknowledgement) | DOE / NNSA LANL management and operations contract | 89233218CNA000001 | not stated | LANL operating contract acknowledged in a paper on deep GP-based cost-aware Bayesian optimization for materials design campaigns; this is a lab M&O contract, not a competed research award. (alvi2026deepgaussianprocessbased pages 16-17) | not stated | alvi2026-npjCM (alvi2026deepgaussianprocessbased pages 16-17) |
| Michael C. Gao and coauthors (institution not stated in acknowledgement; see paper authors) | DOE NETL site support contract | not stated | not stated | The JMR paper states the project was funded in part by the U.S. DOE National Energy Technology Laboratory through a site support contract, but the contract number is not given in the acknowledgement excerpt. (sundar2025calphadbasedbayesianoptimization pages 9-9) | not stated | sundar2025-JMR (sundar2025calphadbasedbayesianoptimization pages 9-9) |


*Table: This table consolidates unique DOE awards, contracts, and user-facility acknowledgements found in 2020–2026 Bayesian optimization and active-learning papers for materials/alloy design. It is useful for identifying which DOE sub-programs, lab contracts, and institutions are visibly supporting this research niche in the literature.*

## Trends (from acknowledgements in this 2020–2026 literature slice)

### 1) Sub-programs growing vs. shrinking (as visible in acknowledgements)
- **ARPA‑E as the most visible driver in alloy-BO papers**: ARPA‑E ULTIMATE (DE‑AR0001427) is acknowledged across multiple alloy BO methods papers and an ARPA‑E final report, suggesting sustained emphasis on autonomous materials discovery workflows within ARPA‑E’s portfolio. (khatamsaz2023bayesianoptimizationwith pages 14-14, khatamsaz2023aphysicsinformed pages 11-11, arroyave2024ultimatebirdshot.final pages 1-5)
- **ARPA‑E diversification to additional programs**: A separate ARPA‑E program, **CHADWICK (DE‑AR0001988)**, is acknowledged in 2026 work on deep GP/cost-aware batch BO for materials design campaigns, indicating ARPA‑E funding is not limited to a single program line. (alvi2026deepgaussianprocessbased pages 16-17)
- **BES support appears but is less frequent in this corpus**: Office of Science/BES appears via the **BES Data Science Initiative (DE‑SC0020381)** and via national-lab/user facility contracts (e.g., DE‑AC02‑06CH11357; DE‑AC02‑07CH11358). These acknowledgements demonstrate DOE Office of Science engagement, but with fewer distinct competed awards captured here than ARPA‑E. (deshmukh2024activelearningof pages 10-11, khatamsaz2023bayesianoptimizationwith pages 14-14)
- **EERE/AMO and NETL appear in a targeted high-temperature alloy/coatings context**: One CALPHAD+multi-objective BO paper acknowledges **EERE Advanced Manufacturing Office (DE‑EE0010214)** and also NETL site support (contract number not provided), suggesting some coupling of BO with manufacturing-relevant alloy/coating development. (sundar2025calphadbasedbayesianoptimization pages 9-9)

### 2) Dominant institutions and PI clusters (from acknowledging papers)
- **Texas A&M-centered cluster dominates ARPA‑E alloy-BO acknowledgements**: Multiple alloy BO papers acknowledging ARPA‑E ULTIMATE (DE‑AR0001427) share overlapping authorship including Raymundo Arróyave, Douglas Allaire, Brent Vela, and Danial Khatamsaz, consistent with a concentrated PI/network driving ARPA‑E-visible output in this niche. (khatamsaz2023bayesianoptimizationwith pages 14-14, khatamsaz2023aphysicsinformed pages 11-11, khatamsaz2023multiobjectivebayesianoptimization pages 10-11)
- **Northwestern cluster visible under BES Data Science Initiative**: Active learning for ternary alloy structures/energies acknowledges **DE‑SC0020381** (BES Data Science Initiative), with authorship including Jeffrey Greeley and collaborators, indicating a separate PI cluster aligned to Office of Science/BES data-science funding. (deshmukh2024activelearningof pages 10-11)
- **National labs appear as enabling partners**: Ames Laboratory and LANL appear via contract identifiers (DE‑AC02‑07CH11358; 89233218CNA000001), reflecting lab involvement, but these identifiers are management/operations contracts rather than uniquely identifying a competed research grant. (khatamsaz2023bayesianoptimizationwith pages 14-14, alvi2026deepgaussianprocessbased pages 16-17)

### 3) Newer (2022+) agency programs funding this topic (visible here)
- **ARPA‑E CHADWICK (DE‑AR0001988)** appears in a 2026 BO-for-materials paper, representing a post‑2022 visible program line in this corpus for BO methods applied to materials design. (alvi2026deepgaussianprocessbased pages 16-17)
- **BES Data Science Initiative (DE‑SC0020381)** appears in a 2024 npj Computational Materials paper for active learning in alloy systems, reflecting continued Office of Science/BES investment in data-driven discovery. (deshmukh2024activelearningof pages 10-11)

### 4) Gaps / opportunities suggested by what is *not* visible in acknowledgements
- **Sparse explicit BES/DMSE core award numbers in alloy-BO methods papers**: Aside from DE‑SC0020381 and lab/user-facility contracts, this dataset contains few explicit DE‑SC* awards tied to DMSE/BES core research in BO acquisition functions, constrained BO, or multi-objective BO for alloys; this could represent an opportunity for more explicit BES/DMSE programmatic investment in BO methodology plus autonomous experimentation integration. (deshmukh2024activelearningof pages 10-11, khatamsaz2023bayesianoptimizationwith pages 14-14)
- **Few explicit LDRD award identifiers**: National-lab participation is visible through M&O contracts and user facilities, but explicit LDRD project numbers are not commonly reported in these acknowledgements; if LDRD is funding this area, it is not strongly surfaced in the subset of publications examined here. (alvi2026deepgaussianprocessbased pages 16-17, deshmukh2024activelearningof pages 10-11)
- **Limited visibility of AMMTO/HPC4Mfg-style acknowledgements in alloy-BO papers**: While AMO/EERE appears (DE‑EE0010214), explicit AMMTO/HPC4Mfg identifiers were not observed in the extracted acknowledgements here, suggesting potential whitespace for manufacturing-oriented BO + closed-loop alloy/process optimization programs to increase visibility in publications. (sundar2025calphadbasedbayesianoptimization pages 9-9)

### Evidence note / limitation
This analysis is strictly based on DOE identifiers explicitly present in the acknowledgements/funding text of the retrieved 2020–2026 papers and reports. It should be interpreted as a **lower bound** on DOE activity (acknowledgements are incomplete, inconsistent, and many relevant papers may not have been retrieved in this run). (deshmukh2024activelearningof pages 10-11, khatamsaz2023bayesianoptimizationwith pages 14-14, alvi2026deepgaussianprocessbased pages 16-17, sundar2025calphadbasedbayesianoptimization pages 9-9)



References

1. (deshmukh2024activelearningof pages 10-11): Gaurav Deshmukh, Noah J. Wichrowski, Nikolaos Evangelou, Pushkar G. Ghanekar, Siddharth Deshpande, Ioannis G. Kevrekidis, and Jeffrey Greeley. Active learning of ternary alloy structures and energies. npj Computational Materials, 10:1-11, May 2024. URL: https://doi.org/10.1038/s41524-024-01256-z, doi:10.1038/s41524-024-01256-z. This article has 19 citations and is from a peer-reviewed journal.

2. (khatamsaz2023bayesianoptimizationwith pages 14-14): Danial Khatamsaz, Brent Vela, Prashant Singh, Duane D. Johnson, Douglas Allaire, and Raymundo Arróyave. Bayesian optimization with active learning of design constraints using an entropy-based approach. npj Computational Materials, 9:1-14, Apr 2023. URL: https://doi.org/10.1038/s41524-023-01006-7, doi:10.1038/s41524-023-01006-7. This article has 107 citations and is from a peer-reviewed journal.

3. (khatamsaz2023aphysicsinformed pages 11-11): Danial Khatamsaz, Raymond Neuberger, Arunabha M. Roy, Sina Hossein Zadeh, Richard Otis, and Raymundo Arróyave. A physics informed bayesian optimization approach for material design: application to niti shape memory alloys. npj Computational Materials, 9:1-11, Dec 2023. URL: https://doi.org/10.1038/s41524-023-01173-7, doi:10.1038/s41524-023-01173-7. This article has 64 citations and is from a peer-reviewed journal.

4. (alvi2026deepgaussianprocessbased pages 16-17): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 3 citations and is from a peer-reviewed journal.

5. (sundar2025calphadbasedbayesianoptimization pages 9-9): Aditya Sundar, Xingru Tan, Shanshan Hu, and Michael C. Gao. Calphad-based bayesian optimization to accelerate alloy discovery for high-temperature applications. Journal of Materials Research, 40:112-122, Jan 2025. URL: https://doi.org/10.1557/s43578-024-01489-0, doi:10.1557/s43578-024-01489-0. This article has 8 citations and is from a peer-reviewed journal.

6. (arroyave2024ultimatebirdshot.final pages 1-5): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

7. (khatamsaz2023multiobjectivebayesianoptimization pages 10-11): Danial Khatamsaz and Douglas L. Allaire. Multi-objective bayesian optimization using an active subspace-based approach. AIAA SCITECH 2023 Forum, Jan 2023. URL: https://doi.org/10.2514/6.2023-2203, doi:10.2514/6.2023-2203. This article has 1 citations.

8. (baird2025bayesianoptimizationhackathon pages 16-17): Sterling Baird, Mehrad Ansari, Zartashia Afzal, Qianxiang Ai, Alexander Al-Feghali, Mathieu Alain, Matias Altamirano, Thomas Andrews, Andy Sode Anker, Rija Ansari, Samuel Ampofo Appiah, Raul Astudillo, Ruhana Azam, Mohammed Azzouzi, Suneel Kumar BVS, Ben Blaiszik, Anna Borisova, Andres Bran, Pengfei Cai, Ting-Yeh Chen, Curtis Chong, Samantha Corapi, Mark Croxall, Gbetondji Dovonon, Jose Manuel Napoles Duarte, Andrew Falkowski, Giuseppe Fisicaro, Martin Fitzner, Quinn Gallagher, Sabah Gaznaghi, Jerome Genzling, Christoph Griehl, Ryan-Rhys Griffiths, Taicheng Guo, Kehan Guo, Nipun Gupta, Ankur Gupta, Mohammad Haddadnia, Yuyang Han, Joscha Hoche, Alexander V. Hopp, Marko Huang, Ayodeji Ijishakin, Ramsey Issa, Yeonghun Kang, Jungtaek Kim, Akshay Kudva, Ruben Laplaza, Magdalena Lederbauer, Shi Xuan Leong, Paul W. Leu, Viola Muning Li, Mingxuan Li, Tao Liu, Stanley Lo, Jakub Lala, Osman Mamun, Owen Melville, Michail Mitsakis, Cameron Movassaghi, Madhav Reddy Muthyala, Marcel Muller, Bozhao Nan, Duc Nguyen, Daniele Ongari, Anthony Onwuli, Can Ozkan, Sergio Pablo-Garcia, Elton Pan, Ratish Panda, Sean Park, Jaehee Park, Dieter Plessers, Tobias Plotz, Ella M. Rajaonson, Bojana Rankovic, Jarett Ren, Rim Rihana, Jurgis Ruza, Akhil S. Nair, Carter Salbego, Erick Lopez Saldivar, Arifin San, Christina Schenk, Stefan P. Schmid, Dylan Schubert, Philippe Schwaller, Cher-Tian Ser, Maitreyee Sharma Priyadarshini, Yuxin Shen, Kevin Shen, Jiale Shi, Farshud Sorourifar, Adrian Sosic, Taylor Sparks, Jan Christopher Spies, Felix Strieth-Kalthoff, Suraj Sudhakar, Aditya Sundar, Alessio Tamburro, Clara Tamura, Yifeng Tang, Dandan Tang, Nikhil Thota, Mohammad Erfan Toloue Sadegh Azadi, Gary Tom, Sang Truong, Ricardo Valencia Albornoz, Luis Walter, Lawrence Wang, Fanjin Wang, Andrew Wang, Yiran Wang, Jeffrey Watchorn, Benjamin Weiser, Geemi Wellawatte, Alexander Wieczorek, Tim Wurger, Ilya Yakavets, Jakob Zeitler, Sylvester Zhang, Yimu Zhao, Yanqiao Zhu, Ruijie Zhu, and Yunheng Zou. Bayesian optimization hackathon for chemistry and materials. ChemRxiv, Jun 2025. URL: https://doi.org/10.26434/chemrxiv-2025-dzh5z, doi:10.26434/chemrxiv-2025-dzh5z. This article has 1 citations.
