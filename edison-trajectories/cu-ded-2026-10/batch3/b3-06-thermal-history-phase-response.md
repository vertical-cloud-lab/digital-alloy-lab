<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: e2e87126-d111-493e-82ca-e89a442c49f3
- Submitted: 2026-10-17T05:46:07Z
- Fetched: 2026-10-17T06:16:57Z (status: success)
- Raw trajectory JSON: ../raw/b3-06-thermal-history-phase-response.json.gz
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

QUESTION: What quantitative links exist between laser-DED or laser-cladding
thermal history and the phases of NAB and Cu-Ni deposits? Report measured or
modeled cooling rates (K/s), interlayer temperatures, linear energy
(J/mm), substrate cooling (e.g. water-cooled substrates), and the resulting
beta-prime martensite fraction, kappa precipitate size and type, Widmanstatten
alpha, dendrite or cell spacing, and Ni/Fe/Mn microsegregation, together with
any corrosion or hardness consequence. Include Hyatt, Magee and Betancourt
1998 (laser-clad NAB, 42.5-595 J/mm), Jia et al. 2025 (water cooling), Li et
al. 2021 (LMD NAB), and studies of intrinsic heat treatment by later layers.
Which thermal-history variables (peak reheat temperature, time above the
beta solvus, cooling rate through 800-500 C) are most predictive?

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

QUESTION: What quantitative links exist between laser-DED or laser-cladding
thermal history and the phases of NAB and Cu-Ni deposits? Report measured or
modeled cooling rates (K/s), interlayer temperatures, linear energy
(J/mm), substrate cooling (e.g. water-cooled substrates), and the resulting
beta-prime martensite fraction, kappa precipitate size and type, Widmanstatten
alpha, dendrite or cell spacing, and Ni/Fe/Mn microsegregation, together with
any corrosion or hardness consequence. Include Hyatt, Magee and Betancourt
1998 (laser-clad NAB, 42.5-595 J/mm), Jia et al. 2025 (water cooling), Li et
al. 2021 (LMD NAB), and studies of intrinsic heat treatment by later layers.
Which thermal-history variables (peak reheat temperature, time above the
beta solvus, cooling rate through 800-500 C) are most predictive?

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


# Thermal history and phase selection in deposited marine copper alloys

**Evidence boundary.** The clearest quantitative laser-DED evidence is for nickel–aluminum bronze (NAB), not Cu–Ni. The commonly quoted **10³–10⁴ K/s** laser-metal-deposition cooling rate is a process-level estimate, **not a measured cooling curve for the Li et al. specimens**. No source examined establishes a numerical laser-DED cooling-rate-to-β′-fraction relationship, a validated κ-size-to-seawater-corrosion relationship, or performance equivalent to wrought C71500 in a matched seawater test. Here, *linear energy* means nominal laser power divided by travel speed; it is not absorbed energy or an independently measured cooling rate. (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 19-24)

## Direct laser deposition and controlled-cooling evidence

1. **Hyatt, C. V., K. H. Magee, and T. Betancourt, “The Effect of Heat Input on the Microstructure and Properties of Nickel Aluminum Bronze Laser Clad with a Consumable of Composition Cu-9.0Al-4.6Ni-3.9Fe-1.2Mn,” *Metallurgical and Materials Transactions A* 29 (1998): 1677–1690. DOI: 10.1007/s11661-998-0090-5.** **Process:** laser cladding, using the stated consumable on **cast NAB**, not demonstrated single-stream pre-alloyed powder DED. **Composition:** Cu balance–9.0Al–4.6Ni–3.9Fe–1.2Mn wt%. A subsequent dissertation’s account of the inaccessible original reports **42.5–595 J/mm** for single- and multibead layers. At **42.5 J/mm** the microstructure was almost wholly martensitic, apart from some grain-boundary α; secondary Widmanstätten α appeared by **47.2 J/mm**, and primary intragranular Widmanstätten α began around **150 J/mm**, increasing and coarsening at higher input. Hardness generally fell as Widmanstätten α increased, although reported peak microhardness exceeded **300 HV** under all studied welding conditions. These are **qualitative phase proportions**, not measured β′ volume fractions. The consulted account gives **no corrosion medium, exposure duration, κ-size series, or deposit cooling-rate series** for this experiment; the article itself could not be inspected. **[CITE] [NUMBERS] [NOVELTY-RISK: NAB laser cladding and heat-input/phase mapping already exist] [GAP: no verified quantitative phase–seawater-performance map].** (kuprienko2025analysisofnickel pages 50-55)

   **Do not attribute related simulated rates to Hyatt’s 42.5–595 J/mm clads.** In the same historical literature surveyed by Kuprienko, separate Gleeble simulations of NAB weld/reheat microstructures yielded **750 K/s water-quenched** and **188 K/s air-quenched** cooling over **800–500 °C**, and up to **3000 K/s** in a water-quenched *reheat simulation*. Predominantly martensitic water-quenched structures contained grain-boundary/Widmanstätten α and **Fe-rich, approximately 10–50 nm cuboids**, assigned only tentatively to κiv. These are **simulated specimen** histories, not measurements on a water-cooled laser-DED substrate. **[NUMBERS] [GAP].** (kuprienko2025analysisofnickel pages 50-55)

