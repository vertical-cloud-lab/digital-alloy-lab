# Funding trends: aluminum alloys — DOD

*Edison `LITERATURE` task `b869fbf7-5d80-4b5a-bcc3-666501a5e89d` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
aluminum alloy development to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: aluminum alloy development for high-performance applications (high-strength Al, Al-Cu, Al-Mg-Sc, Al-Ce, Al-RE, additively manufactured aluminum alloys, lightweight Al for transportation/aerospace/defense)

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


# Executive summary (DOD/DOW posture, 2020–2026 literature acknowledgements)
Across 2020–2026 aluminum-alloy and Al-alloy additive-manufacturing (AM) papers with explicit acknowledgements, DOD funding appears concentrated in ONR core research awards enabling printable high-strength Al alloy design and microstructure/property characterization, complemented by DEVCOM ARL/ARO awards supporting Army-relevant Al feedstock/process development and mechanics mapping. (thapliyal2021designofheterogeneous pages 8-9, thapliyal2020anintegratedcomputational pages 6-6, dhal2022multiscalehierarchicaland pages 7-8, anne2023laserpowderbedfusion pages 7-11)
Post-2022 acknowledgements show increased DOD emphasis on AM process autonomy, digital twins, and defect mitigation via AFOSR and NAVAIR contracts, suggesting a shift toward qualification-ready, closed-loop AM process control in addition to alloy chemistry development. (liu2024deepneuraloperator pages 24-26)
DARPA support in the extracted sample is directed at durability/reliability gaps (stress corrosion cracking in AM Al alloys), aligning with defense needs for certifiable structural performance. (raghavan2023quantifyingstresscorrosion pages 9-11)
Instrument-focused investments (ONR-DURIP) remain visible and materially enable advanced microscopy/atom-probe characterization that underpins modern alloy development and AM process science. (anne2023laserpowderbedfusion pages 7-11, shang2024additivemanufacturingof media e3fa57bd)

> Note: Award amounts and formal project titles are generally not stated in paper acknowledgements; entries below report only what is explicitly acknowledged or safely inferable from the cited text.

