<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 6a3b0d5a-4dc9-40ed-b01c-69ace225da49
- Submitted: 2026-10-17T19:00:46Z
- Fetched: 2026-10-17T19:33:15Z (status: success)
- Raw trajectory JSON: ../raw/el-31-N.json.gz
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

ELEMENT UNDER REVIEW: N (interstitial / gas). Nitrogen porosity in Cu-Ni welds (from shielding or air), nitrogen solubility rising with Ni content; Ti and Al as nitride formers. Answer as an impurity limit and a process control.

Answer for N specifically, not for copper alloys in general:
1. ROLE: what N does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their N ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how N changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-N, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-N, Cu-Ni-N and Cu-Al-N are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of N in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that N neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | N | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: N (interstitial / gas). Nitrogen porosity in Cu-Ni welds (from shielding or air), nitrogen solubility rising with Ni content; Ti and Al as nitride formers. Answer as an impurity limit and a process control.

Answer for N specifically, not for copper alloys in general:
1. ROLE: what N does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their N ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how N changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-N, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-N, Cu-Ni-N and Cu-Al-N are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of N in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that N neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | N | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Nitrogen (N): impurity limit and process control

**Decision — LIMIT, for both Cu–Ni and aluminum-bronze candidates.** Nitrogen is not a demonstrated seawater-corrosion alloying addition in either family. It is nearly insoluble in solid Cu, can enter liquid Cu under sufficiently energetic laser processing, and can leave pores on solidification. Ni increases the concern rather than establishing a beneficial N addition; Al and Ti may instead bind N as nitrides. The most relevant evidence is from *laser welding of Cu*, not blown-powder DED of Cu–Ni or nickel-aluminum bronze (NAB). A powder/deposit N ceiling can therefore be proposed as a **project screening criterion**, but not represented as an ASTM, AWS, or Navy acceptance limit. [CITE] Van Konynenburg et al., *Background Studies in Support of a Feasibility Assessment on the Use of Copper-Base Materials for Nuclear Waste Packages in a Repository in Tuff* (1990), DOI: **10.2172/137782**; Alter, Heider and Bergmann, *Journal of Laser Applications* **32**, 022020 (2020), DOI: **10.2351/7.0000063**. (konynenburg1990backgroundstudiesin pages 142-149, alter2023porenbildungbeimschweissen pages 93-97, alter2023porenbildungbeimschweissen pages 110-114)

## 1. Role and specifications

[CITE] A copper-alloy producibility review calls N *detrimental* in aluminum bronzes and Cu–Ni, although *innocuous* at ordinarily encountered levels in nominally pure Cu; it cautions that these categories are not concentration-independent. Its account describes N₂ as substantially insoluble in Cu. This is not evidence that N improves marine films, acts as a useful solid-solution strengthener, deoxidizes Cu, refines NAB grains, or inhibits dealloying. Cu₃N exists as a **metastable, predominantly thin-film** compound, not an established load-bearing precipitate in these cast or deposited marine alloys. TiN was experimentally identified in a *nitrogen-atomized, spray-formed copper alloy*. Those are different material/process states. (konynenburg1990backgroundstudiesin pages 142-149, ji2010crystallinethinfilms pages 1-2, muller2004effectofreactive pages 1-4, muller2004effectofreactive pages 4-6)

[SPEC][GAP] **No verified specified N range, in wt%, was found** for seawater-service C70600 or C71500 Cu–Ni; C95800 NAB; Mn–Al bronze; tin bronze/gunmetal; brasses; Cu–Ni–Sn or Cu–Ni–Si; or AWS A5.7 **ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl** consumables. The same applies to the requested ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, and EN 12449 specifications: the accessible evidence does **not** verify an N maximum in any of them. Do not turn an unlisted element into an invented specification limit or interpret “other elements” as a nitrogen qualification. A reproduced UNS C61300 aluminum-bronze composition table associated with ASTM B169/B171, for example, specifies Al, Fe, Sn, Mn and Ni but does not specify N. Neither shielding with N₂ nor processing with liquid nitrogen establishes a wt% N addition in an alloy. (mccright1988anannotatedhistory pages 57-58, yushchenko2010effectofnanofoil pages 38-39)

