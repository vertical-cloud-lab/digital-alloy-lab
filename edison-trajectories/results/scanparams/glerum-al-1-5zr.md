# Glerum et al. Al-1.5 Zr supersaturated LPBF (wt%)

_Edison task_id: `5e833ec8-8bbd-4ada-8eb6-0e6b04391224`  
_status: success_

---

# LPBF Scan Parameters and Printability-Map Grid-Search Plan for Al-1.5 Zr (wt%)

**Target Composition:** Al–1.5 Zr (wt%), balance Al. Supersaturated binary for L1₂-Al₃Zr nucleation studies.

---

## 1. Single-Point Reference Parameters

The following table provides a complete Thermo-Calc AM Module steady-state Single-Point parameter set for Al-1.5Zr. Four parameters are changed from Thermo-Calc defaults; all deviations are justified by the Al-Zr LPBF literature.

| Parameter | Recommended Value | TC Default | Changed? | Justification/Citation |
|---|---:|---:|---|---|
| Global – Gas pressure | 1e5 Pa | 1e5 Pa | No | Leave at Thermo-Calc default; no Al-1.5Zr-specific literature found that motivates deviation for the steady-state starting run. |
| Global – Base-plate temperature | 200 °C | 30 °C | Yes | Raise preheat for this Al-rich alloy to reduce thermal gradients/stresses and broaden the non-cracking window; treat as a cautious Al-alloy starting point rather than a hard requirement. Rapid-solidification retention of metastable L1₂-Al₃Zr still occurs in LPBF at high cooling rates, so this is a secondary tuning lever, not the primary one (mair2022microstructuralfeaturesand pages 6-7, anne2023laserpowderbedfusion pages 116-121, anne2023laserpowderbedfusion pages 85-89). |
| Global – Ambient temperature | 23 °C | 23 °C | No | Leave at default. |
| Global – Fluid-flow / Marangoni | On | On | No | Leave at default; melt-pool flow is important in LPBF defect formation and pool geometry (forien2020detectingkeyholepore pages 12-15). |
| Global – Powder density | 80% of solid | 80% of solid | No | Leave at default; consistent with Thermo-Calc guidance and no Al-1.5Zr-specific override found. |
| Geometry – Height | 2.0 mm | 2.0 mm | No | Leave at default for preliminary steady-state AM-module mapping. |
| Geometry – Mesh | Coarse | Coarse | No | Leave at default for preliminary screening. |
| Heat source type | Gaussian | Gaussian | No | Use Gaussian; no composition-specific evidence here requiring core-ring as the starting point. |
| Heat source – Power | 200 W | 200 W | No | Keep default 200 W; this matches successful Al-Zr-bearing LPBF/SLM literature starting points and stays inside Aconity MIDI capability. Croteau and Griffiths both used 200 W for dense Al-Mg-Zr builds; Glerum’s broader Al-Zr studies span this value (croteau2018microstructureandmechanical pages 2-3, griffiths2018effectoflaser pages 1-2, anne2023laserpowderbedfusion pages 35-39). |
| Heat source – Absorptivity mode | Calculated, prefactor 1.0 | Calculated, prefactor 1.0 | No | Do not override. No composition-specific calibrated absorptivity for Al-1.5Zr was found; Al alloys are low-absorptivity at ~1070 nm and powder absorptivity is higher than bulk, but this is insufficient to justify a fixed constant. Since this alloy is overwhelmingly Al-rich, use Thermo-Calc’s calculated mode as the least-assumptive start (reed2024timeresolvedabsorptancein pages 27-31, alsaddah2023multilaserpowderbed pages 52-57). |
| Heat source – Laser wavelength | 1064 nm | 1064 nm | No | Leave at default; matches the near-IR fiber-laser class used in the cited LPBF studies and the Aconity MIDI envelope (croteau2018microstructureandmechanical pages 2-3, griffiths2018effectoflaser pages 1-2). |
| Heat source – Beam radius | 45 µm | 40 µm | Yes | Set 45 µm radius (≈90 µm diameter) to align better with Al-Zr literature analogues and typical Aconity operation; Croteau used ~90 µm spot size, and Glerum’s experiments used ~80–100 µm spots (croteau2018microstructureandmechanical pages 2-3, anne2023laserpowderbedfusion pages 35-39). |
| Heat source – Keyhole model | On | On | No | Leave at default; useful because this alloy’s printability map should explicitly resolve conduction/transition/keyhole boundaries (ayrookuzhy2024theeffectof pages 25-29, forien2020detectingkeyholepore pages 12-15). |
| Heat source – Beam-quality factor M² | 1.0 | 1.0 | No | Leave at default; no composition-specific reason to alter. |
| Scanning – Speed | 400 mm/s | 1000 mm/s | Yes | Lower from default to enter the experimentally relevant Al-Zr window. Glerum’s Al-Zr optimization spans ~150–450 mm/s at 175 W with best density near VED ≈233 J/mm³; Croteau/Griffiths used 200 mm/s at 200 W for Al-Mg-Zr. At 200 W, 400 mm/s is a moderate, less aggressive starting point that should remain well within conduction/transition rather than obvious lack-of-fusion (anne2023laserpowderbedfusion pages 162-168, croteau2018microstructureandmechanical pages 2-3, griffiths2018effectoflaser pages 1-2). |
| Scanning – Layer thickness | 30 µm | 40 µm | Yes | Use 30 µm as the more conservative Al-alloy LPBF starting point and because Al-Zr-bearing analogues used 30 µm successfully; thinner layers help maintain melt depth > layer thickness and reduce lack-of-fusion risk (croteau2018microstructureandmechanical pages 2-3, mair2022microstructuralfeaturesand pages 1-2, anne2023laserpowderbedfusion pages 35-39). |
| Top boundary – Radiation emissivity | 0.8 | 0.8 | No | Leave at default. |
| Top boundary – Convective HTC | 20 W/m²/K | 20 W/m²/K | No | Leave at default. |
| Top boundary – Evaporation | On | On | No | Leave at default; useful for Al LPBF thermal balance and possible vaporization effects. |
| Calculation type | Single Point | — | Yes | Use Single Point for the reference steady-state calculation requested before the Grid sweep. |


