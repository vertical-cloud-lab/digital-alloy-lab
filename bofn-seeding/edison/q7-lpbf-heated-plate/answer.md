## LPBF Processing of Nine Aluminium Alloy Families on the Aconity MIDI: Literature-Based Starting Windows, Build-Plate Heating Effects, and Experimental Design Guidance

---

### 1. Published Aconity Machine Parameters for Aluminium Alloys

The principal group operating aluminium alloys on Aconity platforms is the **University of Innsbruck, Department of Mechatronics, Chair of Materials Science** (Schimbäck, Kaserer, Mair, Riener, Leichtfried, Pogatscher and co-workers). Their Aconity MIDI is equipped with a 1000 W Yb:YAG laser and a resistive build-platform heater rated to 800 °C (schimback2024advancementsinmetal pages 2-3, schimback2022animprovedprocess pages 3-4).

**Scalmalloy® on Aconity MIDI** (measured): P = 370 W, v = 1000 mm/s, h = 100 µm, t = 30 µm, bilinear stripe pattern (5 mm stripe width), 67° rotation, argon atmosphere. Two build-plate conditions were investigated: no heating (NoBPH) and 200 °C (BPH). The 200 °C condition was specifically designed to promote in-situ Al–Sc–Zr solute-cluster formation during the build, yielding high as-built strength without subsequent heat treatment (schimback2024advancementsinmetal pages 2-3, schimback2022animprovedprocess pages 3-4). Process absorption for thermal simulation was set to 0.5 with a Goldak heat-source radius of 70 µm and depth of 100 µm (schimback2024advancementsinmetal pages 2-3).

**Al–Mn–Ti–Zr on Aconity MIDI** (measured, same group): P = 380 W, v = 1900 mm/s, h = 100 µm, t = 30 µm, 67° rotation stripe scan, no preheat. This produced crack-free specimens with as-built YS = 284 ± 3 MPa, UTS = 320 ± 1 MPa, and elongation 16.9 ± 0.2% (mair2022microstructuralfeaturesand pages 1-2).

**AlSi40 on Aconity Mini** (measured, Wilsnack et al.): 200 W max laser, 20–63 µm powder, substrate preheating at 400 °C (initially tested at 500 °C, which induced defect accumulation). Build chamber Ø98 × 130 mm³ (wilsnack2023fabricationofan pages 1-3).

**6182 on AconityONE** (measured, Riener et al.): Four 700 W Nd:YAG lasers, nitrogen atmosphere. A d-optimal DOE varying power, speed, hatch, focus position and preheat from 200–500 °C was performed. The 500 °C condition produced crack-free, fully equiaxed specimens with density >99.0% (riener2022processabilityofhighstrength pages 1-2, riener2022processabilityofhighstrength pages 10-12). DOI: 10.1007/s00170-022-08673-8.

**Other Aconity Al users**: Politecnico di Milano (Aconity MIDI+ for multi-material with pyrometer monitoring) (schimback2022animprovedprocess pages 3-4) and additional thesis work using Aconity MIDI for defect characterization of aluminium alloys.

---

### 2. Crack-Free, >99.5% Dense Process Windows per Alloy Family

The following table compiles starting process windows for 200–400 W machines with 70–100 µm spots, distinguishing measured data from extrapolations. With 20–63 µm (D50 ≈ 45–55 µm) powder and 30–50 µm layers on the Aconity MIDI, recommended starting conditions are:

