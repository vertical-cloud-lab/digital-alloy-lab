<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 850dc22f-484e-484d-b52e-a87f5a6fc3a7
- Submitted: 2026-10-17T19:00:15Z
- Fetched: 2026-10-17T19:33:12Z (status: success)
- Raw trajectory JSON: ../raw/el-29-O.json.gz
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

ELEMENT UNDER REVIEW: O (interstitial / gas). Oxygen in copper powder and deposits: oxygen-free vs tough-pitch copper, Cu2O, steam porosity with hydrogen, oxide films on powder; no literature-certified oxygen limit for copper DED powder was found earlier. Answer as an impurity limit in ppm for powder and deposit, and say which deoxidizers (Al, Mn, Ti, Si, P, B, Mg, Li) control it.

Answer for O specifically, not for copper alloys in general:
1. ROLE: what O does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their O ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how O changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-O, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-O, Cu-Ni-O and Cu-Al-O are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of O in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that O neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | O | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: O (interstitial / gas). Oxygen in copper powder and deposits: oxygen-free vs tough-pitch copper, Cu2O, steam porosity with hydrogen, oxide films on powder; no literature-certified oxygen limit for copper DED powder was found earlier. Answer as an impurity limit in ppm for powder and deposit, and say which deoxidizers (Al, Mn, Ti, Si, P, B, Mg, Li) control it.

Answer for O specifically, not for copper alloys in general:
1. ROLE: what O does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their O ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how O changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-O, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-O, Cu-Ni-O and Cu-Al-O are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of O in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that O neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | O | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Oxygen (O): impurity constraint for marine copper-alloy DED

**Decision: LIMIT, for both Cu–Ni and aluminium-bronze candidates.** Specify **≤0.013 wt% O (130 mass-ppm) in the delivered powder** and **≤0.013 wt% O in the as-deposited material**, measured separately by inert-gas fusion. These are **proposed research acceptance limits, not an ASTM, AWS, Navy, or literature-certified DED specification**. The numerical anchor is an ultrasonic-atomized CuAl10Fe5Ni5 powder measured at **0.013 wt% O** in a study preparing feedstock for DED; its deposit oxygen content and seawater performance were *not* established. Screen preferentially for **≤0.005 wt% (50 ppm)** where practical, particularly for Cu–Ni repairs, and measure hydrogen and powder-surface oxide independently. Do not reject an otherwise sound alloy solely because it exceeds this provisional threshold: a controlled powder/deposit/defect/corrosion study must determine the actual limit. Oxygen is not a useful intentional bulk addition for the proposed seawater alloys; the protective oxides principally form **from the environment after deposition**, whereas pre-existing oxide can become an inclusion or gas-pore source. [NUMBERS] [GAP] (uhlmann2024acomparativeevaluation pages 10-12, jin2019surfacecharacterizationand pages 1-3, toth2021electronbeamwelding pages 2-4)

## 1. Metallurgical role and specifications

O has negligible useful *bulk solid-solution* role in copper: a copper LPBF study cites an equilibrium solid solubility of **up to approximately 2 mass-ppm (0.0002 wt%)**, without identifying the temperature of that maximum. Oxygen above its solubility is principally associated with **Cu₂O/CuO**, powder-surface oxide, or oxides of other alloying elements, not an O-bearing strengthening intermetallic. Copper-oxide nanoparticles did strengthen one deliberately oxidized, *pure-copper LPBF* material, but that does not demonstrate corrosion-resistant Cu–Ni or bronze DED. O is not an established grain-refining or dealloying-inhibiting addition for these families. [CITE] [GAP] (jadhav2020mechanicalandelectrical pages 4-6, jadhav2020mechanicalandelectrical pages 6-10)

