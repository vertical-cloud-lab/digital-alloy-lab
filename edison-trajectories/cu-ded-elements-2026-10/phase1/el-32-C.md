<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 2060f087-32ba-4df8-953a-80b9ed319042
- Submitted: 2026-10-17T19:00:49Z
- Fetched: 2026-10-17T19:30:51Z (status: success)
- Raw trajectory JSON: ../raw/el-32-C.json.gz
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

ELEMENT UNDER REVIEW: C (interstitial / gas). C71500 limits C to 0.05 wt%; carbon is picked up from graphite crucibles or carbon-fiber sonotrodes; carbon solubility in Cu is tiny but higher in Ni-rich melts; graphite flakes and carbides with Cr, Ti, Nb. Answer as an impurity limit.

Answer for C specifically, not for copper alloys in general:
1. ROLE: what C does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their C ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how C changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-C, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-C, Cu-Ni-C and Cu-Al-C are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of C in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that C neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | C | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: C (interstitial / gas). C71500 limits C to 0.05 wt%; carbon is picked up from graphite crucibles or carbon-fiber sonotrodes; carbon solubility in Cu is tiny but higher in Ni-rich melts; graphite flakes and carbides with Cr, Ti, Nb. Answer as an impurity limit.

Answer for C specifically, not for copper alloys in general:
1. ROLE: what C does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their C ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how C changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-C, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-C, Cu-Ni-C and Cu-Al-C are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of C in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that C neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | C | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Carbon (C): impurity limit for marine copper-alloy DED

**Decision: LIMIT, for both Cu–Ni and aluminum-bronze candidates.** Carbon has no established beneficial alloying function for the specified *as-deposited*, seawater-exposed material. A published metallurgical assessment classifies C as detrimental in copper, aluminum bronzes, and Cu–Ni; a directly relevant study reports defects from precipitation of carbon dissolved in molten Cu–Ni–Al bronze, although its full results were unavailable for this review. Neither an improvement in seawater corrosion nor a safe DED concentration has been demonstrated. The limit below is therefore a **proposed research acceptance criterion**, not a claimed ASTM, AWS, or Navy requirement. [CITE] Van Konynenburg *et al.*, *Background Studies in Support of a Feasibility Assessment on the Use of Copper-Base Materials for Nuclear Waste Packages* (1990), DOI: **10.2172/137782**; [CITE] Wenschot, “Defects Caused by Precipitation of in Liquid Copper–Nickel–Aluminium–Bronze Alloys Dissolved Carbon and Removal by Treatment of Melt,” *International Journal of Cast Metals Research* **27**, 65–72 (2014), DOI: **10.1179/1743133613Y.0000000080**. (konynenburg1990backgroundstudiesin pages 142-149, thongyothee2025theeffectof pages 7-7)

## 1. Role and applicable alloys

In Cu-rich metal, C is principally a **melt contaminant and potential graphite or carbide constituent**, not a practical Cu-matrix solid-solution strengthener, protective-film dopant, or established inhibitor of dealloying. Graphite-contact melting is an identified source; a published assessment also proposes CO-cavity formation when retained C reacts with O. Its classification of C as detrimental applies to copper, Cu–Ni, and aluminum bronze; the directly relevant NAB casting paper identifies carbon-precipitation defects, but its unavailable full text prevents assigning a defect-onset concentration. These are **casting and melting** observations, not C-controlled DED results. [CITE] Van Konynenburg *et al.* (1990), DOI: **10.2172/137782**; [CITE] Wenschot (2014), DOI: **10.1179/1743133613Y.0000000080**. (konynenburg1990backgroundstudiesin pages 136-142, konynenburg1990backgroundstudiesin pages 142-149, thongyothee2025theeffectof pages 7-7)

**[SPEC][GAP] Commercial and Navy range audit:** The relevant comparison grades include wrought C71500 (70–30 Cu–Ni; ASTM B111/B171/B466 as applicable), C70600 (90–10 Cu–Ni; ASTM B111/B466), cast C95800 NAB (ASTM B148), and AWS A5.7 ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl repair consumables. **No verified C range for any of those grades was recoverable from the accessible specification tables.** In particular, the supplied **C71500 ≤0.05 wt% C** assertion should be checked against the controlling purchased-product specification: this search did **not** substantiate attributing that number to ASTM B111, B171, B466, or AWS A5.7. Nor was a C range established for Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. Their use in seawater is not evidence that they deliberately contain carbon. The accessible welding assessment describes Cu–Ni and aluminum-bronze filler chemistry but supplies no C specification. [CITE] Van Konynenburg *et al.* (1990), DOI: **10.2172/137782**. (konynenburg1990backgroundstudiesin pages 136-142, konynenburg1990backgroundstudiesin pages 142-149)

