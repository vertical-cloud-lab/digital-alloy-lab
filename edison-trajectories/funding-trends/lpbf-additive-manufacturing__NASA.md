# Funding trends: lpbf additive manufacturing — NASA

*Edison `LITERATURE` task `859b7300-1161-4669-8067-5ecfaa1449ae` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
laser powder bed fusion of metals to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: laser powder bed fusion (LPBF / L-PBF / SLM) additive manufacturing of metallic alloys including process-structure-property relationships, in-situ sensing, qualification, and process parameter optimization

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


## Executive summary (NASA posture in LPBF metals, 2020–2026)
NASA-visible funding in the inspected 2020–2026 LPBF/PBF-LB/M metallic additive manufacturing literature concentrates on (i) STMD and propulsion-focused programs at NASA centers (especially Marshall, with Glenn as a major materials partner) and (ii) university-facing mechanisms supporting qualification-relevant datasets and process windows (ULI, and more recently STRI). STMD program acknowledgements frequently appear as project-level attributions (e.g., RAMPT; Game Changing Program/ORCA; TTT) without public award numbers in the papers, whereas university awards more often include explicit 80NSSC* award IDs. Within this limited corpus, explicit mentions of NASA SBIR/STTR, ECF, ESI, EPSCoR, or ULI consortia details (PIs/PoP/amounts) are sparse or absent in the papers’ funding sections, suggesting that many NASA investments in this area may be reported in venues other than journal acknowledgements (e.g., solicitations, award databases, or technical reports) or that authors do not consistently include award metadata. Overall, NASA’s posture appears to emphasize qualification, repeatability, and propulsion hardware readiness (including alloy development such as HR-series and GRX-810) rather than explicitly framing autonomous closed-loop alloy discovery, which may represent an opportunity for a DOE Genesis Phase I proposal narrative (gap/adjacency).