2. **Li, Boyuan, Han Zheng, Changjun Han, and Kun Zhou, “Nanotwins-Containing Microstructure and Superior Mechanical Strength of a Cu–9Al–5Fe–5Ni Alloy Additively Manufactured by Laser Metal Deposition,” *Additive Manufacturing* 39 (2021): 101825. DOI: 10.1016/j.addma.2020.101825.** **Process:** single pre-alloyed, gas-atomized **blown-powder LMD**; measured feedstock Cu **80.35 ± 0.91**, Al **9.70 ± 0.89**, Fe **5.48 ± 0.86**, Ni **4.47 ± 0.60 wt%**. Nominal powder cut **45–106 μm**, measured D10/D50/D90 **49.76/76.29/116.46 μm**; Hall flow, apparent density, and oxygen were **not reported**. The investigated dense-build window was approximately **1000–1500 W**, **0.5–1.5 m/min**, **1.5–2 mm hatch**. Calculated *nominal* linear energies for documented samples S1–S4 at 1500 W and 0.5, 1, 1.5, and 2 m/min are respectively **180, 90, 60, and 45 J/mm**; the highest measured relative density was **99.55%** at **90 J/mm** (S2). Excessive power produced cracked single tracks; low-input sample S5 developed lack-of-fusion pores and interlayer delamination. **[CITE] [NUMBERS] [NOVELTY-RISK: pre-alloyed NAB powder, laser DED, density, and microstructure are established].** (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand media 8e734898)

   At the melt-pool center Li et al. identified plate-like **β\*** transformation product, approximately **250 nm** wide, and primary grain-boundary Widmanstätten **α sideplates 600–900 nm** wide, with secondary sideplates. At the boundary, **blocky β\*** and intragranular basketweave Widmanstätten α occurred. **β\*** is the authors’ collective designation for unusual martensitic products: their TEM did **not** establish that every plate is crystallographic **β′**. Twin spacing was **8.9–15.6 nm**; Fe₃Al/κII and NiAl clusters had an approximate **50 nm radius**. Fe-rich precipitates occurred in α and β\*, Ni-rich precipitates in β\*, and Al enrichment occurred at neighboring β\*-plate interfaces. Coarse-scale melt-pool EDS maps appeared homogeneous: they do **not** prove zero nanoscale Ni/Fe segregation. The paper describes microscale *α/β\* cellular morphology*, not a measured solidification-cell or dendrite-spacing-versus-cooling-rate calibration. Yield strength was **593–713 MPa**, ultimate tensile strength **769–949 MPa**, and typical elongation **10–12%**, although a porous fast-scan sample reached only **3.04%** elongation. **No seawater-corrosion experiment, measured interlayer temperature, β′ volume fraction, or deposit-specific measured cooling rate was reported.** **[NUMBERS] [NAVY: marine/offshore application, not evidence of US Navy funding] [GAP: corrosion-linked phase quantification].** (li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 24-29, li2021nanotwinscontainingmicrostructureand pages 19-24)

