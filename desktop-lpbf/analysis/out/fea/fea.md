# FEA summary (CalculiX 2.21, C3D10, from cad/lpbf_low.py)

Peak stresses at sharp re-entrant edges of the CAD (pocket floors, box-cut slots) are mesh-dependent; the 99.5th-percentile value is given where it matters. Machined parts get corner radii, which lower those peaks.

| Case | Material | Load | Max σ_vM (MPa), where | Max displacement | Criterion | Result |
|---|---|---|---|---|---|---|
| 1 Chamber: frame + floor plate (bonded across the floor joint), open top, full vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm net + lid 5.9 kN + door 2.4 kN + module/plenum/funnel 1.2 kN under the floor | 54.4 at (-107, -95, 99); 99.5 %: 22.3 | 208.5 µm; door land Δy 194.1 µm, lid land Δz 83.8 µm; floor-joint σz -14.00..0.34 MPa | SF ≥ 2 yield, Goodman ≥ 2 | SF 5.1 yield, 2.0 vs welded HAZ (110 MPa), Goodman 2.7: pass |
| 1b Chamber: frame + floor plate + lid bonded, full vacuum, as built in lpbf_low.py | 6061-T6 aluminium | as 1, lid included | 28.0 at (60, 95, 8); 99.5 %: 9.6 | 62.7 µm at (2, -5, -2); door land Δy 4.3 µm; window seat 48.8 µm | SF ≥ 2 yield, Goodman ≥ 2 | SF 9.9 yield, 3.9 vs HAZ, Goodman 5.3: pass |
| 1b′ Same body at +20 mbar (argon working pressure) | 6061-T6 aluminium | the vacuum loads reversed × 0.002/0.1013 | 0.55 at (60, 95, 8) | 1.24 µm; door land Δy 0.08 µm | SF ≥ 2 | SF 500: pass |
| 2 Lid, vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm on top + window/dose/camera loads | 15.2 at (-30, -84, 120) | 28.0 µm; window seat sag 27.8 µm, tilt 8 µrad; camera port 17.0 µm | SF ≥ 2; sag ≪ ±3.7 mm Rayleigh range | SF 18: pass |
| 3 Door, vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm inside the O-ring | 7.2 at (2, -112, 1) | 5.3 µm | SF ≥ 2; latches at +50 mbar | SF 38; latch load 60 N each vs 3.6 kN rating: pass |
| 4 Recoater block + arm + blade holder (first layout) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | spread 10.2; hit 57.4 at (-112, 33, 14) | blade |uz| 17.2 µm (tip 17.2), |ux| 13.8 µm; over the plate Δuz 12.7 µm; hit |uz| 0 µm | < 5 µm spreading, no yield in a hit | FAIL (hit SF 4.8) |
| 4 Recoater block + arm + blade holder (as built in lpbf_low.py) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | spread 2.4; hit 14.5 at (-97, 33, 21) | blade |uz| 3.4 µm (tip 3.4), |ux| 1.7 µm; over the plate Δuz 2.5 µm; hit |uz| 0 µm | < 5 µm spreading, no yield in a hit | pass (hit SF 19.0) |
| 5 Z lift arm, as built in lpbf_low.py | 6061-T6 | 50 N down + 10 N side | 2.8 at (24, 55, -153) | rod (0.1, 0.5, -5.5) µm | plate tilt < 10 µm over Ø50 | tilt 7.0 µm: pass |
| 6 Optics bridge + posts (first layout: 15 mm plate, 40x40x4 posts) | 6061-T6 | gravity + 4.8 kg of optics | 2.0 | lens bore sag 13.4 µm; f1–f6 = 79, 87, 140, 153, 318, 394 Hz | f1 > 100 Hz | FAIL |
| 6 Optics bridge + posts (as built in lpbf_low.py) | 6061-T6 | gravity + 4.8 kg of optics | 1.1 | lens bore sag 4.3 µm; f1–f6 = 133, 148, 235, 254, 499, 573 Hz | f1 > 100 Hz | pass |
| 7 Window Ø50.8 × 8 | UV fused silica | 1 atm, simply supported Ø48 | max principal 1.18 (Roark 1.08) | 0.74 µm | SF ≥ 6 vs 52.4 MPa | SF 45 (formula 46); 2.4 mm would do at SF 4, 2.9 mm at SF 6: pass |

## 1f Floor-plate bolted joint (Shigley) and floor gland (Parker), as built in lpbf_low.py

