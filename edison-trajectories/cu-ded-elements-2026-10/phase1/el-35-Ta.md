<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 0ddac0ad-f994-4d18-9bf2-0cce5474b7fe
- Submitted: 2026-10-17T19:00:58Z
- Fetched: 2026-10-17T19:20:26Z (status: success)
- Raw trajectory JSON: ../raw/el-35-Ta.json.gz
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

ELEMENT UNDER REVIEW: Ta (refractory, immiscible). Nanocrystalline Cu-Ta (e.g. Cu-3Ta, Army Research Laboratory) made by mechanical alloying; any corrosion data in NaCl or seawater; Ta melts at 3,017 C.

Answer for Ta specifically, not for copper alloys in general:
1. ROLE: what Ta does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ta ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ta changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ta, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ta, Cu-Ni-Ta and Cu-Al-Ta are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ta in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ta neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ta | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ta (refractory, immiscible). Nanocrystalline Cu-Ta (e.g. Cu-3Ta, Army Research Laboratory) made by mechanical alloying; any corrosion data in NaCl or seawater; Ta melts at 3,017 C.

Answer for Ta specifically, not for copper alloys in general:
1. ROLE: what Ta does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ta ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ta changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ta, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ta, Cu-Ni-Ta and Cu-Al-Ta are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ta in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ta neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ta | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Tantalum (Ta) assessment for pre-alloyed marine-copper DED powder

**Decision: EXCLUDE Ta as a designed addition from both the Cu–Ni and aluminum-bronze composition palettes.** This is a decision about the specified induction-melt → ultrasonic-atomization → single-stream DED route, **not** a claim that Ta is intrinsically detrimental to corrosion. Equilibrium Cu–Ta is essentially immiscible, whereas the reported benefits of Ta-rich nanocrystalline Cu require nonequilibrium powder or vapor processing. The available quantitative chloride-corrosion benefits concern *different, Hf- or Zr-containing metallic glasses*. Neither a beneficial Ta interval nor a tolerable impurity maximum is established for an as-deposited Cu–Ni or NAB repair. (riaboshtan2025theformationand pages 1-2, smeltzer2022investigatingmicrostructurepropertyrelationships pages 36-40, asami2004effectofadditional pages 2-4, qin2003effectsofadditional pages 3-4)

The distinction between the measurable chloride results and the proposed deposits is central:

| Material/process | Ta (wt%) | Quantitative finding | Applicability |
|---|---:|---|---|
| Equilibrium Cu–Ta; nonequilibrium electron-beam vapor condensates | Equilibrium: effectively 0; condensates: approximately 0.14–8.1 wt% (0.05–3 at.%) | No mutual equilibrium solid or liquid solubility and no compounds. Vapor deposition kinetically traps Ta; second-phase Ta appears above approximately 0.3 at.% (approximately 0.85 wt.%), and the supersaturated solution decomposes above 500 °C. DOI: 10.15407/fm32.02.250. (riaboshtan2025theformationand pages 1-2, riaboshtan2025theformationand pages 2-5) | Direct evidence of incompatibility with melt alloying; vapor-condensate behavior is not transferable to induction-melted powder or DED. |
| Arc-melted and copper-mold-cast amorphous Cu–Zr–Ti–Ta | approximately 0.47 wt% actual (0.2 at.%) | In 3% NaCl at 298 K for 168 h, corrosion rate changed from 290 to 200 µm/year versus Ta-free Cu–Zr–Ti glass. DOI: 10.1016/j.msea.2003.10.034. (asami2004effectofadditional pages 1-2, asami2004effectofadditional pages 2-4) | Quantitative chloride evidence, but the alloy is a Zr–Ti-bearing metallic glass—not C71500, Cu–Ni, aluminum bronze, NAB, or DED material. |
| Copper-mold-cast amorphous Cu–Hf–Ti–Ta | approximately 4.2 wt% nominal (2 at.%) | In 3% NaCl at 298 K for 168 h, corrosion rate decreased from approximately 0.1 to approximately 0.001 mm/year; passive current also decreased. DOI: 10.2320/matertrans.44.1042. (qin2003effectsofadditional pages 1-2, qin2003effectsofadditional pages 2-3, qin2003effectsofadditional pages 3-4) | Strong result within an Hf–Ti metallic glass, but it does not establish performance in crystalline marine copper alloys, seawater, repair dilution, atomized powder, or DED. |
| Ta-bearing marine Cu–Ni or NAB made by DED; commercial/Navy copper alloys | Not established | No quantitative as-deposited seawater or 3.5 wt% NaCl DED evidence, validated Ta composition range, or commercial/Navy Ta-bearing Cu–Ni/NAB specification was established in the retrieved literature. | Critical evidence gap; no defensible designed-addition bound or specification-derived impurity maximum follows from the available record. |


