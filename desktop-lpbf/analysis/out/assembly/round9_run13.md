# Round 9, runs 13 and 14 (2026-11-27): the whole assembly in one process, and round 8's audit findings fixed in the planner

Sterling, 2026-11-27, on what round 8 left: "deal with the stuff above". Round 8's frame audit
([`scene_audit_40-assembly-module.json`](../videoqa/scene_audit_40-assembly-module.json),
[`scene_audit_41-assembly-chamber.json`](../videoqa/scene_audit_41-assembly-chamber.json)) and run 12 left a list; this is what
the planner did about each, and run 13, planned and recorded with the fixes. Nothing here has been built or tried on hardware.

## What run 13 is

`run_assembly.py` with `ASM_RECORD=/tmp/robotbuild/traj/run13`, `ASM_TAG=_run13`, `ASM_SUMMARY=.../assembly_run13.json`: chapter
40's M steps and chapter 41's C and F steps **planned and recorded in one sequential process**, 08:36-09:21 UTC (2,718 s of
planner time on the shared runner, under a 3 GB cap). Run 12 had been four processes joined at F29, F39 and F51 (`ASM_FF_UNTIL`,
`ASM_CONTINUE`), with both MiRs restarting at the trunnion's dock at each join. Run 13 has no joins: every arm and MiR starts
each step where the recording left it. Code: r9-plan at 8f635f2 (with r9-people's model change, 93adcd2, merged first, so the
long table the planner picks from is the one the renderer draws: kit layout fa560d5f11acc467).

## Run 14: F54 by one arm under the hoist (10:05-10:15 UTC)

After run 13, F54 (the 13.3 kg optics bridge onto the four posts) was changed and tested alone, and run 14 re-planned **F54 to
the end only**, continuing run 13's recording (`ASM_FF_UNTIL=F54`, `ASM_CONTINUE`: run 13's chunks to the end of F53 copied
unchanged, the planner's arms and MiRs put back exactly where that recording left them, so the first motion of F54 starts where
the last one ended; checked: no jump at the join). The hoist takes the bridge's weight (a person brings it to the start of its
path, 80 mm over the posts); arm A comes to its grasp empty with the gripper open, the bridge an obstacle it may only touch,
closes on it and guides it down onto the posts' dowels (the last 12 mm pushed home with the closed fingers). Runs 9-13 had found
no pair of poses for the two-arm carry. The hook hangs 300 mm over the bridge throughout, checked clear. F55-F57 re-planned as
before. Run 14 was planned with `KIT_HASH=fa560d5f11acc467`, run 13's table layout, so the table is the one already drawn.

The files named for run 14 hold the whole assembly: run 13's rows and times to the end of F53, run 14's from F54 on
([`results_run14.json`](results_run14.json), [`run14_times.json`](run14_times.json), [`round9_run14.json`](round9_run14.json));
[`two_hands.json`](two_hands.json), [`mir_drives.json`](mir_drives.json), `robot-build/hud.json` and `times.csv` are on run 14.
F57 by its tubes' axes was tried alone too (each tube slid into the part placed before it, the next cube onto its free end):
five of its eight placements failed (the wrist camera on the bridge, arm A's reach to the back tubes, the cubes onto the tube
ends), so run 14 keeps run 13's F57, failing.

