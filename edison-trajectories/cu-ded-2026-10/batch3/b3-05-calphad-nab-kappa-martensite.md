<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: 99c12723-c37b-4550-9bd5-47d18750c625
- Submitted: 2026-10-17T05:46:06Z
- Fetched: 2026-10-17T06:16:56Z (status: success)
- Raw trajectory JSON: ../raw/b3-05-calphad-nab-kappa-martensite.json.gz
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

QUESTION: How well can CALPHAD and related models predict the phases of
nickel-aluminum bronze after rapid cooling and reheating? Cover: published
thermodynamic assessments of Cu-Al-Ni-Fe(-Mn) and how kappa phases (kappa-I/
II Fe3Al-based, kappa-III NiAl B2, kappa-IV) and beta/beta-prime are
modeled; the Thermo-Calc TCCU versions and any published validation for
NAB; measured vs calculated beta solvus, eutectoid and kappa-precipitation
temperatures (e.g. DTA data at different cooling rates, Kuprienko 2025);
empirical or model equations for the martensite start temperature of
Cu-Al(-Ni-Fe-Mn) as a function of composition; and critical cooling rates
for retaining beta-prime. Which of these quantities could be computed per
candidate composition as a cheap physics node, and how accurate are they?

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

QUESTION: How well can CALPHAD and related models predict the phases of
nickel-aluminum bronze after rapid cooling and reheating? Cover: published
thermodynamic assessments of Cu-Al-Ni-Fe(-Mn) and how kappa phases (kappa-I/
II Fe3Al-based, kappa-III NiAl B2, kappa-IV) and beta/beta-prime are
modeled; the Thermo-Calc TCCU versions and any published validation for
NAB; measured vs calculated beta solvus, eutectoid and kappa-precipitation
temperatures (e.g. DTA data at different cooling rates, Kuprienko 2025);
empirical or model equations for the martensite start temperature of
Cu-Al(-Ni-Fe-Mn) as a function of composition; and critical cooling rates
for retaining beta-prime. Which of these quantities could be computed per
candidate composition as a cheap physics node, and how accurate are they?

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


# Predicting nickel–aluminum bronze phases after rapid cooling and reheating

**Bottom line.** CALPHAD is a defensible *screen for phase stability and transformation driving forces*, not a validated predictor of the as-deposited phase fractions, κ-particle sizes, or β′ martensite in laser DED nickel–aluminum bronze (NAB). The strongest directly applicable cooling-rate dataset shows that κ precipitates survive cooling at **139–424 °C/s**, while the preceding hold at peak temperature changes their measured onset. No verified, composition-resolved accuracy estimate for a Thermo-Calc NAB database, five-component martensite-start equation, or universal critical rate for retaining β′ emerged from the accessible literature. (kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 142-147, kuprienko2025analysisofnickel pages 158-164, kuprienko2025analysisofnickel pages 164-169)

## Thermodynamic descriptions and what the phase names mean

1. **[CITE] [GAP]** S. M. Orzolek, J. K. Semple, and C. R. Fisher, “Influence of processing on the microstructure of nickel aluminum bronze (NAB),” *Additive Manufacturing* **56** (2022), 102859. DOI: **10.1016/j.addma.2022.102859**. **Process:** processing study of NAB; the cited pseudo-binary Thermo-Calc calculation is for Cu–*x*Al–4.5Ni–4.0Fe–1.15Mn, **wt%**, with *x* = 0–25. **Test medium/duration:** not a corrosion test in the evidence examined. The calculation establishes that a phase-diagram calculation exists for a relevant five-element composition, but the retrieved account gives **neither its TCCU version nor a tabulated calculated-versus-measured transformation error**. It cannot establish predictive accuracy for a DED cooling path. (kuprienko2025analysisofnickel pages 23-30, kuprienko2025analysisofnickel pages 164-169)

