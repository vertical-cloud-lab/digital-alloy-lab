<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 2ff874ec-9ef6-4f9f-934a-0ac59cc3b0bb
- Submitted: 2026-10-17T18:58:37Z
- Fetched: 2026-10-17T19:30:27Z (status: success)
- Raw trajectory JSON: ../raw/el-04-Fe.json.gz
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

ELEMENT UNDER REVIEW: Fe (major seawater addition). Cu-Ni: 1.0-1.8 Fe in C70600, 0.4-1.0 in C71500, 1.7-2.3 in C71640; NAB: about 2-5 Fe (kappa phases). Fe controls the protective film and erosion-corrosion resistance of Cu-Ni, but Fe out of solid solution harms it. Dilution from steel substrates adds Fe.

Answer for Fe specifically, not for copper alloys in general:
1. ROLE: what Fe does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Fe ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Fe changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Fe, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Fe, Cu-Ni-Fe and Cu-Al-Fe are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Fe in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Fe neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Fe | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Fe (major seawater addition). Cu-Ni: 1.0-1.8 Fe in C70600, 0.4-1.0 in C71500, 1.7-2.3 in C71640; NAB: about 2-5 Fe (kappa phases). Fe controls the protective film and erosion-corrosion resistance of Cu-Ni, but Fe out of solid solution harms it. Dilution from steel substrates adds Fe.

Answer for Fe specifically, not for copper alloys in general:
1. ROLE: what Fe does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Fe ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Fe changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Fe, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Fe, Cu-Ni-Fe and Cu-Al-Fe are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Fe in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Fe neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Fe | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Fe in pre-alloyed powders for marine laser DED

**Decision — INCLUDE Fe as a designed addition in both Cu–Ni and Al-bronze compositions.** Its demonstrated seawater function in Cu–Ni depends strongly on *Fe remaining available in the Cu–Ni matrix*; in nickel-aluminum bronze (NAB), Fe instead contributes to strengthening Fe–Al-rich κ phases. These are different design regimes, not a single optimum Fe concentration. Evidence supports a **5.0 wt% conservative palette ceiling**, applicable to NAB-type compositions, but **not** to an otherwise conventional Cu–Ni composition. A proposed **6.0 wt% exploratory ceiling** for Al bronze is a *screening hypothesis*, not a demonstrated seawater- or DED-qualified composition. No cited study establishes that an as-deposited alloy at either ceiling meets the requested C71500 corrosion benchmark. [CITE] (kievits1972researchintothe pages 1-2, kievits1972researchintothe pages 3-4, ocejo2022corrosionbehaviorof pages 1-3, li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14)

## 1. Role, alloy families, and specifications

- **Cu–Ni:** Fe in solid solution promotes formation of a more protective Cu₂O-based seawater film incorporating Fe and Ni; the proposed mechanism is reduced ionic/electronic transport through the film. Fe also improves resistance to flow impingement. Fe–Ni-rich segregation or precipitation can consume matrix Fe and increase pitting susceptibility. Kievits and IJsseling identified a precipitate analyzing approximately **Cu 51, Ni 31, Fe 17 wt%**; they did **not** find detectable Fe–Ni precipitates in one **1.5 wt% Fe** CuNi10 specimen. Thus *total Fe* alone is an inadequate acceptance measure. [CITE][NUMBERS] (kievits1972researchintothe pages 3-4, kievits1972researchintothe pages 4-5, kievits1972researchintothe pages 2-3, lewis1981evaluationofcoppernickel pages 48-55)
- **NAB and Mn–Al bronze:** Fe is a κ-phase former and contributor to grain/phase refinement and strength, not principally the dissolved-Fe seawater-film addition invoked for Cu–Ni. Fe–Al-rich κI/κII are described as Fe₃Al-related; Ni–Al-rich κ phases contain NiAl, while Mn–Al bronze can contain Fe–Mn-rich κ. Direct laser-DED examination of nominal **Cu–9Al–5Fe–5Ni wt%** found nanoscale Fe₃Al and NiAl precipitates in an as-deposited α/β* microstructure. κ morphology, retained β, and local galvanic behavior complicate corrosion: more Fe-containing κ is *not* automatically better. [CITE] (ocejo2022corrosionbehaviorof pages 8-10, ocejo2022corrosionbehaviorof pages 5-8, berlangalabari2025theeffectof pages 4-7, li2021nanotwinscontainingmicrostructureand pages 14-19)
- **Other requested families:** The retrieved material does not demonstrate a beneficial *designed* Fe addition for seawater-service tin bronze/gunmetal, brasses, Cu–Ni–Sn, or Cu–Ni–Si, nor an Fe-specific dezincification-inhibition or deoxidation mechanism for those families. Do not transfer the Cu–Ni film rationale to them. Fe-containing silicides or Fe–Ni phases remain plausible joint-composition issues, not established seawater benefits in these families. [GAP] (kievits1972researchintothe pages 2-3, nemani2024advancementsinadditive pages 102-105, nemani2024advancementsinadditive pages 112-113)

