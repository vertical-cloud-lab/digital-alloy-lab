# Plume, condensate and spatter: what they do to the windows, the cameras and the beam (2026-11-25)

Issue #260. [`monitoring.md`](../monitoring.md) proposes a left-wall side camera (LW), a steep lid camera (LP) and a back-wall
light window (BW), each behind a cover slide, and an argon purge across the LW slide. This note asks what the vapour plume,
its condensate and the spatter do in this chamber's argon cross-flow: where they go, how much lands on each window and on the
laser's cover slide, how long the slides last, whether the LW purge is worth it, and what the cameras and the beam see.
Nothing here is built or measured. The geometry is the model's (`cad/lpbf_low.py`) plus the ports in
[`cad/monitoring_spec.py`](../cad/monitoring_spec.py), read at run time.

| File | What it is |
|---|---|
| [`make_case_plume.py`](../analysis/monitoring/plume/make_case_plume.py) | the CFD case: [`analysis/cfd/make_case.py`](../analysis/cfd/make_case.py) (imported, not edited) plus the LW, BW, LP and layer-camera bores as recesses with their own patches, an argon purge slot across the LW slide, the recoater where it stands during lasing, and finer cells at the LW |
| [`run_cases.sh`](../analysis/monitoring/plume/run_cases.sh) | writes and solves the cases with [`analysis/cfd/run_case.sh`](../analysis/cfd/run_case.sh) (OpenFOAM v2406 in Docker, 4 GB, 2 ranks) |
| [`particles.py`](../analysis/monitoring/plume/particles.py) | condensate (random walk) and spatter (drag and gravity) in the solved flow: fates, concentration next to each window, deposition |
| [`spatter.py`](../analysis/monitoring/plume/spatter.py) | spatter on its own: heights, ranges, a Monte Carlo against the chamber's windows, cooling, how long it glows for each camera, motion blur |
| [`plume_jet.py`](../analysis/monitoring/plume/plume_jet.py) | the vapour jet by hand: vapour pressure over each alloy, evaporation, jet speed and momentum, rise in the cross-flow, primary particle size, Mie extinction of the condensate |
| [`fouling.py`](../analysis/monitoring/plume/fouling.py) | the optics of a deposit on a slide, and hours to each window's limit |
| [`summarize.py`](../analysis/monitoring/plume/summarize.py) → [`summary.md`](../analysis/out/monitoring/plume/summary.md) | every table below, regenerated from the JSON files |
| [`analysis/out/monitoring/plume/`](../analysis/out/monitoring/plume/) | `particles.json`, `spatter.json`, `plume_jet.json`, `fouling.json` and the figures |

Edison's two literature answers for this ([`r8-melt-plume`](../edison/r8-melt-plume/answer.md) and
[`r8-viewports`](../edison/r8-viewports/answer.md)) are used throughout; §6 says where this note differs.

## 0. Short answer

With the gas layout gas-flow.md recommends (screens, 35 mm outlet channel, upper slot; 200 + 40 L/min, 2.95 m/s at 3 mm
over the plate):

1. **The bed jet removes the plume.** With worker A's source terms (320 W, 1.1 m/s: 0.47 g of AlSi10Mg condensate per
   hour of lasing, ~0.12 µg per mm of track, a 478 m/s jet off the keyhole wall), the plume's centreline tops out near
   the top of the 20 mm bed jet; Bitharas et al. saw only ~1 mm in a 2.1 m/s cross-flow (SS316) (§3). 100 % of the
   condensate released at 0.5–5 mm and 99.8 % of that released at 5–20 mm leaves through the floor slot within 20 s,
   most within 0.1 s (§1.2).
2. **The laser slide gets the least condensate and the most spatter.** The upper slot's sweep keeps 99.7 % of the
   condensate out of its recess. But 1.5–5 % of 100–200 µm Al droplets launched from the plate reach it, still molten
   (5–8 % at steel-like speeds), and no gas flow that spares the powder can stop them in 126 mm. **Spatter sets its life**:
   at an assumed 100 spatters per second of lasing, ~1,200–3,200 splats covering 8–19 % of its open area per hour of
   lasing (§4.4). Condensate comes next: it tolerates ~100× less deposit than a camera slide and would reach its
   absorption limit in ~30 h of lasing (§4.3). Inspect it after every build and stock slides for a change every few
   hours of lasing until the first builds measure the real rates.
3. **Move the steep lid port (LP) to the back half of the lid, under the upper slot's sweep.** At (−60, −80), where
   monitoring.md put it, the ceiling sweep carries the risen plume past it: it is the dirtiest window, ~12× the LW's
   deposit. Under the candidates at (−40, 60) and (−20, 80) the gas carries ~20× less condensate (10–40× across the four
   runs, §1.2). Its room outside needs the CAD check.
4. **The left-wall port (LW) is the cleanest camera window,** and spatter almost never reaches it (≤ 0.1 % of launches
   in the CFD; it looks in at 13° through a 4 mm recess). **The purge cuts the condensate at its slide ~13× at 1 L/min
   and ~45× at 3 L/min,** and the deposit 4–6× by a turbulent-deposition model, more if its layer is laminar (§1.2). Fit
   the slot and a needle valve on a branch of the loop after the HEPA filter; run it for 7075, keyhole-mode work and long
   builds.
5. **Keep camera slides at or above the gas temperature.** Thermophoresis decides deposition: a slide 10 K colder than the
   gas collects 20–120× more condensate than an isothermal one; a few K warmer repels it (§4.3).