## 2. Seawater corrosion

[GAP] No controlled experiment located compares **otherwise identical Cu alloys differing only in bulk N** in natural seawater, ASTM D1141 water, or 3.5 wt% NaCl. Consequently, there is **no defensible beneficial or harmful N-composition interval**, or N-specific change in corrosion rate, *E*<sub>corr</sub>, impedance/film resistance, pitting or crevice potential, selective-attack depth, erosion–corrosion, or allowable seawater velocity. The laboratory's proposed electrochemical and 30-day immersion tests would establish these quantities; existing marine performance of a Cu–Ni or NAB alloy cannot be attributed to an unspecified N content. Nitride *coatings* and nitrogen-containing aqueous species must not be substituted for evidence about N dissolved in a seawater-service alloy. The credible indirect concern is that gas pores and nitride inclusions could provide local defect sites, **not** a measured N-induced corrosion penalty. (konynenburg1990backgroundstudiesin pages 142-149, muller2004effectofreactive pages 1-4, muller2004effectofreactive pages 6-8)

## 3. DED, welding and dilution

[NUMBERS][CITE] Alter's controlled **515 nm Cu laser-welding** experiments separate shielding atmospheres. Oxygen-free Cu welded in Ar showed no detectable N; Cu welded in synthetic air (approximately 80 vol% N₂/20 vol% O₂) had **22 mass-ppm N = 0.0022 wt% N**, measured on specimens containing both remelted and unmelted metal, and substantial porosity. That number is **an observed content in a porous specimen, not a measured safe/unsafe onset, nor necessarily the concentration within weld metal alone**. Pure N₂ shielding produced approximately **0.3–0.4% section-area porosity** in oxygen-free Cu, with **>100 pores per section** in one analysis; a broader section analysis found approximately **400 small pores per section** at 100 vol% N₂. Dry versus humid synthetic air yielded **10.7% versus 10.3%** porosity in representative sections. The proposed explanation is N uptake followed by N₂ evolution, compounded in N₂/O₂ mixtures by proposed nitrogen-oxide reaction pores; the gas species in individual pores were **inferred, not directly established**. Gas composition is in **vol%**, not alloy wt%. (alter2023porenbildungbeimschweissen pages 101-106, alter2023porenbildungbeimschweissen pages 93-97, alter2023porenbildungbeimschweissen pages 97-101, alter2023porenbildungbeimschweissen pages 106-110, alter2023porenbildungbeimschweissen pages 110-114)

[NUMBERS][CITE] In separate Cu sheet lap welds made in synthetic air with the same green laser, the reference had approximately **12.5% section-area porosity**, a Ni foil approximately **20–21%**, whereas Al or Ti foil reduced it to **<0.3%**. These are *foil-addition welding trials*, **not controlled concentrations of N, Ni, Al or Ti in a single-stream Cu-alloy powder**. The authors propose nitride/oxide scavenging; they did not demonstrate which precipitate caused each reduction. The increased porosity with Ni agrees with their stated higher gas solubility in Cu–Ni, but neither result supplies a Cu–Ni N threshold. (alter2023porenbildungbeimschweissen pages 118-122, alter2023porenbildungbeimschweissen pages 122-126)

[CITE][NAVY] A copper-base fabrication review documents routine welding of 90–10 and 70–30 Cu–Ni using 70–30 filler and discusses aluminum-bronze welding, but it provides **no measured N-dependent solidification- or reheating/liquation-cracking boundary**. For DED onto cast C95800, distinguish N originating in powder from gas or inclusions in the casting, dilution-driven Al/Ti nitride formation, and ordinary NAB phase evolution; for repair onto wrought Cu–Ni, distinguish substrate dilution and higher-Ni gas uptake. Apply the same checks to self-built layers. The direct N evidence does **not** quantify cracking, bond integrity, or corrosion at either interface, and the 515 nm keyhole-welding pore fractions cannot be transferred numerically to a ~1.07 µm blown-powder process. (konynenburg1990backgroundstudiesin pages 149-155, alter2023porenbildungbeimschweissen pages 126-130, alter2023porenbildungbeimschweissen pages 118-122)

