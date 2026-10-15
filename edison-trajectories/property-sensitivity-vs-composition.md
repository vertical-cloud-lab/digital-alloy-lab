## Quantitative Sensitivity of LPBF-Relevant Al-Alloy Properties to Compositional Changes

This report synthesizes published quantitative data on how small compositional changes affect key properties of interest for LPBF aluminum alloys, organized by property category. Where experimental data is sparse, CALPHAD/DFT inference is flagged.

---

### 1. Freezing Range and Solidification Crack Susceptibility Index (CSI)

The Kou crack susceptibility index, defined as CSI = max|dT/d(f_S)^{1/2}|, is the most widely used metric for LPBF-relevant solidification cracking and is exquisitely sensitive to composition near certain critical concentrations.

**Al-Si binary:** The CSI peaks sharply at very low Si (~0.5 wt% Si), where CSI = 5875 °C at f_S^{1/2} = 0.988. By 10 wt% Si the CSI drops to ~95 °C, a ~60× reduction. The maximum solid solubility of Si in Al (~1.7 wt%) corresponds to the largest freezing range (~76 °C). Experimentally in LPBF, alloys at 1.0 and 2.0 wt% Si always exhibited solidification cracks, while 4.0 wt% Si and above were crack-free (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking pages 4-5). This represents an extreme compositional cliff: a change of just ~2 wt% Si (from 2 to 4 wt%) transitions from cracked to crack-free.

**Al-Mg binary:** The CSI peak occurs at ~2.5 wt% Mg without back diffusion and shifts to ~5.5 wt% Mg when back diffusion at 100 °C/s cooling rate is considered (zhang2021predictionofcracking pages 7-9).

**Al-Cu and 2xxx:** CSI peaks between 1–5 wt% Cu (shifting with cooling rate). For the Al-Cu-Mg ternary, maximum vulnerability is near Al-2Cu-1.5Mg (wt%). The 2xxx and 7xxx series show maximum CSI values up to ~12 (×1000 scale), compared to ~7 for 6xxx (zhang2021predictionofcracking pages 5-7, zhang2021predictionofcracking pages 14-15).

**Al-Mg-Si (6xxx):** CSI is highest when w(Mg)/w(Si) ≈ 1.6–2.0 (near Mg₂Si stoichiometry ~1.73). Most 6xxx alloys fall in CSI ~3–5; Cu additions (0.2–1.2 wt%) increase susceptibility (zhang2021predictionofcracking pages 7-9, zhang2021predictionofcracking pages 14-15).

**7xxx (Al-Zn-Mg-Cu):** Unmodified Al-7075 has a very high CSI of ~6504 °C. Adding Zn+Mg reduces it to 5966 °C, and 3.74 wt% Si addition further reduces it to 3960 °C—a ~39% reduction that transitions from crack-prone to crack-free in LPBF, with simultaneous grain refinement from 59 µm to 15 µm (li2021investigationofsolidification pages 1-2).

**Implication for FLAIME:** Near CSI peaks, a 0.1 wt% change can shift CSI by hundreds of °C; near eutectic compositions CSI is flat. TC/CALPHAD grid spacing of ≤0.1 wt% is needed near CSI peaks (dilute hypo-eutectic regimes), while 0.5–1 wt% grids suffice near eutectic compositions.

---

### 2. Yield Strength — Solid Solution Strengthening

The functional form is Δσ = H·c^n, where c is solute concentration and n ranges from 0.5 (Fleischer, weak pinning) to 0.75 (Labusch, strong pinning) (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26). First-principles DFT calculations by Leyson et al. predict τ_y0 = K·c^{2/3} (Labusch scaling) with the following zero-temperature coefficients (leyson2010quantitativepredictionof pages 3-4):

- **Cr:** K = 871 MPa/(atomic fraction)^{2/3} — strongest solute strengthener
- **Cu:** K = 430 MPa/(atomic fraction)^{2/3}
- **Mg:** K = 422 MPa/(atomic fraction)^{2/3}
- **Si:** K = 170 MPa/(atomic fraction)^{2/3} — weakest of the four

DFT-computed misfit volumes: Mg = +5.7 Å³, Cu = −5.6 Å³, Cr = −11.7 Å³, Si = −2.6 Å³ (leyson2010quantitativepredictionof pages 1-2).

