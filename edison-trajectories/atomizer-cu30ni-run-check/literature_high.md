# Edison job-futurehouse-paperqa3-high result: literature_high

**Task ID:** `a67d522e-7d56-4ad9-a324-5d8765ec4423`  
**Status:** success

<details><summary>Query</summary>

```text
We are about to run an AMAZEMET rePOWDER ultrasonic atomizer with its induction-melting module: the
charge is melted in a crucible, then poured through a bottom nozzle, opened by lifting a stopper
("sealing") rod, onto an ultrasonically vibrating plate on the sonotrode inside an argon-filled
chamber. Earlier literature reviews for our lab put the rePOWDER induction module's practical limit
at about 1100-1300 C. So far we have atomized only aluminum alloys on this machine; this is our
first copper-nickel run.

Planned run:
1. Charge: 1.1 kg of 70 wt% Cu / 30 wt% Ni (binary cupronickel, close to UNS C71500 but possibly
   without its Fe and Mn additions). The charge may be pre-alloyed, or elemental Cu plus Ni pieces.
   Liquidus about 1240 C, solidus about 1170 C.
2. Stopper (sealing) rod: hexagonal boron nitride (BN).
3. Crucible: interior coated with BN (base crucible material not confirmed; consider graphite,
   alumina and other common choices).
4. Cleaning: the whole atomization chamber and the powder collection container are wiped with
   Kimwipes and isopropyl alcohol (IPA) beforehand.
5. Ultrasonics: 1:1.5 booster (amplitude gain) with the generator at 100% amplitude.
6. Atomizing surface: a carbon-fiber plate (likely a carbon-carbon composite) dip-coated in
   molybdenum, mounted on the sonotrode.
7. Argon pressures as set on the machine: "melting pressure" 0.1 bar (chamber pressure while
   induction melting), "graining pressure" 0.19 bar (overpressure used while pouring/atomizing to
   push melt through the nozzle), "turbo pressure" 1.5 bar (supply for the turbo / cooling /
   powder-transport gas stream). Our reading of these HMI labels may be imperfect; discuss sensible
   interpretations, including absolute versus gauge pressure.

Identify the problems, failure modes and complications each item could cause, with literature
evidence (and physical or thermodynamic reasoning where the literature is thin), quantified where
possible:

(a) Thermal window: superheat needed for reliable ultrasonic atomization of Cu-30Ni versus a ~1300 C
    induction limit; nozzle freeze-off, skull formation and freezing on the plate; time to dissolve
    Ni (melting point 1455 C) into molten Cu if charged as elemental pieces, and melt homogeneity;
    consequences of the ~70 C freezing range.
(b) BN stopper rod and BN-coated crucible against a Cu-Ni melt at 1250-1350 C: wetting,
    erosion/dissolution, B or N pickup, binder phases in hot-pressed BN (B2O3, calcium borate)
    softening or volatilizing, moisture uptake and outgassing, coating spallation, the stopper
    leaking or sticking in its seat; carbon pickup if the base crucible is graphite (C solubility in
    Cu-Ni).
(c) Molybdenum-dip-coated carbon-fiber plate: Ni-Mo and Cu-Mo interactions (Mo dissolution into
    Ni-containing melts, intermetallics), Mo-C reaction (Mo2C), coating CTE mismatch and spallation
    under ultrasonic loading and thermal shock, Ni attack on carbon fiber where the coating is
    breached, wetting of Cu-Ni on Mo versus carbon, Mo or C contamination of the powder, Mo
    oxidation (volatile MoO3) with residual oxygen, plate damping/heating, resonance-frequency shift
    and fatigue.
(d) Ultrasonic settings: what a 1:1.5 booster at 100% amplitude implies for a dense,
    high-surface-tension melt (Cu-30Ni surface tension ~1.3-1.5 N/m, liquid density ~7.9-8.0 g/cm3):
    median droplet size from Lang's relation at 20-40 kHz, the atomization threshold amplitude, the
    risks of too much amplitude (spatter, coarse droplets, satellites, chaotic breakup, plate
    cracking, generator overload or loss of frequency tracking), and how melt flow rate compares
    with the atomization capacity of the plate (flooding).
(e) Pressures: Cu evaporation and composition shift at 0.1 bar absolute and ~1300 C (vapour
    pressures of Cu versus Ni; Mn loss if C71500-type feedstock containing Mn is used), condensate on
    viewports and the coil; arcing or glow discharge at the induction coil at reduced argon pressure
    (Paschen); whether a ~0.09 bar pressure difference plus metallostatic head overcomes the
    capillary threshold of a non-wetting BN nozzle and what melt flow rate results; effect of a
    1.5 bar gas stream on droplet trajectories, satellite formation, cooling and fines carry-over.
(f) Cleaning with IPA and Kimwipes: residual IPA, water and lint as sources of O, H and C;
    flammability of IPA vapour in the chamber before pumping and inerting; cross-contamination from
    earlier aluminum-alloy runs (Al, Si, Mg, Ce powder left in the chamber or collector).
(g) Powder quality and safety: oxygen pickup, hydrogen porosity in Cu-Ni, expected particle size and
    sphericity compared with published ultrasonic atomization of copper and nickel alloys,
    inhalation and sensitization hazards of nickel-containing powder, combustibility of fine Cu-Ni
    powder when the chamber is vented.
(h) The powder is for a marine/defense application. Does a binary Cu-30Ni meet UNS C71500 or the
    relevant military specification chemistry (Fe, Mn limits), and how do Fe and Mn affect seawater
    corrosion and erosion-corrosion behaviour?

Finish with a table of parameter -> potential problem -> likelihood/severity -> recommended
mitigation or pre-run check, then list which parameters you would change, and to what.

```

</details>

Question: We are about to run an AMAZEMET rePOWDER ultrasonic atomizer with its induction-melting module: the
charge is melted in a crucible, then poured through a bottom nozzle, opened by lifting a stopper
("sealing") rod, onto an ultrasonically vibrating plate on the sonotrode inside an argon-filled
chamber. Earlier literature reviews for our lab put the rePOWDER induction module's practical limit
at about 1100-1300 C. So far we have atomized only aluminum alloys on this machine; this is our
first copper-nickel run.

Planned run:
1. Charge: 1.1 kg of 70 wt% Cu / 30 wt% Ni (binary cupronickel, close to UNS C71500 but possibly
   without its Fe and Mn additions). The charge may be pre-alloyed, or elemental Cu plus Ni pieces.
   Liquidus about 1240 C, solidus about 1170 C.
2. Stopper (sealing) rod: hexagonal boron nitride (BN).
3. Crucible: interior coated with BN (base crucible material not confirmed; consider graphite,
   alumina and other common choices).
4. Cleaning: the whole atomization chamber and the powder collection container are wiped with
   Kimwipes and isopropyl alcohol (IPA) beforehand.
5. Ultrasonics: 1:1.5 booster (amplitude gain) with the generator at 100% amplitude.
6. Atomizing surface: a carbon-fiber plate (likely a carbon-carbon composite) dip-coated in
   molybdenum, mounted on the sonotrode.
