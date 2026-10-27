<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: b158a188-99fd-4da4-8597-365951f28b27
- Submitted: 2026-10-17T18:58:31Z
- Fetched: 2026-10-17T19:30:24Z (status: success)
- Raw trajectory JSON: ../raw/el-02-Ni.json.gz
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

ELEMENT UNDER REVIEW: Ni (major seawater addition). C70600 (9-11 Ni), C71500 (29-33 Ni), C71640 (Cu-30Ni-2Fe-2Mn), C72200 (15-18 Ni, Cr), NAB C95800 and C63000 (4-5.5 Ni), MARINEL (Cu-19Ni-4.6Mn-1.9Al). Nickel raises the liquidus (70-30 melts at about 1,171-1,238 C) and is a US critical mineral.

Answer for Ni specifically, not for copper alloys in general:
1. ROLE: what Ni does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ni ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ni changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ni, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ni, Cu-Ni-Ni and Cu-Al-Ni are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ni in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ni neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ni | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ni (major seawater addition). C70600 (9-11 Ni), C71500 (29-33 Ni), C71640 (Cu-30Ni-2Fe-2Mn), C72200 (15-18 Ni, Cr), NAB C95800 and C63000 (4-5.5 Ni), MARINEL (Cu-19Ni-4.6Mn-1.9Al). Nickel raises the liquidus (70-30 melts at about 1,171-1,238 C) and is a US critical mineral.

Answer for Ni specifically, not for copper alloys in general:
1. ROLE: what Ni does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ni ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ni changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ni, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ni, Cu-Ni-Ni and Cu-Al-Ni are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ni in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ni neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ni | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Nickel as a designed addition to marine copper-alloy DED powder

**Decision: INCLUDE Ni for both Cu–Ni and aluminum-bronze candidates.** The strongest case for Ni is a corrosion-resistant Cu-rich solid solution and a less conductive seawater film; in Ni–Al bronze, its additional function is formation of NiAl-bearing κ precipitates. These benefits do **not** establish that a new, unheated laser-DED deposit will match wrought C71500: film development, as-deposited phase constitution, dilution, and repair-interface attack must be tested separately. The proposed *search bounds* are **33 wt% Ni conservative and 35 wt% Ni aggressive for Cu–Ni compositions**, **5.5 wt% Ni conservative and 7 wt% Ni exploratory for Al-bronze compositions**, with a **2 wt% Ni functional screening floor**. The aggressive limits are engineering hypotheses, not established marine specifications. (schmidfetzer2014phasediagramsthe pages 3-4, lewis1981evaluationofcoppernickel pages 14-17, nemani2024advancementsinadditive pages 62-68, lancaster1999nonferrousmetals pages 12-15)

## 1. Role, mechanisms, and identifiable alloys

