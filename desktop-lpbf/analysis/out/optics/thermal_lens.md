# Thermal lensing at 500 W (`analysis/optics/thermal_lens.py`)

Fused silica: k 1.38 W/m·K, dn/dT 9.60e-06 /K, χ = dn/dT + (n−1)(1+ν)α = 9.871e-06 /K. N-BK7-type glass χ = 6.74e-06 /K, k 1.114. Static beam (worst case: a small coupon near the field centre). Focus moves toward the lens by Δz = h²D/(1 + hD).

| Collimator D | Element | Absorption | P_abs (W) | Beam w (mm) | ΔT centre, rim fixed / insulated rim (K) | D_eff (1/m) | Central-curvature D0 (1/m) | Focus shift (mm) | × z_R |
|---|---|---|---|---|---|---|---|---|---|
| 5.0 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.007 | 1.98 | 1 / 1.1 | 0.00197 | 0.00405 | **0.032** | 0.021 |
| 5.0 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | clean, AR both faces (2 x 30 ppm + bulk) | 0.032 | 1.98 | 4.6 / 4.9 | 0.00899 | 0.0185 | **0.14** | 0.094 |
| 5.0 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | light film 0.05 % | 0.25 | 1.98 | 36 / 38 | 0.0701 | 0.145 | **1.1** | 0.73 |
| 5.0 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | fogged 0.5 % | 2.5 | 1.98 | 3.6e+02 / 3.8e+02 | 0.701 | 1.45 | **10** | 6.8 |
| 5.0 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | sooted 2 % | 10 | 1.98 | 1.4e+03 / 1.5e+03 | 2.8 | 5.78 | **33** | 22 |
| 5.0 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.0145 | 2.28 | 0.48 / 0.84 | 0.00316 | 0.00637 | **0.067** | 0.044 |
| 5.0 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | clean, AR both faces (2 x 30 ppm + bulk) | 0.0395 | 2.28 | 1.3 / 2.3 | 0.0086 | 0.0173 | **0.18** | 0.12 |
| 5.0 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | light film 0.05 % | 0.25 | 2.28 | 8.3 / 14 | 0.0541 | 0.11 | **1.1** | 0.74 |
| 5.0 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | fogged 0.5 % | 2.5 | 2.28 | 83 / 1.4e+02 | 0.541 | 1.1 | **11** | 6.9 |
| 5.0 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | sooted 2 % | 10 | 2.28 | 3.3e+02 / 5.7e+02 | 2.16 | 4.38 | **35** | 23 |
| 3.2 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.007 | 1.27 | 1.2 / 1.2 | 0.0049 | 0.00988 | **0.079** | 0.021 |
| 3.2 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | clean, AR both faces (2 x 30 ppm + bulk) | 0.032 | 1.27 | 5.4 / 5.7 | 0.0224 | 0.0452 | **0.36** | 0.096 |
| 3.2 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | light film 0.05 % | 0.25 | 1.27 | 42 / 44 | 0.175 | 0.353 | **2.8** | 0.74 |
| 3.2 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | fogged 0.5 % | 2.5 | 1.27 | 4.2e+02 / 4.4e+02 | 1.75 | 3.53 | **23** | 6.2 |
| 3.2 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | sooted 2 % | 10 | 1.27 | 1.7e+03 / 1.8e+03 | 6.98 | 14.1 | **60** | 16 |
| 3.2 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.0145 | 1.46 | 0.56 / 0.92 | 0.00778 | 0.0156 | **0.17** | 0.044 |
| 3.2 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | clean, AR both faces (2 x 30 ppm + bulk) | 0.0395 | 1.46 | 1.5 / 2.5 | 0.0212 | 0.0423 | **0.45** | 0.12 |
| 3.2 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | light film 0.05 % | 0.25 | 1.46 | 9.6 / 16 | 0.133 | 0.268 | **2.8** | 0.74 |
| 3.2 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | fogged 0.5 % | 2.5 | 1.46 | 96 / 1.6e+02 | 1.33 | 2.68 | **24** | 6.3 |
| 3.2 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | sooted 2 % | 10 | 1.46 | 3.9e+02 / 6.3e+02 | 5.33 | 10.7 | **64** | 17 |
| 2.5 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.007 | 0.99 | 1.3 / 1.3 | 0.0081 | 0.0162 | **0.13** | 0.021 |
| 2.5 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | clean, AR both faces (2 x 30 ppm + bulk) | 0.032 | 0.99 | 5.9 / 6.2 | 0.037 | 0.074 | **0.59** | 0.097 |
| 2.5 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | light film 0.05 % | 0.25 | 0.99 | 46 / 48 | 0.289 | 0.578 | **4.5** | 0.73 |
| 2.5 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | fogged 0.5 % | 2.5 | 0.99 | 4.6e+02 / 4.8e+02 | 2.89 | 5.78 | **34** | 5.6 |
| 2.5 mm | cover slide (Ø50 x 2, Edmund 36-299, rim on the drawer's Ø46 seat) | sooted 2 % | 10 | 0.99 | 1.8e+03 / 1.9e+03 | 11.6 | 23.1 | **76** | 12 |
| 2.5 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces) | 0.0145 | 1.14 | 0.61 / 0.96 | 0.0128 | 0.0255 | **0.27** | 0.044 |
| 2.5 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | clean, AR both faces (2 x 30 ppm + bulk) | 0.0395 | 1.14 | 1.7 / 2.6 | 0.0348 | 0.0693 | **0.74** | 0.12 |
| 2.5 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | light film 0.05 % | 0.25 | 1.14 | 10 / 16 | 0.219 | 0.438 | **4.5** | 0.74 |
| 2.5 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | fogged 0.5 % | 2.5 | 1.14 | 1e+02 / 1.6e+02 | 2.19 | 4.38 | **35** | 5.8 |
| 2.5 mm | window (Ø50.8 x 9.53, Edmund 38-990, O-ring seat Ø44.9) | sooted 2 % | 10 | 1.14 | 4.2e+02 / 6.6e+02 | 8.78 | 17.5 | **82** | 13 |

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
| 2.5 mm | fused silica | 0.02 % | 0.1 | 0.074 | **1.9** | 0.31 |
| 2.5 mm | fused silica | 0.05 % | 0.25 | 0.185 | **4.6** | 0.75 |
| 2.5 mm | fused silica | 0.10 % | 0.5 | 0.37 | **8.9** | 1.5 |
| 2.5 mm | fused silica | 0.30 % | 1.5 | 1.11 | **24** | 3.9 |
| 2.5 mm | N-BK7-type glass | 0.02 % | 0.1 | 0.0626 | **1.6** | 0.26 |
| 2.5 mm | N-BK7-type glass | 0.05 % | 0.25 | 0.157 | **3.9** | 0.64 |
| 2.5 mm | N-BK7-type glass | 0.10 % | 0.5 | 0.313 | **7.6** | 1.2 |
| 2.5 mm | N-BK7-type glass | 0.30 % | 1.5 | 0.939 | **21** | 3.4 |