| Material or specification | O in metal, wt% | What the number establishes |
|---|---:|---|
| UNS C10100 oxygen-free electronic copper, ASTM B170 | **≤0.0005** (≤5 ppm) | A **specified limit for this unalloyed grade**, not for Cu–Ni or bronze powder. [SPEC] (bastidas2019corrosionofcopper pages 1-2) |
| Cu-ETP/CW004A, commonly associated with C11000 | **Up to approximately 0.04** (400 ppm) is a reported commercial/welding reference; approximately **0.02 or less** is described for modern cathode-derived copper | Oxygen-bearing tough-pitch practice, **not a naval-alloy O allowance**; one copper-industry account says the oxygen content of its cited ETP product standard is *not itself specified*. [NUMBERS] (toth2021electronbeamwelding pages 2-4, coppers1999copperdevelopmentassociation pages 47-50, coppers1999copperdevelopmentassociation pages 40-43) |
| Phosphorus-deoxidized Cu-DHP/CW024A, C12200 family | **No numerical O range established here**; residual **P 0.015–0.040** | P is used to remove residual oxygen; **P content must not be reported as O content**. [NUMBERS] (coppers1999copperdevelopmentassociation pages 47-50) |
| High-strength, vacuum-refined C71500 research alloy | **<0.0005** (<5 ppm O) reported alongside C and S reduced below 5 ppm | A **research-material preparation**, not the C71500 specification. [NUMBERS] (gao2022corrosionbehaviorof pages 1-2) |
| CuAl10Fe5Ni5 ultrasonic-atomized bronze powder | **0.013** (130 ppm); a *different-composition* gas-atomized comparison powder measured **0.019** (190 ppm) | Measured powders, **not permissible O ranges or measured deposits**. [NUMBERS] (uhlmann2024acomparativeevaluation pages 10-12) |

[NAVY] The relevant marine product/filler designations include wrought C70600 and C71500 (ASTM **B111/B171/B466**, as applicable), cast NAB **C95800** (ASTM **B148**), cast Cu–Ni (ASTM **B369**), and the **AWS A5.7** filler classes ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl; associated military procurement requirements can include **MIL-T-16420, MIL-B-24480, and MIL-C-15726**. **No verified numerical *bulk-O* requirement from those named alloy/filler specifications is available in the retrieved evidence.** Do not assign C10100’s limit, an ETP range, or a powder measurement to any of them. Nor was an O range verified for Mn–Al bronze, tin bronze/gunmetal, brasses, Cu–Ni–Sn, or Cu–Ni–Si: oxygen is a melt/powder contamination and oxide-control concern in these families, not a demonstrated seawater-beneficial designed addition. Verify current editions and applicable procurement clauses before asserting specification compliance. [SPEC] [GAP] Welding experience explicitly pairs CDA715 with ERCuNi and CDA613 aluminium bronze with ERCuAl-A2; this is **not** an oxygen specification for either filler. (robitz1990closuredevelopmentfor pages 49-52, robitz1990closuredevelopmentfor pages 17-20, francis1970chapter6– pages 11-14)

**Deoxidizers and joint constraints.** [CITE] P is the established copper deoxidizer: Cu-DHP retains **0.015–0.040 wt% P**, but residual P can cost conductivity, and a casting reference discourages P for aluminium bronze because of phosphides, ductility loss and hot shortness. Al already deoxidizes aluminium-bronze melts; extra Al does **not** erase entrained Al₂O₃ films. Mn and B may improve oxide flotation in aluminium bronze but **cannot reduce existing Al₂O₃**; B can cause hard spots. Mg reacts with O and S in nickel-bronze casting; Li is reported to scavenge O and H. Si deoxidation can carry mechanical-property penalties. Ti is oxygen-affine, but an experimentally demonstrated Ti-based oxygen target or superiority in *these* powders was not found. Any Al, Mn, Ti, Si, P, B, Mg or Li used to bind O transfers it into an oxide/dross/inclusion unless the product is removed: a low *dissolved*-O calculation is not proof of clean powder. Do not prescribe additive masses from oxide stoichiometry alone; recovery, oxygen activity, oxide flotation and the resulting alloy chemistry need measurement. [GAP] (francis1970chapter6– pages 11-14, coppers1999copperdevelopmentassociation pages 47-50, francis1970chapter6– pages 14-18)

## 2. Seawater: distinguish dissolved oxygen from oxygen in the alloy

