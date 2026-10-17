<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 1854f32a-8feb-416b-8952-fbddb3f24cbc
- Submitted: 2026-10-17T18:58:46Z
- Fetched: 2026-10-17T19:30:29Z (status: success)
- Raw trajectory JSON: ../raw/el-07-Sn.json.gz
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

ELEMENT UNDER REVIEW: Sn (major seawater addition). Tin bronzes and gunmetals (C90300, C90500: 8-10 Sn), phosphor bronze C51000 (5 Sn), Cu-Ni-Sn spinodal C72900 (Cu-15Ni-8Sn), admiralty brass (1 Sn). Wide freezing range and Sn-rich delta phase.

Answer for Sn specifically, not for copper alloys in general:
1. ROLE: what Sn does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sn ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sn changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sn, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sn, Cu-Ni-Sn and Cu-Al-Sn are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sn in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sn neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sn | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Sn (major seawater addition). Tin bronzes and gunmetals (C90300, C90500: 8-10 Sn), phosphor bronze C51000 (5 Sn), Cu-Ni-Sn spinodal C72900 (Cu-15Ni-8Sn), admiralty brass (1 Sn). Wide freezing range and Sn-rich delta phase.

Answer for Sn specifically, not for copper alloys in general:
1. ROLE: what Sn does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sn ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sn changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sn, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sn, Cu-Ni-Sn and Cu-Al-Sn are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sn in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sn neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sn | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Sn as a designed addition to marine DED copper powder

**Decision — INCLUDE, with separate family-specific constraints.** Sn merits controlled experiments because it improves tin-bronze erosion resistance, measurably changes Cu–Al–Ni chloride corrosion near 0.5–1.0 wt%, and participates in established Cu–Ni–Sn alloys. None of those findings establishes that an **as-deposited, single-stream laser-DED** alloy will equal wrought C71500 in seawater, or that one high-Sn powder will repair both C95800 and wrought Cu–Ni without cracking. The proposed bounds are therefore *composition-search bounds*, not acceptance limits or demonstrated DED qualifications. [CITE][GAP] (laque1969deteriorationofmetals pages 13-16, saud2016influenceoftin pages 10-12, cheng2020corrosionandcorrosive‐wear pages 1-2, majdanchuk2014electrodeandfiller pages 1-2)

## 1. Role and alloy precedents

- **Tin bronze, gunmetal and phosphor bronze.** Sn strengthens Cu by substitutional solid solution; segregation during freezing can leave Sn-rich interdendritic material and brittle **δ-Cu₄₁Sn₁₁**. Phosphorus—not Sn—is the specifically documented melt deoxidizer in tin–phosphorus bronze. The reviewed cast tin–zinc bronzes include **C90300** and **C90500**; wrought phosphor-bronze designations include **C51000** and **C52100**. The review identifies approximately Cu–8Sn–4Zn and Cu–10Sn–2Zn as the corresponding gunmetal-type compositions, and CuSn8-type wrought bronze as a further precedent. These are casting/wrought precedents, not permissible Sn ranges for C95800 or a Navy-approved repair powder. [CITE][SPEC: alloy designations discussed in Majdanchuk, not verified certificate limits][NUMBERS] (majdanchuk2014electrodeandfiller pages 1-2, majdanchuk2014electrodeandfiller pages 2-4, valloton2012competitionofthe pages 5-7)
- **Brass.** Admiralty brass contains approximately **1 wt% Sn**; Sn reduces, but does **not** eliminate, dezincification of high-Zn brass. LaQue instead identifies limiting Zn to approximately **15 wt%**, or adding approximately **0.05 wt% As, Sb or P**, as more effective dezincification controls. This is not evidence that Sn prevents dealuminification in NAB. Nordic Gold is another identified Cu–Al–Zn–Sn composition, approximately **Cu–5Al–5Zn–1Sn**. [CITE][NUMBERS] (laque1969deteriorationofmetals pages 13-16, sur2025revisitingtheinfluence pages 3-5)
- **Al bronze and NAB.** Sn is **not established as a required designed constituent of baseline C95800** in the evidence retrieved. In *experimental cast NAB*, approximately **1.0 wt% Sn** changed columnar to equiaxed grains and altered κ-phase morphology; hardness and tensile strength rose by as much as **69%** and **28.4%**, respectively. These are mechanical and solidification findings, **not** a seawater-corrosion qualification. In Cu–Al–Sn solid solutions, Sn can facilitate Al-rich passive-film formation; the particularly striking third-element-effect results were measured in **acidified sulfate, not seawater**. [CITE][NUMBERS][GAP] (poojary2023enhancingmicrostructureand pages 6-8, poojary2023enhancingmicrostructureand pages 1-2, sur2025revisitingtheinfluence pages 1-3, sur2025revisitingtheinfluence pages 3-5)
- **Cu–Ni and Cu–Ni–Sn.** Conventional seawater-service Cu–Ni is not evidence that Sn is an essential constituent of wrought **C71500**. In contrast, **C72900-type Cu–15Ni–8Sn** is an established *high-strength, heat-treatable* Cu–Ni–Sn branch: Sn contributes to a supersaturated Cu-rich matrix and Ni/Sn-rich precipitation on aging. Its aged properties must not be attributed to an unaged deposit. The retrieved welding review also identifies **C72500, C72650 and C72700** as wrought tin–nickel bronzes, without furnishing verified specification intervals. **Cu–Ni–Si** should be treated as a separate precipitation system: the retrieved evidence does not establish an Sn requirement or a marine benefit from adding Sn to it. [CITE][SPEC: UNS designation, nominal composition only][GAP] (majdanchuk2014electrodeandfiller pages 2-4, cheng2020corrosionandcorrosive‐wear pages 1-2, cheng2020corrosionandcorrosive‐wear pages 2-4)

