<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: efebb573-f92b-46ef-b3e0-c8dedaf004bb
- Submitted: 2026-10-17T18:59:07Z
- Fetched: 2026-10-17T19:30:39Z (status: success)
- Raw trajectory JSON: ../raw/el-14-Zr.json.gz
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

ELEMENT UNDER REVIEW: Zr (strengthening addition). Cu-Zr C15000 (0.1-0.2 Zr), CuCrZr C18150 (0.05-0.25 Zr); grain refinement of cast aluminum bronze; Zr can be picked up from zirconia crucibles.

Answer for Zr specifically, not for copper alloys in general:
1. ROLE: what Zr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Zr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Zr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Zr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Zr, Cu-Ni-Zr and Cu-Al-Zr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Zr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Zr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Zr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Zr (strengthening addition). Cu-Zr C15000 (0.1-0.2 Zr), CuCrZr C18150 (0.05-0.25 Zr); grain refinement of cast aluminum bronze; Zr can be picked up from zirconia crucibles.

Answer for Zr specifically, not for copper alloys in general:
1. ROLE: what Zr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Zr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Zr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Zr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Zr, Cu-Ni-Zr and Cu-Al-Zr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Zr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Zr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Zr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Zirconium (Zr) as a designed addition to marine copper-alloy DED powder

**Decision: INCLUDE Zr as an exploratory microalloying variable in both the Cu–Ni and aluminum-bronze search spaces, but not as a presumed seawater-corrosion improver.** [CITE][GAP] Copper-alloy casting experiments establish a measurable grain-refinement effect at low Zr contents, commercial Cu–Zr alloys establish practical dilute additions, and infrared-laser powder-bed fusion establishes that a Zr-bearing copper powder can form a dense *as-built* part. None establishes that Zr improves an *as-deposited*, single-stream blown-powder DED alloy relative to wrought C71500 in seawater, or that it prevents cracks at a C95800/Cu–Ni repair interface. The limits below are **proposed experimental-design limits, not Navy-approved chemistry limits**. (m.sadayappan2005grainrefinementof pages 1-8, franczak2020researchofmechanical pages 1-2, xu2024performanceimprovementfor pages 6-9, xu2024performanceimprovementfor pages 2-4)

## 1. Metallurgical role and alloy precedents

[CITE][NUMBERS] In dilute Cu–Zr, Zr has limited high-temperature solubility in the Cu-rich matrix and precipitates on cooling or aging. Cu₅Zr is an established Cu-rich precipitate; Cu–Cr–Zr studies also identify Zr₁₄Cu₅₁. Dispersed precipitates and their interactions with deformation substructure improve thermal stability; this is **not evidence of precipitation hardening in an unaged marine deposit**. A study of Cu–0.15 wt% Zr used induction melting and explicitly investigated aging; a separate account describes Cu–0.15 wt% Zr strengthening as substantially dependent on cold work. (bloom1989rapidsolidificationof pages 44-47, bloom1989rapidsolidificationof pages 75-77, bloom1989rapidsolidificationof pages 77-80, http2007crcuzr(chromiumcopperzirconium) pages 3-4, franczak2020researchofmechanical pages 1-2, franczak2020researchofmechanical pages 2-4)

[CITE][NUMBERS] In permanent-mold casting, Zr can refine brasses and silicon bronzes. The DOE-funded CANMET study found a practical threshold *around* **0.010 wt% added Zr** across its four tested alloys, while reporting measurable refinement in a particular yellow brass after an **0.004 wt% addition**; its authors could not establish the operative nucleation mechanism. Earlier work summarized there reported **0.030 wt% Zr plus 0.020 wt% B** for *iron-free* aluminum bronze, and **0.050 wt% Zr** for gunmetal/red brass. These are casting precedents, **not demonstrations in Fe-bearing C95800 NAB, Cu–Ni, or DED**. Iron already refines many commercial aluminum bronzes, so Zr’s incremental benefit in Fe-bearing NAB needs a Zr-free control. (m.sadayappan2005grainrefinementof pages 8-10, m.sadayappan2005grainrefinementof pages 28-32, m.sadayappan2005grainrefinementof pages 1-8)

