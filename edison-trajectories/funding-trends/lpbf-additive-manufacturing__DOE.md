# Funding trends: lpbf additive manufacturing — DOE

*Edison `LITERATURE` task `75f3b93e-1e77-4661-94bd-39cf690ea323` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
laser powder bed fusion of metals to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: laser powder bed fusion (LPBF / L-PBF / SLM) additive manufacturing of metallic alloys including process-structure-property relationships, in-situ sensing, qualification, and process parameter optimization

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


## Executive summary (DOE posture in LPBF metals, 2020–2026)
Across the 2020–2026 literature examined, DOE support for LPBF/SLM of metallic alloys shows up most visibly through **ARPA‑E** (especially the **ULTIMATE** portfolio and the ARPA‑E/**FES GAMOW** fusion cohort) and through **EERE’s AMMTO** via ORNL-sponsored technical work on in‑situ sensing/qualification and data/AI workflows for defect characterization and qualification. Multiple ARPA‑E projects run on ~2021–2024 periods and exhibit structured milestone reporting plus follow‑on dollars (e.g., a reported $9.5M follow‑on for BIRDSHOT and smaller follow‑on lines such as INFUSE/BES/DOE‑NE in an ODS‑steel program). The literature also indicates that **DOE national-lab internal mechanisms** (e.g., Sandia Grand Challenge LDRD; ORNL LDRD AI Initiative) are being used to push AI‑enabled process/qualification capabilities relevant to closed-loop control and autonomous discovery. In this retrieved corpus, **BES/DE‑SC awards are not frequently acknowledged with traceable PI/award mappings** (beyond follow‑on lines or generic examples), suggesting that for LPBF‑specific work the publicly visible acknowledgements skew toward ARPA‑E, EERE/AMMTO/ORNL, and lab-internal funding. (arroyave2024ultimatebirdshot.final pages 1-5, alman2024finalscientifictechnicalreport pages 1-5, sprayberry2024assessmentandusage pages 1-9, tabassum2412adaptingsegmentanything pages 9-11, boyce2024beyondfingerprintingaiguideddiscovery pages 1-5, zhang2025finalarpaereport pages 1-7, zhang2025finalarpaereport pages 16-19, zhang2025finalarpaereport media 1a7e068b)

## DOE-funded projects acknowledged in recent LPBF literature (one row per project)
| DOE sub-agency / program | PI(s) & institution | Award / contract number(s) | Amount (if stated) | Period of performance (if stated) | Project title or short description | Citation key(s) | Evidence |
|---|---|---|---|---|---|---|---|
| DOE ARPA-E ULTIMATE | Raymundo Arroyave, Texas A&M University | DE-AR0001427 | not stated; follow-on funding table lists BIRDSHOT center: $9.5M | not stated | ULTIMATE: BIRDSHOT is an ARPA-E-supported effort on accelerated alloy/process discovery for high-temperature turbine materials, including additive-manufacturing-relevant design and validation workflows. | arroyave2024ultimatebirdshot.final | (arroyave2024ultimatebirdshot.final pages 1-5, arroyave2024ultimatebirdshot.final pages 16-19, arroyave2024ultimatebirdshot.final pages 19-21) |
| DOE ARPA-E | John Sharon, RTX Technology Research Center (RTRC) | DE-AR0001422 | not stated | 04/15/2021–07/14/2023 | Computationally guided ODS refractory HEAs via additive manufacturing; the report states the work was funded in part by ARPA-E under Award DE-AR0001422. | sharon2023computationallyguidedodsrefractory | (sharon2023computationallyguidedodsrefractory pages 1-4) |
| DOE ARPA-E ULTIMATE | John Perepezko, University of Wisconsin–Madison | DE-AR0001431 | not stated | not stated | Additive manufacturing of ultrahigh-temperature refractory metal alloys using LPBF/reactive synthesis approaches for Mo-Si-B-Ti-class systems aimed at turbine efficiency gains. | perepezko2023additivemanufacturingof | (perepezko2023additivemanufacturingof pages 1-8, perepezko2023additivemanufacturingof pages 11-12) |
| DOE ARPA-E ULTIMATE | David Alman, National Energy Technology Laboratory (NETL) | DE-AR-0001430 | not stated | 06/14/2021–12/31/2023 | Rapid Design and Manufacturing of High-Performance Materials for Turbine Blades; NETL-led ARPA-E ULTIMATE project on rapid design/manufacture of high-performance turbine-blade materials with AM relevance. | alman2024finalscientifictechnicalreport | (alman2024finalscientifictechnicalreport pages 1-5) |
| DOE ARPA-E / FES GAMOW | not clearly stated in excerpt; report executed through PNNL with Ames National Laboratory involvement | Award 20/CJ000/09/03; FOA DE-FOA-0002288; PNNL contract DE-AC05-76RL01830; Ames contract DEAC02-07CH11358 | not stated; follow-on table lists INFUSE $200k, BES $400k, DOE-NE INM $675k, PNNL SPPSi $85k, SCGC $80k | 02/24/2021–02/24/2024 | Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments under the joint ARPA-E/FES GAMOW program; the report gives the ARPA-E award, FOA number, DOE lab management contracts, and follow-on funding categories/amounts. | zhang2025finalarpaereport | (zhang2025finalarpaereport pages 7-10, zhang2025finalarpaereport pages 1-7, zhang2025finalarpaereport pages 16-19, zhang2025finalarpaereport pages 19-20, zhang2025finalarpaereport media 1a7e068b) |
| DOE EERE / AMMTO | Michael Sprayberry, Thomas Butcher, Ryan Dehoff; Oak Ridge National Laboratory | DE-AC05-00OR22725; project id M4CT-24OR1307021 | not stated | not stated | Assessment and Usage of In-Situ Monitoring Data for ASME Part Qualification; ORNL technical report supporting DOE’s Advanced Materials and Manufacturing Technologies Office. | sprayberry2024assessmentandusage | (sprayberry2024assessmentandusage pages 1-9, sprayberry2024assessmentandusage pages 18-21) |
| DOE EERE / AMMTO + ORNL LDRD | Anika Tabassum, Amirkoushyar Ziabari; Oak Ridge National Laboratory | DE-AC05-00OR22725; ORNL LDRD (no award number stated) | not stated | not stated | AM/XCT defect segmentation paper acknowledging sponsorship by DOE EERE’s AMMTO under ORNL contract DE-AC05-00OR22725 and by the Artificial Intelligence Initiative under ORNL LDRD. | tabassum2412adaptingsegmentanything | (tabassum2412adaptingsegmentanything pages 9-11) |
| DOE HPC4EI / ORNL CRADA (AMO/AMMTO-adjacent) | Xiaohua Hu, Jiahao Cheng and collaborators; Oak Ridge National Laboratory with Ford collaborators | DE-AC05-00OR22725; CRADA/NFE-21-08507; ORNL/SPR-2022/2707 | not stated | not stated | Extend an innovative HPC-Compatible Multiple Temporal-spatial Resolution Concurrent Finite Element Modeling Approach to Guide Laser Powder Bed Fusion Additive; ORNL–Ford LPBF modeling collaboration in DOE Advanced Manufacturing Office context. | hu2023extendaninnovative | (hu2023extendaninnovative pages 1-6) |
| DOE HPC4EI / ORNL CRADA Final Report | Balasubramaniam Radhakrishnan, Oak Ridge National Laboratory; Tahany El-Wardany, Raytheon Technologies Research Center; Ranadip Acharya, Collins Aerospace Applied Research and Technology | DE-AC05-00OR22725; CRADA Final Report NFE-21-08592 | not stated | not stated | Development of HPC based phase field simulations tool for modification of alloy morphology to enhance material properties during additive manufacturing (AM) process; identified as part of the High Performance Computing for Energy Innovation program. | radhakrishnan2023developmentofhpc | (radhakrishnan2023developmentofhpc pages 1-6) |
| DOE national-lab LDRD (Sandia Grand Challenge) | Brad Boyce et al., Sandia National Laboratories | SAND2024-11708; no LDRD award number stated | not stated | 2021–2024 | BeyondFingerprinting is a 2021–2024 Sandia Grand Challenge LDRD supporting AI-guided discovery of robust materials and processes, explicitly including laser powder bed fusion as an exemplar area. | boyce2024beyondfingerprintingaiguideddiscovery | (boyce2024beyondfingerprintingaiguideddiscovery pages 1-5) |


*Table: This table consolidates DOE-funded LPBF/SLM metal additive manufacturing projects identified in the evidence, with exact award and contract identifiers, named PIs and institutions where stated, and explicit amounts or periods only when present in the source material.*

## Trends
### 1) Which DOE sub-programs are growing vs. shrinking in this topic?
**Observable growth signals in this literature sample** concentrate in ARPA‑E portfolios where AM is mission-critical (turbine efficiency materials and fusion-materials manufacturing). The ULTIMATE portfolio appears repeatedly with distinct awards spanning 2021–2023/2024 performance windows (DE‑AR0001422; DE‑AR0001427; DE‑AR‑0001430; DE‑AR0001431), indicating sustained ARPA‑E emphasis on rapid alloy/process development and qualification-relevant data generation connected to LPBF and related AM routes. (sharon2023computationallyguidedodsrefractory pages 1-4, arroyave2024ultimatebirdshot.final pages 1-5, alman2024finalscientifictechnicalreport pages 1-5, perepezko2023additivemanufacturingof pages 1-8)

For ARPA‑E’s fusion-related manufacturing efforts, the ARPA‑E/FES **GAMOW** program appears as a structured mechanism explicitly funding advanced manufacturing and materials development (award 20/CJ000/09/03; FOA DE‑FOA‑0002288), and an external retrospective highlights multi‑million‑dollar GAMOW awards with explicit AM scope across 2018–2022 and follow-on selections under later OPEN solicitations. (zhang2025finalarpaereport pages 1-7, zhang2025finalarpaereport pages 7-10, hsu2025retrospectiveofthe pages 12-14)

**EERE/AMMTO** support is repeatedly visible through ORNL execution under contract **DE‑AC05‑00OR22725**, including in‑situ monitoring for qualification and AI/CT defect characterization; however, the available documents often cite the site contract and internal project identifiers rather than distinct financial-assistance award numbers, which limits visibility into “growth vs shrinking” from acknowledgements alone. (sprayberry2024assessmentandusage pages 1-9, tabassum2412adaptingsegmentanything pages 9-11)

In the retrieved papers, **BES/Office of Science (DE‑SC…) is weakly visible** for LPBF specifically: a GAMOW final report lists “BES” as a follow‑on funding category with a dollar amount but without a DE‑SC award number; a separate policy/econometrics paper provides DE‑SC examples but not LPBF-specific PI mappings. Thus, any claim of growth/decline for BES in LPBF cannot be supported from this corpus alone. (zhang2025finalarpaereport media 1a7e068b, popp2026governmentfundingand pages 44-47)

### 2) Which institutions and PIs dominate (in the retrieved corpus)?
ARPA‑E ULTIMATE awards in this sample cluster around **Texas A&M (Arroyave)**, **NETL (Alman)**, **University of Wisconsin–Madison (Perepezko)**, and **RTX Technology Research Center (Sharon)**. (arroyave2024ultimatebirdshot.final pages 1-5, alman2024finalscientifictechnicalreport pages 1-5, perepezko2023additivemanufacturingof pages 1-8, sharon2023computationallyguidedodsrefractory pages 1-4)

EERE/AMMTO acknowledgements cluster strongly around **Oak Ridge National Laboratory**, including work on qualification-relevant in‑situ monitoring datasets/analysis and AI‑assisted defect characterization. (sprayberry2024assessmentandusage pages 1-9, tabassum2412adaptingsegmentanything pages 9-11)

### 3) New agency programs (launched 2022+) funding this topic
Within the constraints of literature-only acknowledgements retrieved here, the clearest “newer” signals are not new DOE program names but **newer AI-focused internal lab initiatives** connected to qualification workflows, such as the ORNL **Artificial Intelligence Initiative** under **LDRD** explicitly acknowledged alongside AMMTO sponsorship. (tabassum2412adaptingsegmentanything pages 9-11)

The ARPA‑E fusion retrospective also notes later follow-on selection activity under **ARPA‑E Vision OPEN 2024**, consistent with continued ARPA‑E use of OPEN-style vehicles to fund AM-relevant fusion manufacturing projects beyond the original GAMOW window. (hsu2025retrospectiveofthe pages 12-14)

### 4) Gaps/opportunities for DOE in LPBF metals (as inferred from acknowledgement visibility)
**Gap 1: Limited BES award traceability in LPBF papers.** In this corpus, LPBF papers seldom acknowledge DE‑SC award numbers with PI/institution mappings, even when “BES” appears as follow‑on. If DOE BES/DMSE and EFRCs are funding LPBF process–structure–property and in‑situ sensing at scale, it is not readily visible from these retrieved acknowledgements, suggesting an opportunity to (i) improve acknowledgement capture in publications, and/or (ii) create clearer program identity for LPBF-focused BES efforts. (zhang2025finalarpaereport media 1a7e068b, popp2026governmentfundingand pages 44-47)

**Gap 2: Autonomous closed-loop alloy discovery positioning.** The portfolio evidence shows ARPA‑E funding for accelerated alloy/process discovery (ULTIMATE) and EERE/AMMTO + lab LDRD funding for sensing/qualification/AI infrastructure. A proposal positioned around **closed-loop alloy discovery that connects in‑situ sensing → qualification → autonomous optimization** sits directly at the intersection of these already-funded thrusts, but the literature suggests these elements are often funded in separate “lanes” (ARPA‑E alloy acceleration vs AMMTO qualification infrastructure vs LDRD AI). A DOE Genesis Phase I could explicitly integrate these lanes into an end-to-end autonomy stack. (arroyave2024ultimatebirdshot.final pages 1-5, sprayberry2024assessmentandusage pages 1-9, tabassum2412adaptingsegmentanything pages 9-11, boyce2024beyondfingerprintingaiguideddiscovery pages 1-5)

**Gap 3: Award metadata in publications for applied programs.** For AMMTO/ORNL and CRADA work, publications often cite the site contract (DE‑AC05‑00OR22725) and CRADA IDs (e.g., NFE‑21‑08507; NFE‑21‑08592) rather than financial assistance award numbers. This complicates portfolio analysis and PI tracking from literature alone; proposals and program offices could benefit from encouraging inclusion of project identifiers in a consistent, searchable form across papers. (hu2023extendaninnovative pages 1-6, radhakrishnan2023developmentofhpc pages 1-6, sprayberry2024assessmentandusage pages 1-9)


References

1. (arroyave2024ultimatebirdshot.final pages 1-5): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

2. (alman2024finalscientifictechnicalreport pages 1-5): David Alman, Michael C. Gao, Michael Kirka, and Michael Widom. Final scientific/technical report rapid design and manufacturing of high-performance materials for turbine blades. ArXiv, Apr 2024. URL: https://doi.org/10.2172/2404558, doi:10.2172/2404558. This article has 1 citations.

3. (sprayberry2024assessmentandusage pages 1-9): Michael Sprayberry, Thomas Butcher, and Ryan Dehoff. Assessment and usage of in-situ monitoring data for asme part qualification. ArXiv, Oct 2024. URL: https://doi.org/10.2172/2455077, doi:10.2172/2455077. This article has 0 citations.

4. (tabassum2412adaptingsegmentanything pages 9-11): Anika Tabassum and Amirkoushyar Ziabari. Adapting segment anything model (sam) to experimental datasets via fine-tuning on gan-based simulation: a case study in additive manufacturing. ArXiv, Dec 2412. URL: https://doi.org/10.48550/arxiv.2412.11381, doi:10.48550/arxiv.2412.11381. This article has 5 citations.

5. (boyce2024beyondfingerprintingaiguideddiscovery pages 1-5): Brad Boyce, Rémi Dingreville, David Adams, Carianne Martinez, James Fowler, Jamin Pillars, Ryan Wixom, Harry Moffat, Warren Davis, Sarah Ackerman, Ann Speed, Anthony Garland, Scott Roberts, Jonathan Coleman, Frank DelRio, Dale Cillessen, Jay Carroll, Habib Najm, John Curry, Kyle Johnson, Sarah Dudley, Sadhvikas Addamane, Amelia Henriksen, Joyce Custer, Jacqueline Wentz, Saaketh Desai, Kimberly Bassett, Troy Shilt, Elise Walker, Matias Kalaswad, Ankit Shrivastava, Tomas Babuska, Matthew Kottwitz, Kaitlynn Fitzgerald, Jonas Actor, Niladri Das, Nathan Bianco, Tylan Watkins, Kyle Dorman, Reese Jones, and Mohammad Khalil. Beyondfingerprinting: ai-guided discovery of robust materials & processes. ArXiv, Sep 2024. URL: https://doi.org/10.2172/2462990, doi:10.2172/2462990. This article has 0 citations.

6. (zhang2025finalarpaereport pages 1-7): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

7. (zhang2025finalarpaereport pages 16-19): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

8. (zhang2025finalarpaereport media 1a7e068b): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

9. (arroyave2024ultimatebirdshot.final pages 16-19): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

10. (arroyave2024ultimatebirdshot.final pages 19-21): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

11. (sharon2023computationallyguidedodsrefractory pages 1-4): John Sharon, Anthony Ventura, Ryan Deacon, Ken Smith, and Soumalya Sarkar. Computationally-guided ods refractory heas via additive manufacturing. ArXiv, Oct 2023. URL: https://doi.org/10.2172/2375527, doi:10.2172/2375527. This article has 0 citations.

12. (perepezko2023additivemanufacturingof pages 1-8): John Perepezko. Additive manufacturing of ultrahigh temperature refractory metal alloys. ArXiv, Nov 2023. URL: https://doi.org/10.2172/2397338, doi:10.2172/2397338. This article has 0 citations.

13. (perepezko2023additivemanufacturingof pages 11-12): John Perepezko. Additive manufacturing of ultrahigh temperature refractory metal alloys. ArXiv, Nov 2023. URL: https://doi.org/10.2172/2397338, doi:10.2172/2397338. This article has 0 citations.

14. (zhang2025finalarpaereport pages 7-10): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

15. (zhang2025finalarpaereport pages 19-20): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

16. (sprayberry2024assessmentandusage pages 18-21): Michael Sprayberry, Thomas Butcher, and Ryan Dehoff. Assessment and usage of in-situ monitoring data for asme part qualification. ArXiv, Oct 2024. URL: https://doi.org/10.2172/2455077, doi:10.2172/2455077. This article has 0 citations.

17. (hu2023extendaninnovative pages 1-6): Extend an innovative HPC-Compatible Multiple Temporal-spatial Resolution Concurrent Finite Element Modeling Approach to Guide Laser Powder Bed Fusion Additive

18. (radhakrishnan2023developmentofhpc pages 1-6): Balasubramaniam Radhakrishnan, Tahany El-Wardany, and Ranadip Acharya. Development of HPC based phase field simulations tool for modification of alloy morphology to enhance material properties during additive manufacturing (AM) process. Office of Scientific and Technical Information (OSTI), Apr 2023. URL: https://doi.org/10.2172/1968682, doi:10.2172/1968682.

19. (hsu2025retrospectiveofthe pages 12-14): S. C. Hsu, M. C. Handley, S. E. Wurzel, and P. B. McGrath. Retrospective of the arpa-e bethe-gamow-era fusion programs and project cohorts. Journal of Fusion Energy, Aug 2025. URL: https://doi.org/10.1007/s10894-025-00504-4, doi:10.1007/s10894-025-00504-4. This article has 0 citations and is from a peer-reviewed journal.

20. (popp2026governmentfundingand pages 44-47): David Popp, Myriam Gregoire-Zawilski, Lizhen Liang, and Daniel E. Acuna. Government Funding and the Direction of Academic Energy Research. National Bureau of Economic Research, Feb 2026. URL: https://doi.org/10.3386/w34856, doi:10.3386/w34856. This article has 1 citations.
