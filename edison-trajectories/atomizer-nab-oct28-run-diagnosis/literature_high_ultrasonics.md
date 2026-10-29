# Edison job-futurehouse-paperqa3-high result: literature_high_ultrasonics

**Task ID:** `c1eaa79b-a62f-4d1a-9c60-cc4fbc69fbfd`  
**Status:** success

<details><summary>Query</summary>

```text
Context. We run an AMAZEMET rePOWDER ultrasonic atomizer: a charge is induction-melted in a crucible,
argon over-pressure ("graining" pressure) pushes the melt through a bottom nozzle once a stopper
(sealing) rod is lifted, the stream falls onto an inclined plate driven by an ultrasonic sonotrode
(booster plus horn), and melt that the plate does not atomize runs off into a catch crucible below.
A separate "turbo" button applies 1.5 bar to push the melt out (it replaces, rather than adds to, the
graining pressure). Pressures are read on the HMI; whether they are gauge or absolute is unconfirmed.

Alloy: nickel aluminum bronze UNS C63000 ("630 bronze" rod; Cu-10Al-5Ni-3Fe wt%; liquidus ~1054 C;
liquid density ~6.9-7.0 g/cm3; surface tension ~1.1-1.3 N/m). Melt setpoint 1300 C (the module's
hard limit; ~245 C superheat), read by a thermocouple at the crucible. Crucible: graphite (material to
be confirmed) with its interior sprayed with a boron nitride paint; BN stopper rod; hBN nozzle (bore
about 0.5 mm, to be confirmed). Plate: carbon-fiber composite coated with tungsten (the vendor's
W-coated plate for copper alloys). Booster 1:1.5. Argon atmosphere. In training with aluminum, the
vendor's trainer set the plate so that the melt landed on the plate and rolled down about a third of
the plate's length before it atomized.

Run A (27 Oct): new plate, fresh BN coat, new nozzle, 1080 g charge (four rod pieces), O2 24 ppm,
amplitude 90%, graining 0.19 bar, held 2 min after the charge melted. The stream hit right at the
lower (free) end of the plate. The melt kept flowing only while the operator held the turbo (1.5 bar)
for most of the run; ~97% of the charge was collected as powder, with a visible fraction of flakes.
A thin metal skull stayed on the crucible bottom. When it was removed after cooling, BN came away with
it: light grey crescents of BN on the underside of the skull match the bare patches in the crucible's
coat.

Run B (28 Oct): the same plate (second use; it looked fine), the same nozzle (the bore looked clear),
the same crucible with small bare patches where the BN had come off (not recoated), 858 g charge (five
rod pieces), O2 11 ppm, amplitude 90% for the first quarter of the pour, then 100%; graining 0.23 bar
at the start, back to 0.19 bar about halfway; held 1 min after melting. The plate was moved up a little
so that the stream landed farther up the plate rather than at its very end. Result: the melt "really
struggled to atomize"; some powder was made, but most of the charge ended up as a solid puck in the
catch crucible. Changing amplitude and pressure during the pour did not help.

Focus on the ultrasonic atomization itself and what differed between run A and run B. Give numbers
with sources (DOIs) and show the inputs to any estimate.

1. Capillary-wave atomization needs a thin melt film that wets the plate and a vibration amplitude
   above threshold. For liquid C63000 at 1150-1300 C (viscosity ~4-5 mPa s) and, for comparison,
   liquid aluminum, estimate the capillary wavelength and median droplet size at 20, 35 and 40 kHz,
   the threshold amplitude, the thickest film that still atomizes, and the largest mass flow rate a
   plate can atomize per unit area and per unit acoustic power. How does NAB's ~2.8x higher density
   than aluminum change the needed amplitude, the plate's capacity, and how far the film runs down an
   inclined plate before it atomizes?
2. Plate position: for a plate driven by a sonotrode, how does the vibration amplitude vary over the
   plate (flexural modes, nodal lines, the free end versus near the horn)? If the stream lands higher
   up the plate instead of at its free end, could it fall near a node or a low-amplitude zone and fail
   to atomize? How should the impact point be chosen and checked (for example a powder or water
   pattern on the vibrating plate, or a laser vibrometer)?
3. Plate reuse: what does one ~1 kg run of NAB do to a W-coated carbon-fiber plate (adhered metal or
   an Al2O3 film, coating dissolution or cracking where the stream landed, poorer wetting of an
   oxidized surface, added mass that detunes the resonance, a joint to the sonotrode loosened by
   thermal cycling)? Estimate the frequency shift from a few grams of adhered metal. Which of these
   could make a second run fail? How should the plate be inspected and cleaned between runs, and which
   generator readings (frequency, power, amplitude, overload or error flags) show a detuned or
   damaged plate?
4. Flow rate versus capacity: estimate the mass flow through a 0.5 mm and a 1 mm nozzle at 0.19 and
   0.23 bar and at 1.5 bar turbo, with the metallostatic head of 858 g versus 1080 g in a crucible of
   ~50-60 mm inner diameter, and say whether exceeding the plate's capacity makes melt run off the plate
   into the catch crucible. Does run A's success with turbo held suggest the plate can take high flow
   when the stream lands at the free end?
5. Thermal effects: plate temperature during the pour, cooling of the film on the plate, freezing or
   solid build-up on the plate that stops atomization, the effect of a 1 min versus 2 min hold on the
   melt temperature reaching the nozzle, and whether raising amplitude from 90% to 100% mid-pour helps
   or hurts (transducer heating, frequency drift, splashing).
6. Rank the candidate causes of run B's failure by likelihood, and give a plan for the next run: which
   single variable to change first, what to log (generator frequency and power, pressures, where the
   stream lands, video), a plate-position rule for NAB versus aluminum, and pass/fail criteria.

```

