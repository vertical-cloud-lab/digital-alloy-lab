<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 3be91072-c969-4110-9549-cc3c259b6311
- Submitted: 2026-10-17T18:58:43Z
- Fetched: 2026-10-17T19:27:55Z (status: success)
- Raw trajectory JSON: ../raw/el-06-Cr.json.gz
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

ELEMENT UNDER REVIEW: Cr (major seawater addition). C72200 (Cu-16Ni-0.5Cr), cast CuNi30Cr2 (e.g. IN-768 type, up to about 2-3 Cr), Cu-Cr precipitation alloys C18200 (about 1 Cr). Solubility of Cr in Cu is small (under 1 wt% at the eutectic). Reported to raise erosion-corrosion resistance of Cu-Ni but to pit in still seawater.

Answer for Cr specifically, not for copper alloys in general:
1. ROLE: what Cr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Cr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Cr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Cr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Cr, Cu-Ni-Cr and Cu-Al-Cr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Cr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Cr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Cr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Cr (major seawater addition). C72200 (Cu-16Ni-0.5Cr), cast CuNi30Cr2 (e.g. IN-768 type, up to about 2-3 Cr), Cu-Cr precipitation alloys C18200 (about 1 Cr). Solubility of Cr in Cu is small (under 1 wt% at the eutectic). Reported to raise erosion-corrosion resistance of Cu-Ni but to pit in still seawater.

Answer for Cr specifically, not for copper alloys in general:
1. ROLE: what Cr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Cr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Cr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Cr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Cr, Cu-Ni-Cr and Cu-Al-Cr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Cr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Cr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Cr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Chromium in pre-alloyed copper powder for seawater DED

**Decision: INCLUDE Cr as a designed variable in the Cu–Ni branch, not as an assumed improvement to NAB.** [CITE] A Cu–Ni alloy containing approximately **0.5 wt% Cr** has unusually good resistance to flowing-seawater impingement. That result does **not** establish the proposal’s more demanding endpoint: an **as-deposited**, crack-free, single-stream repair alloy whose still-water and localized corrosion are at least as good as wrought C71500. Indeed, another Cr-modified Cu–Ni performed worse than C71500 in low-flow crevice tests. Cr is therefore a high-value *experimental factor*, not a proven substitute for Ni or a qualification shortcut. The ranges below are proposed **feedstock compositions in wt%; Cu is the balance**, not guaranteed deposited compositions. (din1993effectofresidual pages 4-7, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48)

The principal evidence and its limits are collected here. (din1993effectofresidual pages 4-7, zhao2022thelaserdeposited pages 7-10, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48, zhao2022thelaserdeposited pages 4-7)

