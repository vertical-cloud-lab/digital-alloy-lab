# Edison Scientific LITERATURE_HIGH Output — SDL State-of-the-Art for Metallic Alloy Discovery

**Task ID:** `5f2b1053-0c0f-4005-8253-cc073335d9f5`
**Mode:** LITERATURE_HIGH | **Date:** 2026-04-10 | **Size:** ~41K chars
**Part of:** Topic 3B Deep-Dive Series (10 queries, ~331K chars total)

> *Raw Edison Scientific output below. The query prompt appears first, followed by the model's structured response.*

---

Question: 
RESEARCH QUESTION: What is the state-of-the-art in self-driving laboratories (SDLs) for metallic alloy discovery, and how does a closed-loop powder→print→test platform compare?

Context: FLAIME proposes an autonomous closed-loop: CALPHAD screening → ultrasonic atomization → LPBF 3D printing → tensile testing → BOFN optimization loop. Need to assess novelty, feasibility, and competitive positioning.

Investigate:
1. Existing SDLs for alloy/metal discovery: A-Lab (LBNL), ORNL, Argonne, MIT, others. What materials and processes do they cover?
2. Are there any existing SDLs that include BOTH powder production AND additive manufacturing in the loop?
3. What is the typical cycle time for an SDL alloy experiment? How does powder→LPBF→tensile compare?
4. What throughput (compositions/month) have published SDLs achieved for metallic alloys?
5. Key challenges: alloy SDLs vs. thin-film/solution-phase SDLs — what makes metals harder?
6. BOFN (Bayesian Optimization of Function Networks) vs. standard BO for multi-stage processes: what literature exists?
7. How feasible is "≥200 compositions in 9 months" for a powder-to-part pipeline?
8. What role does ultrasonic atomization play in existing rapid alloy prototyping? (vs. arc melting, gas atomization, etc.)
9. Published examples of autonomous LPBF alloy optimization (if any)
10. What metrics do reviewers use to evaluate SDL proposals? (iteration speed, cost per experiment, autonomy level)

Cite all sources.


## Technical assessment: state-of-the-art SDLs for metallic alloy discovery and positioning of a powder→print→test closed loop (FLAIME-like)

### 1) State-of-the-art SDLs/MAPs relevant to metallic alloys: what they cover
Published “metal-relevant” autonomous/closed-loop platforms cluster into (i) thin-film metallic systems for rapid thermodynamics/phase mapping, (ii) bulk-alloy high-throughput synthesis/characterization with ML/active learning, and (iii) autonomous metal additive manufacturing (AM) focused on process control/parameter tuning rather than alloy composition.

**Thin-film metal SDLs (fastest cycle time; thermodynamics-focused):**
AMASE (Autonomous MAterials Search Engine) performs a real-time experiment–theory closed loop to map a temperature–composition phase diagram. It autonomously selects compositions/temperatures using Bayesian active learning, performs XRD and analysis, and updates CALPHAD predictions in real time. In a Sn–Bi eutectic thin-film campaign, a live autonomous run completed in just over **8 hours** and reduced required experiments by **~6×** compared with conventional mapping. This is a “CALPHAD-in-the-loop” reference implementation, but it is thin-film (not bulk), and does not include powder production, AM, or mechanical testing. (liang2025realtimeexperimenttheoryclosedloop pages 1-3)

**Bulk alloy SDL-like loops using AM-enabled synthesis (composition loop but not powder-production loop):**
A high-throughput bulk multi-principal-element alloy discovery platform uses directed energy deposition (DED/LENS) with **independently metered elemental powders** (four powder hoppers) enabling in situ alloying and composition variation. It integrates automated XRD/EDS/nano-hardness with an ML/active-learning loop. Reported synthesis throughput is **>100 compositions/week**, including a specific metric of **25 discrete bulk alloy samples in ~4 hours** (implying the >100/week rate). Reported composition control is **±5 at%**. This represents one of the closest published precedents for “bulk AM-in-the-loop” composition discovery, but it does **not** include powder production/atomization as part of the loop and does not report tensile testing in the loop (hardness is used). (nelaturu2024multiprincipalelementalloy pages 1-4, nelaturu2024multiprincipalelementalloy pages 16-20)

