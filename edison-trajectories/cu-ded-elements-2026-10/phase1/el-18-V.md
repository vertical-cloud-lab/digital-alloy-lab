<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 0910b75a-7128-4a5b-a40d-240bd4590ff2
- Submitted: 2026-10-17T18:59:44Z
- Fetched: 2026-10-17T19:30:43Z (status: success)
- Raw trajectory JSON: ../raw/el-18-V.json.gz
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

ELEMENT UNDER REVIEW: V (strengthening addition). Vanadium is rarely used in copper alloys; check for any use in aluminum bronzes, Cu-Ni, or grain refinement, and for its solubility in Cu.

Answer for V specifically, not for copper alloys in general:
1. ROLE: what V does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their V ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how V changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-V, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-V, Cu-Ni-V and Cu-Al-V are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of V in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that V neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | V | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: V (strengthening addition). Vanadium is rarely used in copper alloys; check for any use in aluminum bronzes, Cu-Ni, or grain refinement, and for its solubility in Cu.

Answer for V specifically, not for copper alloys in general:
1. ROLE: what V does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their V ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how V changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-V, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-V, Cu-Ni-V and Cu-Al-V are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of V in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that V neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | V | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Vanadium (V) in pre-alloyed marine-copper DED powder

**Decision: EXCLUDE V from the designed composition palette.** There is credible evidence that V can form strengthening particles in rapidly solidified *binary* Cu–V and historical evidence for grain refinement of *cast tin bronze*. Neither establishes an as-deposited seawater benefit, a workable Cu–Ni or nickel–aluminum-bronze (NAB) composition, or reliable processing in the specified atomizer. A reported high-V Cu–V liquidus of approximately 1,600 °C also exceeds the available melting temperature; it must not, however, be mistaken for the liquidus of a trace-V copper alloy. The proposed exclusion is an evidence-and-process decision, **not a demonstrated V toxicity threshold in the finished alloy**. [CITE] (cziegler2015aspectsofgrain pages 46-51, cziegler2015aspectsofgrain pages 102-106, bell1997solidsolubilityextension pages 3-3, verhoeven1989productiontechniquesfor pages 7-11, janssonUnknownyearphasetransformationsand pages 28-30)

## 1. Role and specifications

- **Demonstrated binary-Cu mechanism.** Bell and Davies found that retained V increases the resistivity of melt-spun Cu–V, whereas microhardness increases as resistivity falls within a given composition batch: they attribute the latter to V coming **out of solution as strengthening particles**. Their study does not identify a Cu–V intermetallic or establish strengthening *without* subsequent ageing in a DED deposit. A first-principles stacking-fault study instead predicts little change in Cu–V stacking-fault energies and no substantial mechanical-property effect from dilute dissolved V; this is a modelling result, not a DED measurement. [CITE][NUMBERS] A. Bell and H. A. Davies, *Materials Science and Engineering A* **226–228** (1997), 1039–1041, DOI: **10.1016/S0921-5093(96)10854-6**. (bell1997solidsolubilityextension pages 1-2, bell1997solidsolubilityextension pages 3-3, muzyk2019generalisedstackingfault pages 2-4)
- **Tin bronze/gunmetal and brass: limited casting precedent.** Cziegler's literature review names V among additions that can refine cast Cu–Sn, but supplies no isolated, transferable V-only marine-alloy performance window in the passages examined. A copper-grain-refiner patent lists V as *one option* for component C of a **four-component** Zr–Mg–C–P-type treatment for brass, tin/lead bronze and gunmetal: component C is specified at **0.003–0.10 wt%**, but the patent's preferred C element is **Fe**, not V. That claimed range is neither a commercial V specification nor proof that V alone works. [CITE][NUMBERS] A. Cziegler, *Aspects of Grain Refinement in Copper Alloys* (2015), §§2.3.2 and 7.5 (DOI not established in retrieved record); J. L. F. Kellie and A. J. J. Cowell, European patent **EP0240513B1**, *Grain Refining of Copper-Based Alloys* (1991; patents do not ordinarily carry DOIs). (cziegler2015aspectsofgrain pages 46-51, EP0240513B1 pages 1-2, EP0240513B1 pages 3-5)
- **No verified V-bearing commercial/Navy range.** In the material inspected, no deliberate V range could be substantiated for **C71500 Cu–Ni, C95800 cast NAB, Mn–Al bronze, standard aluminum-bronze weld metal, Cu–Ni–Sn or Cu–Ni–Si**. Accordingly, **no commercial or Navy alloy/specification containing a verified V addition can be listed**. As a check against confusing other alloying elements with V, a published nominal C95800 composition is Cu ≥79, Al 8.5–9.5, Ni 4–5, Fe 3.5–4.5 and Mn 0.8–1.5 **wt%**; it does not name V. This does *not* prove that every possible unspecified residual V is prohibited. [SPEC][NAVY][GAP][NUMBERS] C. Dharmendra *et al.*, *Additive Manufacturing* **30** (2019), 100872, DOI: **10.1016/j.addma.2019.100872**. The applicable documents to check directly before specifying procurement limits include **ASTM B148** (C95800), **ASTM B111/B171/B466**, **AWS A5.7**, **EN 12449** and the relevant **MIL-T-16420/MIL-B-24480/MIL-C-15726** editions; the sources retrieved here do not establish a V limit under any of them. (dharmendra2019microstructuralevolutionand pages 2-3)