*Table: The evidence progresses from equilibrium Cu–Ta immiscibility through non-transferable metallic-glass chloride results to the complete absence of validated Ta data for marine Cu–Ni/NAB DED. Approximate wt% values are converted from the reported at.% compositions.*

## 1. Role, marine-alloy precedent, and specifications

**[CITE] [GAP]** In equilibrium Cu–Ta, Ta is not an established conventional Cu solid-solution strengthener or Cu–Ta intermetallic former. In *mechanically alloyed nanocrystalline Cu*, Ta segregation at grain boundaries and nanoscale Ta clusters impede grain growth; this is a demonstrated microstructural mechanism, **not** demonstrated grain refinement or corrosion protection in induction-melted Cu–Ni or NAB. A separate vapor-condensate study observes kinetically trapped Ta in fcc Cu, followed by decomposition on heating above **500 °C**. Neither route establishes retention of that structure through a DED melt pool. (smeltzer2022investigatingmicrostructurepropertyrelationships pages 36-40, riaboshtan2025theformationand pages 1-2, riaboshtan2025theformationand pages 2-5)

**[SPEC] [NAVY] [GAP]** No Ta-containing *commercial or Navy seawater-copper alloy with a verified Ta range* was established in the retrieved evidence. This applies to the requested Cu–Ni, aluminum bronze/NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, and Cu–Ni–Si families. ASTM **B111, B171, B466, B148, B369**; **MIL-T-16420, MIL-B-24480, MIL-C-15726**; **AWS A5.7**; and **EN 12449** should be checked against their controlled editions before asserting a specified range. Their use as marine-alloy or filler identifiers does **not** make Ta a specified constituent, and an unlisted constituent must not be converted into an invented Ta maximum. No Ta-mediated deoxidation, Ta-bearing protective seawater-film chemistry, or suppression of selective attack has been demonstrated for those alloys in the evidence examined. (riaboshtan2025theformationand pages 1-2, asami2004effectofadditional pages 2-4, qin2003effectsofadditional pages 3-4)

## 2. Chloride and seawater corrosion

**[NUMBERS] [CITE]** Asami *et al.* measured an arc-melted, copper-mold-cast **Cu–Zr–Ti metallic glass** with **0.2 at.% actual Ta**, approximately **0.47 wt% Ta** when converted using its measured alloy basis. In **3 wt% NaCl**, its 168-hour mass-loss-derived rate was **200 µm/year**, versus **290 µm/year** without Ta: a decrease of approximately **31%**. The nominal Ta charge was higher than the incorporated amount; the paper specifically warns that Ta uptake and its corrosion effect were limited. This is neither 3.5 wt% NaCl nor a crystalline, Cu-balance marine alloy. Asami *et al.*, “Effect of additional elements on the corrosion behavior of a Cu–Zr–Ti bulk metallic glass,” *Materials Science and Engineering A* **375–377** (2004), 235–239, DOI **10.1016/j.msea.2003.10.034**. (asami2004effectofadditional pages 1-2, asami2004effectofadditional pages 2-4)

