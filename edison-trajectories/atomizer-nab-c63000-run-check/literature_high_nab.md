# Edison job-futurehouse-paperqa3-high result: literature_high_nab

**Task ID:** `836e1e92-cbe6-417c-85b9-dee97ad6c92f`  
**Status:** success

<details><summary>Query</summary>

```text
Context. On 27 Oct 2026 we ultrasonically atomized 1,080 g of nickel aluminum bronze UNS C63000
("630 bronze", ASTM B150 rod; nominal Cu-10Al-5Ni-3Fe wt%; limits Al 9.0-11.0, Ni 4.0-5.5, Fe 2.0-4.0,
Mn <= 1.5, Si <= 0.25, Zn <= 0.30; solidus ~1035 C, liquidus ~1054 C; density 7.58 g/cm3) in an
AMAZEMET rePOWDER ultrasonic atomizer. An earlier review wrongly assumed the alloy was binary Cu-30Ni
(liquidus ~1240 C), so its conclusions (only ~60 C of superheat at 1300 C, heavy dissolution of a Mo or
W plate coating by a Ni-rich melt, C71500 chemistry) must be re-checked for C63000.

Set-up: induction melting in a graphite crucible whose interior was sprayed with a boron nitride
coating (aerosol BN paint) and dried; a boron nitride sealing (stopper) rod (the written plan called for
alumina); an hBN bottom nozzle (planned bore 0.5 mm); chamber and powder container wiped with lint-free
wipes and isopropanol beforehand; argon atmosphere with 24 ppm O2 at the pour. HMI pressures: melting
0.1 bar, "graining" (pouring) 0.19 bar, "turbo" 1.5 bar; we have not confirmed whether these are gauge
or absolute. Melt setpoint 1300 C, read by a type N thermocouple at the crucible wall (the module's
stated maximum), held about 2 min after the charge melted. Atomizing surface: a carbon-fiber composite
plate coated with tungsten (described as "dipped in W"; the vendor's kit includes a W plasma-coated
carbon-fiber plate that it recommends for copper alloys) on a 1:1.5 booster at 90% generator
amplitude.

Outcome of run 1: atomization ran to the end of the charge and the operator estimates ~97% yield, but
the melt only kept flowing while the operator held the turbo (1.5 bar) pressure almost the whole time.
The powder is gold-coloured and contains a visible fraction of shiny flakes. A thin skull remained in
the crucible, and fine gold-coloured dust coated the chamber walls.

Please re-assess the run parameters for C63000, give numbers with sources, and show the inputs to any
estimate where the literature is silent.

1. Melt temperature. 1300 C is ~245 C above the liquidus. Compare with foundry pouring temperatures
   for aluminum bronzes (C95800, C95500, C63000), with gas atomization of nickel aluminum bronze for
   additive manufacturing, and with the published ultrasonic atomization of NAB on this kind of
   atomizer (e.g., doi:10.3390/ma17143396 and doi:10.1088/1757-899X/1296/1/012036, which melted at
   1300 C). What does excess superheat cost here (oxidation and dross, Al and Mn loss, attack on the
   crucible, rod, nozzle and plate, plate overheating, particle shape), and what does too little risk
   (freezing in a 0.5 mm nozzle, skulls)? Recommend a setpoint range for the next run.

2. Why did the melt need near-continuous turbo pressure to keep flowing? Weigh these with estimates:
   (a) Al2O3 skin, dross and oxide bifilms on an aluminum bronze melt, collecting in or over a 0.5 mm
   nozzle (compare alumina clogging of nozzles in Al-killed steel casting, and aluminum bronze oxide
   behaviour in foundry practice); (b) freezing at the nozzle exit (cold nozzle, gas flow beneath it);
   (c) capillary back-pressure of a non-wetting melt in a 0.5 mm bore (surface tension of liquid
   Cu-10Al roughly 1.1-1.3 N/m, contact angle on hBN), compared with 0.19 bar plus the metallostatic
   head; (d) reaction products from the BN coating or rod; (e) the pressure difference across the
   melt if the chamber pressure rises during the pour. How should we diagnose this, and what should we
   change (bore size, nozzle preheat, O2 target, skimming or filtering, graining pressure)?

3. Compatibility of a C63000 melt at 1250-1300 C with each material it touches, using thermodynamic
   estimates: the activity of Al (and of Fe and Ni) in liquid Cu-10Al-5Ni-3Fe; whether Al + BN ->
   AlN + B, Al + C -> Al4C3, or Al reduction of Al2O3-SiO2 binders can proceed at that activity;
   carbon pickup by the Fe and Ni from a graphite crucible or carbon-fiber plate; boron and nitrogen
   pickup; silicon from a silicate binder in the BN paint. Is a BN-painted graphite crucible suitable
   for aluminum bronze, and is a BN or an alumina sealing rod the better choice?

4. The plate. The earlier review used 0.66 wt% W and 3.7 wt% Mo saturation in Cu-30Ni at 1300 C. How
   much W (and Mo) can a Cu-10Al-5Ni-3Fe melt dissolve at 1250-1300 C, given the much lower Ni, the
   Fe, and the Al (Al-W and Al-Mo intermetallics)? How do Al-bronze melts wet W, Mo and carbon, and
   what does the alumina skin do to that? Estimate W pickup in the powder and plate life over repeated
   runs. Is a W-coated carbon-fiber plate appropriate for NAB, and how should it be inspected?

5. Flakes. What produces flakes or splats in ultrasonic atomization (melt flow above the plate's
   atomization capacity, a film too thick to break up, droplets hitting the walls or splash guards
   before they solidify, high amplitude ejecting large ligaments), how would holding the turbo
   pressure (higher flow rate) change this, and how do oxide skins on aluminum bronze affect
   sphericity? How should the flake fraction be measured and reduced?

6. Powder for additive manufacturing and naval parts: expected oxygen pickup (ppm) for aluminum
   bronze powder made in argon with ~20-30 ppm O2, and typical O, N and C limits for NAB powder for
   laser powder-bed fusion or directed energy deposition; the rapid-solidification microstructure
   (martensitic beta-prime, suppressed kappa phases) and the post-build heat treatment usually needed
   for corrosion resistance in seawater; and whether anything in these parameters is likely to push
   the powder out of C63000 limits (Al or Mn loss, W, B, C or Si pickup; C63000 requires Cu plus named
   elements >= 99.5%).

7. Charge size: we charged 1.08 kg, against 250-500 g in the vendor's guidance and published runs.
   What does a larger charge change (time to melt, temperature non-uniformity and thermocouple lag,
   plate heat load and coating wear over a longer pour)?

8. Safety for handling this powder (Ni content, combustible metal dust).

Finish with (a) a table: parameter -> issue for C63000 -> evidence or estimate -> recommended setting
for the next run; and (b) a list of which conclusions of a Cu-30Ni assessment no longer apply, which
still apply, and which new risks C63000 adds.

```

