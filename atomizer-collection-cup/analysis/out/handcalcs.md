# Hand calculations

Each block names its formula and source in `handcalcs.py`.

## internal_pressure_shells

```json
{
 "p_design_MPa": 0.12000000000000002,
 "rows": {
  "B body 3 in x 0.065": {
   "hoop_MPa": 2.65,
   "axial_MPa": 1.33,
   "t_required_mm": 0.038,
   "t_actual_mm": 1.65,
   "margin": 43.0
  },
  "B stub / A nipple 2 in x 0.065": {
   "hoop_MPa": 1.73,
   "axial_MPa": 0.86,
   "t_required_mm": 0.025,
   "t_actual_mm": 1.65,
   "margin": 67.0
  }
 }
}
```

## flat_bottom

```json
{
 "a_mm": 36.45,
 "t_mm": 8.0,
 "sigma_simply_supported_MPa": 3.08,
 "sigma_fixed_edge_MPa": 1.87,
 "t_required_UG34_mm": 1.35,
 "centre_deflection_ss_um": 1.49
}
```

## external_pressure

```json
{
 "B body at 25 C": {
  "L_mm": 129.3,
  "Pcr_short_MPa": 21.2,
  "Pcr_long_tube_MPa": 4.31,
  "safety_factor_vs_1bar": 212.0
 },
 "B body at 400 C": {
  "L_mm": 129.3,
  "Pcr_short_MPa": 18.24,
  "Pcr_long_tube_MPa": 3.7,
  "safety_factor_vs_1bar": 182.0
 },
 "B' pot tube (turned adapter) at 25 C": {
  "L_mm": 176.0,
  "Pcr_short_MPa": 15.42,
  "Pcr_long_tube_MPa": 4.31,
  "safety_factor_vs_1bar": 154.0
 },
 "B' pot tube (turned adapter) at 400 C": {
  "L_mm": 176.0,
  "Pcr_short_MPa": 13.26,
  "Pcr_long_tube_MPa": 3.7,
  "safety_factor_vs_1bar": 133.0
 },
 "A nipple at 25 C": {
  "L_mm": 160.0,
  "Pcr_short_MPa": 31.06,
  "Pcr_long_tube_MPa": 14.53,
  "safety_factor_vs_1bar": 311.0
 },
 "A nipple at 400 C": {
  "L_mm": 160.0,
  "Pcr_short_MPa": 26.72,
  "Pcr_long_tube_MPa": 12.5,
  "safety_factor_vs_1bar": 267.0
 }
}
```

## kf_joint

```json
{
 "seal_diameter_mm": 58.2,
 "separating_force_N": {
  "run +0.15 bar": 556.0,
  "relief +0.8 bar": 729.0,
  "design +1.2 bar": 836.0
 },
 "clamp": {
  "finger-tight 0.3 N m": {
   "bolt_tension_N": 250.0,
   "axial_clamp_N": 1804.0
  },
  "snug 1.0 N m": {
   "bolt_tension_N": 833.0,
   "axial_clamp_N": 6012.0
  }
 },
 "note": "Two-segment clamp: radial load = pi * T for a band tension T; axial = radial / tan(theta + phi). The vendor's own overpressure rating governs (bom/README.md)."
}
```

## bottom_weld

```json
{
 "shear_MPa": 1.33,
 "note": "Floor load p*pi*a^2 over the weld's ring area 2*pi*a*t"
}
```

## glass_thermal_stress

```json
{
 "borosilicate 3.3": {
  "MPa_per_K": 0.264,
  "dT_to_short_term_K": 152.0,
  "dT_to_design_K": 23.0,
  "stress_at_850K_step_MPa": 224.0
 },
 "fused quartz": {
  "MPa_per_K": 0.0477,
  "dT_to_short_term_K": 1048.0,
  "dT_to_design_K": 147.0,
  "stress_at_850K_step_MPa": 41.0
 }
}
```

## tie_rods_C

```json
{
 "gasket_area_mm2": 2388.0,
 "total_load_N": 4199.0,
 "per_rod_N": 1050.0,
 "rod_stress_MPa": 12.5,
 "glass_end_compression_MPa": 2.81,
 "torque_per_rod_Nm": 2.52
}
```

## clearances

```json
[
 {
  "t_s": 10.0,
  "T_puck": 125,
  "T_vessel": 33,
  "puck_gap_mm": 1.392,
  "T_liner": 585,
  "liner_gap_mm": 1.152,
  "puck_clear_of_opening_mm": 2.9,
  "liner_clear_of_opening_mm": 3.05
 },
 {
  "t_s": 60.0,
  "T_puck": 271,
  "T_vessel": 101,
  "puck_gap_mm": 1.338,
  "T_liner": 684,
  "liner_gap_mm": 1.118,
  "puck_clear_of_opening_mm": 2.9,
  "liner_clear_of_opening_mm": 3.05
 },
 {
  "t_s": 300.0,
  "T_puck": 391,
  "T_vessel": 295,
  "puck_gap_mm": 1.378,
  "T_liner": 556,
  "liner_gap_mm": 1.336,
  "puck_clear_of_opening_mm": 2.9,
  "liner_clear_of_opening_mm": 3.05
 },
 {
  "t_s": 900.0,
  "T_puck": 366,
  "T_vessel": 300,
  "puck_gap_mm": 1.399,
  "T_liner": 363,
  "liner_gap_mm": 1.477,
  "puck_clear_of_opening_mm": 2.9,
  "liner_clear_of_opening_mm": 3.05
 },
 {
  "t_s": 1800.0,
  "T_puck": 284,
  "T_vessel": 232,
  "puck_gap_mm": 1.411,
  "T_liner": 269,
  "liner_gap_mm": 1.496,
  "puck_clear_of_opening_mm": 2.9,
  "liner_clear_of_opening_mm": 3.05
 },
 {
  "t_s": 3600.0,
  "T_puck": 179,
  "T_vessel": 146,
  "puck_gap_mm": 1.427,
  "T_liner": 171,
  "liner_gap_mm": 1.507,
  "puck_clear_of_opening_mm": 2.9,
  "liner_clear_of_opening_mm": 3.05
 }
]
```