**No retrieved study varies only the *bulk O content* of an otherwise identical Cu–Ni, NAB or marine-bronze deposit and reports corrosion rate, E_corr, film resistance, selective-attack depth, pitting, crevice corrosion, or erosion threshold. Consequently there is no measured bulk-O interval that demonstrably helps seawater corrosion, or a measured seawater-derived bulk-O harm threshold.** Numbers for oxygen dissolved *in seawater* must not be used as alloy-composition bounds. [GAP] (lewis1981evaluationofcoppernickel pages 19-21, lewis1981evaluationofcoppernickel pages 14-17, takaloo2011corrosionbehaviorof pages 2-3)

[CITE] In Cu–Ni, oxygen reduction sustains the cathodic reaction, while environmental exposure develops a predominantly Cu₂O-containing film. Ni and Fe incorporation changes its electrical/ionic resistance; this is an interaction of **Ni/Fe and the corrosion-product film**, not proof that feedstock O should be increased. Lewis and LaQue report typical low-velocity C70600/C71500 corrosion of approximately **2.5–12.7 µm/year**, decreasing to **<2.5 µm/year** on long exposure; ordinary seawater dissolved-O variation of **1–6 mL/L** did not significantly change the reported corrosion rates. C70600 had good service resistance up to approximately **3.0 m/s** under the cited conditions; these are **not O-dependent velocity limits**. Dissolved oxygen can aid protective-film growth *and* accelerate cathodic reduction and oxidation toward less protective cupric products. Sulfide-polluted simulated seawater suppressed protective Cu₂O in one C71500 study and yielded approximately **0.15 mm/year initially**, falling to **0.09 mm/year after 168 h**: these are pollution effects, not a bulk-O comparison. [NUMBERS] (lewis1981evaluationofcoppernickel pages 21-24, lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 17-19, gao2022corrosionbehaviorof pages 1-2, lewis1981evaluationofcoppernickel pages 19-21)

[CITE] For aluminium bronze/NAB, the protective surface can involve Cu₂O and Al-bearing oxide/hydroxide, while exposed microstructural phases and film breakdown permit selective attack and pitting. A cast **C95520**, *not C95800*, experiment used ASTM D1141 artificial seawater with about **7 ppm dissolved O** and found that heat-treatment-dependent microstructure changed protection. This is an environmental oxygen concentration, **not 7 ppm O in the bronze**; its heat-treatment result cannot be assumed for an as-deposited repair. Likewise, a 90/10 Cu–Ni experiment reported E_corr changing from **−0.249 to −0.198 V** and i_corr from **3.812 to 1.056 µA/cm²** over **56 days**, but its solution included **0.5 mol/L H₂O₂ added to natural seawater** and injected oxygen. It is an accelerated *film-aging* comparison, **not ordinary seawater or an alloy-O dose–response**. [NUMBERS] [GAP] (takaloo2011corrosionbehaviorof pages 2-3, jin2019surfacecharacterizationand pages 3-5, jin2019surfacecharacterizationand pages 8-11)

## 3. DED, repair and powder production

**Fusion evidence, with its limits.** [CITE] In an electron-beam *welding* comparison—not laser DED—measured copper feedstock O was **0.0035 wt% (35 ppm)** for the nominal oxygen-free grade versus **0.0179 wt% (179 ppm)** for tough-pitch copper. Optimized oxygen-free welds had almost no detected pores, whereas tough-pitch welds contained **49–112 pores** and **0.071–0.336 mm³ total detected pore volume** per tested specimen. This supports minimizing O but **does not prove that 130 ppm is a crack-free DED threshold**. Hydrogen and nitrogen were each reported below 10 ppm in that experiment, so its authors did **not** establish that all these pores were steam pores. Conversely, when hydrogen contacts Cu₂O, **Cu₂O + H₂ → 2Cu + H₂O** can generate trapped high-pressure steam, blisters and embrittlement. Welding studies also show that shielding moisture and nitrogen entrainment matter independently. [NUMBERS] (toth2021electronbeamwelding pages 4-6, toth2021electronbeamwelding pages 10-12, toth2021electronbeamwelding media 4edfff5d, nyborg2022surfacechemicaland pages 8-8, littleton1974nitrogenporosityin pages 1-2, coppers1999copperdevelopmentassociation pages 47-50)

