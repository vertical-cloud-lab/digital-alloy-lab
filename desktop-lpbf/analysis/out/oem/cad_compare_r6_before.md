# Vendor CAD vs vendor_parts.py builders (r6_before)

Aligned volume IoU (manifold3d booleans) and surface-to-surface distance (20k samples each way). Made by cad/oem/compare_cad.py.

| Builder | Vendor CAD | IoU | Δ volume | mean dist (mm) | P95 (mm) | max (mm) | extents ours / vendor (mm) |
|---|---|---|---|---|---|---|---|
| `mcm_3861N11()` | McMaster 3861N11 (coiled lead dropped) | 0.692 | +23.5 % | 1.70 | 7.58 | 11.93 | [23.8, 27.0, 86.3] / [27.0, 29.0, 66.65] |
| `mcm_5169K72()` | McMaster 5169K72 | 0.746 | +30.6 % | 4.06 | 10.87 | 13.89 | [92.1, 104.94, 121.2] / [97.86, 104.9, 121.27] |