## 4. Melting, atomization and interactions

[CITE][NUMBERS] Nitrogen-atomized **spray-formed** CuSn13.5Pb and CuSn13.5 billets contained measured total N of **0.00015 and 0.00020 wt%**, respectively; gas trapped in pores accounted approximately for the measured N. Addition of **0.15 wt% Ti** to a different Cu–Al–Fe–Mn–Co melt increased reported mean billet density from **7.00 to 7.10 g/cm³**. The study identified TiN by diffraction and reports up to a **threefold porosity reduction** with Ti. These data show why a bulk N assay must be interpreted alongside pore imaging: its reported N can include *trapped N₂*, not just interstitial N. Gas-jet spray forming is **not** ultrasonic droplet atomization in Ar. (muller2004effectofreactive pages 1-4, muller2004effectofreactive pages 4-6, muller2004effectofreactive pages 6-8)

**For the specified induction/ultrasonic route**, keep the charge, cover gas, crucible and feed system dry and air-tight; retain Ar rather than substituting N₂; assay starting metals, melt/solidified witness, each powder fraction and deposits by calibrated inert-gas fusion/hot extraction; and pair N with O/H assays, powder cross-sections or X-ray tomography, deposit density and inclusion identification. [GAP] No retrieved study measures N pickup or N-dependent wetting/surface tension for this exact Cu–Ni/NAB melt in **alumina or zirconia**, graphite contact, or on its **Ti-alloy versus Mo sonotrode**. Nitride formation at a contaminated Ti contact is plausible; neither contamination rate nor a resulting safe sonotrode choice is established. N₂ loss from gas/pores is distinct from evaporation of a metallic alloying constituent. Nitride-driven changes to droplet surface tension have been proposed for spray forming but not measured for this instrument. (alter2023porenbildungbeimschweissen pages 110-114, muller2004effectofreactive pages 1-4)

**Joint-constraint flags:** Ni-rich liquid may retain more N before solidification; available Cu welding comparisons found Ni addition worsened porosity. Al and Ti may consume N into AlN/TiN and O into oxides; their benefit depends on *both* available N and O, and inclusions are not automatically beneficial to corrosion. Fe and Mn effects on the N threshold in these deposits were not established. Stoichiometrically, complete conversion to TiN consumes approximately **3.42 units Ti per unit N by mass**, or to AlN approximately **1.93 units Al per unit N by mass**; these are **mass-balance screening ratios, not experimentally validated alloy-design requirements**. Keep N×Ni, N×O and N×(Al,Ti) interactions available for the later joint analysis. (alter2023porenbildungbeimschweissen pages 118-122, alter2023porenbildungbeimschweissen pages 122-126, muller2004effectofreactive pages 1-4, muller2004effectofreactive pages 4-6)

## 5. Phase diagram and CALPHAD

[NUMBERS][GAP] A literature synthesis reports **0.00005–0.0005 wt% N** dissolved in *liquid pure Cu* over **1,350–2,250 °C**, while describing solid-Cu N as not detectably soluble. This is **not a measured maximum solid solubility**: a defensible numeric wt% maximum *and its temperature* could not be established. The liquid range extends substantially above the proposed 1,200–1,250 °C atomization window; do not use its upper endpoint as a powder-alloy solubility allowance. Separate work measured liquid-Ni N dissolution at **1,773–1,973 K** and rising solubility with temperature, but not a reliable Cu–Ni–N liquidus surface under the proposed conditions. (alter2023porenbildungbeimschweissen pages 38-42, siwka2008equilibriumconstantsand pages 4-5)

