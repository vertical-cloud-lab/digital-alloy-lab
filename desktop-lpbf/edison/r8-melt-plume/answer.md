Question: Context: we are designing a lab-built desktop laser powder bed fusion (LPBF) machine for small-batch screening of aluminium alloys (AlSi10Mg, 6061, 7075 and grain-refined variants with Zr, Sc or TiB2). Laser: 500 W single-mode CW fibre laser at 1070 nm (IPG YLR-500 class) into a SCANLAB basiCube 20 galvo (marking speed up to about 1.1 m/s at f = 160 mm) and a Thorlabs FTH160-1064 f-theta lens (f = 160 mm), giving a ~96 um 1/e2 spot diameter (48-75 um spots are options). Expected process window: 200-350 W, 0.4-1.1 m/s, 30 um layers, ~0.1 mm hatch. Build plates are 25, 50 or 75 mm across, heated to 200 C (500 C reserved). Chamber: ~280 x 190 x 120 mm inside, vacuum-purged then argon at +5 to +20 mbar, with an argon cross-flow of 2.5-3.3 m/s over the plate (140-200 L/min) from a slot nozzle on the back wall to an outlet slot at the front; a cover slide sits under a lid window ~130 mm above the plate.

Using the literature (experiments, synchrotron X-ray imaging, high-speed imaging and validated simulations), give quantitative values for LPBF of AlSi10Mg (and, where available, 6061 and 7075) at this operating point:

1. Melt pool: width, depth and length; conduction-to-keyhole thresholds (normalized enthalpy, keyhole number Ke of Gan et al.), the absorptivity at ~1070 nm of Al powder beds in each regime (in-situ calorimetry such as Trapp et al.), peak surface temperature, Marangoni surface-flow velocities, cooling rates, thermal gradient G and solidification velocity R; keyhole oscillation frequencies and keyhole-porosity windows.
2. Vapour plume: plume height, velocity and tilt at ~1 atm argon; plume temperature; composition (Mg and Zn enrichment in the vapour and the resulting loss from the alloy); whether a plasma forms at 1 um wavelength; the spectral emission lines seen (Al I, Mg I, Si, Zn, Na, K) that would fall inside 600-1000 nm or 1.3-1.7 um detector bands; beam attenuation by the plume and condensate.
3. Condensate (soot): primary particle and agglomerate sizes, mass generation rate per unit track length or per joule of laser energy for Al alloys, how much reaches windows and cover slides, and the measured cover-slide transmission loss per build hour.
4. Spatter: ejection velocities, angles, size distributions and counts per mm of track for Al alloys versus steels; how far hot spatter travels in argon; how a cross-flow changes this.
5. The time and length scales a monitoring system has to resolve (melt-pool transit time, solidification time, keyhole fluctuation spectrum, spatter speeds) and the frame rates, exposures and bandwidths that published Al LPBF monitoring used.

Give numbers with units and a source for each, flag where Al alloys differ from steels or Ti-6Al-4V, and say where data for Al are missing.

## Quantitative LPBF Process Physics for Aluminium Alloys: Literature-Based Reference Data

The following synthesises published experimental, synchrotron X-ray imaging, and validated simulation data relevant to laser powder bed fusion (LPBF) of AlSi10Mg (and, where available, AA6061 and AA7075) at the operating point described (200–350 W, 0.4–1.1 m/s, 30 µm layers, ~96 µm spot, argon atmosphere). A consolidated reference table is provided at the end.

