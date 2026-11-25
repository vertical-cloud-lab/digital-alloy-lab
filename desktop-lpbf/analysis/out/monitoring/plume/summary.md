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

| Released | n | Out in 8 s | Out by the end (t_end) | Median time out (s) | Near the beam axis under the lid | Entered laser recess | Entered LW recess | Entered LP recess | Entered LC recess | Entered BW recess |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5-5 mm | 30000 | 99.5 % | 100.0 % (20 s) | 0.039 | 0.7 % | 0.03 % | 0.01 % | 0.32 % | 0.08 % | 0.02 % |
| 5-20 mm | 30000 | 94.8 % | 99.8 % (20 s) | 0.068 | 7.4 % | 0.28 % | 0.21 % | 2.75 % | 0.86 % | 0.16 % |

Condensate concentration per unit source, C/S (s/m³), next to each window and at other places (in brackets: how many tracers visited; the counting noise is ~1/sqrt of it):

| Control volume | 0.5-5 mm | 5-20 mm |
|---|---|---|
| LW recess | 4.98 (2) | 457 (63) |
| LW near face | 0 (0) | 433 (23) |
| BW recess | 99.3 (6) | 659 (48) |
| BW near face | 74.1 (2) | 510 (15) |
| LP recess | 208 (96) | 2.19e+03 (824) |
| LP near face | 228 (46) | 1.86e+03 (434) |
| LC recess | 23.5 (23) | 322 (259) |
| LC near face | 43.5 (6) | 444 (74) |
| laser recess | 2.33 (9) | 39.5 (84) |
| laser near face | 2.65 (1) | 107 (15) |
| beam column z 20-120 (r < 5 mm) | 22.2 (219) | 274 (3381) |
| over plate z 0-20 | 128 (30000) | 244 (29937) |
| ceiling layer at lid candidate (-60, -80) | 84 (210) | 736 (1896) |
| ceiling layer at lid candidate (-40, 60) | 4.67 (34) | 38 (248) |
| ceiling layer at lid candidate (-20, 80) | 3.83 (24) | 29.3 (195) |
| ceiling layer at lid candidate (80, 80) | 37 (42) | 513 (572) |
| left-wall layer at y -60, z 22-44 | 113 (26) | 910 (329) |
| left-wall layer at y -20, z 22-44 | 46.5 (28) | 612 (319) |
| left-wall layer at y 20, z 22-44 | 42.1 (29) | 420 (223) |
| left-wall layer at y 60, z 22-44 | 66.6 (22) | 547 (167) |

| Window | u* (m/s) | gas speed 1 mm off the face (m/s) |
|---|---|---|
| laser slide (lid, centre) | 0.065 | 0.097 |
| LW slide (left wall, 13°) | 0.017 | 0.015 |
| LP slide (lid, front-left, 54°) | 0.058 | 0.22 |
| layer-camera bore (lid) | 0.026 | 0.077 |
| BW light window (back wall, 8°) | 0.01 | 0.0069 |

Spatter (Al) landing on each window, share of launches:

| Speeds | d (µm) | laser slide (lid, centre) | LW slide (left wall, 13°) | LP slide (lid, front-left, 54°) | layer-camera bore (lid) | BW light window (back wall, 8°) | plate (Ø75) | floor | outlet | lid | door side | other walls and parts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.0 % | 13.9 % | 0.9 % | 58.4 % | 6.6 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 2.9 % | 1.3 % | 0.0 % | 95.2 % | 0.7 % |
| Ly 2017 speeds | 50 | 0.07 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.5 % | 13.5 % | 2.5 % | 0.3 % | 75.9 % | 7.3 % |
| Ly 2017 speeds | 100 | 5.33 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 1.5 % | 21.2 % | 2.6 % | 26.5 % | 17.8 % | 24.8 % |
| Ly 2017 speeds | 150 | 6.75 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 0.8 % | 7.2 % | 0.4 % | 35.4 % | 15.2 % | 33.9 % |
| Ly 2017 speeds | 200 | 7.75 % | 0.08 % | 0.25 % | 0.00 % | 0.00 % | 0.0 % | 2.5 % | 0.1 % | 37.7 % | 14.0 % | 37.7 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 19.9 % | 38.5 % | 0.0 % | 41.7 % | 0.0 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.5 % | 2.7 % | 0.0 % | 93.7 % | 0.1 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.0 % | 1.7 % | 0.0 % | 91.1 % | 0.2 % |
| slow (speeds / 2) | 100 | 4.08 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.5 % | 18.6 % | 3.7 % | 15.1 % | 38.8 % | 18.2 % |
| slow (speeds / 2) | 150 | 5.17 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 2.2 % | 17.2 % | 1.3 % | 27.1 % | 22.3 % | 24.6 % |
| slow (speeds / 2) | 200 | 6.33 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.9 % | 14.9 % | 0.9 % | 28.2 % | 17.3 % | 30.3 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.6 % | 58.5 % | 0.0 % | 15.9 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.7 % | 4.7 % | 0.0 % | 88.5 % | 0.1 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.4 % | 1.5 % | 0.0 % | 95.0 % | 0.1 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.50 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 2.5 % | 34.2 % | 4.6 % | 3.8 % | 45.3 % | 8.0 % |
| Al lognormal (median 2.5 m/s) | 150 | 3.08 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 3.2 % | 30.9 % | 2.7 % | 12.0 % | 28.4 % | 19.8 % |
| Al lognormal (median 2.5 m/s) | 200 | 4.83 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 3.6 % | 24.5 % | 1.4 % | 17.1 % | 21.1 % | 27.4 % |

### p200_lw3: 200 + 40 L/min, LW purge 3 L/min, 285k cells, 400 iterations

Bed: 2.95 m/s mean at 3 mm over Ø75 (2.60–3.33); under the laser slide (z 121): 0.36 m/s, Uy -0.35.

| Released | n | Out in 8 s | Out by the end (t_end) | Median time out (s) | Near the beam axis under the lid | Entered laser recess | Entered LW recess | Entered LP recess | Entered LC recess | Entered BW recess |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5-5 mm | 30000 | 99.5 % | 100.0 % (20 s) | 0.039 | 0.6 % | 0.03 % | 0.05 % | 0.22 % | 0.09 % | 0.01 % |
| 5-20 mm | 30000 | 94.9 % | 99.8 % (20 s) | 0.065 | 6.4 % | 0.22 % | 0.54 % | 2.43 % | 0.89 % | 0.11 % |

Condensate concentration per unit source, C/S (s/m³), next to each window and at other places (in brackets: how many tracers visited; the counting noise is ~1/sqrt of it):

| Control volume | 0.5-5 mm | 5-20 mm |
|---|---|---|
| LW recess | 12.8 (16) | 122 (162) |
| LW near face | 1.09 (6) | 9.27 (43) |
| BW recess | 58.2 (2) | 528 (34) |
| BW near face | 16.9 (1) | 396 (14) |
| LP recess | 159 (67) | 2.16e+03 (730) |
| LP near face | 174 (38) | 1.9e+03 (398) |
| LC recess | 32.7 (26) | 385 (268) |
| LC near face | 56.1 (11) | 519 (121) |
| laser recess | 29.5 (8) | 27 (66) |
| laser near face | 102 (4) | 45 (9) |
| beam column z 20-120 (r < 5 mm) | 18.1 (180) | 272 (3368) |
| over plate z 0-20 | 126 (30000) | 231 (29939) |
| ceiling layer at lid candidate (-60, -80) | 54.7 (155) | 603 (1599) |
| ceiling layer at lid candidate (-40, 60) | 1.32 (10) | 20.1 (153) |
| ceiling layer at lid candidate (-20, 80) | 1.28 (9) | 16.5 (117) |
| ceiling layer at lid candidate (80, 80) | 35.5 (37) | 466 (513) |
| left-wall layer at y -60, z 22-44 | 62.9 (29) | 503 (260) |
| left-wall layer at y -20, z 22-44 | 24.5 (31) | 258 (290) |
| left-wall layer at y 20, z 22-44 | 74.1 (33) | 1.1e+03 (284) |
| left-wall layer at y 60, z 22-44 | 52.1 (18) | 1.15e+03 (285) |

| Window | u* (m/s) | gas speed 1 mm off the face (m/s) |
|---|---|---|
| laser slide (lid, centre) | 0.066 | 0.1 |
| LW slide (left wall, 13°) | 0.14 | 0.82 |
| LP slide (lid, front-left, 54°) | 0.059 | 0.23 |
| layer-camera bore (lid) | 0.032 | 0.11 |
| BW light window (back wall, 8°) | 0.0088 | 0.0053 |

Spatter (Al) landing on each window, share of launches:

