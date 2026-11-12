<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: f62e43c2-c199-4560-ac22-b549fee8c7b5
- Submitted: 2026-10-17T19:01:54Z
- Fetched: 2026-10-17T19:23:10Z (status: success)
- Raw trajectory JSON: ../raw/el-46-Pr.json.gz
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

ELEMENT UNDER REVIEW: Pr (rare earth). Praseodymium additions to copper alloys, if any.

Answer for Pr specifically, not for copper alloys in general:
1. ROLE: what Pr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Pr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Pr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Pr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Pr, Cu-Ni-Pr and Cu-Al-Pr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Pr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Pr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Pr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Pr (rare earth). Praseodymium additions to copper alloys, if any.

Answer for Pr specifically, not for copper alloys in general:
1. ROLE: what Pr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Pr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Pr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Pr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Pr, Cu-Ni-Pr and Cu-Al-Pr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Pr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Pr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Pr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Praseodymium in seawater-service copper-alloy DED

**Decision: EXCLUDE Pr as a designed addition from both Cu–Ni and aluminum-bronze composition palettes.** A Cu–Pr phase assessment establishes that Pr can form copper intermetallics, but the retrieved evidence does not establish a Pr concentration that improves *as-deposited* seawater resistance, produces crack-free Cu-alloy DED, or survives the specified powder-making route reproducibly. Exclusion is a decision about the **designed search space**, not a claim that analytically detectable Pr makes an alloy unacceptable. No defensible numerical Pr impurity ceiling was found. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3, wahyudi2015reviewingtheproperties pages 8-10)

The evidence matrix separates measured or documented facts from questions that remain unanswered.

