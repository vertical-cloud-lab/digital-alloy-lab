# Independent review of the copper function-network benchmark (uploaded snapshot)

**Verdict.** I independently reconstructed the stored runs before examining `analyze.py`. At the headline (κ,η)=(1,1), full-pipeline Bayesian optimization on the function network (BOFN) reaches **73.212%** of the stored optimum after $100,000, BOFN with lot reuse **72.033%**, corrosion-informed tiered screening (`tiered_ni_ref`) **24.233%**, standard Bayesian optimization **14.421%**, and production-setting partial knowledge-gradient function-network optimization (pKGFN) **58.856% on only seven completed seeds**. The comparison supports BOFN over these baselines *in this synthetic benchmark*; it does **not** show that deciding which stage to buy beats running a full chain. The README's integer-valued mean claims reproduce, but some standard errors, bootstrap interpretation, and causal/fidelity wording need correction. I did not run new Bayesian-optimization searches.

**Data and method.** I read `settings.md` first, then wrote and executed the independent NumPy/SciPy reconstruction in `outputs/independent_core.py` before opening `analyze.py`. I read 149 `results/` JSONs (seven production pKGFN and seven other 20-seed headline policies; two additional single-seed sensitivity runs), 30 light pKGFN JSONs (20 headline, ten sensitivity), and separately 80 no-gate JSONs. I use the exact (1,1) optimum **0.492187251856002** from `truth_tables.json`; the 0–$100,000 grid has $250 steps. Each seed contributes its last row with `spent <= grid point` (including the $0 shared seed row), running maximum of `best_validated`, divided by its cell optimum. Endpoints are arithmetic means; my **standard errors use sample SD/√n**. A missing threshold crossing is `∞`, not a fabricated $100k crossing. I leave all supplied inputs unchanged.

## Severity-ranked discrepancies and findings

| Severity | Finding | Evidence / correction |
|---|---|---|
| Changes the conclusion | F1 — Claim scope | Network-aware BOFN beats the baselines here; choosing stages does not demonstrably beat full-pipeline BOFN. Production pKGFN is 58.856%, versus 73.212% full BOFN; matched difference −28.511 points, nominal p=0.046875, not multiplicity-robust. |
| Changes the conclusion | F2 — Fidelity inference | “The lighter settings were not why pKGFN lags” is too categorical: only 7 matched seeds; high−light = −5.337 points, 90% paired-bootstrap interval −23.784 to +11.721. Fidelity, F2 anchoring and F4 fallback fixes changed together. |
| Changes the conclusion | F3 — Matched-bootstrap estimand | The production pKGFN 2.1164× point uses 7 method/20 reference seeds; its matched interval 0.8086–1.9879 uses 7/7 and a different target. The proper matched point is 1.4077×. These are not two intervals for the same sample estimator. |
| Changes the conclusion | F4 — Spec-tiered speed-up | The 17–20× ratios measure crossing a negative −7.691% level, not reaching a good alloy. The bootstrap upper limit 397× is an artifact of flooring method crossing spend at $250; zero-spend crossings really occur. |
| Changes the conclusion | F5 — Causal/mechanistic wording | No-gate ablation supports gate sensitivity, not the exclusive claim “the reason is clear” or proof of what the learned model inferred. Non-random policies change their designs; no physical calibration or gate-bias factorial is available. |
| Changes a number | F6 — Standard errors | All nonzero reported SEs use population SD (ddof=0), not sample SD. They are smaller by factors √((n−1)/n); n=1 gives a misleading ±0. Production pKGFN should be ±11 at $50k and ±12 at $100k, not ±10 and ±11. |
| Changes a number | F7 — Runtime claim | README says production pKGFN takes ~25–35 min/run, 2.9× light. Stored wall_s: mean 62.39 min, range 32.66–83.51; matched light mean 11.23 min (ratio 5.56). Hardware/load equivalence is unknown. |
| Changes a number | F8 — Omitted speed-up row | tiered_ni_ref is present but excluded from the speedup_table default kinds. Against spec tiered it is 11.0278×, $9,000, independent CI 5.0253–397, matched CI 7.2182–14.1786. |
| Changes a number | F9 — Fragile final-budget pKGFN level | Production pKGFN mean jumps from 46.214% at $99,750 to 58.856% at $100,000; three late validations explain 12.642 points. This is legitimate step-function accounting, but the endpoint is unusually sensitive. |
| Changes a number | F10 — Rounding/small numerical differences | Purchases and medians reproduce at the printed precision. Examples: 37.857 Mines sessions → 37.9; tiered_ni immersions 2.550 prints 2.5 in supplied floating-point formatting; reference passes 2.650 prints 2.6. Do not interpret rounded tenths as exact. |
| Changes the conclusion | F11 — Incomplete sensitivities | No (1,0)/(0,1) runs; (0,0) has light pKGFN n=10 and BOFN variants n=1. No screen/audit/mines_only/funnel results. These cannot establish robustness, a screen-audit benefit or a two-step DED benefit. |
| Cosmetic / potentially misleading | F12 — Figure labeling and uncertainty | Proposal PNG is light pKGFN, not production. “Partial: BOFN + reuse” means full downstream testing with lot reuse, not free stage selection. Bands are selective, unlabeled ±SE; full BOFN and standard BO have no bands. |
| Cosmetic | F13 — Small-figure readability | Only endpoint axis ticks; no zero line or intermediate spend ticks. At 3.1 in, 24-point source labels scale to ~6.76 pt; most width is used by direct labels, leaving ~1.64 in of data axes. |
| Verified, no numerical discrepancy | F14 — Internal consistency | Every reconstructed best_validated curve equals the supplied curve exactly; regenerating tables.md gives zero differing lines. Means, median thresholds, listed ratios, bootstrap quantiles, Wilcoxon results and purchase counts reproduce under the supplied conventions. |

