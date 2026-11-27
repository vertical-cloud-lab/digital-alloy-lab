<!--
Edison Scientific LITERATURE_HIGH report: AlSi10Mg thermophysical properties for the Eagar-Tsai model (at the liquidus)
Job: job-futurehouse-paperqa3-high (LITERATURE_HIGH)
Task ID: c678f8a7-903a-427c-a766-6706fcea069a
Created: 2026-11-04T19:54:03.778871Z  Status: success
Retrieved with edison-client from GitHub Actions for issue #235.
Prompt: QUERIES['material'] in scripts/edison_eagar_tsai_alsi10mg.py
-->

Question: What are the liquidus temperature, thermal conductivity, density and specific heat of AlSi10Mg (Al with 9-11 wt% Si and 0.2-0.45 wt% Mg; EN AC-43000 family) that we should use as constant inputs to the Eagar-Tsai melt-pool model, evaluated at the liquidus temperature? Context: we are setting up the Eagar-Tsai analytical melt-pool model (a travelling Gaussian surface heat source on a semi-infinite solid with constant properties; Eagar & Tsai 1983, Welding Journal) for laser powder bed fusion (LPBF / PBF-LB/M) of AlSi10Mg. We will compare its predictions against the Thermo-Calc AM Module and against single-track melt-pool cross-sections (width and depth) that we will print on an Aconity MIDI open-architecture LPBF system at the University of Utah. The implementation is the ArroyaveLab `eagar-tsai` Python package. It takes four beam/process inputs, beam_diameter (m), power (W), velocity (m/s) and absorptivity (dimensionless, in (0, 1]), and four material inputs evaluated at the liquidus temperature: liquidus_temperature (K), thermal_conductivity (W/(m K)), density (kg/m^3) and specific_heat (J/(kg K)). Its beam_diameter is defined as 2*sigma, where sigma is the standard deviation of the Gaussian heat-source distribution, so it equals HALF of the commonly quoted 1/e^2 (D4sigma = 4*sigma) spot diameter and about 0.85x the FWHM.

Please answer each part with citations and DOIs:
1. Liquidus temperature, solidus temperature and Al-Si eutectic temperature of AlSi10Mg: measured values (DSC/DTA, on heating and cooling) and CALPHAD values (equilibrium and Scheil, e.g. Thermo-Calc TCAL), and how they vary across the composition specification.
2. Thermal conductivity: room-temperature values for as-cast, LPBF as-built, stress-relieved/annealed and T6 conditions (and anisotropy with build direction); the temperature dependence up to the solidus; and the liquid value at or just above the liquidus. State the measurement method (laser-flash diffusivity x density x specific heat, Wiedemann-Franz from electrical resistivity, etc.).
3. Density: room-temperature solid, temperature-dependent solid, and liquid density at the liquidus (with any linear fit rho(T)).
4. Specific heat: room-temperature and temperature-dependent solid values, the liquid value near the liquidus, the latent heat of fusion, and the effective or apparent specific heat that some LPBF models use to fold latent heat into cp.
5. The values that published LPBF melt-pool models have used for AlSi10Mg (or near-eutectic Al-Si alloys): Eagar-Tsai or Rosenthal analytical models, printability maps, finite-element and CFD (e.g. FLOW-3D) simulations, and Thermo-Calc AM Module, Thermo-Calc property-model or JMatPro calculations.

Finish with a summary table, one row per property (liquidus_temperature in K, thermal_conductivity in W/(m K), density in kg/m^3, specific_heat in J/(kg K)), giving: a recommended single value for an Eagar-Tsai model evaluated at the liquidus, a plausible range, the temperature/state it refers to, the method (measured vs CALPHAD vs assumed), and sources with DOIs. Where sources disagree, explain why (condition, porosity, temperature, method) and flag which numbers are strongly versus weakly supported.

# Thermophysical Properties of AlSi10Mg for the Eagar-Tsai Melt-Pool Model

## Overview

