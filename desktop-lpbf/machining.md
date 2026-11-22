# Machining review: can BYU's shops make the machined parts? (issue #260, PR #266)

This is a review of the machined parts in `cad/lpbf_low.py` (M50 module) by open-source CAM and scripted
design-for-machining (DFM) rules. It covers what BYU's shops list, what a 3-axis mill, a 4th axis and a lathe can and
cannot reach, and the tools to buy. Nothing here has been quoted by a shop. A BYU machinist reviewed the build animation;
the first section answers him.

## G-code simulated in CAMotics (2026-11-22)

Sterling asked for last round's CAMotics install error to be sorted out. It was a library problem on the runner, not a
CAMotics bug. CAMotics now runs in Docker and has cut every setup of the frame and the floor plate.

It found six problems in the G-code, all caused by `freecad_cam.py`'s settings. All six are fixed. The re-run shows no
gouges and no rapids through stock. What's left is the frame features that were never programmed, six undersized hole
steps in the floor plate, and two slugs that drop out.

### The install error, and the fix

- **The error.** CAMotics' last release is 1.2.0, from February 2019.
  - Its `.deb` declares `libv8-3.14.5 | libv8-dev`. On the runner's Ubuntu 26.04, apt satisfies `libv8-dev` with Node
    22's `libnode-dev`, so the package would install.
  - The programs, though, are linked against V8 3.14 and OpenSSL 1.1, and don't start:
    `camsim: error while loading shared libraries: libv8.so.3.14.5: cannot open shared object file: No such file or directory`.
  - `ldd` also lists `libssl.so.1.1` and `libcrypto.so.1.1` as missing (Ubuntu moved to OpenSSL 3 in 22.04), plus the
    Qt 5 libraries.
- **The fix: a Docker image on Ubuntu 18.04**, the newest LTS that ships V8 3.14 (it left Ubuntu after 19.10) and
  OpenSSL 1.1 ([`camotics.Dockerfile`](analysis/machining/camotics.Dockerfile)).
  - It checks the `.deb`'s sha256.
  - The `.deb` also needs `libqt5websockets5`, which it doesn't declare. Without it, camsim stops with
    `libQt5WebSockets.so.5: cannot open shared object file`.
  - The command-line simulator `camsim` needs no display, so no xvfb. Building from source wasn't needed.
- **CAMotics 1.2.0's own limits,** worked around in the script:
  - **No G83.** It doesn't implement peck drilling: it logs `Not implemented: G83` and skips the hole. The script expands
    every canned cycle into G0/G1 moves the way LinuxCNC runs them.
  - **Start point.** The tool starts at (0, 0, 0), which is inside the blank. A `G92 Z1000` after the preamble starts it
    1 m above the part.
  - **Memory.** A whole frame blank at 0.5 mm needs more than the container's 3 GB, so each blank is cut in 32 mm slabs.
  - **Timing.** Every move takes length / F. Rapids run at a hard-coded 10 m/min (`src/gcode/Move.cpp`:
    `feed = 10000; // TODO FIXME`).

### Method

- **G-code.** FreeCAD 1.0.2 re-posted all five setups from the committed model (a snapshot of `cc1e0a1`), then again
  after each round of fixes.
