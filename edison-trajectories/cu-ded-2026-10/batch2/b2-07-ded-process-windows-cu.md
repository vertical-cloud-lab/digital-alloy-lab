<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: 13cc8d3b-4e30-4dc6-bec3-efefaee291fc
- Submitted: 2026-10-17T05:37:04Z
- Fetched: 2026-10-17T06:08:57Z (status: success)
- Raw trajectory JSON: ../raw/b2-07-ded-process-windows-cu.json.gz
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

QUESTION: What process windows have been reported for blown-powder laser DED
of copper and copper alloys (pure Cu, CuCrZr, Cu-Sn bronzes, Cu-Ni, NAB,
GRCop-42/84), and what limits them? Give laser power, spot size, travel
speed, powder feed rate, layer height, and the resulting porosity, powder
catchment efficiency, dilution and build rate. Compare infrared (~1070 nm)
with blue (~450 nm) or green lasers for copper DED, and report preheating
and substrate effects (copper vs steel substrates). Which porosity mechanisms
(gas, keyhole, lack of fusion, evaporation of Zn/Mn) dominate for copper
alloys in DED?

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

QUESTION: What process windows have been reported for blown-powder laser DED
of copper and copper alloys (pure Cu, CuCrZr, Cu-Sn bronzes, Cu-Ni, NAB,
GRCop-42/84), and what limits them? Give laser power, spot size, travel
speed, powder feed rate, layer height, and the resulting porosity, powder
catchment efficiency, dilution and build rate. Compare infrared (~1070 nm)
with blue (~450 nm) or green lasers for copper DED, and report preheating
and substrate effects (copper vs steel substrates). Which porosity mechanisms
(gas, keyhole, lack of fusion, evaporation of Zn/Mn) dominate for copper
alloys in DED?

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


# Reported copper-alloy powder-laser DED windows

**Scope and comparability.** The directly relevant evidence is uneven: quantitative blown-powder DED data are strongest for pure Cu and one nickel–aluminum bronze (NAB). A reported *single-track window* is not necessarily a sound multilayer-build window. “Building efficiency,” powder catchment, and the fraction of laser power used for melting are different quantities and must not be interchanged. None of the process studies below establishes seawater performance equivalent to wrought C71500. Unless specified, the cited process studies did **not** report a corrosion electrolyte, exposure duration, corrosion current, corrosion potential, impedance, or selective-attack depth. Likewise, a dash below means the requested measurement was not established by the accessible evidence—not that its value was zero. (yamaguchi2024influenceofthe pages 4-5, li2021nanotwinscontainingmicrostructureand pages 4-9, nemani2024advancementsinadditive pages 102-105)

## Primary quantitative process benchmarks

1. **Pure Cu, green laser; exceptionally clear substrate comparison.** H. Siva Prasad, F. Brueckner, J. Volpp and A. F. H. Kaplan, “Laser metal deposition of copper on diverse metals using green laser sources,” *International Journal of Advanced Manufacturing Technology* **107** (2020), 1559–1568. **DOI: 10.1007/s00170-020-05117-z.** **Process:** coaxial blown-powder laser metal deposition (LMD), 515 nm. **Composition:** 99.9 wt% Cu feed; copper, aluminum, tool-steel and Ti–6Al–4V substrates. **Window:** 200–1000 W available, **1.7-mm spot**, 0.1–0.5 m/min travel, 0.65–3.9 g/min powder, **50–90-µm powder**. The minimum tested conditions giving clads differed sharply: Cu substrate **1000 W, 0.1 m/min, 1.3 g/min**; Al **600 W, 0.5 m/min, 1.3 g/min**; tool steel **200 W, 0.5 m/min, 2.6 g/min**; Ti alloy **200 W, 0.5 m/min, 3.9 g/min**. No prescribed layer height, mass catchment percentage, bulk porosity percentage or build-rate benchmark was reported in the cited passages. **[CITE] [NUMBERS] [GAP]** (prasad2020lasermetaldeposition pages 3-4)

   At the *same* 1000 W, 0.5 m/min and 1.3 g/min, Cu-on-Cu yielded a **1.04-mm-wide, 0.26-mm-high** track, **0-mm substrate melting and 0% geometrical dilution**; Cu-on-tool-steel yielded **2.34-mm width, 0.14-mm height, 0.382-mm substrate melting and 77.5% dilution**. The corresponding *estimated minimum fractions of incident laser power used solely for melting* were **0.73%** and **5.15%**, respectively; copper-on-aluminum and copper-on-titanium were **2.94%** and **9.78%**. The article’s abstract gives **5.95% for steel**, whereas its numerical Table 4 gives **5.15%**: retain that discrepancy rather than treating either figure as powder efficiency. A copper wall yielded **2.66%** by the same heat-accounting approach. At the common settings, copper-on-copper had a small, discontinuous pool and visible porosity, while steel exhibited severe dilution and, in one configuration, longitudinal cracking; raising powder feed reduced substrate mixing and removed the observed steel-side cracking. Preheating was *recommended* to stabilize the copper pool, not demonstrated here as a quantified paired improvement. **[NUMBERS] [GAP]** (prasad2020lasermetaldeposition pages 1-3, prasad2020lasermetaldeposition pages 3-4, prasad2020lasermetaldeposition pages 7-9)