| Speeds | d (µm) | laser slide (lid, centre) | LW slide (left wall, 13°) | LP slide (lid, front-left, 54°) | layer-camera bore (lid) | BW light window (back wall, 8°) | plate (Ø75) | floor | outlet | lid | door side | other walls and parts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 19.7 % | 14.5 % | 0.1 % | 61.8 % | 2.9 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.3 % | 2.0 % | 0.0 % | 94.3 % | 0.4 % |
| Ly 2017 speeds | 50 | 0.07 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.5 % | 13.6 % | 2.2 % | 0.3 % | 76.1 % | 7.3 % |
| Ly 2017 speeds | 100 | 5.33 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 1.3 % | 22.0 % | 1.9 % | 26.2 % | 17.8 % | 25.2 % |
| Ly 2017 speeds | 150 | 6.92 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 0.8 % | 7.2 % | 0.4 % | 35.5 % | 15.5 % | 33.5 % |
| Ly 2017 speeds | 200 | 7.75 % | 0.08 % | 0.33 % | 0.00 % | 0.00 % | 0.0 % | 2.3 % | 0.1 % | 37.8 % | 14.2 % | 37.5 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.8 % | 39.0 % | 0.0 % | 40.2 % | 0.0 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 4.6 % | 2.8 % | 0.0 % | 92.5 % | 0.1 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.1 % | 1.9 % | 0.0 % | 91.7 % | 0.3 % |
| slow (speeds / 2) | 100 | 4.00 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.8 % | 18.8 % | 3.5 % | 14.9 % | 38.2 % | 18.6 % |
| slow (speeds / 2) | 150 | 5.33 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 2.1 % | 17.0 % | 1.2 % | 27.3 % | 22.5 % | 24.3 % |
| slow (speeds / 2) | 200 | 6.17 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.7 % | 15.7 % | 0.8 % | 27.9 % | 17.5 % | 30.2 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.5 % | 59.7 % | 0.0 % | 14.7 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.1 % | 4.7 % | 0.0 % | 88.1 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.8 % | 1.5 % | 0.0 % | 94.7 % | 0.1 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.50 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 2.3 % | 34.8 % | 4.3 % | 3.8 % | 44.8 % | 8.3 % |
| Al lognormal (median 2.5 m/s) | 150 | 3.17 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 2.9 % | 31.8 % | 2.8 % | 12.2 % | 27.9 % | 19.1 % |
| Al lognormal (median 2.5 m/s) | 200 | 4.83 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 3.6 % | 24.3 % | 1.2 % | 17.3 % | 21.0 % | 27.6 % |

### p140: 140 + 30 L/min, LW purge 0 L/min, 285k cells, 300 iterations

Bed: 2.03 m/s mean at 3 mm over Ø75 (1.77–2.31); under the laser slide (z 121): 0.31 m/s, Uy -0.31.

| Released | n | Out in 8 s | Out by the end (t_end) | Median time out (s) | Near the beam axis under the lid | Entered laser recess | Entered LW recess | Entered LP recess | Entered LC recess | Entered BW recess |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5-5 mm | 30000 | 99.3 % | 100.0 % (20 s) | 0.056 | 0.6 % | 0.02 % | 0.01 % | 0.09 % | 0.09 % | 0.01 % |
| 5-20 mm | 30000 | 91.5 % | 99.2 % (20 s) | 0.087 | 7.8 % | 0.28 % | 0.09 % | 1.10 % | 1.22 % | 0.06 % |

Condensate concentration per unit source, C/S (s/m³), next to each window and at other places (in brackets: how many tracers visited; the counting noise is ~1/sqrt of it):

| Control volume | 0.5-5 mm | 5-20 mm |
|---|---|---|
| LW recess | 20.6 (3) | 273 (26) |
| LW near face | 4.35 (2) | 208 (8) |
| BW recess | 25.3 (2) | 570 (17) |
| BW near face | 19 (1) | 224 (7) |
| LP recess | 107 (26) | 1.1e+03 (330) |
| LP near face | 67 (13) | 851 (138) |
| LC recess | 61.8 (26) | 941 (366) |
| LC near face | 84.8 (12) | 1.28e+03 (147) |
| laser recess | 0.989 (6) | 28.5 (83) |
| laser near face | 1.09 (2) | 31.4 (7) |
| beam column z 20-120 (r < 5 mm) | 20.5 (141) | 351 (3050) |
| over plate z 0-20 | 188 (30000) | 327 (29965) |
| ceiling layer at lid candidate (-60, -80) | 36.3 (53) | 408 (554) |
| ceiling layer at lid candidate (-40, 60) | 2.89 (15) | 27.7 (146) |
| ceiling layer at lid candidate (-20, 80) | 2.43 (10) | 31.1 (161) |
| ceiling layer at lid candidate (80, 80) | 36.9 (36) | 568 (531) |
| left-wall layer at y -60, z 22-44 | 3.66 (5) | 496 (35) |
| left-wall layer at y -20, z 22-44 | 40.6 (12) | 301 (128) |
| left-wall layer at y 20, z 22-44 | 24.2 (5) | 761 (115) |
| left-wall layer at y 60, z 22-44 | 87.9 (18) | 846 (167) |

| Window | u* (m/s) | gas speed 1 mm off the face (m/s) |
|---|---|---|
| laser slide (lid, centre) | 0.051 | 0.062 |
| LW slide (left wall, 13°) | 0.01 | 0.0054 |
| LP slide (lid, front-left, 54°) | 0.031 | 0.067 |
| layer-camera bore (lid) | 0.021 | 0.054 |
| BW light window (back wall, 8°) | 0.0066 | 0.003 |

Spatter (Al) landing on each window, share of launches:

| Speeds | d (µm) | laser slide (lid, centre) | LW slide (left wall, 13°) | LP slide (lid, front-left, 54°) | layer-camera bore (lid) | BW light window (back wall, 8°) | plate (Ø75) | floor | outlet | lid | door side | other walls and parts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.1 % | 29.2 % | 0.1 % | 46.1 % | 3.1 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.3 % | 1.6 % | 0.0 % | 94.2 % | 0.9 % |
| Ly 2017 speeds | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.4 % | 14.1 % | 3.9 % | 0.4 % | 73.7 % | 7.6 % |
| Ly 2017 speeds | 100 | 5.50 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 3.8 % | 22.2 % | 0.8 % | 26.1 % | 15.2 % | 26.1 % |
| Ly 2017 speeds | 150 | 7.25 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 0.9 % | 7.2 % | 0.3 % | 36.4 % | 14.6 % | 33.1 % |
| Ly 2017 speeds | 200 | 7.58 % | 0.00 % | 0.42 % | 0.00 % | 0.00 % | 0.2 % | 1.9 % | 0.2 % | 38.0 % | 13.8 % | 37.9 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 26.2 % | 50.6 % | 0.0 % | 23.2 % | 0.0 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 8.2 % | 5.9 % | 0.0 % | 85.9 % | 0.1 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.1 % | 8.1 % | 3.2 % | 0.0 % | 88.5 % | 0.1 % |
| slow (speeds / 2) | 100 | 4.17 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 3.2 % | 32.7 % | 4.4 % | 14.8 % | 21.9 % | 18.8 % |
| slow (speeds / 2) | 150 | 5.08 % | 0.00 % | 0.33 % | 0.00 % | 0.00 % | 5.6 % | 19.0 % | 1.0 % | 27.1 % | 16.2 % | 25.7 % |
| slow (speeds / 2) | 200 | 6.00 % | 0.08 % | 0.08 % | 0.00 % | 0.00 % | 3.3 % | 14.8 % | 0.5 % | 28.2 % | 14.8 % | 32.2 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.3 % | 24.4 % | 70.2 % | 0.0 % | 5.1 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.2 % | 12.9 % | 9.3 % | 0.0 % | 77.5 % | 0.1 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.3 % | 3.4 % | 0.0 % | 90.3 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.33 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 7.7 % | 49.0 % | 3.9 % | 3.8 % | 25.0 % | 9.2 % |
| Al lognormal (median 2.5 m/s) | 150 | 2.67 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 8.4 % | 34.8 % | 1.7 % | 13.2 % | 18.2 % | 21.2 % |
| Al lognormal (median 2.5 m/s) | 200 | 5.08 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 6.2 % | 24.7 % | 0.6 % | 18.2 % | 16.2 % | 29.0 % |

### p200_lw1: 200 + 40 L/min, LW purge 1 L/min, 285k cells, 200 iterations

Bed: 2.94 m/s mean at 3 mm over Ø75 (2.60–3.32); under the laser slide (z 121): 0.47 m/s, Uy -0.47.

| Released | n | Out in 8 s | Out by the end (t_end) | Median time out (s) | Near the beam axis under the lid | Entered laser recess | Entered LW recess | Entered LP recess | Entered LC recess | Entered BW recess |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5-5 mm | 30000 | 99.4 % | 100.0 % (20 s) | 0.039 | 0.7 % | 0.04 % | 0.10 % | 0.26 % | 0.04 % | 0.03 % |
| 5-20 mm | 30000 | 94.5 % | 99.8 % (20 s) | 0.067 | 7.2 % | 0.25 % | 0.71 % | 2.45 % | 0.43 % | 0.14 % |

Condensate concentration per unit source, C/S (s/m³), next to each window and at other places (in brackets: how many tracers visited; the counting noise is ~1/sqrt of it):

| Control volume | 0.5-5 mm | 5-20 mm |
|---|---|---|
| LW recess | 33.4 (31) | 229 (212) |
| LW near face | 4.11 (13) | 33.2 (43) |
| BW recess | 138 (9) | 1.33e+03 (41) |
| BW near face | 78.4 (3) | 991 (22) |
| LP recess | 156 (77) | 1.64e+03 (735) |
| LP near face | 188 (38) | 1.4e+03 (376) |
| LC recess | 20.7 (13) | 261 (130) |
| LC near face | 15.5 (6) | 387 (51) |
| laser recess | 12.6 (12) | 32.2 (74) |
| laser near face | 30.5 (2) | 91.2 (12) |
| beam column z 20-120 (r < 5 mm) | 21.9 (195) | 255 (3126) |
| over plate z 0-20 | 127 (30000) | 237 (29921) |
| ceiling layer at lid candidate (-60, -80) | 61 (158) | 656 (1723) |
| ceiling layer at lid candidate (-40, 60) | 2.58 (20) | 24.1 (193) |
| ceiling layer at lid candidate (-20, 80) | 1.81 (12) | 17.8 (128) |
| ceiling layer at lid candidate (80, 80) | 33.7 (50) | 400 (570) |
| left-wall layer at y -60, z 22-44 | 96.8 (26) | 766 (296) |
| left-wall layer at y -20, z 22-44 | 34.1 (31) | 331 (271) |
| left-wall layer at y 20, z 22-44 | 23.6 (16) | 311 (145) |
| left-wall layer at y 60, z 22-44 | 25.8 (16) | 411 (185) |