*Table: This table gives a complete Thermo-Calc AM Module starting parameter set for Al-1.5Zr, marking which settings stay at default and which are changed for a literature-grounded LPBF starting point on an Aconity-like system.*

**Summary of deviations from default:**

- **Base-plate temperature → 200 °C** (from 30 °C): Al-alloy LPBF commonly uses elevated preheat (150–200 °C) to reduce thermal gradients and residual stress. For Al-1.5Zr specifically, the rapid solidification cooling rates in LPBF (~10⁵–10⁶ K/s) remain more than sufficient to retain metastable L1₂-Al₃Zr even with modest preheat (mair2022microstructuralfeaturesand pages 6-7, anne2023laserpowderbedfusion pages 116-121). Note: if the primary interest is maximizing cooling rate for Zr supersaturation retention, a 30 °C base plate could also be tested as a secondary point.

- **Beam radius → 45 µm** (from 40 µm): Croteau et al. used a ~45 µm radius (90 µm spot diameter) for Al-Mg-Zr SLM on a Concept Laser M2 (croteau2018microstructureandmechanical pages 2-3), and Glerum's Al-Zr experiments used 80–100 µm spots (anne2023laserpowderbedfusion pages 35-39). A 45 µm radius is within the Aconity MIDI 40–80 µm range and better matches published Al-Zr analogues.

- **Scan speed → 400 mm/s** (from 1000 mm/s): The Al-Zr literature consistently uses much lower scan speeds than the TC default. Glerum's Al-Zr multilayer optimization found peak density near VED ≈ 233 J/mm³ at ~150–450 mm/s with 175 W (anne2023laserpowderbedfusion pages 162-168). Croteau et al. and Griffiths et al. used 200 mm/s at 200 W for Al-Mg-Zr (croteau2018microstructureandmechanical pages 2-3, griffiths2018effectoflaser pages 1-2, griffiths2018effectoflaser pages 2-3). At 200 W / 400 mm/s / 30 µm layer / 80 µm hatch, VED ≈ 208 J/mm³, well within the demonstrated dense-build window.

- **Layer thickness → 30 µm** (from 40 µm): Standard for Al-alloy LPBF. Croteau et al. used 30 µm layers (croteau2018microstructureandmechanical pages 2-3); Mair et al. also used 30 µm for Al-Mn-Ti-Zr (mair2022microstructuralfeaturesand pages 1-2). Thinner layers ensure melt-pool depth exceeds layer thickness, reducing lack-of-fusion risk.

---

## 2. Grid-Search Plan for P–v Printability Map