2. **Pure Cu, blue laser; quantified pore–efficiency–dilution trade-off.** M. Yamaguchi, N. Kato, Y. Funada, T. Yachi, A. Saikai and T. Furumoto, “Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser,” *International Journal of Advanced Manufacturing Technology* **135** (2024), 5235–5251. **DOI: 10.1007/s00170-024-14789-w.** **Process:** blown-powder blue-laser DED, **445 nm**, Cu on AISI 304 steel. **Composition:** pure Cu feed; powder **D10/D50/D90 = 31/46/71 µm**. **Settings:** **0.2-mm laser spot**, **10 mm/s**, single-layer 90–270 W at **20 mg/s = 1.2 g/min**; multilayer 150–240 W at **10–20 mg/s = 0.6–1.2 g/min**, four layers, hatch 0.3–0.4 mm. Good single-layer finish occurred at **150–180 W** and **0.4–0.5-mm hatch**. **No nominal Z-increment/layer height is established**; hatch is lateral spacing, not spot size or layer height. **[CITE] [NUMBERS]** (yamaguchi2024influenceofthe pages 2-4, yamaguchi2024influenceofthe pages 5-7, yamaguchi2024influenceofthe pages 4-5)

   At **20 mg/s**, increasing power from **150 to 240 W** reduced measured area porosity **0.7% → 0.3%**, increased reported building efficiency **21% → 32%**, but increased steel dilution. At **180 W**, reducing feed from **20 to 10 mg/s** reduced porosity **0.4% → 0.1%** and increased building efficiency **28% → 36%**; conversely **180 W/20 mg/s** gave the preferred compositional separation, reaching **99.0 wt% Cu 200 µm above the interface**. These are measurements on *different selected geometries/hatches*, not an isolated two-factor comparison across all settings. The paper defines building efficiency using **deposited volume divided by powder supplied as an equivalent volume**; it does not independently measure particle-by-particle catchment. Fe, Cr and Ni can still enter the deposit from steel, and Cr-rich oxides were observed. **[NUMBERS] [GAP]** (yamaguchi2024influenceofthe pages 4-5, yamaguchi2024influenceofthe pages 13-15, yamaguchi2024influenceofthe pages 12-13, yamaguchi2024influenceofthe pages 10-12)

