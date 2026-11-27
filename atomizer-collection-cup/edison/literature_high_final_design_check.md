# Edison job-futurehouse-paperqa3-high: literature_high_final_design_check

Task `715c82d5-8c6e-410e-89c5-4dea3aeca1b1`, status success.

<details><summary>Query</summary>

```text
Context. A university lab is replacing the powder collection container of an AMAZEMET rePOWDER ultrasonic
atomizer after a run (0.82 kg of nickel-aluminium bronze, UNS C63000, poured at about 1300 C) produced 1-3 mm
shot instead of powder; the shot piled up on a splash plate and a butterfly valve just under the container's
top seal, burned the EPDM valve seat and cracked the borosilicate tube. The chamber is evacuated to about
10 mbar absolute, backfilled with argon several times and runs at +150 mbar gauge; its relief valve opens at
+0.8 bar gauge. The container hangs from the water-cooled cone's ISO-KF-50 outlet on a hinged clamp.

Final design (please critique, with sources): a TIG-welded vessel, 250 mm long, made of a KF-50 x 2 in
butt-weld stub (304L), a 3 x 2 in concentric butt-weld reducer (316L, 101.6 mm long, 0.065 in wall), a 3 in OD x
0.065 in 316 tube and an 8 mm 316L floor disc (three square-butt / chamfered welds, ER316L, argon back-purge).
Inside: a loose 304 catch puck (70 x 25 mm) on the floor and a loose 304 liner tube (2-3/4 in x 0.065 in) standing
on it, both sacrificial. No valve, no splash plate and no ledge inside the top; the bore only widens below the
seal. A stainless centring ring with an FKM O-ring and an over-pressure ring (rated 50 psig) at the cone joint.
The manufacturer's splash shields (thin discs) lie in the cone's mouth above the joint. Two type K washer
thermocouples under worm clamps: on the stub just below the flange, and 6 mm above the floor, read by a
2-channel meter with relay alarms at 120 C (top) and 150 C (bottom).

Our CalculiX axisymmetric transient model (packed bed of shot at 1050 C, 70 % liquid, k_eff 5 W/m K, pile on the
puck, radiation from the pile top by Monte-Carlo view factors, outside convection 8 W/m2K plus radiation) gives a
peak O-ring temperature of 26 / 32 / 45 C for 100 / 400 / 816 g of shot and a floor peak of about 120 / 255 / 340 C;
a catalogue alternative (KF-50 nipple 160 mm with a blank on the bottom and the puck inside the bottom
centring ring) reaches 128 / 207 / 245 C at its bottom O-ring for 100 / 250 / 400 g. Static FEA gives 7 MPa at
+1.2 bar, 6 MPa under full vacuum and 86 MPa thermal stress at the floor's inside corner (yield about 106 MPa at
320 C).

Questions:
1. What would you change in this design or its materials for this duty (hot copper-alloy shot, Al and Cu alloy
   powders, vacuum/argon cycling)? Any concern with 304L welded to 316L, with ER316L on 0.065 in wall, or with
   sensitisation, distortion of the KF flange 19 mm from a weld, or galling of the loose liner?
2. Is a peak thermal stress near yield at a sharp inside corner of a welded flat floor acceptable for a few
   hundred thermal cycles (shakedown, ASME VIII-2 / III ratcheting rules)? Should the corner get an inside
   fillet weld or a dished floor?
3. Are the alarm set points sensible? What do atomizer or vacuum-furnace operators use to detect unatomized
   melt reaching a collector (thermocouples, pyrometers, load cells, cameras)?
4. Leak and pressure testing: acceptance criteria for a rate-of-rise test on a ~10-20 L chamber at 10 mbar,
   bench soap testing, and whether a pneumatic proof test at 1.5 x the relief setting is appropriate for a
   small stainless vessel with a KF joint (or whether a hydrostatic test is better practice).
5. Any published incidents or lessons on KF joints under positive pressure, over-pressure rings, or elastomer
   seals near hot powder.
Give numbers with sources (standards, vendor technical notes, papers with DOIs) and mark estimates.

```

</details>

Question: Context. A university lab is replacing the powder collection container of an AMAZEMET rePOWDER ultrasonic
atomizer after a run (0.82 kg of nickel-aluminium bronze, UNS C63000, poured at about 1300 C) produced 1-3 mm
shot instead of powder; the shot piled up on a splash plate and a butterfly valve just under the container's
top seal, burned the EPDM valve seat and cracked the borosilicate tube. The chamber is evacuated to about
10 mbar absolute, backfilled with argon several times and runs at +150 mbar gauge; its relief valve opens at
+0.8 bar gauge. The container hangs from the water-cooled cone's ISO-KF-50 outlet on a hinged clamp.

Final design (please critique, with sources): a TIG-welded vessel, 250 mm long, made of a KF-50 x 2 in
butt-weld stub (304L), a 3 x 2 in concentric butt-weld reducer (316L, 101.6 mm long, 0.065 in wall), a 3 in OD x
0.065 in 316 tube and an 8 mm 316L floor disc (three square-butt / chamfered welds, ER316L, argon back-purge).
Inside: a loose 304 catch puck (70 x 25 mm) on the floor and a loose 304 liner tube (2-3/4 in x 0.065 in) standing
on it, both sacrificial. No valve, no splash plate and no ledge inside the top; the bore only widens below the
seal. A stainless centring ring with an FKM O-ring and an over-pressure ring (rated 50 psig) at the cone joint.
The manufacturer's splash shields (thin discs) lie in the cone's mouth above the joint. Two type K washer
thermocouples under worm clamps: on the stub just below the flange, and 6 mm above the floor, read by a
2-channel meter with relay alarms at 120 C (top) and 150 C (bottom).

