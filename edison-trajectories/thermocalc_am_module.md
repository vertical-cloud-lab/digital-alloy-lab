# Thermo-Calc Additive Manufacturing Module

*Edison Scientific LITERATURE_HIGH query*

Question: How has Thermo-Calc's Additive Manufacturing (AM) Module been used in published research? Specifically cover:
(1) Research papers (2020-2026) that used the Thermo-Calc AM Module for melt pool simulation, printability maps, or process parameter optimization in powder bed fusion (LPBF/PBF-LB or PBF-EB)
(2) Integration with other Thermo-Calc capabilities (CALPHAD equilibrium, Scheil solidification, DICTRA diffusion, TC-PRISMA precipitation) in additive manufacturing workflows
(3) Alloy systems studied using the Thermo-Calc AM Module (steels, Ni-based superalloys, Al alloys, Ti alloys, high-entropy alloys, refractory alloys)
(4) Comparison with alternative approaches for AM process simulation (Ansys Additive, FLOW-3D AM, open-source tools, analytical Rosenthal/Eagar-Tsai models)
(5) Validated capabilities and known limitations for predicting melt pool geometry, thermal gradients, solidification rates, columnar-to-equiaxed transitions, printability windows, and defect formation (keyholing, lack of fusion, balling)
(6) Combination with machine learning, Bayesian optimization, or high-throughput computational screening for alloy design for additive manufacturing

# Thermo-Calc's Additive Manufacturing (AM) Module in Published Research: A Comprehensive Review

## Module Overview and Capabilities

The Thermo-Calc AM Module, introduced in version 2023b and substantially updated through 2024b–2025b, is designed for modeling the powder bed fusion (PBF) process with either Laser Beam (PBF-LB) or Electron Beam (PBF-EB) heat sources. Its defining feature is the unified treatment of alloy-dependent material properties (specific heat, density, thermal conductivity, viscosity, surface tension) calculated automatically from CALPHAD thermodynamic databases via the extended Scheil calculator, enabling simulation of *any* alloy without requiring experimental thermophysical property measurements.

### Key Capabilities

| Capability | Description | Introduced |
| :--- | :--- | :--- |
| **Steady-State Simulation** | Stationary melt pool for given process parameters; outputs melt pool size, peak temperature, fluid flow velocity, thermal gradients, solidification rates | 2023b |
| **Transient Simulation** | Time-dependent single- or multi-layer builds; temperature vs. time at selected positions | 2023b |
| **Transient with Heat Source from Steady-State** | Efficiency-accuracy hybrid for multi-layer builds | 2023b |
| **Printability Maps** | Power-speed maps showing keyholing, lack of fusion, and balling defect regions | 2024b |
| **Batch and Grid Calculations** | Efficient parameter sweeps; parity plots comparing to experimental data | 2024b |
| **Keyhole Model with Fluid Flow** | Improved melt pool accuracy in keyholing regime | 2024b |
| **CET Overlay** | Thermal gradient/solidification rate overlay on Columnar-to-Equiaxed Transition plots | 2024b |
| **DICTRA Coupling** | Probe data from AM calculations as input for diffusion simulations | 2023b |
| **TC-PRISMA Coupling** | Pre-processed thermodynamic/kinetic data for precipitation during AM thermal cycles | 2023b |
| **TC-Python API** | Programmatic access to AM Module for automation and high-throughput workflows | 2023b |
| **Exodus Export** | FEA-compatible file format for external post-processing | 2023b |

### Compatible Databases

The AM Module requires databases with surface tension, viscosity, thermal conductivity, molar volume, and gas descriptions. Currently compatible databases include:

- TCFE13+ (steel and Fe-alloys)
- TCNI12+ (Ni-based superalloys)
- TCAl9+ (Al-based alloys)
- TCTI5+ (Ti and TiAl-based alloys)
- TCHEA6+ (high-entropy alloys)
- TCMG6+ (Mg-based alloys)
- TCCU6+ (Cu-based alloys)
- TCNOBL3+ (noble metal alloys)
- TCSLD5+ (solder alloys)
- TCMO1+ (Mo-based alloys)
- TCNB1+ (Nb-based alloys)
- TCPMAG3+ (permanent magnetic materials)

## 1. Research Papers Using the Thermo-Calc AM Module