**[NUMBERS] [CITE]** In a *different* copper-mold-cast **Cu–Hf–Ti glass**, nominal **2 at.% Ta**—approximately **4.2 wt% Ta** on that alloy’s composition basis—reduced the reported 168-hour **3 wt% NaCl** rate from approximately **10⁻¹ to 10⁻³ mm/year** and lowered anodic passive current. Its proposed film mechanism involves an **Hf/Ti-rich surface**; the authors describe the contribution of Ta to that film as requiring further investigation. This result cannot establish a Ta functional floor, a Ta₂O₅ film on NAB, or C71500-equivalent performance after DED. Qin *et al.*, “Effects of Additional Elements on the Glass Formation and Corrosion Behavior of Bulk Glassy Cu–Hf–Ti Alloys,” *Materials Transactions* **44** (2003), 1042–1045, DOI **10.2320/matertrans.44.1042**. (qin2003effectsofadditional pages 1-2, qin2003effectsofadditional pages 2-3, qin2003effectsofadditional pages 3-4)

**[GAP]** No defensible *helpful or harmful concentration interval* for Ta in crystalline Cu–Ni, NAB, or the other specified seawater-alloy families follows from those two experiments. Ta-specific changes in seawater **E_corr, polarization resistance, EIS film resistance, pitting or crevice potential, dealloying depth, erosion–corrosion, and permissible flow velocity** were not established. A benign Ta oxide on exposed Ta particles would not, by itself, prove a continuous protective film over a Cu-rich deposit; preferential attack adjacent to second phases is a **hypothesis to test**, not a reported result. No retrieved result demonstrates the required as-deposited comparison with wrought C71500 or 30-day selective-attack depth. (asami2004effectofadditional pages 2-4, qin2003effectsofadditional pages 3-4, powers2020microstructuralcharacterizationof pages 1-4)

## 3. DED, welding, and substrate dilution

**[GAP]** No Ta-controlled blown-powder laser DED crack-susceptibility, multilayer reheating/liquation, porosity, volatilization, or retention study was established for Cu–Ni or NAB. Likewise, the reviewed evidence does not support assigning Ta an effect measured with **ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl** filler: these are possible *comparison families*, not Ta-bearing welding experiments. Therefore, claims that Ta eliminates hot cracking, or that it causes a quantified amount of liquation cracking, would be unjustified. (riaboshtan2025theformationand pages 1-2, powers2020microstructuralcharacterizationof pages 1-4)

**[CITE] [GAP]** A plausible *process risk*—not a measured defect threshold—is Ta-rich unmelted inclusions or segregated regions acting as pores, lack-of-fusion initiators, or local corrosion heterogeneities. It follows from the contrast between equilibrium immiscibility and the deliberately nonequilibrium preparation of nanocrystalline Cu–Ta. Dilution into **cast NAB C95800** introduces Al, Ni, Fe, and Mn; dilution into **wrought Cu–Ni** introduces Ni and Fe. Neither dilution path has been shown to dissolve or harmlessly redistribute Ta, nor has a Ta-bearing fusion-boundary or reheated-layer phase map been verified. Do not transfer observations on a mechanically milled Cu–Ta compact or sputtered film to an infrared-laser weld without testing. (riaboshtan2025theformationand pages 1-2, smeltzer2022investigatingmicrostructurepropertyrelationships pages 36-40, powers2020microstructuralcharacterizationof pages 1-4)

## 4. Induction melting and ultrasonic atomization

**[NUMBERS] [CITE]** Ta melts at approximately **3,017 °C**, far above the stated **~1,300 °C** induction-module ceiling and **~1,200–1,250 °C** practical liquidus/superheat window. This fact **does not prove** that every trace-Ta Cu alloy has a 3,017 °C liquidus. Rather, equilibrium immiscibility means a Cu-rich liquid can coexist with Ta-rich material: charging Ta metal into a ~0.5 kg copper melt cannot be assumed to yield chemically uniform, fully pre-alloyed particles. The independently prepared vapor condensates explicitly differ from melt-and-cast material. (riaboshtan2025theformationand pages 1-2, riaboshtan2025theformationand pages 2-5)

