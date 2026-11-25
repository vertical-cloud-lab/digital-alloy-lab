<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 92ee0861-d702-4058-bb4c-d3cd18188ca1
- Submitted: 2026-10-17T18:58:55Z
- Fetched: 2026-10-17T19:30:33Z (status: success)
- Raw trajectory JSON: ../raw/el-10-Nb.json.gz
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

ELEMENT UNDER REVIEW: Nb (major seawater addition). Cast Cu-Ni: C96200 (90-10) and C96400 (70-30) contain Nb (up to about 1-1.5 wt%), added for weldability; Cu-Cr-Nb (GRCop, Cr2Nb). Nb is nearly insoluble in Cu and is a US critical mineral.

Answer for Nb specifically, not for copper alloys in general:
1. ROLE: what Nb does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Nb ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Nb changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Nb, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Nb, Cu-Ni-Nb and Cu-Al-Nb are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Nb in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Nb neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Nb | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Nb (major seawater addition). Cast Cu-Ni: C96200 (90-10) and C96400 (70-30) contain Nb (up to about 1-1.5 wt%), added for weldability; Cu-Cr-Nb (GRCop, Cr2Nb). Nb is nearly insoluble in Cu and is a US critical mineral.

Answer for Nb specifically, not for copper alloys in general:
1. ROLE: what Nb does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Nb ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Nb changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Nb, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Nb, Cu-Ni-Nb and Cu-Al-Nb are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Nb in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Nb neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Nb | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Niobium (Nb) for as-deposited marine copper-alloy DED

**Decision: INCLUDE Nb in the Cu–Ni experimental palette, conditionally—not as an established seawater-corrosion addition.** The strongest applicable evidence is that Nb, paired with Si, improves weldability and strength of *cast* Cu–Ni. It does **not** establish that Nb improves seawater corrosion, that the effect survives single-stream laser DED, or that a Nb-bearing deposit will equal wrought C71500 without heat treatment. Keep an Nb-free control at every Ni–Si–Fe composition, and make the seawater and repair-interface tests decisive gates. No independently verified Nb-based design rule was found for conventional nickel-aluminum bronze (NAB). [CITE] (konynenburg1990backgroundstudiesin pages 149-155, klassert2007copperandcopper–nickel pages 6-9, klassert2007copperandcopper–nickel pages 4-6)

## 1. Function, alloy identities, and specifications

**Cast Cu–Ni.** Nb increases tensile and proof strength but can reduce elongation; its reported weldability benefit is reduced heat-affected-zone (HAZ) cracking. In Si-bearing 70–30 cast Cu–Ni, a metallurgical review attributes strengthening to *Ni–Nb–Si precipitates*, formed even during slow casting cooling, with increased strength at the expense of ductility. The review describes about **0.4 wt% Si with Nb normally at least twice the Si content** for strengthened 70–30 castings, and approximately **0.10–0.15 wt% Si plus 0.50–0.70 wt% Nb** as preferred additions to strengthened 90–10 castings. These are *reported practices*, not verified UNS limits or proof of seawater benefit. Nb is therefore chiefly a precipitation/solidification-control addition here, not a demonstrated Cu-matrix solid-solution or protective-film former. [CITE] [NUMBERS] (konynenburg1990backgroundstudiesin pages 149-155, klassert2007copperandcopper–nickel pages 4-6)

**Verified identities versus unverified composition limits:**

