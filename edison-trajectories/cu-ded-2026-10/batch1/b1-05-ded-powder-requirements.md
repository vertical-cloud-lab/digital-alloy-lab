<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: cf5e23c9-cdbd-4ead-8d0e-bdb734f32c99
- Submitted: 2026-10-17T05:10:44Z
- Fetched: 2026-10-17T05:42:05Z (status: success)
- Raw trajectory JSON: ../raw/b1-05-ded-powder-requirements.json.gz
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

QUESTION: What does peer-reviewed work say about powder requirements for
blown-powder laser DED, and how much do they matter? Cover the particle size
range (often quoted as 45-150 or 53-150 um), flowability (Hall, Carney,
angle of repose, avalanche), sphericity, satellites, moisture and oxygen, and
their measured effects on powder catchment efficiency, porosity, surface
finish and deposit chemistry. Include any copper- or copper-alloy-specific
DED work, including high reflectivity at ~1 um wavelength, absorptivity of
Cu-Ni and Al-bronze powders, preheating, and blue or green lasers for copper
DED. Name the papers that actually measured these effects rather than
stating them.

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

QUESTION: What does peer-reviewed work say about powder requirements for
blown-powder laser DED, and how much do they matter? Cover the particle size
range (often quoted as 45-150 or 53-150 um), flowability (Hall, Carney,
angle of repose, avalanche), sphericity, satellites, moisture and oxygen, and
their measured effects on powder catchment efficiency, porosity, surface
finish and deposit chemistry. Include any copper- or copper-alloy-specific
DED work, including high reflectivity at ~1 um wavelength, absorptivity of
Cu-Ni and Al-bronze powders, preheating, and blue or green lasers for copper
DED. Name the papers that actually measured these effects rather than
stating them.

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


# Powder requirements for blown-powder laser DED: measured evidence

**Bottom line.** A nominal **45–150 or 53–150 µm cut is a useful starting feedstock specification, not a demonstrated universal optimum**. Experiments show that particle size, powder condition, nozzle geometry, laser power and substrate jointly control capture and deposit quality. Published copper-alloy data do **not** establish a Hall-flow, oxygen or moisture cutoff that guarantees dense, corrosion-resistant Cu–Ni or nickel–aluminum bronze (NAB) deposits. Values below are identified as direct measurements unless explicitly called an inference or a result from another process. No corrosion test described below used ASTM D1141 substitute seawater unless stated; **3.5 wt% NaCl is not seawater**. (nurminen2004theinfluenceof pages 3-5, kiani2024thereusabilityof pages 6-9, prasad2020lasermetaldeposition pages 7-9, shahriari2023corrosionperformanceof pages 14-14)

## Studies that measured powder or deposition effects

1. **Nurminen, J., Näkki, J., and Vuoristo, P.** “The influence of powder parameters on laser cladding process.” *International Congress on Applications of Lasers & Electro-Optics* (2004), P507. **DOI: 10.2351/1.5060359.** **Process:** blown-powder laser cladding of Stellite 21 on S355 steel; feedstock approximately Co balance–26.0–28.3Cr–2.7–3.3Ni–1.0–1.4Fe–0.49–0.71Mn–5.3–5.7Mo–0.26–0.28C–0.83–1.82Si, wt%. **Measured:** 20–53, 53–150, 63–125 and 63–210 µm cuts; gravimetric powder catchment, coating sections and qualitative surface finish. With a **3 mm spot, 1.5 kW, 23 g/min and 0.5 mm nozzle gap**, three coarser-powder examples captured **74%, 71% and 59%**, respectively; **20–53 µm** reached approximately **100%** with a **6 mm spot, 3.5 kW, 34 g/min and 1 mm gap** and gave a smooth surface. These are *different processing conditions*, not a controlled claim that fine powder always achieves 100% capture. The authors report uneven-feeder/weighing uncertainty; fine powder could cause dust and, when bonding was inadequate, a wavy coating. No corrosion, oxygen cutoff or numerical roughness was established. **[CITE] [NUMBERS] [GAP]** (nurminen2004theinfluenceof pages 3-5, nurminen2004theinfluenceof pages 5-6)