**Bulk high-throughput alloy characterization infrastructures (enablers rather than full autonomy):**
HT-READ proposes/implements compact multi-sample libraries (e.g., 16-sample rings) with automated fiducials and synchronized automated SEM/EDS/EBSD/nanoindentation and XRD fixturing, intended to accelerate characterization and iteratively feed data back into ML for next-round selection. It is a strong “high-throughput bulk alloy characterization” precedent, but explicit end-to-end autonomous campaign cycle times are not reported in the extracted text. (vecchio2021highthroughputrapidexperimental pages 19-33, vecchio2021highthroughputrapidexperimental pages 1-4)

**Metal AM autonomy (process loop rather than composition loop):**
Closed-loop LPBF autonomy in the retrieved literature primarily optimizes **process/controller parameters** (laser power/speed, scan strategy, thermal history control, controller gains), not alloy composition. For example, Bayesian optimization has been used to autotune in-layer PI controller parameters for LPBF; online tuning converged by **iteration 74** and offline tuning by **112 iterations**, reducing overheating but revealing potential microstructural side effects (e.g., lack-of-fusion porosity if laser power is under-assigned by the controller). These studies are highly relevant to the “print” portion of a powder→print→test pipeline, but they are not alloy-discovery loops. (kavas2025insitucontrollerautotuning pages 26-29, kavas2025insitucontrollerautotuning pages 1-3)

A compact comparative summary is provided here:

| Platform/paper | Materials domain | Synthesis/processing modality | What is measured | Closed-loop agent | Reported throughput/cycle time | Notes on relevance to powder→AM→test loop |
|---|---|---|---|---|---|---|
| **AMASE** (Liang et al., *Sci. Adv.* 2025) | Thin-film metallic alloy system (Sn–Bi eutectic phase diagram) | Thin-film composition spreads + thermal processing + XRD, coupled in real time to CALPHAD | Phase boundaries / phase diagram classification from XRD during temperature–composition mapping | Bayesian active learning / BO + GP classification + real-time CALPHAD/Thermo-Calc updating | One autonomous run completed in **just over 8 h**; achieved **~6× reduction** in experiments vs conventional mapping | Strong example of real-time experiment–theory closed loop for metals, but it is **thin-film**, not bulk; no powder production, no additive manufacturing, no mechanical testing. Best prior art for CALPHAD-in-the-loop autonomy, not for powder→print→test. (liang2025realtimeexperimenttheoryclosedloop pages 1-3) |
| **Nelaturu et al. 2024** (*MSEA*) | Bulk multi-principal-element alloys (Cr–Fe–Mn–Ni) | Directed energy deposition / LENS with **four independently controlled powder hoppers** enabling in situ alloying and composition variation | Composition (EDS), phase (XRD), nano-hardness; with conjoint heat treatment across many samples | Batch active learning / ML-guided composition selection | **>100 compositions synthesized in a week**; no per-sample cycle time reported | Closest published high-throughput **bulk AM alloy discovery** platform. Important precedent for AM-in-the-loop compositional search, but it uses **DED feedstock blending**, not powder production + LPBF + tensile. Characterization is mainly microstructure/hardness, not full tensile qualification. (nelaturu2024multiprincipalelementalloy pages 1-4) |
| **HT-READ** (Vecchio et al. 2021, *Acta Mater.*) | Bulk structural alloys (demonstrated on Inconel 625; general alloy development workflow) | 3D-printed **16-sample ring libraries** + automated sample prep/fixturing + automated XRD/SEM/EDS/EBSD/nanoindentation | Microstructure, phase fraction, grain structure, chemistry, nanoindentation-based mechanical response | Iterative ML-assisted closed loop; new data fed back to model for next design round | **16-sample library** per ring; explicit end-to-end cycle time not reported | Excellent example of **bulk-alloy high-throughput characterization** and data plumbing. However, it is not an autonomous powder-production or AM process-optimization loop; more of a rapid characterization/learning infrastructure that could complement powder→print→test. (vecchio2021highthroughputrapidexperimental pages 19-33, vecchio2021highthroughputrapidexperimental pages 1-4) |
| **Boyce & Uchic 2019** (*MRS Bull.* perspective) | Structural alloys / metallurgy broadly | Perspective on rapid synthesis, automated characterization, robotic handling, additive/subtractive integration, information management | N/A (roadmap article rather than one closed-loop experimental platform) | Conceptual autonomy framework; emphasizes automation + AI + process–structure–property loops | No single throughput number; identifies major bottlenecks and enabling components rather than reporting a campaign | Useful benchmark for reviewers: highlights why alloy SDLs are harder—heterogeneous processing, expensive robotics, in-process monitoring focused on defects rather than direct properties, data-management burdens, and integration challenges. Supports novelty of a true metallurgical closed loop. (boyce2019progresstowardautonomous pages 5-6, boyce2019progresstowardautonomous pages 1-2) |
| **Kavas et al. 2024/2025** (BO-tuned LPBF closed-loop control) | Metal additive manufacturing process control (LPBF; wedge specimens, 316L-like control studies) | LPBF with **in-layer PI controller**; BO used to tune controller parameters online/offline for melt-pool/overheating control | Controller performance, overheating reduction, printed-part microstructure / porosity outcomes | Bayesian optimization for controller autotuning | No compositions/month metric; tuning performed via repetitive layer-wise experimentation; explicit alloy-discovery throughput not reported | Important prior art for **autonomous LPBF control**, but optimization target is **process/controller parameters**, not alloy composition. No powder synthesis and no tensile loop. Closest precedent for the “print” autonomy piece only. (kavas2025insitucontrollerautotuning pages 1-3) |
| **BOFN** (Astudillo & Frazier 2021) | Algorithmic / general multi-stage expensive experiments | Abstract network of functions; applicable to manufacturing and multi-stage pipelines with intermediate observations | Intermediate node outputs and final objective | **Bayesian Optimization of Function Networks**: GP per node + EI on implied posterior over final output | No experimental throughput; algorithm paper reports performance gains of **~5% to several orders of magnitude** over methods using less information, with higher compute cost than standard EI in some benchmarks | Highly relevant methodologically for powder→print→test because it explicitly exploits **intermediate measurements from multi-stage pipelines** rather than treating only the final property as observable. Strong justification for BOFN over standard BO in a staged metallurgical workflow. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 19-21, astudillo2021bayesianoptimizationof pages 6-8) |