The production run provenance is confirmed from the seven JSON settings: S=64, 16 stage candidates, 512 pool, 32+16 anchors, 24 perturbations and `CODE_VERSION=2026-10-27`. Light files record S=32, 10 candidates, 256 pool; some old-file settings fields do not record the anchor/perturbation counts or code version. Source documentation says F2/F4 and settings changed together. The no-gate 80 JSONs are independent, normalized by an independently optimized no-gate truth (~0.74505148); I did not rely on a missing `compare/landscape.json`.

## 1. Headline values, side by side — **executed**

All entries below are percentage points of the true optimum; each `±` is a standard error. “Supplied” is the rounded value in both `tables.md` and README's headline tables (its SE uses population SD). These are **all nine policies actually present** at (1,1).

| Policy | n | My $25k | Supplied $25k | My $50k | Supplied $50k | My $100k | Supplied $100k |
|---|---|---|---|---|---|---|---|
| pKGFN, production | 7 | 3.341 ± 5.433 | 3 ± 5 | 24.572 ± 11.109 | 25 ± 10 | 58.856 ± 12.208 | 59 ± 11 |
| pKGFN, light | 20 | 11.951 ± 6.559 | 12 ± 6 | 27.440 ± 7.385 | 27 ± 7 | 58.552 ± 4.844 | 59 ± 5 |
| BOFN, full | 20 | 14.977 ± 5.745 | 15 ± 6 | 38.774 ± 9.116 | 39 ± 9 | 73.212 ± 7.322 | 73 ± 7 |
| BOFN + reuse | 20 | 14.353 ± 4.702 | 14 ± 5 | 32.274 ± 7.805 | 32 ± 8 | 72.033 ± 7.046 | 72 ± 7 |
| Tiered, spec | 20 | -9.427 ± 5.500 | -9 ± 5 | -9.106 ± 5.473 | -9 ± 5 | -7.691 ± 5.366 | -8 ± 5 |
| Tiered, Ni floor | 20 | -6.644 ± 5.497 | -7 ± 5 | 0.762 ± 5.537 | 1 ± 5 | 10.217 ± 6.382 | 10 ± 6 |
| Tiered, Ni + reference | 20 | 7.858 ± 4.225 | 8 ± 4 | 16.136 ± 3.960 | 16 ± 4 | 24.233 ± 4.750 | 24 ± 5 |
| Standard BO | 20 | 5.680 ± 3.413 | 6 ± 3 | 7.180 ± 3.299 | 7 ± 3 | 14.421 ± 6.256 | 14 ± 6 |
| Random | 20 | -0.612 ± 4.532 | -1 ± 4 | 6.904 ± 4.977 | 7 ± 5 | 22.293 ± 5.024 | 22 ± 5 |

**Every 1-point displayed SE discrepancy in the headline table:** production pKGFN $50k 10→11 and $100k 11→12; light pKGFN $25k 6→7; tiered spec $25k 5→6; Ni-floor tiered $50k 5→6; random $25k 4→5. Means are unchanged at supplied precision. All unrounded SEs differ whenever within-policy variance is nonzero: multiply published SE by √(7/6)=1.0801 for production pKGFN or √(20/19)=1.0260 for 20-seed policies. The (0,0) light pKGFN $25k SE changes 4→5, while its two single-seed BOFN results should not display “± 0”. The README's alternate `rec_printed` table likewise has corrected displayed SE: production pKGFN $25k 10→11, $50k 12→13, $100k 6→7; light pKGFN $100k 4→5; random $25k 4→5. Every unrounded mean and SE is in `outputs/all_SE_comparisons.csv`.

Medians of **per-seed** first grid crossings (mine / supplied rounded notation; fraction reaching threshold by $100k) also agree exactly with the supplied integer-$k displays:

| Policy | 60%: mine / supplied; reached | 70%: mine / supplied; reached | 80%: mine / supplied; reached |
|---|---|---|---|
| pKGFN, production | $100,000 / $100k; 4/7 | not reached / >$100k; 3/7 | not reached / >$100k; 2/7 |
| pKGFN, light | $85,500 / $86k; 12/20 | not reached / >$100k; 7/20 | not reached / >$100k; 1/20 |
| BOFN, full | $66,750 / $67k; 17/20 | $73,875 / $74k; 15/20 | $88,125 / $88k; 14/20 |
| BOFN + reuse | $54,375 / $54k; 17/20 | $64,625 / $65k; 17/20 | $80,625 / $81k; 13/20 |
| Tiered, spec | not reached / >$100k; 0/20 | not reached / >$100k; 0/20 | not reached / >$100k; 0/20 |
| Tiered, Ni floor | not reached / >$100k; 0/20 | not reached / >$100k; 0/20 | not reached / >$100k; 0/20 |
| Tiered, Ni + reference | not reached / >$100k; 2/20 | not reached / >$100k; 0/20 | not reached / >$100k; 0/20 |
| Standard BO | not reached / >$100k; 3/20 | not reached / >$100k; 1/20 | not reached / >$100k; 1/20 |
| Random | not reached / >$100k; 1/20 | not reached / >$100k; 0/20 | not reached / >$100k; 0/20 |