The Thermo-Calc AM Module provides a CALPHAD-integrated thermal process model capable of simulating melt pool geometry, mushy zone characteristics, and melting mode transitions during powder bed fusion additive manufacturing. Several key studies have explicitly utilized the dedicated module:

**Hussain (2024, Chalmers University of Technology)** used the Thermo-Calc 2024a AM Module to simulate the PBF-LB process for the non-weldable Ni-base superalloy CM247LC. The work employed the TCNI12 thermodynamic database for Scheil solidification calculations, with a calibrated Gaussian heat source featuring 70% absorptivity and an approximately 80 µm beam diameter. Both steady-state (single-track) and transient (multi-track) calculations were performed to assess the effect of process parameters and stripe width on melt pool depth, mushy zone extent, and solidification cracking. The results showed that low line energy density (0.1 J/mm) and low hatch spacing (0.03 mm) produced shallower melt pools and minimized solidification cracking, while the mushy zone and re-melting behavior under narrow stripe widths (0.2 mm) influenced solute redistribution and residual stresses (hussain2024powderbedfusion–laser pages 7-12, hussain2024powderbedfusion–laser pages 25-33, hussain2024powderbedfusion–laser pages 33-38).

**Hosseini et al. (2025)** used Thermo-Calc's AM Module (version 2024b) with the TCAl9 database to evaluate melting modes in L-PBF of Al6061. The steady-state simulation with a calibrated Gaussian heat source predicted melt pool depths for each set of process parameters. At low energy densities (25.51–44.64 J/mm³), shallow melt pools characteristic of lack-of-fusion were predicted, while at high energy densities (69.44–104.16 J/mm³), deeper melt pools prone to keyhole porosity were identified. Within the optimized window (44.64–50 J/mm³), melt pool dimensions promoted complete fusion and a stable melting mode correlating with 99% relative density, consistent with SEM observations (hosseini2025effectoflaser pages 3-5).

**Vaddamanu (2025, Chalmers University of Technology)** documented use of the Thermo-Calc AM Module for studying PBF-LB processing of a low-alloy engineering steel (SSAB AM Engineering) and a lean hot work tool steel (Osprey HWTS50). The work investigated process optimization at different layer thicknesses (30–90 µm) and linked AM Module melt pool predictions to microstructural outcomes, including the transition from columnar to more equiaxed prior austenite grains at higher layer thicknesses (vaddamanu2025thesisforthe pages 7-13, vaddamanu2025thesisforthe pages 34-39).

Beyond the dedicated AM Module, the broader Thermo-Calc software ecosystem has been extensively used to construct printability maps. **Sheikh et al. (2024, Texas A&M University)** developed an automated computational framework using Thermo-Calc's Property and Equilibrium modules to derive thermophysical properties (thermal conductivity, diffusivity, density, liquidus temperature, specific heat capacity, boiling temperature, and electrical resistivity) that were fed into Eagar-Tsai and Gladush-Smurov analytical melt pool models. These were used to construct printability maps evaluating lack-of-fusion, balling, and keyholing criteria across processing parameter space (sheikh2024anautomatedcomputational pages 14-15). **Sheikh et al. (2025, Texas A&M)** extended this to the Co-Cr-Fe-Mn-Ni high-entropy alloy design space using CALPHAD databases TCHEA5, TCAL7, and TCNI11, incorporating three thermal models and a deep learning surrogate to screen printable alloy compositions (sheikh2025highthroughputalloyand pages 5-7, sheikh2025highthroughputalloyand pages 7-10).

### Summary of Key Studies

