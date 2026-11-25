<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 793106a9-5a24-4130-ae17-5077f1a72015
- Submitted: 2026-10-17T18:59:02Z
- Fetched: 2026-10-17T19:30:36Z (status: success)
- Raw trajectory JSON: ../raw/el-12-Co.json.gz
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

ELEMENT UNDER REVIEW: Co (strengthening addition). C17500 (2.4-2.7 Co with Be), Cu-Ni-Co-Si (C70350), Co in some Cu-Ni and Al bronze variants. Cobalt is a US critical mineral; could it replace part of the nickel?

Answer for Co specifically, not for copper alloys in general:
1. ROLE: what Co does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Co ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Co changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Co, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Co, Cu-Ni-Co and Cu-Al-Co are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Co in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Co neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Co | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Co (strengthening addition). C17500 (2.4-2.7 Co with Be), Cu-Ni-Co-Si (C70350), Co in some Cu-Ni and Al bronze variants. Cobalt is a US critical mineral; could it replace part of the nickel?

Answer for Co specifically, not for copper alloys in general:
1. ROLE: what Co does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Co ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Co changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Co, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Co, Cu-Ni-Co and Cu-Al-Co are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Co in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Co neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Co | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Cobalt (Co) in pre-alloyed powders for marine copper-alloy DED

**Decision: INCLUDE Co as a small, experimental strengthening addition in both Cu–Ni-derived and aluminum-bronze-derived compositions, not as a demonstrated substitute for seawater-grade Ni.** A practical first-pass palette is **0–1.0 wt% Co**; reserve **1.0–2.0 wt% Co** for separately gated trials. The strongest favorable evidence concerns precipitation-hardened *wrought* Cu–Ni–Co–Si, whereas the most directly relevant chloride test on a Co-bearing *bulk aluminum bronze* found worse corrosion than a compositionally different, Co-free bronze. Neither establishes that an as-deposited Co alloy matches wrought C71500. [CITE][GAP] (kuhn2007anewhigh pages 1-2, pan2021accelerateddiscoveryof pages 5-6, atapek2017tribologicalcharacterizationof pages 2-4)

## 1. Established roles and alloy precedents

- **Cu–Ni–Co–Si:** Commercial UNS **C70350 (CuNi1Co1Si)** contains **1.0–2.0 wt% Co, 1.0–2.0 wt% Ni and 0.50–1.0 wt% Si**, Cu balance. Co substitutes for Ni in **δ-(Ni,Co)₂Si** precipitates. This is an *age-hardened electrical-connector strip*, not a qualified marine repair alloy; its specified composition establishes manufacturability, not seawater performance or as-deposited strength. [CITE][NUMBERS][SPEC: UNS/CDA composition reported by Kuhn *et al.*, 2007] (kuhn2007anewhigh pages 1-2, pan2021accelerateddiscoveryof pages 5-6)
- **Experimental Cu–Ni–Co–Si:** At fixed **Ni + Co = 3.0 wt%** and **Si = 0.7 wt%**, tested alloys contained **0.5, 0.7 or 1.0 wt% Co**. The **Cu–2.3Ni–0.7Co–0.7Si** material developed δ-(Ni,Co)₂Si after **70% cold rolling and aging at 450 °C**. Its peak hardness was **258 ± 5 HV after 4 h**, versus approximately **160 HV before aging**; the measured precipitation-hardening contribution was **90 ± 5 HV**, versus **66 ± 6 HV** for Ni₂Si in the Co-free comparator. These are *not* as-deposited DED results. [CITE][NUMBERS] (pan2021accelerateddiscoveryof pages 6-8, pan2021accelerateddiscoveryof pages 5-6, pan2021accelerateddiscoveryof pages 10-12)
- **Aluminum/Mn–Al bronze:** A commercial cast-and-forged mold alloy identified as **CuAl14Fe4Mn2Co** was measured at **13.80 wt% Al, 4.00 wt% Fe, 2.20 wt% Mn and 1.00 wt% Co**, Cu balance. Its reported structure includes a β matrix and coarse **Al–Fe–Co-rich κ particles**. This establishes a **1.00 wt% Co bulk-bronze precedent**, but neither Navy qualification nor a Co-only strengthening effect. A DOE-commissioned copper-alloy assessment categorizes Co as potentially *beneficial* in aluminum bronzes, while calling it *innocuous within anticipated concentrations* in Cu and Cu–Ni; it expressly warns that even these categories have upper bounds. [CITE][NUMBERS] (atapek2017tribologicalcharacterizationof pages 1-2, konynenburg1990backgroundstudiesin pages 142-149)
- **Cu–Be:** A copper-alloy industry handbook describes a low-Be, high-conductivity material with approximately **2.5 wt% Co** and **0.5 wt% Be**, strengthened by thermomechanical processing. This is **not evidence for Co-only strength or seawater fitness**. The requested **UNS C17500 2.4–2.7 wt% Co** specification could not be checked against an unambiguously readable primary UNS/ASTM table; the related mixed **Co + Ni** Be-copper grades must not be misreported as having that much *Co alone*. [CITE][NUMBERS][GAP: exact C17500 specification unverified] (coppers1999copperdevelopmentassociation pages 53-57, coppers1999copperdevelopmentassociation pages 64-65)
- **Other requested families:** No independently verified deliberate Co composition or Co-specific seawater benefit was found for conventional **C71500/C70600, C95800 NAB, tin bronze/gunmetal, Cu–Ni–Sn, or the named Navy brasses and weld fillers**. In particular, *not listing Co* in a retrieved C71500 chemistry is **not** an established numerical impurity maximum. Do not label C70350 or the mold bronze as Navy alloys. [SPEC: C71500 nominal chemistry in DOE technical report; no Co cap established][NAVY][GAP] (mccright1988anannotatedhistory pages 58-60, konynenburg1990backgroundstudiesin pages 136-142, konynenburg1990backgroundstudiesin pages 149-155)