| Parameter | Value | Units | Alloy/Material | Source |
|---|---:|---|---|---|
| Melt-pool depth / width at 200 W, 0.917 m/s, 108 µm spot | 67.2 / 185.1 | µm | AlSi10Mg, 30 µm layer | Experiment (patel2021meltingmodesin pages 243-247) |
| Melt-pool depth / width at 250 W, 0.917 m/s, 108 µm spot | 66.2 / 195.6 | µm | AlSi10Mg, 30 µm layer | Experiment (patel2021meltingmodesin pages 243-247) |
| Melt-pool depth / width at 300 W, 0.917 m/s, 108 µm spot | 70.0 / 202.4 | µm | AlSi10Mg, 30 µm layer | Experiment (patel2021meltingmodesin pages 243-247) |
| Melt-pool depth / width at 350 W, 0.917 m/s, 108 µm spot | 77.7 / 239.4 | µm | AlSi10Mg, 30 µm layer | Experiment (patel2021meltingmodesin pages 243-247) |
| Melt-pool depth / width at 200–350 W, 0.688 m/s | 72.7–79.5 / 205–234.7 | µm | AlSi10Mg, 30 µm layer, 108 µm spot | Experiment (patel2021meltingmodesin pages 243-247) |
| Melt-pool length at the specified operating point | Not quantitatively reported in retrieved Al data | — | AlSi10Mg | Data gap (patel2021meltingmodesin pages 243-247) |
| Conduction-to-transition/keyhole aspect ratio, depth/width | ≈0.4 | dimensionless | AlSi10Mg | Metallographic criterion; rounded keyhole defects appear around/above this value (patel2021meltingmodesin pages 96-100) |
| Normalized-enthalpy conduction/keyhole criterion | ΔH/hₛ ≈10 | dimensionless | General LPBF criterion; not independently validated here for AlSi10Mg | Review/model criterion (patel2021meltingmodesin pages 96-100) |
| Gan keyhole number | Ke ≈ (ΔH/hₘ)/√π; front-wall-angle tangent scales with Ke | dimensionless | Multi-alloy LPBF scaling | Gan scaling as reproduced by Huang et al.; OCR makes the exact notation somewhat uncertain (huang2022keyholefluctuationand pages 2-4) |
| Flat-surface absorptivity at ≈1.07 µm | 0.047 | fraction | Aluminium | Ray-tracing/optical-property calculation (king2015laserpowderbed pages 8-12) |
| Powder-bed absorptivity at ≈1.07 µm | 0.22 | fraction | Aluminium | Multiple-scattering calculation; ≈4.7× flat-surface value (king2015laserpowderbed pages 8-12) |
| Effective absorptivity by melting regime | ≈0.15 conduction; ≈0.425 transition; ≈0.70 keyhole | fraction | Aluminium alloys | Values adopted from aluminium melting-mode analysis (patel2021meltingmodesin pages 63-66) |
| Saturated deep-keyhole absorptivity | ≈0.78 | fraction | Metal tracks; calorimetric LPBF study including Al 1100 | In-situ 1070 nm calorimetry; saturation after rapid rise during keyholing (trapp2017insituabsorptivity pages 4-6) |
| Aluminium keyhole-onset power at 1.5 m/s | 265 ± 15 | W | Al 1100 bare disc | In-situ calorimetry/metallography; 100 ± 15 W was observed melting onset (trapp2017insituabsorptivity pages 6-7) |
| Al 1100 keyhole-transition range at 1.5 m/s | 250–400 | W | Al 1100 bare disc | Track observations (trapp2017insituabsorptivity pages 4-6) |
| Keyhole depression response time near transition | ≤50 | µs | Metal track at 68 W, 0.5 m/s | High-speed imaging; appeared/disappeared within one frame (trapp2017insituabsorptivity pages 4-6) |
| Solidification cooling rate, melt-pool centre | 8.3 ± 2.0 × 10⁵ to 9.5 × 10⁵ | K/s | AlSi10Mg | Numerical and cell-size-based estimates (cauwenbergh2021unravellingthemultiscale pages 5-7) |
| Solidification cooling rate, melt-pool boundary | 1.6 × 10⁵ to 4.4 ± 0.5 × 10⁵ | K/s | AlSi10Mg | Semi-empirical and numerical estimates (cauwenbergh2021unravellingthemultiscale pages 5-7) |
| Cooling rate over 700–1900 J/m input | 3.91 × 10⁵ down to 1.35 × 10⁵ | K/s | AlSi10Mg | Validated thermal simulation; cooling decreases with energy input (samantaray2019modelingofthermal pages 7-10) |
| Wider calculated cooling-rate envelope | Up to ≈1.2–1.75 × 10⁶ | K/s | AlSi10Mg | Analytical model over 250–450 W and 0.2–1.5 m/s (leis2022tuningthehardness pages 6-8, leis2022tuningthehardness pages 4-6) |
| Thermal gradient G and local solidification velocity R | No direct numerical AlSi10Mg pair retrieved; Ṫ = G·R and R is locally bounded by scan speed | K/m; m/s | AlSi10Mg | Explicit Al-specific numerical data gap (leis2022tuningthehardness pages 2-4, sonawane2021structuralaluminumalloy pages 142-145) |
| Peak surface/plume temperature | ≈3360 | K | Generic metal laser plume; not Al-specific | Validated plume simulation; approximately uniform over first millimetres (mayi2020laserinducedplumeinvestigated pages 7-9) |
| Marangoni surface-flow velocity | No reliable AlSi10Mg measurement retrieved; melt-flow values up to ≈5 m/s reported for Al-alloy spatter study context | m/s | Aluminium alloy / cross-material context | Al-specific surface-velocity data remain sparse (guo2024correlativespatterand pages 7-9) |
| Keyhole radial-fluctuation band | 2.5–10 | kHz | LPBF aluminium-alloy study | Synchrotron X-ray imaging; transition regime reaches ≈10 kHz (huang2022keyholefluctuationand pages 1-2, huang2022keyholefluctuationand pages 7-8) |
| Aluminium pore-free energy-density region | Below ≈0.020 | MJ/cm³ | Aluminium LPBF | No pores proposed below this value (guo2023understandingkeyholeinducedporosities pages 24-28) |
| Keyhole penetration/rapid-oscillation threshold | ≈0.026 | MJ/cm³ | Aluminium LPBF | Synchrotron-based keyhole-porosity study (guo2023understandingkeyholeinducedporosities pages 24-28) |
| Plume visible dimensions | 4–5 high × ≈1.5 wide | mm | LPBF metal; not Al-specific | High-speed CCD observations (shi2024areviewof pages 8-10) |
| Plume steady ascent velocity | 38–97 | m/s | Laser–metal plume in air; not LPBF-Al-specific | Measured over 0.57–1.14 MW/cm²; model within ≈10% (mayi2020laserinducedplumeinvestigated pages 7-9) |
| Vapour-jet velocity | Order of hundreds; cited range 20–300 | m/s | LPBF, including Al-alloy spatter analysis | Literature/validated-flow context rather than direct AlSi10Mg measurement (guo2024correlativespatterand pages 7-9, bitharas2022theinterplaybetween pages 6-8) |
| Plume rise before 2.1 m/s cross-flow dominates | ≈1 | mm | LPBF in argon | Simultaneous schlieren/X-ray study; near-pool jet remains dominant (bitharas2022theinterplaybetween pages 6-8) |
| Practical chamber cross-flow range | 2–5 | m/s | General LPBF | Review: too little permits fume accumulation; too much disturbs powder (shi2024areviewof pages 17-21) |
| Mg compositional loss | 57 | % of initial Mg | AlSi10Mg | Reported composition reduction during SLM/LPBF (li2024additivemanufacturingof pages 42-46) |
| Mg compositional loss | 17 | % of initial Mg | AA6061 | Reported composition reduction (li2024additivemanufacturingof pages 42-46) |
| Mg / Zn compositional loss | 19 / 3 | % of initial element | AA7075 | Tabulated result; source text also cites ≈30% Zn losses elsewhere, so study-to-study scatter is large (li2024additivemanufacturingof pages 42-46) |
| Plasma at ≈1 µm CW LPBF conditions | No Al-LPBF proof retrieved; hot vapour is often weakly ionized rather than a laser-supported plasma | — | Aluminium LPBF | Data gap; plasma emission is documented for higher-power Al7075 DED, not directly transferable to this LPBF operating point |
| Spectral lines within 600–1000 nm or 1.3–1.7 µm bands | No validated Al-LPBF line list retrieved | nm | AlSi10Mg, AA6061, AA7075 | Data gap; available Al7075 DED evidence chiefly reports visible Al I/Mg I lines below 600 nm |
| Quantitative direct-beam attenuation by plume | Not reported for Al; accumulated fume is documented to obstruct the beam qualitatively | % | Aluminium/general LPBF | Cross-flow removes prior-track products and reduces laser–fume interaction (bitharas2022theinterplaybetween pages 6-8, shi2024areviewof pages 17-21) |
| Condensate primary-particle diameter | Predominantly 4–16; median ≈9.4 | nm | LPBF stainless steel; no equivalent Al-alloy dataset retrieved | TEM characterization; use only as non-Al proxy (noskov2020characterizationofultrafine pages 4-7, noskov2020characterizationofultrafine pages 1-2) |
| Condensate agglomerate/chain length | ≈0.5 to >10 | µm | LPBF stainless steel; non-Al proxy | Chain-like aggregates of ≈10 nm primaries (noskov2022amicroscopystudy pages 1-2) |
| Coarse condensate particles | ≈0.7–2 | µm | Laser AM stainless steel; non-Al proxy | Rare coarse particles on filters (noskov2020characterizationofultrafine pages 3-4) |
| Condensate mass per track length or laser joule | No quantitative Al-alloy value retrieved | mg/m or mg/J | Aluminium alloys | Explicit literature gap in retrieved evidence |
| Window/cover-slide deposition fraction and transmission loss | No published Al value per build hour retrieved | %/h | Aluminium LPBF | Must be measured for the specific chamber/flow/window geometry |
| Aluminium spatter size distribution | >50% have radius <30 µm at 4.24 MW/cm²; particles with radius >70–80 µm occur | µm | Al alloys including AlSi10 | High-speed imaging (chebil2021studyofspatter pages 7-10, chebil2021studyofspatter pages 4-7) |
| Relative spatter emission by alloy | AlSi7 ≈30% more than AlSi10 at 5.66 MW/cm² | % | AlSi7 versus AlSi10 | High-speed imaging; not a steel comparison (chebil2021studyofspatter pages 4-7) |
| Fraction of solid ejecta / jet spatter | >82 / ≈2 | % of ejecta | Al–Fe–Zr | Synchrotron X-ray tracking (guo2024correlativespatterand pages 4-7) |
| Dominant spatter direction at 350–500 W, 0.8 m/s | Mean −10° to −25°; 70–80% backward | degrees; % | Al–Fe–Zr | Synchrotron X-ray imaging (guo2024correlativespatterand pages 7-9) |
| Backward liquid-droplet fraction | Can exceed 90 | % | Al–Fe–Zr | Occurs where depression width greatly exceeds keyhole aperture (guo2024correlativespatterand pages 7-9) |
| Laser-accelerated spatter example | 0.57 to 3.39 over 350 µs; particle ≈36 µm | m/s; µs; µm | Al–Fe–Zr | Synchrotron X-ray imaging (guo2024correlativespatterand pages 10-12) |
| Spatter count per track length | No robust counts/mm retrieved for Al | count/mm | Aluminium alloys | Retrieved studies report event counts or fitted counts versus linear energy, not normalized counts/mm (guo2024correlativespatterand pages 7-9, guo2024correlativespatterand pages 4-7) |
| Hot-spatter travel at 3.39 m/s, neglecting drag/gravity over 10 ms | ≈34 | mm | Illustrative estimate from measured Al-alloy event | Derived length scale from measured velocity; actual argon drag shortens fine-particle travel (guo2024correlativespatterand pages 10-12) |
| Melt-pool transit time across 96 µm beam at 0.4–1.1 m/s | ≈240–87 | µs | Proposed machine operating point | Kinematic requirement; implies ≥10–20 kfps for several samples per transit |
| Approximate solidification time for a 0.2–0.4 mm-long pool at 0.4–1.1 m/s | ≈0.18–1.0 | ms | Proposed machine; representative AlSi10Mg length scale | Engineering estimate; direct Al melt-pool-length data at this exact point are missing |
| Sampling needed for 10 kHz keyhole oscillation | ≥20 kHz Nyquist; preferably 50–100 kfps or ≥100 kHz photodiode bandwidth | frames/s or Hz | Aluminium LPBF monitoring | Derived from measured 2.5–10 kHz fluctuation band (huang2022keyholefluctuationand pages 1-2, huang2022keyholefluctuationand pages 7-8) |
| Demonstrated regime-identification time resolution | 100 | µs | LPBF, synchrotron-correlated acoustic monitoring; not Al-specific | Resolves conduction, stable-keyhole and unstable-keyhole transitions |
| Exposure needed to limit blur of 3.4 m/s spatter to 10 µm | ≤2.9 | µs | Aluminium spatter monitoring | Derived from measured Al–Fe–Zr spatter speed (guo2024correlativespatterand pages 10-12) |