**Specification check required before procurement.** ASTM **B148** (cast bronzes), **B111/B466/B171** (applicable Cu–Ni product forms), **B103/B122/B139/B740** (wrought tin bronzes, as applicable), AWS **A5.7** filler classifications, and the named MIL specifications must be checked against their *current grade-specific composition tables*. Retrieved material does **not** substantiate exact Sn minimum/maximum values for C90300, C90500, C51000, C95800, C71500, ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl, nor does it show that those four fillers intentionally contain Sn. The nominal examples above must not be misrepresented as certified ASTM, AWS, MIL-T-16420, MIL-B-24480 or MIL-C-15726 limits. [SPEC][GAP] (majdanchuk2014electrodeandfiller pages 1-2, majdanchuk2014electrodeandfiller pages 2-4)

## 2. Quantitative chloride and seawater evidence

Saud and colleagues tested mechanically alloyed, microwave-sintered **Cu–Al–Ni shape-memory material**, rather than NAB or DED, in **3.5 wt% NaCl**. Their corrosion *currents* and separately reported *penetration rates* must not be confused: the apparent rate sequence is **3.19, 2.16, 0.62 and 2.56 mm/year** at **0, 0.5, 1.0 and 1.5 wt% Sn**, respectively. The corresponding *i*corr values are **139.8, 94.8, 27.3 and 112.1 µA/cm²**; *R*p is **2.97, 5.26, 19.20 and 4.20 kΩ·cm²**; and *E*corr is **−560.6, −357.6, −273.3 and −515.5 mV versus SCE**. The favorable response peaks near **1 wt% Sn**, then reverses at **1.5 wt%**; the investigators associate the reversal partly with porosity and Sn-bearing secondary phases. Crucially, even their best reported rate is not evidence of meeting the proposed wrought-C71500 target. Saud *et al.*, *Metallurgical and Materials Transactions A* **47** (2016) 5242–5255, DOI **10.1007/s11661-016-3628-y**. [CITE][NUMBERS][GAP] (saud2016influenceoftin media be681457, saud2016influenceoftin pages 10-12, saud2016influenceoftin pages 10-10, saud2016influenceoftin pages 12-13)

| Alloy / condition | Sn (wt%) | *E*<sub>corr</sub> vs SCE (mV) | *i*<sub>corr</sub> (µA/cm²) | *R*<sub>p</sub> (kΩ·cm²) | Immersion corrosion rate (mm/year) | Decision relevance |
|---|---:|---:|---:|---:|---:|---|
| Mechanically alloyed and microwave-sintered Cu–Al–Ni shape-memory alloy; not NAB or DED | 0 | −560.6 | 139.8 | 2.97 | 3.19 | Unacceptably high for the marine target; comparator only (saud2016influenceoftin media be681457) |
| Mechanically alloyed and microwave-sintered Cu–Al–Ni shape-memory alloy; not NAB or DED | 0.5 | −357.6 | 94.8 | 5.26 | 2.16 | Measurable benefit, but rate remains unacceptably high (saud2016influenceoftin media be681457) |
| Mechanically alloyed and microwave-sintered Cu–Al–Ni shape-memory alloy; not NAB or DED | 1.0 | −273.3 | 27.3 | 19.20 | 0.62 | Best tested Sn level, but rate remains unacceptably high; supports a 1.0 wt% Al-bronze screening point (saud2016influenceoftin media be681457) |
| Mechanically alloyed and microwave-sintered Cu–Al–Ni shape-memory alloy; not NAB or DED | 1.5 | −515.5 | 112.1 | 4.20 | 2.56 | Performance reverses as porosity and Sn-bearing intermetallics increase; supports an aggressive—not conservative—Al-bronze ceiling (saud2016influenceoftin media be681457) |
| Hot-isostatically pressed and aged Cu–15Ni–8Sn; not as-deposited DED | 8.0 | — | — | — | 0.00498 at pH 8; 0.01334 at pH 7 after 70 days | Much lower general rate, but pits and intergranular attack occurred; supports 8 wt% only as a separate aggressive Cu–Ni–Sn pathway, not as proof of DED repair performance (cheng2020corrosionandcorrosive‐wear pages 4-8, cheng2020corrosionandcorrosive‐wear pages 2-4) |


