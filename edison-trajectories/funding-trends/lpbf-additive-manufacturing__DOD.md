# Funding trends: lpbf additive manufacturing — DOD

*Edison `LITERATURE` task `ec5fea45-acb9-4074-9346-86db579fbd79` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
laser powder bed fusion of metals to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: laser powder bed fusion (LPBF / L-PBF / SLM) additive manufacturing of metallic alloys including process-structure-property relationships, in-situ sensing, qualification, and process parameter optimization

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


## Executive summary (DOD/DOW posture in LPBF metals, 2020–2026)
Across the 2020–2026 U.S. literature corpus examined here, Department of Defense funding acknowledgements for LPBF metals concentrate in (i) **ONR awards** supporting **in-situ monitoring/NDE and process–quality linkages** and (ii) **AFOSR awards** supporting **autonomy/AI-driven process optimization**, including **AFOSR YIP**. (bevans2025inprocessmonitoringof pages 53-54, mcneil2020insitumonitoringfor pages 16-17, deneault2021towardautonomousadditive pages 9-10, brettmann2025challengesandopportunities pages 9-9)
Evidence of **Army activity** appears both in **applied transition mechanisms** (ARO **STTR Phase II**, with a stated ~$1.0M total contract amount and explicit 2019–2021 period of performance) and, more recently, in **basic research scale-up** via an **ARO MURI (FY25 award)** explicitly tied to LPBF superalloy solidification. (nuechterlein2021additivemanufacturingfeedstock pages 9-11, nuechterlein2021additivemanufacturingfeedstock pages 1-3, lamb2026cellularsolidificationstructure pages 13-15)
In this extracted set, **Navy contracting** (NAVAIR/NSWC) also appears alongside ONR in the same LPBF monitoring program area, indicating interest in qualification-relevant sensing/assessment deliverables. (bevans2025inprocessmonitoringof pages 53-54)
Notably, within this limited literature-derived acknowledgement sample, **DARPA program award numbers (e.g., AMD/Make-It/Open Manufacturing) and DoD-wide fellowships (NDSEG/Vannevar Bush) are not visible**, suggesting either under-capture by the current paper set or that those mechanisms are less frequently cited in LPBF-metal PSP/sensing papers’ acknowledgements. (spadaccia2025laserpowderbed pages 1-5)

