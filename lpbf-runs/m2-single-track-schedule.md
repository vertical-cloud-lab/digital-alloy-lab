# Single-track runs on BYU's Concept Laser M2 (stainless steel): pilot and schedule

Issue [#100](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/100). This is the fallback path from
the [2026-08-13 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/100#issuecomment-6201170907):
if the atomizer-to-printer loop isn't ready, print commercial stainless steel on BYU's M2 and use cross-section SEM
of single tracks to check the Thermo-Calc AM Module.

**Plan in brief**

1. **One pilot run first.** Carl and Josh print 72 single tracks on the plate's four removable panels: 64
   power-speed settings from a scrambled Sobol sequence, one 16-point block per panel that covers the whole window,
   plus two control tracks per panel. Tracks are 10 mm long at 2 mm pitch and sectioned at mid-length. Carl times
   every step from job prep to SEM. The campaign then picks each run's settings by batch Bayesian optimization
   ([`m2-track-design/`](m2-track-design/README.md) has the reasoning, the Eagar–Tsai checks and the Edison reports).
2. **Running many parameter sets in one build looks feasible on the M2** and seems to be the intended workflow:
   the Concept Laser build processor assigns parameters per part. What still needs checking on BYU's install is how
   to make each track come out as exactly one scan vector. A dry run in the software settles it (see
   [§2](#2-can-the-m2-run-many-parameter-sets-in-one-build)).
3. **Nathan C.'s four-insert plate removes the two worst steps.** The big plate is never lasered, so it never
   needs resurfacing. Nothing needs wire EDM: the inserts are panels about 88 mm (3.5 in) square, and a bandsaw
   takes out the strip of each panel that holds the tracks' section planes and cuts it into mount-sized pieces
   ([§3](#3-substrate-plate-refresh-and-sectioning)). A panel that carries tracks is used up, so if the pilot shows
   that position on the plate doesn't matter, the campaign should put a whole run on one or two panels.
4. **The campaign size comes from the pilot's timing log.** My current estimate is about 3 to 4 person-days per
   run, which allows about one run a week. That fits 3 to 6 campaign runs (about 150 to 400 tracks) between
   mid-January and mid-February, ahead of TMS 2027 (March 14–18, Orlando). [§7](#7-sizing-the-campaign-from-the-pilot) shows
   how to redo that from measured times.

All durations below are **my estimates**, not measurements. Replace them with the pilot's numbers.

**Visuals** ([`m2-viz/`](m2-viz/README.md)): the [pilot design](m2-viz/out/m2-pilot-design.png) (P–v grid and track
map), the [run sheet and schedule](m2-viz/out/m2-schedule.png), and a 3-D animation of the whole process in six
parts, drawn with Nathan C.'s plate: [set up](m2-viz/out/m2_1_setup.gif), [print](m2-viz/out/m2_2_print.gif),
[unload](m2-viz/out/m2_3_unload.gif), [cut](m2-viz/out/m2_4_cut.gif), [mount, polish, SEM](m2-viz/out/m2_5_sem.gif),
and [measure and compare](m2-viz/out/m2_6_results.gif); one video of all six with chapters is
[`m2_full.mp4`](m2-viz/out/mp4/m2_full.mp4).

---

## 1. What we want out of it

For each track, a cross-section at mid-length that gives:

- melt-pool **width**, **depth** below the substrate surface, **height** above it, and fused **area**;
- the **regime**: conduction, transition, keyhole (deep and narrow, often with pores at the root), lack of fusion
  or discontinuous, or balling;
- for a few keyhole tracks, optional **EDS** checks for Mn/Cr loss to evaporation.

For each run, the AM Module predicts width, depth and regime for the same parameters. It can do steady-state
melt-pool calculations, batch and grid sweeps with parity plots against experiment, and printability maps for
keyholing, lack of fusion and balling ([`thermocalc_am_module.md`](../edison-trajectories/thermocalc_am_module.md)).
Published uses of the module calibrate the heat source (absorptivity, beam size) against measured melt pools
before predicting. So the plan is to **calibrate on part of the tracks and validate on the held-out rest**, and to commit
the predictions *before* the cross-sections are measured.

## 2. Can the M2 run many parameter sets in one build?

**Probably yes, and it is the normal workflow, but confirm it on BYU's install with a dry run.**

- Concept Laser jobs are prepared in Materialise Magics with the Concept Laser (now Colibrium Additive) build
  processor. The build processor "automatically transfers the build strategy for each part" to the WRX machine
  software and has "customizable slice parameters per part." The M2 is on its compatibility list
  ([Materialise](https://materialise.com/en/industrial/software/build-processor/concept-laser)). So a job with 72
  tracks, each its own part carrying one of 65 parameter sets (64 Sobol settings plus the control), is what the
  software is built for, not a hack. With Sobol settings almost every track has its own set, so it matters how sets
  are entered: if they can be imported from a file or copied and edited quickly, 65 is fine; if each takes a few
  minutes in the GUI, budget that in A1.
- Concept Laser sold the machine software in tiers. The lighter **CL WRX Control** tier exposes **laser power, scan speed, hatch
  ("trace") spacing, spot size, and contour offset**, which is everything a single-track sweep needs. Editing every
  parameter needs a separate, time-limited **CL WRX Parameter** licence and Concept Laser training. Sources are
  2016 press items ([Metal AM](https://www.metal-am.com/?p=61603),
  [New Equipment Digest](https://newequipment.com/home/product/55101922/68671-software-tool-permits-open-processing-of-all-parameter-settings),
  [Design World](https://www.designworldonline.com/control-additive-builds-concept-laser-parameter-editor/)), so
  check what BYU's licence actually allows.
- People have done this kind of study on this machine model. LLNL's 316L study ran on an M2 (400 W, 54 µm D4σ spot)
  and combined single-track experiments with density pillars ([Kamath et al., OSTI 1116929](https://www.osti.gov/biblio/1116929)).
  ORNL laid out a framework for characterizing more than 700 316L/316H coupons printed on an M2 and a Renishaw AM400
  ([ORNL report](https://info.ornl.gov/sites/publications/Files/Pub199801.pdf)). I did **not** find a published M2
  protocol that says how each single track was set up in the software, which is why the next list is something to try,
  not settled practice.

**How to get one scan vector per track (try these in order during the dry run):**

1. Make each track a thin part, for example 10 mm × 0.05 mm × one layer, whose slice yields a single vector. Expose
   it with a parameter set that has only one exposure type enabled (contour or fill).
2. If the software drops thin parts or gives two vectors, use Magics **line supports**, which are exposed as single
   lines. The build processor can assign parameters per support as well as per part.
3. Either way, check in the slice/vector preview that every track is **one vector of the right length**, and export
   the part-to-parameter-set list. That list is the track map.

**Questions for Josh (also in [§8](#8-kickoff-checklist-josh-and-nathan-c-if-possible)):**

- Is the build processor licensed on a BYU PC, and which WRX version is the machine on?
- Can we copy a parameter set and change power and speed at our licence tier?
- Is there a limit on parameter sets per job, and can sets be imported from a file? With Sobol settings a run
  needs about 65. If there is a limit, split the run into several short jobs, run back to back without breaking
  the inert atmosphere.
- Is skywriting (or an equivalent mark/laser-on delay tuning) on? Without it the beam speeds up and slows down
  with the laser on, and Eagar–Tsai puts the first 0.3 mm of a 2 m/s track up to 1.9× deeper.
- Can a job expose a layer without recoating? That would allow bare-substrate tracks (see §4).
- When was laser power last calibrated? The repo notes the M2 had been down for about two years with "a history of
  frequent problems" ([`alloy-workflow-review.md`](../alloy-workflow-review.md)).
- What spot size, laser rating (200 W or 400 W) and gas does it run? Published M2 configurations range from
  200 W with a 90 µm spot ([Empa](https://www.empa.ch/web/coating-competence-center/concept-laser-m2)) to 400 W with
  a 54 µm spot (LLNL).

**Measure power at the plane before the pilot if at all possible.** For the model comparison, the delivered power
and spot size are the two nuisance parameters that matter most. If they're off, absorptivity calibration silently
soaks up the error.

## 3. Substrate, plate refresh, and sectioning

### Four inserts in one plate (Nathan C.'s approach)

Nathan C.'s plate ([photo](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243#issuecomment-6759290262))
is about 10 in (254 mm) square and marked 316. It has four square pockets in a 2 × 2 grid, and each pocket holds a
removable **panel about 88 mm (3.5 in) square**, held down by four screws near its corners. The pockets are about
90 mm across, about 10 mm apart, and about 30 mm in from the plate's edges. These sizes are scaled from the photo
against Nathan C.'s 10 in, and the photo doesn't show how thick the panels are, so measure both at the kickoff.
An earlier version of this plan assumed four 25 mm cubes. A panel has about 12 times that area, which changes the
layout, the refresh options and the cutting below.

The tracks go on the panels. After a run we unscrew the panels that carry tracks and put in fresh ones.

- **What it removes:** the big plate is never lasered, so it needs no resurfacing between runs, only cleaning
  (blow powder out of the gaps around the panels and out of the screw holes). Nothing is welded to the plate, so
  wire EDM isn't needed.
- **A panel that carries tracks is used up,** because sectioning cuts a strip out of it. A panel with no tracks only
  gets powder on it and can stay in for the next run. Reusing a sectioned panel isn't practical: slicing a slab off
  the whole 88 mm top on a bandsaw is a long cut that wanders, and the thinner panel would then need shims to sit
  flush.
- **Panel material** should match the powder (316L panels for 316L powder). That keeps a different substrate from
  diluting the fused zone, and the substrate's thermal properties then match what the model assumes.
- **Flushness is the critical tolerance.** MIT's single-track work uses a rule of thumb of about 10 µm flatness and
  parallelism (10 to 20% of a layer), which grinding alone does not reliably hold. That is why ordinary builds
  sacrifice the first several layers to self-planarize
  ([Weissbach, Penny & Hart, arXiv:2409.14548](https://arxiv.org/abs/2409.14548)). A proud panel gets a thinner
  powder layer or catches the recoater, and a sunken one gets a thicker layer. **Before every run, dial-indicate
  each panel against the plate and record the offset** at its corners and at the row of tracks, since a panel this
  size can also rock or bow when its screws are tightened. The offset at the tracks becomes that panel's
  layer-thickness input to the model.
- **Use the same surface finish on every panel,** for example ground and then lightly bead-blasted, and record it.
  Absorptivity and powder spreading both depend on it.
- **Mark each panel** with an ID and an orientation mark on its edge. Mixing up the track-to-parameter map after
  sectioning is an easy way to lose a whole run.
- **Keep tracks away from the panel's edges and screws.** The gap around a panel and the screw holes catch powder
  and can disturb the layer next to them, so keep tracks at least 15 mm from the edges; the middle of the panel is
  free.
- **Ask Nathan C.** for the plate, its drawings (pocket depth, panel thickness, screw size) and any spare panels,
  and whether we may cut up his panels or should make our own. For old M2 job files and the machine's quirks, the
  repo notes that Dr. Nathan Crane's students were the last people to run the M2.

### Refreshing the panels (pick one with Josh before the shop work)

Each new panel is cut from 316L plate, machined to fit its pocket, drilled and counterbored for its four screws, and
ground so it sits flush. That is my guess of 1 to 2 hours of shop time per panel, less in batches. So the real
choice is how many panels a run uses up.

| Option | How | Panels used | Notes |
| --- | --- | --- | --- |
| **A. One Sobol block per panel** (the pilot) | Each of the four panels carries one row of 18 tracks (16 Sobol settings + 2 controls) | 4 per run, about 28 for the pilot and six campaign runs | Every run checks whether position on the plate matters, but this uses the most panels and shop time |
| **B. A whole run on one or two panels** (the campaign, if the pilot allows) | One panel holds all 72 tracks in four rows ([§4](#4-pilot-run-carl-and-josh)); the other panels stay in as blanks | 1–2 per run, about 10–16 including the pilot's four | A quarter to half the shop time of A. Plate position is then checked only in the pilot, so choose B only if the pilot shows no position effect |
| **C. No insert plate** (fallback) | Print on a normal plate and cut the region out, or put tracks on printed pedestals that can be cut off | Whole-plate resurfacing each run (mill or surface grinder) | Pedestals add hours of build time, and the plate gets thinner every time |

### Cutting without wire EDM

What we image is a cross-section through each track at its mid-length, polished on its side. Looking down on the
panel shows only the top of each track. So every track on a panel is laid out with its mid-length on one line, the
**target plane** ([§4](#4-pilot-run-carl-and-josh)). One narrow strip of the panel then holds every track's section,
and the cutting only has to get that strip out and into pieces that fit a mount.

1. **Unscrew the panel** and check its ID and orientation mark against the track map.
2. **Bandsaw** (bi-metal blade, with coolant for stainless; an abrasive cut-off saw works too if it takes an 88 mm
   wide panel). The panel lies flat, tracks up, against a fence. A bandsaw face is rough and deformed, so **no
   bandsaw cut comes within 3 mm of the target plane**.
   1. Cut across the panel, square to the tracks, 3 mm to one side of the target plane and about 7 mm to the other.
      That frees a **strip about 10 mm wide** that holds every track's section plane. The rest of the panel is scrap.
   2. If the panels are thicker than about 12 mm, cut the strip lengthwise about 10 mm below the tracks so the pieces
      fit the mount.
   3. Cut the strip into **pieces of nine tracks, about 22 mm long**, and trim off its blank ends.
3. **Fine wet saw.** On an abrasive cut-off saw or a low-speed precision saw with coolant (MIT used a Buehler IsoMet
   4000 at 4000 rpm and 6 mm/min), cut through each piece **0.5 mm from the target plane**, on the 3 mm side. A
   sliver 1.5–2 mm thick falls off. The new face is flatter and much less deformed than a bandsaw face, so grinding
   only has to remove the last 0.5 mm.
   - **This step is optional.** The alternative is to make the bandsaw cut 1.5–2 mm from the plane and grind all of
     that away. That saves a cut per piece, but grinding 1.5–2 mm of stainless on SiC paper is slow. On panel A,
     prepare one piece each way and time both. Keep the faster route, unless its etched section shows smeared or
     deformed metal at the tracks.
4. **Grind to the target plane**, the tracks' mid-length, on coarse SiC paper.
5. **Mount** in conductive hot-mount compound so the SEM doesn't charge. A piece about 22 mm × 10 mm in section fits
   a 1.25" puck.
6. **Grind, polish and etch.** MIT's sequence was 320 then 800 grit, 3 µm diamond, then 0.05 µm alumina. Etch right
   after polishing, because 316 passivates quickly: MIT used dilute aqua regia for 30–45 s, which needs a fume hood.
   Electrolytic 10% oxalic acid is the usual alternative.
7. **Check under the optical microscope** that the etch is good and the track order matches the map. **Then SEM**:
   secondary-electron images of every track at two fixed magnifications. Ronnie's
   [Caliber](https://github.com/vertical-cloud-lab/caliber) can supply SEM and EDS acquisition settings.
   - **What fits in BYU's Apreo C** ([spec page](https://microscopy.byu.edu/apreo-sem),
     [startup SOP](https://microscopy.byu.edu/apreo-sem-startup-sop)): up to 500 g in any stage position, or 2 kg
     flat (0° tilt); 122 mm across with full travel and rotation (larger with limited travel); 85 mm tall, holder
     included, to the 10 mm working distance. Every sample in one load must be within 1–2 mm of the same height, and
     the usual holder takes 12.7 mm pin stubs. So the mount and the polisher limit the piece size, not the SEM. A
     whole panel would fit flat (about 0.6–1.6 kg if 10–25 mm thick), but it couldn't be tilted and would show only
     the tops of the tracks.
   - **Load the pucks themselves,** with heights matched, on a holder for 1.25" mounts: one run's eight pucks fit in
     the 122 mm circle. Keep any load that will be tilted to 70° for EBSD under 500 g, holder included. Without a
     mount holder, break each polished piece out of its puck onto a 25 mm pin stub, as in the lab's
     [stub-mounting video](https://youtu.be/kcyESipwU8Y?t=776). The widest field of view is 3.0 mm at the 10 mm
     working distance, so each track gets its own frames.

## 4. Pilot run (Carl and Josh)

The goal is to get one run all the way from job file to measured cross-sections, with **every step timed**. The
pilot doubles as a machine health check.

**Layout (scaled from the photo; adjust once the panels are measured).** Each panel carries **one row of 18
parallel tracks across its middle**, **10 mm long at 2 mm pitch**, in two groups of nine with a 10 mm gap between the
groups. Every track's mid-length lies on one line, the target plane, so one strip of the panel holds all 18 sections
([§3](#cutting-without-wire-edm)) and each group of nine becomes one mount. The row is about 42 mm wide, well clear
of the panel's edges and screws. Four panels give **72 tracks per run**. A panel has room for four such rows 16 mm
apart, which is how option B puts a whole run on one panel.

Why these numbers (details, Eagar–Tsai runs and Edison reports in [`m2-track-design/`](m2-track-design/README.md)):

- **Length: discard the first and last 2 mm of every track.** In Eagar–Tsai for 316L, a conduction-mode pool is
  within 1% of its steady-state depth at most 0.37 mm after the start and up to 0.17 mm before the end, over
  100–375 W and 0.25–2 m/s. That model leaves out keyhole start-up, the galvo's speed ramp if skywriting is off
  (which it puts at up to 1.9× the steady depth over the first 0.3 mm at 2 m/s), the laser's on/off timing and
  the end crater, so the discard is set well beyond it. A 10 mm track then keeps 6 mm of steady track around the
  target plane: room for ±1 mm of error in finding the plane and for a second plane. 8 mm is the minimum for one
  plane.
- **Pitch: powder sets it, not heat.** Eagar–Tsai puts at most 7 K on a neighbour 2 mm away (375 W, 0.25 m/s),
  which changes its depth by under 0.3%. But each track strips powder from a band beside it (denudation) and
  throws spatter. 2 mm keeps neighbouring bands apart even for the widest tracks. If the pilot's top views (C1)
  show bands narrower than about 0.5 mm per side, the campaign can go to 1.5 mm and put 12 tracks in a mount
  instead of 9.
- **Section plane: mid-length,** found from the track ends visible on the top view. On panel A in the pilot,
  after imaging, grind about 1.5 mm further and image a second plane. The difference between the two planes is the
  along-track scatter, which the model comparison needs as its noise level.

**Parameters.** Use **64 power-speed settings from a scrambled Sobol sequence**, not a grid, plus **2 control
tracks per panel** at the machine's standard stainless parameter set. The window is the old grid's box for a 400 W
M2, **100–375 W and 250–2000 mm/s**, with speed on a log scale: P/v from 0.05 to 1.5 J/mm, from likely balling up
to deep keyholes. Xavier should check the window against the AM Module printability map first; on a 200 W machine,
lower the powers. [`m2-track-design/design.py`](m2-track-design/design.py) generates the settings
([list](m2-track-design/out/pilot_sobol_sets.csv), [figure](m2-track-design/out/m2-sobol-vs-grid.png)).

- **Each panel carries one 16-point block** of the sequence (points 0–15 on panel A, 16–31 on B, and so on) and 2
  controls, in **randomized positions**. Each block on its own covers the whole window evenly, so panel A, which
  is sectioned first, already gives a usable map. All four blocks together give 64 distinct powers and speeds,
  where the grid had 4 of each. The controls on all four panels measure track-to-track noise and any difference
  between panel positions on the plate, which later feeds the transfer question in the abstract. If the pilot
  shows no systematic difference between panels, the campaign can put a whole run on one or two panels (option B
  in [§3](#refreshing-the-panels-pick-one-with-josh-before-the-shop-work)).
- **The campaign uses batch Bayesian optimization, one run per batch.** Each run is 48 settings chosen by batch BO,
  the next 16-point Sobol block, and the 8 controls. BO fits a Gaussian process to the AM Module's error (measured
  minus predicted width and depth) and picks the settings that most reduce its uncertainty, weighted toward the
  regime boundaries. The Sobol block in each run is an unbiased hold-out for validating the model, which the
  BO-chosen points are not. If the campaign shrinks to one or two runs, skip BO and keep drawing Sobol blocks.
- **Powder layer:** use one layer at the standard parameter set's layer thickness.
- **Optional add-on, if a job can expose without recoating:** before the powder layer goes down, run a short
  bare-substrate job as a second row on one panel. The panels have room for it, so all four powder blocks stay.
  Bare-plate tracks remove the powder-layer uncertainty and are the cleanest data for calibrating absorptivity.
  [NIST's AM Bench](https://www.nist.gov/ambench) used bare-plate laser tracks for model validation in the same way.
- **Scan in the same direction on every track** and note how it sits relative to the gas flow. Expose from the
  downstream (gas outlet) side toward the inlet, so spatter lands on finished tracks rather than on fresh powder.
- **Commit the AM Module predictions for all 65 parameter sets** (64 Sobol settings plus the control) **before**
  the print.

**Processing order.** Section **panel A first, all the way through SEM**, to catch problems early: track mapping,
etch, SEM charging. Then do B to D. The timing log then shows both a first-time pass and a repeat pass.

**What to record for the model comparison:** powder certificate composition and particle size distribution;
nominal layer thickness and each panel's measured offset; panel alloy and surface finish; set and measured laser
power; spot size; gas, O₂ level and plate temperature; track length and scan direction; the track-to-parameter map.

## 5. Run sheet with estimated times

Log real times in [`m2-run-timing-log.csv`](m2-run-timing-log.csv), which uses the same step IDs.

| ID | Step | Who | First run (est.) | Routine (est.) |
| --- | --- | --- | --- | --- |
| A1 | Job file: track parts, parameter sets, slice, vector preview, track map | Carl + Josh | 4–8 h | 0.5–1 h |
| A2 | AM Module predictions for the run's parameter sets (committed before printing) | Xavier | 1–2 days of setup | ~1 h |
| A3 | Panels: cut, machine to fit, drill, grind flush, finish, clean, ID-mark, measure | Carl / shop | 1–2 days for a batch of 8 | 1–2 h per panel |
| B1 | Machine check: gas, filter, laser power check | Josh | 0.5–1 h | 15–30 min |
| B2 | Install plate and panels, check flushness, level to recoater | Josh + Carl | 0.5–1 h | 30 min |
| B3 | Load and sieve powder | Josh + Carl | 0.5–1 h | 30 min |
| B4 | Close up and inert to O₂ setpoint | machine | 0.5–1 h | 0.5–1 h |
| B5 | Recoat one layer and expose all tracks; video through the window | Josh | < 15 min | < 15 min |
| B6 | Cool and de-inert | machine | 15–30 min | 15–30 min |
| B7 | Depowder gently, photograph in place, unscrew the panels | Josh + Carl | 0.5–1 h | 30 min |
| B8 | Clean machine, return or sieve powder, handle waste | Josh + Carl | 1–2 h | 1 h |
| C1 | Top-view images of each panel (track continuity, balling) | Carl | 1 h | 30 min |
| C2 | Bandsaw the strip out of each panel and into pieces, then the fine wet saw (8 pieces) | Carl | 3–5 h | 2–3 h |
| C3 | Hot-mount 8 pucks | Carl | 2–3 h | 2 h |
| C4 | Grind, polish, etch | Carl | 4–6 h | 3–4 h |
| C5 | SEM: 72 tracks at two magnifications, plus a few EDS spots | Carl + Ronnie | 4–5 h | 3 h |
| C6 | Measure width, depth, height, area; classify regime | Carl | 3–4 h | 2 h (less once automated) |
| C7 | Upload measurements and track map; compare with predictions | Carl + Xavier | 2 h | 1 h |

Rough totals: the **machine day (B1–B8) is 4 to 8 hours** for two people on the first run, and about 4 hours once
routine. **Post-processing (C1–C7) is about 2 to
3 person-days.** Because C for run *n* overlaps A and B for run *n+1*, **one run a week** looks sustainable. Two a week
needs a second person on metallography and more SEM time.

For metal powder safety (PPE, explosion-rated vacuum, the M2's own SOP), see
[#105](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/105).

## 6. Schedule

This is provisional, and every date after the pilot gets re-planned from the timing log.

| Week of | What | Gate |
| --- | --- | --- |
| **Nov 9** | Kickoff with Josh (and Nathan C. if possible): confirm machine status, software and licences, powder grade on hand, and that the insert plate exists. Carl completes M2 and powder safety training. Xavier sets up the AM Module for the stainless grade. Book SEM time for the week of Nov 30. | Machine is running and the plate is located |
| **Nov 16** | Make or check 8 panels (4 plus 4 spares; 1–2 days of shop time). Build the job file and dry-run it in the software (one vector per track; export the map). Check laser power. Commit the AM Module predictions for the pilot's 65 settings. | Dry run passes |
| **Nov 23** (Thanksgiving Thu 11/26) | **Pilot print on Mon 11/23 or Tue 11/24** if prep is done; otherwise the first slot the next week. Section panel A right away. | 72 tracks printed and mapped |
| **Nov 30** | Metallography on panels A–D. SEM session. | Cross-sections are measurable |
| **Dec 7** | Measurements; compare with the predictions. **Pilot write-up**: timing log, problems found, campaign size. Go/no-go with Sterling by Fri Dec 11. | Go/no-go |
| Dec 14 – early Jan | Finals and holidays, light work: make the campaign's panels, set up the batch-BO loop and run AM Module predictions over the window, automate the melt-pool measurement. | — |
| **Jan 11 – Feb 19** | **Campaign, about 1 run a week.** Each run is one batch-BO round: 48 settings where the AM Module's error is most uncertain (regime boundaries first), 16 from the next Sobol block as a hold-out, and 8 controls. Runs 1–2 can add a second condition (bare substrate or a second layer thickness). Run 6 is a buffer or repeats. | Weekly check-in |
| **Feb 22 – Mar 5** | Calibrate on part of the tracks and validate on the held-out rest; parity plots; measured-vs-predicted printability map; talk figures. | — |
| **Mar 14–18** | TMS 2027, Orlando | — |

## 7. Sizing the campaign from the pilot

After the pilot, compute:

- **T_machine**: machine-day hours per run (B1–B8) and how many slots per week Josh can give.
- **T_post**: person-hours per run for C1–C7, including SEM availability.
- **Cadence** = runs per week = the smaller of the machine slots per week and (person-hours per week ÷ T_post).
- **Runs needed** = total tracks ÷ tracks per run (72 with this layout).

| Scope | What it covers | Tracks | Runs at 72 per run |
| --- | --- | --- | --- |
| **Minimum (TMS-ready)** | One layer thickness; 2–3 Sobol blocks of 64 plus BO points, with 8 controls per run; AM Module calibration and validation | ~110–150 plus controls | **pilot + 2–3** |
| **Standard** | Adds a second condition (bare substrate or a second layer thickness) and 2 runs of boundary refinement | ~300–400 | **pilot + 5–6** |
| **Extended** | Adds spot size or focus offset (if the M2 can adjust it), then small density cubes on the same panels | ~500+ | **pilot + 7–9** |

The original issue's "couple dozen runs" was for the whole ladder on the Aconity: tracks, cubes, artifacts, and
tensile bars. Single tracks alone should need far fewer runs, since adding tracks costs almost no machine time; the
bottleneck is metallography and SEM.

## 8. Kickoff checklist (Josh, and Nathan C. if possible)

- [ ] Machine status, last service, and laser power calibration date. Laser rating (200 or 400 W), spot size, single or dual laser.
- [ ] Inert gas (N₂ or Ar), O₂ setpoint, typical inerting time, plate heating, and which way the gas flows across the plate (the tracks are exposed from the outlet side, [§4](#4-pilot-run-carl-and-josh)).
- [ ] Software: Magics and build processor licence and version, WRX version, parameter-editing tier, limit on parameter sets per job, whether a job can expose without recoating.
- [ ] Powder: grade (316L? 17-4PH?), how much is on hand, lot and certificate, sieving, the minimum fill for the dose chamber.
- [ ] Insert plate: where it is, drawings, panel size and thickness, pocket depth, screw size, how panels are set flush (shims?), how many spare panels, and whether we may cut up Nathan C.'s panels; choose refresh option A or B for the campaign.
- [ ] Shop access for making panels (mill, drill, and a surface grinder with a vise or vacuum chuck, since 316L won't hold on a magnetic chuck) and for saws (a bandsaw that takes an 88 mm panel, an abrasive cut-off or precision saw).
- [ ] Metallography: hot-mount press, polisher, fume hood for aqua regia or an electrolytic oxalic setup.
- [ ] SEM: who is trained, how far ahead to book, conductive mounts, and whether the EMF has a holder for several 1.25" mounts or we should buy one ([§3](#cutting-without-wire-edm)).
- [ ] Where raw images live. Commit only measurements and representative images; the repo is public.

## Sources

- Materialise, [Concept Laser / Colibrium Additive L-PBF Build Processor](https://materialise.com/en/industrial/software/build-processor/concept-laser): per-part slice parameters, per-part build strategy sent to WRX, M2 compatibility.
- [Metal AM (2016)](https://www.metal-am.com/?p=61603), [New Equipment Digest](https://newequipment.com/home/product/55101922/68671-software-tool-permits-open-processing-of-all-parameter-settings), [Design World](https://www.designworldonline.com/control-additive-builds-concept-laser-parameter-editor/): CL WRX software tiers and the CL WRX Parameter licence.
- BYU Electron Microscopy Facility, [Apreo C specifications](https://microscopy.byu.edu/apreo-sem) and [startup SOP](https://microscopy.byu.edu/apreo-sem-startup-sop): the stage limits, the 1–2 mm equal-height rule, and the 3.0 mm widest field at 10 mm working distance.
- R. Weissbach, R. W. Penny, A. J. Hart, *A rapid experimental workflow for studying melt track scaling in laser powder bed fusion using high-precision metal template substrates*, [arXiv:2409.14548](https://arxiv.org/abs/2409.14548) (published in *Progress in Additive Manufacturing*): template inserts, the flatness tolerance, and the full sectioning and etching recipe.
- C. Kamath et al., *Density of additively-manufactured, 316L SS parts using laser powder-bed fusion at powers up to 400 W*, [OSTI 1116929](https://www.osti.gov/biblio/1116929): single tracks and density pillars on a 400 W M2 with a 54 µm D4σ spot.
- ORNL, [316L/316H coupon characterization framework](https://info.ornl.gov/sites/publications/Files/Pub199801.pdf): a framework for more than 700 coupons from a Concept Laser M2 and a Renishaw AM400.
- M2 configurations: [Treatstock](https://www.treatstock.co.uk/machines/item/248-m2-cusing?ln=en-GB) (250 × 250 × 280 mm, 200 W standard, 400 W option); [Empa](https://www.empa.ch/web/coating-competence-center/concept-laser-m2) (200 W, 90 µm spot).
- In this repo: [`thermocalc_am_module.md`](../edison-trajectories/thermocalc_am_module.md), [`edison-literature-high-report.md`](../edison-trajectories/tms-2027-lpbf-parameter-abstract-review/edison-literature-high-report.md) (single-track-first workflows such as Pfaff et al. 2020 and Bergmueller et al. 2023), and [`tms-2027-lpbf-process-parameter-optimization-abstract.md`](../tms-2027-lpbf-process-parameter-optimization-abstract.md).