2. **[CITE] [NUMBERS] [GAP]** I. Marković, M. Banković, L. Balanović, D. Manasijević, and J. Petrović, “Microstructure and hardness of Cu-Al-Ni-Fe alloy after precipitation hardening,” *Machines. Technologies. Materials* **16** (2022), 29–32; **DOI not identified in the publication examined**. **Process:** sand-clay-mold cast; nominal Cu–9Al–3Ni–3Fe, measured **8.996Al–2.619Ni–3.309Fe–balance Cu wt%**; 900 °C/1 h, water quench, then optional 300–400 °C/1 h aging. **Test medium/duration:** no corrosion test reported. At **878 °C**, its Thermo-Calc result assigns approximately **78.40 wt% FCC α, 15.75 wt% BCC β, 3.65 wt% Ni–Al-rich ordered B2 (κ-III), and 2.20 wt% Fe-rich BCC/B2 (labeled κ-I or κ-II)**. This is an instructive *equilibrium calculation*, not measured fractions after quenching; even its Fe-rich phase label does not distinguish κ-I from κ-II. Cast, quenched, and 400 °C-aged hardnesses were approximately **152, 185, and 244 HV10**, respectively. **TCCU version and quantitative phase-fraction validation were not specified.** (markovic2022microstructureandhardness pages 1-2, markovic2022microstructureandhardness pages 2-3)

3. **[CITE] [GAP]** A. Jahanafrooz, F. Hasan, G. W. Lorimer, and N. Ridley, “Microstructural development in complex nickel-aluminum bronzes,” *Metallurgical Transactions A* **14** (1983). DOI: **10.1007/BF02662362**; and F. Hasan, A. Jahanafrooz, G. W. Lorimer, and N. Ridley, “The morphology, crystallography, and chemistry of phases in as-cast nickel-aluminum bronze,” *Metallurgical Transactions A* **13** (1982), 1337–1345. DOI: **10.1007/BF02642870**. **Process:** cast and controlled cooling/quenching; one examined composition is Cu–9.37Al–4.38Fe–4.84Ni–1.18Mn **wt%**, held at **1010 °C for 30 min**, air-cooled, then quenched at selected temperatures. **Test medium/duration:** no seawater exposure in the phase-transformation evidence. These experimental identifications distinguish **coarse Fe-rich κ-I** (which may be disordered BCC, Fe₃Al/D0₃ or FeAl/B2), **Fe₃Al-based κ-II** and fine intragranular **κ-IV**, from **NiAl-based B2 κ-III**. κ-I through κ-IV designate *constituents by chemistry, structure, morphology, location, and processing history*—not four automatically distinct Thermo-Calc phase names. The β parent is high-temperature BCC; β′ is a cooling-dependent martensitic product, not an ordinary equilibrium room-temperature β fraction. (kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickel pages 164-169, kuprienko2025analysisofnickel pages 36-41)

**Assessment/database limitation.** The accessible sources demonstrate multicomponent Thermo-Calc calculations and experimentally established κ crystal structures, **but do not identify a particular published, independently validated Cu–Al–Ni–Fe(–Mn) thermodynamic parameter assessment, the TCCU release used in either calculation, or a head-to-head TCCU-version validation for NAB**. Accordingly, neither a claimed TCCU upgrade nor a numerical database prediction error is supportable here. Before adopting a cheap physics node, record the actual installed database release, active/suspended phases and ordered-phase sublattices, and check whether separate Fe-rich and Ni-rich BCC/B2 solutions are permitted; inspect the output *compositions and structures*, rather than equating a phase-name string to κ-I, II, III, or IV. (kuprienko2025analysisofnickel pages 23-30, markovic2022microstructureandhardness pages 1-2, kuprienko2025analysisofnickel pages 36-41)

## Measured temperatures versus calculations

