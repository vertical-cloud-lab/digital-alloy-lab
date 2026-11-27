# analysis-review

Task 972ea3bf-1d45-4a7f-a695-a1e6e8504ed8 (job-futurehouse-data-analysis-crow-high), status success

## answer

# Independent audit of the synthetic-alloy BOFN benchmark

I saved the complete report as [outputs/report.md](outputs/report.md). I read `settings.md` first and recomputed the results from all 292 JSON runs **without importing or executing `analyze.py`**. I then inspected the supplied analysis, plotting and policy code and checked the figure against my independently computed curves. I used the optima in `settings.md`; I did not rerun the simulations or independently optimize the truth functions.

## Discrepancies and findings

| Severity | Finding | Evidence |
|---|---|---|
| **Changes the conclusion** | “Partial evaluation is what clears 3×” overstates the comparison. | At tiered screening’s final mean level, the point ratios are **3.755×** for pKGFN, **3.790×** for BOFN + powder reuse, **2.618×** for full BOFN and **2.140×** for standard BO. The full-BOFN 90% bootstrap interval extends *above* 3×, while both partial-policy intervals extend *below* it. The tiered comparator itself reuses powder. This is a conditional point-estimate contrast, not an isolated causal effect of partial evaluation. |
| **Changes the conclusion** | The speed-up depends strongly on the selected target and a small late tiered improvement. | Tiered screening’s mean is **62.614% at $95k**, just **0.089 percentage points** below its final **62.703%**. It first reaches that final level at **$99.5k**, nearly the budget limit. With a fixed **62.5%** target, the pKGFN ratio is **3.585×**; at **55%**, it is **2.411×**. A *perfectly flat* plateau would move first crossing to its start: the sensitivity here is to small late increments, not flatness alone. |
| **Changes the conclusion** | “pKGFN ... has the fastest start of any policy” is only a comparison of mean curves at $25k. | pKGFN is **62.003%**, versus **60.967%** for reuse. Across matched seeds the difference is **+1.036 points**, but pKGFN has **6 wins, 2 ties, 12 losses**; two-sided Wilcoxon **p=0.528**. |
| **Changes a number** | The headline bootstrap lower bound does not reproduce exactly. | My 2,000 independent arm-wise seed-0 resamples, following the inspected sampling order, give **[2.144, 5.657]**, or **2.1–5.7×** at one decimal; the README says **2.0–5.7×**. I cannot establish whether a different code/NumPy version, supplied-optimum rounding or another choice explains this boundary difference. |
| **Changes a number** | “About $26k” understates the defined pKGFN crossing slightly. | It first crosses the target at **$26,500** on the specified $250 grid. |
| **Changes a number** | “About six make–print–test cycles” at $25k describes cost equivalents, not pKGFN’s purchases. | By $25k it bought, on average, **0.20 CALPHAD runs, 1.35 atomizations, 8.40 prints and 2.90 tensile tests** beyond shared seed data. Seven of 20 seeds bought no new powder by then. |
| **Cosmetic / precision** | “19 of 20 seeds, Wilcoxon p = 1e-4” omits a tie and rounds the test result heavily. | There are **19 wins, one exact tie, zero losses**; the mean difference is **+21.135 percentage points**. The default SciPy two-sided test gives **p=0.000131834**. An exact signed-rank calculation *after excluding the zero difference* gives **p=3.81×10⁻⁶**; the convention should be specified. |
| **No table discrepancy** | The requested kappa=1 README table and the kappa=0/0.5 $100k tables reproduce at their published precision. | Exact independent estimates follow. |

## Kappa = 1: independent values alongside the README

Each parenthesis contains the README entry. Means and standard errors (SE) are percentages of the supplied optimum, **0.693739**, over 20 seeds. I used the README’s population-SD-divided-by-\(\sqrt{n}\) SE convention for direct comparability.

| Policy | $25k: recomputed (README) | $50k: recomputed (README) | $100k: recomputed (README) |
|---|---:|---:|---:|
| pKGFN | **62.003 ± 5.207** (62 ± 5) | **69.577 ± 3.451** (70 ± 3) | **83.837 ± 1.790** (84 ± 2) |
| BOFN + powder reuse | **60.967 ± 6.081** (61 ± 6) | **73.837 ± 5.055** (74 ± 5) | **89.953 ± 2.399** (90 ± 2) |
| BOFN, full pipeline | **50.068 ± 6.081** (50 ± 6) | **76.831 ± 4.567** (77 ± 5) | **85.751 ± 4.056** (86 ± 4) |
| Standard BO | **48.462 ± 6.751** (48 ± 7) | **63.229 ± 5.182** (63 ± 5) | **83.831 ± 2.751** (84 ± 3) |
| Tiered screening | **46.067 ± 4.973** (46 ± 5) | **55.943 ± 3.463** (56 ± 3) | **62.703 ± 2.250** (63 ± 2) |