- **Cu–Ni:** Ni substitutes for Cu in the FCC matrix; high-temperature binary Cu–Ni has a continuous FCC solid-solution field, rather than a Ni-strengthening intermetallic. In seawater, the principal barrier is Cu₂O. Incorporated Ni²⁺ alters its defect chemistry and increases resistance to electronic and ionic transport; dissolved Fe assists film formation and Ni incorporation. Thus neither Ni content nor the presence of Ni in an analysis substitutes for controlling Fe *in solution* and film maturation. **[CITE][NUMBERS]** Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, US technical report (1981), DOI **10.2172/6255887**. (schmidfetzer2014phasediagramsthe pages 3-4, lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 48-55, nikolaenko1997enthalpiesofformation pages 1-2)
- **NAB and other Al bronzes:** Ni participates in NiAl-rich κIII; Fe contributes Fe₃Al-rich κII and Fe-rich κIV. Their amount and morphology depend on solidification and reheating. A laser-deposited Cu–9Al–5Fe–5Ni, all in wt%, contained β* martensite, α, and nanoscale NiAl and Fe₃Al. Ni is **not** the principal melt deoxidant or an independently established grain refiner: Al/Ti-based deoxidation and precipitation-associated grain refinement must be distinguished from an effect of Ni itself. **[CITE]** Nemani *et al.*, *Journal of Manufacturing and Materials Processing* **8** (2024) 54, DOI **10.3390/jmmp8020054**; Lancaster, “Non-ferrous metals,” in *Metallurgy of Welding* (1999), DOI **10.1007/978-94-010-9506-8_9**. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 74-79, lancaster1999nonferrousmetals pages 12-15)
- **[SPEC] Verified composition anchors, all wt% Ni:** C70600, **9–11** (ASTM/UNS Cu–Ni tubing comparison); C71500, **29–33** (US copper-alloy survey); C72200, approximately **16** with approximately **0.5 wt% Cr** (Lewis–LaQue report); documented C95800 material, **4.50** as cast, and **4.6–5.2** in reported AM feedstocks; reported C63000 AM feedstocks, **4.2–5.0**. These last figures are *measured or reported feedstock compositions*, **not** independently verified full UNS specification intervals. **[CITE][NUMBERS]** Schleich, “Typical Failures of CuNi 90/10 Seawater Tubing Systems and How to Avoid Them” (2004; DOI not identified); Beavers, Agrawal and Berry, *Corrosion-related Failures in Power Plant Condensers* (1980), DOI **10.2172/5047866**; Jafari, Davoodi and Hosseinpour, *Corrosion and Materials Degradation* **2** (2021) 61–77, DOI **10.3390/cmd2010004**; Nemani *et al.* (2024), DOI above. (schleich2004typicalfailuresof pages 1-3, jafari2021effectoffluid pages 2-4, nemani2024advancementsinadditive pages 60-62, nemani2024advancementsinadditive pages 62-68, beavers1980corrosionrelatedfailuresin pages 266-270)
- **[NAVY][SPEC][GAP]** Lewis and LaQue document 70/30 Cu–Ni in merchant and naval heat-exchanger service and report a surveyed **Cu–30Ni–2Fe–2Mn**, all in wt%, tube population; this supports a high-Fe/Mn composition but does *not* verify the requested **C71640** designation or its formal interval. An AWS A5.7 ERCuNiAl-type wire is documented at **5.2 wt% Ni**, alongside approximately **8.8 wt% Al and 3.3 wt% Fe**; other reported WAAM wire is approximately **4 wt% Ni**. Exact AWS A5.7 chemistry limits for **ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl**, and their assignment to **MIL-T-16420, MIL-B-24480, and MIL-C-15726**, could not be verified from the retrieved specifications. Do not present their names as certified Ni ranges. MARINEL is described in the question as **19 wt% Ni**; its specification and as-deposited corrosion were not independently established. **[CITE]** Lewis and LaQue (1981), DOI above; Nemani *et al.* (2024), DOI above. (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 60-64, nemani2024advancementsinadditive pages 60-62)
- **Other families [GAP]:** Cu–Ni–Sn is an age-hardening/spinodal-alloy route, and CuNi₂SiCr denotes a Ni–Si-bearing repair alloy, unlike corrosion-film strengthening in binary Cu–Ni. The retrieved review documents Cu–Ni–Sn/Pb laser alloys but does not establish that their Ni–Sn or Ni–Si precipitates improve *as-deposited seawater* performance. Equally, Ni ranges and independently measured Ni-specific dealloying inhibition for gunmetal/tin bronze, marine brasses, and Mn–Al bronze were not established here. Avoid transferring C71500 performance to these alloys merely because they contain Ni. **[CITE][GAP]** Nemani *et al.* (2024), DOI above. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 26-28, nemani2024advancementsinadditive pages 79-83)

## 2. Seawater corrosion: benefits and adverse regimes