Our CalculiX axisymmetric transient model (packed bed of shot at 1050 C, 70 % liquid, k_eff 5 W/m K, pile on the
puck, radiation from the pile top by Monte-Carlo view factors, outside convection 8 W/m2K plus radiation) gives a
peak O-ring temperature of 26 / 32 / 45 C for 100 / 400 / 816 g of shot and a floor peak of about 120 / 255 / 340 C;
a catalogue alternative (KF-50 nipple 160 mm with a blank on the bottom and the puck inside the bottom
centring ring) reaches 128 / 207 / 245 C at its bottom O-ring for 100 / 250 / 400 g. Static FEA gives 7 MPa at
+1.2 bar, 6 MPa under full vacuum and 86 MPa thermal stress at the floor's inside corner (yield about 106 MPa at
320 C).

Questions:
1. What would you change in this design or its materials for this duty (hot copper-alloy shot, Al and Cu alloy
   powders, vacuum/argon cycling)? Any concern with 304L welded to 316L, with ER316L on 0.065 in wall, or with
   sensitisation, distortion of the KF flange 19 mm from a weld, or galling of the loose liner?
2. Is a peak thermal stress near yield at a sharp inside corner of a welded flat floor acceptable for a few
   hundred thermal cycles (shakedown, ASME VIII-2 / III ratcheting rules)? Should the corner get an inside
   fillet weld or a dished floor?
3. Are the alarm set points sensible? What do atomizer or vacuum-furnace operators use to detect unatomized
   melt reaching a collector (thermocouples, pyrometers, load cells, cameras)?
4. Leak and pressure testing: acceptance criteria for a rate-of-rise test on a ~10-20 L chamber at 10 mbar,
   bench soap testing, and whether a pneumatic proof test at 1.5 x the relief setting is appropriate for a
   small stainless vessel with a KF joint (or whether a hydrostatic test is better practice).
5. Any published incidents or lessons on KF joints under positive pressure, over-pressure rings, or elastomer
   seals near hot powder.
Give numbers with sources (standards, vendor technical notes, papers with DOIs) and mark estimates.


## Critique of the Hot-Shot Collector Vessel Design for an AMAZEMET rePOWDER Ultrasonic Atomiser

The following assessment addresses each of the five questions using evidence from the literature and applicable standards. A consolidated summary is provided in the table below.

