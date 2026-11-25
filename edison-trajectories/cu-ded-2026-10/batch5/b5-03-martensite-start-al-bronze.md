<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: e66da3ae-694f-4411-aa47-cfd00d8633bb
- Submitted: 2026-10-17T06:20:05Z
- Fetched: 2026-10-17T06:51:55Z (status: success)
- Raw trajectory JSON: ../raw/b5-03-martensite-start-al-bronze.json.gz
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

QUESTION: What composition-based rules predict whether beta-prime martensite
is retained in aluminum bronzes and NAB after fast cooling? Cover (a)
martensite start (Ms) equations for Cu-Al-Ni and Cu-Al-Mn shape memory
alloys as functions of Al, Ni, Mn (and Fe) content, and whether they apply
to NAB compositions; (b) the "aluminium equivalent" rules used for aluminum
bronzes (weighting of Fe, Ni, Mn, Si, Sn relative to Al) and their link to
beta content; (c) the beta-solvus and eutectoid temperatures vs composition;
and (d) kappa precipitation kinetics models (JMAK fits, TC-PRISMA /
Kampmann-Wagner, phase-field) for NAB under rapid cooling or cyclic
reheating. Which could serve as a cheap, per-composition physics input next
to CALPHAD, and how accurate is each?

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

QUESTION: What composition-based rules predict whether beta-prime martensite
is retained in aluminum bronzes and NAB after fast cooling? Cover (a)
martensite start (Ms) equations for Cu-Al-Ni and Cu-Al-Mn shape memory
alloys as functions of Al, Ni, Mn (and Fe) content, and whether they apply
to NAB compositions; (b) the "aluminium equivalent" rules used for aluminum
bronzes (weighting of Fe, Ni, Mn, Si, Sn relative to Al) and their link to
beta content; (c) the beta-solvus and eutectoid temperatures vs composition;
and (d) kappa precipitation kinetics models (JMAK fits, TC-PRISMA /
Kampmann-Wagner, phase-field) for NAB under rapid cooling or cyclic
reheating. Which could serve as a cheap, per-composition physics input next
to CALPHAD, and how accurate is each?

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


# Composition rules for retained β′ in aluminum bronze

**Bottom line.** Composition alone does not determine whether a rapidly cooled nickel–aluminum bronze (NAB) deposit retains β′ martensite. The alloy must first form high-temperature β; enough β must then survive competing α and κ transformations during cooling or subsequent layer reheating. A martensite-start temperature (*M*s) is therefore **not** a retained-β′ fraction or a corrosion prediction. For inexpensive per-composition screening, CALPHAD-derived β stability evaluated along representative thermal histories is better justified than transferring shape-memory-alloy *M*s equations to NAB; its predictive accuracy for DED still requires measurement. (recarte1999dependenceofthe pages 2-4, cuevas2002microstructurecharacterizationofa pages 26-29, iorio2015determinationofrolling pages 17-23)

The following comparison separates verified rules from proposed, uncalibrated model inputs.

