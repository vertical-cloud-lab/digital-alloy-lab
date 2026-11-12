<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: de43757e-5446-49f5-899b-5c5f0294e244
- Submitted: 2026-10-17T18:58:40Z
- Fetched: 2026-10-17T19:33:05Z (status: success)
- Raw trajectory JSON: ../raw/el-05-Mn.json.gz
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

ELEMENT UNDER REVIEW: Mn (major seawater addition). Cu-Ni: up to 1 Mn (deoxidizer), C71640 1.5-2.5 Mn; NAB 0.8-3.5 Mn; Mn-Al bronze C95700 11-14 Mn; MARINEL 4.6 Mn. Mn has a high vapor pressure and is lost in laser processing; it is a candidate nickel substitute.

Answer for Mn specifically, not for copper alloys in general:
1. ROLE: what Mn does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Mn ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Mn changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Mn, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Mn, Cu-Ni-Mn and Cu-Al-Mn are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Mn in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Mn neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Mn | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Mn (major seawater addition). Cu-Ni: up to 1 Mn (deoxidizer), C71640 1.5-2.5 Mn; NAB 0.8-3.5 Mn; Mn-Al bronze C95700 11-14 Mn; MARINEL 4.6 Mn. Mn has a high vapor pressure and is lost in laser processing; it is a candidate nickel substitute.

Answer for Mn specifically, not for copper alloys in general:
1. ROLE: what Mn does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Mn ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Mn changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Mn, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Mn, Cu-Ni-Mn and Cu-Al-Mn are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Mn in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Mn neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Mn | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Mn as a designed addition to laser-DED marine copper alloys

**Decision: INCLUDE Mn in both the Cu–Ni and aluminum-bronze search spaces, but do not treat it as a demonstrated one-for-one substitute for Ni.** The strongest composition-controlled chloride evidence shows a benefit at modest Mn content and sharply poorer behavior at higher Mn content without sufficient Ni. Established Mn-containing NAB can be deposited densely by *wire-arc* additive manufacturing, but neither that result nor cast-alloy seawater performance establishes the required **as-deposited, single-stream laser-powder DED** performance. All compositions below are **wt%**, with Cu the balance unless stated otherwise. (yang2019theevolutionof pages 71-76, yang2019theevolutionof pages 79-83, dharmendra2019microstructuralevolutionand pages 14-15)

## 1. Metallurgical role and documented alloy ranges

- **Cu–Ni.** [CITE] Mn is a melt deoxidizer and increases the solubility of Fe in the Cu–Ni matrix. This matters because Fe’s state in solution and the resulting Fe-bearing corrosion film—not an established Mn-rich film—are important to flowing-seawater performance. An older Cu–Ni study discusses Mn at **≤0.75 wt%** and an approximately **1.0–1.75 wt% Fe** optimum for 90–10 Cu–Ni; these are study-specific values, **not verified current ASTM B111 limits**. The often-quoted higher-Mn C71640 composition and the exact C71500, C70600, ASTM B111/B171/B466, EN 12449 and MIL-T-16420/MIL-C-15726 Mn limits were not recoverable as authoritative specification text here and should not be presented as verified limits. [GAP] (parvizi1985photoelectronandelectrochemical pages 33-37, parvizi1985photoelectronandelectrochemical pages 37-41)
- **NAB and aluminum bronze.** [SPEC][NAVY] A published description of **UNS C95800 under ASTM B148** gives **Mn 0.8–1.5 wt%**, Al 8.5–9.5 wt%, Ni 4–5 wt% and Fe 3.5–4.5 wt%. Independently, an AWS A5.7 **ERCuNiAl** filler comparison lists **Mn 0.6–3.5 wt%**, Al 8.5–9.5 wt%, Ni 4.0–5.5 wt% and Fe 3.0–5.0 wt%; this is the paper’s stated *filler range*, not a reproduced complete AWS standard. Its comparison wire, designated CuAl9Ni5Fe3Mn2, is reported as **1.0 wt% Mn** despite the “Mn2” name. Do not substitute the wire’s name for its measured/tabulated composition. [NUMBERS] (dharmendra2019microstructuralevolutionand pages 2-3, kim2021effectoffiller pages 2-4)
- **Mechanism in NAB.** [CITE][NUMBERS] Approximately **1 wt% Mn** is reported to improve castability and retard β transformation, with a phase-diagram effect compared by the authors to approximately **0.15 wt% Al**. Mn principally resides in solid solution at ordinary NAB levels; in one cast alloy containing **1.23 wt% bulk Mn**, phase analyses found **1.1 wt% in α**, **1.0 wt% in β′**, **1.8 wt% in κII**, and **1.1 wt% in κIII**. Thus κII incorporates some Mn, but κII and κIII are principally Fe–Al- and Ni–Al-based phases; calling them specifically Mn intermetallics is incorrect. Fe, rather than Mn, has the well-established grain-refining role in this NAB evidence. (dharmendra2019microstructuralevolutionand pages 1-2, ding2019evolutionofthe pages 1-3, ding2019evolutionofthe media f3cdbb72)
- **Other families.** [CITE] Experimental Cu–Mn–Ni alloys were predominantly α solid solution; **Cu–13.3Mn–4.7Ni** and **Cu–8.8Mn–9.4Ni** additionally contained a reported **τ phase**. Experimental Cu–Mn–Al alloys remained α through **Cu–9.3Mn–4.6Al**, while **Cu–13.6Mn–2.2Al** showed α plus an Mn-rich constituent. Those experimental compositions are **not commercial marine qualifications**. Reliable specification text for C71640, high-Mn C95700, MARINEL, ERCuMnNiAl, Mn-bearing tin bronze/gunmetal, brasses, Cu–Ni–Sn and Cu–Ni–Si was not obtained; their nominal labels should not be turned into certified Mn ranges or claims of seawater suitability. [GAP] (yang2019theevolutionof pages 42-48)

