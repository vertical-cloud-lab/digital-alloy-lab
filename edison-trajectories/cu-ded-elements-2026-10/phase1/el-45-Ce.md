<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 696ec571-e47d-4d26-afae-53b4f5da984b
- Submitted: 2026-10-17T19:01:25Z
- Fetched: 2026-10-17T19:28:15Z (status: success)
- Raw trajectory JSON: ../raw/el-45-Ce.json.gz
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

ELEMENT UNDER REVIEW: Ce (rare earth). Cerium additions to 90-10 and 70-30 Cu-Ni and to aluminum bronze (mostly cast or wrought studies, often Chinese literature): corrosion and film effects, amounts used.

Answer for Ce specifically, not for copper alloys in general:
1. ROLE: what Ce does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ce ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ce changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ce, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ce, Cu-Ni-Ce and Cu-Al-Ce are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ce in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ce neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ce | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ce (rare earth). Cerium additions to 90-10 and 70-30 Cu-Ni and to aluminum bronze (mostly cast or wrought studies, often Chinese literature): corrosion and film effects, amounts used.

Answer for Ce specifically, not for copper alloys in general:
1. ROLE: what Ce does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ce ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ce changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ce, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ce, Cu-Ni-Ce and Cu-Al-Ce are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ce in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ce neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ce | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Cerium (Ce) in copper-alloy powder for marine laser DED

**Decision: LIMIT Ce as an incidental constituent; do not yet make it a designed addition.** Ce-specific studies of 90–10 and 70–30 Cu–Ni in marine electrolytes exist, but their composition–response data could not be verified from accessible full texts. The accessible aluminum-bronze chloride experiment does not report Ce separately, and its **as-cast** experimental alloy did not outperform its comparator. No retrieved evidence establishes Ce retention through the proposed atomization/laser sequence, Ce-specific crack resistance, or corrosion parity with *wrought C71500 as deposited*. The recommendation is a qualification decision, **not** a finding that trace Ce is intrinsically harmful. (davies1993anoteon pages 5-6, li2006corrosionwearbehavior pages 1-2)

All compositions below are **wt%** unless explicitly labeled otherwise. “Charged,” “retained,” “powder,” and “deposit” concentrations are different measurements; mischmetal and unspecified rare earths are **not** interchangeable with elemental Ce.

## 1. Role, mechanisms, and specified alloys

[CITE] [NUMBERS] The strongest directly inspected copper-alloy example of Ce-containing melt treatment is **deoxidation with substantial loss of the addition**: a charge of **0.5 wt% mischmetal** to brass left approximately **0.04 wt% *total* rare-earth elements** after melting/pouring. That is approximately **8% recovery of the charged mixture**, not a measurement of Ce recovery. In the same review, separate **0.05 wt% Ce, La, or Nd** additions improved aluminum-bronze general corrosion in *dilute sulfuric acid*; this is neither seawater evidence nor proof of a protective Ce-bearing seawater film. Davies explicitly questions whether reported benefits reflect oxygen removal rather than a persistent dissolved rare-earth effect. (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8)

[CITE] [GAP] Ce should be treated primarily as a **reactive oxygen getter and possible solidification/microstructure modifier**, rather than an established substitutional corrosion-strengthening solute. Cu–Ce compounds **CeCu4 and CeCu5** appear in a published thermodynamic description; in Al–Ce–Cu, **Al8CeCu4** and Al–Ce compounds provide additional possible sinks. Their identification in an assessment **does not demonstrate** that these phases form in a dilute, rapidly solidified Cu–Ni or NAB deposit. No inspected Cu–Ni/NAB study conclusively identifies a retained Ce concentration, its precipitate, or CeO2/Ce(OH)3 within an *as-deposited* seawater film. In particular, mechanisms established for **cerium-salt inhibitors or applied ceria coatings** cannot be assigned to internally alloyed Ce. (moore2020thermodynamicmodelingof pages 1-4, belov2007theternaryal–ce–cu pages 1-2, moore2020thermodynamicmodelingof pages 7-8, moore2020thermodynamicmodelingof media 85112374)

