<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 413b4e08-3e52-4cda-b8dd-f1257c3046db
- Submitted: 2026-10-17T05:10:46Z
- Fetched: 2026-10-17T05:42:08Z (status: success)
- Raw trajectory JSON: ../raw/b1-07-icme-calphad-cu.json.gz
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

QUESTION: What ICME and CALPHAD work exists for copper alloys in additive
manufacturing or welding? Cover thermodynamic and mobility databases for Cu
alloys (Thermo-Calc TCCU and MOBCU, others) and their validation for Cu-Ni-Fe-
Mn-Cr and Cu-Al-Ni-Fe-Mn; Scheil and back-diffusion predictions of
microsegregation in Cu-Ni; predictions of kappa phase and beta/martensite in
NAB under rapid cooling and cyclic reheating; and coupled thermal-history +
CALPHAD (or DICTRA / precipitation) models for DED. Also give two or three
examples, any alloy system, where coupling CALPHAD to a DED thermal model was
used to DESIGN a composition (e.g. steels, Ni superalloys, Ti) and was shown
to beat equilibrium-only CALPHAD.

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

QUESTION: What ICME and CALPHAD work exists for copper alloys in additive
manufacturing or welding? Cover thermodynamic and mobility databases for Cu
alloys (Thermo-Calc TCCU and MOBCU, others) and their validation for Cu-Ni-Fe-
Mn-Cr and Cu-Al-Ni-Fe-Mn; Scheil and back-diffusion predictions of
microsegregation in Cu-Ni; predictions of kappa phase and beta/martensite in
NAB under rapid cooling and cyclic reheating; and coupled thermal-history +
CALPHAD (or DICTRA / precipitation) models for DED. Also give two or three
examples, any alloy system, where coupling CALPHAD to a DED thermal model was
used to DESIGN a composition (e.g. steels, Ni superalloys, Ti) and was shown
to beat equilibrium-only CALPHAD.

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


# Copper-alloy ICME and CALPHAD for additive manufacturing and repair

**Assessment.** Copper-alloy thermodynamic and mobility databases, Cu–Ni rapid-solidification experiments, and substantial nickel–aluminum-bronze (NAB) welding literature exist. They do **not** yet establish a validated, thermal-history-aware composition-to-corrosion model for *single-stream, pre-alloyed-powder laser DED* on both cast NAB and wrought Cu–Ni. In particular, database coverage of the constituent elements is not evidence of validation of either proposed five-component composition space. No retrieved paper demonstrates that a newly designed composition beats wrought C71500 in seawater **as deposited**. Compositions below are wt% unless explicitly marked otherwise; unreported measurements are not inferred. (janssonUnknownyearphasetransformationsand pages 28-30, kuprienko2025analysisofnickel pages 30-36, lewis1981evaluationofcoppernickel pages 14-17)

## 1. Thermodynamic databases and Cu–Ni solidification

1. **Å. Jansson, Y. Tang, S. Jin, M. Ghasemi, C. M. Lancelot, N. Grundy, Q. Chen and J. Bratberg, “Phase Transformations and Kinetic Simulations of Cu-based Alloys,” *Copper Alloys 2022*, Düsseldorf, 22–23 November 2022, pp. 28–31. DOI: not identified for this conference contribution.** **Process:** calculations and comparisons with principally cast/conventionally processed Cu alloys, **not DED**. Thermo-Calc **TCCU5** contains 32 elements—including Cu, Al, Ni, Fe, Mn, Cr and O—315 solution/intermetallic phases, and assessments of 148 binaries and 64 ternaries. Companion **MOBCU5** includes liquid and FCC mobilities; the authors demonstrate Scheil, DICTRA and precipitation calculations. A Cu–5.2Sn–4.9Pb–4.5Zn DICTRA microsegregation profile at **0.16 °C/s** is compared with experiment, and Cu–1.86Ni–0.45Si precipitate growth is modeled at **675 °C**. These are **not** Cu–Ni–Fe–Mn–Cr or Cu–Al–Ni–Fe–Mn validation cases; no seawater, deposit, or powder tests are reported. **[CITE] [NUMBERS] [GAP]** Explicitly test predicted liquidus/solidus, phase identity, and diffusion against the actual candidate powder and deposits rather than treating element inclusion as validation. (janssonUnknownyearphasetransformationsand pages 28-30, janssonUnknownyearphasetransformationsand pages 30-32)

