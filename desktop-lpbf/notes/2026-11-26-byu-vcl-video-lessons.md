# What Sterling's byu-vcl pings teach about workflow videos (read 2026-11-26)

On 2026-11-26 Sterling rejected the round-7 robot-build video ("moonwalk, motion sickness, collisions and interference, dummy
tool paths instead of real ones") and pointed at his byu-vcl pings, "that helped improve the vertical lab workflows over time".
This is what those pings say, read through the GitHub API: all of his comments on
[byu-vcl PR 318](https://github.com/vertical-cloud-lab/byu-vcl/pull/318) (100 comments), issue 303, 28 companion threads and
the earlier PR 255, at head `859d767`. Every quote below was checked against the comment it links to.

None of the four words he used here ("moonwalk", "motion sickness", "dummy", "tool path") appears in any of those comments, so the
mapping from his byu-vcl feedback to this video's faults is ours.

## The lessons, and what byu-vcl did about each

| # | What he said there | What worked there | What it means for this video |
|---|---|---|---|
| 1 | "couldn't you use something like mujocu (sp?) to simulate this?" ([11-04](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6622599733)); "the robot arm didn't respect collisions with itself, at all. Passed through the MiR250" ([11-04](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6623032979)); "probably other collisions and interferences that I didn't catch" ([11-13](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6867635611)) | An audit of every drawn frame, for everything that moves, with a depth threshold (1.5 mm) and a short list of allowed contacts. An earlier audit that checked only the arms reported zero and was wrong. | The planner's checks cover only the arm paths it planned. The frames also draw people, bases, loads, failed attempts and unplanned moves. Audit what is drawn, and don't animate what wasn't checked. |
| 2 | (Raised by the bot's own review and followed through at his request.) The reply: "Chapter 3's MiR used to slide 148 mm sideways ..., which a differential-drive MiR250 can't do." ([11-04](https://github.com/vertical-cloud-lab/byu-vcl/issues/321#issuecomment-6624719055)) | Bases move as the real robot does: trapezoid at 0.3 m/s², heading on the path, pivot, drive, pivot; a reverse only as a short docking leg. | Our MiRs slid back and forth along their lanes, in reverse half the time. People glided the same way. |
| 3 | "You're probably going to need both mobile robots (i.e., both arms) to be able to do the chamber opening" ([11-05](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6671706461)); "the two arms working together to adjust the position of the plate in real-time" and "holding the lid down while working the latch seems unnecessary?" ([11-20](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-7046840630)) | The second arm got a mechanical job (hold a nut with a keyed tool while the first arm turns; one knob each). A hold with no mechanical reason was removed, with the reason stated. | Use the second arm where a part would move, tip or spring back, and put the number behind it. No decorative holds. |
| 4 | "The robot arm should actually do something.. not just move side to side. Demonstrate an actual workflow" ([10-27](https://github.com/vertical-cloud-lab/byu-vcl/issues/303#issuecomment-6450405539)); "non-physical self-motion", "just floating over" ([11-05](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6646276541)) | Every approach, grasp and retreat is a checked straight line; machining is drawn operation by operation with the stock re-cut; on-screen data is badged real, computed or illustrative. | The cutter must follow the real G-code over a workpiece computed from it. byu-vcl has no G-code-level simulation, so this goes further than it did. |
| 5 | "you should have started backed off to see the full overview and then zoomed in" ([11-06](https://github.com/vertical-cloud-lab/byu-vcl/issues/329#issuecomment-6698086804)); "pull back to a birds-eye view" as speed rises ([11-25](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-7153165197)); "The angle and transparency at 32:20 is off. Can't see the tensile test happening" ([11-05](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6671706461)) | Fixed named views; eased moves with holds; a cut where a move would pass through geometry; the overview first, then the working view. | Our assembly chapters picked a new view for nearly every motion. Fixed cameras, long holds, cuts instead of whip pans. |
| 6 | "max 4-6 words at a time, and not transition the words more than every 3-5 seconds" ([10-04](https://github.com/vertical-cloud-lab/byu-vcl/issues/255#issuecomment-5976518231)) | Short captions that stay put; time-lapses labelled ("shown at 4×"). | Short main caption, held at least 3 s; numbers in the second line. |
| 7 | "They would just fall off" ([11-04](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6638658450)) | Grasps that visibly hold: pockets with lead-ins, a catch ring, a grip block. | A held part must be held by something drawn. |
| 8 | "cringy looking human" ([11-13](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6867635611)); "Elastigirl / Mr. Fantastic powers" ([10-03](https://github.com/vertical-cloud-lab/byu-vcl/issues/255#issuecomment-5966425543)) | A skinned figure whose gait phase follows the distance walked (one cycle per 1.016 m), the lowest shoe on the floor each frame, arms within their real reach. | People walk in steps and step closer instead of stretching or sliding. |
| 9 | "accuracy, thoroughness, lack of collisions, rendering fidelity" ([11-20](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-7030074368)); "simulate as realistically as possible" ([11-07](https://github.com/vertical-cloud-lab/byu-vcl/issues/318#issuecomment-6701736396)) | Audits run before the render, a contact sheet looked at before a full render. | Each fault gets an automated check, and the render is looked at before it is posted. |

## The checks this turned into (round 8)

| Fault | Check | Where |
|---|---|---|
| Motion sickness | jumps per minute, steady-run length and camera speed, measured on the finished MP4's pixels (the 7-second panning rule) | [`cad/robotbuild/video_qa.py`](../cad/robotbuild/video_qa.py) |
| Motion sickness, assembly chapters | shot length, cuts per minute and camera motion from each frame's recorded camera | `cad/robotbuild/camera_rig.py` |
| Moonwalk, people | stance-foot slip and gliding frames | `cad/robotbuild/walk.py` |
| Moonwalk, bases | sideways slip, reversing distance, footprint clearance | `cad/robotbuild/scene_audit.py` |
| Collisions and interference | every drawn frame, pairs deeper than 1.5 mm that aren't allowed contacts | `cad/robotbuild/scene_audit.py` |
| Dummy tool paths | every drawn cutter position is a line of a posted program; minutes and removed volume against the CAM's own numbers | `cad/robotbuild/gcode_sim.py` |
| One-armed work | steps with both arms working, holds used, not needed, or not possible, each with its reason | `analysis/assembly/two_hands.py` |

Results are under [`analysis/out/videoqa/`](../analysis/out/videoqa/); [`robot-build/video.md`](../robot-build/video.md) says which of
these exist and what they found.
