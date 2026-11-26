# bofn-clocked: pre-registration

Written and committed on 2026-11-26, before any experiment below was run (issue 283). The commit that adds this file
comes before the commits that add results; anything changed after that is listed under "Changes after
registration" at the end, with the reason.

**Everything here is synthetic.** The truth is bofn-prelim's invented alloy network with noise, failures, routes and
a corrosion branch added. Durations, capacities and prices are assumptions (README, "Assumptions"). The results say
how policies, routes and records interact *in this model*, not what a real campaign will find.

## Definitions fixed in advance

- **Discovery.** An alloy is *claimed* when one coupon has at least 3 valid tensile bars and a finished 30-day
  immersion whose measured rate passes the limit. The campaign's claim is the claimable coupon with the highest
  *measured* mean objective. Its value is the *true* objective of that design if it truly passes corrosion, else 0.
- **Targets.** T1 = 60 % and T2 = 80 % of the true constrained optimum of that truth. At `kappa = 1` the CALPHAD
  screen's region tops out at 70 % (computed), so T1 is reachable inside the screen and T2 is not; T2 is round 3's
  "halfway" target rounded (halfway from 70 % to 100 % is 85 %; 80 % is the "good alloy" of the earlier reply on this
  issue). At `kappa = 0` both targets lie inside the screen's region (its ceiling is 99 %).
- **Days to T** is the first day the claim's value reaches T; **dollars to T** is the money spent by then. A campaign
  that doesn't get there before its horizon or its budget runs out is censored at the horizon.
- **A tenth.** For a policy P and a conventional baseline C on the same truth, P "reaches a tenth" on a seed if
  days_P ≤ days_C / 10 (and, separately, dollars_P ≤ dollars_C / 10), where C's value is its median over its seeds
  (censored at its horizon, which makes the comparison conservative for P when C is censored: C's true time is
  longer). Reported as the fraction of P's seeds, with a 90 % bootstrap interval.