7. Argon pressures as set on the machine: "melting pressure" 0.1 bar (chamber pressure while
   induction melting), "graining pressure" 0.19 bar (overpressure used while pouring/atomizing to
   push melt through the nozzle), "turbo pressure" 1.5 bar (supply for the turbo / cooling /
   powder-transport gas stream). Our reading of these HMI labels may be imperfect; discuss sensible
   interpretations, including absolute versus gauge pressure.

Identify the problems, failure modes and complications each item could cause, with literature
evidence (and physical or thermodynamic reasoning where the literature is thin), quantified where
possible:

(a) Thermal window: superheat needed for reliable ultrasonic atomization of Cu-30Ni versus a ~1300 C
    induction limit; nozzle freeze-off, skull formation and freezing on the plate; time to dissolve
    Ni (melting point 1455 C) into molten Cu if charged as elemental pieces, and melt homogeneity;
    consequences of the ~70 C freezing range.
(b) BN stopper rod and BN-coated crucible against a Cu-Ni melt at 1250-1350 C: wetting,
    erosion/dissolution, B or N pickup, binder phases in hot-pressed BN (B2O3, calcium borate)
    softening or volatilizing, moisture uptake and outgassing, coating spallation, the stopper
    leaking or sticking in its seat; carbon pickup if the base crucible is graphite (C solubility in
    Cu-Ni).
(c) Molybdenum-dip-coated carbon-fiber plate: Ni-Mo and Cu-Mo interactions (Mo dissolution into
    Ni-containing melts, intermetallics), Mo-C reaction (Mo2C), coating CTE mismatch and spallation
    under ultrasonic loading and thermal shock, Ni attack on carbon fiber where the coating is
    breached, wetting of Cu-Ni on Mo versus carbon, Mo or C contamination of the powder, Mo
    oxidation (volatile MoO3) with residual oxygen, plate damping/heating, resonance-frequency shift
    and fatigue.
(d) Ultrasonic settings: what a 1:1.5 booster at 100% amplitude implies for a dense,
    high-surface-tension melt (Cu-30Ni surface tension ~1.3-1.5 N/m, liquid density ~7.9-8.0 g/cm3):
    median droplet size from Lang's relation at 20-40 kHz, the atomization threshold amplitude, the
    risks of too much amplitude (spatter, coarse droplets, satellites, chaotic breakup, plate
    cracking, generator overload or loss of frequency tracking), and how melt flow rate compares
    with the atomization capacity of the plate (flooding).
(e) Pressures: Cu evaporation and composition shift at 0.1 bar absolute and ~1300 C (vapour
    pressures of Cu versus Ni; Mn loss if C71500-type feedstock containing Mn is used), condensate on
    viewports and the coil; arcing or glow discharge at the induction coil at reduced argon pressure
    (Paschen); whether a ~0.09 bar pressure difference plus metallostatic head overcomes the
    capillary threshold of a non-wetting BN nozzle and what melt flow rate results; effect of a
    1.5 bar gas stream on droplet trajectories, satellite formation, cooling and fines carry-over.
(f) Cleaning with IPA and Kimwipes: residual IPA, water and lint as sources of O, H and C;
    flammability of IPA vapour in the chamber before pumping and inerting; cross-contamination from
    earlier aluminum-alloy runs (Al, Si, Mg, Ce powder left in the chamber or collector).
(g) Powder quality and safety: oxygen pickup, hydrogen porosity in Cu-Ni, expected particle size and
    sphericity compared with published ultrasonic atomization of copper and nickel alloys,
    inhalation and sensitization hazards of nickel-containing powder, combustibility of fine Cu-Ni
    powder when the chamber is vented.
(h) The powder is for a marine/defense application. Does a binary Cu-30Ni meet UNS C71500 or the
    relevant military specification chemistry (Fe, Mn limits), and how do Fe and Mn affect seawater
    corrosion and erosion-corrosion behaviour?

Finish with a table of parameter -> potential problem -> likelihood/severity -> recommended
mitigation or pre-run check, then list which parameters you would change, and to what.


# Comprehensive Risk Assessment for Cu-30Ni Ultrasonic Atomization on the AMAZEMET rePOWDER

## 1. Introduction

This report identifies the problems, failure modes, and complications associated with atomizing a 1.1 kg charge of Cu-30Ni (70 wt% Cu / 30 wt% Ni) on the AMAZEMET rePOWDER ultrasonic atomizer equipped with its induction-melting module. The analysis draws on published rePOWDER operating data, fundamental thermodynamic and physical reasoning, and the broader ultrasonic atomization and metallurgical literature. The rePOWDER induction module has been documented to operate up to approximately 1300 °C, with ultrasonic frequencies of 35–60 kHz depending on sonotrode configuration, and has been used for Al-Cu, Cu, Ti, Nb, and Mg alloys (ukabhai2025investigationofalcu pages 1-3, ciftcli2025alloydevelopmentfrom pages 1-3, scientific2023comparisonofultrasonic pages 7-8).

---

## (a) Thermal Window

**Superheat margin.** The Cu-30Ni liquidus is approximately 1240 °C, and the rePOWDER induction module's practical ceiling is approximately 1300 °C (ukabhai2025investigationofalcu pages 1-3). This provides only ~60 °C of nominal superheat. Published ultrasonic atomization guidance recommends heating the metal to approximately 1.3–1.5 times its absolute liquidus temperature for optimal atomization (scientific2023comparisonofultrasonic pages 2-4, scientific2023comparisonofultrasonic pages 4-5). For Cu-30Ni (liquidus ~1513 K), this corresponds to 1967–2270 K (1694–1997 °C)—far beyond the induction module's capability. Even the lower end of the recommended range exceeds the 1300 °C limit by nearly 400 °C. The consequence is that the melt will be highly viscous and prone to rapid solidification upon contact with unheated surfaces.

**Nozzle freeze-off.** With only 60 °C superheat, the melt stream passing through the BN nozzle will lose heat rapidly to the ceramic walls and argon atmosphere. Given the ~70 °C freezing range (solidus ~1170 °C, liquidus ~1240 °C), partial solidification in the nozzle is highly probable. The mushy zone will increase apparent viscosity dramatically, choking or completely blocking flow within seconds of stopper rod lifting.

**Skull formation and plate freezing.** Even if the melt exits the nozzle, the Cu-30Ni alloy (density ~7.9–8.0 g/cm³, thermal conductivity ~29 W/m·K in liquid) will lose heat rapidly upon contacting the sonotrode plate. With minimal superheat, the melt may freeze as a skull on the plate surface rather than forming the thin film necessary for capillary-wave-driven atomization (scientific2023comparisonofultrasonic pages 4-5).

**Ni dissolution from elemental charge.** If the charge consists of elemental Cu and Ni pieces rather than pre-alloyed feedstock, the Ni (melting point 1455 °C) cannot melt independently at 1300 °C. Dissolution of solid Ni into liquid Cu is diffusion-controlled and depends on temperature, convection, and piece geometry. At only 60 °C above the alloy liquidus—and well below Ni's melting point—dissolution times could extend to tens of minutes for centimeter-scale pieces. Induction stirring helps, but the risk of an inhomogeneous melt with undissolved Ni fragments is substantial (ciftcli2025alloydevelopmentfrom pages 3-6).

