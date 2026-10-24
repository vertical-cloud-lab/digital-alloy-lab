<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 085e153b-3ea7-447c-9d2c-92d4bd6b7ce3
- Submitted: 2026-10-17T18:59:47Z
- Fetched: 2026-10-17T19:30:44Z (status: success)
- Raw trajectory JSON: ../raw/el-19-B.json.gz
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

ELEMENT UNDER REVIEW: B (strengthening addition). Boron-deoxidized copper; boron as a grain refiner in copper and aluminum bronze castings; borides with Ni, Fe, Cr; boron nitride crucibles and coatings.

Answer for B specifically, not for copper alloys in general:
1. ROLE: what B does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their B ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how B changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-B, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-B, Cu-Ni-B and Cu-Al-B are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of B in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that B neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | B | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: B (strengthening addition). Boron-deoxidized copper; boron as a grain refiner in copper and aluminum bronze castings; borides with Ni, Fe, Cr; boron nitride crucibles and coatings.

Answer for B specifically, not for copper alloys in general:
1. ROLE: what B does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their B ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how B changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-B, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-B, Cu-Ni-B and Cu-Al-B are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of B in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that B neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | B | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Boron (B) for pre-alloyed, seawater-service copper DED powder

**Decision: INCLUDE B as a tightly bounded *experimental grain-refining variable*, not as an established corrosion-improving addition.** The defensible evidence comes chiefly from cast brasses and other nonmarine copper alloys. I found no direct demonstration that B-bearing, single-stream laser DED Cu–Ni or nickel–aluminum bronze (NAB) is simultaneously crack-free and at least as seawater-resistant as as-deposited wrought C71500. Accordingly, the bounds below are **research-screening limits, not qualified marine-alloy specifications**. [GAP] (m.sadayappan2005grainrefinementof pages 8-10, rivero2021effectofti pages 1-2, zarebidaki2025evaluationofcorrosion pages 5-7)

The following table keeps the most informative bulk-alloy observations separate from coating results. (sampath2009influenceofminor pages 1-3, m.sadayappan2005grainrefinementof pages 52-60, zarebidaki2025evaluationofcorrosion pages 19-28)

