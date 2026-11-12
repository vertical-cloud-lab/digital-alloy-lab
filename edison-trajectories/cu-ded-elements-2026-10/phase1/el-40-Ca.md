<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 208a52b1-baaf-4053-a8d5-c829f64e31a6
- Submitted: 2026-10-17T19:01:12Z
- Fetched: 2026-10-17T19:25:40Z (status: success)
- Raw trajectory JSON: ../raw/el-40-Ca.json.gz
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

ELEMENT UNDER REVIEW: Ca (deoxidizer). Calcium (and CaB6) as deoxidizer and desulfurizer in copper; any use in Cu-Ni or bronzes.

Answer for Ca specifically, not for copper alloys in general:
1. ROLE: what Ca does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ca ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ca changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ca, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ca, Cu-Ni-Ca and Cu-Al-Ca are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ca in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ca neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ca | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ca (deoxidizer). Calcium (and CaB6) as deoxidizer and desulfurizer in copper; any use in Cu-Ni or bronzes.

Answer for Ca specifically, not for copper alloys in general:
1. ROLE: what Ca does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ca ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ca changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ca, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ca, Cu-Ni-Ca and Cu-Al-Ca are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ca in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ca neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ca | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Calcium for pre-alloyed marine-copper DED powder

**Decision — EXCLUDE Ca as a designed addition from both the Cu–Ni and aluminum-bronze composition searches.** Calcium is a plausible *melt-treatment reagent*, but the retrieved copper-alloy literature does not establish a retained Ca composition that improves seawater corrosion or laser-deposit integrity. The clearest brass review proposes testing Ca as a deoxidizer; it does **not** report a Ca-treated specimen or a beneficial result. Reactivity during powder production adds a substantial, unquantified obstacle. This is a decision about the proposed *alloy palette*, not a claim that trace Ca is intrinsically unacceptable. [CITE] [GAP] (davies1993anoteona pages 6-8, talanov2014behaviorofgas pages 1-2)

The distinction between alloyed Ca, calcium in seawater, and calcium-rich corrosion deposits is pivotal:

| Question | Actually supported finding | Interpretation for proposed Ca addition |
|---|---|---|
| Is alloyed Ca demonstrated to improve marine copper alloys? | No controlled Ca-bearing Cu-Ni, aluminum-bronze/NAB, or copper-alloy seawater comparison was found. A brass review names Ca only as a candidate deoxidizer for future study at impurity and minor-alloying levels; it reports no Ca content or corrosion result. (davies1993anoteona pages 6-8) | No evidence-based Ca floor, optimum, upper bound, or beneficial family can be assigned. |
| Does Ca detected on corroded Cu-Ni prove bulk alloying? | No. Ca was detected on thicker or cathodic regions of a corroded C706-type component and interpreted as an environmental deposit; it was absent from thinned regions. No bulk Ca concentration was reported. (parvizi1985photoelectronandelectrochemical pages 249-254) | Seawater-derived Ca deposits must not be cited as evidence that alloyed Ca improves film chemistry or corrosion resistance. |
| What is the Ca-uncontrolled performance benchmark? | For C71500 in seawater, reported corrosion was **0.3–0.5 mil/year** in quiet water and **0.5–0.7 mil/year** at **2 ft/s (0.61 m/s)**; pitting was 1–2 mil and 1–3 mil, respectively. These are baseline C71500 data, not Ca-controlled results. (lewis1981evaluationofcoppernickel pages 43-48) | Any Ca claim must beat this baseline in a composition-controlled experiment; current literature does not show that it does. |
| What does Ca do during source-material handling? | Ca in Cu-Ca feed reacts with moisture, producing CaO, Ca(OH)2, CaCO3, and H2. Standard calcium-processing material contained 0.1–0.3 wt% O and 0.2–0.3 wt% Cl; sealed argon handling reduced contamination. (talanov2014behaviorofgas pages 1-2) | Ca addition creates oxidation, moisture, gas, and compositional-retention risks during charging and atomization; these data do not establish a tolerable Ca level in DED powder. |
| Is zirconia demonstrably inert to Ca-bearing oxide? | No. CaO and ZrO2 form CaZrO3 completely near 1,200 °C in a ceramic synthesis study. This is not a molten-Cu crucible test. (jahn2020calciumzirconatematerials pages 1-6) | Zirconia compatibility with Ca-bearing copper melts cannot be assumed; dedicated crucible-coupon testing is required. |
| Can a numerical Ca impurity maximum be assigned? | No reviewed marine-alloy specification or controlled study supplied a Ca range or maximum for C71500, C70600, C95800, or the relevant AWS A5.7 fillers. | Do not invent a ppm or wt% limit. Specify Ca as **not intentionally added** and report the analytical detection limit until qualification data exist. |


