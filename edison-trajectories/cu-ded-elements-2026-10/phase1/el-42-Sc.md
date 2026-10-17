<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 2eea4b0e-704a-442e-a41f-5d7141e56722
- Submitted: 2026-10-17T19:01:17Z
- Fetched: 2026-10-17T19:25:42Z (status: success)
- Raw trajectory JSON: ../raw/el-42-Sc.json.gz
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

ELEMENT UNDER REVIEW: Sc (rare earth). Cu-Sc precipitation and grain refinement; scandium cost and supply.

Answer for Sc specifically, not for copper alloys in general:
1. ROLE: what Sc does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sc ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sc changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sc, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sc, Cu-Ni-Sc and Cu-Al-Sc are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sc in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sc neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sc | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Sc (rare earth). Cu-Sc precipitation and grain refinement; scandium cost and supply.

Answer for Sc specifically, not for copper alloys in general:
1. ROLE: what Sc does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sc ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sc changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sc, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sc, Cu-Ni-Sc and Cu-Al-Sc are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sc in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sc neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sc | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Scandium (Sc) for as-deposited marine copper-alloy DED

**Decision: EXCLUDE Sc from the designed composition palette for both Cu–Ni and aluminum-bronze deposits.** [CITE] Sc has demonstrated precipitation-hardening potential in *cast, subsequently aged, nearly pure Cu*, but that is not evidence of dense, crack-free, seawater-resistant **as-deposited** Cu–Ni or NAB-compatible material. The cast Cu–Sc experiments already show Sc-rich grain-boundary constituents at 0.16 wt% Sc; their effects on repair cracking and selective corrosion are unknown. No established Sc-bearing marine filler or verified Sc-containing TCCU5 assessment supplies a conservative design bound. This is a decision about the present proposal, **not** a finding that any trace Sc is harmful. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6, janssonUnknownyearphasetransformationsand pages 28-30, nemani2024advancementsinadditive pages 62-68)

The distinction between measured Cu–Sc behavior and the untested marine application governs this assessment:

| Question | Demonstrated quantitative Cu–Sc fact | Implication / unresolved for as-deposited marine laser DED |
|---|---|---|
| Tested compositions | Induction-melted, graphite-crucible, nominally pure Cu–Sc alloys contained **0.16 wt% Sc** and **0.28 wt% Sc**, Cu balance. These were not Cu–Ni, aluminum-bronze, NAB, or welding-filler alloys. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6) | Establishes experimental cast-Cu compositions only; neither composition has been demonstrated in as-deposited marine Cu-alloy DED. |
| As-cast segregation | Both compositions developed multiphase structures with visible eutectic constituents and **5–10 µm Sc-rich primary particles concentrated at grain boundaries**. (franczak2020researchofmechanical pages 4-6) | Grain-boundary particles could affect cracking and localized corrosion, but their effects under laser-DED solidification and layer reheating remain unmeasured. The evidence does not establish as-deposited grain refinement. |
| Post-aging response at 0.16 wt% Sc | Hardness increased from **43 to 62 HV** after **15 h at 450 °C**; conductivity increased from 43 to 52 MS/m. (franczak2020researchofmechanical pages 4-6) | This is post-aged cast material—not an as-deposited result. It cannot support precipitation strengthening without post-build heat treatment. |
| Post-aging response at 0.28 wt% Sc | Hardness increased from **55 to 70 HV** after **20 h at 450 °C**; conductivity increased from 38 to 50 MS/m. (franczak2020researchofmechanical pages 4-6) | This is also post-aged cast material. Repeated DED thermal cycling might precipitate or coarsen Cu₄Sc, but no layer-reheat study demonstrates either outcome. |
| Cu-rich solubility and phases | The paper reports maximum Sc solubility in Cu of approximately **0.5 wt% Sc at 1130 K** and identifies Cu₄Sc, Cu₂Sc, and CuSc. (franczak2020researchofmechanical pages 2-4) | **Unit caution:** the reproduced phase plot includes atomic-percent and weight-percent presentations, creating ambiguity in reading the plotted solubility directly; use the paper’s stated **0.5 wt%** provisionally and verify against the underlying assessment before setting a bound. (franczak2020researchofmechanical media d30e9571) |
| CALPHAD availability | The documented **TCCU5** framework contains 32 elements but **excludes Sc**; therefore it cannot represent Cu–Sc, Cu–Ni–Sc, or Cu–Al–Sc. (janssonUnknownyearphasetransformationsand pages 28-30) | Thermo-Calc/TCCU predictions for Sc-bearing DED alloys are unsupported unless an independently assessed Sc-containing TDB is obtained or developed and validated. |
| Seawater corrosion | **No quantitative Sc-specific evidence located** for Cu–Ni, aluminum bronze/NAB, Mn–Al bronze, tin bronze, gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si in seawater, ASTM D1141 solution, or 3.5 wt% NaCl. | No demonstrated beneficial or harmful Sc range exists for corrosion rate, potential, impedance, pitting, crevice attack, dealloying, erosion–corrosion, or velocity limits. |
| DED and welding | **No Sc-bearing Cu-alloy laser-DED, welding, or marine-cladding trial located**, including Sc-modified ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl. | Effects on solidification cracking, reheated-layer liquation cracking, porosity, oxidation loss, and dilution into C95800 NAB or wrought Cu–Ni are unresolved. |
| Commercial and Navy specifications | **No commercial or Navy Cu-alloy specification located that intentionally permits or requires Sc.** | No specification-derived functional range or impurity ceiling can be assigned; an impairment threshold must not be invented from the cast-Cu aging study. |


