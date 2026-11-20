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

Edison Scientific was the rubber duck: two `LITERATURE_HIGH` reviews and a critique of this
draft. They're in [`edison/`](edison/).

**Status:** this is a plan. Nothing here has been run on a real sample. The compositions are
proposals. They still need the CALPHAD screen, the design-space freeze, and a check of what is
actually on the shelf.

## Short answers

**On 3 + 3 + 3 with 25 left:** keep the three-way mix, but use about 6–7 seeds rather than 9. Give
the runs this frees up to the optimizer.

- **Edison's verdict on 9 seeds is "slightly too many".** Nine seeds are 36 % of the 25 runs.
  Bossek et al. (2020, [10.1145/3377930.3390155](https://doi.org/10.1145/3377930.3390155)) found
  that an initial design of about 30 % of the budget did best on their benchmark suite. Edison
  suggests 3 baselines, 2 agent picks, 2 space-filling points, 14 optimizer runs and 4 finalist
  runs ([q1](edison/q1-seeding-strategy/artifact-00.md)).
- **A toy simulation agrees on the direction** ([below](#how-many-seeds-a-toy-check)). Across 60
  paired problem instances, 2 baselines + 3 agent + 1 space-filling beat 3 + 3 + 3 by
  0.043 ± 0.014 in the best value found. It beat the best baseline 75 % of the time, against
  55 % for 3 + 3 + 3. 3 + 3 + 3 did worst of all the optimizer splits when the agent picks only
  pointed back at the known alloy family. That is the circularity risk Edison also flags.
- **Don't add a third baseline run.** The 6063 runs (A1–A5) and commercial AlSi10Mg powder at P1
  are baselines that cost no design run. D1-r stays: it measures the benchmark's own spread
  ([#256](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#the-36-al-runs)).

**In the schedule's terms** ([table](#a-proposed-seed-set)):

- D1 and D2 are the baselines.
- S1–S2 are agent picks, with different strengthening mechanisms.
- S3–S4 are space-filling picks from [`seed_design.py`](seed_design.py), made after the CALPHAD
  screen trims the candidate pool.
- B30 stays a dosing check. B15 should check the element the agent picks depend on (Mn, or Zr)
  rather than Si a second time.
- If the flex slots X1–X3 (Dec 14–16) aren't needed to redo failed runs, use them as early
  optimizer picks, not as more seeds.

**What matters more than the split:**

1. **The optimizer picks R1 (Dec 18) and R2 (Jan 8) before any new composition has strength
   data.** Seed tensile bars print at P3 (Jan 12–13). Until then, the strength nodes run on
   priors. So the literature data and strength models that go into those priors decide the first
   six optimizer runs ([pseudo-data](#literature-and-fantasy-data)).
2. **Most of the literature's best Sc-free seeds need Zr, Fe, Ce or Cu.** None of these is on
   the Nov 13 list in [#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6842840090)
   (Mn, Cr, Zn, Sn, Mg, Sc, Er, Ti from ESPI; Si, Fe, Ni and Cu were never ordered). The
   Scalmalloy-type benchmark D2 needs Zr as well. Check whether Zr is coming. If not, order it as
   an Al–Zr master alloy before the S runs (Dec 7–10).
3. **The design box on [PR #72](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/72)
   excludes several of the best-documented Sc-free LPBF alloys:** Al–10Ce (Ce cap 6 wt%), the
   Al–Fe eutectics (Fe cap 0.5 wt%), and Addalloy-type Al–4.5Mg–1.5Zr (Zr cap 1 wt%). Its
   Mg + Si ≤ 6 wt% joint cap even excludes AlSi10Mg. Settle these at the design-space freeze
   (G0, today).
4. **Settle the mineral-burden metric before picking seeds.** Of the 15 palette elements, only
   Fe, Si and Cu are absent from the USGS 2022 critical minerals list. By a plain wt% count of
   listed elements, Al–4Mn–0.5Ti–0.5Zr (5 wt%) is only a little leaner than Scalmalloy (about
   6 wt%, counting Mg). It wins clearly only if the metric weights Sc's supply risk well above
   Mn's. Fe- and
   Si-based strengthening is where "stronger and leaner" is easiest to show.

**Space-filling:** use the integrated-variance pick (`imse`) around the points already chosen.
Maximin pushes every point into an extreme corner. Sobol with an exclusion radius rarely
excludes anything with this few existing points. In 7-D, three points cover little whatever the
method, so space-fill in a reduced space: CALPHAD descriptors, which are what the downstream
nodes see ([details](#space-filling-around-the-points-we-already-have)).

**"Fantasy" data:** call it pseudo-data, keep it in its own source, and never overwrite it in
place. It isn't BoTorch's `fantasize`
([#104](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/104)).
[Below](#literature-and-fantasy-data).

**The pre-registered AI benchmark:** every policy has to start from the same seed set. If only
the AI policy gets the agent picks, the "acceleration factor" measures a warm start, not the
optimizer. Edison q1, pitfall P9. [Below](#making-the-seeds-count-for-the-paper).

## What the 25 experiments are

The [#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#the-36-al-runs)
has 36 Al atomizer runs. Five are the 6063 baseline repeats (A1–A5) and six are flex slots
(X1–X6). That leaves 25 runs whose composition someone has to choose:

| Block | Runs | When | Role |
|---|---|---|---|
| D benchmarks | D1 (AlSi10Mg-type), D2 (Scalmalloy-type), D1-r (repeat) | Nov 30, Dec 2, Feb 8 | baseline seeds |
| B dosing checks | B30 (Si ≈ 3.9 wt%), B15 (Si ≈ 2.1 wt%) | Dec 1, Dec 3 | known-composition seeds on the Al–Si line |
| S CALPHAD seeds | S1–S4 | Dec 7–10 | agent-chosen seeds |
| R optimizer rounds | R1–R4, 3 each | Jan 5 – Feb 3 | optimizer |
| F finalists | F1 ×2, F2 ×2 | Jan 25–28 | repeats of optimizer picks |

The schedule already spends 8 runs on seeds before the optimizer's first batch: D1, D2, B30, B15
and S1–S4. D1-r comes late. The flex slots X1–X3 (Dec 14–16) also come before the first batch is
picked on Dec 18. Following Edison (q1, P10), the 6063 repeats and dosing checks count once for
coverage, since each is one composition, but every run counts toward estimating noise.

When strength data arrive matters more than any of this. P2 (Dec 16–17) prints only single tracks
of the S runs. Their cubes and tensile bars come at P3 (Jan 12–13), with tensile tests Jan 19–22.
So when R1 (Dec 18) and R2 (Jan 8) are picked, the only strength data are commercial AlSi10Mg from
P1 and wrought 6063.

## A proposed seed set

| Slot | Strategy | Composition (wt%) | Why | Needs | In the PR #72 box? |
|---|---|---|---|---|---|
| A1–A5 | baseline (free) | 6063 bar | Run-to-run noise; the dilute end | on hand | yes |
| P1 | baseline (free) | commercial AlSi10Mg powder | Print window, density, tensile and corrosion baselines with no atomizer run | on hand | — |
| D1 | baseline | Al–10Si–0.35Mg | The alloy to beat. As-built YS ≈ 250–350 MPa ([q2](edison/q2-seed-alloys-and-data/artifact-00.md)) | 4047 + Mg | Mg + Si ≤ 6 says no; drop that cap |
| D2 | baseline | Al–4.5Mg–0.7Sc–0.3Zr(–0.5Mn) | The Sc reference. YS 256–278 MPa as-built, 456–469 MPa direct-aged ([10.3390/cryst15010025](https://doi.org/10.3390/cryst15010025)) | Sc on hand; **Zr** | yes |
| B30 | dosing check | 30 % 4047 in 6063 cups, Si ≈ 3.9 | Does measured Si follow the charge? | on hand | yes |
| B15 | dosing check, changed | Al + the Mn (or Zr) the S picks use, at a known level | Check that the element the agent picks depend on dissolves. Elemental Si only dissolved 29–44 % in 2–3.5 min at 738 °C ([#111](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/111)) | Mn on hand | yes |
| S1 | agent | **Al–4Mn–0.5Ti–0.5Zr** (Mair-type) | Sc-free. Mn supersaturation plus L1₂ Al₃(Ti,Zr) nucleants. Reported YS 284, UTS 320 MPa, 16.9 % elongation as-built, crack-free with no preheat at 380 W and 1900 mm/s ([10.1016/j.jallcom.2021.163156](https://doi.org/10.1016/j.jallcom.2021.163156)). A different mechanism from D1 and D2 | Mn, Ti on hand; **Zr** | yes |
| S2 | agent | **an Fe-based eutectic**, e.g. Al–(3–5)Fe–1Mg–(0.5–0.7)Zr. If Fe stays capped at 0.5 wt%: **Al–10Ce** if Ce is ordered | Fe is cheap and not on the critical list. Reported YS 376, UTS 406 MPa, 11 % elongation after 400 °C/4 h ([10.1080/17452759.2025.2516663](https://doi.org/10.1080/17452759.2025.2516663)). Al–10Ce is printable and stable but weaker (YS ≈ 222 MPa, [10.1016/j.addma.2022.102959](https://doi.org/10.1016/j.addma.2022.102959)) | **Fe**, **Zr** (or **Ce**) | no (Fe or Ce cap) |
| S3, S4 | space-filling | from `seed_design.py --method imse` after the CALPHAD screen | Cover what D1, D2, S1 and S2 leave out. Today's picks from the on-hand elements are below | depends | yes |
| X1–X3 | flex | redo failed runs; otherwise early optimizer picks | — | — | — |

The rest of Edison's shortlist ([q2 table](edison/q2-seed-alloys-and-data/artifact-00.md)), in case
the feedstock or the freeze rules out S1 or S2:

- **Al–4Mn–1.3Mg–0.3Zr:** 99.6 % dense and crack-free. Hardness study only, no tensile data.
- **Al–Fe–Cr quasicrystal alloy:** YS 395 MPa as-built, but only 4 % elongation.
- **Addalloy-type Al–4.5Mg–1.5Zr:** YS ≈ 315 MPa. Over the Zr cap, and Mg evaporates.
- **Low-Sc Al–4.5Mg–0.3Sc–0.4Zr:** right on the #255 goal, but it sits next to D2. Leave the Sc
  axis to the optimizer: D2 and the Sc-free picks bracket it.
- **A20X-type Al–Cu–Ag–Mg–Ti–TiB₂:** needs Cu and Ag, and Ag isn't in the palette.

**With only the elements on hand** (Mn, Cr, Mg, Ti, Er, Zn, plus Si from 4047), the agent picks
fall back to Zr-free cousins such as Al–Mn–Cr or Al–Mn–Ti. They have weaker literature support,
because Zr is what suppresses cracking in most of these alloys. That is the case for getting Zr
in before Dec 7.

## Seeds for every node, not just compositions

BOFN keeps one GP per node, and each needs its own starting data. Edison found BOFN and pKGFN
papers that start from full-network evaluations (Astudillo and Frazier 2021; Buathong et al.
2023). Node-level initial designs in each node's own input space have also been published
(Kudva et al. 2026, MOBONS). The newer pKGFN formulation drops the rule that upstream nodes must
be evaluated first, which allows downstream data from other sources (Buathong and Frazier 2025)
([q1 §4](edison/q1-seeding-strategy/answer.md)). Most of that node-level data needs no atomizer
run.

| Node | Inputs → outputs | Seeds that cost no atomizer run | Seeds from atomizer runs | When |
|---|---|---|---|---|
| CALPHAD descriptors | composition → liquidus, solidus, freezing range, Scheil cracking indices (Kou, CSC), phase fractions | A cheap, known function. Compute thousands of compositions with pycalphad now and Thermo-Calc once licensed ([#141](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/141)) | — | W1–W3 |
| Mineral burden | composition → weighted critical-mineral content | Analytic; freeze the weights first | — | G0 |
| Dosing and composition fidelity | charge recipe → measured composition (EDS, ICP-OES) | 6063 and 4047 as received | B30, B15, D1, D2, then every run | Dec 1–3 |
| Atomization | measured composition or its descriptors, superheat, amplitude → yield in cut, D10/D50/D90, sphericity, oxygen | Earlier runs (Oct 2, 6 and 8, and the 4047 runs in [#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159)), tagged with their settings. Lang's relation as a prior mean for size, ± 20–30 % (q2) | A1–A5 (noise), then every run | from Nov 17 |
| Powder characterization (SEM/EDS) | powder → size and shape, satellites, homogeneity | Commercial AlSi10Mg 15–45 µm; the analysis pipeline from [#225](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/225) | Every run, at the Thursday session | weekly |
| Print parameters (tracks, cubes) | powder descriptors + power, speed, hatch, layer → melt-pool depth and width, mode, density, cracks | See the three sources below this table | In-house 6063 and D1 at P2; S-run tracks at P2 | P1 Dec 2–3, P2 Dec 16–17 |
| Hardness (the fast strength screen) | printed material, heat treatment → HV | P1 AlSi10Mg cubes, wrought 6063, published HV for the benchmarks | D1 and the S runs, from P2 and P3 | from Dec 11 |
| Tensile | printed material → yield strength, UTS, elongation | P1 AlSi10Mg bars. Literature values for the benchmarks and Sc-free alloys ([q2 table](edison/q2-seed-alloys-and-data/artifact-00.md)). Strengthening models ([q2](edison/q2-seed-alloys-and-data/artifact-02.md)), e.g. about 104 MPa from 3.7 wt% Mn kept in solid solution | Seeds from P3, then the finalists | Dec 14–16, Jan 19–22, Feb 9–12 |
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
  `seed_design.py --candidates screen.csv --features ...`.

## Space-filling around the points we already have

[`seed_design.py`](seed_design.py) adds space-filling points around everything in
[`seeds.csv`](seeds.csv): 6063, D1, D2, B30 and B15. Add the agent picks there.

**The space.** It is the box a GP with `Normalize` sees: each element's wt% divided by its upper
bound. On top of that, each element one alloy has and the other doesn't adds 0.5 to the distance,
so different element sets count as further apart. Edison flagged plain Euclidean distance for
sparse compositions (q1, P5).

**The candidates:**

- The bounds are the finalized ones on [PR #72](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/72):
  Al ≥ 85 wt%, a cap per element, a 0.10 wt% floor for any element that is switched on, and its
  joint caps except Mg + Si.
- Each candidate has one to three additions, drawn from the elements on hand
  ([#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146)): Mn, Cr, Mg, Ti, Er
  and Zn, plus Si through 4047.
- Each has at least 3 wt% of additions in all. 6063 has about 1, D2 about 6 and AlSi10Mg about 10.

**The four methods:**

| Method | What it does |
|---|---|
| `sobol` | First feasible points of a scrambled Sobol sequence, sampled face by face on the sparse simplex. Ignores the existing points |
| `sobol-exclusion` | Walks the same sequence and skips points within a radius of an existing or picked point (the heuristic in #275) |
| `maximin` | Greedy maximin (Kennard–Stone augmentation, Edison's recommendation): each pick is the candidate farthest from everything so far |
| `imse` | Greedy integrated-variance reduction: each pick most lowers the average variance of a GP over the whole feasible pool. Before any outcome is measured, that variance depends only on where the points are and on an assumed length scale (0.5) |

Three new points, averaged over 10 scrambles ([`results/space_filling_compare.csv`](results/space_filling_compare.csv)):

| Method | Nearest existing point ↑ | Nearest pair of new points ↑ | Fill distance ↓ | Mean distance to nearest point ↓ | Mean GP variance ↓ |
|---|---|---|---|---|---|
| (existing points only) | | | 1.93 | 1.20 | 0.966 |
| `sobol` | 1.14 | 1.21 | 1.81 | 1.03 | 0.928 |
| `sobol-exclusion` | 1.14 | 1.21 | 1.81 | 1.03 | 0.928 |
| `maximin` | 1.78 | 2.10 | 1.72 | 1.11 | 0.955 |
| `imse` | 0.91 | 1.15 | 1.76 | **0.96** | **0.895** |

The picks for seed 0 ([`results/`](results/)):

| Method | SF1 (wt%) | SF2 (wt%) | SF3 (wt%) |
|---|---|---|---|
| `sobol`, `sobol-exclusion` | Al–2.72Cr–0.31Ti | Al–0.86Mn–2.12Cr–0.30Er | Al–4.57Mg–0.47Ti |
| `maximin` | Al–3.00Cr–0.50Er–7.45Zn | Al–4.44Mn–0.50Ti–7.06Zn | Al–4.86Mg–0.48Ti–0.45Er |
| `imse` | Al–3.22Mn–1.45Cr | Al–7.63Si–0.28Er | Al–3.41Si–4.91Zn |

What this shows:

- **Three points don't fill a 7-D space, whichever method picks them.** The best method lowers the
  mean GP variance from 0.97 to 0.90. The worst-covered composition stays almost as far from any
  experiment as before. In a reduced space, the same three runs cover much more: CALPHAD
  descriptors, or one or two sub-system families.
- **Maximin sends every point to a corner.** Al–3Cr–0.5Er–7.5Zn and Al–4.4Mn–0.5Ti–7.1Zn sit on
  several caps at once. They are the hardest of these alloys to melt, dose and print. They also
  cover the space worse on average than plain Sobol does. Maximin designs are known to hug the
  boundary. Edison recommended maximin; this is where I disagree with it.
- **Exclusion rarely bites with this few existing points.** With five points in 7-D, the first
  Sobol points are already well away from all of them, so `sobol` and `sobol-exclusion` pick the
  same alloys. Exclusion starts to matter once the existing set is large: literature points, or a
  dense CALPHAD screen.
- **`imse` covers best on average, and its picks are moderate alloys.** Al–3.2Mn–1.5Cr is a Zr-free
  cousin of the Al–Mn–Cr–Zr focus system. Use `imse`, but check its picks against the CALPHAD
  liquidus and cracking screen before dosing. Edison's objection to IMSE is that it needs a fitted
  GP. In fact it needs only kernel hyperparameters, but the length scale is a real choice. Rerun
  it with `--ell` set from the GP fitted to the A, B and D data once those exist.

## How many seeds: a toy check

[`budget_split_sim.py`](budget_split_sim.py) is a flat-GP toy, not a model of the campaign:

- **The space.** A 6-D unit box, where the response depends mostly on 3 hidden dimensions.
- **The response.** A "known family" bump of height 0.7, where the baselines sit (good, not
  best). A better bump of height 1.0 somewhere else, and a decoy.
- **The seeds.** The agent picks are drawn around the better bump ("agent right") or around the
  known family ("agent wrong"). One free weak point stands in for 6063.
- **The optimizer.** The remaining runs go to batches of 3, picked by qLogEI.
- **The runs.** 30 problem instances per scenario. Every split sees the same instances, so the
  differences are paired.

| Split (baselines + agent + space-filling) | Seeds | Best of 25, agent right | Best of 25, agent wrong | Paired difference vs 3 + 3 + 3, both scenarios | P(beat best baseline by 0.05) |
|---|---|---|---|---|---|
| 3 + 3 + 3 (proposed) | 9 | 0.935 | 0.822 | — | 0.55 |
| 2 + 2 + 2 | 6 | 0.960 | 0.864 | +0.034 ± 0.014 | 0.72 |
| **2 + 3 + 1** | 6 | 0.962 | 0.880 | **+0.043 ± 0.014** | **0.75** |
| 2 + 4 + 0 | 6 | **0.970** | 0.856 | +0.035 ± 0.017 | 0.70 |
| 2 + 0 + 4 | 6 | 0.869 | **0.892** | +0.003 ± 0.028 | 0.60 |
| 2 + 0 + 1 | 3 | 0.860 | 0.854 | −0.021 ± 0.020 | 0.57 |
| 3 + 3 + 6 | 12 | 0.952 | 0.845 | +0.020 ± 0.014 | 0.65 |
| 25 Sobol, no optimizer | 25 | 0.767 | 0.767 | −0.111 ± 0.030 | 0.43 |

The global maximum is about 1.0. ± is one standard error. Full results are in
[`results/budget_split/`](results/budget_split/).

What it says, within its assumptions:

- **About six seeds beat nine or twelve.** Three seeds (2 + 0 + 1) did a little worse than six,
  and spending all 25 runs on Sobol did worst.
- **Agent picks are worth a lot when they know something** (+0.10 when they're right) **and cost
  little when they don't.** They hurt mainly when they crowd the known family. 3 + 3 + 3 spends
  six of nine seeds there in the "wrong" case: three baselines and three agent picks.
- **2 + 3 + 1 was the most robust split.** It came near the top in both scenarios. 2 + 4 + 0 bets
  on the agent being right, and 2 + 0 + 4 bets on it being wrong.

What the toy leaves out, and why the real answer may need more seeds:

- In the toy the optimizer sees its result at once. In the campaign, strength comes back about
  four to six weeks after a run.
- Failed runs ([#274](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/274)).
- The function-network structure.
- A 15-element space.

So treat it as evidence on the direction, not on the exact number. It can be rerun on the 5-node
synthetic network in [#265](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/265)
once that exists.

## Literature and "fantasy" data

#275's "fantasy modelling" is synthetic or literature data that stands in until real data
exist. BoTorch's `fantasize` is something else: it conditions a model on sampled outcomes at
pending points, so that a batch doesn't pick the same point twice. The second meaning is what
[#104](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/104) is about, and what
pKGFN needs. To keep them apart, this folder calls the first kind **pseudo-data**. Edison calls
running the whole loop on it a "synthetic digital-twin dry run" (q1, P7).

How to use pseudo-data without fooling the model (Edison q1 §5, P8):

- **Give every row a `source`** (in-house, literature, database, model) and keep a separate noise
  level per source. Assuming one noise level for every source degrades multi-fidelity BO
  (Foumani et al. 2023).
- **Put it in through the model, not as if it were our own data.** Options:
  - a multi-task or multi-fidelity GP with the source as the task;
  - a prior mean from a physics model, with the GP learning the residual;
  - an RGPE-style ensemble, whose weight on the literature falls as our own data arrive.
- **Never overwrite a pseudo-data row with a real value.** Add the real row and let the source
  term take care of the rest. That keeps the replay honest, and it shows how far the priors were
  off.
- **Use it first for the dry run.** Run the whole loop on pseudo-data before Dec 18, so R1 isn't
  the first time the code sees a full network.

What each node can start from:

| Node | Pseudo-data source |
|---|---|
| Print parameters | Barrionuevo AlSi10Mg rows (local); NIST AM-Bench 2022 Al single tracks ([MDS2-2525](https://data.nist.gov/od/id/mds2-2525)); Eagar–Tsai with an absorptivity fitted to P1 tracks, accurate to about ± 20–30 % in conduction mode |
| Cracking | Scheil Kou index and CSC from CALPHAD, used as features or soft constraints |
| Strength | Literature tensile values (q2 table); solid-solution, Orowan and Hall–Petch terms, each about ± 15–25 % when retained solute and particle sizes are known |
| Atomization | Lang's relation, ± 20–30 % |

Taheri-Mousavi et al. (2024, [10.48550/arXiv.2406.17457](https://doi.org/10.48550/arXiv.2406.17457))
is the closest precedent. They used CALPHAD-derived descriptors and about 40 training
compositions with expected improvement to design an LPBF Al–Er–Zr–Ni alloy.

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

- **Use one common seed set for every policy:** random, expert design of experiments, standard
  BO and BOFN. That set is the baselines and the space-filling seeds.
- **Count the agent picks on purpose.** Either put them in the common set, or charge them to the
  AI policy's budget. Report the warm-start effect and the optimizer's effect separately.
- **Replay only on points that were actually measured.** Anything else needs a clearly labelled,
  cross-validated simulator, and causal acceleration claims should be avoided.

With about 20 compositions, the acceleration factor will rest on that simulator. Space-filling
seeds make the simulator less wrong away from the optimizer's path. That is one more reason to
keep one or two of them.

## Pitfalls

From Edison q1's table ([artifact-01](edison/q1-seeding-strategy/artifact-01.md)) and this work:

| Pitfall | Do instead |
|---|---|
| Nine seeds leave only 12 optimizer runs | About 6–7 seeds |
| A 10d rule would need 140–150 runs in 15-D | Shrink the space before atomizing: at most 3–4 additions, CALPHAD descriptors as GP inputs, sparse kernels |
| Agent picks cluster around Al–Si–Mg and Al–Mg–Sc–Zr | Two picks, with different mechanisms and element sets, chosen away from D1 and D2 |
| Sobol in the full 15-element simplex is almost never feasible | Sample face by face on the sparse simplex (as `seed_design.py` does) |
| Maximin picks extreme corners | `imse`, or maximin only after the CALPHAD screen trims the pool |
| Euclidean distance ignores element identity | Add an element-set term (`--set-weight`) |
| Composition-only space-filling leaves the downstream nodes cold | Seed each node from its own cheap sources; space-fill in descriptor and print-parameter space |
| Pseudo-data pooled with real data biases the model | A source column, per-source noise, multi-task or multi-fidelity; never overwrite rows |
| Seeds differ between the compared policies | One common seed set; report warm-start and optimizer effects separately |
| The seeds need elements we don't have | Check Zr, Fe and Ce now; B15 checks the element the S picks depend on |
| Failed runs dropped from the data | Record failures as outcomes ([#274](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/274)) |

## Files

| File | What |
|---|---|
| [`seeds.csv`](seeds.csv) | Points already chosen: 6063, D1, D2, B30, B15. Add the agent picks here, and replace nominal compositions with measured ones as they come in |
| [`seed_design.py`](seed_design.py) | Space-filling picks around `seeds.csv`, in composition space or, after the CALPHAD screen, in descriptor space |
| [`budget_split_sim.py`](budget_split_sim.py) | The toy simulation of seed and optimizer splits of 25 runs |
| [`results/`](results/) | Outputs of both scripts |
| [`edison/`](edison/) | The Edison queries, answers, artifacts and full trajectories, plus `edison_tasks.py`, which submits, waits for and fetches them |

```bash
pip install numpy scipy
python bofn-seeding/seed_design.py                       # 3 picks, imse
python bofn-seeding/seed_design.py --compare             # all four methods
python bofn-seeding/seed_design.py --elements Mn Cr Mg Si Er Ti Zn Zr   # once Zr is on the shelf
python bofn-seeding/seed_design.py --candidates screen.csv --features freezing_range kou_index l12_fraction

pip install torch botorch
python bofn-seeding/budget_split_sim.py --reps 30 --workers 4   # about 10 min on 4 cores
```

## Edison tasks

| Task | Job | ID | Folder |
|---|---|---|---|
| q1: rubber-duck the 3 + 3 + 3 plan | `LITERATURE_HIGH` | `2d0326f1-fc13-4a90-bcd0-6f92d885d5c8` | [`edison/q1-seeding-strategy/`](edison/q1-seeding-strategy/) |
| q2: seed alloys, datasets, cheap models | `LITERATURE_HIGH` | `33e883b7-532f-4792-b4b6-ee0f24ea776f` | [`edison/q2-seed-alloys-and-data/`](edison/q2-seed-alloys-and-data/) |

Edison's numbers are as it reported them from the cited papers. I haven't checked them against
the papers, so check a value against its source before it goes into a prior.