*Table: Quantitative chloride and substitute-seawater evidence used to set Sn screening bounds. The Cu–Al–Ni data are from Saud et al. (2016), DOI 10.1007/s11661-016-3628-y; the Cu–15Ni–8Sn data are from Cheng et al. (2020), DOI 10.1002/maco.201911323.*

Cheng and colleagues made **Cu–15Ni–8Sn** from prealloyed powder by powder metallurgy, then **aged** it: after **70 days** in **ASTM D1141 substitute seawater** at **25 °C**, general mass-loss rates were **0.00498 mm/year at pH 8.0** and **0.01334 mm/year at pH 7.0**. Nevertheless, pits and intergranular grooves were observed; Ni and Sn accumulated in corrosion products while Cu was relatively depleted. These are not maximum pit-depth measurements, an Sn-free/C71500 comparison, or as-DED data. Cheng *et al.*, *Materials and Corrosion* **71** (2020) 593–607, DOI **10.1002/maco.201911323**. [CITE][NUMBERS][GAP] (cheng2020corrosionandcorrosive‐wear pages 4-8, cheng2020corrosionandcorrosive‐wear pages 2-4, cheng2020corrosionandcorrosive‐wear pages 1-2)

For **wire-arc-deposited Cu–4.2Sn**, simulated-seawater testing reported *E*corr **−0.30 V** and *i*corr **8.11 µA/cm²** before sliding; with sliding, approximately **−0.48 V** and **107 µA/cm²**. This is a valuable *as-deposited* Sn-bronze observation, but it does not isolate the effect of Sn, and wire-arc deposition is not blown-powder laser DED. Zhong *et al.*, *npj Materials Degradation* **9** (2025), DOI **10.1038/s41529-025-00655-x**. [CITE][NUMBERS][GAP] (zhong2025enhancingmechanicalstrength pages 10-11)

**Limits of the benefit.** Tin-bearing bronze can form inner Sn oxides/oxyhydroxides alongside Cu₂O and chloride-containing corrosion products; Sn is **not universally passive**. Cu₃Sn and Cu₆Sn₅ intermetallic specimens in **3.5 wt% NaCl** showed differing pitting and galvanic behavior, so a continuous Sn-rich constituent is not automatically a protective film. Separately, laser-powder-bed-fused **Cu–10Sn** suffered *more* weight loss and higher corrosion current **as fabricated** than after 600 or 800 °C annealing in 3.5 wt% NaCl. That directly cautions against transferring heat-treated bronze results to the required as-deposited condition. Tsao and Chen, *Corrosion Science* **63** (2012) 393–398, DOI **10.1016/j.corsci.2012.06.015**; Nemani *et al.*, *Journal of Manufacturing and Materials Processing* **8** (2024) 54, DOI **10.3390/jmmp8020054**. [CITE][GAP] (tsao2012corrosioncharacterizationof pages 5-6, nemani2024advancementsinadditive pages 50-53)

**Erosion and velocity are composition-dependent, not an Sn-derived qualification.** Historical marine-service guidance places roughly **10 wt% Sn** gunmetal/phosphor bronze near 90–10 Cu–Ni in erosion resistance and sometimes approaching 70–30 Cu–Ni. LaQue reports illustrative critical seawater velocities of **6 ft/s (1.83 m/s)** for Admiralty brass, **15 ft/s (4.57 m/s)** for 90–10 Cu–Ni and **18 ft/s (5.49 m/s)** for 70–30 Cu–Ni; these are *flow-design guidance*, not measured velocity limits for an Sn-modified DED alloy. Direct Sn-dose-resolved NAB or Cu–Ni measurements of crevice depth, pit depth and impingement threshold were not obtained. LaQue, *Ocean Engineering* **1** (1969) 299–312, DOI **10.1016/0029-8018(69)90031-6**. [CITE][NUMBERS][GAP] (laque1969deteriorationofmetals pages 13-16)

## 3. DED, welding and repair interfaces

[CITE][GAP] The directly relevant *welding*, rather than laser-DED, review identifies **hydrogen/water-vapor porosity, weld and heat-affected-zone solidification cracking, Sn liquation and composition inhomogeneity**, and brittle Sn-rich δ-phase as recurring problems in cast tin bronze. It recommends controlling heat input and sometimes using a **lower-Sn consumable**. Those observations are reasons to measure crack length and grain-boundary segregation after successive reheating passes; they do not establish a numerical DED cracking threshold. Majdanchuk, *The Paton Welding Journal* **2014**(1), 55–60, DOI **10.15407/tpwj2014.01.09**. [CITE] (majdanchuk2014electrodeandfiller pages 1-2, majdanchuk2014electrodeandfiller pages 2-4)

