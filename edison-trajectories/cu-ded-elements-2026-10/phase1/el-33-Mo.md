<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: d8b5d0f1-4ab6-4655-8138-33f1da1fc91a
- Submitted: 2026-10-17T19:00:52Z
- Fetched: 2026-10-17T19:30:52Z (status: success)
- Raw trajectory JSON: ../raw/el-33-Mo.json.gz
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

ELEMENT UNDER REVIEW: Mo (refractory, immiscible). Mo raises the pitting resistance of stainless steels and nickel alloys; does it do anything in Cu-Ni or aluminum bronze? Cu-Mo is nearly immiscible. TZM (Mo alloy) is a candidate sonotrode material, so Mo pickup matters.

Answer for Mo specifically, not for copper alloys in general:
1. ROLE: what Mo does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Mo ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Mo changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Mo, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Mo, Cu-Ni-Mo and Cu-Al-Mo are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Mo in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Mo neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Mo | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Mo (refractory, immiscible). Mo raises the pitting resistance of stainless steels and nickel alloys; does it do anything in Cu-Ni or aluminum bronze? Cu-Mo is nearly immiscible. TZM (Mo alloy) is a candidate sonotrode material, so Mo pickup matters.

Answer for Mo specifically, not for copper alloys in general:
1. ROLE: what Mo does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Mo ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Mo changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Mo, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Mo, Cu-Ni-Mo and Cu-Al-Mo are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Mo in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Mo neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Mo | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Molybdenum in pre-alloyed powder for marine copper-alloy DED

**Decision: LIMIT Mo to incidental contamination, not a designed addition.** The decisive evidence is a near-immiscible Cu–Mo binary, a strong dependence of Mo accommodation on Ni content, and the absence of a demonstrated *Mo-only* seawater-corrosion benefit in a deposit. A Cu–Ni study does measure chloride performance, but its Mo-containing alloys also contain boron and undergo a 600 °C anneal; at its lower addition, polarization resistance **decreased**, not increased. Cast Mo-modified nickel-aluminum bronze (NAB) shows some mechanical strengthening but has neither a seawater test nor evidence that the charged Mo was uniformly incorporated. None of these experiments establishes dense, crack-free, corrosion-resistant **as-deposited, single-stream DED** material. [CITE] (hou2021effectsofmo pages 75-81, anene2019effectofdopant pages 1-3, anene2019effectofdopant pages 3-13, kozlova1973boundariesofthe pages 1-3)

## Role, commercial precedent, and corrosion