</details>

Question: Context. On 27 Oct 2026 we ultrasonically atomized 1,080 g of nickel aluminum bronze UNS C63000
("630 bronze", ASTM B150 rod; nominal Cu-10Al-5Ni-3Fe wt%; limits Al 9.0-11.0, Ni 4.0-5.5, Fe 2.0-4.0,
Mn <= 1.5, Si <= 0.25, Zn <= 0.30; solidus ~1035 C, liquidus ~1054 C; density 7.58 g/cm3) in an
AMAZEMET rePOWDER ultrasonic atomizer. An earlier review wrongly assumed the alloy was binary Cu-30Ni
(liquidus ~1240 C), so its conclusions (only ~60 C of superheat at 1300 C, heavy dissolution of a Mo or
W plate coating by a Ni-rich melt, C71500 chemistry) must be re-checked for C63000.

Set-up: induction melting in a graphite crucible whose interior was sprayed with a boron nitride
coating (aerosol BN paint) and dried; a boron nitride sealing (stopper) rod (the written plan called for
alumina); an hBN bottom nozzle (planned bore 0.5 mm); chamber and powder container wiped with lint-free
wipes and isopropanol beforehand; argon atmosphere with 24 ppm O2 at the pour. HMI pressures: melting
0.1 bar, "graining" (pouring) 0.19 bar, "turbo" 1.5 bar; we have not confirmed whether these are gauge
or absolute. Melt setpoint 1300 C, read by a type N thermocouple at the crucible wall (the module's
stated maximum), held about 2 min after the charge melted. Atomizing surface: a carbon-fiber composite
plate coated with tungsten (described as "dipped in W"; the vendor's kit includes a W plasma-coated
carbon-fiber plate that it recommends for copper alloys) on a 1:1.5 booster at 90% generator
amplitude.

Outcome of run 1: atomization ran to the end of the charge and the operator estimates ~97% yield, but
the melt only kept flowing while the operator held the turbo (1.5 bar) pressure almost the whole time.
The powder is gold-coloured and contains a visible fraction of shiny flakes. A thin skull remained in
the crucible, and fine gold-coloured dust coated the chamber walls.

Please re-assess the run parameters for C63000, give numbers with sources, and show the inputs to any
estimate where the literature is silent.

1. Melt temperature. 1300 C is ~245 C above the liquidus. Compare with foundry pouring temperatures
   for aluminum bronzes (C95800, C95500, C63000), with gas atomization of nickel aluminum bronze for
   additive manufacturing, and with the published ultrasonic atomization of NAB on this kind of
   atomizer (e.g., doi:10.3390/ma17143396 and doi:10.1088/1757-899X/1296/1/012036, which melted at
   1300 C). What does excess superheat cost here (oxidation and dross, Al and Mn loss, attack on the
   crucible, rod, nozzle and plate, plate overheating, particle shape), and what does too little risk
   (freezing in a 0.5 mm nozzle, skulls)? Recommend a setpoint range for the next run.

2. Why did the melt need near-continuous turbo pressure to keep flowing? Weigh these with estimates:
   (a) Al2O3 skin, dross and oxide bifilms on an aluminum bronze melt, collecting in or over a 0.5 mm
   nozzle (compare alumina clogging of nozzles in Al-killed steel casting, and aluminum bronze oxide
   behaviour in foundry practice); (b) freezing at the nozzle exit (cold nozzle, gas flow beneath it);
   (c) capillary back-pressure of a non-wetting melt in a 0.5 mm bore (surface tension of liquid
   Cu-10Al roughly 1.1-1.3 N/m, contact angle on hBN), compared with 0.19 bar plus the metallostatic
   head; (d) reaction products from the BN coating or rod; (e) the pressure difference across the
   melt if the chamber pressure rises during the pour. How should we diagnose this, and what should we
   change (bore size, nozzle preheat, O2 target, skimming or filtering, graining pressure)?

3. Compatibility of a C63000 melt at 1250-1300 C with each material it touches, using thermodynamic
   estimates: the activity of Al (and of Fe and Ni) in liquid Cu-10Al-5Ni-3Fe; whether Al + BN ->
   AlN + B, Al + C -> Al4C3, or Al reduction of Al2O3-SiO2 binders can proceed at that activity;
   carbon pickup by the Fe and Ni from a graphite crucible or carbon-fiber plate; boron and nitrogen
   pickup; silicon from a silicate binder in the BN paint. Is a BN-painted graphite crucible suitable
   for aluminum bronze, and is a BN or an alumina sealing rod the better choice?

4. The plate. The earlier review used 0.66 wt% W and 3.7 wt% Mo saturation in Cu-30Ni at 1300 C. How
   much W (and Mo) can a Cu-10Al-5Ni-3Fe melt dissolve at 1250-1300 C, given the much lower Ni, the
   Fe, and the Al (Al-W and Al-Mo intermetallics)? How do Al-bronze melts wet W, Mo and carbon, and
   what does the alumina skin do to that? Estimate W pickup in the powder and plate life over repeated
   runs. Is a W-coated carbon-fiber plate appropriate for NAB, and how should it be inspected?

5. Flakes. What produces flakes or splats in ultrasonic atomization (melt flow above the plate's
   atomization capacity, a film too thick to break up, droplets hitting the walls or splash guards
   before they solidify, high amplitude ejecting large ligaments), how would holding the turbo
   pressure (higher flow rate) change this, and how do oxide skins on aluminum bronze affect
   sphericity? How should the flake fraction be measured and reduced?