**Mechanistic distinction.** Co can provide limited Cu-matrix solid solution and precipitate strengthening where sufficient **Si** or **Be** and suitable thermal processing exist; in high-Al bronze it partitions into κ-type particles. Cu–Co itself has **no reported equilibrium binary intermetallic**. There is no retrieved demonstration that Co supplies the protective seawater film chemistry ordinarily sought from a Cu–Ni alloy, acts as a dependable deoxidizer or grain refiner in these melts, or inhibits marine dezincification. Instead, a copper-industry review reports that **1.4 wt% Co alone**, or **0.8 wt% Co plus 1.4 wt% Ni**, improved intercrystalline-cracking resistance of *as-cast β brass* but **accelerated dezincification**, followed by weakening. That is a warning about a different, Zn-bearing family—not proof that Co harms NAB or Cu–Ni identically. [CITE][NUMBERS][GAP] (nikolaenko1997enthalpiesofformation pages 1-2, davies1993anoteon pages 5-6, davies1993anoteon pages 6-8, konynenburg1990backgroundstudiesin pages 142-149)

## 2. Chloride and seawater corrosion: what the numbers actually establish

| Evidence and exposure | Co-bearing result | Comparator and interpretation |
|---|---|---|
| **Bulk cast-and-forged bronzes, 3.5 wt% NaCl**, Tafel polarization | **1.00 wt% Co** bronze: *E*₍corr₎ **−281 mV versus SCE**, *i*₍corr₎ **58.20 µA/cm²**, estimated corrosion **26.58 mil/year** | Co-unlisted bronze: **−293 mV**, **14.30 µA/cm²**, **6.508 mil/year**. The Co-bearing material had approximately **4.1-fold higher** current and estimated rate **despite its 12 mV more-positive potential**. Crucially, it also had **more Al and Mn and no Ni**, versus **5.00 wt% Ni** in the comparator: this is **not a controlled Co dose–response**. [CITE][NUMBERS] (atapek2017tribologicalcharacterizationof pages 1-2, atapek2017tribologicalcharacterizationof pages 2-4, atapek2017tribologicalcharacterizationof media e3f84a1f, atapek2017tribologicalcharacterizationof media aa51651d) |
| **Cu–Co/Cu–Ni–Co electrodeposited films on carbon steel**, **0.5 mol/L NaCl**, impedance | **24.4 wt% Co** Cu–Co film: charge-transfer resistance **2,558 Ω·cm²**; **28.3 wt% Co + 10.8 wt% Ni** ternary film: **2,102 Ω·cm²** | Best Cu–Ni film (**46.1 wt% Ni**): **2,162 Ω·cm²**; bare steel: **960 Ω·cm²**. A defective **3.8 wt% Co** Cu–Co film yielded **590 Ω·cm²**, worse than steel. Film thickness, grain size and cracks change with plating conditions; the ternary did **not** significantly surpass both binary coatings. **These submicrometer-to-micrometer electroplates are not bulk DED metal, and 24–28 wt% is not a viable palette bound.** [CITE][NUMBERS] (souza2023copperbinaryand pages 5-6, souza2023copperbinaryand pages 13-14, souza2023copperbinaryand media 00819bce) |
| **As-cast β brass**, chloride-associated selective attack | **0.8–1.4 wt% Co** additions reported to improve resistance to intercrystalline cracking | **Dezincification accelerated**; the trade-off precludes calling Co a general dealloying inhibitor. The retrieved review does not supply a corresponding 30-day seawater penetration depth. [CITE][NUMBERS] (davies1993anoteon pages 5-6) |

