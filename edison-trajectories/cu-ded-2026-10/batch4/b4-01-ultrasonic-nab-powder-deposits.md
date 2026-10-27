<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: 72c8d01e-68d1-441c-80d6-d38f5bdadcc6
- Submitted: 2026-10-17T06:11:08Z
- Fetched: 2026-10-17T06:41:49Z (status: success)
- Raw trajectory JSON: ../raw/b4-01-ultrasonic-nab-powder-deposits.json.gz
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

QUESTION: What happened when ultrasonically atomized copper alloy powder was
actually deposited by laser DED? Follow the Berlin group (Uhlmann, Polte,
Fasselt, Mueller, Kloetzer-Freese, Kleba-Ehrhardt, Biegler, Rethmeier; TU
Berlin / Fraunhofer IPK / BAM) after Uhlmann et al. 2024, Materials 17, 3396
and Mueller et al. 2023, IOP Conf. Ser. Mater. Sci. Eng. 1296, 012036: deposit
density, porosity, catchment, microstructure, hardness, tensile, corrosion,
and comparison with gas-atomized NAB powder; how carbon-fiber sonotrode
debris affected deposits; any repair of propeller bronze. Also report any
other study (any alloy) that printed ultrasonically atomized powder by DED
or LPBF and compared it with gas-atomized powder of the same alloy.

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

QUESTION: What happened when ultrasonically atomized copper alloy powder was
actually deposited by laser DED? Follow the Berlin group (Uhlmann, Polte,
Fasselt, Mueller, Kloetzer-Freese, Kleba-Ehrhardt, Biegler, Rethmeier; TU
Berlin / Fraunhofer IPK / BAM) after Uhlmann et al. 2024, Materials 17, 3396
and Mueller et al. 2023, IOP Conf. Ser. Mater. Sci. Eng. 1296, 012036: deposit
density, porosity, catchment, microstructure, hardness, tensile, corrosion,
and comparison with gas-atomized NAB powder; how carbon-fiber sonotrode
debris affected deposits; any repair of propeller bronze. Also report any
other study (any alloy) that printed ultrasonically atomized powder by DED
or LPBF and compared it with gas-atomized powder of the same alloy.

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


## What the deposition evidence establishes

**Ultrasonically atomized nickel–aluminum bronze (NAB) powder was used to make laser directed-energy-deposition (DED) specimens, but the accessible Berlin-group report does not establish their density, mechanical performance, corrosion resistance, or suitability for propeller repair.** Its gas-atomized comparator was a *different aluminum-bronze alloy*, and the reported internal pores were in powder particles—not measured porosity in deposited metal. The 2023 deposition paper’s full text was not obtainable in this search; its numerical deposition results therefore cannot be verified here. (uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 15-15)

### Relevant items

**1. Berlin group—actual DED specimens, with results not independently recoverable.** Müller, V.; Fasselt, J. M.; Kruse, T.; Klötzer, C.; Kleba-Ehrhardt, R.; Choma, T.; Biegler, M.; Rethmeier, M. “Using Ultrasonic Atomization to Recycle Aluminium Bronze Chips for Additive Laser Directed Energy Deposition.” *IOP Conference Series: Materials Science and Engineering* **1296** (2023), 012036. **DOI: 10.1088/1757-899X/1296/1/012036.** **Process:** blown-powder laser DED, using powder ultrasonically atomized from propeller-manufacturing NAB grinding chips; nominal feedstock CuAl10Ni5Fe5 (approximately Cu balance, Al 10, Ni 5, Fe 5 wt%). The subsequent Berlin paper explicitly says that this earlier study produced DED specimens from the same chips. Because the deposition paper’s full text was unavailable, **deposit density/porosity, powder catchment, deposit microstructure, hardness, tensile properties, corrosion-test conditions and results, and any repair on an actual propeller cannot be verified**. Specimen fabrication is not evidence of a qualified propeller repair. **[CITE] [NAVY: ship-propeller application, not identified as US Navy funding] [NOVELTY-RISK: recycled, pre-alloyed NAB powder already reached laser DED] [GAP: no verified as-deposited repair or seawater-performance result].** (uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 15-15)

