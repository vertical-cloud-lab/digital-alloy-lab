# Independent review of the copper benchmark

**Full report:** [outputs/report.md](outputs/report.md)  
**Reproducibility:** [Python script](outputs/audit_reproduce.py) · [Notebook](outputs/audit_notebook.ipynb)

## Verdict

I reconstructed the JSON results independently, before examining `analyze.py`. **The stored results support network-aware full-pipeline BOFN over the supplied baselines in this synthetic benchmark; they do not establish that choosing which stage to purchase beats running the full chain.**

At \((\kappa,\eta)=(1,1)\), the best validated objective after $100,000 averages:

- **Full-pipeline BOFN: 73.212%** of the optimum, 20 seeds.
- **BOFN with lot reuse: 72.033%**, 20 seeds.
- **Production-setting pKGFN: 58.856%**, seven completed seeds.
- **Light-setting pKGFN: 58.552%**, 20 seeds.
- **Corrosion-informed tiered screening: 24.233%**, 20 seeds.
- **Standard BO: 14.421%**, 20 seeds.

The reported means reproduce. Important corrections concern standard errors, the interpretation of matched bootstrap intervals, fidelity conclusions, and causal wording.

I read `settings.md` first. I used the exact optimum **0.492187251856002** from `truth_tables.json`, not the rounded settings value. I independently processed **149 main-result JSONs, 30 light-setting JSONs, and 80 no-gate JSONs**. No Bayesian-optimization searches or Gaussian-process fits were rerun.

## A. Severity-ranked discrepancies and findings

| Severity | Finding | Evidence and correction |
|---|---|---|
| **Changes the conclusion** | Stage selection does not establish an advantage over full-pipeline search | Production pKGFN reaches 58.856%, versus full BOFN 73.212%. On seven matched seeds, the difference is −28.511 points, nominal Wilcoxon p=0.046875, but not multiplicity-robust. |
| **Changes the conclusion** | “The lighter settings were not why pKGFN lags” is too categorical | High minus light on seven matched seeds is −5.337 points; paired-bootstrap 90% interval **−23.784 to +11.721**. Settings, anchoring and fallback fixes changed together. This is neither an equivalence test nor an isolated fidelity experiment. |
| **Changes the conclusion** | Production pKGFN’s matched speed-up interval describes a different sample estimator | Its **2.1164×** point uses seven method seeds and 20 reference-baseline seeds; its matched interval **0.8086–1.9879** uses seven versus seven. The corresponding matched point is **1.4077×**, not 2.1164×. |
| **Changes the conclusion** | The 17–20× speed-ups over spec tiered are scientifically uninformative | Their target is **−7.691%** of optimum. Even standard BO obtains 19.85×. Bootstrap upper limits of **397×** arise from flooring zero-cost method crossings at $250. |
| **Changes the conclusion** | The gate explanation is plausible but not exclusively identified | Removing the gate changes both objectives and adaptive policy choices. Only random search uses identical designs with and without the gate. The logs do not directly establish what the learned model inferred. |
| **Changes a number** | Standard errors are understated | `analyze.py` uses population SD (`ddof=0`) rather than sample SD. Production pKGFN’s displayed SE should be **11 rather than 10 at $50k**, and **12 rather than 11 at $100k**. Single-seed “±0” is not an estimable between-seed error. |
| **Changes a number** | Runtime claim does not match stored `wall_s` | README says ~25–35 minutes/run and 2.9× light. Production files average **62.39 minutes**, range **32.66–83.51**; matched light averages **11.23 minutes**, a ratio of **5.56**. Hardware/load comparability is unknown. |
| **Changes a number** | A present policy is omitted from the spec-tiered speed-up table | `tiered_ni_ref` reaches spec tiered’s target at **$9,000**, giving **11.0278×**; independent CI **5.0253–397**, matched CI **7.2182–14.1786**. The default table-kind list excludes it. |
| **Changes a number / interpretation** | Production pKGFN’s endpoint is unusually sensitive to final-budget validation | Its mean rises from **46.214% at $99,750** to **58.856% at $100,000**, owing to three late validations. This is legitimate step-function accounting, not an aggregation error. |
| **Changes the conclusion** | Sensitivity and new-policy evidence is insufficient | No runs exist for (1,0), (0,1), `pkgfn_screen`, `pkgfn_audit`, `mines_only` or `funnel`. At (0,0), BOFN variants have only one seed each. |
| **Cosmetic / potentially misleading** | Proposal figure uses light pKGFN and ambiguous “Partial” labels | The uploaded original PNG is light pKGFN, n=20. BOFN + reuse tests every purchased Mines build downstream; it does not select arbitrary stages. Selective bands are unlabeled ±SE. |
| **Cosmetic / potentially misleading** | Small-figure readability and axes | Only endpoint ticks; no zero line. At 3.1 inches wide, 24-point source labels become ~6.8 points and the actual data axes occupy ~1.64 inches. |
| **Verified; no discrepancy** | Core numerical aggregation is internally consistent | Independent and supplied `best_validated` curves match **exactly**. Regenerating `tables.md` gives **zero differing lines** under the supplied conventions. Means, medians, listed ratios, bootstrap results, Wilcoxon tests and purchase counts reproduce. |