- **Cu–Ni.** Ni changes the physical premise: measured Mo solubility in Cu–Ni solid solution is approximately **1.0 wt% Mo at 10 wt% Ni**, **1.5–2.0 wt% Mo at 20–30 wt% Ni**, and **3.0–3.5 wt% Mo at 40 wt% Ni**, for the reported 900–1100 °C homogenization conditions. These are *solid-state ternary phase limits*, not corrosion-optimum concentrations or evidence that Mo can be pre-alloyed at the proposed atomization temperature. At sufficiently high Mo and Ni, Mo-rich particles and **NiMo/MoNi** occur. [NUMBERS] (kozlova1973boundariesofthe pages 3-4, kozlova1973boundaryofthe pages 1-3)
- **Cu–Ni plus B:** Arc-melted experimental material contains NiMo and, with B, Ni borides and Mo₂NiB₅; strengthening is attributable substantially to hard second phases rather than a proven Mo-enriched protective seawater film. The experiments cannot separate the corrosion effect of Mo from B using the reported corrosion comparison. [CITE] (hou2021effectsofmo pages 40-50, hou2021effectsofmo pages 75-81, hou2021effectsofmo pages 81-89)
- **NAB/aluminum bronze.** One casting study charged **2 or 3 wt% Mo** into nominal Cu–10Al–5Ni–5Fe, reporting α, β′ and κ-type microstructures. As-cast tensile strength increased from **434 MPa** without Mo to **457 and 460 MPa**, respectively; elongation decreased from **34%** to **32% and 31%**. This is *not* a demonstrated seawater-corrosion benefit, and the paper’s selected EDS spectra frequently do not report Mo: claims that Mo uniformly enters a specific κ phase or refines grains require verification. Its heat-treated improvements cannot be transferred to an as-deposited target. [NUMBERS] [GAP] (anene2019effectofdopant pages 1-3, anene2019effectofdopant pages 3-13, anene2019effectofdopant pages 13-15)
- **Other families.** No verified intentional Mo range or demonstrated Mo-specific seawater function was found for manganese-aluminum bronze, tin bronze/gunmetal, brasses, Cu–Ni–Sn or Cu–Ni–Si. Do not mistake molybdate inhibitors or MoS₂-bearing composites for metallic Mo pre-alloyed into those matrices. No evidence establishes Mo-mediated deoxidation, grain refinement, suppression of dezincification/dealuminification, or incorporation into a protective Cu₂O/Ni/Al-oxide film. The historical documented improvements instead involve Fe/Mn in Cu–Ni, Al/As in certain brasses/bronzes, or Cr in C72200—not Mo. [GAP] (din1993effectofresidual pages 4-7, kozlova1973boundariesofthe pages 1-3)
- **Specifications.** The retrieved UNS/CDA C71500 composition lists **29.0–33.0 wt% Ni** and **0.40–0.70 wt% Fe**, but **no intentional Mo range or Mo-specific impurity maximum**; the cited product forms include ASTM **B111, B171 and B466**. Retrieved AM examples of **AWS A5.7 ERCuNiAl/C95800** use Al–Ni–Fe–Mn, not identified Mo additions. I could not verify a Mo-bearing copper-alloy composition or a numerical Mo maximum under ASTM **B148/B369**, **MIL-T-16420/MIL-B-24480/MIL-C-15726**, **EN 12449**, or AWS A5.7 **ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl**. Thus **“Mo 0 wt% specified” would be incorrect**: *not specified* is not an analytical zero-content requirement. [SPEC] [NAVY] [GAP] (mccright1988anannotatedhistory pages 58-60, nemani2024advancementsinadditive pages 60-62)

**Best directly relevant chloride comparison.** Hou *et al.* used **3 wt% NaCl**, not natural or ASTM D1141 seawater; nominal alloy recipes are given in **atomic percent**, so their labels “2%Mo–2%B” must **not** be read as **2 wt% Mo–2 wt% B**. Their 48 at% Cu–48 at% Ni–2 at% Mo–2 at% B recipe corresponds, by atomic-mass conversion, to approximately **3.16 wt% Mo and 0.36 wt% B**; the 65 at% Cu–31 at% Ni–2 at% Mo–2 at% B recipe is approximately **3.11 wt% Mo and 0.35 wt% B**. These are calculated nominal values, not independently verified deposited compositions. Samples were repeatedly arc melted and annealed **4 h at 600 °C**. [NUMBERS] (hou2021effectsofmo pages 33-40, hou2021effectsofmo pages 40-50)

For the nominal **50 at% Cu–50 at% Ni** base, reported open-circuit potential was **−0.210 V versus SCE** and linear polarization resistance **16,690.4 Ω·cm²**; its 2 at% Mo + 2 at% B modification gave **−0.252 V** and **7,589.5 Ω·cm²**—a **55% decrease** in resistance. For the **68 at% Cu–32 at% Ni** base, values changed from **−0.218 V, 8,782.8 Ω·cm²** to **−0.242 V, 3,766.4 Ω·cm²**—a **57% decrease**. The 50:50 material with **10 at% Mo + 10 at% B** gave **−0.285 V, 13,766.9 Ω·cm²**, still below its unmodified base resistance. The authors propose corrosion-prone interphase boundaries; this is a proposed mechanism, not measured Mo-specific film chemistry. The 2 at% Mo + 2 at% B material reduced *sliding wear volume* in NaCl by **56%**, which is **not** a 56% reduction in corrosion rate. No defensible beneficial Mo-only concentration window, harmful Mo-only threshold, corrosion-rate change, pitting/crevice potential, dealloying depth, erosion-corrosion limit or flow-velocity limit follows from these data. [NUMBERS] [CITE] [GAP] (hou2021effectsofmo pages 75-81, hou2021effectsofmo media 37c817b0)

## Melting, phase equilibria, CALPHAD and repair

