# Hand-measurement validation

- Hand values: 37 unique particles (49 labels; `3.2nA_005` repeats `3.2nA_006`)
- Located: 36 (23 by the line search, 13 by eye); not located: 1
- Segmentation failures (merged region with no dominant sphere, or a fragment): 4: 142.4 µm (annotated), 52.71 µm (3.2nA_006), 161.9 µm (3.2nA_006), 30.45 µm (3.2nA_005)
- Compared: **32**; sem_psd size used: ECD for 28, sphere fit for 4

| Statistic | Value |
|---|---|
| Median relative difference (sem_psd / hand − 1) | +3.6 % |
| Mean ± SD relative difference | +4.7 ± 5.2 % |
| Within ±5 % / ±10 % | 19 / 28 of 32 |
| Bland–Altman bias, 95 % limits (µm) | +2.9, [-3.3, +9.0] |
| Hand < 60 µm: median relative difference | +6.9 % (n = 13) |
| Hand ≥ 60 µm: median relative difference | +1.8 % (n = 19) |
| Same particles at 133x vs 150x (`_005` / `_006` − 1) | +0.5 ± 0.8 % (n = 9) |