2. **Syed, W. U. H., Pinkerton, A. J., and Li, L.** “A comparative study of wire feeding and powder feeding in direct diode laser deposition for rapid prototyping.” *Applied Surface Science* **247** (2005): 268–276. **DOI: 10.1016/j.apsusc.2005.01.138.** **Process:** powder-fed *versus wire-fed laser DED*, 316L on mild steel; 316L was the approximately Fe–17Cr–10Ni–2Mo stainless-steel alloy, not a copper alloy. The powder was **53–150 µm**; the comparison used an **808/940 nm** diode source. At a fixed feed setting, measured powder deposition efficiency rose from **8% at 700 W to 40% at 1300 W**. Front powder feeding gave **20–45% higher efficiency** than rear feeding, whereas rear feeding reduced reported oxidation and roughness by about **20%**. Powder-built tracks had **Ra 70–90 µm**, versus **40–60 µm** for wire-built tracks; adhering particles and some powder-build porosity were observed. **Interpretation:** a compliant sieve cut cannot substitute for specifying delivery geometry and energy; the wire comparison is not evidence for a powder-shape threshold. No marine corrosion was tested. **[CITE] [NUMBERS] [GAP]** (syed2005acomparativestudy pages 1-3, syed2005acomparativestudy pages 3-7)

3. **Kiani, P., Dupuy, A. D., Ma, K., and Schoenung, J. M.** “The Reusability of AlSi10Mg Powder in Directed Energy Deposition.” *Powders* **3** (2024): 28–43. **DOI: 10.3390/powders3010003.** **Process:** blown-powder laser DED; Al–approximately 10Si–Mg, wt%, virgin and recovered powder, sieved to **45–150 µm** between builds. Virgin-to-reused median size rose from **below 80 to above 100 µm** by later cycles; size-distribution span fell **0.51→0.38** and median aspect ratio rose **1.3→1.6**. SEM observed satellites and fused oversize clusters; it did **not** establish an allowable satellite fraction. Measured funnel discharge fell **9.2→8.1–8.5 g/s**; these are **not Hall-flow seconds per 50 g**. Deposits averaged approximately **99% theoretical density**; after the first reuse, reported UTS fell **329→303 MPa** and elongation **9.7→5.0%**, while hardness remained approximately **90–105 HV**. The authors associated reduced flow with additional lack-of-fusion damage, but did not quantify a causal satellite–porosity relationship or measure powder moisture/oxygen content. Chamber oxygen **<20 ppm** is an *atmosphere condition*, not a powder-oxygen specification. No corrosion test. **[CITE] [NUMBERS] [GAP]** (kiani2024thereusabilityof pages 6-9, kiani2024thereusabilityof pages 12-14, kiani2024thereusabilityof pages 4-6, kiani2024thereusabilityof pages 2-4)