## NASA-funded projects acknowledged in recent LPBF metals literature (2020–2026)
| PI name(s) and institution | NASA grant program / sub-program | Award number(s) | Award amount | Project title / short description | Year started / period of performance | Citation key(s) |
|---|---|---|---|---|---|---|
| John J. Lewandowski (funding acquisition; Case Western Reserve University); collaborating NASA ULI fabrication team not fully stated | NASA University Leadership Initiative (ULI) | 80NSSC19M0123 | not stated | Funding statement names the project as **"Development of an Ecosystem for ‘Qualification of Additive Manufacturing Process and Materials in Aviation’"**. In the cited paper, this ULI supports fatigue-based process-window development for LPBF/PBF-LB/M Ti-6Al-4V and defect-informed qualification datasets. | not stated | (ley2026datasetonfatigue pages 17-19, ley2026datasetonfatigue media e2cc7664, ley2026datasetonfatigue pages 1-3) |
| not stated; institution not stated in funding statement (paper authors at Case Western Reserve University / Naval Surface Warfare Center Carderock Division) | NASA Space Technology Research Institute (STRI) | 80NSSC23K1342 | not stated | The paper explicitly cites support from the NASA STRI program under grant 80NSSC23K1342. In context, the support is connected to LPBF/PBF-LB/M Ti-6Al-4V fatigue, defect characterization, and qualification-oriented data generation. | not stated | (ley2026datasetonfatigue pages 17-19, ley2026datasetonfatigue pages 19-20, ley2026datasetonfatigue media e2cc7664, ley2026datasetonfatigue pages 1-3) |
| Nima Shamsaei (Auburn University / NCAME); NASA coauthors Poshou Chen, Colton Katsarelis, Paul Gradl (NASA Marshall Space Flight Center) | NASA center-linked award acknowledged in paper | 80MSFC19C0010 | not stated | The paper states it was partially funded by NASA under Award #80MSFC19C0010. The funded work studies NASA HR-1 for additive manufacturing, focusing on process–microstructure–property effects in laser powder directed energy deposition and relevance to LPBF-adjacent propulsion alloy development. | not stated | (soltanitehrani2022laserpowderdirected pages 11-11, soltanitehrani2022laserpowderdirected pages 1-2) |
| not stated; authors are Paul Gradl, Darren C. Tinker, Alison Park, Omar R. Mireles, Marissa Garcia, Ryan Wilkerson, Christopher Mckinney (NASA Marshall Space Flight Center; NASA Engineering and Safety Center/Langley for Park) | NASA STMD Rapid Analysis and Manufacturing Propulsion Technology (RAMPT) Project | not stated | not stated | The acknowledgements state the research was funded by NASA through the STMD RAMPT Project. The paper covers metal AM process selection/development for aerospace components, including LPBF qualification, alloy characterization, pathfinder hardware, and propulsion-relevant process development. | not stated | (gradl2022robustmetaladditive pages 21-22, gradl2022robustmetaladditive pages 1-2) |
| not stated; authors are Paul R. Gradl, Timothy M. Smith, Darren C. Tinker, Benjamin B. Williams, Christopher A. Kantzos (NASA Marshall Space Flight Center; NASA Glenn Research Center) | NASA STMD Game Changing Program – ORCA; NASA Transformational Tools and Technology (TTT) | not stated | not stated | The acknowledgements identify support from **Optimized and Repeatable Components using Additive (ORCA)** under the STMD Game Changing Program and from **Transformational Tools and Technology (TTT)**. The paper develops and hot-fire tests the GRX-810 alloy using L-PBF and LP-DED for extreme-temperature propulsion hardware. | not stated | (gradl2024extremetemperatureadditively pages 15-16, gradl2024extremetemperatureadditively pages 1-3) |
| not stated; authors are Paul R. Gradl, Thomas W. Teasley, Christopher S. Protz, Colton Katsarelis (NASA Marshall Space Flight Center) and Po Chen (Jacobs at NASA Marshall) | NASA Space Launch System (SLS) Liquid Engines Office (LEO) | not stated | not stated | The acknowledgements in the HR-1 hot-fire paper state funding came from NASA via the SLS Liquid Engines Office (LEO). The work concerns process development and hot-fire testing of additively manufactured NASA HR-1 for liquid rocket engine applications, alongside LP-DED/L-PBF scaling and propulsion hardware maturation. | not stated | (gradl2021processdevelopmentand pages 20-22, gradl2021processdevelopmentand pages 1-3) |
| not stated; also acknowledged by Paul R. Gradl, Timothy M. Smith, Darren C. Tinker, Benjamin B. Williams, Christopher A. Kantzos (NASA Marshall / NASA Glenn) | NASA SLS Liquid Engine Office (LEO) | not stated | not stated | A second 2024 paper acknowledges SLS Liquid Engine Office (LEO) support alongside ORCA/TTT. In this case the funded work is extreme-temperature GRX-810 alloy development and hot-fire testing with L-PBF and LP-DED for rocket-engine components. | not stated | (gradl2024extremetemperatureadditively pages 15-16, gradl2024extremetemperatureadditively pages 1-3) |
| not stated; authors are Paul R. Gradl, Omar Roberto Mireles, Nathan Andrews (NASA Marshall Space Flight Center) | NASA Long Life Additive Manufacturing Assembly (LLAMA) Project | not stated | not stated | The acknowledgements identify the **LLAMA Project** as a NASA-supported project. In context, the document is an overview of additive manufacturing for propulsion systems, including LPBF/DED process development, qualified alloys, and RS-25 / propulsion component applications. | not stated | (gradl2022introductiontoadditive pages 60-66, gradl2022introductiontoadditive pages 66-71) |


*Table: This table compiles the distinct NASA-funded LPBF/metal AM projects and awards that were explicitly acknowledged in the inspected 2020–2026 literature corpus. It separates projects with exact award numbers from NASA program-level support mentions where no numeric award identifier was stated.*