**Benefit/harm window:** These studies do **not** establish a Co concentration at which **bulk as-deposited** Cu–Ni or NAB seawater corrosion reliably improves. A **1.00 wt% Co bronze** performed worse than its non-matched comparator; **0.8–1.4 wt% Co β brasses** exhibited worse dezincification; apparently protective **24.4–28.3 wt% Co electrodeposits** cannot set a DED alloy limit. There are no defensible Co-specific numbers here for natural-seawater immersion rate, ASTM D1141 **30-day selective-attack depth**, pit/crevice potential, erosion–corrosion, or safe flow velocity. *E*₍corr₎ alone must not be interpreted as a corrosion rate. [CITE][NUMBERS][GAP] (atapek2017tribologicalcharacterizationof pages 2-4, davies1993anoteon pages 5-6, souza2023copperbinaryand pages 13-14)

## 3. DED, welding, dilution and powder production

**[GAP: Co-specific DED/welding]** No retrieved experiment isolates Co's effect on **single-stream blown-powder Cu DED** solidification cracking, reheated-layer liquation cracking, pore density, 1.07-µm-laser evaporation/oxidation loss, or dilution into **C95800 NAB** and wrought **C71500 Cu–Ni**. A reported NAB laser deposit is described as defect-free, but it does not establish a benefit from adding Co. Separately, a DOE assessment documents conventional weldability of aluminum bronzes used for nuclear-submarine propellers and use of **70/30 Cu–Ni filler** for both 90/10 and 70/30 Cu–Ni: those are **baseline joining precedents, not Co-bearing AWS-filler qualifications**. No verified Co range was obtained for **AWS A5.7 ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl**, or the listed MIL specifications; do not manufacture one. [NAVY][CITE][GAP] (konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 136-142)

**Process risks are hypotheses requiring measurements.** Cu–Co's limited solid miscibility and positive mixing enthalpy make segregated Co-rich particles, wide local freezing intervals and remelt-interface gradients plausible crack/corrosion risks; Co–Si precipitation might occur during repeated passes but published strip-strength figures require controlled aging. For **Al-rich NAB dilution**, assay the deposited top, first layers and fusion boundary separately because Al/Fe/Ni partitioning can change κ/β populations independently of Co. For **Cu–Ni repair**, retain a Ni-bearing control: replacing Ni with Co has not been shown to preserve the C71500 film or properties. Measure powder-versus-ingot-versus-deposit Co/O, inclusions and pores; test alumina/zirconia crucible attack and Ti- or Mo-sonotrode pickup rather than asserting a proven Co-specific reaction. Co's high melting point does not imply preferential Co evaporation; Co-specific vapor-loss, melt surface-tension, ceramic-reactivity and sonotrode-wear coefficients were not recovered. In particular, adding Co must not be described as an established substitute for oxygen control under argon. [CITE][GAP] (nikolaenko1997enthalpiesofformation pages 1-2, pan2021accelerateddiscoveryof pages 5-6, konynenburg1990backgroundstudiesin pages 142-149)

## 4. Phase equilibria and computational gate

