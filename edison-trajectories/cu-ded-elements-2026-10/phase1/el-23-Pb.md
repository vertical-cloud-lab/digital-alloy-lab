<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 9faf4e8e-468a-4f1e-94f9-250dd406393c
- Submitted: 2026-10-17T18:59:58Z
- Fetched: 2026-10-17T19:22:56Z (status: success)
- Raw trajectory JSON: ../raw/el-23-Pb.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

ELEMENT UNDER REVIEW: Pb (impurity / free-machining). Leaded bronzes and brasses; Cu-Ni specifications limit Pb to about 0.02-0.05 wt% for welding; hot cracking; toxic, restricted (RoHS).

Answer for Pb specifically, not for copper alloys in general:
1. ROLE: what Pb does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Pb ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Pb changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-Pb, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Pb, Cu-Ni-Pb and Cu-Al-Pb are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Pb in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that Pb neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Pb | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

ELEMENT UNDER REVIEW: Pb (impurity / free-machining). Leaded bronzes and brasses; Cu-Ni specifications limit Pb to about 0.02-0.05 wt% for welding; hot cracking; toxic, restricted (RoHS).

Answer for Pb specifically, not for copper alloys in general:
1. ROLE: what Pb does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Pb ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Pb changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-Pb, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Pb, Cu-Ni-Pb and Cu-Al-Pb are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Pb in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that Pb neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Pb | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


This document synthesizes traceable evidence for the treatment of lead (Pb) in copper-nickel and aluminum-bronze alloy powders and deposits for DED in seawater service, following the specified template and providing quantitative, source-cited limits and rationales:

1. ROLE: Pb is not a functional addition for corrosion or microstructure in marine Cu-Ni or Al-bronze alloys. In Cu-Sn-Pb bronzes (e.g., C83600, C93200, C84400) [CITE], Pb (e.g., 5 wt% in C83600 [NUMBERS]) forms a free, low-melting, lubricating phase, enhancing castability and machinability but not seawater corrosion performance. In marine service alloys (Cu-Ni, NAB/Al-bronze), Pb is universally treated as a detrimental impurity due to its tendency to segregate and embrittle grain boundaries [CITE], [NAVY].

2. SEAWATER CORROSION: No directly controlled study was found comparing Pb-free and low-Pb (<0.05 wt%) marine Cu alloys for corrosion in 3.5 wt% NaCl or ASTM D1141. Available evidence is qualitative: some studies find negligible effect of unspecified Pb ranges, others report high-Pb alloys have the poorest resistance. Pb is strongly associated with micro-galvanic corrosion, porosity, and migration of soluble Pb corrosion products (oxides, sulfates, carbonates) in bronze, with no documented protective effect in seawater [CITE], [GAP].

3. DED/WELDING: Primary standards (DOE 1978, engineering reviews) specify Pb ≤0.05 wt% for C70600, C71000, C71500 [Cu-Ni] and require even lower targets in welding practice (ideally ≤0.01 wt%) [SPEC], [NAVY]. Lead in excess causes hot and liquation cracking in Cu-Ni and is specifically cited as a contaminant prohibiting successful braze- and weld-joining; similar guidance applies for aluminum bronze [CITE]. Segregation and grain-boundary enrichment contribute to a 400–600°C ductility trough [NUMBERS]. No additive manufacturing process-specific data was found.

4. POWDER PROCESS: No data was found for DED feedstock production, laser evaporation, or induction/ultrasonic atomization of marine alloys with Pb [GAP]. Studies on Cu-Pb alloys indicate that Pb forms a miscibility gap with a monotectic at 955°C, and separates as Pb-rich droplets at typical atomization superheat (1,200–1,300°C) unless extremely dilute [NUMBERS].

5. PHASE DIAGRAM AND CALPHAD: Cu-Pb has no intermetallics—only FCC α-Cu and nearly pure FCC Pb. Thermodynamic assessments (Teppo 1991, Magnusson 2017) give max Pb solubility in α-Cu ≈1.3 wt% at ≈950°C, <1 ppm at room temp. The monotectic temperature is 955°C, Pb melting is 326–327°C [NUMBERS]. CALPHAD includes reliable binaries for Cu-Pb and Cu-Ni-Pb (Wang et al., CALPHAD 24, 149–167); Cu-Al-Pb not documented in TCCU/COST531 [GAP].