2. **A. Perron, J. D. Roehling, P. E. A. Turchi, J.-L. Fattebert and J. T. McKeown, “Matching time and spatial scales of rapid solidification: dynamic TEM experiments coupled to CALPHAD-informed phase-field simulations,” *Modelling and Simulation in Materials Science and Engineering* **26** (2018), 014002. DOI: 10.1088/1361-651X/aa9a5b.** **Process:** laser-melted **thin films**, neither DED nor production powder. Composition **Cu–44Ni at%**—approximately Cu–42Ni **wt%**, outside the proposed 10–30 wt% Ni range. Dynamic TEM measured interface velocities of approximately **0.1–0.6 m/s**, with reported cooling rates on the order of **8.1 × 10⁶–2.6 × 10⁷ K/s**. CALPHAD-informed phase-field calculations captured a transition toward solute trapping; experimentally observed columnar grains were effectively free of microsegregation under these conditions. No quantified Scheil-versus-back-diffusion comparison for 10–30Ni, Fe/Mn/Cr additions, DED cooling histories, or corrosion is reported. **[CITE] [NUMBERS] [GAP]** Do not assume that a zero-solid-diffusion Scheil calculation bounds measured Cu–Ni segregation accurately when interface trapping becomes important. (perron2018matchingtimeand pages 23-25, perron2018matchingtimeand pages 3-6, perron2018matchingtimeand pages 1-3)

3. **M. E. Balkan, *Thermochemical Modelling and Directed Energy Deposition of Copper-Nickel Functionally Gradient Materials*, MSc thesis, Sabancı University, December 2021. DOI: not identified.** **Process:** two-hopper, **in-situ blended blown-powder laser DED** on C45 steel—not a single pre-alloyed Cu–Ni powder. Despite the thesis title, its actual powders are **Cu–10Sn** and **IN718** (approximately 53.9Ni–18Cr–18Fe–5Nb–3Mo–1Ti–0.6Al); feed sizes **63–160 μm** and **45–106 μm**, respectively. FactSage **FSstel** equilibrium and Scheil calculations were compared with characterization of a **50:50 feed mixture**; measured mixed-build hardness was **225.76 ± 12.4 to 243.44 ± 13.4 HV**, and Archimedes density **8.4840 g/cm³**. Neither the latter value nor a description of apparently defect-free sections establishes relative density. No marine-corrosion test or measured powder oxygen/flow is supplied, and a DED thermal-history field was **not** supplied to CALPHAD. **[CITE] [NOVELTY-RISK] [GAP]** Establishes a Cu-bearing powder-DED thermochemical precedent, but not the proposed feedstock, substrates or performance objective. (balkan2021thermochemicalmodellingand pages 1-9, balkan2021thermochemicalmodellingand pages 43-48, balkan2021thermochemicalmodellingand pages 29-35, balkan2021thermochemicalmodellingand pages 56-63)

**Database decision.** TCCU/MOBCU are defensible starting points; FactSage FSstel is an example of an alternative calculation used for a *different*, Fe/Ni-rich dissimilar joint, not a demonstrated independent assessment of the intended copper spaces. The retrieved sources do not establish which Cu–Ni–Fe–Mn–Cr or Cu–Al–Ni–Fe–Mn higher-order interactions and κ-phase descriptions have been experimentally assessed, nor do they validate MOBCU for κ growth, β decomposition or the proposed DED histories. A comparison of **equilibrium**, **Scheil**, and **finite-diffusion/back-diffusion** predictions against measured interdendritic compositions, coupled with an explicit solute-trapping check, is therefore a testable ICME contribution rather than an already demonstrated copper result. (janssonUnknownyearphasetransformationsand pages 28-30, janssonUnknownyearphasetransformationsand pages 30-32, balkan2021thermochemicalmodellingand pages 43-48, perron2018matchingtimeand pages 23-25)

