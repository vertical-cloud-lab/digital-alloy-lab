# Tables (written by `analyze.py`)

Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.

## Cell (kappa, eta) = (1, 1): both screens biased; optimum J* = 0.492

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 14% ± 5 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| pKGFN, light MC settings (first sweep) | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60% of seeds) | >$100k (35% of seeds) | >$100k (5% of seeds) |
| Tiered screening | 20 | -9% ± 5 | -9% ± 5 | -8% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt% shortlist | 2 | -9% ± 18 | -9% ± 18 | -9% ± 18 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt%, 90-10 coupon gate | 2 | 10% ± 8 | 10% ± 8 | 34% ± 19 | >$100k (50% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 13% ± 4 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| pKGFN, light MC settings (first sweep) | 20 | 19% ± 6 | 37% ± 7 | 68% ± 4 | $52k (80% of seeds) | $78k (60% of seeds) | >$100k (25% of seeds) |
| Tiered screening | 20 | -8% ± 5 | -8% ± 5 | -6% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt% shortlist | 2 | 3% ± 10 | 3% ± 9 | 2% ± 10 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt%, 90-10 coupon gate | 2 | 10% ± 8 | 7% ± 6 | 34% ± 19 | >$100k (50% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Speed-up over tiered screening

Target: tiered screening's mean at $100k, -7.7% of the optimum, which it first reaches at $99k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| BOFN + lot reuse | 20 | $5k | **19.9×** | 10.9–397.0 | 18.4–43.9 | 1.00 |
| BOFN, full pipeline | 20 | $5k | **19.9×** | 18.4–397.0 | 18.4–19.9 | 0.99 |
| Standard BO | 20 | $5k | **19.9×** | 5.2–397.0 | 18.4–19.9 | 0.98 |
| Random | 20 | $10k | **10.2×** | 2.3–397.0 | 9.4–19.9 | 0.87 |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 20 | 12.6 | 12.6 | 12.6 | 29.3 | 29.3 | 29.3 | 29.3 | 29.3 | 12.6 |  |
| pKGFN, light MC settings (first sweep) | 20 | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 | 12.4 |  |
| Tiered screening | 20 | 224.0 | 22.8 | 44.2 | 24.9 | 24.9 | 24.9 | 24.9 | 4.0 | 22.8 |  |
| Tiered, Ni ≥ 10 wt% shortlist | 2 | 224.0 | 38.5 | 94.5 | 12.0 | 12.0 | 12.0 | 12.0 | 2.0 | 38.5 |  |
| Tiered, Ni ≥ 10 wt%, 90-10 coupon gate | 2 | 224.0 | 19.0 | 32.5 | 27.0 | 27.0 | 27.0 | 28.0 | 12.0 | 19.0 |  |
| Standard BO | 20 | 19.7 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |

### Immersion outcomes (new builds only)

| Policy | n | immersions per run | passing immersions per run | seeds with a passing alloy | lowest Ni (wt%) among passing builds |
|---|---|---|---|---|---|
| BOFN, full pipeline | 20 | 21.0 | 7.5 | 17/20 | 8.2 |
| BOFN + lot reuse | 20 | 29.3 | 11.1 | 17/20 | 9.6 |
| pKGFN, light MC settings (first sweep) | 20 | 12.8 | 4.5 | 19/20 | 10.7 |
| Tiered screening | 20 | 4.0 | 0.0 | 0/20 | none |
| Tiered, Ni ≥ 10 wt% shortlist | 2 | 2.0 | 0.0 | 0/2 | none |
| Tiered, Ni ≥ 10 wt%, 90-10 coupon gate | 2 | 12.0 | 7.0 | 1/2 | 10.1 |
| Standard BO | 20 | 21.0 | 1.6 | 5/20 | 12.1 |
| Random | 20 | 21.0 | 1.0 | 12/20 | 12.0 |

## Cell (kappa, eta) = (0, 0): both screens right; optimum J* = 0.382

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 1 | 12% ± 0 | 19% ± 0 | 92% ± 0 | $52k (100% of seeds) | $72k (100% of seeds) | $76k (100% of seeds) |
| BOFN + lot reuse | 1 | 12% ± 0 | 68% ± 0 | 95% ± 0 | $46k (100% of seeds) | $54k (100% of seeds) | $58k (100% of seeds) |
| pKGFN, light MC settings (first sweep) | 10 | -6% ± 4 | -0% ± 4 | 9% ± 7 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 1 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 1 | 10.0 | 10.0 | 10.0 | 31.0 | 31.0 | 31.0 | 31.0 | 31.0 | 10.0 |  |
| pKGFN, light MC settings (first sweep) | 10 | 3.8 | 17.9 | 10.3 | 39.1 | 12.0 | 6.4 | 11.4 | 9.2 | 17.9 |  |

### Immersion outcomes (new builds only)

| Policy | n | immersions per run | passing immersions per run | seeds with a passing alloy | lowest Ni (wt%) among passing builds |
|---|---|---|---|---|---|
| BOFN, full pipeline | 1 | 21.0 | 11.0 | 1/1 | 9.4 |
| BOFN + lot reuse | 1 | 31.0 | 10.0 | 1/1 | 8.9 |
| pKGFN, light MC settings (first sweep) | 10 | 9.2 | 0.3 | 1/10 | 10.1 |

## Sensitivity over the four cells

At $100k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| BOFN, full pipeline | 73% ± 7 (n = 20) | 92% ± 0 (n = 1) |  |  |
| BOFN + lot reuse | 72% ± 7 (n = 20) | 95% ± 0 (n = 1) |  |  |
| pKGFN, light MC settings (first sweep) | 59% ± 5 (n = 20) | 9% ± 7 (n = 10) |  |  |
| Tiered screening | -8% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10 wt% shortlist | -9% ± 18 (n = 2) |  |  |  |
| Tiered, Ni ≥ 10 wt%, 90-10 coupon gate | 34% ± 19 (n = 2) |  |  |  |
| Standard BO | 14% ± 6 (n = 20) |  |  |  |
| Random | 22% ± 5 (n = 20) |  |  |  |

At $50k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| BOFN, full pipeline | 39% ± 9 (n = 20) | 19% ± 0 (n = 1) |  |  |
| BOFN + lot reuse | 32% ± 8 (n = 20) | 68% ± 0 (n = 1) |  |  |
| pKGFN, light MC settings (first sweep) | 27% ± 7 (n = 20) | -0% ± 4 (n = 10) |  |  |
| Tiered screening | -9% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10 wt% shortlist | -9% ± 18 (n = 2) |  |  |  |
| Tiered, Ni ≥ 10 wt%, 90-10 coupon gate | 10% ± 8 (n = 2) |  |  |  |
| Standard BO | 7% ± 3 (n = 20) |  |  |  |
| Random | 7% ± 5 (n = 20) |  |  |  |

## Screen audit (Advance 5)

From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. `m_ref` = 0.849. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.

| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |
|---|---|---|---|---|---|---|---|

## Quality: GP fits and the KG fallback

| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |
|---|---|---|---|---|
| (1, 1) | 124 | 43,050 | 0 | 0% of 0 |
| (0, 0) | 12 | 1,919 | 0 | 0% of 0 |