6. SUPPLY, COST, SAFETY: The 2025 USGS recommends Pb and Cu as critical minerals; Ni status is unconfirmed [CITE]. OSHA PEL for airborne Pb is 50 µg/m³ TWA; RoHS limit is 0.1 wt% [SPEC]. Pb dust and fume are hazardous in powder and AM processes. C10100 copper sets a benchmark of 5 ppm Pb [NUMBERS], [SPEC].

7. BOUNDS (wt%, Cu balance):
   a. DECISION: LIMIT as impurity only in both families.
   b. IMPURITY MAX: ≤0.01 wt% (100 ppm) for DED powder and deposit (stricter welding-source); ≤0.05 wt% (500 ppm) is a commercial outer limit for Cu-Ni/Al-bronze tubes/sheets [SPEC]. Procurement target: ≤0.005 wt% (50 ppm). High-purity: ≤0.0005 wt%.
   c. Failure mode: hot/liquation cracking, grain-boundary segregation, terminal Pb-rich liquid, toxic fume, and microgalvanic corrosion.

8. INTERACTIONS: Phosphorus does not neutralize Pb; no lead-phosphide phase found. Pb and S are each damaging in Cu-Ni joining [CITE]; controlling Pb via element ratios or sums is unsupported [GAP].

9. EVIDENCE QUALITY: Quantitative bounds for marine Cu-Ni alloys are strong and primary ([SPEC], [NAVY]). Most other sections, especially sea-corrosion and DED-specific, rely on general or secondary evidence, and AM-specific performance is an open question ([GAP]).