An important counterexample prevents claiming that all oxygen-bearing copper inevitably cracks: deliberately surface-oxidized **pure-Cu LPBF** powder contained **0.200 wt% O (2,000 ppm)** and produced approximately **0.210–0.220 wt% O** in dense parts. Its 1080-nm powder absorptivity increased **32% → 58%**. That experiment did **not** establish seawater resistance, DED multilayer repair, or suitability of oxide-bearing Cu–Ni/NAB powder. It also shows why an apparent optical-coupling benefit cannot substitute for corrosion and interface tests. [NUMBERS] [GAP] (jadhav2020mechanicalandelectrical pages 6-10, jadhav2020mechanicalandelectrical pages 4-6, jadhav2020mechanicalandelectrical pages 1-4)

[NAVY] [GAP] For **cast C95800**, entrained Al₂O₃/Cu-oxide films and porosity could interrupt bonding and serve as pathways for seawater attack; for **wrought C71500**, oxide at the interface and dilution by substrate metal must be assessed separately from powder oxygen. Repeat-pass reheating can expose/redistribute inclusions or inherited interfaces, but **an O-specific solidification-cracking or reheated-layer liquation-cracking threshold for either DED repair was not found**. Do not call all cracks oxygen-caused: welding reports describe Cu–Ni porosity without prevalent cracking, cast 70/30 Cu–Ni possible freezing-range hot cracking, and aluminium-bronze filler phase balance and interpass cleaning as independent weldability considerations. Examine the fusion boundary, first layer, later remelted layers and self-build independently; measure substrate O, H, dilution, oxide-stringer continuity and selective-corrosion depth. ERCuNi and ERCuAl-A2 provide **welding analogues**, not a qualification of single-stream pre-alloyed powder. ERCuNiAl and ERCuMnNiAl O-specific quantitative evidence was not retrieved. (robitz1990closuredevelopmentfor pages 17-20, robitz1990closuredevelopmentfor pages 49-52, francis1970chapter6– pages 11-14, uhlmann2024acomparativeevaluation pages 10-12)

**Induction/ultrasonic atomization.** [CITE] A directly relevant marine-bronze powder study measured **0.013 wt% O** in argon ultrasonic-atomized CuAl10Fe5Ni5, compared with **0.073 wt%** in the ground chips and **0.119–0.190 wt%** in milled powders; its **0.019 wt%** gas-atomized reference had *different chemistry*. Those values are *powder measurements*, not DED density/corrosion outcomes. The study reports ceramic contaminants and carbon fibres from **its carbon-fibre sonotrode**; it does **not** establish contamination from this proposal’s Ti-alloy or Mo sonotrodes. Al₂O₃ and ZrO₂ inclusions, Ti/Mo transfer, alumina reaction and possible CuAlO₂ formation must therefore be checked on the **actual ceramic crucible and actual sonotrode**, not assumed quantified. In copper–alumina bonding experiments, oxygen improved wetting and produced **CuAlO₂ at the interface**—potentially undesirable crucible interaction in powder making. Oxygen pickup, surface-oxide area per unit powder mass, moisture, and any Mn/Mg/Li/Zn vapor loss during melting/atomization should be audited by feedstock→melt→powder→deposit mass balances; there is **no retrieved rePOWDER-specific numerical O pickup, sonotrode wear rate, or O-dependent surface-tension curve for this alloy set**. [NUMBERS] [GAP] (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 4-6, beraud1989studyofcopperalumina pages 1-2, misra2011influenceofoxygen pages 42-48)

## 4. Thermodynamics and modeling

