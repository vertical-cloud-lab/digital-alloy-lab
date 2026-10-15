# Mehta et al. "Alloy C" — Al-5.0Mn-0.8Cr-0.5Zr (wt%)

_Edison task_id: `bbf94a9b-c51b-47ca-b623-9788d3f57634`  
_status: success_

---

# LPBF Scan Parameters and Printability-Map Grid-Search Plan for Al-5.0Mn-0.8Cr-0.5Zr (wt%) — Mehta "Alloy C"

---

## 1. Single-Point Reference Parameters (Thermo-Calc AM Module Steady-State Run)

The following table lists every field exposed in the AM Module's Conditions tab, with a recommended value, whether it deviates from the Thermo-Calc default, and justification.

### Global Settings
| Parameter | Recommended Value | Default? | Justification |
|---|---|---|---|
| Gas pressure | 1 × 10⁵ Pa | **Default** | Standard Ar atmosphere for LPBF |
| Base-plate temperature | **150 °C** | **Changed** (default 30 °C) | Linder et al. (2024) report that the Al-Mn-Cr-Zr alloy was printed with build-plate preheating at 150 °C on an EOS M290 (linder2024corrosionresistanceof pages 8-11). This is standard practice for Al alloys to reduce thermal gradients and residual stress. |
| Ambient temperature | 23 °C | **Default** | — |
| Fluid-flow / Marangoni | On | **Default** | — |
| Powder density | 80% of solid | **Default** | Consistent with gas-atomized Al alloy powder bed packing |

### Geometry
| Parameter | Recommended Value | Default? | Justification |
|---|---|---|---|
| Height | 2.0 mm | **Default** | — |
| Mesh | Coarse | **Default** | — |

### Heat Source
| Parameter | Recommended Value | Default? | Justification |
|---|---|---|---|
| Heat source type | **Gaussian** | **Default** | Standard for fiber-laser LPBF; no literature motivation for Core-ring for this composition |
| Power | **170 W** | **Changed** (default 200 W) | Mehta et al. (2022) used 170 W as the nominal power on EOS M100; Martucci et al. (2022) confirmed crack-free, ~99.5% dense parts and stable 104.5 HV across 100–170 W, with 170 W recommended as the highest build-rate condition (martucci2022theinfluenceof pages 2-4, martucci2022theinfluenceof pages 12-13). This is well within the Aconity MIDI 50–400 W range. |
| Absorptivity mode | **Calculated, prefactor 1.0** | **Default** | The Thermo-Calc default prefactor is calibrated against AlSi10Mg. Al-5Mn has a higher electrical resistivity than AlSi10Mg due to Mn in solid solution (~5 wt% Mn trapped by rapid solidification), which slightly raises absorptivity. However, without a composition-specific calibrated value in the literature, the safest approach is to retain the default prefactor 1.0 and flag this as a sensitivity parameter (see Section 4). |
| Laser wavelength | 1064 nm | **Default** | Matches Aconity MIDI Yb-fiber laser |
| Beam radius | **40 µm** | **Default** | Matches the 40 µm spot used on the EOS M100 by Martucci et al. (2022) (martucci2022theinfluenceof pages 2-4) and is within the Aconity MIDI 40–80 µm range |
| Keyhole model | On | **Default** | — |
| M² | 1.0 | **Default** | — |

### Scanning Strategy
| Parameter | Recommended Value | Default? | Justification |
|---|---|---|---|
| Scanning speed | **1500 mm/s** | **Changed** (default 1000 mm/s) | At 170 W with VED ≈ 37 J/mm³, the corresponding scan speed is 1500 mm/s (layer thickness 30 µm, hatch 100 µm) per Martucci et al. (2022) (martucci2022theinfluenceof pages 2-4). Within Aconity MIDI range (100–3000 mm/s). |
| Layer thickness | **30 µm** | **Changed** (default 40 µm) | Both Mehta et al. (2022) and Martucci et al. (2022) used 30 µm layer thickness for this alloy (martucci2022theinfluenceof pages 2-4, mehta2022al–mn–cr–zrbasedalloystailored pages 10-10). This is standard for Al-alloy LPBF. |