| Alloy family | Layer (µm) | Power (W) | Speed (mm/s) | Hatch (µm) | VED (J/mm³) | Plate T (°C) | Expected density (%) | Main failure mode | Direct-aging schedule | Key references |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| **1. AlSi10Mg** | 30 | 350–370 | 1300–1650 | 120–130 | 54–79 | 25–100 | >99.5 | Low energy: lack of fusion/balling; high energy: keyhole and hydrogen pores. Heating near 200 °C relieves stress but coarsens the Si network and lowers strength. | Direct age 160–180 °C for 6–12 h; alternatively alloy-specific T6. | Measured AlSi10Mg process-mode window and preheat response; MIDI values are a starting extrapolation. (clement2024investigationintothe pages 43-51, macias2020influenceonmicrostructure pages 1-5, leis2021processwindowfor pages 1-2) |
| **2. Scalmalloy-type Al–Mg–Sc–Zr** | 30 | 370 | 1000 | 100 | 123 | 200 beneficial; 25 if maximum supersaturation is wanted | >99.5 expected | Mg evaporation, condensate/spatter-induced lack of fusion, and keyhole pores at excessive normalized heat input. | 325 °C/4 h; approximately 172 HV, 468 MPa YS and 517 MPa UTS reported. A 200 °C plate can provide partial in-situ clustering/ageing. | **Measured on Aconity MIDI**, 1000 W laser installation; bilinear 5 mm stripes. (schimback2024advancementsinmetal pages 2-3, schimback2022animprovedprocess pages 3-4, cerri2024mainheattreatments pages 14-16, mehta2021laserpowderbed pages 10-11) |
| **3. Al–Mn–Cr–Zr / Al–Mn–Ti–Zr** | 30 | 170–380 | 1000–1900 | 100 | 30–67 | 25–100 | ≈99.5 to >99.7 | Primarily lack of fusion or keyholing rather than intrinsic cracking; high plate temperature risks loss of Mn/Cr/Zr supersaturation. | Al–Mn–Cr–Zr: 350 °C/24 h or 375 °C/14 h; peak ≈142–143 HV. | Measured examples include 170 W/1500 mm/s/100 µm and Al–Mn–Ti–Zr at 380 W/1900 mm/s/100 µm without preheat. (martucci2022theinfluenceof pages 2-4, mair2022microstructuralfeaturesand pages 1-2, mehta2022effectofprecipitation pages 1-3, mehta2023advancingnovelalmncrzr pages 1-3) |
| **4. Al–Mg–Zr, Addalloy-type** | 30 | 330–370 | 900–1200 | 110–130 | 71–125 | 25–100 | >99 expected; verify experimentally | Mg evaporation, unstable melt pool and spatter-induced lack of fusion; cracking if primary Al₃Zr nucleation is insufficient. | Screen 350–400 °C for 4–8 h; schedule is an **extrapolation** from reduced-Sc Al–Mg–Zr–Sc alloys and requires hardness-time verification. | Centre condition is extrapolated from related Al–Mg–Sc/Zr and Er/Zr alloys; reduced-Sc material reached 160 HV after 350 °C/24 h. (belelli2022investigationandcharacterization pages 8-14, guo2022microstructureandmechanical pages 1-2) |
| **5. Al–Fe–Zr (Aheadd CP1-type) / Al–Fe–Mg–Zr** | 30–60 | 350–380 | 1200–1600 | 100–130 | 30–106 | 100 for CP1; 25–100 for Fe–Mg–Zr | >99.7; 99.8 measured for Fe–Mg–Zr | Gas/keyhole porosity and incomplete overlap; excessive Mg increases evaporation porosity. Intrinsic hot cracking is low near the Al–Fe eutectic. | 400 °C/4 h: CP1 ≈310 MPa YS; Al–Fe–Mg–Zr ≈376 MPa YS and 406 MPa UTS. | CP1 measured at 370 W, 1400 mm/s, 130 µm, 60 µm and 100 °C; Fe–Mg–Zr window measured over 200–380 W and 600–2600 mm/s. (pauzon2022anovellaser pages 1-4, li2025precipitationevolutionaging pages 1-3, li2025precipitationevolutionaging pages 3-4) |
| **6. High-Mg Al–Mg–Si(–Mn), eutectic-type** | 30 | 300–370 | 800–1300 | 100–130 | 59–154 | Begin at 100–200; test 300–500 only if cracks persist | >99 possible only with suitable eutectic chemistry or grain refinement; **unverified on MIDI** | Solidification/liquation cracking, Mg evaporation, hydrogen porosity and powder caking at high preheat. | Composition-specific: screen 160–200 °C for Mg₂Si ageing; avoid assigning a final schedule before DSC/hardness curves. | MIDI centre is an extrapolation. High-temperature preheat suppresses cracking in 6xxx only near 500 °C but may reduce density and as-built strength. (li2024additivemanufacturingof pages 31-34, bradfordvialva2021developmentofa pages 113-115, riener2022processabilityofhighstrength pages 10-12) |
| **7. Al–Mg–Er–Zr(–Mn)** | 30 | 350 | 1000 | 130 | 90 | 25–100 | >99.5 expected when Zr/Er produces adequate grain refinement; verify | Cracking when Er/Zr content or primary Al₃(Er,Zr)/Al₃Zr nuclei are insufficient; Mg evaporation at excessive energy. | Screen 325, 350 and 375 °C for 3–8 h; published alloy reached 440 MPa YS, 520 MPa UTS and 15.5% elongation after optimized ageing. | Processing set of 350 W/1000 mm/s/130 µm/30 µm was measured on an SLM 280; transfer to MIDI is an extrapolation. (guo2022microstructureandmechanical pages 1-2, guo2022microstructureandmechanical pages 2-3) |
| **8. Zr-modified 7xxx and 2xxx** | 30 | 300–370 | 800–1300 | 100–130 | 59–154; initially constrain to ≈60–90 | 100–200 for refined variants; 400–500 only as a controlled high-preheat trial | >99.5 may be achievable with effective refiners; conventional chemistry can remain cracked regardless of apparent density | Solidification and liquation cracking, Zn/Mg/Cu segregation, Zn/Mg evaporation and keyhole porosity. In unmodified 7075, 100–200 °C did not suppress cracks and 400 °C produced columnar crack networks. | Composition-specific T6/T7 after density and cracking qualification; direct ageing alone is unlikely to restore optimum properties universally. | **Starting extrapolation**, not a published universal window. Unmodified 7075 lost ≈1 wt.% Zn and 0.3 wt.% Mg; high preheat alone was ineffective. (velikajne2026influenceofbase pages 6-8, velikajne2026influenceofbase pages 8-11, velikajne2026influenceofbase pages 1-2) |
| **9. Al–Ce and Al–Ni eutectic alloys** | 30–45 | 200–365 | 800–1500 | 90–110 | 30–169; target ≈40–80 initially | 25–100 | >99.5 expected for near-eutectic compositions; verify | Low-energy lack of fusion; high-energy keyhole/gas pores. Hot-cracking susceptibility is generally low, but off-eutectic primary intermetallics can embrittle the alloy. | Usually no conventional age-hardening response; use stress relief or chemistry-specific precipitation treatment only after hardness screening. | Al–Ce study used 200 W/30 µm and 365 W/45 µm regimes, 68 µm spot, 67° rotation, argon and O₂ <0.01 vol.%; speeds/hatches here are starting extrapolations. (hesselmann2022effectofprecipitationforming pages 3-5) |