## 2. Seawater and chloride corrosion: what changes with Mn

**Best isolated Mn series.** [CITE][NUMBERS] Yang, *The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes* (UNSW dissertation, 2019), tested homogenized binary alloys after **2 h** in stagnant, aerated, neutral **3.5 wt% NaCl at 25 °C**. Its nominal atomic compositions are converted in the dissertation to the Mn **wt%** reported here; potentials are versus SCE. Rates were calculated from polarization, **not measured 30-day penetration depths**. (yang2019theevolutionof pages 37-42, yang2019theevolutionof pages 71-76)

| Alloy, wt% Mn | Ecor, mV vs SCE | Polarization resistance, Ω·cm² | Reported rate, µm/year |
|---|---:|---:|---:|
| Cu, 0 | −304.5 | 4,155 | 92.4 |
| Cu–0.9Mn | −244.8 | 12,695 | 30.9 |
| Cu–2.2Mn | −262.8 | 14,631 | 26.8 |
| Cu–4.4Mn | −229.9 | 15,342 | **25.6** |
| Cu–8.8Mn | −252.2 | 5,819 | 73.1 |
| Cu–13.2Mn | −292.5 | 3,688 | **109.9** |

The best *binary* measured result is **4.4 wt% Mn**; **8.8 wt%** already deteriorates markedly, and **13.2 wt%** performs worse than pure Cu. These data motivate testing Mn above standard NAB concentrations, but cannot establish that **Cu–4.4Mn equals C71500**, since no matched wrought C71500 control or long-term selective-attack depth is provided. The study suggests Mn₂O₃-assisted passivation at low Mn; this is a proposed explanation, **not evidence that Mn₂O₃ is the principal protective film in NAB or Cu–Ni**. [GAP] (yang2019theevolutionof pages 71-76)

**Ni changes the interpretation.** [CITE][NUMBERS] In the same short NaCl test, approximately **Cu–4.4Mn–4.7Ni** had **83.2 µm/year**, whereas **Cu–13.3Mn–4.7Ni** had **132.4 µm/year** and lower polarization resistance (**5,413 → 3,378 Ω·cm²**). Conversely, approximately **Cu–9.0Mn–28.8Ni** gave **10.3 µm/year**, and **Cu–13.6Mn–29Ni** gave **11.1 µm/year** and **35,045 Ω·cm²**. Hence high Ni can accompany good performance even at high Mn, but the low-Ni pair directly contradicts a general claim that increasing Mn can replace Ni without corrosion penalty. These particular ternary specimens were **not assessed for long-term marine dealloying, galvanic repair interfaces or laser DED**. (yang2019theevolutionof pages 42-48, yang2019theevolutionof pages 79-83)