| Screening input | Verified rule or output | Calibration domain | Reported accuracy | Use for NAB/DED composition screening |
|---|---|---|---|---|
| Recarte et al. (1999) Cu–Al–Ni martensite start | Ms (°C) = 2433 − 169.9Al − 19.1Ni; Al and Ni in wt% | 17 Cu–Al–Ni SMA single crystals; 900 °C for 20 min followed by iced-water quenching; β transformed to 18R or 2H martensite | Maximum experimental–calculated discrepancy: **98 °C** | **Unvalidated extrapolation to NAB.** Use only as a weak prior or engineered feature because NAB has lower Al, Fe and Mn additions, and competing α/κ precipitation. (recarte1999dependenceofthe pages 2-4) |
| Sampath et al. (2019) multicomponent Cu–Al martensite start | Ms (°C) = 706 − 32.3Al − 20.7Fe + 41.5Mn − 26.3Ni; source table reports wt% compositions | Pooled Cu–Al–Fe, Cu–Al–Mn, and Cu–Al–Ni SMA data, principally about 12–14 wt% Al | R² = **87.96%**; adjusted R² = **81.93%**; residual standard error = **38.3851 °C** | **Unvalidated for NAB and DED.** It captures fitted Fe, Mn, and Ni trends, but the mixed SMA datasets and composition range make it unsuitable as a hard β′ classifier. (sampath2019experimentalandtheoretical pages 3-6) |
| Binary Cu–Al eutectoid datum | β → α + γ₂ at **565 ± 2 °C** and **11.96 ± 0.05 wt% Al**; cooling near 10 °C/s can suppress the diffusional eutectoid and produce β′ | Binary Cu–Al rather than Ni–Fe–Mn-bearing NAB | Precise eutectoid point reported; no NAB prediction error available | **Cannot be transferred quantitatively to NAB.** Use only as a binary sanity check because NAB additions alter the phase fields and promote κ phases. (hall1977stresscorrosioncracking pages 107-116) |
| NAB aluminium-equivalent coefficient rule | No defensible equation assigning relative Al weights to Fe, Ni, Mn, Si, and Sn was verified in the retrieved primary literature | Not established | **Unknown** | Do not invent coefficients or treat undocumented handbook variants as universal. Any such rule should be provenance-tracked and fitted locally against measured β or β′ fraction. (cuevas2002microstructurecharacterizationofb pages 21-26, cuevas2002microstructurecharacterizationofa pages 21-26) |
| CALPHAD β fraction along the DED thermal trajectory | Calculate β stability, fraction, and driving force versus composition and local temperature–time history; compare trajectory-aware, equilibrium-only, and no-physics models | Potentially applicable per composition, subject to thermodynamic-database fidelity and absent AM-specific kinetic calibration | **Unknown until validated** using DSC, dilatometry, XRD, or EBSD on candidate alloys | **Best cheap physics input.** Use β fraction, time above the β solvus, driving force, and quench rate as surrogate features; model retained β′ as a learned nonequilibrium residual rather than an equilibrium phase prediction. (cuevas2002microstructurecharacterizationofb pages 26-29, cuevas2002microstructurecharacterizationofa pages 26-29) |
| JMAK κ-precipitation model | No retrieved NAB/DED fit supplied an Avrami exponent, temperature-dependent rate constant, or activation energy | No verified rapid-cooling or cyclic-reheating calibration | **Unknown** | Not currently deployable as a predictive node. Generate isothermal and continuous-cooling data before fitting separate α, κIII, and κIV transformations. |
| TC-PRISMA or Kampmann–Wagner κ model | No retrieved NAB parameterization was validated for DED thermal histories | No verified nucleation-site density, interfacial energy, mobility, or multicycle calibration | **Unknown** | A possible second-generation node after calibration, but currently carries greater setup cost and false-precision risk than CALPHAD-derived scalar features. |
| Phase-field α/κ/β model | No retrieved NAB phase-field model was validated under DED rapid cooling or cyclic reheating | No verified NAB/DED calibration | **Unknown** | Too expensive and under-calibrated for routine per-composition Bayesian-optimization queries; reserve it for mechanistic studies of a few selected compositions. |


*Table: Verified composition and transformation rules are compared by domain, error, and suitability for rapid NAB/DED screening. The table distinguishes practical low-cost inputs from unvalidated extrapolations and unavailable kinetic calibrations.*

## 1. Martensite-start equations: useful warnings, not NAB classifiers

