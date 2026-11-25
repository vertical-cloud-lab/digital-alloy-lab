<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 04506a13-f16b-4c5b-9bf2-276d19c7394b
- Submitted: 2026-10-17T18:58:49Z
- Fetched: 2026-10-17T19:30:30Z (status: success)
- Raw trajectory JSON: ../raw/el-08-Zn.json.gz
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

ELEMENT UNDER REVIEW: Zn (major seawater addition). Brasses: naval brass C46400 (about 39 Zn), aluminum brass C68700 (about 21 Zn), admiralty brass C44300 (28 Zn); Zn is limited to 0.5-1 wt% in Cu-Ni specifications. Dezincification in seawater; Zn boils at 907 C, so lasers evaporate it.

Answer for Zn specifically, not for copper alloys in general:
1. ROLE: what Zn does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Zn ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Zn changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Zn, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Zn, Cu-Ni-Zn and Cu-Al-Zn are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Zn in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Zn neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Zn | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Zn (major seawater addition). Brasses: naval brass C46400 (about 39 Zn), aluminum brass C68700 (about 21 Zn), admiralty brass C44300 (28 Zn); Zn is limited to 0.5-1 wt% in Cu-Ni specifications. Dezincification in seawater; Zn boils at 907 C, so lasers evaporate it.

Answer for Zn specifically, not for copper alloys in general:
1. ROLE: what Zn does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Zn ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Zn changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Zn, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Zn, Cu-Ni-Zn and Cu-Al-Zn are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Zn in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Zn neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Zn | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Zn for as-deposited seawater-service copper-alloy DED

**Decision: LIMIT Zn as an incidental constituent, not a designed addition.** The defensible seawater uses of substantial Zn are principally *brasses*, whose Al, Sn, As, or phase control cannot be credited to Zn alone. The directly relevant laser experiment found substantial Zn loss, and its as-built brass suffered deep selective attack in chloride solution. Neither that experiment nor the retrieved literature establishes that adding Zn to an as-deposited Cu–Ni or nickel–aluminum-bronze (NAB) repair alloy improves on wrought C71500. Set a **provisional engineering ceiling of 0.5 wt% Zn in both powder and deposit**, with no intentional minimum; this is a proposed screening constraint, **not a verified ASTM, AWS, or Navy acceptance limit**. If an applicable procurement specification requires less, it controls. Evidence for that numerical ceiling is **thin** because a controlled low-Zn DED corrosion series was not located. (alfantazi2009corrosionbehaviorof pages 2-3, marchini2026cavitationerosionand pages 12-13, marchini2026cavitationerosionand pages 2-4)

## 1. Role and alloy-family applicability

[NUMBERS] Zn is predominantly an **α-Cu substitutional solute** at the Cu-rich end of Cu–Zn. It strengthens brass by solid solution and lowers its melting range. At larger contents, α+β/ordered β′ structures become important; preferential Zn dissolution leaves a mechanically weak Cu-rich skeleton. These are not beneficial Zn precipitates in low-Zn Cu–Ni or NAB. In Al–Cu–Zn compositions far outside ordinary low-Zn NAB, complex Zn-containing ternary phases have been documented, including a phase approximating Al₃Cu₅Zn₂; its existence does **not** establish a protective precipitate in a proposed repair powder. Zn-containing corrosion products around brass pits can be Zn/O/Cl-rich hydroxychlorides, but their presence is not proof of a durable protective seawater film. (davies1993anoteon pages 3-4, zobac2020experimentalstudyof pages 1-3, marchini2026cavitationerosionand pages 2-4, vernet2018outofequilibriumbehaviourof pages 39-43, marchini2026cavitationerosionand pages 9-12)

[SPEC] The alloy distinctions matter. C26000 is nominally **30 wt% Zn**; the measured CuZn42/CW510L comparator was **41.06 wt% Zn**. An accessible review lists approximately **2 wt% Zn nominal** for cast tin bronze C90500, but that is not a verified ASTM tolerance. The seawater aluminum-brass example discussed in the dezincification literature is **76 wt% Cu–22 wt% Zn–2 wt% Al**. These demonstrate brass and gunmetal uses, not a reason to add Zn to C71500 or C95800. The retrieved C71500 corrosion study instead specified nominal **30 wt% Ni, 0.5 wt% Fe, and 0.3 wt% Mn**, with no Zn addition reported. Primary composition tables for ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, and EN 12449 were **not accessible for verification**; accordingly, no purported certified Zn range is assigned here to C71500, C70600, C95800, C46400, C44300, C68700, ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl. In particular, a commercial grade’s nominal composition must not be represented as an ASTM or Navy maximum. (alfantazi2009corrosionbehaviorof pages 2-3, davies1993anoteon pages 3-4, marchini2026cavitationerosionand pages 2-4, vernet2018outofequilibriumbehaviourof pages 26-28, sharabian2022electronbeampowder pages 16-18)