*Table: Recommended first-pass LPBF settings for nine aluminium-alloy families using an approximately 80 µm spot and 20–63 µm powder. The table distinguishes directly measured conditions from machine-transfer extrapolations and identifies the principal qualification risks.*

**Effect of 50 µm layers and coarser powder:** Increasing layer thickness from 30 to 50 µm generally requires higher power or slower speed to maintain melt-pool depth ≥ 1.5× layer thickness. The Al–Cr–Mo–Sc–Zr study demonstrated successful processing at 100 µm layer thickness with build rates of ~47 cm³/h, though at higher laser power and with correspondingly adjusted hatch spacing (agricola2025parameterstudyof pages 1-2). For the Al–Fe–Zr CP1 alloy, 60 µm layers with 370 W and 1400 mm/s achieved >99.7% density (pauzon2022anovellaser pages 1-4). Coarser powder (D50 ~50 µm) tends to produce rougher layers and may require lower recoating speed; the process window generally narrows because the thicker effective layer reduces melt-pool overlap. The AlSi10Mg process window scales with the ratio P/d_b, where the optimum range was identified as P/d_b = 2000–5200 W/mm, centered around 3000–3500 W/mm for key-bowl melting with low porosity (leis2021processwindowfor pages 1-2).

---

### 3. Build-Plate Heating: Per-Family Effects

