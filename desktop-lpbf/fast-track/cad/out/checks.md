# Checks on the fast-track model (`ft_checks.py`)

Generated from `ft_model.py` with the gantry `P['gantry'] = "four_post_braced_front_g3"` (the g3 frame: the head's far face held from both cross-beams, the default since round 3, 2026-11-28).
The stages are drawn from Zaber's and Thorlabs' STEP files, the box,
head and lens from their makers' drawings (`ft_vendor.py`, `out/vendor-verify.json`); other bought parts are
envelopes (sizes marked in `ft_model.P`). A clash with an envelope means 'check the maker's drawing'.

## 1. Interference and the beam, by state

| State | Parts | Clashes | Designed contacts | Beam envelope hits | Nearest parts to the beam (mm) |
|---|---:|---:|---:|---:|---|
| S1 | 29 | 0 | 6 | 0 | - |
| S2 | 53 | 0 | 8 | 0 | Water-cooled beam dump, 1 kW 2.7, Cover-slide holder, Ø44 opening 5.6, Window retaining flange 7.04, Window ring 7.53 |
| FT-0 | 88 | 0 | 10 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cover-slide holder, Ø44 opening 5.6, FT-0 spreader bar, 48 mm, ground edge, parked 5.9 |
| FT-1 | 106 | 0 | 10 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cord clamp 3.52, Silicone-cord blade, 3 mm 3.96 |
| FT-1V | 108 | 0 | 11 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cord clamp 3.52, Silicone-cord blade, 3 mm 3.96 |
| FT-1 (Thorlabs piston) | 105 | 0 | 10 | 0 | Well block, Ø40.00 bore 0.0, Substrate disc Ø39.8 x 6 0.0, Cord clamp 3.52, Silicone-cord blade, 3 mm 3.96 |

Designed contacts (FT-1):

| a | b | volume_mm3 | why |
|---|---|---|---|
| Gantry uprights | Gantry braces: a diagonal per side, two knee braces at the back | 5294.3 | brace bolted to the post |
| Gantry uprights | Gantry knee braces, front (2) | 1312.0 | brace bolted to the post |
| Gantry cross-beam (clamped at the head height) | Gantry braces: a diagonal per side, two knee braces at the back | 1891.4 | knee brace bolted under the cross-beam |
| Gantry cross-beam, front (under the head plate's front end) | Gantry knee braces, front (2) | 1891.4 | knee brace bolted under the cross-beam |
| Scan-head flange plate (MK-09) | Head-plate top flange on both cross-beams (MK-09) | 43084.8 | top flange welded to the flange plate |
| Fibre bend restrictor | Process fibre | 563.1 | fibre in its bend restrictor |
| Window retaining flange (MK-02) | Window-stack screws, M4 x 12 flat head, flush | 443.2 | screws |
| Rod gland plate, 2 O-rings (MK-07) | Gland screws M5 x 25 with bonded seals (4) | 1134.9 | screws |
| IP68 cable glands M16 (2, back wall) | Recoater M8 data and power cable | 245.3 | cable through the gland |
| Layer camera: Pi HQ, C-mount lens, FESH1000 (MON1) | Camera post, arm and foot (MK-20) | 242.9 | clamp on the camera's mount ring |

**Apertures round the scanned beam** (lens axis at (0, -30); envelope = chief rays from the mirrors, est. 392.9 mm above the bed, to the Ø40 field, plus the beam's own half-width):

| state | element | height_above_bed_mm | envelope_r_mm | offset_mm | opening_r_mm | margin_mm |
|---|---|---|---|---|---|---|
| S2 | window (ring ledge / flange Ø44) | 152.0 | 13.86 | 0.61 | 22.0 | 7.54 |
| S2 | window top | 161.6 | 13.46 | 1.34 | 22.0 | 7.2 |
| S2 | cover slide holder (Ø44) | 130.0 | 14.76 | 1.07 | 22.0 | 6.17 |
| S2 | beam tube lower spigot (Ø50) | 166.0 | 13.28 | 4.32 | 25.0 | 7.4 |
| S2 | beam tube upper spigot (Ø50) | 286.5 | 8.33 | 4.88 | 25.0 | 11.79 |
| FT-1 | window (ring ledge / flange Ø44) | 152.0 | 13.86 | 0.61 | 22.0 | 7.54 |
| FT-1 | window top | 161.6 | 13.46 | 1.34 | 22.0 | 7.2 |
| FT-1 | cover slide holder (Ø44) | 130.0 | 14.76 | 1.07 | 22.0 | 6.17 |
| FT-1 | beam tube lower spigot (Ø50) | 166.0 | 13.28 | 4.32 | 25.0 | 7.4 |
| FT-1 | beam tube upper spigot (Ø50) | 286.5 | 8.33 | 4.88 | 25.0 | 11.79 |
| FT-1V | window (ring ledge / flange Ø44) | 251.8 | 9.76 | 1.77 | 22.0 | 10.47 |
| FT-1V | window top | 261.3 | 9.37 | 1.05 | 22.0 | 11.59 |
| FT-1V | cover slide holder (Ø44) | 130.0 | 14.76 | 1.07 | 22.0 | 6.17 |
| FT-1V | beam tube lower spigot (Ø50) | 265.8 | 9.18 | 3.7 | 25.0 | 12.11 |
| FT-1V | beam tube upper spigot (Ø50) | 286.5 | 8.33 | 2.12 | 25.0 | 14.54 |

## 2. Recoater and piston travel

Hopper parks and the travel it needs (cassette frame, mm):

| beam_r_at_hopper_top_mm | left_park | right_park | travel_needed_mm | stage_travel_mm | travel_range | spare_left_mm | spare_right_mm |
|---|---|---|---|---|---|---|---|
| 18.13 | -31.1 | 35.5 | 66.6 | 101.6 | (-45.8, 55.8) | 14.7 | 20.3 |

**FT-1**: recoater swept over its 101.6 mm (exact booleans, 13 positions), 0 clashes. Smallest gaps:

| mover | part | min_gap_mm | at_hx |
|---|---|---|---|
| Carriage bracket and arm (MK-08) | Stage shield (MK-12) | 2.0 | -45.8 |
| X-LSM carriage | Stage shield (MK-12) | 3.0 | -45.8 |
| Cord clamp (MK-08) | Well block, Ø40.00 bore (MK-03) | 3.0 | -28.9 |
| Cord clamp (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 3.0 | -3.5 |
| X-LSM carriage | Deck plate (MK-01) | 3.77 | -45.8 |
| Hopper, ~30 cm3 (MK-08) | Slot nozzle 45 x 4 mm (MK-11) | 4.0 | -37.3 |

Piston (FT-1): rod 84.6 mm; stroke 20.0 of 20.0 mm; 1 atm on the rod = 12.8 N.

| position | clashes | plate_bottom_above_deck_mm | block_top_below_gland_mm | rope_inside_bore |
|---|---|---|---|---|
| pz=-15 | 0 | 7.7 | 23.0 | True |
| pz=+5 | 0 | 27.7 | 3.0 | True |

**FT-1V**: recoater swept over its 101.6 mm (exact booleans, 13 positions), 0 clashes. Smallest gaps:

| mover | part | min_gap_mm | at_hx |
|---|---|---|---|
| Carriage bracket and arm (MK-08) | Stage shield (MK-12) | 2.0 | -45.8 |
| X-LSM carriage | Stage shield (MK-12) | 3.0 | -45.8 |
| Cord clamp (MK-08) | Well block, Ø40.00 bore (MK-03) | 3.0 | -28.9 |
| Cord clamp (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 3.0 | -3.5 |
| X-LSM carriage | Deck plate (MK-01) | 3.77 | -45.8 |
| Hopper, ~30 cm3 (MK-08) | Slot nozzle 45 x 4 mm (MK-11) | 4.0 | -37.3 |

Piston (FT-1V): rod 105.6 mm; stroke 20.0 of 20.0 mm; 1 atm on the rod = 12.8 N.

| position | clashes | plate_bottom_above_deck_mm | block_top_below_gland_mm | rope_inside_bore |
|---|---|---|---|---|
| pz=-15 | 0 | 7.7 | 23.0 | True |
| pz=+5 | 0 | 27.7 | 3.0 | True |

Piston, Thorlabs MTS50/M-Z8 on end (FT-1):

| position | clashes | plate_bottom_above_deck_mm | block_top_below_gland_mm | rope_inside_bore |
|---|---|---|---|---|
| pz=-15 | 0 | 7.7 | 23.0 | True |
| pz=+5 | 0 | 27.7 | 3.0 | True |

## 3. Mesh sweep with python-fcl

Each moving group tessellated once (0.4 mm) and moved in fine steps against every static part's BVH mesh;
designed contacts and the cord on the block top are left out.

**FT-1, recoater**: 41 poses, 0 contacts. Nearest pairs:

| mover | part | min_dist_mm | at |
|---|---|---|---|
| Carriage bracket and arm (MK-08) | Stage shield (MK-12) | 2.0 | -50.8 |
| Hopper, ~30 cm3 (MK-08) | Well block, Ø40.00 bore (MK-03) | 2.0 | -25.8 |
| Hopper, ~30 cm3 (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 2.0 | -23.3 |
| X-LSM carriage | Stage shield (MK-12) | 3.0 | -50.8 |
| Cord clamp (MK-08) | Well block, Ø40.00 bore (MK-03) | 3.0 | -13.3 |
| Cord clamp (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 3.0 | -13.3 |

**FT-1, piston**: 21 poses, 0 contacts. Nearest pairs:

| mover | part | min_dist_mm | at |
|---|---|---|---|
| Piston rod (MK-06) | Rod gland plate, 2 O-rings (MK-07) | 0.09 | -15.0 |
| Substrate disc Ø39.8 x 6 (MK-05) | Well block, Ø40.00 bore (MK-03) | 0.1 | 0.0 |
| Heater plate Ø39.8 x 24 (MK-04) | Well block, Ø40.00 bore (MK-03) | 0.1 | -6.0 |
| Heater plate Ø39.8 x 24 (MK-04) | Overflow cup (MK-16) | 1.6 | -15.0 |
| Rod-end block: clamp, lead pocket, AE face (MK-15) | Rod gland plate, 2 O-rings (MK-07) | 3.0 | 5.0 |
| Rod-end block: clamp, lead pocket, AE face (MK-15) | Gland screws M5 x 25 with bonded seals (4) | 3.0 | 5.0 |

**FT-1V, recoater**: 41 poses, 0 contacts. Nearest pairs:

| mover | part | min_dist_mm | at |
|---|---|---|---|
| Carriage bracket and arm (MK-08) | Stage shield (MK-12) | 2.0 | -50.8 |
| Hopper, ~30 cm3 (MK-08) | Well block, Ø40.00 bore (MK-03) | 2.0 | -45.8 |
| Hopper, ~30 cm3 (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 2.0 | -25.8 |
| X-LSM carriage | Stage shield (MK-12) | 3.0 | -50.8 |
| Cord clamp (MK-08) | Well block, Ø40.00 bore (MK-03) | 3.0 | -33.3 |
| Cord clamp (MK-08) | Substrate disc Ø39.8 x 6 (MK-05) | 3.0 | -13.3 |

**FT-1V, piston**: 21 poses, 0 contacts. Nearest pairs:

| mover | part | min_dist_mm | at |
|---|---|---|---|
| Piston rod, long, for the cube (MK-06) | Rod gland plate, 2 O-rings (MK-07) | 0.09 | -15.0 |
| Substrate disc Ø39.8 x 6 (MK-05) | Well block, Ø40.00 bore (MK-03) | 0.1 | 0.0 |
| Heater plate Ø39.8 x 24 (MK-04) | Well block, Ø40.00 bore (MK-03) | 0.1 | -1.0 |
| Heater plate Ø39.8 x 24 (MK-04) | Overflow cup (MK-16) | 1.6 | -15.0 |
| Rod-end block: clamp, lead pocket, AE face (MK-15) | Rod gland plate, 2 O-rings (MK-07) | 3.0 | 5.0 |
| Rod-end block: clamp, lead pocket, AE face (MK-15) | Gland screws M5 x 25 with bonded seals (4) | 3.0 | 5.0 |

**Box door (FT-1) opened about its hinges, with the layer camera on its post** (axis est. at y 192.7, z 150.0; the beam tube's centre section off): free to **24.0 deg**, the front edge then 120.2 mm up.

First contact at 25.0 deg:

| pose | mover | part |
|---|---|---|
| 25.0 | Layer camera: Pi HQ, C-mount lens, FESH1000 (MON1) | Beam-tube lens collar, clamped on the lens (MK-10) |

**Box door (FT-1) opened about its hinges, with the camera unclipped** (axis est. at y 192.7, z 150.0; the beam tube's centre section off): free to **26.0 deg**, the front edge then 129.5 mm up.

First contact at 27.0 deg:

| pose | mover | part |
|---|---|---|
| 27.0 | Quarter-turn latch | Beam-tube lens collar, clamped on the lens (MK-10) |

**Beam tube's centre section, the two half-shells slid straight out sideways with no lift** (python-fcl, 2 mm steps over 60 mm (a half-shell is 30 mm wide) against every fixed part; both locating spigots are inside the bore, and the window-stack screws are countersunk flush):

| state | half_shell | contacts | section_length_mm | nearest |
|---|---|---|---|---|
| FT-1 | -x half-shell | 0 | 123.5 | Window retaining flange 0.2, Window-stack screws, M4 x 12 flat head, flush 0.2, Beam-tube lens collar, clamped on the lens 0.2 |
| FT-1 | +x half-shell | 0 | 123.5 | Window retaining flange 0.2, Window-stack screws, M4 x 12 flat head, flush 0.2, Beam-tube lens collar, clamped on the lens 0.2 |
| FT-1V | -y half-shell | 0 | 23.7 | Window retaining flange 0.2, Window-stack screws, M4 x 12 flat head, flush 0.2, Beam-tube lens collar, clamped on the lens 0.2 |
| FT-1V | +y half-shell | 0 | 23.7 | Window retaining flange 0.2, Window-stack screws, M4 x 12 flat head, flush 0.2, Beam-tube lens collar, clamped on the lens 0.2 |

**Taking the box off the frame (FT-1 -> FT-1V)**, numbers from the model (plate at the top of its stroke):

| check | value |
|---|---|
| gland_bottom_below_rail_tops_mm | 12.0 |
| rod_in_rod_end_block_mm | 22.0 |
| rod_length_box_mm | 84.6 |
| rod_length_cube_mm | 105.6 |
| rod_bottom_below_block_top_at_pz_top_mm | 101.6 |
| lift_to_free_rod_from_bore_mm | 103.6 |
| block_top_below_gland_at_pz_top_mm | 3.0 |
| block_top_below_gland_at_pz_bot_mm | 23.0 |

## 4. Sight lines and the layer camera

Rays from 133 points on the plate (Ø38) to the camera's lens front and to each light's port; a ray is blocked if it meets any part (windows, the camera and the lights themselves excluded).

| state | hopper | camera_sees_pct | MON2_lights_pct | MON3_lights_pct |
|---|---|---|---|---|
| FT-0 | hopper at the right park (hx 37.5) | 100.0 | 100.0 | 90.8 |
| FT-0 | hopper at the left park (hx -33.1) | 100.0 | 100.0 | 90.8 |
| FT-1 | hopper at the right park (hx 37.5) | 100.0 | 100.0 | 90.8 |
| FT-1 | hopper at the left park (hx -33.1) | 78.0 | 0.0 | 90.8 |
| FT-1V | hopper at the right park (hx 37.5) | 100.0 | 100.0 | 92.7 |
| FT-1V | hopper at the left park (hx -33.1) | 82.6 | 0.0 | 92.7 |

Camera (IMX477, 1.55 um pixels; f/2.8; circle of confusion two pixels):

| state | lens_f_mm | tilt_deg | distance_mm | um_per_px_across | um_per_px_along | field_mm | scheimpflug_deg | dof_mm_f2_8 | plate_depth_range_mm | rayleigh_um_f2_8 | video_2028x1520_40fps_um_px |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FT-0 | 16.0 | 30.7 | 199.4 | 17.8 | 20.7 | [72.1, 54.0] | 2.96 | 2.48 | 20.4 | 21.5 | 35.5 |
| FT-1V | 25.0 | 24.1 | 298.7 | 17.0 | 18.6 | [68.8, 51.6] | 2.34 | 2.27 | 16.3 | 20.6 | 33.9 |

## 5. Fit

| check | value |
|---|---|
| deck_mm | (245.0, 245.0) |
| box_inside_mm | [402.6, 301.0, 210.8] |
| box_door_opening_mm_est | [358.6, 257.0] |
| deck_in_box_margins_mm | [78.8, 28.0] |
| cube_inside_mm | 289.6 |
| cube_face_opening_mm_est | 266.0 |
| deck_through_opening_margin_mm | 21.0 |
| cube_opening_needed_mm | 247.0 |
| lesker_bx1212s_inside_mm | 304.8 |
| deck_in_lesker_margin_mm | 29.9 |
| X-LSM100B-E03 (used)_length_mm | 239.2 |
| X-LSM100B-E03 (used)_fits_deck | True |
| X-LSM100B-E03 (used)_fits_cube_inside | True |
| X-LSQ075B-E01 (rejected)_length_mm | 285.85 |
| X-LSQ075B-E01 (rejected)_fits_deck | False |
| X-LSQ075B-E01 (rejected)_fits_cube_inside | False |
| X-LSQ150B-E01 (rejected)_length_mm | 360.9 |
| X-LSQ150B-E01 (rejected)_fits_deck | False |
| X-LSQ150B-E01 (rejected)_fits_cube_inside | False |
| window_above_bed_box_mm | 152.0 |
| beam_at_window_box_mm | 2.99 |
| window_irradiance_box_kW_cm2_at_400W | 5.7 |
| cover_slide_above_bed_box_mm | 130.0 |
| window_above_bed_cube_mm | 251.8 |
| beam_at_window_cube_mm | 4.95 |
| window_irradiance_cube_kW_cm2_at_400W | 2.1 |
| cover_slide_above_bed_cube_mm | 130.0 |
| cassette_height_above_floor_mm | 107.7 |
| cube_inside_height_mm | 289.6 |
| box_inside_height_mm | 210.8 |
| head_top_above_bed_box_mm | 528.1 |
| head_top_above_bed_cube_mm | 528.1 |
| substrate_M3_head_outer_r_mm | 21.0 |
| substrate_M3_fits | False |
| substrate_M2.5_head_outer_r_mm | 20.0 |
| substrate_M2.5_fits | False |
| substrate_M2_head_outer_r_mm | 19.0 |
| substrate_M2_fits | True |
| plate_heater_holes_mm | 2 x Ø6.1 x 21.0 deep in a 24.0 mm plate |

## 6. Gas volume from the model, and purging

| state | inside_L | vendor_L | parts_inside_L | gas_L |
|---|---|---|---|---|
| FT-0 | 25.29 | None | 1.05 | 24.24 |
| FT-1 | 25.29 | None | 1.25 | 24.04 |
| FT-1V | 23.83 | 22.6 | 1.19 | 22.64 |

| state | method | target_ppm | minutes | argon_L |
|---|---|---|---|---|
| FT-0 | flow purge at 20 L/min | 1000 | 6.5 ideal, 13-32 expected | 259-647 |
| FT-0 | flow purge at 20 L/min | 100 | 9.3 ideal, 19-46 expected | 371-927 |
| FT-1 | flow purge at 20 L/min | 1000 | 6.4 ideal, 13-32 expected | 257-642 |
| FT-1 | flow purge at 20 L/min | 100 | 9.2 ideal, 18-46 expected | 368-919 |
| FT-1V | pump to 1 mbar, backfill argon | 100 | 2 cycles x (2.6 min pump + ~1 min fill) = 7 | 45 |
| FT-1V | pump to 1 mbar, backfill argon | 10 | 2 cycles x (2.6 min pump + ~1 min fill) = 7 | 45 |
| FT-1V | pump to 5 mbar, backfill argon | 100 | 2 cycles x (2.0 min pump + ~1 min fill) = 6 | 45 |
| FT-1V | pump to 5 mbar, backfill argon | 10 | 2 cycles x (2.0 min pump + ~1 min fill) = 6 | 45 |

Pump speed (1 L/s effective) and base pressures are estimates; the floor is set by leaks, outgassing and the argon's own O2, which the analyzer measures.

## 7. Enclosure air temperature (same load as `fast_track.py`)

| enclosure | area_m2 | cooling | rise_K | air_C | stage_limit_C |
|---|---|---|---|---|---|
| box (FT-0, FT-1) | 0.537 | still air | 32-46 | 71 | 50.0 |
| box (FT-0, FT-1) | 0.537 | fan | 10-14 | 39 | 50.0 |
| cube (FT-1V) | 0.675 | still air | 25-36 | 61 | 50.0 |
| cube (FT-1V) | 0.675 | fan | 8-11 | 36 | 50.0 |

Run time 655 s.