4. **[CITE] [NUMBERS] [NAVY]** A. Kuprienko, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*, PhD dissertation, Ohio State University (2025); **dissertation DOI not verified**. **Process:** pulsed-GMAW **wire-arc DED**, followed by Gleeble or furnace thermal cycles on deposited Cu–**81.35Cu–9.09Al–3.94Fe–4.53Ni–1.00Mn wt%**. **Test medium/duration:** phase analysis, not corrosion. The dissertation acknowledges **Office of Naval Research Manufacturing Science Program funding**. The Gleeble specimens reached **1035 °C** for **2 or 60 s**; furnace specimens reached **1031 °C** for approximately **10 min**. Below, cooling rate is measured over **1000–800 °C**, not assumed to describe the entire cycle. Entries are measured single-sensor DTA events, **not Thermo-Calc predictions**. (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 1-7)

| Cooling condition | Cooling rate, 1000–800 °C (°C/s) | β→α end† (°C) | κ-II start–finish (°C) | κ-IV start–finish (°C) | κ-III start (°C) | Qualification |
|---|---:|---:|---:|---:|---:|---|
| Furnace | 0.1 | 1015 | 1004–990 | 897–763 | 717 | Slow-cooling reference; 10 min at 1031 °C (kuprienko2025analysisofnickel pages 137-142) |
| Gleeble-1 | 287 | 1003 | 965–914 | 872–775 | 679 | 500 °C/s heating; 2 s at 1035 °C (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 131-137) |
| Gleeble-2 | 424 | 995 | 962–907 | 868–765 | 677 | 100 °C/s heating; 2 s at 1035 °C (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 131-137) |
| Gleeble-3 | 139 | 1003 | 974–927 | 866–774 | 685 | 100 °C/s heating; 2 s at 1035 °C (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 137-142) |
| Gleeble-4 | 394 | 995 | 947–890 | Not resolved by SS-DTA‡ | 711 | 100 °C/s heating; 60 s at 1035 °C (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 137-142) |
| Scope/caveat | — | †Not a β solvus | — | ‡TEM confirmed 5–15 nm Fe-rich κ-IV despite the absent thermal signal | — | Alloy: Cu–9.09Al–3.94Fe–4.53Ni–1.00Mn wt.%; values are kinetic SS-DTA events, not an exact equilibrium-CALPHAD validation. Kuprienko reported lower event temperatures with faster cooling, but hold time and prior homogenization also mattered (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 158-164, kuprienko2025analysisofnickel pages 164-169). |


*Table: Measured cooling transformations for DED-Arc NAB Cu–9.09Al–3.94Fe–4.53Ni–1.00Mn (wt.%) from Kuprienko’s 2025 dissertation. The table distinguishes the observed β→α endpoint from a true equilibrium β solvus and flags the κ-IV event that SS-DTA missed but TEM confirmed.*

The tabulated high-temperature α event marks the **end of β→α on cooling**, **not an equilibrium β solvus measured on heating**. Relative to the 0.1 °C/s furnace result, κ-II onset shifted from **1004 °C** to **947–974 °C** in the four Gleeble conditions—a **30–57 °C kinetic difference**, *not* a measured CALPHAD error. A **60-s** rather than **2-s** hold at 1035 °C delayed κ-II onset by approximately **20 °C** despite similar cooling rates; κ-IV was **not resolved by DTA** in that condition but **was confirmed by TEM** as approximately **5–15 nm Fe-rich precipitates**. Thus even a correctly calculated crossing of a solvus does not guarantee dissolution during a brief DED reheat, nor absence of precipitation during subsequent cooling. (kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 142-147, kuprienko2025analysisofnickel pages 152-158, kuprienko2025analysisofnickel pages 158-164)

