# Vacuum tightness of the frame + floor plate, and the purge with the dry scroll pump

From [`analysis/seals/vacuum_purge.py`](../../seals/vacuum_purge.py), which reads `seals.json` from [`seals.py`](../../seals/seals.py). The question and the conclusions are in [`vacuum-and-purge.md`](../../../vacuum-and-purge.md).

Gas envelope 11.3 L; build at +20 mbar of argon. sccs = std cc/s.

## 1. Permeation: the old block against the frame + floor plate

| Design | O₂ (sccs) | N₂ (sccs) | H₂O (sccs) | O₂ during a build (ppm/h) | H₂O during a build (ppm/h) | Ar make-up for 10 ppm O₂ (sccm) | Rate of rise at vacuum (mbar/min) |
|---|---|---|---|---|---|---|---|
| solid block (no floor joint, rail inserts blind in the wall) | 5.60e-06 | 2.86e-06 | 5.05e-05 | 1.76 | 15.8 | 37.4 | 3.18e-04 |
| frame + floor plate (as drawn) | 7.05e-06 | 3.60e-06 | 6.35e-05 | 2.21 | 19.9 | 47.0 | 4.00e-04 |
| the floor joint alone (947 mm cord at 60 C + 4 bonded washers) | 1.44e-06 | 7.38e-07 | 1.30e-05 | 0.45 | 4.1 | 9.6 | 8.20e-05 |

The frame lets in 26 % more O₂ by permeation than the block did. The floor cord is taken at 60 °C; at 40 °C its share would be 0.42× that. N₂/O₂ = 0.51 through FKM (Parker). The 4 bonded washers add 3.53e-08 sccs of O₂.

## 2. Real leaks: one defect channel across a 2 mm seal land

| Channel (µm square) | Air in at vacuum (mbar·L/s) | Rate of rise (mbar/min) | Argon out at +20 mbar (sccm) | Exit velocity (m/s) | Péclet | O₂ in against the outflow during a build (sccs) |
|---|---|---|---|---|---|---|
| 2 | 7.97e-07 | 4.25e-06 | 1.51e-06 | 0.01 | 0.6 | 5.60e-09 |
| 5 | 3.11e-05 | 1.66e-04 | 5.91e-05 | 0.04 | 3.9 | 3.81e-09 |
| 10 | 4.98e-04 | 2.65e-03 | 9.46e-04 | 0.16 | 15.8 | 4.35e-13 |
| 20 | 7.97e-03 | 0.04 | 0.02 | 0.63 | 63.1 | 1.97e-32 |
| 45 | 0.20 | 1.09 | 0.39 | 3.19 | 319.4 | 2.49e-142 |

For comparison, permeation through every seal brings in 7.05e-06 sccs of O₂ during a build.

The leak budget in `seals.md` is 1e-4 mbar·L/s in all, a rise of 5e-4 mbar/min; the acceptance test passes under 1e-3 mbar/min.

## 3. Virtual leaks

| Volume | Size | n | Conductance, molecular (L/s) | τ = V/C (s) | Air it held (mbar·L) | O₂ if all released after back-fill (ppm) |
|---|---|---|---|---|---|---|
| floor crevice | 35 mm³ | 1 | 0.21 | 1.69e-04 | 0.04 | 0.64 |
| plugged rail hole | 20 mm³ | 4 | 1.03e-06 | 19.65 | 0.08 | 1.48 |

## 4. Purge with the Edwards nXDS6i dry scroll (BOM G2)

Listed 6.8 m³/h (1.89 L/s), ultimate 0.02 mbar; two KF-25 bellows (1.2 m). Effective speed at the chamber (L/s): 800 mbar 1.89, 100 mbar 1.89, 10 mbar 1.86, 1 mbar 1.66, 0.1 mbar 0.89, 0.05 mbar 0.63.

Pump-down from 1013 mbar with the soft-pump start (V/S = 25 s to 100 mbar), against the walls' outgassing 5 min after closing: 100 mbar: 1.0 min, 10 mbar: 1.2 min, 1 mbar: 1.4 min, 0.1 mbar: 1.8 min, 0.05 mbar: 2.0 min.

| Minutes after closing | Wall + seal outgassing (mbar·L/s) | Base pressure (mbar) |
|---|---|---|
| 5 | 7.22e-04 | 0.021 |
| 15 | 2.41e-04 | 0.020 |
| 60 | 6.02e-05 | 0.020 |

O₂ after each cycle (pump to the base pressure, 2 min hold with a 1e-4 mbar·L/s leak, back-fill to +20 mbar). One cycle takes ~3.9 min, three ~12 min.

| Base pressure | Ar 5.0 at 1 ppm O₂: cycles 1 / 2 / 3 (ppm) | at 2 ppm O₂ (ppm) |
|---|---|---|
| 1 mbar (the plan) | 204 / 1.41 / 1.22 | 205 / 2.41 / 2.22 |
| 0.1 mbar | 21.49 / 1.22 / 1.22 | 22.49 / 2.22 / 2.22 |
| 0.05 mbar (scroll near its ultimate) | 11.35 / 1.22 / 1.22 | 12.35 / 2.22 / 2.22 |
| 1e-5 mbar (with a turbo) | 1.22 / 1.22 / 1.22 | 2.22 / 2.22 / 2.22 |

## 5. Water after the purge

| Hold before back-fill | Wall + seal water released in the first hour after (mbar·L) | ppm in the loop with no make-up |
|---|---|---|
| 10 min | 0.42 | 36 |
| 30 min | 0.24 | 20 |
| 60 min | 0.15 | 13 |

Powder: 22.5–45.0 mg of water in 150 g (30–61 mbar·L), 2486–4971 ppmv if the hot plate drives it all off.

## Sources

1. Parker O-Ring Handbook ORD 5700 §3.12.1 (leak rate L = 0.7 F D P Q (1-S)^2) and Table 3-24 (permeability); via seals.py
2. Sturm et al. (2004) J. Geophys. Res. 109, D04309, https://doi.org/10.1029/2003JD004073: water permeation of Viton O-rings; via seals.py
3. O'Hanlon, A User's Guide to Vacuum Technology, 3rd ed. (Wiley 2003): viscous and molecular conductance (C = 135 d^4 p / L, C = 12.1 d^3 / L for air, d and L in cm), outgassing of unbaked Al and Viton after 1 h, falling ~1/t
4. Edwards nXDS6i dry scroll pump: 6.8 m3/h and 0.02 mbar ultimate as listed in BOM line G2 (Marshall Scientific listing, fetched 2026-11-22)
5. Shah & London (1978): laminar flow in a square duct, Q = 0.03514 a^4 dp / (mu L)
6. Airgas/Linde argon 5.0 (UHP): O2 <= 1-2 ppm, H2O <= 1-3 ppm (seals.py source 9)