| Question | Verified result | Constraint and evidence quality |
|---|---|---|
| Commercial or Navy Cu alloys and filler specifications | No Pr range was identified in the reviewed compositions for seawater Cu-Ni, aluminum-bronze or NAB, Mn-Al-bronze, tin-bronze or gunmetal, brass, Cu-Ni-Sn, Cu-Ni-Si, or AWS A5.7 Cu-alloy fillers. “Not specified” is **not** a zero-tolerance impurity limit. | [SPEC] No standards-derived Pr maximum was found. Evidence is thin and does not justify inventing a ppm limit. |
| Seawater corrosion | No quantitative Pr-alloying study was found for natural or substitute seawater or 3.5 wt% NaCl: no verified corrosion rate, corrosion potential, polarization resistance, impedance, pitting or crevice potential, selective attack, erosion-corrosion, or velocity limit. | [GAP] No beneficial or harmful Pr range can be assigned. Pr-containing conversion coatings and inhibitors are not evidence for Pr dissolved in a Cu alloy. |
| DED and welding | No Pr-specific Cu-alloy DED, weld-metal, or cladding evidence was found for solidification cracking, reheated-layer liquation cracking, porosity, composition loss, or dilution into C95800 NAB or wrought Cu-Ni. No Pr effect was identified in ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl fillers. | [GAP] Magnet-alloy AM is not transferable evidence. Laser PBF of an Fe-Nd-B alloy containing 1.4 wt% Pr showed cracking, porosity, oxidation, and phase inhomogeneity, but its matrix and mechanisms differ from Cu alloys (wilms2026hightemperatureadditivemanufacturing pages 1-2). |
| Cu-Pr phases | Equilibrium literature supports several Cu-Pr intermetallic stoichiometries, including Cu-rich PrCu6. PrCu13 was reported only after rapid quenching, described as possibly metastable, and assigned a proposed NaZn13 structure without XRD confirmation. Riani et al., DOI: **10.1361/105497102770332171** (riani2002ternaryrareearth pages 2-3). | [CITE] PrCu6 is documented; PrCu13 remains uncertain and cannot establish a dilute-alloy design bound. |
| Maximum Pr solubility and Cu-rich invariants | No verified numerical maximum solid solubility of Pr in Cu, corresponding temperature, or Cu-rich eutectic or peritectic composition and temperature was recovered. | [GAP] These values must remain **NA**. Intermetallic stoichiometry is not a defensible DED composition bound. |
| CALPHAD and database coverage | A published binary thermodynamic assessment calculated Cu-Pr phase equilibria and optimized parameters: Zhuang et al., DOI: **10.1007/BF02665998**. The assessment is independently summarized by Riani et al. (riani2002ternaryrareearth pages 1-2). | [GAP] Cu-Ni-Pr and Cu-Al-Pr ternary assessments, a reusable published TDB, and implementation in Thermo-Calc TCCU or COST 531 were not verified. A binary assessment does not establish pycalphad or TCCU availability. |
| Liquidus and atomizer ceiling | No verified calculation shows that a particular dilute Pr addition drives a candidate Cu-Ni or Cu-Al alloy above 1,250 °C. The stated approximately 1,200–1,250 °C useful-superheat ceiling is an **equipment constraint**, not a measured Pr chemical threshold. | [GAP] Calculate each full multicomponent composition only after obtaining validated Pr-containing parameters. Do not infer a Pr maximum from the machine ceiling alone. |
| Melting, oxidation, and powder handling | Elemental Pr tarnishes and reportedly burns readily at about **150 °C**, forming mixed Pr(III,IV) oxide; it also reacts with water. Wahyudi, DOI: **10.30556/imj.vol18.no2.2015.293** (wahyudi2015reviewingtheproperties pages 8-10). | [NUMBERS] This supports a qualitative warning for oxygen pickup, inclusions, powder ignition, and laser fume. No Cu-Pr-specific data were found for alumina, zirconia, or graphite crucibles; Ti or Mo sonotrodes; vapor loss; or surface tension. |
| U.S. critical-mineral status | Pr appears explicitly on the final 2025 U.S. critical-minerals list, and copper was added in 2025. The supporting methodology is USGS OFR 2025-1047, DOI: **10.3133/ofr20251047** (nassar2025methodologyandtechnical pages 9-10, nassar2025methodologyandtechnical pages 1-4, staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 3-5). | [NUMBERS] [NAVY] The final list was published November 7, 2025, and contains 60 commodities. Supply risk weighs against an unsupported designed Pr addition. |
| Bounds and decision | **EXCLUDE** Pr from the designed search palette. Conservative maximum = **NA**; non-conservative maximum = **NA**; functional floor = **NA**; impurity maximum = **NA**. | [GAP] Failure modes are unquantified seawater performance, potentially brittle or galvanically distinct intermetallics, oxidation and inclusions, powder-fire risk, uncertain cracking, absent ternary thermodynamics, and added critical-mineral dependence. No evidence-based numerical impurity ceiling is available; control Pr through supplier disclosure and measured chemistry rather than an invented limit. |


*Table: Verified evidence and explicit gaps governing Pr in Cu-based maritime DED alloys. The matrix distinguishes documented Cu-Pr phase and supply facts from unsupported corrosion, welding, database, and numerical-bound claims.*

## 1. Role, alloy families, and specifications

[CITE] Cu–Pr is not simply a dilute solid-solution system: the assessed phase literature identifies Pr–Cu compounds including PrCu₆, PrCu₅, PrCu₄, PrCu₂, and PrCu. The Cu-richest *reported* phase, PrCu₁₃, was obtained by rapid quenching and was described as possibly metastable; its proposed structure was not confirmed by X-ray diffraction. These phases establish a potential route to Pr-rich interdendritic material, **not** a demonstrated beneficial precipitate in a seawater Cu alloy. Riani *et al.*, *Journal of Phase Equilibria* **23** (2002) 7–28, DOI **10.1361/105497102770332171**. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3)

