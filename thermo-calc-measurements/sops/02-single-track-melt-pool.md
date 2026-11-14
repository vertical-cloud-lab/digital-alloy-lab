# SOP 02 (draft): single-track cross-sections and heat-source calibration

**Checks:** melt-pool width, depth and depth/width ratio, the conduction/transition/keyhole regime, and
track continuity (balling). These calibrate the Thermo-Calc AM Module's heat source
(absorptivity and beam radius) and the open models compared in #238 and #249. **Analysis:**
[`../analysis/melt_pool_calibration.py`](../analysis/melt_pool_calibration.py). Keyhole criteria:
[#249's `keyhole_open_models.py`](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/249).
Draft. The plate layout, cutting and mounting follow the stainless-steel M2 plan in
[PR #243](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243) (`lpbf-runs/m2-single-track-schedule.md`).
Only the Al/Cu-specific steps are given here.

## Samples
- **Tracks:** 12 mm long at 2 mm spacing, all scanned in one direction across or into the gas flow,
  exposed from the outlet side toward the inlet (#243).
- **Power–speed sets:** scrambled-Sobol blocks rather than a grid (#243), plus repeated control
  sets on every plate.
- **Substrate:** a plate of the same alloy family (6061/6063 for Al; a Cu alloy for Cu), or a
  printed pad of the alloy itself where its composition matters.
- **Two kinds of track per alloy:**
  - **Bare-plate tracks** calibrate the absorptivity of dense metal;
  - **one-powder-layer tracks** (30–50 µm) reproduce LPBF.
- **Powder needed:** enough to spread one layer over the track area, a few grams on a small plate.
  This fits the ~100–300 g we atomize per alloy.

## Preparation (Al and Cu specifics)
1. **Image first:** top views of every track at 50–100×, for continuity, balling and denudation width.
2. **Section** at mid-length, and hot-mount in conductive compound (#243 §3).
3. **Grind and polish:**
   - SiC 320 → 800 → 1200, then 3 µm and 1 µm diamond;
   - for Al, finish with 0.05 µm colloidal silica.
4. **Etch:**
   - **Al:** Keller's reagent, 10–20 s. It contains **HF**: use a fume hood, HF-rated gloves, and keep calcium gluconate gel at hand.
   - **Cu alloys:** ammonium persulfate or ferric chloride.
   - Etch right after polishing.
5. **Image** each track at a fixed magnification (optical 200× or SEM-BSE). Measure in Fiji:
   - width W at the original surface;
   - depth D below it and height H above it;
   - fused area.
   - On one plate, grind 1.5 mm further and section again to get the along-track scatter (#243).

Expect about 18 tracks per mount, 3–4 h of preparation per batch of mounts, and about 2 h to measure
72 tracks by hand. These are the M2 plan's estimates; time our own.

## Analysis
```bash
python ../analysis/melt_pool_calibration.py tracks.csv --material alloy.json \
    --fit-on conduction --am-module am_module_predictions.csv --out out/P1
```
- **Inputs from our own measurements:**
  - `T_liquidus_K` from SOP 01;
  - `k_W_mK` from SOP 04 (eddy current with a Smith–Palmer fit) or from laser flash;
  - `rho` from SOP 03;
  - `cp` from DSC;
  - `r0_um`, the beam's 1/e² radius, from the machine's beam profile.
- **Fit on conduction-mode tracks only (D/W < 0.5):** the model has no keyhole. Then report:
  - the fitted absorptivity;
  - the width-only absorptivity for each track, which shows how it rises with P/v;
  - Ke for each track;
  - the AM Module's bias and RMSE against the measured tracks.
- **Keyhole tracks:** fit a single Ke threshold for keyhole onset (#249).

## Acceptance
- At least 3 conduction-mode tracks and at least 3 keyhole tracks per alloy and per substrate condition.
- Control sets repeat within ±5 % in width.
- The fitted absorptivity is stable to within ±0.03 when any one track is left out.

## Open questions
- Is the desktop machine (#260) running, or do the first tracks come from the Utah MIDI (P1, Dec 2–3)?
- Ask Thermo-Calc's account manager for the AM Module grid export as CSV. #238 and #249 asked for it first.