3. **Jia, Zhiyuan, Zhandong Wang, Mingzhi Chen, Kai Zhao, Guifang Sun, and En-Hou Han, “Tailoring Microstructural Evolution in Laser Deposited Nickel-Aluminum Bronze Alloy by Controlling Water Cooling Condition,” *Journal of Materials Processing Technology* (2025). DOI: 10.1016/j.jmatprotec.2024.118659.** **Process:** laser-deposited NAB with controlled water cooling, as identified by its title and bibliographic record. **[CITE] [NOVELTY-RISK: actively changing heat extraction in laser-deposited NAB is not new].** The original full text was unobtainable. Accordingly, its **powder-versus-wire feed, composition, water-cooling geometry, cooling rates, interlayer temperatures, β′ fractions, κ types/sizes, hardness, and corrosion results cannot responsibly be supplied or inferred from its title**. In particular, the Gleeble water-quench rates above must **not** be presented as Jia’s deposited-substrate measurements. **[GAP: independently verify Jia before assigning numerical benchmarks].** (kuprienko2025analysisofnickel pages 50-55, hatala2024aninvestigationof pages 2-4)

4. **Hatala, Glenn W., Edward Reutzel, and Qian Wang, “An Investigation of Thermomechanical Behavior in Laser Hot Wire Directed Energy Deposition of NAB: Finite Element Analysis and Experimental Validation,” *Metals* 14 (2024): 1143. DOI: 10.3390/met14101143.** **Process:** **laser hot-wire DED**, not powder DED; measured deposited MIL-CuNiAl composition Cu **81.7**, Al **8.67**, Ni **5.40**, Fe **3.29**, Mn **0.81**, Si **0.11 wt%**, on **C63000 NAB**. Main-pass parameters were **9 kW**, **7 mm/s** (**approximately 1286 J/mm nominal laser energy**, excluding hot-wire Joule heating); four beads per layer, **5 s interpass** and **24 s interlayer** dwell, with temperature recorded at three substrate thermocouples. The validated FE temperature-history error was at most **5%** for single-layer and **6%** for multilayer builds. A **500 °C model stress-relaxation threshold** helped reproduce distortion; it is **not** a measured β solvus or proof of a particular κ fraction. The work establishes a practical thermal-model precedent but reports **no measured phase fractions, deposit cooling rate through 800–500 °C, corrosion, or powder metrics**. **[CITE] [NUMBERS] [NAVY: maritime component application] [NOVELTY-RISK: FE-plus-thermal-history validation exists] [GAP: couple validated thermal histories to phase and corrosion observations].** (hatala2024aninvestigationof pages 15-16, hatala2024aninvestigationof pages 1-2, hatala2024aninvestigationof pages 5-8, hatala2024aninvestigationof pages 4-5, hatala2024aninvestigationof pages 8-10)