| Evidence or decision point | Alloy family | Cr (wt%) | Quantitative finding | Interpretation / limitation | Evidence grade |
|---|---:|---:|---|---|---|
| C72200 (Cu–15Ni–0.8Fe–Cr) | Cu–Ni | 0.5 | Chromium additions as low as 0.5 increased localized-impingement resistance. C72200 showed a critical velocity of 12.0 m/s and critical shear stress of 2969 dyn/cm², versus 4.1 m/s and 479 dyn/cm² for C71500; accepted tubular design velocity was >9.0 m/s versus 4.6 m/s. (din1993effectofresidual pages 4-7, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel media c5fcc684) | Strong proof of benefit under high-flow seawater. Proposed mechanism: Cr incorporation strengthens the Fe-rich protective oxide film. (din1993effectofresidual pages 4-7) | Strong for erosion–corrosion |
| C72200 stagnant-water caveat | Cu–Ni | 0.5 | Quiet seawater: 0.4–0.9 mpy general corrosion and 1 mil pitting, versus C71500 at 0.3–0.5 mpy and 1–2 mil pitting. (lewis1981evaluationofcoppernickel pages 43-48) | Does not show a general-corrosion advantage over C71500 in stagnant seawater; the principal demonstrated benefit is film retention under flow. | Moderate |
| C71900 / cast IN768 | Cu–Ni | **NOT VERIFIED** | C71900 gave 1.3, 3.1 and 5.3 mpy at 9.5, 26.3 and 51.5 ft/s, versus C71500 at 2.7, 24.6 and 44.5 mpy. At low/no flow, however, C71900 had greater localized and crevice attack than C71500. (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48) | Higher-Cr Cu–Ni is promising for erosion–corrosion but can be worse in shielded/stagnant conditions. The retrieved sources did **not** verify the Cr specification for C71900/IN768, so they cannot independently justify a numerical composition bound. | Moderate performance evidence; thin composition evidence |
| Laser-deposited NAB over Ni–20Cr underlayer | Al-bronze / NAB | 1.9 in deposited top region | After 21 days in 3.5 wt% NaCl, maximum attack was 1.8 ± 0.1 µm with the Ni–Cr underlayer versus 2.0 ± 0.1 µm with the Ni-only underlayer; corresponding currents were 4.09 and 4.65 µA/cm². The nominal NAB powder contained no Cr; dilution produced 1.9 wt% Cr in the upper deposited region. (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 4-7, zhao2022thelaserdeposited pages 2-4) | **Not independent proof of pre-alloyed Cr in NAB:** Ni, interlayer chemistry, dilution and microstructure changed simultaneously. The small 1.8-versus-2.0 µm difference does not establish a standalone Cr benefit or an NAB design bound. | Thin / confounded |
| Cu–Cr eutectic datum | Cu–Cr binary | 1.27 | Reported eutectic reaction at 1076 °C and 1.27 wt% Cr. (zhao2022thelaserdeposited pages 4-7) | This is the **eutectic composition**, not the maximum equilibrium solid solubility of Cr in Cu. It must not be used as a solubility bound. | Moderate |
| Recommended functional floor | Cu–Ni only | **0.5** | Smallest retrieved addition with a demonstrated measurable seawater effect: marked improvement in localized impingement resistance. (din1993effectofresidual pages 4-7) | Floor is set by demonstrated erosion–corrosion benefit, not by stagnant-seawater superiority. | Moderate–strong |
| Recommended conservative maximum | Cu–Ni only | **0.5** | Matches C72200 and retains direct commercial-service and quantitative high-flow evidence. (din1993effectofresidual pages 4-7, lewis1981evaluationofcoppernickel pages 48-55) | Failure mode above this bound: increasing Cr-rich segregation/eutectic or oxide burden without demonstrated improvement in stagnant seawater or as-deposited DED corrosion. | Moderate |
| Recommended exploratory maximum | Cu–Ni only | **2.0** | Brackets the reported higher-Cr cast Cu–Ni class while remaining an explicitly experimental search bound. | **Aggressive and unqualified:** 2.0 wt% Cr is not proven here to equal wrought C71500 in stagnant seawater, and the retrieved sources did not verify the C71900/IN768 Cr specification. Failure modes are crevice/pitting attack, Cr-rich segregation, oxide skin and uncertain liquidus/atomization behavior. | Thin |
| NAB search decision | Al-bronze / NAB | Do not assign from current evidence | The only quantitative NAB result used Cr supplied by a Ni–20Cr underlayer rather than pre-alloyed NAB powder. (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 4-7) | Keep Cr out of the primary NAB palette until composition-controlled, single-stream DED comparisons establish cracking, dilution and as-deposited seawater behavior. | Thin |


*Table: Evidence-graded comparison separating proven Cu–Ni erosion–corrosion benefits from confounded NAB cladding results and phase-diagram facts. It supports a Cu–Ni-only search interval of 0.5–2.0 wt% Cr, with 2.0 wt% explicitly exploratory.*

## 1. Role, alloy families, and identifiable products

