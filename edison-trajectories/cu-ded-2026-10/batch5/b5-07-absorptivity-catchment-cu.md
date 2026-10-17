<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: 04a840be-d0ab-4488-9e63-7a24cda84ce0
- Submitted: 2026-10-17T06:20:08Z
- Fetched: 2026-10-17T06:51:58Z (status: success)
- Raw trajectory JSON: ../raw/b5-07-absorptivity-catchment-cu.json.gz
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

QUESTION: What measured laser absorptivities exist for copper, Cu-Ni,
bronzes and NAB, as solid surfaces, powders, and melt pools, at 1030-1070 nm
(and 450-532 nm for comparison), e.g. from calorimetry or integrating-sphere
measurements during DED or LPBF? How do absorptivity and powder catchment
efficiency in coaxial blown-powder DED depend on particle size (e.g. 45-150
um), powder stream focus and laser spot for copper alloys, and which
analytical models of catchment (e.g. Ancalmo and Narra 2025) have been
validated? Give numbers usable to calibrate a heat-flow model for Cu-Ni and
NAB deposits.

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

QUESTION: What measured laser absorptivities exist for copper, Cu-Ni,
bronzes and NAB, as solid surfaces, powders, and melt pools, at 1030-1070 nm
(and 450-532 nm for comparison), e.g. from calorimetry or integrating-sphere
measurements during DED or LPBF? How do absorptivity and powder catchment
efficiency in coaxial blown-powder DED depend on particle size (e.g. 45-150
um), powder stream focus and laser spot for copper alloys, and which
analytical models of catchment (e.g. Ancalmo and Narra 2025) have been
validated? Give numbers usable to calibrate a heat-flow model for Cu-Ni and
NAB deposits.

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


# Optical coupling and powder catchment for copper-alloy laser DED

**Bottom line.** Published measurements provide useful *pure-copper* optical bounds and one quantitative *pure-copper* coaxial-DED building-efficiency benchmark. They do **not** establish an absorptivity or catchment-efficiency constant for pre-alloyed Cu–Ni or nickel–aluminum bronze (NAB) deposited at 1030–1070 nm. In particular, a stationary powder bed, a blown powder jet, and a molten track are different optical systems. No measured corrosion or mechanical property can be inferred from an absorptivity experiment. (kohl20213dprintingof pages 1-4, tertuliano2024highabsorptivitynanotextured pages 5-9, yamaguchi2024influenceofthe pages 2-4, piscopo2022anoverviewof pages 7-9)

## Measured optical benchmarks

1. **Spisz, E. W., A. J. Weigund, R. L. Bowmun, and J. R. Juck, *Solar Absorptances and Spectral Reflectances of 12 Metals for Temperatures Ranging from 300 to 500 K*, NASA TN D-5353 (1969); DOI not identified for this technical report.** **Process:** solid-metal optical characterization, *not* DED. **Composition:** elemental Cu. **Conditions/numbers:** for cleaned, as-received, approximately smooth but nonideal copper surfaces, spectral absorptance transcribed by Prasad and colleagues is **4.0% at 1085 nm, 54.5% at 525 nm, and 65.2% at 457 nm**. These are historical *surface* measurements, not Prasad’s in-process measurements; 1085 nm lies just outside the specified 1030–1070 nm interval. Temperature-dependent characterization covered 300–500 K. The later review’s broader room-temperature guide is approximately **5% IR, 40–45% green, and up to 65% blue**, illustrating that quoted green values depend on source and surface. **Tags:** [CITE] [NUMBERS] [GAP: no NAB/Cu–Ni molten-track measurement]. (prasad2020lasermetaldeposition pages 10-10, prasad2020lasermetaldeposition pages 1-3, canacoo2026laseradditivemanufacturing media 4cae5474)

