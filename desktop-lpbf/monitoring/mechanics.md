# Monitoring mechanics: the ports, windows, cameras, coaxial cage and AE path as parts of the model (2026-11-25)

Issue #260. [`monitoring.md`](../monitoring.md) §3–§5 and the other notes in this folder put three viewports (LW, BW, LP), a
side and a steep camera, a coaxial 30 mm cage, an acoustic-emission (AE) path and a digitizer on the machine, with their
positions in [`cad/monitoring_spec.py`](../cad/monitoring_spec.py). This note draws them into the low-profile model as real
parts, cuts the holes they need, and checks them against every other part. Nothing here is built. Vendor parts are envelopes
from listed dimensions, as elsewhere in the model; where a dimension was not read off a vendor drawing, the part's name says
"envelope".

| File | What it is |
|---|---|
| [`cad/monitoring_parts.py`](../cad/monitoring_parts.py) | the parts and their cuts; `lpbf_low.build(monitoring=True)`, or `LPBF_MONITORING=1` for scripts that call `build()` unchanged. Off by default, so every existing output is unchanged |
| [`cad/monitoring_spec.py`](../cad/monitoring_spec.py) | the shared positions; §0 lists what this round changed in it |
| [`analysis/interference.py`](../analysis/interference.py) | with `LPBF_MONITORING=1`: the full check (static states and motion sweeps) on the model with the monitoring parts, written to [`interference-monitoring-M50-M.md`](../analysis/out/monitoring/mech/interference-monitoring-M50-M.md); its default run is unchanged |
| [`analysis/optics/monitoring_views.py`](../analysis/optics/monitoring_views.py) `--drawn` | the ports' sight lines as drawn, with every monitoring part in the model: [`sight_drawn.md`](../analysis/out/monitoring/mech/sight_drawn.md) |
| [`analysis/monitoring/mech/render_parts.py`](../analysis/monitoring/mech/render_parts.py) | the five figures below |
| [`analysis/monitoring/fab/frame_features.py`](../analysis/monitoring/fab/frame_features.py) | the LW and BW ports as setup C cuts them; `monitoring_parts.py` imports it, so the model and the CAM share one geometry |

## 0. Short answer

1. **Everything fits, after nine fixes to the first drawing.** The first interference run with the monitoring parts found
   14 clashing pairs. Each was fixed by moving or trimming a monitoring part, except one: PB2 (the Pi box on the bridge)
   moves 12 mm toward +x to make room for the steep camera (§2). RESULTS_LINE
2. **LP moves to (−40, 60), as plume.md §0 item 3 asks, but its bore runs on the line of sight.** At (−40, 60) the sight
   line is 62.1° steep. A bore normal to the lid (fabrication.md's plan for (−60, −80)) would be Ø33 here, and the face seal
   round it would overlap the main window's flange (Ø100 on the lid's centre) by 5.9 mm. A Ø24 bore on the line of sight,
   as the layer camera's, leaves a Ø40.8 adapter 1.7 mm clear of that flange. The camera passes up through a 2,980 mm²
   cut-out in the optics bridge. (−20, 80) fails: its line of sight meets PB2 above the bridge, at (−35, 139).
3. **The LW window is the catalogue Edmund 36-983 (Ø40 × 4), flat on the wall.** Its clamp ring grows to Ø58 and then meets
   the plate-height through-beam's fibre head. The ring gets a flat toward it and its four screws move from 45° to 60°,
   which keeps 2.75 mm of metal between the flat and the nearest hole. The CAM program for the left wall
   (`frame_C90_with_LW.ngc`) must be re-posted for the new seat (Ø40.2 × 5.5) and holes; this runner has no FreeCAD or
   CAMotics.
4. **The coaxial branch fits above the bridge as a 30 mm cage**, with the cubes where `monitoring_spec.COAX` puts them
   (x −155, −215, −285). Photodiode B's detector overhangs the bridge's −x edge by 39 mm on the cage rods, 1.7 mm inside
   the guard's T-slot frame line and ~12 mm from the process fibre.
5. **The AE path is a Ø2 mm waveguide down the hollow rod into the rod end, with the sensor outside on the rod end.** The
   rod end is the gas boundary and has no room for another feedthrough, so the sensor can't ride on the waveguide's cold
   end. The waveguide is screwed into the rod end's bore floor instead, and the sensor sits on the rod end's back face.
   How the waveguide's hot end is held against the plate is an open question (§4).

## 1. What is drawn

