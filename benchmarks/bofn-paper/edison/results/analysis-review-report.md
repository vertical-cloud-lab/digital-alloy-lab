# Independent audit of the synthetic-alloy BOFN benchmark

**Scope and execution.** I read `settings.md` first, then read all **292 JSON runs** in `results/k0`, `results/k0.5`, and `results/k1`. I implemented the aggregation directly from the JSON in notebook cells **before using any benchmark aggregation functions**: I advanced through each run's actions at each $250 grid point, retained the maximum tested objective, divided by the supplied true optimum (0.693739, 0.530736, 0.484755), and computed population-standard-deviation divided by \(\sqrt{n}\) standard errors (SE), censored time-to-target medians, and percentile bootstraps. I then **inspected** `analyze.py`, `plot.py`, `policies.py`, `run_sweep.py`, `bofn_alloy.py`, `README.md`, and the supplied PNG. I **executed an independent equivalent of** `analyze.curve()` and its bootstrap/paired-test formulas against the stored runs; I **did not execute** `analyze.py`, `plot.py`, policy optimization, or a new simulation. The listed optima are taken from `settings.md`, not independently optimized. JSON actions give stage and spend but **not purchased design identifiers**, so identical designs cannot be ruled in or out from these files.

## Discrepancies and findings, ranked

| Severity | Finding | Evidence / correction |
|---|---|---|
| **Changes the conclusion** | “Partial evaluation is what clears 3×” is an over-attribution. | At the **tiered policy's own final mean** of **62.703%**, the point ratios are pKGFN **3.755×**, BOFN + reuse **3.790×**, full BOFN **2.618×**, standard BO **2.140×**. But full BOFN's 90% interval extends above 3× (upper **3.90×**); both partial-policy intervals extend below 3×. This benchmark supports a *conditional point-estimate contrast*, not a uniquely established ≥3× advantage caused by partial evaluation. The tiered comparator itself reuses powder. |
| **Changes the conclusion** | Endogenous final-level target amplifies a tiny late baseline improvement. | Tiered mean is **62.614% at $95k**, only **0.089 percentage points** short of its $100k mean of 62.703%. The target first appears at **$99.5k**. At a fixed **62.5%** target it crosses at **$95k**, and the pKGFN ratio falls to **3.585×**; at 55% the ratio is **2.411×**. This is target-dependent, not a universal efficiency multiplier. A perfectly flat baseline plateau would instead put the crossing at the plateau's *start*; it is the tiny late increments, not flatness itself, that push the numerator toward $100k. |
| **Changes the conclusion** | “pKGFN also has the fastest start of any policy” sounds stronger than its evidence against reuse. | At $25k pKGFN **62.003%** versus BOFN + reuse **60.967%**; seed-matched difference **+1.036 points**, **6 wins / 2 ties / 12 losses**, Wilcoxon **p=0.528**. It has the highest *mean at that checkpoint*, not a reliable seed-level lead over reuse. By $100k reuse leads by **6.116 points**, pKGFN wins **4/20**, paired p=**0.0136** (unadjusted). |
| **Changes a number** | The headline bootstrap lower bound does not reproduce exactly from the stated inputs and `analyze.speedup` sampling order. | pKGFN/tiered 2,000 independent policy-wise resamples with seed 0 give **[2.144, 5.657]**, i.e. **2.1–5.7×** to one decimal; README gives **2.0–5.7×**. Other displayed intervals reproduce to one decimal. A $250 grid, finite bootstrap, rounding of supplied optimum and other implementation versions can move boundaries; I cannot infer which explains this difference. |
| **Changes a number** | “pKGFN reaches that level after about $26k” is slightly low. | First crossing is **$26,500** on the declared grid. “~$26.5k” (or rounded conventionally, ~$27k) is precise; README's $26k is $500 low. Arrow endpoints are drawn inward, see below. |
| **Changes a number** | “About six make–print–test cycles” at $25k is not what pKGFN actually bought. | $25k is ~six **full-pipeline cost equivalents** ($4,210 each), but its mean actual additional purchases by then were **0.20 CALPHAD, 1.35 atomizations, 8.40 prints, 2.90 tensile tests**. Seven of 20 runs had bought **zero** new powders by $25k. |
| **Cosmetic / precision** | “Ahead ... on 19 of 20 seeds” omits a tie; “p=1e-4” is a one-significant-digit report. | At $100k: **19 wins, 1 exact tie, 0 losses**, +**21.135** percentage points. `scipy.stats.wilcoxon` default two-sided result **0.000131834**; its asymptotic treatment with one zero explains the displayed ~1e-4. An *exact nonzero-difference* Wilcoxon calculation gives **3.81e-6**; stating the test convention matters. |
| **Cosmetic / no numerical discrepancy** | All specified kappa=1 README table cells and other Bottom-line rounded checkpoints and point ratios reproduce. | See detailed tables below. At kappa=0 and 0.5 all requested $100k values also round to the README entries. |

