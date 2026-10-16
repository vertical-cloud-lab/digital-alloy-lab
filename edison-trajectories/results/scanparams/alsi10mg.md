# AlSi10Mg (commercial reference)

_Edison task_id: `616b8cf9-3840-4d59-9dc5-c0744da27e5f`  
_status: success_

---

# LPBF Scan Parameters and Printability-Map Grid-Search Plan for AlSi10Mg (Commercial Reference)

**Target Composition:** Al–10.0 wt% Si–0.325 wt% Mg, bal. Al (midpoint of AlSi10Mg specification)

---

## 1. Single-Point Reference Parameters

The following table provides the complete Thermo-Calc AM Module parameter set for a steady-state Single-Point calculation of AlSi10Mg. Four parameters are changed from defaults; all others remain at Thermo-Calc defaults. Since AlSi10Mg is the AM Module's calibration alloy, this run effectively re-verifies the default absorptivity model against known industrial process windows.

| Parameter Category | Parameter Name | Recommended Value | Default Value | Changed? | Justification/Citation |
|---|---|---:|---:|---|---|
| Global | Gas pressure | 1e5 Pa | 1e5 Pa | No | Leave at Thermo-Calc default; no AlSi10Mg-specific evidence here requiring deviation, and cited LPBF studies operated under standard inert-gas conditions rather than unusual chamber pressures (bogdanova2024mesoscalesimulationof pages 3-5, rehman2021spatterformationand pages 8-10) |
| Global | Base-plate temperature | 150 °C | 30 °C | Yes | Change for better match to common AlSi10Mg LPBF practice: 150 °C preheat was used in Wei et al.; Zhu et al. showed 150 °C promotes in-situ aging/β'' precipitation and is a useful preheat level, while higher preheats around 200 °C can coarsen microstructure and reduce strength (wei2017thealsi10mgsamples pages 5-9, zhu2023microstructuralanalysisof pages 1-3, zhu2023microstructuralanalysisof pages 9-12) |
| Global | Ambient temperature | 23 °C | 23 °C | No | Leave at default; no composition-specific evidence justifies changing ambient temperature for AlSi10Mg steady-state screening (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5) |
| Global | Fluid-flow / Marangoni | ON | ON | No | Leave at default because AlSi10Mg melt-pool behavior is strongly governed by Marangoni-driven flow and related hydrodynamics (rehman2021spatterformationand pages 15-17, rehman2021spatterformationand pages 10-12) |
| Global | Powder density | 80% of solid | 80% of solid | No | Leave at default; no AlSi10Mg-specific evidence here supports overriding the AM Module default packing assumption for preliminary steady-state runs (bogdanova2024mesoscalesimulationof pages 3-5, bajaj2020precipitationduringintrinsic pages 60-63) |
| Geometry | Height | 2.0 mm | 2.0 mm | No | Leave at default for preliminary steady-state comparison run |
| Geometry | Mesh | Coarse | Coarse | No | Leave at default for preliminary screening; user guidance discourages deviation absent a composition-specific reason |
| Heat source type | Heat source type | Gaussian | Gaussian | No | Keep Gaussian: matches the standard single-spot Yb-fiber beam assumption used in AlSi10Mg LPBF studies and in comparable simulations; no clear need for core-ring on Aconity MIDI baseline verification run (bogdanova2024mesoscalesimulationof pages 3-5) |
| Heat source parameters | Power | 350 W | 200 W | Yes | Change to 350 W to align with well-established industrial AlSi10Mg windows: SLM Solutions optimized set reported as 350 W with 30 µm layer and 130 µm hatch; Bogdanova also used 350 W as a baseline substrate-build condition on a 400 W Yb-fiber LPBF system (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5, hyer2020understandingthelaser pages 2-5) |
| Heat source parameters | Absorptivity mode | Calculated, prefactor 1.0 | Calculated, prefactor 1.0 | No | Keep Thermo-Calc default because AlSi10Mg is the calibration alloy for this absorptivity mode; literature supports low solid absorptivity (~0.1) but much higher effective absorption in LPBF due to powder-bed and keyhole multiple reflections, so overriding to a constant is not justified here (bogdanova2024mesoscalesimulationof pages 7-9, bogdanova2024mesoscalesimulationof pages 2-3, bogdanova2024mesoscalesimulationof pages 5-7) |
| Heat source parameters | Laser wavelength | 1064 nm | 1064 nm | No | Leave at default; matches Aconity-class Yb-fiber lasers and the 1070 nm class used in the cited AlSi10Mg LPBF studies (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5, rehman2021spatterformationand pages 8-10) |
| Heat source parameters | Beam radius | 40 µm | 40 µm | No | Leave at default; corresponds to an ~80 µm D4σ spot, matching representative AlSi10Mg LPBF studies and Aconity MIDI typical optics (bogdanova2024mesoscalesimulationof pages 3-5) |
| Heat source parameters | Keyhole model | ON | ON | No | Leave at default because AlSi10Mg at industrially relevant powers can enter transition/keyhole behavior, and including keyhole physics is appropriate for printability-map realism (bogdanova2024mesoscalesimulationof pages 5-7, huang2022keyholefluctuationand pages 2-4) |
| Heat source parameters | Beam-quality factor M² | 1.0 | 1.0 | No | Leave at default; no AlSi10Mg-specific evidence supports altering the nominal beam quality for the baseline run |
| Scanning strategy | Scanning speed | 1300 mm/s | 1000 mm/s | Yes | Change to 1300 mm/s to better match industrial AlSi10Mg windows at 350 W and 30 µm layer thickness; this sits between the vendor-optimized 1650 mm/s case and lower-speed deeper-penetration regimes, giving a representative ~50–55 J/mm³ starting point for Aconity/M290-like processing (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5) |
| Scanning strategy | Layer thickness | 30 µm | 40 µm | Yes | Change to 30 µm because this is the most common AlSi10Mg LPBF layer thickness in the cited industrial/machine-representative studies and widens the dense-process window relative to thicker layers (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5) |
| Top boundary | Radiation emissivity | 0.8 | 0.8 | No | Leave at default; no AlSi10Mg-specific evidence here motivates an override |
| Top boundary | Convective HTC | 20 W/m²/K | 20 W/m²/K | No | Leave at default; no composition-specific evidence justifies changing the preliminary boundary-condition value |
| Top boundary | Evaporation | ON | ON | No | Leave at default because evaporation/recoil effects are relevant in AlSi10Mg melt-pool physics, especially toward transition/keyhole conditions (rehman2021spatterformationand pages 15-17, bogdanova2024mesoscalesimulationof pages 5-7) |
| Calculation type | Calculation type | Single Point | N/A | Yes | Use Single Point for the reference steady-state run before the broader Grid P-v sweep requested by the project |