# DOD-funded projects acknowledged in recent Al-alloy literature
| Agency | Sub-program | Award number(s) | PI(s) and institution | Award amount | Project title/short description | Year started/period | Paper(s) acknowledging | Evidence citation IDs |
|---|---|---|---|---|---|---|---|---|
| ONR | research award | N00014-17-1-2559 | Rajiv S. Mishra and collaborators, University of North Texas (inferred from author list and UNT facility acknowledgement) | not stated | Supported ICME-guided design and LPBF processing of novel aluminum alloys, including a closed-loop design workflow for an age-hardenable Al-Cu-Sc-Zr alloy and a heterogeneous-structured Al-Ni-Ti-Zr alloy with improved printability. The same ONR award is acknowledged across two UNT/Mishra-group papers, indicating a sustained ONR investment in printable high-strength Al alloy design. | 2017 start year inferable from award number | thapliyal2020anintegratedcomputational; thapliyal2021designofheterogeneous | (thapliyal2021designofheterogeneous pages 8-9, thapliyal2020anintegratedcomputational pages 6-6) |
| DEVCOM Army Research Laboratory | research grant | W911NF-18-2-0067 | Rajiv S. Mishra, University of North Texas (inferred; corresponding author and funding acquisition), with alloy-development input from Yongho Sohn group | not stated | Supported characterization of a novel additively manufactured Al alloy using high-resolution nanoindentation mapping, linking hierarchical LPBF microstructures to local mechanical response. The project is clearly aligned with Army interest in process-structure-property mapping for deployable Al AM alloys. | 2018 start year inferable from award number | dhal2022multiscalehierarchicaland | (dhal2022multiscalehierarchicaland pages 7-8) |
| U.S. Army Research Laboratory | research grant | W911NF-15-2-0024 | Danielle Cote and Victor Champagne, Northeastern University / ARL-linked collaboration (funding acquisition explicitly attributed to D.C. and V.C.) | not stated | Funded characterization of thermally treated gas-atomized Al 5056 powder for additive manufacturing/cold-spray-relevant applications. The work focused on phase stability and powder microstructure needed to qualify lightweight Al feedstocks for defense manufacturing workflows. | 2015 start year inferable from award number | tsaknopoulos2020characterizationofthermally | (tsaknopoulos2020characterizationofthermally pages 9-11) |
| Army Research Office | research award | W911NF-18-1-0129 | Jennifer Anne Glerum / Dunand lab, Northwestern University (inferred from dissertation acknowledgements and lab/facility context) | not stated | Supported laser powder-bed fusion of elemental powder blends to produce precipitation- and oxide-dispersion-strengthened aluminum alloys. The project targeted alloy development routes beyond conventional castable Al-Si systems by using blended powders and advanced characterization. | 2018 start year inferable from award number | anne2023laserpowderbedfusion | (anne2023laserpowderbedfusion pages 7-11) |
| DEVCOM Army Research Laboratory | research award | W911NF-19-2-0092 | Jennifer Anne Glerum / Dunand lab, Northwestern University (inferred) | not stated | Supported the same Northwestern dissertation program on LPBF of elemental powder blends for precipitation- and oxide-dispersion-strengthened aluminum alloys. The acknowledgment suggests DEVCOM ARL co-funded alloy/process development and characterization alongside ARO support. | 2019 start year inferable from award number | anne2023laserpowderbedfusion | (anne2023laserpowderbedfusion pages 7-11) |
| DARPA | agreement/contract | HR00112020043 | not stated | not stated | Supported work quantifying stress-corrosion-cracking behavior of additively manufactured aluminum alloys using micro digital image correlation. The project addresses reliability/performance of AM Al alloys under environmentally assisted cracking, a defense-relevant durability gap. | 2020 start year inferable from award number | raghavan2023quantifyingstresscorrosion | (raghavan2023quantifyingstresscorrosion pages 9-11) |
| AFOSR | research grant | FA9550-22-1-0197 | Yue Yu (explicitly acknowledged), institution not stated in evidence excerpt | not stated | Supported digital-twin and deep neural operator modeling for additive manufacturing, including closed-loop prediction/control of melt-pool behavior and defects. The paper is process-focused rather than Al-specific, but it is directly relevant to autonomous AM alloy development workflows. | 2022 start year inferable from award number | liu2024deepneuraloperator | (liu2024deepneuraloperator pages 24-26) |
| NAVAIR | funding contract | N68335-23-C-0440 | not stated | not stated | Supported digital-twin modeling for additive manufacturing under a U.S. Naval Air Systems Command contract. The work targets closed-loop AM process control and defect mitigation, relevant to qualification of high-performance aluminum alloy AM for aerospace and naval aviation applications. | 2023 start year inferable from award number | liu2024deepneuraloperator | (liu2024deepneuraloperator pages 24-26) |
| ONR | DURIP | N00014-17-1-2921 | Haiyan Wang (H.W. indicated), institution not stated in evidence excerpt | not stated | DURIP instrumentation support for the ASTAR crystal orientation system used in TEM-based characterization in a 2024 paper on an ultrastrong, deformable additively manufactured Al alloy with nanoscale intermetallics. This is a facility/instrumentation award rather than a direct alloy R&D grant, but it materially enabled the reported aluminum-alloy study. | 2017 start year inferable from award number | shang2024additivemanufacturingof | (shang2024additivemanufacturingof pages 12-12, shang2024additivemanufacturingof media e3fa57bd) |
| ONR | contract/research support | N00014-22-1-2160 | Haiyan Wang (H.W. indicated), institution not stated in evidence excerpt | not stated | ONR contract support for TEM work used in characterization of an additively manufactured ultrastrong Al alloy containing nanoscale intermetallic lamellae. The funding appears tied to microscopy capability directly supporting alloy-development insights. | 2022 start year inferable from award number | shang2024additivemanufacturingof | (shang2024additivemanufacturingof pages 12-12, shang2024additivemanufacturingof media e3fa57bd) |
| ONR | DURIP instrumentation/facility support | N00014-0400798; N00014-0610539; N00014-0910781; N00014-1712870 | not stated; Northwestern University NUCAPT facility / LEAP tomograph context given in dissertation | not stated | Aggregated ONR-DURIP awards cited as funding used to purchase/upgrade the LEAP tomograph at Northwestern's NUCAPT facility, which enabled advanced atom-probe characterization in the aluminum-alloy LPBF dissertation. These are infrastructure awards rather than direct project grants, but they are explicitly acknowledged in connection with the reported Al alloy research. | 2004, 2006, 2009, and likely 2017 starts inferable from award numbers | anne2023laserpowderbedfusion | (anne2023laserpowderbedfusion pages 7-11) |


*Table: This table normalizes the distinct DOD-funded projects and instrumentation awards identified from recent aluminum-alloy literature acknowledgements. It deduplicates repeated awards and captures only award numbers, PI/institution clues, and project descriptions that were directly supported by the extracted evidence.*