**[CITE] [NUMBERS] [GAP]** V. Recarte, R. B. Pérez-Sáez, E. H. Bocanegra, M. L. Nó, and J. San Juan, “Dependence of the martensitic transformation characteristics on concentration in Cu–Al–Ni shape memory alloys,” *Materials Science and Engineering A* **273–275**, 380–384 (1999), **DOI: 10.1016/S0921-5093(99)00302-0**. **Process:** solution-treated and iced-water-quenched Cu–Al–Ni single crystals, not DED. Seventeen crystals were treated at 900 °C for 20 min. With Al and Ni in **wt%**, the reported fit is *M*s (°C) = **2433 − 169.9Al − 19.1Ni**; its largest reported error is **98 °C**. More Al favors the γ′ rather than β′ martensite variant, while more Ni favors β′. These variant names describe the studied shape-memory transformations; the equation cannot establish how much β′ survives in Fe/Mn-containing NAB. No porosity, seawater, hardness, or powder measurements were part of this study. (recarte1999dependenceofthe pages 1-2, recarte1999dependenceofthe pages 2-4)

**[CITE] [NUMBERS] [GAP]** V. Sampath, Sai Venkata Gayathri, and R. Srinithi, “Experimental and theoretical analyses of transformation temperatures of Cu-based shape memory alloys,” *Bulletin of Materials Science* **42**, 229 (2019), **DOI: 10.1007/s12034-019-1911-4**. **Process:** pooled Cu-based shape-memory-alloy measurements, including cast, solutionized, quenched Cu–Al–Fe; not DED. Its Cu–Al-family regression is *M*s (°C) = **706 − 32.3Al − 20.7Fe + 41.5Mn − 26.3Ni**. The underlying composition table labels alloys in wt%; the fit reports **R² = 87.96%**, adjusted **R² = 81.93%**, and residual standard error **38.3851 °C**. The authors’ own Cu–12Al–4Fe and Cu–13Al–4Fe specimens were solutionized at 900 °C for 1 h, with an additional 950 °C treatment for one specimen; reported *M*s values are **224, 249, and 247 °C**, respectively. The compiled Cu–12.5Al–5Mn entry has *M*s **510 °C**. The paper does **not** establish an independently validated Cu–Al–Mn-only composition equation or an Fe coefficient valid for NAB. It reports no marine-corrosion, deposit-density, or powder tests. (sampath2019experimentalandtheoretical pages 1-2, sampath2019experimentalandtheoretical pages 2-3, sampath2019experimentalandtheoretical pages 3-6)

The extrapolation is substantial: the cited Cu–Al–Ni SMA table includes approximately **13–14 wt% Al**, whereas an experimentally characterized cast NAB contains **9.31 Al, 4.57 Ni, 4.92 Fe, and 1.23 Mn wt%**. For illustration, inserting that NAB composition into the Recarte formula yields roughly **764 °C**; that is an extrapolated arithmetic output, **not a measured NAB *M*s**. Applying the pooled Sampath regression gives roughly **269 °C**, illustrating disagreement rather than providing a validated answer. Neither fit accounts for the changing composition of *residual β* as α and κ form. (recarte1999dependenceofthe pages 2-4, sampath2019experimentalandtheoretical pages 3-6, ocejo2022corrosionbehaviorof pages 1-3)

## 2. “Aluminium equivalent,” β solvus, and eutectoid

**[GAP] Aluminium-equivalent coefficients.** I could not verify a primary-source aluminium-equivalent equation that assigns defensible numerical weights to **Fe, Ni, Mn, Si, and Sn relative to Al** across NAB compositions. Accordingly, no coefficient table or β-content threshold should be presented as an established universal rule. The physically supported qualitative observation is narrower: Ni and Fe modify the α/β balance and enable κ precipitation; **Ni can retard β decomposition**, so a simple sign or coefficient assigned from equilibrium phase balance need not predict retained β′. An equivalent-Al score, if used, should have its source, target response (**high-temperature β fraction versus room-temperature β′ fraction**), composition range, and prediction error specified separately. (cuevas2002microstructurecharacterizationof pages 21-26, cuevas2002microstructurecharacterizationofa pages 26-29, cuevas2002microstructurecharacterizationofb pages 21-26)