3. **NAB, pre-alloyed powder: the closest direct novelty precedent.** B. Li, H. Zheng, C. Han and K. Zhou, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39** (2021), 101825. **DOI: 10.1016/j.addma.2020.101825.** **Process:** blown-powder LMD; **nominal wt% Cu–9Al–5Fe–5Ni**; measured powder wt% **Cu 80.35 ± 0.91, Al 9.70 ± 0.89, Fe 5.48 ± 0.86, Ni 4.47 ± 0.60**. Gas-atomized spherical feed was sold as **45–106 µm**, with measured **D10/D50/D90 49.76/76.29/116.46 µm**. A continuous disk laser with **2-mm spot** was screened over **500–2250 W** and **0.25–2 m/min**; good single tracks appeared approximately **750–1750 W, 0.25–2 m/min**, whereas the reported >99%-dense multilayer window was **1000–1500 W**, approximately **0.5–1.5 m/min**, **1.5–2-mm hatch**. **1500 W, 1 m/min, 2-mm hatch** gave the maximum measured **99.55% relative density**, or approximately **0.45% residual porosity**. The highest reported *single-track volumetric building rate* was **31 mm³/s** under high-power screening; it should **not** be attributed specifically to the 99.55%-dense specimen. The quoted **32 g/min is helium carrier-gas flow, not powder feed**; powder mass feed, powder mass catchment, nominal layer height, oxygen and Hall flow were not established in the accessible methods. **[CITE] [NUMBERS] [NAVY: marine-propeller application, not verified Navy funding] [NOVELTY-RISK: pre-alloyed, dense NAB powder-LMD already demonstrated]** (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand media 36bae893)

   The as-deposited material contained β*-type martensite, Widmanstätten α, Fe₃Al/NiAl precipitates and nanotwins. Reported yield strength was **593–713 MPa**, UTS **769–949 MPa** and elongation **10–12%**. **Gas pores predominated in seven of eight examined parameter sets**; at **750 W, 1 m/min, 1.5-mm hatch**, unmelted-powder-associated *lack-of-fusion* pores predominated and caused delamination. Excessive power caused hot cracks in single tracks; **2250 W** caused sputtering and lower building rate. **No seawater exposure or corrosion current was measured**: excellent strength is not evidence of meeting the C71500 corrosion target. **[NUMBERS] [NOVELTY-RISK] [GAP]** (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9)

4. **Cu–Sn bronze: a usable LDED starting setting, not a marine qualification.** V. T. P. Nguyen, *Functionally Magnetic Gradient Copper–Nickel Material Fabricated via Directed Energy Deposition* (West Virginia University thesis, 2022). **DOI: 10.33915/etd.11213.** **Process actually tested in the relevant chapters:** powder-laser DED of **CuSn10, nominal Cu–10 wt% Sn**, combined with Inconel 718 as a graded/multimaterial structure on **316L steel**; this is **not** a 70–30 Cu–Ni powder repair. CuSn10 parameter screening included **600–900 W**, **9–11 mm/s** and **6–12 g/min**; the selected bronze setting was **700 W, 10 mm/s, 6 g/min**, with **0.54-mm reported layer thickness**. For comparison the Inconel region used **900 W, 10 mm/s, 5 g/min**. Porosity was observed in both regions and described as gas trapping, but no trustworthy numeric bronze-only porosity, catchment, dilution, marine corrosion or build rate could be extracted. Laser spot and lot oxygen/flow were likewise not established here. **[CITE] [NUMBERS] [GAP]** (nguyen2022functionallymagneticgradient pages 28-32, nguyen2022functionallymagneticgradient pages 39-45, nguyen2022functionallymagneticgradient pages 21-28)

   M. E. Balkan, E. Aydoğan, M. Işık, B. Derin and B. Koç, “Directed energy deposition process development for functionally gradient Copper–Inconel 718 materials,” *Journal of Additive Manufacturing Technologies* (2021). **DOI: 10.18416/jamtech.2111581.** **Process:** powder DED of **CuSn10/IN718**, including two powder hoppers and a C45 steel substrate. CuSn10 powder was **63–160 µm**; an optimized *volumetric-energy-input calculation* was **122.18 J/mm³**, versus **71.42 J/mm³** for IN718. Those values alone do **not** specify transferable laser power, spot, catchment, pore fraction, seawater resistance or single-pre-alloyed Cu–Ni processing. **[CITE] [NUMBERS] [GAP]** (balkan2021directedenergydeposition pages 2-3)

