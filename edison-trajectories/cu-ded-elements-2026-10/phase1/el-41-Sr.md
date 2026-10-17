<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: d9d08475-7124-465c-9d92-3c93df8ba79b
- Submitted: 2026-10-17T19:01:15Z
- Fetched: 2026-10-17T19:33:16Z (status: success)
- Raw trajectory JSON: ../raw/el-41-Sr.json.gz
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

ELEMENT UNDER REVIEW: Sr (deoxidizer). Representative of the heavier alkaline earths (Sr, Ba): any use as a modifier, grain refiner or deoxidizer in copper alloys.

Answer for Sr specifically, not for copper alloys in general:
1. ROLE: what Sr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sr, Cu-Ni-Sr and Cu-Al-Sr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Sr (deoxidizer). Representative of the heavier alkaline earths (Sr, Ba): any use as a modifier, grain refiner or deoxidizer in copper alloys.

Answer for Sr specifically, not for copper alloys in general:
1. ROLE: what Sr does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sr ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sr changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sr, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sr, Cu-Ni-Sr and Cu-Al-Sr are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sr in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sr neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sr | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Sr in pre-alloyed copper powder for marine DED

**Decision — EXCLUDE Sr as a designed addition from both Cu–Ni and aluminum-bronze compositions.** [CITE] A Cu-alloy grain-refinement assessment identifies **SrO as a *theoretical* candidate nucleant**, but its copper-melting experiments did **not** add Sr. An aluminum-bronze microalloying paper mentions Sr in the melt, yet the accessible text supplies neither a verified retained Sr concentration nor Sr-specific marine-corrosion or DED results. Neither establishes an addition that meets the proposed as-deposited C71500 seawater benchmark. There is also no supported Sr upper bound, functional floor, or specification-derived impurity limit to transfer into the composition palette. This is an evidence-based screening decision, **not** a finding that every trace of Sr is harmful. [CITE] Cziegler, *Aspects of Grain Refinement in Copper Alloys*, University of Leoben, 2015; Nová, Machuta and Raur, *Manufacturing Technology* **17** (2017), 797–804, DOI: **10.21062/ujep/x.2017/a/1213-2489/mt/17/5/797**. (cziegler2015aspectsofgrain pages 1-6, nova2017theinfluenceof pages 1-2)

## 1. Role, candidate mechanisms, and specifications

- **Cu–Ni, NAB and other aluminum bronzes, Mn–Al bronze, tin bronze/gunmetal, brasses, Cu–Ni–Sn, and Cu–Ni–Si:** [GAP] No verified Sr-containing commercial or Navy grade, intentional Sr **range in wt%**, or demonstrated Sr-specific service mechanism was established in the reviewed evidence. In particular, **none of the named ASTM B111/B171/B466/B148/B369, MIL-T-16420/MIL-B-24480/MIL-C-15726, AWS A5.7, EN 12449, or UNS/CDA grades can responsibly be assigned an Sr range here**. Absence of an identified Sr specification is not an analytical proof of zero Sr in every heat. [CITE] Nová and colleagues discuss aluminum-bronze *microalloying*, but the accessible abstract does not demonstrate retained Sr, its phase, or a quantified Sr effect; DOI: **10.21062/ujep/x.2017/a/1213-2489/mt/17/5/797**. (nova2017theinfluenceof pages 1-2)
- **Possible deoxidizer/inoculant, not proven corrosion addition:** [CITE] Cziegler screened more than 1,000 candidate nucleating compounds and ranked **SrO** among promising candidates by lattice match and melting point; the author explicitly called for further thermodynamic-stability assessment. The *actual* copper-melting additions were Sn, Zn, P, Mg and Fe—not Sr. An oxide inclusion suggested as a nucleant is not evidence for Sr solid-solution strengthening, a protective Sr-bearing seawater film, or improved castability after laser remelting. DOI: **not assigned to the 2015 thesis**. (cziegler2015aspectsofgrain pages 1-6, cziegler2015aspectsofgrain pages 86-91)
- [GAP] No verified Sr-bearing Cu–Ni or bronze precipitate, Sr-induced dealloying inhibition, or Sr–Ni/Fe/Mn/Al strengthening mechanism was found. A strontium signal on an ancient seabed bronze should **not** be counted as alloying evidence: its investigators attribute Ca and Sr to environmental contamination. [CITE] Armetta *et al.*, *Scientific Reports* **11** (2021), DOI: **10.1038/s41598-021-02425-6**. (armetta2021microstructureandphase pages 4-6, armetta2021microstructureandphase pages 2-4)

