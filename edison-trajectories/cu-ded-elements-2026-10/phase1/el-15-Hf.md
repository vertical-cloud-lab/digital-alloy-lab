<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: e97325ef-17fe-43f6-937a-6a4f3b8efab1
- Submitted: 2026-10-17T18:59:10Z
- Fetched: 2026-10-17T19:25:28Z (status: success)
- Raw trajectory JSON: ../raw/el-15-Hf.json.gz
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

ELEMENT UNDER REVIEW: Hf (strengthening addition). Cu-Hf precipitation alloys, studied as an analogue of Cu-Zr; Hf is costly and a US critical mineral.

Answer for Hf specifically, not for copper alloys in general:
1. ROLE: what Hf does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Hf ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Hf changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Hf, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Hf, Cu-Ni-Hf and Cu-Al-Hf are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Hf in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Hf neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Hf | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Hf (strengthening addition). Cu-Hf precipitation alloys, studied as an analogue of Cu-Zr; Hf is costly and a US critical mineral.

Answer for Hf specifically, not for copper alloys in general:
1. ROLE: what Hf does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Hf ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Hf changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Hf, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Hf, Cu-Ni-Hf and Cu-Al-Hf are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Hf in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Hf neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Hf | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Hafnium for as-deposited marine copper-alloy DED

**Decision: EXCLUDE Hf from the designed composition palette for both Cu–Ni and aluminum-bronze repair alloys.** This is a decision about *intentional alloying*, not a claim that trace Hf is prohibited. Hf demonstrably strengthens dilute copper through Cu₅Hf precipitation, but the strongest retrieved results required solution treatment, deformation, and aging—not the specified as-deposited condition. No located study establishes that an Hf addition improves seawater corrosion or crack-free blown-powder DED on Cu–Ni or cast NAB. The Cu-rich phase diagram and evidence for reaction with alumina introduce process risks, while the quoted metal price is high. Accordingly, a numerical marine-alloy ceiling, beneficial floor, or specification-derived impurity limit would be invented rather than evidence-based. (perry1974coppercu5hfalloystheir pages 1-3, loehman2003reactionandbonding pages 1-2, shangina2014improvementofstrength pages 1-2, shangina2014improvementofstrength pages 4-6, machacaUnknownyearextractionofnb pages 23-28)

The distinction between demonstrated behavior and the missing application-specific evidence is summarized below.

| Evidence category | Quantitative finding | Design implication |
|---|---|---|
| Verified Cu-rich phase and strengthening | Maximum reported α-Cu solubility is **0.87 wt% Hf at 965 °C**, falling below **0.04 wt% Hf at 500 °C**; the Cu-rich eutectic is **19.1 wt% Hf at 988 °C**. In Cu–0.9 wt% Hf, aging produced approximately 20 nm Cu₅Hf precipitates; after HPT and aging at 450 °C, hardness was **2,400 MPa** and conductivity was **71% IACS**. (perry1974coppercu5hfalloystheir pages 1-3, shangina2014improvementofstrength pages 4-6) | Demonstrates precipitation strengthening near **0.9 wt% Hf** after aging, but not seawater performance or as-deposited DED strengthening. The eutectic composition is not a defensible dilute-alloy bound. |
| Verified chloride analogue—not directly transferable | Bulk metallic glass `(Cu₀.₆Hf₀.₂₅Ti₀.₁₅)₁₀₀₋ₓNbₓ` was tested in **3 wt% NaCl at 298 K**. Corrosion fell below **0.001 mm/year** at 4 at.% Nb or more; **Nb, not Hf, was varied**, while Hf remained concentrated and the alloys were amorphous. (qin2005glassformationcorrosion pages 1-2, qin2005glassformationcorrosion pages 4-5, qin2005glassformationcorrosion pages 5-6) | Supports possible Hf/Ti-enriched oxide-film chemistry only in a concentrated multicomponent glass. It does **not** establish an Hf benefit, threshold, or qualification for Cu–Ni, NAB, crystalline DED deposits, or seawater service. |
| Missing directly transferable evidence | No located study quantifies Hf-dependent corrosion, selective attack, pitting, crevice corrosion, erosion–corrosion, velocity limits, DED cracking, reheated-layer liquation, or dilution in **Cu–Ni or NAB**. (yang2019theevolutionof pages 68-71, shangina2014improvementofstrength pages 1-2) | **No established conservative Hf bound** exists for the target marine or DED families. Any designed Hf addition requires a dedicated factorial corrosion-and-buildability screen rather than inference from metallic-glass or precipitation-hardening results. |