**[SPEC][NAVY] Source-supported Fe contents, all wt%, Cu balance unless otherwise indicated:** CuNi10Fe/C70600-type **1.0–1.8 Fe**, with **9.0–11.0 Ni** and **0.5–1.0 Mn**; CuNi30Fe/C71500-type **0.4–1.0 Fe**, with **30.0–32.0 Ni** and **0.5–1.5 Mn**. These are historical published grade ranges; the current controlled editions of **ASTM B111, B171 and B466**, and **MIL-T-16420** were *not* independently inspected here. A measured C71500 WAAM repair wire contained **0.55 Fe**, and its C71500 plate **0.56 Fe**. Studied cast CuAl10Fe5Ni5/NAB contained **4.92 Fe** and **4.57 Ni**; a studied Mn–Al bronze contained **3.82 Fe**, **2.21 Ni**, and **12.50 Mn**. Laser-DED NAB powder nominally contained **5 Fe**, with particle-analysis mean **5.48 ± 0.86 Fe**. These measured compositions are **not** substitutes for verifying current **ASTM B148/B369**, **MIL-B-24480**, **MIL-C-15726**, **EN 12449**, UNS C71640 or **AWS A5.7** filler limits; in particular, the supplied **1.7–2.3 Fe** range for C71640 and exact Fe limits for **ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl** remain unverified against specification text. [GAP] (kievits1972researchintothe pages 1-2, ocejo2022corrosionbehaviorof pages 1-3, li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 4-9, song2024microstructuresandcorrosion pages 2-5)

The directly comparable evidence is summarized below. **“Better WAAM corrosion” in the last row is not an Fe-addition experiment:** wire and wrought substrate have essentially the same Fe. (song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 2-5)

