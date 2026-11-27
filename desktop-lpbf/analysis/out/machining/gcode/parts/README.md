# Posted programs for chapter 31's parts (robot-build round 9)

Sterling on round 7's video: "dummy tool paths instead of real ones". Round 8 gave chapter 30 (the chamber frame and floor
plate) its eight posted FreeCAD programs. Chapter 31 still had no program for its other parts: "the vise bracket has no
posted program, so its invented path is gone and only the clock runs". This folder holds the bracket's programs, and the new
chapter 31b plays them the way chapter 30 plays the chamber's.

## The parts chapter 31 shows

| Clip ([`shop_clips.py`](../../../../shop/shop_clips.py)) | Part | Finished geometry (model) | Stock (shop plan) | Program |
|---|---|---|---|---|
| `vf4_vise_part`: arm A sets a blank in the Kurt XL6A air vise on the VF-4 | Recoater motor bracket | [`cad/lpbf_low.py`](../../../../../cad/lpbf_low.py): a 90 x 60 x 170.4 mm block of 6061 under the recoater servo; dfm.json 920.2 cm3, 6 faces, no holes | 2.5 in. 6061 plate, 96 x 176 mm ([`setup_plan.json`](../../setup_plan.json)); 2 setups, +z and -z | `bracket_op1.ngc`, `bracket_op2.ngc` |
| `lathe_slug`: arm A loads a 2-1/8 in. bar slug into the ST-10 | the slug (54 x 100) | the turned profile chapter 31 draws is illustrative | 2-1/8 in. 6061 bar | none: FreeCAD 1.0.2's CAM workbench has no turning operations (its ops: Adaptive, Custom, Deburr, Drilling, Engrave, Helix, MillFace, Pocket, PocketShape, Probe, Profile, Slot, Surface, ThreadMilling, Vcarve, Waterline) |

The model draws the bracket as a plain block: [`joints.py`](../../../../../cad/joints.py) lists its screws as "M4 per the
vendor hole patterns; not drawn", so no holes are programmed. Its programs face it and cut its outline.

## The programs

Made by [`analysis/machining/parts_cam.py`](../../../../machining/parts_cam.py) in FreeCAD 1.0.2's CAM workbench, headless
(the official conda AppImage, sha256 `e00be00a...904f61` checked against the release's SHA256 file, as
[`freecad_cam.py`](../../../../machining/freecad_cam.py) runs it), posted with FreeCAD's `linuxcnc` post. CAM frame: the
block lying flat as op 1 holds it, 90 mm along X (across the jaws), 170.4 along Y, 60 along Z, origin at the centre of its
bottom face; the blank 96 x 176 x 63.5, z -1.75 to 61.75. Tools: the chamber's own T1 and T2 (`freecad_cam.TOOLS`), so the
VF-4 in the video carries the same tools.

| Program | Workholding | Operations (tool, feed) | Minutes (recount) | FreeCAD's estimate |
|---|---|---|---|---|
| `bracket_op1.ngc` | Kurt XL6A on the 96 mm faces, the blank on a 1 in. parallel (19 mm in the 1.75 in. jaws) | face the top to z 60 (T1 2.5 in. face mill, 3000 rpm, 1219 mm/min); outline 90 x 170.4 from z 60 to 21, rough with 0.3 mm left, then finish, two 19.5 mm steps each (T2 3/4 in. 3-flute carbide, A5, 5100 rpm, 1943 mm/min) | 1.85 | 2.32 |
| `bracket_op2.ngc` | turned over about X, gripped on the finished 90 mm faces | face the bottom to 60 thick (T1); outline from the bottom up to z 21.5, 0.5 mm over op 1's, rough and finish, one 21.5 mm step (T2) | 1.21 | 1.42 |

Op 1's outline stops 3.7 mm above the jaws' top; op 2's stops 19.5 mm above them. Per operation, FreeCAD's CycleTime and the
recount are in [`parts_cam.json`](parts_cam.json). Simplifications, as in the chamber's programs: no lead-in or lead-out
dressups (the face mill comes down 1.75 mm at its first point and the outline plunges at its start, in the 3 mm of stock
round the part; a shop would ramp in or start off the blank), no chamfers or deburring, tool changes counted, not timed.

## The simulation check

[`parts_sim.json`](parts_sim.json) (`parts_cam.py --sim`): each program parsed and timed with
[`gcode_sim.py`](../../../../../cad/robotbuild/gcode_sim.py)'s parser and timing, and cut with its `Cutter` (flat-ended
cylinders swept along every move) on a 0.5 mm voxel grid, op 1 then op 2 on what op 1 left.