I distinguish genuine disagreements from rounding. For example, 37.857 Mines sessions becomes 37.9; the stored floating-point formatting prints the Ni-tiered immersion mean of 2.550 as 2.5 and reference-tiered hard-pass mean of 2.650 as 2.6. These do not indicate different underlying counts.

## B. Independent headline reconstruction — executed

I constructed a right-continuous step function on the requested $250 grid, taking the last row with `spent <= grid point`, applying the running maximum, and dividing by the exact cell optimum. Each actual run includes the initial shared-data row at $0.

### Means and standard errors, alongside the supplied table

Values are percentages of optimum. **My SE uses sample SD divided by √n**; supplied SE uses population SD divided by √n. The supplied values below occur in both `tables.md` and README’s headline tables.

| Policy | n | My $25k | Supplied $25k | My $50k | Supplied $50k | My $100k | Supplied $100k |
|---|---|---|---|---|---|---|---|
| pKGFN, production | 7 | 3.341 ± 5.433 | 3 ± 5 | 24.572 ± 11.109 | 25 ± 10 | 58.856 ± 12.208 | 59 ± 11 |
| pKGFN, light | 20 | 11.951 ± 6.559 | 12 ± 6 | 27.440 ± 7.385 | 27 ± 7 | 58.552 ± 4.844 | 59 ± 5 |
| BOFN, full | 20 | 14.977 ± 5.745 | 15 ± 6 | 38.774 ± 9.116 | 39 ± 9 | 73.212 ± 7.322 | 73 ± 7 |
| BOFN + reuse | 20 | 14.353 ± 4.702 | 14 ± 5 | 32.274 ± 7.805 | 32 ± 8 | 72.033 ± 7.046 | 72 ± 7 |
| Tiered, spec | 20 | −9.427 ± 5.500 | −9 ± 5 | −9.106 ± 5.473 | −9 ± 5 | −7.691 ± 5.366 | −8 ± 5 |
| Tiered, Ni floor | 20 | −6.644 ± 5.497 | −7 ± 5 | 0.762 ± 5.537 | 1 ± 5 | 10.217 ± 6.382 | 10 ± 6 |
| Tiered, Ni + reference | 20 | 7.858 ± 4.225 | 8 ± 4 | 16.136 ± 3.960 | 16 ± 4 | 24.233 ± 4.750 | 24 ± 5 |
| Standard BO | 20 | 5.680 ± 3.413 | 6 ± 3 | 7.180 ± 3.299 | 7 ± 3 | 14.421 ± 6.256 | 14 ± 6 |
| Random | 20 | −0.612 ± 4.532 | −1 ± 4 | 6.904 ± 4.977 | 7 ± 5 | 22.293 ± 5.024 | 22 ± 5 |

Every displayed SE correction in this headline table is:

- Production pKGFN: $50k **10→11**, $100k **11→12**.
- Light pKGFN: $25k **6→7**.
- Spec tiered: $25k **5→6**.
- Ni-floor tiered: $50k **5→6**.
- Random: $25k **4→5**.

All nonzero unrounded SEs change, even where integer rounding hides it: the correction factors are √(7/6)=**1.0801** and √(20/19)=**1.0260**. Every unrounded comparison is saved in [all_SE_comparisons.csv](outputs/all_SE_comparisons.csv).

For completeness, README’s alternate `rec_printed` table has additional displayed SE corrections: production pKGFN **10→11, 12→13, 6→7** at $25k/$50k/$100k; light pKGFN $100k **4→5**; random $25k **4→5**. The recommendation means reproduce. `rec_printed` is not the requested demonstrated-build metric.

### Median per-seed spend to reach thresholds

A seed that never crosses contributes infinity. These medians agree with every supplied rounded median and attainment percentage.