**Cu–Mo is not a conventional substitutional-alloy design axis.** The published thermodynamic reassessment predicts a Cu-rich eutectic at **0.119 wt% Mo in liquid, 1357.3 K (1084.2 °C)**, with approximately **0.023 wt% Mo in equilibrium Cu-rich solid** and **99.962 wt% Mo in the Mo-rich phase**; it predicts a Mo-rich monotectic near **2787.6 K**, at **93.22 wt% Mo** in the reacting liquid. These are *calculated*, sparsely experimentally constrained invariant coordinates—not a measured maximum Cu-solid solubility over all temperatures. The **0.023 wt% at 1084 °C** estimate is a useful approximate upper equilibrium Cu-rich solid value from that assessment, **not** a universal certified solubility. Binary Cu–Mo has **no established stable Cu–Mo intermetallic** in that model; NiMo is a *ternary* Ni-containing outcome. The calculated liquid miscibility gap and the approximately **2896 K** melting point of pure Mo explain why nominal addition and actual homogeneous liquid composition can diverge. [NUMBERS] [CITE] (wang2000phaseequilibriain pages 6-9, wang2000phaseequilibriain pages 3-5, wang2000phaseequilibriain pages 5-6, kozlova1973boundariesofthe pages 1-3)

A **Cu-rich liquid can form near copper’s melting point without melting all Mo**. Thus it is misleading to assert that every nonzero Mo addition raises *the Cu-rich liquidus* above **1250 °C**; equally misleading is calling a suspension of undissolved, high-melting Mo *fully pre-alloyed powder*. Ni and Fe change partitioning: in measured Cu–Fe–Mo equilibria the Cu-rich liquid contains roughly **0.05–0.20 wt% Mo** over the reported **1373–1573 K** measurements, whereas much higher solid-state Mo accommodation was measured in Ni-rich Cu–Ni–Mo. Neither measurement establishes complete dissolution of charged Mo in a **~1300 °C** induction melt; a target with a verified **1200–1250 °C liquidus**, useful superheat and no residual particles must be calculated and experimentally checked for each multicomponent recipe. [NUMBERS] [GAP] (wang2000phaseequilibriain pages 2-3, wang2000phaseequilibriain pages 3-5, kozlova1973boundariesofthe pages 3-4)

**Database status:** Wang *et al.* publish explicit Cu–Mo liquid/fcc/bcc CALPHAD parameters and a Cu–Fe–Mo assessment; published experimental Cu–Ni–Mo phase boundaries exist. Those facts **do not verify** that licensed **Thermo-Calc TCCU**, **COST 531**, or a given pycalphad TDB contains mutually consistent assessed **Cu–Ni–Mo and Cu–Al–Mo ternaries**, nor that all NAB κ phases are represented. Inspect the actual database element/phase/interaction listings and compare calculated binary invariants and Ni-bearing isotherms with experiments *before* trusting Scheil liquidus, phase-fraction or hot-cracking rankings. [CITE] [GAP] (wang2000phaseequilibriain pages 5-6, wang2000phaseequilibriain pages 6-9, kozlova1973boundariesofthe pages 3-4)

**Powder and joining implications—not measured Mo-specific DED effects.** At the stipulated induction limit, pure Mo pellets or Mo-bearing material can persist as dense refractory inclusions or segregate between droplets; charged composition should therefore be checked against melt, particle-by-particle and bulk powder assays. A published Cu–Ni–Mo preparation used zirconia and alumina crucibles or levitation melting, but does **not** validate oxygen pickup, dissolution yield or sonotrode wear on this particular argon induction atomizer. No measured Mo-specific reaction rate with alumina, zirconia, graphite or titanium sonotrodes, change in melt surface tension, or preferential Mo evaporation at **1.07 µm** was established. Mo pickup from a TZM sonotrode is a credible contamination *hypothesis*, not a quantified pickup rate. Keep Mo loss distinct from more readily volatile alloy constituents and from oxide-bearing laser fume; measure before/after compositions and oxygen. [GAP] (kozlova1973boundariesofthe pages 1-3, anene2019effectofdopant pages 1-3)

