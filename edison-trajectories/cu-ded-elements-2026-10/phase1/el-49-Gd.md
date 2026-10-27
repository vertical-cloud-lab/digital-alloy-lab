<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 1de568a4-8bf1-4bc8-ba18-27dea662848a
- Submitted: 2026-10-17T19:02:02Z
- Fetched: 2026-10-17T19:20:35Z (status: success)
- Raw trajectory JSON: ../raw/el-49-Gd.json.gz
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

ELEMENT UNDER REVIEW: Gd (rare earth). Representative of the heavy lanthanides (Gd through Lu): any use in copper alloys.

Answer for Gd specifically, not for copper alloys in general:
1. ROLE: what Gd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Gd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Gd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Gd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Gd, Cu-Ni-Gd and Cu-Al-Gd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Gd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Gd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Gd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Gd (rare earth). Representative of the heavy lanthanides (Gd through Lu): any use in copper alloys.

Answer for Gd specifically, not for copper alloys in general:
1. ROLE: what Gd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Gd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Gd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Gd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Gd, Cu-Ni-Gd and Cu-Al-Gd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Gd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Gd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Gd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Gadolinium in copper-alloy powder for marine DED

**Recommendation — EXCLUDE Gd as an intentional addition from both the Cu–Ni and aluminum-bronze search palettes.** This is a decision about the *present proposal*, not a claim that Gd can never benefit a copper alloy. The retrieved record does not establish a Gd content that improves as-deposited seawater corrosion while preserving crack-free, repair-compatible laser deposition. A published Al–Cu–Gd thermodynamic assessment and a newly indexed study of Gd in a Cu–Al–Ni–Mn shape-memory alloy make Gd scientifically testable, but neither supplies a verified design bound for the specified marine deposits. Gd also introduces an additional critical-mineral supply dependency. Assigning a functional floor, a safe upper bound, or a standards-based impurity limit would imply evidence that was not obtained. (staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 3-5)

## 1. Role and commercial precedent

**[GAP]** No *verified intentional Gd range in wt%* was found for marine Cu–Ni, nickel–aluminum bronze (NAB), other aluminum or Mn–Al bronzes, tin bronze or gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. In particular, this review found no qualifying Gd-bearing commercial or Navy alloy under **[SPEC]** ASTM B111, B171, B466, B148, or B369; MIL-T-16420, MIL-B-24480, or MIL-C-15726; AWS A5.7; EN 12449; or a corresponding UNS/CDA marine designation. This is **not** a claim that each specification establishes a numerical maximum of zero: without its applicable edition and complete chemical-composition/“other elements” provisions, no such maximum can be attributed to it. The retrieved Cu–Zn–Sn–P–Ni sheet patent, US 9,080,228 B2, concerns electrical components and does not demonstrate a marine Gd addition. (US9080228B2 pages 4-5, US9080228B2 pages 9-10)

**[CITE] [GAP]** Cu–Gd compound formation and limited equilibrium incorporation in Cu are plausible subjects for phase-diagram study; they are not evidence that Gd provides useful solid-solution strengthening, a particular precipitate population, grain refinement, deoxidation, or a protective seawater film in C71500 or C95800. Gd’s oxygen affinity motivates a *hypothesis* of oxide formation or oxygen scavenging, but neither Gd₂O₃ enrichment in a protective marine film nor inhibition of dezincification, dealuminification, or selective Ni/Fe attack was verified. The Cu-rich phase boundary must be checked before specifying a precipitate or solubility-based mechanism. Relevant primary literature is M. M. Carnasciali, S. Cirafici and E. Franceschi, “On the Gd–Cu system,” *Journal of the Less-Common Metals* (1983), DOI **10.1016/0022-5088(83)90235-7**; and X. Zhou, Y. Ning and Q. Li, “Extension of solid solubility of rare earth metals in copper by rapid solidification,” *Journal of Alloys and Compounds* **183** (1992) 168–173, DOI **10.1016/0925-8388(92)90741-Q**. Their full texts were not obtained here; they cannot substantiate a numerical Gd floor or maximum. (nassar2025methodologyandtechnical pages 1-4)

## 2. Seawater corrosion

**[GAP]** No recoverable, controlled Gd-versus-Gd-free comparison in the relevant copper-rich families established corrosion rate, *E*₍corr₎, linear-polarization resistance, impedance-derived film resistance, cyclic-polarization or crevice thresholds, 30-day selective-attack depth, erosion–corrosion, or a seawater velocity limit. Consequently, the **helpful range and harmful range in wt% are both unknown**; neither can be inferred from Gd-containing magnesium alloys, Gd-doped oxides on copper foam, or marine performance of alloys without Gd. A positive potential shift alone would not demonstrate resistance to localized attack. (US9080228B2 pages 4-5, US9080228B2 pages 9-10)