| Alloy or document | What can actually be established about Nb, in wt% |
|---|---|
| UNS **C96200**, cast 90–10 Cu–Ni; **C96400**, cast 70–30 Cu–Ni | Both designations occur in a historical composition table, but that table **has no Nb column**. The literature's Nb-containing cast 90–10 and 70–30 formulations cannot safely be presented as the *specified Nb ranges* of C96200 or C96400. Their exact Nb limits in the applicable edition of **ASTM B369/UNS** remain **unverified**. [SPEC] [GAP] (konynenburg1990backgroundstudiesin pages 228-233, konynenburg1990backgroundstudiesin pages 149-155) |
| **EN CC383H**, CuNi30Fe1Mn1NbSi-C | Identified expressly as an Nb–Si-containing marine casting grade; the examined source supplies **no numeric Nb interval**. Verify the controlling edition of **EN 1982** before claiming a specification bound. [SPEC] [GAP] (klassert2007copperandcopper–nickel pages 4-6) |
| Marine-fastener **Cu–Ni–Mn–Al–Cr–Nb**, US patent **5,164,157** | Claimed **0.50–1.00 wt% Nb**; a worked alloy contains **0.72 wt% Nb**. It is hot-worked and, for reported peak properties, aged: neither a commercial UNS specification nor evidence of as-deposited DED performance. [NUMBERS] (US5164157A pages 1-3, US5164157A pages 3-4, US5164157A pages 5-6) |
| NASA **GRCop-84**, Cu–Cr–Nb | AM study's target **5.4–6.0 wt% Nb** and **6.2–6.8 wt% Cr**; measured as-built **5.78 wt% Nb**, **6.47 wt% Cr**. This is an aerospace heat-transfer alloy, **not** a seawater or low-temperature induction-atomization precedent. [NUMBERS] (minneci2024characterizationandrationalization pages 2-4, minneci2024characterizationandrationalization media 4c71b3e0) |
| **GRCop-42** | Nominally Cu–4 at% Cr–2 at% Nb in its *source*; converted to the requested mass basis, approximately **2.84 wt% Nb and 3.18 wt% Cr**, Cu balance. These are calculated nominal values, **not** a verified measured powder specification. [NUMBERS] (mastny2026highstrengthcopperalloys pages 14-17) |

No verified specification or Nb interval emerged for Nb as a deliberate addition to **C95800 NAB**, Mn–Al bronze, tin bronze/gunmetal, ordinary marine brasses, Cu–Ni–Sn, or Cu–Ni–Si. Likewise, no Nb requirement was established for wrought **C71500** or the examined Cu–Ni weld-filler practice; do not label these alloys Nb-bearing merely because a cast Cu–Ni relative uses Nb. A study adding **3 wt% NbC** by milling aluminum-bronze chips concerns an *externally added ceramic*, not **3 wt% dissolved or pre-alloyed elemental Nb**, and supplies no seawater qualification. [SPEC] [GAP] (konynenburg1990backgroundstudiesin pages 136-142, klassert2007copperandcopper–nickel pages 4-6, konynenburg1990backgroundstudiesin pages 228-233)

## 2. Seawater corrosion: what is—and is not—quantified

**No controlled Nb-versus-zero-Nb seawater result was verified** for conventional Cu–Ni or aluminum bronze. Specifically, there is no defensible Nb-dependent interval of corrosion rates, *E*₍corr₎, polarization resistance, impedance/film resistance, pitting or crevice potential, 30-day selective-attack depth, dealloying inhibition, or flow-velocity limit. Thus the range over which Nb **helps or harms corrosion is unknown**; neither a beneficial floor nor a harmful threshold can be reported as a measured seawater result. Claims that Nb forms the protective marine film or inhibits NAB dealloying are hypotheses, not findings. [GAP] (konynenburg1990backgroundstudiesin pages 149-155, klassert2007copperandcopper–nickel pages 6-9)

A useful but **non-isolating** quantitative lead is Clark and Guha's US patent **5,164,157**: its Table 6 reports seawater-*cavitation erosion*, printed as **0 mm/h** for wrought invention Alloy E, **0.8 mm/h** for wrought Alloy D, **2.3 mm/h** for cast Alloy D, and **19 mm/h** for wrought 70–30 Cu–Ni. Alloy E contains **0.72 wt% Nb**, but differs from the comparators in other alloying constituents and processing; the patent omits sufficient cavitation-test detail to interpret the reported zero or attribute differences to Nb. Its separate **70-day seawater** experiment measures tensile behavior following hydrogen exposure, *not* the Table 6 cavitation duration and *not* general corrosion. Neither is evidence of the requested as-deposited C71500 equivalence. [CITE] [NUMBERS] (US5164157A pages 4-5, US5164157A pages 5-6, US5164157A pages 6-7)

