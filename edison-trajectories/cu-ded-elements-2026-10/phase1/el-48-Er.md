<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 18e844f5-d208-4077-92c5-9019754e6d70
- Submitted: 2026-10-17T19:02:00Z
- Fetched: 2026-10-17T19:20:34Z (status: success)
- Raw trajectory JSON: ../raw/el-48-Er.json.gz
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

ELEMENT UNDER REVIEW: Er (rare earth). Erbium additions to copper alloys, if any.

Answer for Er specifically, not for copper alloys in general:
1. ROLE: what Er does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Er ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Er changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Er, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Er, Cu-Ni-Er and Cu-Al-Er are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Er in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Er neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Er | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Er (rare earth). Erbium additions to copper alloys, if any.

Answer for Er specifically, not for copper alloys in general:
1. ROLE: what Er does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Er ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Er changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Er, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Er, Cu-Ni-Er and Cu-Al-Er are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Er in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Er neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Er | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Erbium (Er) in Cu-balance marine DED alloys

**Decision: EXCLUDE Er as a designed addition from both the Cu–Ni and aluminum-bronze search spaces.** This is an evidence decision, not proof that every Er addition is harmful. Cu–Er compounds are documented, but the retrieved literature does not establish an Er content that improves **as-deposited** seawater corrosion while preserving powder processability and crack-free repair. No Er-specific specification limit supports calling Er a controlled impurity either. (riani2002ternaryrareearth pages 1-2)

The evidence audit distinguishes Cu-rich results from a superficially relevant Al-rich chloride-corrosion study:

| Requested property | Verified Er-specific Cu-rich evidence | Decision implication |
|---|---|---|
| Cu–Er phases | ErCu₅ is reported as an observed intermetallic; Er₂Cu₉ is assigned only by analogy for Er, not established experimentally (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3) | Intermetallic formation is plausible, but it supplies no defensible marine-alloy addition bound. |
| Chloride/seawater corrosion | No quantitative Er-specific data found for Cu-rich alloys in seawater, ASTM D1141 solution, or 3.5 wt% NaCl. | No demonstrated improvement in corrosion rate, film resistance, pitting, crevice attack, dealloying, or erosion-corrosion. |
| DED and welding | No Er-bearing Cu-alloy DED, cladding, or marine filler-metal tests found. | Effects on cracking, liquation, porosity, dilution, oxidation loss, and as-deposited corrosion remain unknown. |
| Aluminum-alloy evidence | Published alloys containing 1.3–1.4 wt% Er and 2.6–3.0 wt% Cu are **Al-balance**, not Cu-balance (glavatskikh2024microstructureandphase pages 2-4, glavatskikh2024microstructureandphase media 2a2c0006). | Their microstructure and chloride-corrosion results are not transferable to Cu–Ni or aluminum bronze. |
| Powder making, solubility, liquidus, CALPHAD | No reliable Cu-rich numerical values verified for Er solubility, liquidus shift, atomization recovery, crucible/sonotrode reactions, or TCCU/COST 531 coverage. Strong Er–O affinity and Er₂O₃ formation are supported only indirectly and experimentally in high-purity iron, not copper (wang2026interpretablemachinelearning pages 1-4, wang2026interpretablemachinelearning pages 19-22). | Do not invent a processing window or upper bound; oxidation/inclusion risk remains unresolved. |
| Supply criticality | The final 2025 U.S. critical-minerals list explicitly includes both erbium and copper (staff2022usgsminingreview pages 6-9). | Er would add another critical-mineral dependency without demonstrated Cu-alloy performance benefit. |
| Overall design decision | No commercial/Navy Cu-alloy specification, quantitative marine-corrosion benefit, or Cu-alloy DED/welding validation was found. | **EXCLUDE** Er from the designed Cu-balance search palette; report bounds as NA rather than assigning an unsupported impurity limit. |


*Table: Conservative audit of evidence relevant to erbium in Cu-balance marine alloys. It separates verified Cu–Er phase information from nontransferable aluminum-alloy results and unresolved performance data.*

## 1. Role and specified alloys

**[CITE]** Riani *et al.* report Cu–Er intermetallic phase formation, including ErCu₅; their Er₂Cu₉ assignment is **by analogy**, not an experimentally established Er phase. Thus Er cannot be presumed to remain entirely in Cu solid solution. The phase evidence does **not** demonstrate grain refinement, useful precipitation, deoxidation, protective Er-containing seawater films, or inhibition of dezincification, dealuminification, or other selective attack in a Cu-balance alloy. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3)

