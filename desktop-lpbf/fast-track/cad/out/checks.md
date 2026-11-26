# Checks on the fast-track model (`ft_checks.py`)

Generated from `ft_model.py`. Bought parts are envelopes (some sizes are estimates, marked in `ft_model.P`), so a
clash with a bought part's envelope means 'check against the maker's drawing', not a certain clash.

## 1. Interference and the beam, by state

| State | Parts | Clashes | Designed contacts | Beam envelope hits | Nearest parts to the beam (mm) |
|---|---:|---:|---:|---:|---|
| S1 | 13 | 0 | 2 | 0 | - |
| S2 | 31 | 0 | 3 | 0 | Water-cooled beam dump, 500 W 2.7, Cover-slide holder 5.66, Inner clamp ring 8.17, Window ring 8.53 |
| FT-0 | 47 | 0 | 2 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cover-slide holder 5.66, Heater plate Ø39.8 x 28 6.0 |
| FT-1 | 60 | 0 | 3 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cord clamp 3.54, Silicone-cord blade, 3 mm 3.96 |
| FT-1V | 65 | 0 | 4 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cord clamp 3.54, Silicone-cord blade, 3 mm 3.96 |

Designed contacts (FT-1):

| a | b | volume_mm3 | why |
|---|---|---|---|
| Collimator (L2 if the fibre has none) | Process fibre | 4.0 | fibre connector in the collimator |
| IPG YLR-400-SM-EOS (envelope, est.) | Process fibre | 84.9 | fibre leaves the laser's front panel |
| Carriage bracket and arm (MK-08) | Vibration motor | 863.9 | motor clamped on the arm |

## 2. Recoater and piston travel

Hopper parks and the travel it needs (cassette frame, mm):

| beam_r_at_hopper_top_mm | left_park | right_park | travel_needed_mm | X_LSQ075B_travel | X_LSQ150B_travel |
|---|---|---|---|---|---|
| 17.88 | -30.9 | 35.5 | 66.4 | 75.0 | 150.0 |

**FT-1**: recoater swept over ±37.5 mm, 0 clashes. Smallest gaps:

| mover | part | min_gap_mm | at_hx |
|---|---|---|---|
| Carriage bracket and arm (MK-08) | Stage shield (MK-12) | 2.0 | -37.5 |
| Hopper, ~30 cm3 (MK-08) | Well block, Ø40.00 bore (MK-03) | 2.0 | -37.5 |
| Hopper, ~30 cm3 (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 2.0 | -12.5 |
| X-LSQ carriage | Stage shield (MK-12) | 3.0 | -37.5 |
| Cord clamp (MK-08) | Well block, Ø40.00 bore (MK-03) | 3.0 | -25.0 |
| Cord clamp (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 3.0 | -6.2 |

Piston (FT-1): rod 81.6 mm; stroke 20.0 of 20.0 mm; 1 atm on the rod = 12.8 N.

| position | clashes | plate_bottom_above_deck_mm | clamp_top_below_gland_mm | rope_inside_bore |
|---|---|---|---|---|
| pz=-15 | 0 | 3.7 | 23.0 | True |
| pz=+5 | 0 | 23.7 | 3.0 | True |

**FT-1V**: recoater swept over ±37.5 mm, 0 clashes. Smallest gaps:

| mover | part | min_gap_mm | at_hx |
|---|---|---|---|
| Carriage bracket and arm (MK-08) | Stage shield (MK-12) | 2.0 | -37.5 |
| Hopper, ~30 cm3 (MK-08) | Well block, Ø40.00 bore (MK-03) | 2.0 | -37.5 |
| Hopper, ~30 cm3 (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 2.0 | -18.8 |
| X-LSQ carriage | Stage shield (MK-12) | 3.0 | -37.5 |
| Cord clamp (MK-08) | Well block, Ø40.00 bore (MK-03) | 3.0 | -25.0 |
| Cord clamp (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 3.0 | -6.2 |

Piston (FT-1V): rod 102.6 mm; stroke 20.0 of 20.0 mm; 1 atm on the rod = 12.8 N.

| position | clashes | plate_bottom_above_deck_mm | clamp_top_below_gland_mm | rope_inside_bore |
|---|---|---|---|---|
| pz=-15 | 0 | 3.7 | 23.0 | True |
| pz=+5 | 0 | 23.7 | 3.0 | True |

## 3. Fit

| check | value |
|---|---|
| deck_mm | (250.0, 250.0) |
| cube_inside_mm | 289.6 |
| cube_face_opening_mm_est | 266.0 |
| deck_through_opening_margin_mm | 16.0 |
| box_inside_mm | [406.4, 304.8, 203.2] |
| deck_in_box_margins_mm | [78.2, 27.4] |
| X-LSQ075B_length_mm_est | 241.0 |
| X-LSQ075B_fits_cube_square | True |
| X-LSQ075B_fits_deck | True |
| X-LSQ150B_length_mm_est | 316.0 |
| X-LSQ150B_fits_cube_square | False |
| X-LSQ150B_fits_deck | False |
| window_above_bed_box_mm | 145.4 |
| beam_at_window_box_mm | 2.86 |
| window_irradiance_box_kW_cm2_at_400W | 6.2 |
| window_above_bed_cube_mm | 251.8 |
| beam_at_window_cube_mm | 4.96 |
| window_irradiance_cube_kW_cm2_at_400W | 2.1 |
| cassette_height_above_floor_mm | 102.7 |
| cube_inside_height_mm | 289.6 |
| box_inside_height_mm | 203.2 |
| substrate_M3_head_outer_r_mm | 21.0 |
| substrate_M3_fits | False |
| substrate_M2.5_head_outer_r_mm | 20.0 |
| substrate_M2.5_fits | False |
| substrate_M2_head_outer_r_mm | 19.0 |
| substrate_M2_fits | True |

## 4. Gas volume from the model, and purging

| state | inside_L | vendor_L | parts_inside_L | gas_L |
|---|---|---|---|---|
| FT-0 | 25.17 | None | 0.98 | 24.2 |
| FT-1 | 25.17 | None | 1.67 | 23.5 |
| FT-1V | 23.83 | 22.6 | 1.63 | 22.2 |

| state | method | target_ppm | minutes | argon_L |
|---|---|---|---|---|
| FT-0 | flow purge at 20 L/min | 1000 | 6.5 ideal, 13-32 expected | 259-646 |
| FT-0 | flow purge at 20 L/min | 100 | 9.3 ideal, 19-46 expected | 370-925 |
| FT-1 | flow purge at 20 L/min | 1000 | 6.3 ideal, 13-31 expected | 251-628 |
| FT-1 | flow purge at 20 L/min | 100 | 9.0 ideal, 18-45 expected | 359-898 |
| FT-1V | pump to 1 mbar, backfill argon | 100 | 2 cycles x (2.6 min pump + ~1 min fill) = 7 | 44 |
| FT-1V | pump to 1 mbar, backfill argon | 10 | 2 cycles x (2.6 min pump + ~1 min fill) = 7 | 44 |
| FT-1V | pump to 5 mbar, backfill argon | 100 | 2 cycles x (2.0 min pump + ~1 min fill) = 6 | 44 |
| FT-1V | pump to 5 mbar, backfill argon | 10 | 2 cycles x (2.0 min pump + ~1 min fill) = 6 | 44 |

Pump speed (1 L/s effective) and base pressures are estimates; the floor is set by leaks, outgassing and the argon's own O2, which the analyzer measures.

## 5. Enclosure air temperature (same load as `fast_track.py`)

| enclosure | area_m2 | cooling | rise_K | air_C | stage_limit_C |
|---|---|---|---|---|---|
| box (FT-0, FT-1) | 0.537 | still air | 32-46 | 71 | 50.0 |
| box (FT-0, FT-1) | 0.537 | fan | 10-14 | 39 | 50.0 |
| cube (FT-1V) | 0.675 | still air | 25-36 | 61 | 50.0 |
| cube (FT-1V) | 0.675 | fan | 8-11 | 36 | 50.0 |