5. **GRCop-42: infrared feasibility is established, not a marine-alloy process window.** A. Fadhel, N. W. Zuckschwerdt, A. Deshwal, S. Bose, A. Bandyopadhyay and J. Doppa, “Discovery of Feasible 3D Printing Configurations for Metal Alloys via AI-Driven Adaptive Experimental Design,” *Proceedings of the AAAI Conference on Artificial Intelligence* **40** (2026), 39939–39948. **DOI: 10.1609/aaai.v40i47.41428.** **Process:** infrared fiber-laser powder DED, **GRCop-42 = Cu–4 at% Cr–2 at% Nb** (approximately **Cu–3.2 wt% Cr–3.0 wt% Nb**, calculated from the atomic composition), with IN718 transition material on a 316L build plate; **not** single-stream Cu-alloy-on-NAB repair. Powder was **15–53 µm**; argon atmosphere was usually **<20 ppm O₂**—a *chamber specification, not measured powder oxygen*. Feasible specimen settings included **950 W, 750 mm/min, 0.20-mm layer height**; **700 W, 1600 mm/min, 0.11 mm**; **600 W, 1550 mm/min, 0.17 mm**; and **500 W, 250 mm/min, 0.30 mm**. Feed is tabulated in **powder-feeder RPM**, not g/min, so a powder-mass rate or catchment cannot responsibly be inferred. Spot diameter, quantitative pore fraction, dilution and volumetric build rate were not established. “Defect-free” describes inspected, machinable test blocks/cylinders and a visually sound transition, **not** a reported CT-verified zero-porosity fraction. **[CITE] [NUMBERS] [NOVELTY-RISK: AI-guided DED parameter discovery exists, but this is not linked powder/composition/seawater optimization] [GAP]** (fadhel2026discoveryoffeasible pages 5-6, fadhel2026discoveryoffeasible pages 6-8, fadhel2026discoveryoffeasible pages 2-3)

   P. R. Gradl, T. W. Teasley, C. S. Protz, M. B. Garcia, D. Ellis and C. Kantzos, “Advancing GRCop-based Bimetallic Additive Manufacturing to Optimize Component Design and Applications for Liquid Rocket Engines,” *AIAA Propulsion and Energy 2021 Forum* (2021). **DOI: 10.2514/6.2021-3231.** **Processes must be separated:** laser powder DED deposited *superalloys* onto previously **LPBF-made GRCop-42**; a Cu–Ni interlayer was explored for an HR-1 jacket; the cited GRCop-84 jacket demonstration involved **electron-beam wire DED**, not evidence of a quantified blown-powder GRCop-84-on-itself window. No comparable GRCop-42-versus-84 powder-feed, spot, layer, catchment, dilution or porosity dataset is available from this citation. **[CITE] [GAP] [NAVY: no; NASA rocket application]** (gradl2021advancinggrcopbasedbimetallic pages 8-11)

6. **CuCrZr and Cu–Ni: named literature is not a validated table of settings.** A. V. Nemani, M. Ghaffari, K. S. Bokati, N. Valizade, E. Afshari and A. Nasiri, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* **8** (2024), 54. **DOI: 10.3390/jmmp8020054.** **Process:** review distinguishing LPBF, powder LDED and WAAM. It reports that insufficient LDED Cu–Ni energy at higher travel speeds damages track soundness; it also flags sparse Cu–Ni processability/corrosion evidence. Search results identify CuCrZr powder-DED optimization papers, but their primary numerical settings and resulting densities were not accessible here: **do not mislabel a 532-nm CuCr1Zr LPBF result—125 W, 400 mm/s, 99.6% density—as blown-powder DED**. Nor do compositional-gradient Cu/Ni studies establish a **single pre-alloyed Cu–10–30 wt% Ni–Fe–Mn–Cr** powder, deposited both on itself and wrought C71500 and then seawater-tested without heat treatment. **[CITE] [GAP] [NOVELTY-RISK: previous graded Cu–Ni DED exists, but does not establish this exact product-and-test combination]** (canacoo2026laseradditivemanufacturing pages 15-17, nemani2024advancementsinadditive pages 105-106, nemani2024advancementsinadditive pages 102-105)

   A pertinent **near miss** for repair is the review’s account of laser-powder-DED **CuNi2SiCr**, approximately Cu–2 wt% Ni with Si/Cr additions, deposited on *cast NAB*: porosity and a soft single-α-phase deposit led the investigators to advise **against** its use for propeller repair. This is neither 10–30 wt% Ni seawater-grade Cu–Ni nor dense pre-alloyed NAB repair; the accessible account gives no reliable pore percentage, hardness or immersion result to transfer. **[NAVY: propeller application, not verified funding] [NOVELTY-RISK: powder-on-NAB repair has been attempted] [GAP]** (nemani2024advancementsinadditive pages 79-83)