## Trends (NASA × LPBF metals)
### Program mix (where NASA is funding)
- **STMD propulsion/manufacturing maturation programs** are repeatedly acknowledged in propulsion-centric LPBF/DED alloy development and hardware maturation work, including **RAMPT** (STMD), and **ORCA** under the **STMD Game Changing Program**, plus **TTT** (Transformational Tools and Technology). These appear as program/project attributions without award numbers in the inspected papers. (gradl2022robustmetaladditive pages 21-22, gradl2024extremetemperatureadditively pages 15-16, gradl2021processdevelopmentand pages 20-22)
- **SLS program/office support** (specifically the **SLS Liquid Engines Office (LEO)**) is directly acknowledged as a funding source in propulsion AM demonstrations. (gradl2021processdevelopmentand pages 20-22, gradl2024extremetemperatureadditively pages 15-16)
- **University-facing programs** show up with explicit award IDs in at least one qualification/fatigue dataset paper: **NASA ULI** award **80NSSC19M0123**, and a **NASA STRI** grant **80NSSC23K1342**. (ley2026datasetonfatigue pages 17-19, ley2026datasetonfatigue media e2cc7664)

### Institutions and PIs dominating (as visible in acknowledgements)
- **NASA Marshall Space Flight Center (MSFC)** appears as the dominant center in the propulsion-oriented LPBF/DED alloy/hardware papers (e.g., Gradl and colleagues), with **NASA Glenn Research Center (GRC)** prominently involved in GRX-810 extreme-temperature alloy work. (gradl2024extremetemperatureadditively pages 1-3, gradl2021processdevelopmentand pages 20-22)
- **University nodes** visible in explicit award-number acknowledgements include **Case Western Reserve University (CWRU)** (fatigue dataset; funding acquisition attributed to J.J. Lewandowski in author contributions) and **Auburn University / NCAME** (NASA HR-1 alloy processing/microstructure study; partially NASA-funded under an MSFC-linked award number). (ley2026datasetonfatigue pages 17-19, soltanitehrani2022laserpowderdirected pages 11-11)

### New(er) programs (launched 2022+) appearing in this topic
- In this literature sample, the most clearly post-2022 mechanism with an explicit award identifier is **NASA Space Technology Research Institute (STRI)** (grant **80NSSC23K1342**), acknowledged in a 2026 PBF-LB/M Ti-6Al-4V qualification dataset paper. (ley2026datasetonfatigue pages 19-20, ley2026datasetonfatigue media e2cc7664)
- Other STMD efforts (e.g., ORCA under Game Changing; TTT) are acknowledged in 2024 work but the paper does not provide award numbers, limiting the ability to date program starts precisely from acknowledgements alone. (gradl2024extremetemperatureadditively pages 15-16)

### Growing vs. shrinking
The inspected acknowledgements do not provide enough longitudinal, award-level metadata (counts by year, award values, or consistent program identifiers) to support a defensible quantitative claim about **growth vs. shrinkage** of specific NASA sub-programs in LPBF metals from 2020–2026. What can be stated is that **STMD program names and university consortium mechanisms (ULI/STRI)** both appear in 2022–2026 LPBF-related publications, indicating sustained activity across the period. (gradl2022robustmetaladditive pages 21-22, ley2026datasetonfatigue pages 17-19, gradl2024extremetemperatureadditively pages 15-16)

### Visible gaps/opportunities (where NASA is *not* clearly funding, in these acknowledgements)
- **SBIR/STTR, ECF, ESI, EPSCoR**: none of the inspected acknowledgement excerpts contained explicit SBIR/STTR/ECF/ESI/EPSCoR award numbers or program names, despite being within the user’s programs of interest. This could reflect under-reporting in journal acknowledgements or a corpus limitation; either way, it indicates that a literature-only approach may miss these mechanisms and should be complemented with NASA award databases/solicitation tracking for a complete survey. (ley2026datasetonfatigue pages 17-19, gradl2022robustmetaladditive pages 21-22)
- **Autonomous closed-loop alloy discovery / AI-driven process control**: NASA-funded work visible here emphasizes qualification, repeatability, and propulsion readiness (e.g., fatigue process windows; ORCA repeatability; propulsion alloy maturation) rather than explicitly acknowledging awards targeted at autonomous closed-loop alloy discovery. This suggests an opportunity to position closed-loop alloy discovery as an enabling layer atop NASA’s qualification-focused portfolio (e.g., linking in-situ sensing + ML to qualification evidence streams). (ley2026datasetonfatigue pages 17-19, gradl2024extremetemperatureadditively pages 15-16, gradl2022robustmetaladditive pages 21-22)