[GAP] A distinct, measured Zn benefit in as-deposited **Cu–Ni, conventional Al bronze/NAB, Mn–Al bronze, Cu–Ni–Sn, or Cu–Ni–Si** was not established. Do not assign Zn the Ni/Fe-associated seawater performance of Cu–Ni, the Al-associated behavior of aluminum brass, or precipitation strengthening by Ni–Si without a Zn-specific experiment. The retrieved work also does not establish Zn as a grain refiner or a reliable deoxidant for these DED deposits. (alfantazi2009corrosionbehaviorof pages 2-3, davies1993anoteon pages 3-4, zobac2020experimentalstudyof pages 1-3)

## 2. Seawater and chloride corrosion

[CITE][NUMBERS] Alfantazi, Ahmed, and Tromans, *Materials & Design* **30** (2009) 2425–2430, DOI **10.1016/j.matdes.2008.10.015**, compared nominal C71500 Cu–30Ni, C61400 Cu–Al, and C26000 Cu–30Zn in **1 M NaCl**, rather than natural seawater or the proposed ASTM D1141 solution. Zn dealloying was observed for brass; near-neutral-pH tests did not establish a protective passive state or a numerical Zn-addition advantage. Their qualitative Cu–Ni comparison cannot supply a controlled corrosion-rate increment for **0–0.5 wt% Zn**. Do not convert 1 M NaCl results into seawater lifetime predictions. (alfantazi2009corrosionbehaviorof pages 2-3, alfantazi2009corrosionbehaviorof pages 1-2, alfantazi2009corrosionbehaviorof pages 4-5)

[CITE][NUMBERS] Marchini, Abrami, Gelfi, and Pola, *Progress in Additive Manufacturing* **11** (2026) 7697–7711, DOI **10.1007/s40964-026-01764-y**, tested CuZn42 in **aerated 3.5 wt% NaCl**. Wrought transverse material gave *E*₍corr₎ **−537 ± 9 mV versus SCE**, nominal *j*₍corr₎ **(2.96 ± 0.31) × 10⁻⁸ A cm⁻²**, and **247 ± 12 µm** dezincification after 30 days. LPBF build-direction material gave **−643 ± 9 mV**, **(3.16 ± 0.50) × 10⁻⁸ A cm⁻²**, and **790 ± 32 µm**, respectively; scan-plane LPBF depth was **576 ± 23 µm**, versus **324 ± 16 µm** for longitudinal wrought brass. The *j*₍corr₎ values are explicitly **comparative geometric-area indices, not uniform penetration rates**. AM and wrought Zn fractions, porosity, orientation, and α/β balance differed: this is strong evidence of an **as-built localized-attack problem**, but **not** a controlled proof that decreasing Zn intrinsically causes it. The cropped source table provides the electrochemical values. (marchini2026cavitationerosionand pages 9-12, marchini2026cavitationerosionand media 2f988ed6, marchini2026cavitationerosionand pages 12-13, marchini2026cavitationerosionand pages 2-4)

[NUMBERS] Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions* (1993; accessible manuscript without a verified journal DOI), reports **69.88 wt% Cu–30.12 wt% Zn** brass producing **21.80 mg** corrosion product in its short NaCl test; another, much more Zn-rich **52.95 wt% Cu–47.05 wt% Zn** sample produced **58.52 mg** under the reported condition. Different alloy constitution and test treatment prevent interpreting those two observations as a quantitative Zn-only dose response. In α brass, **0.024–0.084 wt% As** was reported to inhibit dezincification, while **0.25 wt% As** could worsen attack in duplex brass. As, Sb, P, Al, Sn, and Ni effects were composition/phase dependent; Fe, Mn, and Co could worsen attack. These are **inhibitors or interactions with Zn-bearing brass**, not demonstrated protective effects *of Zn*. (davies1993anoteon pages 8-9, davies1993anoteon pages 3-4, davies1993anoteon pages 6-8)