For context **only**, an overview calls approximately **6 m/s** an *indicative general Cu–Ni* upper seawater velocity and attributes protective-film adhesion/erosion resistance mainly to **Fe**; it attributes improved resistance in rapidly flowing seawater separately to **Cr**. Neither is an Nb-specific velocity limit. A claim of Nb benefit based on these numbers would conflate elements. [NUMBERS] (klassert2007copperandcopper–nickel pages 6-9, klassert2007copperandcopper–nickel pages 4-6)

## 3. DED, welding, and repair interfaces

[CITE] **Relevant evidence is predominantly casting and welding, not Nb-controlled marine DED.** For Si-bearing cast Cu–Ni, the independently reported weldability condition is **Nb > 1.55 Si − 0.10**, with concentrations in **wt%**; it is a *welding heuristic*, not a guarantee of crack-free layer remelting. At **0.40 wt% Si**, its algebraic threshold is **>0.52 wt% Nb**. The separate historical practice of Nb at least twice Si is more conservative (**≥0.80 wt% Nb** at **0.40 wt% Si**). For Cu–Ni welds, the overview also limits crack-promoting residuals to approximately **0.02 wt% each P and S, 0.50 wt% Zn, 0.02 wt% Pb, and 0.05 wt% C**; these are not permissible Nb levels. [CITE] [NUMBERS] (konynenburg1990backgroundstudiesin pages 149-155, klassert2007copperandcopper–nickel pages 6-9)

The historical 70–30 Cu–Ni filler used on both cast 90–10 and 70–30 and the overview's welding-agent descriptions do **not** demonstrate that **ERCuNi** contains useful Nb. Similarly, no verified Nb-containing range or Nb-versus-control HAZ/liquation-cracking comparison was found for **ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl** under **AWS A5.7**. Their use on NAB is a *joining analogy*, not evidence that Nb heals NAB cracks. Nb-rich particles and oxides, low wetting, and remelting of segregated interdendritic material are plausible **DED risks**, but their effects on first-pass solidification cracking, reheated-layer liquation cracking, pore fraction, and dilution into **C95800** or **C71500** have **not been measured here**. Ni and Si introduced by Cu–Ni substrate dilution could alter Nb–Si precipitation; Al and Fe introduced by NAB could alter interfacial phases. Treat both as testable predictions, not demonstrated benefits. [SPEC] [GAP] (konynenburg1990backgroundstudiesin pages 149-155, klassert2007copperandcopper–nickel pages 6-9, konynenburg1990backgroundstudiesin pages 136-142, minneci2024characterizationandrationalization pages 6-9)

NASA's infrared-laser **LPBF** GRCop-84 provides a useful *counterexample to assuming Nb prevents porosity*: as-built micrographs show circular pores and lack-of-fusion lines even though Cr₂Nb forms and particles become finer in the build. It is **LPBF, not blown-powder DED**, and reports no Nb-isolated crack-resistance comparison. The study calculates a much lower elemental Nb vapor pressure than Cr at laser-melt temperatures, so **preferential Nb evaporation is not supported**; Nb retention must still be checked experimentally in the proposed process. [CITE] [NUMBERS] (minneci2024characterizationandrationalization pages 4-6, minneci2024characterizationandrationalization pages 6-9)

## 4. In-house melting and atomization

The binary Cu–Nb evidence makes charging **pure Nb metal into a roughly 1,300 °C induction furnace** distinctly different from remelting pre-atomized GRCop powder by laser. At **1,090 °C**, liquid Cu on Nb has a mean contact angle of about **67°**; under argon the reported angles are **69° at 1,090 °C** and **42° at 1,200 °C**. Oxygen-doped Nb is more difficult to wet, whereas higher temperatures improve wetting. Undissolved Nb, Nb-rich particles and melt-to-melt variability are therefore credible concerns at limited superheat. Nb is oxygen-reactive: a Cu/Nb/alumina joining study finds that Nb changes Cu's contact angle on alumina, with oxygen-dependent mechanisms unresolved. It does **not** establish a quantified attack rate on an **alumina or zirconia crucible**, graphite crucible, titanium-alloy or molybdenum sonotrode. Those compatibility questions, powder oxygen pickup, inclusion counts, and nozzle fouling need experiments; no validated Nb-specific ultrasonic-atomization surface-tension or vapor-loss coefficient was found. [CITE] [NUMBERS] [GAP] (lima1985wettingcharacteristicsof pages 1-3, marks1999effectsofprocessing pages 46-49, lima1985wettingcharacteristicsof pages 3-4)