| Reference | Thermo-Calc Module(s) | Alloy System | AM Process | Key Finding | Institution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Hussain (2024) | AM Module; Scheil (TCNI12) | CM247LC Ni superalloy | PBF-LB | Calibrated heat source (70% absorptivity, ~80 µm beam); steady-state + transient simulations linked melt pool shape and mushy zone to solidification cracking and residual stress | Chalmers University |
| Hosseini et al. (2025) | AM Module (TCAl9) | Al6061 | L-PBF | Mapped lack-of-fusion, stable, and keyhole regimes; optimal window (44.64–50 J/mm³) yielded 99% density | — |
| Vaddamanu (2025) | AM Module | Low-alloy steel; hot-work tool steel | PBF-LB | Linked layer thickness (30–90 µm) to columnar/equiaxed grain transition | Chalmers University |
| Sheikh et al. (2024) | Property/Equilibrium Modules | General metallic alloys | LPBF printability | Automated printability maps via Eagar-Tsai + Gladush-Smurov models with TC-derived properties | Texas A&M |
| Sheikh et al. (2025) | CALPHAD (TCHEA5/TCAL7/TCNI11) | Co-Cr-Fe-Mn-Ni HEAs | LPBF screening | Deep learning surrogate ~1000× speedup; probabilistic printability maps across HEA space | Texas A&M |
| Sjöström et al. (2022) | DICTRA; thermodynamic DBs | 18Ni300 maraging steel | LPBF | Linked Simufact Additive thermal histories to DICTRA for microsegregation and Ms prediction | Thermo-Calc AB |
| Sargent et al. (2021) | DICTRA; Scheil; TC-Python | Al-Cu; SS316L | LPBF | Integrated process model + DICTRA; showed significant back-diffusion deviations from Scheil for SS316L | UC Davis / U. Pittsburgh |
| Chou et al. (2022) | TC-PRISMA | AISI 441 ferritic SS | L-PBF | NbC and Laves precipitate kinetics during post-heat treatment; calibrated against SEM/TEM | Uppsala University |
| Hariharan et al. (2022) | ICME framework; TC-PRISMA | Haynes 282 Ni superalloy | LPBF | ICME framework for microsegregation/precipitation during LPBF | IIT Madras |
| Franco-Correa et al. (2023) | Scheil-Gulliver; CALPHAD | IN718 | PBF-AM | AM-tailored TTT diagram; shifted γ″/δ precipitation vs. conventional processing | CIATEQ (Mexico) |
| Assi et al. (2022) | CALPHAD + ML + genetic algorithm | Austenitic stainless steel | LPBF | Designed novel printable austenitic alloy; experimentally validated against 316L | IMT Nord Europe |
| Motaman et al. (2020) | CALPHAD + DFT | Fe-Mn-Al-C steel | Metal AM | ICME workflow for alloy selection and thermophysical property prediction for AM | RWTH Aachen |
| Das et al. (2023) | Scheil; CALPHAD | Multi-principal element alloy | Laser beam AM | Scheil + CFD melt-pool modeling for phase fractions, geometry, hatch/layer optimization | Missouri S&T |

## 2. Integration with Other Thermo-Calc Capabilities in AM Workflows

A defining advantage of the Thermo-Calc ecosystem is the ability to chain multiple computational modules into integrated computational materials engineering (ICME) workflows for additive manufacturing.

### CALPHAD Equilibrium + Scheil Solidification

Nearly all identified studies employed Thermo-Calc equilibrium and Scheil-Gulliver solidification calculations as foundational tools. Franco-Correa et al. (2023, CIATEQ, Mexico) used Thermo-Calc with the TCNI8/MOBNI4 databases to analyze phase behavior and construct a tailored TTT diagram specific to PBF-manufactured IN718, revealing that γ″ and δ precipitation occurs at lower temperatures and shorter times in AM parts compared to conventional processing (francocorrea2023tailoredtime–temperaturetransformation pages 2-4). Scaglione et al. (2022, Università di Torino) used Thermo-Calc for both equilibrium and Scheil solidification calculations for Au-based precious alloys and Al-Mg-Si-Er quaternary alloys, including construction of custom CALPHAD databases (scaglione2022solidificationcalculationsof pages 2-4).

### DICTRA Diffusion Simulations

Sjöström et al. (2022, Thermo-Calc Software AB) demonstrated a macro-to-micro modeling linkage for 18Ni300 maraging steel, where thermal histories from Simufact Additive (macroscale FEA) were imported into the DICTRA diffusion module to simulate elemental microsegregation and predict martensite start temperatures at different locations within the build. Higher laser energy caused greater elemental segregation and lower local Ms temperatures, enabling baseplate temperature optimization (sjostrom2022linkageofmacro pages 3-4). Sargent et al. (2021, UC Davis/Pittsburgh) integrated a semi-analytic LPBF process model with DICTRA via TC-Python to model non-equilibrium solidification and solidification cracking susceptibility in Al-Cu alloys and SS316L (sargent2021integrationofprocessing pages 10-11). In related later work, Sargent et al. (2024) reported that DICTRA predictions showed significant deviations from Scheil-Gulliver for SS316L due to strong back-diffusion effects at AM cooling rates (sargent2024integratedcomputationaland pages 49-54).

