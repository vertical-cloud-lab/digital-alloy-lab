<!--
Edison Scientific LITERATURE_HIGH report: Measured absorptance of Al alloys under a moving laser before the keyhole forms
Job: job-futurehouse-paperqa3-high (LITERATURE_HIGH)
Task ID: 816cba74-36cc-48d0-bd33-4e0754d0de57
Created: 2026-11-27T05:18:08.104836Z  Status: success
Retrieved with edison-client from GitHub Actions for issue #235.
Prompt: QUERIES['dimple_absorptance'] in scripts/edison_keyhole_not_done.py
-->

Question: Context: we have written our own physics-based keyhole and melt-pool model for laser powder bed fusion (1070 nm fibre laser, Gaussian beam 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s) of AlSi10Mg and a hypereutectic Al-24.3Si-0.14Mg (wt%) blend. It uses Drude-Fresnel optics of the liquid from its measured electrical resistivity, a ray tracer for multiple reflections in the keyhole, an energy balance at a keyhole wall at the boiling point, and CALPHAD enthalpies. We are now adding Mg evaporation, a powder layer, a tilted keyhole whose shape comes from a point-by-point wall energy balance, and Marangoni melt flow, and we need sourced inputs. Our model's melt absorbs only 0.18-0.20 (Fresnel, clean liquid Al-Si) in the regime where the surface boils but no keyhole has formed, while the Thermo-Calc AM Module uses about 0.31 there. Question: what laser absorptance has been MEASURED (integrating sphere or calorimetry) at 1.03-1.08 um for aluminium alloys (AlSi10Mg, Al-Si, Al 6061, Al 5182, Al 1100, pure Al) under a moving or stationary laser in conduction mode and in the transition just before a keyhole forms, on bare plates and on powder layers? Include Simonds et al. 2024 (AM-Bench 2022, Al 5182), Trapp et al. 2017, Matthews et al. 2018 (J. Laser Appl. 30, 032302), and any AlSi10Mg single-track absorptance. Give the power, speed, spot size, the measured absorptance against time or power, and the DOI with the figure or table number. Is the higher value attributed to surface oxide, ripples, a shallow depression, or vapour?

## Measured Laser Absorptance of Aluminium Alloys at 1.03–1.08 µm in Conduction Mode and the Pre-Keyhole Transition

### 1. Overview

The question of what fraction of incident 1.07 µm laser power is actually coupled into an aluminium melt before a keyhole forms is central to any physics-based model of laser powder-bed fusion (LPBF) of Al-Si alloys. The Drude–Fresnel absorptance of clean, smooth liquid aluminium at normal incidence near 1.07 µm is approximately 0.10–0.15, depending on the assumed electrical resistivity (reed2024timeresolvedabsorptancein pages 27-31, reed2024timeresolvedabsorptanceina pages 27-31). In practice, every published measurement on a real surface under a moving or stationary laser in conduction mode reports a value that significantly exceeds this clean-liquid prediction. The principal studies are summarised below and in the accompanying table.