[CITE] Cu₃N can be prepared by reactive sputtering, but reported film decomposition temperatures span roughly **100–470 °C** depending on preparation; it is not evidence for a stable Cu₃N invariant reaction in an ordinary 1-atm, ~1,250 °C Cu-rich melt. The retrieved work does **not** establish a Cu–N invariant temperature/composition, an N-induced liquidus shift, or a mechanism by which ppm-level N alone pushes liquidus past **1,250 °C**. The relevant processing risk is gas rejection/porosity and possible refractory nitrides, not a demonstrated N-raised Cu-rich liquidus. [GAP] Assessment of **Cu–N, Cu–Ni–N or Cu–Al–N** in the laboratory's exact **Thermo-Calc TCCU version**, COST 531 or a compatible published TDB **was not verified**. COST 531 solder calculations or the existence of a Cu–Ni binary model do not establish N parameters. Inspect actual database element/phase lists and assessed interactions before allowing pycalphad to calculate N-bearing liquidus or TiN/AlN equilibria; otherwise calculate the metallic alloy without an N design variable and treat N separately as a measured gas/inclusion constraint. (ji2010crystallinethinfilms pages 1-2, alter2023porenbildungbeimschweissen pages 38-42, siwka2008equilibriumconstantsand pages 4-5)

## 6. Supply, safety and bounds

[CITE] **N is not a U.S. critical mineral** in either the 2022 or final 2025 designation; the 2025 list does include **Cu and Ni**. Industrial N₂ is abundant and its delivered $/kg depends strongly on cylinder versus bulk-liquid procurement: **no defensible site-specific $/kg quote was obtained**, and the relevant added cost is analytical/control expense rather than alloy-feedstock scarcity. N₂ presents an oxygen-displacement/asphyxiation risk, including from cryogenic liquid; laser exposure to air can generate hazardous NOₓ, alongside ordinary Cu/alloy-metal particulate fume. N itself is not an identified RoHS alloying-element prohibition or a demonstrated Navy-imposed Cu-alloy N maximum; local OSHA ventilation, oxygen monitoring and applicable exposure requirements must be assessed for the actual fume. [GAP] No numeric OSHA/REACH/Navy N-in-alloy limit was verified. The USGS *final 2025 list* is cited via its reproduction in a USGS mining review; N absence should not be confused with the importance of nitrogen fertilizer commodities. (staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 6-9, alter2023porenbildungbeimschweissen pages 101-106)

**[NUMBERS] Proposed LIMIT, both families: total N ≤0.0005 wt% (≤5 mass-ppm) in *each powder lot and deposit*, as an initial project-specific acceptance target, conditional on a validated method with a sufficiently low detection limit.** Set the procurement *aim* lower where practical; verify the retained specification against N-assay uncertainty and porosity/density results. **This 5-ppm value is an engineering screening choice, not a standard limit or a demonstrated universal pore threshold.** It is deliberately below the **22-ppm porous-weld specimen** and can be compared against the **1.5–2-ppm total N** found in two N₂-spray-formed bronzes; the latter were porous spray billets, *not proof that 2 ppm is safe in DED*. A negative result at ≤5 ppm must trigger stricter controls rather than acceptance by chemistry alone: shielding uptake can occur after powder analysis, and bulk N can include pore gas or nitrides. Failure mode setting the proposed ceiling: rejection of N during solidification, aggravated by N–O-related pore formation and potential nitride inclusions; **no distinct N-driven cracking or seawater-corrosion threshold has been established**. Conservative/nonconservative designed-addition bounds and a functional floor are **NA**, since no beneficial designed N addition is substantiated. (alter2023porenbildungbeimschweissen pages 110-114, muller2004effectofreactive pages 6-8, alter2023porenbildungbeimschweissen pages 38-42, alter2023porenbildungbeimschweissen pages 101-106)