Experimental benchmarks: For Al-Mg, Sherby et al. report H ≈ 15 MPa/(at.%)^{0.75} (ryen2006strengtheningmechanismsin pages 1-2). Kendig & Miracle use a c^{1/2} form and report Al-Mg yield strengths of 80, 115, and 130 MPa at 2, 5, and 6.5 wt% Mg respectively (kendig2002strengtheningmechanismsof pages 3-4). Mn gives ~90 MPa strengthening increment at only 0.6 at.% (considerably higher per-atom than Mg), while Fe contributes ~89 MPa up to 0.5 wt% in rapidly solidified alloys (michi2022towardshightemperatureapplications pages 19-21). Zn and Li have very low strengthening ability per atom (michi2022towardshightemperatureapplications pages 19-21).

The full table of collected coefficients is provided below:

| Element | Functional form reported | Coefficient / representative magnitude | Units | Basis / notes | Source |
|---|---|---:|---|---|---|
| Mg | \(\tau_{y0}=Kc^{2/3}\) | 422 | MPa per atomic-fraction^(2/3) | DFT/Leyson zero-temperature solute-strengthening coefficient for dilute Al-Mg | (leyson2010quantitativepredictionof pages 3-4) |
| Mg | \(\Delta\sigma = Hc^n\) | \(n\approx0.75\), \(H\approx15\) | MPa per (at.% Mg)^n | Experimental high-purity Al-Mg yield-stress fit reported by Sherby et al., summarized by Ryen et al. | (ryen2006strengtheningmechanismsin pages 1-2) |
| Mg | composition-strength increment | ~175 at 18.6 at.% Mg | MPa | AM/high-temperature review representative solid-solution strengthening magnitude | (michi2022towardshightemperatureapplications pages 19-21) |
| Cu | \(\tau_{y0}=Kc^{2/3}\) | 430 | MPa per atomic-fraction^(2/3) | DFT/Leyson zero-temperature solute-strengthening coefficient for dilute Al-Cu | (leyson2010quantitativepredictionof pages 3-4) |
| Cu | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | General experimental range for substitutional solutes in Al; Cu-specific \(H\) not given in excerpt | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Cu | AM-specific magnitude | not numerically isolated | — | Michi review notes Cu has high strengthening potential, but no standalone MPa coefficient extracted in excerpt | (michi2022towardshightemperatureapplications pages 19-21) |
| Cr | \(\tau_{y0}=Kc^{2/3}\) | 871 | MPa per atomic-fraction^(2/3) | Highest Leyson coefficient among Mg/Cu/Cr/Si listed; strong dilute solute strengthener in Al | (leyson2010quantitativepredictionof pages 3-4) |
| Cr | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | General experimental range; Cr-specific \(H\) not given in excerpt | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Cr | AM-specific magnitude | not numerically isolated | — | Michi review identifies Cr as a promising low-diffusivity high-temperature solute, but no MPa coefficient quoted in excerpt | (michi2022towardshightemperatureapplications pages 19-21) |
| Si | \(\tau_{y0}=Kc^{2/3}\) | 170 | MPa per atomic-fraction^(2/3) | DFT/Leyson zero-temperature solute-strengthening coefficient for dilute Al-Si | (leyson2010quantitativepredictionof pages 3-4) |
| Si | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | General experimental range; Si-specific \(H\) not given in excerpt | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Si | AM-specific magnitude | not numerically isolated | — | Michi review does not quote a standalone MPa coefficient for Si in solid solution in the excerpt | (michi2022towardshightemperatureapplications pages 19-21) |
| Mn | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | Ryen notes Mn gives considerably higher strengthening per atom than Mg, but no explicit \(H\) value in excerpt | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Mn | composition-strength increment | ~90 at 0.6 at.% Mn | MPa | Representative magnitude from AM/high-temperature review | (michi2022towardshightemperatureapplications pages 19-21) |
| Zn | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | No Zn-specific Leyson coefficient in available excerpts; general solid-solution scaling only | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Zn | AM-specific magnitude | very low; no numeric coefficient quoted | — | Michi review states Zn has very low strengthening ability in Al | (michi2022towardshightemperatureapplications pages 19-21) |
| Fe | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | No Fe-specific Leyson coefficient in available excerpts; general scaling only | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Fe | composition-strength increment | ~89 up to 0.5 wt.% Fe | MPa | Representative predicted full-solid-solution strengthening in rapidly solidified Al-Fe from AM review | (michi2022towardshightemperatureapplications pages 19-21) |
| Li | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | No Li-specific coefficient in available excerpts | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Li | AM-specific magnitude | very low; no numeric coefficient quoted | — | Michi review states Li has very low strengthening ability in Al | (michi2022towardshightemperatureapplications pages 19-21) |
| Ni | \(\Delta\sigma = Hc^n\) | \(n\approx0.5-0.75\) | exponent only | No Ni-specific Leyson or Ryen coefficient in available excerpts | (ryen2006strengtheningmechanismsin pages 1-2, prach2021influenceofzr pages 21-26) |
| Ni | AM-specific magnitude | not numerically isolated | — | Available Michi excerpt discusses Ni-containing AM alloys indirectly, but no standalone solid-solution MPa coefficient | (michi2022towardshightemperatureapplications pages 19-21) |