## 2. Seawater corrosion

**There is no defensible Sr-beneficial or Sr-harmful concentration interval in wt% for these alloys.** [GAP] The reviewed material supplies no paired Sr-free/Sr-bearing marine-copper measurements of corrosion rate, *E*<sub>corr</sub>, polarization resistance, impedance or film resistance, pitting/crevice potential, selective-attack depth, erosion–corrosion, or permissible seawater velocity. Therefore no numerical Sr-related improvement relative to wrought C71500—and no threshold above which Sr demonstrably worsens seawater corrosion—can be stated. The seabed-bronze study records environmental Sr contamination, not a controlled alloy comparison. [CITE] Armetta *et al.*, DOI: **10.1038/s41598-021-02425-6**. (armetta2021microstructureandphase pages 4-6, armetta2021microstructureandphase pages 2-4)

## 3. DED, welding, and dissimilar repair

[GAP] No Sr-controlled **copper-alloy** blown-powder DED, weld-metal, or cladding comparison was verified for solidification cracks, reheated-layer liquation cracks, pores, or laser-induced Sr loss. AWS A5.7 filler families **ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl** therefore provide no Sr-specific validated remedy or limit here; findings for Sr-modified *Al–Si* castings must not be transferred to copper-matrix deposits. Plausible tests—not established outcomes—are Sr partitioning to final liquid at interdendritic or diluted interfaces, oxide-inclusion-associated pores, and changed chemistry on remelting. Assess self-builds and separate C95800 and wrought Cu–Ni dilution zones; measure *retained* rather than charge Sr before attributing any cracking or corrosion change to it. Cziegler’s distinction between hypothetical SrO nucleation and tested copper solutes is particularly important. [CITE] Cziegler, 2015 thesis, DOI: **not assigned**. (cziegler2015aspectsofgrain pages 1-6, cziegler2015aspectsofgrain pages 38-42)

## 4. Induction melting and ultrasonic powder making

**Risk assessment, not measured AMAZEMET performance:** Sr’s oxygen affinity motivates concerns about oxidation during addition, tapping, ultrasonication, powder collection and laser exposure, with a possible loss of controlled metallic Sr to oxide inclusions. Reaction or contamination involving **alumina versus zirconia crucibles, graphite, a Ti-alloy versus Mo sonotrode**, or Sr-bearing laser fume has **not** been quantified for the proposed Cu alloys. [GAP] No Sr-specific evaporation-loss fraction, liquid-metal surface-tension change, powder size distribution, oxygen pickup, or atomization yield can be supplied. Oxygen-free Cu feed and argon shielding do not themselves verify that Sr remains metallic or that oxide inclusions are absent. The candidate-nucleant study explicitly leaves thermodynamic stability unresolved. [CITE] Cziegler, 2015 thesis, DOI: **not assigned**. (cziegler2015aspectsofgrain pages 86-91, cziegler2015aspectsofgrain pages 1-6)

## 5. Cu–Sr phase equilibria and CALPHAD