**Freezing range consequences.** The ~70 °C freezing range means that partially solidified (mushy) droplets may exit the plate, producing non-spherical, dendritic, or porous particles rather than the smooth spheres typical of ultrasonic atomization.

---

## (b) BN Stopper Rod and BN-Coated Crucible

**Wetting and chemical compatibility.** Hexagonal BN is generally non-wetting with respect to molten copper (contact angle >130°), which is favorable for containment. However, the 30 wt% Ni content significantly changes the reactivity: nickel can react with BN at elevated temperatures to form nickel borides (Ni₂B, Ni₃B) and release nitrogen. At 1250–1350 °C, this reaction is thermodynamically possible, though kinetically limited for short hold times.

**B₂O₃ binder phases.** Commercial hot-pressed BN typically contains 1–5% B₂O₃ and sometimes calcium borate binders. B₂O₃ softens at ~450 °C and becomes fluid by ~700 °C; above ~1000 °C it volatilizes significantly. At 1250–1350 °C, binder volatilization is essentially complete, potentially creating porosity in the BN body, weakening the stopper rod, and releasing B₂O₃ vapor into the melt. This introduces boron contamination (typically 10–100 ppm B pickup) and generates gas bubbles that can cause hydrogen-like porosity in the powder.

**Moisture uptake.** BN is hygroscopic, absorbing atmospheric moisture to form surface B(OH)₃. At operating temperature, this decomposes to release water vapor and boric acid, both of which introduce oxygen and hydrogen into the melt. Pre-baking at >400 °C under vacuum or inert gas is essential but may not have been planned.

**Coating spallation.** A BN coating on a crucible substrate (whether graphite, alumina, or other ceramic) relies on mechanical adhesion. Differential thermal expansion between BN and the substrate, combined with thermal cycling, can cause spalling. Once the coating is breached, the melt contacts the substrate directly.

**Carbon pickup from graphite substrate.** If the base crucible is graphite, carbon solubility in Cu-Ni melts at 1300 °C is relevant. Pure Cu dissolves negligible carbon (<0.001 wt%), but the addition of 30% Ni significantly increases carbon solubility because Ni-C has much higher mutual solubility. At 1300 °C, a Cu-30Ni melt could dissolve several hundred ppm C from a graphite substrate, leading to carbide precipitation and embrittlement in the solidified powder.

**Stopper rod leaking or sticking.** The BN stopper rod must form a reliable seal against the nozzle seat. Thermal distortion, binder softening, or erosion of the seating surface could cause premature leakage (melt dripping before the sonotrode is started) or, conversely, thermal seizure if a thin skull forms in the nozzle annulus.

---

## (c) Molybdenum-Dip-Coated Carbon-Fiber Plate

**Mo dissolution into Ni-containing melts.** This is the single most critical material-compatibility issue. The Ni-Mo binary system shows that the Ni-rich FCC solid solution can accommodate approximately 17 at% Mo at room temperature, increasing to approximately 27 at% Mo at 1318 °C (shueh1988intermetallicphaseformation pages 35-43). In the liquid state, solubility is even higher. Mo is nearly immiscible with Cu (shueh1988intermetallicphaseformation pages 29-35), but the 30% Ni content creates a powerful driving force for Mo dissolution. A thin dip-coated Mo layer could dissolve into the Cu-30Ni melt within seconds of contact, contaminating the powder with Mo (potentially hundreds to thousands of ppm) and exposing the underlying carbon fiber.

**Ni-Mo intermetallics.** The Ni-Mo system contains several intermetallic compounds including NiMo (β phase), Ni₃Mo, and Ni₄Mo (shueh1988intermetallicphaseformation pages 35-43, sadiq1987nickelbasedsuperalloys pages 57-65). These form readily at elevated temperatures. In Ni-Mo-Cu triads, the β-NiMo phase forms at the Mo interface and can subsequently decompose when Cu penetrates the barrier (shueh1988intermetallicphaseformation pages 174-181). The formation of hard, brittle intermetallic particles on the plate surface could serve as nuclei for crack initiation under ultrasonic fatigue loading.

**Mo₂C formation.** Molybdenum reacts with carbon above ~1100 °C to form Mo₂C (ΔG_f ≈ −50 kJ/mol at 1300 °C). At the Mo/carbon-fiber interface, this reaction would consume both the Mo coating and the carbon substrate, producing a brittle carbide layer that further compromises coating integrity.

**CTE mismatch and spallation.** The CTE of Mo (~5.3 × 10⁻⁶ /K) differs substantially from that of carbon-carbon composites (~1–2 × 10⁻⁶ /K in-plane, variable through-thickness). Under the combined loading of thermal shock from ~1250 °C melt contact and ultrasonic vibration at 20–40 kHz, the thin dip-coated Mo layer is highly susceptible to spallation and delamination.

**Ni attack on exposed carbon fiber.** Once the Mo coating is breached, molten Ni-containing alloy directly contacts the carbon fiber. Nickel catalyzes carbon dissolution and graphitization: carbon solubility in liquid Ni at 1300 °C is approximately 0.5–1.0 wt%. The plate would erode rapidly, introducing carbon particles and fibers into the powder.

**Mo and C contamination of powder.** Both Mo and C contamination are detrimental for a marine/defense Cu-Ni alloy. Mo contamination affects corrosion behavior; carbon contamination produces carbide inclusions that serve as pit-initiation sites in seawater.

**MoO₃ volatilization.** Any residual oxygen in the argon atmosphere will oxidize Mo to MoO₃, which sublimes at ~795 °C. This produces a characteristic yellow condensate on viewports and chamber walls, and releases Mo vapor that can deposit on the powder.

**Resonance frequency shift and fatigue.** The mass of Cu-30Ni melt on the plate (~7.9–8.0 g/cm³, substantially denser than Al at 2.7 g/cm³) will significantly damp the sonotrode and shift its resonance frequency. Ultrasonic generators with auto-frequency tracking can compensate within a limited bandwidth (typically ±500 Hz), but the heavy loading may exceed this range, causing loss of resonance and cessation of atomization (scientific2023comparisonofultrasonic pages 4-5). Cyclic stress from ultrasonic vibration combined with thermal fatigue also creates a risk of plate cracking.

---

## (d) Ultrasonic Settings

**Predicted droplet size from Lang's equation.** The Lang relation D₃₂ = 0.34[8πσ/(ρf²)]^(1/3) is the standard predictor for ultrasonic atomization droplet diameter (brizio2011developmentofa pages 33-37, scientific2023comparisonofultrasonic pages 4-5). For Cu-30Ni properties (σ ≈ 1.3–1.5 N/m, ρ ≈ 7900–8000 kg/m³):
- At f = 20 kHz: D₃₂ ≈ 74–78 µm
- At f = 35 kHz: D₃₂ ≈ 51–54 µm
- At f = 40 kHz: D₃₂ ≈ 46–49 µm

