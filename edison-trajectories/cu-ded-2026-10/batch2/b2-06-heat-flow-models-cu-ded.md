<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: cb999416-b429-4ffb-88a3-eb0093a12c7c
- Submitted: 2026-10-17T05:37:04Z
- Fetched: 2026-10-17T06:08:56Z (status: success)
- Raw trajectory JSON: ../raw/b2-06-heat-flow-models-cu-ded.json.gz
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

QUESTION: How accurately do analytical heat-flow models (Rosenthal moving
point source, Eagar-Tsai distributed source, Pinkerton's DED model) and
reduced-order numerical models predict melt-pool size, cooling rate through
solidification, and reheating peak temperatures in blown-powder laser DED,
especially for high-conductivity copper alloys? How are they calibrated
(absorptivity, effective conductivity, melt-pool width from single tracks),
and how well do predicted cooling rates match measured dendrite arm or cell
spacing? Report uses of thermal-history models to predict NAB phase
evolution (martensite, kappa precipitation during reheating) or Cu-Ni
segregation in DED, WAAM or welding, and any published temperature-dependent
thermophysical property data for NAB and Cu-Ni (e.g. from NSWC Carderock).

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

QUESTION: How accurately do analytical heat-flow models (Rosenthal moving
point source, Eagar-Tsai distributed source, Pinkerton's DED model) and
reduced-order numerical models predict melt-pool size, cooling rate through
solidification, and reheating peak temperatures in blown-powder laser DED,
especially for high-conductivity copper alloys? How are they calibrated
(absorptivity, effective conductivity, melt-pool width from single tracks),
and how well do predicted cooling rates match measured dendrite arm or cell
spacing? Report uses of thermal-history models to predict NAB phase
evolution (martensite, kappa precipitation during reheating) or Cu-Ni
segregation in DED, WAAM or welding, and any published temperature-dependent
thermophysical property data for NAB and Cu-Ni (e.g. from NSWC Carderock).

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


# Thermal-history models for copper-alloy directed energy deposition

**Bottom line.** The retrieved literature does **not** establish a transferable percentage accuracy for Rosenthal, Eagar–Tsai, or Pinkerton models in blown-powder laser DED of high-conductivity Cu–Ni or nickel–aluminum bronze (NAB). In particular, I found no verified study of **one pre-alloyed powder feed** that independently measures all three proposed validation targets: melt-pool dimensions, cooling rate through solidification, and subsequent reheating peaks. Results for Inconel, LPBF, arc deposition, or mixed elemental feeds should not be presented as that validation. (plotkowski2023assessmentofprocess pages 23-26, plotkowski2023assessmentofprocess pages 26-28, nemani2024advancementsinadditive pages 105-106, yadav2020parametricinvestigationand pages 2-4)

The following benchmark table distinguishes measured quantities from fitted or inferred ones. **“Not reported” is not a zero measurement**: the principal thermal-model studies do not supply comparable seawater-exposure conditions, corrosion current or rate, *E*₍corr₎, impedance, selective-attack depth, or powder-lot Hall-flow/apparent-density/oxygen measurements. (lawson2024understandingcoaxialwire+ pages 90-95, kuprienko2025analysisofnickel pages 94-100, yadav2020parametricinvestigationand pages 2-4, fang2021datadrivenanalysis pages 3-7)

| Source | Process / alloy / feedstock | Calibration or validation | Key quantitative evidence | Applicability and limitation |
|---|---|---|---|---|
| Yadav et al. (2020), *International Journal of Advanced Manufacturing Technology*. DOI: [10.1007/s00170-020-05644-9](https://doi.org/10.1007/s00170-020-05644-9) | Blown-powder laser DED of graded Cu–Ni on Cu; mechanically blended elemental Cu and Ni powders, 45–105 µm; 25, 50, and 75 wt% Ni—not one pre-alloyed feedstock | Single tracks mapped power, speed, and composition to bead geometry; this was process characterization, not validation of Rosenthal, Eagar–Tsai, Pinkerton, or another thermal model | At 0.3 m/min and 1.2–1.8 kW, measured widths included 0.68–1.39 mm; bulk parameters used 1.8 kW and 0.5–0.7 m/min. Relative density >99%; porosity 0–2%, reaching ≈2% in Cu-rich/interface regions; hardness across the full Ni-to-Cu gradient was 115–47 HV; powder flow and oxygen not reported; no corrosion testing (yadav2020parametricinvestigationand pages 2-4, yadav2020parametricinvestigationand pages 1-2, yadav2020parametricinvestigationand pages 10-12, yadav2020parametricinvestigationand pages 7-10) | Closest Cu–Ni powder-DED geometry benchmark, but it overlaps only compositionally: elemental blending and graded deposition conflict with the proposed single-stream, pre-alloyed-powder method. It supplies no predicted cooling rate, reheating peak, segregation model, or seawater benchmark. |
| Lawson (2024), dissertation, *Understanding Coaxial Wire + Powder Laser Directed Energy Deposition of Dissimilar Metals Through Modeling and Experimental Approaches*. DOI not verified | Hybrid coaxial wire-plus-powder laser DED: IN625 wire plus GRCop-42 Cu–Cr–Nb powder; target 30 wt% GRCop-42—not Cu–Ni/NAB and not powder-only DED | Numerical thermal/composition model compared with bead dimensions, maximum temperature, and composition at 600, 900, and 1200 W | Modeled/measured widths: 1.94/1.79, 2.36/2.01, and 3.78/2.80 mm; corresponding absolute errors ≈8%, 17%, and 35%. Modeled/measured maximum temperatures: 1626/1661, 1844/1840, and 1416/1372 °C; absolute errors ≈2.1%, 0.2%, and 3.2%. Modeled/measured bead heights: 1.14/1.49, 1.44/1.26, and 1.65/1.07 mm. No cooling-rate or reheating-peak validation was reported (lawson2024understandingcoaxialwire+ pages 90-95) | Demonstrates that calibration can fit peak temperature while width and especially height remain inaccurate; transfer to high-conductivity copper-alloy powder-only DED is weak because of six-beam simplification, substrate penetration, capture-efficiency uncertainty, dissimilar feed modes, and incomplete mixing. |
| Fang et al. (2021), *Data-Driven Analysis of Thermal Simulations, Microstructure and Mechanical Properties of Inconel 718 Thin Walls Deposited by Metal Additive Manufacturing*. DOI: [10.48550/arXiv.2110.07108](https://doi.org/10.48550/arxiv.2110.07108) | Blown-powder laser DED of IN718 thin walls; 1800 W, 16.7 mm/s, 0.3 g/s, 1.5 mm beam radius; absorptivity 0.45 | Reduced-order finite-element heat-conduction model calibrated/validated using in-situ IR histories; fitted absorptivity, emissivity, and spatially varying convection. IR agreement was qualitative rather than reported as RMSE; molten metal was under-read because its emissivity differed from the solid | Cooling rate/primary dendrite-arm spacing pairs were 19.58 K/s/16.89 µm, 27.30 K/s/11.92 µm, and 43.05 K/s/7.98 µm. Seven-location fit: λ₁ = −0.37Ṫ + 23.02 µm, R² = 0.85. IR camera: 640 × 480 pixels, 7.5–14 µm, ±2 °C rating. Cooling rate was simulated—not independently measured—so the spacing correlation does not establish cooling-rate prediction accuracy (fang2021datadrivenanalysis pages 3-7, fang2021datadrivenanalysis pages 18-21, fang2021datadrivenanalysis pages 33-37, fang2021datadrivenanalysis pages 7-11, fang2021datadrivenanalysis media 9b7d56d8) | Best quantitative example of a thermal-history-to-spacing link, but it is IN718, not copper. Within a single wall, cooling rate alone did not consistently predict local structure/properties; full reheating descriptors were more informative. |
| Kuprienko (2025), Ph.D. dissertation, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*. DOI not verified | GMA-pulsed wire-arc DED/WAAM of NAB, Cu–8.73Al–3.19Fe–4.32Ni–1.45Mn; ONR Manufacturing Science funded | FEA calibrated to bead-on-plate thermocouples; only 3 of 12 thermocouples were usable. NAB thermal conductivity was increased uniformly by 20% to fit histories; trailing liquid-N₂ cooling was represented by a calibrated moving disc heat sink | Gleeble cooling rates were 139–424 °C/s through 1000–800 °C. Measured κII ranges were about 974–890 °C, κIV about 872–763 °C, and κIII onset about 679–647 °C; slow furnace cooling was 0.1 °C/s with κII 1004–990 °C, κIV 897–763 °C, and κIII onset near 717 °C. Cryogenic-model cases predicted 320–693 °C/s, temperature dips of 100–300 °C, and 0.32–0.59 s recovery. Deposit hardness was 180–204 HV0.3; typical UTS 620–710 MPa, yield 300–390 MPa, and elongation 22–37% (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 76-81, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 100-106, kuprienko2025analysisofnickel pages 131-137, kuprienko2025analysisofnickel pages 94-100) | Strongest Navy-relevant evidence that reheating/dip–recovery histories govern NAB κ evolution, but it is arc/wire DED and does not validate a laser melt-pool model or CALPHAD phase prediction. The fitted +20% conductivity is an effective calibration, not new intrinsic-property data. |
| **Evidence boundary** | **Pre-alloyed Cu–Ni/NAB powder-only blown-powder laser DED** | **No retrieved study directly validates Rosenthal, Eagar–Tsai, or Pinkerton against measured melt-pool size, solidification cooling rate, and multilayer reheating peaks for this process/material combination.** | **No source above reports all three of: copper-alloy melt-pool geometry error, independently measured cooling-rate error, and measured reheating-peak error. None provides the requested as-deposited ASTM D1141/natural-seawater corrosion metrics or lot-level Hall flow, apparent density, and oxygen data.** | **This is a substantive proposal gap, not evidence that the analytical models are accurate for high-conductivity Cu alloys. The proposed comparison of heat-flow-informed CALPHAD against equilibrium-only CALPHAD and no physics remains distinct.** |


*Table: Evidence-checked comparison of the closest quantitative Cu-alloy and thermal-history studies. It highlights what was actually calibrated or measured and the unfilled validation gap for pre-alloyed Cu–Ni/NAB blown-powder laser DED.*

## Model accuracy and calibration: relevant items

**1. Plotkowski, A.; Knapp, G.; Coleman, J.; Stump, B.; Rolchigo, M. *Assessment of Process Modeling Tools for Determining Variability in Additively Manufactured Parts*. Oak Ridge National Laboratory, ORNL/SPR-2023/2877 (2023). DOI: 10.2172/1989564.** **Process/alloy:** Review focused on **LPBF 316 stainless steel**, not copper DED. **[CITE] [GAP]** Rosenthal is a moving *point-source*, quasi-steady, semi-infinite conduction solution; Eagar–Tsai replaces the point with a moving Gaussian surface distribution, evaluated through a Green’s-function integral. Both are inexpensive ways to obtain temperature-field descriptors, subject to their source, geometry, material-property, and conduction assumptions. The review says calibrated semi-analytical source shapes can reproduce similar solidification conditions in a conduction regime, but discrepancies persist at the mushy-zone tail; simple conduction solutions deteriorate when keyholing starts. It does **not** give an experimental error percentage applicable to Cu–Ni or NAB blown-powder DED. The review is a rationale for comparing fidelity levels, not a copper validation dataset. **Corrosion, density, mechanical, and powder-lot benchmarks:** not applicable/reported. (plotkowski2023assessmentofprocess pages 1-11, plotkowski2023assessmentofprocess pages 23-26, plotkowski2023assessmentofprocess pages 26-28, plotkowski2023assessmentofprocess pages 28-30)

**Pinkerton-specific limit.** The search identified Pinkerton’s *An analytical model of beam attenuation and powder heating during coaxial laser direct metal deposition* (*Journal of Physics D*, 2007; DOI: **10.1088/0022-3727/40/23/012**) and related DED thermal work, but did not retrieve usable full text from which to verify melt-pool, cooling-rate, or reheating-peak errors. Powder-cloud attenuation and heating are physically relevant to a blown-powder source; **no numeric Pinkerton-versus-Cu–Ni/NAB accuracy claim is justified here**. **[CITE] [GAP]** The citation is bibliographically identified, not counted as direct validation evidence. (plotkowski2023assessmentofprocess pages 23-26, plotkowski2023assessmentofprocess pages 26-28)

**2. Fang, L.; Cheng, L.; Glerum, J. A.; Bennett, J.; Cao, J.; Wagner, G. J. *Data-Driven Analysis of Thermal Simulations, Microstructure and Mechanical Properties of Inconel 718 Thin Walls Deposited by Metal Additive Manufacturing* (2021 preprint). DOI: 10.48550/arXiv.2110.07108.** **Process/alloy:** Powder-fed laser DED, **IN718**, not copper; 1,800 W, 16.7 mm s⁻¹, 0.3 g s⁻¹ powder, 1.5-mm beam radius, with 80- or 120-mm walls and a five-second-dwell variant. **[CITE] [NUMBERS] [GAP]** A conduction FE model used temperature-dependent properties and in-situ IR histories to constrain absorptivity, emissivity, and spatially varying convection; its reported absorption efficiency is **0.45**. Agreement is described as good principally **below the 1,533 K solidus**, but no numerical thermal-history RMSE or melt-pool-width error is established in the retrieved account. IR can under-read the molten region when liquid and solid emissivities differ. Simulated cooling rate was defined between the **last solidus crossing and 1,450 K**; the three wall cases gave **19.58, 27.30, 43.05 K s⁻¹**, paired with measured primary dendrite-arm spacings of **16.89, 11.92, 7.98 µm**. Across seven locations the fitted spacing relation was λ₁(µm) = 23.02 − 0.37·Ṫ(K s⁻¹), **R² = 0.85**. This is a useful *spacing-versus-simulated-cooling* check, **not** an independent measurement proving cooling-rate accuracy; within a wall, cooling rate alone did not consistently explain local properties. Figure 5(a) was also inspected. **Seawater/powder-lot metrics:** not reported. (fang2021datadrivenanalysis pages 11-14, fang2021datadrivenanalysis pages 7-11, fang2021datadrivenanalysis pages 3-7, fang2021datadrivenanalysis pages 18-21, fang2021datadrivenanalysis pages 33-37, fang2021datadrivenanalysis media 9b7d56d8)

**3. Lawson, S. B. *Understanding Coaxial Wire + Powder Laser Directed Energy Deposition of Dissimilar Metals Through Modeling and Experimental Approaches* (2024 dissertation; DOI not verified in the accessible record).** **Process/alloy:** **Hybrid wire-plus-powder** laser DED, IN625 wire/GRCop-42 Cu–Cr–Nb powder, targeting 30 wt% GRCop-42; **not** single-powder-feed Cu–Ni/NAB. **[NUMBERS] [GAP]** At **600/900/1,200 W**, modeled/measured bead widths were **1.94/1.79, 2.36/2.01, 3.78/2.80 mm**—approximately **8%, 17%, 35%** width error relative to measurement. Modeled/measured maximum temperatures were **1,626/1,661, 1,844/1,840, 1,416/1,372 °C**—approximately **2.1%, 0.2%, 3.2%** error. Bead-height pairs were **1.14/1.49, 1.44/1.26, 1.65/1.07 mm**. Thus close peak-temperature agreement did **not** guarantee accurate dimensions; six physical lasers represented as one computational source, penetration, and powder-capture uncertainty constrain transferability. These are **bead dimensions**, not a demonstrated copper-alloy melt-pool-depth validation. Cooling-rate and reheating-peak errors, corrosion, and powder-lot data were not reported in the retrieved evidence. (lawson2024understandingcoaxialwire+ pages 90-95)

**Practical calibration implication.** Measure single-track *fusion-zone* width **and depth**, separately from deposited-bead width and height, over power/speed and substrate conditions; fit optical/powder-coupling absorptivity or effective source parameters to a subset, then reserve other tracks and multilayer temperature histories for testing. An adjusted conductivity may help match thermocouples but must be labeled **effective/fitted**, rather than a measured intrinsic Cu-alloy property. Compare melt geometry, solidification cooling and each reheating peak **separately**, reporting their out-of-calibration errors: fitting one observable need not predict the others. These are recommended validation controls inferred from the reported modeling limitations, not published copper-alloy accuracy figures. (lawson2024understandingcoaxialwire+ pages 90-95, plotkowski2023assessmentofprocess pages 23-26, plotkowski2023assessmentofprocess pages 26-28, kuprienko2025analysisofnickel pages 94-100, fang2021datadrivenanalysis pages 3-7)

## NAB phases, Cu–Ni deposition, and the limits of thermal-history prediction

**4. Kuprienko, A. *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*. Ph.D. dissertation, The Ohio State University (2025; DOI not verified).** **Process/alloy:** Pulsed-GMA **wire-arc DED/WAAM**, ERCuNiAl wire **Cu–8.73Al–3.19Fe–4.32Ni–1.45Mn wt%**, deposited on wrought NAB; funded by the **Office of Naval Research Manufacturing Science Program**. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** This is a substantive overlap in *Navy NAB repair-related thermal-history/phase questions*, **not** in laser DED with in-house pre-alloyed powder. The FE model was aligned with bead-on-plate histories: **three of 12 thermocouples** yielded usable data, and prescribed NAB thermal conductivity was raised **20%** to improve agreement. Numerical thermocouple-peak errors were not tabulated in the verified text; the conductivity adjustment is therefore a calibration precedent, not an independent property determination. In controlled experiments, cooling through **1,000–800 °C** ranged **139–424 °C s⁻¹**; measured κII precipitation was approximately **974–890 °C**, κIV approximately **872–763 °C**, and κIII onset approximately **679–647 °C**. Slowly cooled furnace tests (**0.1 °C s⁻¹**) instead placed κII at **1,004–990 °C**, κIV at **897–763 °C**, and κIII onset near **717 °C**. An additional modeled trailing-liquid-nitrogen perturbation gave local rates **320–693 °C s⁻¹**, temperature dips **100–300 °C**, and recovery times **0.32–0.59 s**; the dip/recovery was interpreted as a short reheating event capable of coarsening α/κ despite active cooling. These are **measured transformation windows plus modeled thermal histories**, not a validated kinetic CALPHAD prediction of κ fraction. (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 87-94, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 100-106, kuprienko2025analysisofnickel pages 131-137, kuprienko2025analysisofnickel pages 113-120, kuprienko2025analysisofnickel pages 94-100)

For this arc-deposited NAB, typical reported ultimate strength was **620–710 MPa**, yield strength **300–390 MPa**, and elongation **22–37%**; a modeled-study block averaged **204 HV0.3**, versus **187 HV0.3** in a wall. One lack-of-fusion specimen reached only **83.9 ksi** ultimate strength and **6.7%** elongation; do not treat the typical values as proof that all repairs are crack-free or fully dense. In the close-cooling comparison hardness decreased to about **180 versus 187 HV**, consistent with the observed coarsening. **Porosity percentage, seawater conditions/rate/*E*₍corr₎/impedance/attack depth, and powder size/flow/oxygen:** not supplied for this wire study. The dissertation also cautions against assuming every WAAM β-like constituent is martensite: it reports conflicting identifications between arc and laser builds. (kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickel pages 76-81, kuprienko2025analysisofnickel pages 106-113)

**5. Vahedi Nemani, A.; Ghaffari, M.; Sabet Bokati, K.; Valizade, N.; Afshari, E.; Nasiri, A. “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review.” *Journal of Manufacturing and Materials Processing* **8**, 54 (2024). DOI: 10.3390/jmmp8020054.** **Processes/alloys:** Review spanning **cast, LPBF, powder laser DED, and WAAM**; representative laser-deposited NAB **Cu–9Al–5Fe–5Ni wt%**. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** It documents existing laser-DED NAB, so “first laser-printed NAB” is untenable. That as-deposited material had martensitic β-like material, Widmanstätten α, nanoscale **Fe₃Al and NiAl**, and nanotwins; reviewed laser-DED yield/ultimate strengths were **593–713/769–949 MPa**, with **10–12% elongation**. WAAM’s lower cooling rates can yield α/κ without unequivocal martensite, whereas rapid laser processing can retain martensitic products. These are **observed structures and properties**, not proof that a Rosenthal/Pinkerton temperature trace quantitatively predicts κ precipitation during laser-DED reheating. The review calls for systematic seawater tests of **as-printed** AM NAB and notes the scarcity of Cu–Ni service-corrosion comparisons. It does not provide a matched 30-day ASTM D1141/natural-seawater result for the proposed deposits. Source-study powder pre-alloying, Hall flow, oxygen, and comparable corrosion metrics could not be confirmed from the reviewed passage. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 105-106, nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 106-108)

**6. Yadav, S.; Jinoop, A. N.; Sinha, N.; Paul, C.; Bindra, K. “Parametric Investigation and Characterization of Laser Directed Energy Deposited Copper–Nickel Graded Layers.” *International Journal of Advanced Manufacturing Technology* **108**, 3779–3791 (2020). DOI: 10.1007/s00170-020-05644-9.** **Process/alloy:** Blown-powder laser DED on Cu, using **mechanically premixed *elemental*** 45–105-µm Cu and Ni powders, not pre-alloyed particles: **Cu–25Ni, Cu–50Ni, Cu–75Ni wt%**. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** It overlaps Cu–Ni DED and single-track screening, **but not** the proposed single pre-alloyed feed or an as-deposited C71500 seawater comparison. The laser was a 2-kW-class fiber system with a **2-mm** defocused spot, **250 °C** Cu-substrate preheat, **1.2–1.8 kW**, **0.3–0.7 m min⁻¹**, and **2.8 g min⁻¹** powder feed for tracks. At 1.2 kW/0.3 m min⁻¹, widths were **0.68 mm for Cu–25Ni**, **1.20 mm for Cu–50Ni**, and **1.23 mm for Cu–75Ni**. Graded bulk achieved **>99% relative density**; porosity reached approximately **2%** in Cu-rich/interfacial regions, versus **<0.5%** in several Ni-rich layers. Hardness ranged from **47 HV** at the pure-Cu end to **115 HV** at the pure-Ni end—not composition-specific values for the three intermediate alloys. No model-predicted cooling rates, Cu–Ni segregation profiles, natural/synthetic-seawater exposure, *i*₍corr₎, impedance, or powder Hall flow/oxygen values were established. **A finer dendritic region is not a quantitative validation of simulated cooling rate.** (yadav2020parametricinvestigationand pages 1-2, yadav2020parametricinvestigationand pages 7-10, yadav2020parametricinvestigationand pages 2-4, yadav2020parametricinvestigationand pages 10-12)

**Cu–Ni segregation gap.** The accessible Cu–Ni DED article reports observed cellular/dendritic structure and Cu/Ni phase signatures but does not couple a validated thermal trace to measured interdendritic **Ni, Fe, Mn, or Cr partitioning**. I could not verify an equivalent quantitative, thermally validated segregation prediction for the specified single pre-alloyed-feed Cu–Ni DED/WAAM/weld compositions. Do not substitute IN718 Nb/Laves segregation, or observations in a Cu–Ni elemental gradient, for that result. (yadav2020parametricinvestigationand pages 7-10, fang2021datadrivenanalysis pages 7-11, yadav2020parametricinvestigationand pages 13-13, nemani2024advancementsinadditive pages 106-108)

## Temperature-dependent property data and an explicit verification boundary

**7. Norkett, J. E.; Fisher, C. R. “Temperature-Dependent Material Property Database for 90/10 Cu–Ni Plate.” *Integrating Materials and Manufacturing Innovation* **15**, 169–180 (2026). DOI: 10.1007/s40192-026-00444-7.** **Process/alloy:** **Wrought/plate 90/10 Cu–Ni**, not a DED deposit or 70/30 Cu–Ni; the bibliographic record surfaced in searching, but its full text was **unobtainable here**. **[CITE—metadata only] [GAP]** This is a promising source to check for temperature-dependent inputs, but neither individual *k*(T), *c*ₚ(T), density/latent-heat values nor any claimed **NSWC Carderock** provenance can be verified from the accessible evidence. Its existence should not be represented as a validated property table for NAB, C71500, liquid copper alloys, or an as-deposited microstructure. The ONR NAB dissertation’s **+20% fitted conductivity** further illustrates why effective model settings must be kept distinct from independently measured *k*(T). No verified NSWC Carderock NAB/Cu–Ni numerical property dataset was retrieved. (kuprienko2025analysisofnickel pages 94-100)

**Proposed model comparison.** For each alloy/substrate combination, carry a measured or explicitly uncertain *k*(T), *c*ₚ(T), density, liquidus/solidus and latent heat through the heat-flow model; record the **last liquidus-to-solidus cooling segment**, subsequent **peak temperatures and residence times in κ/β transformation windows**, and location-specific track geometry. An equilibrium-only CALPHAD phase fraction cannot by itself establish martensite formation or time-dependent κ precipitation; comparing it with thermal-history-informed *and kinetically constrained* calculations, alongside a no-physics surrogate, makes the physics contribution testable. That is a proposed experimental/modeling distinction, **not an accuracy already reported by the cited papers**. (kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 131-137, kuprienko2025analysisofnickel pages 113-120, plotkowski2023assessmentofprocess pages 23-26, kuprienko2025analysisofnickel pages 94-100)

## Top 5 things the PI should know

1. **The defensible gap is *validated transfer*, not invention of a heat-flow equation.** No verified pre-alloyed Cu–Ni/NAB blown-powder study gives independently tested width/depth, solidification-rate, and reheating-peak errors for Rosenthal, Eagar–Tsai, and Pinkerton on both self-build and repair substrates. (plotkowski2023assessmentofprocess pages 23-26, plotkowski2023assessmentofprocess pages 26-28, nemani2024advancementsinadditive pages 105-106, yadav2020parametricinvestigationand pages 2-4)
2. **Do not equate a fitted bead or bright IR peak with validated thermal history.** A copper-containing hybrid experiment differed by roughly **8–35% in width** despite **0.2–3.2%** peak-temperature agreement; NAB FE modeling needed **+20% fitted conductivity** and had only **three usable thermocouples of 12**. (lawson2024understandingcoaxialwire+ pages 90-95, kuprienko2025analysisofnickel pages 94-100)
3. **Reheating deserves its own validated outputs.** Navy-funded NAB work places κ events over distinct temperature intervals and finds that an active-cooling dip/recovery can **coarsen**, not refine, material. Thermodynamic equilibrium alone is insufficient to predict the observed kinetic response. (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 100-106, kuprienko2025analysisofnickel pages 113-120)
4. **A dendrite-spacing correlation is a cross-check, not direct thermometry.** IN718 gives **R² = 0.85** for spacing against **simulated** cooling rates; within-wall property trends were less reliable. A Cu–Ni/NAB-specific spacing calibration and an independent temperature measurement remain necessary. (fang2021datadrivenanalysis pages 7-11, fang2021datadrivenanalysis pages 33-37, fang2021datadrivenanalysis media 9b7d56d8)
5. **Differentiate novelty and qualification explicitly.** Mixed-*elemental* Cu–Ni DED and laser-deposited NAB already exist; pre-alloyed single-feed alloy design, fit-for-repair interfaces, lot-controlled powder inputs, and **as-deposited** seawater performance against wrought C71500 remain separate claims requiring matched, fully specified exposures and quantitative selective-attack measurements. None of the thermal-model papers supplies those corrosion endpoints. (yadav2020parametricinvestigationand pages 2-4, nemani2024advancementsinadditive pages 105-106, nemani2024advancementsinadditive pages 79-83)

References

1. (plotkowski2023assessmentofprocess pages 23-26): Alex Plotkowski, Gerry Knapp, John Coleman, Benjamin Stump, and Matt Rolchigo. Assessment of process modeling tools for determining variability in additively manufactured parts. ArXiv, Mar 2023. URL: https://doi.org/10.2172/1989564, doi:10.2172/1989564. This article has 6 citations.

2. (plotkowski2023assessmentofprocess pages 26-28): Alex Plotkowski, Gerry Knapp, John Coleman, Benjamin Stump, and Matt Rolchigo. Assessment of process modeling tools for determining variability in additively manufactured parts. ArXiv, Mar 2023. URL: https://doi.org/10.2172/1989564, doi:10.2172/1989564. This article has 6 citations.

3. (nemani2024advancementsinadditive pages 105-106): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

4. (yadav2020parametricinvestigationand pages 2-4): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

5. (lawson2024understandingcoaxialwire+ pages 90-95): SB Lawson. Understanding coaxial wire+ powder laser directed energy deposition of dissimilar metals through modeling and experimental approaches. Unknown journal, 2024.

6. (kuprienko2025analysisofnickel pages 94-100): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

7. (fang2021datadrivenanalysis pages 3-7): Lichao Fang, Lin Cheng, Jennifer A. Glerum, Jennifer Bennett, Jian Cao, and Gregory J. Wagner. Data driven analysis of thermal simulations, microstructure and mechanical properties of inconel 718 thin walls deposited by metal additive manufacturing. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2110.07108, doi:10.48550/arxiv.2110.07108. This article has 3 citations.

8. (yadav2020parametricinvestigationand pages 1-2): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

9. (yadav2020parametricinvestigationand pages 10-12): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

10. (yadav2020parametricinvestigationand pages 7-10): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

11. (fang2021datadrivenanalysis pages 18-21): Lichao Fang, Lin Cheng, Jennifer A. Glerum, Jennifer Bennett, Jian Cao, and Gregory J. Wagner. Data driven analysis of thermal simulations, microstructure and mechanical properties of inconel 718 thin walls deposited by metal additive manufacturing. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2110.07108, doi:10.48550/arxiv.2110.07108. This article has 3 citations.

12. (fang2021datadrivenanalysis pages 33-37): Lichao Fang, Lin Cheng, Jennifer A. Glerum, Jennifer Bennett, Jian Cao, and Gregory J. Wagner. Data driven analysis of thermal simulations, microstructure and mechanical properties of inconel 718 thin walls deposited by metal additive manufacturing. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2110.07108, doi:10.48550/arxiv.2110.07108. This article has 3 citations.

13. (fang2021datadrivenanalysis pages 7-11): Lichao Fang, Lin Cheng, Jennifer A. Glerum, Jennifer Bennett, Jian Cao, and Gregory J. Wagner. Data driven analysis of thermal simulations, microstructure and mechanical properties of inconel 718 thin walls deposited by metal additive manufacturing. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2110.07108, doi:10.48550/arxiv.2110.07108. This article has 3 citations.

14. (fang2021datadrivenanalysis media 9b7d56d8): Lichao Fang, Lin Cheng, Jennifer A. Glerum, Jennifer Bennett, Jian Cao, and Gregory J. Wagner. Data driven analysis of thermal simulations, microstructure and mechanical properties of inconel 718 thin walls deposited by metal additive manufacturing. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2110.07108, doi:10.48550/arxiv.2110.07108. This article has 3 citations.

15. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

16. (kuprienko2025analysisofnickel pages 76-81): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

17. (kuprienko2025analysisofnickel pages 137-142): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

18. (kuprienko2025analysisofnickel pages 100-106): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

19. (kuprienko2025analysisofnickel pages 131-137): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

20. (plotkowski2023assessmentofprocess pages 1-11): Alex Plotkowski, Gerry Knapp, John Coleman, Benjamin Stump, and Matt Rolchigo. Assessment of process modeling tools for determining variability in additively manufactured parts. ArXiv, Mar 2023. URL: https://doi.org/10.2172/1989564, doi:10.2172/1989564. This article has 6 citations.

21. (plotkowski2023assessmentofprocess pages 28-30): Alex Plotkowski, Gerry Knapp, John Coleman, Benjamin Stump, and Matt Rolchigo. Assessment of process modeling tools for determining variability in additively manufactured parts. ArXiv, Mar 2023. URL: https://doi.org/10.2172/1989564, doi:10.2172/1989564. This article has 6 citations.

22. (fang2021datadrivenanalysis pages 11-14): Lichao Fang, Lin Cheng, Jennifer A. Glerum, Jennifer Bennett, Jian Cao, and Gregory J. Wagner. Data driven analysis of thermal simulations, microstructure and mechanical properties of inconel 718 thin walls deposited by metal additive manufacturing. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2110.07108, doi:10.48550/arxiv.2110.07108. This article has 3 citations.

23. (kuprienko2025analysisofnickel pages 87-94): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

24. (kuprienko2025analysisofnickel pages 113-120): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

25. (kuprienko2025analysisofnickel pages 30-36): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

26. (kuprienko2025analysisofnickel pages 106-113): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

27. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

28. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

29. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

30. (nemani2024advancementsinadditive pages 106-108): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

31. (yadav2020parametricinvestigationand pages 13-13): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.
