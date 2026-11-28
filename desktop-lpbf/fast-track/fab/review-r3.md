# Fab review, round 3: the CAM programs and the shop-hour allowances

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260), PR 294 round 3, 2026-11-28. This
is a review of this folder's programs and allowances, written the way a CAM programmer would check a job before it goes
on the machine. The reviewer is an agent, not a machinist. Nobody has timed a piece, and this review doesn't change
that. It checks what can be checked from here: the posted G-code, the feeds against the tool makers' charts, and the
allowances against published shop data.

What was run, all from the round-2 files as committed (`gcode/`, `out/cam.json`, `out/hours.json`, `tools.py`):

- **A G-code checker written for this review** (its own parser and interpreter, not `cam.py`'s or `sim.py`'s code).
  It ran on all 63 programs: 74,467 moves, of which 57,654 are feed moves and 3,637 arcs, with the G81/G83 cycles
  expanded.
- **An in-process stock model.** There is one voxel model per piece (0.12-0.70 mm), carried through its setups in
  order. Within each setup the tool's view is the top of the voxel columns, and each setup cuts that height field.
  It checks:
  - rapids against the material under the whole tool disc;
  - the wall next to each end mill against its flute length;
  - the holder, a disc of radius 14 mm for tools up to 6.6 mm and 20 mm above that (assumed), at the stick-out
    `tools.py` gives;
  - every rapid a second time as a Haas-style G00, where each axis runs at its own full rate.

  As a check on the model, the final voxel volumes are within 2 % of `pieces.json`'s volumes for 16 of the 21 pieces
  milled from a box blank. The other five are within 11 %: their lathe and hand features aren't in the G-code, or the
  voxels are coarse against a small piece.
- **A cycle-time recount** with trapezoidal velocity profiles and a look-ahead planner. It uses three machine
  settings (rapids 15-25 m/min, acceleration 2-5 m/s², junction deviation 0.01-0.05 mm) and an exact-stop bound.
- **Two literature sweeps,** one of tool makers' speed and feed charts and one of published setup, CAM and inspection
  times. Every source is listed at the end.

## Short answer

- **The programs are not safe to run on the Haas VF-4 as posted, but they are close.**
  - **The basics pass in all 63 programs:**
    - units (G21), plane (G17), absolute mode and G54;
    - a tool change, with a matching G43 H, before every operation, and in each of the 188 operations the tool in
      the spindle is the one `cam.json` lists;
    - the spindle on at `tools.py`'s speed before every feed move;
    - no F0;
    - flood coolant on;
    - every arc within LinuxCNC's radius rule (worst mismatch 0.002 mm);
    - an M2 at the end.
  - **What stops them running as posted:**
    - **Six setups can't be cut with the tools as `tools.py` defines them.** Either the holder reaches the part
      (MK-18a_A, MK-18a_B, MK-09b_C, MK-03_D) or the cut is deeper than the flutes (MK-03_A, MK-08e_A, MK-18a).
    - **On a Haas, 194 rapid links in 12 setups would cut material.** Haas runs a G00 as a dogleg, not a straight
      line, and these links go 0.8-4.6 mm off the straight line into the part or the stock.
    - **MK-02a_B's outline cuts the soft jaws that hold the piece.** Four more pieces re-cut, in their second setup,
      the full height of the faces a vise would hold.
    - **The 304 lead window (MK-06a/b) runs above both tool makers' charts for 304,** and plunges straight in.
  - **The fixes are in `cam.py`, `tools.py` and `parts.py`,** listed in [§7](#7-fixes-for-the-fab-worker).
- **Feeds and speeds are safe in 6061 and conservative.** The 8100 rpm spindle holds every small tool below the
  makers' surface speeds. The chip loads sit at the makers' slotting values even where the cut is a 12-15 % adaptive,
  which could feed 2-2.5 times faster. Cutting is 3.4 h of FT-1's 121.9 h, so this costs little either way.
- **Cycle time is not where the uncertainty is.**
  - **The parser checks out:** my recount of the posted programs is 205.8 min against the set's 205.1 min.
  - **Acceleration adds 5-10 % to the programs.** With 5-8 s tool changes and spindle starts, the FT-1 machine's mill
    time goes from 3.4 h to 3.7-4.0 h, so 0.3-0.6 h more.
  - **FreeCAD's own cycle times** (the set's high case) are 44 % above the recount.
- **The hours range is credible as a range, but its middle is off.**
  - **The low end (58.5 h for FT-1) leaves out 10-20 h:**
    - fixtures (three sacrificial plates, two sets of soft jaws, a ten-pocket plate for the discs);
    - loading and measuring the 20 tools;
    - sawing about 27 blanks;
    - the program fixes this review found.
  - **The expected 121.9 h counts the CAM as written from scratch,** though it is already written.
  - **The evidence supports these figures for the FT-1 machine** (a sensitivity, not a replacement):
    - **about 77-98 h** with the posted CAM reviewed, fixed and proven out, and a machinist doing the floor work;
    - **about 92-125 h** if a student does half the setups, lathe work and deburring at the pace a university
      teaching-shop sheet gives (typical time 1.7-2.0 times the goal).
  - **The set's high (189 h) is a fair ceiling.**