| Window | u* (m/s) | gas speed 1 mm off the face (m/s) |
|---|---|---|
| laser slide (lid, centre) | 0.067 | 0.1 |
| LW slide (left wall, 13°) | 0.06 | 0.22 |
| LP slide (lid, front-left, 54°) | 0.061 | 0.24 |
| layer-camera bore (lid) | 0.028 | 0.086 |
| BW light window (back wall, 8°) | 0.011 | 0.0076 |

Spatter (Al) landing on each window, share of launches:

| Speeds | d (µm) | laser slide (lid, centre) | LW slide (left wall, 13°) | LP slide (lid, front-left, 54°) | layer-camera bore (lid) | BW light window (back wall, 8°) | plate (Ø75) | floor | outlet | lid | door side | other walls and parts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.13 % | 0.00 % | 0.00 % | 0.0 % | 20.4 % | 14.9 % | 0.6 % | 60.8 % | 2.3 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 2.9 % | 1.8 % | 0.0 % | 94.1 % | 1.1 % |
| Ly 2017 speeds | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.5 % | 13.7 % | 2.2 % | 0.3 % | 75.7 % | 7.6 % |
| Ly 2017 speeds | 100 | 5.58 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 1.4 % | 20.9 % | 2.5 % | 26.2 % | 18.3 % | 24.9 % |
| Ly 2017 speeds | 150 | 6.75 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 0.7 % | 7.5 % | 0.6 % | 35.5 % | 15.2 % | 33.7 % |
| Ly 2017 speeds | 200 | 7.75 % | 0.08 % | 0.25 % | 0.00 % | 0.00 % | 0.2 % | 2.2 % | 0.1 % | 37.8 % | 14.1 % | 37.6 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.6 % | 38.7 % | 0.0 % | 40.7 % | 0.0 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.9 % | 2.2 % | 0.0 % | 93.7 % | 0.1 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.9 % | 1.7 % | 0.0 % | 89.9 % | 0.4 % |
| slow (speeds / 2) | 100 | 4.08 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.5 % | 19.7 % | 3.2 % | 15.0 % | 38.6 % | 17.9 % |
| slow (speeds / 2) | 150 | 5.08 % | 0.00 % | 0.17 % | 0.00 % | 0.00 % | 2.3 % | 17.2 % | 1.2 % | 27.1 % | 22.5 % | 24.5 % |
| slow (speeds / 2) | 200 | 6.17 % | 0.00 % | 0.08 % | 0.00 % | 0.00 % | 1.8 % | 15.2 % | 0.8 % | 28.2 % | 17.3 % | 30.6 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.4 % | 59.4 % | 0.0 % | 15.2 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.1 % | 4.6 % | 0.0 % | 88.3 % | 0.0 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.7 % | 1.4 % | 0.0 % | 94.7 % | 0.1 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.42 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 2.2 % | 33.7 % | 5.3 % | 3.8 % | 45.7 % | 7.8 % |
| Al lognormal (median 2.5 m/s) | 150 | 3.08 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 2.8 % | 32.0 % | 2.6 % | 12.0 % | 28.3 % | 19.2 % |
| Al lognormal (median 2.5 m/s) | 200 | 4.92 % | 0.08 % | 0.00 % | 0.00 % | 0.00 % | 3.5 % | 24.7 % | 1.2 % | 17.2 % | 21.2 % | 27.3 % |

## Fouling (fouling.py)

Condensate source, g per hour of lasing (file: analysis/out/monitoring/melt/plume_source.json): AlSi10Mg 0.097–0.64 (nominal 0.47; worker A 'best': measured Mg/Zn rates + 'wall' reading for Al (plume_source.json)), 6061 0.074–0.24 (nominal 0.19; worker A 'best': measured Mg/Zn rates + 'wall' reading for Al (plume_source.json)), 7075 0.24–0.6 (nominal 0.44; worker A 'best': measured Mg/Zn rates + 'wall' reading for Al (plume_source.json))

### p200

| Window | Released | Size, ΔT | Alloy | mg/m² per h of lasing | h to the limit, dense Al film | h, porous Al (f 0.1) |
|---|---|---|---|---|---|---|
| BW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0733 | 30.9 | 1.46e+04 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0684 | 33.1 | 1.57e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0319 | 71.1 | 3.36e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0298 | 76.1 | 3.6e+04 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0101 | 224 | 1.06e+05 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00947 | 239 | 1.13e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 3.75 | 0.604 | 286 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 3.51 | 0.647 | 306 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 1.24 | 0.877 | 457 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 1.16 | 0.939 | 489 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.464 | 2.35 | 1.22e+03 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.433 | 2.52 | 1.31e+03 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00546 | 199 | 1.04e+05 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.0051 | 214 | 1.11e+05 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 11.9 | 0.0915 | 47.7 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 11.1 | 0.098 | 51 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.103 | 10.6 | 5.52e+03 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.096 | 11.3 | 5.91e+03 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0314 | 34.7 | 1.81e+04 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0293 | 37.2 | 1.94e+04 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00104 | 1.04e+03 | 5.44e+05 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.000975 | 1.12e+03 | 5.82e+05 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 2.22 | 0.491 | 256 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 2.07 | 0.526 | 274 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0163 | 0.448 | 450 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0152 | 0.48 | 482 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0062 | 1.18 | 1.18e+03 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00579 | 1.26 | 1.27e+03 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 8.29e-05 | 88.2 | 8.86e+04 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 7.75e-05 | 94.4 | 9.48e+04 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.139 | 0.0526 | 52.8 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.13 | 0.0563 | 56.6 |
| LW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.73 | 1.49 | 778 |
| LW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.681 | 1.6 | 833 |
| LW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.317 | 3.43 | 1.79e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.297 | 3.67 | 1.91e+03 |
| LW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.101 | 10.8 | 5.62e+03 |
| LW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0943 | 11.6 | 6.02e+03 |
| LW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 22 | 0.0494 | 25.7 |
| LW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 20.6 | 0.0529 | 27.6 |
| BW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.504 | 4.5 | 2.13e+03 |
| BW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.47 | 4.82 | 2.28e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.219 | 10.3 | 4.89e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.205 | 11.1 | 5.24e+03 |
| BW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0697 | 32.5 | 1.54e+04 |
| BW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0651 | 34.8 | 1.65e+04 |
| BW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 25.8 | 0.0879 | 41.6 |
| BW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 24.1 | 0.0941 | 44.5 |
| LP | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 10.2 | 0.107 | 55.8 |
| LP | 5-20 mm | 0.05 um, dT 0 K | 7075 | 9.49 | 0.115 | 59.8 |
| LP | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 3.79 | 0.287 | 150 |
| LP | 5-20 mm | 0.1 um, dT 0 K | 7075 | 3.54 | 0.308 | 160 |
| LP | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0447 | 24.4 | 1.27e+04 |
| LP | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0417 | 26.1 | 1.36e+04 |
| LP | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 97.4 | 0.0112 | 5.83 |
| LP | 5-20 mm | 0.1 um, dT 10 K | 7075 | 90.9 | 0.012 | 6.24 |
| LC | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 1.05 | 1.04 | 542 |
| LC | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.978 | 1.11 | 580 |
| LC | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.32 | 3.41 | 1.78e+03 |
| LC | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.299 | 3.65 | 1.9e+03 |
| LC | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0106 | 102 | 5.34e+04 |
| LC | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.00993 | 110 | 5.71e+04 |
| LC | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 22.6 | 0.0482 | 25.1 |
| LC | 5-20 mm | 0.1 um, dT 10 K | 7075 | 21.1 | 0.0516 | 26.9 |
| laser | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.66 | 0.0111 | 11.1 |
| laser | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.616 | 0.0119 | 11.9 |
| laser | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.251 | 0.0292 | 29.3 |
| laser | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.234 | 0.0312 | 31.4 |
| laser | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00335 | 2.18 | 2.19e+03 |
| laser | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.00313 | 2.34 | 2.34e+03 |
| laser | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 5.62 | 0.0013 | 1.31 |
| laser | 5-20 mm | 0.1 um, dT 10 K | 7075 | 5.25 | 0.00139 | 1.4 |

| Window, speeds | Spatter hits per hour of lasing at 100 spatters/s | splat area (mm²/h) |
|---|---|---|
| LW | Ly 2017 speeds | 3 | 0.7 |
| BW | Ly 2017 speeds | 0 | 0.0 |
| LP | Ly 2017 speeds | 93 | 8.9 |
| LC | Ly 2017 speeds | 0 | 0.0 |
| laser | Ly 2017 speeds | 3219 | 310.9 |
| LW | slow (speeds / 2) | 0 | 0.0 |
| BW | slow (speeds / 2) | 0 | 0.0 |
| LP | slow (speeds / 2) | 57 | 5.7 |
| LC | slow (speeds / 2) | 0 | 0.0 |
| laser | slow (speeds / 2) | 2442 | 240.9 |
| LW | Al lognormal (median 2.5 m/s) | 33 | 2.5 |
| BW | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LP | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LC | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| laser | Al lognormal (median 2.5 m/s) | 1158 | 132.7 |