| Topic | Current Design Value | Concern/Finding | Recommendation | Key Source/Standard |
|---|---|---|---|---|
| 304L/316L dissimilar welding | 304L KF stub to 316L reducer/tube; ER316L GTAW | Metallurgically compatible; dilution, ferrite balance, heat input, and root oxidation matter more than the small grade mismatch. | Retain ER316L; qualify the weld procedure, use low heat input and full argon back-purge, and perform visual plus liquid-penetrant examination. | Related dissimilar-austenitic GTAW studies (patil2024experimentalinvestigationon pages 2-4, noorbakhsh2026effectoffiller pages 1-2, kant2018fabricationandcharacterization pages 3-5) |
| Thin wall and KF distortion | 1.65 mm wall; weld about 19 mm from KF flange | Burn-through, angular distortion, and seal-face warping are credible; no source establishes 19 mm as inherently safe. | Fixture and heat-sink the flange, use pulsed GTAW and balanced short segments, then inspect flange flatness, concentricity, and seal-face condition. | Heat-input and HAZ evidence (patil2024experimentalinvestigationon pages 4-6, kant2018fabricationandcharacterization pages 1-3) |
| Sensitisation | 304L/316L base metals and ER316L filler | Low carbon greatly reduces chromium-carbide sensitisation but does not eliminate it after excessive heat input or repeated thermal cycles. | Control heat input/interpass temperature, maintain purge until the root cools, remove heat tint, and passivate. | Sensitisation evidence (patil2024experimentalinvestigationon pages 2-4, patil2024experimentalinvestigationon pages 4-6, tandon2023impactoffiller pages 6-8) |
| Loose liner galling | Loose 304 liner on loose 304 puck | Austenitic stainless contacts can gall; vacuum/inert conditions weaken oxide-film protection. Reported self-mated threshold is about 18 ksi or 124 MPa, but sliding distance and temperature strongly affect damage. | Provide generous clearance, rounded edges, and removal tabs; consider dissimilar sacrificial grades. Avoid hydrocarbon anti-seize in powder service. | Galling and oxidation studies (bhansali1982theroleof pages 6-9, rogers2020theinteractionof pages 4-5, daure2023gallingofstainless pages 6-7, daure2023gallingofstainless pages 8-9) |
| Thermal stress and shakedown | 86 MPa elastic peak at floor corner; estimated yield 106 MPa at 320 °C; pressure stress 6–7 MPa | Ratios are about 0.81 yield thermal and 0.06–0.07 yield primary. The ideal Bree boundary permits a thermal range near 2 yield when primary stress is below 0.5 yield, suggesting low ratcheting risk; this does not qualify a welded corner or fatigue life. | Model the actual weld radius and residual-stress sensitivity; conduct mesh convergence and several elastic-plastic hot/cold cycles; separately assess fatigue. | ASME VIII-2 Part 5.5.6/5.5.7 and Bree analysis ([name redacted]2017asmeboilerand pages 85-88, carter2005analysisofcyclic pages 2-4, carter2005analysisofcyclic pages 4-6) |
| Floor geometry | 8 mm flat disc with abrupt internal corner | A sharp modeled corner can create a singular or highly mesh-sensitive peak and is unfavorable for thermal fatigue. | Prefer a shallow dished/radiused floor with a full-penetration butt weld; second choice is a machined generous inside radius or qualified smooth weld contour, not a cosmetic fillet. | Cyclic stress and ratcheting principles (swaminathan2005shakedownandratcheting pages 17-24, [name redacted]2017asmeboilerand pages 103-107, swaminathan2005shakedownandratcheting pages 51-55) |
| FKM seal limit | FKM O-ring; predicted peaks 26/32/45 °C | Generic FKM ratings are about 200–204 °C continuous and roughly 230 °C short-term. Predicted temperatures have ample margin if the thermal model is validated. | Verify the exact compound/vendor rating; retain shielding and replace the seal after abnormal heating or visible hardening/damage. | FKM temperature data (tavares2008vacuumsystems–drawbacks pages 38-42, schroeder1999fluorocarbonelastomers pages 13-15, solutions2016oringsandbackup pages 31-33) |
| Alarm set points | 120 °C top and 150 °C bottom; external washer thermocouples | Conservative relative to FKM limits, but external washer sensors may lag and under-read the inner wall. | Retain the alarms; add rate-of-rise logic and a latched high-high trip validated by representative hot-shot tests. Trip melt input while maintaining inerting and cooling. | FKM limits and high-temperature vacuum practice (tavares2008vacuumsystems–drawbacks pages 38-42, [name redacted]1990tisolfacilityonline pages 100-107, [name redacted]1990tisolfacilityonline pages 39-44) |
| Melt-arrival detection | Two type-K washer thermocouples | Thermocouples are rugged but indirect; cameras and pyrometers need a protected sight line, while load cells detect abnormal mass but not temperature. | Use TCs as primary sensors; add a hanger load cell if practical. Use a protected two-colour pyrometer or camera for diagnostics rather than as the sole trip. | High-temperature systems use pyrometers and thermocouples ([name redacted]1990tisolfacilityonline pages 100-107, [name redacted]1990tisolfacilityonline pages 114-118) |
| Rate-of-rise leak test | Chamber about 10–20 L at about 10 mbar absolute | Total gas load is Q = V × dp/dt and includes leakage, outgassing, permeation, and temperature effects. No universal acceptance value applies. | Project-specific estimate: Q ≤ 10^-2 mbar·L/s for a gross operational check and preferably ≤ 10^-3 mbar·L/s for repeatable purging. For 15 L these correspond to about 0.040 and 0.0040 mbar/min. Trend against an established baseline. | Pressure-rise method (rottlander2016fundamentalsofleak pages 12-13, manual–chapter2024pressuresystemssafety pages 28-30, hucknall1991vacuumtechnologyand pages 180-185) |
| Soap/bubble test | Proposed bench soap test | Useful for locating gross positive-pressure leaks but not for demonstrating low vacuum leakage; residues can contaminate the vessel. | Use dry nitrogen or argon at low pressure with commercial leak solution externally, then rinse/dry. Follow with rate-of-rise or helium mass-spectrometer testing. | ASME Section V Article 10 methods and leak-detection guidance ([name redacted]2017asmeboilerand pages 185-189, [name redacted]2017asmeboilerand pages 199-201, tavares2008vacuumsystems–drawbacks pages 50-53) |
| Hydrostatic proof | Relief set at +0.8 bar(g); proposed proof +1.2 bar(g) | Relief setting is not automatically MAWP. Modern ASME VIII-1 hydrotest pressure is generally at least 1.3 × MAWP times the allowable-stress ratio; older rules used 1.5. Hydrotest stores much less energy than a gas test. | Define MAWP for the complete assembly first. Prefer hydrotesting the welded vessel with a code-rated closure, followed by thorough drying and passivation. | ASME VIII-1 UG-99 comparisons ([name redacted]2017asmeboilerand pages 183-185, [name redacted]2017asmeboilerand pages 185-189, manual–chapter2024pressuresystemssafety pages 15-17) |
| Pneumatic proof | Proposed 1.5 × relief setting using KF joint | Modern VIII-1 pneumatic testing is generally about 1.1 × MAWP times stress ratio; VIII-2 uses 1.15. A 1.5 × pneumatic test is not a generic current-code requirement and compressed gas adds rupture energy. | Use pneumatic proof only when hydrotesting/drying is impracticable; apply remote staged pressurisation, restraint, barriers, calibrated relief, and an exclusion zone. | ASME pneumatic ratios and safety guidance ([name redacted]2017asmeboilerand pages 196-199, manual–chapter2024pressuresystemssafety pages 22-25) |
| KF-50 positive-pressure joint | Hinged clamp plus 50 psig over-pressure ring; normal +0.15 bar(g), relief +0.8 bar(g) | Standard ISO-KF is fundamentally a quick-release vacuum joint; generic vacuum references do not establish a positive-pressure rating. The complete assembly rating is limited by the weakest matched component. | Obtain written manufacturer confirmation for KF-50 size, clamp, centring ring, O-ring, temperature, cycles, and proof pressure. Positively retain the hanging collector and prevent personnel exposure below it. | ISO-KF vacuum-service description (tavares2008vacuumsystems–drawbacks pages 46-50) |
| Incident lessons | Prior EPDM seat burned and borosilicate cracked; shields now above joint | Published high-temperature vacuum experience shows radiant heat threatening O-rings, cryopumps, and hardware; effective mitigations included water-cooled shielding, close cooling, interlocks, and redundant temperature measurement. Specific peer-reviewed KF positive-pressure incident reports were not found. | Treat the prior event as a credible design-basis upset: preserve a ledge-free bore, shields above the seal, thermal trips, cooling/pressure interlocks, independent support, and post-upset inspection. | TISOL high-temperature operating lessons ([name redacted]1990tisolfacilityonline pages 107-114, [name redacted]1990tisolfacilityonline pages 100-107, [name redacted]1990tisolfacilityonline pages 114-118, [name redacted]1990tisolfacilityonline pages 39-44) |


*Table: Summary of the principal material, welding, cyclic-stress, instrumentation, leak-test, pressure-test, and KF-joint findings for the proposed hot-shot collector. Numerical leak limits and several operating recommendations are explicitly identified as project-specific estimates rather than code requirements.*

---

### 1. Design and Material Concerns