**[CITE] [NUMBERS] [GAP]** I. D. Hall, *Stress corrosion cracking of copper-base alloys*, PhD thesis, UNSW Sydney (1977), **DOI: 10.26190/unsworks/21044**. **Process:** discussion of cast/heat-treated binary aluminum bronzes, not DED. Hall reports the binary Cu–Al **β → α + γ₂** eutectoid as **565 ± 2 °C at 11.96 ± 0.05 wt% Al** and cites cooling around **10 °C/s** as sufficient to suppress that diffusional reaction and produce β′ in the discussed binary context. This is **not** the multicomponent NAB α + κ reaction or a composition-dependent NAB β-solvus equation. No powder, porosity, or marine-corrosion benchmark accompanies these phase-diagram numbers. (hall1977stresscorrosioncracking pages 107-116)

**[CITE] [NUMBERS] [NAVY]** A. M. Cuevas, *Microstructure characterization of friction-stir processed nickel [aluminum bronze]*, thesis (2002); **DOI not established in the retrieved record**. **Process:** cast NAB background and friction-stir processing, not DED. For a representative **Cu–9Al–5Ni–4Fe–1Mn wt%** bronze, the account places the onset of proeutectoid α formation near **950 °C** and an α + NiAl-type κIII eutectoid near **580 °C**; incompletely decomposed β can form β′. It also reports a marine-alloy compositional heuristic of **Ni greater than Fe**, ideally approximately **5 wt% Ni and 4 wt% Fe**, to limit second-phase attack. This is a compositional corrosion caution, not an aluminium-equivalent coefficient or independently quantified β′ prediction. No applicable seawater test duration, *i*corr, powder specification, or model error is supplied. (cuevas2002microstructurecharacterizationofa pages 26-29)

**[CITE] [GAP]** G. Iorio, *Determination of Rolling Parameters for Numerical Simulation of Cold Rolling of Nickel Aluminum Bronze*, thesis (2015); **DOI not established in the retrieved record**. **Process:** wrought/cast NAB background and rolling, not DED. Its account instead places α formation below approximately **1000 °C**, κ formation below **930 °C**, and a remaining-β → α + κIII reaction around **800 °C**. The different approximately **580 versus 800 °C** κ/eutectoid descriptions in the retrieved NAB secondary accounts must **not** be merged into one universal NAB transformation temperature: alloy chemistry, transformation identified, and thermal path need to be resolved with composition-specific CALPHAD and DSC/dilatometry. A validated Fe–Ni–Mn–Al **β-solvus-versus-composition equation** was not recovered. (cuevas2002microstructurecharacterizationofa pages 26-29, iorio2015determinationofrolling pages 17-23)

## 3. κ precipitation under cooling and reheating

**[GAP]** I did not recover a NAB-specific, quantitatively validated **JMAK/Avrami fit**—an exponent *n*, temperature-dependent rate constant *k*, and fitted error—for κ precipitation under DED-like rapid cooling or repeated layer reheating. Nor did the retrieved evidence substantiate calibrated NAB **TC-PRISMA/Kampmann–Wagner** nucleation-and-growth parameters or a **phase-field** prediction validated against that cycling. This is a limitation of the accessible evidence, not proof that no such work exists. Assigning a generic Avrami exponent or reported computational-model accuracy would manufacture precision. κI/κII, κIII, and fine κIV differ in chemistry and formation context, so a single uncalibrated “κ fraction” kinetic law is particularly difficult to defend. (cuevas2002microstructurecharacterizationofa pages 26-29, cuevas2002microstructurecharacterizationofb pages 21-26)

**Recommended cheap node:** query CALPHAD per candidate composition for the β field, equilibrium β fraction, competing α/κ stability, and transformation driving forces; pass those outputs, a representative local temperature–time trajectory, time in transformation windows, cooling rate, and reheating exposure to the learned microstructure model. Evaluate against **equilibrium-only CALPHAD** and **no-physics** baselines as proposed. This is a practical *feature design*, not a validated claim that equilibrium software predicts retained martensite. Fit the survival/decomposition component from measured as-deposited β′ and κ fractions before introducing JMAK; reserve precipitation software and phase-field for selected, experimentally calibrated compositions. Prediction errors for all these NAB/DED options remain **unreported in the retrieved evidence**. (cuevas2002microstructurecharacterizationofb pages 26-29, cuevas2002microstructurecharacterizationofa pages 26-29, iorio2015determinationofrolling pages 17-23)