[SPEC] [NAVY] **No intentional Ce range was verified** for C71500/C70600 Cu–Ni, C95800 nickel–aluminum bronze (NAB), or for the cited marine-alloy product/filler specifications **ASTM B111/B171/B466/B148/B369; MIL-T-16420, MIL-B-24480, MIL-C-15726; AWS A5.7; EN 12449**. This means **“Ce not specified,” not “Ce prohibited” or “Ce ≤0.”** Do not mislabel an unspecified *other-elements* allowance as a Ce-specific qualification. The published Ce-free AM comparison includes AWS A5.7 ERCuNiAl and C95800-type compositions around **Cu–9Al–4Ni–4Fe–1Mn**; it supplies no Ce precedent for ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl. No verified Navy/DoD specification mandating Ce, Ce content for a Navy gunmetal/tin bronze, or Ce range in commercial Mn–Al bronze, brass, Cu–Ni–Sn, or Cu–Ni–Si was found. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 60-62)

## 2. Seawater corrosion: measured results versus Ce attribution

The following comparison prevents combined-alloy results from being incorrectly presented as Ce dose–response data. (davies1993anoteon pages 5-6, li2006corrosionwearbehavior pages 1-2)

| Alloy family / evidence class | Verified composition and response | Inference allowed | Evidence gap |
|---|---|---|---|
| Cu–Ni: Ce-specific studies | Mao et al. studied rare-earth effects in Cu–30Ni in simulated seawater (DOI: 10.1016/S1002-0721(08)60384-1); Du et al. compared La and Ce in B10 (nominal 90–10 Cu–Ni) (DOI: 10.1016/j.jmrt.2025.05.090). Only bibliographic records were accessible; Ce contents and quantitative corrosion results were not verified. | Direct Ce-specific Cu–Ni literature exists, so Ce merits controlled screening rather than categorical exclusion. | No accessible, verified Ce floor, optimum, harmful threshold, corrosion-rate reduction, film resistance, pitting potential, selective-attack depth, or retained Ce value; neither paper establishes a proposal bound from the evidence inspected. |
| Aluminum bronze: Li et al. (2006) | Experimental Cu–14Al–X contained Cu balance, 14–16 wt% Al, 2.0–4.0 wt% Fe, 0.8–1.0 wt% Mn, 0.4–0.8 wt% Ni, 0.5–1.2 wt% Co, and **0.6–1.6 wt% pooled “traces”**; Ce was not reported separately. In 3.5 wt% NaCl at 18 °C, corrosion rates were 0.0264 g·m⁻²·h⁻¹ as cast, 0.0258 g·m⁻²·h⁻¹ after heat treatment, and 0.0260 g·m⁻²·h⁻¹ for commercial QAl9-4. The as-cast experimental alloy therefore did not outperform the comparator (li2006corrosionwearbehavior pages 1-2). DOI: 10.1361/105994906X83466. | The multicomponent alloy demonstrates manufacturability and near-comparator chloride performance, but only as a combined-composition result. | No Ce-specific wt%, control alloy, as-deposited AM condition, or separable Ce effect; the pooled 0.6–1.6 wt% trace range cannot serve as a Ce bound. Its small advantage appeared only after post-cast heat treatment, which is outside the proposal target. |
| Aluminum bronze: Davies review of older experiments | Davies reports that 0.05 wt% Ce, La, or Nd separately improved general corrosion of aluminum bronze in **dilute sulfuric acid**, not seawater or NaCl (davies1993anoteon pages 5-6). | The 0.05 wt% result is a plausible experimental screening level and evidence of a microalloying-scale effect. | Acid performance cannot establish seawater film chemistry, pitting, dealuminification, erosion–corrosion, or a marine-alloy upper bound; original experimental numerical rates were not available in the inspected review. |
| Brass: mischmetal and dezincification | A 0.5 wt% mischmetal charge to 63.5Cu–2.5Pb–Zn retained only about 0.04 wt% **total mixed rare-earth elements**, attributed to oxidation during melting and pouring. Hot-worked material remained highly susceptible to dezincification, whereas annealed material performed better. In arsenical 60–40 brass, 0.1 wt% mischmetal charge reportedly gave the best result; in ordinary duplex brass, rare earths could marginally increase attack (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8). | Ce-containing additions can be strongly consumed as oxide, and alloy condition, oxygen, and arsenic govern whether the residual rare earth appears beneficial. This is directly relevant to charge-to-powder recovery planning. | Mischmetal is not pure Ce; 0.04 wt% total retained rare earth is neither a Ce concentration nor a Ce specification. These data do not define a Ce limit for Cu–Ni or aluminum bronze and are not DED results. |
| Ce-specific laser DED, welding, and dilution | No verified study was found for elemental Ce additions in laser DED of Cu–Ni or NAB, nor in ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl filler metals. Published AM baselines reviewed use Ce-free compositions such as ERCuNiAl/C95800-type Cu–9Al–4Ni–4Fe–1Mn (nemani2024advancementsinadditive pages 60-62). | None regarding Ce effects on solidification cracking, reheated-layer liquation, porosity, dilution, laser oxidation, or evaporation; these must be treated as research hypotheses. | No Ce-specific crack-susceptibility curve, recovery factor, powder-to-deposit mass balance, substrate-dilution tolerance, or demonstrated as-deposited marine-corrosion benefit. |
| Commercial and Navy specifications | No Ce range was identified in ASTM B111, B171, B466, B148, or B369; MIL-T-16420, MIL-B-24480, or MIL-C-15726; AWS A5.7 marine-copper fillers; EN 12449; or the relevant UNS/CDA Cu–Ni and NAB compositions examined. | Commercial/Navy precedent does not support calling Ce an established specified constituent. | No specification-derived conservative maximum or impurity maximum exists in the sources inspected; assigning one would manufacture a limit rather than derive it from a standard. |