**[GAP]** Ta uptake and particle-to-particle Ta variance, oxide/inclusion content, surface-tension changes, and retained Ta after atomization or a 1.07-µm laser have **not** been measured for this equipment. Oxygen pickup and Ta-rich oxides are reasonable screening concerns; however, no quantitative reaction rate or demonstrated incompatibility with **alumina, zirconia, graphite, a Ti-alloy sonotrode, or a Mo sonotrode** was established. Conversely, a high Ta melting point is **not** evidence of a measured Ta vapor-loss rate: oxidation, Cu-rich-melt separation, and incorporation should be distinguished from evaporation. (riaboshtan2025theformationand pages 1-2, riaboshtan2025theformationand pages 2-5)

## 5. Phase equilibria and CALPHAD

**[CITE] [NUMBERS]** The reviewed Cu–Ta phase evidence describes **negligible equilibrium Ta solid solubility in fcc Cu**, equilibrium liquid immiscibility, and **no equilibrium binary compounds**. Accordingly, its maximum equilibrium fcc-Cu solubility can responsibly be reported only as **negligible/approximately 0 wt%**, **not** as an experimentally verified numerical maximum at a specified temperature. The retrieved record supplies **no defensible invariant temperature or Cu-rich liquid-composition curve at 1,200–1,250 °C**. In contrast, vapor deposition explores **0.05–3 at.% Ta** and mechanical alloying produces Ta-cluster-stabilized nanocrystalline material; those concentrations are *not* equilibrium solubility limits. Riaboshtan *et al.*, “The formation and decomposition of anomalous solutions of tantalum in copper condensates,” *Functional Materials* **32** (2025), 250–258, DOI **10.15407/fm32.02.250**; Powers *et al.*, “Microstructural characterization of phase-separated co-deposited Cu–Ta immiscible alloy thin films,” *Journal of Materials Research* **35** (2020), 1531–1542, DOI **10.1557/jmr.2020.100**. (riaboshtan2025theformationand pages 1-2, riaboshtan2025theformationand pages 2-5, powers2020microstructuralcharacterizationof pages 1-4)

**[GAP]** Neither coverage and validation of **Cu–Ta, Cu–Ni–Ta, and Cu–Al–Ta** in the installed **Thermo-Calc TCCU** release nor an applicable assessed **COST 531/published TDB** was verified. A generic software element list, if Ta appears on it, would not verify assessed binary liquid immiscibility or ternary predictions. Before treating a calculated liquidus as a manufacturing go/no-go, inspect constituent phases and assessments in the *actual database version* and cross-check Cu-rich liquid plus possible Ta-rich phase experimentally. There is no evidence-supported Ta concentration at which this particular multicomponent powder’s liquidus first exceeds **1,250 °C**. (riaboshtan2025theformationand pages 1-2, smeltzer2022investigatingmicrostructurepropertyrelationships pages 36-40)

## 6. Supply, cost, and safety

**[NAVY] [CITE]** Ta is on the **2025 final U.S. critical-minerals list**, published **7 November 2025, 90 FR 50494**; copper was newly added relative to the 2022 list. The retrieved USGS material identifies Ta on the final list, but does not itself establish a purchasing-grade **Ta metal price per kg**; no reliable figure for that quantity should be substituted with the price of Ta-containing ore, Ta₂O₅, or high-purity **niobium**. U.S. Geological Survey, “USGS mining review,” *Mining Engineering* (May 2026), pp. 26–33; Nassar *et al.*, *USGS Open-File Report 2025–1047* (2025), DOI **10.3133/ofr20251047**. The 2022 Ta listing should be verified against its original Federal Register notice before citing that edition specifically. (staff2022usgsminingreview pages 3-5, staff2022usgsminingreview pages 6-9, ciovati2025businessplanfor pages 13-15, nassar2025methodologyandtechnical pages 4-9)