6. **How fast the camera slides foul depends on what the deposit looks like, which only a measurement will show.** As
   isolated nanoparticles, the dirtiest one (LP as placed) loses 10 % of its light in ~150 h of lasing, the others in
   thousands (AlSi10Mg at A's rate; 7075 about the same; ~6 h for the LP if 10 K colder than the gas). As a continuous
   film, the same mass costs the LP 10 % in ~0.3 h and the others in 3–10 h. Real condensate, chains of ~10 nm particles
   and partly oxidised, lies between. Nobody has published it for Al (Edison agrees), so check every slide's
   transmission each build (§4.5).
7. **The plume costs the beam ~0.05–0.2 % at 1070 nm** (worker A's source terms at 320 W: 6061 to 7075; at most ~1 % if
   all the vapour condensed above the spot) and the coaxial photodiode ~4× more at 850 nm, fluctuating with the keyhole;
   the two-colour ratio cancels most of it (§3.4). It doesn't steer the beam. Old plume crosses the beam only where
   vectors are shorter than ~1 mm (§5).
8. **For the side camera: 10–20 µs exposures.** Al spatter moves at a few m/s, so 10 µs blurs it by under a pixel to
   ~3 pixels at 29 µm/px (§2.3). Above ~100 µs the plume's own light, about as bright in total as the pool's in a side
   view, swamps the image (Nagato et al. 2023). Through an 850 ± 5 nm filter, spatter glows above ~1,500 K: 100–200 µm
   droplets for 16–60 ms of flight, small ones for 2–4 ms. Everything else (entrained powder, > 80 % of the ejecta) shows
   only by the diode light.
9. **For the process:** 2–4 % of 100–200 µm spatter lands back on the plate (the layer camera's 25 µm/px sees it); the
   200 °C plate repels condensate by thermophoresis, so little settles on the bed; and the condensate of AlSi10Mg and
   6061 is mostly Al (A: 69–85 mol %), that of 7075 Zn and Mg (§3.1).
10. **At 140 + 30 L/min** (2.03 m/s at 3 mm): 2–3× more 100–200 µm spatter lands back on the plate (6–8 %), the LP gets
    half the condensate and the layer camera's bore 2–3× more; the rest is about the same (§1.3).

## 1. Condensate and spatter in the chamber's flow (CFD)

### 1.1 What was run

- **The gas layout is gas-flow.md's recommended one** (§0.5 there): screens in both slots, the 35 mm outlet channel, and the
  100 × 4 mm upper slot under the lid at z 114–118. It is the only layout that gives the operating point's 2.5–3.3 m/s over
  the plate. This run reproduces it: **2.95 m/s mean at 3 mm over Ø75 (2.60–3.33)** at 200 + 40 L/min, against 2.94
  (2.60–3.32) in gas-flow.md.
- **What's new in the gas volume** (`make_case_plume.py`), with the viewports from `monitoring_spec.py`:

  | Patch | What | As modelled |
  |---|---|---|
  | `lwSlide` | LW cover slide, left wall | Ø25 bore as a 22.2 mm square, its axis where the line of sight crosses the wall (y −18, z 33); slide 4 mm deep in the wall (assumed) |
  | `lwPurge` | argon across the LW slide | a 1.5 × 22 mm slot in the recess's top face, next to the slide, blowing down across it; a wall when off |
  | `bwWindow` | back-wall light window | Ø20 bore through the 16 mm wall at x −116, z 23; window on the outer face |
  | `lpSlide` | steep lid port at (−60, −80) | Ø20 bore, slide 4 mm into the lid (assumed) |
  | `lcWindow` | the layer camera's existing Ø30 bore | through the 16 mm lid at (71, −42); window at the lid's top face (the real one is higher, in the boss) |
  | `slide` | the laser's cover slide | as gas-flow.md: the Ø56 / Ø46 recess, slide at z 126 |

- **The recoater stands at the end of its stroke** (x 91–122), where the layer cycle leaves it while the laser runs and
  where monitoring.md checked the views. gas-flow.md had it at the park position (x −106), which would also blind the LW
  port.
- **Finer cells at the LW port** (1.5 mm across the wall, 2 mm over the recess): 285k cells against gas-flow.md's 178k.
  `checkMesh`: OK, no non-orthogonality.
- **Cases** (coarse mesh, k-ω SST, `simpleFoam`, 2 ranks; run one at a time on a shared runner):

  | Case | Bed + upper slot (L/min) | LW purge | Iterations |
  |---|---|---|---|
  | `p200` | 200 + 40 | off | 800 |
  | `p200_lw3` | 200 + 40 | 3 L/min | 400, from `p200` |
  | `p200_lw1` | 200 + 40 | 1 L/min | 200, from `p200_lw3` |
  | `p140` | 140 + 30 | off | 300, from `p200` |

  The probe 3 mm above the plate centre held within 0.5 % over each case's last 100–200 iterations (−3.23 m/s at
  200 + 40 L/min, −2.24 at 140 + 30). The upper vortex wanders as in gas-flow.md §0.7.

- **Particles** (`particles.py`, frozen flow, one-way): condensate as 30,000 tracers per release band, 6,000 from each of
  five points (the plate centre and ±25 mm in x and y), tracked for 20 s. Two bands: 0.5–5 mm (conduction and keyhole
  onset, §3.2) and 5–20 mm (a hard keyhole's plume top). Spatter of 20–200 µm from the same five points with the three
  speed distributions of §2.1, 1,200–1,500 per size and distribution.

### 1.2 Condensate

**Where it goes** (`p200`, 200 + 40 L/min, LW purge off; 30,000 tracers per band, tracked for 20 s):

| Released | Out through the floor slot in 8 s / 20 s | Median time out | Passed within 30 mm of the beam axis under the lid | Entered: laser slide recess | LW | LP | layer-camera bore | BW |
|---|---|---|---|---|---|---|---|---|
| 0.5–5 mm | 99.5 % / 100 % | 0.04 s | 0.7 % | 0.03 % | 0.01 % | 0.32 % | 0.08 % | 0.02 % |
| 5–20 mm | 94.8 % / 99.8 % | 0.07 s | 7.4 % | 0.28 % | 0.21 % | 2.8 % | 0.86 % | 0.16 % |

- **The bed jet does its job.** Whatever stays in it leaves in a tenth of a second. Even a plume released 5–20 mm up mostly
  leaves; 5 % is still in the chamber after 8 s and 0.2 % after 20 s.
- **Little settles back on the powder.** The CFD is isothermal, but the 200 °C plate pushes sub-micron particles away by
  thermophoresis: 0.5 ν ∇T/T ≈ 2 mm/s across a ~2 mm thermal layer at 150 K difference (estimate, argon at 400 K), ~1,000×
  what Brownian and turbulent deposition carry toward it.
- **The upper slot keeps the laser slide's recess clear.** The gas under it moves toward the door at 0.45 m/s, and only
  0.03–0.28 % of the condensate enters its recess (gas-flow.md had 0.1–0.2 % for the same layout).
- **The steep lid port, where monitoring.md put it, is the dirtiest window.** The ceiling sweep carries the risen plume
  toward the door and right past it at (−60, −80): 0.3–2.8 % enters its recess, ~10× the laser slide's share.

**How much there is next to each window**, as a concentration per unit source rate (C/S, s/m³; multiply by the source in
kg/s for kg/m³). In brackets: how many of the 30,000 tracers visited, so the counting noise is ~1/√ of it:

| Where | Released 0.5–5 mm | Released 5–20 mm |
|---|---|---|
| Laser slide, the 2 mm under it | 2.6 (1) | 110 (15) |
| LW slide, the 2 mm in front of it | 0 (0) | 430 (23) |
| LP slide, the 2 mm under it | 230 (46) | 1,860 (434) |
| Layer-camera bore, its top 4.5 mm | 44 (6) | 440 (74) |
| BW window, the 2 mm in front of it | 74 (2) | 510 (15) |
| Over the plate, z 0–20 mm (for scale) | 130 | 240 |
| Along the beam axis, z 20–120 mm, r < 5 mm | 22 (219) | 270 (3,381) |
| **Under the ceiling where the lid candidates would open:** (−60, −80), the LP as placed | 84 (210) | 740 (1,896) |
| (−40, 60) | 4.7 (34) | 38 (248) |
| (−20, 80) | 3.8 (24) | 29 (195) |
| (80, 80) | 37 (42) | 510 (572) |
| **Along the left wall at the LW height (z 22–44), outside any recess:** y −60 | 110 (26) | 910 (329) |
| y −20 (the LW) | 47 (28) | 610 (319) |
| y +20 | 42 (29) | 420 (223) |
| y +60 | 67 (22) | 550 (167) |

- **Move the steep lid port to the back half of the lid, under the upper slot's sweep** (|x| < 50). Under the candidates
  at (−40, 60) and (−20, 80), which monitoring.md §3 also found clear (57–62° views), the gas carries **~20–25× less
  condensate** than at (−60, −80) (10–40× across the four runs). There the ceiling gas is fresh from the upper slot; the
  candidate at (80, 80), beside the slot's end, gains little. It also moves the port's camera line away from the
  reservoir slot that monitoring_spec.py flags for (−60, −80). The room outside (30–80 mm to the optics bridge,
  monitoring.md §3) needs the CAD check.
- **The LW's own recess shelters its slide** from the low plume (no tracer reached it, against 47 in the wall layer
  outside), and a little from the high one (430 against 610). So keep the slide set back in its bore (4 mm here) rather
  than flush with the liner. Moving the LW along the wall changes little (420–910 along it).
- **The laser slide sees the least condensate of the five** (110 for the high release), but only 15 tracers made it, so
  read it as "a few times less than the camera windows".
- **The BW window**, low on the back wall beside the inlet slot (x −116, z 23), is as exposed as the LW. It is a light
  window, so it tolerates the most (§4).

**The LW purge, off, at 1 L/min and at 3 L/min** (`p200`, `p200_lw1`, `p200_lw3`; at 3 L/min the purge gas leaves the
1.5 × 22 mm slot at 1.5 m/s and crosses the slide at ~0.7 m/s):

| At the LW slide | Purge off | 1 L/min | 3 L/min |
|---|---|---|---|
| Gas 1 mm off the slide (m/s) | 0.015 | 0.22 | 0.82 |
| Friction velocity on it, u* (m/s) | 0.017 | 0.060 | 0.14 |
| Condensate in the 2 mm in front of it, C/S (s/m³), released 0.5–5 / 5–20 mm (tracers that visited) | 0 (0) / 430 (23) | 4.1 (13) / 33 (43) | 1.1 (6) / 9.3 (43) |
| In the whole recess (s/m³) | 5 (2) / 460 (63) | 33 (31) / 230 (212) | 13 (16) / 120 (162) |
| Deposition per unit source, 0.1 µm, isothermal (mg/m²/h per g/h of condensate) | 0 / 0.68 | 0.022 / 0.18 | 0.013 / 0.11 |

- **The purge keeps the condensate off the slide: ~13× less of it in front of the slide at 1 L/min and ~45× less at
  3 L/min** (high release). For the low release almost none reaches the slide either way.
- **The deposition falls less, ~4× at 1 L/min and ~6× at 3 L/min, in this model,** because the purge also scrubs the
  slide: its shear raises u* 3.5–8×, and Lai & Nazaroff's deposition velocity rises with it. That model is for a turbulent
  boundary layer; the purge's own layer is laminar (Re ≈ 100–160 at the slot), so the truth is likely nearer the 13–45×.
  If the slide is colder than the gas, the thermophoretic term doesn't depend on u*, and the purge cuts deposition the
  full 13–45×.
- **It pulls a little gas into the recess's mouth**: more tracers enter the recess with the purge on (0.5 % against
  0.2 %), but they stay out of the purged layer at the slide.
