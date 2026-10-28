# pKGFN: light vs production Monte Carlo settings, matched seeds (written by `quality/compare_light_hq.py`)

Light: S = 32 base samples, 10 candidates, a 256 pool. Production: S = 64, 16 candidates, a 512 pool, with the F2 and F4 fixes. Best alloy demonstrated, % of the optimum.

| Seed | light $25k | production $25k | light $50k | production $50k | light $100k | production $100k | purchases (light / production) | made by the fallback (light / production) | wall time, min (production) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 31% | 33% | 45% | 48% | 63% | 48% | 88 / 98 | 2 / 1 | 67 |
| 1 | -2% | -2% | -2% | 57% | 47% | 57% | 112 / 121 | 76 / 36 | 77 |
| 2 | -3% | -8% | 60% | 76% | 60% | 78% | 110 / 102 | 17 / 30 | 33 |
| 3 | -11% | -4% | -11% | -4% | 78% | 73% | 96 / 108 | 17 / 39 | 30 |

Mean change at $100k on these 4 seeds: +2% of the optimum (production minus light).