**[NUMBERS] [CITE]** Ta is not appropriately treated as a harmless dust: a metal-powder safety review lists an **OSHA 8-hour Ta-dust TWA of 5 mg/m³**, cites irritation and possible respiratory effects with prolonged alloy-dust exposure, and reports Ta-powder minimum explosible concentrations of **160–165 or ~400 g/m³**, depending on the source, with reported ignition energies including **<3 mJ**. These measurements concern particular Ta powders, **not** a measured ignition threshold or exposure limit for dilute Cu–Ta pre-alloyed powder. Capture DED fume, control inhalation, bond/ground powder-handling equipment, and characterize the actual powder. No Ta-specific **RoHS/REACH alloy prohibition or Navy restriction** was established. J. M. Benson, “Safety considerations when handling metal powders,” *Journal of the Southern African Institute of Mining and Metallurgy* (2012), pp. 563–573; DOI **not identified in the retrieved record**. (benson2012safetyconsiderationswhen pages 3-5, benson2012safetyconsiderationswhen pages 6-9, benson2012safetyconsiderationswhen pages 9-10, benson2012safetyconsiderationswhen pages 10-12)

## 7. Bounds, interactions, and evidence quality

**[GAP] Decision and bounds.** **EXCLUDE designed Ta, family: none.** Conservative maximum, non-conservative maximum, and functional floor are **NA**, not zero-valued experimental thresholds. **Impurity maximum is also NA**: no reviewed copper-marine specification or Ta-contamination study supplies a tolerable powder-*and*-deposit value in wt% or ppm. Set the design target to **no intentional Ta addition**, assay incidental Ta in each powder batch and deposit, and specify a numeric acceptance criterion only after establishing analytical detection, incorporation, defect, and corrosion data. The bounding failure mode for the *design decision* is inability to demonstrate homogeneous pre-alloying and reproducible as-deposited marine performance—not a measured Ta cracking or corrosion threshold. (riaboshtan2025theformationand pages 1-2, asami2004effectofadditional pages 2-4, qin2003effectsofadditional pages 3-4)

**[GAP] Interactions for a later joint-constraint model.** Treat **Ta × Ni** and **Ta × Al** as *unresolved phase-equilibrium/dilution interactions*, rather than impose an invented Ni:Ta or Al:Ta ratio. Likewise, there is no validated combined Ta+Fe or Ta+Mn restriction, or evidence that Ta neutralizes Fe/Mn-driven selective attack. Track Ta mass balance and spatial segregation separately from bulk Ta; test whether oxygen produces Ta-rich inclusions and whether Al-bearing NAB dilution or Ni-rich Cu–Ni dilution changes those inclusions. These are experimental questions, not assessed additive composition rules. (riaboshtan2025theformationand pages 1-2, riaboshtan2025theformationand pages 2-5, powers2020microstructuralcharacterizationof pages 1-4)

**[GAP] Evidence quality: thin for the proposed alloy and route.** The strongest Ta–Cu-specific evidence establishes *processing-dependent immiscibility and segregation*, not seawater performance. The only numerical chloride improvements cited above are in glasses with major Zr–Ti or Hf–Ti content, prepared by arc melting and copper-mold casting; neither demonstrates marine Cu–Ni/NAB corrosion, usable atomized pre-alloy, repair dilution, or crack-free DED. No quantitative harmful Ta interval, Ta-containing Navy specification range, equipment-specific incorporation efficiency, or justified ppm tolerance was found. (riaboshtan2025theformationand pages 1-2, asami2004effectofadditional pages 2-4, qin2003effectsofadditional pages 3-4, powers2020microstructuralcharacterizationof pages 1-4)

VERDICT | Ta | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (riaboshtan2025theformationand pages 1-2): V. Riaboshtan, A. Zubkov, V. Belozerov, M. Zhadko, E. Zozulya, and E. Lutsenko. The formation and decomposition of anomalous solutions of tantalum in copper condensates. Functional Materials, 32:250-258, Jun 2025. URL: https://doi.org/10.15407/fm32.02.250, doi:10.15407/fm32.02.250. This article has 0 citations and is from a peer-reviewed journal.

2. (smeltzer2022investigatingmicrostructurepropertyrelationships pages 36-40): JA Smeltzer. Investigating microstructure-property relationships of multiphase nanocrystalline alloys. Unknown journal, 2022.

3. (asami2004effectofadditional pages 2-4): K. Asami, C.-L. Qin, T. Zhang, and A. Inoue. Effect of additional elements on the corrosion behavior of a cu–zr–ti bulk metallic glass. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 375:235-239, Jul 2004. URL: https://doi.org/10.1016/j.msea.2003.10.034, doi:10.1016/j.msea.2003.10.034. This article has 82 citations.