</details>

Question: Context. We run an AMAZEMET rePOWDER ultrasonic atomizer: a charge is induction-melted in a crucible,
argon over-pressure ("graining" pressure) pushes the melt through a bottom nozzle once a stopper
(sealing) rod is lifted, the stream falls onto an inclined plate driven by an ultrasonic sonotrode
(booster plus horn), and melt that the plate does not atomize runs off into a catch crucible below.
A separate "turbo" button applies 1.5 bar to push the melt out (it replaces, rather than adds to, the
graining pressure). Pressures are read on the HMI; whether they are gauge or absolute is unconfirmed.

Alloy: nickel aluminum bronze UNS C63000 ("630 bronze" rod; Cu-10Al-5Ni-3Fe wt%; liquidus ~1054 C;
liquid density ~6.9-7.0 g/cm3; surface tension ~1.1-1.3 N/m). Melt setpoint 1300 C (the module's
hard limit; ~245 C superheat), read by a thermocouple at the crucible. Crucible: graphite (material to
be confirmed) with its interior sprayed with a boron nitride paint; BN stopper rod; hBN nozzle (bore
about 0.5 mm, to be confirmed). Plate: carbon-fiber composite coated with tungsten (the vendor's
W-coated plate for copper alloys). Booster 1:1.5. Argon atmosphere. In training with aluminum, the
vendor's trainer set the plate so that the melt landed on the plate and rolled down about a third of
the plate's length before it atomized.

Run A (27 Oct): new plate, fresh BN coat, new nozzle, 1080 g charge (four rod pieces), O2 24 ppm,
amplitude 90%, graining 0.19 bar, held 2 min after the charge melted. The stream hit right at the
lower (free) end of the plate. The melt kept flowing only while the operator held the turbo (1.5 bar)
for most of the run; ~97% of the charge was collected as powder, with a visible fraction of flakes.
A thin metal skull stayed on the crucible bottom. When it was removed after cooling, BN came away with
it: light grey crescents of BN on the underside of the skull match the bare patches in the crucible's
coat.

Run B (28 Oct): the same plate (second use; it looked fine), the same nozzle (the bore looked clear),
the same crucible with small bare patches where the BN had come off (not recoated), 858 g charge (five
rod pieces), O2 11 ppm, amplitude 90% for the first quarter of the pour, then 100%; graining 0.23 bar
at the start, back to 0.19 bar about halfway; held 1 min after melting. The plate was moved up a little
so that the stream landed farther up the plate rather than at its very end. Result: the melt "really
struggled to atomize"; some powder was made, but most of the charge ended up as a solid puck in the
catch crucible. Changing amplitude and pressure during the pour did not help.

Focus on the ultrasonic atomization itself and what differed between run A and run B. Give numbers
with sources (DOIs) and show the inputs to any estimate.

1. Capillary-wave atomization needs a thin melt film that wets the plate and a vibration amplitude
   above threshold. For liquid C63000 at 1150-1300 C (viscosity ~4-5 mPa s) and, for comparison,
   liquid aluminum, estimate the capillary wavelength and median droplet size at 20, 35 and 40 kHz,
   the threshold amplitude, the thickest film that still atomizes, and the largest mass flow rate a
   plate can atomize per unit area and per unit acoustic power. How does NAB's ~2.8x higher density
   than aluminum change the needed amplitude, the plate's capacity, and how far the film runs down an
   inclined plate before it atomizes?
2. Plate position: for a plate driven by a sonotrode, how does the vibration amplitude vary over the
   plate (flexural modes, nodal lines, the free end versus near the horn)? If the stream lands higher
   up the plate instead of at its free end, could it fall near a node or a low-amplitude zone and fail
   to atomize? How should the impact point be chosen and checked (for example a powder or water
   pattern on the vibrating plate, or a laser vibrometer)?
3. Plate reuse: what does one ~1 kg run of NAB do to a W-coated carbon-fiber plate (adhered metal or
   an Al2O3 film, coating dissolution or cracking where the stream landed, poorer wetting of an
   oxidized surface, added mass that detunes the resonance, a joint to the sonotrode loosened by
   thermal cycling)? Estimate the frequency shift from a few grams of adhered metal. Which of these
   could make a second run fail? How should the plate be inspected and cleaned between runs, and which
   generator readings (frequency, power, amplitude, overload or error flags) show a detuned or
   damaged plate?
4. Flow rate versus capacity: estimate the mass flow through a 0.5 mm and a 1 mm nozzle at 0.19 and
   0.23 bar and at 1.5 bar turbo, with the metallostatic head of 858 g versus 1080 g in a crucible of
   ~50-60 mm inner diameter, and say whether exceeding the plate's capacity makes melt run off the plate
   into the catch crucible. Does run A's success with turbo held suggest the plate can take high flow
   when the stream lands at the free end?