| Policy | 60% median; seeds reaching | 70% median; seeds reaching | 80% median; seeds reaching |
|---|---|---|---|
| pKGFN, production | **$100,000; 4/7** | >$100k; 3/7 | >$100k; 2/7 |
| pKGFN, light | **$85,500; 12/20** | >$100k; 7/20 | >$100k; 1/20 |
| BOFN, full | **$66,750; 17/20** | **$73,875; 15/20** | **$88,125; 14/20** |
| BOFN + reuse | **$54,375; 17/20** | **$64,625; 17/20** | **$80,625; 13/20** |
| Tiered, spec | >$100k; 0/20 | >$100k; 0/20 | >$100k; 0/20 |
| Tiered, Ni floor | >$100k; 0/20 | >$100k; 0/20 | >$100k; 0/20 |
| Tiered, Ni + reference | >$100k; 2/20 | >$100k; 0/20 | >$100k; 0/20 |
| Standard BO | >$100k; 3/20 | >$100k; 1/20 | >$100k; 1/20 |
| Random | >$100k; 1/20 | >$100k; 0/20 | >$100k; 0/20 |

The production pKGFN median of $100k is an actual grid crossing, not an extrapolation. Medians can lie between grid points when averaging the two middle seeds.

### Speed-ups and bootstrap intervals

I reproduced the supplied estimator and its **2,000-replicate, random-seed-0** independent and matched seed bootstraps. Each replicate resets the target to the resampled baseline’s final mean. These exact results round to the supplied table entries.

**Spec-tiered baseline:** target **−7.690822%**, baseline first reaches it at **$99,250**.

| Method | Method first crossing | Ratio | 90% independent CI | 90% matched CI | Bootstrap fraction ≥3 |
|---|---|---|---|---|---|
| pKGFN, production | $5,750 | 17.2609 | 2.7192–397.0000 | 11.5263–20.7895 | 0.9485 |
| pKGFN, light | $5,750 | 17.2609 | 5.7536–397.0000 | 11.9697–21.9444 | 0.9885 |
| BOFN, full | $5,000 | 19.8500 | 18.3500–397.0000 | 18.3500–19.8500 | 0.9925 |
| BOFN + reuse | $5,000 | 19.8500 | 10.9500–397.0000 | 18.3500–43.8889 | 0.9955 |
| Tiered, Ni floor | $23,250 | 4.2688 | 1.1507–397.0000 | 2.6829–7.2182 | 0.5535 |
| Tiered, Ni + reference | $9,000 | 11.0278 | 5.0253–397.0000 | 7.2182–14.1786 | 0.9870 |
| Standard BO | $5,000 | 19.8500 | 5.1558–397.0000 | 18.3500–19.8500 | 0.9760 |
| Random | $9,750 | 10.1795 | 2.3081–397.0000 | 9.4103–19.8500 | 0.8690 |

**Corrosion-informed `tiered_ni_ref` baseline:** target **24.233129%**, baseline first reaches it at **$100,000**.

| Method | Method first crossing | Ratio | 90% independent CI | 90% matched CI | Bootstrap fraction ≥3 |
|---|---|---|---|---|---|
| pKGFN, production | $47,250 | **2.1164** | **0.8766–2.4242** | **0.8086–1.9879** | 0.0065 |
| pKGFN, light | $46,750 | **2.1390** | 1.4933–3.9176 | 1.4936–3.5088 | 0.1155 |
| BOFN, full | $33,500 | **2.9851** | **1.6560–4.1667** | **1.6571–3.4783** | 0.1560 |
| BOFN + reuse | $35,250 | **2.8369** | 1.6571–4.0941 | 1.6812–3.9216 | 0.3790 |
| Tiered, spec | Not reached | 0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000 |
| Tiered, Ni floor | Not reached | 0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000 |
| Standard BO | Not reached | 0.0000 | 0.0000–1.0000 | 0.0000–0.0000 | 0.0000 |
| Random | Not reached | 0.0000 | 0.0000–1.6129 | 0.0000–1.6129 | 0.0000 |

“0×” is the implementation’s encoding of a non-crossing method, not a measured physical speed-up.

**Important matched-sample correction.** Production pKGFN’s seven common seeds are **0,1,2,3,4,5,7**. On those seeds, reference tiered ends at **27.8146%**, first reaches that mean at **$82,000**, and pKGFN reaches it at **$58,250**. Thus the matched point estimate is:

\[
82{,}000/58{,}250=1.4077,
\]

with the supplied matched interval **0.8086–1.9879**. The mixed-sample point of 2.1164 and this matched interval should not be described as an estimate and interval of the same sample estimator. The independent production-pKGFN interval also includes 1, so its spend advantage is not established at that confidence level.

