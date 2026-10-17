<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 3fc93807-2056-4c5c-9f3a-25c6b44de250
- Submitted: 2026-10-17T18:58:34Z
- Fetched: 2026-10-17T19:30:26Z (status: success)
- Raw trajectory JSON: ../raw/el-03-Al.json.gz
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

ELEMENT UNDER REVIEW: Al (major seawater addition). Aluminum bronzes: C95800 (8.5-9.5 Al), C63000 (9-11 Al), C95700 Mn-Al bronze (7-8.5 Al); aluminum brass C68700 (1.8-2.5 Al); Cu-Ni-Al alloys (e.g. the Hiduron series, MARINEL with about 1.9 Al, cast Cu-7Ni-3Al). Above about 9.4 wt% Al, beta and martensitic beta-prime are retained on fast cooling.

Answer for Al specifically, not for copper alloys in general:
1. ROLE: what Al does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Al ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Al changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Al, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Al, Cu-Ni-Al and Cu-Al-Al are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Al in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Al neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Al | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Al (major seawater addition). Aluminum bronzes: C95800 (8.5-9.5 Al), C63000 (9-11 Al), C95700 Mn-Al bronze (7-8.5 Al); aluminum brass C68700 (1.8-2.5 Al); Cu-Ni-Al alloys (e.g. the Hiduron series, MARINEL with about 1.9 Al, cast Cu-7Ni-3Al). Above about 9.4 wt% Al, beta and martensitic beta-prime are retained on fast cooling.

Answer for Al specifically, not for copper alloys in general:
1. ROLE: what Al does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Al ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Al changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Al, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Al, Cu-Ni-Al and Cu-Al-Al are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Al in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Al neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Al | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Aluminum as a designed addition to seawater-service copper DED powders

**Decision: INCLUDE Al, with separate Cu–Ni and aluminum-bronze subspaces.** Al can strengthen Cu-rich α solid solution and, in suitable compositions, contribute an Al-enriched inner oxide/hydroxide barrier. At higher contents it changes solidification and permits β/β′ and potentially corrosion-prone γ phases; Ni and Fe redirect some Al into κ intermetallics. The established marine alloy and additive-manufacturing evidence justifies exploring Al, **not** a claim that an as-deposited, single-stream laser-powder DED alloy already equals wrought C71500 in seawater. No publication by the specified PI is used below. (iannuzzi2017unusualcorrelationbetween pages 1-2, zhang2019tribocorrosionbehaviorof pages 1-2, dharmendra2019microstructuralevolutionand pages 2-3)

## 1. Role and documented alloy palette

