<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 9e90a308-d5e0-42c9-be5e-563efae592fa
- Submitted: 2026-10-17T19:01:00Z
- Fetched: 2026-10-17T19:30:54Z (status: success)
- Raw trajectory JSON: ../raw/el-36-Ga.json.gz
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

ELEMENT UNDER REVIEW: Ga (solid solution). Cu-Ga alpha solid solution (wide); low melting point; gallium is a US critical mineral; any corrosion data for Cu-Ga or Cu-Ni-Ga.

Answer for Ga specifically, not for copper alloys in general:
1. ROLE: what Ga does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ga ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ga changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ga, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ga, Cu-Ni-Ga and Cu-Al-Ga are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ga in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ga neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ga | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ga (solid solution). Cu-Ga alpha solid solution (wide); low melting point; gallium is a US critical mineral; any corrosion data for Cu-Ga or Cu-Ni-Ga.

Answer for Ga specifically, not for copper alloys in general:
1. ROLE: what Ga does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ga ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ga changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ga, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ga, Cu-Ni-Ga and Cu-Al-Ga are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ga in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ga neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ga | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Gallium (Ga): composition-palette decision

**Decision: LIMIT as an uncontrolled impurity; do not designate Ga as a corrosion or crack-control addition.** This is an evidence-limited decision, not a finding that a particular Ga concentration damages a marine copper alloy. The accessible Ga-specific work establishes Cu-rich solid solution and potentially brittle Cu–Ga reaction products, but does not establish improved *as-deposited* seawater performance, a qualified marine weld, or a permissible Ga concentration for the proposed process. Low-temperature liquid-Ga soldering results must not be presented as laser-DED results. [CITE] (gomidzelovic2016analyticapproachto pages 3-6, liu2018gabasedalloysin pages 10-13, liu2018gabasedalloysin pages 8-10)

The following matrix separates measured findings from process extrapolations and missing evidence.