**No hidden mismatch in the requested table:** the values below show the exact reconstruction alongside the README's rounded values. “Not reached” means the median of all seeds' crossing costs is infinite, with noncrossers right-censored at $100k; percentages in parentheses are the number crossing divided by *all* seeds. In particular, the median is **not** the median among successful seeds alone.

## Kappa = 1: recomputation next to the README

Entries in the next two tables have **recomputed value (README value)**. The SE is computed from 20 seeds with `ddof=0`, matching the published convention.

| Policy | $25k mean ± SE, % | $50k mean ± SE, % | $100k mean ± SE, % |
|---|---:|---:|---:|
| pKGFN | **62.003 ± 5.207** (62 ± 5) | **69.577 ± 3.451** (70 ± 3) | **83.837 ± 1.790** (84 ± 2) |
| BOFN + powder reuse (`eifn_reuse`) | **60.967 ± 6.081** (61 ± 6) | **73.837 ± 5.055** (74 ± 5) | **89.953 ± 2.399** (90 ± 2) |
| BOFN, full (`eifn`) | **50.068 ± 6.081** (50 ± 6) | **76.831 ± 4.567** (77 ± 5) | **85.751 ± 4.056** (86 ± 4) |
| Standard BO (`ei`) | **48.462 ± 6.751** (48 ± 7) | **63.229 ± 5.182** (63 ± 5) | **83.831 ± 2.751** (84 ± 3) |
| Tiered screening | **46.067 ± 4.973** (46 ± 5) | **55.943 ± 3.463** (56 ± 3) | **62.703 ± 2.250** (63 ± 2) |

| Policy | Median $ to 60%; reached | Median $ to 70%; reached | Median $ to 80%; reached |
|---|---|---|---|
| pKGFN | **$15,125; 19/20** ($15k; 95%) | **$25,375; 19/20** ($25k; 95%) | **$85,875; 15/20** ($86k; 75%) |
| BOFN + reuse | **$18,750; 20/20** ($19k; 100%) | **$25,500; 18/20** ($26k; 90%) | **$52,375; 17/20** ($52k; 85%) |
| BOFN full | **$31,625; 18/20** ($32k; 90%) | **$35,875; 17/20** ($36k; 85%) | **$42,250; 16/20** ($42k; 80%) |
| Standard BO | **$40,125; 19/20** ($40k; 95%) | **$46,500; 17/20** ($46k; 85%) | **$59,000; 14/20** ($59k; 70%) |
| Tiered | **$55,750; 12/20** ($56k; 60%) | **>$100k; 3/20** (>$100k; 15%) | **>$100k; 2/20** (>$100k; 10%) |

The $46.5k and $25.5k medians in the README are rounded using Python's *ties-to-even* formatting (46k and 26k respectively); these are formatting choices, not errors.

**Four speed-ups versus tiered screening**, using each method's mean-curve first crossing of **tiered's final mean**. I reset NumPy's seed-0 generator for each independent-policy bootstrap comparison, resampled each policy's 20 seeds with replacement 2,000 times, and took the 5th/95th percentiles.