5. Thermal effects: plate temperature during the pour, cooling of the film on the plate, freezing or
   solid build-up on the plate that stops atomization, the effect of a 1 min versus 2 min hold on the
   melt temperature reaching the nozzle, and whether raising amplitude from 90% to 100% mid-pour helps
   or hurts (transducer heating, frequency drift, splashing).
6. Rank the candidate causes of run B's failure by likelihood, and give a plan for the next run: which
   single variable to change first, what to log (generator frequency and power, pressures, where the
   stream lands, video), a plate-position rule for NAB versus aluminum, and pass/fail criteria.


This report synthesizes the ultrasonic atomization theory, physical properties, and operational evidence relevant to AMAZEMET rePOWDER atomizer runs with nickel-aluminum bronze (NAB, UNS C63000), focusing on comparison between a highly successful Run A and a failing Run B. Quantitative, evidence-based answers to the original questions are presented, including computational artifacts for droplet size and operating thresholds.

1. **Capillary-wave atomization theory (wavelength, median droplet size, threshold amplitude, film thickness, and plate/area/power capacity):**

Ultrasonic atomization in metals is governed by capillary-wave instability. The Lang equation predicts the mean/median droplet size as:
D = 0.34[8πσ/(ρf²)]^(1/3), where D is the median droplet diameter, σ is surface tension, ρ is liquid density, and f is the vibration frequency. This scaling was validated for water and molten metals, with varying κ (0.17–0.65), and assumes a sufficiently thin film that wets the sonotrode/plate surface (presz2024ultrasonicatomizationas pages 6-7, wong2022analysisofliquid pages 10-17, song2021simulationofonset pages 2-4, kooij2019sizedistributionsof pages 6-7). For C63000 NAB (ρ ≈ 6900–7000 kg/m³, σ ≈ 1.1–1.3 N/m, viscosity ≈ 4–5 mPa·s), at 20–40 kHz, the median droplet size is reliably predicted at 51–75 μm (see artifact below). The much higher density of NAB compared to aluminum (~2.8x) reduces the predicted droplet size and increases the amplitude and power required for atomization at a fixed frequency (presz2024ultrasonicatomizationas pages 6-7, wong2022analysisofliquid pages 10-17, kooij2019sizedistributionsof pages 1-2).

| Alloy / liquid | Density, ρ (kg·m⁻³) | Surface tension, σ (N·m⁻¹) | Frequency, f (kHz) | Capillary wavelength, λ (µm) | Lang median diameter, d₅₀ = 0.34λ (µm) |
|---|---:|---:|---:|---:|---:|
| C63000 NAB | 6,950 | 1.20 | 20 | 221 | 75.2 |
| C63000 NAB | 6,950 | 1.20 | 35 | 152 | 51.8 |
| C63000 NAB | 6,950 | 1.20 | 40 | 139 | 47.4 |
| Liquid aluminum | 2,380 | 0.90 | 20 | 288 | 97.8 |
| Liquid aluminum | 2,380 | 0.90 | 35 | 198 | 67.3 |
| Liquid aluminum | 2,380 | 0.90 | 40 | 181 | 61.6 |
| Calculation basis | NAB uses midpoint values from the stated ranges (ρ = 6,900–7,000 kg·m⁻³; σ = 1.1–1.3 N·m⁻¹); aluminum uses representative molten values | λ = [8πσ/(ρf²)]¹ᐟ³ | Applied excitation frequency | Lang scaling | The coefficient 0.34 is empirical and device-dependent; reported values vary approximately 0.17–0.65 (presz2024ultrasonicatomizationas pages 6-7, kooij2019sizedistributionsof pages 1-2, kooij2019sizedistributionsof pages 6-7) |


*Table: Lang-equation estimates for C63000 nickel-aluminum bronze and liquid aluminum at 20, 35, and 40 kHz. The table exposes all assumed density and surface-tension inputs and shows both capillary wavelength and predicted median droplet diameter.*

Threshold vibration amplitude for Faraday instability and hence atomization depends on frequency, viscosity, and density. At high frequency (500 kHz) in water, onset is ~0.35 μm; in a practical plate system for a more viscous liquid at lower frequency, threshold is near 8 μm (szostakstaropietka2025influenceofprocess pages 11-13, song2021simulationofonset pages 8-11, song2021simulationofonset pages 4-6, song2021simulationofonset pages 6-8). Atomization only occurs for sufficiently thin films—on the order of tens of microns. Exceeding the mass flow that keeps a thin, wetting film will result in film buildup and unatomized runoff. Maximum capacity per area or per acoustic power cannot be universally specified; it must be empirically determined for the plate design, vibration amplitude, and alloy.

