# Funding trends: self driving labs — NASA

*Edison `LITERATURE` task `0130d96c-c9c9-460b-ad39-ca1efa209a79` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
self-driving laboratories for materials/alloys to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: self-driving laboratories and autonomous experimentation for materials and metallic alloy discovery (closed-loop AI/robot-controlled synthesis-characterization-design loops, autonomous formulation, autonomous additive manufacturing)

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


## Executive summary (NASA posture, 2020–2026)
Within the accessible 2020–2026 topic-relevant literature corpus, NASA’s *award-number-visible* funding for autonomous materials/manufacturing appears concentrated in (i) STMD ecosystem programs that build enabling infrastructure and workforce (e.g., Space Technology Research Institute US‑COMP and NASA Space Technology Research Fellowship awards) and (ii) STMD-adjacent applied mechanisms such as NASA SBIR contracts and the Transformational Tools and Technologies (T3) modeling & simulation portfolio, rather than in large numbers of explicitly-cited grants for fully closed-loop alloy “self-driving laboratory” platforms. (headrick2022versatileacidsolvents pages 8-8, arnold20252040visionstudy pages 13-17)
The clearest NASA awards that show up directly in paper acknowledgements are two legacy NNX-series grants tied to advanced materials processing research (US‑COMP STRI and an NSTRF fellowship), indicating continuing NASA investment in advanced materials capability and talent pipelines. (headrick2022versatileacidsolvents pages 8-8)
On the applied/translation side, a NASA T3 implementation publication lists multiple NASA SBIR contracts explicitly tied to multiscale materials modeling and additive-manufacturing-relevant modeling tools, consistent with NASA’s use of SBIR as a pathway to mature software/toolchain components that enable autonomous/closed-loop manufacturing and qualification. (arnold20252040visionstudy pages 13-17, arnold20252040visionstudy pages 9-13)
Overall, the visible pattern suggests NASA is funding *enabling* pieces (modeling hubs, multiscale models, reliability tools, composite/computational design institutes, fellowships) more strongly than end-to-end autonomous closed-loop alloy discovery laboratories (in the sense used in the materials SDL community), representing a potential opportunity area for proposals like autonomous closed-loop alloy discovery. (headrick2022versatileacidsolvents pages 8-8, arnold20252040visionstudy pages 13-17)

## NASA-funded projects acknowledged in 2020–2026 literature
| PI name(s) & institution | NASA grant program / sub-program | Award / contract number(s) | Award amount | Project title / short description | Year started / period of performance | Citation key(s) where acknowledged |
|---|---|---|---|---|---|---|
| Matteo Pasquali (institution not stated in funding statement; paper author list includes Rice University-affiliated authors, but funding statement itself does not specify institution) | NASA Space Technology Research Institute (STRI/Space Technology Research Grants) — Ultra-Strong Composites by Computational Design (US-COMP) | NNX17AJ32G | not stated | Funding acknowledged for work tied to the NASA Space Technology Research Institute for Ultra-Strong Composites by Computational Design (US-COMP). In the paper, this support underpins advanced materials processing research involving carbon nanotube assembly. (headrick2022versatileacidsolvents pages 8-8) | implied 2017 start from award number only; otherwise not stated | headrick2022versatileacidsolvents |
| Robert J. Headrick (institution not stated in funding statement) | NASA Space Technology Research Fellowship (NSTRF14) | NNX14AL71H | not stated | NASA Space Technology Research Fellowship support acknowledged for R.J.H. The paper links this fellowship support to materials processing and manufacturing research on carbon nanotube assembly. (headrick2022versatileacidsolvents pages 8-8) | implied 2014 cohort/start from fellowship label NSTRF14; otherwise not stated | headrick2022versatileacidsolvents |
| not stated in funding statement | NASA SBIR 2023 Phase I | 80NSSC23PB480 | not stated | “Materials Modeling Hub: Interoperable and Collaborative Multi-Scale Modeling Ecosystem for Data Analysis, Visualization, and Management.” Identified in NASA's T3 implementation activities as a completed SBIR 2023 Phase I effort relevant to materials modeling infrastructure supporting advanced materials/manufacturing workflows. (arnold20252040visionstudy pages 13-17, arnold20252040visionstudy pages 9-13) | 2023 Phase I (explicit) | arnold20252040visionstudy |
| not stated in funding statement | NASA SBIR (2019 Phase I/II/IIE) | 80NSSC19C0409 | not stated | “Additive Manufacturing Innovations; A Multiscale Model for Material Systems with Hierarchical Microstructure using Generalized Method of Cells.” Listed in NASA's T3 implementation activities as an SBIR effort directly relevant to additive manufacturing and multiscale materials modeling. (arnold20252040visionstudy pages 13-17) | 2019 Phase I/II/IIE (explicit) | arnold20252040visionstudy |
| not stated in funding statement | NASA SBIR (2017 series) | 80NSSC18C0053 | not stated | CFDRC project: “Integrated Fluid and Materials Modeling of Environmental Barrier Coatings.” Included in NASA's T3 implementation activities as an SBIR-supported materials modeling effort for coating systems relevant to extreme-environment materials. (arnold20252040visionstudy pages 13-17) | not stated | arnold20252040visionstudy |
| not stated in funding statement | NASA SBIR (2019 Phase I/II) | 80NSSC19C0263 | not stated | N&R Engineering project: “Probabilistic/Reliability Software Tool for Ceramic Matrix Composite/Environmental Barrier Coating Interface Modeling.” Listed in NASA's T3 implementation activities as a NASA SBIR-supported modeling tool effort for advanced materials/coating reliability. (arnold20252040visionstudy pages 13-17) | 2019 Phase I/II (explicit) | arnold20252040visionstudy |