| Evidence topic | Key numeric findings or limits | Source citations | Tags |
|---|---|---|---|
| ROLE | Pb is not a useful solid-solution, precipitation-strengthening, deoxidizing, grain-refining, or protective-film-forming addition in marine Cu-Ni or Al-bronze. In Cu-Sn-Pb bronzes, it separates as soft free-Pb particles that improve machinability, castability, fluidity, and feeding while lowering melting temperature. C83600 contained **5 wt% Pb** in the cited alloy table. C93200, C84400, C93700, C93800, C94300, and C85700 are Pb-bearing commercial grades, but their current standard ranges were not recovered from accessible primary specifications. | (li2025recentprogresson pages 13-15, magnusson2017thermodynamicevaluationof pages 32-36, noyce2006useofcopper pages 2-3) | [CITE] [NUMBERS] [GAP] |
| SEAWATER CORROSION | No controlled Pb series was recovered comparing otherwise identical Cu-Ni or Al-bronze alloys in natural seawater, ASTM D1141 solution, or **3.5 wt% NaCl**. Available bronze evidence is qualitative and contradictory: one unspecified Pb range reportedly had no significant effect on powdery-corrosion formation, whereas a high-Pb copper alloy had the poorest resistance. Pb oxides, sulfates, and carbonates can dissolve or migrate and leave pores that promote localized microgalvanic attack. No Pb range demonstrably improves seawater resistance. | (li2025recentprogresson pages 13-15, li2025recentprogresson pages 9-13) | [CITE] [GAP] |
| DED/WELDING | A DOE joinability review lists C70600, C71000, and C71500 as readily weldable or brazeable with **Pb ≤0.05 wt%**. A separate copper-alloy engineering assessment says Cu-Ni Pb should be below the **0.01 wt% specified** because Pb impairs welding. Pb or S contamination can crack Cu-Ni during brazing by intergranular molten-metal penetration. Aluminum-bronze Pb is held very low for weldability; impurity segregation contributes to a **400–600 °C** ductility trough. No Pb-specific DED, cladding, ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl threshold was found. | (beaver1978stateoftheartsurveyof pages 39-44, konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155) | [CITE] [NUMBERS] [SPEC] [GAP] |
| POWDER PROCESS | No Pb-specific study was found for induction melting or ultrasonic atomization of marine Cu alloys using alumina, zirconia, or graphite crucibles or Ti-alloy or Mo sonotrodes. Cu-Pb experiments used **7, 32, 50, 55, and 73 at% Pb**, **1,300 °C** superheat, and **10 °C/s** cooling. The liquid miscibility-gap critical temperature was about **1,000 °C**, and the monotectic was **955 °C**. Melts containing **32–55 at% Pb** separated by density unless strongly overheated. Dilute-alloy concerns are Pb-rich droplets, particle-to-particle composition scatter, low-melting films, vapor or fume loss, and Pb-bearing condensate. | (чикова2016ополучениисплавов pages 1-2, чикова2016ополучениисплавов media 3032e471) | [CITE] [NUMBERS] [GAP] |
| PHASE/CALPHAD | Cu-Pb has no intermediate intermetallic compound; equilibrium condensed phases are Cu-rich FCC and nearly pure FCC Pb. Maximum Pb solubility in α-Cu is approximately **1.3 wt% at about 950 °C**, falling below **1 wt ppm** at room temperature. The monotectic is about **955 °C**, and the Pb-rich low-temperature invariant is about **326–327 °C**. Pb does not raise the Cu-rich liquidus above **1,250 °C**, but it creates liquid immiscibility and terminal low-temperature liquid. Published assessments include Cu-Pb by Teppo, Niemelä, and Taskinen and Cu-Ni-Pb by Wang et al., *CALPHAD* **24**, 149–167. TCCU or COST 531 coverage of Cu-Al-Pb was not established. | (чикова2016ополучениисплавов media 3032e471, oddy1992metallographyandmicrostructure pages 148-150, magnusson2017thermodynamicevaluationof pages 23-28, balart2020ontherole pages 8-8, magnusson2017thermodynamicevaluationof pages 32-36) | [CITE] [NUMBERS] [GAP] |
| SUPPLY/REG | Pb critical-mineral status and a defensible current price per kilogram were not established by the retrieved passages. A C10100 high-purity-copper benchmark limits Pb to **0.0005 wt%**, or **5 ppm**. Regulatory values requiring confirmation against current official text include an OSHA airborne-Pb PEL of **50 µg/m³** as an 8-hour TWA, an action level of **30 µg/m³**, and a RoHS homogeneous-material limit of **0.1 wt%**, or **1,000 ppm**, subject to exemptions. Fine powder and laser fume create inhalation, ingestion, and contamination hazards. | (nassar2025methodologyandtechnical pages 4-9, magnusson2017thermodynamicevaluationof pages 1-9, magnusson2017thermodynamicevaluationof pages 9-12) | [NUMBERS] [SPEC] [GAP] |
| BOUNDS | **LIMIT as impurity only** in both Cu-Ni and Al-bronze. Recommended powder and deposit acceptance limit: **Pb ≤0.01 wt%**, or **100 ppm**, based on the stricter retrieved Cu-Ni welding guidance. Recommended procurement target: **≤0.005 wt%**, or **50 ppm**, for process and analytical margin. High-purity research heats may target **≤0.0005 wt%**, or **5 ppm**. The documented **0.05 wt%** limit for C70600, C71000, and C71500 is an outer commercial precedent, not a preferred DED limit. Governing failures are terminal Pb-rich liquid, hot or liquation cracking, segregation, localized corrosion, and toxic fume. | (beaver1978stateoftheartsurveyof pages 39-44, magnusson2017thermodynamicevaluationof pages 9-12, konynenburg1990backgroundstudiesin pages 149-155) | [CITE] [NUMBERS] [SPEC] |
| INTERACTIONS | P does not neutralize Pb: calculations retain Pb as a separate inclusion, and no lead-phosphide data were available. Pb and S are independently damaging to Cu-Ni joining and should not be controlled through a compensating sum. Oxygen does not make Pb a useful deoxidizer. Added Ni does not eliminate terminal Pb-rich material; Fe, Ni, Al, and Mn control Cu-alloy phases but cannot be credited against Pb. No validated Pb-to-Ni, Pb-to-Fe, Pb-to-Mn, Pb-to-Al, or combined-element criterion was found. | (beaver1978stateoftheartsurveyof pages 39-44, magnusson2017thermodynamicevaluationof pages 16-21, magnusson2017thermodynamicevaluationof pages 12-14, magnusson2017thermodynamicevaluationof pages 23-28, konynenburg1990backgroundstudiesin pages 142-149) | [CITE] [GAP] |
| GAPS | Missing evidence includes matched **0–0.05 wt% Pb** DED alloys; particle-level segregation after ultrasonic atomization; laser Pb retention and fume mass balance; multilayer hot- and liquation-cracking thresholds; dilution into C95800 and C71500; Pb-specific OCP, LPR, EIS, cyclic-polarization, **30-day** attack-depth, and erosion-corrosion results; current ASTM, MIL, and AWS Pb tables; verified TCCU Cu-Al-Pb and Cu-Ni-Pb descriptions; and directly verified Pb ranges for C93200, C84400, C93700, C93800, and C94300. | (li2025recentprogresson pages 13-15, beaver1978stateoftheartsurveyof pages 39-44, li2025recentprogresson pages 9-13, konynenburg1990backgroundstudiesin pages 142-149, magnusson2017thermodynamicevaluationof pages 21-23) | [CITE] [SPEC] [NAVY] [GAP] |