*Table: Separates direct alloy evidence from environmental calcium deposits, source-material hazards, and the calcium-uncontrolled C71500 corrosion benchmark. It prevents unsupported Ca composition bounds from being inferred from unrelated observations.*

## 1. Metallurgical role and specifications

**Deoxidation is a hypothesis, not an established marine-alloy strengthening mechanism.** Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions* (Copper Development Association, 1993; no verified DOI), recommends investigating Ca alongside P, Li, Mg and rare earths to determine whether deoxidizing brass before casting inhibits dezincification. The recommendation explicitly calls for experiments at impurity and minor-alloying levels: it is **not** a reported Ca concentration, functional floor, or corrosion improvement. Its discussion of cast aluminum bronze concerns *other* additions, not a demonstrated Ca treatment. [CITE] [GAP] (davies1993anoteona pages 6-8)

A chemically plausible treatment would bind dissolved oxygen as CaO and sulfur as CaS, followed by removal of the products from the melt. That is different from retaining a beneficial concentration of Ca in the deposit; retained oxide/sulfide inclusions could instead impair consolidation. The retrieved evidence does not demonstrate Ca solid-solution strengthening, a named beneficial Ca precipitate, Ca-driven grain refinement, inhibition of NAB selective attack, or a Ca-derived protective seawater film. Nor does it establish that CaB₆ supplies a reproducible retained Ca addition, rather than a separate boron-bearing particulate/treatment. [GAP] (davies1993anoteona pages 6-8, talanov2014behaviorofgas pages 1-2)

**[SPEC] Verified Ca-bearing commercial or Navy grades and Ca ranges: none identified.** The retrieved materials do not establish a specified Ca interval for C70600 or C71500 Cu–Ni, C95800 NAB, Mn–Al bronze, tin bronze/gunmetal, marine brass, Cu–Ni–Sn, or Cu–Ni–Si. They likewise do not furnish a Ca limit in the cited ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, EN 12449, or AWS A5.7 documents. Consequently, **“Ca not listed as an intentional alloying element” must not be converted into a numerical [SPEC] maximum or a claim that a grade contains exactly 0 wt% Ca.** No Ca-containing Navy qualification was verified. [GAP] (davies1993anoteona pages 6-8, lewis1981evaluationofcoppernickel pages 43-48)

## 2. Seawater corrosion: what can actually be quantified

**[NUMBERS] Ca effect: no established beneficial or harmful wt% interval.** No controlled comparison of measured *bulk-alloy* Ca additions was located for corrosion rate, E_corr, polarization or film resistance, pitting, crevices, dezincification/selective attack, erosion-corrosion, or limiting seawater velocity in the specified copper families. Ca detected in a corroded C706-type fish-cage component occurred on thicker regions, but not thinned regions; its investigators discussed deposition on cathodic regions. It is **not** evidence that the manufactured alloy contained Ca or that alloyed Ca formed the protective film. Davies likewise gives no Ca-specific dezincification measurement. [CITE] [GAP] (parvizi1985photoelectronandelectrochemical pages 249-254, davies1993anoteona pages 6-8)

**[NUMBERS] Benchmark, *not* a Ca response:** Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, Argonne report ANL/OTEC-BCM-019 (1981), DOI **10.2172/6255887**, report C71500 corrosion of **0.3–0.5 mil/year** in quiet seawater and **0.5–0.7 mil/year** at **2 ft/s (0.61 m/s)**, with respective reported pitting ranges of **1–2 mil** and **1–3 mil**. These historical bulk-alloy exposures do not control Ca content, do not describe an as-deposited DED surface, and cannot establish compliance with the proposed 30-day depth-of-attack criterion. Their report also identifies excellent C70600 resistance up to approximately **3.0 m/s**; this is a C70600 reference, **not a Ca-derived velocity limit**. [CITE] (lewis1981evaluationofcoppernickel pages 43-48)

## 3. DED, welding, repair and powder production

