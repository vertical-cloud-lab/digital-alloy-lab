# Ultrasonic Atomization of Nine Aluminium Alloy Classes on the AMAZEMET rePOWDER: Literature-Based Process Guidance

## 1. Droplet Size Prediction and Measured Particle Size Distributions

**Lang's capillary-wave equation.** The classical relationship derived by Lang relates the median droplet diameter *d* to the capillary wavelength: *d* = 0.34·λ, where the capillary wavelength is λ = (8πσ/(ρf²))^(1/3), with σ = surface tension (N/m), ρ = liquid density (kg/m³), and f = ultrasonic frequency (Hz) (presz2024ultrasonicatomizationas pages 6-7, scientific2023comparisonofultrasonic pages 4-5). The constant 0.34 is an empirical fit for moderate feed rates; at higher throughputs or high amplitude, a correction function involving Weber, Ohnesorge, and ultrasonic-intensity numbers may apply, though for typical rePOWDER operation it can be approximated as unity (scientific2023comparisonofultrasonic pages 4-5). Doubling frequency reduces predicted D50 by approximately 40% (scientific2023comparisonofultrasonic pages 4-5). D50 scales as σ^(1/3), meaning alloys that lower surface tension (Mg, Si, Zn additions) are expected to shift the PSD somewhat finer.

**Calculated D50 for pure Al at 40 kHz.** Using σ ≈ 0.87 N/m, ρ ≈ 2370 kg/m³, the Lang equation predicts a capillary wavelength of ~135 μm and D50 ≈ 46 μm (presz2024ultrasonicatomizationas pages 6-7). At 20 kHz this rises to ~72 μm, at 60 kHz it falls to ~35 μm. For alloys with 4–5 wt% Mg (σ ≈ 0.80 N/m), the predicted D50 at 40 kHz drops by ~3%, a modest effect. High-Zn alloys (σ ≈ 0.75–0.80 N/m) show a similar ~5% reduction.

**Measured PSDs on rePOWDER and ATO machines.** Literature data are summarized below:

| Alloy | Machine / frequency | Amplitude / power | Melt T (°C) | D10 (µm) | D50 (µm) | D90 (µm) | Measurement basis | Reference / DOI |
|---|---|---:|---:|---:|---:|---:|---|---|
| Pure Al | Carbon-fibre plate, 60 kHz | 60% power; 8.55 µm amplitude | 800 | 12.8 | 22.4 | 34.6 | Count-based measured PSD | Priyadarshi et al. (2024), [10.1016/j.addma.2024.104033](https://doi.org/10.1016/j.addma.2024.104033) (priyadarshi2024newinsightsinto pages 3-5, priyadarshi2024newinsightsinto pages 16-19) |
| Pure Al | Carbon-fibre plate, 60 kHz | 60% power; 8.55 µm amplitude | 800 | 18.2 | 31.8 | 59.1 | Volume-based measured PSD | Priyadarshi et al. (2024), [10.1016/j.addma.2024.104033](https://doi.org/10.1016/j.addma.2024.104033) (priyadarshi2024newinsightsinto pages 3-5, priyadarshi2024newinsightsinto pages 16-19) |
| Pure Al | Carbon-fibre plate, 60 kHz | 100% power; 9.9 µm amplitude | 800 | 15.2 | 24.5 | 42.7 | Count-based measured PSD | Priyadarshi et al. (2024), [10.1016/j.addma.2024.104033](https://doi.org/10.1016/j.addma.2024.104033) (priyadarshi2024newinsightsinto pages 3-5, priyadarshi2024newinsightsinto pages 16-19) |
| Pure Al | Carbon-fibre plate, 60 kHz | 100% power; 9.9 µm amplitude | 800 | 21.3 | 41.7 | 82.8 | Volume-based measured PSD | Priyadarshi et al. (2024), [10.1016/j.addma.2024.104033](https://doi.org/10.1016/j.addma.2024.104033) (priyadarshi2024newinsightsinto pages 3-5, priyadarshi2024newinsightsinto pages 16-19) |
| Al–10Cu | AMAZEMET rePOWDER induction system, 40 kHz | Not reported | 1100 | 36 | 65 | 78 | Measured PSD; article also states 90% below 70 µm, which conflicts with the tabulated D90 | Ukabhai et al. (2025), [10.1051/matecconf/202541703001](https://doi.org/10.1051/matecconf/202541703001) (ukabhai2025investigationofalcu pages 3-7) |
| AlSi12 | ATO Lab+ US35, 35 kHz | 80% amplitude; 140 A | Not reported | NR | NR | NR | Measured and sieved; approximately 75% of powder was below 63 µm, but numerical percentiles were unavailable in accessible text | Yankin et al. (2025), [10.1038/s41598-025-06086-7](https://doi.org/10.1038/s41598-025-06086-7) (yankin2025effectofultrasonic pages 2-3, yankin2025effectofultrasonic pages 12-15) |
| AlSi10Mg | Gas atomizer; reference rather than ultrasonic atomization | Not applicable | Not reported | 18.4 | 45.0 | 115 | Volume-based measured PSD of as-atomized powder; included as a gas-atomized benchmark | Stella (2026), thesis; no DOI reported (stella2026processabilityofrecycled pages 55-60, stella2026processabilityofrecycled pages 60-65) |
| Ti–6Al–4V | Ultrasonic cold-crucible/sonotrode atomization, 20 kHz | Not reported | Not reported | NR | NR | NR | Reported cut yield: approximately 80–90% in 20–63 µm; non-Al benchmark | Korzhyk et al. (2025), [10.37434/tpwj2025.10.01](https://doi.org/10.37434/tpwj2025.10.01) (korzhyk2025prospectsofultrasound pages 2-4) |
| Pure Al | Lang capillary-wave estimate, 40 kHz | Small-amplitude idealization | Property-dependent | — | ≈42–50 | — | Calculated estimate using σ≈0.87 N/m and ρ≈2370 kg/m³; not a measured PSD and sensitive to the selected Lang coefficient/formulation | Lang-type relation summarized by Presz et al. (2024), [10.3390/ma17246109](https://doi.org/10.3390/ma17246109) (presz2024ultrasonicatomizationas pages 6-7, scientific2023comparisonofultrasonic pages 4-5) |


*Table: Measured particle-size distributions and cut yields for ultrasonic atomization are separated by count- and volume-based measurement, with gas-atomized and theoretical rows clearly identified as benchmarks rather than equivalent measurements.*

Key observations: (i) At 60 kHz on a carbon-fibre plate, pure Al produced volume-based Dv50 = 31.8 μm at 60% power and 41.7 μm at 100% power; the PSD span (D90–D10) widened from 21.8 to 67.6 μm with increasing amplitude (priyadarshi2024newinsightsinto pages 16-19, priyadarshi2024newinsightsinto pages 13-15). (ii) On the rePOWDER at 40 kHz (induction system), Al-10Cu gave a D50 of 65 μm with 90% below 70 μm (ukabhai2025investigationofalcu pages 3-7), which is coarser than the Lang prediction—possibly reflecting higher melt feed rate or a 1100°C melt temperature that may have promoted plate wetting and coarser films. (iii) AlSi12 on the ATO Lab+ at 35 kHz with 80% amplitude and 140 A yielded approximately 75% of powder below 63 μm (yankin2025effectofultrasonic pages 2-3). (iv) For AMC (Al-matrix composite) on the rePOWDER at 40 kHz with induction, the 40 kHz transducer produced nearly twice the yield of a 60 kHz transducer, attributed to higher achievable amplitude at the lower frequency (jedynak2024processabilityofaluminummatrix pages 3-6).

**In-cut yield estimates for your 40 kHz machine.** Based on the above data, at 40 kHz with 90–100% amplitude and 0.17–0.20 bar overpressure, Al alloys should produce a volume D50 of approximately 42–55 μm. The fraction in the 20–63 μm sieve cut is estimated at 50–65%, and in 15–45 μm at 25–40%. In the coarser 45–106 μm cut, 30–45% is expected. These are engineering estimates; no publication reports measured sieve fractions specifically for Al alloys on the rePOWDER at 40 kHz.

## 2. Superheat Requirements

**Recommended practice.** Pure Al was atomized at 800°C (superheat ~140 K above the 660°C liquidus) with an overpressure of 200 mbar, 250 g charges, and a 0.5 mm nozzle, with yield consistently exceeding 80% (priyadarshi2024newinsightsinto pages 3-5). Al-10Cu on the rePOWDER induction system used 1100°C (superheat ~450 K above the ~548°C eutectic) with 100 g of feed pellets (ukabhai2025investigationofalcu pages 3-7). In general, superheats of 100–200 K above liquidus are appropriate for simple Al–Si and Al–Cu alloys, while alloys requiring dissolution of refractory peritectic phases (Zr, Ti, Cr, Mn, Sc, Er) need substantially higher temperatures (see Section 3).

**Too-low superheat** causes the melt to freeze in the nozzle (nozzle clogging), to solidify on the plate before atomization (producing flakes and irregular "splats"), and in extreme cases to prevent atomization entirely (soong2023atomizationofmetal pages 8-8). **Too-high superheat** intensifies volatile-element evaporation (Mg, Zn, Mn), can promote excessive wetting and erosion of the sonotrode plate, and may enlarge the melt film thickness—leading to coarser particles and more satellites (soong2023atomizationofmetal pages 8-8, bartl2022influenceofsurface pages 8-10).

## 3. Liquidus Temperatures and Dissolution of Refractory Elements

**Al–Zr system.** The binary Al–Zr peritectic (or possibly eutectic) reaction occurs at approximately 660°C with a solid-solution solubility of only ~0.08 wt% Zr under equilibrium conditions (khvan2018newinsightsinto pages 1-6). The Al₃Zr liquidus rises steeply: at 0.3 wt% Zr, the liquidus is approximately 700–720°C; at 0.6 wt% Zr, approximately 760–790°C; at 1.0 wt% Zr, approximately 830–870°C; at 1.5 wt% Zr, approximately 900–940°C (estimated from the assessed Al–Zr phase diagram) (khvan2018newinsightsinto pages 1-6). To fully dissolve an Al-10Zr master alloy in a small unstirred melt, temperatures well above 900°C and vigorous stirring are needed; at 920°C the master alloy may still require 10–20 minutes to dissolve coarse primary Al₃Zr particles.

**Al–Ti:** 0.5 wt% Ti raises the liquidus to ~750°C; 1 wt% Ti to ~830°C. Al-10Ti master alloys contain large Al₃Ti plates that dissolve slowly at ≤800°C.

**Al–Mn:** 4–5 wt% Mn has a liquidus around 710–730°C (binary), but Mn-rich intermetallics (Al₆Mn) can be sluggish to dissolve; 850–900°C with hold times of 10–20 min are typical.

**Al–Cr:** 0.8–2 wt% Cr raises the liquidus to ~740–850°C. Combined Al–Mn–Cr melts risk forming sludge (Al₁₅(Mn,Cr)₃Si₂-type) if cooled below ~700°C even briefly; hold at ≥950°C is advisable for 5Mn-0.8Cr type alloys.

**Al–Sc:** 0.7 wt% Sc has an Al₃Sc peritectic liquidus near 660°C with limited solid solubility (~0.38 wt%). Dissolution of Al-2Sc master alloy proceeds in minutes at 800°C due to the relatively low Sc level.

**Al–Er:** 0.5–1.0 wt% Er forms Al₃Er with a peritectic near 655°C. Er dissolves more readily than Zr at comparable temperatures, but Er is highly prone to oxide/dross formation.

**Industrial gas atomization practice.** Scalmalloy-type (Al-4.5Mg-0.7Sc-0.3Zr) powders are commercially gas-atomized at melt temperatures typically in the range 850–1050°C, often using EIGA (electrode induction melting gas atomization) or VIGA (vacuum induction gas atomization). Published data for melt hold temperatures specific to the gas atomizers used for Scalmalloy are not openly available, but patent literature and conference reports indicate 900–1000°C for the Sc/Zr dissolution step.

**Implications for small rePOWDER charges.** The 170–350 g induction-melted charges in the rePOWDER crucible reach temperature quickly but have no mechanical stirring (only electromagnetic stirring from the induction coil). For alloys with ≥0.6 wt% Zr, hold times of 10–20 minutes at 930–980°C are recommended to ensure dissolution. For 1.2 wt% Zr, consider pre-melting the master alloy into the base charge via arc melting before induction re-melting for atomization. No published data quantifying dissolution kinetics of Al-10Zr, Al-20Mn, Al-20Cr, or Cr powder in a rePOWDER-sized induction melt were found.

## 4. Evaporation and Composition Fidelity

**Magnesium.** Mg is the most volatile common alloying element in Al. Electromagnetic levitation measurements on Scalmalloy showed rapid Mg evaporation during a 45-second cycle at 540 K superheat; Mn loss was 7.9% total mass in the same cycle. At 970 K superheat (as for Zicromal), Mn-related total mass loss exceeded 70% (bartl2022influenceofsurface pages 8-10). Under 750 mbar argon, the shielding factor reduces evaporation by approximately 10³ relative to vacuum (bartl2022influenceofsurface pages 8-10). For the rePOWDER operating at approximately 1 bar argon, Mg losses during a typical 2–5 minute melt-and-pour cycle at 850–920°C are estimated at 1–5% relative, depending on temperature, hold time, and melt surface area. Overcharging Mg by 10–15% is recommended as a starting point for alloys containing ≥3 wt% Mg; refine the overcharge based on ICP-OES analysis of the first atomized batch.

**Zinc.** Zn has very high vapour pressure. Under vacuum (10 Pa), zinc removal from Al–6.3Zn reached 96% at 1103 K (830°C) in a crucible induction furnace. Under 1000 Pa, removal was only 6% at 953 K (smalcerz2021kineticsofzinc pages 4-7). At atmospheric Ar pressure (~10⁵ Pa), direct Zn evaporation from the bulk melt is greatly suppressed; however, the creation of fine droplets during atomization exposes enormous surface area, and Zn loss from finer fractions can be enhanced. Overcharging Zn by 15–25% is recommended for 7xxx-type alloys; this must be calibrated experimentally (smalcerz2021kineticsofzinc pages 4-7, smalcerz2021kineticsofzinc pages 2-4).

**Manganese.** Mn has moderate volatility. Under argon at atmospheric pressure and typical atomization superheats (200–300 K), Mn loss is expected to be <2% and may not require systematic overcharging, though high-Mn alloys (5 wt%) at high temperatures (>950°C) warrant monitoring (bartl2022influenceofsurface pages 8-10).

**Sc, Er, Zr, Ti, Cr:** These elements have negligible vapour pressures at Al atomization temperatures. Losses occur almost exclusively through oxide/dross formation: Sc, Er, and Zr are strong oxide formers and can be preferentially scavenged into dross if oxygen levels in the chamber are >50 ppm or if moisture is present. Recovery for Sc and Zr is typically >95% under good inert-gas practice, while Er may show slightly lower recovery due to its strong affinity for oxygen. No published rePOWDER-specific recovery data were found (bartl2022influenceofsurface pages 8-10).

**During LPBF.** Mg loss during LPBF has been documented for Scalmalloy: surface tension was 3–8% lower for Scalmalloy than for Cr-based alloys, and Mg evaporation contributes to spatter and fume during printing (bartl2022influenceofsurface pages 8-10). For 7xxx alloys, Zn evaporation during LPBF is well-known and can reach several wt% in thin-wall geometries; this is a secondary loss on top of atomization losses.

## 5. Crucible, Nozzle, and Sonotrode Plate Compatibility

**Mo sonotrode plate.** Molybdenum exhibits strong anti-wetting behaviour against molten Al and Al–5Mg alloys. Molecular dynamics simulations predicted an interfacial energy of ~203 mJ/m², indicative of weak van der Waals interaction. In a 96-hour immersion test at 850°C in Al–5%Mg, OES detected negligible Mo dissolved into the bulk melt (from 0.005% to 0.012%). The Mo block did suffer ~20% mass loss, but this was attributed to intergranular corrosion and grain-boundary chipping rather than dissolution (gitzhofer2021provenantiwettingproperties pages 18-19, gitzhofer2021provenantiwettingproperties pages 19-21, gitzhofer2021provenantiwettingproperties pages 13-15). For the short contact times in rePOWDER atomization (seconds per pour), Mo pickup into the powder should be negligible. The anti-wetting behaviour means that the melt film required for atomization must be maintained by continued melt flow; Mg and Si additions improve wetting of most surfaces and may help sustain the film.

**Graphite crucible and nozzle.** Graphite is widely used for Al melts. Priyadarshi et al. used a graphite crucible for pure Al at 800°C with no reported C pickup (priyadarshi2024newinsightsinto pages 3-5). However, for alloys containing reactive elements (Ce, Er, Sc, Mg ≥5%), Al₃C₄ formation is thermodynamically possible above ~750°C and becomes kinetically significant at extended hold times. BN-coated graphite is recommended for these alloys to provide a diffusion barrier. For Al–Ce alloys, cerium can reduce Al₂O₃ and BN and react with graphite; alumina or yttria crucibles should be validated (eskin2017ultrasonicprocessingof pages 7-10).

**Nb sonotrode materials.** For long-term ultrasonic processing of Al melts, Nb and its alloys are recommended over Fe-, Ti-, and Mo-based sonotrode materials due to superior erosion resistance under cavitation conditions. Ti dissolves to 0.02% after just 15–30 seconds at 730°C under cavitation, potentially contaminating the melt and altering grain structure (eskin2017ultrasonicprocessingof pages 7-10). For the rePOWDER's Mo plate (which does not immerse in the melt but rather receives droplets on its surface), this concern is minimal.

## 6. Powder Quality

**Sphericity and satellites.** UA powders are consistently reported as highly spherical and free of satellite particles. For Mo–Si–Ti alloy, >90% of particles had an aspect ratio below 1.2 (hinrichs2021flexiblepowderproduction pages 4-7). For Ti-6Al-4V on UA, the sphericity coefficient was approximately 0.9 (korzhyk2025prospectsofultrasound pages 2-4). The absence of high-velocity gas jets eliminates the main satellite-formation mechanism present in gas atomization.

**Oxygen content.** For the Mo–Si–Ti UA powders, oxygen picked up during atomization and handling was approximately 900 ppm, bringing the total from ~460 ppm (as-cast) to 1280–1450 ppm in the powder state (hinrichs2021flexiblepowderproduction pages 4-7). For Al alloys, oxygen content is typically determined by the native oxide thickness (~2–4 nm Al₂O₃) and scales inversely with particle size. At O₂ levels <100 ppm in the chamber, oxygen content of 20–63 μm Al powder should be in the range 200–600 ppm.

**Cooling rate and microstructure.** Droplets of 20–100 μm diameter cooling in argon experience cooling rates of approximately 10³–10⁵ K/s, depending on size, velocity, and gas pressure. For 50 μm Al alloy droplets in argon at ~1 bar, cooling rates of ~10⁴ K/s are expected, sufficient to retain Zr, Sc, Ti, and Mn in supersaturated solid solution in the finer fractions. In coarser particles (>80 μm), primary Al₃Zr may nucleate during solidification, particularly for alloys with ≥0.6 wt% Zr. Whether coarse powder containing primary Al₃Zr still prints well depends on the size and volume fraction of these precipitates; small primary Al₃Zr can serve as potent grain refiners during LPBF re-melting.

**Hollow particles and porosity.** UA produces minimal internal gas porosity because there is no entrapped atomizing gas, unlike gas atomization where hollow particles are common. Any residual internal porosity in UA particles arises from shrinkage during solidification.

## 7. Sieve Cut for LPBF

**Standard LPBF powder.** The conventional sieve fraction for aluminium LPBF is 15–45 μm or 20–53 μm, with layer thicknesses of 20–30 μm. Gas-atomized AlSi10Mg typically has D50 ≈ 45 μm with only ~54% falling in the 25–63 μm L-PBF range (stella2026processabilityofrecycled pages 55-60, stella2026processabilityofrecycled pages 60-65).

**Coarser fractions.** LPBF with 45–106 μm Ti-6Al-4V powder achieved 98.7% density in initial optimization and >99.9% density with a separate parameter set for larger geometries (both as-built and after HIP), demonstrating that coarse powder can produce fully dense parts if process parameters are adjusted (liravi2026laserpowderbed pages 13-15, liravi2026laserpowderbed pages 1-2). Surface roughness increased from ~9.5 μm to ~15.7 μm with the coarser powder (liravi2026laserpowderbed pages 13-15). Layer thickness must be increased to at least 50–60 μm (or even 80 μm) for powders with D50 > 50 μm to ensure powder spreading without excessive porosity.

**Recommended sieve cut for your rePOWDER powder at 40 kHz.** The 20–63 μm fraction is the best compromise: it captures the bulk of the UA distribution (~50–65% yield), provides adequate flowability, and can be printed on research LPBF platforms (Aconity MIDI, MINI, LAB, Renishaw AM400, reduced-build-plate SLM kits) at layer thicknesses of 30–40 μm. The 15–45 μm cut would be ideal for surface quality but may yield only 25–40% of the atomized batch, requiring excessive recirculation. A secondary 45–90 μm cut can be tested at 50–60 μm layer thickness with appropriate parameter development.

**Minimum powder mass.** For single-track experiments on a reduced build platform (e.g., 50 × 50 mm), approximately 50–100 g of sieved powder suffices. For density cube optimization (10 × 10 × 10 mm cubes, ~20 cubes), approximately 200–400 g is needed depending on overflow/loss. Sub-size tensile bars (gauge length ~15 mm, as per ASTM E8 sub-size) require approximately 300–500 g to print a statistically meaningful batch on a small platform. Given your 170–350 g charges and estimated 50–65% in-cut yield, each atomization run yields roughly 85–230 g of 20–63 μm powder, meaning 2–4 runs may be needed per alloy for a full mechanical-property campaign.

## 8. Recommended Settings Table for Nine Alloy Classes

The table below provides engineering starting windows for the 40 kHz rePOWDER with Mo plate, 1.5:1 booster, argon atmosphere, and 170–350 g charges:

| Alloy class | Approx. liquidus (°C) | Melt setpoint (°C) | Hold time (min) | Pour overpressure (bar) | Amplitude (%) | Expected D50 (µm) | Expected 20–63 µm yield (%) | Mg/Zn overcharge | Key cautions |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1. Al–10Si–0.35Mg | ≈596 | 810–830 | 3–5 | 0.17–0.20 | 90–100 | 45–55 | 50–60 | Mg: +5–10% | Relatively easy baseline alloy; minimize oxide-film entrainment and verify Mg before/after atomization. Settings and yields are engineering starting estimates benchmarked against published Al atomization data. (soong2023atomizationofmetal pages 8-8, yankin2025effectofultrasonic pages 2-3, stella2026processabilityofrecycled pages 55-60) |
| 2. Al–4.5Mg–0.7Sc–0.3Zr–0.5Mn (Scalmalloy-type) | ≈630 | 870–920 | 8–15 | 0.17–0.20 | 90–95 | 40–50 | 55–65 | Mg: +10–15% | Sc/Zr dissolution requires elevated temperature, but prolonged high-temperature holding accelerates Mg evaporation; confirm complete dissolution and composition analytically. Sc and Zr themselves have negligible evaporative loss. (khvan2018newinsightsinto pages 1-6, bartl2022influenceofsurface pages 8-10) |
| 3. Al–5Mn–0.8Cr–0.6Zr or Al–Mn–Ti–Zr | ≈660–680 | 920–980 | 10–20 | 0.18–0.22 | 90–95 | 45–55 | 50–60 | None routinely; determine Mn correction from a trial mass balance | High sludge/intermetallic risk from Mn–Cr–Zr; ≥950°C may be necessary for dissolution. Use fine Al-based master alloys, induction stirring, and preferably BN-coated graphite; inspect the nozzle for solids before pouring. Very high superheat can cause substantial Mn loss. (khvan2018newinsightsinto pages 1-6, bartl2022influenceofsurface pages 8-10) |
| 4. Al–3.6Mg–1.2Zr | ≈640 | 930–980 | 10–20 | 0.17–0.20 | 90–95 | 40–50 | 55–65 | Mg: +10–15% | The unusually high Zr level needs an extended, well-stirred dissolution hold; avoid cooling below the relevant liquidus before pouring. High temperature conflicts directly with Mg retention, so add Mg late where practicable. (khvan2018newinsightsinto pages 1-6, bartl2022influenceofsurface pages 8-10) |
| 5. Al–1Fe–1Zr or Al–2Fe–1Mg–1Zr | ≈650 | 900–950 | 8–15 | 0.17–0.20 | 90–100 | 45–55 | 50–60 | Mg: +5% for Al–2Fe–1Mg–1Zr | Fe and Zr increase the dissolution burden and may leave coarse intermetallics; verify a clean nozzle stream. For the Mg-bearing variant, minimize hold time after Mg addition. (soong2023atomizationofmetal pages 8-8, khvan2018newinsightsinto pages 1-6) |
| 6. Al–5–7Mg–2–3Si, eutectic-type | ≈570–590 | 800–840 | 3–5 | 0.17–0.20 | 90–100 | 40–50 | 55–65 | Mg: +10–15% | Mg lowers surface tension and is expected to shift the PSD finer, but it is volatile and oxidation-prone. Avoid unnecessary superheat or long holds; monitor plate wetting and oxide skins. (presz2024ultrasonicatomizationas pages 6-7, bartl2022influenceofsurface pages 8-10) |
| 7. Al–Mg–Er–Zr | ≈640 | 920–970 | 10–15 | 0.17–0.20 | 90–95 | 40–50 | 55–65 | Mg: +10–15% | Er/Zr dissolution requires high temperature; Er can be lost preferentially to oxide-rich dross rather than evaporation. Prefer BN-coated graphite or a validated dense ceramic, keep O₂ and moisture low, and add Mg late. Published rePOWDER settings for this composition were not found. (khvan2018newinsightsinto pages 1-6, eskin2017ultrasonicprocessingof pages 7-10) |
| 8. Al–Zn–Mg–Cu–Zr, 7xxx-type | ≈620–640 | 870–920 | 5–10 | 0.17–0.20 | 90–100 | 40–50 | 55–65 | Zn: +15–25%; Mg: +10% | Highest composition-fidelity risk: Zn and Mg are volatile, and losses rise sharply with temperature, reduced pressure, exposed surface area, and time. Keep the chamber near atmospheric Ar pressure, shorten the hold, and establish overcharge from ICP/OES mass-balance trials rather than assuming universal recovery. (smalcerz2021kineticsofzinc pages 4-7, smalcerz2021kineticsofzinc pages 2-4) |
| 9. Al–Ce or Al–Ni eutectic | ≈640 | 850–900 | 3–5 | 0.17–0.20 | 90–100 | 45–55 | 50–60 | None routinely | Al–Ce: Ce is highly oxygen-reactive and can reduce/contact-react with some refractories; prefer alumina or a validated BN barrier rather than bare graphite. Al–Ni is comparatively straightforward, but coarse intermetallics must be dissolved. Published rePOWDER PSD/settings for these alloys were not found. (soong2023atomizationofmetal pages 8-8, eskin2017ultrasonicprocessingof pages 7-10) |


*Table: Engineering starting windows for 40 kHz rePOWDER atomization with a Mo plate; most alloy-specific D50 values, yields, holds, and overcharges are estimates requiring short design-of-experiments trials and pre-/post-atomization chemical analysis. Literature supports the general Al atomization baseline, frequency/amplitude trends, refractory-element dissolution concerns, and volatility risks, but not complete validated recipes for all nine compositions.*

**Cleaning between alloys.** To avoid cross-contamination, disassemble and ultrasonically clean the crucible, nozzle, and sealing rod in ethanol or acetone between alloy families. The Mo plate should be scraped and polished with fine SiC paper. Special concern applies to Sc→non-Sc transitions (trace Sc contaminates grain-refining response), Er→non-RE transitions, Zn-bearing→Zn-free alloys (Zn condenses on cold chamber walls and can transfer to subsequent batches), and any Sn or Pb-bearing master alloys. A "sacrificial" atomization run of the next alloy (discarding the powder) is recommended after transitions between chemically dissimilar alloys.

## Limitations and Gaps in Published Data

Several aspects of this guidance are estimates rather than measured data, specifically:

- **No published rePOWDER-specific PSD data exist for any of the nine alloy classes listed.** The measured Al data come from pure Al (60 kHz, Priyadarshi), Al-10Cu (40 kHz rePOWDER, Ukabhai), and AlSi12 (35 kHz ATO Lab+, Yankin).
- **Dissolution kinetics** of Al-10Zr, Al-20Mn, Al-20Cr, or elemental Cr/Mn powder in a small induction-stirred rePOWDER melt have not been published. The hold times recommended are based on foundry practice for larger melts.
- **Mg, Zn, and Mn overcharge values** are starting estimates. The argon-shielding factor (~10⁻³ relative to vacuum) greatly reduces evaporation compared to vacuum melting, but the atomization step creates enormous surface area; no study has measured element loss during ultrasonic atomization of Al–Mg or Al–Zn alloys on rePOWDER.
- **LPBF parameter development** for 20–63 μm UA powder from these specific alloys has not been published. The coarse-powder LPBF data come from Ti-6Al-4V (Liravi 2026).
- **Cooling rate** and microstructure (cell size, primary Al₃Zr/Al₃Sc formation) in UA Al-alloy powder particles have not been directly measured; values are estimated from gas-atomization literature.

Each alloy should be validated with a short trial-and-error campaign: melt a small charge, atomize, analyse composition (ICP-OES) and PSD (laser diffraction), and iterate the overcharge and melt temperature before committing larger charges.

---

**Key references (DOIs):**
- Priyadarshi et al., Additive Manufacturing 83, 104033 (2024): doi:10.1016/j.addma.2024.104033
- Ukabhai et al., MATEC Web Conf. 417, 03001 (2025): doi:10.1051/matecconf/202541703001
- Yankin et al., Scientific Reports 15 (2025): doi:10.1038/s41598-025-06086-7
- Presz et al., Materials 17, 6109 (2024): doi:10.3390/ma17246109
- Bärtl et al., J. Mater. Eng. Perform. 31, 6221 (2022): doi:10.1007/s11665-022-06592-z
- Smalcerz et al., Materials 14, 6641 (2021): doi:10.3390/ma14216641
- Gitzhofer et al., Materials 14, 5355 (2021): doi:10.3390/ma14185355
- Eskin, Mater. Sci. Technol. 33, 636 (2017): doi:10.1080/02670836.2016.1162415
- Khvan et al., J. Alloys Compd. 743, 626 (2018): doi:10.1016/j.jallcom.2018.02.023
- Hinrichs et al., Metals 11, 1723 (2021): doi:10.3390/met11111723
- Liravi et al., Materials 19, 3049 (2026): doi:10.3390/ma19143049
- Jedynak et al., Mater. Res. Proc. 41, 156 (2024): doi:10.21741/9781644903131-17
- Bałasz et al., J. Achiev. Mater. Manuf. Eng. 116, 11 (2023): doi:10.5604/01.3001.0016.3393
- Korzhyk et al., Paton Welding J. 2025(10), 3 (2025): doi:10.37434/tpwj2025.10.01
- Ciftcli et al., JSPM 72, S729 (2025): doi:10.2497/jjspm.15e-sis13-03
