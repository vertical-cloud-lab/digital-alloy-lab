<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: b1b8cab3-0d80-4e2f-9cb4-aee6252ab969
- Submitted: 2026-10-17T18:59:39Z
- Fetched: 2026-10-17T19:30:40Z (status: success)
- Raw trajectory JSON: ../raw/el-16-Mg.json.gz
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

ELEMENT UNDER REVIEW: Mg (strengthening addition). Deoxidizer for copper; Cu-Mg conductor alloys (about 0.1-0.7 Mg); Mg in some aluminum bronzes. High vapor pressure; MgO crucibles.

Answer for Mg specifically, not for copper alloys in general:
1. ROLE: what Mg does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Mg ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Mg changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Mg, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Mg, Cu-Ni-Mg and Cu-Al-Mg are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Mg in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Mg neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Mg | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Mg (strengthening addition). Deoxidizer for copper; Cu-Mg conductor alloys (about 0.1-0.7 Mg); Mg in some aluminum bronzes. High vapor pressure; MgO crucibles.

Answer for Mg specifically, not for copper alloys in general:
1. ROLE: what Mg does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Mg ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Mg changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Mg, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Mg, Cu-Ni-Mg and Cu-Al-Mg are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Mg in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Mg neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Mg | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Mg in pre-alloyed powder for marine copper-alloy DED

**Decision: LIMIT Mg as a controlled residual, rather than include it as a strengthening addition.** The strongest application-specific source calls Mg an end-of-melt *deoxidizer and grain-refining addition* in Cu–Ni, but says its residual is normally only a trace and has no significant effect in service. The same source classifies Mg as detrimental in aluminum bronze because of concern about ductility and elevated-temperature behavior. It supplies neither a numerical Mg tolerance nor evidence that intentional Mg improves seawater corrosion. A published, fully dense NAB wire-arc deposit used a cast substrate reported as **<0.01 wt% Mg**; that is a useful conservative *research acceptance target*, not an ASTM or AWS Mg limit and not proof of Mg tolerance in laser DED. [CITE] [NUMBERS] [GAP] (konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, ding2016fabricatingsuperiornial pages 3-6)

## 1. Role, alloy families, and specifications

In **Cu–Ni**, Mg can scavenge oxygen during melt processing and is reported to assist grain refinement. Both effects concern processing, not an established Mg-strengthened or Mg-passivated seawater alloy; the report says residual Mg is ordinarily trace. In **aluminum bronze/NAB**, the same report advises keeping Mg quite low for fear of impaired ductility or hot behavior. The demonstrated NAB strengthening and marine-corrosion mechanisms instead involve its Al–Fe–Ni–Mn phase balance; Mg is not identified as a protective-film constituent or a standard κ-phase addition. No verified Mg-specific dealloying-inhibition mechanism was found for either family. [CITE] [GAP] (konynenburg1990backgroundstudiesin pages 136-142, konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, ocejo2022corrosionbehaviorof pages 1-3)

| Documented Cu-rich material | Mg, wt% | What the number establishes |
|---|---:|---|
| Cast NAB substrate used for a fully dense multilayer NAB wire-arc build | **<0.01** | Measured/reportable baseline in one deposition study; **not a specification limit**. [NUMBERS] (ding2016fabricatingsuperiornial pages 3-6) |
| Cu–Mg electrical-conductor component in patent JP2009520332A | **0.1–0.7**; preferred **0.5** | Proposed conductor formulation, **not marine service or a Navy alloy**. [NUMBERS] (JP2009520332A pages 1-11) |
| Optional Mg in patented Cu–Sn–Si–B alloy, US11028463B2 | **0–0.5** | Patent claim, not a demonstrated Mg-dependent seawater benefit or gunmetal standard. [NUMBERS] (US11028463B2 pages 1-6) |