6. Powder for additive manufacturing and naval parts: expected oxygen pickup (ppm) for aluminum
   bronze powder made in argon with ~20-30 ppm O2, and typical O, N and C limits for NAB powder for
   laser powder-bed fusion or directed energy deposition; the rapid-solidification microstructure
   (martensitic beta-prime, suppressed kappa phases) and the post-build heat treatment usually needed
   for corrosion resistance in seawater; and whether anything in these parameters is likely to push
   the powder out of C63000 limits (Al or Mn loss, W, B, C or Si pickup; C63000 requires Cu plus named
   elements >= 99.5%).

7. Charge size: we charged 1.08 kg, against 250-500 g in the vendor's guidance and published runs.
   What does a larger charge change (time to melt, temperature non-uniformity and thermocouple lag,
   plate heat load and coating wear over a longer pour)?

8. Safety for handling this powder (Ni content, combustible metal dust).

Finish with (a) a table: parameter -> issue for C63000 -> evidence or estimate -> recommended setting
for the next run; and (b) a list of which conclusions of a Cu-30Ni assessment no longer apply, which
still apply, and which new risks C63000 adds.


# Re-Assessment of Ultrasonic Atomization Parameters for UNS C63000 Nickel Aluminum Bronze

## 1. Melt Temperature

The 1300 °C setpoint provides approximately 246 °C of superheat above the C63000 liquidus (~1054 °C), which is substantially higher than the ~60 °C assumed in the earlier Cu-30Ni review (which used a ~1240 °C liquidus). Published ultrasonic atomization of CuAl10Ni5Fe5 on an AMAZEMET AUS 500 atomizer also used 1300 °C with 1.5 bar system pressure, 40 kHz sonotrode frequency, and Ar grade 5.0, producing highly spherical powder with a mean aspect ratio of 0.935 and 82% of particles above AR = 0.9 (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 6-7). Thus 1300 °C is a demonstrated operating point for NAB ultrasonic atomization, but it is the module's stated maximum and provides more superheat than is typically needed.

Foundry practice for aluminum bronzes (C95800, C95500, C63000) generally uses pouring temperatures of 1150–1200 °C, corresponding to roughly 100–150 °C of superheat. Gas atomization of NAB powder (CuAl10Fe5Ni5) for thermal spraying has been performed using electrode induction-melting gas atomization (krebs2016thermischesundkinetisches pages 40-43). In gas atomization, superheats of 150–300 °C are common to maintain flow through small-diameter nozzles, so 1300 °C is within the gas-atomization range but at the high end.

**Costs of excess superheat:** Accelerated oxidation and dross generation (especially problematic with 10 wt% Al); increased Al and Mn vapor loss from the exposed melt surface; enhanced attack on graphite, BN coatings, and the atomizing plate; increased plate heat load and coating degradation over a longer pour; and reduced melt viscosity that can overshoot the plate's atomization capacity. **Costs of insufficient superheat:** Freezing in a 0.5 mm nozzle, incomplete melt-through, skulling, and interrupted flow.

**Recommendation:** Begin the next run at a 1225–1250 °C wall setpoint, increase in 25 °C steps only if flow remains unstable, and reserve 1300 °C for troubleshooting. Independently verify that the type N thermocouple at the crucible wall reads within ±15 °C of the true bulk-melt temperature, as a 1080 g charge in a small crucible may have significant radial gradients.

## 2. Flow Obstruction and the Need for Continuous Turbo Pressure

Several mechanisms likely contributed, in approximate order of importance:

**(a) Al₂O₃ skin and dross.** A melt containing ~10 wt% Al forms a tenacious Al₂O₃-rich oxide film on any exposed surface within milliseconds at 24 ppm O₂. This skin is analogous to the alumina clogging observed in Al-killed steel continuous casting, where Al₂O₃ inclusions accrete on submerged-entry nozzle walls and progressively restrict flow. In aluminum bronze foundry practice, the oxide skin is similarly recognized as a persistent problem that must be managed through careful pouring technique, fluxing, and filtering. An oxide raft or bridge spanning a 0.5 mm bore would require substantial overpressure to rupture.

**(b) Capillary back-pressure.** The surface tension of liquid Cu-10Al near its liquidus (~1074 K, or approximately the Al₁₀Cu₉₀ composition in mole percent) is approximately 1.35 ± 0.01 N/m, with a temperature coefficient of −2.1 × 10⁻⁴ N/(m·K) (schmitz2014surfacetensionof pages 3-7). For a cylindrical bore of diameter d = 0.5 mm, the maximum capillary pressure ΔP_cap = 4γ cos θ / d. With γ = 1.35 N/m and a non-wetting contact angle on hBN estimated at 120–150°, cos θ ranges from −0.5 to −0.87, giving ΔP_cap ≈ 5.4–10.8 kPa (0.054–0.108 bar). The metallostatic head for a 50–100 mm melt column at 7580 kg/m³ contributes only 3.7–7.4 kPa. Therefore, a graining pressure of 0.19 bar (if gauge, contributing 19 kPa) may only marginally exceed the capillary resistance plus head losses, particularly if the bore is partially blocked by oxide.

**(c) Freezing.** The nozzle tip is cooled by argon flow beneath it. With only ~246 °C superheat, the melt stream loses significant heat while traversing a cold ceramic nozzle. A 0.5 mm stream has a very high surface-to-volume ratio, and even a brief flow interruption could allow a frozen shell to form on the nozzle wall.

**(d) BN reaction products.** At the activity of Al in Cu-10Al, the reaction Al + BN → AlN + B is thermodynamically marginal; the free energy depends on the effective Al activity, which is reduced from its pure-component value by negative deviation in liquid Cu-Al (williams1984thermodynamicsofcoppernickel pages 12-17). However, reaction products from the BN aerosol-paint binder (which may contain silicates) could contribute localized deposits.

**(e) Chamber pressure rise.** If the chamber absolute pressure rises during the pour (e.g., from argon injection or inadequate venting), the net pressure differential across the melt decreases, slowing or stopping flow.

**Diagnosis:** Inspect the nozzle post-run for oxide accretions, frozen metal, or discoloration. Weigh the skull. Log both crucible-side and chamber-side absolute pressures throughout the pour. Confirm whether HMI values are gauge or absolute.

**Changes for the next run:** Enlarge the bore to 0.8–1.0 mm; reduce O₂ to <10 ppm before melting; preheat the nozzle assembly if practical; increase graining pressure to 0.3–0.5 bar differential (verified); use turbo only as a brief unblocking pulse; and consider a debris screen above the nozzle to trap dross.