2. **Kohl, H., L. Schade, G. Matthäus, T. Ullsperger, B. Yürekli, B. Seyfarth, B. Braun, and S. Nolte, “3D printing of high-density copper parts using common NIR CW laser systems at moderate powers,” *Lasers in Manufacturing Conference* (2021); DOI not verified.** **Process:** offline powder integrating-sphere test and separate **LPBF**, not blown-powder DED. **Composition:** 99.7%-pure Cu. **Conditions/numbers:** spherical powder of approximately **14 µm mean diameter**, **56% relative powder packing density**; under nitrogen, approximately **2 W**, **3-mm illuminated diameter**, **0.5-s** measurement, the **1070-nm reflectivity was 56%**. Assuming negligible transmission through the powder sample, this implies **44% effective stationary-powder absorptance**. Measured powder thermal conductivity was **0.19 W m⁻¹ K⁻¹**. Separately, LPBF at **1070 nm**, a **30-µm beam**, **200 W**, **500 mm s⁻¹**, **80-µm hatch** and **25-µm layers** reached approximately **99% relative density**. The 44% measurement must *not* be applied unaltered to 45–150-µm flying particles or a DED melt pool. **Tags:** [CITE] [NUMBERS] [GAP]. (kohl20213dprintingof pages 1-4, kohl20213dprintingof pages 4-8)

3. **Tertuliano, O. A., P. J. DePond, A. C. Lee, J. Hong, D. Doan, L. Capaldi, M. Brongersma, X. W. Gu, M. J. Matthews, W. Cai, and A. J. Lew, “High absorptivity nanotextured powders for additive manufacturing,” *Science Advances* **10** (2024), DOI **10.1126/sciadv.adp0003**.** **Process:** irradiated **LPBF powder-bed calorimetry**, not static-sphere testing or DED. **Composition:** unmodified **99.95%-pure Cu**, compared with chemically nanotextured Cu; Cu–Ag powder was also investigated, but is not Cu–Ni. **Conditions/numbers:** at **175 W** and **60-µm 1/e² beam diameter**, unmodified Cu’s effective absorptivity was **0.172 at 100 mm s⁻¹** and **0.219 at 656 mm s⁻¹**. Five-hour-etched Cu measured **0.286** and **0.372**, respectively; modifying the surface thus altered the measured coupling substantially without changing nominal bulk Cu chemistry. The paper describes near-IR LPBF generally as **1060–1080 nm**, but the examined excerpt does **not** establish the exact experimental wavelength: do not advertise these values as a verified measurement at precisely 1064 or 1070 nm. Its simulated 20-/40-µm bimodal powder is **not** a measured 45–150-µm DED size comparison. **Tags:** [CITE] [NUMBERS] [GAP]. (tertuliano2024highabsorptivitynanotextured pages 5-9, tertuliano2024highabsorptivitynanotextured pages 1-5)

4. **Nordet, G., C. Gorny, Y. Mayi, J. Daligault, M. Dal, A. Effernelli, E. Blanchet, F. Coste, and P. Peyre, “Absorptivity measurements during laser powder bed fusion of pure copper with a 1 kW cw green laser,” *Optics & Laser Technology* **147** (2022), 107612, DOI **10.1016/j.optlastec.2021.107612**.** **Process:** **green-laser LPBF**, time-resolved integrating-sphere measurement; primary full text was unavailable, so the following values come through a later review. **Composition:** pure Cu. **Conditions/numbers:** approximately **75%** for the initially solid/powder-bed state, **50–60%** after a liquid *conduction-mode* pool forms, and **80–90%** during keyholing. These values establish that absorptivity can **decrease upon forming a liquid pool** at green wavelength, then increase in a keyhole; they are not measured green DED values. A later review separately reports solid bulk Cu at IR increasing from about **4–5%** to **11–16%** on melting, without sufficiently specified primary experimental conditions to transfer that range to Cu–Ni or NAB. **Tags:** [CITE] [NUMBERS] [GAP]. (allen2023sheddinglighton pages 163-168, canacoo2026laseradditivemanufacturing pages 14-15)

5. **Jadhav, S. D., and colleagues, “Surface Modified Copper Alloy Powder for Reliable Laser-based Additive Manufacturing,” *Additive Manufacturing* **35** (2020), 101418; DOI not independently verified in the retrieved material.** **Process:** modified-powder **LPBF**. **Composition:** nominal **Cu–1 wt% Cr (CuCr1)**, *not* marine Cu–Ni. **Conditions/numbers:** a **750 °C, 1-h nitrogen treatment** produced a Cr/Cr-nitride-enriched powder surface; a later review reports powder absorbance rising from **34% to 68%** and finished-part density around **98–99%**. Wavelength and optical measurement geometry for that pair were not established from the available excerpts. These are evidence that **surface condition and oxygen/nitride chemistry matter**, not validated NAB input values. **Tags:** [CITE] [NUMBERS] [GAP]. (canacoo2026laseradditivemanufacturing pages 9-10, canacoo2026laseradditivemanufacturing pages 14-15)

