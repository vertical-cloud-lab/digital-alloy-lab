# FEA summary (CalculiX 2.21, C3D10, from cad/lpbf_low.py)

Peak stresses at sharp re-entrant edges of the CAD (pocket floors, box-cut slots) are mesh-dependent; the 99.5th-percentile value is given where it matters. Machined parts get corner radii, which lower those peaks.

| Case | Material | Load | Max σ_vM (MPa), where | Max displacement | Criterion | Result |
|---|---|---|---|---|---|---|
| 1 Chamber: frame + floor plate (bonded across the floor joint), open top, full vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm net + lid 5.9 kN + door 2.4 kN + module/plenum/funnel 1.2 kN under the floor | 54.4 at (-107, -95, 99); 99.5 %: 22.3 | 208.5 µm; door land Δy 194.1 µm, lid land Δz 83.8 µm; floor-joint σz -14.00..0.34 MPa | SF ≥ 2 yield, Goodman ≥ 2 | SF 5.1 yield, 2.0 vs welded HAZ (110 MPa), Goodman 2.7: pass |
| 1b Chamber: frame + floor plate + lid bonded, full vacuum, as built in lpbf_low.py | 6061-T6 aluminium | as 1, lid included | 28.0 at (60, 95, 8); 99.5 %: 9.6 | 62.7 µm at (2, -5, -2); door land Δy 4.3 µm; window seat 48.8 µm | SF ≥ 2 yield, Goodman ≥ 2 | SF 9.9 yield, 3.9 vs HAZ, Goodman 5.3: pass |
| 1b′ Same body at +20 mbar (argon working pressure) | 6061-T6 aluminium | the vacuum loads reversed × 0.002/0.1013 | 0.55 at (60, 95, 8) | 1.24 µm; door land Δy 0.08 µm | SF ≥ 2 | SF 500: pass |
| 2 Lid, vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm on top + window/dose/camera loads | 47.3 at (-45, -107, 120) | 68.0 µm; window seat sag 67.6 µm, tilt 156 µrad; camera port 35.6 µm | SF ≥ 2; sag ≪ ±3.7 mm Rayleigh range | SF 6: pass |
| 3 Door, vacuum, as built in lpbf_low.py | 6061-T6 aluminium | 1 atm inside the O-ring | 7.2 at (2, -112, 1) | 5.3 µm | SF ≥ 2; latches at +50 mbar | SF 38; latch load 60 N each vs 3.6 kN rating: pass |
| 4 Recoater block + arm + blade holder (first layout) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | spread 13.1; hit 75.1 at (-112, 33, 14) | blade |uz| 28.1 µm (tip 28.1), |ux| 23.5 µm; over the plate Δuz 15.7 µm; hit |uz| 1 µm | < 5 µm spreading, no yield in a hit | FAIL (hit SF 3.7) |
| 4 Recoater block + arm + blade holder (as built in lpbf_low.py) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | spread 2.1; hit 11.4 at (-97, 53, 33) | blade |uz| 5.1 µm (tip 4.9), |ux| 2.9 µm; over the plate Δuz 2.4 µm; hit |uz| 0 µm | < 5 µm spreading, no yield in a hit | FAIL (hit SF 24.1) |
| 5 Z lift arm, as built in lpbf_low.py | 6061-T6 | 50 N down + 10 N side | 2.8 at (24, 55, -153) | rod (0.1, 0.5, -5.5) µm | plate tilt < 10 µm over Ø50 | tilt 7.0 µm: pass |
| 6 Optics bridge + posts (first layout: 15 mm plate, 40x40x4 posts) | 6061-T6 | gravity + 4.8 kg of optics | 1.7 | lens bore sag 13.2 µm; f1–f6 = 79, 87, 141, 154, 321, 397 Hz | f1 > 100 Hz | FAIL |
| 6 Optics bridge + posts (as built in lpbf_low.py) | 6061-T6 | gravity + 4.8 kg of optics | 0.9 | lens bore sag 4.4 µm; f1–f6 = 134, 150, 235, 253, 488, 536 Hz | f1 > 100 Hz | pass |
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

## How each case was run