## 3. Compatibility of C63000 Melt with Crucible, Rod, and Nozzle Materials

**Activity of Al in liquid Cu-10Al-5Ni-3Fe at 1250–1300 °C.** The thermodynamic activity coefficient of Al in liquid Cu is significantly less than unity due to the strong negative mixing enthalpy of the Cu-Al system (williams1984thermodynamicsofcoppernickel pages 12-17). For 10 wt% Al (~20 at% Al) at 1300 °C, the Raoultian activity of Al is estimated at roughly 0.01–0.05, depending on the thermodynamic model used. The addition of 5% Ni and 3% Fe modifies this somewhat but does not eliminate the reactivity.

**Al + BN → AlN + B.** The standard free energy of formation of AlN is approximately −287 kJ/mol at 1300 °C, while that of BN is approximately −225 kJ/mol. The net reaction ΔG° ≈ −62 kJ/mol for unit activities would be favorable, but the reduced Al activity in liquid copper (a_Al ~ 0.01–0.05) raises the effective ΔG by RT ln(a_Al) ≈ +50 to +60 kJ/mol at 1573 K, making the reaction thermodynamically marginal—it may proceed slowly at direct contact points but is not expected to cause rapid degradation of dense hBN.

**Al + C → (1/4)Al₄C₃.** The formation of Al₄C₃ from dissolved Al and graphite carbon is thermodynamically favorable even at reduced Al activity, particularly where the melt contacts uncoated graphite through coating defects. This is a concern specific to C63000 that does not arise with Cu-30Ni.

**Carbon pickup by Fe and Ni.** The presence of 3% Fe and 5% Ni in the Cu matrix increases the solubility of carbon compared to pure liquid copper. While carbon solubility in liquid Cu is extremely low (<1 ppm), Fe raises it significantly. Carbon fibers approximately 20 µm long from the carbon-fiber sonotrode plate were detected in ultrasonically atomized NAB powder, demonstrating a real carbon contamination pathway (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 13-15).

**Boron and nitrogen pickup.** Dense hBN is expected to contribute minimal B and N to the melt at short contact times, but aerosol BN paint with unknown binder chemistry adds uncertainty. Silicon from silicate binders in aerosol BN coatings is a further concern, given C63000's Si limit of ≤0.25%.

**Recommendation:** A BN-painted graphite crucible is not ideal for composition-critical NAB powder production. An alumina or alumina-lined crucible would reduce carbon and boron pickup risks. If graphite must be used, apply a continuous, binder-characterized BN barrier, fully bake it, inspect for pinholes, and minimize temperature and hold time. The dense hBN stopper rod is preferred over alumina for its non-wetting properties and resistance to oxide sticking. Analyze C, B, N, and Si in the powder after each run.

## 4. The Atomizing Plate

**W and Mo solubility.** The earlier Cu-30Ni review used 0.66 wt% W and 3.7 wt% Mo saturation at 1300 °C; these values relied on the high Ni content of Cu-30Ni. In C63000, with only 4–5.5% Ni, W and Mo solubility in the copper-rich melt should be dramatically lower. W solubility in pure liquid Cu at 1300 °C is extremely low (< 0.01 wt%), and while Ni and Fe increase it somewhat, the effect at 5% Ni is far less than at 30% Ni. Mo solubility follows a similar trend.

**Wetting and Al₂O₃ skin effects.** The persistent Al₂O₃ skin on a C63000 melt may actually reduce direct contact between the melt and the W coating, thereby reducing dissolution. Liquid Cu wets alumina with a contact angle of approximately 117° (schmitz2014surfacetensionof pages 3-7), and the oxide film acts as an additional barrier. However, the skin can be disrupted by ultrasonic vibration, periodically exposing fresh metal to the coating.

**Carbon fiber substrate.** The more critical concern for NAB is not W dissolution but carbon-fiber release from the substrate. Fine carbon fibers up to ~20 µm were experimentally observed in UA-produced NAB powder (uhlmann2024acomparativeevaluation pages 10-12). Over repeated runs at 1250–1300 °C, thermal cycling, melt erosion, and mechanical wear will progressively damage the W coating and expose the carbon-fiber composite substrate.

**Recommendation:** The W-coated carbon-fiber plate is conditionally appropriate for C63000 (the dissolution concern is much less than for Cu-30Ni). Photograph, weigh, and inspect the plate before and after every run. Measure W and C content in the powder. Retire the plate if the W coating shows cracking, edge recession, or exposed fibers. For long-term production, consider a solid W or WC plate if available.

## 5. Flakes and Splats

Flake formation in ultrasonic atomization results from several interacting mechanisms:

**(i) Excessive melt flow above the plate's atomization capacity.** Holding turbo pressure at 1.5 bar continuously forced a high mass flow rate through the nozzle, producing a thick liquid film on the plate surface. When the film exceeds the critical breakup thickness for the operating frequency and amplitude, capillary-wave instability cannot fully fragment it into discrete droplets; instead, large ligaments, sheets, and flakes are ejected (yang2026effectsofultrasonic pages 6-11, yang2026effectsofultrasonic pages 11-16).

**(ii) Al₂O₃ oxide skins on droplets.** In ultrasonic atomization of Sn-Bi, oxide films forming above a critical temperature fragmented with the droplets and adhered to particle surfaces, increasing particle size and reducing sphericity (yang2026effectsofultrasonic pages 11-16). For C63000, the Al₂O₃ skin is far more refractory and tenacious, so oxide-encapsulated droplets may be unable to relax to a spherical shape before solidifying.

**(iii) Wall and splash-guard impacts.** Droplets ejected at high velocity (especially large ones from an overloaded plate) may strike the chamber walls or splash guards before fully solidifying, producing flattened splats.

**(iv) High amplitude.** At 90% generator amplitude, the breakup force is strong but so is the kinetic energy of ejected material, increasing the probability of wall impacts.

**Measurement:** Sieve at 200 µm (already done) and then perform dynamic image analysis (CAMSIZER or equivalent) to quantify the flake fraction as particles with aspect ratio below 0.5 or 0.6. SEM examination of the fraction above 100 µm will confirm flake morphology.

