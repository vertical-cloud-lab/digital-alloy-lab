# Beam path, end to end (`analysis/optics/beam_path.py`)

500 W, 1070 nm, M² 1.05 typ / 1.1 max; f = 160 mm; fused silica n = 1.4496 at 1070 nm. Paraxial: no lens prescription is used.

## B. Collimator → spot (bare-fibre divergence 140 mrad; range 130–150 mrad in brackets)

| Collimator | f_c (mm) | D (mm) | Spot, M² 1.05 / 1.1 (µm) | Rayleigh range ±z_R (mm) | ±5 % / ±10 % spot growth (mm) | Spot at f = 254 (µm) | Galvo Ø20 clip |
|---|---|---|---|---|---|---|---|
| IPG standard, 5 mm beam (drawn in the model) | 35.7 | 5.00 | 46 / 48 [46–48] | 1.53 | 0.49 / 0.70 | 76 | 1.3e-14 |
| IPG standard, 7.5 mm beam | 53.6 | 7.50 | 31 / 32 [31–32] | 0.68 | 0.22 / 0.31 | 51 | 6.7e-07 |
| f = 30 mm QBH collimator (the model's label, low-profile.md) | 30.0 | 4.20 | 54 / 57 [51–61] | 2.17 | 0.70 / 1.00 | 91 | 2.0e-20 |
| D = 3.2 mm (the ~75 um target; f_c ~ 23 mm) | 22.9 | 3.20 | 72 / 75 [72–75] | 3.75 | 1.20 / 1.72 | 119 | 1.2e-34 |
| IPG affixed 2.5 mm option (YLR series datasheet rev 2/26) | 17.9 | 2.50 | 92 / 96 [92–96] | 6.14 | 1.97 / 2.81 | 152 | 2.6e-56 |

Collimated beam needed for a given spot at f = 160 mm (M² 1.1): 60 µm → D 4.00 mm, f_c 28.5 mm (26.6–30.7); 70 µm → D 3.43 mm, f_c 24.5 mm (22.8–26.3); 75 µm → D 3.20 mm, f_c 22.8 mm (21.3–24.6); 80 µm → D 3.00 mm, f_c 21.4 mm (20.0–23.1); 90 µm → D 2.66 mm, f_c 19.0 mm (17.8–20.5); 100 µm → D 2.40 mm, f_c 17.1 mm (16.0–18.4)

Fibre: the divergence spec implies a 10.2 µm beam diameter at the fibre end (9.5–11.0 µm).

## C. Where the focus lands

The model puts the lens's air focus on the powder plane. The 8 mm window and 3 mm slide push it **3.41 mm below the powder plane**. Spot on the powder plane as drawn (M² 1.1, 140 mrad):

- IPG standard, 5 mm beam (drawn in the model): 48 µm at focus, **117 µm on the powder** (2.2 z_R out)
- IPG standard, 7.5 mm beam: 32 µm at focus, **163 µm on the powder** (5.0 z_R out)
- f = 30 mm QBH collimator (the model's label, low-profile.md): 57 µm at focus, **106 µm on the powder** (1.6 z_R out)
- D = 3.2 mm (the ~75 um target; f_c ~ 23 mm): 75 µm at focus, **101 µm on the powder** (0.9 z_R out)
- IPG affixed 2.5 mm option (YLR series datasheet rev 2/26): 96 µm at focus, **110 µm on the powder** (0.6 z_R out)

| Focus budget item | mm | kind |
|---|---|---|
| window 8 mm + slide 3 mm of fused silica in the converging beam (static; take out by raising the lens) | 3.411 | static |
| cover slide thickness tolerance +/-0.38 mm (Edmund 25-250) | 0.118 | per slide |
| plate stack growth at 200 C (powder-spreading.md), if the blade is zeroed cold | 0.112 | zero the blade hot |
| bridge posts +50 K (mech.md F) | 0.070 | slow drift |

## D/E. Field geometry (k = chief-ray angle at the plate / optical scan angle; not published for the FTH160-1064)

| k | Plate | r (mm) | Scan, optical (°) | Mirror (°) | AOI (°) | Elongation (%) | Plate lateral shift (mm) | Extra focus shift (mm) | Astigmatism (mm) | Chief ray r at slide / window / lens out (mm) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.3 | S25 | 12.7 | 4.5 | 2.3 | 1.4 | 0.03 | 0.081 | 0.000 | 0.002 | 9.7 / 9.1 / 8.4 |
| 0.3 | M50 | 25.4 | 9.1 | 4.5 | 2.7 | 0.11 | 0.163 | 0.001 | 0.009 | 19.3 / 18.2 / 16.7 |
| 0.3 | L75 | 38.1 | 13.6 | 6.8 | 4.1 | 0.26 | 0.244 | 0.001 | 0.020 | 29.0 / 27.2 / 25.0 |
| 0.5 | S25 | 12.7 | 4.5 | 2.3 | 2.3 | 0.08 | 0.135 | 0.000 | 0.006 | 7.6 / 6.7 / 5.5 |
| 0.5 | M50 | 25.4 | 9.1 | 4.5 | 4.5 | 0.32 | 0.271 | 0.002 | 0.025 | 15.3 / 13.3 / 10.9 |
| 0.5 | L75 | 38.1 | 13.6 | 6.8 | 6.8 | 0.71 | 0.409 | 0.004 | 0.057 | 22.8 / 19.9 / 16.3 |
| 0.75 | S25 | 12.7 | 4.5 | 2.3 | 3.4 | 0.18 | 0.203 | 0.001 | 0.014 | 5.1 / 3.6 / 1.8 |
| 0.75 | M50 | 25.4 | 9.1 | 4.5 | 6.8 | 0.71 | 0.409 | 0.004 | 0.057 | 10.1 / 7.2 / 3.6 |
| 0.75 | L75 | 38.1 | 13.6 | 6.8 | 10.2 | 1.62 | 0.617 | 0.009 | 0.128 | 15.1 / 10.7 / 5.2 |

Thin-lens estimate of k (lens at z 160, stop at the mirrors, z 272.7): exit pupil 381 mm above the lens, k = 0.30. The lens's real principal planes are not published, so the tables span k = 0.3-0.75.


k from a thin lens with its front principal plane between the lens body's middle and H' (z 160): as drawn (2nd mirror ~40 mm above the nose): 0.30-0.59; Thorlabs A1 = 7.5 mm (2nd mirror 7.5 mm above the nose): 0.50-0.80

Clear diameter each lid opening needs to pass the L75 edge (r 38.1 mm) with < 0.1 % clipped (mm):

| Beam | k | lid bore (drawn Ø56) | drawer opening (drawn Ø46) | field stop (drawn Ø36) | window flange bore (below window) (drawn Ø42) | window retaining ring (above window) (drawn Ø44) |
|---|---|---|---|---|---|---|
| 5.0 mm | 0.3 | 64.9 | 64.4 | 63.8 | 63.3 | 61.4 |
| 5.0 mm | 0.45 | 56.2 | 55.4 | 54.4 | 53.6 | 50.1 |
| 5.0 mm | 0.6 | 47.5 | 46.4 | 44.9 | 43.7 | 38.8 |
| 3.2 mm | 0.3 | 62.8 | 62.2 | 61.5 | 61.0 | 58.6 |
| 3.2 mm | 0.45 | 54.1 | 53.2 | 52.1 | 51.2 | 47.4 |
| 3.2 mm | 0.6 | 45.4 | 44.2 | 42.6 | 41.3 | 36.0 |

Largest plate radius each lid aperture passes with < 0.1 % clipped (mm; plates are 12.7 / 25.4 / 38.1):

| Collimator | k | lid bore Ø56 | drawer opening Ø46 | field stop Ø36 | window flange bore (below window) Ø42 | window retaining ring (above window) Ø44 | field stop, 50 % reach |
|---|---|---|---|---|---|---|---|
| IPG 5 mm | 0.3 | 32.4 | 26.1 | 19.7 | 23.8 | 25.8 | 23.9 |
| IPG 5 mm | 0.5 | 40.3 | 32.8 | 25.1 | 30.9 | 35.8 | 30.5 |
| IPG 5 mm | 0.75 | 59.1 | 49.3 | 39.0 | 50.3 | 60.0 | 48.0 |
| D 3.2 mm | 0.3 | 33.7 | 27.5 | 21.2 | 25.4 | 27.7 | 23.9 |
| D 3.2 mm | 0.5 | 42.0 | 34.6 | 27.1 | 32.9 | 38.5 | 30.5 |
| D 3.2 mm | 0.75 | 60.0 | 52.3 | 42.2 | 54.0 | 60.0 | 48.0 |

## F. Irradiance at 500 W (lens refocused onto the plate)

**IPG 5 mm, M2 1.1**

| Surface | Beam Ø (mm) | Peak (W/cm²) | P/D (W/cm) | Note |
|---|---|---|---|---|
| collimator output lens | 5.000 | 5.09e+03 | 1e+03 |  |
| shutter mirror / dump (closed) | 5.000 | 5.09e+03 | 1e+03 | the dump takes all 500 W |
| galvo mirrors (45 deg: the footprint is 1.41x longer, so the surface irradiance is 0.71x this) | 5.000 | 5.09e+03 | 1e+03 |  |
| f-theta input | 5.000 | 5.09e+03 | 1e+03 |  |
| f-theta output (protective window, z 182.5 + 3.4) | 5.703 | 3.91e+03 | 877 |  |
| chamber window, top (z 156) | 4.769 | 5.6e+03 | 1.05e+03 |  |
| chamber window, bottom (z 148) | 4.596 | 6.03e+03 | 1.09e+03 |  |
| cover slide, top (z 129) | 4.002 | 7.95e+03 | 1.25e+03 |  |
| cover slide, bottom (z 126) | 3.938 | 8.21e+03 | 1.27e+03 | the face that fouls |
| plate, at focus | 0.048 | 5.54e+07 | 1.04e+05 | melts |

**D 3.2 mm, M2 1.1**

| Surface | Beam Ø (mm) | Peak (W/cm²) | P/D (W/cm) | Note |
|---|---|---|---|---|
| collimator output lens | 3.200 | 1.24e+04 | 1.56e+03 |  |
| shutter mirror / dump (closed) | 3.200 | 1.24e+04 | 1.56e+03 | the dump takes all 500 W |
| galvo mirrors (45 deg: the footprint is 1.41x longer, so the surface irradiance is 0.71x this) | 3.200 | 1.24e+04 | 1.56e+03 |  |
| f-theta input | 3.200 | 1.24e+04 | 1.56e+03 |  |
| f-theta output (protective window, z 182.5 + 3.4) | 3.651 | 9.55e+03 | 1.37e+03 |  |
| chamber window, top (z 156) | 3.053 | 1.37e+04 | 1.64e+03 |  |
| chamber window, bottom (z 148) | 2.942 | 1.47e+04 | 1.7e+03 |  |
| cover slide, top (z 129) | 2.562 | 1.94e+04 | 1.95e+03 |  |
| cover slide, bottom (z 126) | 2.521 | 2e+04 | 1.98e+03 | the face that fouls |
| plate, at focus | 0.075 | 2.27e+07 | 6.67e+04 | melts |

## G. Back-reflection

Uncoated fused silica reflects 3.37 % per face; a good AR coat ~0.25 %.

| D (mm) | Surface | Height (air-equiv., mm) | Core coupling | Into the core, uncoated / AR (W) | Back toward the head, uncoated / AR (W) | Ghost focus z (thin lens) | Return focus from fibre end (mm) / radius there (mm) |
|---|---|---|---|---|---|---|---|
| 5.0 | slide bottom | 126.0 | 1.5e-04 | 0.002 / 0.0002 | 16.8 / 1.25 | 218 | 12.6 / 0.88 |
| 5.0 | slide top | 128.1 | 1.4e-04 | 0.002 / 0.0002 | 16.8 / 1.25 | 220 | 12.8 / 0.89 |
| 5.0 | window bottom | 147.1 | 1.1e-04 | 0.002 / 0.0001 | 16.8 / 1.25 | 233 | 14.7 / 1.03 |
| 5.0 | window top | 152.6 | 1.0e-04 | 0.002 / 0.0001 | 16.8 / 1.25 | 236 | 15.2 / 1.06 |
| 5.0 | f-theta protective window (lower face) | 182.5 | 7.1e-05 | 0.001 / 0.0001 | 16.8 / 1.25 | 250 | 18.2 / 1.27 |
| 3.2 | slide bottom | 126.0 | 8.8e-04 | 0.015 / 0.0011 | 16.8 / 1.25 | 218 | 5.1 / 0.36 |
| 3.2 | slide top | 128.1 | 8.6e-04 | 0.014 / 0.0011 | 16.8 / 1.25 | 220 | 5.2 / 0.37 |
| 3.2 | window bottom | 147.1 | 6.5e-04 | 0.011 / 0.0008 | 16.8 / 1.25 | 233 | 6.0 / 0.42 |
| 3.2 | window top | 152.6 | 6.0e-04 | 0.010 / 0.0008 | 16.8 / 1.25 | 236 | 6.2 / 0.44 |
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
