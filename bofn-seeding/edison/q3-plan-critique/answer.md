## Bottom line

I would retain the mixed seed strategy and a **provisional 6–7-seed target**, but the draft does not yet justify either that exact count or a general IMSE-over-maximin recommendation. Its strongest point is the warning about delayed strength feedback.

## 1. Corrections to the draft

- **“[Bossek et al.] found that an initial design of about 30 % of the budget did best on their benchmark suite.”** Replace with: “They generally favored small initial designs, with substantial problem dependence.” Their [conclusion](https://doi.org/10.1145/3377930.3390155) does not establish a general 30% optimum.
- **“Keep the three-way mix, but use about 6–7 seeds rather than 9.”** The proposed schedule still has **eight pre-optimizer runs**: D1, D2, B30, B15, S1–S4. Including D1-r and four finalist runs leaves exactly 12 optimizer runs. Identify which slot is removed/merged; relabeling dosing checks does not release budget. The toy instead gives *all* nonseed runs to optimization, without these reservations.
- **“Maximin sends every point to a corner.”** Change to “Maximin selected boundary-heavy points in this pool and metric.” Likewise, “hardest ... to melt, dose and print” is an untested feasibility judgment, not an output of the comparison.
- **“Each element one alloy has and the other doesn't adds 0.5 to the distance.”** It adds **0.25 to squared distance**. This distinction materially affects interpreting the exclusion radius.
- **“Exclusion starts to matter once the existing set is large: literature points, or a dense CALPHAD screen.”** A screen is a *candidate pool*, not observed coverage. Only genuinely available observations, with appropriate noise/fidelity, should count as existing information.

## 2. Code audit and executed checks

I reproduced `space_filling_compare.csv` to its reported precision and completed the full **30-replicate × two-scenario × eight-policy** budget rerun.

| Method | Mean nearest distance ↓ | Fill distance ↓ | Mean posterior variance ↓ |
|---|---:|---:|---:|
| Sobol | 1.0290 | 1.8104 | 0.9277 |
| Maximin | 1.1056 | **1.7153** | 0.9548 |
| IMSE | **0.9550** | 1.7595 | **0.8950** |

**`seed_design.py`:**

- **Scaling is a modeling assumption.** Dividing by caps equates the full Ti range (0.5 wt%) with the full Si range (12 wt%). That is not automatically the campaign GP’s geometry: it assumes fixed bounds, equal length scales, and the additional presence features. Descriptor mode uses dataset-wide min–max scaling; freeze those bounds, handle correlated descriptors, and retain composition information where descriptors are insufficient.
- **The element-set term double-counts identity** relative to composition coordinates and jumps at *any* positive concentration. Trace impurities in measured compositions could switch every element “on.” Use a declared intentional-addition/detection threshold and test weights including zero. With weight 0.5, any different support already has distance ≥0.5: the default exclusion radius mostly tests same-support alloys. Seed-0’s pool actually contains **130 candidates** within radius 0.5 of existing points; exclusion is not intrinsically inactive, just inactive for the first selections.
- **The ≥3 wt% filter is unjustified as a strength screen.** It excludes lean precipitation-strengthened candidates—the goal includes reducing mineral burden. Remove it or demonstrate sensitivity. The reference measure also favors three-addition faces: 7,172 of 11,136 default candidates have three additions. “Average coverage” means coverage under this chosen face-sampling distribution, not uniform coverage of all plausible alloys.
- **IMSE algebra checks out** against direct posterior-variance reduction. But it assumes a noiseless, unit-amplitude radial-basis-function GP with fixed isotropic length scale 0.5. Treating *planned* seeds as noiseless observations is optimistic if they fail or remain unmeasured. Include observation noise and node-specific availability. My three-scramble checks retained IMSE’s average-coverage advantage at length scales 0.25, 0.5 and 1, and after removing the set penalty or total-addition cutoff; that is useful sensitivity evidence, not strength-performance validation.
- Rerun with **two** space-filling additions, changed B15, and actual S1/S2: the reported comparison uses three additions around the old five-row `seeds.csv`.

**`budget_split_sim.py`:**

- NumPy problems are paired, but **PyTorch acquisition sampling/fitting is not seeded**. My rerun gave 2+3+1 minus 3+3+3 = **+0.0479 ± 0.0164**, using one standard error across 30 problem clusters. Direction reproduced; exact supplied values did not. The two scenarios reuse the same 30 problems, so they are **not 60 independent instances**; cluster by problem when combining them.
- Baselines all cluster around **one** known bump—not distinct AlSi10Mg and Scalmalloy families. “Agent right” knows the optimum center and active dimensions; “wrong” merely revisits a good family, rather than proposing poor/unprintable alloys. This favors the claim that mistaken agents cost little.
- “Beat baseline” uses the best of **two versus three** baseline points, changing the threshold between policies. Use one fixed reference. “All 25 Sobol” is actually **two baselines + 23 Sobol**; rename it or implement the label.
- `unique=True` prevents duplication **within a batch only**. The pool is never depleted and previous observations are not excluded; my diagnostic found one cross-batch repeat. Explicitly permit/budget replication or exclude observed points. Log rather than suppress GP-fitting failures.
- Discrete-pool qLogEI is a reasonable **controlled flat-BO toy**, not a BOFN/p-KGFN surrogate. Seeds can lie off-pool; the optimizer cannot. Check larger pools or continuous optimization, noisy expected improvement, and especially delayed/partial feedback, feasibility and reserved confirmation runs. No seven-seed policy, IMSE seed policy, or maximin seed policy is tested here.

## 3. Is the disagreement resolved?

**Only conditionally.** IMSE wins the average-error criterion it targets; maximin wins the reported worst-case fill distance. Neither demonstrates better optimization. IMSE needs declared kernel hyperparameters, not a fitted GP. Boundary attraction is expected when maximizing separation, not an implementation bug.

I would prefer maximin when kernel length scales or reference-density weights are unreliable, when rare alloy families and worst-case coverage matter, or after a credible manufacturability screen removes unsafe extremes. A useful compromise is IMSE with a minimum-distance constraint, selected over a **physically reachable** pool. Do not let an equilibrium-only CALPHAD cutoff discard the supersaturated/metastable mechanisms being sought.

## 4. Proposed alloys and feedstock

**D1/D2 are sensible process-matched controls.** Commercial powder and wrought 6063 are valuable but cannot replace controls through the campaign’s own atomization/printing route. Keep B30 and an element-specific B15 only if they resolve separate, consequential dosing uncertainties.

**S1 is a defensible mechanism probe, not a demonstrated winner:** its [reported 284 MPa yield strength](https://doi.org/10.1016/j.jallcom.2021.163156) overlaps the draft’s AlSi10Mg range and is below aged Scalmalloy. Its nucleation strategy also overlaps D2; Mn supersaturation is the important distinction.

**S2 needs a substantive correction.** The quoted **376 MPa yield strength** comes from [Li et al.](https://doi.org/10.1080/17452759.2025.2516663), whose measured printed alloy is **Al–1.87Fe–1.02Mg–1.03Zr**, not Al–(3–5)Fe–1Mg–(0.5–0.7)Zr. Those are different hypotheses. Use the documented chemistry or explicitly withdraw the property attribution. Al–10Ce is not automatically a better fallback: it violates the Ce cap, carries 10 wt% listed critical additions, and lacks a compelling room-temperature strength advantage as presented.

The Zr/Fe/Ce procurement warning is sound, but a purchase order is insufficient: establish delivery, carrier composition, dissolution time/temperature, recovery, and contamination. **Mass-balance the 6063 cups and master-alloy carriers**; nominally pure-Al candidates may be unreachable. Verify bulk chemistry, powder size/yield and oxygen before claiming literature transfer.

**Review choices:**
- I treated the attachments as the schedule authority; I did not verify the linked private issues.
- I clustered uncertainty by independent synthetic problem and distinguished prediction coverage from optimization performance.

[Executed checks, rerun tables, code and saved references](review_checks/review_evidence.zip).

## 5. Prioritized changes before Dec 18

1. **Freeze success criteria:** yield versus ultimate strength, matched heat treatment/orientation, minimum ductility/density, and uncertainty-aware superiority. Define a dated mineral metric explicitly excluding/including Al; Sc-free is not synonymous with low burden.
2. **Fix the 25-run ledger and S2 attribution**, then commit to purchasable, reachable recipes. Consider a low-Sc bridge seed if matching aged Scalmalloy is central; zero-Sc and D2 alone weakly resolve that trade-off.
3. **Write a node-by-date data-availability contract.** Seed tensile results arrive Jan 19–22, not when bars print. Advance a sentinel tensile test if possible; otherwise label the first two batches as prior-driven for strength, while incorporating measured upstream evidence and pending evaluations.
4. **Freeze the executable optimization protocol:** objective, constraints, source-specific noise/fidelity, failures, pending points, repeats, and common seeds/budgets for policy comparisons. Dry-run the entire ingestion-to-batch pipeline.
5. **Rerun seed selection on the final screened pool**, with actual seeds, two additions, declared scaling/reference weights, and sensitivity checks—not the present default demonstration.