### p200_lw3

| Window | Released | Size, ΔT | Alloy | mg/m² per h of lasing | h to the limit, dense Al film | h, porous Al (f 0.1) |
|---|---|---|---|---|---|---|
| LW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0144 | 75.6 | 3.94e+04 |
| LW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0135 | 80.9 | 4.21e+04 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00628 | 174 | 9.04e+04 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00586 | 186 | 9.68e+04 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.002 | 544 | 2.83e+05 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00187 | 582 | 3.03e+05 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.0608 | 17.9 | 9.33e+03 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.0568 | 19.2 | 9.98e+03 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0145 | 156 | 7.37e+04 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0136 | 167 | 7.89e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00633 | 358 | 1.69e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00591 | 383 | 1.81e+05 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00201 | 1.13e+03 | 5.33e+05 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00188 | 1.21e+03 | 5.71e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.857 | 2.65 | 1.25e+03 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.8 | 2.83 | 1.34e+03 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.967 | 1.13 | 587 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.903 | 1.21 | 628 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.362 | 3.01 | 1.57e+03 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.338 | 3.22 | 1.68e+03 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00416 | 262 | 1.36e+05 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00389 | 280 | 1.46e+05 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 9.08 | 0.12 | 62.5 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 8.48 | 0.128 | 66.9 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.165 | 6.61 | 3.44e+03 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.154 | 7.08 | 3.69e+03 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0539 | 20.2 | 1.05e+04 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0503 | 21.6 | 1.13e+04 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00135 | 810 | 4.22e+05 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00126 | 867 | 4.52e+05 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 2.87 | 0.379 | 198 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 2.68 | 0.406 | 212 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.642 | 0.0114 | 11.4 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.599 | 0.0122 | 12.3 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.244 | 0.0299 | 30 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.228 | 0.032 | 32.2 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00352 | 2.08 | 2.08e+03 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00329 | 2.22 | 2.23e+03 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 5.36 | 0.00136 | 1.37 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 5.01 | 0.00146 | 1.47 |
| LW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.123 | 8.86 | 4.61e+03 |
| LW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.115 | 9.48 | 4.94e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0535 | 20.3 | 1.06e+04 |
| LW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.05 | 21.8 | 1.13e+04 |
| LW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0171 | 63.7 | 3.32e+04 |
| LW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.016 | 68.2 | 3.55e+04 |
| LW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.519 | 2.1 | 1.09e+03 |
| LW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 0.485 | 2.25 | 1.17e+03 |
| BW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.34 | 6.67 | 3.15e+03 |
| BW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.318 | 7.14 | 3.38e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.148 | 15.3 | 7.25e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.138 | 16.4 | 7.76e+03 |
| BW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.047 | 48.2 | 2.28e+04 |
| BW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0439 | 51.6 | 2.44e+04 |
| BW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 20 | 0.113 | 53.6 |
| BW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 18.7 | 0.121 | 57.4 |
| LP | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 10.6 | 0.103 | 53.6 |
| LP | 5-20 mm | 0.05 um, dT 0 K | 7075 | 9.89 | 0.11 | 57.4 |
| LP | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 3.96 | 0.275 | 143 |
| LP | 5-20 mm | 0.1 um, dT 0 K | 7075 | 3.7 | 0.294 | 153 |
| LP | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0455 | 23.9 | 1.25e+04 |
| LP | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0425 | 25.6 | 1.33e+04 |
| LP | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 99.4 | 0.011 | 5.71 |
| LP | 5-20 mm | 0.1 um, dT 10 K | 7075 | 92.8 | 0.0117 | 6.11 |
| LC | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 1.52 | 0.715 | 373 |
| LC | 5-20 mm | 0.05 um, dT 0 K | 7075 | 1.42 | 0.766 | 399 |
| LC | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.498 | 2.19 | 1.14e+03 |
| LC | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.465 | 2.34 | 1.22e+03 |
| LC | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0124 | 87.6 | 4.56e+04 |
| LC | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0116 | 93.8 | 4.89e+04 |
| LC | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 26.5 | 0.041 | 21.4 |
| LC | 5-20 mm | 0.1 um, dT 10 K | 7075 | 24.8 | 0.0439 | 22.9 |
| laser | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.283 | 0.0258 | 25.9 |
| laser | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.264 | 0.0277 | 27.8 |
| laser | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.108 | 0.0678 | 68.1 |
| laser | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.101 | 0.0726 | 72.9 |
| laser | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00155 | 4.71 | 4.73e+03 |
| laser | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.00145 | 5.04 | 5.06e+03 |
| laser | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 2.37 | 0.00309 | 3.11 |
| laser | 5-20 mm | 0.1 um, dT 10 K | 7075 | 2.21 | 0.00331 | 3.32 |

| Window, speeds | Spatter hits per hour of lasing at 100 spatters/s | splat area (mm²/h) |
|---|---|---|
| LW | Ly 2017 speeds | 3 | 0.7 |
| BW | Ly 2017 speeds | 0 | 0.0 |
| LP | Ly 2017 speeds | 96 | 9.6 |
| LC | Ly 2017 speeds | 0 | 0.0 |
| laser | Ly 2017 speeds | 3243 | 314.1 |
| LW | slow (speeds / 2) | 0 | 0.0 |
| BW | slow (speeds / 2) | 0 | 0.0 |
| LP | slow (speeds / 2) | 57 | 5.7 |
| LC | slow (speeds / 2) | 0 | 0.0 |
| laser | slow (speeds / 2) | 2430 | 240.9 |
| LW | Al lognormal (median 2.5 m/s) | 33 | 2.5 |
| BW | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LP | Al lognormal (median 2.5 m/s) | 12 | 1.6 |
| LC | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| laser | Al lognormal (median 2.5 m/s) | 1170 | 134.4 |

### p140

| Window | Released | Size, ΔT | Alloy | mg/m² per h of lasing | h to the limit, dense Al film | h, porous Al (f 0.1) |
|---|---|---|---|---|---|---|
| LW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.00437 | 250 | 1.3e+05 |
| LW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.00408 | 267 | 1.39e+05 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0019 | 573 | 2.99e+05 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00177 | 614 | 3.2e+05 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.000604 | 1.8e+03 | 9.4e+05 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.000564 | 1.93e+03 | 1.01e+06 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.22 | 4.95 | 2.58e+03 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.206 | 5.3 | 2.76e+03 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0123 | 185 | 8.73e+04 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0115 | 198 | 9.35e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00534 | 424 | 2.01e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00499 | 454 | 2.15e+05 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0017 | 1.33e+03 | 6.31e+05 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00159 | 1.43e+03 | 6.76e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.96 | 2.36 | 1.12e+03 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.897 | 2.53 | 1.2e+03 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.194 | 5.63 | 2.93e+03 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.181 | 6.02 | 3.14e+03 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.063 | 17.3 | 9e+03 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0589 | 18.5 | 9.64e+03 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00161 | 678 | 3.53e+05 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.0015 | 726 | 3.78e+05 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 3.43 | 0.318 | 166 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 3.2 | 0.34 | 177 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.162 | 6.72 | 3.5e+03 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.151 | 7.19 | 3.75e+03 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0455 | 23.9 | 1.25e+04 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0425 | 25.6 | 1.33e+04 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00203 | 536 | 2.79e+05 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.0019 | 574 | 2.99e+05 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 4.3 | 0.253 | 132 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 4.02 | 0.271 | 141 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0053 | 1.38 | 1.39e+03 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.00495 | 1.48 | 1.48e+03 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.00194 | 3.77 | 3.79e+03 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00181 | 4.04 | 4.05e+03 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 2.62e-05 | 279 | 2.8e+05 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 2.45e-05 | 299 | 3e+05 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.0568 | 0.129 | 129 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.0531 | 0.138 | 138 |
| LW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.208 | 5.23 | 2.72e+03 |
| LW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.195 | 5.6 | 2.92e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0907 | 12 | 6.26e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.0847 | 12.9 | 6.7e+03 |
| LW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0288 | 37.8 | 1.97e+04 |
| LW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0269 | 40.5 | 2.11e+04 |
| LW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 10.5 | 0.104 | 54 |
| LW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 9.82 | 0.111 | 57.8 |
| BW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.145 | 15.7 | 7.42e+03 |
| BW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.135 | 16.8 | 7.94e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0629 | 36 | 1.7e+04 |
| BW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.0588 | 38.6 | 1.82e+04 |
| BW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.02 | 113 | 5.36e+04 |
| BW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0187 | 121 | 5.74e+04 |
| BW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 11.3 | 0.201 | 94.8 |
| BW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 10.6 | 0.215 | 102 |
| LP | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 2.46 | 0.443 | 231 |
| LP | 5-20 mm | 0.05 um, dT 0 K | 7075 | 2.3 | 0.474 | 247 |
| LP | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.8 | 1.36 | 709 |
| LP | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.747 | 1.46 | 759 |
| LP | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0204 | 53.4 | 2.78e+04 |
| LP | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.019 | 57.2 | 2.98e+04 |
| LP | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 43.5 | 0.025 | 13 |
| LP | 5-20 mm | 0.1 um, dT 10 K | 7075 | 40.6 | 0.0268 | 14 |
| LC | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 2.45 | 0.444 | 231 |
| LC | 5-20 mm | 0.05 um, dT 0 K | 7075 | 2.29 | 0.475 | 248 |
| LC | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.689 | 1.58 | 823 |
| LC | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.644 | 1.69 | 881 |
| LC | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0308 | 35.4 | 1.84e+04 |
| LC | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0287 | 37.9 | 1.97e+04 |
| LC | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 65.1 | 0.0167 | 8.71 |
| LC | 5-20 mm | 0.1 um, dT 10 K | 7075 | 60.8 | 0.0179 | 9.33 |
| laser | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.152 | 0.048 | 48.2 |
| laser | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.142 | 0.0514 | 51.6 |
| laser | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0558 | 0.131 | 132 |
| laser | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.0521 | 0.14 | 141 |
| laser | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.000754 | 9.71 | 9.75e+03 |
| laser | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.000704 | 10.4 | 1.04e+04 |
| laser | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 1.63 | 0.00448 | 4.49 |
| laser | 5-20 mm | 0.1 um, dT 10 K | 7075 | 1.53 | 0.00479 | 4.81 |

