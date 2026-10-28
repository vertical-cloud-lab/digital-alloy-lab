# Truth tables (written by `check_truth.py`)

`m_ref` = 0.849: the immersion index of C71500 (70-30 Cu-Ni) deposited dense (rho_m = 0.85) at its best settings (a, P, v) = (0.62, 0.53, 0.30) in the headline world, fixed for every cell. CALPHAD crack screen: f <= 0.34. One-hour screen gate: top quartile by w of the dense candidates (rho_m >= 0.5) that passed the CALPHAD screen, which is what a tiered lab would be ranking.

## The optimum per cell (multi-start local search from the best of 400,000 random designs)

| (kappa, eta) | J* | Ni | Al | Fe | Mn | a | P | v | s | f | g | h | q | rho_u | rho_m | beta | U | w | m | burden |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (1, 1) | **0.492** | 0.43 | 0.58 | 0.50 | 0.00 | 0.64 | 0.58 | 0.34 | 0.73 | 0.74 | 0.41 | 0.12 | 0.81 | 0.79 | 0.93 | 0.15 | 0.76 | 0.88 | 0.95 | 0.61 |
| (0, 0) | **0.382** | 0.32 | 0.38 | 0.40 | 0.00 | 0.50 | 0.63 | 0.48 | 0.55 | 0.40 | 0.29 | 0.21 | 0.94 | 0.63 | 0.95 | 0.11 | 0.64 | 0.97 | 0.92 | 0.43 |
| (1, 0) | **0.492** | 0.43 | 0.58 | 0.50 | 0.00 | 0.64 | 0.58 | 0.34 | 0.73 | 0.74 | 0.41 | 0.12 | 0.81 | 0.79 | 0.93 | 0.15 | 0.76 | 1.00 | 0.95 | 0.61 |
| (0, 1) | **0.382** | 0.32 | 0.38 | 0.40 | 0.00 | 0.50 | 0.63 | 0.48 | 0.55 | 0.40 | 0.29 | 0.21 | 0.94 | 0.63 | 0.95 | 0.11 | 0.64 | 0.79 | 0.92 | 0.43 |

## Required property 1: what the screens do to the optimum

| (kappa, eta) | optimum's f (screen keeps f <= 0.34) | fails CALPHAD screen | optimum's w percentile among dense candidates | below the top quartile | best design passing the CALPHAD screen (% of J*) | best passing both screens (% of J*) |
|---|---|---|---|---|---|---|
| (1, 1) | 0.74 | yes | 100% | no | 72% | 72% |
| (0, 0) | 0.40 | yes | 100% | no | 92% | 92% |
| (1, 0) | 0.74 | yes | 100% | no | 72% | 72% |
| (0, 1) | 0.40 | yes | 97% | no | 92% | 92% |

## Required property 2: the reference alloys at their best settings for J

**(1, 1)**

| Alloy | J | % of J* | U | rho_m | beta | m | passes immersion (m >= m_ref) | w | f | passes CALPHAD screen | burden | densest build: rho_m, beta, m, passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | -0.073 | -15% | 0.48 | 0.85 | 0.00 | 0.85 | yes | 0.83 | 0.72 | no | 1.04 | 0.85, 0.00, 0.85, yes |
| C70600 (90-10 Cu-Ni) | 0.120 | 24% | 0.38 | 0.96 | 0.00 | 0.87 | yes | 0.71 | 0.29 | yes | 0.37 | 0.96, 0.00, 0.87, yes |
| C95800 (NAB) | -0.146 | -30% | 0.79 | 0.92 | 0.48 | 0.55 | no | 0.82 | 0.26 | yes | 0.49 | 0.97, 0.55, 0.53, no |

**(0, 0)**

| Alloy | J | % of J* | U | rho_m | beta | m | passes immersion (m >= m_ref) | w | f | passes CALPHAD screen | burden | densest build: rho_m, beta, m, passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | -0.308 | -81% | 0.15 | 0.26 | 0.00 | 0.67 | no | 0.82 | 0.72 | no | 1.04 | 0.26, 0.00, 0.67, no |
| C70600 (90-10 Cu-Ni) | 0.117 | 31% | 0.38 | 0.96 | 0.00 | 0.87 | yes | 0.88 | 0.29 | yes | 0.37 | 0.96, 0.00, 0.87, yes |
| C95800 (NAB) | -0.146 | -38% | 0.79 | 0.92 | 0.48 | 0.55 | no | 0.74 | 0.26 | yes | 0.49 | 0.97, 0.55, 0.53, no |

