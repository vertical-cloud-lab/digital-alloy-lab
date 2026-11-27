# Structural FEA summary (CalculiX, axisymmetric CAX6)

## Option B vessel (316L weldment)

| Case | max von Mises (MPa) | where (r, z mm) | T there (C) | 316L yield there (MPa) | ratio | max displacement (mm) |
|---|---:|---|---:|---:|---:|---:|
| B_pressure | 6.83 |  | 25 | 172 | 0.04 | 0.002 |
| B_vacuum | 5.69 |  | 25 | 172 | 0.033 | 0.0018 |
| B_hot_10s | 13.3 | [36.7, -206.9] | 66.0 | 156.0 | 0.09 | 0.046 |
| B_hot_60s | 60.8 | [36.7, -243.6] | 65.0 | 157.0 | 0.39 | 0.299 |
| B_hot_300s | 62.4 | [36.7, -243.6] | 290.0 | 109.0 | 0.57 | 0.807 |
| B_hot_900s | 86.8 | [36.7, -243.6] | 319.0 | 106.0 | 0.82 | 0.692 |
| B_hot_1800s | 69.8 | [36.7, -243.6] | 252.0 | 114.0 | 0.61 | 0.476 |
| B_hot_3600s | 41.7 | [36.7, -243.6] | 158.0 | 131.0 | 0.32 | 0.261 |

## Glass tube (option C), thermal stress from the hot pile

| Case | Glass | worst max principal (MPa) | at t (s) | long-term design tensile (MPa) | short-term fracture (MPa) |
|---|---|---:|---:|---:|---:|
| C_400 | QUARTZ | 0.77 | 60 | 7.0 | 50.0 |
| C_400_boro | BORO | 5.56 | 60 | 6.0 | 40.0 |
| C_816 | QUARTZ | 1.25 | 60 | 7.0 | 50.0 |
| S_seat_120 | BORO | 0.65 | 10 | 6.0 | 40.0 |
| S_glass_300 | BORO | 55.47 | 10 | 6.0 | 40.0 |