- **[CITE][NUMBERS][SPEC][NAVY] Nickel-aluminum bronze (NAB).** ASTM B148 UNS **C95800** is reported at **8.5–9.5 wt% Al**, **4–5 wt% Ni**, **3.5–4.5 wt% Fe**, **0.8–1.5 wt% Mn**, Cu balance. Al participates in strengthening α and the corrosion film. Ni-rich κIII is Ni–Al-based; Fe-rich κII and fine κIV are Fe₃Al-based, with substitutions, rather than evidence that *all* added Al remains in protective α. Ni and Fe retard the undesirable binary β → α + γ reaction. Iannuzzi, Vasanth and Frankel, *Journal of The Electrochemical Society* **164**, C488–C497 (2017), DOI **10.1149/2.0391709jes**, includes an author affiliated with Naval Surface Warfare Center Carderock. Dharmendra *et al.*, *Additive Manufacturing* **30**, 100872 (2019), DOI **10.1016/j.addma.2019.100872**. (iannuzzi2017unusualcorrelationbetween pages 1-2, dharmendra2019microstructuralevolutionand pages 2-3)
- **[CITE][NUMBERS][SPEC] Other Al-bronze windows.** DIN 1982 **CC333G/CuAl10Ni5Fe5** permits **8.5–10.5 wt% Al**; its specified Fe and Ni ranges are **4.0–5.5** and **4.0–6.0 wt%**, respectively. An experimentally cast Cu–Al–Fe–Ni bronze containing **10.38–10.89 wt% Al**, **4.43–4.92 wt% Fe**, and **4.50–5.54 wt% Ni** establishes a higher-Al *processing example*, not seawater superiority. Uhlmann *et al.*, *Materials* **17**, 3396 (2024), DOI **10.3390/ma17143396**; Pisarek, *Archives of Foundry Engineering* **13**, 72–79 (2013), DOI **10.2478/afe-2013-0063**. C63000, C95700, C68700, Hiduron and MARINEL are relevant candidate families, but the retrieved primary documents did **not** verify their applicable ASTM/UNS/AWS edition-specific Al limits; the question's stated **C63000 9–11**, **C95700 7–8.5**, **C68700 1.8–2.5**, and **MARINEL approximately 1.9 wt% Al** should be treated as *provisional screening values*, not independently checked [SPEC] limits. (uhlmann2024acomparativeevaluation pages 7-10, pisarek2013modelofcualfeni pages 2-3)
- **[GAP] Cu–Ni, Mn–Al bronze, tin bronze/gunmetal, Cu–Ni–Sn and Cu–Ni–Si.** Al-bearing Cu–Ni–Al is chemically credible as a strengthening/film-forming branch, but the retrieved literature does not establish an Al-only improvement in *as-deposited seawater* corrosion or a minimum effective Al content for it. Nor was evidence found to claim that deliberately adding Al to conventional tin bronze, gunmetal, Cu–Ni–Sn, or Cu–Ni–Si improves their seawater performance; precipitation chemistry from another family must not be transferred to those alloys without tests. In aluminum brass, Al supports an impingement-resistant surface film, but its purported inhibition of **dezincification** is contradictory: Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*, Copper Development Association (1993), reports studies supporting, negating, and qualifying that effect, particularly in duplex brasses. No verified Al-specific grain-refining effect in these exact alloys was recovered; iron-bearing κ particles can refine deposited NAB grains, while Al is oxygen-reactive rather than a substitute for controlling melt oxygen. (davies1993anoteon pages 3-4, dharmendra2019microstructuralevolutionand pages 13-14, mantzavinos2001durabilitystudiesrelevant pages 55-59)

## 2. Seawater corrosion: what the numbers actually measure

**[CITE][NUMBERS]** Zhang *et al.*, *Friction* **7**, 444–456 (2019), DOI **10.1007/s40544-018-0221-y**, tested **cast, untreated C95800 with 9.17 wt% Al**, **4.40 wt% Ni**, **4.17 wt% Fe**, **1.28 wt% Mn**, Cu balance, in artificial seawater with **additional halide varied from 0 to 1.0 mol/L**. This is an *environmental series at fixed Al*, not an Al-concentration series. Its Table 2 gives, at **0 and 0.5 mol/L added halide**, respectively: static corrosion **E_corr −0.204 and −0.280 V versus Ag/AgCl** and **i_corr 3.74 and 4.03 µA/cm²**; during sliding, **−0.338 and −0.381 V** and **23.20 and 35.63 µA/cm²**. At **1.0 mol/L** the sliding current reaches **64.98 µA/cm²**, versus static **2.73 µA/cm²**. Halide damages/repassivation of the inner Al-enriched and outer Cu-enriched oxide/hydroxide film under wear. The paper reports no static pitting potential in the halide-added cases; this is **not proof of immunity to pits or crevice attack in natural seawater**. These polarization currents are not measured 30-day penetration rates. (zhang2019tribocorrosionbehaviorof pages 1-2, zhang2019tribocorrosionbehaviorof pages 4-6, zhang2019tribocorrosionbehaviorof media 486ea679)