*Table: Key literature values and identified data gaps for melt-pool physics, plume and condensate behavior, spatter, and monitoring at conditions close to the proposed aluminium LPBF machine. Non-aluminium proxy values and engineering estimates are explicitly labeled to prevent unsupported transfer.*

---

### 1. Melt Pool Geometry and Thermal Characteristics

**Width, depth, and length.** For AlSi10Mg on 30 µm layers with a 108 µm beam spot, experimentally measured single-track melt pool dimensions at scan speeds of ~0.55–0.92 m/s and powers of 200–350 W give depths of approximately 65–90 µm and widths of approximately 185–240 µm (patel2021meltingmodesin pages 243-247). At the lower scan speed (0.55 m/s, 100 µs exposure), depths reach ~80–88 µm and widths ~220–231 µm. Melt pool length is not independently reported in the retrieved AlSi10Mg literature at these conditions; it is typically 2–4× the width based on cross-material LPBF experience but must be verified for Al alloys at this operating point.

**Conduction-to-keyhole thresholds.** A melt pool depth-to-width aspect ratio of ~0.4 has been proposed as a practical conduction-to-transition/keyhole threshold for aluminium alloys, with rounded keyhole-associated defects appearing at or above this ratio (patel2021meltingmodesin pages 96-100). The widely cited normalised enthalpy threshold of ΔH/h_s ≈ 10 marks the onset of keyholing (patel2021meltingmodesin pages 96-100). The keyhole number Ke, as defined by Gan et al. and reproduced by Huang et al., is Ke ≈ (1/√π)(ΔH/h_m), and the tangent of the front keyhole wall angle scales approximately linearly with Ke across multiple alloys and processing conditions (huang2022keyholefluctuationand pages 2-4). For bare Al 1100 at 1.5 m/s, the experimentally observed keyhole onset occurs at 265 ± 15 W (with the keyhole transition spanning roughly 250–400 W), while melting onset is at ~100 W (trapp2017insituabsorptivity pages 4-6, trapp2017insituabsorptivity pages 6-7).