*Table: Separates verified Ce-alloying evidence from multielement and mischmetal results that cannot define a Ce bound. It highlights that direct quantitative Cu–Ni, DED, and Navy-specification support remains unavailable.*

[NUMBERS] [CITE] In **3.5 wt% NaCl at 18 °C**, Li *et al.* measured **0.0264 g m⁻² h⁻¹** for **as-cast** Cu–14Al–X, **0.0258 g m⁻² h⁻¹** after solution treatment/aging, and **0.0260 g m⁻² h⁻¹** for QAl9-4. Their alloy contained **0.6–1.6 wt% pooled “traces”** and several other alloying elements; its Ce content was **not** specified. The as-cast result was about **1.5% higher**, not lower, than the comparison value. The **0.8% lower** heat-treated result cannot support a no-post-build-heat-treatment target. Neither difference is a measured *Ce effect*, and this experiment does not compare against wrought C71500. (li2006corrosionwearbehavior pages 2-4, li2006corrosionwearbehavior pages 1-2)

[CITE] [GAP] Specific marine-literature leads are Mao *et al.*, “Effect of rare earths on corrosion resistance of Cu-30Ni alloys in simulated seawater,” *Journal of Rare Earths* **27**, 1037–1041 (2009), DOI **10.1016/S1002-0721(08)60384-1**; Lin *et al.*, “Influence of rare earth elements on corrosion resistance of BFe10-1-1 alloys in flowing marine water,” *Journal of Rare Earths* **27**, 259–263 (2009), DOI **10.1016/S1002-0721(08)60231-8**; and Du *et al.*, “The difference in anti-corrosion effect between the addition of La and Ce of a B10 alloy,” *Journal of Materials Research and Technology* **36**, 8062–8074 (2025), DOI **10.1016/j.jmrt.2025.05.090**. Their full experimental results were **not available for verification here**. Accordingly, no numeric Ce-specific optimum, beneficial/harmful interval, corrosion-rate change, *E*₍corr₎ shift, film resistance, pit/crevice/dealloying depth, erosion–corrosion threshold, or seawater velocity limit is defensible from those citations alone. “Rare earths” in the titles must not be silently converted into pure Ce. (davies1993anoteon pages 5-6)

[CITE] [NUMBERS] Davies’ contrary brass evidence illustrates **conditional**, not universal, protection: in ordinary duplex brass, rare-earth/mischmetal additions reportedly increased dezincification slightly; in **arsenical 60–40 brass**, a **0.1 wt% mischmetal charge** gave the best result. A **0.5 wt% mischmetal charge** left **0.04 wt% total RE** in another brass, which remained susceptible when hot worked but improved after annealing. None is a Ce-only chloride corrosion curve, and arsenical-brass behavior should not be transplanted to NAB or Cu–Ni. (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8)

