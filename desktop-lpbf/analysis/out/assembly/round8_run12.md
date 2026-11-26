# Round 8, run 12 (2026-11-26): two hands, MiRs that drive like MiRs, fixed cameras

Sterling, 2026-11-26, on round 7's video: "moonwalk, motion sickness, collisions and interference ... The thought was also that
the two robots would be working in tandem with each other similar to how a human has two hands, holding something down for
example." Lessons 2, 3 and 5 of [`notes/2026-11-26-byu-vcl-video-lessons.md`](../../../notes/2026-11-26-byu-vcl-video-lessons.md).
Nothing here has been built or tried on hardware.

## What run 12 is

`run_assembly.py` with `ASM_RECORD`, on round 7's model and sequence plus the holds below. The first process ran M01-F28 and
was then stopped by the CI harness's 30-minute limit on background jobs. F29 onward was planned in three processes that each
fast-forwarded the steps before their own (`ASM_FF_UNTIL`: each step's end state, nothing planned or recorded):

- F29-F38 continued the first process's recording (`ASM_CONTINUE`: arm states and chunk numbering).
- F39-F50 and F51 onward started their recordings afresh, with both MiRs at the trunnion dock.

The planner is deterministic (seeded RRT-Connect, no time limits). The pieces differ from one sequential run in one way: the
idle MiR stands where the fast-forward left it, not where the previous step left it.

## Against run 11

| | Run 11 | Run 12 |
|---|---|---|
| checked steps passed | 99 of 108 | 99 of 108 (the same nine fail: C00d, F15, F18, F26, F27, F45d, F48b, F54, F57) |
| screws driven | 124 of 129 | 124 of 129 (6 of them now by the second arm while the first holds the part) |
| picks at the long table on a planned path | 57 of 74 | 57 of 74 |
| MiR moves | straight along x, reversing 402 m in total | 167 routes, pivot-drive-pivot, 6.9 m reversing in 29 docking legs of at most 0.5 m |
| robot time (recorded) | 2.9 h | 3.3 h: pivots (868 s at 30 deg/s, an estimate) and longer routes |

Files: [`results_run12.json`](results_run12.json), [`round8_run12.json`](round8_run12.json) (against run 11), per-step time in
[`run12_times.json`](run12_times.json).

## Two hands ([`two_hands.json`](two_hands.json), [`two_hands.py`](../../assembly/two_hands.py))

A part placed on a face seal floats on it. The seal takes far more force to squeeze than the part weighs (Lindley's formula, as
in seals_forces.py, at 20 % squeeze), so the first screw would tip the part. The placing arm keeps its gripper or vacuum cup on
the part while the other arm drives the first two screws; then it lets go (`hold_first`).

| Step | Part | Squeeze (20 %) vs weight | Run 12 |
|---|---|---|---|
| M19 | heater stack, rod and gland plate on the 2-034 | 252 N vs 10 N | **hold used**: arm A holds, arm B drives 2 of 6 ([still](r8_two_hands_M19.png)) |
| C04 | outlet plenum on its 2-044 | 439 N vs 6 N | **hold used**: arm A holds, arm B drives 2 of 6 ([still](r8_two_hands_C04.png)) |
| F30 | lid on its 3.53 mm cord | 2,737 N vs 26 N | **hold used**: arm A's vacuum cup holds, arm B drives 2 of 20 |
| F33b, F37b, F43 | window flange, retaining ring, metering base | 280, 208, 338 N vs 1-5 N | needed, **not possible**: arm B's upper arm meets Fixture B on each of the three screws it tried |
| F14, F16, F23 | plenum, vacuum port, bearing cap on two dowels | | not needed: located and carried by the dowels before the seal is touched (round 7's fix stays) |
| C12, C14, M21, M23, F05b, F54 | parts that sit on a flat or a pilot, no seal | | not needed: weight, pilots, countersinks |
| F18, F03 | rail on a wall, posts screwed from below | | hold used since round 7 |
| F51-F52 | door before its hinge pins | | needed, **not tried**: arm B would push the pins from the back round the chamber; or close the draw latches first |

Steps where both arms work: 19 (run 11: 16).

## MiRs ([`mir_drives.json`](mir_drives.json), [`mir_route.py`](../../assembly/mir_route.py))

Each MiR docks heading +x. It drives forward toward +x, and it reverses only as a docking leg of at most 0.5 m. A longer move
toward -x turns round at a clear spot: pivot 90 deg, 130 mm out, pivot 90 deg. It drives back along the return lane and turns in
the same way at or behind the dock. Every pose was swept with FCL against the bench, the fixtures, the parts in the cell, the
long table and its items, and the other MiR and arm: pivots every 2 deg, legs every 20 mm. The swept bodies are the MiR, its
cabinet, plate, tool stand and screw presenter, and the parked arm with whatever it holds.

- 167 moves, 248 pivots. 163 are clear.
- 4 are not clear. Arm B's cabinet and presenter meet the zero-point release-air line that lies past the table's edge, on F45
  and F45b. The same line blocked those drives in run 10.
- The turns beside the table swing the MiR's corners up to about 270 mm under the table top's edge, with 20 mm under the top.
  The check passes, but a real MiR's 3-D cameras would see the top as an obstacle. Turning spots past the table's ends, or a
  wider aisle, would avoid it.

## Camera (asm_render.py, [`camera_rig.json`](camera_rig.json))

The camera is a fixed tripod per place in the cell, plus three set up where a MiR stops at the table. A shot is chosen per step
by occlusion, held, and changed only by a cut; the camera never moves inside a shot. Every arm motion is drawn. After the
chapter's first 4 drives and 8 picks, a fetch from the table is an ellipsis: checked and timed, not drawn, with a cut and a line
saying so. A pick or move the planner could not plan is a card, never an animation.