**Reduction:** Eliminate continuous turbo pressure; stabilize flow at a rate matched to the plate's atomization capacity through a larger bore and regulated differential pressure; reduce O₂ to minimize oxide skins; and then optimize amplitude from 70–90% at fixed flow rate, selecting the setting by yield, PSD, and aspect ratio.

## 6. Powder for Additive Manufacturing and Naval Parts

**Oxygen pickup.** Ultrasonically atomized CuAl10Ni5Fe5 powder produced under argon shielding contained 0.019 wt% oxygen (190 ppm), compared to 0.013% (130 ppm) for the gas-atomized CuAl9.5Fe reference (uhlmann2024acomparativeevaluation pages 10-12). Gas-atomized NAB powder for thermal spraying contained 350 ± 20 ppm oxygen in the as-atomized condition (krebs2016thermischesundkinetisches pages 40-43). For LPBF of copper alloys, oxygen contents below approximately 200–400 ppm are generally considered acceptable; no published specification for NAB LPBF powder oxygen limits was identified, but the 190 ppm result demonstrates that ultrasonic atomization under good shielding can achieve competitive oxygen levels.

**Typical O, N, C limits.** No formal NAB powder specification for LPBF or DED was found in the literature. By analogy with other AM powder specifications (e.g., AMS standards for Ti and Ni alloys), oxygen should be below ~500 ppm, nitrogen below ~200 ppm, and carbon below ~200 ppm for DED applications. LPBF may tolerate somewhat higher oxygen if it is in the form of a surface oxide rather than internal inclusions.

**Rapid-solidification microstructure.** Gas-atomized NAB powder contains an α matrix with metastable high-temperature β₁ martensitic structures and iron-rich κ precipitates (κ_I–κ_III and nickel-rich κ_IV), with approximately 10–15 atomic percent martensite distributed non-uniformly among particles (krebs2016thermischesundkinetisches pages 82-84, krebs2016thermischesundkinetisches pages 40-43). LPBF-processed NAB (C63000, C63020, C95800) has achieved densities above 99.9% (timmons2025laserpowderbed pages 1-2). The as-built LPBF microstructure consists predominantly or entirely of martensitic β′, with κ phases either suppressed or unresolvable at standard SEM magnification (timmons2025laserpowderbed pages 2-4, doyle2022additivemanufacturingof pages 47-53).

**Heat treatment for corrosion resistance.** The standard post-casting heat treatment for C95800 NAB is 675 ± 10 °C for at least 6 hours (ASTM B505), designed to transform martensitic β′ to α + κ phases and improve ductility and seawater corrosion resistance (doyle2022additivemanufacturingof pages 53-58). For LPBF C63020, this treatment greatly reduced the β′ volume fraction and improved yield strength from 336 to 485 MPa and ductility from 2.9% to 11.4% (timmons2025laserpowderbed pages 2-4). For LPBF C64200 (aluminum-silicon-bronze), heat treatment at 620 °C for 2 h eliminated β′ martensite and improved ductility from ~5% to ~25% (timmons2025laserpowderbed pages 23-26).

**Composition compliance.** C63000 requires Cu plus named elements (Al, Ni, Fe, Mn) ≥ 99.5%, with limits: Al 9.0–11.0, Ni 4.0–5.5, Fe 2.0–4.0, Mn ≤ 1.5, Si ≤ 0.25, Zn ≤ 0.30 wt%. Potential contaminants that could push the powder out of specification include: W from the plate coating, B and N from BN contact materials, C from the graphite crucible or carbon-fiber plate, Si from BN paint binder, and Al or Mn loss through oxidation/volatilization. The Uhlmann study found no substantial compositional change in UA NAB by EDX analysis (uhlmann2024acomparativeevaluation pages 7-10), but EDX lacks the precision needed to confirm compliance with the ≤ 0.5% impurity margin.

## 7. Charge Size

The 1080 g charge is 2.2× the upper end (500 g) and 4.3× the lower end (250 g) of the vendor's guidance and published runs ([name redacted]2023sphericalpowderscontrol pages 4-4, uhlmann2024acomparativeevaluation pages 2-4). The consequences include:

- **Extended melting time.** More time at temperature increases oxidation, dross formation, Al/Mn loss, and carbon pickup from the graphite crucible.
- **Temperature non-uniformity.** A larger melt volume in a small crucible increases radial temperature gradients. The type N thermocouple at the crucible wall may read significantly higher than the melt center or the nozzle region.
- **Thermocouple lag.** The wall-mounted thermocouple responds to the crucible temperature, which lags the melt temperature, especially during melting and initial superheating of a large charge.
- **Plate heat load.** A longer pour delivers more cumulative thermal energy to the plate, increasing the risk of W coating degradation, carbon-fiber exposure, and plate overheating.
- **Coating wear.** Longer melt contact erodes the BN crucible coating, increasing the probability of exposing graphite to the melt.

**Recommendation:** Reduce to 400–500 g for parameter development. If 1 kg batches are ultimately needed, split into 2–3 pours with fresh plates or plate inspection between runs.

## 8. Safety for Handling This Powder

**Nickel content.** C63000 contains 4.0–5.5 wt% Ni. Nickel and its compounds are classified as carcinogenic to humans (IARC Group 1 for nickel compounds; Group 2B for metallic nickel). The ACGIH TLV for inhalable nickel metal dust is 1.5 mg/m³. Respiratory protection and exposure monitoring are required during powder handling, sieving, transfer, and chamber cleaning.

**Combustible metal dust.** Although elemental copper and nickel powders did not propagate flame in standardized 20-L explosion chamber tests using a 5000 J ignitor (cashdollar1994flammabilityofmetals pages 4-5, cashdollar1994flammabilityofmetals pages 1-2), copper-alloy product safety data sheets classify processing-generated dust and fines as combustible dust and a Category 1 flammable solid (dust2023section1identification pages 3-4, dust2023section1identification pages 1-3). The SDS warns that dust concentrations may form explosive atmospheres, that fines can react with water releasing flammable hydrogen, and that molten material reacts violently with water (dust2023section1identification pages 7-9, dust2023section1identification pages 12-14).

**Practical requirements:** Use grounded, conductive, enclosed powder-handling equipment; metal-dust-rated local exhaust ventilation with explosion venting or suppression; antistatic clothing and non-sparking tools; Class D fire extinguishing agents; and appropriate respiratory and skin protection. Do not use ordinary vacuum cleaners. Obtain explosibility testing (MEC, MIT, K_St, P_max) on the actual powder particle-size distribution before any scale-up. Store powder in sealed containers under inert gas.