- The rest of the chamber doesn't notice 1–3 L/min against 240. Values elsewhere moved by up to ~2× between the runs
  (the left-wall layers by 0.5–2.6×, the laser slide's 2 mm layer by ~2×), which is the counting noise of volumes that a
  few tens of tracers visit, plus the upper vortex wandering. Read anything under a factor of ~2 as no difference.

### 1.3 Spatter in the flow

Share of Al spatter launches from the five plate points that end on each surface (`p200`; 1,200–1,500 per row):

| Speeds | d (µm) | Laser slide (Ø46 opening) | LW slide | LP slide | Back on the Ø75 plate | Floor | Outlet slot | Door side | Lid elsewhere |
|---|---|---|---|---|---|---|---|---|---|
| Al-like (median 2.5 m/s) | 20 | 0 | 0 | 0 | 0 | 26 % | 59 % | 16 % | 0 |
| | 50 | 0 | 0 | 0 | 0 | 3.4 % | 1.5 % | 95 % | 0 |
| | 100 | 1.5 % | 0.08 % | 0 | 2.5 % | 34 % | 4.6 % | 45 % | 3.8 % |
| | 150 | 3.1 % | 0 | 0 | 3.2 % | 31 % | 2.7 % | 28 % | 12 % |
| | 200 | 4.8 % | 0.08 % | 0 | 3.6 % | 25 % | 1.4 % | 21 % | 17 % |
| Half of Ly's | 100 | 4.1 % | 0 | 0.08 % | 1.5 % | 19 % | 3.7 % | 39 % | 15 % |
| | 200 | 6.3 % | 0 | 0.08 % | 1.9 % | 15 % | 0.9 % | 17 % | 28 % |
| Ly's (316L, Ti-6Al-4V) | 100 | 5.3 % | 0 | 0.17 % | 1.5 % | 21 % | 2.6 % | 18 % | 27 % |
| | 200 | 7.8 % | 0.08 % | 0.25 % | 0 | 2.5 % | 0.1 % | 14 % | 38 % |

The rest hits the drawer's rim round the laser slide (0.4–7 %), the side and back walls, and the parts in the gas. 20–50 µm
spatter never reaches a window: the bed jet takes it to the door (where the jet climbs, gas-flow.md §0) and the outlet. The
layer camera's bore and the BW window got none.

- **The laser slide is the window spatter finds.** It sits 126 mm straight above the plate, and droplets of 100–200 µm
  launched within ~10° of vertical at ≥ 5 m/s reach it while still liquid (§2.3). 1.5–5 % of them do at Al-like speeds,
  5–8 % at Ly's. No cross-flow that leaves the powder alone can turn them in 120 mm; gas-flow.md §3.6 found the same with
  its assumed launches.
- **The side and lid camera ports are almost out of spatter's reach:** 0–0.25 % per launch (one or two particles in
  1,200), within counting noise.
- **2–4 % of 100–200 µm spatter lands back on the plate**, on parts in progress, at Al-like speeds.

![Spatter on each window, condensate next to each window, and where spatter lands](../analysis/out/monitoring/plume/particles_p200.png)

*`p200`. Left: share of Al spatter launches that hit each window, against size, for the three speed distributions. Middle:
condensate concentration next to each window per unit source, for the two release bands (log scale). Right: where Al
spatter lands on the floor at Al-like speeds; dashed: the Ø75 plate; green: the outlet slot.*

**At 140 + 30 L/min (`p140`, 2.03 m/s at 3 mm over the plate)**, against 200 + 40:
- **More spatter lands back on the plate: 6–8 % of 100–200 µm spatter at Al-like speeds, against 2.5–3.6 %.** The slower
  bed jet carries less of it past the plate's edge. The laser slide's share is the same (1.3–5 %): that spatter goes
  straight up.
- 20 µm spatter goes to the outlet more (70 % against 59 %), as the slower jet carries less of it up the door.
- Condensate leaves a little more slowly (99.3 / 91.5 % in 8 s for the two bands, against 99.5 / 94.8 %) but all of it is
  out by 20 s (99.2–100 %).
- The lid ports trade places: the slower ceiling sweep halves what reaches the LP (850 against 1,860 s/m³ next to its slide)
  and doubles to triples what reaches the layer camera's bore (1,300 against 440). The back-half lid candidates stay
  13–15× cleaner than (−60, −80).
- **The LW purge doesn't change spatter** (`p200_lw3` and `p200_lw1` match `p200` within one particle per size): 3 L/min
  can't turn a 100 µm droplet.

## 2. Spatter on its own

### 2.1 What the literature gives for Al

| What | Al alloys | Steels, Ti-6Al-4V | Source |
|---|---|---|---|
| Speed | one laser-accelerated 36 µm particle went from 0.57 to 3.39 m/s in 350 µs (Al-Fe-Zr, synchrotron X-ray); mean speed rises linearly with intensity (AlSi10, AlSi7; values not retrieved) | hot entrainment 6–20 m/s (60 % of ejections), cold entrainment 2–4 m/s (25 %), recoil break-up of droplets 3–8 m/s (15 %); 316L in an EOS M290: mean 9.7 ± 6.7 m/s in one recording, 2.0 ± 2.0 m/s for one condition; molten spatter 3–8 m/s | Guo et al. 2024; Chebil et al. 2021; Ly et al. 2017; Barrett 2019; Ahmad 2019 (all via Edison) |
| Direction | mean −10° to −25° from vertical (backward), 70–80 % backward, at 350–500 W and 0.8 m/s; nearer vertical at 0.5 m/s | mean ~45° (Barrett) | Guo et al. 2024; Barrett 2019 |
| Size | more than half below 60 µm across at 4.24 MW/cm²; 140–160 µm droplets in every condition | ~90 % of ejecta within the 15–45 µm powder cut | Chebil et al. 2021; Williams 2022 |
| Kind | > 82 % solid (entrained powder), ~2 % jet spatter (Al-Fe-Zr) | 15 % molten, 60 % hot, 25 % cold (Ahmad) | Guo et al. 2024; Ahmad 2019 |
| Number | AlSi10Mg at 350 W, 1.6 m/s (VED 22 J/mm³, 200 °C plate): 10–20 particles under 63 µm and 2–6 over 63 µm in view at a time, in a 1.76 × 1.76 mm box behind the laser with 0.5 mm depth of field; more at higher VED | Barrett: ~1,500 tracked spatter events per second in an M290 | Nagato et al. 2023 (read), Barrett 2019 |

No count per mm of track and no speed distribution was found for Al. So the runs below use three speed distributions and
keep them apart:
- **fast**: Ly et al.'s mechanisms and speeds (6–20, 2–4 and 3–8 m/s), measured on 316L and Ti-6Al-4V;
- **half**: the same, halved;
- **Al-like**: lognormal, median 2.5 m/s, 95 % within 0.8–8 m/s, set from Guo's 3.4 m/s particle, Barrett's 2 m/s condition
  and Ahmad's 3–8 m/s for molten spatter.

Directions are uniform from 0 to 70° off vertical with a random azimuth: the scan direction turns from layer to layer, so
Guo's backward bias averages out over a build. Sizes are 20, 35, 50, 100, 150 and 200 µm, each run separately; the hit rates
in §4 weight them 35, 30, 20, 10, 4 and 1 % by number (Chebil's "more than half below 60 µm", Nagato's ~1 in 5 over 63 µm).
These are assumptions, and §4 gives their effect.

### 2.2 How high and how far

Schiller–Naumann drag in argon at 25 °C (1.65 kg/m³, 22.6 µPa·s) and gravity (`spatter.py`). Al at 2,670 kg/m³, steel at
7,900. Launched from 0.3 mm above the bed:

| d (µm) | v₀ (m/s) | Al: highest point, launched 80° up (mm) | Al: flight time, 80° (ms) | Al: range at 45°, still gas (mm) | Al: carried along the flow, 45° launch (mm) | Steel: highest point (mm) | Steel: range at 45° (mm) |
|---|---|---|---|---|---|---|---|
| 20 | 5 | 9 | 390 | 7 | 690 (it stays airborne) | 27 | 21 |
| 50 | 2 | 20 | 180 | 17 | 290 | 46 | 51 |
| 50 | 5 | 45 | 370 | 36 | 355 | 117 | 108 |
| 50 | 10 | 78 | 590 | 60 | 370 | 212 | 179 |
| 100 | 2 | 50 | 220 | 59 | 140 | 95 | 141 |
| 100 | 5 | 126 | 410 | 121 | 111 | 288 | 340 |
| 100 | 10 | 220 | 620 | 192 | 158 | 554 | 561 |
| 200 | 5 | 291 | 520 | 353 | 101 | 556 | 821 |

- **Al spatter flies a third to half as high as steel spatter of the same size and speed**, because it is a third as dense.
  Its Stokes relaxation time is 2.6 ms at 20 µm, 16 ms at 50 µm, 66 ms at 100 µm and 260 ms at 200 µm (×3 for steel).
- **The cross-flow takes the small spatter and leaves the big.** Particles up to ~50 µm are carried to the door and the
  outlet. 100–200 µm spatter is carried 100–160 mm along the flow over its 0.4–0.8 s flight, mostly inside the bed jet on
  the way up and down; on its way to the lid it crosses the jet in a few ms and keeps its line.
- **What reaches the lid (z 120–126 mm):** a 100 µm Al droplet needs ~5 m/s straight up, a 50 µm one ~16–20 m/s. With the
  fast speeds, 43–60 % of 100–200 µm Al spatter reaches the lid in a box chamber; with the Al-like speeds, much less (§1.3).
- **The LW port is hard to reach.** It looks in at 13° from 160 mm away, through a 4 mm recess. A particle must leave the bed
  within ~15° of horizontal toward −x and keep its speed for 140 mm. 0–0.1 % of launches do in the CFD (0–0.3 % in the
  box chamber), at every size and speed tried.

![Spatter: heights, cooling, and the share reaching each window](../analysis/out/monitoring/plume/spatter.png)

*Left: highest point of Al (solid) and steel (dashed) spatter launched 80° up in still argon; the dotted line is the lid.
Middle: cooling of Al droplets launched at 5 m/s from 2,200 K; the plateau is freezing. Right: share of launches reaching each
window in a box chamber with the 1-D cross-flow, for the three speed distributions.*