| Group | Parts (model names start with) | Where | Drawn from | BOM |
|---|---|---|---|---|
| LW port | bore Ø31, seat Ø40.2 × 5.5, 4 × M4, SAE-4 purge port and Ø4 passage (cut in the frame); window, gasket and flat ring, clamp ring with a flat | left wall, bore centre (y −18.97, z 34.15) | `frame_features.lw_features()` | M0-01, M0-06, M0-13 |
| LW slide | Ø30 × 1.5 slide and a 0.5 mm 316 clip on the left liner; Ø27 hole in the liner, Ø5 for the purge tube | liner's inner face, on the sight line | frame_features' liner hole | M0-02, M0-15 |
| LW purge | SAE-4 × 1/8 in. bored-through fitting, 1/8 in. 316 tube through the wall, bent down inside to a flattened tip 3 mm over the clip; needle valve outside, above the camera's line | (y −18.97, z 72.45) on the wall | fabrication.md §3 (bought, not made) | M0-08, M0-12 |
| Side camera | Chronos 2.1-HD (155 × 96 × 67.3), Kowa LM50JC10M (envelope Ø32 × 50), FBH850-10 + FESH1000 holder; tilt block, plate, 20 mm T-slot post on the process base plate | on the LW sight line; lens front 15 mm off the clamp ring; post at (−300, −38.5) | monitoring_spec `SIDE_CAMERA` | M7-01 to M7-04, M7-08 |
| BW port | obround slot 51.2 × 20.5, seat 58 × 27 × 4.5, 3 × M4 (cut in the frame); window 57.7 × 26.7 × 3, gaskets, clamp frame trimmed clear of the inlet plenum and the recoater sensor clamp; the lower back liner's left piece starts at x −90.8 | back wall, (−125, 111, 29.5) | `frame_features.bw_features()` | M0-03, M0-06, M0-14 |
| BW light | 850 nm mounted LED + collimator, envelope Ø40 × 60, on the BW sight line, 3 mm off the clamp frame | outside the back wall | this note (§2) | M7-05 (see §5) |
| LP port | Ø24 bore on the line of sight and a face O-ring groove (2-025) in the lid; Ø40.8 adapter boss (4 × M4, none on the window flange's side) carrying the Ø25 × 1 slide and the Ø25.4 × 3 window square to the line of sight, retaining ring | lid, (−40, 60, 136) | this note (§3) | M0-07, M7-16 to M7-18 |
| LP camera | IMX296 board in a 40 × 40 × 30 housing (turned so a face, not a corner, faces PB2), Kowa 50 mm, filters; cut-out in the optics bridge | on the LP line; window top 34 mm and lens front 49 mm up the line | monitoring_spec `LID_CAMERA`, `LP_GEOM` | M7-12 to M7-14 |
| Coaxial cage | cube 2 (DMSP950) and cube 3 (DMLP805) on posts, SM1 tubes, ER rods; camera arm to −y (FESH1000, AC254-075-B, cage plate, IMX296 board); PD-A to −y and PD-B to −x (filter, AC254-050-B, pinhole, PDA36A2); beam trap on cube 1's −y port. The old SM1 photodiode chain behind cube 1 is removed | above the bridge, y −25.25, z 271.1 | optics.md §2, `monitoring_spec.COAX` | M5-xx, M6-xx, M0-17, T2 |
| AE | Ø2 mm 316 waveguide (heater block, both radiation shields, the piston head's wire hole, the hollow rod; 3 mm into the rod end's bore floor); Ø19 × 16 sensor and a strap on the rod end's back face; preamp on the process base plate | moves with the piston and the module | monitoring.md §5.4, fabrication.md §3 | M4-01, M4-02, M4-06, M4-09 |
| Recorder | PicoScope 4444 and the sync breakout box on the 4U drawer's floor | rack | sync-and-data.md §2.1 | M1-01, M1-07 |

Not drawn: the trigger generator (a Pico 2 inside PB2, which is drawn as a closed box), cables, the argon line to the purge
valve, the InGaAs and SWIR options (steps 8), the monitoring bulkhead plate on the guard (MN-28), and the waveguide's spring.

## 2. Checks on the model

### 2.1 Interference

INTERFERENCE_SECTION

The first run, and what changed:

| Pair | Overlap (mm³) | Fix |
|---|---:|---|
| PicoScope and bracket × PB1 (the power box stands against the rack's left side) | 283,607 | moved onto the 4U drawer's floor, where sync-and-data.md §2.1 puts it first |
| AE preamp × recoater motor bracket | 3,420 | preamp moved to the base plate's front-left (x −300…−190, y −230…−170) |
| LW purge needle valve × Chronos and its lens | 3,245 | valve stood vertical above the fitting, tube bent up to it |
| LP camera × PB2 and PB2's screws | 758 | housing turned about its axis; PB2 moved 12 mm to +x (`electrical_parts.py`) |
| BW clamp frame × inlet plenum's flange | 136 | frame trimmed 1 mm clear; the third screw is then 1.2 mm from the cut edge (§5) |
| LW clamp ring × side-camera filter holder | 60 | holder starts where its tilted rim is 1 mm off the ring |
| BW clamp frame × recoater sensor clamp | 16 | frame notched 1 mm clear under the clamp |
| BW LED × chamber body; × clamp frame | 10, 3 | a compact Ø40 × 60 source, its nearest edge 3 mm off the frame |
| LW clamp ring × through-beam fibre head | 7 | flat on the ring; holes at 60° (`frame_features.py`) |
| AE waveguide × striker disc | 3 | thread 3 mm deep, not 5 |

### 2.2 Sight lines

SIGHT_SECTION

### 2.3 Height and envelope

The machine is still 579.6 mm above the tray, and its envelope is unchanged (x −1172…1218). The guard is unchanged: the
side camera, its post and photodiode B all stand inside it.

## 3. LP at (−40, 60)

LP_SECTION

## 4. The AE path as drawn

AE_SECTION

## Checks

The load, thermal and AE-path calculations for these parts (window and clamp stresses, the camera mounts, the waveguide's
temperature and contact) are in [`analysis/monitoring/mech/`](../analysis/monitoring/mech/).

## 5. Not done, and limits

LIMITS_SECTION