Median crossing spend includes all 20 seeds: noncrossers count as not reaching the target by $100k, **not** as successful seeds omitted from the median.

| Policy | 60%: recomputed; reached (README) | 70%: recomputed; reached (README) | 80%: recomputed; reached (README) |
|---|---|---|---|
| pKGFN | **$15,125; 19/20** ($15k; 95%) | **$25,375; 19/20** ($25k; 95%) | **$85,875; 15/20** ($86k; 75%) |
| BOFN + reuse | **$18,750; 20/20** ($19k; 100%) | **$25,500; 18/20** ($26k; 90%) | **$52,375; 17/20** ($52k; 85%) |
| BOFN full | **$31,625; 18/20** ($32k; 90%) | **$35,875; 17/20** ($36k; 85%) | **$42,250; 16/20** ($42k; 80%) |
| Standard BO | **$40,125; 19/20** ($40k; 95%) | **$46,500; 17/20** ($46k; 85%) | **$59,000; 14/20** ($59k; 70%) |
| Tiered | **$55,750; 12/20** ($56k; 60%) | **>$100k; 3/20** (>$100k; 15%) | **>$100k; 2/20** (>$100k; 10%) |

The README’s $46k for a $46.5k median, and $26k for $25.5k, follow Python’s ties-to-even formatting. They are formatting choices, not computation errors.

For the **four speed-ups over tiered screening**, I used its own $100k mean, **62.702686%**, as the common target. The intervals use 2,000 independent seed resamples per policy, resetting the NumPy seed-0 generator for each comparison; bounds are the 5th and 95th percentiles.

| Method | Tiered crossing | Method crossing | Recomputed ratio and 90% bootstrap interval | README |
|---|---:|---:|---|---|
| pKGFN | $99,500 | $26,500 | **3.755× [2.144, 5.657]** | 3.8× [2.0, 5.7] |
| BOFN + reuse | $99,500 | $26,250 | **3.790× [2.222, 5.940]** | 3.8× [2.2, 5.9] |
| BOFN full | $99,500 | $38,000 | **2.618× [2.140, 3.902]** | 2.6× [2.1, 3.9] |
| Standard BO | $99,500 | $46,500 | **2.140× [1.467, 2.948]** | 2.1× [1.5, 2.9] |

## Curve and statistical methodology

**Executed:** I constructed each grid curve by walking forward through its JSON actions, carrying forward the running maximum of `best_validated`. I separately executed a literal independent equivalent of the inspected `analyze.curve()` expression. They agree at **all 401 grid positions in all 292 runs**. All runs begin at $0, have strictly increasing recorded spend and have finite validated scores. `searchsorted(..., side="right") - 1` includes the purchase *at* a grid point and selects the last row if multiple purchases share its spend; I checked the latter on a synthetic duplicated-spend example. It yields NaN before the first row. Exactly $100k is included: **two runs** have a purchase there. Otherwise the $100k value carries forward the last purchase. The crossing cost is the **first grid point**, not the purchase’s unrounded spend.

**Inspected and checked against executed tests:** `analyze.paired()` maps each policy’s runs by JSON `seed` and intersects seed keys, so its comparisons are correctly seed-matched. All five kappa=1 headline policies have seeds 0–19. Default SciPy Wilcoxon is a reasonable *unadjusted* paired signed-rank comparison, but its distribution depends on ties and zero differences. The pKGFN–tiered comparison has one zero and 19 positive differences; the default result is the asymptotic **p=0.000131834**, not the conditional exact value quoted above. This distinction does not negate the observed wins. Checkpoints from one best-so-far trajectory are correlated, not independent observations.

**Inspected and tested an alternative:** The published bootstrap describes uncertainty in a *ratio of two first crossings of estimated mean curves*. In **each resample**, it also estimates a new target from the baseline’s own endpoint. It does not describe the distribution of individual-seed savings or uncertainty across other synthetic functions and cost assumptions. Independently resampling arms discards their shared seed pairing. When I resample **matched seed indices together**, the 90% intervals become **[2.249, 5.606]** for pKGFN, **[2.584, 5.537]** for reuse, **[2.140, 3.733]** for full BOFN and **[1.474, 2.948]** for standard BO. The independent bootstrap matches the inspected procedure; paired resampling is a relevant sensitivity analysis, not an assertion that one interval is universally correct. Neither removes dependence on this endogenously chosen target.