## DoD-funded projects identified from acknowledgements (one row per project)
| PI(s) & institution | DoD agency & program | Award number(s) | Award amount | Project title / short description | Period of performance / start year | Papers acknowledging |
|---|---|---|---|---|---|---|
| J. Nuechterlein / Sinter Print, Inc. d.b.a. Elementum 3D, Inc. | Army Research Office (ARO) STTR Phase II | W911NF-20-C-0012 | $999,983.18 | **Design of Easy-to-Use Structural Alloy Feedstocks for Additive Manufacturing**. Final report on AM feedstock designed for uniform printing of metallic builds; ARO-enabled Phase II STTR effort on structural alloy feedstocks for AM. (nuechterlein2021additivemanufacturingfeedstock pages 9-11, nuechterlein2021additivemanufacturingfeedstock pages 1-3, nuechterlein2021additivemanufacturingfeedstock pages 3-9) | 21-Nov-2019 to 22-Nov-2021 | `nuechterlein2021additivemanufacturingfeedstock` |
| Blair K. Brettmann / institution not stated | Office of Naval Research (ONR) | N000142212031 | not stated | ONR-supported research acknowledged in a 2025 advanced manufacturing paper; exact LPBF-metal project title not stated in the acknowledgement excerpt. (brettmann2025challengesandopportunities pages 9-9) | not stated | `brettmann2025challengesandopportunities` |
| Joseph Kalman / institution not stated | Office of Naval Research (ONR) | N000142412353 | not stated | ONR-supported research acknowledged in a 2025 advanced manufacturing paper; exact LPBF-metal project title not stated in the acknowledgement excerpt. (brettmann2025challengesandopportunities pages 9-9) | not stated | `brettmann2025challengesandopportunities` |
| Monique S. McClain / institution not stated | Army Research Office (ARO) Cooperative Agreement | W911NF-22-2-0170 | not stated | ARO cooperative-agreement support acknowledged in a 2025 advanced manufacturing paper; exact project title not stated in the acknowledgement excerpt. (brettmann2025challengesandopportunities pages 9-9) | not stated | `brettmann2025challengesandopportunities` |
| Monique S. McClain / institution not stated | Air Force Office of Scientific Research (AFOSR) Young Investigator Program (YIP) | FA9550-23-1-0292 | not stated | AFOSR YIP-supported research acknowledged in a 2025 advanced manufacturing paper; exact project title not stated in the acknowledgement excerpt. (brettmann2025challengesandopportunities pages 9-9) | not stated | `brettmann2025challengesandopportunities` |
| James R. Deneault, Benji Maruyama et al. / Air Force Research Laboratory and The Ohio State University | Air Force Office of Scientific Research (AFOSR) | FA9550-16-1-0053 | not stated | Support for autonomous additive manufacturing / Bayesian optimization on a 3D printer; a closed-loop AM research robot framework relevant to autonomous process optimization. (deneault2021towardautonomousadditive pages 9-10) | not stated | `deneault2021towardautonomousadditive` |
| James R. Deneault, Benji Maruyama et al. / Air Force Research Laboratory and The Ohio State University | Air Force Office of Scientific Research (AFOSR) | 19RHCOR089 | not stated | Support for autonomous additive manufacturing / Bayesian optimization on a 3D printer; exact program title not stated beyond AFOSR grant support. (deneault2021towardautonomousadditive pages 9-10) | not stated | `deneault2021towardautonomousadditive` |
| S. S. Babu / institution not stated | Office of Naval Research (ONR) | N00014-18-1-2794 | not stated | Partial support for in-situ monitoring for defect identification in nickel-alloy complex geometries fabricated by L-PBF. (mcneil2020insitumonitoringfor pages 16-17) | not stated | `mcneil2020insitumonitoringfor` |
| Prahalada Rao / institution not stated | Office of Naval Research (ONR) | N00014-21-1-2781 | not stated | ONR-funded assessment of part quality as a function of processing parameters and microstructures in LPBF; acknowledged in acoustic-emission-based in-process monitoring and in a related LPBF process-control thesis. (bevans2025inprocessmonitoringof pages 53-54, spadaccia2025laserpowderbed pages 1-5) | not stated | `bevans2025inprocessmonitoringof`; `spadaccia2025laserpowderbed` |
| Prahalada Rao / institution not stated | U.S. Department of Navy / Naval Surface Warfare Center (NAVAIR/NSWC as stated in evidence) | N6833524C0215 | not stated | Navy-supported LPBF part-quality / monitoring research acknowledged as part of Rao’s research program in a 2025 acoustic-emission monitoring paper. (bevans2025inprocessmonitoringof pages 53-54) | not stated | `bevans2025inprocessmonitoringof` |
| D. P. Spadaccia / institution not stated | DoD National Defense Education Program (NDEP) | HQ0034231004 | not stated | NDEP support acknowledged in a 2025 LPBF thesis on layerwise process control and part quality for a complex aerospace component. (spadaccia2025laserpowderbed pages 1-5) | not stated | `spadaccia2025laserpowderbed` |
| Tresa M. Pollock et al. / institution not stated | Army Research Office (ARO) MURI | W911NF-25-2-0164 | not stated | ARO MURI support acknowledged in a 2026 paper on cellular solidification structure in laser powder bed manufacturing of superalloys. (lamb2026cellularsolidificationstructure pages 13-15) | start year implied 2025 by award number; otherwise not stated | `lamb2026cellularsolidificationstructure` |


*Table: This table de-duplicates Department of Defense-funded LPBF/metal additive manufacturing projects identifiable from acknowledgement sections in the retrieved 2020–2026 literature. It captures award numbers, inferred investigators/institutions, any explicitly stated amounts or periods, short project descriptions, and the papers that acknowledged each award.*