**304L welded to 316L with ER316L filler.** The 304L/316L combination is a mild dissimilar joint between two austenitic grades with closely matched thermal expansion coefficients and similar delta-ferrite solidification behaviour. ER316L is an appropriate filler choice: it provides a fully austenitic weld with distributed delta ferrite, good corrosion resistance, and tensile strength exceeding that of 304L base metal (noorbakhsh2026effectoffiller pages 1-2, kant2018fabricationandcharacterization pages 3-5). The small compositional difference between 304L and 316L means that dilution-related property changes are minimal compared with truly dissimilar joints such as austenitic-to-ferritic welds (patil2024experimentalinvestigationon pages 2-4, kant2018fabricationandcharacterization pages 1-3).

**Sensitisation.** Low-carbon L-grades greatly reduce chromium-carbide precipitation in the sensitisation temperature range (~450–850 °C), but sensitisation is not entirely eliminated, particularly after excessive heat input, prolonged interpass dwell, or repeated thermal cycles. One dissimilar-weld study measured a degree of sensitisation (DLEPR) of 9.18% in an E316L weld metal, confirming that some susceptibility persists even with L-grade filler (tandon2023impactoffiller pages 6-8). The practical mitigation is to control heat input (≲0.5 kJ/mm for 1.65 mm wall, *estimate*), limit interpass temperature, and maintain a continuous argon back-purge until the root cools below approximately 300 °C. Post-weld passivation and removal of heat tint are advisable, especially where copper-alloy powder contact could set up galvanic effects.

**ER316L on 0.065 in (1.65 mm) wall.** This wall thickness is weldable by pulsed GTAW with a 1.0–1.6 mm filler rod, but burn-through, root collapse, and angular distortion are significant risks. Pulsed-current GTAW (PCGTAW) has been used successfully on comparable 1.6 mm ER316L joints in research settings (patil2024experimentalinvestigationon pages 4-6). Fit-up must be tight and uniform; any significant gap will cause burn-through or undercut. The argon back-purge is mandatory.

**KF flange distortion.** At 19 mm from the flange face, the weld's heat-affected zone extends toward the KF seal face. No published study was found establishing a safe minimum distance, but standard vacuum-industry practice calls for fixturing and heat-sinking the flange during welding, then verifying flatness and concentricity of the seal face with a dial indicator or CMM. If angular distortion exceeds the ISO-KF centering-ring tolerance (typically ≤0.5 mm total indicated runout, *estimate*), the seal may not seat reliably.

**Galling of the loose liner.** Self-mated austenitic stainless steels are galling-prone: the ASTM G98 threshold galling stress is approximately 18 ksi (124 MPa) for both 304–304 and 316–316 contacts (bhansali1982theroleof pages 6-9). Crucially, an oxidised 316L surface showed roughly 30 times less galling damage than an unoxidised surface at the same load (rogers2020theinteractionof pages 4-5), and operating at elevated temperature (100 °C) significantly increased galling severity for 304/316 pairs (daure2023gallingofstainless pages 8-9). In argon or vacuum, the protective oxide film is absent or quickly worn through, raising galling susceptibility. Mitigation options include: (a) accepting the liner and puck as sacrificial (already stated), (b) providing generous radial clearance (≥1 mm on diameter) and removing the liner with a twist-free axial pull aided by a tab or bail, (c) pre-passivating both surfaces so a fresh oxide forms before first use, and (d) avoiding 304-on-304 self-mating by using one component in a dissimilar alloy (e.g. 316L puck with 304 liner or vice versa, though the benefit is marginal). Hydrocarbon anti-seize must not be used in powder service.

**Other material recommendations.** The choice of 316L for the lower tube and reducer is sound given copper-alloy powder contact and occasional warm-water exposure. Consider specifying all 316/316L (no mixed grades) to simplify consumable control. The 8 mm 316L floor disc is adequately thick for pressure but marginal for thermal stress (see Question 2).

---

### 2. Thermal Stress, Shakedown, and Floor Geometry

**Bree diagram assessment.** The user's FEA reports 86 MPa elastic thermal stress at the floor's inside corner, with a yield stress of approximately 106 MPa at 320 °C. The primary (pressure) stress is 6–7 MPa. Normalising to yield: σ_thermal/S_y ≈ 0.81 and σ_primary/S_y ≈ 0.07. On the classical Bree interaction diagram for a thin cylinder with constant primary pressure and cyclic thermal stress, the elastic shakedown boundary lies at a thermal stress range of 2S_y (i.e. σ_thermal/S_y = 2) when the primary stress is below 0.5S_y (carter2005analysisofcyclic pages 2-4, [name redacted]2017asmeboilerand pages 103-107, carter2005analysisofcyclic pages 4-6). Because the reported thermal stress ratio of 0.81 is well below 2.0, the ideal Bree assessment places this loading combination in the elastic or elastic-shakedown (E) region, meaning that after a few initial cycles, the response should stabilise and no incremental ratcheting is expected.

**Caveats.** The Bree diagram applies to an idealised thin-walled cylinder with uniform membrane stress. It does not directly qualify a sharp inside corner at a welded flat floor, where the stress is a local structural discontinuity stress plus a peak weld-toe stress concentration. The 86 MPa value from an axisymmetric model may be mesh-sensitive at a mathematically sharp corner; with a realistically modelled weld root radius (~1–2 mm) or a deliberately machined fillet, the peak will decrease. ASME VIII-2 Part 5, Paragraph 5.5.6 requires the primary-plus-secondary stress range to remain within the elastic shakedown domain (conventionally ≤3S_m ≈ 2S_y) and separately requires fatigue evaluation per Part 5.5.3 if the component is in cyclic service ([name redacted]2017asmeboilerand pages 85-88, lower2022equivalentsafetyevaluation pages 88-90). For elastic-plastic analysis per Paragraph 5.5.7, demonstration of a stabilised stress-strain hysteresis loop or bounded accumulated plastic strain (≤5% per ASME III Article XIII-3440) is required (gilmartin2024designbyanalysis pages 80-83). The sensitivity of ratcheting behaviour to small load increases has been shown to be very high: a 1.2% increase in thermal load produced a 70.9% increase in ratcheting strain near a boundary (swaminathan2005shakedownandratcheting pages 51-55).