### Constant parameters during sweep
| Parameter | Value | Rationale |
|---|---|---|
| Layer thickness | 30 µm | Held constant; Al-alloy standard (croteau2018microstructureandmechanical pages 2-3, mair2022microstructuralfeaturesand pages 1-2) |
| Hatch spacing | 80 µm | Mid-range of Glerum's 70–90 µm and consistent with VED ≈ 233 J/mm³ target (anne2023laserpowderbedfusion pages 35-39, anne2023laserpowderbedfusion pages 162-168) |
| Beam radius | 45 µm | Held constant at literature-matched value |
| Base-plate temp | 200 °C | Held constant |
| All other params | Per Section 1 | Defaults as specified above |

### Grid axes and bounds

| Axis | Min | Max | Steps | Spacing | Rationale |
|---|---|---|---|---|---|
| **Laser power (P)** | 100 W | 400 W | 7 | ~50 W increments (100, 150, 200, 250, 300, 350, 400) | Spans from below the Croteau/Griffiths 200 W optimum to the Aconity MIDI maximum. Glerum used 175–500 W (anne2023laserpowderbedfusion pages 35-39, anne2023laserpowderbedfusion pages 162-168). |
| **Scan speed (v)** | 100 mm/s | 1000 mm/s | 10 | ~100 mm/s increments (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000) | Covers the full demonstrated Al-Zr range (200–675 mm/s in Glerum, 200–800 mm/s in Croteau) and extends above to capture lack-of-fusion onset (croteau2018microstructureandmechanical pages 2-3, anne2023laserpowderbedfusion pages 35-39). |

**Total grid: 7 × 10 = 70 points.** This is manageable for the AM Module Grid calculation and provides sufficient resolution to map conduction/transition/keyhole boundaries and identify the optimal VED corridor (approximately 150–300 J/mm³ based on literature).

### VED coverage
At fixed t = 30 µm, h = 80 µm:
- Minimum VED: 100 W / (1000 mm/s × 0.080 mm × 0.030 mm) = 41.7 J/mm³ (deep lack-of-fusion)
- Maximum VED: 400 W / (100 mm/s × 0.080 mm × 0.030 mm) = 1667 J/mm³ (extreme keyhole)
- Literature optimum: ~200–250 J/mm³ (croteau2018microstructureandmechanical pages 2-3, anne2023laserpowderbedfusion pages 162-168, croteau2018microstructureandmechanical pages 1-2)

### Third parameter note
**Beam radius** (or equivalently, base-plate preheat) could meaningfully shift the processing window. Increasing beam radius from 45 to 80 µm would broaden the melt pool and reduce peak intensity, shifting the keyhole threshold to higher powers. If resources permit, a secondary 7 × 10 grid at beam radius = 70 µm would be informative but should not be included in the primary sweep.

---

## 3. Expected LPBF Windows / Regimes on the P–v Grid

Based on the thermophysical properties of near-pure aluminum (high thermal conductivity ~237 W/m·K, high reflectivity at 1064 nm, low melting point ~660 °C) and the Al-Zr literature:

**Lack-of-fusion region (high v, low P):** Expected at VED < ~100 J/mm³, approximately P < 150 W at v > 600 mm/s, or P = 200 W at v > 800 mm/s. Melt-pool depth will be less than the 30 µm layer thickness, producing unbonded interlayer regions and incomplete Zr dissolution (anne2023laserpowderbedfusion pages 162-168).

**Conduction-mode region:** Expected at moderate VED ~100–200 J/mm³. At P = 200 W, this spans approximately v = 400–800 mm/s. Melt pools are wide and shallow (aspect ratio < 0.5). This regime is well-suited for stable processing but may not produce sufficient melt-pool depth for complete Zr dissolution in elemental blends (ayrookuzhy2024theeffectof pages 25-29, forien2020detectingkeyholepore pages 12-15).

**Transition region (target for optimal L1₂ nucleation):** VED ~200–350 J/mm³, where melt-pool depth/width aspect ratio is 0.5–2.0. At P = 200 W, this corresponds to v ≈ 200–400 mm/s. This is where Croteau, Griffiths, and Glerum achieved >99% density with bimodal grain structures (fine equiaxed L1₂-nucleated grains at melt-pool base + columnar grains at top) (croteau2018microstructureandmechanical pages 2-3, griffiths2020additivemanufacturingof pages 70-75, croteau2018microstructureandmechanical pages 1-2). **This is the most informative region for the FLAIME BOFN surrogate**, as it captures the G/R conditions required for intrinsic equiaxed nucleation by primary L1₂-Al₃Zr.

