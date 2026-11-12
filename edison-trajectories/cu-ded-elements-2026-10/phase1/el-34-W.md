<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: f118b313-8cd9-40a3-aaac-78b0af1d9f0e
- Submitted: 2026-10-17T19:00:55Z
- Fetched: 2026-10-17T19:20:25Z (status: success)
- Raw trajectory JSON: ../raw/el-34-W.json.gz
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

ELEMENT UNDER REVIEW: W (refractory, immiscible). Cu-W pseudo-alloys and composites; W is nearly insoluble in liquid and solid Cu and melts at 3,422 C.

Answer for W specifically, not for copper alloys in general:
1. ROLE: what W does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their W ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how W changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-W, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-W, Cu-Ni-W and Cu-Al-W are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of W in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that W neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | W | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: W (refractory, immiscible). Cu-W pseudo-alloys and composites; W is nearly insoluble in liquid and solid Cu and melts at 3,422 C.

Answer for W specifically, not for copper alloys in general:
1. ROLE: what W does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their W ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how W changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-W, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-W, Cu-Ni-W and Cu-Al-W are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of W in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that W neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | W | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# W in pre-alloyed copper powder for marine laser DED

**Decision — EXCLUDE W as a designed addition in both Cu–Ni and aluminum-bronze candidates.** This is a decision about *induction-melted, atomized, single-stream powder*, not a claim that all Cu/W composites are unusable. The directly relevant Cu-rich laser studies obtain benefits by attaching **solid W particles to Cu powder**, rather than dissolving W into a melt: they show better infrared absorption but also heterogeneous W distribution and pores at Cu/W interfaces. No located study establishes that W improves the **as-deposited seawater resistance** of Cu–Ni or nickel-aluminum bronze (NAB), or that this feedstock route yields a dense, crack-free W-containing repair. Thus neither a useful alloying floor nor a defensible upper bound follows from the available evidence. [CITE] Rauh *et al.*, “Surface-modified copper powders with submicrometer tungsten particles for high thermal and electrical conductivity processed via laser powder bed fusion,” *Progress in Additive Manufacturing* **11** (2026), 8789–8806, doi:10.1007/s40964-026-01825-2. (rauh2026surfacemodifiedcopperpowders pages 2-4, rauh2026surfacemodifiedcopperpowders pages 7-10)

The following comparison keeps copper-rich laser processing, tungsten-rich corrosion experiments, and a carbide-containing coating separate.

