<!--
Edison Scientific LITERATURE_HIGH (job-futurehouse-paperqa3-high)
Task ID: a45aed31-b276-48bf-a64f-7b98b9e53ce5
Submitted: 2026-11-28T08:50:24Z; fetched: 2026-11-28T09:24:29Z; status: success; has_successful_answer: True
Retrieved with edison-client 0.19.0 (EDISON_PLATFORM_API_KEY) from GitHub Actions for issue #254. The full trajectory is in the .trajectory.json file beside this one.
-->

**Question (LITERATURE_HIGH):** Beyond the uniaxial tensile test, which mechanical tests are used to select and qualify aerospace aluminum alloys and additively manufactured metal parts, what does each reveal that a tensile test cannot, and how much material and time does each take? Cover, with citations and DOIs: fracture toughness (ASTM E399, E1820, B645, B646, E561 R-curves) and the Kahn tear test (ASTM B871); fatigue (high-cycle per ASTM E466, low-cycle per E606, ultrasonic fatigue at 20 kHz) and fatigue-crack growth (E647); Charpy impact (E23) and why it is little used for aluminum; notched tension (E602) and notch sensitivity; compression (E9); shear (B769, B565 pin shear, V-notch); bearing (E238); hardness (Rockwell, Vickers, Brinell) and nanoindentation, and how well hardness predicts yield strength for aluminum; stress-corrosion cracking (G47, G139) and exfoliation (G34); residual-stress measurement; and small-specimen methods (small punch per ASTM E3205, shear punch, miniature tensile, micropillar compression, profilometry-based indentation plastometry). For additively manufactured parts, cover NASA-STD-6030 and MSFC-STD-3716, AMS 7032 and AMS 7003, MMPDS and CMH-17-style A- and B-basis allowables, the role of surface roughness, porosity, build orientation and HIP in fatigue, and why fatigue rather than tensile strength usually limits LPBF aluminum. Finally, which of these tests have been run in a high-throughput or automated way to screen alloys (automated hardness or nanoindentation maps, small punch, miniaturized tensile arrays, robotic test cells). Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion (LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, density cubes and room-temperature tensile bars. It is deciding which elevated-temperature, non-tensile and rate-dependent mechanical tests to add. Prefer primary sources, NASA, NIST and AFRL technical reports, MMPDS and standards; give DOIs or report numbers; give numbers with temperatures, exposure times, strain rates and units; and say which claims are strongly vs. weakly supported.

---

Question: Beyond the uniaxial tensile test, which mechanical tests are used to select and qualify aerospace aluminum alloys and additively manufactured metal parts, what does each reveal that a tensile test cannot, and how much material and time does each take? Cover, with citations and DOIs: fracture toughness (ASTM E399, E1820, B645, B646, E561 R-curves) and the Kahn tear test (ASTM B871); fatigue (high-cycle per ASTM E466, low-cycle per E606, ultrasonic fatigue at 20 kHz) and fatigue-crack growth (E647); Charpy impact (E23) and why it is little used for aluminum; notched tension (E602) and notch sensitivity; compression (E9); shear (B769, B565 pin shear, V-notch); bearing (E238); hardness (Rockwell, Vickers, Brinell) and nanoindentation, and how well hardness predicts yield strength for aluminum; stress-corrosion cracking (G47, G139) and exfoliation (G34); residual-stress measurement; and small-specimen methods (small punch per ASTM E3205, shear punch, miniature tensile, micropillar compression, profilometry-based indentation plastometry). For additively manufactured parts, cover NASA-STD-6030 and MSFC-STD-3716, AMS 7032 and AMS 7003, MMPDS and CMH-17-style A- and B-basis allowables, the role of surface roughness, porosity, build orientation and HIP in fatigue, and why fatigue rather than tensile strength usually limits LPBF aluminum. Finally, which of these tests have been run in a high-throughput or automated way to screen alloys (automated hardness or nanoindentation maps, small punch, miniaturized tensile arrays, robotic test cells). Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion (LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, density cubes and room-temperature tensile bars. It is deciding which elevated-temperature, non-tensile and rate-dependent mechanical tests to add. Prefer primary sources, NASA, NIST and AFRL technical reports, MMPDS and standards; give DOIs or report numbers; give numbers with temperatures, exposure times, strain rates and units; and say which claims are strongly vs. weakly supported.

# Mechanical Tests Beyond Uniaxial Tension for Aerospace Aluminum Alloys and Additively Manufactured Metal Parts

## 1. Fracture Toughness Testing

### ASTM E399 / B645 / B646 — Plane-Strain Fracture Toughness (K_IC)

Fracture toughness testing measures resistance to crack extension under plane-strain, linear-elastic conditions, expressed as the critical stress-intensity factor K_IC. A tensile test provides yield strength, UTS, and elongation on smooth specimens but reveals nothing about how a material behaves in the presence of a pre-existing flaw. ASTM E399 requires fatigue-precracked compact-tension C(T) or single-edge-bend SE(B) specimens with specific a/W and W/B proportions (briseno2021fracturemechanicson pages 5-8, briseno2021fracturemechanicson pages 1-3). ASTM B645 and B646 provide practice for determining and preparing aluminum-alloy fracture-toughness specimens, respectively. For an A413 aluminum alloy with σ_YS = 82 MPa, the calculated minimum valid specimen thickness was approximately 38 mm; at σ_YS = 130 MPa, minimum thickness was approximately 18 mm (briseno2021fracturemechanicson pages 5-8). C(T) specimens of 25 mm thickness have been used for aircraft-grade 2xxx and 7xxx alloys, tested in both L-T and T-L orientations at room temperature and 219.15 K (−54 °C), with at least three specimens per orientation (chemin2019characterizationofphases pages 3-6). These tests are time-consuming due to the fatigue pre-cracking requirement and can consume substantial material, particularly for high-toughness, low-strength alloys where validity requirements demand large specimens.

**What it reveals that tensile cannot:** Crack-initiation resistance, stable crack-growth resistance, plane-strain fracture toughness K_IC, and damage-tolerance behavior in the presence of flaws (briseno2021fracturemechanicson pages 1-3). **Strongly supported.**

### ASTM E1820 — J-Integral and CTOD

ASTM E1820 extends fracture characterization into the elastic-plastic regime via J-integral (J_IC) and crack-tip opening displacement (CTOD), applicable when plane-strain validity per E399 is not achievable. This is particularly relevant for tough aluminum alloys where valid K_IC specimens would be impractically large. J_IC testing is described as more suitable than K_IC for many aluminum alloys but experimentally more complicated (zhu2004teartoughnessevaluation pages 1-2).

### ASTM E561 — R-Curve (Crack-Resistance Curve)

E561 R-curve testing measures crack-resistance as a function of crack extension, capturing stable tearing behavior. This is essential for damage-tolerant design of aircraft structures where cracks may grow stably before catastrophic failure. R-curve methods can be more costly and time-consuming than tear tests (abachi2016fracturebehaviorevaluation pages 1-3). **Moderately supported** — specific procedural details from R-curve studies were not directly extracted.

### ASTM B871 — Kahn Tear Test

The Kahn tear test is an energy-based fracture test specifically developed for aluminum alloy sheet and thin products. It uses a small, V-notched specimen (typically 35 mm × 60 mm × sheet thickness, with a 60° notch and notch-root radius < 60 μm) loaded statically until a crack propagates across the specimen width (abachi2016fracturebehaviorevaluation pages 1-3, morgeneyer2008evolutionofvoids pages 1-2). For AA2139-T8 (3.2-mm sheet), specimens were 35 mm × 60 mm × 3.2 mm, with cracks arrested at ~10 mm propagation (morgeneyer2008evolutionofvoids pages 1-2). The test measures:
- **Unit initiation energy (UE_i):** energy to initiate a crack (e.g., 79 N·mm⁻¹ in T-L and 104 N·mm⁻¹ in L-T for AA2139-T8) (morgeneyer2008evolutionofvoids pages 1-2)
- **Unit propagation energy (UE_p):** energy for stable crack growth, identified as the representative tear-toughness measure (zhu2004teartoughnessevaluation pages 1-2)
- **Tear-strength-to-yield-strength ratio (TYR)** (abachi2016fracturebehaviorevaluation pages 1-3)

**Key advantage:** Low material consumption, low cost, short preparation time, and no fatigue pre-crack required (abachi2016fracturebehaviorevaluation pages 1-3). The reduction in Kahn tear resistance with increased constituent-particle content was shown to be greater than the reduction in smooth-tensile failure strain for 6xxx alloys, demonstrating that tensile ductility alone cannot predict tearing resistance (qvale2022theeffectof pages 1-2). **Strongly supported.**

---

## 2. Fatigue Testing

### High-Cycle Fatigue (HCF) — ASTM E466

ASTM E466 covers force-controlled, constant-amplitude axial fatigue testing of unnotched metallic specimens, typically using round uniform-gauge or hourglass specimens. Tests are run at frequencies of 10–60 Hz (commonly ~40 Hz), with stress ratios R = −1, 0.1, or 0.5 (plessis2020killernotchesthe pages 6-8, witkin2020influenceofsurface pages 1-2). Run-outs are typically defined at 10⁶ to 10⁷ cycles. For LPBF Al2024-RAM2, as-built fatigue limits at 2 × 10⁶ cycles ranged from 109 MPa (45° orientation, Ra = 17.6 μm) to 118 MPa (A-orientation, Ra = 2.1 μm); grinding to Ra = 0.6 μm raised the fatigue limit to 200 MPa (konecna2023influenceofbuild pages 9-12). Generating a full S-N curve typically requires 15–30 specimens across multiple stress levels and takes days to weeks depending on frequency and target life.

**What it reveals that tensile cannot:** Endurance limits, S-N behavior, crack-initiation sites, and the dominant role of surface roughness and defects under cyclic loading (konecna2023influenceofbuild pages 9-12). **Strongly supported.**

### Low-Cycle Fatigue (LCF) — ASTM E606

ASTM E606 covers strain-controlled fatigue testing at high strain amplitudes and low cycle counts (typically < 10⁴ cycles). It uses cylindrical specimens with extensometers, tested at strain rates of ~10⁻³ s⁻¹. LCF reveals cyclic stress-strain behavior, cyclic hardening/softening, hysteresis-loop evolution, and fatigue-life under plastic-strain-dominated conditions. For LPBF metals, LCF behavior depends on microstructure and strength in addition to surface and porosity effects (kan2022acriticalreview pages 15-17).

### Ultrasonic Fatigue at 20 kHz

Ultrasonic fatigue testing accelerates very-high-cycle fatigue (VHCF) testing by operating at ~20 kHz, enabling exploration of fatigue behavior up to 10⁹–10¹⁰ cycles. At 20 kHz continuous loading, 10⁹ cycles can be reached in approximately 14 hours, versus months at conventional frequencies (konecna2023influenceofbuild pages 9-12). This reveals subsurface crack-initiation mechanisms, "fish-eye" fracture origins at internal defects, and the existence (or absence) of a true fatigue limit in the VHCF regime. **Moderately supported** — specific LPBF aluminum VHCF data were referenced but not directly extracted.

### Fatigue Crack Growth (FCG) — ASTM E647

ASTM E647 measures da/dN versus ΔK using pre-cracked C(T) or M(T) specimens. It reveals crack-growth rates, threshold stress-intensity factor range (ΔK_th), Paris-law constants, and the influence of R-ratio, environment, and microstructure on crack propagation. For LPBF Inconel 718, threshold ΔK values of 2–6 MPa√m were calculated from near-surface defects ~50 μm in diameter that initiated fatigue cracks (witkin2020influenceofsurface pages 1-2). FCG testing typically requires C(T) specimens ≥ 25 mm wide and several weeks of testing per specimen.

---

## 3. Charpy Impact Testing (ASTM E23) and Why It Is Little Used for Aluminum

ASTM E23 uses a standard 10 × 10 × 55 mm notched bar struck by a pendulum to measure absorbed energy. For steels, Charpy testing is essential for identifying ductile-to-brittle transition temperatures (DBTT). Aluminum alloys, however, have FCC crystal structures that do not exhibit a sharp DBTT; they remain ductile to cryogenic temperatures. Consequently, Charpy values for aluminum are generally high and do not discriminate among alloys or tempers as effectively as fracture toughness or tear tests. MMPDS does not list Charpy requirements for most aluminum alloys, and the aerospace community relies instead on K_IC, Kahn tear, and R-curve testing for toughness qualification. **Moderately supported** — based on general metallurgical knowledge; direct citations on Charpy-aluminum limitations were not extracted.

---

## 4. Notched Tension (ASTM E602) and Notch Sensitivity

ASTM E602 covers sharp-notch tension testing to measure the notch tensile strength (NTS) and the notch-strength ratio (NSR = NTS/σ_YS). It reveals notch sensitivity: an alloy with NSR > 1 shows notch strengthening (ductile, redistributes stress), while NSR < 1 indicates notch embrittlement. The test uses circumferentially notched round bars with a 60° notch angle and a specified stress-concentration factor (K_t typically 6–8). For high-strength 7xxx alloys, tear tests with varying notch-root radii distinguished pop-in behavior (sudden failure from sharp notches) from gradual crack propagation, confirming that tensile tests on smooth specimens cannot capture this notch-sensitivity response (abachi2016fracturebehaviorevaluation pages 10-14).

---

## 5. Compression Testing (ASTM E9)

ASTM E9 covers uniaxial compression testing using short cylindrical specimens (typically L/D = 1.5–3.0 to avoid buckling). It reveals compressive yield strength (CYS) and work-hardening behavior, which may differ from tension in textured or anisotropic materials. For LPBF metals, compression testing has shown that apparent tensile anisotropy is sometimes due to spatial inhomogeneity rather than intrinsic anisotropy, as confirmed by systematic compressive tests (southern2023indentationplastometryfor pages 1-2). Material consumption is modest (~10 mm diameter × 20 mm cylinders), and tests take minutes.

---

## 6. Shear Testing (ASTM B769, B565, V-Notch)

**ASTM B769** covers double-shear testing of aluminum plate. **ASTM B565** covers pin-type bearing and shear testing for aerospace fastener holes. **V-notch shear** (e.g., Iosipescu) measures in-plane shear strength and modulus. These tests reveal shear strength (typically 55–65% of UTS for aluminum), shear modulus, and the alloy's response to fastener-loading geometries critical in aircraft joints. MMPDS requires shear allowables for structural design. For full A- or B-basis qualification, 20 shear specimens suffice if tensile allowables are already established from 100 specimens (abdi2020materialallowablegeneration pages 9-11).

---

## 7. Bearing Testing (ASTM E238)

ASTM E238 measures bearing yield and ultimate strength of sheet and plate by loading a pin through a hole. It reveals the material's resistance to hole elongation under fastener loading. Bearing strength is typically 1.5–2.0× the tensile UTS for aluminum alloys. Test specimens are small plates with a central hole, and multiple specimens can be cut from limited material.

---

## 8. Hardness Testing and Hardness–Yield-Strength Prediction for Aluminum

### Rockwell, Vickers, Brinell

Hardness testing (Rockwell B/F, Vickers HV, Brinell HB) is rapid, semi-destructive, and requires minimal material (a flat surface ≥ several mm²). It is used for quality control, heat-treatment verification, and spatial property mapping.

### Nanoindentation

Nanoindentation probes sub-micron to micron-scale volumes, measuring hardness and elastic modulus via the Oliver-Pharr method. High-throughput nanoindentation can produce 196–225+ indents per specimen in automated mapping modes (hintsala2018highthroughputnanoindentationfor pages 5-8).

### Hardness–Yield-Strength Correlation (Tabor Relation)

The classical Tabor relation links Vickers hardness to flow stress: P_m ≈ C·σ_f, where P_m is the mean contact pressure, C ≈ 2.956 is the constraint factor, and HV = 0.927·P_m. For fully work-hardened material, σ_YS ≈ HV/2.74, giving a slope of ~0.365 (sekhar2018hardnessyield pages 3-6). For age-hardenable Al-Mg-Si alloys, the relationship is better described with a fitted intercept: σ_YS = 0.383·HV − 101.5, achieving R² = 0.937 (sekhar2018hardnessyield pages 3-6, sekhar2018hardnessyield pages 6-7). Most predictions fall within ±15–30% of tensile-measured yield strength, but outliers arise from differing solution treatments, quenching conditions, and highly over-aged states (sekhar2018hardnessyield pages 6-7). For nanoindentation, the indentation size effect (ISE) causes hardness to increase at depths below ~1–2 μm, complicating direct conversion to bulk yield strength (rodrıguez2003correlationbetweennanoindentation pages 4-5, rodrıguez2003correlationbetweennanoindentation pages 1-2). Pile-up errors can reach ~60% for pyramidal indenters on non-hardening alloys (fujisawa2016amethodfor pages 4-4).

**Summary:** Hardness is a useful screening proxy for yield strength within a consistent alloy/temper family but is not universal; material-specific calibration is needed. **Strongly supported.**

---

## 9. Stress-Corrosion Cracking (ASTM G47, G139) and Exfoliation (ASTM G34)

### ASTM G47 — SCC Susceptibility

ASTM G47 determines susceptibility to stress-corrosion cracking in 2xxx and 7xxx aluminum alloy products by applying sustained tensile stress (typically via C-ring, bolt-loading, or direct tension) in an aggressive environment (usually alternate immersion in 3.5% NaCl solution, 10 min wet / 50 min dry cycles, at ~25 °C) for ≥ 20–30 days (holroyd2023environmentinducedcrackingof pages 29-30). It reveals whether an alloy-temper combination will develop SCC under service-relevant conditions.

### ASTM G139 — Breaking Load SCC

ASTM G139 uses a breaking-load method with pre-cracked or smooth specimens exposed to corrosive media under sustained load. It provides a quantitative measure of SCC resistance for heat-treatable aluminum alloy products (holroyd2023environmentinducedcrackingof pages 29-30).

**Limitation:** Holroyd et al. (2022) caution that ASTM G47 and G139 may not reliably distinguish the SCC susceptibility of closely performing, relatively resistant alloy tempers and cannot precisely predict service life (holroyd2023environmentinducedcrackingof pages 16-16, holroyd2023environmentinducedcrackingof pages 15-16). **Strongly supported.**

### ASTM G34 — Exfoliation (EXCO Test)

The EXCO test immerses specimens in an aggressive oxidizing acidic chloride solution (4.0 M NaCl + 0.5 M KNO₃ + 0.1 M HNO₃, initial pH ~0.4) for 48–96 hours. Surface appearance is visually rated from N (no attack) through EA–ED (increasing exfoliation severity) (zhao2006exfoliationcorrosionkinetics pages 39-43). This test identifies alloys and tempers susceptible to intergranular corrosion-driven layer-by-layer delamination. It can distinguish resistant and susceptible tempers (e.g., AA7075-T76 vs. T6) but may overstate attack relative to service environments for some alloys (zhao2006exfoliationcorrosionkinetics pages 39-43). **Strongly supported.**

### Residual-Stress Measurement

Residual stresses in LPBF parts are typically measured by X-ray diffraction (XRD), hole-drilling (ASTM E837), neutron diffraction, or contour methods. These are critical because LPBF produces high tensile residual stresses at surfaces that can accelerate fatigue-crack initiation and SCC. Shot peening has been shown to shift surface residual stresses from tension to compression, significantly improving fatigue behavior of LPBF Scalmalloy® (from the Musekamp 2022 study context).

---

## 10. Additive Manufacturing Qualification Standards

### NASA-STD-6030 and MSFC-STD-3716

NASA-STD-6030 is the governing standard for additively manufactured spaceflight hardware. It requires an Additive Manufacturing Control Plan (AMCP), a Material Usage Agreement (MUA) specifying the Material Property Suite (MPS), a Part Production Plan (PPP), and an End Item Data Package (EIDP) (glendening2020nasasplansfor pages 11-19). Qualification encompasses the complete process from design through flight-ready part, including feedstock control, process parameters, thermal management, post-processing, and in-process monitoring (kimbrel2026whitepaperdiscussion pages 7-12). MSFC-STD-3716 was the interim predecessor, developed for the SLS RS-25 program, covering metallic LPBF specifically (park2022nasasapproachto pages 12-22). Both require first-article material-property verification including tensile, fatigue, and fracture testing of witness specimens from every hardware build (glendening2020nasasplansfor pages 11-19).

### AMS 7032 and AMS 7003

AMS 7032 defines Installation Qualification (IQ), Operational Qualification (OQ), and Performance Qualification (PQ) for AM processes, concepts reflected within the NASA framework though not using identical terminology (kimbrel2026whitepaperdiscussion pages 7-12). AMS 7003 covers wire-feed AM processes.

### MMPDS A-Basis and B-Basis Allowables

A-basis (T99): a minimum property value that at least 99% of the population will meet or exceed, with 95% confidence. B-basis (T90): at least 90% will meet or exceed, with 95% confidence (prater2016summaryreportfor pages 49-51). Conventional MMPDS requires ≥ 100 specimens from ≥ 10 lots (10 per lot) for full allowable determination; nonparametric distributions may require ≥ 300 observations. A reduced B-basis plan uses ≥ 20 samples from ≥ 3 heats (prater2016summaryreportfor pages 51-53, abdi2020materialallowablegeneration pages 9-11). For AM, equivalent terminology uses C-basis (= A-basis) and D-basis (= B-basis), reflecting the additional variability from build direction, machine, and location (gunasegaram2026modelbasedinsitu pages 13-16). The conventional approach is expensive for AM due to process-dependent variability, motivating model-based and statistically updated approaches using Process Control Reference Distributions (PCRD) (prater2016summaryreportfor pages 51-53, prater2016summaryreportfor pages 57-59). **Strongly supported.**

---

## 11. Why Fatigue Rather Than Tensile Strength Usually Limits LPBF Aluminum

LPBF aluminum alloys routinely achieve tensile yield strengths comparable to wrought counterparts after heat treatment (e.g., 300–450 MPa for AlSi10Mg). However, fatigue performance is severely degraded by:

- **Surface roughness:** As-built LPBF surfaces have Ra = 1.5–17.6 μm depending on orientation, acting as "killer notches" that nucleate fatigue cracks (plessis2020killernotchesthe pages 6-8, afroz2025fatiguelifeof pages 1-2, konecna2023influenceofbuild pages 9-12). For AlSi10Mg, as-built fatigue strength was only 54 MPa; combined post-processing (blasting + laser treatment + laser cavitation peening) raised it to 103 MPa (from Soyama 2024 context, doi:10.3390/coatings14091174).
- **Porosity:** Subsurface pores (lack-of-fusion and gas porosity) become fatigue-crack initiation sites, especially after machining exposes them. Pore size and location matter more than total porosity (afroz2025fatiguelifeof pages 1-2). HIP reduced porosity by 64% and mean pore diameter by 11% in AlSi10Mg (kan2022acriticalreview pages 20-21).
- **Build orientation:** Lack-of-fusion pores at melt-pool boundaries are especially harmful in vertically built specimens (kan2022acriticalreview pages 18-20). Fatigue limits showed modest orientation dependence (109–118 MPa for Al2024-RAM2 depending on orientation) (konecna2023influenceofbuild pages 9-12).
- **HIP effects:** HIP closes porosity and can improve fatigue life but may coarsen the Si phase and reduce hardness; post-HIP machining may be needed (kan2022acriticalreview pages 20-21, afroz2025fatiguelifeof pages 1-2).

The fundamental reason is that tensile tests average bulk properties over the gauge section, while fatigue failure is controlled by the worst local defect in the stressed volume (plessis2020killernotchesthe pages 6-8, afroz2025fatiguelifeof pages 1-2). **Strongly supported.**

---

## 12. Small-Specimen and Emerging Methods

### Small Punch Test (ASTM E3205)

ASTM E3205-20 specifies an 8 mm diameter × 0.5 mm thick disk specimen clamped between dies and loaded by a 2.5 mm diameter ball (or 1.25 mm radius punch) (cannon2026evaluationofthe pages 1-2, brown2020finiteelementmodelling pages 63-68). Material volume is only ~25 mm³. The force-displacement curve yields transition force (F_A), maximum force (F_M), failure displacement (U_F), and total energy, from which yield strength and UTS are estimated via empirical correlations (brown2020finiteelementmodelling pages 63-68). SPT has been applied to AM Ti-6Al-4V, IN718, and stainless steels to assess anisotropy, build-orientation effects, heat-treatment response, and spatial property variation within builds (torres2021mechanicsofthe pages 3-5, lucon2021smallpunchtesting pages 13-14). It has also been combined with Jominy bar testing as a high-throughput screening methodology for heat-treatment optimization (from Miguel 2023, doi:10.3390/met13111797). **Strongly supported.**

### Profilometry-Based Indentation Plastometry (PIP)

PIP uses a spherical indenter ball (~0.5–1 mm radius) pressed into the sample to a controlled depth under kN-range loads. After indentation, the three-dimensional residual indent profile is measured by profilometry. Iterative inverse FEM simulation then converges on the best-fit constitutive stress-strain law (typically Voce) by matching predicted and measured profiles (campbell2022indentationplastometryof pages 1-1, reiffmusgrove2023indentationplastometryof pages 2-2, gu2022indentationplastometryof pages 1-1). The characterized volume is a disk of ~1 mm diameter and ~100–200 μm depth, providing ~1–2 mm lateral resolution (gu2022indentationplastometryof pages 1-1). Commercial automated systems complete indentation, profilometry, and convergence within a few minutes (southern2023indentationplastometryfor pages 2-2). PIP-derived stress-strain curves show excellent agreement with tensile and compressive test data (gu2022indentationplastometryof pages 1-1, campbell2022indentationplastometryof pages 1-1). For AM metals, PIP has been used to study anisotropy, spatial inhomogeneity, and the effect of build position in LPBF maraging steel, detecting that apparent tensile anisotropy was actually due to build-height inhomogeneity (southern2023indentationplastometryfor pages 1-2). PIP has also been applied to porosity effects in AM stainless steel (from Reiff-Musgrove 2022, doi:10.1002/adem.202200642) and can operate at high temperatures up to 800 °C (from Tammpere 2024, doi:10.1002/adem.202301073). **Strongly supported.**

### Micropillar Compression

FIB-milled micropillars (typically 2 μm diameter, 6–7 μm height) enable single-crystal or single-grain mechanical testing. For AM 316L stainless steel, micropillar compression yielded yield stresses of 431–474 MPa, versus 322 MPa for cast material (from Kurdi 2024, doi:10.3390/ma17020439). This technique reveals crystallographic-orientation-dependent deformation, phase-specific mechanical response, and grain-boundary effects, but exhibits size effects and does not directly measure bulk engineering properties (jayaram2022smallscalemechanicaltesting pages 12-13). Material consumption is negligible but FIB preparation is slow (~hours per pillar).

### Miniature Tensile Testing and Shear Punch

Miniature tensile specimens (gauge lengths 5–15 mm, cross-sections ~1 × 0.5 mm) can be machined from small volumes of AM material. The shear punch test uses a flat-ended cylindrical punch pushed through a clamped disk, providing shear yield and ultimate strength from even smaller specimens than SPT.

---

## 13. High-Throughput and Automated Mechanical Testing

### Automated Nanoindentation Mapping

High-throughput nanoindentation is the most mature automated screening method. Modern systems achieve hundreds to thousands of indents per sample using Accelerated Property Mapping (XPM), with individual indent contact times as short as 0.2 s (versus 20 s conventional), reducing drift by two orders of magnitude (hintsala2018highthroughputnanoindentationfor pages 5-8). Hoefler et al. (2025) demonstrated 2,400 nanoindentation + SEM data points in 13 days on a single gradient-aged superalloy sample—approximately 200× faster than conventional tensile testing for equivalent data volume. Each indent required an average of 188 s including loading, while automated SEM imaging took ~44 s per position (hoefler2025automatedsystemfor pages 10-11). The total preparation + measurement time was 314 hours (hoefler2025automatedsystemfor pages 10-11).

### HT-READ (High-Throughput Rapid Experimental Alloy Development)

Vecchio et al. (2021) developed HT-READ, an integrated closed-loop framework combining CALPHAD computation, directed-energy-deposition fabrication of 16-composition libraries via an Alloy Development Feeder, and automated characterization including XRD (~10 min/sample), SEM-EDS/EBSD (~1 min/sample), and nanoindentation (vecchio2021highthroughputrapidexperimental pages 4-7, vecchio2021highthroughputrapidexperimental pages 33-50). Machine-learning (Automatminer) correctly identified three of the five hardest compositions from the 16-member library (vecchio2021highthroughputrapidexperimental pages 4-7). **Strongly supported.**

### Combinatorial Approaches

Diffusion multiples create continuous composition gradients across ternary systems; scanning nanoindentation then maps hardness and modulus across the gradient at ~1,000× the efficiency of one-at-a-time testing (zhang2017combinatorialapproachesfor pages 7-9). Microfabricated cantilever beam arrays enable parallel thin-film property measurement, and MEMS-based tensile arrays allow parallel microtensile testing (zhang2017combinatorialapproachesfor pages 5-7, zhang2017combinatorialapproachesfor pages 9-10). SPT on Jominy bars has been demonstrated for high-throughput screening of heat-treatment effects (from Miguel 2023, doi:10.3390/met13111797).

### Robotic Test Cells

Fully robotic mechanical-testing cells integrating specimen handling, testing, and data analysis are an emerging capability referenced in the literature but not yet widely documented for aluminum alloy screening in peer-reviewed studies. **Weakly supported.**

---

## 14. Summary Recommendations for the BYU Vertical Cloud Lab

Given that the BYU lab designs LPBF aluminum alloys with AI and CALPHAD, makes powder by ultrasonic atomization, and currently tests through single tracks, density cubes, and room-temperature tensile bars, the following tests should be prioritized for addition:

**Highest priority (fatigue-critical for LPBF aluminum):**
1. **High-cycle fatigue (ASTM E466):** Because fatigue, not tensile strength, is the life-limiting property for LPBF aluminum. Surface roughness, porosity, and build orientation all govern fatigue performance.
2. **Automated nanoindentation mapping:** For rapid screening of hardness-composition-microstructure relationships across alloy libraries—the most automatable and highest-throughput mechanical test available (~200× faster than tensile).
3. **Small punch testing (ASTM E3205):** For estimating tensile properties from minimal material (25 mm³ per specimen), enabling screening of many compositions.

**High priority (qualification-essential):**
4. **Fracture toughness (ASTM E399/E1820) or Kahn tear test (B871):** Kahn tear testing is recommended first due to low material requirements and suitability for sheet/thin specimens.
5. **Fatigue crack growth (ASTM E647):** Required for damage-tolerance certification.
6. **Stress-corrosion cracking (ASTM G47) and exfoliation (G34):** Essential for any alloy intended for service in humid or marine environments.

**Medium priority (supplementary/screening):**
7. **PIP (profilometry-based indentation plastometry):** Full stress-strain curves from minimal material in minutes, with demonstrated applicability to AM metals.
8. **Elevated-temperature tensile testing:** For alloys targeting thermal stability.
9. **Compression testing (ASTM E9):** To verify isotropy and characterize compressive properties.

**Lower priority (specialized):**
10. **Charpy impact (E23):** Low discriminating power for aluminum alloys.
11. **Bearing (E238) and shear (B769, B565):** Needed only for specific joint-design qualification.
12. **Micropillar compression:** Valuable for understanding single-grain behavior but not for engineering qualification.

---

## Strength of Evidence Assessment

| Claim | Support Level |
|-------|---------------|
| Fracture toughness tests reveal damage tolerance that tensile cannot | **Strong** |
| Kahn tear test specimen sizes and unit energies | **Strong** |
| Fatigue limits LPBF aluminum due to surface/porosity defects | **Strong** |
| ASTM G34 EXCO solution and exposure conditions | **Strong** |
| Hardness predicts Al yield strength within ±15–30% with calibration | **Strong** |
| MMPDS A/B-basis definitions and specimen requirements | **Strong** |
| NASA-STD-6030 qualification framework | **Strong** |
| Automated nanoindentation achieves ~200× faster screening | **Strong** |
| PIP provides accurate stress-strain curves for AM metals | **Strong** |
| SPT ASTM E3205 specimen dimensions and AM applicability | **Strong** |
| HT-READ methodology for combinatorial alloy screening | **Strong** |
| Charpy is little used for aluminum due to no DBTT | **Moderate** |
| Robotic test cells for alloy screening | **Weak** |
| Ultrasonic fatigue specific LPBF aluminum data | **Moderate** |
| AMS 7032/7003 detailed requirements | **Moderate** |


References

1. (briseno2021fracturemechanicson pages 5-8): Juan Jose Mejia Briseno and Francisco Casanova-del-Angel. Fracture mechanics on aluminum specimens. World Journal of Mechanics, 11:237-257, Jan 2021. URL: https://doi.org/10.4236/wjm.2021.1112016, doi:10.4236/wjm.2021.1112016. This article has 10 citations.

2. (briseno2021fracturemechanicson pages 1-3): Juan Jose Mejia Briseno and Francisco Casanova-del-Angel. Fracture mechanics on aluminum specimens. World Journal of Mechanics, 11:237-257, Jan 2021. URL: https://doi.org/10.4236/wjm.2021.1112016, doi:10.4236/wjm.2021.1112016. This article has 10 citations.

3. (chemin2019characterizationofphases pages 3-6): Aline Emanuelle Albuquerque Chemin, Conrado Moreira Afonso, Fernando Antonio Pascoal, Carla Isabel dos Santos Maciel, Cassius Olivio Figueiredo Terra Ruchert, and Waldek Wladimir Bose Filho. Characterization of phases, tensile properties, and fracture toughness in aircraft‐grade aluminum alloys. Material Design & Processing Communications, Aug 2019. URL: https://doi.org/10.1002/mdp2.79, doi:10.1002/mdp2.79. This article has 29 citations and is from a peer-reviewed journal.

4. (zhu2004teartoughnessevaluation pages 1-2): Hong Zhu, Shinji Kumai, Toshikazu Tanaka, and Akikazu Sato. Tear toughness evaluation of a permanent mold cast a356 aluminum alloy using a small-size specimen. Materials Transactions, 45:1714-1721, May 2004. URL: https://doi.org/10.2320/matertrans.45.1714, doi:10.2320/matertrans.45.1714. This article has 11 citations and is from a peer-reviewed journal.

5. (abachi2016fracturebehaviorevaluation pages 1-3): Parvin Abachi, Pouyan Shoushtari Zadeh Naseri, Kazem Purazrang, and Tom W. Coyle. Fracture behavior evaluation of high-strength 7050 and 7075 aluminum alloys using v-notched specimen. Fracture Mechanics - Properties, Patterns and Behaviours, Oct 2016. URL: https://doi.org/10.5772/64463, doi:10.5772/64463. This article has 12 citations.

6. (morgeneyer2008evolutionofvoids pages 1-2): T.F. Morgeneyer, M.J. Starink, and I. Sinclair. Evolution of voids during ductile crack propagation in an aluminium alloy sheet toughness test studied by synchrotron radiation computed tomography. Acta Materialia, 56:1671-1679, May 2008. URL: https://doi.org/10.1016/j.actamat.2007.12.019, doi:10.1016/j.actamat.2007.12.019. This article has 116 citations and is from a highest quality peer-reviewed journal.

7. (qvale2022theeffectof pages 1-2): Kristin Qvale, Susanne Thomesen, Odd Sture Hopperstad, and Tore Børvik. The effect of constituent particles on the tear resistance of three 6000-series aluminium alloys. International Journal of Fracture, 238:165-183, Aug 2022. URL: https://doi.org/10.1007/s10704-022-00658-8, doi:10.1007/s10704-022-00658-8. This article has 6 citations and is from a peer-reviewed journal.

8. (plessis2020killernotchesthe pages 6-8): A. du Plessis and S. Beretta. Killer notches: the effect of as-built surface roughness on fatigue failure in alsi10mg produced by laser powder bed fusion. Additive Manufacturing, 35:101424, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101424, doi:10.1016/j.addma.2020.101424. This article has 230 citations and is from a highest quality peer-reviewed journal.

9. (witkin2020influenceofsurface pages 1-2): David B. Witkin, Dhruv Patel, Thomas V. Albright, Glenn E. Bean, and Tait McLouth. Influence of surface conditions and specimen orientation on high cycle fatigue properties of inconel 718 prepared by laser powder bed fusion. International Journal of Fatigue, 132:105392, Mar 2020. URL: https://doi.org/10.1016/j.ijfatigue.2019.105392, doi:10.1016/j.ijfatigue.2019.105392. This article has 127 citations and is from a domain leading peer-reviewed journal.

10. (konecna2023influenceofbuild pages 9-12): Radomila Konecna, Tibor Varmus, Gianni Nicoletto, and Michal Jambor. Influence of build orientation on surface roughness and fatigue life of the al2024-ram2 alloy produced by laser powder bed fusion (l-pbf). Metals, 13:1615, Sep 2023. URL: https://doi.org/10.3390/met13091615, doi:10.3390/met13091615. This article has 17 citations.

11. (kan2022acriticalreview pages 15-17): Wen Hao Kan, Louis Ngai Sam Chiu, Chao Voon Samuel Lim, Yuman Zhu, Yang Tian, Derui Jiang, and Aijun Huang. A critical review on the effects of process-induced porosity on the mechanical properties of alloys fabricated by laser powder bed fusion. Journal of Materials Science, 57:9818-9865, Mar 2022. URL: https://doi.org/10.1007/s10853-022-06990-7, doi:10.1007/s10853-022-06990-7. This article has 422 citations and is from a peer-reviewed journal.

12. (abachi2016fracturebehaviorevaluation pages 10-14): Parvin Abachi, Pouyan Shoushtari Zadeh Naseri, Kazem Purazrang, and Tom W. Coyle. Fracture behavior evaluation of high-strength 7050 and 7075 aluminum alloys using v-notched specimen. Fracture Mechanics - Properties, Patterns and Behaviours, Oct 2016. URL: https://doi.org/10.5772/64463, doi:10.5772/64463. This article has 12 citations.

13. (southern2023indentationplastometryfor pages 1-2): Tom Southern, Jimmy E. Campbell, Kyriakos I. Kourousis, Barry Mooney, Yuanbo T. Tang, and Trevor William Clyne. Indentation plastometry for study of anisotropy and inhomogeneity in maraging steel produced by laser powder bed fusion. steel research international, Mar 2023. URL: https://doi.org/10.1002/srin.202200881, doi:10.1002/srin.202200881. This article has 16 citations and is from a peer-reviewed journal.

14. (abdi2020materialallowablegeneration pages 9-11): Frank Abdi, Parviz Yavari, Vasyl Harik, and Cody Godines. Material allowable generation and am process parameters effect on porosity. Coatings, 10:625, Jun 2020. URL: https://doi.org/10.3390/coatings10070625, doi:10.3390/coatings10070625. This article has 10 citations.

15. (hintsala2018highthroughputnanoindentationfor pages 5-8): Eric D. Hintsala, Ude Hangen, and Douglas D. Stauffer. High-throughput nanoindentation for statistical and spatial property determination. JOM, 70:494-503, Feb 2018. URL: https://doi.org/10.1007/s11837-018-2752-0, doi:10.1007/s11837-018-2752-0. This article has 160 citations and is from a peer-reviewed journal.

16. (sekhar2018hardnessyield pages 3-6): Aluru Praveen Sekhar, Supriya Nandy, Kalyan Kumar Ray, and Debdulal Das. Hardness - yield strength relation of al-mg-si alloys. IOP Conference Series: Materials Science and Engineering, 338:012011, Mar 2018. URL: https://doi.org/10.1088/1757-899x/338/1/012011, doi:10.1088/1757-899x/338/1/012011. This article has 37 citations.

17. (sekhar2018hardnessyield pages 6-7): Aluru Praveen Sekhar, Supriya Nandy, Kalyan Kumar Ray, and Debdulal Das. Hardness - yield strength relation of al-mg-si alloys. IOP Conference Series: Materials Science and Engineering, 338:012011, Mar 2018. URL: https://doi.org/10.1088/1757-899x/338/1/012011, doi:10.1088/1757-899x/338/1/012011. This article has 37 citations.

18. (rodrıguez2003correlationbetweennanoindentation pages 4-5): R Rodrıguez and I Gutierrez. Correlation between nanoindentation and tensile propertiesinfluence of the indentation size effect. Materials Science and Engineering A, 361(1-2):377-384, Nov 2003. URL: https://doi.org/10.1016/s0921-5093(03)00563-x, doi:10.1016/s0921-5093(03)00563-x. This article has 359 citations.

19. (rodrıguez2003correlationbetweennanoindentation pages 1-2): R Rodrıguez and I Gutierrez. Correlation between nanoindentation and tensile propertiesinfluence of the indentation size effect. Materials Science and Engineering A, 361(1-2):377-384, Nov 2003. URL: https://doi.org/10.1016/s0921-5093(03)00563-x, doi:10.1016/s0921-5093(03)00563-x. This article has 359 citations.

20. (fujisawa2016amethodfor pages 4-4): Naoki Fujisawa, Tomo Ogura, and Akio Hirose. A method for studying the nano-scale stress-strain response of a material by nanoindentation. Materials Transactions, 57:1006-1009, Apr 2016. URL: https://doi.org/10.2320/matertrans.m2015459, doi:10.2320/matertrans.m2015459. This article has 2 citations and is from a peer-reviewed journal.

21. (holroyd2023environmentinducedcrackingof pages 29-30): N.J. Henry Holroyd, Tim L. Burnett, John J. Lewandowski, and Geoffrey M. Scamans. Environment-induced cracking of high-strength al-zn-mg-cu aluminum alloys: past, present, and future. Corrosion, 79:48-71, Oct 2022. URL: https://doi.org/10.5006/4149, doi:10.5006/4149. This article has 51 citations and is from a peer-reviewed journal.

22. (holroyd2023environmentinducedcrackingof pages 16-16): N.J. Henry Holroyd, Tim L. Burnett, John J. Lewandowski, and Geoffrey M. Scamans. Environment-induced cracking of high-strength al-zn-mg-cu aluminum alloys: past, present, and future. Corrosion, 79:48-71, Oct 2022. URL: https://doi.org/10.5006/4149, doi:10.5006/4149. This article has 51 citations and is from a peer-reviewed journal.

23. (holroyd2023environmentinducedcrackingof pages 15-16): N.J. Henry Holroyd, Tim L. Burnett, John J. Lewandowski, and Geoffrey M. Scamans. Environment-induced cracking of high-strength al-zn-mg-cu aluminum alloys: past, present, and future. Corrosion, 79:48-71, Oct 2022. URL: https://doi.org/10.5006/4149, doi:10.5006/4149. This article has 51 citations and is from a peer-reviewed journal.

24. (zhao2006exfoliationcorrosionkinetics pages 39-43): X Zhao. Exfoliation corrosion kinetics of high strength aluminum alloys. Unknown journal, 2006.

25. (glendening2020nasasplansfor pages 11-19): A Glendening and R Russell. Nasa's plans for development of standards for additive manufactured components. Unknown journal, 2020.

26. (kimbrel2026whitepaperdiscussion pages 7-12): B Kimbrel, M Chytka, J Muhammad, T Poe, and D Andreev. White paper discussion on potential approaches for augmenting nasa-std-6030 framework for in-space manufacturing. Unknown journal, 2026.

27. (park2022nasasapproachto pages 12-22): A Park, M James, RW Russell, and BM West. Nasa's approach to additive manufacturing certification: methodologies for qualification of additively manufactured aerospace hardware. Unknown journal, 2022.

28. (prater2016summaryreportfor pages 49-51): TJ Prater, QA Bean, NJ Werkheiser, and MM Johnston. Summary report for the technical interchange meeting on development of baseline material properties and design guidelines for in-space manufacturing activities. Unknown journal, 2016.

29. (prater2016summaryreportfor pages 51-53): TJ Prater, QA Bean, NJ Werkheiser, and MM Johnston. Summary report for the technical interchange meeting on development of baseline material properties and design guidelines for in-space manufacturing activities. Unknown journal, 2016.

30. (gunasegaram2026modelbasedinsitu pages 13-16): Dayalan Gunasegaram, Tarasankar DebRoy, Paul Greenway, Griffin Keller, Craig Brice, Amanda Barnard, and Manyalibo Matthews. Model-based, <i>in-situ</i> , non-destructive qualification and certification of parts made by autonomous additive manufacturing. Journal of Physics: Materials, 9:031002, Aug 2026. URL: https://doi.org/10.1088/2515-7639/ae9228, doi:10.1088/2515-7639/ae9228. This article has 0 citations.

31. (prater2016summaryreportfor pages 57-59): TJ Prater, QA Bean, NJ Werkheiser, and MM Johnston. Summary report for the technical interchange meeting on development of baseline material properties and design guidelines for in-space manufacturing activities. Unknown journal, 2016.

32. (afroz2025fatiguelifeof pages 1-2): L. Afroz, M. Qian, J. Forsmark, Y. Li, M. Easton, and R. Das. Fatigue life of laser powder bed fusion (l-pbf) alsi10mg alloy: effects of surface roughness and porosity. Progress in Additive Manufacturing, Aug 2024. URL: https://doi.org/10.1007/s40964-024-00759-x, doi:10.1007/s40964-024-00759-x. This article has 53 citations and is from a peer-reviewed journal.

33. (kan2022acriticalreview pages 20-21): Wen Hao Kan, Louis Ngai Sam Chiu, Chao Voon Samuel Lim, Yuman Zhu, Yang Tian, Derui Jiang, and Aijun Huang. A critical review on the effects of process-induced porosity on the mechanical properties of alloys fabricated by laser powder bed fusion. Journal of Materials Science, 57:9818-9865, Mar 2022. URL: https://doi.org/10.1007/s10853-022-06990-7, doi:10.1007/s10853-022-06990-7. This article has 422 citations and is from a peer-reviewed journal.

34. (kan2022acriticalreview pages 18-20): Wen Hao Kan, Louis Ngai Sam Chiu, Chao Voon Samuel Lim, Yuman Zhu, Yang Tian, Derui Jiang, and Aijun Huang. A critical review on the effects of process-induced porosity on the mechanical properties of alloys fabricated by laser powder bed fusion. Journal of Materials Science, 57:9818-9865, Mar 2022. URL: https://doi.org/10.1007/s10853-022-06990-7, doi:10.1007/s10853-022-06990-7. This article has 422 citations and is from a peer-reviewed journal.

35. (cannon2026evaluationofthe pages 1-2): Liam Cannon, Karl Peter Davidson, and Md Zakaria Quadir. Evaluation of the small punch test: repeatability and sample parameter influence. Journal of Materials Engineering and Performance, 35:40778-40788, Jul 2026. URL: https://doi.org/10.1007/s11665-026-14603-6, doi:10.1007/s11665-026-14603-6. This article has 0 citations and is from a peer-reviewed journal.

36. (brown2020finiteelementmodelling pages 63-68): V Brown. Finite element modelling of the small punch test for structure critical design. Unknown journal, 2020.

37. (torres2021mechanicsofthe pages 3-5): Jonathan Torres and Ali P. Gordon. Mechanics of the small punch test: a review and qualification of additive manufacturing materials. Journal of Materials Science, 56:10707-10744, Mar 2021. URL: https://doi.org/10.1007/s10853-021-05929-8, doi:10.1007/s10853-021-05929-8. This article has 97 citations and is from a peer-reviewed journal.

38. (lucon2021smallpunchtesting pages 13-14): Enrico Lucon, Jake T. Benzing, Nicholas Derimow, and Nik Hrabe. Small punch testing to estimate the tensile and fracture properties of additively manufactured ti-6al-4v. Journal of Materials Engineering and Performance, 30:5039-5049, Mar 2021. URL: https://doi.org/10.1007/s11665-021-05603-9, doi:10.1007/s11665-021-05603-9. This article has 45 citations and is from a peer-reviewed journal.

39. (campbell2022indentationplastometryof pages 1-1): Jimmy E Campbell, Marcus Gaiser-Porter, Wenchen Gu, Steve Ooi, Max Burley, James Dean, and Trevor William Clyne. Indentation plastometry of very hard metals. Feb 2022. URL: https://doi.org/10.1002/adem.202101398, doi:10.1002/adem.202101398. This article has 34 citations and is from a peer-reviewed journal.

40. (reiffmusgrove2023indentationplastometryof pages 2-2): Rebecca Reiff-Musgrove, Marcus Gaiser-Porter, Wenchen Gu, Jimmy E. Campbell, Peter Lewis, Andreas Frehn, Andrew D. Tarrant, Yuanbo T. Tang, Max Burley, and Trevor William Clyne. Indentation plastometry of particulate metal matrix composites, highlighting effects of microstructural scale. Advanced Engineering Materials, Jan 2023. URL: https://doi.org/10.1002/adem.202201479, doi:10.1002/adem.202201479. This article has 16 citations and is from a peer-reviewed journal.

41. (gu2022indentationplastometryof pages 1-1): Wenchen Gu, Jimmy Campbell, Yuanbo Tang, Hamed Safaie, Richard Johnston, Yuchen Gu, Cameron Pleydell-Pearce, Max Burley, James Dean, and Trevor William Clyne. Indentation plastometry of welds. Advanced Engineering Materials, Feb 2022. URL: https://doi.org/10.1002/adem.202101645, doi:10.1002/adem.202101645. This article has 34 citations and is from a peer-reviewed journal.

42. (southern2023indentationplastometryfor pages 2-2): Tom Southern, Jimmy E. Campbell, Kyriakos I. Kourousis, Barry Mooney, Yuanbo T. Tang, and Trevor William Clyne. Indentation plastometry for study of anisotropy and inhomogeneity in maraging steel produced by laser powder bed fusion. steel research international, Mar 2023. URL: https://doi.org/10.1002/srin.202200881, doi:10.1002/srin.202200881. This article has 16 citations and is from a peer-reviewed journal.

43. (jayaram2022smallscalemechanicaltesting pages 12-13): Vikram Jayaram. Small-scale mechanical testing. Annual Review of Materials Research, 52:473-523, Jul 2022. URL: https://doi.org/10.1146/annurev-matsci-080819-123640, doi:10.1146/annurev-matsci-080819-123640. This article has 41 citations and is from a domain leading peer-reviewed journal.

44. (hoefler2025automatedsystemfor pages 10-11): Thomas Hoefler, Ayako Ikeda, Toshio Osada, Toru Hara, Kyoko Kawagishi, and Takahito Ohmura. Automated system for high-throughput process-structure-property dataset generation of structural materials: a γ/γ′ superalloy case study. Aug 2025. URL: https://doi.org/10.1016/j.matdes.2025.114279, doi:10.1016/j.matdes.2025.114279. This article has 11 citations and is from a highest quality peer-reviewed journal.

45. (vecchio2021highthroughputrapidexperimental pages 4-7): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 107 citations and is from a highest quality peer-reviewed journal.

46. (vecchio2021highthroughputrapidexperimental pages 33-50): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 107 citations and is from a highest quality peer-reviewed journal.

47. (zhang2017combinatorialapproachesfor pages 7-9): Xiaokun Zhang and Yong Xiang. Combinatorial approaches for high-throughput characterization of mechanical properties. Journal of Materiomics, 3:209-220, Sep 2017. URL: https://doi.org/10.1016/j.jmat.2017.07.002, doi:10.1016/j.jmat.2017.07.002. This article has 54 citations.

48. (zhang2017combinatorialapproachesfor pages 5-7): Xiaokun Zhang and Yong Xiang. Combinatorial approaches for high-throughput characterization of mechanical properties. Journal of Materiomics, 3:209-220, Sep 2017. URL: https://doi.org/10.1016/j.jmat.2017.07.002, doi:10.1016/j.jmat.2017.07.002. This article has 54 citations.

49. (zhang2017combinatorialapproachesfor pages 9-10): Xiaokun Zhang and Yong Xiang. Combinatorial approaches for high-throughput characterization of mechanical properties. Journal of Materiomics, 3:209-220, Sep 2017. URL: https://doi.org/10.1016/j.jmat.2017.07.002, doi:10.1016/j.jmat.2017.07.002. This article has 54 citations.