**Keyhole region (high P, low v):** Expected at VED > ~400 J/mm³, approximately P > 300 W at v < 200 mm/s, or P = 400 W at v < 400 mm/s. Deep keyhole formation with spherical pore defects. Glerum observed ~400 µm melt-pool depths at 350 W / 200 mm/s in single-line scans (anne2023laserpowderbedfusion pages 85-89), confirming deep penetration at these conditions. While keyhole-mode data are useful for model validation, this regime should be avoided for physical builds.

**Key insight for BOFN surrogate:** The transition/conduction boundary (~200 J/mm³) is where L1₂-Al₃Zr primary precipitate density and equiaxed grain fraction vary most steeply with process parameters, making it the highest-information region for Bayesian optimization.

---

## 4. Composition-Specific Flags

### 4a. Absorptivity behaviour relative to AlSi10Mg
Al-1.5Zr is 98.5 wt% Al and lacks the Si content that raises absorptivity in AlSi10Mg. Bulk aluminum absorptivity at ~1070 nm is approximately 0.15 (reed2024timeresolvedabsorptancein pages 27-31), with powder-bed absorptivity roughly 2× higher due to multiple scattering (alsaddah2023multilaserpowderbed pages 52-57). The Al₂O₃ native oxide layer on atomized powder provides some absorptivity enhancement but likely less than AlSi10Mg's eutectic Si network. **Recommendation:** Use Thermo-Calc's Calculated absorptivity mode with prefactor 1.0 as a starting point. If the AM Module's calculated absorptivity appears unrealistically high (i.e., calibrated primarily against AlSi10Mg's higher absorptivity), Thermo-Calc's account manager should flag this and consider testing prefactor values of 0.85–1.0 in a sensitivity study.

### 4b. L1₂ vs. D0₂₃ phase handling — CRITICAL
**Recommendation: Set metastable L1₂-Al₃Zr as ACTIVE and equilibrium D0₂₃-Al₃Zr as SUSPENDED** in the Scheil and AM Module phase setup.

Justification: Thermo-Calc CALPHAD equilibrium calculations predict D0₂₃ as the thermodynamically stable form (lower Gibbs free energy), but LPBF cooling rates of 10⁵–10⁶ K/s strongly favor L1₂ nucleation due to its lower liquid–matrix interface energy (0.1276 vs. 0.1324 J/m² at 800 °C) and structural coherency with the fcc-Al matrix (griffiths2020additivemanufacturingof pages 79-82). Experimentally, D0₂₃ is never observed in as-fabricated LPBF Al-Zr parts; only L1₂ forms (anne2023laserpowderbedfusion pages 85-89, mair2022microstructuralfeaturesand pages 6-7). L1₂-Al₃Zr is metastable up to ~550 °C and can remain stable for hundreds of hours above 450 °C due to the extremely low diffusivity of Zr in Al (1.20 × 10⁻²⁰ m²/s at 400 °C) (anne2023laserpowderbedfusion pages 85-89, griffiths2020additivemanufacturingof pages 46-49). The L1₂ → D0₂₃ transformation requires long thermal exposure at 450–500 °C (griffiths2020additivemanufacturingof pages 102-106).

### 4c. Hot-cracking / solidification-cracking susceptibility
Binary Al-1.5Zr with L1₂ primary precipitates acting as grain refiners is reported as **crack-free** in LPBF (anne2023laserpowderbedfusion pages 81-85, croteau2018microstructureandmechanical pages 1-2). The absence of long-range solidification cracking is attributed to the equiaxed grain structure nucleated by primary Al₃Zr particles, which eliminates the columnar-dendritic network vulnerable to hot tearing. No special hot-cracking precautions are needed beyond maintaining VED within the demonstrated window.

### 4d. Atomization / feedstock notes
Dissolving 1.5 wt% Zr requires an Al-10Zr or Al-5Zr master alloy rather than elemental Zr due to Zr's high melting point (~1855 °C) and limited dissolution kinetics in an Al melt. The wide liquidus–solidus gap (Al melting ~661 °C, Al-1.5Zr liquidus ~1130 °C) means elemental powder blends require high energy input for complete Zr dissolution (anne2023laserpowderbedfusion pages 31-35). For pre-alloyed atomized powder (recommended for Aconity MIDI builds), this is not an issue. **This does not change the CALPHAD/AM-Module input** — the simulation assumes a homogeneous liquid composition regardless of feedstock form.