6. **Jadhav, S. D., D. Fu, M. Deprez, K. Ramharter, D. Willems, B. Van Hooreweder, and K. Vanmeensel, “Highly conductive and strong CuSn0.3 alloy processed via laser powder bed fusion starting from a tin-coated copper powder,” *Additive Manufacturing* **36** (2020), 101607, DOI **10.1016/j.addma.2020.101607**.** **Process:** **LPBF** of *tin-coated Cu powder*, not pre-alloyed blown powder. **Composition:** approximately **Cu–0.3 wt% Sn** in the resulting alloy. **Conditions/numbers:** a review reports about **62-nm Sn coating** and powder absorptivity increasing from **19% to 51%**; reported part density **99.6%**, tensile strength **256 MPa**, conductivity **80% IACS**. The wavelength and measurement geometry underlying the 19%/51% values were not verified in the available primary text. This is a dilute tin-bronze *powder-surface* comparator, **not** a Cu–Al bronze or NAB absorptivity measurement. **Tags:** [CITE] [NUMBERS] [GAP]. (canacoo2026laseradditivemanufacturing pages 37-38, canacoo2026laseradditivemanufacturing pages 14-15)

**Unmeasured in the material retrieved:** a verified 1030–1070-nm absorptivity for **C71500, Cu–10–30 wt% Ni–Fe/Mn/Cr powders or tracks, aluminum bronze, or NAB**, stratified into solid substrate, atomized powder, in-flight particles, conduction melt pool, and keyhole; corresponding 450–532-nm material-specific curves are likewise absent. CuSn0.3, CuCr1, and elemental Cu are *comparators*, not composition-matched calibration data. (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 12-14, allen2023sheddinglighton pages 163-168, tertuliano2024highabsorptivitynanotextured pages 5-9)

## Blown-powder DED: incorporation, focus, and model validation

7. **Yamaguchi, M., N. Kato, Y. Funada, T. Yachi, A. Saikai, and T. Furumoto, “Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser,” *International Journal of Advanced Manufacturing Technology* **135** (2024), 5235–5251, DOI **10.1007/s00170-024-14789-w**.** **Process:** **445-nm, three-beam coaxial blown-powder laser DED** on **AISI 304** steel, not a single IR laser. **Composition:** pure Cu powder; reported particle sizes **D₁₀–D₉₀ = 31–71 µm, D₅₀ = 46 µm**. **Conditions/numbers:** **0.2-mm laser spot**, **10 mm s⁻¹**, argon, **3-mm nozzle-to-build stand-off**, **10 or 20 mg s⁻¹** feed. The best reported **36% building efficiency** and **0.1% sectional porosity** were at **180 W, 10 mg s⁻¹**. At **20 mg s⁻¹** and **0.4-mm hatch**, increasing power from **150 to 240 W** increased efficiency from **21% to 32%** and reduced porosity from **0.7% to 0.3%**, but increased substrate dilution. Critically, “building efficiency” is calculated as **deposited geometric volume × assumed Cu density / estimated supplied powder mass**: substrate dilution and nominal feed-rate uncertainty can make it differ from rigorously weighed powder catchment. **No absorptivity was measured.** **Tags:** [CITE] [NUMBERS] [GAP: different wavelength/substrate/alloy]. (yamaguchi2024influenceofthe pages 2-4, yamaguchi2024influenceofthe pages 4-5, yamaguchi2024influenceofthe pages 10-12, yamaguchi2024influenceofthe pages 1-2)

