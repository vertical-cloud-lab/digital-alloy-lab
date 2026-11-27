# Structural FEA summary (CalculiX, axisymmetric CAX6)

## Option B vessel (316L weldment)

| Case | max von Mises (MPa) | where (r, z mm) | T there (C) | 316L yield there (MPa) | ratio | max displacement (mm) |
|---|---:|---|---:|---:|---:|---:|
| B_pressure | 9.5 |  | 25 | 172 | 0.055 | 0.0021 |
| B_vacuum | 8.97 |  | 25 | 172 | 0.052 | 0.0019 |
| B_hot_10s | 14.0 | [37.9, -207.8] | 64.0 | 157.0 | 0.09 | 0.038 |
| B_hot_60s | 60.8 | [31.8, -244.0] | 53.0 | 161.0 | 0.38 | 0.253 |
| B_hot_300s | 53.7 | [31.8, -244.0] | 268.0 | 112.0 | 0.48 | 0.59 |
| B_hot_900s | 56.5 | [36.3, -239.8] | 312.0 | 107.0 | 0.53 | 0.502 |
| B_hot_1800s | 46.0 | [36.3, -239.8] | 247.0 | 115.0 | 0.4 | 0.361 |
| B_hot_3600s | 28.2 | [36.3, -239.8] | 157.0 | 131.0 | 0.21 | 0.204 |

## Glass tube (option C), thermal stress from the hot pile

| Case | Glass | worst max principal (MPa) | at t (s) | long-term design tensile (MPa) | short-term fracture (MPa) |
|---|---|---:|---:|---:|---:|
| C_400 | QUARTZ | 0.77 | 60 | 7.0 | 50.0 |
| C_400_boro | BORO | 5.56 | 60 | 6.0 | 40.0 |
| C_816 | QUARTZ | 1.25 | 60 | 7.0 | 50.0 |
| S_seat_120 | BORO | 0.65 | 10 | 6.0 | 40.0 |
| S_glass_300 | BORO | 55.47 | 10 | 6.0 | 40.0 |

## Upper part, shot fused in the bore just under the KF joint (B welded, B' turned adapter)

Elastic thermal stress at the worst of the saved times (10, 60, 300, 900, 1800, 3600 s), held on one ring at the KF flange's back taper. Face dish: how far the KF face's O-ring land tilts while hot.

| Case | design | worst at t (s) | max von Mises (MPa) | where (r, z mm) | T there (C) | yield there (MPa) | ratio | part's max T (C) | face dish (um) |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| B_hangup_25 | B | 10 | 359.3 | [25.2, -8.9] | 236 | 116 | 3.09 | 265 | 40.9 |
| B_hangup_100 | B | 10 | 466.3 | [26.5, -2.1] | 290 | 109 | 4.27 | 699 | 233.7 |
| B_hangup_25_adapter | B' | 10 | 276.7 | [23.9, -6.7] | 216 | 119 | 2.33 | 221 | 27.2 |
| B_hangup_100_adapter | B' | 10 | 492.2 | [23.9, -15.5] | 397 | 99 | 4.96 | 403 | 28.8 |