- [CITE] There **is** a dedicated binary review—Chakrabarti and Laughlin, “The Cu–Sr (Copper–Strontium) System,” *Bulletin of Alloy Phase Diagrams* **5** (1984), 391–396, DOI: **10.1007/BF02872963**—and a published binary thermodynamic optimization—Risold, Hallstedt and Gauckler, “Thermodynamic Optimization of the Ca–Cu and Sr–Cu Systems,” *CALPHAD* **20** (1996), 151–160, DOI: **10.1016/S0364-5916(96)00022-3**. **Their phase diagrams and numerical phase-boundary tables were not obtainable for verification in this review**. Consequently the maximum Sr solid solubility in Cu **in wt% and at a specified temperature**, individual metallic Cu–Sr intermetallic formulae, invariant temperatures/compositions, and dilute Cu-rich liquidus slope are **not reported as numbers**; inventing these would turn an unverified diagram into a false design constraint. (cziegler2015aspectsofgrain pages 1-6)
- [NUMBERS] Thermo-Calc’s documented **TCCU5 (2022)** framework contains **32 elements**, **315** solution/intermetallic phases, and **148** assessed binaries plus **64** assessed ternaries. Its explicit element list includes Ca but **excludes Sr**. Thus TCCU5 cannot generate a validated Sr-dependent liquidus, Scheil path, Sr phase fraction or Sr surface tension for Cu–Ni–Sr or Cu–Al–Sr; pycalphad requires a separately compatible Sr-bearing assessment. [CITE] Jansson *et al.*, “Phase Transformations and Kinetic Simulations of Cu-based Alloys,” *Copper Alloys 2022* conference proceedings, pp. 28–30, ISBN **978-3-910411-01-2**; **no DOI identified**. (janssonUnknownyearphasetransformationsand pages 28-30)
- [CITE] Wang, Ji, Pei, Cheng and Rao report an experimental/thermodynamic **Zn–Cu–Sr** ternary, *CALPHAD* **81** (2023), 102561, DOI: **10.1016/j.calphad.2023.102561**. This is evidence that Sr-containing assessments exist **outside TCCU**, not validation of Cu–Ni–Sr or Cu–Al–Sr. [GAP] No verified Cu–Ni–Sr or Cu–Al–Sr assessment, confirmed COST 531 Sr coverage, or compatible published TDB was obtained. **Whether Sr moves any proposed multicomponent liquidus above the approximately 1,200–1,250 °C useful-superheat ceiling is undetermined**, not a demonstrated reason to accept or reject a numerical Sr content. (janssonUnknownyearphasetransformationsand pages 28-30)

## 6. Supply, price, and safety

- [CITE] [NAVY] **Sr is not on the 2022 U.S. final critical-minerals list**: the USGS states it was removed relative to 2018. It is **also absent from the 2025 final list** in the USGS’s published rendering of that list. This status must not be conflated with Ni’s listing or Cu’s later addition. [CITE] USGS National Minerals Information Center, “USGS mineral review,” *Mining Engineering* (May 2024), pp. 43–49, citing **87 FR 10381**; USGS, *Critical Minerals Memory Match Game*, General Information Product **266** (2026), DOI: **10.3133/gip266**. The USGS 2025 *draft methodology* separately classified Sr’s modeled risk as **negligible** and did not recommend it; Nassar *et al.*, USGS Open-File Report **2025–1047**, DOI: **10.3133/ofr20251047**. (staff2024usgsmineralreview pages 6-8, olinger2026criticalmineralsmemory media 2a575c2d, nassar2025methodologyandtechnical media 6aad7a32)
- [GAP] **Price per kg of Sr metal: not verified.** Celestite-ore or strontium-carbonate quotations are not interchangeable with a price for pure metal or a Cu–Sr master alloy; no approximate dollar-per-kg figure is asserted without a specified product, purity and date. [CITE] USGS economic assessment, DOI: **10.3133/ofr20251047**, addresses mineral-supply risk rather than an attributable Sr-metal purchase quotation. (nassar2025methodologyandtechnical pages 31-32, nassar2025methodologyandtechnical pages 33-35)
- **Handling controls:** Treat reactive Sr-bearing feed and fine metal powder as potential oxidation/fire and inhalation hazards; use supplier SDS, dry inert handling, suitable fire controls, and local exhaust for atomization and laser fume. [GAP] No Sr-specific OSHA exposure limit, applicable RoHS/REACH prohibition, Navy alloy restriction, or dose–response measurement for these powders was established by the reviewed evidence. Do not label stable Sr compounds and elemental Sr powder as having identical hazards, or substitute an unverified regulatory number for a measured exposure. (cziegler2015aspectsofgrain pages 1-6)

## 7. Bounds and joint constraints

| Palette field | Sr recommendation in wt% | Basis and limiting failure mode |
|---|---:|---|
| Designed addition; Cu–Ni and Al bronze | **Exclude; target 0 added Sr** | No established Sr-containing marine grade or demonstrated C71500-comparable as-deposited corrosion; uncertain retention, oxide inclusions and dissimilar-interface response. **Zero added is a design choice, not an ASTM impurity limit.** (nova2017theinfluenceof pages 1-2, cziegler2015aspectsofgrain pages 1-6) |
| Conservative maximum; non-conservative maximum; functional floor | **NA; NA; NA** | No verified Sr-bearing qualifying grade or quantitative dose–response from which to set these values. (nova2017theinfluenceof pages 1-2, cziegler2015aspectsofgrain pages 1-6) |
| Maximum tolerable *incidental* Sr in powder **and** deposit | **NA** | No named specification or study establishing a transferable Sr maximum in wt% or ppm was verified. Specify an assay/reporting requirement and acceptance testing rather than invent a certified limit. (nova2017theinfluenceof pages 1-2, janssonUnknownyearphasetransformationsand pages 28-30) |