| Material/process | Composition (wt%) | Quantitative finding | Transferability/reason |
|---|---:|---|---|
| Marine Cu-Ni, aluminum-bronze/NAB, Mn-Al-bronze, tin-bronze/gunmetal, brass, Cu-Ni-Sn, Cu-Ni-Si, and AWS A5.7 marine fillers | No intentional W addition documented | No verified commercial/Navy W range and no numerical W impurity maximum identified in the reviewed specifications | Strong negative screening evidence, but absence of a listed addition is **not** a formal 0 wt% limit; no specification-based impurity cap can be assigned. |
| Mechanically W-coated Cu powder; PBF-LB/M antecedent | W = 0.25–1 | Up to 98.5% relative density and 96% IACS reported with a 500 W, 1,070 nm laser | Cu-rich AM evidence, but W was a surface coating—not a melt-pre-alloyed addition; no DED, cracking, or seawater-corrosion result. (rauh2026surfacemodifiedcopperpowders pages 2-4) |
| Mechanically bonded Cu/W powder; PBF-LB/M | Cu = 93.74; W = 6.26 | At 1,070 nm, powder absorptivity increased from 25.6% for Cu to 71.6% for Cu/W; maximum density was 99.78% optically but 96.46% by Archimedes | Demonstrates improved infrared coupling, not alloying or marine durability. W remained heterogeneous and agglomerated; poor Cu wetting produced interfacial porosity. Feedstock and process differ from induction-atomized, single-stream DED powder. (rauh2026surfacemodifiedcopperpowders pages 2-4, rauh2026surfacemodifiedcopperpowders pages 7-10, rauh2026surfacemodifiedcopperpowders pages 15-17) |
| Powder-metallurgy W-Cu pseudoalloy; 3.5 wt% NaCl | W = 95; Cu = 5 | After 8 h attritor milling: corrosion rate 0.40 mm/year, Ecorr −354.17 mV versus Ag/AgCl, Icorr 72.59 µA | Matrix is W-rich—the inverse of the proposed Cu-base alloys. Results chiefly reflect binder distribution, porosity, and galvanic dissolution and cannot predict Cu-Ni or NAB performance. (kumkumoglu2016comparativeeffectsof pages 60-67, kumkumoglu2016comparativeeffectsof pages 77-85) |
| Powder-metallurgy W-Cu-Ni pseudoalloy; 3.5 wt% NaCl | W = 95; Cu = 4; Ni = 1 | After 8 h attritor milling: corrosion rate 0.02 mm/year, Ecorr −320.64 mV versus Ag/AgCl, Icorr 3.77 µA | Ni improved the binder and densification in a W-rich pseudoalloy; it does not establish a beneficial W×Ni interaction in Cu-rich Cu-Ni or NAB deposits. (kumkumoglu2016comparativeeffectsof pages 72-77, kumkumoglu2016comparativeeffectsof pages 77-85) |
| Laser-clad Ni60-WC coating on Cu alloy; 3.5 wt% NaCl | W not reported; present as WC/W₂C in a Ni-Cr-rich coating | Coating: Ecorr −0.69 V, icorr 0.234 × 10⁻⁶ mA/mm², Rp 113.74 kΩ, corrosion rate 0.0158 mm/year; Cu substrate: −0.232 V, 1.14 × 10⁻⁶ mA/mm², 33.9 kΩ, 0.0183 mm/year | Proxy only: improvement was attributed to dense Ni-based cladding plus Cr₇C₃ and NiO/Cr₂O₃ films—not elemental W in copper. It is not Cu-Ni, NAB, pre-alloyed powder, or DED repair-alloy evidence. (liu2022researchonwear pages 8-10, liu2022researchonwear media 3c9e18ba) |
| Design recommendation for pre-alloyed Cu-base DED powder | W designed addition = 0 | **EXCLUDE**; no defensible functional floor, conservative maximum, or non-conservative maximum exists for the target marine Cu-Ni/NAB families | W is effectively immiscible, risks segregation, agglomeration and interfacial porosity, and lacks direct as-deposited seawater evidence. No source-backed impurity maximum was found, so `impurity_max_wt = NA` rather than an invented ppm limit. (rauh2026surfacemodifiedcopperpowders pages 7-10, rauh2026surfacemodifiedcopperpowders pages 5-7) |


*Table: Direct and proxy evidence for elemental W in copper-powder design, with transferability limits made explicit. The evidence supports excluding W as a designed Cu-Ni or aluminum-bronze addition while leaving the impurity cap unquantified.*

## 1. Role and specified marine alloys

**[SPEC][GAP] No verified intentional W range** was found for C71500 Cu–Ni, C95800 NAB, other aluminum or manganese-aluminum bronzes, tin bronzes/gunmetals, marine brasses, Cu–Ni–Sn, Cu–Ni–Si, or the marine copper welding-filler classes ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl. The same applies to the specifications named for checking—ASTM B111, B171, B466, B148 and B369; MIL-T-16420, MIL-B-24480 and MIL-C-15726; AWS A5.7; and EN 12449. This **does not establish a certified 0 wt% limit**: these documents’ current composition tables and any residual-element clauses must be checked before claiming a numerical W impurity allowance. Tungsten electrodes used in arc welding are not tungsten additions to the filler. No commercial/Navy marine-copper grade with a source-verified W range can be listed. (rauh2026surfacemodifiedcopperpowders pages 2-4, kumkumoglu2016comparativeeffectsof pages 60-67)

**[CITE] Mechanism.** In the Cu/W work actually located, W acts as a separate, laser-absorbing refractory particulate, **not** as a demonstrated Cu solid-solution corrosion inhibitor, deoxidizer, grain refiner, or precursor to a protective marine film. The W-rich powder-metallurgy specimens retain distinct W and Cu phases. No W-bearing precipitate or intermetallic, W-derived protective film, or inhibition of Cu–Ni selective attack, NAB phase-selective attack, or brass dezincification was established for the proposed Cu-rich alloys. Do not substitute results for WC, electrodeposited Ni–W, or a WO₃-filled polymer coating for an elemental-W addition. [CITE] Kumkumoğlu, *Comparative Effects of Ni–Co Addition and Milling Parameters on Corrosion Resistance Behavior of W–Cu Based P/M Alloys* (2016 thesis; DOI not identified); Rauh *et al.* (2026), doi:10.1007/s40964-026-01825-2. (rauh2026surfacemodifiedcopperpowders pages 2-4, kumkumoglu2016comparativeeffectsof pages 60-67, kumkumoglu2016comparativeeffectsof pages 77-85)