**[CITE][NUMBERS]** A separate **11.54 wt% Al**, **4.47 wt% Fe**, **4.60 wt% Ni** cast NAB was tested after various heat treatments in ASTM D1141-type artificial seawater: normalized material showed higher impedance/polarization resistance than quenched material; the authors report an approximately **19% lower corrosion rate** for one normalized condition, but observed selective and pitting attack, including α/κ boundaries after **six days**. Since Al content is constant, the result measures **microstructure/heat-treatment dependence**, not the benefit of raising Al to 11.54 wt%. The study does not qualify that composition for as-deposited repair. Takaloo *et al.*, *Materials Sciences and Applications* (2011), DOI **10.4236/msa.2011.211207**. (takaloo2011corrosionbehaviorof pages 3-5, takaloo2011corrosionbehaviorof pages 7-9, takaloo2011corrosionbehaviorof pages 9-12)

**[NAVY][CITE]** In chloride tests on NAB, Cu-rich **α**, rather than necessarily the Al-bearing κ particles, can dissolve preferentially at approximately neutral pH; at lower pH the vulnerable phase can change. Air-measured SKPFM nobility even ranked phases oppositely to their observed attack. Avoid a blanket statement that “κ is always anodic” or that “more Al always prevents selective attack.” Iannuzzi *et al.*, DOI **10.1149/2.0391709jes**. **[GAP]** The retrieved sources do not provide a controlled Al-series giving seawater corrosion-rate, film-resistance, pitting-depth or crevice-depth improvement relative to wrought **C71500**. An aluminum-brass literature review gives an **up-to-2.2 m/s** service velocity with Al-bearing brass; it is **not** a validated DED-NAB or Cu–Ni–Al velocity limit. Mantzavinos, *Durability Studies Relevant to Marine Equipment* (2001), DOI **10.5525/gla.thesis.73974**. (iannuzzi2017unusualcorrelationbetween pages 9-10, iannuzzi2017unusualcorrelationbetween pages 1-2, mantzavinos2001durabilitystudiesrelevant pages 55-59)

## 3. Laser deposition, welding analogy and substrate dilution

**[CITE][NUMBERS]** A **Cu–9Al–4Fe–4Ni–1Mn**, all values wt%, **wire-arc** DED study produced sound, nearly fully dense multilayer bars at **170 J/mm** and reported no serious weld-metal solidification or HAZ-liquation cracking under its conditions. As-built WAAM tensile results were **388 ± 12 MPa yield strength** and **26 ± 1% elongation**, versus **300 ± 15 MPa** and **16 ± 2%** for its cast comparator. Reheating changed κ precipitation and β decomposition; these are *WAAM on stainless substrate*, not a proof of crack-free blown-powder laser DED on C95800 or C71500. Dharmendra *et al.*, DOI **10.1016/j.addma.2019.100872**. (dharmendra2019microstructuralevolutionand pages 13-14, dharmendra2019microstructuralevolutionand pages 2-3, dharmendra2019microstructuralevolutionand pages 14-15)

**[CITE][NUMBERS]** A contrasting infrared-laser **powder-bed** study of NAB with **9.56 wt% Al** and **0.09 wt% O** achieved only **≥94% relative density** at its selected parameters; as-built material was predominantly β′/needle α, with **479 MPa** tensile strength but just **1.49% elongation**. Its report of diminished Al and alumina on a **wear scar** must **not** be misreported as measured Al evaporation from its build. Alkelae and Sasaki, *Tribology Online* **15**, 126–135 (2020), DOI **10.2474/trol.15.126**. This illustrates the potentially severe dense-and-ductile trade-off near/above the β boundary, not a quantified composition-dependent cracking threshold. (alkelae2020tribologicalandmechanical pages 3-5, alkelae2020tribologicalandmechanical pages 5-9)