## Summary Tables

The following table maps each run parameter to the C63000-specific issue, the evidence or estimate supporting the assessment, and the recommended setting for the next run:

| Parameter | Issue for C63000 | Evidence or estimate | Recommended setting for next run |
|---|---|---|---|
| Melt temperature | At 1300 °C, nominal superheat is **246 °C** above the stated 1054 °C liquidus. This increases oxidation, Al/Mn loss, refractory attack, plate heat load, and hold-time sensitivity; inadequate superheat risks nozzle freezing and skulls. | Published ultrasonic atomization of CuAl10Ni5Fe5 used **1300 °C**, 1.5 bar system pressure, 40 kHz, and Ar 5.0, so 1300 °C is demonstrated but not necessarily optimal (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 7-10). | Begin at a **1225–1250 °C wall setpoint** and increase in 25 °C steps only if flow remains unstable. Use **1250–1275 °C** if the nozzle is difficult to preheat; reserve **1300 °C** for troubleshooting. Independently verify bulk-melt temperature. |
| Chamber O₂ | **24 ppm O₂** permits rapid regeneration of an Al₂O₃ skin on a melt containing about 10 wt% Al. Oxide fragments can bridge a small nozzle and inhibit droplet spheroidization. | Ultrasonic-atomized NAB produced under good Ar shielding contained **0.019 wt% O, or 190 ppm**, showing that low powder oxygen is achievable but not that 24 ppm prevents surface-film formation (uhlmann2024acomparativeevaluation pages 10-12). | Purge to **less than 10 ppm O₂**, preferably **less than 5 ppm**, before melting and maintain it through pouring. Log O₂ continuously and check for air ingress during pressure-mode changes. |
| Nozzle bore | A nominal **0.5 mm** bore is highly sensitive to oxide fragments, reaction products, dimensional error, and freezing. | Using surface tension γ = 1.35 N/m, the maximum cylindrical capillary scale is 4γ/d = **10.8 kPa, or 0.108 bar**. For a non-wetting contact angle of 120–180°, the estimated barrier is about **0.054–0.108 bar**. The measured surface tension near the liquidus for a Cu-rich Al–Cu alloy is 1.35 N/m (schmitz2014surfacetensionof pages 3-7). | Start with a verified **0.8 mm hBN bore**; use **1.0 mm** if blockage persists. Measure and inspect the finished bore and quantify melt flow before returning to 0.5 mm. |
| Graining pressure | If **0.19 bar** is differential pressure, it only modestly exceeds estimated capillary resistance and may not overcome an oxide bridge or frozen lip. If it is absolute pressure, the pressure balance is entirely different. | Metallostatic pressure equals density × gravity × melt depth. With density 7580 kg/m³, a **50–100 mm** head contributes only about **0.037–0.074 bar**. Net drive equals crucible absolute pressure minus chamber absolute pressure plus metallostatic head. | Confirm whether every HMI value is gauge or absolute and record pressure on both sides of the melt. If equipment ratings permit, trial a regulated differential of **0.30–0.50 bar**, then reduce it to the lowest value producing a steady, capacity-matched stream. |
| Turbo pressure | Near-continuous **1.5 bar** probably forced excessive or pulsating flow through a partial restriction, thickening the plate film and promoting ligaments, splashes, flakes, and plate overheating. | Published NAB atomization used **1.5 bar system pressure**, but its pressure reference and nozzle geometry are not established here (uhlmann2024acomparativeevaluation pages 4-6). Film thickness, amplitude, temperature, and oxide films all affect breakup and morphology (yang2026effectsofultrasonic pages 6-11, yang2026effectsofultrasonic pages 11-16). | Use turbo only as a **brief start or unblock pulse**, not as normal feed pressure. Obtain steady flow through nozzle cleanliness, preheating, a larger bore, and regulated differential pressure. |
| Crucible material | BN-painted graphite limits direct contact, but coating pinholes, binder cracking, or erosion expose carbon. Fe and Ni increase carbon-pickup concern, and Al₄C₃ formation is thermodynamically possible at direct carbon contact. | Fine carbon fibres were found in ultrasonically atomized NAB powder produced using a carbon-fibre sonotrode, demonstrating a real carbon-contamination pathway (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 13-15). Carbon pickup from this particular crucible configuration has not been quantified. | Prefer a qualified **high-alumina or alumina-lined crucible** for composition-critical powder. If graphite is retained, use a continuous binder-characterized BN barrier, dry and bake it fully, inspect for pinholes, minimize temperature and hold time, and measure **C, B, N, and Si**. |
| Sealing rod | Dense hBN is non-wetting and releases readily, whereas alumina may collect adherent oxide. BN nevertheless creates possible B/N pickup and must not contain a silicate binder. | Direct C63000 reaction data are sparse. Liquid Cu is non-wetting on alumina at approximately 117°, while dense BN is commonly used as a non-wetting metal-contact material (schmitz2014surfacetensionof pages 3-7). | Retain a **dense, binder-free hBN stopper rod** if post-run inspection shows no erosion. Otherwise compare it with dense high-purity alumina. Do not coat the immersed tip with aerosol BN paint or unidentified binder; analyze B and N after the run. |
| Atomizing plate | The earlier Cu–30Ni W/Mo saturation values do not apply. W dissolution should be much lower in low-Ni C63000, but coating cracks, local Al–W reaction, thermal fatigue, and exposure of carbon fibres can still contaminate powder. | NAB ultrasonic atomization produced carbon fibres up to about **20 µm** from the carbon-fibre sonotrode (uhlmann2024acomparativeevaluation pages 10-12). The same work obtained powder with mean aspect ratio **0.935**, with 82% of particles above 0.9 aspect ratio (uhlmann2024acomparativeevaluation pages 6-7). | The vendor’s **W plasma-coated carbon-fibre plate is conditionally appropriate**. Photograph, weigh, and inspect it before and after every run for W loss, cracking, edge recession, exposed fibres, delamination, and warping. Measure W and C in powder and retire the plate if substrate becomes exposed or contamination rises. |
| Charge size | **1080 g** is 2.2 times a 500 g batch and 4.3 times a 250 g batch. It extends melting and pouring, increases thermal gradients and thermocouple lag, and raises oxide production, plate heat input, and coating wear. | Published rePOWDER descriptions establish water-cooled vibrating-sonotrode operation but do not validate this charge size ([name redacted]2023sphericalpowderscontrol pages 4-4). The stated 250–500 g equipment guidance should therefore control development runs. | Use **250–500 g**, preferably **400–500 g**, during parameter development. Divide 1.08 kg into at least two or three separately qualified pours. |
| Ultrasonic amplitude | **90% generator amplitude** supplies strong breakup but may eject large ligaments or splashes when incoming flow is excessive or pulsating. Reducing amplitude alone will not correct excessive mass flow. | Increasing amplitude accelerates capillary-wave growth and film breakup; unfavorable film conditions produce irregular particles and satellites (yang2026effectsofultrasonic pages 6-11). | Retain **90%** only after stabilizing mass flow. Then compare **70%, 80%, and 90%** at fixed temperature and flow, selecting the setting by yield, PSD, aspect ratio, and measured flake fraction. |
| Atmosphere | Ar 5.0 is suitable, but gas purity alone does not control chamber O₂, moisture, leaks, backflow, or the pressure difference across the nozzle. | Published NAB ultrasonic atomization used **Ar grade 5.0** and produced powder containing 0.019 wt% O (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 10-12). | Continue **Ar 5.0 or better**. Leak-check, purge below 10 ppm O₂, monitor dew point, and log crucible-side and chamber absolute pressures throughout pouring. |
| Powder handling | C63000 contains **4.0–5.5 wt% Ni**, creating inhalation and sensitization concerns. Fine powder and chamber-wall dust should be treated as combustible dust despite non-ignition results for some pure Cu and Ni samples. | Pure Cu and Ni dust did not propagate flame in one 20 L study, but that does not qualify bronze powder. Copper-alloy safety information classifies generated fines as combustible dust and warns of ignition and explosion hazards (cashdollar1994flammabilityofmetals pages 4-5, dust2023section1identification pages 3-4, dust2023section1identification pages 7-9). | Use enclosed transfer, grounded conductive equipment, metal-dust-rated local extraction, antistatic clothing, eye protection, and exposure-assessment-based respiratory protection. Prohibit ignition sources and ordinary vacuum cleaners; obtain explosibility testing for the actual powder PSD before scale-up. |