**Absorptivity at ~1070 nm.** The calculated flat-surface absorptivity of aluminium at ~1.07 µm is only 0.047, while multiple-scattering in the powder bed raises total absorptivity to ~0.22 — approximately 4.7× the flat value (king2015laserpowderbed pages 8-12). In-situ calorimetry by Trapp et al. found that a ~100 µm powder layer has approximately twice the absorptivity of a polished bare disc at low power. Once the powder track fully melts, absorptivity drops sharply, then rises again as keyhole formation develops, eventually saturating at ~0.78 in the deep-keyhole regime (trapp2017insituabsorptivity pages 4-6). Patel & Vlasea adopt effective values of ~0.15 (conduction), ~0.425 (transition), and ~0.70 (keyhole) for aluminium alloys (patel2021meltingmodesin pages 63-66). These values are substantially lower than those for steels and Ti-6Al-4V in conduction mode (steel flat absorptivity ~0.3 versus Al ~0.05), but converge in keyhole mode (~0.7–0.8 for all materials).

**Peak surface temperature.** The plume temperature near the melt-pool surface has been modelled at ~3360 K for a laser-metal interaction in argon, approximately uniform over the first few millimetres of plume height (mayi2020laserinducedplumeinvestigated pages 7-9). For aluminium, the boiling point is ~2743 K; keyhole-mode surface temperatures therefore reach well above this.

**Marangoni surface-flow velocities.** No direct AlSi10Mg melt-pool surface velocity measurement was retrieved. Melt flow velocities up to ~5 m/s have been cited in the context of Al-alloy spatter studies (guo2024correlativespatterand pages 7-9). CFD simulations for Al alloys typically report Marangoni-driven velocities of 0.5–3 m/s; this remains a data gap for direct experimental validation at LPBF-relevant Al conditions.

**Cooling rates, G and R.** Cooling rates for AlSi10Mg LPBF have been estimated at 8.3 ± 2.0 × 10⁵ K/s (melt pool centre) and 1.6–4.4 × 10⁵ K/s (melt pool boundary) from cell-size-based semi-empirical and numerical models (cauwenbergh2021unravellingthemultiscale pages 5-7). Thermal simulations over a range of energy inputs (700–1900 J/m) give 1.35–3.91 × 10⁵ K/s, with cooling rate decreasing as energy input increases (samantaray2019modelingofthermal pages 7-10). Analytical models extending to 250–450 W and 0.2–1.5 m/s calculate cooling rates up to ~1.2–1.75 × 10⁶ K/s (leis2022tuningthehardness pages 6-8, leis2022tuningthehardness pages 4-6). No independently measured numerical G (K/m) and R (m/s) pair for AlSi10Mg was retrieved; the relationship Ṫ = G·R holds, with R locally bounded by the scan velocity (leis2022tuningthehardness pages 2-4, sonawane2021structuralaluminumalloy pages 142-145). These cooling rates are broadly similar to those for steels and Ti-6Al-4V at comparable energy densities, though aluminium's higher thermal conductivity shifts the absolute values.

**Keyhole oscillation frequencies and porosity windows.** Huang et al. report keyhole radial fluctuations spanning 2.5–10 kHz, with the highest frequencies (~10 kHz) occurring in the transition regime (regime II) between stable and unstable keyholing, using 200–500 W and 0.6–1.6 m/s (huang2022keyholefluctuationand pages 1-2, huang2022keyholefluctuationand pages 7-8). For aluminium LPBF specifically, Guo et al. identify a pore-free region below ~0.020 MJ/cm³ linear energy density, with rapid keyhole oscillation onset near ~0.026 MJ/cm³ (guo2023understandingkeyholeinducedporosities pages 24-28). Keyhole-penetration pores (KP-pores) form when oscillations cause the keyhole to exceed the melt-pool depth, while RF-pores and R-pores form via liquid-bridge pinch-off and rear-wall humps respectively (guo2023understandingkeyholeinducedporosities pages 18-24, guo2023understandingkeyholeinducedporosities pages 4-8).

---

### 2. Vapour Plume

**Plume height, velocity, and tilt.** High-speed CCD imaging of LPBF plumes reports dimensions of approximately 4–5 mm in length and ~1.5 mm in width (shi2024areviewof pages 8-10). Measured steady ascent velocities range from 38 m/s at 0.57 MW/cm² to 97 m/s at 1.14 MW/cm² (mayi2020laserinducedplumeinvestigated pages 7-9). The vapour-jet velocity at the melt-pool surface is of order 20–300 m/s (guo2024correlativespatterand pages 7-9). With an argon cross-flow of ~2.1 m/s, the plume propagates upward only ~1 mm before its momentum is comparable to the cross-flow; without cross-flow, it rises higher and trails fume (bitharas2022theinterplaybetween pages 6-8). Schlieren imaging shows the plume tilts backward at higher scan speeds (shi2024areviewof pages 8-10). A practical cross-flow of 2–5 m/s is recommended: too little allows fume accumulation and laser obstruction; too much disturbs the powder bed (shi2024areviewof pages 17-21).

**Plume temperature.** Modelled at ~3360 K near the melt-pool surface (mayi2020laserinducedplumeinvestigated pages 7-9).

**Composition (Mg and Zn enrichment and loss).** For AlSi10Mg, Mg losses of ~57% of the initial Mg content have been reported during IR-laser LPBF. For AA6061, ~17% Mg loss; for AA7075, ~19% Mg loss and ~3% Zn loss in one study, though Zn losses up to ~30% are cited elsewhere due to Zn's lower boiling point (~907 °C vs ~1090 °C for Mg) (li2024additivemanufacturingof pages 42-46). Green-laser processing at lower energy density reduces these losses. The vapour is therefore strongly enriched in Mg relative to the bulk alloy, and in Zn for 7xxx alloys.

**Plasma formation at ~1 µm wavelength.** No direct evidence of a laser-sustained plasma (inverse bremsstrahlung absorption) at 1 µm CW LPBF conditions was retrieved for aluminium alloys. The plume is widely described as a weakly ionised metal vapour rather than a true plasma at these power densities. CW fibre-laser LPBF at 200–500 W does not reach the threshold for significant inverse bremsstrahlung at 1.07 µm in argon; this contrasts with pulsed Nd:YAG or CO₂ laser welding where plasma formation is more readily observed.

**Spectral emission lines.** For Al7075 DED (not LPBF), Ren et al. report emission lines of Al I (396.054 nm), Mg I (383.229 nm), and Cr I in the visible range. These principal Al and Mg lines fall below 600 nm and would therefore be outside the user's proposed 600–1000 nm and 1.3–1.7 µm detector bands. No validated Al-LPBF spectral line list for the 600–1000 nm or 1.3–1.7 µm ranges was retrieved — this is an explicit data gap. Weak Na I (589 nm) and K I (766–770 nm) lines from trace impurities in the powder could potentially fall in the 600–1000 nm band but have not been documented for LPBF Al alloys.