| Evidence area | Ga-specific finding | Evidence type / applicability | Evidence gap or failure mode | Decision consequence |
|---|---|---|---|---|
| Commercial marine-alloy specifications | No intentional Ga range was identified in ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449, or relevant UNS/CDA compositions for Cu-Ni, aluminum bronze/NAB, Mn-Al bronze, tin bronze/gunmetal, brasses, Cu-Ni-Sn, or Cu-Ni-Si. | Direct specification search; no qualifying Navy or commercial precedent found. | [GAP] No specification establishes either a beneficial Ga addition or a tolerable Ga impurity concentration in marine Cu alloys. | No specification-based conservative design bound is available. |
| Cu-Ga phase stability | Ga has substantial solubility in FCC Cu, but the retrieved sources do not quantify the equilibrium maximum reliably. A demonstrated Cu-20 wt% Ga solid-solution powder is only a reaction starting material, not proof of maximum solubility. Verified products include brittle theta-CuGa2 and gamma-Cu9Ga4; liquid-Ga/Cu reactions produced CuGa2 at 200 degrees C and CuGa2/Cu9Ga4 over 160-300 degrees C. Liu et al., Materials 11 (2018) 1384, DOI 10.3390/ma11081384 (liu2018gabasedalloysin pages 10-13, liu2018gabasedalloysin pages 8-10). | Indirect microelectronics and diffusion-bonding evidence; relevant to phase formation but not DED solidification. | Intermetallic formation, brittle films, Kirkendall voids, and residual low-melting segregate are credible risks; exact Cu-rich solvus and multicomponent DED phase boundaries remain unverified. | Do not use 20 wt% as a bound. Phase evidence argues against intentional Ga until CALPHAD and rapid-solidification validation are completed. |
| Seawater corrosion | No quantitative study was found for Ga-bearing Cu-Ga, Cu-Ni-Ga, or Cu-Al-Ga bulk alloys in natural seawater, ASTM D1141 solution, or 3.5 wt% NaCl. No Ga-dependent corrosion rate, corrosion potential, polarization resistance, film resistance, pitting or crevice threshold, selective-attack depth, erosion-corrosion result, or velocity limit was identified. | Explicit direct-evidence gap. | [GAP] No evidence that Ga forms a protective marine film, inhibits dealloying, or meets or exceeds wrought C71500 as deposited; beneficial and harmful composition ranges cannot be assigned. | Ga cannot presently be credited toward the proposal's corrosion objective. |
| Laser DED and welding | No Ga-alloyed Cu DED, laser-cladding, or ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl weld study was found. Low-temperature Cu-Ga joining instead shows brittle CuGa2/Cu9Ga4 regions, cracks, and Kirkendall voids. Liu et al., DOI 10.3390/ma11081384 (liu2018gabasedalloysin pages 6-8, liu2018gabasedalloysin pages 10-13). | Indirect microelectronics evidence, not fusion welding or AM. | [GAP] Effects on DED solidification cracking, reheating or liquation cracking, keyhole porosity, Ga oxidation or evaporation, and dilution into C95800 or C71500 are unmeasured. | Treat Ga segregation and low-melting grain-boundary liquid as risks, not demonstrated grain refinement or crack control. |
| Crucibles and Ti/Mo sonotrode | Historical elemental-liquid-Ga tests found alumina satisfactory to at least 1000 degrees C and graphite or stabilized zirconia satisfactory to about 800 degrees C; these were not Cu-Ga melt tests. Mo reacted at 600 degrees C and was severely attacked or completely reacted at 800 degrees C; Ti disintegrated in Ga after 337 h at 450 degrees C. Wilkinson, ANL-5027, DOI 10.2172/4407475 (wilkinson1953effectsofgallium pages 6-9, wilkinson1953effectsofgallium pages 1-6, wilkinson1953effectsofgallium pages 19-22). | Direct elemental-Ga compatibility tests, but indirect for dilute Ga in a Cu-rich melt and short ultrasonic-atomization exposures. | [GAP] No measured attack rate exists for alumina or zirconia crucibles or Ti-alloy/Mo rePOWDER sonotrodes in Cu-Ga melts near 1200-1300 degrees C; sonotrode contamination and Ga loss are unknown. | Alumina or zirconia appears preferable to exposed Ti or Mo, but every Ga heat would require post-atomization chemistry and hardware inspection. |
| Supply and cost | The United States was entirely import-reliant for Ga; China supplied 98% of 2024 global production and held 87% of primary low-purity capacity. USGS Scientific Investigations Report 2025-5021, DOI 10.3133/sir20255021 (alonso2025worldmineralsoutlook—cobalt pages 15-17). A later USGS-derived chart gives an apparent cumulative import price near US$500/kg in 2024 and US$580/kg in 2025, although series assignment is imperfect (kumar2026lessonsfromchinasc pages 8-11). | Direct authoritative supply data; secondary presentation of price data. | Critical-mineral concentration and price volatility conflict with adding Ga where no marine benefit is demonstrated. | Supply risk reinforces impurity control rather than intentional alloying. |
| Overall decision and bound | LIMIT as an uncontrolled impurity only. | Evidence-weighted conclusion. | There is no experimentally supported numerical marine impurity tolerance and no applicable specification limit; inventing an allowable ppm or wt% value would be unjustified. | impurity_max_wt = NA pending qualification through controlled Ga ladders, deposit chemistry, crack and porosity assessment, ASTM D1141 electrochemistry and immersion, and substrate-dilution testing. |


*Table: Evidence matrix for gallium in Cu-balance marine directed-energy-deposition alloys, distinguishing direct results from indirect microelectronics or elemental-Ga tests. The evidence supports limiting Ga as an uncontrolled impurity, with no numerical maximum assigned pending qualification.*

## 1. Role and specified alloys