**Interactions.** Ni permits substantially more C uptake than Cu in the respective pure-metal melts; this is a *directional warning*, not a calibrated Ni:C acceptance ratio for Cu–Ni powder. Strong carbide formers, particularly Ti and potentially Cr or Nb where present, can convert available C into particles rather than eliminate the impurity. Guo *et al.* directly produced TiCₓ by reacting graphite with Cu–Ti liquid; that is evidence for a particle-forming interaction, **not** for improved seawater durability of an NAB deposit. C–O interaction can instead produce CO porosity. No defensible numerical constraint involving C+Ni, C+Fe, C+Mn, or C+Al was found. [CITE] Amini *et al.*, “Growth of Graphene and Graphite Nanocrystals from a Molten Phase,” *Journal of Materials Science* **46**, 6255–6263 (2011), DOI: **10.1007/s10853-011-5432-9**; [CITE] Guo *et al.*, “Synthesis of Cu-Based TiCₓ Composites via In-Situ Reaction between CuₓTi Melt and Dissolvable Solid Carbon,” *Powder Technology* **362**, 375–385 (2020), DOI: **10.1016/j.powtec.2019.11.122**; [CITE] Van Konynenburg *et al.* (1990), DOI: **10.2172/137782**. (amini2011growthofgraphene pages 2-5, guo2020synthesisofcubased pages 7-12, konynenburg1990backgroundstudiesin pages 142-149)

## 2. Seawater corrosion: what can and cannot be quantified