*Table: This table compares key autonomous or closed-loop platforms and methods relevant to metallic alloy discovery and metal additive manufacturing. It helps position a powder→print→test platform by showing what parts of the loop have been demonstrated already, and where the main novelty remains.*

### 2) Does prior art include BOTH powder production and additive manufacturing in the same loop?
**No published autonomous alloy-discovery SDL was found in the retrieved literature that includes both (a) powder production (atomization) and (b) additive manufacturing (LPBF/DED) as part of a single, iterative, closed-loop *optimization* over new alloy compositions.**

However, two important partial precedents exist:

1. **Powder↔LPBF closed-loop recycling (powder production + AM coupled physically, but not alloy discovery):**
A study explicitly demonstrates a physical closed-loop cycle for 316L: LPBF rods are produced, then remelted and ultrasonically atomized, sieved, and reused for LPBF (“print → atomize → sieve → reprint”). This is a strong precedent that powder production can be physically integrated with LPBF in a loop, but it is framed as recycling/processability rather than autonomous alloy optimization. (bashmakova2026ontheultrasonic pages 2-5, bashmakova2026ontheultrasonic pages 1-2)

2. **DED alloy discovery via in situ mixing (AM + composition loop, but no powder production):**
The DED active-learning alloy discovery platform achieves >100 compositions/week by metering elemental powders in multiple hoppers, but powders are purchased feedstocks (no in-loop atomization). (nelaturu2024multiprincipalelementalloy pages 1-4)

### 3) Typical cycle time and throughput: metals SDLs vs powder→LPBF→tensile
**Reported cycle times/throughputs vary by 2–4+ orders of magnitude across SDL domains because the bottleneck is usually sample synthesis + characterization.** SDL metrics literature emphasizes that “throughput” must be reported as both theoretical and demonstrated values and must include sample preparation + measurement, because measurement-only rates can greatly exceed end-to-end experimental rates. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3)

Metal-relevant numeric benchmarks in retrieved sources:

- **Thin-film metal SDL (AMASE):** one autonomous run in **just over 8 h** (phase diagram mapping). (liang2025realtimeexperimenttheoryclosedloop pages 1-3)
- **Bulk AM-enabled alloy discovery (DED + active learning):** **25 alloys/4 h**, consistent with **>100 alloys/week**. (nelaturu2024multiprincipalelementalloy pages 16-20, nelaturu2024multiprincipalelementalloy pages 1-4)
- **General SDL demonstrated throughput examples (not metals-specific):** e.g., **30–33 samples/h** demonstrated in one cited platform; microfluidic spectral sampling example: **100 samples/h demonstrated vs 1,200 measurements/h theoretical**, with demonstrated unassisted lifetime **2 days** and assisted lifetime **up to one month**. These are useful reviewer benchmarks but are not directly transferable to a powder→LPBF→tensile pipeline. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3)