**[GAP] Ca-specific DED and welding outcomes are unmeasured.** No retrieved Ca-controlled experiment measures solidification cracking, reheated-layer liquation cracking, porosity, laser evaporation/oxidation loss, or cracking and corrosion after dilution into cast C95800 or wrought Cu–Ni. ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl are useful *Ca-uncontrolled welding comparators*, not evidence that Ca prevents cracking or survives a 1.07-µm laser. In particular, cleaner melt chemistry from a deoxidizer cannot by itself prove fewer DED pores: oxide inclusions, moisture-derived gas and Ca loss may counteract it. Ca retention should be assayed separately in charge, atomized powder and each deposit, including the NAB and Cu–Ni interfaces. These are process-risk hypotheses, not reported Ca–DED findings. [GAP] (davies1993anoteona pages 6-8, talanov2014behaviorofgas pages 1-2)

**[CITE] [NUMBERS] Feedstock-handling evidence:** Talanov and Kotsar, *Behavior of Gas Impurities at Manufacturing of High-Purity Calcium* (2014; no verified DOI), specifically discuss calcium **in a Cu–Ca production alloy** reacting with moist air: Ca forms CaO and H₂; CaO hydrates to Ca(OH)₂; subsequent reaction produces CaCO₃. They describe sealed argon handling. Calcium product made by their conventional route contained **0.1–0.3 wt% oxygen** and **0.2–0.3 wt% chlorine**. These are *source-material* values, **not permissible oxygen or chlorine limits for the proposed copper powder**. Verify the purity and storage history of any Ca-bearing charge or master alloy before interpreting atomization yields. [CITE] (talanov2014behaviorofgas pages 1-2)

**Crucible/sonotrode compatibility is unresolved for this melt.** Jahn, *Calcium Zirconate Materials for Refractory Applications* (2020 dissertation; no verified DOI), reports complete formation of CaZrO₃ from CaO plus ZrO₂ at approximately **1,200 °C** in ceramic synthesis. Thus zirconia cannot simply be assumed inert toward *Ca-bearing oxide* at the stated atomization temperatures; this is **not** proof that a dilute Ca-bearing liquid Cu alloy attacks a zirconia crucible at that rate. Corresponding Ca–Cu melt tests against alumina, zirconia, graphite, titanium-alloy and molybdenum sonotrodes, and measurements of surface tension, Ca evaporation, and droplet chemistry, were not found. Graphite also introduces a potential carbide/contamination question, not a documented performance result for this atomizer. [CITE] [NUMBERS] [GAP] (jahn2020calciumzirconatematerials pages 1-6, talanov2014behaviorofgas pages 1-2)

## 4. Phase equilibria and computational feasibility

**[GAP] No defendable numerical Cu–Ca solvus or liquidus limit was recovered.** The requested maximum Ca solubility in Cu, its temperature, a verified list of Cu–Ca intermetallics/invariant reactions, and liquidus shifts for the intended Cu–Ni–Al–Ca compositions could not be extracted from an accessible assessed *metallic* Cu–Ca phase diagram. They therefore cannot justify either an aggressive Ca ceiling or a claim that adding Ca does—or does not—take a particular alloy above **1,200–1,250 °C**. An indexed publication by Risold, Hallstedt and Gauckler, “Thermodynamic Assessment of the Ca–Cu–O System,” *Journal of the American Ceramic Society* **78** (1995), 2655–2661, DOI **10.1111/j.1151-2916.1995.tb08036.x**, establishes the existence of an assessment bearing on **oxygen-containing equilibria**; it is not a verified, deployable Cu–Ni–Ca or Cu–Al–Ca powder-design TDB. Its full model parameters were not accessible in this search. [CITE] [GAP] (jahn2020calciumzirconatematerials pages 1-6, talanov2014behaviorofgas pages 1-2)

**[GAP] TCCU/COST 531 coverage was not verified.** Do not equate an element appearing in a database selector with assessed Cu–Ca, Cu–Ni–Ca and Cu–Al–Ca interactions. Before a pycalphad/Thermo-Calc Ca calculation is used to set a limit, inspect the licensed TCCU constituent list and assessed-system documentation, available phase parameters and ternary interactions, then compare measured powder/deposit compositions with calculation. No Ca-specific prediction meeting those checks is available here. [GAP]

## 5. Supply, regulation and interactions