**[GAP]** For a single pre-alloyed stream, first-track dilution should be calculated as **Al_interface ≈ (1 − d)Al_powder + dAl_substrate**, where *d* is the measured melted-substrate mass fraction, not assumed equal on C95800 and wrought Cu–Ni. On C71500, dilution drives Al downward and Ni upward; on C95800, it tends toward substrate NAB chemistry but may remelt cast β/κ and expose a locally vulnerable HAZ. On Cu–Ni, Ni-rich aluminide precipitation, differential thermal contraction and an abrupt composition/film transition require inspection. These are **design hypotheses**, not reported successful joints. Composition-resolved cross sections, HAZ crack searches, gas/oxide porosity measurements, and separate interface versus top-layer 30-day corrosion depths are necessary. No retrieved primary source verified AWS A5.7 **ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl** Al ranges or demonstrated their comparability on both substrates; filler identities alone cannot establish a powder DED bound. (dharmendra2019microstructuralevolutionand pages 13-14, dharmendra2019microstructuralevolutionand pages 2-3, iannuzzi2017unusualcorrelationbetween pages 1-2)

## 4. Powder manufacturing and phase/temperature constraints

**[CITE][NUMBERS]** Especially pertinent process precedent is Uhlmann *et al.*, DOI **10.3390/ma17143396**: propeller CuAl10Ni5Fe5 chips were induction melted at **1,300 °C** under argon and ultrasonically atomized at **40 kHz**. The atomized sample measured **9.83 wt% Al by EDX**, compared with **10.4 wt%** on screened chips; the authors explicitly caution that EDX is not sufficiently precise to establish a **0.57 wt% evaporation loss**. Hot-gas extraction instead reliably found powder **0.013 wt% oxygen**, versus **0.073 wt%** in chips and **0.019 wt%** in the different gas-atomized comparison powder; its powder had Hausner ratio **1.05**. Ceramic debris and fibers originating from that study's **carbon-fiber** sonotrode occurred. These observations do **not** show that alumina or zirconia crucibles chemically reduce, or that a Ti-alloy or Mo sonotrode contaminates, the proposed rePOWDER melt. Test *each* proposed crucible/sonotrode pair by melt/atomized-powder Al, O, C, Ti, Mo, Zr and inclusion analysis; suppress Al oxide dross and moisture-derived hydrogen rather than assuming an argon cover eliminates them. (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 7-10)

**[CITE][NUMBERS]** The **binary** Cu–Al assessment gives **L → (Cu) + β at 1,035 ± 5 °C** and **β → (Cu) + γ₁ at 567 ± 2 °C**; at the latter invariant the assessed Cu-rich α endpoint is **81.5 ± 0.5 atomic% Cu**, corresponding to approximately **8.8 wt% Al** after atomic-to-mass conversion. This **solid-state eutectoid endpoint is not the maximum α solubility at all temperatures**; the recovered source does not resolve a defensible numeric maximum and its temperature, so that requested value remains [GAP]. Binary β/β′ retention above approximately **9.4 wt% Al** is a **screening warning**, not a validated multicomponent NAB transition: Ni and Fe change phase boundaries. Ponweiser, Lengauer and Richter, *Intermetallics* **19**, 1737–1746 (2011), DOI **10.1016/j.intermet.2011.07.007**; Iannuzzi *et al.*, DOI **10.1149/2.0391709jes**. The Al-rich **θ-Al₂Cu** in the full binary assessment should not be portrayed as a predicted precipitate in a Cu-rich NAB deposit. The notation γ₁ versus γ₂ differs between binary assessments and bronze-microstructure reports; use the actual database phase descriptions. (ponweiser2011reinvestigationofphase pages 3-4, iannuzzi2017unusualcorrelationbetween pages 1-2, ponweiser2011reinvestigationofphase pages 1-2)