*Table: This table compiles the unique NASA-funded projects that were explicitly identifiable from the extracted acknowledgements and NASA program-report evidence. It is useful because it separates award-backed findings from broader program mentions and flags where PI/institution details were not stated in the accessible funding text.*

## Trends (NASA × autonomous experimentation for materials/alloys)

### 1) Sub-programs growing vs. shrinking (as visible from acknowledgements)
- **Growing/active signals in enabling and translation mechanisms**: NASA’s STMD-oriented mechanisms show recurring visibility: Space Technology Research Institute (STRI/US‑COMP), NSTRF fellowships, and multiple **SBIR contracts** listed under NASA’s T3 implementation activities (suggesting a steady pipeline of small-to-mid scale applied projects). (headrick2022versatileacidsolvents pages 8-8, arnold20252040visionstudy pages 13-17)
- **T3 portfolio scaling signal**: The T3 implementation publication states “**14 Awards approx. $3.5M/year**” for NRA awards enhancing the modeling & simulation portfolio, consistent with increasing structured investments in modeling/toolchain capabilities relevant to autonomous/closed-loop workflows. (arnold20252040visionstudy pages 9-13)
- **ECF/ESI/ULI/EPSCoR not award-number-visible in this corpus**: NASA Early Career Faculty / Early Stage Innovation are referenced as mechanisms in NASA advanced manufacturing context, but no specific award numbers were extractable from the accessible text; similarly, EPSCoR is mentioned as leveraged funding in the T3 report without itemized award IDs. (vickers2022nasaadvisorycounciltechnology pages 13-19, arnold20252040visionstudy pages 13-17)

### 2) Which institutions and PIs are dominating (from award-number-visible evidence)
- **Academic PI visibility (limited)**: The only explicitly identifiable PI tied to an award number in this corpus is **Matteo Pasquali** (acknowledging support via NASA STRI US‑COMP, NNX17AJ32G) and an associated NASA fellowship award acknowledged by **Robert J. Headrick** (NNX14AL71H). (headrick2022versatileacidsolvents pages 8-8)
- **Industry performers are prominent in SBIR contract evidence**: The NASA T3 implementation publication lists SBIR contracts associated with companies (e.g., CFDRC; N&R Engineering) for modeling tools relevant to advanced materials/coatings and AM. These entries are contract-number-specific but do not identify individual PIs in the provided text. (arnold20252040visionstudy pages 13-17)