At **C95800**, a first-pass melt diluted by Al/Ni/Fe-rich substrate is *not* the powder composition: predict local solidification and κ/β constituents using the actual mixed composition, and examine reheated cast-substrate grain boundaries for liquation. At wrought **Cu–Ni**, Ni uptake and Sn segregation may move the fusion boundary toward a Cu–Ni–Sn precipitation/segregation regime. Both are **testable mechanisms, not documented results for these two specific repair interfaces**. Published LPBF of prealloyed Cu–15Ni–8Sn and Cu–10Sn shows process sensitivity to energy input and porosity; LPBF evidence does not prove a dense, crack-free single-stream DED repair. AWS **A5.7** ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl are useful *Sn-lean welding comparators* only after their current compositions are verified; no retrieved source establishes an Sn-bearing qualification for them here. [CITE][SPEC][GAP] (majdanchuk2014electrodeandfiller pages 2-4, nemani2024advancementsinadditive pages 43-47, nemani2024advancementsinadditive pages 110-112)

## 4. Melting, atomization, phase boundaries and CALPHAD

**Powder process.** Adding Sn to Cu is not a reason, by itself, to expect the **Cu–Sn binary liquidus** to exceed the approximately **1,200–1,250 °C useful-superheat ceiling**: Sn lowers the melting temperature along the Cu-rich binary branch. A Ni-/Fe-/Al-rich *multicomponent* candidate nevertheless requires its own calculated liquidus and a measured melt/superheat margin. Wide Cu–Sn freezing intervals promote segregation, residual liquid and feeding defects; excessive laser energy can vaporize material and destabilize tracks, whereas insufficient energy leaves pores. The reviewed LPBF Cu–10Sn study found poorer behavior at its highest tested energy density because material vaporization/balling became problematic; it does **not** isolate a measured Sn evaporation percentage. [CITE][NUMBERS][GAP] (valloton2012competitionofthe pages 1-3, nemani2024advancementsinadditive pages 43-47, valloton2012competitionofthe pages 3-5)

For the proposed argon induction/ultrasonic setup, use dry, oxygen-free charge and analyze **feed metal, atomized size fractions and deposits separately** for Sn and oxygen. Oxidation/oxide inclusions and Sn loss are plausible variables; however, no retrieved experiment quantifies Sn pickup/loss or a specific chemical reaction against **alumina versus zirconia crucibles, graphite, or titanium-alloy versus molybdenum sonotrodes** on this apparatus. A published Cu–21Sn directional-solidification experiment *did* melt Cu–Sn inside an alumina capillary under argon and reported **wetting/bubble difficulties**; that is relevant caution, not a proof of a destructive alumina–Sn reaction. Nor was a measured Sn-induced surface-tension change for the proposed melt established. [CITE][GAP] (valloton2012competitionofthe pages 3-5, valloton2012competitionofthe pages 5-7)

**Phase diagram.** The often-quoted maximum α-Cu solubility is approximately **15.8 wt% Sn near 520 °C**, not a room-temperature single-phase allowance or a safe DED composition. Cu–Sn has a Cu-rich **L + α → β peritectic near 796–798 °C** and **β → α + δ around 520 °C**; δ is **Cu₄₁Sn₁₁**. Other Cu–Sn phases, including Cu₃Sn and Cu₆Sn₅, must not be called δ-Cu₄₁Sn₁₁. Binary α solubility cannot bound Sn independently of Ni and Al, rapid-solidification segregation or successive-pass thermal cycling. Valloton *et al.*, *Acta Materialia* **60** (2012) 3840–3848, DOI **10.1016/j.actamat.2012.03.030**. [CITE][NUMBERS] (sur2025revisitingtheinfluence pages 3-5, valloton2012competitionofthe pages 3-5, valloton2012competitionofthe pages 5-7)

**CALPHAD status.** Assessed Cu–Sn phase descriptions exist, and a Cu–Al–Sn corrosion study reports a calculated ternary phase diagram—yet also observed **Cu₃Sn and multiple phases where its calculation expected a single phase**. Retrieved evidence does **not** verify precisely which Cu–Ni–Sn and Cu–Al–Sn ternary interactions are assessed in the installed **TCCU release**, or establish that **COST 531** contains a validated copper-rich multicomponent model for this particular composition space. An Al-*rich* Al–Cu–Sn thermodynamic/solidification paper is **not validation** of Cu-rich NAB. Audit the installed TDB phase descriptions and parameters; compare equilibrium and Scheil results against DSC and powder/deposit EDS. Sur *et al.*, *Journal of The Electrochemical Society* **172** (2025) 101502, DOI **10.1149/1945-7111/ae0eb6**; de Albuquerque *et al.*, *Materials Today Communications* **40** (2024) 109545, DOI **10.1016/j.mtcomm.2024.109545**. [CITE][GAP] (sur2025revisitingtheinfluence pages 10-13, albuquerque2024solidificationpathsof pages 1-5)