[CITE][NUMBERS] In wrought Cu–15 wt% Ni–8 wt% Sn, a review of a Zr-addition series reports that **0.5 wt% Zr**, after processing/aging, gave **980 MPa** tensile strength and **330 HB** hardness. It attributes the response to reduced Sn segregation, changes in precipitate morphology, and suppression of discontinuous precipitation; it reports predominantly solute Zr below **0.1 wt%**, and Ni₅Zr and eventually Ni₄SnZr at higher additions. **This high-Sn, aged alloy is not a stand-in for as-deposited 70–30 Cu–Ni.** Zr has also been discussed as a microalloying addition to Cu–Ni–Si, but a verified marine-service composition and corrosion benefit were not located. (yang2023researchprogresson pages 11-13, yang2023researchprogresson pages 7-10)

[SPEC][GAP] Documented **nonmarine composition precedents**, all in wt%, are commercial Cu–Zr near **0.15 Zr** (identified as C15100 in the retrieved Cu–Zr study), Cu–Cr–Zr in a reported commercial-use range of approximately **0.04–0.10 Zr**, and a successfully printed *experimental* Cu–0.82 Cr–0.48 Zr powder. The contextual C15000 **0.10–0.20 Zr** and C18150 **0.05–0.25 Zr** ranges should **not** be represented here as independently verified ASTM/UNS limits: the retrieved material does not reproduce their controlling composition tables. NARloy-Z, Cu–3 Ag–0.5 Zr, is another *nonmarine* high-temperature example. No verified Zr minimum/maximum was found in the cited marine C71500, C95800, or AWS A5.7 ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl filler specifications. **“Not specified” is not equivalent to “permitted without limit” or “prohibited.”** (bloom1989rapidsolidificationof pages 77-80, franczak2020researchofmechanical pages 1-2, franczak2020researchofmechanical pages 2-4, xu2024performanceimprovementfor pages 2-4)

## 2. Seawater corrosion: what can actually be quantified

[GAP] **No controlled, Zr-only comparison was verified for Cu–Ni, NAB, manganese-aluminum bronze, or their DED repairs in natural seawater, ASTM D1141 water, or 3.5 wt% NaCl.** Consequently there is no defensible Zr-specific beneficial or harmful *seawater* concentration interval, corrosion rate, E_corr shift, impedance/film-resistance improvement, pitting/crevice threshold, selective-attack depth, erosion–corrosion benefit, or flow-velocity limit. In particular, do not transfer corrosion numbers for zirconium-based metallic glasses, Ti–Ni–Zr, or aluminum-base alloys to dilute Cu–Zr. (m.sadayappan2005grainrefinementof pages 72-77, m.sadayappan2005grainrefinementof pages 77-80, ocejo2022corrosionbehaviorof pages 1-3, ocejo2022corrosionbehaviorof pages 10-14)

[CITE][NUMBERS] The closest controlled Zr comparison in the retrieved copper literature is **not a chloride test**. CANMET compared cast silicon bronze without Zr against nominally comparable casts with **0.022–0.024 wt% measured Zr** in **0.05 M phosphate-buffered solutions**, pH 6 or 8. At pH 6, the reported silicon-bronze polarization resistance changed from **1.28 to 1.92 kΩ** and 120-day mass loss from **1.253 to 0.850 mg/cm²** (base versus refined). At pH 8, resistance changed in the *opposite* direction, **3.87 to 3.03 kΩ**, while 120-day mass loss was **0.130 versus 0.110 mg/cm²**. The authors found **no conclusive corrosion advantage** after considering the full dataset. Their separate accelerated dezincification bath contained FeCl₃, CuSO₄, and HCl; neither it nor the phosphate bath is seawater. Their yellow-brass specimens were B-refined, not a Zr-on/Zr-off comparison. (m.sadayappan2005grainrefinementof pages 72-77, m.sadayappan2005grainrefinementof pages 80-84, m.sadayappan2005grainrefinementof pages 84-92, m.sadayappan2005grainrefinementof pages 77-80)

[CITE] As a *Zr-free comparator for failure-mode selection*, NAB/MAB exposures in simulated seawater identify selective β-phase attack and sensitivity to phase distribution; the reported experimental NAB and MAB compositions do not vary Zr. A separate NAB investigation found that **0.012 wt% Ti** refined grains without significantly changing measured corrosion (**0.021 versus 0.023 mm/year**), illustrating why grain refinement alone cannot establish Zr-mediated protection. Neither study demonstrates Zr-bearing protective oxide, suppressed dealuminification/dezincification, or seawater-film improvement. (ocejo2022corrosionbehaviorof pages 1-3, ocejo2022corrosionbehaviorof pages 14-15, rivero2021effectofti pages 6-8, rivero2021effectofti pages 1-2)