GRCop-84's as-built powder/LPBF study reports Cr₂Nb precipitating before the Cu matrix; calculated dissolution of Cr₂Nb in liquid requires roughly **1,900 K (~1,627 °C)**, well beyond the available induction-module temperature. This is a warning against choosing **~5.8 wt% Nb with ~6.5 wt% Cr** as the in-house atomization target, **not** proof that every dilute Nb-bearing Cu–Ni liquidus exceeds **1,250 °C**. In laser conditions the paper estimates vapor pressures at **2,100 K** of **Cu 1,090 Pa, Cr 328 Pa, Nb 9.20 × 10⁻⁶ Pa**: measure Cr/Nb ratio before and after DED rather than assuming Nb itself is volatilizing. [CITE] [NUMBERS] (minneci2024characterizationandrationalization pages 2-4, minneci2024characterizationandrationalization pages 6-9)

## 5. Phase diagrams and CALPHAD

The examined Cu–Nb phase-diagram account reports **no binary Cu–Nb intermetallic**, a **peritectic near 1,090 °C**, **<0.2 wt% Nb in Cu at 20 °C**, and a literature value of approximately **1.6 wt% Nb in Cu near 1,090 °C**; it explicitly cautions that published phase-diagram and solubility values vary. Crucially, do **not** treat **1.6 wt%** as a measured room-temperature solid-solubility ceiling, a verified solubility in *every* Cu–Ni/Al melt, or an atomizer-safe liquidus cutoff. Mechanical alloying can force about **10 wt% Nb** into metastable Cu-rich powder, with **11.6 wt%** estimated after extended milling, but those non-equilibrium results are inapplicable as equilibrium liquidus bounds. Binary **Cr₂Nb** in GRCop and proposed **Ni–Nb–Si** cast-Cu–Ni precipitates must not be mislabeled Cu–Nb intermetallics. [CITE] [NUMBERS] (lei2011structureevolutionand pages 4-6, lima1985wettingcharacteristicsof pages 1-3, minneci2024characterizationandrationalization pages 1-2)

A peer-reviewed GRCop study *did* run **Thermo-Calc with a Copper database** to model Cu–Cr–Nb Cr₂Nb dissolution and solidification. This establishes feasibility for **that system and database instance**, **not** coverage, validated parameterizations, or predictive accuracy for **Cu–Nb, Cu–Ni–Nb, or Cu–Al–Nb** in the laboratory's particular **TCCU** release. No inspected source independently verified those three assessed descriptions in **TCCU**, **COST 531**, or a distributable published **TDB**. Verify constituent/phase availability and binary/ternary assessment citations in the installed database, then calculate equilibrium *and Scheil* liquidus/solidus/last-liquid fractions at actual powder and substrate-diluted compositions. **No justified numerical Nb concentration at which this equipment's liquidus crosses 1,250 °C is available.** [CITE] [GAP] (minneci2024characterizationandrationalization pages 2-4, minneci2024characterizationandrationalization pages 6-9)

## 6. Supply, safety, bounds, and interactions

**Supply and regulation.** A USGS review explicitly lists **Nb and Cu** among the **final 2025 U.S. critical minerals**; the cited primary 2025 methodology also identifies a substantial Nb supply-disruption concern. The searched material did not substantiate a **2022-list entry**, a defensible **current USD/kg quotation** for the *specific purchasing form and purity* (Nb metal versus ferroniobium), an Nb-specific **OSHA PEL**, or an alloy-level **RoHS/REACH or Navy prohibition**: do not invent those numbers or claim approval from silence. Ferroniobium is an unsuitable automatic substitution for high-purity Nb where its Fe addition would change the experiment. Apply the applicable metal-powder combustible-dust, inhalation/ventilation, laser-fume, and powder-waste procedures, and obtain the actual supplier SDS and installation safety review; absence of a verified Nb-specific limit is not evidence of no hazard. [NAVY] [GAP] (nassar2025methodologyandtechnical pages 1-4, iii2026usgscriticalminerals pages 1-2, nassar2025methodologyandtechnical pages 24-25)

