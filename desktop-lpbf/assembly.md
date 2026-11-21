# Assembling the desktop LPBF with two UR12e arms: the sequence, collisions in motion, the seals and the forces

Written 2026-11-20 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260). It answers
two comments on the [build animation](build-sequence.md):
- a BYU machinist: "Some of those gaskets might be hard to get on ... the animation was not worried about space and collisions";
- sgbaird: "have a set of two UR12e-s do the fine-detail assembly ... knowing that creation and use of additional tooling is fine. Also address the point about collisions rather than just space. Be thorough".

The cell follows [byu-vcl PR 318](https://github.com/vertical-cloud-lab/byu-vcl/pull/318) (round 14, commit 11d4410), through [`analysis/robot/cell.py`](analysis/robot/cell.py).

Nothing here has been built or tried on hardware. The numbers come from the model, from the sources cited, or from estimates, which are labelled as such. The model is `cad/lpbf_low.py` with the M50 module, as of 23:07 UTC. That includes the chamber change of [chamber-construction.md](chamber-construction.md): a through-frame and a bolted floor plate with a second 3.53 mm cord.

## Result

**Two UR12e arms can do most of the fine assembly. They cannot do it to this design, in the animation's order, with stock tools.** The run covered:
- 113 steps from chapters 3-5;
- 135 screws in 23 joints, which is every screw the model draws for chapters 3-4 except the reservoir's own two lid screws (fitted when it is filled);
- every part of the M50 build module and the process module.

Each step was checked in motion: the part swept along its insertion path, both arms checked frame by frame on a planned approach, and the 1.5 mm audit. The full table is [below](#step-table).

| | Pass | Fail | Person or machine shop |
|---|---|---|---|
| Build module (chapter 3), 22 parts, seals and turn-overs | 17 | 3 | 2 (inserts, felt bore seal) |
| Chamber and under-floor work, Fixture P and C | 12 of 13 | 1 (the first turn-over) | 0 |
| Upright work on Fixture B, 40 steps | 18 | 22 | 8 |
| Screws (135) | 91 driven on a planned, collision-free approach | 44 | - |
| of which the tool reaches and the drive itself is clear | 118 | 17 | - |
| Chapter 5 (tray, rack, gas, hoses) | - | - | 6: 84 kg, 23-40 kg units, hoses |

**What it takes:**
1. **Turn things over, so every screw goes in from above or the side.**
   - The module body is turned over twice and the heater stack once, each by one arm rolling its wrist. All three pass.
   - The chamber is turned over twice by both arms: 7.4 kg (frame + floor plate), then 15.8 kg (with the module, Z stage and legs). Both of those fail in this run; see below.
2. **Open fixtures 1000 mm up**, so the arms can reach under the floor plate and the base plate:
   - Fixture P, a floor-standing pedestal under the floor plate;
   - Fixture B, an open stand under the base plate.
3. **The right drivers.**
   - The OnRobot Screwdriver works only downward or sideways, tops out at 5 N m, and holds only magnetic screws. 316 screws aren't magnetic.
   - An inline nutrunner takes the M6 joints (7.4 N m).
   - An angle-head nutrunner drives everything upward. Pointing an inline tool upward puts the wrist under the arm base and into the pedestal; no collision-free pose was found.
   - All three need retaining bits.
4. **Custom tools.** A spigot mandrel and pusher, a PEEK rod bullet, a ring loader, a PTFE roller for the cords, and pin caps for the 2F-85. A small vacuum nozzle is still needed.
5. **Pick-insert-push.** 16 parts are let go 6-39 mm short of their seat and pushed home with the closed fingers, because the fingers would otherwise hit what the part goes into. Three Macor rings are dropped the last 21-27 mm over guide pins.

**What fails, by cause.** Patch requests and cell changes are at the end.

- **Design:**
  - The welded rod end can't go on once the rod is through the gland (M25).
  - The recoater carriage and ball screw have no path into the closed chamber (F20, F21; sweep-blocked at 182 and 214 mm). The new through-frame is open at the bottom before the floor plate goes on, so they can go in from below first.
  - The blade holder's path is blocked by the carriage block (F26).
- **Order:**
  - The optics posts, placed early, block arm A's fingers at the side-wall parts: the Ferrotec feedthrough, the bearing cap, the motor bracket (F22, F23, F25). They also block the right draw latch's way in (F50, the hand-check's U2.2).
  - Fit the posts after the side-wall work. Their screws still go in from under Fixture B.
- **Cell:**
  - Fixture B's end frames are 124-184 mm from the chamber's side walls. That is too close for the right-wall screws: the vacuum port, the bearing cap and the hinge pins (F16, F23, F52). Move the frames out, or carry the base plate on its front and back edges.
  - The second turn-over (F05) fails when arm B's upper arm reaches its own tool stand. Mount the stands lower or at the cabinet's side.
  - At Fixture C the module's captive M6 and the Z-flange M5 (C11, C13) find no pose: the first IK branch's upper arm hits the bench top. Raise Fixture C 300 mm or put it at the bench's end.
- **Grasp:**
  - The first turn-over (C01) folds arm B's forearm onto its own gripper.
  - The 14.3 kg bridge (F54) has no collision-free pair of start poses.
  - The inlet plenum can't be held from the front while arm B screws it from behind (F14). Two locating pins on the back wall would let one arm place it and then drive it.
- **Tool:**
  - The Macor rings and disc springs need a small vacuum nozzle (M05, M07). The 2F-85's 22 mm fingertips hit the thermocouples and the head.
  - The 100 mm window flange and retaining ring and the 130 mm galvo are wider than the 2F-85's 85 mm stroke (F33, F37, F56). Use the vacuum gripper.
  - The OnRobot's 86 × 114 mm body is blocked at the outlet plenum, the dosing base and the rail. The nutrunner reaches all of them (C05, F44, F18).
- **Planning budget:**
  - All 18 floor screws (C00d) and all 8 base-plate screws (F06) are reachable, and their drive is clear. The approach under the plate wasn't found within 300 RRT iterations for 15 and 8 of them.
  - On a real cell that is one taught via-point.
- **My step list:**
  - The metering base was swept without the O-rings that ride on it (F43).
  - The camera window was ordered before its own O-ring (F48).

  Both are corrected in `sequence.py` and were not re-run.

**Collisions, not just space.** On the way in, the tightest gaps are:

| Step | Gap | Where |
|---|---|---|
| rod in the head (M10) | 0.02 mm | |
| stack in the bore (M22) | 0.03 mm | the rod passing the gland plate |
| heaters (M03) | 0.05 mm | Ø6.1 bores |
| spigot mandrel's sleeve (M20) | 0.05 mm | over the Ø95.8 spigot |
| module into the port (C10) | 0.05 mm | |
| dowel (C02) | 0.05 mm | |

The arms' tightest clearance to anything they may not touch is 0.0-0.1 mm. Those cases are fingers beside a seated part, at the plate's bore (M23) and the floor screws. The roller works within 1.0-1.1 mm of the gland walls.

**Seals.**
- **Stretch.** Every ring's installed stretch is 1.4-2.7 %; Parker allows 5 %. The most stretch while fitting is 18.6 % (2-010), well under Parker's 25-50 %.
- **Rod rings.** The two 2-114 rod rings have to be folded through a Ø15.93 throat: about 34 % bending strain, the riskiest seal step.
- **Lid gland.** It has R4.3 corners, against Parker's R ≥ 10.6 mm, so a moulded ring (2-278 fits the length at +0.3 %) or the cord takes 29 % bending strain there. The new floor gland's R11.5 meets the rule, and a moulded 2-277 fits it at +1.7 % with no splice.
- **Port chamfer.** The floor port needs a 2.5 mm × 20° lead-in for the 2-238.
- **Half-dovetails.** The roller needs only 0.12-0.35 N/mm. Their trouble is seals.md's overfill.

**Forces.**
- **Push.** At their poses the arms can push 113-191 N downward before a joint reaches its torque limit (corrected link-mass torques). The F/T sensor reads to ±100 N.
- **Too much for the arm:**
  - the spigot seal's 328 N break-out, which the captive M6 pull home;
  - the dowels' 1.6 kN press fit, for the machine shop;
  - the door latches' 725 N each, for a person.
- **Tip-over.** The MiR250 with its 131 kg ballast keeps a restoring / overturning moment of 5.8 or more for any load the arms carry. A robot pressing a dowel would tip it (0.5).


## Renders

Rendered offscreen by [`render_assembly.py`](analysis/assembly/render_assembly.py) from the run's own snapshots: the same arm poses, tools, held parts and placed parts the checks used. The cell overview is under [The cell](#the-cell).

| | |
|---|---|
| ![Chamber assembly (15.5 kg) turned over by both arms holding two legs](analysis/out/assembly/render_F05_mid.png) | ![Heater stack into the bore: the rod on its bullet passes the two rod O-rings](analysis/out/assembly/render_M22_1.png) |
| F05, the tightest moment of the second turn-over: the 15.8 kg chamber assembly halfway through its 180 deg turn, carried 1.1 m by both arms holding two legs. The run stops later in this carry, when arm B's upper arm reaches its own tool stand. | M22: arm B lowers the heater stack into the module bore. The plate-to-bore gap is 0.03 mm. The rod on its PEEK bullet passes the two 2-114 rod rings, and B lets go 39 mm short and pushes it home. |
| ![Spigot O-ring: mandrel on the spigot, pusher stroke](analysis/out/assembly/render_M20.png) | ![Build module (upside down) into the floor port on Fixture C](analysis/out/assembly/render_C10_1.png) |
| M20: the spigot's 2-238 goes on over the acetal mandrel. Arm A strokes the pusher down, and the sleeve clears the spigot by 0.05 mm. | C10: the finished module goes down into the floor port of the upside-down chamber on Fixture C, with 0.05 mm clearance at the spigot. Its captive M6 then pull the seal home. |
| ![Chamber set onto the base plate on Fixture B](analysis/out/assembly/render_F05.png) | ![Lid cord rolled into the body's gland (roller on arm A)](analysis/out/assembly/render_F29_A_0.png) |
| F05: the chamber assembly at the end of the checked part of its carry, over the base plate on Fixture B. | F29: arm A rolls the lid cord into the frame's gland, working over the chamber between the optics posts (1.0 mm from the gland walls). Arm B does the back half. |
| ![Chamber turn-over by both arms (F05), every few frames of the checked path](analysis/out/assembly/turnover_F05.gif) | ![F06: base-plate-to-leg M6 driven up from under the plate (angle-head nutrunner)](analysis/out/assembly/render_screw_F06.png) |
| F05, the two-arm turn-over, every few frames of the checked path. | F06: a base-plate-to-leg M6 driven up from under the base plate on Fixture B by the angle-head nutrunner. All 8 drives are clear; the approach under the plate was not planned within 300 RRT iterations. |
| ![C00d: floor-plate M4 driven up through a U-notch (angle-head nutrunner)](analysis/out/assembly/render_screw_C00d.png) | ![F31: lid M5 (OnRobot Screwdriver, side-mounted)](analysis/out/assembly/render_screw_F31.png) |
| C00d: a floor-plate M4 driven up through its U-notch, with the plate on Fixture P. The angle head keeps the wrist 250 mm to the side. | F31: a lid M5 driven by the side-mounted OnRobot Screwdriver. All 20 pass, with 2.6 mm to spare. |
| ![F18: rail M4 driven from inside the chamber (angle-head nutrunner)](analysis/out/assembly/render_screw_F18h.png) |  |
| F18: a recoater-rail M4 driven from inside the chamber toward the back wall by the angle-head nutrunner (4/4). The OnRobot's body does not fit inside the 190 mm deep chamber. |  |

## How it was checked

Everything is in [`analysis/assembly/`](analysis/assembly/). One command re-runs it on whatever `cad/` holds (about 25 min):

```bash
OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/assembly/run_assembly.py     # the build, step by step
/tmp/venv/bin/python desktop-lpbf/analysis/assembly/seals_forces.py                                    # seals, forces, tip-over
/tmp/venv/bin/python desktop-lpbf/analysis/assembly/report.py                                          # steps.md, sequence.json, push.json
xvfb-run -a -s "-screen 0 1600x1200x24" /tmp/venv/bin/python desktop-lpbf/analysis/assembly/render_assembly.py
```

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

Flips and two-arm carries are checked the same way along the part's whole path (lift, turn, move, lower), with both arms' IK and collisions at every frame.

What is not simulated: the elastomer's own shape while it is stretched or rolled (the tools are checked, not the rubber), cables and hoses, the pick side of each step (kitting trays), and the MiR's own driving.

## The cell

![Cell layout](analysis/out/assembly/render_cell.png)

- **Arms.** Two UR12e arms, each with a 2F-85 and a D405, on MiR250s with 480 mm cabinets, so each arm's base is 800 mm above the floor. These are byu-vcl PR 318's arms. Arm A docks on the front of the bench (y < 0) and arm B on the back. Each MiR slides along x to line up with a station, as PR 318's MiR drives along the VLM opening. Each arm base sits 240 mm off the bench edge.
- **Bench and stations.** The bench is 1400 × 800 mm, with its top at 760 mm. On it, from left to right:
  - the module nests;
  - Fixture C, where the chamber sits upside down.

  Fixture P stands on the floor beside the bench. It is a column that carries the floor plate 1000 mm up, so the arms can reach under the plate's edges. Fixture B is an open stand that holds the process base plate by its two ends, 1000 mm up, with the front and back left open.
- **Tool changer.** Each arm has an ATI QC-21 automatic changer: 25 kg, Mxy 56.5 N m, 42.4 mm coupled, plus about a 16 mm UR plate. The QC-11 is lighter (0.245 kg, 36.1 mm), but it is rated only 20.3 N m in Mxy. The two-arm lifts below put up to about 15 N m on each wrist, which leaves the QC-11 too little margin. The D405 clamps to the changer's master side, so it stays on every tool.
- **Tool stand.** Each arm has one on its own cabinet, behind the arm base, as PR 318 keeps finger sets on a stand on the MiR. Each stand holds that arm's set of tool plates.

| Tool | On | Used for | Published numbers (fetched 2026-11-20 UTC) |
|---|---|---|---|
| Robotiq 2F-85 | both arms | parts, flips, two-arm carries, hand tools (mandrel, pusher, loader) | 85 mm stroke, 20-235 N, 0.925 kg; pads 38 × 22 mm ([manual](https://blog.robotiq.com/hubfs/support-files/2F-85_2F-140_General_PDF_20210623.pdf), 22:24) |
| 2F-85 pin caps (custom) | either | small rings (internal two-point grip), Macor rings, disc springs | 2 mm wall over the pad, Ø2 × 6 mm pin |
| OnRobot Screwdriver | A | M3-M5 screws driven down or sideways | 0.15-5 N m, M1.6-M6, 2.5 kg, 308.5 × 86 × 114 mm, side-mounted. Downward or sideways only. Magnetic screws only ([datasheet v1.7](https://onrobot.com/storage/datasheets/screwdriver/datasheet_screwdriver_v1.7_en), 22:18) |
| Inline nutrunner (Kolver PLUTO 10 class) | either | M6 driven down (7.4 N m), and M4-M5 where the OnRobot's body doesn't fit | 1.5-10 N m, 0.5 kg (Brera 2022, via [Edison r3](edison/r3-robot-oring-assembly/answer.md)). The Ø40 × 250 mm envelope is an estimate. |
| Angle-head nutrunner (Atlas Copco / Kolver angle-head class) | either | every screw driven upward: the 18 floor-plate M4, the 8 post-base and 8 leg-base M6 | 0.5-10 N m class. The envelope is an estimate: Ø40 × 230 mm body, 90° head 44 × 40 × 46 mm. An inline driver pointing up puts the wrist under the arm base and into the pedestal; this one keeps the wrist 250 mm to the side. |
| OnRobot VGC10 | A | the floor plate, the lid, the wall liners | 0.814 kg; 100 × 100 × 101.5 mm; 6 kg on its standard cups, up to 15 kg on custom ones ([datasheet](https://onrobot.com/storage/datasheets/vgc10/datasheet_vgc10_v1.7_en.pdf), 22:24) |
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
| chamber assembly at the second turn-over, two arms (15.8 kg / 2) | 7.75 kg | 0 N | 14.4 |
| optics bridge with lens and ring, two arms (14.3 kg / 2) | 6.65 kg | 0 N | 14.8 |
| 8.1 kg on one arm (more than any single-arm lift in the sequence) | 8.1 kg | 0 N | 18.9 |
| 12.5 kg at 1300 mm (rated payload at full reach) | 12.5 kg | 0 N | 5.8 |
| reservoir push home 94 N, sideways at 1.25 m | 0.5 kg | 94 N | 6.7 |
| dowel press 1.6 kN (if a robot tried) | 0.0 kg | 1644 N | 0.5 |

MiR publishes a centre-of-mass ceiling for the payload when it drives at 1.2 m/s: 860 mm above the floor for 200 kg. The arm, cabinet, box and ballast here put it at about 480 mm (an estimate). So the cell can drive between stations with the arm folded.

## The sequence, and why it differs from the animation

The robot sequence ([`sequence.py`](analysis/assembly/sequence.py)) keeps the animation's sub-assemblies (render_build.py chapters 3-5), but it changes the order and which way up each part sits. The rule behind every change: every screw is driven from above or from the side, every part goes onto something it can rest on, and nothing heavier than about 8 kg rests on one arm.

1. **Heater stack, built upside down on a pedestal nest.** In order:
   - the block, bayonet face down;
   - the heaters, thermocouples, cutoff, Macor rings and shields, all dropping in from above;
   - the piston head;
   - the disc springs;
   - the three M3 stack screws, driven down;
   - the rod, into the head's socket;
   - its two radial set screws.

   Arm A then turns the stack over in its wrist (a 180° roll about the tool axis, 320 mm above the bench) and hands it to arm B. B takes it by the heater block from above, with its fingers crossed at 90° to A's.
2. **Module body, built upside down on its spigot face.** In order:
   - the gland plate with its 2-034 face ring (held by the PFPE film);
   - six M4, driven down;
   - the handle and its two M4;
   - the two 2-114 rod rings, folded through the throat by the loader.

   Arm A then turns the body upright onto a three-post nest. Next:
   - the 2-238 goes on over the mandrel;
   - arm B lowers the stack into the bore on the PEEK bullet, the rod passing down through both rod rings;
   - arm A drops the plate in at +8 mm overtravel and gives it the 60° bayonet turn.

   A turns the module over again for the rod end and the striker's three flat-head M3.
3. **Chamber (frame + floor plate):**
   - **Floor plate on Fixture P.** The plate goes face up on Fixture P, a floor-standing pedestal. The floor cord is rolled into its gland. Both arms lower the frame onto the plate's two dowels, and the 18 M4 floor screws go up through the U-notches with the angle-head nutrunner.
   - **First turn-over.** Both arms, one on each side wall, turn the chamber over onto Fixture C. The chamber sits on four strips outside the lid gland.
   - **Under-floor work, all from above:**
     - the module's dowel and diamond pin;
     - the outlet plenum and the overflow funnel, each with its face ring held by the PFPE film, and their M4;
     - the module-present sensor;
     - the whole module, down into the floor port; its two captive M6 pull the spigot seal home;
     - the Z stage and its four M5;
     - the four legs, each with one M6 down its Ø11 bore on a 150 mm bit extension.
4. **Base plate and posts on Fixture B.**
   - Both arms carry the 12 kg base plate onto Fixture B.
   - Arm B holds each optics post while arm A drives its two M6 up from below with the angle-head nutrunner.
5. **Second turn-over (15.8 kg).** Both arms take the chamber by two diagonal legs, lift it off Fixture C, turn it 180° about the arms' common axis while carrying it about 1.1 m across, and set its legs on the base plate. The eight base-plate-to-leg M6 then go in from below.
6. **Everything else goes on upright, from above or the side:**
   - the jar, the liners and the LED bar;
   - the inlet plenum, held by A while B drives its M4 into the back wall;
   - the vacuum port;
   - the recoater;
   - the gas knife and the chute;
   - the lid cord, rolled by A (front half) and B (back half), then the lid on the vacuum gripper and its 20 M5;
   - the window stack;
   - the drawer;
   - the metering base, screwed down before its feedthrough covers two of its screws;
   - the dosing parts and the reservoir;
   - the camera, the hinges and latches, the door, the hinge pins;
   - the optics bridge (14.3 kg with its lens, by both arms) and its eight M6;
   - the galvo and the beam path.
7. **People and the machine shop.** These are listed in the step table with a reason for each:
   - the helical inserts;
   - lead and fibre routing;
   - the bore seal (felt);
   - the KF-40 wing-nut clamp;
   - the SAE-4 threaded ports;
   - the f-theta lens (Ø90, threaded);
   - the guard;
   - the draw latches;
   - chapter 5: the 84 kg module onto the tray, the rack and gas units of 23-40 kg, the hoses and the dock.

## Step table

Generated by `report.py` from `run_assembly.py`. Sweep: the part along its insertion path against what is already in its sub-assembly (FCL on 0.1 mm meshes, OpenCascade booleans to confirm a block); gap = smallest clearance on the way. Arm: IK at every 3 mm of the path on one branch, FCL each frame for both arms, tools, D405, changer and held part, the approach planned (RRT-Connect), 1.5 mm depth limit at the seat (byu-vcl PR 318). Clearance = smallest distance from the tool, wrist, forearm and held part to anything they are not meant to touch.

| Step | What | Tool | Arm | Sweep | Gap (mm) | Arms | Arm clearance (mm) | Force / torque | Notes |
|---|---|---|---|---|---|---|---|---|---|
| M01 | Heater block onto the stack nest, bayonet face down | gripper | A | PASS |  | PASS |  |  |  |
| M02 | Three M3 helical inserts in the block's underside |  | machine shop | - |  | - |  |  | Installed right after tapping with a powered insert tool and the tang broken off, as for every insert in the chamber body (render_build chapter 2); a cobot would need a dedicated inserter and tang-break station for 3 inserts. |
| M03 | Three cartridge heaters into their bores | gripper | A | PASS | 0.05 | PASS |  |  | released 24 mm short and pushed home with the closed fingers |
| M04 | Thermocouples and the thermal cutoff | gripper | A | PASS | 0.09 | PASS | 0.1 |  | released 33 mm short and pushed home with the closed fingers |
| M05 | Macor rings and radiation shields over three guide pins | gripper+caps | A | PASS | 0.30 | FAIL | 0.1 |  | released 27 mm above its seat and let drop over its guide; released 24 mm above its seat and let drop over its guide; released 21 mm above its seat and let drop over its guide; arm A: A/cap/left_finger_tip hits Type K thermocouples M50 (control, edge, limit; 0 |
| M06 | Piston head onto the break | gripper | A | PASS | 0.30 | PASS | 1.7 |  |  |
| M07 | Disc springs into the head's slotted counterbores | gripper+caps | A | PASS | 0.30 | FAIL |  |  | arm A: A/cap/left_finger_tip hits Piston head M50 (6061-T6, cool side of the break; Tier B: 316L with a water channel) (3.0 mm deep); pushed home instead, but A/cap/left_finger_tip hits Piston head M50 (6061-T6, cool side of the break; Tier B: 316L with a wate |
| M08 | Three M3 x 25 stack screws down through the head (torque-controlled: disc-spring preload) | screwdriver | A | PASS |  | PASS | 1.5 | 0.6 N m | 3/3 screws;  |
| M09 | Bore seal (aramid felt + carbon-filled PTFE scraper) stretched into the head's groove |  | person | - |  | - |  |  | A felt strip and a split PTFE scraper are wrapped, not pushed; no published robot method for felt. |
| M10 | Hollow rod into the head's socket | gripper | A | PASS | 0.02 | PASS |  |  |  |
| M11 | Two M4 cup-point set screws into the rod (radial) | screwdriver | A | PASS |  | PASS | 0.7 | 1.1 N m | 2/2 screws;  |
| M12 | Welded module body onto its nest, spigot face down | gripper | A | PASS |  | PASS | 41.4 |  |  |
| M13 | Gland-plate face O-ring (2-034) into the gland plate's groove, groove up, PFPE film | gripper+caps | B | PASS | 1.70 | - |  |  |  |
| M14 | Gland plate, its face O-ring, onto the welded collar | gripper | A | PASS | 1.70 | PASS |  |  |  |
| M15 | Six M4 x 20 gland-plate screws, star pattern | screwdriver | A | PASS |  | PASS | 2.2 | 2.2 N m | 6/6 screws;  |
| M16 | Handle under the gland plate | gripper | A | PASS | 2.43 | PASS | 36.6 |  |  |
| M17 | Two M4 handle screws | screwdriver | A | PASS |  | PASS | 2.2 | 2.2 N m | 2/2 screws;  |
| M18 | Two 2-114 rod O-rings folded through the Ø15.93 throat into their grooves (ring loader) | ring_loader | A | PASS | 0.14 | PASS | 0.1 |  |  |
| M19 | Module body turned upright (wrist roll, 180 deg about the tool axis) onto the upright nest |  | A | - |  | PASS |  |  |  |
| M20 | Spigot O-ring (2-238) over the mandrel into the spigot groove | gripper | A (holds: B) | PASS | 0.05 | PASS |  |  |  |
| M21 | Heater stack turned over by arm A and handed to arm B, which takes it by the heater block from above |  | A | - |  | PASS |  |  |  |
| M22 | Heater stack into the bore from the top; the rod (on its PEEK bullet) passes down through the two rod O-rings | gripper | B | PASS | 0.03 | PASS | 11.4 | needs 35 N (peak 104); arm can push 161 N | released 39 mm short and pushed home with the closed fingers |
| M23 | Rim wiper onto the plate; plate into the bore onto the bayonet, turned 60 deg (piston at +8 mm overtravel) | gripper | A | PASS | 2.00 | PASS | 0.1 | needs 10 N; arm can push 164 N | released 18 mm short and pushed home with the closed fingers |
| M24 | Module turned upside down again (wrist roll) onto its spigot nest |  | A | - |  | PASS |  |  |  |
| M25 | Rod end with its hermetic connector onto the rod (as drawn: welded to the rod) | gripper | A | FAIL |  | PASS |  |  | sweep: Rod end M50 blocked by Hollow piston rod M50 (5/8 in. x 0.065 in. seamles after 0.0 mm |
| M26 | Striker disc | gripper | A | PASS | 0.30 | PASS |  |  |  |
| M27 | Three M3 x 10 flat-head striker screws | screwdriver | A | PASS |  | PASS | 0.6 | 1.1 N m | 3/3 screws;  |
| C00a | Floor plate (inserts and the two frame dowels already in) onto Fixture P, gland face up, by the vacuum gripper | vacuum | A | PASS |  | PASS |  |  |  |
| C00b | Floor O-ring cord (3.53 mm, vulcanized splice) rolled into the floor plate's pad gland | roller | A (holds: B) | - |  | PASS | 1.1 |  |  |
| C00c | Frame lowered onto the floor plate's dowels, one arm on each side wall |  |  | - |  | PASS |  | 4.3 kg, 2.1 kg per arm | 4.3 kg;  |
| C00d | Eighteen M4 x 16 floor-plate screws up through the U-notches into the frame's skirt, from under the plate's ed | nutrunner_angle | A | PASS |  | PART | 1.2 | 1.1 N m | 3/18 screws; in the: approach: no path in 300 iterations; in the: approach: end pose in collision; in the: approach: no path in 300 iterations (+12 more) |
| C01 | Chamber (frame + floor plate, about 11 kg) turned over by both arms onto Fixture C |  |  | - |  | FAIL |  | 7.39 kg, 3.7 kg per arm | 7.39 kg; arm B: B/forearm hits B/gr/adapter |
| C02 | Locating dowel and diamond pin into the floor | gripper | A | PASS | 0.05 | PASS |  | needs 1644 N; arm can push 175 N | TOO MUCH FORCE for the arm: NO: 16x the F/T range; a UR pushing this hard is past its force limit. Arbor press by a person, or a slip fit (g6) with ;  |
| C03 | Outlet-plenum O-ring (2-044) into the plenum's flange groove, plenum on a nest, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| C04 | Outlet plenum with its O-ring and KF-25 port onto the floor | gripper | A | PASS | 1.68 | PASS |  |  |  |
| C05 | Six M4 x 12 outlet-plenum screws | nutrunner/screwdriver | A | PASS |  | PASS | 2.2 | 2.2 N m | 6/6 screws;  |
| C06 | Overflow-funnel O-ring (2-042) into the funnel block's groove, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| C07 | Overflow funnel block (KF-40 port welded on) onto the floor | gripper | A | PASS | 1.68 | PASS | 11.1 |  |  |
| C08 | Four M4 x 12 overflow-funnel screws | screwdriver | A | PASS |  | PASS | 0.8 | 2.2 N m | 4/4 screws;  |
| C09 | Module-present sensor | gripper | A | PASS | 0.82 | PASS | 0.5 |  | released 18 mm short and pushed home with the closed fingers |
| C10 | Build module (upside down) down into the Ø96 floor port; dowel and diamond pin through its flange lugs | gripper | A | PASS | 0.05 | PASS | 9.5 | needs 109 N (peak 328); arm can push 138 N | peak beyond the arm: robot starts it on the lead-in chamfer (<= 50 N in force mode), the two captive M6 screws pull it home;  |
| C11 | Two captive M6 screws pull the flange onto the floor (they also finish pushing the spigot seal home) | nutrunner_angle | A | PASS |  | FAIL |  | 4.0 N m | 0/2 screws; nge #1: screwdriver: A/upper_arm hits bench top; also no way with nutrunner, nutrunner_angle; nge #2: screwdriver: A/upper_arm hits bench top; also no way with nutrunner, nutrunner_angle |
| C12 | Z stage (flange, actuator, belt fold, servo, carriage, arm, magnet, pre-assembled) onto the floor | gripper | A | PASS | 0.30 | PASS | 0.5 |  |  |
| C13 | Four counterbored M5 x 12 Z-flange screws | nutrunner_angle | A | PASS |  | FAIL |  | 4.2 N m | 0/4 screws; red #1: screwdriver: A/upper_arm hits bench top; also no way with nutrunner, nutrunner_angle; red #2: screwdriver: A/upper_arm hits bench top; also no way with nutrunner, nutrunner_angle; red #3: screwdriver: A/upper_arm hits bench top; also no way |
| C14 | Four legs onto the floor, one at a time | gripper | A | PASS | 0.30 | PASS | 2.1 |  | released 21 mm short and pushed home with the closed fingers |
| C15 | One M6 x 25 down each leg's Ø11 bore (160 mm bit extension) | nutrunner/nutrunner_angle | A | PASS |  | PART | 1.0 | 7.4 N m | 3/4 screws; ore #4: nutrunner: approach: end pose in collision; also no way with nutrunner_angle |
| F01 | Process base plate onto Fixture B (both arms, one at each end) |  |  | - |  | PASS | 0.0 | 11.99 kg, 6.0 kg per arm | 11.99 kg;  |
| F02 | Levelling mounts |  | person | - |  | - |  |  | They thread in when the finished process module goes onto the tray (chapter 5); until then Fixture B carries the plate on its ends. |
| F03 | Optics posts onto the base plate, one at a time, held by arm B while arm A drives their base screws from below | gripper | B | PASS | 0.30 | FAIL |  |  | held-part screws: 316 #5: approach: no clear way in to the hole's mouth (A/upper_arm hits A/gr/camera); held-part screws: 316 #7: approach: no clear way in to the hole's mouth (A/wrist1 hits Base plate, process module (M; 316 #8: approach: no clear way in to t |
| F03h | Optics posts onto the base plate, one at a time, held by arm: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | PASS | 3.0 | 7.4 N m | 2/2 screws;  |
| F03h | Optics posts onto the base plate, one at a time, held by arm: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | PASS | 3.0 | 7.4 N m | 2/2 screws;  |
| F03h | Optics posts onto the base plate, one at a time, held by arm: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | PART | 3.0 | 7.4 N m | 1/2 screws; 316 #5: approach: no clear way in to the hole's mouth (A/upper_arm hits A/gr/camera) |
| F03h | Optics posts onto the base plate, one at a time, held by arm: screws of bridge_base driven while arm B holds i | nutrunner_angle | A (holds: B) | PASS |  | FAIL |  | 7.4 N m | 0/2 screws; 316 #7: approach: no clear way in to the hole's mouth (A/wrist1 hits Base plate, process module (M; 316 #8: approach: no clear way in to the hole's mouth (A/forearm hits Fixture P (floor-plate pedes |
| F04 | Two M6 x 25 up into each post's bottom cap, from under the plate | screwdriver | A | - |  | - |  | 7.4 N m | all screws of this joint were already driven (with the part held) |
| F05 | Chamber assembly (frame, floor plate, module, Z stage, legs; about 17 kg) turned over by both arms holding two |  |  | - |  | FAIL | 48.8 | 15.84 kg, 7.9 kg per arm | 15.84 kg; arm B: B/upper_arm hits B tool stand |
| F06 | Eight M6 x 25 base-plate-to-leg screws, from under the plate | nutrunner_angle | A | PASS |  | FAIL |  | 7.4 N m | 0/8 screws; 316 #1: approach: no clear way in to the hole's mouth (A/upper_arm hits Base plate, process module; 316 #2: approach: no clear way in to the hole's mouth (no IK (out of reach or joint limit)); 316 #3: approach: no clear way in to the hole's mouth ( |
| F07 | Overflow jar in from the right under the floor, up onto its KF-40 port | gripper | B | PASS | 0.30 | PASS | 2.0 |  |  |
| F08 | KF-40 clamp round the jar's flange (wing nut) |  | person | - |  | - |  |  | A hinged KF clamp needs its ring opened round the flange and a wing nut turned; nothing on the 2F-85 or the screwdriver does that. A robot-friendly alternative is a lever (over-centre) KF clamp. |
| F09 | Overflow-jar sensor | gripper | B | PASS | 9.25 | PASS | 4.5 |  |  |
| F10 | Lift-out wall liners into the open chamber | vacuum | A | PASS | 0.06 | PASS | 0.1 |  |  |
| F11 | LED bar | gripper | A | PASS | 0.40 | FAIL | 2.9 |  | arm A: A/gr/left_finger_tip hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) at 15 mm along the insertion |
| F12 | Through-beam fibre heads with their 2-010 O-rings, threaded into the side walls from outside |  | person | - |  | - |  |  | Threading an M6 head with a fibre attached means winding the fibre with it; the ring itself is a pick-and-place. |
| F13 | Inlet-plenum O-ring (2-044) into the plenum's flange groove, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F14 | Inlet plenum with its O-ring and KF-25 port onto the back wall, held there by arm A | gripper | A | PASS | 1.68 | FAIL |  |  | arm A: no IK at the start pose at 0 mm along the insertion; held-part screws: 316 #7: screwdriver: B/tool/screwdriver hits Inlet plenum port (KF-25); also no way with nutrunner |
| F14h | Inlet plenum with its O-ring and KF-25 port onto the back wa: screws of plenum_in driven while arm A holds it | nutrunner_angle/screwdriver | B (holds: A) | PASS |  | PART | 0.8 | 2.2 N m | 6/7 screws; 316 #7: screwdriver: B/tool/screwdriver hits Inlet plenum port (KF-25); also no way with nutrunner |
| F15 | Nine M4 x 16 inlet-plenum screws into the back wall | screwdriver | B | - |  | - |  | 2.2 N m | all screws of this joint were already driven (with the part held) |
| F16 | Vacuum-port adapter (KF-25 stub welded in) with its 2-024 O-ring onto the right wall | gripper | A | PASS | 0.30 | FAIL | 198.3 |  | released 12 mm short and pushed home with the closed fingers; held-part screws: 316 #1: screwdriver: B/upper_arm hits Fixture B (open stand); also no way with nutrunner, nutrunne; 316 #2: screwdriver: B/upper_arm hits Fixture B (o |
| F16h | Vacuum-port adapter (KF-25 stub welded in) with its 2-024 O-: screws of vac_port driven while arm A holds it | nutrunner_angle | B (holds: A) | PASS |  | FAIL |  | 4.2 N m | 0/4 screws; 316 #1: screwdriver: B/upper_arm hits Fixture B (open stand); also no way with nutrunner, nutrunne; 316 #2: screwdriver: B/upper_arm hits Fixture B (open stand); also no way with nutrunner, nutrunne; 316 #3: screwdriver: B/upper_arm hits Fixture B  |
| F17 | Four M5 x 20 vacuum-port screws | screwdriver | A | - |  | - |  | 4.2 N m | all screws of this joint were already driven (with the part held) |
| F18 | Recoater guide rail onto the back wall | gripper | A | PASS | 2.50 | FAIL |  |  | arm A: A/gr/left_finger_tip hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) (3.0 mm deep) at 168 mm along the insertion |
| F18h | Recoater guide rail onto the back wall: screws of rail driven while arm A holds it | nutrunner_angle | B (holds: A) | PASS |  | PASS | 1.9 | 2.2 N m | 4/4 screws;  |
| F19 | Five M4 x 16 rail screws, driven from inside the chamber toward the back wall | screwdriver | A | - |  | - |  | 2.2 N m | all screws of this joint were already driven (with the part held) |
| F20 | Carriage onto the rail from its end | gripper | A | FAIL | 0.30 | FAIL | 0.5 |  | sweep: Recoater carriage blocked by Process chamber body (6061-T6 through-frame from 5 after 182.0 mm; arm A: held:F20:Recoater carriage hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) at 10 |
| F21 | Ball screw through the side-wall bores and the ball nut (turned through the nut: 30 turns at 10 mm lead) | gripper | A | FAIL | 0.30 | FAIL | 0.0 |  | sweep: Recoater ball screw blocked by Process chamber body (6061-T6 through-frame from 5 after 214.0 mm; arm A: held:F21:Recoater ball screw hits Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor plate bolted under it) a |
| F22 | Feedthrough spacer, its two 2-024 O-rings, the Ferrotec unit and the coupling on the left wall | gripper | A | PASS | 0.30 | FAIL | 1.7 |  | arm A: A/gr/left_finger hits Optics bridge posts #2 at 60 mm along the insertion |
| F23 | Blind bearing cap and its 2-019 O-ring on the right wall | gripper | A | PASS | 0.30 | FAIL | 0.9 |  | arm A: A/gr/left_finger hits Optics bridge posts #4 at 111 mm along the insertion; held-part screws: 316 #1: screwdriver: screw:Bearing-cap screws, M4 x 20 31 hits A/wrist2; also no way with nutrunne; 316 #2: screwdriver: screw:Bearing-cap screws, M4  |
| F23h | Blind bearing cap and its 2-019 O-ring on the right wall: screws of bearing_cap driven while arm A holds it | nutrunner_angle | B (holds: A) | PASS |  | FAIL |  | 2.2 N m | 0/4 screws; 316 #1: screwdriver: screw:Bearing-cap screws, M4 x 20 31 hits A/wrist2; also no way with nutrunne; 316 #2: screwdriver: screw:Bearing-cap screws, M4 x 20 31 hits A/wrist2; also no way with nutrunne; 316 #3: screwdriver: screw:Bearing-cap screws, M |
| F24 | Four M4 x 20 bearing-cap screws | screwdriver | A | - |  | - |  | 2.2 N m | all screws of this joint were already driven (with the part held) |
| F25 | Motor standoff, bracket and recoater servo | gripper | A | PASS | 0.05 | FAIL | 0.0 |  | arm A: A/gr/left_finger_tip hits Optics bridge posts #2 at 108 mm along the insertion; arm A: approach: no path in 800 iterations; released 9 mm short and pushed home with the closed fingers; arm A: approach: no path in 800 iterations; released 15 mm short and |
| F26 | Blade holder and blade | gripper | A | FAIL |  | FAIL | 22.7 |  | sweep: Blade holder blocked by Recoater carriage block (6061) after 0.0 mm; arm A: held:F26:Blade holder hits Recoater carriage block (6061) (3.0 mm deep) at 129 mm along the insertion |
| F27 | Two M3 x 8 blade screws | nutrunner_angle | A | PASS |  | FAIL |  | 1.1 N m | 0/2 screws; 316 #1: screwdriver: A/upper_arm hits A cabinet; also no way with nutrunner_angle; 316 #2: screwdriver: A/upper_arm hits A cabinet; also no way with nutrunner_angle |
| F28 | Gas knife and dose chute | gripper | A | PASS | 3.00 | PASS | 3.0 |  |  |
| F29 | Lid O-ring cord (3.53 mm) rolled into the body's top gland: arm A rolls, arm B feeds the cord | roller | A (holds: B) | - |  | PASS | 1.0 |  |  |
| F30 | Lid (inserts in) onto the cord, by the vacuum gripper | vacuum | A | PASS | 0.30 | PASS | 26.2 |  |  |
| F31 | Twenty M5 x 25 lid screws, star pattern | screwdriver | A | PASS |  | PASS | 2.6 | 4.2 N m | 20/20 screws;  |
| F32 | Window-flange O-ring (2-036) into the flange's lower groove, PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F33 | Field stop, then the window flange with its O-ring | gripper | A | PASS | 0.10 | FAIL | 0.1 |  | released 27 mm short and pushed home with the closed fingers; arm A: part 100 mm across at the grasp: wider than the 2F-85's 85 mm stroke |
| F34 | Six counterbored M4 x 16 window-flange screws (torque-controlled) | screwdriver | A | PASS |  | PASS | 2.2 | 2.2 N m | 6/6 screws;  |
| F35 | Window O-ring (2-031) into the flange's seat groove | gripper+caps | B | PASS | 1.15 | PASS |  |  |  |
| F36 | Ø2 in. fused-silica window onto its O-ring | gripper | A | PASS | 0.20 | PASS |  |  | released 27 mm short and pushed home with the closed fingers |
| F37 | FKM flat ring and the retaining ring | gripper | A | PASS | 0.20 | FAIL | 0.3 |  | released 24 mm short and pushed home with the closed fingers; arm A: part 100 mm across at the grasp: wider than the 2F-85's 85 mm stroke |
| F38 | Six M3 x 10 retaining-ring screws (torque-controlled: clamp the silica evenly) | screwdriver | A | PASS |  | PASS | 1.5 | 0.8 N m | 6/6 screws;  |
| F39 | Cover-slide drawer (2-033 in its half-dovetail, put in on the bench) into the lid's front edge | gripper | A | PASS | 0.30 | PASS |  | needs 50 N (peak 358); arm can push 1500 N | released 6 mm short and pushed home with the closed fingers |
| F40 | Quarter-turn drawer latches |  | robot (custom bit) | - |  | - |  |  | Two quarter-turn studs, turned with a slotted bit on the screwdriver; the latch hardware is an envelope in the model (seals.md: no catalogue latch fits). |
| F41 | Drawer-closed sensor | gripper | A | PASS | 1.32 | PASS | 1.0 |  | released 18 mm short and pushed home with the closed fingers |
| F42 | Metering-base O-ring (2-040) on its lid side (groove faces down when fitted: PFPE film) | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F42b | Metering-base dock-face O-ring (2-040), groove up | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F43 | Metering base alone (feedthrough, coupling and stepper not yet on) onto the lid | gripper | A | FAIL |  | FAIL |  |  | sweep: Metering base blocked by Metering-base dock-face O-ring (FKM 75A 2-040, sea after 0.0 mm; arm A: held:F43:Metering base hits Metering-base dock-face O-ring (FKM 75A 2-040, seals the reservoir's base plate) (3.0 mm deep); pushed home instead, but held:F4 |
| F44 | Four M4 x 16 metering-base screws (before the roller feedthrough covers two of them) | nutrunner | A | PASS |  | PASS | 0.0 | 2.2 N m | 4/4 screws;  |
| F45 | Roller feedthrough (threaded M8 x 1 over its 2-012), coupling, stepper, dock rails, load cell, NFC, side port, | gripper | A | FAIL | 0.30 | FAIL | 0.2 |  | sweep: Roller shaft blocked by Metering base (6061, fluted roller over a 100 mm d after 0.0 mm; arm A: no IK at the start pose at 0 mm along the insertion; sweep: Roller feedthrough O-ring blocked by Metering base (6061, fluted roller over a 100 mm d after 0.0 |
| F46 | Reservoir M slid onto the dovetail dock (about 94 N to seat on the dock O-ring) | gripper | A | PASS | 1.10 | PASS |  | needs 94 N; arm can push 191 N |  |
| F47 | Camera adapter O-ring (2-022), PFPE film | gripper+caps | B | PASS | 1.68 | - |  |  |  |
| F48 | Camera viewport adapter, window O-ring, window, flat ring, retaining ring, camera | gripper | A | FAIL | 0.04 | FAIL | 1.6 |  | sweep: Camera window blocked by Camera viewport adapter + boss (6061; Ø1 in. windo after 0.0 mm; released 33 mm short and pushed home with the closed fingers; sweep: Camera window O-ring blocked by Camera viewport adapter + boss (6061; Ø1 in. windo after 0.0 m |
| F49 | Pressure transducer and relief valve (SAE-4 O-ring-boss ports) |  | person | - |  | - |  |  | Threaded ports need a wrench on a hex and a set torque; a 2F-85 can only spin a plain body. |
| F50 | Hinge knuckles on the chamber and the two draw latches | gripper | A | FAIL | 0.30 | FAIL | 1.0 |  | released 9 mm short and pushed home with the closed fingers; sweep: Draw latches on the chamber's side faces blocked by Optics bridge posts #3 after 16.0 mm; arm A: held:F50:Draw latches on the chamber's  hits Optics bridge posts #3 at 87 mm along the insertio |
| F51 | Door (cord rolled into its half-dovetail on the bench) brought in, knuckles in line | gripper | A | PASS | 0.01 | PASS | 0.0 | needs 725 N |  |
| F52 | Hinge pins slid in along x | gripper | A | PASS | 0.10 | FAIL |  |  | arm A: A/upper_arm hits Fixture B (open stand) at 0 mm along the insertion |
| F53 | f-theta lens threaded into its adapter ring under the bridge (on the bench, bridge upside down) |  | person | - |  | - |  |  | The Ø90 lens is wider than the 2F-85's 85 mm stroke and threads M85 x 1; a strap wrench by hand (operations.md: lens and ring fitted to the bridge on the bench). |
| F54 | Optics bridge (13.3 kg, lens and ring under it) onto the four posts, one arm at each end |  |  | - |  | FAIL |  | 14.28 kg, 7.1 kg per arm | 14.28 kg; no collision-free pair of arm poses at the start of the carry |
| F55 | Eight M6 x 35 bridge screws down into the posts | nutrunner | A | PASS |  | PASS | 3.0 | 7.4 N m | 8/8 screws;  |
| F56 | Galvo riser and the basiCube 20 scan head on the bridge | gripper | A | PASS | 0.30 | FAIL |  |  | arm A: part 130 mm across at the grasp: wider than the 2F-85's 85 mm stroke; arm A: part 130 mm across at the grasp: wider than the 2F-85's 85 mm stroke |
| F57 | Beam tube, shutter and collimator | gripper | A | PASS | 0.00 | FAIL |  |  | arm A: no IK at the start pose at 0 mm along the insertion; arm A: no IK at the start pose at 0 mm along the insertion; arm A: no IK at the start pose at 0 mm along the insertion |
| F58 | Process fiber routed to the collimator |  | person | - |  | - |  |  | Armoured fiber, >= 100 mm bend radius: cable routing stays manual. |
| F59 | Class 1 laser guard: T-slot frame, panels, door rail, sliding door, guard lock, operator panel |  | person | - |  | - |  |  | T-slot nuts and 1.5 mm panels up to 730 mm wide; its hardware is not drawn (joints.NOT_DRAWN). |
| T01 | Process module (84 kg) off Fixture B onto the VLM tray; levelling mounts threaded in |  | person + hoist | - |  | - |  |  | 84 kg is 3.4 times two UR12e payloads; a hoist or lift table. |
| T02 | 19 in. rack and its units (UPS 23 kg, laser 40 kg, PC 8 kg, DIN drawer 9 kg) |  | person + lift | - |  | - |  |  | the UPS and the laser exceed a UR12e's 12.5 kg; cage nuts and screws are not drawn |
| T03 | Gas module: base plate, scroll pump (26 kg), blower, filter housing, O2 box, argon manifold |  | person + lift | - |  | - |  |  | the pump exceeds 12.5 kg; the units' screws are not drawn |
| T04 | KF-25 bellows, vacuum valve, argon and O2 lines |  | person | - |  | - |  |  | hose and tube routing (deformable, KF wing-nut clamps) |
| T05 | Tray dock and umbilicals |  | person | - |  | - |  |  | cable and hose routing |
| T06 | Leak check: rate of rise from <= 1 mbar, O2 drift at +20 mbar argon |  | machine | - |  | - |  |  | the seal verification in assembly.md |

## Seals: every O-ring and cord

Every gland comes from `lpbf_low.GLANDS` after `build()`, plus the lid cord. `seals_forces.py` computes the numbers and writes them to [`out/assembly/seals_forces.json`](analysis/out/assembly/seals_forces.json).

| Gland | Ring | Installed stretch | Most stretch while fitting | How the cell fits it | Lead-in it needs |
|---|---|---|---|---|---|
| lid | 3.53 mm cord (vulcanized splice) | cord (no stretch); a moulded 2-278 would be +0.29 % (-0.25 to +0.83 % over tolerance) | corners R4.3: 29 % bending strain (Parker: R >= 10.6, about 14 %) | cord laid in by arm B at the midpoints, ends, quarter points (Adebola et al. 2024), rolled home by arm A's 3.2 mm PTFE wheel at 10-20 N; the splice at a straight run | none (axial face seal) |
| spigot | 2-238 | +2.3 % | +9.3 % | stretched over the acetal spigot mandrel (cone + 0.45 mm sleeve) and pushed off into the groove by the pusher | floor port's lower edge: >= 3.5 mm at 15 deg or 2.5 mm at 20 deg (the ring enters the port from below); the spigot's top edge is covered by the mandrel's sleeve |
| gland_plate_M50 | 2-034 | +1.5 % | +3.4 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| rod_M50 x 2 | 2-114 | +2.2 % on the rod; OD -3.8 % in the groove | folded: ~34 % bending strain at a 2.5 mm fold | folded into the slotted loader tube (kidney fold), pushed through the Ø15.93 throat and released into the groove, the deeper groove first; then the rod enters on the PEEK bullet | rod end: the bullet's 15 deg nose (>= 3.0 mm at 15 deg); the throat's edges rounded R0.2-0.4 and polished |
| hermetic_M50 | 2-014 | +1.4 % | +9.5 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| overflow_funnel | 2-042 | +2.0 % | +3.2 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| floor | 3.53 mm cord (vulcanized splice) | cord (no stretch); a moulded 2-277 would be +1.73 % (+1.16 to +2.31 % over tolerance) | corners R11.5: 13 % bending strain (Parker: R >= 10.6, about 13 %) | floor plate face up on Fixture P: cord laid in by arm B, rolled home by arm A's 3.2 mm wheel; nothing above the plate yet, so the roller has the whole gland to itself | none (axial face seal) |
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
| camera_adapter | 2-022 | +2.7 % | +6.7 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
| camera_window | 2-017 | +2.5 % | +8.3 % | 2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed | none (axial face seal) |
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
  - **Raw push:** limited by the joint torques. At the force steps' own poses, [`push.json`](analysis/out/assembly/push.json) gives the largest static push along the insertion before a joint reaches its limit, C02 (arm A): 175 N; C10 (arm A): 138 N; F39 (arm A): 1500 N; F46 (arm A): 191 N; M22 (arm B): 161 N; M23 (arm A): 164 N; F30 (arm A): 113 N. Those figures load each link's mass only on the joints upstream of it, as the corrected `cell.max_force` and `shop_checks.joint_torques` do.
  - **What limits it:**
    - A downward push at these poses tops out at 113-191 N before a joint reaches its torque limit. Holding the pose alone uses 31-48 % of the most-loaded joint.
    - Horizontally (the drawer) it is 1.5 kN.
  - **So:**
    - The reservoir's 94 N, the rod's 35 N running and the plate's 10 N search are all within both the motors and the sensor.
    - The spigot's 328 N break-out is not: 138 N is available at C10.
    - Nor is the dowels' 1.6 kN: 175 N is available.
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

1. **Rod end: clamp it, don't weld it** (`cad/modules_low.py` / `cad/lpbf_low.py` rod-end part; `cad/joints.py` new joint `rod_end_M50`).
   - **Why:** step M25 fails, and the sweep shows it: the welded cap is part of the rod. At assembly the rod has to pass down through the gland plate's two 2-114 rings, so the cap can only go on afterwards, and welding 10 mm from FKM is not an option. In service the same weld traps the gland plate (operations.md M7.2).
   - **Change:**
     - make the cap a sleeve on the plain Ø15.875 rod: bore Ø15.90 H8 × 20 deep;
     - one Parker rod groove Ø20.0 × 3.6 inside it for a third 2-114, sealing on the rod's OD;
     - two M4 × 6 cup-point set screws at 90° and 270°, the same detail as the piston head's socket;
     - the hermetic connector's boss unchanged.
   - The cell then fits the cap from above with the module upside down (M24-M27). The cap's 2-114 goes in with the same loader.
2. **Lead-in chamfer on the floor port's underside edge** (`cad/lpbf_low.py`, floor plate).
   - **Change:** 20° × 2.5 mm on the Ø96 port's lower edge, polished R0.2. That is Trelleborg Table 16's minimum for a 3.53 mm ring; 15° × 3.5 mm also does.
   - **Why:** the module's 2-238 enters the port from below, and a sharp edge there shaves it.
   - The port's top edge, flush with the powder floor, stays sharp. The ring never passes it.
3. **Lid gland corners to R ≥ 10.6 mm, and moulded rings in both cord glands** (`cad/lpbf_low.py`: the lid O-ring and its gland cut, `rbox(..., 4.3)`; `GLANDS["floor"]`).
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
5. **Rod gland: open grooves instead of a throat** (`cad/modules_low.py`, gland plate). This is optional, but it removes the riskiest seal step (M18).
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

**Changes to this note's own files, for the next run** (not re-run here):

- `sequence.py`:
  - **The optics posts (F03-F04).** Fit them after the side-wall work (F22-F27). They block A's fingers there and the right draw latch's way in.
  - **The recoater (rail, carriage, ball screw, blade holder).** Fit it from below through the frame's open bottom before the floor plate goes on (C00). The new through-frame allows that, and the closed chamber blocks both documented paths (F20, F21, F26).
  - **The window flange, its retaining ring and the galvo.** Fit them with the VGC10, not the 2F-85.
  - **The Macor rings and disc springs.** Fit them with the small vacuum nozzle (tooling C12).
- `cell2.py` / `tooling.py`:
  - **Fixture B.** Move its end frames 200 mm further out, or carry the base plate on its front and back edges.
  - **Fixture C.** Raise it 300 mm (C11, C13).
  - **Tool stands.** Mount them lower, at the cabinets' outer side (F05).
  - **The first turn-over.** Grasp the frame on the turn axis (C01): bolt two temporary handles to the side faces' latch holes.
  - **Upward screws.** Teach one via-point under each plate (C00d, F06).