**[CITE][NUMBERS] Natural seawater.** Lewis and LaQue report typical average corrosion of C70600 and C71500 of **2.5–12.7 µm/year**, falling below **2.5 µm/year** after **14–16 years** in quiet/low-velocity exposure; the twenty deepest C71500 pits averaged **<127 µm after 16 years**. At low velocity their compiled quiet-water ranges were, respectively, **5.1–15.2** and **7.6–12.7 µm/year**; at approximately **0.61 m/s**, **12.7–27.9** and **12.7–17.8 µm/year**. These overlapping ranges do **not** demonstrate a monotonic field advantage for raising Ni from 10 to 30 wt%, because Fe contents and exposure histories differ. In a separate **30-day**, **2.0 m/s** dataset, C70600 gave approximately **85–94 µm/year** and C71500 approximately **90–95 µm/year**; short-term rates cannot be equated to mature-film service rates or a 30-day depth of attack. **[CITE][NUMBERS]** Lewis and LaQue (1981), DOI above. (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 55-60, lewis1981evaluationofcoppernickel pages 43-48)

**[CITE][NUMBERS] Controlled chloride and film mechanism.** In a **2-hour**, stagnant, **3.5 wt% NaCl** experiment at **25 °C**, Yang’s Cu–Ni series containing **9.3, 18.8, 28.4 and 48.0 wt% Ni** gave, respectively, corrosion rates **55.0, 44.2, 29.0 and 20.6 µm/year**; polarization resistances **7,882, 7,952, 13,055 and 18,019 Ω·cm²**; and corrosion potentials **−261.0, −235.7, −211.4 and −202.8 mV versus SCE**. Pure Cu gave **92.4 µm/year**, **4,155 Ω·cm²**, and **−304.5 mV versus SCE**. The original specimen names are **atomic-percent** labels: for example, Cu₇₀Ni₃₀ is **28.4 wt% Ni**, not 30 wt%. Lewis and LaQue’s reported Cu₂O-film electronic resistance rose from **5.5 × 10³** for Cu to **23.5 × 10³** for 90/10 and **82.5 × 10³** for 70/30; the corresponding ionic-resistance series was **4, 11 and 21 × 10³** in the report’s tabulated units. The thesis also reports poorer repeated-scan response of its Ni-rich specimens, which it attributes to **denickelification**; that interpretation is not a demonstrated 30-day penetration depth. **[CITE][NUMBERS]** Yang, *The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes*, UNSW thesis (2019), DOI **10.26190/unsworks/21760**; Lewis and LaQue (1981), DOI above. (yang2019theevolutionof pages 68-71, yang2019theevolutionof pages 37-42, lewis1981evaluationofcoppernickel pages 43-48)

**[CITE][NUMBERS] Flow, local attack and limits.** The reported *accepted tubular design velocities* are **3.6 m/s** for C70600 with approximately **1.4 wt% Fe**, **4.6 m/s** for C71500 with approximately **0.5 wt% Fe**, and **>9 m/s** for Cr-bearing C72200. A different experiment gave critical velocities **4.5, 4.1 and 12.0 m/s**, respectively: the apparent reversal between the two Cu–Ni grades is a warning that apparatus, temperature and criterion matter. Chromium-bearing alloys improved high-velocity impingement but could show *more* local attack in quiet water. For C70600, deposit retention becomes a concern below approximately **1 m/s**; sulphide-polluted water disrupts protective films. Neither a tube velocity nor a rotating-disc rpm is a universal DED-part velocity rating. **[CITE][NUMBERS]** Lewis and LaQue (1981), DOI above; Schleich (2004), DOI not identified. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 48-55, schleich2004typicalfailuresof pages 3-6)

**[CITE][NUMBERS] NAB: Ni is not an independent corrosion variable.** Jafari *et al.* tested as-cast **Cu–8.79Al–4.50Ni–3.70Fe–1.00Mn**, all wt%, in **3.5 wt% NaCl**. At **25 °C**, its extrapolated rate was **0.02 mm/year** stagnant and **0.06 mm/year** at **9,000 rpm**; after **675 °C/6 h** annealing, approximately **0.01** and **0.05 mm/year**, respectively. Annealing reduced corrosion-sensitive β from **>20% to ~7%**, changing the microstructure *without changing Ni content*. Conversely, the AM review reports **one-order-of-magnitude lower mass loss after 3–6 months seawater exposure** for an **as-printed, martensitic L-PBF** NAB than for the compared cast/wrought α/κ alloys. These are different processes, microstructures and tests: neither result proves that increasing Ni alone prevents NAB selective attack or that a laser-DED NAB will match C71500. **[CITE][NUMBERS][GAP]** Jafari *et al.* (2021), DOI above; Nemani *et al.* (2024), DOI above. (jafari2021effectoffluid pages 2-4, jafari2021effectoffluid pages 7-8, nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79)