- **Cu–Ni:** [CITE] [NUMBERS] In the reported C72200/IN-838 composition, **Ni 15, Fe 0.8, Cr 0.5 wt%**, Cr greatly improves resistance to *localized impingement*. Incorporation of Cr into an Fe-containing protective oxide is a proposed explanation, not a demonstrated quantitative film composition or proof of stainless-steel-like Cr₂O₃ passivation. Ni and Fe also affect the defect chemistry and resistance of the underlying Cu₂O-based film; preserving useful Fe while varying Cr is essential. The historical review identifies C71900 and its cast counterpart **IN-768** as Cr-modified Cu–Ni, but the retrieved primary material does **not verify their specification limits in wt% Cr**. Do not label an assumed “CuNi30Cr2” value as an ASTM-certified C71900/IN-768 range. *El Din, “Effect of residual and minor constituents on the corrosion behaviour of some technically important alloys,”* **Desalination** 93 (1993) 487–498, doi:**10.1016/0011-9164(93)80124-6**; Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications* (1981), doi:**10.2172/6255887**. (din1993effectofresidual pages 4-7, lewis1981evaluationofcoppernickel pages 17-19)
- **Aluminum bronze/NAB:** [CITE] [NUMBERS] An infrared-laser-deposited NAB layer above a **Ni–20 wt% Cr** interlayer acquired **1.9 wt% Cr** in an analyzed upper region. Importantly, its NAB feed powder contained **no specified Cr**: **Cu 81.1, Al 10.8, Ni 4.1, Fe 4.0 wt%**. This is evidence that Cr can enter deposited NAB through dilution and coexist with its α, retained β′, and κ microstructures—not a commercial Cr-bearing NAB specification, controlled Cr addition, or demonstrated dealloying inhibitor. Zhao *et al.*, “The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution,” **Metals** 12 (2022) 781, doi:**10.3390/met12050781**. (zhao2022thelaserdeposited pages 4-7, zhao2022thelaserdeposited pages 2-4)
- **Other Cu families:** [GAP] C18200/CuCr1-type precipitation-hardening Cu–Cr and the studied CuNi2SiCr/C18000 class establish *processing* interest in Cr, not seawater equivalence to C71500. Cr-rich precipitation can strengthen aged Cu alloys, but a strength gain dependent on aging cannot be credited to this **no-post-build-heat-treatment** design. The retrieved sources do not substantiate a Cr-containing Navy-grade **Mn–Al bronze, tin bronze/gunmetal, or brass**, nor Cr-induced grain refinement, deoxidation, inhibition of dezincification/dealuminification, or a Cr-bearing AWS seawater filler with a verified composition. In particular, the documented inhibitors in the historical examples are **As** for selective attack and Al or Sn-derived films—not Cr. Do not transfer their benefits to Cr. Polkam, *Laser Powder Bed Fusion of CuNi2SiCr Alloy* (2022; thesis, DOI not established in the retrieved record); El Din (1993), doi:**10.1016/0011-9164(93)80124-6**. (din1993effectofresidual pages 4-7, polkam2022laserpowderbed pages 1-5, batawi1993microstructuraldesignand pages 65-68)

**Specifications:** [SPEC] The designations C72200 and C71900 above identify commercial alloy classes, **not independently checked numerical ASTM composition limits**. The available evidence does not establish a Cr requirement or allowable Cr range in **ASTM B111/B171/B466/B148/B369; MIL-T-16420, MIL-B-24480, MIL-C-15726; AWS A5.7; or EN 12449**. Neither conventional C95800 NAB nor C71500 should be described as a specified Cr-bearing alloy on this record. Obtain controlled editions and a chemical certificate before invoking one of those standards as a bound. In particular, AWS Cu–Ni and Al-bronze filler *families* do not by themselves validate Cr-containing **ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl** filler compositions. (din1993effectofresidual pages 4-7, beaver1978stateoftheartsurveyof pages 60-64, beaver1978stateoftheartsurveyof pages 39-44, zhao2022thelaserdeposited pages 2-4)

## 2. Seawater corrosion: benefit and counterexample