*Table: Separates verified Cu–Hf phase and strengthening data from an indirect chloride-resistant metallic-glass analogue and directly relevant evidence gaps. No commercial seawater qualification or established conservative Hf bound is inferred.*

## 1. Role and applicable alloy specifications

**[CITE] [NUMBERS] Demonstrated mechanism.** Hf has appreciable *high-temperature* solubility in α-Cu and much lower solubility on cooling. In experimentally prepared Cu–0.9 wt% Hf, subsequent aging produced approximately 20 nm Cu₅Hf particles that hardened the matrix and impeded grain growth. After quenching, high-pressure torsion, and 1 h at 450 °C, hardness was approximately **2,400 MPa** and electrical conductivity **71% IACS**. These are not properties demonstrated in an as-deposited marine alloy. The Cu–0.7 wt% Cr–0.9 wt% Hf variant also benefited from Cr and Cu₅Hf precipitation, so its results cannot be assigned to Hf alone. Shangina *et al.*, *Journal of Materials Science* **49** (2014), 6674–6681, doi:**10.1007/s10853-014-8339-4**. (shangina2014improvementofstrength pages 1-2, shangina2014improvementofstrength pages 2-4, shangina2014improvementofstrength pages 4-6)

**[SPEC] [NAVY] [GAP] Marine families.** No verified Hf-bearing grade or specified **Hf range in wt%** was found among the reviewed C71500 Cu–Ni, C95800 NAB, Cu–Ni–Sn, Cu–Ni–Si, manganese-aluminum bronze, tin bronze/gunmetal, or brass applications. Nor was a positive Hf allowance or Hf maximum verified in ASTM B111, B171, B466, B148, or B369; MIL-T-16420, MIL-B-24480, or MIL-C-15726; AWS A5.7; EN 12449; or a relevant UNS/CDA marine-alloy chemistry. **“Not specified” must not be translated into “0 wt% allowed” or into an impurity tolerance.** No retrieved Navy or DoD qualification or funding result demonstrates Hf in these marine fillers. For those families, grain refinement, deoxidation, inhibition of denickelification/dealuminification/dezincification, and a protective Hf-bearing seawater film remain *hypotheses*, not established roles. (qin2005glassformationcorrosion pages 1-2, shangina2014improvementofstrength pages 1-2, yang2019theevolutionof pages 68-71)

## 2. Seawater corrosion: what the measurements do—and do not—show

**[GAP]** No transferable Hf-dose series was located for crystalline Cu–Ni, NAB, or the other specified marine families in natural seawater, ASTM D1141 substitute ocean water, or 3.5 wt% NaCl. Consequently there is **no established Hf range that helps or harms** their corrosion, and no Hf-specific change in corrosion rate, *E*₍corr₎, impedance-derived film resistance, pitting or crevice behavior, selective-attack depth, erosion–corrosion, or allowable velocity that can be quoted. A 3.5 wt% NaCl study reported **29.0 µm/year for Hf-free Cu–30 wt% Ni** after a short electrochemical exposure; that is context for a comparator, **not** an Hf effect or a 30-day seawater acceptance value. Yang, *The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes* (UNSW dissertation, 2019), doi:**10.26190/unsworks/21760**. (yang2019theevolutionof pages 68-71)