4. **Saboori, A., Aversa, A., Bosio, F., Bassini, E., Librera, E., De Chirico, M., Biamino, S., Ugues, D., Fino, P., and Lombardi, M.** “An investigation on the effect of powder recycling on the microstructure and mechanical properties of AISI 316L produced by Directed Energy Deposition.” *Materials Science and Engineering A* **766** (2019): 138360. **DOI: 10.1016/j.msea.2019.138360.** **Process:** blown-powder laser DED; nominal powder Fe balance–16.7Cr–10Ni–2Mo–1.8Mn–0.5Si–0.02C–0.02Nb, wt%. **Powder:** **50–150 µm**, measured *d*10/*d*50/*d*90 **63.3/85.4/135.2 µm**; both lots largely spherical, roughly half of spherical particles bearing satellites; recycled powder additionally had resolidified splats. **Deposits:** recycled-powder specimens contained about **2.4%** nonmetallic inclusions, predominantly Mn/Si oxides averaging roughly **12 µm**, versus generally submicrometre inclusions in fresh-powder specimens. Elongation was **31.2 ± 2.2% fresh versus 16.2 ± 2.1% recycled**; UTS was **628.2 ± 6.6 versus 651.6 ± 43.9 MPa**. Oxygen-analysis methods were described, but a validated **powder oxygen concentration → inclusion fraction → property threshold** is not established by these quoted data. This directly demonstrates that ostensibly spherical, correctly sized powder can still give damaging oxide inclusions; it does not isolate satellites as their cause. No seawater test. **[CITE] [NUMBERS] [GAP]** (saboori2019aninvestigationon pages 2-3, saboori2019aninvestigationon pages 8-10, saboori2019aninvestigationon pages 6-8)

**Flow-test interpretation.** Hall and Carney funnels measure discharge under their respective orifice conditions; angle of repose and avalanche tests probe other, often dynamic, aspects of cohesion. They are potentially useful *lot descriptors*, not interchangeable numbers or published qualification limits for ultrasonic-atomized Cu–Ni/NAB powder in this nozzle. In particular, neither Kiani’s **g/s** discharge nor DED catchment **%** can be reported as Hall seconds/50 g. Among the original studies above, no controlled comparison establishes a universal Hall, Carney, repose-angle or avalanche acceptance value, or quantifies an independently varied **moisture content** against copper-alloy DED porosity or corrosion. Measure and report non-flow as such rather than imputing a Hall value from a Carney result. **[GAP]** (kiani2024thereusabilityof pages 6-9, kiani2024thereusabilityof pages 4-6, mathias2024metalpowderas pages 19-20)

## Copper-specific laser evidence and its limits

5. **Prasad, H. S., Brueckner, F., Volpp, J., and Kaplan, A. F. H.** “Laser metal deposition of copper on diverse metals using green laser sources.” *International Journal of Advanced Manufacturing Technology* **107** (2020): 1559–1568. **DOI: 10.1007/s00170-020-05117-z.** **Process:** coaxial *blown-powder laser DED* of **99.9 wt% Cu**, **50–90 µm** powder, with a **515 nm** green laser; 200–1000 W, 1.7 mm spot and 0.65–3.9 g/min powder. Copper-on-copper needed approximately **1 kW at 0.1 m/min and 1.3 g/min** to form a melt pool under the reported conditions. High-speed imaging documented substrate-dependent particle incorporation, including impediment by an aluminum-substrate oxide skin. Calculated *lower bounds on incident energy spent melting*, **not optical absorptivity or catchment**, were **0.73% on Cu, 2.94% on Al, 5.95% on steel and 9.78% on Ti alloy**; a Cu wall gave **2.66%**. The article reproduces earlier **smooth, cleaned elemental Cu** spectral-absorptance values of **4.0% at 1085 nm, 54.5% at 525 nm and 65.2% at 457 nm**. **It did not measure absorptivity of Cu–Ni powder or Al-bronze powder**, and discussed preheating as a possible remedy rather than testing a preheated Cu–Ni/NAB DED condition. No seawater corrosion was assessed. **[CITE] [NUMBERS] [GAP]** (prasad2020lasermetaldeposition pages 7-9, prasad2020lasermetaldeposition pages 6-7, prasad2020lasermetaldeposition pages 3-4, prasad2020lasermetaldeposition pages 1-3)

6. **Yamaguchi, M., Kato, N., Funada, Y., Yachi, T., Saikai, A., and Furumoto, T.** “Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser.” *International Journal of Advanced Manufacturing Technology* **135** (2024): 5235–5251. **DOI: 10.1007/s00170-024-14789-w.** **Process:** blown-powder laser DED of nominally pure Cu on AISI 304 stainless steel; **445 nm** laser, **0.2 mm** spot, **10 mm/s** travel; powder **D10/D50/D90 = 31/46/71 µm**, with **10 or 20 mg/s** feed. At **180 W and 10 mg/s**, measured minimum porosity was **0.1%** and building efficiency **36%**. **150–180 W** and **0.4–0.5 mm** hatch gave good single-layer surface quality; higher power and lower feed improved density/efficiency but increased **Fe–Cu substrate dilution**. At **180 W and 20 mg/s**, deposited Cu was reported as **99.0 wt% 200 µm above the interface** under the low-dilution condition. Neither a corrosion benchmark nor Cu–Ni/NAB powder absorptivity was measured. **[CITE] [NUMBERS] [GAP]** (yamaguchi2024influenceofthe pages 1-2, yamaguchi2024influenceofthe pages 2-4)

7. **Li and colleagues’ Cu–9Al–5Fe–5Ni laser-metal-deposition NAB study, as identified in** Nemani, A. V., Ghaffari, M., Sabet Bokati, K., Valizade, N., Afshari, E., and Nasiri, A., “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* **8** (2024): 54, **DOI: 10.3390/jmmp8020054**. **Process attributed to the underlying study:** laser DED of NAB, composition **Cu balance–9Al–5Fe–5Ni wt%**. The review reports as-deposited martensitic β*, Widmanstätten α, Fe₃Al/NiAl precipitates; across processing conditions, **yield 593–713 MPa, UTS 769–949 MPa and elongation 10–12%**. **Evidence limit:** those numbers were checked in the *review*, not independently against the original article; its full citation/DOI, feedstock powder characterization, deposit porosity and seawater corrosion could not be verified here. Do not represent the review DOI as the primary study’s DOI. **[CITE: review only] [NUMBERS: secondary] [NOVELTY-RISK: NAB laser DED already exists] [GAP]** (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83)

8. **Prior art requiring retrieval before claiming novelty:** Yao, C.-L., and Shim, D.-S., “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate,” *Journal of Alloys and Compounds* **918** (2022): 165776, **DOI: 10.1016/j.jallcom.2022.165776**; and Rayner, A. J., Morshed-Behbahani, K., Spence, C., Wood, G., Hamre, D., Nasiri, A., and Bishop, D. P., “Directed Energy Deposition of UNS C63020 Nickel Aluminum Bronze Powder,” conference chapter (2024), **DOI: 10.1007/978-3-031-67398-6_13**. The former’s **CuNi2SiCr** name indicates a low-Ni Cu alloy, *not* 10–30 wt% Ni. A later review explicitly describes CuNi2SiCr powder deposited on NAB for propeller repair and reports **porous, soft single-α deposits** as a concern; that review instead cites a Yao study emphasizing microstructure/mechanics. **Neither original full text was obtained here:** actual wt% analyses, sieve/flow/oxygen, corrosion solution/duration, density, *i*₍corr₎ and hardness must **not** be invented. Rayner’s chapter DOI is identifiable, but the contents were likewise inaccessible. **[NOVELTY-RISK: pre-existing single-alloy powder/NAB-repair work] [NAVY: marine-propeller application, not verified Navy funding] [GAP]** (nemani2024advancementsinadditive pages 79-83)

## Corrosion benchmarks—important, but **not powder-laser-DED proof**

9. **Song, J., Jimenez, X. A., To, A. C., and Fu, Y.** “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys.” *Materials* **17** (2024): 876. **DOI: 10.3390/ma17040876.** **Process:** **cold-metal-transfer WAAM**, not laser/powder DED; **1.2 mm wire** nominally **67.5Cu–30Ni–0.7Mn–0.55Fe–0.25Ti–0.1Si wt%**, deposited on a **wrought C71500 plate** measured at **68.046Cu–30.46Ni–0.73Mn–0.56Fe wt%**, plus minor reported elements. Electrochemistry: **naturally aerated 3.5 wt% NaCl**, room temperature, **3 h initial immersion**, EIS **100 kHz–10 mHz**, followed by cyclic polarization; no electrolyte circulation or 30-day immersion was reported. Best WAAM condition: **8 m/min** wire feed, **1000 mm/min** travel, **3.85 mm** track distance. Fitted film resistance *Rf* for wrought was **1.08/1.18 × 10⁵ Ω** on XY/YZ surfaces versus **1.40/1.66 × 10⁵ Ω** for this WAAM condition; the study reports lower passive current and higher breakdown potential for that condition. Another WAAM condition had *lower* film resistance than wrought. Preferential attack of **Ni-depleted interdendritic regions** remained despite apparently favorable bulk electrochemistry; no selective-attack depth was established in the cited text. **Funded by ONR N00014-21-1-2800.** Film resistance is **not** a corrosion rate or *i*₍corr₎. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: as-built Cu–Ni versus C71500 already compared, by WAAM] [GAP: powder laser DED and long seawater exposure]** (song2024microstructuresandcorrosion pages 14-17, song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion media f0ef3224)

10. **Shahriari, A., Chalasani, D., Amirkhiz, B. S., and Mohammadi, M.** “Corrosion performance of wire arc additively manufactured NAB alloy.” *npj Materials Degradation* **7** (2023). **DOI: 10.1038/s41529-023-00405-x.** **Process:** **GMAW/WAAM** ERCuNiAl NAB versus **cast** NAB from an impeller; exact individual wire/cast elemental assays were not verified in the accessible text. **Naturally aerated 3.5 wt% NaCl** at **23 ± 2 °C**; as-built and cast immersed **96 h**, heat-treated samples **24 h**—a **non-identical exposure-duration comparison**; flow not stated. EIS used **10 mV, 100 kHz–0.01 Hz**. As-built WAAM gave the best reported resistance, with total impedance of approximately **103 kΩ·cm²**, compared with approximately **10.2, 2.58 and 3.8 kΩ·cm²** for specimens treated **350 °C/2 h, 550 °C/4 h and 675 °C/6 h**, respectively. Reported treated-condition *i*₍corr₎ values were approximately **4.4, 6.6 and 8 µA/cm²**. The α matrix adjacent to cathodic κ particles was attacked; approximately **3 µm** maximum local surface depression was reported for the first heat-treated condition. These are **not** powder-feedstock effects, and as-built WAAM superiority does not prove NAB laser DED will outperform C71500. **[CITE] [NUMBERS] [NAVY: impeller/marine application; funding not verified] [GAP]** (shahriari2023corrosionperformanceof pages 10-10, shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 8-10, shahriari2023corrosionperformanceof pages 14-14)

11. **Huo, R., Wang, Z., Wang, M., Wang, R., Zhang, S., Zhang, C., Wu, C., Chen, H., and Chen, J.** “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* **18** (2025): 2205. **DOI: 10.3390/ma18102205.** **Process:** **CMT-WAAM**, not laser DED; wire **Cu balance–8.73Al–5.9Fe–4.52Ni–1.39Mn wt%**, minor Si, Pb and Zn. **Aerated 3.5 wt% NaCl in deionized water**, **25 ± 5 °C**; OCP stabilized **1 h**; flow and 30-day immersion not reported. Raising heat input **243.8→644.7 J/mm** raised *i*₍corr₎ **2.56 ± 0.04→7.52 ± 0.07 µA/cm²** and made polarization potential *E* more negative **−269.61 ± 40→−700.94 ± 15 mV**; reported surface microhardness across the same end-member samples was **192.4 ± 6.9→166.9 ± 0.3 HV**. The abstract gives different summary hardness endpoints; the values quoted here are the explicitly enumerated **surface measurements**. Heat input itself is a consequential corrosion/microstructure variable, independent of powder qualification. **[CITE] [NUMBERS] [NAVY: marine application, funding unverified] [GAP: not powder DED]** (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 1-2)

### What remains unanswered

No retrieved original experiment jointly established an allowable **Hall/Carney/repose/avalanche value, satellite fraction, powder-moisture or powder-oxygen ceiling** for pre-alloyed **10–30 wt% Ni Cu–Ni or NAB blown-powder laser DED**, with measured capture, deposit composition, porosity *and* as-deposited 30-day seawater corrosion. Likewise, **elemental copper’s near-IR reflectivity is not measured absorptivity of Cu–Ni or Al-bronze powder**, and short, static NaCl electrochemistry cannot demonstrate equivalence to wrought C71500 under flowing natural or ASTM D1141 seawater. These are appropriate experimental questions, not established facts or grounds to dismiss the identified NAB-repair prior art. **[GAP]** (kiani2024thereusabilityof pages 6-9, prasad2020lasermetaldeposition pages 3-4, shahriari2023corrosionperformanceof pages 14-14, song2024microstructuresandcorrosion pages 2-5, nemani2024advancementsinadditive pages 79-83)

## Top 5 things the PI should know

1. **Guard the novelty claim.** Powder laser DED of NAB and CuNi2SiCr-on-NAB repair have prior art; differentiate the work by *pre-alloyed composition selection, specified dissimilar substrates and as-deposited seawater performance*, not simply “first copper-alloy DED.” (nemani2024advancementsinadditive pages 79-83)
2. **Test delivered powder, not merely the sieve certificate.** Capture changed from **59–74%** among coarser Stellite examples and approached **100%** for fine powder under a different high-power condition; delivery geometry alone changed efficiency by **20–45%** in a 316L comparison. Characterize nozzle-output mass flow and actual catchment for every alloy/lot. (nurminen2004theinfluenceof pages 5-6, syed2005acomparativestudy pages 3-7)
3. **Treat oxidation and morphology as distinct risks.** DED recycling produced oxide inclusions and roughly **halved 316L elongation** despite predominantly spherical feedstock; separately record oxygen, water exposure, satellites/agglomerates and chemistry *before and after deposition*. No defensible Cu-alloy cutoff follows from that steel experiment. (saboori2019aninvestigationon pages 2-3, saboori2019aninvestigationon pages 8-10)
4. **Do not extrapolate pure-Cu laser optics to alloy powder.** Direct green- and blue-laser copper DED demonstrations exist, including **0.1% porosity** with blue light, but their absorptivity and power requirements do not specify Cu–Ni/NAB behavior. Measure alloy-powder optical response and substrate-specific process windows if wavelength or preheating is central to the proposal. (prasad2020lasermetaldeposition pages 3-4, yamaguchi2024influenceofthe pages 1-2, prasad2020lasermetaldeposition pages 1-3)
5. **Make the corrosion comparator genuinely comparable.** An ONR-funded **WAAM** 70/30 Cu–Ni build exceeded wrought C71500 in selected *short-term* film-resistance tests yet retained Ni-depleted selective attack. Matched as-deposited C71500 controls, substrate/interface observations and longer **specified static/flowing seawater** exposures are necessary before claiming repair-service equivalence. (song2024microstructuresandcorrosion pages 14-17, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 13-14)

References

1. (nurminen2004theinfluenceof pages 3-5): Janne Nurminen, Jonne Näkki, and Petri Vuoristo. The influence of powder parameters on laser cladding process. International Congress on Applications of Lasers &amp; Electro-Optics, pages P507, Jan 2004. URL: https://doi.org/10.2351/1.5060359, doi:10.2351/1.5060359. This article has 5 citations.

2. (kiani2024thereusabilityof pages 6-9): Parnian Kiani, Alexander D. Dupuy, Kaka Ma, and Julie M. Schoenung. The reusability of alsi10mg powder in directed energy deposition. Powders, 3:28-43, Jan 2024. URL: https://doi.org/10.3390/powders3010003, doi:10.3390/powders3010003. This article has 14 citations.

3. (prasad2020lasermetaldeposition pages 7-9): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

4. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

5. (nurminen2004theinfluenceof pages 5-6): Janne Nurminen, Jonne Näkki, and Petri Vuoristo. The influence of powder parameters on laser cladding process. International Congress on Applications of Lasers &amp; Electro-Optics, pages P507, Jan 2004. URL: https://doi.org/10.2351/1.5060359, doi:10.2351/1.5060359. This article has 5 citations.

6. (syed2005acomparativestudy pages 1-3): Waheed Ul Haq Syed, Andrew J. Pinkerton, and Lin Li. A comparative study of wire feeding and powder feeding in direct diode laser deposition for rapid prototyping. Applied Surface Science, 247:268-276, Jul 2005. URL: https://doi.org/10.1016/j.apsusc.2005.01.138, doi:10.1016/j.apsusc.2005.01.138. This article has 305 citations and is from a domain leading peer-reviewed journal.

7. (syed2005acomparativestudy pages 3-7): Waheed Ul Haq Syed, Andrew J. Pinkerton, and Lin Li. A comparative study of wire feeding and powder feeding in direct diode laser deposition for rapid prototyping. Applied Surface Science, 247:268-276, Jul 2005. URL: https://doi.org/10.1016/j.apsusc.2005.01.138, doi:10.1016/j.apsusc.2005.01.138. This article has 305 citations and is from a domain leading peer-reviewed journal.

8. (kiani2024thereusabilityof pages 12-14): Parnian Kiani, Alexander D. Dupuy, Kaka Ma, and Julie M. Schoenung. The reusability of alsi10mg powder in directed energy deposition. Powders, 3:28-43, Jan 2024. URL: https://doi.org/10.3390/powders3010003, doi:10.3390/powders3010003. This article has 14 citations.

9. (kiani2024thereusabilityof pages 4-6): Parnian Kiani, Alexander D. Dupuy, Kaka Ma, and Julie M. Schoenung. The reusability of alsi10mg powder in directed energy deposition. Powders, 3:28-43, Jan 2024. URL: https://doi.org/10.3390/powders3010003, doi:10.3390/powders3010003. This article has 14 citations.

10. (kiani2024thereusabilityof pages 2-4): Parnian Kiani, Alexander D. Dupuy, Kaka Ma, and Julie M. Schoenung. The reusability of alsi10mg powder in directed energy deposition. Powders, 3:28-43, Jan 2024. URL: https://doi.org/10.3390/powders3010003, doi:10.3390/powders3010003. This article has 14 citations.

11. (saboori2019aninvestigationon pages 2-3): Abdollah Saboori, Alberta Aversa, Federico Bosio, Emilio Bassini, Erica Librera, Michele De Chirico, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. An investigation on the effect of powder recycling on the microstructure and mechanical properties of aisi 316l produced by directed energy deposition. Materials Science and Engineering: A, 766:138360, Oct 2019. URL: https://doi.org/10.1016/j.msea.2019.138360, doi:10.1016/j.msea.2019.138360. This article has 250 citations.

12. (saboori2019aninvestigationon pages 8-10): Abdollah Saboori, Alberta Aversa, Federico Bosio, Emilio Bassini, Erica Librera, Michele De Chirico, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. An investigation on the effect of powder recycling on the microstructure and mechanical properties of aisi 316l produced by directed energy deposition. Materials Science and Engineering: A, 766:138360, Oct 2019. URL: https://doi.org/10.1016/j.msea.2019.138360, doi:10.1016/j.msea.2019.138360. This article has 250 citations.

13. (saboori2019aninvestigationon pages 6-8): Abdollah Saboori, Alberta Aversa, Federico Bosio, Emilio Bassini, Erica Librera, Michele De Chirico, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. An investigation on the effect of powder recycling on the microstructure and mechanical properties of aisi 316l produced by directed energy deposition. Materials Science and Engineering: A, 766:138360, Oct 2019. URL: https://doi.org/10.1016/j.msea.2019.138360, doi:10.1016/j.msea.2019.138360. This article has 250 citations.

14. (mathias2024metalpowderas pages 19-20): Laura E. T. Mathias, Vitor E. Pinotti, Bruna F. Batistão, Nicolas Rojas-Arias, Gustavo Figueira, Angelo F. Andreoli, and Piter Gargarella. Metal powder as feedstock for laser-based additive manufacturing: from production to powder modification. Journal of Materials Research, 39:19-47, Dec 2024. URL: https://doi.org/10.1557/s43578-023-01271-8, doi:10.1557/s43578-023-01271-8. This article has 77 citations and is from a peer-reviewed journal.

15. (prasad2020lasermetaldeposition pages 6-7): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

16. (prasad2020lasermetaldeposition pages 3-4): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

17. (prasad2020lasermetaldeposition pages 1-3): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

18. (yamaguchi2024influenceofthe pages 1-2): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

19. (yamaguchi2024influenceofthe pages 2-4): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

20. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

21. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

22. (song2024microstructuresandcorrosion pages 14-17): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

23. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

24. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

25. (song2024microstructuresandcorrosion pages 13-14): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

26. (song2024microstructuresandcorrosion media f0ef3224): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

27. (shahriari2023corrosionperformanceof pages 10-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

28. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

29. (shahriari2023corrosionperformanceof pages 8-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

30. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

31. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

32. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

33. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.
