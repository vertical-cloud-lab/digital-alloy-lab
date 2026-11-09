# Single-track runs on BYU's Concept Laser M2 (stainless steel): pilot and schedule

Issue [#100](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/100). This is the fallback path from
the [2026-08-13 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/100#issuecomment-6201170907):
if the atomizer-to-printer loop isn't ready, print commercial stainless steel on BYU's M2 and use cross-section SEM
of single tracks to check the Thermo-Calc AM Module.

**Plan in brief**

1. **One pilot run first.** Carl and Josh print four inserts holding 72 single tracks: a 4 × 4 power-speed grid,
   repeated on each insert, plus two control tracks per insert. Carl times every step from job prep to SEM.
2. **Running many parameter sets in one build looks feasible on the M2** and seems to be the intended workflow:
   the Concept Laser build processor assigns parameters per part. What still needs checking on BYU's install is how
   to make each track come out as exactly one scan vector. A dry run in the software settles it (see
   [§2](#2-can-the-m2-run-many-parameter-sets-in-one-build)).
3. **Nathan C.'s four-insert plate removes the two worst steps.** The big plate is never lasered, so it never
   needs resurfacing. Nothing needs wire EDM, because the only thing we cut is a small cube, which a bandsaw plus an
   abrasive or precision saw can handle.
4. **The campaign size comes from the pilot's timing log.** My current estimate is about 3 to 4 person-days per
   run, which allows about one run a week. That fits 3 to 6 campaign runs (about 150 to 400 tracks) between
   mid-January and mid-February, ahead of TMS 2027 (March 14–18, Orlando). [§7](#7-sizing-the-campaign-from-the-pilot) shows
   how to redo that from measured times.

All durations below are **my estimates**, not measurements. Replace them with the pilot's numbers.

**Visuals** ([`m2-viz/`](m2-viz/README.md)): the [pilot design](m2-viz/out/m2-pilot-design.png) (P–v grid and track
map), the [run sheet and schedule](m2-viz/out/m2-schedule.png), and a 3-D animation of the whole process in three
parts: [print](m2-viz/out/m2_1_print.gif), [unload and cut](m2-viz/out/m2_2_cut.gif), and
[mount, SEM, compare](m2-viz/out/m2_3_sem.gif).

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
  tracks, each its own part carrying one of 17 parameter sets, is what the software is built for, not a hack.
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
- Is there a limit on parameter sets per job? If so, split the run into several short jobs, run back to back
  without breaking the inert atmosphere.
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

The tracks go on four small cubes seated in pockets in a full-size build plate. After a run we pull the four cubes
and put in fresh ones.

- **What it removes:** the big plate is never lasered, so it needs no resurfacing between runs, only cleaning
  (blow powder out of the pocket gaps). Nothing is welded to the plate, so wire EDM isn't needed.
- **Insert material** should match the powder (316L cubes for 316L powder). That keeps a different substrate from
  diluting the fused zone, and the substrate's thermal properties then match what the model assumes.
- **Flushness is the critical tolerance.** MIT's single-track work uses a rule of thumb of about 10 µm flatness and
  parallelism (10 to 20% of a layer), which grinding alone does not reliably hold. That is why ordinary builds
  sacrifice the first several layers to self-planarize
  ([Weissbach, Penny & Hart, arXiv:2409.14548](https://arxiv.org/abs/2409.14548)). A proud insert gets a thinner
  powder layer or catches the recoater, and a sunken one gets a thicker layer. **Before every run, dial-indicate
  each insert against the plate and record the offset.** It becomes that insert's layer-thickness input to the model.
- **Use the same surface finish on every insert,** for example ground and then lightly bead-blasted, and record it.
  Absorptivity and powder spreading both depend on it.
- **Mark each insert** with an ID and an orientation notch on the side. Mixing up the track-to-parameter map after
  sectioning is an easy way to lose a whole run.
- **Ask Nathan C.** for the plate, its drawings and any spare inserts. For old M2 job files and the machine's quirks,
  the repo notes that Dr. Nathan Crane's students were the last people to run the M2.

### Refreshing the inserts (pick one with Josh before the shop work)

| Option | How | Cost per run | Notes |
| --- | --- | --- | --- |
| **A. Consumable cubes** (simplest) | Section the cube and discard it | 4 new cubes (about 30 for a campaign) cut from 316L bar, faced and ground in one batch | No re-measuring of reused cubes. Shop time is up front. |
| **B. Re-topped cubes** | Bandsaw off the top 6–8 mm slab for metallography, regrind the top, then shim back to flush | About 3–4 uses per cube | Fewer cubes, but the flushness check and shimming come back every run |
| **C. No insert plate** (fallback) | Print on a normal plate and cut the region out, or put tracks on printed pedestals that can be cut off | Whole-plate resurfacing each run (mill or surface grinder) | Pedestals add hours of build time, and the plate gets thinner every time |

### Cutting without wire EDM

1. **Rough cut on the bandsaw** (bi-metal blade, with coolant for stainless): take the top slab off the cube and split
   it into one slab per row of tracks. A bandsaw face is rough and deformed, so cut **at least 1–2 mm away from the
   target plane** (mid-length of the tracks).
2. **Final face** on an abrasive cut-off saw with coolant, or a low-speed precision saw. MIT used a Buehler IsoMet
   4000 at 4000 rpm and 6 mm/min. Then grind down to the target plane.
3. **Mount** in conductive hot-mount compound so the SEM doesn't charge. A slab about 8 mm × 22 mm fits a 1.25" puck.
4. **Grind, polish and etch.** MIT's sequence was 320 then 800 grit, 3 µm diamond, then 0.05 µm alumina. Etch right
   after polishing, because 316 passivates quickly: MIT used dilute aqua regia for 30–45 s, which needs a fume hood.
   Electrolytic 10% oxalic acid is the usual alternative.
5. **Check under the optical microscope** that the etch is good and the track order matches the map. **Then SEM**:
   secondary-electron images of every track at two fixed magnifications. Ronnie's
   [Caliber](https://github.com/vertical-cloud-lab/caliber) can supply SEM and EDS acquisition settings.

## 4. Pilot run (Carl and Josh)

The goal is to get one run all the way from job file to measured cross-sections, with **every step timed**. The
pilot doubles as a machine health check.

**Layout (example for a cube with a 25 mm square top; rescale to Nathan C.'s real inserts).** Each insert has two rows
of 9 parallel tracks. Tracks are 8 mm long at 2 mm pitch, rows are 3 mm apart, and there is at least 3 mm of margin
from every edge. That gives 18 tracks per insert and **72 per run**.

**Parameters.** Use a **4 × 4 grid of power and speed** that straddles the predicted keyhole and lack-of-fusion/balling
boundaries, plus **2 control tracks per insert** at the machine's standard stainless parameter set. Xavier can pick the
grid from the AM Module printability map. As a starting point, for a 400 W M2:

| | 250 mm/s | 500 mm/s | 1000 mm/s | 2000 mm/s |
| --- | --- | --- | --- | --- |
| **100 W** | ✓ | ✓ | ✓ | ✓ |
| **200 W** | ✓ | ✓ | ✓ | ✓ |
| **300 W** | ✓ | ✓ | ✓ | ✓ |
| **375 W** | ✓ | ✓ | ✓ | ✓ |

That spans P/v from 0.05 to 1.5 J/mm, from likely balling up to deep keyholes. On a 200 W machine, scale it down.

- **Each insert carries one complete replicate** (16 grid tracks and 2 controls) in **randomized positions**. Four
  inserts give four replicates, and differences between insert positions on the plate become measurable instead of
  confounded with the parameters. The controls on all four inserts give a run-to-run and position check that later
  feeds the transfer question in the abstract.
- **Powder layer:** use one layer at the standard parameter set's layer thickness.
- **Optional add-on, if a job can expose without recoating:** run a short bare-substrate job on one insert before
  the powder layer goes down. That insert then gets no powder-layer tracks, which leaves three replicates. Bare-plate
  tracks remove the powder-layer uncertainty and are the cleanest data for calibrating absorptivity.
  [NIST's AM Bench](https://www.nist.gov/ambench) used bare-plate laser tracks for model validation in the same way.
- **Scan in the same direction on every track** and note how it sits relative to the gas flow. Expose from the
  downstream (gas outlet) side toward the inlet, so spatter lands on finished tracks rather than on fresh powder.
- **Commit the AM Module predictions for all 17 parameter sets** (16 grid plus control) **before** the print.

**Processing order.** Section **insert A first, all the way through SEM**, to catch problems early: track mapping,
etch, SEM charging. Then do B to D. The timing log then shows both a first-time pass and a repeat pass.

**What to record for the model comparison:** powder certificate composition and particle size distribution;
nominal layer thickness and each insert's measured offset; insert alloy and surface finish; set and measured laser
power; spot size; gas, O₂ level and plate temperature; track length and scan direction; the track-to-parameter map.

## 5. Run sheet with estimated times

Log real times in [`m2-run-timing-log.csv`](m2-run-timing-log.csv), which uses the same step IDs.

| ID | Step | Who | First run (est.) | Routine (est.) |
| --- | --- | --- | --- | --- |
| A1 | Job file: track parts, parameter sets, slice, vector preview, track map | Carl + Josh | 4–8 h | 0.5–1 h |
| A2 | AM Module predictions for the run's parameter sets (committed before printing) | Xavier | 1–2 days of setup | ~1 h |
| A3 | Inserts: machine and grind, finish, clean, ID-mark, measure flatness | Carl / shop | ~1 day for a batch of 8 | 2–3 h per 4 |
| B1 | Machine check: gas, filter, laser power check | Josh | 0.5–1 h | 15–30 min |
| B2 | Install plate and inserts, check flushness, level to recoater | Josh + Carl | 0.5–1 h | 30 min |
| B3 | Load and sieve powder | Josh + Carl | 0.5–1 h | 30 min |
| B4 | Close up and inert to O₂ setpoint | machine | 0.5–1 h | 0.5–1 h |
| B5 | Recoat one layer and expose all tracks; video through the window | Josh | < 15 min | < 15 min |
| B6 | Cool and de-inert | machine | 15–30 min | 15–30 min |
| B7 | Depowder gently, photograph in place, remove inserts | Josh + Carl | 0.5–1 h | 30 min |
| B8 | Clean machine, return or sieve powder, handle waste | Josh + Carl | 1–2 h | 1 h |
| C1 | Top-view images of each insert (track continuity, balling) | Carl | 1 h | 30 min |
| C2 | Bandsaw rough cut, then final cut (8 slabs) | Carl | 2–3 h | 1–2 h |
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
| **Nov 16** | Make or check 8 inserts (4 plus 4 spares). Build the job file and dry-run it in the software (one vector per track; export the map). Check laser power. Commit the AM Module predictions for the pilot grid. | Dry run passes |
| **Nov 23** (Thanksgiving Thu 11/26) | **Pilot print on Mon 11/23 or Tue 11/24** if prep is done; otherwise the first slot the next week. Section insert A right away. | 72 tracks printed and mapped |
| **Nov 30** | Metallography on inserts A–D. SEM session. | Cross-sections are measurable |
| **Dec 7** | Measurements; compare with the predictions. **Pilot write-up**: timing log, problems found, campaign size. Go/no-go with Sterling by Fri Dec 11. | Go/no-go |
| Dec 14 – early Jan | Finals and holidays, light work: make the campaign's insert batch, run AM Module predictions for the campaign grid, automate the melt-pool measurement. | — |
| **Jan 11 – Feb 19** | **Campaign, about 1 run a week.** Runs 1–2 fill out the power-speed grid (and a second condition: bare substrate or a second layer thickness). Runs 3–5 refine the regime boundaries and spots where model and data disagree, chosen by Bayesian optimization or active learning with the AM Module as prior; each run is one batch. Run 6 is a buffer or repeats. | Weekly check-in |
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
| **Minimum (TMS-ready)** | One layer thickness; about 6 × 6 power-speed grid × 3–4 replicates; AM Module calibration and validation | ~110–150 plus controls | **pilot + 2–3** |
| **Standard** | Adds a second condition (bare substrate or a second layer thickness) and 2 runs of boundary refinement | ~300–400 | **pilot + 5–6** |
| **Extended** | Adds spot size or focus offset (if the M2 can adjust it), then small density cubes on the same inserts | ~500+ | **pilot + 7–9** |

The original issue's "couple dozen runs" was for the whole ladder on the Aconity: tracks, cubes, artifacts, and
tensile bars. Single tracks alone should need far fewer runs, since adding tracks costs almost no machine time; the
bottleneck is metallography and SEM.

## 8. Kickoff checklist (Josh, and Nathan C. if possible)

- [ ] Machine status, last service, and laser power calibration date. Laser rating (200 or 400 W), spot size, single or dual laser.
- [ ] Inert gas (N₂ or Ar), O₂ setpoint, typical inerting time, plate heating.
- [ ] Software: Magics and build processor licence and version, WRX version, parameter-editing tier, limit on parameter sets per job, whether a job can expose without recoating.
- [ ] Powder: grade (316L? 17-4PH?), how much is on hand, lot and certificate, sieving, the minimum fill for the dose chamber.
- [ ] Insert plate: where it is, drawings, insert size, how inserts are held and set flush, how many spares; choose refresh option A or B.
- [ ] Shop access for inserts (mill or surface grinder) and saws (bandsaw, abrasive cut-off, precision saw).
- [ ] Metallography: hot-mount press, polisher, fume hood for aqua regia or an electrolytic oxalic setup.
- [ ] SEM: who is trained, how far ahead to book, conductive mounts.
- [ ] Where raw images live. Commit only measurements and representative images; the repo is public.

## Sources

- Materialise, [Concept Laser / Colibrium Additive L-PBF Build Processor](https://materialise.com/en/industrial/software/build-processor/concept-laser): per-part slice parameters, per-part build strategy sent to WRX, M2 compatibility.
- [Metal AM (2016)](https://www.metal-am.com/?p=61603), [New Equipment Digest](https://newequipment.com/home/product/55101922/68671-software-tool-permits-open-processing-of-all-parameter-settings), [Design World](https://www.designworldonline.com/control-additive-builds-concept-laser-parameter-editor/): CL WRX software tiers and the CL WRX Parameter licence.
- R. Weissbach, R. W. Penny, A. J. Hart, *A rapid experimental workflow for studying melt track scaling in laser powder bed fusion using high-precision metal template substrates*, [arXiv:2409.14548](https://arxiv.org/abs/2409.14548) (published in *Progress in Additive Manufacturing*): template inserts, the flatness tolerance, and the full sectioning and etching recipe.
- C. Kamath et al., *Density of additively-manufactured, 316L SS parts using laser powder-bed fusion at powers up to 400 W*, [OSTI 1116929](https://www.osti.gov/biblio/1116929): single tracks and density pillars on a 400 W M2 with a 54 µm D4σ spot.
- ORNL, [316L/316H coupon characterization framework](https://info.ornl.gov/sites/publications/Files/Pub199801.pdf): a framework for more than 700 coupons from a Concept Laser M2 and a Renishaw AM400.
- M2 configurations: [Treatstock](https://www.treatstock.co.uk/machines/item/248-m2-cusing?ln=en-GB) (250 × 250 × 280 mm, 200 W standard, 400 W option); [Empa](https://www.empa.ch/web/coating-competence-center/concept-laser-m2) (200 W, 90 µm spot).
- In this repo: [`thermocalc_am_module.md`](../edison-trajectories/thermocalc_am_module.md), [`edison-literature-high-report.md`](../edison-trajectories/tms-2027-lpbf-parameter-abstract-review/edison-literature-high-report.md) (single-track-first workflows such as Pfaff et al. 2020 and Bergmueller et al. 2023), and [`tms-2027-lpbf-process-parameter-optimization-abstract.md`](../tms-2027-lpbf-process-parameter-optimization-abstract.md).