### Evidence note
The table above includes both (i) projects with **explicit NASA award numbers** and (ii) program-level attributions where the **award number was not stated** in the paper. Award amounts and periods of performance were rarely reported in the inspected papers and are therefore marked **not stated** where appropriate. (ley2026datasetonfatigue pages 17-19, soltanitehrani2022laserpowderdirected pages 11-11, gradl2022robustmetaladditive pages 21-22)

References

1. (ley2026datasetonfatigue pages 17-19): Brett E. Ley, Austin Q. Ngo, and John J. Lewandowski. Dataset on fatigue results and fatigue fracture initiation site characterization in stress-relieved pbf-lb/m ti-6al-4v four-point bend and axial specimens: part i (high power, variable scan velocities). Data, 11:81, Apr 2026. URL: https://doi.org/10.3390/data11040081, doi:10.3390/data11040081. This article has 0 citations and is from a peer-reviewed journal.

2. (ley2026datasetonfatigue media e2cc7664): Brett E. Ley, Austin Q. Ngo, and John J. Lewandowski. Dataset on fatigue results and fatigue fracture initiation site characterization in stress-relieved pbf-lb/m ti-6al-4v four-point bend and axial specimens: part i (high power, variable scan velocities). Data, 11:81, Apr 2026. URL: https://doi.org/10.3390/data11040081, doi:10.3390/data11040081. This article has 0 citations and is from a peer-reviewed journal.

3. (ley2026datasetonfatigue pages 1-3): Brett E. Ley, Austin Q. Ngo, and John J. Lewandowski. Dataset on fatigue results and fatigue fracture initiation site characterization in stress-relieved pbf-lb/m ti-6al-4v four-point bend and axial specimens: part i (high power, variable scan velocities). Data, 11:81, Apr 2026. URL: https://doi.org/10.3390/data11040081, doi:10.3390/data11040081. This article has 0 citations and is from a peer-reviewed journal.

4. (ley2026datasetonfatigue pages 19-20): Brett E. Ley, Austin Q. Ngo, and John J. Lewandowski. Dataset on fatigue results and fatigue fracture initiation site characterization in stress-relieved pbf-lb/m ti-6al-4v four-point bend and axial specimens: part i (high power, variable scan velocities). Data, 11:81, Apr 2026. URL: https://doi.org/10.3390/data11040081, doi:10.3390/data11040081. This article has 0 citations and is from a peer-reviewed journal.

5. (soltanitehrani2022laserpowderdirected pages 11-11): Arash Soltani-Tehrani, Poshou Chen, Colton Katsarelis, Paul Gradl, Shuai Shao, and Nima Shamsaei. Laser powder directed energy deposition (lp-ded) nasa hr-1 alloy: laser power and heat treatment effects on microstructure and mechanical properties. Additive Manufacturing Letters, 3:100097, Dec 2022. URL: https://doi.org/10.1016/j.addlet.2022.100097, doi:10.1016/j.addlet.2022.100097. This article has 22 citations and is from a peer-reviewed journal.

6. (soltanitehrani2022laserpowderdirected pages 1-2): Arash Soltani-Tehrani, Poshou Chen, Colton Katsarelis, Paul Gradl, Shuai Shao, and Nima Shamsaei. Laser powder directed energy deposition (lp-ded) nasa hr-1 alloy: laser power and heat treatment effects on microstructure and mechanical properties. Additive Manufacturing Letters, 3:100097, Dec 2022. URL: https://doi.org/10.1016/j.addlet.2022.100097, doi:10.1016/j.addlet.2022.100097. This article has 22 citations and is from a peer-reviewed journal.