5. **Doyle, Ryan P., *Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition*, Oregon State University thesis (2022), chapter 3, “Effect of Wire-Fed Laser Directed Energy Deposition Parameters and Heat Treatment on the Microstructure and Mechanical Properties of NAB C95800.” DOI: not located.** **Process:** **wire-laser DED**, *not* a NAB powder experiment; the other thesis chapter’s powder and LPBF numbers concern a different high-entropy alloy and must not be assigned to NAB. C95800 feedstock was Cu **82.0**, Al **8.64**, Ni **4.21**, Fe **3.19**, Mn **1.32 wt%**. Four as-deposited parameter sets, **800 W/300, 1000 W/600, 1200 W/600, and 1200 W/900 mm/min**, correspond to calculated **160, 100, 120, and 80 J/mm** and measured relative densities **99.84%, 99.58%, 99.89%, and 99.61%**, respectively. As-deposited α and darker Fe/Ni-enriched regions were observed; the study’s SEM/EDS did **not** resolve κ particle size or β′ fraction. A **675 °C/6 h furnace-cooled** *post-build* treatment changed XRD intensities and Ni/Al segregation; it **cannot** be treated as evidence that intrinsic reheating has the same effect. As deposited versus treated: hardness **218.8 ± 4.4 versus 204.1 ± 3.1 HV**; yield **410.5 ± 6.3 versus 372.2 ± 6.7 MPa**; ultimate strength **757.8 ± 5.4 versus 714.5 ± 8.3 MPa**; elongation **29.0 ± 1.0% versus 31.2 ± 0.25%**. There was **no corrosion test**. The thesis acknowledges Navy grant support. **[NUMBERS] [NAVY] [NOVELTY-RISK: as-deposited NAB on laser DED already shown] [GAP: powder/thermal cycling/corrosion together].** (doyle2022additivemanufacturingof pages 43-47, doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

## Later-layer reheating, cooling controls, and corrosion comparisons

6. **Li, Boyuan, Changjun Han, Yuxi Xie, Paulo Jorge da Silva Bartolo, and Kun Zhou, “Microstructural Heterogeneity Induced by Thermal Accumulation in a Nickel–Aluminum–Bronze Alloy Additively Manufactured via Directed Energy Deposition,” *CIRP Annals* 72 (2023): 133–136. DOI: 10.1016/j.cirp.2023.04.008.** **Process:** DED NAB. **[CITE] [NOVELTY-RISK: build-height thermal accumulation and resulting heterogeneity have been studied].** Its original paper was unobtainable here; therefore **specific peak reheat temperatures, dwell above β solvus, cooling rates, β′/κ fractions, and property gradients are unverified**. Treat the paper as a required priority for checking intrinsic-heat-treatment novelty, not as quantitative proof of a particular mechanism. Independently, Li’s accessible 2021 LMD study already shows distinct center-versus-boundary martensite/α morphologies without reporting each layer’s reheating curve. **[GAP: measured repeated thermal histories tied to quantitative as-deposited phases and seawater attack].** (li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 19-24)

7. **Kuprienko, Alexey, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*, PhD dissertation, Ohio State University (2025). DOI: not located.** **Process:** primarily **wire-arc DED (WAAM)** NAB followed by *separate* Gleeble thermal simulations; nominal wire **81.35Cu–9.09Al–3.94Fe–4.53Ni–1.00Mn wt%**. In original experiments, holding at **1035 °C for 2 versus 60 s**, followed by respective approximate cooling rates of **424 versus 394 K/s** in the compared cases, produced markedly different structures: the short hold largely retained preceding α-grain/melt-pool/layer-band structure, while the long hold produced prior-β-boundary α and intragranular Widmanstätten α. Other measured Gleeble cooling segments included **800–500 °C averages of 180 and 277 K/s**. Those observations make **time at peak temperature a demonstrable confounder of a cooling-rate-only model**, without providing a β′-fraction calibration. The thesis also reports that trailing liquid-nitrogen cooling *close* to a WAAM arc caused a modeled temperature dip and recovery—a miniature reheat—and could **coarsen** microstructure and reduce hardness; cooling farther behind the arc did not significantly change microstructure. This was supported by the **Office of Naval Research Manufacturing Science Program**. **[CITE] [NUMBERS] [NAVY] [GAP: arc-derived kinetics must be validated for powder-laser DED].** (kuprienko2025analysisofnickel pages 147-152, kuprienko2025analysisofnickel pages 131-137, kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 120-125)

8. **Huo, Renjie, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen, “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing,” *Materials* 18 (2025): 2205. DOI: 10.3390/ma18102205.** **Process:** **CMT wire-arc DED**, *not laser DED*. Wire: Cu balance–**8.73Al–5.90Fe–4.52Ni–1.39Mn wt%**; **interlayer temperature <50 °C**. Calculated arc heat inputs **243.8, 378.8, 502.8, 644.7 J/mm** progressively coarsened α grains (**38.26 to 74.62 μm** overall) and κ from submicron/network-like material toward micron- to tens-of-microns/needle-like features. Measured hardness across the four conditions was **192.4 ± 6.9, 182.3 ± 2.8, 178.9 ± 2.9, 166.9 ± 0.3 HV**. In **aerated, static 3.5 wt% NaCl at 25 ± 5 °C**, with **1 h open-circuit stabilization**, polarization gave **i_corr = 2.56 ± 0.04, 3.85 ± 0.11, 5.03 ± 0.08, 7.52 ± 0.07 μA/cm²**; the corresponding fitted polarization potentials were **−269.61 ± 40, −466.62 ± 10, −517.77 ± 20, −700.94 ± 15 mV**. Film resistance **R_f fell from 1152 to 185.8 Ω·cm²** and charge-transfer resistance **R_ct from 2485 to 707 Ω·cm²** at the endpoints. These are **short NaCl electrochemical tests, not natural seawater, ASTM D1141 substitute seawater, flowing seawater, or 30-day immersion**; reported polarization potential must not be conflated with the distinct 1-h OCP readings. **[CITE] [NUMBERS] [NAVY: marine-engineering application, funding not established] [NOVELTY-RISK: heat input–κ–corrosion link already demonstrated in arc DED] [GAP: powder-laser validation and long-exposure comparison].** (huo2025modulatingheatinput pages 15-16, huo2025modulatingheatinput pages 7-10, huo2025modulatingheatinput pages 13-15, huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 2-4, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput media 19fa7e37)

9. **de Luca, Ricardo, et al., “Correlation of Solidification Thermal Variables with Microstructure and Hardness in CuMn11Al8Fe3Ni3 Manganese–Aluminum–Bronze Alloy,” *Materials* 18 (2025): 234. DOI: 10.3390/ma18020234.** **Process:** **directionally cast**, *not laser or additive manufacturing*, against a water-cooled base. Measured ingot composition Cu **74.63**, Mn **11.01**, Al **8.93**, Fe **2.37**, Ni **1.59 wt%**. Measured near-liquidus cooling rates declined from **13.03 K/s at 4 mm** to **0.23 K/s at 53 mm** from the chilled surface; reported image-classified *secondary β* fraction rose from **32.10% to 48.50%**, while Brinell hardness decreased **199 to 184 HB** and local Vickers microhardness moved oppositely **222 to 244 HV**. **This β quantity must not be relabeled β′ martensite**, and a *near-liquidus* rate must not be substituted for cooling over **800–500 °C**. No corrosion test or cell-spacing calibration was reported. **[NUMBERS] [GAP: a water-cooled cast analogue is not Jia’s laser-deposited result].** (luca2025correlationofsolidification pages 6-9, luca2025correlationofsolidification pages 1-3, luca2025correlationofsolidification pages 4-6)

**Cu–Ni and benchmark limitation.** None of the accessible evidence establishes for pre-alloyed **Cu–10–30Ni–Fe–Mn–Cr blown-powder laser DED** a paired measurement of cooling rate, Cu–Ni solidification-cell/dendrite spacing, quantitative Ni/Fe/Mn partitioning, and *as-deposited* seawater corrosion; none documents a matched repair interface on **wrought C71500**, nor a side-by-side 30-day natural/ASTM D1141 seawater comparison with wrought **70–30 Cu–Ni**. The NAB NiAl/Fe₃Al κ and β′ transformation results should **not** be transferred to the largely Cu–Ni alloy family as though identical phases were expected. Likewise, no examined NAB laser study reports a defensible **selective-attack depth versus measured thermal cycle**, or powder Hall flow/apparent density/oxygen by alloy lot. **[GAP].** (li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 4-9, doyle2022additivemanufacturingof pages 53-58, huo2025modulatingheatinput pages 10-13)

## Which thermal-history variables are most predictive?

**Mechanistic ranking, not a published multivariable predictive fit:** **(1) peak *local* reheat temperature relative to the composition-dependent β and κ solvi, together with (2) cumulative time above those boundaries over subsequent passes**, because these determine whether earlier α/κ structure dissolves or survives; Kuprienko’s approximately matched **394–424 K/s** comparisons nevertheless changed structure dramatically when the **1035 °C hold changed from 2 to 60 s**. **(3) Cooling rate through 800–500 °C** then helps discriminate diffusional Widmanstätten α/κ precipitation from retained β capable of later martensitic transformation; record the *subsequent lower-temperature portion* too, rather than assuming β′ forms entirely in the 800–500 °C interval. **(4) Initial solidification gradient/rate and (5) interlayer baseline temperature, dwell, substrate contact and build height** help determine cellular-scale structure and the preceding three descriptors. Linear energy is a useful controllable covariate but cannot replace these local histories; Li’s approximately **45–180 J/mm** nominal conditions supplied no measured phase-fraction-versus-rate fit, while Hatala’s validated thermocouple model supplied no phase-fraction measurements. Running thermal-history-informed CALPHAD against equilibrium-only and no-physics baselines is therefore a **testable model-comparison proposal**, not an already demonstrated phase/corrosion prediction in these sources. (kuprienko2025analysisofnickel pages 50-55, li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 9-14, hatala2024aninvestigationof pages 15-16, hatala2024aninvestigationof pages 8-10, kuprienko2025analysisofnickel pages 147-152, kuprienko2025analysisofnickel pages 131-137)

## Top 5 things the PI should know

1. **Do not claim powder-fed NAB laser DED itself as novel:** Li 2021 produced **>99%-dense** pre-alloyed NAB powder deposits; make *alloy design plus quantified thermal-history-to-as-deposited seawater performance* the distinction. (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9)
2. **Check Jia 2025 and Li 2023 in full before finalizing novelty language:** water-cooled laser deposition and thermal-accumulation heterogeneity both have direct prior art, but their numerical results were not verifiable here. (li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 19-24)
3. **Instrument repeated local reheats, not just power/speed:** a **2-to-60-s hold at 1035 °C** altered NAB structure despite similar subsequent rapid cooling; track *peak, cumulative time above composition-specific solvi, and 800–500 °C rate*. (kuprienko2025analysisofnickel pages 147-152, kuprienko2025analysisofnickel pages 131-137)
4. **Keep comparison classes honest:** Hyatt is cast-substrate laser cladding, Doyle and Hatala are **wire-laser**, Huo and Kuprienko are **wire-arc**, and de Luca is **cast**. Huo’s roughly **threefold i_corr increase** is an informative *arc-process, short-NaCl* warning, **not** proof about laser-DED deposits in seawater. (kuprienko2025analysisofnickel pages 50-55, doyle2022additivemanufacturingof pages 53-58, hatala2024aninvestigationof pages 4-5, huo2025modulatingheatinput pages 10-13)
5. **The central unresolved benchmark is a matched, as-deposited corrosion qualification:** compare optimized powder-DED NAB/Cu–Ni, both self-built and on their intended repair substrates, with wrought **C71500** under the *same explicitly specified* solution, duration, flow, finish and selective-attack measurements; published tensile strength or 1-h NaCl polarization alone cannot establish that target. (li2021nanotwinscontainingmicrostructureand pages 4-9, doyle2022additivemanufacturingof pages 53-58, huo2025modulatingheatinput pages 10-13)

References

1. (li2021nanotwinscontainingmicrostructureand pages 1-4): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

2. (li2021nanotwinscontainingmicrostructureand pages 9-14): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

3. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

4. (li2021nanotwinscontainingmicrostructureand pages 19-24): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

5. (kuprienko2025analysisofnickel pages 50-55): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

6. (li2021nanotwinscontainingmicrostructureand media 8e734898): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

7. (li2021nanotwinscontainingmicrostructureand pages 14-19): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

8. (li2021nanotwinscontainingmicrostructureand pages 24-29): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

9. (hatala2024aninvestigationof pages 2-4): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

10. (hatala2024aninvestigationof pages 15-16): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

11. (hatala2024aninvestigationof pages 1-2): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

12. (hatala2024aninvestigationof pages 5-8): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

13. (hatala2024aninvestigationof pages 4-5): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

14. (hatala2024aninvestigationof pages 8-10): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

15. (doyle2022additivemanufacturingof pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

16. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

17. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

18. (kuprienko2025analysisofnickel pages 147-152): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

19. (kuprienko2025analysisofnickel pages 131-137): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

20. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

21. (kuprienko2025analysisofnickel pages 120-125): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

22. (huo2025modulatingheatinput pages 15-16): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

23. (huo2025modulatingheatinput pages 7-10): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

24. (huo2025modulatingheatinput pages 13-15): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

25. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

26. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

27. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

28. (huo2025modulatingheatinput media 19fa7e37): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

29. (luca2025correlationofsolidification pages 6-9): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

30. (luca2025correlationofsolidification pages 1-3): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

31. (luca2025correlationofsolidification pages 4-6): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.