8. **Prasad, H. S., F. Brueckner, J. Volpp, and A. F. H. Kaplan, “Laser metal deposition of copper on diverse metals using green laser sources,” *International Journal of Advanced Manufacturing Technology* **107** (2020), 1559–1568, DOI **10.1007/s00170-020-05117-z**.** **Process:** **515-nm coaxial ring-slit blown-powder laser metal deposition**. **Composition:** **99.9%-pure Cu**, **50–90-µm powder**, on sandblasted Cu and Al, H13 tool steel, and Ti–6Al–4V. **Conditions/numbers:** **1.7-mm Gaussian spot**, **200–1000 W**, **0.1–0.5 m min⁻¹**, **0.65–3.9 g min⁻¹**. At **1 kW**, high-speed imaging found approximately **0.3 ms** powder incorporation on Cu versus **0.1–0.2 ms** on other substrates. The authors calculated a **0.73% lower-bound fraction of incident power expended *purely on melting*** for a copper-on-copper single track, versus **2.66%** for a wall, and **2.94%/5.15%/9.78%** on Al/tool-steel/Ti-alloy substrates. **Those percentages are neither optical absorptivity nor mass catchment efficiency**. The small, steep Cu-supported pool qualitatively lowers capture probability; no Cu-specific measured mass-capture percentage is given. **Tags:** [CITE] [NUMBERS] [GAP]. (prasad2020lasermetaldeposition pages 3-4, prasad2020lasermetaldeposition pages 9-10, prasad2020lasermetaldeposition pages 1-3)

9. **Williams, N., K. Snyder, I. Smith, A. Duong, E. Carpenter, and R. Barua, “The First Layer: Single-Track Insights into Direct Energy Deposition Processed Cu-Ni Thermoelectric Alloys,” *Journal of Manufacturing and Materials Processing* **9** (2025), 170, DOI **10.3390/jmmp9060170**.** **Process:** laser blown-powder **DED** of **mechanically premixed *elemental* Cu and Ni powders onto 316L steel**, *not pre-alloyed powder* and not seawater repair. **Composition:** the methods state **65:35 atomic Cu:Ni** but subsequently call it **65:35 wt%**; the former converts to approximately **66.8 wt% Cu–33.2 wt% Ni**. **Conditions/numbers:** **57 ± 15 µm** mean particles; apparent/tap densities **4.74/5.20 g cm⁻³**, Hall flow **0.3 g s⁻¹**; **800 W**, linear heat input **63–137 J mm⁻¹** and incoming linear powder mass **0.011–0.026 g mm⁻¹**. *Neither powder catchment nor optical absorptivity was measured.* Its reported optimal “**4000 ± 500 kJ g⁻¹**” contains a **1000-fold unit error**: dividing roughly 70 J mm⁻¹ by 0.016–0.021 g mm⁻¹ gives approximately **3.3–4.4 kJ g⁻¹**, not thousands of kJ g⁻¹. The elemental-powder segregation/incomplete Ni-melting problem creates a **[NOVELTY-RISK]** for broad claims about “first Cu–Ni DED,” but does **not** preempt single-stream *pre-alloyed* Cu–Ni powder or marine qualification. **Tags:** [CITE] [NUMBERS] [NOVELTY-RISK] [GAP]. (williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 4-6, williams2025thefirstlayer pages 9-11)

10. **Haghshenas, A., A. Bohlen, D. Tyralla, and R. Groll, “The relevance of wall roughness modeling for simulation of powder flows in laser metal deposition nozzles,” *International Journal of Advanced Manufacturing Technology* **123** (2022), 1441–1458, DOI **10.1007/s00170-022-10186-3**.** **Process:** high-speed-video/large-eddy-simulation **single vertical jet**, **not coaxial DED catchment**. **Composition:** 316L steel powder, separated into **45–53, 71–80, and 90–100 µm** experimental fractions. **Key finding:** larger particles and rougher nozzle walls reduced speed and broadened jet divergence, with particle-size-effect saturation; the nozzle had **1.7-mm bore**, and measured roughness-angle dispersion was approximately **5.9°**. This supports **measuring the actual size-resolved powder footprint rather than assuming that 45–150 µm share one trajectory**. It supplies *no* defensible Cu-alloy capture percentage or universal monotonic catchment-versus-size law. **Tags:** [CITE] [NUMBERS] [GAP]. (haghshenas2022therelevanceof pages 1-2, haghshenas2022therelevanceof pages 3-6)