## 5. Supply, safety and interactions

**Supply.** **Tin appears on the U.S. final 2025 critical-minerals list; copper was added in 2025.** The 2025 table itself lists “Tin—Metallurgy,” correcting the misleading inference that tin was absent simply because it falls on the following page. The retrieved USGS historical tin account gives **2020** annual averages of **$7.99/lb New York dealer**, approximately **$17.6/kg**, and **$7.77/lb LME cash**, approximately **$17.1/kg**; these are *historical commodity prices*, not a 2026 quote, certified powder cost or an alloy surcharge. USGS, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, Open-File Report **2025–1047**, DOI **10.3133/ofr20251047**; final list, **90 FR 50494**. The retrieved material did not independently reproduce the complete **2022** list, so its tin entry should be confirmed against the 2022 Federal Register before stating a 2022 yes/no as a verified finding. [CITE][NAVY: supply relevance, not a documented Sn-alloy qualification][NUMBERS][GAP] (staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 6-9, nassar2025methodologyandtechnical pages 9-10, earths20122010mineralsyearbook pages 4-4)

**Health and regulation.** Treat elemental Sn and inorganic tin-oxide dust/fume differently from **organotin compounds**; do not infer an organotin prohibition on bulk Sn-bearing bronze, or claim a measured fume exposure from alloy composition alone. Obtain current OSHA/NIOSH substance-specific limits and SDS for the actual powder and fume; control inhalable powder and laser fumes by enclosure, local exhaust, appropriate filtration, housekeeping and exposure monitoring. Also screen **Pb** in gunmetal feedstocks separately: using leaded commercial bronzes as corrosion precedents does not make Pb acceptable under RoHS/REACH or a Navy acquisition specification. The retrieved sources did not establish a Sn-specific Navy prohibition, an applicable powder-explosion threshold, or a verified numerical OSHA tin limit; none is invented here. [GAP] (majdanchuk2014electrodeandfiller pages 1-2, majdanchuk2014electrodeandfiller pages 2-4)

**Joint constraints.** Constrain **Sn × Al** rather than transferring the beneficial acid-sulfate Cu–Al–Sn synergy to chloride service: the sulfate study found improved Al-rich passivation, whereas the chloride Cu–Al–Ni study peaked near **1 wt% Sn** and deteriorated by **1.5 wt%**. Constrain **Sn × Ni** for an intentionally separate Cu–Ni–Sn precipitation branch: **15 wt% Ni + 8 wt% Sn** is an *aged* reference, not proof that replacing Ni with Sn preserves C71500-type seawater behavior. Keep **Fe** appropriate to the target Cu–Ni or NAB substrate and reassess first-layer dilution; LaQue's approximate erosion guidance was **1.25 wt% Fe in 90–10 Cu–Ni** versus **0.5 wt% Fe in 70–30 Cu–Ni**, not an Sn–Fe optimum. Prevent Zn/Sn dezincification arguments from being substituted for NAB dealuminification evidence; avoid importing Pb-, Bi-, S- or excess-P-bearing low-melting boundary constituents into a crack-sensitive DED search. No validated numerical Sn/(Ni+Fe), Sn/Al or Sn/Mn ratio was found. [CITE][NUMBERS][GAP] (sur2025revisitingtheinfluence pages 13-16, saud2016influenceoftin pages 10-12, laque1969deteriorationofmetals pages 13-16, majdanchuk2014electrodeandfiller pages 2-4)

## 6. Explicit search bounds and evidence quality

