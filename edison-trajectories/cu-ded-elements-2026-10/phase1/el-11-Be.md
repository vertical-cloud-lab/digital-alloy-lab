<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 6c901ba2-c872-41f4-bb94-288e98a8c5fc
- Submitted: 2026-10-17T18:58:59Z
- Fetched: 2026-10-17T19:30:34Z (status: success)
- Raw trajectory JSON: ../raw/el-11-Be.json.gz
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

ELEMENT UNDER REVIEW: Be (strengthening addition). Beryllium coppers C17200 (1.8-2.0 Be), C17510 (0.2-0.6 Be with 1.4-2.2 Ni), C17500 (Co-Be); Navy uses include undersea housings and non-sparking tools. Be powder and fume are toxic (OSHA 2017 beryllium standard).

Answer for Be specifically, not for copper alloys in general:
1. ROLE: what Be does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Be ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Be changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Be, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Be, Cu-Ni-Be and Cu-Al-Be are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Be in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Be neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Be | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Be (strengthening addition). Beryllium coppers C17200 (1.8-2.0 Be), C17510 (0.2-0.6 Be with 1.4-2.2 Ni), C17500 (Co-Be); Navy uses include undersea housings and non-sparking tools. Be powder and fume are toxic (OSHA 2017 beryllium standard).

Answer for Be specifically, not for copper alloys in general:
1. ROLE: what Be does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Be ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Be changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Be, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Be, Cu-Ni-Be and Cu-Al-Be are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Be in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Be neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Be | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Beryllium (Be): composition-palette decision

**Decision: LIMIT Be as an impurity, not a designed addition.** Be can strengthen copper and improve the chloride-bearing *marine-atmosphere* corrosion of a conventional Cu–Be alloy, but that is not evidence that an **as-deposited, single-stream DED** Cu–Ni or nickel–aluminum bronze (NAB) repair will match wrought C71500 in immersed seawater. The best directly relevant NAB impurity investigation proposed **0.10 wt% Be** as a *possible* C95800 impurity limit, not as a beneficial addition; it found reduced ductility with impurity additions, but did **not** attribute its observed heat-affected-zone cracking to Be. In contrast, deliberately adding even modest Be creates a consequential powder-and-laser-fume exposure problem under an occupational limit of **0.2 µg Be/m³**, eight-hour time-weighted average. Specify **Be ≤0.10 wt% in both powder and deposit**, as a provisional procurement ceiling rather than a proven safe or corrosion-neutral threshold; target no intentional addition and the lowest analytically practicable content. This ceiling must be reconsidered if a Navy material specification, industrial-hygiene assessment, or qualification test is stricter. [CITE][NUMBERS][GAP] (allen2000castmetalcoalition pages 9-10, nelson2026assessmentofberyllium pages 3-4, mcmanus2020criticalparticulatecontaminant(s) pages 4-6)

## 1. Metallurgical role and identifiable alloys

**Mechanisms.** Dissolved Be supplies solid-solution strengthening, but the characteristic high strength of commercial Cu–Be comes principally from **solution treatment followed by aging**: Guinier–Preston zones evolve into coherent and partially coherent precipitates; Ni–Be-bearing beryllide particles can form during solidification and thermal processing. Thus the tensile properties of conventionally aged C17200/C17510 cannot be assigned to an unaged DED deposit. In the one measured marine-exposure study, preferential oxidation and outward enrichment produced an outer Be-rich, Cu-poor corrosion-product region containing **BeO**; the investigators proposed that its low electronic conductivity impedes aggressive-ion transport. These are precipitation and film-chemistry mechanisms, respectively—not demonstrated grain refinement, deoxidation sufficient to prevent DED porosity, or suppression of dezincification/dealuminification in another alloy family. [CITE] (murray1994fracturetestingand pages 5-7, murray1994fracturetestingand pages 3-5, kong2018insightintothe pages 8-12)