## 4. Process and marine-performance benchmarks: do not conflate unlike tests

**[CITE] [NUMBERS] [NAVY]** I. Cobo Ocejo, M. V. Biezma Moraleda, and P. Linhardt, “Corrosion Behavior of Heat-Treated Nickel-Aluminum Bronze and Manganese-Aluminum Bronze in Natural Waters,” *Metals* **12**, 380 (2022), **DOI: 10.3390/met12030380**. **Process:** **cast** NAB, nominally **Cu–9.31Al–4.92Fe–4.57Ni–1.23Mn wt%**; not an AM deposit. As-cast material was compared with quenching from **850 °C/1 h** and with that quench followed by **600 °C/2 h** tempering. In **DIN 50905-4 simulated seawater, not ASTM D1141**, a **72 h potentiostatic** test gave **82.10 µA cm⁻²** for as-cast and **200.00 µA cm⁻²** for quenched-and-tempered NAB at **−100 mV versus SCE**. These are *current densities at imposed potential*, **not** *i*corr at free corrosion potential; neither *E*corr nor flow rate is established by the cited test. β-rich regions were selectively attacked in treated material. This is a Navy-*application* reference through NAB marine use, **not verified DoD funding**. No powder flow/oxygen, deposit density, or C71500 comparison is reported. (ocejo2022corrosionbehaviorof pages 3-5, ocejo2022corrosionbehaviorof pages 8-10, ocejo2022corrosionbehaviorof pages 1-3, ocejo2022corrosionbehaviorof media a0bf1dec)

**[CITE] [NUMBERS] [NAVY]** P. J. Rivero, C. Berlanga, J. F. Palacio, and M. V. Biezma-Moraleda, “Effect of Ti on Microstructure, Mechanical Properties and Corrosion Behavior of a Nickel-Aluminum Bronze Alloy,” *Materials Research* **24** (2021), **DOI: 10.1590/1980-5373-MR-2020-0335**. **Process:** sand-cast **Cu–9.5Al–4.8Fe–4.6Ni–1.3Mn–balance Cu wt%**, with or without **120 ppm Ti**, subsequently dehydrogenated; **not as-deposited AM**. In **3.5 wt% NaCl**, static **720 h** immersion gave **0.034% versus 0.020% mass loss** and reported corrosion rates **0.021 versus 0.023 mm yr⁻¹**, respectively; the study found **no significant improvement in corrosion susceptibility**. Vickers microhardness was **172.89 versus 206.89 HV**. Electrochemical testing followed **1 h** open-circuit stabilization and used an Ag/AgCl reference; *i*corr, *E*corr, seawater flow, deposit porosity, and powder size/flow/oxygen are not established in the cited results. The NaCl test is **not** equivalent to natural seawater or ASTM D1141 seawater. The Navy tag denotes application, not verified funding. (rivero2021effectofti pages 3-5, rivero2021effectofti pages 6-8, rivero2021effectofti pages 5-6, rivero2021effectofti pages 2-3, rivero2021effectofti pages 1-2)