### 4e. Base-plate preheat sensitivity
If Thermo-Calc's account manager wishes to test the effect of preheat on the L1₂ nucleation window, running the single-point calculation at both 30 °C and 200 °C base-plate temperature would be informative. The primary effect is on the intrinsic heat-treatment temperature–time profile in the 300–650 °C range where secondary L1₂ precipitation occurs during subsequent layer passes (anne2023laserpowderbedfusion pages 116-121).

---

## 5. Citations

1. **Glerum (2023)** — J.A. Glerum, "Laser Powder-Bed Fusion of Elemental Powder Blends to Manufacture Precipitation and Oxide-Dispersion Strengthened Aluminum Alloys," PhD Thesis, 2023. DOI: 10.21985/n2-k0nf-gm36 (anne2023laserpowderbedfusion pages 35-39, anne2023laserpowderbedfusion pages 81-85, anne2023laserpowderbedfusion pages 31-35, anne2023laserpowderbedfusion pages 85-89, anne2023laserpowderbedfusion pages 162-168, anne2023laserpowderbedfusion pages 185-191, anne2023laserpowderbedfusion pages 116-121)

2. **Croteau et al. (2018)** — J.R. Croteau, S. Griffiths, M.D. Rossell, C. Leinenbach, C. Kenel, V. Jansen, D.N. Seidman, D.C. Dunand, N.Q. Vo, "Microstructure and mechanical properties of Al-Mg-Zr alloys processed by selective laser melting," *Acta Materialia* 153:35–44. DOI: 10.1016/j.actamat.2018.04.053 (croteau2018microstructureandmechanical pages 2-3, croteau2018microstructureandmechanical pages 9-10, croteau2018microstructureandmechanical pages 3-4, croteau2018microstructureandmechanical pages 1-2)

3. **Griffiths et al. (2018)** — S. Griffiths, M.D. Rossell, J. Croteau, N.Q. Vo, D.C. Dunand, C. Leinenbach, "Effect of laser rescanning on the grain microstructure of a selective laser melted Al-Mg-Zr alloy," *Materials Characterization* 143:34–42. DOI: 10.1016/j.matchar.2018.03.033 (griffiths2018effectoflaser pages 1-2, griffiths2018effectoflaser pages 2-3, griffiths2018effectoflaser pages 9-9)

4. **Griffiths (2020)** — S.J. Griffiths, "Additive Manufacturing of L12 Precipitate Strengthened Nickel and Aluminum Alloys," PhD Thesis, EPFL, 2020. DOI: 10.5075/epfl-thesis-7962 (griffiths2020additivemanufacturingof pages 46-49, griffiths2020additivemanufacturingof pages 70-75, griffiths2020additivemanufacturingof pages 79-82, griffiths2020additivemanufacturingof pages 102-106)

5. **Mair et al. (2022)** — P. Mair, I. Letofsky-Papst, G. Leichtfried, "Microstructural features and mechanical properties of a novel Ti- and Zr-modified Al-Mn alloy processed by laser powder bed fusion," *J. Alloys Compd.* 897:163156. DOI: 10.1016/j.jallcom.2021.163156 (mair2022microstructuralfeaturesand pages 1-2, mair2022microstructuralfeaturesand pages 6-7)

6. **Reed (2024)** — M.K. Reed, "Time-Resolved Absorptance in Laser-Powder Bed Fusion: Effect of Gaussian and Novel Beam Shapes," Thesis, 2024. (reed2024timeresolvedabsorptancein pages 27-31)

7. **Alsaddah (2023)** — M. Alsaddah, "Multi-laser powder bed fusion using 808 nm sources," Thesis, 2023. (alsaddah2023multilaserpowderbed pages 52-57)

8. **Forien et al. (2020)** — J.-B. Forien, N.P. Calta, P.J. DePond, G.M. Guss, T.T. Roehling, M.J. Matthews, "Detecting keyhole pore defects and monitoring process signatures during LPBF," *Additive Manufacturing* 35:101336. DOI: 10.1016/j.addma.2020.101336 (forien2020detectingkeyholepore pages 12-15, forien2020detectingkeyholepore pages 9-12)

9. **Ayrookuzhy (2024)** — E.V. Ayrookuzhy, "The effect of beam pulsing on laser beam processing of Ti-6Al-4V using a prototype laser additive manufacturing platform," Thesis, 2024. (ayrookuzhy2024theeffectof pages 25-29)