## 2. Seawater corrosion

**[GAP] No attributable V-on/V-off quantitative comparison was found for copper alloys** in natural seawater, ASTM D1141 water or **3.5 wt% NaCl**. Thus there is no defensible V-beneficial or V-harmful *composition range* and no V-specific corrosion-rate, corrosion-potential, impedance/film-resistance, pitting, crevice, dealloying, erosion–corrosion or safe-flow-velocity number. Nor is V incorporation into a protective Cu–Ni or NAB film, or inhibition of selective attack, demonstrated. Do not transfer results on vanadium-containing **titanium, steel or V–Co–Ni alloys** to Cu-rich marine deposits. Relevant but explicitly **V-free** additive-manufactured NAB illustrates why processing must be controlled: changing arc heat input from **243.8 to 644.7 J/mm** increased reported corrosion-current density from **2.56 ± 0.04 to 7.52 ± 0.07 µA/cm²**; this is **not an effect of V** and not a direct comparison with wrought C71500. [CITE][NUMBERS][GAP] R. Huo *et al.*, *Materials* **18** (2025), 2205, DOI: **10.3390/ma18102205**. (huo2025modulatingheatinput pages 2-4)

## 3. DED, welding and repair dilution

**[GAP] No V-controlled blown-powder Cu–Ni/NAB DED or matching-filler weld series was established.** Consequently there is no measured V effect on solidification cracking, reheated-layer liquation cracking, porosity, laser evaporation/oxidation loss, or integrity after dilution into either cast C95800 or wrought Cu–Ni. The V-bearing refractory particles and oxygen-sensitive segregation described below make particle-rich boundaries, incomplete melting and oxide inclusions *plausible screening hazards*, **not reported DED defects**. Laser-induced V loss cannot be quantified from these sources; V's high melting point is not evidence that its *oxide* cannot enter fume. [GAP] V-free NAB welding/WAAM experience supplies the appropriate baseline, not an inferred V remedy: Dharmendra and colleagues explicitly identify **porosity and hot cracking** as NAB weldability problems and note the compositional sensitivity of seawater performance. Published WAAM builds and an ERCuNiAl-wire study demonstrate process sensitivity, but neither evaluates a V-bearing **ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl** filler. Dilution must therefore be tested separately on both substrates; no V–Al, V–Ni or V–Fe crack-free ratio can be prescribed. [CITE][NAVY][GAP] Dharmendra *et al.*, DOI: **10.1016/j.addma.2019.100872**; Huo *et al.*, DOI: **10.3390/ma18102205**. (dharmendra2019microstructuralevolutionand pages 2-3, huo2025modulatingheatinput pages 2-4)

## 4. Induction melting and atomization

**[NUMBERS] The high-V precedent is incompatible with the equipment:** a Cu–V superconducting-composite processing review describes V dendrites in a Cu matrix and estimates a Cu–V liquidus **around 1,600 °C**, explicitly calling it poorly established and **not assigning that number to a particular V wt%**. It cannot be used to claim that **0.10 wt% V** requires 1,600 °C, or to calculate the wt% at which this apparatus crosses **1,200–1,250 °C**. Melt-spun low-V Cu–V was instead prepared by first arc-melting the alloy and then induction-melting approximately **10 g** charges in silica under argon: feasibility at that scale does not validate a **0.5 kg**, approximately **1,300 °C** ultrasonic-atomization charge. [CITE][NUMBERS] J. D. Verhoeven and D. K. Finnemore, *Production Techniques for Discontinuous Filament A-15 Superconductor Wire*, OSTI report (1989), DOI: **10.2172/6616372**; Bell and Davies, DOI: **10.1016/S0921-5093(96)10854-6**. (verhoeven1989productiontechniquesfor pages 7-11, bell1997solidsolubilityextension pages 1-2)