**[CITE] [NUMBERS]** Ga can enter a Cu-rich solid solution: Liu *et al.* describe a **Cu–20 wt% Ga solid-solution powder** used as a starting material in a liquid-Ga reaction. That is **not** a measured maximum equilibrium solubility, a suitable DED composition, or evidence of seawater protection. The same review identifies Cu₉Ga₄ and brittle CuGa₂ reaction products; a separate Ga–Al–Ni-paste diffusion joint to Cu/Ni contained Ni₃Ga, Cu₃Ga and Cu solid solution. These observations establish possible solid-solution and intermetallic mechanisms, not useful precipitate strengthening of an as-deposited marine alloy. [CITE] Liu, Sweatman, McDonald and Nogita, “Ga-Based Alloys in Microelectronic Interconnects: A Review,” *Materials* **11** (2018), 1384, DOI **10.3390/ma11081384**. (liu2018gabasedalloysin pages 3-6, liu2018gabasedalloysin pages 6-8, liu2018gabasedalloysin pages 10-13, liu2018gabasedalloysin pages 8-10)

**[SPEC] [NAVY] [GAP]** No *intentional* Ga composition range was verified for C71500/Cu–Ni, C95800/NAB or the other specified marine families—Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn and Cu–Ni–Si—or for the named filler classes ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl. Accordingly, **no Ga-bearing commercial or Navy grade and no Ga range in wt% can be responsibly listed** from ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449 or UNS/CDA data on the evidence retrieved. This is *not* a claim that every edition of every specification prohibits trace Ga: a missing intentional addition is not an impurity limit. There is likewise no demonstrated Ga-specific deoxidation, grain refinement, chloride-film modification or dealloying inhibition in these families. The documented application of the Cu–Ga–Ni ternary work is predominantly solder/interconnect metallurgy, not Navy seawater service. (gomidzelovic2016analyticapproachto pages 1-2, liu2018gabasedalloysin pages 8-10)

## 2. Seawater corrosion

**[GAP]** No usable head-to-head dataset was found for bulk, Ga-alloyed Cu–Ga, Cu–Ni–Ga or Cu–Al–Ga versus its Ga-free parent alloy in natural seawater, ASTM D1141 substitute seawater or **3.5 wt% NaCl**. Consequently, neither a helpful nor a harmful **Ga range in wt%** is experimentally assignable. Specifically unavailable are Ga-dependent corrosion rates, *E*₍corr₎, polarization or film resistance, pit or crevice potentials, selective-attack depth, erosion-corrosion and velocity limits. There is no evidence that a Ga-bearing deposit equals or exceeds wrought C71500 after 30 days as deposited. Liquid-Ga attack on solid Cu is **not** a seawater-corrosion measurement; neither are results for Ga-activated aluminum sacrificial anodes or Ga-containing dental alloys. (wilkinson1953effectsofgallium pages 26-29, liu2018gabasedalloysin pages 10-13)

## 3. DED, welding and repair dilution

**[CITE] [GAP]** No Ga-controlled blown-powder Cu-alloy DED or applicable marine filler weld experiment was identified that measures solidification cracking, reheated-layer liquation cracking, porosity, evaporation or oxide loss. The nearest Ga-specific joining evidence instead concerns **160–300 °C** Cu/liquid-Ga diffusion couples and electronic interconnects: CuGa₂ and Cu₉Ga₄ form, with reported cracks in intermetallic regions and Kirkendall voids. These establish *plausible failure mechanisms*, not a measured DED cracking threshold. Liu *et al.*, *Materials* **11** (2018), 1384, DOI **10.3390/ma11081384**. (liu2018gabasedalloysin pages 3-6, liu2018gabasedalloysin pages 10-13, liu2018gabasedalloysin pages 8-10)

