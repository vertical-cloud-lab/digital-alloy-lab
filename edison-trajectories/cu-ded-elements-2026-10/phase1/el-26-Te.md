<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 36e10129-9536-48c5-aeb7-a3ef0adbfe0a
- Submitted: 2026-10-17T19:00:07Z
- Fetched: 2026-10-17T19:22:58Z (status: success)
- Raw trajectory JSON: ../raw/el-26-Te.json.gz
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

ELEMENT UNDER REVIEW: Te (impurity / free-machining). Tellurium copper C14500 (0.4-0.7 Te); impurity limit in Cu-Ni; hot shortness.

Answer for Te specifically, not for copper alloys in general:
1. ROLE: what Te does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Te ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Te changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Te, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Te, Cu-Ni-Te and Cu-Al-Te are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Te in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Te neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Te | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Te (impurity / free-machining). Tellurium copper C14500 (0.4-0.7 Te); impurity limit in Cu-Ni; hot shortness.

Answer for Te specifically, not for copper alloys in general:
1. ROLE: what Te does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Te ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Te changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Te, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Te, Cu-Ni-Te and Cu-Al-Te are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Te in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Te neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Te | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Tellurium (Te): composition-screen decision

**Decision — LIMIT Te as an impurity, not a designed addition, for both Cu–Ni and aluminum-bronze DED powders.** Te’s established function in copper is free machining, whereas the available marine-copper metallurgy classifies it as detrimental in both Cu–Ni and aluminum bronze. Its very low solubility, Cu₂Te formation, and reported association with heat-affected-zone (HAZ) cracking conflict with the requirement for dense, crack-free multilayer deposits and sound repair interfaces. No verified Te-controlled experiment establishes an *as-deposited* seawater-corrosion advantage over C71500. The numerical limit below is therefore a conservative processing screen, **not** a demonstrated DED-safe or seawater-qualified threshold. [CITE] [NAVY] (konynenburg1990backgroundstudiesin pages 142-149, magnusson2017thermodynamicevaluationof pages 41-43, riley1986impurityeffectsin pages 3-4)

| Item | Verified Te-specific quantitative result | Applicability / limitation |
|---|---:|---|
| C14500 tellurium copper | 0.4–0.7 wt% Te | Range supplied in the project brief; not independently verified here against the controlling ASTM/UNS specification. It is a free-machining high-copper alloy, not evidence that Te is suitable in Cu-Ni or aluminum bronze DED. |
| UNS C10100 oxygen-free electronic copper | 0.0002 wt% Te maximum (2 ppm) | Reported from the C10100 material standard in SKB R-17-20; a high-purity-copper limit, not a Cu-Ni, NAB, or welding-filler specification. (magnusson2017thermodynamicevaluationof pages 9-12) |
| Cu-Ni hot workability | Harmful Te may require control to as low as 0.003 wt% (30 ppm) | Literature-review threshold for Cu-Ni hot working; directly relevant as a conservative ceiling for thermal processing, but not established by DED crack testing or identified as an ASTM B111/B466 limit. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6) |
| Te solubility in Cu | 1 at. ppm at 600 °C, approximately 0.0002 wt% Te by conversion | Calculated from `log x = −7372/T + 2.43`; demonstrates extremely low equilibrium solubility and Cu₂Te precipitation tendency. It is an estimate at 600 °C, not a measured global maximum solubility. (magnusson2017thermodynamicevaluationof pages 41-43) |
| Melt volatilization | Approximately 50% Te vaporized at 1300 °C under reducing copper-alloy/slag conditions | Establishes possible high-temperature Te loss and oxygen-potential sensitivity; the experiment used slag and long equilibration, not argon ultrasonic atomization or laser DED, so the loss fraction must not be transferred quantitatively. (klemettinen2020recyclingoftellurium pages 4-7) |
| Seawater corrosion | No quantitative Te-controlled Cu-Ni, NAB, aluminum-bronze, or C14500 seawater/3.5 wt% NaCl comparison located | No defensible beneficial range for corrosion rate, potential, impedance, pitting, crevice attack, dealloying, erosion-corrosion, or velocity limit; corrosion benefit is unproven for the proposal alloys. |
| DED and welding | No quantitative Te-controlled copper-alloy DED study located | Welding literature identifies Te among impurities associated with copper-alloy HAZ cracking; no demonstrated crack-free Te range exists for ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl deposits. (riley1986impurityeffectsin pages 3-4) |
| U.S. critical-mineral status | Te retained on the final 2025 list after draft recommendation for removal | Te was already on the 2022 list; the 2025 technical assessment recommended removal, but the final list retained it. (nassar2025methodologyandtechnical pages 9-10, staff2022usgsminingreview pages 6-9) |
| Price | 349 US$/kg in 2011; approximately 70 US$/kg in 2017 inferred as 20% of the peak | Historical, purity-unspecified values only; no current firm 2025–2026 procurement quote was verified, so these are unsuitable as present powder-cost estimates. (chung2024purificationprinciplesand pages 3-5) |