**The negative-target speed-up is not meaningful alloy-search acceleration.** Independent resamples can place the baseline target below a method’s starting value, yielding a zero-cost crossing. `_ratio` floors that cost at $250, generating the finite 397× upper percentile. A separate 20,000-replicate bootstrap with literal zero-cost crossings has an infinite upper percentile. Neither result should be quoted as useful experimental acceleration.

### Wilcoxon tests: production pKGFN against every other present policy

All comparisons use seven matched seeds. Entries are **mean difference in percentage points; wins/ties/losses; two-sided p**. They reproduce all requested supplied tests.

| Production pKGFN minus… | $25k | $50k | $100k |
|---|---|---|---|
| Light pKGFN | −11.323; 3/0/4; 0.578125 | −2.099; 3/0/4; 0.937500 | −5.337; 3/0/4; 0.687500 |
| Full BOFN | −20.507; 0/0/7; 0.015625 | −20.774; 1/0/6; 0.218750 | −28.511; 1/0/6; 0.046875 |
| BOFN + reuse | −14.007; 1/0/6; 0.109375 | −14.940; 2/0/5; 0.375000 | −3.053; 3/0/4; 0.812500 |
| Spec tiered | +16.650; 6/1/0; 0.031250 | +36.963; 7/0/0; 0.015625 | +69.290; 7/0/0; 0.015625 |
| Ni-floor tiered | +13.921; 5/1/1; 0.093750 | +30.181; 6/0/1; 0.046875 | +53.370; 7/0/0; 0.015625 |
| Ni + reference tiered | −6.759; 2/0/5; 0.468750 | +3.640; 5/0/2; 0.687500 | +31.041; 6/0/1; 0.046875 |
| Standard BO | −0.309; 2/1/4; 0.843750 | +20.041; 4/0/3; 0.218750 | +46.761; 5/0/2; 0.078125 |
| Random | +3.774; 4/1/2; 0.562500 | +21.813; 5/0/2; 0.156250 | +39.952; 6/0/1; 0.031250 |

### High fidelity versus light on matched seeds

At $100k:

| Policy, same seven seeds | Mean ± sample SE |
|---|---|
| Production pKGFN | **58.856 ± 12.208%** |
| Light pKGFN | **64.192 ± 4.671%** |
| Full BOFN | **87.367 ± 3.878%** |

The production-minus-light paired difference is **−5.337 points**, p=**0.6875**, 3/0/4 wins/ties/losses. A 50,000-draw paired-seed bootstrap gives a 90% interval **−23.784 to +11.721 points**. This does not establish equivalence or rule out a practically relevant fidelity effect.

The matched-light README row should display sample SE **±11, ±12, ±5**, rather than **±10, ±12, ±4**, at $25k/$50k/$100k; exact means are **14.664%, 26.671%, 64.192%**. Fidelity, F2 anchoring/deduplication and F4 fallback fixes changed together, so their effects cannot be separated.

## C. `curve`, `cost_to`, seed matching — executed and inspected

I executed an adversarial five-row example at spends $500, $1,000 twice, $100,000 and $100,010.

| Check | Executed result |
|---|---|
| Before first row | `curve` returns **NaN** at $0 and $250 |
| First row | Value **0.2** at $500 and $750 |
| Duplicate-spend rows | Value **0.3** at exactly $1,000: last row at that spend, with running maximum |
| Last pre-budget point | Value **0.3** at $99,750 |
| Exactly $100k | Value **0.4**: the $100,000 row is included |
| Post-budget row | $100,010 value is excluded |
| `cost_to` for targets 0.2/0.3/0.4/0.5 | **$500 / $1,000 / $100,000 / infinity** |

This is the correct right-continuous construction. Actual logs all start at $0, so pre-first-row behavior is not exercised by the benchmark. I found **no stored decreases** in `best_validated`; every independent curve equals the supplied curve exactly.

`rec_printed` deliberately does **not** receive a running maximum: it is the current model’s recommendation rather than the historical demonstrated best. Mean-curve `first_cost` uses a 1e−12 tolerance, whereas per-seed `cost_to` uses strict comparison. This produced no printed benchmark discrepancy.

I tested shuffled seed lists `[7,0,2]` and `[2,3,7]`: `matched_idx` correctly pairs **(2,2), (7,7)**. Both it and `paired` match explicit seed IDs, not row positions. Actual seed keys are unique. The seed-matching implementation is correct; the estimand change in the matched bootstrap remains important.

## D. Statistical methodology and target sensitivity

### Fixed-target first crossings — executed

These are first crossings of the **mean curve**, not medians of seed-specific crossing costs.