18 x McMaster 92290A154 (M4 x 16, 316), tapped 6061; proof 210 MPa (A4-50 basis, conservative), preload 1383 N each at 1.11 N·m (K = 0.2); grip 8.1 mm, k_b 168 kN/mm, k_m 304 kN/mm (30° frustum), C = 0.356. Thread engagement 7.9 mm: strip 7.9 kN > screw break 4.2 kN. Total preload 24.9 kN on 30 cm² of lands = 8.3 MPa; head bearing 61 MPa.

| Case | Load on the joint (N) | Per screw (N) | Load factor n_L | Separation factor n_0 |
|---|---|---|---|---|
| nominal O-ring, +20 mbar | 4063 | 226 | 5.7 | 9.5 |
| O-ring at max squeeze, +50 mbar (relief valve +34) | 5366 | 298 | 4.3 | 7.2 |
| Parker 80A bar, +50 mbar | 9402 | 522 | 2.5 | 4.1 |
| Parker 80A bar, +0.5 bar regulator fault | 11952 | 664 | 2.0 | 3.2 |
| nominal O-ring, full vacuum | -1792 | -100 | – (joint pressed shut) | – (joint pressed shut) |

Floor gland: 3.53 mm FKM 75A cord, groove 2.65 deep × 4.6 wide (Parker face gland 2.57–2.72 × 4.5–4.75); squeeze 24.9 % (21.2–28.4 % at ±0.05 mm and cord tolerance); fill 80 % (max 88 % cold); path 947 mm; vulcanized cord, made to length: no stretch. O-ring force 4.0 kN nominal, 5.1 kN at max squeeze, 9.1 kN on Parker's 80A bar. pass.

Mode shapes (case 6): direction of the galvo's centre of mass in each mode, and where the largest motion is.
- first layout: 15 mm plate, 40x40x4 posts, mode 1: 79 Hz; galvo translates along [1.0, 0.03, 0.04] at 0.92 of the peak motion (tilt x 100 mm: 0.09); peak at [-116.0, -170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 2: 87 Hz; galvo translates along [-0.03, 1.0, 0.01] at 0.99 of the peak motion (tilt x 100 mm: 0.02); peak at [-64.0, -170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 3: 140 Hz; galvo translates along [0.05, 0.03, 1.0] at 0.67 of the peak motion (tilt x 100 mm: 0.31); peak at [-64.0, -170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 4: 153 Hz; galvo translates along [0.03, -0.94, 0.35] at 0.21 of the peak motion (tilt x 100 mm: 0.07); peak at [225.0, 170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 5: 318 Hz; galvo translates along [-0.21, -0.08, 0.98] at 0.27 of the peak motion (tilt x 100 mm: 0.42); peak at [-116.0, -170.0, 218.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 6: 394 Hz; galvo translates along [0.09, -0.56, -0.82] at 0.10 of the peak motion (tilt x 100 mm: 0.51); peak at [-25.0, 170.0, 218.0]
- as built in lpbf_low.py, mode 1: 133 Hz; galvo translates along [1.0, 0.03, 0.06] at 0.88 of the peak motion (tilt x 100 mm: 0.09); peak at [-116.0, -190.0, 233.0]
- as built in lpbf_low.py, mode 2: 148 Hz; galvo translates along [0.04, -1.0, 0.0] at 0.97 of the peak motion (tilt x 100 mm: 0.02); peak at [-64.0, -190.0, 233.0]
- as built in lpbf_low.py, mode 3: 235 Hz; galvo translates along [-0.0, -0.71, -0.7] at 0.25 of the peak motion (tilt x 100 mm: 0.11); peak at [245.0, -190.0, 233.0]
- as built in lpbf_low.py, mode 4: 254 Hz; galvo translates along [-0.08, 0.05, -1.0] at 0.67 of the peak motion (tilt x 100 mm: 0.29); peak at [-64.0, -190.0, 208.0]
- as built in lpbf_low.py, mode 5: 499 Hz; galvo translates along [-0.36, 0.15, 0.92] at 0.19 of the peak motion (tilt x 100 mm: 0.37); peak at [-64.0, -190.0, 208.0]
- as built in lpbf_low.py, mode 6: 573 Hz; galvo translates along [0.7, -0.46, -0.55] at 0.21 of the peak motion (tilt x 100 mm: 0.40); peak at [-116.0, -190.0, 233.0]