**Powder→LPBF→tensile will almost certainly be much slower** than thin-film phase mapping or hardness-based bulk screening, because producing tensile specimens and running tensile tests are inherently slower and often require machining/EDM and careful metrology. No retrieved paper reports an end-to-end cycle time for powder-atomize → LPBF-build → tensile test → model update, so direct quantitative comparison is not possible from this evidence set. (nelaturu2024multiprincipalelementalloy pages 16-20, volk2024performancemetricsto pages 1-2)

### 4) Throughput (compositions/month) achieved for metallic alloys
From the retrieved literature, the clearest “compositions per time” figure for bulk alloys is:

- **DED + active learning bulk alloy discovery:** **>100 compositions/week**, implying **>400 compositions/month** under similar operating assumptions. (nelaturu2024multiprincipalelementalloy pages 1-4)

Thin-film phase mapping is not naturally reported in “compositions/month,” but AMASE’s **8 h** run indicates that phase diagram mapping (a different objective than mechanical property optimization) can proceed at day-scale per autonomous campaign. (liang2025realtimeexperimenttheoryclosedloop pages 1-3)

### 5) Why metal/alloy SDLs are harder than thin-film/solution-phase SDLs
Metals add several compounding difficulties:

- **Process–structure–property coupling and microstructure sensitivity:** Optimal performance depends on processing history and microstructure, not only composition, making iterative experimentation necessary. (boyce2019progresstowardautonomous pages 1-2)
- **Kinetics urgency and real-time evolution during processing:** AMASE explicitly highlights time constraints “due to kinetics” and the challenge of dynamic experiment–theory updates under real-time reaction/phase evolution. (liang2025realtimeexperimenttheoryclosedloop pages 1-3)
- **Thin-film vs bulk divergences:** Thin films can have evaporation and substrate-stress effects that shift phase behavior, complicating translation to bulk alloys. (liang2025realtimeexperimenttheoryclosedloop pages 1-3)
- **In-process metrology limitations:** In AM, in-process monitoring often targets off-nominal conditions/defects rather than direct mechanical properties, making property-driven closed-loop control more difficult. (boyce2019progresstowardautonomous pages 5-6)
- **Robotics/integration barriers for metallurgy:** Safety, reach/payload, positional accuracy, and harsh environments (vacuum/high temperature) complicate automation. Software linking multiple instruments to AI planners is immature; data rates can reach Gb/s, stressing storage/curation. (boyce2019progresstowardautonomous pages 5-6)
- **Motor-function challenges for heterogeneous workflows:** Dispensing/handling solids and translating human protocols to robots is difficult; instrument vendors rarely design for SDL integration. (seifrid2022autonomouschemicalexperiments pages 1-2)

### 6) BOFN vs standard BO for multi-stage pipelines (powder→print→test)
BOFN (Bayesian Optimization of Function Networks) directly matches the structure of a multi-stage metallurgy pipeline.

- **Core idea:** model each pipeline stage (node) with its own GP and incorporate intermediate measurements, rather than modeling only the final objective as in standard BO. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2)
- **Benefit:** intermediate observations improve the implied posterior on the final objective (even though it becomes non-Gaussian), improving query efficiency; reported gains range from ~5% to orders-of-magnitude over methods that use less information. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2)
- **Tradeoff:** EI-FN acquisition evaluation is more computationally expensive than standard EI, with reported per-iteration runtimes often much larger than EI (and sometimes less than KG). (astudillo2021bayesianoptimizationof pages 19-21)

For a powder→LPBF→tensile pipeline, BOFN’s explicit use of intermediate observables (e.g., powder PSD/sphericity/chemistry, printability proxies, porosity from in situ monitoring, hardness/microstructure before tensile) is a principled argument for BOFN over standard BO that only observes final tensile metrics. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2)

### 7) Feasibility of “≥200 compositions in 9 months” for a powder-to-part pipeline
Direct published end-to-end powder→LPBF→tensile cycle times were not found in the retrieved evidence. A feasibility assessment must therefore be made by triangulation from adjacent demonstrated systems:

