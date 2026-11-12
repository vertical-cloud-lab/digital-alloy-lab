<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: aaeddb2b-ebd5-45e7-9c7b-da10af3dcd9d
- Submitted: 2026-10-17T18:59:04Z
- Fetched: 2026-10-17T19:30:37Z (status: success)
- Raw trajectory JSON: ../raw/el-13-Ti.json.gz
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

ELEMENT UNDER REVIEW: Ti (strengthening addition). Cu-Ti C19900 (about 3 Ti); ERCuNi welding filler (AWS A5.7) carries 0.2-0.5 Ti as a deoxidizer; 0.1 wt% Ti in wire-arc NAB lowered corrosion current (Zhang et al. 2026). Ti attacks ceramic crucibles and forms intermetallics with Ni and Cu.

Answer for Ti specifically, not for copper alloys in general:
1. ROLE: what Ti does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ti ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ti changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ti, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ti, Cu-Ni-Ti and Cu-Al-Ti are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ti in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ti neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ti | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ti (strengthening addition). Cu-Ti C19900 (about 3 Ti); ERCuNi welding filler (AWS A5.7) carries 0.2-0.5 Ti as a deoxidizer; 0.1 wt% Ti in wire-arc NAB lowered corrosion current (Zhang et al. 2026). Ti attacks ceramic crucibles and forms intermetallics with Ni and Cu.

Answer for Ti specifically, not for copper alloys in general:
1. ROLE: what Ti does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ti ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ti changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ti, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ti, Cu-Ni-Ti and Cu-Al-Ti are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ti in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ti neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ti | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Titanium (Ti): composition-screen decision

**Decision — INCLUDE Ti as a designed, low-level addition in both Cu–Ni and aluminum-bronze candidates.** [CITE] The case is strongest for *processability*: specified Cu–Ni welding consumables use Ti to scavenge oxygen and nitrogen and limit porosity, while cast and wire-arc-deposited nickel-aluminum bronze (NAB) demonstrate grain refinement at small additions. It is **not** established that Ti makes an as-deposited alloy as seawater-resistant as wrought C71500. More Ti is not reliably better: the tested NAB response is non-monotonic, and Cu–Ni welding experience identifies excessive Ti as a cracking promoter. Accordingly, the proposed bounds are experimental design limits, not qualified DED or Navy composition limits. (devletian2006fluxcoredarc pages 4-7, devletian2006fluxcoredarc pages 7-10, zhang2026effectoflowlevel pages 13-16, rivero2021effectofti pages 6-8)

## 1. Roles, alloy families, and specifications

- **Cu–Ni welding alloys.** [SPEC] [NAVY] AWS A5.7 **ERCuNi / UNS C71580** wire contains **0.20–0.50 wt% Ti**; the Navy **MIL-E-21562E(SH) EN67/RN67** wire/rod has the same range. The report also lists **0.50 wt% maximum Ti** in AWS A5.6 ECuNi *as-deposited shielded-metal-arc weld metal*: that number is a maximum, not a 0.50 wt% target. Ti acts principally as a deoxidizer, denitrider and grain refiner, improving fluidity and limiting weld porosity. Neither the filler specification nor this report demonstrates Ti precipitation strengthening or improved seawater corrosion in the weld. These consumable ranges must not be presented as the compositions required by ASTM B111/B171/B466 wrought C71500. (devletian2006fluxcoredarc pages 4-7, devletian2006fluxcoredarc pages 7-10)
- **Aluminum bronze/NAB.** [NUMBERS] Rivero *et al.* added **0.012 wt% Ti** to *cast* CuAl10Fe5Ni5/C95500; Zhang *et al.* studied **nominal 0.03, 0.05 and 0.10 wt% Ti** in wire-arc NAB. The latter applied **50-nm Ti particles between layers**, not pre-alloyed wire or powder. Ti-bearing material showed finer grains and altered κ-phase fractions/morphology; Zhang found Ti largely in α-Cu and **did not identify a new Ti-bearing second phase through 0.10 wt%**. Consequently, neither study establishes a Ti range in ASTM B148 C95800 or an AWS ERCuNiAl filler specification. (rivero2021effectofti pages 1-2, zhang2026effectoflowlevel pages 2-4, zhang2026effectoflowlevel pages 4-8, rivero2021effectofti pages 6-8)
- **Other families.** [GAP] In Cu–Sn bronze, Ti additions and Ti–Ni-containing interdendritic intermetallics have been studied for cast-alloy grain structure and strength; that is not proof of seawater performance in a Ti-containing gunmetal. The located evidence does not establish a Ti-containing Navy specification or quantitative marine benefit for Mn–Al bronze, brass, gunmetal, Cu–Ni–Sn or Cu–Ni–Si. In particular, corrosion resistance of *bulk titanium* or a titanium coating cannot be transferred to dilute Ti in Cu, and Ti has **not** been shown here to inhibit dezincification or selective Al attack. The Cu–Ti intermetallic system does provide a possible strengthening route at substantially higher Ti content, but age-hardening data do not establish strengthening **as deposited**, without heat treatment. (brice2015anassessmentof pages 31-37, silva2023developmentoftinibaseda pages 48-53, zhang2026effectoflowlevel pages 4-8)