**[CITE][NUMBERS]** The Cu–Co binary has **maximum equilibrium Co solubility in Cu-rich fcc of atomic fraction 0.08 at 1,385 K (≈1,112 °C)**, equivalent to **≈7.46 wt% Co** using Cu 63.546 and Co 58.933 g/mol. Its reported **peritectic α-Co + liquid ⇌ Cu-rich fcc** occurs at **1,385 K**; no binary compound is reported. Substantial positive liquid mixing enthalpy, **7.1 ± 0.9 kJ/mol** at Co atomic fraction 0.55, contrasts with Cu–Ni's continuous binary liquid/solid solutions. The Cu–Co liquidus becomes approximately **1,673 K (1,400 °C)** over an intermediate-Co region; thus a pure-Co endpoint (**1,495 °C**) or intermediate-Co-rich melt is unsuitable for the stated atomizer. **Do not treat the 7.46 wt% maximum *solid* solubility as the allowable room-temperature, corrosion-safe or atomizable Co content:** a multicomponent alloy's liquidus and superheat must be calculated and then measured. [CITE][NUMBERS] (nikolaenko1997enthalpiesofformation pages 1-2, nikolaenko1997enthalpiesofformation pages 6-7)

**[GAP: database verification]** The retrieved source establishes binary phase behavior but does **not** verify that the particular installed **Thermo-Calc TCCU release**, **COST 531**, or an accessible published **Cu–Al–Co / Cu–Ni–Co TDB** contains assessed ternary Co interactions. Check the installed database element/phase inventory and assessment documentation; reproduce binary Cu–Co and Ni-containing isopleths before trusting multicomponent extrapolation, and use DSC on each proposed charge. For this apparatus require a **computed and measured liquidus ≤1,200–1,250 °C with useful operating superheat**, rather than claiming that **2 wt% Co itself** crosses that threshold in every Cu–Ni/bronze composition. [GAP] (nikolaenko1997enthalpiesofformation pages 1-2)

## 5. Supply, occupational health and bounds

**[CITE][NUMBERS]** USGS documentation confirms **Co and Cu on the final 2025 U.S. critical-minerals list**; the August draft contained **54** commodities and November final **60**. A retrieved USGS analysis addresses trade-disruption risk; it is not a dated cobalt metal quotation. **A defensible current dollar-per-kilogram Co price and a verified 2022-list citation could not be extracted**, so neither a spot quotation nor a false fixed price is supplied. Quote a dated purchasing/index price separately for the proposal, distinguishing metal from small-lot high-purity powder. Co is **not a supply-risk-free replacement** for Ni. [CITE][NUMBERS][GAP] (iii2026usgscriticalminerals pages 1-2, nassar2025methodologyandtechnical pages 1-4, profileUnknownyear1.geologicalconsiderationsa pages 6-9)

**[CITE][GAP]** Treat Co-containing powder and collected laser fume as inhalation hazards: enclosed transfer, local extraction/filtration, exposure assessment, appropriate respirators and combustible-dust controls are warranted. A retrieved historical safety table displays **0.1 mg/m³ as Co** for dust/fume but has corrupted column alignment, so it **cannot authenticate that number as the present OSHA PEL or NIOSH REL**. Verify applicable current OSHA/NIOSH limits and the particular powder's SDS; no verified blanket Co limit under **RoHS/REACH** or Navy procurement rule was retrieved. Do not conflate elemental Co with cobalt–tungsten-carbide carcinogenicity classifications, or Co with Be-fume hazards. [CITE][GAP] (arnold1990healthandsafety pages 49-51, headquarters20131.identification pages 8-9, coppers1999copperdevelopmentassociation pages 53-57)

**Proposed search-space bounds—not certified service limits:**