| Method | Tiered crossing | Method crossing | Ratio and 90% interval, recomputed | README |
|---|---:|---:|---|---|
| pKGFN | $99,500 | $26,500 | **3.755× [2.144, 5.657]** | 3.8× [2.0, 5.7] |
| BOFN + reuse | $99,500 | $26,250 | **3.790× [2.222, 5.940]** | 3.8× [2.2, 5.9] |
| BOFN full | $99,500 | $38,000 | **2.618× [2.140, 3.902]** | 2.6× [2.1, 3.9] |
| Standard BO | $99,500 | $46,500 | **2.140× [1.467, 2.948]** | 2.1× [1.5, 2.9] |

## Curve construction and inference checks

- **Executed:** My forward-time implementation and an independent literal implementation of the inspected `analyze.curve()` expression agree at all **401 × 292** run-grid positions (including each run's $100k value). All runs start with a row at spend $0, have monotone *strictly increasing* recorded spends, and have finite `best_validated`. `searchsorted(spent, grid, side="right") - 1` selects the **last** purchase on or before a grid spend; at an exact grid-price purchase it immediately includes it. A synthetic duplicated-spend test also selects the last duplicate. Before the first recorded row the inspected expression yields NaN; it does **not** invent a starting value. The running maximum prevents decreases in `best_validated` (already nondecreasing in these logs). The $100k grid endpoint includes any purchase made exactly at $100k: **two of the 292 runs** have such a row. All other curves carry forward the last observed value; they do not extrapolate a new evaluation at the limit. `analyze.cost_to` uses first grid crossings, not exact within-grid spend.
- **Executed and inspected:** `analyze.paired()` constructs maps indexed by JSON `seed` and intersects the seed keys, so it **matches correctly** regardless of directory listing order. For kappa=1 all five headline policies have seeds 0–19. The default SciPy two-sided Wilcoxon signed-rank test is valid as an unadjusted paired comparison of signed, nonzero differences, *conditional on its assumptions*, but zero differences and tied magnitudes change the reference distribution. The pKGFN–tiered comparison has one exact zero: SciPy's default uses the asymptotic p=0.000131834 rather than the conditional exact p=3.81e-6 for the 19 nonzero differences. The claim of 19 wins stands independently of test convention. The score is the **best-so-far maximum** on each seed, so observations at different spend checkpoints are highly correlated, not independent replications.
- **Inspected and recomputed alternative:** The percentile bootstrap targets a *ratio of estimated mean-curve crossing times*, recalculating the baseline's target in each resample. It is **not** an interval for each seed's speed-up, nor a guaranteed probability that the population ratio exceeds 3. It ignores matched seeds by independently resampling policy arms. Paired-by-seed resampling changes the 90% intervals to **[2.249, 5.606] pKGFN**, **[2.584, 5.537] reuse**, **[2.140, 3.733] full BOFN**, **[1.474, 2.948] standard BO** (2,000 draws). Both choices are legitimate for different sampling models, but matched seeds argue for paired resampling; neither bootstrap solves endogenous-target fragility, selection of this target, synthetic-world uncertainty, or 20-seed sampling error.
- **Inspected:** `plot.py` shows **mean ± 1 SE**, *not* a 90%/95% confidence interval and not seed-to-seed variability. Under normal approximation a 95% mean interval is around ±2.09 sample SE with 19 degrees of freedom; using `ddof=0` makes displayed bands slightly narrower than conventional sample SE. Overlapping or separated plotted bands are not a paired-significance test.
- **Inspected / executed paired spot checks:** There are many policy pairs, checkpoints, bias settings and metrics. The README's p-values (including **0.015625** for 7/8 wins of any-alloy pKGFN vs screening at kappa=0 and **0.00486** against full BOFN at kappa=1/$50k) are unadjusted. Predefine a primary comparison/endpoint or apply a family-wise or false-discovery correction to exploratory tests; avoid selecting the strongest result after inspection. The tiered-vs-pKGFN p=0.000132 remains small under, for example, a Bonferroni adjustment for ten tests (**0.00132**), but that does not validate the ≥3× mechanistic claim. At n=8, an apparent p=0.016 is based on very few reversals and has low precision. No noise, cost-model, true-optimum, or across-problem uncertainty is captured.

## Supplied PNG and `plot.partial_vs_full()`

**Inspected the PNG; executed numerical cross-checks of the traces and arrow, but did not regenerate the image.** Read off the figure: all traces begin around **35%** (calculated **34.920%**); at $25k the red solid/dashed are about **62%/61%**, and the full BOFN / standard BO / screening gray traces are about **50%/48%/46%**. At $50k they are about **70%/74%/77%/63%/56%**; at $100k about **84%/90%/86%/84%/63%**, respectively. These agree with the tabulated recomputation within graphical reading precision.

The annotation's y-coordinate is **62.703%**. Its defined *mathematical* crossing endpoints are **$26.5k and $99.5k**, ratio **3.755×**. The actual arrowheads are deliberately inset by **$0.8k** each, at **$27.3k and $98.7k**: those drawn endpoints are **not** the crossing spends, although the 3.8× text correctly uses the uninset ones. At the right, a red solid pKGFN trace jumps from **81.113% at $99.5k to 83.837% at $99.75k**; there is **no** additional increase at exactly $100k. From $95k to $100k its mean rises **4.439 points**, supplied by improvements in **4 of 20 seeds** (each improved by ~15–37 points). Those rises are attributable to recorded tensile actions in the last few thousand dollars, not visual interpolation. They should not be misread as a typical smooth late improvement.

**Possible visual misreadings:** SE ribbons look like uncertainty intervals about policy superiority but are neither confidence intervals nor paired contrasts; the y-axis starts around **25%**, not zero, magnifying vertical differences; labels “Partial: BOFN + reuse” and “Full: BOFN” correctly describe their *incremental-choice rules*, but reuse still pays for full pipelines on some steps and tiered screening also reuses powder. Thus the red-vs-gray grouping is not a controlled comparison of *only* whether evaluation is partial. The lack of per-seed trajectories hides pKGFN's four-run terminal jump and its variability. The large solid-vs-dashed red visual contrast should not be mistaken for pKGFN beating powder reuse at the finish.

## Action logs: what the policies purchased

**Executed:** Counted JSON actions and reconciled all stage costs and final spends with the stored `counts` for all five kappa=1 headline policies. Subtracted the **shared 37 CALPHAD runs** (32 initial plus 5 seed alloys) and **5 each** for atomizations, prints and tensile tests; incorrectly subtracting only 32 CALPHAD calls would add five phantom new calls. Means over 20 seeds:

| Policy | New CALPHAD | New atomizations | New prints | New tensile tests | Final spend range |
|---|---:|---:|---:|---:|---:|
| pKGFN | **1.85** | **4.75** | **36.30** | **6.95** | $98,510–$99,940 |
| BOFN + reuse | 11.75 | 11.75 | 30.00 | 30.00 | $97,610–$99,990 |
| BOFN full | 23.00 | 23.00 | 23.00 | 23.00 | $96,830 (all seeds) |
| Standard BO | 23.00 | 23.00 | 23.00 | 23.00 | $96,830 (all seeds) |
| Tiered screening | 224.00 | 13.10 | 28.45 | 28.45 | $97,340–$99,740 |

pKGFN's mean action totals were **37 CALPHAD, 95 atomizations, 726 prints, 139 tensile tests** across the 20 runs. Its README's “about 5 new powders against 36 prints” is accurate (**4.75** and **36.30**); it leaves **~29.35 more new prints than tensile tests** per run, the reason best-validated may lag untested printed designs. Its actions `C/A/L/T` cost $10/$1,500/$2,500/$200; BOFN + reuse has **235 full ($4,210) and 365 reuse ($2,700)** steps, while tiered pays one **$2,240** screening batch per seed followed by full/reuse steps. The sums of recorded spends and stage counts agree for all kappa=1 runs, and no recorded action had zero or negative incremental spend. **No run ends below $95k.** Full BOFN/standard BO leave $3,170 because another $4,210 cycle does not fit; this is *budget granularity*, not an early failure. pKGFN leaves $60–$1,490; its low-cost eligible stage is not necessarily bought when marginal value/fallback is flat, but there is no evidence of runs ending far below budget.

**Signs worth investigating, not proof of MC settings causing harm:** pKGFN buys only **0–4 new CALPHAD calls** per seed, has **one seed with zero new atomizations**, and buys a median of **10 consecutive prints** (maximum **19**); its **726 print actions themselves produce zero immediate best-validated gains**, because the metric credits tested designs only. Of **139 tensile actions**, **61** improved the incumbent. Median longest action gap between improvements is ~**28** steps (max **49**), versus ~8 for full BOFN; this is partly forced by the different action granularity. These trajectories are compatible with myopic attraction to existing powders and deferred testing, not direct evidence that **64 base samples / 16 candidates per stage** caused those choices. Such a causal diagnosis needs reruns with larger candidate pools/base samples *holding policy and seeds fixed*. JSON does not include purchased compositions/laser settings or KG scores: code permits repeated printed designs and repeated atomizations (and CALPHAD deduplicates cached compositions), but I **cannot verify** whether identical physical purchases occurred in these stored runs; consecutive `L` rows alone are not duplicates.

## Sensitivity: independently recomputed at $100k

All cells are **mean ± SE % from JSON (README rounded entry)**. Sample sizes are per row, not balanced across policies.

| Kappa | Policy | n | $100k value % (README) |
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

At kappa=0.5, BOFN full is **93.111%** on the same *eight seeds* as any-alloy pKGFN (**80.686%**), explaining the README's 93% matched-seed comparison despite **87.436%** over all 12 BOFN seeds. At kappa=0, the eight matched seeds' $50k values are **80.734%** any-alloy pKGFN, **60.312%** tiered and **66.902%** BOFN. These variants had **32 base samples and 10 candidates**, versus 64 and 16 for main pKGFN: across-variant conclusions mix candidate-rule and Monte Carlo (MC) settings. Eight or 12 seeds are useful for showing **these observed benchmark outcomes**, but do not establish universal rankings, stable tail probabilities, or that the same ordering survives different synthetic truths/costs. The kappa=0.5 BOFN–tiered $100k paired comparison has 11/12 wins and unadjusted Wilcoxon **p=0.0342**; it is still exploratory among many contrasts.

## Verdict and suggested wording

The **kappa=1 result against biased tiered screening is real in the stored synthetic trajectories**: pKGFN is +21.135 points at $100k with 19 wins and one tie, and the stipulated mean-curve crossing ratio is 3.755×. It is **not evidence that pKGFN outperforms full-pipeline BOFN or powder reuse overall**, nor that ≥3× savings transfer beyond this target, these hand-built functions, and this tiered comparator. The strongest alternative here is **BOFN + powder reuse**, with an almost identical crossing ratio and a higher final mean. The unqualified causal/headline wording about partial evaluation “clearing 3×” is overstated.

> **Most defensible single sentence:** “In this synthetic alloy benchmark at kappa=1, where CALPHAD misses an inoculant effect, pKGFN and BOFN with powder reuse reach tiered screening's $100k mean validated score at about $26.5k (3.75×) and $26.25k (3.79×), respectively, but the result depends on the chosen target and does not show that pKGFN beats full-pipeline BOFN.”

### Discretionary analytical decisions

- I retained the study's $250 spend grid, supplied optima, mean-of-seeds definition and `ddof=0` SE so the independent numbers are directly comparable to the published table; for times-to-target I kept noncrossers at infinity rather than conditioning on successes.
- I used independent arm-wise bootstrap draws with 2,000 replicates and a seed-0 generator *reset per method* to reproduce the documented procedure, and reported a paired-seed bootstrap sensitivity because all policies share seeded initial alloys.
- I compared the pre-specified headline metric `best_validated` rather than substituting `rec_printed` or an unvalidated recommendation: that metric is the README figure's demonstrated-alloy endpoint.
- I called small late spend differences and matched-seed decisions explicitly rather than treating rounded headline ratios as exact or interpreting figure ribbons as hypothesis tests.