*Table: This table compiles a complete Thermo-Calc AM Module single-point parameter set for AlSi10Mg, explicitly identifying which values remain at default and which should be changed to better match representative industrial LPBF practice on an Aconity MIDI-class system.*

**Key deviations justified:**

- **Power → 350 W:** The SLM Solutions optimized parameter set for AlSi10Mg specifies 350 W with 30 µm layer thickness and 130 µm hatch spacing, yielding ~54 J/mm³ (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5). Bogdanova et al. used 350 W as the baseline substrate-build condition on a 400 W Yb-fiber system (bogdanova2024mesoscalesimulationof pages 3-5). This value is well within the Aconity MIDI range (50–400 W).

- **Scan speed → 1300 mm/s:** At 350 W and 30 µm layer thickness, 1300 mm/s gives a volumetric energy density of ~51 J/mm³ (assuming 130 µm hatch), which falls squarely within the >99% density window of 32–54 J/mm³ identified by Hyer et al. (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5). The SLM Solutions vendor-optimized speed is 1650 mm/s; we select a slightly lower value to produce a deeper melt pool that better exercises the AM Module's keyhole model while remaining in the productive conduction/transition regime. This is well within the Aconity MIDI range (100–3000 mm/s).

- **Layer thickness → 30 µm:** This is the standard industrial layer thickness for AlSi10Mg LPBF across EOS, SLM Solutions, and comparable platforms (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5). Hyer et al. demonstrated that smaller slice thickness widens the dense-processing window (hyer2020understandingthelaser pages 1-2).