**[CITE][NUMBERS]** Pisarek measured **1,082.6 °C liquidus** and **1,023.3 °C solidus** for a cast bronze containing **10.38–10.89 wt% Al** and roughly **4.4–5.5 wt% each Fe/Ni**, DOI **10.2478/afe-2013-0063**. Thus Al-rich NAB is not intrinsically above the proposed **1,200–1,250 °C practical liquidus ceiling**; adding Ni/Fe or changing composition still demands a fresh liquidus and usable-superheat check. Schmitz, Brillo and Egry, *European Physical Journal Special Topics* **223**, 469–479 (2014), DOI **10.1140/epjst/e2014-02103-5**, measured Cu–Al melt surface tension but tabulated compositions as **atomic fractions**: its “Al10Cu90” is **approximately 4.5 wt% Al**, *not* 10 wt% Al. Near that composition, surface tension at its liquidus was **1.35 ± 0.01 N/m**, versus **1.31 ± 0.01 N/m** for Cu. Do not claim a monotonic decrease at the proposed Cu-rich bounds. (pisarek2013modelofcualfeni pages 2-3, schmitz2014surfacetensionof pages 3-7)

**[GAP] CALPHAD.** Binary Cu–Al has published thermodynamic assessments; Cu–Ni–Al includes κ/Ni–Al chemistry requiring a consistent *ternary or higher-order* description. A database containing the three element names is not proof that its relevant Cu–Ni–Al and Cu–Al–Fe–Ni phases are assessed and stable at these compositions. The available sources do **not** verify TCCU's released-version ternary parameters, COST 531's usable coverage, or an exportable TDB for this precise problem. **Cu–Al–Al is not a distinct ternary system**: the repeated Al reduces to binary Cu–Al. In Thermo-Calc, inspect TCCU version/phase constituents and calculate equilibrium liquidus, Scheil terminal liquid, α/β/γ/κ fractions, and dilution-path endpoints; in pycalphad, first obtain a licensed/valid TDB and compare against measured cast and deposited microstructures. (ponweiser2011reinvestigationofphase pages 1-2, pisarek2013modelofcualfeni pages 2-3, iannuzzi2017unusualcorrelationbetween pages 1-2)

## 5. Supply, safety and proposed search-space bounds

**[CITE][NAVY]** Al and Ni appear on the U.S. **2025 final** critical-minerals list, and USGS's 2025 methodology recommended **adding Cu**; Al and Ni were already listed in **2022**. The relevant final 2025 notice is **90 FR 50494**; Nassar *et al.*, USGS Open-File Report **2025-1047**, DOI **10.3133/ofr20251047**. Al's commodity cost is ordinarily order **US$2–4/kg** as a *planning estimate for primary metal*, not a documented current supplier quotation for oxygen-free charge Al or certified alloy powder. No Al-specific Navy procurement prohibition, RoHS restriction on metallic Al, or REACH authorization limit was verified in the retrieved sources; do not mistake applicable **Pb/Cd** restrictions on contaminated scrap for an Al ban. Powder dust poses inhalation/combustible-cloud hazards; contain fine powder, ground equipment, avoid water on burning metal, and capture laser fumes and co-alloy Ni/Mn aerosols. A retrieved occupational review reproduces **15 mg/m³ total Al-metal dust** as an OSHA PEL, but labels the welding-fume OSHA category **not established**; its adjacent **5 mg/m³** welding-fume values are UK/Australian values, **not** an OSHA Al-fume PEL. Recheck the current OSHA substance entry and any more protective applicable exposure rule before specifying controls. (staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 9-11, nassar2025methodologyandtechnical pages 33-35, ferguson2018systematicreviewof pages 21-22)

**[NUMBERS][SPEC] Candidate limits, all wt% Al in the final Cu-balance alloy:**

| Design branch | Functional floor | Conservative maximum | Non-conservative maximum | What limits it |
|---|---:|---:|---:|---|
| Al-bronze/NAB | **1.8** *palette floor from aluminum brass; NAB's demonstrated marine range begins at 8.5* | **9.5** | **10.5** | C95800 commercial upper end/approximately 9.4 binary β warning; aggressive end from DIN CC333G and cast 10.38–10.89 example, limited by β′/γ/selective corrosion and laser density/ductility. |
| Cu–Ni–Al, without an NAB-like Ni–Fe package | **1.8** *provisional screening floor only* | **3.0 provisional** | **5.0 provisional** | Cu–Ni–Al strengthening chemistry versus unverified as-deposited seawater film, Ni–Al precipitation, Cu–Ni repair dilution and unknown hot-cracking window; **these two Cu–Ni caps are research choices, not verified specification limits**. |