### 3) New agency programs (launched 2022+) funding this topic (as evidenced here)
- **NASA SBIR 2023 Phase I (80NSSC23PB480)** appears explicitly, indicating continuing/new SBIR starts in 2023 directly linked to “Materials Modeling Hub” infrastructure for data analysis/visualization/management. (arnold20252040visionstudy pages 13-17, arnold20252040visionstudy pages 9-13)
- **In-Space Manufacturing (ISM 2.0) and STMD framing**: While not providing award numbers in the excerpted review text, the in-space additive manufacturing literature explicitly frames ISM 2.0 and STMD budget scales and typical project sizes, consistent with a post‑2022 portfolio emphasis on autonomous/closed-loop manufacturing in the space context. (prisacariu2026additivemanufacturingin pages 4-6)

### 4) Gaps / opportunities where NASA is not (visibly) funding but could
- **Few explicit NASA awards tied to full closed-loop alloy SDLs**: A key autonomous additive manufacturing paper’s acknowledgements, for example, list AFOSR awards but **no NASA funding**, suggesting that major materials SDL/autonomous AM demonstrations in the open literature are often funded by other agencies even when aligned with NASA-relevant manufacturing autonomy goals. (deneault2021towardautonomousadditive pages 9-10)
- **Opportunity: end-to-end autonomous alloy discovery testbeds**: The visible NASA-funded items emphasize modeling infrastructure, reliability tools, coatings/composites, and workforce development; comparatively fewer award-number-bearing acknowledgements point to integrated “synthesis–characterization–design” closed-loop alloy discovery platforms. This is a potential gap for NASA (particularly STMD/center programs) to target if autonomy-driven alloy discovery is mission-enabling (e.g., in-space manufacturing, repair, qualification). (arnold20252040visionstudy pages 13-17, headrick2022versatileacidsolvents pages 8-8)

*Limitations:* This survey is strictly based on the accessible full-text acknowledgements/funding statements retrieved here; many relevant NASA awards may not have been captured because (i) some materials SDL papers were unobtainable in full text, (ii) some NASA-relevant documents are program reports without granular award IDs, or (iii) papers may omit award numbers or use non-standard acknowledgment formats.

References

1. (headrick2022versatileacidsolvents pages 8-8): Robert J. Headrick, Steven M. Williams, Crystal E. Owens, Lauren W. Taylor, Oliver S. Dewey, Cedric J. Ginestra, Lucy Liberman, Asia Matatyaho Ya’akobi, Yeshayahu Talmon, Benji Maruyama, Gareth H. McKinley, A. John Hart, and Matteo Pasquali. Versatile acid solvents for pristine carbon nanotube assembly. Science Advances, Apr 2022. URL: https://doi.org/10.1126/sciadv.abm3285, doi:10.1126/sciadv.abm3285. This article has 40 citations and is from a highest quality peer-reviewed journal.

2. (arnold20252040visionstudy pages 13-17): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

3. (arnold20252040visionstudy pages 9-13): SM Arnold. 2040 vision study: nasa's t3 implementation activities. Unknown journal, 2025.

4. (vickers2022nasaadvisorycounciltechnology pages 13-19): J Vickers. Nasa advisory council-technology, innovation, and engineering committee-advanced manufacturing. Unknown journal, 2022.

5. (prisacariu2026additivemanufacturingin pages 4-6): Emilia Georgiana Prisăcariu, Oana Dumitrescu, and Raluca Andreea Roșu. Additive manufacturing in space: technologies, flight heritage, and materials. Technologies, 14:165, Mar 2227. URL: https://doi.org/10.3390/technologies14030165, doi:10.3390/technologies14030165. This article has 1 citations.

6. (deneault2021towardautonomousadditive pages 9-10): James R. Deneault, Jorge Chang, Jay Myung, Daylond Hooper, Andrew Armstrong, Mark Pitt, and Benji Maruyama. Toward autonomous additive manufacturing: bayesian optimization on a 3d printer. MRS Bulletin, 46:566-575, Apr 2021. URL: https://doi.org/10.1557/s43577-021-00051-1, doi:10.1557/s43577-021-00051-1. This article has 184 citations and is from a domain leading peer-reviewed journal.