[**Joint-constraint flags**] No validated Sr/(Ni + Fe), Sr/Al, or Sr/Mn ratio exists. Record charge-to-powder-to-deposit Sr and oxygen together; examine any Sr-rich particles with O and substrate-derived Al/Fe/Ni/Mn at diluted interfaces. These are **proposed measurements**, not demonstrated neutralization or synergy. In particular, an SrO grain-refinement hypothesis cannot establish that Sr removes enough oxygen to avoid pores, cancels deleterious Fe effects, or improves Cu–Ni film chemistry. [CITE] Cziegler, 2015 thesis, DOI: **not assigned**. (cziegler2015aspectsofgrain pages 1-6, cziegler2015aspectsofgrain pages 86-91)

**Evidence quality — thin.** [GAP] The decisive gaps are retained-Sr analyses of copper powders and deposits, a verified Cu-rich solvus/liquidus readout, Sr-specific copper-weld cracking tests, and matched as-deposited 30-day marine exposure against C71500. The available SrO work is theoretical; the accessible aluminum-bronze account does not establish a transferable dosage; archaeological Sr is environmentally acquired; and the documented TCCU5 database does not include Sr. **Do not report numerical “helps” or “harms” ranges until those measurements exist.** (cziegler2015aspectsofgrain pages 1-6, nova2017theinfluenceof pages 1-2, armetta2021microstructureandphase pages 4-6, janssonUnknownyearphasetransformationsand pages 28-30)

VERDICT | Sr | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (cziegler2015aspectsofgrain pages 1-6): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

2. (nova2017theinfluenceof pages 1-2): Iva Nová, Jiří Machuta, and Luboš Raur. The influence of microalloying on the thermal treatment of aluminum bronzes. Manufacturing Technology, 17:797-804, Oct 2017. URL: https://doi.org/10.21062/ujep/x.2017/a/1213-2489/mt/17/5/797, doi:10.21062/ujep/x.2017/a/1213-2489/mt/17/5/797. This article has 4 citations and is from a peer-reviewed journal.

3. (cziegler2015aspectsofgrain pages 86-91): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

4. (armetta2021microstructureandphase pages 4-6): Francesco Armetta, Maria Luisa Saladino, Antonella Scherillo, and Eugenio Caponetti. Microstructure and phase composition of bronze montefortino helmets discovered mediterranean seabed to explain an unusual corrosion. Scientific Reports, Nov 2021. URL: https://doi.org/10.1038/s41598-021-02425-6, doi:10.1038/s41598-021-02425-6. This article has 15 citations and is from a peer-reviewed journal.

5. (armetta2021microstructureandphase pages 2-4): Francesco Armetta, Maria Luisa Saladino, Antonella Scherillo, and Eugenio Caponetti. Microstructure and phase composition of bronze montefortino helmets discovered mediterranean seabed to explain an unusual corrosion. Scientific Reports, Nov 2021. URL: https://doi.org/10.1038/s41598-021-02425-6, doi:10.1038/s41598-021-02425-6. This article has 15 citations and is from a peer-reviewed journal.

6. (cziegler2015aspectsofgrain pages 38-42): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

7. (janssonUnknownyearphasetransformationsand pages 28-30): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

8. (staff2024usgsmineralreview pages 6-8): U Staff. Usgs mineral review. Unknown journal, 2024.

9. (olinger2026criticalmineralsmemory media 2a575c2d): Danielle A. Olinger. Critical minerals memory match game. General Information Product, Jan 2026. URL: https://doi.org/10.3133/gip266, doi:10.3133/gip266. This article has 0 citations.

10. (nassar2025methodologyandtechnical media 6aad7a32): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

11. (nassar2025methodologyandtechnical pages 31-32): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

12. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