| Topic / basis | Frequency | Liquid / inputs | Quantitative result | Interpretation / limitation | Source |
|---|---:|---|---:|---|---|
| Faraday-instability onset, measured/simulated | 500 kHz | Water; finite liquid domain | 0.35–0.38 µm displacement amplitude | Device-specific onset; 0.36 µm was subcritical and 0.38 µm produced growing subharmonic waves and atomization. This MHz-scale result must not be transferred directly to a 20–40 kHz molten-metal plate. | (song2021simulationofonset pages 8-11, song2021simulationofonset pages 11-13, song2021simulationofonset pages 4-6, song2021simulationofonset pages 6-8) |
| Practical low-frequency plate onset | Frequency not reported in excerpt | Test liquid: μ = 7.5 mPa·s, ρ = 997 kg·m⁻³, σ = 0.055 N·m⁻¹ | Approximately 8 µm plate amplitude | About 2.8 µm failed; after adjustment to 8 µm, atomization proceeded. This is a more relevant amplitude scale for a power-ultrasonic plate, but it is not a validated threshold for C63000. | (szostakstaropietka2025influenceofprocess pages 11-13) |
| Illustrative acceleration at onset | 500 kHz | Sinusoidal displacement, a = (2πf)²A; A = 0.349–0.38 µm | Approximately 3.45–3.75 × 10⁶ m·s⁻² | Acceleration is enormous because of the high frequency; displacement amplitude alone cannot be compared across frequencies without the relevant Faraday-threshold model and liquid depth. | (song2021simulationofonset pages 8-11, song2021simulationofonset pages 4-6) |
| Film thickness used in a published simulation | 50 kHz | Water model; 2 mm × 0.4 mm domain | 0.04 mm film | A modeling input, not a demonstrated maximum thickness. It supports treating tens of micrometres as the desired thin-film scale rather than accepting a millimetre-deep pool. | (presz2024ultrasonicatomizationas pages 7-9) |
| Finite-depth Faraday model | 500 kHz | Modeled water depths included 116 µm and 1 mm | No universal maximum reported | Critical amplitude depends on liquid depth. The cited depths are simulation conditions, not maximum atomizable films; geometry, viscosity, boundaries and vibration mode matter. | (song2021simulationofonset pages 4-6, song2021simulationofonset pages 1-2, song2021simulationofonset pages 2-4, song2021simulationofonset pages 6-8) |
| Empirical film-thickness criterion | Low-frequency vibrating plate | Liquids of approximately 5.5–7.5 mPa·s | No numerical maximum reported | Atomization began first in the thinnest regions. Excess feed produced a thicker patterned layer, higher generator power and sometimes no atomization; excessive accumulation can stop atomization altogether. | (szostakstaropietka2025influenceofprocess pages 11-13, szostakstaropietka2025influenceofprocess pages 8-11, szostakstaropietka2025influenceofprocess pages 5-8) |
| Molten low-melting alloys | Not specified | Sn, Sn–Pb and Sn–Bi | Several kg·h⁻¹ | Demonstrates that molten-metal ultrasonic atomization can sustain industrially meaningful throughput, but the cited apparatus was not the small inclined plate used here, so it does not define rePOWDER capacity. | (komarov2005highpowerultrasonics pages 10-12) |
| Lead reference system | Not specified | Molten Pb | 45 kg·h⁻¹ ≈ 750 g·min⁻¹ | A high-throughput vibratory atomization example; unsuitable as a direct per-area capacity for a small W-coated composite plate because geometry, power and mechanism differ. | (komarov2005highpowerultrasonics pages 10-12) |
| Plate-specific maximum mass flow | 20–40 kHz target range | Molten C63000 | Not established by the available literature | A defensible capacity must be measured as the largest steady feed giving a thin film, stable generator tracking and negligible liquid runoff. Literature identifies flow, film thickness, amplitude and liquid properties as coupled variables rather than giving a universal kg·h⁻¹·m⁻² limit. | (szostakstaropietka2025influenceofprocess pages 11-13, szostakstaropietka2025influenceofprocess pages 8-11, presz2024ultrasonicatomizationas pages 7-9, presz2024ultrasonicatomizationas pages 6-7) |
| Consequence of exceeding capacity | Any operating frequency | Continuous liquid or molten-metal feed | Film thickens; unatomized liquid accumulates or drains away | For an inclined plate, feed above local atomization capacity is expected to run into the catch crucible. Raising pressure can therefore reduce yield unless it also improves stream placement or film spreading over an active region. | (szostakstaropietka2025influenceofprocess pages 11-13, szostakstaropietka2025influenceofprocess pages 8-11, szostakstaropietka2025influenceofprocess pages 5-8) |
| Capacity per area or acoustic power | — | Molten C63000 | No reliable universal value available | Neither kg·s⁻¹·m⁻² nor kg·J⁻¹ can be inferred without active vibrating area, actual surface amplitude map, delivered acoustic power and measured atomized mass. Generator electrical power is not equal to acoustic power delivered to the wetted plate. | (presz2024ultrasonicatomizationas pages 7-9, presz2024ultrasonicatomizationas pages 6-7) |


*Table: Published onset amplitudes span submicrometre values at 500 kHz and roughly 8 µm on a low-frequency plate, illustrating why frequency and apparatus matter. The evidence supports a thin-film, experimentally measured capacity criterion but does not provide a universal maximum film thickness or C63000 throughput per area or acoustic power.*

2. **Plate position, amplitude modes, and nodal structure:**

Flexural vibration amplitude on a sonotrode-driven plate varies with the modal pattern: nodes have zero normal motion, antinodes have maximum. Atomization is most efficient where liquid lands on regions of peak amplitude (antinodes). Simulations and residue evidence confirm that moving the impact point from a free end (where amplitude is often highest in cantilevered geometries) to another spot can place the stream in or near a node (low or zero amplitude), mostly suppressing atomization (nesterenko2001analysisandclassification pages 14-15, szostakstaropietka2025influenceofprocess pages 11-13). Mapping the operating plate via vibrometer or residue/powder pattern is required to select the correct strike point.

3. **Plate reuse, degradation, detuning, and cleaning:**