**[GAP]** For C95800 repair, dilution would add Al, Ni, Fe and Mn to a Cu–Ga melt; for wrought Cu–Ni repair it would add Ni and possible Fe/Mn. Whether either fusion boundary forms Ga-enriched terminal liquid, Ni–Ga compounds, brittle Cu–Ga compounds, porosity or a galvanically unfavorable transition zone is **unmeasured**. The solder literature does not establish that Ga prevents cracks in either substrate. Report any future first-layer and reheated-layer cracking separately from bulk deposit cracking, and assay Ga in feedstock, deposit and fusion boundary rather than assuming charge equals deposited composition. (liu2018gabasedalloysin pages 6-8, liu2018gabasedalloysin pages 10-13, gomidzelovic2016analyticapproachto pages 1-2)

## 4. Induction melting, atomization and hardware

**[CITE] [NUMBERS]** In historical **elemental liquid-Ga contact** tests, Al₂O₃ contained Ga to at least **1,000 °C**, and stabilized ZrO₂ and graphite were reported satisfactory to approximately **800 °C**. By contrast, Mo reacted at **600 °C** and was severely attacked or completely reacted at **800 °C**; Ti disintegrated after **337 h at 450 °C**. These temperatures and exposure times are **not** compatibility ratings for an Al₂O₃/ZrO₂ crucible or Ti-alloy/Mo sonotrode in a Cu-rich melt near **1,200–1,300 °C**. Wilkinson, *Effects of Gallium on Materials at Elevated Temperatures*, Argonne report, 1953, DOI **10.2172/4407475**. (wilkinson1953effectsofgallium pages 6-9, wilkinson1953effectsofgallium pages 1-6, wilkinson1953effectsofgallium pages 19-22)

**[CITE] [GAP]** Oxidation/slag uptake is credible, not a quantified charge-loss prediction: equilibrium black-copper/oxide-slag experiments at **1,300–1,450 °C** and oxygen partial pressures **10⁻⁶–10⁻¹¹ atm** found greater Ga retention in the Cu phase under more reducing conditions. They do not establish the rate in argon induction atomization, the extent of Ga₂O₃ skin formation, crucible pickup, Ga vaporization, or a Ga-dependent melt surface tension and ultrasonic droplet-size shift. The melting point of *elemental* Ga, approximately **29.8 °C**, does not imply that a **Cu-rich pre-alloyed powder** is liquid near room temperature. Hasan, Rhamdhani and Brooks, “Thermodynamics of Gallium (Ga) at Black Copper Smelting Conditions Relevant to E-Waste Processing,” *Metallurgical and Materials Transactions B* **53** (2022), 3136–3146, DOI **10.1007/s11663-022-02593-4**; Gomidželović *et al.*, cited below. (hasan2022thermodynamicsofgallium pages 1-2, hasan2022thermodynamicsofgallium pages 9-10, gomidzelovic2016analyticapproachto pages 3-6)

## 5. Phases, liquidus and CALPHAD

**[CITE] [NUMBERS]** The Cu-rich FCC solid solution is real, but the sources obtained **do not establish its maximum Ga solubility in wt% and corresponding temperature**. The observed Cu–20 wt% Ga solid-solution *starting powder* must not be substituted for that solvus. Identified Cu–Ga reaction phases include Cu₉Ga₄ and CuGa₂, and a Ga–Al–Ni-paste joint also showed Cu₃Ga; accessible reports do **not** give a reliable complete set of binary invariant temperatures/compositions. Specifically, low-temperature liquid-Ga/Cu contact generated CuGa₂ at **200 °C** and combinations of CuGa₂/Cu₉Ga₄ over approximately **160–300 °C**. These are kinetic joining observations, **not invariant-reaction measurements**. Liu *et al.*, DOI **10.3390/ma11081384**. A dedicated binary assessment exists: J. Li *et al.*, “A thermodynamic assessment of the copper–gallium system,” *CALPHAD* **32** (2008), 447–453, DOI **10.1016/j.calphad.2008.03.006**; its numerical phase boundaries could not be independently checked in retrieved full text. (liu2018gabasedalloysin pages 3-6, liu2018gabasedalloysin pages 6-8, liu2018gabasedalloysin pages 10-13, liu2018gabasedalloysin pages 8-10)