*Table: This table links each run parameter to C63000-specific failure mechanisms, quantitative evidence or transparent estimates, and a practical next-run setting. Recommendations prioritize stable, low-oxide flow before particle-size or throughput optimization.*

The following table compares each conclusion from the earlier Cu-30Ni assessment with its validity for C63000:

| Conclusion from Cu–30Ni assessment | Status for C63000 | Explanation |
|---|---|---|
| Only ~60 °C superheat at 1300 °C | **No longer applies** | C63000 liquidus is approximately 1054 °C, not approximately 1240 °C; therefore, 1300 °C represents about **246 °C superheat**, not 60 °C. Published ultrasonic atomization of CuAl10Ni5Fe5 nevertheless used 1300 °C, so it is demonstrated but not necessarily optimal (uhlmann2024acomparativeevaluation pages 4-6). |
| Heavy W/Mo dissolution by a Ni-rich melt | **Greatly reduced risk** | C63000 contains only 4.0–5.5 wt% Ni rather than approximately 30 wt% Ni. The Cu–30Ni saturation values cannot be transferred; W and Mo dissolution should be much lower in the Cu-rich NAB melt, while its alumina skin may further impede clean metal–coating contact. This remains an estimate requiring powder and plate analysis. |
| C71500/Cu–30Ni chemistry applies | **No longer applies** | The charge was C63000, nominally Cu–10Al–5Ni–3Fe, with fundamentally different liquidus, oxidation, solidification, refractory compatibility, and rapid-solidification behavior. NAB grades investigated by LPBF include C63000 at nominal Cu–10.5Al–4.5Ni–3.5Fe (timmons2025laserpowderbed pages 1-2). |
| Inert melt with no strongly reactive alloying element | **No longer applies; new risk** | Approximately 10 wt% Al makes C63000 strongly oxygen-reactive. A persistent Al₂O₃-rich skin can obstruct a 0.5 mm nozzle and interfere with droplet breakup and spheroidization. Reactions with BN or carbon are thermodynamically possible, although their extent at the effective Al activity is not established by the available literature (williams1984thermodynamicsofcoppernickel pages 12-17, yang2026effectsofultrasonic pages 11-16). |
| Mo plate coating is an acceptable alternative | **Likely lower risk, but unverified** | Mo dissolution should also be lower than in Cu–30Ni because C63000 has far less Ni. However, Cu–Al–Ni–Fe-specific Mo solubility, reactive wetting, coating erosion, and possible Al–Mo intermetallic formation require direct testing; the earlier 3.7 wt% value must not be reused. |
| BN crucible coating is inert | **Only partly applies; new risk** | Dense, binder-free BN is useful as a non-wetting barrier, but complete chemical inertness toward a 10 wt% Al melt at 1250–1300 °C should not be assumed. AlN/B formation is thermodynamically plausible but activity-dependent; aerosol-paint binders can introduce Si, oxygen, or other contaminants (williams1984thermodynamicsofcoppernickel pages 12-17). |
| Carbon from a graphite crucible or plate is tolerable | **New composition and inclusion risk** | Coating defects expose graphite, and Fe/Ni-containing NAB may acquire more carbon than pure Cu; direct Al–C contact also permits Al₄C₃ formation in principle. Experimentally, fine carbon fibres up to approximately 20 µm were found in ultrasonically atomized NAB from a carbon-fibre sonotrode (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 13-15). |
| Standard 0.5 mm nozzle bore is adequate | **More critical for C63000** | Oxide films and dross make a 0.5 mm bore much less tolerant than it would be for Cu–Ni. With surface tension around 1.35 N/m, the characteristic maximum capillary pressure 4γ/d is approximately 10.8 kPa or 0.108 bar before accounting for contact angle, freezing, oxide bridging, or pressure loss (schmitz2014surfacetensionof pages 3-7). |
| No significant volatile-element loss | **New risk** | Al and especially Mn are more readily oxidized or depleted than the principal Cu–Ni constituents. Higher temperature, longer holding, air ingress, and the large charge increase exposure. Published ultrasonic-atomization literature also notes possible Mn depletion in some alloys, although one NAB study found no substantial compositional change by EDX (uhlmann2024acomparativeevaluation pages 7-10). |
| Powder chemistry is not especially contamination-sensitive | **New risk** | C63000 requires Cu plus the named elements to total at least 99.5%, leaving limited allowance for W, B, C, Si, oxygen-bearing inclusions, and other contamination. Ultrasonic NAB powder has shown carbon-fibre and ceramic contamination despite otherwise favorable composition and morphology (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 7-10). |
| A simple FCC Cu–Ni microstructure is expected | **No longer applies; new metallurgical requirement** | NAB undergoes complex β-to-α-plus-κ transformations. Rapidly solidified C63020 LPBF material has been reported as predominantly or entirely martensitic β′; treatment at 675 °C for 6 h greatly reduced β′ and improved ductility. Such heat treatment is a strong qualification candidate, but seawater-corrosion performance must be demonstrated rather than assumed (timmons2025laserpowderbed pages 2-4). |
| Spherical powder is expected | **Still applies, with an oxide/flow caveat** | Ultrasonic atomization can produce highly spherical NAB powder: mean aspect ratio was 0.935 and 82% of particles had aspect ratio above 0.9. Nevertheless, spatters and carbon fibres were observed, and oxide-bearing films or excessive feed can produce irregular particles and splats (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7, yang2026effectsofultrasonic pages 11-16). |