[GAP] No verified Pr-specific role or concentration was recovered for Cu–Ni, aluminum bronze/NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. In particular, Pr-controlled Cu₂O/NiO/Al₂O₃ seawater-film chemistry, dealloying inhibition, solid-solution strengthening, and grain refinement in those matrices remain **unproved**. Older copper-metallurgy evidence concerns **Ce**, not Pr: a Cu–40 Zn–1 Pb brass treated with 0.1 wt% Ce showed improved hot ductility, whereas industrial addition of mixed rare earths caused gas blisters and scrap. It cannot establish a Pr floor, benefit, or safe ceiling. Savitskii, *Metal Science and Heat Treatment of Metals* **3** (1961) 391–400, DOI **10.1007/BF00812593**. (savitskii1961theproblemof pages 9-10)

[SPEC] **No Pr-containing commercial or Navy copper alloy and no specification-assigned Pr range in wt% was verified.** This applies to the requested ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449, and UNS/CDA candidates. This search result must **not** be represented as a clause-by-clause certification of every current standard edition, or as a specification limit of 0 wt% Pr. (riani2002ternaryrareearth pages 1-2, savitskii1961theproblemof pages 9-10)

## 2. Seawater corrosion

[GAP] **No quantitative Pr-versus-Pr-free comparison was verified** for a copper-base alloy in natural seawater, ASTM D1141 substitute ocean water, or 3.5 wt% NaCl. Consequently there is no defensible helpful or harmful Pr interval, corrosion rate, Δ*E*₍corr₎, polarization or film resistance, pit/crevice threshold, selective-attack depth, erosion–corrosion result, or flow-velocity limit. There is likewise no evidence that Pr permits a lower Ni concentration while maintaining the as-deposited performance of wrought C71500. Pr supplied as an aqueous inhibitor or conversion-coating ingredient is **not** an alloying experiment and cannot answer that comparison. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3)

## 3. DED, welding, and repair dilution

[GAP] No Pr-controlled copper-alloy laser DED, weld, or cladding comparison was verified for solidification cracking, reheated-layer liquation cracking, porosity, Pr evaporation/oxidation loss, or chemical dilution into **cast C95800 NAB** versus **wrought Cu–Ni**. Nor was a Pr-specific effect verified for ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl weld metal. Interdendritic enrichment, Pr oxide inclusions, and local galvanic differences are **risks to test**, not observed failure rates or a basis for a numerical bound. Dilution also makes a single nominal powder composition an inadequate proxy for first-layer interface chemistry. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3, wahyudi2015reviewingtheproperties pages 8-10)

[CITE] A deliberately **non-transferable comparator** illustrates why an AM citation must be read by matrix: laser powder-bed fusion of an Fe–Nd–B magnet powder containing **1.4 wt% Pr** exhibited substantial cracking and porosity, while electron-beam processing of that powder produced dense parts. Neither result isolates Pr's effect nor predicts Cu-alloy DED. Wilms *et al.*, *Progress in Additive Manufacturing* **11** (2026) 3961–3979, DOI **10.1007/s40964-026-01561-7**. (wilms2026hightemperatureadditivemanufacturing pages 1-2)

## 4. Powder production and melt handling

[NUMBERS] Elemental Pr oxidizes on exposure to air and is reported to burn readily at approximately **150 °C**, yielding mixed-valence Pr oxide; it reacts with water. This supports precautions against oxygen pickup, reactive fine powder, and laser-generated particulate, but **150 °C is not an ignition temperature measured for Cu–Pr powder**. Wahyudi, *Indonesian Mining Journal* **18** (2015) 92–108, DOI **10.30556/imj.vol18.no2.2015.293**. (wahyudi2015reviewingtheproperties pages 8-10)

[GAP] No measured Pr recovery or inclusion population was found for approximately 0.5 kg induction melts in **alumina versus zirconia** under Ar, graphite contact, or contact with a **Ti-alloy versus Mo sonotrode**. Pr-induced crucible reduction/reaction, vapor-loss rate, changes in liquid surface tension and ultrasound atomization, and oxidation during 1.07-µm laser exposure therefore cannot be ranked quantitatively. A mass balance should compare charged metal, retained melt, segregated dross, size-classified powder, and deposit chemistry; that is a proposed verification method, **not** an existing Pr result. The approximately **1,200–1,250 °C** practical liquidus limit is the specified equipment constraint, not a measured Pr composition limit. (wahyudi2015reviewingtheproperties pages 8-10, riani2002ternaryrareearth pages 1-2)

