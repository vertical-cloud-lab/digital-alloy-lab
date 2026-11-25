# Plume study: key numbers

Written by `analysis/monitoring/plume/summarize.py` from the JSON files in this folder.

## Vapour plume by hand (plume_jet.py)

| Alloy | Scenario | T_s (K) | p_sat (atm) | Regime | Jet speed (m/s) | Metal out (g/h of lasing) | Vapour (mol) | Plume height 10 mm downstream, 200 / 140 L/min (mm) | Primary particles (nm) |
|---|---|---|---|---|---|---|---|---|---|
| AlSi10Mg | conduction | 2000 | 0.15 | no jet | 0 | 0.000396 | Mg 96 %, Al 4 % | 0.4 / 0.6 | 27 |
| AlSi10Mg | conduction | 2300 | 0.44 | no jet | 0 | 0.0013 | Mg 86 %, Al 14 % | 0.4 / 0.6 | 67 |
| AlSi10Mg | keyhole onset | 2607 | 1.20 | jet | 113 | 0.176 | Mg 69 %, Al 30 % | 3.6 / 4.6 | 6 |
| AlSi10Mg | keyhole | 2771 | 2.00 | jet | 441 | 0.736 | Mg 59 %, Al 41 % | 9.2 / 11.8 | 3 |
| 6061 | conduction | 2000 | 0.41 | no jet | 0 | 0.0011 | Mg 98 %, Al 2 % | 0.4 / 0.6 | 62 |
| 6061 | conduction | 2234 | 0.93 | no jet | 0 | 0.00268 | Mg 96 %, Al 4 % | 0.4 / 0.6 | 111 |
| 6061 | keyhole onset | 2314 | 1.20 | jet | 108 | 0.184 | Mg 94 %, Al 6 % | 3.6 / 4.6 | 6 |
| 6061 | keyhole | 2488 | 2.00 | jet | 425 | 0.764 | Mg 90 %, Al 10 % | 9.2 / 11.8 | 3 |
| 7075 | conduction | 1623 | 0.77 | no jet | 0 | 0.00432 | Zn 77 %, Mg 23 % | 0.4 / 0.6 | 89 |
| 7075 | conduction | 1656 | 0.92 | no jet | 0 | 0.00519 | Zn 77 %, Mg 23 % | 0.4 / 0.6 | 96 |
| 7075 | keyhole onset | 1710 | 1.20 | jet | 61 | 0.323 | Zn 76 %, Mg 24 % | 3.6 / 4.6 | 8 |
| 7075 | keyhole | 1822 | 2.00 | jet | 242 | 1.34 | Zn 75 %, Mg 24 % | 9.2 / 11.8 | 5 |

Alloy boiling points (Raoult, ideal): AlSi10Mg 2549 K, 6061 2256 K, 7075 1673 K

| Beam / coaxial attenuation through the plume above the spot | column (mg/m²) | τ at 1.07 µm, 20 nm / 300 nm | τ at 0.85 µm, 20 nm / 300 nm |
|---|---|---|---|
| AlSi10Mg: conduction, T_s 2000 K | 0.055 | 3.9e-06 / 2.1e-04 | 1.5e-05 / 3.0e-04 |
| AlSi10Mg: conduction, T_s 2300 K | 0.181 | 1.3e-05 / 7.0e-04 | 4.8e-05 / 9.8e-04 |
| AlSi10Mg: keyhole onset, p_sat 1.2 atm | 20.3 | 1.4e-03 / 7.9e-02 | 5.4e-03 / 1.1e-01 |
| AlSi10Mg: keyhole, p_sat 2 atm | 40.1 | 2.8e-03 / 1.6e-01 | 1.1e-02 / 2.2e-01 |
| 6061: conduction, T_s 2000 K | 0.152 | 1.1e-05 / 5.9e-04 | 4.0e-05 / 8.2e-04 |
| 6061: conduction, T_s 2300 K | 0.372 | 2.6e-05 / 1.5e-03 | 9.9e-05 / 2.0e-03 |
| 6061: keyhole onset, p_sat 1.2 atm | 24.1 | 1.7e-03 / 9.4e-02 | 6.4e-03 / 1.3e-01 |
| 6061: keyhole, p_sat 2 atm | 45.1 | 3.2e-03 / 1.8e-01 | 1.2e-02 / 2.4e-01 |
| 7075: conduction, T_s 2000 K | 0.599 | 4.2e-05 / 2.3e-03 | 1.6e-04 / 3.2e-03 |
| 7075: conduction, T_s 2300 K | 0.721 | 5.0e-05 / 2.8e-03 | 1.9e-04 / 3.9e-03 |
| 7075: keyhole onset, p_sat 1.2 atm | 80.8 | 5.7e-03 / 3.2e-01 | 2.1e-02 / 4.4e-01 |
| 7075: keyhole, p_sat 2 atm | 194 | 1.4e-02 / 7.6e-01 | 5.2e-02 / 1.0e+00 |

