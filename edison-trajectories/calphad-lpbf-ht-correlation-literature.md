# Edison response: calphad-lpbf-ht-correlation-literature-resubmit

- Task ID: `7fef0337-187e-41ae-840b-12579040533c`
- Status: `success`

---

## Survey of Empirical Correlations and Benchmark Recommendations for a 6-Node Synthetic LPBF Al-Alloy DAG

### 1. Empirical R²/Correlation Values

The following table consolidates the literature evidence mapped to the edges of the proposed DAG:

| Proposed DAG edge | Literature proxy / relationship | Source paper | Correlation metric | Reported value | Notes |
|---|---|---|---|---|---|
| y0 CALPHAD descriptor → y1 printability proxy | Scheil/Kou crack-susceptibility vs observed LPBF Al-Si cracking | Hyer et al., *Acta Materialia* 2021 | Qualitative agreement; peak-location comparison | No explicit R² reported; predicted peak susceptibility at ~0.5 wt.% Si vs measured peak crack density at ~1.0 wt.% Si | Useful as a **moderate-fidelity** link, but literature does **not** provide strong numerical R² for Al LPBF printability; indicates possible mismatch even when trend is right (hyer2021effectsofalloy pages 1-2, hyer2021effectsofalloy pages 7-8) |
| y0 CALPHAD descriptor → y1 printability proxy | CALPHAD-derived printability / cracking descriptors predicted from composition | Ni et al. / AlloyGPT 2025 | Forward-prediction R² for CALPHAD-derived properties | R² range **0.86–0.99** overall; CSC noted as among the hardest / lowest-R² targets | This is **model-to-database** accuracy, not direct experimental printability correlation, so it is an upper bound for descriptor predictability rather than descriptor→experiment fidelity (ni2025endtoendpredictionand pages 5-6) |
| y0 CALPHAD descriptor → y1 printability proxy | Hot-cracking criteria vs measured crack density under wrong cracking regime | Wahlmann et al. 2021 | Spearman rank correlation | **Negative correlation** for SI / Kou / CTI under laser remelting | Important lower-bound / breakdown case: hot-cracking metrics can fail when cold cracking dominates, implying effective R² can be near 0 or worse in mismatch regimes (wahlmann2021numericalalloydevelopment pages 14-15) |
| y1 printability proxy → y3 single-track / stability proxy | No directly reported LPBF Al-alloy R² found in surveyed literature | — | — | — | Evidence gap; best justified as a **moderate** synthetic coupling rather than one anchored by a specific published R² |
| y2 composition-aware powder / melt-pool root → y3 single-track / stability proxy | No directly reported LPBF Al-alloy R² found in surveyed literature | — | — | — | Evidence gap; likely moderate-to-high physically, but not numerically benchmarked in the retrieved corpus |
| y3 single-track / stability proxy → y4 porosity / build-quality proxy | General MFBO / materials guidance on informativeness threshold (used as synthetic-benchmark prior, not AM-specific experiment) | Sabanza-Gil et al. 2025 | Informativeness threshold R² | Favorable MFBO when **R² > 0.75**, strongly favorable when **R² > 0.9** | Not an AM experiment, but useful for choosing synthetic edge strengths that are “informative enough” for MFBO algorithms to benefit (sabanzagil2025bestpracticesfor pages 7-9, sabanzagil2025bestpracticesfor pages 5-7) |
| y4 porosity / build-quality proxy → y5 mechanical / final property | Porosity vs ductility in LPBF AlSi10Mg | Laursen et al. 2020 | Linear-regression R² | **0.790** (fracture-surface porosity), **0.794** (bulk porosity) | Strongest experimentally quantified porosity→property link in retrieved Al LPBF literature; ductility is the most porosity-sensitive endpoint (laursen2020relationshipbetweenductility pages 7-10, laursen2020relationshipbetweenductility pages 10-10, laursen2020relationshipbetweenductility pages 6-7) |
| y4 porosity / build-quality proxy → y5 mechanical / final property | Porosity vs UTS in LPBF AlSi10Mg | Laursen et al. 2020 | Linear-regression R² | **0.615** (fracture-surface porosity), **0.693** (bulk porosity) | Moderate-to-strong coupling for strength, weaker than ductility (laursen2020relationshipbetweenductility pages 10-10) |
| y4 porosity / build-quality proxy → y5 mechanical / final property | Porosity vs yield strength in LPBF AlSi10Mg | Laursen et al. 2020 | Linear-regression R² | **0.249** (fracture-surface porosity), **0.306** (bulk porosity) | Weak link for yield strength specifically; important caution against making porosity→all-mechanics too strong if y5 mixes YS heavily (laursen2020relationshipbetweenductility pages 10-10, laursen2020relationshipbetweenductility pages 6-7) |
| y4 porosity / build-quality proxy → y5 mechanical / final property | Porosity vs elastic modulus in LPBF AlSi10Mg | Laursen et al. 2020 | Linear-regression R² | **0.498** (fracture-surface porosity), **0.575** (bulk porosity) | Moderate coupling; again weaker than ductility (laursen2020relationshipbetweenductility pages 10-10) |
| y4 porosity / build-quality proxy → y5 mechanical / final property | Porosity vs ductility via IDS model in LPBF AlSi10Mg | Laursen et al. 2020 | IDS log-log fit R² | **0.732** (surface), **0.765** (bulk) | Confirms robust but imperfect nonlinear porosity→ductility relationship (laursen2020relationshipbetweenductility pages 7-10, laursen2020relationshipbetweenductility pages 10-10) |
| y4 porosity / build-quality proxy → y5 mechanical / final property | Review consensus across LPBF alloys incl. AlSi10Mg | Kan et al. 2022 | Qualitative synthesis | Ductility more sensitive than strength; correlations can weaken at very low porosity | Supports making this edge strong for ductility-dominated objectives, but not unrealistically deterministic (kan2022acriticalreview pages 6-8, kan2022acriticalreview pages 8-11, kan2022acriticalreview pages 11-15) |
| y3/y4 process-structure state → y5 final property via aging / precipitation indicator | JMAK precipitation-kinetics fit quality in Al alloys | Sun 2023 | JMAK fit R² | Mean **0.963**, median **0.983**; constrained-n mean **0.934** | Not LPBF mechanical-property data directly, but a strong precedent that precipitation-state indicators can be highly predictive when the mechanism is matched (sun2023quantitativesensitizationmodeling pages 72-81, sun2023quantitativesensitizationmodeling pages 66-72) |
| y3/y4 process-structure state → y5 final property via aging / precipitation indicator | Precipitation-strengthening model vs measured yield strength in Al-Zn-Mg-Cu | Liu 2024 | Relative prediction error | Strength error **within 3%** | Very strong property-link once precipitation state is known; supports a high-fidelity aging/property edge in synthetic DAGs (liu2024effectofoveraging pages 10-12) |
| y3/y4 process-structure state → y5 final property via aging / precipitation indicator | Review of age-hardening / Kampmann–Wagner / JMAK-type models | Wu et al. 2025 review | Relative prediction error | Peak error reported **within ±2%** in one cited model; otherwise “excellent agreement” | Useful as upper-end justification for a very strong precipitation/aging→mechanical coupling (wu2025aluminumalloyhot pages 18-22) |