## 3. DED, welding, and substrate dilution

[GAP] No verified experiment isolates elemental Ce in **single-stream, blown-powder laser DED** of Cu–Ni or NAB, nor in a Ce-controlled ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl welding series. Thus neither **solidification-crack suppression** nor **reheated-layer liquation-crack resistance** can be claimed. Plausible *risks to test* are interdendritic Ce-containing constituents/liquid films, Ce oxide particles or entrained gas creating pores, and repeated remelting of a segregated interface. These are mechanisms to falsify by microscopy and crack testing, **not reported Ce-specific outcomes**. Existing Ce-free NAB AM work establishes only that changing thermal history changes the α/β′/κ-phase balance; it cannot validate Ce. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 60-62, moore2020thermodynamicmodelingof pages 1-4)

[GAP] The first layers on cast **C95800** can receive Al/Fe/Ni/Mn and existing κ-bearing microstructure; layers on wrought Cu–Ni instead dilute the same feedstock toward Cu–Ni. Either changes the amount of Ce available to oxidize or form compounds, so a nominal single-stream powder composition is **not** the interfacial composition. Establish Ce in **charge → powder → single bead → upper layer → fusion boundary**, and assess each substrate plus self-build for cracks, porosity, corrosion and selective-attack depth. There is no evidence-derived safe Ce dilution percentage, evaporation fraction, or laser-specific retention factor. Welding/thermal-spray results are **indirect**, not substitutes for these experiments. (davies1993anoteon pages 5-6, nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 60-62)

## 4. Induction melting and ultrasonic powder atomization

[NUMBERS] [CITE] The **0.5 wt% charged → 0.04 wt% retained total RE** brass observation is a warning that nominal Ce charge is an unreliable powder specification. Oxidation and dross entrainment are credible leading risks despite argon protection. A Cu–Al–Fe bronze casting study used Al pre-deoxidation, covered its melt, degassed it, and applied rare-earth deoxygenation just before pouring; this is **casting**, not a demonstrated rePOWDER protocol. Qualify actual oxygen pickup, Ce recovery and inclusion populations at the relevant residence times. (li2006corrosionwearbehavior pages 2-4, davies1993anoteon pages 5-6)

[GAP] Direct compatibility data for **Ce-bearing Cu alloy at the proposed temperatures** against **Al2O3, ZrO2, graphite, a Ti-alloy sonotrode, or a Mo sonotrode** were not verified. Treat ceramic reduction/contamination, graphite carbon pickup, adherent Ce-rich oxide, and sonotrode erosion/reaction as coupon-test questions rather than established rates or ranking of crucibles. Likewise, Ce-dependent atomization yield, droplet surface tension, powder flow, laser-vapor loss and fume composition have **not** been quantified. A report that TCCU can calculate liquid surface tension is not a measurement or validation for this Ce-containing melt. (davies1993anoteon pages 5-6, janssonUnknownyearphasetransformationsand pages 28-30)

## 5. Phase diagram, liquidus and CALPHAD

[CITE] [NUMBERS] **Ce is present as an element in Thermo-Calc TCCU5**: its published description lists **32 elements**, **148 assessed binary** and **64 assessed ternary** systems. But elemental inclusion **does not establish which Ce-containing binary/ternary has been independently assessed or its quality**; confirm the installed TCCU version and each Cu–Ce, Cu–Ni–Ce and Cu–Al–Ce subsystem before interpreting a Scheil run. A separate published CALPHAD construction explicitly incorporates **Ce–Cu and Al–Ce–Cu** descriptions: Moore *et al.*, *Journal of Phase Equilibria and Diffusion* **41**, 764–783 (2020), DOI **10.1007/s11669-020-00852-y**. Its cited Cu–Ce source is Zhuang, Qiao and Wei, “Thermodynamic Evaluation of the Cu-R (R: Ce, Pr, Nd, Sm) Binary Systems,” *Journal of Phase Equilibria* **17**, 508–521 (1996); Bo *et al.* assess Al–Ce–Cu in *Journal of Alloys and Compounds* **484**, 286–295 (2009), DOI **10.1016/j.jallcom.2009.04.083**. **No Cu–Ni–Ce ternary assessment or COST 531 Ce subsystem was independently verified.** (moore2020thermodynamicmodelingof pages 1-4, moore2020thermodynamicmodelingof pages 4-5, moore2020thermodynamicmodelingof pages 20-20, janssonUnknownyearphasetransformationsand pages 28-30)