*Table: This table compiles the quantitative solid-solution strengthening coefficients and representative magnitudes available in the retrieved evidence for common solutes in aluminum. It is useful for comparing which elemental axes are likely to have short surrogate length scales and where the literature is sparse.*

**Implication for FLAIME:** For Cr and Mn axes, the surrogate needs a shorter lengthscale prior; 0.1 wt% changes produce measurable (5–15 MPa) strength differences. For Zn, much coarser resolution (1+ wt%) suffices. Dispensing accuracy of 0.01 g on 10 g charges (~0.1 wt% resolution) is adequate for most axes except Cr and Mn near solubility limits.

---

### 3. LPBF Tensile Properties — Al-Si Composition Dependence

In LPBF binary Al-Si (Hyer et al., Acta Materialia 2021), yield strength increases from ~57 MPa (0.5 wt% Si) to ~326 MPa (16 wt% Si), while elongation drops from ~29% to ~5.2%. UTS ranges from ~86 to ~485 MPa across the same range. Elastic modulus increases from ~41 to ~72 GPa. Cooling rates estimated at 10⁶–10⁷ K/s (hyer2021compositiondependentsolidificationcracking pages 9-10). This gives an approximate sensitivity of ~17 MPa YS per wt% Si across the 0.5–16% range (nonlinear; steeper at lower Si).

---

### 4. Scalmalloy (Al-Mg-Sc-Zr) — Precipitation Strengthening Sensitivity

Scalmalloy® (Al-4.5Mg-0.75Sc-0.35Zr-0.45Mn nominal) exhibits dramatic aging response:
- **As-built LPBF:** YS = 256–352 MPa, UTS = 349–412 MPa, elongation = 19–24% (cerri2024mainheattreatments pages 5-7, ren2024studyonmicrostructure pages 8-10)
- **After direct aging (325°C/4h):** YS = 456–535 MPa, UTS = 512–560 MPa, elongation = 8–13% (ren2024studyonmicrostructure pages 8-10, lu2023microstructuralevaluationand pages 6-9)

This represents a ~200 MPa YS increment from precipitation of Al₃(Sc,Zr) nanoprecipitates (~1.5–3.3 nm radius, number density ~1.4×10²⁴ m⁻³, volume fraction ~2.5%) (glerum2020synthesisofprecipitationstrengthened pages 7-8). The Orowan strengthening contribution from L1₂ precipitates is estimated at ~104 MPa for r = 3.3 nm and V_f = 0.0025, with combined shearing contributions of ~160 MPa (adetan2025microstructuralandmechanical pages 72-76).

Extended Sc solubility in Al under LPBF conditions reaches ~3 wt% (vs. equilibrium ~0.35–0.4 wt%) (cerri2024mainheattreatments pages 2-5). This means the Sc solubility cliff is effectively pushed to much higher concentrations under LPBF rapid solidification, but the equilibrium peritectic at ~0.12 wt% Sc (591°C) remains critical for primary Al₃Sc grain-refiner formation (prach2021influenceofzr pages 42-47).

---

### 5. Peritectic Thresholds and Solubility-Limit Crossings (Compositional "Cliffs")

These are the sharpest property transitions in the FLAIME composition space:

| Element | Peritectic/Eutectic T (°C) | Equilibrium solid solubility | Key transition |
|---------|---------------------------|------------------------------|----------------|
| **Zr** | 660.8 (peritectic) | 0.28 wt% (0.083 at.%) | Below: no primary Al₃Zr nucleants; Above: grain refinement onset |
| **Sc** | 591 (peritectic) | 0.12 wt% at peritectic; drops to ~0 at RT | Below: no primary Al₃Sc; Above: potent grain refinement |
| **Er** | ~655 (peritectic) | Very low (~0.05 wt%) | Similar cliff to Sc but with faster diffusion/coarsening |
| **Ce** | 621 (eutectic) | ~10⁻⁴ wt% at eutectic T | Virtually all Ce forms Al₁₁Ce₃; eutectic at ~10.6 wt% Ce |
| **Fe** | 655 (eutectic) | ~0.05 wt% at RT | Above ~0.05 wt%: Al₃Fe/Al₁₃Fe₄ intermetallic formation onset |
| **Si** | 577 (eutectic, 12.6 wt%) | ~1.65 wt% at 577°C | Eutectic crossing: dramatic microstructure change |

(prach2021influenceofzr pages 42-47, adetan2025microstructuralandmechanical pages 24-31)

**Implication for FLAIME:** For Zr and Sc, the grain-refinement cliff occurs over a ~0.05 wt% window. Dispensing accuracy of ±0.01 g on 10 g charges (±0.1 wt%) may be insufficient to reliably hit these targets. TC/CALPHAD simulations need ≤0.02 at.% grid spacing near the peritectic compositions.

---

### 6. Thermal Conductivity Sensitivity

Per 1 wt% solute in solid solution, thermal conductivity reductions are (zhang2023thermalconductivityof pages 7-9):
- **Si:** ~54 W/(m·K) — most detrimental
- **Mg:** ~36 W/(m·K)
- **Cu:** ~17 W/(m·K)
- **Zn:** ~6 W/(m·K) — least detrimental

Electrical resistivity increments per wt% in solid solution (µΩ·cm/wt%) provide a more complete ranking (zhang2023thermalconductivityof pages 5-7, zhang2023thermalconductivityof pages 4-5):

| Element | Δρ_solid-solution | Δρ_precipitated | Max solid solubility (wt%) |
|---------|-------------------|-----------------|---------------------------|
| Cr | 4.00 | — | ~0.77 |
| V | 3.58 | 0.28 | ~0.5 |
| Mn | 2.94 | 0.34 | ~1.82 |
| Ti | 2.88 | 0.12 | ~1.0 |
| Fe | 2.56 | 0.058 | ~0.05 |
| Zr | 1.74 | — | ~0.28 |
| Si | 1.02 | 0.088 | ~1.65 |
| Ni | 0.81 | 0.061 | ~0.04 |
| Mg | 0.54 | 0.22 | ~14.9 |
| Cu | 0.344 | 0.030 | ~5.67 |
| Zn | 0.094 | 0.023 | ~82.8 |

The in-solution effect is 2–44× larger than the precipitated-state effect. Trace levels (0.1 wt%) of Mn, Cr, or V reduce conductivity by ~12–19 W/(m·K) in Al-9Si alloys (zhang2023thermalconductivityof pages 7-9). Conversion to thermal conductivity uses the Wiedemann–Franz relation: k ≈ L₀T/ρ + c, where L₀ ≈ 2.1×10⁻⁸ W·Ω·K⁻² (zhang2023thermalconductivityof pages 4-5).

**Implication for FLAIME:** For the Al-Mn-Cr-Zr system, even 0.1 wt% changes in Mn or Cr significantly affect thermal conductivity. Heat treatment (precipitation) can recover ~50% of the conductivity loss.

---

### 7. Corrosion / Pitting Potential Sensitivity

The galvanic relationship between the Al matrix and intermetallic particles drives localized corrosion. Key quantitative data (in 0.1 M NaCl vs. SCE) (li2017asummaryof pages 3-4, li2017asummaryof pages 11-13, li2017asummaryof pages 8-9):

