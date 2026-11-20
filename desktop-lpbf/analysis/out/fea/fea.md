# FEA summary (CalculiX 2.21, C3D10, from cad/lpbf_low.py)

Peak stresses at sharp re-entrant edges of the CAD (pocket floors, box-cut slots) are mesh-dependent; the 99.5th-percentile value is given where it matters. Machined parts get corner radii, which lower those peaks.

| Case | Material | Load | Max σ_vM (MPa), where | Max displacement | Criterion | Result |
|---|---|---|---|---|---|---|
| 1 Chamber body alone (open top), full vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm net + lid 4.7 kN + door 2.4 kN | 42.9 at (106, -75, 100); 99.5 %: 21.3 | 223.0 µm; door land Δy 208.7 µm, lid land Δz 78.9 µm | SF ≥ 2 yield, Goodman ≥ 2 | SF 6.4 yield, 2.6 vs welded HAZ (110 MPa), Goodman 3.4: pass |
| 1b Chamber body + lid bonded, full vacuum, as built in lpbf_low.py | 6061-T6 aluminium | as 1, lid included | 9.1 at (110, -85, 98); 99.5 %: 4.1 | 23.7 µm at (0, -28, 128); door land Δy 4.1 µm; window seat 23.6 µm | SF ≥ 2 yield, Goodman ≥ 2 | SF 30.2 yield, 12.0 vs HAZ, Goodman 16.1: pass |
| 2 Lid, vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm on top + window/dose/camera loads | 15.2 at (-30, -84, 120) | 28.0 µm; window seat sag 27.8 µm, tilt 8 µrad; camera port 17.0 µm | SF ≥ 2; sag ≪ ±3.7 mm Rayleigh range | SF 18: pass |
| 3 Door, vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm inside the O-ring | 8.0 at (4, -93, 108) | 6.5 µm | SF ≥ 2; latches at +50 mbar | SF 35; latch load 60 N each vs 3.6 kN rating: pass |
| 4 Recoater block + arm + blade holder (first layout) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | spread 10.2; hit 57.4 at (-112, 33, 14) | blade |uz| 17.2 µm (tip 17.2), |ux| 13.8 µm; over the plate Δuz 12.7 µm; hit |uz| 0 µm | < 5 µm spreading, no yield in a hit | FAIL (hit SF 4.8) |
| 4 Recoater block + arm + blade holder (as built in lpbf_low.py) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | spread 2.4; hit 14.5 at (-97, 33, 21) | blade |uz| 3.4 µm (tip 3.4), |ux| 1.7 µm; over the plate Δuz 2.5 µm; hit |uz| 0 µm | < 5 µm spreading, no yield in a hit | pass (hit SF 19.0) |
| 5 Z lift arm, as built in lpbf_low.py | 6061-T6 | 50 N down + 10 N side | 11.4 at (-0, -6, -110) | rod (0.1, -0.0, -3.0) µm | plate tilt < 10 µm over Ø50 | tilt 3.8 µm: pass |
| 6 Optics bridge + posts (first layout: 15 mm plate, 40x40x4 posts) | 6061-T6 | gravity + 4.8 kg of optics | 2.0 | lens bore sag 13.4 µm; f1–f6 = 79, 87, 140, 153, 318, 394 Hz | f1 > 100 Hz | FAIL |
| 6 Optics bridge + posts (as built in lpbf_low.py) | 6061-T6 | gravity + 4.8 kg of optics | 1.1 | lens bore sag 4.3 µm; f1–f6 = 133, 148, 235, 254, 499, 573 Hz | f1 > 100 Hz | pass |
| 7 Window Ø50.8 × 8 | UV fused silica | 1 atm, simply supported Ø48 | max principal 1.15 (Roark 1.08) | 0.73 µm | SF ≥ 6 vs 52.4 MPa | SF 45 (formula 46); 2.4 mm would do at SF 4, 2.9 mm at SF 6: pass |

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