11. **Maffia, S., F. Chiappini, G. Maggiani, V. Furlan, M. Guerrini, and B. Previtali, “Enhancing productivity and efficiency in conventional laser metal deposition process for Inconel 718—Part II: advancing the process performance,” *International Journal of Advanced Manufacturing Technology* **129** (2023), 279–298, DOI **10.1007/s00170-023-12197-0**.** **Process:** coaxial conventional laser metal deposition on steel. **Composition:** **IN718 Ni-based superalloy**, *not* Cu–Ni. **Conditions/numbers:** optimized thick walls reached **70% powder catchment** at **1500 g h⁻¹** deposition; catchment was inferred from measured wall geometry, density and fed powder. This shows that 36% is **not** a universal DED efficiency, while 70% is **not** a justified assumption for Cu–Ni/NAB. **Tags:** [CITE] [NUMBERS] [GAP]. (maffia2023enhancingproductivityand pages 1-2, maffia2023enhancingproductivityand pages 3-5)

12. **Ancalmo, C., and S. P. Narra, “Prediction of the powder catchment efficiency and melt track height in laser directed energy deposition,” *Journal of Manufacturing Processes* **137** (2025), 207–220, DOI **10.1016/j.jmapro.2025.01.039**.** **Process:** analytical laser-DED catchment/height modeling. **Composition, size/spot settings, experimental validation error, and materials tested: *not verified***: its full text could not be retrieved, and a subsequent review lists its citation without those results. It is an essential modeling paper to inspect before a proposal claims a new analytical catchment model, but it cannot be called **validated specifically for Cu–Ni, NAB, or even for a specified alloy** on the evidence available. **Tags:** [CITE] [NOVELTY-RISK: predicts the proposed intermediate quantity] [GAP: copper-alloy validation unestablished]. (araujo2025powdergasjetstream pages 43-44, canacoo2026laseradditivemanufacturing pages 36-37)

**Which model ideas have experimental support?** Liu, Z., H. Zhang, S. Peng, H. Kim, D. Du, and W. Cong, “Analytical modeling and experimental validation of powder stream distribution during direct energy deposition,” *Additive Manufacturing* **30** (2019), 100848, DOI **not verified here**, explicitly validates **jet distribution**; Tabernero, I., A. Lamikiz, E. Ukar, L. N. López de Lacalle, C. Angulo, and G. Urbikain, “Numerical simulation and experimental validation of powder flux distribution in coaxial laser cladding,” *Journal of Materials Processing Technology* **210** (2010), 2125–2134, DOI **not verified here**, likewise validates **coaxial flux distribution**. Eisenbarth, D., P. M. Borges Esteves, F. Wirth, and K. Wegener, “Spatial powder flow measurement and efficiency prediction for laser direct metal deposition,” *Surface & Coatings Technology* **362** (2019), 397–408, DOI **10.1016/j.surfcoat.2019.02.009**, measured the spatial jet using a traversed pinhole and predicted efficiency. The retrieved reviews document these methods but do not provide verified Cu–Ni/NAB experimental accuracy for any of them. **Geometric jet–pool overlap is an upper-bound/intermediate predictor, not proof that every intercepted particle melts and stays attached.** (araujo2025powdergasjetstream pages 43-44, araujo2025powdergasjetstream pages 8-11, santoni2025ontheextent pages 34-36, santoni2025ontheextent pages 12-14)

At the powder-focus plane the measured flux concentrates; below focus its peak falls and footprint spreads. Positioning the working surface at the powder focus and measuring the powder footprint *relative to the actual molten width*, rather than laser-spot diameter alone, is therefore essential. Higher gas flow can move or broaden that focus, and the substrate itself perturbs the impinging jet. None of the cited data establish a numerical improvement in catchment when a Cu–Ni/NAB nozzle is moved a particular number of millimeters or its spot changed to a particular diameter. (piscopo2022anoverviewof pages 7-9, piscopo2022anoverviewof pages 9-12, araujo2025powdergasjetstream pages 8-11, prasad2020lasermetaldeposition pages 3-4)

## Heat-flow calibration and exclusions