| Phase/Composition | E_corr (V_SCE) | E_pit (V_SCE) | Role |
|-------------------|----------------|---------------|------|
| Pure Al | −0.82 to −1.22 | −0.55 to −0.67 | Matrix |
| Al-1Cu (solid soln) | −0.69 | — | Ennobled matrix |
| Al-4Cu (solid soln) | −0.90 | — | +300 mV shift vs pure Al |
| Al₂Cu (θ) | −0.565 | — | Cathodic (noble) |
| Al₇Cu₂Fe | −0.55 | −0.40 | Strongly cathodic |
| Al₂CuMg (S-phase) | −0.93 | — | Initially anodic, then Cu-enriched |
| MgZn₂ (η) | −1.0 | — | Anodic |
| Mg₂Si (β) | — | < matrix E_corr | Anodic |
| Al₂₀Cu₂Mn₃ | −0.79 | −0.42 | Cathodic |

Adding 4 wt% Cu shifts the matrix E_corr from −1.2 to −0.9 V_SCE, and 5.2 wt% Cu increases pitting potential by ~200 mV (li2017asummaryof pages 8-9). The onset of Cu-containing intermetallics (Al₂Cu, Al₇Cu₂Fe) fundamentally changes the galvanic landscape. Fe above its solubility limit (~0.05 wt%) forms β-Al₅FeSi (strongly cathodic) or α-Al(FeMn)Si phases; Mn additions ≥0.3 wt% promote the less-harmful α-phase morphology (ikeuba2024areviewof pages 13-15).

**Implication for FLAIME:** Cu and Fe have the sharpest corrosion sensitivity. A 0.1 wt% change in Fe near its solubility limit (~0.05 wt%) can trigger intermetallic formation and dramatically change corrosion behavior. For Cu, the sensitivity is ~75 mV per wt% in the 0–4 wt% range.

---

### 8. Printability Window Sensitivity

Printability in P-v space is primarily governed by CSI and freezing range:

- **Al-Si (near eutectic, 10–12 wt% Si):** Widest printability window; crack-free across broad P-v range (hyer2021compositiondependentsolidificationcracking pages 1-2).
- **Al-Si (1–2 wt% Si):** Very narrow or no crack-free window (hyer2021compositiondependentsolidificationcracking pages 4-5).
- **7xxx (unmodified):** Extremely narrow; AA7075 CSI = 6504 °C (li2021investigationofsolidification pages 1-2). Adding 3.74 wt% Si reduces CSI to 3960 °C and opens a crack-free window.
- **Al-Mn-Ce (Al₉₂Mn₆Ce₂):** Processed crack-free without baseplate heating; compressive strength >1200 MPa (gabrysiak2021developmentandcharacterization pages 1-2).
- **Scalmalloy® (Al-Mg-Sc-Zr):** Bimodal microstructure with Al₃(Sc,Zr) grain refiners provides a robust process window when Sc > peritectic threshold (cerri2024mainheattreatments pages 2-5).
- **Al-Ni-Ti-Zr:** Reported to exhibit excellent printability with a wide P-v window due to heterogeneous grain structure and low freezing range.

The 4 wt% Si addition to 7075 reduces the melting point by ~17 °C, reduces latent heat release, and promotes eutectic feeding — all widening the printability window (dixit2022laseradditivemanufacturing pages 16-18).

---

### 9. Al-Mn-Cr-Zr (FLAIME Initial Focus) and Al-Ce Systems

**Al-Mn-Cr-Zr:** An LPBF-processed Al-Mn-Ni-Cu-Zr system (related composition space) achieved YS ~320 MPa stress-relieved (300°C/4h) with ~200 MPa attributed to Mn retained in solid solution (>1.5 at.%), rising to YS ~410 MPa after aging at 400°C/1h from additional L1₂-Al₃Zr and Mn-rich precipitate formation (hesselmann2022effectofprecipitationforming pages 11-14). The Scancromal® system (Al-Cr-Sc-Zr) achieves hardness comparable to AlSi10Mg with build rates of ~47 cm³/h.

**Al-Ce:** Ce has virtually zero solid solubility in Al (~10⁻⁴ wt%), so all Ce forms Al₁₁Ce₃ eutectic (eutectic at ~10.6 wt% Ce, 621°C). Near-eutectic Al-Ce-Mn alloys with ~7 wt% Mn achieved YS ~268 MPa with excellent thermal stability at 300–400°C (hesselmann2022effectofprecipitationforming pages 1-3, adetan2025microstructuralandmechanical pages 24-31).

