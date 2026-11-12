<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 9e252e78-da6b-4bd4-9f94-2a1bbe9477c4
- Submitted: 2026-10-17T19:00:01Z
- Fetched: 2026-10-17T19:33:09Z (status: success)
- Raw trajectory JSON: ../raw/el-24-Bi.json.gz
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

ELEMENT UNDER REVIEW: Bi (impurity / free-machining). Lead-free free-machining brasses and bronzes (e.g. C89833 type); bismuth films on grain boundaries embrittle copper at ppm levels; impurity limit.

Answer for Bi specifically, not for copper alloys in general:
1. ROLE: what Bi does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Bi ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Bi changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Bi, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Bi, Cu-Ni-Bi and Cu-Al-Bi are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Bi in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Bi neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Bi | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Bi (impurity / free-machining). Lead-free free-machining brasses and bronzes (e.g. C89833 type); bismuth films on grain boundaries embrittle copper at ppm levels; impurity limit.

Answer for Bi specifically, not for copper alloys in general:
1. ROLE: what Bi does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Bi ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Bi changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Bi, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Bi, Cu-Ni-Bi and Cu-Al-Bi are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Bi in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Bi neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Bi | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Bi in pre-alloyed copper powder for marine laser DED

**Decision: LIMIT Bi as an impurity, rather than include it as a composition variable.** [NUMBERS] Specify **Bi ≤0.001 wt% (10 ppm) in both powder and deposit** for the combined Cu–Ni/aluminum-bronze search space. This is the published Cu–Ni hot-workability control level, **not** a demonstrated DED cracking threshold or an identified ASTM/AWS acceptance limit. For tin-bronze-rich candidates, a more cautious, separately qualified target is **≤0.0004 wt% (4 ppm)**. The benefit of Bi-bearing *cast, free-machining* plumbing alloys does not establish crack-free multipass DED, repair compatibility, or corrosion equivalence to wrought C71500. Bi segregates strongly to Cu grain boundaries; repeated melting and reheating make the potential benefit–risk tradeoff especially unfavorable. Analytical verification is essential at these ppm levels. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 1-3, lozovoi2006structuralandchemical pages 8-9)

## 1. Role, alloy families, and specifications

[CITE][NUMBERS] In conventional Cu-rich alloys, Bi is principally a **lead-replacement free-machining constituent**: predominantly discrete Bi-rich particles rather than a useful bulk solid-solution strengthener. A measured lead-free cast gunmetal, **JIS CAC901**, contained **0.4 wt% Bi**, **5.5 wt% Sn**, **6.0 wt% Zn**, **0.1 wt% Ni**, and **87.1 wt% Cu**; its visible second phase was Bi. A published **UNS C89836** composition gives **Bi 1.5–3.5 wt%**, **Cu 87–91 wt%**, **Sn 4–7 wt%**, **Zn 2–4 wt%**, and **Ni ≤0.90 wt%**. A cast EnviroBrass III experimental composition had **0.9 wt% Bi**, **0.03 wt% Se**, **0.6 wt% Ni**, and **35.3 wt% Zn**, Cu balance. These establish intentional use in **cast plumbing brasses/gunmetals**, not suitability as blown-powder marine repair filler. The C89836 range is a published UNS composition reproduced in a research paper; confirm the current controlling UNS/ASTM procurement edition before treating it as an acceptance specification. The retrieved material did **not** substantiate a numerical range for the question’s suggested **C89833** designation. (yasuda2017corrosionbehaviorof pages 1-2, yasuda2017corrosionbehaviorof media 062fd124, rane2026surfacealloyingand pages 2-4, m.sadayappan2005grainrefinementof pages 19-23)