[CITE] [NUMBERS] Published thermodynamic entries include **CeCu4/CeCu5**; experimental **Al-rich** Al–Ce–Cu work identified **Al4Ce (Al11Ce3), Al8CeCu4 and Al2Cu**, and placed **L → (Al) + Al8CeCu4 at 610 °C**, approximately **14 wt% Cu and 7 wt% Ce**. That study covers at most **35 wt% Cu**: its eutectic is **not** the Cu-rich alloy’s liquidus or invariant. Belov and Khvan, *Acta Materialia* **55**, 5473–5482 (2007), DOI **10.1016/j.actamat.2007.06.009**. The retrieved material did **not** establish a trustworthy numerical **maximum solid solubility of Ce in Cu (wt% and temperature)**, Cu-rich invariant temperatures/compositions, or a validated Ce-induced liquidus slope; these requested numbers must remain **unreported**, not be inferred from the Al-rich diagram. (belov2007theternaryal–ce–cu pages 1-2, moore2020thermodynamicmodelingof pages 7-8, moore2020thermodynamicmodelingof media 85112374)

[GAP] **No evidence supports asserting that a trace Ce addition alone raises a Cu-rich alloy’s liquidus above 1,250 °C.** Conversely, the installed database must calculate *each complete* Cu–Ni–Al–Fe–Mn–Ce formulation; Ni/Fe-rich high-liquidus compositions may fail the **1,200–1,250 °C useful-superheat screen** regardless of a small Ce dose. Require a database-coverage check, measured DSC liquidus and actual melt-superheat margin before a powder trial. (moore2020thermodynamicmodelingof pages 1-4, janssonUnknownyearphasetransformationsand pages 28-30)

## 6. Supply, cost and safety

[CITE] [NAVY] **Ce appears by name on the 2022 U.S. final critical-minerals list**, as does Ni; Cu was not on that listed set. The 2025 USGS *methodology/technical-input* report recommends **adding Cu** to an updated list; that recommendation is **not itself** the final rule. Cerium remains a named commodity in the 2025 risk assessment. Sources: *2022 Final List of Critical Minerals*, **87 Fed. Reg. 10381** (24 February 2022; no DOI), and Nassar *et al.*, USGS Open-File Report **2025–1047** (2025), DOI **10.3133/ofr20251047**. No independently inspected text of the **2025 final Federal Register list** was available here, so its precise legal entries should be checked directly rather than deduced solely from the technical report. (nassar2025methodologyandtechnical pages 1-4, janssonUnknownyearphasetransformationsand pages 28-30, jenkins2023outliningpotentialbiomarkers pages 1-2, nassar2025methodologyandtechnical pages 33-35)

[GAP] A documented **current price for *Ce metal*, in USD/kg**, was not obtained; no defensible metal-versus-oxide or bulk-versus-small-lot conversion can be made. Obtain dated supplier quotes for metal/master alloy of stated purity and compare **cost per kg of Ce actually retained**, not per kg charged. No Ce-specific OSHA permissible exposure limit, blanket RoHS/REACH prohibition, or Navy ban was verified; **absence of a verified Ce-specific limit does not remove general respirable-dust, combustible-metal-powder, laser-fume, ventilation, waste and exposure-control obligations**. A USGS toxicology review reports limited REE health data and cellular uptake of CeO2 nanoparticles, which warrants fume/powder containment but is **not** an exposure limit for Ce-bearing Cu powder. Jenkins *et al.*, *Toxics* **11**, 188 (2023), DOI **10.3390/toxics11020188**. (jenkins2023outliningpotentialbiomarkers pages 14-15, jenkins2023outliningpotentialbiomarkers pages 1-2)

## 7. Bounds and failure modes