**Flowing water—substantial benefit.** [CITE] [NUMBERS] The DOE compilation reports C72200’s **critical velocity 12.0 m/s** and **critical wall shear 2,969 dyn/cm²**, versus C71500’s **4.1 m/s** and **479 dyn/cm²**. Listed *accepted tubular design velocities* are **>9.0 versus 4.6 m/s**; these are tube-service figures, **not** approved velocities for a DED repair. In another multi-velocity-jet comparison, C71900 versus C71500 corrosion rates were **1.3 versus 2.7 mpy at 9.5 ft/s**, **3.1 versus 24.6 mpy at 26.3 ft/s**, and **5.3 versus 44.5 mpy at 51.5 ft/s**. The same compilation reports no measurable impingement on the Cr-modified C72200 and C71900 at or below **4.6 m/s** in particular jet tests. Lewis and LaQue (1981), doi:**10.2172/6255887**. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel media c5fcc684, lewis1981evaluationofcoppernickel media 3f6e8440)

**Quiet water and crevices—the qualification risk.** [CITE] [NUMBERS] In one low-velocity seawater comparison, C72200 had **0.4–0.9 mpy** general attack and **1 mil** pitting in quiet water; C71500 had **0.3–0.5 mpy** and **1–2 mil**, respectively. At approximately **0.61 m/s**, the corresponding general rates were **0.8–1.2 versus 0.5–0.7 mpy**. In a separate set of tests, C71900’s *no-flow* crevice/localized depths were **0.003–0.009/0.004–0.009 in**, versus C71500’s **nil–0.006/nil–0.004 in**; C71900 was exposed for **6–9 months**, C71500 for **one year**, so these are warning signals rather than controlled equal-duration effect sizes. A three-month higher-flow comparison similarly lists C71900 crevice depths of **0.013 and 0.008 in**, with **nil** reported for C71500, despite less impingement of C71900. Lewis and LaQue (1981), doi:**10.2172/6255887**. (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48)

**NAB cladding—suggestive, confounded.** [CITE] [NUMBERS] After **21 days in 3.5 wt% NaCl**, maximum cross-sectional attack of laser-deposited NAB was **3.4 ± 0.1 µm** without an interlayer, **2.0 ± 0.1 µm** above a Ni-rich interlayer, and **1.8 ± 0.1 µm** above the Ni–Cr interlayer. Corresponding polarization-derived currents were **7.82, 4.65, and 4.09 µA/cm²**; Ni–Cr-case *E*corr was **−252 mV versus Ag/AgCl** and *R*p **4,865 Ω·cm²**. The Ni-only case’s *R*p was **5,275 Ω·cm²**, so the electrical metrics do not all rank the Cr case first. Substrate was **SUS630 steel**, not C95800 or wrought Cu–Ni; the simultaneous changes in Ni barrier, Fe dilution, and deposited microstructure prevent attribution of the small **0.2 µm** Ni–Cr/Ni-only depth difference to Cr alone. Zhao *et al.* (2022), doi:**10.3390/met12050781**. (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 4-7, zhao2022thelaserdeposited pages 2-4)

[GAP] No retrieved study demonstrates a Cr-dependent **30-day ASTM D1141** depth-of-selective-attack comparison on **as-deposited, single-stream Cu–Ni–Cr** against wrought C71500. No defensible Cr-specific numerical threshold for cyclic-polarization breakdown/repassivation potential, EIS film resistance, biofouling, or NAB dealuminification can be extracted from these comparisons. The **helpful range directly established here is approximately 0.5 wt% Cr in Cu–Ni for impingement**; an upper range that improves **still-seawater** corrosion has *not* been established. (din1993effectofresidual pages 4-7, zhao2022thelaserdeposited pages 7-10, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48)

## 3. DED, dissimilar repair, and reheating

