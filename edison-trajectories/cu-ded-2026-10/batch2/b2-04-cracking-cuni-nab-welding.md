<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: f6ce3ed1-8e93-4230-bf0a-876adaa985dd
- Submitted: 2026-10-17T05:37:02Z
- Fetched: 2026-10-17T06:08:54Z (status: success)
- Raw trajectory JSON: ../raw/b2-04-cracking-cuni-nab-welding.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What causes solidification cracking, liquation cracking, and
ductility-dip cracking when Cu-Ni (90-10, 70-30) and nickel-aluminum bronze
are welded or deposited, and what does that imply for designing a DED
composition? Cover the effects of Ni content and freezing range, impurity
limits (S, P, Pb, Bi, Se, Te, C, Zn), deoxidizers and grain refiners in
filler metals (ERCuNi with Ti; ERCuNiAl; ERCuMnNiAl), heat input and
restraint, and any crack-susceptibility index (Kou's |dT/d(fs)^(1/2)|, CSC,
freezing-range indices) that has been validated on copper alloys. Include
DED or laser cladding studies that report cracking of Cu alloys and what
removed it.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What causes solidification cracking, liquation cracking, and
ductility-dip cracking when Cu-Ni (90-10, 70-30) and nickel-aluminum bronze
are welded or deposited, and what does that imply for designing a DED
composition? Cover the effects of Ni content and freezing range, impurity
limits (S, P, Pb, Bi, Se, Te, C, Zn), deoxidizers and grain refiners in
filler metals (ERCuNi with Ti; ERCuNiAl; ERCuMnNiAl), heat input and
restraint, and any crack-susceptibility index (Kou's |dT/d(fs)^(1/2)|, CSC,
freezing-range indices) that has been validated on copper alloys. Include
DED or laser cladding studies that report cracking of Cu alloys and what
removed it.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Cracking risks for single-stream copper-alloy DED

**Bottom line.** The strongest directly relevant evidence distinguishes three different problems: late-solidification cracking in a restrained deposit; remelting-related cracking at a dissimilar-material interface; and cracking during subsequent solid-state thermal cycles. They require different tests. Conventional wrought Cu–30Ni welding is generally reported to be limited more by *porosity* than cracking, whereas an industry source specifically warns that **cast** 70/30 Cu–Ni can hot-crack because of its larger freezing range. Neither observation establishes a monotonic relationship between 10 and 30 wt% Ni and DED crack susceptibility. (lancaster1999nonferrousmetals pages 12-15, robitz1990closuredevelopmentfor pages 17-20)

## Mechanisms and composition consequences

**Solidification cracking** starts in the fusion zone when contracting, restrained grains remain separated by poorly fed intergranular liquid near the end of freezing. Terminal-liquid segregation, grain morphology, dilution, and imposed strain matter as well as the bulk liquidus–solidus interval. In Cu–Ni, nominally continuous Cu–Ni solid solubility is therefore not a guarantee against cracking: cast 70/30 Cu–Ni was specifically identified as vulnerable because of its solidification range, and Cu–35Ni deposited onto 316L developed centerline hot cracks where excessive substrate melting introduced substantial Fe dilution. The latter is an *elemental-powder, steel-substrate* result, not proof that prealloyed Cu–Ni cracks on wrought Cu–Ni. For aluminum bronze, the welding evidence instead emphasizes phase constitution: a crack-sensitive, nominally single-phase Cu–Al–Fe weld deposit could be replaced by a virtually crack-free duplex filler containing approximately 10Al–2.5Fe–5Ni wt%; the source cautions that its cracking cannot simply be attributed to a broad intrinsic freezing range. **Design implication:** assess the *actual deposited and first-layer diluted compositions*, terminal liquid, and phase constitution, not Ni content or equilibrium freezing range alone. (giorjao2021newcompositionbased pages 1-2, robitz1990closuredevelopmentfor pages 17-20, lancaster1999nonferrousmetals pages 12-15, williams2025thefirstlayer pages 6-9, williams2025thefirstlayer media 5e43e90f)

**Liquation cracking** occurs beside a new melt pool when previously solid material develops an intergranular liquid film during reheating and is strained before that film heals. The closest retrieved NAB additive-manufacturing example is **NAB deposited onto 316L**, where liquid copper penetrated stainless-steel grain boundaries and cracks appeared in the *steel-side* heat-affected zone. Finer-grained steel, an Inconel 625 buffer, or a preliminary NAB laser-clad layer were suggested, **not demonstrated here as crack-removal treatments**. This is not direct evidence of the same mechanism in cast NAB or wrought Cu–Ni repair substrates. First-layer dilution and subsequent-pass reheating on *both proposed substrates* need their own sectioned-interface tests. (nemani2024advancementsinadditive pages 79-83)