[CITE] In the cited cast-brass experiments, introducing Bi with Se changed the grain-size *rating* from **1.3 to 4.3**, but the composition changed in several ways simultaneously; it does not prove Bi is an effective inoculant for Cu–Ni or NAB DED. Bi particles can aid chip breaking in cast free-machining alloys. The Cu–Bi binary has **no stable intermetallic**, whereas assessed **Ni–Bi** contains NiBi and NiBi₃: do not call either a demonstrated precipitate in dilute marine Cu–Ni–Bi without phase identification. Bi₂O₃ on an exposed **Bi particle** is an aqueous corrosion product, not proof that Bi deoxidizes the melt or improves the Cu–Ni/NAB protective film. No substantiated Bi benefit was found for wrought C71500-type Cu–Ni, NAB/C95800, Mn–Al bronze, Cu–Ni–Sn, or Cu–Ni–Si; nor was an intentional Bi range established for the named Navy substrate or AWS A5.7 ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl fillers. **An unspecified “other elements” allowance must not be interpreted as permission for designed Bi.** [GAP][NAVY][SPEC] The retrieved editions did not permit verification of a Bi-specific limit in ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, or EN 12449. (teppo1990anassessmentof pages 1-5, vassilev2009commentsandreconciliation pages 1-2, m.sadayappan2005grainrefinementof pages 8-10, m.sadayappan2005grainrefinementof pages 19-23, yasuda2017corrosionbehaviorof pages 1-2)

## 2. Quantitative chloride-corrosion evidence—and its limits

[CITE][NUMBERS] Yasuda and colleagues tested **cast CAC901 with 0.4 wt% Bi** in **deaerated 3.0 wt% NaCl at 30 °C**, *not* flowing natural seawater, ASTM D1141, or an as-deposited weld. Its corrosion potential was approximately **−0.45 V versus saturated Ag/AgCl**, similar to two other Cu–Sn–Zn casting alloys. Their polarization curves were governed principally by the **alloy matrix**; they do not show that adding Bi lowered the corrosion rate. Separate Bi-particle measurements showed that Bi was more noble than CAC901 and suffered little preferential attack at the alloy’s natural potential, unlike Pb particles in leaded CAC406. At more anodic potentials Bi₂O₃ and BiOCl formed: Bi current at **0.00 and +0.10 V versus Ag/AgCl** decayed after one hour to **0.08 and 0.11 mA cm⁻²**, respectively, but remained **2.3 mA cm⁻² at +0.40 V**. In chloride-bearing buffered solutions the passive response degraded around **−0.10 V versus Ag/AgCl**. These are **particle/potential observations**, not a beneficial bulk-Bi concentration window. (yasuda2017corrosionbehaviorof pages 1-2, yasuda2017corrosionbehaviorof pages 2-3, yasuda2017corrosionbehaviorof pages 5-6, yasuda2017corrosionbehaviorof pages 6-8)

[CITE][NUMBERS] Brass dezincification evidence is **conflicting and confounded**. A Copper Development Association review reports a historical 60–40-type brass series at **0, 0.08, 0.25 and 1.00 wt% Bi**: the **0.25 wt%** specimen ranked worst and had **11.0% elongation**, versus **38.5%** for the Bi-free specimen. The reviewer noted that the Bi-containing compositions also had higher estimated β-brass fractions, so the ranking cannot isolate Bi. Other tested brasses with **2 wt% Bi**, or **1 wt% Bi plus 0.12 wt% As**, dezincified roughly like corresponding Pb-bearing alloys; the latter’s resistance cannot be assigned to Bi rather than As. Their test medium was not established as seawater or **3.5 wt% NaCl**. **No Bi concentration was shown to improve Cu–Ni or aluminum-bronze seawater corrosion**, and no Bi-specific rate, EIS film resistance, pit/crevice depth, erosion–corrosion loss, or allowable seawater velocity was established for those families. [GAP] CAC901’s behavior also cannot establish the specified **30-day selective-attack depth** or C71500-equivalent performance. (davies1993anoteon pages 8-9, davies1993anoteon pages 5-6, davies1993anoteon pages 4-5, yasuda2017corrosionbehaviorof pages 1-2)

## 3. DED, welding, and dilution

[CITE][NUMBERS] The strongest directly useful quantitative joining-adjacent evidence is a U.S. Bureau of Mines review of **commercial hot-rolling experience**, not a Bi-dosed DED trial: maximum Bi was **0.001 wt% in Cu–Ni**, **0.001 wt% in nickel silver**, **0.002 wt% in 70–30 brass**, and **0.0004 wt% in phosphor bronze**. The same review identifies Bi among low-melting boundary-film impurities implicated in **heat-affected-zone cracking**. Atomistic work found that saturating a modeled Cu boundary with Bi reduced its calculated separation work from **3.35 to 0.96 J m⁻²** at one-monolayer boundary coverage; monolayer *boundary coverage is not a bulk wt% threshold*. Together these support concern about last-to-freeze segregation, solidification cracks, and reheating/liquation of Bi-rich boundary material. They **do not quantify** DED crack probability, dilution tolerance, or a laser-specific safe concentration. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6, lozovoi2006structuralandchemical pages 8-9)