## 2. NAB κ, β and martensite: measured thermal-history constraints

4. **D. Ding, Z. Pan, S. Van Duin, H. Li and C. Shen, “Fabricating Superior NiAl Bronze Components through Wire Arc Additive Manufacturing,” *Materials* **9** (2016), 652. DOI: 10.3390/ma9080652.** **Process:** pulsed-GMAW **WAAM** on **cast NAB**, with no substrate preheat or powder. Wire specification: **Al 8.5–9.5, Ni 4–5.5, Fe 3–5.5, Mn 0.6–3.5, Cu balance**; cast substrate measured **Al 8.8, Ni 5.2, Fe 4.4, Mn 1.1, Cu balance**. Deposits were described as *fully dense*, but no defensible numerical pore fraction was located. The as-deposited metal contained Widmanstätten α and fine martensitic products; rapid cooling suppressed some β → α + κIII decomposition. **As-deposited** weld-metal hardness averaged **181 HV1**, versus **188 HV1** for cast substrate; weld-metal yield strength **339–342 MPa**, UTS **630–653 MPa**, and average elongation **27.8%**, versus cast substrate **332 MPa**, **689 MPa**, **25.3%**. A narrow, **<1 mm** substrate heat-affected zone transformed toward harder, less ductile martensite. There is **no corrosion test** in this article. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] [GAP]** The cast-NAB repair interface is established for *wire arc*, not corrosion-qualified pre-alloyed-powder laser DED. (ding2016fabricatingsuperiornial pages 3-6, ding2016fabricatingsuperiornial pages 1-3, ding2016fabricatingsuperiornial pages 6-9)

5. **A. Kuprienko, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*, PhD dissertation, Welding Engineering, Ohio State University, 2025. DOI: not identified.** **Process:** ONR-funded **wire-arc DED** deposit plus extracted-specimen Gleeble, furnace and resolidification experiments; **not laser powder DED**. Filler nominally **Cu 81.35–Al 9.09–Fe 3.94–Ni 4.53–Mn 1.00**. Single-sensor differential thermal analysis of specimens cooled at **0.1 °C/s** gave α onset **1015 °C**, κII onset/finish **1004/990 °C**, κIV onset **897 °C**, and κIII onset **717 °C**. At **424 °C/s** between 1000 and 800 °C, corresponding measured onsets were α **995 °C**, κII **962 °C**, κIV **868 °C**, and κIII **677 °C**. A **60 s** hold near **1035 °C** altered precipitation temperatures relative to shorter holds, even when cooling rates were similar; absence of a detectable κIV calorimetric peak did **not** establish absence of κIV by microscopy. The dissertation also reports that nitrogen cooling close behind the arc could cause a temperature dip/reheat and **lower**, rather than raise, local microhardness. It identifies ONR Manufacturing Science support. These are **experimental constraints**, not validated TCCU/MOBCU predictions; no seawater-performance comparison is furnished here. **[CITE] [NUMBERS] [NAVY] [GAP]** Repeated peak temperature, dwell and cooling segments must be retained in a NAB predictor. (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 137-142)

6. **A. Shahriari, D. Chalasani, B. S. Amirkhiz and M. Mohammadi, “Corrosion performance of wire arc additively manufactured NAB alloy,” *npj Materials Degradation* **7** (2023), article 84. DOI: 10.1038/s41529-023-00405-x.** **Process:** ERCuNiAl-wire **WAAM** on 316L, compared with **cast** NAB; the retrieved text does not securely establish an exact measured bulk composition. In **naturally aerated 3.5 wt% NaCl**, approximately **23 ± 2 °C**, open circuit was stabilized **1800 s**; EIS was measured at **100 kHz–0.01 Hz**, **10 mV**, and cyclic polarization at **0.166 mV/s**. As-built/cast immersion lasted **96 h**, heat-treated immersion **24 h**; do **not** interpret these as matched 30-day exposures. As-built WAAM had the largest EIS arc and better chloride resistance than the cast or heavily heat-treated conditions despite a less noble approximately **−0.293 V versus saturated Ag/AgCl** open-circuit potential, versus approximately **−0.222 V** for the other conditions. Heat treatments at **350 °C/2 h**, **550 °C/4 h**, and **675 °C/6 h** changed κ distributions; reported latter-condition corrosion currents were approximately **6.6** and **8 μA/cm²**, respectively. The paper attributes attack to cathodic κ constituents adjoining anodic Cu-rich α. An exact as-built *i*₍corr₎, density, strength, and powder metrics should **not** be claimed from the retrieved evidence. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** Direct precedent for *as-built* NAB chloride testing, but it is arc-wire and simple NaCl, not a laser-powder/C71500 seawater comparison. (shahriari2023corrosionperformanceof pages 10-12, shahriari2023corrosionperformanceof pages 5-8, shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 14-14, shahriari2023corrosionperformanceof pages 12-14)