*Table: Traceable Pb-specific evidence supporting impurity-only control in Cu-Ni and aluminum-bronze DED alloys. Quantitative limits are separated from unverified standards, commercial ranges, and unresolved AM and corrosion questions.*

VERDICT | Pb | decision=LIMIT | family=both | conservative_max_wt=0.01 | nonconservative_max_wt=0.05 | floor_wt=NA | impurity_max_wt=0.01 | evidence=moderate

References

1. (li2025recentprogresson pages 13-15): Hongliang Li, Zilu Zhang, Hanjie Guo, Chao Ren, Chunyan Liu, and Li Xiang. Recent progress on corrosion behavior, mechanism, and protection strategies of bronze artefacts. Heritage, 8:340, Aug 2025. URL: https://doi.org/10.3390/heritage8080340, doi:10.3390/heritage8080340. This article has 16 citations.

2. (magnusson2017thermodynamicevaluationof pages 32-36): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

3. (noyce2006useofcopper pages 2-3): J. O. Noyce, H. Michels, and C. W. Keevil. Use of copper cast alloys to control escherichia coli o157 cross-contamination during food processing. Applied and Environmental Microbiology, 72:4239-4244, Jun 2006. URL: https://doi.org/10.1128/aem.02532-05, doi:10.1128/aem.02532-05. This article has 292 citations and is from a peer-reviewed journal.

4. (li2025recentprogresson pages 9-13): Hongliang Li, Zilu Zhang, Hanjie Guo, Chao Ren, Chunyan Liu, and Li Xiang. Recent progress on corrosion behavior, mechanism, and protection strategies of bronze artefacts. Heritage, 8:340, Aug 2025. URL: https://doi.org/10.3390/heritage8080340, doi:10.3390/heritage8080340. This article has 16 citations.

5. (beaver1978stateoftheartsurveyof pages 39-44): R. J. Beaver. State-of-the-art survey of joinability of materials for otec heat exchangers. ArXiv, 80:10647, Dec 1978. URL: https://doi.org/10.2172/6523751, doi:10.2172/6523751. This article has 1 citations.

6. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

7. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

8. (чикова2016ополучениисплавов pages 1-2): Ольга Анатольевна Чикова, Ганна Сакун, and Владимир Степанович Цепелев. О получении сплавов cu–pb путем гомогенизации жидкого металла. ArXiv, pages 76-82, Aug 2016. URL: https://doi.org/10.17073/0021-3438-2016-4-76-82, doi:10.17073/0021-3438-2016-4-76-82. This article has 4 citations.

9. (чикова2016ополучениисплавов media 3032e471): Ольга Анатольевна Чикова, Ганна Сакун, and Владимир Степанович Цепелев. О получении сплавов cu–pb путем гомогенизации жидкого металла. ArXiv, pages 76-82, Aug 2016. URL: https://doi.org/10.17073/0021-3438-2016-4-76-82, doi:10.17073/0021-3438-2016-4-76-82. This article has 4 citations.

10. (oddy1992metallographyandmicrostructure pages 148-150): Andrew Oddy and D. A. Scott. Metallography and microstructure of ancient and historic metals. Studies in Conservation, 37(4):282, Nov 1992. URL: https://doi.org/10.2307/1506361, doi:10.2307/1506361. This article has 1275 citations and is from a domain leading peer-reviewed journal.

11. (magnusson2017thermodynamicevaluationof pages 23-28): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

12. (balart2020ontherole pages 8-8): M. J. Balart, F. Gao, J. B. Patel, and F. Miani. On the role of dilute solute additions on growth restriction in binary copper alloys. Metallography, Microstructure, and Analysis, 9:825-832, Nov 2020. URL: https://doi.org/10.1007/s13632-020-00695-6, doi:10.1007/s13632-020-00695-6. This article has 3 citations.

13. (nassar2025methodologyandtechnical pages 4-9): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

14. (magnusson2017thermodynamicevaluationof pages 1-9): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

15. (magnusson2017thermodynamicevaluationof pages 9-12): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

16. (magnusson2017thermodynamicevaluationof pages 16-21): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

17. (magnusson2017thermodynamicevaluationof pages 12-14): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

18. (magnusson2017thermodynamicevaluationof pages 21-23): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.