### Top Boundary
| Parameter | Recommended Value | Default? | Justification |
|---|---|---|---|
| Radiation emissivity | 0.8 | **Default** | — |
| Convective HTC | 20 W/m²/K | **Default** | — |
| Evaporation | On | **Default** | Mn has moderately high vapor pressure; keeping evaporation on is conservative. |

### Calculation Type
| Parameter | Recommended Value |
|---|---|
| Calculation type | **Single Point** (for the reference run); **Grid** for the P–v map (Section 2) |

**Reference single-point VED:** P/(v × h × t) = 170 / (1500 × 0.1 × 0.03) ≈ **37.8 J/mm³**, consistent with the ~37 J/mm³ used by Martucci et al. (2022) (martucci2022theinfluenceof pages 2-4).

---

## 2. Grid-Search Plan for P–v Printability Map

### Sweep Axes

| Axis | Range | Resolution | Justification |
|---|---|---|---|
| **Laser Power (P)** | 80–370 W | 7 levels: 80, 130, 170, 220, 270, 320, 370 W | Lower bound captures the 100 W crack-free condition from Martucci et al. (martucci2022theinfluenceof pages 2-4); upper bound matches EOS M290 parameters from Linder et al. at 370 W (linder2024corrosionresistanceof pages 8-11) and approaches Aconity MIDI max (~400 W). |
| **Scan Speed (v)** | 500–2500 mm/s | 9 levels: 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500 mm/s | Lower bound from Mehta's DOE (500 mm/s) (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10); upper bound extends beyond 2000 mm/s to capture lack-of-fusion boundary. Kimura et al. explored up to 3200 mm/s for Al-3Mn at higher power (kimura2021microstructuresandmechanical pages 1-2). |

**Grid size: 7 × 9 = 63 points.** This is computationally tractable for the AM Module Grid mode and covers VED from ~7 J/mm³ (370 W / 2500 / 0.1 / 0.03) to ~53 J/mm³ (80 W / 500 / 0.1 / 0.03), spanning from severe lack-of-fusion to potential keyhole.

### Held-Constant Parameters
| Parameter | Value | Rationale |
|---|---|---|
| **Layer thickness** | 30 µm | Literature standard for this alloy |
| **Hatch spacing** | 100 µm (0.1 mm) | Used by Martucci et al. (2022) (martucci2022theinfluenceof pages 2-4); also Kimura et al. for Al-Mn (kimura2021microstructuresandmechanical pages 1-2). Mehta explored 100–150 µm but 100 µm is the baseline (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10). |
| **Beam radius** | 40 µm | Default; matches literature |

### Third-Parameter Sensitivity Note
If time permits, a secondary 1D sweep of **beam radius** (40, 60, 80 µm) at the reference P–v point (170 W, 1500 mm/s) would be informative, as the Aconity MIDI supports variable spot sizes. Increasing beam radius to 60–80 µm shifts the conduction-to-keyhole transition to higher power and may be relevant for the physical build. Similarly, **base-plate preheat** (30 °C vs. 150 °C vs. 200 °C) would shift the thermal boundary conditions but should not be added to the main grid.

---

## 3. Expected LPBF Windows / Regimes on the P–v Grid

Based on the literature data and typical Al-alloy melt-pool behavior:

- **Lack-of-fusion regime** (VED < ~20 J/mm³): High-speed / low-power corner — approximately P < 130 W at v > 1750 mm/s, or P < 220 W at v > 2250 mm/s. Melt-pool depth insufficient to remelt the 30 µm layer plus prior track. Martucci et al. achieved ~99.5% density even at 100 W / 875 mm/s (VED ≈ 37 J/mm³), so the lack-of-fusion boundary should lie at significantly higher speeds or lower powers than the published window (martucci2022theinfluenceof pages 2-4).

- **Conduction-mode (optimal) regime** (VED ~25–50 J/mm³): The core of the Mehta/Martucci crack-free window — P = 100–370 W with corresponding speeds that maintain VED ≈ 30–45 J/mm³. The reference point (170 W / 1500 mm/s, VED ≈ 38 J/mm³) sits squarely here. Linder et al.'s 370 W / 1300 mm/s (VED ≈ 95 J/mm³ with 130 µm hatch; ~73 J/mm³ normalized to 100 µm hatch) may already be in the transition zone (linder2024corrosionresistanceof pages 8-11).