## 5. Phase diagrams and CALPHAD

[CITE] **A published Cu–Pr binary assessment exists:** Zhuang, Qiao, Wei, and Shen, “Thermodynamic evaluation of the Cu–R (R: Ce, Pr, Nd, Sm) binary systems,” *Journal of Phase Equilibria* **17** (1996) 508–521, DOI **10.1007/BF02665998**. Riani *et al.* independently describe its optimized parameters and calculated diagrams. A published assessment does **not** establish that its parameter file is distributed as a usable TDB. (riani2002ternaryrareearth pages 1-2)

[NUMBERS] [GAP] **Maximum equilibrium Pr solubility in Cu: unavailable in verified wt% and temperature. Cu-rich invariant reaction temperature and composition: unavailable.** Do not substitute the stoichiometric **PrCu₆ composition of approximately 27.0 wt% Pr**—calculated from atomic masses—for solubility or for a practicable additive concentration. Formation of Cu-rich compounds makes an interdendritic low-melting constituent a concern, but the retrieved evidence does **not** show that adding any specified dilute wt% Pr raises a Cu–Ni or Cu–Al alloy's liquidus beyond **1,250 °C**; the full-base-alloy composition and validated phase description are required. PrCu₁₃ remains particularly unsuitable as an equilibrium constraint. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3)

[GAP] Inclusion of **Pr in Thermo-Calc TCCU or COST 531**, and assessed **Cu–Ni–Pr or Cu–Al–Pr** ternaries, could not be verified. Before a pycalphad screen, inspect the installed database element list, phase definitions, assessed ternary interactions, and liquidus predictions for the actual candidate compositions. Do not treat a Cu–Pr binary extrapolation as validation of NAB-interface phase fractions or cracking. (riani2002ternaryrareearth pages 1-2)

## 6. Supply, cost, and safety

[NUMBERS] [CITE] Pr is explicitly present on the **final 2025 U.S. List of Critical Minerals**, published **7 November 2025**; copper is also listed and was among the additions recommended relative to the 2022 list. The final 2025 list contains **60 commodities**, versus **50** in 2022. USGS, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, Open-File Report **2025-1047**, DOI **10.3133/ofr20251047**; USGS, “Annual Review 2025: Mining,” *Mining Engineering* (May 2026), citing **90 FR 50494**. Critical-mineral designation identifies supply exposure; it does not constitute an alloy or Navy approval. (nassar2025methodologyandtechnical pages 9-10, staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 3-5)

[GAP] A trustworthy **Pr-metal-specific approximate USD/kg price** for a specified purity, form, quantity, location, and date was not established; Nd or mixed Nd–Pr oxide quotations must not be mislabeled as Pr metal prices. No Pr-specific OSHA permissible exposure limit, Pr ban under RoHS/REACH, or Navy prohibition on Pr in copper fillers was verified. Avoid inventing one. Require supplier SDS review, oxygen-controlled powder transfer, combustible-metal-dust controls, local extraction/filtration for laser fume, and task-specific industrial-hygiene assessment; elemental Pr's documented reactivity is the reason for caution, not evidence of a measured exposure threshold in this process. (wahyudi2015reviewingtheproperties pages 8-10, gomołka2026theavailabilityof pages 3-5)

## 7. Bounds, interactions, and evidence quality