- A DED in situ alloying + active learning pipeline achieves **>100 alloys/week** (25 alloys in 4 h) using automated XRD/EDS/nano-hardness and batch heat-treatment. (nelaturu2024multiprincipalelementalloy pages 1-4, nelaturu2024multiprincipalelementalloy pages 16-20)
- Ultrasonic atomization (UA) can produce AM-suitable powder fractions at lab scale; for AlSi12 UA, ~**75%** of powder passed a <63 µm sieve criterion for LPBF. (yankin2025effectofultrasonic pages 2-3)

Thus, **≥200 compositions in 9 months (~5–6/week)** is well below the demonstrated synthesis throughput of the DED-based loop (>100/week), suggesting the target could be plausible if the LPBF+tensile portion does not become a severe bottleneck and if batching strategies are used. The key feasibility risks are not “can the loop produce metal samples,” but whether it can do so repeatedly with adequate powder quality and minimal requalification burden.

Critical risks specific to UA→LPBF cycling include:

- **Compositional drift/evaporation:** In a UA recycling study, Mn decreased >3× (0.88 wt% to ~0.27–0.28 wt%), attributed to evaporation during atomization; oxide regions were observed, and oxygen pickup after recycling was noted. Such drift could confound composition–property learning if not measured and corrected. (bashmakova2026ontheultrasonic pages 11-13, bashmakova2026ontheultrasonic pages 1-2)

### 8) Role of ultrasonic atomization in rapid alloy prototyping (vs arc melting/gas atomization)
Within retrieved sources, ultrasonic atomization is positioned as a flexible lab-scale route for AM powder prototyping and for closed-loop powder regeneration:

- **Rapid AM powder fraction production:** For AlSi12, UA produced ~75% of powder meeting a <63 µm size criterion for SLM use, and achieved improved powder “suitability factors” versus commercial powder. (yankin2025effectofultrasonic pages 2-3, yankin2025effectofultrasonic pages 1-2)
- **Morphology improvements:** For 316L recycling, UA increased sphericity from ~0.56 (virgin) to ~0.84–0.90 (UA), with LPBF-appropriate PSD values after sieving (D50 ~31–34 µm). (bashmakova2026ontheultrasonic pages 7-9)
- **Powder-development flexibility:** For refractory Mo–Si–Ti, UA is described as a flexible arc-melting-based approach for alloy-composition development with powder properties meeting PBF needs (qualitative in excerpt). (hinrichs2021flexiblepowderproduction pages 1-2)

A concise quantitative summary is provided here:

| Paper | Material | Purpose (powder development vs recycling) | Key UA conditions (frequency/current/amplitude if mentioned) | Powder size/yield for AM | Morphology/sphericity | Composition/impurities changes | Relevance to closed-loop powder→print |
|---|---|---|---|---|---|---|---|
| Bashmakova et al. 2026 | SS316L rods previously made by PBF-LB | Closed-loop recycling: print rods by LPBF → remelt/UA → sieve → reprint | ATO Lab Plus US35; 35 kHz; current varied ~70–160 A; amplitude 60–80%; process O2 ≤100 ppm; three rods atomized per sample; instability noted above 180 A (bashmakova2026ontheultrasonic pages 2-5, bashmakova2026ontheultrasonic pages 1-2) | Sieved to PBF-LB-suitable fraction; PSD after sieving D10 = 13.5–15.0 µm, D50 = 31.0–34.0 µm, D90 ≈ 49 µm (bashmakova2026ontheultrasonic pages 7-9) | Sphericity improved from 0.56 (virgin) to 0.84–0.90 (UA); fewer satellites/agglomerates; improved flowability; reduced internal porosity (bashmakova2026ontheultrasonic pages 7-9, bashmakova2026ontheultrasonic pages 1-2) | Main alloying elements largely preserved; Mn dropped from 0.88 ± 0.094 wt.% to 0.27–0.28 wt.% (>3× decrease); localized Mn/Si/O-rich oxide regions observed; oxygen increased after recycling (bashmakova2026ontheultrasonic pages 11-13, bashmakova2026ontheultrasonic pages 1-2) | Strongest partial precedent for a physical powder→print loop, but aimed at feedstock regeneration/processability rather than autonomous alloy discovery (bashmakova2026ontheultrasonic pages 2-5, bashmakova2026ontheultrasonic pages 1-2) |
| Yankin et al. 2025 | AlSi12 | AM powder development/qualification | ATO Lab + US35; ~35 kHz; current ~140–150 A tested; amplitude ~75–80%; arc angle −5° to 5°; 63 µm sieve for Renishaw AM400 use (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 2-3) | ~75% of produced powder passed <63 µm sieve for SLM; literature cited minimum particle diameters ~15 µm; ATOLab+-derived powders reported elsewhere to enable LPBF parts of 99.2% density (yankin2025effectofultrasonic pages 2-3) | UA powder had suitability factors 21% higher than commercial powder, with improved sphericity; PSD span varied up to 37.5% with parameters (yankin2025effectofultrasonic pages 1-2) | Oxidation noted as a challenge for continuous Al UA because fast droplet oxidation and low density require high amplitudes; no explicit bulk evaporation numbers in excerpt (yankin2025effectofultrasonic pages 1-2) | Shows UA can rapidly produce AM-suitable powder fractions at lab scale, but no integrated print→test optimization loop is reported (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 2-3) |
| Hinrichs et al. 2021 | Mo-20Si-52.8Ti (at.%) refractory alloy | Flexible lab-scale powder development for PBF AM; EIGA explored as upscale route | UA is arc-melting-based with plasma arc between W electrode and water-cooled crucible on vibrating sonotrode; inert gas carries detached droplets; quantitative frequency/current/amplitude not given in excerpt (hinrichs2021flexiblepowderproduction pages 1-2) | Quantitative PSD/yield not given in excerpt; authors state UA powder properties, quality, and quantities “perfectly meet the requests for alloy development for powder bed fusion AM” (hinrichs2021flexiblepowderproduction pages 1-2) | Compared against EIGA for size distribution, sphericity, microstructure, phase constitution, chemistry, and interstitials; multiple UA batches produced to assess stability/reliability, but no numeric sphericity in excerpt (hinrichs2021flexiblepowderproduction pages 1-2) | Refractory-alloy challenges emphasized: liquidus >2000 °C, brittle intermetallics, sensitivity to interstitials; no explicit impurity-change numbers in excerpt (hinrichs2021flexiblepowderproduction pages 1-2) | Important evidence that UA is viewed as a flexible rapid alloy-powder prototyping route for PBF, but not yet integrated into an autonomous powder→print→test closed loop (hinrichs2021flexiblepowderproduction pages 1-2) |