**[CITE][GAP]** The single palette-wide maxima are therefore **9.5 conservative** and **10.5 non-conservative wt% Al**, **only when a paired Fe/Ni-containing aluminum-bronze branch is allowed**. For the Cu–Ni branch the **1.8 wt% floor and 3.0/5.0 wt% ceilings remain hypotheses**, not an assertion of measured Al onset or qualified Cu–Ni–Al seawater service. The functional-floor precedent is the question's stated **C68700 1.8–2.5 wt% Al** and the literature's approximately **2–2.5 wt% Al** aluminum-brass film/impingement observation; composition-controlled measurements below that range were not recovered. Do **not** impose a universal Al impurity maximum, because Al is deliberately included. (dharmendra2019microstructuralevolutionand pages 2-3, uhlmann2024acomparativeevaluation pages 7-10, pisarek2013modelofcualfeni pages 2-3, mantzavinos2001durabilitystudiesrelevant pages 55-59)

**Joint constraints and evidence quality.** Couple Al to **Ni + Fe** because κ precipitation competes with Al in α and suppresses γ; avoid treating the binary **9.4 wt%** threshold as a fixed limit when those partners vary. Monitor Mn's deoxidation and κ substitutions; Zn + Al in brass changes the α/β balance and can worsen dezincification even when surface-film performance improves. Excess oxide and C/Ti/Mo/Zr inclusions threaten density and crack initiation; adding Al does not neutralize Pb, Bi or other low-melting segregants. These interactions motivate Fe/Ni/Al ratios and measured post-dilution phase maps, **not an evidence-backed universal numerical ratio**. Overall evidence is **moderate** for including Al and an Al-bronze maximum, but **thin** for the Cu–Ni branch, cross-substrate single-stream powder DED, verified rePOWDER crucible/sonotrode reactivity, and 30-day as-deposited C71500 parity. (iannuzzi2017unusualcorrelationbetween pages 1-2, davies1993anoteon pages 3-4, uhlmann2024acomparativeevaluation pages 7-10, alkelae2020tribologicalandmechanical pages 3-5)

VERDICT | Al | decision=INCLUDE | family=both | conservative_max_wt=9.5 | nonconservative_max_wt=10.5 | floor_wt=1.8 | impurity_max_wt=NA | evidence=moderate

References

1. (iannuzzi2017unusualcorrelationbetween pages 1-2): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

2. (zhang2019tribocorrosionbehaviorof pages 1-2): Beibei Zhang, Jianzhang Wang, Junya Yuan, and Fengyuan Yan. Tribocorrosion behavior of nickel-aluminium bronze sliding against alumina under the lubrication by seawater with different halide concentrations. Friction, pages 1-13, Nov 2019. URL: https://doi.org/10.1007/s40544-018-0221-y, doi:10.1007/s40544-018-0221-y. This article has 39 citations and is from a peer-reviewed journal.

3. (dharmendra2019microstructuralevolutionand pages 2-3): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

4. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

5. (pisarek2013modelofcualfeni pages 2-3): B. P. Pisarek. Model of cu-al-fe-ni bronze crystallization. Archives of Foundry Engineering, 13:72-79, Sep 2013. URL: https://doi.org/10.2478/afe-2013-0063, doi:10.2478/afe-2013-0063. This article has 80 citations.

6. (davies1993anoteon pages 3-4): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

7. (dharmendra2019microstructuralevolutionand pages 13-14): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

8. (mantzavinos2001durabilitystudiesrelevant pages 55-59): Dimitris Mantzavinos. Durability studies relevant to marine equipment. Text, Jan 2001. URL: https://doi.org/10.5525/gla.thesis.73974, doi:10.5525/gla.thesis.73974. This article has 1 citations and is from a peer-reviewed journal.