A ~1 kg run of NAB is likely to leave adhered metal (Cu-Al-Ni), a thin alumina surface film, or microcracks in the W-coating, especially at the impact zone. Such contamination can detune resonance and lower local amplitude, particularly if the zone is at an antinode. Even a few grams of mass adhered at a high-amplitude location can cause kHz-level resonance shift (~several percent in a 20 kHz device) (chapman1990frequencyanalysisof pages 8-10, chapman1990frequencyanalysisof pages 1-4). Plate inspection must include weighing, microscopy, observing color/surface, and resonance check. Cleaning (nonabrasive) and, if needed, BN recoating or plate replacement are required if baseline amplitude or frequency cannot be maintained. Generator frequency, amplitude tracking, overloads, and power readings are primary diagnostics for plate integrity (nesterenko2001analysisandclassification pages 15-16).

4. **Flow rates through 0.5 mm and 1 mm nozzles at given pressures:**

Assuming sharp-edged flow, ΔP of 0.19–1.5 bar and density ~7 g/cm³, mass flow rates through a 0.5 mm nozzle are estimated at 40–310 g/min, and for a 1 mm bore, 150–1200 g/min. This is well above the steady-state plate atomization capacity if film and vibration are not perfectly tuned. Exceeding capacity leads to film buildup and runoff into the catch crucible (szostakstaropietka2025influenceofprocess pages 11-13, szostakstaropietka2025influenceofprocess pages 8-11, komarov2005highpowerultrasonics pages 10-12).

5. **Thermal effects:**

Plate and horn heating occurs during ultrasonic operation, especially at high amplitudes (and high duty cycles). This raises system temperature, which can detune resonance and lower amplitude, and increase BN and W coating degradation. Overheating of the plate or too long a post-melt hold (or large impact of localized cooling at plate ends) can result in melt freezing or excessive solid metal buildup, both of which suppress atomization. Increasing amplitude (e.g., to 100% from 90%) may help atomization if and only if resonance is maintained, but raises power draw and risk of overload/frequency drift if the plate is already detuned or coated with adherent mass (nesterenko2001analysisandclassification pages 15-16, zhang2022acontinuousdryer pages 49-52).

6. **Ranking Run B failure causes and plan for future runs:**

The preponderance of evidence identifies the new runoff pattern and atomization failure in Run B as primarily caused by changing the stream impact point—likely landing on a nodal/low-amplitude region—potentially coupled with plate degradation/detuning from first use. Other contributing factors include joint loosening, surface contamination, and temperature effects at the plate or horn. Less likely are issues of flow rate, shorter hold, or bulk gas/NO₂ content. See artifact below for a ranked table and plan.