## 3. Deposition, welding, and the two repair interfaces

**[CITE]** The binary FCC Cu–Ni path avoids a *binary* brittle intermetallic at a Cu–Ni repair interface, and Lancaster describes cupronickel weld cracking as ordinarily less serious than porosity. **It is not a guarantee against solidification cracks:** Pb, Bi, S and other low-melting contamination, a widened multicomponent freezing interval, insufficient wetting, and reheated-layer liquation require examination. Cu–Ni filler needs a deoxidant—Lancaster specifically recommends **Ti**—whereas a Ni addition by itself does not remove oxygen or hydrogen. His successful duplex Al-bronze filler contained nominally **5.5 wt% Ni, 10 wt% Al and 2.5 wt% Fe**; this is welding evidence, not proof that Ni alone suppresses laser-DED cracking. **[CITE][GAP]** Lancaster (1999), DOI above. (lancaster1999nonferrousmetals pages 12-15, lancaster1999nonferrousmetals pages 15-18)

**[CITE][NUMBERS]** Published laser DED of **Cu–9Al–5Fe–5Ni**, all wt%, demonstrates a Ni-bearing NAB build, with reported yield strength **593–713 MPa**, tensile strength **769–949 MPa** and elongation **10–12%**; it does not establish a Ni–crack-susceptibility curve, post-reheat liquation limit, or 30-day seawater equivalence. The AM review also identifies deposition of **CuNi₂SiCr powder on cast AlBC3 NAB**: its porous, low-hardness, essentially α deposit was judged unsuitable for that propeller-repair application. Thus a Ni-bearing powder on NAB is not automatically a successful repair. NAB-on-316L WAAM studies report conflicting interface cracking outcomes with different heat inputs; they cannot be transferred quantitatively to a Cu-alloy-on-C95800 joint. At the C95800 interface, map the **local** Ni:Al:Fe balance, remelted β/κ constitution, pores and selective-attack depth; at wrought C71500, check first-track Ni dilution and HAZ loss of wrought temper. **[CITE][GAP]** Nemani *et al.* (2024), DOI above; Saboori *et al.*, *Applied Sciences* **9** (2019) 3316, DOI **10.3390/app9163316**. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 106-108, nemani2024advancementsinadditive pages 62-68)

## 4. Powder production, thermodynamics, and feasibility

**[CITE][NUMBERS]** The binary Cu–Ni liquidus rises toward Ni’s melting point as Ni increases. It has **complete high-temperature solid solubility, up to 100 wt% Ni in the FCC field near the pure-Ni melting endpoint**, rather than a finite maximum-solubility composition at one temperature; no established *binary* intermetallic or eutectic/peritectic invariant sets the upper bound. One thermodynamic study nevertheless reports a **low-temperature FCC/FCC miscibility gap** closing near **354 °C** at approximately **64 wt% Ni** (converted from **67.3 at%**), relevant to prolonged aging, not directly to atomization. Cu–Al–Ni is different: NiAl-containing κ makes a binary-solubility rule unsafe for NAB. **[CITE]** Schmid-Fetzer, *Journal of Phase Equilibria and Diffusion* **35** (2014) 735–760, DOI **10.1007/s11669-014-0343-5**; Nikolaenko and Turchanin, *Metallurgical and Materials Transactions B* **28** (1997) 1119–1130, DOI **10.1007/s11663-997-0068-5**. (schmidfetzer2014phasediagramsthe pages 3-4, nikolaenko1997enthalpiesofformation pages 1-2)