| Alloy family | No preheat (~25 °C) | 100–200 °C | 300–500 °C | Best plate temperature | Net assessment |
|---|---|---|---|---:|---|
| **1. AlSi10Mg** | Dense and crack-tolerant; finest cellular Al–Si network and highest as-built strength, but greater residual stress/distortion. | Strong stress relief: residual stress fell from about **50 MPa to negligible at 200 °C**. However, α-Al cells and Si precipitates coarsen, the Si network thickens and loses connectivity, and strength falls; fracture strain was approximately unchanged. | At ≥300 °C, rapid Si-network fragmentation, spheroidization and coarsening progressively soften the alloy; prolonged exposure risks over-ageing. | **25–100 °C** | **Indifferent to mild heating; harmed by high heating.** Use ~100 °C only when distortion control outweighs maximum as-built strength. (macias2020influenceonmicrostructure pages 1-5, bosio2021laserpowderbed pages 43-47, macias2020influenceonmicrostructure pages 5-9) |
| **2. Scalmalloy-type Al–Mg–Sc–Zr** | Normally prints crack-free and retains maximum Sc/Zr supersaturation for subsequent direct ageing, but with higher residual stress. | **200 °C is beneficial:** demonstrated on an Aconity MIDI as an in-situ thermal treatment promoting dense Al–Sc–Zr solute clusters and high strength directly after LPBF. | 300–350 °C accelerates Al₃(Sc,Zr) precipitation and can approach peak ageing; prolonged or ≥400 °C exposure causes precipitate coarsening/over-ageing. | **200 °C** | **Benefits from heating.** Best-supported family for deliberate in-situ ageing during the build. (schimback2024advancementsinmetal pages 1-2, schimback2024advancementsinmetal pages 2-3, cerri2024mainheattreatments pages 11-14, cerri2024mainheattreatments pages 14-16) |
| **3. Al–Mn–Cr–Zr / Al–Mn–Ti–Zr** | Preferred: preserves high Mn/Cr/Zr supersaturation; crack-free Al–Mn–Ti–Zr was demonstrated without substrate preheating. | May reduce residual stress, but long builds can begin consuming supersaturation and reduce the later age-hardening reserve; direct evidence for a density benefit is limited. | Temperatures near **350–405 °C** enter the intended ageing range: Al–Mn and Al₃Zr precipitation raises hardness, but uncontrolled in-build residence creates height-dependent properties and eventual coarsening. | **25–100 °C** | **Generally harmed by sustained heating** if uniform post-build ageing and maximum supersaturation are priorities. (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10, mair2022microstructuralfeaturesand pages 1-2, mehta2022effectofprecipitation pages 1-3, mehta2023advancingnovelalmncrzr pages 1-3) |
| **4. Al–Mg–Zr, Addalloy-type** | Generally printable when sufficient primary Al₃Zr provides grain refinement; maximizes supersaturation but retains residual stress. | Likely useful for stress relief, but may initiate Zr clustering/precipitation and height-dependent ageing; quantitative plate-temperature evidence is sparse. | Enters the Al₃Zr ageing regime; may strengthen during short exposure but prolonged heating sacrifices supersaturation. High temperature also aggravates Mg loss and powder caking. | **25–100 °C** | **Largely indifferent to mild heating; avoid high heating.** Recommendation is extrapolated from related Al–Mg–Zr–Sc/Er alloys. (belelli2022investigationandcharacterization pages 8-14, guo2022microstructureandmechanical pages 1-2, guo2022microstructureandmechanical pages 2-3) |
| **5. Al–Fe–Zr (Aheadd CP1-type) / Al–Fe–Mg–Zr** | Expected to be intrinsically crack-resistant near the Al–Fe eutectic; residual stress is the main reason to heat rather than crack avoidance. | **100 °C is a measured CP1 baseline:** 370 W, 1400 mm/s, 130 µm hatch and 60 µm layers gave **>99.7% density**. No evidence establishes a need for 200 °C. | About **400 °C** is an effective post-build ageing temperature: CP1 reached about **310 MPa YS**, while Al–Fe–Mg–Zr reached **376 MPa YS** after 4 h. Applying it throughout a build risks nonuniform ageing and powder sintering. | **100 °C** | **Indifferent; mild heating is prudent.** Higher temperature should be reserved for controlled post-build ageing. (pauzon2022anovellaser pages 1-4, li2025precipitationevolutionaging pages 1-3, li2025precipitationevolutionaging pages 3-4) |
| **6. High-Mg Al–Mg–Si(–Mn), eutectic/6xxx-type** | Conventional broad-freezing-range chemistry suffers severe hot cracking; eutectic redesign or grain refiners can reduce this sensitivity. | Reduces thermal gradients but usually does not eliminate cracking; 6061 at 200 °C reached **98.72% density**, yet microcracks remained. | For unmodified 6061/6182-type alloys, approximately **500 °C** can be decisive: Uddin et al. reported crack-free 6061, and 6182 became fully equiaxed and crack-free with density up to **99.0%**. Density may decline through pore coalescence, and powder caking/oxidation become serious. | **500 °C only for unmodified crack-prone chemistry; 100–200 °C for grain-refined/eutectic-designed variants** | **Needs high heating only when chemistry is not intrinsically printable.** Prefer grain refinement/eutectic redesign over routine 500 °C operation. (li2024additivemanufacturingof pages 31-34, bradfordvialva2021developmentofa pages 113-115, riener2022processabilityofhighstrength pages 10-12) |
| **7. Al–Mg–Er–Zr(–Mn)** | A sufficiently Zr/Er-rich composition can be crack-free while retaining maximum supersaturation for ageing; insufficient nucleant content leaves cracks. | Plausibly promotes early Al₃(Er,Zr) clustering and lowers stress, but a quantitative plate-heating study was not identified. Treat any strengthening claim as extrapolation from Scalmalloy. | 325–375 °C is the useful post-build precipitation range; prolonged in-build exposure can create nonuniform core–shell Al₃(Er,Zr) precipitation, while high temperature aggravates Mg evaporation and caking. | **25–100 °C** | **Indifferent to mild heating; avoid high in-build ageing.** Published processability derives mainly from chemistry rather than plate heat. (guo2022microstructureandmechanical pages 1-2, guo2022microstructureandmechanical pages 2-3) |
| **8. Zr-modified 7xxx and 2xxx** | Conventional alloys crack severely; effective Zr-based grain refinement can improve printability, but process optimization alone is rarely sufficient. | Unmodified 7075 showed **no significant crack-density reduction at 100 or 200 °C**. Lower thermal gradients do not remove segregation-driven hot cracking. | At **400 °C**, 7075 developed columnar crack networks, stress relaxed and hardness fell to **117 ± 6 HV0.5 transverse / 83 ± 7 HV0.5 parallel**; loss remained about **1 wt.% Zn and 0.3 wt.% Mg**. Heating at 200–400 °C also failed to guarantee crack-free 2xxx. | **100–200 °C with proven grain refiners; otherwise no reliable plate-only solution** | **Preheat alone is ineffective and high heating can be harmful.** Use Zr/Ti/ceramic nucleants or eutectic modification first; validate any 400–500 °C trial cautiously. (li2024additivemanufacturingof pages 31-34, velikajne2026influenceofbase pages 6-8, velikajne2026influenceofbase pages 8-11, velikajne2026influenceofbase pages 1-2) |
| **9. Al–Ce and Al–Ni eutectic alloys** | Near-eutectic solidification gives intrinsically low hot-cracking susceptibility; room-temperature processing is normally adequate. | May reduce stress/distortion but offers no established density or cracking advantage and may begin coarsening the fine eutectic architecture. | Generally unnecessary; prolonged high temperature coarsens the strengthening intermetallic network. High preheat also raises powder-sintering/caking risk without solving a primary printability problem. | **25–100 °C** | **Indifferent; potentially harmed at high temperature.** Preserve the rapidly solidified eutectic architecture unless stress control requires mild heating. (hesselmann2022effectofprecipitationforming pages 3-5, li2025precipitationevolutionaging pages 3-4) |


*Table: Quantitative comparison of how ambient, moderate, and high build-plate temperatures affect cracking, residual stress, ageing response, density, and microstructural stability across the nine aluminium-alloy families. Recommendations distinguish measured behavior from family-level extrapolation.*

**Key quantitative results:**

**(a) Solidification and liquation cracking:**
- AlSi10Mg: inherently crack-free regardless of preheat.
- 6182 at 500 °C: fully equiaxed grains (mean ECD 19.46 µm vs 33.72 µm at 200 °C), crack-free (riener2022processabilityofhighstrength pages 10-12). At 400 °C, initial equiaxed formation appeared (ECD 25.35 µm) but crack elimination was incomplete.
- 7075: preheating at 25, 100, 200, and 400 °C was systematically studied. At 200 °C, neither crack density nor grain morphology changed significantly. At 400 °C, crack networks transitioned to columnar morphology, but cracks were not eliminated (velikajne2026influenceofbase pages 6-8, velikajne2026influenceofbase pages 8-11, velikajne2026influenceofbase pages 1-2). DOI: 10.3390/ma19050970.
- 6061 at 500 °C (Uddin et al.): crack-free parts achieved, but as-built mechanical properties were low (YS ≈ 60 MPa, UTS ≈ 130 MPa, elongation 15%). After T6 treatment, strength recovered to YS ≈ 280–290 MPa and UTS ≈ 310–315 MPa, with reduced elongation (3.5–5.4%) (li2024additivemanufacturingof pages 31-34, bradfordvialva2021developmentofa pages 113-115).