## 2. Seawater-relevant corrosion: what the measurements actually show

[CITE] [NUMBERS] **Cast NAB, Rivero *et al.* (2021), 3.5 wt% NaCl:** At **0 versus 0.012 wt% Ti**, respectively, 30-day mass loss was **0.034% versus 0.020%**, but the difference was *not statistically significant at 95% confidence*. Open-circuit potential was **−150 versus −148 mV versus Ag/AgCl**; polarization-derived corrosion rate **0.021 versus 0.023 mm/year**; polarization resistance **2.4 × 10⁵ versus 2.1 × 10⁵ Ω·cm²**. The electrochemical rate and resistance therefore move slightly in the **unfavorable** direction despite the lower measured mass loss. The authors observed general corrosion rather than visible pitting after immersion. This is not evidence for a protective TiO₂ film. (rivero2021effectofti pages 2-3, rivero2021effectofti pages 5-6, rivero2021effectofti pages 6-8)

[CITE] [NUMBERS] **Wire-arc NAB, Zhang *et al.* (2026), 3.5 wt% NaCl:** The measured sequence **baseline / 0.03 / 0.05 / 0.10 wt% nominal Ti** gave *i*₍corr₎ **10.06 / 10.88 / 10.00 / 8.49 µA·cm⁻²** and *E*₍corr₎ **−192.91 / −191.96 / −188.57 / −188.57 mV versus SCE**. Thus **0.03 wt% worsened current by about 8%**, 0.05 wt% was essentially unchanged, and 0.10 wt% reduced current by **15.6%** versus baseline. Corresponding stabilized OCP values reported in Table 4 were **−219.72 / −223.91 / −223.95 / −206.98 mV**; OCP and *E*₍corr₎ are different measurements and should not be conflated. Across **7–21 days**, the three Ti-modified alloys lost **0.237 / 0.211 / 0.167 g·m⁻²·day⁻¹**, respectively; the cited passage does not give an equally usable baseline immersion rate. At 0.10 wt%, the product-layer thickness was **1.83 µm**. XRD identified **Cu₂O and Al₂O₃**, **not TiO₂**; grain/κ-phase morphology and film continuity, rather than demonstrated Ti-rich passivation, are the defensible explanations. The study did **not** establish film resistance by EIS or 30-day selective-attack depth. (zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel pages 11-13, zhang2026effectoflowlevel media 354f2189, zhang2026effectoflowlevel pages 4-8)

[GAP] **Helpful and harmful ranges are processing-specific.** In these NAB datasets, **0.012 wt%** refines cast grains without a significant corrosion change; **0.03 wt%** is worse electrochemically in the wire-arc experiment; **0.05 wt%** gives essentially baseline current; **0.10 wt%** performs best among its tested conditions. There is **no measured upper concentration at which Ti starts harming seawater corrosion**, nor a Ti-specific result for natural seawater, ASTM D1141 seawater, erosion-corrosion, flow-velocity limits, crevices or quantitative dealloying depth. None of the values constitutes an as-deposited C71500-versus-DED comparison. (rivero2021effectofti pages 5-6, zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel pages 2-4)