*Table: Quantitative Cu–Sc evidence is confined to induction-cast, post-aged nominally pure copper. The table separates those demonstrated results from unresolved corrosion, DED, welding, specification, and CALPHAD questions.*

## 1. Role and specifications

**[CITE] [NUMBERS] Demonstrated mechanism.** In Cu-rich binary alloys, Sc can enter the Cu solid solution and subsequently precipitate Cu₄Sc during artificial aging. Franczak *et al.* induction-melted alloys containing **0.16 and 0.28 wt% Sc**, Cu balance. After aging at **450 °C**, hardness changed respectively from **43 to 62 HV in 15 h** and from **55 to 70 HV in 20 h**; electrical conductivity changed from **43 to 52** and **38 to 50 MS/m**. Their *as-cast* alloys instead contained visible eutectic constituents and **5–10 µm** Sc-enriched primary grain-boundary particles. Neither an as-deposited precipitation benefit nor Sc-induced grain refinement was demonstrated. These are not seawater-service alloys. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6)

**[GAP] Marine-alloy role.** No Sc-specific evidence located establishes protective-film modification, deoxidation benefit, grain refinement, inhibition of dealloying, or improved corrosion in Cu–Ni, aluminum bronze/NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. In particular, the well-established *Al₃Sc-in-aluminum* grain-refinement mechanism must not be assigned to a Cu-matrix NAB alloy. A review of grain refinement in deoxidized Cu does not establish Sc as its effective inoculant. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6, balart2016grainrefinementof pages 1-2)

**[SPEC] [NAVY]** No intentional Sc addition or Sc composition range could be verified for C71500, C95800, or the named ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, or EN 12449 products. None of the named ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl fillers can therefore be presented here as a *specified Sc-bearing filler*. **“No verified Sc range” is not a specification limit of 0 wt%.** (franczak2020researchofmechanical pages 2-4, nemani2024advancementsinadditive pages 62-68)

## 2. Seawater corrosion

**[GAP] No quantitative Sc-effect range is established.** The located Cu–Sc primary experiment reports hardness, conductivity, and microstructure—not exposure to natural seawater, ASTM D1141 water, or **3.5 wt% NaCl**. Consequently there is no defensible Sc-dependent corrosion rate, *E*₍corr₎, polarization/impedance or film-resistance change, pitting or crevice threshold, selective-attack depth, erosion–corrosion result, or permissible seawater velocity. Neither a beneficial nor a harmful **wt% Sc range** can be quoted, and parity with as-deposited or wrought C71500 cannot be claimed. Grain-boundary Sc-rich particles are a *hypothesis for investigation*, not measured evidence of galvanic attack. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6)

## 3. DED, welding, and repair interfaces