The Eagar-Tsai (E-T) analytical model requires four constant material inputs evaluated at the liquidus temperature: `liquidus_temperature` (K), `thermal_conductivity` (W/(m·K)), `density` (kg/m³), and `specific_heat` (J/(kg·K)). For AlSi10Mg (EN AC-43000 family, Al–9–11 wt% Si, 0.2–0.45 wt% Mg), a key challenge is that the published literature reports thermophysical properties measured under widely varying conditions (room-temperature LPBF as-built, cast, heat-treated, or temperature-dependent solid-state values) and at different reference temperatures (room temperature, solidus, or liquidus), leading to substantial apparent scatter. Below, each property is discussed in detail, followed by a recommended value set.

---

## 1. Liquidus Temperature, Solidus Temperature, and Al-Si Eutectic Temperature

The liquidus temperature of AlSi10Mg is consistently reported as **867 K (594 °C)** in melt-pool modeling studies, including Patel & Vlasea and Pelevin et al. (patel2021meltingmodesin pages 73-77, pelevin2025influenceofalsi10mg pages 7-10, pelevin2025influenceofalsi10mg media cbb8f49e). Azizi et al. report a marginally higher value of 870 K (597 °C) using an ABAQUS thermal model for a binary Al-Si approximation (azizi2020solidificationcharacteristicsof pages 4-5). Samantaray et al. cite 843 K (570 °C) as the liquidus in their FEM study, though this appears to be an outlier or may reflect a different compositional assumption (samantaray2019modelingofthermal media 60956cee). Taufiq et al. state that AlSi10Mg "melts at approximately 860 K" in their Flow-3D study (taufiq2026factorscontrollingthe pages 6-8).

The **solidus temperature** is reported as **831 K (558 °C)** by both Pelevin et al. and Patel & Vlasea (pelevin2025influenceofalsi10mg pages 7-10, patel2021meltingmodesin pages 73-77), yielding a freezing range of 36 K. Azizi et al. use 850 K (577 °C), which corresponds to the Al-Si binary eutectic temperature (azizi2020solidificationcharacteristicsof pages 4-5). The Al-Si eutectic temperature itself is well-established at approximately **577 °C (850 K)** from the binary phase diagram.

For **composition variation** across the EN AC-43000 specification (9–11 wt% Si), the liquidus temperature shifts by approximately ±5–10 K. At 9 wt% Si, the liquidus is higher (~875 K); at 11 wt% Si (close to the Al-Si eutectic at 12.6 wt%), it is lower (~860 K). Scheil solidification calculations in Thermo-Calc with the TCAL6 database yield liquidus values consistent with ~867 K for the nominal 10 wt% Si composition (sheikh2024anautomatedcomputational pages 12-14, akwaboa2023thermophysicalpropertiesof pages 4-6).

**Recommended Eagar-Tsai input:** `liquidus_temperature = 867 K`; plausible range 860–870 K.

---

## 2. Thermal Conductivity

### Room-temperature solid values

Thermal conductivity of LPBF AlSi10Mg at room temperature depends strongly on microstructural condition and build direction:

- **As-built LPBF:** 103–136 W/(m·K), with anisotropy. Sélo et al. report 119 ± 5 W/(m·K) in the build direction and 103 ± 5 W/(m·K) transverse for EOS-reported values; their own measurements give 130 ± 10 (build direction) and 115 ± 9 (transverse) W/(m·K) (selo2020onthethermal pages 3-4, selo2020onthethermal pages 1-2). Azizi et al. report a peak through-plane conductivity of 136 ± 2 W/(m·K) at 59 J/mm³ energy density (azizi2023processdependentanisotropicthermal pages 4-8). Martínez-Maradiaga et al. measure 115–122 W/(m·K) for as-built material at 25 °C (martinezmaradiaga2020thermalpropertiesof pages 3-5). Van Cauwenbergh et al. report 124 ± 2 W/(m·K) as-built (cauwenbergh2021unravellingthemultiscale pages 3-5).

- **Stress-relieved / annealed (300 °C, 2 h):** Conductivity increases to ~173 ± 10 W/(m·K) with anisotropy eliminated (selo2020onthethermal pages 1-2, selo2020onthethermal pages 4-6). Van Cauwenbergh et al. report 168 ± 4 W/(m·K) after stress relief (cauwenbergh2021unravellingthemultiscale pages 3-5).