- **Base-plate temperature → 150 °C:** Platform preheating to 150 °C is common practice for AlSi10Mg LPBF and reduces residual stress/distortion without the microstructural coarsening and strength degradation reported at 200 °C (zhu2023microstructuralanalysisof pages 1-3, zhu2023microstructuralanalysisof pages 5-7, zhu2023microstructuralanalysisof pages 9-12). Wei et al. similarly used 150 °C preheat (wei2017thealsi10mgsamples pages 5-9). Zhu et al. showed 150 °C promotes beneficial in-situ β″ (Mg₅Si₆) precipitation in the as-built condition (zhu2023microstructuralanalysisof pages 5-7, zhu2023microstructuralanalysisof pages 7-9).

---

## 2. Grid-Search Plan for P–v Printability Map

The AM Module Grid calculation should sweep laser power and scan speed as the two conventional printability-map axes, holding all other parameters constant at the single-point values above.

| Parameter | Value | Rationale |
|---|---|---|
| Power axis range | 100–400 W (100, 150, 200, 250, 300, 350, 400 W) | Spans the practical Aconity MIDI envelope and brackets the AlSi10Mg window from low-power lack-of-fusion risk to high-power transition/deep-keyhole behavior; 350 W is a well-established industrial reference point for AlSi10Mg, while 400 W intentionally probes the upper boundary (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5, rehman2021spatterformationand pages 8-10) |
| Power step count | 7 levels (50 W increments) | 50 W spacing is coarse enough to keep the Grid run tractable but fine enough to resolve regime changes around the commonly used 250–350 W region for AlSi10Mg (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5, hyer2020understandingthelaser pages 2-5) |
| Scan-speed axis range | 200–2000 mm/s (200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000 mm/s) | Covers very slow/high-input conditions associated with unstable keyhole or overmelting through the dense industrial AlSi10Mg window and out to high-speed lack-of-fusion conditions; published AlSi10Mg studies place the useful window broadly in the ~800–1800 mm/s range depending on power and machine (wei2017thealsi10mgsamples pages 12-15, wei2017thealsi10mgsamples pages 9-12, hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5) |
| Speed step count | 10 levels (200 mm/s increments) | 200 mm/s spacing gives adequate resolution across the conduction/transition regime center while still keeping total points manageable for steady-state Grid calculations (wei2017thealsi10mgsamples pages 12-15, wei2017thealsi10mgsamples pages 9-12, hyer2020understandingthelaser pages 2-5) |
| Total grid points | 7 × 10 = 70 | Large enough to train an initial BOFN/surrogate on regime shape and melt-pool trends, but still practical for AM Module Grid mode and a matching physical coupon study (bajaj2020precipitationduringintrinsic pages 58-60, bajaj2020precipitationduringintrinsic pages 60-63) |
| Layer thickness held constant | 30 µm | Best match to modern AlSi10Mg LPBF practice and the cited industrial parameter sets; also widens the dense-processing window relative to thicker layers (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5) |
| Hatch spacing reference | 130 µm | Use as the reference spacing for VED and overlap interpretation; directly matches the SLM Solutions optimized AlSi10Mg parameter set and is representative for dense AlSi10Mg builds (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5) |
| Beam radius held constant | 40 µm | Corresponds to an ~80 µm beam diameter / D4σ spot, matching representative Yb-fiber AlSi10Mg studies and the Thermo-Calc default/Aconity-like optics (bogdanova2024mesoscalesimulationof pages 3-5) |
| Base-plate temperature held constant | 150 °C | Good AlSi10Mg validation setting: common in the literature, reduces thermal stress, and avoids the strength degradation/coarsening reported at higher preheats near 200 °C (wei2017thealsi10mgsamples pages 5-9, zhu2023microstructuralanalysisof pages 1-3, zhu2023microstructuralanalysisof pages 9-12) |
| Other AM Module settings | As per single-point reference parameters | Keeps the grid interpretable by varying only P and v while preserving the AlSi10Mg-calibrated absorptivity model and other default physics choices (bogdanova2024mesoscalesimulationof pages 2-3, bogdanova2024mesoscalesimulationof pages 5-7) |
| Optional 3rd-parameter note | Secondary follow-on sweep at beam radius 60 µm or 80 µm, not in main grid | Beam size will shift keyhole onset and melt-pool width/depth; a larger radius should move the printability window toward higher powers/lower keyhole sensitivity, but this should be explored only after the main P–v map is established (bogdanova2024mesoscalesimulationof pages 3-5, bajaj2020precipitationduringintrinsic pages 60-63) |