**Proposed palette bounds—experimental decisions, not specification or seawater-qualified limits:**

| Family | Functional floor | Conservative maximum | Non-conservative maximum | Bounding failure mode |
|---|---:|---:|---:|---|
| **Cu–Ni with deliberately controlled Si** | **0.50 wt% Nb**, conditional on a comparable Si-containing casting chemistry | **0.80 wt% Nb** | **1.00 wt% Nb** | Below the floor, reported cast-90–10 practice and Nb–Si welding balance may be ineffective; above the conservative value, evidence for the proposed atomizer, ductility and crack-free as-deposited repair becomes weak. The **1.00 wt%** ceiling is a *patented multi-element marine-alloy claim*, not a demonstrated safe DED or seawater threshold. [CITE] [NUMBERS] (konynenburg1990backgroundstudiesin pages 149-155, US5164157A pages 3-4, klassert2007copperandcopper–nickel pages 6-9) |
| **NAB/Al-bronze as an independent design family** | **NA** | **NA** | **NA** | No verified Nb-specific marine benefit or numeric Nb design interval. A Cu–Ni powder trial on NAB is an **interface experiment**, not validation of an Nb-bearing NAB powder. [GAP] (konynenburg1990backgroundstudiesin pages 136-142, klassert2007copperandcopper–nickel pages 4-6) |

For Cu–Ni without the requisite Si, even the **0.50 wt% functional floor is unproven**. The **0.80 wt%** ceiling is selected from the reported **≥2×Si** practice at **0.40 wt% Si**, *not* falsely attributed to ASTM B369, a Navy specification, or C96400. Do not use **1.6 wt%** from a binary near-peritectic phase account or the much larger GRCop Nb loadings as permission to exceed this aggressive **1.00 wt%** trial ceiling. Nb as an impurity in Nb-free comparator powders should be measured and reported, but **no evidence-derived maximum tolerable ppm or wt%** was established; the LIMIT-only `impurity_max` field is consequently **NA**. [NUMBERS] [SPEC] [GAP] (konynenburg1990backgroundstudiesin pages 149-155, lima1985wettingcharacteristicsof pages 1-3, minneci2024characterizationandrationalization pages 1-2, konynenburg1990backgroundstudiesin pages 228-233)

**Joint constraints to carry forward.** For cast Cu–Ni, record **Nb − 1.55Si + 0.10 > 0** and separately evaluate the more conservative **Nb/Si ≥ 2** historical practice, all in **wt%**; these are *not interchangeable* criteria. Track **Ni–Nb–Si precipitates** and loss of ductility as Si/Ni/Nb vary. Track **Fe** separately for marine-film/impingement behavior, **Cr:Nb** for Cr₂Nb versus free Nb in Cu–Cr–Nb, and **Al, Ni, Mn, Cr and Nb jointly** when evaluating the patented marine fastener alloy: it specifies **Cu/(Mn+Ni) between 3 and 4.9**, **Al+Nb ≥ 2.1 wt%** and **Ni/(Al+Nb) ≥ 6**, although OCR renders the plus signs imperfectly. Those patented ratios belong to an aged multi-element alloy and are *not* transferred as DED rules. Track O, Si and trace P/S/Pb at both substrate interfaces; Nb's possible oxygen gettering can mean undesirable Nb oxides rather than a beneficial marine film. [CITE] [NUMBERS] [GAP] (konynenburg1990backgroundstudiesin pages 149-155, US5164157A pages 3-4, klassert2007copperandcopper–nickel pages 6-9, klassert2007copperandcopper–nickel pages 4-6, minneci2024characterizationandrationalization pages 1-2, marks1999effectsofprocessing pages 46-49)

**Evidence quality:** moderate for the narrow claim *Nb–Si-assisted cast-Cu–Ni weldability*; **thin** for the actual decision criterion—Nb's incremental effect on *as-deposited*, crack-free, C71500-competitive seawater performance and NAB/Cu–Ni repairs. The patent's aged, hot-worked cavitation result, cast-alloy welding guidance and NASA's aerospace LPBF phases cannot close that gap. [GAP] (konynenburg1990backgroundstudiesin pages 149-155, minneci2024characterizationandrationalization pages 2-4, US5164157A pages 5-6, US5164157A pages 6-7)