| Applicable family | Co bound, wt% of alloy | Basis; bound-setting failure mode |
|---|---:|---|
| **Both**, conservative screening maximum | **1.0** | Direct bulk-bronze precedent **1.00**; independently, experimental Cu–Ni–Co–Si reaches **1.0**. Stops before the **1.0–2.0** commercial strip interval becomes the default for *as-deposited marine metal*. Gate on bronze chloride attack and Co-rich/κ segregation. This is a *research cap*, **not** a demonstrated corrosion-safe threshold. [NUMBERS][CITE] (atapek2017tribologicalcharacterizationof pages 1-2, pan2021accelerateddiscoveryof pages 5-6, atapek2017tribologicalcharacterizationof pages 2-4) |
| **Both**, non-conservative screening maximum | **2.0** | Upper Co concentration documented for **C70350 wrought strip**, not for seawater DED; above the **1.00 wt%** Co cast-bronze precedent. Conditional on phase/liquidus calculation, successful atomization, crack-free deposition and measured corrosion. Failure modes: loss of superheat, Co-/κ-rich heterogeneity, local attack and unqualified repair dilution. [NUMBERS][SPEC: published UNS C70350 range][GAP] (kuhn2007anewhigh pages 1-2, nikolaenko1997enthalpiesofformation pages 1-2, atapek2017tribologicalcharacterizationof pages 2-4) |
| **Both**, functional research floor | **0.5** | Lowest Co addition **actually tested** in the retrieved Cu–Ni–Co–Si composition series. It is a **testable floor**, *not* proof of a measurable beneficial response at 0.5 wt% in as-deposited Cu–Ni or Al bronze. If no Co-specific benefit above measurement scatter occurs, remove Co from the final palette. [NUMBERS][GAP] (pan2021accelerateddiscoveryof pages 5-6, pan2021accelerateddiscoveryof pages 10-12) |

**Interactions for joint constraints.** In silicide designs, screen **Ni + Co** together (**3.0 wt%** in one experimental series) and the approximate **(Ni + Co):Si atomic ratio ≈2:1** for δ-(Ni,Co)₂Si; these are *precipitation-design relationships*, not seawater-qualified allowable sums. Co substitution for Ni changed overaging response **after** cold work and aging, not proven Cu–Ni-film protection. In bronze, constrain **Co jointly with Al, Fe, Mn and Ni** because Co participates in Al–Fe–Co-rich κ particles and the unfavorable **1.00 wt% Co** comparison also changed all four other elements. In β brass, **Co + Ni** did not neutralize dezincification. Do not infer that Co neutralizes oxygen, dealloying, or weld-hot-crack promoters **Pb/Bi/S/O**. [CITE][NUMBERS][GAP] (pan2021accelerateddiscoveryof pages 6-8, pan2021accelerateddiscoveryof pages 5-6, atapek2017tribologicalcharacterizationof pages 1-2, davies1993anoteon pages 5-6, konynenburg1990backgroundstudiesin pages 142-149)

**Evidence assessment.** Strong for the *existence* of cobalt-bearing connector strip, a cobalt-bearing cast bronze, the Cu–Co binary phase diagram and the measured outcomes *in their own test conditions*; **thin for the requested as-deposited, seawater-exposed, Co-containing DED powder and NAB/Cu–Ni repairs**. No retrieved controlled experiment proves a positive Co window or a safe Ni-for-Co replacement. Consequently, the numbers above define an explicitly falsifiable proposal palette, not a claim of qualified service performance. [GAP] (kuhn2007anewhigh pages 1-2, atapek2017tribologicalcharacterizationof pages 2-4, souza2023copperbinaryand pages 13-14, nikolaenko1997enthalpiesofformation pages 1-2)

**Key full references:** Atapek Ş.H. *et al.*, “Tribological Characterization of Al-bronzes Used as Mold Materials,” *Archives of Foundry Engineering* **17**, 7–12 (2017), DOI **10.1515/afe-2017-0122**; de Souza T.M. *et al.*, “Copper Binary and Ternary Alloys as Anticorrosive Coatings for Carbon Steel in a Saline Medium,” *Materials Research* **26** (2023), DOI **10.1590/1980-5373-mr-2023-0076**; Kuhn H.-A. *et al.*, “A new high performance copper based alloy for electro-mechanical connectors,” *Materialwissenschaft und Werkstofftechnik* **38**, 624–634 (2007), DOI **10.1002/mawe.200700152**; Pan S. *et al.*, “Accelerated discovery of high-performance Cu–Ni–Co–Si alloys through machine learning,” *Materials & Design* **209**, 109929 (2021), DOI **10.1016/j.matdes.2021.109929**; Nikolaenko I.V. and Turchanin M.A., “Enthalpies of Formation of Liquid Binary (Copper + Iron, Cobalt, and Nickel) Alloys,” *Metallurgical and Materials Transactions B* **28**, 1119–1130 (1997), DOI **10.1007/s11663-997-0068-5**; Davies D.D., *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*, Copper Development Association (1993), **DOI not identified** (summarizes Bailey, *Journal of the Institute of Metals* **89**, 110 (1960–61)); Van Konynenburg R.A. *et al.*, *Background Studies in Support of a Feasibility Assessment on the Use of Copper-Base Materials for Nuclear Waste Packages in a Repository in Tuff*, DOE (1990), DOI **10.2172/137782**; Nassar N.T. *et al.*, USGS Open-File Report **2025–1047** (2025), DOI **10.3133/ofr20251047**. (atapek2017tribologicalcharacterizationof pages 2-4, souza2023copperbinaryand pages 13-14, kuhn2007anewhigh pages 1-2, pan2021accelerateddiscoveryof pages 5-6, nikolaenko1997enthalpiesofformation pages 1-2, davies1993anoteon pages 5-6, konynenburg1990backgroundstudiesin pages 142-149, nassar2025methodologyandtechnical pages 1-4)