**2. Berlin group—quantitative powder comparison, *not* a deposited-part comparison.** Uhlmann, E.; Polte, J.; Fasselt, J. M.; Müller, V.; Klötzer-Freese, C.; Kleba-Ehrhardt, R.; Biegler, M.; Rethmeier, M. “A Comparative Evaluation of Powder Characteristics of Recycled Material from Bronze Grinding Chips for Additive Manufacturing.” *Materials* **17** (2024), 3396. **DOI: 10.3390/ma17143396.** **Process:** powder preparation and characterization for blown-powder laser DED; no new deposit-property test in this article. Ultrasonic atomization remelted propeller-grinding chips nominally CuAl10Ni5Fe5 at 1300 °C, delivered melt at 1.5 bar to a **40 kHz carbon-fiber sonotrode** under grade-5.0 argon, and screened powder at 200 µm. The commercially gas-atomized reference was **CuAl9.5Fe, without nominal Ni**: it is not a same-composition NAB control. The authors’ EDX estimates, which they caution are not precise bulk assays, were UA Cu 75.16, Al 9.83, Fe 6.76, Ni 5.91, Mn 2.33 wt%, versus GA Cu 89.3, Al 9.3, Fe 1.1 wt%. (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation media 6830b2c2)

The UA versus GA powder results were, respectively: area-equivalent size **X₁₀/X₅₀/X₉₀ = 48/98/174 versus 64/95/135 µm**; mean aspect ratio **0.935 versus 0.843**; particles with aspect ratio >0.9, **82% versus 43.5%**; ASTM B964 **Carney**, *not Hall*, flow time **8.62 versus 10.55 s/150 g**; repose angle **13.74° versus 20.08°**; Hausner ratio **1.05 versus 1.12**; and oxygen **0.019 versus 0.013 wt%**. Microscopy showed almost no enclosed gas pores in UA particles and more in GA particles; **neither observation is a deposit-density measurement**. Absolute loose/apparent density and powder-catchment values suitable for a deposit comparison were not established by these cited results. Powder from the propeller grinding route contained some ceramic abrasive debris. Fine carbon fibers up to approximately **20 µm** were also observed in UA powder and attributed to sonotrode shedding. The authors proposed that carbon *could* cause lack of fusion or porosity, but **did not demonstrate that it caused either defect in deposits**. They explicitly called for tests under real DED powder-feeding conditions and mechanical testing of resulting structures. **[CITE] [NUMBERS] [NAVY: marine-propeller application; EU MarTERA funding, not identified as US Navy funding] [NOVELTY-RISK: NAB ultrasonic feedstock and powder benchmarking are prior art] [GAP: matched-alloy GA control, catchment, deposited defects and corrosion remain unestablished].** (uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 12-13, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 13-15)

**3. Independent example that *printed both atomization routes*: 316L LPBF.** Grzelak, K.; Bielecki, M.; Kluczyński, J.; Szachogłuchowicz, I.; Śnieżek, L.; Torzewski, J.; Łuszczek, J.; Słoboda, Ł.; Wachowski, M.; Komorek, Z.; Małek, M.; Zygmuntowicz, J. “A Comparative Study on Laser Powder Bed Fusion of Differently Atomized 316L Stainless Steel.” *Materials* **15** (2022), 4938. **DOI: 10.3390/ma15144938.** **Process:** LPBF, **not DED**; commercial plasma-arc gas-atomized (PAGA) versus ultrasonically atomized (UA) nominal 316L. These were **not chemically identical heats**: PAGA versus UA powder contained approximately Cr 17.8/17.3, Ni 12.8/10.5, Mn 0.98/1.0, Mo 2.31/2.4 and O 0.020/0.022 wt%, Fe balance. UA originated from welding wire and had different size classification, so properties cannot be attributed solely to atomization. (grzelak2022acomparativestudy pages 2-4, grzelak2022acomparativestudy pages 8-10, grzelak2022acomparativestudy pages 10-13)