In particular, production pKGFN's 60% median is an exact grid crossing at **$100,000** (four of seven seeds reached 60%), not an extrapolation; the three others did not cross. Some 70% and 80% medians are `∞` because at least half the seeds did not reach the level. README lines 8–30 and 66–107 reproduce these rounded means, medians and paired tests under their own SE convention; its 49-point BOFN-versus-reference difference is **48.979** points and its 17/20 matched wins give a two-sided Wilcoxon **p=0.000322**. Its qualitative claim that the production pKGFN equals light pKGFN at 59% only concerns *unmatched, differently sized samples*.

### Speed-ups — **executed**

A speed-up is the baseline's **first mean-curve crossing of its own $100k final mean**, divided by the method's first mean-curve crossing of that same target. Each row below reproduces `tables.md`'s exact implementation, including its 2,000-replicate, seed-0, policy-independent and matched-seed percentile bootstraps; decimals expose differences hidden by the published one-decimal display. A non-crossing method is represented by **0×** in that implementation, rather than a measured speed-up. The extra `tiered_ni_ref` row versus spec tiered was omitted from the supplied table even though it exists in the files.

**Baseline: spec tiered**, final target **−7.690822%**, baseline first crossing **$99,250** (the supplied `$99k`):

| Method | First mean crossing | Ratio | 90% independent CI | 90% matched CI | Bootstrap fraction ≥3 |
|---|---|---|---|---|---|
| pKGFN, production | $5,750 | 17.2609 | 2.7192–397.0000 | 11.5263–20.7895 | 0.9485 |
| pKGFN, light | $5,750 | 17.2609 | 5.7536–397.0000 | 11.9697–21.9444 | 0.9885 |
| BOFN, full | $5,000 | 19.8500 | 18.3500–397.0000 | 18.3500–19.8500 | 0.9925 |
| BOFN + reuse | $5,000 | 19.8500 | 10.9500–397.0000 | 18.3500–43.8889 | 0.9955 |
| Tiered, Ni floor | $23,250 | 4.2688 | 1.1507–397.0000 | 2.6829–7.2182 | 0.5535 |
| Tiered, Ni + reference | $9,000 | 11.0278 | 5.0253–397.0000 | 7.2182–14.1786 | 0.9870 |
| Standard BO | $5,000 | 19.8500 | 5.1558–397.0000 | 18.3500–19.8500 | 0.9760 |
| Random | $9,750 | 10.1795 | 2.3081–397.0000 | 9.4103–19.8500 | 0.8690 |

**Baseline: corrosion-informed `tiered_ni_ref`**, final target **24.233129%**, baseline first crossing **$100,000**:

| Method | First mean crossing | Ratio | 90% independent CI | 90% matched CI | Bootstrap fraction ≥3 |
|---|---|---|---|---|---|
| pKGFN, production | $47,250 | 2.1164 | 0.8766–2.4242 | 0.8086–1.9879 | 0.0065 |
| pKGFN, light | $46,750 | 2.1390 | 1.4933–3.9176 | 1.4936–3.5088 | 0.1155 |
| BOFN, full | $33,500 | 2.9851 | 1.6560–4.1667 | 1.6571–3.4783 | 0.1560 |
| BOFN + reuse | $35,250 | 2.8369 | 1.6571–4.0941 | 1.6812–3.9216 | 0.3790 |
| Tiered, spec | not reached | 0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000 |
| Tiered, Ni floor | not reached | 0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000 |
| Standard BO | not reached | 0.0000 | 0.0000–1.0000 | 0.0000–0.0000 | 0.0000 |
| Random | not reached | 0.0000 | 0.0000–1.6129 | 0.0000–1.6129 | 0.0000 |

The published one-decimal CIs and probabilities in `tables.md` and the README agree with the exact rows above (subject to ordinary rounding). Most important: full BOFN needs **$33,500**, giving **2.9851×** (published 3.0×, independent 90% CI **1.6560–4.1667**, matched CI **1.6571–3.4783**); reuse needs **$35,250**, **2.8369×** (independent **1.6571–4.0941**, matched **1.6812–3.9216**); production pKGFN needs **$47,250**, **2.1164×** (independent **0.8766–2.4242**, matched **0.8086–1.9879**). The matched production pKGFN/reference bootstrap **instead uses baseline seeds 0,1,2,3,4,5,7**, whose baseline final mean is **27.8146%**; on that matched subset the point ratio is **$82,000/$58,250 = 1.4077×**. Label the matched point alongside its matched interval; the mixed-sample 2.1× should not be presented as the center of the 0.8–2.0 interval. The independent 90% interval includes 1 for production pKGFN, so its spend advantage is not established at that confidence level. A 90% CI does not prove a **≥3×** effect for full BOFN: its independent bootstrap fraction ≥3 is **0.156**. The production pKGFN bootstrap fraction ≥3 is **0.0065**.

