<!--
Edison Scientific PRECEDENT task (batch 3)
- Task ID: 50f607e6-b432-411f-9c7b-f993baf9061c
- Submitted: 2026-10-17T05:46:10Z
- Fetched: 2026-10-17T06:17:01Z (status: success)
- Raw trajectory JSON: ../raw/b3-09-precedent-ni-bearing-repair.json.gz
- Synthesis: ../README.md
-->

Question:

Has anyone deposited a nickel-bearing nickel-aluminum bronze powder or a
10-30 wt% Ni copper-nickel powder by blown-powder laser directed energy
deposition or laser cladding onto CAST nickel-aluminum bronze or onto
WROUGHT copper-nickel as a repair, and measured cracking, dilution, the
heat-affected zone, or corrosion of the fusion zone and heat-affected zone?
Known near misses: Yao & Shim 2022 (CuNi2SiCr powder on NAB, low Ni), Hyatt
et al. 1998 (laser cladding NAB on NAB with a consumable), Bhattacharya et
al. 2011 (Cu-30Ni direct metal deposition on C71500), and the 2019 Springer
chapter "Laser-Additive Repair of Cast Ni-Al-Bronze Components". Give DOIs,
what each tested, and what remains undone. Exclude publications by Sterling
G. Baird.

---

Question: Has anyone deposited a nickel-bearing nickel-aluminum bronze powder or a
10-30 wt% Ni copper-nickel powder by blown-powder laser directed energy
deposition or laser cladding onto CAST nickel-aluminum bronze or onto
WROUGHT copper-nickel as a repair, and measured cracking, dilution, the
heat-affected zone, or corrosion of the fusion zone and heat-affected zone?
Known near misses: Yao & Shim 2022 (CuNi2SiCr powder on NAB, low Ni), Hyatt
et al. 1998 (laser cladding NAB on NAB with a consumable), Bhattacharya et
al. 2011 (Cu-30Ni direct metal deposition on C71500), and the 2019 Springer
chapter "Laser-Additive Repair of Cast Ni-Al-Bronze Components". Give DOIs,
what each tested, and what remains undone. Exclude publications by Sterling
G. Baird.


No. ## Finding

**There is a partial match, but I could not verify a study that completes the full repair-and-interface assessment.** Pi et al. (2025) deposited matching, gas-atomized powder onto *cast* aluminum bronze and measured a heat-affected zone (HAZ) and corrosion of the clad relative to the casting. Its alloy, however, is strongly manganese-bearing (13.16 wt% Mn) and contains only 2.11 wt% Ni; it is not a conventional ∼4–5 wt% Ni nickel–aluminum bronze (NAB). Its corrosion comparison does not separately test the fusion boundary and HAZ. On the wrought Cu–Ni side, Bhattacharya et al. (2011) is the closest process-and-material match, but the accessible evidence does not establish zone-resolved interface testing. Thus, the answer is **yes for parts of the proposed experiment, but no verified publication meeting its full scope**. (ziqiang2025lasercladdingremanufacturing pages 3-6, ziqiang2025lasercladdingremanufacturing pages 1-3, riza2024mechanicalcharacterisationof pages 51-55, kuprienko2025analysisofnickel pages 36-41)