**[CITE] [NUMBERS] Indirect, compositionally remote evidence.** Qin *et al.* cast amorphous Cu–Hf–Ti–Nb alloys and exposed them to **3 wt% NaCl at 298 K**. At Nb contents of at least **4 at% in the original study**—not an Hf-dose series—reported one-week mass-loss rates were below **0.001 mm/year**. XPS found Hf- and Ti-enriched oxidized surface species, but **Nb was the varied element**, and the material was a concentrated multicomponent glass rather than a dilute, crystalline Cu–Ni/NAB deposit. The at%-defined glass is deliberately **not recast as a supposed dilute-Hf wt% marine-alloy composition**. It cannot establish an Hf corrosion benefit or superiority to wrought C71500. Qin *et al.*, *Acta Materialia* **53** (2005), 3903–3911, doi:**10.1016/j.actamat.2005.04.037**. (qin2005glassformationcorrosion pages 1-2, qin2005glassformationcorrosion pages 4-5, qin2005glassformationcorrosion pages 5-6)

## 3. DED, welding, and repair interfaces

**[GAP]** The retrieved Cu–Hf strengthening experiments used arc melting followed by wrought/deformation and aging routes, **not** single-stream, infrared-fiber-laser blown-powder DED. No verified Hf-specific data quantify solidification cracking, reheated-layer liquation cracking, lack-of-fusion or gas porosity, oxidation/evaporation loss, or Hf partitioning after dilution into either cast C95800 or wrought C71500. In particular, use of ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl as *Hf-bearing* welding evidence would be unsupported: no Hf-bearing qualification or quantitative Hf effect in these fillers was verified. These remain necessary coupon-level tests, not asserted improvements from welding analogies. (shangina2014improvementofstrength pages 1-2, shangina2014improvementofstrength pages 2-4, yang2019theevolutionof pages 68-71)

**[CITE] Mechanistic risk, not an observed DED failure.** Low-temperature Cu-rich eutectic/intermetallic-bearing interdendritic material could provide a last-to-freeze or remelting path in a compositionally segregated DED track; Hf oxides could contribute inclusions. Whether either actually produces hot cracks or pores at proposed dilute concentrations must be measured. A high melting point for *elemental* Hf does not itself prove high laser-evaporation loss, nor does the binary eutectic prove that Hf prevents cracking. Cross-sections of first-layer/NAB and first-layer/Cu–Ni bonds, reheated overlaps, and locally diluted compositions are therefore essential if Hf is ever reconsidered. (perry1974coppercu5hfalloystheir pages 1-3, perry1974coppercu5hfalloystheir pages 3-6, loehman2003reactionandbonding pages 1-2)

## 4. Powder making and Cu–Hf phase limits

**[CITE] [NUMBERS] Binary constraints.** Perry reported maximum α-Cu solubility of **0.87 wt% Hf at approximately 965 °C**, falling below **0.04 wt% Hf at 500 °C**; the Cu-rich eutectic occurs at **19.1 wt% Hf and 988 °C**. Cu₅Hf participates in the eutectic, and Cu₅Hf was reported to form peritectically from Cu₄Hf. These measurements are for **binary Cu–Hf**: 19.1 wt% Hf is *not* a recommended powder composition, and 0.87 wt% is *not* a demonstrated safe marine-DED limit. The inspected Cu-rich phase diagram provides visual corroboration of the eutectic location. Perry, “Copper–Cu₅Hf alloys: Their constitution and some properties after directional solidification,” *Materials Science and Engineering* **13** (1974), 57–62, doi:**10.1016/0025-5416(74)90021-4**. (perry1974coppercu5hfalloystheir pages 1-3, perry1974coppercu5hfalloystheir pages 3-6, shangina2014improvementofstrength media 6e817154)