| Window, speeds | Spatter hits per hour of lasing at 100 spatters/s | splat area (mm²/h) |
|---|---|---|
| LW | Ly 2017 speeds | 0 | 0.0 |
| BW | Ly 2017 speeds | 0 | 0.0 |
| LP | Ly 2017 speeds | 99 | 10.3 |
| LC | Ly 2017 speeds | 0 | 0.0 |
| laser | Ly 2017 speeds | 3297 | 322.0 |
| LW | slow (speeds / 2) | 3 | 0.7 |
| BW | slow (speeds / 2) | 0 | 0.0 |
| LP | slow (speeds / 2) | 51 | 7.1 |
| LC | slow (speeds / 2) | 0 | 0.0 |
| laser | slow (speeds / 2) | 2448 | 238.2 |
| LW | Al lognormal (median 2.5 m/s) | 30 | 1.8 |
| BW | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LP | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LC | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| laser | Al lognormal (median 2.5 m/s) | 1047 | 123.3 |

### p200_lw1

| Window | Released | Size, ΔT | Alloy | mg/m² per h of lasing | h to the limit, dense Al film | h, porous Al (f 0.1) |
|---|---|---|---|---|---|---|
| LW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.024 | 45.4 | 2.37e+04 |
| LW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0224 | 48.6 | 2.53e+04 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0104 | 104 | 5.43e+04 |
| LW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.00975 | 112 | 5.82e+04 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00333 | 328 | 1.71e+05 |
| LW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00311 | 351 | 1.83e+05 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.217 | 5.02 | 2.62e+03 |
| LW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.202 | 5.38 | 2.8e+03 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0813 | 27.9 | 1.32e+04 |
| BW | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0759 | 29.9 | 1.41e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0354 | 64.1 | 3.03e+04 |
| BW | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.033 | 68.6 | 3.25e+04 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0112 | 202 | 9.54e+04 |
| BW | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.0105 | 216 | 1.02e+05 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 3.97 | 0.571 | 270 |
| BW | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 3.71 | 0.612 | 289 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 1.08 | 1.01 | 525 |
| LP | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 1.01 | 1.08 | 562 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.406 | 2.68 | 1.4e+03 |
| LP | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.379 | 2.87 | 1.5e+03 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00451 | 242 | 1.26e+05 |
| LP | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00421 | 259 | 1.35e+05 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 9.85 | 0.111 | 57.6 |
| LP | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 9.2 | 0.118 | 61.7 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.0391 | 27.8 | 1.45e+04 |
| LC | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.0366 | 29.8 | 1.55e+04 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0122 | 89.1 | 4.64e+04 |
| LC | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0114 | 95.4 | 4.97e+04 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.000371 | 2.93e+03 | 1.53e+06 |
| LC | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.000347 | 3.14e+03 | 1.64e+06 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 0.79 | 1.38 | 718 |
| LC | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 0.738 | 1.48 | 769 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.194 | 0.0377 | 37.8 |
| laser | 0.5-5 mm | 0.05 um, dT 0 K | 7075 | 0.181 | 0.0403 | 40.5 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0741 | 0.0988 | 99.2 |
| laser | 0.5-5 mm | 0.1 um, dT 0 K | 7075 | 0.0692 | 0.106 | 106 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00111 | 6.6 | 6.62e+03 |
| laser | 0.5-5 mm | 0.3 um, dT 0 K | 7075 | 0.00104 | 7.06 | 7.09e+03 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | AlSi10Mg | 1.61 | 0.00456 | 4.57 |
| laser | 0.5-5 mm | 0.1 um, dT 10 K | 7075 | 1.5 | 0.00488 | 4.9 |
| LW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.194 | 5.62 | 2.93e+03 |
| LW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.181 | 6.01 | 3.13e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.0844 | 12.9 | 6.72e+03 |
| LW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.0788 | 13.8 | 7.2e+03 |
| LW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0269 | 40.5 | 2.11e+04 |
| LW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0251 | 43.4 | 2.26e+04 |
| LW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 1.75 | 0.622 | 324 |
| LW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 1.64 | 0.666 | 347 |
| BW | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 1.03 | 2.21 | 1.04e+03 |
| BW | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.96 | 2.36 | 1.12e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.447 | 5.07 | 2.4e+03 |
| BW | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.418 | 5.43 | 2.57e+03 |
| BW | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.142 | 15.9 | 7.54e+03 |
| BW | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.133 | 17.1 | 8.08e+03 |
| BW | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 50.2 | 0.0452 | 21.4 |
| BW | 5-20 mm | 0.1 um, dT 10 K | 7075 | 46.9 | 0.0484 | 22.9 |
| LP | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 8.05 | 0.135 | 70.5 |
| LP | 5-20 mm | 0.05 um, dT 0 K | 7075 | 7.52 | 0.145 | 75.5 |
| LP | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 3.03 | 0.36 | 188 |
| LP | 5-20 mm | 0.1 um, dT 0 K | 7075 | 2.83 | 0.385 | 201 |
| LP | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.0336 | 32.4 | 1.69e+04 |
| LP | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.0314 | 34.7 | 1.81e+04 |
| LP | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 73.4 | 0.0148 | 7.74 |
| LP | 5-20 mm | 0.1 um, dT 10 K | 7075 | 68.5 | 0.0159 | 8.28 |
| LC | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.976 | 1.12 | 581 |
| LC | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.912 | 1.19 | 622 |
| LC | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.305 | 3.57 | 1.86e+03 |
| LC | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.285 | 3.83 | 1.99e+03 |
| LC | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00926 | 118 | 6.12e+04 |
| LC | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.00865 | 126 | 6.56e+04 |
| LC | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 19.7 | 0.0553 | 28.8 |
| LC | 5-20 mm | 0.1 um, dT 10 K | 7075 | 18.4 | 0.0592 | 30.8 |
| laser | 5-20 mm | 0.05 um, dT 0 K | AlSi10Mg | 0.58 | 0.0126 | 12.7 |
| laser | 5-20 mm | 0.05 um, dT 0 K | 7075 | 0.542 | 0.0135 | 13.6 |
| laser | 5-20 mm | 0.1 um, dT 0 K | AlSi10Mg | 0.221 | 0.0331 | 33.2 |
| laser | 5-20 mm | 0.1 um, dT 0 K | 7075 | 0.207 | 0.0354 | 35.5 |
| laser | 5-20 mm | 0.3 um, dT 0 K | AlSi10Mg | 0.00331 | 2.21 | 2.22e+03 |
| laser | 5-20 mm | 0.3 um, dT 0 K | 7075 | 0.00309 | 2.36 | 2.37e+03 |
| laser | 5-20 mm | 0.1 um, dT 10 K | AlSi10Mg | 4.8 | 0.00152 | 1.53 |
| laser | 5-20 mm | 0.1 um, dT 10 K | 7075 | 4.48 | 0.00163 | 1.64 |

| Window, speeds | Spatter hits per hour of lasing at 100 spatters/s | splat area (mm²/h) |
|---|---|---|
| LW | Ly 2017 speeds | 3 | 0.7 |
| BW | Ly 2017 speeds | 0 | 0.0 |
| LP | Ly 2017 speeds | 261 | 9.0 |
| LC | Ly 2017 speeds | 0 | 0.0 |
| laser | Ly 2017 speeds | 3261 | 315.6 |
| LW | slow (speeds / 2) | 0 | 0.0 |
| BW | slow (speeds / 2) | 0 | 0.0 |
| LP | slow (speeds / 2) | 57 | 5.7 |
| LC | slow (speeds / 2) | 0 | 0.0 |
| laser | slow (speeds / 2) | 2424 | 237.9 |
| LW | Al lognormal (median 2.5 m/s) | 33 | 2.5 |
| BW | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LP | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| LC | Al lognormal (median 2.5 m/s) | 0 | 0.0 |
| laser | Al lognormal (median 2.5 m/s) | 1131 | 131.7 |

## Spatter glow and blur (spatter.py)