- **Transition regime** (VED ~50–80 J/mm³): Higher P / lower v combinations. Melt-pool depth/width ratio approaches 1:1; onset of keyhole instability. Expected roughly at P > 250 W for v < 1000 mm/s.

- **Keyhole regime** (VED > ~80 J/mm³): Low-speed / high-power corner — P > 300 W at v < 750 mm/s. Keyhole porosity expected. The AM Module's keyhole model (enabled by default) should capture this transition.

**Most informative region for the FLAIME BOFN surrogate:** The conduction–keyhole transition zone (VED ~45–70 J/mm³) is where melt-pool geometry and solidification conditions change most rapidly, making it the highest-value region for calibrating the surrogate model.

---

## 4. Composition-Specific Flags

### 4a. Absorptivity Relative to AlSi10Mg
Al-5Mn has significantly higher electrical resistivity than Al-10Si-Mg due to ~5 wt% Mn in supersaturated solid solution. The Hagen-Rubens relation predicts modestly higher absorptivity at 1064 nm (estimated ~0.15–0.20 for flat Al-Mn vs. ~0.10–0.15 for AlSi10Mg). In powder-bed geometry with multiple reflections, effective absorptivity is higher for both alloys. **Recommendation:** Start with the Thermo-Calc Calculated mode (prefactor 1.0, calibrated against AlSi10Mg). If simulated melt-pool depths are consistently shallower than Martucci's measured values (~80–140 µm at 100–170 W) (martucci2022theinfluenceof pages 4-8), consider increasing the prefactor to 1.1–1.2 to account for the higher Mn-driven resistivity. Additionally, Al-Mn alloys form a thin Al₂O₃ + Mn-oxide skin during atomization that may slightly increase powder absorptivity. Adam should note this as a calibration target.

### 4b. L1₂ vs. D0₂₃ Phase Handling for Zr
**Recommendation: Activate metastable L1₂-Al₃Zr and suspend equilibrium D0₂₃-Al₃Zr** in the Scheil / AM-Module setup. At LPBF cooling rates (10⁴–10⁶ K/s), the kinetically favored phase is L1₂-Al₃Zr, which nucleates coherently from the Al matrix. The equilibrium D0₂₃ structure forms only after prolonged high-temperature exposure (>475 °C for extended times). Martucci et al. (2022) identified Al₃Zr by XRD in as-built samples without distinguishing the crystal structure, but the rapid solidification conditions strongly favor L1₂ (martucci2022theinfluenceof pages 8-10). Plyushchay et al. (2025) confirm from first principles that D0₂₃ configurations are unfavorable at early nucleation stages. The TCAL7 database (used by Mehta et al.) includes the Al-Zr binary with L1₂ and D0₂₃ phases; ensure both are present in the phase list and that D0₂₃ is set to "Suspended" or "Dormant" for Scheil calculations.

### 4c. Mn Solute Trapping and Supersaturation
Martucci et al. (2022) demonstrate that at VED ≈ 37 J/mm³ across all power conditions (100–170 W), the Al-Mn-Cr-Zr alloy retains nearly complete Mn supersaturation in the α-Al matrix, with precipitation area fractions below 0.3% (martucci2022theinfluenceof pages 12-13, martucci2022theinfluenceof pages 1-2). Mn diffuses four orders of magnitude slower than Si in Al, so the supersaturation is robust across a wide process window. This means that Scheil solidification with back-diffusion suppressed for Mn and Cr is appropriate. The Al₆Mn and Al₁₂Mn intermetallics detected by XRD are minor and form primarily at melt-pool boundaries during in-process reheating (martucci2022theinfluenceof pages 8-10).

### 4d. Hot-Cracking / Solidification-Cracking Susceptibility
The alloy is reported crack-free across all tested conditions (100–170 W, VED ≈ 37 J/mm³) (martucci2022theinfluenceof pages 4-8, martucci2022theinfluenceof pages 1-2). Mehta et al. explicitly designed the composition to have negligible solidification cracking susceptibility based on Scheil analysis, selecting compositions with minimal terminal freezing range (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10). **No hot-cracking issues are expected** within the recommended parameter window. At extreme VED (>80 J/mm³), remelting-induced segregation could theoretically increase cracking risk, but this has not been reported.