**Ductility-dip cracking (DDC)** is solid-state intergranular fracture under tensile strain during a high-temperature ductility minimum; it should not be diagnosed from the presence of a crack alone. A fabrication report places a ductility dip near **1000 °F (about 538 °C) for CDA 613 aluminum bronze**, and another interviewee raises a possible DDC concern for its welding; neither supplies a demonstrated DDC temperature interval, crack micrograph, or quantitative threshold for C70600, C71500, or NAB. Repeated DED thermal cycles warrant hot-ductility testing and fracture-surface/EBSD distinction between a solid-state boundary and a resolidified liquid film. Do **not** transplant nickel-*superalloy* DDC thresholds to 10–30Ni Cu alloys. (robitz1990closuredevelopmentfor pages 17-20, lancaster1999nonferrousmetals pages 12-15)

**Trace elements and fillers.** Lancaster directly identifies excessive **Bi and Pb** as low-melting, hot-embrittling copper-alloy contaminants, but gives no allowable wt% or ppm threshold. The retrieved direct Cu–Ni/NAB evidence does **not** establish defensible independent crack-acceptance limits for **S, P, Se, Te, C, or Zn**; specifying numerical limits for them would overstate this search. Treat S, P, Pb, Bi, Se, and Te as separately assayed, controlled impurity candidates and experimentally test any asserted threshold. Keep C and Zn under compositional control rather than assigning them an unsupported shared mechanism: Zn volatilization is explicitly associated with *brass* welding and possible porosity; phosphorus-deoxidized *copper plate* is not evidence that P is an effective deoxidizer for Cu–Ni weld metal. Clean starting material and interpass oxide removal matter. Cu–Ni filler requires a deoxidizer to limit porosity; **Ti** is specifically identified as suitable. The retrieved texts do not supply verified ER**CuNi**, ER**CuNiAl**, or ER**CuMnNiAl** standard chemistry ranges or a comparative crack test among these three, so their names alone cannot establish optimal Ti, Al, Mn, or Ni additions. Use them as experimentally characterized filler *starting points*, not prevalidated prealloyed DED recipes; distinguish Ti used to deoxidize Cu–Ni from Ti demonstrated to refine *cast NAB* grains. (lancaster1999nonferrousmetals pages 12-15, robitz1990closuredevelopmentfor pages 17-20, rivero2021effectofti pages 5-6, rivero2021effectofti pages 3-5)

**Heat input and restraint.** Too little absorbed energy produces incomplete fusion or incompletely melted feed; too much can increase melt-pool size, substrate dilution, residual strain, gas porosity, and hot cracking. A fixed J/mm target cannot be ported between an 800-W elemental-blend single track on steel and a prealloyed NAB multilayer build. The C715 welding interviews report room-temperature preheat and, in one practice, **interpass below 350 °F (177 °C)** for sections up to **2 in.** thick; these are fabrication observations, not an established DED operating limit. Test thin and massive substrates and constrained repair geometries separately. (robitz1990closuredevelopmentfor pages 17-20, williams2025thefirstlayer pages 4-6, li2021nanotwinscontainingmicrostructureand pages 9-14)

## Direct studies and quantitative benchmarks

All compositions below are nominal **wt%** unless specified. *NR* means the cited study does not report the requested measurement; no corrosion outcome is inferred from strength or density. Tags denote **[CITE]** useful direct evidence, **[NUMBERS]** quantitative benchmark, **[NAVY]** documented naval application, **[NOVELTY-RISK]** overlap with the proposed work, and **[GAP]** a missing required demonstration.

1. **J. F. Lancaster, “Non-ferrous metals,” in *Metallurgy of Welding* (1999), pp. 197–223, DOI: 10.1007/978-94-010-9506-8_9.** *Process:* conventional fusion welding of wrought/fabricated copper alloys; Cu–Ni examples approximately **5, 10, 20, and 30Ni** and duplex aluminum-bronze filler nominally **10Al–2.5Fe–5Ni**. Matching single-phase aluminum-bronze multipass filler was crack-prone; duplex filler was described as virtually crack-free. Cu–Ni cracking was not considered a major routine problem, but deoxidized, including Ti-bearing, filler limited porosity; excess Pb/Bi caused hot embrittlement. *Conditions/numbers:* no quantitative crack threshold, powder, density, mechanical, or seawater test. **[CITE] [GAP]** The qualitative filler comparison does not rank ERCuNiAl against ERCuMnNiAl in laser DED. (lancaster1999nonferrousmetals pages 12-15)