*Table: This table defines a practical 70-point power–speed grid for AlSi10Mg AM Module printability mapping and matching Aconity MIDI tests. It fixes the main non-axis variables so the resulting map isolates regime transitions driven by laser power and scan speed.*

**Rationale for bounds:**

- The **power range 100–400 W** spans from insufficient energy input (expected LOF at low power / high speed) to deep-keyhole conditions (high power / low speed), covering the full Aconity MIDI operating envelope. Published AlSi10Mg LPBF studies use powers from 150–375 W on comparable 400 W-class machines (rehman2021spatterformationand pages 8-10, bogdanova2024mesoscalesimulationof pages 3-5, hyer2020understandingthelaser pages 2-5).

- The **speed range 200–2000 mm/s** ensures the map captures unstable keyhole behavior at the slow end (Bogdanova et al. observed unstable keyholing at 300 mm/s with 325–375 W) (bogdanova2024mesoscalesimulationof pages 5-7, bogdanova2024mesoscalesimulationof pages 7-9) and lack-of-fusion conditions at the fast end (Wei et al. showed penetration depths as shallow as 8 µm at 180 W / 1400 mm/s) (wei2017thealsi10mgsamples pages 12-15, wei2017thealsi10mgsamples pages 9-12).

- The **70-point grid (7 × 10)** is computationally tractable for AM Module steady-state Grid calculations while providing sufficient resolution to map regime boundaries and train an initial BOFN surrogate.

- **Hatch spacing of 130 µm** is held constant as a reference for VED interpretation and overlap criteria, matching the SLM Solutions specification (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5).

- **Third-parameter sensitivity:** Beam radius (40 → 60 or 80 µm) would meaningfully shift the keyhole threshold by reducing peak intensity. A secondary follow-on sweep at 60 µm or 80 µm beam radius is recommended after the main P–v map is established, as the Aconity MIDI supports adjustable focus. This should not be added to the primary grid to keep it interpretable (bogdanova2024mesoscalesimulationof pages 3-5).

---

## 3. Expected LPBF Windows / Regimes on the P–v Grid

Based on the literature evidence for AlSi10Mg with a ~40 µm beam radius (80 µm D4σ) and 30 µm layer thickness:

**Lack-of-fusion regime (LOF):** Expected at high speed / low power — specifically the upper-right corner of the P–v map. At P ≤ 150 W and v ≥ 1400 mm/s, melt pool penetration depths are expected to be ≤30 µm (less than one layer thickness), producing incomplete interlayer bonding. Wei et al. measured penetration depths of only 7.6–8 µm at 150–180 W / 1400 mm/s with a 70 µm spot (wei2017thealsi10mgsamples pages 12-15, wei2017thealsi10mgsamples pages 9-12). The LED < 1.0 J/cm region should show LOF porosity signatures.

**Conduction mode:** Expected in the broad central-to-lower-power band, approximately P = 150–250 W and v = 800–1600 mm/s (VED ~25–55 J/mm³). In this regime, melt pool depth-to-width ratios remain below ~0.5, and semicircular melt pool cross-sections are expected (wei2017thealsi10mgsamples pages 9-12). Rehman et al. confirmed only conduction-mode melt flow for AlSi10Mg under their conditions at moderate energy densities (rehman2021spatterformationand pages 15-17).

**Transition regime:** Expected approximately at P = 250–350 W and v = 600–1200 mm/s. Melt pool depths reach 1.5–3× layer thickness. This is the most informative region for the FLAIME BOFN surrogate, as it captures the sensitivity of melt pool geometry to small parameter changes and contains the optimal industrial process window. Hyer et al. measured melt pool depths of ~125–200 µm (4–7× the 30 µm layer thickness) at 250 W / 1000–1200 mm/s (hyer2020understandingthelaser pages 2-5).

