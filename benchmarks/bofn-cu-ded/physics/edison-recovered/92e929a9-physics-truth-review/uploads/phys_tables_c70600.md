# Physics-based truth: checks

Immersion reference: C70600. CALPHAD grid: 864 points, 0 missing.

## Corrosion model on dense, beta-free coupons

| Alloy | Ni in alpha (900 C) | Al in alpha (900 C) | Fe in solution | 30-day mass loss (uA d/cm2) | ratio to C71500 | mean rate (mm/y) | i at 1 h | 1 d | 10 d | 30 d (uA/cm2) | m | passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cu (C10100) | 0.0 | 0.0 | 0.00 | 116.3 | 3.46 | 0.0453 | 6.9 | 4.3 | 3.84 | 3.74 | 0.518 | no |
| C70600 90-10 Cu-Ni | 10.0 | 0.0 | 1.40 | 41.7 | 1.24 | 0.0163 | 6.5 | 3.5 | 1.33 | 0.77 | 0.815 | yes |
| C71500 70-30 Cu-Ni | 30.0 | 0.0 | 0.68 | 33.6 | 1.00 | 0.0131 | 5.8 | 3.0 | 1.05 | 0.58 | 0.877 | yes |
| C61400 aluminum bronze | 0.0 | 6.9 | 0.98 | 61.0 | 1.82 | 0.0238 | 6.3 | 3.6 | 2.03 | 1.49 | 0.705 | no |
| C95800 NAB | 2.4 | 8.1 | 2.17 | 43.3 | 1.29 | 0.0169 | 6.2 | 3.3 | 1.40 | 0.86 | 0.804 | no |
| Cu-7Ni-3Al-1Fe-1Mn (Yang 2018) | 6.8 | 3.0 | 0.96 | 53.6 | 1.59 | 0.0209 | 6.4 | 3.6 | 1.76 | 1.20 | 0.742 | no |
| NAB 7Al-7Ni-4Fe-2Mn (Tan 2024) | 2.1 | 5.4 | 1.04 | 57.0 | 1.70 | 0.0222 | 6.4 | 3.6 | 1.89 | 1.33 | 0.724 | no |
| NAB 9Al-5Ni-4Fe-2Mn (Tan 2024) | 3.8 | 8.5 | 2.98 | 41.5 | 1.23 | 0.0162 | 6.1 | 3.3 | 1.33 | 0.81 | 0.816 | yes |
| v1 optimum (13Ni-5.5Al-2.2Fe) | 5.8 | 3.6 | 1.41 | 44.2 | 1.31 | 0.0172 | 6.4 | 3.5 | 1.42 | 0.87 | 0.798 | no |

m_ref = 0.8078 (C70600 dense at its best settings, rho_m = 0.978; 'passes' compares with it). Mean rate uses n = 2 (0.0117 mm/y per uA/cm2). The film model reads the alpha composition at 900 C (Fe capped at 1.5 wt%).

## Reference alloys at their best settings for J, (kappa, eta) = (1, 1)