## 2. Seawater corrosion: what the numbers do—and do not—show

**[NUMBERS][GAP] No Cu-rich W-addition response curve in seawater, ASTM D1141 water, or 3.5 wt% NaCl was located.** Consequently, there is no established beneficial or harmful W concentration interval, C71500 comparison, Ecorr or film-resistance trend, pit/crevice threshold, depth of selective attack, erosion–corrosion response, or permissible seawater velocity for a Cu–Ni/NAB–W deposit. Two chloride studies illustrate why apparently positive results cannot supply those missing bounds:

* **Inverse-matrix comparator.** A sintered **95 wt% W–5 wt% Cu** specimen tested in **3.5 wt% NaCl** after 8 h attritor milling had a reported Tafel-derived rate of **0.40 mm/year**, Ecorr **−354.17 mV versus Ag/AgCl**, and total Icorr **72.59 µA**. Replacing 1 wt% Cu with Ni (**95 wt% W–4 wt% Cu–1 wt% Ni**) gave **0.02 mm/year**, **−320.64 mV**, and **3.77 µA**; replacing it with Co instead gave **0.75 mm/year**. The unmodified 95W–5Cu specimens varied from **0.15 to 14.45 mm/year** with milling conditions. These are W-*matrix* pseudoalloys, with pronounced fabrication/porosity and binder effects; the improvement is **from changing their binder**, not evidence that adding W protects Cu–Ni. The reported current is in µA, not a transferable current density. [NUMBERS][CITE] Kumkumoğlu (2016 thesis; DOI not identified). (kumkumoglu2016comparativeeffectsof pages 60-67, kumkumoglu2016comparativeeffectsof pages 72-77, kumkumoglu2016comparativeeffectsof pages 77-85)
* **Different coating chemistry.** A laser-clad **Ni60–WC coating on a copper-alloy substrate** in **3.5 wt% NaCl** gave **0.0158 versus 0.0183 mm/year** for the substrate, respectively; reported Rp was **113.74 versus 33.9 kΩ**, and coating Ecorr **−0.69 V versus −0.232 V** for the substrate. The authors attribute resistance to the dense **Ni/Cr-containing coating**, Cr₇C₃, and NiO/Cr₂O₃—not a Cu alloy containing dissolved elemental W. Coating W wt% and equivalence to a C71500 reference were not reported. The electrochemical numbers were checked against the paper’s Table 6. [NUMBERS][CITE] Liu, Xu and Li, “Research on Wear and Corrosion Resistance of Ni60–WC Coating Fabricated by Laser on the Preheated Copper Alloy,” *Coatings* **12** (2022), 1537, doi:10.3390/coatings12101537. (liu2022researchonwear pages 8-10, liu2022researchonwear media 3c9e18ba)

## 3. DED, welding, and substrate dilution

**[NUMBERS][CITE] The genuine Cu-rich positive result is optical, not corrosion-related.** Rauh *et al.* mechanically attached fine W to already atomized Cu powder: **6.26 wt% W**, corresponding to 3 vol% W. At **1,070 nm**, measured powder absorptivity increased from **25.6%** for Cu powder to **71.6%** for Cu/W. Laser powder-bed fusion reached maxima of **99.78% relative density by optical sections**, but **96.46% by Archimedes**. W agglomerated, its distribution was heterogeneous, and interfacial pores were attributed partly to poor Cu wetting. The authors also cite an earlier surface-coated-powder result at **0.25–1 wt% W** and **98.5% optical relative density**. Neither demonstration used induction-pre-alloyed powder, blown-powder DED, NAB/Cu–Ni repair, or seawater testing. An absorptivity gain for W on *powder surfaces* must not be assumed for W segregated inside an atomized particle. [CITE] Rauh *et al.* (2026), doi:10.1007/s40964-026-01825-2. (rauh2026surfacemodifiedcopperpowders pages 2-4, rauh2026surfacemodifiedcopperpowders pages 7-10, rauh2026surfacemodifiedcopperpowders pages 15-17)

