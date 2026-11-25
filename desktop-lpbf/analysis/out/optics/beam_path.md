# Beam path, end to end (`analysis/optics/beam_path.py`)

500 W, 1070 nm, M² 1.05 typ / 1.1 max; f = 160 mm; fused silica n = 1.4496 at 1070 nm. Paraxial: no lens prescription is used.

## B. Collimator → spot (bare-fibre divergence 140 mrad; range 130–150 mrad in brackets)

| Collimator | f_c (mm) | D (mm) | Spot, M² 1.05 / 1.1 (µm) | Rayleigh range ±z_R (mm) | ±5 % / ±10 % spot growth (mm) | Spot at f = 254 (µm) | Galvo Ø20 clip |
|---|---|---|---|---|---|---|---|
| IPG affixed 2.5 mm (drawn from 2026-11-23; YLR series datasheet rev 2/26) | 17.9 | 2.50 | 92 / 96 [92–96] | 6.14 | 1.97 / 2.81 | 152 | 2.6e-56 |
| IPG 2.5 mm + Sill S6EXK0012-328 1.2x expander (catalogue, no power rating) | 21.4 | 3.00 | 76 / 80 [76–80] | 4.26 | 1.36 / 1.95 | 127 | 2.5e-39 |
| D = 3.2 mm (the ~75 um target; f_c ~ 23 mm: no catalogue part found) | 22.9 | 3.20 | 72 / 75 [72–75] | 3.75 | 1.20 / 1.72 | 119 | 1.2e-34 |
| Wavelength COL-1070-D25-F30 (QBH, f = 30 mm; also low-profile.md's label) | 30.0 | 4.20 | 54 / 57 [51–61] | 2.17 | 0.70 / 1.00 | 91 | 2.0e-20 |
| IPG standard, 5 mm beam (drawn until 2026-11-22) | 35.7 | 5.00 | 46 / 48 [46–48] | 1.53 | 0.49 / 0.70 | 76 | 1.3e-14 |
| IPG standard, 7.5 mm beam | 53.6 | 7.50 | 31 / 32 [31–32] | 0.68 | 0.22 / 0.31 | 51 | 6.7e-07 |

Collimated beam needed for a given spot at f = 160 mm (M² 1.1): 60 µm → D 4.00 mm, f_c 28.5 mm (26.6–30.7); 70 µm → D 3.43 mm, f_c 24.5 mm (22.8–26.3); 75 µm → D 3.20 mm, f_c 22.8 mm (21.3–24.6); 80 µm → D 3.00 mm, f_c 21.4 mm (20.0–23.1); 90 µm → D 2.66 mm, f_c 19.0 mm (17.8–20.5); 100 µm → D 2.40 mm, f_c 17.1 mm (16.0–18.4)

Fibre: the divergence spec implies a 10.2 µm beam diameter at the fibre end (9.5–11.0 µm).

## C. Where the focus lands

The 9.53 mm window (Edmund 38-990) and 2.0 mm slide (Edmund 36-299), drawn as the BOM parts since 2026-11-25, push the focus down by **3.58 mm** (the 8 mm window and 3 mm slide drawn before gave 3.41 mm). The model raises the lens by 3.58 mm (lens output end z 186.08), so the focus lands at z = +0.004 mm. The extra 0.17 mm comes out of the shim stack (2.83 mm nominal, was 3.00), so the bridge does not move; 0–6 mm of shims moves the lens 2.83 mm up (no shims) to 3.17 mm down. Spot on the powder plane as drawn, and if the lens had not been raised (M² 1.1, 140 mrad):

- IPG affixed 2.5 mm (drawn from 2026-11-23; YLR series datasheet rev 2/26): 96 µm at focus, **96 µm on the powder** (before: 111 µm, 0.6 z_R out)
- IPG 2.5 mm + Sill S6EXK0012-328 1.2x expander (catalogue, no power rating): 80 µm at focus, **80 µm on the powder** (before: 104 µm, 0.8 z_R out)
- D = 3.2 mm (the ~75 um target; f_c ~ 23 mm: no catalogue part found): 75 µm at focus, **75 µm on the powder** (before: 104 µm, 1.0 z_R out)
- Wavelength COL-1070-D25-F30 (QBH, f = 30 mm; also low-profile.md's label): 57 µm at focus, **57 µm on the powder** (before: 110 µm, 1.6 z_R out)
- IPG standard, 5 mm beam (drawn until 2026-11-22): 48 µm at focus, **48 µm on the powder** (before: 122 µm, 2.3 z_R out)
- IPG standard, 7.5 mm beam: 32 µm at focus, **32 µm on the powder** (before: 171 µm, 5.2 z_R out)

| Focus budget item | mm | kind |
|---|---|---|
| window 9.53 mm + slide 2.0 mm of fused silica in the converging beam (static; take out by raising the lens) | 3.576 | static |
| cover slide thickness tolerance +0.15/-0.00 mm (Edmund 36-299): focus up to this much lower | 0.047 | per slide |
| window thickness tolerance +/-0.20 mm (Edmund 38-990) | 0.062 | once (the burn test takes it out) |
| plate stack growth at 200 C (powder-spreading.md), if the blade is zeroed cold | 0.112 | zero the blade hot |
| bridge posts +50 K (mech.md F) | 0.070 | slow drift |

## D/E. Field geometry (k = chief-ray angle at the plate / optical scan angle; not published for the FTH160-1064)

| k | Plate | r (mm) | Scan, optical (°) | Mirror (°) | AOI (°) | Elongation (%) | Plate lateral shift (mm) | Extra focus shift (mm) | Astigmatism (mm) | Chief ray r at slide / window / lens out (mm) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.3 | S25 | 12.7 | 4.5 | 2.3 | 1.4 | 0.03 | 0.085 | 0.000 | 0.002 | 9.7 / 9.1 / 8.3 |
| 0.3 | M50 | 25.4 | 9.1 | 4.5 | 2.7 | 0.11 | 0.170 | 0.001 | 0.009 | 19.3 / 18.2 / 16.5 |
| 0.3 | L75 | 38.1 | 13.6 | 6.8 | 4.1 | 0.26 | 0.256 | 0.002 | 0.021 | 28.9 / 27.3 / 24.8 |
| 0.5 | S25 | 12.7 | 4.5 | 2.3 | 2.3 | 0.08 | 0.142 | 0.000 | 0.007 | 7.6 / 6.7 / 5.3 |
| 0.5 | M50 | 25.4 | 9.1 | 4.5 | 4.5 | 0.32 | 0.285 | 0.002 | 0.026 | 15.2 / 13.4 / 10.6 |
| 0.5 | L75 | 38.1 | 13.6 | 6.8 | 6.8 | 0.71 | 0.428 | 0.004 | 0.059 | 22.8 / 20.0 / 15.8 |
| 0.75 | S25 | 12.7 | 4.5 | 2.3 | 3.4 | 0.18 | 0.213 | 0.001 | 0.015 | 5.1 / 3.7 / 1.6 |
| 0.75 | M50 | 25.4 | 9.1 | 4.5 | 6.8 | 0.71 | 0.428 | 0.004 | 0.059 | 10.1 / 7.3 / 3.1 |
| 0.75 | L75 | 38.1 | 13.6 | 6.8 | 10.2 | 1.62 | 0.647 | 0.009 | 0.135 | 15.0 / 10.8 / 4.5 |

Thin-lens estimate of k (lens at H', z 163.6; stop at the 2nd mirror, z 271.1): exit pupil 328 mm above the lens, k = 0.33. The lens's real principal planes are not published, so the tables span k = 0.3-0.75.


k from a thin lens with its front principal plane between the lens body's middle and H' (z 160): as drawn (2nd mirror 35 mm above the nose): 0.33-0.63; before 2026-11-23 (2nd mirror 40 mm above the nose): 0.30-0.59; Thorlabs A1 = 7.5 mm (2nd mirror 7.5 mm above the nose): 0.50-0.80

Clear diameter each lid opening needs to pass the L75 edge (r 38.1 mm) with < 0.1 % clipped (mm):

| Beam | k | lid bore (drawn Ø56) | drawer opening (drawn Ø46) | cover slide clear aperture (drawn Ø42) | field stop (drawn Ø36) | window flange bore (below window) (drawn Ø42) | window clear aperture (drawn Ø46) | window retaining ring (above window) (drawn Ø44) |
|---|---|---|---|---|---|---|---|---|
| 5.0 mm | 0.3 | 64.9 | 64.4 | 64.2 | 63.8 | 63.3 | 62.4 | 61.4 |
| 5.0 mm | 0.45 | 56.2 | 55.3 | 55.1 | 54.4 | 53.6 | 51.8 | 50.1 |
| 5.0 mm | 0.6 | 47.5 | 46.3 | 45.9 | 44.9 | 43.7 | 41.2 | 38.8 |
| 3.2 mm | 0.3 | 62.8 | 62.2 | 62.0 | 61.5 | 61.0 | 59.8 | 58.6 |
| 3.2 mm | 0.45 | 54.1 | 53.2 | 52.8 | 52.1 | 51.2 | 49.3 | 47.4 |
| 3.2 mm | 0.6 | 45.4 | 44.1 | 43.6 | 42.6 | 41.3 | 38.6 | 36.0 |

Largest plate radius each lid aperture passes with < 0.1 % clipped (mm; plates are 12.7 / 25.4 / 38.1):

| Collimator | k | lid bore Ø56 | drawer opening Ø46 | cover slide clear aperture Ø42 | field stop Ø36 | window flange bore (below window) Ø42 | window clear aperture Ø46 | window retaining ring (above window) Ø44 | field stop, 50 % reach |
|---|---|---|---|---|---|---|---|---|---|
| IPG 2.5 mm (drawn) | 0.3 | 34.3 | 28.1 | 25.9 | 21.8 | 26.0 | 29.1 | 28.5 | 23.9 |
| IPG 2.5 mm (drawn) | 0.5 | 42.6 | 35.4 | 32.8 | 27.8 | 33.7 | 39.0 | 39.6 | 30.5 |
| IPG 2.5 mm (drawn) | 0.75 | 60.0 | 53.6 | 50.0 | 43.4 | 55.5 | 60.0 | 60.0 | 48.0 |
| IPG 5 mm | 0.3 | 32.4 | 26.1 | 23.9 | 19.7 | 23.8 | 26.6 | 25.8 | 23.9 |
| IPG 5 mm | 0.5 | 40.3 | 32.9 | 30.2 | 25.1 | 30.9 | 35.7 | 35.8 | 30.5 |
| IPG 5 mm | 0.75 | 59.1 | 49.5 | 45.8 | 39.0 | 50.3 | 60.0 | 60.0 | 48.0 |
| D 3.2 mm | 0.3 | 33.7 | 27.5 | 25.3 | 21.2 | 25.4 | 28.4 | 27.7 | 23.9 |
| D 3.2 mm | 0.5 | 42.0 | 34.7 | 32.0 | 27.1 | 32.9 | 38.1 | 38.5 | 30.5 |
| D 3.2 mm | 0.75 | 60.0 | 52.4 | 48.8 | 42.2 | 54.0 | 60.0 | 60.0 | 48.0 |

L75 reach as drawn (k over the drawn thin-lens range; the opening that limits it; < 0.1 % clipped):

| Collimator | k | Reach (mm) | Limited by | L75 (38.1) | M50 (25.4) |
|---|---|---|---|---|---|
| IPG 2.5 mm (drawn) | 0.33 | 22.4 | field stop | no | no |
| IPG 2.5 mm (drawn) | 0.48 | 27.0 | field stop | no | yes |
| IPG 2.5 mm (drawn) | 0.63 | 33.8 | field stop | no | yes |
| D 3.2 mm | 0.33 | 21.8 | field stop | no | no |
| D 3.2 mm | 0.48 | 26.2 | field stop | no | yes |
| D 3.2 mm | 0.63 | 32.9 | field stop | no | yes |
| IPG 5 mm | 0.33 | 20.3 | field stop | no | no |
| IPG 5 mm | 0.48 | 24.3 | field stop | no | no |
| IPG 5 mm | 0.63 | 30.5 | field stop | no | yes |

## F. Irradiance at 500 W (lens refocused onto the plate)

**IPG 5 mm, M2 1.1**

| Surface | Beam Ø (mm) | Peak (W/cm²) | P/D (W/cm) | Note |
|---|---|---|---|---|
| collimator output lens | 5.000 | 5.09e+03 | 1e+03 |  |
| shutter mirror / dump (closed) | 5.000 | 5.09e+03 | 1e+03 | the dump takes all 500 W |
| galvo mirrors (45 deg: the footprint is 1.41x longer, so the surface irradiance is 0.71x this) | 5.000 | 5.09e+03 | 1e+03 |  |
| f-theta input | 5.000 | 5.09e+03 | 1e+03 |  |
| f-theta output (protective window, z 186.1) | 5.703 | 3.91e+03 | 877 |  |
| chamber window, top (z 156.0) | 4.763 | 5.61e+03 | 1.05e+03 |  |
| chamber window, bottom (z 146.5) | 4.558 | 6.13e+03 | 1.1e+03 |  |
| cover slide, top (z 129.0) | 4.012 | 7.91e+03 | 1.25e+03 |  |
| cover slide, bottom (z 127.0) | 3.969 | 8.08e+03 | 1.26e+03 | the face that fouls |
| plate, at focus | 0.048 | 5.54e+07 | 1.04e+05 | melts |

**D 3.2 mm, M2 1.1**

| Surface | Beam Ø (mm) | Peak (W/cm²) | P/D (W/cm) | Note |
|---|---|---|---|---|
| collimator output lens | 3.200 | 1.24e+04 | 1.56e+03 |  |
| shutter mirror / dump (closed) | 3.200 | 1.24e+04 | 1.56e+03 | the dump takes all 500 W |
| galvo mirrors (45 deg: the footprint is 1.41x longer, so the surface irradiance is 0.71x this) | 3.200 | 1.24e+04 | 1.56e+03 |  |
| f-theta input | 3.200 | 1.24e+04 | 1.56e+03 |  |
| f-theta output (protective window, z 186.1) | 3.651 | 9.55e+03 | 1.37e+03 |  |
| chamber window, top (z 156.0) | 3.049 | 1.37e+04 | 1.64e+03 |  |
| chamber window, bottom (z 146.5) | 2.918 | 1.5e+04 | 1.71e+03 |  |
| cover slide, top (z 129.0) | 2.569 | 1.93e+04 | 1.95e+03 |  |
| cover slide, bottom (z 127.0) | 2.541 | 1.97e+04 | 1.97e+03 | the face that fouls |
| plate, at focus | 0.075 | 2.27e+07 | 6.67e+04 | melts |

## G. Back-reflection

Uncoated fused silica reflects 3.37 % per face; a good AR coat ~0.25 %.

| D (mm) | Surface | Height (air-equiv., mm) | Core coupling | Into the core, uncoated / AR (W) | Back toward the head, uncoated / AR (W) | Ghost focus z (thin lens) | Return focus from fibre end (mm) / radius there (mm) |
|---|---|---|---|---|---|---|---|
| 5.0 | slide bottom | 127.0 | 1.5e-04 | 0.002 / 0.0002 | 16.8 / 1.25 | 219 | 12.7 / 0.89 |
| 5.0 | slide top | 128.4 | 1.4e-04 | 0.002 / 0.0002 | 16.8 / 1.25 | 220 | 12.8 / 0.90 |
| 5.0 | window bottom | 145.8 | 1.1e-04 | 0.002 / 0.0001 | 16.8 / 1.25 | 232 | 14.5 / 1.02 |
| 5.0 | window top | 152.4 | 1.0e-04 | 0.002 / 0.0001 | 16.8 / 1.25 | 236 | 15.2 / 1.06 |
| 5.0 | f-theta protective window (lower face) | 182.5 | 7.1e-05 | 0.001 / 0.0001 | 16.8 / 1.25 | 250 | 18.2 / 1.27 |
| 3.2 | slide bottom | 127.0 | 8.7e-04 | 0.015 / 0.0011 | 16.8 / 1.25 | 219 | 5.2 / 0.36 |
| 3.2 | slide top | 128.4 | 8.5e-04 | 0.014 / 0.0011 | 16.8 / 1.25 | 220 | 5.2 / 0.37 |
| 3.2 | window bottom | 145.8 | 6.6e-04 | 0.011 / 0.0008 | 16.8 / 1.25 | 232 | 6.0 / 0.42 |
| 3.2 | window top | 152.4 | 6.0e-04 | 0.010 / 0.0008 | 16.8 / 1.25 | 236 | 6.2 / 0.44 |
| 3.2 | f-theta protective window (lower face) | 182.5 | 4.2e-04 | 0.007 / 0.0005 | 16.8 / 1.25 | 250 | 7.4 / 0.52 |

Flat specular melt pool or bare plate at focus (cat's eye), R 0.9, optics T 0.98 (W back into the core):

| D (mm) | k | r = 0 | 1 | 2 | 3 | 5 | 8 | 12.7 | 25.4 mm |
|---|---|---|---|---|---|---|---|---|---|
| 5.0 | 0.3 | 441 | 416 | 350 | 263 | 104 | 11.1 | 0.0407 | 3.2e-14 |
| 5.0 | 0.5 | 441 | 376 | 233 | 104 | 8.08 | 0.0157 | 2.73e-09 | 6.52e-43 |
| 5.0 | 0.75 | 441 | 308 | 104 | 17.3 | 0.0544 | 4.35e-08 | 2.68e-23 | 5.97e-99 |
| 3.2 | 0.3 | 441 | 383 | 251 | 124 | 13.1 | 0.0544 | 6.22e-08 | 1.75e-37 |
| 3.2 | 0.5 | 441 | 298 | 92.4 | 13.1 | 0.0253 | 6.12e-09 | 1.92e-25 | 1.57e-107 |
| 3.2 | 0.75 | 441 | 183 | 13.1 | 0.162 | 1.26e-07 | 1.64e-22 | 1.2e-59 | 2.42e-244 |

## H. Safety optics (MPE 5 mW/cm², as safety_calcs.py)

| D (mm) | Collimated φ (mrad) | NOHD collimated (km) | Through f-theta φ (mrad) | NOHD from focus (m) | NOHD specular Al (m) |
|---|---|---|---|---|---|
| 5.0 | 0.300 | 11.9 | 31.2 | 114 | 108 |
| 3.2 | 0.468 | 7.6 | 20.0 | 178 | 169 |

Bare fibre: NOHD 25.5 m (140 mrad), 27.4 m (130 mrad). Eyewear for the direct beam: OD ≥ 5.4.

Guard, 1.6 mm 5052, 1-D lower bound on burn-through (391 J/cm², no conduction):

| D (mm) | From focus (mm) | Beam Ø (mm) | I (W/cm²) | t at absorptance 0.08 / 0.4 (s) |
|---|---|---|---|---|
| 5.0 | 50 | 1.56 | 2.25e+04 | 0.22 / 0.04 |
| 5.0 | 150 | 4.69 | 2.51e+03 | 1.95 / 0.39 |
| 5.0 | 300 | 9.38 | 627 | 7.81 / 1.56 |
| 5.0 | 600 | 18.75 | 157 | 31.24 / 6.25 |
| 3.2 | 50 | 1.00 | 5.48e+04 | 0.09 / 0.02 |
| 3.2 | 150 | 3.00 | 6.11e+03 | 0.80 / 0.16 |
| 3.2 | 300 | 6.00 | 1.53e+03 | 3.20 / 0.64 |
| 3.2 | 600 | 12.00 | 382 | 12.79 / 2.56 |

## I. Collimator choice: what each option does to the process (optics.md §9.1)

Baseline with a known Al window: EOS M 290 / M 280, AlSi10Mg 30 um, 100 µm, 370 W, 1300 mm/s, hatch 0.19 mm (peak 9.4 MW/cm²). Ke ratio = keyhole number (Gan et al. 2021) over the baseline's, at 1.1 m/s (the basiCube 20's marking speed); it scales as P/√(V r³). Hatch = 1.9 × spot (the baseline's ratio, assumed). Screening build: three 10 × 10 mm coupons, 15 mm at 30 µm, 8 s recoat, run at the power that matches the baseline's Ke. M² 1.1, 140 mrad.

| Option | D (mm) | Spot on powder (µm) | z_R (mm) | ±10 % band (mm) | 0.112 mm plate growth | Spot after a ±1 mm focus error | Light-film thermal shift | Peak at 350 W (MW/cm², × baseline) | Ke × baseline at 350 / 500 W | Power for the baseline's Ke at 1.1 m/s (W) | Hatch (mm) | Rate (mm³/s) | 15 mm screening build (min) | P/D on the optics at 500 W (kW/cm) | Cat's eye < 10 W beyond r (mm) | Field-stop reach, k 0.48 (mm) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IPG 5 mm affixed (in the quote; drawn until 2026-11-22) | 5.00 | 48 | 1.53 | ±0.70 | +0.3 % | 57–57 µm | 1.1 mm → 59 µm | 38.8 (4.11×) | 3.10 / 4.42 | 113 | 0.091 | 3.0 | 93 (scan 29 %) | 1.00 | 5.1 | 24.3 |
| Wavelength COL-1070-D25-F30 (QBH, f 30 mm) | 4.20 | 57 | 2.17 | ±1.00 | +0.1 % | 63–63 µm | 1.6 mm → 71 µm | 27.3 (2.90×) | 2.38 / 3.41 | 147 | 0.108 | 3.6 | 89 (scan 25 %) | 1.19 | 4.3 | 25.2 |
| custom collimator, f ~ 23 mm (D 3.2 mm) | 3.20 | 75 | 3.75 | ±1.72 | +0.0 % | 78–78 µm | 2.7 mm → 93 µm | 15.9 (1.68×) | 1.59 / 2.26 | 221 | 0.142 | 4.7 | 84 (scan 21 %) | 1.56 | 3.3 | 26.2 |
| IPG 5 mm + 1.5x Galilean expander used backwards (D 3.33 mm) | 3.33 | 72 | 3.45 | ±1.58 | +0.1 % | 75–75 µm | 2.5 mm → 89 µm | 17.2 (1.83×) | 1.69 / 2.41 | 208 | 0.137 | 4.5 | 85 (scan 22 %) | 1.50 | 3.4 | 26.1 |
| IPG 2.5 mm + Sill 1.2x expander (D 3.0 mm) | 3.00 | 80 | 4.26 | ±1.95 | +0.0 % | 82–82 µm | 3.1 mm → 99 µm | 14.0 (1.48×) | 1.44 / 2.06 | 243 | 0.152 | 5.0 | 83 (scan 20 %) | 1.67 | 3.1 | 26.4 |
| IPG 2.5 mm affixed (drawn since 2026-11-23) | 2.50 | 96 | 6.14 | ±2.81 | +0.0 % | 97–97 µm | 4.5 mm → 119 µm | 9.7 (1.03×) | 1.09 / 1.56 | 320 | 0.182 | 6.0 | 81 (scan 17 %) | 2.00 | 2.6 | 27.0 |
| IPG 5 mm, run out of focus so the powder sees 75 um | 5.00 | 75 (48 at focus, 1.85 mm out) | 1.53 | – (on the slope) | +3.6 % | 55–101 µm | 1.1 mm → 53 or 104 µm | 15.8 (1.68×) | 1.58 / 2.26 | 221 | 0.142 | 4.7 | 84 (scan 21 %) | 1.00 | 5.1 | 24.3 |

Notes: the light-film shift (0.05 % absorbed in the slide) is 0.73 z_R for every beam size (thermal_lens.md); with the defocused option it shrinks or grows the spot depending on which side of the powder the focus sits. The expander rows add two lenses to the 500 W beam (each a further ~0.2 z_R of thermal shift when clean, Faas et al. 2018). Galvo fill D/20 mm and f-theta fill D/12 mm are ≤ 0.42 for every option.