The spec-tiered target is **below zero** and gives essentially every model-based policy a large ratio, even standard BO (19.85×) and `tiered_ni_ref` (11.03×); it is not evidence of a useful alloy search speed-up. In independent resamples of the spec-tiered seeds the target can be below the starting mean, producing a *zero-cost* crossing. The supplied `_ratio` floors the method's cost at **$250**, giving a finite **397×** upper percentile ($99,250/$250); this is a convention, not observed spend. A 20,000-replicate bootstrap with a literal zero-cost crossing has an infinite upper percentile for that comparison. The baseline first crossing can fluctuate near $100k by construction, and target, crossing and method rankings are resampled jointly; such percentile intervals are discrete, nonlinear and not general-purpose uncertainty bands. Bootstrap seeds as paired blocks when the same seed data matter, and report matched point/interval with the same matched sample. Comparisons remain descriptive because policy searches, calibration and target were selected in this specific benchmark.

### Paired pKGFN tests — **executed**

The table lists production-setting pKGFN minus each named policy; W/T/L denotes wins/ties/losses over the **same seven seeds**. These reproduce all 24 Wilcoxon rows in `tables.md` and README (exact two-sided p values rather than rounded).

| Production pKGFN minus… (n=7) | $25k: Δ; W/T/L; p | $50k: Δ; W/T/L; p | $100k: Δ; W/T/L; p |
|---|---|---|---|
| pKGFN, light | -11.323; 3/0/4; 0.578125 | -2.099; 3/0/4; 0.937500 | -5.337; 3/0/4; 0.687500 |
| BOFN, full | -20.507; 0/0/7; 0.015625 | -20.774; 1/0/6; 0.218750 | -28.511; 1/0/6; 0.046875 |
| BOFN + reuse | -14.007; 1/0/6; 0.109375 | -14.940; 2/0/5; 0.375000 | -3.053; 3/0/4; 0.812500 |
| Tiered, spec | +16.650; 6/1/0; 0.031250 | +36.963; 7/0/0; 0.015625 | +69.290; 7/0/0; 0.015625 |
| Tiered, Ni floor | +13.921; 5/1/1; 0.093750 | +30.181; 6/0/1; 0.046875 | +53.370; 7/0/0; 0.015625 |
| Tiered, Ni + reference | -6.759; 2/0/5; 0.468750 | +3.640; 5/0/2; 0.687500 | +31.041; 6/0/1; 0.046875 |
| Standard BO | -0.309; 2/1/4; 0.843750 | +20.041; 4/0/3; 0.218750 | +46.761; 5/0/2; 0.078125 |
| Random | +3.774; 4/1/2; 0.562500 | +21.813; 5/0/2; 0.156250 | +39.952; 6/0/1; 0.031250 |

For the most relevant *paired fidelity* comparison, high versus light scores at $100k were **58.856±12.208% versus 64.192±4.671%** on the seven common seeds; mean paired difference **−5.337 points**, Wilcoxon **p=0.6875**, paired seed-bootstrap 90% interval **−23.784 to +11.721 points** (50,000 draws, random seed 20261027). The matched-light README row should have sample-SE displays **±11, ±12, ±5**, rather than **±10, ±12, ±4** at $25k/$50k/$100k; its exact means are **14.664%, 26.671%, 64.192%**. They have 3/0/4 high-setting wins/ties/losses. At $25k the difference is −11.323 (p=0.578125), at $50k −2.099 (p=0.9375). On those same seven seeds full BOFN ends at **87.367±3.878%**, production pKGFN minus full BOFN **−28.511** points (1/0/6, p=0.046875). The 7-seed high result is vulnerable to seed selection and cannot establish equivalence or that lighter Monte Carlo settings played no role. Even the seven high-setting `wall_s` total range **32.66–83.51 min** versus matched light mean **11.23 min**; timings are observational and may reflect a different machine/load.

**Multiplicity:** these are exploratory comparisons over eight rivals × three budgets (24 tests): Holm adjustment makes the minimum adjusted p **0.375**, and production-pKGFN-versus-full BOFN at $100k adjusts to **0.84375**. Thus nominal p=0.047 must not be advertised as a multiplicity-robust finding. In contrast, full BOFN versus `tiered_ni_ref` at $100k uses all 20 matched seeds: **+48.979 points, 17/0/3, p=0.000322**; even conservatively correcting the 9-policy, 3-budget all-pairs family (108 tests) by Holm gives **0.0274**. The choice of comparison family is discretionary; both families and exact tests are in `outputs/independent_paired.csv` and `outputs/all_policy_pairs.csv`.

## 2. Supplied curve/cost/seed logic — **executed and inspected**