**[GAP] No W-specific DED or marine-filler welding data** were located for solidification cracks, reheated-layer liquation cracks, or crack-free dilution zones at either cast C95800 or wrought C71500. The observed Cu/W **interfacial and gas pores** are an actual LPBF warning; claims that W either causes or cures DED hot cracking would be speculative. Likewise, no measured W evaporation/oxidation loss, W transfer into either substrate, or residual-W distribution across either repair interface was found. Conventional copper laser processing already has a reflectivity/heat-extraction and lack-of-fusion problem; adding poorly wetted solids introduces a further, unqualified interface. [CITE] Canacoo *et al.*, “Laser Additive Manufacturing of Copper and Its Alloys: Challenges, Process Innovations, and Future Perspectives,” *International Journal of Precision Engineering and Manufacturing–Green Technology* (2026), doi:10.1007/s40684-026-00928-z; Rauh *et al.* (2026), doi:10.1007/s40964-026-01825-2. (canacoo2026laseradditivemanufacturing pages 4-6, rauh2026surfacemodifiedcopperpowders pages 7-10)

## 4. Induction melting, atomization, and phase/CALPHAD constraints

**[NUMBERS] W melts at approximately 3,422 °C**, far above the stated approximately **1,300 °C** induction-module maximum. Cu/W’s poor miscibility and the need to disperse W solids are evidenced by the powder-metallurgy and laser studies. Under the proposed route, an added W piece cannot be assumed to become a compositionally uniform **pre-alloyed Cu droplet**: undissolved W may settle in the crucible or produce compositionally variable, W-bearing inclusions if entrained. Poor wetting, density-driven segregation, agglomeration and Cu/W interfacial porosity are evidenced in Cu/W laser specimens; transfer of their *magnitudes* to ultrasonic atomization is untested. Ultrasonic breakup must overcome surface tension, but no measured W-specific change in Cu-alloy surface tension, powder yield or sonotrode wear was found. [CITE] Rauh *et al.* (2026), doi:10.1007/s40964-026-01825-2; Kustron *et al.*, “Development of High-Power Ultrasonic System Dedicated to Metal Powder Atomization,” *Applied Sciences* **13** (2023), 8984, doi:10.3390/app13158984. (rauh2026surfacemodifiedcopperpowders pages 7-10, kumkumoglu2016comparativeeffectsof pages 60-67)

**[GAP] Crucible/sonotrode and loss mechanisms remain unquantified.** No W-specific experiment was found for oxide pickup or reactions in alumina versus zirconia crucibles, graphite contact, or interaction with a titanium-alloy versus molybdenum sonotrode. Oxidation of exposed W-containing fines and entrained oxide are plausible handling/process concerns; a numerical loss allowance or claim of substantial elemental-W vapor loss at the Cu melt temperature is *not* established. The W-rich study reports oxidation becoming faster with temperature and discusses tungsten oxide behavior, but it does not measure loss from the proposed Cu melt or laser plume. [CITE] Kumkumoğlu (2016 thesis; DOI not identified). (kumkumoglu2016comparativeeffectsof pages 47-51)

**[GAP] Thermodynamics must not be reduced to “the Cu liquidus becomes 3,422 °C.”** Distinguish the *onset of Cu-rich melting* from the temperature at which **all added W is dissolved/melted**. Solid W may coexist with Cu-rich liquid at the available atomization temperature; a calculation returning a high *complete-melting liquidus* would not by itself demonstrate that the Cu-rich liquid cannot atomize, but it would defeat a homogeneous pre-alloyed feedstock. The inspected material establishes negligible W solubility in Cu qualitatively, but **not a defensible maximum in wt% at a specified temperature**, an experimentally checked Cu–W invariant-reaction temperature, or an assessed Cu–Ni–W/Cu–Al–W equilibrium section. Neither a Cu–W intermetallic nor a quantitative W-induced Cu-alloy liquidus shift was verified. The existence and parameter coverage of **W in the installed Thermo-Calc TCCU release, COST 531, or a usable published TDB were not verified**; element availability alone would not validate Cu–W, Cu–Ni–W or Cu–Al–W interactions. For pycalphad, inspect constituent/phase parameter records and calculate both the *first-liquid* and *last-solid* temperatures before using any **1,200–1,250 °C** screen. [CITE] Rauh *et al.* (2026), doi:10.1007/s40964-026-01825-2. (rauh2026surfacemodifiedcopperpowders pages 2-4, rauh2026surfacemodifiedcopperpowders pages 7-10)