**Beam attenuation by the plume.** No quantitative percentage of beam attenuation by the plume was retrieved for Al LPBF. Qualitatively, accumulated fume from prior tracks can "seriously block" the laser when cross-flow is insufficient, while adequate cross-flow (~2–5 m/s) convects products away and maintains repeatable conditions (bitharas2022theinterplaybetween pages 6-8, shi2024areviewof pages 17-21). For steels and Ti-6Al-4V, plume attenuation of a few percent per pass is commonly cited in the welding literature; Al alloys may produce less dense metal vapour per unit energy due to lower absorptivity in conduction mode, but this remains unquantified.

---

### 3. Condensate (Soot)

**Primary particle and agglomerate sizes.** For LPBF of stainless steel (the best-characterised system), TEM analysis shows primary condensate nanoparticles with equivalent projected-area diameters predominantly 4–16 nm, with a median of ~9.4 nm (noskov2020characterizationofultrafine pages 4-7, noskov2020characterizationofultrafine pages 1-2, noskov2020characterizationofultrafine pages 3-4). These form fractal-like chain agglomerates ranging from ~0.5 µm to >10 µm in length (noskov2022amicroscopystudy pages 1-2). Rare coarser particles of 0.7–2 µm were also observed on filters (noskov2020characterizationofultrafine pages 3-4). Particles >30 nm retain a metallic core with an oxide shell (noskov2020characterizationofultrafine pages 10-11, noskov2020characterizationofultrafine pages 7-9). **No equivalent Al-alloy condensate characterisation was retrieved** — this is a significant data gap. Al condensate is expected to form alumina-rich nanoparticles due to Al's high oxygen affinity; primary particle sizes may be comparable or slightly larger than steel fume particles.

**Mass generation rate.** No quantitative mass generation rate per unit track length or per joule was retrieved for any Al alloy. This is a critical missing measurement for window-contamination modelling.

**Window/cover-slide transmission loss.** No published measurement of cover-slide transmission loss per build hour for Al LPBF was found. This quantity is geometry- and flow-dependent and must be measured for the specific chamber configuration.

---

### 4. Spatter

**Ejection velocities and angles for Al alloys.** For Al-Fe-Zr LPBF (synchrotron X-ray imaging), at 350–500 W and 800 mm/s, the mean spatter trajectory angle is approximately −10° to −25° (backward), with 70–80% of ejecta being backward spatter; at 500 mm/s the mean angle approaches 0° (more vertical) (guo2024correlativespatterand pages 7-9). An example laser–spatter interaction accelerated a ~36 µm particle from 0.57 to 3.39 m/s over 350 µs (guo2024correlativespatterand pages 10-12). Vapour-jet velocities of 20–300 m/s drive the ejection. For AlSi10/AlSi7, mean spatter velocity increases linearly with laser intensity, and over half of detected spatters have radii <30 µm at 4.24 MW/cm²; particles with radii >70–80 µm occur in all tested conditions (chebil2021studyofspatter pages 7-10, chebil2021studyofspatter pages 4-7). AlSi7 produces ~30% more spatters than AlSi10 at 5.66 MW/cm² (chebil2021studyofspatter pages 4-7).

**Solid vs liquid spatter.** In Al-Fe-Zr, solid spatter constitutes >82% of all ejecta; jet spatter is ~2% (guo2024correlativespatterand pages 4-7). The wide, shallow vapour depression zone in conduction-mode Al melting promotes backward liquid droplets that can exceed 90% of the liquid fraction (guo2024correlativespatterand pages 7-9).

**Comparison with steels and Ti-6Al-4V.** Approximately 90% of melt-pool ejections in LPBF generally fall within the 15–45 µm powder-size range (williams2022maximisingtheutilisation pages 89-93). No direct quantitative Al-vs-steel spatter-count comparison (counts per mm of track) was retrieved. Aluminium's lower absorptivity in conduction mode means higher laser powers are needed to reach keyholing, potentially producing fewer vapour-driven ejecta per watt but more vigorous ejection once keyhole mode is established. The higher thermal conductivity of Al produces wider, shallower melt pools with broader vapour depressions, promoting backward spatter trajectories relative to the more vertical ejection seen in steel and Ti keyholes.

**Spatter travel distance.** At the measured velocity of 3.39 m/s, a spatter particle would travel ~34 mm in 10 ms neglecting drag (guo2024correlativespatterand pages 10-12). Argon drag significantly shortens travel for fine particles (<30 µm), but particles >80 µm can travel tens of millimetres. Cross-flow sweeps vertically ejected spatters toward the filter/outlet and away from subsequent scan tracks (chebil2021studyofspatter pages 7-10, bitharas2022theinterplaybetween pages 6-8).

---

### 5. Monitoring System Requirements

**Melt-pool transit time.** For a ~96 µm beam at 0.4–1.1 m/s, the beam transit time is ~240–87 µs. Resolving multiple samples per transit requires frame rates of ≥10–20 kHz for coaxial imaging.

**Solidification time.** For a representative melt pool length of 0.2–0.4 mm at 0.4–1.1 m/s, the solidification dwell time is ~0.18–1.0 ms.

**Keyhole fluctuation spectrum.** Measured at 2.5–10 kHz (huang2022keyholefluctuationand pages 1-2, huang2022keyholefluctuationand pages 7-8). Capturing this requires Nyquist sampling at ≥20 kHz; in practice, 50–100 kHz photodiode bandwidth or 50–100 kfps camera frame rate is needed to fully resolve the keyhole oscillation spectrum.

**Spatter speeds.** Measured up to ~3.4 m/s for laser-accelerated Al particles (guo2024correlativespatterand pages 10-12); limiting motion blur to ~10 µm requires exposures ≤2.9 µs.

**Published monitoring configurations.** For LPBF process monitoring, demonstrated approaches include: coaxial high-speed cameras at ≥10 kHz with 1070 nm notch-filtered thermal emission imaging; off-axis schlieren at similar frame rates; synchrotron X-ray imaging at up to 1 MHz for keyhole dynamics; and acoustic emission with ~100 µs time resolution for regime identification. Melt-pool thermal monitoring using NIR cameras at ~1 kHz frame rate has been demonstrated for Ti-6Al-4V and steels (bitharas2022theinterplaybetween pages 3-4, bitharas2022theinterplaybetween pages 1-3). **Al-specific LPBF monitoring publications are scarce** — most published monitoring work uses steels, Inconel, or Ti-6Al-4V, and the lower thermal emission from cooler Al conduction-mode melt pools (due to lower absorptivity) makes thermal imaging more challenging.