*Table: This table compiles the most relevant quantitative and qualitative evidence on ultrasonic atomization for additive-manufacturing powder development and recycling. It is useful for positioning a powder→print platform by distinguishing existing feedstock-regeneration and rapid-powder-prototyping precedents from a fully autonomous alloy-discovery loop.*

### 9) Published examples of autonomous LPBF alloy optimization
In the retrieved evidence, autonomy in LPBF is primarily focused on **process optimization/control** rather than alloy composition optimization:

- **BO for in-layer controller autotuning:** online convergence by iteration **74** and offline by **112**, optimizing PI gains and a sensor-based cost function; highlights the feasibility of closed-loop “autotuning” but also the risk of quality tradeoffs (lack-of-fusion if control reduces power too aggressively). (kavas2025insitucontrollerautotuning pages 26-29)
- **Physics-guided/digital-twin approaches:** layerwise or hatch-level parameter changes to control thermal history, porosity, or residual stress are discussed as emerging autonomous methods, but without composition search. (riensche2025rapidautonomousand pages 6-6, riensche2025rapidautonomousand pages 2-3)

No retrieved paper demonstrates a fully autonomous LPBF loop that optimizes alloy composition with tensile testing as the objective.

### 10) Reviewer-relevant SDL evaluation metrics for a metals SDL proposal
A widely cited SDL performance-metrics perspective recommends that SDL proposals/reports quantify and clearly distinguish:

- **Degree of autonomy** (piecewise, semi-closed-loop, closed-loop, self-motivated). (volk2024performancemetricsto pages 2-3)
- **Operational lifetime** (demonstrated/theoretical × assisted/unassisted), because lifetime constrains cumulative throughput. (volk2024performancemetricsto pages 1-2)
- **Throughput** (demonstrated vs theoretical), including sample preparation and measurement; avoid conflating measurement-only speed with end-to-end experiment speed. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3)
- **Precision/reproducibility** measured by unbiased replicates. (volk2024performancemetricsto pages 1-2)
- **Material usage/cost per experiment** (including cleaning and hazardous/high-value materials). (volk2024performancemetricsto pages 1-2)
- **Accessible parameter space** (demonstrated vs theoretical bounds). (volk2024performancemetricsto pages 2-3)
- **Optimization efficiency** (experiments-to-target), including algorithm benchmarking vs random and other optimizers. (volk2024performancemetricsto pages 2-3)

