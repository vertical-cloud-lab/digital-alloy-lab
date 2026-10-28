# Physics-based truth (`BOFN_TRUTH=phys`, bar 9010): written by `phys/check_phys.py`

- Inside the proposal's limits: 74% of the box.
- Bar: m_ref = 0.831 (dense 90-10 Cu-Ni).
- Optimum at (1, 1): J* = 0.298 at Ni 12.9, Al 2.4, Fe 0.3, Mn 0.0 wt%, a = 0.38, P = 0.63, v = 0.56; strength estimate 340 MPa, freezing range 14 C, liquidus 1125 C, k = 39 W/m K; rho_m 0.99, beta 0.07, U 0.58, m 0.895; passes the CALPHAD crack screen (f = 0.07).
- Best design passing the CALPHAD crack screen: 100% of J* (Ni 15.1, Al 2.4, Fe 0.5, Mn 0.0 wt%).

| Reference alloy | inside limits | J (% of J*) | yield estimate (MPa) | freezing range (C) | liquidus (C) | k (W/m K) | ln rate vs C71500 | rho_m | beta | U | m | passes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | yes | -0.124 (-42%) | 147 | 59 | 1229 | 22 | +0.00 | 0.97 | 0.00 | 0.34 | 0.841 | yes |
| C70600 (90-10 Cu-Ni) | yes | 0.027 (9%) | 91 | 26 | 1132 | 46 | +0.04 | 0.98 | 0.00 | 0.28 | 0.831 | no |
| C95800 (NAB) | yes | -0.148 (-50%) | 448 | 78 | 1118 | 31 | +1.23 | 0.92 | 0.44 | 0.68 | 0.205 | no |

| Bar | m_ref | share of designs inside the limits passing immersion | Ni floor (optimized), wt% | witness |
|---|---|---|---|---|
| 90-10 | 0.831 | 0.8% | 1.6 | Ni 1.6, Al 2.1, Fe 3.7, Mn 0.1 |
| 70-30 | 0.842 | 0.6% | 2.4 | Ni 2.4, Al 2.1, Fe 3.7, Mn 0.0 |