**[CITE] [GAP] Melting and interfaces.** Perry melted Cu–Hf charges in **boron-nitride crucibles under argon**, not in the specified alumina/zirconia ultrasonic atomizer. Sandia researchers observed Hf segregation toward ceramic interfaces; in a related Ag–Cu–Hf/alumina braze they identified interfacial HfO₂ by TEM. Their separate Ag–Hf tests showed limited visible reaction with alumina but a more continuous reaction layer against silica. This supports **testing** Hf recovery and oxide inclusion formation with the actual alumina crucible; it does not establish a loss percentage in a Cu melt. No quantitative compatibility or contamination result was located for a zirconia or graphite crucible, Ti-alloy or Mo sonotrode, nor a measured Hf-dependent liquid surface tension, atomization yield, vapor loss, or laser fume generation. Loehman *et al.*, *Journal of the European Ceramic Society* **23** (2003), 2805–2811, doi:**10.1016/S0955-2219(03)00292-9**. (perry1974coppercu5hfalloystheir pages 1-3, loehman2003reactionandbonding pages 1-2, loehman2003reactionandbonding pages 2-5)

**[CITE] [GAP] Liquidus and CALPHAD.** The *Cu-rich binary* eutectic is below pure Cu’s melting point; it does **not** support a claim that dilute Hf alone drives a Cu-rich melt above the approximately **1,200–1,250 °C** usable atomization-liquidus window. Conversely, it cannot clear a Ni-, Fe-, or Al-bearing multicomponent candidate: calculate its full liquidus and required superheat experimentally and with a validated database. A published **Cu–Hf binary thermodynamic assessment** is identified by Turchanin and Agraval, “Thermodynamic Assessment of the Copper–Hafnium System,” *Powder Metallurgy and Metal Ceramics* **47** (2008), 223–233, doi:**10.1007/s11106-008-9008-4**. Thermo-Calc **TCHEA3** documentation explicitly includes and assesses binary Cu–Hf; its displayed fully assessed ternaries do **not** establish fully assessed Cu–Ni–Hf or Cu–Al–Hf. Turchanin *et al.* developed a Cu–Hf–Ni–Ti–Zr **liquid-property** CALPHAD model, not a demonstrated validation of the complete dilute marine-alloy solidification description: *Journal of Phase Equilibria and Diffusion* **42** (2021), 623–646, doi:**10.1007/s11669-021-00898-6**. Whether the installed **TCCU** release, COST 531, or an accessible published TDB provides validated Cu–Ni–Hf/Cu–Al–Hf parameters **was not verified**; check its element and phase lists before interpreting a Thermo-Calc or pycalphad result. (turchanin2021thermodynamicsandchemical pages 22-23, perry1974coppercu5hfalloystheir pages 1-3, tiUnknownyeartchea3tcshigh pages 1-4, turchanin2021thermodynamicsandchemical pages 1-2)

## 5. Supply, occupational controls, and joint constraints

**[CITE] [NUMBERS] Supply and cost.** A USGS review explicitly names Hf on the **final November 2025 U.S. critical-minerals list**; the retrieved passage does not independently display its entry on the **2022** list, so that year’s Hf status is not asserted here without the original notice. A 2026 extraction paper cites an indicative **2024 Hf price of US$4,657/kg**, warns that quotations vary, and attributes the number to a market-price reference; it is **not** a verified current purchasing quote for certified alloy feedstock. At that indicative price, **0.9 wt% Hf** represents approximately **US$42 of Hf per kilogram of alloy charge** before processing losses. USGS Nassar *et al.*, *Open-File Report 2025–1047*, doi:**10.3133/ofr20251047**; Cheje Machaca *et al.*, *International Journal of Minerals, Metallurgy and Materials* **33** (2026), 1966–1979, doi:**10.1007/s12613-025-3367-x**. (iii2026usgscriticalminerals pages 1-2, turchanin2021thermodynamicsandchemical pages 1-2, machacaUnknownyearextractionofnb pages 23-28)

