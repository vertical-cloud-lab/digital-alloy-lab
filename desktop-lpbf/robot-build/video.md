# The desktop LPBF built by two mobile manipulators: the video (round 7, 2026-11-25)

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260) and PR 266. Sterling asked on
2026-11-25 to see the build carried out **by** two UR12e arms, each on a MiR250, using the full set of parts spread
along a long table; every machining step and the assembly (screws, seals, tightening), with a person only where one is
really needed; and, on screen, the running cost by category (new against used, with the expensive items one by one),
the lead times (the long ones, and how short they get bought used), and time estimates for machining and assembly.

**Video:** [`cad/img/robotbuild/robot-build.mp4`](../cad/img/robotbuild/robot-build.mp4) (STATUS_MP4).
YouTube chapter list: [`chapters.txt`](../cad/img/robotbuild/chapters.txt); four frames of every chapter:
[`contact-sheet.jpg`](../cad/img/robotbuild/contact-sheet.jpg); what went in: [`compose.json`](../cad/img/robotbuild/compose.json).

STATUS_STILLS

## How it is made

Each chapter is rendered on its own, as raw 1280 x 720 frames with one line of metadata per frame
([`cad/robotbuild/README.md`](../cad/robotbuild/README.md), [`common.py`](../cad/robotbuild/common.py)). Then
[`compose.py`](../cad/robotbuild/compose.py) draws every panel over the frames with PIL
([`panels.py`](../cad/robotbuild/panels.py)) and streams them into one H.264 file (12 fps). So the numbers on screen can
change without re-rendering any 3-D, and every chapter shares one look:

- **Caption bar** (top): what is happening, and a second line with the numbers and sources. At its right end, who is
  working (robot A, robot B, person, machine, outsourced, supplier) and the step's result (pass, fail, redesign, person
  needed).
- **Clocks** (bottom left): project time in 8 h working days, and running machine, robot, person and CAM hours and
  outsourced days. Each frame carries the real-world time it stands for (`proc_s`: 1/12 s for a robot motion shown in
  real time, much more in a time-lapse) and what it adds to each counter (`add`); the clocks are the running sums over
  the whole video. A chapter that sets no `add` is counted from who is working (each robot, person or machine named
  counts the frame's time). The clocks are hidden where no project time passes (the hall, the parts tour, the summary).
- **Cost panel** (right, chapter 10): the running total of the kit at spec (the laser chain as specified, the cheapest
  listed option on every other line), new against used where a sensible listing exists; the current category with its
  new and used cost; and its big items, the one in close-up highlighted, each with its new and used price and lead
  time. The BOM's cheapest-to-premium range is the second line (its low end mixes in under-spec substitutes, such as a
  $3.3k laser).
- **Lead-time panel** (right, chapter 10): every order's lead time in weeks from placing it to the part at BYU, new and
  used side by side, the longest first, long ones (six weeks or more new) marked; the item in close-up highlighted.
- **Chart** (right, chapter 50): the leak check's pressure curve, drawn up to the frame's time.
- A thin progress bar along the bottom edge with a tick at each chapter; each chapter's title shows for its first
  seconds.

The person is byu-vcl PR 318's ([commit 9740ba8](https://github.com/vertical-cloud-lab/byu-vcl/tree/9740ba8)
`vertical-lab/people.py`): MakeHuman's CC0 base mesh with its skeleton and skin weights, posed every frame (a walk cycle,
two-bone arm IK to hand targets, a lean, the head turned to what it looks at). It is vendored as
[`cad/robotbuild/people.py`](../cad/robotbuild/people.py), in the colours of the PR branch's other MakeHuman figure
(`render_scale.PERSON_COLOURS`: a long-sleeved T-shirt, jeans, trainers) and with safety glasses. MakeHuman's files are
fetched at run time (sha256-pinned) and never committed.

## The chapters

STATUS_TABLE