**[GAP]** For the stated approximately **1,300 °C** induction ceiling, a **30–33 wt% Ni** Cu–Ni composition, already near the upper melting interval quoted in the question, must have its *actual multicomponent liquidus and useful superheat* calculated and measured; do not mistake a liquidus below **1,250 °C** for proof that **35 wt%** can be ultrasonically atomized. Establish a per-charge go/no-go requirement, for example **calculated/measured liquidus ≤1,250 °C plus demonstrated stable atomization superheat**, rather than assign an unsupported universal Ni liquidus cutoff. The published binary assessment and a published **Cu–Al–Ni Cu–Ni-side** thermodynamic description by **J. Miettinen**, *Calphad* (2005), DOI **10.1016/j.calphad.2005.02.002**, show that relevant assessments exist; the retrieved evidence does **not** verify which ternary interactions are included or validated in the installed **TCCU/COST 531** versions. “Cu–Ni–Ni” reduces to **Cu–Ni**, not a distinct ternary. Run TCCU and pycalphad on the *same documented parameter set*, and compare equilibrium liquidus with Scheil-predicted terminal liquid and measured DSC. (schmidfetzer2014phasediagramsthe pages 3-4, nikolaenko1997enthalpiesofformation pages 1-2)

**[GAP]** No located experiment measures Ni loss, surface-tension change, or contamination specifically during **rePOWDER** ultrasonic atomization of these alloys using **alumina versus zirconia** crucibles or **Ti-alloy versus Mo** sonotrodes. Consequently do not claim that Ni deoxidizes the melt, that it necessarily attacks either ceramic, or that it evaporates preferentially to Cu. The practical, testable risks are oxide/inclusion pickup from air leaks and Ni–Al-bearing feedstock, carbon/oxygen pickup if graphite is substituted, sonotrode-derived Ti or Mo, and insufficient fluidity/superheat as Ni raises liquidus. Compare charge, melt, classified powder and deposit by ICP/OES, O/N/C analysis and inclusion microscopy; confirm powder size and flow before interpreting laser porosity. Laser weld data support the importance of deoxidation and cleanliness, **not** a measured Ni evaporation-loss coefficient for this machine. (lancaster1999nonferrousmetals pages 12-15, lancaster1999nonferrousmetals pages 15-18, manoharanUnknownyear3.processmicrostructurerelationship pages 101-104)

## 5. Supply, safety, joint constraints, and bound-setting

**[CITE][SPEC]** Ni was already a U.S. critical mineral under the **2022** list and remains so on the **final 2025** list; copper’s addition in 2025 should not be confused with removal of Ni. The USGS technical report concerns the **draft** recommendation: the final list differs from it, as the subsequent USGS review explains. **[CITE]** Nassar *et al.*, USGS Open-File Report **2025-1047**, DOI **10.3133/ofr20251047**; USGS mining review of the final 2025 list (2026; DOI not identified). A source-supported current Ni metal price in **USD/kg** was **not** recovered, so no fabricated spot-price figure is assigned; quote a dated supplier/USGS benchmark before costing 0.5-kg charges. (nassar2025methodologyandtechnical pages 9-10, staff2022usgsminingreview pages 6-9)

**[CITE][NUMBERS]** An occupational review reports **OSHA Ni PEL 1 mg/m³, 8-hour TWA**, versus **NIOSH REL 0.015 mg/m³**, and distinguishes **IARC Group 2B metallic Ni** from **Group 1 Ni compounds**. Ni sensitization, inhalable powder, fine laser fume and subsequent oxide/soluble-species formation demand enclosure, local exhaust, appropriate filtration, personal exposure monitoring and powder-spill controls. Those are *airborne exposure* limits, not permitted alloy wt% values. Retrieved sources do not establish a blanket **RoHS prohibition** on Ni metal in a marine alloy, a particular **REACH** applicability determination, or a universal Navy Ni prohibition: verify product-specific and contract-specific requirements rather than invent one. **[CITE]** Kodali, Erdely and Zeidler-Erdely, “Toxicity of Airborne Metals” (2026), DOI **10.1016/B978-0-323-95488-4.00102-9**. (kodali2026toxicityofairborne pages 5-6, kodali2026toxicityofairborne pages 3-5)