## Trends (from the extracted acknowledgements only)
### 1) Sub-programs appearing to grow vs. shrink in LPBF metals
* **Growing/active signals (in this corpus):**
  * **ARO MURI** presence in a 2026 LPBF-superalloy solidification paper (award **W911NF-25-2-0164**) suggests recent (FY25) scaling of Army basic research investments into LPBF microstructure/solidification science. (lamb2026cellularsolidificationstructure pages 13-15)
  * **AFOSR YIP** appears (award **FA9550-23-1-0292**), consistent with continued on-ramping of early-career PIs into manufacturing/materials-adjacent topics (though the paper is not LPBF-focused, it still explicitly cites AFOSR YIP). (brettmann2025challengesandopportunities pages 9-9)
  * **ONR** repeatedly appears with multiple awards spanning 2018–2024-era numbers, and in LPBF monitoring/NDE and quality-assessment contexts (e.g., **N00014-18-1-2794**, **N00014-21-1-2781**). (mcneil2020insitumonitoringfor pages 16-17, bevans2025inprocessmonitoringof pages 53-54)
* **Not observable here (cannot infer shrinkage, only lack of evidence in sample):**
  * No explicit **DARPA** award numbers tied to LPBF metals were captured in the mined acknowledgements, so growth/shrinkage of DARPA sub-programs cannot be assessed from this dataset. 

### 2) Institutions and PIs dominating (visibility within this sample)
* **Process monitoring / sensing / qualification thread:** Prahalada Rao’s program is repeatedly associated with **ONR N00014-21-1-2781** and also a **Navy/NAVAIR/NSWC award N6833524C0215**, with the paper explicitly stating that the ONR award funded assessment of part quality vs. processing parameters/microstructures and supported a PhD dissertation. (bevans2025inprocessmonitoringof pages 53-54)
* **In-situ defect identification in nickel alloys:** S. S. Babu is associated with **ONR N00014-18-1-2794** in an LPBF in-situ monitoring paper. (mcneil2020insitumonitoringfor pages 16-17)
* **Autonomy/closed-loop optimization:** Deneault/Maruyama et al. cite **AFOSR FA9550-16-1-0053** and **19RHCOR089** for autonomous AM / Bayesian optimization. (deneault2021towardautonomousadditive pages 9-10)
* **Applied feedstock development:** The ARO **STTR Phase II** contract (**W911NF-20-C-0012**) is tied to Elementum 3D/Sinter Print and includes explicit PoP and total amount (~$1.0M). (nuechterlein2021additivemanufacturingfeedstock pages 9-11, nuechterlein2021additivemanufacturingfeedstock pages 1-3)

### 3) New programs (launched 2022+) observed funding this topic
* **AFOSR Young Investigator Program (YIP)** award **FA9550-23-1-0292** is explicitly acknowledged (2023 award year implied by number). (brettmann2025challengesandopportunities pages 9-9)
* **ARO MURI** award **W911NF-25-2-0164** is explicitly acknowledged in a 2026 LPBF-superalloy paper (FY25 start implied by award number). (lamb2026cellularsolidificationstructure pages 13-15)
* **NDEP** support (DoD education pipeline) is acknowledged as **HQ0034231004** in an LPBF process-control dissertation document. (spadaccia2025laserpowderbed pages 1-5)

### 4) Gaps/opportunities suggested by what is *not* visible in acknowledgements
* **DARPA LPBF metals award visibility gap:** despite multiple LPBF papers in the retrieved corpus, no DARPA award numbers were captured in mined acknowledgements; if DARPA is a target sponsor for autonomous closed-loop alloy discovery, additional targeted literature harvesting (e.g., specific program performer lists and their publications) may be needed beyond general scholar queries. 
* **DoD-wide fellowships gap:** within this sample, explicit acknowledgements of **NDSEG** or **Vannevar Bush Faculty Fellowship** did not appear; these mechanisms may still fund relevant PIs but may be less consistently acknowledged in journal articles than agency grants/contracts, or the relevant papers were not retrieved.
* **AFRL/ARL/NRL award-number gap:** one paper acknowledges AFRL (Aerospace Systems Directorate) support without an award number; more targeted retrieval of AFRL/ARL/NRL performer publications may be required to map those funding streams precisely. (brettmann2025challengesandopportunities pages 9-9)