## 3. DED, repair welding, and powder production

[NAVY] [CITE] **Use welding as an analogue, not a DED qualification.** The Cu–Ni shipboard welding study describes Ti/Si killing agents as necessary to suppress gas porosity but also reports that **excess Ti, Fe or Si promotes cracking**. Cu–30Ni has an approximately **1170–1240 °C** solidus–liquidus interval; segregation, restraint and reheating make solidification, HAZ-liquation and ductility-dip cracking credible in multilayer repair. No isolated numerical Ti cracking threshold was established by that report: **0.20 wt% is the specified *minimum* in ERCuNi, not a demonstrated onset of cracking**. Inspect reheated subsurface layers as well as surfaces. (devletian2006fluxcoredarc pages 4-7, devletian2006fluxcoredarc pages 7-10)

[GAP] Ti-specific, single-stream **laser blown-powder DED** evidence on self-builds, C95800 repairs and wrought Cu–Ni repairs was not located. The wire-arc nanoparticle experiment cannot establish that dissolved Ti in pre-alloyed powder reproduces its nucleation mechanism. Conversely, laser powder DED of an extreme *Ti-alloy-to-Cu-alloy gradient* cracked in Cu–Ti-intermetallic-rich transitions; this demonstrates a hazard at high local Ti, **not** that a deposit containing 0.10–0.50 wt% Ti will crack. At the NAB interface, Al/Fe/Ni dilution can change κ phases and local Ti partitioning; at a Cu–Ni interface, dilution lowers the deposit’s specified Ti while reheating can expose segregated grain boundaries. These are testable predictions, not measured Ti-specific repair outcomes. Evaporation or oxidation loss under a 1.07-µm laser has not been quantified for these compositions; analyze **charge, atomized powder and each deposit** rather than assuming nominal Ti is retained. (zhang2026effectoflowlevel pages 2-4, rubioejchel2026laserpowderdirected pages 1-2, rubioejchel2026laserpowderdirected pages 3-4, zhang2026effectoflowlevel pages 4-8, devletian2006fluxcoredarc pages 7-10)

[CITE] **Induction melting/atomization.** Ti has strong oxygen affinity; dry, low-oxygen argon, short hot-contact times and oxide/inclusion assays matter more than nominal charge accuracy alone. Work on **Ti-rich Ti–Al melts** shows ceramic interaction, oxygen pickup and effects of melt time/temperature, but does **not** quantify losses from dilute Cu–Ti in the proposed alumina or zirconia crucible. A Cu–Ti melt has been used deliberately to react with graphite, producing **TiC**: graphite-contact hardware is therefore an avoidable Ti sink/inclusion source. Containerless Cu–Ti measurements found surface tension increased as Ti fraction increased over the **large compositions tested**; they do not give a validated droplet-size correction at 0.10–0.50 wt% Ti. The reported **1–1.5% droplet mass loss around 1800 K** is *total mass loss at a higher temperature*, not a Ti evaporation percentage at the atomizer. [GAP] No quantitative evidence was obtained for Ti loss or pickup from the particular ultrasonic atomizer’s **Ti-alloy versus Mo sonotrode**. Measure tip wear and powder chemistry; do not assume either tip inert. (gomes2011effectofmelting pages 4-5, gomes2011effectofmelting pages 5-8, guo2020synthesisofcubased pages 7-12, guo2020synthesisofcubased pages 17-22, amore2011surfacetensionof pages 2-3, amore2011surfacetensionof pages 4-5)

## 4. Phase limits and the 1,250 °C processing gate