[NUMBERS] A published Cu–O account places the **Cu + Cu₂O eutectic near 0.39 wt% O and 1065 °C**, below pure Cu’s approximately **1083 °C** melting point. This is *not* an admissible impurity level: the oxide-containing low-melting constituent and very low solid O solubility argue against using a phase boundary as the powder bound. At **0.013 wt% O**, oxygen itself is not a plausible cause of a copper-rich alloy’s liquidus exceeding the atomizer’s approximately **1200–1250 °C useful-superheat window**; Ni, Al and other *metallic* additions govern that concern. The retrieved sources **do not establish a precisely temperature-qualified maximum O solubility in fcc Cu**: the approximately 2-ppm figure cited above must not be represented as a verified value *at 1083 °C*. Cu₂O/CuO are oxides, and CuAlO₂ is an oxide reaction product—not metallic Cu–O intermetallics. [GAP] (beraud1989studyofcopperalumina pages 1-2, jadhav2020mechanicalandelectrical pages 4-6, cUnknownyeartcox7tcsmetaloxide pages 17-21)

[CITE] **Thermo-Calc TCOX7**, a *metal-oxide-solutions* database distinct from the copper-alloy database, explicitly documents assessed **Cu–O**, **Cu–Ni–O**, and **Al₂O₃–Cu–O** systems; it represents cuprite and CuO as well as Cu-containing oxide solutions. Its documentation warns that its ionic liquid and another database’s metallic liquid should not simply be activated together. **Do not infer O assessment in TCCU merely because Cu–Ni–Al metallic alloys can be calculated there**; no verified TCCU O assessment or O-bearing COST 531 assessment was located. For pycalphad, a *licensed and compatible* exported oxide-capable TDB, validated against Cu–O and the relevant oxide equilibria, is required; an unverified metallic-only TDB cannot predict oxide inclusions or deoxidation. [GAP] (cUnknownyeartcox7tcsmetaloxide pages 1-5, cUnknownyeartcox7tcsmetaloxide pages 21-23)

## 5. Supply, safety and evidence status

Oxygen is an abundant industrial gas, **not an alloying commodity justified by nickel-substitution economics**. It is not itself a US critical *mineral* on the 2022 or 2025 lists; the nickel/copper criticality motivating the wider search does not make intentional O advantageous. For a reproducible cost comparison, purchased bulk oxygen is of order **US$0.1–1/kg** depending strongly on supply form and contract; **no sourced price specific to the proposed 0.5-kg atomization charges was established**, and high-purity argon, testing and rejected powder will dominate O-control cost. Oxygen has no analogous elemental-heavy-metal RoHS restriction, but concentrated O₂ is an oxidizer, and Cu-/Ni-bearing powder and laser-generated oxide fumes pose inhalation/combustible-dust risks. Use local exhaust, suitable respiratory controls, inert-gas oxygen-deficiency precautions and applicable OSHA exposure assessments for the *metals and their compounds*; **no retrieved source establishes a Navy-specific permissible wt% O or a RoHS/REACH O-in-copper prohibition**. [GAP] (uhlmann2024acomparativeevaluation pages 10-12, coppers1999copperdevelopmentassociation pages 47-50)

**Constraint for the composition search.** Treat O as a **measured impurity response**, not a palette dimension: powder and deposit each **≤0.013 wt% (130 ppm) provisionally** for *both* families, with ≤0.005 wt% (50 ppm) as a preferred screening target rather than a claimed naval or DED standard. Failure modes to reject experimentally are oxide-film/stringer inclusions, steam- or other gas-related porosity, interrupted fusion and substrate interfaces, and corrosion initiation at those defects. Joint constraints are O × H/moisture; O × available **Al/P/Ti/Si/Mg/Li** and oxide-removal efficiency; O × Mn/B and oxide flotation; and **Ni/Fe/Al-dependent corrosion-film chemistry**, which is distinct from bulk O. An O limit alone cannot guarantee dense, crack-free, C71500-equivalent seawater performance as deposited. Evidence is **moderate for controlling oxygen as an impurity**, but **thin for the proposed numerical DED/seawater threshold**. [GAP] (uhlmann2024acomparativeevaluation pages 10-12, toth2021electronbeamwelding pages 2-4, toth2021electronbeamwelding pages 10-12, lewis1981evaluationofcoppernickel pages 17-19, francis1970chapter6– pages 11-14)