| Family and alloy evidence | Fe (wt%) | Method | Measured seawater or chloride result | Limitation for Fe causality |
|---|---:|---|---|---|
| Cu–Ni, C71500 / CuNi30Fe commercial range | 0.4–1.0 | Source-reported commercial range; not independently verified against the current ASTM B111 or B466 text (kievits1972researchintothe pages 1-2) | Historical low-velocity seawater rates were 0.3–0.5 mpy in quiet water and 0.5–0.7 mpy at 0.61 m/s. The reported accepted design velocity was 4.6 m/s for C71500 containing about 0.5 Fe (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48) | Alloy-level benchmark, not a controlled Fe series; Ni, Mn, processing, and film age also differ. |
| Cu–Ni, C70600 / CuNi10Fe commercial range | 1.0–1.8 | Source-reported commercial range; not independently verified against the current ASTM B111 or B466 text (kievits1972researchintothe pages 1-2) | Historical low-velocity seawater rates were 0.2–0.6 mpy in quiet water and 0.5–1.1 mpy at 0.61 m/s. The reported accepted design velocity was 3.6 m/s for C70600 containing about 1.4 Fe (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48) | Alloy-level benchmark. Solid-solution Fe improves impingement resistance, whereas Fe–Ni-rich precipitation can increase pitting susceptibility (kievits1972researchintothe pages 3-4, kievits1972researchintothe pages 2-3). |
| Cast NAB, studied CuAl10Fe5Ni5 / C95800-type composition | 4.92 measured | Foundry analysis; as-cast material was compared with quenching at 850 °C and quench-plus-temper treatment at 600 °C (ocejo2022corrosionbehaviorof pages 1-3) | In simulated seawater, susceptibility ranked T2 greater than as-received greater than T1. Selective attack was governed principally by retained and distributed β phase; a sharp passive-to-active transition occurred between −150 and −100 mV SCE (ocejo2022corrosionbehaviorof pages 1-3, ocejo2022corrosionbehaviorof pages 8-10) | Fe was unchanged; this demonstrates seawater service near 5 Fe and heat-history sensitivity, not an isolated Fe effect. |
| Laser-DED NAB, Cu–9Al–5Fe–5Ni | 5 nominal; 5.48 ± 0.86 measured in powder | Pre-alloyed gas-atomized powder, 45–106 µm; infrared laser metal deposition under Ar/He. Optimized builds exceeded 99% relative density and reached 99.55%; excessive power caused hot cracks, while insufficient energy caused lack-of-fusion pores (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14) | No seawater test was reported. As-deposited phases included β-star martensite, Widmanstätten α, Fe3Al and NiAl nanoprecipitates, and trace Cu2O and CuO (li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 9-14) | Strong direct processability evidence near 5 Fe, but no controlled Fe series or as-deposited seawater comparison with C71500. |
| WAAM 70/30 Cu–Ni | 0.55 wire; 0.56 substrate plate | CMT wire-arc DED using TECHALLOY 413 wire on C71500 plate; no pores or macro- or microscopic cracks were observed (song2024microstructuresandcorrosion pages 2-5) | In naturally aerated 3.5 wt% NaCl, the best WAAM sample had film resistance of 1.40 × 10⁵ Ω on XY and 1.66 × 10⁵ Ω on YZ, versus 1.08 × 10⁵ and 1.18 × 10⁵ Ω for wrought material. Ni-depleted interdendritic regions were preferentially attacked (song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 10-13) | Fe was essentially unchanged between wire and substrate; performance depended on deposition condition, orientation, film, and Ni segregation, not demonstrably on Fe. |


*Table: Directly compares sourced Fe contents with marine-corrosion and additive-manufacturing observations. It distinguishes composition ranges from measured analyses and identifies where unchanged Fe prevents causal attribution.*

## 2. Quantitative seawater evidence and the harmful regime

**[CITE][NUMBERS] Cu–Ni film chemistry and Fe partitioning.** After **six months of flowing seawater**, an approximately **11.6 Ni–1.05 Fe** alloy with only **0.08 wt% precipitated Fe** developed a reported film analyzing **15 wt% Fe**; an approximately **11.3 Ni–1.99 Fe** alloy with **1.84 wt% precipitated Fe** yielded a film with only **4.3 wt% Fe**. The comparator with **11.8 Ni and <0.05 Fe** had no reported film Fe. These are historical film analyses, *not* controlled modern EIS measurements, and support tracking precipitated Fe separately from bulk Fe. Kievits and IJsseling report the opposing tendencies that added Fe improves impingement resistance but can worsen pitting when metallurgical distribution is unfavorable. A separate published **70Cu–30Ni–xFe–1Mn wt%** series tested **x = 0.4, 0.6, 0.8, 1.0** and judged **1.0 Fe** best for its corrosion-product film; its retrieved full-text file was misidentified, so numerical impedance or corrosion rates from that study cannot responsibly be quoted. [GAP] (kievits1972researchintothe pages 2-3, kievits1972researchintothe pages 3-4, lewis1981evaluationofcoppernickel pages 48-55)

**[CITE][NUMBERS] Service benchmarks, not isolated Fe effects.** Historical quiet-seawater rates were **0.2–0.6 mil/year** for C70600 and **0.3–0.5 mil/year** for C71500; at **0.61 m/s**, respectively **0.5–1.1** and **0.5–0.7 mil/year**. Reported accepted *tube design* velocities were **3.6 m/s** for C70600 at approximately **1.4 Fe** and **4.6 m/s** for C71500 at approximately **0.5 Fe**. Separate reported critical velocities were **4.5 m/s** for C70600 at **27 °C** and **4.1 m/s** for C71500 at **12 °C**: do not equate critical velocities with design ratings or extrapolate either to unfilmed 30-day DED coupons. Historical one-year C71500 crevice attack ranged from **nil to 0.006 inch** under no flow, versus **nil to 0.003 inch** at **0.61 m/s**; Fe was not varied in that comparison. [CITE][NUMBERS] (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48)

