# FT-1 laser-hazard numbers for the LSO (`lso_numbers.py`)

Inputs: 400 W CW at 1070 nm, M² 1.1, 5 mm collimated beam, f = 254 mm. Method and MPE values: PR 266's `desktop-lpbf/safety_calcs.py` §1 (ANSI Z136.1 via the NIU manual). Estimates for the request; the LSO's evaluation decides.

| Quantity | Value | Basis |
|---|---|---|
| MPE, eye, t >= 10 s | 5.0 mW/cm² | Z136.1 via the NIU manual (PR 266) |
| MPE, skin, t >= 10 s | 1.0 W/cm² | same |
| Class 1 accessible emission (MPE x 7 mm pupil) | 1.92 mW | derived |
| Focused spot (1/e² diameter), Rayleigh range | 76 µm, 3.9 mm | Gaussian, M² 1.1 |
| Peak irradiance at focus | 1.8e+07 W/cm² | same |
| NHZ, collimated 5 mm beam (head off or between collimator and head) | 10.6 km | divergence 0.30 mrad full |
| NHZ, direct beam through the f-theta, from the focus | 162 m | 19.7 mrad full angle |
| NHZ, specular off a bare Al plate (R 0.9) | 154 m | from the focus |
| NHZ, bare fibre end (collimator off) | 23 m | 140 mrad full angle (PR 266's assumption) |
| NHZ, diffuse off powder (rho 0.1) | 0.50 m | Lambertian, normal viewing |
| NHZ, diffuse off powder (rho 0.5) | 1.13 m | Lambertian, normal viewing |
| Eyewear OD, direct 400 W | >= 5.3 | OD = log10(H0/MPE), 7 mm pupil |
| Eyewear OD, specular 0.9 x 400 W | >= 5.3 | OD = log10(H0/MPE), 7 mm pupil |
| Eyewear OD, alignment at 40 W (10 %) | >= 4.3 | OD = log10(H0/MPE), 7 mm pupil |
| Eyewear OD, alignment at 4 W (1 %) | >= 3.3 | OD = log10(H0/MPE), 7 mm pupil |
| Window or viewing-panel OD for Class 1 behind it, full 400 W | >= 5.3 | derived |
| Energy on a stationary spot before the beam stops: laser gate (12 µs) and wiring, 1 ms | 0.4 J | P x t |
| Energy on a stationary spot before the beam stops: safety relay into the laser's interlock loop, 20 ms | 8.0 J | P x t |
| Energy on a stationary spot before the beam stops: a slow path, 100 ms | 40.0 J | P x t |