5. **[CITE] [NUMBERS]** B. P. Pisarek, “Model of Cu-Al-Fe-Ni Bronze Crystallization,” *Archives of Foundry Engineering* **13** (2013), 72–79. DOI: **10.2478/afe-2013-0063**. **Process:** cast, thermal/derivative analysis; nominal Cu–11Al–5Fe–6Ni, while the measured alloy series spans **10.38–10.89Al, 4.43–4.92Fe, 4.50–5.54Ni, 0.3–0.8Mn wt%**, balance Cu, with minor Si/Cr/Mo/W variations. **Test medium/duration:** no corrosion exposure. In the representative cooling curve, measured **liquidus 1082.6 °C; solidus 1023.3 °C; κ-II characteristic point 897.4 °C; α 812.2 °C; κ-III 736.6 °C; κ-IV 702.7 °C; and residual-β→α+γ₂ event 461.7 °C**. These are characteristic *cooling-curve points*, not all onset temperatures. The paper’s broader transformation intervals differ from the particular point values. Also, **β→α+κ-III** (often called a κ eutectoid) must not be confused with the lower-temperature, Al-rich residual-**β→α+γ₂** reaction; γ₂ is especially pertinent to the approximately 11 wt% Al cast composition and cannot be presumed in ordinary approximately 9 wt% Al NAB. The paper does not give a same-composition CALPHAD prediction/error table. Its original DTA figure was inspected alongside the text. (pisarek2013modelofcualfeni pages 1-2, pisarek2013modelofcualfeni media 5909cb01, pisarek2013modelofcualfeni pages 2-3, pisarek2013modelofcualfeni pages 3-5, kuprienko2025analysisofnickel pages 30-36)

6. **[CITE] [NUMBERS] [GAP]** J. Hájek, A. Kříž, O. Chocholaty, and D. Pakuła, “Effect of heat treatment on microstructural changes in aluminium bronze,” *Archives of Metallurgy and Materials* **61** (2016), 1271–1276. DOI: **10.1515/amm-2016-0210**. **Process:** wrought/rolled Cu–**9.67Al–3.46Fe–1.31Mn–0.081Ni wt%**, heated for **90 min** at 700, 850, or 1000 °C and cooled in water, oil, air, or furnace; not a conventional Ni-rich NAB composition. **Test medium/duration:** no quantitative seawater-corrosion protocol or result established in the inspected evidence. The paper states that the low-temperature **β→α+γ₂** eutectoid develops only below approximately **1 °C/min**, while faster cooling can bypass it; water quenching from **1000 °C** gave predominantly martensitic morphology. That approximately **0.017 °C/s** statement concerns suppression of *that eutectoid in that alloy*, **not a critical laser-DED rate for κ suppression or β′ retention in NAB**. (hajek2016effectofheat pages 1-2)

**Martensite-start and critical-rate finding.** Kuprienko discusses β ordering at roughly **600–400 °C** and martensitic transformation around **200 °C**, but does **not** supply a fitted \(M_s=f(w_{Al},w_{Ni},w_{Fe},w_{Mn})\), its domain or its predictive error. A published Cu–Al–Ni *shape-memory* equation, if obtained independently, would require calibration before extension to Fe/Mn-containing, segregation-prone approximately 9 wt% Al NAB; **no defensible numeric equation for this candidate family was established by the retrieved evidence**. Likewise, the observation that κ-II/III/IV persist around **400 °C/s** gives **no universal β′-retention threshold**: β′ and κ can coexist, prior β fraction matters, and LPBF and laser DED experience different solidification/reheat cycles. Kuprienko explicitly proposes testing **>1000 °C/s** as future work rather than reporting a measured threshold. (kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickel pages 142-147, kuprienko2025analysisofnickel pages 164-169, nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 79-83)

## Process benchmarks and proposal overlap

7. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** B. Li, H. Zheng, C. Han, and K. Zhou, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39** (2021), 101825. DOI: **10.1016/j.addma.2020.101825**. **Process:** laser metal deposition/laser DED, **Cu–9Al–5Fe–5Ni wt%**; **test medium/duration:** no seawater-corrosion benchmark established in the inspected evidence. As-deposited material contains β-derived martensitic structure **alongside Widmanstätten α and nanoscale Fe₃Al/NiAl**, illustrating why a β′ label cannot imply complete κ suppression. A published review reports **yield strength 593–713 MPa, UTS 769–949 MPa, elongation 10–12%** across processing conditions. **Porosity/density and powder size/flow/oxygen were not verified here.** Overlap: successful laser deposition of a pre-existing NAB composition; the proposed novelty must rest on composition-to-powder-to-corrosion optimization and repair validation, rather than laser deposition of NAB alone. (kuprienko2025analysisofnickel pages 164-169, nemani2024advancementsinadditive pages 79-83)

8. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** T. Murray, S. Thomas, Y. Wu, W. Neil, and C. Hutchinson, “Selective laser melting of nickel aluminium bronze,” *Additive Manufacturing* **33** (2020), 101122. DOI: **10.1016/j.addma.2020.101122**. **Process:** LPBF, feedstock Cu–**9.8Al–5.2Ni–4.6Fe–0.3Mn wt%**. **Test medium/duration:** **seawater immersion, 3 and 6 months** in the accessible secondary account; whether natural or ASTM D1141 seawater, flow and numeric mass-loss values were **not verified**. The as-printed material was reported as predominantly **twinned martensite without detected κ**; its immersion mass loss was approximately **an order of magnitude lower than cast and wrought NAB** comparators. **Density, powder size/flow/oxygen, corrosion current/Ecorr and comparison to wrought C71500 were not established.** Overlap: high marine corrosion resistance without heat treatment is *not* intrinsically new; LPBF is not blown-powder DED and the comparator was NAB, not 70–30 Cu–Ni. (nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79)

9. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** L.-M. Zhang, X.-Y. Cai, B.-L. Song, B.-L. Dong, S.-W. Lin, and F. Khoshnaw, “Effect of low-level Ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of WAAM-processed nickel-aluminium bronze,” *Advanced Materials Joining* **1** (2026). DOI: **10.1007/s44500-026-00016-x**. **Process:** wire-arc DED using NAB wire, with **elemental Ti nanoparticles applied between layers in situ**—*not* single-stream pre-alloyed-powder laser DED. Baseline wire: **8.73Al–4.28Ni–3.22Fe–1.44Mn–balance Cu wt%**, interpreting the paper’s apparent “Mg: Bal.” typo cautiously; Ti additions **0, 0.03, 0.05, 0.10 wt%**. **Test:** room-temperature, static **3.5 wt% NaCl**, immersion **7/14/21 days**; polarization after OCP stabilization, **0.33 mV/s**, potential versus saturated calomel electrode (SCE). Baseline as-deposited **\(E_{corr}=-192.91\) mV versus SCE, \(i_{corr}=10.06\) µA/cm²**; 0.10 wt% Ti: **−188.57 mV, 8.49 µA/cm²**. Baseline longitudinal **UTS 664.2 MPa, yield 334.9 MPa, elongation 28.6%, hardness 181.2 HV0.3**; 0.10 wt% Ti longitudinal **UTS 718.2 MPa, yield 372.5 MPa, elongation 28.0%**. The Ti nanopowder averaged **50 nm**; this is *not* a reported DED feedstock size, Hall flow or oxygen measurement. **Deposit porosity, impedance and attack depth were not quantified in the cited evidence.** Overlap: as-deposited NAB composition/property/corrosion tuning; distinction: feed mode, chemistry, and lack of the proposed seawater/C71500/repair comparison. (zhang2026effectoflowlevel pages 2-4, zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel pages 8-11)