[CITE] **Welding analog, not Cr-specific DED proof:** Cu–Ni joining guidance identifies oxygen-related weld porosity and embrittlement; a conventional Cu–Ni GTAW/GMAW filler carries **0.20–0.50 wt% Ti** as deoxidizer, and one recommended interpass limit is **<66 °C**. Iron pickup and low-melting contaminants can encourage hot cracking in dissimilar Cu joining; P-containing Ni phosphides and contamination by Pb/Zn are additional hazards. In steel/Cu–Ni overlays, prior Ni buttering reduces undesirable Fe dilution. These findings motivate controlling oxygen and measuring local chemistry in a NAB/Cu–Ni repair, but **do not establish a Cr-induced hot-cracking threshold** or authorize Ti additions to this composition palette. Beaver, *State-of-the-Art Survey of Joinability of Materials for OTEC Heat Exchangers* (1978), doi:**10.2172/6523751**; Carlone and Astarita, “Dissimilar Metal Welding,” **Metals** 9 (2019) 1206, doi:**10.3390/met9111206**. (beaver1978stateoftheartsurveyof pages 60-64, beaver1978stateoftheartsurveyof pages 39-44, carlone2019dissimilarmetalwelding pages 13-14)

[CITE] In the *different* SUS630/NAB laser-overlay study, the Ni-only intermediate-layer specimen fractured near the interface; the authors proposed **liquation cracking of Al-rich intermetallic material** and measured **6.87 ± 0.5% elongation**, versus **9.44 ± 0.6%** for the Ni–Cr interlayer specimen. This is a warning about reheated Al-rich interfaces, **not proof that Cr prevents liquation** in C95800. Local Cr-rich or oxide particles and interfacial composition gradients are plausible crack/porosity hypotheses for repeated layers; their incidence, Cr evaporation/retention and laser oxidation losses require direct measurement. Zhao *et al.* (2022), doi:**10.3390/met12050781**. (zhao2022thelaserdeposited pages 4-7)

[GAP] Published CuCrZr laser processing demonstrates that some Cr-bearing Cu alloys can be consolidated, while infrared-laser copper processing remains sensitive to absorption and lack of fusion; it does **not** demonstrate crack-free, corrosion-qualified **Cu–Ni–Cr powder DED onto itself, C95800, and wrought Cu–Ni**. The proposed weld-metal chemistry near each substrate must therefore be treated as a **measured dilution trajectory**, not the nominal powder chemistry. Check first and reheated layers separately for solidification cracks, partially melted-zone liquation, connected oxide/particle strings, oxygen and Cr loss, and through-interface attack. Canacoo *et al.*, “Laser Additive Manufacturing of Copper and Its Alloys,” **International Journal of Precision Engineering and Manufacturing–Green Technology** (2026), doi:**10.1007/s40684-026-00928-z**. (zhao2022thelaserdeposited pages 4-7, canacoo2026laseradditivemanufacturing pages 10-12)

## 4. Powder melting, binary equilibria, and CALPHAD

[CITE] [NUMBERS] **Oxide-shell risk is observed; atomizer failure is inferred.** A Cu–Cr/Al₂O₃ wetting study reports that a nominal **95 vol% Cu–5 vol% Cr** specimen—approximately **4.1 wt% Cr** as analyzed—formed a persistent Cr-rich oxide shell on heating, obstructing normal sessile-droplet formation even under controlled atmosphere. Capillary extrusion at approximately **1,260 °C** allowed transient contact; apparent contact angles of roughly **128–138°** still indicated poor alumina wetting. The article bears an **October 1, 2026 online publication date**, despite a November issue designation. These experiments are relevant to oxidation and feed delivery, but were **not induction melting, zirconia testing, or ultrasonic atomization** at 0.5–2 wt% Cr. Zygmuntowicz *et al.*, “Wetting kinetics and oxidation-induced passivation of copper–nickel and copper–chromium alloys on aluminium oxide substrates,” **Advances in Science and Technology Research Journal** 20 (2026) 263–279, doi:**10.12913/22998624/225757**. (zygmuntowicz2026wettingkineticsand pages 6-8, zygmuntowicz2026wettingkineticsand pages 8-10, zygmuntowicz2026wettingkineticsand pages 1-2)

