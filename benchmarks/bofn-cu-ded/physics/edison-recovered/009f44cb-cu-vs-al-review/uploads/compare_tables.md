# Copper against aluminum (written by `compare/compare.py`)

Optima: aluminum (kappa = 1) 0.694; copper (1, 1) 0.492; copper (1, 1) without the immersion gate 0.745. Every percentage is of the optimum of the truth the runs were scored on.

## The two truths on random designs

| Uniform random designs (10^6 per truth) | Al (kappa = 1) | Cu (1, 1) | Cu (1, 1) without the immersion gate |
|---|---|---|---|
| optimum J* | 0.694 | 0.492 | 0.745 |
| median design (% of J*) | -17% | -42% | -21% |
| share with J > 0 | 28.373% | 2.962% | 20.316% |
| share with J at least 50% of J* | 5.511% | 0.455% | 1.930% |
| share with J at least 60% of J* | 3.261% | 0.225% | 0.777% |
| share with J at least 70% of J* | 1.599% | 0.075% | 0.215% |
| share with J at least 80% of J* | 0.513% | 0.011% | 0.036% |
| expected best of 5 random designs (% of J*) | 29% | -15% | 15% |
| expected best of 21 random designs (% of J*) | 58% | 8% | 42% |
| expected best of 24 random designs (% of J*) | 61% | 11% | 44% |
| expected best of 26 random designs (% of J*) | 62% | 12% | 45% |
| expected best of 29 random designs (% of J*) | 63% | 14% | 47% |
| the five shared seed designs: mean best (% of J*), 20 seeds | 35% | -10% | |
| share passing immersion (m >= m_ref) | | 3.2% | |

## Composition or process? Where the copper needle is

| Share of designs (`needle.py`) | Al (kappa = 1) | Cu (1, 1) |
|---|---|---|
| optimum composition, random settings: J at least 60% of J* | 8.7% | 2.7% |
| optimum composition, random settings: J > 0 | 39.1% | 10.8% |
| random composition, optimum settings: J at least 60% of J* | 66.1% | 5.3% |
| random composition, its best of 2,048 settings: J at least 60% of J* | 83.9% | 30.6% |
| random composition, its best of 2,048 settings: J > 0 | 100.0% | 66.5% |
| random designs passing immersion | | 3.2% |
| the same designs, had they deposited fully dense | | 61.7% |
| random designs depositing at rho_m >= 0.9 | | 0.14% |

## The two benchmarks' results

| Policy | Al (kappa = 1): n | start | $25k | $50k | $100k | Cu (1, 1): n | start | $25k | $50k | $100k |
|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 20 | 35% | 62% ± 5 | 70% ± 3 | 84% ± 2 |  |  |  |  |  |
| BOFN + lot reuse | 20 | 35% | 61% ± 6 | 74% ± 5 | 90% ± 2 | 20 | -10% | 14% ± 5 | 32% ± 8 | 72% ± 7 |
| BOFN, full pipeline | 20 | 35% | 50% ± 6 | 77% ± 5 | 86% ± 4 | 20 | -10% | 15% ± 6 | 39% ± 9 | 73% ± 7 |
| Standard BO | 20 | 35% | 48% ± 7 | 63% ± 5 | 84% ± 3 | 20 | -10% | 6% ± 3 | 7% ± 3 | 14% ± 6 |
| Random | 20 | 35% | 52% ± 5 | 61% ± 4 | 68% ± 2 | 20 | -10% | -1% ± 4 | 7% ± 5 | 22% ± 5 |
| Tiered screening | 20 | 35% | 46% ± 5 | 56% ± 3 | 63% ± 2 | 20 | -10% | -9% ± 5 | -9% ± 5 | -8% ± 5 |
| Tiered, no powder reuse | 20 | 35% | 45% ± 5 | 52% ± 4 | 57% ± 3 |  |  |  |  |  |
| Tiered, Ni ≥ 10 wt% |  |  |  |  |  | 20 | -10% | -7% ± 5 | 1% ± 5 | 10% ± 6 |
| Tiered, Ni ≥ 10 wt%, reference screen |  |  |  |  |  | 20 | -10% | 8% ± 4 | 16% ± 4 | 24% ± 5 |
| pKGFN, any alloy | 20 | 35% | 51% ± 6 | 61% ± 5 | 82% ± 5 |  |  |  |  |  |

## The copper network without the immersion gate (J = U - 0.3 B; same network, stages, costs and seeds)

| Policy | Cu (1, 1) as benchmarked: n | start | $25k | $50k | $100k | Cu without the immersion gate: n | start | $25k | $50k | $100k | Al (kappa = 1) $100k |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BOFN + lot reuse | 20 | -10% | 14% ± 5 | 32% ± 8 | 72% ± 7 | 20 | 23% | 47% ± 6 | 71% ± 3 | 88% ± 2 | 90% ± 2 |
| BOFN, full pipeline | 20 | -10% | 15% ± 6 | 39% ± 9 | 73% ± 7 | 20 | 23% | 44% ± 6 | 67% ± 5 | 85% ± 5 | 86% ± 4 |
| Standard BO | 20 | -10% | 6% ± 3 | 7% ± 3 | 14% ± 6 | 20 | 23% | 39% ± 6 | 49% ± 5 | 65% ± 4 | 84% ± 3 |
| Random | 20 | -10% | -1% ± 4 | 7% ± 5 | 22% ± 5 | 20 | 23% | 43% ± 4 | 47% ± 4 | 51% ± 3 | 68% ± 2 |
| pKGFN: picks the stage |  |  |  |  |  |  |  |  |  |  | 84% ± 2 |

## Tiered screening against corrosion-aware tiered screening

| Policy | n | $25k | $50k | $100k | builds immersed per run | of which pass immersion | builds stopped by the one-hour screen per run | lots retired at Utah per run |
|---|---|---|---|---|---|---|---|---|
| Tiered screening | 20 | -9% ± 5 | -9% ± 5 | -8% ± 5 | 4.0 | 0.0 | 20.9 | 8.0 |
| Tiered, Ni ≥ 10 wt% | 20 | -7% ± 5 | 1% ± 5 | 10% ± 6 | 2.5 | 0.8 | 15.8 | 17.6 |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 8% ± 4 | 16% ± 4 | 24% ± 5 | 9.9 | 2.6 | 11.2 | 12.6 |

## Finding the feasible region first

The copper objective is gated: an alloy that fails immersion scores minus 0.3 times its burden. Before a policy has demonstrated an alloy with J > 0, one-step KG has little to improve on.

| Policy | n | seeds whose shared seed data already holds an alloy with J > 0 | median new spend to the first alloy with J > 0 (seeds that reach it) | KG-flat fallback share before it | after it |
|---|---|---|---|---|---|
| BOFN + lot reuse | 20 | 5 | $21k (20 of 20) |  |  |
| pkgfn (light settings) | 20 | 5 | $39k (19 of 20) | 43% of 893 | 4% of 1051 |
| BOFN, full pipeline | 20 | 5 | $14k (20 of 20) |  |  |
| Standard BO | 20 | 5 | $24k (20 of 20) |  |  |
| Random | 20 | 5 | $31k (17 of 20) |  |  |
| Tiered screening | 20 | 5 | >$100k (5 of 20) |  |  |
| Tiered, Ni ≥ 10 wt% | 20 | 5 | $43k (13 of 20) |  |  |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 5 | $19k (17 of 20) |  |  |