## 3. DED, welding, and repair interfaces

[CITE][NUMBERS] The strongest directly retrieved laser precedent is **powder-bed fusion, not blown-powder DED**: Xu *et al.* printed gas-atomized **Cu–0.82 Cr–0.48 Zr wt%** using a **1064-nm** laser, argon with chamber oxygen below **100 ppm**, substrate preheat of **170 °C**, and an in-process layer-remelting strategy. Reported optimized relative density was **99.8%** versus **98.9%** without remelting; remelted material achieved **329 MPa** tensile strength without *post-build* heat treatment. In-process remelting, substrate choice, and laser thermal history make those results unsuitable as evidence that the proposed single-pass, single-stream Cu–Ni/NAB repair will be dense or crack-free. (xu2024performanceimprovementfor pages 4-6, xu2024performanceimprovementfor pages 6-9, xu2024performanceimprovementfor pages 1-2, xu2024performanceimprovementfor pages 2-4)

[GAP] No verified experiment isolates Zr’s effects on **DED solidification cracking, remelted-layer liquation cracking, gas/oxide porosity, laser-induced Zr loss**, or dilution into cast C95800 versus wrought C71500. The Cu-rich eutectic and strong Zr affinity for other alloying elements give *testable concerns*: interdendritic Zr-rich material might supply a low-melting boundary film on reheating, whereas adequate retained Zr and effective nuclei might favor equiaxed solidification. Neither direction is quantified for these repairs. Evaluate first-layer dilution and later-layer reheating separately, and inspect crack/porosity area fractions and boundary chemistry; do not label a standard ERCuNi/ERCuNiAl filler as a Zr-bearing repair demonstration without its certified analysis. (bloom1989rapidsolidificationof pages 44-47, http2007crcuzr(chromiumcopperzirconium) pages 3-4, m.sadayappan2005grainrefinementof pages 8-10, xu2024performanceimprovementfor pages 6-9, xu2024performanceimprovementfor pages 2-4)

## 4. Atomization and phase-diagram constraints

[CITE][NUMBERS] **Retained Zr, not charged Zr, is the design variable.** In induction-melted EnviroBrass III, CANMET observed useful grain refinement with **0.002–0.040 wt% Zr additions**, but reported approximately **50% Zr loss on melting or holding for an hour**, attributed principally to oxidation; refinement could fade within an hour. This is a copper-casting warning, not a measured loss factor for the argon-shielded rePOWDER system. Charge with a characterized Cu–Zr master alloy, measure Zr/O before and after atomization and after DED, and screen powder for oxide inclusions; a purely stoichiometric overcharge cannot substitute for these measurements. (m.sadayappan2005grainrefinementof pages 32-37, m.sadayappan2005grainrefinementof pages 23-28, m.sadayappan2005grainrefinementof pages 1-8)

[GAP] No source retrieved here quantifies **Zr pickup from a ZrO₂ crucible**, its reaction rate with Al₂O₃ or graphite, or Zr exchange with a Ti-alloy or Mo ultrasonic sonotrode in this copper melt. Zirconia therefore poses a possible *background-contamination confounder*, not an established Zr feedstock; separately blank-test Al₂O₃ and ZrO₂ crucibles and assay Zr, O, Ti, Mo, and C. Zr oxidation/inclusion formation is supported by the casting observations; claims of substantial Zr *vaporization* or a numerical Zr-dependent liquid surface-tension change at 1.07 µm are **not established** by the retrieved evidence. (m.sadayappan2005grainrefinementof pages 32-37, m.sadayappan2005grainrefinementof pages 1-8, xu2024performanceimprovementfor pages 2-4)