VERDICT | Co | decision=INCLUDE | family=both | conservative_max_wt=1.0 | nonconservative_max_wt=2.0 | floor_wt=0.5 | impurity_max_wt=NA | evidence=thin

References

1. (kuhn2007anewhigh pages 1-2): H.‐A. Kuhn, A. Käufler, D. Ringhand, and S. Theobald. A new high performance copper based alloy for electro‐mechanical connectors. Materialwissenschaft und Werkstofftechnik, 38:624-634, Aug 2007. URL: https://doi.org/10.1002/mawe.200700152, doi:10.1002/mawe.200700152. This article has 19 citations and is from a peer-reviewed journal.

2. (pan2021accelerateddiscoveryof pages 5-6): Shaobin Pan, Yongjie Wang, Jinxin Yu, Mujin Yang, Yanqing Zhang, Haiting Wei, Yuechao Chen, Junwei Wu, Jiajia Han, Cuiping Wang, and Xingjun Liu. Accelerated discovery of high-performance cu-ni-co-si alloys through machine learning. Materials & Design, 209:109929, Nov 2021. URL: https://doi.org/10.1016/j.matdes.2021.109929, doi:10.1016/j.matdes.2021.109929. This article has 90 citations and is from a highest quality peer-reviewed journal.

3. (atapek2017tribologicalcharacterizationof pages 2-4): Ş. H. Atapek, G. Aktaş Çelik, Ş. Polat, and B. Pisarek. Tribological characterization of al-bronzes used as mold materials. Archives of Foundry Engineering, 17:7-12, Dec 2017. URL: https://doi.org/10.1515/afe-2017-0122, doi:10.1515/afe-2017-0122. This article has 6 citations.

4. (pan2021accelerateddiscoveryof pages 6-8): Shaobin Pan, Yongjie Wang, Jinxin Yu, Mujin Yang, Yanqing Zhang, Haiting Wei, Yuechao Chen, Junwei Wu, Jiajia Han, Cuiping Wang, and Xingjun Liu. Accelerated discovery of high-performance cu-ni-co-si alloys through machine learning. Materials & Design, 209:109929, Nov 2021. URL: https://doi.org/10.1016/j.matdes.2021.109929, doi:10.1016/j.matdes.2021.109929. This article has 90 citations and is from a highest quality peer-reviewed journal.

5. (pan2021accelerateddiscoveryof pages 10-12): Shaobin Pan, Yongjie Wang, Jinxin Yu, Mujin Yang, Yanqing Zhang, Haiting Wei, Yuechao Chen, Junwei Wu, Jiajia Han, Cuiping Wang, and Xingjun Liu. Accelerated discovery of high-performance cu-ni-co-si alloys through machine learning. Materials & Design, 209:109929, Nov 2021. URL: https://doi.org/10.1016/j.matdes.2021.109929, doi:10.1016/j.matdes.2021.109929. This article has 90 citations and is from a highest quality peer-reviewed journal.

6. (atapek2017tribologicalcharacterizationof pages 1-2): Ş. H. Atapek, G. Aktaş Çelik, Ş. Polat, and B. Pisarek. Tribological characterization of al-bronzes used as mold materials. Archives of Foundry Engineering, 17:7-12, Dec 2017. URL: https://doi.org/10.1515/afe-2017-0122, doi:10.1515/afe-2017-0122. This article has 6 citations.

7. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

8. (coppers1999copperdevelopmentassociation pages 53-57): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

