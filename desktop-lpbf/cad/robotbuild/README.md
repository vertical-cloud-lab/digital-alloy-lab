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
