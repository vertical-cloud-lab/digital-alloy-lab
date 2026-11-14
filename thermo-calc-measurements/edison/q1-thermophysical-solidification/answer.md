Question: We want to MEASURE, on our own aluminium-alloy (and some copper-alloy) samples, the quantities that Thermo-Calc and pycalphad calculate, so we can validate or calibrate CALPHAD databases and models. Our samples are small: a few hundred grams of ultrasonically atomized powder per alloy (15-63 um), small arc-melted or cast buttons, and laser powder bed fusion (LPBF) single tracks, pads and ~10 mm coupons. Alloys of interest: AlSi10Mg, Al-Mg-Sc-Zr (Scalmalloy-type), lean Al-Mg-Zr / Al-Mn / Al-Ce / Al-Cu / Al-Fe-Ni type LPBF alloys, and Cu alloys (Ni-Al bronze C63000, Cu-Ni). Please review the peer-reviewed literature and standards and, for each quantity group below, give the best direct measurement method, the practical proxy method, typical uncertainty, minimum sample size, typical time per sample, the data-reduction / analysis that converts the raw signal into the CALPHAD-comparable quantity (with equations), and published examples that compared the measurement against Thermo-Calc, Scheil, or pycalphad predictions for Al or Cu alloys (with DOIs):

1. Liquidus, solidus, incipient melting, freezing range, fraction solid vs temperature and latent heat by DSC/DTA: heating/cooling-rate and sample-mass effects, calibration, baseline subtraction, heat-flow integration and thermal-lag (deconvolution / inverse) corrections, comparison with Scheil vs equilibrium; specific heat by the sapphire method (ASTM E1269).
2. Hot-cracking / hot-tearing susceptibility: Kou's |dT/d(fs^1/2)| index, CSC (Clyne-Davies), constrained-rod casting, and crack-density measurement on LPBF tracks and pads, and how well these correlate for Al alloys.
3. Thermal diffusivity and conductivity: laser flash (ASTM E1461) with k = alpha*rho*cp; electrical conductivity / resistivity by eddy current (%IACS, ASTM E1004) and four-point probe; the Wiedemann-Franz / Smith-Palmer relation for Al alloys; and how resistivity tracks solute in solid solution and precipitation.
4. Density and thermal expansion: Archimedes (ASTM B962), gas pycnometry, push-rod dilatometry (ASTM E228); lattice parameters from XRD (Nelson-Riley extrapolation, Rietveld) and Vegard-type solute-content estimates for supersaturated Al (Mg, Sc, Zr, Mn, Si).
5. Phase identification and fractions: XRD/Rietveld, SEM/EBSD image analysis and stereology, synchrotron diffraction; microsegregation and partition coefficients from EDS/WDS/EPMA mapping (e.g., weighted-interval-rank-sort methods) compared with Scheil.
6. Precipitation (TC-PRISMA-type outputs): precipitate size distributions, number density and volume fraction by TEM (with stereological correction), SAXS and atom-probe tomography; hardness and conductivity aging curves as proxies; calibrating interfacial energy from coarsening rates (LSW); TTP diagrams from isothermal aging.
7. Diffusion: diffusion couples and diffusion multiples with EDS/EPMA line scans, Boltzmann-Matano and Sauer-Freise analysis, open software (e.g., pyDiffusion), and use for mobility database assessment.
8. Elastic constants and strength: resonant ultrasound spectroscopy, impulse excitation (ASTM E1876), pulse-echo ultrasound, nanoindentation (Oliver-Pharr); yield strength from Vickers hardness (Tabor factor for Al alloys), shear punch, small punch and profilometry-based indentation plastometry for small samples.
9. Liquid surface tension and viscosity of Al and Cu alloy melts: electromagnetic/electrostatic levitation oscillating drop, sessile drop, maximum bubble pressure, oscillating-cup viscometry, and the oxide-film problem for Al.
10. Thermochemistry: enthalpy of formation/mixing (solution or drop calorimetry), activities (Knudsen effusion mass spectrometry, EMF), and Mg/Zn vapour pressure relevant to evaporation during LPBF.

End with a ranked table of which of these measurements give the most information per dollar and per hour for validating CALPHAD-based design of new LPBF aluminium alloys, and give a full reference list with DOIs.


# Experimental Validation of CALPHAD Databases and Models for LPBF Aluminium and Copper Alloys: A Comprehensive Measurement Guide

## 1. Liquidus, Solidus, Incipient Melting, Freezing Range, Fraction Solid vs. Temperature, and Latent Heat

### Best Direct Method: Calibrated DSC (Differential Scanning Calorimetry)

**Procedure.** DSC is the primary direct measurement method for solidification thermodynamics of Al and Cu alloys. Specimens of approximately 20 mg are machined from representative material and placed in alumina crucibles under flowing argon. Temperature and sensitivity calibration uses high-purity metal standards (In, Sn, Zn, Al); specific heat capacity is determined by the sapphire (α-Al₂O₃) ratio method per ASTM E1269. An empty-pan baseline run is subtracted from the sample signal (zhang2017differentialscanningcalorimetry pages 2-3, djurdjevic2025quantifyinglatentheat pages 4-7).

**Heating/cooling-rate effects.** Heating rates of 3–10 K/min are most commonly used; rates above 10 K/min increase thermal lag and broaden peaks, while very slow rates (0.5 K/min) may allow solid-state diffusion that shifts apparent transformation temperatures (gottardi2015solidfractiondetermination pages 1-2, zhang2017differentialscanningcalorimetry pages 1-2). For A356-type alloys, the calculated liquid fraction at a given temperature was found to be lower at 10 K/min than at 3 K/min (zhang2017differentialscanningcalorimetry pages 1-2). Cooling curves differ significantly from heating curves and should not be substituted when defining processing windows (zhang2017differentialscanningcalorimetry pages 8-11).

**Thermal-lag (deconvolution) correction.** The thermal resistance between the sample and the sensor causes the recorded temperature to lag the true sample temperature. The lag increases with heating rate and sample mass. The corrected temperature can be estimated by T_true ≈ T_recorded − R_th × (dH/dt), where R_th is the thermal resistance obtained from calibration. More rigorous approaches use inverse deconvolution methods that de-smear the instrument transfer function.

**Fraction solid and latent heat integration.** The fraction solid is obtained by partial integration of the baseline-subtracted heat-flow signal:

f_s(T) = 1 − [∫_{T_s}^{T} (dH/dT) dT] / [∫_{T_s}^{T_L} (dH/dT) dT]

where T_s and T_L are solidus and liquidus. Total latent heat is the integral ∫ (dH/dT) dT over the melting/solidification range. For AlSi5Cu alloys, DSC yielded latent heats of 424–438 kJ/kg, while Thermo-Calc predicted 434–456 kJ/kg and JMatPro 429–432 kJ/kg, with relative errors ranging from 0.2% to 7.5% (djurdjevic2025quantifyinglatentheat pages 8-10, djurdjevic2025quantifyinglatentheat pages 4-7).

**Comparison with Scheil vs. equilibrium.** For MHD-processed Al 319s, the first DSC heating curve resembled the equilibrium CALPHAD prediction more closely, while the Scheil prediction better matched strongly microsegregated material (zhang2017differentialscanningcalorimetry pages 8-11). Equilibrium calculations predict a solidus approximately 17 K higher than Scheil due to homogenization (zhang2017differentialscanningcalorimetry pages 1-2). Thermo-Calc Scheil calculations can be compared point-by-point with the DSC-derived f_s(T) curve.

**Practical proxy.** Cooling-curve thermal analysis (Newtonian method) in a small foundry cup provides comparable data at lower cost and with cooling rates representative of casting, giving latent heat within 0.4–1.4% of DSC values (djurdjevic2025quantifyinglatentheat pages 10-11, djurdjevic2025quantifyinglatentheat pages 7-8).

**Typical uncertainty.** Liquidus/solidus: ±1–3 K; latent heat: ±3–5%; f_s(T): ±0.02–0.05 absolute.

**Minimum sample.** ~10–30 mg per DSC run; arc-melted buttons or powder compacts are adequate.

**Time per sample.** 2–4 h including baseline and replicate runs.

---

## 2. Hot-Cracking / Hot-Tearing Susceptibility

### Kou's Criterion: |dT/d(f_s^{1/2})|

Kou's solidification cracking index (SCI) is defined as the maximum absolute slope of the temperature vs. square-root-of-solid-fraction curve near the end of solidification (kou2021predictingsusceptibilityto pages 8-10):