2. **E. S. Robitz Jr., M. D. McAninch Jr., and D. Edmonds, *Closure Development for High-Level Nuclear Waste Containers for the Tuff Repository; Phase 1, Final Report* (1990), DOI: 10.2172/138043.** *Process:* industrial GTAW/GMAW/SMAW interviews concerning **CDA 715/C71500, nominal Cu–30Ni**, distinguishing cast and wrought products. Wrought material was welded successfully with matching **ECuNi** and room-temperature preheat; one fabricator welded sections up to **2 in.**, holding interpass below **350 °F**, and reported **porosity rather than cracks** as the main defect. A separate source warned that **cast** 70/30 Cu–Ni may hot-crack because of its large solidification range. Another cited **CDA 613**, not C71500, for a roughly **1000 °F** ductility dip. *Seawater, powder, hardness and crack-rate tests:* NR. **[CITE] [NUMBERS] [NAVY]** The report also documents CDA 613 structures made for the US Navy; that does not make the C715 cracking observation a Navy-funded DED result. **[GAP]** (robitz1990closuredevelopmentfor pages 17-20)

3. **B. Li, H. Zheng, C. Han, and K. Zhou, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39** (2021) 101825, DOI: 10.1016/j.addma.2020.101825.** *Process:* **blown-powder laser metal deposition**, single **gas-atomized prealloyed** NAB feed; measured powder **Cu–9.70Al–5.48Fe–4.47Ni**, balance Cu **80.35 wt%**. Powder **45–106 µm**, D10/D50/D90 **49.76/76.29/116.46 µm**; Hall flow and oxygen NR. Excessive laser power produced large hot cracks attributed to residual stress. The reported feasible, near-full-density window was **1000–1500 W, 0.5–1.5 m/min, 1.5–2 mm hatch**; **750 W** generated lack-of-fusion pores and **2 m/min** gas pores. Most optimized samples exceeded **99% relative density**, maximum **99.55%** at **1500 W, 1 m/min, 2 mm hatch**. As-printed yield **593–713 MPa**, UTS **769–949 MPa**, elongation generally **10–12%**. *Corrosion medium/duration, icorr, Ecorr, impedance, attack depth:* **NR—not seawater-qualified**. The substrate is not identified in the cited methods excerpt. **[CITE] [NUMBERS] [NOVELTY-RISK]** Prealloyed single-feed NAB laser DED and process-window development have already been demonstrated. **[GAP]** No matched C71500 seawater comparison or proposed cast-NAB/wrought-Cu–Ni repair qualification. (li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 24-29)

4. **N. Williams, K. Snyder, I. Smith, A. Duong, E. Carpenter, and R. Barua, “The First Layer: Single-Track Insights into Direct Energy Deposition Processed Cu–Ni Thermoelectric Alloys,” *Journal of Manufacturing and Materials Processing* **9** (2025) 170, DOI: 10.3390/jmmp9060170.** *Process:* **blown-powder laser DED** of **physically mixed elemental** Cu and Ni, nominal **Cu–35Ni**, onto **316L stainless steel**; not single prealloyed feed and outside the proposed 10–30Ni range. Powder mean diameter **57 ± 15 µm**, apparent/bulk and tap densities **4.74/5.20 g cm⁻³**, Hall flow **0.3 g s⁻¹**, Hausner ratio **1.10**; powder oxygen NR. At **800 W** and material loading **0.011 g/mm**, complete substrate penetration/Fe dilution accompanied centerline hot cracks across tested linear heat inputs. At **0.016 g/mm and 67 J/mm**, the authors observed a roughly **500-µm-high** uniform track with about **100 µm** substrate penetration and minimal Fe dilution. At **0.021 g/mm and 137 J/mm**, cracks recurred; insufficient energy also left roughly **50-µm** unmelted Ni inclusions. *Multilayer density, strength, corrosion and crack-free repair:* NR. The track evidence is illustrated in the paper’s cropped Figure 4(a,b). **[CITE] [NUMBERS] [NOVELTY-RISK]** Cu–Ni DED itself is not new. **[GAP]** It does not establish that increasing mass input removes cracks in prealloyed Cu–Ni deposited on Cu alloys. (williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 4-6, williams2025thefirstlayer pages 6-9, williams2025thefirstlayer media 5e43e90f)