Since 2026-11-22 every case records when it ran, on which commit of the model, its mesh and its solver (SPOOLES up to 60,000 nodes, ccx's ITERATIVE CHOLESKY above; the bridge on a coarser mesh so that its modes can use SPOOLES; see the script's docstring). Cases without a record ran earlier, on the model of their day.

| Case | Run (UTC) | Model commit | Nodes | Solver |
|---|---|---|---|---|
| 1 | before 2026-11-22 (not recorded) | – | 139,613 | ITERATIVE CHOLESKY |
| 1b | before 2026-11-22 (not recorded) | – | 284,108 | ITERATIVE CHOLESKY |
| 2 | 2026-11-22 06:16 | 9f45d80 | 265,140 | ITERATIVE CHOLESKY |
| 3 | before 2026-11-22 (not recorded) | – | 39,920 | SPOOLES |
| 4 (as built in lpbf_low.py) | 2026-11-22 06:45 | 9f45d80 | 300,172 | ITERATIVE CHOLESKY |
| 4 (first layout) | 2026-11-22 06:33 | 9f45d80 | 114,961 | ITERATIVE CHOLESKY |
| 5 | before 2026-11-22 (not recorded) | – | 16,985 | SPOOLES |
| 6 (as built in lpbf_low.py) | 2026-11-22 06:04 | 9f45d80 | 131,318, hmax 10 mm | SPOOLES (gravity), SPOOLES (modes) |
| 6 (first layout: 15 mm plate, 40x40x4 posts) | 2026-11-22 06:01 | 9f45d80 | 63,484, hmax 10 mm | SPOOLES (gravity), SPOOLES (modes) |
| 7 | before 2026-11-22 (not recorded) | – | 16,253 | SPOOLES |

### Checks of the solver and mesh settings

- Solver, 2026-11-22, model 9f45d80, the same mesh solved twice. Door (case 3, 39,950 nodes), SPOOLES / ITERATIVE CHOLESKY: peak von Mises 6.883 / 6.882 MPa (−0.01 %), max displacement 5.278 µm in both. Z lift arm (case 5, 16,887 nodes): peak 2.953 / 2.898 MPa (−1.9 %), max displacement +0.07 %, plate tilt 7.027 / 7.025 µm. Re-meshing moves a peak more than the solver does: the door's peak was 7.18 MPa on the 2026-11-21 mesh (39,920 nodes) of the same part.
- Bridge mesh, case 6a on 9f45d80. Old mesh (hmax 7, 141,517 nodes): f1–f6 = 78.5, 86.8, 140.0, 153.2, 318.7, 395.1 Hz, lens bore sag 13.4 µm. New mesh (hmax 10, 63,484 nodes): 78.7, 87.0, 141.2, 153.6, 320.7, 397.5 Hz (+0.2 to +0.9 %), 13.2 µm. On the old mesh the gravity step took 19 min with ITERATIVE CHOLESKY (the rigid masses slow PCG down); on the new one, 13 s with SPOOLES.
- Memory, peak of the whole run under a 4.5 GB cap: lid 1.5 GB with ITERATIVE CHOLESKY (with SPOOLES it passed 4.2 GB and was killed); bridge 3.5 GB (SPOOLES, 6b's modes on 131,318 nodes); recoater 1.5 GB with ITERATIVE CHOLESKY (SPOOLES on 4a's 115,000 nodes passed 4.4 GB and was killed).

### What changed against the previous results