### TC-PRISMA Precipitation Modeling

Chou et al. (2022, Uppsala University/Thermo-Calc) used TC-PRISMA to model precipitation kinetics during post-heat treatment of L-PBF-produced AISI 441 ferritic stainless steel. The Langer-Schwartz-Kampmann-Wagner numerical approach simulated simultaneous nucleation, growth, and coarsening of NbC and Laves (Fe₂Nb) precipitates. The calibrated model reproduced experimental trends in mean precipitate radii and phase amounts versus temperature, serving as a tool for optimizing post-build heat treatments (chou2022precipitationkineticsduring pages 1-2).

### Coupled AM Module → DICTRA/TC-PRISMA Workflow

The Thermo-Calc AM Module allows users to predict the microstructure of an alloy by coupling with DICTRA and TC-PRISMA. Probe data (time-temperature histories at selected positions) generated from an AM calculation can be used as input for diffusion and precipitation calculations. Thermal gradient and solidification rates from the AM Module can be overlaid on CET plots from the General Model Library, allowing evaluation of columnar vs. equiaxed solidification without data export/import.

## 3. Alloy Systems Studied

The Thermo-Calc AM Module and broader CALPHAD ecosystem have been applied to a diverse range of alloy systems:

- **Nickel-based superalloys:** CM247LC (Hussain 2024), Haynes 282 (Hariharan et al. 2022), IN718 (Franco-Correa et al. 2023), IN738LC (Nomoto et al. 2021)
- **Steels:** 18Ni300 maraging steel (Sjöström et al. 2022), SS316L (Sargent et al. 2021), AISI 441 ferritic stainless (Chou et al. 2022), low-alloy engineering steels (Vaddamanu 2025), Fe-Mn-Al-C TWIP/TRIP steels (Motaman et al. 2020), austenitic stainless (Assi et al. 2022)
- **Aluminum alloys:** Al6061 (Hosseini et al. 2025), Al-Cu alloys (Sargent et al. 2021), Al-Mg-Si-Er (Scaglione et al. 2022), Al 7xxx series (Uba et al. 2025)
- **High-entropy alloys:** Co-Cr-Fe-Mn-Ni Cantor-derived HEAs (Sheikh et al. 2025), AlCrFe₂Ni₂ (Mooraj et al. 2024), FeCoCrNi (Hou et al. 2021)
- **Refractory alloys:** W-Re and W-Re-Ta systems (Michael & Sowards 2023)
- **Ti-based alloys:** Ti₀.₄Zr₀.₄Nb₀.₁Ta₀.₁ and Ti₀.₄₈₆V₀.₃₇₅Cr₀.₁₁₁Ta₀.₀₂₈ refractory complex concentrated alloys (Jobes et al. 2025)
- **Shape memory alloys:** NiTiHf alloys (Dabbaghi et al. 2024) (dabbaghi2024lpbfprocessabilityof pages 5-7)
- **Precious alloys:** Au-based alloys (Scaglione et al. 2022)

## 4. Comparison with Alternative Simulation Approaches

The Thermo-Calc AM Module occupies a unique niche between high-fidelity CFD tools and simple analytical models:

| Tool/Approach | Type | Key Capabilities | Limitations | Speed | Typical Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thermo-Calc AM Module** | CALPHAD-integrated thermal FE model | Melt pool geometry, mushy zone, melting mode; alloy-agnostic via CALPHAD databases; steady-state and transient modes | Simplified fluid dynamics; no Marangoni convection or recoil pressure modeling | Fast to moderate | Parameter sweeps, alloy screening, process optimization |
| **Eagar-Tsai Model** | Analytical quasi-steady-state | Temperature fields, melt pool dimensions; very fast | No temperature-dependent properties, latent heat, evaporation, or fluid flow; underestimates depth in keyhole regimes | Very fast | Rapid screening, printability mapping |
| **Gladush-Smurov** | Analytical keyhole correction | Improved depth prediction in keyholing vs. Eagar-Tsai | Still neglects fluid dynamics and recoil pressure | Very fast | Correcting analytical models for keyhole risk |
| **Full CFD (FLOW-3D AM)** | High-fidelity CFD | Melt pool flow, Marangoni convection, vapor recoil, keyhole dynamics, free-surface physics | Very computationally expensive; impractical for broad sweeps | Slow, high cost | Single-track mechanism studies |
| **Part-scale FEA (Ansys Additive, Simufact)** | Part-scale thermal/mechanical FEA | Thermal histories, residual stress, distortion | Coarse melt-pool resolution; requires calibration | Moderate to high | Build qualification, distortion studies |
| **ML Surrogates** | Data-driven | ~1000× acceleration after training; probabilistic printability maps | Limited to training domain; generalization concerns | Extremely fast | High-throughput alloy/process screening |