*Table: This table identifies which conclusions from the earlier Cu–30Ni assessment are invalid, remain applicable with caveats, or become new risks for C63000 nickel-aluminum bronze.*


References

1. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

2. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

3. (krebs2016thermischesundkinetisches pages 40-43): Sebastian Krebs. Thermisches und kinetisches spritzen von bronzematerialien zum kavitationsschutz im maritimen umfeld. Text, Jan 2016. URL: https://doi.org/10.24405/4294, doi:10.24405/4294. This article has 1 citations and is from a peer-reviewed journal.

4. (schmitz2014surfacetensionof pages 3-7): J. Schmitz, J. Brillo, and I. Egry. Surface tension of liquid al-cu and wetting at the cu/sapphire solid-liquid interface. The European Physical Journal Special Topics, 223:469-479, Feb 2014. URL: https://doi.org/10.1140/epjst/e2014-02103-5, doi:10.1140/epjst/e2014-02103-5. This article has 12 citations.

5. (williams1984thermodynamicsofcoppernickel pages 12-17): R.O. Williams. Thermodynamics of copper-nickel alloys containing aluminum, silicon, titanium, and chromium relative to their use in ceramic brazing. ArXiv, Nov 1984. URL: https://doi.org/10.2172/6243874, doi:10.2172/6243874. This article has 1 citations.

6. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

7. (uhlmann2024acomparativeevaluation pages 13-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

8. (yang2026effectsofultrasonic pages 6-11): Xiao-Feng Yang, Hao-Di Li, Ding-Ying Ren, Hao Lan, Xiao-Qiang Hu, Qian Wang, and Peng Yu. Effects of ultrasonic atomization parameters on the properties of sn-58bi powder and its application in ultrasonic-assisted soldering. Journal of Materials Science: Materials in Electronics, Oct 2026. URL: https://doi.org/10.1007/s10854-026-18683-x, doi:10.1007/s10854-026-18683-x. This article has 0 citations and is from a peer-reviewed journal.

9. (yang2026effectsofultrasonic pages 11-16): Xiao-Feng Yang, Hao-Di Li, Ding-Ying Ren, Hao Lan, Xiao-Qiang Hu, Qian Wang, and Peng Yu. Effects of ultrasonic atomization parameters on the properties of sn-58bi powder and its application in ultrasonic-assisted soldering. Journal of Materials Science: Materials in Electronics, Oct 2026. URL: https://doi.org/10.1007/s10854-026-18683-x, doi:10.1007/s10854-026-18683-x. This article has 0 citations and is from a peer-reviewed journal.

10. (krebs2016thermischesundkinetisches pages 82-84): Sebastian Krebs. Thermisches und kinetisches spritzen von bronzematerialien zum kavitationsschutz im maritimen umfeld. Text, Jan 2016. URL: https://doi.org/10.24405/4294, doi:10.24405/4294. This article has 1 citations and is from a peer-reviewed journal.

11. (timmons2025laserpowderbed pages 1-2): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

12. (timmons2025laserpowderbed pages 2-4): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

13. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

14. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

15. (timmons2025laserpowderbed pages 23-26): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

16. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

17. ([name redacted]2023sphericalpowderscontrol pages 4-4): Michael [name redacted], Dane [name redacted], Jonah [name redacted], Łukasz [name redacted], Bartosz [name redacted], Tomasz [name redacted], Marcin [name redacted], and Steven [name redacted]. Spherical powders: control over the size and morphology of powders for additive manufacturing and enriched stable isotope nuclear targets. EPJ Web of Conferences, 285:03002, Jan 2023. URL: https://doi.org/10.1051/epjconf/202328503002, doi:10.1051/epjconf/202328503002. This article has 10 citations and is from a peer-reviewed journal.

18. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

19. (cashdollar1994flammabilityofmetals pages 4-5): Kenneth L. Cashdollar. Flammability of metals and other elemental dust clouds. Process Safety Progress, 13:139-145, Jul 1994. URL: https://doi.org/10.1002/prs.680130306, doi:10.1002/prs.680130306. This article has 69 citations and is from a peer-reviewed journal.

20. (cashdollar1994flammabilityofmetals pages 1-2): Kenneth L. Cashdollar. Flammability of metals and other elemental dust clouds. Process Safety Progress, 13:139-145, Jul 1994. URL: https://doi.org/10.1002/prs.680130306, doi:10.1002/prs.680130306. This article has 69 citations and is from a peer-reviewed journal.

21. (dust2023section1identification pages 3-4): C Dust. Section 1: identification. Unknown journal, 2023.

22. (dust2023section1identification pages 1-3): C Dust. Section 1: identification. Unknown journal, 2023.

23. (dust2023section1identification pages 7-9): C Dust. Section 1: identification. Unknown journal, 2023.

24. (dust2023section1identification pages 12-14): C Dust. Section 1: identification. Unknown journal, 2023.