**Bound decision — EXCLUDE; family: none.** The conservative maximum, aggressive maximum, and functional floor are each **NA wt%**: there is no established Pr-bearing maritime Cu-alloy specification, Pr-specific corrosion improvement, or Cu-alloy AM/cladding outcome from which to derive them. **Impurity maximum: NA wt%** rather than an invented ppm figure: none of the examined evidence supplies a tolerable Pr threshold for either powder or deposit. Specify *no intentional Pr addition*, require reporting of adventitious Pr in charge materials and powder, and revisit analytical control only if supplier chemistry establishes a recurring source. The constraining failure modes are **unresolved**, rather than experimentally located: Pr-rich interdendritic phases and reheating response, oxide inclusions and porosity, possible local selective attack, powder handling, and uncertain interfacial dilution. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3, savitskii1961theproblemof pages 9-10, wahyudi2015reviewingtheproperties pages 8-10)

[GAP] **Interactions for later joint constraints:** no validated Pr:Ni, Pr:Fe, Pr:Mn, Pr:Al, or combined rare-earth/oxygen/sulfur ratio was found. Treat Ni/Fe/Mn/Al-dependent phase stability, Pr–O inclusion formation, Pr recovery, and substrate dilution as unmeasured interactions; do not claim that Pr neutralizes sulfur, improves NAB κ-phase chemistry, or compensates for reduced Ni on the basis of Ce or mixed-rare-earth observations. Evidence is **thin for the requested application**, despite the comparatively credible binary phase and elemental-oxidation literature. (riani2002ternaryrareearth pages 1-2, savitskii1961theproblemof pages 9-10, wahyudi2015reviewingtheproperties pages 8-10)

VERDICT | Pr | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (riani2002ternaryrareearth pages 1-2): P. Riani, D. Mazzone, G. Zanicchi, R. Marazza, and R. Ferro. Ternary rare earth germanium systems with cu and ag—a review and a contribution to their assessment. Journal of Phase Equilibria, 23:7-28, Feb 2002. URL: https://doi.org/10.1361/105497102770332171, doi:10.1361/105497102770332171. This article has 6 citations.

2. (riani2002ternaryrareearth pages 2-3): P. Riani, D. Mazzone, G. Zanicchi, R. Marazza, and R. Ferro. Ternary rare earth germanium systems with cu and ag—a review and a contribution to their assessment. Journal of Phase Equilibria, 23:7-28, Feb 2002. URL: https://doi.org/10.1361/105497102770332171, doi:10.1361/105497102770332171. This article has 6 citations.

3. (wahyudi2015reviewingtheproperties pages 8-10): T. Wahyudi. Reviewing the properties of rare earth element-bearing minerals, rare earth elements and cerium oxide compound. ArXiv, 18:92-108, 2015. URL: https://doi.org/10.30556/imj.vol18.no2.2015.293, doi:10.30556/imj.vol18.no2.2015.293. This article has 15 citations.

4. (wilms2026hightemperatureadditivemanufacturing pages 1-2): Markus Benjamin Wilms, Natalia Shkodich, Hamed Shokri, Bilal Gökce, Michael Farle, Pavel Krakhmalev, and Silja-Katharina Rittinghaus. High-temperature additive manufacturing of nd-fe-b by powder bed fusion. Progress in Additive Manufacturing, 11:3961-3979, Feb 2026. URL: https://doi.org/10.1007/s40964-026-01561-7, doi:10.1007/s40964-026-01561-7. This article has 0 citations and is from a peer-reviewed journal.

5. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

6. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

7. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

8. (staff2022usgsminingreview pages 3-5): US Staff. Usgs mining review. Unknown journal, 2022.

9. (savitskii1961theproblemof pages 9-10): E. M. Savitskii. The problem of rare earth metals. Metal Science and Heat Treatment of Metals, 3:391-400, Sep 1961. URL: https://doi.org/10.1007/bf00812593, doi:10.1007/bf00812593. This article has 3 citations.

10. (gomołka2026theavailabilityof pages 3-5): Krystyna Gomółka and Piotr Kasprzak. The availability of rare earth elements and the development of electromobility industry in european union. Economics and Environment, 98:1473, Oct 2026. URL: https://doi.org/10.34659/eis.2026.98.3.1473, doi:10.34659/eis.2026.98.3.1473. This article has 0 citations.