**[CITE] [NUMBERS] [GAP] Safety and restrictions.** A published alloy-design review lists an occupational exposure limit of **0.5 mg/m³ for Hf**, but its compiled OSHA/NIOSH table does **not** establish whether that number is specifically an enforceable OSHA Hf PEL rather than another occupational guideline. Do not label it an OSHA PEL without checking the applicable substance/form and regulation. Capture airborne atomization dust and laser fume, prevent combustible-metal-powder accumulation, and assess actual particle size, oxide content, and exposure. No Hf-specific Navy prohibition, RoHS restriction, or REACH restriction was verified; absence of a verified restriction is not a waiver. Schoenung, Ogunseitan and He, *Journal of Sustainable Metallurgy* **11** (2025), 3495–3510, doi:**10.1007/s40831-025-01250-9**. (schoenung2025humanhealthand pages 7-9, schoenung2025humanhealthand pages 9-10)

**[GAP] Interactions for joint constraints.** Cu₅Hf precipitation ties the available Hf to Cu-rich solid solution and cooling history; demonstrated Cu–Cr–Hf strengthening involves **both** Cr particles and Cu₅Hf. Hf and Zr occupied the intermetallic phase together in Perry’s experimental Cu–Hf–Zr alloys. Hf’s oxide-forming affinity makes oxygen pickup and ceramic contact plausible competitors for dissolved, strengthening-active Hf. There is **no validated marine-DED sum or ratio** involving Hf with Ni, Fe, Mn, Al, Sn, or Si, and no measured quantity by which Hf neutralizes—or worsens—selective dissolution in those families. Such constraints must not be invented from the Cu–Cr–Hf or concentrated-glass studies. (perry1974coppercu5hfalloystheir pages 3-6, shangina2014improvementofstrength pages 1-2, shangina2014improvementofstrength pages 4-6, qin2005glassformationcorrosion pages 5-6, loehman2003reactionandbonding pages 1-2)

## 6. Bounds and evidence quality

**[GAP] Evidence quality: thin for the decision context.** The binary equilibrium and post-aged precipitation mechanism are credible; marine corrosion, as-deposited strength, single-stream DED buildability, repair-interface behavior, and a validated multicomponent phase boundary are not established. Under **EXCLUDE**, the requested conservative maximum, non-conservative maximum, functional floor, and impurity maximum are therefore all **NA** for **both** target families. Neither the **0.87 wt%** high-temperature solubility nor the **0.9 wt%** mechanically processed experimental composition is a specification-qualified marine bound. The exclusion is set by the *unverified seawater and cracking performance plus powder-process uncertainty and cost*, not by a proved deleterious Hf threshold. If a separate, explicitly exploratory study proceeds, those numbers can motivate test compositions only after feedstock analysis, dilution mapping, actual liquidus measurement, and as-deposited 30-day corrosion comparisons against wrought C71500—not as preapproved limits. (perry1974coppercu5hfalloystheir pages 1-3, loehman2003reactionandbonding pages 1-2, shangina2014improvementofstrength pages 1-2, shangina2014improvementofstrength pages 4-6, qin2005glassformationcorrosion pages 4-5, machacaUnknownyearextractionofnb pages 23-28)

VERDICT | Hf | decision=EXCLUDE | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (perry1974coppercu5hfalloystheir pages 1-3): A.J Perry. Copper-cu5hf alloys: their constitution and some properties after directional solidification. Materials Science and Engineering, 13:57-62, Jan 1974. URL: https://doi.org/10.1016/0025-5416(74)90021-4, doi:10.1016/0025-5416(74)90021-4. This article has 13 citations.

2. (loehman2003reactionandbonding pages 1-2): Ronald E. Loehman, Bryan D. Gauntt, F. Michael Hosking, Paul G. Kotula, Summer Rhodes, and John J. Stephens. Reaction and bonding of hf and zr containing alloys to alumina and silica. Journal of The European Ceramic Society, 23:2805-2811, Jan 2003. URL: https://doi.org/10.1016/s0955-2219(03)00292-9, doi:10.1016/s0955-2219(03)00292-9. This article has 15 citations and is from a domain leading peer-reviewed journal.

