# Full BOFN benchmark — GitHub Actions run #5

- Workflow run: [24736409107](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/actions/runs/24736409107)
- Head SHA: `2afb7dd`
- Algorithms × seeds: 7 × 20 = 140 parallel jobs (Random, Sobol, LowFidOnly, Node2Only, HighFidOnly, TSFN, pKGFN)
- Equal-cost budget: $2,400 on the 6-node Extended Manufacturing DAG (noise_std=0.05)
- True network max (median over seeds): 1.297 (black dashed line in the figure)
- Source artifact (full per-seed JSONs): `../../results/actions_full/bofn-combined-24736409107.zip`

## Final posterior-mean (mean ± 1σ over 20 seeds)

| Algorithm   | Final mean | ± std  | Avg iters |
|-------------|-----------:|-------:|----------:|
| TSFN        | 1.177      | 0.062  | 11.0      |
| HighFidOnly | 1.150      | 0.114  | 11.0      |
| pKGFN       | 1.043      | 0.130  | 44.0      |
| Sobol       | 1.004      | 0.103  | 11.0      |
| Random      | 1.000      | 0.130  | 11.0      |
| LowFidOnly  | 0.894      | 0.162  | 264.0     |
| Node2Only   | 0.894      | 0.161  | 132.0     |

TSFN (BOFN Thompson sampling) ranks first and HighFidOnly second at matched
cost; both pull clearly ahead of Random/Sobol. pKGFN spends its budget on
cheap root nodes (4× more acquisition iterations than HighFidOnly) but on
this harder 6-node noisy problem it trails TSFN — the extra cheap-node
observations haven't yet paid off at this budget. Single-root baselines
(LowFidOnly, Node2Only) trail all full-pipeline methods because they never
observe the terminal node y5. The dashed reference at 1.297 shows there is
still a meaningful gap to the noise-free optimum for every algorithm.