### 2.3 What the side camera sees of it

**Motion blur** is speed × exposure ÷ pixel (`spatter.py`; pixels at the plate from monitoring.md §3):

| Camera at the LW port | µm/px across the view | 2.5 m/s (Al-like median), 10 µs | 2.5 m/s, 30 µs | 5 m/s, 10 µs | 5 m/s, 100 µs | 10 m/s, 100 µs |
|---|---|---|---|---|---|---|
| Chronos 2.1-HD + 50 mm f/4 | 29 | 0.9 px | 2.6 px | 1.7 px | 17 px | 34 px |
| IMX296 + 50 mm f/2.8 (shortest exposure 30 µs) | 10 | – | 7.5 px | – | 50 px | 100 px |

- **Use 10–20 µs.** At the Al-like speeds (median 2.5 m/s) a 10 µs frame on the Chronos blurs spatter by under a pixel to
  ~3 pixels, so speed and direction can be read from two frames. At 100 µs every spatter is a streak, which is also a way to
  measure speed in one frame.
- **Nagato et al. 2023 saw the plume's light swamp a 645 ± 10 nm image above 100 µs**, even with 280 W of pulsed laser
  light. That is the other reason to keep exposures short, or to pulse the light.
- Edison's "≤ 2.9 µs for 10 µm of blur" is for a 10 µm pixel; at the LW port's 29 µm/px, 10 µs is enough.

**How long spatter glows.** Each droplet cools by convection (Ranz–Marshall, argon at the film temperature) and radiation
(emissivity 0.15), with latent heat over the freezing range. A Biot number of ~10⁻⁴ makes it one temperature throughout.
Convection carries ~10–30× more heat than radiation (at 2,000 K, from 200 down to 50 µm). A camera sees a droplet by its
own light while the photoelectrons per pixel stay above ~100 (5× a ~20 e⁻ read noise), with a grey emissivity of 0.15
and the blur spread over the pixels:

| Al droplet, launched at 5 m/s from 2,200 K | Liquid for | Chronos at LW, 850 ± 5 nm, 10 µs: glows above / for | Chronos, 450–950 nm, 10 µs | IMX296 at LW, 850 ± 5 nm, 30 µs | Layer camera (Pi HQ, its 400–650 nm IR-cut filter), 10 ms |
|---|---|---|---|---|---|
| 35 µm | 13 ms | 1,582 K / 2.1 ms (8 mm of flight) | 1,181 K / 4.5 ms (14 mm) | 1,816 K / 1.2 ms (5 mm) | 1,822 K / 1.1 ms |
| 50 µm | 26 ms | 1,554 K / 4.3 ms (16 mm) | 1,165 K / 8.9 ms (27 mm) | 1,763 K / 2.6 ms (11 mm) | 1,775 K / 2.5 ms (10 mm) |
| 100 µm | 94 ms | 1,514 K / 16 ms (60 mm) | 1,142 K / 33 ms (94 mm) | 1,681 K / 11 ms (45 mm) | 1,689 K / 11 ms (44 mm) |
| 200 µm | 342 ms | 1,489 K / 60 ms (203 mm) | 1,128 K / 121 ms (308 mm) | 1,623 K / 44 ms (164 mm) | 1,610 K / 46 ms (168 mm) |

- **Through a 10 nm filter at 850 nm, spatter is self-luminous only above ~1,500 K**: small spatter for the first few mm,
  100–200 µm droplets for most of their flight. Broadband (450–950 nm, behind the 1070 nm notch) adds ~400 K of range.
- **With an 808/850 nm diode light and the matching filter, the camera sees everything that crosses the beam of light**,
  hot or cold: entrained powder, which is most of the ejecta (> 82 % solid in Guo's Al-Fe-Zr), shows only by light. So the
  light, not the glow, is what makes powder entrainment and denudation visible.
- **The layer camera's 10 ms frames record only the hottest droplets**, as streaks 50 mm long at 5 m/s. Its stills between
  layers miss all of it.
- **Large droplets reach the lid still liquid.** A 100 µm droplet stays liquid for ~94 ms and reaches 126 mm in ~30–60 ms,
  so it hits the laser slide molten and sticks. A 50 µm one is solid after ~26 ms.

## 3. The vapour plume

**The source terms are worker A's** (melt-pool model, [`analysis/out/monitoring/melt/plume_source.json`](../analysis/out/monitoring/melt/plume_source.json)).
This note uses two of its readings and says which:
- **for the jet, its `exit` state at the depression wall** (`wall`: Knight jump at the hottest point, Mach 0.43);
- **for the condensate, its `best` reading**: Mg and Zn at the rates measured LPBF losses imply (its Hertz–Knudsen–Langmuir
  over-predicts Mg ~10×), and Al from the `wall` reading.

`plume_jet.py --source <file>` reads it (results under `worker_A` in `plume_jet.json`). The scenarios below the table are this
note's own cross-check, made before A's file existed: surface temperatures as scenarios, vapour pressures from
Clausius–Clapeyron anchored at each element's boiling point (CRC Handbook: Al 2,792 K and 294 kJ/mol, Mg 1,363 K and
127 kJ/mol, Zn 1,180 K and 115 kJ/mol, Si 3,538 K and 359 kJ/mol), and Raoult's law over the alloy.

| Worker A, 320 W, 96 µm, 200 °C plate (7075: 25 °C plate) | AlSi10Mg, 1.1 / 0.6 m/s | 6061, 1.1 / 0.6 m/s | 7075, 1.1 / 0.6 m/s |
|---|---|---|---|
| Depression wall: T_s, exit speed (Mach 0.43) | 2,763 K, 478 m/s | 2,508 K, 464 m/s | 1,839 K, 265 m/s |
| Vapour leaving the wall's hot area (`wall` reading, all elements) | 1.1 / 1.2 g/h | 1.4 / 1.6 g/h | 4.9 / 5.2 g/h |
| **Condensate, `best`** (g per hour of lasing) | **0.47 / 0.50** | **0.19 / 0.18** | **0.44 / 0.24** (0.61 / 0.42 with a Zn- and Mg-depleted surface) |
| … per mm of track | 0.12 / 0.23 µg | 0.05 / 0.08 µg | 0.11 / 0.11 µg |
| … its composition (mol) | 85 % Al, 15 % Mg | 69 % Al, 31 % Mg | 55 % Zn, 44 % Mg |
| Jet momentum length L_m at 200 / 140 L/min (this note) | 3.2 / 4.6 mm | 3.6 / 5.2 mm | 5.1 / 7.3 mm |
| Plume centreline 10 mm downstream, 200 / 140 L/min | 11 / 14 mm | 12 / 15 mm | 15 / 19 mm |
| Primary particles (this note's coagulation model) | 3 nm | 3 nm | 6 nm |

*From 200 to 400 W at 1.1 m/s A's `best` runs 0.10–0.64 g/h for AlSi10Mg and 0.07–0.24 g/h for 6061. At 200 W AlSi10Mg
has no jet (the wall stays below its boiling point).*

### 3.1 What evaporates, and when there is a jet

- **The alloys "boil" (total vapour pressure 1 atm) well below aluminium's 2,792 K:** AlSi10Mg at 2,549 K, 6061 at
  2,256 K and **7075 at 1,673 K**, because of their Mg and Zn (Raoult; A gets 2,539, 2,259 and 1,675 K).
- **Raoult puts Mg and Zn in the vapour** (59–96 mol % Mg over AlSi10Mg). **The measured losses say the surface runs out
  of them**: A's calibrated `best` vapour over AlSi10Mg and 6061 is 69–85 mol % Al. Over 7075 it stays Zn and Mg. So the
  condensate of AlSi10Mg and 6061 is mostly Al, and the deposit optics of §4.2 (Al) fit it.
- **Below the alloy's boiling point there is no jet.** Vapour diffuses into the argon over the hot spot. At 2,000–2,300 K
  that is 0.001–0.005 g per hour of lasing from a hot spot half the beam's area: almost nothing.
- **Above it, the vapour leaves as a jet.** Knight's (1979) jump conditions across the Knudsen layer, with 1 atm outside:

| Scenario (AlSi10Mg; 6061 and 7075 in `plume_jet.json`) | T_s | Vapour pressure | Jet speed | Mass out, from a Ø67 µm keyhole mouth | Momentum flux |
|---|---|---|---|---|---|
| Conduction, 2,000 / 2,300 K | 2,000 / 2,300 K | 0.15 / 0.44 atm | none | 0.0004 / 0.001 g/h | – |
| Keyhole onset, 1.2 atm | 2,607 K | 1.2 atm | 113 m/s (Mach 0.10) | 0.18 g/h | 5.5 µN |
| Keyhole, 2 atm (recoil + capillary pressure of a ~30 µm keyhole) | 2,771 K | 2 atm | 441 m/s (Mach 0.39) | 0.74 g/h | 90 µN |

- **The 2 atm row matches A's depression wall** (2,771 against 2,763 K, 441 against 478 m/s, Mach 0.39 against 0.43).
  Both jet speeds sit inside the 20–300 m/s to "hundreds of m/s" found for LPBF vapour jets (Guo et al. 2024; Bitharas
  et al. 2022) and above the 38–97 m/s plume ascent Mayi et al. (2020) measured at 0.57–1.14 MW/cm²; our peak intensity
  is ~10 MW/cm² at 350 W.
- **The mass leaving the wall overstates the condensate**, because its Mg comes from Raoult. A's `best` (0.47 g/h for
  AlSi10Mg) uses the measured Mg loss instead; it sits between this note's keyhole-onset (0.18 g/h) and 2 atm (0.74 g/h)
  rows. §4 uses A's `best`.

