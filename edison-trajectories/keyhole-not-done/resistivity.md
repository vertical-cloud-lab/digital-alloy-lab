<!--
Edison Scientific LITERATURE_HIGH report: Liquid electrical resistivity of hypereutectic Al-Si, Ti-6Al-4V, 316L and Al6061
Job: job-futurehouse-paperqa3-high (LITERATURE_HIGH)
Task ID: bb7e1cf7-4ae5-4e5a-af19-b7871336540c
Created: 2026-11-27T03:35:51.956846Z  Status: success
Retrieved with edison-client from GitHub Actions for issue #235.
Prompt: QUERIES['resistivity'] in scripts/edison_keyhole_not_done.py
-->

Question: Context: we have written our own physics-based keyhole and melt-pool model for laser powder bed fusion (1070 nm fibre laser, Gaussian beam 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s) of AlSi10Mg and a hypereutectic Al-24.3Si-0.14Mg (wt%) blend. It uses Drude-Fresnel optics of the liquid from its measured electrical resistivity, a ray tracer for multiple reflections in the keyhole, an energy balance at a keyhole wall at the boiling point, and CALPHAD enthalpies. We are now adding Mg evaporation, a powder layer, a tilted keyhole whose shape comes from a point-by-point wall energy balance, and Marangoni melt flow, and we need sourced inputs. Question: what measured electrical resistivity data exist for (a) liquid Al-Si alloys above 12 wt% Si (hypereutectic, ideally up to 25-30 wt% Si or across the whole Al-Si system, including liquid Si), with the temperature coefficient; (b) liquid Ti-6Al-4V near melting and as high in temperature as measured (pulse heating, e.g. Boivineau et al. 2006); (c) liquid 316 or 316L stainless steel (pulse heating or levitation, e.g. the Graz group); (d) liquid Al6061 or Al-Mg-Si alloys. For each, give the numbers or the fitted equation, the temperature range, whether it is corrected for thermal expansion, the method and uncertainty, and the paper with its DOI and the table or figure number.

## Measured Electrical Resistivity Data for Liquid Metals Relevant to Laser Powder Bed Fusion Modelling

This report consolidates the available measured electrical resistivity data for four alloy systems of interest to Drude–Fresnel optical modelling of LPBF keyholes, covering liquid Al–Si alloys (hypereutectic), liquid Ti–6Al–4V, liquid 316L stainless steel, and liquid Al6061/Al–Mg–Si. For each system, the fitted equation or numerical values, temperature range, thermal expansion correction status, measurement method, uncertainty, and primary references are provided.

The following summary table consolidates all sourced data:

| Alloy system | Liquid-phase fit equation, ρ in µΩ·m and T in K | Temperature range (K) | Thermal-expansion corrected? | Method | Uncertainty | Reference | Location in paper |
|---|---|---:|---|---|---|---|---|
| Pure Al, liquid | **Corrected:** ρ<sub>VE</sub> = 0.097 + 1.681×10<sup>−4</sup>T. **Initial geometry:** ρ<sub>IG</sub> = 0.128 + 1.063×10<sup>−4</sup>T. At 933.47 K after melting: 0.2539 corrected and 0.2272 uncorrected. | 933.47–1491 | Both reported; volume-expansion correction used measured density/diameter. | Submicrosecond ohmic pulse heating; six runs averaged. | Not stated numerically in the extracted table. | Leitner et al. (2017), *Metallurgical and Materials Transactions A*, DOI [10.1007/s11661-017-4053-6](https://doi.org/10.1007/s11661-017-4053-6) (leitner2017thermophysicalpropertiesof pages 5-6, leitner2017thermophysicalpropertiesof pages 6-7, leitner2017thermophysicalpropertiesof pages 4-5) | Table I; Table II; Fig. 2 |
| Al–Si, including hypereutectic Al–14, Al–20 and Al–30 wt% Si; comparison series also includes 5, 8 and 12 wt% Si | No numerical ρ(T) fit tabulated. Conductivity is represented as σ(T)=σ₀+(dσ/dT)(T−T<sub>L</sub>), with σ decreasing as T rises; use ρ=1/σ. Exact σ₀ and dσ/dT must be digitized from the figure or obtained from the authors. | Approximately 900–1700 | Not stated; rotating-field measurement is contactless, but no explicit density/volume correction is reported. | Rotating magnetic-field method; BeO crucible; evacuated to ≈0.001 Pa and backfilled with He to ≈10⁵ Pa; heating to 1400 °C followed by cooling and ≥15 min isothermal holds. | Total relative error ≈3%; random error in locating anomalous points <2% at p=0.95. | Chikova et al. (2016), *Acta Metallurgica Slovaca* 22, 153–163, DOI [10.12776/ams.v22i3.774](https://doi.org/10.12776/ams.v22i3.774) (chikova2016viscosityendelectrical pages 5-8, chikova2016viscosityendelectrical pages 3-5) | Fig. 1b; experimental-method section |
| Al–Si, broad-composition literature lead | Numerical data were not recoverable in the available corpus; consult the original article before model use. | Not established here | To be checked in original paper. | Direct liquid-alloy electrical/thermal-conductivity study. | To be checked in original paper. | Sun et al. (2019), “Thermal and electrical conductivity of liquid Al–Si alloys,” *International Journal of Thermophysics*, DOI [10.1007/s10765-019-2497-1](https://doi.org/10.1007/s10765-019-2497-1) | Original tables/figures not available in the retrieved text |
| Al–Si, broad-composition literature lead | Numerical data were not recoverable in the available corpus; consult the original article before model use. | Not established here | To be checked in original paper. | Liquid-alloy structure-sensitive-property measurements. | To be checked in original paper. | Sklyarchuk et al. (2009), “Structure sensitive properties of liquid Al–Si alloys,” *International Journal of Thermophysics* 30, 1400–1410, DOI [10.1007/s10765-009-0585-3](https://doi.org/10.1007/s10765-009-0585-3) | Original tables/figures not available in the retrieved text |
| AISI 316L, NIST SRM 1155a, liquid | **Corrected:** ρ<sub>corr</sub> = 1.154 + 1.893×10<sup>−4</sup>T. **Initial geometry:** ρ<sub>IG</sub> = 1.263 + 2.021×10<sup>−5</sup>T. | 1708–2900 | Both reported. Correction: ρ=ρ<sub>IG</sub>[d(T)/d<sub>RT</sub>]<sup>2</sup>; wire length is treated as constant during the pulse. | Ohmic pulse heating, ≈50 µs; current and voltage measured directly; radial expansion measured by time-resolved shadow imaging. | Corrected liquid 4.5%; uncorrected liquid 2.5%, both k=2 under GUM. | Pichler et al. (2020), *Journal of Materials Science* 55, 4081–4093, DOI [10.1007/s10853-019-04261-6](https://doi.org/10.1007/s10853-019-04261-6) (pichler2020measurementsofthermophysical pages 5-6, pichler2020measurementsofthermophysical pages 8-9, pichler2020measurementsofthermophysical pages 9-11) | Eq. 7; Table 3; Table 4; Table 6; Fig. 7 |
| AISI 316L, recommended compilation fit | ρ<sub>el</sub> = 0.740303 + 5.43411×10<sup>−13</sup>T³ | 1713–3000 | Yes; compilation recommends corrected pulse-heating data and warns that omission underestimates liquid ρ by about 5–10%. | Polynomial regression/critical compilation of pulse-heating datasets; not a new measurement. | No fit uncertainty reported in the extracted table. | Gilmutdinov et al. (2026 preprint), DOI [10.21203/rs.3.rs-10433902/v1](https://doi.org/10.21203/rs.3.rs-10433902/v1) (gilmutdinov2026practicalformulasfor pages 33-37, gilmutdinov2026practicalformulasfor media 9f405ad0) | Table 9; Fig. 7a |
| Ti–6Al–4V, liquid recommended compilation fit | ρ<sub>el</sub> = 1.96871 − 2.55261×10<sup>−4</sup>T + 5.91686×10<sup>−8</sup>T² − 7.56988×10<sup>−12</sup>T³ | 1921–3550 | Yes; intended to represent expansion-corrected data. | Regression/critical compilation drawing on pulse-heating datasets, including Boivineau et al. (2006), Basak et al. (2003), Kaschnitz et al. and Milošević et al.; not a new measurement. | No fit uncertainty reported in the extracted table. | Gilmutdinov et al. (2026 preprint), DOI [10.21203/rs.3.rs-10433902/v1](https://doi.org/10.21203/rs.3.rs-10433902/v1); underlying Boivineau et al. (2006), DOI [10.1007/PL00021868](https://doi.org/10.1007/PL00021868); Basak et al. (2003), DOI [10.1023/B:IJOT.0000004101.88449.86](https://doi.org/10.1023/B:IJOT.0000004101.88449.86) (basak2003measurementofspecific pages 11-13, gilmutdinov2026practicalformulasfor pages 33-37, gilmutdinov2026practicalformulasfor media 39b3cd9f, gilmutdinov2026practicalformulasfor media 9f405ad0) | Compilation Table 9 and Fig. 7b; Basak Fig. 5 |
| Ti–6Al–4V, ISS-EML benchmark near melting | Liquid equation is not legible in the retrieved excerpt. The reported **solid β-phase** relation is ρ<sub>e,s</sub> = (152.7±0.4) + (4.76±0.23)×10<sup>−3</sup>T µΩ·cm = (1.527±0.004) + (4.76±0.23)×10<sup>−5</sup>T µΩ·m; liquid results agree closely with Boivineau et al. | Solid fit: 1650–1900; liquid/undercooled data shown around the 1933 K liquidus | Geometry is measured inductively with density/diameter, so expansion is incorporated rather than applied as a separate wire correction. | Containerless electromagnetic levitation aboard the ISS; inductive resistivity and density measurement. | Instrumental resistivity uncertainty ≈0.05%; quoted 95% fit intervals additionally capture scatter from droplet motion/oscillation. | Mohr et al. (2020), *Advanced Engineering Materials* 22, DOI [10.1002/adem.202000169](https://doi.org/10.1002/adem.202000169) (mohr2020precisemeasurementsof pages 4-6, mohr2020precisemeasurementsof pages 6-7) | Eq. 19; Fig. 2a |
| Al6061 or Al–Mg–Si, liquid | No direct measured liquid-AA6061 fit was located. Provisional pure-Al baseline: ρ<sub>VE</sub> = 0.097 + 1.681×10<sup>−4</sup>T; this should not be labeled AA6061 without an alloy-scattering correction. | Baseline valid only for pure Al, 933.47–1491 | Pure-Al baseline is corrected for volume expansion. | Pure-Al submicrosecond ohmic pulse heating. Brandt and Neuer also investigated Al–Si alloys containing Mg/Cu up to and above melting, but no defensible AA6061 liquid fit was recoverable here. | Pure-Al fit uncertainty not stated numerically in the extracted table; AA6061 uncertainty unknown. | Leitner et al. (2017), DOI [10.1007/s11661-017-4053-6](https://doi.org/10.1007/s11661-017-4053-6); Brandt & Neuer (2003), DOI [10.1002/adem.200390007](https://doi.org/10.1002/adem.200390007); Brandt & Neuer (2007), DOI [10.1007/s10765-006-0144-0](https://doi.org/10.1007/s10765-006-0144-0) (brandt2003measurementofthe pages 1-2, brandt2003measurementofthe pages 2-4, leitner2017thermophysicalpropertiesof pages 4-5) | Leitner Table I, Table II and Fig. 2; Brandt & Neuer alloy-comparison figures/tables |


*Table: Measured liquid resistivity equations, ranges, expansion corrections, methods, uncertainties, and exact source locations. Rows clearly distinguish primary measurements from later compilation fits and flag systems for which no defensible direct numerical dataset was recovered.*

---

### (a) Liquid Al–Si Alloys (Hypereutectic, >12 wt% Si)

**Pure liquid aluminium (baseline).** Leitner et al. (2017) measured the electrical resistivity of pure aluminium by submicrosecond ohmic pulse-heating, averaging six consecutive experiments. The volume-expansion-corrected liquid resistivity follows a linear fit (leitner2017thermophysicalpropertiesof pages 4-5):

ρ_VE(T) = −0.097 + 1.681 × 10⁻⁴ T  [µΩ·m],  T_m = 933.47 K to 1491 K

The initial-geometry (uncorrected) value is ρ_IG(T) = −0.128 + 1.063 × 10⁻⁴ T µΩ·m. At the onset of the liquid phase (T_m = 933.47 K), the corrected resistivity is 0.2539 µΩ·m (25.39 µΩ·cm), and the uncorrected value is 0.2272 µΩ·m (leitner2017thermophysicalpropertiesof pages 5-6, leitner2017thermophysicalpropertiesof pages 6-7). These coefficients are reported in Table I of that paper; tabulated values at 50 K intervals appear in Table II.

**Hypereutectic Al–Si alloys.** Chikova et al. (2016) measured the electrical conductivity of liquid Al–Si alloys at compositions of 5, 8, 12, 14, 20, and 30 wt% Si using a rotating magnetic-field method in BeO crucibles under helium atmosphere (evacuated to ~0.001 Pa, then backfilled to ~10⁵ Pa) (chikova2016viscosityendelectrical pages 3-5). The temperature range covered approximately 900–1700 K (up to 1400 °C). The conductivity is represented as σ(T) = σ₀ + (dσ/dT)(T − T_L), with σ decreasing (hence ρ increasing) as temperature rises; silicon additions lower the absolute conductivity relative to pure aluminium (chikova2016viscosityendelectrical pages 5-8). The total relative measurement error is approximately 3%, with the random error for identifying anomalous temperature-dependence points below 2% at p = 0.95. Notably, the Al–16 wt% Si alloy exhibits abrupt resistivity changes at certain temperatures attributed to melt structural transitions (chikova2016viscosityendelectrical pages 3-5). However, numerical σ₀ and dσ/dT values must be digitised from Fig. 1b of their paper. DOI: [10.12776/ams.v22i3.774](https://doi.org/10.12776/ams.v22i3.774).

**Additional recommended references (not fully recoverable in this search).** Two papers that likely contain the most useful numerical data for the full Al–Si composition range in the liquid state were identified but could not be retrieved in full:

- **Sun, Muta, Kurosaki, and Ohishi (2019)**, "Thermal and electrical conductivity of liquid Al–Si alloys," *International Journal of Thermophysics*. DOI: [10.1007/s10765-019-2497-1](https://doi.org/10.1007/s10765-019-2497-1). This paper is likely the most directly relevant dataset for liquid Al–Si electrical conductivity across a range of compositions.

- **Sklyarchuk, Plevachuk, Yakymovych, Eckert, Willers, and Eigenfeld (2009)**, "Structure sensitive properties of liquid Al–Si alloys," *International Journal of Thermophysics* 30, 1400–1410. DOI: [10.1007/s10765-009-0585-3](https://doi.org/10.1007/s10765-009-0585-3). This paper reports density, viscosity, and electrical conductivity of liquid Al–Si alloys.

**Brandt and Neuer (2003, 2007)** measured the electrical resistivity of Al–Si alloys (up to ~12 wt% Si, with Cu and Mg additions) from room temperature up to and above the melting point using a steady-state four-probe method in a vacuum furnace; their 2007 paper (DOI: [10.1007/s10765-006-0144-0](https://doi.org/10.1007/s10765-006-0144-0)) extends to multi-component aluminium casting alloys and includes data at 650 °C (above the liquidus for many compositions) (brandt2003measurementofthe pages 1-2, brandt2003measurementofthe pages 2-4).

---

### (b) Liquid Ti–6Al–4V

**Mohr et al. (2020)** performed benchmark measurements of Ti–6Al–4V thermophysical properties using containerless electromagnetic levitation (EML) aboard the International Space Station. For the solid β-phase in the temperature range 1650–1900 K (mohr2020precisemeasurementsof pages 4-6):

ρ_e,s(T) = (152.7 ± 0.4) + (4.76 ± 0.23) × 10⁻³ T  [µΩ·cm],  i.e.  (1.527 ± 0.004) + (4.76 ± 0.23) × 10⁻⁵ T  [µΩ·m]

The measurement uncertainty of the electrical resistivity values is on the order of 0.05%, though the stated confidence intervals additionally capture scatter from residual sample oscillations and movements (mohr2020precisemeasurementsof pages 4-6). The geometry factor is calibrated against a solid Zr reference sample. The liquid-phase resistivity is stated to be "in very good agreement with the values obtained by Boivineau et al." (mohr2020precisemeasurementsof pages 6-7). The liquidus temperature is T_liq = 1933 K. DOI: [10.1002/adem.202000169](https://doi.org/10.1002/adem.202000169), Fig. 2a, Eq. 19.

**Boivineau et al. (2006)** measured the thermophysical properties of solid and liquid Ti–6Al–4V (TA6V) using a combined approach of DSC and the ohmic pulse-heating system at TU Graz, covering the liquid phase at high temperatures. This paper is widely cited as the primary source for liquid Ti–6Al–4V resistivity. DOI: [10.1007/PL00021868](https://doi.org/10.1007/PL00021868). The full text was not recoverable, but its data are reproduced in the Gilmutdinov compilation.

**Basak, Overfelt, and Wang (2003)** measured the electrical resistivity of Ti–6Al–4V (and IN 718, CF8M) using millisecond-resolution pulse-heating from ~1350 K to near the solidus. The expanded uncertainty in electrical resistivity was ±1% (two standard deviations) (basak2003measurementofspecific pages 11-13, basak2003measurementofspecific pages 7-11). The resistivity increases by ~2% over the 1350–1800 K range; the data show a small positive temperature coefficient. DOI: [10.1023/B:IJOT.0000004101.88449.86](https://doi.org/10.1023/B:IJOT.0000004101.88449.86), Fig. 5.

**Gilmutdinov et al. (2026, preprint)** compiled and fitted a critical assessment of all available pulse-heating data for Ti–6Al–4V. For the liquid phase, the expansion-corrected resistivity is given by a cubic polynomial (gilmutdinov2026practicalformulasfor media 9f405ad0):

ρ_el(T) = 1.96871 − 2.55261 × 10⁻⁴ T + 5.91686 × 10⁻⁸ T² − 7.56988 × 10⁻¹² T³  [µΩ·m],  1921 ≤ T ≤ 3550 K

A critical feature is that the uncorrected raw resistivity ρ_IG shows a non-physical drop upon melting (Δρ < 0), which disappears once volumetric thermal expansion is properly accounted for, yielding a positive resistivity jump Δρ > 0 (gilmutdinov2026practicalformulasfor pages 33-37). The compilation warns that neglecting thermal expansion correction results in a 5–10% underestimation of ρ in the liquid state. DOI: [10.21203/rs.3.rs-10433902/v1](https://doi.org/10.21203/rs.3.rs-10433902/v1), Table 9, Fig. 7b.

---

### (c) Liquid 316L Stainless Steel

**Pichler, Simonds, Sowards, and Pottlacher (2020)** (the Graz group) measured the thermophysical properties of NIST SRM 1155a (AISI 316L) using ohmic pulse heating with ~50 µs pulse duration, heating 0.5 mm diameter wire samples from room temperature through vaporisation. The solidus and liquidus temperatures are T_s = 1675 K and T_l = 1708 K, respectively (pichler2020measurementsofthermophysical pages 5-6). For the liquid phase (T_l to 2900 K), the fitted equations are (pichler2020measurementsofthermophysical pages 8-9):

**Thermal-expansion corrected:** ρ_corr(T) = 1.154 + 1.893 × 10⁻⁴ T  [µΩ·m]

**Initial geometry (uncorrected):** ρ_IG(T) = 1.263 + 2.021 × 10⁻⁵ T  [µΩ·m]

The correction uses ρ(t) = ρ_IG(t) × [d(t)/d_RT]², where d(t) is the wire diameter at time t measured by shadow imaging and d_RT is the room-temperature diameter (pichler2020measurementsofthermophysical pages 5-6). The expanded uncertainties (k = 2, GUM) are: corrected liquid resistivity 4.5%, uncorrected liquid resistivity 2.5% (pichler2020measurementsofthermophysical pages 9-11). Tabulated values at 100 K intervals are provided in Table 6; at 1700 K the corrected value is 1.464 µΩ·m, rising to 1.627 µΩ·m at 2500 K (pichler2020measurementsofthermophysical pages 9-11). DOI: [10.1007/s10853-019-04261-6](https://doi.org/10.1007/s10853-019-04261-6), Table 3, Table 4, Table 6, Fig. 7.

**Gilmutdinov et al. (2026)** provide a compiled fit for the liquid region (1713–3000 K) expressed as (gilmutdinov2026practicalformulasfor media 9f405ad0):

ρ_el(T) = 0.740303 + 5.43411 × 10⁻¹³ T³  [µΩ·m]

This unusual functional form (intercept plus a cubic term only) arises from their piecewise polynomial fitting strategy. For the solid region (298–1679 K), a 5th-degree polynomial is used. The slope in the liquid is approximately b ≈ 1.9 × 10⁻⁴ µΩ·m·K⁻¹, consistent with the Pichler et al. linear fit (gilmutdinov2026practicalformulasfor pages 33-37). DOI: [10.21203/rs.3.rs-10433902/v1](https://doi.org/10.21203/rs.3.rs-10433902/v1), Table 9, Fig. 7a.

---

### (d) Liquid Al6061 / Al–Mg–Si Alloys

No direct measurement of the electrical resistivity of liquid Al6061 (Al–1.0Mg–0.6Si–0.28Cu–0.20Cr, nominal) was identified in the literature searched. This is a significant gap, likely because: (i) the low liquidus temperature (~925 K) makes pyrometric pulse-heating measurements difficult for the same reasons discussed by Leitner et al. (2017) for pure aluminium, and (ii) Al6061 is not commonly studied in its fully liquid state.

**Practical approach for modelling.** The pure-aluminium liquid baseline from Leitner et al. (2017) provides ρ_VE = −0.097 + 1.681 × 10⁻⁴ T µΩ·m (corrected for volume expansion) from T_m = 933.47 K to 1491 K (leitner2017thermophysicalpropertiesof pages 4-5). The resistivity at the onset of the liquid phase is 0.2539 µΩ·m (corrected). For the dilute alloy corrections appropriate to the small solute concentrations in Al6061, Matthiessen's rule can be applied using the known room-temperature specific resistivities of Mg, Si, and Cu in aluminium solid solution.

**Brandt and Neuer (2003, 2007)** measured the resistivity of a series of Al–Si alloys with additions of 0.3 and 0.6 wt% Mg and 1–3 wt% Cu, extending from room temperature through the melting range (brandt2003measurementofthe pages 1-2, brandt2003measurementofthe pages 2-4). The 2003 paper (DOI: [10.1002/adem.200390007](https://doi.org/10.1002/adem.200390007)) reports data at 25 °C, 400 °C, 500 °C, and 650 °C for over 20 alloy compositions; their 2007 paper (DOI: [10.1007/s10765-006-0144-0](https://doi.org/10.1007/s10765-006-0144-0)) extends the analysis to thermal conductivity of ternary and multi-component aluminium alloys up to and above the melting temperature. These are the closest available data for Al–Mg–Si alloys near the liquidus but do not provide explicit liquid-phase ρ(T) fits for Al6061-type compositions.

---

### Key Practical Notes for Drude–Fresnel Implementation

1. **Thermal expansion correction is essential.** For all pulse-heating datasets, the distinction between ρ_IG (initial geometry, uncorrected) and ρ_corr (volume-expansion corrected) is critical. Neglecting this correction underestimates liquid resistivity by 5–10% and propagates directly into optical absorptivity via the Wiedemann–Franz-derived thermal conductivity and the Drude model's DC conductivity input (gilmutdinov2026practicalformulasfor pages 33-37).

2. **For Ti–6Al–4V**, the uncorrected resistivity appears to decrease upon melting, which is non-physical; only the corrected data show the expected positive resistivity jump at the liquidus (gilmutdinov2026practicalformulasfor pages 33-37).

3. **Temperature units.** All fitted equations above use T in kelvin and ρ in µΩ·m unless otherwise noted. The Mohr et al. Ti–6Al–4V solid-phase fit uses µΩ·cm (divide by 100 for µΩ·m).

4. **For hypereutectic Al–Si**, the resistivity data above the eutectic composition are sparse. The Sun et al. (2019) and Sklyarchuk et al. (2009) papers should be consulted directly for the most complete datasets. Liquid silicon itself is metallic (ρ ≈ 0.75–0.80 µΩ·m near its melting point of 1687 K), so the Al–Si system transitions from a low-resistivity liquid (pure Al, ~0.25 µΩ·m) to a moderate-resistivity liquid (pure Si, ~0.75 µΩ·m) with a non-trivial composition dependence influenced by the semiconductor-to-metal transition of silicon upon melting.

References

1. (leitner2017thermophysicalpropertiesof pages 5-6): Matthias Leitner, Thomas Leitner, Alexander Schmon, Kirmanj Aziz, and Gernot Pottlacher. Thermophysical properties of liquid aluminum. Metallurgical and Materials Transactions A, 48:3036-3045, Mar 2017. URL: https://doi.org/10.1007/s11661-017-4053-6, doi:10.1007/s11661-017-4053-6. This article has 314 citations.

2. (leitner2017thermophysicalpropertiesof pages 6-7): Matthias Leitner, Thomas Leitner, Alexander Schmon, Kirmanj Aziz, and Gernot Pottlacher. Thermophysical properties of liquid aluminum. Metallurgical and Materials Transactions A, 48:3036-3045, Mar 2017. URL: https://doi.org/10.1007/s11661-017-4053-6, doi:10.1007/s11661-017-4053-6. This article has 314 citations.

3. (leitner2017thermophysicalpropertiesof pages 4-5): Matthias Leitner, Thomas Leitner, Alexander Schmon, Kirmanj Aziz, and Gernot Pottlacher. Thermophysical properties of liquid aluminum. Metallurgical and Materials Transactions A, 48:3036-3045, Mar 2017. URL: https://doi.org/10.1007/s11661-017-4053-6, doi:10.1007/s11661-017-4053-6. This article has 314 citations.

4. (chikova2016viscosityendelectrical pages 5-8): Оlga А. Chikova, Konstantin V. Nikitin, Olga P. Moskovskikh, and Vladimir S. Tsepelev. Viscosity end electrical conductivity of liquid hypereutectic alloys al-si. Acta Metallurgica Slovaca, 22:153-163, Sep 2016. URL: https://doi.org/10.12776/ams.v22i3.774, doi:10.12776/ams.v22i3.774. This article has 29 citations.

5. (chikova2016viscosityendelectrical pages 3-5): Оlga А. Chikova, Konstantin V. Nikitin, Olga P. Moskovskikh, and Vladimir S. Tsepelev. Viscosity end electrical conductivity of liquid hypereutectic alloys al-si. Acta Metallurgica Slovaca, 22:153-163, Sep 2016. URL: https://doi.org/10.12776/ams.v22i3.774, doi:10.12776/ams.v22i3.774. This article has 29 citations.

6. (pichler2020measurementsofthermophysical pages 5-6): Peter Pichler, Brian J. Simonds, Jeffrey W. Sowards, and Gernot Pottlacher. Measurements of thermophysical properties of solid and liquid nist srm 316l stainless steel. Journal of materials science, 55:4081-4093, Dec 2019. URL: https://doi.org/10.1007/s10853-019-04261-6, doi:10.1007/s10853-019-04261-6. This article has 170 citations and is from a peer-reviewed journal.

7. (pichler2020measurementsofthermophysical pages 8-9): Peter Pichler, Brian J. Simonds, Jeffrey W. Sowards, and Gernot Pottlacher. Measurements of thermophysical properties of solid and liquid nist srm 316l stainless steel. Journal of materials science, 55:4081-4093, Dec 2019. URL: https://doi.org/10.1007/s10853-019-04261-6, doi:10.1007/s10853-019-04261-6. This article has 170 citations and is from a peer-reviewed journal.

8. (pichler2020measurementsofthermophysical pages 9-11): Peter Pichler, Brian J. Simonds, Jeffrey W. Sowards, and Gernot Pottlacher. Measurements of thermophysical properties of solid and liquid nist srm 316l stainless steel. Journal of materials science, 55:4081-4093, Dec 2019. URL: https://doi.org/10.1007/s10853-019-04261-6, doi:10.1007/s10853-019-04261-6. This article has 170 citations and is from a peer-reviewed journal.

9. (gilmutdinov2026practicalformulasfor pages 33-37): Vitaliy Gilmutdinov, Rinetta Mosina, Georgii Gordeev, Vladimir Ankudinov, Igor Kuzmin, and Mikhail Krivilyov. Practical formulas for additive manufacturing alloys: thermophysical and mechanical properties. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10433902/v1, doi:10.21203/rs.3.rs-10433902/v1.

10. (gilmutdinov2026practicalformulasfor media 9f405ad0): Vitaliy Gilmutdinov, Rinetta Mosina, Georgii Gordeev, Vladimir Ankudinov, Igor Kuzmin, and Mikhail Krivilyov. Practical formulas for additive manufacturing alloys: thermophysical and mechanical properties. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10433902/v1, doi:10.21203/rs.3.rs-10433902/v1.

11. (basak2003measurementofspecific pages 11-13): D. Basak, R. A. Overfelt, and D. Wang. Measurement of specific heat capacity and electrical resistivity of industrial alloys using pulse heating techniques. International Journal of Thermophysics, 24:1721-1733, Nov 2003. URL: https://doi.org/10.1023/b:ijot.0000004101.88449.86, doi:10.1023/b:ijot.0000004101.88449.86. This article has 115 citations and is from a peer-reviewed journal.

12. (gilmutdinov2026practicalformulasfor media 39b3cd9f): Vitaliy Gilmutdinov, Rinetta Mosina, Georgii Gordeev, Vladimir Ankudinov, Igor Kuzmin, and Mikhail Krivilyov. Practical formulas for additive manufacturing alloys: thermophysical and mechanical properties. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10433902/v1, doi:10.21203/rs.3.rs-10433902/v1.

13. (mohr2020precisemeasurementsof pages 4-6): Markus Mohr, Rainer Wunderlich, Rada Novakovic, Enrica Ricci, and Hans-Jörg Fecht. Precise measurements of thermophysical properties of liquid ti–6al–4v (ti64) alloy on board the international space station. Advanced Engineering Materials, Apr 2020. URL: https://doi.org/10.1002/adem.202000169, doi:10.1002/adem.202000169. This article has 84 citations and is from a peer-reviewed journal.

14. (mohr2020precisemeasurementsof pages 6-7): Markus Mohr, Rainer Wunderlich, Rada Novakovic, Enrica Ricci, and Hans-Jörg Fecht. Precise measurements of thermophysical properties of liquid ti–6al–4v (ti64) alloy on board the international space station. Advanced Engineering Materials, Apr 2020. URL: https://doi.org/10.1002/adem.202000169, doi:10.1002/adem.202000169. This article has 84 citations and is from a peer-reviewed journal.

15. (brandt2003measurementofthe pages 1-2): R. Brandt and G. Neuer. Measurement of the electric resistivity of metals up to and above the melting temperature. Advanced Engineering Materials, 5:52-55, Feb 2003. URL: https://doi.org/10.1002/adem.200390007, doi:10.1002/adem.200390007. This article has 18 citations and is from a peer-reviewed journal.

16. (brandt2003measurementofthe pages 2-4): R. Brandt and G. Neuer. Measurement of the electric resistivity of metals up to and above the melting temperature. Advanced Engineering Materials, 5:52-55, Feb 2003. URL: https://doi.org/10.1002/adem.200390007, doi:10.1002/adem.200390007. This article has 18 citations and is from a peer-reviewed journal.

17. (basak2003measurementofspecific pages 7-11): D. Basak, R. A. Overfelt, and D. Wang. Measurement of specific heat capacity and electrical resistivity of industrial alloys using pulse heating techniques. International Journal of Thermophysics, 24:1721-1733, Nov 2003. URL: https://doi.org/10.1023/b:ijot.0000004101.88449.86, doi:10.1023/b:ijot.0000004101.88449.86. This article has 115 citations and is from a peer-reviewed journal.