**[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** R. P. Doyle, *Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition*, Oregon State University master’s thesis (2022); **DOI not established in the retrieved record**. **Process for its NAB results: wire-laser DED, *not* blown-powder DED**. C95800 feed wire was **Cu–8.64Al–4.21Ni–3.19Fe–1.32Mn wt%**, diameter **0.89 mm**, deposited on stainless steel. Candidate builds exceeded **99.5% relative density**. As-printed yield strength was **410.5 MPa**, UTS **757.8 MPa**, elongation **29.0%**, and hardness **218.8 HV**; after **675 °C/6 h** annealing, these were **372.2 MPa**, **714.5 MPa**, **31.2%**, and **204.1 HV**. A Navy grant is acknowledged. It establishes prior as-printed NAB laser deposition and thermal-treatment work, **not** the proposed pre-alloyed powder-feed optimization or a verified C71500 seawater benchmark. NAB powder particle size, Hall flow, apparent density, oxygen, and comparable *i*corr/*E*corr are **not applicable or not reported**. (doyle2022additivemanufacturingof pages 1-9, doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

**[NOVELTY-RISK] [GAP] Closest powder-process prior art requiring full-text verification.** A. J. Rayner *et al.*, “Directed Energy Deposition of UNS C63020 Nickel Aluminum Bronze Powder” (2024), **DOI: 10.1007/978-3-031-67398-6_13**, and K. Hu *et al.*, “Microstructure, mechanical and corrosion properties of additively manufactured nickel-aluminum bronze alloys: laser power directed energy deposition vs. laser powder fed fusion,” *Journal of Alloys and Compounds* **1066**, 187981 (2026), **DOI: 10.1016/j.jallcom.2026.187981**, were identified bibliographically but their full results were **not retrievable here**. They overlap **powder-fed NAB fabrication** and, for Hu *et al.*, corrosion testing; feedstock chemistry, size/flow/oxygen, density, electrolyte and exposure, *i*corr, hardness, and repair-substrate results therefore **cannot responsibly be quoted**. C.-L. Yao *et al.*, “A study on mechanical properties of CuNi2SiCr layered on nickel-aluminum bronze via directed energy deposition,” *Journal of Materials Research and Technology* **18**, 5337–5361 (2022), **DOI: 10.1016/j.jmrt.2022.04.159**, is additionally direct **DED-on-NAB-substrate** novelty-risk prior art, but the accessible record does not verify its feed method or quantitative results. None of these bibliographic leads substantiates the full proposed combination of **single-stream, newly pre-alloyed powders; both NAB and wrought Cu–Ni repair; as-deposited C71500-comparable seawater resistance; and network-guided alloy selection**. (doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

## Top 5 things the PI should know

1. **Do not use SMA *M*s as a β′ yes/no gate.** The best-documented Cu–Al–Ni rule has a **98 °C maximum error even in its quenched-SMA domain**; its transfer to roughly 9% Al, Fe/Mn-bearing NAB is unvalidated. (recarte1999dependenceofthe pages 2-4, ocejo2022corrosionbehaviorof pages 1-3)
2. **Separate β formation from β survival.** Composition-sensitive CALPHAD β/α/κ outputs plus cooling and reheating descriptors are defensible inexpensive physics features; retained β′ must be calibrated as a nonequilibrium outcome. (cuevas2002microstructurecharacterizationofa pages 26-29, iorio2015determinationofrolling pages 17-23)
3. **Do not assert a universal Fe/Ni/Mn/Si/Sn aluminium-equivalent equation or NAB κ kinetic accuracy.** Neither coefficient set nor DED-calibrated JMAK, TC-PRISMA, or phase-field error was verified; making and testing that calibration is a legitimate proposal gap. (cuevas2002microstructurecharacterizationofb pages 21-26, cuevas2002microstructurecharacterizationofa pages 21-26)
4. **Treat retained β-rich material as a corrosion-risk feature, but compare like with like.** Cast NAB showed **82.1 versus 200 µA cm⁻² at −100 mV SCE** after differing thermal treatments in one simulated seawater protocol; neither number is *i*corr, a C71500 comparison, or a 30-day immersion result. (ocejo2022corrosionbehaviorof pages 3-5, ocejo2022corrosionbehaviorof pages 8-10, ocejo2022corrosionbehaviorof media a0bf1dec)
5. **Position novelty against actual AM precedents, not against casting alone.** Navy-supported **wire-laser NAB DED** and identified **powder-fed NAB DED** already exist. The differentiator needs to be demonstrated in **pre-alloyed powder chemistry, dissimilar repair, as-deposited seawater benchmarks, and experimentally tested thermal-history-aware optimization**; quantitative prior-art powder claims await full-text verification. (doyle2022additivemanufacturingof pages 1-9, doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

References

1. (recarte1999dependenceofthe pages 2-4): V. Recarte, R. B. Pérez-Sáez, E. Bocanegra, M. Nó, and J. S. San Juan. Dependence of the martensitic transformation characteristics on concentration in cu–al–ni shape memory alloys. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 273:380-384, Dec 1999. URL: https://doi.org/10.1016/s0921-5093(99)00302-0, doi:10.1016/s0921-5093(99)00302-0. This article has 127 citations.

2. (cuevas2002microstructurecharacterizationofa pages 26-29): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

3. (iorio2015determinationofrolling pages 17-23): G Iorio. Determination of rolling parameters for numerical simulation of cold rolling of nickel aluminum bronze. Unknown journal, 2015.

4. (sampath2019experimentalandtheoretical pages 3-6): V Sampath, Sai Venkata Gayathri, and R Srinithi. Experimental and theoretical analyses of transformation temperatures of cu-based shape memory alloys. Bulletin of Materials Science, Jul 2019. URL: https://doi.org/10.1007/s12034-019-1911-4, doi:10.1007/s12034-019-1911-4. This article has 19 citations and is from a peer-reviewed journal.

5. (hall1977stresscorrosioncracking pages 107-116): Stress corrosion cracking of copper-base alloys This article has 1 citations.

6. (cuevas2002microstructurecharacterizationofb pages 21-26): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

7. (cuevas2002microstructurecharacterizationofa pages 21-26): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

8. (cuevas2002microstructurecharacterizationofb pages 26-29): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

9. (recarte1999dependenceofthe pages 1-2): V. Recarte, R. B. Pérez-Sáez, E. Bocanegra, M. Nó, and J. S. San Juan. Dependence of the martensitic transformation characteristics on concentration in cu–al–ni shape memory alloys. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 273:380-384, Dec 1999. URL: https://doi.org/10.1016/s0921-5093(99)00302-0, doi:10.1016/s0921-5093(99)00302-0. This article has 127 citations.

10. (sampath2019experimentalandtheoretical pages 1-2): V Sampath, Sai Venkata Gayathri, and R Srinithi. Experimental and theoretical analyses of transformation temperatures of cu-based shape memory alloys. Bulletin of Materials Science, Jul 2019. URL: https://doi.org/10.1007/s12034-019-1911-4, doi:10.1007/s12034-019-1911-4. This article has 19 citations and is from a peer-reviewed journal.

11. (sampath2019experimentalandtheoretical pages 2-3): V Sampath, Sai Venkata Gayathri, and R Srinithi. Experimental and theoretical analyses of transformation temperatures of cu-based shape memory alloys. Bulletin of Materials Science, Jul 2019. URL: https://doi.org/10.1007/s12034-019-1911-4, doi:10.1007/s12034-019-1911-4. This article has 19 citations and is from a peer-reviewed journal.

12. (ocejo2022corrosionbehaviorof pages 1-3): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

13. (cuevas2002microstructurecharacterizationof pages 21-26): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

14. (ocejo2022corrosionbehaviorof pages 3-5): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

15. (ocejo2022corrosionbehaviorof pages 8-10): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

16. (ocejo2022corrosionbehaviorof media a0bf1dec): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 10 citations.

17. (rivero2021effectofti pages 3-5): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

18. (rivero2021effectofti pages 6-8): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

19. (rivero2021effectofti pages 5-6): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

20. (rivero2021effectofti pages 2-3): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

21. (rivero2021effectofti pages 1-2): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

22. (doyle2022additivemanufacturingof pages 1-9): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

23. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

24. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.
