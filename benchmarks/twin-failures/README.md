# Failed vs. abandoned atomizer runs in a simulated year of the vertical lab (DAL #274)

Issue #274 asks how BOFN should treat a failed experiment, in Ax's terms. Sterling asked for that question in "the
full vertical lab vision from byu-vcl", as a two-campaign, year-long simulation. This benchmark runs it inside the
byu-vcl digital twin, [round 3](https://github.com/vertical-cloud-lab/byu-vcl/pull/394) (asynchronous acquisition,
physical capacity, interim readings), with the engine pinned at
[`f1606a9`](https://github.com/vertical-cloud-lab/byu-vcl/commit/f1606a93df64da25a99b168c198f5498f08469da). Two
campaigns run for one simulated year at the same time:
- aluminium for LPBF (FLAIME), with $120k;
- copper for DED (ONR YIP), with $60k.

They share the atomizer, its operators and the other instruments. Only the atomizer's failures and how the optimizer
handles them change between runs. Everything here is simulated: synthetic truths, simulated instruments, assumed
prices and schedules. The failure regimes are fitted to the lab's ten logged atomizer runs where the log allows and
assumed elsewhere; each assumption is listed below.

The method-level companion, on DAL's own aluminium and copper networks with eleven strategies and over a thousand
campaigns, is on [`claude/issue-274-20261126-0639`](https://github.com/vertical-cloud-lab/digital-alloy-lab/tree/claude/issue-274-20261126-0639)
(`benchmarks/bofn-failures/`). This one adds what a method-level benchmark can't show: days on a calendar, two
campaigns competing for one atomizer, failures that take the atomizer down for both, and a learning curve.

## Summary

7 seeds × 6 strategies × both campaigns × one simulated year, on the lab's own failure record (regime `lab`):
42 BOFN years with both campaigns, 13 to 19 CPU-minutes each, paired by seed. Plus 21 years of round 3's
heuristic, random and GP-BO for reference.

- **The primary endpoint showed no difference between strategies.** It was fixed at 07:45 UTC, when only seed 0 had
  run: days to the state of the art (T1), averaged over both campaigns. Against round 3's own handling every
  alternative was sooner on average: `drop` -11 d (Holm p 1.00), `abandon` -25 d (Holm p 1.00), `retry` -27 d (Holm p 1.00), `viability_x` -28 d (Holm p 1.00), `viability_node` -37 d (Holm p 1.00). None survives the correction, and every interval crosses zero.
  Aluminium reached T1 in about 3 to 5 months under every strategy. Copper reached it in 4 or 5 of 7 years.
- **Round 3's own handling (`bad_value`: a failed run counts as zero yield) did worst on aluminium.** This and the
  following bullets are exploratory: unadjusted, and not part of the endpoint fixed in advance.
  - Every alternative ended with a better best aluminium alloy, by +0.11 to +0.15 utility on average (`bad_value`
    0.605 ± 0.051). The bootstrap intervals all sit above zero, with paired p from 0.05 to 0.12.
  - Every alternative also reached T2 (halfway from the state of the art to the oracle's best, both campaigns
    averaged) 48 to 84 days sooner.
  - The mechanism shows in the spending. The zeros make the yield model pessimistic near every failure, so the
    policy turns cautious. It spent $92k of aluminium's $120k, against $117 to 120k for the others,
    and demonstrated 15 new aluminium alloys a year, against 34 to 38.
- **Among the five alternatives, nothing separates.**
  - `abandon` against `drop` (`ABANDONED` against `FAILED`): -0.006 (-0.026 to +0.014) on aluminium, -9 d (-28 to +9) to T2.
  - Rerunning once before giving up (`retry`, Xavier's "make sure it's the material") against `abandon`:
    +0.019 (-0.011 to +0.043, p 0.27) on aluminium. It had the highest mean (0.750 ± 0.014), at about 4.0 repeat failures
    a year.
  - The node-level viability model against Ax 1.3's on the design: -0.017 (-0.061 to +0.030), +19 d (-10 to +53) to T2. In this twin
    both see the cause of the input-driven failures, because the atomizer settings are part of the design vector.
- **Copper hardly moved:** -0.04 to -0.01 on its best alloy against `bad_value`, and every interval crosses zero. Its
  lots take three or more runs and rarely fail whole, so failure handling barely touches its decisions.
- **Copper pays for aluminium's failures anyway.**
  - 29 to 40 % of aluminium's runs failed, and 71 to 82 % of those failed from their inputs: cold
    melts from CALPHAD liquidus errors, and flooding.
  - Repairs after transient failures took the shared atomizer down 63 to 85 days a year.
  - Aluminium set off 4.0 to 5.3 repairs a year and copper 0.1 to 0.7, because aluminium pours about seven
    times as often.
  - Those repairs took 16 to 20 of copper's Friday and Saturday atomizer days a year.
- **The lab's record hurts most where nothing models a failure.** Round 3's GP-BO, which never sees a failed design
  again, ended at 0.25 on aluminium. Random ended at 0.36 and the heuristic at 0.60 (5 seeds each).
- **Not run** (section 7): the hidden region where abandoning a composition is right, and the value of the
  diagnosis. They are wired up and calibrated; neither fit in the job.

## 1. The setting

- **The lab:** the twin's `vertical_lab` facility (PR 318's design):
  - one AMAZEMET rePOWDER atomizer, with starts at 08:00, 10:30 and 13:00 on weekdays plus Saturday mornings. Its
    week is split as DAL #256 plans it: aluminium Monday to Thursday, copper Friday and Saturday;
  - in-house LPBF and DED, SEM, PIP, CubXL corrosion screening, tensile testing and immersion;
  - two mobile robots and a technician.
- **Run settings:** the 225 cm³ crucible, powder reuse on, and the stocked lab's day-0 inventory.
- **The engine and the budgets:** round 3's asynchronous engine, with every station, robot, person and fixture booked
  physically and actions admitted as their gating station frees up. Money goes out on round 3's spending plan: 15 % of
  the budget at day 0, rising to all of it at day 274.
- **The optimizer:** round 3's time-aware BOFN, `Net3` with expected improvement per bottleneck-hour, for both
  campaigns. Only its handling of a failed atomizer run changes.
- **What is scored:** the true utility of the best *new* alloy each campaign has demonstrated, and the days to two
  targets from round 2's oracle:
  - T1 matches the state of the art: 0.423 for aluminium (AlSi10Mg), 0.556 for copper (NAB);
  - T2 is halfway from there to the best design the oracle found: 0.639 and 0.657.

## 2. The lab's atomizer record, and the failure regimes

The twin's atomizer fails with probability
`0.06 + 0.55 / (1 + exp((superheat − 70) / 14)) + 0.15 / (1 + exp(−(pour − 340) / 25))` (`twin/physics.py`, plus
wear above 1300 °C for copper). The 0.06 is chance. The rest comes from the run's inputs: the superheat is set over
the liquidus the campaign *believes*, so a CALPHAD error makes a cold melt, and the pour pressure can flood the plate.
The twin records only `failed`. `failures.py` adds four things:
- a cause for each failed run: `transient`, Ax's `FAILED`, or `intrinsic`, Ax's `ABANDONED` with a viability label of 0;
- the lab's diagnosis of that cause, right 80 % of the time (assumed);
- the regimes below;
- a ledger of every run, which a policy sees only when the lot's results come back.

**The record** (DAL PR 286, [`atomizer-runs/runs.csv`](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/8320f13623c7961fcce12ee4d5d2033f4d8c9936/atomizer-runs/runs.csv), each run read for its cause):

| # | Date | Alloy | Outcome | Cause, as read from the log |
|---|---|---|---|---|
| 1 | Oct 2 | Al 4047 in a 6063 cup | failed | set-up: melt shot out too fast, plate too far away |
| 2 | Oct 6 | Al 6063 | failed | set-up: stream on the upper sonotrode, vibration started late |
| 3 | Oct 8 | Al rods | failed | **the settings**: too little amplitude for a carbon-fibre plate; the melt froze on the tip |
| 4 | Oct 21 | Al 4047 | failed | set-up: plate in the wrong place until corrected mid-pour |
| 5 | Oct 22 | Al 4047 | made powder | below target |
| 6 | Oct 27 | C63000 | made powder | about 91 % of the charge |
| 7 | Oct 28 | C63000 | failed | consumable: a plate on its second use never started atomizing |
| 8 | Nov 5 | C63000 | failed | equipment: the induction generator tripped mid-pour |
| 9 | Nov 10 | C63000 | made powder | about 75 % |
| 10 | Nov 13 | C63000 | failed | consumable: a plate on its second use; the hot shot burned the collection cup's seals and cracked its glass (#269); the atomizer was down for more than a week |

None of the seven failures is attributed to the alloy. The same 630 bronze made powder twice and failed three times.
One failure came from the settings, and six from set-up, consumables and equipment, all of which have since had a rule
added (plate gauge, new plate each run, cone shields).

| Regime | Transient failures per run | Input-caused | Damage |
|---|---|---|---|
| `twin` | 0.06 (round 3 as it is; the layer only labels causes, and a test checks that the year is unchanged run for run) | the twin's law | the twin's own breakdowns only |
| `lab` | a learning curve fitted to the record: `p(n) = 0.10 + 0.90 exp(−(n − 1)/τ)`, maximum likelihood τ = 9.6 runs (95 % profile interval 3.0 to 40.3; the 0.10 floor is assumed). The year starts at run 11, at 0.42, and both campaigns' runs count. | the twin's law | 1 transient failure in 6 damages the atomizer (Nov 13 of six), lognormal repair with a median of 14 days (σ = 0.5, assumed); no new powder is planned while it is down |
| `lab_region` | as `lab` | the twin's law, plus a hidden region where 90 % of runs fail (below) | as `lab` |

**The hidden region** (`lab_region`, a stress test, not a claim about these alloys): compositions that won't atomize,
which no CALPHAD node sees.
- **Aluminium:** Mg/4 + Li ≥ 0.30. Mg and Li are oxide formers, and their dross clogs the nozzle.
- **Copper:** Cr/0.7 + Nb/0.8 + Ti/0.5 ≥ 0.45. These refractory additions don't fully dissolve. NAB is left outside
  the region, since it atomized on Oct 27 and Nov 10.

`calibrate_region.py` placed the thresholds against the twin's oracle (500 random designs per campaign,
`results/region_calibration.json`). The aluminium region covers 46 % of the space and 28 % of its best 5 %; the copper
region 53 % and 32 %. The optimum therefore sits at the region's edge, which is the case where abandoning a
composition is right.

## 3. The strategies

All of them are round 3's time-aware BOFN; `strategies.py` changes only what it does after a failed atomizer run. A
*run* is one pour, and an *attempt* is one powder action: a lot, or a top-up of one. An attempt that made no powder
counts as failed.

| Strategy | Ax analogue | The failed run's data | The design afterwards | New designs weighted by |
|---|---|---|---|---|
| `bad_value` | none: "soft pushing" (Xavier, in #274) | 0 yield in the atomize node, as round 3 does | as round 3: aluminium never again; copper lots topped up again and again | P(yield > 3 %), as round 3 |
| `drop` | `FAILED` (Ax ≤ 1.2.3 also for missing metrics) | none | may come back, with no memory of the failure | P(yield > 3 %) on successes only |
| `abandon` | `ABANDONED` | none | pending for good: never retried, and new designs keep their distance | as `drop` |
| `retry` | none: Xavier's "make sure it's the material" | none | one rerun at the same settings, queued first and allowed the atomizer's next free slot within 3 days (dropped after 30 days, counted); a second failure abandons it | as `drop` |
| `viability_x` | `ABANDONED` + `AddExecutionViability` (Ax 1.3, opt-in) | a GP on 0/1 over the whole design, one label per attempt | pending for good | P(f(x) ≥ 0.8), once 3 attempts have failed (Ax's defaults) |
| `viability_node` | the node-level version proposed in `bofn-failed-vs-abandoned.md` §4 | a GP on 0/1 over the atomize node's inputs (composition, CALPHAD liquidus, atomizer settings), one label per run; runs diagnosed transient left out | diagnosed transient: back, as `FAILED`; diagnosed intrinsic: abandoned | P(f(x_node) ≥ 0.8), once 3 runs are labelled 0 |
| `viability_node_nodiag` | | as above, every failure labelled 0 | abandoned | as above |
| `oracle` | | as `viability_node`, with the true cause | as `viability_node` | as above |

The viability weight multiplies the acquisition value of a new design and of atomizing a screened copper blend. That is
the outcome-constraint form in which BoTorch carries Ax's `execution_viable ≥ 0.8`. The weight also picks the
atomizer settings: the best of 64 by the yield node's mean plus half a standard deviation, times the weight. The
companion's names map as follows:
- `bad_value` is closest to its `impute`, though `impute` records only input-caused failures, at the worst value seen;
- `viability_x` and `viability_node` are its `viab_x` and `viab_node`;
- its `partial` and `keep` have no counterpart here, because an atomizer failure leaves no upstream node with data to
  keep. CALPHAD always runs.

## 4. What changed in the twin, and what didn't

- **No new powder is planned while the atomizer is repaired** (`failures._wrap_gate`, the same for every policy).
  Round 3 admits an action if its gating station can take it within 2 h of queue wait. It measures that wait against
  an idle station, and an idle station also waits out a repair, so the wait looked short. Without the change, a
  two-week repair let powder actions queue up behind it. The twin's own 36-hour breakdowns are left as they are.
- **A queued rerun (`retry`) may book the atomizer's next free slot up to 3 days out**, where round 3 allows 2 hours.
  Round 3 checks each action's slot at the hour its own charge will be ready, and that hour depends on the alloy, so
  new designs kept taking the slots a top-ranked rerun needed. In a first version, 4 of 28 reruns ran in a year.
- **Two fixes in `strategies.py` that the first runs needed, both applied before the results below:**
  - round 3's BOFN, when it refreshes its new designs, keeps only candidates without a design id, so queued reruns
    vanished;
  - hiding or abandoning a lot didn't change the artifact count `Net3.propose` watches, so the candidate list waited for
    the next part to come back.

  Every strategy except `bad_value`, which neither change touches, was rerun from seed 0 on the fixed code.
- **Failures are drawn when a run is booked**, as the twin draws everything, and damage starts at the end of the
  failed run. Runs already booked inside a repair window still run. `overlap_h` in each run's result counts those
  hours, so the approximation stays visible.
- Unchanged: the spending plan, the materials and their lead times, the facility, the instruments, and the other
  stations' breakdowns.

## 5. Results: the lab's record (regime `lab`, 7 seeds)

![best new alloy against days](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-274-20261126-0642/benchmarks/twin-failures/figures/twinfail_lab_best_vs_days.png?raw=true)

![paired differences](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-274-20261126-0642/benchmarks/twin-failures/figures/twinfail_lab_paired.png?raw=true)

![where the atomizer's runs went](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-274-20261126-0642/benchmarks/twin-failures/figures/twinfail_lab_atomizer.png?raw=true)

| Strategy | n | Al best new | Al T1 hit, KM median day | Al T2 hit | Cu best new | Cu T1 hit, KM median day | Cu T2 hit | Al runs failed (inputs / transient) | Cu runs failed | atomizer down, d | repairs set off by Al / Cu | Cu atomizer days lost to Al's repairs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bad_value` | 7 | 0.605 ± 0.051 | 6/7, 148 | 4/7 | 0.619 ± 0.040 | 5/7, 260 | 4/7 | 151 of 372 (123 / 27) | 8 of 50 | 78 | 4.7 / 0.7 | 16 |
| `drop` | 7 | 0.738 ± 0.016 | 7/7, 141 | 7/7 | 0.587 ± 0.034 | 5/7, 267 | 2/7 | 129 of 361 (97 / 32) | 10 of 52 | 82 | 5.1 / 0.1 | 20 |
| `abandon` | 7 | 0.732 ± 0.015 | 7/7, 104 | 7/7 | 0.575 ± 0.038 | 5/7, 302 | 2/7 | 113 of 357 (83 / 30) | 10 of 52 | 63 | 4.1 / 0.4 | 16 |
| `retry` | 7 | 0.750 ± 0.014 | 7/7, 81 | 7/7 | 0.581 ± 0.035 | 5/7, 288 | 1/7 | 118 of 358 (88 / 30) | 10 of 50 | 85 | 4.7 / 0.4 | 20 |
| `viability_x` | 7 | 0.728 ± 0.012 | 7/7, 101 | 7/7 | 0.602 ± 0.054 | 4/7, 295 | 4/7 | 110 of 354 (79 / 31) | 11 of 52 | 83 | 5.3 / 0.4 | 20 |
| `viability_node` | 7 | 0.711 ± 0.024 | 7/7, 111 | 6/7 | 0.610 ± 0.048 | 4/7, 233 | 4/7 | 106 of 364 (75 / 31) | 10 of 48 | 69 | 4.0 / 0.6 | 16 |
| `heuristic` | 5 | 0.603 ± 0.055 | 5/5, 92 | 2/5 | 0.459 ± 0.127 | 3/5, 331 | 0/5 | 99 of 405 (64 / 36) | 11 of 59 | 80 | 5.2 / 0.6 | 17 |
| `random` | 5 | 0.358 ± 0.116 | 3/5, 195 | 1/5 | 0.295 ± 0.126 | 1/5, - | 0/5 | 155 of 410 (128 / 26) | 21 of 65 | 78 | 5.2 / 0.4 | 14 |
| `gpbo` | 5 | 0.253 ± 0.105 | 2/5, - | 0/5 | 0.564 ± 0.057 | 3/5, 348 | 1/5 | 155 of 384 (123 / 32) | 15 of 64 | 97 | 6.0 / 0.8 | 17 |

What each strategy spent and made in a year (means over seeds):

| Strategy | Al spent | Al new alloys demonstrated | Al designs atomized | Al designs given up after transient failures only | Al repeat failures from the inputs | Cu spent | Cu new alloys |
|---|---|---|---|---|---|---|---|
| `bad_value` | $92k | 14.9 | 186 | 1.1 | 0.0 | $61k | 6.4 |
| `drop` | $120k | 34.3 | 172 | 1.1 | 2.3 | $61k | 5.4 |
| `abandon` | $119k | 35.4 | 178 | 1.9 | 0.0 | $61k | 6.7 |
| `retry` | $120k | 38.4 | 166 | 0.7 | 4.0 | $61k | 6.4 |
| `viability_x` | $117k | 36.1 | 177 | 2.1 | 0.0 | $61k | 6.1 |
| `viability_node` | $120k | 36.4 | 182 | 2.1 | 0.3 | $60k | 6.1 |
| `heuristic` | $120k | 71.2 | 132 | 0.8 | 3.6 | $60k | 9.4 |
| `random` | $119k | 53.4 | 205 | 0.6 | 0.0 | $61k | 11.6 |
| `gpbo` | $108k | 19.2 | 192 | 2.0 | 0.0 | $60k | 9.6 |

Paired against `bad_value`, seed by seed: mean difference (95 % bootstrap interval) and p. Days are restricted means to the target, censored at day 365, so negative is sooner. The primary endpoint (days to T1, both campaigns) carries Holm's correction over its 5 comparisons; the other columns are exploratory, with unadjusted paired t-test p.

| Strategy | **Days to T1, both (primary)** | Days to T2, both | Al best new | Cu best new | Al days to T1 | Cu days to T1 | seeds better / worse on the primary |
|---|---|---|---|---|---|---|---|
| `drop` | -11 (-57 to +39), p 0.68, Holm 1.00 | -48 (-88 to +3), p 0.11 | +0.133 (+0.038 to +0.249), p 0.07 | -0.033 (-0.108 to +0.024), p 0.41 | -21 (-108 to +70), p 0.68 | -1 (-55 to +35), p 0.96 | 5 / 2 |
| `abandon` | -25 (-70 to +19), p 0.35, Holm 1.00 | -57 (-106 to -4), p 0.09 | +0.127 (+0.034 to +0.233), p 0.07 | -0.045 (-0.135 to +0.031), p 0.37 | -49 (-145 to +48), p 0.40 | -2 (-30 to +37), p 0.94 | 5 / 2 |
| `retry` | -27 (-91 to +48), p 0.51, Holm 1.00 | -63 (-128 to +22), p 0.18 | +0.145 (+0.048 to +0.257), p 0.05 | -0.038 (-0.137 to +0.057), p 0.51 | -71 (-173 to +31), p 0.26 | +16 (-46 to +74), p 0.64 | 5 / 2 |
| `viability_x` | -28 (-82 to +18), p 0.35, Holm 1.00 | -84 (-140 to -24), p 0.04 | +0.123 (+0.020 to +0.237), p 0.09 | -0.018 (-0.127 to +0.088), p 0.77 | -61 (-152 to +6), p 0.22 | +5 (-76 to +70), p 0.91 | 4 / 3 |
| `viability_node` | -37 (-109 to +24), p 0.36, Holm 1.00 | -65 (-135 to +18), p 0.18 | +0.106 (+0.003 to +0.211), p 0.12 | -0.009 (-0.103 to +0.089), p 0.87 | -61 (-155 to +12), p 0.25 | -13 (-95 to +65), p 0.78 | 3 / 4 |

Exploratory contrasts between strategies (a minus b, paired by seed, unadjusted t-test p):

| a − b | what it asks | Days to T1, both | Days to T2, both | Al best new | Cu best new |
|---|---|---|---|---|---|
| `viability_node` − `viability_x` | node-level against Ax 1.3's design-level viability | -8 (-28 to +9), p 0.44 | +19 (-10 to +53), p 0.32 | -0.017 (-0.061 to +0.030), p 0.52 | +0.009 (-0.000 to +0.025), p 0.33 |
| `viability_node` − `drop` | a failure model against none | -25 (-69 to +12), p 0.30 | -17 (-51 to +17), p 0.41 | -0.027 (-0.084 to +0.022), p 0.40 | +0.023 (-0.070 to +0.115), p 0.67 |
| `abandon` − `drop` | ABANDONED against FAILED, no failure model | -14 (-45 to +20), p 0.46 | -9 (-28 to +9), p 0.39 | -0.006 (-0.026 to +0.014), p 0.59 | -0.012 (-0.070 to +0.030), p 0.69 |
| `retry` − `abandon` | one rerun before giving up, against giving up at once | -2 (-35 to +38), p 0.92 | -6 (-31 to +30), p 0.76 | +0.019 (-0.011 to +0.043), p 0.27 | +0.007 (-0.095 to +0.093), p 0.90 |

**One year, run by run** (seed 0, `bad_value` against `viability_node`). Both re-runs reproduce their benchmark
years to the last digit. The shaded bands are repairs, during which neither campaign can atomize. In this seed,
aluminium's runs that failed from their inputs fell from 121 under `bad_value` to 86 under `viability_node`. Over
all seven seeds the averages are 123 and 75; `viability_x`, at 79, did about as well.

![anatomy of one simulated year](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-274-20261126-0642/benchmarks/twin-failures/figures/twinfail_timeline_lab_s0.png?raw=true)

**The cheap references** use round 3's own handling. The heuristic, random and GP-BO ran 5 seeds each in the `lab`
regime; their rows are in the tables above. The heuristic and random also ran 3 seeds each with the hidden region,
in the table below. The BOFN strategies didn't run with the hidden region, so these rows only show what it does to
policies that don't model failures.

#### Regime `lab_region`

| Strategy | n | Al best new | Al T1 hit, KM median day | Al T2 hit | Cu best new | Cu T1 hit, KM median day | Cu T2 hit | Al runs failed (inputs / transient) | Cu runs failed | atomizer down, d | repairs set off by Al / Cu | Cu atomizer days lost to Al's repairs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `heuristic` | 3 | 0.569 ± 0.066 | 3/3, 138 | 1/3 | 0.495 ± 0.103 | 1/3, - | 0/3 | 145 of 383 (120 / 25) | 12 of 60 | 139 | 7.3 / 1.3 | 17 |
| `random` | 3 | 0.240 ± 0.240 | 1/3, - | 1/3 | 0.143 ± 0.143 | 0/3, - | 0/3 | 258 of 417 (242 / 17) | 37 of 66 | 65 | 3.7 / 0.7 | 11 |

What each strategy spent and made in a year (means over seeds):

| Strategy | Al spent | Al new alloys demonstrated | Al designs atomized | Al designs given up after transient failures only | Al repeat failures from the inputs | Cu spent | Cu new alloys |
|---|---|---|---|---|---|---|---|
| `heuristic` | $119k | 44.3 | 122 | 0.3 | 7.0 | $60k | 7.7 |
| `random` | $119k | 32.0 | 209 | 0.7 | 0.0 | $59k | 9.3 |

## 6. What this means for the lab's ledger, and for Ax

- **Don't count a failed run as a bad value in a GP that also sets the policy's appetite.** In the twin that is round
  3's own handling. It made the aluminium campaign cautious: it left about a quarter of its money unspent and
  demonstrated fewer than half as many alloys as any alternative. Its best alloy ended 0.11 to 0.15 below theirs
  (exploratory). Xavier's caution in this thread, that
  arbitrary bad values "may push answers away poorly", is what happened here. Record the run in a ledger, and let
  a separate model decide what the failure says.
- **A rerun before giving up is cheap, and here it didn't hurt.** On the lab's record, six of seven failures had
  nothing to do with the alloy. Retrying once at the same settings cost about four repeat failures a year. It had
  the highest mean aluminium result of the six strategies, but seven seeds can't separate it from abandoning at once
  (+0.019, −0.011 to +0.043). As the learning curve flattens a rerun buys less, so revisit this when the transient
  rate is measured again.
- **Ax's statuses alone barely matter here.** `abandon` (`ABANDONED`) and `drop` (`FAILED`) ended level. The
  method-level companion found the same on DAL's networks.
- **A viability model on the node's own inputs did no better than Ax 1.3's on the design here.** The twin's
  input-caused failures depend on the atomizer settings and the liquidus error, and both models can learn the
  settings: the design vector includes them. The node model's case rests on what the design model can't see. That
  would be measured intermediates, data from purchased powder or other campaigns, and pKGFN's partial evaluations,
  none of which this benchmark has. The companion, on DAL's networks with a learnability check, found node-level
  viability ahead of `viab_x` on copper and level on aluminium at $100k.
- **The shared atomizer turns one campaign's failures into the other's delay.** Aluminium pours about seven times as
  many runs, so it sets off almost every repair, and each repair takes copper's Friday and Saturday slots with it.
  A lab that runs both campaigns should schedule (or price) aluminium's risky runs knowing that.
- **For the ledger** (`bofn-failed-vs-abandoned.md` §4, on the 11-20 branch and the companion's): keep one row per
  run with the settings, the outcome, the lab's diagnosis, and whether the diagnosis was checked by a rerun. The
  strategies above need nothing else.

## 7. Not run, and what would settle the open questions

- **The hidden region (`lab_region`), where abandoning a composition is right.** It is calibrated
  (`results/region_calibration.json`) and wired up, but there was no room for it in the job: 15 BOFN years, about an
  hour on 4 cores. It is the experiment most likely to change a recommendation above.
- **The value of the diagnosis** (`diag`: viability node with no diagnosis, and with the true cause). That is 8 years.
- **More seeds.** Seven per strategy leaves most paired intervals wide. Twelve would narrow them by about a third.
- **GP-BO with Ax's statuses.** That is the closest thing to Ax out of the box. It appears here only with round 3's
  own handling, as a reference.
- **Failures beyond the atomizer:** lost tensile tests (PR 288: one in five), a build that fails on the plate, a
  coupon lost in immersion.
- **A slower learning curve** (`lab_slow`, τ = 40 runs, the upper end of the fit's interval), and the twin's own law
  (`twin`), are defined in `failures.py` and not run.

All of these run with `bench.py run region diag twin` once the job has the hours. Its runs go seed by seed, so a cut
run still leaves every strategy on the same seeds.

## Limits

- **All simulated.** The truths, the instruments and the prices are the twin's. Ten logged runs fix the learning
  curve's time constant only loosely (3 to 40 runs). The floor of 0.10, the damage probability (one event), the
  repair time and the diagnosis accuracy are assumptions.
- **Seeds:** 7 per strategy, paired by seed. A BOFN year with both campaigns took 13 to 19 minutes with four on the
  runner, and the job has six hours. Gaps under about 0.05 in utility, or 30 days, mean little at this count. The
  primary endpoint carries a correction for the number of comparisons; everything else is exploratory.
- **Seeds pair the world, not the draws.** A seed fixes the truth, the market and the twin's own breakdowns. Once
  strategies decide differently they draw different failures (the companion instead draws them per stage and
  attempt, so every strategy meets the same faults).
- **Atomizer only.** Prints, deposits, tensile bars and immersion coupons can fail in the lab too: PR 288 lost one
  tensile test in five. Here they fail only as the twin already has them, as measured outcomes such as low density,
  never as lost runs.
- **One optimizer.** Ax's own GP-BO isn't run with the Ax strategies. Its round-3 counterpart, GP-BO with a kriging
  believer, appears only as a reference line, with round 3's own handling.
- **Compute:** a BOFN year with both campaigns takes about 9.5 CPU-minutes, and this run had one 4-core runner. The
  lab's camera Pis have been off the tailnet since Nov 9 and 17. The CubXL Pi (1 GB, running the deck camera) is too
  small for a 0.6 GB BOFN worker.

## Files and how to run

| File | What it is |
|---|---|
| `get_twin.sh` | fetches the twin at the pinned commit (sparse: `vertical-lab/twin/` and the oracle's targets) |
| `failures.py` | the record, the learning-curve fit, the regimes, causes and diagnosis, damage and the repair gate, the ledger |
| `strategies.py` | the eight strategies on round 3's `Net3` |
| `bench.py` | experiments and the runner, seed by seed (`results/<experiment>.jsonl`, one line per simulated year) |
| `analyze.py`, `figures.py` | statistics (paired by seed: bootstrap intervals, paired t-tests, exact sign-flip p-values, Holm on the primary endpoint) and figures |
| `timeline.py` | one year run by run, every atomizer booking and its outcome, for the timeline figure |
| `calibrate_region.py` | places the hidden region against the twin's oracle |
| `test_twin_failures.py` | 17 checks; among them, the `twin` regime reproduces round 3 run for run |

```bash
bash get_twin.sh                                    # -> /tmp/byu-vcl/vertical-lab
python -m venv /tmp/venv && /tmp/venv/bin/pip install numpy scipy scikit-learn scikit-image matplotlib pillow pytest botorch
export TWIN_DIR=/tmp/byu-vcl/vertical-lab
/tmp/venv/bin/python -m pytest -q test_twin_failures.py
TWIN_WORKERS=4 /tmp/venv/bin/python bench.py run main base_lite      # about 3.5 h on 4 cores
TWIN_WORKERS=4 /tmp/venv/bin/python bench.py run region diag          # not run here (section 7)
TWIN_WORKERS=2 /tmp/venv/bin/python timeline.py run 0 lab bad_value viability_node && /tmp/venv/bin/python timeline.py fig 0 lab bad_value viability_node
/tmp/venv/bin/python analyze.py --figs
```