9. (zhang2019tribocorrosionbehaviorof pages 4-6): Beibei Zhang, Jianzhang Wang, Junya Yuan, and Fengyuan Yan. Tribocorrosion behavior of nickel-aluminium bronze sliding against alumina under the lubrication by seawater with different halide concentrations. Friction, pages 1-13, Nov 2019. URL: https://doi.org/10.1007/s40544-018-0221-y, doi:10.1007/s40544-018-0221-y. This article has 39 citations and is from a peer-reviewed journal.

10. (zhang2019tribocorrosionbehaviorof media 486ea679): Beibei Zhang, Jianzhang Wang, Junya Yuan, and Fengyuan Yan. Tribocorrosion behavior of nickel-aluminium bronze sliding against alumina under the lubrication by seawater with different halide concentrations. Friction, pages 1-13, Nov 2019. URL: https://doi.org/10.1007/s40544-018-0221-y, doi:10.1007/s40544-018-0221-y. This article has 39 citations and is from a peer-reviewed journal.

11. (takaloo2011corrosionbehaviorof pages 3-5): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

12. (takaloo2011corrosionbehaviorof pages 7-9): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

13. (takaloo2011corrosionbehaviorof pages 9-12): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

14. (iannuzzi2017unusualcorrelationbetween pages 9-10): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

15. (dharmendra2019microstructuralevolutionand pages 14-15): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

16. (alkelae2020tribologicalandmechanical pages 3-5): Fathia Alkelae and Shinya Sasaki. Tribological and mechanical characterization of nickel aluminium bronze (nab) manufactured by laser powder-bed fusion (l-pbf). Tribology Online, 15:126-135, Jun 2020. URL: https://doi.org/10.2474/trol.15.126, doi:10.2474/trol.15.126. This article has 16 citations and is from a peer-reviewed journal.

17. (alkelae2020tribologicalandmechanical pages 5-9): Fathia Alkelae and Shinya Sasaki. Tribological and mechanical characterization of nickel aluminium bronze (nab) manufactured by laser powder-bed fusion (l-pbf). Tribology Online, 15:126-135, Jun 2020. URL: https://doi.org/10.2474/trol.15.126, doi:10.2474/trol.15.126. This article has 16 citations and is from a peer-reviewed journal.

18. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

19. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

20. (ponweiser2011reinvestigationofphase pages 3-4): Norbert Ponweiser, Christian L. Lengauer, and Klaus W. Richter. Re-investigation of phase equilibria in the system al–cu and structural analysis of the high-temperature phase η1-al1−δcu. Intermetallics, 19:1737-1746, Nov 2011. URL: https://doi.org/10.1016/j.intermet.2011.07.007, doi:10.1016/j.intermet.2011.07.007. This article has 174 citations and is from a peer-reviewed journal.

21. (ponweiser2011reinvestigationofphase pages 1-2): Norbert Ponweiser, Christian L. Lengauer, and Klaus W. Richter. Re-investigation of phase equilibria in the system al–cu and structural analysis of the high-temperature phase η1-al1−δcu. Intermetallics, 19:1737-1746, Nov 2011. URL: https://doi.org/10.1016/j.intermet.2011.07.007, doi:10.1016/j.intermet.2011.07.007. This article has 174 citations and is from a peer-reviewed journal.

22. (schmitz2014surfacetensionof pages 3-7): J. Schmitz, J. Brillo, and I. Egry. Surface tension of liquid al-cu and wetting at the cu/sapphire solid-liquid interface. The European Physical Journal Special Topics, 223:469-479, Feb 2014. URL: https://doi.org/10.1140/epjst/e2014-02103-5, doi:10.1140/epjst/e2014-02103-5. This article has 12 citations.

23. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

24. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

25. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

26. (ferguson2018systematicreviewof pages 21-22): G Ferguson, R Hopkins, K Poortinga, and L McCallum. Systematic review of occupational aluminum exposure and adverse health conditions. Unknown journal, 2018.