**[SPEC]** The material located does **not** verify an intentional Mg range in C71500 under ASTM B111/B171/B466 or MIL-T-16420; C95800/C95500 under ASTM B148 or applicable Navy bronze specifications; the other listed ASTM, MIL, or EN specifications; or AWS A5.7 ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl. Do not turn an unspecified “other elements” allowance into a specified Mg range. A technical review describes conventional E/RCuNi filler as approximately 30 wt% Ni with Fe **0.4–0.7 wt%**, Mn up to **1.0 wt%**, Ti up to **0.5 wt%**, and Si up to **0.15 wt%**; it gives no intentional Mg requirement. It likewise describes aluminum-bronze filler with Al **9–11 wt%**, Fe at most **1.5 wt%**, and an aggregate limit on other elements, **not an individual Mg allowance**. [CITE] [SPEC] [GAP] (konynenburg1990backgroundstudiesin pages 136-142)

For **Mn–Al bronze, brasses, tin bronze/gunmetal, Cu–Ni–Sn, and Cu–Ni–Si**, the retrieved evidence does not establish a commercial/Navy Mg-bearing marine grade, its Mg range, or Mg-specific strengthening, film, or dealloying benefits. The optional-Mg Cu–Sn patent cannot supply those missing results. [GAP] (US11028463B2 pages 1-6, ocejo2022corrosionbehaviorof pages 1-3)

## 2. Seawater corrosion

**No attributable quantitative Mg effect was found.** Specifically, there is no retrieved matched-composition Mg-free/Mg-added Cu–Ni or aluminum-bronze dataset establishing a favorable or harmful Mg interval for corrosion rate, *E*₍corr₎, impedance/film resistance, pitting or crevice penetration, selective attack, erosion–corrosion, or permissible seawater velocity. Consequently **no Mg concentration can presently be claimed to meet the wrought C71500 benchmark**, and there is no defensible Mg-dependent velocity limit. Cu–Mg conductor performance and corrosion of *Mg-base* alloys cannot answer this Cu-base question. [GAP] (JP2009520332A pages 1-11, konynenburg1990backgroundstudiesin pages 142-149, greenberg1960aqueouscorrosionof pages 17-20)

The relevant **Mg-uncontrolled baseline**, not an Mg-addition result, is Jafari, Davoodi and Hosseinpour, “Effect of Fluid Flow on the Corrosion Performance of as-Cast and Heat-Treated Nickel Aluminum Bronze Alloy (UNS C95800) in Saline Solution,” *Corrosion and Materials Degradation* **2** (2021), 61–77, **DOI: 10.3390/cmd2010004**. Their C95800 was tested in **3.5 wt% NaCl**, at **25 and 40 °C** and **0–9,000 rpm**; flow worsened its electrochemical corrosion response, while annealing reduced its corrosion-sensitive β-phase fraction from **>20% to about 7%**. Its composition table does **not** report Mg. Neither those results nor the NAB/Mn–Al-bronze comparison by Cobo Ocejo, Biezma Moraleda and Linhardt, *Metals* **12** (2022), 380, **DOI: 10.3390/met12030380**, isolate an Mg effect. [CITE] [NUMBERS] [GAP] (jafari2021effectoffluid pages 2-4, ocejo2022corrosionbehaviorof pages 1-3)

## 3. DED, repair welding, and powder production

**[NAVY] [CITE]** Ding *et al.*, “Fabricating Superior NiAl Bronze Components through Wire Arc Additive Manufacturing,” *Materials* **9** (2016), 652, **DOI: 10.3390/ma9080652**, deposited commercial NAB wire on a cast substrate to an apparently fully dense structure without base-metal preheating; the reported substrate had **<0.01 wt% Mg**. Their process was **wire-arc AM, not laser blown-powder DED**, and they did not vary or measure Mg in the deposit. Their reheated layer bands and transformed heat-affected material demonstrate why successful deposition alone does not establish as-deposited seawater resistance. The underlying report on Cu alloys notes that low elevated-temperature ductility in aluminum bronze may cause weld cracking and that Cu–Ni deoxidation and filler chemistry are important. Neither source measures an Mg-dependent solidification-cracking, reheated-layer liquation-cracking, or porosity threshold. [NUMBERS] [GAP] (ding2016fabricatingsuperiornial pages 3-6, konynenburg1990backgroundstudiesin pages 149-155)

