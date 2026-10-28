# Film corrosion model: fit and nickel floor (written by `phys/fit_corrosion.py`)

30 rates from 11 studies; ln(rate) RMSE 0.23. Coefficients per wt% (Ni through the film term): ni -0.841, al -0.280, al2 +0.386, fe -0.000 (Al2 multiplies Al^2/10). Floors of the base fit: 90-10 bar 1.6 wt% Ni (witness Ni 1.6, Al 3.1, Fe 0.0), 70-30 bar 2.6 wt% Ni (witness Ni 2.6, Al 3.2, Fe 0.0).

| Fit | b_Ni (film) | b_Al | b_Al2 (per Al^2/10) | b_Fe | RMSE (ln) | Ni floor, 90-10 bar (wt%) | Ni floor, 70-30 bar (wt%) |
|---|---|---|---|---|---|---|---|
| base: saturating film (Ni scale 5 wt%), quadratic Al, signs fixed | -0.84 | -0.280 | +0.386 | -0.000 | 0.23 | 1.6 | 2.6 |
| linear Al | -0.73 | +0.040 | +0.000 | -0.000 | 0.32 | 10.0 | 30.0 |
| signs free | -0.91 | -0.286 | +0.382 | +0.129 | 0.22 | 0.5 | 2.0 |
| linear Al, signs free (the first form tried) | -0.82 | +0.029 | -0.000 | +0.153 | 0.32 | 4.7 | 10.9 |
| Ni scale 3 wt% | -0.74 | -0.272 | +0.389 | -0.000 | 0.25 | 1.2 | 1.4 |
| Ni scale 8 wt% | -0.93 | -0.283 | +0.383 | -0.000 | 0.20 | 1.4 | 4.4 |
| Ni scale 12 wt% | -1.00 | -0.277 | +0.380 | -0.030 | 0.19 | 0.7 | 5.8 |
| linear Ni | -0.28 | -0.259 | +0.378 | -0.208 | 0.18 | 0.0 | 7.9 |
| Fe in solution up to 1.0 wt% | -0.84 | -0.280 | +0.386 | -0.000 | 0.23 | 1.6 | 2.6 |
| Fe in solution up to 2.5 wt% | -0.84 | -0.280 | +0.386 | -0.000 | 0.23 | 1.6 | 2.6 |
| no ridge | -0.87 | -0.288 | +0.392 | -0.000 | 0.23 | 1.5 | 2.5 |
| strong ridge (0.5) | -0.65 | -0.226 | +0.338 | -0.000 | 0.23 | 1.7 | 2.7 |
| equal weights | -0.80 | -0.313 | +0.439 | -0.000 | 0.22 | 1.0 | 1.8 |
| without AlFozan2008 | -0.81 | -0.276 | +0.384 | -0.000 | 0.22 | 1.5 | 2.5 |
| without CohenWhitted1971 | -0.90 | -0.233 | +0.355 | -0.000 | 0.23 | 2.9 | 4.3 |
| without LewisLaQue1981_1y | -0.95 | -0.274 | +0.295 | -0.000 | 0.16 | 1.2 | 2.1 |
| without LewisLaQue1981_quiet | -0.85 | -0.281 | +0.386 | -0.000 | 0.23 | 1.6 | 2.6 |
| without Qian2025 | -0.82 | -0.278 | +0.385 | -0.000 | 0.22 | 1.5 | 2.5 |
| without Ravindran1983 | -0.72 | -0.264 | +0.377 | -0.000 | 0.23 | 1.3 | 2.2 |
| without Tan2024 | -0.90 | -0.443 | +0.613 | -0.000 | 0.21 | 0.0 | 0.6 |
| without Wheatfall1967_123d | -0.87 | -0.284 | +0.388 | -0.000 | 0.23 | 1.6 | 2.6 |
| without Wheatfall1967_surface | -0.78 | -0.273 | +0.382 | -0.000 | 0.23 | 1.5 | 2.4 |
| without Yang2018 | -0.83 | -0.262 | +0.368 | -0.000 | 0.23 | 1.9 | 2.9 |
| without Zhao2022 | -0.81 | -0.286 | +0.397 | -0.000 | 0.22 | 1.4 | 2.3 |
| with Reinhart 1968 copper and Cu-Ni (Edison's bridge data; deep, cold) | -0.46 | -0.231 | +0.359 | -0.000 | 0.23 | 0.4 | 1.1 |
| with all of Reinhart 1968 (also its Al bronzes and NAB) | -0.57 | -0.332 | +0.242 | -0.000 | 0.39 | 0.0 | 0.0 |

Across these fits the floor ranges from 0.0 to 10.0 wt% Ni with the 90-10 bar and from 0.0 to 30.0 wt% with the 70-30 bar.

Residuals of the base fit (ln rate, observed vs fitted, within each study's own intercept):

| Study | Alloy | ln observed | ln fitted |
|---|---|---|---|
| Tan2024 | ZCuAl7-7-4-2 (cast) | -1.05 | -1.26 |
| Tan2024 | Cu-7.90Al-6.13Ni-3.92Fe-2.12Mn (cast) | -1.02 | -0.94 |
| Tan2024 | Cu-8.94Al-5.18Ni-4.12Fe-2.18Mn (cast) | -0.37 | -0.51 |
| Tan2024 | Cu-9.94Al-3.99Ni-3.94Fe-1.82Mn (cast) | -0.25 | +0.02 |
| Yang2018 | Cu-7Ni-3Al-1Fe-1Mn (cast) | -3.84 | -3.78 |
| Yang2018 | C70600 (commercial; nominal composition assumed) | -3.33 | -3.38 |
| Qian2025 | B10 (wrought tube) | -8.60 | -8.86 |
| Qian2025 | B30 (wrought tube) | -9.22 | -8.95 |
| LewisLaQue1981_quiet | C70600 (9-11 Ni 1-2 Fe 0.5-1 Mn; midpoints) | -0.92 | -0.86 |
| LewisLaQue1981_quiet | C71500 (about Cu-30Ni-0.5Fe) | -0.92 | -0.97 |
| LewisLaQue1981_1y | generic aluminum bronze (grade unspecified; C61400 assumed) | +3.77 | +4.09 |
| LewisLaQue1981_1y | generic NAB (grade unspecified; C95800 assumed) | +5.01 | +4.37 |
| LewisLaQue1981_1y | C70600 | +3.42 | +3.43 |
| LewisLaQue1981_1y | C71500 | +3.01 | +3.32 |
| Zhao2022 | N-1 laser-deposited NAB on steel (diluted) | +2.06 | +1.81 |
| Zhao2022 | N-2 laser-deposited NAB on steel (diluted) | +1.54 | +1.79 |
| Ravindran1983 | Copper CDA 110 | +4.11 | +3.97 |
| Ravindran1983 | 90-10 Cu-Ni (nominal) | +3.11 | +3.24 |
| Ravindran1983 | 70-30 Cu-Ni (nominal) | +3.11 | +3.13 |
| Wheatfall1967_123d | Unalloyed Cu | +2.49 | +2.58 |
| Wheatfall1967_123d | Cu-Ni(30) (nominal) | +1.84 | +1.75 |
| Wheatfall1967_surface | Unalloyed Cu (loss largely localized) | +1.50 | +1.35 |
| Wheatfall1967_surface | Cu-Ni(30) (nominal) | +0.35 | +0.51 |
| CohenWhitted1971 | C122 copper | -0.01 | +0.04 |
| CohenWhitted1971 | C608 aluminum bronze (Al 5.0-6.5) | -0.29 | -0.29 |
| CohenWhitted1971 | C613 aluminum bronze (Al 6-8; Fe <= 3.5) | -0.31 | -0.02 |
| CohenWhitted1971 | C706 90-10 Cu-Ni | -0.36 | -0.68 |
| CohenWhitted1971 | C715 70-30 Cu-Ni | -0.78 | -0.79 |
| AlFozan2008 | 90/10 Cu-Ni (measured: Ni 9.93 Fe 1.41 Mn 0.273) | -1.93 | -2.26 |
| AlFozan2008 | 70/30 Cu-Ni (measured: Ni 30 Fe 0.53 Mn 0.51) | -2.70 | -2.37 |