## Wavelength, substrate, and defect interpretation

**Infrared versus visible light.** Near-IR (~1070 nm) couples poorly into clean solid Cu: Prasad and colleagues cite **approximately 4% absorptance at 1085 nm versus 54.5% at 525 nm** for reference surfaces. This helps explain why visible sources more readily establish a conduction-mode pool, but **wavelength is not itself a process prescription**: power, beam diameter, initial surface, substrate heat sinking, overlapping tracks, oxide and powder interception all matter. The green Cu-on-Cu example needed **1000 W with a 1.7-mm spot**, while blue Cu-on-steel produced **0.1% porosity at 180 W with a 0.2-mm spot**—different substrates and irradiances, **not** a controlled head-to-head energy-saving measurement. Likewise, 532-nm CuCrZr LPBF density and LPBF keyhole thresholds cannot be imported as DED specifications. Blue/IR hybrid Cu-on-steel observations suggest blue light controls pool width while a focused IR beam strongly increases penetration/keyhole depth, underscoring the dilution hazard at repair interfaces. **[CITE] [NUMBERS] [GAP: no same-machine, same-spot, same-alloy three-wavelength blown-powder comparison established]** (canacoo2026laseradditivemanufacturing pages 17-19, canacoo2026laseradditivemanufacturing pages 8-9, prasad2020lasermetaldeposition pages 1-3, prasad2020lasermetaldeposition pages 3-4)

**Preheat and the actual repair substrate.** The green-laser study found that Cu’s heat extraction made its pool smaller and less continuous than steel’s; on steel, the opposite problem was deep substrate melting, up to **77.5% single-track geometrical dilution** under the specified common condition. Copper workpiece/track buildup reduced the estimated melting-energy deficit (**0.73% first Cu track versus 2.66% Cu wall**). Preheating to improve wetting and pool continuity is physically plausible and explicitly recommended, but the accessible studies do not furnish a defensible paired **temperature-versus-density-versus-catchment** curve for copper powder DED; **cast NAB and wrought Cu–Ni substrates cannot be assumed to behave like either pure Cu or tool steel**. Both interface composition and first-layer pore/crack inspection therefore need separate optimization. **[NUMBERS] [GAP]** (prasad2020lasermetaldeposition pages 3-4, prasad2020lasermetaldeposition pages 7-9)

**Which pores dominate?** The direct NAB powder-LMD evidence is unusually specific: **gas entrapment dominates across its successfully built parameter sets; low-power lack of fusion dominates the unsuccessful 750-W set**. Yamaguchi’s lower-power pure-Cu specimens exhibited pores associated with insufficient fusion and possible shielding/carrier-gas entrapment; increasing power/remelting lowered pores but increased steel dilution and generated detectable Cr oxide. Keyhole collapse is a credible *high-irradiance* risk, and green CuCrZr **LPBF** reports vaporization/keyholes beyond roughly 150 W, but this does **not** show that keyholes dominate the cited NAB powder-DED builds. **Zn evaporation cannot be invoked as the main mechanism in Zn-free pure Cu, CuSn10, Cu–Ni or nominal Cu–Al–Ni–Fe NAB; Mn evaporation is an alloy-dependent possibility, not a demonstrated dominant source of pores in these DED data.** Quantify powder-versus-deposit Zn/Mn/O, pore morphology/chemistry and thermal conditions before asserting evaporation-driven porosity. **[CITE] [NUMBERS] [GAP]** (yamaguchi2024influenceofthe pages 8-10, canacoo2026laseradditivemanufacturing pages 15-17, yamaguchi2024influenceofthe pages 10-12, li2021nanotwinscontainingmicrostructureand pages 9-14)