### 3.2 How high it gets in the cross-flow, and its tilt

The jet bends over within its momentum length L_m = √(J / ρU²) and then rises slowly, z ≈ 2.3 L_m (x / L_m)^(1/3)
(momentum-dominated jet in cross-flow; Hasselbrink & Mungal 2001). Without a jet, the hot gas rises as a bent-over buoyant
plume, Δz = 1.6 F^(1/3) x^(2/3) / U (Briggs). Cross-flow at 2.95 m/s (200 L/min) and 2.03 m/s (140 L/min) at 3 mm:

| Regime | L_m at 200 / 140 L/min | Centreline 10 mm downstream | 50 mm downstream |
|---|---|---|---|
| Conduction (no jet) | – | 0.4 / 0.6 mm | 1.1 / 1.7 mm |
| Keyhole onset | 0.6 / 0.9 mm | 3.6 / 4.6 mm | 6.2 / 7.9 mm |
| Keyhole, 2 atm | 2.5 / 3.7 mm | 9.2 / 11.8 mm | 16 / 20 mm |

![Vapour pressure, plume rise and condensate optics](../analysis/out/monitoring/plume/plume_jet.png)

*Left: vapour pressure over each alloy and its pure elements. Middle: AlSi10Mg's plume centreline at 200 L/min (solid) and
140 L/min (dashed); grey is the fixed layout's ~20 mm bed jet. Right: Mie mass coefficients of Al and alumina spheres.*

- **With A's source terms the jet reaches the top of the bed jet.** At 320 W its momentum (~140 µN for AlSi10Mg) gives
  L_m ≈ 3–5 mm and a centreline 11–19 mm up 10 mm downstream: the 2 atm row, and the 5–20 mm release band of §1.2.
- **Measured plumes are lower.** Bitharas et al. (2022, SS316 at 0.75 m/s) saw the plume "dissipated within the convective
  flow after propagating upwards for ~1 mm" in a 2.1 m/s cross-flow, which is the keyhole-onset row; Shi et al.'s review
  (2024) gives a visible plume 4–5 mm high and ~1.5 mm wide. The scaling is for a steady jet in a uniform cross-flow, and
  the vapour jet is a few hundred µm of hot gas that starts inside the bed's boundary layer, so read 1–20 mm as the range
  and both release bands of §1.2 as its two ends.
- **Tilt:** past ~1 mm the centreline runs only 5–10° above the bed, downstream. In the moving source's frame the gas
  speed is the cross-flow minus the scan: at 1.1 m/s, 1.85 m/s scanning with the flow and 4.05 m/s against it. Heights
  scale as U^(−2/3), so scanning with the flow lifts the plume ~1.4× and against it ~0.8×.
- **At 140 L/min every height is ~1.3× the 200 L/min one.**

### 3.3 What it condenses into

- **Primary particles: 3–8 nm in a jet (3–6 nm with A's exit states), 30–110 nm without one** (`plume_jet.py`):
  free-molecular coagulation with full coalescence until the gas cools below ~900 K (650 K for Zn-rich 7075 condensate).
  In a jet the vapour mixes with argon and cools that far within 0.3–0.65 mm and 1–16 µs, so the particles have little
  time to grow. Without a jet it cools slowly in the hot boundary layer (~5 ms), and they grow larger.
- **Measured, for comparison (stainless steel, no Al data found):** primary particles 4–16 nm, median 9.4 nm, with a metal
  core and oxide shell above ~30 nm (Noskov et al. 2020), in chain-like agglomerates 0.5 to > 10 µm long (Noskov et
  al. 2022). The jet case agrees.
- So the condensate that reaches a window is agglomerates of ~3–15 nm particles, Al-rich from AlSi10Mg and 6061 and Zn-
  and Mg-rich from 7075 (§3.1), partly oxidised. How much depends on the chamber's O₂ (not modelled); in air, at the next
  slide change, the rest oxidises.

### 3.4 What it does to the beam and the coaxial signal

Mie extinction of the condensate, per kg (Al from Rakić 1995; alumina from Boidin et al. 2016):

| Al spheres | 10 nm | 20 nm | 100 nm | 300 nm | 1 µm |
|---|---|---|---|---|---|
| at 1.07 µm (m²/kg) | 54 | 70 | 347 | 3,900 | 1,370 |
| at 0.85 µm (m²/kg) | 218 | 266 | 1,084 | 5,396 | 1,384 |

Alumina spheres under 50 nm don't absorb and barely scatter (< 1 m²/kg). Al absorbs ~4× more at 850 nm than at 1070 nm
(its interband absorption near 800 nm).

- **Above the spot:** the beam crosses the plume's own column of condensing metal. With A's source terms (320 W,
  `best`) it is 19 mg/m² for AlSi10Mg, 7 for 6061 and 31 for 7075. As 20 nm primaries that is an optical depth of
  **0.13 % (AlSi10Mg), 0.05 % (6061) and 0.22 % (7075) at 1070 nm, and ~4× those at 850 nm (0.2–0.8 %)**. This note's
  scenarios, which count all the vapour as condensing, give up to 0.3 % (AlSi10Mg) and 1.4 % (7075) at 1070 nm. In
  conduction mode the column is ~100–400× smaller. Fully grown 300 nm agglomerates would extinguish ~50× more per mass,
  but they form ms later, downstream.
- **The plume doesn't steer or defocus the beam measurably:** hot argon and metal vapour change the refractive index by
  ~10⁻⁴ over ~1 mm, which moves the beam by under a µm (estimate). Edison found no evidence of a plasma in CW LPBF of Al at
  1 µm, only weakly ionised vapour; none is expected at ~10 MW/cm².
- **The coaxial photodiode looks back through the same column.** At 700–900 nm it loses ~0.2–1 % to the plume (up to
  ~5 % if all the vapour condensed), more in 7075 and in keyhole mode, and the loss fluctuates with the keyhole. It is
  one more reason to use the two-colour ratio (monitoring.md §2.2), in which a grey loss cancels. Al's extinction falls by
  ~27 % from 700 to 900 nm (20 nm spheres), so it cancels only partly: a 2 % loss at 700 nm biases a 700/900 nm ratio by
  ~0.5 %, ~5 K at 2,000 K.
- **Away from the spot, the chamber's background is negligible.** Along the beam axis (z 20–120 mm) the CFD gives C/S of
  22–270 s/m³ (§1.2), so 3–35 mg/m³ of condensate at A's 0.47 g/h for AlSi10Mg (about the same for 7075). Over the
  100 mm path that is an optical depth of ~0.06 % as agglomerates of 10 nm primaries (absorption ~70 m²/kg plus their
  scattering ~100 m²/kg, a Rayleigh–Debye estimate), and at most ~1.4 % if it were all compact 300 nm particles.

### 3.5 What the side camera sees of the plume

- The hot vapour and fresh condensate glow. A side view through ~1.5 mm of plume at ~2,000 K, with an absorption optical
  depth of ~2 × 10⁻³ at 850 nm, is ~400× dimmer per unit area than a 2,500 K pool with emissivity 0.15. But at 13° the
  pool's projected area is tiny (0.2 × 0.3 mm × sin 13°) and the plume's is ~6 mm². **So in a side view the plume shines
  about as brightly in total as the pool** (estimate, continuum only; Al I, Mg I and Na lines fall outside 600–1000 nm per
  Edison, and K I 766/770 nm, if present as an impurity, falls inside it).
- It leans downstream, ~5–10° above the bed past the first mm, across the LW camera's view (the flow runs in −y, the camera
  looks along +x). Its length and tilt are a direct read-out of the cross-flow at the bed.
- The condensate cloud further downstream is too thin to see without light: an optical depth of ~10⁻³.

## 4. Window fouling

### 4.1 How much condensate there is

No fume rate for Al LPBF was found (Edison agrees). **This note uses worker A's `best` reading** (§3): Mg and Zn at the
rates measured composition losses imply (57 % of AlSi10Mg's Mg and 17 % of 6061's, Li 2024 via Edison; 12 % of 7075's Mg
and 18 % of its Zn, Velikajne et al. 2026), plus the Al its depression-wall reading evaporates. Nominal = the 320 W,
1.1 m/s case on a 200 °C plate. The **lower bound** counts only the measured Mg and Zn (with the Al that Raoult sends
with them: ×1.5 for AlSi10Mg, ×1.07 for 6061, ×1.0 for 7075), at 0.4–1.1 m/s:

| Alloy | Condensate, g per hour of lasing: A's `best`, nominal (A's cases) | Lower bound: measured Mg and Zn only |
|---|---|---|
| AlSi10Mg | **0.47** (0.10 at 200 W – 0.64 at 400 W) | 0.035–0.095 |
| 6061 | **0.19** (0.07–0.24) | 0.021–0.058 |
| 7075 | **0.44** (0.24–0.61; 25 °C-plate cases) | 0.078–0.72 (Mg 19 %, Zn 3–30 %) |

- **Most of the AlSi10Mg and 6061 condensate is Al evaporated from the keyhole wall** (85 and 69 mol %), which no
  measurement constrains: that is why A's rate is 5–8× the Mg-only bound. It is the term to measure (§4.5).
- **7075 and AlSi10Mg make about the same mass; 6061 about 40 % of it.** 7075's is Zn and Mg.
- Every deposition rate below scales linearly with this source.

### 4.2 How much deposit each window can take

A deposit on fused silica, at normal incidence (`fouling.py`, characteristic-matrix method), with the same mass laid down
two ways:

| Window and limit | As a continuous Al film | As isolated Al nanoparticles, 10 % filled (Maxwell Garnett) |
|---|---|---|
| Laser slide: 0.03 % absorbed at 1070 nm (optics.md §2.2: beyond it the spot grows > 10 %) | 0.007 mg/m² (0.003 nm) | 7 mg/m² (2.7 nm equivalent) |
| Camera slide: 10 % less light at 850 nm | 1.1 mg/m² (0.4 nm) | 570 mg/m² (210 nm) |
| Light window: 20 % less light | 2.3 mg/m² | 1,070 mg/m² |

![Deposit optics](../analysis/out/monitoring/plume/fouling.png)

*Absorption and transmission loss against the mass deposited, as a continuous Al film (orange), isolated Al particles
(blue) and alumina (green), at 1070 nm (solid) and 850 nm (dashed).*

- **The two bounds are ~1,000× apart, and the truth is between them.** A deposit a few nm thick can't be a continuous
  film: it is islands of particles, so the left column overstates it. But the condensate comes as chains (§3.3), which
  absorb more per mass than isolated spheres, so the right column understates it. Oxidation pulls toward the right
  (alumina, MgO and ZnO absorb nothing here). Neither column includes the haze a thick porous deposit scatters, which
  will limit camera contrast before absorption does.
- **The laser slide is ~100× more sensitive than a camera slide** for the same deposit.
- **Both columns use aluminium's optics.** That fits AlSi10Mg and 6061, whose condensate is mostly Al by A's `best`
  (§3.1). 7075's is Zn and Mg: small metallic Mg particles absorb ~2.6× less than Al near 850 nm, where Al has an
  interband absorption (Im[(ε−1)/(ε+2)] is 0.010 for Mg, ε = −63 + 13i at 0.83 µm, Hagemann et al. 1975, against 0.025
  for Al, −60 + 44i, Rakić 1995), and the oxides absorb nothing. So for 7075, Al is the pessimistic choice.

### 4.3 How fast each window gets there

Deposition J = v_d × C next to each window (§1.2), with v_d from Lai & Nazaroff (2000) for a 0.1 µm agglomerate (mobility
size of a ~0.5 µm chain) and the CFD's friction velocity on each window. Source: worker A's `best` for AlSi10Mg at 320 W,
1.1 m/s, 0.47 g/h (7075 ≈ the same, 6061 × 0.4). **Per hour of lasing**, in `p200` (200 + 40 L/min, LW purge off):

| Window | v_d (m/s) | Deposit, released 0.5–5 / 5–20 mm (mg/m² per h) | Same, slide 10 K colder than the gas | Hours to its limit at 5–20 mm, isolated particles (continuous film) | Same, 10 K colder |
|---|---|---|---|---|---|
| Laser slide | 5.0 × 10⁻⁶ | 0.006 / 0.25 | (it runs warmer) | **29** (0.03) | – |
| LW slide | 1.6 × 10⁻⁶ | 0 / 0.32 | 0 / 22 | 1,800 (3.4) | 26 (0.05) |
| LW slide, 3 L/min purge (`p200_lw3`) | 1.2 × 10⁻⁵ | 0.006 / 0.054 | 0.06 / 0.52 | 11,000 (20) | 1,100 (2.1) |
| LP slide (−60, −80) | 4.3 × 10⁻⁶ | 0.46 / 3.8 | 12 / 97 | **150** (0.3) | 6 (0.01) |
| Layer-camera bore | 1.5 × 10⁻⁶ | 0.03 / 0.32 | 2.2 / 23 | 1,800 (3.4) | 25 (0.05) |
| BW window | 0.9 × 10⁻⁶ | 0.03 / 0.22 | 3.8 / 26 | 4,900 (10) | 42 (0.09) |

*AlSi10Mg at A's 0.47 g/h; 7075 is about the same and 6061 about 0.4× (§4.1). Against the Mg-only lower bound the hours are
5–8× longer. The laser slide's v_d is for a downward-facing surface. Hours to the limit from the 5–20 mm release, which
A's jets reach (§3.2); the 0.5–5 mm release gives 7–40× longer (and none reached the LW slide). The near-face values
behind them rest on 15–430 tracers (§1.2), so take them to within ~2×.*

- **Thermophoresis decides it.** A window 10 K colder than the gas next to it collects 20–120× more than an isothermal
  one: 0.5 × ν ∇T/T ≈ 1 × 10⁻⁴ m/s across a 2 mm layer, against 1–5 × 10⁻⁶ m/s for Brownian and turbulent
  deposition. The other way round, **a camera slide kept a few K warmer than the gas repels sub-micron condensate.** The
  laser slide, which absorbs some beam, is warmer than the gas already. A heated window costs a resistive ring or an ITO
  coating and a thermistor per port (not priced).
- **As isolated particles on a slide no colder than the gas, condensate costs the camera slides 10 % of their light in
  150 h of lasing (LP as placed) to thousands of hours (LW, layer camera, BW).** If it forms a continuous film, the LP as
  placed loses 10 % in ~0.3 h and the others in 3–10 h; 10 K colder, in minutes.
- **The laser slide is the most sensitive window.** With A's source and the high release, condensate takes it to the
  0.03 % absorption limit in ~30 h of lasing as isolated particles (~1,200 h from the low release), and within an hour as
  a continuous film. So the laser slide needs the per-build check for condensate too, not only for spatter (§4.4).

### 4.4 Spatter on the slides

Hits per hour of lasing, at an assumed **100 spatters per second of lasing** (this size mix is ~0.3 g/h, 1–3 % of the metal
deposited; no Al count was found) and a splat 2.75 d across for molten droplets of ≥ 50 µm (Pasandideh-Fard et al. 1996):

| Window (`p200`) | Al-like speeds: hits / splat area (mm²) per h | Ly's speeds | Its open area (mm²) |
|---|---|---|---|
| Laser slide | 1,160 / 133 | 3,220 / 311 | 1,660 (Ø46) |
| LW slide | ~30 / 2.5 (one particle in 1,200) | ~3 / 0.7 | 490 |
| LP slide | 0 | 93 / 8.9 | 310 |
| BW window, layer-camera bore | 0 | 0 | |

*At 140 + 30 L/min the laser slide gets the same (1,050 / 123 and 3,300 / 322).*

- **Spatter sets the laser slide's life, with condensate close behind.** At the assumed rate it gathers ~8–19 % of its
  open area in splats per hour of lasing. A molten Al splat in the beam absorbs part of the 25–120 W/mm² that crosses the
  slide at 500 W (a 3.2–5 mm beam there, optics.md §2.2) and can burn in or crack it. That is a consumable changed every
  few hours of lasing unless the real spatter rate is much lower. It scales directly with the spatter rate, which nobody
  has measured for Al; condensate alone would take it to its absorption limit in ~30 h (§4.3).
- **Where the beam crosses the slide matters most.** 126 mm above focus the beam is 3.2–5 mm across. With the spot at the
  Ø75 plate's edge its chief ray is tilted 13°, so at the slide it sits only ~7.5 mm off-centre (37.5 − 126 × tan 13°).
  The beam uses the central ~Ø20 mm of the Ø46 opening, about a fifth of it. Change the slide when splats appear there.
- **The camera ports barely see spatter:** under 1 % of their area per hour even at the fast speeds.

### 4.5 So: how often to change slides, and is the LW purge worth it?

| Window | What limits it | Change it | Notes |
|---|---|---|---|
| Laser slide | molten spatter (§4.4); condensate within ~30 h of lasing (§4.3) | **inspect after every build; expect to change it every few hours of lasing** until the splat count and its absorption are measured | it sees the least condensate of any window, thanks to the upper slot, but tolerates ~100× less |
| LW slide | condensate, slowly; spatter rarely | at the per-build transmission check, when it has lost ~10 % | the cleanest camera port; with the purge, cleaner still |
| LP slide at (−60, −80) | condensate: the dirtiest window | as LW, but it fouls ~12× faster | **move it to (−40, 60) or (−20, 80)**: ~20× less |
| Layer-camera window | condensate in its 16 mm bore; its window sits higher, in the boss | rarely | already behind a deep bore |
| BW light window | condensate | rarely; it only has to pass light | 20 % loss is fine |