---

### Key Differences: Aluminium vs Steels and Ti-6Al-4V

- **Absorptivity**: Al flat-surface absorptivity at 1.07 µm is ~5× lower than steel (~0.05 vs ~0.3), requiring substantially higher laser power to reach keyholing. The powder-bed enhancement factor (~4.7×) partially compensates (king2015laserpowderbed pages 8-12).
- **Thermal conductivity**: Al's ~150 W/(m·K) versus steel's ~15–25 W/(m·K) produces wider, shallower melt pools and faster lateral heat dissipation.
- **Element evaporation**: Mg and Zn losses from Al alloys (up to 57% Mg, up to 30% Zn) far exceed typical compositional changes in steels or Ti-6Al-4V during LPBF (li2024additivemanufacturingof pages 42-46).
- **Spatter**: Al alloys produce predominantly backward spatter from wide vapour depressions, versus more vertical ejection in Ti-6Al-4V deep keyholes (guo2024correlativespatterand pages 7-9).
- **Plasma formation**: Al LPBF at ~1 µm wavelength does not form a significant plasma, unlike CO₂-laser welding of metals.

### Identified Data Gaps for Aluminium LPBF

1. Melt-pool length measurements at LPBF-relevant conditions.
2. Direct G and R measurements or high-fidelity simulations with reported values.
3. Marangoni surface-flow velocity measurements.
4. Condensate/fume characterisation (particle size, composition, mass generation rate) for Al alloys.
5. Quantitative laser beam attenuation by plume and condensate.
6. Cover-slide/window transmission loss per build hour.
7. Spectral emission line identification in the 600–1000 nm and 1.3–1.7 µm bands for Al LPBF (as opposed to DED).
8. Spatter counts per mm of track with direct Al-vs-steel comparison.
9. Al-specific in-situ monitoring demonstrations with reported frame rates and bandwidths.

References

1. (patel2021meltingmodesin pages 243-247): Sagar Patel and Mihaela Vlasea. Melting modes in laser powder bed fusion. SSRN Electronic Journal, Jan 2019. URL: https://doi.org/10.2139/ssrn.3490412, doi:10.2139/ssrn.3490412. This article has 3 citations.

2. (patel2021meltingmodesin pages 96-100): Sagar Patel and Mihaela Vlasea. Melting modes in laser powder bed fusion. SSRN Electronic Journal, Jan 2019. URL: https://doi.org/10.2139/ssrn.3490412, doi:10.2139/ssrn.3490412. This article has 3 citations.

3. (huang2022keyholefluctuationand pages 2-4): Yuze Huang, Tristan Fleming, Samuel Clark, Sebastian Marussi, Fezzaa Kamel, Jeyan Thiyagalingam, Chu Lun Alex Leung, and Peter Lee. Keyhole fluctuation and pore formation mechanisms during laser powder bed fusion additive manufacturing. Nature Communications, Aug 2021. URL: https://doi.org/10.1038/s41467-022-28694-x, doi:10.1038/s41467-022-28694-x. This article has 615 citations and is from a highest quality peer-reviewed journal.

4. (king2015laserpowderbed pages 8-12): W. E. King, A. T. Anderson, R. M. Ferencz, N. E. Hodge, C. Kamath, S. A. Khairallah, and A. M. Rubenchik. Laser powder bed fusion additive manufacturing of metals; physics, computational, and materials challenges. Applied physics reviews, 2:041304, Dec 2015. URL: https://doi.org/10.1063/1.4937809, doi:10.1063/1.4937809. This article has 1897 citations and is from a domain leading peer-reviewed journal.

5. (patel2021meltingmodesin pages 63-66): Sagar Patel and Mihaela Vlasea. Melting modes in laser powder bed fusion. SSRN Electronic Journal, Jan 2019. URL: https://doi.org/10.2139/ssrn.3490412, doi:10.2139/ssrn.3490412. This article has 3 citations.

6. (trapp2017insituabsorptivity pages 4-6): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

7. (trapp2017insituabsorptivity pages 6-7): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

8. (cauwenbergh2021unravellingthemultiscale pages 5-7): P. Van Cauwenbergh, V. Samaee, L. Thijs, J. Nejezchlebová, P. Sedlák, A. Iveković, D. Schryvers, B. Van Hooreweder, and K. Vanmeensel. Unravelling the multi-scale structure–property relationship of laser powder bed fusion processed and heat-treated alsi10mg. Scientific Reports, Mar 2021. URL: https://doi.org/10.1038/s41598-021-85047-2, doi:10.1038/s41598-021-85047-2. This article has 257 citations and is from a peer-reviewed journal.

9. (samantaray2019modelingofthermal pages 7-10): Mihir Samantaray, Seshadev Sahoo, and Dhirendranath Thatoi. Modeling of thermal and solidification behavior during laser additive manufacturing of alsi10mg alloy powders and its experimental validation. Journal of Laser Applications, Aug 2019. URL: https://doi.org/10.2351/1.5104318, doi:10.2351/1.5104318. This article has 31 citations and is from a peer-reviewed journal.

10. (leis2022tuningthehardness pages 6-8): Artur Leis, David Traunecker, Rudolf Weber, and Thomas Graf. Tuning the hardness of produced parts by adjusting the cooling rate during laser-based powder bed fusion of alsi10mg by adapting the process parameters. Metals, 12:2000, Nov 2022. URL: https://doi.org/10.3390/met12122000, doi:10.3390/met12122000. This article has 12 citations.

11. (leis2022tuningthehardness pages 4-6): Artur Leis, David Traunecker, Rudolf Weber, and Thomas Graf. Tuning the hardness of produced parts by adjusting the cooling rate during laser-based powder bed fusion of alsi10mg by adapting the process parameters. Metals, 12:2000, Nov 2022. URL: https://doi.org/10.3390/met12122000, doi:10.3390/met12122000. This article has 12 citations.

