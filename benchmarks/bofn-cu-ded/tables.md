# Tables (written by `analyze.py`)

Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.

## Cell (kappa, eta) = (1, 1): both screens biased; optimum J* = 0.492

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60% of seeds) | >$100k (35% of seeds) | >$100k (5% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 14% ± 5 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| Tiered screening | 20 | -9% ± 5 | -9% ± 5 | -8% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 19% ± 6 | 37% ± 7 | 68% ± 4 | $52k (80% of seeds) | $78k (60% of seeds) | >$100k (25% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 13% ± 4 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| Tiered screening | 20 | -8% ± 5 | -8% ± 5 | -6% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Speed-up over tiered screening

Target: tiered screening's mean at $100k, -7.7% of the optimum, which it first reaches at $99k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | $6k | **17.3×** | 5.8–397.0 | 12.0–21.9 | 0.99 |
| BOFN + lot reuse | 20 | $5k | **19.9×** | 10.9–397.0 | 18.4–43.9 | 1.00 |
| BOFN, full pipeline | 20 | $5k | **19.9×** | 18.4–397.0 | 18.4–19.9 | 0.99 |
| Standard BO | 20 | $5k | **19.9×** | 5.2–397.0 | 18.4–19.9 | 0.98 |
| Random | 20 | $10k | **10.2×** | 2.3–397.0 | 9.4–19.9 | 0.87 |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|
| Tiered screening | 20 | +21 points (16/4/0; p = 0.00044) | +37 points (20/0/0; p = 1.9e-06) | +66 points (20/0/0; p = 1.9e-06) |
| BOFN, full pipeline | 20 | -3 points (3/1/16; p = 0.07) | -11 points (6/0/14; p = 0.23) | -15 points (4/0/16; p = 0.024) |
| BOFN + lot reuse | 20 | -2 points (4/2/14; p = 0.16) | -5 points (8/0/12; p = 0.65) | -13 points (2/0/18; p = 0.0094) |
| Standard BO | 20 | +6 points (5/3/12; p = 0.62) | +20 points (12/0/8; p = 0.019) | +44 points (17/0/3; p = 4.8e-05) |
| Random | 20 | +13 points (14/3/3; p = 0.0075) | +21 points (16/0/4; p = 0.012) | +36 points (19/0/1; p = 3.6e-05) |

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 | 12.4 | 12.3 |
| BOFN, full pipeline | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 20 | 12.6 | 12.6 | 12.6 | 29.3 | 29.3 | 29.3 | 29.3 | 29.3 | 12.6 |  |
| Tiered screening | 20 | 224.0 | 22.8 | 44.2 | 24.9 | 24.9 | 24.9 | 24.9 | 4.0 | 22.8 |  |
| Standard BO | 20 | 19.7 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |

## Sensitivity over the four cells

At $100k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 59% ± 5 (n = 20) |  |  |  |
| BOFN, full pipeline | 73% ± 7 (n = 20) |  |  |  |
| BOFN + lot reuse | 72% ± 7 (n = 20) |  |  |  |
| Tiered screening | -8% ± 5 (n = 20) |  |  |  |
| Standard BO | 14% ± 6 (n = 20) |  |  |  |
| Random | 22% ± 5 (n = 20) |  |  |  |

At $50k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 27% ± 7 (n = 20) |  |  |  |
| BOFN, full pipeline | 39% ± 9 (n = 20) |  |  |  |
| BOFN + lot reuse | 32% ± 8 (n = 20) |  |  |  |
| Tiered screening | -9% ± 5 (n = 20) |  |  |  |
| Standard BO | 7% ± 3 (n = 20) |  |  |  |
| Random | 7% ± 5 (n = 20) |  |  |  |

## Screen audit (Advance 5)

From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. `m_ref` = 0.849. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.

| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |
|---|---|---|---|---|---|---|---|

## Quality: GP fits and the KG fallback

| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |
|---|---|---|---|---|
| (1, 1) | 120 | 39,374 | 0 | 22% of 1,944 |