**Helpful versus harmful Zn range:** the retrieved experiments establish **no lower Zn interval that measurably improves** corrosion of Cu–Ni or NAB. They establish selective-attack concerns for approximately **30–42 wt% Zn** brasses and complex inhibitor-dependent behavior in approximately **22 wt% Zn** aluminum brass. No supported Zn-specific threshold for pitting, crevice corrosion, film resistance, erosion–corrosion, or permitted seawater velocity can be transferred to a **≤0.5 wt% Zn DED** composition. [GAP] An *as-deposited* C71500 head-to-head comparison, including cyclic polarization, EIS, and selective-attack depth, remains necessary. (alfantazi2009corrosionbehaviorof pages 2-3, marchini2026cavitationerosionand pages 9-12, davies1993anoteon pages 3-4, marchini2026cavitationerosionand pages 12-13)

The table separates directly measured laser loss and chloride attack from alloy-composition examples; it is **not** a table of certified ASTM chemistry limits. (alfantazi2009corrosionbehaviorof pages 2-3, marchini2026cavitationerosionand pages 9-12, marchini2026cavitationerosionand pages 2-4, sharabian2022electronbeampowder pages 16-18)

| Grade / process | Zn (wt%) | Quantitative performance | Interpretation / limitations | Source DOI |
|---|---:|---|---|---|
| C71500 Cu–30Ni, wrought reference | Not reported; nominal tested composition was Cu–30.0Ni–0.5Fe–0.3Mn | Tested in 1 M NaCl at pH 6.5 and 10; no defensible Zn-specific corrosion rate was reported | Zn was not a designed constituent in this experiment; this is a Zn-free Cu–Ni reference, not evidence for a beneficial Zn addition (alfantazi2009corrosionbehaviorof pages 2-3) | [10.1016/j.matdes.2008.10.015](https://doi.org/10.1016/j.matdes.2008.10.015) |
| C26000 Cu–30Zn, wrought brass | 30 nominal | Early Zn dealloying occurred in 1 M NaCl; at pH 6.5 there was no passivity. The study did not report a defensible Zn-specific penetration or mass-loss rate | Supports dezincification risk at 30 wt% Zn, but does not establish a low-Zn threshold or permit a quantitative comparison with C71500 (alfantazi2009corrosionbehaviorof pages 2-3, alfantazi2009corrosionbehaviorof pages 1-2) | [10.1016/j.matdes.2008.10.015](https://doi.org/10.1016/j.matdes.2008.10.015) |
| C90500 tin bronze | 2 nominal | No quantitative seawater or NaCl performance reported in the cited composition table | Secondary-review nominal composition only; not an ASTM-certified range and not evidence that 2 wt% Zn improves seawater corrosion (sharabian2022electronbeampowder pages 16-18) | [10.1007/s00170-022-09922-6](https://doi.org/10.1007/s00170-022-09922-6) |
| CuZn42 LPBF feedstock powder → bulk deposit | ≈43 powder → 35.46 deposit | Absolute Zn loss ≈7.54 percentage points; approximately 17.5% of the powder Zn fraction was lost | Direct evidence of severe selective Zn vaporization under a 1070 nm laser. Transferability from LPBF to blown-powder DED is indirect (marchini2026cavitationerosionand pages 2-4) | [10.1007/s40964-026-01764-y](https://doi.org/10.1007/s40964-026-01764-y) |
| CuZn42 conventional wrought bar (BR) | 41.06 | In aerated 3.5 wt% NaCl: BRT Ecorr = −537 ± 9 mV vs SCE; 30-day dezincification depth = 247 ± 12 µm | Wrought comparator; orientation and α/β microstructure affect performance (marchini2026cavitationerosionand pages 9-12, marchini2026cavitationerosionand pages 12-13) | [10.1007/s40964-026-01764-y](https://doi.org/10.1007/s40964-026-01764-y) |
| CuZn42 LPBF, build-direction section (AMz) | 35.46 bulk | In aerated 3.5 wt% NaCl: Ecorr = −643 ± 9 mV vs SCE; 30-day dezincification depth = 790 ± 32 µm | Despite lower Zn than wrought material, AMz was 106 mV more active and had ≈3.20× deeper dezincification. The Zn comparison is strongly confounded by ≈3 vol% porosity, lack-of-fusion defects, layered architecture, and orientation; it does not prove that lower Zn intrinsically worsens corrosion (marchini2026cavitationerosionand pages 9-12, marchini2026cavitationerosionand pages 12-13, marchini2026cavitationerosionand pages 2-4) | [10.1007/s40964-026-01764-y](https://doi.org/10.1007/s40964-026-01764-y) |


*Table: Selected quantitative evidence distinguishes composition facts from demonstrated corrosion and laser-processing behavior. The CuZn42 comparison documents major laser Zn loss and worse AM dezincification, while emphasizing that porosity and process heterogeneity confound any causal attribution to Zn content alone.*

## 3. DED, welding, powder production, and substrate dilution

[CITE][NUMBERS] In Marchini *et al.*, the nominal approximately **43 wt% Zn powder** yielded **35.46 wt% Zn** LPBF bulk—approximately **7.5 percentage points**, or **17.5% of the powder’s Zn fraction**, lost. Their laser wavelength was **1070 nm**; the deposit had about **2–3 vol% porosity**, and its pores and interlayer discontinuities favored localized attack. This is **LPBF evidence, not blown-powder DED evidence**; it establishes a credible vaporization and reproducibility hazard, not a validated DED loss factor at **0.5 wt% Zn**. Vapor/recoil effects and fume removal during *pure-Zn* LPBF are investigated by Qin *et al.*, *Materials* **14** (2021) 2677, DOI **10.3390/ma14102677**, but pure Zn is a mechanistic analogue, not a Cu-alloy process qualification. (marchini2026cavitationerosionand pages 1-2, marchini2026cavitationerosionand pages 9-12, marchini2026cavitationerosionand pages 2-4, qin2021influenceoflaser pages 1-2)

[GAP] No retrieved Zn-controlled **DED** or applicable ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl filler study quantified Zn’s independent effect on solidification cracking, reheated-layer liquation cracking, or porosity. Volatile loss, shifting local chemistry, oxide/fume inclusions, and a widened freezing range in *multicomponent* alloys are **screening hypotheses**, not established failure thresholds. Nor was an experiment located measuring Zn segregation or corrosion after Zn-bearing deposition onto **cast C95800** or **wrought C71500**. Substrate dilution can lower the first-layer Zn fraction but cannot certify the composition or integrity of upper, repeatedly remelted layers; measure powder, each deposit height, and both interfaces. Welding analogues should not be labeled direct DED results. (marchini2026cavitationerosionand pages 1-2, qin2021influenceoflaser pages 1-2, marchini2026cavitationerosionand pages 2-4)

[NUMBERS] Binary Cu–Zn alloying **lowers**, rather than raises, the Cu-rich liquidus: the accessible phase-diagram account gives approximately **1084 °C** at Cu, falling toward approximately **930 °C** for Cu-rich compositions up to **32.5 wt% Zn**. Thus Zn alone does **not** drive a Cu-balance feedstock above the stated **1200–1250 °C** atomization ceiling. The actual **Cu–Ni–Al–Fe–Mn–Zn** liquidus still needs a multicomponent calculation. Given Zn’s approximately **907 °C** atmospheric boiling point, charge retention and fume are concerns even when equilibrium alloy liquidus is feasible; boiling point alone does not quantify Zn loss from solution. No directly applicable measurements were found for **0.5-kg argon induction/ultrasonic atomization**, Zn reaction with **alumina, zirconia, graphite, titanium sonotrodes, or molybdenum sonotrodes**, or Zn-dependent droplet surface tension. Treat refractory and sonotrode contamination, ZnO dross, and batch-to-batch fractionation as tests to perform, not observed facts for this equipment. (marchini2026cavitationerosionand pages 2-4, vernet2018outofequilibriumbehaviourof pages 39-43)

## 4. Phase-diagram/CALPHAD and joint constraints

[CITE][NUMBERS] The binary account places the α-primary/β-peritectic region beginning at about **32.5 wt% Zn** and describes a peritectic near **902 °C** and β→β′ ordering near **454 °C**; the α-solubility upper limit is given as **38.3 atomic% Zn**, **not 38.3 wt% Zn**. Converting that atomic percentage with Cu and Zn atomic masses gives approximately **39.1 wt% Zn**, but the excerpt does not uniquely pin that maximum to a measured temperature: **do not report “39.1 wt% at 454 °C” as an experimentally verified solvus point**. The rich-Zn γ/Cu₅Zn₈ and Al–Cu–Zn ternary phases are outside the proposed impurity window. Vernet, *Out-of-Equilibrium Behaviour of Copper-Based Alloys in Industrial, Artistic and Historical Gravity Casting Processes* (2018 dissertation), DOI **10.15167/vernet-justine-marie_phd2018-03-15**; Zobac, Kroupa, and Richter, *Journal of Materials Science* **55** (2020) 10796–10810, DOI **10.1007/s10853-020-04686-4**. (zobac2020experimentalstudyof pages 1-3, vernet2018outofequilibriumbehaviourof pages 39-43)

[CITE] Published CALPHAD assessments of **Cu–Zn** and **Al–Cu–Zn** exist; Zobac *et al.* identify assessed binary descriptions and report disputed ternary γ/γ′ and complex-phase relations. A publication lead is Liang and Schmid-Fetzer’s Al–Cu–Zn ternary assessment, *Calphad* (2016), DOI **10.1016/j.calphad.2015.11.001**. **Neither the installed Thermo-Calc TCCU version’s specific Zn-bearing interaction coverage nor a compatible Cu–Ni–Zn ternary parameter set was verified from accessible database documentation.** Presence of Zn as an available element is not proof of assessed ternary interactions; check database constituents, phases, and parameter provenance before pycalphad extrapolation. [GAP] Neither equilibrium α stability nor a favorable calculated liquidus alone predicts vapor loss, crack susceptibility, or as-deposited corrosion. (zobac2020experimentalstudyof pages 1-3, zobac2020experimentalstudyof pages 7-9)

**Interactions to retain for joint screening:** Zn plus **Al** can move composition toward aluminum-brass/Al–Cu–Zn phase fields; Zn plus **Sn** occurs in gunmetal and tin-modified brass, but Sn’s inhibition depends on phase constitution; **Ni** addition was reported to improve one tin-bearing brass’s dezincification behavior, not to establish a protective **Zn:Ni ratio** in Cu–Ni; **Fe/Mn** can aggravate brass dezincification in cited tests. The α/β balance and local Cu/Zn depletion matter more than a simple sum of nominal Zn and Ni. As/Sb/P can inhibit **α-brass** attack but may fail in **duplex brass**, and As may accelerate its attack; importing these toxic inhibitors into a repair alloy is not justified here. No quantitative Ni+Zn, Al+Zn, Fe:Zn, Mn:Zn, or vapor-pressure constraint was validated for the proposed multicomponent DED alloy. (davies1993anoteon pages 6-8, davies1993anoteon pages 3-4, zobac2020experimentalstudyof pages 1-3)

## 5. Supply, safety, and specification confidence

[NAVY][CITE] **Zn was on both U.S. critical-mineral lists:** the **2022 final list**, *87 FR 10381*, is reproduced by Jenkins, Musgrove, and White, *Toxics* **11** (2023) 188, DOI **10.3390/toxics11020188**; USGS authors reproduce Zn, Ni, and newly included Cu in the **2025 final list**, *90 FR 50494*. The 2025 USGS *recommendation* to add copper is documented separately by Nassar *et al.*, Open-File Report **2025–1047**, DOI **10.3133/ofr20251047**. Reducing Ni by substituting Zn does **not** eliminate critical-mineral exposure. These list citations document supply policy, **not** a Navy authorization or prohibition on Zn-bearing repairs. (nassar2025methodologyandtechnical pages 9-10, iii2026usgscriticalminerals pages 1-2, jenkins2023outliningpotentialbiomarkers pages 1-2)

[GAP] A dated, verified zinc metal purchasing quotation or market series was not retrieved, so a defensible **$/kg** figure cannot be stated here. Similarly, no Zn-specific Navy repair prohibition was verified. RoHS/REACH restrictions should **not** be represented as a blanket ban on metallic Zn in copper alloys: regulatory attention to lead-bearing brasses is distinct from Zn itself. Zn is nutritionally essential yet exposure-dependent toxic; vaporized Zn can form inhalable oxide fume, so apply captured ventilation, exposure assessment, enclosed powder handling, and appropriate combustible-metal-powder controls. The accessible sources do **not** establish the precise current OSHA ZnO-fume PEL; obtain the controlling OSHA **29 CFR 1910.1000** table and industrial-hygiene determination before specifying an exposure number. Jenkins *et al.* discuss Zn exposure; Qin *et al.* document laser-fume formation. (qin2021influenceoflaser pages 1-2, marchini2026cavitationerosionand pages 2-4, jenkins2023outliningpotentialbiomarkers pages 1-2)

**Bounds and evidence quality.** [SPEC][GAP] For **both Cu–Ni and Al-bronze/NAB**, specify **Zn ≤0.5 wt% in powder and deposit as a provisional project impurity limit**, with no intentional Zn charge. Its failure-mode rationale is compositional volatility followed by uncertain as-built phase constitution, pores, and selective attack—not a demonstrated sharp corrosion transition at 0.5 wt%. An applicable tighter certified material or filler limit must supersede it; the requested ASTM/AWS/MIL upper-limit number was not verified. **Conservative designed-addition maximum, nonconservative designed-addition maximum, and functional floor are not assigned** under a LIMIT decision. No as-deposited Cu–Ni or NAB data establish the smallest Zn concentration with a beneficial measurable seawater effect, much less C71500-equivalent 30-day attack. The high-Zn brass result is direct for LPBF and chloride, but its extrapolation to dilute-Zn, ultrasonic-atomized, blown-powder DED is **thin**. (alfantazi2009corrosionbehaviorof pages 2-3, marchini2026cavitationerosionand pages 9-12, marchini2026cavitationerosionand pages 12-13, marchini2026cavitationerosionand pages 2-4)

VERDICT | Zn | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.5 | evidence=thin

References

1. (alfantazi2009corrosionbehaviorof pages 2-3): A.M. Alfantazi, T.M. Ahmed, and D. Tromans. Corrosion behavior of copper alloys in chloride media. Materials & Design, 30:2425-2430, Aug 2009. URL: https://doi.org/10.1016/j.matdes.2008.10.015, doi:10.1016/j.matdes.2008.10.015. This article has 357 citations and is from a highest quality peer-reviewed journal.

2. (marchini2026cavitationerosionand pages 12-13): Luca Marchini, Maria Beatrice Abrami, Marcello Gelfi, and Annalisa Pola. Cavitation erosion and corrosion behavior of lpbf and conventionally produced cuzn42 alloy. Progress in Additive Manufacturing, 11:7697-7711, Jun 2026. URL: https://doi.org/10.1007/s40964-026-01764-y, doi:10.1007/s40964-026-01764-y. This article has 0 citations and is from a peer-reviewed journal.

3. (marchini2026cavitationerosionand pages 2-4): Luca Marchini, Maria Beatrice Abrami, Marcello Gelfi, and Annalisa Pola. Cavitation erosion and corrosion behavior of lpbf and conventionally produced cuzn42 alloy. Progress in Additive Manufacturing, 11:7697-7711, Jun 2026. URL: https://doi.org/10.1007/s40964-026-01764-y, doi:10.1007/s40964-026-01764-y. This article has 0 citations and is from a peer-reviewed journal.

4. (davies1993anoteon pages 3-4): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

5. (zobac2020experimentalstudyof pages 1-3): Ondrej Zobac, Ales Kroupa, and Klaus W. Richter. Experimental study of the al–cu–zn ternary phase diagram. Journal of Materials Science, 55:10796-10810, Apr 2020. URL: https://doi.org/10.1007/s10853-020-04686-4, doi:10.1007/s10853-020-04686-4. This article has 28 citations and is from a peer-reviewed journal.

6. (vernet2018outofequilibriumbehaviourof pages 39-43): JUSTINE MARIE VERNET. Out-of-equilibrium behaviour of copper-based alloys in industrial, artistic and historical gravity casting processes. ArXiv, Mar 2018. URL: https://doi.org/10.15167/vernet-justine-marie\_phd2018-03-15, doi:10.15167/vernet-justine-marie\_phd2018-03-15. This article has 1 citations.

7. (marchini2026cavitationerosionand pages 9-12): Luca Marchini, Maria Beatrice Abrami, Marcello Gelfi, and Annalisa Pola. Cavitation erosion and corrosion behavior of lpbf and conventionally produced cuzn42 alloy. Progress in Additive Manufacturing, 11:7697-7711, Jun 2026. URL: https://doi.org/10.1007/s40964-026-01764-y, doi:10.1007/s40964-026-01764-y. This article has 0 citations and is from a peer-reviewed journal.

8. (vernet2018outofequilibriumbehaviourof pages 26-28): JUSTINE MARIE VERNET. Out-of-equilibrium behaviour of copper-based alloys in industrial, artistic and historical gravity casting processes. ArXiv, Mar 2018. URL: https://doi.org/10.15167/vernet-justine-marie\_phd2018-03-15, doi:10.15167/vernet-justine-marie\_phd2018-03-15. This article has 1 citations.

9. (sharabian2022electronbeampowder pages 16-18): Elmira Sharabian, Martin Leary, Darren Fraser, and Stefan Gulizia. Electron beam powder bed fusion of copper components: a review of mechanical properties and research opportunities. The International Journal of Advanced Manufacturing Technology, 122:513-532, Aug 2022. URL: https://doi.org/10.1007/s00170-022-09922-6, doi:10.1007/s00170-022-09922-6. This article has 56 citations.

10. (alfantazi2009corrosionbehaviorof pages 1-2): A.M. Alfantazi, T.M. Ahmed, and D. Tromans. Corrosion behavior of copper alloys in chloride media. Materials & Design, 30:2425-2430, Aug 2009. URL: https://doi.org/10.1016/j.matdes.2008.10.015, doi:10.1016/j.matdes.2008.10.015. This article has 357 citations and is from a highest quality peer-reviewed journal.

11. (alfantazi2009corrosionbehaviorof pages 4-5): A.M. Alfantazi, T.M. Ahmed, and D. Tromans. Corrosion behavior of copper alloys in chloride media. Materials & Design, 30:2425-2430, Aug 2009. URL: https://doi.org/10.1016/j.matdes.2008.10.015, doi:10.1016/j.matdes.2008.10.015. This article has 357 citations and is from a highest quality peer-reviewed journal.

12. (marchini2026cavitationerosionand media 2f988ed6): Luca Marchini, Maria Beatrice Abrami, Marcello Gelfi, and Annalisa Pola. Cavitation erosion and corrosion behavior of lpbf and conventionally produced cuzn42 alloy. Progress in Additive Manufacturing, 11:7697-7711, Jun 2026. URL: https://doi.org/10.1007/s40964-026-01764-y, doi:10.1007/s40964-026-01764-y. This article has 0 citations and is from a peer-reviewed journal.

13. (davies1993anoteon pages 8-9): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

14. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

15. (marchini2026cavitationerosionand pages 1-2): Luca Marchini, Maria Beatrice Abrami, Marcello Gelfi, and Annalisa Pola. Cavitation erosion and corrosion behavior of lpbf and conventionally produced cuzn42 alloy. Progress in Additive Manufacturing, 11:7697-7711, Jun 2026. URL: https://doi.org/10.1007/s40964-026-01764-y, doi:10.1007/s40964-026-01764-y. This article has 0 citations and is from a peer-reviewed journal.

16. (qin2021influenceoflaser pages 1-2): Yu Qin, Jinge Liu, Yanzhe Chen, Peng Wen, Yufeng Zheng, Yun Tian, Maximilian Voshage, and Johannes Henrich Schleifenbaum. Influence of laser energy input and shielding gas flow on evaporation fume during laser powder bed fusion of zn metal. Materials, 14:2677, May 2021. URL: https://doi.org/10.3390/ma14102677, doi:10.3390/ma14102677. This article has 42 citations.

17. (zobac2020experimentalstudyof pages 7-9): Ondrej Zobac, Ales Kroupa, and Klaus W. Richter. Experimental study of the al–cu–zn ternary phase diagram. Journal of Materials Science, 55:10796-10810, Apr 2020. URL: https://doi.org/10.1007/s10853-020-04686-4, doi:10.1007/s10853-020-04686-4. This article has 28 citations and is from a peer-reviewed journal.

18. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

19. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

20. (jenkins2023outliningpotentialbiomarkers pages 1-2): Jill A. Jenkins, MaryLynn Musgrove, and Sarah Jane O. White. Outlining potential biomarkers of exposure and effect to critical minerals: nutritionally essential trace elements and the rare earth elements. Toxics, 11:188, Feb 2023. URL: https://doi.org/10.3390/toxics11020188, doi:10.3390/toxics11020188. This article has 48 citations.
