# Vendor CAD vs vendor_parts.py builders (r6_after)

Aligned volume IoU (manifold3d booleans) and surface-to-surface distance (20k samples each way). Made by cad/oem/compare_cad.py.

| Builder | Vendor CAD | IoU | Δ volume | mean dist (mm) | P95 (mm) | max (mm) | extents ours / vendor (mm) |
|---|---|---|---|---|---|---|---|
| `mcm_3861N11()` | McMaster 3861N11 (coiled lead dropped) | 0.948 | +1.4 % | 0.24 | 1.48 | 8.30 | [27.0, 29.0, 66.65] / [27.0, 29.0, 66.65] |
| `mcm_5169K72()` | McMaster 5169K72 | 0.949 | +0.0 % | 0.84 | 4.98 | 13.10 | [94.8, 104.84, 121.0] / [97.86, 104.9, 121.27] |