[CITE] Cu–Ti is **not an isomorphous strengthening system**: assessed diagrams identify Cu-rich **Cu₄Ti**, and further toward Ti-rich compositions **Cu₂Ti, Cu₃Ti₂, Cu₄Ti₃, CuTi and CuTi₂**. This implies potential particle strengthening, but also hard intermetallics and, after segregation or reheating, brittle boundary constituents. The retrieved phase sources do **not** securely establish a *numerical maximum Ti solubility in α-Cu, in wt% at a specified temperature*; no numerical solubility-derived upper bound is claimed here. A Cu–Ti alloy near **80 wt% Cu** was reported to melt near **885 °C**; that *high-Ti eutectic-region datum* must not be mistaken for the liquidus of a dilute Cu–Ni–Ti repair powder. (brice2015anassessmentof pages 31-37, silva2023developmentoftinibaseda pages 48-53, guo2020synthesisofcubased pages 7-12)

[CITE] Cu–Ni–Ti has experimental 900 °C phase equilibria and measured high-Ti ternary invariant reactions; a published assessment of a Ti–Ni–Cu pseudobinary also exists. A Cu–Al–Ti diffusion-couple study used CALPHAD and identified Ti–Cu–Al and Cu–Ti reaction products. Thermo-Calc **TCCU** is documented as a Cu-alloy thermodynamic database compatible with kinetic modeling, but these retrieved sources do **not** verify which specific Ti binaries/ternaries are assessed in the PI’s installed **TCCU version**; inspect its element and assessed-system lists and benchmark against experiments before using pycalphad exports. **COST 531 is a lead-free *solder* effort**, not evidence of validated NAB or Cu–Ni–Ti repair thermodynamics. (jin2018experimentaldeterminationof pages 1-3, tang2000phaseequilibriain pages 1-2, wang2018ahighthroughputsearch pages 3-7, tang2000phaseequilibriain pages 2-3)

[NUMBERS] **The liquidus gate is controlled by the complete composition, especially Ni.** Published welding data give **1240 °C** for wrought Cu–30Ni/C71500: that leaves only **10 °C below 1250 °C** *before* adding Ti, other elements, measurement uncertainty or the useful superheat needed for atomization. By contrast, Cu–10Ni is listed near **1170 °C**. It is unjustified either to assert that small Ti always raises liquidus or to use the low binary Cu–Ti eutectic to assert that it always lowers the multicomponent liquidus. Require measured DSC/thermal analysis and equilibrium-plus-Scheil predictions for **each Ni–Ti–Al–Fe–Mn combination**; reject compositions whose measured liquidus leaves inadequate operating superheat below the equipment ceiling. (devletian2006fluxcoredarc pages 4-7, amore2011surfacetensionof pages 4-5, jin2018experimentaldeterminationof pages 1-3)

## 5. Joint constraints, supply, safety and evidence quality

- **Interactions.** [CITE] In Cu–Ni weld metal, evaluate **Ti + Si + Fe** jointly for the deoxidation/porosity-versus-cracking tradeoff; **Mn** also deoxidizes/desulfurizes and may moderate susceptibility. Control **O and N** because they consume Ti; avoid treating Ti as a substitute for controlling **P, Pb, Bi or other low-melting impurities**. With **Ni**, model Ni–Ti/ternary intermetallic formation and the Ni-driven liquidus increase; with **Al + Ni + Fe**, measure NAB κ-phase changes and Al₂O₃/Cu₂O film integrity. With **C**, anticipate TiC where carbon-containing hardware contacts the melt. No validated numerical Ti/Ni, Ti/Al, or Ti/Fe sum-or-ratio criterion was found for these DED alloys. (devletian2006fluxcoredarc pages 4-7, devletian2006fluxcoredarc pages 7-10, jin2018experimentaldeterminationof pages 3-4, zhang2026effectoflowlevel pages 4-8, guo2020synthesisofcubased pages 17-22)
- **Supply.** [CITE] Titanium is a US critical-mineral supply concern in the cited government technical literature; distinguish the **2025 USGS *recommendation*** to add **copper** from proof of the wording of the **final** list. A USGS titanium-sponge outlook reports **one active US sponge producer in 2023**, limited to electronics, and China supplying **67% of world sponge output** that year. [GAP] These retrieved sources provide **no defensible contemporaneous USD/kg Ti sponge or powder price**, and do not independently reproduce the text of both the **2022 and 2025 final Federal Register lists**; a numeric procurement quote or formal final-list claim would be unsupported here. At 0.10 wt% Ti, a 0.5-kg charge requires **0.5 g Ti** before losses; at 0.50 wt%, **2.5 g**. (alonso2025worldmineralsoutlook—cobalt pages 22-25, nassar2025methodologyandtechnical pages 9-10)
- **Safety/regulation.** [GAP] No Ti-specific prohibition in the cited ASTM/AWS/Navy specifications or a RoHS/REACH ban on Ti as a copper-alloy addition was established. Do not present a generic dust limit as a Ti-alloy-specific OSHA permissible exposure limit. Treat atomized fines and laser fume as inhalation exposures, and isolated fine Ti-containing or Ti-rich residues as potential combustible-metal-dust hazards; use enclosure, local exhaust, appropriate dust/fire controls and the actual powder’s safety data. Risks depend on particle size, oxidation state and co-alloying metals, rather than on bulk Ti wt% alone. (devletian2006fluxcoredarc pages 7-10, tetsui2010evaluationofyttria pages 1-2)