**Seawater benchmark discipline.** The LMD NAB paper measures tensile behavior, *not* seawater corrosion. Separately, Nemani *et al.* describe **LPBF**, rather than DED, NAB with a roughly **one-order-of-magnitude lower 3- and 6-month seawater immersion mass loss** in an as-printed martensitic microstructure than in cast/wrought NAB; this cannot establish Cu–Ni C71500 equivalence or predict LMD NAB corrosion. The sources assembled here do not provide matched **as-deposited powder-DED alloy versus wrought C71500** polarization, impedance, 30-day immersion, flow and selective-attack data in the same medium. Do not equate **3.5 wt% NaCl**, ASTM D1141 substitute seawater and natural flowing seawater or treat a rapid polarization current as a 30-day loss rate. **[CITE] [GAP]** (nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79, li2021nanotwinscontainingmicrostructureand pages 1-4, nemani2024advancementsinadditive pages 102-105)

### Top 5 things the PI should know

1. **The novelty boundary is not “NAB is printable”:** a pre-alloyed Cu–9Al–5Fe–5Ni powder already gave **99.55% density** and **769–949 MPa UTS** by LMD. Distinguish the proposed alloys through *as-deposited seawater performance, lower-Ni compositions and repair on actual NAB/C71500 substrates*. (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9)
2. **Optimize deposition and corrosion-facing chemistry together:** blue Cu-on-steel improved pores **0.4% → 0.1%** and volumetric efficiency **28% → 36%** by reducing feed, but did so at the expense of greater substrate dilution; the low-dilution setting was different. (yamaguchi2024influenceofthe pages 13-15, yamaguchi2024influenceofthe pages 12-13)
3. **Treat substrate as a categorical experimental variable:** the same green Cu settings produced **0% dilution on Cu** and **77.5% on tool steel**, plus markedly different melt-pool continuity and cracking susceptibility. An NAB or Cu–Ni repair coupon requires its own first-layer window. (prasad2020lasermetaldeposition pages 3-4, prasad2020lasermetaldeposition pages 7-9)
4. **Do not collapse the defect modes:** gas pores dominated the successful NAB powder builds; lack of fusion dominated the underpowered failed one. Keyholes and Zn/Mn evaporation should remain testable hypotheses, not asserted explanations for every Cu-alloy pore. (li2021nanotwinscontainingmicrostructureand pages 9-14, yamaguchi2024influenceofthe pages 10-12)
5. **Measure quantities the literature often omits:** calibrate feeder RPM to **g/min**, report actual powder **catchment separately from deposited-volume efficiency**, Z-increment and mass build rate; log powder size, flow and oxygen by lot; and benchmark as-deposited alloy and wrought C71500 under *identical*, explicitly stated seawater, exposure and flow conditions. This combined qualification dataset is not established by the studies above. (yamaguchi2024influenceofthe pages 4-5, li2021nanotwinscontainingmicrostructureand pages 4-9, nemani2024advancementsinadditive pages 102-105, fadhel2026discoveryoffeasible pages 6-8)

References

1. (yamaguchi2024influenceofthe pages 4-5): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

2. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

3. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

4. (prasad2020lasermetaldeposition pages 3-4): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

5. (prasad2020lasermetaldeposition pages 1-3): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

6. (prasad2020lasermetaldeposition pages 7-9): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

7. (yamaguchi2024influenceofthe pages 2-4): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

8. (yamaguchi2024influenceofthe pages 5-7): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

9. (yamaguchi2024influenceofthe pages 13-15): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

10. (yamaguchi2024influenceofthe pages 12-13): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

11. (yamaguchi2024influenceofthe pages 10-12): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

12. (li2021nanotwinscontainingmicrostructureand pages 1-4): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

13. (li2021nanotwinscontainingmicrostructureand pages 9-14): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

14. (li2021nanotwinscontainingmicrostructureand media 36bae893): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