# Trends (from the extracted acknowledgement set)
## Sub-programs growing vs. shrinking (as visible in this literature-only sample)
- **Growing/most visible (2022–2024 starts):** AM autonomy / digital-twin / closed-loop process control, evidenced by AFOSR grant **FA9550-22-1-0197** and NAVAIR contract **N68335-23-C-0440** appearing in AM digital-twin work. (liu2024deepneuraloperator pages 24-26)
- **Sustained:** ONR **core research** support for Al alloy design for LPBF, with ONR award **N00014-17-1-2559** acknowledged across multiple Al-alloy AM design papers (suggesting a sustained research line rather than a one-off). (thapliyal2021designofheterogeneous pages 8-9, thapliyal2020anintegratedcomputational pages 6-6)
- **Sustained infrastructure:** ONR **DURIP** instrumentation awards (multiple N00014 DURIP numbers for APT upgrades; TEM orientation system support), consistent with continued capital investment in characterization capacity that enables alloy discovery/qualification. (anne2023laserpowderbedfusion pages 7-11, shang2024additivemanufacturingof media e3fa57bd)
- **Not assessable from this sample:** evidence for “shrinking” programs is not directly inferable from acknowledgements alone; absence in a small corpus is not evidence of decline.

## Dominant institutions and PI clusters (in the extracted corpus)
- **University of North Texas (UNT) / Rajiv S. Mishra ecosystem:** appears repeatedly in ONR- and DEVCOM ARL-acknowledged Al-alloy AM design and nanoindentation-based property mapping, with shared award **N00014-17-1-2559** across two papers and ARL award **W911NF-18-2-0067** in a related paper. (thapliyal2021designofheterogeneous pages 8-9, thapliyal2020anintegratedcomputational pages 6-6, dhal2022multiscalehierarchicaland pages 7-8)
- **Northwestern University / Dunand lab + NUCAPT characterization ecosystem:** ARO **W911NF-18-1-0129** and DEVCOM ARL **W911NF-19-2-0092** are acknowledged in a dissertation focused on LPBF of elemental powder blends for advanced Al alloys; multiple ONR-DURIP awards are also tied to the APT (LEAP) infrastructure used. (anne2023laserpowderbedfusion pages 7-11)
- **Microscopy-instrumentation PI signal:** the ONR contract **N00014-22-1-2160** and ONR-DURIP **N00014-17-1-2921** are acknowledged by “H.W.” in a Nature Communications AM Al alloy paper, indicating ONR support for characterization capability directly used in Al-alloy AM work. (shang2024additivemanufacturingof pages 12-12, shang2024additivemanufacturingof media e3fa57bd)

## New (launched 2022+) DOD programs/funding mechanisms appearing in this sample
- **ONR contract N00014-22-1-2160** (2022 start inferable from award number) supporting TEM characterization for AM Al alloy work. (shang2024additivemanufacturingof pages 12-12, shang2024additivemanufacturingof media e3fa57bd)
- **AFOSR FA9550-22-1-0197** (2022 start) supporting AM digital-twin modeling/closed-loop control methods relevant to autonomous AM and alloy discovery workflows. (liu2024deepneuraloperator pages 24-26)
- **NAVAIR N68335-23-C-0440** (2023 start) supporting AM digital twin/defect mitigation—indicating a service acquisition/qualification pathway for AM process control. (liu2024deepneuraloperator pages 24-26)

## Visible gaps / opportunities (where DOD is not clearly visible in this sample)
- **Limited explicit presence of AFRL/NRL and DOD-wide fellowships** (NDSEG, Vannevar Bush, YIP, MURI) in the extracted Al-alloy-development acknowledgements; this may reflect under-sampling, but it also suggests an opportunity to more explicitly tie **autonomous closed-loop alloy discovery** to defense priorities (e.g., accelerated qualification of high-strength AM Al alloys for platforms). (thapliyal2021designofheterogeneous pages 8-9, anne2023laserpowderbedfusion pages 7-11, liu2024deepneuraloperator pages 24-26)
- **Chemistry space gaps:** within this literature-only sample, most explicit DOD-funded alloy-development work centers on **printable high-strength Al alloys** and feedstock/process studies, with less direct visibility on **Al-Ce / Al-rare-earth** alloy development funding, despite its relevance to casting/temperature capability; targeted solicitations could connect RE-containing Al alloys to defense sustainment and supply-chain resilience.



References