Sapphire cover slide (c-plane, 2 mm, χ = 1.82e-05 /K, k 27.0), same geometry:

| Collimator D | Absorption | ΔT centre (K) | D_eff (1/m) | Focus shift (mm) | × z_R |
|---|---|---|---|---|---|
| 5.0 mm | 0.05 % | 2.2 | 0.00681 | **0.11** | 0.071 |
| 5.0 mm | 0.50 % | 22 | 0.0681 | **1.1** | 0.71 |
| 5.0 mm | 2.00 % | 90 | 0.272 | **4.2** | 2.8 |
| 3.2 mm | 0.05 % | 2.6 | 0.0167 | **0.27** | 0.072 |
| 3.2 mm | 0.50 % | 26 | 0.167 | **2.6** | 0.7 |
| 3.2 mm | 2.00 % | 1e+02 | 0.668 | **9.9** | 2.7 |
| 2.5 mm | 0.05 % | 2.8 | 0.0275 | **0.44** | 0.072 |
| 2.5 mm | 0.50 % | 28 | 0.275 | **4.3** | 0.7 |
| 2.5 mm | 2.00 % | 1.1e+02 | 1.1 | **16** | 2.5 |

Check against mech.md E (500 W, 0.5 %): its formula gives 43.8 mm. mech.md: w = 1.27 mm, D = P dn/dT/(2 pi k w^2), dz = f^2 D: 43.8 mm. Here: the slide is at z 127 (not 145), the central-curvature power is 2x, and dz = h^2 D/(1 + h D) for an element h above focus.

Time constants: local (w = 2 mm) 1.2 s; whole slide 108 s.