**[NUMBERS] Refractory compatibility is a real concern, but the quantitative tests concern concentrated Cu–Nb/Cu–V composite processing at much higher temperatures.** The review reports oxygen pickup **>2,300 ppm by weight** with alumina, pyrolytic BN and **CaO-stabilized zirconia**, versus **<2,300 ppm by weight** with yttria, thoria and **yttria-stabilized zirconia**; graphite reduced oxygen pickup to **<500 ppm by weight** but increased carbon from **<100 to approximately 2,000 ppm by weight** in compared experiments. The review also records V-dendrite segregation in Cu–V cast into alumina. These figures are **not validated acceptance limits** for dilute-V powder, and zirconia performance depends on stabilizer and operating conditions. No verified Cu–V-specific measurement was obtained for sonotrode attack by **Ti alloy or Mo**, V oxidation loss during this particular atomization process, V-dependent liquid surface tension or resulting powder yield. Measure charge/powder/deposit V, O and C and inspect crucible and sonotrode inclusions if any exploratory melt is attempted. [CITE][NUMBERS][GAP] Verhoeven and Finnemore, DOI: **10.2172/6616372**. (verhoeven1989productiontechniquesfor pages 7-11, verhoeven1989productiontechniquesfor pages 11-15)

## 5. Phase diagram and CALPHAD

**[NUMBERS] Maximum reported *equilibrium* solubility of V in Cu: 0.17 atomic% at 1,085 °C, equivalent to approximately _0.136 wt% V_**, using atomic weights V 50.94 and Cu 63.55. Chill-block melt-spinning gave apparent nonequilibrium retention of **0.5 atomic% ≈0.40 wt%** by bulk resistivity or **1.0 atomic% ≈0.80 wt%** by surface-sensitive lattice-parameter measurement. These are **not equilibrium limits**, nor a validated DED solubility. V in excess of the retained amount produced strengthening particles. [CITE][NUMBERS] Bell and Davies, DOI: **10.1016/S0921-5093(96)10854-6**. (bell1997solidsolubilityextension pages 1-2, bell1997solidsolubilityextension pages 3-3)

**Phase topology remains disputed.** A ball-milling paper calls Cu–V immiscible in equilibrium liquid and solid, whereas Verhoeven and Finnemore describe an *accepted* Cu–V monotectic diagram but argue the observed monotectic might be **oxygen-induced**; they report V-rich dendrites under carefully controlled processing. These sources do **not** justify declaring an uncontested invariant-reaction temperature or a named equilibrium Cu–V intermetallic. Nor does the **<2,500 ppm by weight oxygen** figure cited for suppression of a Cu–Nb monotectic constitute a measured dilute-Cu–V oxygen limit. [CITE][NUMBERS][GAP] M. Baricco *et al.*, *Spectrochimica Acta A* **49** (1993), 1331–1344, DOI: **10.1016/0584-8539(93)80041-8**; Verhoeven and Finnemore, DOI: **10.2172/6616372**. Published binary thermodynamic assessments exist—M. Hämäläinen *et al.*, *CALPHAD* **14** (1990), 125–137, DOI: **10.1016/0364-5916(90)90014-Q**; M. A. Turchanin, *Powder Metallurgy and Metal Ceramics* **45** (2006), 272–278, DOI: **10.1007/s11106-006-0075-0**—but their full parameter sets and reconciliation with the processing evidence were not verified here. (baricco1993xrayabsorptionspectroscopy pages 1-3, verhoeven1989productiontechniquesfor pages 7-11)

**[GAP] TCCU is not a usable V-containing calculation merely because Thermo-Calc accepts a composition input.** The published **TCCU5/MOBCU5 32-element list does not include V**; it therefore cannot calculate Cu–V, Cu–Ni–V or Cu–Al–V within that database, or V-containing Scheil paths, surface tension or liquidus. No validated, mutually consistent **COST 531** or published ternary Cu–Ni–V/Cu–Al–V TDB was verified. A separate assessed binary Cu–V description would need explicit sourcing and validation before pycalphad extrapolation; ternary predictions would remain uncertain. [CITE][NUMBERS] Å. Jansson *et al.*, “Phase Transformations and Kinetic Simulations of Cu-Based Alloys,” *Copper Alloys 2022* conference proceedings, pp. 28–31 (conference paper; DOI not established in retrieved text). (janssonUnknownyearphasetransformationsand pages 28-30, janssonUnknownyearphasetransformationsand pages 30-32)

## 6. Supply, cost and occupational safety