**The LW purge is worth fitting, cheaply, and running when it matters:**
- It cuts the condensate at the LW slide ~13× at 1 L/min and ~45× at 3 L/min (deposition 4–6× by the turbulent model,
  more for a laminar purge layer; §1.2), for 0.4–1.2 % of the loop's flow. Its gas should come from the loop after the
  HEPA filter (a needle valve on a branch, like the slide purge in gas-flow.md §0), not from the cylinder, so it costs no
  argon.
- The LW slide is already the cleanest camera window, so the purge matters most for 7075, for keyhole-mode parameters, and
  if the slide runs colder than the gas.
- Machining the slot into the LW adapter costs little when the adapter is made (monitoring.md §0 item 1), and it can stay
  shut.
- **Warming the slide does the same job by another route** (§4.3): a slide a few K above the gas repels condensate by
  thermophoresis. A purge and a warm slide together leave only spatter, which barely reaches the LW (§1.3).

**What to measure on the first builds** (none of it published for Al, per Edison):
- the transmission of every slide before and after each build (an LED and a photodiode through the slide, or the layer
  camera's flat-field), against lasing hours and alloy;
- the splats on the laser slide per hour of lasing, under a microscope, which gives the spatter rate this note assumes;
- the condensate on a witness slide at the LW and LP positions, weighed or measured by transmission;
- the spatter speeds, angles and counts with the LW camera itself (§2.3), which replaces the assumed launch.

## 5. When does the plume reach the beam path?

A scaling argument in place of a transient CFD of a plume puff (not run; §7):

- **The beam always crosses its own plume** in the first 1–5 mm above the spot (§3.4). That costs ~0.05–0.2 % at 1070 nm
  (≤ ~1 %) and can't be avoided; the cross-flow only decides how long the plume stays near the next track.
- **It crosses an older plume only if the gas is too slow to clear the plume's width between passes.** Successive hatch
  vectors are ~0.1 mm apart and, for a 10 mm vector at 1 m/s, ~10 ms apart. In that time the bed jet carries the plume
  20–30 mm downstream (2–3 m/s at 1–3 mm). The plume is ~1.5 mm wide (Shi et al. 2024). So the beam meets old condensate
  only if the gas over the spot is slower than ~1.5 mm / 10 ms ≈ 0.15 m/s: a 15–20× margin at 140–200 L/min.
- **The margin shrinks at short vectors and turnarounds.** A 1 mm vector at 1 m/s returns in ~1 ms, by when the plume has
  moved only 2–3 mm: about two plume widths. So small features, contours and the skywriting at vector ends are where the
  beam can see its own recent plume.
- **Scan against the flow when you can.** Moving upstream (+y) the beam runs away from its plume; moving downstream (−y) at
  1.1 m/s it chases a plume that moves only 1.85 m/s faster than it. That is also the usual advice for commercial machines.
- **Off the plate centre the beam is tilted** (up to 13° at the Ø75 plate's edge with f = 160 mm), so above the spot it
  leans back toward the plate centre. At the upstream edge of the plate (+y) it leans downstream over its own plume and
  crosses it 0.2–1 mm downstream of the spot, 1–5 mm up (keyhole onset to hard keyhole, from §3.2's trajectories). That
  is the same near-field column as before, not old plume.
- **The upper chamber's slow recirculation is where old condensate meets the beam.** Along the beam axis above 20 mm the
  CFD's concentration is 0.2–1× the average over the plate's lowest 20 mm (C/S 22–270 against 130–240 s/m³): the
  condensate that rises out of the bed jet mixes through the upper chamber before it leaves. §3.4 shows it costs the beam
  under 0.1 %.

## 6. Against Edison's answers

[`r8-melt-plume`](../edison/r8-melt-plume/answer.md) and [`r8-viewports`](../edison/r8-viewports/answer.md)
(LITERATURE_HIGH, 2026-11-25). Where they agree with this note:
- a plume that rises ~1 mm before a ~2 m/s cross-flow takes it (Bitharas et al. 2022), 4–5 mm high and ~1.5 mm wide (Shi
  et al. 2024), with vapour-jet speeds of 20–300 m/s: §3.2's keyhole-onset row;
- no plasma at 1 µm in CW Al LPBF; the plume and its lines mostly outside 600–1000 nm;
- condensate primaries of ~10 nm in micron-long chains (Noskov et al., steel);
- large Mg and Zn losses from Al alloys, so a Mg- and Zn-rich vapour (§3.1);
- backward, mostly solid, Al spatter at a few m/s (Guo et al. 2024);
- nobody has published a window or cover-slide transmission loss per build hour for Al, nor a fume rate per joule: they
  have to be measured on this machine (§4.3).

Where this note differs or adds:
- **Mg loss of 57 % for AlSi10Mg.** Edison takes it from a 2024 thesis's compilation (Li 2024), with 17 % for 6061 and
  19 % Mg and 3–30 % Zn for 7075; worker A uses the first two and Velikajne et al. 2026 for 7075 (12 % Mg, 18 % Zn).
  Neither this note nor A has seen the primary sources behind Li's numbers. Losing 57 % of AlSi10Mg's 0.35 wt % Mg
  (0.2 wt %) takes keyhole-mode evaporation on most tracks; conduction-mode tracks would lose ~100× less (§3.1). Treat
  it as an upper value until the first coupons are analysed. It is only 13 % of A's AlSi10Mg condensate anyway; the Al
  from the keyhole wall is the rest, and nobody has measured it.
- **"Windows downstream receive more condensate."** In this chamber, with the upper slot sweeping the ceiling toward the
  door, that holds for the lid (the front lid port is the dirtiest window), but the two side windows are low and in
  recesses, and get ~10× less than the front lid port (§1.2).
- **"Exposure ≤ 2.9 µs to keep blur to 10 µm"** is right for 10 µm pixels; at the LW port's 29 µm/px, 10 µs keeps the
  blur near a pixel for Al spatter (§2.3).
- **Plume attenuation "a few percent per pass" from the welding literature** is too high for 200–350 W; §3.4 gives
  ~0.05–0.2 % at 1070 nm with worker A's source terms, and at most ~1 % if all the vapour condensed above the spot.
- **Sacrificial cover slides of borosilicate or soda-lime glass** (r8-viewports) are fine for the camera ports, as long as
  each camera keeps its own 1070 nm blocking filter (monitoring.md §6); the laser slide stays fused silica (optics.md
  §2.2).

## 7. Not done, and limits

- **Nothing is measured.** No Al fume rate, no Al spatter count per mm of track and no slide transmission loss per hour
  was found in the literature (Edison agrees). Every rate in §4 scales with two inputs: the condensate rate, worker A's
  `best` (most of it modelled Al evaporation, the rest measured Mg and Zn losses; 5–8× the Mg-only bound for AlSi10Mg and
  6061), and the spatter rate, an assumed 100 per second of lasing. The first builds should measure both (§4.5).
- **The CFD is isothermal and steady**, as in gas-flow.md: no 200 °C plate, no hot plume, no thermophoresis in the flow.
  - The plate's buoyancy lifts condensate out of the bed jet, and thermophoresis pushes it away from the hot bed (it
    doesn't land on the powder). The 5–20 mm release stands in for what rises.
  - The upper vortex wanders by ±25 % (gas-flow.md §0.7), so the lid windows' numbers are one snapshot.
  - Coarse mesh (285k cells; 1.5–2 mm at the LW recess, 2.25–4.5 mm elsewhere). The recesses are 2–6 cells deep, so the
    flow inside them is resolved only roughly. No mesh check was run for these cases.
- **Condensate is a tracer with turbulent and Brownian diffusion.** No agglomeration, no settling (under 0.1 mm/s), no
  thermophoresis in the random walk. Deposition is J = v_d × C next to the face, with v_d from Lai & Nazaroff (2000) for
  smooth surfaces and a thermophoretic term for a window 10 K colder than the gas. Tracer counts are 30,000 per release
  band, but the small control volumes in front of the windows are visited by only a few to a few hundred of them
  (`summary.md` lists the counts). So values there can move by 2× or more between runs, and more for the rarest (the BW
  window's and the laser slide's 2 mm layers, 9–23 tracers). The rankings and the large factors (the LP's ~20×, the
  purge's 13–45×) hold across the runs.
- **Spatter launch is assumed** (§2.1), and the fates of 100–200 µm spatter depend on it more than on the flow. Spatter is
  one-way coupled, without turbulent dispersion, and sticks wherever it first touches. Splat size is one formula
  (ξ = 0.5 Re^0.25).
- **Geometry.** Round bores are equal-area squares, straight through their wall rather than along the line of sight. The
  BW bore's 48° obliquity and the layer camera's boss above the lid aren't modelled. The cover-slide depths (4 mm) are
  assumptions until the CAD worker draws them. The LW purge is a 1.5 × 22 mm slot at 1.5 m/s (3 L/min); a real gas knife
  would be thinner and faster.
- **The plume's rise is a scaling, not a simulation.** The jet's exit state and mass come from worker A (its `wall`
  exit, its `best` mass; A's own limits apply, notably that Al evaporation from the keyhole wall is modelled, not
  measured, and that 7075 on a 200 °C plate wasn't in A's file during this run). The jet-in-cross-flow and buoyant-plume
  scalings are for steady jets in a uniform stream, not a few-hundred-µm jet starting inside the bed's boundary layer;
  the one measurement found (Bitharas et al., SS316) is ~10× lower. This note's own scenarios use Raoult's law with
  activity = mole fraction and an assumed keyhole mouth (0.7 × the spot).
- **The deposit's optics** bracket rather than predict: a continuous film overstates absorption, Maxwell Garnett spheres
  understate it for chain-like agglomerates, and neither includes the haze a thick porous deposit scatters.
- **Not run:** a transient puff (§5 is a scaling argument), the fine mesh, the upper slot at z 110–114 (gas-flow.md §0.1),
  purge flows other than 1 and 3 L/min, and the LP port at another position as a real recess (§1.2 used the gas next to
  the ceiling there instead).

## 8. Re-running

Cases go to `/tmp/plume`; they are not committed. On a shared 4-core runner each coarse case took 10–25 min.

```bash
D=desktop-lpbf; M=$D/analysis/monitoring/plume; PY=/tmp/venv/bin/python
$M/run_cases.sh                                    # p200, p200_lw3, p140, p200_lw1: make_case_plume.py + run_case.sh each
for c in p200 p200_lw3 p140 p200_lw1; do /tmp/capmem 4 $PY $M/particles.py /tmp/plume/$c; done   # ~5-15 min each
/tmp/capmem 2 $PY $M/spatter.py                    # ~1-2 min
/tmp/capmem 2 $PY $M/plume_jet.py                  # seconds; reads analysis/out/monitoring/melt/plume_source.json (--source)
$PY $M/fouling.py && $PY $M/summarize.py           # fouling.json (same --source), summary.md
```

Here `plume_jet.py` and `fouling.py` read worker A's file from its own worktree with `--source` (the file wasn't on this
branch yet); on the merged branch the default path is the same file.

`run_cases.sh` ran p140 and p200_lw1 for 300 and 200 iterations here (from p200's and p200_lw3's fields) to fit the
time; its defaults are 500 and 300. `particles.py` merges each case into its JSON when it writes it, so two cases can run
side by side; with 30,000 tracers per band and 20 s each case took ~10–15 min under load.

## Sources

Read for this note:
- Nagato, K., Ozawa, T., Neuenfeldt, M., Zanger, F., Zhao, M., Schulze, V. (2023). Enhancing the prediction quality of
  mechanical properties for powder bed fusion with laser beam by dynamic observation of flying particles. Mater. Des.
  227:111696. https://doi.org/10.1016/j.matdes.2023.111696 (open access; Table 1–3, Figs. 4 and 8: AlSi10Mg on an SLM280HL,
  83 µm spot, 200 °C plate, spatter counts, pulsed 640 nm illumination, plume light above 100 µs)
- Rakić, A. D. (1995). Algorithm for the determination of intrinsic optical constants of metal films: application to
  aluminum. Appl. Opt. 34:4755–4767. https://doi.org/10.1364/AO.34.004755 (n, k from refractiveindex.info's CC0 copy)
- Hagemann, H.-J., Gudat, W., Kunz, C. (1975). Optical constants from the far infrared to the x-ray region: Mg, Al, Cu,
  Ag, Au, Bi, C, and Al₂O₃. J. Opt. Soc. Am. 65:742–744. https://doi.org/10.1364/JOSA.65.000742 (Mg n, k via
  refractiveindex.info)
- Boidin, R. et al. (2016). Pulsed laser deposited alumina thin films. Ceram. Int. 42:1177–1182.
  https://doi.org/10.1016/j.ceramint.2015.09.048 (amorphous alumina n ≈ 1.67 at 0.8 µm, via refractiveindex.info)
- Li, Z. et al. (2022). A review of spatter in laser powder bed fusion additive manufacturing. Micromachines 13:1366.
  https://doi.org/10.3390/mi13081366 (its summary of Ly et al. 2017's mechanisms and speeds)
- Bitharas, I., Parab, N., Zhao, C., Sun, T., Rollett, A. D., Moore, A. J. (2022). The interplay between vapour, liquid, and
  solid phases in laser powder bed fusion. Nat. Commun. https://doi.org/10.1038/s41467-022-30667-z (full text via Europe PMC,
  PMC9135709: SS316, 0.75 m/s; "with the cross-flow [u_max ~2.1 m/s] the plume is dissipated ... after propagating upwards
  for ~1 mm"; vapour jet "of the order of hundreds of m/s")

From this run's other work:
- Worker A's melt-pool and evaporation model: `analysis/out/monitoring/melt/plume_source.json` (keys documented in its
  `keys` block; the `best` and `wall` readings are used here, §3). Its 7075 loss fractions are from Velikajne et al.
  (2026), Materials 19:970, https://doi.org/10.3390/ma19050970 (DOI checked to resolve; not read here).

