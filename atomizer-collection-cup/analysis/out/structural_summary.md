# Structural FEA summary (CalculiX, axisymmetric CAX6)

## Option B vessel (316L weldment)

| Case | max von Mises (MPa) | where (r, z mm) | T there (C) | 316L yield there (MPa) | ratio | max displacement (mm) |
|---|---:|---|---:|---:|---:|---:|
| B_pressure | 4.4 |  | 25 | 172 | 0.026 | 0.0016 |
| B_vacuum | 3.67 |  | 25 | 172 | 0.021 | 0.0014 |
| B_hot_10s | 14.0 | [37.9, -207.7] | 64.0 | 157.0 | 0.09 | 0.046 |
| B_hot_60s | 60.6 | [31.8, -244.0] | 53.0 | 161.0 | 0.38 | 0.293 |
| B_hot_300s | 53.7 | [31.8, -244.0] | 268.0 | 112.0 | 0.48 | 0.793 |
| B_hot_900s | 55.8 | [36.3, -239.8] | 310.0 | 107.0 | 0.52 | 0.695 |
| B_hot_1800s | 45.4 | [36.3, -239.8] | 245.0 | 115.0 | 0.39 | 0.48 |
| B_hot_3600s | 27.4 | [36.3, -239.8] | 154.0 | 132.0 | 0.21 | 0.262 |

## Glass tube (option C), thermal stress from the hot pile

| Case | Glass | worst max principal (MPa) | at t (s) | long-term design tensile (MPa) | short-term fracture (MPa) |
|---|---|---:|---:|---:|---:|
| C_400 | QUARTZ | 0.77 | 60 | 7.0 | 50.0 |
| C_400_boro | BORO | 5.56 | 60 | 6.0 | 40.0 |
| C_816 | QUARTZ | 1.25 | 60 | 7.0 | 50.0 |
| S_seat_120 | BORO | 0.65 | 10 | 6.0 | 40.0 |
| S_glass_300 | BORO | 55.47 | 10 | 6.0 | 40.0 |