**Keyhole regime:** Expected at high power / low speed — the lower-left corner of the P–v map. At P ≥ 300 W and v ≤ 600 mm/s, deep keyholing with unstable vapor depression is expected. Bogdanova et al. observed unstable keyholes at 300 mm/s for all tested powers (325–375 W) and quasi-stable keyholes at 900–1200 mm/s at 325–375 W (bogdanova2024mesoscalesimulationof pages 5-7, bogdanova2024mesoscalesimulationof pages 7-9). Effective absorption can rise from ~35% at 1200 mm/s to ~77% at 300 mm/s due to keyhole multiple reflections (bogdanova2024mesoscalesimulationof pages 7-9). Deep keyhole melt pool depths can exceed 400 µm (hyer2020understandingthelaser pages 2-5).

**Most informative region for BOFN surrogate:** The transition band running diagonally from approximately (200 W, 600 mm/s) to (400 W, 1800 mm/s) is where melt pool depth is most sensitive to parameter variation. Grid points in this band should be prioritized for experimental validation on the Aconity MIDI.

---

## 4. Composition-Specific Flags

### 4a. Absorptivity Behavior Relative to AlSi10Mg Calibration

Since AlSi10Mg **is** the calibration alloy for the AM Module's absorptivity model, the prefactor = 1.0 should be correct by construction. The flat-surface solid absorptivity of AlSi10Mg at 1064–1070 nm is ~0.1 (bogdanova2024mesoscalesimulationof pages 2-3, bogdanova2024mesoscalesimulationof pages 5-7). However, effective absorption in LPBF is substantially higher due to powder-bed multiple reflections and keyhole-cavity trapping, ranging from ~35% at 1200 mm/s to ~77% at 300 mm/s in single-track simulations (bogdanova2024mesoscalesimulationof pages 7-9). Thermo-Calc's account manager should verify that the AM Module's calculated absorptivity produces melt pool depths consistent with published data: at 350 W / 1200 mm/s, experimental remelting depths on comparable machines are in the range 100–200 µm (bogdanova2024mesoscalesimulationof pages 9-10, hyer2020understandingthelaser pages 2-5). If the module over-predicts depth by >50%, the prefactor may need to be reduced slightly (e.g., 0.8–0.9); if it under-predicts, the opposite adjustment applies. The native Al₂O₃ oxide skin on atomized powder increases near-IR absorptivity somewhat relative to polished bulk aluminum, but this effect should already be captured in the calibration.

### 4b. L1₂ vs. D0₂₃ Phase Handling

**Not applicable for AlSi10Mg.** The L1₂-Al₃Zr / D0₂₃-Al₃Zr metastable/stable phase question applies exclusively to Zr-bearing aluminum alloys. For AlSi10Mg Scheil or AM Module solidification calculations, the relevant phases are FCC-Al (primary), diamond-Si (eutectic), and potentially Mg₂Si and β-Al₅FeSi (with minor Fe). No special phase suspension is needed.

### 4c. Hot Cracking / Solidification Cracking

AlSi10Mg is a near-eutectic Al–Si alloy with excellent liquid flowability, and the ~10 wt% Si content effectively **eliminates solidification cracking** during LPBF (hyer2020understandingthelaser pages 1-2). This is one of the primary reasons AlSi10Mg is the most widely used aluminum LPBF alloy. No hot-cracking susceptibility flags are needed for this composition. The solidification range is narrow (~36 K, with T_liq ≈ 867 K and T_sol ≈ 831 K) (bogdanova2024mesoscalesimulationof pages 5-7), which suppresses cracking.

### 4d. Atomization and Powder Issues

No special atomization concerns for AlSi10Mg — it is a standard gas-atomized commercial LPBF powder. Unlike Zr-bearing alloys (which require Al–10Zr master alloys for dissolution), AlSi10Mg atomizes straightforwardly. Minor Mg vapor loss during printing has been reported but is generally small and does not change recommended scan parameters (wei2017thealsi10mgsamples pages 12-15). Build atmosphere should be argon or nitrogen with O₂ < 100–500 ppm (hyer2020understandingthelaser pages 1-2, bogdanova2024mesoscalesimulationof pages 3-5).

### 4e. Practical Notes for Thermo-Calc's account manager and BYU Operator

1. **Platform preheat trade-off:** 150 °C is recommended for both the simulation and Aconity MIDI builds. The base plate self-heats during long builds (measured up to ~82 °C even without active preheating) (zhu2023microstructuralanalysisof pages 1-3). Builds at 200 °C or above will coarsen the microstructure and reduce as-built strength (zhu2023microstructuralanalysisof pages 1-3, zhu2023microstructuralanalysisof pages 5-7).