**Evidence quality — thin for the alloy-design decision, despite substantial direct evidence for Cu laser-welding porosity.** Principal limitations are the lack of N-composition seawater series, direct Cu–Ni/NAB blown-powder DED comparisons, validated N limits in the requested alloy specifications, and verified N-bearing CALPHAD assessments. The apparent conflict between reports calling N₂ effectively insoluble in Cu and laser studies finding N pickup reflects different *molecular-gas versus hot-liquid/laser* conditions; the 22-ppm measurement further includes N retained in a porous specimen, not necessarily N in the Cu lattice. (konynenburg1990backgroundstudiesin pages 142-149, alter2023porenbildungbeimschweissen pages 110-114, alter2023porenbildungbeimschweissen pages 38-42, muller2004effectofreactive pages 6-8)

VERDICT | N | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.0005 | evidence=thin

References

1. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

2. (alter2023porenbildungbeimschweissen pages 93-97): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

3. (alter2023porenbildungbeimschweissen pages 110-114): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

4. (ji2010crystallinethinfilms pages 1-2): Ailing Ji, Du Yun, Lei Gao, and Zexian Cao. Crystalline thin films of stoichiometric cu3n and intercalated cu3nmx (m = metals): growth and physical properties. physica status solidi (a), 207:2769-2780, Dec 2010. URL: https://doi.org/10.1002/pssa.201026449, doi:10.1002/pssa.201026449. This article has 25 citations.

5. (muller2004effectofreactive pages 1-4): Hilmar R. Müller, Klaus Ohla, Robert Zauter, and Michael Ebner. Effect of reactive elements on porosity in spray-formed copper-alloy billets. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 383:78-86, Oct 2004. URL: https://doi.org/10.1016/j.msea.2004.02.060, doi:10.1016/j.msea.2004.02.060. This article has 21 citations.

6. (muller2004effectofreactive pages 4-6): Hilmar R. Müller, Klaus Ohla, Robert Zauter, and Michael Ebner. Effect of reactive elements on porosity in spray-formed copper-alloy billets. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 383:78-86, Oct 2004. URL: https://doi.org/10.1016/j.msea.2004.02.060, doi:10.1016/j.msea.2004.02.060. This article has 21 citations.

7. (mccright1988anannotatedhistory pages 57-58): R. D. McCright. An annotated history of container candidate material selection. ArXiv, Jul 1988. URL: https://doi.org/10.2172/60703, doi:10.2172/60703. This article has 11 citations.

8. (yushchenko2010effectofnanofoil pages 38-39): KA Yushchenko, AI Ustinov, and BA Zadery. Effect of nanofoil of ni—nbc system on structure of electron beam welds in heat-resistant alloys. Unknown journal, 2010.

9. (muller2004effectofreactive pages 6-8): Hilmar R. Müller, Klaus Ohla, Robert Zauter, and Michael Ebner. Effect of reactive elements on porosity in spray-formed copper-alloy billets. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 383:78-86, Oct 2004. URL: https://doi.org/10.1016/j.msea.2004.02.060, doi:10.1016/j.msea.2004.02.060. This article has 21 citations.

10. (alter2023porenbildungbeimschweissen pages 101-106): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

11. (alter2023porenbildungbeimschweissen pages 97-101): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

12. (alter2023porenbildungbeimschweissen pages 106-110): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

13. (alter2023porenbildungbeimschweissen pages 118-122): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

14. (alter2023porenbildungbeimschweissen pages 122-126): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

15. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

16. (alter2023porenbildungbeimschweissen pages 126-130): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

17. (alter2023porenbildungbeimschweissen pages 38-42): L Alter. Porenbildung beim schweißen von kupferwerkstoffen unter verwendung von laserstrahlung im grünen wellenlängenbereich. Unknown journal, 2023.

18. (siwka2008equilibriumconstantsand pages 4-5): Jerzy Siwka. Equilibrium constants and nitrogen activity in liquid metals and iron alloys. Isij International, 48:385-394, Apr 2008. URL: https://doi.org/10.2355/isijinternational.48.385, doi:10.2355/isijinternational.48.385. This article has 44 citations and is from a peer-reviewed journal.

19. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

20. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.