9. (coppers1999copperdevelopmentassociation pages 64-65): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

10. (mccright1988anannotatedhistory pages 58-60): R. D. McCright. An annotated history of container candidate material selection. ArXiv, Jul 1988. URL: https://doi.org/10.2172/60703, doi:10.2172/60703. This article has 11 citations.

11. (konynenburg1990backgroundstudiesin pages 136-142): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

12. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

13. (nikolaenko1997enthalpiesofformation pages 1-2): I. V. Nikolaenko and M. A. Turchanin. Enthalpies of formation of liquid binary (copper + iron, cobalt, and nickel) alloys. Metallurgical and Materials Transactions B, 28:1119-1130, Dec 1997. URL: https://doi.org/10.1007/s11663-997-0068-5, doi:10.1007/s11663-997-0068-5. This article has 51 citations.

14. (davies1993anoteon pages 5-6): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

15. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

16. (atapek2017tribologicalcharacterizationof media e3f84a1f): Ş. H. Atapek, G. Aktaş Çelik, Ş. Polat, and B. Pisarek. Tribological characterization of al-bronzes used as mold materials. Archives of Foundry Engineering, 17:7-12, Dec 2017. URL: https://doi.org/10.1515/afe-2017-0122, doi:10.1515/afe-2017-0122. This article has 6 citations.

17. (atapek2017tribologicalcharacterizationof media aa51651d): Ş. H. Atapek, G. Aktaş Çelik, Ş. Polat, and B. Pisarek. Tribological characterization of al-bronzes used as mold materials. Archives of Foundry Engineering, 17:7-12, Dec 2017. URL: https://doi.org/10.1515/afe-2017-0122, doi:10.1515/afe-2017-0122. This article has 6 citations.

18. (souza2023copperbinaryand pages 5-6): Thais Machado de Souza, Gustavo Dionisio Mesquita, Bruno S. M. Loureiro, Lucas Ferreira da Silva Dias, Dalva C. B. do Lago, and Lilian F. de Senna. Copper binary and ternary alloys as anticorrosive coatings for carbon steel in a saline medium. Materials Research, Jan 2023. URL: https://doi.org/10.1590/1980-5373-mr-2023-0076, doi:10.1590/1980-5373-mr-2023-0076. This article has 7 citations.

19. (souza2023copperbinaryand pages 13-14): Thais Machado de Souza, Gustavo Dionisio Mesquita, Bruno S. M. Loureiro, Lucas Ferreira da Silva Dias, Dalva C. B. do Lago, and Lilian F. de Senna. Copper binary and ternary alloys as anticorrosive coatings for carbon steel in a saline medium. Materials Research, Jan 2023. URL: https://doi.org/10.1590/1980-5373-mr-2023-0076, doi:10.1590/1980-5373-mr-2023-0076. This article has 7 citations.

20. (souza2023copperbinaryand media 00819bce): Thais Machado de Souza, Gustavo Dionisio Mesquita, Bruno S. M. Loureiro, Lucas Ferreira da Silva Dias, Dalva C. B. do Lago, and Lilian F. de Senna. Copper binary and ternary alloys as anticorrosive coatings for carbon steel in a saline medium. Materials Research, Jan 2023. URL: https://doi.org/10.1590/1980-5373-mr-2023-0076, doi:10.1590/1980-5373-mr-2023-0076. This article has 7 citations.

21. (nikolaenko1997enthalpiesofformation pages 6-7): I. V. Nikolaenko and M. A. Turchanin. Enthalpies of formation of liquid binary (copper + iron, cobalt, and nickel) alloys. Metallurgical and Materials Transactions B, 28:1119-1130, Dec 1997. URL: https://doi.org/10.1007/s11663-997-0068-5, doi:10.1007/s11663-997-0068-5. This article has 51 citations.

22. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

23. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

24. (profileUnknownyear1.geologicalconsiderationsa pages 6-9): C PROFILE. 1. geological considerations. Unknown journal, Unknown year.

25. (arnold1990healthandsafety pages 49-51): SD Arnold and GM Talley. Health and safety guide for inorganic compounds and metals used in the fabrication of superconductive alloys. Unknown journal, 1990.

26. (headquarters20131.identification pages 8-9): C Headquarters, U Ave, and DB Street. 1. identification. Unknown journal, 2013.