**[GAP] No Sc-specific Cu-alloy laser-DED or marine welding/cladding result was located.** Thus there is no demonstrated reduction—or increase—in solidification cracking, reheated-layer liquation cracking, porosity, oxidation/evaporation loss, or substrate-interface cracking. The **5–10 µm** grain-boundary primary constituents observed in cast Cu–Sc suggest a reason to examine terminal-liquid films and reheating, but do not measure crack susceptibility. In particular, do not transfer an aluminum-alloy Sc crack-refinement result to Cu–Ni or NAB. (franczak2020researchofmechanical pages 4-6, nemani2024advancementsinadditive pages 62-68)

**[CITE] [NAVY] Indirect process context only.** Cu-alloy AM reviews identify high thermal conductivity and near-infrared reflectivity as laser-fusion obstacles; a review estimates **2–6%** theoretical Cu absorption around **1064 nm**, but does **not** measure what Sc does to absorption. An ONR-funded *Sc-free* NAB weld-metal study shows that layer reheating and cooling history can change NAB phase constitution and hardness; Sc does not appear in its experiments. An AM review reports laser DED of *Sc-free* CuNi₂SiCr onto cast NAB and identifies α-Cu and κ phases in NAB deposits. These studies motivate testing dilution into **C95800** and wrought Cu–Ni, rather than predicting Sc behavior at either interface. Conventional filler experience likewise cannot validate an untested Sc-modified ERCuNi or NAB filler. (nemani2024advancementsinadditive pages 5-8, nemani2024advancementsinadditive pages 62-68, kuprienko2025analysisofnickel pages 1-7)

## 4. Melting and ultrasonic atomization

**[CITE] [NUMBERS] Directly observed processing:** Cu–Sc at **0.16–0.28 wt% Sc** was induction melted and cast in **graphite crucibles**; the reported melt homogenization was **1350 ± 10 °C for 30 min** under a graphite-protected reducing atmosphere. This demonstrates one casting route, **not** successful atomization in an alumina/zirconia crucible at a roughly **1300 °C** heater ceiling. Graphite contact is part of that experiment, not proof of compatibility with the proposed ceramic crucibles or ultrasonic sonotrode. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6)

**[GAP] Risks requiring measurement, not asserted failures:** Sc pickup into oxide/dross and nonmetallic inclusions; possible interaction with alumina or zirconia; contamination or reaction at a Ti-alloy or Mo sonotrode; and feed-to-powder-to-deposit Sc retention. No Sc-specific vaporization fraction, oxygen pickup, surface-tension change, wetting change, or powder-yield measurement was located. An argon atmosphere reduces exposure but cannot establish Sc recovery. Test actual feedstock, atomized powder, fines, and deposit chemically before assigning a compensation allowance. (franczak2020researchofmechanical pages 2-4, janssonUnknownyearphasetransformationsand pages 28-30)

## 5. Phase diagram and CALPHAD

**[CITE] [NUMBERS]** The Cu–Sc paper *states* maximum Cu-rich solid solubility of approximately **0.5 wt% Sc at 1130 K (about 857 °C)**. It identifies **Cu₄Sc, Cu₂Sc, and CuSc**; the paper describes their approximate Sc contents as **15, 25, and 42 wt%**, respectively. Its reproduced Figure 3 combines an **at%** overview with a **wt%** Cu-rich inset: the plotted units and the stated solubility merit checking against the underlying binary assessment before treating **0.5 wt%** as a precision constraint. The figure depicts Cu-rich liquidus depression toward a eutectic rather than evidence that trace Sc alone raises pure Cu above the equipment’s **1200–1250 °C** usable-liquidus limit. A Cu–Ni–Sc or Cu–Al–Sc liquidus, invariant-reaction temperature/composition in **wt% Sc**, and interaction-dependent superheat margin cannot be reliably calculated from this binary figure. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical media d30e9571)

**[CITE] [GAP]** Thermo-Calc’s documented **TCCU5** lists **32 elements and excludes Sc**: it therefore cannot calculate an assessed Cu–Sc, Cu–Ni–Sc, or Cu–Al–Sc system, even though it can perform Scheil and liquid-property calculations for its *supported* compositions. No validated Sc-inclusive COST 531 assessment or accessible published TDB for these three marine-relevant systems was established by this search. Do not interpret a pycalphad run with missing Sc parameters as a prediction; obtain the actual TDB and verify its elements, phases, and binary/ternary assessments first. (janssonUnknownyearphasetransformationsand pages 28-30, janssonUnknownyearphasetransformationsand pages 30-32)