**[CITE] [GAP]** A directly relevant *lead*, not an extracted result, is J. Zhang *et al.*, “Effect of Gd content on the microstructure evolution and corrosion resistance of Cu–Al–Ni–Mn–Gd shape memory alloys,” *Intermetallics* **197** (2026) 109445, DOI **10.1016/j.intermet.2026.109445**. It was indexed with an October 2026 date, but its full text could not be obtained. Its Gd contents, electrolyte, quantitative results, and direction of effect therefore remain **unverified**; moreover a Cu–Al–Ni–Mn shape-memory alloy is not cast C95800 NAB or a deposited repair. It must not be used to claim parity with wrought C71500. (staff2022usgsminingreview pages 9-11)

## 3. DED, welding, and repair dilution

**[GAP]** No Gd-controlled blown-powder Cu-alloy DED, laser-cladding, or marine welding comparison was verified. Gd’s effects on solidification cracking, remelted-layer liquation cracking, oxide-associated porosity, laser-induced oxidation or evaporation, and retention after dilution into C95800 or wrought Cu–Ni are **unknown**. AWS A5.7 filler classes ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl identify useful *Gd-free repair-process comparators*, not evidence that Gd improves their weldability. Casting, wrought, and welding evidence, if subsequently obtained, would still require validation in the stipulated no-post-heat-treatment, multilayer laser process. (US9080228B2 pages 4-5, US9080228B2 pages 9-10)

**[GAP] Mechanistic risks to test, not measured outcomes:** segregation of Gd or a Gd-bearing final solidification constituent could extend terminal freezing and promote hot tears; a reheated constituent could liquate; entrained Gd-rich oxides could nucleate pores or inclusions. NAB dilution also changes local Al, Ni, Fe and Mn simultaneously, whereas Cu–Ni dilution changes Gd concentration and freezing path. None of these statements supplies a Gd threshold or establishes that those failures occur. A defensible test would compare matched Gd-free and Gd-bearing pre-alloyed powders, measured retained Gd and oxygen, transverse crack/inclusion mapping, and interface-resolved corrosion on **both** substrates.

## 4. Induction melting and ultrasonic atomization

**[GAP]** No verified numerical recovery, oxide-inclusion rate, surface-tension change, atomization yield, vapor-loss rate, or crucible/sonotrode reaction rate exists here for Cu–Gd melted under the specified conditions. Evaluate oxidation during charging, melting, droplet breakup, powder storage and laser deposition; examine whether alumina or zirconia supplies oxygen or reaction products, whether graphite introduces carbon, and whether Ti-alloy or Mo sonotrode contact contaminates the melt. These are **qualification questions**, not demonstrated incompatibilities. Pure Gd melting behavior is not a substitute for the liquidus of the actual multicomponent powder. Analyze charge, melt, classified powder and deposited metal separately for Gd and oxygen before treating nominal wt% as retained wt%.

## 5. Phase diagrams and CALPHAD

**[CITE] [GAP]** A published assessment *does* exist: L. G. Zhang, H. Q. Dong, G. X. Huang, J. Shan, L. B. Liu and Z. P. Jin, “Thermodynamic assessment of the Al–Cu–Gd system,” *Calphad* (2009), DOI **10.1016/j.calphad.2009.08.003**. The original binary study is Carnasciali *et al.*, DOI **10.1016/0022-5088(83)90235-7**. Neither full assessment nor a usable parameter file was available for verification. Accordingly, **the maximum equilibrium Gd solubility in Cu in wt% and its temperature, the complete Cu–Gd intermetallic and invariant-reaction list, and a Gd-dependent liquidus shift cannot be reported reliably here**. Naming a nominally plausible compound such as Cu₅Gd is not a substitute for verifying the Cu-rich liquidus and reaction sequence. In particular, no calculation establishes whether an actual Cu–Ni–Gd or Cu–Al–Gd candidate exceeds the approximately **1,200–1,250 °C** useful-atomization-liquidus ceiling. (nassar2025methodologyandtechnical pages 1-4)