## Condensate in the CFD (particles.py)

### p200: 200 + 40 L/min, LW purge 0 L/min, 285k cells, 800 iterations

Bed: 2.95 m/s mean at 3 mm over Ø75 (2.60–3.33); under the laser slide (z 121): 0.45 m/s, Uy -0.45.

| Released | n | Out in 8 s | Median time out (s) | Near the beam axis under the lid | Entered laser recess | Entered LW recess | Entered LP recess | Entered LC recess | Entered BW recess |
|---|---|---|---|---|---|---|---|---|---|
| 0.5-5 mm | 10000 | 99.5 % | 0.039 | 0.7 % | 0.04 % | 0.03 % | 0.27 % | 0.14 % | 0.02 % |
| 5-20 mm | 10000 | 95.1 % | 0.062 | 7.2 % | 0.24 % | 0.25 % | 2.59 % | 0.86 % | 0.14 % |

Condensate concentration per unit source, C/S (s/m³), next to each window and at other places:

| Control volume | 0.5-5 mm | 5-20 mm |
|---|---|---|
| LW recess | 22.4 | 473 |
| LW near face | 2.55 | 335 |
| BW recess | 146 | 375 |
| BW near face | 119 | 254 |
| LP recess | 204 | 1.78e+03 |
| LP near face | 205 | 1.81e+03 |
| LC recess | 36.4 | 367 |
| LC near face | 51.9 | 525 |
| laser recess | 0.407 | 17.3 |
| laser near face | 0 | 30.1 |
| beam column z 20-120 (r < 5 mm) | 20.6 | 243 |
| over plate z 0-20 | 126 | 234 |
| ceiling layer at lid candidate (-60, -80) | 75.4 | 685 |
| ceiling layer at lid candidate (-40, 60) | 3.13 | 27.9 |
| ceiling layer at lid candidate (-20, 80) | 1.88 | 30.3 |
| ceiling layer at lid candidate (80, 80) | 49.9 | 533 |
| left-wall layer at y -60, z 22-44 | 80.5 | 749 |
| left-wall layer at y -20, z 22-44 | 47.8 | 544 |
| left-wall layer at y 20, z 22-44 | 31.9 | 463 |
| left-wall layer at y 60, z 22-44 | 70.7 | 735 |

| Window | u* (m/s) | gas speed 1 mm off the face (m/s) |
|---|---|---|
| laser slide (lid, centre) | 0.065 | 0.097 |
| LW slide (left wall, 13°) | 0.017 | 0.015 |
| LP slide (lid, front-left, 54°) | 0.058 | 0.22 |
| layer-camera bore (lid) | 0.026 | 0.077 |
| BW light window (back wall, 8°) | 0.01 | 0.0069 |

Spatter (Al) landing on each window, share of launches:

| Speeds | d (µm) | laser slide (lid, centre) | LW slide (left wall, 13°) | LP slide (lid, front-left, 54°) | layer-camera bore (lid) | BW light window (back wall, 8°) | plate (Ø75) | floor | outlet | lid | walls and parts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.0 % | 13.9 % | 0.9 % | 65.0 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 2.9 % | 1.3 % | 0.0 % | 95.9 % |
| Ly 2017 speeds | 50 | 0.07 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.5 % | 13.5 % | 2.5 % | 0.3 % | 83.2 % |
| Ly 2017 speeds | 100 | 8.00 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 1.5 % | 21.2 % | 2.6 % | 26.5 % | 40.0 % |
| Ly 2017 speeds | 150 | 11.92 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 0.8 % | 7.2 % | 0.4 % | 35.4 % | 44.0 % |
| Ly 2017 speeds | 200 | 12.00 % | 0.08 % | 0.25 % | 0.00 % | 0.00 % | 0.0 % | 2.5 % | 0.1 % | 37.7 % | 47.4 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 19.9 % | 38.5 % | 0.0 % | 41.7 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.5 % | 2.7 % | 0.0 % | 93.9 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.0 % | 1.7 % | 0.0 % | 91.3 % |
| slow (speeds / 2) | 100 | 5.25 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.5 % | 18.6 % | 3.7 % | 15.1 % | 55.8 % |
| slow (speeds / 2) | 150 | 8.75 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 2.2 % | 17.2 % | 1.3 % | 27.1 % | 43.3 % |
| slow (speeds / 2) | 200 | 9.92 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.9 % | 14.9 % | 0.9 % | 28.2 % | 44.1 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.6 % | 58.5 % | 0.0 % | 15.9 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.7 % | 4.7 % | 0.0 % | 88.6 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.4 % | 1.5 % | 0.0 % | 95.1 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.75 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 2.5 % | 34.2 % | 4.6 % | 3.8 % | 53.1 % |
| Al lognormal (median 2.5 m/s) | 150 | 4.17 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 3.2 % | 30.9 % | 2.7 % | 12.0 % | 47.1 % |
| Al lognormal (median 2.5 m/s) | 200 | 6.83 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 3.6 % | 24.5 % | 1.4 % | 17.1 % | 46.5 % |

## Fouling (fouling.py)

Condensate source, g per hour of lasing (from measured Mg / Zn losses x 1.5 for Al): AlSi10Mg 0.035–0.095 (nominal 0.057), 6061 0.03–0.081 (nominal 0.049), 7075 0.12–1.1 (nominal 0.36)

### p200

| Window | Released | Size, ΔT | Alloy | mg/m² per h of lasing | h to the limit, dense Al film | h, porous Al (f 0.1) |
|---|---|---|---|---|---|---|
| LW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.000526 | 2.07e+03 | 1.08e+06 |
| LW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.00325 | 335 | 1.74e+05 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.000229 | 4.76e+03 | 2.48e+06 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00142 | 769 | 4.01e+05 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 7.28e-05 | 1.5e+04 | 7.8e+06 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00045 | 2.42e+03 | 1.26e+06 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.0159 | 68.5 | 3.57e+04 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.0983 | 11.1 | 5.77e+03 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0143 | 158 | 7.48e+04 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0887 | 25.5 | 1.21e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00624 | 363 | 1.72e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0386 | 58.7 | 2.78e+04 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00198 | 1.14e+03 | 5.4e+05 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.0123 | 185 | 8.73e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.735 | 3.09 | 1.46e+03 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 4.55 | 0.499 | 236 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.137 | 7.94 | 4.14e+03 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.849 | 1.28 | 669 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0512 | 21.3 | 1.11e+04 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.317 | 3.44 | 1.79e+03 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.000603 | 1.81e+03 | 9.41e+05 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00373 | 292 | 1.52e+05 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 1.31 | 0.829 | 432 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 8.13 | 0.134 | 69.8 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.015 | 72.6 | 3.78e+04 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0928 | 11.7 | 6.12e+03 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00457 | 238 | 1.24e+05 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0283 | 38.5 | 2e+04 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.000152 | 7.16e+03 | 3.73e+06 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.000941 | 1.16e+03 | 6.03e+05 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.323 | 3.37 | 1.75e+03 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 2 | 0.544 | 284 |
| LW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0691 | 15.8 | 8.21e+03 |
| LW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.427 | 2.55 | 1.33e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0301 | 36.2 | 1.89e+04 |
| LW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.186 | 5.86 | 3.05e+03 |
| LW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00956 | 114 | 5.93e+04 |
| LW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0592 | 18.4 | 9.59e+03 |
| LW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 2.09 | 0.522 | 272 |
| LW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 12.9 | 0.0843 | 43.9 |
| BW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0308 | 73.6 | 3.48e+04 |
| BW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.191 | 11.9 | 5.63e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0134 | 169 | 8e+04 |
| BW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.0829 | 27.3 | 1.29e+04 |
| BW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00426 | 532 | 2.52e+05 |
| BW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0264 | 86 | 4.07e+04 |
| BW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 1.58 | 1.44 | 680 |
| BW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 9.76 | 0.232 | 110 |
| LP | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 1.21 | 0.9 | 469 |
| LP | 5-20 mm | 0.05 um, dT 0 K | 7075 | 7.48 | 0.146 | 75.8 |
| LP | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.451 | 2.41 | 1.26e+03 |
| LP | 5-20 mm | 0.1 um, dT 0 K | 7075 | 2.79 | 0.39 | 203 |
| LP | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00532 | 205 | 1.07e+05 |
| LP | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0329 | 33.1 | 1.72e+04 |
| LP | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 11.6 | 0.094 | 48.9 |
| LP | 5-20 mm | 0.1 um, dT 10 K | 7075 | 71.7 | 0.0152 | 7.91 |
| LC | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.152 | 7.17 | 3.74e+03 |
| LC | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.94 | 1.16 | 604 |
| LC | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0463 | 23.5 | 1.22e+04 |
| LC | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.287 | 3.8 | 1.98e+03 |
| LC | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00154 | 707 | 3.68e+05 |
| LC | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.00954 | 114 | 5.95e+04 |
| LC | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 3.28 | 0.333 | 173 |
| LC | 5-20 mm | 0.1 um, dT 10 K | 7075 | 20.3 | 0.0537 | 28 |
| laser | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0227 | 0.322 | 323 |
| laser | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.141 | 0.052 | 52.2 |
| laser | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00864 | 0.847 | 850 |
| laser | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.0534 | 0.137 | 137 |
| laser | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.000116 | 63.3 | 6.36e+04 |
| laser | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.000715 | 10.2 | 1.03e+04 |
| laser | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.194 | 0.0378 | 37.9 |
| laser | 5-20 mm | 0.1 um, dT 10 K | 7075 | 1.2 | 0.00611 | 6.13 |