| Material or source | Be, **wt%** | What the range establishes |
|---|---:|---|
| **UNS C17200** high-strength Cu–Be | **1.8–2.0** | Established heat-treatable commercial alloy; the cited engineering paper also describes approximately **0.2 wt% Ni**. **[SPEC][NUMBERS]** (murray1994fracturetestingand pages 3-5) |
| **UNS C17510** Cu–Ni–Be | **0.2–0.7** in the cited technical report; the user-supplied narrower range is **0.2–0.6** | Established *aged* conductivity/strength alloy, with approximately **1.4–2.2 wt% Ni/Co** in that report; its wording does not resolve individual Ni versus Co limits. Do not substitute this research-paper range for the current procurement specification. **[SPEC][NUMBERS]** (murray1994fracturetestingand pages 3-5) |
| **UNS C17410**, Cu–Co–Be | **0.15–0.50**; Co **0.35–0.60** | Published UNS-comparison composition, not evidence of seawater or DED qualification. Its separately measured experimental specimen had **0.215 wt% Be** and is **not** the universal C17410 composition. **[SPEC][NUMBERS]** (berto2015hightemperaturefatigue pages 1-3) |
| Cu–Co–Be and Cu–Ni–Be wrought alloy families | approximately **0.4–0.7** and **0.2–0.6**, respectively | A Copper Development Association-derived table documents these families, but its extracted column alignment does **not** securely assign every number to a UNS grade. **[NUMBERS]** (coppers1999copperdevelopmentassociation pages 64-65) |
| **UNS C17500** | **Not independently verified here** | A commercial Co–Be grade is mentioned in the retrieved technical literature, but a defensible current Be specification range could not be confirmed from an inspected standard. **[GAP]** (coppers1999copperdevelopmentassociation pages 64-65) |
| **C95800 NAB**, cast-alloy impurity investigation | **proposed maximum 0.10**, *not an established ASTM B148 limit verified here* | Proposed limit following tests of multiple impurities; not a designed-Be NAB grade. **[NUMBERS][GAP]** (allen2000castmetalcoalition pages 9-10) |

**Scope of specifications.** The inspected evidence does **not** establish an intentional-Be range for ASTM B111/B171/B466 C71500 Cu–Ni, ASTM B148 C95800 NAB, ASTM B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7 ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl, or EN 12449. None should be represented as authorizing a Be-bearing repair filler on the basis of this search. Nor was a commercial Be-bearing Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si *marine repair alloy* established. The existence of Cu–Al–Be shape-memory compositions would not make them NAB alloys or qualify them for seawater repair. [SPEC][GAP] (liu2003thermodynamicdatabaseon pages 2-5, allen2000castmetalcoalition pages 9-10)

## 2. Quantitative corrosion evidence—and its limits

**[CITE][NUMBERS] Kong et al., 2018.** The actual tested QBe2 contained **1.98 wt% Be, 0.30 wt% Ni and 0.05 wt% Fe**, Cu balance. Its controls were unalloyed Cu and QSn6.5-0.1 containing **6.27 wt% Sn, 0.13 wt% P, 0.11 wt% Ni and 0.03 wt% Fe**, Cu balance. Outdoor exposure on Hainan was to a humid, chloride-depositing **marine atmosphere** (mean chloride deposition **48.5 mg m⁻² day⁻¹**), **not continuous seawater immersion**. At **6 months**, Cu/tin bronze/QBe2 mass-loss rates were **45.6/46.4/17.1 g m⁻² year⁻¹**; at **12 months**, **42.2/38.0/15.5 g m⁻² year⁻¹**. QBe2 therefore lost approximately **63% less mass than Cu** and **59% less than tin bronze** at 12 months. Average pit depths in that order were **9/6.2/4.2 µm** at 6 months and **15.7/10.2/7.1 µm** at 12 months; maximum depths were **12/9/7 µm** and **19/16/14 µm**, respectively. *All three pitted*: Be reduced, rather than eliminated, attack. BeO was detected in an approximately **0.3 µm** Be-enriched outer region of an approximately **2.2 µm** product layer. Because the alloys differ in more than Be and include differing processing histories, this is not a controlled Be-dose response in Cu–Ni or NAB. (kong2018insightintothe pages 1-5, kong2018insightintothe pages 5-8, kong2018insightintothe pages 8-12, kong2018insightintothe pages 12-15)