5. **P. J. Rivero, C. Berlanga, J. F. Palacio, and M. V. Biezma-Moraleda, “Effect of Ti on Microstructure, Mechanical Properties and Corrosion Behavior of a Nickel-Aluminum Bronze Alloy,” *Materials Research* **24** (2021), DOI: 10.1590/1980-5373-mr-2020-0335.** *Process:* **sand cast** CuAl10Fe5Ni5/C95500, Ti-free versus **120 ppm Ti**. Ti refined ASTM grain number **6.7 ± 0.3 → 8.9 ± 0.4** and increased microhardness **172.89 → 206.89 HV**. *Corrosion:* **static 3.5 wt% NaCl, room temperature, 720 h**, mass loss **0.034% versus 0.020%**, a **statistically nonsignificant** difference; electrochemical corrosion rates **0.021 versus 0.023 mm/year**, OCP **−150 versus −148 mV against Ag/AgCl**. Polarization followed approximately **1 h** OCP stabilization; icorr and selective-attack depth were not established in the retrieved excerpt. **No cracking-removal experiment.** **[CITE] [NUMBERS] [GAP]** A grain refiner is not automatically a crack remedy or a C715-equivalent seawater alloy. (rivero2021effectofti pages 1-2, rivero2021effectofti pages 2-3, rivero2021effectofti pages 5-6, rivero2021effectofti pages 3-5, rivero2021effectofti pages 6-8)

6. **C. Dharmendra, S. Shakerin, G. D. J. Ram, and M. Mohammadi, “Wire-arc additive manufacturing of nickel aluminum bronze/stainless steel hybrid parts—Interfacial characterization, prospects, and problems,” *Materialia* **13** (2020) 100834; and C. Dharmendra, S. Shakerin, and M. Mohammadi, “Metallurgical Assessment of Additive Manufactured Nickel Aluminum Bronze–316L Stainless Steel Bimetallic Structure: Effect of Deposit Geometry on the Interfacial Characteristics and Cracking,” *Journal of Materials Engineering and Performance* **30** (2021) 8746–8762, DOI: **10.1007/s11665-021-06194-1**.** *Process:* **wire-arc DED/WAAM**, nominal **Cu–9Al–4Ni–4Fe–1Mn** on **316L**. Intergranular substrate-side cracking was attributed to liquid-Cu penetration; the comparison reported **114 A and 170 J/mm**. Inconel buffering, finer substrate grains and laser-clad buttering were **suggestions**. DOI for the *Materialia* article was not verified in the retrieved excerpts and is deliberately not invented. *Corrosion, powder and comparable density:* NR. **[CITE] [NUMBERS] [GAP]** It establishes a substrate-specific liquation hazard, not proven cast-NAB repair liquation. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 112-113)

7. **A. Chiocca, F. Soulié, F. Deschaux-Beaume, and C. Bordreuil, “Study of the effect of growth kinetic and nucleation law on grain structure simulation during gas tungsten arc welding of Cu–Ni plate,” *Welding in the World* **63** (2019) 887–901, DOI: 10.1007/s40194-019-00717-0.** *Process:* **GTAW wrought Cu30Ni plate** (the excerpt does not independently verify that “30” is a measured wt%); finite-element weld heat flow coupled to Scheil-type solid fraction and grain-growth modeling. Model inputs include approximately **1200 °C solidus** and **1250 °C liquidus**, i.e. about **50 °C** for the modeled material—not a measured cross-alloy hot-cracking ranking. Pool geometry and grain structure were compared with experiments; **observed cracks and crack-index validation were not reported**. *Corrosion and powder:* not applicable/NR. **[CITE] [NUMBERS] [GAP]** Heat-flow-coupled solidification is precedent; its direct Cu–Ni crack-prediction validation remains a gap. (chiocca2019studyofthe pages 4-6, chiocca2019studyofthe pages 1-3, chiocca2019studyofthe pages 6-8, chiocca2019studyofthe pages 12-14)

## Crack-susceptibility indices: usable hypotheses, not copper validation

