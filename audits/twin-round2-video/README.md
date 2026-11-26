# Audit of the twin round-2 video

**Video:** [A year of alloy discovery in an automated lab: a simulated benchmark](https://www.youtube.com/watch?v=Pz7hxqfODmE) (11:41).
**Source:** byu-vcl [PR 393](https://github.com/vertical-cloud-lab/byu-vcl/pull/393) at head [`357d149`][bv].
**Asked for in:** [issue 276](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/276#issuecomment-7180754041). Audited 2026-11-26.

YouTube blocks CI runners, so the video itself was not watched. The audit reads what it is built from: the frame code,
the data feed, the two summaries, the stored per-seed runs, the description and the contact sheet. The numbers legible on
the contact sheet match those sources.

## What to believe

The arithmetic is right and the video says it is a simulation. Its two headline factors are not a measure of what
automation does, and the cost figure on the takeaway card is chosen, per campaign, as the first basis on which the
automated lab comes out cheaper.

1. **Everything checked reproduces.** All 4 speed-ups, all 20 cost ratios, the 18 cost-per-alloy figures and the copper
   scores come out of the stored runs to the digits shown.
2. **Aluminium's "1.9× faster" is mostly feedstock on the shelf.** The automated lab starts with about a month of
   stock; the conventional lab orders each charge's metal when it needs it. With both ordering as they go, the factor
   is 1.16 (95 % interval 0.72 to 1.66).
3. **Copper's "3.7× faster" compares two different optimizers,** and its reference median is the last of six seeds
   that got there. With plain BOFN in both labs, the automated lab reached the copper target in 3 of 12 seeds. What
   does hold: in every comparison where both arms get there in at least half their seeds, the automated lab reaches
   the copper target sooner, by 1.4 to 3.8 times.
4. **The takeaway's "84 %" means two different things.** For aluminium it needs outside users to rent the idle
   instruments; for copper it leaves out equipment. With equipment included, the automated lab costs 2.0× (aluminium)
   and 1.15× (copper) as much to reach the target.
5. **"State of the art" is a low bar on this synthetic truth.** One random design in twelve beats it, and some of
   the seed alloys planned in issue 275 beat it on their first test.
6. **Against the conventional lab run the usual way** (a metallurgist's heuristic), aluminium is no faster
   (1.05, 0.69 to 2.25) at 2.6× the operating cost. Copper is 2.2× faster (1.76 to 2.63), and that holds up.
7. **The replay shows aluminium's luckiest seed:** it reaches the target on day 20; the median of the 12 seeds is day 116.
8. **Against this repo's records,** the twin's prices and powder sizes match. Its atomizer has a 6 % base chance of
   failing and runs 5 to 8 times a week in the two labs compared; the lab's log has 2 good runs in 10, at 1.7 a week.

## How it was checked

- **Recomputed independently.** [`recompute.py`](recompute.py) reads only `out/twin2/runs/*.jsonl` and
  `oracle.json` and imports none of the twin's code. Its output is [`recomputed.md`](recomputed.md).
- **Costs re-run with the twin's own model.** [`rerun_twin_costs.py`](rerun_twin_costs.py) calls `twin/econ.py` on the
  stored runs; output in [`rerun_twin_costs.txt`](rerun_twin_costs.txt). The cost bases other than cash need that
  model, so this part is a re-run, not an independent derivation.
- **Statistics.** Intervals are 95 % percentile bootstraps over seeds (20,000 resamples). Each comparison also has a
  two-sided permutation test that handles seeds which never reach the target (exact for 12 seeds against 12). The
  family for Holm's correction is the 13 comparisons the video and description state ([recomputed.md §5][R5]).
- **Real-world records** were read at pinned commits: the atomizer log on PR 286, issues 146, 159, 219, 250, 256 and
  275, the SEM, EDS and tensile data on PR 288, and the benchmarks on PRs 117 and 206.
- **Not done.** No simulation was re-run. The frame text was read from the code at `357d149`; the upload was built from
  `73b155f`, which this audit did not diff against it. Private quotes in the procurement threads are compared but
  not repeated here.

Words used below: *stocked* means feedstock bought and on the shelf at day 0; *lean* means each charge's metal is
ordered when needed. `bofn` is plain BOFN and `bofn_blend` adds blend screening for copper. *T1* is the video's
"state of the art" target and *T2* the harder one stored beside it (halfway to the best alloy the twin's search found).

## 1. The claims, most important first

Verdicts: **Holds**, **Reword** (the number is right, the wording claims more than it shows), **Not supported**,
**Open** (rests on an assumption no data here can check).

| # | Claim | Where | Verdict | Reason | Evidence |
|---|---|---|---|---|---|
| 1 | Aluminium (FLAIME): "reached the state-of-the-art target 1.9x faster" | Results, takeaway, description | **Reword** | Reproduces: 1.89 (1.07 to 3.39); 220 against 116 days; automated faster in 83 % of seed pairs; p = 0.0056, which is 0.050 after Holm, on the line. With one median rule for both arms it is 1.76 (0.97 to 3.62). The automated arm is stocked and the conventional arm is lean. With both lean: **1.16 (0.72 to 1.66), p = 0.59**; with the heuristic on both, 1.15 (0.60 to 2.11). In the first 365 days both labs reach the target in 12 and 11 of 12 seeds. | [§2][R2], [§5][R5], [§10][R10]; [`bench2.py` L46-L54][bench2]; [`campaign.py` L97-L105][stocked]; [notes L391-L393][n56] |
| 2 | Copper (ONR): "reached the state-of-the-art target 3.7x faster" | Results, takeaway, description | **Reword** | Reproduces: 3.73 (2.04 to unbounded). Three problems. (a) Different optimizers: `bofn_blend` in the automated lab, `bofn` in the conventional one. Plain `bofn` in the automated lab reached the target in 3 of 12 seeds and ended at 0.33. (b) The conventional arm got there in 6 of 12 seeds, so its "median" of 840 days is its last hit; one fewer and there is none. It is a lower bound. (c) The automated arm has 12 more stored seeds; with all 24 it reaches the target in 19 and the factor is 3.45 (1.77 to unbounded). The direction is solid: automated faster in 95 % of seed pairs, p < 0.0001, 12 of 12 against 1 of 12 in the first year. | [§2][R2], [§9][R9], [§10][R10]; [notes L318][n54]; [`bench2.py` L71][bench2b] |
| 3 | Takeaway card: "1.9× faster, 84 %" and "3.7× faster, 84 %" | Takeaway | **Reword** | The card shows, per campaign, the first cost basis on which the automated lab is cheaper. Aluminium's 84 % is operating cost *with outside users renting the idle hours* (0.47 to 1.42). Copper's 84 % is operating cost *without equipment and without outside users* (0 to 1.50). Both intervals include 100 %. Full cost with equipment is 200 % (114 to 357) and 115 % (0 to 205), in the card's smallest type. | [`data.py` L616-L630][pick]; [`figs_anim.py` L1063-L1080][take]; [rerun][RR] |
| 4 | The ten cost ratios (aluminium 63, 136, 200, 84, 114 %; copper 41, 84, 115, 42, 48 %) | Results, description | **Holds** as arithmetic; few differ from 100 % | All ten reproduce exactly. Intervals that exclude 100 %: aluminium full cost (costs more, 114 to 357); copper cash (0 to 74), copper shared operating (0 to 75) and shared full (0 to 85). The rest include 100 %. Of the two cash ratios tested, copper's survives Holm and aluminium's does not (p = 0.014, 0.12 after correction). See "What the cost includes" below. | [rerun][RR]; [§3][R3], [§5][R5] |
| 5 | "the automated lab reached state-of-the-art alloys" | Takeaway headline, results, description | **Reword** | The target is the score of AlSi10Mg (0.42) and C95800 (0.56) on the twin's synthetic truth. 8.2 % of random designs beat it in both spaces. From issue 275's seed alloys every policy, random included, reaches it on its first tests (median day 2 automated, day 52 to 73 on issue 256's schedule), because a dosing-check alloy outscores AlSi10Mg on this truth. Time to T1 measures how soon a lab tests its first dozen alloys. At T2 the aluminium factor is the same, 1.89 (1.05 to 4.18); copper is 7 of 12 automated seeds against 1 of 12 conventional in three years. | [`oracle.json` L62, L136][oracle]; [notes L410-L413][n57]; [§1][R1], [§7][R7] |
| 6 | "Against the conventional lab run with a metallurgist's heuristic instead: FLAIME 1.1x, ONR 2.2x faster ... there the automated lab costs more unless outside users share it" | Takeaway footer, description | **Holds** for copper; **Reword** for aluminium | Copper: 2.18 (1.76 to 2.63), p < 0.0001, survives Holm. Aluminium: 1.05 (0.69 to 2.25), p = 0.38, which is "no faster". The cost sentence is true for copper only (77 % shared operating, 64 to 98). Aluminium's estimates stay above 100 % even when shared: 163 % operating (68 to 253) and 216 % full (93 to 329). In the conventional lab the heuristic reaches T1 before BOFN in both campaigns (123 against 220 days; 490 against 840), so the headline's reference is the slower of the two. | [§2][R2], [§5][R5]; [rerun][RR] |
| 7 | "on copper, tiered CALPHAD screening finished ahead of BOFN with blend screening (0.69 against 0.67; with a hidden gamma-2 corrosion effect, 0.69 against 0.55)" | Description | **Holds**, understated | Reproduces (0.686, 0.674, 0.552). At 12 seeds the first gap is a tie (+0.012, −0.025 to +0.045, p = 0.52) and the second is not established (p = 0.10). The 24-seed result is the informative one and is not in the description: **0.68 against 0.58** (+0.096, 0.021 to 0.185, p = 0.021). Also missing: plain BOFN scored 0.33 on copper, level with random (0.35). | [§4][R4]; [notes L226-L229][n53] |
| 8 | "on aluminium a metallurgist's heuristic reaches the state of the art sooner, and BOFN's lead is in the final alloy" | Description | **Holds** | Heuristic 37 days against 116, faster in 76 % of seed pairs, p = 0.032 (0.20 after Holm: likely, not established). Final alloy 0.687 against 0.605, +0.082 (0.038 to 0.123), p = 0.0023, survives Holm. | [§2][R2], [§4][R4], [§5][R5] |
| 9 | The replayed year (seed 0) | Replay, 3:41 to 9:41 | **Reword** (label it) | Seed 0's aluminium campaign reaches T1 on day 20.3, the earliest of the 12 seeds (median 116.2, latest 231). Its copper campaign is typical (day 225.6, median 225.3). Final alloys rank 5th and 9th of 12. The live plots therefore show aluminium crossing the target about three months before the median seed. | [§6][R6]; [notes][nvid] |
| 10 | "Runs: 12 automated and 12 conventional twin-years"; "reached the target in 100 % of 12 automated and 50 % of 12 conventional twin-years" | Takeaway footer, results footnote | **Reword** | The conventional runs last three years with three years' money ($360k and $180k); the automated runs last one. On the same 365 days: aluminium 12 of 12 against 11 of 12; copper 12 of 12 against 1 of 12. With all 24 automated copper seeds it is 79 %, not 100 %. | [`bench2.py` L49][bench2]; [§9][R9], [§10][R10] |
| 11 | Cost per alloy tested: conventional $9.4k (no equipment) and $11.6k; automated $15.7k and $28.6k; automated at 60 % use $4.5k and $5.9k | Results | **Holds**; the 60 % bars are **Open** | All 18 figures reproduce. Carrying its own costs the automated lab costs 1.7× per alloy without equipment and 2.5× with it. The 60 % bars assume outside users. | [rerun][RR] |
| 12 | Utilization, and "the spare hours, offered to outside users" ($13.0M a year at capacity; $1.55M demand-limited) | Results | Utilization **holds**; revenue is **Open** | The campaigns use 5.8 % of the lab's equipment-weighted hours and 46 % of the atomizer's slots. "At capacity" is a ceiling: every station filled to 60 %. "Demand-limited" assumes 10 hours a week of paying work on every instrument. Nothing in this repo or byu-vcl records outside demand. | [`econ_summary.json`][econ] (`outside_work`, `utilization`) |
| 13 | "Real: ... Assumed: station times, fees and outside-facility delays. Simulated: ..." | Notes frame, description | **Holds**, incomplete | Prices match the procurement threads for every item checked. 76 % of the automated lab's $5.40M of equipment is priced from procurement records or list prices, 24 % is estimated. Missing from "Assumed": stock on the automated lab's shelf at day 0; the atomizer's failure rate and yield; 1.25 staff running the automated lab; three years for the conventional lab. "Every measurement, with noise": the simulators are not calibrated on the lab's measurements (section 2). | [`compose.py` L719-L733][notesf]; [rerun][RR]; section 2 |
| 14 | "against the same campaigns run the conventional way (partner facilities and core facilities)" | Description | **Reword** | The conventional lab is the proposals' planned lab, with the atomizer available 16 times a week. It is not how the lab works today (section 2). The twin has a model of today's schedule, `dal256`, which the video does not use. Against it, from common seeds, copper is 3.9× (3.2 to unbounded; 12 of 12 seeds against 6 of 12) and aluminium to T2 is 1.4× (0.8 to 3.8). | [notes L296-L299][n54]; [§2][R2], [§7][R7] |
| 15 | "The takeaway compares the vertical lab with BOFN against the conventional lab with the same BOFN (the lab's own contribution)" | `notes/twin_video.md` | **Not supported** | For copper the optimizers differ (row 2). For aluminium the optimizer is the same but stocking differs (row 1). | [`twin_video.md` L55-L56][nvid] |
| 16 | The acceleration factor: median days, Kaplan-Meier, percentile bootstrap, after Rohr et al. 2020 | `notes/twin_video.md`, "The figures we track" | **Holds** as a description, with four caveats | See "The acceleration-factor method" below. | [`accel.py` L58-L146][accel] |

### What holds up, plainly

- The pipeline is reproducible: one script, the stored runs, the same numbers.
- The automated lab reaches the copper target sooner than the conventional lab: 2.2× against the heuristic
  (survives correction), 3.6× with tiered screening in both labs (2.4 to 6.4, 24 seeds), and 1.9× with the heuristic in
  both labs and both ordering as they go (1.42 to 2.74).
- BOFN's final aluminium alloy is better than the heuristic's (survives correction).
- The description says where BOFN loses, and the results frame shows all five cost bases, including the unfavourable ones.
- The economics notes state Rohr et al.'s definition correctly (experiments, against random selection) and say the
  twin applies it to days and dollars.

### What the cost includes and leaves out

*Included*, per campaign, up to the day it reaches the target ([`econ.py` L785-L805][costc]): feedstock, consumables
and outside fees as spent; labour; service contracts; electricity and space; and, on the "full" bases, straight-line
depreciation of the equipment ($5.40M automated, $0.54M conventional) and of the floor space.

*Left out or favourable to the automated lab:*
- **Interest.** Depreciation is at a 0 % discount rate.
- **Hands.** The automated lab is staffed by one technician and a quarter of an engineer, and its in-house stations
  need no hands-on time ([`econ.py` L94-L99][staff], [L417-L457][hands]). Today the lab's steps are done by hand,
  and computer control of the atomizer is an open issue
  ([issue 151](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/151)).
- **Commissioning and downtime.** The real atomizer went from crates on site (June 11,
  [issue 142](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/142)) to its first training run
  (Sept 29, [PR 286's README][runsreadme]) in about 110 days.
- **Outside users,** on the "shared" bases: assumed demand.
- **Design and analysis time** is left out of both labs.

*Favourable to the conventional lab:* BYU instruments it uses carry no charge or subsidised rates, and its students
cost $27 an hour.

### The acceleration-factor method

- **What Rohr et al. define.** Their factor is a ratio of numbers of experiments, sequential learning against random
  selection, on a fixed dataset. A ratio of days between two facilities is a different quantity. The twin's
  `notes/twin_econ.md` gives the definition; `notes/twin_video.md` cites the paper without that qualifier.
- **Two median rules.** When every seed reaches the target the code takes the ordinary median, otherwise the
  Kaplan-Meier one, which for 12 seeds is the 6th value, not the mean of the 6th and 7th
  ([`accel.py` L85-L89][accel]). The bootstrap mixes the two. Aluminium's headline is 1.89 (1.07 to 3.39) by the
  code's rule and 1.76 (0.97 to 3.62) with Kaplan-Meier throughout.
- **Unequal horizons.** One year against three. It does no harm when the one-year arm always gets there, and it makes
  "heuristic in both labs, copper: 3.4×" unreliable (7 of 12 seeds in one year against 12 of 12 in three).
- **Choice among many.** `econ_summary.json` holds 6 comparisons × 2 campaigns × 7 quantities with no test and no
  correction. The video's comparison is chosen by rule ([`data.py` L601-L613][pick]), and the rule lands on the
  conventional lab's slower policy.

## 2. The twin's assumptions against this repo's records

| Assumption | In the twin | This repo's record | Reading |
|---|---|---|---|
| Feedstock prices | Day-0 prices per kg, taken from this repo's threads ([`supply.py` L59-L62][supply]) | Per-kg figures in issues [146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6353382512) and [250](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/250#issuecomment-6778615370) | **Match** for the 12 items checked (Mn, Cr, Zn, Sn, Ti, Sc, Er, Si, Al granules, 6063 rod, AlSi10Mg powder, bronze rod). AMAZEMET spares are assumed; none has been priced here. |
| Supplier lead times | Median 3 days for rod, 10 to 35 days for most additions, 28 for Sc and Er | Quoted: stock items at once, Sc and Er 3 to 5 weeks. Achieved on the one specialty order: decided [Sept 8](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6353384112); one part found never placed on [Oct 5](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6353384957) and still unordered on Nov 13; the other part due to ship about [Nov 13](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6842840090): at least 65 days. Rod orders: 2 to 5 days. | The quotes match. The twin models the supplier's delay and not the ordering delay, which was the larger part. Ordering as you go is slower in practice than in the twin, which makes stocking matter more, not less. |
| Stock at day 0 | Automated lab only: a month of everything but Sc and Er, bought and charged at day 0 ([`campaign.py` L97-L105][stocked]) | The lab orders as it goes | This, not automation, carries the aluminium headline (row 1). A conventional lab can keep a shelf too; the twin never ran one that does. |
| Atomizer starts | 16 slots a week in both labs. Used in seed 0: 7.7 a week automated, 5.4 conventional, 4.3 on issue 256's schedule | [10 runs in six weeks][runs], 1.7 a week, never two in a day. Planned: 3 to 4 a week ([issue 256][sched]) | Both of the twin's labs run the atomizer 3 to 5 times as often as the lab has. |
| Atomizer failures | 6 % base chance, more for a cold melt ([`physics.py` L58][phys]) | [2 good runs of 10][runs] (Oct 27, Nov 10), 1 partial, 7 with little or no powder | Far apart. The lab is still commissioning, but nothing logged supports 6 %. |
| Usable powder | 91 % of the charge on a good run ([`physics.py` L62][phys]) | 91 % is the best run. The only weighed balance, two runs pooled, is [52.4 %](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6517044293); Nov 10 was estimated at about 75 % | The twin's typical run is the lab's best run. |
| Aluminium powder | The FLAIME campaign atomizes about 160 aluminium lots a year (seed 0) | [Five aluminium runs][runs], all "little powder", none weighed; the only tensile data are on commercial powder ([PR 288][tens]) | The aluminium half of the benchmark has no logged run behind its atomizer step. |
| Plates and nozzles | Copper: one plate and one nozzle a run. Aluminium: a plate lasts 5 runs ([`atomize_yield.py` L77-L78][yieldm]) | Copper plates [single-use](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6509252104); nozzle replaced every run. Aluminium: "4 to 6 runs" is a planning figure | **Match** for copper. Aluminium is unmeasured. |
| Time per run | 2.5 h booked; conventional hands-on 3.5 h ([`econ.py` L420][hands]) | [Estimated][sched] 10 to 15 person-hours from charge to SEM; "nothing in the chain has been timed end to end" | The twin's atomizer step fits the estimate's 2.5 to 3.5 h. The whole chain's labour is an estimate on both sides. |
| Powder size | About twice Lang's formula: about 100 µm for bronze ([`physics.py` L7-L8][physd]) | [Volume D50 103.7 µm][prov] (5,937 particles, one stub) | **Match.** |
| Tensile | Three machined sub-size bars, clip-on extensometer; yield scatter 1 to 2 % per bar ([notes L183][nmech]); AlSi10Mg yields 305 MPa | [PR 288][tens]: 228 ± 13 MPa (5.7 %) on four valid as-printed coupons, one of five broke in the grip, strain channel suspect, yield moves up to 30 MPa with the fit window | The simulated test is cleaner than the lab's first real one: three to five times less yield scatter and no lost tests. UTS and elongation scatter are comparable. |
| EDS | Simulated spectra with overlaps and detection limits | [PR 288][eds]: standardless EDS of loose AlSi10Mg powder read Si about 2 wt % low and Mg about 1 wt % high; one spectrum a sample, no repeatability | Nothing to calibrate precision against yet. The real bias is larger than a composition tolerance. |
| Calibration | `calib_*.json` fit the fast emulators to the twin's own slower simulators | SEM, EDS and tensile data exist on PR 288 | No simulator is fitted to a lab measurement on PR 288. The only lab figures they cite are from the atomizer runs (issue 219). |
| Utah printer, BYU SEM | 7 days to book, 2 to return; SEM 1 day ([`facility.py` L77-L95][fac]) | Print started [7 days](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353371606) after drop-off; SEM booked 2 days ahead | **Match** on the little there is. |
| Issue 256's schedule | `dal256`: one run a day Monday to Thursday, copper on Fridays, weekly SEM, Utah on alternate weeks | [The schedule][sched] | Faithful to the plan. The plan's own times are estimates. |
| Issue 275's seeds | Seven aluminium seeds, as planned | [The seeding plan][seed] | Faithful. On the twin's truth some seeds already beat T1 (row 5). |
| "Conventional lab" | The proposals' lab: first new aluminium alloy tested on day 96 (median), 23 a year | The one real case, commercial powder with no atomizing: [30 days](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138) from plan to tensile, 53 to polished-section EDS | The twin's conventional lab is a plan, more productive than the lab is today. That is conservative for the comparison, but the automated lab has no real counterpart at all. |

## 3. Against this repo's own benchmarks

| Question | This repo | The twin | Agree? |
|---|---|---|---|
| Does BOFN beat standard BO on aluminium? | `bofn-prelim`, 20 seeds, noise-free, 7-D: 85.8 % against 83.8 % of optimum at $100k, [p = 0.45][hc]. The README lists "BOFN beats standard BO" under [claims the benchmark doesn't support][prelim]. | 0.650 against 0.455, +0.195 (0.065 to 0.342), p = 0.009. From common seeds: 0.688 against 0.596, p = 0.076. | **Disagree in size.** The twin shows a gap the earlier benchmark does not. It is 23-D with noise and a new BOFN implementation; neither result has been run on the other's truth. |
| Tiered screening against BOFN on aluminium | BOFN ahead when the screen misses an effect (62.7 % against 85.8 %); level when it doesn't | 0.34 against 0.65 | **Agree**, and the twin's notes say why. |
| BOFN on copper | `bofn-cu-ded`, 20 seeds: [BOFN 73 %, random 22 %, standard BO 14 %, tiered −8 %][cuded] | Tiered 0.69, `bofn_blend` 0.67 (0.58 at 24 seeds), GP-BO 0.53, random 0.35, plain BOFN 0.33 | **Reversed.** The twin's notes explain tiered (nothing in its truth is hidden from the screen). They do not explain plain BOFN falling below GP-BO (−0.20, −0.39 to −0.01, p = 0.066). From common seeds the two are level (0.64 against 0.63). |
| A speed-up number | "3.8×" is spend against tiered screening, from mean curves, at one setting; [only 4 of 24 comparisons survive Holm](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-7175746177) | Days between two labs, from per-seed medians | **Not comparable.** Neither supports "BOFN is N× faster" in general. |
| Noise | None in any of this repo's benchmarks | Simulated instruments | The twin is the only one with noise, so it cannot be checked against the others on that. |
| Issue 265's test function | [No campaign has been run on it](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/265#issuecomment-7047070034) | Not used | Nothing to compare. |

## 4. Suggested rewording

**Takeaway card and the description's two bullets.** Replace the per-campaign "X× faster, 84 %" with:

> In this simulated benchmark, a stocked automated lab reached a new alloy better than the reference alloy sooner than
> a conventional lab that orders metal as it goes: aluminium in 116 days against 220 (1.9×, 95 % interval 1.1 to 3.4),
> copper in 225 days against at least 840 (at least 3.7×; the conventional lab got there in 6 of 12 three-year runs).
> Most of aluminium's gain is the stock: with both labs ordering as they go it is 1.2× (0.7 to 1.7). Copper's
> comparison also changes the method: the automated lab screens powder blends first.

**Cost.** Use one basis for both campaigns and lead with the one that includes the equipment:

> To get there, the automated lab cost 2.0× as much for aluminium and 1.15× for copper, equipment included
> (0.6× and 0.4× counting only what the campaigns spent). Equipment included, it costs less than the conventional lab
> only for copper, and only if outside users rent its idle hours, which this model assumes and does not show.

**"State of the art".** Say what the target is:

> The target is the reference alloy's score on the twin's synthetic alloy model (AlSi10Mg, C95800). One random design
> in twelve beats it, so reaching it measures how fast a lab makes and tests its first alloys, not a discovery.

**The heuristic line.**

> Against a conventional lab run by a metallurgist's rules of thumb, the automated lab is no faster on aluminium
> (1.05×, 0.7 to 2.2) at 2.6× the operating cost, and 2.2× faster on copper (1.8 to 2.6).

**Copper, in "Where BOFN doesn't win".**

> On copper, tiered CALPHAD screening finished ahead of BOFN with blend screening: 0.68 against 0.58 over 24 seeds
> (0.69 against 0.67 in the first 12). Plain BOFN did no better than random (0.33 against 0.35).

**The replay.** A caption for its whole length:

> One seed of twelve. In this one, aluminium reaches the target on day 20; the median seed takes 116 days.

**Run counts.** "12 one-year automated runs and 12 three-year conventional runs per policy" in place of "twin-years".

**Notes frame.** Add to "Assumed": "the automated lab's feedstock stock on day 0; the atomizer's failure rate and
yield; who staffs the automated lab". Change "Every measurement, with noise" to "Every measurement, with modelled
noise not yet calibrated on the lab's instruments".

**`notes/twin_video.md` L55-L56.** "The takeaway compares the stocked vertical lab running BOFN (with blend screening
for copper) against the conventional lab ordering as it goes and running plain BOFN."

## 5. Experiments that would settle the open claims

Ranked by how much each would change the reading. The first four reuse the twin as it is.

1. **Stock the conventional lab.** `conventional` with `stock="stocked"`, `bofn` and `heuristic`, 12 seeds. With
   `stock.jsonl` this completes the two-by-two of lab and stocking, and gives automation's own share for row 1.
2. **Same copper method in both labs.** Either `bofn_blend` in the conventional lab on Utah's MX-Lab, or a stated
   reason it cannot run there. And `bofn_blend` with `stock="lean"`, which `stock.jsonl` lacks.
3. **More seeds on the two headline arms,** 36 each, and one comparison named in advance. Aluminium's factor sits on
   the 0.05 line after correction, and copper's reference median rests on one seed.
4. **One horizon.** Run the automated lab for three years too, or report every factor on the first 365 days of both.
5. **Put the logged atomizer in.** Failure rate, usable yield and starts per week from
   [`atomizer-runs/runs.csv`][runs], and the achieved ordering delay from issue 146, in both labs. This is the largest
   gap between the twin and the record.
6. **Calibrate the tensile and EDS simulators on PR 288,** then re-run: 5.7 % yield scatter, one lost test in five,
   and the measured AlSi10Mg strength.
7. **Report the factor against the target,** not at T1 alone. `econ_summary.json` already stores it
   (`af_vs_target`).
8. **Show the cost with no outside users as the default,** and the shared case as a sensitivity. The 0 to 40 hours a
   week table is already in `outside_work.demand_sensitivity`.
9. **Run the two BOFN codes on one truth:** the twin's BOFN and GP-BO on `bofn-cu-ded`'s network, or this repo's
   BOFN inside the twin. That settles the reversed copper ranking in section 3.
10. **In the lab:** time ten atomizer runs end to end and weigh every lot. Issue 256 says nothing has been timed, and
    one weighed mass balance exists.

## Files

| File | What it is |
|---|---|
| [`recompute.py`](recompute.py) | Independent recomputation from the stored runs (numpy only) |
| [`recomputed.md`](recomputed.md) | Its output: every arm, factor, interval, test and the Holm table |
| [`rerun_twin_costs.py`](rerun_twin_costs.py) | Re-runs the twin's cost model; needs the byu-vcl checkout |
| [`rerun_twin_costs.txt`](rerun_twin_costs.txt) | Its output: re-run against stored, for 20 cost ratios and 18 cost-per-alloy figures |

```bash
git clone https://github.com/vertical-cloud-lab/byu-vcl /tmp/byu-vcl && git -C /tmp/byu-vcl checkout 357d149
python audits/twin-round2-video/recompute.py /tmp/byu-vcl/vertical-lab > audits/twin-round2-video/recomputed.md
python audits/twin-round2-video/rerun_twin_costs.py /tmp/byu-vcl/vertical-lab /tmp/rerun.json
```

[bv]: https://github.com/vertical-cloud-lab/byu-vcl/tree/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab
[R1]: recomputed.md#1-every-arm-seeds-that-reached-t1-and-when
[R2]: recomputed.md#2-time-to-t1-acceleration-factors-intervals-and-tests
[R3]: recomputed.md#3-cash-to-t1-the-campaigns-own-spending
[R4]: recomputed.md#4-best-alloy-at-the-end-of-the-year-mean-true-utility-over-seeds
[R5]: recomputed.md#5-holms-correction-over-the-13-comparisons-the-video-states
[R6]: recomputed.md#6-the-replayed-seed-seed-0-of-automated-bofn_blend-against-the-12-seeds
[R7]: recomputed.md#7-the-same-headline-at-the-harder-target-t2
[R9]: recomputed.md#9-copper-with-all-24-automated-seeds-mainjsonl-seeds-0-11-plus-cu_seedsjsonl-seeds-12-23
[R10]: recomputed.md#10-seeds-at-t1-within-the-first-365-days-both-labs-on-the-same-window
[RR]: rerun_twin_costs.txt
[bench2]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/bench2.py#L46-L54
[bench2b]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/bench2.py#L71
[stocked]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/campaign.py#L97-L105
[accel]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/accel.py#L58-L146
[pick]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/video/data.py#L601-L630
[take]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/video/figs_anim.py#L1063-L1080
[notesf]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/video/compose.py#L719-L733
[costc]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/econ.py#L785-L805
[staff]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/econ.py#L94-L99
[hands]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/econ.py#L417-L457
[physd]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/physics.py#L7-L8
[supply]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/supply.py#L59-L62
[phys]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/physics.py#L58-L62
[yieldm]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/instruments/atomize_yield.py#L77-L78
[fac]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/twin/facility.py#L77-L95
[oracle]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/out/twin2/oracle.json#L62
[econ]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/out/twin2/econ/econ_summary.json
[n53]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/notes/twin_round2.md?plain=1#L226-L229
[n54]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/notes/twin_round2.md?plain=1#L296-L321
[n56]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/notes/twin_round2.md?plain=1#L391-L393
[n57]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/notes/twin_round2.md?plain=1#L410-L413
[nvid]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/notes/twin_video.md?plain=1#L51-L58
[nmech]: https://github.com/vertical-cloud-lab/byu-vcl/blob/357d149b3832b254e06bfe80904df00ec534ef19/vertical-lab/notes/twin_instruments_mech.md?plain=1#L183
[runs]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/8320f13623c7961fcce12ee4d5d2033f4d8c9936/atomizer-runs/runs.csv
[runsreadme]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/8320f13623c7961fcce12ee4d5d2033f4d8c9936/atomizer-runs/README.md
[prov]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/8320f13623c7961fcce12ee4d5d2033f4d8c9936/atomizer-runs/2026-10-27-nab-k7m2q9/provenance.md?plain=1#L35
[sched]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/6ff7717e33a2e7a500995ab43e1ae58fd43a88c6/al-campaign-schedule/README.md?plain=1#L91-L107
[seed]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/ce394072f58aaedbbd72c688cbf597ac09cb6303/bofn-seeding/README.md
[tens]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/48e1ddc3ebe02fb2bb700d39b7af651784cdde13/preliminary-data/tensile-alsi10mg-utah/README.md?plain=1#L44-L51
[eds]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/48e1ddc3ebe02fb2bb700d39b7af651784cdde13/preliminary-data/sem-eds-feedstock/README.md?plain=1#L30-L35
[hc]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/d1ca727fb37fa044cbcf78c420e17aa1ac827bc5/benchmarks/bofn-prelim/checks/headline_check.txt#L45-L48
[prelim]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/d1ca727fb37fa044cbcf78c420e17aa1ac827bc5/benchmarks/bofn-prelim/README.md?plain=1#L323-L337
[cuded]: https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/b1ba843b33d57e8fbb15e6bbf1aa7468b815f8d7/benchmarks/bofn-cu-ded/README.md?plain=1#L45-L58