The same investigators briefly immersed initially unexposed specimens in **3.5 wt% NaCl**, rather than measuring year-long immersed-seawater loss: QBe2 **E_corr −192.5 mV versus SCE; i_corr 4.63 µA cm⁻²**; Cu **−216.5 mV; 4.73 µA cm⁻²**; tin bronze **−218.7 mV; 6.58 µA cm⁻²**. The measured QBe2–Cu *initial* current difference is only **0.10 µA cm⁻²** (~**2%**), much less striking than the outdoor mass-loss contrast. After **6/12 months outdoor weathering**, subsequent NaCl EIS gave QBe2 film resistance **7,818/15,900 Ω cm²**, versus Cu **6,119/5,720** and tin bronze **11,000/11,400 Ω cm²**: **QBe2 did not have the highest film resistance at six months**. Its 12-month fitted pit-branch resistance was **7,676 Ω cm²**, versus **6,537** for Cu and **5,174** for tin bronze. The authors explicitly distinguish this laboratory NaCl assessment from their field exposure. No helpful-versus-harmful *Be concentration interval* is established by these one-composition comparisons. [CITE][NUMBERS] (kong2018insightintothe pages 19-23, kong2018insightintothe pages 28-32, kong2018insightintothe pages 5-8, kong2018insightintothe pages 8-12)

**[GAP] Seawater acceptance remains unproven.** No inspected Be-dose-series demonstrates immersed natural seawater or ASTM D1141 performance relative to wrought **70–30 Cu–Ni C71500**, including 30-day selective-attack depth. There are no defensible Be-specific thresholds for crevice corrosion, biofouling, dealloying inhibition, erosion-corrosion, or allowable seawater velocity in either candidate repair family. A brine review describes cupronickels as highly seawater-resistant and Be–Cu only as slightly better than ordinary Cu, but does not supply a comparable C17200-versus-C71500 test; combining their unrelated rates would be misleading. Nor do these data establish a range where Be *harms* seawater corrosion: such a threshold is unknown, not zero. [GAP] (kong2018insightintothe pages 19-23, banning1973corrosionresistanceof pages 16-19)

## 3. DED, welding, and substrate dilution

**[CITE][GAP] Precedent is welding, not Be-bearing blown-powder DED.** C17510 plate was reportedly welded with **C17200 filler** for an unrelated fusion-magnet project, showing that joining a Be-bearing copper is possible; that work does not establish a crack-free Be-bearing DED build, corrosion-resistant marine joint, or an as-deposited precipitation response. A cast-C95800 impurity program studied Be alongside Pb, Bi, Zn, Sn, Se, Cr and Si, singly and in combinations. Added impurities adversely affected ductility, whereas **only Pb and Bi** were identified as causing heat-affected-zone cracking in its weldability observations. Consequently, calling **0.10 wt% Be** a measured NAB liquation-cracking onset would misstate the result. [NAVY][NUMBERS][GAP] (murray1994fracturetestingand pages 5-7, allen2000castmetalcoalition pages 9-10)

For sequential DED layers, segregation of Be or Ni–Be phases and reheating of any locally enriched boundaries are **plausible** solidification/liquation-cracking concerns; Be oxidation can plausibly contribute oxide inclusions and lack-of-fusion/porosity, and laser vaporization can change chemistry and generate hazardous particulate. **None of these Be-specific rates, crack thresholds or deposition-to-powder recovery factors was measured in the inspected studies.** The literature on infrared-laser copper AM establishes a *general* high-reflectivity/high-thermal-conductivity process difficulty, not a measured Be remedy. [CITE][GAP] (murray1994fracturetestingand pages 5-7, jr1968technologyandusesa pages 14-19)

At a NAB fusion boundary, Al, Fe, Ni and Mn from **C95800** enter the first bead; on wrought Cu–Ni, Ni enters it. Their local compositions—not just the powder assay—govern primary phases, Be partitioning, interdendritic material, galvanic contrast and possible selective attack. A single-stream feed offers no separate interlayer to isolate either interface. **No measured Be partition coefficient, permissible dilution, Be–Al/Ni reaction map, or Be-containing AWS A5.7 filler qualification was found.** Do not transfer ordinary ERCuNi or aluminum-bronze filler crack or corrosion performance to a modified Be-bearing powder. [SPEC][GAP] (liu2003thermodynamicdatabaseon pages 2-5, allen2000castmetalcoalition pages 9-10)

## 4. Powder production; phase diagrams and CALPHAD