- **Functional floor: 0.5 wt% Sn, Al-bronze-related screening.** This is the smallest *directly tested* beneficial chloride addition in the retrieved Cu–Al–Ni series, **not** the demonstrated physical threshold in cast NAB, Cu–Ni or DED. A lower trace addition may work but remains unproven. [NUMBERS][GAP] (saud2016influenceoftin media be681457)
- **Conservative maximum: 1.0 wt% Sn for the proposed shared Cu–Ni/Al-bronze search.** This is a *proposed screening cap*, supported by the approximately **1 wt%** optimum in experimental cast NAB, **1 wt%** commercial Cu–Al–Zn/Admiralty-brass precedents, and the chloride Cu–Al–Ni screening peak. It is **not** a C95800/C71500/AWS compositional allowance or a demonstrated Cu–Ni seawater optimum. Primary failure concern above it: Sn-rich segregation, residual liquid, reheated-boundary cracking and localized attack. [CITE][NUMBERS][GAP] (poojary2023enhancingmicrostructureand pages 6-8, sur2025revisitingtheinfluence pages 1-3, saud2016influenceoftin pages 10-12, majdanchuk2014electrodeandfiller pages 2-4)
- **Non-conservative maximum: 1.5 wt% Sn for an Al-bronze/NAB-adjacent *exploratory* branch.** This point is *deliberately a falsification limit*, not a proven benefit: the Cu–Al–Ni chloride experiment had distinctly worse corrosion there than at **1.0 wt%**, and its porosity/precipitate effects confound attribution. Do not advance a 1.5 wt% NAB deposit without clean multilayer/HAZ microscopy and 30-day penetration measurements. [NUMBERS][GAP] (saud2016influenceoftin media be681457, saud2016influenceoftin pages 6-8, saud2016influenceoftin pages 12-13)
- **Separate, not interchangeable Cu–Ni–Sn branch:** approximately **8 wt% Sn with 15 wt% Ni** is defensible *only* as an aggressive C72900-type experimental branch, because the supporting marine rates are from an **aged powder-metallurgy** alloy with pits and intergranular attack. Tin bronze at **8–10 wt% Sn** likewise establishes alloy existence, **not** permission to insert 8–10 wt% into a common NAB/Cu–Ni repair palette. If that branch is pursued, give it separate CALPHAD, weldability and as-deposited seawater gates. [CITE][NUMBERS][GAP] (majdanchuk2014electrodeandfiller pages 1-2, majdanchuk2014electrodeandfiller pages 2-4, cheng2020corrosionandcorrosive‐wear pages 4-8, cheng2020corrosionandcorrosive‐wear pages 2-4)

**Evidence assessment: moderate for including Sn as a research variable; thin for claiming the final marine/repair target.** Controlled chloride evidence comes from a porous, sintered Cu–Al–Ni shape-memory alloy; the direct cast-NAB Sn study measures mechanical properties; the best quantified Cu–Ni–Sn marine rates concern an aged alloy; and LPBF or welding is not the specified laser DED. No retrieved study establishes an as-deposited Sn-bearing deposit simultaneously dense, crack-free on itself and both repair substrates, and at least as resistant to seawater—including maximum selective-attack depth—as wrought C71500. [CITE][GAP] (poojary2023enhancingmicrostructureand pages 6-8, saud2016influenceoftin pages 10-12, majdanchuk2014electrodeandfiller pages 2-4, cheng2020corrosionandcorrosive‐wear pages 4-8, nemani2024advancementsinadditive pages 50-53)

VERDICT | Sn | decision=INCLUDE | family=both | conservative_max_wt=1.0 | nonconservative_max_wt=1.5 | floor_wt=0.5 | impurity_max_wt=NA | evidence=moderate

References

1. (laque1969deteriorationofmetals pages 13-16): F.L. LaQue. Deterioration of metals in an ocean environment. Ocean Engineering, 1:299-312, Feb 1969. URL: https://doi.org/10.1016/0029-8018(69)90031-6, doi:10.1016/0029-8018(69)90031-6. This article has 11 citations and is from a domain leading peer-reviewed journal.

2. (saud2016influenceoftin pages 10-12): Safaa N. Saud, E. Hamzah, T. Abubakar, H. R. Bakhsheshi-Rad, and M. N. Mohammed. Influence of tin additions on the phase-transformation characteristics of mechanical alloyed cu-al-ni shape-memory alloy. Metallurgical and Materials Transactions A, 47:5242-5255, Jul 2016. URL: https://doi.org/10.1007/s11661-016-3628-y, doi:10.1007/s11661-016-3628-y. This article has 32 citations.

3. (cheng2020corrosionandcorrosive‐wear pages 1-2): Jinjuan Cheng, Zheming Wang, Xue-ping Gan, Qian Lei, Zhou Li, and Kechao Zhou. Corrosion and corrosive‐wear behaviors of a high strength and toughness cu–15ni–8sn alloy in seawater. Materials and Corrosion, 71:593-607, Dec 2020. URL: https://doi.org/10.1002/maco.201911323, doi:10.1002/maco.201911323. This article has 25 citations.

4. (majdanchuk2014electrodeandfiller pages 1-2): T. B. Majdanchuk. Electrode and filler materials for surfacing and welding of cast tin bronzes (review). The Paton Welding Journal, 2014:55-60, Jan 2014. URL: https://doi.org/10.15407/tpwj2014.01.09, doi:10.15407/tpwj2014.01.09. This article has 2 citations.

5. (majdanchuk2014electrodeandfiller pages 2-4): T. B. Majdanchuk. Electrode and filler materials for surfacing and welding of cast tin bronzes (review). The Paton Welding Journal, 2014:55-60, Jan 2014. URL: https://doi.org/10.15407/tpwj2014.01.09, doi:10.15407/tpwj2014.01.09. This article has 2 citations.

6. (valloton2012competitionofthe pages 5-7): J. Valloton, J.-D. Wagnière, and M. Rappaz. Competition of the primary and peritectic phases in hypoperitectic cu-sn alloys solidified at low speed in a diffusive regime. Acta Materialia, 60:3840-3848, May 2012. URL: https://doi.org/10.1016/j.actamat.2012.03.030, doi:10.1016/j.actamat.2012.03.030. This article has 54 citations and is from a highest quality peer-reviewed journal.