UA versus PAGA powder had particle-count D₁₀/D₅₀/D₉₀ **34.1/46.1/55.2 versus 16.4/29.4/50.4 µm**, sphericity **0.89 versus 0.75**, apparent density **4.40 versus 4.29 g/cm³**, and flow **14.83 versus 18.69 s/50 g**. Selected LPBF settings for UA/PAGA were **250/220 W**, both **800 mm/s** and **0.12 mm** hatch spacing, at **86.81/76.39 J/mm³**. Metallographic section porosity was **0.03%/0.02%**—approximately **99.97%/99.98%** section density—and maximum measured pore size **0.05/0.04 mm**. UA/PAGA hardness was **216.44/233.67 HV0.5**; mean yield strength **436.45/454.78 MPa**, ultimate tensile strength **612.68/621.14 MPa**, elongation **45.41%/35.98%**, and Charpy energy **121.0/148.4 J**. No seawater or corrosion test was reported for this comparison. The authors relate much of the property difference to the distinct melting settings; it is **not** proof that UA intrinsically lowers strength. The reported funding was Poland’s Military University of Technology, **not stated to be US Navy/DoD**. **[CITE] [NUMBERS] [GAP: LPBF steel cannot validate copper-alloy DED or seawater performance].** (grzelak2022acomparativestudy pages 8-10, grzelak2022acomparativestudy pages 10-13, grzelak2022acomparativestudy pages 13-16, grzelak2022acomparativestudy pages 16-18)

**4. Other demonstrated ultrasonic-powder laser DED, without a matched gas-atomized print control.** Cabrioli, M.; Colmenero, M. S.; Gholamzadeh, S.; Vanazzi, M.; Amirabdollahian, S.; Perini, M.; Łacisz, W.; Kalicki, B. “Upcycling of Copper Scrap into High-Quality Powder for Additive Manufacturing: Processing, Characterization, and Sustainability Assessment.” *Journal of Manufacturing and Materials Processing* **9** (2025), 320. **DOI: 10.3390/jmmp9090320.** Its indexed abstract reports ultrasonically atomizing offshore-cable scrap to approximately **99.5 wt% Cu** and printing it by **laser DED**, with qualitative printability and substrate compatibility. This is **essentially unalloyed Cu, not NAB or Cu–Ni**. The retrieved document attached to its record was an unrelated report, so deposit porosity, process conditions, powder metrics and any gas-atomized comparison **could not be checked and are not claimed here**. **[CITE: bibliographic/abstract-level only] [NAVY: offshore source, not demonstrated Navy funding] [NOVELTY-RISK: ultrasonic Cu powder has also been laser-DED-printed independently] [GAP: no verified same-alloy UA–GA deposit comparison].**

**5. Corrosion benchmarks that must not be mistaken for Berlin powder-DED results.** Huo, R.; Wang, Z.; Wang, M.; Wang, R.; Zhang, S.; Zhang, C.; Wu, C.; Chen, H.; Chen, J. “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* **18** (2025), 2205. **DOI: 10.3390/ma18102205.** **Process: wire-arc DED/WAAM using cold-metal-transfer arc, not laser or powder.** Wire: Cu balance, Al **8.73**, Fe **5.90**, Ni **4.52**, Mn **1.39 wt%**. As-deposited specimens received heat inputs **243.8–644.7 J/mm**. In **aerated, nominally static 3.5 wt% NaCl at 25 ± 5 °C**, testing used **3600 s OCP**, EIS, another **1800 s OCP**, then polarization; no 30-day immersion or flowing seawater is reported. Across lowest-to-highest heat input, measured hardness was **192.4 ± 6.9 to 166.9 ± 0.3 HV**, grain size **38.26–74.62 µm**, fitted polarization potential **−269.61 ± 40 to −700.94 ± 15 mV versus SCE**, and *i*₍corr₎ **2.56 ± 0.04 to 7.52 ± 0.07 µA/cm²**. EIS fitted film resistance **1152 to 185.8 Ω·cm²** and charge-transfer resistance **2485 to 707 Ω·cm²**. Coarsening of κ precipitates and less uniform Al accompanied poorer short-term corrosion performance. **[CITE] [NUMBERS] [NOVELTY-RISK: as-deposited NAB microstructure–corrosion relationships already studied, but by WAAM] [GAP: no matched C71500 or long-duration flowing-seawater qualification].** Note that the paper’s abstract states different hardness endpoints; the values above are from its results and conclusions. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 13-15, huo2025modulatingheatinput pages 15-16)