**Recommendation: fillet vs. dished floor.** The sharp inside corner is the worst-case geometry for both thermal fatigue and stress-corrosion cracking. A dished (torispherical or ellipsoidal) floor eliminates the right-angle junction entirely and reduces thermal stress through curvature-induced flexibility and thermal-path redistribution. If a flat floor must be retained, a generous machined inside fillet radius (≥3t = ~5 mm minimum, ideally 8–10 mm, *estimate*) or a full-penetration weld with a smooth, blended internal profile is strongly preferable to an unrelieved sharp corner. A cosmetic fillet bead laid inside a sharp square-butt joint is not recommended, as it introduces another HAZ and stress concentration without eliminating the geometric discontinuity. Modelling a few elastic-plastic thermal cycles in CalculiX with the actual post-weld geometry will confirm whether the response is shakedown or alternating plasticity and will provide a strain range for a fatigue-life estimate.

---

### 3. Alarm Set Points and Melt-Detection Methods

**FKM O-ring temperature limits.** The continuous-service temperature rating for generic FKM (Viton A type) is approximately 200–204 °C, with short-term excursions to approximately 230 °C and very short exposure (48 h) at 315 °C (tavares2008vacuumsystems–drawbacks pages 38-42, schroeder1999fluorocarbonelastomers pages 13-15, solutions2016oringsandbackup pages 31-33, schroeder1999fluorocarbonelastomers pages 15-18). Viton outgassing in vacuum begins to show carbon-oxide decomposition products around 210 °C (tavares2008vacuumsystems–drawbacks pages 38-42). The proposed alarm at 120 °C on the stub (near the KF seal) is conservative, being approximately 60% of the continuous limit, which provides margin for sensor lag, local hot spots, and thermal transients. The 150 °C bottom alarm is similarly conservative and appropriate for detecting an excessive thermal load approaching structural concern.

**Sensor selection.** Type K washer thermocouples under worm clamps are a robust, low-cost approach. External washer sensors will, however, lag the inner-wall and O-ring temperature, potentially by tens of degrees during a fast transient (such as a large shot pile landing). Rate-of-rise alarming (°C/min threshold) is recommended in addition to absolute setpoints. A latched high-high trip that halts melt feed while maintaining argon flow and water cooling is advisable.

**Alternative detection methods.** In gas atomisation and vacuum-furnace practice, several techniques are used for detecting unatomised melt reaching a collector or unexpected locations:
- **Thermocouples** are the most common and are used in the TISOL on-line isotope-separation facility, where thermocouples on vacuum-chamber walls and near seals provided essential thermal safety data ([name redacted]1990tisolfacilityonline pages 100-107, [name redacted]1990tisolfacilityonline pages 39-44).
- **Optical pyrometers** (single- or two-colour) are used where a direct sight path to the hot material exists; the TISOL facility used an optical pyrometer to monitor source temperature before transitioning to a tungsten-rhenium thermocouple rated to 2760 °C ([name redacted]1990tisolfacilityonline pages 100-107, [name redacted]1990tisolfacilityonline pages 114-118). A protected two-colour pyrometer aimed through a sight port above or below the collection zone could detect shot arrival by its infrared signature, but would require a clean, unobstructed window.
- **Load cells or strain-gauge hangers** can detect mass accumulation in real time and would flag an unexpectedly large load, but do not directly sense temperature.
- **Cameras** (visible or infrared) through borosilicate or sapphire viewports are increasingly used in research atomisers, but window survival and fouling are concerns in this application.

For this system, the thermocouple-based approach with rate-of-rise logic is recommended as the primary safety interlock, supplemented by a hanger load cell or visual camera as a diagnostic tool.

---

### 4. Leak and Pressure Testing

**Rate-of-rise test.** For an evacuated chamber at approximately 10 mbar, the standard pressure-rise method is: evacuate the vessel, isolate the pump, and record pressure versus time (rottlander2016fundamentalsofleak pages 12-13, manual–chapter2024pressuresystemssafety pages 28-30, hucknall1991vacuumtechnologyand pages 180-185). The leak rate is calculated as Q_L = V × Δp/Δt, where V is the vessel volume in litres, Δp is the pressure increase in mbar, and Δt is the elapsed time in seconds, yielding Q_L in mbar·L/s (rottlander2016fundamentalsofleak pages 12-13, hucknall1991vacuumtechnologyand pages 172-177). A real leak produces a linear pressure-rise curve; outgassing produces a decaying curve that must be allowed to stabilise before measuring the linear portion (manual–chapter2024pressuresystemssafety pages 28-30, tavares2008vacuumsystems–drawbacks pages 50-53). For a ~15 L chamber at 10 mbar (rough vacuum service with argon backfill cycling), no universal code acceptance value exists. A reasonable project-specific criterion is Q_L ≤ 1 × 10⁻² mbar·L/s for gross integrity (corresponding to Δp ≈ 0.04 mbar/min for 15 L), and preferably ≤ 1 × 10⁻³ mbar·L/s for repeatable vacuum and purge performance (*estimates*). The "gas-tight" general criterion cited in the literature is below 10⁻⁷ mbar·L/s, which is relevant to high-vacuum or He-leak-tested systems (rottlander2016fundamentalsofleak pages 7-9). For this application, the leak rate should ensure the vessel can be evacuated to 10 mbar within a reasonable pump-down time and that the argon purity remains adequate between cycles.

