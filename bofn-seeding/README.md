# Seeding the BOFN campaign: which experiments come first (#275)

[#275](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/275) asks how to choose the
initial experiments for the Al alloy campaign in
[#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255), which
[#256](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/256) schedules. It suggests
a mix of three sources, about three runs each:

- **agent-chosen** compositions (literature, databases, CALPHAD);
- **known baselines** (AlSi10Mg, Scalmalloy);
- **Sobol** or another space-filling design.

It also asks:

- how to bring in the databases from [#7](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/7)
  and [#8](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/8);
- how "fantasy" data (synthetic, or from the literature) could stand in until real data exist;
- whether 3 + 3 + 3 makes sense with 25 experiments left.

Edison Scientific was the rubber duck, in three rounds ([`edison/`](edison/)):

1. q1, a `LITERATURE_HIGH` review of the 3 + 3 + 3 idea.
2. q2, a `LITERATURE_HIGH` review of seed alloys, datasets and cheap models.
3. q3, an `ANALYSIS` critique of this plan's first draft. It reran both scripts here. Its
   corrections are folded in below.

**Status:** this is a plan. Nothing here has been run on a real sample. The compositions are
proposals. They still need the CALPHAD screen, the design-space freeze, and a check of what is
actually on the shelf.

## Short answers

**On 3 + 3 + 3 with 25 left:** keep the three-way mix, but aim for about 6–7 seeds, not 9. Then
move the calendar so that the optimizer actually gets the runs this frees up.

- **Edison judged 9 seeds "slightly too many"** ([q1](edison/q1-seeding-strategy/artifact-00.md)).
  It suggests 3 baselines, 2 agent picks, 2 space-filling points, 14 optimizer runs and 4
  finalist runs. Its main citation is Bossek et al. (2020,
  [10.1145/3377930.3390155](https://doi.org/10.1145/3377930.3390155)). They found that small
  initial designs generally did better, with strong dependence on the problem. q1 read their
  best strategy as using about 30 % of the budget; q3 cautions that this is not a general
  optimum.
- **A toy simulation agrees on the direction** ([below](#how-many-seeds-a-toy-check)). This is
  the version with q3's fixes. 2 baselines + 3 agent + 1 space-filling beat 3 + 3 + 3 by
  0.036 ± 0.018 in the best value found (30 paired instances, both scenarios averaged). It beat
  the best baseline 72 % of the time, against 58 % for 3 + 3 + 3. Twelve seeds did no better
  than nine.
- **Don't add a third baseline run.** The 6063 runs (A1–A5) and commercial AlSi10Mg powder at P1
  are baselines that cost no design run. D1-r stays: it measures the benchmark's own spread
  ([#256](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#the-36-al-runs)).

**The 25-run ledger.** In the #256 calendar, eight runs come before the optimizer's first batch on
Dec 18: D1, D2, B30, B15 and S1–S4. Calling some of them something else frees nothing for the
optimizer. To actually get to about seven seeds:

| Role | Runs | Count |
|---|---|---|
| Seeds | D1, D2 (baselines); B30, B15 (dosing checks); S1, S2 (agent picks); S3 (space-filling) | 7 |
| Early optimizer pick ("R0") | S4. BOFN picks it at G1 (Dec 4), running on pseudo-data plus the A, B and D powder data. If that pipeline isn't ready by Dec 4, S4 becomes a second space-filling seed | 1 |
| Optimizer rounds | R1–R4 | 12 |
| Finalists | F1 ×2, F2 ×2 | 4 |
| Benchmark repeat | D1-r | 1 |
| **Total** | | **25** |

The flex slots X1–X3 (Dec 14–16) sit outside the 25. If they aren't needed to redo failed runs,
make them more R0 picks, chosen on Dec 11.

**What matters more than the split:**

1. **R1 (Dec 18) and R2 (Jan 8) are picked before any new composition has strength data.** Seed
   tensile bars print at P3 (Jan 12–13) and are tested Jan 19–22. Until then, the strength nodes
   run on priors: literature data and strength models
   ([pseudo-data](#literature-and-fantasy-data)). If you can, pull one sentinel tensile test
   forward, such as D1 bars at P2 (Dec 16–17). Otherwise, say plainly that the first two batches
   are prior-driven for strength.
2. **Most of the literature's best Sc-free seeds need Zr, Fe, Ce or Cu.** None of these is on the
   [Nov 13 list in #146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6842840090)
   (Mn, Cr, Zn, Sn, Mg, Sc, Er, Ti from ESPI; Si, Fe, Ni and Cu were never ordered). The
   Scalmalloy-type benchmark D2 needs Zr as well. An order isn't enough. Confirm delivery, the
   carrier composition (e.g. an Al–Zr master alloy), the dissolution time and temperature, and
   the recovery, before the S runs (Dec 7–10).
3. **A 6063 cup brings its own chemistry.** Every charge built in 6063 cups also carries about
   0.5–0.7 Mg and 0.3–0.4 Si, and master alloys bring extra Al. So nominal compositions like
   Al–3.2Mn–1.5Cr can't be made that way. Either switch to a high-purity Al base (#256's do-now
   list raises this) or mass-balance every recipe against what is reachable (the byu-vcl
   reachability script referenced in #146).
4. **The design box on [PR #72](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/72)
   excludes several of the best-documented Sc-free LPBF alloys.** S2 below breaks its Fe cap
   (0.5 wt%) and its Zr cap (1 wt%). Al–10Ce breaks the Ce cap (6 wt%). Addalloy-type
   Al–4.5Mg–1.5Zr breaks the Zr cap. Its Mg + Si ≤ 6 wt% joint cap even excludes AlSi10Mg. Settle
   these at the design-space freeze (G0, today).
5. **Freeze the success criteria and the mineral-burden metric before picking seeds.** For
   success, decide:
   - yield or ultimate strength;
   - matched heat treatment and build orientation;
   - minimum ductility and density;
   - what counts as "beats" given the uncertainty.

   For the metric, note that of the 15 palette elements only Fe, Si and Cu are absent from the
   USGS 2022 critical minerals list. Al itself is on it, so say whether the metric counts Al.
   By a plain wt% count of listed additions, Al–4Mn–0.5Ti–0.5Zr (5 wt%) is only a little leaner
   than Scalmalloy (about 6 wt%, counting Mg). Sc-free is not the same as low burden. Fe- and
   Si-based strengthening is where "stronger and leaner" is easiest to show.

**Space-filling:** pick space-filling seeds with `imse` (integrated variance), on a reachable,
screened pool, optionally with a minimum distance. Maximin picked boundary-heavy alloys here. Sobol
with an exclusion radius didn't exclude anything in its first picks. In 7-D, two or three points
cover little whatever the method, so space-fill in a reduced space: CALPHAD descriptors, which are
what the downstream nodes see ([details](#space-filling-around-the-points-already-chosen)).

**"Fantasy" data:** call it pseudo-data, keep it in its own source, and never overwrite it in
place. It isn't BoTorch's `fantasize`
([#104](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/104)).
[Below](#literature-and-fantasy-data).

**The pre-registered AI benchmark:** every policy has to start from the same seed set. If only
the AI policy gets the agent picks, the "acceleration factor" measures a warm start, not the
optimizer (Edison q1, pitfall P9). [Below](#making-the-seeds-count-for-the-paper).

## What the 25 experiments are

The [#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#the-36-al-runs)
has 36 Al atomizer runs. Five are the 6063 baseline repeats (A1–A5) and six are flex slots
(X1–X6). That leaves 25 runs whose composition someone has to choose:

| Block | Runs | When | Role in #256 |
|---|---|---|---|
| D benchmarks | D1 (AlSi10Mg-type), D2 (Scalmalloy-type), D1-r (repeat) | Nov 30, Dec 2, Feb 8 | baseline seeds |
| B dosing checks | B30 (Si ≈ 3.9 wt%), B15 (Si ≈ 2.1 wt%) | Dec 1, Dec 3 | known-composition checks on the Al–Si line |
| S CALPHAD seeds | S1–S4 | Dec 7–10 | agent-chosen seeds |
| R optimizer rounds | R1–R4, 3 each | Jan 5 – Feb 3 | optimizer |
| F finalists | F1 ×2, F2 ×2 | Jan 25–28 | repeats of optimizer picks |

Following Edison (q1, P10), count the 6063 repeats, the dosing checks and D1-r once each for
coverage, since each is one composition. Count every run toward estimating noise.

## A proposed seed set

| Slot | Strategy | Composition (wt%) | Why | Needs | In the PR #72 box? |
|---|---|---|---|---|---|
| A1–A5 | baseline (free) | 6063 bar | Run-to-run noise; the dilute end | on hand | yes |
| P1 | baseline (free) | commercial AlSi10Mg powder | Print-window, density, tensile and corrosion baselines with no atomizer run. Not a substitute for D1, which goes through our own atomizer | on hand | — |
| D1 | baseline | Al–10Si–0.35Mg | The alloy to beat. As-built YS ≈ 250–350 MPa ([q2](edison/q2-seed-alloys-and-data/artifact-00.md)) | 4047 + Mg | the Mg + Si ≤ 6 cap says no; drop that cap |
| D2 | baseline | Al–4.5Mg–0.7Sc–0.3Zr(–0.5Mn) | The Sc reference. YS 256–278 MPa as-built, 456–469 MPa direct-aged ([10.3390/cryst15010025](https://doi.org/10.3390/cryst15010025)) | Sc on hand; **Zr** | yes |
| B30 | dosing check | 30 % 4047 in 6063 cups, Si ≈ 3.9 | Does measured Si follow the charge? | on hand | yes |
| B15 | dosing check | as planned (Si), or retargeted to Mn or Zr | Retarget only if that is the larger dosing uncertainty for S1 and S2 (q3). Elemental Si dissolved only 29–44 % in 2–3.5 min at 738 °C ([#111](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/111)), so solid additions can't be assumed to dissolve | Mn on hand | yes |
| S1 | agent | **Al–4Mn–0.5Ti–0.5Zr** | Sc-free. Mn kept in supersaturated solid solution, plus L1₂ Al₃(Ti,Zr) nucleants. Reported YS 284, UTS 320 MPa, 16.9 % elongation as-built, crack-free with no preheat at 380 W and 1900 mm/s (Mair et al., [10.1016/j.jallcom.2021.163156](https://doi.org/10.1016/j.jallcom.2021.163156)). A mechanism probe, not a proven winner: 284 MPa overlaps AlSi10Mg's range and is below aged Scalmalloy. Its nucleation route overlaps D2's, so the Mn supersaturation is what's new | Mn, Ti on hand; **Zr** | yes |
| S2 | agent | **Al–1.87Fe–1.02Mg–1.03Zr** | An Fe-based eutectic. Fe is cheap and not on the critical list. This is the measured chemistry of the printed alloy in Li et al. ([10.1080/17452759.2025.2516663](https://doi.org/10.1080/17452759.2025.2516663)): YS 376, UTS 406 MPa, 11 % elongation after 400 °C/4 h (as reported by Edison) | **Fe**, **Zr** | no (Fe 1.87 > 0.5; Zr 1.03 > 1.0) |
| S3 | space-filling | from `seed_design.py --method imse` on the screened, reachable pool | Covers what D1, D2, S1 and S2 leave out. Today's examples from the on-hand elements are [below](#space-filling-around-the-points-already-chosen) | depends | yes |
| S4 | R0 (optimizer) | picked by BOFN at G1 (Dec 4) | Its first pick, made on pseudo-data plus powder data. Falls back to a second space-filling seed | depends | — |

If the feedstock or the freeze rules out S1 or S2, the rest of Edison's shortlist
([q2 table](edison/q2-seed-alloys-and-data/artifact-00.md)) offers these alternatives:

- **Al–4Mn–1.3Mg–0.3Zr:** inside the box. 99.6 % dense and crack-free, but a hardness study only,
  with no tensile data.
- **Low-Sc bridge, Al–4.5Mg–0.3Sc–0.4Zr:** YS ≈ 220 MPa as-built, ≈ 380 MPa direct-aged (indicative).
  If matching aged Scalmalloy is the main route, this resolves the Sc trade-off better than D2 plus
  zero-Sc picks (q3). It sits close to D2, though.
- **Al–Fe–Cr quasicrystal alloy:** YS 395 MPa as-built, but only 4 % elongation. Needs Fe.
- **Addalloy-type Al–4.5Mg–1.5Zr:** YS ≈ 315 MPa. Over the Zr cap, and Mg evaporates.
- **Al–10Ce:** not a good fallback (q3). It breaks the Ce cap, carries 10 wt% of a listed element,
  and is weaker at room temperature (YS ≈ 222 MPa).
- **A20X-type:** needs Cu and Ag, and Ag isn't in the palette.

**With only the elements on hand** (Mn, Cr, Mg, Ti, Er, Zn, plus Si from 4047), the agent picks
fall back to Zr-free cousins such as Al–Mn–Cr or Al–Mn–Ti. These have weaker literature support,
because Zr is what suppresses cracking in most of these alloys. That is the case for getting Zr in
before Dec 7.

## Seeds for every node, not just compositions

BOFN keeps one GP per node, and each needs its own starting data. Edison found three relevant
results ([q1 §4](edison/q1-seeding-strategy/answer.md)):

- BOFN and pKGFN papers start from full-network evaluations (Astudillo and Frazier 2021; Buathong
  et al. 2023).
- Node-level initial designs, each in its node's own input space, have also been published
  (Kudva et al. 2026, MOBONS).
- The newer pKGFN formulation drops the rule that upstream nodes must be evaluated first. That lets
  downstream data come from other sources (Buathong and Frazier 2025).

Most of that node-level data needs no atomizer run:

| Node | Inputs → outputs | Seeds that cost no atomizer run | Seeds from atomizer runs | When |
|---|---|---|---|---|
| CALPHAD descriptors | composition → liquidus, solidus, freezing range, Scheil cracking indices (Kou, CSC), phase fractions | A cheap, known function. Compute thousands of compositions with pycalphad now and Thermo-Calc once licensed ([#141](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/141)) | — | W1–W3 |
| Mineral burden | composition → weighted critical-mineral content | Analytic; freeze the weights first | — | G0 |
| Dosing and composition fidelity | charge recipe → measured composition (EDS, ICP-OES) | 6063 and 4047 as received | B30, B15, D1, D2, then every run | Dec 1–3 |
| Atomization | measured composition or its descriptors, superheat, amplitude → yield in cut, D10/D50/D90, sphericity, oxygen | Earlier runs (Oct 2, 6 and 8, and the 4047 runs in [#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159)), tagged with their settings. Lang's relation as a prior mean for size, ± 20–30 % (q2) | A1–A5 (noise), then every run | from Nov 17 |
| Powder characterization (SEM/EDS) | powder → size and shape, satellites, homogeneity | Commercial AlSi10Mg 15–45 µm; the analysis pipeline from [#225](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/225) | Every run, at the Thursday session | weekly |
| Print parameters (tracks, cubes) | powder descriptors + power, speed, hatch, layer → melt-pool depth and width, mode, density, cracks | See the three sources below this table | In-house 6063 and D1 at P2; S-run tracks at P2 | P1 Dec 2–3, P2 Dec 16–17 |
| Hardness (the fast strength screen) | printed material, heat treatment → HV | P1 AlSi10Mg cubes, wrought 6063, published HV for the benchmarks | D1 and the S runs, from P2 and P3 | from Dec 11 |
| Tensile | printed material → yield strength, UTS, elongation | P1 AlSi10Mg bars. Literature values ([q2 table](edison/q2-seed-alloys-and-data/artifact-00.md)). Strengthening models ([q2](edison/q2-seed-alloys-and-data/artifact-02.md)), e.g. about 104 MPa from 3.7 wt% Mn kept in solid solution | Seeds from P3, then the finalists | Dec 14–16, Jan 19–22, Feb 9–12 |
| Corrosion | material → OCP, polarization | Wrought 6063 and printed AlSi10Mg, already in #256 | Finalists | when the electrodes arrive ([#221](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/221)) |

The print-parameter node has three sources that need no new alloy:

- **Literature.** The Barrionuevo LPBF density dataset in [`database-samples/`](../database-samples/)
  has 353 AlSi10Mg rows from 15 papers and 12 printers. 18 are on AconityLAB and 27 on a Concept
  Laser M2, the machine BYU has.
- **Models.** Eagar–Tsai and AM Module printability maps
  ([#262](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/262)).
- **P1.** Commercial AlSi10Mg single tracks in Sobol blocks, as in
  [#243](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243), plus cubes.

Two consequences:

- **The print-parameter node doesn't need new alloys to get started.** The atomizer runs only have
  to teach it how a new composition shifts the window. One build plate holds many parameter sets,
  so space-fill the print parameters on the plate, within the window the models predict.
- **Space-filling belongs in each node's own input space** (Edison q1, P6). A downstream GP sees
  CALPHAD descriptors and powder properties, not raw wt%. Once the CALPHAD screen exists, pick
  the space-filling seeds in descriptor space:
  `seed_design.py --candidates screen.csv --features ...`. The screen is a candidate pool. Only
  real observations (with their noise) belong in the existing points, not screened candidates.

**Write down a node-by-date data contract** before Dec 18: which node has what data, from which
source, on each decision date. That is what the R0–R2 picks actually rest on.

## Space-filling around the points already chosen

[`seed_design.py`](seed_design.py) adds space-filling points around everything in
[`seeds.csv`](seeds.csv): 6063, D1, D2, B30, B15, and the proposed S1 and S2.

**The distance.** Each element's wt% is divided by its upper bound. That is a modelling
assumption: it puts the full Ti range (0.5 wt%) on a par with the full Si range (12 wt%), as a GP
with `Normalize` over the box and equal length scales would. On top of that, every element that
one alloy has and the other doesn't adds 0.25 to the squared distance (`--set-weight 0.5`), so
different element sets count as further apart. Edison flagged plain Euclidean distance for sparse
compositions (q1, P5). The set term switches on at any non-zero amount, so give measured
compositions an intentional-addition threshold before they go into `seeds.csv`. Otherwise trace
impurities switch every element on.

**The candidates:**

- The bounds are the finalized ones on [PR #72](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/72):
  Al ≥ 85 wt%, a cap per element, a 0.10 wt% floor for any element that is switched on, and its
  joint caps except Mg + Si.
- Each candidate has one to three additions, drawn from the elements on hand
  ([#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146)): Mn, Cr, Mg, Ti, Er
  and Zn, plus Si through 4047. They are sampled face by face on the sparse simplex.
- Each has at least 3 wt% of additions in all (`--min-total 3`). That keeps space-filling runs out
  of the dilute corner, which the 6063 runs already cover. It is a judgment call, not a strength
  screen: it also excludes lean precipitation-strengthened alloys. With `--min-total 0`, `imse`
  picks dilute binaries (Al–0.29Ti, Al–2.45Mn).
- About two thirds of the pool has three additions. "Average coverage" below therefore means
  coverage of this pool, not of every plausible alloy.

**The four methods:**

| Method | What it does |
|---|---|
| `sobol` | First feasible points of a scrambled Sobol sequence, sampled face by face on the sparse simplex. Ignores the existing points |
| `sobol-exclusion` | Walks the same sequence and skips points within a radius of an existing or picked point (the heuristic in #275) |
| `maximin` | Greedy maximin, i.e. Kennard–Stone augmentation (Edison q1's recommendation): each pick is the candidate farthest from everything so far |
| `imse` | Greedy integrated-variance reduction: each pick most lowers the average variance of a GP over the pool. That variance depends only on where the points are and the kernel's hyperparameters (length scale 0.5), not on outcomes. It treats the planned points as noise-free observations, which is optimistic if a run fails. `--min-distance` adds a maximin-style floor |

Two new points around the seven existing ones, averaged over 10 scrambles
([`results/space_filling_compare.csv`](results/space_filling_compare.csv)):

| Method | Nearest existing point ↑ | Nearest pair of new points ↑ | Fill distance ↓ | Mean distance to nearest point ↓ | Mean GP variance ↓ |
|---|---|---|---|---|---|
| (existing points only) | | | 1.92 | 1.17 | 0.965 |
| `sobol` | 1.11 | 1.52 | 1.83 | 1.06 | 0.939 |
| `sobol-exclusion` | 1.11 | 1.52 | 1.83 | 1.06 | 0.939 |
| `maximin` | 1.83 | 2.11 | **1.69** | 1.11 | 0.957 |
| `imse` | 0.94 | 1.34 | 1.78 | **0.99** | **0.915** |

The picks for seed 0 ([`results/`](results/)):

| Method | SF1 (wt%) | SF2 (wt%) |
|---|---|---|
| `sobol`, `sobol-exclusion` | Al–2.72Cr–0.31Ti | Al–0.86Mn–2.12Cr–0.30Er |
| `maximin` | Al–3.00Cr–0.50Er–7.45Zn | Al–4.86Mg–0.48Ti–0.45Er |
| `imse` | Al–3.22Mn–1.45Cr | Al–7.63Si–0.28Er |
| `imse --min-distance 1.2` | Al–3.22Mn–1.45Cr | Al–6.55Zn |

What this shows:

- **Two or three points don't fill a 7-D space, whichever method picks them.** The best method lowers
  the mean GP variance from 0.97 to 0.92. In a reduced space the same runs cover much more:
  CALPHAD descriptors, or one or two sub-system families.
- **Each method wins the criterion it targets.** `imse` wins on average coverage (mean distance,
  mean variance). `maximin` wins on worst-case coverage (fill distance) and on separation. Neither
  result says which seeds lead to better optimization.
- **In this pool and metric, maximin picked boundary-heavy alloys.** For example, Al–3Cr–0.5Er–7.5Zn
  sits on three caps at once. Maximizing separation is expected to pull points to the boundary;
  this is not a bug. My judgment, untested, is that such alloys are among the harder ones to melt,
  dose and print. Prefer maximin when the kernel's length scales are unreliable, when rare families
  and worst-case coverage matter, or after a credible manufacturability screen has removed unsafe
  extremes (q3). A compromise is `imse --min-distance`.
- **The exclusion radius didn't bite in the first picks.** The first Sobol points were already well
  away from every existing point, so `sobol` and `sobol-exclusion` picked the same alloys. The pool
  does hold candidates within the radius (130 of 11,136 for seed 0, as q3 also counted); the walk
  just didn't reach them. With the set term, any two alloys with different element sets are at least 0.5 apart, so a
  radius of 0.5 mainly tests alloys with the same element set.
- **The Al–Mn–Cr pick is the most stable one.** Al–(3.2–3.7)Mn–(1.5–1.7)Cr appears at length
  scales 0.25 and 0.5, with or without the minimum distance. The other pick moves with the
  settings: Al–8.3Si at 0.25, Al–7.6Si–0.3Er at 0.5, Al–6.6Zn with the minimum distance. At 1.0,
  both picks are Zn-bearing (Al–1.6Mn–0.2Er–3.3Zn, Al–1.6Cr–0.2Ti–2.9Zn). So the tables are
  examples. The real S3 (and S4
  if it falls back) should come from rerunning on the screened, reachable pool with the actual
  seeds. q3's rerun found `imse` kept its average-coverage lead at length scales 0.25–1, and with
  the set term or the 3 wt% floor removed.

## How many seeds: a toy check

[`budget_split_sim.py`](budget_split_sim.py) is a flat-GP toy, not a model of the campaign:

- **The space.** A 6-D unit box, where the response depends mostly on 3 hidden dimensions.
- **The response.** A "known family" bump of height 0.7, where the baselines sit (good, not
  best). A better bump of height 1.0 somewhere else, and a decoy.
- **The seeds.** The agent picks are drawn around the better bump ("agent right") or around the
  known family ("agent wrong"). One free weak point stands in for 6063.
- **The optimizer.** The remaining runs go to batches of 3, picked by qLogEI from a discrete pool.
- **The runs.** 30 problem instances, each run in both scenarios. Every split sees the same
  instances and the same random seeds, so the differences are paired.

| Split (baselines + agent + space-filling) | Seeds | Best of 25, agent right | Best of 25, agent wrong | Paired difference vs 3 + 3 + 3 (both scenarios) | P(beat best baseline by 0.05) |
|---|---|---|---|---|---|
| 3 + 3 + 3 (proposed) | 9 | 0.937 | 0.841 | — | 0.58 |
| 2 + 2 + 2 | 6 | 0.958 | 0.879 | +0.030 ± 0.017 | 0.67 |
| **2 + 3 + 1** | 6 | **0.981** | 0.869 | **+0.036 ± 0.018** | **0.72** |
| 2 + 4 + 0 | 6 | 0.970 | 0.875 | +0.033 ± 0.022 | 0.68 |
| 2 + 0 + 4 | 6 | 0.883 | **0.883** | −0.007 ± 0.036 | 0.53 |
| 2 + 0 + 1 | 3 | 0.875 | 0.875 | −0.015 ± 0.030 | 0.53 |
| 3 + 3 + 6 | 12 | 0.951 | 0.840 | +0.006 ± 0.017 | 0.65 |
| 2 + 23 Sobol, no optimizer | 25 | 0.767 | 0.767 | −0.122 ± 0.040 | 0.43 |

Notes on the table:

- The global maximum is about 1.0.
- ± is one standard error over the 30 instances, with each instance's difference averaged over
  the two scenarios first.
- Splits without agent picks give the same result in both scenarios, as they should.
- No GP fit failed.
- Full results are in [`results/budget_split/`](results/budget_split/).
- q3's rerun of the first version of the script gave +0.048 ± 0.016 for 2 + 3 + 1.

What it says, within its assumptions:

- **About six seeds did better than nine.** 2 + 2 + 2, 2 + 3 + 1 and 2 + 4 + 0 each beat 3 + 3 + 3
  by 0.03–0.04, about two standard errors. Twelve seeds were no better than nine. Three seeds
  without agent picks were about the same as nine.
- **Agent picks pay off when they know something,** by +0.11 when they're right (2 + 3 + 1 at
  0.981 against 2 + 0 + 1 at 0.875). When they're wrong, the toy says they cost little. But see the
  assumptions below, which favour that.
- **3 + 3 + 3 and 3 + 3 + 6 did worst of the optimizer splits when the agent pointed back at the
  known family** (0.84, against 0.87–0.88). Six of their seeds crowd that family.
- **2 + 3 + 1 had the best average and the best chance of beating the baseline.** The differences
  among the six-seed splits are within noise, though.

What the toy leaves out, and why the real answer may need more seeds:

- In the toy the optimizer sees its result at once. In the campaign, strength comes back weeks
  after a run.
- Failed runs ([#274](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/274)).
- Feasibility.
- The function-network structure.
- A 15-element space.
- The baselines all sit in one family, not two distinct ones (AlSi10Mg and Scalmalloy).

Two of its assumptions favour the claim that a mistaken agent costs little:

- "Agent right" knows where the optimum is and which dimensions matter.
- "Agent wrong" only revisits a good family. It never proposes poor or unprintable alloys.

No IMSE or maximin seed policy was tested. So take it as evidence on the direction, not on the
exact number. It can be rerun on the 5-node synthetic network in
[#265](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/265) once that exists.

## Literature and "fantasy" data

#275's "fantasy modelling" is synthetic or literature data that stands in until real data exist.
BoTorch's `fantasize` is something else: it conditions a model on sampled outcomes at pending
points, so that a batch doesn't pick the same point twice. The second meaning is what
[#104](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/104) is about, and what pKGFN
needs. To keep them apart, this folder calls the first kind **pseudo-data**. Edison calls running
the whole loop on it a "synthetic digital-twin dry run" (q1, P7).

How to use pseudo-data without fooling the model (Edison q1 §5, P8):

- **Give every row a `source`** (in-house, literature, database, model) and keep a separate noise
  level per source. Assuming one noise level for every source degrades multi-fidelity BO
  (Foumani et al. 2023).
- **Put it in through the model, not as if it were our own data.** Options:
  - a multi-task or multi-fidelity GP with the source as the task;
  - a prior mean from a physics model, with the GP learning the residual;
  - an RGPE-style ensemble, whose weight on the literature falls as our own data arrive.
- **Never overwrite a pseudo-data row with a real value.** Add the real row and let the source term
  take care of the rest. That keeps the replay honest, and it shows how far the priors were off.
- **Use it first for the dry run.** Run the whole loop from data ingestion to a batch on
  pseudo-data before Dec 4, so that R0 and R1 aren't the first time the code sees a full network.

What each node can start from:

| Node | Pseudo-data source |
|---|---|
| Print parameters | Barrionuevo AlSi10Mg rows (local); NIST AM-Bench 2022 Al single tracks ([MDS2-2525](https://data.nist.gov/od/id/mds2-2525)); Eagar–Tsai with an absorptivity fitted to P1 tracks, accurate to about ± 20–30 % in conduction mode |
| Cracking | Scheil Kou index and CSC from CALPHAD, used as features or soft constraints |
| Strength | Literature tensile values (q2 table); solid-solution, Orowan and Hall–Petch terms, each about ± 15–25 % when retained solute and particle sizes are known |
| Atomization | Lang's relation, ± 20–30 % |

Taheri-Mousavi et al. (2024, [10.48550/arXiv.2406.17457](https://doi.org/10.48550/arXiv.2406.17457))
is the closest precedent. They used CALPHAD-derived descriptors and about 40 training compositions
with expected improvement to design an LPBF Al–Er–Zr–Ni alloy.

**Databases from #7 and #8**, sorted by node:

- **Print parameters:**
  - the Barrionuevo dataset (local, 1,579 rows, six alloys);
  - NIST AM-Bench 2022 (Al single tracks).
- **Strength:**
  - review tables: Aversa et al. 2019, [10.3390/ma12071007](https://doi.org/10.3390/ma12071007),
    and Liu et al. 2024, [10.1088/2631-7990/ad1657](https://doi.org/10.1088/2631-7990/ad1657);
  - the Luo 2024 AlSi10Mg process-structure-property set on Zenodo, listed in
    [`alloy-databases.md`](../alloy-databases.md);
  - an AlSi10Mg tensile set (Jatti et al., PLOS ONE, [10.1371/journal.pone.0324049](https://doi.org/10.1371/journal.pone.0324049)).
- **Wrought and cast handbook data only:**
  - Knovel, Total Materia and MatWeb. These give the wrought 6063 baseline, not LPBF behaviour.
- **No use at these nodes:**
  - the DFT repositories (AFLOW, OQMD, JARVIS, NOMAD).

Edison couldn't verify the DOI it gave for a separate Barrionuevo AlSi10Mg data descriptor, so
check that DOI before using it.

## Making the seeds count for the paper

The schedule pre-registers an AI benchmark at G1 (Dec 4). Edison q1 (§6, P9) makes three points
about it:

- **Use one common seed set for every policy:** random, expert design of experiments, standard BO
  and BOFN. That set is the baselines and the space-filling seeds.
- **Count the agent picks on purpose.** Either put them in the common set, or charge them to the AI
  policy's budget. Report the warm-start effect and the optimizer's effect separately.
- **Replay only on points that were actually measured.** Anything else needs a clearly labelled,
  cross-validated simulator, and causal acceleration claims should be avoided.

Also freeze the executable protocol at G1: objective, constraints, per-source noise or fidelity,
how failures and pending points are handled, repeats, and common seeds and budgets. With about 20
compositions, the acceleration factor will rest on that simulator. Space-filling seeds make it
less wrong away from the optimizer's path, which is one more reason to keep one or two.

## Before Dec 18, in order

From Edison q3's list ([answer](edison/q3-plan-critique/answer.md)), adjusted to the schedule:

1. **Freeze the success criteria and the mineral-burden metric** (G0, today). See short answer 5.
2. **Fix the ledger and the recipes.** Adopt (or reject) the table above. Confirm Zr, and Fe if S2
   stays. Mass-balance every recipe against the 6063 cups and the master-alloy carriers. Decide on
   a low-Sc bridge seed.
3. **Write the node-by-date data contract.** Pull one sentinel tensile test forward if you can.
4. **Freeze the executable optimization protocol and dry-run it on pseudo-data** by G1 (Dec 4), so
   it can pick S4.
5. **Rerun `seed_design.py` on the final screened, reachable pool,** with the actual seeds, then pick
   S3 (and S4 if it falls back).

## Pitfalls

From Edison q1's table ([artifact-01](edison/q1-seeding-strategy/artifact-01.md)), q3, and this
work:

| Pitfall | Do instead |
|---|---|
| Nine seeds before the first batch leave only 12 optimizer runs | About 7 seeds; S4 as an early optimizer pick |
| Relabeling slots without moving them frees nothing | Change what is decided when (the ledger above) |
| A 10d rule would need 140–150 runs in 15-D | Shrink the space before atomizing: at most 3–4 additions, CALPHAD descriptors as GP inputs, sparse kernels |
| Agent picks cluster around Al–Si–Mg and Al–Mg–Sc–Zr | Two picks, with different mechanisms and element sets, chosen away from D1 and D2 |
| A literature property attached to the wrong chemistry | Quote the measured chemistry from the paper (S2 was wrong in the first draft) |
| Sobol in the full 15-element simplex is almost never feasible | Sample face by face on the sparse simplex (as `seed_design.py` does) |
| Nominal compositions that 6063 cups can't make | Mass-balance recipes, or use a high-purity base |
| Maximin picks boundary-heavy alloys | `imse`, `imse --min-distance`, or maximin after a manufacturability screen |
| Euclidean distance ignores element identity | Add an element-set term (`--set-weight`), with an intentional-addition threshold |
| Composition-only space-filling leaves the downstream nodes cold | Seed each node from its own cheap sources; space-fill in descriptor and print-parameter space |
| Pseudo-data pooled with real data biases the model | A source column, per-source noise, multi-task or multi-fidelity; never overwrite rows |
| Seeds differ between the compared policies | One common seed set; report warm-start and optimizer effects separately |
| The seeds need elements we don't have | Check Zr, Fe and Ce now |
| Failed runs dropped from the data | Record failures as outcomes ([#274](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/274)) |

## Files

| File | What |
|---|---|
| [`seeds.csv`](seeds.csv) | Points already chosen (6063, D1, D2, B30, B15) and proposed (S1, S2). Replace nominal compositions with measured ones as they come in |
| [`seed_design.py`](seed_design.py) | Space-filling picks around `seeds.csv`, in composition space or, after the CALPHAD screen, in descriptor space |
| [`budget_split_sim.py`](budget_split_sim.py) | The toy simulation of seed and optimizer splits of 25 runs |
| [`results/`](results/) | Outputs of both scripts |
| [`edison/`](edison/) | The Edison queries, answers, artifacts, notebook and full trajectories, plus `edison_tasks.py`, which submits, waits for and fetches them |

```bash
pip install numpy scipy
python bofn-seeding/seed_design.py --n 2                 # imse around seeds.csv
python bofn-seeding/seed_design.py --n 2 --compare       # all four methods
python bofn-seeding/seed_design.py --n 2 --min-distance 1.2
python bofn-seeding/seed_design.py --elements Mn Cr Mg Si Er Ti Zn Zr   # once Zr is on the shelf
python bofn-seeding/seed_design.py --candidates screen.csv --features freezing_range kou_index l12_fraction

pip install torch botorch
python bofn-seeding/budget_split_sim.py --reps 30 --workers 4   # about 8 min on 4 cores
```

## Edison tasks

| Task | Job | ID | Folder |
|---|---|---|---|
| q1: rubber-duck the 3 + 3 + 3 plan | `LITERATURE_HIGH` | `2d0326f1-fc13-4a90-bcd0-6f92d885d5c8` | [`edison/q1-seeding-strategy/`](edison/q1-seeding-strategy/) |
| q2: seed alloys, datasets, cheap models | `LITERATURE_HIGH` | `33e883b7-532f-4792-b4b6-ee0f24ea776f` | [`edison/q2-seed-alloys-and-data/`](edison/q2-seed-alloys-and-data/) |
| q3: critique of the first draft, with the scripts rerun | `ANALYSIS` | `53ab490c-74b7-4648-996a-f554d5087675` | [`edison/q3-plan-critique/`](edison/q3-plan-critique/) |

Edison's numbers are as it reported them from the cited papers. I haven't checked them against the
papers, so check a value against its source before it goes into a prior. q3 caught one wrong
attribution in the first draft (S2), which shows how easily that can happen. q3's answer links a
`review_evidence.zip` that stayed on Edison's side; its notebook is saved here instead.