**(b) Density and hydrogen porosity:**
- AlSi10Mg at 150 °C showed higher measured porosity (1.7% vs 0.9% at ambient) (zhu2023microstructuralanalysisof pages 3-5).
- 6182 at 500 °C: maximum density 99.0%, but density generally decreased with increasing preheat due to pore coalescence via Ostwald ripening (riener2022processabilityofhighstrength pages 10-12).
- For hydrogen porosity, all Al alloys benefit from powder drying (353 K/4 h documented for Al–Mn–Cr–Zr) (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10).

**(c) Residual stress and distortion:**
- AlSi10Mg: at 200 °C, residual stress dropped from ~50 MPa (tensile) to negligible (macias2020influenceonmicrostructure pages 1-5).
- 7075 at 400 °C: pronounced stress relaxation, with GROD (grain reference orientation deviation) maps indicating substantially lower internal strain (velikajne2026influenceofbase pages 8-11).

**(d) As-built strength (in-situ ageing effects):**
- AlSi10Mg at 200 °C: Si-rich eutectic network coarsened and thickened, the heat-affected zone doubled in thickness, and strength decreased relative to no-preheat builds (macias2020influenceonmicrostructure pages 1-5, macias2020influenceonmicrostructure pages 5-9).
- Scalmalloy at 200 °C: in-situ cluster formation produced high as-built strength without post-treatment, eliminating the need for the standard 325 °C/4 h ageing step (schimback2024advancementsinmetal pages 1-2, schimback2024advancementsinmetal pages 2-3).
- Al–Mn–Cr–Zr: elevated platform temperatures risk consuming the Mn/Cr/Zr supersaturation intended for post-build direct ageing. Peak aging temperatures are 350–405 °C; uncontrolled exposure during long builds creates height-dependent properties (mehta2022effectofprecipitation pages 1-3, mehta2022effectofprecipitation pages 5-7).

**(e) Mg and Zn evaporation:**
- Scalmalloy: Mg burn-off is directly linked to normalized heat input; keyhole mode shows up to 1.2 wt% Mg loss vs 0.3 wt% in heat-conduction mode (schimback2022animprovedprocess pages 3-4). DOI: 10.2139/ssrn.4201040.
- 7075: approximately 1 wt% Zn and 0.3 wt% Mg were lost regardless of preheating temperature (25–400 °C) (velikajne2026influenceofbase pages 1-2).

**(f) Powder caking and sintering:**
- At ≥400 °C, Al powder sintering becomes significant, particularly for high-Mg alloys. AlSi40 at 500 °C on the Aconity Mini showed defect accumulation in lower layers, improved at 400 °C (wilsnack2023fabricationofan pages 1-3). Powder reuse after high-preheat builds requires careful re-sieving and characterization.

---

### 4. Setting a First Print Window for Novel Alloys

**Normalized enthalpy and keyhole threshold:** The normalized enthalpy is defined as β = AP / [ρ h_s √(π α v σ³)], where A is absorptivity, P is laser power, ρ is density, h_s is the heat content to reach melting, α is thermal diffusivity, v is scan speed, and σ is the Gaussian beam parameter (hong2026fittingfreediagnosisof pages 4-5). Melt-pool aspect ratio d/(w/2) classifies regimes: <1 conduction, 1–2 transition, >2 keyhole (hong2026fittingfreediagnosisof pages 4-5). For aluminium alloys, aim for the transition zone (key-bowl melting) for maximum efficiency and minimum porosity.

**Eagar–Tsai / Rosenthal models:** The Rosenthal point-source solution applies when beam radius r_b ≪ thermal diffusion distance; the Eagar–Tsai extension handles finite Gaussian beams by numerical integration of the temperature field, with melt-pool boundaries located at the liquidus isotherm via root-finding (hong2026fittingfreediagnosisof pages 4-5, francis2017theeffectsof pages 67-70). These models omit temperature-dependent properties and latent heat but are computationally fast and accurate to within a few percent in the conduction regime (hong2026fittingfreediagnosisof pages 4-5). For high-conductivity aluminium, the Rosenthal solution is especially applicable because conductive heat extraction is the dominant transport mechanism (bajaj2020precipitationduringintrinsic pages 60-63, bajaj2020precipitationduringintrinsic pages 58-60).

**Absorptivity values for Al alloys:** Bulk aluminium absorptivity at 1064 nm is ~0.06–0.12; powder absorptivity increases to ~0.2–0.4 due to multiple reflections. For thermal simulation of Scalmalloy on the Aconity MIDI, an absorption coefficient of 0.5 was used with a Goldak heat source (schimback2024advancementsinmetal pages 2-3). In the transition/keyhole regime, effective absorptivity can rise to 0.5–0.7 through multiple reflections within the vapour depression (hong2026fittingfreediagnosisof pages 4-5, martucci2023developmentandcharacterisation pages 21-23). A practical starting assumption: use A ≈ 0.3–0.4 for conduction-mode estimates and A ≈ 0.5 for Goldak-type simulations.