The principal advantage of the Thermo-Calc approach is its seamless access to CALPHAD thermodynamic databases, enabling alloy-agnostic predictions across arbitrary compositions without requiring experimental thermophysical property measurements. This makes it uniquely suited for high-throughput alloy screening (sheikh2024anautomatedcomputational pages 14-15, sheikh2025highthroughputalloyand pages 5-7).

## 5. Validated Capabilities and Known Limitations

### Validated Capabilities

- **Melt pool geometry:** Hosseini et al. (2025) demonstrated that AM Module predictions correctly identified transitions between lack-of-fusion, stable melting, and keyhole modes in L-PBF of Al6061, with optimal energy density yielding 99% density.
- **Mushy zone and cracking:** Hussain (2024) showed AM Module predictions of melt pool depth and mushy zone were consistent with experimentally observed solidification cracking patterns in CM247LC, with ~28% melt pool depth decrease at reduced stripe width.
- **Solidification cracking susceptibility:** Sargent et al. (2021) validated DICTRA-predicted cracking susceptibility trends against experimental measurements in Al-Cu alloys.
- **Precipitation kinetics:** Chou et al. (2022) demonstrated TC-PRISMA-calibrated precipitation models reproduced experimental precipitate size and phase fraction trends in L-PBF ferritic stainless steel.

### Known Limitations

1. **Fluid dynamics:** The AM Module does not capture Marangoni convection, vapor recoil pressure, or keyhole instabilities, which strongly influence melt pool shape in keyholing regimes (sheikh2025highthroughputalloyand pages 7-10).
2. **Temperature-dependent properties:** Analytical models typically evaluate material properties at fixed temperatures, introducing errors under conditions with significant thermal variation (sheikh2024anautomatedcomputational pages 14-15).
3. **DICTRA convergence:** Coupling process thermal models to DICTRA for non-equilibrium solidification can encounter numerical convergence issues, limiting throughput in high-throughput workflows (sargent2021integrationofprocessing pages 10-11).
4. **Balling prediction:** Purely analytical approaches cannot reliably detect balling defects, which require consideration of surface tension, wetting, and melt pool stability (sheikh2025highthroughputalloyand pages 3-5).
5. **Scheil approximations:** Standard Scheil-Gulliver assumes local equilibrium at the interface and zero back-diffusion in solid, which may be inaccurate at extreme LPBF cooling rates (10⁴–10⁶ K/s) (nomoto2021nonandquasiequilibrium pages 1-2). Thermo-Calc introduced modified Scheil models with solute trapping in the 2023a extended Scheil calculator to partially address this.

## 6. Combination with Machine Learning and High-Throughput Screening

The integration of Thermo-Calc CALPHAD capabilities with machine learning represents a rapidly growing research direction:

**Sheikh et al. (2025, Texas A&M)** developed a deep learning surrogate trained on CALPHAD-derived thermophysical properties and melt pool model outputs that accelerated printability assessment by ~1000× without significant accuracy loss. This enabled ensemble probabilistic printability maps across the Co-Cr-Fe-Mn-Ni HEA composition space. The framework pre-screened compositions for single-phase FCC stability at 1300°C using the TCHEA5 database before proceeding to printability evaluation (sheikh2025highthroughputalloyand pages 5-7).

**Assi et al. (2022, IMT Nord Europe)** combined machine learning, CALPHAD via Thermo-Calc, physical models, and multi-objective genetic algorithm to design a novel austenitic stainless steel specifically for LPBF, examining solidification range, phase stability, and thermal properties (assi2022alloysdesignfor pages 213-216).

