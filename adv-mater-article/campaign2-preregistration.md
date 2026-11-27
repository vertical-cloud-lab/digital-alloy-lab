# Campaign 2 pre-registration (draft)

*Draft of 2026-11-27, for the 2027 campaign that version A of the article rests on. Bracketed items wait on
campaign 1 and on decisions D3, D9 and D10 in the [README](README.md). The final version must be committed
(hash and date recorded here) **before the first campaign 2 decision**, and every later change logged under
"Deviations". The synthetic benchmarks showed why: without a fixed target, baseline and stopping rule, the
speed-up depends on which target and seed one picks (PR #293, PR #297).*

## Questions

- **Q1 (live).** Does the cost-aware network optimizer, run on the real lab, stop candidates at different steps
  because of the acquisition, and what does it find within the budget?
- **Q2 (twin).** Across repeated simulated campaigns on a twin fitted to the lab's records, does it reach the
  target at lower spend than screen-then-test, and is the gain larger when the CALPHAD screen misses an effect
  (κ = 1) than when it doesn't (κ = 0)?

The live campaign answers Q1 once; Q2 needs repetition, so it is answered on the twin. Neither is claimed from the
other.

## Fixed before the first decision

| Item | Setting |
|---|---|
| Design space | [elements and bounds frozen at D10; Si in or out] |
| Objective | [e.g. desirability on yield strength (as built and after the one pre-chosen heat treatment), elongation, and mineral burden B (D9); a print counts only if ≥ 99 % dense and crack-free] |
| Target T | [objective value, e.g. yield strength above AlSi10Mg printed and tested the same way by more than both 95 % CI half-widths, at no lower elongation, with B below Scalmalloy's by ≥ X %] |
| Nodes | CALPHAD → charge → atomize → powder characterization → print (desktop) → density/section/hardness → tensile (finalists) |
| Node costs | median cost per result from campaign 1's step log (Table 1), frozen at [date] |
| Acquisition | partial-evaluation knowledge gradient per unit cost; a node may be queried only if its parents have outputs; [batch size, how pending results are fantasized] |
| Failed vs abandoned steps | [#274 resolution: model failure at the failing step] |
| Prior data | campaign 1 (all runs, prints and tests), [plus seeds: six compositions, #275] |
| Budget | [person-hours and $; e.g. 12 weeks, ≤ 35 atomizer runs] |
| Stopping rule | budget exhausted, or T met and confirmed by ≥ 3 tensile specimens and outside composition |
| Decision log | every decision records: candidate, node, acquisition value, cost, runner-up, model version; committed weekly |

## Twin analysis (Q2)

- **Fit:** the twin's step durations, costs, failure rates, usable-powder fraction and measurement noise come from
  campaign 1 and 2 records (T1). It passes if, replaying campaign 2's own decisions, its spend to T lands within
  [x %] of the real one (T4).
- **Policies:** the cost-aware network optimizer, screen-then-test (CALPHAD screen, then full chain on the top
  [k]), full-chain network BO, standard BO and random. All start from the same prior data and seeds.
- **Conditions:** κ = 0 and κ = 1 (how much nucleant-driven crack suppression the screen misses), plus the
  measured κ if campaign data allow estimating it.
- **Primary endpoint:** spend to T. Secondary: days to T; best objective at the budget.
- **Analysis:** ≥ 20 seeds per policy and condition; acceleration factor = ratio of median spend to T;
  matched-seed bootstrap 90 % CI; seeds that never reach T are counted as censored, not dropped.
- **H1** is rejected if the median spend to T is not lower than screen-then-test's at κ = 1. **H2** is rejected if
  the acceleration factor at κ = 1 is not larger than at κ = 0.

## What gets reported regardless

The result is reported whatever it is, including a tie or a loss to screening.

## Record

| Version | Commit | Date | Who approved |
|---|---|---|---|
| draft | (this file) | 2026-11-27 | — |

## Deviations

None yet.