---

### 10. Summary of Compositional Cliffs and Resolution Requirements

**Deliverable 3: Practical Implications**

**(a) Dispensing accuracy (AutoTrickler, ±0.01 g on ~10 g):**
- ±0.1 wt% resolution is adequate for: Mg, Si, Cu, Zn axes (smooth property gradients in most ranges).
- ±0.1 wt% resolution is marginal for: Zr (peritectic at 0.28 wt%), Sc (peritectic at 0.12 wt%), Fe (solubility limit ~0.05 wt%). For these elements, dispensing accuracy of ±0.01 wt% (i.e., ±0.001 g on 10 g) would better resolve the critical transitions.
- For Er (solubility ~0.05 wt%), similar concerns as Fe/Sc apply.

**(b) Stoichiometry shifts during induction melting:**
- Mg volatilization is the primary concern (vapor pressure ~10× higher than Al at melt temperatures). LPBF Scalmalloy studies report Mg loss during processing. Dispensing ~5–10% excess Mg may be needed.
- Zn is also volatile (relevant for 7xxx). Li is extremely volatile and oxidation-prone.
- Fe, Ni, Cu, Mn, Cr, Zr have negligible volatilization losses.
- Differential oxidation: Al₂O₃ formation is thermodynamically favorable but kinetically limited in inert atmosphere. Mg and Li form tenacious oxides preferentially.

**(c) Thermo-Calc / TCAL10 simulation resolution:**

| Composition regime | Recommended at.% grid spacing | Rationale |
|---|---|---|
| Near Zr/Sc/Er peritectic | ≤0.02 at.% | Grain refinement onset cliff |
| Near Fe/Ni intermetallic onset | ≤0.02 at.% | Phase fraction jumps |
| Near Al-Si eutectic (10–13 wt%) | 0.5 wt% (~0.5 at.%) | CSI is flat |
| Al-Si hypoeutectic (0–4 wt%) | ≤0.25 wt% | CSI changes rapidly |
| Al-Mg (2–6 wt%) | 0.5 wt% | Smooth CSI variation |
| Al-Cu (0–5 wt%) | 0.25 wt% | CSI peak region |
| 7xxx multicomponent | 0.5 wt% per element | Moderate sensitivity |
| Al-Ce near eutectic | 0.5 wt% | Low solubility, Ce mostly in intermetallic |

**Deliverable 4: Data Sparsity Flags**

The following property × element pairings rely primarily on DFT/CALPHAD inference rather than direct experimental measurement:
- **Solid solution strengthening of Cr, Fe, Ni, Ti in Al at LPBF cooling rates:** Only DFT predictions and limited rapidly-solidified data exist (michi2022towardshightemperatureapplications pages 19-21).
- **Grain size vs. exact Zr/Sc/Er composition in LPBF:** No published systematic composition-scan study; data exists only for discrete compositions.
- **Printability window size (P-v area) as function of composition:** No quantitative metric exists; assessments are qualitative (cracked vs. crack-free).
- **CTE and density per wt% solute:** Literature does not report systematic measurements; values are primarily from rule-of-mixtures or handbook data.
- **Corrosion sensitivity of Al-Mn-Cr-Zr system:** Virtually no published data for this specific system.
- **Thermal conductivity of LPBF-specific microstructures:** In-solution vs. precipitated partitioning is process-dependent; published data is limited to cast/wrought alloys.
- **Al-Er precipitation kinetics and strengthening coefficients:** Limited to a few studies; no systematic MPa-per-at.% data.

---

### Summary for FLAIME Decision-Making

The BO surrogate needs the finest lengthscale priors along the **Zr, Sc, Er, and Fe** axes (property cliffs within 0.05–0.3 wt% windows), moderate resolution along **Mn, Cr, Cu, Si** (significant property sensitivity at 0.1–1 wt% scale), and the coarsest resolution along **Zn and Mg** (smooth, gradual property changes). The current AutoTrickler dispensing accuracy (±0.1 wt%) is marginally sufficient for most elements but may need tighter control for Sc and Er near their peritectic thresholds. Thermo-Calc grid spacing should be ≤0.02 at.% for peritectic-forming elements and ≤0.25 wt% for major solutes near CSI peaks.