12. (leis2022tuningthehardness pages 2-4): Artur Leis, David Traunecker, Rudolf Weber, and Thomas Graf. Tuning the hardness of produced parts by adjusting the cooling rate during laser-based powder bed fusion of alsi10mg by adapting the process parameters. Metals, 12:2000, Nov 2022. URL: https://doi.org/10.3390/met12122000, doi:10.3390/met12122000. This article has 12 citations.

13. (sonawane2021structuralaluminumalloy pages 142-145): Akash Arun Sonawane. Structural aluminum alloy processed by laser powder bed fusion (l-pbf) : a fundamental understanding of cracking. Unknown journal, 2021. URL: https://doi.org/10.70675/b76c3001z60daz4747zb50bzf30f70232dcd, doi:10.70675/b76c3001z60daz4747zb50bzf30f70232dcd.

14. (mayi2020laserinducedplumeinvestigated pages 7-9): Y. Mayi, M. Dal, P. Peyre, M. Bellet, C. Metton, C. Moriconi, and R. Fabbro. Laser-induced plume investigated by finite element modelling and scaling of particle entrainment in laser powder bed fusion. Journal of Physics D: Applied Physics, 53:075306, Dec 2019. URL: https://doi.org/10.1088/1361-6463/ab5900, doi:10.1088/1361-6463/ab5900. This article has 78 citations and is from a peer-reviewed journal.

15. (guo2024correlativespatterand pages 7-9): Da Guo, Rubén Lambert-Garcia, Samy Hocine, Xianqiang Fan, Henry Greenhalgh, Ravi Shahani, Marta Majkut, Alexander Rack, Peter D Lee, and Chu Lun Alex Leung. Correlative spatter and vapour depression dynamics during laser powder bed fusion of an al-fe-zr alloy. International Journal of Extreme Manufacturing, 6:055601, Jun 2024. URL: https://doi.org/10.1088/2631-7990/ad4e1d, doi:10.1088/2631-7990/ad4e1d. This article has 65 citations.

16. (huang2022keyholefluctuationand pages 1-2): Yuze Huang, Tristan Fleming, Samuel Clark, Sebastian Marussi, Fezzaa Kamel, Jeyan Thiyagalingam, Chu Lun Alex Leung, and Peter Lee. Keyhole fluctuation and pore formation mechanisms during laser powder bed fusion additive manufacturing. Nature Communications, Aug 2021. URL: https://doi.org/10.1038/s41467-022-28694-x, doi:10.1038/s41467-022-28694-x. This article has 615 citations and is from a highest quality peer-reviewed journal.

17. (huang2022keyholefluctuationand pages 7-8): Yuze Huang, Tristan Fleming, Samuel Clark, Sebastian Marussi, Fezzaa Kamel, Jeyan Thiyagalingam, Chu Lun Alex Leung, and Peter Lee. Keyhole fluctuation and pore formation mechanisms during laser powder bed fusion additive manufacturing. Nature Communications, Aug 2021. URL: https://doi.org/10.1038/s41467-022-28694-x, doi:10.1038/s41467-022-28694-x. This article has 615 citations and is from a highest quality peer-reviewed journal.

18. (guo2023understandingkeyholeinducedporosities pages 24-28): Liping Guo, Hongze Wang, Hanjie Liu, Yuze Huang, Qianglong Wei, Chu Lun Alex Leung, Yi Wu, and Haowei Wang. Understanding keyhole induced-porosities in laser powder bed fusion of aluminum and elimination strategy. International Journal of Machine Tools and Manufacture, 184:103977, Jan 2023. URL: https://doi.org/10.1016/j.ijmachtools.2022.103977, doi:10.1016/j.ijmachtools.2022.103977. This article has 180 citations and is from a highest quality peer-reviewed journal.

19. (shi2024areviewof pages 8-10): Guanglei Shi, Runze Zhang, Yachao Cao, and Guang Yang. A review of the vaporization behavior of some metal elements in the lpbf process. Micromachines, 15:846, Jun 2024. URL: https://doi.org/10.3390/mi15070846, doi:10.3390/mi15070846. This article has 39 citations.

20. (bitharas2022theinterplaybetween pages 6-8): I. Bitharas, N. Parab, C. Zhao, T. Sun, A. D. Rollett, and A. J. Moore. The interplay between vapour, liquid, and solid phases in laser powder bed fusion. Nature Communications, May 2022. URL: https://doi.org/10.1038/s41467-022-30667-z, doi:10.1038/s41467-022-30667-z. This article has 172 citations and is from a highest quality peer-reviewed journal.

21. (shi2024areviewof pages 17-21): Guanglei Shi, Runze Zhang, Yachao Cao, and Guang Yang. A review of the vaporization behavior of some metal elements in the lpbf process. Micromachines, 15:846, Jun 2024. URL: https://doi.org/10.3390/mi15070846, doi:10.3390/mi15070846. This article has 39 citations.

22. (li2024additivemanufacturingof pages 42-46): Ying-Jie Li. Additive manufacturing of 6061 and 7075 aluminium alloy with selective laser melting. Unknown journal, 2024. URL: https://doi.org/10.70675/5f083431z1407z40f1z83bfz19a675dc42f6, doi:10.70675/5f083431z1407z40f1z83bfz19a675dc42f6.

23. (noskov2020characterizationofultrafine pages 4-7): Aleksey Noskov, Torunn K. Ervik, Ilya Tsivilskiy, Albert Gilmutdinov, and Yngvar Thomassen. Characterization of ultrafine particles emitted during laser-based additive manufacturing of metal parts. Scientific Reports, Dec 2020. URL: https://doi.org/10.1038/s41598-020-78073-z, doi:10.1038/s41598-020-78073-z. This article has 39 citations and is from a peer-reviewed journal.

24. (noskov2020characterizationofultrafine pages 1-2): Aleksey Noskov, Torunn K. Ervik, Ilya Tsivilskiy, Albert Gilmutdinov, and Yngvar Thomassen. Characterization of ultrafine particles emitted during laser-based additive manufacturing of metal parts. Scientific Reports, Dec 2020. URL: https://doi.org/10.1038/s41598-020-78073-z, doi:10.1038/s41598-020-78073-z. This article has 39 citations and is from a peer-reviewed journal.

25. (noskov2022amicroscopystudy pages 1-2): Aleksey Noskov, Mikhael El-Khoury, Sergey Drobyshev, Evgeny Kuchaev, Fatih Yanbaev, Olga Zhigalina, Dmitriy Khmelenin, and Albert Gilmutdinov. A microscopy study of nanoparticles emitted during laser additive manufacturing with stainless steel powder. Materials Letters: X, 14:100139, Jun 2022. URL: https://doi.org/10.1016/j.mlblux.2022.100139, doi:10.1016/j.mlblux.2022.100139. This article has 6 citations.