[CITE][NUMBERS] Published estimates of the **maximum equilibrium Zr solubility in Cu** disagree: roughly **0.11 wt% at 950 °C** in a Cu–Cr–Zr assessment; Cu–Zr studies report **<0.13 wt% at 940 °C**, approximately **0.15 wt% at 980 °C**, and a fitted **0.24 wt% at 980 °C**. Treat **approximately 0.1–0.2 wt% near 950–980 °C** as a working bracket, **not** a universal solubility limit in Cu–Ni or Cu–Al. Cu-rich invariant/eutectic temperatures are reported around **966–980 °C** (approximately **963 °C** for one Cu–Cr–Zr ternary eutectic); Cu₅Zr and Zr₁₄Cu₅₁ must be considered when assessing segregation. A Cu-rich eutectic does **not** justify asserting that dilute Zr by itself drives copper’s liquidus above **1,250 °C**; conversely, it does not certify the liquidus of a Ni/Al/Fe/Mn-rich candidate. Require a full-composition liquidus calculation and a measured meltability check, with useful superheat below the apparatus limit. (bloom1989rapidsolidificationof pages 44-47, http2007crcuzr(chromiumcopperzirconium) pages 1-3, http2007crcuzr(chromiumcopperzirconium) pages 3-4, http2007crcuzr(chromiumcopperzirconium) pages 13-15)

[CITE][GAP] Published Cu–Zr thermodynamic/phase assessments and Cu–Cr–Zr assessments exist, and published work treats Cu–Ni–Zr-related thermodynamics; the retrieved material **does not establish** an assessed, experimentally validated **Cu-rich Cu–Ni–Zr or Cu–Al–Zr ternary** usable in the local **TCCU** release, nor that **COST 531** contains the required marine-alloy descriptions. Check actual database element lists and phase availability, inspect invariant/solidification predictions against experimental compositions, and record version and parameter provenance before using a pycalphad TDB as a design constraint. Binary availability alone does not validate Zr interactions with NAB κ/β phases. (http2007crcuzr(chromiumcopperzirconium) pages 1-3, http2007crcuzr(chromiumcopperzirconium) pages 3-4, kulikova2017chemicalinteractionand pages 3-6, kulikova2017chemicalinteractionand pages 1-3)

## 5. Supply, safety, bounds, and interactions

[CITE][NAVY] **Zr was on the U.S. 2022 critical-minerals list and remains on the November 2025 final list; copper joined the 2025 list.** The later list identifies Zr supply-chain single-point-of-failure concerns. Critical-mineral designation does not itself prohibit Navy use; no Zr-specific Navy prohibition, RoHS/REACH restriction applicable to these bulk alloys, or certified purchase price for the required Cu–Zr master alloy was verified. **Price per kg: not reliably established; obtain a dated supplier quote rather than treating zircon mineral-concentrate prices as metallic Zr powder/master-alloy prices.** (iii2026usgscriticalminerals pages 1-2, iii2026usgscriticalmineralsa pages 1-2, hartmann2022draftcriticalminerals pages 13-15)

[CITE][NUMBERS] Fine **elemental Zr** powder poses ignition/deflagration hazards: published measurements report a **1–3 mJ minimum ignition energy** for tested Zr dust, with sensitivity increasing as particle size decreases. These measurements must **not** be assigned unchanged to pre-alloyed Cu powder containing ≤0.5 wt% Zr. Segregated fines, unmelted Zr charge, and collected laser/atomizer fume nevertheless merit inert handling, combustible-dust assessment, local exhaust/HEPA capture, and appropriate metal-fire procedures. No verified Zr-specific OSHA permissible-exposure value was obtained here; apply the current material-specific exposure limits and rules for accompanying Cu/Ni fume after checking authoritative OSHA documents and the actual SDS. (xiong2020studyonthe pages 1-2, reding2018metaldustexplosion pages 1-2)

**Proposed composition bounds, Zr wt% in finished alloy, Cu as balance:**

| Bound | Both-family design value | Evidentiary basis and bound-setting failure mode |
|---|---:|---|
| **Functional floor** | **0.010** | Approximate reproducible grain-refinement threshold in *cast brasses/silicon bronze*; **0.004** was detectable in one brass, but is less robust. Oxidation/poor retention may leave too little active Zr, particularly for NAB or Cu–Ni, where the floor is unvalidated. (m.sadayappan2005grainrefinementof pages 28-32, m.sadayappan2005grainrefinementof pages 1-8) |
| **Conservative maximum** | **0.15** | Near the established dilute commercial Cu–Zr composition and upper end of several reported Cu-rich solubility measurements; **not** a marine specification or demonstrated as-deposited strengthening limit. Boundary/interdendritic Zr phases, oxidation, and unverified seam corrosion govern screening. (bloom1989rapidsolidificationof pages 44-47, bloom1989rapidsolidificationof pages 73-75, franczak2020researchofmechanical pages 1-2) |
| **Non-conservative maximum** | **0.50** | Experimental Cu–Ni–Sn strengthening at **0.5**, NARloy-Z at **0.5**, and LPBF Cu–Cr–Zr powder at **0.48** provide *process/alloy precedents*, **not** marine DED validation. Ni₅Zr/Ni₄SnZr or Cu–Zr boundary phases, oxide inclusions, and possible reheating cracks set the aggressive stop; the complete alloy must also satisfy its measured liquidus/superheat constraint. (bloom1989rapidsolidificationof pages 77-80, xu2024performanceimprovementfor pages 2-4, yang2023researchprogresson pages 11-13) |