7. (sur2025revisitingtheinfluence pages 3-5): Debashish Sur, Nathan C. Smith, Elaf A. Anber, Kaitlyn L. Anderson, Peter F. Connors, Daniel Foley, Mitra L. Taheri, Junsoo Han, Christopher M. Wolverton, and John R. Scully. Revisiting the influence of sn in cu-al alloys: a <i>third element effect</i> enabling stainless steel type corrosion behavior. Journal of The Electrochemical Society, 172(10):101502, Oct 2025. URL: https://doi.org/10.1149/1945-7111/ae0eb6, doi:10.1149/1945-7111/ae0eb6. This article has 6 citations and is from a peer-reviewed journal.

8. (poojary2023enhancingmicrostructureand pages 6-8): Sushanth Poojary, Vikas Marakini, Rajath N. Rao, and Vijeesh Vijayan. Enhancing microstructure and mechanical properties of nickel aluminium bronze alloy through tin addition. Scientific Reports, Oct 2023. URL: https://doi.org/10.1038/s41598-023-44146-y, doi:10.1038/s41598-023-44146-y. This article has 16 citations and is from a peer-reviewed journal.

9. (poojary2023enhancingmicrostructureand pages 1-2): Sushanth Poojary, Vikas Marakini, Rajath N. Rao, and Vijeesh Vijayan. Enhancing microstructure and mechanical properties of nickel aluminium bronze alloy through tin addition. Scientific Reports, Oct 2023. URL: https://doi.org/10.1038/s41598-023-44146-y, doi:10.1038/s41598-023-44146-y. This article has 16 citations and is from a peer-reviewed journal.

10. (sur2025revisitingtheinfluence pages 1-3): Debashish Sur, Nathan C. Smith, Elaf A. Anber, Kaitlyn L. Anderson, Peter F. Connors, Daniel Foley, Mitra L. Taheri, Junsoo Han, Christopher M. Wolverton, and John R. Scully. Revisiting the influence of sn in cu-al alloys: a <i>third element effect</i> enabling stainless steel type corrosion behavior. Journal of The Electrochemical Society, 172(10):101502, Oct 2025. URL: https://doi.org/10.1149/1945-7111/ae0eb6, doi:10.1149/1945-7111/ae0eb6. This article has 6 citations and is from a peer-reviewed journal.

11. (cheng2020corrosionandcorrosive‐wear pages 2-4): Jinjuan Cheng, Zheming Wang, Xue-ping Gan, Qian Lei, Zhou Li, and Kechao Zhou. Corrosion and corrosive‐wear behaviors of a high strength and toughness cu–15ni–8sn alloy in seawater. Materials and Corrosion, 71:593-607, Dec 2020. URL: https://doi.org/10.1002/maco.201911323, doi:10.1002/maco.201911323. This article has 25 citations.

12. (saud2016influenceoftin media be681457): Safaa N. Saud, E. Hamzah, T. Abubakar, H. R. Bakhsheshi-Rad, and M. N. Mohammed. Influence of tin additions on the phase-transformation characteristics of mechanical alloyed cu-al-ni shape-memory alloy. Metallurgical and Materials Transactions A, 47:5242-5255, Jul 2016. URL: https://doi.org/10.1007/s11661-016-3628-y, doi:10.1007/s11661-016-3628-y. This article has 32 citations.

13. (saud2016influenceoftin pages 10-10): Safaa N. Saud, E. Hamzah, T. Abubakar, H. R. Bakhsheshi-Rad, and M. N. Mohammed. Influence of tin additions on the phase-transformation characteristics of mechanical alloyed cu-al-ni shape-memory alloy. Metallurgical and Materials Transactions A, 47:5242-5255, Jul 2016. URL: https://doi.org/10.1007/s11661-016-3628-y, doi:10.1007/s11661-016-3628-y. This article has 32 citations.

14. (saud2016influenceoftin pages 12-13): Safaa N. Saud, E. Hamzah, T. Abubakar, H. R. Bakhsheshi-Rad, and M. N. Mohammed. Influence of tin additions on the phase-transformation characteristics of mechanical alloyed cu-al-ni shape-memory alloy. Metallurgical and Materials Transactions A, 47:5242-5255, Jul 2016. URL: https://doi.org/10.1007/s11661-016-3628-y, doi:10.1007/s11661-016-3628-y. This article has 32 citations.

15. (cheng2020corrosionandcorrosive‐wear pages 4-8): Jinjuan Cheng, Zheming Wang, Xue-ping Gan, Qian Lei, Zhou Li, and Kechao Zhou. Corrosion and corrosive‐wear behaviors of a high strength and toughness cu–15ni–8sn alloy in seawater. Materials and Corrosion, 71:593-607, Dec 2020. URL: https://doi.org/10.1002/maco.201911323, doi:10.1002/maco.201911323. This article has 25 citations.

