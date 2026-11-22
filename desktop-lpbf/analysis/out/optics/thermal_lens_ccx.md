# CalculiX cross-check of the cover-slide thermal lens (`analysis/optics/thermal_lens_ccx.py`)

2° sector of the slide (C3D6 at the axis, C3D8 elsewhere), absorbed power in the bottom element row, rim at the mount temperature, *FILM h = 10 W/m²K on both faces. Same inputs as the finite-volume solve in thermal_lens.py.

| Case | Beam w on slide (mm) | P_abs (W) | Mesh (nodes / elements) | ΔT centre, CalculiX / FV (K) | D_eff, CalculiX / FV (1/m) | Central curvature D0 (1/m) | Focus shift, CalculiX / FV (mm) |
|---|---|---|---|---|---|---|---|
| 3.2 mm beam, fogged 0.5 % | 1.26 | 2.50 | 1833 / 840 | 302.3 / 296.1 | 1.767 / 1.781 | 3.585 | 22.9 / 23.1 |
| 5 mm beam, fogged 0.5 % | 1.97 | 2.50 | 1833 / 840 | 256.5 / 253.3 | 0.715 / 0.718 | 1.469 | 10.4 / 10.5 |
| 3.2 mm beam, light film 0.05 % | 1.26 | 0.25 | 1833 / 840 | 30.2 / 29.6 | 0.177 / 0.178 | 0.359 | 2.7 / 2.8 |