7. **Y. Tan, H. Xie, X. Feng, S. Huang, W. Zhang, L. Peng, W. Wang and Y. Zhao, “Effect of Al/Ni Ratio on the Microstructure and Properties of Nickel–Aluminum Bronze Alloys,” *Materials* **17** (2024), 1330. DOI: 10.3390/ma17061330.** **Process:** **vacuum-induction cast**, not AM. Measured series, expressed as **Al/Ni/Fe/Mn**: **6.94/6.82/4.10/1.72; 7.90/6.13/3.92/2.12; 8.94/5.18/4.12/2.18; 9.94/3.99/3.94/1.82**, with Cu balance. **Static 3.5 wt% NaCl at 25 °C for 30 days**, refreshed every seven days—not ASTM D1141 or flowing seawater. Across the increasing Al/Ni series, hardness rose **104 → 202 HV**, UTS **356 → 751 MPa**, but elongation fell **50.5 → 11.0%**. The **6.94Al/6.82Ni** endpoint had a reported **0.00267 mm/y** 30-day mass-loss-derived rate. At day 30 the four alloys’ measured polarization-fit *i*₍corr₎ values were **0.35, 0.36, 0.69, 0.78 μA/cm²**; *E*₍corr₎ **−281.48, −295.55, −249.35, −257.75 mV**; and **EIS-fit** *R*ₚ **521,367, 196,434, 111,544, 90,707 Ω·cm²**, in the same alloy order. These EIS-fit resistances are distinct from the polarization-derived *R*ₚ values in that paper. Maximum local attack for the **9.94Al/3.99Ni** alloy exceeded **3 μm**. No CALPHAD-based additive-build or C71500 result is demonstrated. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** Especially relevant warning: lowering Ni while raising Al can buy hardness at a corrosion/ductility cost. (tan2024effectofalni pages 1-2, tan2024effectofalni pages 12-16, tan2024effectofalni pages 10-12, tan2024effectofalni pages 2-4, tan2024effectofalni media b97df175)

## 3. Corrosion controls appropriate to the Navy objective

8. **H. R. Jafari, A. Davoodi and S. Hosseinpour, “Effect of Fluid Flow on the Corrosion Performance of as-Cast and Heat-Treated Nickel Aluminum Bronze Alloy (UNS C95800) in Saline Solution,” *Corrosion and Materials Degradation* **2** (2021), 61–77. DOI: 10.3390/cmd2010004.** **Process:** **cast** and annealed **675 °C/6 h** C95800; measured **Al 8.79, Ni 4.50, Fe 3.70, Mn 1.00**, Cu balance. In **3.5 wt% NaCl** at **25 or 40 °C**, a rotating-disk electrode compared stationary conditions with **1,000, 3,000, 6,000, 9,000 rpm**; rpm should not be mislabeled as a specified seawater pipe-flow velocity. At **25 °C**, as-cast *i*₍corr₎ increased from **1.74 μA/cm²** static to **5.57 μA/cm²** at 9,000 rpm; annealed material increased from **0.918** to **5.22 μA/cm²**. At **40 °C**, as-cast values increased **3.37 → 8.97 μA/cm²**. Removing corrosion-sensitive retained β by annealing improved performance. **[CITE] [NUMBERS] [GAP]** A winning stagnant short-test alloy may not remain superior under service-relevant flow. (jafari2021effectoffluid pages 2-4, jafari2021effectoffluid pages 7-8)