| Reference | Alloy | Method | Laser wavelength | Spot size, 1/e² diameter | Power | Speed / exposure | Surface condition | Measured absorptance | Figure / table | DOI |
|---|---|---|---:|---:|---:|---|---|---|---|---|
| Trapp et al. (2017) (trapp2017insituabsorptivity pages 2-3, trapp2017insituabsorptivity pages 4-6, trapp2017insituabsorptivity pages 6-7) | Al 1100 | Direct calorimetry; supporting high-speed video and metallography | 1070 nm | 60 ± 5 µm | 30–≈540 W | 100, 500, 1500 mm/s | Ground bare disc | At 1500 mm/s, ≈0.10–0.15 through the non-keyhole range; observed boiling/keyhole threshold 265 ± 15 W. The rise thereafter is associated with a recoil-pressure depression and multiple reflections. | Fig. 7; Table 2; track morphology in Fig. 8 | [10.1016/j.apmt.2017.08.006](https://doi.org/10.1016/j.apmt.2017.08.006) |
| Trapp et al. (2017) (trapp2017insituabsorptivity pages 1-2, trapp2017insituabsorptivity pages 7-8) | Al 1100 / metallic-powder result | Direct calorimetry | 1070 nm | 60 ± 5 µm | Low power through keyhole regime | 100–1500 mm/s | ≈100 µm powder layer on substrate | Unmelted powder had about twice the bare-disc absorptance at low power; absorptance fell toward the bare/liquid-surface value as the powder melted, then rose when a depression/keyhole formed. The available figure-level powder curves are for 316L, so this is not a numerical Al-1100 powder curve. | General powder result; Fig. 6 illustrates behavior for 316L | [10.1016/j.apmt.2017.08.006](https://doi.org/10.1016/j.apmt.2017.08.006) |
| Matthews et al. (2018) (trapp2017insituabsorptivity pages 1-2) | Al 1100 | Direct calorimetry; companion report from the Trapp–Matthews group | 1070 nm | 60 µm | 30–≈540 W | 100, 500, 1500 mm/s | Bare plate | Companion presentation of the LLNL calorimetric work; an independently tabulated Al value or figure could not be verified from the available text. Use the directly documented Trapp result above rather than counting this as an independent measurement. | Figure/value not independently verified | [10.2351/1.5040636](https://doi.org/10.2351/1.5040636) |
| Simonds et al. (2024), stationary (simonds2024abilitytosimulate pages 1-3, simonds2024abilitytosimulate pages 3-6, simonds2024abilitytosimulate media 71f44c40) | Al 5182, NIST SRM 1241c | Integrating-sphere radiometry synchronized with 50 kHz X-ray imaging | 1070 nm | 122.5 µm | 501 W | Stationary; 1.982 ms exposure | Mirror-polished, 1 mm bare plate; plate tilted 7° | ≈0.24 average before the defined keyhole transition; transition at ≈0.189 ms when instantaneous absorptance reached 0.35; ≈0.65 average after keyhole formation (values read from plotted experimental reference lines). | Figs. 2–4, especially Fig. 4(a,b) | [10.1007/s40192-023-00336-0](https://doi.org/10.1007/s40192-023-00336-0) |
| Simonds et al. (2024), scanned (simonds2024abilitytosimulate pages 3-6, simonds2024abilitytosimulate pages 6-8, simonds2024abilitytosimulate media 99642dbd) | Al 5182, NIST SRM 1241c | Integrating-sphere radiometry synchronized with X-ray imaging | 1070 nm | 122.5 µm | 473 W | 700 mm/s; 1.980 ms exposure | Mirror-polished bare plate; plate tilted 7° | ≈0.24 average before the defined keyhole transition and ≈0.44 after it (read from plotted experimental reference lines); keyhole criterion was instantaneous absorptance ≥0.25. | Figs. 6–8, especially Fig. 8(a,b) | [10.1007/s40192-023-00336-0](https://doi.org/10.1007/s40192-023-00336-0) |
| Allen (2023), Ch. 5 (allen2023sheddinglighton pages 115-120, allen2023sheddinglighton pages 124-129, allen2023sheddinglighton pages 138-143) | AlSi10Mg | Time-resolved integrating-sphere radiometry in a Renishaw AM400 | 1070 nm | 70 µm | 157 W | 60 µs point exposure; 55 µm point distance, giving ≈0.79 m/s effective speed | Traditionally machined bare substrate | 0.04 ± 0.04 for the illustrated five-track record; the chapter-wide conduction-mode summary reports 0.06 ± 0.02. | Fig. 5.4(d); abstract / chapter summary; Fig. 5.6 | Thesis; no article DOI reported |
| Allen (2023), Ch. 5 (allen2023sheddinglighton pages 115-120, allen2023sheddinglighton pages 138-143) | AlSi10Mg | Time-resolved integrating-sphere radiometry | 1070 nm | 70 µm | 157 W | 60 µs point exposure; ≈0.79 m/s effective speed | AM-built substrate without loose powder (AM0; rough hatch surface) | 0.18 ± 0.06 for the illustrated record; chapter-wide conduction-mode summary 0.22 ± 0.05. | Fig. 5.4(c); Fig. 5.6 | Thesis; no article DOI reported |
| Allen (2023), Ch. 5 (allen2023sheddinglighton pages 115-120, allen2023sheddinglighton pages 138-143) | AlSi10Mg | Time-resolved integrating-sphere radiometry | 1070 nm | 70 µm | 157 W | 60 µs point exposure; ≈0.79 m/s effective speed | AM30 powder layer; nominal 30 µm recoater increment, estimated actual thickness >120 µm | 0.77 ± 0.08 in conduction-mode processing. | Fig. 5.4(b); Fig. 5.6 | Thesis; no article DOI reported |
| Allen (2023), Ch. 5 (allen2023sheddinglighton pages 115-120, allen2023sheddinglighton pages 138-143) | AlSi10Mg | Time-resolved integrating-sphere radiometry | 1070 nm | 70 µm | 157 W | 60 µs point exposure; ≈0.79 m/s effective speed | AM90 powder layer; nominal 90 µm recoater increment, estimated actual thickness >180 µm | 0.74 ± 0.07 in conduction-mode processing. | Fig. 5.4(a); Fig. 5.6 | Thesis; no article DOI reported |
| Allen (2023), Ch. 5, transition (allen2023sheddinglighton pages 143-148) | AlSi10Mg | Time-resolved integrating-sphere radiometry | 1070 nm | 105 µm | 375 W | 100 µs point exposure; ≈0.50 m/s effective speed | Machined bare / rough AM0 surfaces | Between temporary keyholes, ≈0.10 on machined material and ≈0.30 on AM0; averages including intermittent keyhole openings were 0.30 ± 0.05 and 0.49 ± 0.07, respectively. | Fig. 5.5(c,d); Fig. 5.6 | Thesis; no article DOI reported |
| Allen (2023), Ch. 5, transition (allen2023sheddinglighton pages 143-148) | AlSi10Mg | Time-resolved integrating-sphere radiometry | 1070 nm | 105 µm | 375 W | 100 µs point exposure; ≈0.50 m/s effective speed | AM30 / AM90 powder layers | Average absorptance 0.84 ± 0.10 (AM30) and 0.74 ± 0.09 (AM90); ISR alone could not unambiguously separate powder multiple scattering from intermittent depressions. | Fig. 5.5(a,b); Fig. 5.6 | Thesis; no article DOI reported |
| Reed (2024) (reed2024timeresolvedabsorptanceinb pages 83-89, reed2024timeresolvedabsorptanceina pages 83-89) | AlSi10Mg | Time-resolved integrating-sphere radiometry; same experimental dataset as Allen Ch. 5 | 1070 nm | 70 µm conduction; 104 µm transition | 157 W conduction; 375 W transition | ≈0.76–0.79 m/s conduction; 0.50 m/s transition | Machined, AM0, AM30 and AM90 | Confirms conduction values: machined 0.04 ± 0.04, AM0 0.18 ± 0.06, AM30 0.77 ± 0.08, AM90 0.74 ± 0.07. The 375 W case shows intermittent opening/closing of depressions rather than a single intrinsic pre-keyhole value. | Conduction and transition time-trace figures in results chapter | Thesis; no DOI identified |
| Allen et al. / Allen thesis Ch. 4 (allen2023sheddinglighton pages 94-100, allen2023sheddinglighton pages 100-105, allen2023sheddinglighton pages 110-115) | Al 6061 | Integrating-sphere radiometry plus inline coherent imaging | ≈1070 nm Yb-fibre laser | 238 µm | 974 W | Stationary, nominal 10 ms pulse | Sanded and methanol-cleaned bare plate | 0.723 ± 0.001 after a keyhole formed; this is a developed-keyhole value, not conduction/pre-keyhole absorptance. Reliable ISR data before keyholing were limited by direct back-reflection for up to 2.51 ms. | Time trace in Fig. 4.1; summary table in Ch. 4 | [10.1016/j.procir.2022.08.041](https://doi.org/10.1016/j.procir.2022.08.041) |
| Rubenchik et al. (2014), out-of-band comparator (rubenchik2014temperaturedependent780nmlaser pages 5-6, rubenchik2014temperaturedependent780nmlaser pages 3-4, rubenchik2014temperaturedependent780nmlaser pages 4-5) | Engineering-grade Al | Direct calorimetry; temperature-dependent surface measurement | **780 nm, not 1.03–1.08 µm** | Not comparable to LPBF spot | Low-intensity heating study | Stationary thermal cycles | Real engineering surface with native oxide and directional roughness | Clean bulk-Fresnel calculation ≈0.13; ≈50 nm alumina can raise calculated absorptance above 0.20, while measured excess also required roughness/corrugation. Not a 1070 nm melt-pool datum. | Thin-film/oxide and polarization figures in the paper | [10.1117/1.OE.53.12.122506](https://doi.org/10.1117/1.OE.53.12.122506) |


*Table: Measured near-infrared absorptance for aluminium alloys on bare, rough AM-built, and powder-covered surfaces, with conduction and transition values separated from developed-keyhole measurements. The final row is an explicitly out-of-band 780 nm comparator for oxide and roughness effects.*

---

### 2. Trapp et al. (2017) — Al 1100 Bare Plate, Calorimetry

Trapp et al. used direct micro-calorimetry with a 1070 nm Yb-fibre laser focused to a 60 ± 5 µm (1/e²) Gaussian spot on 0.6 mm thick Al 1100 discs at scan speeds of 100, 500, and 1500 mm/s (trapp2017insituabsorptivity pages 2-3, trapp2017insituabsorptivity pages 3-4). At 1500 mm/s, the conduction-mode absorptivity was approximately 0.10–0.15 and remained roughly constant across the low-power range (up to ≈200 W) where no melting or only shallow melting occurred. The onset of keyhole formation was observed at 265 ± 15 W at 1500 mm/s (Table 2 and Fig. 7 of that paper), after which absorptivity climbed steeply (trapp2017insituabsorptivity pages 4-6, trapp2017insituabsorptivity pages 6-7). The extrapolated zero-power absorptivity for Al 1100 was notably higher than the clean-metal Fresnel prediction; Trapp et al. attributed this to enhanced absorption from the native aluminium oxide layer, noting that the discs were ground before experiments but not sputtered clean (trapp2017insituabsorptivity pages 6-7). For 316L steel at the same conditions, the flat-surface regime gave ≈ 0.29–0.31 for comparison (trapp2017insituabsorptivity pages 4-6). With a ≈100 µm powder layer on the Al 1100 substrate, absorptivity at low power was approximately twice that of the bare disc, then dropped sharply as powder melted, and rose again at keyhole onset (trapp2017insituabsorptivity pages 1-2, trapp2017insituabsorptivity pages 7-8). DOI: 10.1016/j.apmt.2017.08.006; key data in Fig. 7 and Table 2.

---

### 3. Matthews et al. (2018) — Al 1100, Calorimetry (Companion Paper)

Matthews, Trapp, Guss, and Rubenchik (J. Laser Appl. 30, 032302, 2018; DOI: 10.2351/1.5040636) presented a companion publication from the same Lawrence Livermore National Laboratory (LLNL) calorimetric apparatus described by Trapp et al. (2017), reporting the same 1070 nm, 60 µm spot measurements on Al 1100 and 316L at 100–1500 mm/s (trapp2017insituabsorptivity pages 1-2). The full text of this paper could not be retrieved independently during this search, but its experimental parameters, materials, and results overlap with the Trapp 2017 dataset described above. The conduction-mode absorptivity of bare Al 1100 at 1500 mm/s remains ≈ 0.10–0.15 up to the keyhole transition.

---

### 4. Simonds et al. (2024) — Al 5182, Integrating-Sphere Radiometry (AM-Bench 2022)

Simonds et al. combined integrating-sphere radiometry (40 ns time resolution) with high-speed synchrotron X-ray imaging at the Advanced Photon Source on 1 mm thick, mirror-polished bare plates of Al 5182 (NIST SRM 1241c) with a 1070 nm laser and a 122.5 µm (1/e²) spot diameter (simonds2024abilitytosimulate pages 1-3, simonds2024abilitytosimulate pages 3-6).

**Stationary exposure (501 W, 1.982 ms):** The measured average absorptance before keyhole formation was ≈ 0.24 (≈ 24%), with the keyhole transition occurring at ≈ 0.189 ms, defined as the point where absorptance reached 0.35 (Figs. 2–4). After the keyhole formed, the average absorptance climbed to ≈ 0.65 (Fig. 4b) (simonds2024abilitytosimulate media 71f44c40, simonds2024abilitytosimulate media 99642dbd).

**Scanned exposure (473 W, 700 mm/s, 1.980 ms):** The pre-keyhole average absorptance was again ≈ 0.24, while the post-keyhole average was ≈ 0.44 (Figs. 6–8) (simonds2024abilitytosimulate pages 6-8, simonds2024abilitytosimulate media bd134611). Notably, the pre-keyhole absorptance of 0.24 significantly exceeds the clean Fresnel prediction for liquid aluminium (≈ 0.10–0.15). Simonds et al. concluded that "most simulations rely on literature values for optical properties... that are not representative of the aluminum material tested" and that "reflection and absorption are very sensitive to surface preparation" (simonds2024abilitytosimulate pages 6-8). They specifically highlighted that once a keyhole forms, the dependence on intrinsic optical properties largely disappears because multiple reflections dominate (simonds2024abilitytosimulate pages 3-6). DOI: 10.1007/s40192-023-00336-0; Figs. 4a and 8a.

---

### 5. Allen (2023 thesis, Chapter 5) & Reed (2024 thesis) — AlSi10Mg, ISR in a Commercial AM Machine

Allen et al. installed a custom integrating sphere directly inside a Renishaw AM 400 system and measured time-resolved absorptance at 260 kHz during multi-track LPBF of AlSi10Mg with plasma-atomised powder (D50 = 28 µm, 15–63 µm range) (allen2023sheddinglighton pages 115-120, allen2023sheddinglighton pages 124-129). This is the only known study reporting calibrated, time-resolved absorptance for AlSi10Mg powder layers under realistic AM conditions.

**Conduction mode (157 W, 70 µm spot, 60 µs exposure, ≈ 790 mm/s effective speed):**
- Machined bare AlSi10Mg substrate: 0.06 ± 0.02 (chapter summary) or 0.04 ± 0.04 (single illustrative trace) — the lowest value, consistent with a smooth, specularly reflecting metallic surface (allen2023sheddinglighton pages 138-143).
- AM-built substrate with no loose powder (AM0, rough hatched surface): 0.22 ± 0.05 — substantially higher due to periodic roughness from prior hatch lines (allen2023sheddinglighton pages 138-143).
- 30 µm nominal powder layer (AM30, actual thickness >120 µm): 0.77 ± 0.08 — high due to multiple scattering among powder particles (allen2023sheddinglighton pages 138-143, reed2024timeresolvedabsorptanceina pages 83-89).
- 90 µm nominal powder layer (AM90, actual thickness >180 µm): 0.74 ± 0.07 (allen2023sheddinglighton pages 138-143, reed2024timeresolvedabsorptanceina pages 83-89).

These are shown in Fig. 5.4 and summarised in Fig. 5.6 of the Allen thesis.

**Transition mode (375 W, 105 µm spot, 100 µs exposure, ≈ 500 mm/s):**
- Machined bare: average 0.30 ± 0.05, with sporadic temporary keyhole openings superimposed on a base of ≈ 0.10 (allen2023sheddinglighton pages 143-148).
- AM0 (rough): average 0.49 ± 0.07, base between keyholes ≈ 0.30 (allen2023sheddinglighton pages 143-148).
- AM30 powder: average 0.84 ± 0.10 (allen2023sheddinglighton pages 143-148).
- AM90 powder: average 0.74 ± 0.09, with signs of powder depletion by denudation reducing absorptance of later tracks by up to 40% (allen2023sheddinglighton pages 143-148).

Shown in Fig. 5.5 and Fig. 5.6. The Reed (2024) thesis reports the identical dataset and confirms all numerical values (reed2024timeresolvedabsorptanceinb pages 83-89, reed2024timeresolvedabsorptanceina pages 83-89).

---

### 6. Allen (2023 thesis, Chapter 4) — Al 6061, ISR + ICI Spot Welding

Using a 1070 nm multimode fibre laser with a 238 µm (1/e²) spot, Allen measured absorptance during 10 ms stationary spot welds on sanded Al 6061 at 974 W (allen2023sheddinglighton pages 110-115, allen2023sheddinglighton pages 100-105). After keyhole formation, the average absorptance was 0.723 ± 0.001. Reliable pre-keyhole absorptance data could not be obtained because back-reflections from the initially flat, highly reflective aluminium surface escaped the integrating sphere for up to 2.51 ms, before a keyhole tilted the reflected beam into the sphere walls (allen2023sheddinglighton pages 100-105). Published in Procedia CIRP 111, 5–9 (2022); DOI: 10.1016/j.procir.2022.08.041; data in Fig. 4.1 and summary Table 4.1.

---

### 7. Why Is the Measured Pre-Keyhole Absorptance Higher Than the Clean-Liquid Fresnel Value?

The user's model gives 0.18–0.20 from Drude–Fresnel optics of liquid Al-Si, while the Thermo-Calc AM Module uses ≈ 0.31. The experimental data above consistently report values between 0.06 and 0.24 on bare plates, depending on alloy and surface condition, with the difference from the idealized Fresnel prediction attributed to several factors:

**(a) Surface oxide.** Rubenchik et al. (2014) showed, through thin-film optical modelling at 780 nm, that a native alumina layer of only ≈ 50 nm thickness raises the absorptivity of engineering-grade aluminium from the clean-Fresnel value of ≈ 0.13 to above 0.20 (rubenchik2014temperaturedependent780nmlaser pages 4-5). The alumina refractive index (n ≈ 1.62 at 0.78 µm) modifies the boundary conditions for the incident light, acting as an anti-reflection coating; the effect carries over qualitatively to 1.07 µm. Trapp et al. noted that the extrapolated zero-power absorptivity of Al 1100 exceeded the literature value for clean metal and attributed this to oxide, "even though this effect is considered to be small as the discs were ground before the experiments" (trapp2017insituabsorptivity pages 6-7).

**(b) Surface roughness/corrugation.** Rubenchik et al. (2014) further demonstrated, using polarisation-resolved measurements, that surface corrugation couples incident radiation into surface electromagnetic modes (surface plasmons), producing absorptance in excess of what oxide alone can explain (rubenchik2014temperaturedependent780nmlaser pages 4-5). In the Allen AlSi10Mg data, the hatched AM0 substrate (periodic roughness from prior hatch lines at 35 µm spacing) absorbed 0.22, nearly four times the machined substrate value of 0.06 (allen2023sheddinglighton pages 138-143), providing direct evidence that micron-scale roughness dramatically increases coupling in conduction mode.

**(c) Shallow vapour depression (pre-keyhole).** At the transition, before a true keyhole with an aspect ratio > 1 is established, Trapp et al. observed (at 68 W, 500 mm/s on 316L) the intermittent appearance of a small depression (≈ 30 µm deep) lasting only ≈ 50 µs before collapsing, with associated fluctuations in absorptance (trapp2017insituabsorptivity pages 4-6). Allen et al. observed analogous temporary depressions in AlSi10Mg causing sporadic absorptance spikes from 0.10 to > 0.50 on bare machined surfaces at 375 W (allen2023sheddinglighton pages 143-148). These shallow depressions allow one or two additional Fresnel reflections (the coupling expected for a cone of aspect ratio ≈ 1 is ≈ 0.58), and their time-averaged contribution raises the apparent absorptance above the flat-surface value.

**(d) Vapour/plume absorption.** Trapp et al. discussed the possibility that laser light may be absorbed or reflected in the vapour plume before reaching the metallic surface, noting that the plume tilts more with increasing scan speed, reducing plume–beam interaction (trapp2017insituabsorptivity pages 6-7). However, vapour-plume absorption is generally considered small relative to the oxide and roughness effects for aluminium at 1.07 µm in the conduction-mode regime.

**In summary:** The measured pre-keyhole absorptance of bare aluminium (0.10–0.24) exceeds the clean-liquid Drude–Fresnel prediction (0.10–0.15) primarily because of native oxide films and surface roughness/corrugation, with an additional contribution from intermittent shallow depressions at the transition. Vapour/plume absorption is a minor contributor. The Thermo-Calc AM Module's value of ≈ 0.31 likely reflects an engineering compromise that lumps oxide, roughness, and incipient depression effects into a single effective absorptance; it is higher than most bare-plate measurements but lower than any powder-covered measurement (≈ 0.65–0.77).

---

### 8. Summary of Key Figures and DOIs

- **Trapp et al. (2017):** Fig. 7 (Al 1100 vs 316L vs W absorptivity at 1500 mm/s), Table 2 (keyhole thresholds), Fig. 6 (powder vs bare 316L). DOI: 10.1016/j.apmt.2017.08.006.
- **Matthews et al. (2018):** Companion to Trapp 2017. DOI: 10.2351/1.5040636.
- **Simonds et al. (2024):** Fig. 2 (stationary Al 5182 absorptance vs time), Fig. 4a (pre-keyhole experimental value ≈ 24%), Fig. 8a (scanned pre-keyhole ≈ 24%). DOI: 10.1007/s40192-023-00336-0.
- **Allen (2023 thesis, Ch. 5):** Fig. 5.4 (time-resolved absorptance for AlSi10Mg, four surface conditions), Fig. 5.6 (all average absorptance vs power).
- **Reed (2024 thesis):** Confirms Allen values; conduction and transition time-trace figures in results chapter.
- **Allen et al. / Allen thesis Ch. 4 (Al 6061):** Fig. 4.1, Table 4.1 (keyhole absorptance 0.72). DOI: 10.1016/j.procir.2022.08.041.
- **Rubenchik et al. (2014):** Oxide thin-film model and polarisation data for engineering-grade Al at 780 nm. DOI: 10.1117/1.OE.53.12.122506.

References

1. (reed2024timeresolvedabsorptancein pages 27-31): MK Reed. Time-resolved absorptance in laser-powder bed fusion: effect of gaussian and novel beam shapes. Unknown journal, 2024.

2. (reed2024timeresolvedabsorptanceina pages 27-31): MK Reed. Time-resolved absorptance in laser-powder bed fusion: effect of gaussian and novel beam shapes. Unknown journal, 2024.

3. (trapp2017insituabsorptivity pages 2-3): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

4. (trapp2017insituabsorptivity pages 4-6): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

5. (trapp2017insituabsorptivity pages 6-7): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

6. (trapp2017insituabsorptivity pages 1-2): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

7. (trapp2017insituabsorptivity pages 7-8): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

8. (simonds2024abilitytosimulate pages 1-3): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Niranjan Parab, Cang Zhao, Tao Sun, and Paul A. Williams. Ability to simulate absorption and melt pool dynamics for laser melting of bare aluminum plate: results and insights from the 2022 asynchronous am-bench challenge. Integrating Materials and Manufacturing Innovation, 13:175-184, Feb 2024. URL: https://doi.org/10.1007/s40192-023-00336-0, doi:10.1007/s40192-023-00336-0. This article has 9 citations and is from a peer-reviewed journal.

9. (simonds2024abilitytosimulate pages 3-6): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Niranjan Parab, Cang Zhao, Tao Sun, and Paul A. Williams. Ability to simulate absorption and melt pool dynamics for laser melting of bare aluminum plate: results and insights from the 2022 asynchronous am-bench challenge. Integrating Materials and Manufacturing Innovation, 13:175-184, Feb 2024. URL: https://doi.org/10.1007/s40192-023-00336-0, doi:10.1007/s40192-023-00336-0. This article has 9 citations and is from a peer-reviewed journal.

10. (simonds2024abilitytosimulate media 71f44c40): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Niranjan Parab, Cang Zhao, Tao Sun, and Paul A. Williams. Ability to simulate absorption and melt pool dynamics for laser melting of bare aluminum plate: results and insights from the 2022 asynchronous am-bench challenge. Integrating Materials and Manufacturing Innovation, 13:175-184, Feb 2024. URL: https://doi.org/10.1007/s40192-023-00336-0, doi:10.1007/s40192-023-00336-0. This article has 9 citations and is from a peer-reviewed journal.

11. (simonds2024abilitytosimulate pages 6-8): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Niranjan Parab, Cang Zhao, Tao Sun, and Paul A. Williams. Ability to simulate absorption and melt pool dynamics for laser melting of bare aluminum plate: results and insights from the 2022 asynchronous am-bench challenge. Integrating Materials and Manufacturing Innovation, 13:175-184, Feb 2024. URL: https://doi.org/10.1007/s40192-023-00336-0, doi:10.1007/s40192-023-00336-0. This article has 9 citations and is from a peer-reviewed journal.

12. (simonds2024abilitytosimulate media 99642dbd): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Niranjan Parab, Cang Zhao, Tao Sun, and Paul A. Williams. Ability to simulate absorption and melt pool dynamics for laser melting of bare aluminum plate: results and insights from the 2022 asynchronous am-bench challenge. Integrating Materials and Manufacturing Innovation, 13:175-184, Feb 2024. URL: https://doi.org/10.1007/s40192-023-00336-0, doi:10.1007/s40192-023-00336-0. This article has 9 citations and is from a peer-reviewed journal.

13. (allen2023sheddinglighton pages 115-120): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

14. (allen2023sheddinglighton pages 124-129): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

15. (allen2023sheddinglighton pages 138-143): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

16. (allen2023sheddinglighton pages 143-148): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

17. (reed2024timeresolvedabsorptanceinb pages 83-89): MK Reed. Time-resolved absorptance in laser-powder bed fusion: effect of gaussian and novel beam shapes. Unknown journal, 2024.

18. (reed2024timeresolvedabsorptanceina pages 83-89): MK Reed. Time-resolved absorptance in laser-powder bed fusion: effect of gaussian and novel beam shapes. Unknown journal, 2024.

19. (allen2023sheddinglighton pages 94-100): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

20. (allen2023sheddinglighton pages 100-105): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

21. (allen2023sheddinglighton pages 110-115): TR Allen. Shedding light on laser-metal interactions: in situ monitoring with inline coherent imaging and integrating sphere radiometry. Unknown journal, 2023.

22. (rubenchik2014temperaturedependent780nmlaser pages 5-6): Alexander M. Rubenchik, Sheldon S. Q. Wu, V. Keith Kanz, Mary M. LeBlanc, W. Howard Lowdermilk, Mark D. Rotter, and Joel R. Stanley. Temperature-dependent 780-nm laser absorption by engineering grade aluminum, titanium, and steel alloy surfaces. Optical Engineering, 53:122506, Dec 2014. URL: https://doi.org/10.1117/1.oe.53.12.122506, doi:10.1117/1.oe.53.12.122506. This article has 60 citations and is from a peer-reviewed journal.

23. (rubenchik2014temperaturedependent780nmlaser pages 3-4): Alexander M. Rubenchik, Sheldon S. Q. Wu, V. Keith Kanz, Mary M. LeBlanc, W. Howard Lowdermilk, Mark D. Rotter, and Joel R. Stanley. Temperature-dependent 780-nm laser absorption by engineering grade aluminum, titanium, and steel alloy surfaces. Optical Engineering, 53:122506, Dec 2014. URL: https://doi.org/10.1117/1.oe.53.12.122506, doi:10.1117/1.oe.53.12.122506. This article has 60 citations and is from a peer-reviewed journal.

24. (rubenchik2014temperaturedependent780nmlaser pages 4-5): Alexander M. Rubenchik, Sheldon S. Q. Wu, V. Keith Kanz, Mary M. LeBlanc, W. Howard Lowdermilk, Mark D. Rotter, and Joel R. Stanley. Temperature-dependent 780-nm laser absorption by engineering grade aluminum, titanium, and steel alloy surfaces. Optical Engineering, 53:122506, Dec 2014. URL: https://doi.org/10.1117/1.oe.53.12.122506, doi:10.1117/1.oe.53.12.122506. This article has 60 citations and is from a peer-reviewed journal.

25. (trapp2017insituabsorptivity pages 3-4): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

26. (simonds2024abilitytosimulate media bd134611): Brian J. Simonds, Jack Tanner, Alexandra Artusio-Glimpse, Niranjan Parab, Cang Zhao, Tao Sun, and Paul A. Williams. Ability to simulate absorption and melt pool dynamics for laser melting of bare aluminum plate: results and insights from the 2022 asynchronous am-bench challenge. Integrating Materials and Manufacturing Innovation, 13:175-184, Feb 2024. URL: https://doi.org/10.1007/s40192-023-00336-0, doi:10.1007/s40192-023-00336-0. This article has 9 citations and is from a peer-reviewed journal.