These are liquid-state median diameters; solid-state values would be slightly smaller due to thermal contraction (scientific2023comparisonofultrasonic pages 4-5). The predicted sizes are within the range suitable for powder bed fusion (15–75 µm) if the sonotrode operates at ≥35 kHz.

**1:1.5 booster at 100% amplitude.** The booster amplifies the transducer's output displacement by 1.5×. At 100% generator amplitude, this could produce tip displacements of 30–50 µm peak-to-peak (equipment-dependent). For a dense, high-surface-tension melt, this may exceed the regime of stable capillary-wave breakup and enter chaotic atomization characterized by large irregular ejections, spatter, excessive satellite formation, and bimodal particle size distributions (yang2026effectsofultrasonic pages 11-16). Published work on Sn-58Bi found optimal atomization at 30% amplitude (yang2026effectsofultrasonic pages 1-6), though the much lower density and surface tension of that alloy limit direct comparison.

**Atomization threshold.** The critical amplitude for capillary-wave instability increases with surface tension and density. Cu-30Ni has surface tension approximately 18× that of water and density approximately 8× that of water. The threshold amplitude will therefore be substantially higher than for low-melting alloys, but the exact value is not available from the literature and must be determined experimentally.

**Flooding risk.** If the melt flow rate from the nozzle exceeds the atomization capacity of the plate (which depends on frequency, amplitude, and melt properties), a persistent pool will accumulate. This pool damps vibration, shifts the resonance, and eventually cascades off the plate as large drops rather than fine spherical powder. Given the high density, even modest volumetric flow rates correspond to large mass flow rates.

---

## (e) Pressures

**Interpretation of HMI labels.** The three displayed pressures—"melting pressure" 0.1 bar, "graining pressure" 0.19 bar, and "turbo pressure" 1.5 bar—require careful interpretation. If these are absolute pressures, 0.1 bar absolute (~75 Torr) during melting is a significant partial vacuum. If gauge pressures (above atmospheric), then 0.1 bar gauge ≈ 1.113 bar absolute, which is close to the ~1.1 bar operating pressure documented in published rePOWDER literature (scientific2023comparisonofultrasonic pages 7-8, scientific2023comparisonofultrasonic pages 1-2). The difference is critical: 0.1 bar absolute creates evaporation and arcing hazards, while 1.1 bar absolute is benign. The rePOWDER system has been described as operating at approximately 1.1 bar in argon (scientific2023comparisonofultrasonic pages 1-2), suggesting that the HMI values may be gauge pressures.

**Cu and Ni vapor pressure at 1300 °C.** At 1300 °C (1573 K), the vapor pressure of Cu is approximately 0.01 Pa and that of Ni is approximately 0.001 Pa. Even at 0.1 bar absolute (~10,000 Pa), these vapor pressures are negligible—evaporative composition shift of the Cu-Ni binary is not a concern at this temperature (khalimova2024cuevaporationfrom pages 4-6).

**Mn evaporation.** If the feedstock is C71500-type containing Mn (up to ~1%), the situation is different. Mn has a vapor pressure of approximately 10–100 Pa at 1300 °C, which is 3–4 orders of magnitude higher than Cu or Ni. At reduced pressure (0.1 bar absolute), Mn evaporation would be significant, with losses potentially reaching 10–30% of the initial Mn content within minutes (khalimova2024cuevaporationfrom pages 6-8). Mn condensate would deposit on viewports, the induction coil, and chamber walls.

**Paschen breakdown.** At reduced argon pressure, electrical breakdown between the induction coil turns or between the coil and grounded metalwork is a concern. The Paschen minimum for argon occurs at a pd product of approximately 1 Torr·cm, corresponding to a breakdown voltage of approximately 340 V (burm2008breakdownmagneticfield pages 1-3, chen2025adcdischarge pages 5-9). At 0.1 bar absolute (75 Torr) with coil spacings of a few cm, the pd product would be 75–300 Torr·cm, well to the right of the Paschen minimum, where breakdown voltage increases with pd. However, induction coils operate at elevated AC frequencies (typically 10–400 kHz), and the breakdown mechanism for inductively coupled plasmas differs from DC Paschen behavior: the breakdown magnetic field decreases with increasing frequency, and argon plasma ignition can occur at conditions that DC theory would predict as stable (burm2008breakdownmagneticfield pages 3-4). If the melting pressure is truly 0.1 bar absolute, arcing risk is moderate to high.

**Capillary threshold of the BN nozzle.** For a non-wetting BN nozzle (contact angle θ ≈ 140° for Cu on BN), the capillary pressure opposing flow is P_cap = −2σ cos(θ)/r. For σ ≈ 1.35 N/m and a nozzle radius r ≈ 2 mm: P_cap ≈ 2 × 1.35 × cos(140°) / 0.002 ≈ 1035 Pa ≈ 0.01 bar. The nominal pressure differential of 0.09 bar (if 0.19 − 0.10 bar) plus the metallostatic head of ~1.1 kg over the crucible cross-section (roughly 700–1500 Pa for typical crucible dimensions) should exceed this capillary threshold. However, the margin is modest, and any partial solidification in the nozzle will dramatically increase the effective resistance to flow.

**1.5 bar turbo/transport gas.** A 1.5 bar gas supply (whether gauge or absolute) driving the cooling/transport gas stream creates a high-velocity flow in the atomization chamber. For the dense Cu-Ni powder, this is beneficial for rapid cooling and spheroidization, but may blow fine particles (<10 µm) past the cyclone collector, reducing yield of the finest fraction. Satellite formation from particle-particle collisions in the gas stream is also enhanced at higher gas velocities.

---

## (f) Cleaning with IPA and Kimwipes

**IPA flammability.** Isopropyl alcohol has a flash point of 12 °C and a lower explosive limit (LEL) of 2 vol% in air. If the chamber is wiped with IPA and then sealed before the solvent has fully evaporated, the resulting IPA-air mixture inside the chamber could be within the explosive range. Ignition could occur from the induction coil, electrical connections, or static discharge during argon purging. The correct procedure is to allow complete evaporation with the chamber open, then perform multiple vacuum/argon purge cycles (ukabhai2025investigationofalcu pages 3-7).

**Residual O, H, and C.** IPA (C₃H₈O) residue introduces carbon, hydrogen, and oxygen. Even a few milligrams of residual IPA, decomposing at operating temperature, can contribute measurable oxygen pickup (tens of ppm) and hydrogen porosity in Cu-Ni powder. Kimwipes are cellulose-based and shed fibers (lint) that similarly decompose to CO, CO₂, H₂O, and carbonaceous residue.

**Cross-contamination from Al-alloy runs.** Previous aluminum alloy atomization campaigns will have deposited Al, Si, Mg, and possibly Ce powder throughout the chamber, collection system, cyclone, filters, and dead spaces. Even after wiping, residual powder trapped in crevices, threads, gasket grooves, and downstream ducting can contaminate the Cu-Ni batch. Al and Si contamination is particularly problematic: Al₂O₃ inclusions in Cu-Ni powder degrade mechanical properties and corrosion resistance. A thorough mechanical cleaning with HEPA-filtered metal-powder vacuum, followed by swab testing for Al/Mg/Si by XRF or ICP, should precede the Cu-Ni run.