15. (nguyen2022functionallymagneticgradient pages 28-32): Vy Tran Phuong Nguyen. Functionally magnetic gradient copper-nickel material fabricated via directed energy deposition. ArXiv, 2022. URL: https://doi.org/10.33915/etd.11213, doi:10.33915/etd.11213. This article has 1 citations.

16. (nguyen2022functionallymagneticgradient pages 39-45): Vy Tran Phuong Nguyen. Functionally magnetic gradient copper-nickel material fabricated via directed energy deposition. ArXiv, 2022. URL: https://doi.org/10.33915/etd.11213, doi:10.33915/etd.11213. This article has 1 citations.

17. (nguyen2022functionallymagneticgradient pages 21-28): Vy Tran Phuong Nguyen. Functionally magnetic gradient copper-nickel material fabricated via directed energy deposition. ArXiv, 2022. URL: https://doi.org/10.33915/etd.11213, doi:10.33915/etd.11213. This article has 1 citations.

18. (balkan2021directedenergydeposition pages 2-3): Muhammed Enes Balkan, Eda Aydoğan, Murat Işık, Bora Derin, and Bahattin Koç. Directed energy deposition process development for functionally gradient copper-inconel 718 materials. Journal of Additive Manufacturing Technologies, Dec 2021. URL: https://doi.org/10.18416/jamtech.2111581, doi:10.18416/jamtech.2111581. This article has 12 citations.

19. (fadhel2026discoveryoffeasible pages 5-6): Azza Fadhel, Nathaniel W. Zuckschwerdt, Aryan Deshwal, Susmita Bose, Amit Bandyopadhyay, and Jana Doppa. Discovery of feasible 3d printing configurations for metal alloys via ai-driven adaptive experimental design. Proceedings of the AAAI Conference on Artificial Intelligence, 40(47):39939-39948, Mar 2026. URL: https://doi.org/10.1609/aaai.v40i47.41428, doi:10.1609/aaai.v40i47.41428. This article has 2 citations and is from a domain leading peer-reviewed journal.

20. (fadhel2026discoveryoffeasible pages 6-8): Azza Fadhel, Nathaniel W. Zuckschwerdt, Aryan Deshwal, Susmita Bose, Amit Bandyopadhyay, and Jana Doppa. Discovery of feasible 3d printing configurations for metal alloys via ai-driven adaptive experimental design. Proceedings of the AAAI Conference on Artificial Intelligence, 40(47):39939-39948, Mar 2026. URL: https://doi.org/10.1609/aaai.v40i47.41428, doi:10.1609/aaai.v40i47.41428. This article has 2 citations and is from a domain leading peer-reviewed journal.

21. (fadhel2026discoveryoffeasible pages 2-3): Azza Fadhel, Nathaniel W. Zuckschwerdt, Aryan Deshwal, Susmita Bose, Amit Bandyopadhyay, and Jana Doppa. Discovery of feasible 3d printing configurations for metal alloys via ai-driven adaptive experimental design. Proceedings of the AAAI Conference on Artificial Intelligence, 40(47):39939-39948, Mar 2026. URL: https://doi.org/10.1609/aaai.v40i47.41428, doi:10.1609/aaai.v40i47.41428. This article has 2 citations and is from a domain leading peer-reviewed journal.

22. (gradl2021advancinggrcopbasedbimetallic pages 8-11): Paul R. Gradl, Thomas W. Teasley, Christopher S. Protz, Marissa B. Garcia, David Ellis, and Christopher Kantzos. Advancing grcop-based bimetallic additive manufacturing to optimize component design and applications for liquid rocket engines. AIAA Propulsion and Energy 2021 Forum, Jul 2021. URL: https://doi.org/10.2514/6.2021-3231, doi:10.2514/6.2021-3231. This article has 77 citations.

23. (canacoo2026laseradditivemanufacturing pages 15-17): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

24. (nemani2024advancementsinadditive pages 105-106): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

25. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

26. (canacoo2026laseradditivemanufacturing pages 17-19): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

27. (canacoo2026laseradditivemanufacturing pages 8-9): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

28. (yamaguchi2024influenceofthe pages 8-10): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

29. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

30. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