## 6. Supply, price, and safety

**[CITE] [NUMBERS]** The USGS account of the **2025 final U.S. critical-minerals list** explicitly includes **scandium, nickel, and copper** among **60** commodities; Sc was also on the 2022 list. The supply literature characterizes Sc as a small, opaque by-product market, with production estimates rather than reliable transaction statistics. Its published historical price corridor for **99.99% Sc metal** is **US$185,000–210,000/kg**, with reported April 2023 quotations of **US$348,000 and US$517,000/kg**. These unusual quotations should **not** be used as a current 2026 purchasing quote. The same source estimates **Sc₂O₃ at 1.6% of the metal price**—approximately **US$3,000–3,400/kg oxide** when applied to the historical metal corridor—not the price of alloy-ready Sc metal. At **0.16 wt% Sc**, the historical metal corridor alone implies approximately **US$296–336 per kg of alloy** for contained Sc, before master-alloy conversion, losses, or powder production. (iii2026usgscriticalminerals pages 1-2, sverdrup2024onthesupply pages 4-6)

**[GAP]** No Sc-specific OSHA exposure limit, Navy prohibition, or RoHS/REACH restriction for *Sc in Cu alloy* was verified; absence of a verified element-specific rule does not exempt powder making from applicable dust, fume, chemical, and environmental controls. Treat Sc-containing fine metal powder and laser fume as inhalation and combustible-powder assessments requiring ventilation, collection, contamination control, and a process-specific safety review. No Sc-specific toxicity threshold for these operations was established in the retrieved evidence. (sverdrup2024onthesupply pages 4-6)

## 7. Bounds, interactions, and evidence quality

**[CITE] [GAP] Decision and bounds.** **EXCLUDE as a designed addition, both families.** There is **no specification-derived conservative maximum, demonstrated as-deposited aggressive maximum, marine functional floor, or defensible impurity maximum** in wt% Sc. The **0.16 and 0.28 wt% Sc** cast-Cu experiments are *not* qualification of those concentrations for either deposit family. The approximately **0.5 wt% Sc** *reported binary solubility* is not a joint Cu–Ni/NAB limit; grain-boundary particles are observed well below it. Accordingly all four requested numerical verdict fields are **NA**, rather than false precision. If Sc is carried over unintentionally, record it analytically in **both powder and deposit**; a project-specific acceptance criterion would need to follow demonstrable crack, inclusion, corrosion, and 30-day selective-attack testing. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6, janssonUnknownyearphasetransformationsand pages 28-30)

**[GAP] Joint constraints:** no measured permissible Sc:Ni, Sc:Fe, Sc:Mn, or Sc:Al ratio, nor **Sc + Al/Fe/Mn** sum, exists for these deposits. Candidate interactions to *test* are partitioning among Cu₄Sc, α-Cu, and NAB κ/β constituents; Sc consumption by oxygen; and changes in Sc recovery when Ni- or Al-rich substrate metal dilutes the first layer. No study found establishes that Sc neutralizes an embrittler or offsets Ni while preserving seawater-film performance. These are hypotheses, not design equations. The strongest element-specific evidence supports Cu–Sc precipitation **after aging**; it is **thin** for the actual marine, no-heat-treatment, single-stream laser-DED objective. (franczak2020researchofmechanical pages 2-4, franczak2020researchofmechanical pages 4-6, janssonUnknownyearphasetransformationsand pages 28-30, nemani2024advancementsinadditive pages 62-68)