For a **1030–1070-nm Cu–Ni or NAB DED model**, treat **~0.04–0.05** as a *clean, cool elemental-Cu solid-surface comparison only*, **0.44** as a *14-µm stationary Cu powder-bed comparison only*, and **0.17–0.22** as *irradiated Cu LPBF effective-absorptivity comparisons, with exact wavelength unconfirmed*. None is a measured Cu–Ni/NAB coefficient. Treat the observed **21–36%** blue-Cu DED building efficiencies as a **sensitivity-analysis range for mass utilization**, not as an alloy-independent prior or optical absorption; **70%** represents an optimized *IN718* counterexample. Fit separate parameters for substrate/track optical coupling, powder-beam attenuation and heating, and actual deposited-to-delivered mass. Do not multiply a powder-bed absorptance by a capture fraction and call that the measured substrate heat input. (prasad2020lasermetaldeposition pages 1-3, kohl20213dprintingof pages 1-4, tertuliano2024highabsorptivitynanotextured pages 5-9, yamaguchi2024influenceofthe pages 2-4, yamaguchi2024influenceofthe pages 10-12, maffia2023enhancingproductivityand pages 1-2, piscopo2022anoverviewof pages 9-12)

**Evidence absent from these optical/catchment items:** seawater or **3.5 wt% NaCl/ASTM D1141** test salinity, immersion duration and flow; **Ecorr, corrosion current/rate, impedance, selective-attack depth**; Cu–Ni/NAB repair strength and elongation; and DED powder **oxygen-per-lot** values. Those properties were *not measured in the cited optical studies* and cannot responsibly be filled with unrelated alloy values. The full text required to establish Ancalmo–Narra’s tested alloy, model equations and validation error was unavailable. No Navy/DoD support is substantiated for the enumerated quantitative optical/catchment studies; **[NAVY] is consequently not assigned on conjecture**. (kohl20213dprintingof pages 1-4, yamaguchi2024influenceofthe pages 2-4, prasad2020lasermetaldeposition pages 3-4, tertuliano2024highabsorptivitynanotextured pages 5-9, araujo2025powdergasjetstream pages 43-44)

## Top 5 things the PI should know

1. **The key calibration gap is real:** no verified composition-, state- and wavelength-matched **Cu–Ni/NAB DED absorptivity** or 45–150-µm capture curve was established; measure both on the actual atomized lots and substrates. (canacoo2026laseradditivemanufacturing pages 14-15, kohl20213dprintingof pages 1-4, yamaguchi2024influenceofthe pages 2-4, araujo2025powdergasjetstream pages 43-44)
2. **Keep optical states separate.** At roughly 1 µm, elemental solid Cu is around **4–5%**, whereas a particular *stationary fine-powder bed* gave **44%**; LPBF calorimetry yielded **17–22%** for untreated Cu under different irradiation conditions. These are not contradictory measurements of one property. (prasad2020lasermetaldeposition pages 1-3, kohl20213dprintingof pages 1-4, tertuliano2024highabsorptivitynanotextured pages 5-9)
3. **Calibrate delivered mass independently of energy coupling.** The strongest directly documented Cu coaxial-DED benchmark here is **36% volume-based building efficiency**, at **445 nm**, **46-µm D₅₀**, and **0.2-mm spot**; it is not an IR Cu–Ni catchment measurement. (yamaguchi2024influenceofthe pages 2-4, yamaguchi2024influenceofthe pages 4-5)
4. **Measure powder-focus overlap and incorporation separately:** size fraction, nozzle stand-off, actual jet footprint, melt-pool width and bouncing/retention all matter; validated steel jet-distribution models and Ancalmo–Narra are starting points, **not Cu–Ni/NAB validations**. (haghshenas2022therelevanceof pages 3-6, piscopo2022anoverviewof pages 7-9, santoni2025ontheextent pages 12-14, araujo2025powdergasjetstream pages 43-44)
5. **Position novelty precisely:** mixed-*elemental* Cu–Ni DED and Cu–Al alloy DED already exist, while the retrieved material does not demonstrate a **single-stream pre-alloyed powder → NAB/Cu–Ni repair → as-deposited seawater performance** result. Do not reuse Williams’s apparent **1000-fold kJ/g error** or mistake optical benchmarks for marine-property benchmarks. (williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 9-11, canacoo2026laseradditivemanufacturing pages 12-14)