**[CITE][GAP] Melt and atomization.** Be is oxygen-reactive; historical Be metallurgy reports noticeable oxidation at approximately **700 °C**, rapid oxidation at **≥1,000 °C**, and ready reaction of *finely divided elemental Be* with air. These observations make oxygen pickup, BeO-bearing inclusions, melt/powder composition drift and airborne contamination credible issues despite argon shielding. They do **not** quantify Be activity or oxidation kinetics in the proposed Cu-rich **0.5 kg** melt, and elemental-Be powder behavior should not be treated as measured behavior of pre-alloyed Cu powder. Prefer controlled master-alloy charging and oxygen/Be mass-balance measurements over assuming quantitative retention. The inspected evidence establishes **no** attack rate for liquid Cu–Be on alumina or zirconia crucibles, graphite, a Ti-alloy or Mo ultrasonic sonotrode; no Be-specific melt surface-tension shift or atomization-size distribution; and no measured Be-vapor loss under the specified **~1.07 µm** laser. Treat each as a qualification experiment, not an established compatibility failure or benefit. (jr1968technologyandusesa pages 14-19, mcmanus2020criticalparticulatecontaminant(s) pages 4-6)

**[CITE] Thermodynamic coverage is not interchangeable across databases.** Liu *et al.* explicitly list **Cu–Be binary** and **Cu–Ni–Be ternary** in their *published assessed copper-alloy database* and illustrate the calculated Cu–Be binary, including an ordering-associated **β(B2)/γ(A2)** bcc-region miscibility feature. Their displayed assessment inventory does **not** identify **Cu–Al–Be**. This is evidence that an assessment exists; it does **not** establish that a licensed **Thermo-Calc TCCU** installation or **COST 531** contains those same parameters, nor that its phases can be exported as a redistribution-ready `.tdb` for pycalphad. Verify `BE` and all required phase descriptions directly in the installed database and compare its calculated binary/ternary equilibria against published diagrams before using it for inverse design. [GAP] (liu2003thermodynamicdatabaseon pages 2-5, liu2003thermodynamicdatabaseon pages 1-2, liu2003thermodynamicdatabaseon media 751da32c)

**[NUMBERS][GAP] Solubility, reactions, liquidus.** The inspected text/figure establishes Cu–Be phase assessment and the existence of beryllides, but does **not** provide a sufficiently readable, independently verified numeric **maximum Cu-rich Be solubility in wt% and its temperature**, complete named Cu–Be invariant-reaction temperatures/compositions, or liquidus numbers for each proposed *multicomponent* powder. Those requested numbers should not be fabricated from an unreadable figure. Copper-rich commercial Cu–Be existence alone does not show that Be drives liquidus above **~1,250 °C**; conversely, its use cannot certify adequate superheat for a high-Ni or high-Al composition. Calculate *each complete composition’s* liquidus, Scheil terminal phases and liquid fraction at the atomizer's usable pour temperature, then measure melting behavior before approving it. [GAP] (liu2003thermodynamicdatabaseon pages 2-5, murray1994fracturetestingand pages 5-7, liu2003thermodynamicdatabaseon media 751da32c)

## 5. Supply, safety, composition rule and interactions

**[NAVY][CITE] Strategic status.** Be appears on both the **2022** and **final 2025** U.S. critical-minerals lists; Cu appears on the final 2025 list. A USGS *technical input* report must not be mistaken for the final list: the separately inspected final-list table explicitly names Be and Cu. These classifications establish strategic relevance, not a Be supply shortage for this particular research charge. **An auditable approximate $/kg price for a specified Be metal/master-alloy product and date was not recoverable here; no quote is asserted.** [GAP] (staff2022usgsminingreview pages 6-9, nassar2025methodologyandtechnical pages 1-4)

**[CITE][NUMBERS] Exposure, not bulk percentage, is the safety endpoint.** A peer-reviewed 2026 occupational discussion gives the U.S. OSHA airborne Be **PEL 0.2 µg/m³, eight-hour TWA**, and **2 µg/m³ short-term ceiling**; the welding-fume study independently quotes the **0.2 µg/m³** limit and warns that trace Be in fume can be difficult to quantify. Sensitization, chronic beryllium disease and carcinogenicity warrant containment, HEPA-filtered source extraction, industrial-hygiene sampling, wet/HEPA cleaning, powder segregation and documented waste controls for melting, atomization, sieving, DED, grinding and repair removal. Argon process shielding is **not** respiratory containment. The requested OSHA regulatory exclusion/action-level wording, applicable RoHS/REACH treatment of a specific alloy product, and any binding Navy-wide Be prohibition were **not verified** in the inspected primary sources: **0.10 wt% is neither an OSHA exposure exemption nor a declaration of RoHS/REACH compliance**. Request current EHS and procurement review rather than claiming such an exemption. [NAVY][GAP] (nelson2026assessmentofberyllium pages 3-4, mcmanus2020criticalparticulatecontaminant(s) pages 4-6)