## 6. Recommended bounds, **Ti wt% in pre-alloyed powder and resulting alloy**

| Bound | Cu–Ni family | Aluminum-bronze/NAB family | Setting evidence and failure mode |
|---|---:|---:|---|
| **Functional floor** | **0.20 wt%**, for the *specified ERCuNi deoxidizing-filler function*, **not** a measured minimum DED effect | **0.012 wt%** for *measured cast grain refinement*; **0.05 wt%** is the lowest tested wire-arc level with clear refinement | Below the relevant tested/specification level, a functional effect in that family is not established; **0.03 wt%** wire-arc Ti actually worsened *i*₍corr₎. (devletian2006fluxcoredarc pages 7-10, rivero2021effectofti pages 1-2, zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel pages 16-18) |
| **Conservative maximum** | **0.50 wt%** | **0.10 wt%** | Cu–Ni: upper **AWS A5.7/MIL-E-21562E(SH)** ERCuNi/EN67/RN67 wire limit; excess-Ti welding-crack risk. NAB: highest tested wire-arc level with favorable NaCl response, **not** a standard filler limit; larger-addition behavior is untested. (devletian2006fluxcoredarc pages 7-10, devletian2006fluxcoredarc pages 4-7, zhang2026effectoflowlevel pages 13-16) |
| **Non-conservative maximum** | **0.50 wt%** | **0.50 wt%, exploratory only** | Do **not** extend Cu–Ni beyond its qualified filler ceiling on the present evidence. For NAB, 0.50 wt% is a proposed *cross-family* stress-test ceiling borrowed from Cu–Ni filler practice, **not** a demonstrated safe NAB concentration. Stop lower if DSC, inclusions, cracking or chloride attack fails; no solubility-derived or NAB seawater validation supports 0.50 wt%. (devletian2006fluxcoredarc pages 7-10, rubioejchel2026laserpowderdirected pages 1-2, rivero2021effectofti pages 6-8) |

**Palette encoding:** If a single search-space ceiling must cover *both* families, use **conservative_max_wt = 0.10** and **nonconservative_max_wt = 0.50**; these do **not** imply that the same concentration is equally justified in each family. Encode **floor_wt = 0.012** as the smallest demonstrated *microstructural* Ti effect, while treating **0.20 wt%** separately as the specified Cu–Ni *welding-consumable* floor. There is **no impurity-only maximum** because Ti is deliberately included. Prioritize paired controls and actual-composition verification, followed by the proposed ASTM D1141 electrochemical screen and 30-day cross-section depth, on both self-builds and each repair substrate. [GAP] The evidence supporting Ti’s **seawater performance as a pre-alloyed, as-deposited laser-DED material remains thin**. (rivero2021effectofti pages 1-2, devletian2006fluxcoredarc pages 7-10, zhang2026effectoflowlevel pages 13-16)

### Full citations central to the decision