**[CITE][NUMBERS] As-deposited comparator:** Song *et al.* used WAAM **30 Ni–0.55 Fe–0.70 Mn** wire on a wrought **30.46 Ni–0.56 Fe–0.73 Mn** plate. After **3 h** in naturally aerated **3.5 wt% NaCl**, the best build's fitted film resistances were **1.40 × 10⁵ Ω (XY)** and **1.66 × 10⁵ Ω (YZ)**, against wrought **1.08 × 10⁵** and **1.18 × 10⁵ Ω** under their fixture and fit; **sample 1 underperformed** wrought. The source reports Ω, not normalized Ω·cm². Ni-depleted interdendritic regions were preferentially attacked, and potential/film performance depended on build orientation and process settings. These data establish feasibility near **0.55 Fe** without a post-build treatment, **not** that adding Fe caused the improvement or that the user’s immersion/depth criterion is met. (song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 2-5)

**[CITE][NUMBERS] Al-bronze caution:** In **3.5 wt% NaCl at 25 °C**, a fixed-composition as-cast C95800 study estimated **0.02 mm/year** from polarization at stagnant conditions and **0.06 mm/year** at **9000 rpm**; heat-treated counterparts gave **0.01** and **0.05 mm/year**. As-cast *E*corr shifted from **−262 to −278 mV** over that rotation range; the study attributes differences principally to flow and β-phase redistribution, **not varying Fe**. In a different NAB/Mn–Al-bronze sliding study, static corrosion was approximately **0.02 mm/year**, rising toward **0.1 mm/year** under wear; its electrolyte was **1 M NaCl**, *not* ASTM D1141 seawater. As-printed **4.6 Fe** LPBF NAB reportedly lost approximately one order of magnitude less mass after **3 and 6 months’ seawater immersion** than cast/wrought counterparts, but the result compares *microstructures*, not a Fe series or blown-powder DED. [GAP] (jafari2021effectoffluid pages 7-8, berlangalabari2025theeffectof pages 4-7, nemani2024advancementsinadditive pages 74-79)

## 3. Laser DED, repair dilution, and powder making

**[CITE][NUMBERS] Direct laser-DED evidence exists for NAB, not for an Fe sweep.** Li *et al.* deposited pre-alloyed nominal **Cu–9Al–5Fe–5Ni wt%** powder with **1000–1500 W** and optimized to **>99%** relative density, reaching **99.55%**. Excess laser power produced **large hot cracks in tracks**; insufficient energy caused lack-of-fusion pores and layer delamination; other settings left gas pores. The authors detected trace **Cu₂O/CuO**. Their powder was *commercial gas-atomized* and their carrier/protection included **He**, unlike the proposed in-house ultrasonic powder and Ar-only DED. Neither their hot cracks nor pores were shown to be **caused by Fe**. [GAP] (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14)

**[CITE] Repair-interface risk:** Wire-arc NAB on **316L steel** produced reported Cu penetration and intergranular liquation cracks on the *steel* heat-affected side; a lower-energy study reported no such cracks. This is a warning about Fe-rich *steel dilution and interface heat input*, **not proof that cast NAB or wrought Cu–Ni repair cracks in the same way**. NAB dilution can introduce Al/Ni/Fe and alter β/κ distributions at a Cu–Ni repair interface; Cu–Ni dilution into NAB can conversely lower local Al/Fe. Inspect first-layer composition, fusion boundary and reheated-layer HAZ separately. The identified NAB-on-steel Fe₃Al interface is not evidence of Fe-specific porosity or a quantified tolerable steel-dilution percentage. [GAP] (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 112-113)