**[CITE] [NUMBERS]** Gomidželović *et al.* calculated Cu–Ga–Ni liquid thermodynamics over **1,473–2,073 K** and a **298 K** ternary section with **11 phases** using Thermo-Calc **SSOL5**; that section is illustrated in their Figure 6. Thus “no CALPHAD treatment of Cu–Ni–Ga exists” would be wrong. But this does **not** verify a fitted, experimentally validated ternary description for the Cu-rich rapid-solidification region, nor Ga availability or assessed Cu–Ga/Cu–Ni–Ga/Cu–Al–Ga interactions in the laboratory’s particular **TCCU** installation or **COST 531**. L. Gomidželović, A. Kostov, D. Živković and V. Krstić, “Analytic Approach to Alloys Thermodynamics: Ternary Cu-Ga-Ni System,” *Materials Research* **19** (2016), 1026–1032, DOI **10.1590/1980-5373-MR-2015-0238**. Check the installed TCCU element list and phase models, inspect any TDB provenance, and calculate *both* equilibrium and Scheil paths for the actual Ni/Al/Fe/Mn compositions. (gomidzelovic2016analyticapproachto pages 3-6, gomidzelovic2016analyticapproachto media dc02ee7b, gomidzelovic2016analyticapproachto pages 1-2)

**[GAP]** A Cu-rich Ga addition cannot be claimed either to exceed or remain below the instrument’s **~1,250 °C liquidus/superheat ceiling** on these data: obtain an actual multicomponent liquidus before charging. The low melting point of pure Ga is not an adequate liquidus calculation. (gomidzelovic2016analyticapproachto pages 3-6, liu2018gabasedalloysin pages 8-10)

## 6. Supply, cost, safety and interactions

**[CITE] [NUMBERS]** Ga is identified as a supply-risk critical mineral in the retrieved USGS analysis; its inclusion in the **2022** and **2025 final** U.S. lists should be verified against the respective *Federal Register* notices when those notices are cited formally. The USGS reports **98%** of world Ga production in China in **2024**, **87%** of world primary low-purity capacity there and complete U.S. import reliance for domestic use. E. Alonso *et al.*, *World Minerals Outlook—Cobalt, Gallium, Helium, Lithium, Magnesium, Palladium, Platinum, and Titanium Through 2029*, USGS Scientific Investigations Report **2025-5021**, DOI **10.3133/sir20255021**. (hasan2022thermodynamicsofgallium pages 1-2, alonso2025worldmineralsoutlook—cobalt pages 15-17)

**[NUMBERS] [GAP]** A secondary chart derived from USGS import data suggests approximately **US$500/kg in 2024** and **US$580/kg in 2025** for the aggregate import-price series; its rendering does not establish a reliable same-grade purchase quotation or high-purity/low-purity comparison. Treat these as *indicative*, not a 0.5-kg laboratory procurement quote. No verified Ga-specific OSHA permissible exposure limit, RoHS/REACH prohibition or Navy restriction was identified; do **not** infer that Ga powder or mixed laser fume is harmless from the low toxicity ascribed to bulk Ga in an electronics review. Apply enclosed powder handling, particulate/fume capture and applicable local exposure assessment without inventing a Ga-specific legal threshold. (liu2018gabasedalloysin pages 1-3, alonso2025worldmineralsoutlook—cobalt pages 15-17, kumar2026lessonsfromchinas media c9f144e7, kumar2026lessonsfromchinasc pages 8-11)

**[CITE] [GAP]** For later joint constraints, track the **Ga:Ni ratio**, **Ga plus Al**, and local **Ga:Cu** after dilution: Ni₃Ga and Cu₃Ga were observed in a Ga/Al/Ni-containing *joining paste*, while Cu₉Ga₄/CuGa₂ can consume Cu in other interfacial reactions. This supports screening for competing phases, **not** a validated numerical sum/ratio or a conclusion that Ni or Al neutralizes Ga. No Ga–Fe or Ga–Mn protective synergy, or validated effect on NAB dealloying, was identified. (liu2018gabasedalloysin pages 3-6, liu2018gabasedalloysin pages 6-8, gomidzelovic2016analyticapproachto pages 1-2)