| Family / evidence tier | B (wt%) | Measured outcome | Applicability to seawater DED |
|---|---:|---|---|
| C85800 cast yellow brass — indirect casting evidence | 0.0024 retained, with 0.010 Fe; refinement faded near 0.0004 B | Grain grade increased from base `<1–6` to `7.5`; refinement persisted through holding and remelting but was lost after dilution. Sadayappan et al., DOI: [10.2172/840819](https://doi.org/10.2172/840819). (m.sadayappan2005grainrefinementof pages 52-60) | Establishes a low functional B level for one brass, not Cu-Ni, NAB, DED, or seawater performance. |
| C89550 cast EnviroBrass III — indirect casting evidence | 0.0036 retained, with 0.013 Fe | Grain grade increased from `2` to `7.5`; retained B was 0.0035 after 6 h and 0.0028 after remelting. Sadayappan et al., DOI: [10.2172/840819](https://doi.org/10.2172/840819). (m.sadayappan2005grainrefinementof pages 52-60) | Supports ppm-level grain refinement in brass only; Fe-B hard particles become a concern at higher Fe. |
| Cu-12.5Al-5Mn shape-memory casting — experimental but nonmarine | 0.05–0.19 | About 80% grain-size reduction after homogenizing, rolling, betatizing, and step quenching; transformation temperatures rose while recoverable strain declined. Sampath and Mallik, DOI: [10.1051/esomat/200905028](https://doi.org/10.1051/esomat/200905028). (sampath2009influenceofminor pages 1-3, sampath2009influenceofminor pages 3-6) | Al-Mn evidence, but not NAB and not as-deposited; post-cast thermomechanical treatment prevents direct transfer to DED. |
| ZCuPb20Sn5-0.1P lead-tin bronze — experimental but nonmarine | 0.01–0.20; optimum 0.10 | At 0.10 B, lead-particle diameter fell from 30.0 to 24.8 µm, Ni4B3 formed, hardness reached 75 HB, and tensile strength reached about 244 MPa; above 0.10 B, coarse boride, shrinkage, and porosity appeared. Ren et al., DOI: [10.3390/ma14247806](https://doi.org/10.3390/ma14247806). (ren2021effectsofb pages 16-18, ren2021effectsofb pages 12-14) | Demonstrates a boride and porosity ceiling in a Ni-bearing bronze, but supplies no seawater, Cu-Ni, NAB, welding, or DED validation. |
| High-purity Cu casting — mechanistic, impractical concentration | 0.40 | Produced a columnar-to-equiaxed transition; B-rich B-C-O particles were implicated. Adding 0.15 P caused excessive equiaxed-grain coarsening. Balart et al., DOI: [10.1007/s11661-016-3671-8](https://doi.org/10.1007/s11661-016-3671-8). (balart2016grainrefinementof pages 1-2, balart2016grainrefinementof pages 11-12, balart2016grainrefinementof pages 13-17) | Far above practical marine-alloy bounds and equilibrium Cu solubility; graphite contact can form B4C. Not DED evidence. |
| B-refined yellow brass — nonchloride corrosion evidence | 0.001–0.002 | In 0.05 M KH2PO4/NaOH at pH 6 and 8, weight loss, polarization resistance, potentiodynamic response, and dezincification showed no conclusive improvement over B-free controls. Sadayappan et al., DOI: [10.2172/840819](https://doi.org/10.2172/840819). (m.sadayappan2005grainrefinementof pages 80-84, m.sadayappan2005grainrefinementof pages 84-92, m.sadayappan2005grainrefinementof pages 77-80) | Not seawater or NaCl; cannot establish B effects on marine pitting, crevice attack, erosion-corrosion, or selective attack. |
| Electroless Ni-B coating on Cu — chloride evidence, not bulk alloy | 6.0 in coating | In ASTM D1141 simulated seawater, corrosion current density was 5.5 × 10^-7 A/cm² and corrosion rate was 0.23 mpy, versus 1.2 × 10^-6 A/cm² and 0.54 mpy for Cu-10Ni. Zarebidaki and Dadras, preprint DOI: [10.21203/rs.3.rs-6881634/v1](https://doi.org/10.21203/rs.3.rs-6881634/v1). (zarebidaki2025evaluationofcorrosion pages 7-11, zarebidaki2025evaluationofcorrosion pages 19-28) | Surface-coating result only; it does not demonstrate that dilute B improves bulk Cu-Ni or NAB deposits or survives laser DED. |


*Table: Quantitative evidence for elemental boron in copper-based materials, separated by alloy family and evidence relevance. The table distinguishes bulk-alloy results from coating data and flags the absence of direct seawater DED validation.*

## 1. Role, alloy families, and specifications

**[CITE][NUMBERS] Cast brasses and bronzes.** In C85800 yellow brass, a melt containing **0.0024 wt% B and 0.010 wt% Fe** attained a grain-refinement rating of **7.5**, compared with a variable **<1–6** for the untreated melt; dilution to **0.0004 wt% B** lost refinement. C89550 EnviroBrass III gave a rating of **7.5 versus 2** with **0.0036 wt% B and 0.013 wt% Fe**. These are *measured experimental casting compositions*, not the UNS-prescribed B ranges. Earlier casting work also reports B with Ti, Fe/Co or Zr for gunmetal, tin bronze, iron-free aluminum bronze and β-brass; efficacy depends on the other elements and casting conditions. Silicon brass and silicon bronze did **not** respond to B as reliably as to Zr. M. Sadayappan *et al.*, *Grain Refinement of Permanent Mold Cast Copper Base Alloys*, technical report (2005), DOI **10.2172/840819**. (m.sadayappan2005grainrefinementof pages 8-10, m.sadayappan2005grainrefinementof pages 52-60, m.sadayappan2005grainrefinementof pages 19-23)

**[CITE][NUMBERS] Aluminum–manganese bronze, but not NAB.** Induction-melted Cu–**12.5 wt% Al–5 wt% Mn** with **0.05–0.19 wt% B** showed approximately **80% grain-size reduction**. The specimens were subsequently homogenized, hot rolled, betatized and quenched: neither the composition nor condition establishes performance of *as-deposited* C95800-type NAB. V. Sampath and U. S. Mallik, *ESOMAT* (2009), DOI **10.1051/esomat/200905028**. (sampath2009influenceofminor pages 1-3, sampath2009influenceofminor pages 3-6)

**[CITE][NUMBERS] Lead–tin bronze.** In experimental ZCuPb20Sn5–**0.1 wt% P** castings, additions of **0–0.2 wt% B** refined Cu-rich grains and decreased mean Pb-particle diameter from **30.0 to 24.8 μm** at **0.1 wt% B**. The authors attribute strengthening partly to dispersed **Ni₄B₃**: tensile strength reached approximately **244 MPa** and hardness **75 HB** at **0.1 wt% B**; at **0.2 wt% B**, coarse second phase and shrinkage/porosity accompanied deterioration. This is not evidence for the same phase fraction or optimum in ordinary marine Cu–Ni. X. Ren *et al.*, *Materials* **14**, 7806 (2021), DOI **10.3390/ma14247806**. (ren2021effectsofb pages 2-4, ren2021effectsofb pages 16-18, ren2021effectsofb pages 12-14)

**Mechanism.** B can consume dissolved oxygen to produce **B₂O₃**, suppressing Cu₂O-related casting porosity; segregate at solidification interfaces and restrict grain growth; and, depending on chemistry, enter B-rich particles or **Fe/Ni borides**. In graphite-contact melts, B-rich particles consistent with **B₄C** were observed. Its limited *equilibrium* solubility in Cu rules out assuming that useful deposited B remains entirely in solid solution. B-rich particles may help nucleation but can instead become hard inclusions; **grain refinement is not proof of corrosion protection**. M. J. Balart *et al.*, *Metallurgical and Materials Transactions A* **47**, 4988–5011 (2016), DOI **10.1007/s11661-016-3671-8**; A. Passerone *et al.*, *Surface Science* **603**, 2725–2733 (2009), DOI **10.1016/j.susc.2009.07.011**. (passerone2009thermodynamicsandsurface pages 1-2, balart2016grainrefinementof pages 1-2, balart2016grainrefinementof pages 12-13, balart2016grainrefinementof pages 13-17)

**[SPEC][NAVY][GAP] Commercial qualification.** The retrieved evidence does **not** establish a specified intentional B range for C95800 NAB, C71500/C70600 Cu–Ni, or AWS A5.7 **ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl**. Nor does it verify a numerical B maximum under ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726 or EN 12449. **Do not equate an unlisted B constituent with a specified zero-content or impurity maximum.** C85800 and C89550 above document foundry practice, *not* a B-bearing Navy specification. No B-specific protective seawater-film chemistry or demonstrated inhibition of dealloying in bulk NAB/Cu–Ni was identified. (m.sadayappan2005grainrefinementof pages 8-10, rivero2021effectofti pages 1-2, zarebidaki2025evaluationofcorrosion pages 5-7)

## 2. Seawater corrosion: what is, and is not, quantitative

**[GAP] Bulk-alloy evidence.** I found **no defensible B-addition-versus-B-free bulk Cu–Ni or NAB dataset** in natural seawater, ASTM D1141 water or **3.5 wt% NaCl**. Thus there is **no established B range that improves or harms** their corrosion rate, *E*₍corr₎, film resistance, pitting, crevice attack, selective attack, erosion-corrosion or allowable flow velocity. Likewise, no B-dependent 30-day attack depth or comparison with wrought C71500 is available. A reported copper-alloy effect cannot be inferred merely because a study calls conventional Cu–Ni “B10” or “B30”: those labels need to be checked against the alloy composition rather than read as B additions. (zarebidaki2025evaluationofcorrosion pages 5-7, zarebidaki2025evaluationofcorrosion pages 17-19, ren2021effectsofb pages 2-4)

**[CITE][NUMBERS] Nonseawater bulk comparison.** Sadayappan *et al.* tested yellow brasses containing **0 versus 0.001–0.002 wt% B** in **0.05 M phosphate buffer**, not seawater: polarization resistance at pH 6 was **2.89 versus 4.62 kΩ** (untreated versus refined), but at pH 8 it was **10.02 versus 7.40 kΩ**. After **120 days at pH 6**, mass loss was **0.378 versus 0.408 mg cm⁻²**. Their separate **17-day FeCl₃/CuSO₄/HCl** dezincification test also gave no conclusive advantage to grain refinement. These mixed outcomes neither demonstrate chloride-seawater protection nor isolate grain size from B/Fe chemistry. DOI **10.2172/840819**. (m.sadayappan2005grainrefinementof pages 80-84, m.sadayappan2005grainrefinementof pages 84-92, m.sadayappan2005grainrefinementof pages 77-80)

**[CITE][NUMBERS] Important non-equivalent comparator.** An **electroless Ni–6 wt% B coating on pure Cu**, *not* B alloyed into Cu, yielded *i*₍corr₎ **5.5 × 10⁻⁷ A cm⁻²**, *E*₍corr₎ **−0.330 V versus Ag/AgCl**, and a reported **0.23 mpy**; uncoated Cu–**10 wt% Ni** yielded **1.2 × 10⁻⁶ A cm⁻²** and **0.54 mpy**. The paper describes ASTM D1141 simulated seawater but labels its numerical tables **3.5 wt% NaCl**; that electrolyte discrepancy should be resolved before reuse. Neither coating composition nor its corrosion advantage predicts the response of dilute B in a Cu-balanced DED deposit. A. Zarebidaki and D. Dadras, **2025 preprint**, DOI **10.21203/rs.3.rs-6881634/v1**. (zarebidaki2025evaluationofcorrosion pages 1-5, zarebidaki2025evaluationofcorrosion pages 7-11, zarebidaki2025evaluationofcorrosion pages 19-28)

## 3. DED, repair welding, and powder making

**[GAP] DED and filler metals.** No retrieved controlled study measures B-induced **solidification cracking, reheated-layer liquation cracking, deposited porosity, laser evaporation/oxidation loss, or NAB/Cu–Ni substrate dilution** for the proposed powder and laser. Nor do the retrieved AWS filler data supply a B-bearing filler qualification that could substitute for such a study. Casting offers a *mechanistic warning*, not a DED crack threshold: in B-refined brass, hard B/Fe-rich particles appeared above approximately **0.05–0.06 wt% Fe**, and B above an approximately **0.02 wt% casting optimum** coarsened rather than refined grains. NAB already contains far more Fe than that brass; **transferring the numerical Fe threshold to NAB would be invalid**, but Fe–B particle formation is a high-priority risk to test. Repeated remelting and dilution require examination of both fusion boundaries and reheated interlayers. DOI **10.2172/840819**. (m.sadayappan2005grainrefinementof pages 72-77, m.sadayappan2005grainrefinementof pages 65-68)

**[CITE][NUMBERS] Melt and atomization risks.** The brass report measured only approximately **50% recovery** of the initially added B from a Cu–**2 wt% B master alloy** under its foundry conditions; this is **not** an atomizer-specific recovery factor. A Cu–**12.5 wt% Al–5 wt% Mn** series was made as **0.5 kg**, Ar-protected induction melts using B master alloy, demonstrating charge-scale feasibility but not ultrasonic atomization or powder cleanliness. B's oxygen affinity and surface activity make powder-oxide/inclusion formation and variable retained B plausible. In graphite-contact copper, a **0.4 wt% B** addition produced B/C/O-rich particles consistent with carbide formation; avoid assuming graphite and alumina/zirconia have interchangeable reactions. Experimental Cu–B liquid surface-tension measurements exist only at much higher B concentration, **10 at% B, approximately 1.86 wt% B**, and cannot quantify the droplet behavior of the proposed dilute multicomponent powder. No measured B pickup or loss from **alumina, zirconia, BN coatings/crucibles, or Ti-alloy/Mo sonotrodes**, or quantitative B-specific laser-fume loss, was found; BN should **not** be treated as chemically invisible. DOI **10.2172/840819**; DOI **10.1051/esomat/200905028**; DOI **10.1007/s11661-016-3671-8**; DOI **10.1016/j.susc.2009.07.011**. (sampath2009influenceofminor pages 1-3, m.sadayappan2005grainrefinementof pages 65-68, passerone2009thermodynamicsandsurface pages 2-3, passerone2009thermodynamicsandsurface pages 1-2, balart2016grainrefinementof pages 4-7, balart2016grainrefinementof pages 13-17)

## 4. Phase diagram and CALPHAD

**[CITE][NUMBERS] Cu–B, not a high-liquidus obstacle at trace additions.** Cu–B has a **Cu-rich eutectic near 1,013–1,014 °C** between Cu-rich FCC and B-rich solid, with **no assessed binary Cu–B intermetallic**. The reported experimental maximum B solubility in FCC Cu is about **0.05 wt%**; one assessed maximum is **0.08 wt% near the eutectic (~1,000–1,014 °C)**, decreasing to **<1 wt ppm** at room temperature. A later bronze article's claim of **0.06 wt% room-temperature and 0.53 wt% maximum** B solubility conflicts with this assessed phase-diagram account; do **not** use those figures for design. H. Magnusson, *Thermodynamic Evaluation of Impurity Elements in OFP Copper*, SKB report **R-17-20** (2017; no DOI established in the retrieved record); J. Miettinen, V.-V. Visuri and T. Fabritius, *Archives of Metallurgy and Materials* **66**, 297–304 (2021), DOI **10.24425/amm.2021.134787**. (magnusson2017thermodynamicevaluationof pages 12-14, magnusson2017thermodynamicevaluationof pages 32-36, ren2021effectsofb pages 2-4, miettinen2021thermodynamicdescriptionof pages 1-2, miettinen2021thermodynamicdescriptionof pages 2-3)

**[CITE] Fig. 4** in Miettinen *et al.* shows the **Cu-rich liquidus falling**, not rising, over the dilute-B interval; **0.002–0.05 wt% B alone cannot reasonably be claimed to drive binary Cu above the approximately 1,250 °C atomization threshold**. That statement does **not** certify the liquidus of a specific Ni/Fe/Al-containing design: calculate it for every candidate and measure it if it approaches the equipment limit. Cu–B was assessed by multiple groups, and published parameters for **Fe–Cu–B** include FeB and Fe₂B; the latter are *ternary-system Fe borides, not Cu–B compounds*. Published assessment does **not** establish that a particular installed **Thermo-Calc TCCU** version contains validated Cu–Ni–B and Cu–Al–B ternaries, or that COST 531 supplies them. Inspect the database's element/phase coverage and parameter provenance; pycalphad requires the actual compatible TDB rather than extrapolation presented as validation. DOI **10.24425/amm.2021.134787**. (miettinen2021thermodynamicdescriptionof pages 1-2, miettinen2021thermodynamicdescriptionof pages 2-3, miettinen2021thermodynamicdescriptionof pages 3-7, miettinen2021thermodynamicdescriptionof media 48d764b7)

## 5. Supply, safety, bounds, and interactions

**[NAVY][CITE] Criticality.** **B was added to the final US 2025 critical-minerals list; it was not on the 2022 list.** The 2025 list also names Cu and Ni. USGS authors, *USGS Critical Minerals Review* (2026), citing the final 2025 Federal Register list, document **2025-19813**. A reliable **USD kg⁻¹ elemental B or Cu–B-master-alloy procurement price** was not established by the retrieved evidence; borate-ore prices would be a misleading substitute. (iii2026usgscriticalminerals pages 1-2)

**[GAP] Health and compliance.** No verified B-specific OSHA occupational limit, RoHS/REACH classification applicable to the *elemental B-bearing alloy*, or B-specific Navy prohibition was established here. Do not transfer classifications of **boric acid/borates** wholesale to elemental B, B₂O₃, BN or a finished copper alloy. Require supplier SDS review and controls for respirable powder, combustible-metal dust and laser-generated Cu/Ni/B-bearing fumes; B-containing oxide fume and cross-contamination merit measurement, not an invented exposure limit. (passerone2009thermodynamicsandsurface pages 1-2, passerone2009thermodynamicsandsurface pages 6-7)

**Proposed search-space bounds—B in the *retained powder and deposit*, all compositions wt%.** [NUMBERS]

| Bound | Al-bronze | Cu–Ni | Basis and bound-setting failure mode |
|---|---:|---:|---|
| Functional floor | **0.002** | **0.002**, *unproven transfer* | Roughly **20 wt ppm** gave measurable grain-rating change in cast Cu–Zn; below this, treatment may fade or be swamped by recovery/analytical variation. There is **no established Cu–Ni or NAB functional floor**. (m.sadayappan2005grainrefinementof pages 19-23, m.sadayappan2005grainrefinementof pages 92-102) |
| Conservative maximum | **0.020** | **0.010** | **Research limits, not commercial/Navy precedents**: about **0.020** was a reported casting optimum before brass grain coarsening, while the Cu–Ni ceiling is reduced because Ni borides/DED behavior are unqualified. Risk: hard borides, hot cracking and heterogeneity; Fe-rich NAB particularly requires direct testing. (m.sadayappan2005grainrefinementof pages 65-68, ren2021effectsofb pages 16-18) |
| Non-conservative maximum | **0.050** | **0.020** | **Experimental-only**: **0.05** is the lower end of the Cu–Al–Mn grain-refinement series and approximately the experimentally reported *maximum equilibrium solubility in binary Cu*, **not** a guarantee of solubility in either multicomponent alloy. Cu–Ni is held lower pending boride, crack and seawater tests. Risk: segregation/particles, porosity and loss of ductility or corrosion resistance. (sampath2009influenceofminor pages 1-3, magnusson2017thermodynamicevaluationof pages 32-36, ren2021effectsofb pages 16-18) |

These asymmetric maxima are **engineering hypotheses**, especially for Cu–Ni; **no commercially or Navy-qualified B-bearing seawater alloy establishes a conservative upper bound**. If the composition palette requires *only* previously qualified marine-alloy bounds, B should instead be omitted from the initial qualification subset. The Cu–Al–Mn **0.19 wt% B** experiment and Pb–Sn bronze **0.1 wt% B** strength optimum cannot justify either as an as-deposited NAB/Cu–Ni seawater bound. For **LIMIT** or **EXCLUDE**, an impurity maximum is inapplicable to this chosen decision; no source-verified B impurity maximum for the requested DED powder/deposit was found. (sampath2009influenceofminor pages 1-3, ren2021effectsofb pages 16-18, zarebidaki2025evaluationofcorrosion pages 5-7)

**Interactions for joint constraints.** [CITE][GAP] Treat **retained B**, rather than B charged to the melt, as the independent variable. Track **Fe × B** and **Ni × B** against boride particles; B₂O₃ formation against oxygen removal and oxide inclusions; **B × C** against B₄C with graphite contact; and **B × P** against altered inoculants—**0.4 wt% B plus 0.15 wt% P** produced excessive grain coarsening where **0.4 wt% B without P** showed a columnar-to-equiaxed transition. **Al/Mn/B** coupling is suggested by Cu–Al–Mn experiments, but no validated sum or atomic-ratio constraint for C95800 or C71500 emerges from them. In a brass experiment **0.05–0.06 wt% Fe** marked B/Fe hard-spot onset; this is a *brass-specific warning*, **not** a permissible NAB Fe/B ratio. No demonstrated B-driven substitution for the Ni required to form the seawater-protective Cu–Ni film was found. DOI **10.2172/840819**; DOI **10.1007/s11661-016-3671-8**; DOI **10.1051/esomat/200905028**. (m.sadayappan2005grainrefinementof pages 72-77, m.sadayappan2005grainrefinementof pages 65-68, balart2016grainrefinementof pages 11-12, balart2016grainrefinementof pages 13-17, sampath2009influenceofminor pages 1-3, zarebidaki2025evaluationofcorrosion pages 1-5)

**Evidence quality: thin for the proposal's decisive endpoints.** Grain-size and selected particle/strength findings are quantitative, but mainly casting- or heat-treatment-derived; the chloride data concern a **Ni–B surface coating**, not a B-alloyed deposit. There is neither an established B-specific seawater benefit nor a DED crack/corrosion threshold, specification maximum, atomizer recovery, or qualified crucible/sonotrode compatibility. B should remain in the design only if composition-resolved B recovery, particle/crack mapping, and **as-deposited** self-build and substrate-repair seawater testing are explicit go/no-go measurements. (sampath2009influenceofminor pages 1-3, m.sadayappan2005grainrefinementof pages 8-10, zarebidaki2025evaluationofcorrosion pages 19-28, zarebidaki2025evaluationofcorrosion pages 5-7)

VERDICT | B | decision=INCLUDE | family=both | conservative_max_wt=0.020 | nonconservative_max_wt=0.050 | floor_wt=0.002 | impurity_max_wt=NA | evidence=thin

References

1. (m.sadayappan2005grainrefinementof pages 8-10): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

2. (rivero2021effectofti pages 1-2): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

3. (zarebidaki2025evaluationofcorrosion pages 5-7): Arman Zarebidaki and Danesh Dadras. Evaluation of corrosion resistance of cu, cu-10 wt% ni, cu-20 wt% ni, and electroless ni-b and ni-p coatings in simulated seawater. Unknown journal, Jun 2025. URL: https://doi.org/10.21203/rs.3.rs-6881634/v1, doi:10.21203/rs.3.rs-6881634/v1.

4. (sampath2009influenceofminor pages 1-3): V. Sampath and U. S. Mallik. Influence of minor additions of boron and zirconium on shape memory properties and grain refinement of a cu-al-mn shape memory alloy. ArXiv, pages 05028, Jan 2009. URL: https://doi.org/10.1051/esomat/200905028, doi:10.1051/esomat/200905028. This article has 21 citations.

5. (m.sadayappan2005grainrefinementof pages 52-60): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

6. (zarebidaki2025evaluationofcorrosion pages 19-28): Arman Zarebidaki and Danesh Dadras. Evaluation of corrosion resistance of cu, cu-10 wt% ni, cu-20 wt% ni, and electroless ni-b and ni-p coatings in simulated seawater. Unknown journal, Jun 2025. URL: https://doi.org/10.21203/rs.3.rs-6881634/v1, doi:10.21203/rs.3.rs-6881634/v1.

7. (sampath2009influenceofminor pages 3-6): V. Sampath and U. S. Mallik. Influence of minor additions of boron and zirconium on shape memory properties and grain refinement of a cu-al-mn shape memory alloy. ArXiv, pages 05028, Jan 2009. URL: https://doi.org/10.1051/esomat/200905028, doi:10.1051/esomat/200905028. This article has 21 citations.

8. (ren2021effectsofb pages 16-18): Xiaoyan Ren, Guowei Zhang, Hong Xu, Zhaojie Wang, Yijun Liu, Fenger Sun, Yuanyuan Kang, Mingjie Wang, Weize Lv, and Zhi Yin. Effects of b on the structure and properties of lead-tin bronze alloy and the mechanism of strengthening and toughening. Materials, 14:7806, Dec 2021. URL: https://doi.org/10.3390/ma14247806, doi:10.3390/ma14247806. This article has 20 citations.

9. (ren2021effectsofb pages 12-14): Xiaoyan Ren, Guowei Zhang, Hong Xu, Zhaojie Wang, Yijun Liu, Fenger Sun, Yuanyuan Kang, Mingjie Wang, Weize Lv, and Zhi Yin. Effects of b on the structure and properties of lead-tin bronze alloy and the mechanism of strengthening and toughening. Materials, 14:7806, Dec 2021. URL: https://doi.org/10.3390/ma14247806, doi:10.3390/ma14247806. This article has 20 citations.

10. (balart2016grainrefinementof pages 1-2): María José Balart, Jayesh B. Patel, Feng Gao, and Zhongyun Fan. Grain refinement of deoxidized copper. Metallurgical and Materials Transactions A, 47:4988-5011, Aug 2016. URL: https://doi.org/10.1007/s11661-016-3671-8, doi:10.1007/s11661-016-3671-8. This article has 57 citations.

11. (balart2016grainrefinementof pages 11-12): María José Balart, Jayesh B. Patel, Feng Gao, and Zhongyun Fan. Grain refinement of deoxidized copper. Metallurgical and Materials Transactions A, 47:4988-5011, Aug 2016. URL: https://doi.org/10.1007/s11661-016-3671-8, doi:10.1007/s11661-016-3671-8. This article has 57 citations.

12. (balart2016grainrefinementof pages 13-17): María José Balart, Jayesh B. Patel, Feng Gao, and Zhongyun Fan. Grain refinement of deoxidized copper. Metallurgical and Materials Transactions A, 47:4988-5011, Aug 2016. URL: https://doi.org/10.1007/s11661-016-3671-8, doi:10.1007/s11661-016-3671-8. This article has 57 citations.

13. (m.sadayappan2005grainrefinementof pages 80-84): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

14. (m.sadayappan2005grainrefinementof pages 84-92): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

15. (m.sadayappan2005grainrefinementof pages 77-80): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

16. (zarebidaki2025evaluationofcorrosion pages 7-11): Arman Zarebidaki and Danesh Dadras. Evaluation of corrosion resistance of cu, cu-10 wt% ni, cu-20 wt% ni, and electroless ni-b and ni-p coatings in simulated seawater. Unknown journal, Jun 2025. URL: https://doi.org/10.21203/rs.3.rs-6881634/v1, doi:10.21203/rs.3.rs-6881634/v1.

17. (m.sadayappan2005grainrefinementof pages 19-23): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

18. (ren2021effectsofb pages 2-4): Xiaoyan Ren, Guowei Zhang, Hong Xu, Zhaojie Wang, Yijun Liu, Fenger Sun, Yuanyuan Kang, Mingjie Wang, Weize Lv, and Zhi Yin. Effects of b on the structure and properties of lead-tin bronze alloy and the mechanism of strengthening and toughening. Materials, 14:7806, Dec 2021. URL: https://doi.org/10.3390/ma14247806, doi:10.3390/ma14247806. This article has 20 citations.

19. (passerone2009thermodynamicsandsurface pages 1-2): A. Passerone, M. L. Muolo, F. Valenza, and R. Novakovic. Thermodynamics and surface properties of liquid cu-b alloys. Surface Science, 603:2725-2733, Sep 2009. URL: https://doi.org/10.1016/j.susc.2009.07.011, doi:10.1016/j.susc.2009.07.011. This article has 19 citations and is from a peer-reviewed journal.

20. (balart2016grainrefinementof pages 12-13): María José Balart, Jayesh B. Patel, Feng Gao, and Zhongyun Fan. Grain refinement of deoxidized copper. Metallurgical and Materials Transactions A, 47:4988-5011, Aug 2016. URL: https://doi.org/10.1007/s11661-016-3671-8, doi:10.1007/s11661-016-3671-8. This article has 57 citations.

21. (zarebidaki2025evaluationofcorrosion pages 17-19): Arman Zarebidaki and Danesh Dadras. Evaluation of corrosion resistance of cu, cu-10 wt% ni, cu-20 wt% ni, and electroless ni-b and ni-p coatings in simulated seawater. Unknown journal, Jun 2025. URL: https://doi.org/10.21203/rs.3.rs-6881634/v1, doi:10.21203/rs.3.rs-6881634/v1.

22. (zarebidaki2025evaluationofcorrosion pages 1-5): Arman Zarebidaki and Danesh Dadras. Evaluation of corrosion resistance of cu, cu-10 wt% ni, cu-20 wt% ni, and electroless ni-b and ni-p coatings in simulated seawater. Unknown journal, Jun 2025. URL: https://doi.org/10.21203/rs.3.rs-6881634/v1, doi:10.21203/rs.3.rs-6881634/v1.

23. (m.sadayappan2005grainrefinementof pages 72-77): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

24. (m.sadayappan2005grainrefinementof pages 65-68): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.

25. (passerone2009thermodynamicsandsurface pages 2-3): A. Passerone, M. L. Muolo, F. Valenza, and R. Novakovic. Thermodynamics and surface properties of liquid cu-b alloys. Surface Science, 603:2725-2733, Sep 2009. URL: https://doi.org/10.1016/j.susc.2009.07.011, doi:10.1016/j.susc.2009.07.011. This article has 19 citations and is from a peer-reviewed journal.

26. (balart2016grainrefinementof pages 4-7): María José Balart, Jayesh B. Patel, Feng Gao, and Zhongyun Fan. Grain refinement of deoxidized copper. Metallurgical and Materials Transactions A, 47:4988-5011, Aug 2016. URL: https://doi.org/10.1007/s11661-016-3671-8, doi:10.1007/s11661-016-3671-8. This article has 57 citations.

27. (magnusson2017thermodynamicevaluationof pages 12-14): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

28. (magnusson2017thermodynamicevaluationof pages 32-36): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

29. (miettinen2021thermodynamicdescriptionof pages 1-2): Jyrki Miettinen, Ville-Valtteri Visuri, and Timo Fabritius. Thermodynamic description of ternary fe-b-x systems. part 9: fe-b-cu. Archives of Metallurgy and Materials, pages 297-304, Dec 2021. URL: https://doi.org/10.24425/amm.2021.134787, doi:10.24425/amm.2021.134787. This article has 5 citations and is from a peer-reviewed journal.

30. (miettinen2021thermodynamicdescriptionof pages 2-3): Jyrki Miettinen, Ville-Valtteri Visuri, and Timo Fabritius. Thermodynamic description of ternary fe-b-x systems. part 9: fe-b-cu. Archives of Metallurgy and Materials, pages 297-304, Dec 2021. URL: https://doi.org/10.24425/amm.2021.134787, doi:10.24425/amm.2021.134787. This article has 5 citations and is from a peer-reviewed journal.

31. (miettinen2021thermodynamicdescriptionof pages 3-7): Jyrki Miettinen, Ville-Valtteri Visuri, and Timo Fabritius. Thermodynamic description of ternary fe-b-x systems. part 9: fe-b-cu. Archives of Metallurgy and Materials, pages 297-304, Dec 2021. URL: https://doi.org/10.24425/amm.2021.134787, doi:10.24425/amm.2021.134787. This article has 5 citations and is from a peer-reviewed journal.

32. (miettinen2021thermodynamicdescriptionof media 48d764b7): Jyrki Miettinen, Ville-Valtteri Visuri, and Timo Fabritius. Thermodynamic description of ternary fe-b-x systems. part 9: fe-b-cu. Archives of Metallurgy and Materials, pages 297-304, Dec 2021. URL: https://doi.org/10.24425/amm.2021.134787, doi:10.24425/amm.2021.134787. This article has 5 citations and is from a peer-reviewed journal.

33. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

34. (passerone2009thermodynamicsandsurface pages 6-7): A. Passerone, M. L. Muolo, F. Valenza, and R. Novakovic. Thermodynamics and surface properties of liquid cu-b alloys. Surface Science, 603:2725-2733, Sep 2009. URL: https://doi.org/10.1016/j.susc.2009.07.011, doi:10.1016/j.susc.2009.07.011. This article has 19 citations and is from a peer-reviewed journal.

35. (m.sadayappan2005grainrefinementof pages 92-102): M.Sadayappan, J.P.Thomson, M.Elboujdaini, G.Ping Gu, and M. Sahoo. Grain refinement of permanent mold cast copper base alloys. ArXiv, Apr 2005. URL: https://doi.org/10.2172/840819, doi:10.2172/840819. This article has 58 citations.
