# Physics-based truth (`BOFN_TRUTH=phys`, bar 9010): written by `phys/check_phys.py`

- Inside the proposal's limits: 74% of the box.
- Bar: m_ref = 0.810 (dense 90-10 Cu-Ni).
- Optimum at (1, 1): J* = 0.429 at Ni 11.7, Al 4.3, Fe 3.2, Mn 0.0 wt%, a = 0.42, P = 0.63, v = 0.54; strength estimate 396 MPa, freezing range 33 C, liquidus 1127 C, k = 33 W/m K; rho_m 0.99, beta 0.17, U 0.65, m 0.925; passes the CALPHAD crack screen (f = 0.16).
- Best design passing the CALPHAD crack screen: 100% of J* (Ni 12.6, Al 4.4, Fe 2.5, Mn 0.0 wt%).

| Reference alloy | inside limits | J (% of J*) | yield estimate (MPa) | freezing range (C) | liquidus (C) | k (W/m K) | ln rate vs C71500 | rho_m | beta | U | m | passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | yes | -0.090 (-21%) | 147 | 59 | 1229 | 22 | +0.00 | 0.97 | 0.00 | 0.34 | 0.841 | yes |
| C70600 (90-10 Cu-Ni) | yes | 0.027 (6%) | 91 | 26 | 1132 | 46 | +0.11 | 0.98 | 0.00 | 0.28 | 0.810 | no |
| C95800 (NAB) | yes | -0.148 (-35%) | 448 | 78 | 1118 | 31 | +0.95 | 0.92 | 0.44 | 0.68 | 0.289 | no |

| Bar | m_ref | share of designs inside the limits passing immersion | Ni floor (optimized), wt% | witness |
|---|---|---|---|---|
| 90-10 | 0.810 | 5.2% | 2.2 | Ni 2.2, Al 2.9, Fe 1.4, Mn 0.0 |
| 70-30 | 0.842 | 3.2% | 3.3 | Ni 3.3, Al 2.9, Fe 3.7, Mn 0.4 |