I generated an adversarial five-row example at spends $500, $1,000 (two rows), $100,000, and $100,010. `analyze.curve` gives **NaN at $0 and $250** (before first row), **0.2 at $500/$750**, **0.3 at exactly $1,000** (the last duplicate-spend row and running maximum), **0.3 at $99,750**, and **0.4 at exactly $100,000**; it excludes the $100,010 row. `cost_to` returns **$500, $1,000, $100,000, ∞** for targets 0.2, 0.3, 0.4, 0.5. This is right-continuous and grid-rounded upward, not a linear interpolation. Every actual JSON starts with an `init` row at $0, so actual pre-first-row behavior is never exercised; all 179 scored-run initial rows are present. I found **no decreases** in stored `best_validated`, and the independent curves and supplied curves match **exactly (max absolute difference zero)**. There is a deliberate `curve` exception: `rec_printed` is *not* made monotonic (it describes the current model's recommendation, not best demonstrated value). A first-crossing helper uses a 1e-12 tolerance for mean curves, whereas `cost_to` uses a strict comparison; no printed benchmark change arose from that difference.

`matched_idx` and `paired` sort/intersect explicit seed IDs, not positional indices. I tested deliberately shuffled IDs `[7,0,2]` against `[2,3,7]` and obtained pairs `(2,2),(7,7)`, then checked all actual run keys are unique. `paired` calls the two-sided signed-rank test and includes zero differences via SciPy's default zero handling. The speed-up's matched bootstrap does align IDs, but switches to their intersection for both curves; it does **not** preserve the 20-seed baseline target from the mixed-sample estimate.

## 3. Target sensitivity, inference and wording — **executed plus policy interpretation inspected**

For fixed target levels of the (1,1) optimum, first crossing of each **mean** curve is:

| Policy | 55% | 60% | 65% |
|---|---|---|---|
| pKGFN, production | $100,000 | not reached | not reached |
| pKGFN, light | $100,000 | not reached | not reached |
| BOFN, full | $76,250 | $85,750 | $85,750 |
| BOFN + reuse | $65,750 | $71,000 | $81,000 |
| Tiered, spec | not reached | not reached | not reached |
| Tiered, Ni floor | not reached | not reached | not reached |
| Tiered, Ni + reference | not reached | not reached | not reached |
| Standard BO | not reached | not reached | not reached |
| Random | not reached | not reached | not reached |

At fixed **55%**, production pKGFN reaches its target only at the $100k endpoint, versus $76,250 for full BOFN and $65,750 for reuse; at **60% and 65% its seven-seed mean never reaches the target**, while full BOFN needs $85,750 at both 60% and 65% and reuse needs $71,000 and $81,000, respectively. The low 24.23% reference target and the negative spec-tiered target strongly affect the apparent “speed-up.” No single speed-up factor is stable across scientifically plausible outcome levels. A first-crossing of a mean is **not** the median first-crossing of seeds (e.g. production pKGFN mean never reaches 60%, but its per-seed median 60% cost is $100k).

A **standard error** is not a 90% confidence interval. The supplied `±` is further understated by ddof=0; selection of only completed production seeds is not included in any interval. Percentile bootstraps are non-smooth near no crossing, zero spend and the terminal grid point. Interpret their quantiles conditionally on the stored seeds and the chosen simulator, not as proof that an implementation generalizes to new physical alloys. README's “aluminum headline does not carry over” is fair *for this stored implementation*, but “the reason is clear: the immersion gate” overstates identification: the no-gate comparison changes policy choices as well as the objective; only random holds designs fixed. The causal assertion that BOFN “learns [the gate] from intermediate measurements” is a plausible mechanism, **not measured directly by the JSONs**. Synthetic hand-chosen functions, noiseless observations, an uncalibrated deposit-quality index (not literal relative density), an optimistic known-reference-coupon screen, and no physical data make external/physical performance an open question. The optimum-fails-CALPHAD restriction is verifiable from `truth_tables.json`; the one-hour screen does **not** exclude the optimum, as the README itself notes. Thus I would not attribute all copper-vs-aluminum differences to an immersion screen or claim the best method is partial stage selection.

**Most defensible single preliminary-results sentence:** “In a synthetic, deliberately biased copper directed-energy-deposition benchmark, full-pipeline function-network Bayesian optimization demonstrated alloys averaging 73% of the modeled optimum after $100,000 of new purchases (20 seeds), versus 24% for corrosion-informed tiered screening (20 seeds) and 14% for standard Bayesian optimization (20 seeds); a seven-seed production-setting partial-stage knowledge-gradient implementation averaged 59% and did not establish an advantage over full-pipeline search.”

As a supplemental check, I transcribed the no-gate truth into NumPy and independently optimized it by three SciPy differential-evolution starts: **0.74505147885**. The 80 no-gate files reproduce README's mean $100k percentages (BOFN reuse 87.555%, full 84.774%, standard BO 65.156%, random 50.867%); the 26 random-design records per seed are identical between gate/no-gate. Other policies choose different designs, so this is a *compound ablation*, not an identified share of their performance loss.

| No-gate policy | n | $25k | $50k | $100k |
|---|---|---|---|---|
| Standard BO | 20 | 38.946 ± 5.954 | 48.801 ± 5.529 | 65.156 ± 4.610 |
| BOFN, full | 20 | 43.726 ± 6.110 | 66.782 ± 5.148 | 84.774 ± 4.853 |
| BOFN + reuse | 20 | 47.117 ± 5.653 | 71.171 ± 3.539 | 87.555 ± 2.198 |
| Random | 20 | 43.248 ± 4.543 | 47.334 ± 3.618 | 50.867 ± 3.300 |

## 4. The uploaded proposal PNG — **actual raster read and figure code inspected**

`bofn_cu_best_vs_spend_k1_partial_vs_full.png` is an 11×6.2-inch, 300-dpi raster. I read positions against its graph coordinates and checked its curves against the independent JSON reconstructions; raster-level values are approximate (typically within ~0.6 point). The pKGFN red solid curve is **light-settings, 20 seeds**, not the production-setting seven-seed curve. The plot has five policies, with no plotted corrosion-aware baseline:

| Trace in uploaded PNG | Visual ~25k / 50k / 100k (% optimum) | Exact independent curve at 25k / 50k / 100k |
|---|---|---|
| Solid red “Partial: pKGFN” (light) | ~12 / 27 / 59 | 11.951 / 27.440 / 58.552 |
| Dashed red “Partial: BOFN + reuse” | ~14 / 32 / 72 | 14.353 / 32.274 / 72.033 |
| Dark “Full: BOFN” | ~15 / 39 / 73 | 14.977 / 38.774 / 73.212 |
| Light gray “Full: standard BO” | ~6 / 7 / 14 | 5.680 / 7.180 / 14.421 |
| Gray “Tiered screening” (spec) | ~−9 / −9 / −8 | −9.427 / −9.106 / −7.691 |

The start level for the 20-seed traces is **−9.610%** (axis label −10); the current production-figure variant starts at **−13.831%** on its seven pKGFN seeds (axis label −14). **There is no called-out spend or horizontal target level in this uploaded figure**: plot code disables the callout when the baseline is the uninformative negative-valued spec-tiered rule. Its *unplotted* corresponding pair would be **$5,750 and −7.691%** for light pKGFN versus **$99,250 and −7.691%** for spec tiered; for the corrosion-informed comparison it would be **$46,750 and +24.233%** for light pKGFN versus **$100,000 and +24.233%** for the reference baseline. Do not invent a callout from a figure that has none.

At 3.1 inches wide, the plotting code scales its nominal 24-pt source labels to ~6.8 pt, and plot data use ~53% of the source width (~1.64 inches at proposal size). Its x axis labels only 0 and 100, its y axis only −10 and 73, with **no zero line**. Light gray standard BO and near-flat tiered traces can disappear into the background. Red and spec-tiered **±one (population-based) SE** ribbons appear, while full BOFN and standard BO lack ribbons: do not read missing shading as greater precision. Two red traces suggest “partial” has a single benefit, though BOFN reuse tests every purchased Mines build downstream, and pKGFN is the actual stage selector. Add `light n=20` (or replace with the current n=7 curve), state bands/seed counts, include a visible 0% line and intermediate spend ticks, and distinguish reuse from stage selection. If claiming the 3× result, use the corrosion-informed reference baseline, not this old plot; label its exact comparator and target.

## 5. Purchases and run pathology — **executed; mechanisms inspected**

I reconciled **all 179 main+light run ledgers exactly** against eight stage counts, the $1,600-per-paid-scale-up capacity of four sessions per lot, the five pre-existing seed lots, and final stored spend. Every new build count equals new Mines purchases; each stage completion count S/T/K/I equals its populated build field. This independently checks `tables.md`'s purchase table below (values are **my unrounded means per run**, excluding five shared seed builds and lots; the supplied table rounds to one decimal). `C` denotes CALPHAD, `A` atomization, `U` Utah small deposition, `M` Mines large deposition, `S` microscopy, `T` tensile, `K` one-hour screen, `I` immersion.

| Policy | C | A | U | M | S | T | K | I | Validated builds | Paid scale-ups |
|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN, production | 4.57 | 17.57 | 16.29 | 37.86 | 13.43 | 5.86 | 11.86 | 11.29 | 5.29 | 12.71 |
| pKGFN, light | 6.70 | 12.45 | 11.30 | 40.50 | 15.70 | 7.20 | 14.00 | 12.85 | 6.15 | 12.30 |
| BOFN, full | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 |
| BOFN + reuse | 12.55 | 12.55 | 12.55 | 29.30 | 29.30 | 29.30 | 29.30 | 29.30 | 29.30 | 13.40 |
| Tiered, spec | 224.00 | 22.80 | 44.25 | 24.85 | 24.85 | 24.85 | 24.85 | 4.00 | 4.00 | 11.00 |
| Tiered, Ni floor | 224.00 | 31.00 | 67.40 | 18.35 | 18.35 | 18.35 | 18.35 | 2.55 | 2.55 | 9.75 |
| Tiered, Ni + reference | 224.00 | 26.50 | 53.65 | 21.15 | 21.15 | 21.15 | 21.15 | 9.90 | 9.90 | 10.10 |
| Standard BO | 19.70 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 |
| Random | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 | 21.00 |

- **What was bought.** BOFN full, standard BO and random run ~21 complete eight-stage chains (standard BO saves 1.3 CALPHAD calls on previously known compositions). BOFN reuse runs **12.55 new lots and 29.30 fully tested Mines sessions**. Spec tiered performs **224 new CALPHAD screens**, ~22.8 atomizations, 44.25 Utah visits, 24.85 Mines sessions, only **4.0 immersions**. Ni-floor tiered performs 31.0 lots, 67.4 Utah visits, 18.35 Mines sessions and **2.55 immersions**. Reference-gated Ni tiered performs 26.5 lots, 53.65 Utah visits, 21.15 Mines sessions, **9.9 immersions** with **2.65 hard passes** on average. Production pKGFN does only **4.57 CALPHAD calls**, but **37.86 Mines sessions on 17.57 new lots**, only **5.86 tensile** and **11.29 immersion** purchases, and **5.29 completely validated new builds**; buying immersion and tensile on different builds does not validate both. The five shared fully tested seed builds are excluded throughout.
- **Repeated purchases:** no duplicate exact stored builds or Utah sessions in any main/light run; no duplicate lots except *standard BO seed 19*, which atomizes exactly the same serialized `(composition, atomizer setting)=(0,0,1,0,0)` a second time (lot indices 14 and 20). These are checks of stored/rounded identities, not proof of equality at unlimited floating precision. There are many **intentional repeat Mines sessions** on distinct settings of the same lot. The cost ledger does not show free/reused identical purchases by accident.
- **Budget and stalls:** all headline runs end between **$97,790 and $100,000**; none ends far below $100k. Spec tiered has **15/20 runs with zero improvement from the initial validated best**, Ni-floor tiered **11/20**, reference-gated tiered **3/20**, random **4/20**. High-setting pKGFN can spend up to **$77,900** in a contiguous no-improvement run (seed 2); the longest contiguous run of new actions costing ≤$500 each without improving the validated best is **10 actions/$3,510** (seed 5). Light pKGFN has up to **20 such actions/$5,570** (seed 15) or **16 actions/$7,900** (seed 14). At $99,750 the production pKGFN mean is **46.214%**, versus **58.856%** at $100k, because seeds **3, 5, 7** finalize gains of ~20.77, 48.01 and 19.70 points during that last grid interval. The end figure and $100k medians therefore depend strongly on near-budget validation.
- **Unfinished builds:** production pKGFN deposits ~37.86 new builds but validates ~5.29; ~26.00 new builds have **neither tensile nor immersion**, ~32.00 have no tensile and ~26.57 have no immersion. Light pKGFN: 40.50 deposited, 6.15 validated, 26.60 with neither test. Full BOFN validates all 21. For an upper bound using the synthetic truth on *all* stored deposited designs (including five seed designs), my independently transcribed oracle scores production pKGFN **70.817%** versus **58.856% demonstrated**, light **68.496%** versus **58.552% demonstrated**. This is an unavailable oracle, not prospective achievable policy performance; serialized compositions rounded to four decimals make the re-evaluated oracle approximate.

**Flat knowledge-gradient (KG) diagnostic, production pKGFN:**

| Seed | Fallback actions / all | Share | Spend on fallback | New validated / deposited |
|---|---|---|---|---|
| 0 | 1/86 | 1.2% | $100 | 4/44 |
| 1 | 68/97 | 70.1% | $62,650 | 6/33 |
| 2 | 69/103 | 67.0% | $67,750 | 3/32 |
| 3 | 3/90 | 3.3% | $750 | 5/44 |
| 4 | 28/105 | 26.7% | $29,600 | 8/39 |
| 5 | 5/103 | 4.9% | $800 | 5/42 |
| 7 | 93/105 | 88.6% | $90,800 | 6/31 |

Production pKGFN has **267/689=38.75%** fallback-marked purchases (README's “39%” and `tables.md` pooled 26% across high and light reproduce), spending ~**36.08%** of its new budget on flagged purchases. On seeds 1, 2 and 7 the fallback takes **70.1%, 67.0%, 88.6%** of their actions (seed 4 takes 26.7%; other seeds ~1.2%, 3.3%, 4.9%). In the before-state J≤0, **255/383=66.6%** of purchases are fallback, compared with **12/306=3.9%** after first J>0; light has **380/907=41.9%** before and **38/1,037=3.7%** after. Source code marks fallback when estimated KG per dollar is below **1e−10** or no eligible KG candidate remains, and buys a one-step action using a path-priced EI heuristic or an optimistic posterior sample. The flag is evidence of *this discretized numerical acquisition being near-flat*, **not** proof mathematical knowledge gradient is exactly zero, nor proof the fallback buys an optimal path. The flag does not indicate which of its two fallback subbranches was used; action labels cannot identify that. It is consistent with delayed rewards and an unfinished-validation backlog, but this is mechanistic interpretation, not a controlled intervention.

## 6. Sensitivity cells and proposed new policies — **executed where files exist; remainder inspected only**

At (0,0), normalized by `truth_tables.json`'s optimum **0.381561510051002**, I independently find:

| Cell (0,0) policy | n | $25k | $50k | $100k |
|---|---|---|---|---|
| pKGFN, light | 10 | -5.622 ± 4.724 | -0.356 ± 3.836 | 9.373 ± 7.474 |
| BOFN, full | 1 | 11.831 ± not estimable | 19.487 ± not estimable | 92.255 ± not estimable |
| BOFN + reuse | 1 | 11.831 ± not estimable | 67.672 ± not estimable | 95.195 ± not estimable |

These reproduce the rounded (0,0) table: light pKGFN −6±4, approximately 0±4, 9±7 (the $25k **sample** SE is ~5, not 4); full BOFN 12,19,92; reuse 12,68,95. **n=1 means no between-seed SE for either BOFN row and no valid method comparison.** No stored JSONs exist for sensitivity cells (1,0) or (0,1), and (0,0) has no production pKGFN, tiered, standard BO, random, screen/audit, mine-only or funnel result. `tables.md`'s populated sensitivity entries agree at its reporting precision; blank cells really mean absent runs, not zero performance. README's phrases “both screens right” and “robust to screen bias” cannot be inferred from these sparse cells.

I enumerated every kind in `results/` and `quality/results-light/`: **no `pkgfn_screen`, `pkgfn_audit`, `mines_only` or `funnel` files**. Consequently the screen-audit and fixed-funnel result tables are empty and the two-step DED split table is not rendered at all in `tables.md`; I **inspected only** their `analyze.py` implementations and README policy descriptions, and did not manufacture outcome values. In particular, the audit method's final-gate truth check and near-cutoff oversampling cannot be validated as an empirical estimator without audit logs. The code's current implementation offers *questions to test*, not evidence that a Utah step, a trusting screen, auditing or fixed top-k funnel helps. The same caveat applies to the unfinished S=256 fidelity check.

## Verification record, artifacts, and limits

| Check | Status | Evidence |
|---|---|---|
| Read settings, exact optima, inventories; reconstruct all 179 main/light curves with NumPy before opening supplied aggregator | **Executed** | `outputs/independent_core.py`, `outputs/independent_summary.csv`; max supplied-versus-independent curve error = **0** |
| Headline means, sample SE, medians, paired Wilcoxon, both baseline speed-ups and both bootstrap schemes | **Executed** | `outputs/all_SE_comparisons.csv`, `independent_paired.csv`, `independent_speedups.csv`, `replicated_bootstrap.csv`; exact 2,000-replicate bootstrap replication matches supplied |
| Regenerate supplied `tables.md` with pure NumPy analysis functions while avoiding torch import/new truth optimization | **Executed** | `outputs/supplied_tables_regenerated.md`; **zero differing lines** versus uploaded `tables.md` |
| Synthetic step-function edge cases; shuffled seed IDs; original cost-and-capacity reconciliation; build statuses and actions | **Executed** | Edge-case test outputs; `outputs/inventory_cost_ledger.csv` (179/179 exact), `action_audit_per_seed.csv` |
| Target sensitivity, Holm corrections, matched high-v-light comparisons and paired-bootstrap interval | **Executed** | `fixed_target_costs.csv`, `all_policy_pairs.csv`, `independent_paired.csv`; bootstrap seed 20261027 |
| Actual original PNG and plot code; approximate trace read-offs | **Executed raster/inspected code** | `outputs/figure_raster_readings.csv`; displayed pixel checks above |
| No-gate optimum and four-policy JSON summary; random same-design check | **Executed** | `outputs/nogate_summary.csv`; SciPy/NumPy truth transcription; no aluminum JSONs supplied, so prior aluminum comparison **not re-executed** |
| Metallurgical plausibility, BoTorch/GP implementations, F2/F4 correctness, physical density calibration, new policies' behavior | **Inspected only / not established** | Source descriptions; no new training, experimental measurements, or absent run files |

I treated the seven completed high-fidelity pKGFN seeds as a **nonrandom convenience subset**; intervals conditional on them do not account for incomplete uploads. I chose sample SD for a conventional between-seed SE (instead of retaining the supplied population SD), both independent and matched seed bootstraps to expose different estimands, and a 108-test all-policy family only as a conservative multiplicity sensitivity check. No web source was needed; every factual input here is a supplied file or an executed reconstruction. Reproducibility and detailed decimal-level audits are in `outputs/`; original inputs were not modified.

**Reproducibility check:** I also executed `outputs/audit_reproduce.py` in a fresh Python process: exit code 0, no stderr; the generated final report matched exactly. The replayable notebook is `outputs/audit_notebook.ipynb`.

**Discretionary analytical decisions**
- I used the exact uploaded optima rather than re-optimizing the gated truth: the requested metric depends on the benchmark's stipulated normalization; the separate no-gate optimum required an independent reconstruction because its landscape JSON was absent.
- I report sample-SD standard errors rather than the supplied population-SD convention, since seeds represent replicate runs and n=1 cannot estimate a between-seed error; I preserve the supplied numbers side by side for auditability.
- I keep `∞` for censored threshold costs and call zero-cost bootstrap crossings undefined/infinite instead of interpreting the supplied $250 floor as experimental spend.
- I present matched and independent resampling separately and explicitly recompute the matched-sample point estimate, because matching changes the target when one policy has 7 rather than 20 seeds.
- I use fixed 55/60/65% targets alongside baseline-endpoint targets to test sensitivity without substituting a favorable single threshold, and apply Holm corrections as a conservative illustration rather than post hoc confirmatory inference.
- I characterize missing runs as unavailable, not poor results, and describe physical explanations as hypotheses because the task supplies a hand-built noiseless simulator, not measured validation.
