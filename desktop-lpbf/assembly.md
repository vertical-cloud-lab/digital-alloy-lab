# Assembling the desktop LPBF with two UR12e arms: the sequence, collisions in motion, the seals and the forces

Written 2026-11-20 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260). It answers
two comments on the [build animation](build-sequence.md):
- a BYU machinist: "Some of those gaskets might be hard to get on ... the animation was not worried about space and collisions";
- sgbaird: "have a set of two UR12e-s do the fine-detail assembly ... knowing that creation and use of additional tooling is fine. Also address the point about collisions rather than just space. Be thorough".

The cell follows [byu-vcl PR 318](https://github.com/vertical-cloud-lab/byu-vcl/pull/318) (round 14, commit 11d4410), through [`analysis/robot/cell.py`](analysis/robot/cell.py).

> **Update 2026-11-22 (round 4): patch 1 is answered by an order change, not a clamped cap; the two-arm run was not repeated.**
> - **Why not the clamped sleeve:** as specified below, the rod would run 20 mm into the cap. The hermetic connector's M12 bore
>   crosses the cap at 9 to 21 mm above the striker, so the rod would block it. A Ø20 groove in the Ø22 cap leaves a 1 mm wall.
>   And set screws below the rod seal are a leak path.
> - **What works instead:** keep the rod end welded, made by the shop on the bare rod, away from every O-ring. Then change the
>   order:
>   1. the gland plate, with its two 2-114s already loaded, goes onto the rod's top end;
>   2. the rod goes into the head's socket;
>   3. the stack, the rod and the gland plate enter the bore from the bottom, the tube's open end. With the body upside down on
>      its nest, that is from above.
>
>   In service the same holds in reverse. The gland plate comes out with the stack; then, on the bench, the rod comes down out of
>   the head and through the gland plate. This is exactly the person's procedure in [operations.md](operations.md) A1 and M7,
>   re-run step by step on this model (results there).
> - **Not re-run here:** chapter 3 (M10-M27) needs that order, and steps M16 and C10 see the module's new handle. It now has a
>   grip block for the robot in front of the chamber ([robot-ops.md](robot-ops.md)). The rest of this note is run 2's.

Nothing here has been built or tried on hardware. The numbers come from the model, from the sources cited, or from estimates, which are labelled as such. The model is `cad/lpbf_low.py` with the M50 module. It includes:
- the chamber change of [chamber-construction.md](chamber-construction.md): a through-frame and a bolted floor plate with a second 3.53 mm cord;
- for run 2, two items from this note's patch list: the lid gland's R13 corners and the floor port's lead-in.

## Round 8 (2026-11-26): run 12, two hands, MiRs that drive like MiRs, fixed cameras

Run 12 passes the same steps as run 11 (99 of 108, 124 of 129 screws, 57 of 74 table picks). The placing arm now holds a part on its face seal while the other arm drives the first two screws (M19, C04, F30); F33b, F37b and F43 need the same hold, but arm B's upper arm meets Fixture B; the door before its hinge pins (F51-F52) was not tried. Every MiR move is pivot, drive forward, pivot (167 moves, 6.9 m of reversing in docking legs of at most 0.5 m; 4 moves at F45 and F45b not clear). Run 12 was planned in four processes joined at F29, F39 and F51 (`ASM_FF_UNTIL`, `ASM_CONTINUE`). Details: [`analysis/out/assembly/round8_run12.md`](analysis/out/assembly/round8_run12.md), [`two_hands.json`](analysis/out/assembly/two_hands.json), [`mir_drives.json`](analysis/out/assembly/mir_drives.json); the video: [`robot-build/video.md`](robot-build/video.md) round 8.

## Round 7 (2026-11-25): the build done by the two arms from the long parts table, recorded, and redesigned where it failed

Sterling, 2026-11-25: "we should see the assembly being carried out **by** two UR12e units each on a MiR250 using the full set
of parts spread across a really long table ... it's fine for the robot to grab and use custom tools as desired (you'll need to
design, render, and simulate usage of these, though)". Run 7 (round 6) checked each step at its station with the part already
in the gripper. Round 7 adds where the part comes from, records every committed motion, and redesigns the steps that failed.
Nothing here has been built or tried on hardware.

### Run 11 (2026-11-26, 00:20-01:13 UTC): the table-pick fix and four next changes (not in the video)

The video replays run 10. Run 11 adds the table-pick fix (fe7b30c: a pick is planned with only the objects in the item's slot,
without the extras fitted at the station) and the next change for four of run 10's failing steps. Results:
[`results_run11.json`](analysis/out/assembly/results_run11.json); against run 10:
[`round7_run11.json`](analysis/out/assembly/round7_run11.json); real time per step:
[`run11_times.json`](analysis/out/assembly/run11_times.json).

| | Run 10 | Run 11 |
|---|---|---|
| checked steps passed | 98 of 108 | **99 of 108** |
| screws driven | 124 of 129 | 124 of 129 |
| picks at the long table on a planned path | 55 of 74 | **57 of 74** |
| planner's compute time | 4,688 s | 3,180 s |

| Step | Change in run 11 | Result |
|---|---|---|
| M13, C00a (picks) | the pick planned with the table item alone | **both picks plan** |
| F45 | a 35 mm axial leg before the lift (was 12 mm) | **PASS**: the shaft clears the metering base, and arm B carries it |
| F15 | a 100 mm bit extension (was 60) | 6 of 7: the screwdriver's body still meets the plenum's KF-25 port on screw 7, so the length isn't the cause; the side-mounted driver's body is. Next: the angle-head nutrunner for that screw, or the screw moved along the flange |
| F18 | a 30 mm bit on the held rail screws (run 10: 60 mm) | 3 of 4: now arm A's forearm meets the base plate. Next: arm B drives that screw from above the open top while arm A holds |
| F26 | in 15 mm high (run 10: 9 mm) | the same: the right fingertip meets the chamber body 117 mm into the move, so it is the fingers' width, not the height. Next: fingers along z, or the blade cartridge put in by its fin as the tending robot does |

### Run 10 (2026-11-25, 21:19-22:37 UTC): run 9's next fixes, recorded again for the video

Run 9's recording lived in `/tmp` on a runner that is gone, so the video's assembly chapters are rendered from run 10. Run 10
has the fixes run 9 listed as next (commit 07c972d), the grasp-down kit layout that run 9 never ran with, and the same checks.
Results: [`results_run10.json`](analysis/out/assembly/results_run10.json); against run 9:
[`round7_run10.json`](analysis/out/assembly/round7_run10.json); real time per step:
[`run10_times.json`](analysis/out/assembly/run10_times.json).

| | Run 9 | Run 10 |
|---|---|---|
| checked steps passed (robot steps, no notes) | 93 of 108 | **98 of 108** |
| screws driven | 123 of 129 | **124 of 129** |
| picks at the long table on a planned path | 40 of 74 | **55 of 74** |
| screw-presenter trips planned | 117 of 123 | 119 of 124 |
| planner's compute time | 7,163 s | 4,688 s |

What each change did:

| Step | Run 9 | Change in run 10 | Run 10 |
|---|---|---|---|
| F52, F52b | the fingertips holding a hinge pin's end met the door's front face, 6 mm behind the hinge axis | **the pin pusher** (new tool, `tooling.pin_pusher`): a Ø4.5 x 60 mm push rod with a Ø4 x 3 mm magnet in its tip, on a 12 x 12 x 150 mm bar, holds the pin by its end face on its axis; the rod is thinner than the Ø5.2 knuckle bores. The pins become 17-4 PH, which is magnetic and harder than the 304 knuckles (316 on 304 galls) | **PASS**, 0.1 mm |
| F45b, F45c | arm A's upper arm met the base plate, or found no pose | arm B from the back | **PASS** |
| F06 | 7 of 8 leg screws: no approach for one in 500 planner iterations | 2,000 iterations for this step | **PASS**, 8 of 8 |
| C00d | 17 of 18 floor-plate screws | 2,000 iterations | 17 of 18: still no approach |
| F15 | 6 of 7 inlet-plenum screws: the driver met the plenum's KF-25 port | a 60 mm bit extension | 6 of 7: the same contact |
| F18 | 3 of 4 held rail screws: arm A's driver met the chamber body | a 60 mm bit extension on the held part's screws | 3 of 4: now arm A's wrist 1 meets the base plate |
| F26 | the blade holder's own path met the frame (the holder stood 5 mm outside the door opening at the recoater's park) | in 6 mm right of its seat, then slid left inside the chamber | **the part's path now passes**; the arm fails: the right fingertip meets the chamber body 117 mm into the move |
| F27 | arm A's upper arm met Fixture B on both blade screws | arm B from the back | 0 of 2: arm B's driver meets the overflow funnel block |
| F45 | the part's path met the metering base; arm A met the base plate | arm B from the back | still FAIL, now on the part itself: after the 12 mm unscrew the roller shaft is still inside the metering base, so going up it meets the base (the part's sweep and arm B's carry both stop there, 3 mm deep). It needs a longer axial leg before the lift |
| F45d | the dock rails went on before the load cell that carries them | the load cell first | the load cell and rails pass; the NFC reader's antenna now meets the metering base on its path |
| F48b | the ring pad's body met the camera boss 63 mm along the line of sight | a 100 mm stem on the pad (was 55) | the same contact at the same place, so it is not the VGC10 body; it is at the seat (the pad's lip in the counterbore, or the tool's axis against the tilted bore) and needs a look at the geometry |
| F57 | the dichroic cube met beam tube #1, placed before it | the cubes first, then the tubes | now tube #1 meets the dichroic: the tubes' ends sit in the cubes' ports, so neither order works from above. The tubes have to slide in along their own axes |
| F54 | no pair of arm poses at the start of the carry | (none) | the same |

**Picks at the table.** 55 of 74 picks now have a planned path (run 9: 40), mostly from the grasp-down layout. Of the
10 that fail, a diagnostic re-run of M13 and C00a found **the held part at the table is not the part on the table**:
- M13's held body carries the PEEK rod bullet, a tool fitted at the station, which sticks 32 mm out of the rod's end, so on
  the nest the held rod reaches z 839.9 against the table top's 860;
- C00a's held body carries the overflow funnel that a person fits on the bench in C00, which hangs 62 mm under the plate
  (z 798), while the table holds the bare plate.