**Proposed one-element bounds, all wt% Ni in the Cu-balance alloy:**

| Search branch | Functional floor | Conservative upper | Non-conservative upper | What sets the bounds |
|---|---:|---:|---:|---|
| Cu–Ni | **2** *(experimental screening floor, not proved seawater efficacy)* | **33** | **35** | **33** is the verified C71500 specification ceiling and preserves a direct wrought target; **35** tests modestly beyond it but fails if measured liquidus/superheat, powder yield, Ni cost, or as-deposited corrosion fail. Even **9–11** has strong established service evidence with suitable Fe; there is no claim that **2** matches it. |
| Al bronze/NAB | **2** *(κ-development screening floor)* | **5.5** | **7** | Approximately **4–5.2** is directly represented by studied C95800/C63000 feedstocks and **5.5** by a successful duplex weld filler; **7** is an explicitly unqualified extension that fails on excessive NiAl/Fe–Al κ, brittle as-deposited β/κ, segregation or selective attack. |

The **common palette entry** may therefore be *Ni 0–35 wt%* with a **2 wt% first-effect screening level**, but a joint design must impose **family-dependent** maxima and the liquidus ceiling; the palette is **not** a recommendation to add 35 wt% Ni to NAB. Binary Cu–Ni complete solubility supports investigating above the commercial ceiling, **not** using 48 wt% Ni in a machine whose melt ceiling has not been demonstrated for it. **[CITE][SPEC][GAP]** Beavers *et al.* (1980), DOI above; Schmid-Fetzer (2014), DOI above; Lancaster (1999), DOI above; Nemani *et al.* (2024), DOI above. (beavers1980corrosionrelatedfailuresin pages 266-270, schmidfetzer2014phasediagramsthe pages 3-4, lancaster1999nonferrousmetals pages 12-15, nemani2024advancementsinadditive pages 74-79)

**Interactions to carry forward.** On the Cu–Ni branch, assess **Ni × dissolved Fe**, not Ni independently: the report gives approximately **1.3–2.0 wt% Fe** to make 90/10 comparable in flowing-seawater service to 70/30, whereas conventional 70/30 uses approximately **0.4–0.7 wt% Fe**; excessive or precipitated Fe changes the benefit. Track Mn alongside Fe and impurity **S/Pb/Bi**, and compare results at equal film age. On the Al-bronze branch, constrain **Ni jointly with Al and Fe** against the fractions of α, β/β*, κIII (NiAl), Fe₃Al-bearing κ and *terminal liquid*; track dilution-induced local ratios rather than nominal powder composition alone. Zn-rich brass requires a separate dezincification constraint, while Ni–Sn/Si age hardening cannot be credited as an as-deposited seawater benefit without immersion evidence. **[CITE][NUMBERS][GAP]** Lewis and LaQue (1981), DOI above; Jafari *et al.* (2021), DOI above; Lancaster (1999), DOI above; Nemani *et al.* (2024), DOI above. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 48-55, jafari2021effectoffluid pages 2-4, nemani2024advancementsinadditive pages 62-68, lancaster1999nonferrousmetals pages 12-15)

**Evidence quality:** **moderate for including Ni and for the conservative family-specific ceilings; thin for the 2 wt% floor, either aggressive ceiling, and the *combined* requirement of crack-free single-stream laser DED plus as-deposited ≥C71500 seawater performance on **both** repair substrates.** The 30-day ASTM D1141 depth-of-selective-attack comparison, specimen orientation, oxide-film maturation and interface-specific results are decisive experiments, not outcomes established by the cited wrought, casting, welding, L-PBF or WAAM work. (lewis1981evaluationofcoppernickel pages 55-60, jafari2021effectoffluid pages 7-8, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83)