1. (thapliyal2021designofheterogeneous pages 8-9): Saket Thapliyal, Shivakant Shukla, Le Zhou, Holden Hyer, Priyanshi Agrawal, Priyanka Agrawal, Mageshwari Komarasamy, Yongho Sohn, and Rajiv S. Mishra. Design of heterogeneous structured al alloys with wide processing window for laser-powder bed fusion additive manufacturing. Additive Manufacturing, 42:102002, Jun 2021. URL: https://doi.org/10.1016/j.addma.2021.102002, doi:10.1016/j.addma.2021.102002. This article has 109 citations and is from a highest quality peer-reviewed journal.

2. (thapliyal2020anintegratedcomputational pages 6-6): Saket Thapliyal, Mageshwari Komarasamy, Shivakant Shukla, Le Zhou, Holden Hyer, Sharon Park, Yongho Sohn, and Rajiv S. Mishra. An integrated computational materials engineering-anchored closed-loop method for design of aluminum alloys for additive manufacturing. Materialia, 9:100574, Mar 2020. URL: https://doi.org/10.1016/j.mtla.2019.100574, doi:10.1016/j.mtla.2019.100574. This article has 85 citations and is from a peer-reviewed journal.

3. (dhal2022multiscalehierarchicaland pages 7-8): Abhijeet Dhal, Saket Thapliyal, Supreeth Gaddam, Priyanka Agrawal, and Rajiv S. Mishra. Multiscale hierarchical and heterogeneous mechanical response of additively manufactured novel al alloy investigated by high-resolution nanoindentation mapping. Scientific Reports, Oct 2022. URL: https://doi.org/10.1038/s41598-022-23083-2, doi:10.1038/s41598-022-23083-2. This article has 28 citations and is from a peer-reviewed journal.

4. (anne2023laserpowderbedfusion pages 7-11): Jennifer Anne Glerum. Laser powder-bed fusion of elemental powder blends to manufacture precipitation and oxide-dispersion strengthened aluminum alloys. Text, 2023. URL: https://doi.org/10.21985/n2-k0nf-gm36, doi:10.21985/n2-k0nf-gm36. This article has 0 citations and is from a peer-reviewed journal.

5. (liu2024deepneuraloperator pages 24-26): Ning Liu, Xuxiao Li, Manoj R. Rajanna, Edward W. Reutzel, Brady Sawyer, Prahalada Rao, Jim Lua, Nam Phan, and Yue Yu. Deep neural operator enabled digital twin modeling for additive manufacturing. ArXiv, May 2024. URL: https://doi.org/10.48550/arxiv.2405.09572, doi:10.48550/arxiv.2405.09572. This article has 34 citations.

6. (raghavan2023quantifyingstresscorrosion pages 9-11): Seetha Raghavan, Remelisa Esteves, and Ranajay Ghosh. Quantifying stress corrosion cracking performance of additively manufactured aluminum alloys via micro digital image correlation. Dec 2023. URL: https://doi.org/10.21203/rs.3.rs-3798144/v1, doi:10.21203/rs.3.rs-3798144/v1.

7. (shang2024additivemanufacturingof media e3fa57bd): Anyu Shang, Benjamin Stegman, Kenyi Choy, Tongjun Niu, Chao Shen, Zhongxia Shang, Xuanyu Sheng, Jack Lopez, Luke Hoppenrath, Bohua Peter Zhang, Haiyan Wang, Pascal Bellon, and Xinghang Zhang. Additive manufacturing of an ultrastrong, deformable al alloy with nanoscale intermetallics. Nature Communications, Jun 2024. URL: https://doi.org/10.1038/s41467-024-48693-4, doi:10.1038/s41467-024-48693-4. This article has 63 citations and is from a highest quality peer-reviewed journal.

8. (tsaknopoulos2020characterizationofthermally pages 9-11): Kyle Tsaknopoulos, Caitlin Walde, Derek Tsaknopoulos, Victor Champagne, and Danielle Cote. Characterization of thermally treated gas-atomized al 5056 powder. Materials, 13:4051, Sep 2020. URL: https://doi.org/10.3390/ma13184051, doi:10.3390/ma13184051. This article has 15 citations.

9. (shang2024additivemanufacturingof pages 12-12): Anyu Shang, Benjamin Stegman, Kenyi Choy, Tongjun Niu, Chao Shen, Zhongxia Shang, Xuanyu Sheng, Jack Lopez, Luke Hoppenrath, Bohua Peter Zhang, Haiyan Wang, Pascal Bellon, and Xinghang Zhang. Additive manufacturing of an ultrastrong, deformable al alloy with nanoscale intermetallics. Nature Communications, Jun 2024. URL: https://doi.org/10.1038/s41467-024-48693-4, doi:10.1038/s41467-024-48693-4. This article has 63 citations and is from a highest quality peer-reviewed journal.