**[SPEC][NUMBERS] Binding design-screen instruction.** **LIMIT; Cu–Ni and Al-bronze branches alike; Be ≤0.10 wt% in incoming powder *and* analyzed deposit; no Be addition target.** Source: Allen, *Cast Metal Coalition Research and Development Closeout Report* (2000), *proposed* C95800 Be impurity maximum, **doi:10.2172/765235**—**not** an authenticated ASTM B148/C71500/AWS maximum or a proven safe boundary. The failure mode motivating its transfer to both branches is an unqualified, toxic, compositionally drifting Be-bearing powder/deposit, with observed *combined-impurity* ductility loss in cast NAB; Be-specific cracking or corrosion failure **at 0.10 wt% has not been shown**. Because the choice is LIMIT, **conservative maximum, non-conservative maximum and functional floor are not assigned**. The lowest *measured marine-film effect* found here was at **1.98 wt%**, whereas **0.15 wt%** is a commercial Cu–Co–Be specification minimum for a different, age-hardened application—not a validated corrosion floor for this proposal. [GAP] (allen2000castmetalcoalition pages 9-10, kong2018insightintothe pages 1-5, berto2015hightemperaturefatigue pages 1-3)

**Joint constraints to retain.** Track **Be–Ni** and **Be–Co** jointly because Be-bearing beryllides and aged strength require their chemistry; C17510 and C17410 bounds cannot be applied independently to an arbitrary Ni-poor powder. Track **Be–Al–Ni–Fe–Mn** at the diluted NAB interface, and **Be–Ni** at the Cu–Ni interface, using measured dilution and phase predictions rather than inventing a stoichiometric ratio. Minimize O ingress because it consumes Be into BeO while generating particles/fume; monitor simultaneous **Pb and Bi** because these—not Be—were the impurity-study elements actually linked to C95800 weld-HAZ cracks. No evidence establishes that Be neutralizes Zn dealloying, Fe/Mn-related seawater attack, or Cu–Ni–Sn/Cu–Ni–Si precipitate damage. [CITE][GAP] (murray1994fracturetestingand pages 5-7, allen2000castmetalcoalition pages 9-10, kong2018insightintothe pages 8-12)

**Evidence grade: thin for this decision's intended marine DED application.** The strong *narrow* finding is that a **1.98 wt% Be wrought Cu–Be** composition resisted one outdoor chloride-bearing marine atmosphere better than its Cu and tin-bronze controls. Evidence is indirect or absent for Be-dose dependence, Be-bearing powder/laser behavior, as-deposited film formation, joint corrosion on NAB/Cu–Ni, and parity with C71500 during continuous seawater immersion. Therefore no claim that an impurity-level Be limit itself improves corrosion is warranted. [CITE][GAP] (kong2018insightintothe pages 1-5, kong2018insightintothe pages 5-8, kong2018insightintothe pages 19-23)

**Principal sources and identifiers.** Kong D. *et al.*, “Insight into the mechanism of alloying elements (Sn, Be) effect on copper corrosion during long-term degradation in harsh marine environment,” *Applied Surface Science* **455** (2018) 543–553, **doi:10.1016/j.apsusc.2018.06.029**. Liu X.J. *et al.*, “Thermodynamic database on microsolders and copper-based alloy systems,” *Journal of Electronic Materials* **32** (2003) 1265–1272, **doi:10.1007/s11664-003-0021-6**. Murray H.A., Zatz I.J. and Ratka J.O., “Fracture testing and performance of beryllium copper alloy C17510,” *ASTM STP* (1994) 109–133, **doi:10.1520/STP18122S**. Allen D., *Cast Metal Coalition Research and Development Closeout Report* (2000), **doi:10.2172/765235**. Berto F., Gallo P. and Lazzarin P., “High temperature fatigue tests of a Cu-Be alloy…,” *Key Engineering Materials* **627** (2015) 77–80, **doi:10.4028/www.scientific.net/KEM.627.77**. McManus T.N. and Haddad A.N., “Critical particulate contaminant(s) generated during arc welding on aluminum alloys,” *Environment and Natural Resources Research* **10** (2020) 43 ff., **doi:10.5539/enrr.v10n1p43**; this last is **exposure analogy, not Cu–Be DED data**. Nassar N.T. *et al.*, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, USGS OFR 2025–1047, **doi:10.3133/ofr20251047**, is **technical input, not the final list**. (kong2018insightintothe pages 1-5, liu2003thermodynamicdatabaseon pages 2-5, murray1994fracturetestingand pages 3-5, allen2000castmetalcoalition pages 9-10, berto2015hightemperaturefatigue pages 1-3, mcmanus2020criticalparticulatecontaminant(s) pages 4-6, nassar2025methodologyandtechnical pages 1-4, staff2022usgsminingreview pages 6-9)