VERDICT | Ni | decision=INCLUDE | family=both | conservative_max_wt=33 | nonconservative_max_wt=35 | floor_wt=2 | impurity_max_wt=NA | evidence=moderate

References

1. (schmidfetzer2014phasediagramsthe pages 3-4): Rainer Schmid-Fetzer. Phase diagrams: the beginning of wisdom. Journal of Phase Equilibria and Diffusion, 35:735-760, Sep 2014. URL: https://doi.org/10.1007/s11669-014-0343-5, doi:10.1007/s11669-014-0343-5. This article has 100 citations and is from a peer-reviewed journal.

2. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

3. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

4. (lancaster1999nonferrousmetals pages 12-15): J. F. Lancaster. Non-ferrous metals. ArXiv, pages 197-223, Jan 1999. URL: https://doi.org/10.1007/978-94-010-9506-8\_9, doi:10.1007/978-94-010-9506-8\_9. This article has 7 citations.

5. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

6. (nikolaenko1997enthalpiesofformation pages 1-2): I. V. Nikolaenko and M. A. Turchanin. Enthalpies of formation of liquid binary (copper + iron, cobalt, and nickel) alloys. Metallurgical and Materials Transactions B, 28:1119-1130, Dec 1997. URL: https://doi.org/10.1007/s11663-997-0068-5, doi:10.1007/s11663-997-0068-5. This article has 51 citations.

7. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

8. (schleich2004typicalfailuresof pages 1-3): W Schleich. Typical failures of cuni 90/10 seawater tubing systems and how to avoid them. Unknown journal, 2004.

9. (jafari2021effectoffluid pages 2-4): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

10. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

11. (beavers1980corrosionrelatedfailuresin pages 266-270): J. A. Beavers, A. K. Agrawal, and W. E. Berry. Corrosion-related failures in power plant condensers. final report. [pwr]. Unknown journal, Aug 1980. URL: https://doi.org/10.2172/5047866, doi:10.2172/5047866. This article has 6 citations.

12. (lewis1981evaluationofcoppernickel pages 60-64): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

13. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

14. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

15. (lewis1981evaluationofcoppernickel pages 55-60): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

16. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

17. (yang2019theevolutionof pages 68-71): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

18. (yang2019theevolutionof pages 37-42): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

19. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

20. (schleich2004typicalfailuresof pages 3-6): W Schleich. Typical failures of cuni 90/10 seawater tubing systems and how to avoid them. Unknown journal, 2004.

21. (jafari2021effectoffluid pages 7-8): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

22. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

23. (lancaster1999nonferrousmetals pages 15-18): J. F. Lancaster. Non-ferrous metals. ArXiv, pages 197-223, Jan 1999. URL: https://doi.org/10.1007/978-94-010-9506-8\_9, doi:10.1007/978-94-010-9506-8\_9. This article has 7 citations.

24. (nemani2024advancementsinadditive pages 106-108): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

25. (manoharanUnknownyear3.processmicrostructurerelationship pages 101-104): S Manoharan. 3. process-microstructure relationship in simultaneous wire-fed and powder-fed laser directed energy deposition of compositionally graded metals. Unknown journal, Unknown year.

26. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

27. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

28. (kodali2026toxicityofairborne pages 5-6): Vamsi K. Kodali, Aaron Erdely, and Patti C. Zeidler-Erdely. Toxicity of Airborne Metals. Elsevier, Jan 2026. URL: https://doi.org/10.1016/b978-0-323-95488-4.00102-9, doi:10.1016/b978-0-323-95488-4.00102-9. This article has 0 citations.

29. (kodali2026toxicityofairborne pages 3-5): Vamsi K. Kodali, Aaron Erdely, and Patti C. Zeidler-Erdely. Toxicity of Airborne Metals. Elsevier, Jan 2026. URL: https://doi.org/10.1016/b978-0-323-95488-4.00102-9, doi:10.1016/b978-0-323-95488-4.00102-9. This article has 0 citations.