[CITE][GAP] **Joint constraints to carry forward:** assess *retained* Zr versus O and hold time; test Zr × B and Zr × Fe for whether grain refinement adds anything beyond Fe-bearing NAB; track S (historically reported to poison Zr refinement), Mg if used to protect Zr in casting, and possible Zr–Si reactions. Where Ni and Sn are substantial, distinguish Cu₅Zr from **Ni₅Zr/Ni₄SnZr** and Sn segregation before applying the 0.50-wt% precedent to Cu–Ni repair. No defensible universal **Zr/Ni, Zr/Fe, Zr/Mn, or Zr/Al numerical ratio** was verified, and Zr does not substitute for demonstrating a favorable α/β/κ balance or corrosion film in Fe-bearing NAB. (m.sadayappan2005grainrefinementof pages 8-10, m.sadayappan2005grainrefinementof pages 23-28, yang2023researchprogresson pages 11-13, ocejo2022corrosionbehaviorof pages 1-3)

**Evidence grade: thin for the proposal’s decisive endpoint.** Copper-casting refinement, Cu–Zr phase behavior, and Cu–Cr–Zr laser processing are documented, but the crucial Zr-controlled comparisons of **as-deposited** marine corrosion, cast-NAB/wrought-Cu–Ni repair-interface integrity, and Zr mass balance across this atomizer and DED system remain unreported in the evidence located. The non-conservative bound is therefore an experimental screening ceiling, **not** a seawater-safe range. (m.sadayappan2005grainrefinementof pages 1-8, m.sadayappan2005grainrefinementof pages 84-92, xu2024performanceimprovementfor pages 6-9, ocejo2022corrosionbehaviorof pages 1-3)

**Principal traceable sources:** Sadayappan *et al.*, *Grain Refinement of Permanent Mold Cast Copper Base Alloys*, CANMET/US DOE report MTL 2004-6, DOI **10.2172/840819**; Franczak *et al.*, *Archives of Civil and Mechanical Engineering* **20** (2020), DOI **10.1007/s43452-020-00035-z**; MSIT, “Cr–Cu–Zr,” *Landolt–Börnstein* (2007), DOI **10.1007/978-3-540-47000-7_19**; Xu *et al.*, *Materials* **17**, 624 (2024), DOI **10.3390/ma17030624**; Yang *et al.*, *Materials* **16**, 5913 (2023), DOI **10.3390/ma16175913**; Ocejo *et al.*, *Metals* **12**, 380 (2022), DOI **10.3390/met12030380**; Xiong *et al.*, *Journal of Hazardous Materials* **387**, 122009 (2020), DOI **10.1016/j.jhazmat.2019.122009**. Standards and AWS designations mentioned above were **not independently verified for Zr chemistry**; an invented DOI or composition limit would be misleading. (m.sadayappan2005grainrefinementof pages 1-8, franczak2020researchofmechanical pages 1-2, http2007crcuzr(chromiumcopperzirconium) pages 1-3, xu2024performanceimprovementfor pages 2-4, yang2023researchprogresson pages 11-13, ocejo2022corrosionbehaviorof pages 1-3, xiong2020studyonthe pages 1-2)

VERDICT | Zr | decision=INCLUDE | family=both | conservative_max_wt=0.15 | nonconservative_max_wt=0.50 | floor_wt=0.010 | impurity_max_wt=NA | evidence=thin

References

1. (m.sadayappan2005grainrefinementof pages 1-8): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

