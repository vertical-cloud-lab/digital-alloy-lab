# Campaign 2 pre-registration (draft)

*Draft of 2026-11-27, for the 2027 campaign that version A of the article rests on. Revised the same day so that
campaign 2 is measured against **industry scandium-free alloys printed and tested in-house** (Sterling, on
[#120](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/120)). The campaign paper
([#277](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277)) adds the same baselines and owns their
sourcing and first measurement; the two pre-registrations must use the same definitions (marked **with #277**
below). Bracketed items wait on campaign 1 and on decisions D3, D9 and D10 in the [README](README.md). The final
version must be committed (hash and date recorded here) **before the first campaign 2 decision**, and every later
change logged under "Deviations". The synthetic benchmarks showed why: without a fixed target, baseline and
stopping rule, the speed-up depends on which target and seed one picks (PR #293, PR #297).*

## Questions

- **Q1 (live).** Does the cost-aware network optimizer, run on the real lab, stop candidates at different steps
  because of the acquisition, and does what it finds lie beyond the front of the industry baselines measured the
  same way?
- **Q2 (twin).** Across repeated simulated campaigns on a twin fitted to the lab's records, does it reach the
  target at lower spend than screen-then-test, and is the gain larger when the CALPHAD screen misses an effect
  (κ = 1) than when it doesn't (κ = 0)?

The live campaign answers Q1 once; Q2 needs repetition, so it is answered on the twin. Neither is claimed from the
other.

## The baselines: an industry front, measured in-house

Of the scandium-free alloys sold as powder for LPBF, two belong to the families campaign 2 works in, and both are
stronger than AlSi10Mg after a single direct age. Bought, printed, aged and tested here exactly as the candidates
are, they give a one-to-one comparison: if a candidate lies beyond them, the improvement is not an artefact of a
different machine, specimen or test. Their in-house values against their data sheets show whether this lab
measures on a par with industry.

| Baseline | Role | Data sheet: condition, orientation | YS / UTS (MPa), EL (%) | B_NIR (wt %)\* |
|---|---|---|---|---|
| **EOS Aluminium Al5X1**, Al–Mg–Zr–Mn (Mg 2.5–4.2, Zr 0.6–1.8, Mn 0.1–1.0 wt %; Aluminum Association 5A05.50); gas-atomized, 20–63 µm | Commercial counterpart of the Al–Mg–Zr seeds (O1; Croteau et al. 2018). On their data sheets it is the stronger of the two and has the lower burden | direct aged 400 °C, 6 h; horizontal; EOS M 290, 40 µm, ASTM E8 | 385 / 415, 14.5 (as built: 260 / 310, 23) | 3.1–4.2 |
| **Höganäs forAM Al-HS1**, Al–4.8Mn–0.8Cr–0.8Zr (typical); gas-atomized, 20–63 µm | Commercial counterpart of the Al–Mn–Cr–Zr focus family (seeds S1, O3) | direct aged 375 °C, 4 h, in air; X/Y; bars machined from printed cylinders | 370 / 440, 12 (as built: 220 / 285, 25) | 5.4–5.6 |
| AlSi10Mg: commercial lot, plus the in-house atomized lot as route control | Lower anchor; the campaign paper's comparator | as built, horizontal (EOS M 290, 30 µm) | 270 / 461, 10.2 | 5.2–10.3 |
| Scalmalloy | Context only (data sheets), unless the campaign paper prints it [check #277's branch] | direct aged 325 °C, 4 h | 465–500 / 505–530, 11.5–15.8 | 4.7–6.0 |

\* B_NIR = Σ wᵢ·NIRᵢ/100 from the nominal composition (Al5X1 at the midpoints of its ranges), with the campaign
paper's inputs (USGS *Mineral Commodity Summaries 2026*; `tools/mineral_burden_check.py`). A range, because USGS gives
some import reliances only as bounds. Campaign values use each lot's ICP-OES composition. Sources: EOS process and
material data sheets for Al5X1, Höganäs data sheet 3312HOG-3, PR #285's AlSi10Mg and Scalmalloy set; all values
checked against the vendors' documents on 2026-11-27.

- **At least one of Al5X1 and Al-HS1; both if sourcing allows** (**decide with #277**, whose run is pricing them).
  On their data sheets, Al5X1 has the higher aged yield strength *and* the lower B_NIR, so under B_NIR it alone
  sets the scandium-free front, and Al-HS1 sits behind it. Al-HS1 still earns its place as the same-family
  comparator for Al–Mn–Cr–Zr candidates, and it would join the front on another axis (its data sheet advertises
  strength at temperature) or under a burden metric that weighs Mn less. If only one is bought: Al5X1 for the
  front; Al-HS1 if campaign 2 stays in the Al–Mn–Cr–Zr family.
- **Measured the same way as the candidates:**
  - same machine, and the same builds: every tensile build of campaign 2 carries at least one baseline;
  - the same laser parameters; a baseline that isn't ≥ 99 % dense with them gets the same short power–speed sweep a
    candidate would get, and the sweep is reported;
  - the same specimen geometry, surface and test, and ICP-OES on every lot, like every candidate powder;
  - the same aging rule: each baseline joins its family's aging curve, and is also aged on its supplier's schedule
    for the parity check.
- **Who measures them first.** The campaign paper buys the powders and prints them first, in campaign 1; its
  sourcing and schedule are on #277's branch. Campaign 2 reprints them in its own builds, and on the desktop LPBF
  for density and hardness.

## Fixed before the first decision

| Item | Setting |
|---|---|
| Design space | **3–5 elements** (more spreads ~20–35 runs too thin for the surrogates), [bounds frozen at D10; Si in or out]; Sc excluded |
| Objectives | **Aged yield strength (maximize) and mineral burden B (minimize)**. A print counts only if ≥ 99 % dense and crack-free, and a candidate only if its elongation is at least [floor: e.g. 5 %, FLAIME's Al–Mn–Cr–Zr gate, or no lower than the baseline it is compared with]. **Decide:** elongation as a floor or as a third objective |
| Burden metric | B as frozen for the campaign paper before its screen ranks anything (**with #277**, decision D9; currently proposed: B_NIR = Σ wᵢ·NIRᵢ/100, MCS 2026, Fe counted as zero, bounds carried as intervals), from each lot's ICP-OES composition, reported by element. **Known issue to fix:** B_NIR counts Mg like Sc, so Scalmalloy's B is mostly its 4.7 wt % Mg, and any alloy with less Mg beats it without any design effort. Al5X1 does. So the claim is not "lower B than Scalmalloy": it is expanding the scandium-free front, with Sc excluded outright. Sc content and the cost of the critical additions are reported alongside, and the SI redraws the front under each |
| Baselines | As above: Al5X1 and/or Al-HS1, printed, aged and tested here the same way as the candidates; AlSi10Mg in the same builds |
| Parity check | Each in-house baseline, in its data sheet's condition and orientation, on machined bars (as the suppliers test), n ≥ 3. **On a par** if its mean yield strength and UTS each lie within ±10 % of the data-sheet value (**decide the band, with #277**). Elongation is reported, not tested: it depends on specimen geometry and surface. A baseline outside the band is investigated before campaign 2's first decision (parameters, surface, extensometry, powder O). If the gap stays, the paper reports the offset and drops "on a par with industry". The same-build comparison stands either way |
| Target T | A Sc-free candidate **expands the in-house baseline front**. Against every in-house baseline it either has lower B, or is stronger; and it is stronger than in-house AlSi10Mg (the campaign paper's bar, kept as a floor). Equivalently, its yield-strength margin over the front at its own burden is positive. So a candidate as strong as Al5X1 counts if its B is lower, and one with more B counts only if it is stronger. It must also be crack-free, ≥ 99 % dense and above the elongation floor, with n ≥ 3 valid specimens (5 recommended). "Stronger" uses the rule below. "Lower B" uses the campaign paper's interval rule (**with #277**). That rule is either unpaired, with the whole interval below the other's lower bound, or paired, lower for every import reliance within the USGS bounds. Paired is fairer, because both alloys share the same inputs |
| "Stronger" | **With #277.** Its draft rule needs the means to differ by more than both 95 % CI half-widths. At the April AlSi10Mg bars' scatter (CV 5.7 %), applied at Al5X1's ~385 MPa, beating Al5X1 under that rule takes ≈ 110 MPa with n = 3 each and ≈ 55 MPa with n = 5. A Welch test (the 95 % CI of the difference excludes zero) takes ≈ 50 MPa with n = 3 and ≈ 32 MPa with n = 5. **Decide:** the rule and n. Recommended: Welch, n = 5 for baselines and finalists |
| Beyond published alloys | Reported, not part of T: whether the candidate is also non-dominated by the published values of Sc-free alloys (the campaign paper's comparator set, `literature-alloys.csv` at its freeze commit). Those were measured on other machines and specimens, so the test is stated as against reported values. It decides whether the alloy can be called new, rather than better than what was measured here |
| Heat treatment | An aging curve per alloy family (Zr-only alloys peak at higher aging temperatures), not one pre-chosen treatment for all; the baselines also at their suppliers' schedules |
| Nodes | CALPHAD → charge → atomize → powder characterization → print (desktop) → density/section/hardness → tensile (finalists) |
| Node costs | median cost per result from campaign 1's step log (Table 1), frozen at [date] |
| Acquisition | partial-evaluation knowledge gradient per unit cost, on a scalar target: the candidate's yield-strength margin over the in-house front at its burden (positive means it expands the front); a node may be queried only if its parents have outputs; [batch size, how pending results are fantasized] |
| Failed vs abandoned steps | [#274 resolution: model failure at the failing step] |
| Prior data | campaign 1 (all runs, prints and tests, including the baselines), [plus seeds: six compositions, #275] |
| Budget | [person-hours and $; e.g. 12 weeks, ≤ 35 atomizer runs] |
| Stopping rule | budget exhausted, or T met and confirmed by the specimens above and an outside composition check |
| Decision log | every decision records: candidate, node, acquisition value, cost, runner-up, model version; committed weekly |
| Stop labels | Every stop is labelled **failure** (the step gave no usable result), **constraint** (a hard rule), or **acquisition** (lower expected gain per cost than another candidate's step). Only acquisition stops test the method |
| Stop audit | A random **25 %** of acquisition stops is pushed one step further; the share that would have been worth continuing is the false-stop rate. Departures from a pre-registered expert stage-gate are logged with what they returned |
| Failures in the model | Hardware failures (plate, nozzle, cup) are modelled as a per-step failure process, not as a property of the composition (#274) |

## Twin analysis (Q2)

- **Fit out of sample:** the twin is fitted on **campaign 1 only** (T1), and its prediction of campaign 2 (spend and
  days to T, failure counts) is committed here before campaign 2 starts. It passes if campaign 2 lands inside the
  predicted interval (T4). It is refitted on both campaigns only afterwards, for the counterfactuals.
- **Ground truths** are drawn from the fitted posterior over the composition–property landscape, not from one
  hand-built function. The baselines sit at their in-house measured values, so T means the same thing in the twin
  as in the lab.
- **Policies:** the cost-aware network optimizer (pKGFN); **full-chain network BO** (the headline comparison, since it
  isolates partial evaluation); the **best-form screen-then-test**, which uses every CALPHAD output, including
  the primary Al₃(Zr,Sc) fraction, is trained on campaign 1 and has its cut-off k tuned; standard BO;
  multi-fidelity BO; and random. All start from the same prior data and seeds.
- **Conditions:** the **measured** κ (from Fig. 4d's crack-index misses, with its interval) is primary; κ = 0 and κ = 1
  bracket it.
- **Robustness:** decisions and acceleration factors are recomputed with every step cost moved by ±50 %.
- **Model check before campaign 2:** on campaign 1 data, the network must predict yield strength better than a
  GP from composition straight to yield strength (held-out log likelihood).
- **Primary endpoint:** spend to T, the first confirmed expansion of the in-house baseline front. Secondary: days to
  T; best margin over the front at the budget.
- **Analysis:** ≥ 20 seeds per policy and condition; acceleration factor = ratio of median spend to T;
  matched-seed bootstrap 90 % CI; seeds that never reach T are counted as censored, not dropped.
- **H1** is rejected if the median spend to T is not lower than full-chain network BO's, and separately than the
  best-form screen's, at the measured κ. **H2** is rejected if the acceleration factor at κ = 1 is not larger than
  at κ = 0.

## What gets reported regardless

The result is reported whatever it is: a tie or a loss to screening, a campaign that doesn't expand the front, and
baselines that miss their data sheets.

## Record

| Version | Commit | Date | Who approved |
|---|---|---|---|
| draft | (this file) | 2026-11-27 | — |
| draft, baselines changed to Al5X1 / Al-HS1 measured in-house | (this file) | 2026-11-27 | — |

## Deviations

None yet.