9. **R. O. Lewis and F. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, technical report, 1981. DOI: 10.2172/6255887.** **Process:** synthesis of **wrought/conventional Cu–Ni** marine-service and exposure data, **not AM**. C71500 is approximately **Cu–30Ni–0.4–0.7Fe**, not pure binary Cu–30Ni. Reviewed seawater data place ordinary long-term average attack around **2.5–12.7 μm/y**, with **<2.5 μm/y** in some **14–16-year** quiescent/low-flow exposures; a separate **one-year**, **0.6 m/s** equal-area galvanic experiment recorded **20.3 μm/y** for uncoupled C71500. Rates depend strongly on flow, film maturation, exposure duration and galvanic geometry; these figures are **not interchangeable acceptance thresholds** for a 30-day salt test. **[CITE] [NUMBERS] [NAVY] [GAP]** Test an actual wrought C71500 coupon *alongside every candidate* in the same natural or ASTM D1141 seawater, with matched flow, exposure and exposed-area preparation. (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel pages 14-17)

10. **S. A. Campbell, G. J. W. Radford, C. D. S. Tuck and B. D. Barker, “Corrosion and Galvanic Compatibility Studies of a High-Strength Copper-Nickel Alloy,” *Corrosion* **58** (2002), 57–71. DOI: 10.5006/1.3277305.** **Process:** conventional high-strength **MARINEL Cu–Ni**, not DED. Measured **Ni 19.10, Mn 4.57, Al 1.90, Fe 1.18, Cr 0.41, Nb 0.72, Si 0.13, Cu balance**. In **natural seawater tidal-raft** exposures, average penetration-rate estimates declined from **0.058 ± 0.001 mm/y at 113 days** to **0.012 ± 0.003 mm/y at 660 days**; localized attack emerged after more than six months. Also investigated stainless-steel galvanic couples. **[CITE] [NUMBERS] [NAVY] [GAP]** Relevant lower-Ni, naval-oriented compositional precedent, but its Al/Nb additions, conventional production, and long-term natural-water behavior do not establish that a proposed Fe/Mn/Cr-only pre-alloyed DED powder will work. (campbell2002corrosionandgalvanic pages 1-2)

## 4. Thermal-history coupling versus *successful composition design*: do not conflate them

11. **S. Sridar, N. Sargent, X. Wang, M. A. Klecka and W. Xiong, “Determination of Location-Specific Solidification Cracking Susceptibility for a Mixed Dissimilar Alloy Processed by Wire-Arc Additive Manufacturing,” preprint, January 2022. DOI: 10.20944/preprints202201.0370.v1.** **Process:** **two-wire WAAM**, selected **26 wt% P91 / 74 wt% IN740H** blend; nominal composition **Al 1.037, C 0.046, Co 15.02, Cr 20.6, Cu 0.023, Fe 23.13, Mn 0.29, Mo 0.61, Nb 1.12, Ti 1.11, Si 0.14, V 0.06, Ni balance**. At **175 °C interpass**, locally inferred rates reached **270 K/s**. Measured dendrite spacing and local cooling rates entered **DICTRA**, and predicted solid-fraction curves were compared with equilibrium and Scheil: the DICTRA solidus lay **between** those endpoints, while the highest calculated cracking susceptibility matched the top region’s more extensive cracking. **Crucially, the chosen composition cracked**; this is evidence for improved *diagnosis* over equilibrium alone, **not** proof of successful history-informed composition design. No seawater or powder measurements. **[CITE] [NUMBERS] [GAP]** A useful methodological comparator and an instructive failed-design control. (sridar2022determinationoflocationspecific pages 1-2, sridar2022determinationoflocationspecific pages 7-12, sridar2022determinationoflocationspecific pages 4-5)