[GAP][NAVY] For single-stream DED onto itself and **C95800 or wrought Cu–Ni**, anticipate the **fusion boundary, remelted interlayer boundaries, and heat-affected substrate** as critical inspection sites. Dilution can lower the *average* deposit Bi concentration without eliminating local Bi-rich liquid or boundary segregation. Conversely, a clean substrate does not make Bi-bearing powder benign. Direct comparisons using the four named AWS fillers, measurements of Bi laser evaporation/porosity, and Bi-specific multipass or repair cracking studies were **not retrieved**. These are mechanistic risks extrapolated from phase equilibria, copper embrittlement, and hot-working observations—not claimed AM results. (riley1986impurityeffectsin pages 3-4, lozovoi2006structuralandchemical pages 8-9, teppo1990anassessmentof pages 1-5)

## 4. Atomization and phase-diagram feasibility

[CITE][NUMBERS] Cu–Bi is a **simple eutectic**, near **270 °C** on the Bi-rich side; Cu melts near **1084.9 °C**. Consequently, ppm-level Bi is **not a credible mechanism for pushing a Cu-rich liquidus above the approximately 1,250 °C atomizer constraint**. It instead creates a very-low-temperature last-to-freeze constituent. Solubility estimates **disagree**: Teppo *et al.* assessed a maximum around **0.01 at% Bi at ~1200 K (~927 °C)**, approximately **0.033 wt%**, whereas a later COST-531-based account cites a measured maximum of **0.0207 at% at 975 °C**, approximately **0.068 wt%**. Both are orders of magnitude above the proposed **0.001 wt% process-control level**: **equilibrium solubility is not a crack-safety limit**. Cu–Bi binary CALPHAD assessments and its parameters in **COST 531** are documented. Ni–Bi has an assessed COST 531 binary, and a published Cu–Bi–Ni experimental/thermodynamic paper is identified in the literature (**Gao *et al.*, DOI below**), but its full text was unavailable here; its parameters and compatibility with **Thermo-Calc TCCU** were *not* verified. An Al–Bi–Cu phase-equilibria review exists, but neither a validated Cu-rich Al–Bi–Cu TDB nor TCCU’s Bi coverage was verified. Check licensed **TCCU element/phase lists and TDB records** before any pycalphad calculation; extrapolating available binaries does not establish ternary accuracy. (teppo1990anassessmentof pages 1-5, teppo1990anassessmentof pages 13-14, manasijevic2010predictionofphase pages 2-3, vassilev2009commentsandreconciliation pages 1-2, manasijevic2010predictionofphase pages 3-6)

[CITE][GAP] Oxygen-free charge and argon do not prove zero Bi oxidation or zero transfer loss. In a *different* high-temperature smelting system, **Bi-containing Cu equilibrated with calcium-aluminate oxide in alumina at 1400 °C**, and investigators used sealed ampoules to avoid losses of volatile elements including Bi. That demonstrates **possible** oxidation/slag partitioning and volatility, **not a measured 1200–1300 °C rePOWDER loss**, nor reaction rates with **zirconia, graphite, titanium-alloy or Mo sonotrodes**. Bi-specific ultrasonic-atomization surface tension, sonotrode compatibility, 1.07-µm laser vapor fraction, oxide entrainment, and powder-to-deposit Bi retention remain unmeasured here. Do **not** overfeed Bi to compensate for an assumed evaporation fraction. Measure charge, powder-size fractions, and deposit by suitably calibrated trace-element analysis, and monitor oxygen and fume. (khartcyzov2025distributionofpb pages 1-3, khartcyzov2025distributionofpb pages 7-9)

## 5. Supply, safety, and actionable joint constraints

