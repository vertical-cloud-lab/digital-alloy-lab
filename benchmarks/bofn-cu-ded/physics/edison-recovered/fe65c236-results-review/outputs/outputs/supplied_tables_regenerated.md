# Tables (written by `analyze.py`)

Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.

## Cell (kappa, eta) = (1, 1): both screens biased; optimum J* = 0.492

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | 3% ± 5 | 25% ± 10 | 59% ± 11 | $100k (57% of seeds) | >$100k (43% of seeds) | >$100k (29% of seeds) |
| pKGFN, light settings (first sweep) | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60% of seeds) | >$100k (35% of seeds) | >$100k (5% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 14% ± 5 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| Tiered screening | 20 | -9% ± 5 | -9% ± 5 | -8% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt% | 20 | -7% ± 5 | 1% ± 5 | 10% ± 6 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 8% ± 4 | 16% ± 4 | 24% ± 5 | >$100k (10% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | 19% ± 10 | 30% ± 12 | 71% ± 6 | $54k (86% of seeds) | $92k (57% of seeds) | >$100k (29% of seeds) |
| pKGFN, light settings (first sweep) | 20 | 19% ± 6 | 37% ± 7 | 68% ± 4 | $52k (80% of seeds) | $78k (60% of seeds) | >$100k (25% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 13% ± 4 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| Tiered screening | 20 | -8% ± 5 | -8% ± 5 | -6% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt% | 20 | 2% ± 4 | 7% ± 4 | 13% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 8% ± 4 | 16% ± 4 | 24% ± 5 | >$100k (10% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

### Speed-up over tiered screening

Target: tiered screening's mean at $100k, -7.7% of the optimum, which it first reaches at $99k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | $6k | **17.3×** | 2.7–397.0 | 11.5–20.8 | 0.95 |
| pKGFN, light settings (first sweep) | 20 | $6k | **17.3×** | 5.8–397.0 | 12.0–21.9 | 0.99 |
| BOFN + lot reuse | 20 | $5k | **19.9×** | 10.9–397.0 | 18.4–43.9 | 1.00 |
| BOFN, full pipeline | 20 | $5k | **19.9×** | 18.4–397.0 | 18.4–19.9 | 0.99 |
| Standard BO | 20 | $5k | **19.9×** | 5.2–397.0 | 18.4–19.9 | 0.98 |
| Random | 20 | $10k | **10.2×** | 2.3–397.0 | 9.4–19.9 | 0.87 |
| Tiered, Ni ≥ 10 wt% | 20 | $23k | **4.3×** | 1.2–397.0 | 2.7–7.2 | 0.55 |

### Speed-up over corrosion-aware tiered screening (Ni ≥ 10 wt%, reference screen)

Target: tiered, ni ≥ 10 wt%, reference screen's mean at $100k, 24.2% of the optimum, which it first reaches at $100k.

| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |
|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | $47k | **2.1×** | 0.9–2.4 | 0.8–2.0 | 0.01 |
| pKGFN, light settings (first sweep) | 20 | $47k | **2.1×** | 1.5–3.9 | 1.5–3.5 | 0.12 |
| BOFN + lot reuse | 20 | $35k | **2.8×** | 1.7–4.1 | 1.7–3.9 | 0.38 |
| BOFN, full pipeline | 20 | $34k | **3.0×** | 1.7–4.2 | 1.7–3.5 | 0.16 |
| Standard BO | 20 | >$100k | **0.0×** | 0.0–1.0 | 0.0–0.0 | 0.00 |
| Random | 20 | >$100k | **0.0×** | 0.0–1.6 | 0.0–1.6 | 0.00 |
| Tiered screening | 20 | >$100k | **0.0×** | 0.0–0.0 | 0.0–0.0 | 0.00 |
| Tiered, Ni ≥ 10 wt% | 20 | >$100k | **0.0×** | 0.0–0.0 | 0.0–0.0 | 0.00 |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|
| pKGFN, light settings (first sweep) | 7 | -11 points (3/0/4; p = 0.58) | -2 points (3/0/4; p = 0.94) | -5 points (3/0/4; p = 0.69) |
| Tiered screening | 7 | +17 points (6/1/0; p = 0.031) | +37 points (7/0/0; p = 0.016) | +69 points (7/0/0; p = 0.016) |
| Tiered, Ni ≥ 10 wt% | 7 | +14 points (5/1/1; p = 0.094) | +30 points (6/0/1; p = 0.047) | +53 points (7/0/0; p = 0.016) |
| Tiered, Ni ≥ 10 wt%, reference screen | 7 | -7 points (2/0/5; p = 0.47) | +4 points (5/0/2; p = 0.69) | +31 points (6/0/1; p = 0.047) |
| BOFN, full pipeline | 7 | -21 points (0/0/7; p = 0.016) | -21 points (1/0/6; p = 0.22) | -29 points (1/0/6; p = 0.047) |
| BOFN + lot reuse | 7 | -14 points (1/0/6; p = 0.11) | -15 points (2/0/5; p = 0.38) | -3 points (3/0/4; p = 0.81) |
| Standard BO | 7 | -0 points (2/1/4; p = 0.84) | +20 points (4/0/3; p = 0.22) | +47 points (5/0/2; p = 0.078) |
| Random | 7 | +4 points (4/1/2; p = 0.56) | +22 points (5/0/2; p = 0.16) | +40 points (6/0/1; p = 0.031) |

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | 4.6 | 17.6 | 16.3 | 37.9 | 13.4 | 5.9 | 11.9 | 11.3 | 17.6 | 12.7 |
| pKGFN, light settings (first sweep) | 20 | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 | 12.4 | 12.3 |
| BOFN, full pipeline | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 20 | 12.6 | 12.6 | 12.6 | 29.3 | 29.3 | 29.3 | 29.3 | 29.3 | 12.6 |  |
| Tiered screening | 20 | 224.0 | 22.8 | 44.2 | 24.9 | 24.9 | 24.9 | 24.9 | 4.0 | 22.8 |  |
| Tiered, Ni ≥ 10 wt% | 20 | 224.0 | 31.0 | 67.4 | 18.4 | 18.4 | 18.4 | 18.4 | 2.5 | 31.0 |  |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 224.0 | 26.5 | 53.6 | 21.1 | 21.1 | 21.1 | 21.1 | 9.9 | 26.5 |  |
| Standard BO | 20 | 19.7 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |

## Cell (kappa, eta) = (0, 0): both screens right; optimum J* = 0.382

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN, light settings (first sweep) | 10 | -6% ± 4 | -0% ± 4 | 9% ± 7 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| BOFN, full pipeline | 1 | 12% ± 0 | 19% ± 0 | 92% ± 0 | $52k (100% of seeds) | $72k (100% of seeds) | $76k (100% of seeds) |
| BOFN + lot reuse | 1 | 12% ± 0 | 68% ± 0 | 95% ± 0 | $46k (100% of seeds) | $54k (100% of seeds) | $58k (100% of seeds) |

### Matched seeds (Wilcoxon signed-rank)

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|

### Purchases per $100k (mean over seeds, new purchases only)

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN, light settings (first sweep) | 10 | 3.8 | 17.9 | 10.3 | 39.1 | 12.0 | 6.4 | 11.4 | 9.2 | 17.9 | 13.9 |
| BOFN, full pipeline | 1 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 1 | 10.0 | 10.0 | 10.0 | 31.0 | 31.0 | 31.0 | 31.0 | 31.0 | 10.0 |  |

## Sensitivity over the four cells

At $100k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 59% ± 11 (n = 7) |  |  |  |
| pKGFN, light settings (first sweep) | 59% ± 5 (n = 20) | 9% ± 7 (n = 10) |  |  |
| BOFN, full pipeline | 73% ± 7 (n = 20) | 92% ± 0 (n = 1) |  |  |
| BOFN + lot reuse | 72% ± 7 (n = 20) | 95% ± 0 (n = 1) |  |  |
| Tiered screening | -8% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10 wt% | 10% ± 6 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10 wt%, reference screen | 24% ± 5 (n = 20) |  |  |  |
| Standard BO | 14% ± 6 (n = 20) |  |  |  |
| Random | 22% ± 5 (n = 20) |  |  |  |

At $50k:

| Policy | (1, 1) both screens biased | (0, 0) both screens right | (1, 0) crack screen biased only | (0, 1) one-hour screen biased only |
|---|---|---|---|---|
| pKGFN: picks the stage | 25% ± 10 (n = 7) |  |  |  |
| pKGFN, light settings (first sweep) | 27% ± 7 (n = 20) | -0% ± 4 (n = 10) |  |  |
| BOFN, full pipeline | 39% ± 9 (n = 20) | 19% ± 0 (n = 1) |  |  |
| BOFN + lot reuse | 32% ± 8 (n = 20) | 68% ± 0 (n = 1) |  |  |
| Tiered screening | -9% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10 wt% | 1% ± 5 (n = 20) |  |  |  |
| Tiered, Ni ≥ 10 wt%, reference screen | 16% ± 4 (n = 20) |  |  |  |
| Standard BO | 7% ± 3 (n = 20) |  |  |  |
| Random | 7% ± 5 (n = 20) |  |  |  |

## Screen audit (Advance 5)

From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. `m_ref` = 0.849. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.

| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |
|---|---|---|---|---|---|---|---|

## Quality: GP fits and the KG fallback

| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |
|---|---|---|---|---|
| (1, 1) | 167 | 75,434 | 0 | 26% of 2,633 |
| (0, 0) | 12 | 1,919 | 0 | 45% of 952 |