| Alloy | J | T_liq (C) | Scheil range (K) | beta at 900 C | kappa at 700 C | s | f | g | h | rho_u | rho_m | beta | U | w | m | passes | feasible |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cu (C10100) | 0.000 | 1084 | 0 | 0.00 | 0.000 | 0.00 | 0.00 | 0.00 | 0.95 | 0.00 | 0.43 | 0.00 | 0.11 | 0.31 | 0.388 | no | yes |
| C70600 90-10 Cu-Ni | 0.034 | 1131 | 85 | 0.00 | 0.000 | 0.06 | 0.34 | 0.00 | 0.10 | 0.89 | 0.98 | 0.00 | 0.29 | 0.45 | 0.808 | yes | yes |
| C71500 70-30 Cu-Ni | -0.073 | 1228 | 162 | 0.00 | 0.000 | 0.16 | 0.65 | 0.00 | 0.05 | 0.69 | 0.91 | 0.00 | 0.34 | 0.46 | 0.852 | yes | yes |
| C61400 aluminum bronze | -0.015 | 1069 | 28 | 0.00 | 0.030 | 0.32 | 0.11 | 0.00 | 0.13 | 0.91 | 0.99 | 0.00 | 0.48 | 0.46 | 0.701 | no | yes |
| C95800 NAB | -0.136 | 1116 | 96 | 0.47 | 0.133 | 0.51 | 0.38 | 0.70 | 0.08 | 0.87 | 0.95 | 0.25 | 0.62 | 0.46 | 0.611 | no | yes |
| Cu-7Ni-3Al-1Fe-1Mn (Yang 2018) | -0.025 | 1094 | 68 | 0.00 | 0.059 | 0.29 | 0.27 | 0.00 | 0.09 | 0.97 | 0.98 | 0.00 | 0.46 | 0.46 | 0.736 | no | yes |
| NAB 7Al-7Ni-4Fe-2Mn (Tan 2024) | -0.089 | 1103 | 113 | 0.00 | 0.167 | 0.50 | 0.45 | 0.71 | 0.08 | 0.94 | 0.96 | 0.00 | 0.60 | 0.45 | 0.712 | no | yes |
| NAB 9Al-5Ni-4Fe-2Mn (Tan 2024) | -0.161 | 1108 | 100 | 0.68 | 0.142 | 0.52 | 0.40 | 0.66 | 0.06 | 0.85 | 0.94 | 0.36 | 0.64 | 0.46 | 0.563 | no | yes |
| v1 optimum (13Ni-5.5Al-2.2Fe) | 0.063 | 1129 | 74 | 0.00 | 0.177 | 0.44 | 0.29 | 0.00 | 0.11 | 0.97 | 0.98 | 0.00 | 0.57 | 0.46 | 0.793 | no | yes |
## Landscape (uniform random designs)

- 400,000 designs; 74.5% lie inside the proposal's limits (liquidus <= 1,250 C, Cu >= 65 wt%, Ni >= Fe above 7 wt% Al, Fe <= 2.3 wt% below 1.5 wt% Al).
- Pass immersion: 0.7% of the box, 0.7% of the feasible space.
- J > 0: 0.2% of the box, 0.2% of the feasible space.
- Within 60% / 80% of the optimum (feasible space): 0.00% / 0.000%.
- Lowest Ni among designs that pass immersion: 9.20 wt% (box), 9.20 wt% (feasible).

- With a 10 wt% Ni floor (46% of the box): 1.1% pass immersion, 0.3% have J > 0, 0.01% are within 60% of the optimum.
  - Ni 0-1 wt%: 0.00% of feasible designs pass immersion
  - Ni 1-2 wt%: 0.00% of feasible designs pass immersion
  - Ni 2-3 wt%: 0.00% of feasible designs pass immersion
  - Ni 3-4 wt%: 0.00% of feasible designs pass immersion
  - Ni 4-5 wt%: 0.00% of feasible designs pass immersion
  - Ni 5-6 wt%: 0.00% of feasible designs pass immersion
  - Ni 6-7 wt%: 0.00% of feasible designs pass immersion
  - Ni 8-10 wt%: 0.02% of feasible designs pass immersion
  - Ni 10-12 wt%: 0.09% of feasible designs pass immersion
  - Ni 12-15 wt%: 0.21% of feasible designs pass immersion
  - Ni 15-20 wt%: 0.62% of feasible designs pass immersion
  - Ni 20-30 wt%: 2.50% of feasible designs pass immersion
- Expected best of 5 / 24 uniform random feasible designs: -55% / -28% of the optimum; mean best of the five shared seed designs (seeds 0-19): -46%.


## Optimum, (kappa, eta) = (1, 1)

J* = 0.1900 at Ni 15.0 wt%, Al 3.0, Fe 1.5, Mn 0.0; a = 0.4334, P = 0.5712, v = 0.4695. s = 0.34, f = 0.21, g = 0.00, h = 0.08, q = 0.98, rho_u = 0.87, rho_m = 0.99, beta = 0.000, U = 0.50, w = 0.47, m = 0.858.