References

1. (bevans2025inprocessmonitoringof pages 53-54): Benjamin Bevans, Alexander Riensche, Antonio Carrington, Kaustubh Deshmukh, Mihir Darji, Yuri Plotnikov, John Sions, Kyle Snyder, Derek Hass, and Prahalada Rao. In-process monitoring of part quality in laser powder bed fusion additive manufacturing process using acoustic emission sensors. Journal of Manufacturing Science and Engineering, pages 1-48, Feb 2025. URL: https://doi.org/10.1115/1.4067848, doi:10.1115/1.4067848. This article has 5 citations.

2. (mcneil2020insitumonitoringfor pages 16-17): J. Logan McNeil, Kevin Sisco, Curt Frederick, Michael Massey, Keith Carver, Fred List, Caian Qiu, Morgan Mader, Suresh Sundarraj, and S. S. Babu. In-situ monitoring for defect identification in nickel alloy complex geometries fabricated by l-pbf additive manufacturing. Metallurgical and Materials Transactions A, 51:6528-6545, Oct 2020. URL: https://doi.org/10.1007/s11661-020-06036-0, doi:10.1007/s11661-020-06036-0. This article has 43 citations.

3. (deneault2021towardautonomousadditive pages 9-10): James R. Deneault, Jorge Chang, Jay Myung, Daylond Hooper, Andrew Armstrong, Mark Pitt, and Benji Maruyama. Toward autonomous additive manufacturing: bayesian optimization on a 3d printer. MRS Bulletin, 46:566-575, Apr 2021. URL: https://doi.org/10.1557/s43577-021-00051-1, doi:10.1557/s43577-021-00051-1. This article has 184 citations and is from a domain leading peer-reviewed journal.

4. (brettmann2025challengesandopportunities pages 9-9): Blair K. Brettmann, Joseph Kalman, Jena M. McCollum, Levi M. J. Moore, Alice M. Savage, and Monique S. McClain. Challenges and opportunities in manufacturing highly filled polymers. npj Advanced Manufacturing, Jul 2025. URL: https://doi.org/10.1038/s44334-025-00046-9, doi:10.1038/s44334-025-00046-9. This article has 6 citations.

5. (nuechterlein2021additivemanufacturingfeedstock pages 9-11): J Nuechterlein. Additive manufacturing feedstock designed for uniform printing of metallic builds. Unknown journal, 2021.

6. (nuechterlein2021additivemanufacturingfeedstock pages 1-3): J Nuechterlein. Additive manufacturing feedstock designed for uniform printing of metallic builds. Unknown journal, 2021.

7. (lamb2026cellularsolidificationstructure pages 13-15): James D. Lamb, Evan B. Raeker, Haydn Schroader, Nicolò M. della Ventura, McLean P. Echlin, Daniel S. Gianola, and Tresa M. Pollock. Cellular solidification structure in laser powder bed manufacturing of superalloys. Metallurgical and Materials Transactions A, 57:2430-2446, Jan 2026. URL: https://doi.org/10.1007/s11661-026-08110-5, doi:10.1007/s11661-026-08110-5. This article has 0 citations.

8. (spadaccia2025laserpowderbed pages 1-5): DP Spadaccia. Laser powder bed fusion (lpbf) of a complex aerospace component: effects of layerwise process control on part quality. Unknown journal, 2025.

9. (nuechterlein2021additivemanufacturingfeedstock pages 3-9): J Nuechterlein. Additive manufacturing feedstock designed for uniform printing of metallic builds. Unknown journal, 2021.