## 5. Supply, safety, interactions, and bounds

**[NAVY][NUMBERS] Supply.** USGS identifies W on the **2022** U.S. critical-minerals list; a discussion of the **final 2025** list also identifies W among minerals for which recycling supplied the only domestic source in 2025. USGS reports China supplied **82.7%** of 2022 mined W. Its **January 2024** scenario price of **$300 per metric-ton unit of WO₃** corresponds to about **$37.8/kg of *contained W*** because that unit contains **7.93 kg W**. This is a dated *concentrate-content equivalent*, **not a quotation for 99.9% W metal, a W master alloy, or atomized Cu/W powder**. [CITE] Safirova, Golovko and Dulabova, *Analysis of the Potential Effects of Uzbekistan’s Mineral Endowment on the Critical Mineral Supply of Tungsten*, USGS OFR 2025–1032, doi:10.3133/ofr20251032. (safirova2025analysisofthe pages 6-10, safirova2025analysisofthe pages 12-13, safirova2025analysisofthe pages 10-12, staff2022usgsminingreview pages 6-9)

**[GAP] Safety and regulation.** Treat inhalable W-bearing powder and captured laser particulate as exposure-control issues; keep powders contained and use appropriate extraction and exposure assessment. The retrieved sources did **not** substantiate a numeric W-specific **OSHA** permissible exposure limit, a W-specific **RoHS/REACH** concentration restriction for these alloys, or a **Navy** prohibition. Do not present a hard-metal WC–Co health finding as the toxicity of elemental W in Cu. No regulatory wt% ceiling for this proposal can be inferred from the reviewed evidence. (kumkumoglu2016comparativeeffectsof pages 47-51)

**[GAP] Interaction constraints.** There is **no supported Cu-rich W+Ni, W+Fe, W+Mn, W+Al, W+Sn or W+Si sum/ratio rule**, or demonstrated neutralization of a marine-alloy embrittler. The measured **1 wt% Ni-for-Cu substitution at constant 95 wt% W** improved density and 3.5 wt% NaCl behavior in a *W-rich* binder system; it cannot set a W/Ni ratio for Cu-rich repair powder. The relevant joint constraint is qualitative instead: greater undissolved-W fraction can aggravate heterogeneity/wetting risk, while alloy chemistry and dilution determine the Cu-rich matrix corrosion independently. (kumkumoglu2016comparativeeffectsof pages 72-77, kumkumoglu2016comparativeeffectsof pages 77-85)

**[SPEC][GAP] Bounds for the stated feedstock and both families.** Set **designed W addition = 0 wt%** (EXCLUDE), rather than borrowing **0.25–1 wt%** or **6.26 wt%** from *surface-modified LPBF composites*. A *conservative upper bound*, *non-conservative upper bound* and *functional corrosion floor* are **NA**, because no established marine Cu-alloy W addition or demonstrated Cu-rich as-deposited corrosion response supports them. A powder/deposit **impurity maximum is also NA**: no source-verified ASTM, MIL, AWS, EN or UNS W tolerance or study-derived ppm threshold was found. Exclusion is an experimental-palette decision, **not** a claim that unavoidable trace W at any concentration makes a deposit fail. The design-limiting failure modes are unavailable homogeneous melting/partitioning, particulate wetting and interfacial porosity, and unproved marine durability; quantitative crack, selective-attack and impurity thresholds remain [GAP]. (rauh2026surfacemodifiedcopperpowders pages 2-4, rauh2026surfacemodifiedcopperpowders pages 7-10, kumkumoglu2016comparativeeffectsof pages 77-85)

VERDICT | W | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (rauh2026surfacemodifiedcopperpowders pages 2-4): Simon Rauh, Shashank Deepak Prabhu, Lioba Fischer, Jannik Huber, Gerhard Wolf, Nico Hempel, and Peter Mayr. Surface-modified copper powders with submicrometer tungsten particles for high thermal and electrical conductivity processed via laser powder bed fusion. Progress in Additive Manufacturing, 11:8789-8806, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01825-2, doi:10.1007/s40964-026-01825-2. This article has 0 citations and is from a peer-reviewed journal.

