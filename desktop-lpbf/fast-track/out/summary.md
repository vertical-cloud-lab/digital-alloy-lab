# fast_track.py output

Box 16 x 12 x 8 in: 25.2 L, gas volume ~23.5 L; purge at 20 L/min.

| target_ppm | volume_changes | ideal_min | real_min_low | real_min_high | argon_L_low | argon_L_high |
|---|---|---|---|---|---|---|
| 1000 | 5.34 | 6.3 | 12.5 | 31.3 | 251 | 627 |
| 500 | 6.04 | 7.1 | 14.2 | 35.4 | 283 | 708 |
| 100 | 7.64 | 9.0 | 17.9 | 44.9 | 359 | 897 |

Build time, argon and powder:

| build_mm | layers | scan_s_per_layer | hours_low | hours_high | nozzle_L_min | argon_m3_low | argon_m3_high | builds_per_cylinder | argon_usd | powder_g |
|---|---|---|---|---|---|---|---|---|---|---|
| 10.0 | 333 | 4.9 | 1.19 | 1.84 | 27.0 | 2.83 | 3.88 | 2.4-3.4 | 31-124 | 30 |
| 15.0 | 500 | 4.9 | 1.79 | 2.76 | 27.0 | 3.8 | 5.37 | 1.8-2.5 | 42-172 | 45 |

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

- **FT0**: $18,536-31,578 (without the monitoring group: $14,076-25,356); vendors at or over $3,500 (PO): none
  - Laser and optics (used): $4,757-7,946
  - Scan control and computing: $1,183-2,473
  - Motion: $150-600
  - Enclosure and chamber: $944-1,210
  - Heated plate: $610-1,010
  - Gas and O2: $2,651-4,130
  - Safety: $2,780-3,682
  - Stock and fabrication: $1,000-1,575
  - Powder handling: $0-2,730
  - Monitoring: $4,460-6,222
- **FT1**: $26,665-41,328 (without the monitoring group: $21,405-33,106); vendors at or over $3,500 (PO): Zaber ($5,896)
  - Laser and optics (used): $4,757-7,946
  - Scan control and computing: $1,375-2,705
  - Motion: $5,976-6,096
  - Enclosure and chamber: $944-1,210
  - Heated plate: $946-1,406
  - Gas and O2: $2,651-4,130
  - Safety: $2,780-3,682
  - Stock and fabrication: $1,975-3,200
  - Powder handling: $0-2,730
  - Monitoring: $5,260-8,222
- **FT1V**: $37,406-53,738 (without the monitoring group: $32,146-45,516); vendors at or over $3,500 (PO): Zaber ($5,896), Ideal Vacuum ($9,450)
  - Laser and optics (used): $4,757-7,946
  - Scan control and computing: $1,375-2,705
  - Motion: $5,976-6,096
  - Enclosure and chamber: $11,360-13,100
  - Heated plate: $946-1,406
  - Gas and O2: $2,651-4,130
  - Safety: $2,780-3,682
  - Stock and fabrication: $2,300-3,720
  - Powder handling: $0-2,730
  - Monitoring: $5,260-8,222

Milestones (working days -> weeks):

- FT-0 single-track bench: FIRST TRACKS at 10-26 working days = 1.9-5.3 weeks
- FT-1 purge-box LPBF (stages on one PO): FIRST TRACKS at 16-37 working days = 3.2-7.3 weeks
- FT-1 purge-box LPBF (stages on one PO): FIRST COUPONS at 21-47 working days = 4.2-9.3 weeks
- FT-1 purge-box LPBF (stages on PCards): FIRST TRACKS at 13-37 working days = 2.7-7.3 weeks
- FT-1 purge-box LPBF (stages on PCards): FIRST COUPONS at 18-47 working days = 3.7-9.3 weeks
- FT-1V same, in a stock vacuum chamber: FIRST TRACKS at 17-42 working days = 3.4-8.4 weeks
- FT-1V same, in a stock vacuum chamber: FIRST COUPONS at 22-52 working days = 4.4-10.4 weeks

Shop throughput against FT-1 purge-box LPBF (stages on PCards): FIRST COUPONS (early with the low hours, late with the full hours):

- 5 shop h a working day: 4.5-9.3 weeks
- 8 shop h a working day: 3.7-7.5 weeks
- 12 shop h a working day: 3.2-6.5 weeks

Layout sketch: bed 63 mm above the box floor, 140 mm below the window; lens 363 mm above the floor; overall ~768 mm with the stage below.