For the proposed **1.07-µm fiber laser and argon atomization/DED process**, Mg oxidation, volatile loss, oxide inclusions and composition drift are plausible *failure hypotheses*, not established Mg-loss percentages. Deoxidation may remove oxygen from a melt while leaving Mg-bearing oxide particles; it must not be equated with guaranteed pore elimination. Dilution into **C95800** would put any surviving Mg into an Al-bearing, multiphase fusion boundary for which the technical report raises a ductility concern. Dilution into **wrought Cu–Ni** would reduce local Mg concentration, but cannot be credited with a corrosion benefit. Measure Mg and O in charge, atomized powder, deposited bulk and each repair-interface traverse, and section both interfaces for inclusions and cracks. [CITE] [GAP] (konynenburg1990backgroundstudiesin pages 136-142, konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, ding2016fabricatingsuperiornial pages 3-6)

**[GAP] Powder hardware:** The Cu–Ni processing report supports late Mg addition as a deoxidizing practice and warns that aluminum-bronze melts are difficult to refine and that slags can attack crucibles. It does **not** quantify Mg evaporation from this **0.5-kg** induction charge, Mg reaction rates with **Al₂O₃, ZrO₂ or graphite**, titanium-alloy or molybdenum sonotrode contamination, or Mg-dependent droplet surface tension on the specified ultrasonic atomizer. These are experimental checks, not grounds for fabricated equipment-specific limits. MgO crucibles are another processing option, not evidence that Mg improves the deposited alloy. [CITE] [GAP] (konynenburg1990backgroundstudiesin pages 136-142)

## 4. Phase diagram, CALPHAD, and compositional interactions

**[CITE]** Bocklund *et al.*, “ESPEI for Efficient Thermodynamic Database Development, Modification, and Uncertainty Quantification: Application to Cu–Mg,” in *Zentropy* (2024), pp. 393–416, **DOI: 10.1201/9781003514466-19**, assesses Cu–Mg using pycalphad/ESPEI. Its equilibrium solids comprise Cu-rich fcc and Mg-rich hcp solutions, **Cu₂Mg** (C15 Laves phase, with a homogeneity range), and **CuMg₂** (also Mg₂Cu). Its assessed phase diagram contains the Cu-rich liquid/fcc/Cu₂Mg invariant region. Prior binary modeling cited there is Zhou *et al.*, *Journal of Phase Equilibria and Diffusion* **28** (2007), 158–166, **DOI: 10.1007/s11669-007-9022-0**; the cited Al–Cu–Mg assessment is Bühler *et al.*, *Journal of Phase Equilibria* **19** (1998), 317–329, **DOI: 10.1361/105497198770342058**. **Do not confuse the latter Al–Cu–Mg system with a validated Cu-rich NAB–Mg calculation.** [GAP] (bocklund2024espeiforefficient pages 9-13, bocklund2024espeiforefficient pages 17-21, bocklund2024espeiforefficient pages 13-17, bocklund2024espeiforefficient media de05fd86)

**[NUMBERS] [GAP]** The accessible phase-diagram text/figure does not resolve a trustworthy numerical **maximum Cu-rich solid solubility in wt% and temperature**, invariant temperature/composition, or liquidus at each proposed composition; none is asserted here. These must be read from a checked phase-diagram assessment or computed and validated before becoming a search bound. Pure Cu melts near **1,085 °C**; adding dilute Mg to that reference does **not by itself demonstrate** a liquidus above the equipment’s **1,200–1,250 °C** useful-superheat cutoff. Ni, Fe, Al and Mn, together with evaporation/oxide losses, must be included in the *actual multicomponent* liquidus calculation. A published **binary** or **Al–Cu–Mg** assessment does not verify that a particular installed **TCCU** release contains valid **Cu–Ni–Mg** and **Cu–Al–Mg** ternary descriptions, nor that COST 531 supplies them: check constituent lists, assessed interactions and phase coverage in the installed databases before trusting a Scheil path or extrapolated liquidus. [CITE] [GAP] (bocklund2024espeiforefficient pages 9-13, bocklund2024espeiforefficient pages 13-17, bocklund2024espeiforefficient media de05fd86)