10. **[CITE] [NUMBERS] [GAP]** C. M. Abreu, I. Feijoo, G. Pena, and M. C. Pérez, “Influence of Deep Cryogenic Treatment on the Mechanical Properties and Corrosion Resistance of Nickel–Aluminum Bronze,” *Corrosion and Materials Degradation* **5** (2024), 624–640. DOI: **10.3390/cmd5040030**. **Process:** cast Cu–**8.96Al–4.93Ni–5.09Fe–1.24Mn–0.09Si–0.53Zn–balance Cu wt%**, as cast or cryogenic/675 °C annealed. **Test:** stationary **3.5% NaCl at pH 7.9**, room temperature; **60-min OCP** and EIS over **1–72 h**, versus SCE. As-cast tensile **yield 258 MPa, UTS 636 MPa, elongation 17.5%**; the −180 °C/16 h *then* 675 °C/2 h condition gave **286 MPa, 680 MPa, 19.5%**. The authors measured EIS but the examined sections do **not** substantiate an as-cast numeric impedance or direct comparison to C71500. Annealing changes κ morphology and removes detectable retained β′; those observations reinforce the requirement to benchmark the *as-deposited* condition separately. (abreu2024influenceofdeep pages 2-4, abreu2024influenceofdeep pages 4-5, abreu2024influenceofdeep pages 5-8)

## Recommended cheap physics node—and its accuracy limits

For **each measured candidate composition**, compute with an explicitly version-pinned Thermo-Calc database: equilibrium liquidus/solidus and solidification interval; an α/β phase-boundary curve and phase fractions; Fe-rich versus Ni-rich ordered-phase **chemical potentials, compositions, solvus-crossing temperatures and precipitation driving forces**; and a restricted-equilibrium/Scheil solidification scenario. Then apply the modeled *local* layer-by-layer temperature–time histories to estimate **time above each calculated solvus**, exposure to precipitation windows, and cooling rate over **1000–800 °C**. Keep the equilibrium-only result as an explicit baseline. These are *cheap descriptors and experimentally testable hypotheses*, not predicted room-temperature κ counts, β′ fractions, \(M_s\), cracking, or corrosion. The source data establish a **30–57 °C difference in measured κ-II onset between cooling protocols for one composition**, not a transferable ±30–57 °C accuracy claim for CALPHAD. Calibration should use heating/cooling dilatometry or SS-DTA plus microscopy/EBSD/TEM on candidate powders and deposits, distinguishing true solvus measurements from cooling onsets and validating layer reheating separately. (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 152-158, markovic2022microstructureandhardness pages 1-2, kuprienko2025analysisofnickel pages 164-169)

**Unanswered acceptance test:** None of these phase studies establishes that a **single pre-alloyed-powder, blown-powder laser DED** deposit is simultaneously dense and crack-free on itself and cast NAB/wrought Cu–Ni, and equals or exceeds **wrought C71500 in as-deposited flowing seawater**. The cited **3.5% NaCl electrochemical** numbers, seawater immersion account and mechanically tested coupons cannot be interchanged as that demonstration; nor do they supply comparable powder-lot Hall flow, apparent density and oxygen, deposit porosity, impedance, or selective-attack depth. (nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83, zhang2026effectoflowlevel pages 2-4)

## Top 5 things the PI should know

1. **Use CALPHAD as a ranked, version-controlled thermodynamic prior, not an as-built phase oracle:** even the retrieved Thermo-Calc NAB examples lack a quantified TCCU-specific validation. (kuprienko2025analysisofnickel pages 23-30, markovic2022microstructureandhardness pages 1-2)
2. **κ survives welding-like cooling:** up to **424 °C/s** did not remove κ; an undetectable DTA peak did not mean absent κ-IV. (kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 142-147, kuprienko2025analysisofnickel pages 158-164)
3. **Reheat history is indispensable:** changing a **1035 °C hold from 2 to 60 s** shifted κ-II onset approximately **20 °C**, so equilibrium-solvus crossings alone misrepresent a multilayer deposit. (kuprienko2025analysisofnickel pages 120-125, kuprienko2025analysisofnickel pages 137-142)
4. **Avoid invented thresholds:** no verified quinary \(M_s\) equation or universal critical cooling rate for retaining β′ was found; β′ may coexist with κ in laser DED while LPBF can lack detectable κ. (kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickel pages 164-169, nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 79-83)
5. **Frame novelty around the complete acceptance test:** laser-deposited NAB, corrosion-resistant as-printed LPBF NAB, and as-deposited WAAM NaCl benchmarks already exist; the evidence does **not** establish the proposed *pre-alloyed single-stream powder + both repair substrates + as-deposited C71500-level seawater performance* combination. (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83, zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel pages 2-4)

