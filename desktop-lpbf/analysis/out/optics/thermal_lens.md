# Thermal lensing at 500 W (`analysis/optics/thermal_lens.py`)

Fused silica: k 1.38 W/m·K, dn/dT 9.60e-06 /K, χ = dn/dT + (n−1)(1+ν)α = 9.871e-06 /K. N-BK7-type glass χ = 6.74e-06 /K, k 1.114. Static beam (worst case: a small coupon near the field centre). Focus moves toward the lens by Δz = h²D/(1 + hD).

| Collimator D | Element | Absorption | P_abs (W) | Beam w (mm) | ΔT centre, rim fixed / insulated rim (K) | D_eff (1/m) | Central-curvature D0 (1/m) | Focus shift (mm) | × z_R |
|---|---|---|---|---|---|---|---|---|---|
| 5.0 mm | cover slide (Ø50.8 x 3, rim on the drawer) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.008 | 1.97 | 0.81 / 0.92 | 0.00231 | 0.0047 | **0.037** | 0.024 |
| 5.0 mm | cover slide (Ø50.8 x 3, rim on the drawer) | clean, AR both faces (2 x 30 ppm + bulk) | 0.033 | 1.97 | 3.4 / 3.8 | 0.00951 | 0.0194 | **0.15** | 0.098 |
| 5.0 mm | cover slide (Ø50.8 x 3, rim on the drawer) | light film 0.05 % | 0.25 | 1.97 | 25 / 29 | 0.0718 | 0.147 | **1.1** | 0.74 |
| 5.0 mm | cover slide (Ø50.8 x 3, rim on the drawer) | fogged 0.5 % | 2.5 | 1.97 | 2.5e+02 / 2.9e+02 | 0.718 | 1.47 | **10** | 6.8 |
| 5.0 mm | cover slide (Ø50.8 x 3, rim on the drawer) | sooted 2 % | 10 | 1.97 | 1e+03 / 1.1e+03 | 2.87 | 5.87 | **33** | 22 |
| 5.0 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.013 | 2.30 | 0.51 / 0.81 | 0.00278 | 0.00561 | **0.06** | 0.039 |
| 5.0 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | clean, AR both faces (2 x 30 ppm + bulk) | 0.038 | 2.30 | 1.5 / 2.4 | 0.00812 | 0.0164 | **0.18** | 0.11 |
| 5.0 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | light film 0.05 % | 0.25 | 2.30 | 9.7 / 15 | 0.0531 | 0.108 | **1.1** | 0.74 |
| 5.0 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | fogged 0.5 % | 2.5 | 2.30 | 97 / 1.5e+02 | 0.531 | 1.08 | **11** | 6.9 |
| 5.0 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | sooted 2 % | 10 | 2.30 | 3.9e+02 / 6.2e+02 | 2.13 | 4.32 | **35** | 23 |
| 3.2 mm | cover slide (Ø50.8 x 3, rim on the drawer) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.008 | 1.26 | 0.95 / 1.1 | 0.00571 | 0.0115 | **0.091** | 0.024 |
| 3.2 mm | cover slide (Ø50.8 x 3, rim on the drawer) | clean, AR both faces (2 x 30 ppm + bulk) | 0.033 | 1.26 | 3.9 / 4.3 | 0.0236 | 0.0473 | **0.37** | 0.1 |
| 3.2 mm | cover slide (Ø50.8 x 3, rim on the drawer) | light film 0.05 % | 0.25 | 1.26 | 30 / 33 | 0.178 | 0.359 | **2.8** | 0.74 |
| 3.2 mm | cover slide (Ø50.8 x 3, rim on the drawer) | fogged 0.5 % | 2.5 | 1.26 | 3e+02 / 3.3e+02 | 1.78 | 3.59 | **23** | 6.2 |
| 3.2 mm | cover slide (Ø50.8 x 3, rim on the drawer) | sooted 2 % | 10 | 1.26 | 1.2e+03 / 1.3e+03 | 7.13 | 14.3 | **60** | 16 |
| 3.2 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.013 | 1.47 | 0.59 / 0.89 | 0.00684 | 0.0137 | **0.15** | 0.039 |
| 3.2 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | clean, AR both faces (2 x 30 ppm + bulk) | 0.038 | 1.47 | 1.7 / 2.6 | 0.02 | 0.04 | **0.43** | 0.12 |
| 3.2 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | light film 0.05 % | 0.25 | 1.47 | 11 / 17 | 0.131 | 0.263 | **2.8** | 0.74 |
| 3.2 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | fogged 0.5 % | 2.5 | 1.47 | 1.1e+02 / 1.7e+02 | 1.31 | 2.63 | **24** | 6.3 |
| 3.2 mm | window (Ø50.8 x 8, O-ring seat Ø44.9) | sooted 2 % | 10 | 1.47 | 4.5e+02 / 6.8e+02 | 5.24 | 10.5 | **64** | 17 |

