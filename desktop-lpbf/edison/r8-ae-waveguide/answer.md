Question: Context: we are designing a lab-built desktop laser powder bed fusion (LPBF) machine for small-batch screening of aluminium alloys (AlSi10Mg, 6061, 7075 and grain-refined variants with Zr, Sc or TiB2). Laser: 500 W single-mode CW fibre laser at 1070 nm (IPG YLR-500 class) into a SCANLAB basiCube 20 galvo (marking speed up to about 1.1 m/s at f = 160 mm) and a Thorlabs FTH160-1064 f-theta lens (f = 160 mm), giving a ~96 um 1/e2 spot diameter (48-75 um spots are options). Expected process window: 200-350 W, 0.4-1.1 m/s, 30 um layers, ~0.1 mm hatch. Build plates are 25, 50 or 75 mm across, heated to 200 C (500 C reserved). Chamber: ~280 x 190 x 120 mm inside, vacuum-purged then argon at +5 to +20 mbar, with an argon cross-flow of 2.5-3.3 m/s over the plate (140-200 L/min) from a slot nozzle on the back wall to an outlet slot at the front; a cover slide sits under a lid window ~130 mm above the plate.

We want acoustic emission (AE) monitoring of cracking during LPBF of crack-prone aluminium alloys (6061, 7075). The build plate (25-75 mm across, 6061) sits on graphite foil on a heater block (200 C, up to 500 C later) that stands on three Macor ceramic standoffs on a piston with a hollow rod; the piston slides in a bore sealed by an O-ring, and the module is swapped often.

1. AE in LPBF: which papers detected cracking (hot or cold) with structure-borne AE; sensor types and models, frequency bands, sampling rates, preamp gains and thresholds; how they told crack signals from recoater, gas-flow and pump noise. Any for Al alloys besides Seleznev et al. 2022?
2. Mounting through a heated, multi-interface stack: transmission loss across dry or bolted contacts, graphite foil and ceramic standoffs; typical dB loss per interface at 100-500 kHz; how contact pressure and couplants (high-temperature grease, gold or aluminium foil) change it.
3. Waveguides for high-temperature AE: rod diameter, material, length, tip and contact design, spring force, dispersion (Pochhammer-Chree modes) and attenuation at 100-500 kHz; published designs (welding, nuclear, LPBF heated plates) and how much signal they lose against direct mounting.
4. High-temperature AE sensors (MISTRAS/PAC D9215, Vallen VS-HT series, KRN and others): temperature ratings and sensitivities; whether a sensor can sit on a 200 C plate.
5. Calibration: Hsu-Nielsen pencil-lead breaks, path-loss measurement, and how often a removable plate's acoustic coupling should be re-checked.
6. Signal processing used to place cracks in time and layer: waveform features, clustering, machine learning; false-alarm rates where reported.

Give quantitative values and sources.

# Acoustic Emission Monitoring of Cracking During LPBF of Aluminium Alloys: A Comprehensive Technical Review

## 1. AE Detection of Cracking in LPBF

### 1.1 Confirmed Crack Detection Studies

The most direct demonstration of structure-borne AE crack detection in LPBF is the work of Seleznev et al. (2022) on a high-strength Al₉₂Mn₆Ce₂ alloy. They used a Physical Acoustics (PAC/MISTRAS) D9215 broadband high-temperature sensor coupled directly to the underside of the build plate with Molykote 41 high-temperature grease. The signal chain comprised a 40 dB low-noise preamplifier, a 50–600 kHz band-pass filter, and an 18-bit PAC PCI-2 acquisition board sampling at 2 MHz. The detection threshold was set individually before each build at approximately 90–100 dB, just above the measured background-noise amplitude. Crack-related AE signals exhibited a triangular waveform with an immediate peak rise and a gradual decay over 1–3 ms, with peak power spectral density at approximately 100 kHz and significant energy content extending to 500 kHz. All observed cracks were confirmed by post-build micro-computed tomography (μ-CT), and the temporal correspondence between AE events and μ-CT-identified crack locations was established by synchronizing both datasets to the machine log file (seleznev2022insitudetection pages 2-3, seleznev2022insitudetection pages 3-5, seleznev2022insitudetection pages 5-7).

Critically, Seleznev et al. found that cracking could be delayed: some cracks formed 5–65 minutes after the corresponding layer was manufactured, and several appeared only after the build was completed during the cooling phase, underscoring the need for post-build AE monitoring as well (seleznev2022insitudetection pages 5-7). This is the only published study that explicitly detected and ground-truthed cracking in an aluminium alloy using structure-borne AE during LPBF.

### 1.2 Other LPBF AE Monitoring Studies

Richter et al. (2025) deployed a dual-sensor system combining an airborne Avisoft Bioacoustics CM16/CMPA48AAF-5V microphone (2–200 kHz) and a structure-borne Vallen VS370-A3 piezoelectric sensor (150–600 kHz) beneath the build plate, acquired synchronously at 1.25 MHz via an Elsys TPCE-8S DAQ. They reported that the structure-borne sensor was superior for detecting "secondary process emissions" interpreted as cracking or delamination—broadband events occurring while the laser was off—and achieved approximately 99% process-state classification accuracy using a CNN on spectrogram windows (richter2025finedetectionof pages 1-3, richter2025finedetectionof pages 3-5, richter2025finedetectionof pages 5-7).

