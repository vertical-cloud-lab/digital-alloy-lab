# Campaign 2 pre-registration (draft)

*Draft of 2026-11-27, revised after a mock editorial review the same day (outline.md §9), for the 2027 campaign that version A of the article rests on. Bracketed items wait on
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
| Design space | **3–5 elements** (more spreads ~20–35 runs too thin for the surrogates), [bounds frozen at D10; Si in or out] |
| Objective | [e.g. desirability on aged yield strength and elongation; a print counts only if ≥ 99 % dense and crack-free; Sc-free as a constraint, with mineral burden B reported by element rather than folded into the objective (D9)] |
| Positive control | An in-house **Sc-free reference alloy** ([Al–Mg–Zr or Al–Mn–Cr–Zr], from the literature), atomized, printed, aged and tested exactly as the candidates. In-house AlSi10Mg (route control) is printed beside the commercial lot on both machines |
| Target T | **Aged yield strength at least that of the positive control**, at no lower elongation, crack-free and ≥ 99 % dense, Sc-free, with n ≥ 3 specimens and the difference beyond both 95 % CI half-widths. Not "above as-built AlSi10Mg" (AlSi10Mg printed here gives 228 MPa, below its datasheets), and not "lower B than Scalmalloy" (any low-Mg alloy passes that, since B weights Mg like Sc). If the campaign can't plausibly reach T, decide before it starts that the article is a methods paper for another journal |
| Heat treatment | An aging curve per alloy family (Zr-only alloys peak at higher aging temperatures), not one pre-chosen treatment for all |
| Nodes | CALPHAD → charge → atomize → powder characterization → print (desktop) → density/section/hardness → tensile (finalists) |
| Node costs | median cost per result from campaign 1's step log (Table 1), frozen at [date] |
| Acquisition | partial-evaluation knowledge gradient per unit cost; a node may be queried only if its parents have outputs; [batch size, how pending results are fantasized] |
| Failed vs abandoned steps | [#274 resolution: model failure at the failing step] |
| Prior data | campaign 1 (all runs, prints and tests), [plus seeds: six compositions, #275] |
| Budget | [person-hours and $; e.g. 12 weeks, ≤ 35 atomizer runs] |
| Stopping rule | budget exhausted, or T met and confirmed by ≥ 3 tensile specimens and outside composition |
| Decision log | every decision records: candidate, node, acquisition value, cost, runner-up, model version; committed weekly |
| Stop labels | Every stop is labelled **failure** (the step gave no usable result), **constraint** (a hard rule), or **acquisition** (lower expected gain per cost than another candidate's step). Only acquisition stops test the method |
| Stop audit | A random **25 %** of acquisition stops is pushed one step further; the share that would have been worth continuing is the false-stop rate. Departures from a pre-registered expert stage-gate are logged with what they returned |
| Failures in the model | Hardware failures (plate, nozzle, cup) are modelled as a per-step failure process, not as a property of the composition (#274) |

## Twin analysis (Q2)

- **Fit out of sample:** the twin is fitted on **campaign 1 only** (T1), and its prediction of campaign 2 (spend and
  days to T, failure counts) is committed here before campaign 2 starts. It passes if campaign 2 lands inside the
  predicted interval (T4). It is refitted on both campaigns only afterwards, for the counterfactuals.
- **Ground truths** are drawn from the fitted posterior over the composition–property landscape, not from one
  hand-built function.
- **Policies:** the cost-aware network optimizer (pKGFN); **full-chain network BO** (the headline comparison, since it
  isolates partial evaluation); the **best-form screen-then-test**, which uses every CALPHAD output, including
  the primary Al₃(Zr,Sc) fraction, is trained on campaign 1 and has its cut-off k tuned; standard BO;
  multi-fidelity BO; and random. All start from the same prior data and seeds.
- **Conditions:** the **measured** κ (from Fig. 4d's crack-index misses, with its interval) is primary; κ = 0 and κ = 1
  bracket it.
- **Robustness:** decisions and acceleration factors are recomputed with every step cost moved by ±50 %.
- **Model check before campaign 2:** on campaign 1 data, the network must predict yield strength better than a
  GP from composition straight to yield strength (held-out log likelihood).
- **Primary endpoint:** spend to T. Secondary: days to T; best objective at the budget.
- **Analysis:** ≥ 20 seeds per policy and condition; acceleration factor = ratio of median spend to T;
  matched-seed bootstrap 90 % CI; seeds that never reach T are counted as censored, not dropped.
- **H1** is rejected if the median spend to T is not lower than full-chain network BO's, and separately than the
  best-form screen's, at the measured κ. **H2** is rejected if the acceleration factor at κ = 1 is not larger than
  at κ = 0.

## What gets reported regardless

The result is reported whatever it is, including a tie or a loss to screening.

## Record

| Version | Commit | Date | Who approved |
|---|---|---|---|
| draft | (this file) | 2026-11-27 | — |

## Deviations

None yet.
