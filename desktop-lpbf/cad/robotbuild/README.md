# The desktop LPBF built by two mobile manipulators: the video's contract (round 7, 2026-11-25)

Sterling asked on 2026-11-25 for the build to be shown being done **by** two UR12e arms, each on a MiR250: unpacking,
every machining step, the seals, the screws and the tightening, with a person only where one is really needed, the
full set of parts spread across a really long table, running cost (new against used), lead times, and time estimates.

Several renderers draw chapters in parallel and write raw 3-D frames plus per-frame metadata; `compose.py` draws the
on-screen panels and joins everything into one MP4. [`common.py`](common.py) holds the shared frames, sizes, colours,
the plotter and the frame writer; read its docstring first.

## Chapters

| Chapter folder | Owner | What it shows |
|---|---|---|
| `00-intro` | video | the hall from above: the long table, the shop, the assembly bench, both MiRs, a person for scale |
| `10-parts` | video | the camera runs along the long table, category by category; the cost panel adds each category (new and used) and calls out the expensive items one by one; the lead-time panel shows each order's lead time, new against used |
| `20-receiving` | shop | boxes arrive; a person with a pallet jack moves the heavy crates; the arms cut the tape and unpack onto the table and the stock rack |
| `30-machining-chamber` | shop | the chamber frame and floor plate: the person loads the 34.7 kg blank with a vacuum lifter; the arms tend the VF-4 and HRT210 through every setup, flip and re-clamp the part; a machine clock runs |
| `31-machining-parts` | shop | the other machined parts: lathe (top-down loading), vise parts, the saw; time-lapse with the clock |
| `32-finishing` | shop | TIG welding by a person, honing sent out, deburr, wash, measuring (a person reads the bore gauge), kitting back onto the table |
| `38-tools` | assembly | the custom tools and fixtures the arms use (tooling.py's meshes, the same ones the planner checks), one at a time on a turntable, with what each is for and its cost ([`ch_tools.py`](ch_tools.py)) |
| `40-assembly-module` | assembly | the build module, every step by the two arms with their tools, parts fetched from the long table |
| `41-assembly-chamber` | assembly | the chamber and the process module, the same way; failed steps shown with their redesign or the person who does them |
| `50-integration` | video | the process module onto the VLM tray (person and hoist), the rack units, hoses, the leak check |
| `60-summary` | video | time and cost: in-house, outsourced and the robot shop; what had to be redesigned; where a person is needed |

## Rules for every renderer

- 1280 x 720 frames from `common.plotter()`, written with `common.Chapter`. Draw the 3-D only: no text in the frame
  (the compositor adds it), except labels that belong to an object, which go in `labels`.
- Every robot motion shown comes from a collision-checked plan (cell.py's FCL checks, RRT-Connect, PR 318's 1.5 mm
  audit). Where a step fails, show the failure honestly (`status: "fail"`) and then the redesign or the person.
- `proc_s` is real-world time: real time for robot motions (1/12 s a frame), time-lapse for machining (say how much in
  `sub`). The compositor adds the counters up across chapters.
- Memory: run every renderer and planner under `/tmp/capmem <limit> ...`; limits are in the worker briefs. The runner
  has 4 cores and 15 GB, and three earlier sessions on this branch were lost to running out of memory.
- Never commit frames (`/tmp/robotbuild/frames`) or trajectory pickles (`/tmp/robotbuild/traj`); commit scripts,
  summaries (JSON/MD/CSV) and a few stills.

## Rendering the long assembly chapters in slices

`asm_render.py` plays a chapter twice: pass 1 without drawing (where the work is in every frame, the tripods' occlusion once
per step, then the shot plan), pass 2 draws. A slice draws only its frames, into `<chapter>.part<k>/`: `ASM_PART=k/n` (by the
planned frame count), `ASM_RANGE=lo:hi` with `ASM_RANGE_IDX=k`, or `ASM_STEPS=<first step>:<step after the last>` with
`ASM_RANGE_IDX=k` and the same `ASM_CUTS` in every slice. With `ASM_STEPS` a slice can be drawn as soon as the planner has
finished its last step: record.py writes each step's events to `asm_<chapter>.chunk<k>.pkl` as it goes, and the renderer reads
the chunks while the full file is absent. `merge_parts.py <chapter>` joins the slices and keeps each slice's `audit/` folder
(`ROBOTBUILD_AUDIT=1`) as `<chapter>/audit.part<k>/`, listed with its frames in `<chapter>/audit_parts.json`. A frame costs
about 0.65 s (SSAA) on the shared 4-core runner; `ROBOTBUILD_AA=fxaa` roughly halves it.

Round 9: a slice boundary is a *soft* one. Round 8 forced a cut at each (a different tripod), so that nothing in the shot plan
reached across it; now the shot plan is chosen segment by segment (each from its own frames and the camera before it), so a
slice's frames are still the chapter's own, but the camera carries on across a boundary unless the next step needs another view.
Other round-9 camera rules: a cut is forced only where something jumped (the first frame drawn while a MiR is away on a drive not
shown; its return, if the MiR or arm is not where it was; an arm jump over `ASM_JUMP_DEG` = 5 deg, smaller ones are drawn as a
short labelled reposition); a fetch not shown holds the shot; picks at the table are drawn on the visits whose drives are drawn
(`ASM_PICK_SHOW` = 2). `asm_slices.py` takes both chapters in one queue and starts each slice under `/tmp/memslot` (the
runner's shared memory budget), at most three at a time, module slices first.

```
# chapters 40 and 41 from run 13 (each slice starts when the planner has passed its last step)
python asm_slices.py module:M08,M17,M24 chamber:C09f,C14,F05b,F10a,F16,F25,F31,F39,F45,F51,F55 \
  --results=<planner's results_run13.json> --traj=/tmp/robotbuild/traj/run13 --upto=T01 --max-running=3 --mem=2.5
# one slice by hand
ROBOTBUILD_AUDIT=1 ASM_TRAJ=/tmp/robotbuild/traj/run13 ASM_STEPS=F10a:F16 ASM_RANGE_IDX=4 ASM_UPTO=T01 \
  ASM_CUTS=C09f,C14,F05b,F10a,F16,F25,F31,F39,F45,F51,F55 \
  xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/memslot 2.5 /tmp/venv/bin/python asm_render.py chamber \
  --fail_notes=desktop-lpbf/analysis/out/assembly/run10_fail_notes.json
python merge_parts.py 41-assembly-chamber
```