**Alloy thermal conductivity effects:** High-conductivity dilute alloys (e.g., Al–Fe–Zr with ~180 W/m·K after ageing) require higher linear energy for equivalent melt-pool depth. Mn/Cr/Fe-rich alloys with lower thermal conductivity (~120–160 W/m·K) have wider process windows because heat is retained in the melt pool longer (pauzon2022anovellaser pages 1-4, mehta2022effectofprecipitation pages 1-3).

**Mg/Zn vapour pressure effects:** High-vapour-pressure elements narrow the window toward lower energy inputs to minimize evaporation. The optimum for Scalmalloy lies in conduction-to-transition mode; keyhole mode causes up to 1.2 wt% Mg loss and melt-pool instability (schimback2022animprovedprocess pages 3-4). For 7075, Zn loss of ~1 wt% is essentially unavoidable at conventional LPBF parameters (velikajne2026influenceofbase pages 1-2).

**Balling/humping limits:** At high speeds with insufficient line energy, the melt track becomes discontinuous (balling). AlSi10Mg showed that P/d_b < 2000 W/mm leads to partial failure and balling (leis2021processwindowfor pages 1-2). This corresponds approximately to P < 160 W for an 80 µm spot.

---

### 5. Efficient Experimental Design with Scarce Powder (100–300 g)

**Three-stage protocol:**

**Stage 1 – Single scan tracks (SSTs):** Print single tracks on a bare substrate or thin powder layer, varying laser power (3–5 levels) and scan speed (5–8 levels) in a grid. Each track is ~10–20 mm long and consumes negligible powder. Assess track continuity, width, and depth from cross-sections. This identifies the stable P–v window and can be used to estimate hatch spacing from geometric overlap criteria (martucci2023developmentandcharacterisation pages 20-21, martucci2023developmentandcharacterisation pages 83-100, bertoli2018processstructurepropertiesrelationshipsin pages 35-39, bertoli2018processstructurepropertiesrelationshipsin pages 20-26).

**Stage 2 – Small density cubes:** Use 5–10 mm cubes (10 × 10 × 10 mm³ is a standard; each cube ~2.7 g for Al). A fractional factorial or Taguchi L9/L16 design with 3 factors (power, speed, hatch) at 2–3 levels requires 9–16 cubes (~24–43 g). Include 2–3 replicates at the centre point. Measure density by Archimedes or image analysis (chia2022processparameteroptimization pages 11-13, yadegari2025aluminumlaseradditive pages 19-21).

**Stage 3 – Sub-size tensile bars:** ASTM E8 sub-size specimens (gauge 25 × 6 × 6 mm or thinner, ~6–8 g each). Three tensile bars minimum per condition require ~18–24 g. SS-J2 miniature specimens (~0.5 mm thick, ~12 mm gauge) can be used if material is extremely limited; note that SS-J2/SS-T geometries may slightly overestimate ductility and yield strength relative to full-size bars (juhasz2020inandexsitu pages 104-109). Alternatively, miniature dog-bones with 11.5 × 3.5 × 1 mm gauge section were demonstrated for the Al–Fe–Mg–Zr alloy (li2025precipitationevolutionaging pages 3-4).

**Powder budget estimate per alloy:** ~15 g for SSTs + ~40 g for cubes (16 × ~2.5 g) + ~30 g for 3 tensile bars + ~40 g for powder losses (filling, sieving) ≈ **~125 g minimum** for density + hardness + 3 tensile values. With 200–300 g, a second condition (e.g., different VED or plate temperature) is feasible.