**[GAP]** A *published Al–Cu–Gd assessment* is distinct from confirmation that **Thermo-Calc TCCU**, **COST 531**, or a distributable **pycalphad-readable TDB** contains internally compatible Cu–Gd, Cu–Ni–Gd and Cu–Al–Gd descriptions. Database inclusion and version must be inspected, not assumed; an unassessed Cu–Ni–Gd ternary extrapolation is not a validated phase map. For any future candidate, calculate equilibrium and Scheil liquidus/terminal constituent over powder–deposit–dilution compositions, then verify by DSC and microscopy before using a phase boundary as a wt% bound.

## 6. Supply, cost and safety

**[CITE] [NAVY] [NUMBERS]** Gd is a U.S. critical mineral: the USGS account identifies its inclusion in the **2025 final list**, published **7 November 2025**, **90 FR 50494**, and identifies the preceding **2022** list. The same account reports Chinese export controls covering Gd introduced in **April 2025**; it lists copper and nickel on the 2025 final list as well. These are supply-chain facts, **not** evidence of an approved Navy Gd-bearing alloy. See also N. T. Nassar *et al.*, USGS *Open-File Report 2025–1047*, DOI **10.3133/ofr20251047**; that report concerns methodology/draft assessment and should not itself be called the final legal notice. (nassar2025methodologyandtechnical pages 4-9, staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 3-5)

**[GAP]** A defensible approximate **USD/kg for metallic Gd** could not be verified: an oxide quote, metal quote and master-alloy quote differ in chemistry, purity, quantity and date. No Gd-specific OSHA exposure limit, RoHS/REACH composition prohibition, or Navy material prohibition was verified; **absence of a verified rule is not an exemption**. Treat respirable atomized powder and laser fume as exposure hazards; perform combustible-metal-dust and process-specific fire assessment, inert-gas/asphyxiation controls, local exhaust, and applicable SDS/industrial-hygiene review. Do not assume that a limit for a gadolinium contrast agent applies to metallic powder.

## 7. Bounds and interactions

**Decision and bounds — [GAP].** **EXCLUDE** intentional Gd for *both* target families. There is no established commercial/Navy or demonstrated DED/cladding **conservative maximum**, no experimentally defensible **non-conservative maximum**, and no measured **functional floor**, all in wt%. Because the decision is EXCLUDE rather than LIMIT, **impurity maximum is NA**, not “0 wt%”: none of the named specifications or retrieved studies provides a verifiable Gd-specific ppm/wt% acceptance ceiling for both powder and deposit. Procure Gd-free feedstock, measure incidental Gd when relevant, and apply the complete purchased-material specification’s applicable *total-other-elements* provision rather than inventing a Gd-specific limit. The failure mode that prevents *each proposed designed bound* is lack of linked evidence for retained composition → cracking/oxidation → as-deposited localized seawater attack; an exact numerical failure threshold is not known.

**Interactions — [GAP].** Do not impose a numerical Gd+Ni, Gd+Fe, Gd+Mn, Gd+Al, Gd+O, or Gd/S/P constraint without ternary equilibria and measured partitions. Candidate dependencies for a *later* study are oxygen consumed versus Gd recovered; Gd enrichment in Al-bearing constituents after NAB dilution; possible Gd–S/O inclusions; and competition among Cu, Ni, Fe, Mn and Al for the local solidification path and protective-film chemistry. None demonstrates that Gd neutralizes a harmful element or substitutes for Ni in seawater service.

**Evidence quality: thin.** The strongest available evidence concerns Gd’s supply status, not performance in the target alloy/process. The 1983 Cu–Gd work, 1992 rapid-solidification paper, 2009 Al–Cu–Gd assessment and October 2026 shape-memory corrosion paper are identifiable by DOI but were not available in full for numerical checking. In particular, no Gd-specific corrosion benefit, safe concentration, weldability effect, or alloy-specific regulatory threshold should be presented as established. No publications by the specified PI were used. (nassar2025methodologyandtechnical pages 4-9, staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 3-5)

VERDICT | Gd | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

2. (staff2022usgsminingreview pages 3-5): US Staff. Usgs mining review. Unknown journal, 2022.

3. (US9080228B2 pages 4-5): Keiichiro Oishi. Copper alloy sheet and method for manufacturing copper alloy sheet. Patent (WO,EP,US,CN,JP,KR,TW), 2015.

4. (US9080228B2 pages 9-10): Keiichiro Oishi. Copper alloy sheet and method for manufacturing copper alloy sheet. Patent (WO,EP,US,CN,JP,KR,TW), 2015.

5. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

6. (nassar2025methodologyandtechnical pages 4-9): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