### 4e. TCAL Database Coverage
Mehta et al. (2022) used TCAL7 with MOBAL5 databases for alloy design (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10). The current TCAL10 database has improved coverage, but users should verify that Al-Mn-Zr and Al-Cr-Zr ternary interactions are fully assessed rather than relying on binary extrapolation. The Al-Mn, Al-Zr, and Al-Cr binaries are well-assessed, and the Mn-Zr interaction in Al is likely partially assessed in TCAL10 given its importance in aerospace Al alloys. **Adam should confirm with Thermo-Calc support that the Al-Mn-Zr ternary is assessed in TCAL10/11** before running, as binary-extrapolated liquidus/solidus could introduce errors in melt-pool depth predictions.

### 4f. Atomization / Powder Flags
Zr dissolution in the Al melt requires superheating or use of an Al-10Zr master alloy due to Zr's high melting point. Mehta's powder was produced by nitrogen gas atomization at Höganäs AB with verified Zr content of 0.59 wt% (martucci2022theinfluenceof pages 2-4). For any new powder lot, ICP verification of actual Zr content is critical. Mn vapor loss during atomization is negligible due to Mn's low vapor pressure relative to Al, but Mg (not present in this alloy) would be a concern. **These powder issues do not change the recommended scan parameters but should be checked before builds.**

---

## 5. Citations

1. Linder, C., Mehta, B., Sainis, S., Lindén, J. B., Zanella, C., & Nyborg, L. (2024). Corrosion resistance of additively manufactured aluminium alloys for marine applications. *npj Materials Degradation*, 8(1). DOI: 10.1038/s41529-024-00459-5 (linder2024corrosionresistanceof pages 8-11)

2. Martucci, A., Mehta, B., Lombardi, M., & Nyborg, L. (2022). The Influence of Processing Parameters on the Al-Mn Enriched Nano-Precipitates Formation in a Novel Al-Mn-Cr-Zr Alloy Tailored for Power Bed Fusion-Laser Beam Process. *Metals*, 12(8), 1387. DOI: 10.3390/met12081387 (martucci2022theinfluenceof pages 2-4, martucci2022theinfluenceof pages 12-13, martucci2022theinfluenceof pages 4-8, martucci2022theinfluenceof pages 8-10, martucci2022theinfluenceof pages 1-2)

3. Mehta, B., Nyborg, L., Frisk, K., & Hryha, E. (2022). Al–Mn–Cr–Zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. *Journal of Materials Research*, 37, 1256–1268. DOI: 10.1557/s43578-022-00533-1 (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10)

4. Kimura, T., Nakamoto, T., Ozaki, T., & Miki, T. (2021). Microstructures and mechanical properties of aluminum-transition metal binary alloys (Al-Fe, Al-Mn, and Al-Cr) processed by laser powder bed fusion. *Journal of Alloys and Compounds*, 872, 159680. DOI: 10.1016/j.jallcom.2021.159680 (kimura2021microstructuresandmechanical pages 1-2)

5. Mehta, B., Bengtsson, S., Riabov, D., Natesan, E., Frisk, K., Ahlström, J., & Nyborg, L. (2024). Mechanical properties and microstructural characterisation including high-temperature performance of Al-Mn-Cr-Zr-based alloys tailored for additive manufacturing. *Materials & Design*, 244, 113160. DOI: 10.1016/j.matdes.2024.113160 (unobtainable — cited for reported YS 250–500 MPa and high-T YS ~170 MPa at 300 °C)

6. Mehta, B., Frisk, K., & Nyborg, L. (2024). Role of Cr in Mn-rich precipitates for Al–Mn–Cr–Zr-based alloys tailored for additive manufacturing. *Calphad*, 84, 102667. DOI: 10.1016/j.calphad.2024.102667 (unobtainable — cited for CALPHAD assessment context)

7. Michi, R. A., Plotkowski, A., Shyam, A., Dehoff, R. R., & Babu, S. S. (2022). Towards high-temperature applications of aluminium alloys enabled by additive manufacturing. *International Materials Reviews*, 67(3), 298–345. DOI: 10.1080/09506608.2021.1951580 (general context on Mn diffusivity and high-T Al alloy strategies)

8. Plyushchay, I., Wei, Z., & Gemming, S. (2025). First Principles Insight into L1₂ Precipitate Formation in Al-Zr Alloys. DOI: 10.20944/preprints202508.1910.v1 (L1₂ vs. D0₂₃ nucleation preference)