1. Rivero, P. J., Berlanga, C., Palacio, J. F. & Biezma-Moraleda, M. V. “Effect of Ti on Microstructure, Mechanical Properties and Corrosion Behavior of a Nickel-Aluminum Bronze Alloy.” *Materials Research* **24** (2021). **doi:10.1590/1980-5373-mr-2020-0335**. (rivero2021effectofti pages 1-2, rivero2021effectofti pages 6-8)
2. Zhang, L.-M. *et al.* “Effect of low-level Ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of WAAM-processed nickel-aluminium bronze.” *Advanced Materials Joining* **1**, article 17 (2026). **doi:10.1007/s44500-026-00016-x**. (zhang2026effectoflowlevel pages 2-4, zhang2026effectoflowlevel pages 13-16)
3. Devletian, J. H., Sullivan, M. J. & Engineer, C. W. *Flux Cored Arc Welding of CuNi 90/10 Piping with CuNi 70/30 Filler Metal* (2006), especially Tables 2–3; reproduces **ANSI/AWS A5.7 ERCuNi** and **MIL-E-21562E(SH) EN67/RN67** composition requirements. **DOI not established in retrieved report**. (devletian2006fluxcoredarc pages 4-7, devletian2006fluxcoredarc pages 7-10)
4. Jin, B. *et al.* “Experimental determination of phase equilibria at 900°C and liquidus surface in the Cu–Ni–Ti system.” *Journal of Mining and Metallurgy B* **54**, 209–223 (2018). **doi:10.2298/JMMB180209009J**. (jin2018experimentaldeterminationof pages 1-3)
5. Wang, J. *et al.* “A High-Throughput Search for Composition–Phase–Property Relations of Cu–Ni/Ti–Al Elastic Copper Alloys.” *Materials* **11**, 2513 (2018). **doi:10.3390/ma11122513**. (wang2018ahighthroughputsearch pages 3-7)
6. Amore, S., Brillo, J., Egry, I. & Novakovic, R. “Surface tension of liquid Cu–Ti binary alloys measured by electromagnetic levitation and thermodynamic modelling.” *Applied Surface Science* **257**, 7739–7745 (2011). **doi:10.1016/j.apsusc.2011.04.019**. (amore2011surfacetensionof pages 4-5)
7. Guo, L. *et al.* “Synthesis of Cu-based TiCₓ composites via in-situ reaction between CuₓTi melt and dissolvable solid carbon.” *Powder Technology* **362**, 375–385 (2020). **doi:10.1016/j.powtec.2019.11.122**. (guo2020synthesisofcubased pages 7-12)
8. Rubio-Ejchel, D. *et al.* “Laser powder directed energy deposition fabrication and tensile sandwich evaluation of Ti64–C103–GRCop-42 functionally graded materials.” *Journal of Materials Research* (2026). **doi:10.1557/s43578-026-01964-w**. (rubioejchel2026laserpowderdirected pages 1-2)
9. Alonso, E. *et al.* *World Minerals Outlook—Cobalt, Gallium, Helium, Lithium, Magnesium, Palladium, Platinum, and Titanium Through 2029.* USGS Scientific Investigations Report 2025–5021 (2025). **doi:10.3133/sir20255021**. (alonso2025worldmineralsoutlook—cobalt pages 22-25)
10. Nassar, N. T. *et al.* *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals.* USGS Open-File Report 2025–1047 (2025). **doi:10.3133/ofr20251047**. (nassar2025methodologyandtechnical pages 9-10)

VERDICT | Ti | decision=INCLUDE | family=both | conservative_max_wt=0.10 | nonconservative_max_wt=0.50 | floor_wt=0.012 | impurity_max_wt=NA | evidence=thin

References

1. (devletian2006fluxcoredarc pages 4-7): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

2. (devletian2006fluxcoredarc pages 7-10): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

3. (zhang2026effectoflowlevel pages 13-16): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

4. (rivero2021effectofti pages 6-8): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

5. (rivero2021effectofti pages 1-2): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

6. (zhang2026effectoflowlevel pages 2-4): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

7. (zhang2026effectoflowlevel pages 4-8): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

8. (brice2015anassessmentof pages 31-37): D. A. Brice. An assessment of uncommon titanium binary systems: ti-zn, ti-cu, and ti-sb. ArXiv, May 2015. URL: https://doi.org/10.12794/metadc799482, doi:10.12794/metadc799482. This article has 6 citations.