| Policy | 55% optimum | 60% optimum | 65% optimum |
|---|---|---|---|
| Production pKGFN | **$100,000** | Not reached | Not reached |
| Light pKGFN | **$100,000** | Not reached | Not reached |
| Full BOFN | **$76,250** | **$85,750** | **$85,750** |
| BOFN + reuse | **$65,750** | **$71,000** | **$81,000** |
| Spec tiered | Not reached | Not reached | Not reached |
| Ni-floor tiered | Not reached | Not reached | Not reached |
| Ni + reference tiered | Not reached | Not reached | Not reached |
| Standard BO | Not reached | Not reached | Not reached |
| Random | Not reached | Not reached | Not reached |

Thus the apparent speed-up depends strongly on whether the target is −7.69%, 24.23%, or a useful 55–65%. Neither tiered baseline reaches 55–65%, so a finite ratio at those targets cannot be estimated within this budget. Production pKGFN’s **mean** never reaches 60%, despite a **median seed-specific** 60% cost of $100k. These are different summaries.

### Bootstrap interpretation

The supplied bootstrap correctly resamples whole seeds. However:

- A baseline’s own final mean is a random, data-dependent target, not an externally fixed performance goal.
- First-crossing estimators are discrete and non-smooth; no crossings, zero-cost crossings and terminal-budget jumps complicate percentile intervals.
- The $250 denominator floor hides zero-cost cases rather than resolving their interpretation.
- Matched bootstrap intervals must accompany matched-sample points and targets.
- Intervals describe variability conditional on this simulator and observed seeds. They do not account for omitted/uncompleted production runs, model calibration or physical generalization.
- “P(speed-up ≥3)” is a **bootstrap fraction**, not a posterior probability that the true effect exceeds threefold.

For full BOFN versus reference tiered, the point estimate rounds to 3.0×, but its independent 90% interval is **1.656–4.167** and only **15.6%** of supplied bootstrap replicates exceed 3. The data support a useful spend advantage at this low reference target, not a demonstrated minimum threefold advantage.

### Multiple comparisons — executed

There are **24 requested pKGFN tests**: eight rivals × three budgets. Holm correction over that family gives a minimum adjusted p of **0.375**. The production-pKGFN-versus-full-BOFN $100k p becomes **0.84375**. None of these should be presented as multiplicity-robust confirmatory significance.

The broader BOFN finding is stronger: full BOFN versus reference tiered at $100k has **+48.979 points, 17/0/3, p=0.000322** across 20 matched seeds. Even a conservative Holm correction over **108 all-policy, all-budget comparisons** gives **0.0274**. I report both families because the appropriate family should follow a prespecified scientific question, not the most favorable correction.

### Wording

The README’s claim that the aluminum headline does not carry over is fair **for this implementation and these stored runs**. Its categorical attribution to “the immersion gate,” and claim that the model learns the stated mechanism, are stronger than the intervention identifies.

The no-gate ablation is informative but compound for adaptive policies. Synthetic hand-chosen functions, noiseless observations, a deposit-quality index that is not literal relative density, and a reference-coupon screen value supplied by the truth limit physical interpretation. The one-hour screen does **not** exclude the optimum; the CALPHAD screen does, as the README itself notes.

**Most defensible preliminary-results sentence:**

> In a synthetic, deliberately biased copper directed-energy-deposition benchmark, full-pipeline function-network Bayesian optimization demonstrated alloys averaging 73% of the modeled optimum after $100,000 of new purchases (20 seeds), versus 24% for corrosion-informed tiered screening (20 seeds) and 14% for standard Bayesian optimization (20 seeds); a seven-seed production-setting partial-stage knowledge-gradient implementation averaged 59% and did not establish an advantage over full-pipeline search.

## E. Figure audit — actual raster read; plotting code inspected

The uploaded `bofn_cu_best_vs_spend_k1_partial_vs_full.png` contains **light pKGFN, n=20**, not production pKGFN. Its traces agree with the corresponding reconstructed curves. Raster readings are approximate, generally within ~0.6 percentage point.

| Uploaded trace | Visual ~25k / 50k / 100k | Exact reconstructed 25k / 50k / 100k |
|---|---|---|
| Solid red “Partial: pKGFN” | ~12 / 27 / 59 | **11.951 / 27.440 / 58.552** |
| Dashed red “Partial: BOFN + reuse” | ~14 / 32 / 72 | **14.353 / 32.274 / 72.033** |
| Dark “Full: BOFN” | ~15 / 39 / 73 | **14.977 / 38.774 / 73.212** |
| Light gray “Full: standard BO” | ~6 / 7 / 14 | **5.680 / 7.180 / 14.421** |
| Gray “Tiered screening” | ~−9 / −9 / −8 | **−9.427 / −9.106 / −7.691** |