References

1. (kohl20213dprintingof pages 1-4): H Kohl, L Schade, G Matthäus, and T Ullsperger. 3d printing of high-density copper parts using common nir cw laser systems at moderate powers. Unknown journal, 2021.

2. (tertuliano2024highabsorptivitynanotextured pages 5-9): Ottman A. Tertuliano, Philip J. DePond, Andrew C. Lee, Jiho Hong, David Doan, Luc Capaldi, Mark Brongersma, X. Wendy Gu, Manyalibo J. Matthews, Wei Cai, and Adrian J. Lew. High absorptivity nanotextured powders for additive manufacturing. Science Advances, Sep 2024. URL: https://doi.org/10.1126/sciadv.adp0003, doi:10.1126/sciadv.adp0003. This article has 44 citations and is from a highest quality peer-reviewed journal.

3. (yamaguchi2024influenceofthe pages 2-4): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

4. (piscopo2022anoverviewof pages 7-9): Gabriele Piscopo, Eleonora Atzeni, Abdollah Saboori, and Alessandro Salmi. An overview of the process mechanisms in the laser powder directed energy deposition. Applied Sciences, 13:117, Dec 2022. URL: https://doi.org/10.3390/app13010117, doi:10.3390/app13010117. This article has 111 citations.

5. (prasad2020lasermetaldeposition pages 10-10): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

6. (prasad2020lasermetaldeposition pages 1-3): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

7. (canacoo2026laseradditivemanufacturing media 4cae5474): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

8. (kohl20213dprintingof pages 4-8): H Kohl, L Schade, G Matthäus, and T Ullsperger. 3d printing of high-density copper parts using common nir cw laser systems at moderate powers. Unknown journal, 2021.

9. (tertuliano2024highabsorptivitynanotextured pages 1-5): Ottman A. Tertuliano, Philip J. DePond, Andrew C. Lee, Jiho Hong, David Doan, Luc Capaldi, Mark Brongersma, X. Wendy Gu, Manyalibo J. Matthews, Wei Cai, and Adrian J. Lew. High absorptivity nanotextured powders for additive manufacturing. Science Advances, Sep 2024. URL: https://doi.org/10.1126/sciadv.adp0003, doi:10.1126/sciadv.adp0003. This article has 44 citations and is from a highest quality peer-reviewed journal.

10. (allen2023sheddinglighton pages 163-168): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

11. (canacoo2026laseradditivemanufacturing pages 14-15): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

12. (canacoo2026laseradditivemanufacturing pages 9-10): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

13. (canacoo2026laseradditivemanufacturing pages 37-38): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

14. (canacoo2026laseradditivemanufacturing pages 12-14): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

15. (yamaguchi2024influenceofthe pages 4-5): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

16. (yamaguchi2024influenceofthe pages 10-12): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

17. (yamaguchi2024influenceofthe pages 1-2): Mitsugu Yamaguchi, Naoki Kato, Yoshinori Funada, Taisei Yachi, Ayahito Saikai, and Tatsuaki Furumoto. Influence of the laser power and powder feed rate on the porosity, dilution, and building efficiency of pure copper parts fabricated via directed energy deposition with a blue laser. The International Journal of Advanced Manufacturing Technology, 135:5235-5251, Nov 2024. URL: https://doi.org/10.1007/s00170-024-14789-w, doi:10.1007/s00170-024-14789-w. This article has 6 citations.

18. (prasad2020lasermetaldeposition pages 3-4): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

19. (prasad2020lasermetaldeposition pages 9-10): Himani Siva Prasad, Frank Brueckner, Joerg Volpp, and Alexander F. H. Kaplan. Laser metal deposition of copper on diverse metals using green laser sources. The International Journal of Advanced Manufacturing Technology, 107:1559-1568, Mar 2020. URL: https://doi.org/10.1007/s00170-020-05117-z, doi:10.1007/s00170-020-05117-z. This article has 164 citations.

20. (williams2025thefirstlayer pages 2-4): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

21. (williams2025thefirstlayer pages 4-6): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

22. (williams2025thefirstlayer pages 9-11): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