**Inspected:** Figure bands are **mean ± 1 SE**, neither 90% nor 95% confidence intervals and not the range among seeds. A conventional normal-theory 95% mean interval with 19 degrees of freedom would be about ±2.09 *sample* SE. Ribbon overlap does not test a paired difference. The README also reports many policy pairs, bias levels, endpoints and checkpoints with unadjusted p-values. I would preregister one primary endpoint and comparison or adjust exploratory tests for multiplicity. For illustration, the pKGFN–tiered **0.000132** remains small if multiplied by ten (**0.00132**), but this does not establish the causal ≥3× wording. At 8–12 seeds, isolated p-values such as 0.016 are highly sensitive to individual seeds.

## The supplied partial-versus-full PNG

**Inspected the supplied PNG and `plot.py`; executed numerical checks of its traces and annotation. I did not regenerate the PNG.** Visually, all traces begin near **35%**, agreeing with **34.920%** computed. At $25k the figure shows approximately **62/61/50/48/46%** for pKGFN/reuse/full BOFN/standard BO/tiered; at $50k approximately **70/74/77/63/56%**; and at $100k approximately **84/90/86/84/63%**. These agree with the exact means above to reading precision.

The arrow is drawn at the tiered final mean, **62.703%**. Its mathematical crossing spends are **$26.5k** for pKGFN and **$99.5k** for tiered, yielding the labeled **3.8×** after rounding. Plot code moves the *visible arrowheads* inward by $0.8k each, to **$27.3k and $98.7k**; these are not themselves the ratio’s numerator and denominator. The red solid pKGFN trace jumps from **81.113% at $99.5k** to **83.837% at $99.75k**; it does **not** rise further at exactly $100k. From $95k to $100k, four of 20 seeds improve after recorded late tensile tests, raising the mean **4.439 points**. It would mislead to read that visual jump as a typical smooth improvement.

The y-axis begins around **25%** rather than zero, accentuating vertical separation. The ±1 SE ribbons can look like confidence bands or suggest significance even though they are neither paired comparisons nor seed ranges. Labels “Partial” and “Full” fairly indicate *incremental policy rules*, but BOFN + reuse sometimes purchases a whole new pipeline and tiered screening reuses existing powders; red versus gray is not a comparison differing **only** in permission to partially evaluate. The plot does not show the substantial between-seed heterogeneity behind pKGFN’s last-step rise.

## What the action logs show

**Executed:** I counted actions and reconciled all final spends against stage `counts` for the five kappa=1 headline policies. To calculate *new* purchases, I subtracted the shared **37 CALPHAD** calls (32 initial plus five seed alloys) and **five** initial purchases at each other stage. Means over 20 runs:

| Policy | New CALPHAD | New atomizations | New prints | New tensile tests | Final-spend range |
|---|---:|---:|---:|---:|---:|
| pKGFN | **1.85** | **4.75** | **36.30** | **6.95** | $98,510–$99,940 |
| BOFN + reuse | 11.75 | 11.75 | 30.00 | 30.00 | $97,610–$99,990 |
| BOFN full | 23.00 | 23.00 | 23.00 | 23.00 | $96,830 in every run |
| Standard BO | 23.00 | 23.00 | 23.00 | 23.00 | $96,830 in every run |
| Tiered screening | 224.00 | 13.10 | 28.45 | 28.45 | $97,340–$99,740 |

The README’s “about 5 new powders against 36 prints” is correct: **4.75 atomizations and 36.30 prints** per pKGFN run. It omits the mean of only **6.95 tensile tests**; approximately **29.35** more new builds are printed than tested. Summed across pKGFN’s 20 runs, there are **37 new CALPHAD actions, 95 atomizations, 726 prints and 139 tensile tests**. No print directly changes *validated* best, whereas **61 of 139** recorded pKGFN tensile actions improved it. BOFN + reuse records **235 full-pipeline and 365 powder-reuse** steps across its 20 runs. No recorded action has zero or negative cost, and the stage-count costs reconcile to final spend.

