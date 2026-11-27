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
  "T_liner": 463,
  "T_puck": 133,
  "T_vessel": 32,
  "liner_gap_mm": 1.24,
  "puck_gap_mm": 1.387
 },
 {
  "t_s": 60.0,
  "T_liner": 555,
  "T_puck": 263,
  "T_vessel": 90,
  "liner_gap_mm": 1.209,
  "puck_gap_mm": 1.337
 },
 {
  "t_s": 300.0,
  "T_liner": 513,
  "T_puck": 376,
  "T_vessel": 249,
  "liner_gap_mm": 1.337,
  "puck_gap_mm": 1.359
 },
 {
  "t_s": 900.0,
  "T_liner": 344,
  "T_puck": 356,
  "T_vessel": 243,
  "liner_gap_mm": 1.453,
  "puck_gap_mm": 1.369
 },
 {
  "t_s": 1800.0,
  "T_liner": 250,
  "T_puck": 277,
  "T_vessel": 186,
  "liner_gap_mm": 1.48,
  "puck_gap_mm": 1.387
 },
 {
  "t_s": 3600.0,
  "T_liner": 156,
  "T_puck": 173,
  "T_vessel": 118,
  "liner_gap_mm": 1.499,
  "puck_gap_mm": 1.413
 }
]
```