| Window, speeds | Spatter hits per hour of lasing at 100 spatters/s | splat area (mm²/h) |
|---|---|---|
| LW | Ly 2017 speeds | 3 | 0.7 |
| BW | Ly 2017 speeds | 0 | 0.0 |
| LP | Ly 2017 speeds | 93 | 8.9 |
| LC | Ly 2017 speeds | 0 | 0.0 |
| laser | Ly 2017 speeds | 5076 | 503.7 |
| LW | slow (speeds / 2) | 0 | 0.0 |
| BW | slow (speeds / 2) | 0 | 0.0 |
| LP | slow (speeds / 2) | 57 | 5.7 |
| LC | slow (speeds / 2) | 0 | 0.0 |
| laser | slow (speeds / 2) | 3507 | 365.5 |
| LW | Al lognormal (median 2.5 m/s) | 33 | 2.5 |
| BW | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LP | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LC | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| laser | Al lognormal (median 2.5 m/s) | 1476 | 176.0 |

## Spatter glow and blur (spatter.py)

| Spatter | Camera, exposure | visible above (K) | glows for (ms) | over (mm) |
|---|---|---|---|---|
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1582 | 2.1 | 8 |
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1516 | 2.4 | 9 |
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1181 | 4.5 | 14 |
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1143 | 4.8 | 15 |
| Al, 35 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 10 us | 1880 | 0.9 | 4 |
| Al, 35 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1788 | 1.3 | 5 |
| Al, 35 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1822 | 1.1 | 5 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1554 | 4.3 | 16 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1473 | 5.0 | 18 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1165 | 8.9 | 27 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1118 | 9.7 | 28 |
| Al, 50 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 10 us | 1841 | 2.1 | 9 |
| Al, 50 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1728 | 2.8 | 12 |
| Al, 50 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1775 | 2.5 | 10 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1514 | 16.5 | 60 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1399 | 20.7 | 70 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1142 | 33.5 | 94 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1073 | 37.9 | 100 |
| Al, 100 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 10 us | 1785 | 8.5 | 36 |
| Al, 100 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1628 | 12.8 | 50 |
| Al, 100 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1689 | 11.0 | 44 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1489 | 59.7 | 203 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1339 | 80.8 | 247 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1128 | 120.6 | 308 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1037 | 143.1 | 334 |
| Al, 200 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 10 us | 1751 | 31.8 | 127 |
| Al, 200 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1547 | 52.7 | 186 |
| Al, 200 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1610 | 45.6 | 168 |