**A. M. Jordan and Q. Zhang, “Evaluating Thermodynamics-Based Hot-Cracking Models for Various AM Alloys,” *Integrating Materials and Manufacturing Innovation* (2026), DOI: 10.1007/s40192-025-00437-y**, compares Scheil-derived **Kou CSI** (late-stage maximum \(|dT/d\sqrt{f_s}|\)), **Clyne–Davies CSC** \((t_{0.99}-t_{0.9})/(t_{0.9}-t_{0.4})\), and solidification-range-based alternatives. Its PBF compilation contained **460 alloys from 128 sources**, but the evaluated families were Al, steels, Ni superalloys and high-entropy alloys—**not a validated Cu–Ni/NAB subset**. Reported recommended-family balanced accuracies were approximately **70.3% Al, 87.5% stainless steel, 65.3% other steels, 57.6% Ni superalloys, and 62.2% high-entropy alloys**; these must **not** be presented as copper performance. The author explicitly notes that terminal-solid-fraction bounds are alloy-dependent. Classical CSC also assumes a cooling-time history; substituting a measured/modelled DED heat-flow history is a plausible *testable improvement*, not an established success. **[CITE] [NUMBERS] [GAP]** (jordan2026acomprehensivehot pages 39-44, jordan2026acomprehensivehot pages 44-49, jordan2026acomprehensivehot pages 49-54, jordan2026acomprehensivehot pages 71-76)

For the proposed composition search, record liquidus, equilibrium and Scheil solidus or *specified* high-solid-fraction temperatures, late-liquid fraction, Kou index and CSC under the **same declared thermal-history assumption**. Then compare these predictors against blinded, location-resolved cracks in single tracks, constrained multilayer deposits, and both repair interfaces. A simple overall freezing interval can miss impurity-driven terminal films and NAB phase effects; none of these indices alone predicts liquation, DDC, powder porosity, or seawater corrosion. Direct copper-alloy discrimination and absolute acceptance thresholds remain **unvalidated in the retrieved literature**. (lancaster1999nonferrousmetals pages 12-15, giorjao2021newcompositionbased pages 1-2, jordan2026acomprehensivehot pages 44-49, jordan2026acomprehensivehot pages 49-54, chiocca2019studyofthe pages 4-6)

**Boundary of the evidence.** I did not verify a study that simultaneously demonstrates *one newly designed prealloyed powder*, crack-free self-build and repair on **both cast NAB and wrought Cu–Ni**, and **as-deposited** corrosion at least as good as a side-by-side wrought C71500 control in specified natural or ASTM D1141 seawater, including exposure duration and flow. The directly quantified corrosion example above is **720 h static 3.5% NaCl on a casting**, not that test. I also did not verify copper-specific Kou/CSC validation, impurity-by-impurity ppm crack limits, or a direct three-way ER-filler crack comparison. These are material proposal gaps, not grounds for claiming the alloys already meet the seawater target. (rivero2021effectofti pages 5-6, rivero2021effectofti pages 6-8, li2021nanotwinscontainingmicrostructureand pages 1-4, nemani2024advancementsinadditive pages 79-83, jordan2026acomprehensivehot pages 91-97)

## Top 5 things the PI should know

1. **Demonstrate the missing combined endpoint:** prealloyed single-feed powder → crack-free self-build **and both repairs** → as-deposited, matched-condition C71500 seawater comparison. Density or 3.5% NaCl polarization alone cannot establish it. (li2021nanotwinscontainingmicrostructureand pages 24-29, rivero2021effectofti pages 5-6, nemani2024advancementsinadditive pages 79-83)
2. **Do not assume more Ni means fewer cracks.** Distinguish wrought from cast 70/30, assess actual Fe/Mn/Cr/Al and substrate dilution, and measure terminal solidification across the 10–30Ni design space. (robitz1990closuredevelopmentfor pages 17-20, lancaster1999nonferrousmetals pages 12-15, williams2025thefirstlayer pages 6-9)
3. **Separate the three cracking labels experimentally.** Fusion-zone interdendritic cracks, partially melted/penetrated HAZ boundaries, and solid-state DDC imply different alloy and process remedies. (giorjao2021newcompositionbased pages 1-2, nemani2024advancementsinadditive pages 79-83, robitz1990closuredevelopmentfor pages 17-20)
4. **Prealloyed NAB laser DED and crack-avoiding parameter windows are prior art.** Li and coauthors already report **99.55% density** and strong as-printed Cu–9Al–5Fe–5Ni; novelty must lie in comparative, cross-substrate *composition–powder–process–seawater* qualification rather than NAB printability alone. (li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 24-29, li2021nanotwinscontainingmicrostructureand pages 4-9)
5. **Present Kou/CSC and heat-flow-coupled CALPHAD as prospective copper predictors requiring validation**, while assaying low-melting impurities and controlling deoxidation/oxygen. No copper-specific predictive accuracy or defensible universal trace-element ppm limit was established here. (jordan2026acomprehensivehot pages 44-49, jordan2026acomprehensivehot pages 49-54, lancaster1999nonferrousmetals pages 12-15, jordan2026acomprehensivehot pages 91-97)