23. (haghshenas2022therelevanceof pages 1-2): Armin Haghshenas, Annika Bohlen, Dieter Tyralla, and Rodion Groll. The relevance of wall roughness modeling for simulation of powder flows in laser metal deposition nozzles. The International Journal of Advanced Manufacturing Technology, 123:1441-1458, Oct 2022. URL: https://doi.org/10.1007/s00170-022-10186-3, doi:10.1007/s00170-022-10186-3. This article has 15 citations.

24. (haghshenas2022therelevanceof pages 3-6): Armin Haghshenas, Annika Bohlen, Dieter Tyralla, and Rodion Groll. The relevance of wall roughness modeling for simulation of powder flows in laser metal deposition nozzles. The International Journal of Advanced Manufacturing Technology, 123:1441-1458, Oct 2022. URL: https://doi.org/10.1007/s00170-022-10186-3, doi:10.1007/s00170-022-10186-3. This article has 15 citations.

25. (maffia2023enhancingproductivityand pages 1-2): Simone Maffia, Federico Chiappini, Gianluca Maggiani, Valentina Furlan, Massimo Guerrini, and Barbara Previtali. Enhancing productivity and efficiency in conventional laser metal deposition process for inconel 718 – part ii: advancing the process performance. The International Journal of Advanced Manufacturing Technology, 129:279-298, Sep 2023. URL: https://doi.org/10.1007/s00170-023-12197-0, doi:10.1007/s00170-023-12197-0. This article has 17 citations.

26. (maffia2023enhancingproductivityand pages 3-5): Simone Maffia, Federico Chiappini, Gianluca Maggiani, Valentina Furlan, Massimo Guerrini, and Barbara Previtali. Enhancing productivity and efficiency in conventional laser metal deposition process for inconel 718 – part ii: advancing the process performance. The International Journal of Advanced Manufacturing Technology, 129:279-298, Sep 2023. URL: https://doi.org/10.1007/s00170-023-12197-0, doi:10.1007/s00170-023-12197-0. This article has 17 citations.

27. (araujo2025powdergasjetstream pages 43-44): João Pedro Madeira Araujo, Jhonattan Gutjahr, Qingping Yang, and Diane Mynors. Powder-gas jet stream characterisation techniques in laser directed energy deposition: a systematic review. Processes, 13:2995, Sep 2025. URL: https://doi.org/10.3390/pr13092995, doi:10.3390/pr13092995. This article has 0 citations.

28. (canacoo2026laseradditivemanufacturing pages 36-37): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

29. (araujo2025powdergasjetstream pages 8-11): João Pedro Madeira Araujo, Jhonattan Gutjahr, Qingping Yang, and Diane Mynors. Powder-gas jet stream characterisation techniques in laser directed energy deposition: a systematic review. Processes, 13:2995, Sep 2025. URL: https://doi.org/10.3390/pr13092995, doi:10.3390/pr13092995. This article has 0 citations.

30. (santoni2025ontheextent pages 34-36): Alberto Santoni, Eleonora Santecchia, Anna Maria Schiavone, Valentina Latini, Bogdan Daniel Lascu, and Constantin Romica Stoica. On the extent of feedstock–system interaction in determining the efficiency of laser powder directed energy deposition. Metals, 15:599, May 2025. URL: https://doi.org/10.3390/met15060599, doi:10.3390/met15060599. This article has 9 citations.

31. (santoni2025ontheextent pages 12-14): Alberto Santoni, Eleonora Santecchia, Anna Maria Schiavone, Valentina Latini, Bogdan Daniel Lascu, and Constantin Romica Stoica. On the extent of feedstock–system interaction in determining the efficiency of laser powder directed energy deposition. Metals, 15:599, May 2025. URL: https://doi.org/10.3390/met15060599, doi:10.3390/met15060599. This article has 9 citations.

32. (piscopo2022anoverviewof pages 9-12): Gabriele Piscopo, Eleonora Atzeni, Abdollah Saboori, and Alessandro Salmi. An overview of the process mechanisms in the laser powder directed energy deposition. Applied Sciences, 13:117, Dec 2022. URL: https://doi.org/10.3390/app13010117, doi:10.3390/app13010117. This article has 111 citations.
