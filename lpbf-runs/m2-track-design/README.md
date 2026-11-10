# Track length, spacing and sampling for the M2 single-track runs

Issue [#100](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/100), PR
[#243](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243). This folder backs the track design in
[§4 of the plan](../m2-single-track-schedule.md#4-pilot-run-carl-and-josh): how long each track is, how far apart,
in what order, where it is sectioned, and how the power–speed settings are chosen (Sobol blocks and batch BO, not a
grid). It has two sources:

- **Eagar–Tsai runs for 316L** ([`eagar_tsai_316l.py`](eagar_tsai_316l.py)), which test the physical assumptions
  behind the design. These use [ArroyaveLab `eagar-tsai`](https://github.com/ArroyaveLab/eagar-tsai) 0.6.0, the
  package PR #238 checked, plus the same integral evaluated over the finite time the laser is on.
- **Four Edison literature reports** ([`edison-trajectories/m2-single-track-design/`](../../edison-trajectories/m2-single-track-design/),
  prompts in [`scripts/edison_m2_track_design.py`](../../scripts/edison_m2_track_design.py)) on start and end
  transients, interactions between neighbouring tracks, sampling, and 316L inputs.

## Recommendations

| Choice | Recommendation | Main reason |
| --- | --- | --- |
| Track length | **12 mm** (10 mm at the least) | Modelled start and end zones are short (below), but keyhole start-up, the galvo, the laser's on/off timing and the end crater are not modelled, and they scale with speed. 12 mm leaves 3 mm to discard at each end and 6 mm of steady track around the target plane: ±1 mm of slack in finding the plane and room for a second plane 1.5 mm further on. It still fits four rows on one panel at 15 mm row pitch (option B) |
| Discard at each end | **3 mm** | 8× the longest conduction start zone Eagar–Tsai gives (0.37 mm) and 18× its end zone (0.17 mm). At 2 m/s, 3 mm is 1.5 ms: enough for a 1 ms keyhole start-up or galvo ramp. Common practice is 10–15 mm tracks sectioned in their middle third |
| Section plane | **Mid-length** (6 mm), found from the track ends visible on the top view; on panel A in the pilot, a **second plane 1.5 mm further on** | One plane per track is enough if the along-track scatter is small; the second plane on panel A measures it. The top views (C1) give width along the whole steady zone of every track for free |
| Spacing | **2 mm centre to centre** (pilot); 1.5 mm in the campaign if the pilot's top views show narrow denuded bands | Heat from a neighbour is negligible at 1 mm or more; denuded powder and spatter set the spacing. 2 mm is more than 6× the widest pool Eagar–Tsai gives in the window (0.26 mm). 1.5 mm would put 12 tracks in a 1.25" mount instead of 9 |
| Scan direction | **The same on every track**, into or across the gas flow, never with it | With the flow, the plume and spatter are blown ahead of the beam onto the track still to be drawn |
| Exposure order | **Strictly from the gas outlet side toward the inlet**, with parameter sets in randomized positions; no interleaving | Spatter blown downstream lands on finished tracks. Interleaving (odd positions, then even) is sometimes suggested for heat, but heat doesn't matter here and interleaving would put upstream spatter on positions not yet drawn |
| Galvo | **Ask whether skywriting is on**; check the first 3 mm of a few tracks in the pilot (top view, or a longitudinal section of a spare track) | Without it, Eagar–Tsai puts the first 0.3 mm up to 1.9× deeper at 2 m/s for a 0.3 ms ramp |
| Settings | **64 scrambled-Sobol points in four 16-point blocks, one block per panel**, plus 2 controls per panel; **batch BO** in the campaign, one M2 run per batch, with one more Sobol block per run held out for validation | See [Sampling](#sampling-sobol-blocks-then-batch-bo) |

## What Eagar–Tsai says (and doesn't)

All runs use 316L with constant properties (nominal k 26 W/m/K, ρ 7300 kg/m³, c 710 J/kg/K, so
α = 5.0 × 10⁻⁶ m²/s; liquidus 1723 K), absorptivity 0.4 and a 54 µm 1/e² spot (LLNL's 400 W M2), unless noted.
The Edison 316L report suggests k 21.5, ρ 7500, c 640 (α 4.5 × 10⁻⁶) and a liquidus of 1697 K, but its literature
search returned nothing, so those are unsourced. The two alternative property sets below bracket α from 3.5 to
7.0 × 10⁻⁶ m²/s instead. Eagar–Tsai is conduction only: no Marangoni flow, keyhole, evaporation or powder. Its
peak temperatures are 10,000–70,000 K over this window, far above boiling, so it cannot say where keyholing starts,
as PR #238 also found for AlSi10Mg. What it can test is how long the heat flow takes to settle and how far heat
spreads, and that is what it is used for here.

**Steady state over the window** ([`out/steady_state_grid.csv`](out/steady_state_grid.csv), 1 µm grid): inside the
plan's window (100–375 W, 250–2000 mm/s) the pool is 60–256 µm wide, 21–127 µm deep and 0.18–0.65 mm long. The
length depends almost only on power.

**Start and end of a track** ([`out/finite_track_summary.csv`](out/finite_track_summary.csv)). The same Eagar–Tsai
integral, but with the laser on only from t = 0 to the end of the track, gives the fused depth and width at every
transverse section, from each point's maximum temperature over all time. At mid-length it reproduces the package's
steady state (200 W, 1 m/s: W 102.8 vs. 102.0 µm, D 47.5 vs. 47.0 µm; the package is on a 1 µm grid).

![Start and end transients](out/m2-track-transients.png)

| | 9 settings, 100–375 W, 0.25–2 m/s | Same, α from 3.5 to 7.0 × 10⁻⁶ m²/s or a 90 µm spot |
| --- | --- | --- |
| Depth at the very start | 58–66% of steady state | 46–66% |
| Distance to within 5% / 1% of steady-state depth | ≤ 0.20 / ≤ 0.32 mm | ≤ 0.22 / ≤ 0.37 mm |
| Same, as a multiple of the steady-state depth | 2.3–3.7 D | |
| Distance from the end where depth is still within 1% | ≤ 0.12 mm | ≤ 0.17 mm |
| With a 0.3 ms galvo speed ramp at each end, laser on | first 0.2–0.3 mm up to 1.3× (1 m/s) and 1.9× (2 m/s) deeper than steady state; settled within 1% by 0.34 mm | |

So conduction alone settles within about a third of a millimetre, roughly three pool depths. Anything longer seen
in a real track comes from physics Eagar–Tsai leaves out (next section), and that is why the discard zone is set by
the literature rather than by this model.

**Heat reaching a neighbour** ([`out/neighbour_heating.csv`](out/neighbour_heating.csv)): the surface temperature
rise beside the middle of a finished 10 mm track.

| Setting | at 0.5 mm | at 1 mm | at 2 mm | at 3 mm |
| --- | --- | --- | --- | --- |
| 375 W, 0.25 m/s (1.5 J/mm, the hottest corner) | 108 K | 27 K | 6.8 K (peaks 0.2 s after the beam passes) | 3.0 K |
| 200 W, 1 m/s | 14 K | 3.6 K | 0.9 K | 0.4 K |
| 100 W, 2 m/s | 3.6 K | 0.9 K | 0.2 K | 0.1 K |

In Eagar–Tsai a preheat of ΔT is the same as lowering the liquidus by ΔT, which deepens the pool by 0.3–0.4% per
10 K ([`out/preheat_sensitivity.csv`](out/preheat_sensitivity.csv)). So a neighbour 2 mm away changes the depth by
under 0.3% even at the hottest setting, and 1 mm would still be under about 1%. Heat does not set the spacing.

## What the literature adds (Edison), and how far to trust it

**All four first-round reports are ungrounded.** They ran during an outage of Edison's literature search, and each
says it retrieved no papers ("no contexts were retrieved, so this answer is not grounded in evidence") and that its
DOIs and numbers come from the model's own knowledge. They don't even agree with each other: the four reports give
four different DOIs for Yadroitsev et al. 2010. So the numbers below are a second opinion to test against, not
sources. The transients and spacing queries were resubmitted
(`_task_ids_retry.json`); see the end of this section for whether the retries were grounded.

| Report | What it says | How it changes the design |
| --- | --- | --- |
| [Transients and length](../../edison-trajectories/m2-single-track-design/track-transients-and-length.md) | Conduction pools settle within 1–3 pool lengths. A keyhole forms in 50–200 µs, but its depth takes 0.3–1 ms to settle. Galvo acceleration takes 0.1–1 ms, and uncompensated mark/laser delays are 50–500 µs, so at 1–3 m/s the ends can carry the wrong energy per length over 0.1–3 mm unless skywriting is on. Keyholes collapse within 50–200 µs of laser-off and leave end-of-vector pores (Martin et al. 2019); the end crater spans 0.5–1 pool length. Practice: 5–20 mm tracks, 10 mm most common, sectioned "in the middle"; discard distances are rarely stated. Width and depth vary 5–15% along stable tracks and 20–30% near instability. It recommends 10–15 mm, ≥3 mm discard (5 mm for keyholes at high speed) and 3 sections per calibration track | Its conduction figure agrees with Eagar–Tsai (about 2–4 pool depths, 0.1–0.4 mm). Its keyhole and galvo times are why the discard went from 2 to 3 mm and the length from 10 to 12 mm. Three sections per track would triple polishing and SEM, so the pilot measures the section-to-section scatter on panel A first |
| [Spacing and order](../../edison-trajectories/m2-single-track-design/track-spacing-and-order.md) | At 1 atm the vapour jet entrains gas and pulls powder into the track (Matthews et al. 2016). The denuded band is 2–5× the track width in total, 0.1–0.4 mm beyond each edge for 0.1–0.2 mm tracks, and 0.5–1 mm in total for keyholes. Spatter lands mostly 2–5 mm away, and some goes more than 10 mm downstream. Expose from outlet to inlet and scan into or across the flow. Spacing ≥1.5 mm, 2–2.5 mm for keyhole settings, and ≥3× the pool width. Heat is negligible beyond 1.5–2 mm. A spread layer is 50–65% dense | Supports 2 mm. Its heat estimate matches Eagar–Tsai's (≤7 K at 2 mm). It also suggests interleaving the exposure for heat, which this design doesn't do: Eagar–Tsai shows heat doesn't matter, and interleaving would break the outlet-to-inlet order |
| [Sampling](../../edison-trajectories/m2-single-track-design/sampling-sobol-vs-batch-bo.md) | Start with 64 Owen-scrambled Sobol points in (P, log v), a power of two for balance. Then run batch active learning with one build per batch, using a heteroscedastic multi-output GP plus a regime classifier. The acquisition mixes integrated-variance reduction (about 50%), boundary entropy (30%) and model-discrepancy checks (20%). Hold out 20–25% of settings for validation, split by setting, not by section. Repeat a few settings across builds and panels. It rates the evidence for 64-point Sobol over a maximin LHS as weak, and for space-filling plus batch BO as moderate to strong | Matches the design below. Its point about cross-build repeats is why the controls stay the same set in every run |
| [316L inputs](../../edison-trajectories/m2-single-track-design/ss316l-eagar-tsai-inputs-and-single-track-data.md) | Liquidus 1697 K, k 21.5 W/m/K, ρ 7500 kg/m³, c 640 J/kg/K (α 4.5 × 10⁻⁶ m²/s), boiling 3090–3134 K. Absorptivity 0.35 in conduction and 0.6–0.8 in keyhole mode. Its single-track data points are marked as approximate digitizations | α lies inside the 3.5–7.0 × 10⁻⁶ bracket used above, so the transient and heat conclusions stand. Its data points are too uncertain to calibrate Eagar–Tsai against; use the original papers or MeltpoolNet for that |

## Sampling: Sobol blocks, then batch BO

![Sobol blocks vs. the grid](out/m2-sobol-vs-grid.png)

**Pilot.** [`design.py`](design.py) draws 64 points of a scrambled 2-D Sobol sequence over P 100–375 W and
log v 250–2000 mm/s (the old grid's box, so P/v still spans 0.05–1.5 J/mm), seed 100, rounded to 1 W and 5 mm/s
([`out/pilot_sobol_sets.csv`](out/pilot_sobol_sets.csv)).

- **Each panel gets one block of 16 consecutive points** (0–15 on A, 16–31 on B, ...). Every such block of a base-2
  Sobol sequence is itself a balanced, space-filling set over the whole box. So **panel A, which is sectioned
  first, covers the whole window on its own**, and A–D together are a 64-point design. The centred discrepancy of
  each 16-point block is 0.0021, against 0.034 for the 4 × 4 grid (lower is more even).
- **64 distinct powers and speeds instead of 4 of each** (62 and 63 after rounding). A Gaussian process learns
  far more from 64 distinct points than from 4 replicates of 16, and the grid's repeated levels leave the space
  between them empty.
- **Replicates move into the controls.** The 2 controls per panel (8 per run) at the machine's standard 316L set
  estimate track-to-track noise and any panel or position effect. Keyhole depth is noisier than conduction depth,
  so consider making one of each panel's two controls a fixed keyhole setting instead.
- **The box is still a guess.** Xavier should check it against the AM Module's printability map before the pilot
  and change `P_RANGE` / `V_RANGE` in `design.py` if most of it is deep keyhole. On a 200 W M2, lower `P_RANGE`.

**Campaign: batch BO, one M2 run per batch.** With about one run a week and 3–6 campaign runs, there are only 3–6
rounds, each of up to 64 new tracks: a large-batch, few-round setting.

- **Each run:** 48 tracks chosen by batch BO, **16 from the next Sobol block** (points 64–79 for run 1, 80–95 for
  run 2, and so on), and the 8 controls. The Sobol block in each run is an unbiased, space-filling hold-out set
  for validating the AM Module, which BO-chosen points are not, since BO crowds them where the model is unsure.
- **What BO optimizes:** the goal is to calibrate and validate the AM Module, not to find one best track. So the
  surrogate is a GP on the AM Module's error (measured minus predicted depth and width, in log), and the
  acquisition reduces its integrated posterior variance (`qNegIntegratedPosteriorVariance` in BoTorch), weighted
  toward the regime boundaries (keyhole onset, depth equal to the layer, balling) where the printability map is
  decided. If the TMS story needs a process optimum too, add a constrained objective (for example a target depth
  per layer with depth/width < 0.5 and a continuous track) as a second batch criterion.
- **When Sobol alone is enough:** if the campaign shrinks to 1–2 runs, BO has too few rounds to pay off. Just
  continue the Sobol sequence; the next 64 points fill in the gaps of the first 64.
- **Ax:** add the pilot's 64 points as manual trials, then generate each batch with a BoTorch step
  (`client.get_next_trials(max_trials=48)`), as in the lab's Honegumi templates.

## Files

| File | What it is |
| --- | --- |
| [`eagar_tsai_316l.py`](eagar_tsai_316l.py) | All the Eagar–Tsai runs (about 10 min on 4 cores): `python eagar_tsai_316l.py [grid] [finite] [neighbour]` |
| [`design.py`](design.py) | The pilot's Sobol blocks; `python design.py` |
| [`figures.py`](figures.py) | The two figures above; `python figures.py` |
| `out/` | CSVs, the along-track profiles (`finite_track_profiles.json`) and the figures |

Environment: Python 3.12 with numpy 2.5, scipy 1.18, matplotlib 3.11 and `eagar-tsai` 0.6.0 installed from its
repository (`pip install -e .`).