| | Run 12 | Run 13 | Run 14 (run 13 + F54 on re-planned) |
|---|---|---|---|
| checked steps passed | 99 of 108 | 104 of 110 | **105 of 110** (F54 passes) |
| still failing | C00d, F15, F18, F26, F27, F45d, F48b, F54, F57 | F15, F18, F26, F27, F54, F57 | F15, F18, F26, F27, F57 |
| screws driven | 124 of 129 | 125 of 129 | 125 of 129 |
| table picks planned | 57 of 74 | 62 of 76 | 62 of 77 (F54's bridge is brought by a person on the hoist) |
| MiR moves clear | 163 of 167 | 175 of 175 | 175 of 175 (7.2 m reversing in 31 docking legs of at most 0.5 m) |
| steps where both arms work | 19 | 19 | 18 (F54 is one arm now) |
| robot / person time | 3.30 h / 6.35 h | 3.27 h / 6.37 h | 3.28 h / 6.35 h |

## Against run 12

| | Run 12 (round 8, four processes) | Run 13 (round 9, one process) |
|---|---|---|
| checked steps passed | 99 of 108 | **104 of 110** (C00d, F45d and F48b now pass; F45e and F45f are new) |
| still failing | C00d, F15, F18, F26, F27, F45d, F48b, F54, F57 | F15, F18, F26, F27, F54, F57 |
| screws driven | 124 of 129 | **125 of 129** (C00d 18 of 18: #7 and #16 by arm B) |
| picks at the long table on a planned path | 57 of 74 | **62 of 76** (F36, F45, F45b now plan; F45e, F45f new and planned) |
| MiR moves clear (FCL, every pose) | 163 of 167 | **175 of 175** |
| MiR reversing | 6.9 m in 29 docking legs of at most 0.5 m | 8.1 m in 33 docking legs of at most 0.5 m (260 pivots) |
| holds on a seal (one arm holds, the other drives the first screws) | M19, C04, F30 | M19, C04, F30 (F33b, F37b, F43 not possible, with the reason) |
| steps where both arms work | 19 | 19 |
| robot time (recorded) / person time | 3.30 h / 6.35 h | 3.27 h / 6.37 h |

Files: [`results_run13.json`](results_run13.json), [`round9_run13.json`](round9_run13.json) (against run 12, from
`round7_summary.py`), per-step time [`run13_times.json`](run13_times.json), [`two_hands.json`](two_hands.json),
[`mir_drives.json`](mir_drives.json) (the last two now hold run 14, which differs from run 13 only from F54 on).

## Round 8's findings, and what changed

| Finding (round 8) | Cause found | Change | Checked |
|---|---|---|---|
| 41: the two angle-head nutrunners 31 mm into each other (frames 3635-3641); arm A's wrist through an outlet-plenum screw (1414-1417) | **the planner and the recording parted after a failed screw attempt**: the attempt is recorded as a failed screw with no motion, but the planner left the arm at the attempt's last pose, MiR dock and tool, and planned the other arm against that pose while the video drew the arm where it really was | `drive_screw` puts the arm back (dock, joints, tool) after a failed attempt; the arm that could not drive a screw parks (a planned, recorded move) before the other arm tries it | F06 and C00d-C05 alone: no pair over 1.5 mm in `rec_check.py`; C00d now drives all 18 |
| arm A's D405 camera 50 mm into the floor plate on a move to park (found by `rec_check.py` this round) | `cell.Checker.collisions` dropped every body outside `links`, `grip` and `caps` from the checked group; cell2's arm keeps its wrist camera and tool changer in `fixed`, so **no planned motion checked the camera or the changer** since cell2 split them out | they are the arm's own bodies in the check (analysis/robot/cell.py) | C00d-C05 alone: 0 pairs |
| 41: arm A's fingertip 44 mm into the galvo (10073, 10109) | the pick-insert-push ("released N mm short and pushed home with the closed fingers") was checked with the fingers closed but recorded with the grasp's opening, so the drawn push had the fingers open and wider | the push is recorded as it was checked: let go, close the fingers, push (the part rides on the closed fingers) | by construction; the renderer cuts at the jump between the two moves |
| 40: the 2F-85's body 78 mm in the module's handle (2958-3024, 3169-3241) | the turn-overs gripped the tube from the front after the handle was on, and the planner does not check a gripper against the part it holds | M26 and M28 take the module by the handle's I-section grip block, which is there for the 2F-85 (module_params.MODULE_GRIP) | M18-M28 alone: 0 pairs |
| 40: a knuckle 42 mm in the tube (2118) | the turn-over's approach was planned with the module already held and the fingers closed | approached with the gripper open and the module on its nest as an obstacle, ending in a straight line in (70, 45 or 30 mm), or planned to the grasp where the arm would fold onto itself (M26) | M18-M28 alone: 0 pairs |
| 40: MiR A 34 mm into the long table's stretchers while it turned (342-347) | the planner's table model had the top and legs only; the drawn table had two 12 m rails at \|y\| 390, where a pivoting MiR's corners pass | the stretchers are a cross rail at each leg pair (an H-frame, `kit_table.stretcher_boxes`), drawn and in the planner's table model | 175 of 175 MiR moves clear |
| F45, F45b: MiR B's cabinet and presenter on the zero-point release-air line (4 moves not clear, as in run 10) | the line lies on the table coiled (that is what is drawn) but the planner checked its fitted shape, routed valve to Y to modules, which reached into lane B | a hose or line on the table is its coil's box in the planner's table model | F45-F45c's drives clear |
| 41: the trunnion's jaws 88 mm into their stands in every frame | the shafts ended flush on the stands' solid faces: a zero-clearance contact the audit read as containment | each stand has a Ø53 x 60 bearing bore and the Ø50 shaft runs 50 mm into it, 1.5 mm clear (tooling.py) | FCL distance 1.48 mm |
| 41: the hoist hook 50 mm through the build module (3297-3376) | drawn 60 mm over the midpoint of the arms' TCPs, which for the chamber carried by two legs (F05b) is inside the chamber | the planner computes the hook 300 mm over the carried part's top (a lifting bar on two slings), checks it and its chain against the cell, the parts and both arms, and records it in the carry (`move2`'s `hook`) | F01 and F05b: clear |

## The failing steps (item 10)

| Step | Run 12 | Change in run 13 | Run 13 |
|---|---|---|---|
| C00d | 17 of 18 floor-plate screws (no approach for #7) | the arm that can't reach a screw parks before the other arm tries it; C01c (new) drives any screw left, from above, with the chamber upside down in the trunnion | **PASS**, 18 of 18 (#7 and #16 by arm B); C01c has nothing left |
| F45d | the NFC reader's antenna met the metering base on its drop (and, behind it, the side port's stub met the rails) | split: F45d (load cell, rails, docked sensor from above); F45e, the antenna into its pocket in the metering base's -x face from that side; F45f, the side port's KF-16 stub from that side | **PASS**, F45e and F45f pass |
| F48b | the ring pad met the camera boss at the seat | the pad's lip 24.0 mm (was 24.6): 0.5 mm a side in the tilted Ø25.6 counterbore was used up by the tessellations and a grasp centre taken from the tilted part, and no world-axis step frees a tool touching a tilted bore, so the depth check read the touch as deep | **PASS** |
| F15 | 6 of 7 (the screwdriver meets the KF-25 port on #7) | not changed: the angle-head nutrunner and the other arm were already tried for #7 | 6 of 7 |
| F18 | 3 of 4 held rail screws | not changed (time-boxed) | 3 of 4 |
| F26, F27 | the fingertip meets the chamber body; arm B's driver meets the funnel block | not changed: putting the cartridge in by its fin (the tending robot's way) needs the recoater run to the middle first, and the recorder draws every part at the model's home state, so a recoater moved by a step would be drawn in the wrong place | fail |
| F54 | no pair of arm poses at the start of the carry | run 13: not changed. Run 14: the hoist takes the weight and arm A alone guides the bridge onto the dowels, coming to it empty with the gripper open | run 13 fail; **run 14 PASS** |
| F57 | beam tube #1 meets the dichroic | not changed: the tubes must slide along their own axes | fail |

## Two hands ([`two_hands.json`](two_hands.json))

| Step | Run 13 |
|---|---|
| M19, C04, F30 | **hold used**: the placing arm keeps the part on its seal while the other arm drives 2 screws (F30: 1 of 20 screws lies under the vacuum cup and is left for F31) |
| F33b, F37b | **not possible, and why**: the VGC10 that places the Ø100 window flange and retaining ring covers both bolt circles (r 40, r 32) with its 100 x 100 mm body, so no arm reaches a screw while it holds. Without a hold the six screws are run down snug in a star pattern before any is torqued: the seal's 20 % squeeze is 0.36 mm, so the first screw tilts the part about 0.3 deg at most |
| F43 | **not possible**: with arm A holding, arm B's upper arm meets Fixture B on every first screw; with the roles swapped (tried this round), arm A's upper arm met Fixture B the same way. F44 drives all four with no hold |
| F51-F52 (door) | **not needed**: F51b (new) closes the door's two draw latches over their strikes before the hinge pins; they hold the door on its cord, knuckles in line, while the pin pusher works (a note: the latches are envelopes in the model, so the push is not planned) |
| F18, F03 | hold used (since round 7) |

## MiRs ([`mir_drives.json`](mir_drives.json))

175 base moves, all pivot-drive-pivot (260 pivots, 910 s at 30 deg/s, an estimate), every pose clear against the bench, the
fixtures, the parts present, the other MiR and arm where the recording has them, and the long table's top, legs, stretchers,
nests, trays and items (a coiled hose or line as its coil). Reversing only in 33 docking legs of at most 0.5 m (8.1 m in all).

## The recording checked as it is drawn ([`rec_check.py`](../../assembly/rec_check.py))

The planner checks each motion against its own world; the renderer draws the recording. `rec_check.py` replays the recording's
events exactly as `asm_render.py` does (objects at their put poses, held parts on the TCP, each arm's MiR, tool and opening) and
checks arm against arm and each arm against the parts present, with the planner's 0.1 mm meshes (the drawn meshes are decimated
to 12,000 triangles, which closes counterbores). On the step tests before the freeze (F05b-F06, C00d-C05, the whole of chapter
40, M18-M28) it found no pair over 1.5 mm once the fixes above were in; on the first of them it is what found the unchecked
wrist camera (50 mm into the floor plate on C00d's move to park). It was not run on the whole of run 13 or 14: it was stopped to free
memory for the renders (W4's frame audit covers the rendered chapters).

## Still open

- F15, F18, F26, F27 and F57 fail as above (F54 too in run 13; it passes in run 14); each is shown failing in the video, and
  falls to a person (5 min a step, 1 min a screw in the estimates). Their next changes are in assembly.md's open points.
- Picks at the table not planned: 5 of 76 (M04, F02b, F18, F39, F45d's first part: a fingertip meets its riser, a tray rim, the
  recoater rail or the drawer's latch studs). Nine more parts are sub-assemblies taken from a nest, not the table; they appear
  in the gripper at park (a cut, as before).
- F51b's latch push and C01c are notes or empty here; the door drive is still in no step.