[CITE][NUMBERS][NAVY] **Bi was on the U.S. 2022 critical-minerals list and remains on the November 2025 final list**; Cu and Ni also appear on the **2025** list. A secondary compilation quoting USGS *Mineral Commodity Summaries* gives indicative Bi metal prices **US$8.98 kg⁻¹ (2024)** and **US$11.66 kg⁻¹ (2025)**, versus an approximately **US$11.68 kg⁻¹ February-2025 market quote**. These are commodity-scale indicators, **not** 0.5-kg laboratory-order prices. No Bi-specific OSHA permissible exposure limit, RoHS/REACH ban or exemption, or Navy Bi prohibition was verified in the retrieved sources: do not invent one or infer that Bi is regulated identically to Pb. Treat fine metal powder and **Bi-containing laser fumes/oxides** as potential inhalation exposures, use local exhaust/inert handling and assess all co-present hazardous alloy constituents under applicable rules. (staff2024usgsmineralreview pages 6-8, iii2026usgscriticalminerals pages 1-2, teer2025geochemicalanalysisfor pages 82-83, khartcyzov2025distributionofpb pages 1-3)

[NUMBERS][SPEC] **Joint-constraint implementation:** set `Bi ≤ 0.001 wt%` for both Cu–Ni and aluminum-bronze candidate powders *as a project-wide conservative screening rule*, with **`Bi ≤ 0.0004 wt%`** as an additional caution for Sn-rich bronze variants. The first number **comes from Cu–Ni hot-rolling experience**, not a demonstrated C95800, AWS, or Navy standard; the second comes from phosphor-bronze hot rolling. Reject use of free-machining-casting bounds or the much higher equilibrium-solubility bounds as DED design maxima. Track **Bi with Pb, Te and Se** because their individual low-melting/segregation hazards are not safely eliminated by a simple `Bi + Pb` allowance; the review cites **Cu–Ni Te 0.003 wt%** and **Se 0.006 wt%** as separate hot-workability control levels. It reports Li as an experimental mitigation of Bi embrittlement, **not** a demonstrated marine-DED remedy. No defensible beneficial Bi:Ni, Bi:Fe, Bi:Mn or Bi:Al ratio was found. Sn/Zn-rich cast-alloy observations and As-dependent dezincification must not be projected onto Ni/Fe/Mn/Al marine repair alloys. [GAP] A final acceptance criterion requires experimentally measured local Bi segregation, cross-section cracks and seawater attack on both self-build and each substrate. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6, riley1986impurityeffectsin pages 1-3, davies1993anoteon pages 5-6)

**Evidence quality:** **Moderate for excluding Bi as a designed DED addition and for the *provisional* Cu–Ni-derived 10-ppm screening limit; thin for a universal DED pass/fail limit and all claims of Bi-induced marine-corrosion improvement.** Cast plumbing alloy particle passivation does not resolve whether even trace Bi alters a marine deposit’s 30-day performance. (riley1986impurityeffectsin pages 3-4, yasuda2017corrosionbehaviorof pages 1-2, yasuda2017corrosionbehaviorof pages 6-8)

### Principal sources and specifications