- **Simulation.** [`camotics_sim.py`](analysis/machining/camotics_sim.py) cuts each setup in camsim on the full blank at
  0.5 mm, with each tool's diameter and stick-out from `freecad_cam.TOOLS`. All the tools are flat-ended cylinders:
  CAMotics has no drill-point shape, so the drill points are checked by arithmetic ([below](#drill-points)).
- **Chaining.** camsim's workpiece can only be a box, so a setup can't start from the last one's result.
  - Each setup's result is turned back into the part frame and intersected with the others. For the frame, it's also
    intersected with the blank minus the 274 × 184 waterjet slug.
  - The final shape is the same as chaining.
- **Compared with the model on a 0.5 mm voxel grid:**
  - gouges (material the part keeps that was cut away);
  - leftover (material that should be gone);
  - the deepest point of each.

  Differences within 1 mm of the model's surface are voxel noise and are not counted. Material no longer joined to the
  part is listed as loose.
- **Rapids through stock.** CAMotics cuts with rapids like any other move and doesn't flag them.
  - So the script sweeps every G0 against the stock in front of it: the chained result of the earlier setups, minus
    what this setup has cut so far (a z-map of the lowest tool tip).
  - It counts material more than 0.5 mm inside the tool's path.

### Results after the fixes

Results are in [`camotics_sim.json`](analysis/out/machining/camotics/camotics_sim.json). The first run, before the
fixes, is in [`camotics_sim_before_fixes.json`](analysis/out/machining/camotics/camotics_sim_before_fixes.json).

| Setup | Cut away (cm³) | Rapids through stock | CAMotics time (min) | Recount (min) | FreeCAD's estimate (min) |
|---|---|---|---|---|---|
| frame A, top up | 427 | 0 | 41.7 | 41.3 | 49.2 |
| frame B, bottom up | 445 | 0 | 6.8 | 6.5 | 11.0 |
| frame C, front up (door) | 323 | 0 | 11.1 | 10.5 | 15.9 |
| floor A, top up | 455 | 0 | 51.2 | 51.0 | 58.9 |
| floor B, bottom up | 177 | 0 | 10.0 | 9.2 | 23.9 |
| **frame / floor plate** | | **0** | **59.6 / 61.2** | **58.3 / 60.2** | **76.0 / 82.8** |

| Part | Gouge deeper than 1 mm | Leftover deeper than 1 mm | Deepest leftover | Loose pieces |
|---|---|---|---|---|
| frame | none | 31.8 cm³ in 27 places | 12.4 mm: the bore in the right wall at y 0, z 58-82 | none |
| floor plate | none (deepest 0.5 mm, voxel noise) | 0.14 cm³ in 6 places | 2.0 mm: four hole steps at (±135, ±90) | port slug 52.6 cm³, slot core 12.7 cm³; both drop in setup A |

- **All of the frame's leftover is setup-C work that `freecad_cam.py` never programmed:** the back-wall inlet slot
  (13.1 cm³), the side-wall bores (7.3 and 2 × 3.5 cm³), the ports, the rail holes and the plenum and insert holes.
  Setup C programs only the door opening, as before.
- **The floor plate's leftover is six hole steps wider than the biggest drill in the set.** They are at (±135, ±90),
  z -11 to -9.5, and at (±58, 0), z -8 to -7. The 6.0 mm drill leaves up to 1 mm of wall. They need the right drill
  or a helical end-mill pass.

| Floor plate, first run | Floor plate, after the fixes |
|---|---|
| ![](analysis/out/machining/camotics/camotics_floor_before_fixes.png) | ![](analysis/out/machining/camotics/camotics_floor.png) |

| Frame, first run | Frame, after the fixes |
|---|---|
| ![](analysis/out/machining/camotics/camotics_frame_before_fixes.png) | ![](analysis/out/machining/camotics/camotics_frame.png) |

### What it found, and the fixes in freecad_cam.py

1. **The face mills left the corners and patches along the edges unfaced** (both parts, all four face ops).
   - The face op used the stock as its boundary, which keeps the 63.5 mm face mill inside the stock. FreeCAD's default
     45° zig-zag also touches the edges only at its turns.
   - CAMotics showed 1.55-2.7 mm of skin in patches up to 20 mm in from every edge.
   - Fix: face the face's bounding box plus the tool radius (`BoundaryShape = Boundbox` with `ClearEdges`), zig-zag along
     x. That adds 0.5 min per face op.
2. **The floor plate's bottom web was never faced off.**
   - Setup A cuts the outside down to z -20.5, 2.2 mm short of the blank's bottom. Setup B's stock was the 312 × 222
     outline, so its face mill stayed inside the outline and the web ring outside it stayed on.
   - Then 303 rapids of the 1/4 in. notch tool ran its shank through the ring (10 cm³ in all).
   - Fix 1 faces the web off.
3. **Two dowel holes that open on top were drilled up through the bottom** in setup B, because `drill_all` took every
   hole.
   - That cut two Ø6 × 5.5 mm holes into the underside (127 mm³ each). The drill also rapided 3.5 mm into solid stock.
   - Fix: holes that open only on top are drilled in setup A, and the rest from below.
4. **Inner hole steps were drilled before the step above them.**
   - The 5.0 mm step of four stepped holes went before their 6.0 mm counterbore, and the 3.3 mm step of ten M4 holes
     before their 4.2 mm step. So the drill rapided down to its R plane 4-5.5 mm inside solid stock, 14 times.
   - Fix: the step nearest the entry face goes first.
5. **Through holes stopped with the drill's tip at the far face.** That leaves the 118° point's cone in the exit: 1.3 mm
   for the 4.2 mm drill.
   - Fix: `ExtraOffset = Drill Tip` on steps whose far end opens at full diameter.
6. **The port and slot slugs were held by the web until setup B,** whose fixture needs the port open for its centre stud.
   - Fix: the trepan and the slot profiles go to z -23.2, 0.5 mm past the blank, so the slugs drop in setup A. The
     fixture must leave room under them.
   - The 20 × 104 slot is cut by its outline only, so its 7 × 91 × 20 mm core drops too. Hold it, or pocket the slot.

Before the fixes, floor setup B had 319 rapids through stock: 303 from the notch tool, 16 from the drills. The floor
plate had 0.25 cm³ of gouges and 71 cm³ of leftover deeper than 1 mm, 65 cm³ of it the two slugs. The frame had no
gouges and no rapids through stock, only the unfaced edges and the unprogrammed features.

### Drill points

The simulation's drills are flat, so it can't see their points. By arithmetic, from the programmed depths:

- **Blind steps still stop with the drill's tip at the model's flat floor.** So the full diameter ends 0.3 × D short:
  1.0 mm for the 3.3 mm M4 tap drill, 1.5 mm for the 5.0 mm pilot, 1.8 mm for the 6.0 mm drill.
- That matters for the frame's 18 M4 holes (thread depth) and the 20 lid inserts' 5.0 mm pilots. Drill to the thread or
  insert depth plus the point, or use a flat-bottom drill.
- Every drill op is listed under `drills` in `camotics_sim.json`.

### Cycle time

- **CAMotics' time and the recount agree to within the rapid speed:** 59.6 against 58.3 min for the frame, 61.2 against
  60.2 min for the floor plate. Both are length / F. CAMotics runs rapids at 10 m/min, the recount at the VF-4's
  25.4 m/min.
- **FreeCAD's own estimate is 15-140 % higher than CAMotics' per setup,** because it times every move that changes Z at
  the plunge feed (`freecad_notes` in [`freecad_cam.json`](analysis/out/machining/freecad_cam.json)).
- None of the three counts acceleration, tool changes or spindle ramp-up.
- The fixes changed the cutting time from 57 to 58 min for the frame and from 58 to 60 min for the floor plate.

### Not checked

- **Holder, spindle and fixture collisions.** CAMotics models the cutter only, and the rapid check treats the tool as a
  cylinder going up forever.
- **Cutting loads:** chip load, deflection and chatter.
- **The taps, reamers, insert tools and chamfers,** which aren't programmed.
- **Anything under about 1 mm.** The 0.5 mm grid doesn't check the O-ring grooves' width and depth to tolerance.
- **Frame setup C beyond the door opening,** which isn't programmed.

Run: `docker build -t camotics:1.2.0 -f desktop-lpbf/analysis/machining/camotics.Dockerfile desktop-lpbf/analysis/machining`,
then `freecad_cam.py` (its docstring), then `/tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/machining/camotics_sim.py`.
It takes about 13 min.

## Update: the chamber as a through-frame, the 4th axis, and honest hours (2026-11-20, evening)

### The answer to the machinist

He is right on both counts.

- **The deep pocket was the worst part.** It needed 6 in. OAL end mills and a 3/8 in. tool at 13:1 for the R5 corners,
  and it turned 78 % of a 33 kg block into chips.
  - It is now a through-frame cut from 5-1/2 in. plate, with a 20 mm floor plate bolted under it on a second face O-ring
    ([`chamber-construction.md`](chamber-construction.md) is the decision record).
  - The core comes out as one 17 kg slug (waterjet or bandsaw), and the walls are finished from both sides at 63 mm
    stick-out. Nothing on the frame or the floor plate needs a tool longer than a standard 3/4 x 4 in. end mill (3.3:1).
- **Nothing in the machine needs 5-axis.** The earlier review used six fixed tool directions, which are 3-axis setups,
  never simultaneous 5-axis. On a mill with a 4th axis the frame takes three setups (bottom, top, then the four walls in one
  clamping on the rotary), down from six.
  - Across all 48 machined parts, the rotary takes the setup count from 118 to 60 where a part swings inside an
    HRT210. Most of that drop is two-setup plates, where a flip in the vise is just as quick, so setup time only falls
    from 99 h to 85 h.
  - Four details still need a special tool or a compound angle (below), and each has a fix.
- **"A few hundred hours of toolpathing and machining" is about right.** Counted honestly, the 48 parts are about 264 h
  with 3-axis setups (250 h with a 4th axis).
  - Only 28 h of that is the machine cutting. The rest is CAM (116 h), setups (99 h) and deburring and inspection.
  - The earlier "63 h of machine and setup time plus 30-40 h of CAM" for 37 parts left out most of the setup and
    programming time.
  - The levers that bring the total down to about 150 h are [listed below](#hours-for-the-whole-machine). The chamber
    redesign is one of them, but not the biggest.

### What changed and what was re-run

- **Model.** Section 5 of `cad/lpbf_low.py` (`FRAME`, `CHAMBER_OPS`) and `cad/joints.py`:
  - frame and floor plate;
  - floor O-ring;
  - 18 M4 floor screws and 2 dowels;
  - rail holes tapped through the back wall from outside, with sealed plugs;
  - a 260 mm rail;
  - the inlet plenum raised onto the frame;
  - R10 inside corners, an R6.5 door opening and round-ended slots;
  - the through-beam's 2-010 groove made a counterbore. Its inner wall had been 0.1 mm thick round the M6 thread, and that
    sliver also broke the FEA mesh.
- **Checks on the new model.** Interference (0 for M50, S25 and L75, all states and sweeps), CalculiX (cases 1, 1b, 1f: yield
  SF 5.1 open-top and 9.9 with the lid) and the
  Shigley floor-joint check: see [`chamber-construction.md`](chamber-construction.md).
- **Voxel stock removal** ([`cam_sim.py`](analysis/machining/cam_sim.py); the frame's stock is the blank minus the
  waterjet slug):

  | Part | Residual, standard tools | Residual, + long tools |
  |---|---|---|
  | frame | 1.05 cm³ | 0.56 cm³ |
  | floor plate | 0.09 cm³ | 0.09 cm³ |
  | old block | 29.1 cm³ | 3.4 cm³ |

  What's left on the frame is voxel slivers in the R10 corners (the 3/4 in. tool's R9.5 fits) and Ø3-4 holes the voxels
  can't resolve.

  | Frame, standard tools | Floor plate, standard tools |
  |---|---|
  | ![](analysis/out/machining/cam_process_chamber_body_std.png) | ![](analysis/out/machining/cam_chamber_floor_plate_std.png) |
- **Per setup** ([`per_setup.json`](analysis/out/machining/per_setup.json)): the frame needs all six directions, and the
  front alone has 319 cm³ only it can reach (the door opening).
- **Real CAM:** FreeCAD 1.0.2's CAM workbench, run headless ([`freecad_cam.py`](analysis/machining/freecad_cam.py),
  [`freecad_cam.json`](analysis/out/machining/freecad_cam.json)).
  - It programmed the frame (two flat setups plus the door opening) and the floor plate (two setups) with Adaptive,
    Profile, Pocket, Helix and Drilling, and posted LinuxCNC G-code.
  - Cutting time from the G-code: frame 60.0 min, floor plate 57.9 min. Its O-ring grooves used a slow 1/8 in. tool and
    account for 38 and 35 min of that; a 4 mm end mill does each in about 8 min.
  - Taps, reamers and tool changes are not timed.
  - Its 1.0 Adaptive op only sees the stock as a box, so the frame's opening was cut with Profile passes. Its Drilling and
    Helix ops needed work-arounds headless; both are documented in the script.
  - CAMotics now runs (in Docker) and has cut this G-code; six fixes followed. See
    [G-code simulated in CAMotics](#g-code-simulated-in-camotics-2026-11-22) above. The times in this bullet are from
    before those fixes.
  - Use it as a head start and a check. The shop will still program and prove out in its own CAM.
- **Setup plan:** [`setup_plan.json`](analysis/out/machining/setup_plan.json) ([`setup_plan.py`](analysis/machining/setup_plan.py)).
  For the frame and the floor plate it gives:
  - the blank and the core removal;
  - every setup's machine, fixture, which face is up (as a rotation from the model frame) and the A-axis index angles;
  - per operation: the feature, the tool (type, diameter, stick-out), the cuts it makes as references to the model
    (`FR-xx`, `FP-xx`, `J:<key>`), and a time from vendor feeds;
  - and, for every other part, the 3-axis and 4th-axis setup counts.
- **Time on the mill at vendor feeds** (Helical's 1600-2400 SFM and chip loads for 3-flute carbide in 6061, Haas drill and
  tap charts, 60 % efficiency): frame 112 min, floor plate 51 min, plus 12-71 min on the waterjet.

### The frame, setup by setup

| Setup | Machine and fixture | Face up | Work |
|---|---|---|---|
| F-S0 | bandsaw; waterjet (a Ø12 start hole first) | top | saw the 15 x 9.5 x 5.5 in. blank; core out as one 274 x 184 slug |
| F-S1 | VF-4, 3-axis; blank on risers, toe clamps on 1 in. end tabs | bottom | face; outside and opening up to mid-height; rebate; 18 M4 holes; 2 dowel holes |
| F-S2 | VF-4, 3-axis; end tabs sawn off; a "dummy floor" plate that pins and screws the frame down through its own floor-screw holes | top | face; outside and opening down to mid-height; lid gland; 20 lid inserts |
| F-S3 | VF-4 + HRT210-class rotary on a 2-1/2 in. riser; the same dummy-floor plate on the platter, A along the frame's z | A = 0 front, 90 left, 180 back, 270 right | door opening; Ø18 bores and through-beams; inlet slot, argon port, plenum inserts, rail holes; KF-25 bore, vacuum and bearing-cap inserts, O₂ port |

- **Swing.** About its z axis the frame swings 188 mm, more than the HRT210's 152.4 mm centre height. Hence the riser,
  which puts A at 215.9 mm. The rotary carries 4.3 kg plus the plate, well inside its 38.6 kg unsupported rating.
- **The other way to hold it.** Putting A along the frame's x needs no riser (127 mm swing), but the side walls then need
  their own setups and the sealing faces are cut on the rotary. It still comes to three setups.
- **The rail holes** were the one feature still on an inside face: they had to be drilled and tapped through the door
  opening, 206 mm from the front face. They are now tapped through the back wall from outside, in the F-S3 back index,
  with an M4 plug screw on a bonded seal washer at each outer end. That is 4 small seals, worth about 0.02 ppm O₂/h.

### 4th axis and 5-axis, part by part

[`setup_plan.json`](analysis/out/machining/setup_plan.json) has every part's reachable directions, its 3-axis setups and
the best rotary axis with its swing.

- **Where the rotary saves setups** (3-axis → with a 4th axis):
  - the frame 6 → 3;
  - the piston head 6 → 3;
  - the build plate 5 → 2;
  - the camera viewport adapter 5 → 2;
  - the M50 module body 4 → 1;
  - the cover-slide drawer 4 → 1;
  - the gland plate, heater block and rod end 3 → 1;
  - the metering base 3 → 2.
  - The other parts are mostly plates with two setups (top, bottom). A rotary would do both in one clamping, but a
    flip in the vise takes as long, so the hours model gives the rotary no credit there.
- **Too big for an HRT210:** the base plates (swing 240-274 mm) and the optics bridge (184 mm) stay on the table.
- **Needs a special tool or a compound angle (5-axis or a fixture), with a fix for each:**

  | Part | Feature | Fix |
  |---|---|---|
  | camera viewport adapter | boss and bore on the line of sight from (75, −45) to the plate centre: two angles, so a single rotary can't square it up | a sine plate on the 4th axis, or turn the boss as its own part on a seat with one tilt |
  | chamber lid | the cover-slide drawer slot is enclosed (still drawn so) | mill it open from the underside, then a 1/4 in. keyseat cutter for the drawer's ledges, or sinker EDM |
  | chamber door, cover-slide drawer | half-dovetail O-ring grooves | a dovetail cutter, or plain grooves with moulded seals |
  | build plate, heater block, piston head, gland plate, module body | bayonet lugs, internal and radial grooves, the bore | lathe work (grooving tools) and outsourced honing, as before |

- **BYU's kit** (pages fetched 22:31-22:46 UTC):
  - Physics' Haas VF-2SS "provides new capabilities like a 4th axis" (rotary model not published).
  - The Physical Facilities shop lists a "multi-axis CNC mill" with no model.
  - No BYU page names a rotary table model, a trunnion, a 5-axis machine or a right-angle head.
  - The ME Prototyping Lab's "DM1 and VF4 CNC mills" was not on the live page at 22:44 UTC.

  The plan assumes a VF-4-class mill with an HRT210-class rotary, which matches the machinist's "one of our 4 axis
  machines". Check the rotary's centre height before planning F-S3.

### Hours for the whole machine

The method and per-part rows are in [`hours.py`](analysis/machining/hours.py) and
[`hours.csv`](analysis/out/machining/hours.csv).

- **CAM hours are an estimate:** 0.5 h + 0.6 h per setup + 0.015 h per hole, +1 h for lathe-and-mill parts, and +8 h for the
  block's deep pocket. A search found no published rule of thumb.
- **Setups:** 0.75 h for vise parts and 1.25 h for parts over 300 mm. Modern Machine Shop's survey median is 68-90 min.
- **Run** uses the conservative removal rates of the review below.
- **Deburr and inspect:** 0.25 h a part, 1 h for a part with a sealing face.

| | CAM | Setups | Run | Deburr + inspect | Total |
|---|---|---|---|---|---|
| Chamber body before (block, 6 setups) | 12.8 h | 7.5 h | 15.5 h (3.5-5 h at vendor feeds) | 1 h | 36.8 h |
| Chamber body now (frame 3 setups with a 4th axis + floor plate 2 + waterjet) | 8.2 h | 7.5 h | 7.1 h (3.5 h at vendor feeds) | 2 h | 24.8 h |
| All 48 machined parts, 3-axis | 116 h | 99 h (118 setups) | 28 h | 21 h | **264 h** |
| All 48 machined parts, with a 4th axis where it helps | 116 h | 85 h (60 setups) | 28 h | 21 h | **250 h** |

**What drives the few hundred hours:** 48 parts each need a program, a fixture, setups and a first-article check. Cutting
is about a tenth of it. These levers bring the total down; the hours are estimates from the per-part rows:

1. **Buy instead of make, about 30-40 h.**
   - The window flange and retaining ring become a stock fused-silica viewport.
   - The f-theta adapter ring, field stop, beam tube and camera window ring become Thorlabs SM-series lens tubes and
     adapters.
   - The recoater motor standoff and bracket become a stock NEMA 23 bracket.
   - The door and guard-door handles become catalogue pulls.
   - The Macor rings and the striker become stock washers and discs.

   Those 12 parts take about 52 h to make here; buying them leaves about 1 h each to adapt.
2. **Waterjet the 2D plate parts, about 15-20 h.** That covers the two base plates, the optics bridge, the galvo riser, the
   Z flange, the legs, the damper bracket, the arm and the small lugs. Each profile becomes a DXF, and the mill only drills.
3. **Standardise:** one tool library and one insert family, a CAM template per part type, and the same holes everywhere.
   That cuts about 30 % of the remaining CAM time, roughly 20-25 h.
4. **Use the 4th axis where it saves a setup: about 14 h.**
5. **Order plate at the finished thickness, about 6-8 h:**
   - lid and door 5/8 in.;
   - base plates 5/8 in. MIC-6;
   - optics bridge 1 in.

   Only the sealing faces then need skimming.
6. **The chamber redesign, about 12 h** (37 → 25 h), plus no long tools, no 13:1 corners, and the core back as stock.
7. **Merge small parts, about 5 h:** the window ring into its flange, and the recoater arm with the blade holder.

Together, roughly 100-115 h of savings: from about 250-265 h to about 150 h. Ten of the 48 parts were added to the model
this week (robot-tending and adapter parts); without them the totals are about 40 h lower.

### Tooling after the redesign

[`tooling-bom.csv`](tooling-bom.csv):

- **Dropped to quantity 0, as not needed:**
  - the 6 in. OAL 3/4 in. end mill (X1, $307.93);
  - the long 1/2 in. (A6, $96.63);
  - the 5 in. OAL 3/4 and 1 in. options (A7, A8);
  - the ball and corner-radius mills for the coves (A11, A12, X2);
  - the extension holder (X3).
- **Added:**
  - a second standard 3/4 in. end mill (A5, roughing and finishing);
  - a 4 mm gland end mill (A14, optional);
  - the "dummy floor" fixture plate (L7, 1 in. MIC-6, McMaster 86825K914, $437.71);
  - a 2-1/2 in. riser for the rotary (L8);
  - the rotary itself (L9, the shop's).
- **Buy for this job: $3,695.03** (was $3,661.88). Optional: $3,905.60 (was $4,950.78).
- [`machines.csv`](machines.csv) has a 4th-axis row, and the waterjet and saw rows are updated for the 5-1/2 in. frame
  blank.

### Still open from the review below

- the lid's drawer slot (still enclosed);
- the lid inserts' 1.18 mm webs (the lid gland and inserts were left as they were);
- the door and drawer dovetail grooves;
- the thin webs in the heater block, piston head, striker and carriage block;
- honing, outsourced.

## Short answer (the 37-part review, before the frame redesign)

The review below is of the model before the chamber became a frame and a floor plate. Where it disagrees with the section
above, the section above is current.

- **Most of it can be made at BYU.** Every machined part fits BYU's Haas mills in one setup, except the
  590 × 550 mm gas-module base plate, which needs one re-position or a waterjet outline. The largest milled part is
  the optics bridge (605 × 370 × 25 mm). The chamber body is cut from a 13 × 9.5 × 6 in. block. The Haas VF-4 in
  the ME Prototyping Lab (EB 117) travels 50 × 20 × 25 in., and Physics' VF-2SS travels 30 × 16 × 20 in. The Physical Facilities
  Manufacturing Shop (108 CTB) lists a CNC lathe with live tooling, TIG welding and wire EDM. It works by fee-paid
  work order and is open to all departments ([BYU shops](#byus-shops)).
- **Outsource the honing.** The Ø50.80 H7 bore (Ra ≤ 0.4 µm) has to be honed after the 316L module body is welded.
  No BYU shop lists a honing machine, and no Utah shop was found that advertises small-bore precision honing. The
  same goes for the S25 and L75 bores.
- **Two features cannot be machined as drawn. Change them before anyone writes a CAM program:**
  1. **The lid's cover-slide drawer slot** is an enclosed slot, 72 × 6 mm, running 146 mm in from the front edge. No
     straight tool reaches it, with standard or long tools: 11 cm³ stays uncut (red in
     [`cam_chamber_lid_std_long.png`](analysis/out/machining/cam_chamber_lid_std_long.png)). The fix is to mill it
     open from the lid's underside, as below.
  2. **Two of the recoater rail's M4 insert holes** in the inside face of the back wall sit at x = ±115/125 mm. That
     is outside the door opening (±110 mm), so no drill can be lined up on them from outside. Move them to
     |x| ≤ 100 mm or bolt the rail to a bar.
- **The 120 mm deep chamber pocket needs long tools or an extension holder.**
  - Standard-length end mills in an ER32 holder leave 29 cm³ in a band along the walls, because the holder hits the
    wall top.
  - The longest uncoated 3/4 and 1 in. carbide end mills found (5 in. overall) still leave 15.3 cm³: they don't
    reach the lowest ~30 mm of the walls.
  - The long set with 6 in. OAL tools (e.g. a 3/4 in. McMaster 8745A19, AlTiN, $307.93) gets it to 3.4 cm³.
  - A slim 32 mm extension holder with a 1/2 or 3/8 in. tool at 150 mm stick-out gets it to 0.9 cm³ (finishing
    cuts only).
  - What is left is the drawn corner and floor radii:
    - the R5 vertical corners would need a 3/8 in. tool at 12.6:1 length to diameter. Specify R ≥ 9.6 mm (3/4 in.
      tool) or R ≥ 12.7 mm (1 in. tool);
    - the R5 floor coves need a corner-radius tool with 120 mm reach.
- **Thin walls to fix:**
  - the lid-screw insert holes leave 1.2 mm to the O-ring gland and to the outer wall;
  - the heater block and the piston head have 0.4 mm webs;
  - the striker's counterbores break through;
  - the carriage-block bore leaves a 0.5 mm wall;
  - the lid's six M4 × 4 mm inserts for the window flange end 0.5 mm above the drawer slot. That leaves no room for
    the insert's prong or the tap's lead, and a crack there is a leak into the gas envelope.
- **Machine time, roughly:** 63 h of machine and setup time for one machine's 37 parts, plus about 30-40 h of CAM
  programming. That is at conservative removal rates (16 cm³/min in 6061, 3 cm³/min in 316L). An adaptive (HEM)
  roughing path on the VF-4 would probably cut the chamber's 10 h of roughing to 2-4 h (an estimate, not run).
  The chamber body alone is 15.5 h, because 78 % of its 12.1 L block becomes chips.
- **Tooling:** see [`tooling-bom.csv`](tooling-bom.csv) (115 lines).
  - **Buy for this job: $3,662**, plus two items not priced: metric STI plug gauges and the honing service.
  - Shop-standard tools, if a shop had none: $5,132 more.
  - Optional routes: $4,951, most of it a $3,769 roughness tester.
  - Prices are from McMaster-Carr and Lakeshore Carbide, fetched 2026-11-20 14:05-14:41 UTC.

## What was run

All scripts are in [`analysis/machining/`](analysis/machining/), and results and images are in
[`analysis/out/machining/`](analysis/out/machining/). The scripts used a frozen copy of `cad/` from 2026-11-20
13:53 UTC. The seal grooves another agent was adding at the time are not in it; they are covered by rule
[below](#features-from-the-seal-changes-not-in-the-model-copy-used).

| Step | Script | What it does | Run time |
|---|---|---|---|
| 1 | `inventory.py` | Builds the model with every joint hole cut. Classifies the parts as `render_build.py` does: 37 machined, 12 sheet, 86 bought, 28 fastener sets. Exports each machined part as B-rep and STL. | 14 s |
| 2 | `cam_ocl.py` | **OpenCAMLib 2023.1.11** (`BatchDropCutter`, `Waterline`; run in a Python 3.11 container because there is no wheel for 3.14). Drop-cutter grids, with a second drop for the tool holder, and waterline contours for the chamber body, lid, door and module body. | 62 s |
| 3 | `toolpaths.py` | Turns the OCL grids into zig-zag raster finishing paths and G-code (20-34 k moves per part, kept in `/tmp`). Draws them, and checks the stock-removal simulation against OCL. | 30 s |
| 4 | `cam_sim.py`, `per_setup.py` | Dexel/voxel 3-axis stock-removal simulation, described below. Also a setup count for all 37 parts, and the removal per setup. | 7 + 2 + 4 min |
| 5 | `residual_report.py` | Sorts the chamber's residual stock by cause. | 5 s |
| 6 | `dfm.py` | DFM rules on every B-rep: stock, holes, internal radii, sharp corners, webs, time. | 2 min |

How the simulation works:

- It voxelizes the part at 0.4-0.5 mm.
- For each of the six setup directions and each flat end mill (diameter, stick-out, holder diameter) it computes:
  - the part's height map from that side;
  - the cutter-location surface, as a grey dilation of the height map by the cutter disk;
  - a holder check: the tip can go no lower than the holder's own drop minus the stick-out;
  - the finished surface, as an erosion by the cutter disk, which is the swept volume of a dense raster.
- Everything above the finished surface is removable from that setup. Residual = stock − part − everything removable
  from any setup with any tool.
- The cutter-location surface matches OpenCAMLib's drop-cutter: median difference 0.0 mm for the chamber and −0.2 mm
  for the lid, and 97.5-100 % of points within one voxel ([`toolpaths.json`](analysis/out/machining/toolpaths.json)).

Two tool sets were run (sizes in `cam_sim.py`):
- **standard** (usually on hand): 1/16, 1/8, 1/4, 3/8, 1/2 and 3/4 in. at stocked lengths;
- **+long** (buy): 1 in. × 6 in., 3/4 × 6, 1/2 × 6, 3/8 × 4, 1/4 × 4 and a 1/8 in. long-reach.

Limits:
- flat end mills only (no ball or bull-nose), 3-axis only;
- no fixturing in the setup count;
- a voxel can't resolve features under ~2 voxels (Ø3.2 holes show as residual; they are drilled anyway);
- coaxial holes in opposite walls are merged into one long "hole" by `dfm.py` (Ø18 and Ø3.2 through both side walls
  of the chamber).

| OpenCAMLib toolpaths on the old block (blue raster, orange waterlines) | Residual stock of the chamber body, standard vs long tools: these two images were re-run on the through-frame (about 1 cm³ left); the block's 29.1 / 3.4 cm³ versions are in the git history |
|---|---|
| ![](analysis/out/machining/toolpath_chamber_z.png) | ![](analysis/out/machining/cam_process_chamber_body_std.png) ![](analysis/out/machining/cam_process_chamber_body_std_long.png) |

## Residual stock (what 3-axis milling can't reach)

| Part | Stock | Residual, standard tools | Residual, + long tools | Where, and what does it |
|---|---|---|---|---|
| Process chamber body (6061-T6) | 13 × 9.5 × 6 in. block, 12.15 L; part 2.73 L | **29.1 cm³** | **3.4 cm³** | Standard tools leave:<br>- a band along the walls, z = 6-102 mm, 20.7 cm³: the holder hits the wall top, since the deepest standard stick-out is 63 mm and the pocket is 120 mm deep;<br>- R5 vertical corners, 5.7 cm³.<br>With long tools:<br>- corners 0.7 cm³;<br>- R5 floor coves 2.0 cm³ (a flat end mill cannot cut a cove);<br>- the two rail insert holes in the back wall that sit outside the door opening's reach, 0.12 cm³ each (see above);<br>- 8 mm³ slivers in the sharp corners of the door opening and the inlet slot (they take the radius of a 1/8 in. tool).<br>Split by cause in [`residual_chamber.json`](analysis/out/machining/residual_chamber.json). |
| Chamber body, with the tool lengths actually found for sale ([`chamber_reach.py`](analysis/machining/chamber_reach.py)) | same | – | 15.3 cm³ with 5 in. OAL 3/4 and 1 in. tools; 0.9 cm³ adding a 32 mm extension holder (1/2 and 3/8 in. at 150 mm) | With 5 in. tools, a 12.3 cm³ band along the lowest ~30 mm of the walls stays uncut. ![](analysis/out/machining/cam_chamber_reach_5in.png) |
| Chamber lid (6061-T6, 16 mm) | 0.75 in. plate | **11.9 cm³** | **11.2 cm³** | The enclosed drawer slot. A 6 mm tall slot only admits a ≤ 1/8 in. tool from the front edge, and it is 146 mm deep. ![](analysis/out/machining/cam_chamber_lid_std_long.png) |
| Chamber door (6061-T6, 15 mm) | 0.75 in. plate | 0 | 0 | As drawn (plain rectangular groove). The half-dovetail groove that replaces it is an undercut by definition, so it needs a dovetail cutter (below). ![](analysis/out/machining/cam_chamber_door_std.png) |
| M50 module body (316L weldment) | turned and welded | 0.25 cm³ | 0.06 cm³ | Slivers ≤ 0.8 mm thick at the tube-to-flange face (z = −30 mm). They come from the coincident faces of the fused weldment, and the post-weld boring removes them. The spigot's radial O-ring groove is reachable from the side, but it is turned on the lathe. ![](analysis/out/machining/cam_build_module_m50_spigot_std_long.png) |

**Stock removal per setup** ([`per_setup.py`](analysis/machining/per_setup.py),
[`per_setup.json`](analysis/out/machining/per_setup.json); standard + long tools). "Only from this setup" is the
volume no other setup can reach, which is what makes the setup necessary.

| Part | Setup | Removable, cm³ | Only from this setup, cm³ | What needs it |
|---|---|---|---|---|
| Chamber body (9,424 cm³ of chips) | +Z (top) | 8,669 | 2,217 | pocket, lid gland, lid-screw inserts |
| | −Y (front) | 6,035 | 320 | door opening |
| | +Y (back) | 2,112 | 11.8 | inlet slot |
| | +X (right) | 2,244 | 9.4 | KF-25 port, side ports and bores |
| | −Z (floor) | 3,440 | 6.9 | inserts and dowels for the module, Z flange and legs |
| | −X (left) | 2,102 | 0.8 | recoater-screw bore |
| Lid (642 cm³) | −Y (front edge) | 468 | 34 | mouth of the drawer slot |
| | +Z / −Z | 390 / 389 | 10.2 / 9.1 | top-face inserts and counterbores / underside features |
| Door (249 cm³) | +Y (seal face) | 154 | 7.5 | O-ring groove |
| M50 module body | all | 988-1,248 | < 0.7 | everything is reachable from several sides; it is turned |

So the chamber body needs all six setups: the top, the floor and all four sides. Plan it as a block on
a fixture plate with a probe, not in a vise.

**Setups and undercuts for all 37 parts** come from the sweep in `cam_sim.json`: a greedy cover of every skin voxel
by the six directions, with a 1/8 in. tool of unlimited reach.
- 30 parts need 2 setups.
- These need more:
  - chamber body 5 with a thin tool of unlimited reach, 6 with real tools (table above);
  - build plate 5;
  - piston head 6;
  - camera adapter 5;
  - heater block, cover-slide drawer and module body 3-4.
- Skin that no direction reaches (undercuts and turned grooves):
  - build plate 20 %: bayonet lugs and gripper groove, so turn and groove it;
  - piston head 9 %: seal grooves;
  - camera adapter 9 %;
  - heater block 8 %: the bayonet socket's lug undercut, so an internal grooving tool on the lathe plus three milled entry slots;
  - gland plate 6 %;
  - the welded square-tube bridge posts 43 %: the closed inside of the tube, which is expected.

## DFM over every machined part

Full results are in [`dfm.json`](analysis/out/machining/dfm.json). Time = roughing at the MRR above + finishing 50 %
of the area at 40 cm²/min (6061) or 10 cm²/min (316L) + 0.3-2.5 min per hole + 20 min per setup (40 for the chamber
body).

| Part | Mat. | Stock (standard size) | Setups | Holes (from `joints.py`) | Smallest internal R / sharp internal edges | Thinnest web | Time, min |
|---|---|---|---|---|---|---|---|
| Process chamber body | 6061 | 13 × 9.5 × 6 in. block, 78 % removed | 6 | 35 STI (24 M5, 6 M6, 5 M4), Ø96, Ø25.4, Ø18 ×2, Ø6.4 ×2, Ø3.2 ×2 | R5 × 120 deep (3/8 in. at 12.6:1); sharp vertical corners in the outlet and overflow slots (162 mm of edge); door-opening and inlet-slot corners sharp | **1.18 mm** (M5 lid inserts to gland and outer wall) | 930 |
| Chamber lid | 6061 | 0.75 in. plate (5/8 in. if the 16 mm becomes 15.9) | 2 + slot | 20 × Ø5.5, 10 STI M4, Ø56, Ø22, 2 × Ø8 sensor ports | drawer slot unmachinable | 1.45 mm (M5 clearance holes to the edge) | 121 |
| Chamber door | 6061 | 0.75 in. plate | 2 | hinge and latch holes not drawn | R6 | – | 60 |
| Optics bridge | 6061 | 1.25 in. plate (1 in. if 25 → 25.4 mm) | 2 | 8 × M6 clearance, Ø80, Ø96 | – | – | 250 |
| Base plates (2) | MIC-6 | 0.75 in. (5/8 in. if 15 → 15.9 mm) | 2 | 8 × M8 tapped, 16 × M6 clearance + 4 cbore | R8 | 3.2 mm | 256 + 218 |
| M50 module body | 316L | weldment: Ø4 in. bar + 3/4 in. plate + tube + collar | 4 | Ø50.8 bore (hone), 6 × M4 tapped (collar), 2 × Ø6 dowel, 2 × captive-screw | – | 1.35 mm (flange tab holes to the edge) | 115 + honing |
| Gland plate | 316L | Ø3.375 in. bar | 2 | 6 × M4 clearance, 2 × M4 tapped, Ø15.98 rod bore | 2-114 grooves to add | 2.0 mm | 66 |
| Heater block | 6061 | Ø2.125 in. bar | 3 | 3 STI M3, 3 × Ø6.1 cartridge, 3 × Ø1.2 thermocouple (12.5 deep, 10.4:1) | sharp bayonet lug corners (38 mm of edge) | **0.4 mm** (Ø4.2 hole), 0.7-0.75 mm (TC and cartridge) | 72 |
| Piston head | 6061 | Ø2.125 in. bar | 6 | 3 × M8, 3 × Ø3.2, M5 cbore, Ø15.9 rod bore, M4 set screws | R1.7 × 11.5 (1/8 in. tool) | **0.4 mm** | 127 |
| Rod end | 316L | Ø1.625 in. bar | 2 | 3 × M3 tapped, Ø12.7, Ø5.6 × 29 (5.2:1) | – | 0.75 mm | 49 |
| Striker disc | 416 | Ø1.125 in. bar | 2 | 3 × M3 countersunk | – | **0.0 mm: the counterbores break out** | 44 |
| Recoater carriage block | 6061 | 1.75 in. plate | 2 | Ø24 bore | R2 | **0.53 mm** at the Ø24 bore | 49 |
| Camera adapter | 6061 | 1.75 in. plate | 5 | Ø22 | – | 1.2 mm | 108 |
| Overflow funnel block | 316L | 1 in. plate | 2 | Ø38 | sharp internal edges (228 mm) | 3.0 mm | 75 |
| 22 other parts | 6061 / Macor / 316L | plate or bar | 2 (build plate 5, drawer 3) | few | – | ≥ 1.0 mm (the Z-flange counterbores sit 1.0 mm from its edge) | 41-135 each |

### Holes and threads

- **Helical inserts (STI)**: 48 per machine (35 in the chamber body, 10 in the lid, 3 in the heater block). The McMaster
  91732A insert pages list these STI drills: M2.5 No. 37 (2.64 mm), M3 3.2 mm, M4 No. 19 (4.22 mm), M5 5.3 mm,
  M6 6.3 mm.
  - `joints.py` draws each insert hole at the insert's length plus a 1.5-3 mm tip at the screw size: M5 is 7.5 + 3.0 mm.
  - **Pronged inserts need room below for the prong and for the tap's lead.** For the 7.5 mm M5 insert, plan
    7.5 + ~2.5 mm (prong, about half a diameter) + 2 pitches = 11.6 mm. The model has 10.5 mm. Deepen the drill by
    about 1 mm, or use bottoming STI taps (the ones priced in the BOM are bottoming).
  - This is a rule of thumb; check it against the insert maker's chart.
- **Insert depth as drawn, against that rule:**

  | Inserts | Count | Drawn: insert + tip, mm | Needed (L + D/2 + 2P), mm |
  |---|---|---|---|
  | chamber top, M5 × 7.5 (lid screws) | 20 | 7.5 + 3.0 | 11.6 |
  | chamber floor, M5 × 7.5 (Z flange) | 4 | 7.5 + 1.5 | 11.6 |
  | chamber floor, M6 × 9 (legs) | 4 | 9.0 + 2.0 | 14.0 |
  | chamber floor, M6 × 12 (module flange) | 2 | 12.0 + 1.5 | 17.0 (the floor is 20 mm, so 3 mm left) |
  | back wall, M4 × 6 (rail) | 5 | 6.0 + 1.5 | 9.4 |
  | lid, M4 × 6 (metering base) | 4 | 6.0 + 3.0 | 9.4 |
  | lid, M4 × 4 (window flange) | 6 | 4.0 + 0.5 | 7.4: **no room above the drawer slot** |
  | heater block, M3 × 4.5 | 3 | 4.5 + 1.5 | 7.0 |

- **Tapped holes**: M3, M4, M6 and M8, all at or under 2.5 × D. The piston head's two radial M4 set-screw holes
  show as one 50 mm "hole" in `dfm.json` because they are coaxial. **Dowels**: 6 mm m6 pins → Ø6 H7, reamed.
- **Deep holes**: one Ø1.2 thermocouple hole is 12.5 mm deep (10.4:1). Peck it with a carbide micro-drill, or go
  to a Ø1.6 (1/16 in.) sheath. The Ø5.6 × 29 hole in the rod end (5.2:1) needs pecking.

### Features from the seal changes (not in the model copy used)

| Feature | Where | How it is cut | Tool (BOM) |
|---|---|---|---|
| 1.78 mm cord half-dovetail grooves, 1.32 deep × 2.3 wide (Parker; depth 1.27-1.37) | door and drawer faces | Rough with a 2 mm (or 1/16 in.) end mill, then one dovetail pass on one wall. An undercut, so a special tool. | dovetail O-ring cutter (G1), 2 mm end mill |
| 1.78 mm face grooves (2.3-2.6 wide) | dock slot, plenums, window flange, camera adapter, metering base, gland plate | 2 mm or 1/16 in. end mill, two passes; corners ≥ 1.2 mm radius | A |
| 3.53 mm lid face gland, 4.6 × 2.65 | chamber top face | 1/8 in. end mill, two passes (gland corners R4/R6 allow it) | A1 |
| 2-238 radial groove on the spigot OD, root Ø90.5 × 4.8 wide | module body, after welding | external grooving insert (3.1 mm), two plunges and a finish pass; same setup as the bore so it runs true to it | G2 |
| two 2-114 rod-gland grooves, Ø20.0 in a Ø15.93 throat (2.04 deep, ~3.6 wide) | 316L gland plate | Micro 100 internal grooving tool (min. hole 9.4 mm, 1.57 mm wide), three side-stepped plunges per groove | G3 + X4 holder |
| SAE J1926 O-ring-boss ports (in place of NPT) | chamber body and lid sensor and gas ports | port counterbore-and-step-drill set (cuts the spot face, thread relief and O-ring cone), then the straight-thread tap | H1-H4 |

### Tolerances and finishes the design needs

| Feature | Requirement | Source |
|---|---|---|
| O-ring glands (lid, door, window, drawer, gland plate) | depth and width ±0.05 mm; sealing face Ra ≤ 0.8 µm, flanks Ra ≤ 1.6 µm | `analysis/out/seals/seals.md` (Parker ORD 5700 checks at ±0.05 mm); `low-profile.md` materials table |
| Chamber top face (lid seal) | flat within 0.05 mm over 312 × 222 mm (suggested: ±0.05 on gland depth is already 6 % of the 0.88 mm squeeze) | inferred from the gland check |
| Module bore | Ø50.80 H7 (+0.030/0), Ra ≤ 0.4 µm, honed after welding; plate keeps a 0.15 mm cold gap | `cad/module_params.py`, `modules.md`, `build-sequence.md` |
| Spigot in the Ø96 port | 0.10 mm radial clearance (H7/g6 seized hot in the FEA): port Ø96.00 H7, spigot Ø95.80 ±0.02 (suggested); groove root Ø90.5 × 4.8 | `cad/module_params.py` (`SPIGOT_FIT`), `seals.md` §6 |
| Rod gland | 2 × 2-114 grooves Ø20.0, throat Ø15.93; polished seamless rod | `seals.md` §8 |
| Bayonet ramps | 0.4 mm rise over 40°; the disc springs work at ≤ 0.10 mm, so hold the ramp height to about ±0.02 mm (suggested) | `hot-swap.md` (ii) |
| Dowel holes | Ø6 H7 for m6 pins | `fasteners.csv` (93600A686) |
| Spigot OD and groove to the bore | concentric within ~0.05 mm (suggested; cut in one setup after welding) | – |

### Welding and honing (the M50 module body)

1. Turn the spigot from Ø4 in. 316L bar. Waterjet and turn the flange from 3/4 in. plate. Cut the cylinder from tube
   and the collar from plate or bar. Leave ≥ 0.5 mm on the bore diameter and on the spigot OD.
2. Tack the parts on a fixture with a copper or aluminium chill mandrel in the bore. TIG-weld the three circumferential
   seams with ER316L, short balanced passes, and an argon back-purge so the bore doesn't sugar. 316L shrinks at
   circumferential welds and pulls the bore in locally. That is why the bore is finished after welding, not before.
3. Optional stress relief: ME's Project Support Center lists heat-treat furnaces. Then, in one lathe setup on the
   tube's OD or a fixture:
   - face the spigot and flange;
   - turn the spigot OD and the radial groove;
   - bore to Ø50.80 −0.05.
4. Send it out for honing to H7 and Ra ≤ 0.4 µm. Check it with a bore gauge at three depths and two angles; the
   build plate's 0.15 mm cold gap is the margin.
5. Drill and tap the 6 × M4 collar holes and the flange's dowel and screw holes on the mill, located from the bore.

## BYU's shops

From public pages, fetched 2026-11-20 13:59-14:14 UTC.

| Shop | Who runs it | Published equipment |
|---|---|---|
| ME Prototyping Lab, EB 117 ([me.byu.edu/me-prototyping-lab](https://www.me.byu.edu/me-prototyping-lab); booking site [byuprojectslab.simplybook.me](https://byuprojectslab.simplybook.me/v2/)) | Students and faculty for class, club, capstone, research and personal projects. For CNC, a lab assistant programs the part from a STEP file and cuts it at a later appointment. | "DM1 and VF4 CNC mills"; manual mills; a collet lathe (< 1 in. stock), a Harrison lathe and a "Moriseiki or Kent" chuck lathe; waterjet; plasma table; CNC press brake; welding. **Haas VF-4: 50 × 20 × 25 in.** ([Haas](https://www.haascnc.com/machines/vertical-mills/vf-series/models/medium/vf-4.html)) |
| PF Manufacturing Shop, 108 CTB (formerly the PML; [pf.byu.edu](https://pf.byu.edu/transportation-and-manufacturing-services)) | Staff, fee-for-service by work order, open to all departments | "Multi-axis CNC mill"; "CNC lathe with live turret spindle capacity"; "Wire EDM"; GTAW, SMAW and GMAW welding, and laser micro-welding. No models or rates published. |
| MFGEN 101 CTB Machining Lab ([mfgen.byu.edu/101-lab-schedule](https://mfgen.byu.edu/101-lab-schedule)) | Manual machines only for students who took MFGEN 220 or ME EN 382; the TA or supervisor runs CNC, EDM, grinder and waterjet | lathes, mills, CNC, surface grinder, wire EDM, waterjet (fee), metal shear |
| MFGEN Foundry and Welding Lab, 140 CTB ([mfgen.byu.edu/weld-lab](https://mfgen.byu.edu/weld-lab)) | After a welding class or with proof of experience | SMAW, TIG and MIG |
| Physics & Astronomy shop ([news](https://physics.byu.edu/department/news/2020-08-new-mill-becomes-part-of-the-p-a-family)) | Department machinist; use by other departments not stated | **Haas VF-2SS** with 4th axis and probes, 30 × 16 × 20 in. ([Haas layout](https://haascnc.com/content/dam/haascnc/pdp_feed/mld/VF-2-2SS-2TR_MLD_11_2021.pdf)); Bridgeport knee mill |
| ME Project Support Center ([capstone.byu.edu](https://capstone.byu.edu/physical-prototyping-resources)) | Lends instruments | optical measuring microscopes, heat-treat furnaces |

- **Not found anywhere:** a honing machine, a CMM, a roughness tester, the waterjet makes, any welder model, any lathe
  swing, or machining rates.
- The page counting "three multi-axis CNC mills" is a
  [2019 Wayback copy](http://web.archive.org/web/20240811023217/https://pml.byu.edu/pml-research-support).
- Utah shops that list related work:
  - Wheeler Machinery (Salt Lake City): hydraulic-cylinder honing;
  - LACO Technologies (Salt Lake City): vacuum chambers, certified welders, helium leak test;
  - JawsTec (Lehi): stainless TIG on sheet.

Machine needs against these shops are in [`machines.csv`](machines.csv).

## Design changes that make it cheaper to machine

In order of payoff.

1. **Lid drawer slot (blocker).** Mill it from the lid's underside as an open pocket, 60 mm wide and 11 mm deep. Then
   widen its top 6 mm to 72 mm with a 1/4 in. keyseat (T-slot) cutter, which leaves 6 mm ledges for the drawer.
   - The 5 mm skin under the slot seals nothing: the drawer seals on the lid's front face, and the slot is already
     inside the gas envelope.
   - Or screw two 316 strips under an open slot.
   - As drawn it needs a 150 mm sinker-EDM electrode.
2. **Rail insert holes (blocker).** Keep every hole in the inside faces of the back and side walls within
   |x| ≤ 100 mm of the door opening, or mount the rail on a bar bolted through holes drilled from outside.
3. **Pocket corners and coves.** R5 × 120 mm deep needs a 3/8 in. tool at 12.6:1.
   - Use R ≥ 9.6 mm (3/4 in. × 6 in. end mill, 6.3:1, still a long-reach job) or R ≥ 12.7 mm (1 in., 4.7:1).
   - Make the floor coves match a stocked corner radius on a long tool (e.g. a 1/2 in. ball end, R6.35), or drop them.
   - The bigger saving is a **four-wall frame plus a bolted floor plate**. The pocket becomes a through-opening cut
     60 mm deep from each side with standard tools, the frame comes from 5 in. plate (120 mm walls), and the floor is
     a 20 mm plate. The cost is one more 3.53 mm face O-ring and 20 screws.
4. **Plates to stock thickness.** Make these dimensions match the plate as delivered, so only sealing faces are
   skimmed:
   - base plates 15 → 5/8 in. (15.9 mm) MIC-6, flat and ±0.13 mm thick as cast;
   - lid and door 16 / 15 → 5/8 in.;
   - optics bridge 25 → 1 in.

   That saves about 6 h of facing.
5. **Thin webs:**
   - lid inserts: use M4 inserts (OD 4.91 mm, 1.75 mm webs), or widen the wall by 3 mm;
   - heater block and piston head: ≥ 1.0 mm between holes;
   - striker counterbores: don't break out;
   - carriage-block bore: ≥ 1.5 mm wall;
   - module flange tabs: ≥ 2 mm past the holes.

   Drills wander (a rule of thumb is about 0.05 mm per 10 mm of depth), and inserts swell the wall when they go in.
6. **Window-flange screws in the lid.** Six M4 × 4 mm inserts on the Ø80 bolt circle end 0.5 mm above the drawer
   slot (0.7 mm web). Two fixes:
   - put the window flange's O-ring outside its bolt circle, so the screw holes sit inside the sealed area and a hole
     that cracks into the slot is harmless;
   - or space the holes unevenly so they miss the slot (|x| > 40 mm or y > 40 mm).
7. **Sharp internal corners** of the door opening (220 × 92 mm), the inlet slot (120 × 8) and the outlet and overflow
   slots: draw R ≥ 3.2 mm (1/4 in. tool), and give the mating plenums and funnel block the same radius.
8. **Half-dovetail grooves** are costly and tolerance-critical (`notes/2026-11-20-pain-points.md` P23). A plain
   rectangular groove with a moulded press-in seal avoids the dovetail cutter and its extra passes.
9. **Heater-block thermocouple holes:** Ø1.6 instead of Ø1.2 brings the depth ratio from 10.4:1 to 7.8:1
   (12.5 mm deep).

## Tooling

[`tooling-bom.csv`](tooling-bom.csv) lists one real product per tool, with vendor, part number, URL, price and fetch
time. Each row is flagged "usually on hand in a prototyping shop" or "buy for this job" and says which parts need it.

| Flag | Lines priced | Cost if bought |
|---|---|---|
| buy for this job | 41 (+ 2 unpriced) | **$3,661.88** |
| usually on hand in a prototyping shop | 48 | $5,132.39 |
| optional (only if that route is chosen) | 8 with a quantity (12 more listed at quantity 0) | $4,950.78 |

The biggest "buy" lines:
- SAE J1926 -4 port counterbore and step drill: $475.96;
- dial bore gauge 35-60 mm: $436.04;
- metric go/no-go thread plug gauges: $420.73 for M3, M4 and M6;
- 3/4 in. × 6 in. OAL end mill: $307.93;
- internal grooving tool and its quick-change holder: $353.19;
- CNMG inserts for 316L: $223.24;
- two dovetail O-ring cutters: $177.46;
- STI taps, drills and insert tools: $263.96 in all.

What the run found about the tools:
- **McMaster's STI taps are straight-flute only.** The BOM uses bottoming taps.
- **The installation tools also break off the prongs**, so the separate punches are optional.
- **No metric STI plug gauge is on McMaster** (inch only); it needs a gauge maker.
- **No 6 in. OAL uncoated 3/4 or 1 in. end mill was found.** McMaster's are AlTiN steel grades.
- **The widest Micro 100 internal groover is 1.57 mm**, so each 3.6 mm rod-gland groove takes three plunges.
- **The 1-1/4 in. boring bar reaches 127 mm**, which is enough for the M50 bore (about 90 mm).
- **Argon purge plugs or dams** for the module seams weren't priced; buy them from a welding supplier.


## Not checked

- Fixturing (how the chamber block is held for the ±X and ±Y setups).
- Chatter and deflection of the long tools.
- Thread-mill options.
- Ball and bull-nose tools in the simulation.
- The S25 and L75 modules (same features, other bore sizes).
- The hinges, latches and plenum screws, which `joints.py` doesn't draw yet.
- Any shop's real rates or queue.

Programming time and the removal rates are planning assumptions, not measurements.