[GAP] For the specified **approximately 1,300 °C induction module**, do **not** infer from the **1,076 °C eutectic** that all 2 wt% Cr-containing feeds have enough superheat. Zhao *et al.* cite a **Cu–Cr eutectic at 1.27 wt% Cr and 1,076 °C**; **1.27 wt% is the *liquid* eutectic composition, not the maximum Cr solubility in α-Cu**. The retrieved evidence confirms low equilibrium Cu–Cr mutual solubility but does **not independently quantify** its maximum wt% and temperature, the **2 wt% Cu–Ni–Cr or Cu–Al–Cr liquidus**, or a refractory-solid fraction at a proposed pour temperature. No numerical chromium effect on surface tension, Cr vapor loss, zirconia reaction, graphite pickup, or Ti-alloy versus Mo sonotrode dissolution was verified. Obtain database-specific liquidus/**last-particle-dissolution** and Scheil outputs for *each complete composition*, then verify by DSC/melt observation, powder oxygen and composition before/after atomization, and sonotrode/crucible contamination analysis. Zhao *et al.* (2022), doi:**10.3390/met12050781**; Lei *et al.*, “Cu-Containing High Entropy Alloys for Nuclear Fusion Application,” **Materials Transactions** 61 (2020/2021) 1247–1251, doi:**10.2320/matertrans.mt-m2020049**. (zhao2022thelaserdeposited pages 4-7, lei2021cucontaininghighentropy pages 48-58)

[GAP] **CALPHAD assessment is not identical to database coverage.** The retrieved material does not document a verified **TCCU release/version**, a specific **COST 531 assessment**, or a downloadable, validated Cu–Cr/Cu–Ni–Cr/Cu–Al–Cr **TDB** covering this palette. Consequently I cannot assert assessed ternaries or report calculated liquidus values. Test element/phase availability and binary-versus-ternary interaction provenance in the actual TCCU installation; export only license-permitted model parameters for pycalphad and compare computed invariants to the reported binary eutectic. In particular, check for predicted Cr-rich primary solids and oxide phases before accepting a nominal **≤1,250 °C** liquidus as proof of atomizability. (zhao2022thelaserdeposited pages 4-7, lei2021cucontaininghighentropy pages 48-58)

## 5. Interactions, supply, and safeguards

- **Ni–Fe–Cr:** [CITE] [NUMBERS] The C72200 demonstration combines **Ni 15, Fe 0.8, Cr 0.5 wt%**; it does **not** isolate Cr at lower Ni. Cu–Ni film measurements summarized by Lewis and LaQue show markedly different Ni/Fe enrichment when Fe precipitates rather than remaining largely in solution, so compare **Cr × Fe × Ni** and measured phase fractions, not a universal Cr/Ni replacement ratio. There is no defensible numeric constraint on **Cr + Fe** or **Cr/Ni** from these data. Fe enrichment from NAB dilution can additionally produce selectively attacked Fe-rich dendrites; the SUS630 overlay is a warning, not a C95800 dilution measurement. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 48-55, zhao2022thelaserdeposited pages 4-7, din1993effectofresidual pages 4-7)
- **Al, Mn, Si and contaminants:** [GAP] Screen Cr × Al and Cr × Ni near NAB for β′/κ redistribution, phase-boundary liquation, oxide inclusions and local corrosion; Cr × Si in CuNi2SiCr belongs to a different strengthening system. Fe/Mn oxide-film and Cu₂O behavior cannot be presumed transferable to a Cr-rich particle. Avoid invoking a Cr-induced remedy for As-controlled dezincification/dealuminification, or for P-, Pb- and Zn-associated joining defects without an actual factorial study. (carlone2019dissimilarmetalwelding pages 13-14, zhao2022thelaserdeposited pages 4-7, din1993effectofresidual pages 4-7, polkam2022laserpowderbed pages 1-5)
- **Criticality, price and safety:** [CITE] [NUMBERS] Chromium appears on the **2022 U.S. critical-minerals list** and the **November 7, 2025 final list**; the latter also lists Cu and Ni. The 2025 final list, rather than the earlier 2025 methodology proposal alone, is the pertinent status. U.S. Geological Survey, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, OFR 2025-1047, doi:**10.3133/ofr20251047**; final-list reference **90 FR 50494**. A defensible **USD/kg price for the particular high-purity Cr metal/master alloy** was not retrieved: chromite, ferrochrome, bulk Cr metal, and small-quantity high-purity feedstock are different products; request a dated, delivered **0.5 kg-charge-scale** quotation rather than presenting an invented spot price. Metallic alloyed Cr must not be equated to Cr(VI) coating chemistry. Nevertheless, assess respirable powder and laser-fume exposure and determine whether **Cr(VI)** occurs; OSHA’s applicable Cr(VI) permissible exposure limit is **5 µg/m³, eight-hour TWA** (29 CFR 1910.1026). This occupational airborne limit is not a wt% limit for finished alloy. Verify applicable RoHS/REACH use and Navy procurement/air-permit requirements rather than assuming a blanket ban on Cr metal; the retrieved sources establish no Navy prohibition on this addition. Use enclosed inert powder handling, suitable extraction/filtration and exposure monitoring. (nassar2025methodologyandtechnical pages 33-35, staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 9-11)

## 6. Proposed bounds and evidence quality

**[CITE] [NUMBERS] Conservative maximum: 0.5 wt% Cr, Cu–Ni branch.** This is the retrieved commercially identified C72200 level and the **functional floor**—the smallest *documented* Cr addition with a marked seawater impingement effect. It is not a demonstrated minimum for still-water corrosion. **Failure mode limiting confidence in higher concentrations:** oxide/segregation burden and localized corrosion without a demonstrated gain over C71500 in quiet seawater. **Non-conservative maximum: 2.0 wt% Cr, Cu–Ni branch, explicitly an exploratory design cap**, not a verified UNS specification or demonstrated DED-compatible limit. It deliberately challenges Cr-rich-particle formation, oxide-skin/feedstock losses, uncertain melt superheat and the C71900-class low-flow crevice counterexample; the retrieved literature does **not** establish that 2.0 wt% meets the stated as-deposited target. Neither bound is automatically transferred to an Al-bronze-only composition. The **impurity_max_wt field is NA**, because this is an INCLUDE decision, not an asserted impurity specification. Overall **evidence = moderate** for *the Cu–Ni decision*, but **thin** for its 2.0 wt% cap, NAB transfer and as-deposited repair qualification. (din1993effectofresidual pages 4-7, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48, zhao2022thelaserdeposited pages 4-7, zygmuntowicz2026wettingkineticsand pages 6-8)

**[GAP] Acceptance gate:** At each planned Cr level, reject a feed whose measured melt retains refractory solids or cannot be poured/atomized with useful superheat; reject a deposited alloy that cracks on itself **or either repair substrate**, has connected oxide/porosity, or exceeds wrought C71500’s **30-day maximum selective-attack depth** under matched ASTM D1141 exposure. OCP, LPR, EIS and cyclic polarization should be supporting diagnostics, **not substitutes** for the matched long-immersion criterion. This is a proposed qualification protocol, not an already demonstrated Cr result. (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48, zhao2022thelaserdeposited pages 4-7)

VERDICT | Cr | decision=INCLUDE | family=Cu-Ni | conservative_max_wt=0.5 | nonconservative_max_wt=2.0 | floor_wt=0.5 | impurity_max_wt=NA | evidence=moderate

References

1. (din1993effectofresidual pages 4-7): A.M.Shams El Din. Effect of residual and minor constituents on the corrosion behaviour of some technically important alloys. Desalination, 93:487-498, Aug 1993. URL: https://doi.org/10.1016/0011-9164(93)80124-6, doi:10.1016/0011-9164(93)80124-6. This article has 3 citations and is from a domain leading peer-reviewed journal.

2. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

3. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

4. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

5. (zhao2022thelaserdeposited pages 4-7): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

6. (lewis1981evaluationofcoppernickel media c5fcc684): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

7. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

8. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

9. (polkam2022laserpowderbed pages 1-5): RP Polkam. Laser powder bed fusion of cuni2sicr alloy: process parameters optimization and electro-mechanical characterization. Unknown journal, 2022.

10. (batawi1993microstructuraldesignand pages 65-68): E El Batawi. Microstructural design and thermal stability of rapidly solidified, high strenght, high conductivity copper alloys. Unknown journal, 1993.

11. (beaver1978stateoftheartsurveyof pages 60-64): R. J. Beaver. State-of-the-art survey of joinability of materials for otec heat exchangers. ArXiv, 80:10647, Dec 1978. URL: https://doi.org/10.2172/6523751, doi:10.2172/6523751. This article has 1 citations.

12. (beaver1978stateoftheartsurveyof pages 39-44): R. J. Beaver. State-of-the-art survey of joinability of materials for otec heat exchangers. ArXiv, 80:10647, Dec 1978. URL: https://doi.org/10.2172/6523751, doi:10.2172/6523751. This article has 1 citations.

13. (lewis1981evaluationofcoppernickel media 3f6e8440): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

14. (carlone2019dissimilarmetalwelding pages 13-14): P. Carlone and A. Astarita. Dissimilar metal welding. Metals, Nov 2019. URL: https://doi.org/10.3390/met9111206, doi:10.3390/met9111206. This article has 23 citations.

15. (canacoo2026laseradditivemanufacturing pages 10-12): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

16. (zygmuntowicz2026wettingkineticsand pages 6-8): Justyna Zygmuntowicz, Paulina Piotrkiewicz, Waldemar Kaszuwara, Marcin Wachowski, and Michal Jambor. Wetting kinetics and oxidation-induced passivation of copper–nickel and copper–chromium alloys on aluminium oxide substrates. Advances in Science and Technology Research Journal, 20:263-279, Nov 2026. URL: https://doi.org/10.12913/22998624/225757, doi:10.12913/22998624/225757. This article has 0 citations.

17. (zygmuntowicz2026wettingkineticsand pages 8-10): Justyna Zygmuntowicz, Paulina Piotrkiewicz, Waldemar Kaszuwara, Marcin Wachowski, and Michal Jambor. Wetting kinetics and oxidation-induced passivation of copper–nickel and copper–chromium alloys on aluminium oxide substrates. Advances in Science and Technology Research Journal, 20:263-279, Nov 2026. URL: https://doi.org/10.12913/22998624/225757, doi:10.12913/22998624/225757. This article has 0 citations.

18. (zygmuntowicz2026wettingkineticsand pages 1-2): Justyna Zygmuntowicz, Paulina Piotrkiewicz, Waldemar Kaszuwara, Marcin Wachowski, and Michal Jambor. Wetting kinetics and oxidation-induced passivation of copper–nickel and copper–chromium alloys on aluminium oxide substrates. Advances in Science and Technology Research Journal, 20:263-279, Nov 2026. URL: https://doi.org/10.12913/22998624/225757, doi:10.12913/22998624/225757. This article has 0 citations.

19. (lei2021cucontaininghighentropy pages 48-58): Yu Lei, Naoyuki Hashimoto, and Shigehito Isobe. Cu-containing high entropy alloys for nuclear fusion application. MATERIALS TRANSACTIONS, 61:1247-1251, Jul 2021. URL: https://doi.org/10.2320/matertrans.mt-m2020049, doi:10.2320/matertrans.mt-m2020049. This article has 11 citations and is from a peer-reviewed journal.

20. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

21. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

22. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.