- [CITE][NUMBERS] Riley, W. D.; Makar, H. V. “Impurity effects in secondary copper alloys.” *Conservation & Recycling* **9** (1986), 315–323. **DOI: 10.1016/0361-3658(86)90066-4.** Commercial hot-rolling limits and boundary/HAZ failure discussion. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 1-3)
- [CITE][NUMBERS] Yasuda, Y.; Abe, H.; Matsubayashi, R.; Maruyama, T.; Haruna, T. “Corrosion Behavior of Lead-Free Copper Alloy Castings and Their Crystallized Substances of Cu₂S and Bi.” *Materials Transactions* **58** (2017), 1679–1686. **DOI: 10.2320/MATERTRANS.M2017196.** JIS CAC901 composition and 3.0 wt% NaCl results. (yasuda2017corrosionbehaviorof pages 1-2, yasuda2017corrosionbehaviorof media 062fd124, yasuda2017corrosionbehaviorof pages 5-6)
- [CITE][NUMBERS] Lozovoi, A. Y.; Paxton, A. T.; Finnis, M. W. “Structural and chemical embrittlement of grain boundaries by impurities: A general theory and first-principles calculations for copper.” *Physical Review B* **74** (2006), 155416. **DOI: 10.1103/PhysRevB.74.155416.** (lozovoi2006structuralandchemical pages 8-9)
- [CITE][NUMBERS] Teppo, O.; Niemelä, J.; Taskinen, P. “An assessment of the thermodynamic properties and phase diagram of the system Bi–Cu.” *Thermochimica Acta* **173** (1990), 137–150. **DOI: 10.1016/0040-6031(90)80598-S.** (teppo1990anassessmentof pages 1-5, teppo1990anassessmentof pages 13-14)
- [CITE][NUMBERS] Manasijević, D. *et al.* “Prediction of phase equilibria and thermal analysis in the Bi–Cu–Pb ternary system.” *Thermochimica Acta* **503–504** (2010), 115–120. **DOI: 10.1016/j.tca.2010.03.018.** Documents COST 531’s Cu–Bi binary parameters; **its Pb-containing ternary invariants must not be mistaken for Cu–Bi binary invariants**. (manasijevic2010predictionofphase pages 1-2, manasijevic2010predictionofphase pages 2-3, manasijevic2010predictionofphase pages 3-6)
- [CITE] Vassilev, G.; Gandova, V.; Docheva, P. “Comments and reconciliation of the Ni–Bi-system thermodynamic reassessments.” *Crystal Research and Technology* **44** (2009), 25–30. **DOI: 10.1002/crat.200800391.** Gao, F. *et al.* “Experimental investigation and thermodynamic calculation in the Ag–Bi–Ni and Cu–Bi–Ni systems.” *Journal of Materials Research* **24** (2009), 2644–2653. **DOI: 10.1557/JMR.2009.0302**; full text not independently assessed here. (vassilev2009commentsandreconciliation pages 1-2)
- [CITE][SPEC] Rane, K. K. *et al.* “Surface Alloying and Surface Compositing of Copper Alloy Castings Using Mold and Core Coatings.” *International Journal of Metalcasting* (2026). **DOI: 10.1007/s40962-026-01959-7.** Reproduces UNS **C89836 Bi 1.5–3.5 wt%**; its corrosion medium was **tap water, not seawater**. (rane2026surfacealloyingand pages 2-4, rane2026surfacealloyingand pages 4-6)
- [CITE] Davies, D. D. *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*. Copper Development Association, 1993, report **7013-0009**; **no DOI identified**. (davies1993anoteon pages 1-3, davies1993anoteon pages 5-6, davies1993anoteon pages 8-9)
- [CITE][NUMBERS] Sadayappan, M. *et al.* *Grain Refinement of Permanent Mold Cast Copper Base Alloys*. Technical report, 2005. **DOI: 10.2172/840819.** (m.sadayappan2005grainrefinementof pages 8-10, m.sadayappan2005grainrefinementof pages 19-23)
- [CITE] Khartcyzov, G.; Shevchenko, M.; Jak, E. “Distribution of Pb, Zn, Fe, As, Sn, Sb, Bi, and Ni Between Oxide Liquid and Metal … at 1400 °C.” *Journal of Sustainable Metallurgy* **11** (2025), 813–824. **DOI: 10.1007/s40831-024-00952-w.** (khartcyzov2025distributionofpb pages 1-3, khartcyzov2025distributionofpb pages 7-9)
- [SPEC][NAVY] U.S. Department of the Interior, **“2022 Final List of Critical Minerals,” 87 FR 10381 (24 February 2022)**, and **“2025 Final List of Critical Minerals,” Federal Register document 2025-19813 (November 2025)**; regulatory notices, **no DOI stated**. USGS 2025-list methodology: Nassar, N. T. *et al.*, *USGS Open-File Report 2025–1047*, **DOI: 10.3133/ofr20251047**. (staff2024usgsmineralreview pages 6-8, iii2026usgscriticalminerals pages 1-2, nassar2025methodologyandtechnical pages 1-4)

VERDICT | Bi | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.001 | evidence=moderate

References

1. (riley1986impurityeffectsin pages 3-4): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

2. (riley1986impurityeffectsin pages 1-3): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

3. (lozovoi2006structuralandchemical pages 8-9): A. Lozovoi, A. Paxton, M. Centre, S. O. Mathematics, Physics, Queen's University, Belfast, U. Materials, Imperial College of Science, Technology, Medicine, London, and U.K. Structural and chemical embrittlement of grain boundaries by impurities: a general theory and first-principles calculations for copper. Physical Review B, Oct 2006. URL: https://doi.org/10.1103/physrevb.74.155416, doi:10.1103/physrevb.74.155416. This article has 201 citations and is from a domain leading peer-reviewed journal.