**Reduced build-volume inserts:** Use a small-diameter build insert (Ø50–80 mm available for the Aconity MIDI's Ø170 mm platform) to reduce powder bed volume and waste.

**DOE approaches:** Taguchi L9 (3 factors, 3 levels, 9 runs), Taguchi L16 (up to 5 factors, 2 levels, 16 runs), or Central Composite Design (3 factors, 15–20 runs including axials and centre points) are efficient (chia2022processparameteroptimization pages 11-13, yadegari2025aluminumlaseradditive pages 19-21). A compact 12–20 condition DOE around the starting-table centre point should vary power (±15–20%), speed (±20–30%), and hatch (±15%), holding layer thickness constant at 30 µm initially.

---

### 6. Scan Strategy and Other Critical Settings

**Scan rotation:** 67° layer-to-layer rotation is the near-universal standard for Al LPBF, documented for Scalmalloy, Al–Mn–Ti–Zr, Al–Mn–Cr–Zr, Al–Fe–Zr CP1, Al–Ce, and Al–Mg–Er–Zr alloys (hesselmann2022effectofprecipitationforming pages 3-5, mair2022microstructuralfeaturesand pages 1-2, pauzon2022anovellaser pages 1-4, guo2022microstructureandmechanical pages 1-2).

**Stripe vs chessboard:** Stripe (island) scanning with 5–10 mm strip width is standard; shorter scan vectors reduce residual stress. The Scalmalloy study on the Aconity MIDI used bilinear 5 mm stripes and found that restricting scan vector angle relative to the gas flow direction is important to reduce vapour-plume/laser interaction and spatter (schimback2024advancementsinmetal pages 2-3, schimback2022animprovedprocess pages 3-4).

**Oxygen level:** Maintain O₂ < 100–500 ppm (0.01–0.05 vol%). Al–Ce alloy processing used O₂ < 0.01 vol% (hesselmann2022effectofprecipitationforming pages 3-5). Lower oxygen is particularly critical for high-Mg alloys where oxide formation at the melt surface affects wetting and spatter.

**Gas flow:** Argon flow must be sufficient to clear the metal vapour plume and spatter from the processing zone. For Scalmalloy, Mg condensate deposits along the gas flow direction; scan vector orientation relative to gas flow affects Mg burn-off and spatter redeposition (schimback2022animprovedprocess pages 3-4).

**Recoater type:** Flexible rubber-lip or silicone recoaters are preferred for coarser or less flowable ultrasonically atomized powders. Rigid steel blades can displace or streak irregular particles.

**Powder drying:** Drying at 80 °C (353 K) for 4 h before printing is documented for Al–Mn–Cr–Zr powders and reduces hydrogen porosity from moisture-adsorbed hydroxyl groups (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10). All Al powders should be dried, particularly high-Mg compositions where moisture promotes both hydrogen porosity and oxide growth.

**Powder oxygen content:** Higher oxygen content (from oxide shells on particles) affects melt-pool wetting and oxide inclusion formation. Ultrasonically atomized powder in an inert atmosphere should target O < 0.1 wt%; the Al–Fe–Zr CP1 powder contained 0.098 wt% O (pauzon2022anovellaser pages 1-4).

---

### 7. Direct-Ageing Schedules per Alloy Family

| Alloy family | Ageing schedule | As-built → Peak-aged properties | Stress relief? |
|---|---|---|---|
| AlSi10Mg | Direct age 160–180 °C/6–12 h, or T6 (500 °C/2 h + WQ + 180 °C/12 h) | As-built: UTS ~430–480 MPa, elongation 4–10%. T6 reduces strength but increases elongation to ~12–22% | Optional 300 °C/2 h SR reduces residual stress but begins Si coarsening (bosio2021laserpowderbed pages 90-93, juhasz2020inandexsitu pages 104-109) |
| Scalmalloy Al–Mg–Sc–Zr | **325 °C/4 h** (standard) | As-built: YS 256–278 MPa, UTS 349–350 MPa, ε 19–20%. After 325 °C/4 h: **YS 456–469 MPa, UTS 512–521 MPa, ε 12–13%**, HV ~172 | Not needed if 200 °C platform used; otherwise implicit (cerri2024mainheattreatments pages 14-16, mehta2021laserpowderbed pages 10-11, cerri2024mainheattreatments pages 1-2) |
| Al–Mn–Cr–Zr | **350 °C/24 h** or **375 °C/14 h** | As-built: ~102–104 HV. Peak: **~142–143 HV**; YS ~340 MPa, UTS ~440 MPa for best quaternary variants | Direct ageing serves as stress relief; slow precipitation kinetics allow flexibility (mehta2022effectofprecipitation pages 1-3, mehta2023advancingnovelalmncrzr pages 1-3, mehta2022effectofprecipitation pages 5-7) |
| Al–Mg–Zr (Addalloy) | Screen 350–400 °C/4–24 h | Reduced-Sc variant: 105 → 160 HV at 350 °C/24 h. Sc-free: lower peak, verify experimentally | Direct ageing includes stress relief (belelli2022investigationandcharacterization pages 8-14) |
| Al–Fe–Zr CP1 | **400 °C/4 h** | As-built: modest strength. After ageing: **YS ~310 MPa, thermal conductivity ~180 W/m·K** | 300 °C/2 h SR before base-plate removal is standard practice (pauzon2022anovellaser pages 1-4) |
| Al–Fe–Mg–Zr | **400 °C/4 h** | As-built: YS ~218 MPa, UTS 310 MPa. After 400 °C/4 h: **YS ~376 MPa, UTS ~406 MPa, ε 11.1%** | Direct ageing inherently stress-relieves (li2025precipitationevolutionaging pages 1-3, li2025precipitationevolutionaging pages 3-4) |
| Al–Mg–Er–Zr | Screen 325–375 °C/3–8 h | Published: **YS 440 ± 3 MPa, UTS 520 ± 2 MPa, ε 15.5%** (optimized composition after ageing) | Direct ageing serves as stress relief (guo2022microstructureandmechanical pages 1-2, guo2022microstructureandmechanical pages 2-3) |
| 7xxx/2xxx Zr-modified | Composition-dependent T6/T7 | Conventional 7075-T6: YS ~500 MPa; LPBF rarely matches this due to cracking and Zn/Mg loss. Verify feasibility before specifying schedule | Stress relief at 100–200 °C before removal; solution treatment only if crack-free (li2024additivemanufacturingof pages 31-34, velikajne2026influenceofbase pages 6-8) |
| Al–Ce / Al–Ni eutectic | Limited conventional ageing response; some Al–Ce–Ni–Ti–Zr alloys may respond to 300–400 °C treatment | Stress relief at 200–300 °C if needed; intermetallic architecture is set during solidification (hesselmann2022effectofprecipitationforming pages 3-5) | Optional SR only |

---

### 8. Recommended Starting Table and Compact DOE

The recommended starting parameters for the nine families on the Aconity MIDI with 20–63 µm powder are presented in the table above (artifact-00). To build a compact 12–20 condition DOE around each centre point:

**Suggested 16-condition fractional factorial per alloy (2^(4-1) = 8 main + 4 centre + 4 axial):**
- Factor A: Laser power (centre ± 15%, e.g., 315 / 370 / 425 W for Scalmalloy)
- Factor B: Scan speed (centre ± 25%, e.g., 750 / 1000 / 1250 mm/s)
- Factor C: Hatch spacing (centre ± 20%, e.g., 80 / 100 / 120 µm)
- Factor D: Plate temperature (2 levels: RT and recommended preheat)
- Layer thickness fixed at 30 µm
- Responses: relative density (image analysis on XZ cross-section), microhardness, crack density, melt-pool dimensions

**Build layout estimate:** 8 cubes (10 × 10 × 10 mm) + 4 centre-point replicates + 3 tensile bars per best condition ≈ ~105 g of Al per alloy, feasible within 200–300 g budget using a reduced-diameter build insert.

**Measurement priorities:** (1) Relative density by optical image analysis ≥ 6 images per orientation; (2) Vickers hardness HV0.3; (3) Crack density measurement for crack-prone families; (4) Tensile testing on best-density condition.

---

### Key References with DOIs

- Schimbäck et al. 2024, in-situ heat treatment of Al alloys on Aconity MIDI: DOI 10.1016/j.msea.2024.146102 (schimback2024advancementsinmetal pages 2-3)
- Schimbäck et al. 2022, improved scan strategy for Scalmalloy on Aconity MIDI: DOI 10.2139/ssrn.4201040 (schimback2022animprovedprocess pages 3-4)
- Mair et al. 2022, Al-Mn-Ti-Zr alloy: DOI 10.1016/j.jallcom.2021.163156 (mair2022microstructuralfeaturesand pages 1-2)
- Riener et al. 2022, 6182 on AconityONE at 500 °C: DOI 10.1007/s00170-022-08673-8 (riener2022processabilityofhighstrength pages 1-2, riener2022processabilityofhighstrength pages 10-12)
- Pauzon et al. 2022, Al-Fe-Zr CP1: DOI 10.1016/j.scriptamat.2022.114878 (pauzon2022anovellaser pages 1-4)
- Mehta et al. 2022, Al-Mn-Cr-Zr: DOI 10.1557/s43578-022-00533-1 (mehta2022al–mn–cr–zrbasedalloystailored pages 10-10, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3)
- Mehta et al. 2022, precipitation kinetics Al-Mn-Cr-Zr: DOI 10.1016/j.jallcom.2022.165870 (mehta2022effectofprecipitation pages 1-3, mehta2022effectofprecipitation pages 5-7)
- Mehta et al. 2023, advancing Al-Mn-Cr-Zr: DOI 10.1016/j.jallcom.2023.171685 (mehta2023advancingnovelalmncrzr pages 1-3)
- Macías et al. 2020, AlSi10Mg platform temperature: DOI 10.1016/j.actamat.2020.10.001 (macias2020influenceonmicrostructure pages 1-5, macias2020influenceonmicrostructure pages 5-9)
- Leis et al. 2021, AlSi10Mg process window: DOI 10.18419/opus-11716 (leis2021processwindowfor pages 1-2)
- Hesselmann et al. 2022, Al-Ce alloy: DOI 10.1016/j.addma.2022.102959 (hesselmann2022effectofprecipitationforming pages 3-5)
- Velikajne et al. 2026, 7075 preheat: DOI 10.3390/ma19050970 (velikajne2026influenceofbase pages 6-8, velikajne2026influenceofbase pages 8-11, velikajne2026influenceofbase pages 1-2)
- Guo et al. 2022, Al-Mg-Mn-Er-Zr: DOI 10.1016/j.matdes.2022.111064 (guo2022microstructureandmechanical pages 1-2, guo2022microstructureandmechanical pages 2-3)
- Li et al. 2025, Al-Fe-Mg-Zr eutectic: DOI 10.1080/17452759.2025.2516663 (li2025precipitationevolutionaging pages 1-3, li2025precipitationevolutionaging pages 3-4)
- Cerri et al. 2024, Scalmalloy heat treatments review: DOI 10.3390/cryst15010025 (cerri2024mainheattreatments pages 11-14, cerri2024mainheattreatments pages 14-16, cerri2024mainheattreatments pages 1-2)
- Mehta et al. 2021, Scalmalloy peak hardening: DOI 10.3390/met12010057 (mehta2021laserpowderbed pages 10-11)
- Belelli et al. 2022, Al-Mg-Zr-Sc reduced Sc: DOI 10.1016/j.jallcom.2022.166519 (belelli2022investigationandcharacterization pages 8-14)
- Zhu et al. 2023, AlSi10Mg platform preheating: DOI 10.1016/j.msea.2023.145486 (zhu2023microstructuralanalysisof pages 3-5, zhu2023microstructuralanalysisof pages 9-12)
- Hong et al. 2026, normalized enthalpy and Eagar-Tsai diagnostics: DOI 10.3390/ma19153290 (hong2026fittingfreediagnosisof pages 4-5)
- Martucci et al. 2022, Al-Mn-Cr-Zr processing parameters: DOI 10.3390/met12081387 (martucci2022theinfluenceof pages 2-4)
- Agricola et al. 2024, Al-Cr-Mo-Sc-Zr high build rate: DOI 10.1007/s40964-024-00627-8 (agricola2025parameterstudyof pages 1-2)
- Martucci et al. 2022, low-power Scalmalloy: DOI 10.3390/ma15093123 (martucci2022lowpowerlaserpowder pages 11-13, martucci2022lowpowerlaserpowder pages 2-4)
- Yadegari et al. 2025, Al LPBF sustainability review: DOI 10.3390/app15042221 (yadegari2025aluminumlaseradditive pages 19-21, yadegari2025aluminumlaseradditive pages 39-41)