f-theta lens heated by its own absorption (all elements lumped, beam at its collimated size, at H' 160 mm above focus):

| Collimator D | Material | Total absorption | P_abs (W) | D_eff (1/m) | Focus shift (mm) | × z_R |
|---|---|---|---|---|---|---|
| 5.0 mm | fused silica | 0.02 % | 0.1 | 0.0182 | **0.46** | 0.3 |
| 5.0 mm | fused silica | 0.05 % | 0.25 | 0.0455 | **1.2** | 0.75 |
| 5.0 mm | fused silica | 0.10 % | 0.5 | 0.0909 | **2.3** | 1.5 |
| 5.0 mm | fused silica | 0.30 % | 1.5 | 0.273 | **6.7** | 4.4 |
| 5.0 mm | N-BK7-type glass | 0.02 % | 0.1 | 0.0154 | **0.39** | 0.26 |
| 5.0 mm | N-BK7-type glass | 0.05 % | 0.25 | 0.0384 | **0.98** | 0.64 |
| 5.0 mm | N-BK7-type glass | 0.10 % | 0.5 | 0.0768 | **1.9** | 1.3 |
| 5.0 mm | N-BK7-type glass | 0.30 % | 1.5 | 0.23 | **5.7** | 3.7 |
| 3.2 mm | fused silica | 0.02 % | 0.1 | 0.0448 | **1.1** | 0.3 |
| 3.2 mm | fused silica | 0.05 % | 0.25 | 0.112 | **2.8** | 0.75 |
| 3.2 mm | fused silica | 0.10 % | 0.5 | 0.224 | **5.5** | 1.5 |
| 3.2 mm | fused silica | 0.30 % | 1.5 | 0.672 | **16** | 4.1 |
| 3.2 mm | N-BK7-type glass | 0.02 % | 0.1 | 0.0379 | **0.96** | 0.26 |
| 3.2 mm | N-BK7-type glass | 0.05 % | 0.25 | 0.0947 | **2.4** | 0.64 |
| 3.2 mm | N-BK7-type glass | 0.10 % | 0.5 | 0.189 | **4.7** | 1.3 |
| 3.2 mm | N-BK7-type glass | 0.30 % | 1.5 | 0.568 | **13** | 3.6 |

Sapphire cover slide (c-plane, 2 mm, χ = 1.82e-05 /K, k 27.0), same geometry:

| Collimator D | Absorption | ΔT centre (K) | D_eff (1/m) | Focus shift (mm) | × z_R |
|---|---|---|---|---|---|
| 5.0 mm | 0.05 % | 2.2 | 0.00692 | **0.11** | 0.071 |
| 5.0 mm | 0.50 % | 22 | 0.0692 | **1.1** | 0.71 |
| 5.0 mm | 2.00 % | 90 | 0.277 | **4.2** | 2.8 |
| 3.2 mm | 0.05 % | 2.6 | 0.017 | **0.27** | 0.072 |
| 3.2 mm | 0.50 % | 26 | 0.17 | **2.6** | 0.7 |
| 3.2 mm | 2.00 % | 1e+02 | 0.679 | **9.9** | 2.6 |

Check against mech.md E (500 W, 0.5 %): its formula gives 43.8 mm. mech.md: w = 1.27 mm, D = P dn/dT/(2 pi k w^2), dz = f^2 D: 43.8 mm. Here: the slide is at z 126 (not 145), the central-curvature power is 2x, and dz = h^2 D/(1 + h D) for an element h above focus.

Time constants: local (w = 2 mm) 1.2 s; whole slide 108 s.