- **Statistics.** Mean ± SE over seeds; paired differences on matched seeds (the same truth seed, initial data and
  noise streams where the policy doesn't change them) with two-sided Wilcoxon signed-rank tests; Kaplan-Meier-style
  medians when some seeds are censored. No correction for multiple comparisons unless stated; the number of tests is
  reported.

## E1. Headline: how many days and dollars to T1 and T2, against the conventional baselines

**Setup.** Two truths, `kappa = 1` (CALPHAD's crack screen misses the inoculant effect) and `kappa = 0` (it doesn't),
10 seeds each. Conventional baselines, decisions in rounds of 4 designs at Monday meetings after all of a round's
results are back, tiered screening as the decision rule (bofn-prelim's: CALPHAD screen, then EI on the shortlist):
`conv_lots` (custom powder lots from an outside supplier, outside printing, outside EDM, core-facility tensile; the
Genesis draft's 8-32-week cycle) and `conv_atomizer` (DAL's own atomizer on DAL #256's schedule, outside printing).
Automated lab (`vertical`: in-house atomizer, in-house printer and the partner's at once, in-house bars, 24 immersion
positions with interim readings), asynchronous decisions, each policy filling what capacity allows: tiered screening,
GP-BO (kriging believer), BOFN (network EI per cost of the remaining path), pKGFN (fixed, see E4), random.
Budget $250k for every campaign; horizons 1 year (automated) and 4 years (conventional).

**Meant to show.** (a) How much of any speed-up comes from the lab (tiered screening on the automated lab against the
conventional baselines) and how much from the algorithm (network policies against tiered screening on the same lab).
(b) Whether "a tenth of the time and a tenth of the money" is reachable in this model, and under which truth.

**Expected, and what would count against it.**
- The automated lab's speed-up in days over `conv_lots` is mostly the lab's: tiered screening on the automated lab
  reaches T1 several times sooner than `conv_lots`. *Against:* automated tiered screening no faster than `conv_lots`.
- At `kappa = 1`, network policies reach T2 and tiered screening doesn't (its region tops out at 70 %).
  *Against:* tiered screening reaches T2, or network policies don't on most seeds.
- At `kappa = 0`, network policies are no faster than tiered screening on the automated lab (bofn-prelim found them
  level). *Against (in their favour):* a paired advantage at p < 0.05.
- Money: the automated lab spends *less* than `conv_lots` to T1 but not ten times less, because the floor is the
  30-day immersion and a few powders, prints and bars. *Against:* ≥ 10× less money on most seeds.
- pKGFN after the E4 fix keeps up with BOFN at `kappa = 0`. *Against:* it is behind BOFN at p < 0.05.

## E2. Routes: running in-house and partner routes together

**Setup.** `kappa = 1`, BOFN and tiered screening, 10 seeds, on three facilities: `nearterm` (today's lab: the
atomizer on DAL #256's schedule, the partner's printer only, outside EDM), `vertical_ih` (in-house printer only) and
`vertical` (in-house and partner printers together).

**Meant to show** how much wall time each route buys. **Expected:** `vertical` ≤ `vertical_ih` < `nearterm` in days
to T2; the partner's printer adds little once the in-house printer runs round the clock. *Against:* `nearterm`
within 20 % of `vertical`.

## E3. The value of provenance

**E3a, another lab's data.** `kappa = 1`, BOFN, 10 seeds. Every campaign gets the same 40 coupons' worth of records
from "another lab" whose printer runs on a shifted process ridge and whose tensile frames read high, plus two
reference alloys both labs have made. Models: `separate` (ignore the other lab), `naive` (pool as if own),
`site` (pool with a per-site offset on the density and strength nodes). **Expected:** `site` ≤ `separate` <
`naive` in days to T2 (naive pooling misleads). *Against:* naive pooling no worse than separate.

**E3b, a time machine.** `kappa = 1`, BOFN, 8 seeds, three campaigns in a row on the same physics with different
goals (mineral weight 0.3, then 0.6, then 0.1 with a tighter corrosion limit) and calibration drift between them.
Each campaign re-makes two reference alloys at random times (repeats shuffled over time). Histories:
`none` (each campaign starts cold), `documented` (every node-level record of earlier campaigns, with campaign labels,
so the drift is estimated from the repeats) and `poor` (the same experiments recorded the usual way: process
settings missing and filled with nominal values, no campaign labels, failed builds and failed powders left out).
**Expected:** campaigns 2 and 3 reach T1 and T2 sooner and cheaper with `documented` than with `none`; `poor` helps
less than `documented` and may hurt. *Against:* `documented` no better than `none` in campaign 3.

## E4. pKGFN at `kappa = 0`

**Question (Sterling):** why does bofn-prelim's pKGFN fall behind screening when the screen is right (57 % against
85 %)? byu-vcl's round 3 found that with an incumbent of 0 and a never-negative utility, the knowledge gradient of
finishing a part is exactly 0.

**Plan.** Re-run bofn-prelim's own `run_pkgfn` unchanged at `kappa = 0` (seeds 0-7), logging the best KG of every
stage at every step, the fallback flag, and the best value reachable from the compositions it may atomize (the
"restricted ceiling"). Run bofn-prelim's own lookahead variant (`pkgfn_la`, still restricted) on the same seeds to
separate "restricted to simulated compositions" from "a new powder's value is invisible to one-step KG".
**Expected (before looking):** KG of tensile tests is exactly zero on most steps (an alternative design holds the
inner max), and KG of new powders is near zero, so pKGFN keeps printing a few powders. *Against:* KG of tensile
rarely zero, or the restricted ceiling below 60 % (then the restriction, not KG, is the cause).

**Fix in this benchmark's pKGFN:** any composition may be atomized (CALPHAD runs first, $10); a new powder is valued
together with its first build; finishing steps (replicate bars, immersion, stopping) are decided by the same
claim-aware rules for every policy, so they can't be valued at zero. Tested in E1.

## E5. Stretch: one search across alloy families

`CrossTruth`: six composition dims, three families (7xxx-like, Al-Si, Al-Mg-Sc) whose best alloys lie between them.
BOFN, 8 seeds, `vertical` lab, same money. `global` (one campaign over the whole space) against `per_family` (three
campaigns, one per family corner, each with a third of the budget and of the lab's capacity, run at the same time).
**Expected:** `global` reaches a higher value by day 120 than the best of the three `per_family` campaigns.
*Against:* `per_family` ahead at day 120. This is a first look; the truth is hand-made and the effect is built in, so
it shows how the search behaves when boundaries blur, not that they do.

## Changes after registration

All made on 2026-11-26 before any of the final runs, which were started together afterwards
(`python run.py all`). None was made after seeing a result of the experiments above.

1. **E2b added (before any E2 run).** Sterling's comment asks for gas-atomized powder with its lead time and lot size
   as a route, and for "intelligently moving to gas atomization and a distributed validation network". No policy uses
   that route for discovery (51 days per lot can't shorten time to T1/T2), so E2b tests it where it matters: confirming
   the claimed alloy on a gas-atomized lot printed on the partner's machine (targets T1c/T2c), ordering the lot either
   after the claim or early (three bars at the top of the field plus a passing day-7 immersion reading). *Expected:*
   ordering early confirms sooner on most seeds; *against:* no paired difference.
2. **Policy fixes found in smoke-test campaigns** (single seeds run while writing the code, not the experiments):
   - pKGFN valued a print by one coupon's fantasy; every KG was then exactly 0 on 95 % of decisions and the campaign
     stalled. It now fantasizes a build's six coupons jointly, which is what a print returns.
   - BOFN's constrained EI from 32 raw draws rounded to exactly 0 when the corrosion model expected a fail, and a
     campaign stalled (E3a, seed 0, `separate`). EI is now computed in normal form with a smooth pass probability, as
     byu-vcl's round 3 does, and an action needs EI ≥ 1e-4 to start (round 3's threshold).
   - The EI incumbent was the largest single-bar reading, which is biased high once many parts are tested (the
     winner's curse) and made EI vanish. It is now the model's posterior mean at tested parts likely to pass
     corrosion (BOFN, pKGFN and GP-BO alike).
   - Tiered screening and BOFN made powders they then didn't print. Every powder now gets at least one build at the
     policy's own best settings, and an unprinted lot counts against the batch limit until it is printed.
   - When nothing is worth its cost and nothing is in flight, a model-based policy makes its single best candidate
     rather than ending the campaign with money left (counted as `zero_value` in every result file).
   - The conventional baseline tracked its lots by predicted index and crashed when a lot failed; it now finds them
     by composition.
3. **A first E1 sweep was started and stopped.** It had finished 15 pKGFN campaigns with the code before fix 2; those
   results were discarded, not used.
4. **E2b's confirmation policy was fixed and E2b re-run.** In the first E2b runs the discovery loop kept spending
   while the gas-atomized lot was out for 51 days, and 6 of 10 "after" campaigns ran out of money before confirming,
   which says more about the budget than about when to order. Discovery now stops once an alloy is claimed and its
   production lot is on order. The 14 finished E2b campaigns were discarded; no other experiment uses that policy.
   A second bug in the same policy (a lot counted as ordered when proposed, not when the supplier accepted it, so one
   campaign stopped discovery with nothing on order) was fixed before the final E2b run.
