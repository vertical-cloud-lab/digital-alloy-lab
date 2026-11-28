# Vendor CAD vs vendor_parts.py builders: before (0dbb5a3) and after (2026-11-23 refinement)

Aligned volume IoU from exact mesh booleans (manifold3d); symmetric surface-to-surface distance from 20 000 samples each way
(mean of the two means, the larger P95, Hausdorff). Alignment: best of the 24 axis rotations about the bounding-box centres,
then ICP if it raises the IoU. Made by `cad/oem/compare_cad.py`; vendor files listed in `cad/oem/cad-manifest.csv` (not committed).

| Builder | Vendor CAD | IoU before | IoU after | Δ vol before | Δ vol after | mean dist before / after (mm) | P95 before / after (mm) | max before / after (mm) |
|---|---|---|---|---|---|---|---|---|
| `clearpath_sd_231x()` | Teknic CPM-SDSK-231x (-Q STEP) | 0.586 | **0.661** | +69.4 % | +34.6 % | 3.40 / 1.71 | 12.49 / 12.05 | 25.18 / 23.81 |
| `mcm_6627T91()` | McMaster 6627T91 | 0.945 | **0.982** | +5.4 % | +0.8 % | 1.04 / 0.69 | 13.12 / 11.43 | 19.38 / 19.17 |
| `mcm_6709K12()` | McMaster 6709K12 | 0.784 | **0.834** | +10.8 % | +3.5 % | 0.86 / 0.63 | 3.30 / 2.56 | 6.00 / 4.04 |
| `mcm_4566N401()` | McMaster 4566N401 | 0.841 | **0.841** | +0.6 % | +0.6 % | 0.40 / 0.40 | 1.80 / 1.80 | 4.96 / 4.96 |
| `kf_weld_stub(25)` | McMaster 5786N23 | 0.973 | **0.973** | -0.1 % | -0.1 % | 0.03 / 0.03 | 0.31 / 0.31 | 0.73 / 0.73 |
| `kf_weld_stub(40)` | McMaster 5786N25 | 0.969 | **0.969** | -0.8 % | -0.8 % | 0.04 / 0.04 | 0.31 / 0.31 | 0.74 / 0.74 |
| `kf_wing_clamp(25)` | McMaster 4518K72 | 0.283 | **0.706** | -0.6 % | +5.6 % | 1.41 / 0.54 | 3.78 / 2.77 | 6.98 / 6.91 |
| `kf_wing_clamp(40)` | McMaster 4518K73 | 0.515 | **0.798** | -2.5 % | +1.8 % | 1.19 / 0.46 | 2.93 / 2.84 | 7.01 / 7.36 |
| `mcm_4123K45('-x')` | McMaster 4123K45 | 0.578 | **0.881** | -2.4 % | -7.0 % | 2.65 / 0.50 | 18.15 / 2.72 | 35.70 / 9.19 |
| `mcm_3861N11()` | McMaster 3861N11 (coiled lead dropped) | 0.261 | **0.267** | +22.9 % | +22.9 % | 8.52 / 8.39 | 43.47 / 43.93 | 68.76 / 69.32 |
| `mcm_5169K72()` | McMaster 5169K72 | 0.746 | **0.746** | +30.6 % | +30.6 % | 4.06 / 4.09 | 10.87 / 10.87 | 13.89 / 13.88 |
