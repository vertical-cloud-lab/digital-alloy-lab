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

The method-level companion, on DAL's own aluminium and copper networks with ten strategies and 1,356 campaigns, is
on [`claude/issue-274-20261126-0639`](https://github.com/vertical-cloud-lab/digital-alloy-lab/tree/claude/issue-274-20261126-0639)
(`benchmarks/bofn-failures/`). This one adds what a method-level benchmark can't show: days on a calendar, two
campaigns competing for one atomizer, failures that take the atomizer down for both, and a learning curve.

RESULTS_SUMMARY

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
| `retry` | none: Xavier's "make sure it's the material" | none | one rerun at the same settings, then abandoned | as `drop` |
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
- **Failures are drawn when a run is booked**, as the twin draws everything, and damage starts at the end of the
  failed run. Runs already booked inside a repair window still run. `overlap_h` in each run's result counts those
  hours, so the approximation stays visible.
- Unchanged: the spending plan, the materials and their lead times, the facility, the instruments, and the other
  stations' breakdowns.

RESULTS_SECTIONS

## Limits

- **All simulated.** The truths, the instruments and the prices are the twin's. Ten logged runs fix the learning
  curve's time constant only loosely (3 to 40 runs). The floor of 0.10, the damage probability (one event), the
  repair time and the diagnosis accuracy are assumptions.
- **Seeds:** 10 per strategy in the main experiment and 5 or 6 in the others. Gaps under about 0.05 in utility mean
  little at these counts. Every comparison is paired by seed and corrected for the number made.
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
| `analyze.py`, `figures.py` | statistics (paired by seed, bootstrap intervals, exact sign-flip p-values, Holm) and figures |
| `calibrate_region.py` | places the hidden region against the twin's oracle |
| `test_twin_failures.py` | 16 checks; among them, the `twin` regime reproduces round 3 run for run |

```bash
bash get_twin.sh                                    # -> /tmp/byu-vcl/vertical-lab
python -m venv /tmp/venv && /tmp/venv/bin/pip install numpy scipy scikit-learn scikit-image matplotlib pillow pytest botorch
export TWIN_DIR=/tmp/byu-vcl/vertical-lab
/tmp/venv/bin/python -m pytest -q test_twin_failures.py
TWIN_WORKERS=4 /tmp/venv/bin/python bench.py run main base region diag   # about 4 h on 4 cores
/tmp/venv/bin/python analyze.py --figs
```
