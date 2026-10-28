# Tables (written by `analyze.py`)

Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.

## Cell (kappa, eta) = (1, 1): both screens biased; optimum J* = 0.492

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 4 | 4% ± 8 | 44% ± 15 | 64% ± 6 | >$100k (50% of seeds) | >$100k (50% of seeds) | >$100k (0% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 14% ± 5 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| pKGFN, light settings | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60% of seeds) | >$100k (35% of seeds) | >$100k (5% of seeds) |
| Tiered screening | 20 | -9% ± 5 | -9% ± 5 | -8% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10% | 20 | -7% ± 5 | 1% ± 5 | 6% ± 6 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10%, coupon gate | 20 | 8% ± 4 | 16% ± 4 | 23% ± 5 | >$100k (10% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 4 | 7% ± 10 | 47% ± 15 | 78% ± 1 | $50k (100% of seeds) | $57k (100% of seeds) | >$100k (25% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 13% ± 4 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| pKGFN, light settings | 20 | 19% ± 6 | 37% ± 7 | 68% ± 4 | $52k (80% of seeds) | $78k (60% of seeds) | >$100k (25% of seeds) |
| Tiered screening | 20 | -8% ± 5 | -8% ± 5 | -6% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10% | 20 | 2% ± 4 | 7% ± 4 | 9% ± 4 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10%, coupon gate | 20 | 8% ± 4 | 15% ± 4 | 23% ± 5 | >$100k (10% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Speed-up over tiered screening

Target: tiered screening's mean at $100k, -7.7% of the optimum, which it first reaches at $99k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 4 | $9k | **10.7×** | 3.5–397.0 | 4.5–16.0 | 0.96 |
| BOFN + lot reuse | 20 | $5k | **19.9×** | 10.9–397.0 | 18.4–43.9 | 1.00 |
| BOFN, full pipeline | 20 | $5k | **19.9×** | 18.4–397.0 | 18.4–19.9 | 0.99 |
| Standard BO | 20 | $5k | **19.9×** | 5.2–397.0 | 18.4–19.9 | 0.98 |
| Random | 20 | $10k | **10.2×** | 2.3–397.0 | 9.4–19.9 | 0.87 |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|
| Tiered screening | 4 | +20 points (4/0/0; p = 0.12) | +59 points (4/0/0; p = 0.12) | +75 points (4/0/0; p = 0.12) |
| Tiered, Ni ≥ 10% | 4 | +21 points (4/0/0; p = 0.12) | +61 points (4/0/0; p = 0.12) | +64 points (4/0/0; p = 0.12) |
| Tiered, Ni ≥ 10%, coupon gate | 4 | +3 points (2/0/2; p = 0.62) | +32 points (3/0/1; p = 0.38) | +39 points (3/0/1; p = 0.25) |
| BOFN, full pipeline | 4 | -18 points (0/0/4; p = 0.12) | +9 points (2/0/2; p = 0.88) | -25 points (0/0/4; p = 0.12) |
| BOFN + lot reuse | 4 | -22 points (0/0/4; p = 0.12) | -15 points (1/0/3; p = 0.62) | -2 points (1/0/3; p = 0.88) |
| Standard BO | 4 | +2 points (1/0/3; p = 0.88) | +40 points (3/0/1; p = 0.25) | +47 points (3/0/1; p = 0.25) |
| Random | 4 | +12 points (4/0/0; p = 0.12) | +46 points (4/0/0; p = 0.12) | +41 points (3/0/1; p = 0.25) |
| pKGFN, light settings | 4 | +1 points (2/0/2; p = 0.88) | +21 points (4/0/0; p = 0.12) | +2 points (2/0/2; p = 0.88) |

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 4 | 6.8 | 14.2 | 17.8 | 39.5 | 17.8 | 7.8 | 15.2 | 14.0 | 14.2 | 10.2 |
| BOFN, full pipeline | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 20 | 12.6 | 12.6 | 12.6 | 29.3 | 29.3 | 29.3 | 29.3 | 29.3 | 12.6 |  |
| pKGFN, light settings | 20 | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 | 12.4 |  |
| Tiered screening | 20 | 224.0 | 22.8 | 44.2 | 24.9 | 24.9 | 24.9 | 24.9 | 4.0 | 22.8 |  |
| Tiered, Ni ≥ 10% | 20 | 224.0 | 31.6 | 68.0 | 18.0 | 18.0 | 18.0 | 18.0 | 2.1 | 31.6 |  |
| Tiered, Ni ≥ 10%, coupon gate | 20 | 224.0 | 26.6 | 55.0 | 21.1 | 21.1 | 21.1 | 22.1 | 9.1 | 26.6 |  |
| Standard BO | 20 | 19.7 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |

### Immersion outcomes (new builds only)

| Policy | n | immersions per run | passing immersions per run | seeds with a passing alloy | lowest Ni (wt%) among passing builds |
|---|---|---|---|---|---|
| pKGFN: picks the stage | 4 | 14.0 | 6.2 | 4/4 | 8.8 |
| BOFN, full pipeline | 20 | 21.0 | 7.5 | 17/20 | 8.2 |
| BOFN + lot reuse | 20 | 29.3 | 11.1 | 17/20 | 9.6 |
| pKGFN, light settings | 20 | 12.8 | 4.5 | 19/20 | 10.7 |
| Tiered screening | 20 | 4.0 | 0.0 | 0/20 | none |
| Tiered, Ni ≥ 10% | 20 | 2.1 | 0.5 | 4/20 | 11.0 |
| Tiered, Ni ≥ 10%, coupon gate | 20 | 9.1 | 2.6 | 10/20 | 10.1 |
| Standard BO | 20 | 21.0 | 1.6 | 5/20 | 12.1 |
| Random | 20 | 21.0 | 1.0 | 12/20 | 12.0 |

## Cell (kappa, eta) = (0, 0): both screens right; optimum J* = 0.382

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 1 | 12% ± 0 | 19% ± 0 | 92% ± 0 | $52k (100% of seeds) | $72k (100% of seeds) | $76k (100% of seeds) |
| BOFN + lot reuse | 1 | 12% ± 0 | 68% ± 0 | 95% ± 0 | $46k (100% of seeds) | $54k (100% of seeds) | $58k (100% of seeds) |
| pKGFN, light settings | 10 | -6% ± 4 | -0% ± 4 | 9% ± 7 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BOFN, full pipeline | 1 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 1 | 10.0 | 10.0 | 10.0 | 31.0 | 31.0 | 31.0 | 31.0 | 31.0 | 10.0 |  |
| pKGFN, light settings | 10 | 3.8 | 17.9 | 10.3 | 39.1 | 12.0 | 6.4 | 11.4 | 9.2 | 17.9 |  |

### Immersion outcomes (new builds only)

| Policy | n | immersions per run | passing immersions per run | seeds with a passing alloy | lowest Ni (wt%) among passing builds |
|---|---|---|---|---|---|
| BOFN, full pipeline | 1 | 21.0 | 11.0 | 1/1 | 9.4 |
| BOFN + lot reuse | 1 | 31.0 | 10.0 | 1/1 | 8.9 |
| pKGFN, light settings | 10 | 9.2 | 0.3 | 1/10 | 10.1 |

## Sensitivity over the four cells

At $100k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 64% ± 6 (n = 4) |  |  |  |
| BOFN, full pipeline | 73% ± 7 (n = 20) | 92% ± 0 (n = 1) |  |  |
| BOFN + lot reuse | 72% ± 7 (n = 20) | 95% ± 0 (n = 1) |  |  |
| pKGFN, light settings | 59% ± 5 (n = 20) | 9% ± 7 (n = 10) |  |  |
| Tiered screening | -8% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10% | 6% ± 6 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10%, coupon gate | 23% ± 5 (n = 20) |  |  |  |
| Standard BO | 14% ± 6 (n = 20) |  |  |  |
| Random | 22% ± 5 (n = 20) |  |  |  |

At $50k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 44% ± 15 (n = 4) |  |  |  |
| BOFN, full pipeline | 39% ± 9 (n = 20) | 19% ± 0 (n = 1) |  |  |
| BOFN + lot reuse | 32% ± 8 (n = 20) | 68% ± 0 (n = 1) |  |  |
| pKGFN, light settings | 27% ± 7 (n = 20) | -0% ± 4 (n = 10) |  |  |
| Tiered screening | -9% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10% | 1% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10%, coupon gate | 16% ± 4 (n = 20) |  |  |  |
| Standard BO | 7% ± 3 (n = 20) |  |  |  |
| Random | 7% ± 5 (n = 20) |  |  |  |

## Screen audit (Advance 5)

From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. `m_ref` = 0.849. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.

| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |
|---|---|---|---|---|---|---|---|

## Quality: GP fits and the KG fallback

| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |
|---|---|---|---|---|
| (1, 1) | 164 | 75,471 | 0 | 25% of 429 |
| (0, 0) | 12 | 1,919 | 0 | 0% of 0 |