**Li et al. (2021)** proposed combining CALPHAD-generated thermodynamic data from Thermo-Calc with machine learning (ANNs and unsupervised learning) to enable high-throughput microstructure simulation across multi-component alloy spaces. The approach replaced direct in-situ CALPHAD calls to dramatically reduce computational cost (li2021towardshighthroughputmicrostructure pages 1-3).

**Pak et al. (2025, CMU)** developed an agentic AI workflow (LLM-orchestrated) that automates early-stage LPBF alloy evaluation. The system uses Thermo-Calc for CALPHAD-based property prediction, an analytical melt pool model for physics-informed process simulation, and automated generation of lack-of-fusion process maps. The LLM agent parses user prompts, prepares input files, selects databases, and communicates with Thermo-Calc to retrieve critical material properties (arxiv:2510.02567).

**Pei et al. (2026)** coupled CALPHAD thermodynamic calculations (including Thermo-Calc) with seven ML algorithms to predict liquidus, solidus, γ′ solvus, and γ′ volume fraction across 388,000 Ni-based superalloy candidate compositions, enabling multi-objective optimization that was experimentally validated (pei2026acceleratedoptimizationof pages 2-4).

## Fit Assessment for VCL

### Relevance to VCL Pipeline

The Thermo-Calc AM Module aligns with several stages of the VCL alloy discovery pipeline:

| VCL Pipeline Stage | AM Module Relevance | Integration Pathway |
| :--- | :--- | :--- |
| **Alloy Screening** | CALPHAD equilibrium + Scheil for phase stability and solidification behavior screening | TC-Python API for automated composition sweeps |
| **Process Optimization** | Printability maps (keyholing, lack of fusion, balling) for initial LPBF parameter selection | AM Module steady-state calculations per alloy |
| **Melt Pool Prediction** | Melt pool geometry, thermal gradients, solidification rates for process-structure linkage | Steady-state and transient calculations |
| **Microstructure Prediction** | CET overlay, DICTRA microsegregation, TC-PRISMA precipitation | Coupled AM → DICTRA → TC-PRISMA workflow |
| **Post-Processing Optimization** | Precipitation kinetics during heat treatment | TC-PRISMA with AM probe data |
| **ML Integration** | TC-Python API enables training ML surrogates on CALPHAD outputs for 1000× acceleration | Python ecosystem compatibility |

### Advantages for VCL

1. **Alloy-agnostic:** Can simulate any alloy in compatible databases (TCFE13+, TCNI12+, TCAl9+, TCHEA6+), critical for VCL's novel composition exploration
2. **TC-Python API:** Enables integration into autonomous BO/active learning loops via Python scripting
3. **Integrated ecosystem:** Single platform for equilibrium → Scheil → melt pool → microsegregation → precipitation predictions
4. **Printability maps:** Direct output of process windows, reducing trial-and-error LPBF parameter development
5. **Database compatibility:** TCHEA6+ for HEAs and TCAl9+ for Al alloys directly relevant to VCL target systems

### Limitations and Considerations

1. **Cost:** Academic license for Thermo-Calc base + AM Module + databases typically several thousand dollars/year (EAGER budget allocated ~$20K/2yr for Thermo-Calc)
2. **Fluid dynamics gap:** No Marangoni convection or recoil pressure modeling; keyhole predictions less accurate than full CFD
3. **Complementary tools needed:** Part-scale distortion/residual stress requires separate FEA (Ansys/Simufact); detailed melt pool fluid dynamics requires CFD (FLOW-3D AM)
4. **Database coverage:** AM-compatible databases require specific property data (surface tension, viscosity); not all alloy systems fully supported
5. **Open-source alternative:** pycalphad + Scheil + analytical models can replicate some screening functionality at lower cost, but lack the integrated melt pool simulation and printability map capabilities

### Recommendation

The Thermo-Calc AM Module is a **strong fit** for VCL's alloy discovery pipeline, particularly for:
- Initial process window identification via printability maps
- Automated CALPHAD-based alloy screening via TC-Python
- Linking melt pool predictions to microstructural outcomes (CET, microsegregation, precipitation)
- Training ML surrogates for high-throughput alloy/process co-optimization

The existing EAGER budget allocation (~$20K/2yr) for Thermo-Calc licenses should include the AM Module add-on and relevant databases (TCAl9+ for Al alloys, TCHEA6+ for HEAs) to maximize utility. The TC-Python API provides the automation pathway needed for integration with VCL's Bayesian optimization framework.