These are captured visually in extracted figures/tables from the metrics paper. (volk2024performancemetricsto media e35da528, volk2024performancemetricsto media c062d7c6)

### Competitive positioning and novelty of a closed-loop powder→print→test platform
Relative to the above state-of-the-art, a **CALPHAD → atomize powder → LPBF print → tensile test → BOFN optimization** platform would be positioned as:

- **Novel integration across manufacturing stages:** Retrieved prior art typically optimizes (a) thin-film phase mapping (fast) (liang2025realtimeexperimenttheoryclosedloop pages 1-3), (b) bulk alloy composition via DED + hardness/XRD/EDS loops without powder production (nelaturu2024multiprincipalelementalloy pages 1-4), or (c) LPBF process parameters/controller tuning without composition optimization (kavas2025insitucontrollerautotuning pages 26-29). A unified powder-production + LPBF + mechanical property loop for new alloys appears not yet demonstrated in the retrieved literature.

- **Feasibility depends on managing metal-specific bottlenecks:** the major technical feasibility challenges are consistent with published barriers: automation/integration difficulty in harsh metallurgical environments, data-management scale, and metrology aligned to properties rather than defects. (boyce2019progresstowardautonomous pages 5-6, seifrid2022autonomouschemicalexperiments pages 1-2)

- **BOFN is a defensible choice for staged pipelines:** because it exploits intermediate outputs, matching powder→print→test structure better than “final-output-only” BO, and is shown to outperform methods that ignore intermediate node data. (astudillo2021bayesianoptimizationof pages 2-4, astudillo2021bayesianoptimizationof pages 1-2)

- **UA is a plausible enabler, but must be instrumented for drift:** UA can produce AM-suitable powder fractions and improve sphericity, but recycling cycles show element loss (Mn) and oxide/oxygen pickup risks that must be measured/controlled to prevent confounded learning. (yankin2025effectofultrasonic pages 2-3, bashmakova2026ontheultrasonic pages 7-9, bashmakova2026ontheultrasonic pages 11-13)

Overall, the competitive advantage is best framed as **closing the loop at the “manufacturing-grade bulk property” level**, where state-of-the-art either stops at thin-film thermodynamics, bulk hardness proxies, or AM process parameters; the principal feasibility challenge is achieving robust, repeatable, property-relevant characterization and powder/print quality control at a throughput compatible with iterative learning.



References

1. (liang2025realtimeexperimenttheoryclosedloop pages 1-3): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 19 citations and is from a highest quality peer-reviewed journal.

2. (nelaturu2024multiprincipalelementalloy pages 1-4): Phalgun Nelaturu, Jason R. Hattrick-Simpers, Michael Moorehead, Vrishank Jambur, Izabela Szlufarska, Adrien Couet, and Dan J. Thoma. Multi-principal element alloy discovery using directed energy deposition and machine learning. Materials Science and Engineering: A, 891:145945, Jan 2024. URL: https://doi.org/10.1016/j.msea.2023.145945, doi:10.1016/j.msea.2023.145945. This article has 37 citations.

3. (nelaturu2024multiprincipalelementalloy pages 16-20): Phalgun Nelaturu, Jason R. Hattrick-Simpers, Michael Moorehead, Vrishank Jambur, Izabela Szlufarska, Adrien Couet, and Dan J. Thoma. Multi-principal element alloy discovery using directed energy deposition and machine learning. Materials Science and Engineering: A, 891:145945, Jan 2024. URL: https://doi.org/10.1016/j.msea.2023.145945, doi:10.1016/j.msea.2023.145945. This article has 37 citations.

4. (vecchio2021highthroughputrapidexperimental pages 19-33): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.

5. (vecchio2021highthroughputrapidexperimental pages 1-4): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.

6. (kavas2025insitucontrollerautotuning pages 26-29): Baris Kavas, Efe C. Balta, Michael Tucker, Raamadaas Krishnadas, Alisa Rupenyan, John Lygeros, and Markus Bambach. In-situ controller autotuning by bayesian optimization for closed-loop feedback control of laser powder bed fusion process. ArXiv, Jun 2025. URL: https://doi.org/10.48550/arxiv.2406.19096, doi:10.48550/arxiv.2406.19096. This article has 18 citations.

7. (kavas2025insitucontrollerautotuning pages 1-3): Baris Kavas, Efe C. Balta, Michael Tucker, Raamadaas Krishnadas, Alisa Rupenyan, John Lygeros, and Markus Bambach. In-situ controller autotuning by bayesian optimization for closed-loop feedback control of laser powder bed fusion process. ArXiv, Jun 2025. URL: https://doi.org/10.48550/arxiv.2406.19096, doi:10.48550/arxiv.2406.19096. This article has 18 citations.