4. (qin2003effectsofadditional pages 3-4): Chunling Qin, Katsuhiko Asami, Tao Zhang, Wei Zhang, and Akihisa Inoue. Effects of additional elements on the glass formation and corrosion behavior of bulk glassy cu-hf-ti alloys. Materials Transactions, 44:1042-1045, May 2003. URL: https://doi.org/10.2320/matertrans.44.1042, doi:10.2320/matertrans.44.1042. This article has 43 citations and is from a peer-reviewed journal.

5. (riaboshtan2025theformationand pages 2-5): V. Riaboshtan, A. Zubkov, V. Belozerov, M. Zhadko, E. Zozulya, and E. Lutsenko. The formation and decomposition of anomalous solutions of tantalum in copper condensates. Functional Materials, 32:250-258, Jun 2025. URL: https://doi.org/10.15407/fm32.02.250, doi:10.15407/fm32.02.250. This article has 0 citations and is from a peer-reviewed journal.

6. (asami2004effectofadditional pages 1-2): K. Asami, C.-L. Qin, T. Zhang, and A. Inoue. Effect of additional elements on the corrosion behavior of a cu–zr–ti bulk metallic glass. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 375:235-239, Jul 2004. URL: https://doi.org/10.1016/j.msea.2003.10.034, doi:10.1016/j.msea.2003.10.034. This article has 82 citations.

7. (qin2003effectsofadditional pages 1-2): Chunling Qin, Katsuhiko Asami, Tao Zhang, Wei Zhang, and Akihisa Inoue. Effects of additional elements on the glass formation and corrosion behavior of bulk glassy cu-hf-ti alloys. Materials Transactions, 44:1042-1045, May 2003. URL: https://doi.org/10.2320/matertrans.44.1042, doi:10.2320/matertrans.44.1042. This article has 43 citations and is from a peer-reviewed journal.

8. (qin2003effectsofadditional pages 2-3): Chunling Qin, Katsuhiko Asami, Tao Zhang, Wei Zhang, and Akihisa Inoue. Effects of additional elements on the glass formation and corrosion behavior of bulk glassy cu-hf-ti alloys. Materials Transactions, 44:1042-1045, May 2003. URL: https://doi.org/10.2320/matertrans.44.1042, doi:10.2320/matertrans.44.1042. This article has 43 citations and is from a peer-reviewed journal.

9. (powers2020microstructuralcharacterizationof pages 1-4): Max Powers, Benjamin Derby, Alex Shaw, Evan Raeker, and Amit Misra. Microstructural characterization of phase-separated co-deposited cu–ta immiscible alloy thin films. Journal of Materials Research, 35:1531-1542, May 2020. URL: https://doi.org/10.1557/jmr.2020.100, doi:10.1557/jmr.2020.100. This article has 30 citations and is from a peer-reviewed journal.

10. (staff2022usgsminingreview pages 3-5): US Staff. Usgs mining review. Unknown journal, 2022.

11. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

12. (ciovati2025businessplanfor pages 13-15): Gianluigi Ciovati, Marla Schuchman, William Donaldson, Alex Murokh, Miles Naughton, Dwight Osha, Drew Packard, John Rathke, and Alan Todd. Business plan for a domestic supply of superconducting radiofrequency cavities. Unknown journal, Jan 2025. URL: https://doi.org/10.2172/2497788, doi:10.2172/2497788.

13. (nassar2025methodologyandtechnical pages 4-9): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

14. (benson2012safetyconsiderationswhen pages 3-5): JM Benson. Safety considerations when handling metal powders. Unknown journal, 2012.

15. (benson2012safetyconsiderationswhen pages 6-9): JM Benson. Safety considerations when handling metal powders. Unknown journal, 2012.

16. (benson2012safetyconsiderationswhen pages 9-10): JM Benson. Safety considerations when handling metal powders. Unknown journal, 2012.

17. (benson2012safetyconsiderationswhen pages 10-12): JM Benson. Safety considerations when handling metal powders. Unknown journal, 2012.