16. (zhong2025enhancingmechanicalstrength pages 10-11): W. Zhong, Liang Wang, Dun Miao, Xiang Cai, Meng-Meng Yang, Yanxin Qiao, Qi-chao Zhang, and Jian Zhou. Enhancing mechanical strength and tribological performance in tin bronze alloys via rolling treatment. npj Materials Degradation, Aug 2025. URL: https://doi.org/10.1038/s41529-025-00655-x, doi:10.1038/s41529-025-00655-x. This article has 4 citations and is from a peer-reviewed journal.

17. (tsao2012corrosioncharacterizationof pages 5-6): L.C. Tsao and C.W. Chen. Corrosion characterization of cu–sn intermetallics in 3.5 wt.% nacl solution. Corrosion Science, 63:393-398, Oct 2012. URL: https://doi.org/10.1016/j.corsci.2012.06.015, doi:10.1016/j.corsci.2012.06.015. This article has 67 citations and is from a highest quality peer-reviewed journal.

18. (nemani2024advancementsinadditive pages 50-53): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

19. (nemani2024advancementsinadditive pages 43-47): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

20. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

21. (valloton2012competitionofthe pages 1-3): J. Valloton, J.-D. Wagnière, and M. Rappaz. Competition of the primary and peritectic phases in hypoperitectic cu-sn alloys solidified at low speed in a diffusive regime. Acta Materialia, 60:3840-3848, May 2012. URL: https://doi.org/10.1016/j.actamat.2012.03.030, doi:10.1016/j.actamat.2012.03.030. This article has 54 citations and is from a highest quality peer-reviewed journal.

22. (valloton2012competitionofthe pages 3-5): J. Valloton, J.-D. Wagnière, and M. Rappaz. Competition of the primary and peritectic phases in hypoperitectic cu-sn alloys solidified at low speed in a diffusive regime. Acta Materialia, 60:3840-3848, May 2012. URL: https://doi.org/10.1016/j.actamat.2012.03.030, doi:10.1016/j.actamat.2012.03.030. This article has 54 citations and is from a highest quality peer-reviewed journal.

23. (sur2025revisitingtheinfluence pages 10-13): Debashish Sur, Nathan C. Smith, Elaf A. Anber, Kaitlyn L. Anderson, Peter F. Connors, Daniel Foley, Mitra L. Taheri, Junsoo Han, Christopher M. Wolverton, and John R. Scully. Revisiting the influence of sn in cu-al alloys: a <i>third element effect</i> enabling stainless steel type corrosion behavior. Journal of The Electrochemical Society, 172(10):101502, Oct 2025. URL: https://doi.org/10.1149/1945-7111/ae0eb6, doi:10.1149/1945-7111/ae0eb6. This article has 6 citations and is from a peer-reviewed journal.

24. (albuquerque2024solidificationpathsof pages 1-5): Sarah de Albuquerque, Guillaume Reinhart, Danielle Cristina Camilo Magalhães, José Eduardo Spinelli, Hadjer Soltani, Wafa Boumechta, Felipe Bertelli, and Henri Nguyen-Thi. Solidification paths of al-cu-sn alloys: comparison of thermodynamic analyses and solidification experiments using in situ x-radiography. Aug 2024. URL: https://doi.org/10.1016/j.mtcomm.2024.109545, doi:10.1016/j.mtcomm.2024.109545. This article has 10 citations and is from a peer-reviewed journal.

25. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

26. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

27. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

28. (earths20122010mineralsyearbook pages 4-4): R EARTHS. 2010 minerals yearbook. Unknown journal, 2012.

29. (sur2025revisitingtheinfluence pages 13-16): Debashish Sur, Nathan C. Smith, Elaf A. Anber, Kaitlyn L. Anderson, Peter F. Connors, Daniel Foley, Mitra L. Taheri, Junsoo Han, Christopher M. Wolverton, and John R. Scully. Revisiting the influence of sn in cu-al alloys: a <i>third element effect</i> enabling stainless steel type corrosion behavior. Journal of The Electrochemical Society, 172(10):101502, Oct 2025. URL: https://doi.org/10.1149/1945-7111/ae0eb6, doi:10.1149/1945-7111/ae0eb6. This article has 6 citations and is from a peer-reviewed journal.

30. (saud2016influenceoftin pages 6-8): Safaa N. Saud, E. Hamzah, T. Abubakar, H. R. Bakhsheshi-Rad, and M. N. Mohammed. Influence of tin additions on the phase-transformation characteristics of mechanical alloyed cu-al-ni shape-memory alloy. Metallurgical and Materials Transactions A, 47:5242-5255, Jul 2016. URL: https://doi.org/10.1007/s11661-016-3628-y, doi:10.1007/s11661-016-3628-y. This article has 32 citations.