| Spatter | Camera, exposure | visible above (K) | glows for (ms) | over (mm) |
|---|---|---|---|---|
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1582 | 2.1 | 8 |
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1516 | 2.4 | 9 |
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1181 | 4.5 | 14 |
| Al, 35 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1143 | 4.8 | 15 |
| Al, 35 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 30 us | 1816 | 1.2 | 5 |
| Al, 35 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1788 | 1.3 | 5 |
| Al, 35 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1822 | 1.1 | 5 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1554 | 4.3 | 16 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1473 | 5.0 | 18 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1165 | 8.9 | 27 |
| Al, 50 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1118 | 9.7 | 28 |
| Al, 50 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 30 us | 1763 | 2.6 | 11 |
| Al, 50 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1728 | 2.8 | 12 |
| Al, 50 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1775 | 2.5 | 10 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1514 | 16.5 | 60 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1399 | 20.7 | 70 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1142 | 33.5 | 94 |
| Al, 100 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1073 | 37.9 | 100 |
| Al, 100 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 30 us | 1681 | 11.3 | 45 |
| Al, 100 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1628 | 12.8 | 50 |
| Al, 100 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1689 | 11.0 | 44 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 10 us | 1489 | 59.7 | 203 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm, 100 us | 1339 | 80.8 | 247 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 10 us | 1128 | 120.6 | 308 |
| Al, 200 um, T0 2200 K, 5 m/s | LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070), 100 us | 1037 | 143.1 | 334 |
| Al, 200 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 30 us | 1623 | 44.3 | 164 |
| Al, 200 um, T0 2200 K, 5 m/s | LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm, 100 us | 1547 | 52.7 | 186 |
| Al, 200 um, T0 2200 K, 5 m/s | Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter), 10000 us | 1610 | 45.6 | 168 |

## Compact tables (as quoted in monitoring/plume.md)

### p200

| Released | Out in 8 s | Out in 20 s | Median time out | Near the beam axis under the lid | laser | LW | LP | LC | BW |
|---|---|---|---|---|---|---|---|---|---|
| 0.5–5 mm | 99.5 % | 100.0 % | 0.039 s | 0.7 % | 0.03 % | 0.01 % | 0.32 % | 0.08 % | 0.02 % |
| 5–20 mm | 94.8 % | 99.8 % | 0.068 s | 7.4 % | 0.28 % | 0.21 % | 2.75 % | 0.86 % | 0.16 % |

| Where | 0.5–5 mm | 5–20 mm |
|---|---|---|
| LW recess | 5 (2) | 4.6e+02 (63) |
| LW near face | 0 (0) | 4.3e+02 (23) |
| BW recess | 99 (6) | 6.6e+02 (48) |
| BW near face | 74 (2) | 5.1e+02 (15) |
| LP recess | 2.1e+02 (96) | 2.2e+03 (824) |
| LP near face | 2.3e+02 (46) | 1.9e+03 (434) |
| LC recess | 24 (23) | 3.2e+02 (259) |
| LC near face | 44 (6) | 4.4e+02 (74) |
| laser recess | 2.3 (9) | 39 (84) |
| laser near face | 2.6 (1) | 1.1e+02 (15) |
| beam column z 20-120 (r < 5 mm) | 22 (219) | 2.7e+02 (3381) |
| over plate z 0-20 | 1.3e+02 (30000) | 2.4e+02 (29937) |
| ceiling layer at lid candidate (-60, -80) | 84 (210) | 7.4e+02 (1896) |
| ceiling layer at lid candidate (-40, 60) | 4.7 (34) | 38 (248) |
| ceiling layer at lid candidate (-20, 80) | 3.8 (24) | 29 (195) |
| ceiling layer at lid candidate (80, 80) | 37 (42) | 5.1e+02 (572) |
| left-wall layer at y -60, z 22-44 | 1.1e+02 (26) | 9.1e+02 (329) |
| left-wall layer at y -20, z 22-44 | 47 (28) | 6.1e+02 (319) |
| left-wall layer at y 20, z 22-44 | 42 (29) | 4.2e+02 (223) |
| left-wall layer at y 60, z 22-44 | 67 (22) | 5.5e+02 (167) |

| Window | u* | gas 1 mm off | J/S 0.1 um dT0, low / high (mg/m2/h per g/h) |
|---|---|---|---|
| laser | 0.065 | 0.097 | 0.013 / 0.53 |
| LW | 0.017 | 0.015 | 0 / 0.68 |
| LP | 0.058 | 0.22 | 0.99 / 8.1 |
| LC | 0.026 | 0.077 | 0.067 / 0.68 |
| BW | 0.01 | 0.0069 | 0.068 / 0.47 |

| Window | v_d 0.1 um | mg/m2/h low / high (AlSi10Mg) | 10 K colder | h porous (dense), high | 10 K colder |
|---|---|---|---|---|---|
| laser | 5e-06 | 0.0062 / 0.25 | 0.14 / 5.6 | 29 (0.029) | 1.3 (0.0013) |
| LW | 1.6e-06 | 0 / 0.32 | 0 / 22 | 1.8e+03 (3.4) | 26 (0.049) |
| LP | 4.3e-06 | 0.46 / 3.8 | 12 / 97 | 1.5e+02 (0.29) | 5.8 (0.011) |
| LC | 1.5e-06 | 0.031 / 0.32 | 2.2 / 23 | 1.8e+03 (3.4) | 25 (0.048) |
| BW | 9.2e-07 | 0.032 / 0.22 | 3.8 / 26 | 4.9e+03 (10) | 42 (0.088) |

| Window | Al-like hits/h, mm2/h | Ly hits/h, mm2/h |
|---|---|---|
| laser | 1158 / 132.7 | 3219 / 310.9 |
| LW | 33 / 2.5 | 3 / 0.7 |
| LP | 0 / 0.0 | 93 / 8.9 |
| LC | 0 / 0.0 | 0 / 0.0 |
| BW | 0 / 0.0 | 0 / 0.0 |

| Speeds | d | laser | LW | LP | plate | floor | outlet | lid | door side |
|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.0 % | 13.9 % | 0.9 % | 58.4 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 2.9 % | 1.3 % | 0.0 % | 95.2 % |
| Ly 2017 speeds | 50 | 0.07 % | 0.00 % | 0.00 % | 0.5 % | 13.5 % | 2.5 % | 0.3 % | 75.9 % |
| Ly 2017 speeds | 100 | 5.33 % | 0.00 % | 0.17 % | 1.5 % | 21.2 % | 2.6 % | 26.5 % | 17.8 % |
| Ly 2017 speeds | 150 | 6.75 % | 0.00 % | 0.17 % | 0.8 % | 7.2 % | 0.4 % | 35.4 % | 15.2 % |
| Ly 2017 speeds | 200 | 7.75 % | 0.08 % | 0.25 % | 0.0 % | 2.5 % | 0.1 % | 37.7 % | 14.0 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 19.9 % | 38.5 % | 0.0 % | 41.7 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.5 % | 2.7 % | 0.0 % | 93.7 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.0 % | 1.7 % | 0.0 % | 91.1 % |
| slow (speeds / 2) | 100 | 4.08 % | 0.00 % | 0.08 % | 1.5 % | 18.6 % | 3.7 % | 15.1 % | 38.8 % |
| slow (speeds / 2) | 150 | 5.17 % | 0.00 % | 0.17 % | 2.2 % | 17.2 % | 1.3 % | 27.1 % | 22.3 % |
| slow (speeds / 2) | 200 | 6.33 % | 0.00 % | 0.08 % | 1.9 % | 14.9 % | 0.9 % | 28.2 % | 17.3 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.6 % | 58.5 % | 0.0 % | 15.9 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.7 % | 4.7 % | 0.0 % | 88.5 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.4 % | 1.5 % | 0.0 % | 95.0 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.50 % | 0.08 % | 0.00 % | 2.5 % | 34.2 % | 4.6 % | 3.8 % | 45.3 % |
| Al lognormal (median 2.5 m/s) | 150 | 3.08 % | 0.00 % | 0.00 % | 3.2 % | 30.9 % | 2.7 % | 12.0 % | 28.4 % |
| Al lognormal (median 2.5 m/s) | 200 | 4.83 % | 0.08 % | 0.00 % | 3.6 % | 24.5 % | 1.4 % | 17.1 % | 21.1 % |

### p200_lw3

| Released | Out in 8 s | Out in 20 s | Median time out | Near the beam axis under the lid | laser | LW | LP | LC | BW |
|---|---|---|---|---|---|---|---|---|---|
| 0.5–5 mm | 99.5 % | 100.0 % | 0.039 s | 0.6 % | 0.03 % | 0.05 % | 0.22 % | 0.09 % | 0.01 % |
| 5–20 mm | 94.9 % | 99.8 % | 0.065 s | 6.4 % | 0.22 % | 0.54 % | 2.43 % | 0.89 % | 0.11 % |