**Joint constraints:** Treat Mg jointly with **O and Al** for oxide/inclusion formation and potential NAB hot-ductility loss, and with **Ni, Fe and Mn** for dilution, grain structure and the established seawater-active phase balance. Do **not** impose an invented Mg:Ni, Mg:Fe or Mg:Mn ratio. Oxygen-scavenging Mg is not demonstrated to substitute for the specified Fe/Mn corrosion contributions of Cu–Ni; neither is it shown to neutralize the selectively attacked β phase in NAB. The small Cu–Ni residual levels described in the report are a *process control*, not an independently established Mg precipitation-strengthening scheme for the as-deposited alloy. [CITE] [GAP] (jafari2021effectoffluid pages 2-4, konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155)

## 5. Supply, safety, and bounds

**[CITE]** Mg is a U.S. critical mineral on the **2022 list** and remains on the **final 2025 list**; the 2025 final-list citation is **90 FR 50494**. Mg *metal* should not be conflated with magnesium compounds. USGS reports discuss concentrated magnesium-metal production and supply uncertainty: Alonso *et al.*, *World Minerals Outlook—Cobalt, Gallium, Helium, Lithium, Magnesium, Palladium, Platinum, and Titanium Through 2029*, USGS Scientific Investigations Report 2025–5021, **DOI: 10.3133/sir20255021**; Nassar *et al.*, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, USGS OFR 2025–1047, **DOI: 10.3133/ofr20251047**. The retrieved final-list table also lists copper and nickel. **No verifiable contemporaneous Mg-metal price per kg was obtained**: a numerical purchase-price claim, particularly for high-purity small charges, would be speculative. [GAP] (alonso2025worldmineralsoutlook—cobalt pages 17-19, staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 9-11, nassar2025methodologyandtechnical pages 31-32)

Mg is not a Pb/Cd-style intentional toxic alloy addition, but reactive fine metal powder and condensed laser fume require a powder/fire assessment, contained transfer and ventilation, combustible-metal-appropriate fire procedures, and exposure monitoring for the **whole alloy fume**. No Mg-specific Navy prohibition or RoHS/REACH concentration restriction, nor a verified applicable numerical OSHA Mg-fume limit, was established in the retrieved evidence; do not mistake the OSHA value for **another metal's** oxide fume for an Mg standard. [GAP] (konynenburg1990backgroundstudiesin pages 136-142, blanc1991anexperimentalhuman pages 1-2)

**Numerical bound and failure mode.** **LIMIT** applies to **both Cu–Ni and aluminum-bronze candidate powders and deposited bulk**: use **Mg <0.01 wt% (100 ppm)** as an *interim, analytically verifiable screening ceiling*, tied to the measured cast-NAB substrate in Ding *et al.*; it is **not** a qualified DED safety/corrosion threshold and **not** an ASTM, MIL, AWS or UNS Mg limit. Specify a validated analytical detection limit below that ceiling, report the measured retained Mg rather than just the charge, and revisit the ceiling if matched-composition Cu–Ni and NAB tests establish another value. The conservative failure mode is **unverified corrosion/hot-ductility performance at the NAB repair boundary**, compounded by uncertain Mg retention and oxide inclusions. There is **no evidence-based beneficial floor or designed-addition maximum** for this dual-family, as-deposited seawater application. The Cu–Mg conductor’s **0.1–0.7 wt%** and Cu–Sn patent’s optional **0–0.5 wt%** are exploration precedents only, not admissible marine DED bounds. [NUMBERS] [GAP] (ding2016fabricatingsuperiornial pages 3-6, konynenburg1990backgroundstudiesin pages 149-155, JP2009520332A pages 1-11, US11028463B2 pages 1-6)

