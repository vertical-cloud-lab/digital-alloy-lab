# Tables (written by `analyze.py`)

Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.

## Cell (kappa, eta) = (1, 1): both screens biased; optimum J* = 0.492

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60% of seeds) | >$100k (35% of seeds) | >$100k (5% of seeds) |
| BOFN, full pipeline | 15 | 20% ± 7 | 46% ± 10 | 74% ± 8 | $48k (87% of seeds) | $52k (73% of seeds) | $72k (73% of seeds) |
| BOFN + lot reuse | 15 | 20% ± 5 | 39% ± 9 | 75% ± 8 | $52k (87% of seeds) | $71k (87% of seeds) | $78k (73% of seeds) |
| Tiered screening | 7 | -14% ± 7 | -13% ± 7 | -11% ± 7 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 14 | 8% ± 5 | 10% ± 4 | 21% ± 8 | >$100k (21% of seeds) | >$100k (7% of seeds) | >$100k (7% of seeds) |
| Random | 14 | 5% ± 5 | 10% ± 5 | 23% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 19% ± 6 | 37% ± 7 | 68% ± 4 | $52k (80% of seeds) | $78k (60% of seeds) | >$100k (25% of seeds) |
| BOFN, full pipeline | 15 | 20% ± 7 | 46% ± 10 | 74% ± 8 | $48k (87% of seeds) | $52k (73% of seeds) | $72k (73% of seeds) |
| BOFN + lot reuse | 15 | 18% ± 5 | 38% ± 9 | 75% ± 8 | $52k (87% of seeds) | $71k (87% of seeds) | $78k (73% of seeds) |
| Tiered screening | 7 | -12% ± 7 | -11% ± 7 | -11% ± 7 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 14 | 8% ± 5 | 10% ± 4 | 21% ± 8 | >$100k (21% of seeds) | >$100k (7% of seeds) | >$100k (7% of seeds) |
| Random | 14 | 5% ± 5 | 10% ± 5 | 23% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Speed-up over tiered screening

Target: tiered screening's mean at $100k, -11.3% of the optimum, which it first reaches at $99k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | $0k | **395.0×** | 5.6–395.0 | 8.8–17.2 | 0.99 |
| BOFN + lot reuse | 15 | $0k | **395.0×** | 18.4–395.0 | 10.9–19.8 | 1.00 |
| BOFN, full pipeline | 15 | $0k | **395.0×** | 18.4–395.0 | 10.9–19.8 | 1.00 |
| Standard BO | 14 | $0k | **395.0×** | 9.4–395.0 | 9.4–19.8 | 0.99 |
| Random | 14 | $0k | **395.0×** | 5.3–395.0 | 9.4–19.8 | 0.97 |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|
| Tiered screening | 7 | +26 points (5/2/0; p = 0.062) | +47 points (7/0/0; p = 0.016) | +78 points (7/0/0; p = 0.016) |
| BOFN, full pipeline | 15 | -5 points (2/1/12; p = 0.084) | -12 points (3/0/12; p = 0.083) | -10 points (4/0/11; p = 0.15) |
| BOFN + lot reuse | 15 | -4 points (2/2/11; p = 0.1) | -5 points (5/0/10; p = 0.36) | -10 points (2/0/13; p = 0.083) |
| Standard BO | 14 | +8 points (4/3/7; p = 0.93) | +26 points (9/0/5; p = 0.025) | +45 points (12/0/2; p = 0.00085) |
| Random | 14 | +11 points (9/3/2; p = 0.062) | +26 points (12/0/2; p = 0.0067) | +43 points (14/0/0; p = 0.00012) |

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 | 12.4 | 12.3 |
| BOFN, full pipeline | 15 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 15 | 12.3 | 12.3 | 12.3 | 29.5 | 29.5 | 29.5 | 29.5 | 29.5 | 12.3 |  |
| Tiered screening | 7 | 224.0 | 15.9 | 21.0 | 30.1 | 30.1 | 30.1 | 30.1 | 5.1 | 15.9 |  |
| Standard BO | 14 | 20.6 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 14 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |

## Sensitivity over the four cells

At $100k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 59% ± 5 (n = 20) |  |  |  |
| BOFN, full pipeline | 74% ± 8 (n = 15) |  |  |  |
| BOFN + lot reuse | 75% ± 8 (n = 15) |  |  |  |
| Tiered screening | -11% ± 7 (n = 7) |  |  |  |
| Standard BO | 21% ± 8 (n = 14) |  |  |  |
| Random | 23% ± 5 (n = 14) |  |  |  |

At $50k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 27% ± 7 (n = 20) |  |  |  |
| BOFN, full pipeline | 46% ± 10 (n = 15) |  |  |  |
| BOFN + lot reuse | 39% ± 9 (n = 15) |  |  |  |
| Tiered screening | -13% ± 7 (n = 7) |  |  |  |
| Standard BO | 10% ± 4 (n = 14) |  |  |  |
| Random | 10% ± 5 (n = 14) |  |  |  |

## Screen audit (Advance 5)

From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. `m_ref` = 0.849. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.

| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |
|---|---|---|---|---|---|---|---|

## Quality: GP fits and the KG fallback

| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |
|---|---|---|---|---|
| (1, 1) | 85 | 22,276 | 0 | 22% of 1,944 |