| Where | 0.5–5 mm | 5–20 mm |
|---|---|---|
| LW recess | 13 (16) | 1.2e+02 (162) |
| LW near face | 1.1 (6) | 9.3 (43) |
| BW recess | 58 (2) | 5.3e+02 (34) |
| BW near face | 17 (1) | 4e+02 (14) |
| LP recess | 1.6e+02 (67) | 2.2e+03 (730) |
| LP near face | 1.7e+02 (38) | 1.9e+03 (398) |
| LC recess | 33 (26) | 3.9e+02 (268) |
| LC near face | 56 (11) | 5.2e+02 (121) |
| laser recess | 30 (8) | 27 (66) |
| laser near face | 1e+02 (4) | 45 (9) |
| beam column z 20-120 (r < 5 mm) | 18 (180) | 2.7e+02 (3368) |
| over plate z 0-20 | 1.3e+02 (30000) | 2.3e+02 (29939) |
| ceiling layer at lid candidate (-60, -80) | 55 (155) | 6e+02 (1599) |
| ceiling layer at lid candidate (-40, 60) | 1.3 (10) | 20 (153) |
| ceiling layer at lid candidate (-20, 80) | 1.3 (9) | 16 (117) |
| ceiling layer at lid candidate (80, 80) | 35 (37) | 4.7e+02 (513) |
| left-wall layer at y -60, z 22-44 | 63 (29) | 5e+02 (260) |
| left-wall layer at y -20, z 22-44 | 25 (31) | 2.6e+02 (290) |
| left-wall layer at y 20, z 22-44 | 74 (33) | 1.1e+03 (284) |
| left-wall layer at y 60, z 22-44 | 52 (18) | 1.1e+03 (285) |

| Window | u* | gas 1 mm off | J/S 0.1 um dT0, low / high (mg/m2/h per g/h) |
|---|---|---|---|
| laser | 0.066 | 0.1 | 0.52 / 0.23 |
| LW | 0.14 | 0.82 | 0.013 / 0.11 |
| LP | 0.059 | 0.23 | 0.77 / 8.4 |
| LC | 0.032 | 0.11 | 0.11 / 1.1 |
| BW | 0.0088 | 0.0053 | 0.013 / 0.32 |

| Window | v_d 0.1 um | mg/m2/h low / high (AlSi10Mg) | 10 K colder | h porous (dense), high | 10 K colder |
|---|---|---|---|---|---|
| laser | 5.1e-06 | 0.24 / 0.11 | 5.4 / 2.4 | 68 (0.068) | 3.1 (0.0031) |
| LW | 1.2e-05 | 0.0063 / 0.054 | 0.061 / 0.52 | 1.1e+04 (20) | 1.1e+03 (2.1) |
| LP | 4.4e-06 | 0.36 / 4 | 9.1 / 99 | 1.4e+02 (0.27) | 5.7 (0.011) |
| LC | 2e-06 | 0.054 / 0.5 | 2.9 / 27 | 1.1e+03 (2.2) | 21 (0.041) |
| BW | 8e-07 | 0.0063 / 0.15 | 0.86 / 20 | 7.2e+03 (15) | 54 (0.11) |

| Window | Al-like hits/h, mm2/h | Ly hits/h, mm2/h |
|---|---|---|
| laser | 1170 / 134.4 | 3243 / 314.1 |
| LW | 33 / 2.5 | 3 / 0.7 |
| LP | 12 / 1.6 | 96 / 9.6 |
| LC | 0 / 0.0 | 0 / 0.0 |
| BW | 0 / 0.0 | 0 / 0.0 |

| Speeds | d | laser | LW | LP | plate | floor | outlet | lid | door side |
|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 19.7 % | 14.5 % | 0.1 % | 61.8 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.3 % | 2.0 % | 0.0 % | 94.3 % |
| Ly 2017 speeds | 50 | 0.07 % | 0.00 % | 0.00 % | 0.5 % | 13.6 % | 2.2 % | 0.3 % | 76.1 % |
| Ly 2017 speeds | 100 | 5.33 % | 0.00 % | 0.17 % | 1.3 % | 22.0 % | 1.9 % | 26.2 % | 17.8 % |
| Ly 2017 speeds | 150 | 6.92 % | 0.00 % | 0.17 % | 0.8 % | 7.2 % | 0.4 % | 35.5 % | 15.5 % |
| Ly 2017 speeds | 200 | 7.75 % | 0.08 % | 0.33 % | 0.0 % | 2.3 % | 0.1 % | 37.8 % | 14.2 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.8 % | 39.0 % | 0.0 % | 40.2 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 4.6 % | 2.8 % | 0.0 % | 92.5 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.1 % | 1.9 % | 0.0 % | 91.7 % |
| slow (speeds / 2) | 100 | 4.00 % | 0.00 % | 0.08 % | 1.8 % | 18.8 % | 3.5 % | 14.9 % | 38.2 % |
| slow (speeds / 2) | 150 | 5.33 % | 0.00 % | 0.17 % | 2.1 % | 17.0 % | 1.2 % | 27.3 % | 22.5 % |
| slow (speeds / 2) | 200 | 6.17 % | 0.00 % | 0.08 % | 1.7 % | 15.7 % | 0.8 % | 27.9 % | 17.5 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.5 % | 59.7 % | 0.0 % | 14.7 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.1 % | 4.7 % | 0.0 % | 88.1 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.8 % | 1.5 % | 0.0 % | 94.7 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.50 % | 0.08 % | 0.00 % | 2.3 % | 34.8 % | 4.3 % | 3.8 % | 44.8 % |
| Al lognormal (median 2.5 m/s) | 150 | 3.17 % | 0.00 % | 0.08 % | 2.9 % | 31.8 % | 2.8 % | 12.2 % | 27.9 % |
| Al lognormal (median 2.5 m/s) | 200 | 4.83 % | 0.08 % | 0.00 % | 3.6 % | 24.3 % | 1.2 % | 17.3 % | 21.0 % |

### p140

| Released | Out in 8 s | Out in 20 s | Median time out | Near the beam axis under the lid | laser | LW | LP | LC | BW |
|---|---|---|---|---|---|---|---|---|---|
| 0.5–5 mm | 99.3 % | 100.0 % | 0.056 s | 0.6 % | 0.02 % | 0.01 % | 0.09 % | 0.09 % | 0.01 % |
| 5–20 mm | 91.5 % | 99.2 % | 0.087 s | 7.8 % | 0.28 % | 0.09 % | 1.10 % | 1.22 % | 0.06 % |

| Where | 0.5–5 mm | 5–20 mm |
|---|---|---|
| LW recess | 21 (3) | 2.7e+02 (26) |
| LW near face | 4.3 (2) | 2.1e+02 (8) |
| BW recess | 25 (2) | 5.7e+02 (17) |
| BW near face | 19 (1) | 2.2e+02 (7) |
| LP recess | 1.1e+02 (26) | 1.1e+03 (330) |
| LP near face | 67 (13) | 8.5e+02 (138) |
| LC recess | 62 (26) | 9.4e+02 (366) |
| LC near face | 85 (12) | 1.3e+03 (147) |
| laser recess | 0.99 (6) | 28 (83) |
| laser near face | 1.1 (2) | 31 (7) |
| beam column z 20-120 (r < 5 mm) | 21 (141) | 3.5e+02 (3050) |
| over plate z 0-20 | 1.9e+02 (30000) | 3.3e+02 (29965) |
| ceiling layer at lid candidate (-60, -80) | 36 (53) | 4.1e+02 (554) |
| ceiling layer at lid candidate (-40, 60) | 2.9 (15) | 28 (146) |
| ceiling layer at lid candidate (-20, 80) | 2.4 (10) | 31 (161) |
| ceiling layer at lid candidate (80, 80) | 37 (36) | 5.7e+02 (531) |
| left-wall layer at y -60, z 22-44 | 3.7 (5) | 5e+02 (35) |
| left-wall layer at y -20, z 22-44 | 41 (12) | 3e+02 (128) |
| left-wall layer at y 20, z 22-44 | 24 (5) | 7.6e+02 (115) |
| left-wall layer at y 60, z 22-44 | 88 (18) | 8.5e+02 (167) |

| Window | u* | gas 1 mm off | J/S 0.1 um dT0, low / high (mg/m2/h per g/h) |
|---|---|---|---|
| laser | 0.051 | 0.062 | 0.0041 / 0.12 |
| LW | 0.01 | 0.0054 | 0.004 / 0.19 |
| LP | 0.031 | 0.067 | 0.13 / 1.7 |
| LC | 0.021 | 0.054 | 0.097 / 1.5 |
| BW | 0.0066 | 0.003 | 0.011 / 0.13 |

| Window | v_d 0.1 um | mg/m2/h low / high (AlSi10Mg) | 10 K colder | h porous (dense), high | 10 K colder |
|---|---|---|---|---|---|
| laser | 3.8e-06 | 0.0019 / 0.056 | 0.057 / 1.6 | 1.3e+02 (0.13) | 4.5 (0.0045) |
| LW | 9.3e-07 | 0.0019 / 0.091 | 0.22 / 11 | 6.3e+03 (12) | 54 (0.1) |
| LP | 2e-06 | 0.063 / 0.8 | 3.4 / 44 | 7.1e+02 (1.4) | 13 (0.025) |
| LC | 1.1e-06 | 0.046 / 0.69 | 4.3 / 65 | 8.2e+02 (1.6) | 8.7 (0.017) |
| BW | 6e-07 | 0.0053 / 0.063 | 0.96 / 11 | 1.7e+04 (36) | 95 (0.2) |

| Window | Al-like hits/h, mm2/h | Ly hits/h, mm2/h |
|---|---|---|
| laser | 1047 / 123.3 | 3297 / 322.0 |
| LW | 30 / 1.8 | 0 / 0.0 |
| LP | 0 / 0.0 | 99 / 10.3 |
| LC | 0 / 0.0 | 0 / 0.0 |
| BW | 0 / 0.0 | 0 / 0.0 |