VERDICT | Be | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.10 | evidence=thin

References

1. (allen2000castmetalcoalition pages 9-10): D. Allen. Cast metal coalition research and development closeout report. ArXiv, Aug 2000. URL: https://doi.org/10.2172/765235, doi:10.2172/765235. This article has 0 citations.

2. (nelson2026assessmentofberyllium pages 3-4): Malachi Nelson, Samuel Bays, and Chandrakanth Bolisetti. Assessment of beryllium use in nuclear power generation. Communications Materials, Sep 2026. URL: https://doi.org/10.1038/s43246-026-01295-7, doi:10.1038/s43246-026-01295-7. This article has 0 citations and is from a peer-reviewed journal.

3. (mcmanus2020criticalparticulatecontaminant(s) pages 4-6): Thomas Neil McManus and Assed N. Haddad. Critical particulate contaminant(s) generated during arc welding on aluminum alloys. Environment and Natural Resources Research, 10:43, Jan 2020. URL: https://doi.org/10.5539/enrr.v10n1p43, doi:10.5539/enrr.v10n1p43. This article has 0 citations.

4. (murray1994fracturetestingand pages 5-7): HA Murray, IJ Zatz, and JO Ratka. Fracture testing and performance of beryllium copper alloy c 17510. ArXiv, pages 109-133, Jan 1994. URL: https://doi.org/10.1520/stp18122s, doi:10.1520/stp18122s. This article has 9 citations.

5. (murray1994fracturetestingand pages 3-5): HA Murray, IJ Zatz, and JO Ratka. Fracture testing and performance of beryllium copper alloy c 17510. ArXiv, pages 109-133, Jan 1994. URL: https://doi.org/10.1520/stp18122s, doi:10.1520/stp18122s. This article has 9 citations.

6. (kong2018insightintothe pages 8-12): Decheng Kong, Chaofang Dong, Xiaoqing Ni, Cheng Man, Kui Xiao, and Xiaogang Li. Insight into the mechanism of alloying elements (sn, be) effect on copper corrosion during long-term degradation in harsh marine environment. Applied Surface Science, 455:543-553, Oct 2018. URL: https://doi.org/10.1016/j.apsusc.2018.06.029, doi:10.1016/j.apsusc.2018.06.029. This article has 83 citations and is from a domain leading peer-reviewed journal.

7. (berto2015hightemperaturefatigue pages 1-3): Filippo Berto, P. Gallo, and P. Lazzarin. High temperature fatigue tests of a cu-be alloy and synthesis in terms of linear elastic strain energy density. Sep 2015. URL: https://doi.org/10.4028/www.scientific.net/kem.627.77, doi:10.4028/www.scientific.net/kem.627.77. This article has 23 citations and is from a peer-reviewed journal.

8. (coppers1999copperdevelopmentassociation pages 64-65): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

9. (liu2003thermodynamicdatabaseon pages 2-5): X. J. Liu, I. Ohnuma, C. P. Wang, M. Jiang, R. Kainuma, K. Ishida, M. Ode, Toshiyuki Koyama, H. Onodera, and Toshio Suzuki. Thermodynamic database on microsolders and copper-based alloy systems. Journal of Electronic Materials, 32:1265-1272, Nov 2003. URL: https://doi.org/10.1007/s11664-003-0021-6, doi:10.1007/s11664-003-0021-6. This article has 58 citations and is from a peer-reviewed journal.