**NAB film and localized attack.** [CITE][NUMBERS] Ding *et al.*, “Evolution of the Corrosion Product Film on Nickel-Aluminum Bronze and Its Corrosion Behavior in 3.5 wt % NaCl Solution,” *Materials* **12**, 209 (2019), **DOI:10.3390/ma12020209**, examined cast **Cu–9.22Al–4.17Fe–4.17Ni–1.23Mn**. Its film was chiefly **Al-rich inner oxide and Cu-rich outer oxide**, described as Al₂O₃/Cu₂O; **no Mn oxide was identified as the controlling film constituent**. β′ and lamellar α+κIII regions were attacked early, while κII resisted attack; a protective film developed on severely attacked β′ by roughly **150 min**, and after **240 h** the overall film reached about **4.3 µm**. Corrosion current fell from **11.35 to 3.78 µA/cm²** over the reported initial-to-240-h comparison. These observations resolve *where an Mn-bearing NAB corrodes*, **not the causal effect of varying its Mn**. Crevice acidification can reverse the apparent protection of κ phases by dissolving their oxide. No Mn-dependent seawater velocity threshold, crevice depth or erosion–corrosion limit was established. [GAP] (ding2019evolutionofthe pages 1-3, ding2019evolutionofthe pages 3-6, ding2019evolutionofthe pages 12-14, ding2019evolutionofthe pages 6-9)

## 3. Deposition, repair and powder-production implications

**Directly relevant fusion evidence, but not the proposed laser process.** [CITE][SPEC] Dharmendra *et al.*, “Microstructural evolution and mechanical behavior of nickel aluminum bronze Cu-9Al-4Fe-4Ni-1Mn fabricated through wire-arc additive manufacturing,” *Additive Manufacturing* **30**, 100872 (2019), **DOI:10.1016/j.addma.2019.100872**, made near-full-density, well-bonded **1 wt% Mn** NAB at approximately **170 J/mm**; layer interfaces showed no reported defects or preferential cracking. As-built yield strength was **388 ± 12 MPa**, ultimate strength **685 ± 10 MPa**, and elongation **26 ± 1%**. Interpass reheating formed microstructural HAZ bands and altered κ precipitation; absence of cracks in this build does **not** prove that higher-Mn laser-powder deposits, reheated layers or NAB fusion boundaries resist solidification or liquation cracking. Its suggested **675 °C/≥6 h** corrosion-optimizing treatment is incompatible with the required *as-deposited* outcome. (dharmendra2019microstructuralevolutionand pages 14-15, dharmendra2019microstructuralevolutionand pages 13-14, dharmendra2019microstructuralevolutionand pages 2-3)

[CITE] Kim *et al.*, “Effect of Filler Metal Type on Microstructure and Mechanical Properties of Fabricated NiAl Bronze Alloy Using Wire Arc Additive Manufacturing System,” *Metals* **11**, 513 (2021), **DOI:10.3390/met11030513**, deposited ERCuNiAl (**specified in their table as 0.6–3.5 wt% Mn**) and a nominal **1.0 wt% Mn** comparison wire on cast NAB. CT found **no internal voids or cracks** in either wall. Because Al, Ni and Fe also differ between the filler ranges, this is **not an isolated Mn-versus-cracking experiment**. Available evidence does not quantify Mn-driven liquation cracking, Mn loss in remelted layers, or cracking on *wrought Cu–Ni* repair substrates. ERCuNi and ERCuAl-A2 experience cannot be assigned an Mn benefit without their certified composition and matched weld tests. [GAP] (kim2021effectoffiller pages 2-4, kim2021effectoffiller pages 4-8)