Via Edison (r8-melt-plume, r8-viewports; not re-read here):
- Ly, S., Rubenchik, A. M., Khairallah, S. A., Guss, G., Matthews, M. J. (2017). Metal vapor micro-jet controls material
  redistribution in laser powder bed fusion additive manufacturing. Sci. Rep. 7:4085. https://doi.org/10.1038/s41598-017-04237-z
- Guo, D. et al. (2024). Correlative spatter and vapour depression dynamics during laser powder bed fusion of an Al-Fe-Zr
  alloy. Int. J. Extreme Manuf. 6:055601. https://doi.org/10.1088/2631-7990/ad4e1d
- Chebil, G. et al. (2021). Study of spatter ejections during laser-powder bed fusion process for aluminum alloys. J. Laser
  Appl. 33:042047. https://doi.org/10.2351/7.0000493
- Mayi, Y. et al. (2020). Laser-induced plume investigated by finite element modelling and scaling of particle entrainment in
  laser powder bed fusion. J. Phys. D 53:075306. https://doi.org/10.1088/1361-6463/ab5900
- Shi, G. et al. (2024). A review of the vaporization behavior of some metal elements in the LPBF process. Micromachines
  15:846. https://doi.org/10.3390/mi15070846
- Noskov, A. et al. (2020). Characterization of ultrafine particles emitted during laser-based additive manufacturing of
  metal parts. Sci. Rep. https://doi.org/10.1038/s41598-020-78073-z; Noskov, A. et al. (2022). A microscopy study of
  nanoparticles emitted during laser additive manufacturing with stainless steel powder. Mater. Lett. X 14:100139.
  https://doi.org/10.1016/j.mlblux.2022.100139
- Li, Y.-J. (2024). Additive manufacturing of 6061 and 7075 aluminium alloy with selective laser melting (thesis; the Mg and
  Zn loss compilation). https://doi.org/10.70675/5f083431z1407z40f1z83bfz19a675dc42f6
- Barrett, C. (2019). High speed stereovision in situ monitoring of spatter during laser powder bed fusion (thesis);
  Ahmad, A. (2019). Large scale selective laser melting: study of the effects and removal of spatter by the inert gas flow
  (thesis). https://doi.org/10.32657/10220/47940
- Williams, R. (2022). Maximising the utilisation of Ti-6Al-4V metal powder in the selective laser melting process
  (thesis). https://doi.org/10.17638/03157594

Models and methods:
- Knight, C. J. (1979). Theoretical modeling of rapid surface vaporization with back pressure. AIAA J. 17:519–523.
  https://doi.org/10.2514/3.61164
- Hasselbrink, E. F., Mungal, M. G. (2001). Transverse jets and jet flames. Part 1. Scaling laws for strong transverse jets.
  J. Fluid Mech. 443:1–25. https://doi.org/10.1017/S0022112001005146
- Briggs, G. A. (1975). Plume rise predictions. In Lectures on Air Pollution and Environmental Impact Analyses, AMS, 59–111
  (bent-over buoyant plume, Δz = 1.6 F^(1/3) x^(2/3) / U)
- Friedlander, S. K. (2000). Smoke, Dust, and Haze, 2nd ed. Oxford University Press (free-molecular coagulation, ch. 7–8)
- Lai, A. C. K., Nazaroff, W. W. (2000). Modeling indoor particle deposition from turbulent flow onto smooth surfaces.
  J. Aerosol Sci. 31:463–476. https://doi.org/10.1016/S0021-8502(99)00536-4
- Macleod, H. A. (2010). Thin-Film Optical Filters, 4th ed. CRC Press (characteristic-matrix method, ch. 2)
- Pasandideh-Fard, M., Qiao, Y. M., Chandra, S., Mostaghimi, J. (1996). Capillary effects during droplet impact on a solid
  surface. Phys. Fluids 8:650–659. https://doi.org/10.1063/1.868850
- Malitson, I. H. (1965). Interspecimen comparison of the refractive index of fused silica. J. Opt. Soc. Am. 55:1205–1209.
  https://doi.org/10.1364/JOSA.55.001205
- CRC Handbook of Chemistry and Physics (boiling points and enthalpies of vaporisation of Al, Mg, Zn, Si, Cu)
- OpenFOAM v2406 (`opencfd/openfoam-run:2406`), as in gas-flow.md; miepython 3.3.1 for the Mie efficiencies
