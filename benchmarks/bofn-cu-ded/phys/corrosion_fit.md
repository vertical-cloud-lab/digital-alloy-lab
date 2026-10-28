# Film corrosion model: fit and nickel floor (written by `phys/fit_corrosion.py`)

16 rates from 6 studies; ln(rate) RMSE 0.23. Coefficients per wt% (Ni through the film term): ni -0.318, al -0.169, al2 +0.323, fe -0.000 (Al2 multiplies Al^2/10). Floors of the base fit: 90-10 bar 1.0 wt% Ni (witness Ni 1.0, Al 2.4, Fe 0.0), 70-30 bar 1.9 wt% Ni (witness Ni 1.9, Al 2.3, Fe 0.0).

| Fit | b_Ni (film) | b_Al | b_Al2 (per Al^2/10) | b_Fe | RMSE (ln) | Ni floor, 90-10 bar (wt%) | Ni floor, 70-30 bar (wt%) |
|---|---|---|---|---|---|---|---|
| base: saturating film (Ni scale 5 wt%), quadratic Al, signs fixed | -0.32 | -0.169 | +0.323 | -0.000 | 0.23 | 1.0 | 1.9 |
| linear Al | -0.00 | +0.140 | +0.000 | -0.000 | 0.31 | 0.0 | 0.0 |
| signs free | -0.01 | -0.134 | +0.291 | +0.387 | 0.21 | 0.0 | 0.0 |
| linear Al, signs free (the first form tried) | +0.44 | +0.151 | -0.000 | +0.511 | 0.27 | 0.0 | 0.0 |
| Ni scale 3 wt% | -0.03 | -0.137 | +0.307 | -0.000 | 0.24 | 0.0 | 0.0 |
| Ni scale 8 wt% | -0.58 | -0.197 | +0.335 | -0.000 | 0.22 | 2.0 | 5.3 |
| Ni scale 12 wt% | -0.68 | -0.201 | +0.336 | -0.000 | 0.21 | 1.6 | 7.8 |
| linear Ni | -0.19 | -0.188 | +0.328 | -0.000 | 0.20 | 0.0 | 15.9 |
| Fe in solution up to 1.0 wt% | -0.32 | -0.169 | +0.323 | -0.000 | 0.23 | 1.0 | 1.9 |
| Fe in solution up to 2.5 wt% | -0.32 | -0.169 | +0.323 | -0.000 | 0.23 | 1.0 | 1.9 |
| no ridge | -0.41 | -0.183 | +0.332 | -0.000 | 0.23 | 1.5 | 2.5 |
| strong ridge (0.5) | -0.09 | -0.116 | +0.281 | -0.000 | 0.24 | 0.0 | 0.0 |
| equal weights | -0.30 | -0.167 | +0.337 | -0.000 | 0.23 | 0.9 | 1.8 |
| without LewisLaQue1981_1y | -1.01 | -0.289 | +0.304 | -0.000 | 0.15 | 1.1 | 2.0 |
| without LewisLaQue1981_quiet | -0.33 | -0.170 | +0.323 | -0.000 | 0.25 | 1.1 | 2.0 |
| without Qian2025 | -0.19 | -0.155 | +0.316 | -0.000 | 0.22 | 0.0 | 0.1 |
| without Tan2024 | -0.65 | -0.366 | +0.561 | -0.000 | 0.22 | 0.0 | 0.5 |
| without Yang2018 | -0.11 | -0.044 | +0.220 | -0.000 | 0.23 | 5.5 | 8.0 |
| without Zhao2022 | -0.00 | -0.152 | +0.329 | -0.000 | 0.20 | 0.0 | 0.0 |

Across these fits the floor ranges from 0.0 to 5.5 wt% Ni with the 90-10 bar and from 0.0 to 15.9 wt% with the 70-30 bar.

Residuals of the base fit (ln rate, observed vs fitted, within each study's own intercept):

| Study | Alloy | ln observed | ln fitted |
|---|---|---|---|
| Tan2024 | ZCuAl7-7-4-2 (cast) | -1.05 | -1.23 |
| Tan2024 | Cu-7.90Al-6.13Ni-3.92Fe-2.12Mn (cast) | -1.02 | -0.92 |
| Tan2024 | Cu-8.94Al-5.18Ni-4.12Fe-2.18Mn (cast) | -0.37 | -0.51 |
| Tan2024 | Cu-9.94Al-3.99Ni-3.94Fe-1.82Mn (cast) | -0.25 | -0.04 |
| Yang2018 | Cu-7Ni-3Al-1Fe-1Mn (cast) | -3.84 | -3.67 |
| Yang2018 | C70600 (commercial; nominal composition assumed) | -3.33 | -3.49 |
| Qian2025 | B10 (wrought tube) | -8.60 | -8.89 |
| Qian2025 | B30 (wrought tube) | -9.22 | -8.92 |
| LewisLaQue1981_quiet | C70600 (9-11 Ni 1-2 Fe 0.5-1 Mn; midpoints) | -0.92 | -0.90 |
| LewisLaQue1981_quiet | C71500 (about Cu-30Ni-0.5Fe) | -0.92 | -0.94 |
| LewisLaQue1981_1y | generic aluminum bronze (grade unspecified; C61400 assumed) | +3.77 | +4.00 |
| LewisLaQue1981_1y | generic NAB (grade unspecified; C95800 assumed) | +5.01 | +4.61 |
| LewisLaQue1981_1y | C70600 | +3.42 | +3.32 |
| LewisLaQue1981_1y | C71500 | +3.01 | +3.28 |
| Zhao2022 | N-1 laser-deposited NAB on steel (diluted) | +2.06 | +1.71 |
| Zhao2022 | N-2 laser-deposited NAB on steel (diluted) | +1.54 | +1.88 |