**Specific process risks to measure rather than presume solved.** [CITE] A high-temperature Cu–Mn diagram has a liquidus/solidus **minimum of 871 °C at 33.7 wt% Mn**; therefore modest Mn additions to Cu **do not themselves imply** a liquidus above the atomizer’s approximately **1,200–1,250 °C** practical limit. Added **Ni and Fe** can change the *multicomponent* liquidus, so reject or accept every full trial composition by TCCU equilibrium-liquidus and non-equilibrium freezing-range calculations, then verify by thermal analysis. Laser ablation of other Mn-bearing alloys preferentially releases Mn, establishing a credible **volatility warning**, but **not a measured Cu–Mn powder-DED loss percentage**. Compare analyzed charge, powder size fractions, deposit interior and laser-fume catch; distinguish evaporation from oxide-skimming and dilution. A historical crucible handbook lists **alumina** among possible crucibles for both Cu and Mn, but warns against silica pickup in Mn-rich alloys. It does **not** prove alumina or zirconia inertness for this induction melt, graphite compatibility, or compatibility with a Ti-alloy or Mo sonotrode. Measure O, C, Ti/Mo pickup, inclusions and sonotrode wear; surface tension and atomization-yield changes have no verified Mn-specific value for this apparatus. [GAP] (zelenaya2022computermodelof pages 1-2, schwartz1953cruciblehandbooka pages 9-10, schwartz1953cruciblehandbooka media 3b981b3e, tahir2026laserbasedsynthesisand pages 129-129)

For either repair substrate, treat the first layer as a **separate composition**: NAB dilution changes Al/Ni/Fe/Mn balance and β′/κ population; Cu–Ni dilution reduces Al/Fe/Mn where absent and shifts the intended film chemistry. Calculate dilution and the entire composition path, including the reheated interface, rather than testing only undiluted bulk coupons. This is a design requirement inferred from the documented composition-sensitive phase and corrosion behavior, **not a measured Mn-specific dilution result**. [GAP] (dharmendra2019microstructuralevolutionand pages 1-2, ding2019evolutionofthe pages 3-6)

## 4. Phase diagram, supply and safety