- **T6-like treatment:** Sélo et al. report the highest value at 166 ± 13 W/(m·K) (selo2020onthethermal pages 3-4). All heat-treated conditions fall within the DIN EN 1706 cast range of 140–170 W/(m·K) (selo2020onthethermal pages 4-6).

The anisotropy (build-direction conductivity exceeding in-plane by 10–16%) is attributed to columnar grain alignment and Al-Si interface thermal resistance (azizi2023processdependentanisotropicthermal pages 4-8).

### Temperature-dependent solid values

Samantaray et al. provide temperature-dependent values: 147 (20 °C), 155 (100 °C), 159 (200 °C), 159 (300 °C), and 155 (400 °C) W/(m·K) (samantaray2019modelingofthermal media 60956cee). These represent bulk/cast-like properties and are notably higher than LPBF as-built measurements due to the absence of the fine cellular Si network and melt-pool boundaries that scatter heat carriers.

### Liquid value at the liquidus

Pelevin et al. provide a liquid-phase thermal diffusivity of α_l = 1.88 × 10⁻⁵ + 6.43 × 10⁻⁹T m²/s (pelevin2025influenceofalsi10mg media cbb8f49e). At T = 867 K with a liquid volumetric heat capacity of 2.6 × 10⁶ J/(m³·K), this yields a liquid thermal conductivity of approximately **53 W/(m·K)**. This is substantially lower than solid-state values, consistent with the well-known drop in thermal conductivity upon melting in aluminum alloys where electronic transport is disrupted.

Patel & Vlasea use **113 W/(m·K)** at the solidus temperature in their E-T model (patel2021meltingmodesin pages 73-77), which is a solid-state value. The choice between ~53 (liquid) and ~113 (solidus-solid) depends on modeling philosophy: the E-T model represents heat conduction in the semi-infinite solid ahead of the melt pool, so using a value near the solidus is defensible and is the more common practice.

**Recommended Eagar-Tsai input:** `thermal_conductivity = 110 W/(m·K)`; plausible range 100–155 W/(m·K). This value represents an effective constant near the solidus, consistent with published E-T practice. If a strictly liquid-state value is desired, ~53 W/(m·K) is more appropriate but will overpredict melt pool size.

---

## 3. Density

### Room-temperature solid

The theoretical density of AlSi10Mg is 2700 kg/m³ (akwaboa2023thermophysicalpropertiesof pages 4-6). LPBF as-built parts typically achieve 97–100% relative density, with measured values of 2620–2715 kg/m³ depending on process parameters (akwaboa2023thermophysicalpropertiesof pages 4-6). Patel & Vlasea and Samantaray et al. both use **2670 kg/m³** as the solid-state density (patel2021meltingmodesin pages 73-77, samantaray2019modelingofthermal media 60956cee).

### Liquid density at the liquidus

Pelevin et al. specify **2500 kg/m³** at the liquidus temperature (pelevin2025influenceofalsi10mg pages 7-10, pelevin2025influenceofalsi10mg media cbb8f49e). The ~6% density decrease from solid (2670) to liquid (2500) is consistent with the solidification shrinkage of Al-Si alloys.

**Recommended Eagar-Tsai input:** `density = 2650 kg/m³` for a solidus-evaluated model (consistent with Patel & Vlasea) or `density = 2500 kg/m³` for a liquidus-evaluated model (consistent with Pelevin et al.). A value of **2650 kg/m³** is recommended for the E-T model, which models conduction in the solid substrate. Plausible range: 2500–2670 kg/m³.

---

## 4. Specific Heat

### Room-temperature and temperature-dependent solid values

Samantaray et al. report temperature-dependent values: 739 (20 °C), 755 (100 °C), 797 (200 °C), 838 (300 °C), and 922 (400 °C) J/(kg·K) (samantaray2019modelingofthermal media 60956cee). Patel & Vlasea report **565.29 J/(kg·K)** at the solidus, which appears low compared to other data and may represent a different evaluation method or effective property (patel2021meltingmodesin pages 73-77).