**LIMIT, both Cu–Ni and aluminum-bronze candidate families.** Use **Ce ≤0.04 wt% (≤400 ppm) measured individually in both powder and deposit** as a **provisional internal screening ceiling**, *not* as a published safety threshold, commercial specification, or evidence of corrosion neutrality. The only numerical processing anchor is Davies’ **0.04 wt% retained *total mixed rare earth*** after a much larger mischmetal charge: the ceiling deliberately keeps unplanned Ce from exceeding that observed *total*, but that cross-alloy extrapolation is weak and should be revisited after controlled trials. Reject the stronger claim that Davies established “0.04 wt% allowable Ce” in Cu–Ni or NAB. Specify analytical detection/reporting for Ce, La and other RE separately, powder oxygen and inclusion counts; do **not** increase the Ce charge merely to compensate for presumed oxidation. **No established Navy/commercial conservative maximum, Ce-specific functional floor, beneficial/harmful threshold or defensible aggressive upper bound was verified.** If an impurity ceiling must be strictly derived from a Cu–Ni/NAB **specification or direct study**, rather than selected as a project-control criterion, the correct answer is **not established**; 400 ppm is expressly a *proposed* acceptance criterion. Failure modes that motivate limiting Ce are **uncertain recovery/oxide inclusions** and **unqualified interfacial segregation/porosity/cracking and localized corrosion**, not a measured failure at 400 ppm. (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8, li2006corrosionwearbehavior pages 1-2)

## 8–9. Interactions and evidence quality

[CITE] [GAP] For joint constraints, track **Ce retained versus oxygen available**, rather than total charged Ce alone; distinguish elemental Ce from mischmetal’s **Ce + La + Pr + Nd**. Track **Ce with Al** for potential Al–Ce–Cu compounds, and separately **Al–Ni–Fe–Mn** for NAB κ/β′ phase balance; **Ni–Fe–Mn–Ce** interactions in marine Cu–Ni remain unquantified. Brass reports show an **As × rare-earth × microstructure** interaction: the sign of the dezincification response changes between ordinary and arsenical duplex brass. Other potentially consumptive partners, including S, P and Si, require assay and phase identification; stoichiometric Ce/O or Ce/S design ratios are **not validated** for these deposits. (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8, nemani2024advancementsinadditive pages 62-68, moore2020thermodynamicmodelingof pages 1-4, belov2007theternaryal–ce–cu pages 1-2)

**Overall evidence: thin for this specific proposal**, despite credible Ce-containing copper-alloy research. Available quantitative chloride data confound Ce with several other elements; the brass melt-loss data concern a *mixture*; the phase-diagram experiment is *Al-rich*; and the retrieved AM literature is *Ce-free*. Priority falsification tests are composition/oxygen mass balance; Ce-rich inclusions and interfacial phases; self-build and two-substrate crack/porosity comparisons; and **as-deposited** seawater electrochemistry followed by 30-day maximum selective-attack depth against wrought C71500. Neither a short electrochemical improvement nor a post-heat-treated casting result by itself demonstrates that target. (davies1993anoteon pages 5-6, nemani2024advancementsinadditive pages 62-68, li2006corrosionwearbehavior pages 1-2, belov2007theternaryal–ce–cu pages 1-2)

VERDICT | Ce | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.04 | evidence=thin

References

1. (davies1993anoteon pages 5-6): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

2. (li2006corrosionwearbehavior pages 1-2): W.S. Li, Z.P. Wang, Y. Lu, and L.H. Yuan. Corrosion wear behavior of al-bronzes in 3.5% nacl solution. Journal of Materials Engineering and Performance, 15:102-110, Feb 2006. URL: https://doi.org/10.1361/105994906x83466, doi:10.1361/105994906x83466. This article has 19 citations and is from a peer-reviewed journal.

3. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

4. (moore2020thermodynamicmodelingof pages 1-4): Emily E. Moore, P. Turchi, Vincenzo Lordi, D. Weiss, Zachary C. Sims, H. Henderson, M. Kesler, Orlando Rios, Scott K. McCall, and A. Perron. Thermodynamic modeling of the al-ce-cu-mg-si system and its application to aluminum-cerium alloy design. Journal of Phase Equilibria and Diffusion, 41:764-783, Nov 2020. URL: https://doi.org/10.1007/s11669-020-00852-y, doi:10.1007/s11669-020-00852-y. This article has 31 citations and is from a peer-reviewed journal.