**[GAP] Powder-making and laser losses:** Fe-bearing Al-bronze melt and powder should be checked for Fe-rich segregation, oxide inclusions and sonotrode pickup, but no retrieved experiment quantifies **Fe loss**, Fe-specific vaporization, surface-tension change, or reaction rates of these compositions with **alumina, zirconia, graphite or a Ti-alloy sonotrode** at the stated temperatures. In a *different*, Fe-bearing ultrasonic-atomized multicomponent alloy, investigators detected **Mo contamination** from a Mo sonotrode and surface **Al/Cu/Mn oxides**; those observations establish a credible contamination-control requirement, **not a transferable 2.6 wt% Mo pickup** for these proposed powders. Measure melt/powder/deposit Fe by bulk analysis and oxygen/inclusions separately; do not describe Fe as an established sacrificial deoxidizer or assume Fe evaporation is the main loss mechanism. The near-IR Cu reflectivity and powder oxidation/porosity concerns are process constraints but are not Fe-specific measurements. (goncharov2026designofcobaltfree pages 10-13, nemani2024advancementsinadditive pages 105-106, li2021nanotwinscontainingmicrostructureand pages 9-14)

## 4. Phase boundaries, interactions, and proposed bounds

**[CITE] Thermodynamics:** Cu–Fe has restricted Cu-rich fcc solubility, a reported Cu-rich **L + γ-Fe → α-Cu peritectic near 1094 °C**, another Fe-rich peritectic near **1478 °C**, and an Fe-rich solid-state reaction reported at **820–855 °C**; the latter temperatures are **not** Cu-rich liquidus values. Cu–Ni–Fe additionally has a solid miscibility gap and Fe/Ni-rich versus Cu-rich fcc products, with conflicting historical assessed/experimental boundaries. Published Thermo-Calc calculations using a **Servant Cu–Ni–Fe assessment** exist. The retrieved sources do **not** yield a reliably readable **maximum Fe solubility in binary Cu expressed in wt% at a specified temperature**, a Cu–Al–Fe TDB assessment, or verified **TCCU/COST 531 version-specific ternary coverage**. Do not substitute the **~0.1 wt% at 400 °C in CuNi10** reported by one study for *binary* Cu–Fe maximum solubility: Kievits and IJsseling explicitly note contradictory measurements. Likewise, neither an exact liquidus at **5–6 Fe** nor clearance below the equipment’s **~1200–1250 °C useful-liquidus threshold** has been established here. Reject any candidate whose assessed liquidus plus required superheat exceeds the actual induction operating window; calculate full compositions and check melt thermally. [GAP] (kievits1972researchintothe pages 2-3, gallino2003phasediagramthermal pages 34-42, gallino2003phasediagramthermal pages 42-51)

**[NUMBERS] Composition-screen rules, wt% Fe in finished alloy, Cu balance:**

| Bound | Cu–Ni branch | Al-bronze/NAB branch | What sets it |
|---|---:|---:|---|
| **Functional floor** | **0.4**: lower end of reported C71500 seawater grade, a *practical documented floor*, not a demonstrated minimum detectable Fe effect | **2.0 exploratory**: Fe-bearing **Cu–8Al–2Ni–2Fe–2Mn** WAAM has been reported; no controlled minimum Fe effect identified | Below these values, a reliably measurable *Fe-specific* benefit remains unestablished. (kievits1972researchintothe pages 1-2, nemani2024advancementsinadditive pages 112-113) |
| **Conservative maximum** | **1.8** for conventional 90/10-type Cu–Ni; **1.0** if targeting a C71500-like 70/30 branch | **5.0**, supported by nominal laser-DED NAB and near-5-Fe cast material | Above the Cu–Ni range: Fe–Ni-rich precipitation/segregation and pitting; near/above NAB range: phase balance, cracking and unqualified seawater response. A measured powder mean of **5.48 Fe** is not evidence that a *nominal* 5.48-Fe composition was validated. (kievits1972researchintothe pages 1-2, kievits1972researchintothe pages 3-4, ocejo2022corrosionbehaviorof pages 1-3, li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 4-9) |
| **Non-conservative maximum** | **2.0**, restricted to an experimental Cu–Ni branch: historical **~1.99 Fe** material contained **1.84 precipitated Fe**, a warning rather than successful qualification | **6.0 provisional** for Fe-rich Al-bronze CALPHAD screening only; *no retrieved as-deposited seawater or atomization validation at 6.0* | Dissolved-Fe depletion/pitting in Cu–Ni; excessive κ/β heterogeneity, hot cracking and/or atomizer liquidus/superheat in Al bronze. **Neither aggressive bound is an approved design limit.** (lewis1981evaluationofcoppernickel pages 48-55, li2021nanotwinscontainingmicrostructureand pages 9-14) |