**Principal references (DOIs).** Uhlmann *et al.*, *Materials* **17** (2024), 3396, **10.3390/ma17143396**; Tóth *et al.*, *Welding in the World* **65** (2021), 2077–2091, **10.1007/s40194-021-01158-4**; Jadhav *et al.*, *Materials Design & Processing Communications* **2** (2020), **10.1002/mdp2.94**; Tarafder *et al.*, *Materials* **14** (2021), 2932, **10.3390/ma14112932**; Nyborg and Cao, *Surface and Interface Analysis* **54** (2022), 944–953, **10.1002/sia.7107**; Beraud *et al.*, *Journal of Materials Science* **24** (1989), 4545–4554, **10.1007/BF00544543**; Lewis and LaQue, Argonne report ANL/OTEC-BCM-019 (1981), **10.2172/6255887**; Gao and Liu, *Materials* **15** (2022), 8513, **10.3390/ma15238513**; Jin *et al.*, *Materials* **12** (2019), 1869, **10.3390/ma12111869**; Francis, “Copper and Heavy Non-Ferrous Casting Alloys” (1970), **10.1016/B978-0-08-015711-5.50017-8**; Bastidas *et al.*, *Corrosion Reviews* **37** (2019), 307–320, **10.1515/corrrev-2019-0012**; Robitz *et al.*, US technical report (1990), **10.2172/138043**. The vendor’s **TCOX7 database documentation** is the basis for the database-status statements; named ASTM, AWS and MIL specifications should be consulted in their current editions for legally operative requirements. (uhlmann2024acomparativeevaluation pages 10-12, toth2021electronbeamwelding pages 2-4, jadhav2020mechanicalandelectrical pages 6-10, tarafder2021quasistatictensileproperties pages 2-3, nyborg2022surfacechemicaland pages 7-8, beraud1989studyofcopperalumina pages 1-2, lewis1981evaluationofcoppernickel pages 14-17, gao2022corrosionbehaviorof pages 1-2, jin2019surfacecharacterizationand pages 3-5, francis1970chapter6– pages 11-14, bastidas2019corrosionofcopper pages 1-2, robitz1990closuredevelopmentfor pages 49-52, cUnknownyeartcox7tcsmetaloxide pages 21-23)

VERDICT | O | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.013 | evidence=moderate

References

1. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

2. (jin2019surfacecharacterizationand pages 1-3): Tingzhu Jin, Weifang Zhang, Ning Li, Xuerong Liu, Lu Han, and Wei Dai. Surface characterization and corrosion behavior of 90/10 copper-nickel alloy in marine environment. Materials, 12:1869, Jun 2019. URL: https://doi.org/10.3390/ma12111869, doi:10.3390/ma12111869. This article has 148 citations.

3. (toth2021electronbeamwelding pages 2-4): Tamás Tóth, Jonas Hensel, Sven Thiemer, Philipp Sieber, and Klaus Dilger. Electron beam welding of rectangular copper wires applied in electrical drives. Welding in the World, 65:2077-2091, Aug 2021. URL: https://doi.org/10.1007/s40194-021-01158-4, doi:10.1007/s40194-021-01158-4. This article has 21 citations and is from a domain leading peer-reviewed journal.

4. (jadhav2020mechanicalandelectrical pages 4-6): Suraj Dinkar Jadhav, Jozef Vleugels, Jean‐Pierre Kruth, Jan Van Humbeeck, and Kim Vanmeensel. Mechanical and electrical properties of selective laser‐melted parts produced from surface‐oxidized copper powder. Material Design & Processing Communications, Apr 2020. URL: https://doi.org/10.1002/mdp2.94, doi:10.1002/mdp2.94. This article has 133 citations and is from a peer-reviewed journal.