2. (rauh2026surfacemodifiedcopperpowders pages 7-10): Simon Rauh, Shashank Deepak Prabhu, Lioba Fischer, Jannik Huber, Gerhard Wolf, Nico Hempel, and Peter Mayr. Surface-modified copper powders with submicrometer tungsten particles for high thermal and electrical conductivity processed via laser powder bed fusion. Progress in Additive Manufacturing, 11:8789-8806, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01825-2, doi:10.1007/s40964-026-01825-2. This article has 0 citations and is from a peer-reviewed journal.

3. (rauh2026surfacemodifiedcopperpowders pages 15-17): Simon Rauh, Shashank Deepak Prabhu, Lioba Fischer, Jannik Huber, Gerhard Wolf, Nico Hempel, and Peter Mayr. Surface-modified copper powders with submicrometer tungsten particles for high thermal and electrical conductivity processed via laser powder bed fusion. Progress in Additive Manufacturing, 11:8789-8806, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01825-2, doi:10.1007/s40964-026-01825-2. This article has 0 citations and is from a peer-reviewed journal.

4. (kumkumoglu2016comparativeeffectsof pages 60-67): FB Kumkumoğlu. Comparative effects of ni-co addition and milling parameters on corrosion resistance behavior of w-cu based p/m alloys. Unknown journal, 2016.

5. (kumkumoglu2016comparativeeffectsof pages 77-85): FB Kumkumoğlu. Comparative effects of ni-co addition and milling parameters on corrosion resistance behavior of w-cu based p/m alloys. Unknown journal, 2016.

6. (kumkumoglu2016comparativeeffectsof pages 72-77): FB Kumkumoğlu. Comparative effects of ni-co addition and milling parameters on corrosion resistance behavior of w-cu based p/m alloys. Unknown journal, 2016.

7. (liu2022researchonwear pages 8-10): Yu Liu, Tianhao Xu, and Guohui Li. Research on wear and corrosion resistance of ni60-wc coating fabricated by laser on the preheated copper alloy. Coatings, 12:1537, Oct 2022. URL: https://doi.org/10.3390/coatings12101537, doi:10.3390/coatings12101537. This article has 17 citations.

8. (liu2022researchonwear media 3c9e18ba): Yu Liu, Tianhao Xu, and Guohui Li. Research on wear and corrosion resistance of ni60-wc coating fabricated by laser on the preheated copper alloy. Coatings, 12:1537, Oct 2022. URL: https://doi.org/10.3390/coatings12101537, doi:10.3390/coatings12101537. This article has 17 citations.

9. (rauh2026surfacemodifiedcopperpowders pages 5-7): Simon Rauh, Shashank Deepak Prabhu, Lioba Fischer, Jannik Huber, Gerhard Wolf, Nico Hempel, and Peter Mayr. Surface-modified copper powders with submicrometer tungsten particles for high thermal and electrical conductivity processed via laser powder bed fusion. Progress in Additive Manufacturing, 11:8789-8806, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01825-2, doi:10.1007/s40964-026-01825-2. This article has 0 citations and is from a peer-reviewed journal.

10. (canacoo2026laseradditivemanufacturing pages 4-6): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

11. (kumkumoglu2016comparativeeffectsof pages 47-51): FB Kumkumoğlu. Comparative effects of ni-co addition and milling parameters on corrosion resistance behavior of w-cu based p/m alloys. Unknown journal, 2016.

12. (safirova2025analysisofthe pages 6-10): Elena Safirova, Yelena Golovko, and Nafisa Dulabova. Analysis of the potential effects of uzbekistan’s mineral endowment on the critical mineral supply of tungsten. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251032, doi:10.3133/ofr20251032. This article has 1 citations.

13. (safirova2025analysisofthe pages 12-13): Elena Safirova, Yelena Golovko, and Nafisa Dulabova. Analysis of the potential effects of uzbekistan’s mineral endowment on the critical mineral supply of tungsten. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251032, doi:10.3133/ofr20251032. This article has 1 citations.

14. (safirova2025analysisofthe pages 10-12): Elena Safirova, Yelena Golovko, and Nafisa Dulabova. Analysis of the potential effects of uzbekistan’s mineral endowment on the critical mineral supply of tungsten. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251032, doi:10.3133/ofr20251032. This article has 1 citations.

15. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.