**Full-source identifiers:** Van Konynenburg *et al.*, *Background Studies in Support of a Feasibility Assessment on the Use of Copper-Base Materials for Nuclear Waste Packages* (DOE report, 1990), **doi:10.2172/137782**; Klassert and Tikana, *Copper and Copper–Nickel Alloys—An Overview* (2007; DOI not verified); de Lima *et al.*, *J. Mater. Sci.* **20**, 2464–2470 (1985), **doi:10.1007/BF00556075**; Lei *et al.*, *Mater. Sci. Eng. A* **528**, 4475–4481 (2011), **doi:10.1016/j.msea.2011.02.083**; Minneci *et al.*, *Metall. Mater. Trans. A* **55**, 1377–1396 (2024), **doi:10.1007/s11661-024-07315-w**; Marks, *Effects of Processing Conditions and Ambient Environment on Copper/Niobium/Copper Interlayer Joints for Alumina* (1999), **doi:10.2172/843055**; Nassar *et al.*, USGS Open-File Report **2025–1047**, **doi:10.3133/ofr20251047**; Clark and Guha, **US patent 5,164,157** (1992; no DOI). **ASTM B369, AWS A5.7, EN 1982 and the applicable UNS chemistry tables must be checked in their controlling editions before any Nb value is labeled [SPEC].** (konynenburg1990backgroundstudiesin pages 149-155, klassert2007copperandcopper–nickel pages 6-9, nassar2025methodologyandtechnical pages 1-4, lima1985wettingcharacteristicsof pages 1-3, minneci2024characterizationandrationalization pages 6-9, konynenburg1990backgroundstudiesin pages 228-233, marks1999effectsofprocessing pages 46-49)

VERDICT | Nb | decision=INCLUDE | family=Cu-Ni | conservative_max_wt=0.80 | nonconservative_max_wt=1.00 | floor_wt=0.50 | impurity_max_wt=NA | evidence=thin

References

1. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

2. (klassert2007copperandcopper–nickel pages 6-9): A Klassert and L Tikana. Copper and copper–nickel alloys–an overview. Unknown journal, 2007.

3. (klassert2007copperandcopper–nickel pages 4-6): A Klassert and L Tikana. Copper and copper–nickel alloys–an overview. Unknown journal, 2007.

4. (konynenburg1990backgroundstudiesin pages 228-233): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

5. (US5164157A pages 1-3): Charles A. Clark. Copper based alloy. Patent (WO,EP,US,JP,AU,CA,GB), 1992.

6. (US5164157A pages 3-4): Charles A. Clark. Copper based alloy. Patent (WO,EP,US,JP,AU,CA,GB), 1992.

7. (US5164157A pages 5-6): Charles A. Clark. Copper based alloy. Patent (WO,EP,US,JP,AU,CA,GB), 1992.

8. (minneci2024characterizationandrationalization pages 2-4): Robert P. Minneci, Michael P. Haines, Paul R. Gradl, David L. Ellis, Eric A. Lass, Jeffrey R. Bunn, Hahn Choo, Zachary C. Jones, Sudarsanam S. Babu, and Claudia J. Rawn. Characterization and rationalization of microstructural evolution in grcop-84 processed by laser-powder bed fusion (l-pbf). Metallurgical and Materials Transactions A, 55:1377-1396, Feb 2024. URL: https://doi.org/10.1007/s11661-024-07315-w, doi:10.1007/s11661-024-07315-w. This article has 4 citations.

9. (minneci2024characterizationandrationalization media 4c71b3e0): Robert P. Minneci, Michael P. Haines, Paul R. Gradl, David L. Ellis, Eric A. Lass, Jeffrey R. Bunn, Hahn Choo, Zachary C. Jones, Sudarsanam S. Babu, and Claudia J. Rawn. Characterization and rationalization of microstructural evolution in grcop-84 processed by laser-powder bed fusion (l-pbf). Metallurgical and Materials Transactions A, 55:1377-1396, Feb 2024. URL: https://doi.org/10.1007/s11661-024-07315-w, doi:10.1007/s11661-024-07315-w. This article has 4 citations.