---

## (g) Powder Quality and Safety

**Oxygen pickup.** Copper and nickel are both susceptible to oxygen dissolution from residual moisture, oxide skins on feedstock, and imperfect inerting. Published rePOWDER data for Ti alloys show oxygen pickup of approximately 220 ppm relative to feedstock (ciftcli2025alloydevelopmentfrom pages 3-6). For Cu-Ni, which has lower oxygen affinity than Ti, oxygen pickup may be lower, but residual moisture from BN components and IPA cleaning can still raise oxygen to problematic levels. Target oxygen for AM-grade Cu-Ni powder should be <500 ppm.

**Hydrogen porosity.** Copper dissolves hydrogen readily in the liquid state (~5 ppm at 1 atm H₂, 1300 °C) and rejects it on solidification, forming spherical gas pores. Sources of hydrogen include moisture in BN, IPA residue, and atmospheric humidity. The rapid solidification inherent in ultrasonic atomization may trap hydrogen as fine porosity within particles, degrading powder density and mechanical properties of built parts.

**Particle size and sphericity.** Based on the Lang equation predictions (brizio2011developmentofa pages 33-37, scientific2023comparisonofultrasonic pages 4-5) and published rePOWDER results (ukabhai2025investigationofalcu pages 3-7), the expected median particle size is approximately 46–78 µm depending on frequency (20–40 kHz). Ultrasonic atomization generally produces high sphericity (circularity >0.9) and narrow particle size distributions compared to gas atomization (scientific2023comparisonofultrasonic pages 1-2), though the limited superheat and high melt density may reduce sphericity relative to lower-melting alloys.

**Nickel inhalation and sensitization hazards.** Nickel compounds are classified as Group 1 carcinogens (IARC) for inhalation exposure. Metallic nickel powder is classified as Group 2B (possibly carcinogenic). The ACGIH TLV-TWA for inhalable nickel is 1.5 mg/m³; the respirable fraction limit is 0.2 mg/m³. Nickel is also a potent skin sensitizer—repeated dermal contact can cause allergic contact dermatitis that persists lifelong. Fine Cu-30Ni powder requires handling with P100 respiratory protection, nitrile gloves (not latex), safety glasses, and local exhaust ventilation. The powder should be treated as a respiratory sensitizer in the lab safety data sheet.

**Combustibility.** Fine metallic Cu-Ni powder (<75 µm) is combustible in air, though Cu-Ni alloys are less pyrophoric than aluminum or titanium. The minimum ignition energy is substantially higher than for Al, but dust cloud explosions are still possible. When venting the chamber after a run, the powder should not be exposed to air currents that could generate a dispersed dust cloud. An inert-gas blanket should be maintained during powder transfer.

---

## (h) Specification Compliance: Binary Cu-30Ni vs. UNS C71500

**Chemistry requirements.** UNS C71500 (ASTM B171, MIL-C-15726, etc.) specifies: Cu balance, Ni 29.0–33.0%, Fe 0.40–1.0%, Mn 1.0% max (typically 0.5–1.0% nominal), C 0.05% max, Si 0.05% max, S 0.02% max, P 0.02% max, Zn 0.5% max, Pb 0.02% max. A binary Cu-30Ni alloy without deliberate Fe and Mn additions does not meet UNS C71500 and cannot be certified to military specifications.

**Role of Fe and Mn in seawater corrosion.** Iron and manganese are not merely incidental impurities; they are functionally essential alloying elements. Iron is incorporated into the protective Cu₂O/Cu(OH)₂ corrosion film that forms on Cu-Ni alloys in seawater, improving film adherence, density, and protectiveness. Without controlled Fe content, the corrosion film is porous and non-protective, leading to accelerated general corrosion and pitting (konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 142-149). Mn serves as a deoxidant during melting and also improves corrosion resistance and hot workability. However, excessive Fe (or poorly distributed Fe precipitates) can also promote localized attack, so the Fe content must be controlled within the specified range (konynenburg1990backgroundstudiesin pages 149-155).

**Erosion-corrosion behavior.** The 70-30 Cu-Ni alloy has a maximum recommended seawater velocity of approximately 3.0 m/s (10 ft/s), compared with 2.4 m/s (8 ft/s) for 90-10 Cu-Ni (janikowski2008selectingtubingmaterials pages 9-11). This superior erosion-corrosion resistance is attributed to both the higher Ni content and the Fe/Mn-stabilized protective film. Without Fe and Mn, the binary alloy's erosion-corrosion resistance would be significantly inferior to specification-compliant C71500. In water-droplet impingement testing, 70-30 Cu-Ni has a relative erosion resistance of 0.8 (normalized to titanium Grade 2 = 1.0) at a hardness of 135 HV (janikowski2008selectingtubingmaterials pages 9-11).

**Recommendation.** For a marine/defense application, procure certified C71500-compliant pre-alloyed feedstock with controlled Fe and Mn content rather than attempting to add these elements ad hoc during a small-batch ultrasonic atomization run.

---

## Risk Assessment Summary Table

The following table consolidates all identified failure modes with their assessed likelihood, severity, and recommended mitigations:

| Parameter/Item | Potential Problem | Likelihood | Severity | Recommended Mitigation or Pre-Run Check |
|---|---|---|---|---|
| **(a) Thermal window** | 1300°C limit vs ~1240°C liquidus provides only ~60°C superheat. Ideal ultrasonic atomization requires 1.3-1.5x absolute melting temperature (scientific2023comparisonofultrasonic pages 2-4). | High | High | Switch to the arc-melting module (>3500°C) (ukabhai2025investigationofalcu pages 1-3) or use a lower-melting Cu alloy. |
| **(a) Thermal window** | Nozzle freeze-off. Low superheat causes rapid solidification in the unheated BN nozzle during pouring. | High | High | Preheat the nozzle if possible; increase "graining pressure" to force melt through faster. |
| **(a) Thermal window** | Skull formation / plate freezing. Sluggish melt freezes upon contacting the sonotrode plate, halting atomization. | High | High | Hold at maximum 1300°C before pouring; ensure sonotrode is operating before melt impact. |
| **(a) Thermal window** | Ni dissolution kinetics. Elemental Ni (Tm 1455°C) may fail to fully dissolve into the 1300°C Cu melt within the short hold time. | Med | Med | Use pre-alloyed Cu-30Ni feedstock instead of elemental Cu and Ni pieces. |
| **(b) BN Crucible/Stopper** | Wetting and erosion. While non-wetting to Cu, high Ni content at elevated temperatures can react with BN. | Low | Med | Limit melt hold time; inspect BN coating and stopper rod for degradation post-run. |
| **(b) BN Crucible/Stopper** | Binder outgassing. B2O3 binders in hot-pressed BN soften at ~450°C and volatilize >1000°C, releasing gas into the melt. | Med | Med | Perform a high-temperature, high-vacuum bake-out of the crucible and stopper before the run. |
| **(b) BN Crucible/Stopper** | Moisture uptake. BN absorbs atmospheric moisture, generating H2O/H2 outgassing leading to porosity and oxidation. | Med | High | Store BN components in a desiccator; strictly enforce the pre-run vacuum bake-out cycle. |
| **(c) Mo-Coated C/C Plate** | Mo dissolution into Ni melt. Molybdenum has high solid solubility in Nickel (~17-27 at%) and rapidly dissolves into Ni-containing melts (shueh1988intermetallicphaseformation pages 35-43). | High | High | Do not use Mo-coated plates for Ni alloys; switch to a ceramic (alumina/zirconia) plate. |
| **(c) Mo-Coated C/C Plate** | Carbon attack and Mo2C formation. Once the Mo coating dissolves, Ni will attack the underlying carbon composite. | High | High | Discard the Mo-coated C/C plate for this run; procure a non-reactive refractory plate. |
| **(c) Mo-Coated C/C Plate** | Coating spallation. Extreme CTE mismatch between Mo and carbon fiber combined with ultrasonic fatigue and thermal shock. | Med | Med | Inspect coating pre-run; avoid rapid thermal cycling if this plate must be used. |
| **(c) Mo-Coated C/C Plate** | Resonance shift and damping. The dense Cu-30Ni melt dampens plate vibration, potentially shifting resonance frequency out of generator range. | Med | High | Ensure generator has auto-frequency tracking; test resonance with a proxy fluid first. |
| **(d) Ultrasonic Settings** | Amplitude too high. 100% amplitude + 1:1.5 booster on a dense, high-surface-tension melt risks chaotic breakup, spatter, and satellites. | High | Med | Start at 30-50% amplitude and increase gradually until stable atomization is achieved (yang2026effectsofultrasonic pages 1-6). |
| **(d) Ultrasonic Settings** | Plate flooding. Melt flow rate from the nozzle exceeds the atomization capacity of the vibrating plate. | Med | High | Reduce "graining pressure" or use a smaller nozzle diameter to mechanically restrict melt flow. |
| **(d) Ultrasonic Settings** | Droplet size mismatch. Lang's equation predicts ~46-78 µm at 20-40 kHz; this may not match desired powder specs. | Low | Low | Evaluate if the predicted D50 meets requirements; change sonotrode frequency if a different size is needed. |
| **(e) Pressures** | Evaporation. While Cu/Ni vapor pressure is low at 1300°C, any volatile impurities (e.g., Zn, Mn) will rapidly evaporate at 0.1 bar (khalimova2024cuevaporationfrom pages 6-8). | Med | Med | Backfill Argon to ~0.5-0.8 bar during melting if volatile elements are present. |
| **(e) Pressures** | Paschen breakdown (arcing). 0.1 bar (75 Torr) Ar near high-voltage induction coils severely risks glow discharge / electrical arcing (burm2008breakdownmagneticfield pages 1-3). | Med | High | Increase "melting pressure" to ~0.5-1.0 bar to stay safely above the Paschen minimum for Argon. |
| **(e) Pressures** | Capillary threshold. 0.09 bar differential (0.19 minus 0.10) plus metallostatic head may not overcome a non-wetting BN nozzle. | Med | High | Ensure sufficient melt volume (1.1 kg is good); increase graining pressure immediately if flow stalls. |
| **(e) Pressures** | Fines carry-over. 1.5 bar "turbo" gas stream may blow fine Cu-Ni powder past the collector into the filtration/exhaust system. | High | Low | Optimize cyclone settings; tune the turbo gas pressure to balance cooling vs. powder recovery. |
| **(f) Cleaning** | IPA flammability & contamination. IPA flash point is 12°C. Vapors can ignite or introduce massive C/H/O contamination into the chamber. | High | High | Allow full IPA evaporation with door open; perform a deep, prolonged vacuum purge before heating. |
| **(f) Cleaning** | Cross-contamination. Lint from Kimwipes (C, H, O) or residual Al/Mg/Si/Ce from prior runs contaminates the Cu-Ni powder. | High | Med | Use cleanroom polyester lint-free wipes; physically abrade and scrub chamber walls thoroughly. |
| **(g) Powder Quality/Safety** | Gas porosity. Oxygen and hydrogen picked up from moisture, lint, or IPA residues cause internal porosity in the solidifying droplets. | Med | Med | Maximize vacuum purge cycles; use high-purity (5N) Argon and thoroughly dried feedstock. |
| **(g) Powder Quality/Safety** | Ni inhalation hazard. Nickel powder is a known carcinogen and sensitizer. | High | High | Operators must wear P100/N95 respirators, nitrile gloves, and use proper local exhaust when venting/cleaning. |
| **(h) Specification** | Missing Fe and Mn. Binary Cu-30Ni fails UNS C71500 specs. Fe and Mn are essential for seawater corrosion film stability and erosion resistance (konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 142-149). | High | High | Add 0.4-1.0 wt% Fe and ~1.0 wt% Mn to the feedstock if the powder is intended for actual marine defense use. |


*Table: A comprehensive risk assessment table detailing potential failure modes, likelihood, severity, and mitigation strategies across all subsystems of the AMAZEMET rePOWDER atomizer for a Cu-30Ni run.*

## Recommended Parameter Changes

Based on the analysis above, the following parameter changes are recommended before attempting the Cu-30Ni run:

| Parameter | Current Setting | Recommended Change | Rationale |
|---|---|---|---|
| Melting module | Induction module; practical ceiling approximately 1300 °C | **Do not run the full 1.1 kg charge until AMAZEMET confirms continuous operation at 1300 °C with Cu–30Ni.** If unavailable, use a higher-temperature, bottom-pour-compatible module or externally prepare the alloy and conduct a reduced-mass qualification run. | A 1240 °C liquidus leaves only about 60 °C nominal superheat at the module limit, before nozzle and transfer losses. Published rePOWDER information identifies an approximately 1300 °C induction limit, while stable atomization generally benefits from appreciably greater superheat (scientific2023comparisonofultrasonic pages 2-4, ukabhai2025investigationofalcu pages 1-3). |
| Melt temperature and hold | Target approximately 1250–1300 °C; hold unspecified | Target **1290–1300 °C measured in the liquid**, minimize the post-homogenization hold, and verify temperature calibration with a suitable pyrometer or sacrificial thermocouple trial. Abort if the measured temperature falls below a validated pour threshold. | Low superheat increases viscosity, nozzle freeze-off, skull formation, and freezing on the plate; long holds increase refractory attack and contamination. Temperature strongly affects spreading and atomization stability (yang2026effectsofultrasonic pages 11-16, scientific2023comparisonofultrasonic pages 4-5). |
| Feedstock | Either pre-alloyed Cu–30Ni or elemental Cu plus Ni pieces | Use **certified pre-alloyed Cu–30Ni**, preferably clean shot or small pieces with known O, C, S, Fe, Mn, Al, Si, Mg, B, Mo, and hydrogen-related quality. Do not use elemental Ni pieces for the first run. | Nickel melts at 1455 °C; at a 1300 °C furnace ceiling it must dissolve rather than melt independently. Dissolution time becomes geometry- and convection-dependent, creating incomplete dissolution and segregation risks. |
| Qualification charge | Full 1.1 kg first Cu–Ni run | First run a **small engineering charge permitted by the OEM**, then section the retained button or skull and analyze top, middle, and bottom chemistry before committing 1.1 kg. | A staged trial limits damage if the nozzle freezes, the plate coating fails, or melt chemistry changes. rePOWDER literature demonstrates alloy-dependent process behavior and the need to tailor temperature and nozzle conditions (ciftcli2025alloydevelopmentfrom pages 3-6). |
| Atomizing plate | Dip-coated Mo on carbon–carbon composite | Replace it with an **OEM-qualified plate specifically validated for molten Cu–30Ni at 1300 °C and the installed frequency**. Do not substitute alumina, zirconia, or another plate without acoustic qualification. | Mo is nearly immiscible with Cu but interacts strongly with Ni: Ni-rich solid solution accepts substantial Mo and Ni–Mo compounds can form. A coating breach also exposes carbon, while thermal shock and ultrasonic strain can spall a dip coating and detune the assembly (shueh1988intermetallicphaseformation pages 35-43, shueh1988intermetallicphaseformation pages 174-181, shueh1988intermetallicphaseformation pages 29-35). |
| Ultrasonic amplitude | 1:1.5 booster; generator at 100% | Determine actual calibrated tip displacement, then begin at the **lowest OEM-approved atomizing amplitude—provisionally 30–50%—and ramp only until continuous atomization is obtained**. Establish a hard limit from generator load and frequency-tracking data. | “100%” is not a transferable displacement value; with a 1.5-gain booster it may impose excessive plate stress, spatter, satellites, and tracking loss. Published low-melting-alloy work found an optimum at 30%, but this is a starting precedent, not a Cu–Ni setpoint (yang2026effectsofultrasonic pages 1-6). |
| Melt delivery rate | Controlled indirectly by nozzle and “graining pressure” | Conduct a **cold-flow or lower-temperature surrogate calibration**, then use the smallest stable pressure differential and/or OEM-approved nozzle that keeps only a thin replenished film on the plate. Stop if a persistent pool forms. | Atomization capacity is finite; excessive feed floods and damps the plate, whereas too little pressure permits freeze-off. Earlier work recommends changing nozzle diameter to obtain stable flow at lower temperature (ciftcli2025alloydevelopmentfrom pages 3-6). |
| Melting pressure | HMI value 0.1 bar; absolute/gauge meaning uncertain | Before changing the number, verify the HMI definition against the P&ID/manual and an independent absolute gauge. If it is **0.1 bar absolute**, request OEM approval to melt nearer the normal validated argon pressure rather than at deep sub-atmospheric pressure; if **0.1 bar gauge**, retain only after confirming relief and vessel ratings. | Absolute and gauge interpretations differ by about 1 bar. Reduced-pressure argon can increase volatile-element transport and alter induction-discharge behavior; inductive breakdown depends on pressure, frequency, and geometry rather than on a simple DC Paschen curve alone (khalimova2024cuevaporationfrom pages 4-6, burm2008breakdownmagneticfield pages 1-3, burm2008breakdownmagneticfield pages 3-4). |
| Graining pressure | HMI value 0.19 bar; presumed pouring overpressure | Verify whether it is absolute, gauge, or a regulated setpoint. Control and record the **actual pressure above the melt and chamber pressure separately**, beginning with the minimum differential that starts stable flow; do not assume the displayed difference is 0.09 bar. | If both values are absolute in the same reference, the nominal differential is 9 kPa, but mixed references invalidate that calculation. Flow also depends on nozzle diameter and length, contact angle, viscosity, metallostatic head, and partial obstruction. |
| Turbo/transport gas | HMI value 1.5 bar | Confirm whether 1.5 bar is supply pressure or chamber pressure and whether it is gauge or absolute. Begin with the **OEM baseline for dense Cu-alloy powder**, then tune using collector mass balance, filter differential pressure, and fines recovery rather than pressure alone. | Gas transport affects cooling, trajectories, particle collisions, satellite formation, and fines carry-over. Published ultrasonic systems use inert-gas cooling and separation, but equipment pressures and flow paths are configuration-specific (scientific2023comparisonofultrasonic pages 7-8, scientific2023comparisonofultrasonic pages 2-4). |
| BN stopper, coating, and base crucible | BN stopper and BN-coated crucible; BN grade and substrate unknown | Obtain BN grade, binder chemistry, coating cure schedule, and crucible substrate certification. Dry or bake components within supplier limits, inspect the stopper seat and nozzle bore, perform a room-temperature leak/lift test, and prefer a **dense non-carbon crucible system qualified for Cu–Ni**. | Unknown binders, retained moisture, coating cracks, or a graphite substrate can cause outgassing, spallation, leakage, sticking, and B/C contamination. Limiting high-temperature contact time reduces refractory attack. |
| Cleaning and prior-run contamination | Kimwipes and IPA after Al-alloy campaigns | Remove loose powder first with an approved HEPA metal-powder vacuum; use low-lint polyester wipes and reagent-grade IPA only where compatible; allow complete evaporation, then perform validated evacuation/argon purge cycles. Swab-test the chamber, collector, cyclone, and filter path for Al, Mg, Si, and Ce. | Cellulose lint and residual solvent contribute C/H/O, while prior Al-alloy residues can contaminate the batch. Published rePOWDER work uses evacuation and repeated argon preparation to limit oxidation (ukabhai2025investigationofalcu pages 3-7). |
| Alloy chemistry | Binary 70Cu–30Ni, or unspecified C71500-type material | For qualification to UNS C71500 or a defense procurement specification, purchase **certified specification-compliant feedstock** rather than adding Fe/Mn ad hoc. Verify the governing product-form specification and heat analysis; typical C71500 chemistry includes controlled Fe and Mn, but exact limits must come from the invoked specification revision. | A binary Cu–30Ni heat should not be represented as C71500. Controlled Fe/Mn additions support marine performance, while excessive or poorly distributed Fe can promote localized attack; 70–30 Cu–Ni also has better allowable seawater-flow performance than 90–10 Cu–Ni (konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 142-149, janikowski2008selectingtubingmaterials pages 9-11). |


*Table: Recommended changes and verification steps for the first Cu–30Ni rePOWDER run. The table prioritizes thermal margin, material compatibility, pressure interpretation, contamination control, and specification compliance.*

## Critical Parameters to Change (Priority Order)

1. **Atomizing plate material** (CRITICAL): Do not use the Mo-dip-coated carbon-fiber plate for Cu-30Ni. The Ni content will dissolve the Mo coating rapidly (shueh1988intermetallicphaseformation pages 35-43), exposing carbon fiber to further attack. Procure a plate material that is inert to both Cu and Ni at 1250–1350 °C and acoustically qualified for the installed sonotrode. Consult AMAZEMET for their recommended plate for Cu-Ni alloys.

2. **Feedstock** (CRITICAL): Use pre-alloyed, specification-compliant Cu-30Ni (with Fe and Mn if C71500 compliance is required) rather than elemental Cu + Ni pieces. Elemental Ni cannot melt at 1300 °C and dissolution kinetics are uncertain (ciftcli2025alloydevelopmentfrom pages 3-6).