**[GAP] No defensible beneficial or harmful C-composition interval can be assigned.** The retrieved literature supplies no controlled series varying **bulk C in a Cu-rich marine alloy** while measuring corrosion rate, E_corr, polarization resistance, impedance, pit/crevice depth, dealloying, or erosion–corrosion in natural seawater, ASTM D1141 water, or 3.5 wt% NaCl. Graphene-containing *polymer coatings* and graphite-reinforced composites are not evidence for interstitial C in a single-stream, pre-alloyed DED deposit. A marine galvanic-series guide places exposed **graphite above NAB and Cu–Ni** in nobility: electrically connected, seawater-accessible graphite inclusions are consequently a plausible local cathode, but the guide gives **no C concentration-to-pit-depth relationship**. [CITE] Francis, Turnbull and Hinds, *Bimetallic Corrosion: Guides for Good Practice in Corrosion Control No. 5* (2020; no DOI verified). (francis2020bimetalliccorrosion(guides pages 7-11, jena2020grapheneoxidechitosansilvercomposite pages 6-8)

**[NUMBERS] Benchmark, expressly *not* a carbon effect:** Lewis and LaQue report C71500 corrosion of **0.3–0.5 mil/year** (approximately **7.6–12.7 µm/year**) in quiet seawater and **0.5–0.7 mil/year** (approximately **12.7–17.8 µm/year**) at **0.61 m/s**, with reported pit depths of **1–2 mil** and **1–3 mil**, respectively. Their accepted maximum *tube design* velocity for a specified approximately **0.5 wt% Fe** C71500 is **4.6 m/s**; it is **not** a validated velocity limit for a new DED alloy. The film mechanism established for Cu–Ni is Ni/Fe incorporation into Cu₂O, not carbon-derived protection. Carbon was not varied in these comparisons. [CITE][NUMBERS] Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, Argonne National Laboratory report ANL/OTEC-BCM-019 (1981), DOI: **10.2172/6255887**. (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48)

## 3. DED, repair interfaces, and powder making

**[GAP]** No C-controlled blown-powder laser-DED experiment was located that separates C's contribution to **solidification cracking, reheated-layer liquation cracking, keyhole/gas porosity, selective evaporation, oxidation loss, or dilution** into C95800 versus wrought Cu–Ni. Welding provides a limited analogy: a welding technical report identifies trace-composition control for hot-cracking-prone C71500 and possible multipass porosity, while describing ERCuNi and ERCuAl-A2 practices; it **does not establish that C caused those cracks or provide a C threshold**. For Cu–Ni repair, test the diluted first layer separately from bulk deposit; for cast NAB, inspect the fusion boundary and reheated HAZ for graphite/carbides, pores, and cracks. Do not transfer a cast-material or weld-consumable limit to either interface without testing. [CITE] Robitz, McAninch and Edmonds, *Closure Development for High-Level Nuclear Waste Containers for the Tuff Repository: Phase 1, Final Report* (1990), DOI: **10.2172/138043**; [CITE] Wenschot (2014), DOI: **10.1179/1743133613Y.0000000080**. (thongyothee2025theeffectof pages 7-7, robitz1990closuredevelopmentfor pages 20-22)

For the proposed **argon induction-melt/ultrasonic-atomization** route, avoid graphite crucibles, graphite covers, and carbon-containing sonotrodes where practical. The copper-family assessment explicitly flags carbon absorption in Cu–Ni melting and the difficulty of refining aluminum bronze melts; graphite-contact experiments show surface/interface graphite rather than uniformly dissolved carbon in Cu-rich metal. Sample the **charge, atomized powder, and deposit**: melt chemistry alone cannot exclude entrained graphite particles. Graphite/carbon has no credible *selective vapor-loss correction* at the stated melt temperature, and neither a measured C-dependent surface-tension change nor a quantified reaction of C with alumina, zirconia, a titanium-alloy sonotrode, or a molybdenum sonotrode was found for this apparatus. TiC formation on Ti contamination is chemically plausible; Mo-carbide formation here remains unverified. [CITE] Van Konynenburg *et al.* (1990), DOI: **10.2172/137782**; [CITE] Amini *et al.* (2011), DOI: **10.1007/s10853-011-5432-9**; [CITE] Guo *et al.* (2020), DOI: **10.1016/j.powtec.2019.11.122**. (amini2011growthofgraphene pages 2-5, guo2020synthesisofcubased pages 7-12, konynenburg1990backgroundstudiesin pages 136-142, konynenburg1990backgroundstudiesin pages 142-149)

## 4. Phase diagram and CALPHAD

**[NUMBERS]** Deck and Vecchio quote approximately **0.0001 wt% C at 1100 °C in Cu**—about **1 mass ppm**—while explicitly noting that **1100 °C is above Cu's melting point**. **This is a liquid value, not the requested maximum solid solubility.** An independently verified numerical maximum for solid Cu, with its temperature, was **not found**; do not relabel the 1100 °C figure as such. Cu–C has no reported stable binary carbide in the retrieved melt study, which instead describes Cu-rich liquid plus graphite. The retrieved evidence does not establish a Cu–C invariant temperature or a quantitative C-induced liquidus shift. On this basis, trace C is *not demonstrated* to drive a Cu-rich candidate above **1250 °C**; a Ni-/Al-rich candidate must still pass its **full multicomponent** liquidus screen. [CITE][NUMBERS] Deck and Vecchio, “Prediction of Carbon Nanotube Growth Success by the Analysis of Carbon–Catalyst Binary Phase Diagrams,” *Carbon* **44**, 267–275 (2006), DOI: **10.1016/j.carbon.2005.07.023**; [CITE] Amini *et al.* (2011), DOI: **10.1007/s10853-011-5432-9**. (amini2011growthofgraphene pages 1-2, deck2006predictionofcarbon pages 5-6)

**[GAP] Database audit:** This review could not verify an assessed, interoperable **Cu–C, Cu–Ni–C, or Cu–Al–C** description in the installed Thermo-Calc **TCCU** release, **COST 531**, or an accessible published TDB. The presence of a `GRAPHITE` phase name or C in an element menu is **not proof** that the required binaries, ternaries, interstitial sublattices, and carbide phases are assessed consistently. Before accepting any pycalphad or Thermo-Calc output as a C solubility or liquidus constraint, inspect the actual licensed database's constituent definitions and parameter records, then compare its Cu–C result against the experimental/compiled liquid datum above. [CITE] Deck and Vecchio (2006), DOI: **10.1016/j.carbon.2005.07.023**. (deck2006predictionofcarbon pages 5-6)

## 5. Supply, safety, and proposed bound

**[CITE][NUMBERS]** *Graphite*, the mineral commodity, is distinct from “all carbon” as an alloying element. The USGS 2025-list methodology separately discusses natural and synthetic graphite and **recommends adding copper**; it is a technical input, **not proof of the wording of the final 2025 list**. An examined review identifies graphite and nickel as USGS-listed critical minerals, but a verified side-by-side reading of the **2022 and 2025 final lists** was unavailable here. Thus, do not label elemental impurity C itself a listed critical mineral. A reported **2024 natural-flake graphite** average of **US$1,070 per metric tonne ≈ US$1.07/kg** is a bulk mineral proxy, **not** a delivered high-purity charge-material price; reported synthetic graphite averaged approximately **US$4.55/kg**. At impurity levels, neither is an economic reason to add C. [CITE] Nassar *et al.*, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, USGS Open-File Report 2025–1047, DOI: **10.3133/ofr20251047**; [CITE] Paul, *Development of Coal-Derived Carbon Materials for Electrochemical Energy Storage Systems* (2026; DOI not verified). (nassar2025methodologyandtechnical pages 1-4, nassar2025methodologyandtechnical pages 33-35, paul2026developmentofcoalderived pages 15-19, paul2026developmentofcoalderived pages 19-24)

**[GAP]** No verified carbon-specific RoHS/REACH, Navy-prohibition, or OSHA graphite exposure-limit text was recovered; such a restriction must **not** be invented. Graphite is not equivalent to harmless inhalable dust. Assess respirable Cu/Ni-bearing atomization and laser fumes separately; contain powder, capture fumes, minimize dust clouds, and qualify the *actual powder size distribution*. A DOE dust review reports that very fine **0.2–2 µm carbon** had a measured minimum explosible concentration of **90 g/m³** and maximum explosion pressure of **5.5 bar** under its test conditions; that finding must not be extrapolated to the DED alloy powder without testing. [CITE][NUMBERS] Cadwallader, *Dust Combustion Safety Issues for Fusion Applications* (2003), DOI: **10.2172/910731**. (cadwallader2003dustcombustionsafety pages 14-18, cadwallader2003dustcombustionsafety pages 11-14)

**[NUMBERS] Proposed powder-and-deposit criterion: total C ≤0.005 wt% (≤50 mass ppm), both families; target ≤0.002 wt% (≤20 mass ppm) where achievable.** This is an intentionally conservative **engineering screening limit**, **not [SPEC]**: it is **50 times** the quoted approximately 0.0001 wt% *liquid pure-Cu* solubility at 1100 °C and therefore does **not** guarantee graphite-free metal, especially after segregation, dilution, or cooling. The failure modes motivating the limit are carbon precipitation/entrainment, carbide inclusions where carbide formers are present, and possible C–O-associated porosity. Neither a proven failure threshold at 0.005 wt% nor validation of the proposed target across Cu–Ni and NAB exists. Verify total C in **powder and deposit** by a suitable combustion-based method, and inspect inclusions and repair interfaces before treating the limit as qualified. No designed-addition conservative bound, aggressive bound, or functional floor is warranted. [CITE] Deck and Vecchio (2006), DOI: **10.1016/j.carbon.2005.07.023**; [CITE] Wenschot (2014), DOI: **10.1179/1743133613Y.0000000080**; [CITE] Van Konynenburg *et al.* (1990), DOI: **10.2172/137782**. (deck2006predictionofcarbon pages 5-6, konynenburg1990backgroundstudiesin pages 142-149, thongyothee2025theeffectof pages 7-7)

**Evidence quality: thin for the numerical bound and for corrosion/DED causality; moderate for treating C as an unwanted melting contaminant.** The central unresolved experiment is a controlled total-C series, made with the intended crucible and sonotrode, tested as deposited on both substrates against C71500 with inclusion identification and 30-day selective-attack depths. (deck2006predictionofcarbon pages 5-6, konynenburg1990backgroundstudiesin pages 142-149, thongyothee2025theeffectof pages 7-7, lewis1981evaluationofcoppernickel pages 43-48)

VERDICT | C | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.005 | evidence=thin

References

1. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

2. (thongyothee2025theeffectof pages 7-7): Chawanan Thongyothee and Sombun Chareonvilisiri. The effect of gas venting on the mechanical properties of c95800 aluminum bronze castings. Engineering, Technology &amp; Applied Science Research, Aug 2025. URL: https://doi.org/10.48084/etasr.10993, doi:10.48084/etasr.10993. This article has 1 citations and is from a peer-reviewed journal.

3. (konynenburg1990backgroundstudiesin pages 136-142): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

4. (amini2011growthofgraphene pages 2-5): Shaahin Amini, Haamun Kalaantari, Javier Garay, Alexander A. Balandin, and Reza Abbaschian. Growth of graphene and graphite nanocrystals from a molten phase. Journal of Materials Science, 46:6255-6263, Mar 2011. URL: https://doi.org/10.1007/s10853-011-5432-9, doi:10.1007/s10853-011-5432-9. This article has 50 citations and is from a peer-reviewed journal.

5. (guo2020synthesisofcubased pages 7-12): Lei Guo, Yang Yang, Xiaochun Wen, Han Gao, Zhe Wang, and Zhancheng Guo. Synthesis of cu-based ticx composites via in-situ reaction between cuxti melt and dissolvable solid carbon. Powder Technology, 362:375-385, Feb 2020. URL: https://doi.org/10.1016/j.powtec.2019.11.122, doi:10.1016/j.powtec.2019.11.122. This article has 28 citations and is from a domain leading peer-reviewed journal.

6. (francis2020bimetalliccorrosion(guides pages 7-11): R Francis, A Turnbull, and G Hinds. Bimetallic corrosion (guides for good practice in corrosion control no. 5). Unknown journal, 2020.

7. (jena2020grapheneoxidechitosansilvercomposite pages 6-8): Geetisubhra Jena, B. Anandkumar, S.C. Vanithakumari, R.P. George, John Philip, and G. Amarendra. Graphene oxide-chitosan-silver composite coating on cu-ni alloy with enhanced anticorrosive and antibacterial properties suitable for marine applications. Progress in Organic Coatings, 139:105444, Feb 2020. URL: https://doi.org/10.1016/j.porgcoat.2019.105444, doi:10.1016/j.porgcoat.2019.105444. This article has 133 citations and is from a peer-reviewed journal.

8. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

9. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

10. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

11. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

12. (robitz1990closuredevelopmentfor pages 20-22): Closure development for high-level nuclear waste containers for the tuff repository; Phase 1, Final report This article has 2 citations.

13. (amini2011growthofgraphene pages 1-2): Shaahin Amini, Haamun Kalaantari, Javier Garay, Alexander A. Balandin, and Reza Abbaschian. Growth of graphene and graphite nanocrystals from a molten phase. Journal of Materials Science, 46:6255-6263, Mar 2011. URL: https://doi.org/10.1007/s10853-011-5432-9, doi:10.1007/s10853-011-5432-9. This article has 50 citations and is from a peer-reviewed journal.

14. (deck2006predictionofcarbon pages 5-6): Christian P. Deck and Kenneth Vecchio. Prediction of carbon nanotube growth success by the analysis of carbon–catalyst binary phase diagrams. Carbon, 44:267-275, Feb 2006. URL: https://doi.org/10.1016/j.carbon.2005.07.023, doi:10.1016/j.carbon.2005.07.023. This article has 389 citations and is from a domain leading peer-reviewed journal.

15. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

16. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

17. (paul2026developmentofcoalderived pages 15-19): AM Paul. Development of coal-derived carbon materials for electrochemical energy storage systems. Unknown journal, 2026.

18. (paul2026developmentofcoalderived pages 19-24): AM Paul. Development of coal-derived carbon materials for electrochemical energy storage systems. Unknown journal, 2026.

19. (cadwallader2003dustcombustionsafety pages 14-18): L. C. Cadwallader. Dust combustion safety issues for fusion applications. ArXiv, May 2003. URL: https://doi.org/10.2172/910731, doi:10.2172/910731. This article has 2 citations.

20. (cadwallader2003dustcombustionsafety pages 11-14): L. C. Cadwallader. Dust combustion safety issues for fusion applications. ArXiv, May 2003. URL: https://doi.org/10.2172/910731, doi:10.2172/910731. This article has 2 citations.