4. (yasuda2017corrosionbehaviorof pages 1-2): Yoshinobu Yasuda, Hiroyuki Abe, Ryozo Matsubayashi, Toru Maruyama, and Takumi Haruna. Corrosion behavior of lead-free copper alloy castings and their crystallized substances of cu2s and bi. Journal of the Japan Institute of Metals and Materials, 58:1679-1686, Jul 2017. URL: https://doi.org/10.2320/matertrans.m2017196, doi:10.2320/matertrans.m2017196. This article has 6 citations.

5. (yasuda2017corrosionbehaviorof media 062fd124): Yoshinobu Yasuda, Hiroyuki Abe, Ryozo Matsubayashi, Toru Maruyama, and Takumi Haruna. Corrosion behavior of lead-free copper alloy castings and their crystallized substances of cu2s and bi. Journal of the Japan Institute of Metals and Materials, 58:1679-1686, Jul 2017. URL: https://doi.org/10.2320/matertrans.m2017196, doi:10.2320/matertrans.m2017196. This article has 6 citations.

6. (rane2026surfacealloyingand pages 2-4): Kaustubh Kishore Rane, Mehran Zare, Flavio Toma, Swaroop Kumar Behera, Benjamin Church, and Pradeep Rohatgi. Surface alloying and surface compositing of copper alloy castings using mold and core coatings. International Journal of Metalcasting, Apr 2026. URL: https://doi.org/10.1007/s40962-026-01959-7, doi:10.1007/s40962-026-01959-7. This article has 1 citations and is from a peer-reviewed journal.

7. (m.sadayappan2005grainrefinementof pages 19-23): Grain Refinement of Permanent Mold Cast Copper Base Alloys This article has 58 citations.

8. (teppo1990anassessmentof pages 1-5): Osmo Teppo, Jaana Niemelä, and Pekka Taskinen. An assessment of the thermodynamic properties and phase diagram of the system bi-cu. Thermochimica Acta, 173:137-150, Dec 1990. URL: https://doi.org/10.1016/0040-6031(90)80598-s, doi:10.1016/0040-6031(90)80598-s. This article has 75 citations and is from a peer-reviewed journal.

9. (vassilev2009commentsandreconciliation pages 1-2): G. Vassilev, V. Gandova, and P. Docheva. Comments and reconciliation of the ni–bi‐system thermodynamic reassessments. Crystal Research and Technology, 44:25-30, Jan 2009. URL: https://doi.org/10.1002/crat.200800391, doi:10.1002/crat.200800391. This article has 36 citations and is from a peer-reviewed journal.

10. (m.sadayappan2005grainrefinementof pages 8-10): Grain Refinement of Permanent Mold Cast Copper Base Alloys This article has 58 citations.

11. (yasuda2017corrosionbehaviorof pages 2-3): Yoshinobu Yasuda, Hiroyuki Abe, Ryozo Matsubayashi, Toru Maruyama, and Takumi Haruna. Corrosion behavior of lead-free copper alloy castings and their crystallized substances of cu2s and bi. Journal of the Japan Institute of Metals and Materials, 58:1679-1686, Jul 2017. URL: https://doi.org/10.2320/matertrans.m2017196, doi:10.2320/matertrans.m2017196. This article has 6 citations.

12. (yasuda2017corrosionbehaviorof pages 5-6): Yoshinobu Yasuda, Hiroyuki Abe, Ryozo Matsubayashi, Toru Maruyama, and Takumi Haruna. Corrosion behavior of lead-free copper alloy castings and their crystallized substances of cu2s and bi. Journal of the Japan Institute of Metals and Materials, 58:1679-1686, Jul 2017. URL: https://doi.org/10.2320/matertrans.m2017196, doi:10.2320/matertrans.m2017196. This article has 6 citations.

13. (yasuda2017corrosionbehaviorof pages 6-8): Yoshinobu Yasuda, Hiroyuki Abe, Ryozo Matsubayashi, Toru Maruyama, and Takumi Haruna. Corrosion behavior of lead-free copper alloy castings and their crystallized substances of cu2s and bi. Journal of the Japan Institute of Metals and Materials, 58:1679-1686, Jul 2017. URL: https://doi.org/10.2320/matertrans.m2017196, doi:10.2320/matertrans.m2017196. This article has 6 citations.

