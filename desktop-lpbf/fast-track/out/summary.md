# fast_track.py output

Box 16 x 12 x 8 in: 25.2 L, gas volume ~21.2 L; purge at 20 L/min.

| target_ppm | volume_changes | ideal_min | real_min_low | real_min_high | argon_L_low | argon_L_high |
|---|---|---|---|---|---|---|
| 1000 | 5.34 | 5.7 | 11.3 | 28.3 | 226 | 566 |
| 500 | 6.04 | 6.4 | 12.8 | 31.9 | 256 | 639 |
| 100 | 7.64 | 8.1 | 16.2 | 40.5 | 324 | 809 |

Build time, argon and powder:

| build_mm | layers | scan_s_per_layer | hours_low | hours_high | nozzle_L_min | argon_m3_low | argon_m3_high | builds_per_cylinder | argon_usd | powder_g |
|---|---|---|---|---|---|---|---|---|---|---|
| 10.0 | 333 | 4.9 | 1.19 | 1.84 | 27.0 | 2.74 | 3.79 | 2.5-3.5 | 30-121 | 30 |
| 15.0 | 500 | 4.9 | 1.79 | 2.76 | 27.0 | 3.71 | 5.29 | 1.8-2.6 | 41-169 | 45 |

Heat budget at 200 °C (well block + plate on Macor standoffs):

| surface_W | standoffs_W | heater_load_W | heaters_W | margin | laser_avg_W | box_area_m2 | box_rise_still_K | box_rise_fan_K | box_air_C_still_vs_stage_max | box_air_C_fan |
|---|---|---|---|---|---|---|---|---|---|---|
| 51.6 | 4.5 | 56.0 | 200.0 | 3.57 | 46-91 | 0.537 | 32-46 | 9-14 | 71 vs 50 | 39 |

Optics (f = 254 mm, M2 1.1):

| beam_mm | spot_um | rayleigh_mm | spot_growth_at_5mm_defocus | beam_at_window_mm | window_kW_per_cm2_at_400W |
|---|---|---|---|---|---|
| 5.0 | 76 | 3.87 | 1.63 | 2.77 | 6.7 |
| 7.5 | 51 | 1.72 | 3.08 | 4.15 | 3.0 |

Cost by alternative (parts.csv):

- **FT0**: $13,130-22,185; vendors at or over $3,500 (PO): none
  - Laser and optics (used): $4,691-6,440
  - Scan control and computing: $1,670-2,850
  - Motion: $150-600
  - Enclosure and chamber: $750-1,350
  - Heated plate: $630-1,010
  - Gas and O2: $1,571-2,099
  - Safety: $2,668-3,530
  - Stock and fabrication: $1,000-1,575
  - Powder handling: $0-2,730
- **FT1**: $20,334-29,708; vendors at or over $3,500 (PO): Zaber ($6,238)
  - Laser and optics (used): $4,691-6,440
  - Scan control and computing: $1,670-2,850
  - Motion: $6,318-6,438
  - Enclosure and chamber: $750-1,350
  - Heated plate: $691-1,071
  - Gas and O2: $1,571-2,099
  - Safety: $2,668-3,530
  - Stock and fabrication: $1,975-3,200
  - Powder handling: $0-2,730
- **FT1V**: $30,969-41,278; vendors at or over $3,500 (PO): Zaber ($6,238), Ideal Vacuum ($9,450)
  - Laser and optics (used): $4,691-6,440
  - Scan control and computing: $1,670-2,850
  - Motion: $6,318-6,438
  - Enclosure and chamber: $11,060-12,400
  - Heated plate: $691-1,071
  - Gas and O2: $1,571-2,099
  - Safety: $2,668-3,530
  - Stock and fabrication: $2,300-3,720
  - Powder handling: $0-2,730

Milestones (working days -> weeks):

- FT-0 single-track bench: FIRST TRACKS at 8-21 working days = 1.6-4.2 weeks
- FT-1 purge-box LPBF (stages on one PO): FIRST TRACKS at 16-30 working days = 3.2-6.0 weeks
- FT-1 purge-box LPBF (stages on one PO): FIRST COUPONS at 21-40 working days = 4.2-8.0 weeks
- FT-1 purge-box LPBF (stages on PCards): FIRST TRACKS at 11-22 working days = 2.2-4.4 weeks
- FT-1 purge-box LPBF (stages on PCards): FIRST COUPONS at 16-32 working days = 3.2-6.4 weeks
- FT-1V same, in a stock vacuum chamber: FIRST TRACKS at 17-32 working days = 3.4-6.4 weeks
- FT-1V same, in a stock vacuum chamber: FIRST COUPONS at 22-42 working days = 4.4-8.4 weeks

Layout sketch: bed 63 mm above the box floor, 140 mm below the window; lens 363 mm above the floor; overall ~768 mm with the stage below.