References

1. (lancaster1999nonferrousmetals pages 12-15): J. F. Lancaster. Non-ferrous metals. ArXiv, pages 197-223, Jan 1999. URL: https://doi.org/10.1007/978-94-010-9506-8\_9, doi:10.1007/978-94-010-9506-8\_9. This article has 7 citations.

2. (robitz1990closuredevelopmentfor pages 17-20): Closure development for high-level nuclear waste containers for the tuff repository; Phase 1, Final report This article has 2 citations.

3. (giorjao2021newcompositionbased pages 1-2): Rafael Giorjao, Benjamin Sutton, and Antonio Ramirez. New composition based technique for solidification cracking resistance evaluation. Metallurgical and Materials Transactions A, 52:2512-2521, Apr 2021. URL: https://doi.org/10.1007/s11661-021-06244-2, doi:10.1007/s11661-021-06244-2. This article has 25 citations.

4. (williams2025thefirstlayer pages 6-9): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

5. (williams2025thefirstlayer media 5e43e90f): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

6. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

7. (rivero2021effectofti pages 5-6): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

8. (rivero2021effectofti pages 3-5): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

9. (williams2025thefirstlayer pages 4-6): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

10. (li2021nanotwinscontainingmicrostructureand pages 9-14): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

11. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

12. (li2021nanotwinscontainingmicrostructureand pages 24-29): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

13. (williams2025thefirstlayer pages 2-4): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

14. (rivero2021effectofti pages 1-2): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

15. (rivero2021effectofti pages 2-3): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

16. (rivero2021effectofti pages 6-8): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

17. (nemani2024advancementsinadditive pages 112-113): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

18. (chiocca2019studyofthe pages 4-6): A. Chiocca, F. Soulié, F. Deschaux-Beaume, and C. Bordreuil. Study of the effect of growth kinetic and nucleation law on grain structure simulation during gas tungsten arc welding of cu-ni plate. Welding in the World, 63:887-901, Mar 2019. URL: https://doi.org/10.1007/s40194-019-00717-0, doi:10.1007/s40194-019-00717-0. This article has 4 citations and is from a domain leading peer-reviewed journal.

19. (chiocca2019studyofthe pages 1-3): A. Chiocca, F. Soulié, F. Deschaux-Beaume, and C. Bordreuil. Study of the effect of growth kinetic and nucleation law on grain structure simulation during gas tungsten arc welding of cu-ni plate. Welding in the World, 63:887-901, Mar 2019. URL: https://doi.org/10.1007/s40194-019-00717-0, doi:10.1007/s40194-019-00717-0. This article has 4 citations and is from a domain leading peer-reviewed journal.

20. (chiocca2019studyofthe pages 6-8): A. Chiocca, F. Soulié, F. Deschaux-Beaume, and C. Bordreuil. Study of the effect of growth kinetic and nucleation law on grain structure simulation during gas tungsten arc welding of cu-ni plate. Welding in the World, 63:887-901, Mar 2019. URL: https://doi.org/10.1007/s40194-019-00717-0, doi:10.1007/s40194-019-00717-0. This article has 4 citations and is from a domain leading peer-reviewed journal.

21. (chiocca2019studyofthe pages 12-14): A. Chiocca, F. Soulié, F. Deschaux-Beaume, and C. Bordreuil. Study of the effect of growth kinetic and nucleation law on grain structure simulation during gas tungsten arc welding of cu-ni plate. Welding in the World, 63:887-901, Mar 2019. URL: https://doi.org/10.1007/s40194-019-00717-0, doi:10.1007/s40194-019-00717-0. This article has 4 citations and is from a domain leading peer-reviewed journal.

22. (jordan2026acomprehensivehot pages 39-44): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

23. (jordan2026acomprehensivehot pages 44-49): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

24. (jordan2026acomprehensivehot pages 49-54): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

25. (jordan2026acomprehensivehot pages 71-76): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

26. (li2021nanotwinscontainingmicrostructureand pages 1-4): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

27. (jordan2026acomprehensivehot pages 91-97): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.