*Table: Compact audit of the quantitative evidence that constrains tellurium in copper-alloy DED. It distinguishes directly supported limits from supplied values, derived estimates, indirect processing evidence, and unresolved corrosion or AM gaps.*

## 1. Role and alloy specifications

[CITE] Te is added to free-machining copper to aid chip breaking; the copper-alloy mechanism supported here is formation of a separate copper telluride, principally Cu₂Te, rather than substantial Cu-matrix solid-solution strengthening. A U.S. Bureau of Mines review distinguishes Te for machinability from Al for impingement-corrosion resistance and P/B/Si for deoxidation; a separate materials review calls Te detrimental to copper, aluminum bronze, and Cu–Ni because Cu–X compounds impede working and joining. Neither establishes Te as a protective-film former, deoxidizer, grain refiner, or inhibitor of dezincification or other marine dealloying. (riley1986impurityeffectsin pages 1-3, konynenburg1990backgroundstudiesin pages 142-149, magnusson2017thermodynamicevaluationof pages 14-16)

[SPEC] [NUMBERS] **C14500 tellurium copper:** **0.4–0.7 wt% Te**, as stated in the question; the controlling UNS/CDA or product-standard text was **not independently obtained**, so this is a supplied commercial range, not a verified ASTM clause. It demonstrates a machinability use, not fitness for seawater repair. **UNS C10100:** the composition table reproduced in H. Magnusson, *Thermodynamic Evaluation of Impurity Elements in OFP Copper*, SKB R-17-20 (2017), gives **Te ≤0.0002 wt% (2 ppm)**; C10100 is high-purity copper, **not** a Cu–Ni or NAB specification. [GAP] I could not substantiate an intentionally Te-bearing grade or Te-specific permitted range in C70600/C71500 Cu–Ni, C95800 NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si, or in ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, EN 12449, or AWS A5.7. Do not assign any of those documents a Te limit without the governing edition. (magnusson2017thermodynamicevaluationof pages 9-12, riley1986impurityeffectsin pages 1-3)

## 2. Seawater-corrosion evidence

[GAP] Targeted searches did **not** yield a controlled comparison varying Te in C71500, C70600, C95800, or a related copper alloy in natural seawater, ASTM D1141 water, or 3.5 wt% NaCl. Consequently there is **no defensible numerical beneficial or harmful Te range** for corrosion rate, *E*corr, polarization resistance, impedance/film resistance, pit or crevice depth, selective attack, erosion-corrosion, or permissible flow velocity. Likewise, the corrosion of C14500 or Cu₂Te in an unrelated medium cannot establish equivalence to as-deposited C71500. Te-containing sulfide/oxide species observed in high-temperature smelting slag are **not seawater-film evidence**. [CITE] The materials review identifies working/joining difficulty, not a measured seawater penalty; thus possible corrosion damage from telluride-associated heterogeneity is a **testable concern, not a measured effect**. (konynenburg1990backgroundstudiesin pages 142-149, klemettinen2020recyclingoftellurium pages 4-7)

## 3. DED, welding, and repair interfaces