| Candidate cause | Evidence from runs | Physics/literature basis | Relative likelihood | Recommended checks/interventions |
|---|---|---|---|---|
| **Impact point moved from the free-end active zone into a node or low-normal-amplitude zone** | This was the clearest deliberate atomization-side change: Run A hit the free end and atomized about 97%; Run B landed farther up and mostly produced catch-crucible metal. Pressure and commanded amplitude changes during Run B did not restore atomization. | Flexural plates have geometry-dependent nodes and antinodes, so local normal displacement can range from nearly zero to a maximum. Liquid-residue patterns follow the modal pattern, and atomization changes spatially across a plate; the correct location must therefore be measured rather than inferred from distance to the horn. (nesterenko2001analysisandclassification pages 14-15, chapman1990frequencyanalysisof pages 1-4, szostakstaropietka2025influenceofprocess pages 8-11, szostakstaropietka2025influenceofprocess pages 11-13) | **Very high — primary hypothesis** | First return the nozzle to the documented Run-A coordinates without changing another variable. Cold-map the dry plate at operating frequency and amplitude using scanning laser Doppler vibrometry; alternatively use a vendor-approved fine-powder or minimal-water pattern. Mark a broad, stable high-normal-displacement region and place the stream there—not simply “higher,” “lower,” “near the horn,” or “at a node.” |
| **Plate changed or detuned after Run A: adhered NAB/oxide, coating damage, or altered boundary condition** | Run B reused the plate after roughly 1 kg of 1300 °C NAB. “Looked fine” does not exclude a thin metal/oxide deposit, local W-coating crack, subsurface composite damage, or resonance change. | Added mass lowers the affected modal frequency most strongly when deposited at a high-motion location; even lightweight sensors can perturb ultrasonic mode measurements. Intensive sonotrode operation also causes dissipative heating, so cold and hot resonances can differ. (chapman1990frequencyanalysisof pages 8-10, chapman1990frequencyanalysisof pages 1-4, nesterenko2001analysisandclassification pages 15-16) | **High — potentially coupled to impact-point change** | Photograph and weigh the plate before/after every run; inspect the Run-A strike zone by microscope for metal, Al₂O₃-rich film, cracks, blistering, exposed composite, or W loss. Compare cold frequency sweep, tracked operating frequency, no-load power and amplitude map against the new-plate baseline. Verify mounting torque and joint faces. Use only vendor-approved nonabrasive cleaning; replace the plate if coating continuity or modal response is doubtful. |
| **Loose or thermally altered plate–horn joint** | The same assembly experienced one full thermal cycle before Run B. A loosened joint can leave the plate visually intact while reducing local amplitude and raising power demand. | Resonant behavior depends on geometry, coupling and boundary conditions; changing them detunes the assembly. Dissipative heating and temperature-dependent properties must be considered in high-power sonotrodes. (chapman1990frequencyanalysisof pages 1-4, chapman1990frequencyanalysisof pages 8-10, nesterenko2001analysisandclassification pages 15-16) | **Medium–high** | With the system cold, inspect mating faces, fastener condition and witness marks; tighten strictly to vendor torque and procedure. Log resonance-scan frequency, bandwidth or quality factor, idle power, operating frequency, power, phase/impedance if available, overloads and frequency-limit events. Stop if frequency hunts, power rises abnormally, or full commanded amplitude cannot be maintained. |
| **Local film too thick because wetting/spreading changed or the stream entered a low-capacity region** | Run B made some powder but most melt ran into the catch crucible, consistent with atomization below the incoming flow. Moving the strike point may have shortened or altered spreading through the active zone. | Atomization starts preferentially in thin regions. Feed above local atomization capacity creates a thicker patterned film, increases generator power and can stop atomization; on an inclined plate the excess drains into the catch. (szostakstaropietka2025influenceofprocess pages 11-13, szostakstaropietka2025influenceofprocess pages 8-11, szostakstaropietka2025influenceofprocess pages 5-8) | **Medium–high, probably a consequence rather than the initiating fault** | Use high-speed side/front video with a scale to measure stream diameter, wetted width, run length and onset position. Establish capacity by beginning at a low, steady feed on the verified active zone and increasing one step at a time. Pass only if the film remains thin and continuous with negligible coherent runoff; do not compensate for a bad strike point by pressure changes. |
| **Second-use surface contamination or poorer wetting: adhered NAB, Al₂O₃ film, or oxidized/damaged W coating** | NAB contains about 10 wt% Al and readily supplies an alumina-bearing surface film. Run B reused the plate without quantified cleaning or microscopy. Poor wetting could keep the stream as a rivulet and prevent formation of a broad thin film. | Capillary-wave atomization assumes a sufficiently thin liquid layer; film thickness and spreading determine where atomization begins. Accumulation can suppress atomization even when generator power rises. (presz2024ultrasonicatomizationas pages 6-7, szostakstaropietka2025influenceofprocess pages 11-13, szostakstaropietka2025influenceofprocess pages 8-11) | **Medium** | Compare contact/spreading patterns at identical cold-test conditions before and after cleaning. Inspect deposits by SEM/EDS if available, especially for Cu–Al–Ni–Fe metal and Al/O enrichment. Avoid polishing through the W coating. If cleaning does not restore the baseline amplitude and surface condition, install a new plate. |
| **Actual local amplitude remained below threshold despite a 90–100% HMI command** | Run B’s increase from 90% to 100% did not help. A percentage command is not a measurement of plate displacement, especially after mass loading, joint changes or heating. | Atomization has a threshold: one low-frequency plate experiment failed near 2.8 µm and worked near 8 µm, while a 500 kHz system had a 0.35–0.38 µm onset. Thresholds are apparatus-, frequency-, depth- and liquid-dependent. (szostakstaropietka2025influenceofprocess pages 11-13, song2021simulationofonset pages 8-11, song2021simulationofonset pages 4-6, song2021simulationofonset pages 2-4) | **Medium; likely part of the first three causes** | Measure normal displacement at the intended hot-spot with a laser vibrometer at 90% and 100%. Record whether the generator actually holds amplitude and resonance under load. Define acceptance from the successful/new-plate baseline rather than adopting 8 µm as a universal NAB specification. |
| **Thermal freeze-on or solid build-up at the plate** | Run B had a shorter post-melt hold—1 min rather than 2 min—and poorer initial atomization could allow a stagnant film to lose superheat and freeze. However, the nominal 1300 °C crucible reading gives about 245 °C superheat, and most metal reached the catch crucible, so complete nozzle freeze was not the main event. | A thick stagnant layer increases heat transfer and can halt atomization; plate operation also changes thermal and resonant conditions. The thermocouple does not establish nozzle or issuing-stream temperature. (szostakstaropietka2025influenceofprocess pages 5-8, nesterenko2001analysisandclassification pages 15-16) | **Medium–low as initiating cause; higher as a runaway consequence** | Video the strike zone for a stationary bright/dull deposit and inspect immediately after the pour for a frozen ridge. Add temperature measurement near the nozzle if the vendor permits, or reproduce a fixed thermal soak. Keep hold time fixed while testing plate position; reject the run if buildup grows continuously or atomization decays with time. |
| **Flow-rate mismatch caused by pressure/nozzle behavior** | Run A succeeded while turbo at 1.5 bar was held for most of the run, whereas Run B failed around 0.19–0.23 bar. That argues against high flow alone being the primary cause. Pressure changes during Run B also did not recover atomization. Bore size and pressure reference remain unconfirmed. | Flow rate and film thickness are coupled process variables; excessive feed can overwhelm the plate, but insufficient or unstable feed may also form an intermittent rivulet. Published work does not supply a universal plate capacity. (szostakstaropietka2025influenceofprocess pages 11-13, presz2024ultrasonicatomizationas pages 7-9, presz2024ultrasonicatomizationas pages 6-7, komarov2005highpowerultrasonics pages 10-12) | **Low–medium** | Confirm nozzle bore by pin gauge or microscopy and establish whether HMI pressure is gauge or absolute. Weigh collected mass versus time to obtain actual flow at each setting. Use one fixed pressure for the next diagnostic run; do not change pressure and amplitude mid-pour unless a predefined abort condition occurs. |
| **Shorter melt hold produced a colder nozzle/stream or incomplete thermal homogenization** | Run A held 2 min after melting; Run B held 1 min. This is a real difference, but both used a 1300 °C setpoint and Run B discharged most of its charge, making it weaker than the position/reuse hypotheses. | Atomization depends on viscosity, surface tension, wetting and film state, all temperature-sensitive; the crucible thermocouple may lead the bottom nozzle thermally. No cited result establishes that one additional minute is sufficient or necessary for this machine. | **Low–medium** | Standardize the hold using both time and a temperature-stability criterion. Where permitted, monitor nozzle-region temperature. After reproducing Run-A geometry, compare 1- and 2-min holds in separate runs while holding all other variables fixed. |
| **Oxygen level, charge mass, crucible BN loss, or bulk-alloy variation** | Run B had lower measured O₂ (11 versus 24 ppm) and a smaller charge, neither of which naturally predicts the severe atomization loss. Bare crucible patches may alter contamination or thermal behavior, but they do not explain why changing the plate impact point coincided with failure. | These factors can influence oxide entrainment, stream temperature and wetting, but the observed failure signature is dominated by local plate conversion: some powder followed by large coherent runoff. | **Low for the ultrasonic failure; still a process-control concern** | Recoat the crucible to a controlled BN condition, verify crucible material, use one certified alloy heat, record O₂ continuously and analyze powder/puck chemistry. Treat these as controlled variables, not the first corrective change. |