Near-infrared copper reflectivity and high conductivity generally challenge fusion AM. The retrieved Cu-rich NAB AM examples and AWS ERCuNiAl welding feedstocks **do not contain a controlled Mo addition**. An unrelated, **Mo-matrix** LPBF experiment with **20 vol% Cu** reached only **97–98% relative density** and retained grain-boundary cracks, some Cu-filled; it cannot demonstrate that adding Mo heals cracking in a **Cu-matrix blown-powder DED** deposit. There are no attributable Mo-specific measurements of Cu-alloy solidification cracking, reheated-layer liquation, oxide-associated porosity, laser evaporation, or dilution-induced cracking on cast C95800 or wrought C71500. Treat Mo-rich particles/NiMo and Fe-bearing interfacial phases as *risks to test*, not proven defects: section first-layer and reheated-layer interfaces; compare Mo segregation, crack/void frequency and 30-day selective-attack depth against Mo-free controls. Even a genuinely single-phase Cu–Ni–Mo equilibrium calculation need not describe a rapidly cooled, locally diluted NAB repair bead. [NAVY] [GAP] (nemani2024advancementsinadditive pages 1-2, nemani2024advancementsinadditive pages 60-62, hyer2025strategiesforfabricating pages 23-26, kozlova1973boundariesofthe pages 3-4)

## Bounds, interactions and secondary constraints

**[LIMIT; Cu–Ni and aluminum-bronze families]** Set the *provisional project screening/action ceiling* at **0.02 wt% Mo (200 mass-ppm)** in **both assayed DED powder and deposit**, with **zero intentional charge**. This is deliberately near/below the reassessed **~0.023 wt% Cu-rich solid equilibrium estimate at 1084 °C**; it is **not an ASTM, MIL, AWS or Navy impurity specification and not an experimentally demonstrated safe seawater threshold**. Its purpose is to detect sonotrode/recycled-feedstock pickup and avoid assuming that trace Mo remains dissolved across Cu-rich and Al-bronze formulations. The bound’s failure mode is undissolved/segregated refractory material and possible local galvanic attack, **not** a documented onset of cracking at 200 ppm. If analytical reproducibility or measured pickup makes 200 ppm unworkable, report that explicitly and requalify a *measured* process-specific limit; do not silently relax it as a standards allowance. Because this is LIMIT rather than INCLUDE, **conservative maximum, nonconservative maximum and functional floor are NA**. Neither the **2–3 wt% Mo charged into experimental cast NAB** nor the approximately **3.1 wt% Mo nominal in co-doped Cu–Ni** is an established commercial upper bound or a demonstrated beneficial floor for this application. [NUMBERS] [GAP] (wang2000phaseequilibriain pages 6-9, anene2019effectofdopant pages 1-3, hou2021effectsofmo pages 40-50, hou2021effectsofmo pages 75-81)

**Joint constraints.** Mo partitioning must be evaluated **with Ni**, not independently: approximate measured Cu–Ni solid solubility grows from **~1 wt% Mo at 10 wt% Ni** to **~3–3.5 wt% Mo at 40 wt% Ni** under the cited high-temperature treatments. At elevated Mo and Ni, monitor NiMo and loss of Ni from the Cu-rich matrix; **Fe** can redirect Mo into Fe–Mo-bearing phases, and **Al/Fe/Ni** already control NAB α/β/κ fractions. B is an essential confounder in the chloride study because it yields Ni borides and Mo₂NiB₅; none of these observations defines a validated Ni:Mo, Fe:Mo, Mn:Mo or Al:Mo corrosion-optimizing ratio, or shows that Mo neutralizes an impurity. [NUMBERS] [GAP] (kozlova1973boundariesofthe pages 3-4, kozlova1973boundaryofthe pages 3-4, wang2000phaseequilibriain pages 2-3, hou2021effectsofmo pages 40-50, anene2019effectofdopant pages 3-13)

**Supply and safety.** **Mo is absent from both the 2022 U.S. critical-minerals list and the 2025 *final* list**: the latter’s alphabetical table goes from manganese/metallurgical coal through neodymium, nickel and niobium without Mo. Conversely **Cu was added to the final 2025 list** and Ni appears in it. Critical-list exclusion does not rule out procurement risk: the mining review records **Chinese Mo export controls in February 2025**. [SPEC] (staff2022usgsminingreview pages 3-5, staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 9-11, nassar2025methodologyandtechnical pages 9-10)