The fix (fe7b30c, in `commit.place`): plan the pick with a body of only the objects in the item's slot, without the extras
fitted at the station. Tested alone (`--only=M04,M13,C00a` with recording, 2026-11-26): M13's and C00a's picks now plan;
M04's does not (a fingertip meets its riser on the lift, a separate cause). Physically C00a's plate comes off the bench with
the funnel already on, so its pick belongs at the bench, not the table; the table holds the bare plate in the model. The other failed picks: M04 (a
fingertip meets its riser on the lift), F02b, F18, F36 (a fingertip meets the O₂ sample line), F39 (the drawer-latch studs),
F45d (a fingertip meets its tray's rim), and F45 and F45b, whose MiR drive is swept into the zero-point release-air line
lying past the table's edge.

### What was added

- **The long parts table** ([`cad/robotbuild/kit_table.py`](cad/robotbuild/kit_table.py)): every item the sequence places (a
  part, a bought or bench-built sub-assembly, or one piece of a step that places pieces one at a time) and every other part of
  the model has a slot on the 12 m x 0.9 m table in line with the bench (`common.LONG_TABLE`): 228 slots in eight
  category zones (stock, sheet, motion, gas, optics, electronics, seals and fasteners, frames) from x 2630 to 13692 mm, in
  assembly order inside a zone. Each item stands in the orientation it goes on in (upside down for the steps done upside down),
  so the arm takes it with the grasp it inserts it with; arm A's items on the front half, arm B's on the back, two-arm parts
  across the middle; >= 50 mm between items for the fingers. Supports: the table top, a kitting nest (a 12 mm plate with a
  15 mm pocket rim) for items that would not stand, a 45 mm riser (half the item's footprint) under low parts the gripper takes
  from above (its fingertips reach below the part: run 8's first picks of the heater block and the cartridge heaters hit the
  table top), small-part trays, and one labelled bin per McMaster number for the screws. The heavy units (UPS 23 kg, laser
  40 kg, scroll pump 26 kg, rack frame 22 kg, power box 16 kg) and everything people fit in chapter 5 go on nine EUR pallets
  behind arm B's lane. Machined parts also have their stock blank at the same slot, for the table before machining.
  Committed layout: [`analysis/out/assembly/kit_slots.json`](analysis/out/assembly/kit_slots.json).
- **Fetches** ([`analysis/assembly/fetch.py`](analysis/assembly/fetch.py)): for each place step the actor's MiR drives along
  its lane from the bench to the item's slot (up to ~13 m), the arm is planned from park to 70 mm back from the grasp, comes in on
  a checked straight line with the fingers open round the item (the item, its nest and the neighbouring items in the world),
  closes, lifts it 90 mm straight up (checked) and is planned back to park holding it; the MiR drives back to the station dock,
  the parked arm and the held part swept along the drive against the cell, the table and everything on it (every robot body's
  swept box against every other body's box, the overlapping pairs checked with FCL every 20 mm). A step that places several
  pieces (the nine Macor rings, the four legs) fetches its tray once. The station check then runs as before, from park.
- **A screw presenter on each MiR**: a vibratory rail presenter that holds one screw head-up at a pick-up nest. The OnRobot
  Screwdriver picks its screw from such a presenter and checks that it picked one
  ([product page](https://onrobot.com/en/products/onrobot-screwdriver), read 2026-11-25; OnRobot leaves the feeder to the
  integrator). No vendor or model is chosen: the 250 x 130 x 150 mm envelope is an estimate. Each screw: the driver is planned from the last screw's retreat to the presenter's pick-up
  nest, down and up 40 mm (checked), and planned on to the next hole. Run 8 first had the presenter on the cabinet top beside
  the arm base; there it took the elbow's room and four of the first five floor screws (C00d) lost their approach plans. It now
  hangs on the cabinet's far face beside the tool stand, its top 20 mm under the deck. The presenter trips are reported apart
  from the station results (117 of the 123 screws driven in run 9 had their presenter trip planned).
- **Recording** ([`analysis/assembly/record.py`](analysis/assembly/record.py), `ASM_RECORD=<dir>`): every committed motion
  in order (joint vectors per frame for both arms, gripper closure, tool changes, each MiR's x along its lane, the objects each
  arm carries and every object's pose, the screws' run-down and torque, the trunnion's turn), one pickle per chapter under
  `/tmp/robotbuild/traj` (not committed). The planner still tries several docks, rolls and tools per step; only the chosen one
  is recorded. The video chapters 40 and 41 replay these.
- **Real time per step** (`/tmp/robotbuild/data/assembly.json` for the video's summary and the cost worker): the motion times
  come from the recorded paths at cobot speeds, the rest are labelled estimates: joints <= 60 deg/s and the TCP <= 250 mm/s
  plus 0.4 s to start and stop; insertions 50 mm/s and the last 10 mm at 10 mm/s; screws run down at 300 rpm (pitch x 5 per
  second) plus 1 s to torque; the gripper 0.8 s; a tool change 8 s (estimate); MiR drives 0.3 m/s^2 and 1 m/s (MiR250
  datasheet) plus 6 s to dock (estimate); persons' steps by estimate (minutes per step in `commit.PERSON_MIN`).
  Results.json's old `seconds` field was the checker's compute time, not real time; it is now `compute_s`.

### Pass/fail, before and after

| | Run 7 (round 6, `results.json`) | Run 9 (round 7, `results_run9.json`) |
|---|---|---|
| checked steps passed (robot steps, no notes) | 77 of 97 | 93 of 108 |
| screws driven | 111 of 129 | 123 of 129 |
| place steps whose part came from the long table on a planned pick and checked drives | not modelled | 40 of 65 (the others: the pick at the table was not planned, listed below; moved sub-assemblies and the hand tools need no fetch) |

Steps were added and split between the runs (F25, F45, F48 and F52 became two to four steps each; F57b is new), so the counts are of different lists; the table below compares step by step.

Still failing in run 9:

| Step | What | Why |
|---|---|---|
| C00d | Eighteen M4 x 16 floor-plate screws up through the U-notches into the frame's sk | in the: approach: no path in 500 iterations |
| F06 | Eight M6 x 25 base-plate-to-leg screws, from under the plate | 316 #1: approach: no clear way in to the hole's mouth (A/upper_arm hits Base plate, process module |
| F15 | Nine M4 x 16 inlet-plenum screws into the back wall | 316 #7: screwdriver: B/tool/screwdriver hits Inlet plenum port (KF-25); also no way with nutrunner |
| F18 | Recoater rail with its carriage, carriage block, ball nut and arm (bought and pr | released 24 mm short and pushed home with the closed fingers; held-part screws: d thro: screwdriver: A/tool/screwdriver hits Process chamber body (6061-T6 through-frame f |
| F26 | Blade holder and blade, in through the door opening and up under the recoater ar | sweep: Blade holder blocked by Process chamber body (6061-T6 through-frame from 5 after 52.0 mm; arm A: held:F26:Blade holder hits Process chamber body (6061-T6 through-f |
| F27 | Two M3 x 8 blade screws (100 mm bit extension: run 7's driver met the module and | 316 #1: screwdriver: A/upper_arm hits Fixture B (open stand); also no way with nutrunner_angle; 316 #2: screwdriver: A/upper_arm hits Fixture B (open stand); also no way  |
| F45 | Roller feedthrough (M8 x 1 nose over its 2-012) into the metering base along its | sweep: Roller shaft blocked by Metering base (6061, fluted roller over a 100 mm d after 13.0 mm; arm A: A/upper_arm hits Base plate, process module (MIC-6, 15 mm) at 0 mm |
| F45b | Roller drive coupling onto the feedthrough's shaft | arm A: A/upper_arm hits Base plate, process module (MIC-6, 15 mm) at 0 mm along the insertion |
| F45c | Dosing stepper, its shaft into the coupling | arm A: no IK at the start pose at 0 mm along the insertion |
| F45d | Dock rails, load cell, NFC reader, side port blank and docked sensor, from just  | sweep: Load cell blocked by Dovetail rails for the reservoirs (lips pull the p after 0.0 mm; arm A: held:F45d:Load cell hits Dovetail rails for the reservoirs (lips pull  |
| F48b | Camera window gasket (1 mm FKM flat ring), window and flat ring into the counter | arm A: A/tool/ringpad hits Camera viewport adapter + boss (6061; Ø30 bore on the line of sight, Ø20 aperture, Ø1 in. window; FKM seals) at 63 mm along the insertion |
| F52 | Left hinge pin slid in from the left along the hinge axis, pushed home on its en | arm A: A/gr/left_finger_tip hits Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal groove, latch ears); pushed home instead, but A/gr/left_finger_tip hits Cham |
| F52b | Right hinge pin slid in from the right along the hinge axis, pushed home on its  | arm A: A/gr/left_finger_tip hits Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal groove, latch ears); pushed home instead, but A/gr/left_finger_tip hits Cham |
| F54 | Optics bridge (13.3 kg, lens and ring under it) onto the four posts: the hoist l | no collision-free pair of arm poses at the start of the carry |
| F57 | Beam tubes, dichroic and fold-mirror cubes, shutter, photodiode chain and collim | released 12 mm short and pushed home with the closed fingers; arm A: held:F57:Coaxial-monitoring dichroic hits Enclosed beam tubes #1; pushed home instead, but held:F57:C |

Picks at the table that were not planned (the station steps themselves pass; in the video the part appears in the gripper, with a note):

M04 (lift: no IK at the start); M13 (lift: no IK at the start); C00a (lift: no IK at the start); F02b (lift: no IK at the start); F10a (in to the grasp: no IK at the start); F10b (in to the grasp: no IK at the start); F10d (in to the grasp: no IK at the start); F16 (in to the grasp: no IK at the start); F18 (in to the grasp: left_finger_tip hits Recoater guide rail (15 mm, 260 ); F21 (in to the grasp: no IK at the start); F22 (in to the grasp: no IK at the start); F23 (in to the grasp: no IK at the start); F25 (in to the grasp: no IK at the start); F25c (in to the grasp: no IK at the start); F26 (in to the grasp: no IK at the start); F39 (in to the grasp: left_finger_tip hits Drawer latches: 2 x quarter-turn); F41 (in to the grasp: no IK at the start); F45 (in to the grasp: no IK at the start); F45b (in to the grasp: no IK at the start); F45c (in to the grasp: no IK at the start); F48c (lift: no IK at the start); F50 (in to the grasp: no IK at the start); F52 (in to the grasp: no IK at the start); F52b (in to the grasp: no IK at the start); F56b (in to the grasp: no IK at the start).


### Every redesign, tool and re-sequence, and why

| Step | Run 7 (round 6) | Change in round 7 | Kind | Run 9 |
|---|---|---|---|---|
| F10a, F10b, F10d, F10e | FAIL: the stock fingers met the module handle and the frame in the door opening | **liner wand** (tooling.liner_wand, new): a 12 x 12 mm bar, 300 mm to two Ø15 bellows cups 50 mm apart on its face; it carries each back half through the door opening by its front face, the wrist outside the chamber; the last leg 250 mm instead of 560. Hanger tabs like the side liners' are not possible: the recoater carriage block passes 2.4 mm in front of the back liners over the whole width | tool | F10a PASS; F10b PASS; F10d PASS; F10e PASS |
| F14 | FAIL: arm A had no pose behind the back wall; the holding wrist met arm B's driver on screw 7 | the plenum's flange goes onto the two Ø3 dowels in the wall with a transition fit (H7/m6) and hangs there on its own (the dowels engage 4.5 mm before the 2-044 is squeezed), so arm B places it and drives the nine screws; no holding arm | design + re-sequence | F14 PASS |
| F16 | FAIL: arm B's driver met arm A's wrist on all four screws | hangs on its two Ø3 dowels like the plenum; no holding arm | design + re-sequence | F16 PASS |
| F23 | FAIL: as F16 | hangs on its two Ø3 dowels; no holding arm | design + re-sequence | F23 PASS |
| F18 | FAIL: 3 of 4 held-part screws; arm B's upper arm met the base plate | roles swapped: arm B holds the rail from above, arm A drives from inside the chamber (as F19) | re-sequence | F18 FAIL |
| F25, F25b, F25c | FAIL: the motor bracket, brought in 260 mm along -x, started inside the trunnion's stands | three steps: the standoff; the bracket (a pillar on the base plate) lowered from above; the servo along +x into the coupling | re-sequence | F25 PASS; F25b PASS; F25c PASS |
| F26 | FAIL: the blade holder met the frame below the door opening (its bottom is 5 mm under the sill) | in 9 mm high over the sill, then down, then 12 mm back onto the arm's dowels; out-leg 200 mm | re-sequence | F26 FAIL |
| F27 | FAIL: the driver met the module's spigot and the upper arm Fixture B | a 100 mm bit extension keeps the driver above the chamber | tool | F27 FAIL |
| F45, F45b, F45c, F45d | FAIL: the 300 mm diagonal explode path swept the threaded nose through the base; no IK 300 mm up | four steps along each part's own axis: the feedthrough 12 mm along its axis then up; the coupling and the stepper along y; the dock parts from 70 mm above | re-sequence | F45 FAIL; F45b FAIL; F45c FAIL; F45d FAIL |
| F48b, F48c | FAIL: the window stack moved straight up, off the tilted line of sight; the fingertips met the boss | along the camera's line of sight; the two 1 mm FKM rings and the window by the **ring pad** (tooling.ring_pad, new: an annular silicone lip OD 24.6 / ID 21.4, since a 2.1 mm ring is narrower than the Ø6 nozzle cup), the retaining ring and the camera by the gripper | tool + re-sequence | F48b FAIL; F48c PASS |
| F52, F52b | FAIL: both pins slid together, held at one; arm A's upper arm met its cabinet | each pin from its own outer side along the hinge axis, held at its end and pushed home on its end face | re-sequence | F52 FAIL; F52b FAIL |
| F03 | FAIL: 4 of 8 screws: arm A could not reach the back posts' screws under the plate while arm B held them | per post, the arm on the far side holds it and the near arm drives its two screws from below | re-sequence | F03 PASS |
| F54 | FAIL: no pair of arm poses 260 mm above the posts | lowered the last 80 mm only, and hoist-assisted (14.3 kg; Edison r7) | re-sequence + lifting aid | F54 FAIL |
| F56b | FAIL: no IK at the start, 340 mm up | from 60 mm above | re-sequence | F56b PASS |
| F57 | FAIL: the three beam tubes as one part 107 mm across; no IK 340 mm up | one piece at a time (the tubes split), from 60 mm above | re-sequence | F57 FAIL |
| F49 | person (threaded SAE-4 ports) | robot: the gripper starts each thread by wrist rotation; the final ~20 N m torque is open (over the nutrunners' 10 N m) | robot (torque open) | F49 PASS |

### Where a person is still needed, and why

| Step | What | Who in round 7 | Why |
|---|---|---|---|
| M02 | three M3 helical inserts in the heater block | machine shop | put in right after tapping, with the tang broken off, as every insert in the chamber body; a cobot would need an inserter and a tang-break station for three inserts |
| M09 | bore seal: aramid felt strip and split PTFE scraper into the head's groove | person | the felt is wrapped and the split scraper sprung over, not pushed; no tool here does that, and no published robot method for felt was found |
| M12 | two 2-114 rod O-rings through the Ø15.93 throat (ring loader) | robot, then a person checks | the loader is simulated and passes; the grooves are hidden, so a person looks in with a light for a twisted or unseated ring (Edison r7) |
| M25 | the rod end's seven weld-in feedthroughs and the rod, TIG-welded | machine shop | welds, before chapter 3, away from every O-ring |
| C00 | overflow funnel (2-042, block, four M4) onto the floor plate's underside, on the bench | person | all four screws are open from above with the plate face down on the bench, so a robot could do it on a nest; that nest is not modelled, so it was not checked |
| C09e | M5 push-in elbows and a temporary Ø4 release-air line | person | a tube to route; the elbows themselves could be run in by the nutrunner with a socket |
| C11 | release air off: the zero-point modules lock | machine (the cell's valve) | |
| C15b | overflow-jar sensor and bracket onto the front-right leg, on the bench | person | a leg on a nest is open on every side, so a robot could do it; the nest is not modelled, so it was not checked |
| F01, F05b, F54 | base plate 11.8 kg, chamber assembly 19.6 kg, optics bridge 14.3 kg | a person on a hoist, both arms guide | Edison r7: no standard or precedent for two arms on separate MiR250s sharing a load; a rated lifting device above ~10 kg |
| F02 | levelling mounts | person (chapter 5) | they thread in when the 84 kg module goes onto the tray |
| F06b | release-air line from the valve to both modules | person | tube routing |
| F08 | KF-40 toggle clamp round the jar's flange | person | its hinged ring has to be held open round both flanges before one push on the lever; an air-released clamp would let the robot do it, but no product was checked this round |
| F12 | through-beam fibre heads (M6, with their 2-010) threaded into the side walls | person | the fibre has to be wound with the thread |
| F21 | ball screw through the nut (30 turns) | robot, then a person checks | simulated and passes; a person turns it by hand over its stroke for smoothness (ball circuits, preload: Edison r7) |
| F39 | the drawer's 2-033 into its half-dovetail | person on the bench (3 min, estimate) | stretched under the retaining lip; Edison r7 keeps it manual until a robot method is validated |
| F49 | pressure transducer and relief valve (SAE-4) | robot, final torque open | round 7: the gripper starts each thread by wrist rotation; the ~20 N m SAE-4 torque is over both nutrunners' 10 N m, so a bigger angle-head driver or a person's torque wrench for the last turn |
| F51 | the door's 1.78 mm cord into its half-dovetail | person on the bench (5 min, estimate) | as F39 |
| F53 | f-theta lens onto its ring over the shims (M85 x 1) | person | Ø90 is over the 2F-85's 85 mm stroke; the thread can cross on an expensive optic (Edison r7 agrees) |
| F57b | beam alignment and scan-field calibration | person (new, 90 min estimate) | alignment and calibration need judgment and instruments (Edison r7) |
| F58 | process fiber to the collimator | person | armoured fiber, >= 100 mm bend radius |
| F59 | Class 1 laser guard: T-slot frame, panels, door rail, sliding door, guard lock, panel | person | T-slot nuts and 1.5 mm panels up to 730 mm wide; its hardware is not drawn |
| T01-T05 | the 84 kg module onto the tray; rack units (UPS 23 kg, laser 40 kg); gas module (pump 26 kg); hoses; umbilicals | person + hoist or lift | over a UR12e's 12.5 kg payload, or hoses and cables to route |
| T06 | leak check | machine | |

**The Edison review of round 7** (`edison/r7-robot-build-review/answer.md`, sections 2-3) would keep a person, at least until
validated, for: the f-theta lens on its M85 thread (agreed: F53 stays manual), the internal rod-gland O-rings (M12), the
half-dovetail O-rings (drawer ring, door cord), optics alignment and calibration, and the ball screw. Where the simulation shows
the robot can do it with a tool (M12's ring loader, F21's ball screw), the robot keeps the step and a person checks it after
(M12: a light into the throat for a twisted or unseated ring; F21: the screw turned by hand over its stroke). The two
half-dovetail rings are fitted on the bench by a person (F39, F51), and alignment and calibration are a new person step (F57b).
On **two arms on separate MiR250s sharing one load** the review finds no standard or precedent and advises a rated lifting device
above ~10 kg. So the three carries over 10 kg (F01 base plate 11.8 kg, F05b chamber assembly 19.6 kg, F54 optics bridge 14.3 kg)
are now hoist-assisted: a person runs a small chain hoist on a jib with a lifting bar, and the two arms only guide the part along
the path that was checked; C00c (4.3 kg) and C01 (8.3 kg) stay two-arm carries.

**Failure modes the cell has to catch** (same review, section 3; none of them is simulated here):
- cross-threading and galling of the 316 screws in 18-8 inserts: the drivers' torque-angle trace (a screw that reaches torque
  early, in too small an angle, stops the step for a person); a new screw, not a re-drive;
- a twisted or rolled O-ring: an image from the D405 on the wrist after each ring, against a reference;
- a part off its expected pose at the pick or before the insertion: the D405 re-registers on the part or its fiducial, as the
  tending robot does after each MiR docking (robot-ops.md);
- a dropped part: the 2F-85 reports an object-detected width after closing; a missing or wrong width stops the step.

### Times

Real-world time from run 10's recording (run 9's in brackets; motions at the speeds above; tool changes, docking, the torque
phase and every person's time are estimates):

| Chapter | Elapsed (h) | Arm A busy (h) | Arm B busy (h) | Person (h) |
|---|---|---|---|---|
| 3: the build module | 0.53 (0.53) | 0.47 (0.47) | 0.01 (0.01) | 0.06 (0.06) |
| 4-5: the chamber, the process module and the tray | 9.17 (9.06) | 2.01 (1.87) | 0.36 (0.30) | 6.31 (6.31) |

The arms work one at a time in this plan (the planner moves one arm while the other waits), so elapsed time is about the sum. Driving to the table and back is a large share: the parts sit by category, and the electronics and seals are 10-12 m from the bench. Two easy gains, not modelled: kit the next steps' parts onto a tray on the MiR in one trip, and let the idle arm fetch while the other works. Chapter 4-5's person time is mostly chapter 5 and the guard: the rack and gas module with a hoist (T01-T05, 2.75 h), the laser guard (F59, 1 h) and alignment and calibration (F57b, 1.5 h), all estimates. The per-step lists are [`run10_times.json`](analysis/out/assembly/run10_times.json) (run 10) and [`round7_times.json`](analysis/out/assembly/round7_times.json) (run 9) (also `/tmp/robotbuild/data/assembly.json`, which the video's summary and the cost worker read; the run's `compute_s` is the checker's own time, not the assembly's).


### The video chapters

Rendered with [`cad/robotbuild/asm_render.py`](cad/robotbuild/asm_render.py) from run 10's recording (frames in `/tmp/robotbuild/frames`, not committed; the video is [`robot-build/video.md`](robot-build/video.md)): 40-assembly-module: 1,967 frames (2 min 44 s at 12 fps) from chapter 3; 41-assembly-chamber: 4,672 frames (6 min 29 s) from chapters 4-5, capped at a frame budget per step, with each step redesigned in round 6 or 7 preceded by a 3 s card that says what failed before and what changed (`--fail_notes`, [`run10_fail_notes.json`](analysis/out/assembly/run10_fail_notes.json); a REDESIGN badge). Real time per frame is in each frame's `proc_s` (motions at real time up to the step's frame budget, then time-lapsed, as the frame's sub-caption says; in chapter 41 the planned moves, most drives and the tool changes of a step are cut and their time carried into the next frame shown). The camera picks, for each motion, the least-occluded of 24 views (12 azimuths x 30/45 deg) by casting rays from the camera to 17 points round the work point against both arms, both MiRs and the fixtures (and, for a pick, the parts on the table near it; vtkOBBTree), and holds it through the motion; seal insertions get a 0.38 m close-up; transit moves are shown from a fixed wide view of the cell. A screw that one arm can't reach and the other then drives is shown as handed over, not as a failure. Both chapters were drawn in slices in parallel (`ASM_RANGE`, [`merge_parts.py`](cad/robotbuild/merge_parts.py)). Stills: [ring loader](cad/img/robotbuild/still-40-assembly-module-36.png), [the hoist and both arms](cad/img/robotbuild/still-41-assembly-chamber-25.png), [the pin pusher](cad/img/robotbuild/still-41-assembly-chamber-85.png); from round 7's first renders: [pick at the table](analysis/out/assembly/r7_pick_table.png), [MiR drive](analysis/out/assembly/r7_mir_drive.png), [spigot mandrel](analysis/out/assembly/r7_spigot_mandrel.png), [gland-plate screw](analysis/out/assembly/r7_screw_gland.png).

### Open points

**Still failing in run 10, and the next change for each** (run 10's changes are in the table above; run 11 tried four of
these, noted on each):
- **F15** (6 of 7 screws: the driver meets the plenum's KF-25 port on one, with or without the 60 mm extension): drive that
  screw before the port's stub goes on (the stub is welded, so: a shorter stub, or the screw moved 5 mm along the flange). Run 11's 100 mm extension didn't help: the side-mounted driver's body meets the port, so try the
  angle-head nutrunner on that screw.
- **F18** (3 of 4 held rail screws): with the 60 mm extension arm A's wrist 1 meets the base plate; without it the driver met
  the chamber body. Try a 30 mm extension between the two, or swap the roles back for that one screw (arm A holds, arm B
  drives from above the open top). Run 11's 30 mm bit: arm A's forearm meets the base plate instead.
- **F26** (blade holder): the part's path passes since run 10; the right fingertip meets the chamber body. Take the holder
  by its top and bottom faces (fingers along z) or with a narrower fingertip pair, or fit the blade cartridge to the arm on a
  bench nest and put the whole cartridge in by its fin (robot-ops.md's blade-cartridge job passes that way on the finished
  machine). Run 11 entered 15 mm high: the same fingertip contact, so it is the fingers' width.
- **F27** (blade screws): arm B's driver meets the overflow funnel block. Drive them on the bench with the cartridge on a
  nest before F26 (the cartridge is quick-swap anyway, with dowels and ball plungers).
- **F45** (roller feedthrough): the part's own path. **Fixed in run 11** with a 35 mm axial leg before the lift.
- **F45d**: the NFC reader's antenna meets the metering base on its 70 mm drop: bring it in from the side, or fit it before
  F43.
- **F48b** (camera window stack): the ring pad meets the camera boss at the seat, not on the way; check the pad's axis
  against the tilted counterbore (the tool may come in vertical while the part follows the line of sight), and the lip's
  0.5 mm radial clearance.
- **F57** (beam line): the tubes' ends sit in the cubes' ports, so the tubes have to slide in along their own axes: each
  tube into the cube placed before it, then the next cube onto the tube's free end.
- **F54** optics bridge: still no pair of arm poses at the start of the carry 80 mm above the posts. With the hoist taking the
  14.3 kg, one arm (or a person) can guide it onto the posts' dowels; check one-arm guidance.
- **C00d** 17 of 18: one screw has no approach even at 2,000 planner iterations; drive it after C01, with the chamber in the
  trunnion.

**Other open points**
- **Picks at the table that were not planned:** run 9 had 25, mostly parts gripped sideways at their seat whose kitted pose put
  the arm's flange behind its own base. The grasp-down layout (`kit_table.py`: the arm turns the part on its way to the
  station) brought run 10 to 10, and those are the held-body mismatches and contacts listed under run 10 above.
- **Moves back to park that the planner did not find** (`go_park`, e.g. after M04, M19, M26, M28): the run counts them as failed
  returns and starts the next step from park; the video draws them as straight joint moves labelled NOT PLANNED. Chapter 41 also
  has 19 places where a recorded motion does not start where the last one ended (a re-plan inside a step): the video cuts there.
- **F49**: the transducer's and relief valve's ~20 N m SAE-4 torque is over both nutrunners' 10 N m: a bigger angle-head driver
  or a person's torque wrench for the last turn.
- **C00 and C15b** (bench sub-assemblies) are robot-feasible on nests that are not modelled; they stay with a person here.
- **The door drive** (pneumatic rotary actuator on the hinge axis, `automation.py`) is in no step of the sequence; it goes on after
  the left hinge pin.
- **Two-arm carries under 10 kg** (C00c 4.3 kg, C01 8.3 kg) stay two-arm, as the Edison review allows; the hoist for the heavier
  ones is drawn as a hook and chain only, not checked for collisions.
- The screw presenter's size and place, the risers and nests, the hoist and the speeds behind the times are estimates.

## Round 6 (2026-11-25): the round-5 rod end, its screws, M16, and a re-run on the round-5 model

Sterling asked on 2026-11-25 for everything round 5 left undone ([followup-checks.md](followup-checks.md) §0). For this note
that was four things:
- the stale part names;
- the gland-plate screws that round 5's rod end hid;
- M16;
- a re-run of the two-arm build on the round-5 model. Round 5 ran chapter 3 on the round-4 model and never re-ran chapters 4-5.

### What changed in the model

- **The gland plate's six M4 moved onto the arc behind the rod end** ([`cad/joints.py`](cad/joints.py), `gland_screw_angles()`).
  - **Why:** the even 30° + 60° k pattern put three of them over the rod end's feedthrough block on S25 and M50. A torque
    screwdriver could not reach them, and they could not be withdrawn: operations.md A1.20 and M7.1 failed, 3 of 6 on M50.
  - **Rule:** keep the even pattern where every screw clears the block and its sleeves by ≥ 4.5 mm in plan (the Ø7 head
    plus 1 mm). Otherwise spread the six evenly over the arc behind the block's back face (y +6). Keep them 9 mm clear (the
    torque screwdriver's Ø16 chuck plus 1 mm) if they then stay ≥ 11 mm apart; otherwise 4.5 mm.
  - **Result:**

    | Module | Screw angles | Pitch | Plan clearance to the rod end |
    |---|---|---|---|
    | S25 | 28.2°-151.8°, every 24.7° | 9.5 mm | 4.5 mm |
    | M50 | 25.5°-154.5°, every 25.8° | 15.6 mm | 9.0 mm |
    | L75 | 18.4°-161.6°, every 28.6° | 23.5 mm | 10.1 mm |

    L75's even pattern cleared round 5's block by 4.6 mm, but not the wider block below.
  - **The seal holds with no screw in front.** The joint is metal to metal; the groove sets the 1.78 mm ring's squeeze at
    0.48 mm. The figures:
    - six M4 at 2.2 N m give ~11-16 kN of preload (nut factor 0.2-0.3);
    - the ring pushes back with ≤ 0.3 kN (an estimate: 0.7-1.75 N/mm over 177 mm of ring at ~27 % squeeze);
    - vacuum in the chamber adds ~0.3 kN, which closes the joint;
    - the 14 mm 316L plate's front overhang bends ~1-2 µm under its share of the ring (a cantilever estimate).
- **The rod end's type K sleeves moved apart, and the block is 81 mm wide (was 72)** ([`cad/modules_low.py`](cad/modules_low.py), `ROD_FT`).
  - **Why:** a sleeve stood under each of the handle's two M4 (x ±19, y −33.4 on M50). A person could reach them only with a
    ball-end key (A1.22); the robot's driver could not reach them at all (M22, 0 of 2 in this round's first pass).
  - **Change:** the sleeves moved from x ±12.5, ±21.5 and ±30.5 to ±11.85, ±26.16 and ±34.83.
    - The handle screws now sit in an 8.0 mm gap, 4.0 mm from the sleeve on each side.
    - Every sleeve keeps 2.4 mm to its neighbour and 2.5 mm to the block's edge.
    - Depth, height and the power sleeve are unchanged, and the block stays inside the base plate's slot (x ±56).
    - [electrical.md](electrical.md) §13.3 still gives the round-5 layout (72 × 16 mm). Ask Solid Sealing about weld access on
      this one.
  - **Still open:** S25's handle screws sit over the block itself, at x ±13, y −20.7, behind its face at y −22. Inside S25's
    Ø55.4 gland plate they cannot move clear of it. Two ways out:
    - fit the handle before the rod goes through the gland plate (operations.md A1: A1.21-A1.22 straight after A1.11). S25's
      rod set screws point sideways (0°, 180°), so the handle's riser doesn't block them;
    - or move the handle's screws, which is a change to the handle.

### Hand operations and interference on the changed model

`run_ops.py <module> --only=A1,M7 --tag=-r6-rodend`; operations.md is not updated here.

| Check | Round 5 | Round 6 |
|---|---|---|
| M50 A1.20 and M7.1, gland-plate screws | FAIL, 3 of 6 | PASS, 6 of 6 with the torque screwdriver |
| M50 A1.22, handle screws | PASS, ball-end key only | PASS, 2 of 2 with the torque screwdriver |
| S25 A1.20 and M7.1 | not run (3 of 6 sat over the block) | PASS, 6 of 6 with the torque screwdriver |
| S25 A1.22 | not run | FAIL: both screws over the block (above) |
| L75 A1.20, M7.1 and A1.22 | not run | PASS: 6 of 6, 6 of 6 and 2 of 2, all with the torque screwdriver |
| A1 and M7, all steps | M50 only | M50 19 pass / 0 fail; S25 17 / 1 (A1.22); L75 19 / 0 |

Sources: [M50](analysis/out/ops/results-M50-r6-rodend.md), [S25](analysis/out/ops/results-S25-r6-rodend.md),
[L75](analysis/out/ops/results-L75-r6-rodend.md). Operations.py's A1.14 and M7.2 still name the removed hermetic connector
(not this note's file).

**Interference** (`interference.py`, exact booleans, the same 6 static states and 8 motion sweeps as round 5):

| Module | Result | Rod end's tightest gaps |
|---|---|---|
| M50 | 0 | Z lift arm 1.0 mm (as designed: the block's underside is 1 mm over the arm); the guard frame 4.0 mm on the swap path; the base plate 4.5 mm at the bottom of the stroke; the gland plate 3.0 mm at the +8 mm overtravel |
| S25 | 0 | the same, and its handle screws 2.0 mm above the block at the overtravel |
| L75 | not finished | stopped when the merged model arrived (below); its rod end and gland plate changed as M50's did |

These ran on this round's model before the merge with the other round-6 changes; the merged model is checked below.

### The robot sequence ([`sequence.py`](analysis/assembly/sequence.py)) and the animation's captions

- **Stale names.**
  - M04 now places the three type K thermocouples; there is no cutoff. M19 no longer lists the cutoff.
  - M25 was the hermetic connector. It is now a machine-shop step: the seven weld-ins are TIG-welded into the block's face, and
    the rod into its top, before chapter 3.
  - The rod end arrives with the rod at M13. The key "Rod end" matches both the block and its feedthroughs.
  - [`render_build.py`](cad/render_build.py)'s chapter 3 now flies in the feedthrough block, and its captions say so. Nothing
    else in it changed.
- **M13, M14 and M19.** Arm A takes the rod end's block by its two end faces: 81 mm across, fingers along x. Run 3 gripped
  the Ø22 end cap with the fingers along y, where one finger now sits inside the block.
- **M16** (next section).
- **M21.** The handle is now lowered 15 mm in front of its seat and slid back the last 15 mm, held by its grip block's 40 mm
  web. Run 3 lowered it straight down the module's axis, which takes its two side arms through the type K sleeves. This
  round's first pass found that: blocked after 18 mm.
- **C10.** Arm B now holds the module by the handle's grip block. Runs 1-3 held it at (0, 0, −62) with the fingertips
  pointing along its axis, 40 mm apart: inside the bore, beyond the gland plate and the rod end. The check never tests
  the fingers against the part they hold, so C10 passed.

### M16: the welded body is gripped by its tube, not its flange

Run 3's automatic grasp took the top slice of the upright body: the flange, 119 mm across its dowel lugs, wider than the
2F-85's 85 mm stroke. The handle's grip block, which the tending robot uses, isn't on yet at M16; the handle goes on at M21.

So M16 now grips the tube between the flange and the collar, from the front, as the turn-overs M18, M26 and M28 already
did:
- **Fit:** the tube is Ø56.8 on M50, inside the 85 mm stroke. The nest's three posts (20°, 90°, 160°) leave the front free
  for the fingers.
- **Load:** the welded body is 1.73 kg ([`mass.json`](analysis/out/mass.json)), with its centre of mass on the axis, 31 mm
  above the grip. The 2F-85 grips with 20-235 N and carries 5 kg ([Robotiq product sheet, May 2025](https://blog.robotiq.com/hubfs/Product-sheets/Adaptive%20Grippers/Product-sheet-Adaptive-Grippers-EN.pdf),
  fetched 2026-11-25 01:02 UTC).
- **Friction:** with μ 0.3 (assumed, steel on the stock pads), 2μF holds the 17 N body from F = 28 N; at 100 N the margin
  is 3.5×.

A Robotiq 2F-140 (140 mm stroke, 10-125 N, 2.5 kg, same sheet) would take the flange. It would be a third tool on each
changer, with half the grip force, so it is not needed. On L75 the tube is Ø82.2, which leaves 1.4 mm a side in the
2F-85's stroke: workable with the AprilTag re-registration, but tight. This study builds M50 only.
[`assembly-tooling.csv`](assembly-tooling.csv) E3 records this; no tool changed.

### Run 4: chapter 3 on the round-5 model

`run_assembly.py --only=M` on the model above (round 5's merged model plus this round's two changes). Round 5's second
pass ran on the round-4 model, with its Ø24 end cap and hermetic connector.

| | Round 5, second pass | Round 6, first pass (72 mm block) | Round 6, second pass |
|---|---|---|---|
| Chapter 3, all 28 rows (notes count as passing) | 27 (M16 fails) | 26 (M21, M22) | 27 (M21) |
| Chapter 3, checked part, seal and turn-over steps | 20 of 21 | 19 of 20 | 19 of 20 |
| Chapter 3, screws | 16 of 16 | 14 of 16 | 16 of 16 |
| All checked steps, with run 2's chapters 4-5 | 64 of 80 | 63 of 79 | 63 of 79 |
| All screws, with run 2's chapters 4-5 | 118 of 135 | 116 of 135 | 118 of 135 |

M25 is now a machine-shop step, so chapter 3 has 20 checked steps, not 21.

- **First pass,** on the 72 mm block:
  - M13, M14 and M19 passed with the new grip on the block;
  - M16 passed on the tube;
  - M20 passed, 6 of 6, with the screwdriver 1.0 mm from the block;
  - M21 failed: lowered down the axis, the handle's side arms ran into the type K sleeves after 18 mm;
  - M22 failed, 0 of 2: a sleeve stood on each handle screw's axis. That is why the sleeves moved.
- **Second pass,** on the 81 mm block:
  - M22 passes, 2 of 2. The OnRobot's Ø6.35 bit passes 0.8 mm from the sleeves.
  - M21's handle now misses the sleeves (part sweep PASS, 2.43 mm). But arm A, holding the grip block from the front, hit
    its own wrist 2 with its upper arm 39 mm along the insertion. M21 is fixed in run 5, below.

### Run 5: chapters 3-5 on the merged round-6 model

The lead merged this round's workers into one model (PR branch 4e95878). What changed for this note:
- **Zero-point clamps** ([hot-swap.md](hot-swap.md) §3.2a): two SCHUNK NSE-HT mini 88-20 modules at (100, 40) and (−102, −26)
  under the floor, each on a 6061 plate and two posts. The module gains two arms with clamping pins.
- **No captive M6:** they and their retainers are gone. The clamps hold the module; old C11 drove the captive M6.
- **The overflow jar** sits at (94, −46) with a grip fin. The Z servo folded back, the legs moved, and the outlet hose was
  re-routed.

**What the sequence does now** ([`sequence.py`](analysis/assembly/sequence.py); 128 steps, was 119):

| Steps | What | Why |
|---|---|---|
| M29, M30 | Each zero-point arm, its pin screwed in on the bench, onto its flange ear. The module is upside down after the last turn-over; arm A holds the arm's plate 20 mm short of the pin | The pin's Ø20 head is on the clamp side of the plate, so it can't go in from above. Fitted earlier, the arms would meet the upright nest's posts. The automatic grasp near the hanger put a fingertip into the rod end |
| C12, C13 | The Z flange and its four M5 move ahead of the module | Run 2's fix for C12. On this model its fingers met a back-arc gland screw, and C13's driver met a zero-point arm |
| C09b-C09e | The four posts (threaded in by their studs), the two plates and the two NSE modules (vacuum gripper, Ø88), then the push-in elbows and a temporary release-air line (a person) | The modules must be open, at 6 bar, for the pins to enter |
| C10 | The module comes in along the machine's own swap path, reversed: 158 mm behind the port and 40 mm below it, then up. Arm B holds the handle's grip block | A straight 150 mm drop took the flange's tab through the left plate, which is cut back only to clear the swap path. B holds the grip block because runs 1-3's grasp was inside the bore |
| C11 | Now a machine step: vent the air, and the springs lock both pins at 2 × 0.5 kN | There are no screws to drive. The arm pushes the spigot ring home in force mode in C10: 132 N running, against the 147 N it can push there in run 2 |
| F02b | The release valve onto the base plate, before the chamber goes on | Once the chamber is on, the valve sits under the floor |
| F05b | Both arms hold the legs 40 mm lower (z −135) | At z −95 arm B's inner finger on the back-right leg ran into the right NSE module |
| F06b | The permanent air line (a person) | Replaces the temporary line |
| F07-F09b | The jar comes in from the front along its lane, held by its fin's 40 mm web, and up 8 mm onto its port. Then the toggle clamp (a person), and the sensor with its bracket and the bracket's two M4 | The jar's new place and fin |
| M21 | The handle's riser held by its two ends (48 mm, fingers along x) | Across the riser's 6 mm, one finger reached the power sleeve |

Run 5's first attempt (stopped part-way, 03:07 UTC) found the C10, C12, C13 and F05b failures above, and M21, M29 and M30 in
chapter 3. The other chapter-3 steps passed as in run 4.

**Run 5's result** (`run_assembly.py`, no `--only`, 2026-11-25 03:08-03:58 UTC, 51 min; [`results.json`](analysis/out/assembly/results.json),
the step table below):

| | Round 5 (chapter 3 second pass + run 2's chapters 4-5) | Round 6, run 5 (merged model) |
|---|---|---|
| Chapter 3: all rows | 27 of 28 | **30 of 30** |
| Chapter 3: checked steps / screws | 20 of 21 / 16 of 16 | **22 of 22 / 16 of 16** |
| Chapter 4a (C): checked steps / screws | 14 of 15 / 35 of 38 | **18 of 18 / 31 of 36** |
| Chapters 4b-5 (F, T): checked steps / screws | 30 of 44 / 67 of 81 | 28 of 45 / 64 of 83 |
| All checked steps | 64 of 80 | **68 of 85** |
| All screws on a planned, collision-free approach | 118 of 135 | 111 of 135 |
| Screws whose drive itself is clear | 121 of 135 | 117 of 135 |
| Steps for a person, the machine or the shop | 16 | 20 |

**Passing now that failed before:** M16, M21 and M22 (chapter 3; M25 is now the shop's step); C10, held by the grip block along the swap path (2.2 mm,
but the arm can push 132 N there, the same as the spigot ring's running friction, so it is marginal); C12 and C13 (the Z flange
first); the zero-point clamps, C09b-C09d (0.3 mm); the jar by its fin, F07 (15 mm); the release valve, F02b.

**New failures, all from parts that moved in rounds 5-6 (run 6, below, took them on):**
- **C05 (4 of 6) and C08 (2 of 4):** two outlet-plenum screws sit beside the plenum's KF-25 port, which round 5 moved to its left
  end, and two funnel screws beside the KF-40 stub at the slot's front end. Neither driver clears the port. Fix: drive those screws
  before the stub is welded on, or move them (a part change).
- **F05b:** the two-arm carry by the legs. Gripped at z −95, arm B's finger meets the right zero-point module; at z −135 arm A's
  adapter meets the base plate at the end of the carry. Both arms need a grip between them, about z −120, or two lifting lugs on
  the floor plate.
- **F09 and F09b:** the jar sensor's bracket now sits on the front-right leg. Arm A can't reach it from the front, and the bracket's
  two M4 are hemmed in by the base plate and the leg. Fit them before the legs go on (chapter 4a), or by hand.
- **F10:** the liners' straight path down is blocked by the frame. operations.md M3's ways in and out through the door should
  replace it (not done here).
- **F50:** the door's hinge knuckles. A fingertip meets the module's handle, whose grip block sits in front of the knuckles. Fit
  the knuckles before the module, or from the side.
- F54 (the bridge, two arms) and F57 (the beam parts; one is now 107 mm across where gripped) fail differently from run 2. They
  are not checked further here.

The rest fail as in run 2: F14, F16, F18, F23 (patch 9), F25, F26, F27, F45, F48b, F52, F03, F56b, and C00d and F06 by one
screw each.

### Run 6: the new chapter-4 failures, re-run alone

Sterling asked for every undone item, so run 5's new failures were taken on. Run 6 re-ran only chapter 4a and the changed
chapter-4b steps with their set-up steps (`run_assembly.py --only=C,F01,F02,F05,F07,F10,F11,F50`, 5 min a pass, two passes,
2026-11-25 04:07-04:17 UTC). Chapter 3 isn't needed for that: C10 places the whole module. Its rows replace run 5's in
[`results.json`](analysis/out/assembly/results.json), and the step table below says which run each row is from.

| Failure | What changed | Result |
|---|---|---|
| C05, two outlet-plenum screws beside the KF-25 port | a 60 mm bit extension | **PASS, 6 of 6** |
| C08, two funnel screws beside the KF-40 stub | the same extension | still 2 of 4: the stub's flange stands over them. **Geometry:** move those two screws out from under the stub, or put the stub on the funnel's side |
| F05b, the carry by the legs | arm A back at z −95 (its front-left leg is clear of the left module); arm B holds its leg's centre at z −124, 2 mm under the right module and clear of the base plate | **PASS** |
| F09, F09b, the jar sensor's bracket on the front-right leg | upside down in chapter 4a (first pass) arm A's forearm met the frame and its wrist the legs and the Z servo, so C15b now fits the sensor, bracket and two M4 to the leg on the bench before C14 | a bench step, not checked (the bench nest isn't modelled); 2 screws fewer in the count |
| F50, the hinge knuckles against the handle | the knuckles go on in chapter 4a before the module (C09f), one at a time, arm B; the strikes stay in F50 | **PASS**: C09f (14.6 mm) and F50 |
| F10, the liners | split into six steps along operations.md M3's ways through the door, back halves first | **still FAIL, all six:** the VGC10 (first pass) met the door opening's edges and the knuckles; the 2F-85 (second pass) met the handle's grip block under the opening, and arm A's wrist met the frame. The door path fits a hand. **Tooling:** a slim fork on a ~200 mm extension that takes the side liners' pull tabs and the back halves' top edges, so the wrist stays outside the opening |

**Seals re-run** ([`seals_forces.json`](analysis/out/assembly/seals_forces.json), 2026-11-25 04:07 UTC):
- the removed connector's 2-014 is gone;
- the camera adapter's ring is now a 2-030 (+2.4 % installed, +4.9 % while fitting), from the camera change;
- the camera window sits on a flat FKM gasket, so the 2-017 is gone.

The seal table below is updated to match.

**Counts after run 6** (runs 5 and 6 together, 133 steps):

| | Run 5 | Runs 5 + 6 |
|---|---|---|
| Chapter 3: checked steps / screws | 22 of 22 / 16 of 16 | 22 of 22 / 16 of 16 |
| Chapter 4a (C): checked steps / screws | 18 of 18 / 31 of 36 | **19 of 19 / 33 of 36** |
| Chapters 4b-5 (F, T): checked steps / screws | 28 of 45 / 64 of 83 | 30 of 49 / 64 of 81 |
| All checked steps | 68 of 85 | **71 of 90** |
| All screws on a planned, collision-free approach | 111 of 135 | **113 of 133** |
| Screws whose drive itself is clear | 117 of 135 | 119 of 133 |
| Steps for a person, the machine or the shop | 20 | 21 |

Round 5 (its chapter-3 pass and run 2's chapters 4-5) was 64 of 80 checked steps and 118 of 135 screws. F10's one step is now
six, so its failure counts six times.

### Run 7: the funnel on the bench and the plate fingers for the liners

The same partial run, twice (2026-11-25 04:27-04:36 UTC); its rows replace run 6's.
- **C08 is gone: the funnel is bolted to the floor plate on the bench**, as the hand op does (operations.md A2.13).
  - C06-C08 became a bench step, C00, before the floor plate goes onto Fixture P. C00a carries the plate with the funnel on it.
  - Fixture P's column now stops at x 60 (was 120), so the funnel and its KF-40 stub hang beside it.
  - The chamber now carries the stub 62 mm under the plate, which met a trunnion stand on the way in (C01, first pass). C01's
    lift is now 230 mm (was 150), and C01 passes.
  - No geometry change.
- **The side liners pass with the tending robot's plate fingers** ([`eoat.py`](analysis/robot/eoat.py) `PLATE_FINGERS`, as
  `ops.py` `job_liner` uses them). The fingers come straight in along +y and close their lips on the hanger tab's 2 mm grip plate
  at y −76, z 76.
  - F10c (left) and F10f (right) PASS, 0.1 mm at the tightest.
- **The four back halves still fail. They have no tab, so the stock 2F-85 holds them by the auto grasp:**
  - F10a and F10d, the lower halves: a finger meets the module handle's grip block, under the door opening.
  - F10b and F10e, the upper halves: a finger meets the door opening's edge, 381 mm along the path.
  - **Needed:** a hanger tab on each back half like the side liners' (a part change, `cad/automation.py` add_liner_tabs), for the
    same plate fingers.

**Counts after run 7** (runs 5-7 together, 131 steps):

| | Run 5 | Runs 5 + 6 | Runs 5-7 |
|---|---|---|---|
| Chapter 3: checked / screws | 22 of 22 / 16 of 16 | 22 of 22 / 16 of 16 | 22 of 22 / 16 of 16 |
| Chapter 4a: checked / screws | 18 of 18 / 31 of 36 | 19 of 19 / 33 of 36 | **17 of 17 / 31 of 32** |
| Chapters 4b-5: checked / screws | 28 of 45 / 64 of 83 | 30 of 49 / 64 of 81 | **32 of 49 / 64 of 81** |
| All checked steps | 68 of 85 | 71 of 90 | **71 of 88** |
| All screws, planned approach | 111 of 135 | 113 of 133 | **111 of 129** |
| Screws whose drive is clear | 117 of 135 | 119 of 133 | 117 of 129 |
| Steps for a person, the machine or the shop | 20 | 21 | 22 |

Fewer screws in the count: the funnel's four M4 and the jar-sensor bracket's two are now bench work.

Still failing in chapters 4-5:
- **needs a part change:** the four back liner halves (a tab each), and patch 9's F14, F16, F18 and F23;
- **as in run 2:** F25, F26, F27, F45, F48b, F52, F03 and F56b, plus F54 and F57 (run 5), and C00d and F06 by one screw each.

## Result

**Two UR12e arms can do most of the fine assembly, given a turn-over positioner, three drivers and a few custom tools.** What still fails comes down to:
- four design patches (rod end, dowels, locating pins, door);
- a handful of step and path fixes this run found but did not re-run;
- three seal-seating or threading steps that a straight-line check can't show.

The check covers 117 steps from chapters 3-5 and 135 screws in 23 joints, which is every screw the model draws for chapters 3-4 except the reservoir's own two lid screws. Each step is checked in motion: the part swept along its path, both arms checked frame by frame on a planned approach, and the 1.5 mm audit.
- **Run 1** (2026-11-20 23:13 UTC) was the first sequence.
- **Run 2** (2026-11-21 00:51 UTC) came after the patches the model took and the cell and sequence fixes below.
- Both runs used the model after its chamber change: a through-frame and a bolted floor plate with a second 3.53 mm cord. Run 2's model also has the lid gland at R13 and the floor port's 20° × 2.5 mm chamfer.

| | Run 1 | Run 2 |
|---|---|---|
| Build module (chapter 3): parts, seals, turn-overs | 17 pass, 3 fail | **19 pass, 1 fail** (the welded rod end) |
| Chamber and under-floor work | 12 pass, 1 fail | **14 pass, 1 fail** |
| Upright work on Fixture B | 18 pass, 22 fail | **30 pass, 14 fail** |
| All checked steps (screws and person-only steps not counted) | 47 pass, 26 fail | **63 pass, 16 fail** |
| Screws driven on a planned, collision-free approach | 91 of 135 | **118 of 135** |
| Screws whose drive itself is clear (tool on the screw, all the way in) | 118 of 135 | **121 of 135** |
| Steps for a person or the machine shop | 16 | 16 (unchanged: inserts, felt seal, lead and fibre routing, KF clamp, threaded ports, lens, guard, door latches, chapter 5) |

**What changed between the runs, and what it fixed:**
- **A trunnion positioner in place of both two-arm turn-overs.** Two stands, an axis 1000 mm up, and jaws on the chamber's side walls.
  - In run 1 both turn-overs failed: arm B's forearm hit its own gripper (C01), and its upper arm hit its own tool stand (F05).
  - Now the arms only carry the chamber the right way up: 7.4 kg into the jaws (C01), and 15.8 kg by two legs across 1.0 m onto the base plate (F05b), lifted 320 mm to clear the stands.
  - The trunnion's two 180° turns pass the mover check. The jaws open before the arms lift.
- **Fixture B is now two columns under the base plate,** and **the tool stands hang below the cabinet tops.** The base plate's carry (F01) passes.
- **Order changes:**
  - The Z flange goes on alone, its four M5 driven, then the actuator; C13 now passes 4/4 (0/4 before).
  - The optics posts go on after the side-wall parts and the draw latches. F22 (the Ferrotec feedthrough) and F50 (the right draw latch's way in) now pass.
  - The recoater rail goes on with its carriage, block, nut and arm, as bought. The ball screw comes in alone (F21 passes).
- **Tools:**
  - the vacuum gripper for the Ø100 window flange and retaining ring and the galvo riser (F33b, F37b and F56 now pass);
  - a small-part vacuum nozzle for the Macor rings, shields and disc springs (M05 and M07 now pass);
  - a 130 mm extension for the captive M6.
- **Approach planning for upward screws.** 1000 RRT iterations, a pre-approach slid out from under the plate, and a restart from park when a retreat leaves the arm touching. The 18 floor screws went from 3 to 17 planned.
- **A bookkeeping bug fixed.** While iterating, a screw could be left on the other arm's bit after a failed fallback attempt, which spoiled the next two-arm carry. Run 1 had no fallback, so it wasn't affected.

**What still fails (run 2), by cause.** Patch numbers refer to the list at the end.

- **Needs a design patch:**
  - M25, the rod end welded to the rod: patch 1.
  - F14, F16, F23: the inlet plenum, the vacuum-port adapter and the bearing cap can't be held by one arm while the other screws them. In F16 and F23, B's driver meets A's holding wrist; in F14, A can't reach behind the back wall. Patch 9, two locating pins per flange, removes the holding.
  - C02 passes the motion check, but the dowels' 1.6 kN press is 11 × what the arm can push there (149 N): patch 4.
- **Needs a step or path fix this run found but did not re-run:**
  - **C12:** the Z flange's fingers meet the module's gland plate. Fit the flange before the module.
  - **F27:** the blade's two M3 sit 11-17 mm above the floor, too low for any of the three drivers. Screw the blade into its holder on the bench.
  - **F54:** grasp the bridge between the posts, not over post 1.
  - **F25, F56b, F57:** use shorter approach paths (the motor bracket, the galvo, the beam parts). Their animation paths start out of reach or, in this layout, inside the trunnion's stand.
- **Needs a different tool shape:** F11, the LED bar 1 mm from the wall. The VGC10's 100 mm body hits the frame, so it needs a slim side-mounted nozzle.
- **Not settled by this check:**
  - **F26:** the blade holder can't pass the door's 8 mm sill. It has to go in through the frame's open bottom before the floor plate, which is not modelled here.
  - **F48b:** the camera window's 2-017 can't be laid straight into its seat in the boss as drawn; check the seat for an undercut.
  - **F45:** the roller feedthrough is threaded, so a straight sweep can't show it going in.
  - **C11:** the check counts the captive M6 against its own retainer, which holds it captive by design.
- **Planning budget:** one screw each in C00d, F06 and F03, out of 34 driven upward. Their drives are clear; their approaches weren't found in 1000 iterations.
- **Cell, still:** in F18 one rail screw's driving arm meets the base plate's edge (3 of 4), and in F52 the hinge pins, slid in from the right, put arm A's upper arm into its own cabinet.

**Collisions, not just space.** On the way in, the tightest gaps are:

| Step | Gap | Where |
|---|---|---|
| rod in the head (M10) | 0.02 mm | |
| stack in the bore (M22) | 0.03 mm | the rod passing the gland plate |
| heaters (M03) | 0.05 mm | Ø6.1 bores |
| spigot mandrel's sleeve (M20) | 0.05 mm | over the Ø95.8 spigot |
| module into the port (C10) | 0.05 mm | |
| dowel (C02) | 0.05 mm | |

- The arms' tightest clearance to anything they may not touch is 0.0-0.1 mm: fingers beside seated parts.
- The rollers run 0.9-1.1 mm from the gland walls.
- 16 parts are let go 6-39 mm short of their seat and pushed home with the closed fingers. Two Macor rings drop the last 6-9 mm onto their guide pins.

**Seals.**
- **Stretch.** Installed stretch is 1.4-2.7 % for every ring; Parker allows 5 %. The most stretch while fitting is 18.6 %.
- **Rod rings.** The two 2-114s, folded through the Ø15.93 throat at about 34 % bending strain, remain the riskiest seal step.
- **Lid gland.** Its corners are now R13 in the model, so its corner strain drops from 29 % to 12 %. A moulded 2-277 would fit it at +2.8 % (2.2-3.4 % over tolerance), and the floor gland at +1.7 %. The floor port now has its lead-in.

**Forces and tip-over.**
- **Push.** At the force steps' poses the arms can push 113-191 N downward (149 N at the dowels, 119 N at the spigot), using the corrected link-mass torques.
- **Too much for the arm:** the spigot's 328 N break-out (the captive M6 pull it home), the dowels' 1.6 kN, and the door latches' 725 N.
- **Tip-over.** Every load the arms carry keeps the MiR's restoring / overturning moment at 5.8 or more. A robot pressing a dowel would tip it (0.5).


## Renders

Rendered offscreen by [`render_assembly.py`](analysis/assembly/render_assembly.py) from run 2's own snapshots: the same arm poses, tools, held parts and placed parts the checks used. The cell overview is under [The cell](#the-cell).

| | |
|---|---|
| ![The trunnion has turned the chamber upside down for the under-floor work](analysis/out/assembly/render_C01b.png) | ![Chamber assembly (15.8 kg) carried upright by both arms, each holding a leg, from the trunnion to Fixture B](analysis/out/assembly/render_F05b_mid.png) |
| C01b: the trunnion has turned the chamber (frame + floor plate) upside down. The jaws clamp the side walls 10 mm above the turn axis. The under-floor work then goes on from above. | F05b, halfway through the 1.0 m carry: the 15.8 kg chamber assembly, back upright, held by both arms by two legs on its way from the trunnion to the base plate on Fixture B. |
| ![Chamber assembly carried by both arms from the trunnion to Fixture B (F05b), every few frames of the checked path](analysis/out/assembly/carry_F05b.gif) | ![Heater stack into the bore: the rod on its bullet passes the two rod O-rings](analysis/out/assembly/render_M22_1.png) |
| F05b: the two-arm carry from the trunnion to Fixture B, every few frames of the checked path. | M22: arm B lowers the heater stack into the module bore. The plate-to-bore gap is 0.03 mm. The rod on its PEEK bullet passes the two 2-114 rod rings, and B lets go 39 mm short and pushes it home. |
| ![Spigot O-ring: mandrel on the spigot, pusher stroke](analysis/out/assembly/render_M20.png) | ![Build module (upside down) into the floor port, chamber in the trunnion](analysis/out/assembly/render_C10_1.png) |
| M20: the spigot's 2-238 goes on over the acetal mandrel. Arm A strokes the pusher down, and the sleeve clears the spigot by 0.05 mm. | C10: the finished module goes down into the floor port of the upside-down chamber in the trunnion, with 0.05 mm clearance at the spigot. Its captive M6 then pull the seal home. |
| ![Lid cord rolled into the body's gland (roller on arm A)](analysis/out/assembly/render_F29_A_0.png) | ![C00d: floor-plate M4 driven up through a U-notch (angle-head nutrunner)](analysis/out/assembly/render_screw_C00d.png) |
| F29: arm A rolls the lid cord into the frame's gland, working over the chamber between the optics posts (1.0 mm from the gland walls). Arm B does the back half. | C00d: a floor-plate M4 driven up through its U-notch, with the plate on Fixture P. The angle head keeps the wrist 250 mm to the side. 17 of 18 are planned (3 in run 1). |
| ![F06: base-plate-to-leg M6 driven up from under the plate (angle-head nutrunner)](analysis/out/assembly/render_screw_F06.png) | ![F31: lid M5 (OnRobot Screwdriver, side-mounted)](analysis/out/assembly/render_screw_F31.png) |
| F06: a base-plate-to-leg M6 driven up from under the base plate on Fixture B (now two columns) by the angle-head nutrunner. 7 of 8 are planned; all 8 drives are clear. | F31: a lid M5 driven by the side-mounted OnRobot Screwdriver. All 20 pass, with 2.6 mm to spare. |
| ![F18: rail M4 driven from inside the chamber (angle-head nutrunner)](analysis/out/assembly/render_screw_F18h.png) |  |
| F18: a recoater-rail M4 driven from inside the chamber toward the back wall by the angle-head nutrunner (3 of 4). The OnRobot's body does not fit inside the 190 mm deep chamber. |  |

## How it was checked

Everything is in [`analysis/assembly/`](analysis/assembly/). One command re-runs it on whatever `cad/` holds (16 min for run 2, on a shared 4-core runner):

```bash
OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/assembly/run_assembly.py     # the build, step by step
/tmp/venv/bin/python desktop-lpbf/analysis/assembly/seals_forces.py                                    # seals, forces, tip-over
/tmp/venv/bin/python desktop-lpbf/analysis/assembly/report.py                                          # steps.md, sequence.json, push.json
xvfb-run -a -s "-screen 0 1600x1200x24" /tmp/venv/bin/python desktop-lpbf/analysis/assembly/render_assembly.py
```

- Scratch (frames, `parts.json`, tool meshes) goes to `/tmp/asm`; `ASM_DIR` moves it, so that two runs on different models
  don't share it. The UR arm meshes are cached under `/tmp/ur_arm_cache` (`UR_ARM_CACHE`); loading them needs `pycollada`.
- `--only=M` (or `--only=M,C`) re-runs chapter 3 (and 4a) alone into `results_M.json` (`results_M_C.json`). `report.py`
  then uses those rows for those chapters and the full run's `results.json` for the rest, and `steps.md` says which rows
  came from which run.

| File | What it does |
|---|---|
| [`cell2.py`](analysis/assembly/cell2.py) | The cell: two UR12e on MiR250s, the bench, the fixtures and the tool stands. It imports [`../robot/cell.py`](analysis/robot/cell.py) (byu-vcl PR 318's arm, 2F-85, D405, FCL bodies, IK branches, RRT-Connect, 1.5 mm audit) and adds an automatic tool changer, so the arm can carry the 2F-85, a screwdriver, a nutrunner, a vacuum gripper or a roller. The D405 stays on the arm side of the changer. Each arm's world includes the other arm, with its tool and whatever it holds. |
| [`tooling.py`](analysis/assembly/tooling.py) | Dimensioned CadQuery CAD of the custom tools and fixtures, exported as STEP to [`out/assembly/tooling/`](analysis/out/assembly/tooling/). The bought tools are drawn at their published sizes. |
| [`sequence.py`](analysis/assembly/sequence.py) | The build order: every part and fastener of chapters 3-5 and `joints.py`. For each step it gives the insertion path, the tool, which arm acts and which holds. |
| [`run_assembly.py`](analysis/assembly/run_assembly.py) | The checks below, step by step |
| [`seals_forces.py`](analysis/assembly/seals_forces.py) | Ring stretch, moulded rings in rectangular grooves, chamfers, dovetail insertion, friction, forces and tip-over |
| [`report.py`](analysis/assembly/report.py), [`render_assembly.py`](analysis/assembly/render_assembly.py) | The tables, the replay file for `render_build.py`, the renders |
| [`out/assembly/`](analysis/out/assembly/) | Outputs:<ul><li>[`results.json`](analysis/out/assembly/results.json): every check, and every screw;</li><li>[`steps.md`](analysis/out/assembly/steps.md): the table below;</li><li>[`sequence.json`](analysis/out/assembly/sequence.json): for `render_build.py` to replay. Per step: the parts' exact `Part.name`s, insertion waypoints relative to the final pose in model coordinates ending at [0, 0, 0] (4 × 4 poses for the turn-overs), the tool (and the joint key for screws), the arm, the clearance, pass/fail, and for rings the fitting method;</li><li>[`seals_forces.json`](analysis/out/assembly/seals_forces.json);</li><li>[`push.json`](analysis/out/assembly/push.json);</li><li>[`tooling/*.step`](analysis/out/assembly/tooling/): the custom tools.</li></ul> |

Each step gets three checks:

1. **Part sweep.** The part travels its insertion path against everything already in its sub-assembly. This reuses `analysis/ops/checks.path_check`: FCL on 0.1 mm meshes, sampled every 1 mm. A contact only counts as a block when manifold3d finds more than 0.5 mm³ shared and OpenCascade's exact boolean confirms it. The check reports the smallest gap along the way.
2. **Arms, frame by frame.** The actor's MiR docks at a station and may slide along the bench. Its TCP then follows the part's path:
   - IK every 3 mm, all on one branch (a joint jump over 20° counts as a fail);
   - FCL every frame, for the links, the tool, the D405, the changer and the held part, against the cell, every part present and the other arm;
   - the move to the start of the path planned with `cell.Checker.plan`: the straight joint line, otherwise RRT-Connect with 1.5° edge checks.

   The part and the tool may touch the part's own seat only up to 1.5 mm deep (byu-vcl PR 318's round-11 rule). A part whose fingertips would reach its seat is let go short of it and pushed home with the closed fingers ("released N mm short" in the table), and the push is checked too.
3. **Screws.** Each screw rides on the driver's bit from the mouth of its hole to its seat. The check tries 12 roll angles about the screw axis and every IK branch, checks the drive frame by frame, plans the move there, and checks that the screw's own axis line is clear (`checks.withdraw_check`). The driver is chosen per screw:
   - the OnRobot Screwdriver, which works downward or sideways only, up to 5 N m;
   - otherwise the inline nutrunner.

Flips and two-arm carries are checked the same way along the part's whole path (lift, turn, move, lower), with both arms' IK and collisions at every frame. The trunnion's turn is checked as a mover, as in byu-vcl PR 318: 37 frames of the turning chamber and jaws against the cell, everything placed and both parked arms.

What is not simulated: the elastomer's own shape while it is stretched or rolled (the tools are checked, not the rubber), cables and hoses, the pick side of each step (kitting trays), and the MiR's own driving.

## The cell

![Cell layout](analysis/out/assembly/render_cell.png)

- **Arms.** Two UR12e arms, each with a 2F-85 and a D405, on MiR250s with 480 mm cabinets, so each arm's base is 800 mm above the floor. These are byu-vcl PR 318's arms. Arm A docks on the front of the bench (y < 0) and arm B on the back. Each MiR slides along x to line up with a station, as PR 318's MiR drives along the VLM opening. Each arm base sits 240 mm off the bench edge.
- **Bench and stations (run 2).** The bench is 800 × 800 mm, top at 760 mm, and carries the module nests. The rest stands on the floor:
  - **Fixture P,** a 240 × 150 column that holds the floor plate 1000 mm up, so the arms reach under its edges.
  - **The trunnion,** a turn-over positioner: two stands, an axis along x 1000 mm up, and two jaws that clamp the chamber's side walls 10 mm above the axis. Something like a geared stepper with a brake would drive it. In run 2 it turns the chamber upside down for the under-floor work and back upright. Run 1 tried both turn-overs with the two arms alone, and both failed.
  - **Fixture B,** two 120 × 200 columns under the process base plate. They are clear of the legs' and posts' base screws and of the Z actuator, and nothing stands beside or above the plate. Run 1's end frames blocked the right-wall screws.
- **Tool changer.** Each arm has an ATI QC-21 automatic changer: 25 kg, Mxy 56.5 N m, 42.4 mm coupled, plus about a 16 mm UR plate. The QC-11 is lighter (0.245 kg, 36.1 mm), but it is rated only 20.3 N m in Mxy. The two-arm lifts below put up to about 15 N m on each wrist, which leaves the QC-11 too little margin. The D405 clamps to the changer's master side, so it stays on every tool.
- **Tool stand.** Each arm has one hung on its cabinet's far face, below the cabinet top, as PR 318 keeps finger sets on a stand on the MiR. Each stand holds that arm's set of tool plates. In run 1 the stand sat on the cabinet top behind the arm base, where arm B's upper arm hit it during the second turn-over.

| Tool | On | Used for | Published numbers (fetched 2026-11-20 UTC) |
|---|---|---|---|
| Robotiq 2F-85 | both arms | parts, flips, two-arm carries, hand tools (mandrel, pusher, loader) | 85 mm stroke, 20-235 N, 0.925 kg; pads 38 × 22 mm ([manual](https://blog.robotiq.com/hubfs/support-files/2F-85_2F-140_General_PDF_20210623.pdf), 22:24) |
| 2F-85 pin caps (custom) | either | small rings (internal two-point grip), Macor rings, disc springs | 2 mm wall over the pad, Ø2 × 6 mm pin |
| OnRobot Screwdriver | A | M3-M5 screws driven down or sideways | 0.15-5 N m, M1.6-M6, 2.5 kg, 308.5 × 86 × 114 mm, side-mounted. Downward or sideways only. Magnetic screws only ([datasheet v1.7](https://onrobot.com/storage/datasheets/screwdriver/datasheet_screwdriver_v1.7_en), 22:18) |
| Inline nutrunner (Kolver PLUTO 10 class) | either | M6 driven down (7.4 N m), and M4-M5 where the OnRobot's body doesn't fit | 1.5-10 N m, 0.5 kg (Brera 2022, via [Edison r3](edison/r3-robot-oring-assembly/answer.md)). The Ø40 × 250 mm envelope is an estimate. |
| Angle-head nutrunner (Atlas Copco / Kolver angle-head class) | either | every screw driven upward: the 18 floor-plate M4, the 8 post-base and 8 leg-base M6 | 0.5-10 N m class. The envelope is an estimate: Ø40 × 230 mm body, 90° head 44 × 40 × 46 mm. An inline driver pointing up puts the wrist under the arm base and into the pedestal; this one keeps the wrist 250 mm to the side. |
| OnRobot VGC10 | A | the floor plate, the lid, the wall liners; the Ø100 window flange and retaining ring, the 155 × 130 galvo riser and the galvo (run 2) | 0.814 kg; 100 × 100 × 101.5 mm; 6 kg on its standard cups, up to 15 kg on custom ones ([datasheet](https://onrobot.com/storage/datasheets/vgc10/datasheet_vgc10_v1.7_en.pdf), 22:24) |
| Small-part vacuum nozzle (custom, on the VGC10) | A | the 9 Macor rings, 2 shields, 3 disc springs, the LED bar (run 2) | Ø5 × 60 mm stem, Ø6 cup |
| Trunnion positioner (custom) | floor | both chamber turn-overs (run 2) | stands 90 × 260 mm, axis 1000 mm up, Ø50 shafts, 12 × 90 × 70 mm jaws |
| Roller (custom) | A | the lid and floor cords; the door and drawer cords on their nests | Ø30 PTFE wheel on a sprung fork with 15 mm travel and 8-25 N. A 3.2 mm wheel for the 3.53 mm cord, a 1.4 mm wheel under a half-dovetail lip. |
| Spigot mandrel and pusher (custom) | B, A | the 2-238 on the spigot | acetal. The cone runs Ø96.7 to Ø82 over 40 mm; a 0.45 mm sleeve covers the spigot's top edge. |
| Rod bullet (custom) | on the rod | the rod through the two 2-114 rings | PEEK, 15° nose, Ø8 bore for the leads |
| Ring loader (custom) | A | the 2-114 rings into the gland plate's internal grooves | slotted tube, Ø15.6 OD, through the Ø15.93 throat |

The vendor rows of [`assembly-tooling.csv`](assembly-tooling.csv) have every source and its fetch time; the custom rows give a dimensioned spec and an estimated price. No vendor publishes a price for the arms, the changer, the screwdriver or the VGC10.

### Where the arms are, and how sure

- **Docking.** The MiR250 docks to a VL marker within ±3 mm and ±0.5° (MiR's [spec page](https://mobile-industrial-robots.com/it/prodotti/robot/mir250/specifiche), 22:37). After docking, the wrist D405 reads an AprilTag cube on each fixture, as PR 318's arms do.
  - AprilTag 36h11 measured 0.39 mm and 0.77° at 10-50 cm ([DeepTag, Table 2](https://arxiv.org/abs/2105.13731), 22:39). That figure is the error of a measured 10 cm displacement, not an absolute pose.
  - So after re-registration a part lands within roughly 0.4-1 mm (an estimate). Over a 300 mm part, the 0.77° grows to about 4 mm at its far end, so long parts (lid, frame, bridge) need two tags or a touch-off in force mode.
- **Repeatability.** The UR12e repeats to ±0.05 mm (UR datasheet, 22:32).
- **What that is enough for:**
  - Screws: the OnRobot tolerates up to 0.5 mm of pre-mount error.
  - Clearance holes: ISO 273 medium gives 0.3-0.5 mm a side.
- **What it is not enough for:**
  - the plate in its bore (0.15 mm radial);
  - the spigot in the port (0.10 mm);
  - the H7 dowels (0-0.012 mm).

  Those need a lead-in chamfer and a force-guided spiral search in force mode, as SDU's two-UR10e WRC 2018 cell did (Edison r3 §4.2). The UR's F/T sensor reads ±100 N to ±5.5 N.

### Tip-over (MiR250 94 kg, 131 kg ballast, 30 kg cabinet structure (estimate), 12 kg UR control box, 33.5 kg arm)

The check takes the restoring moment about the MiR's near edge (half its 580 mm width) and divides it by the overturning moment of the payload at reach plus any push at its height. The arm's own mass is lumped at its base. That is an underestimate of the overturning moment when the arm stretches out, so the margins below are upper bounds.

| Case | Payload per arm | Push | Restoring / overturning |
|---|---|---|---|
| chamber assembly, two arms (15.8 kg / 2) | 7.75 kg | 0 N | 14.4 |
| optics bridge with lens and ring, two arms (14.3 kg / 2) | 6.65 kg | 0 N | 14.8 |
| 8.1 kg on one arm (more than any single-arm lift in the sequence) | 8.1 kg | 0 N | 18.9 |
| 12.5 kg at 1300 mm (rated payload at full reach) | 12.5 kg | 0 N | 5.8 |
| reservoir push home 94 N, sideways at 1.25 m | 0.5 kg | 94 N | 6.7 |
| dowel press 1.6 kN (if a robot tried) | 0.0 kg | 1644 N | 0.5 |

MiR publishes a centre-of-mass ceiling for the payload when it drives at 1.2 m/s: 860 mm above the floor for 200 kg. The arm, cabinet, box and ballast here put it at about 480 mm (an estimate). So the cell can drive between stations with the arm folded.

## The sequence, and why it differs from the animation

The robot sequence ([`sequence.py`](analysis/assembly/sequence.py)) keeps the animation's sub-assemblies (render_build.py chapters 3-5), but it changes the order and which way up each part sits. The rule behind every change: every screw is driven from above or from the side, every part goes onto something it can rest on, and nothing heavier than about 8 kg rests on one arm.

1. **Heater stack, gland plate and rod, all upside down (runs 3-4: the round-4 order).** In order:
   - the block, bayonet face down on a pedestal nest;
   - the heaters, the three type K thermocouples (control, edge, limit), the Macor rings and shields, all dropping in from
     above (round 6: the thermal cutoff is gone, [electrical.md](electrical.md) §13.4);
   - the piston head;
   - the disc springs;
   - the three M3 stack screws, driven down;
   - meanwhile, on its own nest: the gland plate's 2-034 face ring, laid in groove up and held by the PFPE film; the plate
     turned over onto the nest; the two 2-114 rod rings, folded through the throat by the loader;
   - the rod, its rod end welded on by the shop (a 316L block with seven Solid Sealing weld-in feedthroughs on its front
     face, [electrical.md](electrical.md) §13.3), lowered top end first through both rod rings on the PEEK bullet. Arm A
     holds it by the block's two end faces, 81 mm across (round 6; run 3 held the Ø22 end cap, where a finger now sits in
     the block); the nest holds the plate;
   - the rod, with the gland plate riding on it, into the head's socket, and the rod's two radial set screws.

   Run 2 built the rod into the head first, turned the stack over and handed it to arm B, and fitted the rod end last
   (M25). That step failed because the rod end is welded to the rod, and in service the weld trapped the gland plate
   (operations.md M7.2). The stack is no longer turned over or handed between the arms.
2. **Module body: upright for its spigot ring, then upside down for the stack (runs 3-4).** In order:
   - arm A sets the welded body upright on a three-post nest, gripping it across the tube between the flange and the
     collar (Ø56.8; round 6, as the turn-overs grip it), and the 2-238 goes on over the mandrel;
   - arm A turns it upside down onto its spigot nest;
   - arm A lowers the whole stack, the rod and the gland plate into the bore from the tube's open end, which faces up, and
     the gland plate lands on the welded collar;
   - six M4, driven down. Round 6: they sit on the arc behind the rod end's block, where the even pattern put three over it;
   - the handle, lowered 15 mm in front of its seat (clear of the rod end's sleeves) and slid back onto the gland plate,
     held by its grip block; then its two M4, which now pass between the sleeves;
   - the striker disc and its three flat-head M3.

   The rod end needs nothing more here: its feedthroughs are welded in by the shop, and their plugs go on at the machine.
   Arm A then turns the module upright, drops the plate in at +8 mm overtravel and gives it the 60° bayonet turn, and turns
   the module over again, ready for the chamber (C10).
3. **Chamber (frame + floor plate).**
   - **On Fixture P.** The plate goes face up on Fixture P, a floor-standing pedestal, and the floor cord is rolled into its gland. Both arms lower the frame onto the plate's two dowels. The 18 M4 floor screws go up through the U-notches with the angle-head nutrunner.
   - **Into the trunnion (run 2).** Both arms carry the 7.4 kg chamber upright into the trunnion's jaws. The trunnion turns it upside down, with both arms parked.
   - **Under-floor work, all from above.** The parts go on in this order:
     - the module's dowel and diamond pin;
     - the outlet plenum and the overflow funnel, each with its face ring held by a PFPE film, and their M4;
     - the module-present sensor;
     - **round 6, the zero-point clamps** ([hot-swap.md](hot-swap.md) §3.2a):
       - the four posts, turned into the floor's M6 inserts by their studs;
       - the two plates on the vacuum gripper;
       - the two SCHUNK NSE-HT mini 88-20 modules, pin face up, on the vacuum gripper (Ø88 is past the 2F-85's stroke);
       - a person fits their push-in elbows and a temporary release-air line, so the modules are open;
     - the whole module, down into the floor port. Arm B holds it by the handle's grip block (round 6). Its two arms' clamping
       pins enter the open modules; then the air is vented and the springs lock them, 2 × 0.5 kN. Until round 5 two captive M6,
       driven on a 130 mm extension, pulled the spigot seal home; they are gone, so the arm pushes it home (132 N running);
     - the Z flange alone and its four M5, then the actuator, belt fold and servo on it (round 6: the servo folded to the back);
     - the four legs, each with one M6 down its Ø11 bore on a 150 mm extension.
4. **Base plate on Fixture B.** Both arms carry the 12 kg base plate onto Fixture B's two columns. Round 6: the zero-point
   release valve goes on it here, because once the chamber is on it stands under the floor.
5. **Back upright, and across (run 2).**
   - The trunnion turns the chamber assembly back upright, then opens its jaws.
   - Both arms each take a leg and carry the assembly straight across onto the base plate.
   - The eight base-plate-to-leg M6 then go in from below.
   - Round 6: a person routes the release-air line from the valve to both modules, in place of the temporary one.
6. **Everything else goes on upright, from above or the side.** Run 2's changes are marked "run 2".
   - The jar. Round 6: it comes in from the front along its lane and up onto its port, held by its grip fin's web, as the
     tending robot holds it; then its sensor and bracket on the front-right leg, and the bracket's two M4.
   - The LED bar before the liners, with the nozzle (run 2).
   - The liners.
   - The inlet plenum, held by A while B drives its M4 into the back wall.
   - The vacuum port.
   - The recoater, as a rail unit, for which the closed chamber needs a new path (run 2):
     - the rail goes on with its carriage, carriage block, ball nut and arm already on it, as bought;
     - the ball screw comes in alone through the right wall's bore and turns through the nut;
     - the blade holder comes in through the door opening.
   - The feedthrough and the bearing cap.
   - The gas knife and the chute.
   - The lid cord, rolled by A (front half) and B (back half), then the lid on the vacuum gripper and its 20 M5.
   - The window stack: the flange and the retaining ring on the vacuum gripper (run 2).
   - The drawer.
   - The metering base, screwed down before its feedthrough covers two of its screws, then the dosing parts and the reservoir.
   - The camera, in its own order: adapter, window O-ring, window, flat ring, retaining ring.
   - The hinges and latches, the door, the hinge pins.
   - Then the optics posts (run 2, moved here from before the turn-over). Arm B holds each post while arm A drives its M6 from below.
   - The 14.3 kg bridge, by both arms, and its eight M6.
   - The galvo riser and the galvo, both on the vacuum gripper (run 2), and the beam path.
7. **People and the machine shop.** These are listed in the step table with a reason for each:
   - the helical inserts;
   - lead and fibre routing;
   - the bore seal (felt);
   - the KF-40 toggle clamp on the jar (round 5: it was a wing-nut clamp);
   - the rod end's weld-ins (the machine shop, round 6);
   - the zero-point modules' push-in elbows and release-air line (round 6);
   - the SAE-4 threaded ports;
   - the f-theta lens (Ø90, threaded);
   - the guard;
   - the draw latches;
   - chapter 5: the 84 kg module onto the tray, the rack and gas units of 23-40 kg, the hoses and the dock.

## Step table

Run 5 (round 6, 2026-11-25), on the merged round-6 model: every row is from one run, `run_assembly.py` with no `--only`. Generated by `report.py` (`analysis/out/assembly/steps.md`).

Runs 5-7 (round 6, 2026-11-25), on the merged round-6 model: run 5 ran every chapter; runs 6 and 7 re-ran chapter 4a and the changed chapter-4b steps (F01-F05b, F07, F10a-F10f, F11, F50), and the latest run's rows replace the earlier ones (each row of `results.json` keeps a `run` tag). Generated by `report.py` (`analysis/out/assembly/steps.md`).

Generated by `report.py` from `run_assembly.py`. Sweep: the part along its insertion path against what is already in its sub-assembly (FCL on 0.1 mm meshes, OpenCascade booleans to confirm a block); gap = smallest clearance on the way. Arm: IK at every 3 mm of the path on one branch, FCL each frame for both arms, tools, D405, changer and held part, the approach planned (RRT-Connect), 1.5 mm depth limit at the seat (byu-vcl PR 318). Clearance = smallest distance from the tool, wrist, forearm and held part to anything they are not meant to touch.

| Step | What | Tool | Arm | Sweep | Gap (mm) | Arms | Arm clearance (mm) | Force / torque | Notes |
|---|---|---|---|---|---|---|---|---|---|
| M01 | Heater block onto the stack nest, bayonet face down | gripper | A | PASS |  | PASS |  |  |  |
| M02 | Three M3 helical inserts in the block's underside |  | machine shop | - |  | - |  |  | Installed right after tapping with a powered insert tool and the tang broken off, as for every insert in the chamber body (render_build chapter 2); a cobot would need a dedicated inserter and tang-break station for 3 inserts. |
| M03 | Three cartridge heaters into their bores | gripper | A | PASS | 0.05 | PASS |  |  | released 24 mm short and pushed home with the closed fingers |
| M04 | Three type K thermocouples (control, edge, limit) into their bores | gripper | A | PASS | 0.09 | PASS | 2.5 |  | released 36 mm short and pushed home with the closed fingers |
| M05 | Macor rings and radiation shields over three guide pins | nozzle | A | PASS | 0.30 | PASS | 2.1 |  | released 9 mm above its seat and let drop over its guide; released 6 mm above its seat and let drop over its guide |
| M06 | Piston head onto the break | gripper | A | PASS | 0.30 | PASS | 1.7 |  |  |
| M07 | Disc springs into the head's slotted counterbores (small-part vacuum nozzle) | nozzle | A | PASS | 0.30 | PASS |  |  |  |
| M08 | Three M3 x 25 stack screws down through the head (torque-controlled: disc-spring preload) | screwdriver | A | PASS |  | PASS | 1.5 | 0.6 N m | 3/3 screws;  |
| M09 | Bore seal (aramid felt + carbon-filled PTFE scraper) stretched into the head's groove |  | person | - |  | - |  |  | A felt strip and a split PTFE scraper are wrapped, not pushed; no published robot method for felt. |
| M10 | Gland-plate face O-ring (2-034) into the gland plate's groove, groove up, PFPE film | gripper+caps | B | PASS | 1.70 | - |  |  |  |
| M11 | Gland plate, its face O-ring held by the film, turned over onto its own nest (face down, rod bore vertical) | gripper | A | PASS |  | PASS |  |  |  |
| M12 | Two 2-114 rod O-rings folded through the Ø15.93 throat into their grooves (ring loader), plate on its nest | ring_loader | A | PASS | 0.14 | PASS | 0.1 |  |  |
| M13 | Rod (its rod end welded on by the shop: a 316L block with seven weld-in feedthroughs) lowered top end first th | gripper | A | PASS | 0.03 | PASS | 2.5 | needs 35 N (peak 104); arm can push 156 N |  |
| M14 | Rod, with the gland plate riding on it, into the piston head's socket (stack upside down: from above) | gripper | A | PASS | 0.02 | PASS |  |  |  |
| M15 | Two M4 cup-point set screws into the rod (radial) | screwdriver | A | PASS |  | PASS | 0.7 | 1.1 N m | 2/2 screws;  |
| M16 | Welded module body onto its upright nest (flange on the nest's three posts), gripped across the tube | gripper | A | PASS |  | PASS |  |  |  |
| M17 | Spigot O-ring (2-238) over the mandrel into the spigot groove (before the stack: the mandrel reaches into the  | gripper | A (holds: B) | PASS | 0.05 | PASS |  |  |  |
| M18 | Module body turned upside down (wrist roll) onto its spigot nest, the tube's open end up |  | A | - |  | PASS |  |  |  |
| M19 | Heater stack, rod and gland plate lowered into the bore from the tube's open end (body upside down); the gland | gripper | A | PASS | 0.20 | PASS |  |  |  |
| M20 | Six M4 x 20 gland-plate screws on the arc behind the rod end's block (round 6, joints.py) | screwdriver | A | PASS |  | PASS | 1.0 | 2.2 N m | 6/6 screws;  |
| M21 | Handle lowered in front of the rod end's sleeves, then slid 15 mm back onto the gland plate (module upside dow | gripper | A | PASS | 2.43 | PASS | 7.7 |  |  |
| M22 | Two M4 handle screws | screwdriver | A | PASS |  | PASS | 0.8 | 2.2 N m | 2/2 screws;  |
| M23 | Striker disc onto the rod end | gripper | A | PASS | 0.12 | PASS |  |  | released 24 mm short and pushed home with the closed fingers |
| M24 | Three M3 x 10 flat-head striker screws | screwdriver | A | PASS |  | PASS | 0.6 | 1.1 N m | 3/3 screws;  |
| M25 | Rod end's seven weld-in feedthroughs (3 x FA11631 + 3 x FA11632 type K, 1 x FA10443 4-pin power) welded into t |  | machine shop | - |  | - |  |  | TIG welds at the block's face and at the rod, on the bare rod before chapter 3, away from every O-ring; the inner joints to the feedthrough pins are made before the sleeves are welded. Ask Solid Sealing to confirm the blind-bore weld and the weld access (elect |
| M26 | Module turned upright (wrist roll, 180 deg about the tool axis) onto the upright nest |  | A | - |  | PASS |  |  |  |
| M27 | Rim wiper onto the plate; plate into the bore onto the bayonet, turned 60 deg (piston at +8 mm overtravel) | gripper | A | PASS | 2.00 | PASS | 0.1 | needs 10 N; arm can push 164 N | released 18 mm short and pushed home with the closed fingers |
| M28 | Module turned upside down again (wrist roll) onto its spigot nest, ready for the chamber (C10) |  | A | - |  | PASS |  |  |  |
| M29 | Right zero-point arm with its clamping pin (SPC mini 20 class, screwed in on the bench) onto the flange's ear  | gripper | A | PASS | 0.30 | PASS | 15.6 |  |  |
| M30 | Left zero-point arm with its clamping pin onto the flange's ear at 135 deg | gripper | A | PASS | 0.30 | PASS | 14.8 |  |  |
| C00 | Overflow funnel: its 2-042 in the block's groove, the block (KF-40 stub welded on) and its four M4 x 12 onto t |  | person (bench) | - |  | - |  |  | operations.md A2.13: with the plate on the bench, face down, all four screws are open from above; on the machine two sit under the KF-40 stub's flange (run 6: 2 of 4). Not checked here: the bench is not modelled. |
| C00a | Floor plate (inserts, the two frame dowels and the overflow funnel already on) onto Fixture P, gland face up,  | vacuum | A | PASS |  | PASS |  |  |  |
| C00b | Floor O-ring cord (3.53 mm, vulcanized splice) rolled into the floor plate's pad gland | roller | A (holds: B) | - |  | PASS | 1.1 |  |  |
| C00c | Frame lowered onto the floor plate's dowels, one arm on each side wall |  |  | - |  | PASS |  | 4.3 kg, 2.1 kg per arm | 4.3 kg;  |
| C00d | Eighteen M4 x 16 floor-plate screws up through the U-notches into the frame's skirt, from under the plate's ed | nutrunner_angle | A | PASS |  | PART | 2.2 | 1.1 N m | 17/18 screws; in the: approach: no path in 500 iterations |
| C01 | Chamber (frame + floor plate, 7.4 kg) carried upright by both arms from Fixture P into the trunnion's jaws |  |  | - |  | PASS | 0.0 | 8.25 kg, 4.1 kg per arm | 8.25 kg;  |
| C01b | The trunnion turns the chamber upside down (180 deg about x), both arms parked |  |  | - |  | PASS |  |  |  |
| C02 | Locating dowel and diamond pin into the floor | gripper | A | PASS | 0.05 | PASS | 37.7 | needs 1644 N; arm can push 149 N | TOO MUCH FORCE for the arm: NO: 16x the F/T range; a UR pushing this hard is past its force limit. Arbor press by a person, or a slip fit (g6) with ;  |
| C03 | Outlet-plenum O-ring (2-044) into the plenum's flange groove, plenum on a nest, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| C04 | Outlet plenum with its O-ring and KF-25 port onto the floor | gripper | A | PASS | 1.68 | PASS | 2.0 |  |  |
| C05 | Six M4 x 12 outlet-plenum screws (60 mm bit extension: two sit beside the KF-25 port) | screwdriver | A | PASS |  | PASS | 2.2 | 2.2 N m | 6/6 screws;  |
| C09 | Module-present sensor | gripper | A | PASS | 0.82 | PASS | 0.5 |  | released 30 mm short and pushed home with the closed fingers |
| C09f | Door hinge knuckles onto the frame's front face, one at a time (shimmed at assembly; screws not drawn) | gripper | B | PASS | 0.30 | PASS | 14.6 |  | released 9 mm short and pushed home with the closed fingers; released 9 mm short and pushed home with the closed fingers; released 9 mm short and pushed home with the closed fingers; released 9 mm short and pushed home with the closed fingers |
| C12 | Z mounting flange alone onto the floor (the actuator goes on after the module, its screws now) | gripper | A | PASS | 0.30 | PASS | 2.9 |  | released 30 mm short and pushed home with the closed fingers |
| C13 | Four counterbored M5 x 12 Z-flange screws | screwdriver | A | PASS |  | PASS | 2.6 | 4.2 N m | 4/4 screws;  |
| C09b | Four zero-point posts turned into the floor's M6 inserts by their studs | gripper | A | PASS | 0.30 | PASS | 3.5 |  |  |
| C09c | Two zero-point module plates (10 mm 6061) onto the posts; their screws into the posts' ends are not drawn | vacuum | A | PASS | 0.30 | PASS | 2.1 |  |  |
| C09d | Two SCHUNK NSE-HT mini 88-20 zero-point modules (Ø88, 1.0 kg) onto the plates, pin face up: the vacuum gripper | vacuum | A | PASS | 0.30 | PASS | 7.2 |  |  |
| C09e | M5 push-in elbows into the modules' release ports, and a temporary Ø4 release-air line from the cell's supply |  | person | - |  | - |  |  | Small threaded fittings with a tube to follow. The modules have to be open (6 bar) for the clamping pins to enter in C10. |
| C10 | Build module (upside down) into the Ø96 floor port along its swap path, held by its handle's grip block; dowel | gripper | B | PASS | 0.05 | PASS | 2.2 | needs 109 N (peak 328); arm can push 132 N | peak beyond the arm: robot starts it on the lead-in chamfer (<= 50 N in force mode) and pushes it home in force mode; the two zero-point modu;  |
| C11 | Release air off: the zero-point modules' springs lock both clamping pins (2 x 0.5 kN); no screws |  | machine | - |  | - |  |  | The cell vents the temporary line. 1 kN holds 4.6x the worst separating load (hot-swap.md 3.2a). The spigot ring is already home: arm B pushed the module in at C10 (132 N running). The captive M6 are gone; the floor keeps their inserts for a hand fallback. |
| C13b | Z actuator, belt fold, servo, carriage, arm and magnet (pre-assembled) onto the flange | gripper | A | PASS | 0.30 | PASS | 8.9 |  |  |
| C14 | Four legs onto the floor, one at a time | gripper | A | PASS | 0.30 | PASS | 4.6 |  |  |
| C15 | One M6 x 25 down each leg's Ø11 bore (160 mm bit extension) | nutrunner | A | PASS |  | PASS | 1.0 | 7.4 N m | 4/4 screws;  |
| C15b | Overflow-jar sensor on its bracket, and the bracket's two M4 x 10, onto the front-right leg on the bench befor |  | person (bench) | - |  | - |  |  | A leg on a nest is open on every side; on the machine its back face is hemmed in by the frame, the other legs, the Z servo and (upright) the base plate. Not checked here: the bench nest is not modelled. |
| F01 | Process base plate onto Fixture B (both arms, one at each end) |  |  | - |  | PASS | 0.0 | 11.79 kg, 5.9 kg per arm | 11.79 kg;  |
| F02 | Levelling mounts |  | person | - |  | - |  |  | They thread in when the finished process module goes onto the tray (chapter 5); until then Fixture B carries the plate on its ends. |
| F02b | Zero-point release valve (3/2 NC, 24 V, on its sub-base) onto the base plate; its screws are not drawn | gripper | A | PASS | 0.30 | PASS |  |  |  |
| F05 | The trunnion turns the chamber assembly (module, Z stage, legs) back upright |  |  | - |  | PASS |  |  |  |
| F05b | Chamber assembly (with the module, zero-point clamps, Z stage and legs) carried upright by both arms, each hol |  |  | - |  | PASS | 117.6 | 19.62 kg, 9.8 kg per arm | 19.62 kg;  |
| F06 | Eight M6 x 25 base-plate-to-leg screws, from under the plate | nutrunner_angle | A | PASS |  | PART | 3.0 | 7.4 N m | 7/8 screws; 316 #1: approach: no clear way in to the hole's mouth (A/upper_arm hits Base plate, process module |
| F06b | Release-air line: Ø4 tube from the valve through a union Y to both zero-point modules' push-in elbows (in plac |  | person | - |  | - |  |  | Tube routing (deformable), as the hoses in chapter 5. The modules stay locked while the line is swapped: their springs hold. |
| F07 | Overflow jar in from the front along its lane and up 8 mm onto its KF-40 port, held by its grip fin | gripper | A | PASS | 0.30 | PASS | 15.0 |  |  |
| F08 | KF-40 toggle clamp (MKS 100318805) round the jar's flange, lever to the front |  | person | - |  | - |  |  | Its hinged ring has to be held open round both flanges before one push on the lever locks it; nothing on the 2F-85 holds the ring open. An air-released KF clamp would let the robot do it (hot-swap.md). |
| F11 | LED bar (small-part vacuum nozzle on its top face) | nozzle | A | PASS | 6.00 | PASS | 6.0 |  |  |
| F10a | Wall liner, back lower left, in through the door opening and onto its wall | gripper | A | PASS | 0.36 | FAIL | 0.6 |  | arm A: A/gr/right_finger hits Module M50 handle (6061, screwed under the gland plate; riser, arm and I-section robot grip block at y -156 to -126, in front of the door's hinge knuckles) at 354 mm along the insertion |
| F10b | Wall liner, back upper left, in through the door opening and onto its wall | gripper | A | PASS | 0.36 | FAIL | 2.6 |  | arm A: A/gr/left_finger hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) at 381 mm along the insertion |
| F10c | Wall liner, left, in through the door opening and onto its wall, held by its hanger tab (plate fingers) | gripper+plate | A | PASS | 0.36 | PASS | 0.1 |  |  |
| F10d | Wall liner, back lower right, in through the door opening and onto its wall | gripper | A | PASS | 0.36 | FAIL | 0.8 |  | arm A: A/gr/right_finger hits Module M50 handle (6061, screwed under the gland plate; riser, arm and I-section robot grip block at y -156 to -126, in front of the door's hinge knuckles) at 354 mm along the insertion |
| F10e | Wall liner, back upper right, in through the door opening and onto its wall | gripper | A | PASS | 0.36 | FAIL | 2.6 |  | arm A: A/gr/left_finger hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) at 381 mm along the insertion |
| F10f | Wall liner, right, in through the door opening and onto its wall, held by its hanger tab (plate fingers) | gripper+plate | A | PASS | 0.36 | PASS | 0.1 |  |  |
| F12 | Through-beam fibre heads with their 2-010 O-rings, threaded into the side walls from outside |  | person | - |  | - |  |  | Threading an M6 head with a fibre attached means winding the fibre with it; the ring itself is a pick-and-place. |
| F13 | Inlet-plenum O-ring (2-044) into the plenum's flange groove, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F14 | Inlet plenum with its O-ring and KF-25 port onto the back wall, held there by arm A | gripper | A | PASS | 1.68 | FAIL |  |  | arm A: no IK at the start pose at 0 mm along the insertion; held-part screws: 316 #7: screwdriver: B/tool/screwdriver hits Inlet plenum port (KF-25); also no way with nutrunner |
| F14h | Inlet plenum with its O-ring and KF-25 port onto the back wa: screws of plenum_in driven while arm A holds it | nutrunner_angle/screwdriver | B (holds: A) | PASS |  | PART | 0.8 | 2.2 N m | 6/7 screws; 316 #7: screwdriver: B/tool/screwdriver hits Inlet plenum port (KF-25); also no way with nutrunner |
| F15 | Nine M4 x 16 inlet-plenum screws into the back wall | screwdriver | B | - |  | - |  | 2.2 N m | all screws of this joint were already driven (with the part held) |
| F16 | Vacuum-port adapter (KF-25 stub welded in) with its 2-024 O-ring onto the right wall | gripper | A | PASS | 0.30 | FAIL |  |  | released 12 mm short and pushed home with the closed fingers; held-part screws: 316 #1: screwdriver: B/tool/screwdriver hits A/wrist1; also no way with nutrunner, nutrunner_angle; 316 #2: screwdriver: B/tool/screwdriver hits A/wri |
| F16h | Vacuum-port adapter (KF-25 stub welded in) with its 2-024 O-: screws of vac_port driven while arm A holds it | nutrunner_angle | B (holds: A) | PASS |  | FAIL |  | 4.2 N m | 0/4 screws; 316 #1: screwdriver: B/tool/screwdriver hits A/wrist1; also no way with nutrunner, nutrunner_angle; 316 #2: screwdriver: B/tool/screwdriver hits A/wrist2; also no way with nutrunner, nutrunner_angle; 316 #3: screwdriver: B/tool/screwdriver hits A/w |
| F17 | Four M5 x 20 vacuum-port screws | screwdriver | A | - |  | - |  | 4.2 N m | all screws of this joint were already driven (with the part held) |
| F18 | Recoater rail with its carriage, carriage block, ball nut and arm (bought and pre-assembled on the rail) onto  | gripper | A | PASS | 2.40 | FAIL |  |  | released 24 mm short and pushed home with the closed fingers; held-part screws: d thro: screwdriver: B/upper_arm hits Base plate, process module (MIC-6, 15 mm); also no way with  |
| F18h | Recoater rail with its carriage, carriage block, ball nut an: screws of rail driven while arm A holds it | nutrunner_angle | B (holds: A) | PASS |  | PART | 1.9 | 2.2 N m | 3/4 screws; d thro: screwdriver: B/upper_arm hits Base plate, process module (MIC-6, 15 mm); also no way with  |
| F19 | Five M4 x 16 rail screws, driven from inside the chamber toward the back wall | screwdriver | A | - |  | - |  | 2.2 N m | all screws of this joint were already driven (with the part held) |
| F21 | Ball screw in through the right wall's bore and turned through the ball nut (30 turns at 10 mm lead) into the  | gripper | A | PASS | 1.00 | PASS | 3.0 |  | released 33 mm short and pushed home with the closed fingers |
| F22 | Feedthrough spacer, its two 2-024 O-rings, the Ferrotec unit and the coupling on the left wall | gripper | A | PASS | 0.30 | PASS |  |  |  |
| F23 | Blind bearing cap and its 2-019 O-ring on the right wall | gripper | A | PASS | 0.30 | FAIL | 22.1 |  | released 15 mm short and pushed home with the closed fingers; held-part screws: 316 #1: screwdriver: B/tool/screwdriver hits A/wrist2; also no way with nutrunner, nutrunner_angle; 316 #2: screwdriver: B/tool/screwdriver hits A/wri |
| F23h | Blind bearing cap and its 2-019 O-ring on the right wall: screws of bearing_cap driven while arm A holds it | nutrunner_angle | B (holds: A) | PASS |  | FAIL |  | 2.2 N m | 0/4 screws; 316 #1: screwdriver: B/tool/screwdriver hits A/wrist2; also no way with nutrunner, nutrunner_angle; 316 #2: screwdriver: B/tool/screwdriver hits A/wrist2; also no way with nutrunner, nutrunner_angle; 316 #3: screwdriver: B/tool/screwdriver hits A/w |
| F24 | Four M4 x 20 bearing-cap screws | screwdriver | A | - |  | - |  | 2.2 N m | all screws of this joint were already driven (with the part held) |
| F25 | Motor standoff, bracket and recoater servo | gripper | A | PASS | 0.05 | FAIL | 0.0 |  | arm A: held:F25:Recoater motor bracket hits Trunnion stands at 0 mm along the insertion |
| F26 | Blade holder and blade, in through the door opening and up under the recoater arm | gripper | A | FAIL | 0.05 | FAIL | 1.3 |  | sweep: Blade holder blocked by Process chamber body (6061-T6 through-frame from 5 after 43.0 mm; arm A: held:F26:Blade holder hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) at 90 mm along t |
| F27 | Two M3 x 8 blade screws | nutrunner_angle | A | PASS |  | FAIL |  | 1.1 N m | 0/2 screws; 316 #1: screwdriver: A/tool/screwdriver hits Build module M50: spigot, flange, honed 316L cylinder; 316 #2: screwdriver: A/upper_arm hits Fixture B (open stand); also no way with nutrunner_angle |
| F28 | Gas knife and dose chute | gripper | A | PASS | 3.00 | PASS | 3.0 |  |  |
| F29 | Lid O-ring cord (3.53 mm) rolled into the body's top gland: arm A rolls, arm B feeds the cord | roller | A (holds: B) | - |  | PASS | 0.9 |  |  |
| F30 | Lid (inserts in) onto the cord, by the vacuum gripper | vacuum | A | PASS | 0.30 | PASS |  |  |  |
| F31 | Twenty M5 x 25 lid screws, star pattern | screwdriver | A | PASS |  | PASS | 2.6 | 4.2 N m | 20/20 screws;  |
| F32 | Window-flange O-ring (2-036) into the flange's lower groove, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F33 | Field stop | gripper | A | PASS | 0.10 | PASS | 0.1 |  | released 27 mm short and pushed home with the closed fingers |
| F33b | Window flange with its O-ring (Ø100: the vacuum gripper) | vacuum | A | PASS | 0.30 | PASS |  |  |  |
| F34 | Six counterbored M4 x 16 window-flange screws (torque-controlled) | screwdriver | A | PASS |  | PASS | 2.2 | 2.2 N m | 6/6 screws;  |
| F35 | Window O-ring (2-031) into the flange's seat groove | gripper+caps | B | PASS | 1.15 | PASS |  |  |  |
| F36 | Ø2 in. fused-silica window onto its O-ring | gripper | A | PASS | 0.20 | PASS |  |  | released 27 mm short and pushed home with the closed fingers |
| F37 | FKM flat ring | gripper | A | PASS | 0.30 | PASS | 0.3 |  | released 24 mm short and pushed home with the closed fingers |
| F37b | Window retaining ring (Ø100: the vacuum gripper) | vacuum | A | PASS | 0.20 | PASS |  |  |  |
| F38 | Six M3 x 10 retaining-ring screws (torque-controlled: clamp the silica evenly) | screwdriver | A | PASS |  | PASS | 1.5 | 0.8 N m | 6/6 screws;  |
| F39 | Cover-slide drawer (2-033 in its half-dovetail, put in on the bench) into the lid's front edge | gripper | A | PASS | 0.30 | PASS |  | needs 50 N (peak 358); arm can push 1500 N | released 6 mm short and pushed home with the closed fingers |
| F40 | Quarter-turn drawer latches |  | robot (custom bit) | - |  | - |  |  | Two quarter-turn studs, turned with a slotted bit on the screwdriver; the latch hardware is an envelope in the model (seals.md: no catalogue latch fits). |
| F41 | Drawer-closed sensor | gripper | A | PASS | 1.32 | PASS | 1.0 |  | released 18 mm short and pushed home with the closed fingers |
| F42 | Metering-base O-ring (2-040) on its lid side (groove faces down when fitted: PFPE film) | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F42b | Metering-base dock-face O-ring (2-040), groove up | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F43 | Metering base alone (feedthrough, coupling and stepper not yet on) onto the lid | gripper | A | PASS | 0.30 | PASS | 23.2 |  |  |
| F44 | Four M4 x 16 metering-base screws (before the roller feedthrough covers two of them) | nutrunner | A | PASS |  | PASS | 0.0 | 2.2 N m | 4/4 screws;  |
| F45 | Roller feedthrough (threaded M8 x 1 over its 2-012), coupling, stepper, dock rails, load cell, NFC, side port, | gripper | A | FAIL | 0.30 | FAIL | 0.2 |  | sweep: Roller shaft blocked by Metering base (6061, fluted roller over a 100 mm d after 0.0 mm; arm A: no IK at the start pose at 0 mm along the insertion; sweep: Roller feedthrough O-ring blocked by Metering base (6061, fluted roller over a 100 mm d after 0.0 |
| F46 | Reservoir M slid onto the dovetail dock (about 94 N to seat on the dock O-ring) | gripper | A | PASS | 1.10 | PASS |  | needs 94 N; arm can push 191 N |  |
| F47 | Camera adapter O-ring (2-022), PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F48 | Camera viewport adapter with its 2-030 | gripper | A | PASS | 0.30 | PASS | 5.7 |  |  |
| F48b | Camera window gasket (1 mm FKM flat ring), window, flat ring, retaining ring, in that order, then the camera | gripper | A | FAIL | 0.04 | FAIL | 0.1 |  | sweep: Camera window gasket, under the window blocked by Camera viewport adapter + boss (6061; Ø30 bore on  after 1.0 mm; arm A: A/gr/right_finger_tip hits Camera viewport adapter + boss (6061; Ø30 bore on the line of sight, Ø20 aperture, Ø1 in. window; FKM se |
| F49 | Pressure transducer and relief valve (SAE-4 O-ring-boss ports) |  | person | - |  | - |  |  | Threaded ports need a wrench on a hex and a set torque; a 2F-85 can only spin a plain body. |
| F50 | The two draw-latch strikes on the chamber's side faces (the hinge knuckles went on in C09f) | gripper | A | PASS | 0.26 | PASS |  |  |  |
| F51 | Door (cord rolled into its half-dovetail on the bench) brought in, knuckles in line | gripper | A | PASS | 0.01 | PASS | 0.0 | needs 725 N |  |
| F52 | Hinge pins slid in along x | gripper | A | PASS | 0.10 | FAIL |  |  | arm A: A/upper_arm hits A cabinet at 0 mm along the insertion |
| F03 | Optics posts (moved here: they blocked the side-wall parts and the right latch) onto the base plate, one at a  | gripper | B | PASS | 0.30 | FAIL | 2.2 |  | held-part screws: 316 #3: approach: no path in 500 iterations; 316 #4: approach: no path in 500 iterations; held-part screws: 316 #7: approach: no clear way in to the hole's mouth (no IK (out of reach or joint limit)); 316 #8: approach: no clear way in to the  |
| F03h | Optics posts (moved here: they blocked the side-wall parts a: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | PASS | 3.0 | 7.4 N m | 2/2 screws;  |
| F03h | Optics posts (moved here: they blocked the side-wall parts a: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | FAIL |  | 7.4 N m | 0/2 screws; 316 #3: approach: no path in 500 iterations; 316 #4: approach: no path in 500 iterations |
| F03h | Optics posts (moved here: they blocked the side-wall parts a: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | PASS | 3.0 | 7.4 N m | 2/2 screws;  |
| F03h | Optics posts (moved here: they blocked the side-wall parts a: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | FAIL |  | 7.4 N m | 0/2 screws; 316 #7: approach: no clear way in to the hole's mouth (no IK (out of reach or joint limit)); 316 #8: approach: no clear way in to the hole's mouth (no IK (out of reach or joint limit)) |
| F04 | Two M6 x 25 up into each post's bottom cap, from under the plate | screwdriver | A | - |  | - |  | 7.4 N m | all screws of this joint were already driven (with the part held) |
| F53 | f-theta lens threaded into its adapter ring over its 3 mm shim stack, under the bridge (on the bench, bridge u |  | person | - |  | - |  |  | The Ø90 lens is wider than the 2F-85's 85 mm stroke and threads M85 x 1; a strap wrench by hand (operations.md: lens and ring fitted to the bridge on the bench). |
| F54 | Optics bridge (13.3 kg, lens and ring under it) onto the four posts, one arm at each end |  |  | - |  | FAIL |  | 14.32 kg, 7.2 kg per arm | 14.32 kg; no collision-free pair of arm poses at the start of the carry |
| F55 | Eight M6 x 35 bridge screws down into the posts | nutrunner | A | PASS |  | PASS | 3.0 | 7.4 N m | 8/8 screws;  |
| F56 | Galvo riser plate (155 x 130: the vacuum gripper) | vacuum | A | PASS | 0.30 | PASS | 21.2 |  |  |
| F56b | basiCube 20 scan head on the riser (3.75 kg: the vacuum gripper on its top) | vacuum | A | PASS | 0.30 | FAIL |  |  | arm A: no IK at the start pose at 0 mm along the insertion |
| F57 | Beam tubes, dichroic and fold-mirror cubes, shutter, photodiode chain and collimator | gripper | A | PASS | 0.00 | FAIL |  |  | arm A: part 107 mm across at the grasp: wider than the 2F-85's 85 mm stroke; arm A: no IK at the start pose at 0 mm along the insertion; arm A: no IK at the start pose at 0 mm along the insertion; arm A: no IK at the start pose at 0 mm along the insertion; arm |
| F58 | Process fiber routed to the collimator |  | person | - |  | - |  |  | Armoured fiber, >= 100 mm bend radius: cable routing stays manual. |
| F59 | Class 1 laser guard: T-slot frame, panels, door rail, sliding door, guard lock, operator panel |  | person | - |  | - |  |  | T-slot nuts and 1.5 mm panels up to 730 mm wide; its hardware is not drawn (joints.NOT_DRAWN). |
| T01 | Process module (84 kg) off Fixture B onto the VLM tray; levelling mounts threaded in |  | person + hoist | - |  | - |  |  | 84 kg is 3.4 times two UR12e payloads; a hoist or lift table. |
| T02 | 19 in. rack and its units (UPS 23 kg, laser 40 kg, PC 8 kg, DIN drawer 9 kg) |  | person + lift | - |  | - |  |  | the UPS and the laser exceed a UR12e's 12.5 kg; cage nuts and screws are not drawn |
| T03 | Gas module: base plate, scroll pump (26 kg), blower, filter housing, O2 box, argon manifold |  | person + lift | - |  | - |  |  | the pump exceeds 12.5 kg; the units' screws are not drawn |
| T04 | KF-25 bellows, vacuum valve, argon and O2 lines, and the zero-point valve's air supply |  | person | - |  | - |  |  | hose and tube routing (deformable, KF wing-nut clamps) |
| T05 | Tray dock and umbilicals |  | person | - |  | - |  |  | cable and hose routing |
| T06 | Leak check: rate of rise from <= 1 mbar, O2 drift at +20 mbar argon |  | machine | - |  | - |  |  | the seal verification in assembly.md |

## Seals: every O-ring and cord

Every gland comes from `lpbf_low.GLANDS` after `build()`, plus the lid cord. `seals_forces.py` computes the numbers and writes them to [`out/assembly/seals_forces.json`](analysis/out/assembly/seals_forces.json).

| Gland | Ring | Installed stretch | Most stretch while fitting | How the cell fits it | Lead-in it needs |
|---|---|---|---|---|---|
| lid | 3.53 mm cord (vulcanized splice) | cord (no stretch); a moulded 2-277 would be +2.76 % (+2.18 to +3.35 % over tolerance) | corners R13: 12 % bending strain (Parker: R >= 10.6) | cord laid in by arm B at the midpoints, ends, quarter points (Adebola et al. 2024), rolled home by arm A's 3.2 mm PTFE wheel at 10-20 N; the splice at a straight run | none (axial face seal) |
| spigot | 2-238 | +2.3 % | +9.3 % | stretched over the acetal spigot mandrel (cone + 0.45 mm sleeve) and pushed off into the groove by the pusher | floor port's lower edge: 20 deg x 2.5 mm, now in the model (FP-04), = Trelleborg's minimum for 3.53 mm; the spigot's top edge is covered by the mandrel's sleeve |
| gland_plate_M50 | 2-034 | +1.5 % | +3.4 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| rod_M50 x 2 | 2-114 | +2.2 % on the rod; OD -3.8 % in the groove | folded: ~34 % bending strain at a 2.5 mm fold | folded into the slotted loader tube (kidney fold), pushed through the Ø15.93 throat and released into the groove, the deeper groove first; then the rod enters on the PEEK bullet | rod end: the bullet's 15 deg nose (>= 3.0 mm at 15 deg); the throat's edges rounded R0.2-0.4 and polished |
| overflow_funnel | 2-042 | +2.0 % | +3.2 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| floor | 3.53 mm cord (vulcanized splice) | cord (no stretch); a moulded 2-277 would be +1.73 % (+1.16 to +2.31 % over tolerance) | corners R11.5: 13 % bending strain (Parker: R >= 10.6) | floor plate face up on Fixture P: cord laid in by arm B, rolled home by arm A's 3.2 mm wheel; nothing above the plate yet, so the roller has the whole gland to itself | none (axial face seal) |
| inlet_plenum | 2-044 | +2.0 % | +3.1 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| outlet_plenum | 2-044 | +2.0 % | +3.1 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| vacuum_port | 2-024 | +2.5 % | +6.0 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| fibre_heads x 2 | 2-010 | +2.1 % | +18.6 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| recoater_feedthrough | 2-024 | +2.5 % | +6.0 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| recoater_cap | 2-019 | +2.2 % | +7.1 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| window_lower | 2-031 | +1.7 % | +3.9 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| window_flange | 2-036 | +2.6 % | +4.2 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| drawer | 2-033 | +2.0 % | +4.0 %; through a 1.71 mm lip: 3.8-7.7 % lateral squeeze, 0.116-0.353 N/mm | 2F-85 pin caps open inside the ring (2-point internal grip), lay it on the groove, roller_n presses it under the dovetail lip | none (axial face seal) |
| metering_base | 2-040 | +2.0 % | +3.4 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| reservoir_dock | 2-040 | +2.0 % | +3.4 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| roller_feedthrough | 2-012 | +2.7 % | +13.5 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| reservoir_lid_M | 2-030 | +2.0 % | +4.4 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| camera_adapter | 2-030 | +2.4 % | +4.9 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| sae4_ports x 4 | 3-904 | on the fitting | - | comes fitted on the transducer and relief valve; turned in with the part | SAE J1926 port's 12 deg chamfer (part of the port standard) |
| door | cord |  | ; through a 1.71 mm lip: 3.8-7.7 % lateral squeeze, 0.116-0.353 N/mm | cord: vulcanized ring rolled into the half-dovetail (roller_n), arm B tensioning the free loop | none (axial face seal) |

What this table says:

- **Installed stretch is within Parker's limit everywhere.** Parker allows 5 % or less (ORD 5700 §3.3, [handbook](https://nfc.arizona.edu/sites/default/files/2022-02/parker_o-ring_handbook.pdf), read 22:18 UTC). Every face ring sits at 1.4-2.7 %. The spigot ring is at +2.3 % and the rod rings at +2.2 %.
- **Stretch while fitting is low too.** Parker says installation stretch "ordinarily does not exceed 25-50 %". The most any ring sees here is 18.6 %: the 2-010 fibre-head ring, opened by the pin caps. The 2-238 sees 9.3 % over the mandrel, and only for the seconds the pusher takes. Edison found no published dwell limit, so the cell holds no ring stretched for longer than one move.
- **The rod rings are the exception.** To pass the gland plate's Ø15.93 throat, each 2-114 has to be folded, not stretched. Folding it into a kidney shape small enough for the loader puts about 34 % bending strain in its outer fibre (an estimate, at a 2.5 mm fold radius). That is a quarter of FKM's 125 % elongation at break, but it is the step most likely to nick or twist a ring.
  - Edison rates it "Medium". It needs a loader, trials and a borescope check.
  - A gland plate split at the grooves, with a retainer forming one side of each groove, would let the rings drop into open grooves instead. See patch request 5.

**A moulded AS568 ring in the near-rectangular face grooves.**
- **Lid** (959.0 mm inner perimeter). A 2-278 (ID 304.39 ± 1.65 mm, Parker Table 9-1) would sit on the inner wall at +0.29 %, and at -0.25 to +0.83 % over its tolerance.
  - The length is right. At the bottom of the tolerance band it is 2.6 mm slack, which the 1.07 mm of free width in the 4.6 mm groove takes up.
  - The corners are the problem. The gland's inner corners are R4.3. Parker §4.3 asks for at least 3 × the cross-section (10.6 mm), and ideally 6 × (21.2 mm), for a standard ring in a non-circular groove. Bending a 3.53 mm section round R4.3 strains its outer fibre 29 %; at R10.6 that is 14 %. The cord has the same corners, so it has the same problem, plus a splice.
  - Long term, a ring held bent at 29 % takes a compression set at the four corners, and that is where a lid seal would start to leak.
- **Floor** (new, chamber-construction.md). The gland has R11.5 corners, which meets Parker's rule. A moulded 2-277 would sit at +1.73 % (1.16-2.31 % over tolerance) with 13 % corner strain.
  - The cell can fit a moulded ring there with no splice. See patch request 3.

**Lead-in chamfers.** Parker gives only "10-20°, chamfer longer than the ring's overlap". The lengths below are Trelleborg's Table 16, read 22:41 UTC. Only three places need one:
1. **The floor port's lower edge.** The 2-238 on the spigot enters it from below. It needs at least 3.5 mm at 15°, or 2.5 mm at 20°. The model draws a sharp edge there (patch request 2).
2. **The spigot's own top edge.** It is flush with the powder floor and must stay sharp. The mandrel's 0.45 mm sleeve covers it while the ring goes on, so the ring never touches it.
3. **The rod's lower end.** The PEEK bullet gives it a 15° nose. The rod's 1.65 mm wall is too thin to chamfer 3 mm.

The reservoir plate's leading edge slides across the dock's 2-040. It should get the 1.5 mm × 20° lead-in that Trelleborg gives for 1.78 mm, or it will shave the ring.

**Half-dovetails (door, drawer).** Pushing the 1.78 mm cord through the 1.71 mm lip squeezes it 3.8 % sideways at nominal size and 7.7 % at maximum size. By Lindley's relation that takes 0.12-0.35 N per mm of contact, so the roller's 8-25 N spring is far more than enough. Force is not the problem.
- The problem is seals.md's note (a). The groove is overfilled: 94 % nominal, 111 % at worst tolerance when warm.
- Edison rates robotic half-dovetail insertion "at the boundary of current capability", 60-80 % first-pass success (an estimate).
- The cell fits these cords on the bench, with the door and the drawer face up on nests, where the roller has the whole groove. That makes it the easiest form of the hardest case.

**Lubricant.** A film of Krytox LVP, wiped on with a lint-free swab.
- It is a PFPE grease: 1 × 10⁻¹³ Torr at 20 °C, rated -15 to 300 °C, and Chemours lists Viton A as compatible ([data sheet](https://cdn.shopify.com/s/files/1/0270/6758/0483/files/Krytox_LVP.pdf), 22:36 UTC). A 2 oz tube is listed at $90-220.
- The film also holds a face ring in a groove that faces down when the part goes on: the gland plate, the outlet and inlet plenums, the funnel block, the window flange, the metering base's lid side and the camera adapter.
  - That is common practice, but it is the step where a ring falls out unseen.
  - So the D405 looks at each of these grooves just before the part goes on, and the force check below catches a ring pinched under the flange.

**Verification**, in the order the cell does it:
1. **Vision.** The D405's RGB, 70-120 mm from the groove before each closure, checks that the ring is present, unbroken, in the groove all the way round, and not twisted.
   - At 100 mm, with its 87° × 58° field and 1280 × 720 pixels, a pixel covers about 0.12 mm.
   - Its depth is quoted at ±2 % at 50 cm (Intel). A distributor quotes about ±1.4 % at 20 cm, but that came from a search snippet and was not fetched. Either way it is too coarse to see a 0.5-0.9 mm proud cord, so seating is checked by force, not depth. (Adebola et al. needed a side view for the same reason.)
2. **Force.**
   - The roller presses at a set 10-20 N in force mode. The UR's F/T sensor reads ±100 N to ±5.5 N. A dip in that force means a gap; a spike means an overlap.
   - The rod and the spigot follow reference curves: 35 N running and 104 N break-out for the rod, 109 N and 328 N for the spigot (Parker §5.11.2, dry). A double peak means a pinched ring.
   - A face flange screwed down metal to metal shows nothing in its torque. So the vision check before closure is the only per-ring check those seals get.
3. **Leak test.** The rate of rise from 1 mbar or below, then the O₂ drift at +20 mbar argon (seals.md), then a helium sniff of each new joint if the rate of rise fails.

## Forces: what each step needs against what the arm and its tools give

| Step | What | Needs | Basis | Robot? |
|---|---|---|---|---|
| C02 | Ø6 m6 dowel and diamond pin pressed 10 mm into the 6061 floor (H7) | 1644 N | Lame press fit, 0.008 mm diametral interference, mu 0.15: p = 58 MPa | NO: 16x the F/T range; a UR pushing this hard is past its force limit. Arbor press by a person, or a slip fit (g6) with retaining compound so the robot only inserts it |
| C10 | spigot's 2-238 entering the Ø96 floor port | 109 N (peak 328 N) | Parker 5.11.2: fc 2.07 lb/in at 22.1 % over pi x 96 mm; break-out 3x | robot starts it on the lead-in chamfer (<= 50 N in force mode), the two captive M6 screws pull it home |
| M22 | hollow rod through the two 2-114 rod O-rings | 35 N (peak 104 N) | Parker 5.11.2: fc 1.99 lb/in at 21.3 % over pi x 15.875 mm, two rings | yes in force mode with a PFPE film (lubricated, about half); dry break-out is at the F/T range |
| M23 | build plate into the honed bore (0.15 mm radial clearance) and onto the bayonet | 10 N | sliding fit; 10 N contact for a spiral search | yes: force-guided spiral search; positioning alone (AprilTag + D405, about +-0.4 mm) is coarser than the clearance |
| F39 | drawer against its 2-033 (358 N to squeeze, seals.md) | 50 N (peak 358 N) | the two quarter-turn latches pull it the last 0.4 mm | robot pushes to first contact only |
| F46 | reservoir onto the dock O-ring along its 2 deg ramps (seals.md) | 94 N | seals.md: 94 N push home, 58 N pull-out | yes, but at the F/T range's edge (100 N): set the push to 94 N +- 5.5 N |
| F51 | door draw latches, 725 N preload each (seals.md) | 725 N | 1807A61 over-centre latches | NO: a person closes them (or pneumatic clamps, seals.md (b)) |
| screws | M3 / M4 / M5 / M6 A2-70 in A2 inserts, mu 0.14 (MoS2 paste) | M3 1.1, M4 2.2, M5 4.2, M6 7.4 N m | Pfeiffer Vacuum's A2-70 table (90 % of Rp0.2): M4 2.2, M5 4.2, M6 7.4 N m at mu 0.14; M3 from TR Fastenings | OnRobot Screwdriver 0.15-5 N m covers M3-M5; M6 needs the inline nutrunner (1.5-10 N m) |
| M02/C01 | helical inserts (M3-M6) | insert 0.45-3 (Bollhoff's powered tools) N m | Bollhoff HELICOIL power tools E-S 206 (0.45-0.95 N m), E-PSG (0.9-3 N m) | machine shop, with the tang broken off |

- **What the UR12e gives.**
  - **Force sensing:** the F/T sensor reads ±100 N and ±10 N m, to ±5.5 N and ±0.5 N m (UR12e datasheet, 22:32 UTC). UR publishes no maximum force for `force_mode`; the script manual only says the actual wrench "may be lower".
  - **Raw push:** limited by the joint torques. At the force steps' own poses, [`push.json`](analysis/out/assembly/push.json) gives the largest static push along the insertion before a joint reaches its limit, C02 (arm A): 149 N; C10 (arm A): 119 N; F39 (arm A): 1500 N; F46 (arm A): 191 N; M22 (arm B): 161 N; M23 (arm A): 164 N; F30 (arm A): 113 N. Those figures load each link's mass only on the joints upstream of it, as the corrected `cell.max_force` and `shop_checks.joint_torques` do.
  - **What limits it:**
    - A downward push at these poses tops out at 113-191 N before a joint reaches its torque limit. Holding the pose alone uses 31-48 % of the most-loaded joint.
    - Horizontally (the drawer) it is 1.5 kN.
  - **So:**
    - The reservoir's 94 N, the rod's 35 N running and the plate's 10 N search are all within both the motors and the sensor.
    - The spigot's 328 N break-out is not: 119 N is available at C10.
    - Nor is the dowels' 1.6 kN: 149 N is available.
- **Screws.** At μ 0.14 (MoS₂ paste on 316 in 18-8 inserts, Pfeiffer's table), the joints need:

  | Screw | Torque | Driver |
  |---|---|---|
  | M3 | 1.1 N m | OnRobot (0.15-5 N m, ±0.04 N m below 1.33 N m) |
  | M4 | 2.2 N m | OnRobot |
  | M5 | 4.2 N m | OnRobot, at 84 % of its maximum |
  | M6 | 7.4 N m | inline nutrunner (1.5-10 N m) |

  - The OnRobot stops itself at 35-45 N axial, so a screw that cross-threads stops it instead of the arm.
  - A 7.4 N m reaction is well inside the wrist's 56 N m and the QC-21's Mz rating of 35 N m.
- **Seal closures don't need the arm's force.**
  - The lid's 20 × M5, the floor's 18 × M4 and the flanges all squeeze their rings metal to metal.
  - The spigot's 109-328 N is pulled home by its two captive M6.
  - The drawer's 358 N is closed by its latches.
  - The arm only starts each part, under 50 N.
- **What the arm can't do:**
  - press the dowels (1.6 kN);
  - close the door's draw latches (725 N each).

## Changes needed, as patch requests for files this note doesn't own

1. **ANSWERED BY THE ORDER (round 4, 2026-11-22), no part change:** the rod end stays welded, the gland plate goes onto the
   rod's top end first and the stack enters the bore from the tube's open end (the update at the top; chapter 3 re-run as
   run 3). The original request follows. **Rod end: clamp it, don't weld it** (`cad/modules_low.py` / `cad/lpbf_low.py` rod-end part; `cad/joints.py` new joint `rod_end_M50`).
   - **Why:** step M25 fails, and the sweep shows it: the welded cap is part of the rod. At assembly the rod has to pass down through the gland plate's two 2-114 rings, so the cap can only go on afterwards, and welding 10 mm from FKM is not an option. In service the same weld traps the gland plate (operations.md M7.2).
   - **Change:**
     - make the cap a sleeve on the plain Ø15.875 rod: bore Ø15.90 H8 × 20 deep;
     - one Parker rod groove Ø20.0 × 3.6 inside it for a third 2-114, sealing on the rod's OD;
     - two M4 × 6 cup-point set screws at 90° and 270°, the same detail as the piston head's socket;
     - the hermetic connector's boss unchanged.
   - The cell then fits the cap from above with the module upside down (M24-M27). The cap's 2-114 goes in with the same loader.
2. **DONE in the model (FP-04, 2026-11-21):** **Lead-in chamfer on the floor port's underside edge** (`cad/lpbf_low.py`, floor plate).
   - **Change:** 20° × 2.5 mm on the Ø96 port's lower edge, polished R0.2. That is Trelleborg Table 16's minimum for a 3.53 mm ring; 15° × 3.5 mm also does.
   - **Why:** the module's 2-238 enters the port from below, and a sharp edge there shaves it.
   - The port's top edge, flush with the powder floor, stays sharp. The ring never passes it.
3. **PARTLY DONE: the lid gland corners are now R13 in the model (2026-11-21).** **Lid gland corners to R ≥ 10.6 mm, and moulded rings in both cord glands** (`cad/lpbf_low.py`: the lid O-ring and its gland cut; `GLANDS["floor"]`).
   - Still open: the moulded rings. Re-derived from the model, a 2-277 fits the lid's new 941.7 mm inner perimeter at +2.8 % (2.2-3.4 % over tolerance) with 12 % corner strain, and the floor gland at +1.7 %.
   - **Lid:** the inner wall's corner radius is 4.3 mm, against Parker §4.3's 3 × 3.53 = 10.6 mm minimum. That puts 29 % bending strain at the corners.
     - Open the inner wall to R11.5, as the new floor gland already is. Then re-pick the moulded ring for the lid's new inner perimeter.
     - At today's perimeter it would be a 2-278 at +0.3 %.
   - **Floor:** specify an AS568 2-277 (ID 291.69 mm) in place of the spliced cord. It sits at +1.7 % stretch (1.2-2.3 % over tolerance) with 13 % corner strain, and has no splice.
   - The cell rolls both kinds in the same way.
4. **Module dowels and floor-plate dowels: no press fit by robot** (`cad/joints.py`, `module_dowels` and `floor_dowels`).
   - A Ø6 m6 dowel pressed 10 mm into 6061 needs about 1.6 kN (Lamé, 0.008 mm interference, μ 0.15).
     - That is 16 × the UR's F/T range.
     - Pushed by an arm on a MiR at 1 m height, it would tip the MiR: restoring / overturning moment 0.5.
   - **Either:** press them in the machine shop on an arbor press before the floor plate reaches the cell. Mark both dowel steps "machine shop".
   - **Or:** ream for a slip fit (H7 hole, g6 pin) and retain them with a retaining compound (e.g. Loctite 638). Then the robot inserts them with a 10 N spiral search.
5. **Rod gland: open grooves instead of a throat** (`cad/modules_low.py`, gland plate). This is optional, but it removes the riskiest seal step (M12; M18 in runs 1-2).
   - Split the 14 mm gland plate at the first groove. A 5 mm 316L retainer ring then forms each groove's outer side, held by the same six M4.
   - Each 2-114 then drops into an open, stepped bore instead of being folded through a Ø15.93 throat.
6. **KF-40 clamp on the overflow jar: over-centre lever clamp** (`cad/lpbf_low.py`, "Overflow clamp").
   - A hinged wing-nut clamp needs two hands (F08: a person). A lever-type KF-40 clamp can be closed by one 2F-85 pushing its lever.
7. **Door: robot-closable clamps, and a 2.62 mm cord** (`cad/lpbf_low.py`, door).
   - **Clamps:** the two 1807A61 draw latches need 725 N each to set (seals.md); a person does F51 today. seals.md (b)'s pneumatic over-centre clamps (DE-STA-CO 802-U class, 890 N) would let the robot or the controller close the door.
   - **Cord:** the half-dovetail is overfilled (seals.md (a)). The 2.62 mm cord in Parker's half-dovetail (Design Chart 4-5) fixes that.
8. **Floor-plate screws: the driver has to reach down to 1.1 N m, driving upward** (a tooling choice; `joints.py` key `floor` is fine as drawn).
   - The 18 M4 floor screws go up through U-notches at the plate's edge at about 1.1 N m (JOINT_NOTES).
   - The OnRobot can't drive upward, and the PLUTO 10 class starts at 1.5 N m. So the angle-head nutrunner (E8b) has to be one whose range starts at 1 N m or below.
   - The run found all 18 drives clear with it.
9. **Two locating pins on each flange that one arm must hold while the other screws it** (`cad/joints.py`: `plenum_in`, `vac_port`, `bearing_cap`).
   - **Change:** two Ø3 m6 dowels per flange, pressed into the frame's wall, with slip holes in the flange.
   - **Why:** F14, F16 and F23. The flanges sit on the back wall and the right wall, which arm A can reach only around the chamber.
     - The inlet plenum's start pose is out of A's reach (F14).
     - The right-wall flanges need the stand clear (F16, F23).
   - With pins, the arm that places the flange can also drive its screws.

**Round 6 (2026-11-25) additions:**

10. **S25's handle screws sit over the rod end's block** (`cad/joints.py` handle screws, or the handle in `cad/modules_low.py`;
    operations.md A1).
    - Neither a torque screwdriver nor a ball-end key reaches them (A1.22 on S25), and they can't move clear inside S25's
      Ø55.4 gland plate.
    - **Order change (no part change):** fit the handle and its two M4 to the gland plate before the rod goes through it
      (A1.21-A1.22 straight after A1.11). S25's rod set screws point sideways, so the handle's riser doesn't block them.
    - On M50 and L75 the handle screws are reachable now.
11. **electrical.md §13.3 still gives round 5's 72 × 16 mm face** with sleeves at x ±12.5, ±21.5 and ±30.5. The model is now
    81 × 16 mm, at ±11.85, ±26.16 and ±34.83. The spacing rule (2.4 mm between sleeves) is the same; ask Solid Sealing about weld
    access on this layout.
12. **The check doesn't test the fingers against the part they hold** (`run_assembly.py`). C10's grasp had the fingers inside the
    bore in runs 1-3, and it passed; it was found by reading the grasp. A check would need contact depth, because the pads touch
    the part by design.
13. **The jar's KF-40 toggle clamp is still a person's step** (F08). An air-released KF clamp, or a bayonet jar, would let the
    robot do it ([hot-swap.md](hot-swap.md)).

**Which remaining failures depend on these patches:**
- C02 (dowels: the arm can push 149 N, the press needs 1.6 kN) needs 4.
- F08 (KF-40 clamp, a person) needs 6.
- F51 (door latches, a person) needs 7.
- F14, F16 and F23 need 9. In F14 arm A can't reach behind the back wall to hold the inlet plenum while B screws it. In F16 and F23 arm B's driver meets arm A's holding wrist at the vacuum port and the bearing cap. Pins remove the holding.
- F45 (roller feedthrough) is threaded. The straight sweep can't show a screw motion; a person or a spinning wrist does it.

**Run 2 applied this note's own fixes:**
- the trunnion positioner in place of both two-arm turn-overs;
- Fixture B as two columns under the base plate;
- tool stands hung below the cabinet tops;
- the posts after the side-wall parts and the latches;
- the recoater as a rail unit, the ball screw alone, the blade holder through the door opening;
- the vacuum gripper for the three parts wider than 85 mm, the nozzle for the small parts;
- the F43/F48 step fixes;
- 1000 RRT iterations for screw approaches, with a pre-approach slid out from under the plate;
- a 130 mm extension for the captive M6;
- the trunnion's jaws opening before the arms lift the chamber out.