2. (franczak2020researchofmechanical pages 1-2): Krystian Franczak, Paweł Kwaśniewski, Grzegorz Kiesiewicz, Małgorzata Zasadzińska, Bartosz Jurkiewicz, Paweł Strzępek, and Zbigniew Rdzawski. Research of mechanical and electrical properties of cu–sc and cu–zr alloys. Archives of Civil and Mechanical Engineering, Feb 2020. URL: https://doi.org/10.1007/s43452-020-00035-z, doi:10.1007/s43452-020-00035-z. This article has 31 citations.

3. (xu2024performanceimprovementfor pages 6-9): Lianyong Xu, Yaqing Zhang, Lei Zhao, Wenjing Ren, and Yongdian Han. Performance improvement for the cucrzr alloy produced by laser powder bed fusion using the remelting process. Materials, 17:624, Jan 2024. URL: https://doi.org/10.3390/ma17030624, doi:10.3390/ma17030624. This article has 12 citations.

4. (xu2024performanceimprovementfor pages 2-4): Lianyong Xu, Yaqing Zhang, Lei Zhao, Wenjing Ren, and Yongdian Han. Performance improvement for the cucrzr alloy produced by laser powder bed fusion using the remelting process. Materials, 17:624, Jan 2024. URL: https://doi.org/10.3390/ma17030624, doi:10.3390/ma17030624. This article has 12 citations.

5. (bloom1989rapidsolidificationof pages 44-47): TA Bloom. Rapid solidification of high-conductivity copper alloys. Unknown journal, 1989.

6. (bloom1989rapidsolidificationof pages 75-77): TA Bloom. Rapid solidification of high-conductivity copper alloys. Unknown journal, 1989.

7. (bloom1989rapidsolidificationof pages 77-80): TA Bloom. Rapid solidification of high-conductivity copper alloys. Unknown journal, 1989.

8. (http2007crcuzr(chromiumcopperzirconium) pages 3-4): Materials Science International Team MSIT® http. Cr-Cu-Zr (Chromium-Copper-Zirconium), pages 228-242. Springer Berlin Heidelberg, Jan 2007. URL: https://doi.org/10.1007/978-3-540-47000-7\_19, doi:10.1007/978-3-540-47000-7\_19. This article has 3 citations.

9. (franczak2020researchofmechanical pages 2-4): Krystian Franczak, Paweł Kwaśniewski, Grzegorz Kiesiewicz, Małgorzata Zasadzińska, Bartosz Jurkiewicz, Paweł Strzępek, and Zbigniew Rdzawski. Research of mechanical and electrical properties of cu–sc and cu–zr alloys. Archives of Civil and Mechanical Engineering, Feb 2020. URL: https://doi.org/10.1007/s43452-020-00035-z, doi:10.1007/s43452-020-00035-z. This article has 31 citations.

10. (m.sadayappan2005grainrefinementof pages 8-10): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

11. (m.sadayappan2005grainrefinementof pages 28-32): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

12. (yang2023researchprogresson pages 11-13): Shaodan Yang, Kexing Song, Yanjun Zhou, Ran Yang, Yan Yu, Lele Liu, Jidong Chen, Fei Zhou, Wenhao Yang, Guoshang Zhang, and Juan Du. Research progress on cu–15ni–8sn alloys: the effect of microalloying and heat treatment on microstructure and properties. Materials, 16:5913, Aug 2023. URL: https://doi.org/10.3390/ma16175913, doi:10.3390/ma16175913. This article has 40 citations.

13. (yang2023researchprogresson pages 7-10): Shaodan Yang, Kexing Song, Yanjun Zhou, Ran Yang, Yan Yu, Lele Liu, Jidong Chen, Fei Zhou, Wenhao Yang, Guoshang Zhang, and Juan Du. Research progress on cu–15ni–8sn alloys: the effect of microalloying and heat treatment on microstructure and properties. Materials, 16:5913, Aug 2023. URL: https://doi.org/10.3390/ma16175913, doi:10.3390/ma16175913. This article has 40 citations.

14. (m.sadayappan2005grainrefinementof pages 72-77): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

15. (m.sadayappan2005grainrefinementof pages 77-80): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

16. (ocejo2022corrosionbehaviorof pages 1-3): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

17. (ocejo2022corrosionbehaviorof pages 10-14): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

18. (m.sadayappan2005grainrefinementof pages 80-84): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

19. (m.sadayappan2005grainrefinementof pages 84-92): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

20. (ocejo2022corrosionbehaviorof pages 14-15): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