3. **Ultrasonic amplitude** (HIGH): Reduce from 100% to 30–50% initially and ramp up empirically. The combination of 1.5× booster gain and 100% amplitude on a dense, high-surface-tension melt risks chaotic breakup, spatter, and generator overload (yang2026effectsofultrasonic pages 1-6, yang2026effectsofultrasonic pages 11-16).

4. **Melting pressure interpretation** (HIGH): Verify whether 0.1 bar is absolute or gauge. If absolute, increase to ≥0.5 bar absolute to reduce Paschen breakdown risk (burm2008breakdownmagneticfield pages 1-3). Published rePOWDER data indicate normal operation at ~1.1 bar, suggesting these may be gauge values (scientific2023comparisonofultrasonic pages 7-8).

5. **BN component preparation** (MODERATE): Bake out BN stopper rod and crucible coating at >400 °C under vacuum or argon before the run to remove moisture and volatile binder phases.

6. **Cleaning protocol** (MODERATE): Replace Kimwipes with lint-free polyester wipes; ensure complete IPA evaporation before sealing; HEPA-vacuum the chamber; swab-test for Al/Si/Mg contamination from prior runs (ukabhai2025investigationofalcu pages 3-7).

7. **Alloy composition** (HIGH for end-use): Add 0.4–1.0% Fe and ~1.0% Mn to the feedstock if the powder must meet UNS C71500 for marine/defense service (konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 142-149, janikowski2008selectingtubingmaterials pages 9-11).

8. **Run staging** (MODERATE): Conduct a small-mass engineering trial before committing the full 1.1 kg charge, to verify nozzle flow, plate integrity, and atomization stability (ciftcli2025alloydevelopmentfrom pages 3-6).

In summary, this run pushes the rePOWDER induction module to its thermal limits while simultaneously introducing severe material-compatibility challenges with the Mo-coated C/C sonotrode plate. The most probable failure mode is a combination of nozzle freeze-off (due to insufficient superheat) and rapid dissolution of the Mo coating by the Ni-containing melt. Both issues should be resolved before proceeding. The specification question—whether a binary Cu-30Ni meets C71500—is unambiguously negative: Fe and Mn additions are required for both specification compliance and functional seawater corrosion performance.

References

1. (ukabhai2025investigationofalcu pages 1-3): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

2. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

3. (scientific2023comparisonofultrasonic pages 7-8): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

4. (scientific2023comparisonofultrasonic pages 2-4): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

5. (scientific2023comparisonofultrasonic pages 4-5): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

6. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

7. (shueh1988intermetallicphaseformation pages 35-43): Y Shueh. Intermetallic phase formation and breakdown of mo diffusion barriers in ni-mo-cu and ni-mo-monel 400 diffusion triads. Unknown journal, 1988.

8. (shueh1988intermetallicphaseformation pages 29-35): Y Shueh. Intermetallic phase formation and breakdown of mo diffusion barriers in ni-mo-cu and ni-mo-monel 400 diffusion triads. Unknown journal, 1988.

9. (sadiq1987nickelbasedsuperalloys pages 57-65): S SADIQ. Nickel based superalloys containing. Unknown journal, 1987.

10. (shueh1988intermetallicphaseformation pages 174-181): Y Shueh. Intermetallic phase formation and breakdown of mo diffusion barriers in ni-mo-cu and ni-mo-monel 400 diffusion triads. Unknown journal, 1988.

11. (brizio2011developmentofa pages 33-37): PJ Brizio. Development of a novel humidifier for air breathing devices. Unknown journal, 2011.

12. (yang2026effectsofultrasonic pages 11-16): Xiao-Feng Yang, Hao-Di Li, Ding-Ying Ren, Hao Lan, Xiao-Qiang Hu, Qian Wang, and Peng Yu. Effects of ultrasonic atomization parameters on the properties of sn-58bi powder and its application in ultrasonic-assisted soldering. Journal of Materials Science: Materials in Electronics, Oct 2026. URL: https://doi.org/10.1007/s10854-026-18683-x, doi:10.1007/s10854-026-18683-x. This article has 0 citations and is from a peer-reviewed journal.

13. (yang2026effectsofultrasonic pages 1-6): Xiao-Feng Yang, Hao-Di Li, Ding-Ying Ren, Hao Lan, Xiao-Qiang Hu, Qian Wang, and Peng Yu. Effects of ultrasonic atomization parameters on the properties of sn-58bi powder and its application in ultrasonic-assisted soldering. Journal of Materials Science: Materials in Electronics, Oct 2026. URL: https://doi.org/10.1007/s10854-026-18683-x, doi:10.1007/s10854-026-18683-x. This article has 0 citations and is from a peer-reviewed journal.

14. (scientific2023comparisonofultrasonic pages 1-2): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

15. (khalimova2024cuevaporationfrom pages 4-6): Galiia Khalimova, Mykyta Levchenko, Hans-Peter Markus, Dariusz Sosin, Thilo Kreschel, and Olena Volkova. Cu evaporation from liquid iron alloy in stream. Metals, 14:1233, Oct 2024. URL: https://doi.org/10.3390/met14111233, doi:10.3390/met14111233. This article has 3 citations.

16. (khalimova2024cuevaporationfrom pages 6-8): Galiia Khalimova, Mykyta Levchenko, Hans-Peter Markus, Dariusz Sosin, Thilo Kreschel, and Olena Volkova. Cu evaporation from liquid iron alloy in stream. Metals, 14:1233, Oct 2024. URL: https://doi.org/10.3390/met14111233, doi:10.3390/met14111233. This article has 3 citations.

17. (burm2008breakdownmagneticfield pages 1-3): Karel Burm. Breakdown magnetic field in an inductively coupled plasma. Physics Letters A, 372:6280-6283, Oct 2008. URL: https://doi.org/10.1016/j.physleta.2008.08.037, doi:10.1016/j.physleta.2008.08.037. This article has 23 citations and is from a peer-reviewed journal.

18. (chen2025adcdischarge pages 5-9): You-Hsuan Chen, Ting Wang, and Pi-Sin Chen. A dc discharge plasma experiment for undergraduate laboratories. ArXiv, Dec 2025. URL: https://doi.org/10.48550/arxiv.2512.10259, doi:10.48550/arxiv.2512.10259. This article has 0 citations.

19. (burm2008breakdownmagneticfield pages 3-4): Karel Burm. Breakdown magnetic field in an inductively coupled plasma. Physics Letters A, 372:6280-6283, Oct 2008. URL: https://doi.org/10.1016/j.physleta.2008.08.037, doi:10.1016/j.physleta.2008.08.037. This article has 23 citations and is from a peer-reviewed journal.

20. (ukabhai2025investigationofalcu pages 3-7): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

21. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

22. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

23. (janikowski2008selectingtubingmaterials pages 9-11): Daniel S. Janikowski. Selecting tubing materials for power generation heat exchangers. Materials Performance, 47:58-63, Sep 2008. URL: https://doi.org/10.5006/mp2008\_47\_9-58, doi:10.5006/mp2008\_47\_9-58. This article has 27 citations and is from a peer-reviewed journal.