**[NAVY][CITE] V is a US critical mineral** in the **2025 final list**; the reviewed USGS account also places Cu on that list. The 2025 designation should not be confused with an alloy-qualification decision; the 2022-versus-2025 legislative-list comparison was not verified directly from the Federal Register during this search. The relevant analytical source is N. T. Nassar *et al.*, USGS *Open-File Report 2025-1047*, DOI: **10.3133/ofr20251047**. **[GAP] A reproducible commodity quote in USD/kg of elemental V, dated and differentiated from V₂O₅ or ferrovanadium, was not recovered**; giving a price for one form as though it were induction-ready pure V would misstate this project's cost. (nassar2025methodologyandtechnical pages 1-4, staff2022usgsminingreview pages 6-9)

**[NUMBERS] Treat laser fume and airborne powder as hazards.** A secondary toxicology review reports OSHA figures of **0.5 mg/m³ for V₂O₅ respirable dust** and **0.1 mg/m³ for V₂O₅ fume**, but describes them as 8-hour limits; the *ceiling-versus-TWA designation must be checked against current 29 CFR 1910.1000 before using those values for compliance*. These are **airborne exposure figures, not permitted V wt% in copper**. Inhalation of pentavalent V compounds is associated with respiratory irritation; control powder dispersion, oxygen exposure and laser plume by enclosure, local extraction/filtration and occupational exposure assessment. Neither a V-specific **RoHS/REACH concentration ban on these marine copper alloys** nor a Navy V prohibition was substantiated in the retrieved evidence. [CITE][NUMBERS][GAP] J. Briffa *et al.*, *Heliyon* **6** (2020), e04691, DOI: **10.1016/j.heliyon.2020.e04691**; M. H. Fourie, *Retrospective Case-Control Study of Cancer Incidence Associated with Vanadium Pentoxide Exposure* (2009 thesis; DOI not established). (briffa2020heavymetalpollution pages 7-8, fourie2009retrospectivecasecontrolstudy pages 14-18, fourie2009retrospectivecasecontrolstudy pages 18-21)

## 7–9. Bounds, interactions and evidence quality

**[SPEC][GAP] Bounds decision — EXCLUDE.** For the requested *designed-addition* search space, set **V = 0 wt% nominal** in **both Cu–Ni and Al-bronze**. Conservative maximum, non-conservative maximum and functional floor are **NA**: the patent's **0.003–0.10 wt% optional component** is a multicomponent *casting* claim, not a marine-Cu–Ni/NAB performance bound; the **0.136 wt% equilibrium Cu solubility** is not a marine-alloy qualification; and the Cu + **0.10 wt% V** casting comparison was only **640 µm** versus **650 µm** for unalloyed Cu—approximately **1.5%** smaller, without evidence that the difference is significant. Neither result supplies a demonstrated functional floor for this project. [CITE][NUMBERS] Cziegler (2015), Appendix Table 7-2, reporting Bustos's experiments; Bell and Davies, DOI: **10.1016/S0921-5093(96)10854-6**; EP0240513B1. (cziegler2015aspectsofgrain pages 102-106, bell1997solidsolubilityextension pages 3-3, EP0240513B1 pages 3-5)

**Incidental impurity:** no verified marine-alloy specification or V-controlled corrosion/DED study sets a maximum tolerable **V wt% or ppm** in both powder and deposit; hence **impurity_max_wt = NA**, *not* an invented 0.10 wt% specification. If an internal analytical reporting threshold is adopted for purchases, label it a provisional process-control rule rather than a literature-established tolerable limit. The decision-setting failure modes are **unvalidated as-deposited corrosion and repair cracking**, together with possible oxygen-bearing particles, limited equilibrium V solubility and, at sufficiently high but **unquantified** V content, loss of melt superheat. [GAP] (cziegler2015aspectsofgrain pages 102-106, bell1997solidsolubilityextension pages 3-3, verhoeven1989productiontechniquesfor pages 7-11, dharmendra2019microstructuralevolutionand pages 2-3)