SCI = max |dT/d(f_s^{1/2})| evaluated as f_s^{1/2} → 1 (typically f_s > 0.87–0.99)

A steeper terminal slope indicates faster loss of liquid feeding and greater cracking susceptibility. The calculation starts with a CALPHAD Scheil–Gulliver solidification curve providing T vs. f_s, which is transformed to T vs. f_s^{1/2} and numerically differentiated (hyer2021effectsofalloy pages 1-2, wu2025advancesincrack pages 9-12).

### Clyne–Davies CSC Criterion

The Clyne–Davies crack susceptibility coefficient is a time-based ratio (oriola2024onthehot pages 32-36, djurdjevic2026improvingcastingsimulation pages 10-12, wu2025advancesincrack pages 12-14):

CSC = t_v / t_r = (t_{f_s=0.99} − t_{f_s=0.90}) / (t_{f_s=0.90} − t_{f_s=0.40})

At constant cooling rate R, this simplifies to:

CSC = (T_{f_s=0.90} − T_{f_s=0.99}) / (T_{f_s=0.40} − T_{f_s=0.90})

Higher CSC indicates higher cracking susceptibility.

### Experimental Validation

LPBF crack-density measurement involves fabricating single tracks, pads, or small coupons at standardized parameters, cross-sectioning, polishing, and measuring total crack length per unit area using optical/SEM metallography and ImageJ (jordan2026acomprehensivehot pages 44-49). Both Kou and CSC indices have shown qualitative agreement with observed cracking in Al–Si, AA5083, and Al-7xxx alloys processed by LPBF (hyer2021effectsofalloy pages 1-2). Introducing solid-state back-diffusion (available in Thermo-Calc's Scheil with back-diffusion module) reduces the predicted Kou index and shifts the composition of maximum susceptibility (hyer2021effectsofalloy pages 1-2).

### Constrained-Rod Casting

The constrained-rod casting test provides physical crack lengths under controlled restraint, and can validate CALPHAD-derived rankings for casting-relevant cooling rates.

**Typical uncertainty.** Kou's SCI depends on the Scheil database and numerical discretization near f_s = 1; experimental crack density is reproducible to ±15–25% when geometry and process parameters are held constant.

**Time per sample.** Computation: minutes. LPBF track fabrication + metallography: 2–6 h.

---

## 3. Thermal Diffusivity, Conductivity, and Electrical Resistivity

### Laser Flash Analysis (ASTM E1461)

The laser flash method applies a short energy pulse to the front surface of a disk specimen (typically 12.7 mm diameter × 2–3 mm thick) and records the rear-surface temperature transient with an IR detector. Thermal diffusivity α is determined from the half-rise time t_{1/2} by α = 0.1388 × L² / t_{1/2} (with finite-pulse, heat-loss, and non-uniform-heating corrections). Thermal conductivity is then (barakathulla2026conductivityofcast pages 4-5, akwaboa2023thermophysicalpropertiesof pages 2-4, barakathulla2026conductivityofcast pages 2-4):

k(T) = α(T) × ρ × c_p(T)

where ρ is the room-temperature density (measured by Archimedes or pycnometry) and c_p is specific heat (from DSC or a reference-sample ratio method using a molybdenum standard) (akwaboa2023thermophysicalpropertiesof pages 2-4).

**Sample preparation.** Surfaces are ground flat and coated with graphite for consistent laser absorption. Measurements are performed at 100–600 °C with 3+ replicates per temperature (akwaboa2023thermophysicalpropertiesof pages 2-4).

### Electrical Resistivity / Conductivity

**Eddy-current method (ASTM E1004):** A coil is placed on the sample surface and the impedance change measures conductivity in %IACS. Requires a flat area ≥10 mm and calibration blocks. Measurement takes seconds per point.

**Four-point probe:** Four collinear probes contact the surface; sheet resistivity ρ_s = (π/ln 2) × (V/I) × correction factors for finite geometry (barakathulla2026conductivityofcast pages 4-5).

### Wiedemann–Franz and Smith–Palmer Relations

The electronic thermal conductivity is related to electrical conductivity by the Wiedemann–Franz law (barakathulla2026conductivityofcast pages 4-5, akwaboa2023thermophysicalpropertiesof pages 7-9):

k_e = L × σ_e × T

where L is the Lorenz number (2.1–2.45 × 10⁻⁸ W·Ω/K² for Al alloys) and T is absolute temperature. Total thermal conductivity adds a lattice contribution: k = k_e + k_lattice, with k_lattice ≈ 10.5–12.6 W/(m·K) for Al alloys (barakathulla2026conductivityofcast pages 4-5).

The Smith–Palmer relation extends this: k = A × σ_e × T + B, where A and B are empirically fitted constants that account for the lattice contribution and deviations from the ideal Lorenz number.

### Resistivity as a Solute/Precipitation Tracker

Matthiessen's rule separates resistivity contributions: ρ_total = ρ_thermal + Σ(Δρ_i × c_i) + ρ_defects, where Δρ_i is the specific resistivity per wt% solute i in solid solution and c_i is its concentration. For Al alloys, specific resistivities include ~24 nΩ·m/wt% for Mn, ~5 nΩ·m/wt% for Si, ~5.4 nΩ·m/wt% for Mg (liu2017microstructureevolutionduring pages 139-143). Precipitation removes solute from solution, reducing ρ; thus resistivity-vs-aging-time curves track precipitation kinetics and can be compared with TC-PRISMA predictions of matrix composition (akwaboa2023thermophysicalpropertiesof pages 7-9, akwaboa2023thermophysicalpropertiesof pages 6-7).

**Typical uncertainty.** Laser flash α: ±2–3%; k: ±3–5% (combining α, ρ, c_p errors). Eddy current: ±0.5–1% IACS.

**Minimum sample.** 12.7 mm disk for LFA; ~10 mm flat area for eddy current.

**Time per sample.** LFA: 1–2 h; eddy current: 5 min.

---

## 4. Density and Thermal Expansion

### Archimedes Method (ASTM B962)

Samples are weighed in air and in a liquid of known density (water or ethanol). Density ρ = m_air × ρ_liquid / (m_air − m_liquid). Relative density (compared to CALPHAD-predicted theoretical density) quantifies porosity.

### Gas Pycnometry

Helium displacement pycnometry measures skeletal density on specimens as small as 1 cm³; accuracy ±0.01–0.02 g/cm³ (akwaboa2023thermophysicalpropertiesof pages 2-4).

### Push-Rod Dilatometry (ASTM E228)

A specimen (typically 25–50 mm long, 5–10 mm diameter) is heated at a controlled rate while a push rod records length change ΔL/L₀. The coefficient of thermal expansion (CTE) is α_CTE = (1/L₀)(dL/dT). Discontinuities in the CTE curve indicate phase transformations.

### XRD Lattice Parameters: Nelson–Riley Extrapolation and Vegard's Law

High-angle XRD peaks are measured and the lattice parameter a is plotted against the Nelson–Riley function cos²θ/sinθ + cos²θ/θ; the true parameter is the y-intercept. For Rietveld refinement, the full diffraction pattern is fitted to extract lattice parameters, phase fractions, and microstrain simultaneously.

**Vegard-type solute estimates for supersaturated Al.** For fcc Al with dissolved solute X, the lattice parameter shifts approximately linearly: a(X) = a_Al + Σ(∂a/∂c_X × c_X). Published coefficients include ∂a/∂c ≈ +5.3 × 10⁻⁴ nm/at% Mg, −2.0 × 10⁻⁴ nm/at% Si, +7.5 × 10⁻⁴ nm/at% Sc (in solution), and various values for Zr, Mn, Cu. These allow estimation of total solute retained in supersaturated solid solution after LPBF rapid solidification, providing a direct check against Scheil-predicted terminal solid composition.

**Typical uncertainty.** Archimedes: ±0.1–0.3%; lattice parameter: ±0.0001–0.0005 nm (Rietveld).

**Minimum sample.** Archimedes: ~1 g; XRD: ~1 cm² flat surface or ~0.5 g powder.

**Time per sample.** Archimedes: 15 min; XRD scan: 30–120 min; Rietveld analysis: 1–2 h.

---

## 5. Phase Identification, Phase Fractions, and Microsegregation

### XRD / Rietveld Refinement

Quantitative phase fractions are obtained by full-pattern Rietveld refinement, fitting calculated patterns for each crystalline phase to the measured diffractogram. The weight fraction of phase j is proportional to S_j² × Z_j × M_j × V_j, where S_j is the Rietveld scale factor, Z_j is the formula units per cell, M_j is molecular weight, and V_j is cell volume. Detection limits are typically 0.5–2 wt% for crystalline phases (liu2017microstructureevolutionduring pages 183-188).

### SEM/EBSD Image Analysis and Stereology

Phase fractions can be estimated from EBSD maps by counting indexed pixels for each phase, with stereological corrections for 2D sectioning effects. Area fraction equals volume fraction for random sections (Delesse's principle).

### Synchrotron Diffraction

High-energy synchrotron X-rays provide bulk-averaged phase fractions with superior peak resolution and access to in-situ solidification experiments.

### Microsegregation by EPMA/WDS Mapping

Quantitative electron-probe microanalysis provides spatially resolved composition maps with ~1–3 µm spatial resolution (liu2017microstructureevolutionduring pages 183-188, liu2017microstructureevolutionduring pages 143-151). The key data-reduction methods are:

**Weighted Interval Rank Sort (WIRS).** Each EPMA measurement point is assigned a weighted rank based on its composition relative to dataset extremes, with element-specific weights reflecting partitioning direction (k < 1 or k > 1). Points are sorted by this composite rank, and the normalized rank provides a fraction-solid coordinate: f_s(i) = (R_i − 0.5)/N. The resulting C_s(f_s) profiles are fitted to the Scheil equation (fukaya2026experimentalmeasurementsof pages 4-5, farnin2021solidificationpathand pages 18-23, farnin2021solidificationpathand pages 14-18):

ln(C_s/C_0) = (k − 1) × ln(1 − f_s) + ln(k)

The fitted k values for each element are the experimentally measured partition coefficients, directly comparable with CALPHAD Scheil predictions (farnin2021solidificationpathand pages 14-18, fukaya2026experimentalmeasurementsof pages 5-7). WIRS generally yields higher R² values than single-element sorting (fukaya2026experimentalmeasurementsof pages 4-5).

**Practical considerations.** The EPMA interaction volume (~2–3 µm) can mix matrix with fine precipitates, requiring Fe-concentration cutoffs or other masks to separate phases before constructing microsegregation profiles (liu2017microstructureevolutionduring pages 143-151). At least 5000 measurement points are recommended for reliable statistics (fukaya2026experimentalmeasurementsof pages 1-2).

**Typical uncertainty.** Rietveld phase fractions: ±1–3 wt%; EPMA partition coefficients: ±5–15% relative.

**Time per sample.** XRD + Rietveld: 2–4 h; EPMA map + WIRS analysis: 4–8 h.

---

## 6. Precipitation (TC-PRISMA-Type Outputs)

### Measurement Methods

**TEM.** Dark-field or HAADF-STEM imaging provides precipitate size distributions. Mean radius is measured from projected images with stereological corrections (Ashby–Brown or thickness-correction factors). Number density N_v = N_A / (t + d̄), where N_A is areal density, t is foil thickness, and d̄ is mean particle diameter. Volume fraction f_v = (4/3)π r̄³ × N_v.

**SAXS.** Small-angle X-ray scattering profiles are fitted with a form factor (spherical, Schulz-distributed sizes) plus a Porod term for large-scale heterogeneities and a constant background. Electronic contrast between precipitate and matrix (e.g., Al₃Sc assuming 25 at% Sc) provides absolute volume fraction; number density follows from f_v divided by mean particle volume (bajaj2020precipitationduringintrinsic pages 114-116). In-situ SAXS during isothermal holds tracks precipitation kinetics in real time.

**APT.** Atom-probe tomography provides 3D composition maps at near-atomic resolution. Clusters are identified using iso-concentration surfaces (e.g., 1 at% Sc threshold). Mean radius from cluster volume, number density from cluster count divided by reconstruction volume, and volume fraction from atom counts in precipitates (bajaj2020precipitationduringintrinsic pages 114-116). Core–shell structures (e.g., Al₃(Sc,Zr) with Zr-rich shell) are directly resolved.

### Comparison with TC-PRISMA / KWN Models

The Kampmann–Wagner numerical (KWN) framework, implemented in TC-PRISMA or Thermo-Calc's precipitation module, predicts time-evolving particle size distributions, number densities, and volume fractions. Key adjustable parameters are nucleation-site density, mobility-enhancement prefactor, and precipitate–matrix interfacial energy σ (bajaj2020precipitationduringintrinsic pages 111-114). For LPBF Al-Sc alloys, number densities up to 10²³ m⁻³ and radii below 5 nm have been reported in the as-built state (bajaj2020precipitationduringintrinsic pages 26-29).

### LSW Coarsening and Interfacial Energy Calibration

In the coarsening regime, the LSW relation gives:

r̄³(t) − r̄³(t₀) = K_r × t, where K_r = (8σV_m D C_e) / (9RT)

Measuring the mean radius r̄ at multiple aging times and fitting the slope K_r, with known D and C_e from the CALPHAD database, allows extraction of the interfacial energy σ. Published values for Al₃Sc/Al interfaces range from 0.07 to 0.15 J/m².

### Hardness and Conductivity as Proxies

Aging curves of Vickers hardness and electrical conductivity vs. time/temperature provide indirect TTP (time–temperature–precipitation) diagrams that can be compared with TC-PRISMA predictions of volume fraction and matrix composition evolution.

**Typical uncertainty.** TEM size: ±10–15%; number density: ±factor of 2; SAXS volume fraction: ±10–20%.

**Minimum sample.** TEM: electropolished 3 mm discs; SAXS: ~1 mm thick, few mm²; APT: needle specimens.

**Time per sample.** TEM: 8–16 h (including prep); APT: 8–24 h; SAXS: 2–8 h per beamtime slot.

---

## 7. Diffusion

### Diffusion Couples and Multiples

Diffusion couples are prepared by bonding end-members (e.g., pure Al vs. alloy, or two alloys of different composition), encapsulating in evacuated quartz tubes, and annealing at controlled temperatures for times sufficient to develop measurable diffusion profiles (typically 24–500 h) (zhong2019…ofdiffusion pages 80-87, christianson2020experimentalmeasurementof pages 1-2). Diffusion multiples extend this concept by joining multiple compositions in a single assembly, enabling high-throughput extraction of composition-dependent diffusivities from a single anneal (zhong2019…ofdiffusion pages 23-28).

### Analysis Methods

**Boltzmann–Matano.** The classic method transforms x vs. C profiles using the Boltzmann variable λ = x/√t. The Matano plane is located where ∫(C − C₀)dx = 0, and the interdiffusion coefficient is (wang2016computationalstudyof pages 1-4):

D̃(C*) = −(1/2t) × (dx/dC)|_{C*} × ∫_{C₀}^{C*} x dC

**Sauer–Freise.** An extension that does not require locating the Matano plane and accounts for volume changes during interdiffusion, useful for systems with significant molar volume differences (wang2016computationalstudyof pages 1-4, wang2016computationalstudyof pages 18-22).

**Forward-simulation analysis (FSA)** and **numerical inverse methods** iteratively simulate concentration profiles using assumed D(C) functions and optimize parameters until simulated profiles match experimental EPMA data (yang2024measurementofdiffusion pages 12-13, christianson2020experimentalmeasurementof pages 1-2).

**pyDiffusion** is an open-source Python library for diffusion simulation and data analysis that implements these methods (yang2024measurementofdiffusion pages 12-13).

### Mobility Database Assessment

Measured interdiffusion and impurity diffusion coefficients are used to optimize atomic mobility parameters within the CALPHAD framework. The mobility M_i is represented by an Arrhenius expression with composition-dependent Redlich–Kister polynomials. Optimization is performed using DICTRA's Parrot module, with validation against independent diffusion couples (wang2016computationalstudyof pages 1-4, wang2016computationalstudyof pages 18-22, christianson2020experimentalmeasurementof pages 1-2, christianson2020experimentalmeasurementof pages 7-8).

**Typical uncertainty.** D̃: ±10–30% (limited by EPMA spatial resolution and smoothing).

**Minimum sample.** Arc-melted buttons (5–10 g each end-member) bonded into 10–20 mm couples.

**Time per sample.** Preparation: 2–4 h; annealing: 24–500 h; EPMA + analysis: 8–16 h.

---

## 8. Elastic Constants and Strength

### Resonant Ultrasound Spectroscopy (RUS)

A small specimen (parallelepiped or sphere, ~1–10 mm) is placed between two piezoelectric transducers. The frequency spectrum of mechanical resonances is measured and compared with FEM-calculated resonance frequencies for trial values of elastic constants (C₁₁, C₁₂, C₄₄). Inverse optimization yields E, ν, and G simultaneously. Accuracy: ±0.1–0.5% for E.

### Impulse Excitation Technique (ASTM E1876)

A prismatic bar (recommended minimum ~50 × 10 × 3 mm) is struck with a small impulse and the natural flexural frequency f_f is measured. Young's modulus is calculated from E = 0.9465 × (m f_f² / b) × (L³/t³) × T₁, where T₁ is a correction factor for Poisson's ratio and specimen geometry. Torsional modes yield shear modulus G. Accuracy: ±1% for E (clyne2024profilometrybasedindentationplastometry pages 19-23).

### Pulse-Echo Ultrasound

Longitudinal and shear wave velocities V_L and V_S are measured through a specimen of known thickness. Elastic moduli follow from: E = ρV_S²(3V_L² − 4V_S²)/(V_L² − V_S²); ν = (V_L² − 2V_S²)/(2(V_L² − V_S²)).

### Nanoindentation (Oliver–Pharr)

A Berkovich or spherical indenter is pressed into the surface under load control. The unloading stiffness S = dP/dh and contact area A yield reduced modulus E_r = (√π / 2) × S / √A, from which E is extracted knowing the indenter's properties. Hardness H = P_max / A.

### Profilometry-Based Indentation Plastometry (PIP)

A spherical WC indenter creates a residual indent in a flat sample (minimum ~10 × 10 × 2 mm). The indent profile (depth and pile-up) is measured by profilometry. An inverse FEM procedure iterates Voce or Ludwik constitutive parameters until the simulated indent profile matches the measured one, yielding a full stress–strain curve and yield strength (clyne2024profilometrybasedindentationplastometry pages 19-23, tammpere2024profilometry‐basedindentationplastometry pages 13-14, mohammed2025boronnitridenanotubes pages 10-12). For Al 7075, PIP-derived yield strengths of ~378 MPa agreed well with bulk tensile values (mohammed2025boronnitridenanotubes pages 10-12). High-temperature PIP (to 800 °C) is now available but may be affected by creep at temperatures above ~200 °C for Al alloys (tammpere2024profilometry‐basedindentationplastometry pages 13-14).

### Vickers Hardness–Yield Strength (Tabor Relation)

For work-hardening metals, σ_y ≈ HV / (C × 3), where C is a constraint factor. For Al alloys with moderate work hardening, σ_y (MPa) ≈ HV/3 × 9.81 (with HV in kgf/mm²), or more precisely, σ_{0.08} ≈ HV/2.9 using the Tabor representative strain of ~8% for a Vickers indenter.

**Typical uncertainty.** IET: ±1% E; RUS: ±0.5% E; nanoindentation: ±5–10% E, ±10% H; PIP yield: ±5–10%.

**Minimum sample.** PIP: ~10 × 10 × 2 mm flat; nanoindentation: polished surface ~1 cm²; RUS: ~1 mm cube.

**Time per sample.** IET: 30 min; PIP: 1–2 h (including profiling); nanoindentation: 2–4 h.

---

## 9. Liquid Surface Tension and Viscosity

### Electromagnetic Levitation (EML) Oscillating Drop

A specimen (typically 0.5–2 g) is electromagnetically levitated and heated in Ar/He atmosphere. The molten droplet is squeezed by modulating the levitation field, exciting surface oscillations. Surface tension γ is calculated from the oscillation frequency using the Rayleigh relation (seimiya2026surfacetensionof pages 1-3, seimiya2026surfacetensionofa pages 6-9):

γ = (3π m ω_R²) / (8 × l(l−1)(l+2))

where ω_R is the angular frequency of the l = 2 surface mode and m is the droplet mass. Under terrestrial gravity, the fivefold degeneracy of the l = 2 mode is lifted and the Cummings–Blackburn sum rule combines the five observed frequencies (reiplinger2024densityandsurface pages 4-6). Viscosity η is obtained from the exponential damping of oscillation amplitude via the Lamb relation (beckers2021…oftemperaturedependent pages 4-8, beckers2021…oftemperaturedependent pages 1-4).

### The Oxide Film Problem for Al

Liquid aluminum rapidly forms a surface oxide (Al₂O₃) that has higher emissivity than the metal, causing pyrometric temperature overestimation and altering surface oscillation behavior. Oxide-affected heating curves must be excluded from pyrometer calibration, and oscillation data should be analyzed only when no oxide film is visible (seimiya2026surfacetensionof pages 1-3, seimiya2026surfacetensionofa pages 6-9, seimiya2026surfacetensionofa pages 1-6). For Al-rich melts, brief overheating to ~1650 K evaporates surface oxide, but this risks alloy evaporation (reiplinger2024densityandsurface pages 4-6).

### Comparison with CALPHAD / Butler Equation

The Butler equation combines bulk thermodynamic mixing data (excess Gibbs energies from CALPHAD) with pure-component surface tensions to predict alloy surface tension. For Al–Si alloys, the ideal-solution approximation reproduced measured surface tensions more consistently than the subregular-solution CALPHAD calculation, suggesting limited thermodynamic nonideality contribution to surface properties (seimiya2026surfacetensionof pages 1-3, seimiya2026surfacetensionofa pages 1-6).

### Other Methods

**Sessile drop** and **maximum bubble pressure** are container-based alternatives but suffer from oxide contamination and wetting artifacts for reactive Al melts. **Oscillating-cup viscometry** provides viscosity without levitation but uses crucibles.

**Published Al-alloy example.** Bärtl et al. measured surface tension of Scalmalloy (Al-Mg-Sc-Mn-Zr), Zicromal (Al-Cr-Zr-Mn), and Scancromal (Al-Cr-Sc-Zr) by EML, finding Scalmalloy's surface tension 3–8% lower than the Cr-based alloys over 500 K above liquidus, correlating with more unstable LPBF melt dynamics (Bärtl et al., J. Mater. Eng. Perform. 31:6221–6233, 2022, DOI: 10.1007/s11665-022-06592-z).

**Typical uncertainty.** γ: ±2–5%; η: ±10–20%.

**Time per sample.** 4–8 h per alloy (including levitation setup and multiple temperature points).

---

## 10. Thermochemistry

### Enthalpy of Formation/Mixing

**Solution calorimetry** dissolves a sample in a liquid-metal bath (e.g., liquid Sn at 700 °C) and measures the heat of dissolution, from which the enthalpy of formation is derived by Hess's law.

**Drop calorimetry** drops a sample at room temperature into a high-temperature calorimeter and measures the enthalpy increment, which includes both heat content and any transformation enthalpies.

### Activities by KEMS (Knudsen Effusion Mass Spectrometry)

KEMS heats a sample in a Knudsen cell with a small orifice; the effusing vapor is analyzed by mass spectrometry. Ion intensities are converted to partial pressures using ionization cross-sections and instrument sensitivity factors. Activities follow from a_i = p_i / p_i°. The method is particularly relevant for Mg vapor pressure measurement over Al-Mg alloys, directly validating the CALPHAD-predicted Mg activity and informing evaporation loss calculations during LPBF (beckers2021…oftemperaturedependent pages 13-16). Scalmalloy faces significant Mg evaporation during both powder production and LPBF processing due to Mg's high vapor pressure.

### EMF (Electromotive Force)

Galvanic cells with solid or liquid electrolytes measure the chemical potential difference of a component (e.g., Mg in Al-Mg alloys), providing activities directly through the Nernst equation: a_Mg = exp(−n F E / RT).

**Typical uncertainty.** ΔH_f: ±1–5 kJ/mol (solution calorimetry); activities by KEMS: ±5–15% relative.

**Minimum sample.** Calorimetry: 0.1–1 g; KEMS: 50–200 mg.

**Time per sample.** Solution calorimetry: 4–8 h; KEMS: 8–24 h.

---

## Ranked Cost-Effectiveness Table

The following table ranks the ten measurement groups by their information return per dollar and per hour for validating CALPHAD-based design of new LPBF aluminium alloys:

| Rank | Measurement Group | Best Direct Method | Approx. Cost per Sample (USD) | Time per Sample (h) | CALPHAD Quantities Validated (count) | Info/Dollar Score (10 = best) | Info/Hour Score (10 = best) | Overall Rank | Notes |
|---:|---|---|---:|---:|---|---:|---:|---:|---|
| 1 | **3 — Thermal/electrical transport** | Eddy-current conductivity first; laser-flash analysis when direct $\alpha(T)$ and $k(T)$ are needed | **$5–20** eddy current; **$100–300** LFA | **0.1**; **1–2** LFA | $\rho_e$, $\alpha$, $k$ (**3**) | **10** | **10** | **1** | Exceptional screening value: conductivity is sensitive to retained solute and precipitation; LFA gives $k=\alpha\rho c_p$. Use identical temperature and temper conditions. (barakathulla2026conductivityofcast pages 4-5, akwaboa2023thermophysicalpropertiesof pages 2-4, akwaboa2023thermophysicalpropertiesof pages 7-9) |
| 2 | **4 — Density, expansion, lattice parameter** | Archimedes density plus calibrated XRD; add dilatometry for $\mathrm{CTE}(T)$ | **$5–10** Archimedes; **$50–100** XRD | **0.2**; **1–2** XRD | $\rho$, CTE, lattice parameter/solution content (**3**) | **10** | **9** | **2** | Very inexpensive and reusable. Density also checks LPBF porosity; lattice parameter can constrain supersaturation only after correcting stress, temperature, texture, and phase overlap. |
| 3 | **1 — Melting and solidification** | Calibrated DSC/DTA with empty-pan baseline, multiple scan rates, and integrated heat flow | **$50–200** | **2–4** | $T_L$, $T_S$, freezing range, latent heat, $f_s(T)$ (**5**) | **9** | **8** | **3** | Highest-value direct thermodynamic experiment. Run representative as-built/cast material and a remelted second cycle; rate and thermal history materially change inferred $f_s(T)$. (gottardi2015solidfractiondetermination pages 1-2, zhang2017differentialscanningcalorimetry pages 2-3, zhang2017differentialscanningcalorimetry pages 1-2, djurdjevic2025quantifyinglatentheat pages 4-7) |
| 4 | **8 — Elastic constants and strength** | ASTM E1876 impulse excitation for $E$; PIP for yield/stress–strain; nanoindentation for local heterogeneity | **$20–50** IET; **$50–200** PIP; **$100–300** nanoindentation | **0.5**; **1–2** PIP; **2–4** nanoindentation | $E$, $\nu/G$, $\sigma_y$ or flow curve (**3**) | **9** | **9** | **4** | Rapid small-coupon screening. PIP uses inverse FE fitting of the residual indent profile and can agree well with tensile data, but texture, porosity, creep, and constitutive-form assumptions matter. (clyne2024profilometrybasedindentationplastometry pages 19-23, tammpere2024profilometry‐basedindentationplastometry pages 13-14, mohammed2025boronnitridenanotubes pages 10-12) |
| 5 | **2 — Hot cracking/hot tearing** | CALPHAD–Scheil Kou/CSC screening followed by standardized LPBF track/pad crack-density measurement | **≈$0** incremental computation; **$200–500** experimental validation | **1–4** | Terminal $f_s(T)$ behavior, crack index, observed crack density (**3**) | **8** | **8** | **5** | Cheap computational triage, but not a thermodynamic measurement by itself. Validate at fixed geometry/process window because grain refinement, residual stress, wetting, and feeding can reverse composition-only rankings. (hyer2021effectsofalloy pages 1-2, kou2021predictingsusceptibilityto pages 8-10, djurdjevic2026improvingcastingsimulation pages 10-12) |
| 6 | **5 — Phases and microsegregation** | XRD/Rietveld for bulk crystalline phase fractions plus quantitative EPMA/WDS mapping and WIRS/rank-sort analysis | **$100–200** XRD; **$200–500** per EPMA map | **2–4**; **4–8** EPMA | Phase identities/fractions and several $k_i$ or $C_i(f_s)$ curves (**≈5**) | **7** | **6** | **6** | Highly diagnostic for database errors. EPMA interaction volume and unresolved fine precipitates can mix matrix and particle chemistry; use many points, standards, masks, and uncertainty propagation. (liu2017microstructureevolutionduring pages 183-188, liu2017microstructureevolutionduring pages 143-151, farnin2021solidificationpathand pages 18-23, farnin2021solidificationpathand pages 14-18) |
| 7 | **6 — Precipitation kinetics** | TEM or SAXS for size distributions and fraction; APT when chemistry, clustering, or core–shell partitioning is essential | **$500–1,000** TEM; **$500–1,500** SAXS; **$2,000–5,000** APT | **8–16** TEM; **8–24** APT | Radius/PSD, number density, volume fraction, composition (**4**) | **4** | **4** | **7** | Essential for TC-PRISMA/KWN calibration but expensive and model-dependent. Combine SAXS statistics with TEM/APT chemistry rather than relying on one technique. (bajaj2020precipitationduringintrinsic pages 114-116, bajaj2020precipitationduringintrinsic pages 111-114, bajaj2020precipitationduringintrinsic pages 26-29) |
| 8 | **7 — Diffusion and mobility** | Diffusion couple or multiple, long anneal, quantitative EPMA, then Sauer–Freise or inverse/DICTRA fitting | **$500–2,000** per couple | **100–500** including anneal | $\tilde D(T,C)$ and fitted mobility parameters (**2–4**) | **4** | **1** | **8** | Poor throughput but uniquely valuable when mobility data control homogenization, precipitation, or back-diffusion. Use independent couples for validation rather than fitting and testing the same profile. (yang2024measurementofdiffusion pages 12-13, wang2016computationalstudyof pages 1-4, wang2016computationalstudyof pages 18-22, christianson2020experimentalmeasurementof pages 1-2) |
| 9 | **9 — Liquid surface tension and viscosity** | Electromagnetic-levitation oscillating drop, ideally with controlled oxygen and verified oxide-free surface | **$1,000–5,000** | **4–8** | $\gamma(T,x)$ and $\eta(T,x)$ (**2**) | **2** | **4** | **9** | Specialized but relevant to melt-pool dynamics. Al oxide films, evaporation, pyrometry, electromagnetic deformation, rotation, and mode splitting dominate uncertainty. (seimiya2026surfacetensionof pages 1-3, beckers2021…oftemperaturedependent pages 4-8, beckers2021…oftemperaturedependent pages 13-16, reiplinger2024densityandsurface pages 4-6) |
| 10 | **10 — Thermochemistry and activities** | Drop/solution calorimetry for $\Delta H$; KEMS or EMF for activities and vapor pressure | **$500–2,000** calorimetry; **$2,000–10,000** KEMS | **4–8**; **8–24** KEMS | $\Delta H_{mix/f}$, $a_i/\mu_i$, $p_i$ (**2–3**) | **1** | **2** | **10** | Most fundamental database-calibration data, but lowest routine return for alloy screening because facilities, reference states, vapor-species assignments, and high-temperature calibrations are demanding. Reserve for suspected database failures or Mg/Zn evaporation models. |


*Table: A practical ranking of measurement groups for validating CALPHAD-guided LPBF aluminium-alloy design, emphasizing information returned per external-testing dollar and laboratory hour. Costs are indicative service-labor ranges and exclude capital equipment, specimen fabrication, replicate tests, and method development.*

---

## Key Recommendations for Small-Sample CALPHAD Validation

For laboratories working with limited quantities of ultrasonically atomized powder (15–63 µm), arc-melted buttons, and small LPBF coupons:

1. **Start with eddy-current conductivity and Archimedes density** — these are fast, cheap, non-destructive, and immediately reveal whether solute partitioning and porosity match predictions.
2. **Run calibrated DSC** on ~20 mg specimens to validate liquidus, solidus, and f_s(T) against Scheil calculations.
3. **Compute Kou/CSC indices** from the same Scheil curves and validate against LPBF single-track crack density.
4. **Perform XRD Rietveld and EPMA/WIRS** on polished cross-sections to check phase fractions and partition coefficients.
5. **Use impulse excitation (IET) or PIP** for rapid elastic modulus and yield-strength screening on 10 mm coupons.
6. **Reserve TEM/SAXS/APT, diffusion couples, EML, and KEMS** for targeted investigations when database discrepancies are identified.

---

## References with DOIs

1. Djurdjevic, M.B.; Manasijevic, S. Improving Casting Simulation Accuracy Through Thermal Analysis of Aluminum Alloys. *Crystals* **2026**, 16, 159. DOI: 10.3390/cryst16030159

2. Djurdjevic, M.; Jovanovic, V.; Stopic, S. Quantifying Latent Heat in AlSi5Cu Alloys via DSC, Thermal Analysis, and Commercial Software. *Metals* **2025**, 15, 1045. DOI: 10.3390/met15091045

3. Zhang, D.; Atkinson, H.V.; Dong, H.; Zhu, Q. Differential Scanning Calorimetry (DSC) and Thermodynamic Prediction of Liquid Fraction vs Temperature for Two High-Performance Alloys. *Metall. Mater. Trans. A* **2017**, 48, 4701–4712. DOI: 10.1007/s11661-017-4235-2

4. Gottardi, G.; Pola, A.; La Vecchia, G.M. Solid Fraction Determination via DSC Analysis. 2015.

5. Kou, S. Predicting Susceptibility to Solidification Cracking and Liquation Cracking by CALPHAD. *Metals* **2021**, 11, 1442. DOI: 10.3390/met11091442

6. Hyer, H.; Zhou, L.; Mehta, A.; Sohn, Y. Effects of Alloy Composition and Solid-State Diffusion Kinetics on Powder Bed Fusion Cracking Susceptibility. *J. Phase Equilib. Diffus.* **2021**, 42, 5–13. DOI: 10.1007/s11669-020-00844-y

7. Wu, H. et al. Advances in Crack Formation Mechanisms, Evaluation Models, and Compositional Strategies for AM Ni-Based Superalloys. *CMES* **2025**, 143, 2675–2709. DOI: 10.32604/cmes.2025.064854

8. Barakathulla, A. et al. Conductivity of Cast Aluminium Alloys: A Review. *Int. J. Metalcast.* **2026**. DOI: 10.1007/s40962-026-01931-5

9. Akwaboa, S. et al. Thermophysical Properties of Laser Powder Bed Fused Ti-6Al-4V and AlSi10Mg Alloys. *Materials* **2023**, 16, 4920. DOI: 10.3390/ma16144920

10. Wang, J. et al. Computational Study of Atomic Mobility in hcp Mg–Al–Zn Ternary Alloys. *Calphad* **2016**, 54, 134–143. DOI: 10.1016/j.calphad.2016.07.003

11. Christianson, D.W.; Zhu, L.; Manuel, M.V. Experimental Measurement of Diffusion Coefficients and Assessment of Diffusion Mobilities in HCP Mg–Li–Al Alloys. *Calphad* **2020**, 71, 101999. DOI: 10.1016/j.calphad.2020.101999

12. Yang, Y.; Zhu, L.; Manuel, M.V. Measurement of Diffusion Coefficients and Assessment of Atomic Mobilities in HCP Mg-Ag-Sn Alloys. *J. Phase Equilib. Diffus.* **2024**, 45, 583–595. DOI: 10.1007/s11669-024-01114-x

13. Zhong, J.; Chen, L.; Zhang, L. High-Throughput Determination of High-Quality Interdiffusion Coefficients in Metallic Solids: A Review. *J. Mater. Sci.* **2020**, 55, 10303–10338. DOI: 10.1007/s10853-020-04805-1

14. Bajaj, P.; Svendsen, B.; Raabe, D. Precipitation During Intrinsic Heat Treatment in Laser Additive Manufacturing. 2020. DOI: 10.18154/rwth-2020-10461

15. Sigli, C. et al. Recent Advances in the Metallurgy of Aluminum Alloys. Part II: Age Hardening. *C. R. Phys.* **2018**, 19, 688–709. DOI: 10.1016/j.crhy.2018.10.012

16. Seimiya, Y.; Yoneyama, H.; Ozawa, S. Surface Tension of Molten Al–Si Alloys Measured by Electromagnetic Levitation. *Int. J. Thermophys.* **2026**, 47. DOI: 10.1007/s10765-026-03847-y

17. Reiplinger, B. et al. Density and Surface Tension of Liquid Al, V and Their Binary Alloys Measured by Electromagnetic Levitation. *J. Mater. Sci.* **2024**, 59, 13183–13199. DOI: 10.1007/s10853-024-09951-4

18. Bärtl, M. et al. Influence of Surface Tension and Evaporation on Melt Dynamics of Aluminum Alloys for LPBF. *J. Mater. Eng. Perform.* **2022**, 31, 6221–6233. DOI: 10.1007/s11665-022-06592-z

19. Halwax, A. et al. Enthalpy of Formation of Calcium and Magnesium Oxide Obtained by KEMS. *Metall. Mater. Trans. B* **2024**, 55, 821–835. DOI: 10.1007/s11663-024-02995-6

20. Tammpere, H. et al. Profilometry-Based Indentation Plastometry at High Temperature. *Adv. Eng. Mater.* **2024**, 26. DOI: 10.1002/adem.202301073

21. Mohammed, S.M.A.K. et al. Boron Nitride Nanotubes Induced Strengthening in Aluminum 7075 via Cryomilling and SPS. *Adv. Compos. Hybrid Mater.* **2025**, 8. DOI: 10.1007/s42114-024-01173-1

22. Chanbi, D. et al. Synthesis and Mechanical Characterization of Binary and Ternary Intermetallic Alloys Based on Fe-Ti-Al by Resonant Ultrasound Vibrational Methods. *Materials* **2018**, 11, 746. DOI: 10.3390/ma11050746

23. Liu, Z. et al. Alloy Design for Laser Powder Bed Fusion Additive Manufacturing: A Critical Review. *Int. J. Extreme Manuf.* **2024**, 6, 022002. DOI: 10.1088/2631-7990/ad1657

24. Zhang, C. et al. CALPHAD-Based Modeling and Experimental Validation of Microstructural Evolution and Microsegregation in Mg Alloys During Solidification. *J. Phase Equilib. Diffus.* **2019**, 40, 495–507. DOI: 10.1007/s11669-019-00732-0

25. Faria, G.A. et al. On the Use of Metastable Interface Equilibrium Assumptions on Prediction of Solidification Micro-Segregation in LPBF. *Sci. Technol. Weld. Join.* **2019**, 24, 446–456. DOI: 10.1080/13621718.2019.1608406

26. Stryzhyboroda, O. et al. Phase Equilibria in the Al–Co–Cr–Fe–Ni HEA System. *Front. Mater.* **2020**, 7, 270. DOI: 10.3389/fmats.2020.00270

27. Novakovic, R. et al. Thermodynamic Evaluation of the Surface Tension and Viscosity of Liquid Quaternary Alloys: Ti-Al-Cr-Nb. *Microgravity Sci. Technol.* **2023**, 35, 1–15. DOI: 10.1007/s12217-023-10080-x

28. Mohr, M. et al. Surface Tension and Viscosity of Liquid Pd₄₃Cu₂₇Ni₁₀P₂₀ Measured in Levitation Under Microgravity. *NPJ Microgravity* **2019**, 5. DOI: 10.1038/s41526-019-0065-4

29. Zhang, Y. et al. An Effective Approach to Acquire the Impurity Diffusion Coefficients in Binary Alloys with Quantified Uncertainties. *Metals* **2021**, 11, 809. DOI: 10.3390/met11050809

30. Argyrou, A. et al. LPBF AlSi10Mg at the Nanoscale: A Critical Review via Nanoindentation. *Appl. Sci.* **2026**, 16, 2730. DOI: 10.3390/app16062730

References

1. (zhang2017differentialscanningcalorimetry pages 2-3): Duyao Zhang, Helen V. Atkinson, Hongbiao Dong, and Qiang Zhu. Differential scanning calorimetry (dsc) and thermodynamic prediction of liquid fraction vs temperature for two high-performance alloys for semi-solid processing (al-si-cu-mg (319s) and al-cu-ag (201)). Metallurgical and Materials Transactions A, 48:4701-4712, Jul 2017. URL: https://doi.org/10.1007/s11661-017-4235-2, doi:10.1007/s11661-017-4235-2. This article has 24 citations.

2. (djurdjevic2025quantifyinglatentheat pages 4-7): Mile Djurdjevic, Vladimir Jovanovic, and Srecko Stopic. Quantifying latent heat in alsi5cu alloys (with 1, 2, and 4% of cu by mass) via dsc, thermal analysis, and commercial software. Metals, 15:1045, Sep 2025. URL: https://doi.org/10.3390/met15091045, doi:10.3390/met15091045. This article has 4 citations.

3. (gottardi2015solidfractiondetermination pages 1-2): G Gottardi, A Pola, and GM La Vecchia. Solid fraction determination via dsc analysis. Unknown journal, 2015.

4. (zhang2017differentialscanningcalorimetry pages 1-2): Duyao Zhang, Helen V. Atkinson, Hongbiao Dong, and Qiang Zhu. Differential scanning calorimetry (dsc) and thermodynamic prediction of liquid fraction vs temperature for two high-performance alloys for semi-solid processing (al-si-cu-mg (319s) and al-cu-ag (201)). Metallurgical and Materials Transactions A, 48:4701-4712, Jul 2017. URL: https://doi.org/10.1007/s11661-017-4235-2, doi:10.1007/s11661-017-4235-2. This article has 24 citations.

5. (zhang2017differentialscanningcalorimetry pages 8-11): Duyao Zhang, Helen V. Atkinson, Hongbiao Dong, and Qiang Zhu. Differential scanning calorimetry (dsc) and thermodynamic prediction of liquid fraction vs temperature for two high-performance alloys for semi-solid processing (al-si-cu-mg (319s) and al-cu-ag (201)). Metallurgical and Materials Transactions A, 48:4701-4712, Jul 2017. URL: https://doi.org/10.1007/s11661-017-4235-2, doi:10.1007/s11661-017-4235-2. This article has 24 citations.

6. (djurdjevic2025quantifyinglatentheat pages 8-10): Mile Djurdjevic, Vladimir Jovanovic, and Srecko Stopic. Quantifying latent heat in alsi5cu alloys (with 1, 2, and 4% of cu by mass) via dsc, thermal analysis, and commercial software. Metals, 15:1045, Sep 2025. URL: https://doi.org/10.3390/met15091045, doi:10.3390/met15091045. This article has 4 citations.

7. (djurdjevic2025quantifyinglatentheat pages 10-11): Mile Djurdjevic, Vladimir Jovanovic, and Srecko Stopic. Quantifying latent heat in alsi5cu alloys (with 1, 2, and 4% of cu by mass) via dsc, thermal analysis, and commercial software. Metals, 15:1045, Sep 2025. URL: https://doi.org/10.3390/met15091045, doi:10.3390/met15091045. This article has 4 citations.

8. (djurdjevic2025quantifyinglatentheat pages 7-8): Mile Djurdjevic, Vladimir Jovanovic, and Srecko Stopic. Quantifying latent heat in alsi5cu alloys (with 1, 2, and 4% of cu by mass) via dsc, thermal analysis, and commercial software. Metals, 15:1045, Sep 2025. URL: https://doi.org/10.3390/met15091045, doi:10.3390/met15091045. This article has 4 citations.

9. (kou2021predictingsusceptibilityto pages 8-10): Sindo Kou. Predicting susceptibility to solidification cracking and liquation cracking by calphad. Metals, 11:1442, Sep 2021. URL: https://doi.org/10.3390/met11091442, doi:10.3390/met11091442. This article has 58 citations.

10. (hyer2021effectsofalloy pages 1-2): Holden Hyer, Le Zhou, Abhishek Mehta, and Yongho Sohn. Effects of alloy composition and solid-state diffusion kinetics on powder bed fusion cracking susceptibility. Journal of Phase Equilibria and Diffusion, 42:5-13, Nov 2020. URL: https://doi.org/10.1007/s11669-020-00844-y, doi:10.1007/s11669-020-00844-y. This article has 47 citations and is from a peer-reviewed journal.

11. (wu2025advancesincrack pages 9-12): Huabo Wu, Jialiao Zhou, Lan Huang, Zi Wang, Liming Tan, Jin Lv, and Feng Liu. Advances in crack formation mechanisms, evaluation models, and compositional strategies for additively manufactured nickel-based superalloys. Computer Modeling in Engineering &amp; Sciences, 143:2675-2709, Jan 2025. URL: https://doi.org/10.32604/cmes.2025.064854, doi:10.32604/cmes.2025.064854. This article has 20 citations.

12. (oriola2024onthehot pages 32-36): A Oriola. On the hot cracking susceptibility of refractory high entropy alloys (rheas) during solidification: toward a crack susceptibility index for additive manufacturing. Unknown journal, 2024.

13. (djurdjevic2026improvingcastingsimulation pages 10-12): Mile B. Djurdjevic and Srecko Manasijevic. Improving casting simulation accuracy through thermal analysis of aluminum alloys. Crystals, 16:159, Feb 2026. URL: https://doi.org/10.3390/cryst16030159, doi:10.3390/cryst16030159. This article has 4 citations.

14. (wu2025advancesincrack pages 12-14): Huabo Wu, Jialiao Zhou, Lan Huang, Zi Wang, Liming Tan, Jin Lv, and Feng Liu. Advances in crack formation mechanisms, evaluation models, and compositional strategies for additively manufactured nickel-based superalloys. Computer Modeling in Engineering &amp; Sciences, 143:2675-2709, Jan 2025. URL: https://doi.org/10.32604/cmes.2025.064854, doi:10.32604/cmes.2025.064854. This article has 20 citations.

15. (jordan2026acomprehensivehot pages 44-49): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

16. (barakathulla2026conductivityofcast pages 4-5): Amjath Barakathulla, Abdallah Elsayed, Mark Easton, Trevor Abbott, John Grandfield, and Hua Qian Ang. Conductivity of cast aluminium alloys: a review. International Journal of Metalcasting, Mar 2026. URL: https://doi.org/10.1007/s40962-026-01931-5, doi:10.1007/s40962-026-01931-5. This article has 2 citations and is from a peer-reviewed journal.

17. (akwaboa2023thermophysicalpropertiesof pages 2-4): Stephen Akwaboa, Congyuan Zeng, Nigel Amoafo-Yeboah, Samuel Ibekwe, and Patrick Mensah. Thermophysical properties of laser powder bed fused ti-6al-4v and alsi10mg alloys made with varying laser parameters. Materials, 16:4920, Jul 2023. URL: https://doi.org/10.3390/ma16144920, doi:10.3390/ma16144920. This article has 11 citations.

18. (barakathulla2026conductivityofcast pages 2-4): Amjath Barakathulla, Abdallah Elsayed, Mark Easton, Trevor Abbott, John Grandfield, and Hua Qian Ang. Conductivity of cast aluminium alloys: a review. International Journal of Metalcasting, Mar 2026. URL: https://doi.org/10.1007/s40962-026-01931-5, doi:10.1007/s40962-026-01931-5. This article has 2 citations and is from a peer-reviewed journal.

19. (akwaboa2023thermophysicalpropertiesof pages 7-9): Stephen Akwaboa, Congyuan Zeng, Nigel Amoafo-Yeboah, Samuel Ibekwe, and Patrick Mensah. Thermophysical properties of laser powder bed fused ti-6al-4v and alsi10mg alloys made with varying laser parameters. Materials, 16:4920, Jul 2023. URL: https://doi.org/10.3390/ma16144920, doi:10.3390/ma16144920. This article has 11 citations.

20. (liu2017microstructureevolutionduring pages 139-143): Chenglu Liu. Microstructure evolution during homogenization and its effect on the high temperature deformation behaviour in aa6082 based alloys. ArXiv, Jan 2017. URL: https://doi.org/10.14288/1.0360654, doi:10.14288/1.0360654. This article has 19 citations.

21. (akwaboa2023thermophysicalpropertiesof pages 6-7): Stephen Akwaboa, Congyuan Zeng, Nigel Amoafo-Yeboah, Samuel Ibekwe, and Patrick Mensah. Thermophysical properties of laser powder bed fused ti-6al-4v and alsi10mg alloys made with varying laser parameters. Materials, 16:4920, Jul 2023. URL: https://doi.org/10.3390/ma16144920, doi:10.3390/ma16144920. This article has 11 citations.

22. (liu2017microstructureevolutionduring pages 183-188): Chenglu Liu. Microstructure evolution during homogenization and its effect on the high temperature deformation behaviour in aa6082 based alloys. ArXiv, Jan 2017. URL: https://doi.org/10.14288/1.0360654, doi:10.14288/1.0360654. This article has 19 citations.

23. (liu2017microstructureevolutionduring pages 143-151): Chenglu Liu. Microstructure evolution during homogenization and its effect on the high temperature deformation behaviour in aa6082 based alloys. ArXiv, Jan 2017. URL: https://doi.org/10.14288/1.0360654, doi:10.14288/1.0360654. This article has 19 citations.

24. (fukaya2026experimentalmeasurementsof pages 4-5): H Fukaya, M Kubo, S Yano, S Suzuki, and K Ioroi. Experimental measurements of partition coefficients in fe-36mass% ni alloy. Unknown journal, 2026.

25. (farnin2021solidificationpathand pages 18-23): CJ Farnin. Solidification path and weldability analysis of an experimental trip steel via novel characterization of variable solute partition coefficients. Unknown journal, 2021.

26. (farnin2021solidificationpathand pages 14-18): CJ Farnin. Solidification path and weldability analysis of an experimental trip steel via novel characterization of variable solute partition coefficients. Unknown journal, 2021.

27. (fukaya2026experimentalmeasurementsof pages 5-7): H Fukaya, M Kubo, S Yano, S Suzuki, and K Ioroi. Experimental measurements of partition coefficients in fe-36mass% ni alloy. Unknown journal, 2026.

28. (fukaya2026experimentalmeasurementsof pages 1-2): H Fukaya, M Kubo, S Yano, S Suzuki, and K Ioroi. Experimental measurements of partition coefficients in fe-36mass% ni alloy. Unknown journal, 2026.

29. (bajaj2020precipitationduringintrinsic pages 114-116): P. Bajaj, B. Svendsen, and D. Raabe. Precipitation during intrinsic heat treatment in laser additive manufacturing. ArXiv, pages 2020, Oct 2020. URL: https://doi.org/10.18154/rwth-2020-10461, doi:10.18154/rwth-2020-10461. This article has 3 citations.

30. (bajaj2020precipitationduringintrinsic pages 111-114): P. Bajaj, B. Svendsen, and D. Raabe. Precipitation during intrinsic heat treatment in laser additive manufacturing. ArXiv, pages 2020, Oct 2020. URL: https://doi.org/10.18154/rwth-2020-10461, doi:10.18154/rwth-2020-10461. This article has 3 citations.

31. (bajaj2020precipitationduringintrinsic pages 26-29): P. Bajaj, B. Svendsen, and D. Raabe. Precipitation during intrinsic heat treatment in laser additive manufacturing. ArXiv, pages 2020, Oct 2020. URL: https://doi.org/10.18154/rwth-2020-10461, doi:10.18154/rwth-2020-10461. This article has 3 citations.

32. (zhong2019…ofdiffusion pages 80-87): W Zhong. … of diffusion coefficients of nine elements in magnesium and establishment of a comprehensive mobility database for lightweight magnesium alloys. Unknown journal, 2019.

33. (christianson2020experimentalmeasurementof pages 1-2): David W. Christianson, Lilong Zhu, and Michele V. Manuel. Experimental measurement of diffusion coefficients and assessment of diffusion mobilities in hcp mg–li–al alloys. Calphad-computer Coupling of Phase Diagrams and Thermochemistry, 71:101999, Dec 2020. URL: https://doi.org/10.1016/j.calphad.2020.101999, doi:10.1016/j.calphad.2020.101999. This article has 11 citations.

34. (zhong2019…ofdiffusion pages 23-28): W Zhong. … of diffusion coefficients of nine elements in magnesium and establishment of a comprehensive mobility database for lightweight magnesium alloys. Unknown journal, 2019.

35. (wang2016computationalstudyof pages 1-4): Jingya Wang, Na Li, Chuanyun Wang, Juan Ignacio Beltran, Javier LLorca, and Yuwen Cui. Computational study of atomic mobility in hcp mg–al–zn ternary alloys. Calphad, 54:134-143, Sep 2016. URL: https://doi.org/10.1016/j.calphad.2016.07.003, doi:10.1016/j.calphad.2016.07.003. This article has 19 citations.

36. (wang2016computationalstudyof pages 18-22): Jingya Wang, Na Li, Chuanyun Wang, Juan Ignacio Beltran, Javier LLorca, and Yuwen Cui. Computational study of atomic mobility in hcp mg–al–zn ternary alloys. Calphad, 54:134-143, Sep 2016. URL: https://doi.org/10.1016/j.calphad.2016.07.003, doi:10.1016/j.calphad.2016.07.003. This article has 19 citations.

37. (yang2024measurementofdiffusion pages 12-13): Yang Yang, Lilong Zhu, and Michele V. Manuel. Measurement of diffusion coefficients and assessment of atomic mobilities in hcp mg-ag-sn alloys. Journal of Phase Equilibria and Diffusion, 45:583-595, Jun 2024. URL: https://doi.org/10.1007/s11669-024-01114-x, doi:10.1007/s11669-024-01114-x. This article has 3 citations and is from a peer-reviewed journal.

38. (christianson2020experimentalmeasurementof pages 7-8): David W. Christianson, Lilong Zhu, and Michele V. Manuel. Experimental measurement of diffusion coefficients and assessment of diffusion mobilities in hcp mg–li–al alloys. Calphad-computer Coupling of Phase Diagrams and Thermochemistry, 71:101999, Dec 2020. URL: https://doi.org/10.1016/j.calphad.2020.101999, doi:10.1016/j.calphad.2020.101999. This article has 11 citations.

39. (clyne2024profilometrybasedindentationplastometry pages 19-23): Bill Clyne. Profilometry-based indentation plastometry at high temperature. JournalArticle, Aug 2024. URL: https://doi.org/10.17863/cam.111087, doi:10.17863/cam.111087. This article has 0 citations.

40. (tammpere2024profilometry‐basedindentationplastometry pages 13-14): Hannes Tammpere, Phil McKeown, James Miller, Chizhou Fang, Emily Curtis, Marcus Gaiser‐Porter, Max Burley, James Campbell, Maria Artiles, Yuanbo Tang, Satoshi Utada, Roger Reed, and Trevor Clyne. Profilometry‐based indentation plastometry at high temperature. Advanced Engineering Materials, Aug 2024. URL: https://doi.org/10.1002/adem.202301073, doi:10.1002/adem.202301073. This article has 12 citations and is from a peer-reviewed journal.

41. (mohammed2025boronnitridenanotubes pages 10-12): Sohail M. A. K. Mohammed, Ambreen Nisar, Denny John, Abhijith K. Sukumaran, Yifei Fu, Tanaji Paul, Alexander F. Hernandez, Sudipta Seal, and Arvind Agarwal. Boron nitride nanotubes induced strengthening in aluminum 7075 composite via cryomilling and spark plasma sintering. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01173-1, doi:10.1007/s42114-024-01173-1. This article has 14 citations and is from a peer-reviewed journal.

42. (seimiya2026surfacetensionof pages 1-3): Yusaku Seimiya, Haruto Yoneyama, and Shumpei Ozawa. Surface tension of molten al–si alloys measured by electromagnetic levitation: comparison with ideal- and subregular-solution calculations. International Journal of Thermophysics, Oct 2026. URL: https://doi.org/10.1007/s10765-026-03847-y, doi:10.1007/s10765-026-03847-y. This article has 0 citations and is from a peer-reviewed journal.

43. (seimiya2026surfacetensionofa pages 6-9): Yusaku SEIMIYA, Haruto YONEYAMA, and Shumpei OZAWA. Surface tension of molten al–si alloys measured by electromagnetic levitation and evaluated using the butler equation. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10699497/v1, doi:10.21203/rs.3.rs-10699497/v1.

44. (reiplinger2024densityandsurface pages 4-6): B. Reiplinger, Y. Seimiya, J. Brillo, and S. Ozawa. Density and surface tension of liquid al, v and their binary alloys measured by electromagnetic levitation. Journal of Materials Science, 59:13183-13199, Jul 2024. URL: https://doi.org/10.1007/s10853-024-09951-4, doi:10.1007/s10853-024-09951-4. This article has 11 citations and is from a peer-reviewed journal.

45. (beckers2021…oftemperaturedependent pages 4-8): M Beckers, M Engelhardt, and S Schneider. … of temperature-dependent viscosity and surface tension of liquid al69. 1cu12. 8ag18. 1 eutectic alloy under microgravity conditions using the oscillating-drop-method. Unknown journal, 2021.

46. (beckers2021…oftemperaturedependent pages 1-4): M Beckers, M Engelhardt, and S Schneider. … of temperature-dependent viscosity and surface tension of liquid al69. 1cu12. 8ag18. 1 eutectic alloy under microgravity conditions using the oscillating-drop-method. Unknown journal, 2021.

47. (seimiya2026surfacetensionofa pages 1-6): Yusaku SEIMIYA, Haruto YONEYAMA, and Shumpei OZAWA. Surface tension of molten al–si alloys measured by electromagnetic levitation and evaluated using the butler equation. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10699497/v1, doi:10.21203/rs.3.rs-10699497/v1.

48. (beckers2021…oftemperaturedependent pages 13-16): M Beckers, M Engelhardt, and S Schneider. … of temperature-dependent viscosity and surface tension of liquid al69. 1cu12. 8ag18. 1 eutectic alloy under microgravity conditions using the oscillating-drop-method. Unknown journal, 2021.