10. (mastny2026highstrengthcopperalloys pages 14-17): P Mastny. High-strength copper alloys for indirect additive manufacturing using photolithography. Unknown journal, 2026.

11. (konynenburg1990backgroundstudiesin pages 136-142): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

12. (US5164157A pages 4-5): Charles A. Clark. Copper based alloy. Patent (WO,EP,US,JP,AU,CA,GB), 1992.

13. (US5164157A pages 6-7): Charles A. Clark. Copper based alloy. Patent (WO,EP,US,JP,AU,CA,GB), 1992.

14. (minneci2024characterizationandrationalization pages 6-9): Robert P. Minneci, Michael P. Haines, Paul R. Gradl, David L. Ellis, Eric A. Lass, Jeffrey R. Bunn, Hahn Choo, Zachary C. Jones, Sudarsanam S. Babu, and Claudia J. Rawn. Characterization and rationalization of microstructural evolution in grcop-84 processed by laser-powder bed fusion (l-pbf). Metallurgical and Materials Transactions A, 55:1377-1396, Feb 2024. URL: https://doi.org/10.1007/s11661-024-07315-w, doi:10.1007/s11661-024-07315-w. This article has 4 citations.

15. (minneci2024characterizationandrationalization pages 4-6): Robert P. Minneci, Michael P. Haines, Paul R. Gradl, David L. Ellis, Eric A. Lass, Jeffrey R. Bunn, Hahn Choo, Zachary C. Jones, Sudarsanam S. Babu, and Claudia J. Rawn. Characterization and rationalization of microstructural evolution in grcop-84 processed by laser-powder bed fusion (l-pbf). Metallurgical and Materials Transactions A, 55:1377-1396, Feb 2024. URL: https://doi.org/10.1007/s11661-024-07315-w, doi:10.1007/s11661-024-07315-w. This article has 4 citations.

16. (lima1985wettingcharacteristicsof pages 1-3): O. F. De Lima, M. Krehl, and K. Schulze. Wetting characteristics of copper on niobium. Journal of Materials Science, 20:2464-2470, Jul 1985. URL: https://doi.org/10.1007/bf00556075, doi:10.1007/bf00556075. This article has 14 citations and is from a peer-reviewed journal.

17. (marks1999effectsofprocessing pages 46-49): Robert Alan Marks. Effects of processing conditions and ambient environment on the microstructure and fracture strength of copper/niobium/copper interlayer joints for alumina. Lawrence Berkeley National Laboratory, Dec 1999. URL: https://doi.org/10.2172/843055, doi:10.2172/843055. This article has 1 citations.

18. (lima1985wettingcharacteristicsof pages 3-4): O. F. De Lima, M. Krehl, and K. Schulze. Wetting characteristics of copper on niobium. Journal of Materials Science, 20:2464-2470, Jul 1985. URL: https://doi.org/10.1007/bf00556075, doi:10.1007/bf00556075. This article has 14 citations and is from a peer-reviewed journal.

19. (lei2011structureevolutionand pages 4-6): Ruoshan Lei, Mingpu Wang, Zhi-you Li, Haigen Wei, Wenchao Yang, Yanlin Jia, and S. Gong. Structure evolution and solid solubility extension of copper–niobium powders during mechanical alloying. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 528:4475-4481, May 2011. URL: https://doi.org/10.1016/j.msea.2011.02.083, doi:10.1016/j.msea.2011.02.083. This article has 76 citations.

20. (minneci2024characterizationandrationalization pages 1-2): Robert P. Minneci, Michael P. Haines, Paul R. Gradl, David L. Ellis, Eric A. Lass, Jeffrey R. Bunn, Hahn Choo, Zachary C. Jones, Sudarsanam S. Babu, and Claudia J. Rawn. Characterization and rationalization of microstructural evolution in grcop-84 processed by laser-powder bed fusion (l-pbf). Metallurgical and Materials Transactions A, 55:1377-1396, Feb 2024. URL: https://doi.org/10.1007/s11661-024-07315-w, doi:10.1007/s11661-024-07315-w. This article has 4 citations.

21. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

22. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

23. (nassar2025methodologyandtechnical pages 24-25): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