No verifiable, like-for-like **2025–26 price per kilogram of elemental Mo metal suitable for an atomizer charge** was obtained; assigning a commodity *oxide* or concentrate quote to high-purity pellets would be spurious. Likewise, no Mo-specific OSHA exposure number or RoHS/REACH/Navy **ban applicable to this alloy** was validated by the retrieved primary material. Treat fine combustible/respirable metal-containing powder and laser fume as exposure and housekeeping hazards: obtain the actual feedstock SDS and applicable OSHA standards, control airborne dust/fume, and distinguish metallic Mo from soluble molybdates and Mo oxides before specifying a limit. [GAP] (staff2022usgsminingreview pages 3-5, kodali2026toxicityofairborne pages 8-9)

**Evidence grade: thin for the proposed marine as-deposited DED decision**, notwithstanding useful primary phase-equilibrium data and one confounded quantitative NaCl comparison. Priority falsification tests are Mo-free versus trace-Mo controls from the same powder route; powder/deposit Mo and oxygen assays; particle and repair-interface microscopy; and identical as-deposited ASTM D1141 electrochemistry followed by **30-day maximum selective-attack depth**, alongside wrought C71500. [GAP] (hou2021effectsofmo pages 75-81, anene2019effectofdopant pages 1-3, kozlova1973boundariesofthe pages 3-4)

**Full identifiable literature citations:** Wang, C. P., Liu, X. J., Ohnuma, I., Kainuma, R., Ishida, K. and Hao, S. M., “Phase equilibria in the Cu–Fe–Mo and Cu–Fe–Nb systems,” *Journal of Phase Equilibria* **21** (2000), 54–62, DOI **10.1361/105497100770340426**; Kozlova, R. F., Rabkin, V. B. and Blinova, N. V., “Boundaries of the single-phase side fields of the system Mo–Cu–Ni in the solid state,” *Soviet Powder Metallurgy and Metal Ceramics* **12** (1973), 140–144, DOI **10.1007/BF00807778**; Kozlova, R. F., Rabkin, V. B., Losev, L. Ya. and Pashchenko, E. F., “Boundary of the two-phase field of Mo(Ni,Cu) and Cu(Ni,Mo) solid solutions,” *ibid.* **12** (1973), 399–402, DOI **10.1007/BF00791268**; Hou, R., Wu, M.-W., Li, Q., Li, W., Chen, D. L. and Li, D., “Effects of Mo and B additives on hardness and the resistance of Cu–Ni alloy to wear, corrosion and corrosive wear,” *Metals and Materials International* **27** (2021), 4911–4921, DOI **10.1007/s12540-020-00801-x**; Anene, F. A., Nwankwo, N. E. and Nwoke, V. U., “Effect of dopant and heat treatment on the microstructure and mechanical properties of nickel-aluminum bronze,” *Metallurgical and Materials Engineering* **25** (2019), 147–162, DOI **10.30544/423**; Nemani, A. V. *et al.*, “Advancements in additive manufacturing for copper-based alloys and composites,” *Journal of Manufacturing and Materials Processing* **8** (2024), 54, DOI **10.3390/jmmp8020054**; Hyer, H. C. *et al.*, “Strategies for fabricating molybdenum structures using laser powder bed fusion,” technical report (2025), DOI **10.2172/3377998**; Nassar, N. T. *et al.*, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, USGS OFR 2025-1047, DOI **10.3133/ofr20251047**. Standards and the cited mining-review composition table were not independently retrieved as current controlled editions; no DOI or unverified Mo clause is asserted for them. (wang2000phaseequilibriain pages 6-9, kozlova1973boundariesofthe pages 3-4, kozlova1973boundaryofthe pages 1-3, hou2021effectsofmo pages 75-81, anene2019effectofdopant pages 1-3, nemani2024advancementsinadditive pages 1-2, hyer2025strategiesforfabricating pages 23-26, nassar2025methodologyandtechnical pages 9-10, mccright1988anannotatedhistory pages 58-60)

VERDICT | Mo | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.02 | evidence=thin

References

1. (hou2021effectsofmo pages 75-81): Runfang Hou, Ming-Wei Wu, Qingyang Li, Wei Li, Daolun L. Chen, and Dongyang Li. Effects of mo and b additives on hardness and the resistance of cu–ni alloy to wear, corrosion and corrosive wear. Metals and Materials International, 27:4911-4921, Jul 2021. URL: https://doi.org/10.1007/s12540-020-00801-x, doi:10.1007/s12540-020-00801-x. This article has 16 citations and is from a peer-reviewed journal.