5. (jadhav2020mechanicalandelectrical pages 6-10): Suraj Dinkar Jadhav, Jozef Vleugels, Jean‐Pierre Kruth, Jan Van Humbeeck, and Kim Vanmeensel. Mechanical and electrical properties of selective laser‐melted parts produced from surface‐oxidized copper powder. Material Design & Processing Communications, Apr 2020. URL: https://doi.org/10.1002/mdp2.94, doi:10.1002/mdp2.94. This article has 133 citations and is from a peer-reviewed journal.

6. (bastidas2019corrosionofcopper pages 1-2): David M. Bastidas, Benjamin Valdez, Michael Schorr, and Jose M. Bastidas. Corrosion of copper intrauterine devices: review and recent developments. Corrosion Reviews, 37:307-320, May 2019. URL: https://doi.org/10.1515/corrrev-2019-0012, doi:10.1515/corrrev-2019-0012. This article has 21 citations and is from a peer-reviewed journal.

7. (coppers1999copperdevelopmentassociation pages 47-50): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

8. (coppers1999copperdevelopmentassociation pages 40-43): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

9. (gao2022corrosionbehaviorof pages 1-2): Xin Gao and Ming Liu. Corrosion behavior of high-strength c71500 copper-nickel alloy in simulated seawater with high concentration of sulfide. Materials, 15:8513, Nov 2022. URL: https://doi.org/10.3390/ma15238513, doi:10.3390/ma15238513. This article has 34 citations.

10. (robitz1990closuredevelopmentfor pages 49-52): Closure development for high-level nuclear waste containers for the tuff repository; Phase 1, Final report This article has 2 citations.

11. (robitz1990closuredevelopmentfor pages 17-20): Closure development for high-level nuclear waste containers for the tuff repository; Phase 1, Final report This article has 2 citations.

12. (francis1970chapter6– pages 11-14): J.L. FRANCIS. Chapter 6 – copper and heavy non-ferrous casting alloys. ArXiv, pages 209-237, Jan 1970. URL: https://doi.org/10.1016/b978-0-08-015711-5.50017-8, doi:10.1016/b978-0-08-015711-5.50017-8. This article has 1 citations.

13. (francis1970chapter6– pages 14-18): J.L. FRANCIS. Chapter 6 – copper and heavy non-ferrous casting alloys. ArXiv, pages 209-237, Jan 1970. URL: https://doi.org/10.1016/b978-0-08-015711-5.50017-8, doi:10.1016/b978-0-08-015711-5.50017-8. This article has 1 citations.

14. (lewis1981evaluationofcoppernickel pages 19-21): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

15. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

16. (takaloo2011corrosionbehaviorof pages 2-3): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 43 citations and is from a peer-reviewed journal.

17. (lewis1981evaluationofcoppernickel pages 21-24): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

18. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

19. (jin2019surfacecharacterizationand pages 3-5): Tingzhu Jin, Weifang Zhang, Ning Li, Xuerong Liu, Lu Han, and Wei Dai. Surface characterization and corrosion behavior of 90/10 copper-nickel alloy in marine environment. Materials, 12:1869, Jun 2019. URL: https://doi.org/10.3390/ma12111869, doi:10.3390/ma12111869. This article has 148 citations.

20. (jin2019surfacecharacterizationand pages 8-11): Tingzhu Jin, Weifang Zhang, Ning Li, Xuerong Liu, Lu Han, and Wei Dai. Surface characterization and corrosion behavior of 90/10 copper-nickel alloy in marine environment. Materials, 12:1869, Jun 2019. URL: https://doi.org/10.3390/ma12111869, doi:10.3390/ma12111869. This article has 148 citations.

21. (toth2021electronbeamwelding pages 4-6): Tamás Tóth, Jonas Hensel, Sven Thiemer, Philipp Sieber, and Klaus Dilger. Electron beam welding of rectangular copper wires applied in electrical drives. Welding in the World, 65:2077-2091, Aug 2021. URL: https://doi.org/10.1007/s40194-021-01158-4, doi:10.1007/s40194-021-01158-4. This article has 21 citations and is from a domain leading peer-reviewed journal.