**Interactions to record if V appears in feedstock:** distinguish dissolved V from V-rich particles and oxide; measure V–O–C alongside Al, Ni, Fe and Mn, because oxygen/refractory contamination and segregation can change the apparent effect. The patented grain-refiner claim requires V, *if selected*, to coexist with a Zr/Ti component, Mg-family component and a fourth component such as P; it supplies **no validated V:Ni, V:Fe, V:Mn or V:Al ratio**, and no evidence that V substitutes for Ni's seawater function or neutralizes NAB selective attack. The seemingly conflicting reports of equilibrium liquid immiscibility versus an oxygen-induced monotectic, and the divergent rapidly quenched solubility measurements, further limit transfer to a repeatedly reheated DED build. Overall V-specific evidence for the proposal is **thin**. [CITE][GAP] EP0240513B1; Baricco *et al.*, DOI: **10.1016/0584-8539(93)80041-8**; Verhoeven and Finnemore, DOI: **10.2172/6616372**; Bell and Davies, DOI: **10.1016/S0921-5093(96)10854-6**. (EP0240513B1 pages 1-2, baricco1993xrayabsorptionspectroscopy pages 1-3, verhoeven1989productiontechniquesfor pages 7-11, bell1997solidsolubilityextension pages 3-3)

VERDICT | V | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (cziegler2015aspectsofgrain pages 46-51): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

2. (cziegler2015aspectsofgrain pages 102-106): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

3. (bell1997solidsolubilityextension pages 3-3): A. Bell and H.A. Davies. Solid solubility extension in cu-v and cu-cr alloys produced by chill block melt-spinning. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, pages 1039-1041, Jun 1997. URL: https://doi.org/10.1016/s0921-5093(96)10854-6, doi:10.1016/s0921-5093(96)10854-6. This article has 30 citations.

4. (verhoeven1989productiontechniquesfor pages 7-11): JD Verhoeven and DK Finnemore. Production techniques for discontinuous filament a-15 superconductor wire. ArXiv, Apr 1989. URL: https://doi.org/10.2172/6616372, doi:10.2172/6616372. This article has 1 citations.

5. (janssonUnknownyearphasetransformationsand pages 28-30): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

6. (bell1997solidsolubilityextension pages 1-2): A. Bell and H.A. Davies. Solid solubility extension in cu-v and cu-cr alloys produced by chill block melt-spinning. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, pages 1039-1041, Jun 1997. URL: https://doi.org/10.1016/s0921-5093(96)10854-6, doi:10.1016/s0921-5093(96)10854-6. This article has 30 citations.

7. (muzyk2019generalisedstackingfault pages 2-4): M Muzyk. Generalised stacking fault energies of copper alloys-density functional theory calculations. Unknown journal, 2019.

8. (EP0240513B1 pages 1-2): James Leslie Frederick Kellie. Grain refining of copper-based alloys. Patent (WO,EP,US,JP,AU,BR,GB,ZA), 1991.

9. (EP0240513B1 pages 3-5): James Leslie Frederick Kellie. Grain refining of copper-based alloys. Patent (WO,EP,US,JP,AU,BR,GB,ZA), 1991.

10. (dharmendra2019microstructuralevolutionand pages 2-3): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 188 citations and is from a highest quality peer-reviewed journal.

11. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

12. (verhoeven1989productiontechniquesfor pages 11-15): JD Verhoeven and DK Finnemore. Production techniques for discontinuous filament a-15 superconductor wire. ArXiv, Apr 1989. URL: https://doi.org/10.2172/6616372, doi:10.2172/6616372. This article has 1 citations.

13. (baricco1993xrayabsorptionspectroscopy pages 1-3): M. Baricco, L. Battezzati, S. Enzo, I. Soletta, and G. Cocco. X-ray absorption spectroscopy and diffraction study of miscible and immiscible binary metallic systems prepared by ball milling. Spectrochimica Acta Part A: Molecular and Biomolecular Spectroscopy, 49:1331-1344, Aug 1993. URL: https://doi.org/10.1016/0584-8539(93)80041-8, doi:10.1016/0584-8539(93)80041-8. This article has 21 citations and is from a peer-reviewed journal.

14. (janssonUnknownyearphasetransformationsand pages 30-32): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

15. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

16. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

17. (briffa2020heavymetalpollution pages 7-8): Jessica Briffa, Emmanuel Sinagra, and Renald Blundell. Heavy metal pollution in the environment and their toxicological effects on humans. Heliyon, 6:e04691, Sep 2020. URL: https://doi.org/10.1016/j.heliyon.2020.e04691, doi:10.1016/j.heliyon.2020.e04691. This article has 5481 citations.

18. (fourie2009retrospectivecasecontrolstudy pages 14-18): MH Fourie. Retrospective case-control study of cancer incidence associated with vanadium pentoxide exposure in the mineral processing industry. Unknown journal, 2009.

19. (fourie2009retrospectivecasecontrolstudy pages 18-21): MH Fourie. Retrospective case-control study of cancer incidence associated with vanadium pentoxide exposure in the mineral processing industry. Unknown journal, 2009.