3. (shangina2014improvementofstrength pages 1-2): D. V. Shangina, J. Gubicza, E. Dodony, N. R. Bochvar, P. B. Straumal, N. Yu. Tabachkova, and S. V. Dobatkin. Improvement of strength and conductivity in cu-alloys with the application of high pressure torsion and subsequent heat-treatments. Journal of Materials Science, 49:6674-6681, Jun 2014. URL: https://doi.org/10.1007/s10853-014-8339-4, doi:10.1007/s10853-014-8339-4. This article has 78 citations and is from a peer-reviewed journal.

4. (shangina2014improvementofstrength pages 4-6): D. V. Shangina, J. Gubicza, E. Dodony, N. R. Bochvar, P. B. Straumal, N. Yu. Tabachkova, and S. V. Dobatkin. Improvement of strength and conductivity in cu-alloys with the application of high pressure torsion and subsequent heat-treatments. Journal of Materials Science, 49:6674-6681, Jun 2014. URL: https://doi.org/10.1007/s10853-014-8339-4, doi:10.1007/s10853-014-8339-4. This article has 78 citations and is from a peer-reviewed journal.

5. (machacaUnknownyearextractionofnb pages 23-28): Darwin Michell Cheje Machaca, Rosario Belen Juyo Salazar, Thamyres Cardoso de Carvalho, Denise Crocce Romano Espinosa, and Jorge Alberto Soares Tenório. Extraction of nb, ta, zr and hf from tin slags originating from cassiterite beneficiation. International Journal of Minerals, Metallurgy and Materials, 33:1966-1979, Jun 2026. URL: https://doi.org/10.1007/s12613-025-3367-x, doi:10.1007/s12613-025-3367-x. This article has 0 citations.

6. (qin2005glassformationcorrosion pages 1-2): Chunling Qin, Wei Zhang, Katsuhiko Asami, Naofumi Ohtsu, and Akihisa Inoue. Glass formation, corrosion behavior and mechanical properties of bulk glassy cu–hf–ti–nb alloys. Acta Materialia, 53:3903-3911, Aug 2005. URL: https://doi.org/10.1016/j.actamat.2005.04.037, doi:10.1016/j.actamat.2005.04.037. This article has 75 citations and is from a highest quality peer-reviewed journal.

7. (qin2005glassformationcorrosion pages 4-5): Chunling Qin, Wei Zhang, Katsuhiko Asami, Naofumi Ohtsu, and Akihisa Inoue. Glass formation, corrosion behavior and mechanical properties of bulk glassy cu–hf–ti–nb alloys. Acta Materialia, 53:3903-3911, Aug 2005. URL: https://doi.org/10.1016/j.actamat.2005.04.037, doi:10.1016/j.actamat.2005.04.037. This article has 75 citations and is from a highest quality peer-reviewed journal.

8. (qin2005glassformationcorrosion pages 5-6): Chunling Qin, Wei Zhang, Katsuhiko Asami, Naofumi Ohtsu, and Akihisa Inoue. Glass formation, corrosion behavior and mechanical properties of bulk glassy cu–hf–ti–nb alloys. Acta Materialia, 53:3903-3911, Aug 2005. URL: https://doi.org/10.1016/j.actamat.2005.04.037, doi:10.1016/j.actamat.2005.04.037. This article has 75 citations and is from a highest quality peer-reviewed journal.

9. (yang2019theevolutionof pages 68-71): The Evolution of Corrosion and Electrochemical Behaviour of High Entropy Brasses and Bronzes This article has 2 citations.