[CITE] [NUMBERS] W. D. Riley and H. V. Makar, “Impurity effects in secondary copper alloys,” *Conservation & Recycling* **9** (1986) 315–323, DOI **10.1016/0361-3658(86)90066-4**, report that Cu–Ni hot-workability control may require **Te as low as 0.003 wt% (30 ppm)**. They separately identify Te among impurities associated with copper-alloy **HAZ cracking** and discuss impurity segregation, grain-boundary voiding, and low-solubility phases. The 0.003 wt% value concerns **Cu–Ni hot working**, not a measured threshold for laser solidification or HAZ liquation. It is also not a Te limit inferred from the paper’s Pb/Bi tables. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6)

[GAP] No retrieved controlled Te series measures solidification-crack length, remelt/HAZ liquation cracks, porosity, Te loss, or oxygen pickup during Cu-alloy fiber-laser blown-powder DED. Nor was a Te-controlled welding series verified for **ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl**; those filler designations must not be presented as evidence of Te tolerance. During repair, mixing a Te-bearing bead with wrought Cu–Ni or cast NAB, then reheating it with subsequent passes, could expose locally segregated telluride to HAZ stresses; the severity and even the relevant local phase equilibria require experiment. Substrate dilution is **not** a substitute for qualifying the powder: the undiluted upper layers and spatially nonuniform fusion boundary must also meet the Te screen. These are extrapolations from wrought/welding metallurgy, **not AM observations**. (konynenburg1990backgroundstudiesin pages 142-149, riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6)

## 4. Melting, atomization, phase diagram, and CALPHAD

[NUMBERS] [CITE] L. Klemettinen *et al.*, “Recycling of tellurium via copper smelting processes,” *SN Applied Sciences* **2** (2020), article 337, DOI **10.1007/s42452-020-2137-1**, measured substantial Te retention in metallic Cu but approximately **50% Te volatilization under reducing copper–slag conditions at 1,300 °C**. They cite a liquid-Cu Te activity coefficient of about **0.065 at 1,200 °C** and find oxygen-potential-dependent evaporation; primary Cu-matte smelting behaved differently. **Neither 50% nor 0.065 is an atomizer recovery factor**: those are different compositions, gas/slag interfaces, temperatures, and dwell times. Argon induction melting, ultrasonic atomization, and a transient laser pool need their own input–melt–powder–deposit Te mass balance and fume sampling. Elemental Te’s boiling point is approximately **990 °C**, but pure-element boiling alone cannot predict evaporation from a dilute Cu melt. [GAP] No retrieved experiment quantifies Te’s reaction with alumina, zirconia, graphite, Ti-alloy or Mo sonotrodes; oxide/inclusion pickup, probe erosion, and changes in Cu-alloy surface tension, droplet breakup, infrared absorptivity, and powder porosity remain unverified. (klemettinen2020recyclingoftellurium pages 1-2, klemettinen2020recyclingoftellurium pages 4-7, vissers1966laboratoryinvestigationsin pages 12-15)

