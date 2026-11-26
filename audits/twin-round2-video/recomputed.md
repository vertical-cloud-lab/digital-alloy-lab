# Recomputed from the stored runs (byu-vcl 357d149)

Written by `recompute.py`; see its docstring for the definitions. Days are days since the campaign started.

Targets: T1 (the video's "state of the art") = {'flaime_al': 0.4232, 'onr_cu': 0.5559}; T2 (the harder target in `bench2_summary.json`) = {'flaime_al': 0.6393, 'onr_cu': 0.6565}.

## 1. Every arm: seeds that reached T1, and when

| Arm (file) | Campaign | Reached T1 | Median days (twin) | KM median | Earliest to latest | Mean final best |
|---|---|---|---|---|---|---|
| automated, stocked, `bofn_blend` (`main.jsonl`) | FLAIME (Al) | 12/12 | 116.2 | 109.9 | 20.3 to 231.1 | 0.687 ± 0.015 |
| automated, stocked, `bofn_blend` (`main.jsonl`) | ONR (Cu) | 12/12 | 225.3 | 224.9 | 144.3 to 309.2 | 0.674 ± 0.009 |
| automated, stocked, `bofn` (`main.jsonl`) | FLAIME (Al) | 11/12 | 122.7 | 122.7 | 23.3 to 216.3 | 0.650 ± 0.034 |
| automated, stocked, `bofn` (`main.jsonl`) | ONR (Cu) | 3/12 | unbounded | unbounded | 106.0 to 156.0 | 0.327 ± 0.086 |
| automated, stocked, `heuristic` (`main.jsonl`) | FLAIME (Al) | 12/12 | 37.2 | 22.7 | 3.1 to 192.0 | 0.605 ± 0.017 |
| automated, stocked, `heuristic` (`main.jsonl`) | ONR (Cu) | 7/12 | 145.6 | 145.6 | 96.1 to 239.5 | 0.585 ± 0.023 |
| automated, stocked, `tiered` (`main.jsonl`) | FLAIME (Al) | 7/12 | 106.4 | 106.4 | 2.2 to 293.8 | 0.338 ± 0.090 |
| automated, stocked, `tiered` (`main.jsonl`) | ONR (Cu) | 11/12 | 88.2 | 88.2 | 39.2 to 194.4 | 0.686 ± 0.016 |
| automated, stocked, `gpbo` (`main.jsonl`) | FLAIME (Al) | 10/12 | 190.1 | 190.1 | 107.8 to 265.8 | 0.455 ± 0.066 |
| automated, stocked, `gpbo` (`main.jsonl`) | ONR (Cu) | 8/12 | 218.1 | 218.1 | 71.1 to 254.7 | 0.529 ± 0.056 |
| automated, stocked, `random` (`main.jsonl`) | FLAIME (Al) | 1/12 | unbounded | unbounded | 60.7 to 60.7 | 0.102 ± 0.060 |
| automated, stocked, `random` (`main.jsonl`) | ONR (Cu) | 4/12 | unbounded | unbounded | 26.5 to 109.5 | 0.347 ± 0.083 |
| automated, stocked, `sobol` (`main.jsonl`) | FLAIME (Al) | 1/12 | unbounded | unbounded | 11.2 to 11.2 | 0.105 ± 0.049 |
| automated, stocked, `sobol` (`main.jsonl`) | ONR (Cu) | 3/12 | unbounded | unbounded | 51.0 to 149.3 | 0.447 ± 0.054 |
| automated, stocked, `cost_aware` (`main.jsonl`) | FLAIME (Al) | 10/12 | 90.9 | 90.9 | 2.2 to 338.7 | 0.552 ± 0.076 |
| automated, stocked, `cost_aware` (`main.jsonl`) | ONR (Cu) | 11/12 | 73.6 | 73.6 | 15.5 to 270.0 | 0.633 ± 0.015 |
| conventional, lean, 3 y, `bofn` (`conventional.jsonl`) | FLAIME (Al) | 12/12 | 219.6 | 193.6 | 101.6 to 520.6 | 0.743 ± 0.008 |
| conventional, lean, 3 y, `bofn` (`conventional.jsonl`) | ONR (Cu) | 6/12 | 839.6 | 839.6 | 221.8 to 839.6 | 0.546 ± 0.029 |
| conventional, lean, 3 y, `heuristic` (`conventional.jsonl`) | FLAIME (Al) | 12/12 | 122.6 | 122.6 | 21.6 to 274.6 | 0.675 ± 0.014 |
| conventional, lean, 3 y, `heuristic` (`conventional.jsonl`) | ONR (Cu) | 12/12 | 490.1 | 451.5 | 237.3 to 1063.2 | 0.642 ± 0.012 |
| conventional, lean, 3 y, `tiered` (`conventional.jsonl`) | FLAIME (Al) | 7/12 | 323.6 | 323.6 | 105.6 to 707.6 | 0.338 ± 0.090 |
| conventional, lean, 3 y, `tiered` (`conventional.jsonl`) | ONR (Cu) | 12/12 | 334.3 | 324.1 | 210.8 to 777.5 | 0.706 ± 0.010 |
| conventional, lean, 3 y, `gpbo` (`conventional.jsonl`) | FLAIME (Al) | 9/12 | 339.6 | 339.6 | 226.4 to 725.6 | 0.520 ± 0.077 |
| conventional, lean, 3 y, `gpbo` (`conventional.jsonl`) | ONR (Cu) | 11/12 | 692.5 | 692.5 | 188.4 to 790.0 | 0.642 ± 0.021 |
| conventional, lean, 3 y, `random` (`conventional.jsonl`) | FLAIME (Al) | 8/12 | 602.6 | 602.6 | 115.4 to 1072.6 | 0.389 ± 0.085 |
| conventional, lean, 3 y, `random` (`conventional.jsonl`) | ONR (Cu) | 9/12 | 702.3 | 702.3 | 158.1 to 1002.9 | 0.617 ± 0.028 |
| conventional, lean, 3 y, `sobol` (`conventional.jsonl`) | FLAIME (Al) | 3/12 | unbounded | unbounded | 129.6 to 841.4 | 0.272 ± 0.070 |
| conventional, lean, 3 y, `sobol` (`conventional.jsonl`) | ONR (Cu) | 7/12 | 789.9 | 789.9 | 236.4 to 949.9 | 0.567 ± 0.020 |
| automated, lean, `bofn` (`stock.jsonl`) | FLAIME (Al) | 12/12 | 189.3 | 185.9 | 80.8 to 345.8 | 0.625 ± 0.035 |
| automated, lean, `bofn` (`stock.jsonl`) | ONR (Cu) | 6/12 | 339.4 | 339.4 | 108.2 to 339.4 | 0.434 ± 0.074 |
| automated, lean, `heuristic` (`stock.jsonl`) | FLAIME (Al) | 12/12 | 106.8 | 101.1 | 11.2 to 261.4 | 0.577 ± 0.020 |
| automated, lean, `heuristic` (`stock.jsonl`) | ONR (Cu) | 10/12 | 261.2 | 261.2 | 148.8 to 323.4 | 0.576 ± 0.025 |
| automated, stocked, DAL 275 seeds, `bofn` (`seeded.jsonl`) | FLAIME (Al) | 12/12 | 2.5 | 2.5 | 2.5 to 130.6 | 0.688 ± 0.018 |
| automated, stocked, DAL 275 seeds, `bofn` (`seeded.jsonl`) | ONR (Cu) | 12/12 | 85.7 | 85.3 | 75.4 to 138.4 | 0.641 ± 0.015 |
| automated, stocked, DAL 275 seeds, `gpbo` (`seeded.jsonl`) | FLAIME (Al) | 11/12 | 2.2 | 2.2 | 2.2 to 3.2 | 0.596 ± 0.056 |
| automated, stocked, DAL 275 seeds, `gpbo` (`seeded.jsonl`) | ONR (Cu) | 11/12 | 91.3 | 91.3 | 75.7 to 151.2 | 0.625 ± 0.018 |
| automated, stocked, DAL 275 seeds, `random` (`seeded.jsonl`) | FLAIME (Al) | 12/12 | 2.2 | 2.2 | 2.2 to 46.9 | 0.596 ± 0.021 |
| automated, stocked, DAL 275 seeds, `random` (`seeded.jsonl`) | ONR (Cu) | 9/12 | 64.4 | 64.4 | 38.3 to 228.0 | 0.589 ± 0.015 |
| DAL 256 schedule, lean, DAL 275 seeds, `bofn` (`seeded_dal256.jsonl`) | FLAIME (Al) | 12/12 | 73.4 | 73.4 | 59.4 to 94.4 | 0.664 ± 0.018 |
| DAL 256 schedule, lean, DAL 275 seeds, `bofn` (`seeded_dal256.jsonl`) | ONR (Cu) | 6/12 | 335.8 | 335.8 | 221.5 to 335.8 | 0.302 ± 0.091 |
| DAL 256 schedule, lean, DAL 275 seeds, `gpbo` (`seeded_dal256.jsonl`) | FLAIME (Al) | 9/12 | 52.4 | 52.4 | 38.4 to 59.4 | 0.469 ± 0.084 |
| DAL 256 schedule, lean, DAL 275 seeds, `gpbo` (`seeded_dal256.jsonl`) | ONR (Cu) | 10/12 | 276.4 | 276.4 | 209.9 to 349.1 | 0.506 ± 0.069 |
| DAL 256 schedule, lean, DAL 275 seeds, `random` (`seeded_dal256.jsonl`) | FLAIME (Al) | 11/12 | 52.4 | 52.4 | 38.4 to 101.4 | 0.546 ± 0.051 |
| DAL 256 schedule, lean, DAL 275 seeds, `random` (`seeded_dal256.jsonl`) | ONR (Cu) | 5/12 | unbounded | unbounded | 213.4 to 356.6 | 0.275 ± 0.088 |
| automated, hidden Cu effect, `bofn_blend` (`cu_hidden.jsonl`) | ONR (Cu) | 9/12 | 234.7 | 234.7 | 134.3 to 274.8 | 0.552 ± 0.077 |
| automated, hidden Cu effect, `bofn` (`cu_hidden.jsonl`) | ONR (Cu) | 3/12 | unbounded | unbounded | 106.0 to 156.0 | 0.291 ± 0.089 |
| automated, hidden Cu effect, `tiered` (`cu_hidden.jsonl`) | ONR (Cu) | 11/12 | 88.2 | 88.2 | 39.2 to 194.4 | 0.686 ± 0.016 |
| automated, hidden Cu effect, `heuristic` (`cu_hidden.jsonl`) | ONR (Cu) | 7/12 | 145.6 | 145.6 | 96.1 to 239.5 | 0.585 ± 0.023 |
| automated, hidden Cu effect, `gpbo` (`cu_hidden.jsonl`) | ONR (Cu) | 8/12 | 218.1 | 218.1 | 71.1 to 254.7 | 0.529 ± 0.056 |
| automated, hidden Cu effect, `random` (`cu_hidden.jsonl`) | ONR (Cu) | 4/12 | unbounded | unbounded | 26.5 to 109.5 | 0.347 ± 0.083 |

## 2. Time to T1: acceleration factors, intervals and tests

AF = median days of the reference arm ÷ median days of the new arm. `new faster` / `ref faster` are shares of the seed pairs (one seed from each arm) whose order is known. p: two-sided permutation test, Gehan statistic.

| Comparison (reference → new) | Campaign | Reached (ref, new) | Median days (ref, new) | AF | 95% bootstrap interval | AF with KM medians | new faster / ref faster / unknown | p |
|---|---|---|---|---|---|---|---|---|
| video headline: automated `bofn_blend` vs conventional `bofn` | FLAIME (Al) | 12/12, 12/12 | 219.6, 116.2 | 1.89 | 1.07 to 3.39 | 1.76 (0.97 to 3.62) | 83% / 17% / 0% | 0.0056 |
| video headline: automated `bofn_blend` vs conventional `bofn` | ONR (Cu) | 6/12, 12/12 | 839.6, 225.3 | 3.73 | 2.04 to unbounded | 3.73 (2.04 to unbounded) | 95% / 5% / 0% | < 0.0001 |
| same optimizer on both: automated `bofn` vs conventional `bofn` | FLAIME (Al) | 12/12, 11/12 | 219.6, 122.7 | 1.79 | 0.88 to 2.58 | 1.58 (0.84 to 2.58) | 73% / 26% / 1% | 0.0531 |
| same optimizer on both: automated `bofn` vs conventional `bofn` | ONR (Cu) | 6/12, 3/12 | 839.6, unbounded | none (new arm's median unbounded) | 0.00 to unbounded | none (new arm's median unbounded) (0.00 to unbounded) | 25% / 6% / 69% | 0.2956 |
| video footer: automated `bofn_blend` vs conventional `heuristic` | FLAIME (Al) | 12/12, 12/12 | 122.6, 116.2 | 1.05 | 0.69 to 2.25 | 1.11 (0.66 to 2.25) | 61% / 39% / 0% | 0.3777 |
| video footer: automated `bofn_blend` vs conventional `heuristic` | ONR (Cu) | 12/12, 12/12 | 490.1, 225.3 | 2.18 | 1.76 to 2.63 | 2.01 (1.69 to 2.61) | 98% / 2% / 0% | < 0.0001 |
| heuristic on both: automated `heuristic` vs conventional `heuristic` | FLAIME (Al) | 12/12, 12/12 | 122.6, 37.2 | 3.29 | 1.08 to 11.35 | 5.41 (1.15 to 11.99) | 78% / 22% / 0% | 0.0167 |
| heuristic on both: automated `heuristic` vs conventional `heuristic` | ONR (Cu) | 12/12, 7/12 | 490.1, 145.6 | 3.37 | 0.00 to 4.43 | 3.10 (0.00 to 4.37) | 58% / 8% / 35% | 0.0213 |
| automated `tiered` vs conventional `tiered` | FLAIME (Al) | 7/12, 7/12 | 323.6, 106.4 | 3.04 | 0.00 to unbounded | 3.04 (0.00 to unbounded) | 54% / 25% / 21% | 0.2129 |
| automated `tiered` vs conventional `tiered` | ONR (Cu) | 12/12, 11/12 | 334.3, 88.2 | 3.79 | 2.77 to 6.47 | 3.67 (2.63 to 6.47) | 92% / 6% / 3% | 0.0001 |
| automated `gpbo` vs conventional `gpbo` | FLAIME (Al) | 9/12, 10/12 | 339.6, 190.1 | 1.79 | 1.33 to 4.03 | 1.79 (1.33 to 4.03) | 81% / 11% / 8% | 0.0026 |
| automated `gpbo` vs conventional `gpbo` | ONR (Cu) | 11/12, 8/12 | 692.5, 218.1 | 3.18 | 0.00 to 4.11 | 3.18 (0.00 to 4.11) | 64% / 8% / 28% | 0.0122 |
| stocking removed: automated lean `bofn` vs conventional lean `bofn` | FLAIME (Al) | 12/12, 12/12 | 219.6, 189.3 | 1.16 | 0.72 to 1.66 | 1.04 (0.71 to 1.67) | 57% / 43% / 0% | 0.5899 |
| stocking removed: automated lean `bofn` vs conventional lean `bofn` | ONR (Cu) | 6/12, 6/12 | 839.6, 339.4 | 2.47 | 0.00 to unbounded | 2.47 (0.00 to unbounded) | 47% / 7% / 46% | 0.0500 |
| stocking removed: automated lean `heuristic` vs conventional lean `heuristic` | FLAIME (Al) | 12/12, 12/12 | 122.6, 106.8 | 1.15 | 0.60 to 2.11 | 1.21 (0.57 to 2.21) | 58% / 42% / 0% | 0.5512 |
| stocking removed: automated lean `heuristic` vs conventional lean `heuristic` | ONR (Cu) | 12/12, 10/12 | 490.1, 261.2 | 1.88 | 1.42 to 2.74 | 1.73 (1.38 to 2.73) | 79% / 7% / 14% | 0.0013 |
| stocking alone: automated stocked `bofn` vs automated lean `bofn` | FLAIME (Al) | 12/12, 11/12 | 189.3, 122.7 | 1.54 | 0.95 to 2.23 | 1.52 (0.91 to 2.22) | 69% / 31% / 0% | 0.1277 |
| stocking alone: automated stocked `bofn` vs automated lean `bofn` | ONR (Cu) | 6/12, 3/12 | 339.4, unbounded | none (new arm's median unbounded) | 0.00 to unbounded | none (new arm's median unbounded) (0.00 to unbounded) | 22% / 40% / 38% | 0.4077 |
| today's schedule: automated seeded `bofn` vs DAL 256 schedule seeded `bofn` | FLAIME (Al) | 12/12, 12/12 | 73.4, 2.5 | 29.69 | 7.49 to 29.69 | 29.69 (19.23 to 29.69) | 92% / 8% / 0% | 0.0002 |
| today's schedule: automated seeded `bofn` vs DAL 256 schedule seeded `bofn` | ONR (Cu) | 6/12, 12/12 | 335.8, 85.7 | 3.92 | 3.16 to unbounded | 3.94 (3.33 to unbounded) | 100% / 0% / 0% | < 0.0001 |
| optimizer alone, automated lab: `heuristic` (ref) vs `bofn_blend` | FLAIME (Al) | 12/12, 12/12 | 37.2, 116.2 | 0.32 | 0.10 to 1.11 | 0.21 (0.10 to 1.14) | 24% / 76% / 0% | 0.0322 |
| optimizer alone, automated lab: `heuristic` (ref) vs `bofn_blend` | ONR (Cu) | 7/12, 12/12 | 145.6, 225.3 | 0.65 | 0.53 to unbounded | 0.65 (0.54 to unbounded) | 49% / 51% / 0% | 0.9319 |
| optimizer alone, automated lab: `gpbo` (ref) vs `bofn` | FLAIME (Al) | 10/12, 11/12 | 190.1, 122.7 | 1.55 | 0.89 to 2.19 | 1.55 (0.88 to 2.33) | 73% / 26% / 1% | 0.0517 |
| optimizer alone, automated lab: `gpbo` (ref) vs `bofn` | ONR (Cu) | 8/12, 3/12 | 218.1, unbounded | none (new arm's median unbounded) | 0.00 to 1.49 | none (new arm's median unbounded) (0.00 to 1.49) | 22% / 53% / 25% | 0.1584 |
| optimizer alone, automated lab: `random` (ref) vs `bofn` | FLAIME (Al) | 1/12, 11/12 | unbounded, 122.7 | unbounded (reference's median unbounded) | unbounded to unbounded | unbounded (reference's median unbounded) (unbounded to unbounded) | 85% / 8% / 8% | 0.0003 |
| optimizer alone, automated lab: `random` (ref) vs `bofn` | ONR (Cu) | 4/12, 3/12 | unbounded, unbounded | none (neither arm's median is bounded) | 0.00 to unbounded | none (neither arm's median is bounded) (0.00 to unbounded) | 17% / 33% / 50% | 0.4067 |
| optimizer alone, conventional lab: `heuristic` (ref) vs `bofn` | FLAIME (Al) | 12/12, 12/12 | 122.6, 219.6 | 0.56 | 0.38 to 1.13 | 0.63 (0.33 to 1.15) | 26% / 74% / 0% | 0.0519 |
| optimizer alone, conventional lab: `heuristic` (ref) vs `bofn` | ONR (Cu) | 12/12, 6/12 | 490.1, 839.6 | 0.58 | 0.00 to 1.15 | 0.54 (0.00 to 1.15) | 25% / 75% / 0% | 0.0358 |

## 3. Cash to T1 ("the campaigns' own spending")

Ratio = median cash the new arm had spent when it reached T1 ÷ the reference's. Below 1: the new arm spent less.

| Comparison (reference → new) | Campaign | Median cash (ref, new) | Ratio new ÷ ref | 95% bootstrap interval | p |
|---|---|---|---|---|---|
| video headline: automated `bofn_blend` vs conventional `bofn` | FLAIME (Al) | $61421, $38845 | 0.63 | 0.36 to 1.02 | 0.0145 |
| video headline: automated `bofn_blend` vs conventional `bofn` | ONR (Cu) | $119811, $49687 | 0.41 | 0.00 to 0.74 | 0.0003 |
| same optimizer on both: automated `bofn` vs conventional `bofn` | FLAIME (Al) | $61421, $39611 | 0.64 | 0.35 to 1.08 | 0.0460 |
| same optimizer on both: automated `bofn` vs conventional `bofn` | ONR (Cu) | $119811, $unbounded | none (a median is unbounded) | 0.00 to unbounded | 0.6768 |
| video footer: automated `bofn_blend` vs conventional `heuristic` | FLAIME (Al) | $31577, $38845 | 1.23 | 0.49 to 2.11 | 0.8428 |
| video footer: automated `bofn_blend` vs conventional `heuristic` | ONR (Cu) | $64107, $49687 | 0.78 | 0.61 to 1.01 | 0.0284 |
| heuristic on both: automated `heuristic` vs conventional `heuristic` | FLAIME (Al) | $31577, $19713 | 0.62 | 0.24 to 1.22 | 0.1432 |
| heuristic on both: automated `heuristic` vs conventional `heuristic` | ONR (Cu) | $64107, $48294 | 0.75 | 0.55 to unbounded | 0.4834 |

## 4. Best alloy at the end of the year (mean true utility over seeds)

| Comparison (a against b) | Campaign | Seeds | Mean a | Mean b | a - b | 95% bootstrap interval | p (permutation) |
|---|---|---|---|---|---|---|---|
| Cu: `tiered` against `bofn_blend`, main (seeds 0-11) | ONR (Cu) | 12, 12 | 0.686 | 0.674 | +0.012 | -0.025 to +0.045 | 0.5213 |
| Cu: `tiered` against `bofn_blend`, seeds 12-23 only (`cu_seeds.jsonl`) | ONR (Cu) | 12, 12 | 0.675 | 0.495 | +0.180 | +0.043 to +0.338 | 0.0230 |
| Cu: `tiered` against `bofn_blend`, all 24 seeds | ONR (Cu) | 24, 24 | 0.680 | 0.584 | +0.096 | +0.021 to +0.185 | 0.0214 |
| Cu, hidden effect: `tiered` against `bofn_blend` | ONR (Cu) | 12, 12 | 0.686 | 0.552 | +0.134 | +0.003 to +0.297 | 0.0994 |
| Cu, hidden effect: `bofn_blend` against `bofn` | ONR (Cu) | 12, 12 | 0.552 | 0.291 | +0.261 | +0.033 to +0.477 | 0.0335 |
| Cu: `bofn_blend` against `bofn` | ONR (Cu) | 12, 12 | 0.674 | 0.327 | +0.347 | +0.187 to +0.510 | < 0.0001 |
| Cu, triple the money: `tiered` against `bofn_blend` (`cu_money.jsonl`) | ONR (Cu) | 12, 12 | 0.698 | 0.626 | +0.073 | +0.008 to +0.141 | 0.0592 |
| Al: `bofn_blend` against `heuristic` | FLAIME (Al) | 12, 12 | 0.687 | 0.605 | +0.082 | +0.038 to +0.123 | 0.0023 |
| Al: `bofn` against `gpbo` | FLAIME (Al) | 12, 12 | 0.650 | 0.455 | +0.195 | +0.065 to +0.342 | 0.0089 |
| Al: `bofn` against `random` | FLAIME (Al) | 12, 12 | 0.650 | 0.102 | +0.548 | +0.405 to +0.662 | < 0.0001 |
| Cu: `bofn` against `gpbo` | ONR (Cu) | 12, 12 | 0.327 | 0.529 | -0.202 | -0.394 to -0.007 | 0.0656 |
| Cu: `bofn` against `random` | ONR (Cu) | 12, 12 | 0.327 | 0.347 | -0.020 | -0.244 to +0.200 | 0.8648 |
| Al, seeded: `bofn` against `gpbo` | FLAIME (Al) | 12, 12 | 0.688 | 0.596 | +0.092 | +0.002 to +0.217 | 0.0759 |
| Cu, seeded: `bofn` against `gpbo` | ONR (Cu) | 12, 12 | 0.641 | 0.625 | +0.016 | -0.026 to +0.063 | 0.5083 |

## 5. Holm's correction over the 13 comparisons the video states

The family: the two headline speed-ups, the two against the heuristic, the two cash ratios shown in the results frame (the other cost bases are sums of the same cash and a time-proportional charge, so they are tested through days and cash), the heuristic-against-BOFN order on aluminium, and the three final-alloy comparisons of the description.

| Claim | p | Holm-adjusted p | Survives at 0.05 |
|---|---|---|---|
| time: video footer: automated `bofn_blend` vs conventional `heuristic`: onr_cu | < 0.0001 | < 0.0001 | yes |
| time: video headline: automated `bofn_blend` vs conventional `bofn`: onr_cu | < 0.0001 | 0.0004 | yes |
| cash: video headline: automated `bofn_blend` vs conventional `bofn`: onr_cu | 0.0003 | 0.0028 | yes |
| final: Al: `bofn_blend` against `heuristic` | 0.0023 | 0.0231 | yes |
| time: video headline: automated `bofn_blend` vs conventional `bofn`: flaime_al | 0.0056 | 0.0500 | on the line |
| cash: video headline: automated `bofn_blend` vs conventional `bofn`: flaime_al | 0.0145 | 0.1159 | no |
| cash: video footer: automated `bofn_blend` vs conventional `heuristic`: onr_cu | 0.0284 | 0.1989 | no |
| time: optimizer alone, automated lab: `heuristic` (ref) vs `bofn_blend`: flaime_al | 0.0322 | 0.1989 | no |
| final: Cu, hidden effect: `tiered` against `bofn_blend` | 0.0994 | 0.4972 | no |
| time: video footer: automated `bofn_blend` vs conventional `heuristic`: flaime_al | 0.3777 | 1.0000 | no |
| final: Cu: `tiered` against `bofn_blend`, main (seeds 0-11) | 0.5213 | 1.0000 | no |
| cash: video footer: automated `bofn_blend` vs conventional `heuristic`: flaime_al | 0.8428 | 1.0000 | no |
| time: optimizer alone, automated lab: `heuristic` (ref) vs `bofn_blend`: onr_cu | 0.9319 | 1.0000 | no |

## 6. The replayed seed (seed 0 of automated `bofn_blend`) against the 12 seeds

| Campaign | Seed 0 reached T1 on day | Rank among 12 (1 = earliest) | Median of 12 | Seed 0 final best | Rank (1 = best) | Mean of 12 |
|---|---|---|---|---|---|---|
| FLAIME (Al) | 20.3 | 1 | 116.2 | 0.707 | 5 | 0.687 |
| ONR (Cu) | 225.6 | 7 | 225.3 | 0.654 | 9 | 0.674 |

## 7. The same headline at the harder target T2

| Comparison | Campaign | Reached (ref, new) | Median days (ref, new) | AF | 95% bootstrap interval |
|---|---|---|---|---|---|
| video headline: automated `bofn_blend` vs conventional `bofn` | FLAIME (Al) | 12/12, 10/12 | 289.5, 152.9 | 1.89 | 1.05 to 4.18 |
| video headline: automated `bofn_blend` vs conventional `bofn` | ONR (Cu) | 1/12, 7/12 | unbounded, 277.9 | unbounded (reference's median unbounded) | unbounded to unbounded |
| same optimizer on both: automated `bofn` vs conventional `bofn` | FLAIME (Al) | 12/12, 8/12 | 289.5, 185.5 | 1.56 | 0.00 to 3.09 |
| same optimizer on both: automated `bofn` vs conventional `bofn` | ONR (Cu) | 1/12, 1/12 | unbounded, unbounded | none (neither arm's median is bounded) | 0.00 to unbounded |
| video footer: automated `bofn_blend` vs conventional `heuristic` | FLAIME (Al) | 9/12, 10/12 | 690.6, 152.9 | 4.52 | 1.49 to 8.67 |
| video footer: automated `bofn_blend` vs conventional `heuristic` | ONR (Cu) | 6/12, 7/12 | 951.5, 277.9 | 3.42 | 0.00 to unbounded |
| heuristic on both: automated `heuristic` vs conventional `heuristic` | FLAIME (Al) | 9/12, 3/12 | 690.6, unbounded | none (new arm's median unbounded) | 0.00 to 2.50 |
| heuristic on both: automated `heuristic` vs conventional `heuristic` | ONR (Cu) | 6/12, 2/12 | 951.5, unbounded | none (new arm's median unbounded) | 0.00 to 0.00 |

## 8. When each lab had its first new alloy, and what the year cost in cash

| Arm | Campaign | Median day of the first new alloy tested | Median new alloys tested by the end | Median cash spent (budget) |
|---|---|---|---|---|
| automated, stocked, `bofn_blend` (1 year) | FLAIME (Al) | 19.8 | 35 | $87,082 ($120,000) |
| automated, stocked, `bofn_blend` (1 year) | ONR (Cu) | 161.4 | 8 | $59,951 ($60,000) |
| automated, lean, `bofn` (1 year) | FLAIME (Al) | 71.5 | 24 | $69,670 ($120,000) |
| automated, lean, `bofn` (1 year) | ONR (Cu) | 120.3 | 8 | $59,448 ($60,000) |
| conventional, lean, `bofn` (3 years) | FLAIME (Al) | 95.5 | 70 | $294,082 ($360,000) |
| conventional, lean, `bofn` (3 years) | ONR (Cu) | 383.8 | 14 | $150,528 ($180,000) |
| DAL 256 schedule, lean, seeded `bofn` (1 year) | FLAIME (Al) | 73.4 | 18 | $85,726 ($120,000) |
| DAL 256 schedule, lean, seeded `bofn` (1 year) | ONR (Cu) | 290.0 | 1 | $43,524 ($60,000) |

## 9. Copper with all 24 automated seeds (`main.jsonl` seeds 0-11 plus `cu_seeds.jsonl` seeds 12-23)

The conventional lab has 12 seeds. The video's copper headline uses automated seeds 0-11 only.

| Comparison (reference → new) | Reached (ref, new) | Median days (ref, new) | AF | 95% bootstrap interval | p |
|---|---|---|---|---|---|
| conventional `bofn` → automated `bofn_blend`, seeds 0-11 (the video's) | 6/12, 12/12 | 839.6, 225.3 | 3.73 | 2.04 to unbounded | < 0.0001 |
| conventional `bofn` → automated `bofn_blend`, seeds 12-23 | 6/12, 7/12 | 839.6, 312.6 | 2.69 | 0.00 to unbounded | 0.0237 |
| conventional `bofn` → automated `bofn_blend`, all 24 | 6/12, 19/24 | 839.6, 243.4 | 3.45 | 1.77 to unbounded | 0.0002 |
| conventional `heuristic` → automated `bofn_blend`, all 24 | 12/12, 19/24 | 490.1, 243.4 | 2.01 | 1.52 to 2.48 | 0.0002 |
| conventional `tiered` → automated `bofn_blend`, all 24 | 12/12, 19/24 | 334.3, 243.4 | 1.37 | 1.05 to 1.91 | 0.0498 |
| conventional `tiered` → automated `tiered`, all 24 | 12/12, 21/24 | 334.3, 94.2 | 3.55 | 2.37 to 6.39 | < 0.0001 |

## 10. Seeds at T1 within the first 365 days, both labs on the same window

The conventional runs last three years; this counts only their first year. p: Fisher's exact test, two-sided.

| Policy (conventional, automated) | Campaign | Conventional by day 365 | Automated by day 365 | p |
|---|---|---|---|---|
| `bofn`, `bofn_blend` | FLAIME (Al) | 11/12 | 12/12 | 1.000 |
| `bofn`, `bofn_blend` | ONR (Cu) | 1/12 | 12/12 | 0.000 |
| `bofn`, `bofn` | FLAIME (Al) | 11/12 | 11/12 | 1.000 |
| `bofn`, `bofn` | ONR (Cu) | 1/12 | 3/12 | 0.590 |
| `heuristic`, `heuristic` | FLAIME (Al) | 12/12 | 12/12 | 1.000 |
| `heuristic`, `heuristic` | ONR (Cu) | 2/12 | 7/12 | 0.089 |
| `tiered`, `tiered` | FLAIME (Al) | 6/12 | 7/12 | 1.000 |
| `tiered`, `tiered` | ONR (Cu) | 8/12 | 11/12 | 0.317 |
| `gpbo`, `gpbo` | FLAIME (Al) | 6/12 | 10/12 | 0.193 |
| `gpbo`, `gpbo` | ONR (Cu) | 2/12 | 8/12 | 0.036 |
| `random`, `random` | FLAIME (Al) | 3/12 | 1/12 | 0.590 |
| `random`, `random` | ONR (Cu) | 1/12 | 4/12 | 0.317 |
| `sobol`, `sobol` | FLAIME (Al) | 1/12 | 1/12 | 1.000 |
| `sobol`, `sobol` | ONR (Cu) | 2/12 | 3/12 | 1.000 |

