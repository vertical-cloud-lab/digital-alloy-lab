# Tables (written by `analyze.py`)

Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.

## Cell (kappa, eta) = (1, 1): both screens biased; optimum J* = 0.429

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 1 | 18% ± 0 | 32% ± 0 | 71% ± 0 | $100k (100% of seeds) | $100k (100% of seeds) | >$100k (0% of seeds) |
| BOFN, full pipeline | 6 | 18% ± 8 | 53% ± 16 | 76% ± 14 | $38k (83% of seeds) | $50k (83% of seeds) | $76k (67% of seeds) |
| BOFN + lot reuse | 6 | 11% ± 10 | 44% ± 16 | 89% ± 3 | $51k (100% of seeds) | $54k (100% of seeds) | $62k (83% of seeds) |
| Tiered screening | 6 | -16% ± 9 | -16% ± 9 | -2% ± 8 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 6 | 4% ± 5 | 4% ± 5 | 5% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Random | 5 | 11% ± 16 | 11% ± 16 | 12% ± 15 | >$100k (20% of seeds) | >$100k (20% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 1 | 51% ± 0 | 51% ± 0 | 71% ± 0 | $58k (100% of seeds) | $65k (100% of seeds) | >$100k (0% of seeds) |
| BOFN, full pipeline | 6 | 18% ± 8 | 53% ± 16 | 76% ± 14 | $38k (83% of seeds) | $50k (83% of seeds) | $76k (67% of seeds) |
| BOFN + lot reuse | 6 | 11% ± 10 | 44% ± 16 | 89% ± 3 | $51k (100% of seeds) | $54k (100% of seeds) | $62k (83% of seeds) |
| Tiered screening | 6 | -25% ± 4 | -11% ± 7 | -1% ± 8 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 6 | 4% ± 5 | 4% ± 5 | 5% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Random | 5 | 11% ± 16 | 11% ± 16 | 12% ± 15 | >$100k (20% of seeds) | >$100k (20% of seeds) | >$100k (0% of seeds) |

### Speed-up over tiered screening

Target: tiered screening's mean at $100k, -2.1% of the optimum, which it first reaches at $100k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 1 | $12k | **8.5×** | 6.6–399.0 | 3.2–3.2 | 0.97 |
| BOFN + lot reuse | 6 | $10k | **10.5×** | 2.7–399.0 | 3.1–19.9 | 0.94 |
| BOFN, full pipeline | 6 | $5k | **19.9×** | 3.1–399.0 | 3.1–19.9 | 0.97 |
| Standard BO | 6 | $14k | **6.9×** | 0.0–399.0 | 0.0–19.9 | 0.70 |
| Random | 5 | $5k | **19.9×** | 0.0–19.9 | 0.0–19.9 | 0.74 |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|
| Tiered screening | 1 | +24 points (1/0/0; p = 1) | +39 points (1/0/0; p = 1) | +49 points (1/0/0; p = 1) |
| BOFN, full pipeline | 1 | -29 points (0/0/1; p = 1) | -59 points (0/0/1; p = 1) | -27 points (0/0/1; p = 1) |
| BOFN + lot reuse | 1 | +10 points (1/0/0; p = 1) | -52 points (0/0/1; p = 1) | -25 points (0/0/1; p = 1) |
| Standard BO | 1 | +24 points (1/0/0; p = 1) | +39 points (1/0/0; p = 1) | +76 points (1/0/0; p = 1) |
| Random | 1 | +24 points (1/0/0; p = 1) | +39 points (1/0/0; p = 1) | +75 points (1/0/0; p = 1) |

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 1 | 25.0 | 5.0 | 0.0 | 48.0 | 18.0 | 8.0 | 15.0 | 14.0 | 5.0 | 10.0 |
| BOFN, full pipeline | 6 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 6 | 11.8 | 11.8 | 11.8 | 30.2 | 30.2 | 30.2 | 30.2 | 30.2 | 11.8 |  |
| Tiered screening | 6 | 224.0 | 19.8 | 28.2 | 27.2 | 27.2 | 27.2 | 27.2 | 5.3 | 19.8 |  |
| Standard BO | 6 | 20.7 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 5 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |

### Immersion outcomes (new builds only)

| Policy | n | immersions per run | passing immersions per run | seeds with a passing alloy | lowest Ni (wt%) among passing builds |
|---|---|---|---|---|---|
| pKGFN: picks the stage | 1 | 14.0 | 3.0 | 1/1 | 6.1 |
| BOFN, full pipeline | 6 | 21.0 | 9.8 | 5/6 | 7.4 |
| BOFN + lot reuse | 6 | 30.2 | 14.2 | 6/6 | 5.5 |
| Tiered screening | 6 | 5.3 | 0.0 | 0/6 | none |
| Standard BO | 6 | 21.0 | 1.7 | 1/6 | 16.4 |
| Random | 5 | 21.0 | 0.8 | 3/5 | 18.1 |

## Sensitivity over the four cells

At $100k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 71% ± 0 (n = 1) |  |  |  |
| BOFN, full pipeline | 76% ± 14 (n = 6) |  |  |  |
| BOFN + lot reuse | 89% ± 3 (n = 6) |  |  |  |
| Tiered screening | -2% ± 8 (n = 6) |  |  |  |
| Standard BO | 5% ± 5 (n = 6) |  |  |  |
| Random | 12% ± 15 (n = 5) |  |  |  |

At $50k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 32% ± 0 (n = 1) |  |  |  |
| BOFN, full pipeline | 53% ± 16 (n = 6) |  |  |  |
| BOFN + lot reuse | 44% ± 16 (n = 6) |  |  |  |
| Tiered screening | -16% ± 9 (n = 6) |  |  |  |
| Standard BO | 4% ± 5 (n = 6) |  |  |  |
| Random | 11% ± 16 (n = 5) |  |  |  |

## Screen audit (Advance 5)

From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. `m_ref` = 0.810. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.

| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |
|---|---|---|---|---|---|---|---|

## Quality: GP fits and the KG fallback

| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |
|---|---|---|---|---|
| (1, 1) | 30 | 9,696 | 0 | 5% of 107 |