- **Phase equilibria.** [CITE] Cu and γ-Mn share an FCC solid-solution phase; the assessed binary has a **871 °C/33.7 wt% Mn minimum**, while Mn-rich allotrope reactions occur elsewhere in the diagram. Cu-rich binary alloys were observed single-phase through **8.8 wt% Mn**, whereas an approximately **13.2 wt% Mn** specimen contained an additional uncertain Mn-rich phase. **Neither observation is a rigorously measured maximum equilibrium solubility at a specified temperature**: quoting **13.2 wt% at 750 °C** as that maximum would misidentify a homogenized specimen as a phase boundary. Published Cu–Mn binary, Cu–Mn–Ni ternary and Cu–Al–Mn copper-rich thermodynamic assessments are identified, but **this search did not verify the installed TCCU release, its assessed ternary coverage, or COST 531 compatibility with pycalphad**. Check database phase lists and reproduce measured phase observations before imposing CALPHAD-derived limits. Zelenaya *et al.*, *Condensed Matter and Interphases* **24**, 466–474 (2022), **DOI:10.17308/kcmf.2022.24/10551**. [GAP] (zelenaya2022computermodelof pages 1-2, magnusson2017thermodynamicevaluationof pages 21-23, yang2019theevolutionof pages 42-48, magnusson2017thermodynamicevaluationof pages 28-32)
- **Criticality/cost.** [CITE] Mn is treated as a U.S. critical mineral in the **2022** framework and is retained in discussion of the **2025 final** list; Cu is a **2025 addition**, so substituting Mn for Ni does not remove critical-mineral exposure. USGS-reported estimated U.S. **2025 net import reliance for manganese ore was 100%**; *ore* import reliance is not a price or availability figure for high-purity Mn metal. An auditable contemporaneous USD/kg quotation for the actual pure metal/master alloy was **not obtained**, so assigning a numerical procurement price would conflate ore, ferroalloy and metal. Nassar *et al.*, USGS Open-File Report **2025–1047**, **DOI:10.3133/ofr20251047**. [GAP] (staff2022usgsminingreview pages 3-5, czerwinski2022criticalmineralsfor pages 4-6, nassar2025methodologyandtechnical pages 9-10)
- **Worker protection.** [CITE][NUMBERS] The cited occupational sources give an **OSHA Mn ceiling of 5 mg/m³**, **NIOSH REL 1 mg/m³ eight-hour TWA and 3 mg/m³ STEL**, and a more protective **ACGIH respirable-Mn TLV of 0.02 mg/m³ eight-hour TWA**. These are **air concentrations, not permissible Mn concentrations in powder or alloy**. Chronic inhalation can cause neurological injury. Use enclosed powder transfer, appropriate combustible-metal-powder precautions, local extraction at laser/plume and sieving stations, and breathing-zone Mn sampling; do not infer a Navy prohibition or RoHS/REACH bulk-metal composition limit from occupational limits. Flynn and Susi, *Journal of Occupational and Environmental Hygiene* **7**, 115–126 (2010), **DOI:10.1080/15459620903454600**; Ramzani *et al.*, *Health Scope* **11** (2022), **DOI:10.5812/jhealthscope.120968**. [GAP] (damato2012weldingandindustrial pages 13-15, driscoll2000healthhazardevaluation pages 23-25, damato2013the“science"of pages 13-16)

## 5. Search bounds and joint constraints

**[NUMBERS] Recommended initial *design-search* bounds, not acceptance specifications:** **functional floor 0.9 wt% Mn**, **conservative maximum 1.5 wt% Mn**, and **non-conservative maximum 4.4 wt% Mn**, for **both** Cu–Ni and aluminum-bronze candidate families. The floor is the smallest tested binary addition with a measurable short-term chloride-rate difference from Cu (**30.9 versus 92.4 µm/year**) and overlaps NAB’s established 0.8–1.5 wt% use; it does **not** prove that 0.9 wt% benefits every Ni/Al/Fe background. The conservative ceiling comes from the documented C95800/ASTM B148 range, rather than extrapolating the broader ERCuNiAl filler range to every alloy family. The aggressive **4.4 wt%** ceiling is the measured binary chloride optimum and remains below the binary **8.8 wt%** deterioration point; applying it to Cu–Ni or Al bronze is an **experimental hypothesis**, not an established marine grade. In particular, low-Ni ternary results caution that **4.4 wt% Mn can perform poorly even though Cu–4.4Mn performed well**. Neither upper bound overrides a full-alloy liquidus, oxygen/inclusion, crack, or 30-day selective-attack rejection gate. No *impurity-only* limit applies because the decision is INCLUDE. (yang2019theevolutionof pages 71-76, yang2019theevolutionof pages 79-83, dharmendra2019microstructuralevolutionand pages 2-3)

**[CITE] Joint constraints to carry forward:** retain Fe **in solution** when assessing Cu–Ni flow-film performance; evaluate **Ni/Fe** and **Al plus Mn’s β-stabilizing effect** when screening NAB, and do not trade Ni down on the strength of Cu–Mn binary corrosion alone. Flag α+τ in tested Cu–Mn–Ni compositions, retained β′/α+κIII for localized NAB attack, and high Mn together with Zn/Al for possible selective dissolution. These are *conditional interactions*, not a validated universal Mn+Ni, Mn/Fe or Mn+Al numerical inequality. The reported NAB comparison favored approximately **5 wt% Ni versus 4 wt% Fe**, but that should not be misrepresented as an experimentally optimized Mn ratio. Test each shortlisted powder **as deposited** against wrought C71500 in the same seawater protocol and record both area-average loss and **maximum selective-attack depth**, including each dissimilar interface. [GAP] (parvizi1985photoelectronandelectrochemical pages 33-37, cuevas2002microstructurecharacterizationof pages 21-26, yang2019theevolutionof pages 42-48, ding2019evolutionofthe pages 3-6)

**Evidence grade: moderate for inclusion in the *search*, thin for the specified final qualification.** Controlled Mn-dependent evidence is short-duration NaCl electrochemistry, while dense deposition evidence is largely wire-arc NAB with multiple other alloying elements; long-term natural seawater, flow/crevice behavior, the specified atomizer and laser, matched low-Ni substitutions, and as-deposited cross-substrate comparison with C71500 remain unproven. No publication by the identified PI is used. (yang2019theevolutionof pages 71-76, dharmendra2019microstructuralevolutionand pages 14-15, yang2019theevolutionof pages 79-83)

VERDICT | Mn | decision=INCLUDE | family=both | conservative_max_wt=1.5 | nonconservative_max_wt=4.4 | floor_wt=0.9 | impurity_max_wt=NA | evidence=moderate

References

1. (yang2019theevolutionof pages 71-76): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

2. (yang2019theevolutionof pages 79-83): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

3. (dharmendra2019microstructuralevolutionand pages 14-15): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

4. (parvizi1985photoelectronandelectrochemical pages 33-37): MS Parvizi. Photoelectron and electrochemical studies of the corrosion of a copper-nickel alloy. Unknown journal, 1985.

5. (parvizi1985photoelectronandelectrochemical pages 37-41): MS Parvizi. Photoelectron and electrochemical studies of the corrosion of a copper-nickel alloy. Unknown journal, 1985.

6. (dharmendra2019microstructuralevolutionand pages 2-3): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

7. (kim2021effectoffiller pages 2-4): Jae Won Kim, Jae-Deuk Kim, Joo-Yong Cheon, and Changwook Ji. Effect of filler metal type on microstructure and mechanical properties of fabricated nial bronze alloy using wire arc additive manufacturing system. Metals, 11:513, Mar 2021. URL: https://doi.org/10.3390/met11030513, doi:10.3390/met11030513. This article has 17 citations.

8. (dharmendra2019microstructuralevolutionand pages 1-2): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

9. (ding2019evolutionofthe pages 1-3): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

10. (ding2019evolutionofthe media f3cdbb72): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

11. (yang2019theevolutionof pages 42-48): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

12. (yang2019theevolutionof pages 37-42): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

13. (ding2019evolutionofthe pages 3-6): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

14. (ding2019evolutionofthe pages 12-14): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

15. (ding2019evolutionofthe pages 6-9): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

16. (dharmendra2019microstructuralevolutionand pages 13-14): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

17. (kim2021effectoffiller pages 4-8): Jae Won Kim, Jae-Deuk Kim, Joo-Yong Cheon, and Changwook Ji. Effect of filler metal type on microstructure and mechanical properties of fabricated nial bronze alloy using wire arc additive manufacturing system. Metals, 11:513, Mar 2021. URL: https://doi.org/10.3390/met11030513, doi:10.3390/met11030513. This article has 17 citations.

18. (zelenaya2022computermodelof pages 1-2): A. E. Zelenaya, V. I. Lutsyk, and V. D. Baldanov. Computer model of cu-ni-mn isobaric phase diagram: verification of crystallisation intervals and change of the three-phase reaction type. Конденсированные среды и межфазные границы, 24:466-474, Jan 2022. URL: https://doi.org/10.17308/kcmf.2022.24/10551, doi:10.17308/kcmf.2022.24/10551. This article has 1 citations.

19. (schwartz1953cruciblehandbooka pages 9-10): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

20. (schwartz1953cruciblehandbooka media 3b981b3e): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

21. (tahir2026laserbasedsynthesisand pages 129-129): S Tahir. Laser-based synthesis and sintering of binary, ternary, and compositionally complex alloy nanoparticles for magnetocaloric cooling/submitted by: shabbir tahir from …. Unknown journal, 2026.

22. (magnusson2017thermodynamicevaluationof pages 21-23): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

23. (magnusson2017thermodynamicevaluationof pages 28-32): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

24. (staff2022usgsminingreview pages 3-5): US Staff. Usgs mining review. Unknown journal, 2022.

25. (czerwinski2022criticalmineralsfor pages 4-6): Frank Czerwinski. Critical minerals for zero-emission transportation. Materials, 15:5539, Aug 2022. URL: https://doi.org/10.3390/ma15165539, doi:10.3390/ma15165539. This article has 45 citations.

26. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

27. (damato2012weldingandindustrial pages 13-15): V D'Amato and M McCullion. Welding and industrial hygiene: the welding process and lessons learned. Unknown journal, 2012.

28. (driscoll2000healthhazardevaluation pages 23-25): RJ Driscoll and M Kiefer. Health hazard evaluation report: heta 2000-0185-2808: thyssen-dover elevator, middleton, tennessee. Unknown journal, 2000.

29. (damato2013the“science"of pages 13-16): V D'Amato and M McCullion. The “science" of the welding process and exposure assessments. Unknown journal, 2013.

30. (cuevas2002microstructurecharacterizationof pages 21-26): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.