| Study and DOI | Feedstock / substrate | Measurements reported | Fit to the exact prompt |
|---|---|---|---|
| **Yao & Shim (2022)** — [10.1016/j.jallcom.2022.165776](https://doi.org/10.1016/j.jallcom.2022.165776) | Blown CuNi2SiCr powder on NAB; Ni content is only about 2 wt%; substrate’s cast/wrought condition was not independently established. | Corrosion and deposited-layer characterization. | **Near miss:** correct laser-powder approach and NAB substrate, but neither nickel-bearing NAB powder nor 10–30 wt% Ni Cu–Ni powder; cast substrate status is unconfirmed. |
| **Hyatt, Magee & Betancourt (1998)** — [10.1007/s11661-998-0090-5](https://doi.org/10.1007/s11661-998-0090-5) | Cu–9.0Al–4.6Ni–3.9Fe–1.2Mn **wire consumable** laser-clad onto cast NAB; heat inputs of 42.5–595 J/mm. | Clad microstructure, hardness and heat-input effects; rapid cooling produced largely martensitic structures at low heat input, with increasing Widmanstätten α as heat input rose. (kuprienko2025analysisofnickel pages 50-55, kuprienko2025analysisofnickel pages 169-173) | **Near miss:** right alloy family and cast-NAB substrate, but wire rather than blown powder; no fusion-zone/HAZ corrosion program. |
| **Bhattacharya et al. (2011)** — [10.1016/j.jallcom.2011.03.091](https://doi.org/10.1016/j.jallcom.2011.03.091) | Cu–30Ni powder, CO₂-laser DMD, on **rolled C71500 plate**—a wrought Cu–Ni substrate. (riza2024mechanicalcharacterisationof pages 51-55) | Bulk deposited-alloy microstructure, mechanical properties and corrosion were evaluated. The primary paper was inaccessible here; separate corrosion measurements of the fusion boundary or HAZ should **not** be inferred. | **Closest Cu–Ni match:** satisfies powder composition, blown-powder DMD and wrought-substrate requirements, but does not establish zone-resolved cracking, dilution, HAZ or fusion-zone/HAZ corrosion assessment. |
| **Cao et al. (2019)** — [10.1007/978-3-030-05861-6_19](https://doi.org/10.1007/978-3-030-05861-6_19) | Cast Ni–Al–bronze repair; the inaccessible full chapter left feedstock form, composition and powder-feeding configuration independently unverified. | Reported as laser-additive repair of cast NAB; exact cracking, dilution, HAZ and corrosion-test coverage could not be verified from accessible evidence. | **Unresolved near miss:** title and substrate are directly relevant, but it cannot safely be counted as an exact blown-powder, composition and measurement match without the chapter’s methods and results. |
| **Pi et al. (2025)** — [10.1038/s41598-025-96674-4](https://doi.org/10.1038/s41598-025-96674-4) | Gas-atomized ZCuAl8Mn13Fe3Ni2 powder on matched **cast** alloy: 13.16 wt% Mn and only 2.11 wt% Ni—strongly Mn-bearing aluminum bronze rather than conventional 4–5 wt% Ni NAB. (ziqiang2025lasercladdingremanufacturing pages 1-3) | Approximately 100 µm HAZ; clad, HAZ and substrate grain sizes about 5–10, 20–35 and 200–400 µm. Compared clad-surface electrochemistry with cast alloy, not separate fusion-zone/HAZ corrosion. No quantitative dilution or crack assessment. Corrosion-current exponent is internally inconsistent: text/abstract gives about 3.73×10⁻², while the table/conclusion supports 3.73×10⁻³ mA/cm². (ziqiang2025lasercladdingremanufacturing pages 3-6, ziqiang2025lasercladdingremanufacturing pages 6-9) | **Partial match:** blown matching powder on cast bronze and a measured HAZ, but the powder is low-Ni/high-Mn and corrosion was not zone resolved. |
| **Zhao et al. (2022)** — [10.3390/met12050781](https://doi.org/10.3390/met12050781) | NAB powder (Cu–10.8Al–4.1Ni–4.0Fe) laser-deposited on **SUS630 stainless steel**, directly or over Ni/NiCr interlayers. (zhao2022thelaserdeposited pages 2-4) | Measured interface microstructure, dilution effects, tensile bonding, polarization/EIS and immersion corrosion. Direct deposition produced Fe-rich dendrites from substrate dilution; Ni-bearing interlayers isolated the NAB layer and improved corrosion behavior. (zhao2022thelaserdeposited pages 1-2, zhao2022thelaserdeposited media 2d66eb0f) | **Near miss:** demonstrates dilution–corrosion coupling with genuine NAB powder, but the substrate is steel—not cast NAB or wrought Cu–Ni—and corrosion was not a cast-NAB repair HAZ study. |


*Table: Comparison of the closest non-Baird studies against the required feedstock, substrate and zone-specific measurement criteria. It distinguishes exact process/material matches from studies addressing only part of the requested repair problem.*

**What the closest studies actually establish.** Pi et al., DOI **10.1038/s41598-025-96674-4**, used ZCuAl8Mn13Fe3Ni2 powder on a matching cast propeller alloy. They report an approximately **100 µm HAZ** and compare coating electrochemistry with the cast alloy, finding a higher corrosion current for the coating. They do not report separate corrosion results for the fusion boundary and HAZ, or a quantitative dilution or cracking assessment in the examined passages. Their reported corrosion-current exponent is inconsistent between parts of the article (10⁻² versus 10⁻³ mA/cm²); the relative increase of 18.68% is the less ambiguous comparison. (ziqiang2025lasercladdingremanufacturing pages 3-6, ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 6-9)

Bhattacharya et al., DOI **10.1016/j.jallcom.2011.03.091**, studied Cu–30Ni made by CO₂-laser direct metal deposition on **rolled C71500 plate**, alongside deposited-alloy microstructure, mechanical and corrosion properties. Rolled plate meets the wrought-substrate criterion. Because the primary article was not obtainable in this search, I cannot verify from its methods whether corrosion was measured specifically *across* the fusion zone or HAZ, or whether cracking and dilution were quantified; its title’s reference to corrosion must not be treated as proof of zone-specific tests. (riza2024mechanicalcharacterisationof pages 51-55)

The specified exclusions matter. Hyatt, Magee and Betancourt (1998), DOI **10.1007/s11661-998-0090-5**, varied heat input and examined the microstructure and hardness of NAB laser-clad onto cast NAB, but used a **consumable wire**, not blown powder. Yao and Shim’s CuNi2SiCr-on-NAB corrosion study (2022), DOI **10.1016/j.jallcom.2022.165776**, uses a low-Ni copper alloy rather than either stipulated powder composition. Cao, Wanjara, Gholipour and Wang’s chapter, *Laser-Additive Repair of Cast Ni–Al–Bronze Components* (2019), DOI **10.1007/978-3-030-05861-6_19**, is highly relevant by title, but its full text was unavailable here: its feedstock form and exact interface measurements should **not** be asserted without checking the chapter. The Yao and Cao DOIs were identifiable in publication records, but their experimental details could not be independently checked against primary text in this search. (kuprienko2025analysisofnickel pages 50-55, kuprienko2025analysisofnickel pages 169-173)

A useful wrong-substrate control is Zhao et al. (2022), DOI **10.3390/met12050781**: genuine NAB powder containing **4.1 wt% Ni** was laser-deposited onto **SUS630 stainless steel**. They assessed substrate dilution, microstructure and corrosion; direct deposition produced Fe-rich dendrites, whereas nickel-based interlayers separated the bronze from steel. Their interface micrographs illustrate why results on steel cannot substitute for results on a cast-NAB repair. (zhao2022thelaserdeposited pages 1-2, zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited media 2d66eb0f)

**Still undone—or at least not demonstrated by the verified evidence—is an integrated, blown-powder repair study** using conventional Ni-bearing NAB powder on a documented cast-NAB substrate, or 10–30 wt% Ni Cu–Ni powder on documented wrought Cu–Ni, that maps crack incidence, compositional/geometric dilution and HAZ structure **and** measures corrosion separately in the deposit, exposed fusion boundary and HAZ against parent metal. The absence claim is limited by the inaccessible primary papers, particularly the 2019 chapter and the detailed methods of Bhattacharya et al.; it is not proof that no such experiment exists. No publications by Sterling G. Baird were used. (ziqiang2025lasercladdingremanufacturing pages 3-6, ziqiang2025lasercladdingremanufacturing pages 6-9, riza2024mechanicalcharacterisationof pages 51-55, zhao2022thelaserdeposited pages 2-4)

References

1. (ziqiang2025lasercladdingremanufacturing pages 3-6): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

2. (ziqiang2025lasercladdingremanufacturing pages 1-3): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

3. (riza2024mechanicalcharacterisationof pages 51-55): Syed Riza. Mechanical characterisation of high strength alloys produced by laser assisted direct metal deposition. Text, Jan 2024. URL: https://doi.org/10.25916/sut.26293366, doi:10.25916/sut.26293366. This article has 1 citations and is from a peer-reviewed journal.

4. (kuprienko2025analysisofnickel pages 36-41): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

5. (kuprienko2025analysisofnickel pages 50-55): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

6. (kuprienko2025analysisofnickel pages 169-173): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

7. (ziqiang2025lasercladdingremanufacturing pages 6-9): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

8. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

9. (zhao2022thelaserdeposited pages 1-2): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

10. (zhao2022thelaserdeposited media 2d66eb0f): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.