14. (davies1993anoteon pages 8-9): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

15. (davies1993anoteon pages 5-6): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

16. (davies1993anoteon pages 4-5): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

17. (riley1986impurityeffectsin pages 4-6): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

18. (teppo1990anassessmentof pages 13-14): Osmo Teppo, Jaana Niemelä, and Pekka Taskinen. An assessment of the thermodynamic properties and phase diagram of the system bi-cu. Thermochimica Acta, 173:137-150, Dec 1990. URL: https://doi.org/10.1016/0040-6031(90)80598-s, doi:10.1016/0040-6031(90)80598-s. This article has 75 citations and is from a peer-reviewed journal.

19. (manasijevic2010predictionofphase pages 2-3): Dragan Manasijević, Aleksandra Mitovski, Duško Minić, Dragana Živković, Saša Marjanović, Radiša Todorović, and Ljubiša Balanović. Prediction of phase equilibria and thermal analysis in the bi–cu–pb ternary system. Thermochimica Acta, 503:115-120, May 2010. URL: https://doi.org/10.1016/j.tca.2010.03.018, doi:10.1016/j.tca.2010.03.018. This article has 3 citations and is from a peer-reviewed journal.

20. (manasijevic2010predictionofphase pages 3-6): Dragan Manasijević, Aleksandra Mitovski, Duško Minić, Dragana Živković, Saša Marjanović, Radiša Todorović, and Ljubiša Balanović. Prediction of phase equilibria and thermal analysis in the bi–cu–pb ternary system. Thermochimica Acta, 503:115-120, May 2010. URL: https://doi.org/10.1016/j.tca.2010.03.018, doi:10.1016/j.tca.2010.03.018. This article has 3 citations and is from a peer-reviewed journal.

21. (khartcyzov2025distributionofpb pages 1-3): G. Khartcyzov, M. Shevchenko, and E. Jak. Distribution of pb, zn, fe, as, sn, sb, bi, and ni between oxide liquid and metal in the ‘cuo0.5’-cao-alo1.5 system in equilibrium with cu metal at 1400 °c. Journal of Sustainable Metallurgy, Nov 2025. URL: https://doi.org/10.1007/s40831-024-00952-w, doi:10.1007/s40831-024-00952-w. This article has 5 citations and is from a peer-reviewed journal.

22. (khartcyzov2025distributionofpb pages 7-9): G. Khartcyzov, M. Shevchenko, and E. Jak. Distribution of pb, zn, fe, as, sn, sb, bi, and ni between oxide liquid and metal in the ‘cuo0.5’-cao-alo1.5 system in equilibrium with cu metal at 1400 °c. Journal of Sustainable Metallurgy, Nov 2025. URL: https://doi.org/10.1007/s40831-024-00952-w, doi:10.1007/s40831-024-00952-w. This article has 5 citations and is from a peer-reviewed journal.

23. (staff2024usgsmineralreview pages 6-8): U Staff. Usgs mineral review. Unknown journal, 2024.

24. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

25. (teer2025geochemicalanalysisfor pages 82-83): KDP Teer. Geochemical analysis for potential critical mineral resources in carbon fly ash. Unknown journal, 2025.

26. (manasijevic2010predictionofphase pages 1-2): Dragan Manasijević, Aleksandra Mitovski, Duško Minić, Dragana Živković, Saša Marjanović, Radiša Todorović, and Ljubiša Balanović. Prediction of phase equilibria and thermal analysis in the bi–cu–pb ternary system. Thermochimica Acta, 503:115-120, May 2010. URL: https://doi.org/10.1016/j.tca.2010.03.018, doi:10.1016/j.tca.2010.03.018. This article has 3 citations and is from a peer-reviewed journal.

27. (rane2026surfacealloyingand pages 4-6): Kaustubh Kishore Rane, Mehran Zare, Flavio Toma, Swaroop Kumar Behera, Benjamin Church, and Pradeep Rohatgi. Surface alloying and surface compositing of copper alloy castings using mold and core coatings. International Journal of Metalcasting, Apr 2026. URL: https://doi.org/10.1007/s40962-026-01959-7, doi:10.1007/s40962-026-01959-7. This article has 1 citations and is from a peer-reviewed journal.

28. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

29. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