**[CITE] [NAVY] Criticality:** Ca is **not** a highlighted critical *element* on the USGS visualization of the **final 2025** list; Ni and Cu are highlighted. The source distinguishes listed *potash* and *phosphate rock* commodities from elemental potassium and calcium. The 2022 final-list citation is Federal Register **87 FR 10381–10382**; the 2025 final-list citation is **90 FR 50494–50497**. The retrieved 2022-list text did not independently verify Ca's entry, so it is not asserted here. Olinger, USGS *Critical Minerals Memory Match Game* (2026), DOI **10.3133/gip266**, provides the visually checked 2025 identification. [CITE] [NAVY] (rupkeUnknownyearutahmining2025 pages 31-31, olinger2026criticalmineralsmemory pages 1-2, olinger2026criticalmineralsmemory media fe2a3453)

**[GAP] Cost/regulatory limits:** A reproducible USD/kg quote specifying Ca metal purity, form, quantity and date was not recovered; no numerical price is warranted. No Ca-specific OSHA permissible exposure limit, Ca-specific RoHS/REACH prohibition, or Navy restriction applicable to these copper alloys was established by the retrieved sources. That does **not** waive general combustible/reactive-powder, workplace-dust or laser-fume controls. Ca-bearing feed exposed to moisture can evolve H₂; treat any proposed fine Ca-bearing powder or condensate as requiring a site-specific fire/air-exposure assessment and measured airborne contaminants. [GAP] (talanov2014behaviorofgas pages 1-2)

**Joint-constraint flags, not fitted ratios:** oxygen and sulfur consume available Ca through proposed deoxidation/desulfurization; aluminum and zirconia-bearing refractory surfaces create additional oxide-chemistry/compatibility questions. Ca interaction with Ni, Fe, Mn, Al, P, B and Si, including any change in NAB κ-phase constitution or Cu–Ni protective-film chemistry, is not quantified for these alloys. No defensible Ca:O, Ca:S, Ca:Al, Ca:Ni or Ca:Fe design ratio was identified. CaB₆ must be evaluated with **both** retained Ca and added B measured; it is not evidence for a Ca-only alloy effect. [GAP] (davies1993anoteona pages 6-8, jahn2020calciumzirconatematerials pages 1-6, talanov2014behaviorofgas pages 1-2)

## 6. Bounds and evidence quality

**EXCLUDE intentional Ca for both families.** Conservative maximum **NA**; non-conservative maximum **NA**; functional floor **NA**; and specification-derived impurity maximum **NA**. No commercial/Navy Ca range or Ca-controlled experiment sets any of those numbers. The operative instruction is **no intentional Ca charge** and disclosure of measured Ca and the analytical detection limit in charge, powder and deposit—not the fictional limit “0 wt% Ca.” The decision reflects unproved seawater benefit coupled to plausible retained-inclusion, moisture, composition-loss and interface risks. Conversely, the search does **not** show a wt% at which Ca actually starts harming either family. Evidence for the Ca-specific design decision is **thin**; the historical *Ca-uncontrolled* Cu–Ni corrosion benchmark and Ca-source moisture chemistry are substantially better documented. [GAP] (davies1993anoteona pages 6-8, lewis1981evaluationofcoppernickel pages 43-48, talanov2014behaviorofgas pages 1-2)

VERDICT | Ca | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (davies1993anoteona pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

2. (talanov2014behaviorofgas pages 1-2): AA Talanov and ML Kotsar. Behavior of gas impurities at manufacturing of high-purity calcium. Unknown journal, 2014.

3. (parvizi1985photoelectronandelectrochemical pages 249-254): MS Parvizi. Photoelectron and electrochemical studies of the corrosion of a copper-nickel alloy. Unknown journal, 1985.

4. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

5. (jahn2020calciumzirconatematerials pages 1-6): C Jahn. Calcium zirconate materials for refractory applications. Unknown journal, 2020.

6. (rupkeUnknownyearutahmining2025 pages 31-31): A Rupke, SE Mills, MD Vanden Berg, and N Christensen. Utah mining 2025. Unknown journal, Unknown year.

7. (olinger2026criticalmineralsmemory pages 1-2): Danielle A. Olinger. Critical minerals memory match game. General Information Product, Jan 2026. URL: https://doi.org/10.3133/gip266, doi:10.3133/gip266. This article has 0 citations.

8. (olinger2026criticalmineralsmemory media fe2a3453): Danielle A. Olinger. Critical minerals memory match game. General Information Product, Jan 2026. URL: https://doi.org/10.3133/gip266, doi:10.3133/gip266. This article has 0 citations.