9. (silva2023developmentoftinibaseda pages 48-53): JD Silva. Development of ti-ni-based alloys for solid-state refrigeration. Unknown journal, 2023.

10. (rivero2021effectofti pages 2-3): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

11. (rivero2021effectofti pages 5-6): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

12. (zhang2026effectoflowlevel pages 11-13): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

13. (zhang2026effectoflowlevel media 354f2189): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

14. (rubioejchel2026laserpowderdirected pages 1-2): Daniel Rubio-Ejchel, Michael Lester, KenHee Ryou, Christopher Tandoc, Dillon K. Jobes, Jun Fan, Wenda Tan, William S. LePage, Yong-Jie Hu, and Jerard V. Gordon. Laser powder directed energy deposition fabrication and tensile sandwich evaluation of ti64-c103-grcop-42 functionally graded materials. Journal of Materials Research, Sep 2026. URL: https://doi.org/10.1557/s43578-026-01964-w, doi:10.1557/s43578-026-01964-w. This article has 1 citations and is from a peer-reviewed journal.

15. (rubioejchel2026laserpowderdirected pages 3-4): Daniel Rubio-Ejchel, Michael Lester, KenHee Ryou, Christopher Tandoc, Dillon K. Jobes, Jun Fan, Wenda Tan, William S. LePage, Yong-Jie Hu, and Jerard V. Gordon. Laser powder directed energy deposition fabrication and tensile sandwich evaluation of ti64-c103-grcop-42 functionally graded materials. Journal of Materials Research, Sep 2026. URL: https://doi.org/10.1557/s43578-026-01964-w, doi:10.1557/s43578-026-01964-w. This article has 1 citations and is from a peer-reviewed journal.

16. (gomes2011effectofmelting pages 4-5): F. Gomes, H. Puga, Joaquim Barbosa, and C. Silva Ribeiro. Effect of melting pressure and superheating on chemical composition and contamination of yttria-coated ceramic crucible induction melted titanium alloys. Journal of Materials Science, 46:4922-4936, Feb 2011. URL: https://doi.org/10.1007/s10853-011-5405-z, doi:10.1007/s10853-011-5405-z. This article has 68 citations and is from a peer-reviewed journal.

17. (gomes2011effectofmelting pages 5-8): F. Gomes, H. Puga, Joaquim Barbosa, and C. Silva Ribeiro. Effect of melting pressure and superheating on chemical composition and contamination of yttria-coated ceramic crucible induction melted titanium alloys. Journal of Materials Science, 46:4922-4936, Feb 2011. URL: https://doi.org/10.1007/s10853-011-5405-z, doi:10.1007/s10853-011-5405-z. This article has 68 citations and is from a peer-reviewed journal.

18. (guo2020synthesisofcubased pages 7-12): Lei Guo, Yang Yang, Xiaochun Wen, Han Gao, Zhe Wang, and Zhancheng Guo. Synthesis of cu-based ticx composites via in-situ reaction between cuxti melt and dissolvable solid carbon. Powder Technology, 362:375-385, Feb 2020. URL: https://doi.org/10.1016/j.powtec.2019.11.122, doi:10.1016/j.powtec.2019.11.122. This article has 28 citations and is from a domain leading peer-reviewed journal.

19. (guo2020synthesisofcubased pages 17-22): Lei Guo, Yang Yang, Xiaochun Wen, Han Gao, Zhe Wang, and Zhancheng Guo. Synthesis of cu-based ticx composites via in-situ reaction between cuxti melt and dissolvable solid carbon. Powder Technology, 362:375-385, Feb 2020. URL: https://doi.org/10.1016/j.powtec.2019.11.122, doi:10.1016/j.powtec.2019.11.122. This article has 28 citations and is from a domain leading peer-reviewed journal.

20. (amore2011surfacetensionof pages 2-3): S. Amore, J. Brillo, I. Egry, and R. Novakovic. Surface tension of liquid cu–ti binary alloys measured by electromagnetic levitation and thermodynamic modelling. Applied Surface Science, 257:7739-7745, Jun 2011. URL: https://doi.org/10.1016/j.apsusc.2011.04.019, doi:10.1016/j.apsusc.2011.04.019. This article has 64 citations and is from a domain leading peer-reviewed journal.