22. (toth2021electronbeamwelding pages 10-12): Tamás Tóth, Jonas Hensel, Sven Thiemer, Philipp Sieber, and Klaus Dilger. Electron beam welding of rectangular copper wires applied in electrical drives. Welding in the World, 65:2077-2091, Aug 2021. URL: https://doi.org/10.1007/s40194-021-01158-4, doi:10.1007/s40194-021-01158-4. This article has 21 citations and is from a domain leading peer-reviewed journal.

23. (toth2021electronbeamwelding media 4edfff5d): Tamás Tóth, Jonas Hensel, Sven Thiemer, Philipp Sieber, and Klaus Dilger. Electron beam welding of rectangular copper wires applied in electrical drives. Welding in the World, 65:2077-2091, Aug 2021. URL: https://doi.org/10.1007/s40194-021-01158-4, doi:10.1007/s40194-021-01158-4. This article has 21 citations and is from a domain leading peer-reviewed journal.

24. (nyborg2022surfacechemicaland pages 8-8): Lars Nyborg and Yu Cao. Surface chemical and geometrical properties of pure copper powder intended for binder jetting and sintering. Surface and Interface Analysis, 54:944-953, May 2022. URL: https://doi.org/10.1002/sia.7107, doi:10.1002/sia.7107. This article has 11 citations and is from a peer-reviewed journal.

25. (littleton1974nitrogenporosityin pages 1-2): J Littleton and J Lammas. Nitrogen porosity in gas shielded arc welding of copper. Unknown journal, 1974.

26. (jadhav2020mechanicalandelectrical pages 1-4): Suraj Dinkar Jadhav, Jozef Vleugels, Jean‐Pierre Kruth, Jan Van Humbeeck, and Kim Vanmeensel. Mechanical and electrical properties of selective laser‐melted parts produced from surface‐oxidized copper powder. Material Design & Processing Communications, Apr 2020. URL: https://doi.org/10.1002/mdp2.94, doi:10.1002/mdp2.94. This article has 133 citations and is from a peer-reviewed journal.

27. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

28. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

29. (beraud1989studyofcopperalumina pages 1-2): C. Beraud, M. Courbiere, C. Esnouf, D. Juve, and D. Treheux. Study of copper-alumina bonding. Dec 1989. URL: https://doi.org/10.1007/bf00544543, doi:10.1007/bf00544543. This article has 149 citations and is from a peer-reviewed journal.

30. (misra2011influenceofoxygen pages 42-48): Surya Kumar Misra. Influence of oxygen on the interfacial reaction between sapphire and copper. Text, Jan 2011. URL: https://doi.org/10.14288/1.0093750, doi:10.14288/1.0093750. This article has 0 citations and is from a peer-reviewed journal.

31. (cUnknownyeartcox7tcsmetaloxide pages 17-21): CCCF Al C and FG La. Tcox7-tcs metal oxide solutions database, version 7.0. Unknown journal, Unknown year.

32. (cUnknownyeartcox7tcsmetaloxide pages 1-5): CCCF Al C and FG La. Tcox7-tcs metal oxide solutions database, version 7.0. Unknown journal, Unknown year.

33. (cUnknownyeartcox7tcsmetaloxide pages 21-23): CCCF Al C and FG La. Tcox7-tcs metal oxide solutions database, version 7.0. Unknown journal, Unknown year.

34. (tarafder2021quasistatictensileproperties pages 2-3): Prithwish Tarafder, Christopher Rock, and Timothy Horn. Quasi-static tensile properties of unalloyed copper produced by electron beam powder bed fusion additive manufacturing. Materials, 14:2932, May 2021. URL: https://doi.org/10.3390/ma14112932, doi:10.3390/ma14112932. This article has 26 citations.

35. (nyborg2022surfacechemicaland pages 7-8): Lars Nyborg and Yu Cao. Surface chemical and geometrical properties of pure copper powder intended for binder jetting and sintering. Surface and Interface Analysis, 54:944-953, May 2022. URL: https://doi.org/10.1002/sia.7107, doi:10.1002/sia.7107. This article has 11 citations and is from a peer-reviewed journal.