Jüngert et al. (2024) used four Vallen VS160-NS sensors (100–450 kHz, resonance 160 kHz, rated to 180 °C) with a Vallen AMSY-6 system. Sensors were initially hot-glued to the build plate (one sensor's glue failed as the chamber heated), and subsequently mounted in spring-loaded cylindrical recesses with temperature-resistant gel. Process-generated AE amplitudes reached approximately 70 dB. This was a feasibility study; pores and cracks were hypothesized to produce additional emissions distinct from the normal print pattern, but individual crack events were not independently validated (jungert2024acousticemissionmonitoring pages 1-3, jungert2024acousticemissionmonitoring pages 3-8).

Pandiyan et al. (2023) employed an Avisoft CM16/CMPA airborne microphone at 400 kHz sampling, triggered by a photodiode, to classify LPBF process regimes (lack-of-fusion, conduction, keyhole) in 316L using CNN, XGBoost, and SVM approaches (pandiyan2023optimizinginsitumonitoring pages 3-4, pandiyan2023optimizinginsitumonitoring pages 4-5). Shevchik et al. (2018) used a fiber Bragg grating (FBG) sensor at 10 MHz (downsampled to 1 MHz) with a spectral CNN for quality classification in 316L (shevchik2018acousticemissionfor pages 5-7). Both are general-regime classifiers rather than validated crack detectors. Beyond Seleznev et al. (2022), there is a 2023 follow-up by Kononenko et al. (cited in multiple reviews) that applied machine learning to AE crack detection during LPBF, referenced as building on the same experimental platform (chang2026areviewof pages 22-23, nobari2026mechanismssensorsand pages 9-11).

The following table summarizes the key LPBF AE monitoring studies:

| Reference | Material | Sensor type/model | Mounting | Frequency band | Sampling rate | Preamp gain | Threshold | Noise discrimination method | Key findings / crack status |
|---|---|---|---|---:|---:|---:|---:|---|---|
| Seleznev et al. (2022) | Al–92Mn–6Ce–2 | Structure-borne broadband high-temperature PAC/MISTRAS D9215 | Directly beneath build plate; Molykote 41 grease | 50–600 kHz filter; cracks peaked near 100 kHz with content to 500 kHz | 2 MHz, 18 bit | 40 dB | Approximately 90–100 dB, selected just above pre-build background; later analysis used energy ≈10⁴ V² | Recorded machine states separately before each build. Recoater/rake and most modules were insignificant; circulation pump raised noise from about 0.2 to 2 V. Stable pump noise was rejected by threshold; remaining bursts were separated using waveform, RMS, energy, skewness and kurtosis. | **Confirmed crack detection**, correlated with μCT and machine time. Crack hits showed immediate rise and 1–3 ms decay; delayed cracking occurred minutes to about one hour after layer manufacture or build completion. (seleznev2022insitudetection pages 2-3, seleznev2022insitudetection pages 3-5, seleznev2022insitudetection pages 5-7, seleznev2022insitudetection pages 7-7) |
| Richter et al. (2025) | 316L stainless steel | Structure-borne Vallen VS370-A3 plus airborne Avisoft CM16/CMPA48AAF-5V | VS370-A3 directly beneath plate; microphone above plate | Structure-borne 150–600 kHz; airborne 2–200 kHz | 1.25 MHz synchronous acquisition | Not reported | Not reported | Machine trigger separated process states; emissions were divided into primary events during laser operation and secondary substrate events while the laser was off. CNN used 8 ms spectrogram windows. | **Detected secondary broadband emissions interpreted as cracking or delamination, but individual cracks were not independently ground-truthed.** Structure-borne channel was superior for these events; process-state accuracy was ≈99.0% structure-borne, 98.2% airborne and 99.1% combined. (richter2025finedetectionof pages 1-3, richter2025finedetectionof pages 3-5, richter2025finedetectionof pages 5-7) |
| Jüngert et al. (2024) | Metal LPBF specimens; alloy not stated in retrieved excerpt | Four Vallen VS160-NS sensors with Vallen preamplifiers and AMSY-6 system | Under build plate; initially hot glue, then cylindrical recesses with temperature-resistant gel and spring loading | 100–450 kHz; resonance 160 kHz | Not reported | Not reported | Not reported | Initial characterization recorded normal process and machine sources, including powder recoating. Multi-channel/layer timing was used to associate events with process phases. | **Feasibility study, not validated crack detection.** Process emissions reached about 70 dB; pores and cracks were hypothesized to add distinct events. Hot glue failed thermally; spring-loaded gel coupling was more robust. Sensor rating was 180 °C. (jungert2024acousticemissionmonitoring pages 1-3, jungert2024acousticemissionmonitoring pages 3-8) |
| Pandiyan et al. (2023) | 316L stainless steel | Airborne Avisoft CM16/CMPA microphone | About 120 mm from process zone at 45°; bronze mesh spatter guard | Nominally 0–150 kHz | 400 kHz | Not reported | Acquisition triggered by photodiode at 0.5 V; no AE crack threshold reported | Photodiode synchronized AE to individual laser tracks. Periodograms, empirical-mode decomposition, CNN, XGBoost and SVM, with saliency/SHAP analysis, classified process regimes. | **Not a demonstrated crack detector.** Classified lack-of-fusion, conduction and keyhole-related process conditions/general anomalies rather than individually validated crack events. (pandiyan2023optimizinginsitumonitoring pages 3-4, pandiyan2023optimizinginsitumonitoring pages 4-5) |
| Shevchik et al. (2018) | 316L stainless steel | Airborne fiber-Bragg-grating optical AE sensor | Inside chamber, approximately 200 mm from process zone, supported on chamber wall | Conventional acoustic passband not reported; FBG centered at 1547 nm with ±1 nm optical reflection band | 10 MHz, downsampled to 1 MHz | Not applicable/not reported | No hit threshold reported | Acquisition synchronized to laser exposure, allowing recoater intervals between layers to be excluded; spectral CNN analyzed acoustic signatures. | **Not a direct crack-detection validation.** Demonstrated in-situ classification of LPBF quality/process regimes, principally defect/porosity-related signatures. (shevchik2018acousticemissionfor pages 5-7) |


*Table: Comparison of representative LPBF acoustic-monitoring studies, separating confirmed crack detection from inferred secondary emissions and general process/defect classification. “Not reported” means the parameter was absent from the retrieved publication text.*

### 1.3 Noise Discrimination

The principal noise source identified in LPBF AE monitoring is the inert-gas circulation pump, which raised the noise amplitude approximately 10-fold (from about 0.2 V to 2 V) in the Seleznev et al. experiments (seleznev2022insitudetection pages 2-3, seleznev2022insitudetection pages 3-5). Most of this stable pump noise was suppressed by the fixed amplitude threshold. The recoater/powder rake and other machine modules did not significantly influence the AE signal in the 50–600 kHz band (seleznev2022insitudetection pages 3-5). Noise signals fell into three distinct waveform types (continuous bursts, single bursts, and hardware-switcher bursts), all of which occurred independently of the AM process and could thus be recognized by their presence during setup periods (seleznev2022insitudetection pages 3-5). Richter et al. separated primary emissions (during laser activity) from secondary emissions (laser off) using a machine trigger signal, effectively time-gating the crack-sensitive channel (richter2025finedetectionof pages 3-5). Jüngert et al. performed an initial characterization step recording each machine function separately to build a noise baseline (jungert2024acousticemissionmonitoring pages 1-3).

## 2. Transmission Loss Through a Multi-Interface Heated Stack

### 2.1 Couplant Attenuation

Xu et al. (2024) systematically measured the frequency-dependent transfer function of four couplant materials (acrylic adhesive pads, hot glue, honey, and vaseline) for a Vallen VS30-V piezoelectric sensor on a steel block from 50 kHz to 1 MHz. The couplant-only attenuation was generally less than 5 dB across the entire frequency range (xu2024frequencydependentamplitude pages 5-6, xu2024frequencydependentamplitude pages 6-9). Acrylic adhesive pads exhibited the best repeatability (mean relative standard deviation 9.7% at 50–100 kHz), while vaseline exceeded 30% RSD over most of the band (xu2024frequencydependentamplitude pages 5-6). Below 500 kHz, most couplants are generally adequate for AE transmission (brunner2021structuralhealthand pages 5-6).

### 2.2 Contact Pressure Effects

For high-temperature ultrasonic transducer stacks, Milani (2022) demonstrated that initial deformation of 50 µm silver foil interlayers closed interfacial gaps, allowing the contact load to be reduced from approximately 12 kN (150 MPa) to 2 kN (25 MPa) without significant loss in transmission. Belleville springs were used to maintain approximately 500 N per bolt at temperature, with room-temperature preloads increased to 767 N per bolt to compensate for thermal expansion and relaxation at 650 °C (milani2022designandmanufacturinga pages 28-33).

### 2.3 Implications for the User's Stack

The user's stack comprises: build plate → graphite foil → heater block → Macor ceramic standoffs → piston. Each dry or lightly coupled interface introduces transmission loss. Macor glass-ceramic has an acoustic impedance of approximately 11–13 MRayl (versus ~17 MRayl for aluminium and ~46 MRayl for steel), resulting in a theoretical reflection coefficient at an Al/Macor interface of approximately 0.13–0.20, corresponding to a transmission loss on the order of 1–2 dB per well-coupled interface. Graphite foil (acoustic impedance ~3–5 MRayl depending on density and compression) creates a larger mismatch with aluminium, potentially 3–6 dB per interface if loosely clamped. Each dry metal-to-metal contact without couplant may add 3–10+ dB of loss at 100–500 kHz depending on surface roughness, flatness, and clamping pressure—rough or low-pressure contacts can attenuate signals by 10–20 dB or more. The total cumulative path loss through the full stack (build plate → graphite foil → heater → Macor → piston) could easily reach 15–30+ dB, which would likely bury crack signals in noise. This strongly favors sensing directly on or immediately beneath the build plate rather than through the full stack.

## 3. Waveguides for High-Temperature AE

The following table summarizes published waveguide design parameters:

| Parameter | Recommended values / design implications | Source |
|---|---|---|
| Rod diameter | **0.8–3.0 mm** is the published practical range for informative AE transmission in rod/wire guides. A **1.59 mm** diameter was experimentally/model validated; increasing diameter raised the A0 amplitude, which approached saturation near **4.77 mm**, while 1.59 mm matched the sensor tip and preserved S0 response. | Zakharov et al. (2010); Zelenyak et al. (2015) (zakharov2010acousticemissionsignal pages 1-5, zelenyak2015modelingofacoustic pages 11-15) |
| Material | Prefer **stainless/carbon steel** for strength and weldability or **alumina** for electrical/thermal isolation. In an aluminium-plate model, steel and alumina had approximately **3.5 dB relative reduction**, brass about **5 dB**, and aluminium about **10 dB**; impedance matching and temperature-dependent properties must be considered. | Zelenyak et al. (2015); Kazys and Vaskeliene (2021) (zelenyak2015modelingofacoustic pages 15-18, zelenyak2015modelingofacoustic pages 11-15, kazys2021hightemperatureultrasonic pages 7-9, kazys2021hightemperatureultrasonic pages 9-11) |
| Length | Use the shortest length that keeps the sensor cool and separates early reflections: approximately **100–300 mm** for a 200 °C plate; up to **700 mm** for much hotter sources. Published examples include **145 mm**, **276–306 mm**, **600 mm**, and **700 mm**. Each additional **76.5 mm** produced about **15 µs** arrival delay in one model, but little change in the relative FFT spectrum. | Zelenyak et al. (2015); Kazys and Vaskeliene (2021) (zelenyak2015modelingofacoustic pages 11-15, kazys2021hightemperatureultrasonic pages 7-9, kazys2021hightemperatureultrasonic pages 9-11) |
| Thermal reduction capability | A **145 mm** tapered stainless-steel or titanium rod reduced a **200 °C tip to about 50 °C** at the transducer. A **700 mm SS304** wire/strip guide reduced a **600 °C tip to about 26 °C**. Thermal performance depends strongly on diameter, convection, clamping and heat sinking. | Kazys and Vaskeliene (2021) (kazys2021hightemperatureultrasonic pages 7-9, kazys2021hightemperatureultrasonic pages 9-11) |
| Signal loss versus direct mounting | A **1.59 mm × 306 mm aluminium** waveguide produced approximately **13 dB amplitude loss** relative to direct mounting. Material comparisons showed aluminium around **10 dB** reduction versus about **3.5 dB** for steel/alumina; these values are geometry- and mode-dependent rather than universal per-unit-length attenuation constants. | Zelenyak et al. (2015) (zelenyak2015modelingofacoustic pages 1-4, zelenyak2015modelingofacoustic pages 11-15) |
| Hot-end tip/contact | Use a flat, polished tip normal to the plate for repeatable spring contact, or weld/braze the guide where permanence is acceptable. Published terminating concentrators include **stepwise, conical and exponential** profiles; the **exponential concentrator** was reported to minimize reflection and distortion when matching a thin rod to a larger sensor face. Hemispherical and inclined tips are specialized alternatives for focusing or mode conversion. | Zakharov et al. (2010); Kazys and Vaskeliene (2021) (zakharov2010acousticemissionsignal pages 1-5, kazys2021hightemperatureultrasonic pages 7-9) |
| Dispersion and modes | Cylindrical rods support multiple **Pochhammer–Chree longitudinal, flexural and torsional modes**; group velocity varies with frequency–diameter product, broadening an impulsive AE waveform and biasing arrival-time location. Thin rods limit the number of modes but can reduce amplitude. Zelenyak’s plate/rod system was dominated by **A0**, with S0 also identifiable; rectangular strips can support a less-dispersive SH mode. Calibrate using the actual guide, band and temperature. | Zakharov et al. (2010); Zelenyak et al. (2015); Kazys and Vaskeliene (2021) (zelenyak2015modelingofacoustic pages 15-18, zakharov2010acousticemissionsignal pages 1-5, zelenyak2015modelingofacoustic pages 11-15, kazys2021hightemperatureultrasonic pages 9-11) |
| Spring/contact force | A published spring-loaded acoustic coupler used **2–5 lbf (9–22 N)** at the rod tip. Treat this as a starting range: use a Belleville or coil spring to maintain constant load through thermal cycling, then optimize force by pencil-lead-break transfer measurements while checking that the guide does not indent or constrain the plate. | Jolly (1994) (jolly1994investigationofacoustic pages 6-10, jolly1994investigationofacoustic pages 10-12) |
| Practical starting design for a 200 °C LPBF plate | Start with a **1.5–2.0 mm diameter, 150–250 mm long 304/316 stainless-steel rod**, a polished flat hot tip, **10–20 N** spring preload, and a larger cool-end shoe/concentrator matched to the sensor. Expect roughly **5–15 dB** insertion loss and determine the actual 100–500 kHz transfer function after installation. | Engineering synthesis of the cited waveguide results (zelenyak2015modelingofacoustic pages 1-4, zakharov2010acousticemissionsignal pages 1-5, zelenyak2015modelingofacoustic pages 11-15, kazys2021hightemperatureultrasonic pages 7-9, jolly1994investigationofacoustic pages 6-10) |


*Table: Published dimensions, materials, thermal isolation, insertion loss, modal behavior and contact loading for high-temperature AE waveguides. The final row translates the evidence into a practical starting design for a 200 °C LPBF build plate.*

### 3.1 Key Design Principles

For AE waveguides, rod diameters of 0.8–3.0 mm are recommended for informative transmission (zakharov2010acousticemissionsignal pages 1-5). A 1.59 mm diameter UNS K12211 (iron alloy) waveguide, 306 mm long, produced approximately 13 dB amplitude reduction relative to direct sensor mounting on an aluminium plate (zelenyak2015modelingofacoustic pages 1-4). Material selection strongly affects transmission: steel and alumina waveguides showed only approximately 3.5 dB relative reduction, brass about 5 dB, and aluminium about 10 dB in the same FEM study (zelenyak2015modelingofacoustic pages 11-15). For a 500 °C temperature difference across the waveguide, signal shapes and amplitudes were essentially unchanged, with only a 1.65 µs arrival-time delay (zelenyak2015modelingofacoustic pages 15-18).

### 3.2 Dispersion

Finite cross-section rods support Pochhammer–Chree longitudinal, flexural, and torsional modes. Multiple modes can propagate simultaneously at a given frequency, causing dispersion that broadens the AE pulse and may affect source location accuracy (zakharov2010acousticemissionsignal pages 1-5). Rectangular-strip waveguides can support a non-dispersive shear-horizontal mode up to about 2 MHz, reducing pulse distortion (kazys2021hightemperatureultrasonic pages 9-11).

### 3.3 Thermal Isolation

A 145 mm tapered stainless-steel or titanium rod reduced a 200 °C tip temperature to approximately 50 °C at the sensor end (kazys2021hightemperatureultrasonic pages 7-9). A 700 mm SS304 wire (0.5 mm radius) reduced 600 °C to 26 °C (kazys2021hightemperatureultrasonic pages 9-11). For the user's 200 °C application, a 150–250 mm stainless-steel rod should suffice to bring the sensor end below 50 °C.

### 3.4 Concentrator Tips

When the waveguide diameter is smaller than the AE sensor face, a terminating concentrator is needed. Stepwise, conical, and exponential designs have been published; the exponential concentrator produces minimal distortion and reflection (zakharov2010acousticemissionsignal pages 1-5).

## 4. High-Temperature AE Sensors

### 4.1 Sensors Used in LPBF Studies

The PAC/MISTRAS D9215 is a broadband, high-temperature-rated structure-borne sensor that was used successfully at the bottom of an LPBF build plate with high-temperature grease coupling (seleznev2022insitudetection pages 2-3). The Vallen VS160-NS (100–450 kHz, resonance 160 kHz) is rated to 180 °C, making it marginal for a 200 °C plate without thermal management (jungert2024acousticemissionmonitoring pages 1-3). The Vallen VS370-A3 (150–600 kHz) was used beneath the build plate by Richter et al. (2025), though its temperature rating was not explicitly stated in the retrieved text (richter2025finedetectionof pages 1-3).

### 4.2 Temperature Considerations

Standard PZT ceramics have Curie temperatures in the range of 200–350 °C, so sensors based on soft PZT (e.g., PZT-5A, Tc ≈ 365 °C) can typically operate continuously at around 200 °C, though sensitivity may degrade and couplant/cable integrity must be maintained (shrout1993hightemperaturesensormicrophone pages 148-151). For 500 °C operation, bismuth titanate (Bi₄Ti₃O₁₂, Tc ≈ 685 °C) or lithium niobate (LiNbO₃, Tc ≈ 1150 °C) based sensors or sodium bismuth titanate (NBT) thick-film sensors are needed (shrout1993hightemperaturesensormicrophone pages 148-151). Buffer rod/waveguide designs allow conventional PZT sensors to be used for structures at 500 °C and beyond by keeping the sensor at a safe temperature (shrout1993hightemperaturesensormicrophone pages 148-151).

### 4.3 Practical Recommendation

For the user's 200 °C plate, a D9215-class high-temperature broadband sensor directly coupled to the build plate underside with high-temperature silicone grease (e.g., Molykote 41, rated to ~200 °C) is the simplest proven approach, as demonstrated by Seleznev et al. For the 500 °C reserved scenario, a stainless-steel waveguide with a cool-end conventional sensor is the standard solution.

## 5. Calibration

### 5.1 Hsu-Nielsen Pencil-Lead Break (PLB)

The Hsu-Nielsen source (ASTM E976) uses a 0.5 mm diameter, 2H pencil lead extended 2.5 mm from the tip and held at 45° to the test surface. When the lead fractures under the gradually applied bending load, it releases a broadband step-unload impulse into the structure (jolly1994investigationofacoustic pages 1-6, jolly1994investigationofacoustic pages 10-12). Burns (2012) reported a mean PLB amplitude of 80.7 dB_AE with a standard deviation of 2.7 dB_AE from 30 breaks on an aluminium plate, within the ±3 dB_AE repeatability criterion of ASTM E976 (burns2012developmentandcharacterisation pages 170-174). Hinrichs et al. (2024) found PLB relative standard deviation of 15–40% across a broad frequency range above 60 kHz, noting that ball impacts and electromagnetic actuators had lower RSD below 40–60 kHz but higher RSD at higher frequencies (hinrichs2024analysisofthe pages 1-3).

### 5.2 Path-Loss Measurement

Path loss is measured by performing PLBs at multiple known distances from the sensor and plotting peak amplitude versus distance. The slope gives the attenuation coefficient in dB/mm at the dominant frequency. For the user's small plates (25–75 mm), geometric spreading and edge reflections will dominate, so a grid of PLB positions covering the plate area is more informative than a simple line attenuation measurement.

### 5.3 Coupling Verification for Removable Plates

For the user's frequently swapped build-plate modules, coupling should be re-verified before every build. The procedure is: (1) mount the plate and sensor assembly; (2) perform a minimum of 5–10 PLBs at fixed, marked positions on the plate top surface; (3) record peak amplitude, rise time, and frequency content; (4) compare with the reference baseline established during the initial calibration. Per ASTM E976 and standard practice, amplitudes should reproduce within ±3 dB (burns2012developmentandcharacterisation pages 170-174, hinrichs2024analysisofthe pages 1-3). Burns (2012) demonstrated that five removal/remounting cycles with ten PLBs at each location provided a robust assessment of coupling reproducibility (burns2012developmentandcharacterisation pages 115-120). The spring-loaded sensor mounting used by Jüngert et al. (temperature-resistant gel in a cylindrical recess) is a practical model for a removable-plate system, as it avoids the coupling failures observed with hot glue at elevated temperatures (jungert2024acousticemissionmonitoring pages 3-8, jungert2024acousticemissionmonitoring pages 1-3).

## 6. Signal Processing for Crack Identification

### 6.1 Waveform Features

Seleznev et al. (2022) identified three time-domain statistical features that effectively separated crack signals from noise (seleznev2022insitudetection pages 5-7):
- **RMS**: Noise signals had RMS below 0.4 V; most crack signals had higher RMS, following the basic AE energy–defect size relationship.
- **Skewness**: Crack signals clustered tightly between −0.4 and +0.5.
- **Kurtosis**: Crack signals ranged from 0 to 15, while noise typically had higher kurtosis due to their peaked/bursty nature.

An energy threshold of 10⁴ V² effectively suppressed most noise while preserving the principal crack signals detected by μ-CT. However, some crack signals with SNR < 1 were missed, and not all μ-CT cracks produced individually resolvable AE events (e.g., triple crack #2 in Build Job 2 produced only one AE event) (seleznev2022insitudetection pages 5-7).

### 6.2 Machine Learning Approaches

Multiple ML methods have been applied to AE-based LPBF monitoring (chang2026areviewof pages 22-23, nobari2026mechanismssensorsand pages 9-11, chang2026areviewof pages 16-19):
- **Spectral CNNs** (Shevchik et al., 2018): classification of process quality regimes from wavelet spectrograms.
- **VAE and GAN** (Pandiyan et al., 2021): semi-supervised anomaly detection achieving 96–97% accuracy for identifying defect-free vs. anomalous regimes (chang2026areviewof pages 22-23).
- **CNN on spectrograms** (Richter et al., 2025): approximately 99% process-state classification accuracy; the structure-borne channel was slightly more accurate (~99.0%) than the airborne channel (~98.2%) (richter2025finedetectionof pages 5-7).
- **K-means clustering with PCA** has been used for unsupervised defect classification in DED, grouping crack signals by short duration, high amplitude, and high energy (nobari2026mechanismssensorsand pages 11-12).
- **STFT, CWT, and HPSS** are used for time-frequency analysis and denoising of AE signals (nobari2026mechanismssensorsand pages 9-11).
- For crack detection specifically, the **Welch method** was reported for power spectral estimation (chang2026areviewof pages 22-23).

### 6.3 Layer and Temporal Assignment

Crack signals can be assigned to specific layers by synchronizing AE timestamps with the machine log file, which records the start and end time of each layer. Seleznev et al. demonstrated this by plotting AE events on the build timeline and correlating them with μ-CT crack heights, finding delays of minutes to over an hour between layer deposition and crack formation (seleznev2022insitudetection pages 3-5, seleznev2022insitudetection pages 5-7). Richter et al. used a machine trigger to separate laser-on and laser-off intervals, assigning secondary emissions to inter-layer cooling periods (richter2025finedetectionof pages 3-5).

### 6.4 False-Alarm Rates

No study in the retrieved literature reported explicit false-alarm rates (false positive rates) for AE crack detection in LPBF. Seleznev et al. noted that some pump-noise bursts exceeded the threshold and would constitute false alarms without additional waveform classification; they recommended either physically isolating the pump or implementing threshold-free monitoring with ML classification as a future goal (seleznev2022insitudetection pages 5-7). The semi-supervised approaches of Pandiyan et al. (2021) reported 96–97% accuracy for anomaly detection but did not decompose this into precision and recall for cracks specifically (chang2026areviewof pages 22-23). This remains an open area requiring further work, particularly for crack-prone aluminium alloys where the number of genuine crack events may be small relative to noise events.

## Summary and Recommendations for the User's System

For the described lab-built LPBF machine targeting crack-prone 6061 and 7075 aluminium alloys:

1. **Sensor selection**: A MISTRAS/PAC D9215 or equivalent broadband high-temperature sensor (50–600 kHz) mounted directly beneath the build plate is the proven configuration for crack AE at 200 °C. The Vallen VS160-NS (rated 180 °C) is a viable alternative if thermally managed.

2. **Mounting**: Couple the sensor to the build plate underside using high-temperature silicone grease (Molykote 41 or equivalent). A spring-loaded recess in the plate is recommended for removability and thermal robustness, following the Jüngert et al. design. Avoid routing the AE signal through the full graphite-foil/heater/Macor/piston stack, as cumulative interface losses could exceed 15–30 dB.

3. **Acquisition**: Sample at ≥2 MHz, 18-bit, with 40 dB preamplifier gain and a 50–600 kHz band-pass filter. Set the threshold just above the background with the gas system running (expect the argon circulation pump to be the dominant noise source).

4. **Waveguide option**: For the 500 °C reserved scenario, a 1.5–2 mm diameter, 150–250 mm long 304/316 stainless-steel rod with a polished flat tip, 10–20 N spring preload, and an exponential concentrator at the cool end is a practical starting design, with an expected insertion loss of 5–15 dB.

5. **Calibration**: Perform Hsu-Nielsen PLBs (0.5 mm 2H lead, 2.5 mm extension, 45°) at 5–10 fixed positions before every build. Compare peak amplitudes to a reference baseline within ±3 dB to verify coupling.

6. **Signal processing**: Use waveform shape (triangular, 1–3 ms decay), RMS, skewness (−0.4 to 0.5), and kurtosis (0–15) for initial crack/noise separation. Synchronize AE timestamps to the layer log. Continue monitoring for at least one hour after build completion to capture delayed cracking. For automated classification, CNN-based approaches on spectrograms have achieved approximately 99% accuracy for process-state discrimination.

References

1. (seleznev2022insitudetection pages 2-3): Mikhail Seleznev, Tobias Gustmann, Judith Miriam Friebel, Urs Alexander Peuker, Uta Kühn, Julia Kristin Hufenbach, Horst Biermann, and Anja Weidner. In situ detection of cracks during laser powder bed fusion using acoustic emission monitoring. Additive Manufacturing Letters, 3:100099, Dec 2022. URL: https://doi.org/10.1016/j.addlet.2022.100099, doi:10.1016/j.addlet.2022.100099. This article has 58 citations and is from a peer-reviewed journal.

2. (seleznev2022insitudetection pages 3-5): Mikhail Seleznev, Tobias Gustmann, Judith Miriam Friebel, Urs Alexander Peuker, Uta Kühn, Julia Kristin Hufenbach, Horst Biermann, and Anja Weidner. In situ detection of cracks during laser powder bed fusion using acoustic emission monitoring. Additive Manufacturing Letters, 3:100099, Dec 2022. URL: https://doi.org/10.1016/j.addlet.2022.100099, doi:10.1016/j.addlet.2022.100099. This article has 58 citations and is from a peer-reviewed journal.

3. (seleznev2022insitudetection pages 5-7): Mikhail Seleznev, Tobias Gustmann, Judith Miriam Friebel, Urs Alexander Peuker, Uta Kühn, Julia Kristin Hufenbach, Horst Biermann, and Anja Weidner. In situ detection of cracks during laser powder bed fusion using acoustic emission monitoring. Additive Manufacturing Letters, 3:100099, Dec 2022. URL: https://doi.org/10.1016/j.addlet.2022.100099, doi:10.1016/j.addlet.2022.100099. This article has 58 citations and is from a peer-reviewed journal.

4. (richter2025finedetectionof pages 1-3): Roland Axel Richter, Jamasp Jhabvala, Nicolas Mari, Roland Logé, and Elia Iseli. Fine detection of process state and secondary process emissions in laser powder-bed fusion (lpbf) by dual acoustic sensor acquisition and machine learning. IOP Conference Series: Materials Science and Engineering, 1332(1):012032, Aug 2025. URL: https://doi.org/10.1088/1757-899x/1332/1/012032, doi:10.1088/1757-899x/1332/1/012032. This article has 2 citations.

5. (richter2025finedetectionof pages 3-5): Roland Axel Richter, Jamasp Jhabvala, Nicolas Mari, Roland Logé, and Elia Iseli. Fine detection of process state and secondary process emissions in laser powder-bed fusion (lpbf) by dual acoustic sensor acquisition and machine learning. IOP Conference Series: Materials Science and Engineering, 1332(1):012032, Aug 2025. URL: https://doi.org/10.1088/1757-899x/1332/1/012032, doi:10.1088/1757-899x/1332/1/012032. This article has 2 citations.

6. (richter2025finedetectionof pages 5-7): Roland Axel Richter, Jamasp Jhabvala, Nicolas Mari, Roland Logé, and Elia Iseli. Fine detection of process state and secondary process emissions in laser powder-bed fusion (lpbf) by dual acoustic sensor acquisition and machine learning. IOP Conference Series: Materials Science and Engineering, 1332(1):012032, Aug 2025. URL: https://doi.org/10.1088/1757-899x/1332/1/012032, doi:10.1088/1757-899x/1332/1/012032. This article has 2 citations.

7. (jungert2024acousticemissionmonitoring pages 1-3): Anne Jüngert, Thomas Thenikl, Roman Hofmann, Ludwig Maderner, and Martin Werz. Acoustic emission monitoring of a laser powder bed fusion process. e-Journal of Nondestructive Testing, Oct 2024. URL: https://doi.org/10.58286/30248, doi:10.58286/30248. This article has 5 citations.

8. (jungert2024acousticemissionmonitoring pages 3-8): Anne Jüngert, Thomas Thenikl, Roman Hofmann, Ludwig Maderner, and Martin Werz. Acoustic emission monitoring of a laser powder bed fusion process. e-Journal of Nondestructive Testing, Oct 2024. URL: https://doi.org/10.58286/30248, doi:10.58286/30248. This article has 5 citations.

9. (pandiyan2023optimizinginsitumonitoring pages 3-4): Vigneashwara Pandiyan, Rafał Wróbel, Christian Leinenbach, and Sergey Shevchik. Optimizing in-situ monitoring for laser powder bed fusion process: deciphering acoustic emission and sensor sensitivity with explainable machine learning. Dec 2023. URL: https://doi.org/10.1016/j.jmatprotec.2023.118144, doi:10.1016/j.jmatprotec.2023.118144. This article has 100 citations and is from a domain leading peer-reviewed journal.

10. (pandiyan2023optimizinginsitumonitoring pages 4-5): Vigneashwara Pandiyan, Rafał Wróbel, Christian Leinenbach, and Sergey Shevchik. Optimizing in-situ monitoring for laser powder bed fusion process: deciphering acoustic emission and sensor sensitivity with explainable machine learning. Dec 2023. URL: https://doi.org/10.1016/j.jmatprotec.2023.118144, doi:10.1016/j.jmatprotec.2023.118144. This article has 100 citations and is from a domain leading peer-reviewed journal.

11. (shevchik2018acousticemissionfor pages 5-7): S.A. Shevchik, C. Kenel, C. Leinenbach, and K. Wasmer. Acoustic emission for in situ quality monitoring in additive manufacturing using spectral convolutional neural networks. Additive Manufacturing, 21:598-604, May 2018. URL: https://doi.org/10.1016/j.addma.2017.11.012, doi:10.1016/j.addma.2017.11.012. This article has 636 citations and is from a highest quality peer-reviewed journal.

12. (chang2026areviewof pages 22-23): Wen-Biao Chang, Qi-Fei Zhang, Wei Chen, Yuan Gao, Bin Liu, Zhong-Hua Li, and Chang-Ying Dang. A review of in situ quality monitoring in additive manufacturing using acoustic emission technology. Sensors, 26:438, Jan 2026. URL: https://doi.org/10.3390/s26020438, doi:10.3390/s26020438. This article has 7 citations and is from a peer-reviewed journal.

13. (nobari2026mechanismssensorsand pages 9-11): Sanae Tajalli Nobari, Fabian Hanning, Yongcui Mi, and Joerg Volpp. Mechanisms, sensors, and signals for defect formation and in situ monitoring in metal additive manufacturing. Eng, 7:129, Mar 2026. URL: https://doi.org/10.3390/eng7030129, doi:10.3390/eng7030129. This article has 7 citations.

14. (seleznev2022insitudetection pages 7-7): Mikhail Seleznev, Tobias Gustmann, Judith Miriam Friebel, Urs Alexander Peuker, Uta Kühn, Julia Kristin Hufenbach, Horst Biermann, and Anja Weidner. In situ detection of cracks during laser powder bed fusion using acoustic emission monitoring. Additive Manufacturing Letters, 3:100099, Dec 2022. URL: https://doi.org/10.1016/j.addlet.2022.100099, doi:10.1016/j.addlet.2022.100099. This article has 58 citations and is from a peer-reviewed journal.

15. (xu2024frequencydependentamplitude pages 5-6): Ronghua Xu, Raúl Enrique Beltrán-Gutiérrez, Max Käding, Alexander Lange, Steffen Marx, and Jörn Ostermann. Frequency dependent amplitude response of different couplant materials for mounting piezoelectric sensors. NDT &amp; E International, Jan 2024. URL: https://doi.org/10.1016/j.ndteint.2023.102993, doi:10.1016/j.ndteint.2023.102993. This article has 13 citations and is from a domain leading peer-reviewed journal.

16. (xu2024frequencydependentamplitude pages 6-9): Ronghua Xu, Raúl Enrique Beltrán-Gutiérrez, Max Käding, Alexander Lange, Steffen Marx, and Jörn Ostermann. Frequency dependent amplitude response of different couplant materials for mounting piezoelectric sensors. NDT &amp; E International, Jan 2024. URL: https://doi.org/10.1016/j.ndteint.2023.102993, doi:10.1016/j.ndteint.2023.102993. This article has 13 citations and is from a domain leading peer-reviewed journal.

17. (brunner2021structuralhealthand pages 5-6): Andreas J. Brunner. Structural health and condition monitoring with acoustic emission and guided ultrasonic waves: what about long-term durability of sensors, sensor coupling and measurement chain? Applied Sciences, 11:11648, Dec 2021. URL: https://doi.org/10.3390/app112411648, doi:10.3390/app112411648. This article has 59 citations.

18. (milani2022designandmanufacturinga pages 28-33): MT Milani. Design and manufacturing of an encapsulation for a high-temperature ultrasonic transducer. Unknown journal, 2022.

19. (zakharov2010acousticemissionsignal pages 1-5): D Zakharov, SN Ptichkov, and VV Shemyakin. Acoustic emission signal attenuation in the waveguides used in underwater ae testing. Unknown journal, 2010.

20. (zelenyak2015modelingofacoustic pages 11-15): Andreea-Manuela Zelenyak, Marvin Hamstad, and Markus Sause. Modeling of acoustic emission signal propagation in waveguides. Sensors, 15:11805-11822, May 2015. URL: https://doi.org/10.3390/s150511805, doi:10.3390/s150511805. This article has 88 citations and is from a peer-reviewed journal.

21. (zelenyak2015modelingofacoustic pages 15-18): Andreea-Manuela Zelenyak, Marvin Hamstad, and Markus Sause. Modeling of acoustic emission signal propagation in waveguides. Sensors, 15:11805-11822, May 2015. URL: https://doi.org/10.3390/s150511805, doi:10.3390/s150511805. This article has 88 citations and is from a peer-reviewed journal.

22. (kazys2021hightemperatureultrasonic pages 7-9): Rymantas Kazys and Vaida Vaskeliene. High temperature ultrasonic transducers: a review. Sensors, 21:3200, May 2021. URL: https://doi.org/10.3390/s21093200, doi:10.3390/s21093200. This article has 196 citations and is from a peer-reviewed journal.

23. (kazys2021hightemperatureultrasonic pages 9-11): Rymantas Kazys and Vaida Vaskeliene. High temperature ultrasonic transducers: a review. Sensors, 21:3200, May 2021. URL: https://doi.org/10.3390/s21093200, doi:10.3390/s21093200. This article has 196 citations and is from a peer-reviewed journal.

24. (zelenyak2015modelingofacoustic pages 1-4): Andreea-Manuela Zelenyak, Marvin Hamstad, and Markus Sause. Modeling of acoustic emission signal propagation in waveguides. Sensors, 15:11805-11822, May 2015. URL: https://doi.org/10.3390/s150511805, doi:10.3390/s150511805. This article has 88 citations and is from a peer-reviewed journal.

25. (jolly1994investigationofacoustic pages 6-10): W.D. Jolly. Investigation of acoustic emission coupling techniques. Ndt & E International, 27:219, Jan 1994. URL: https://doi.org/10.1016/0963-8695(94)90557-6, doi:10.1016/0963-8695(94)90557-6. This article has 0 citations and is from a domain leading peer-reviewed journal.

26. (jolly1994investigationofacoustic pages 10-12): W.D. Jolly. Investigation of acoustic emission coupling techniques. Ndt & E International, 27:219, Jan 1994. URL: https://doi.org/10.1016/0963-8695(94)90557-6, doi:10.1016/0963-8695(94)90557-6. This article has 0 citations and is from a domain leading peer-reviewed journal.

27. (shrout1993hightemperaturesensormicrophone pages 148-151): TR Shrout. High temperature sensor/microphone development for active noise control. Unknown journal, 1993.

28. (jolly1994investigationofacoustic pages 1-6): W.D. Jolly. Investigation of acoustic emission coupling techniques. Ndt & E International, 27:219, Jan 1994. URL: https://doi.org/10.1016/0963-8695(94)90557-6, doi:10.1016/0963-8695(94)90557-6. This article has 0 citations and is from a domain leading peer-reviewed journal.

29. (burns2012developmentandcharacterisation pages 170-174): JM Burns. Development and characterisation of a fibre-optic acoustic emission sensor. Unknown journal, 2012.

30. (hinrichs2024analysisofthe pages 1-3): Reemt Hinrichs, Nan Jiang, Raúl Beltrán, Thomas Krause, Max Käding, Alexander Lange, Boso Schmidt, Jörn Ostermann, and Steffen Marx. Analysis of the repeatability of the pencil lead break in comparison to the ball impact and electromagnetic body-noise actuator. e-Journal of Nondestructive Testing, Jun 2024. URL: https://doi.org/10.58286/29911, doi:10.58286/29911. This article has 3 citations.

31. (burns2012developmentandcharacterisation pages 115-120): JM Burns. Development and characterisation of a fibre-optic acoustic emission sensor. Unknown journal, 2012.

32. (chang2026areviewof pages 16-19): Wen-Biao Chang, Qi-Fei Zhang, Wei Chen, Yuan Gao, Bin Liu, Zhong-Hua Li, and Chang-Ying Dang. A review of in situ quality monitoring in additive manufacturing using acoustic emission technology. Sensors, 26:438, Jan 2026. URL: https://doi.org/10.3390/s26020438, doi:10.3390/s26020438. This article has 7 citations and is from a peer-reviewed journal.

33. (nobari2026mechanismssensorsand pages 11-12): Sanae Tajalli Nobari, Fabian Hanning, Yongcui Mi, and Joerg Volpp. Mechanisms, sensors, and signals for defect formation and in situ monitoring in metal additive manufacturing. Eng, 7:129, Mar 2026. URL: https://doi.org/10.3390/eng7030129, doi:10.3390/eng7030129. This article has 7 citations.