7. (gradl2022robustmetaladditive pages 21-22): P. Gradl, Darren C. Tinker, A. Park, O. Mireles, Marissa B. Garcia, Ryan P. Wilkerson, and Christopher Mckinney. Robust metal additive manufacturing process selection and development for aerospace components. Journal of Materials Engineering and Performance, 31:6013-6044, Apr 2022. URL: https://doi.org/10.1007/s11665-022-06850-0, doi:10.1007/s11665-022-06850-0. This article has 290 citations and is from a peer-reviewed journal.

8. (gradl2022robustmetaladditive pages 1-2): P. Gradl, Darren C. Tinker, A. Park, O. Mireles, Marissa B. Garcia, Ryan P. Wilkerson, and Christopher Mckinney. Robust metal additive manufacturing process selection and development for aerospace components. Journal of Materials Engineering and Performance, 31:6013-6044, Apr 2022. URL: https://doi.org/10.1007/s11665-022-06850-0, doi:10.1007/s11665-022-06850-0. This article has 290 citations and is from a peer-reviewed journal.

9. (gradl2024extremetemperatureadditively pages 15-16): P. Gradl, Timothy M. Smith, Darren C. Tinker, Benjamin B. Williams, and Christopher A. Kantzos. Extreme temperature additively manufactured grx-810 alloy development and hot-fire testing for liquid rocket engines. AIAA SCITECH 2024 Forum, Jan 2024. URL: https://doi.org/10.2514/6.2024-0997, doi:10.2514/6.2024-0997. This article has 12 citations.

10. (gradl2024extremetemperatureadditively pages 1-3): P. Gradl, Timothy M. Smith, Darren C. Tinker, Benjamin B. Williams, and Christopher A. Kantzos. Extreme temperature additively manufactured grx-810 alloy development and hot-fire testing for liquid rocket engines. AIAA SCITECH 2024 Forum, Jan 2024. URL: https://doi.org/10.2514/6.2024-0997, doi:10.2514/6.2024-0997. This article has 12 citations.

11. (gradl2021processdevelopmentand pages 20-22): Paul R. Gradl, Thomas W. Teasley, Christopher S. Protz, Colton Katsarelis, and Po Chen. Process development and hot-fire testing of additively manufactured nasa hr-1 for liquid rocket engine applications. AIAA Propulsion and Energy 2021 Forum, Aug 2021. URL: https://doi.org/10.2514/6.2021-3236, doi:10.2514/6.2021-3236. This article has 65 citations.

12. (gradl2021processdevelopmentand pages 1-3): Paul R. Gradl, Thomas W. Teasley, Christopher S. Protz, Colton Katsarelis, and Po Chen. Process development and hot-fire testing of additively manufactured nasa hr-1 for liquid rocket engine applications. AIAA Propulsion and Energy 2021 Forum, Aug 2021. URL: https://doi.org/10.2514/6.2021-3236, doi:10.2514/6.2021-3236. This article has 65 citations.

13. (gradl2022introductiontoadditive pages 60-66): Paul R. Gradl, Omar Roberto Mireles, and Nathan Andrews. Introduction to additive manufacturing for propulsion systems. Text, Jan 2022. URL: https://doi.org/10.13140/rg.2.2.13113.93285, doi:10.13140/rg.2.2.13113.93285. This article has 18 citations and is from a peer-reviewed journal.

14. (gradl2022introductiontoadditive pages 66-71): Paul R. Gradl, Omar Roberto Mireles, and Nathan Andrews. Introduction to additive manufacturing for propulsion systems. Text, Jan 2022. URL: https://doi.org/10.13140/rg.2.2.13113.93285, doi:10.13140/rg.2.2.13113.93285. This article has 18 citations and is from a peer-reviewed journal.