**Soap/bubble testing.** A bench soap test with the vessel pressurised to low positive pressure (e.g. +0.5 bar argon or nitrogen) is a practical gross-leak check but is limited to detecting leaks of approximately 10⁻³ to 10⁻⁴ mbar·L/s and does not replace a vacuum rate-of-rise test (tavares2008vacuumsystems–drawbacks pages 50-53). Soap residues must be thoroughly rinsed and dried to avoid contaminating powder or the vacuum seal.

**Pneumatic vs. hydrostatic proof test.** ASME BPVC Section VIII, Division 1 (UG-99/UG-100) establishes hydrostatic testing as the standard proof-test method ([name redacted]2017asmeboilerand pages 183-185, manual–chapter2024pressuresystemssafety pages 22-25, manual–chapter2024pressuresystemssafety pages 15-17). The 2015 edition requires a minimum hydrostatic test pressure of 1.3 × MAWP × (S_T/S) ([name redacted]2017asmeboilerand pages 183-185). Pneumatic testing is an alternative permitted when the vessel cannot safely be filled with water, cannot be readily dried, or service conditions do not tolerate residual liquid ([name redacted]2017asmeboilerand pages 189-190). The 2015 pneumatic test pressure is 1.1 × MAWP × (S_T/S) for Division 1 and 1.15 × MAWP × (S_T/S) for Division 2 ([name redacted]2017asmeboilerand pages 196-199, [name redacted]2017asmeboilerand pages 189-190, [name redacted]2017asmeboilerand pages 199-201). Pneumatic testing stores significantly more energy than hydrostatic testing—at the same pressure, the pneumatic stored energy can be approximately 200 times greater—and requires exclusion-zone calculations, barricading, staged pressurisation, and formal safety review (manual–chapter2024pressuresystemssafety pages 22-25, edwards2011evaluatingandreducing pages 1-2).

**Practical recommendation for this vessel.** For a small (~15 L, ~1 bar gauge MAWP) stainless vessel with a KF joint, the absolute stored energy during a pneumatic proof test at 1.2 bar is very low (of order PV ≈ 15 L × 1.2 bar ≈ 18 J, expanding to ~1 bar atmospheric, *estimate*), making the blast hazard negligible at any reasonable exclusion distance. Nevertheless, good practice is to: (a) hydrostatically test the welded body (without the KF O-ring or centring ring) to 1.3–1.5 × MAWP, then drain and dry; (b) assemble the complete vessel with the KF seal and pressure-test pneumatically at 1.1–1.15 × MAWP with nitrogen, using staged pressurisation, behind a barrier; (c) follow with a vacuum rate-of-rise test and a soap-bubble check at positive pressure. The proposed 1.5 × relief setting (i.e. 1.5 × 0.8 = 1.2 bar) is consistent with older code hydrostatic ratios but should be justified against a formally defined MAWP, not the relief-valve setting alone.

---

### 5. Incidents and Lessons Learned

**KF joints under positive pressure.** ISO-KF (Klein Flange) connections are fundamentally designed for vacuum service, with published operating ranges typically cited as 1000 to 10⁻⁴ mbar (tavares2008vacuumsystems–drawbacks pages 46-50). No specific peer-reviewed incident reports of KF joint failures under positive pressure were identified in the literature search. However, the standard KF clamp exerts a finite clamping force that may not reliably seal against positive pressure without supplementary retention; over-pressure rings (also called positive-pressure rings or safety clamps) are specifically designed to address this gap by adding mechanical retention against internal pressure. The user's specified 50 psig (3.4 bar) rated over-pressure ring provides margin well above the 0.8 bar relief setting, but the assembly rating is determined by the weakest link—clamp, ring, O-ring, flange weld, and seal-face condition.

**Elastomer seals near hot material.** The TISOL on-line isotope-separation facility at TRIUMF provides the most directly relevant published lessons on protecting elastomer seals from radiant and conducted heat in vacuum equipment. During off-line testing, radiant heat from a resistance-heated target raised the target-chamber temperature sufficiently to threaten the O-ring seals and seriously degrade cryopump performance; the response was to install water-cooled copper shielding between the heat source and the seals ([name redacted]1990tisolfacilityonline pages 100-107, [name redacted]1990tisolfacilityonline pages 39-44). At higher source temperatures (~1900 °C), nearly every metal-to-metal connection seized, and sublimed copper condensed as droplets on heat shields, confirming that thermal overload can produce widespread mechanical and contamination damage ([name redacted]1990tisolfacilityonline pages 107-114). Thermocouple insulation (alumina) vaporised above approximately 1950 °C, causing loss of temperature measurement ([name redacted]1990tisolfacilityonline pages 114-118). The TISOL experience also demonstrated that vacuum-system interlocks (gate-valve closure on pressure rise) and redundant temperature monitoring (pyrometer plus thermocouple) are essential when hot materials are present ([name redacted]1990tisolfacilityonline pages 39-44).

**Lessons for this application.** The user's prior incident—EPDM valve-seat burning and borosilicate-tube cracking from unatomised melt—is itself the most relevant design-basis event. The design changes (eliminating the valve, splash plate, and internal ledges; adding a sacrificial puck/liner; using FKM rather than EPDM; monitoring temperature) directly address the failure mode. Additional recommendations include:
- Maintaining positive argon flow during and after melt pouring to prevent air ingress even if a seal partially fails.
- Using a secondary mechanical restraint (e.g. a safety chain) on the hanging collector so that a failed KF clamp or burned O-ring does not allow the vessel to drop.
- Post-incident inspection of the KF seal face, O-ring, and over-pressure ring after any run producing visible shot rather than powder.
- Documenting each run's thermocouple data to trend vessel thermal history and detect progressive seal or liner degradation.

---

### Summary