No headline run finishes below **$95k**. Full BOFN and standard BO stop at **$96,830** because their next **$4,210** full cycle will not fit; that is budget granularity, not a far-early stop. pKGFN finishes $60–$1,490 short. Its seed runs purchase **0–4 new CALPHAD calls** each; one purchases **no new powder**. Its median longest consecutive-print sequence is **10 actions** (maximum **19**), and the median longest action gap between validated improvements is roughly **28 steps**, although action granularity differs by policy. These patterns are compatible with myopic concentration on existing powders and deferred testing. They **do not demonstrate that 64 base samples and 16 candidates per stage caused the behavior**: that requires fixed-seed reruns with larger settings. JSON rows have `action`, spend and score, **but not purchased design identifiers or acquisition values**. The code permits repeated prints and CALPHAD caching, but the stored logs cannot establish whether identical physical designs were repeatedly bought. Consecutive print actions alone are not proof of duplicates.

## Sensitivity at $100k

**Executed:** Recomputed all requested sensitivity values. Each cell is mean ± SE in percent, followed by the README’s rounded entry; the supplied optima are **0.484755** for kappa=0 and **0.530736** for kappa=0.5.

| Kappa | Policy | n | Recomputed (README) |
|---:|---|---:|---:|
| 0 | pKGFN | 12 | **57.023 ± 6.890** (57 ± 7) |
| 0 | BOFN + reuse | 8 | **86.504 ± 6.692** (87 ± 7) |
| 0 | BOFN full | 12 | **79.221 ± 7.721** (79 ± 8) |
| 0 | Standard BO | 12 | **71.151 ± 5.100** (71 ± 5) |
| 0 | Tiered | 12 | **85.134 ± 1.533** (85 ± 2) |
| 0 | pKGFN, any alloy | 8 | **90.917 ± 1.895** (91 ± 2) |
| 0.5 | pKGFN | 12 | **65.518 ± 5.177** (66 ± 5) |
| 0.5 | BOFN + reuse | 8 | **86.800 ± 3.699** (87 ± 4) |
| 0.5 | BOFN full | 12 | **87.436 ± 5.288** (87 ± 5) |
| 0.5 | Standard BO | 12 | **78.329 ± 3.638** (78 ± 4) |
| 0.5 | Tiered | 12 | **78.377 ± 2.247** (78 ± 2) |
| 0.5 | pKGFN, any alloy | 8 | **80.686 ± 7.047** (81 ± 7) |

The README’s **93%** BOFN figure in its kappa=0.5 *matched-eight-seed* comparison is also correct: BOFN reaches **93.111% on seeds 0–7**, versus **87.436% over all 12**. On matched seeds 0–7 at kappa=0/$50k, any-alloy pKGFN/tiered/BOFN reach **80.734/60.312/66.902%**. Any-alloy pKGFN used *lighter* Monte Carlo settings (**32 base samples, 10 candidates**) than headline pKGFN (**64, 16**); a policy comparison therefore does not isolate the effect of its new candidate rule. Eight to 12 seeds can document outcomes on these runs, but cannot establish stable rankings across other synthetic functions, cost assumptions or stochastic draws.

## Verdict and defensible wording

The kappa=1 difference from *biased tiered screening* is genuine in the stored trajectories: pKGFN finishes **21.135 percentage points** higher, with **19 seed wins and one tie**, and achieves the study’s stipulated crossing ratio of **3.755×**. This does **not** show that pKGFN beats full-pipeline BOFN or powder reuse overall, or that savings of at least 3× generalize to other targets or settings. BOFN + powder reuse has a similar crossing ratio and a higher $100k mean. I would not use the unqualified “partial evaluation is what clears 3×” formulation.

> **Most defensible single sentence:** “In this synthetic alloy benchmark at kappa=1, where CALPHAD misses an inoculant effect, pKGFN and BOFN with powder reuse reach tiered screening’s $100k mean validated score at about $26.5k (3.75×) and $26.25k (3.79×), respectively, but the result depends on the chosen target and does not show that pKGFN beats full-pipeline BOFN.”

### Discretionary analytical decisions

- I retained the stipulated $250 grid, supplied optima, mean-of-seeds definition and published SE convention to make the independent reconstruction directly comparable; I retained noncrossers when computing crossing medians.
- I reproduced independent arm-wise, 2,000-draw bootstrap resampling with its seed reset, then added matched-seed resampling because shared initial alloys make it an informative alternative.
- I kept `best_validated` as the headline endpoint rather than substituting a prediction or untested printed alloy: it measures what was actually printed **and** tensile-tested.
- I reported numerical crossings separately from visually inset arrow endpoints, and treated exploratory p-values and figure bands as descriptive unless their inferential assumptions were specified.