21. (amore2011surfacetensionof pages 4-5): S. Amore, J. Brillo, I. Egry, and R. Novakovic. Surface tension of liquid cu–ti binary alloys measured by electromagnetic levitation and thermodynamic modelling. Applied Surface Science, 257:7739-7745, Jun 2011. URL: https://doi.org/10.1016/j.apsusc.2011.04.019, doi:10.1016/j.apsusc.2011.04.019. This article has 64 citations and is from a domain leading peer-reviewed journal.

22. (jin2018experimentaldeterminationof pages 1-3): Bo Jin, Xing-Xu Lu, Shuli Liu, Dan-Dan Huang, and Yong Du. Experimental determination of phase equilibria at 900°c and liquidus surface in the cu-ni-ti system. Journal of Mining and Metallurgy, Section B: Metallurgy, 54:209-223, Jan 2018. URL: https://doi.org/10.2298/jmmb180209009j, doi:10.2298/jmmb180209009j. This article has 7 citations.

23. (tang2000phaseequilibriain pages 1-2): Weijia Tang, Rolf Sandström, and Shuichi Miyazaki. Phase equilibria in the pseudobinary ti0.5ni0.5-ti0.5cu0.5 system. Journal of Phase Equilibria, 21:227-234, May 2000. URL: https://doi.org/10.1361/105497100770340020, doi:10.1361/105497100770340020. This article has 25 citations.

24. (wang2018ahighthroughputsearch pages 3-7): Jianwei Wang, Xiao-lin Wei, Z. Chuan, Sun Lu, Guojie Huang, Jingmin Shi, and Wang Ligen. A high-throughput search for composition–phase–property relations of cu–ni/ti–al elastic copper alloys. Materials, 11:2513, Dec 2018. URL: https://doi.org/10.3390/ma11122513, doi:10.3390/ma11122513. This article has 1 citations.

25. (tang2000phaseequilibriain pages 2-3): Weijia Tang, Rolf Sandström, and Shuichi Miyazaki. Phase equilibria in the pseudobinary ti0.5ni0.5-ti0.5cu0.5 system. Journal of Phase Equilibria, 21:227-234, May 2000. URL: https://doi.org/10.1361/105497100770340020, doi:10.1361/105497100770340020. This article has 25 citations.

26. (jin2018experimentaldeterminationof pages 3-4): Bo Jin, Xing-Xu Lu, Shuli Liu, Dan-Dan Huang, and Yong Du. Experimental determination of phase equilibria at 900°c and liquidus surface in the cu-ni-ti system. Journal of Mining and Metallurgy, Section B: Metallurgy, 54:209-223, Jan 2018. URL: https://doi.org/10.2298/jmmb180209009j, doi:10.2298/jmmb180209009j. This article has 7 citations.

27. (alonso2025worldmineralsoutlook—cobalt pages 22-25): Elisa Alonso, Amanda Sarah Brioche, Ruth Schulte, Loyd M. Trimmer, Ji-Eun Kim, Andrew L. Gulley, and David George Pineault. World minerals outlook—cobalt, gallium, helium, lithium, magnesium, palladium, platinum, and titanium through 2029. Scientific Investigations Report, Jan 2025. URL: https://doi.org/10.3133/sir20255021, doi:10.3133/sir20255021. This article has 25 citations.

28. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

29. (tetsui2010evaluationofyttria pages 1-2): Toshimitsu Tetsui, Toshiharu Kobayashi, Takashi Mori, Tatsuya Kishimoto, and Hiroshi Harada. Evaluation of yttria applicability as a crucible for induction melting of tial alloy. Materials Transactions, 51:1656-1662, Sep 2010. URL: https://doi.org/10.2320/matertrans.maw201002, doi:10.2320/matertrans.maw201002. This article has 106 citations and is from a peer-reviewed journal.

30. (zhang2026effectoflowlevel pages 16-18): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.