**Evidence quality:** strong for Cu–Mg phase identities and for the cited qualitative difference between Cu–Ni deoxidation and aluminum-bronze caution; **thin** for any Mg-specific as-deposited marine corrosion, laser cracking, atomization retention, validated numerical impurity tolerance, or comparison against C71500. The proposed **0.01 wt%** ceiling is consequently a *study design choice anchored to a published low-Mg baseline*, not a proven performance boundary. (bocklund2024espeiforefficient pages 9-13, konynenburg1990backgroundstudiesin pages 149-155, ding2016fabricatingsuperiornial pages 3-6)

VERDICT | Mg | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin

References

1. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

2. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

3. (ding2016fabricatingsuperiornial pages 3-6): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 279 citations.

4. (konynenburg1990backgroundstudiesin pages 136-142): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

5. (ocejo2022corrosionbehaviorof pages 1-3): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

6. (JP2009520332A pages 1-11): ププケ フランク. Electrical composite conductor and manufacturing method thereof. Patent (WO,EP,US,CN,JP,KR,AT,AU,CA,DE,DK,ES,PL,PT,RU,SI,ZA), 2009.

7. (US11028463B2 pages 1-6): Kai Weber. Copper alloy containing tin, method for producing same, and use of same. Patent (WO,EP,US,CN,JP,KR,DE,MX), 2021.

8. (greenberg1960aqueouscorrosionof pages 17-20): S. Greenberg and W.E. Ruther. Aqueous corrosion of magnesium alloys. ArXiv, May 1960. URL: https://doi.org/10.2172/4162995, doi:10.2172/4162995. This article has 0 citations.

9. (jafari2021effectoffluid pages 2-4): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

10. (bocklund2024espeiforefficient pages 9-13): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. ESPEI for Efficient Thermodynamic Database Development, Modification, and Uncertainty Quantification: Application to Cu–Mg, pages 393-416. Jenny Stanford Publishing, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 2 citations.

11. (bocklund2024espeiforefficient pages 17-21): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. ESPEI for Efficient Thermodynamic Database Development, Modification, and Uncertainty Quantification: Application to Cu–Mg, pages 393-416. Jenny Stanford Publishing, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 2 citations.

12. (bocklund2024espeiforefficient pages 13-17): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. ESPEI for Efficient Thermodynamic Database Development, Modification, and Uncertainty Quantification: Application to Cu–Mg, pages 393-416. Jenny Stanford Publishing, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 2 citations.

13. (bocklund2024espeiforefficient media de05fd86): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. ESPEI for Efficient Thermodynamic Database Development, Modification, and Uncertainty Quantification: Application to Cu–Mg, pages 393-416. Jenny Stanford Publishing, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 2 citations.

14. (alonso2025worldmineralsoutlook—cobalt pages 17-19): Elisa Alonso, Amanda Sarah Brioche, Ruth Schulte, Loyd M. Trimmer, Ji-Eun Kim, Andrew L. Gulley, and David George Pineault. World minerals outlook—cobalt, gallium, helium, lithium, magnesium, palladium, platinum, and titanium through 2029. Scientific Investigations Report, Jan 2025. URL: https://doi.org/10.3133/sir20255021, doi:10.3133/sir20255021. This article has 25 citations.

15. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

16. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

17. (nassar2025methodologyandtechnical pages 31-32): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

18. (blanc1991anexperimentalhuman pages 1-2): Paul D. Blanc, Hofer Wong, Michael S. Bernstein, and Homer A. Boushey. An experimental human model of metal fume fever. Annals of internal medicine, 114 11:930-6, Jun 1991. URL: https://doi.org/10.7326/0003-4819-114-11-930, doi:10.7326/0003-4819-114-11-930. This article has 124 citations and is from a highest quality peer-reviewed journal.