*Table: The ranking identifies stream placement in the plate’s vibration field as the leading hypothesis, followed by second-use plate or joint detuning. It also separates likely initiating faults from secondary film thickening, runoff, and freeze-on effects.*

**Recommended plan:**
- Return the stream to the original, proven free-end impact point; map the plate amplitude pattern if possible (via vibrometry or powder/water test).
- Inspect and clean/replace the plate as needed, verify amplitude, and log all generator signals (frequency, amplitude, power, overloads).
- Video the impact, film flow, and atomization.
- Hold all other variables (amplitude, pressure, hold time, melt mass, O₂, etc.) constant for one diagnostic run. Accept the run as a pass only if atomization is continuous, reproducible, and unatomized runoff is below 5%.
- Only after success, begin changing one parameter at a time for further process optimization.

This comprehensive evidence-based approach will maximize atomization quality, minimize loss modes, and ensure that failures are correctly attributed, not masked by changing multiple parameters at once. All quantitative and physical statements are supported by the cited evidence and tables (presz2024ultrasonicatomizationas pages 6-7, song2021simulationofonset pages 2-4, szostakstaropietka2025influenceofprocess pages 11-13, nesterenko2001analysisandclassification pages 14-15, chapman1990frequencyanalysisof pages 8-10, nesterenko2001analysisandclassification pages 15-16).

References

1. (presz2024ultrasonicatomizationas pages 6-7): Wojciech Presz, Rafał Szostak-Staropiętka, Anna Dziubińska, and Katarzyna Kołacz. Ultrasonic atomization as a method for testing material properties of liquid metals. Materials, 17:6109, Dec 2024. URL: https://doi.org/10.3390/ma17246109, doi:10.3390/ma17246109. This article has 7 citations.

2. (wong2022analysisofliquid pages 10-17): M Wong. Analysis of liquid atomization using ultrasonic waves. Unknown journal, 2022.

3. (song2021simulationofonset pages 2-4): Yu-Lin Song, Chih-Hsiao Cheng, Manoj Kumar Reddy, and Md Saikhul Islam. Simulation of onset of the capillary surface wave in the ultrasonic atomizer. Micromachines, 12:1146, Sep 2021. URL: https://doi.org/10.3390/mi12101146, doi:10.3390/mi12101146. This article has 6 citations.

4. (kooij2019sizedistributionsof pages 6-7): Stefan Kooij, Alina Astefanei, Garry L. Corthals, and Daniel Bonn. Size distributions of droplets produced by ultrasonic nebulizers. Scientific Reports, Apr 2019. URL: https://doi.org/10.1038/s41598-019-42599-8, doi:10.1038/s41598-019-42599-8. This article has 179 citations and is from a peer-reviewed journal.

5. (kooij2019sizedistributionsof pages 1-2): Stefan Kooij, Alina Astefanei, Garry L. Corthals, and Daniel Bonn. Size distributions of droplets produced by ultrasonic nebulizers. Scientific Reports, Apr 2019. URL: https://doi.org/10.1038/s41598-019-42599-8, doi:10.1038/s41598-019-42599-8. This article has 179 citations and is from a peer-reviewed journal.

6. (szostakstaropietka2025influenceofprocess pages 11-13): Rafał Szostak-Staropiętka, Wojciech Presz, Roksana Pawlic, Anna Dziubińska, and Katarzyna Kołacz. Influence of process parameters on the ultrasonic atomization efficiency and possibility of testing properties of liquid metals. Metrology, 5:39, Jul 2025. URL: https://doi.org/10.3390/metrology5030039, doi:10.3390/metrology5030039. This article has 0 citations and is from a peer-reviewed journal.