2. **VED cross-check:** The single-point conditions (350 W, 1300 mm/s, 30 µm layer, 130 µm hatch) give VED ≈ 350/(1.3 × 0.13 × 0.03) ≈ 69 J/mm³. This is slightly above the Hyer et al. >99% density window of 32–54 J/mm³ (hyer2020understandingthelaser pages 1-2). If the AM Module predicts excessively deep melt pools at these conditions, consider increasing speed to 1500 mm/s (VED ≈ 60 J/mm³) or 1650 mm/s (VED ≈ 54 J/mm³, matching the SLM Solutions spec exactly).

3. **Grid computation time:** Bogdanova et al. report simulation times of ~80 min per single track at 1200 mm/s to ~20 h at 300 mm/s for their mesoscale code (bogdanova2024mesoscalesimulationof pages 5-7). The Thermo-Calc AM Module steady-state solver should be substantially faster, but the 70-point grid may still take several hours. Consider running the 7 × 10 grid overnight.

4. **Absorptivity sensitivity flag:** Bogdanova et al. explicitly state their simulation results were "highly sensitive to the absorption coefficient" (bogdanova2024mesoscalesimulationof pages 5-7). If the AM Module Grid produces melt pool depth maps that do not qualitatively match the expected regime diagram above, the absorptivity prefactor is the first parameter to adjust.

---

## 5. Citations

1. Hyer, H., Zhou, L., Park, S., et al. (2020). Understanding the Laser Powder Bed Fusion of AlSi10Mg Alloy. *Metallography, Microstructure, and Analysis*, 9, 484–502. DOI: [10.1007/s13632-020-00659-w](https://doi.org/10.1007/s13632-020-00659-w)

2. Wei, P., Wei, Z., Chen, Z., et al. (2017). The AlSi10Mg samples produced by selective laser melting: single track, densification, microstructure and mechanical behavior. *Applied Surface Science*, 408, 38–50. DOI: [10.1016/j.apsusc.2017.02.215](https://doi.org/10.1016/j.apsusc.2017.02.215)

3. Bogdanova, M., Chernyshikhin, S., Zakirov, A., et al. (2024). Mesoscale Simulation of Laser Powder Bed Fusion with an Increased Layer Thickness for AlSi10Mg Alloy. *J. Manuf. Mater. Process.*, 8, 7. DOI: [10.3390/jmmp8010007](https://doi.org/10.3390/jmmp8010007)

4. Zhu, S., Katti, I., Qiu, D., Forsmark, J.H., & Easton, M.A. (2023). Microstructural analysis of the influences of platform preheating and post-build heat treatment on mechanical properties of LPBF AlSi10Mg. *Mater. Sci. Eng. A*, 882, 145486. DOI: [10.1016/j.msea.2023.145486](https://doi.org/10.1016/j.msea.2023.145486)

5. Rehman, A.U., Mahmood, M.A., Ansari, P., et al. (2021). Spatter Formation and Splashing Induced Defects in Laser-Based Powder Bed Fusion of AlSi10Mg Alloy. *Metals*, 11, 2023. DOI: [10.3390/met11122023](https://doi.org/10.3390/met11122023)

6. Huang, Y., Fleming, T., Clark, S., et al. (2022). Keyhole fluctuation and pore formation mechanisms during laser powder bed fusion additive manufacturing. *Nature Communications*, 13. DOI: [10.1038/s41467-022-28694-x](https://doi.org/10.1038/s41467-022-28694-x)

7. Yang, T., Liu, T., Liao, W., et al. (2020). Laser powder bed fusion of AlSi10Mg: Influence of energy intensities on spatter and porosity evolution, microstructure and mechanical properties. *J. Alloys Compd.*, 849, 156300. DOI: [10.1016/j.jallcom.2020.156300](https://doi.org/10.1016/j.jallcom.2020.156300)

8. Bajaj, P., Svendsen, B., & Raabe, D. (2020). Precipitation during intrinsic heat treatment in laser additive manufacturing. DOI: [10.18154/rwth-2020-10461](https://doi.org/10.18154/rwth-2020-10461)