**[SPEC] [NAVY] [GAP]** No verified Er addition or Er range was found for the marine Cu–Ni, aluminum-bronze/NAB, Mn–Al-bronze, tin-bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si families. In particular, this review found **no Er range to report** from ASTM B111, B171, B466, B148, or B369; MIL-T-16420, MIL-B-24480, or MIL-C-15726; AWS A5.7; EN 12449; or a verified UNS/CDA marine-alloy composition. Absence of an Er entry must not be restated as a specified *maximum permissible Er impurity*. No Er-specific Navy application or funding result was identified. (riani2002ternaryrareearth pages 1-2)

## 2. Seawater corrosion

**[GAP]** For **Er added to Cu-balance alloys**, no defensible quantitative comparison was retrieved for natural seawater, ASTM D1141 substitute ocean water, or 3.5 wt% NaCl. Consequently the helpful and harmful Er ranges, corrosion-rate change, *E*<sub>corr</sub>, film or polarization resistance, pit/crevice behavior, depth of selective attack, erosion–corrosion, and allowable velocity are **unknown**. There is no basis to assert equivalence to wrought C71500, particularly for an unheated deposit. (riani2002ternaryrareearth pages 1-2, glavatskikh2024microstructureandphase pages 1-2)

**[NUMBERS] [CITE]—important nontransferable result.** Glavatskikh *et al.* tested Er-bearing **Al-balance** alloys in 3.5 wt% NaCl. Their measured compositions contain **1.3–1.4 wt% Er but only 2.6–3.0 wt% Cu**; the reported **0.68–0.98 µA cm⁻²** corrosion-current range concerns these Al-matrix alloys and accompanying Cr-related phases and processing, **not Er-treated copper**. Their composition table was checked visually. None of those Er contents or electrochemical values supplies a Cu–Ni or NAB design bound. (glavatskikh2024microstructureandphase pages 2-4, glavatskikh2024microstructureandphase media 2a2c0006, glavatskikh2024microstructureandphase pages 1-2)

## 3. DED, welding, and repair interfaces

**[GAP]** No Er-specific single-stream blown-powder Cu-alloy DED result, nor an Er-bearing ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl filler comparison, was verified. Effects on solidification cracking, reheated-layer liquation cracking, porosity, laser oxidation/evaporation loss, and composition gradients after dilution into cast C95800 or wrought Cu–Ni remain unmeasured. Cu–Er compound formation makes interdendritic segregation and local galvanic contrast **questions to test**, not demonstrated failure mechanisms. Do not assign a crack-prevention or crack-onset Er threshold from unrelated Al-alloy welding or casting. (riani2002ternaryrareearth pages 1-2, glavatskikh2024microstructureandphase pages 1-2, wang2026interpretablemachinelearning pages 1-4)

## 4. Melt, atomization, and laser processing

**[CITE] [GAP]** Er has strong oxygen affinity: a 2026 study reports Er₂O₃-bearing particles and models oxide stability in an **iron** melt. This supports treating oxygen pickup, oxide inclusions, and reduced recovered metallic Er as credible *screening risks*, but does not measure any of them in an argon-melted Cu alloy or AMAZEMET powder. Reactions with alumina, zirconia, graphite, Ti-alloy or Mo sonotrodes; changes in surface tension; Er vapor loss; and recovery across induction melting, ultrasonic atomization and the approximately 1.07-µm laser were not quantified for this system. Crucible compatibility should therefore be tested, not inferred from the iron experiment. (wang2026interpretablemachinelearning pages 1-4, wang2026interpretablemachinelearning pages 4-7, wang2026interpretablemachinelearning pages 19-22)

## 5. Phase diagram and CALPHAD

**[CITE]** A Cu–Er binary phase diagram has been reviewed; ErCu₅ is reported, whereas Er₂Cu₉ was assumed by analogy. That distinction matters when interpreting an apparently Er-rich last-to-freeze constituent. **[GAP]** The inspected sources do not give a defensible *maximum Er solubility in Cu in wt% at a named temperature*, Cu-rich invariant temperature/composition, or liquidus-versus-Er curve. Accordingly it cannot be established whether an Er-containing candidate crosses the project's approximately **1,200–1,250 °C practical liquidus ceiling**; neither an increase nor a decrease should be assigned without an applicable assessment or measurement. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3)

**[GAP]** Publication of a binary phase review is **not** verification that a usable assessed Cu–Er parameter set is distributed in Thermo-Calc **TCCU**, **COST 531**, or a particular pycalphad-readable TDB. Cu–Ni–Er and Cu–Al–Er descriptions, and the versions/licences in which they might exist, were likewise not verified. An Al–Cu–Er calculation or an **Al-balance** Thermo-Calc study does not validate Cu-rich ternary predictions; the inspected Al-rich study used the **TTAL5 aluminum database**, not TCCU. Check the installed database's element, phase and assessed-interaction listings before screening Er compositions. (glavatskikh2024microstructureandphase pages 2-4, glavatskikh2024microstructureandphase pages 4-6)

## 6. Supply, cost, and safety

