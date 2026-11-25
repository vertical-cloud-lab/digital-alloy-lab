# CalculiX cross-check of the cover-slide thermal lens (`analysis/optics/thermal_lens_ccx.py`)

2° sector of the slide (C3D6 at the axis, C3D8 elsewhere), absorbed power in the bottom element row, rim at the mount temperature, *FILM h = 10 W/m²K on both faces. Same inputs as the finite-volume solve in thermal_lens.py.

| Case | Beam w on slide (mm) | P_abs (W) | Mesh (nodes / elements) | ΔT centre, CalculiX / FV (K) | D_eff, CalculiX / FV (1/m) | Central curvature D0 (1/m) | Focus shift, CalculiX / FV (mm) |
|---|---|---|---|---|---|---|---|
| 3.2 mm beam, fogged 0.5 % | 1.27 | 2.50 | 1833 / 840 | 426.6 / 422.1 | 1.732 / 1.746 | 3.529 | 22.9 / 23.1 |
| 5 mm beam, fogged 0.5 % | 1.98 | 2.50 | 1833 / 840 | 360.3 / 358.1 | 0.698 / 0.701 | 1.446 | 10.3 / 10.4 |
| 3.2 mm beam, light film 0.05 % | 1.27 | 0.25 | 1833 / 840 | 42.7 / 42.2 | 0.173 / 0.175 | 0.353 | 2.7 / 2.8 |
| 2.5 mm beam (drawn), light film 0.05 % | 0.99 | 0.25 | 1833 / 840 | 46.4 / 45.8 | 0.285 / 0.289 | 0.578 | 4.4 / 4.5 |