12. **T. Reindl, C. Koenig, A. Aslam, J. Vincic, J. R. Jinschek, A. Bastos Fanta and P. Mayr, “Cyclic heating effects on microstructure development in duplex stainless steel manufactured via wire-arc directed energy deposition,” *Multiscale and Multidisciplinary Modeling, Experiments and Design* **9** (2026), article 161. DOI: 10.1007/s41939-026-01247-1.** **Process:** existing **ER2209-wire WAAM**, not new composition design. Measured build thermal histories were reproduced in situ and tested against **CALPHAD-based precipitation/phase-kinetics** modeling. Austenite changed from about **57%** in fresh deposits to **80% after two reheating cycles**, illustrating why final equilibrium alone cannot describe position-dependent as-built phases. No copper, marine corrosion, composition optimization, or quantitative equilibrium-only design win. **[CITE] [NUMBERS] [GAP]** Particularly close *methodological* analogue for NAB κ evolution during cyclic reheating. (reindl2026cyclicheatingeffects pages 1-3)

13. **F. Markanday, G. Conduit, B. Conduit, J. Pürstl, K. Christofidou, L. Chechik, G. Baxter, C. Heason and H. Stone, “Design of a Ni-based superalloy for laser repair applications using probabilistic neural network identification,” *Data-Centric Engineering* **3** (2022), e30. DOI: 10.1017/dce.2022.31.** **Process:** designed for **blown-powder laser-DED repair**, but the retrieved experimental verification uses **arc-melted material and laser-pass tests**, **not a validated DED build**. Designed AM718R measured approximately **Al 1.2, Co 0.7, Cr 19.1, Fe 16.7, Mo 2.6, Nb 4.8, Ti 0.9, W 1.6, Ni balance**. Eutectic area fraction on the tested material was **1.7 ± 0.3%**, versus **3.4 ± 0.5%** for IN718. Thermodynamic features contributed to design, but no DED thermal-history-to-CALPHAD calculation or head-to-head demonstration against an equilibrium-only alloy selector is established. Its recommended precipitation treatment also conflicts with an *as-deposited* requirement. **[CITE] [NUMBERS] [GAP]** Genuine AM-oriented composition-selection precedent, **not** a qualifying example of the complete requested coupling. (markanday2022designofa pages 1-2, markanday2022designofa pages 13-16)

**Requested two or three fully qualifying success stories:** **not found.** The three studies above separately demonstrate location-aware diffusion-versus-equilibrium comparisons, cyclic-history-to-kinetics coupling, and thermodynamics-informed alloy selection. None establishes *all three together*: **DED heat-flow history → CALPHAD/DICTRA/precipitation-guided selection of a new composition → experimentally superior result compared with an equilibrium-only-selected composition**. Claiming they do would overstate the literature. (sridar2022determinationoflocationspecific pages 1-2, sridar2022determinationoflocationspecific pages 7-12, markanday2022designofa pages 13-16, reindl2026cyclicheatingeffects pages 1-3)

## Remaining qualification gap

No directly substantiated retrieved study combines **in-house ultrasonic-atomized, characterized single pre-alloyed Cu–Ni–Fe–Mn–Cr or Cu–Al–Ni–Fe–Mn powder**, quantitative **powder size/Hall flow/apparent density/oxygen**, density and crack mapping in both self-build and **cast-NAB/wrought-Cu–Ni repair interfaces**, phase/segregation validation along measured **laser-DED cyclic thermal histories**, and **matched as-deposited 30-day seawater-versus-wrought-C71500** corrosion—including selective-attack depth. The retrieved NAB corrosion comparisons generally use **3.5 wt% NaCl**, which is not natural or ASTM D1141 seawater; neither a corrosion current nor a calculated annualized short-test mass loss alone establishes long-term marine equivalence. The available literature also does not supply an experimentally validated correlation between candidate-powder oxygen/flow and that complete performance chain. (shahriari2023corrosionperformanceof pages 14-14, tan2024effectofalni pages 2-4, ding2016fabricatingsuperiornial pages 6-9, lewis1981evaluationofcoppernickel pages 14-17, balkan2021thermochemicalmodellingand pages 29-35)

## Top 5 things the PI should know