The proposed design is fundamentally sound for its intended duty. The principal areas requiring attention are: (a) the sharp inside corner at the flat floor, which should be replaced with a dished floor or generous fillet radius to reduce peak thermal stress and improve fatigue life; (b) verification that the KF flange seal face is not distorted by the nearby weld; (c) explicit manufacturer confirmation of the KF/over-pressure-ring assembly rating for positive pressure and temperature; (d) formal definition of MAWP as the basis for proof-test pressure rather than relying solely on the relief-valve setting; and (e) addition of rate-of-rise alarming and a latched safety trip to the thermocouple system.

References

1. (patil2024experimentalinvestigationon pages 2-4): Tejas Patil, Ajit Bhosale, S.G.K. Manikandan, Bibin Jose, Mithul Naidu, Sachin Salunkhe, Robert Cep, and Emad Abouel Nasr. Experimental investigation on solidification cracking &amp; intergranular corrosion of aisi 321 &amp; aisi 316 l dissimilar weld on pulsed current gas tungsten arc welding (pcgtaw). Heliyon, 10(15):e34648, Aug 2024. URL: https://doi.org/10.1016/j.heliyon.2024.e34648, doi:10.1016/j.heliyon.2024.e34648. This article has 3 citations.

2. (noorbakhsh2026effectoffiller pages 1-2): Reza Zare Noorbakhsh, Farhad Ostovan, Ehsan Shafiei, and Meysam Toozandehjani. Effect of filler metals on microstructure, mechanical properties, and corrosion resistance of gas tungsten arc welded 316ug stainless steel. Materials Today Communications, 57:116584, Dec 2026. URL: https://doi.org/10.1016/j.mtcomm.2026.116584, doi:10.1016/j.mtcomm.2026.116584. This article has 0 citations and is from a peer-reviewed journal.

3. (kant2018fabricationandcharacterization pages 3-5): Rahul Kant, Rutash Mittal, Chandan Kumar, Bharat Singh Rana, Manish Kumar, and Rajnish Kumar. Fabrication and characterization of weldments aisi 304 and aisi 316 used in industrial applications. Materials Today: Proceedings, 5:18475-18481, Jan 2018. URL: https://doi.org/10.1016/j.matpr.2018.06.189, doi:10.1016/j.matpr.2018.06.189. This article has 36 citations.

4. (patil2024experimentalinvestigationon pages 4-6): Tejas Patil, Ajit Bhosale, S.G.K. Manikandan, Bibin Jose, Mithul Naidu, Sachin Salunkhe, Robert Cep, and Emad Abouel Nasr. Experimental investigation on solidification cracking &amp; intergranular corrosion of aisi 321 &amp; aisi 316 l dissimilar weld on pulsed current gas tungsten arc welding (pcgtaw). Heliyon, 10(15):e34648, Aug 2024. URL: https://doi.org/10.1016/j.heliyon.2024.e34648, doi:10.1016/j.heliyon.2024.e34648. This article has 3 citations.

5. (kant2018fabricationandcharacterization pages 1-3): Rahul Kant, Rutash Mittal, Chandan Kumar, Bharat Singh Rana, Manish Kumar, and Rajnish Kumar. Fabrication and characterization of weldments aisi 304 and aisi 316 used in industrial applications. Materials Today: Proceedings, 5:18475-18481, Jan 2018. URL: https://doi.org/10.1016/j.matpr.2018.06.189, doi:10.1016/j.matpr.2018.06.189. This article has 36 citations.

6. (tandon2023impactoffiller pages 6-8): Vipin Tandon, Awanikumar P. Patil, and Suhas Kowshik. Impact of filler electrodes on welding properties of dissimilar welded 316l/201 austenitic stainless steels. RAiSE-2023, pages 90, Dec 2023. URL: https://doi.org/10.3390/engproc2023059090, doi:10.3390/engproc2023059090. This article has 8 citations.

7. (bhansali1982theroleof pages 6-9): K.J. Bhansali and A.E. Miller. The role of stacking fault energy on galling and wear behavior. Wear, 75:241-252, Jan 1982. URL: https://doi.org/10.1016/0043-1648(82)90151-x, doi:10.1016/0043-1648(82)90151-x. This article has 118 citations and is from a highest quality peer-reviewed journal.

8. (rogers2020theinteractionof pages 4-5): Samuel R. Rogers, David Bowden, Rahul Unnikrishnan, Fabio Scenini, Michael Preuss, David Stewart, Daniele Dini, and David Dye. The interaction of galling and oxidation in 316l stainless steel. Wear, 450-451:203234, Jun 2020. URL: https://doi.org/10.1016/j.wear.2020.203234, doi:10.1016/j.wear.2020.203234. This article has 17 citations and is from a highest quality peer-reviewed journal.

9. (daure2023gallingofstainless pages 6-7): J.L. Daure, D. Kóti, M.J. Carrington, D.G. McCartney, D.A. Stewart, and P.H. Shipway. Galling of stainless steels as a function of test conditions in an astm g196-type test setup – the role of temperature, rotational velocity, interrupted rotation and rotational distance. Jul 2023. URL: https://doi.org/10.1016/j.wear.2023.204804, doi:10.1016/j.wear.2023.204804. This article has 12 citations and is from a highest quality peer-reviewed journal.

10. (daure2023gallingofstainless pages 8-9): J.L. Daure, D. Kóti, M.J. Carrington, D.G. McCartney, D.A. Stewart, and P.H. Shipway. Galling of stainless steels as a function of test conditions in an astm g196-type test setup – the role of temperature, rotational velocity, interrupted rotation and rotational distance. Jul 2023. URL: https://doi.org/10.1016/j.wear.2023.204804, doi:10.1016/j.wear.2023.204804. This article has 12 citations and is from a highest quality peer-reviewed journal.

11. ([name redacted]2017asmeboilerand pages 85-88): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

12. (carter2005analysisofcyclic pages 2-4): P. Carter. Analysis of cyclic creep and rupture. part 2: calculation of cyclic reference stresses and ratcheting interaction diagrams. International Journal of Pressure Vessels and Piping, 82:27-33, Jan 2005. URL: https://doi.org/10.1016/j.ijpvp.2004.06.010, doi:10.1016/j.ijpvp.2004.06.010. This article has 44 citations and is from a peer-reviewed journal.