8. (boyce2019progresstowardautonomous pages 5-6): Brad L. Boyce and Michael D. Uchic. Progress toward autonomous experimental systems for alloy development. MRS Bulletin, 44:273-280, Apr 2019. URL: https://doi.org/10.1557/mrs.2019.75, doi:10.1557/mrs.2019.75. This article has 56 citations and is from a domain leading peer-reviewed journal.

9. (boyce2019progresstowardautonomous pages 1-2): Brad L. Boyce and Michael D. Uchic. Progress toward autonomous experimental systems for alloy development. MRS Bulletin, 44:273-280, Apr 2019. URL: https://doi.org/10.1557/mrs.2019.75, doi:10.1557/mrs.2019.75. This article has 56 citations and is from a domain leading peer-reviewed journal.

10. (astudillo2021bayesianoptimizationof pages 2-4): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

11. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

12. (astudillo2021bayesianoptimizationof pages 19-21): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

13. (astudillo2021bayesianoptimizationof pages 6-8): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

14. (bashmakova2026ontheultrasonic pages 2-5): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

15. (bashmakova2026ontheultrasonic pages 1-2): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

16. (volk2024performancemetricsto pages 1-2): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 80 citations and is from a highest quality peer-reviewed journal.

17. (volk2024performancemetricsto pages 2-3): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 80 citations and is from a highest quality peer-reviewed journal.

18. (seifrid2022autonomouschemicalexperiments pages 1-2): Martin Seifrid, Robert Pollice, Andrés Aguilar-Granda, Zamyla Morgan Chan, Kazuhiro Hotta, Cher Tian Ser, Jenya Vestfrid, Tony C. Wu, and Alán Aspuru-Guzik. Autonomous chemical experiments: challenges and perspectives on establishing a self-driving lab. Accounts of Chemical Research, 55:2454-2466, Aug 2022. URL: https://doi.org/10.1021/acs.accounts.2c00220, doi:10.1021/acs.accounts.2c00220. This article has 309 citations and is from a domain leading peer-reviewed journal.

19. (yankin2025effectofultrasonic pages 2-3): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

20. (bashmakova2026ontheultrasonic pages 11-13): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

21. (yankin2025effectofultrasonic pages 1-2): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

22. (bashmakova2026ontheultrasonic pages 7-9): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

23. (hinrichs2021flexiblepowderproduction pages 1-2): Frauke Hinrichs, Alexander Kauffmann, Daniel Schliephake, Sascha Seils, Susanne Obert, Karin Ratschbacher, Melissa Allen, Astrid Pundt, and Martin Heilmaier. Flexible powder production for additive manufacturing of refractory metal-based alloys. Metals, 11:1723, Oct 2021. URL: https://doi.org/10.3390/met11111723, doi:10.3390/met11111723. This article has 23 citations.

24. (riensche2025rapidautonomousand pages 6-6): Alex Riensche, Kaustubh Deshmukh, Antonio Carrington, Mihir Darji, Benjamin Bevans, Kyle Snyder, John Sions, Yuri Plotnikov, Kevin D. Cole, and Prahalada Rao. Rapid, autonomous, and shape-agnostic physics-guided thermal history control to improve part quality in laser powder bed fusion additive manufacturing. Journal of Manufacturing Science and Engineering, Jun 2025. URL: https://doi.org/10.1115/1.4068695, doi:10.1115/1.4068695. This article has 3 citations.

25. (riensche2025rapidautonomousand pages 2-3): Alex Riensche, Kaustubh Deshmukh, Antonio Carrington, Mihir Darji, Benjamin Bevans, Kyle Snyder, John Sions, Yuri Plotnikov, Kevin D. Cole, and Prahalada Rao. Rapid, autonomous, and shape-agnostic physics-guided thermal history control to improve part quality in laser powder bed fusion additive manufacturing. Journal of Manufacturing Science and Engineering, Jun 2025. URL: https://doi.org/10.1115/1.4068695, doi:10.1115/1.4068695. This article has 3 citations.

26. (volk2024performancemetricsto media e35da528): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 80 citations and is from a highest quality peer-reviewed journal.

27. (volk2024performancemetricsto media c062d7c6): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 80 citations and is from a highest quality peer-reviewed journal.