- **The five pieces most likely to run long** ([§6](#6-five-pieces-most-likely-to-take-longer-than-planned)):
  - MK-03, the well block;
  - MK-07, the rod gland;
  - MK-02a, the window ring;
  - MK-09b, the collimator saddle;
  - MK-11a/b, the nozzle and the collector.

## 1. Feeds and speeds

The machine is the one `tools.py` assumes: a Haas VF-4 with an 8100 rpm spindle and 22.4 kW, 122 Nm at 2000 rpm.
It has 16.5 m/min maximum cutting feed, 25.4 m/min rapids and a 20-pocket carousel (4.2 s tool to tool, 4.5 s chip to
chip) ([Haas VF-4, Wayback copy of 2025-11-06][haas-vf4]). The programs use exactly 20 tools (T1-T5, T7 and 14 drills),
so the whole library fits the carousel only if it stays loaded for the whole job.

Surface speed is vc = π·D·n. Chip load is fz = F/(n·z). For the adaptive passes, hex is the chip thickness after
radial thinning ([Sandvik formulas][sandvik-f]). "Used" is what the posted programs do, measured on the in-process
stock.

| Tool | n (rpm) | vc | fz | F (mm/min) | Used (ap, ae) | Makers' charts, wrought Al | Verdict |
|---|---:|---|---|---:|---|---|---|
| T1 2.5 in. face mill, 4 inserts | 3000 | 598 m/min (1963 SFM) | 0.102 mm (0.004 in.) | 1219 | ap ≤ 1.7 mm, ae up to 0.92 D | Haas HP-AL face mill, 6061: 3936 SFM (1200 m/min), fz 0.012 in. (0.30 mm) [haas-fm] | safe; about half the speed and a third of the chip load |
| T2 1/2 in. 3-fl carbide | 7600 | 303 m/min (995 SFM) | 0.076 mm (0.003 in.) | 1737 (plunge 869) | adaptive ae 12-15 % (worst 0.18 D), ap 12 mm (0.94 D), worst 14.6 mm; pockets 45 %, 6 mm; full width 670 mm in all; straight plunges up to 6.0 mm (0.47 D, MK-10c_A) | Harvey: 800-1500 SFM, 0.004 in. at 1/2 [harvey-g]. Helical H40ALV-3: 2100 SFM; slot 0.0029, rough 0.0054 (ap 1.25-2 D, ae 30-40 %), light roughing (ae 15-25 %) 0.0058-0.0079 in. [helical-3fl] [helical-old] | safe. hex at 15 % ae is 0.054 mm (0.0021 in.): no rubbing. The adaptives could feed 2-2.5 times faster (Helical's light-roughing load); the speed is spindle-limited |
| T3 1/4 in. 3-fl carbide, 1 in. flutes | 8100 | 162 m/min (530 SFM) | 0.038 mm (0.0015 in.) | 926 (463) | full slots 1442 mm in all at ap 3 mm (0.47 D); walls up to 23.4 mm (3.7 D) beside the tool; straight plunges 3.0 mm | Harvey 0.002 in. at 1/4. Helical: slot 0.0015, rough 0.0028; reduce for reach over 3 D. Haas HSAM2 slot 0.003 at 2000 SFM [haas-em] | safe. At Helical's slotting load; below the makers' surface speed (spindle-limited) |
| T4 1/8 in. 2-fl carbide, **in 6061** | 8100 | 81 m/min (265 SFM) | 0.020 mm (0.0008 in.) | 329 (165) | full slots in the plenums and windows (MK-11a/b), ap 1 mm | Helical slot 0.0008, rough 0.0014 in.; YG-1 EMK70 1095 SFM, slot 0.0015 in. [yg1] | safe, conservative |
| T4 1/8 in. **in 304** (MK-06a/b lead window) | 8100 | 81 m/min (265 SFM) | 0.020 mm (0.0008 in.) | 329 (165) | full slot (measured ae 1.0 D), 0.3 mm steps, a straight G1 Z plunge at every step | Harvey: 304 at 100-250 SFM [harvey-g]; YG-1, austenitic: 220 SFM, slot 0.0005 in. [yg1]. Harvey: a straight plunge "can easily lead to tool breakage"; ramp at 1-3° in ferrous metals [harvey-entry] | **over both charts** (speed 6-20 % over, chip load 1.6 times YG-1's) **and plunging: a likely broken tool.** Run it at about 5000 rpm (165 SFM) and 0.0005 in. (F about 125 mm/min), with a ramp or helical entry |
| T5 2.0 mm 2-fl carbide | 8100 | 51 m/min (167 SFM) | 0.013 mm (0.0005 in.) | 206 | O-ring grooves full width, ap 0.5 mm (0.25 D) | YG-1 EMK70 at about 2 mm: 1095 SFM, slot 0.0009 in. | safe; half the chart's load at 15 % of its speed (spindle-limited) |
| T7 1/2 in. 90° spot drill | 4000 | 160 m/min (524 SFM) at full diameter | 0.08 mm/rev | 320 | countersinks and spots | Haas carbide 142° spot drill: 543 SFM, 0.18-0.23 mm/rev at 1/2 in. [haas-spot] (no 90° chart found) | safe; the feed is 35-45 % of that chart |
| Drills 1.6-10 mm | min(8100, 60000/D) | 41-168 m/min (D ≤ 6.6); 188 m/min (9.6, 10) | 0.025·D, at most 0.15 mm/rev | 324-1215 | G83 at Q 0.75 D | Iscar IC608: 70-300 m/min; 0.10-0.25 mm/rev at Ø3-5, 0.15-0.35 at Ø5.1-8, 0.25-0.45 at Ø8.1-12 [iscar]. Haas Al drills: 200 m/min; 0.12-0.18 at 3 mm, 0.17-0.25 at 6, 0.24-0.30 at 10 [haas-drill] | safe; feeds at 50-70 % of the charts' low end. `tools.py`'s comment "~60-70 m/min" is wrong: the formula gives 188 m/min where the spindle allows it |

By operation type, as `cam.py` sets them up (ae is the radial step, ap the axial step):

| Operation (`cam.py`) | Tools | ae | ap | Entry | Verdict |
|---|---|---|---|---|---|
| Face (`MillFace`, bounding box) | T1, T2 | 70 % | to 2 mm (one or two passes) | from outside the stock | fine |
| Outside (`Adaptive`, outline) | T2 (T3 once) | 12 % | 12 mm (T2), 6 mm (T3) | helix, or from outside | fine; feed conservative; links are `G0` at depth ([§2](#2-the-g-code)) |
| Open pocket (`Adaptive`, inside) | T2, T4 | 15 % | 12 mm (T2), 2 mm (T4) | helix | fine |
| Pocket (`Pocket` 3D, offset) | T2, T3, T4, T5 | 45 % | 6 / 3 / 1 / 0.5 mm | straight plunge at half feed | fine in 6061; ramp preferred |
| O-ring groove (`Profile`, both wires) | T5 | full width | 0.5 mm (0.25 D) | straight plunge | fine |
| Through opening (`Profile` round the hole) | T3, T4 | full width (a slot round the slug) | 3 mm (T3), 1 mm (T4) | straight plunge | fine |
| Bore and counterbore (`Helix`) | T2, T3, T4 | 40 % | 1.0 mm a turn (0.5 for counterbores) | helix; but a sideways `G0` at the surface first | fine once `StartDepth` is raised ([§7](#7-fixes-for-the-fab-worker)) |
| Drill (`Drilling`, G83), countersink (G81) | drills, T7 | – | Q 0.75 D | – | fine; deep holes need long drills |
| Slide pocket raster (Custom, MK-02d) | T3 | 40 % | 0.6 mm | straight plunge at half feed | fine |
| Lead window (Custom, MK-06a/b, **304**) | T4 | full width | 0.3 mm | straight plunge | **too fast for 304** |

Macor (MK-03s) and the turning of the 304 rods and the 6061 discs are not programmed. Their minutes are `parts.py`
estimates, and [§4](#4-the-allowances-against-published-data)'s sensitivity takes them at 1.5-3 times.

- **Machinery's Handbook.** No reliable copy of Table 10 (31st ed., "Cutting Speeds and Feeds for Milling Aluminum
  Alloys") could be read, so no Handbook values are quoted; the makers' charts above stand in for it.
- **Power isn't a limit.**
  - **The largest removal rates** are 96 cm³/min (T1 facing MK-01) and 47 cm³/min (T2 adaptive, ae 2.3 mm × ap
    12 mm).
  - **Even at a high 1.2 J/mm³,** that is under 2 kW against the VF-4's 22.4 kW. No cut is near the torque curve.
- **Nothing rubs.** The thinnest chips are the 2 mm cutter's 0.013 mm in its full-width grooves and the T2 adaptive's
  0.054 mm after radial thinning. Both are well above the 3-8 µm edge radius of a sharp uncoated aluminium cutter (my
  estimate; no maker gives one).
- **Plunges.**
  - **What the programs do.** FreeCAD's `Pocket` and `Profile` enter with a straight G1 Z at half feed:
    - T2 makes them up to 6.0 mm deep (MK-10c_A, line 8787: the lens-bore pocket);
    - T3 makes them up to 3.0 mm deep (MK-03_B, MK-02a_B, MK-10c_B).
  - **What the makers say.** Centre-cutting end mills can plunge in aluminium at reduced feed. Harvey's entry guide
    still recommends a ramp (3-10° in non-ferrous metals) or a helix [harvey-entry]. That is not a safety stop at
    these depths in 6061, but a ramp entry would remove the risk.
- **Deep holes.** Sandvik says its solid-carbide drill needs internal coolant past 3 × D [sandvik-462]. The programs
  call flood coolant (`M8`) and peck, so through-spindle coolant isn't assumed. Six holes are deeper than 5 × D and
  need long-series drills:

  | Setup | Drill (mm) | Depth (mm) | Depth/D | Line |
  |---|---|---:|---:|---:|
  | MK-03_D | 2.0 | 31.6 | 15.8 | 25 |
  | MK-04_A | 2.0 | 26.5 | 13.2 | 25 |
  | MK-15c_C | 3.4 | 31.5 | 9.3 | 25 |
  | MK-03_C | 6.4 | 41.9 | 6.5 | 25 |
  | MK-15c_A | 4.5 | 26.9 | 6.0 | 536 |
  | MK-04_C | 2.5 | 13.8 | 5.5 | 25 |

  - **`tools.py` gives the 2.0 mm drill a 30 mm length.** At that length its holder reaches the well block 1.7 mm
    before MK-03_D's hole is deep enough.
  - **Every posted G83 pecks at Q = 0.75 D, whatever the depth.** `cam.py` sets `PeckDepth` to 1.0 D or 0.5 D, but
    FreeCAD 1.0.2 binds `PeckDepth` to the expression `OpToolDiameter*0.75` (`Path/Op/Drilling.py`, line 331), and
    `cam.py` clears only the `RetractHeight` expression. 0.75 D is fine to 5 × D; the six deep holes should get 0.5 D,
    as `cam.py` meant.

## 2. The G-code

The checker parsed every posted program with its own interpreter. It ran each check below on all 63 programs, and the
in-process checks against the voxel stock.

| Check | Result |
|---|---|
| Units, plane, distance mode, work offset before the first move | pass, all 63 (`G17 G54 G40 G49 G80 G90`, `G21`) |
| A tool change before each operation, with the tool `cam.json` lists | pass: 188 of 188 operations; 138 tool changes, each followed by `G43 H` with the same number |
| Spindle on, at `tools.py`'s speed, before the first feed move | pass. `M3 S` follows every `M6`. No dwell is programmed after `M3`, so the machine's own spindle-at-speed check has to hold the first feed (LinuxCNC waits only if its at-speed signal is wired) |
| No feed move at F0 or without F | pass; the feeds are exactly `tools.py`'s horizontal and half-feed vertical values |
| Arcs (3,637; the LinuxCNC rule: no mismatch over 0.5 mm, or over 0.005 mm and 0.1 % of the radius) | pass; worst start/end radius mismatch 0.002 mm |
| Rapids into material, straight-line rapids (LinuxCNC) | pass. The only hits are helix starts at the exact height of the surface: MK-09b_C lines 2424-2578 (0.13 mm) and MK-15c_C lines 51 and 105 (0.06 mm), both within the voxel size |
| Rapids into material, Haas-style G00 (each axis at its own full rate: a dogleg) | **fail: 194 moves in 12 setups** (next table) |
| Rapids at zero clearance | 206 lateral `G0` moves in 20 setups are at the exact height of the surface they start from: every `Helix` bore and counterbore rapids to `StartDepth`, then sideways. The surface is as-supplied (not faced) in MK-14_B (lines 25, 79, 133, the Ø20 rod hole in the Ideal Vacuum plate), so a plate thicker than nominal is hit at rapid. 11,874 `Adaptive` link moves run at zero lift over the floor just cut |
| Deepest cut against flute length (wall beside the tool) | **fail in 8 setups**: four by 7-20 mm, four by 0.05-0.95 mm (next table) |
| Holder against the in-process stock, at `tools.py`'s stick-out | **fail in 4 setups**, tight in one (next table) |
| Program end | `M5` and `M9` before `M2` in all 63. A Haas program ends with `M30`, and files usually start and end with `%`: post with a Haas or Fanuc post, or edit them |
| Work offset | not a fault, but a setup risk. The G54 origin is the piece's model origin. It is outside the stock in 20 setups, and Z0 is more than 1 mm from the stock top in 54 (from −26 to +65 mm). Each setup needs a sheet giving the offset from a datum the operator can touch off |
| First move after a tool change | the hand-written Custom op (MK-06a_A and MK-06b_A, line 21) moves X and Y before any Z move. It relies on the tool-change height; add a `G0 Z` first |

**The programs with problems, by file and line:**

| Program | Line | Problem | What it needs |
|---|---|---|---|
| MK-18a_A, MK-18a_B | 415-540 (outline adaptive) | T2 cuts the outline 50.4 / 51.7 mm deep. That is past its 32 mm flutes, and its 45 mm stick-out puts the holder 5.4 / 6.7 mm into the stock. B re-cuts A's full outline, almost all in air | split the depth: A to about z 25, B to meet it; or a 1/2 in. tool with 2 in. flutes and 55 mm stick-out |
| MK-09b_C | 2423-2578 (counterbores 9.5 × 5.5 at x −94) | the counterbores sit on the saddle's 12 mm foot, 1.25 mm from a wall 34.8 mm tall. A 1/8 in. cutter would need 42 mm of stick-out and a holder under 12 mm across: **it can't be cut as drawn** | a design change in `parts.py`: tap the foot and screw up from under the head plate, or move the holes 6 mm or more from the wall and counterbore with a 3/8 in. long-reach tool |
| MK-03_D | 25 | 2.0 mm drill, 31.6 mm deep; `tools.py`'s 30 mm length can't reach | a long-series 2.0 mm drill (DIN 340 class, about 55 mm of flute) and Q 1.0 |
| MK-03_A | 696 (Ø40 H7 rough helix to z −0.5) | T2 goes 40.5 mm deep in the bore, past its 32 mm flutes. The shank rubs the top 8.5 mm of the bore | rough from both sides (A and B, 21 mm each) or use a 1/2 in. cutter with 1-3/4 in. flutes or a necked shank |
| MK-08e_A | 5367 (outline) | T2 cuts a 39.0 mm wall with 32 mm of flute | split the depth (A and B already overlap) or use a long-flute tool |
| MK-10c_B, MK-15c_A, MK-11b_A, MK-09b_C | 6012; 451; 395; 2504 | the wall beside the tool equals or just passes the flutes: T2 32.05 / 32.0, T3 25.5 / 25.4, T4 10.0 / 9.5, T4 10.45 / 9.5 | 1-2 mm less depth per setup, or the next flute length up |
| MK-02a_B | 4822 | T5 at its 10 mm stick-out leaves the holder 0.7 mm above the ring | 15 mm stick-out |
| MK-02a_B | 82-4584 (outline, z 12 to −0.3) | the piece is held "in soft jaws on the OD" (`pieces.json`), but the outline cuts the full 12.3 mm round the OD, through the jaws. Setup A had already cut the lower 6 mm | stop B's outline at about z 5.5 |
| MK-07_B, MK-15b_B, MK-15c_B, MK-18a_B | outline ops | A cuts the outline to 1-3 mm above the bottom, then B, flipped, cuts the full height again. That passes through the faces a vise holds in B | B's outline only through the remaining skin plus 0.5 mm; or B on a sacrificial plate |
| MK-06a_A, MK-06b_A | 21-35 | T4 in 304 at S8100 F329 with straight plunges ([§1](#1-feeds-and-speeds)); an XY move before any Z move | a 304 tool controller (about 5000 rpm, F about 125, ramp entry) and a `G0 Z` first |
| MK-14_B | 25, 79, 133 | helix rapids at Z0.000 across an unfaced plate | `StartDepth` at the surface + 1 mm (every Helix op) |

**Haas G00 (dogleg) rapids.** Haas's G00 reference says each axis moves at its own maximum rate and the axes need not
finish together, so a G00 is not a straight line ([Haas G00][haas-g00]; the page refuses automated fetches, so this was
read through a search summary). Autodesk's Haas post states it directly: "By default positioning moves will be output
as high feed G1s instead of G0s", and with G0 forced "the CNC will follow a dogleg path rather than a direct path"
([Autodesk Haas post][autodesk-haas], read 2026-11-28). FreeCAD's `Adaptive` writes its "LinkClear" moves
as `G0 X Y` at the depth just cut (`Path/Op/Adaptive.py` lines 565-570, `LiftDistance` 0 by default). Replayed as
doglegs on the in-process stock:

| Setup | Links that hit | Furthest off the straight line | Example lines |
|---|---:|---:|---|
| MK-08e_A | 80 | 4.6 mm | 4914, 6683 |
| MK-09b_B | 26 | 2.8 mm | 478, 1250 |
| MK-08e_B | 24 | 3.4 mm | 774, 1386 |
| MK-10c_B | 18 | 1.1 mm | 882, 1957 |
| MK-10c_A | 12 | 1.1 mm | 4875, 7793 |
| MK-11b_B | 12 | 1.1 mm | 708, 1815 |
| MK-02a_B | 6 | 0.9 mm | 584, 2832 |
| MK-02b_B, MK-02c_A | 4 each | 0.9 mm | 557, 2028 |
| MK-02a_A, MK-02e_A | 3 each | 0.9 / 1.2 mm | 584; 1318 |
| MK-02d_A | 2 | 1.2 mm | 1318 |

At 25 m/min a 1/2 in. cutter that takes 0.3 mm off a wall sees a chip of about 0.3 mm a tooth. That is several times
the makers' roughing load: a gouge on the finished wall at best. With straight-line rapids (LinuxCNC, the post's
target) none of these moves touches material. The fix is one line in `cam.py`'s post step: rewrite `G0` moves with
only X and Y below the operation's safe height as `G1` at a high feed (5000 mm/min, say), as Autodesk does.

## 3. Cycle time

The same 63 programs, recounted three ways. Every count multiplies by the piece quantity, and every time is in
minutes.

| | Programs (min) | FT-1 machine (h, with tool changes) |
|---|---:|---:|
| The set's recount (feeds as programmed, rapids 25.4 m/min, no acceleration; 4.2 s tool change) | 205.1 | 3.42 |
| This parser, same assumptions | 205.8 | – |
| Trapezoid, 25 m/min, 5 m/s², junction deviation 0.05 mm; 5 s tool change + 2 s spindle start | 216.8 | 3.73 |
| Trapezoid, 20 m/min, 3 m/s², 0.02 mm | 221.3 | – |
| Trapezoid, 15 m/min, 2 m/s², 0.01 mm; 8 s tool change + 2 s spindle start | 226.0 | 4.00 |
| Exact stop at every block, 15 m/min, 2 m/s² | 236.5 | 4.17 |
| FreeCAD's own cycle time (the set's high case) | 295.5 | 4.88 |

- **Where the extra time goes.** It sits in the programs with many short moves:
  - MK-10c: 21.5 → 24.4-26.4 min;
  - MK-08e: 5.8 → 6.8-7.6 min;
  - MK-18a: 3.2 → 3.6-4.0 min.

  The plate programs barely move: MK-09a is 23.8 → 24.0-24.3 min.
- **Per piece** (minutes, quantities included; "trapezoid" is the 25 m/min, 5 m/s² and 15 m/min, 2 m/s² settings):

  | Piece | Setups | Tool changes | The set's recount | This parser, flat | Trapezoid | Exact stop | FreeCAD |
  |---|---:|---:|---:|---:|---|---:|---:|
  | MK-01 | 2 | 11 | 16.9 | 16.9 | 17.2-17.6 | 17.8 | 23.3 |
  | MK-02a | 2 | 7 | 24.1 | 24.1 | 25.3-26.1 | 27.2 | 29.7 |
  | MK-02b | 2 | 8 | 6.7 | 6.7 | 7.2-7.7 | 8.0 | 10.1 |
  | MK-02c | 1 | 3 | 3.8 | 3.8 | 4.3-4.6 | 5.0 | 6.0 |
  | MK-02d | 1 | 3 | 4.4 | 4.4 | 4.8-5.0 | 5.9 | 7.5 |
  | MK-02e | 1 | 2 | 2.0 | 2.0 | 2.3-2.4 | 2.7 | 3.1 |
  | MK-03 | 4 | 9 | 10.4 | 10.4 | 10.8-11.2 | 11.4 | 15.2 |
  | MK-04 | 3 | 4 | 0.3 | 0.3 | 0.4-0.6 | 0.6 | 0.6 |
  | MK-05 (× 10) | 1 | 20 | 1.2 | 1.3 | 1.8-2.2 | 2.2 | 4.8 |
  | MK-06a, MK-06b | 2 + 2 | 4 | 0.6 | 0.6 | 0.6 | 0.6 | 1.7 |
  | MK-07 | 2 | 5 | 12.2 | 12.3 | 12.4-12.5 | 12.6 | 13.2 |
  | MK-08c | 3 | 5 | 3.7 | 3.7 | 3.8-3.9 | 3.9 | 5.0 |
  | MK-08d | 3 | 5 | 0.9 | 1.0 | 1.0-1.1 | 1.1 | 1.7 |
  | MK-08e | 3 | 6 | 5.8 | 5.8 | 6.8-7.6 | 9.2 | 10.6 |
  | MK-09a | 2 | 5 | 23.8 | 23.9 | 24.0-24.3 | 24.6 | 39.0 |
  | MK-09b | 3 | 6 | 8.1 | 8.1 | 8.7-9.2 | 10.3 | 10.9 |
  | MK-10c | 3 | 6 | 21.5 | 21.6 | 24.4-26.4 | 29.3 | 31.6 |
  | MK-11a | 4 | 7 | 11.7 | 11.8 | 12.1-12.4 | 12.6 | 18.3 |
  | MK-11b | 4 | 7 | 11.4 | 11.4 | 11.9-12.3 | 12.6 | 18.9 |
  | MK-13 | 2 | 3 | 5.9 | 5.9 | 6.1-6.2 | 6.3 | 6.8 |
  | MK-14 | 2 | 4 | 3.7 | 3.7 | 3.9-4.1 | 4.1 | 5.0 |
  | MK-15a | 2 | 6 | 11.5 | 11.5 | 11.6-11.8 | 11.9 | 11.7 |
  | MK-15b | 2 | 4 | 4.0 | 4.0 | 4.2-4.4 | 4.4 | 4.8 |
  | MK-15c | 3 | 8 | 6.1 | 6.2 | 6.5-6.7 | 6.9 | 9.3 |
  | MK-16 | 2 | 3 | 1.1 | 1.1 | 1.1-1.2 | 1.2 | 1.4 |
  | MK-18a | 2 | 5 | 3.2 | 3.2 | 3.6-4.0 | 4.1 | 5.1 |
  | **All** | **63** | **156** | **205.1** | **205.8** | **216.8-226.0** | **236.5** | **295.5** |

- **What it means for the hours.** The recount is not a source of error worth chasing: on the FT-1 machine the
  difference is 0.3-0.6 h, against 121.9 h.
- **The real lever on cutting time is the feeds.** At the makers' chip loads the adaptives would cut about 40 % less
  time. That saves about 1 h on FT-1, which still doesn't matter.

## 4. The allowances against published data

| Allowance | The set: low / expected / high | Published | Reading |
|---|---|---|---|
| Mill setup | 20 / 45 / 90 min a setup (75 / 120 min over 200 mm) | **MMS Top Shops medians** ("last good piece to first good piece", whole job changeovers in production shops) [mms-2015] [mms-2014] [mms-2013] [mms-2012] [mms-2011]:<br>- 2015: 90 min top shops, 68 min others<br>- 2014: 37 vs 60 min<br>- 2013: 52.5 vs 60 min<br>- 2012: 2 vs 3 h<br>- 2011: 2.5 vs 3.5 h<br>**Other sources:**<br>- re-clamping a small part in a vise: 2 min [das]<br>- indicating a vise: about 30 min [mms-fix]<br>- a workholding change by standard methods: 20 min [kurt]<br>- setting a tool by hand: about 5 min [mmt-preset]<br>- university students' first-time mill setup: 10 / 21 / 28 min (goal / typical / max) [ufl] | "68-90 min median" is two medians from one year (2015): 68 for the other shops, 90 for the top shops. Both are whole job changeovers, which include loading tools and proving out. For one-off pieces from one loaded tool library, these sources are consistent with 30-60 min for a piece's first setup and 15-30 min for its second to fourth (a flip or a side face, same tools). The set charges 45 min for every setup, including the flips |
| CAM | low 0.7 h a piece; expected 0.5 + 0.6 a setup + 0.015 a hole (+1 if turned) | - "a Senior CAM Programmer usually takes an hour to program a part with a variety of features" in Fusion 360 [cloudnc]<br>- an estimator's default of 10 min per feature [gwiz] | The expected formula gives 61.5 h for 35 pieces (1.8 h a piece). That is above an experienced programmer's 1 h a part, but reasonable for a student in FreeCAD. **The CAM is already written.** What remains is review and prove-out (the set's 0.25 h a setup, an assumption) plus this review's fixes (3-6 h) |
| Deburr and inspection | 0.25 h a piece; 1 h with a sealing face | - deburring: 2.8 min a part in a worked example [cte]<br>- AS9102 first-article reports: 2-5 h, but that is aerospace paperwork [qm] | Reasonable. The 1 h covers MK-03's H7 bore with a bore gauge, the 0.01-0.02 mm flatness checks on a surface plate and the finish checks |
| Tool change | 4.2 s | VF-4: 4.2 s tool to tool, 4.5 s chip to chip [haas-vf4] | fine; 4.5 s plus spindle start changes little ([§3](#3-cycle-time)) |
| Remakes | none / none / three pieces made twice | scrap and rework medians 1.5-2.2 % of parts in production shops [mms-2011]; an estimator's default 5 % scrap [gwiz]; no published figure for one-off tight-tolerance parts | the high case's three remakes is a ceiling; an expected 0.5-1 remake (3-5 h) is easier to defend |
| Student pace | not modelled | a university teaching shop's sheet for undergraduates on manual machines: mill part 102 / 201 / 264 min and lathe part 95 / 160 / 195 min (goal / typical / max); typical is 1.7-2.0 times the goal [ufl] | the closest published student factor found. No published student-to-professional factor was found |
| Not counted at all | – | – | **fixtures:**<br>- FX-1, the ten-pocket plate for MK-05;<br>- sacrificial plates under MK-01_B, MK-09a_B and MK-15a_B;<br>- soft jaws for MK-02a_B (OD) and MK-10c_B (ID);<br>- lathe soft jaws for MK-04 and MK-05.<br>**Other items:**<br>- loading and measuring the 20 tools (about 5 min each);<br>- sawing about 27 blanks (only MK-07, MK-10a/b and MK-15c's slit are counted);<br>- the fixes in [§7](#7-fixes-for-the-fab-worker) |

**A sensitivity for the FT-1 machine (cumulative S1 to FT-1), not a replacement:**

| Item | h | Basis |
|---|---:|---|
| Setups | 33.2-41.5 | a piece's first mill setup at the set's 0.75 h (1.25 h over 200 mm); further setups of the same piece at 0.25-0.5 h; lathe 0.5 h |
| CAM (programs exist) | 14.8 | 0.25 h a mill setup to review and prove out (the set's assumption), 0.25 h a lathe-only piece |
| Mill run | 4.1-4.4 | the set's 3.8 h, plus this review's 0.3-0.6 h |
| Lathe and hand work | 2.3-4.5 | the set's estimates × 1.5-3: manual lathe, measuring to ±0.025 mm |
| Deburr and inspection; sheet parts | 8.6; 3.9 | as the set |
| Fixtures, tool library, sawing, CAM fixes | 10-20 | 4-8 + 1-2.5 + 2-4 + 3-6 (estimates) |
| **Machinist** | **77-98** | the set's "CAM taken as done" figure is 83.8 h |
| A student doing half the setups, lathe and deburring at 1.7-2.0 × | +15-27 | [ufl] |
| **Machinist and student** | **92-125** | the set's expected is 121.9 h |

**What the sensitivity says about the set's range:**

- **The set's low (58.5 h)** charges every setup 20 min and leaves out the uncounted items. It is about 20 h too low
  to be a real floor.
- **The set's expected (121.9 h)** sits at the top of the machinist-and-student band.
- **The set's high (189.3 h)** stays a fair ceiling: fresh CAM, 90 min setups and three remakes.

For the schedule, 90-120 h for FT-1 with the programs fixed is the defensible middle. A BYU machinist's quote on
three pieces (the set suggests MK-03, MK-07 and a small bracket) would still pin it better than any of this.

## 5. What a machinist would ask before starting

These are not program faults. They are what sets the setup times, and what turns a 45 min setup into 2 h:

- **A setup sheet for every setup.** It gives the G54 position against a datum the operator can touch off, the stock
  size and the holding, the tools with their stick-outs, and the first-article dimensions. None exists. In 54 of 63
  setups Z0 is not the stock top, and in 20 the XY origin is outside the stock.
- **Workholding for the through-cut thin plates.** The fixtures are not drawn:
  - MK-02b_B, MK-02c_A, MK-02d_A and MK-02e_A are 4.4-6.35 mm plates whose outline goes through (to −0.3 mm), and
    `pieces.json` gives no holding;
  - MK-11a_B, MK-11b_B and MK-16_A are cut through the same way.

  Each needs tabs, a sacrificial plate with screws, or double-sided tape with a light finish pass.
- **Thin features.**
  - MK-08e: a 3 mm foot under an 8 mm web, cut from 2 in. bar "41 mm out" of the vise;
  - MK-11a/b: a 2 mm front wall with a 45-50 mm slot through it, and 1.5 mm walls round the plenums;
  - MK-02e: a 4.4 mm plate with a slide pocket.

  Thin walls chatter and move when released. Expect lighter finishing passes than programmed and a second look at
  flatness.
- **Tilted and side setups.** Thirteen setups stand a piece on its end or side, in the vise or a V-block:
  - MK-03_C and _D;
  - MK-04_C;
  - MK-06a_B and MK-06b_B (the tube turned 90° in the V-block);
  - MK-08c_C, MK-08d_C;
  - MK-10c_C;
  - MK-11a_C and _D, MK-11b_C and _D;
  - MK-15c_C.

  Each needs the part squared to the table (indicated) and a Z0 on a small face. These are the setups that take
  20 min more than a flip.

## 6. Five pieces most likely to take longer than planned

| Piece | The set's expected h | Why it will run long |
|---|---:|---|
| **MK-03, the well block** | 6.7 | Four setups, two of them side setups (6.4 mm heater holes 42 mm deep, a 2.0 mm thermocouple hole 31.6 mm deep, 15.8 × D). The Ø40.000-40.025 H7 bore has cylindricity 0.01, Ra 0.8 and is square to the top within 0.02, over 40 mm of depth: several boring-head passes, each measured with a bore gauge, not "10 min". The top face has flatness 0.02 and height 40.00 ± 0.02. Its rough bore needs a longer cutter than T2 ([§2](#2-the-g-code)). A broken 2 mm drill in the thermocouple hole scraps a piece with four setups in it. The set's own high case makes it twice |
| **MK-07, the rod gland** | 6.0 | A sawn 64 mm square indicated in a 4-jaw (15-30 min before the first cut). A 12.95 +0.05/0 throat, then two internal grooves Ø17.15-17.20 × 3.56-3.68 inside it: an internal grooving tool in a 13 mm bore is small, slow and hard to measure. Concentricity 0.03. It goes back to the mill for a face groove and counterbores, and B's outline re-cuts the held faces ([§2](#2-the-g-code)) |
| **MK-02a, the window ring** | 4.7 | The window seat floor needs flatness 0.01 and 16 RMS, with a face O-ring land under fused silica; the base O-ring land is the same. Each groove is cut with a 2 mm cutter in two profiles. The soft jaws on the OD have to be made, and B's outline must be shortened so it doesn't cut them. Sealing faces mean a light finishing pass, a surface-plate check, and likely a second try |
| **MK-09b, the collimator saddle** | 5.0 | The bar stands 44.45 mm tall in the vise for the L profile, with 26 link rapids that a Haas would run into the part. The slot edges are held at ±0.05 mm because they set the collimator axis. Its counterbores can't be cut as drawn ([§2](#2-the-g-code)), so the piece changes before anyone can start |
| **MK-11a and MK-11b, nozzle and collector** | 6.4 each | Four setups each, two of them on end in the vise (front face, boss). There is a 2 mm front wall with a 45-50 mm slot or window cut through it with the 1/8 in. cutter, open plenums 8-10 mm deep, and thin slivers that the round-2 voxel check showed the outline leaves (up to 2.8 mm). A 0.33 mm gouge on MK-11b is still open. Thin walls and small parts on end are where chatter and re-fixturing eat time |

Next in line: MK-08e (a 3 mm foot on an L cut 39 mm deep, 80 dogleg links) and MK-18a (a 51 mm deep outline the set's
tools can't reach).

## 7. Fixes for the fab worker

In `cam.py`:

1. **Helix start height.** For every bore and counterbore, set `StartDepth` 1 mm above the surface. As posted, 206
   rapids in 20 setups move sideways at the surface's exact height.
2. **Adaptive links.** After posting, rewrite every `G0` with only X and Y below the operation's safe height as `G1`
   at a high feed (about 5000 mm/min). `LiftDistance` or a lower `KeepToolDownRatio` alone doesn't fix it: the
   direct links stay `G0` beside the walls. As posted, 194 links in 12 setups hit material on a Haas.
3. **Peck depth.** Call `op.setExpression("PeckDepth", None)` before setting `PeckDepth`. Every G83 is now
   Q = 0.75 D, against `cam.py`'s intended 1.0 D or 0.5 D.
4. **Outline depths and the holding.**
   - On flipped pieces, cut B's outline only through what A left, plus 0.5 mm: MK-02a, MK-07, MK-15b, MK-15c and
     MK-18a.
   - Split MK-18a's 51 mm outline and MK-08e_A's 39 mm one between the two setups.
   - Rough MK-03's bore from both sides.
5. **Ramp entries.** Ramp or helix into `Pocket` and `Profile` instead of plunging straight down (T2 6 mm, T3 3 mm).
6. **Setup sheets and the post.**
   - Put each setup's G54 on a datum the operator can touch off (the stock top centre, or a corner), and write a
     setup sheet with the offset, stock, holding, tools and stick-outs.
   - Post with a Haas or Fanuc post (`%`, `M30`), or prove out on the Haas's graphics first.

In `tools.py`:

7. **The tool library.**
   - **T2:** add a 1/2 in. long-flute cutter (about 2 in. of flute, at least 55 mm stick-out) for MK-03_A, MK-08e_A
     and MK-18a, or keep every depth within 30 mm.
   - **T5:** give it 15 mm of stick-out.
   - **Drills:**
     - Give each drill a flute length and a stick-out.
     - Use a long-series 2.0 mm drill for MK-03_D and MK-04_A.
     - Use jobber or 8 × D drills for MK-15c_C (3.4 mm), MK-03_C (6.4 mm), MK-15c_A (4.5 mm) and MK-04_C (2.5 mm).
     - Correct the drills' "~60-70 m/min" comment.
   - **304:** add a tool controller for MK-06a/b's lead window (T4 at about 5000 rpm and F 125 mm/min, ramp entry).
   - **Feeds (optional):** raise the adaptive chip loads toward Helical's light-roughing values (T2 about 0.006 in.).
     This saves about 1 h on FT-1.

In `parts.py`:

8. **MK-09b's counterbores.** The holes A sit 1.25 mm from a wall 34.8 mm tall. Tap the foot and screw up from under
   the head plate, or move the holes 6 mm or more from the wall.
9. **MK-02b/c/d/e, MK-11a/b and MK-16.** Record how each through-cut plate is held (tabs, a sacrificial plate or
   tape). Add the fixtures to `hours.py`:
   - FX-1;
   - three sacrificial plates;
   - two sets of soft jaws;
   - lathe soft jaws.

   Add 4-8 h for them, as an estimate.

## Sources

All read 2026-11-28 (UTC) unless noted. The Haas pages refuse automated fetches; their specs were read from Wayback
copies.

- [haas-vf4]: Haas VF-4 specifications, Wayback copy of 2025-11-06,
  https://web.archive.org/web/20251106035848/https://www.haascnc.com/machines/vertical-mills/vf-series/models/medium/vf-4.html
- [haas-g00]: Haas mill G-code reference, G00,
  https://www.haascnc.com/service/codes-settings.type=gcode.machine=mill.value=G00.html
- [autodesk-haas]: Autodesk's Haas post processor, https://cam.autodesk.com/posts/post.php?name=haas
- [harvey-g]: Harvey Tool, General Machining Guidelines, https://www.harveytool.com/resources/general-machining-guidelines
- [helical-3fl]: Helical Solutions, H40ALV-3 speeds and feeds,
  https://harveyperformance.widen.net/content/bujcsxkuoz/original/SF_H40ALV-3.pdf
- [helical-old]: Helical aluminium parameters, an older catalogue page hosted by a reseller,
  https://cdn.shopify.com/s/files/1/0612/0733/files/Helical_Aluminum_Parameters.pdf
- [haas-em]: Haas Tooling HSAM2 end mills, speeds and feeds,
  https://www.haascnc.com/content/dam/haascnc/ecommerce-assets/linedrawings/milling/end_mills/speeds-and-feeds/03-0564%20to%2003-0587%20end%20mills,%20hsam2,%20speeds%20and%20feeds,%20inch.pdf
- [yg1]: YG-1 miniature end mill speeds and feeds (EMK70),
  https://www.yg1usa.com/downloads/Miniature_End_Mill_Speeds_and_Feeds.pdf
- [harvey-entry]: Harvey Performance, "Most Common Methods of Tool Entry" (2017),
  https://www.harveyperformance.com/in-the-loupe/types-tool-entry/
- [sandvik-f]: Sandvik Coromant, milling formulas and definitions,
  https://www.sandvik.coromant.com/en-gb/knowledge/machining-formulas-definitions/milling-formulas-definitions
- [haas-fm]: Haas "High Performance AL" face mill speeds and feeds,
  https://www.haascnc.com/content/dam/haascnc/ecommerce-assets/speeds-and-feeds/High%20Performance%20AL%20Speeds%20and%20Feeds.pdf
- [haas-spot]: Haas carbide 142° spot drills, speeds and feeds,
  https://haascnc.com/content/dam/haascnc/ecommerce-assets/linedrawings/holemaking/spot_drills/speed---feeds/03-2222%20to%2003-2231%20Carbide%20Speeds%20and%20Feeds,%20Landscape%20142%20Deg%20Spot%20Drills.pdf
- [iscar]: Iscar IC608 solid carbide drill data, https://www.iscar.com/eCatalog/Ecat/datafileENM/INFO/4714.pdf
- [haas-drill]: Haas Tooling aluminium drills, speeds and feeds,
  https://www.haascnc.com/content/dam/haascnc/ecommerce-assets/speeds-and-feeds/Speeds%20and%20Feeds%20AL%20Drills%20editable.pdf
- [sandvik-462]: Sandvik CoroDrill Dura 462,
  https://www.sandvik.coromant.com/en-us/tools/solid-round-tools/solid-carbide-drills/corodrill-dura-462
- [mms-2015]: Modern Machine Shop, "Best Practices of Top U.S. Shops" (2015),
  https://www.mmsonline.com/articles/best-practices-of-top-us-shops
- [mms-2014]: Modern Machine Shop, "What it takes to be a Top Shop",
  https://www.mmsonline.com/articles/what-it-takes-to-be-a-top-shop
- [mms-2013]: Modern Machine Shop, "Top Shops' secrets to success",
  https://www.mmsonline.com/articles/top-shops-secrets-to-success
- [mms-2012]: Modern Machine Shop, "Top machining strategies and equipment",
  https://www.mmsonline.com/articles/top-machining-strategies-and-equipment
- [mms-2011]: Modern Machine Shop, "See how you stack up", https://www.mmsonline.com/articles/see-how-you-stack-up
- [mms-fix]: Modern Machine Shop, "Quick-change fixturing locks in time, cost savings" (2011),
  https://www.mmsonline.com/articles/quick-change-fixturing-locks-in-time-cost-savings
- [kurt]: American Machinist, "Zero-point clamping system aligns instantly" (2013),
  https://www.americanmachinist.com/machining-cutting/article/21898295/zeropoint-clamping-system-aligns-instantly
- [mmt-preset]: MoldMaking Technology, "Using presetters to reduce machine idle time" (2018),
  https://www.moldmakingtechnology.com/articles/using-presetters-to-reduce-machine-idle-time
- [das]: Das, Gupta and Nau, setup-cost estimation (University of Maryland, about 1995), citing Wilson and Harvey,
  *Manufacturing Planning and Estimating Handbook* (1963), https://www.cs.umd.edu/~nau/papers/das1995estimation.pdf
- [ufl]: University of Florida MAE design lab, teaching-assistant part time estimates,
  https://web.mae.ufl.edu/designlab/TA/Assigned%20Parts%20Time%20Estimates.pdf
- [cloudnc]: CloudNC, CAM Assist beta feedback (2023), https://cloudnc.com/blog/cam-assist-beta-feedback
- [gwiz]: CNCCookbook G-Wizard CAD/CAM estimator guide,
  https://s3.amazonaws.com/s3.cnccookbook.com/GWCalcCADCAMEstimator.htm
- [cte]: Cutting Tool Engineering (2009), deburring example, https://ctemag.com/?p=95145
- [qm]: Quality Magazine, "How to simplify your AS9102 first article inspection process" (2021),
  https://www.qualitymag.com/articles/96602-how-to-simplify-your-as9102-first-article-inspection-process
- FreeCAD 1.0.2 source as shipped in the AppImage: `Mod/CAM/Path/Op/Drilling.py` (the `PeckDepth` expression,
  line 331) and `Mod/CAM/Path/Op/Adaptive.py` (link moves, lines 565-577; `LiftDistance` 0, line 1098)

[haas-vf4]: https://web.archive.org/web/20251106035848/https://www.haascnc.com/machines/vertical-mills/vf-series/models/medium/vf-4.html
[haas-g00]: https://www.haascnc.com/service/codes-settings.type=gcode.machine=mill.value=G00.html
[autodesk-haas]: https://cam.autodesk.com/posts/post.php?name=haas
[harvey-g]: https://www.harveytool.com/resources/general-machining-guidelines
[helical-3fl]: https://harveyperformance.widen.net/content/bujcsxkuoz/original/SF_H40ALV-3.pdf
[helical-old]: https://cdn.shopify.com/s/files/1/0612/0733/files/Helical_Aluminum_Parameters.pdf
[haas-em]: https://www.haascnc.com/content/dam/haascnc/ecommerce-assets/linedrawings/milling/end_mills/speeds-and-feeds/03-0564%20to%2003-0587%20end%20mills,%20hsam2,%20speeds%20and%20feeds,%20inch.pdf
[yg1]: https://www.yg1usa.com/downloads/Miniature_End_Mill_Speeds_and_Feeds.pdf
[harvey-entry]: https://www.harveyperformance.com/in-the-loupe/types-tool-entry/
[sandvik-f]: https://www.sandvik.coromant.com/en-gb/knowledge/machining-formulas-definitions/milling-formulas-definitions
[haas-fm]: https://www.haascnc.com/content/dam/haascnc/ecommerce-assets/speeds-and-feeds/High%20Performance%20AL%20Speeds%20and%20Feeds.pdf
[haas-spot]: https://haascnc.com/content/dam/haascnc/ecommerce-assets/linedrawings/holemaking/spot_drills/speed---feeds/03-2222%20to%2003-2231%20Carbide%20Speeds%20and%20Feeds,%20Landscape%20142%20Deg%20Spot%20Drills.pdf
[iscar]: https://www.iscar.com/eCatalog/Ecat/datafileENM/INFO/4714.pdf
[haas-drill]: https://www.haascnc.com/content/dam/haascnc/ecommerce-assets/speeds-and-feeds/Speeds%20and%20Feeds%20AL%20Drills%20editable.pdf
[sandvik-462]: https://www.sandvik.coromant.com/en-us/tools/solid-round-tools/solid-carbide-drills/corodrill-dura-462
[mms-2015]: https://www.mmsonline.com/articles/best-practices-of-top-us-shops
[mms-2014]: https://www.mmsonline.com/articles/what-it-takes-to-be-a-top-shop
[mms-2013]: https://www.mmsonline.com/articles/top-shops-secrets-to-success
[mms-2012]: https://www.mmsonline.com/articles/top-machining-strategies-and-equipment
[mms-2011]: https://www.mmsonline.com/articles/see-how-you-stack-up
[mms-fix]: https://www.mmsonline.com/articles/quick-change-fixturing-locks-in-time-cost-savings
[kurt]: https://www.americanmachinist.com/machining-cutting/article/21898295/zeropoint-clamping-system-aligns-instantly
[mmt-preset]: https://www.moldmakingtechnology.com/articles/using-presetters-to-reduce-machine-idle-time
[das]: https://www.cs.umd.edu/~nau/papers/das1995estimation.pdf
[ufl]: https://web.mae.ufl.edu/designlab/TA/Assigned%20Parts%20Time%20Estimates.pdf
[cloudnc]: https://cloudnc.com/blog/cam-assist-beta-feedback
[gwiz]: https://s3.amazonaws.com/s3.cnccookbook.com/GWCalcCADCAMEstimator.htm
[cte]: https://ctemag.com/?p=95145
[qm]: https://www.qualitymag.com/articles/96602-how-to-simplify-your-as9102-first-article-inspection-process