The original figure’s common start is **−9.610%**, shown as −10. The separate current-production figure starts at **−13.831%** for its seven pKGFN seeds, shown as −14; initial values match across policies on common seed IDs, so this is a sample-composition difference.

**There is no called-out spend or horizontal target level in the uploaded original PNG.** The plotting code disables the callout for this uninformative negative-valued baseline. The unplotted spec-tiered comparison would use **$5,750 at −7.691%** for light pKGFN versus **$99,250** for spec tiered. With the reference baseline, the light-pKGFN crossing is **$46,750 at +24.233%** versus **$100,000**; production pKGFN’s corresponding crossing is **$47,250**.

At **3.1 inches wide**, I would change the presentation:

- Identify pKGFN’s **settings and seed count**; do not attach the new seven-seed claim to the old 20-seed curve.
- Replace “Partial: BOFN + reuse” with an explicit **lot-reuse** label. Every new Mines build receives downstream tests; this differs fundamentally from stage selection.
- State that ribbons are **±one SE**, not 90% confidence bands, and make uncertainty treatment consistent. Full BOFN and standard BO currently have no ribbons, which can suggest false certainty.
- Add a visible **0% line** and intermediate spend ticks. Only −10/73 and 0/100 are currently labeled.
- Increase contrast of standard BO and tiered traces.
- Reduce label width: the 11-inch source figure’s 24-point labels shrink to ~6.8 points, and the data axes use only ~1.64 inches at final width.

If the proposal quotes the corrosion-informed ~3× result, its figure should show that comparator, not the old spec-tiered rule.

## F. Purchase behavior and pathologies — executed

I reconciled **all 179 main/light ledgers exactly** against stage counts, final inventory capacity, the five pre-existing seed lots and $1,600 paid scale-ups supporting four sessions. Every new-build count equals Mines purchases; completed stage fields agree with S/T/K/I counts. The supplied purchase table reproduces at its one-decimal precision.

C=CALPHAD; A=atomization; U=Utah deposition; M=Mines deposition; S=microscopy; T=tensile; K=one-hour screen; I=immersion. All counts below exclude the shared five seed builds/lots.

| Policy | C | A | U | M | S | T | K | I | Fully validated new builds | Paid scale-ups |
|---|---|---|---|---|---|---|---|---|---|---|
| Production pKGFN | 4.57 | 17.57 | 16.29 | 37.86 | 13.43 | 5.86 | 11.86 | 11.29 | **5.29** | 12.71 |
| Light pKGFN | 6.70 | 12.45 | 11.30 | 40.50 | 15.70 | 7.20 | 14.00 | 12.85 | **6.15** | 12.30 |
| Full BOFN | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | **21.00** | 21.00 |
| BOFN + reuse | 12.55 | 12.55 | 12.55 | 29.30 | 29.30 | 29.30 | 29.30 | 29.30 | **29.30** | 13.40 |
| Spec tiered | 224.00 | 22.80 | 44.25 | 24.85 | 24.85 | 24.85 | 24.85 | 4.00 | **4.00** | 11.00 |
| Ni-floor tiered | 224.00 | 31.00 | 67.40 | 18.35 | 18.35 | 18.35 | 18.35 | 2.55 | **2.55** | 9.75 |
| Ni + reference tiered | 224.00 | 26.50 | 53.65 | 21.15 | 21.15 | 21.15 | 21.15 | 9.90 | **9.90** | 10.10 |
| Standard BO | 19.70 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | **21.00** | 21.00 |
| Random | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | **21.00** | 21.00 |

### What the policies bought

- Full BOFN, standard BO and random purchase ~21 complete chains. Standard BO saves some CALPHAD calls on known compositions.
- BOFN reuse purchases fewer new lots but **29.3 fully tested Mines builds**.
- Tiered policies spend heavily on CALPHAD/Utah screening. Ni-floor tiered has only **2.55 immersions/run**; changing the one-hour gate to the reference gives **9.9 immersions**, **2.65 hard immersion passes**, and 24.233% final validated objective.
- Production pKGFN deposits **37.86** new builds but validates **5.29**. Its **5.86 tensile tests and 11.29 immersions are often on different builds**; buying both test types does not imply that both were completed on each build.

### Repetition, budgets and stalls