- The old results for cases 2, 4 and 6 date from 2026-11-17 (78afc86). Since then the chamber has grown 40 mm in y (inner half-width iy 75 → 95 mm, so the lid is 222 mm across, was 182), the dose slot and the blade have grown from ±30 to ±50 mm (dose_y), and joints.py has cut the screw and insert holes. This run (cases 2, 4 and 6) used the model at commit 9f45d80 (9f45d80745b77afb2c7b884fde5d0b435439105d), from a separate worktree, while the model was being edited.
- Lid (case 2): window-seat sag 27.8 → 67.6 µm, peak 15.2 → 47.3 MPa (SF 18 → 5.8), 99.5th percentile 7.2 → 15.7 MPa, seat tilt 8 → 156 µrad, camera port 17.0 → 35.6 µm. Mostly the wider lid: its span between the sealing lands grew from ~164 to ~204 mm in y, and a plate's sag grows as about the fourth power of its short span (×2.4). The cover-slide drawer slot, added after the old run, leaves two 5 mm skins from the front edge to y = +35 mm, past the window bore: it tilts the seat, and the peak sits on the top face at the slot's front corner, beside the drawer-latch receptacle. Still a pass: SF ≥ 2, the sag is far inside the ±3.7 mm Rayleigh range, and tilting an 8 mm window by 156 µrad shifts the beam ~0.4 µm.
- Recoater (case 4), as built: blade |uz| 3.4 → 5.1 µm (tip 4.9), |ux| 1.7 → 2.9 µm, so it is now just over the 5 µm criterion and the table says FAIL. The blade holder is 114 mm long (was 74), because the blade now spans ±50 mm, though 31 mm deep (was 19). Hit peak 14.5 → 11.4 MPa (SF 24). The first layout, rebuilt from today's parameters (a 94 mm holder), went 17.2 → 28.1 µm.
- Bridge (case 6b): modes 1–4 unchanged within 1 % (133 → 134, 148 → 150, 235 → 235, 254 → 253 Hz). Modes 5–6 dropped from 499 to 488 Hz and from 573 to 536 Hz. The posts have gained welded end caps and M6 screw holes since the old run. The coarser mesh raises 6a's modes 5–6 by 0.6 %, so the drop is not the mesh. Lens bore sag 4.3 → 4.4 µm.

Mode shapes (case 6): direction of the galvo's centre of mass in each mode, and where the largest motion is.
- first layout: 15 mm plate, 40x40x4 posts, mode 1: 79 Hz; galvo translates along [-1.0, -0.03, -0.04] at 0.92 of the peak motion (tilt x 100 mm: 0.09); peak at [-116.0, -170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 2: 87 Hz; galvo translates along [0.03, -1.0, -0.01] at 0.99 of the peak motion (tilt x 100 mm: 0.02); peak at [-64.0, -170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 3: 141 Hz; galvo translates along [0.05, 0.04, 1.0] at 0.66 of the peak motion (tilt x 100 mm: 0.31); peak at [-64.0, -170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 4: 154 Hz; galvo translates along [-0.05, 0.92, -0.4] at 0.21 of the peak motion (tilt x 100 mm: 0.07); peak at [225.0, 170.0, 233.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 5: 321 Hz; galvo translates along [-0.2, -0.09, 0.98] at 0.26 of the peak motion (tilt x 100 mm: 0.43); peak at [-64.0, -170.0, 218.0]
- first layout: 15 mm plate, 40x40x4 posts, mode 6: 397 Hz; galvo translates along [0.08, -0.49, -0.87] at 0.11 of the peak motion (tilt x 100 mm: 0.50); peak at [-25.0, 170.0, 218.0]
- as built in lpbf_low.py, mode 1: 134 Hz; galvo translates along [-1.0, -0.03, -0.08] at 0.88 of the peak motion (tilt x 100 mm: 0.09); peak at [-118.0, -190.0, 233.0]
- as built in lpbf_low.py, mode 2: 150 Hz; galvo translates along [-0.05, 1.0, -0.01] at 0.97 of the peak motion (tilt x 100 mm: 0.02); peak at [-62.0, -190.0, 233.0]
- as built in lpbf_low.py, mode 3: 235 Hz; galvo translates along [0.0, -0.65, -0.76] at 0.28 of the peak motion (tilt x 100 mm: 0.13); peak at [245.0, -190.0, 233.0]
- as built in lpbf_low.py, mode 4: 253 Hz; galvo translates along [0.08, -0.06, 1.0] at 0.67 of the peak motion (tilt x 100 mm: 0.30); peak at [-62.0, -190.0, 208.0]
- as built in lpbf_low.py, mode 5: 488 Hz; galvo translates along [0.47, -0.22, -0.86] at 0.24 of the peak motion (tilt x 100 mm: 0.35); peak at [-62.0, -190.0, 208.0]
- as built in lpbf_low.py, mode 6: 536 Hz; galvo translates along [0.83, -0.56, -0.0] at 0.22 of the peak motion (tilt x 100 mm: 0.33); peak at [-62.0, -190.0, 208.0]