*Table: This table summarizes the empirical correlation values and closest literature proxies relevant to each edge of a 6-node synthetic LPBF Al-alloy DAG. It highlights where the evidence is quantitative and where important gaps or breakdown cases remain, which is useful for choosing defensible synthetic coupling strengths.*

#### 1(a) CALPHAD Descriptors → Printability/Cracking Outcomes

The relationship between CALPHAD-derived solidification descriptors (freezing range, Scheil eutectic fraction, Kou's |dT/d(f_S^{1/2})| coefficient, Clyne-Davies CSC) and actual LPBF cracking outcomes for Al-alloys is predominantly **qualitative** in the published literature. Hyer et al. (2021) demonstrated that the Kou criterion correctly predicted the composition-dependent trend of solidification cracking in binary Al-Si alloys processed by LPBF, but found the predicted peak susceptibility occurred at ~0.5 wt% Si while the experimental peak crack density was at ~1.0 wt% Si (hyer2021effectsofalloy pages 7-8). They noted that including solid-state diffusion shifts the predicted peak to higher solute concentrations, indicating sensitivity to assumed diffusion kinetics (hyer2021effectsofalloy pages 1-2). No explicit R² values between CALPHAD cracking indices and measured LPBF crack density were reported in any of the retrieved Al-alloy papers.

For composition-to-property predictions using CALPHAD-derived databases, Ni et al. (2025) reported that AlloyGPT achieves R² values ranging from 0.86 to 0.99 across various physical quantities predicted from Al-alloy compositions, but noted that the crack susceptibility coefficient (CSC) had the **lowest R²** among all predicted properties (ni2025endtoendpredictionand pages 5-6). This represents an upper bound on descriptor predictability from a model-to-database perspective rather than a direct CALPHAD-to-experiment correlation.

#### 1(b) Porosity → Mechanical Properties

Laursen et al. (2020) provide the most comprehensive quantitative data, based on 174 LPBF AlSi10Mg tensile samples across eight build plates. Their Table 4 reports the following R² values from linear regression (laursen2020relationshipbetweenductility pages 10-10):

- **Ductility vs. porosity**: R² = 0.790 (fracture-surface) / 0.794 (bulk Archimedes)
- **UTS vs. porosity**: R² = 0.615 (fracture-surface) / 0.693 (bulk)
- **Yield strength vs. porosity**: R² = 0.249 (fracture-surface) / 0.306 (bulk)
- **Elastic modulus vs. porosity**: R² = 0.498 (fracture-surface) / 0.575 (bulk)
- **IDS model (ductility, log-log)**: R² = 0.732 (fracture-surface) / 0.765 (bulk)

Porosity affects ductility by approximately 300% across the observed range, compared to only ~10% variation in strength (laursen2020relationshipbetweenductility pages 6-7). The review by Kan et al. (2022) confirms that ductility is far more sensitive to porosity than strength across LPBF alloys, and that at very low porosity levels, microstructure (not porosity) becomes the dominant factor controlling mechanical properties (kan2022acriticalreview pages 6-8, kan2022acriticalreview pages 8-11).

#### 1(c) Precipitation/Aging Indicators → Final Mechanical Properties

JMAK kinetics models for precipitation-related phenomena in Al-alloys achieve high fit quality: Sun (2023) reported a mean R² = 0.963 (median 0.983) for JMAK fits to isothermal sensitization kinetics in 5xxx Al-Mg alloys, and even constraining the JMAK exponent to n = 1 still yielded mean R² = 0.934 (sun2023quantitativesensitizationmodeling pages 72-81, sun2023quantitativesensitizationmodeling pages 66-72). For combined precipitation-strengthening models, Liu (2024) reported yield strength prediction errors within 3% for an Al-Zn-Mg-Cu alloy across multiple over-aging conditions (liu2024effectofoveraging pages 10-12). Wu et al. (2025) in a comprehensive review cited one model achieving peak errors within ±2% between simulated and experimental results (wu2025aluminumalloyhot pages 18-22). These values imply an effective R² ≥ 0.95 for the precipitation/aging → mechanical property link when the mechanism is correctly captured.

---

### 2. Recommended Edge-Coupling Strengths and Assessment of Your Current Settings

Your current coupling vector [0, 0, 0, 0.5, 0.8, 0.7] and resulting R²(y_k vs y5) of {0.67, 0.75, 0.67, 0.98, 0.995} can be assessed against the literature as follows:

**y0 (CALPHAD) → y5: R² = 0.67.** This is **reasonable but perhaps slightly optimistic** for a direct CALPHAD-to-final-property chain. The literature shows only qualitative agreement between Scheil-derived cracking indices and LPBF outcomes, with documented cases of mismatch (peak location shift by ~2× in Si content) (hyer2021effectsofalloy pages 7-8). An R² of 0.4–0.7 would be defensible depending on the alloy system.

**y1 (AM-Module printability) → y5: R² = 0.75.** This is **reasonable**. No direct R² is reported in the literature for this exact edge, but printability proxies that incorporate process-relevant physics (melt-pool stability, single-track formation) would be expected to have moderate-to-good predictive power for final properties when combined through the DAG.

**y2 (composition-aware powder/melt-pool root) → y5: R² = 0.67.** This is **reasonable**. This mirrors the CALPHAD-to-outcome correlation level, which is appropriate since composition-aware melt-pool models face similar fidelity limitations.

**y3 (melt-pool/single-track stability) → y5: R² = 0.98.** This is **high but defensible** for a direct melt-pool-to-property link, particularly if the melt-pool proxy captures the dominant defect-formation physics (lack-of-fusion, keyholing). Process-structure-property models in the literature achieve very high accuracy when the correct process window is identified.

**y4 (porosity/build-quality) → y5: R² = 0.995.** This is **too high** relative to literature evidence. Laursen et al. (2020) report R² ≈ 0.79 for porosity-ductility (the strongest porosity-property correlation) and only R² ≈ 0.25–0.69 for strength metrics (laursen2020relationshipbetweenductility pages 10-10). We recommend reducing this to **R² ≈ 0.80–0.90** unless y5 is explicitly modeled as a ductility-dominated metric. If y5 represents a composite mechanical property (e.g., mixing yield, UTS, and elongation), R² ≈ 0.80 is more realistic.

**Recommended adjustments to coupling vector:** Consider modifying from [0, 0, 0, 0.5, 0.8, 0.7] to approximately [0, 0, 0, 0.5, **0.55–0.65**, 0.7] to bring the y4→y5 edge closer to published empirical ranges, and add noise to the y0→y1 edge to reflect the documented CALPHAD-to-experiment uncertainty. Additive noise levels should be set such that early nodes (y0, y1, y2) have σ_noise/σ_signal ratios of 0.3–0.5 (reflecting the qualitative nature of CALPHAD correlations), while later nodes (y3, y4) can have lower noise ratios of 0.1–0.2.

---

### 3. Prior Synthetic AM/Al-Alloy Multi-Fidelity BO Benchmarks

Our survey found **no published synthetic benchmark specifically designed to mimic an LPBF Al-alloy discovery pipeline as a multi-fidelity DAG**. The closest comparators are:

1. **Sabanza-Gil et al. (2025), *Nature Computational Science***: Proposed best practices for MFBO using synthetic functions (Branin-2D, Park-4D) with tunable α-parameter controlling LF informativeness. They use R² between LF and HF as the informativeness metric, with favorable MFBO thresholds at R² > 0.75 and cost ratio ρ < 0.2, and strongly favorable at R² > 0.9, ρ ≈ 0.1 (sabanzagil2025bestpracticesfor pages 7-9, sabanzagil2025bestpracticesfor pages 5-7). Real benchmarks include COFs (ρ = 0.065, R² = 0.98), FreeSolv (ρ = 0.1, R² = 0.88), and Alexandria polarizability (ρ = 0.167, R² = 0.99) (sabanzagil2025bestpracticesfor pages 5-7). Code available via BoTorch.

2. **Tran et al. (2020), *J. Chem. Phys.***: Multi-fidelity GP framework fusing DFT (high-fidelity) and ML interatomic potentials (low-fidelity) for ternary Al-Nb-Ti random alloys. Not a synthetic DAG benchmark per se but demonstrates MFBO for alloy bulk modulus optimization.

3. **Khatamsaz et al. (2023), *npj Computational Materials***: Constrained multi-objective BO for Mo-Nb-Ti-V-W MPEA gas turbine alloys using CALPHAD-derived properties (solidification range, solidus temperature, thermal conductivity) as constraints. Provides a CALPHAD-in-the-loop materials BO framework but not a synthetic DAG benchmark.

4. **Chiappetta et al. (2024)**: Multi-fidelity UQ for LPBF based on the NIST AMBench2018-01 Inconel 625 benchmark, using multi-index stochastic collocation. This is a real AM benchmark, not synthetic, and not Al-alloy-specific.

5. **AlloyGPT (Ni et al. 2025)**: GitHub repository at https://github.com/Taheri-Mousavi-Laboratory/AlloyGPT provides code for forward prediction and inverse design of Al-alloys using a CALPHAD-derived database (ni2025alloygptendtoendprediction pages 9-12). The training dataset was generated by Thermo-Calc and covers Al-Ni-Er-Zr-Y-Yb compositions with printability descriptors (CSC, HCS, freezing range).

6. **Barrionuevo et al. (2025), *Scientific Data***: Published a large-scale LPBF dataset (1,579 samples of commercial alloys) for relative density prediction, available as a benchmark dataset for ML models.

Your proposed 6-node DAG benchmark would be, to our knowledge, the **first synthetic DAG benchmark explicitly designed to represent an LPBF Al-alloy discovery pipeline** for multi-fidelity BO algorithm comparison.

---

### 4. Correlation Breakdowns (Lower Bounds on Edge Fidelity)

Several important breakdown cases were identified:

**Wahlmann et al. (2021)** provide the most striking example: Spearman rank correlations between four CALPHAD-based cracking criteria (solidification interval, Kou criterion, critical temperature interval, shrinkage coefficient) and measured crack densities showed **negative correlations** for the first three criteria in laser-remelted Ni-base superalloys (wahlmann2021numericalalloydevelopment pages 11-14, wahlmann2021numericalalloydevelopment pages 14-15). The alloys computationally optimized for minimal hot-cracking susceptibility exhibited the **highest** crack densities because the dominant mechanism under laser remelting conditions was cold cracking, not hot cracking. This demonstrates that when the assumed failure mechanism does not match reality, CALPHAD-to-outcome R² can be effectively zero or negative.

**Hyer et al. (2021)** showed that the standard Scheil model predicted peak cracking susceptibility at ~0.5 wt% Si while measured peak crack density occurred at ~1.0 wt% Si in binary Al-Si LPBF (hyer2021effectsofalloy pages 7-8). Including solid-state diffusion corrections shifted predictions closer to experiment but dramatically reduced predicted susceptibility magnitudes. This represents a systematic bias rather than random scatter.

**Uba et al. (2025)** highlighted fundamental limitations of the classic Scheil approach for LPBF: assumptions of no solid diffusion, no solute trapping at high growth rates, and no melt-pool convection effects all break down under LPBF conditions (cooling rates ~10⁵–10⁷ K/s) (uba2025enhancingtheprintability pages 4-5). These limitations suggest that the cheapest CALPHAD descriptor (y0) should have the weakest coupling to downstream experimental nodes.

**For the porosity → property edge**, Kan et al. (2022) note that at very low porosity levels (<0.5%), microstructure dominates and the porosity-property correlation essentially disappears, meaning the effective R² drops substantially in the high-quality regime (kan2022acriticalreview pages 8-11, kan2022acriticalreview pages 11-15).

**Defensible lower bounds**: Based on these findings, the lowest defensible R² for the CALPHAD-to-printability edge (y0 → y1) is approximately **0.1–0.3** (accounting for cases where the correct trend is captured but with significant offset or mechanism mismatch). For porosity → mechanical property, the lower bound is approximately **R² ≈ 0.25** (yield strength, which showed the weakest porosity dependence in Laursen et al. 2020) (laursen2020relationshipbetweenductility pages 10-10). These lower bounds can be used to define a "pessimistic" DAG variant for robustness testing of your BO algorithms.

---

### Summary Recommendation

Your proposed coupling values are broadly reasonable but would benefit from two adjustments: (1) reducing the y4→y5 coupling from R² = 0.995 to ~0.80–0.90 to match the Laursen et al. (2020) empirical evidence, and (2) considering a "stress test" variant with the y0→y1 edge degraded to R² ≈ 0.2–0.4 to capture the documented CALPHAD breakdown regime. The Sabanza-Gil et al. (2025) MFBO guidelines suggest that edges with R² < 0.75 and cost ratios > 0.2 will offer limited benefit to multi-fidelity algorithms, which is a useful design principle for making the benchmark discriminative between TSFN, pKGFN, and baselines.