21. (rivero2021effectofti pages 6-8): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

22. (rivero2021effectofti pages 1-2): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

23. (xu2024performanceimprovementfor pages 4-6): Lianyong Xu, Yaqing Zhang, Lei Zhao, Wenjing Ren, and Yongdian Han. Performance improvement for the cucrzr alloy produced by laser powder bed fusion using the remelting process. Materials, 17:624, Jan 2024. URL: https://doi.org/10.3390/ma17030624, doi:10.3390/ma17030624. This article has 12 citations.

24. (xu2024performanceimprovementfor pages 1-2): Lianyong Xu, Yaqing Zhang, Lei Zhao, Wenjing Ren, and Yongdian Han. Performance improvement for the cucrzr alloy produced by laser powder bed fusion using the remelting process. Materials, 17:624, Jan 2024. URL: https://doi.org/10.3390/ma17030624, doi:10.3390/ma17030624. This article has 12 citations.

25. (m.sadayappan2005grainrefinementof pages 32-37): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

26. (m.sadayappan2005grainrefinementof pages 23-28): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

27. (http2007crcuzr(chromiumcopperzirconium) pages 1-3): Materials Science International Team MSIT® http. Cr-Cu-Zr (Chromium-Copper-Zirconium), pages 228-242. Springer Berlin Heidelberg, Jan 2007. URL: https://doi.org/10.1007/978-3-540-47000-7\_19, doi:10.1007/978-3-540-47000-7\_19. This article has 3 citations.

28. (http2007crcuzr(chromiumcopperzirconium) pages 13-15): Materials Science International Team MSIT® http. Cr-Cu-Zr (Chromium-Copper-Zirconium), pages 228-242. Springer Berlin Heidelberg, Jan 2007. URL: https://doi.org/10.1007/978-3-540-47000-7\_19, doi:10.1007/978-3-540-47000-7\_19. This article has 3 citations.

29. (kulikova2017chemicalinteractionand pages 3-6): T. Kulikova, A. Maiorova, V. Bykov, and K. Shunyaev. Chemical interaction and thermodynamic properties of (cu,ni)-zr glass-forming alloys. The European Physical Journal Special Topics, 226:1097-1106, Apr 2017. URL: https://doi.org/10.1140/epjst/e2016-60212-x, doi:10.1140/epjst/e2016-60212-x. This article has 8 citations.

30. (kulikova2017chemicalinteractionand pages 1-3): T. Kulikova, A. Maiorova, V. Bykov, and K. Shunyaev. Chemical interaction and thermodynamic properties of (cu,ni)-zr glass-forming alloys. The European Physical Journal Special Topics, 226:1097-1106, Apr 2017. URL: https://doi.org/10.1140/epjst/e2016-60212-x, doi:10.1140/epjst/e2016-60212-x. This article has 8 citations.

31. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

32. (iii2026usgscriticalmineralsa pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

33. (hartmann2022draftcriticalminerals pages 13-15): Thomas Hartmann, Stuart Maloy, and Isabella Johanna van Rooyen. Draft critical minerals evaluation report: advanced materials and manufacturing technology. ArXiv, Sep 2022. URL: https://doi.org/10.2172/2478110, doi:10.2172/2478110. This article has 3 citations.

34. (xiong2020studyonthe pages 1-2): Xinyu Xiong, Qiuping Xiao, Jian Zhou, Yongxu Wang, Bin Li, and Lifeng Xie. Study on the effect of simulated nuclear industry working conditions on the explosion severity parameters of zirconium powder and the explosion mechanism. Apr 2020. URL: https://doi.org/10.1016/j.jhazmat.2019.122009, doi:10.1016/j.jhazmat.2019.122009. This article has 16 citations and is from a highest quality peer-reviewed journal.

35. (reding2018metaldustexplosion pages 1-2): Nicholas S. Reding and Mark B. Shiflett. Metal dust explosion hazards: a technical review. Industrial & Engineering Chemistry Research, 57:11473-11482, Aug 2018. URL: https://doi.org/10.1021/acs.iecr.8b02465, doi:10.1021/acs.iecr.8b02465. This article has 55 citations and is from a peer-reviewed journal.

36. (bloom1989rapidsolidificationof pages 73-75): TA Bloom. Rapid solidification of high-conductivity copper alloys. Unknown journal, 1989.