2. (anene2019effectofdopant pages 1-3): Franklin Amaechi Anene, Nkem Emelike Nwankwo, and Victor Ugochukwu Nwoke. Effect of dopant and heat treatment on the microstructure and mechanical properties of nickel-aluminum bronze. Metallurgical and Materials Engineering, 25:147-162, Jul 2019. URL: https://doi.org/10.30544/423, doi:10.30544/423. This article has 8 citations.

3. (anene2019effectofdopant pages 3-13): Franklin Amaechi Anene, Nkem Emelike Nwankwo, and Victor Ugochukwu Nwoke. Effect of dopant and heat treatment on the microstructure and mechanical properties of nickel-aluminum bronze. Metallurgical and Materials Engineering, 25:147-162, Jul 2019. URL: https://doi.org/10.30544/423, doi:10.30544/423. This article has 8 citations.

4. (kozlova1973boundariesofthe pages 1-3): R. F. Kozlova, V. B. Rabkin, and N. V. Blinova. Boundaries of the single-phase side fields of the system mo-cu-ni in the solid state. Soviet Powder Metallurgy and Metal Ceramics, 12:140-144, Feb 1973. URL: https://doi.org/10.1007/bf00807778, doi:10.1007/bf00807778. This article has 8 citations.

5. (kozlova1973boundariesofthe pages 3-4): R. F. Kozlova, V. B. Rabkin, and N. V. Blinova. Boundaries of the single-phase side fields of the system mo-cu-ni in the solid state. Soviet Powder Metallurgy and Metal Ceramics, 12:140-144, Feb 1973. URL: https://doi.org/10.1007/bf00807778, doi:10.1007/bf00807778. This article has 8 citations.

6. (kozlova1973boundaryofthe pages 1-3): R. F. Kozlova, V. B. Rabkin, L. Ya. Losev, and E. F. Pashchenko. Boundary of the two-phase field of mo (ni, cu) and cu (ni, mo) solid solutions in the system mo-cu-ni. Soviet Powder Metallurgy and Metal Ceramics, 12:399-402, May 1973. URL: https://doi.org/10.1007/bf00791268, doi:10.1007/bf00791268. This article has 8 citations.

7. (hou2021effectsofmo pages 40-50): Runfang Hou, Ming-Wei Wu, Qingyang Li, Wei Li, Daolun L. Chen, and Dongyang Li. Effects of mo and b additives on hardness and the resistance of cu–ni alloy to wear, corrosion and corrosive wear. Metals and Materials International, 27:4911-4921, Jul 2021. URL: https://doi.org/10.1007/s12540-020-00801-x, doi:10.1007/s12540-020-00801-x. This article has 16 citations and is from a peer-reviewed journal.

8. (hou2021effectsofmo pages 81-89): Runfang Hou, Ming-Wei Wu, Qingyang Li, Wei Li, Daolun L. Chen, and Dongyang Li. Effects of mo and b additives on hardness and the resistance of cu–ni alloy to wear, corrosion and corrosive wear. Metals and Materials International, 27:4911-4921, Jul 2021. URL: https://doi.org/10.1007/s12540-020-00801-x, doi:10.1007/s12540-020-00801-x. This article has 16 citations and is from a peer-reviewed journal.

9. (anene2019effectofdopant pages 13-15): Franklin Amaechi Anene, Nkem Emelike Nwankwo, and Victor Ugochukwu Nwoke. Effect of dopant and heat treatment on the microstructure and mechanical properties of nickel-aluminum bronze. Metallurgical and Materials Engineering, 25:147-162, Jul 2019. URL: https://doi.org/10.30544/423, doi:10.30544/423. This article has 8 citations.

10. (din1993effectofresidual pages 4-7): A.M.Shams El Din. Effect of residual and minor constituents on the corrosion behaviour of some technically important alloys. Desalination, 93:487-498, Aug 1993. URL: https://doi.org/10.1016/0011-9164(93)80124-6, doi:10.1016/0011-9164(93)80124-6. This article has 3 citations and is from a domain leading peer-reviewed journal.

11. (mccright1988anannotatedhistory pages 58-60): R. D. McCright. An annotated history of container candidate material selection. ArXiv, Jul 1988. URL: https://doi.org/10.2172/60703, doi:10.2172/60703. This article has 11 citations.

12. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