## 7. Bounds and evidence quality

**LIMIT, both substrate families; no defensible numerical impurity maximum.** Specify *no intentional Ga addition* and require measured Ga in powder and deposit. An enforceable **maximum tolerable wt% or ppm cannot be attributed to any verified named marine specification or Ga-controlled DED/corrosion study**; therefore the evidence-based entry is **NA**, not a fabricated threshold. A purchasing instruction such as “as low as reasonably achievable, report detection limit and batch assay” is a *management choice*, not an established corrosion-safe composition. The failure modes governing future qualification are possible Ga-enriched boundary films/intermetallic brittleness, uncertain laser/sonotrode losses, and—most decisively—unknown as-deposited seawater corrosion relative to C71500. No conservative designed-addition maximum, non-conservative maximum or functional floor applies under **LIMIT**. Evidence for Ga metallurgy is real, but evidence for the proposed marine alloy and process is **thin**. (gomidzelovic2016analyticapproachto pages 3-6, liu2018gabasedalloysin pages 10-13, alonso2025worldmineralsoutlook—cobalt pages 15-17, wilkinson1953effectsofgallium pages 19-22, liu2018gabasedalloysin pages 8-10)

VERDICT | Ga | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (gomidzelovic2016analyticapproachto pages 3-6): Lidija Gomidželović, Ana Kostov, Dragana Živković, and Vesna Krstić. Analytic approach to alloys thermodynamics: ternary cu-ga-ni system. Materials Research-ibero-american Journal of Materials, 19:1026-1032, Aug 2016. URL: https://doi.org/10.1590/1980-5373-mr-2015-0238, doi:10.1590/1980-5373-mr-2015-0238. This article has 11 citations.

2. (liu2018gabasedalloysin pages 10-13): Shiqian Liu, Keith Sweatman, Stuart McDonald, and Kazuhiro Nogita. Ga-based alloys in microelectronic interconnects: a review. Materials, 11:1384, Aug 2018. URL: https://doi.org/10.3390/ma11081384, doi:10.3390/ma11081384. This article has 154 citations.

3. (liu2018gabasedalloysin pages 8-10): Shiqian Liu, Keith Sweatman, Stuart McDonald, and Kazuhiro Nogita. Ga-based alloys in microelectronic interconnects: a review. Materials, 11:1384, Aug 2018. URL: https://doi.org/10.3390/ma11081384, doi:10.3390/ma11081384. This article has 154 citations.

4. (liu2018gabasedalloysin pages 6-8): Shiqian Liu, Keith Sweatman, Stuart McDonald, and Kazuhiro Nogita. Ga-based alloys in microelectronic interconnects: a review. Materials, 11:1384, Aug 2018. URL: https://doi.org/10.3390/ma11081384, doi:10.3390/ma11081384. This article has 154 citations.

5. (wilkinson1953effectsofgallium pages 6-9): W. D. Wilkinson. Effects of gallium on materials at elevated temperatures. ArXiv, Aug 1953. URL: https://doi.org/10.2172/4407475, doi:10.2172/4407475. This article has 16 citations.

6. (wilkinson1953effectsofgallium pages 1-6): W. D. Wilkinson. Effects of gallium on materials at elevated temperatures. ArXiv, Aug 1953. URL: https://doi.org/10.2172/4407475, doi:10.2172/4407475. This article has 16 citations.

7. (wilkinson1953effectsofgallium pages 19-22): W. D. Wilkinson. Effects of gallium on materials at elevated temperatures. ArXiv, Aug 1953. URL: https://doi.org/10.2172/4407475, doi:10.2172/4407475. This article has 16 citations.