10. (kong2018insightintothe pages 1-5): Decheng Kong, Chaofang Dong, Xiaoqing Ni, Cheng Man, Kui Xiao, and Xiaogang Li. Insight into the mechanism of alloying elements (sn, be) effect on copper corrosion during long-term degradation in harsh marine environment. Applied Surface Science, 455:543-553, Oct 2018. URL: https://doi.org/10.1016/j.apsusc.2018.06.029, doi:10.1016/j.apsusc.2018.06.029. This article has 83 citations and is from a domain leading peer-reviewed journal.

11. (kong2018insightintothe pages 5-8): Decheng Kong, Chaofang Dong, Xiaoqing Ni, Cheng Man, Kui Xiao, and Xiaogang Li. Insight into the mechanism of alloying elements (sn, be) effect on copper corrosion during long-term degradation in harsh marine environment. Applied Surface Science, 455:543-553, Oct 2018. URL: https://doi.org/10.1016/j.apsusc.2018.06.029, doi:10.1016/j.apsusc.2018.06.029. This article has 83 citations and is from a domain leading peer-reviewed journal.

12. (kong2018insightintothe pages 12-15): Decheng Kong, Chaofang Dong, Xiaoqing Ni, Cheng Man, Kui Xiao, and Xiaogang Li. Insight into the mechanism of alloying elements (sn, be) effect on copper corrosion during long-term degradation in harsh marine environment. Applied Surface Science, 455:543-553, Oct 2018. URL: https://doi.org/10.1016/j.apsusc.2018.06.029, doi:10.1016/j.apsusc.2018.06.029. This article has 83 citations and is from a domain leading peer-reviewed journal.

13. (kong2018insightintothe pages 19-23): Decheng Kong, Chaofang Dong, Xiaoqing Ni, Cheng Man, Kui Xiao, and Xiaogang Li. Insight into the mechanism of alloying elements (sn, be) effect on copper corrosion during long-term degradation in harsh marine environment. Applied Surface Science, 455:543-553, Oct 2018. URL: https://doi.org/10.1016/j.apsusc.2018.06.029, doi:10.1016/j.apsusc.2018.06.029. This article has 83 citations and is from a domain leading peer-reviewed journal.

14. (kong2018insightintothe pages 28-32): Decheng Kong, Chaofang Dong, Xiaoqing Ni, Cheng Man, Kui Xiao, and Xiaogang Li. Insight into the mechanism of alloying elements (sn, be) effect on copper corrosion during long-term degradation in harsh marine environment. Applied Surface Science, 455:543-553, Oct 2018. URL: https://doi.org/10.1016/j.apsusc.2018.06.029, doi:10.1016/j.apsusc.2018.06.029. This article has 83 citations and is from a domain leading peer-reviewed journal.

15. (banning1973corrosionresistanceof pages 16-19): LH Banning and LL Oden. Corrosion resistance of metals in hot brines: a literature review. Unknown journal, 1973.

16. (jr1968technologyandusesa pages 14-19): KA Gschneidner Jr. Technology and uses of beryllium, cesium, germanium, hafnium, niobium (columbium), rare earths (including yttrium and …. Unknown journal, 1968.

17. (liu2003thermodynamicdatabaseon pages 1-2): X. J. Liu, I. Ohnuma, C. P. Wang, M. Jiang, R. Kainuma, K. Ishida, M. Ode, Toshiyuki Koyama, H. Onodera, and Toshio Suzuki. Thermodynamic database on microsolders and copper-based alloy systems. Journal of Electronic Materials, 32:1265-1272, Nov 2003. URL: https://doi.org/10.1007/s11664-003-0021-6, doi:10.1007/s11664-003-0021-6. This article has 58 citations and is from a peer-reviewed journal.

18. (liu2003thermodynamicdatabaseon media 751da32c): X. J. Liu, I. Ohnuma, C. P. Wang, M. Jiang, R. Kainuma, K. Ishida, M. Ode, Toshiyuki Koyama, H. Onodera, and Toshio Suzuki. Thermodynamic database on microsolders and copper-based alloy systems. Journal of Electronic Materials, 32:1265-1272, Nov 2003. URL: https://doi.org/10.1007/s11664-003-0021-6, doi:10.1007/s11664-003-0021-6. This article has 58 citations and is from a peer-reviewed journal.

19. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

20. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