**Principal sources:** Franczak *et al.*, “Research of mechanical and electrical properties of Cu–Sc and Cu–Zr alloys,” *Archives of Civil and Mechanical Engineering* **20**, 28 (2020), **doi:10.1007/s43452-020-00035-z**; Balart *et al.*, “Grain Refinement of Deoxidized Copper,” *Metallurgical and Materials Transactions A* **47**, 4988–5011 (2016), **doi:10.1007/s11661-016-3671-8**; Nemani *et al.*, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites,” *Journal of Manufacturing and Materials Processing* **8**, 54 (2024), **doi:10.3390/jmmp8020054**; Sverdrup and Sverdrup, “On the Supply Dynamics of Scandium…,” *Biophysical Economics and Sustainability* **9** (2024), **doi:10.1007/s41247-024-00118-y**. For database coverage: Jansson *et al.*, “Phase Transformations and Kinetic Simulations of Cu-based Alloys,” *Copper Alloys 2022* proceedings, ISBN 978-3-910411-01-2 (**no DOI established**). For the critical-minerals list: USGS authors Jones *et al.*, “USGS critical minerals review,” *Mining Engineering*, May 2026 (**no DOI established**). The NAB weld comparator is Kuprienko, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*, Ohio State University dissertation (2025; **no DOI established**). No publication by the specified PI is relied on. (franczak2020researchofmechanical pages 1-2, balart2016grainrefinementof pages 1-2, nemani2024advancementsinadditive pages 1-2, sverdrup2024onthesupply pages 4-6, janssonUnknownyearphasetransformationsand pages 28-30, iii2026usgscriticalminerals pages 1-2, kuprienko2025analysisofnickel pages 1-7)

VERDICT | Sc | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (franczak2020researchofmechanical pages 2-4): Krystian Franczak, Paweł Kwaśniewski, Grzegorz Kiesiewicz, Małgorzata Zasadzińska, Bartosz Jurkiewicz, Paweł Strzępek, and Zbigniew Rdzawski. Research of mechanical and electrical properties of cu–sc and cu–zr alloys. Archives of Civil and Mechanical Engineering, Feb 2020. URL: https://doi.org/10.1007/s43452-020-00035-z, doi:10.1007/s43452-020-00035-z. This article has 31 citations.

2. (franczak2020researchofmechanical pages 4-6): Krystian Franczak, Paweł Kwaśniewski, Grzegorz Kiesiewicz, Małgorzata Zasadzińska, Bartosz Jurkiewicz, Paweł Strzępek, and Zbigniew Rdzawski. Research of mechanical and electrical properties of cu–sc and cu–zr alloys. Archives of Civil and Mechanical Engineering, Feb 2020. URL: https://doi.org/10.1007/s43452-020-00035-z, doi:10.1007/s43452-020-00035-z. This article has 31 citations.

3. (janssonUnknownyearphasetransformationsand pages 28-30): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

4. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

5. (franczak2020researchofmechanical media d30e9571): Krystian Franczak, Paweł Kwaśniewski, Grzegorz Kiesiewicz, Małgorzata Zasadzińska, Bartosz Jurkiewicz, Paweł Strzępek, and Zbigniew Rdzawski. Research of mechanical and electrical properties of cu–sc and cu–zr alloys. Archives of Civil and Mechanical Engineering, Feb 2020. URL: https://doi.org/10.1007/s43452-020-00035-z, doi:10.1007/s43452-020-00035-z. This article has 31 citations.

6. (balart2016grainrefinementof pages 1-2): María José Balart, Jayesh B. Patel, Feng Gao, and Zhongyun Fan. Grain refinement of deoxidized copper. Metallurgical and Materials Transactions A, 47:4988-5011, Aug 2016. URL: https://doi.org/10.1007/s11661-016-3671-8, doi:10.1007/s11661-016-3671-8. This article has 57 citations.

7. (nemani2024advancementsinadditive pages 5-8): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

8. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

9. (janssonUnknownyearphasetransformationsand pages 30-32): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

10. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

11. (sverdrup2024onthesupply pages 4-6): Harald Ulrik Sverdrup and Antoniy Elias Sverdrup. On the supply dynamics of scandium, global resources, production, oxide and metal price, a prospective modelling study using world7. Biophysical Economics and Sustainability, Apr 2024. URL: https://doi.org/10.1007/s41247-024-00118-y, doi:10.1007/s41247-024-00118-y. This article has 14 citations.

12. (franczak2020researchofmechanical pages 1-2): Krystian Franczak, Paweł Kwaśniewski, Grzegorz Kiesiewicz, Małgorzata Zasadzińska, Bartosz Jurkiewicz, Paweł Strzępek, and Zbigniew Rdzawski. Research of mechanical and electrical properties of cu–sc and cu–zr alloys. Archives of Civil and Mechanical Engineering, Feb 2020. URL: https://doi.org/10.1007/s43452-020-00035-z, doi:10.1007/s43452-020-00035-z. This article has 31 citations.

13. (nemani2024advancementsinadditive pages 1-2): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.