Tan, Y.; Xie, H.; Feng, X.; Huang, S.; Zhang, W.; Peng, L.; Wang, W.; Zhao, Y. “Effect of Al/Ni Ratio on the Microstructure and Properties of Nickel–Aluminum Bronze Alloys.” *Materials* **17** (2024), 1330. **DOI: 10.3390/ma17061330.** **Process: vacuum-induction-melted CAST alloy, not DED.** Measured wt% Al/Ni/Fe/Mn, Cu balance, were **6.94/6.82/4.10/1.72**, **7.90/6.13/3.92/2.12**, **8.94/5.18/4.12/2.18**, and **9.94/3.99/3.94/1.82**. Static **3.5 wt% NaCl, 25 °C, 30 days**, solution changed weekly: the highest-Ni/lowest-Al composition had mass-loss rate **0.00267 mm/year**; its **30-day** fitted *i*₍corr₎, *E*₍corr₎ and polarization resistance were **0.35 µA/cm², −281.48 mV and 173.48 kΩ·cm²**. The lowest-Ni/highest-Al alloy gave **0.78 µA/cm², −257.75 mV and 54.04 kΩ·cm²**. Across the composition series, hardness rose about **104–202 HV**, tensile strength **356–751 MPa**, while elongation fell **50.5–11.0%**. This provides a **Ni-reduction trade-off in cast NAB**, not evidence that reduced-Ni *DED* NAB meets a C71500 seawater target. **[CITE] [NUMBERS] [NOVELTY-RISK: varying NAB Al/Ni for corrosion and strength is established in castings] [GAP: establish the trade-off in as-deposited powder DED and against wrought C71500].** (tan2024effectofalni pages 2-4, tan2024effectofalni pages 10-12, tan2024effectofalni pages 1-2)

### Top 5 things the PI should know

1. **Do not claim that ultrasonic NAB powder has never been laser-DED-deposited.** Berlin’s 2023 specimens precede this proposal; the defensible distinction is controlled *new compositions* and validated as-deposited deposit, interface and seawater outcomes. (uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 15-15)
2. **Do not turn attractive powder numbers into deposit claims.** Berlin’s 2024 comparison shows better UA powder flow and morphology, but its GA control is Ni-free and its powder-particle pore observations say nothing quantitative about deposit density or catchment. (uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 12-13, uhlmann2024acomparativeevaluation pages 7-10)
3. **Treat sonotrode debris as a measurable risk, not a proven failure mechanism.** Carbon fibers were detected in feedstock; their effect on built material was hypothesized, not measured. Track inclusions alongside lot oxygen, feed efficiency and resulting defects. (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 13-15)
4. **Separate short electrochemistry from the service-life endpoint.** Published as-deposited WAAM NAB data show a roughly threefold change in short-test *i*₍corr₎ with heat input, while 30-day cast-NAB results show composition-dependent behavior. Neither tests flowing natural seawater or demonstrates parity with wrought 70–30 Cu–Ni. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 4-5, tan2024effectofalni pages 10-12, tan2024effectofalni pages 2-4)
5. **A same-*grade* printing comparison exists, but not the required same-*heat* copper DED control.** The 316L UA/PAGA LPBF study achieved similarly low section porosity using different powders **and different laser energies**. Match composition and powder-size distributions—or explicitly model their effects—before attributing copper-DED performance to atomization route. (grzelak2022acomparativestudy pages 8-10, grzelak2022acomparativestudy pages 10-13, grzelak2022acomparativestudy pages 13-16)

References

1. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

2. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

3. (uhlmann2024acomparativeevaluation pages 15-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

4. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

5. (uhlmann2024acomparativeevaluation media 6830b2c2): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

6. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

7. (uhlmann2024acomparativeevaluation pages 12-13): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

8. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

9. (uhlmann2024acomparativeevaluation pages 13-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

10. (grzelak2022acomparativestudy pages 2-4): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

11. (grzelak2022acomparativestudy pages 8-10): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

12. (grzelak2022acomparativestudy pages 10-13): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

13. (grzelak2022acomparativestudy pages 13-16): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

14. (grzelak2022acomparativestudy pages 16-18): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

15. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

16. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

17. (huo2025modulatingheatinput pages 13-15): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

18. (huo2025modulatingheatinput pages 15-16): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

19. (tan2024effectofalni pages 2-4): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

20. (tan2024effectofalni pages 10-12): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

21. (tan2024effectofalni pages 1-2): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.