[CITE] [NUMBERS] The Cu-rich phase evidence in Magnusson, SKB R-17-20 (2017), Appendix A1.15, reproducing Pashinkin and Fedorov’s experimental assessment, gives **log₁₀*x*Te = −7372/*T* + 2.43**, with *x*Te a **mole fraction** and *T* kelvin. It estimates **1 atomic ppm Te at 600 °C**, approximately **0.00020 wt% Te** after atomic-mass conversion; **this is not the measured maximum solubility**. Cu₂Te has numerous polymorphs; the reproduced diagram also identifies CuTe and several invariant temperatures, but its full-composition labels do **not** justify assigning a precise Cu-rich eutectic temperature or composition without resolving the original diagram. The displayed Cu-rich boundary falls from pure Cu’s melting point on Te addition: there is **no evidence that trace Te raises a Cu-rich liquidus above 1,250 °C**. This says nothing about whether the *other* proposed alloying elements already make an alloy unatomizable. (magnusson2017thermodynamicevaluationof pages 41-43, magnusson2017thermodynamicevaluationof media 2f5d53ac)

[GAP] Magnusson explicitly found **no computational thermodynamic assessment of binary Cu–Te** in the literature it surveyed and made **no Cu–P–Te ternary calculation**. This historical finding does **not verify the current contents or validity** of proprietary Thermo-Calc **TCCU**, COST 531, or any subsequently published TDB, nor establish assessed **Cu–Ni–Te** or **Cu–Al–Te** interactions. Before using pycalphad/TCCU to reject or accept a composition, inspect their actual element/phase inventories and parameter references and flag any missing Cu₂Te or ternary terms; a numerical extrapolation is not an assessed marine-alloy phase boundary. (magnusson2017thermodynamicevaluationof pages 12-14, magnusson2017thermodynamicevaluationof pages 14-16, magnusson2017thermodynamicevaluationof pages 41-43)

## 5. Supply, safety, interactions, and numerical bound

[CITE] [NAVY] Te was on the earlier U.S. critical-minerals list. The USGS technical analysis for 2025 **recommended removing** it, but the **final 2025 list retained it**; confusing the draft with the final decision would invert its status. Sources: N. T. Nassar *et al.*, USGS Open-File Report **2025-1047**, DOI **10.3133/ofr20251047**; USGS final-list review reproduced in *Mining Engineering* (May 2026). [NUMBERS] A published historical U.S. price was **US$349/kg in 2011**, declining to approximately **US$70/kg by 2017** (20% of that peak, calculated); **neither is a verified FY2027 quote**, and grade/powder-making costs are unspecified. H. Chung *et al.*, *Canadian Metallurgical Quarterly* **63** (2024) 1626–1642, DOI **10.1080/00084433.2024.2355031**. (nassar2025methodologyandtechnical pages 9-10, staff2022usgsminingreview pages 6-9, chung2024purificationprinciplesand pages 3-5)

[NUMBERS] [CITE] Te and TeO₂ aerosols warrant capture and exposure monitoring during charging, powder transfers, and laser deposition. An older review reports garlic-like breath at airborne Te concentrations **≤0.01 mg/m³** and quotes historical recommendations of **0.1** and **0.01 mg/m³**; these are **not established here as current OSHA permissible exposure limits**. D. R. Vissers and M. J. Steindler, Argonne technical report (1966), DOI **10.2172/4507507**. [GAP] This search did not verify a current OSHA Te PEL, Te-specific RoHS/REACH restriction, or Navy prohibition. Do not confuse restrictions on **cadmium** in CdTe devices with restrictions on elemental Te in copper alloy. (vissers1966laboratoryinvestigationsin pages 12-15, vissers1966laboratoryinvestigationsin pages 68-69, chung2024purificationprinciplesand pages 9-10)

**Interactions for joint constraints.** [CITE] [GAP] Cu₂Te formation competes with keeping Te dissolved; Te is also grouped with S and Se as a copper-chalcogenide-forming embrittling impurity, so assess their **combined** inclusion/segregation burden rather than treating added Te as an independent beneficial solute. In *dilute oxygen-free Cu*, the SKB review does **not** predict phosphorus to neutralize Te’s phase behavior. No verified quantitative Te:Ni, Te:Fe, Te:Mn, Te:Al, Te:O, or Te:S ratio or sum rule applies to the proposed multicomponent powder or its NAB/Cu–Ni fusion zone; do not transfer the dilute-Cu P result as proof for either repair interface. (magnusson2017thermodynamicevaluationof pages 50-51, magnusson2017thermodynamicevaluationof pages 14-16, magnusson2017thermodynamicevaluationof pages 16-21)

**Bound and failure mode.** [SPEC] [NUMBERS] Set a **provisional acceptance ceiling of Te ≤0.003 wt% (30 ppm) in both powder and deposit**, applicable to **both** target families as a project screen. Its documentary basis is the **Cu–Ni hot-workability literature threshold** above; **extension to NAB is a conservative, unvalidated policy choice**, not an ASTM/AWS/MIL specification. Procure toward **≤0.002 wt% (20 ppm)** to provide analytical/processing margin, subject to a validated Te assay; this tighter number is a *project target*, not a published failure threshold. The failure mode setting the ceiling is impurity-associated hot-workability/HAZ cracking and Cu₂Te segregation. For comparison only, C10100’s **0.0002 wt%** limit governs a distinct high-purity-copper grade. No Te functional floor or designed-addition upper bound is justified for seawater DED. [GAP] The evidence is **moderate for rejecting a designed addition, thin for the exact DED/NAB-safe ceiling and any Te–seawater effect**. (magnusson2017thermodynamicevaluationof pages 9-12, magnusson2017thermodynamicevaluationof pages 41-43, riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6)

VERDICT | Te | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.003 | evidence=thin

References

1. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

2. (magnusson2017thermodynamicevaluationof pages 41-43): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

3. (riley1986impurityeffectsin pages 3-4): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

4. (magnusson2017thermodynamicevaluationof pages 9-12): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

5. (riley1986impurityeffectsin pages 4-6): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

6. (klemettinen2020recyclingoftellurium pages 4-7): Lassi Klemettinen, Katri Avarmaa, Dmitry Sukhomlinov, Hugh O’Brien, Pekka Taskinen, and Ari Jokilaakso. Recycling of tellurium via copper smelting processes. SN Applied Sciences, 2:1-9, Feb 2020. URL: https://doi.org/10.1007/s42452-020-2137-1, doi:10.1007/s42452-020-2137-1. This article has 16 citations.

7. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

8. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

9. (chung2024purificationprinciplesand pages 3-5): Hanwen Chung, Semiramis Friedrich, Jeraldiny Becker, and Bernd Friedrich. Purification principles and methodologies to produce high-purity tellurium. Canadian Metallurgical Quarterly, 63:1626-1642, May 2024. URL: https://doi.org/10.1080/00084433.2024.2355031, doi:10.1080/00084433.2024.2355031. This article has 21 citations and is from a peer-reviewed journal.

10. (riley1986impurityeffectsin pages 1-3): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

11. (magnusson2017thermodynamicevaluationof pages 14-16): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

12. (klemettinen2020recyclingoftellurium pages 1-2): Lassi Klemettinen, Katri Avarmaa, Dmitry Sukhomlinov, Hugh O’Brien, Pekka Taskinen, and Ari Jokilaakso. Recycling of tellurium via copper smelting processes. SN Applied Sciences, 2:1-9, Feb 2020. URL: https://doi.org/10.1007/s42452-020-2137-1, doi:10.1007/s42452-020-2137-1. This article has 16 citations.

13. (vissers1966laboratoryinvestigationsin pages 12-15): D. R. Vissers and M. J. Steindler. Laboratory investigations in support of fluid-bed fluoride volatility processes. part x. a literature survey on the properties of tellurium, its oxygen and fluorine compounds. Unknown journal, Feb 1966. URL: https://doi.org/10.2172/4507507, doi:10.2172/4507507. This article has 0 citations.

14. (magnusson2017thermodynamicevaluationof media 2f5d53ac): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

15. (magnusson2017thermodynamicevaluationof pages 12-14): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

16. (vissers1966laboratoryinvestigationsin pages 68-69): D. R. Vissers and M. J. Steindler. Laboratory investigations in support of fluid-bed fluoride volatility processes. part x. a literature survey on the properties of tellurium, its oxygen and fluorine compounds. Unknown journal, Feb 1966. URL: https://doi.org/10.2172/4507507, doi:10.2172/4507507. This article has 0 citations.

17. (chung2024purificationprinciplesand pages 9-10): Hanwen Chung, Semiramis Friedrich, Jeraldiny Becker, and Bernd Friedrich. Purification principles and methodologies to produce high-purity tellurium. Canadian Metallurgical Quarterly, 63:1626-1642, May 2024. URL: https://doi.org/10.1080/00084433.2024.2355031, doi:10.1080/00084433.2024.2355031. This article has 21 citations and is from a peer-reviewed journal.

18. (magnusson2017thermodynamicevaluationof pages 50-51): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

19. (magnusson2017thermodynamicevaluationof pages 16-21): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.