References

1. (kuprienko2025analysisofnickel pages 137-142): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

2. (kuprienko2025analysisofnickel pages 142-147): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

3. (kuprienko2025analysisofnickel pages 158-164): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

4. (kuprienko2025analysisofnickel pages 164-169): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

5. (kuprienko2025analysisofnickel pages 23-30): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

6. (markovic2022microstructureandhardness pages 1-2): I Marković, M Banković, and L Balanović. Microstructure and hardness of cu-al-ni-fe alloy after precipitation hardening. Unknown journal, 2022.

7. (markovic2022microstructureandhardness pages 2-3): I Marković, M Banković, and L Balanović. Microstructure and hardness of cu-al-ni-fe alloy after precipitation hardening. Unknown journal, 2022.

8. (kuprienko2025analysisofnickel pages 30-36): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

9. (kuprienko2025analysisofnickel pages 36-41): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

10. (kuprienko2025analysisofnickel pages 120-125): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

11. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

12. (kuprienko2025analysisofnickel pages 131-137): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

13. (kuprienko2025analysisofnickel pages 152-158): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

14. (pisarek2013modelofcualfeni pages 1-2): B. P. Pisarek. Model of cu-al-fe-ni bronze crystallization. Archives of Foundry Engineering, 13:72-79, Sep 2013. URL: https://doi.org/10.2478/afe-2013-0063, doi:10.2478/afe-2013-0063. This article has 80 citations.

15. (pisarek2013modelofcualfeni media 5909cb01): B. P. Pisarek. Model of cu-al-fe-ni bronze crystallization. Archives of Foundry Engineering, 13:72-79, Sep 2013. URL: https://doi.org/10.2478/afe-2013-0063, doi:10.2478/afe-2013-0063. This article has 80 citations.

16. (pisarek2013modelofcualfeni pages 2-3): B. P. Pisarek. Model of cu-al-fe-ni bronze crystallization. Archives of Foundry Engineering, 13:72-79, Sep 2013. URL: https://doi.org/10.2478/afe-2013-0063, doi:10.2478/afe-2013-0063. This article has 80 citations.

17. (pisarek2013modelofcualfeni pages 3-5): B. P. Pisarek. Model of cu-al-fe-ni bronze crystallization. Archives of Foundry Engineering, 13:72-79, Sep 2013. URL: https://doi.org/10.2478/afe-2013-0063, doi:10.2478/afe-2013-0063. This article has 80 citations.

18. (hajek2016effectofheat pages 1-2): J. Hájek, A. Kříž, O. Chocholaty, and D. Pakuła. Effect of heat treatment on microstructural changes in aluminium bronze. Archives of Metallurgy and Materials, 61:1271-1276, Sep 2016. URL: https://doi.org/10.1515/amm-2016-0210, doi:10.1515/amm-2016-0210. This article has 21 citations and is from a peer-reviewed journal.

19. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

20. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

21. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

22. (zhang2026effectoflowlevel pages 2-4): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

23. (zhang2026effectoflowlevel pages 13-16): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

24. (zhang2026effectoflowlevel pages 8-11): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

25. (abreu2024influenceofdeep pages 2-4): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.

26. (abreu2024influenceofdeep pages 4-5): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.

27. (abreu2024influenceofdeep pages 5-8): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.