26. (noskov2020characterizationofultrafine pages 3-4): Aleksey Noskov, Torunn K. Ervik, Ilya Tsivilskiy, Albert Gilmutdinov, and Yngvar Thomassen. Characterization of ultrafine particles emitted during laser-based additive manufacturing of metal parts. Scientific Reports, Dec 2020. URL: https://doi.org/10.1038/s41598-020-78073-z, doi:10.1038/s41598-020-78073-z. This article has 39 citations and is from a peer-reviewed journal.

27. (chebil2021studyofspatter pages 7-10): Gwenaëlle Chebil, Pierre Lapouge, Yves Renollet, Cécile Davoine, Marc Thomas, Véronique Favier, and Matthieu Schneider. Study of spatter ejections during laser-powder bed fusion process for aluminum alloys. Journal of Laser Applications, Nov 2021. URL: https://doi.org/10.2351/7.0000493, doi:10.2351/7.0000493. This article has 9 citations and is from a peer-reviewed journal.

28. (chebil2021studyofspatter pages 4-7): Gwenaëlle Chebil, Pierre Lapouge, Yves Renollet, Cécile Davoine, Marc Thomas, Véronique Favier, and Matthieu Schneider. Study of spatter ejections during laser-powder bed fusion process for aluminum alloys. Journal of Laser Applications, Nov 2021. URL: https://doi.org/10.2351/7.0000493, doi:10.2351/7.0000493. This article has 9 citations and is from a peer-reviewed journal.

29. (guo2024correlativespatterand pages 4-7): Da Guo, Rubén Lambert-Garcia, Samy Hocine, Xianqiang Fan, Henry Greenhalgh, Ravi Shahani, Marta Majkut, Alexander Rack, Peter D Lee, and Chu Lun Alex Leung. Correlative spatter and vapour depression dynamics during laser powder bed fusion of an al-fe-zr alloy. International Journal of Extreme Manufacturing, 6:055601, Jun 2024. URL: https://doi.org/10.1088/2631-7990/ad4e1d, doi:10.1088/2631-7990/ad4e1d. This article has 65 citations.

30. (guo2024correlativespatterand pages 10-12): Da Guo, Rubén Lambert-Garcia, Samy Hocine, Xianqiang Fan, Henry Greenhalgh, Ravi Shahani, Marta Majkut, Alexander Rack, Peter D Lee, and Chu Lun Alex Leung. Correlative spatter and vapour depression dynamics during laser powder bed fusion of an al-fe-zr alloy. International Journal of Extreme Manufacturing, 6:055601, Jun 2024. URL: https://doi.org/10.1088/2631-7990/ad4e1d, doi:10.1088/2631-7990/ad4e1d. This article has 65 citations.

31. (guo2023understandingkeyholeinducedporosities pages 18-24): Liping Guo, Hongze Wang, Hanjie Liu, Yuze Huang, Qianglong Wei, Chu Lun Alex Leung, Yi Wu, and Haowei Wang. Understanding keyhole induced-porosities in laser powder bed fusion of aluminum and elimination strategy. International Journal of Machine Tools and Manufacture, 184:103977, Jan 2023. URL: https://doi.org/10.1016/j.ijmachtools.2022.103977, doi:10.1016/j.ijmachtools.2022.103977. This article has 180 citations and is from a highest quality peer-reviewed journal.

32. (guo2023understandingkeyholeinducedporosities pages 4-8): Liping Guo, Hongze Wang, Hanjie Liu, Yuze Huang, Qianglong Wei, Chu Lun Alex Leung, Yi Wu, and Haowei Wang. Understanding keyhole induced-porosities in laser powder bed fusion of aluminum and elimination strategy. International Journal of Machine Tools and Manufacture, 184:103977, Jan 2023. URL: https://doi.org/10.1016/j.ijmachtools.2022.103977, doi:10.1016/j.ijmachtools.2022.103977. This article has 180 citations and is from a highest quality peer-reviewed journal.

33. (noskov2020characterizationofultrafine pages 10-11): Aleksey Noskov, Torunn K. Ervik, Ilya Tsivilskiy, Albert Gilmutdinov, and Yngvar Thomassen. Characterization of ultrafine particles emitted during laser-based additive manufacturing of metal parts. Scientific Reports, Dec 2020. URL: https://doi.org/10.1038/s41598-020-78073-z, doi:10.1038/s41598-020-78073-z. This article has 39 citations and is from a peer-reviewed journal.

34. (noskov2020characterizationofultrafine pages 7-9): Aleksey Noskov, Torunn K. Ervik, Ilya Tsivilskiy, Albert Gilmutdinov, and Yngvar Thomassen. Characterization of ultrafine particles emitted during laser-based additive manufacturing of metal parts. Scientific Reports, Dec 2020. URL: https://doi.org/10.1038/s41598-020-78073-z, doi:10.1038/s41598-020-78073-z. This article has 39 citations and is from a peer-reviewed journal.

35. (williams2022maximisingtheutilisation pages 89-93): Robert Williams. Maximising the utilisation of ti-6al-4v metal powder in the selective laser melting process. Text, Jan 2022. URL: https://doi.org/10.17638/03157594, doi:10.17638/03157594. This article has 0 citations and is from a peer-reviewed journal.

36. (bitharas2022theinterplaybetween pages 3-4): I. Bitharas, N. Parab, C. Zhao, T. Sun, A. D. Rollett, and A. J. Moore. The interplay between vapour, liquid, and solid phases in laser powder bed fusion. Nature Communications, May 2022. URL: https://doi.org/10.1038/s41467-022-30667-z, doi:10.1038/s41467-022-30667-z. This article has 172 citations and is from a highest quality peer-reviewed journal.

37. (bitharas2022theinterplaybetween pages 1-3): I. Bitharas, N. Parab, C. Zhao, T. Sun, A. D. Rollett, and A. J. Moore. The interplay between vapour, liquid, and solid phases in laser powder bed fusion. Nature Communications, May 2022. URL: https://doi.org/10.1038/s41467-022-30667-z, doi:10.1038/s41467-022-30667-z. This article has 172 citations and is from a highest quality peer-reviewed journal.