- I found **no duplicate exact stored builds or Utah sessions** in main/light runs.
- One standard-BO run, **seed 19**, repeats a serialized lot at composition `(0,0,1,0)` and atomizer setting `0`—lot indices 14 and 20. It does not repeat a complete stored build. Other repeated sessions are intentional reuse at different settings.
- Identity checks are limited by stored four-decimal composition coordinates; they do not prove equality at unlimited floating precision.
- Every headline run ends between **$97,790 and $100,000**. There is no current run ending far below budget.
- No improvement from the shared initial validated best occurs in **15/20 spec-tiered**, **11/20 Ni-tiered**, **3/20 reference-tiered**, and **4/20 random** runs.
- Production pKGFN has a contiguous no-improvement block costing up to **$77,900**, seed 2.
- Defining a cheap action as costing ≤$500, production pKGFN has up to **10 consecutive cheap, no-improvement actions costing $3,510**, seed 5. Light pKGFN has **20 costing $5,570**, seed 15, and **16 costing $7,900**, seed 14.
- Production pKGFN’s last-grid jump is real: seeds **3,5,7** finalize gains of approximately **20.77, 48.01 and 19.70 points** between $99,750 and $100k. Their average produces the **12.642-point** jump in the seven-seed mean.

### Deposited but never completed

Production pKGFN averages **26.00 new builds with neither tensile nor immersion**, **32.00 without tensile**, and **26.57 without immersion**. Light averages 40.50 deposits but only 6.15 validated builds, including **26.60 with neither test**. Full BOFN validates all 21 new builds.

As an upper-bound diagnostic, I independently evaluated all stored deposited designs against the synthetic truth, including the seed builds. The unavailable-oracle best averages approximately **70.817%** for production pKGFN versus **58.856% demonstrated**, and **68.496%** for light versus **58.552% demonstrated**. Composition rounding makes these oracle reevaluations approximate. They are not prospective achievable policy outcomes.

### How often was KG flat?

| Production seed | Fallback / all actions | Fallback share | Spend on fallback | New validated / deposited |
|---|---|---|---|---|
| 0 | 1/86 | 1.2% | $100 | 4/44 |
| 1 | 68/97 | 70.1% | $62,650 | 6/35 |
| 2 | 69/103 | 67.0% | $67,750 | 3/32 |
| 3 | 3/90 | 3.3% | $750 | 5/40 |
| 4 | 28/105 | 26.7% | $29,600 | 8/36 |
| 5 | 5/103 | 4.9% | $800 | 5/42 |
| 7 | 93/105 | 88.6% | $90,800 | 6/36 |

Production pKGFN has **267/689=38.75%** fallback-marked purchases and spends **36.08%** of its budget on them. Light has **418/1,944=21.50%**. The pooled headline quality row reproduces: **685/2,633=26.02%**, with **75,434 GP fits and zero recorded failures**.

Classifying each action by the state **before the purchase**:

- Production: fallback **255/383=66.6%** before the first demonstrated J>0, versus **12/306=3.9%** afterward.
- Light: **380/907=41.9%** before versus **38/1,037=3.7%** afterward.

The code marks fallback when estimated KG per dollar is below **1e−10**, or no eligible KG candidate remains. It then buys one action using path-priced expected improvement, or an optimistic posterior sample when EI is also zero. The flag does **not** distinguish those two fallback branches.

These flags indicate near-flat **numerically estimated, discretized acquisition values**, not proof that the mathematical knowledge gradient is exactly zero. They are consistent with myopic stage choice and delayed rewards: pricing the complete validation path while purchasing only its next step does not ensure later decisions finish that path.

## G. Sensitivities, new policies and no-gate results

### Available sensitivity results — executed

At (0,0), using optimum **0.381561510051002**:

| Policy | n | $25k | $50k | $100k |
|---|---|---|---|---|
| Light pKGFN | 10 | **−5.622 ± 4.724%** | **−0.356 ± 3.836%** | **9.373 ± 7.474%** |
| Full BOFN | 1 | **11.831%** | **19.487%** | **92.255%** |
| BOFN + reuse | 1 | **11.831%** | **67.672%** | **95.195%** |

The supplied rounded means reproduce. Light pKGFN’s displayed $25k sample SE should be **5**, not 4. The single-seed BOFN rows do **not** have estimable between-seed SEs; “±0” is misleading. Their medians are simply that one run’s threshold times.

There are **no stored results for (1,0) or (0,1)**, and no production pKGFN or other baselines at (0,0). The blank sensitivity cells genuinely mean missing evidence. These data cannot support robustness to screen bias or a comparison of the two bias mechanisms.

### New policies — inspected only; no outcome data

I enumerated every stored policy and found **no** `pkgfn_screen`, `pkgfn_audit`, `mines_only` or `funnel` JSONs. Therefore:

- The screen-audit result table has no empirical rows.
- The two-step DED split table is not rendered in `tables.md`.
- There is no fixed-funnel result table to validate.
- No result supports an audit benefit, a Utah-stage benefit, or fixed top-k funnel performance.

I inspected their code and descriptions only. Near-cutoff oversampling and using the final gate for the audit truth comparison remain methodological issues, but cannot be tested empirically without those runs. The S=256 fidelity experiment is also unavailable.

### No-gate supplement — executed

`compare/landscape.json` was not supplied. I transcribed the no-gate truth into NumPy and optimized it with three independent SciPy differential-evolution starts, obtaining **0.74505147885**. The 80 no-gate runs give:

| Policy | n | $25k | $50k | $100k |
|---|---|---|---|---|
| Standard BO | 20 | 38.946 ± 5.954% | 48.801 ± 5.529% | **65.156 ± 4.610%** |
| Full BOFN | 20 | 43.726 ± 6.110% | 66.782 ± 5.148% | **84.774 ± 4.853%** |
| BOFN + reuse | 20 | 47.117 ± 5.653% | 71.171 ± 3.539% | **87.555 ± 2.198%** |
| Random | 20 | 43.248 ± 4.543% | 47.334 ± 3.618% | **50.867 ± 3.300%** |

These reproduce README’s integer means and demonstrate strong gate sensitivity. I verified that the **26 random designs per seed are identical** with and without the gate; only random is a clean same-design rescoring. I did not re-execute the copper-versus-aluminum comparison because aluminum JSONs were not supplied here.

## H. Executed-versus-inspected verification record

| Requested check | Status | Evidence |
|---|---|---|
| Independent JSON curves, headline means/SEs/medians for every present policy | **Executed** | Independent code written before inspecting aggregator; exact supplied-curve agreement |
| Both baseline speed-ups, independent and matched bootstraps | **Executed** | Exact 2,000-replicate reproduction; separate 20,000-replicate sensitivity |
| All requested matched Wilcoxon tests and multiplicity sensitivity | **Executed** | 24 requested tests; 108 all-pair/budget tests |
| `curve`, `cost_to`, exact-$100k/pre-first-row behavior and shuffled seed matching | **Executed and inspected** | Adversarial boundary cases and explicit seed-ID tests |
| Compare against supplied `tables.md` | **Executed** | Regenerated table has **zero differing lines** under supplied conventions |
| README headline, fidelity, purchases and available sensitivity claims | **Executed and inspected** | Numerical comparisons above; all decimal-level SE comparisons saved |
| Figure traces, start and callout | **Actual raster read; code inspected** | Approximate raster readings checked against exact reconstructed arrays |
| Action counts, inventory costs, fallback, budgets, repetitions, unfinished builds | **Executed** | **179/179** main/light cost reconciliations exact |
| Available sensitivities and no-gate ablation | **Executed** | File inventories and reconstructed tables |
| Absent screen/audit/mines-only/funnel policies | **Inspected only** | No stored runs; no fabricated numerical conclusions |
| GP training, F2/F4 algorithmic correctness, physical calibration, new optimization runs | **Not re-executed** | This review evaluates stored results; it does not replace those experiments |

The saved [report.md](outputs/report.md) includes the full findings and tables. Numerical audit files include [independent_summary.csv](outputs/independent_summary.csv), [replicated_bootstrap.csv](outputs/replicated_bootstrap.csv), [independent_paired.csv](outputs/independent_paired.csv), [all_SE_comparisons.csv](outputs/all_SE_comparisons.csv), [action_audit_per_seed.csv](outputs/action_audit_per_seed.csv), and [inventory_cost_ledger.csv](outputs/inventory_cost_ledger.csv).

I also executed the saved reproduction script in a **fresh Python process: exit code 0, no stderr**, and verified that its generated report matched. Original benchmark inputs were unchanged.

### Discretionary analytical decisions

- I used the exact uploaded gated optima rather than re-optimizing the benchmark’s normalization; I independently reconstructed the missing no-gate optimum.
- I report **sample-SD standard errors**, preserving the supplied population-SD values side by side. Single-seed between-run SE is not estimable.
- I retain infinity for unreached threshold costs and distinguish literal zero-spend bootstrap crossings from the supplied $250 denominator floor.
- I report matched and independent estimators separately because the seven-versus-20 imbalance changes both the matched target and point estimate.
- I examine fixed **55%, 60%, 65%** targets rather than selecting only a favorable baseline-dependent target, and use Holm corrections as an exploratory multiplicity sensitivity check.
- I treat completed production seeds as a convenience subset, missing runs as unavailable evidence, and physical mechanisms as hypotheses rather than experimentally established explanations.
