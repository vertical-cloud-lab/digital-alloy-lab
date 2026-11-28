# Round 10: the frame audit's pairs over 1.5 mm in chapters 41 and 40, classified (2026-11-27)

Every pair the frame audit (scene_audit.py, every drawn frame, translational depth over 1.5 mm) found is sorted into: **(a)** real clipping a viewer could see, by cause and owner; **(b)** an artifact of the drawn meshes (re-measured at the pair's worst frame with the planner's own 0.1 mm meshes, as analysis/assembly/rec_check.py does, the pair is clear); **(c)** a contact that is meant to be there but is not on the allowed list (fingertips or pads on the part they hold, at most 5 mm). Re-measured with cad/robotbuild/pairs_classify.py, then this file's pairs_classify_md.py (the same translational depth as scene_audit.py, at the recorded poses).

| Chapter | Frames | Pairs | (a) real | (b) mesh artifact | (c) intended | Round 9 pairs |
|---|---:|---:|---:|---:|---:|---:|
| 41-assembly-chamber | 12821 | 74 | 0 | 62 | 12 | 238 |
| 40-assembly-module | 2983 | 9 | 0 | 9 | 0 | 29 |

## 41-assembly-chamber: 74 pairs

Frames audited: 12821. Against round 9's 238 pairs: 12 in both, 226 gone, 62 new.

| Class | Pairs | What it is |
|---|---:|---|
| (a) real clipping | 0 | by cause (pairs; distinct frames): none |
| (b) drawn-mesh artifact or model | 62 | 62 a screw at its pick in the screw presenter, which is modelled as a solid envelope without its nest; 0 clear on the planner's 0.1 mm meshes |
| (c) intended contact | 12 | fingertips on the part they hold, within 5 mm |

Class (a) by depth: 0 pairs 1.5-5 mm, 0 pairs 5-10 mm, 0 pairs 10-20 mm, 0 over 20 mm.

Frames with any class-(a) pair: 0 of 12821 (0.0 %; frame ranges are capped at 40 per pair in the audit JSON, so this is a lower bound).

### (b) drawn-mesh artifacts: the largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| mirA/A screw presenter () x o410 (Optics-bridge screws, M6 x 35 316 ) | mirA x shcs | 34.4 | 34.4 | 4 (11902-11905) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o396 (Base-plate-to-leg screws, M6 x 25 ) | mirA x shcs | 24.2 | 24.2 | 3 (4126-4128) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirB/B screw presenter () x o196 (Lid screws, M5 x 25 316 socket hea) | mirB x shcs | 24.2 | 24.2 | 3 (7398-7400) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirB/B screw presenter () x o204 (Lid screws, M5 x 25 316 socket hea) | mirB x shcs | 24.2 | 24.2 | 3 (7451-7453) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o195 (Lid screws, M5 x 25 316 socket hea) | mirA x shcs | 24.2 | 24.2 | 3 (7515-7517) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o418 (Optics-post base screws, M6 x 25 3) | mirA x shcs | 24.2 | 24.2 | 3 (11018-11020) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o419 (Optics-post base screws, M6 x 25 3) | mirA x shcs | 24.2 | 24.2 | 3 (11051-11053) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirB/B screw presenter () x o420 (Optics-post base screws, M6 x 25 3) | mirB x shcs | 24.2 | 24.2 | 3 (11122-11124) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |

### (c) intended contacts: the largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| B/cap/ring/left_finger_tip () x o96 (Window O-ring, lower (FKM 75A 2-03) | fingers x part | 4.7 | 4.7 | 22 (8165-8186) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/cap/ring/right_finger_tip () x o96 (Window O-ring, lower (FKM 75A 2-03) | fingers x part | 4.7 | 4.7 | 22 (8165-8186) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/0 () x o95 (Ø2 in. fused-silica window, 9.53 m) | fingers x part | 3.4 | 3.4 | 2 (8494-8495) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/0 () x o95 (Ø2 in. fused-silica window, 9.53 m) | fingers x part | 3.4 | 3.4 | 2 (8494-8495) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/gr/left_finger_tip/0 () x o78 (Recoater carriage block (6061)) | fingers x part | 2.9 | 2.9 | 5 (6043-6044; 6187-6189) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/gr/right_finger_tip/0 () x o78 (Recoater carriage block (6061)) | fingers x part | 2.9 | 2.9 | 5 (6043-6044; 6187-6189) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/gr/left_finger_tip/0 () x o96 (Window O-ring, lower (FKM 75A 2-03) | fingers x part | 2.2 | 2.2 | 22 (8165-8186) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/gr/right_finger_tip/0 () x o96 (Window O-ring, lower (FKM 75A 2-03) | fingers x part | 2.2 | 2.2 | 22 (8165-8186) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |

## 40-assembly-module: 9 pairs

Frames audited: 2983. Against round 9's 29 pairs: 0 in both, 29 gone, 9 new.

| Class | Pairs | What it is |
|---|---:|---|
| (a) real clipping | 0 | by cause (pairs; distinct frames): none |
| (b) drawn-mesh artifact or model | 9 | 9 a screw at its pick in the screw presenter, which is modelled as a solid envelope without its nest; 0 clear on the planner's 0.1 mm meshes |
| (c) intended contact | 0 | fingertips on the part they hold, within 5 mm |

Class (a) by depth: 0 pairs 1.5-5 mm, 0 pairs 5-10 mm, 0 pairs 10-20 mm, 0 over 20 mm.

Frames with any class-(a) pair: 0 of 2983 (0.0 %; frame ranges are capped at 40 per pair in the audit JSON, so this is a lower bound).

### (b) drawn-mesh artifacts: the largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| mirA/A screw presenter () x o259 (Heater-stack screws M50, M3 x 25 3) | mirA x shcs | 22.6 | 22.6 | 2 (981-982) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirB/B screw presenter () x o271 (Gland-plate screws M50, M4 x 20 31) | mirB x shcs | 18.5 | 18.5 | 2 (2233-2234) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o268 (Gland-plate screws M50, M4 x 20 31) | mirA x shcs | 18.5 | 18.5 | 2 (2285-2286) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o276 (od set screws M50, M4 cup point 31) | mirA x set | 10.5 | 10.5 | 1 (1728-1728) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o274 (Handle screws M50, M4 x 10 316 #1) | mirA x shcs | 7.9 | 7.9 | 1 (2427-2427) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o278 (Striker screws M50, M3 x 10 316 fl) | mirA x fhcs | 4.7 | 4.7 | 1 (2550-2550) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o269 (Gland-plate screws M50, M4 x 20 31) | mirA x shcs | 2.0 | 2.0 | 1 (2328-2328) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |
| mirA/A screw presenter () x o272 (Gland-plate screws M50, M4 x 20 31) | mirA x shcs | 2.0 | 2.0 | 1 (2345-2345) | model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid 250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads the same depth on the planner's meshes |

