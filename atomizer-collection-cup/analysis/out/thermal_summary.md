# Thermal FEA summary (CalculiX, axisymmetric, transient)

Every case: the shot (or powder) lands all at once at t = 0 and the run is followed for an hour. Shot: packed bed (60 % dense) at 1050 C, 70 % liquid, k_eff 5 W/m K unless the case says otherwise. Peaks are the hottest node of each part at any of the 180 output times. Seal ratings: FKM 200 C continuous / 230 C short; EPDM 150 / 175 C; FFKM 240 / 325 C. Cases: `analysis/thermal.py` (CASES).

| Case | What lands, where | Joint O-ring max (C) [at s] | Other seal max (C) | TC top max | TC bottom max | Floor/plate max | Glass dT max (K) |
|---|---|---|---|---:|---:|---:|---:|
| B_100 | 100 g shot on the puck | 26 [2130] |  | 27 | 108 | 124 |  |
| B_400 | 400 g shot on the puck | 32 [1530] |  | 34 | 238 | 264 |  |
| B_816 | 816 g shot on the puck (Nov 13 charge) | 44 [1140] |  | 51 | 321 | 348 |  |
| B_816_k2 | 816 g, pile k 2 W/m K | 45 [1170] |  | 52 | 297 | 320 |  |
| B_816_k20 | 816 g, pile k 20 W/m K (fused) | 42 [1230] |  | 48 | 349 | 383 |  |
| B_816_noliner | 816 g, no liner | 43 [930] |  | 50 | 345 | 354 |  |
| B_816_cupuck | 816 g, copper puck | 44 [1140] |  | 51 | 347 | 378 |  |
| B_816_powder400 | 816 g of powder at 400 C (a good run) | 29 [1770] |  | 30 | 86 | 92 |  |
| B_hangup_25 | 25 g of shot fused in the bore just under the joint | 195 [22] |  | 158 | 25 | 25 |  |
| B_hangup_100 | 100 g of shot fused in the bore just under the joint | 389 [53] |  | 703 | 26 | 26 |  |
| A_100 | 100 g shot on the puck | 37 [1230] | bottom O-ring 138 [480] | 41 | 107 | 154 |  |
| A_250 | 250 g shot on the puck | 66 [870] | bottom O-ring 215 [630] | 80 | 182 | 234 |  |
| A_400 | 400 g shot on the puck | 110 [720] | bottom O-ring 248 [750] | 141 | 221 | 269 |  |
| C_400 | 400 g shot in the pan, fused quartz | 28 [206] | seal_top 73 [25]; seal_bot 264 [150] | nan | nan | 160 | 132.5 |
| C_816 | 816 g shot in the pan, fused quartz | 32 [360] | seal_top 99 [180]; seal_bot 333 [240] | nan | nan | 221 | 286.3 |
| C_400_boro | 400 g shot in the pan, borosilicate | 28 [206] | seal_top 56 [22]; seal_bot 263 [150] | nan | nan | 160 | 116.7 |
| S_seat_120 | stock cup: 120 g of shot against the EPDM seat (Nov 13) | 49 [180] | seat 1013 [0]; seal_top 48 [720]; seal_bot 28 [180] | nan | nan | nan | 22.4 |
| S_glass_300 | stock cup: 300 g of shot fallen into the glass, against its wall (Nov 13) | 26 [131] | seat 92 [16]; seal_top 56 [10]; seal_bot 412 [0] | nan | nan | nan | 919.3 |

## Largest shot mass before the hottest seal reaches 150 C / 200 C

Linear interpolation between the mass cases (base cases only).

| Design | Seal | to 150 C (g) | to 200 C (g) | cases (mass g, seal peak C) |
|---|---|---|---|---|
| B (joint O-ring) | oring | > 816 (largest case run) | > 816 (largest case run) | 100: 26, 400: 32, 816: 44 |
| A (bottom O-ring) | boring | 123 | 221 | 100: 138, 250: 215, 400: 248 |
| C (bottom glass seal) | seal_bot | < 400 | < 400 | 400: 264, 816: 333 |

## When the alarms would sound (s after the metal lands)

Top thermocouple alarm 120 C, bottom 150 C; blank = never within the hour.

| Case | top TC >= 120 C | bottom TC >= 150 C | O-ring >= 150 C | O-ring >= 200 C | bottom TC at 60 s | at 1 h |
|---|---:|---:|---:|---:|---:|---:|
| B_400 |  | 136 |  |  | 66.0 | 104.0 |
| B_816 |  | 119 |  |  | 69.0 | 151.0 |
| B_816_powder400 |  |  |  |  | 30.0 | 70.0 |
| B_hangup_25 | 7 |  | 3 |  | 25.0 | 25.0 |
| B_hangup_100 | 0 |  | 2 | 4 | 25.0 | 26.0 |
| A_100 |  |  |  |  | 55.0 | 49.0 |
| A_250 |  | 236 |  |  | 70.0 | 74.0 |

## Checks on the model

- `analysis/verify_axifea.py`: steady film, radiation and surface-flux cases match closed-form answers to 0.001 K; a lumped transient is within 0.8 %.
- Sensitivity of B_816 to the pile's conductivity (2, 5, 20 W/m K), the liner and a copper puck: see the table (the joint O-ring moves by about 2 K).
- Not modelled: wall-to-wall radiation and argon convection inside (the pile's radiation is put on the first wall it reaches, all absorbed: conservative for the walls near the pile); the clamp (it would carry heat from the cup's flange to the cooled cone: conservative); the shot arriving over 30-90 s instead of at once (conservative for peaks).