13. (hou2021effectsofmo pages 33-40): Runfang Hou, Ming-Wei Wu, Qingyang Li, Wei Li, Daolun L. Chen, and Dongyang Li. Effects of mo and b additives on hardness and the resistance of cu–ni alloy to wear, corrosion and corrosive wear. Metals and Materials International, 27:4911-4921, Jul 2021. URL: https://doi.org/10.1007/s12540-020-00801-x, doi:10.1007/s12540-020-00801-x. This article has 16 citations and is from a peer-reviewed journal.

14. (hou2021effectsofmo media 37c817b0): Runfang Hou, Ming-Wei Wu, Qingyang Li, Wei Li, Daolun L. Chen, and Dongyang Li. Effects of mo and b additives on hardness and the resistance of cu–ni alloy to wear, corrosion and corrosive wear. Metals and Materials International, 27:4911-4921, Jul 2021. URL: https://doi.org/10.1007/s12540-020-00801-x, doi:10.1007/s12540-020-00801-x. This article has 16 citations and is from a peer-reviewed journal.

15. (wang2000phaseequilibriain pages 6-9): Cui Ping Wang, Xing Jun Liu, Ikuo Ohnuma, Ryosuke Kainuma, Kiyohito Ishida, and Shi Ming Hao. Phase equilibria in the cu-fe-mo and cu-fe-nb systems. Journal of Phase Equilibria, 21:54-62, Jan 2000. URL: https://doi.org/10.1361/105497100770340426, doi:10.1361/105497100770340426. This article has 50 citations.

16. (wang2000phaseequilibriain pages 3-5): Cui Ping Wang, Xing Jun Liu, Ikuo Ohnuma, Ryosuke Kainuma, Kiyohito Ishida, and Shi Ming Hao. Phase equilibria in the cu-fe-mo and cu-fe-nb systems. Journal of Phase Equilibria, 21:54-62, Jan 2000. URL: https://doi.org/10.1361/105497100770340426, doi:10.1361/105497100770340426. This article has 50 citations.

17. (wang2000phaseequilibriain pages 5-6): Cui Ping Wang, Xing Jun Liu, Ikuo Ohnuma, Ryosuke Kainuma, Kiyohito Ishida, and Shi Ming Hao. Phase equilibria in the cu-fe-mo and cu-fe-nb systems. Journal of Phase Equilibria, 21:54-62, Jan 2000. URL: https://doi.org/10.1361/105497100770340426, doi:10.1361/105497100770340426. This article has 50 citations.

18. (wang2000phaseequilibriain pages 2-3): Cui Ping Wang, Xing Jun Liu, Ikuo Ohnuma, Ryosuke Kainuma, Kiyohito Ishida, and Shi Ming Hao. Phase equilibria in the cu-fe-mo and cu-fe-nb systems. Journal of Phase Equilibria, 21:54-62, Jan 2000. URL: https://doi.org/10.1361/105497100770340426, doi:10.1361/105497100770340426. This article has 50 citations.

19. (nemani2024advancementsinadditive pages 1-2): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

20. (hyer2025strategiesforfabricating pages 23-26): Holden C. Hyer, Josh Kendall, Denise Adorno Lopes, and A. Nelson. Strategies for fabricating molybdenum structures using laser powder bed fusion. Unknown journal, Mar 2025. URL: https://doi.org/10.2172/3377998, doi:10.2172/3377998.

21. (kozlova1973boundaryofthe pages 3-4): R. F. Kozlova, V. B. Rabkin, L. Ya. Losev, and E. F. Pashchenko. Boundary of the two-phase field of mo (ni, cu) and cu (ni, mo) solid solutions in the system mo-cu-ni. Soviet Powder Metallurgy and Metal Ceramics, 12:399-402, May 1973. URL: https://doi.org/10.1007/bf00791268, doi:10.1007/bf00791268. This article has 8 citations.

22. (staff2022usgsminingreview pages 3-5): US Staff. Usgs mining review. Unknown journal, 2022.

23. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

24. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

25. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

26. (kodali2026toxicityofairborne pages 8-9): Vamsi K. Kodali, Aaron Erdely, and Patti C. Zeidler-Erdely. Toxicity of Airborne Metals. Elsevier, Jan 2026. URL: https://doi.org/10.1016/b978-0-323-95488-4.00102-9, doi:10.1016/b978-0-323-95488-4.00102-9. This article has 0 citations.