1. **Make the comparison falsifiable:** select candidates prospectively with identical budgets using thermal-history-aware ICME, equilibrium-only CALPHAD, and no-physics models; otherwise prior art supports only the *plausibility* of an ICME advantage, not the claimed design win. (sridar2022determinationoflocationspecific pages 7-12, reindl2026cyclicheatingeffects pages 1-3)
2. **Validate the copper database where it matters:** direct assessments of every proposed higher-order composition and fast-cooling κ/β kinetics were not established merely by TCCU/MOBCU element coverage. Measure phase identities and local solute profiles, including repair dilution zones. (janssonUnknownyearphasetransformationsand pages 28-30, janssonUnknownyearphasetransformationsand pages 30-32, kuprienko2025analysisofnickel pages 137-142)
3. **NAB thermal cycles are consequential and counterintuitive:** approximately **0.1 versus 424 °C/s** shifts measured κ onsets; an added cooling intervention can produce an intermediate reheat and softer metal. Model repeated passes, not only a single monotonic cooldown. (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 137-142)
4. **Design against selective attack, not just hardness or *E*₍corr₎:** the lower-Ni/higher-Al cast series became much stronger but more selectively attacked; WAAM NAB showed superior chloride resistance despite a **more negative** open-circuit potential. (shahriari2023corrosionperformanceof pages 2-2, tan2024effectofalni pages 12-16, tan2024effectofalni pages 10-12, tan2024effectofalni pages 2-4)
5. **The service benchmark requires an actual control:** run contemporaneous **wrought C71500** and both repair substrates under matched seawater chemistry, duration, flow and galvanic geometry; document deposit pores/cracks and lot-specific powder oxygen. Historical rates change with film maturity and hydrodynamics, so literature-only C71500 comparisons cannot demonstrate the proposal’s pass criterion. (jafari2021effectoffluid pages 7-8, campbell2002corrosionandgalvanic pages 1-2, lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel pages 14-17)

References

1. (janssonUnknownyearphasetransformationsand pages 28-30): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

2. (kuprienko2025analysisofnickel pages 30-36): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

3. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

4. (janssonUnknownyearphasetransformationsand pages 30-32): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

5. (perron2018matchingtimeand pages 23-25): Aurelien Perron, John D Roehling, Patrice E A Turchi, Jean-Luc Fattebert, and Joseph T McKeown. Matching time and spatial scales of rapid solidification: dynamic tem experiments coupled to calphad-informed phase-field simulations. Modelling and Simulation in Materials Science and Engineering, 26:014002, Dec 2018. URL: https://doi.org/10.1088/1361-651x/aa9a5b, doi:10.1088/1361-651x/aa9a5b. This article has 18 citations and is from a peer-reviewed journal.

6. (perron2018matchingtimeand pages 3-6): Aurelien Perron, John D Roehling, Patrice E A Turchi, Jean-Luc Fattebert, and Joseph T McKeown. Matching time and spatial scales of rapid solidification: dynamic tem experiments coupled to calphad-informed phase-field simulations. Modelling and Simulation in Materials Science and Engineering, 26:014002, Dec 2018. URL: https://doi.org/10.1088/1361-651x/aa9a5b, doi:10.1088/1361-651x/aa9a5b. This article has 18 citations and is from a peer-reviewed journal.

7. (perron2018matchingtimeand pages 1-3): Aurelien Perron, John D Roehling, Patrice E A Turchi, Jean-Luc Fattebert, and Joseph T McKeown. Matching time and spatial scales of rapid solidification: dynamic tem experiments coupled to calphad-informed phase-field simulations. Modelling and Simulation in Materials Science and Engineering, 26:014002, Dec 2018. URL: https://doi.org/10.1088/1361-651x/aa9a5b, doi:10.1088/1361-651x/aa9a5b. This article has 18 citations and is from a peer-reviewed journal.

8. (balkan2021thermochemicalmodellingand pages 1-9): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

9. (balkan2021thermochemicalmodellingand pages 43-48): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

10. (balkan2021thermochemicalmodellingand pages 29-35): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

11. (balkan2021thermochemicalmodellingand pages 56-63): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

12. (ding2016fabricatingsuperiornial pages 3-6): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

13. (ding2016fabricatingsuperiornial pages 1-3): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

14. (ding2016fabricatingsuperiornial pages 6-9): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

15. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

16. (kuprienko2025analysisofnickel pages 120-125): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

17. (kuprienko2025analysisofnickel pages 137-142): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

18. (shahriari2023corrosionperformanceof pages 10-12): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

19. (shahriari2023corrosionperformanceof pages 5-8): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

20. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

21. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

22. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

23. (tan2024effectofalni pages 1-2): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

24. (tan2024effectofalni pages 12-16): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

25. (tan2024effectofalni pages 10-12): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

26. (tan2024effectofalni pages 2-4): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

27. (tan2024effectofalni media b97df175): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

28. (jafari2021effectoffluid pages 2-4): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

29. (jafari2021effectoffluid pages 7-8): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

30. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

31. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

32. (campbell2002corrosionandgalvanic pages 1-2): S. A. Campbell, G. J. W. Radford, C. D. S. Tuck, and B. D. Barker. Corrosion and galvanic compatibility studies of a high-strength copper-nickel alloy. Corrosion, 58:57-71, Jan 2002. URL: https://doi.org/10.5006/1.3277305, doi:10.5006/1.3277305. This article has 97 citations and is from a peer-reviewed journal.

33. (sridar2022determinationoflocationspecific pages 1-2): Soumya Sridar, Noah Sargent, Xin Wang, Michael A. Klecka, and Wei Xiong. Determination of location-specific solidification cracking susceptibility for a mixed dissimilar alloy processed by wire-arc additive manufacturing. Metals, Jan 2022. URL: https://doi.org/10.20944/preprints202201.0370.v1, doi:10.20944/preprints202201.0370.v1. This article has 28 citations.

34. (sridar2022determinationoflocationspecific pages 7-12): Soumya Sridar, Noah Sargent, Xin Wang, Michael A. Klecka, and Wei Xiong. Determination of location-specific solidification cracking susceptibility for a mixed dissimilar alloy processed by wire-arc additive manufacturing. Metals, Jan 2022. URL: https://doi.org/10.20944/preprints202201.0370.v1, doi:10.20944/preprints202201.0370.v1. This article has 28 citations.

35. (sridar2022determinationoflocationspecific pages 4-5): Soumya Sridar, Noah Sargent, Xin Wang, Michael A. Klecka, and Wei Xiong. Determination of location-specific solidification cracking susceptibility for a mixed dissimilar alloy processed by wire-arc additive manufacturing. Metals, Jan 2022. URL: https://doi.org/10.20944/preprints202201.0370.v1, doi:10.20944/preprints202201.0370.v1. This article has 28 citations.

36. (reindl2026cyclicheatingeffects pages 1-3): T. Reindl, C. Koenig, A. Aslam, J. Vincic, J. R. Jinschek, A. Bastos Fanta, and P. Mayr. Cyclic heating effects on microstructure development in duplex stainless steel manufactured via wire-arc directed energy deposition. Multiscale and Multidisciplinary Modeling, Experiments and Design, Jul 2026. URL: https://doi.org/10.1007/s41939-026-01247-1, doi:10.1007/s41939-026-01247-1. This article has 0 citations.

37. (markanday2022designofa pages 1-2): Freddie Markanday, Gareth Conduit, Bryce Conduit, Julia Pürstl, Katerina Christofidou, Lova Chechik, Gavin Baxter, Christopher Heason, and Howard Stone. Design of a ni-based superalloy for laser repair applications using probabilistic neural network identification. Data-Centric Engineering, Oct 2022. URL: https://doi.org/10.1017/dce.2022.31, doi:10.1017/dce.2022.31. This article has 7 citations and is from a peer-reviewed journal.

38. (markanday2022designofa pages 13-16): Freddie Markanday, Gareth Conduit, Bryce Conduit, Julia Pürstl, Katerina Christofidou, Lova Chechik, Gavin Baxter, Christopher Heason, and Howard Stone. Design of a ni-based superalloy for laser repair applications using probabilistic neural network identification. Data-Centric Engineering, Oct 2022. URL: https://doi.org/10.1017/dce.2022.31, doi:10.1017/dce.2022.31. This article has 7 citations and is from a peer-reviewed journal.