5. (belov2007theternaryal–ce–cu pages 1-2): N.A. Belov and A.V. Khvan. The ternary al–ce–cu phase diagram in the aluminum-rich corner. Acta Materialia, 55:5473-5482, Sep 2007. URL: https://doi.org/10.1016/j.actamat.2007.06.009, doi:10.1016/j.actamat.2007.06.009. This article has 137 citations and is from a highest quality peer-reviewed journal.

6. (moore2020thermodynamicmodelingof pages 7-8): Emily E. Moore, P. Turchi, Vincenzo Lordi, D. Weiss, Zachary C. Sims, H. Henderson, M. Kesler, Orlando Rios, Scott K. McCall, and A. Perron. Thermodynamic modeling of the al-ce-cu-mg-si system and its application to aluminum-cerium alloy design. Journal of Phase Equilibria and Diffusion, 41:764-783, Nov 2020. URL: https://doi.org/10.1007/s11669-020-00852-y, doi:10.1007/s11669-020-00852-y. This article has 31 citations and is from a peer-reviewed journal.

7. (moore2020thermodynamicmodelingof media 85112374): Emily E. Moore, P. Turchi, Vincenzo Lordi, D. Weiss, Zachary C. Sims, H. Henderson, M. Kesler, Orlando Rios, Scott K. McCall, and A. Perron. Thermodynamic modeling of the al-ce-cu-mg-si system and its application to aluminum-cerium alloy design. Journal of Phase Equilibria and Diffusion, 41:764-783, Nov 2020. URL: https://doi.org/10.1007/s11669-020-00852-y, doi:10.1007/s11669-020-00852-y. This article has 31 citations and is from a peer-reviewed journal.

8. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

9. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

10. (li2006corrosionwearbehavior pages 2-4): W.S. Li, Z.P. Wang, Y. Lu, and L.H. Yuan. Corrosion wear behavior of al-bronzes in 3.5% nacl solution. Journal of Materials Engineering and Performance, 15:102-110, Feb 2006. URL: https://doi.org/10.1361/105994906x83466, doi:10.1361/105994906x83466. This article has 19 citations and is from a peer-reviewed journal.

11. (janssonUnknownyearphasetransformationsand pages 28-30): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

12. (moore2020thermodynamicmodelingof pages 4-5): Emily E. Moore, P. Turchi, Vincenzo Lordi, D. Weiss, Zachary C. Sims, H. Henderson, M. Kesler, Orlando Rios, Scott K. McCall, and A. Perron. Thermodynamic modeling of the al-ce-cu-mg-si system and its application to aluminum-cerium alloy design. Journal of Phase Equilibria and Diffusion, 41:764-783, Nov 2020. URL: https://doi.org/10.1007/s11669-020-00852-y, doi:10.1007/s11669-020-00852-y. This article has 31 citations and is from a peer-reviewed journal.

13. (moore2020thermodynamicmodelingof pages 20-20): Emily E. Moore, P. Turchi, Vincenzo Lordi, D. Weiss, Zachary C. Sims, H. Henderson, M. Kesler, Orlando Rios, Scott K. McCall, and A. Perron. Thermodynamic modeling of the al-ce-cu-mg-si system and its application to aluminum-cerium alloy design. Journal of Phase Equilibria and Diffusion, 41:764-783, Nov 2020. URL: https://doi.org/10.1007/s11669-020-00852-y, doi:10.1007/s11669-020-00852-y. This article has 31 citations and is from a peer-reviewed journal.

14. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

15. (jenkins2023outliningpotentialbiomarkers pages 1-2): Jill A. Jenkins, MaryLynn Musgrove, and Sarah Jane O. White. Outlining potential biomarkers of exposure and effect to critical minerals: nutritionally essential trace elements and the rare earth elements. Toxics, 11:188, Feb 2023. URL: https://doi.org/10.3390/toxics11020188, doi:10.3390/toxics11020188. This article has 48 citations.

16. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

17. (jenkins2023outliningpotentialbiomarkers pages 14-15): Jill A. Jenkins, MaryLynn Musgrove, and Sarah Jane O. White. Outlining potential biomarkers of exposure and effect to critical minerals: nutritionally essential trace elements and the rare earth elements. Toxics, 11:188, Feb 2023. URL: https://doi.org/10.3390/toxics11020188, doi:10.3390/toxics11020188. This article has 48 citations.