**[CITE] [NUMBERS]** Er belongs to the rare-earth commodities included in the **2022 U.S. critical-minerals list**; the **2025 final list** explicitly names **erbium** and adds **copper**. The latter is the final list, not merely a USGS draft economic recommendation. Er therefore adds a separate critical-mineral sourcing consideration rather than reducing the project's existing Cu dependence. (nassar2025methodologyandtechnical pages 33-35, staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 6-9)

**[GAP]** No reproducible quotation with date, purity, form, and lot size was verified, so an approximate **USD/kg price is not responsibly assignable** here. Er-specific occupational exposure limit, applicable RoHS/REACH restriction, Navy prohibition, or comparative toxicity threshold was also not verified; **“not verified” is not “unregulated” or “safe.”** For a proposed experiment, assess the actual powder and laser condensate by supplier SDS and institutional combustible-metal-dust, inhalation and fume controls. An Er-specific emission rate or powder-ignition threshold has not been established by the sources reviewed. (wang2026interpretablemachinelearning pages 1-4)

## 7. Bounds and decision

**EXCLUDE; family: neither.** **Conservative maximum = NA; non-conservative maximum = NA; functional floor = NA; impurity maximum = NA**, all expressed as unavailable *wt%* values rather than invented limits. No commercial/Navy Er range, Cu-rich corrosion benefit, DED or marine-filler validation, recovery value, measured Cu solubility limit, or assessed liquidus window can anchor the requested numerical bounds. The controlling decision failure is **absence of demonstrated as-deposited marine benefit coupled with unresolved inclusion, segregation and repair-interface risks**, not a proven toxic or cracking concentration. A separately labelled exploratory study could first measure powder/deposit Er recovery, phases, defects and seawater response against an Er-free composition; it would **not** turn an arbitrary trial content into a literature-derived bound. (riani2002ternaryrareearth pages 1-2, wang2026interpretablemachinelearning pages 1-4)

## 8. Interactions for subsequent joint constraints

**[GAP]** No validated Cu-rich Er–Ni, Er–Fe, Er–Mn, Er–Al, Er–Sn, or Er–Si **sum, ratio or neutralization rule** was found. Candidate interactions to *measure*, rather than constrain numerically, are Er with residual **O** (oxide/inclusion formation), Al and Fe introduced by NAB dilution, and Ni at a Cu–Ni repair interface. Er₂O₃ stability demonstrated in iron cannot be transposed into an Er/O stoichiometric cleanliness limit for molten Cu; nor does an Al-rich Al–Cu–Er particle establish the phase assemblage of NAB. (glavatskikh2024microstructureandphase pages 2-4, glavatskikh2024microstructureandphase pages 4-6, wang2026interpretablemachinelearning pages 1-4)

## 9. Evidence quality and principal citations

**Overall: thin for the specified application.** Binary Cu–Er phase identification and U.S. mineral-list status are substantially firmer than any assertion about Er-dependent Cu-alloy corrosion, DED or Navy specifications. The most tempting chloride result is from an **Al-balance**, partly heat-treated system, and the directly observed oxide result is from **iron**, not Cu. Confusing either matrix with copper, or interpreting “ER” welding-electrode prefixes as the chemical symbol Er, would manufacture apparent evidence. (glavatskikh2024microstructureandphase pages 2-4, riani2002ternaryrareearth pages 1-2, wang2026interpretablemachinelearning pages 1-4)

- **[CITE]** P. Riani, D. Mazzone, G. Zanicchi, R. Marazza and R. Ferro, “Ternary Rare Earth Germanium Systems with Cu and Ag—A Review and a Contribution to Their Assessment,” *Journal of Phase Equilibria* **23**, 7–28 (2002). DOI: **10.1361/105497102770332171**. Cu–Er binary-phase review; not a marine-corrosion experiment. (riani2002ternaryrareearth pages 1-2, riani2002ternaryrareearth pages 2-3)
- **[CITE] [NUMBERS]** M. V. Glavatskikh, R. Yu. Barkov, L. E. Gorlov, M. G. Khomutov and A. V. Pozdniakov, “Microstructure and Phase Composition of Novel Crossover Al-Zn-Mg-Cu-Zr-Y(Er) Alloys with Equal Zn/Mg/Cu Ratio and Cr Addition,” *Metals* **14**, 547 (2024). DOI: **10.3390/met14050547**. **Al-balance** composition and chloride study; not evidence of Cu-rich corrosion performance. (glavatskikh2024microstructureandphase pages 2-4, glavatskikh2024microstructureandphase media 2a2c0006, glavatskikh2024microstructureandphase pages 1-2)
- **[CITE]** J. Wang *et al.*, “Interpretable machine learning prediction of erbium-related thermodynamic parameters and experimental validation of Er₂O₃ phase stability in metallic melts,” *International Journal of Minerals, Metallurgy and Materials*, accepted manuscript (2026). DOI: **10.1007/s12613-026-3587-2**. Its experimental melt is **high-purity iron**. (wang2026interpretablemachinelearning pages 1-4, wang2026interpretablemachinelearning pages 4-7)
- **[CITE] [NAVY]** N. T. Nassar *et al.*, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, U.S. Geological Survey Open-File Report **2025–1047** (2025). DOI: **10.3133/ofr20251047**. This is the **methodology and draft-list recommendation**, not an Er-alloy qualification or the final-list legal text. (nassar2025methodologyandtechnical pages 4-9, nassar2025methodologyandtechnical pages 33-35)