8. (alonso2025worldmineralsoutlook—cobalt pages 15-17): Elisa Alonso, Amanda Sarah Brioche, Ruth Schulte, Loyd M. Trimmer, Ji-Eun Kim, Andrew L. Gulley, and David George Pineault. World minerals outlook—cobalt, gallium, helium, lithium, magnesium, palladium, platinum, and titanium through 2029. Scientific Investigations Report, Jan 2025. URL: https://doi.org/10.3133/sir20255021, doi:10.3133/sir20255021. This article has 25 citations.

9. (kumar2026lessonsfromchinasc pages 8-11): A Kumar and P Kotasthane. Lessons from china's weaponisation of critical minerals: a case study of gallium and germanium. Unknown journal, 2026.

10. (liu2018gabasedalloysin pages 3-6): Shiqian Liu, Keith Sweatman, Stuart McDonald, and Kazuhiro Nogita. Ga-based alloys in microelectronic interconnects: a review. Materials, 11:1384, Aug 2018. URL: https://doi.org/10.3390/ma11081384, doi:10.3390/ma11081384. This article has 154 citations.

11. (gomidzelovic2016analyticapproachto pages 1-2): Lidija Gomidželović, Ana Kostov, Dragana Živković, and Vesna Krstić. Analytic approach to alloys thermodynamics: ternary cu-ga-ni system. Materials Research-ibero-american Journal of Materials, 19:1026-1032, Aug 2016. URL: https://doi.org/10.1590/1980-5373-mr-2015-0238, doi:10.1590/1980-5373-mr-2015-0238. This article has 11 citations.

12. (wilkinson1953effectsofgallium pages 26-29): W. D. Wilkinson. Effects of gallium on materials at elevated temperatures. ArXiv, Aug 1953. URL: https://doi.org/10.2172/4407475, doi:10.2172/4407475. This article has 16 citations.

13. (hasan2022thermodynamicsofgallium pages 1-2): Mohammad Mehedi Hasan, M. Akbar Rhamdhani, and Geoffrey A. Brooks. Thermodynamics of gallium (ga) at black copper smelting conditions relevant to e-waste processing. Metallurgical and Materials Transactions B, 53:3136-3146, Jul 2022. URL: https://doi.org/10.1007/s11663-022-02593-4, doi:10.1007/s11663-022-02593-4. This article has 9 citations.

14. (hasan2022thermodynamicsofgallium pages 9-10): Mohammad Mehedi Hasan, M. Akbar Rhamdhani, and Geoffrey A. Brooks. Thermodynamics of gallium (ga) at black copper smelting conditions relevant to e-waste processing. Metallurgical and Materials Transactions B, 53:3136-3146, Jul 2022. URL: https://doi.org/10.1007/s11663-022-02593-4, doi:10.1007/s11663-022-02593-4. This article has 9 citations.

15. (gomidzelovic2016analyticapproachto media dc02ee7b): Lidija Gomidželović, Ana Kostov, Dragana Živković, and Vesna Krstić. Analytic approach to alloys thermodynamics: ternary cu-ga-ni system. Materials Research-ibero-american Journal of Materials, 19:1026-1032, Aug 2016. URL: https://doi.org/10.1590/1980-5373-mr-2015-0238, doi:10.1590/1980-5373-mr-2015-0238. This article has 11 citations.

16. (liu2018gabasedalloysin pages 1-3): Shiqian Liu, Keith Sweatman, Stuart McDonald, and Kazuhiro Nogita. Ga-based alloys in microelectronic interconnects: a review. Materials, 11:1384, Aug 2018. URL: https://doi.org/10.3390/ma11081384, doi:10.3390/ma11081384. This article has 154 citations.

17. (kumar2026lessonsfromchinas media c9f144e7): A Kumar and P Kotasthane. Lessons from china's weaponisation of critical minerals: a case study of gallium and germanium. Unknown journal, 2026.
