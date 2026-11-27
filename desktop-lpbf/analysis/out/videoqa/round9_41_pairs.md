# Round 9: the frame audit's pairs over 1.5 mm in chapters 41 and 40, classified (2026-11-27)

Chapter 41's audit went from 209 pairs (round 8) to 238, and chapter 40's from 221 to 29. This sorts every pair into: **(a)** real clipping a viewer could see; **(b)** an artifact of the drawn meshes (the renderer draws each part decimated to at most 12,000 triangles; re-measured at the pair's worst frame with the planner's own 0.1 mm meshes, as analysis/assembly/rec_check.py does, the pair is clear); **(c)** a contact that is meant to be there but is not on the allowed list (fingertips or pads on the part they hold, at most 5 mm, the part moving with the fingers). Re-measured with cad/robotbuild/pairs_classify.py (then pairs_classify_md.py) (the same translational depth as scene_audit.py, at the recorded poses).

| Chapter | Pairs | (a) real | (b) mesh artifact | (c) intended |
|---|---:|---:|---:|---:|
| 41-assembly-chamber | 238 | 175 | 0 | 63 |
| 40-assembly-module | 29 | 17 | 0 | 12 |

Why 41's count rose (round 8: 209 pairs, 10,325 frames; round 9: 238, 13,640 frames): 138 pairs are in both rounds; 71 of round 8's are gone (the hoist hook in the build module, 22; parts in parts, 25; fingers in parts, 11; the wrist and a gripper, the stretchers, the jaws in their stands, the person in MiR A's tool stand, the seal tools); 100 are new, 76 of them fingertips on parts and 22 parts in parts. No pair is a decimation artifact any more: round 9 draws each part at the scene file's 12,000 triangles (round 8 drew 2,500, which closed bores and counterbores), and only 11 parts have more than that (hoses, the chamber body, the floor plate, two servos); every pair re-measured on the planner's own meshes reads the same depth. The fingertip pairs are new partly because the parts are now drawn with their true surfaces, which the fingertips' closed pads meet, and partly from run 13/14's re-planned grasps (pick, push home with the fingers closed).

## 41-assembly-chamber: 238 pairs

| Class | Pairs | What it is |
|---|---:|---|
| (a) real clipping | 175 | by cause (pairs; distinct frames): part in part, away from its seat 73 (632 fr); fingers closed past the part (> 5 mm) 45 (443 fr); staged put into the table top 30 (11 fr); part just off its seat (<= 6 mm) 16 (464 fr); tool through the part it works on 7 (191 fr); person's hands (renderer) 2 (39 fr); arm link through a screw 2 (10 fr) |
| (b) drawn-mesh artifact | 0 | clear on the planner's 0.1 mm meshes |
| (c) intended contact | 63 | fingertips on the part they hold, within 5 mm |

Class (a) by depth: 41 pairs 1.5-5 mm, 74 pairs 5-10 mm, 49 pairs 10-20 mm, 11 over 20 mm.

Frames with any class-(a) pair: 1278 of 13640 (9.4 %; frame ranges are capped at 40 per pair in the audit JSON, so this is a lower bound). The fixes, by owner: the plan (run_assembly.py and its checks; W3): stage dual carries at the table slot, check tools and parts against the part being placed along insertion paths, close grasps only to the part's width; the renderer (asm_render.py; W4): the person's hand targets 20 mm outside the part, and the release fix already in 118a9b3 (re-render 41's slices 0-10 to apply it).

### (a) real clipping: the 10 largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| kt/long table top () x o253 ( Floor-plate dowels, Ø6 x 20 316 #) | kt x dowel | 40.6 | 40.6 | 4 (277-280) | plan: the dual carry's 'staged' put sets the part at the carry's first pose, which sinks it into the long table's top; fix: stage it at its table slot (or lift the carry's first pose clear of the top) |
| kt/long table top () x o254 ( Floor-plate dowels, Ø6 x 20 316 #) | kt x dowel | 40.6 | 40.6 | 4 (277-280) | plan: the dual carry's 'staged' put sets the part at the carry's first pose, which sinks it into the long table's top; fix: stage it at its table slot (or lift the carry's first pose clear of the top) |
| o53 (Process chamber body (6061-T6 thro) x o68 (Lift-out wall liner, right (0.5 mm) | part x part | 37.5 | 37.5 | 14 (5444-5457) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| o53 (Process chamber body (6061-T6 thro) x op/glove () | part x person | 28.1 | 28.1 | 15 (6078-6092) | renderer: the person's hand targets after a failed step reach into the part (people.py's fingers curl past the surface); fix: aim the hands at the part's outside, 20 mm off it |
| o53 (Process chamber body (6061-T6 thro) x o93 (Chamber lid (6061-T6, 16 mm, cover) | part x part | 24.2 | 24.2 | 2 (8345-8346) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| kt/long table top () x o54 (Chamber floor plate (6061-T6, 20 m) | kt x part | 23.4 | 23.4 | 4 (277-280) | plan: the dual carry's 'staged' put sets the part at the carry's first pose, which sinks it into the long table's top; fix: stage it at its table slot (or lift the carry's first pose clear of the top) |
| A/tool/ringpad/0/None () x o129 (Camera window (Ø1 in. x 3 mm fused) | arm tool x part | 21.8 | 21.8 | 12 (10874-10885) | plan: the tool's path (liner wand, ring pad, pin rod, nutrunner) passes through the part it works on; fix: check the tool body against that part in the planner (it is excluded as the step's own part) |
| o481 (Zero-point posts #1) x o485 (Zero-point module plates #1) | part x part | 20.1 | 20.1 | 8 (2340-2347) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| o482 (Zero-point posts #2) x o485 (Zero-point module plates #1) | part x part | 20.1 | 20.1 | 8 (2340-2347) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| A/tool/wand/0/None () x o71 (Lift-out wall liner, back lower le) | arm tool x part | 20.1 | 20.1 | 32 (5081-5112) | plan: the tool's path (liner wand, ring pad, pin rod, nutrunner) passes through the part it works on; fix: check the tool body against that part in the planner (it is excluded as the step's own part) |

### (c) intended contacts: the 10 largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| A/gr/right_finger_tip/0 () x o65 (Vacuum port adapter O-ring (FKM 75) | fingers x part | 4.9 | 4.9 | 1 (6238-6238) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/cap/ring/left_finger_tip () x o94 (Window flange (6061, two FKM O-rin) | fingers x part | 4.9 | 4.9 | 9 (9194-9202) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/cap/ring/right_finger_tip () x o94 (Window flange (6061, two FKM O-rin) | fingers x part | 4.9 | 4.9 | 9 (9194-9202) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/0 () x o109 (Metering base (6061, fluted roller) | fingers x part | 4.9 | 4.9 | 12 (10529-10535; 10546-10549; 10582-10582) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/0 () x o109 (Metering base (6061, fluted roller) | fingers x part | 4.9 | 4.9 | 12 (10529-10535; 10546-10549; 10582-10582) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/1 () x o144 (Door handle) | fingers x part | 4.9 | 4.9 | 21 (11255-11275) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/1 () x o144 (Door handle) | fingers x part | 4.9 | 4.9 | 21 (11255-11275) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/1 () x o95 (Ø2 in. fused-silica window, 9.53 m) | fingers x part | 4.5 | 4.5 | 2 (9287-9288) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/1 () x o95 (Ø2 in. fused-silica window, 9.53 m) | fingers x part | 4.5 | 4.5 | 2 (9287-9288) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/1 () x o62 (Outlet plenum port (KF-25)) | fingers x part | 3.9 | 3.9 | 21 (4120-4137; 4226-4228) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |

## 40-assembly-module: 29 pairs

| Class | Pairs | What it is |
|---|---:|---|
| (a) real clipping | 17 | by cause (pairs; distinct frames): part in part, away from its seat 6 (2 fr); part just off its seat (<= 6 mm) 6 (24 fr); fingers closed past the part (> 5 mm) 5 (7 fr) |
| (b) drawn-mesh artifact | 0 | clear on the planner's 0.1 mm meshes |
| (c) intended contact | 12 | fingertips on the part they hold, within 5 mm |

Class (a) by depth: 9 pairs 1.5-5 mm, 6 pairs 5-10 mm, 2 pairs 10-20 mm, 0 over 20 mm.

Frames with any class-(a) pair: 33 of 2974 (1.1 %; frame ranges are capped at 40 per pair in the audit JSON, so this is a lower bound). The fixes, by owner: the plan (run_assembly.py and its checks; W3): stage dual carries at the table slot, check tools and parts against the part being placed along insertion paths, close grasps only to the part's width; the renderer (asm_render.py; W4): the person's hand targets 20 mm outside the part, and the release fix already in 118a9b3 (re-render 41's slices 0-10 to apply it).

### (a) real clipping: the 10 largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| A/gr/left_finger_tip/0 () x o24 (Module M50 handle (6061, screwed u) | fingers x part | 10.5 | 10.5 | 4 (2644-2645; 2804-2805) | plan: the recorded grasp closes the fingers past the part's surface (deeper than the pads' compliance); fix: close to the part's width at the grasp (record the opening the checker used) |
| A/gr/right_finger_tip/0 () x o24 (Module M50 handle (6061, screwed u) | fingers x part | 10.5 | 10.5 | 4 (2644-2645; 2804-2805) | plan: the recorded grasp closes the fingers past the part's surface (deeper than the pads' compliance); fix: close to the part's width at the grasp (record the opening the checker used) |
| A/gr/left_finger_tip/0 () x o39 (Striker disc M50 (416 stainless, o) | fingers x part | 7.5 | 7.5 | 2 (2495-2496) | plan: the recorded grasp closes the fingers past the part's surface (deeper than the pads' compliance); fix: close to the part's width at the grasp (record the opening the checker used) |
| A/gr/right_finger_tip/0 () x o39 (Striker disc M50 (416 stainless, o) | fingers x part | 7.5 | 7.5 | 2 (2495-2496) | plan: the recorded grasp closes the fingers past the part's surface (deeper than the pads' compliance); fix: close to the part's width at the grasp (record the opening the checker used) |
| o29 (Heater block M50 (6061-T6, bayonet) x o30 (Cartridge heaters M50 (3 x 50 W, 2) | part x part | 6.4 | 6.4 | 1 (423-423) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| o19 (Build module M50: spigot, flange, ) x o28 (Plate rim wiper M50 (carbon-filled) | part x part | 6.4 | 6.4 | 1 (2751-2751) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| A/gr/right_finger_tip/0 () x o30 (Cartridge heaters M50 (3 x 50 W, 2) | fingers x part | 5.4 | 5.4 | 1 (421-421) | plan: the recorded grasp closes the fingers past the part's surface (deeper than the pads' compliance); fix: close to the part's width at the grasp (record the opening the checker used) |
| o30 (Cartridge heaters M50 (3 x 50 W, 2) x st/Stack nest () | part x st | 5.4 | 5.4 | 1 (423-423) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| o27 (Build plate M50 (Ø50.5 x 10, 6061-) x o29 (Heater block M50 (6061-T6, bayonet) | part x part | 4.7 | 4.7 | 1 (2751-2751) | plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release a few mm off the seat); fix: check part against part along insertion paths, and seat on release |
| o29 (Heater block M50 (6061-T6, bayonet) x o472 (Macor standoff rings M50 #3) | part x part | 3.8 | 3.8 | 6 (676-681) | plan or renderer: the part is 3.73 mm off its designed pose, at the end of a placement (the insertion's last frames) or left off its seat at a release; fix: the release fix in asm_render.py (118a9b3: a held part keeps the grasp's finger closure; 41's slices 0-10 were drawn before it), and insertions that end exactly on the seat |

### (c) intended contacts: the 10 largest

| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |
|---|---|---:|---:|---|---|
| A/gr/left_finger_tip/1 () x o24 (Module M50 handle (6061, screwed u) | fingers x part | 4.9 | 4.9 | 2 (2644-2644; 2804-2804) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/1 () x o24 (Module M50 handle (6061, screwed u) | fingers x part | 4.9 | 4.9 | 2 (2644-2644; 2804-2804) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/0 () x o30 (Cartridge heaters M50 (3 x 50 W, 2) | fingers x part | 4.5 | 4.5 | 1 (421-421) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/1 () x o30 (Cartridge heaters M50 (3 x 50 W, 2) | fingers x part | 4.3 | 4.3 | 1 (422-422) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/gr/left_finger_tip/0 () x o503 () | fingers x part | 3.9 | 3.9 | 40 (1885-1924) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| B/gr/right_finger_tip/0 () x o503 () | fingers x part | 3.9 | 3.9 | 40 (1885-1924) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/0 () x o28 (Plate rim wiper M50 (carbon-filled) | fingers x part | 2.6 | 2.6 | 1 (2748-2748) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/left_finger_tip/0 () x o27 (Build plate M50 (Ø50.5 x 10, 6061-) | fingers x part | 2.5 | 2.5 | 3 (2748-2750) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/0 () x o27 (Build plate M50 (Ø50.5 x 10, 6061-) | fingers x part | 2.4 | 2.4 | 3 (2748-2750) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |
| A/gr/right_finger_tip/0 () x o28 (Plate rim wiper M50 (carbon-filled) | fingers x part | 2.4 | 2.4 | 1 (2748-2748) | fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm) |