For a **single cross-family search-space number**, use conservative_max_wt **5.0** and exploratory nonconservative_max_wt **6.0**, but encode the **family-conditioned constraints above**; never interpret either as permission for **6 Fe in 70/30 Cu–Ni**. Recommended Fe-containing interactions for joint constraints are **Ni–Fe** (Fe retention/precipitation and protective-film chemistry), **Al–Fe–Ni** (Fe₃Al/NiAl κ and β balance), **Mn–Fe–Ni** (composition-dependent bronze phases), and **Fe–Si** where silicides are possible. A proposed numerical *Ni/Fe*, *Al/Fe* or *Fe+Mn* safety ratio is **not validated** by these sources. If considering steel-substrate dilution, calculate local—not just powder—Fe together with Al and Ni; if there is no steel substrate, do not impose a steel-dilution penalty on the two requested Cu-alloy repairs. [GAP] (kievits1972researchintothe pages 3-4, ocejo2022corrosionbehaviorof pages 5-8, gallino2003phasediagramthermal pages 34-42, ocejo2022corrosionbehaviorof pages 1-3, nemani2024advancementsinadditive pages 79-83, li2021nanotwinscontainingmicrostructureand pages 14-19)

## 5. Supply, safety, evidence quality, and key citations

**[GAP]** A primary **2022 US critical-minerals list, 2025 final list, current elemental Fe price/kg, OSHA Fe-oxide-fume limit, RoHS/REACH restriction, and applicable Navy material prohibition** were not retrieved or verified. Do **not** label Fe a US critical mineral, assign a defensible purchase price, or claim a Navy waiver on this evidence. Powder handling warrants combustible-dust assessment and airborne-dust controls; laser processing warrants capture/monitoring of metal/oxide fumes and oxygen exposure. Those are prudent controls, **not measured Fe-specific exposure rates for this process**. Evidence is **moderate** for including Fe and for the established-family ceilings, but **thin** for the **6.0 wt% exploratory limit**, Fe-specific cracking causality, in-house powder contamination, and proof of C71500-equivalent *as-deposited* 30-day seawater performance. (goncharov2026designofcobaltfree pages 10-13, nemani2024advancementsinadditive pages 102-105, li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14)

**Selected full research citations [CITE].** F. J. Kievits and F. P. IJsseling, “Research into the corrosion behaviour of CuNi10Fe alloys in seawater,” *Werkstoffe und Korrosion* **23** (1972), 1084–1096, **doi:10.1002/maco.19720231203**. R. O. Lewis and F. L. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications* (1981), **doi:10.2172/6255887**. J. Song, X. A. Jimenez, A. C. To and Y. Fu, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* **17** (2024), 876, **doi:10.3390/ma17040876**. B. Li, H. Zheng, C. Han and K. Zhou, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39** (2021), 101825, **doi:10.1016/j.addma.2020.101825**. I. Cobo Ocejo, M. V. Biezma Moraleda and P. Linhardt, “Corrosion Behavior of Heat-Treated Nickel-Aluminum Bronze and Manganese-Aluminum Bronze in Natural Waters,” *Metals* **12** (2022), 380, **doi:10.3390/met12030380**. H. R. Jafari, A. Davoodi and S. Hosseinpour, “Effect of Fluid Flow on the Corrosion Performance of as-Cast and Heat-Treated Nickel Aluminum Bronze Alloy (UNS C95800) in Saline Solution,” *Corrosion and Materials Degradation* **2** (2021), 61–77, **doi:10.3390/cmd2010004**. C. Berlanga-Labari *et al.*, “The Effect of Kappa Phases on Tribocorrosion Behaviour of Nickel Aluminum Bronze (NAB) and Manganese Aluminum Bronze (MAB),” *Lubricants* **13** (2025), 290, **doi:10.3390/lubricants13070290**. A. V. Nemani *et al.*, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites,” *Journal of Manufacturing and Materials Processing* **8** (2024), 54, **doi:10.3390/jmmp8020054**. I. Goncharov *et al.*, “Design of Cobalt-Free High-Entropy Alloy Binder for WC-Base Cemented Carbides,” *Metals* **16** (2026), 318, **doi:10.3390/met16030318**; its ultrasonic-atomization data concern a *different alloy*. (kievits1972researchintothe pages 1-2, lewis1981evaluationofcoppernickel pages 43-48, song2024microstructuresandcorrosion pages 2-5, li2021nanotwinscontainingmicrostructureand pages 1-4, ocejo2022corrosionbehaviorof pages 1-3, jafari2021effectoffluid pages 7-8, berlangalabari2025theeffectof pages 4-7, nemani2024advancementsinadditive pages 79-83, goncharov2026designofcobaltfree pages 10-13)