| Speeds | d | laser | LW | LP | plate | floor | outlet | lid | door side |
|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.1 % | 29.2 % | 0.1 % | 46.1 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.3 % | 1.6 % | 0.0 % | 94.2 % |
| Ly 2017 speeds | 50 | 0.00 % | 0.00 % | 0.00 % | 0.4 % | 14.1 % | 3.9 % | 0.4 % | 73.7 % |
| Ly 2017 speeds | 100 | 5.50 % | 0.00 % | 0.17 % | 3.8 % | 22.2 % | 0.8 % | 26.1 % | 15.2 % |
| Ly 2017 speeds | 150 | 7.25 % | 0.00 % | 0.17 % | 0.9 % | 7.2 % | 0.3 % | 36.4 % | 14.6 % |
| Ly 2017 speeds | 200 | 7.58 % | 0.00 % | 0.42 % | 0.2 % | 1.9 % | 0.2 % | 38.0 % | 13.8 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 26.2 % | 50.6 % | 0.0 % | 23.2 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 8.2 % | 5.9 % | 0.0 % | 85.9 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.1 % | 8.1 % | 3.2 % | 0.0 % | 88.5 % |
| slow (speeds / 2) | 100 | 4.17 % | 0.00 % | 0.00 % | 3.2 % | 32.7 % | 4.4 % | 14.8 % | 21.9 % |
| slow (speeds / 2) | 150 | 5.08 % | 0.00 % | 0.33 % | 5.6 % | 19.0 % | 1.0 % | 27.1 % | 16.2 % |
| slow (speeds / 2) | 200 | 6.00 % | 0.08 % | 0.08 % | 3.3 % | 14.8 % | 0.5 % | 28.2 % | 14.8 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.3 % | 24.4 % | 70.2 % | 0.0 % | 5.1 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.2 % | 12.9 % | 9.3 % | 0.0 % | 77.5 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 6.3 % | 3.4 % | 0.0 % | 90.3 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.33 % | 0.08 % | 0.00 % | 7.7 % | 49.0 % | 3.9 % | 3.8 % | 25.0 % |
| Al lognormal (median 2.5 m/s) | 150 | 2.67 % | 0.00 % | 0.00 % | 8.4 % | 34.8 % | 1.7 % | 13.2 % | 18.2 % |
| Al lognormal (median 2.5 m/s) | 200 | 5.08 % | 0.00 % | 0.00 % | 6.2 % | 24.7 % | 0.6 % | 18.2 % | 16.2 % |

### p200_lw1

| Released | Out in 8 s | Out in 20 s | Median time out | Near the beam axis under the lid | laser | LW | LP | LC | BW |
|---|---|---|---|---|---|---|---|---|---|
| 0.5–5 mm | 99.4 % | 100.0 % | 0.039 s | 0.7 % | 0.04 % | 0.10 % | 0.26 % | 0.04 % | 0.03 % |
| 5–20 mm | 94.5 % | 99.8 % | 0.067 s | 7.2 % | 0.25 % | 0.71 % | 2.45 % | 0.43 % | 0.14 % |

| Where | 0.5–5 mm | 5–20 mm |
|---|---|---|
| LW recess | 33 (31) | 2.3e+02 (212) |
| LW near face | 4.1 (13) | 33 (43) |
| BW recess | 1.4e+02 (9) | 1.3e+03 (41) |
| BW near face | 78 (3) | 9.9e+02 (22) |
| LP recess | 1.6e+02 (77) | 1.6e+03 (735) |
| LP near face | 1.9e+02 (38) | 1.4e+03 (376) |
| LC recess | 21 (13) | 2.6e+02 (130) |
| LC near face | 16 (6) | 3.9e+02 (51) |
| laser recess | 13 (12) | 32 (74) |
| laser near face | 31 (2) | 91 (12) |
| beam column z 20-120 (r < 5 mm) | 22 (195) | 2.5e+02 (3126) |
| over plate z 0-20 | 1.3e+02 (30000) | 2.4e+02 (29921) |
| ceiling layer at lid candidate (-60, -80) | 61 (158) | 6.6e+02 (1723) |
| ceiling layer at lid candidate (-40, 60) | 2.6 (20) | 24 (193) |
| ceiling layer at lid candidate (-20, 80) | 1.8 (12) | 18 (128) |
| ceiling layer at lid candidate (80, 80) | 34 (50) | 4e+02 (570) |
| left-wall layer at y -60, z 22-44 | 97 (26) | 7.7e+02 (296) |
| left-wall layer at y -20, z 22-44 | 34 (31) | 3.3e+02 (271) |
| left-wall layer at y 20, z 22-44 | 24 (16) | 3.1e+02 (145) |
| left-wall layer at y 60, z 22-44 | 26 (16) | 4.1e+02 (185) |

| Window | u* | gas 1 mm off | J/S 0.1 um dT0, low / high (mg/m2/h per g/h) |
|---|---|---|---|
| laser | 0.067 | 0.1 | 0.16 / 0.47 |
| LW | 0.06 | 0.22 | 0.022 / 0.18 |
| LP | 0.061 | 0.24 | 0.87 / 6.5 |
| LC | 0.028 | 0.086 | 0.026 / 0.65 |
| BW | 0.011 | 0.0076 | 0.075 / 0.95 |

| Window | v_d 0.1 um | mg/m2/h low / high (AlSi10Mg) | 10 K colder | h porous (dense), high | 10 K colder |
|---|---|---|---|---|---|
| laser | 5.2e-06 | 0.074 / 0.22 | 1.6 / 4.8 | 33 (0.033) | 1.5 (0.0015) |
| LW | 5.4e-06 | 0.01 / 0.084 | 0.22 / 1.8 | 6.7e+03 (13) | 3.2e+02 (0.62) |
| LP | 4.6e-06 | 0.41 / 3 | 9.8 / 73 | 1.9e+02 (0.36) | 7.7 (0.015) |
| LC | 1.7e-06 | 0.012 / 0.3 | 0.79 / 20 | 1.9e+03 (3.6) | 29 (0.055) |
| BW | 9.6e-07 | 0.035 / 0.45 | 4 / 50 | 2.4e+03 (5.1) | 21 (0.045) |

| Window | Al-like hits/h, mm2/h | Ly hits/h, mm2/h |
|---|---|---|
| laser | 1131 / 131.7 | 3261 / 315.6 |
| LW | 33 / 2.5 | 3 / 0.7 |
| LP | 0 / 0.0 | 261 / 9.0 |
| LC | 0 / 0.0 | 0 / 0.0 |
| BW | 0 / 0.0 | 0 / 0.0 |

| Speeds | d | laser | LW | LP | plate | floor | outlet | lid | door side |
|---|---|---|---|---|---|---|---|---|---|
| Ly 2017 speeds | 20 | 0.00 % | 0.00 % | 0.13 % | 0.0 % | 20.4 % | 14.9 % | 0.6 % | 60.8 % |
| Ly 2017 speeds | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 2.9 % | 1.8 % | 0.0 % | 94.1 % |
| Ly 2017 speeds | 50 | 0.00 % | 0.00 % | 0.00 % | 0.5 % | 13.7 % | 2.2 % | 0.3 % | 75.7 % |
| Ly 2017 speeds | 100 | 5.58 % | 0.00 % | 0.17 % | 1.4 % | 20.9 % | 2.5 % | 26.2 % | 18.3 % |
| Ly 2017 speeds | 150 | 6.75 % | 0.00 % | 0.17 % | 0.7 % | 7.5 % | 0.6 % | 35.5 % | 15.2 % |
| Ly 2017 speeds | 200 | 7.75 % | 0.08 % | 0.25 % | 0.2 % | 2.2 % | 0.1 % | 37.8 % | 14.1 % |
| slow (speeds / 2) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 20.6 % | 38.7 % | 0.0 % | 40.7 % |
| slow (speeds / 2) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.9 % | 2.2 % | 0.0 % | 93.7 % |
| slow (speeds / 2) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.9 % | 1.7 % | 0.0 % | 89.9 % |
| slow (speeds / 2) | 100 | 4.08 % | 0.00 % | 0.08 % | 1.5 % | 19.7 % | 3.2 % | 15.0 % | 38.6 % |
| slow (speeds / 2) | 150 | 5.08 % | 0.00 % | 0.17 % | 2.3 % | 17.2 % | 1.2 % | 27.1 % | 22.5 % |
| slow (speeds / 2) | 200 | 6.17 % | 0.00 % | 0.08 % | 1.8 % | 15.2 % | 0.8 % | 28.2 % | 17.3 % |
| Al lognormal (median 2.5 m/s) | 20 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 25.4 % | 59.4 % | 0.0 % | 15.2 % |
| Al lognormal (median 2.5 m/s) | 35 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 7.1 % | 4.6 % | 0.0 % | 88.3 % |
| Al lognormal (median 2.5 m/s) | 50 | 0.00 % | 0.00 % | 0.00 % | 0.0 % | 3.7 % | 1.4 % | 0.0 % | 94.7 % |
| Al lognormal (median 2.5 m/s) | 100 | 1.42 % | 0.08 % | 0.00 % | 2.2 % | 33.7 % | 5.3 % | 3.8 % | 45.7 % |
| Al lognormal (median 2.5 m/s) | 150 | 3.08 % | 0.00 % | 0.00 % | 2.8 % | 32.0 % | 2.6 % | 12.0 % | 28.3 % |
| Al lognormal (median 2.5 m/s) | 200 | 4.92 % | 0.08 % | 0.00 % | 3.5 % | 24.7 % | 1.2 % | 17.2 % | 21.2 % |

