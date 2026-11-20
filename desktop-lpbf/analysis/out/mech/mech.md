# Machine-element and heat-transfer checks (from `analysis/mech/mech_checks.py`)

## A. Z coupling: can the pot magnet pull the piston down?

| Force on the piston and rod (M50) | N |
|---|---|
| 2 × 2-114 rod O-rings, running (Parker Fig. 5-9, 75A, 17–26 % squeeze, oil basis) | 28–34–43 |
| same, dry or PFPE-greased in argon (×1.5) and after a dwell (break-out up to ×3.0) | up to 192 |
| bore seal (felt + PTFE scraper, 0.05–0.4 N/mm, assumed) | 8–64 |
| plate rim wiper (0.03–0.1 N/mm, assumed) | 5–16 |
| atmosphere on the rod at full vacuum (pushes it up) | 20 |
| piston + stack + 40 mm of powder (helps) | −4 |
| **pull needed to lower a layer, running** | **36–139** |
| **pull needed after a dwell (break-out)** | **262–331** |
| pot magnet 5679K95, rated on thick mild steel | 196 |
| same on a 430 SS striker at 68 °C with 0–0.05 mm of debris | **74–138** |

Margin (magnet / need): running 0.53–3.82; after a dwell 0.22–0.53. Below 1 the plate stays put while the arm drops, the magnet lets go, and the next layer is spread onto an unlowered plate.

## B. Recoater ball screw (12 × 10, fixed-supported, THK formulas)

Critical speed 14418 rpm vs 900 rpm at 150 mm/s (margin 13× at 80 %); buckling 9.3 kN vs ~15 N; DN 10800 (limit 70,000); L10 1.4e+12 rev ≈ 3.3e+10 layers. fatigue life is effectively unlimited at these loads; life is set by powder getting into the nut and rail.

## C. Screws, latches, hinges

Lid: the O-ring needs 205 N per screw and +20 mbar adds 6 N. Recommend 2500 N preload (2.5 N·m, K = 0.2); A4-70's 75 % of proof is 4792 N (4.8 N·m). Window ring: 6 × M3 at 0.04 N·m to a metal stop. 316 screws in 18-8 helical inserts gall; the lid and window screws sit outside the seal, so use anti-seize there, or silver-plated / Nitronic 60 screws.

- Door, 3.53 mm cord: each latch 801 N (rating 3558 N, SF 4.4); each hinge 613 N, Ø5 pin in double shear 16 MPa; squeeze lost 26 µm
- Door, 1.78 mm cord: each latch 410 N (rating 3558 N, SF 8.7); each hinge 314 N, Ø5 pin in double shear 8 MPa; squeeze lost 14 µm

## D. Chamber warm-up over a 10 h build (lumped; natural convection + radiation + argon loop)

Aluminium shell 12.8 kg; laser average 105 W (350 W × 30 % duty), all of it ending as heat in the chamber or module.

| Case | Heat in (W) | UA at the end (W/K) | Time constant (min) | Chamber after 10 h (°C) |
|---|---|---|---|---|
| bare outside, M50 heater 72 W | 177 | 3.5 | 54 | **73** |
| black-anodized outside | 177 | 4.7 | 41 | **61** |
| bare, L75 (92 W) | 197 | 3.6 | 54 | **78** |
| bare + water-cooled floor plate (UA 15 W/K) | 177 | 18.0 | 11 | **33** |

Affected: pot magnet (79 C rating) under the floor, camera and Pi HQ electronics (~50 C), load cell, inductive sensors (70 C), recoater servo, the module's spigot O-ring (84 C at a 60 C chamber), optics drift.

## E. Cover-slide thermal lens (beam radius on the slide 1.27 mm)

| Laser (W) | Absorption | Absorbed (W) | Focus shift (mm) | × Rayleigh range |
|---|---|---|---|---|
| 200 | 0.005 % | 0.010 | 0.2 | 0.0 |
| 200 | 0.050 % | 0.100 | 1.8 | 0.5 |
| 200 | 0.500 % | 1.000 | 17.5 | 4.7 |
| 350 | 0.005 % | 0.018 | 0.3 | 0.1 |
| 350 | 0.050 % | 0.175 | 3.1 | 0.8 |
| 350 | 0.500 % | 1.750 | 30.7 | 8.3 |
| 500 | 0.005 % | 0.025 | 0.4 | 0.1 |
| 500 | 0.050 % | 0.250 | 4.4 | 1.2 |
| 500 | 0.500 % | 2.500 | 43.8 | 11.9 |

Check: literature: -22 to -30 mm at 400 W with ~0.5 % absorption [6].

## F. Thermal drift of the optics over the warm-up

Chamber +50 K: bridge posts grow 70 µm; galvo offset drift ~239 µm at the plate. focus moves by the post growth (≪ the ±3.7 mm Rayleigh range); the galvo's offset drift is comparable to a hatch spacing over a warm-up, so calibrate warm or re-register on fiducials each few hours.

## Sources

1. Parker O-Ring Handbook ORD 5700, §5.11-5.14: F = fc Lr + fh Ar; Fig. 5-9 (fc vs compression and hardness), Fig. 5-10 (fh), break-out up to 3x running friction after a rest (§5.14.1)
2. THK ball screw technical data: critical speed N = lambda * d_r / L^2 * 1e7 (rpm), buckling P = eta * d_r^4 / L^2 * 1e4 (N), DN <= 70,000; L10 = (Ca / (fw Fa))^3 * 1e6 rev. https://tech.thk.com/en/products/pdf/en_b15_011.pdf
3. Shigley's Mechanical Engineering Design, 10th ed., Ch. 8 (T = K F d, K = 0.2 dry steel; A4-70 proof 450 MPa per ISO 3506-1)
4. Churchill & Chu (1975), Int. J. Heat Mass Transfer 18, 1323 (vertical plates); McAdams (1954) horizontal plates; emissivity of bare machined 6061 0.05-0.1, black anodize ~0.8 (Incropera, Fundamentals of Heat and Mass Transfer, App. A.11)
5. Thermal lens of an absorbing plate: dioptric power D = P_abs (dn/dT) / (2 pi k w^2) (thin plate, Gaussian beam; e.g. Koechner, Solid-State Laser Engineering, §7.1); fused silica k = 1.38 W/mK, dn/dT = 9.6e-6 /K at 1064 nm (Corning 7980 data sheet)
6. Focus shift of a measured 400 W system with a contaminated window: -22 to -30 mm (LiM 2017 contribution 31, https://www.wlt.de/lim/Proceedings2017/Data/PDF/Contribution31_final.pdf), as cited in low-profile.md
7. NdFeB reversible temperature coefficient of Br about -0.12 %/K (grade N42 data, e.g. Arnold Magnetic Technologies); McMaster 5679K95 pot magnet, 44 lbf, rated to 79 C (modules.md)
8. SCANLAB basiCube / hurrySCAN data sheets: long-term offset drift < 0.3 mrad over 8 h after warm-up, gain drift < 0.1 % over 8 h; temperature drift: offset < 30 urad/K, gain < 50 ppm/K (typical class values; check the purchased head)