| Chapter | What it shows | Where its motion comes from | Time |
|---|---|---|---|
| 00 The hall | The hall from above, then a fly-over: the robot shop ([`analysis/shop/shop_cell.py`](../analysis/shop/shop_cell.py), beside the bench), the 12 m table with every part on it as delivered ([`kit_table.py`](../cad/robotbuild/kit_table.py), machined parts as their stock blanks, parts over 12.5 kg on pallets behind lane B), the assembly bench ([`analysis/assembly/cell2.py`](../analysis/assembly/cell2.py)), both MiR250 + UR12e (PR 318's meshes), a person and a 355 ml can | Only MiR A drives, along its own empty lane with its arm parked (1 m/s, 0.3 m/s²: shop_cell's MiR speed); no arm moves | No project time |
| 10 The parts | The camera runs along the table zone by zone (stock, sheet, motion, gas, optics, electronics, seals, frames) and closes in on the big items: the MIC-6 plate, the laser, galvo, f-theta lens, collimator, shutter, scan card and PC, UPS, safety controller, zero-point clamps, scroll pump, O2 analyzer, blower and the rack. Then the long leads, each with its own beat: the IDEC guard switch (27 weeks), the Omron K8DT relay (out of stock until March 2027), the laser (12-15 weeks new, about a week used) and the honing (3-6 weeks, estimate); it ends on the totals at spec and the weeks to ready-to-assemble. Cost and lead-time panels as above | Camera only | No project time |
| 15 Estimates | Three cards: making the custom parts (287 shop hours: CAM, setups, cutting, deburr and inspection); the routes (BYU hours, cost, weeks to the first leak test; the recommended hybrid keeps 134 hours at BYU and takes 7-12 weeks); the assembly (steps, robot-hours, person-hours, failures) | None (2-D) | No project time |
| 20-41 | The shop worker's receiving, machining and finishing chapters and the assembly worker's two assembly chapters: see their notes | Collision-checked plans (cell.py's FCL checks, IK branches, RRT-Connect) | Real time for the arms; machining time-lapsed |
| 50 Integration | sequence.py's tray steps at the Kardex VLM: T01 the 84 kg process module onto the tray by a person with a lift table; T02 the 12U rack and its units (UPS 23 kg, laser 40 kg, PC, DIN drawer); T03 the gas module (scroll pump 26 kg); T04 the hoses and lines; T05 the tray dock; T06 the leak check (rate of rise) | A person's moves, keyframed (walk cycle, hand targets); the arms stay parked beside the opening because none of T01-T06 is planned for them | Time-lapsed: about 3.6 h of a person's work and 1.25 h of pumping |
| 60 Summary | Charts: the clocks' totals; the kit's cost by category, new against used; when every part is in hand by buying route; time and cost by route (in-house, outsourced, hybrid, robot shop); where a person is needed; what was redesigned | None (2-D) | No project time |

## Caveats

- **The integration chapter's person and lift table are illustrations, not plans.** The steps and who does them are
  sequence.py's (T01-T06). The lift table drawn is the shop's (Vestil SCTAB-1000-2040-AC, 20 x 40 in, 1,000 lb, from
  [`robot-shop-equipment.csv`](../robot-shop-equipment.csv)); whether it rises to the tray's 857 mm and rolls is not
  checked. Its times are estimates. The leak check's curve is the expected one from [`seals.md`](../seals.md) section 7
  (pump-down to 1 mbar in about a minute; a rise of about 8 × 10⁻⁴ mbar/min against the 1 × 10⁻³ pass line), not a
  measurement.
- **The intro's and the parts tour's motions are camera moves and one MiR driving an empty lane**; the arms stay in
  cell2's park pose.
- **Costs and lead times** are the data worker's ([`lead-times.md`](lead-times.md), [`hud.json`](hud.json)): new is
  bom.csv's low-to-high range; used is the sensible eBay and surplus listings of
  [`cost/used-options.csv`](../cost/used-options.csv) re-based on today's BOM. Lead times include BYU's purchase-order
  time where an order needs one.
- The 3-D frames are flat-shaded software renders at 12 fps; small parts are simplified as in the CAD (most screws are
  shown only where the assembly chapters drive them).

## Rebuild

From the repo root, under `xvfb-run -a -s "-screen 0 1920x1080x24"` and `/tmp/capmem 3G` (frames go to
`/tmp/robotbuild/frames`, never into the repo):

```
python desktop-lpbf/cad/robotbuild/ch_intro.py          # 00-intro
python desktop-lpbf/cad/robotbuild/ch_parts.py          # 10-parts (ch_parts.py meta: the numbers only)
python desktop-lpbf/cad/robotbuild/ch_estimates.py      # 15-estimates
python desktop-lpbf/cad/robotbuild/ch_integration.py    # 50-integration
python desktop-lpbf/cad/robotbuild/ch_summary.py        # 60-summary
python desktop-lpbf/cad/robotbuild/compose.py           # the MP4, chapters.txt, contact sheet, compose.json
```