VERDICT | Fe | decision=INCLUDE | family=both | conservative_max_wt=5.0 | nonconservative_max_wt=6.0 | floor_wt=0.4 | impurity_max_wt=NA | evidence=moderate

References

1. (kievits1972researchintothe pages 1-2): F. J. Kievits and F. P. Ijsseling. Research into the corrosion behaviour of cuni10fe alloys in seawater. Materials and Corrosion-werkstoffe Und Korrosion, 23:1084-1096, Dec 1972. URL: https://doi.org/10.1002/maco.19720231203, doi:10.1002/maco.19720231203. This article has 23 citations and is from a peer-reviewed journal.

2. (kievits1972researchintothe pages 3-4): F. J. Kievits and F. P. Ijsseling. Research into the corrosion behaviour of cuni10fe alloys in seawater. Materials and Corrosion-werkstoffe Und Korrosion, 23:1084-1096, Dec 1972. URL: https://doi.org/10.1002/maco.19720231203, doi:10.1002/maco.19720231203. This article has 23 citations and is from a peer-reviewed journal.

3. (ocejo2022corrosionbehaviorof pages 1-3): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

4. (li2021nanotwinscontainingmicrostructureand pages 1-4): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

5. (li2021nanotwinscontainingmicrostructureand pages 9-14): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

6. (kievits1972researchintothe pages 4-5): F. J. Kievits and F. P. Ijsseling. Research into the corrosion behaviour of cuni10fe alloys in seawater. Materials and Corrosion-werkstoffe Und Korrosion, 23:1084-1096, Dec 1972. URL: https://doi.org/10.1002/maco.19720231203, doi:10.1002/maco.19720231203. This article has 23 citations and is from a peer-reviewed journal.

7. (kievits1972researchintothe pages 2-3): F. J. Kievits and F. P. Ijsseling. Research into the corrosion behaviour of cuni10fe alloys in seawater. Materials and Corrosion-werkstoffe Und Korrosion, 23:1084-1096, Dec 1972. URL: https://doi.org/10.1002/maco.19720231203, doi:10.1002/maco.19720231203. This article has 23 citations and is from a peer-reviewed journal.

8. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

9. (ocejo2022corrosionbehaviorof pages 8-10): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

10. (ocejo2022corrosionbehaviorof pages 5-8): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

11. (berlangalabari2025theeffectof pages 4-7): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

12. (li2021nanotwinscontainingmicrostructureand pages 14-19): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

13. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

14. (nemani2024advancementsinadditive pages 112-113): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

15. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

16. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

17. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

18. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

19. (song2024microstructuresandcorrosion pages 13-14): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

20. (jafari2021effectoffluid pages 7-8): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

21. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

22. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

23. (goncharov2026designofcobaltfree pages 10-13): Ivan Goncharov, Vera Popovich, Marcel Sluiter, Anatoly Popovich, and Maurizio Vedani. Design of cobalt-free high-entropy alloy binder for wc-base cemented carbides. Metals, 16:318, Mar 2026. URL: https://doi.org/10.3390/met16030318, doi:10.3390/met16030318. This article has 1 citations.

24. (nemani2024advancementsinadditive pages 105-106): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

25. (gallino2003phasediagramthermal pages 34-42): I Gallino. Phase diagram, thermal stability, and high temperature oxidation of the ternary cu-ni-fe system. Unknown journal, 2003.

26. (gallino2003phasediagramthermal pages 42-51): I Gallino. Phase diagram, thermal stability, and high temperature oxidation of the ternary cu-ni-fe system. Unknown journal, 2003.