VERDICT | Er | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (riani2002ternaryrareearth pages 1-2): P. Riani, D. Mazzone, G. Zanicchi, R. Marazza, and R. Ferro. Ternary rare earth germanium systems with cu and ag—a review and a contribution to their assessment. Journal of Phase Equilibria, 23:7-28, Feb 2002. URL: https://doi.org/10.1361/105497102770332171, doi:10.1361/105497102770332171. This article has 6 citations.

2. (riani2002ternaryrareearth pages 2-3): P. Riani, D. Mazzone, G. Zanicchi, R. Marazza, and R. Ferro. Ternary rare earth germanium systems with cu and ag—a review and a contribution to their assessment. Journal of Phase Equilibria, 23:7-28, Feb 2002. URL: https://doi.org/10.1361/105497102770332171, doi:10.1361/105497102770332171. This article has 6 citations.

3. (glavatskikh2024microstructureandphase pages 2-4): Maria V. Glavatskikh, Ruslan Yu. Barkov, Leonid E. Gorlov, Maxim G. Khomutov, and Andrey V. Pozdniakov. Microstructure and phase composition of novel crossover al-zn-mg-cu-zr-y(er) alloys with equal zn/mg/cu ratio and cr addition. Metals, 14(5):547, May 2024. URL: https://doi.org/10.3390/met14050547, doi:10.3390/met14050547. This article has 27 citations.

4. (glavatskikh2024microstructureandphase media 2a2c0006): Maria V. Glavatskikh, Ruslan Yu. Barkov, Leonid E. Gorlov, Maxim G. Khomutov, and Andrey V. Pozdniakov. Microstructure and phase composition of novel crossover al-zn-mg-cu-zr-y(er) alloys with equal zn/mg/cu ratio and cr addition. Metals, 14(5):547, May 2024. URL: https://doi.org/10.3390/met14050547, doi:10.3390/met14050547. This article has 27 citations.

5. (wang2026interpretablemachinelearning pages 1-4): J Wang, L Wang, J Li, and C Chen. Interpretable machine learning prediction of erbium-related thermodynamic parameters and experimental validation of er2o3 phase stability in metallic melts. Unknown journal, 2026. URL: https://doi.org/10.1007/s12613-026-3587-2, doi:10.1007/s12613-026-3587-2.

6. (wang2026interpretablemachinelearning pages 19-22): J Wang, L Wang, J Li, and C Chen. Interpretable machine learning prediction of erbium-related thermodynamic parameters and experimental validation of er2o3 phase stability in metallic melts. Unknown journal, 2026. URL: https://doi.org/10.1007/s12613-026-3587-2, doi:10.1007/s12613-026-3587-2.

7. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

8. (glavatskikh2024microstructureandphase pages 1-2): Maria V. Glavatskikh, Ruslan Yu. Barkov, Leonid E. Gorlov, Maxim G. Khomutov, and Andrey V. Pozdniakov. Microstructure and phase composition of novel crossover al-zn-mg-cu-zr-y(er) alloys with equal zn/mg/cu ratio and cr addition. Metals, 14(5):547, May 2024. URL: https://doi.org/10.3390/met14050547, doi:10.3390/met14050547. This article has 27 citations.

9. (wang2026interpretablemachinelearning pages 4-7): J Wang, L Wang, J Li, and C Chen. Interpretable machine learning prediction of erbium-related thermodynamic parameters and experimental validation of er2o3 phase stability in metallic melts. Unknown journal, 2026. URL: https://doi.org/10.1007/s12613-026-3587-2, doi:10.1007/s12613-026-3587-2.

10. (glavatskikh2024microstructureandphase pages 4-6): Maria V. Glavatskikh, Ruslan Yu. Barkov, Leonid E. Gorlov, Maxim G. Khomutov, and Andrey V. Pozdniakov. Microstructure and phase composition of novel crossover al-zn-mg-cu-zr-y(er) alloys with equal zn/mg/cu ratio and cr addition. Metals, 14(5):547, May 2024. URL: https://doi.org/10.3390/met14050547, doi:10.3390/met14050547. This article has 27 citations.

11. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

12. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

13. (nassar2025methodologyandtechnical pages 4-9): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