**(1, 0)**

| Alloy | J | % of J* | U | rho_m | beta | m | passes immersion (m >= m_ref) | w | f | passes CALPHAD screen | burden | densest build: rho_m, beta, m, passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | -0.073 | -15% | 0.48 | 0.85 | 0.00 | 0.85 | yes | 0.88 | 0.72 | no | 1.04 | 0.85, 0.00, 0.85, yes |
| C70600 (90-10 Cu-Ni) | 0.120 | 24% | 0.38 | 0.96 | 0.00 | 0.87 | yes | 0.88 | 0.29 | yes | 0.37 | 0.96, 0.00, 0.87, yes |
| C95800 (NAB) | -0.146 | -30% | 0.79 | 0.92 | 0.48 | 0.55 | no | 0.74 | 0.26 | yes | 0.49 | 0.97, 0.55, 0.53, no |

**(0, 1)**

| Alloy | J | % of J* | U | rho_m | beta | m | passes immersion (m >= m_ref) | w | f | passes CALPHAD screen | burden | densest build: rho_m, beta, m, passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | -0.308 | -81% | 0.15 | 0.26 | 0.00 | 0.67 | no | 0.78 | 0.72 | no | 1.04 | 0.26, 0.00, 0.67, no |
| C70600 (90-10 Cu-Ni) | 0.117 | 31% | 0.38 | 0.96 | 0.00 | 0.87 | yes | 0.71 | 0.29 | yes | 0.37 | 0.96, 0.00, 0.87, yes |
| C95800 (NAB) | -0.146 | -38% | 0.79 | 0.92 | 0.48 | 0.55 | no | 0.82 | 0.26 | yes | 0.49 | 0.97, 0.55, 0.53, no |

## Required property 3: the optimum is a ridge in (P, v)

| (kappa, eta) | grid points within 0.5% of J* (of 10,201) | P range | v range | P - v range |
|---|---|---|---|---|
| (1, 1) | 17 (0.2%) | 0.53 to 0.64 | 0.29 to 0.40 | 0.23 to 0.24 |
| (0, 0) | 8 (0.1%) | 0.59 to 0.66 | 0.44 to 0.51 | 0.15 to 0.15 |
| (1, 0) | 17 (0.2%) | 0.53 to 0.64 | 0.29 to 0.40 | 0.23 to 0.24 |
| (0, 1) | 8 (0.1%) | 0.59 to 0.66 | 0.44 to 0.51 | 0.15 to 0.15 |

## Required property 4: the Utah power cap binds for copper-rich compositions

| (kappa, eta) | compositions | median best rho_u (Utah, P <= 0.5) | median best rho_m (Mines) | share with best rho_u < 0.3 | share passing the Utah gate (rho_u >= 0.5) | share with best rho_m > 0.7 | optimum's composition: best rho_u, best rho_m |
|---|---|---|---|---|---|---|---|
| (1, 1) | copper-rich (Ni <= 0.07, Al <= 0.2, i.e. under about 2 wt% Ni and 2 wt% Al) (first 200) | 0.40 | 0.88 | 15% | 15% | 100% | 0.92, 0.93 |
| (0, 0) | copper-rich (Ni <= 0.07, Al <= 0.2, i.e. under about 2 wt% Ni and 2 wt% Al) (first 200) | 0.40 | 0.88 | 15% | 15% | 100% | 0.93, 0.94 |
| (1, 0) | copper-rich (Ni <= 0.07, Al <= 0.2, i.e. under about 2 wt% Ni and 2 wt% Al) (first 200) | 0.40 | 0.88 | 15% | 15% | 100% | 0.92, 0.93 |
| (0, 1) | copper-rich (Ni <= 0.07, Al <= 0.2, i.e. under about 2 wt% Ni and 2 wt% Al) (first 200) | 0.40 | 0.88 | 15% | 15% | 100% | 0.93, 0.94 |