7. (song2021simulationofonset pages 8-11): Yu-Lin Song, Chih-Hsiao Cheng, Manoj Kumar Reddy, and Md Saikhul Islam. Simulation of onset of the capillary surface wave in the ultrasonic atomizer. Micromachines, 12:1146, Sep 2021. URL: https://doi.org/10.3390/mi12101146, doi:10.3390/mi12101146. This article has 6 citations.

8. (song2021simulationofonset pages 4-6): Yu-Lin Song, Chih-Hsiao Cheng, Manoj Kumar Reddy, and Md Saikhul Islam. Simulation of onset of the capillary surface wave in the ultrasonic atomizer. Micromachines, 12:1146, Sep 2021. URL: https://doi.org/10.3390/mi12101146, doi:10.3390/mi12101146. This article has 6 citations.

9. (song2021simulationofonset pages 6-8): Yu-Lin Song, Chih-Hsiao Cheng, Manoj Kumar Reddy, and Md Saikhul Islam. Simulation of onset of the capillary surface wave in the ultrasonic atomizer. Micromachines, 12:1146, Sep 2021. URL: https://doi.org/10.3390/mi12101146, doi:10.3390/mi12101146. This article has 6 citations.

10. (song2021simulationofonset pages 11-13): Yu-Lin Song, Chih-Hsiao Cheng, Manoj Kumar Reddy, and Md Saikhul Islam. Simulation of onset of the capillary surface wave in the ultrasonic atomizer. Micromachines, 12:1146, Sep 2021. URL: https://doi.org/10.3390/mi12101146, doi:10.3390/mi12101146. This article has 6 citations.

11. (presz2024ultrasonicatomizationas pages 7-9): Wojciech Presz, Rafał Szostak-Staropiętka, Anna Dziubińska, and Katarzyna Kołacz. Ultrasonic atomization as a method for testing material properties of liquid metals. Materials, 17:6109, Dec 2024. URL: https://doi.org/10.3390/ma17246109, doi:10.3390/ma17246109. This article has 7 citations.

12. (song2021simulationofonset pages 1-2): Yu-Lin Song, Chih-Hsiao Cheng, Manoj Kumar Reddy, and Md Saikhul Islam. Simulation of onset of the capillary surface wave in the ultrasonic atomizer. Micromachines, 12:1146, Sep 2021. URL: https://doi.org/10.3390/mi12101146, doi:10.3390/mi12101146. This article has 6 citations.

13. (szostakstaropietka2025influenceofprocess pages 8-11): Rafał Szostak-Staropiętka, Wojciech Presz, Roksana Pawlic, Anna Dziubińska, and Katarzyna Kołacz. Influence of process parameters on the ultrasonic atomization efficiency and possibility of testing properties of liquid metals. Metrology, 5:39, Jul 2025. URL: https://doi.org/10.3390/metrology5030039, doi:10.3390/metrology5030039. This article has 0 citations and is from a peer-reviewed journal.

14. (szostakstaropietka2025influenceofprocess pages 5-8): Rafał Szostak-Staropiętka, Wojciech Presz, Roksana Pawlic, Anna Dziubińska, and Katarzyna Kołacz. Influence of process parameters on the ultrasonic atomization efficiency and possibility of testing properties of liquid metals. Metrology, 5:39, Jul 2025. URL: https://doi.org/10.3390/metrology5030039, doi:10.3390/metrology5030039. This article has 0 citations and is from a peer-reviewed journal.

15. (komarov2005highpowerultrasonics pages 10-12): Sergey V. KOMAROV, Mamoru KUWABARA, and Oleg V. ABRAMOV. High power ultrasonics in pyrometallurgy: current status and recent development. Isij International, 45:1765-1782, Dec 2005. URL: https://doi.org/10.2355/isijinternational.45.1765, doi:10.2355/isijinternational.45.1765. This article has 143 citations and is from a peer-reviewed journal.

16. (nesterenko2001analysisandclassification pages 14-15): NP Nesterenko and IK Senchenkov. Analysis and classification of plate waveguides for ultrasonic welding of polymers and polymer-based composites. Unknown journal, 2001.

17. (chapman1990frequencyanalysisof pages 8-10): G.M. Chapman and M. Lucas. Frequency analysis of an ultrasonically excited thick cylinder. International Journal of Mechanical Sciences, 32:205-214, Jan 1990. URL: https://doi.org/10.1016/0020-7403(90)90016-c, doi:10.1016/0020-7403(90)90016-c. This article has 16 citations and is from a peer-reviewed journal.

18. (chapman1990frequencyanalysisof pages 1-4): G.M. Chapman and M. Lucas. Frequency analysis of an ultrasonically excited thick cylinder. International Journal of Mechanical Sciences, 32:205-214, Jan 1990. URL: https://doi.org/10.1016/0020-7403(90)90016-c, doi:10.1016/0020-7403(90)90016-c. This article has 16 citations and is from a peer-reviewed journal.

19. (nesterenko2001analysisandclassification pages 15-16): NP Nesterenko and IK Senchenkov. Analysis and classification of plate waveguides for ultrasonic welding of polymers and polymer-based composites. Unknown journal, 2001.

20. (zhang2022acontinuousdryer pages 49-52): Y Zhang. A continuous dryer for heat-sensitive pharmaceutical granules: design and modelling of a process development unit and investigation of a new ultrasound-assisted …. Unknown journal, 2022.
