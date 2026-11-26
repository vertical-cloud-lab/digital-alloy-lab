<!-- Edison artifact key: artifact-00 -->
| Paper / benchmark | Dimensionality, d | Initial design, m | Type of initial points | Total budget, T | Ratio m/d |
|---|---:|---:|---|---:|---:|
| Eriksson & Jankowiak (2021), runtime test | 100 | 10 | Sobol (SAASBO algorithm default) | 50 | 0.100 (pqac-00000001, pqac-00000055) |
| Eriksson & Jankowiak (2021), MOPTA vehicle design | 124 | 50 | Initial-design method not restated; SAASBO default is Sobol | Not reported in cited passage | 0.403 (pqac-00000003, pqac-00000055) |
| Eriksson & Jankowiak (2021), SVM | 388 | 20 | Initial-design method not restated; SAASBO default is Sobol | Not reported in cited passage | 0.052 (pqac-00000003, pqac-00000055) |
| Papenmeier et al. (2023), BAxUS follow-up benchmark | 388 | 10 | Common initial samples; exact generator not stated in cited passage | 1,000 | 0.026 (pqac-00000005) |
| Hvarfner et al. (2024), vanilla BO benchmarks | 12–6,392 | 30 | Common initialization; acquisition optimization uses global Sobol and incumbent-centered samples | Task-dependent | 2.500–0.0047 (pqac-00000068) |
| Xu et al. (2024), 30D–388D benchmarks | 30–388 | 20 | Matched initial datasets across methods; exact generator not stated in cited passage | Task-dependent | 0.667–0.052 (pqac-00000030) |
| Xu et al. (2024), Humanoid-Standup | 1,003 | 50 | Matched initial dataset; exact generator not stated in cited passage | Task-dependent | 0.050 (pqac-00000030) |
| Baird et al. (2022), CrabNet hyperparameter optimization | 23 | Ax default; count not established in cited passage | Ax-generated initialization | 100 adaptive iterations | Not computable (pqac-00000009, pqac-00000010) |
| Proposed aluminium-alloy campaign | 15 candidate elements | 6 | Hand-picked: 2 commercial, 3 literature-derived, 1 exploratory | ≈25 | 0.400 |


*Table: Published SAASBO and high-dimensional BO benchmarks generally begin with 10–50 initial observations and usually use randomized or quasi-random coverage. The proposed six-point expert seed has a moderate numerical m/d ratio, but unlike the benchmark initializations it is not space-filling.*