13. (carter2005analysisofcyclic pages 4-6): P. Carter. Analysis of cyclic creep and rupture. part 2: calculation of cyclic reference stresses and ratcheting interaction diagrams. International Journal of Pressure Vessels and Piping, 82:27-33, Jan 2005. URL: https://doi.org/10.1016/j.ijpvp.2004.06.010, doi:10.1016/j.ijpvp.2004.06.010. This article has 44 citations and is from a peer-reviewed journal.

14. (swaminathan2005shakedownandratcheting pages 17-24): S Swaminathan. Shakedown and ratcheting behavior of structures under thermal cycling. Unknown journal, 2005.

15. ([name redacted]2017asmeboilerand pages 103-107): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

16. (swaminathan2005shakedownandratcheting pages 51-55): S Swaminathan. Shakedown and ratcheting behavior of structures under thermal cycling. Unknown journal, 2005.

17. (tavares2008vacuumsystems–drawbacks pages 38-42): VMS Tavares. Vacuum systems–drawbacks. Unknown journal, 2008.

18. (schroeder1999fluorocarbonelastomers pages 13-15): Herman Schroeder. Fluorocarbon Elastomers, pages 410-437. Springer US, Jan 1987. URL: https://doi.org/10.1007/978-1-4615-7823-9\_14, doi:10.1007/978-1-4615-7823-9\_14. This article has 11 citations.

19. (solutions2016oringsandbackup pages 31-33): TS SOlUTIONS. O-rings and back-up rings. Unknown journal, 2016.

20. ([name redacted]1990tisolfacilityonline pages 100-107): [name redacted]. Tisol facility, on-line isotope separation at triumf. Unknown journal, 1990.

21. ([name redacted]1990tisolfacilityonline pages 39-44): [name redacted]. Tisol facility, on-line isotope separation at triumf. Unknown journal, 1990.

22. ([name redacted]1990tisolfacilityonline pages 114-118): [name redacted]. Tisol facility, on-line isotope separation at triumf. Unknown journal, 1990.

23. (rottlander2016fundamentalsofleak pages 12-13): H Rottländer, W Umrath, and G Voss. Fundamentals of leak detection. Unknown journal, 2016.

24. (manual–chapter2024pressuresystemssafety pages 28-30): GS Manual–Chapter. Pressure systems safety w/change 2 (11/15/2024). Unknown journal, 2024.

25. (hucknall1991vacuumtechnologyand pages 180-185): D. J. Hucknall. Vacuum technology and applications. ArXiv, Jan 1991. URL: https://doi.org/10.1016/c2013-0-01220-0, doi:10.1016/c2013-0-01220-0. This article has 57 citations.

26. ([name redacted]2017asmeboilerand pages 185-189): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

27. ([name redacted]2017asmeboilerand pages 199-201): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

28. (tavares2008vacuumsystems–drawbacks pages 50-53): VMS Tavares. Vacuum systems–drawbacks. Unknown journal, 2008.

29. ([name redacted]2017asmeboilerand pages 183-185): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

30. (manual–chapter2024pressuresystemssafety pages 15-17): GS Manual–Chapter. Pressure systems safety w/change 2 (11/15/2024). Unknown journal, 2024.

31. ([name redacted]2017asmeboilerand pages 196-199): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

32. (manual–chapter2024pressuresystemssafety pages 22-25): GS Manual–Chapter. Pressure systems safety w/change 2 (11/15/2024). Unknown journal, 2024.

33. (tavares2008vacuumsystems–drawbacks pages 46-50): VMS Tavares. Vacuum systems–drawbacks. Unknown journal, 2008.

34. ([name redacted]1990tisolfacilityonline pages 107-114): [name redacted]. Tisol facility, on-line isotope separation at triumf. Unknown journal, 1990.

35. (lower2022equivalentsafetyevaluation pages 88-90): [name redacted], [name redacted], and [name redacted]. Equivalent safety evaluation of the 2021 edition of the asme boiler and pressure vessel code to editions incorporated by reference in 49 cfr 192, 193, and 195. Unknown journal, Mar 2022. URL: https://doi.org/10.2172/1928959, doi:10.2172/1928959.

36. (gilmartin2024designbyanalysis pages 80-83): Declan Gilmartin. Design by analysis methods for ductile collapse modes under static and repeated loading. Dissertation, Jan 2024. URL: https://doi.org/10.48730/vb7q-nn67, doi:10.48730/vb7q-nn67. This article has 0 citations.

37. (schroeder1999fluorocarbonelastomers pages 15-18): Herman Schroeder. Fluorocarbon Elastomers, pages 410-437. Springer US, Jan 1987. URL: https://doi.org/10.1007/978-1-4615-7823-9\_14, doi:10.1007/978-1-4615-7823-9\_14. This article has 11 citations.

38. (hucknall1991vacuumtechnologyand pages 172-177): D. J. Hucknall. Vacuum technology and applications. ArXiv, Jan 1991. URL: https://doi.org/10.1016/c2013-0-01220-0, doi:10.1016/c2013-0-01220-0. This article has 57 citations.

39. (rottlander2016fundamentalsofleak pages 7-9): H Rottländer, W Umrath, and G Voss. Fundamentals of leak detection. Unknown journal, 2016.

40. ([name redacted]2017asmeboilerand pages 189-190): [name redacted], [name redacted], and [name redacted]. Asme boiler and pressure vessel code evaluation and equivalence study for liquefied natural gas facilities. Unknown journal, 2017.

41. (edwards2011evaluatingandreducing pages 1-2): VH Edwards, D Sanford, and B Bonstead. Evaluating and reducing the risks of pneumatic pressure testing. Unknown journal, 2011.