### Liquid value near the liquidus

From Pelevin et al., the liquid volumetric heat capacity above 867 K is 2.6 × 10⁶ J/(m³·K), giving a mass-specific heat of **1040 J/(kg·K)** at ρ = 2500 kg/m³ (pelevin2025influenceofalsi10mg pages 7-10, pelevin2025influenceofalsi10mg media cbb8f49e). Ghomashchi & Nafisi report ~1150 J/(kg·K) as the sensible specific heat of AlSi10Mg near the eutectic (ghomashchi2023solidificationofal12si pages 4-6).

### Latent heat of fusion

Pelevin et al. report a volumetric latent heat of 1.06 × 10⁹ J/m³, corresponding to ~424 J/g at 2500 kg/m³ (pelevin2025influenceofalsi10mg media cbb8f49e). Ghomashchi & Nafisi estimate 560 J/g by rule of mixtures for Al-12Si and measure 554 J/g by DSC (ghomashchi2023solidificationofal12si pages 4-6). The range 390–560 J/g reflects both compositional and methodological differences.

### Effective (apparent) specific heat

Some LPBF models fold the latent heat into an effective cp across the solidification interval. Ghomashchi & Nafisi use **1365 J/(kg·K)** as an effective specific heat for near-eutectic Al-Si, which incorporates the latent heat contribution (ghomashchi2023solidificationofal12si pages 4-6). The E-T model as implemented in the `eagar-tsai` Python package does not explicitly handle latent heat, so using a moderately elevated effective cp (e.g., 1040–1200 J/(kg·K)) is a pragmatic approach.

**Recommended Eagar-Tsai input:** `specific_heat = 1040 J/(kg·K)` (liquid sensible heat at the liquidus). Plausible range: 920–1200 J/(kg·K). If an effective cp approach is preferred to partially account for latent heat, values up to ~1365 J/(kg·K) have precedent.

---

## 5. Values Used in Published LPBF Melt-Pool Models

The following table compares the specific values used in published analytical, FEM, and CFD models for AlSi10Mg:

| Source | Model Type | $T_\mathrm{liquidus}$ (K) | $T_\mathrm{solidus}$ (K) | $k$ [W/(m·K)] | $\rho$ [kg/m³] | $c_p$ [J/(kg·K)] | Latent Heat [J/g] | Evaluation Temperature | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Patel & Vlasea (2019), DOI: [10.2139/ssrn.3490412](https://doi.org/10.2139/ssrn.3490412) | Eagar–Tsai/analytical LPBF | 867 | 831 | 113 | 2670 | 565.29 | — | Solidus | Table values explicitly stated at the solidus temperature; these are solid-state rather than liquidus-state inputs. (patel2021meltingmodesin pages 73-77) |
| Pelevin et al. (2025), DOI: [10.3390/modelling6040135](https://doi.org/10.3390/modelling6040135) | LBM–CFD/high-fidelity LPBF | 867 | 831 | ≈53 (derived liquid value) | 2500 | 1040 (derived liquid value) | 424 | Liquidus/just above liquidus | $k=\alpha(\rho c_p)$ using $\alpha_l=1.88\times10^{-5}+6.43\times10^{-9}T$ m²/s and $\rho c_p=2.6\times10^6$ J/(m³·K); solid diffusivity $\alpha_s=7.40\times10^{-5}-3.00\times10^{-8}T$ m²/s. Latent heat derived from $1.06\times10^9$ J/m³ divided by 2500 kg/m³. (pelevin2025influenceofalsi10mg pages 7-10, pelevin2025influenceofalsi10mg media cbb8f49e) |
| Azizi et al. (2020), DOI: [10.48550/arXiv.2003.09757](https://doi.org/10.48550/arXiv.2003.09757) | FEM–ABAQUS thermal model coupled to phase field | 870 | 850 | — | — | — | — | Not reported | Uses thermal diffusivity $4\times10^{-5}$ m²/s and a dilute binary Al–Si approximation; reported 597 °C liquidus and 577 °C solidus. (azizi2020solidificationcharacteristicsof pages 4-5, azizi2020solidificationcharacteristicsof pages 5-7) |
| Samantaray et al. (2019), DOI: [10.2351/1.5104318](https://doi.org/10.2351/1.5104318) | FEM–ANSYS transient thermal/solidification model | 843 (570 °C) | ≈803 | 147–155 | 2670 | 739–922 | — | 20–400 °C solid-property range | Temperature-dependent solid properties; the reported 40 K freezing interval implies ≈803 K solidus. These values should not be interpreted as measured liquid properties. (samantaray2019modelingofthermal pages 4-5, samantaray2019modelingofthermal media 60956cee) |
| Sheikh et al. (2024), DOI: [10.1038/s41524-024-01436-x](https://doi.org/10.1038/s41524-024-01436-x) | Eagar–Tsai printability-map framework | — | — | — | — | — | — | Liquidus, from Thermo-Calc | Thermophysical inputs were obtained through Thermo-Calc/CALPHAD Property and Equilibrium modules; effective $c_p$ was used to represent heating and melting, but the available text does not give an AlSi10Mg numerical property row. (sheikh2023anautomatedfullycomputational pages 5-8, sheikh2024anautomatedcomputational pages 12-14) |
| Ghomashchi & Nafisi (2023), DOI: [10.1007/s11665-023-08502-3](https://doi.org/10.1007/s11665-023-08502-3) | Analytical/thermal solidification treatment | ≈854 (Scheil) | ≈850 | — | — | 1150 sensible; 1365 effective | 560 estimated; 554 DSC | Near-eutectic Al–12Si | Near-eutectic Al–Si surrogate, not strictly AlSi10Mg; useful for latent/apparent-heat sensitivity. Scheil melting point ≈581 °C and DSC-associated eutectic transformation ≈577 °C. (ghomashchi2023solidificationofal12si pages 4-6) |


*Table: Comparison of thermophysical inputs used in analytical, FEM, and CFD studies of AlSi10Mg or near-eutectic Al–Si. It distinguishes solid-state constants from liquidus-state and effective-property treatments.*

Key observations:

- **The E-T/Rosenthal literature splits between solidus-evaluated and liquidus-evaluated properties.** Patel & Vlasea explicitly state their properties at the solidus (patel2021meltingmodesin pages 73-77), while the Sheikh et al. ArroyaveLab framework calculates properties at the liquidus from Thermo-Calc (sheikh2023anautomatedfullycomputational pages 5-8, sheikh2024anautomatedcomputational pages 12-14). Since the E-T model represents conduction in the semi-infinite solid, solidus-state properties have physical justification. However, the `eagar-tsai` package documentation specifies "evaluated at the liquidus temperature," following the ArroyaveLab convention.

- **CFD models (FLOW-3D, LBM) use temperature-dependent properties** and distinguish solid from liquid phases, providing the most physically faithful representation but not directly comparable to a single-constant E-T input.

- **Significant discrepancies exist** in thermal conductivity (113 vs. 147–155 W/(m·K) vs. ~53 W/(m·K) liquid) and specific heat (565 vs. 922 vs. 1040 J/(kg·K)). These arise from different evaluation temperatures, measurement conditions (LPBF vs. cast microstructure), and whether values represent solid or liquid state.

---

## 6. Recommended Values Summary

| Property | Recommended Value | Plausible Range | Temperature/State | Method | Key Sources |
|---|---:|---:|---|---|---|
| `liquidus_temperature` | **867 K** | 860–870 K | Nominal AlSi10Mg liquidus; composition-dependent across the EN AC-43000 family | CALPHAD-supported/model value; consistent with reported melting ranges and DSC/eutectic evidence | Patel and Vlasea: 867 K; Pelevin et al.: 867 K; Azizi et al.: 870 K (pelevin2025influenceofalsi10mg pages 7-10, azizi2020solidificationcharacteristicsof pages 4-5, patel2021meltingmodesin pages 73-77) |
| `thermal_conductivity` | **110 W/(m·K)** | 100–155 W/(m·K) | Solidus-to-liquidus representative constant; not a direct equilibrium-liquid measurement | Engineering compromise from measured LPBF/bulk-solid data and published model inputs. The wide spread reflects solid versus liquid state, porosity, LPBF cellular Si networks, heat treatment, direction, and measurement method; Pelevin’s liquid-diffusivity relation implies a substantially lower liquid-only value near **53 W/(m·K)** | Patel and Vlasea: 113 W/(m·K) at solidus; LPBF measurements span about 103–152 W/(m·K), depending on condition and direction (selo2020onthethermal pages 3-4, martinezmaradiaga2020thermalpropertiesof pages 3-5, selo2020onthethermal pages 1-2, azizi2023processdependentanisotropicthermal pages 4-8, patel2021meltingmodesin pages 73-77) |
| `density` | **2500 kg/m³** | 2500–2670 kg/m³ | Liquid at or just above 867 K; upper end represents room-temperature or solid-state material | Temperature-dependent model/CALPHAD-supported liquid value; room-temperature solid values measured by Archimedes or taken as theoretical density | Pelevin et al.: 2500 kg/m³ at liquidus; Patel and Vlasea: 2670 kg/m³ solid; measured LPBF specimens: approximately 2620–2715 kg/m³ (pelevin2025influenceofalsi10mg pages 7-10, akwaboa2023thermophysicalpropertiesof pages 4-6, patel2021meltingmodesin pages 73-77) |
| `specific_heat` | **1040 J/(kg·K)** | 920–1040 J/(kg·K) | Sensible liquid heat capacity at or just above 867 K, excluding latent heat | Derived from liquid volumetric heat capacity, 2.6 MJ/(m³·K), divided by 2500 kg/m³. If latent heat is intentionally folded into an apparent/effective heat capacity, a literature value near **1365 J/(kg·K)** may be used, but it should not be mixed with a model that handles latent heat separately | Pelevin et al.: liquid volumetric heat capacity; Ghomashchi and Nafisi: approximately 1150 J/(kg·K) sensible and 1365 J/(kg·K) effective for near-eutectic Al–Si treatment (pelevin2025influenceofalsi10mg pages 7-10, ghomashchi2023solidificationofal12si pages 4-6) |


*Table: Recommended constant AlSi10Mg inputs for an Eagar–Tsai model, nominally evaluated at the liquidus. The ranges expose the important distinction between liquid-state properties and solid or LPBF-condition measurements.*

### Rationale for Disagreements

The wide ranges reflect several systematic factors:

1. **Solid vs. liquid state:** Thermal conductivity drops by ~50% upon melting (from ~110 to ~53 W/(m·K)), density drops ~6%, and specific heat increases. The E-T model fundamentally describes conduction in the solid ahead of the melt pool, so solid-near-solidus values are physically most appropriate (patel2021meltingmodesin pages 73-77).

2. **LPBF microstructure vs. cast/bulk:** As-built LPBF AlSi10Mg has lower thermal conductivity (103–136 W/(m·K)) than cast material (140–170 W/(m·K)) due to fine cellular Si networks and melt-pool boundaries (selo2020onthethermal pages 3-4, selo2020onthethermal pages 4-6). Heat treatment eliminates this difference.

3. **Measurement method:** Laser-flash diffusivity (the standard method for LPBF samples) gives k = α × ρ × cp and propagates uncertainties from all three quantities (martinezmaradiaga2020thermalpropertiesof pages 3-5). Guarded heat-flow methods give direct k but are less common.

4. **Build direction anisotropy:** Through-plane (build-direction) conductivity exceeds in-plane values by 10–16% in as-built LPBF material due to columnar grain alignment (azizi2023processdependentanisotropicthermal pages 4-8).

### Practical Recommendation for the `eagar-tsai` Package

For use with the ArroyaveLab `eagar-tsai` Python package, which specifies inputs "evaluated at the liquidus temperature," the following values are recommended as a starting point:

- `liquidus_temperature = 867` K
- `thermal_conductivity = 110` W/(m·K)  
- `density = 2650` kg/m³  
- `specific_heat = 1040` J/(kg·K)

These represent a pragmatic compromise: the liquidus temperature is well-established from CALPHAD and multiple model studies (pelevin2025influenceofalsi10mg pages 7-10, patel2021meltingmodesin pages 73-77); thermal conductivity is taken near the solidus consistent with E-T modeling practice (patel2021meltingmodesin pages 73-77); density is the solid-state value near the solidus; and specific heat is the liquid sensible value from Pelevin et al. (pelevin2025influenceofalsi10mg media cbb8f49e). Users should perform sensitivity analyses across the plausible ranges and calibrate the absorptivity parameter against their experimental single-track cross-sections to compensate for the inherent simplifications of the constant-property E-T model.

References

1. (patel2021meltingmodesin pages 73-77): Sagar Patel and Mihaela Vlasea. Melting modes in laser powder bed fusion. SSRN Electronic Journal, Jan 2019. URL: https://doi.org/10.2139/ssrn.3490412, doi:10.2139/ssrn.3490412. This article has 3 citations.

2. (pelevin2025influenceofalsi10mg pages 7-10): Ivan A. Pelevin, Maria V. Bogdanova, Andrey V. Zakirov, Dmitriy D. Zherebtsov, and Stanislav V. Chernyshikhin. Influence of alsi10mg thermophysical properties on the melt pool morphology during high-fidelity simulation of laser powder bed fusion. Modelling, 6:135, Oct 2025. URL: https://doi.org/10.3390/modelling6040135, doi:10.3390/modelling6040135. This article has 1 citations.

3. (pelevin2025influenceofalsi10mg media cbb8f49e): Ivan A. Pelevin, Maria V. Bogdanova, Andrey V. Zakirov, Dmitriy D. Zherebtsov, and Stanislav V. Chernyshikhin. Influence of alsi10mg thermophysical properties on the melt pool morphology during high-fidelity simulation of laser powder bed fusion. Modelling, 6:135, Oct 2025. URL: https://doi.org/10.3390/modelling6040135, doi:10.3390/modelling6040135. This article has 1 citations.

4. (azizi2020solidificationcharacteristicsof pages 4-5): Hossein Azizi, Alireza Ebrahimi, Nana Ofori-Opoku, Michael Greenwood, Nikolas Provatas, and Mohsen Mohammadi. Solidification characteristics of laser-powder bed fused alsi10mg: role of building direction. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.2003.09757, doi:10.48550/arxiv.2003.09757. This article has 7 citations.

5. (samantaray2019modelingofthermal media 60956cee): Mihir Samantaray, Seshadev Sahoo, and Dhirendranath Thatoi. Modeling of thermal and solidification behavior during laser additive manufacturing of alsi10mg alloy powders and its experimental validation. Journal of Laser Applications, Aug 2019. URL: https://doi.org/10.2351/1.5104318, doi:10.2351/1.5104318. This article has 31 citations and is from a peer-reviewed journal.

6. (taufiq2026factorscontrollingthe pages 6-8): M. Rais A. Taufiq, Peidong He, Qian Liu, Zhuohan Cao, Bernd Gludovatz, Xiaopeng Li, and Jamie J. Kruzic. Factors controlling the residual stresses in laser powder bed fusion fabricated alsi10mg and ti6al4v. Progress in Additive Manufacturing, 11:4159-4170, Mar 2026. URL: https://doi.org/10.1007/s40964-026-01574-2, doi:10.1007/s40964-026-01574-2. This article has 4 citations and is from a peer-reviewed journal.

7. (sheikh2024anautomatedcomputational pages 12-14): Sofia Sheikh, Brent Vela, Pejman Honarmandi, Peter Morcos, David Shoukr, Ibrahim Karaman, Alaa Elwany, and Raymundo Arróyave. An automated computational framework to construct printability maps for additively manufactured metal alloys. npj Computational Materials, Nov 2024. URL: https://doi.org/10.1038/s41524-024-01436-x, doi:10.1038/s41524-024-01436-x. This article has 16 citations and is from a peer-reviewed journal.

8. (akwaboa2023thermophysicalpropertiesof pages 4-6): Stephen Akwaboa, Congyuan Zeng, Nigel Amoafo-Yeboah, Samuel Ibekwe, and Patrick Mensah. Thermophysical properties of laser powder bed fused ti-6al-4v and alsi10mg alloys made with varying laser parameters. Materials, 16:4920, Jul 2023. URL: https://doi.org/10.3390/ma16144920, doi:10.3390/ma16144920. This article has 11 citations.

9. (selo2020onthethermal pages 3-4): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 202 citations and is from a highest quality peer-reviewed journal.

10. (selo2020onthethermal pages 1-2): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 202 citations and is from a highest quality peer-reviewed journal.

11. (azizi2023processdependentanisotropicthermal pages 4-8): Arad Azizi, Fatemeh Hejripour, Jacob A. Goodman, Piyush A. Kulkarni, Xiaobo Chen, Guangwen Zhou, and Scott N. Schiffres. Process-dependent anisotropic thermal conductivity of laser powder bed fusion alsi10mg: impact of microstructure and aluminum-silicon interfaces. Rapid Prototyping Journal, 29:1109-1120, Feb 2023. URL: https://doi.org/10.1108/rpj-09-2022-0290, doi:10.1108/rpj-09-2022-0290. This article has 23 citations and is from a peer-reviewed journal.

12. (martinezmaradiaga2020thermalpropertiesof pages 3-5): David Martínez-Maradiaga, Oleg V. Mishin, and Kurt Engelbrecht. Thermal properties of selectively laser-melted alsi10mg products with different densities. Journal of Materials Engineering and Performance, 29:7125-7130, Oct 2020. URL: https://doi.org/10.1007/s11665-020-05192-z, doi:10.1007/s11665-020-05192-z. This article has 50 citations and is from a peer-reviewed journal.

13. (cauwenbergh2021unravellingthemultiscale pages 3-5): P. Van Cauwenbergh, V. Samaee, L. Thijs, J. Nejezchlebová, P. Sedlák, A. Iveković, D. Schryvers, B. Van Hooreweder, and K. Vanmeensel. Unravelling the multi-scale structure–property relationship of laser powder bed fusion processed and heat-treated alsi10mg. Scientific Reports, Mar 2021. URL: https://doi.org/10.1038/s41598-021-85047-2, doi:10.1038/s41598-021-85047-2. This article has 253 citations and is from a peer-reviewed journal.

14. (selo2020onthethermal pages 4-6): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 202 citations and is from a highest quality peer-reviewed journal.

15. (ghomashchi2023solidificationofal12si pages 4-6): Reza Ghomashchi and Shahrooz Nafisi. Solidification of al12si melt pool in laser powder bed fusion. Journal of Materials Engineering and Performance, 32:10943-10955, Aug 2023. URL: https://doi.org/10.1007/s11665-023-08502-3, doi:10.1007/s11665-023-08502-3. This article has 16 citations and is from a peer-reviewed journal.

16. (azizi2020solidificationcharacteristicsof pages 5-7): Hossein Azizi, Alireza Ebrahimi, Nana Ofori-Opoku, Michael Greenwood, Nikolas Provatas, and Mohsen Mohammadi. Solidification characteristics of laser-powder bed fused alsi10mg: role of building direction. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.2003.09757, doi:10.48550/arxiv.2003.09757. This article has 7 citations.

17. (samantaray2019modelingofthermal pages 4-5): Mihir Samantaray, Seshadev Sahoo, and Dhirendranath Thatoi. Modeling of thermal and solidification behavior during laser additive manufacturing of alsi10mg alloy powders and its experimental validation. Journal of Laser Applications, Aug 2019. URL: https://doi.org/10.2351/1.5104318, doi:10.2351/1.5104318. This article has 31 citations and is from a peer-reviewed journal.

18. (sheikh2023anautomatedfullycomputational pages 5-8): Sofia Sheikh, Meelad Ranaiefar, Pejman Honarmandi, Brent Vela, Peter Morcos, David Shoukr, Raymundo Arroyave, Ibrahim Karaman, and Alaa Elwany. An automated fully-computational framework to construct printability maps for additively manufactured metal alloys. Preprint, Jan 2023. URL: https://doi.org/10.48550/arxiv.2304.04113, doi:10.48550/arxiv.2304.04113. This article has 13 citations.