10. (shangina2014improvementofstrength pages 2-4): D. V. Shangina, J. Gubicza, E. Dodony, N. R. Bochvar, P. B. Straumal, N. Yu. Tabachkova, and S. V. Dobatkin. Improvement of strength and conductivity in cu-alloys with the application of high pressure torsion and subsequent heat-treatments. Journal of Materials Science, 49:6674-6681, Jun 2014. URL: https://doi.org/10.1007/s10853-014-8339-4, doi:10.1007/s10853-014-8339-4. This article has 78 citations and is from a peer-reviewed journal.

11. (perry1974coppercu5hfalloystheir pages 3-6): A.J Perry. Copper-cu5hf alloys: their constitution and some properties after directional solidification. Materials Science and Engineering, 13:57-62, Jan 1974. URL: https://doi.org/10.1016/0025-5416(74)90021-4, doi:10.1016/0025-5416(74)90021-4. This article has 13 citations.

12. (shangina2014improvementofstrength media 6e817154): D. V. Shangina, J. Gubicza, E. Dodony, N. R. Bochvar, P. B. Straumal, N. Yu. Tabachkova, and S. V. Dobatkin. Improvement of strength and conductivity in cu-alloys with the application of high pressure torsion and subsequent heat-treatments. Journal of Materials Science, 49:6674-6681, Jun 2014. URL: https://doi.org/10.1007/s10853-014-8339-4, doi:10.1007/s10853-014-8339-4. This article has 78 citations and is from a peer-reviewed journal.

13. (loehman2003reactionandbonding pages 2-5): Ronald E. Loehman, Bryan D. Gauntt, F. Michael Hosking, Paul G. Kotula, Summer Rhodes, and John J. Stephens. Reaction and bonding of hf and zr containing alloys to alumina and silica. Journal of The European Ceramic Society, 23:2805-2811, Jan 2003. URL: https://doi.org/10.1016/s0955-2219(03)00292-9, doi:10.1016/s0955-2219(03)00292-9. This article has 15 citations and is from a domain leading peer-reviewed journal.

14. (turchanin2021thermodynamicsandchemical pages 22-23): Mikhail Turchanin, Pavel Agraval, Liya Dreval, and Anna Vodopyanova. Thermodynamics and chemical ordering of liquid cu-hf-ni-ti-zr alloys. Journal of Phase Equilibria and Diffusion, 42:623-646, Jun 2021. URL: https://doi.org/10.1007/s11669-021-00898-6, doi:10.1007/s11669-021-00898-6. This article has 23 citations and is from a peer-reviewed journal.

15. (tiUnknownyeartchea3tcshigh pages 1-4): RRSST Ti and VWYZ Zr. Tchea3: tcs high entropy alloy database. Unknown journal, Unknown year.

16. (turchanin2021thermodynamicsandchemical pages 1-2): Mikhail Turchanin, Pavel Agraval, Liya Dreval, and Anna Vodopyanova. Thermodynamics and chemical ordering of liquid cu-hf-ni-ti-zr alloys. Journal of Phase Equilibria and Diffusion, 42:623-646, Jun 2021. URL: https://doi.org/10.1007/s11669-021-00898-6, doi:10.1007/s11669-021-00898-6. This article has 23 citations and is from a peer-reviewed journal.

17. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

18. (schoenung2025humanhealthand pages 7-9): Julie M. Schoenung, Oladele A. Ogunseitan, and Haoyang He. Human health and ecotoxicity considerations in metallic alloy design. Journal of Sustainable Metallurgy, 11:3495-3510, Sep 2025. URL: https://doi.org/10.1007/s40831-025-01250-9, doi:10.1007/s40831-025-01250-9. This article has 3 citations and is from a peer-reviewed journal.

19. (schoenung2025humanhealthand pages 9-10): Julie M. Schoenung, Oladele A. Ogunseitan, and Haoyang He. Human health and ecotoxicity considerations in metallic alloy design. Journal of Sustainable Metallurgy, 11:3495-3510, Sep 2025. URL: https://doi.org/10.1007/s40831-025-01250-9, doi:10.1007/s40831-025-01250-9. This article has 3 citations and is from a peer-reviewed journal.