| | op 1 | op 2 | both |
|---|---|---|---|
| simulated minutes (feeds as programmed, rapids 25.4 m/min) | 1.86 | 1.23 | 3.09 |
| recount of the posted G-code (`freecad_cam.gcode_times`) | 1.85 | 1.21 | 3.06 |
| FreeCAD's own estimate (sum of op CycleTimes) | 2.32 | 1.42 | 3.74 |
| removed (cm3) | 94.3 | 57.9 | 152.2 |

Blank minus part: 152.7 cm3 exactly, 152.2 cm3 on the voxel grid; the simulation removed 152.2 cm3 (+0.02 %). Nothing is
left more than 1 mm outside the part, and nothing is cut more than 1 mm inside it (0.03 cm3 of voxel steps at the walls).

## Chapter 31b

[`cad/robotbuild/ch_programs.py`](../../../../../cad/robotbuild/ch_programs.py) renders
`/tmp/robotbuild/frames/31b-machining-programs/` under chapter 31's title ("Machining the other parts: vise, lathe, saw"),
so the YouTube chapter list gains no entry. The blank in the vise (98 mm opening; the jaw plates stand 1 mm proud of the
jaws) on its parallel; op 1 at 3.7x real time, then a cut to op 2 (the vise at 92 mm on the finished faces; turning the
part over is not planned for the arms, so it is not drawn), then the finished part. Every cutting frame puts the cutter where
the program is at that frame's time (the table carrying the part in X and Y, the head in Z, `shop_chapters.vf4_for`), the
stock as the program has cut it so far (`gcode_sim.Cutter`, 0.75 mm voxels), the last ~0.2 m of path, and the program and
line in the frame's sub; the camera rides on the table, as in chapter 30's cutting shots. Every drawn position is in
[`parts_frames.json`](parts_frames.json), re-checked at the end of the render against the re-parsed program.

## Checks (2026-11-27)

* **Frames:** 736 at 12 fps (61.3 s): 3 s of the blank in the vise, op 1 (30 s at 3.7x), Z home, a cut, 3 s of op 2's
  setup, op 2 (20 s at 3.7x), Z home, 4 s of the finished part. All 600 cutting frames put the cutter on the program line
  their frame names (re-parsed: worst 0.00005 mm off), every one inside the VF-4's travels
  ([`parts_frames.json`](parts_frames.json)). The clocks: 3.1 min of machine time, the programs' own minutes.
* **Collision audit** ([`scene_audit.py`](../../../../../cad/robotbuild/scene_audit.py) `run 31b-machining-programs`, every
  recorded frame; [`scene_audit_31b-machining-programs.json`](../../../videoqa/scene_audit_31b-machining-programs.json)):
  736 of 736 frames checked, 25 movers against 94 actors: 0 pairs deeper than 1.5 mm (worst 0.0 mm). Six pairs are
  the VF-4 model's own pieces, rigid over the chapter and not counted (the table's, the head's, and each vise's jaw plates
  in their jaws). No allowed contact was needed for the cutter in the stock: as in chapter 30, the stock is cut up to
  the cutter's position before the frame is drawn, so the cutter stands in the space it has cut (the 0.75 mm voxels
  leave it well under 1.5 mm). The first render rebuilt the vise's meshes for op 2, which turned its jaw plates into
  five moving pairs; the vise is now one group per opening, built once.
* **Camera** ([`video_qa.py`](../../../../../cad/robotbuild/video_qa.py) on a compose of this chapter alone;
  [`camera-round9-31b.json`](../../../videoqa/camera-round9-31b.json)): 0 jumps a minute, one steady run of 61.3 s, 0 % of
  runs under 2 s, a 95th-percentile camera speed of 0.006 frame widths a second: pass. The cut between the programs keeps
  the same view of the part, so the check does not see it as a jump.

Still: [`cad/img/robotbuild/round9/r9-31b-bracket_op1-ngc-outline.png`](../../../../../cad/img/robotbuild/round9/r9-31b-bracket_op1-ngc-outline.png).

## Not done

* The slug's turning program (FreeCAD 1.0.2 has no turning operations); chapter 31's turned profile stays illustrative.
* The bracket's screw holes: the model doesn't draw them, so they are not programmed.
* Chapter 31's vise clip loads a 72 x 150 x 63.5 blank (a "typical" one: its 2F-85 grips 72 mm across, and 96 mm is past
  its 85 mm stroke). That blank can't hold the 90 x 170.4 part; chapter 31b draws the shop plan's 96 x 176 blank.
* `compose.py` takes extra chapter folders matching `\d\d-[a-z0-9-]+`, which `31b-machining-programs` doesn't match; the
  check above composed it with that one pattern widened to `\d\d[a-z]?-[a-z0-9-]+` for the run. The folder sorts after
  `31-machining-parts` and before `32-finishing`.
