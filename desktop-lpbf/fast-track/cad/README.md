# Fast-track CAD: FT-0, FT-1 and FT-1V as one machine that grows

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260). Round 1 (2026-11-26) answered
Sterling's request on PR 294 to "attempt the full FT-0, FT-1, and FT-1V modeling and progression, showing also the
progression of how we would move from one configuration to the next as parts become available". Round 2 (2026-11-27)
redraws the bought parts that decide fit from the makers' STEP files and drawings, adds the monitoring parts and the
PCard route's Thorlabs piston stage, and fixes what the other round-2 workers found. Round 3 (2026-11-28) re-runs
everything on the g3 gantry, the frame the structural FEA passed and now the model's default, and adds two checks: the
deck cassette through the cube's face, and taking the scan head off for service. Nothing has been bought or built.

- **The model:** one parametric CadQuery model with five states, S1 → S2 → FT-0 → FT-1 → FT-1V, each built from the
  one before in the order the parts arrive.
- **The checks:** interference, the scanned beam, recoater and piston sweeps (exact booleans and a python-fcl mesh
  sweep), the box door's swing, taking the beam tube off, fit, the layer camera's and lights' sight lines, gas volume;
  the cassette's way into the cube and the scan head's way off the gantry.
- **The schedule and spend:** when each state can start, and what it adds to the cost.
- **The images:** each state, each step between states, the monitoring parts, the camera's view, the Thorlabs variant.

It extends the study in [`../README.md`](../README.md).

| File | What it is |
|---|---|
| [`ft_model.py`](ft_model.py) | the model: parameters with sources (`P`), `build(state, pz, hx, lid_open, piston, monitoring)`, the made parts (`MADE`, MK-01 to MK-23), the monitoring parts (`MON`, MON1 to MON9), the diff between states, STEP export |
| [`ft_vendor.py`](ft_vendor.py) → [`out/vendor-verify.json`](out/vendor-verify.json) | the bought parts drawn to the makers' dimensions, with `measure` and `verify` modes against the vendors' STEP files |
| [`vendor-cad-manifest.csv`](vendor-cad-manifest.csv) | where each vendor file came from (URL, sha256, date); the files themselves are not committed |
| [`ft_checks.py`](ft_checks.py) → [`out/checks.md`](out/checks.md), [`out/checks.json`](out/checks.json) | all the checks above, by state |
| [`ft_progression.py`](ft_progression.py) → [`out/progression.md`](out/progression.md), [`out/progression.csv`](out/progression.csv) | the schedule of the five states (three ordering scenarios), the spend by state, what each step adds, moves and removes, and the assembly order at each step |
| [`ft_cassette.py`](ft_cassette.py) → [`out/cassette.md`](out/cassette.md), [`out/cassette.json`](out/cassette.json) | round 3: what the deck cassette needs to get into the cube (envelope, the smallest square or round opening at every roll angle, the pocket it sits in, a python-fcl insertion through a parametric opening) |
| [`ft_head_service.py`](ft_head_service.py) → [`out/head-service.md`](out/head-service.md), [`out/head-service.json`](out/head-service.json) | round 3: taking the scan head off the g3 gantry (python-fcl and exact booleans along each route) |
| [`ft_render.py`](ft_render.py) → [`../img/cad-*.png`](../img/), [`../img/cad-progression.gif`](../img/cad-progression.gif) | renders |
| `out/ft-0.step`, `out/ft-1.step`, `out/ft-1v.step`, `out/ft-1-thorlabs.step` | the machines as STEP assemblies |

```bash
python desktop-lpbf/fast-track/cad/ft_model.py                      # STEP files
python desktop-lpbf/fast-track/cad/ft_vendor.py verify              # needs the vendor files in /tmp/ft-vcad/
python desktop-lpbf/fast-track/cad/ft_checks.py                     # out/checks.*  (11-26 min on one core)
python desktop-lpbf/fast-track/cad/ft_progression.py                # out/progression.*, img/progression-gantt.png
python desktop-lpbf/fast-track/cad/ft_cassette.py                   # out/cassette.*  (~5 min)
python desktop-lpbf/fast-track/cad/ft_head_service.py               # out/head-service.*  (~2 min)
xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/fast-track/cad/ft_render.py
```

All of it is on the g3 gantry (`P["gantry"] = "four_post_braced_front_g3"`, the default since round 3): the checks,
the renders, the STEP files and the progression. `ft_vendor.py verify` was not re-run in round 3 (the vendor files
are not on this runner); [`out/vendor-verify.json`](out/vendor-verify.json) is round 2's and the vendor parts have not
changed.

The Python packages are in [`../../analysis/requirements.txt`](../../analysis/requirements.txt): CadQuery 2.8,
PyVista, python-fcl and trimesh.

![The five states](../img/cad-progression.png)

![Each state built up from the one before](../img/cad-progression.gif)

## Short answer

- **Still one machine in five states, and nothing wasted.** The parts that drop out along the way are FT-0's rod
  collar and spreader bar, the box's rod and long beam-tube section (the cube takes a 21 mm longer rod and a short
  section), and the box itself when the cube arrives; it then becomes the spreadability rig.
- **Drawing the bought parts from the makers' files changed the cassette.** Zaber's STEP shows the X-LSQ075B recoater
  is 285.85 mm long, not ~241 mm, so it fits neither the deck nor the cube with room to load it. The **X-LSM100B-E03**
  (239.2 mm, 101.6 mm travel) replaces it, and the deck shrinks to **245 x 245 mm**. The hopper needs 66.6 mm of
  travel between its parks and has 101.6 mm.
- **The optics moved.** The lens axis is 30 mm in front of the plate centre (no specular return into the fibre), the
  head is SCANLAB's 206.9 x 140 x 180 mm housing hung by its entrance face, and the LINOS lens's datasheet puts its
  bottom 299.5 mm above the bed. The head's top is 528.1 mm above the bed.
- **The checks are clean in all five states and with the Thorlabs stage, on the g3 gantry:** no clashes and nothing
  in the scanned-beam envelope (29, 53, 88, 106, 108 and 105 parts); the hopper over its full 101.6 mm and the plate
  over its 20 mm stroke without contact (exact booleans and a python-fcl mesh sweep). The nearest parts to the beam
  are the cord clamp at the hopper's park (3.5 mm) and the cover-slide holder (5.6 mm); the tightest apertures keep
  6.2 mm round the beam. g3 changed none of these numbers: its new members sit above and beside the head, outside
  the enclosure and the beam.
- **The box opens now, but only to 24 degrees.** The beam tube's centre section is two half-shells that slide off
  sideways (no contact over 60 mm). The door then swings 24 degrees before the layer camera meets the lens collar
  (26 degrees with the camera unclipped), which lifts its front edge 120 mm: a tight opening for hand-spreading and
  plate changes.
- **The gantry is g3, the frame the structural FEA passed** (`P["gantry"] = "four_post_braced_front_g3"`, the
  default since round 3): 45 mm posts, front and back cross-beams carrying the head's flange plate (MK-09), a diagonal
  per side, knee braces at the back and the front, a top flange on both beams with three gussets under the head, and a
  **10 mm support plate on the head's far (+x) face from both cross-beams**, with angle brackets. The FEA gives
  62.0 / 100.6 / 179.4 Hz, over its 60 Hz minimum (50.0 Hz without the far-side plate, 43.1 Hz without the front
  braces and the flange). Its two new parts go in at S1 with the rest of the frame; the ±15 V supply moves behind the
  back post. Everything in this folder is now on g3 ([close-up](../img/cad-gantry-g3.png)).
- **The scan head still comes off for service on g3,** but not by lifting the head alone: its input turret passes
  through MK-09, so either MK-09 lifts off with the head on it (after the collimator comes off, or it catches under
  the front cross-beam), or the far-side plate and the mirror block come off and the head slides 46 mm toward +x
  before it lifts. Details in [the head section](#taking-the-scan-head-off-on-g3).
- **Gas volume from the model:** FT-0 24.2 L, FT-1 24.0 L, FT-1V 22.6 L (Ideal Vacuum gives the empty cube 22.6 L).
- **Monitoring (MON1-MON9)** is drawn: a Raspberry Pi HQ layer camera through its own window port (17.8 µm per pixel
  across the plate in the box), two raking LED lights through wall ports, a coaxial photodiode behind the head's input
  mirror, an acoustic-emission sensor on the rod-end block, thermocouples, and a digitizer on the laser's sync.
- **The cube's face opening is still unverified** (Ideal Vacuum's site blocked us), but round 3 pinned down what it
  must be. The cassette is 245 x 245 mm and 107.7 mm tall, and in the billet frame its deck lies in the bottom face's
  pocket, which is as big as the face opening: so the opening must be **square, at least 245 mm plus clearance
  (247 mm with 1 mm a side) with sharp corners, and 245 + 0.586 r with corner radius r** (252.4 mm at r = 1/2 in.,
  259.9 mm at 1 in.; python-fcl insertion through a parametric opening). Tilting or rolling the cassette lets it
  through a 196-207 mm face but not onto the floor, so it doesn't help in this cube, and round 2's fallback (the bare
  deck edge-on through 180.3 mm, the cassette built inside) doesn't work either. Rounding the deck's corners (up to
  ~33 mm) covers larger corner radii; under 245 mm the cube can't take this cassette, and Kurt J. Lesker's BX1212S,
  with a full-face door, is the documented alternative.

## What round 2 changed, and why

Round 1 drew most bought parts as estimated envelopes. Round 2 draws the ones that decide fit from the makers' own
files, in our code (`ft_vendor.py`; no vendor geometry is copied or committed; URLs and sha256 in
[`vendor-cad-manifest.csv`](vendor-cad-manifest.csv)), and takes the other workers' findings.

| Item | Round 1 | Round 2 | Source |
|---|---|---|---|
| Recoater stage | Zaber X-LSQ075B-E01, ~241 mm long (estimate) | **Zaber X-LSM100B-E03**: 239.2 x 84.8 x 21.0 mm with its controller, 101.6 mm travel (parts.csv M1c) | X-LSM100A-E03 STEP (same body; Zaber offers no STEP of the B), datasheet |
| Why | | the X-LSQ075B measures **285.85 mm**: it fits neither the deck nor the cube's 289.6 mm inside with room to load it; the X-LSQ150B is 360.9 mm | Zaber STEPs |
| Deck cassette | 250 x 250 mm | **245 x 245 mm**: the X-LSM100B spans x -148.8 to 90.4 on a deck from -150.5 to 94.5 (1.7 and 4.1 mm spare); the cube's face opening must be >= 247 mm (round 3: 245 mm plus clearance with sharp corners, 245 + 0.586 r with corner radius r, because the deck lies in the bottom face's pocket) | this model |
| Piston stage | X-VSR20A, 120 x 80 mm footprint (estimate) | X-VSR20A-E01 **88 x 101 x 73 mm** retracted, 64 x 64 platform, M6 grid; drive housing turned to +y | Zaber STEP |
| PCard piston stage | not modelled | **Thorlabs MTS50/M-Z8 on end** beside the rod, an L-arm to the same rod-end block, a tower plate on the bracket plate: `build(..., piston="thorlabs")` | Thorlabs STEP |
| Box | "SCE-16128CHNFSS class" (not a real part) | **Saginaw SCE-16EL1208SSLP**: 16 x 12 x 8 in., 0.075 in. 304, door 15.50 x 11.63 in., usable depth 8.30 in., quarter-turn latch, concealed hinges, poured gasket, four panel studs that now hold the deck (MK-23) | Saginaw drawing |
| Scan head | 160 x 140 x 115 mm on a plate (estimate) | hurrySCAN 20/30 housing **206.9 x 140 x 180 mm, 5.8 kg**, hung by its beam-entrance face from a flange plate (MK-09) on the gantry's two cross-beams; the unit's input turret and 45 deg mirror block drawn by eye from the listing photos | SCANLAB brochure drawing (the 25 sharing it is an assumption); seller's photos |
| f-theta lens | Ø110 x 66 mm, working distance 300 mm (estimates) | LINOS 4401-288-000-20: **Ø118 body, Ø119.8 ring, 69.2 mm long, WD 296.2 mm, FFL 344.8 mm**; with the window and cover slide in the beam the focus moves 3.3 mm, so the lens bottom is 299.5 mm and its flange 348.1 mm above the bed; the head's top 528.1 mm above the bed | LINOS datasheet; process worker |
| Lens axis | over the plate centre | **at (0, -30)**: on axis the plate's specular reflection would put ~342 W back into the fibre core, 30 mm off none. The window stack is centred at y -11 (box) and -21 (cube), the beam tube at y -17 / -24, the cover-slide holder opened from Ø40 to Ø44 | process worker (`../process/`) |
| Cover slide | under the window / the cube's top plate | **130 mm above the bed in both enclosures**; in the cube on a drop tube from the top plate (a sooted slide defocuses 2.3 mm there against 9.4 mm at 221 mm) | process worker |
| Heaters | 1/4 x 1 in. cartridges, length unverified (McMaster login wall) | **Ø6 x 20 mm, 24 V 50 W cartridges** (LulzBot KT-CP0013 class, H1): 2 in the plate in Ø6.1 x 21 mm holes, 4 in the well block from its -x face. The heater plate drops from 28 to **24 mm** | lead |
| Beam tube | one tube with a floor ring in the lens collar: captive once the lid is shut (video worker) | collar clamped on the lens, and a **centre section split in two half-shells** (2 toggle clamps) located by Ø50 spigots *inside* both its ends: each half slides off sideways, then the door opens | this model; checks below |
| Window-stack screws | not drawn | 6 x M4 x 12 flat heads, countersunk flush, so the half-shells slide over them | this model |
| Rod's lower end | open question | a **potted plug** (vacuum epoxy, 15 mm) in the hollow rod; the 6-wire pigtail leaves into a pocket in the **rod-end block** (MK-15: rod clamp, M4 screw, the AE sensor's face) and plugs into a 6-way terminal block on it | this model |
| FT-0 layer spreading | 70 mm film applicator (knobs to ±41 mm) | **48 mm spreader bar** (48 x 12 x 30 mm, ground edge), parked at +x out of the raking light: the slot nozzle and exhaust collector leave 54 mm on the block top (video worker) | this model |
| Gantry | two 30 mm uprights and a cross-beam at the back, the head cantilevered (13 Hz, structural FEA) | **four 45 mm posts, front and back cross-beams, a diagonal per side, knee braces at the back and the front**; the head's flange plate spans both cross-beams, with a 60 mm top flange bolted on both and three gussets (`P["gantry"] = "four_post_braced_front"`). **Round 3: g3 is the default** (`"four_post_braced_front_g3"`): the gussets under the head and a 10 mm support plate on the head's far face from both cross-beams, with angle brackets | structural FEA 4c and its addendum (43.1 / 59.7 / 67.2 Hz without the front braces and the flange; 50.0 Hz braced; **62.0 / 100.6 / 179.4 Hz on g3**) |
| Monitoring | none | MON1-MON9 (below) | PR 266/281 `monitoring.md`, adapted |
| Cables and fasteners | not drawn | recoater M8 to a back-wall gland (box) or a KF-25 feedthrough (cube); X-VSR20A M8; well-block leads; heater and TC cable; gland screws M5 x 25 with bonded seals, inside the gland's face seal at (±12.5, ±12.5) and into M5 taps in the deck (fab worker); deck clamps on the panel studs (box), M6 deck screws into the bottom plate (cube); bracket-plate screws into T-nuts | this model |

### The bought parts against the makers' files (`ft_vendor.py verify`, `out/vendor-verify.json`)

Our shapes are outer envelopes with the mounting features (holes, faces, connectors) at the measured places, so they
are fuller than the vendors' hollow bodies; the extents are what decides fit.

| Part | Maker's file | Extents, ours (mm) | Extents, maker's (mm) | Volume, ours vs maker's |
|---|---|---|---|---:|
| Zaber X-VSR20A-E01 | STEP | 73.0 x 88.0 x 101.0 | 73.0 x 88.0 x 101.0 | +13.9 % |
| Zaber X-LSM100A-E03 (the B's body) | STEP | 21.0 x 84.81 x 239.2 | 21.0 x 84.81 x 239.2 | +4.8 % |
| Thorlabs MTS50/M-Z8 | STEP | 22.0 x 43.0 x 163.45 | 22.0 x 43.0 x 163.45 | +7.5 % |
| Zaber X-LSQ075B-E01 (rejected) | STEP | 43.1 x 65.0 x 285.85 | 43.1 x 65.0 x 285.85 | envelope only |
| Zaber X-LSQ150B-E01 (rejected) | STEP | 43.1 x 65.0 x 360.9 | 43.1 x 65.0 x 360.85 | envelope only |
| SCANLAB hurrySCAN 20/30 housing | drawing | 140 x 180 x 206.9 | 140 x 180 x 206.9 | no STEP |
| LINOS 4401-288-000-20 | drawing | 69.1 x 119.8 x 119.8 | 69.2 x 119.8 x 119.8 | no STEP |
| Saginaw SCE-16EL1208SSLP | drawing | 203.2 x 304.8 x 406.4 | 203.2 x 304.8 x 406.4 | no STEP |

Not available this round: Ideal Vacuum's cube (its sites returned a Cloudflare block), McMaster parts (login wall),
the Lesker BX1212S (VacuCAD login). Those stay estimates, marked in `ft_model.P`.

## The checks (`out/checks.md`)

| State | Parts | Clashes | Designed contacts | Parts in the beam envelope |
|---|---:|---:|---:|---:|
| S1 | 29 | 0 | 6 | 0 |
| S2 | 53 | 0 | 8 | 0 |
| FT-0 | 88 | 0 | 10 | 0 |
| FT-1 | 106 | 0 | 10 | 0 |
| FT-1V | 108 | 0 | 11 | 0 |
| FT-1, Thorlabs MTS50/M-Z8 piston | 105 | 0 | 10 | 0 |

The last run (round 3, 2026-11-28) took 655 s (capped at 3 GB), on the g3 gantry. Each state has two more parts than
on round 2's braced frame (the far-side support plate and its angle brackets); every other number below is unchanged.
The far-side plate meets the head's far face and both beams' inner faces face to face, so those pairs show neither as
clashes nor as designed contacts (no shared volume).

- **Beam:** with the lens axis at (0, -30) the envelope is an oblique cone; the nearest parts are the cord clamp at
  the hopper's park (3.5 mm) and the cover-slide holder (5.6 mm). Margins round the envelope at the apertures:
  the window 7.54 mm (box) and 10.47 mm (cube), the cover-slide holder 6.17 mm, the tube's lower and upper spigots 7.4 and 11.79 mm (box), 12.11 and 14.54 mm (cube).
- **Recoater:** the hopper needs 66.6 mm of travel between its parks (-31.1 and +35.5 mm, where it clears the beam and
  its blade has passed the overflow slot); the X-LSM100B gives 101.6 mm, 14.7 mm spare at the left end and 20.3 mm at
  the right. Swept over the full travel, 13 positions with exact booleans and 41 with python-fcl: no contact; the
  closest is the carriage bracket to the stage shield's slot, 2.0 mm, at the left end.
- **Piston:** 20 mm of the X-VSR20A's 20 mm stroke (50 mm of the MTS50's); at the bottom the heater plate is 7.7 mm
  above the deck, at the top the rod-end block is 3.0 mm under the gland, and the rope wiper stays in the bore over the
  whole stroke. 21 fcl poses, no contact. Rods: 84.6 mm (box), 105.6 mm (cube). In the cube, 1 atm pushes the rod
  with 12.8 N against the stage's 100 N continuous thrust.
- **Box door:** with the tube's half-shells off, it swings to **24 degrees** before the layer camera meets the beam-tube lens collar (its front edge then 120.2 mm up), or 26 degrees with the camera unclipped, when the quarter-turn latch meets the beam-tube lens collar (129.5 mm). Hinge axis estimated at the door's back top edge.
- **Beam tube removal:** FT-1: the 123.5 mm section's half-shells slide out along x, no contact over 60 mm; FT-1V: the 23.7 mm section's half-shells slide out along y, no contact over 60 mm.
- **Fit:** the deck has 78.8 and 28.0 mm to spare in the box, 21 mm through the cube's estimated 266 mm face opening
  (10.5 mm a side, and the same on the cube's floor: the deck sits in the bottom face's pocket, see
  [below](#will-the-cassette-fit-through-the-cubes-face); round 2 gave 22.3 mm a side from the 289.6 mm plate-to-plate
  size), 29.9 mm a side in a Lesker BX1212S. The cassette stands 107.7 mm above the floor in a 289.6 mm tall cube (the
  vibration motor on the hopper's arm; round 2's 102.7 mm predates moving the motor up onto the arm). The window is 152.0 mm above the bed in the box (a 2.99 mm beam, 5.7 kW/cm² at 400 W) and
  251.8 mm in the cube (4.95 mm, 2.1 kW/cm²); the cover slide is 130 mm above the bed in both. M2 substrate screws fit
  (head edge at r = 19.0 mm on the 19.9 mm disc); M2.5 and M3 don't.
- **Gas:** FT-0 24.2 L, FT-1 24.0 L, FT-1V 22.6 L of gas. A 20 L/min flow purge of the box reaches 1000 ppm in
  6.4 min ideally (13-32 min expected, 257-642 L of argon); two pump-and-fill cycles to 1 mbar take the cube below
  100 ppm on paper in about 7 min with 45 L (pump speed 1 L/s through the KF-25 hose is an estimate).
- **Sight lines:** with the hopper parked at the right, where it waits while the laser runs, the camera sees all of the
  plate in FT-0, FT-1 and FT-1V, the -x light reaches all of it and the -y light 91-93 %. Parked at the left, the
  hopper shades the -x light completely and 17-22 % of the camera's view. Two round-2 changes got there: FT-0's
  spreader bar parks at +x (at -x it shaded the -x light completely), and the cube's camera port moved out to
  (-100, -50) (at (-70, -55) it saw 76 % of the plate, looking past the drop tube that hangs the cube's cover slide).
- **Two late round-2 fixes** (the vibration motor was 5 mm into the arm; the pump hose 17.7 mm into the pump's inlet,
  both found by the video worker's frame audit) are in the model, and the full runs since include them.
- **Heat (`fast_track.py`'s load):** box air 71 °C in still air, 39 °C with the fan; cube 61 °C and 36 °C. The stages
  are rated to 50 °C, so both need the fan.

## Monitoring (MON1-MON9)

Sterling asked to film what happens in the chamber at the highest resolution, frame rate and zoom that fit, and to
log as much metadata as possible. PR 266's `../../monitoring.md` (sections 9-10 on PR 281's branch) answers that for
the robot-built machine; here it is fitted to FT-0, FT-1 and FT-1V and drawn (purple in the renders). Prices are in
[`../parts.csv`](../parts.csv) (rows MON1, MON2 (both lights), MON4, MON5, MON6, MON8; the MCC 134 is in C3), read
live by the lead.

| Id | What | Suggested product | First state | In the model |
|---|---|---|---|---|
| MON1 | layer camera | Raspberry Pi HQ Camera (IMX477, 4056 x 3040, 1.55 µm), 16 mm C-mount lens (25 mm for FT-1V), Thorlabs FESH1000 short-pass in front | FT-0 | on a post on the box door, looking through its own Ø1 in. window port (MK-19) at the plate, 30.7 deg off vertical; on the cube's top plate at 24.1 deg; Scheimpflug wedge (MK-20) |
| MON2 | raking light from -x, 15 deg | Thorlabs mounted white LED (MCWHL7 class), SM1 tube with an aspheric condenser (ACL2520U class), LEDD1B driver fired by the Pi | FT-0 | through a window port in the box's left wall (MK-21); a bore in the cube's left plate |
| MON3 | raking light from -y, 30 deg, over the nozzle | as MON2 | FT-0 | the box's front wall; the cube's door |
| MON4 | coaxial photodiode | short-pass dichroic (DMSP1000 class) cut to replace the hurrySCAN's 45 deg input mirror: it still folds the 1070 nm beam into the head and passes 400-1000 nm back out of the mirror block's back port, into an SM1 tube with FESH1000, a bandpass, AC254-050-B, a 500 µm pinhole and a PDA36A2 | S1 (aligned once, used from FT-0) | on the input-mirror block's back face |
| MON5 | acoustic emission | resonant 150 kHz sensor with integrated preamp (MISTRAS R15I-AST or Vallen VS150-RIC class), couplant, decoupler | FT-1 | clamped on the rod-end block's +x face (it rides with the plate) |
| MON6 | thermocouples | self-adhesive type K patches on the beam tube and window ring (S2); 1/16 in. sheathed type K in the plate and the well block, and a box-air probe through a compression fitting (FT-0) | S2 | drawn in their holes and on their faces |
| MON7 | laser and layer sync | the RTC4's (or RTC5's) laser gate and a job-list trigger bit, through an isolator to the digitizer and the Pi | FT-0 | no geometry |
| MON8 | digitizer | PicoScope 4824A class, 8 channels on one clock (photodiode, AE, gate, layer sync) | FT-0 | envelope on the bench |
| MON9 | thermocouple logger | MCC 134 HAT on the Pi I/O node (parts.csv C3) | S2 | no geometry |

The layer camera, from the model (`ft_model.camera_geometry`, `ft_checks.camera_numbers`; IMX477, f/2.8, circle of
confusion two pixels):

| | Box (FT-0, FT-1) | Cube (FT-1V) |
|---|---|---|
| C-mount lens | 16 mm | 25 mm |
| tilt off vertical | 30.7 deg | 24.1 deg |
| lens to plate centre | 199.4 mm | 298.7 mm |
| µm per pixel, across / along the tilt | 17.8 / 20.7 | 17.0 / 18.6 |
| field (full sensor) | 72.1 x 54.0 mm | 68.8 x 51.6 mm |
| Scheimpflug wedge | 2.96 deg | 2.34 deg |
| depth of field at f/2.8 | 2.48 mm | 2.27 mm |
| plate depth across the tilt | 20.4 mm | 16.3 mm |
| Rayleigh radius at f/2.8, 550 nm, on the plate | 21.5 µm | 20.6 µm |
| video 2028 x 1520 at 40 fps | 35.5 µm per pixel | 33.9 µm per pixel |

Sight lines (rays from 133 points on the plate to the camera's lens and to each light's port, hopper at either park; a blocked ray meets any part):

| State | Hopper | Camera sees | MON2 lights | MON3 lights |
|---|---|---:|---:|---:|
| FT-0 | right park (hx 37.5) | 100.0 % | 100.0 % | 90.8 % |
| FT-0 | left park (hx -33.1) | 100.0 % | 100.0 % | 90.8 % |
| FT-1 | right park (hx 37.5) | 100.0 % | 100.0 % | 90.8 % |
| FT-1 | left park (hx -33.1) | 78.0 % | 0.0 % | 90.8 % |
| FT-1V | right park (hx 37.5) | 100.0 % | 100.0 % | 92.7 % |
| FT-1V | left park (hx -33.1) | 82.6 % | 0.0 % | 92.7 % |

![What the layer camera sees in FT-1](../img/cad-camera-view-ft-1.png)

![Monitoring parts in FT-1](../img/cad-monitoring-ft-1.png)

![Under the box in FT-1](../img/cad-under-ft-1.png)

## Opening the box, and moving from the box to the cube

The video worker collision-checked assembly paths on round 1's model and found three problems. Round 2's answers:

1. **The beam tube trapped the lid.** Its lens collar had a floor ring inside the tube, so the tube could slide only
   14 mm up the lens, and the lid needs more than 15 mm to clear the gasket. Now the collar stays clamped on the lens
   and the tube's centre section is two half-shells held by two toggle clamps. Both of its ends sit over Ø50 mm
   spigots *inside* the bore (3 mm overlap, light-tight), one on the window flange and one under the collar, and the
   window-stack screws are countersunk flush. So each half-shell slides straight off sideways with no lift:
   FT-1: the 123.5 mm section's half-shells slide out along x, no contact over 60 mm; FT-1V: the 23.7 mm section's half-shells slide out along y, no contact over 60 mm. Then the door opens to 24 degrees (26 with the camera unclipped). `build(..., lid_open=True)` draws it.
2. **FT-0's film applicator didn't fit between the nozzle and the collector** (70 mm against 54 mm). FT-0 spreads its
   layers with a 48 mm spreader bar (48 x 12 x 30 mm, ground edge) that rides on the block top between them, with the
   layer depth set by the plate's recess under the block top (shims under the FT-0 collar). parts.csv M4 should
   change from the film applicator to this bar (a short length of 1/2 x 1-1/4 in. ground flat stock, edge ground).
3. **The box couldn't slide off its rails with the gland under its floor.** The gland plate hangs 12.0 mm below the rail tops, and the rod reaches 22.0 mm into the rod-end block.. The FT-1 -> FT-1V order
   that avoids lifting the box:

   | Step | What | Numbers from the model |
   |---|---|---|
   | 1 | plate to the top of its stroke (pz +5), heaters off and cool, substrate off | |
   | 2 | beam tube half-shells off, door open | free to 24 deg with the camera on the door |
   | 3 | at the rod-end block: the pigtail's 6 wires out of the terminal plug, rod clamp (M4) loose | the rod is 22.0 mm into the block |
   | 4 | lift the heater plate and its rod straight up out of the bore | 103.6 mm lift; the rod (84.6 mm, box) passes the block, the gland's O-rings, the floor and the deck |
   | 5 | deck clamps off (4 stud nuts), recoater M8 and well-block leads unplugged at the glands, cassette lifted out through the door opening | deck 245 x 245 mm in a 402.6 x 301.0 mm box |
   | 6 | stage to the bottom of its stroke, gland plate (4 x M5) unbolted and taken out sideways | block top 23.0 mm under the gland (3.0 mm at the top of the stroke); the gland hangs 12.0 mm below the rail tops |
   | 7 | box unbolted from the support rails and slid forward off them | nothing hangs below its floor now |
   | 8 | cube onto the rails (its underside lands where the box's was), gland onto its bottom plate, the X-VSR20A untouched | |
   | 9 | hopper and overflow cup emptied; the cassette carried in level through the door at mid-height of the opening and set down on the floor, M6 deck screws into the bottom plate | the deck lies in the bottom face's pocket, as big as the face opening: at least 245 mm plus clearance with sharp corners (see [the cassette section](#will-the-cassette-fit-through-the-cubes-face)) |
   | 10 | the long rod's plate assembly down through the bore, the gland and into the rod-end block; plug in, clamp | rod 105.6 mm (cube) |
   | 11 | window stack on the top plate, cover-slide drop tube, short half-shells; cross-beam and optics up 21.0 mm | |

   The pigtail's plug has to pass the gland's 12.9 mm bore (step 4): either screw terminals that are wired after the
   rod is through, as drawn, or a 6-pin circular plug of 12 mm or less (estimate: Lemo 0B or Binder 719 class, check
   its current rating against 2.1 A per heater). The leads are potted in the rod, so the cube's long rod is a second
   plate-and-rod assembly made ahead (2 more H1 cartridges and one more MK-04), or the leads are re-potted (a day for
   the epoxy).

## Will the cassette fit through the cube's face?

Round 3, [`ft_cassette.py`](ft_cassette.py) → [`out/cassette.md`](out/cassette.md). FT-1V moves the cassette (the
deck plate and everything bolted on it) into the Ideal Vacuum cube at step 9 above, with the heater plate and rod
already out, the recoater's M8, the well-block leads and both gas lines unplugged, and the deck screws not in. The
cube's face opening is not published; the model draws an estimate (266 mm square, sharp corners).

**What has to go in.** 245.0 x 245.0 mm (the deck; nothing overhangs it once the gas lines are off) and **107.7 mm
tall** from the deck's underside. The tallest part is the vibration motor on the hopper's arm, at any hopper position;
the hopper's top is at 97.7 mm, the nozzle and collector at 72.7 mm, the X-LSM100B under its shield at 40 mm. Seen
along the door's axis the cassette sweeps 245.0 x 107.7 mm, and the same along x.

**The frame decides it, not the door.** The P107540 frame is one billet with interchangeable 12 x 12 in. plates, so
each face's opening runs straight through as a pocket, and each plate's 7.6 mm boss sits in its pocket (the model
draws it so). The deck rests on the bottom plate's boss, below the side pockets' edges (11.8 mm below them with the
266 mm estimate), so it lies in the bottom face's pocket, which is exactly as big as the face opening. The opening
therefore has to hold the deck's footprint, whichever way the cassette comes in, and has to be square (or square with
small corner radii). The deck's sharp corners meet the pocket's corner radius r first: the pocket needs a side of
**245 + 0.586 r** (zero clearance). A python-fcl run confirms it: the frame redrawn with a parametric pocket on all six
faces and the five closed plates' bosses, the cassette carried in through the door at mid-height of the opening
(2 mm steps), then lowered onto the floor (1 mm steps), bisection on the opening's side:

| Opening's corner radius (mm) | Smallest opening, fcl (mm) | With 1 mm a side (mm) | If slid in along the sill (mm) |
|---:|---:|---:|---:|
| 0 | 245.0 | 247.0 | 245.0 |
| 6.35 (1/4 in.) | 248.8 | 250.8 | 252.8 |
| 12.7 (1/2 in.) | 252.4 | 254.4 | 263.4 |
| 19.05 (3/4 in.) | 256.2 | 258.2 | 274.5 |
| 25.4 (1 in.) | 259.9 | 261.9 | 285.8 |
| 38.1 (1.5 in.) | 267.3 | 269.3 | over 289 |

- **The model's 266 mm estimate** passes with 10.5 mm a side, and would take a corner radius up to 35.8 mm.
- **Carry it in at mid-height, not along the sill:** slid along the sill, the deck's lower corners meet the opening's
  own corner radii (the last column). With 10.5 mm a side or less there is no room for fingers beside the deck, so it
  needs two lifting handles or eye-bolt holes on its top face, at the front and back strips (23-25 mm free), and the
  hopper and the overflow cup emptied first.
- **A round opening would not do:** the bottom pocket would be round too, and the 245 mm square deck needs 346.5 mm
  across its corners, more than the 289.6 mm inside. (A round door alone would need 246.9 mm along y, 245.2 mm along
  x.)

**Tilting or rotating doesn't lower it in this cube.** Rolled about the insertion axis so that the deck runs along the
opening's diagonal, the cassette passes a much smaller square face: 207.3 mm at 39.3 deg through the door with the
hopper at its right park, **196.9 mm** with the hopper parked at the left (43.6 deg), 196.2 mm through a side plate
(50.8 deg); fcl confirms the first through a 19.4 mm wall (207.8 mm passes, 206.8 mm is blocked). But the deck then has
to lie flat in the bottom pocket, which is the same size as the face, so in a billet cube the roll gains nothing. The
same goes for round 2's fallback (the bare deck in edge-on through 180.3 mm, the cassette built inside): the bare deck
would get in but could not lie flat. The roll numbers matter only for a chamber whose inside is bigger than its door,
such as a welded box with a hinged door; there, taking parts off gains little more: hopper, arm and motor off 196.9 mm,
the shield too 192.6 mm, down to the bare deck's 180.3 mm.

**If the opening turns out smaller:**

1. **At least 245 mm but with larger corner radii than the table allows:** round the deck's four corners. With a deck
   corner radius R_d the pocket needs 245 + 0.586 (r - R_d). R_d can go to about 33 mm before the X-LSM100B's
   back-left corner (1.7 mm from the deck's left edge, 23.2 mm from its back) leaves the deck; the M6 deck-screw holes
   stay 7 mm inside the edge. Example: a 254 mm opening with 1 in. corners needs R_d of 10 mm or more (13.5 mm with
   1 mm a side).
2. **Under 245 mm:** the 245 mm deck can't lie in the cube with anything taken off it. The parts themselves span
   241.8 mm in x (the X-LSM100B and its shield) and 196.3 mm in y (nozzle to stage), so a cube deck cut to about
   243 x 200 mm with rounded corners gains about 2 mm; below about 243 mm the X-LSM100B (239.2 mm) can't sit square in
   the cube at all. Then the Lesker BX1212S (304.8 mm inside, a full-face door) or a welded cube with a door is the
   chamber.
3. **Whatever it is,** the P108171 plate's boss, which fits the opening, gives its size and corner radius, and so do
   the 12 x 12 in. faces of the short-cube frame P108364, which take the same plates. Both STEP files were read once,
   on 2026-11-25, for their outside sizes only
   ([`route-catalogue-chambers.csv`](../../robot-build/route-catalogue-chambers.csv)).

## FT-1V's chamber: the Ideal Vacuum cube or a Lesker box

Ideal Vacuum's sites blocked every fetch on 2026-11-27, so the cube's face opening is still an estimate (266 mm).
Round 3 worked out what the cassette needs ([previous section](#will-the-cassette-fit-through-the-cubes-face)): a
square opening of at least **245 mm plus clearance** (247 mm with 1 mm a side) if its corners are sharp, more if they
are radiused, because the deck lies in the bottom face's pocket, which is as big as the face opening. Round 2's
fallback for a smaller opening (the bare deck in edge-on through 180.3 mm and the cassette built inside) does not work
in a billet frame: the deck would get through the door but could not lie flat on the floor.

The documented alternative is Kurt J. Lesker's BX1212S box chamber (read by the lead on lesker.com): 12 x 12 x 12 in.
(304.8 mm) inside, 304 stainless, a hinged aluminium door over the whole front face, ports KF40 and ISO100-K
(positions not stated), $7,995, lead time not stated. It is not drawn in the model (its STEP needs a VacuCAD login);
on its published inside size the 245 mm deck loads through the door with 29.9 mm each side, the stage stays under its
floor (a machined or bored floor for the gland), and the window needs a machined top or a viewport on the ISO100-K
port if that port can sit on top.

**Which is less risky:** the Lesker box carries less fit risk (a full-face door; nothing depends on an unpublished
opening) and lists for less than the cube kit ($7,995 against parts.csv E2's $9,210-9,450, before machining either
one's top); the Ideal Vacuum cube carries less schedule risk ("Available now" on 2026-11-25, while Lesker's "KJLC will
contact you" suggests a made-to-order lead time). So: confirm the cube's face opening and its corner radius (a call,
a drawing, or the P108171 plate's boss, which fits the opening) against the table in the previous section, and order
the cube; if the opening is under 245 mm, ask Lesker for a lead time.

## Taking the scan head off on g3

Round 3, [`ft_head_service.py`](ft_head_service.py) → [`out/head-service.md`](out/head-service.md). On g3 the head is
held on both faces: MK-09 is bolted to its entrance face, with the input turret through MK-09's Ø52 hole (1 mm a side)
to the 45 deg mirror block, and the far-side plate presses on its far face. Each route moves a rigid group in 2 mm
steps against every fixed part, in FT-1 and in FT-1V (the same results in both). python-fcl flags contacts and an exact
intersection over 0.5 mm³ confirms them, so parts that slide along each other's faces (the head on the far-side pad,
MK-09's plate between the beams, its top flange off the beams) don't count. In every route the beam tube's
half-shells come off first (as for opening the lid), then the head's DB-9, DB-25, water and air, and the fibre at the
collimator.

| Route | Result |
|---|---|
| A1: MK-09 lifted straight up with the head, lens, lens collar, input stack and collimator on it | **blocked at 12 mm**: the collimator, which comes in from -y under the front cross-beam, meets the beam |
| A2: the same with the collimator off first | free over 160 mm |
| B1: the head alone (mirror block off its turret, head unbolted from MK-09) slid toward +x, far-side plate in place | **blocked at once** by the far-side plate |
| B2: the same with the far-side plate and its brackets off first | free: 46 mm toward +x takes the turret out of MK-09's hole, then 160 mm up |
| C: the head alone straight up | **blocked at 2 mm**: its turret in MK-09's hole |

Nothing traps the head for good, but on g3 it can't simply be lifted out of its frame:

- **The way to do it (A2):** take the collimator out of the mirror block's input port, unbolt MK-09's angle brackets
  and its top flange from both beams, loosen the far-side plate's brackets so its pad lets go, and lift MK-09 straight
  up with the head, lens, collar, input stack and photodiode branch on it (about 10 kg, estimate; the head alone is
  5.8 kg). The input mirror and the coaxial photodiode stay aligned to the head; only the collimator is re-seated.
- **The head on its own (B2):** the far-side plate and its brackets off, the mirror block (with the photodiode branch
  and the collimator) off the turret, the head unbolted from MK-09, slid 46 mm toward +x and lifted. The photodiode
  branch has to be re-aligned afterwards.
- **Refitting:** bolt the head to MK-09 first and bring the far-side pad up to its face last, so the pad does not push
  the head sideways (the pad or strap is an estimate: the head's far face has no published mounting points).

## The PCard route's piston stage: Thorlabs MTS50/M-Z8

`build(state, piston="thorlabs")` (and `out/ft-1-thorlabs.step`) puts the MTS50/M-Z8 (163.45 x 43 x 22 mm by
Thorlabs' STEP, 50 mm travel; with a KDC101 controller it is parts.csv M2b, $2,179-2,300 read by the lead) on end
beside the rod: its carriage faces -y, an L-arm (MK-15) carries the same rod-end block, and a tower plate on the
bracket plate holds the stage with its lower end through a cut-out. It checks clean (no clashes, nothing in the beam;
20 mm of its 50 mm used; the same 3.0 and 23.0 mm block-to-gland gaps). Its limit is force, not fit: the structural
FEA ([`../analysis/out/fea/struct.md`](../analysis/out/fea/struct.md), 4d) takes Thorlabs' 4.5 kg (44 N) vertical
rating and finds the gland as drawn (two O-rings at 15 % squeeze) not acceptable (up to 50 N at breakout in FT-1,
58 N in FT-1V), and one O-ring at 10 % acceptable (19 N and 27 N at breakout). So the MTS50 needs a one-O-ring gland.

## The five states

Weeks are scenario A's (stages on PCards, cube ordered on day 0); `out/progression.md` has B and C. The schedule is
this folder's own task graph (`ft_progression.py`), built on `fast_track.py`'s task durations: the orders and
approvals in its `COMMON` (the RTC4's eBay window, the 208/240 V circuit for the laser, the O₂ analyzers), and its
per-state shop days from the fabrication worker's hours ([`../fab/out/hours.json`](../fab/out/hours.json), at 8 h a
working day early and 5 h late). The upgrade steps (1-2 days each) are estimates.

| State | Starts | Needs these to have arrived (parts.csv) | Made parts first used | What it can do | Gate before the next state |
|---|---|---|---|---|---|
| **S1** optics bench | checks at 1.4-3.8 wk | laser chain L1-L7 (RTC4 L5b), water L10-L11, PC C1, T-slot frame E4, eyewear S2, coaxial photodiode MON4 | deck MK-01, target stand MK-18, the head's mounts MK-09 (flange plate, top flange, gussets, and g3's far-side support plate with its angle brackets) | guide laser only: the head and the RTC4 talk; field size and distortion on a target at the powder plane; the photodiode branch aligned | LSO registration; the laser's interface and the 208/240 V circuit |
| **S2** box round the beam | full power at 1.6-4.2 wk | box E1, window and cover slides L8, beam dump L9, safety relay and switches S1, S5, S6, the Pi and its I/O node C2-C4, thermocouples MON6 | window stack MK-02, beam tube MK-10 (long section), deck clamps MK-23 | full power into a water-cooled dump inside a closed Class 1 box: calorimetry, a focus ladder, interlocks proven | the laser makes its power and its spot, inside its return window |
| **FT-0** single-track bench | tracks at 1.9-5.2 wk | heater parts H1 (2), H2-H4, gas and O₂ G1-G8, extinguisher and room O₂ S3-S4, spreader bar M4, stock F1, glovebox P1, camera, lights and digitizer MON1-MON3, MON7-MON8 | well block MK-03, heater plate MK-04, substrates MK-05, rod MK-06, gland MK-07, nozzle and collector MK-11, overflow cup MK-16, collar and terminal bracket MK-17, camera and light ports MK-19-MK-21 | flow purge with an O₂ log, the plate at 200 °C, single tracks on hand-spread layers, pads | EHS review; O₂ log; stages and FT-1 parts in |
| **FT-1** purge-box LPBF | coupons at 3.1-8.1 wk | X-LSM100B M1c, X-VSR20A M2 (or the MTS50 M2b), hopper parts M3, second heater zone H5, stage supplies C5, AE sensor MON5 | arm and hopper MK-08, shield MK-12, bracket, riser and rod-end block MK-15 | multi-layer coupons at 100-1000 ppm O₂, plate and well at 200 °C | coupons made, or the O₂ log asks for FT-1V |
| **FT-1V** cube | coupons at 3.7-9.3 wk | cube frame and plates E2, pump-purge kit E3, feedthroughs E5 | cube top and bottom plates MK-13/14, long rod MK-06, short beam-tube section MK-10, cover-slide drop tube | the same coupons at < 100 ppm by pump-purge; the box becomes the spreadability rig | - |

Milestones in weeks, earliest to latest:

| Milestone | A: stages on PCards, cube ordered on day 0 | B: stages on PCards, cube ordered after FT-0's O2 log | C: both stages on one Zaber PO, cube after the O2 log |
|---|---|---|---|
| S1 guide-laser and scanner checks | 1.4-3.8 wk | 1.4-3.8 wk | 1.4-3.8 wk |
| S2 FULL POWER INTO THE DUMP | 1.6-4.2 wk | 1.6-4.2 wk | 1.6-4.2 wk |
| FT-0 FIRST TRACKS | 1.9-5.2 wk | 1.9-5.2 wk | 1.9-5.2 wk |
| FT-1 FIRST COUPONS | 3.1-8.1 wk | 3.1-8.1 wk | 3.6-8.1 wk |
| FT-1V FIRST COUPONS (< 100 ppm) | 3.7-9.3 wk | 5.1-10.9 wk | 5.1-10.9 wk |

Spend by the state that first needs each `parts.csv` line (the lead's round-2 file):

| State | Adds | Cumulative |
|---|---:|---:|
| S1 | $6.5k-11.2k | $6.5k-11.2k |
| S2 | $3.1k-4.0k | $9.7k-15.2k |
| FT-0 | $11.2k-21.3k | $20.9k-36.4k |
| FT-1 | $8.3k-10.8k | $29.1k-47.2k |
| FT-1V | $11.7k-13.8k | $40.8k-61.0k |

The FT-1 and FT-1V sums are the study's stand-alone totals (`fast_track.py`, from the same `parts.csv`) plus what
growing costs: FT-0's spreader M4 ($150-600) and, at FT-1V, the box E1 ($694-760), which then becomes the
spreadability rig.

![Schedule of the progression](../img/progression-gantt.png)

### The steps, in pictures

Green: added. Blue: moved. Red: removed (faint). Grey: unchanged. The part lists are in
[`out/progression.md`](out/progression.md).

| | |
|---|---|
| ![S1 to S2](../img/cad-step-s1-to-s2.png) | ![S2 to FT-0](../img/cad-step-s2-to-ft-0.png) |
| ![FT-0 to FT-1](../img/cad-step-ft-0-to-ft-1.png) | ![FT-1 to FT-1V](../img/cad-step-ft-1-to-ft-1v.png) |

### The three machines

| | |
|---|---|
| ![FT-0](../img/cad-ft-0.png) | ![FT-0 section](../img/cad-section-ft-0.png) |
| ![FT-1](../img/cad-ft-1.png) | ![FT-1 section](../img/cad-section-ft-1.png) |
| ![FT-1V](../img/cad-ft-1v.png) | ![FT-1V section](../img/cad-section-ft-1v.png) |

### Details

| | |
|---|---|
| ![FT-1 with the box door open](../img/cad-door-open-ft-1.png) | ![FT-1 with the Thorlabs MTS50/M-Z8](../img/cad-ft-1-thorlabs.png) |
| ![The layer camera's view in FT-1V](../img/cad-camera-view-ft-1v.png) | ![S1 and S2](../img/cad-s2.png) |
| ![The head's mounts on the g3 gantry, from +x](../img/cad-gantry-g3.png) | |

## How it is built

- **Frame:** the origin is the centre of the substrate's top face at the start of a build, in the box states; +X is
  the recoat direction and +Y points to the back. The bench stays put between states. In FT-1V the cassette, the rod
  and the optics sit 21.0 mm higher, because the cube's floor plate (22.9 mm) is that much thicker than the box's
  sheet floor; the cube's underside lands where the box's was, so the support rails and the X-VSR20A don't move.
- **Inside the enclosure, on the 245 mm deck (MK-01):**
  - **Well block (MK-03):** 80 x 80 x 40 mm on four Macor standoffs, four Ø6 x 20 mm cartridges from its -x face, a
    thermocouple beside them, and a 7 x 44 mm overflow slot at x = 22-29 mm over the overflow cup (MK-16) in a deck
    pocket.
  - **Plate stack:** the Ø39.8 x 6 mm substrate (three M2 countersunk screws at r = 17.1 mm) on the Ø39.8 x 24 mm heater
    plate (MK-04: two Ø6 x 20 mm cartridges in from below, a thermocouple, lead grooves to the rod socket, a fibreglass
    rope wiper in a groove), on the hollow 1/2 in. rod (MK-06) whose lower end is potted.
  - **Gas, on the block's top:** the 45 x 4 mm slot nozzle in front and the exhaust collector behind, so the
    cross-flow runs along +Y, across the recoat direction.
  - **Recoater:** the X-LSM100B runs behind the collector at y = 82 mm under a stainless shield (MK-12) with a slot for
    the carriage bracket; the arm (MK-08) reaches forward over the collector to the 20 x 46 mm hopper with its 3 mm
    silicone-cord blade. The hopper parks at x = +37.5 mm while the laser runs (it must be at +35.5 or beyond).
- **Under the enclosure:** the rod passes the deck, the floor and the gland plate (MK-07: two O-rings on the rod, a
  face seal, four M5 screws inside it) to the rod-end block (MK-15) on the X-VSR20A's platform. The stage sits on a
  riser on a bracket plate across the base rails. At the top of the stroke the block stops 3.0 mm under the gland.
- **On the enclosure:** the window stack (MK-02: ring, Ø50.8 x 9.53 mm fused-silica window, retaining flange; in the
  box also an inner clamp ring under the thin door) centred at y = -11 mm (box) or -21 mm (cube); the cover slide
  130 mm above the bed in a Ø44 holder (in the cube on a drop tube); the beam tube (MK-10) from the flange to the
  lens collar; one direct-opening Omron D4NS-2CF tongue switch per guard (S5): on the box's front for the lid
  (the cube's door in FT-1V) and on the lens collar for the beam tube.
- **Gantry (g3, the default):** four 45 mm T-slot posts, the back pair on the back support rail and the front pair on
  the bench in front of the front rail, a cross-beam between each pair at the head's height, a diagonal per side, knee
  braces at the back (120 mm) and at the front (80 mm, short enough to clear the collimator), the structural FEA's
  frame. In FT-1V both cross-beams slide up 21.0 mm with the head.
- **Optics:** the hurrySCAN hangs by its entrance face from a 12 mm flange plate (MK-09) bolted to both cross-beams
  with angle brackets, stiffened against the head's pitch by a 60 x 12 mm top flange that lies on both beams and three
  8 mm triangular gussets between it and the plate, under the head's footprint (at y = -100.6, -15 and 15, clear of
  the input turret at y -55). A 10 mm support plate (MK-09) lies against the head's far (+x) face, x 149.6 to 159.6,
  from the front cross-beam to the back one, with its own angle brackets on both beams; the head's far face has no
  published mounting points, so the plate is a pad or a strap (estimate). The ±15 V supply sits behind the back
  post. The input turret passes through a Ø52 hole in MK-09, and the 45 deg mirror block on its end sticks out toward
  -x; the collimator comes in from -y, under the front cross-beam, and the photodiode branch (MON4) sits on the
  block's back. The lens screws into the head (M85 x 1).
- **Beam envelope:** chief rays from a pivot 392.9 mm above the bed (estimate, inside the process worker's 296-424 mm)
  to the Ø40 field, plus the converging beam's own half-width; with the axis offset the envelope is an oblique cone,
  Ø40.2 at the bed and centred on the plate, Ø16.7 at the tube's upper end and 4.9 mm off the tube's axis there.


## Differences from fab/ (v1)

The fabrication worker's [`../fab/`](../fab/) (round 2) machined the made parts from this model's round-1 geometry and
changed some of them; it documents its delta to this v2 model on its side. Taken here: the rod gland's four M5 screws
moved inside the gland's face O-ring, to (±12.5, ±12.5) with M5 taps in the deck (at ±21 they left four open leak paths
from the box to the room). Still different, for the lead to settle:

| Part | This model (v2) | fab/ (v1) |
|---|---|---|
| Beam tube MK-10 | collar clamped on the lens; centre section split in two half-shells (2 toggle clamps) over Ø50 spigots inside both ends; slides off sideways | one-piece 2-3/8 in. tube in a 2 mm socket on the window flange and a 3 mm socket in the collar, held by four M4 tie rods; the collar's lens bore is 112 mm (round 1's Ø110 envelope; the lens is Ø118/119.8) |
| Window stack MK-02 | 6 x M4 flat heads, flush, on Ø80; flange aperture Ø44; 1.8 mm window recess | 8 x M5 flat heads on Ø84 clamping flange, window, ring and lid; aperture Ø38; 2.2 mm recess (window + 0.8 mm FKM cushion); AS568-030 and -140 face grooves; ring with a 4 mm lip, 12 mm tall |
| Cover-slide holder | one piece, the slide goes in from +x | split at the slide plane |
| Rod socket in the heater plate | Ø12.80 x 8 | Ø12.95 x 8 with a set screw (seamless 1/2 in. tube is 12.70 ± 0.13 mm) |
| Rod MK-06 | 1/2 in. x 0.035 in. 304 tube | 0.497-0.501 in. OD seamless |
| Macor standoffs | Ø6.35 | Ø7.94 |
| Slot nozzle and exhaust collector MK-11 | 55 x 19 x 8 mm and 60 x 13 x 10 mm | larger |
| Overflow cup MK-16 | 304 | 6061 |

With fab's window flange the beam keeps about 4.5 mm of margin at the window instead of 7.5 mm (aperture Ø38 against
Ø44). fab's one-piece tube can only come off if the collar slides up the lens body once the tie rods are out; this
model's checks cover the half-shell version only.

## Estimates, and what was not done

- **Still estimates, marked in `ft_model.P`:** the cube's face opening (266 mm) and frame; the hurrySCAN 25 using the
  20/30 housing, its beam displacement (30.4 mm) and input height; the input turret and mirror block (by eye from the
  listing photos); the IPG chassis depth, the PC, the pump, the beam dump, the digitizer, the camera and light stacks;
  the chief-ray pivot; the box door's hinge axis (taken as the door's back top edge). A clash or a fit against these
  means "check the maker's drawing", not a certainty.
- **The gantry is the structural FEA's frame** ([`../analysis/out/fea/struct.md`](../analysis/out/fea/struct.md), 4c:
  13 Hz for round 1's two uprights, 79 Hz for four posts with the head on a horizontal plate): four 45 mm posts (drawn as the 30 mm profile scaled up, an
  envelope), the front pair 25 mm in front of the front rail on L feet, a front cross-beam that carries the head
  plate's front end, a diagonal per side from the front post's top to the back post's base, and two knee braces at the
  back. The FEA's addendum ran that frame as drawn here (43.1 / 59.7 / 67.2 Hz: the front portal racking in x, and the
  head nodding on its 12 mm flange plate), so this model adds 80 mm knee braces in the front portal (above the lid's
  swing; the lid hinges at the back, so its front edge never comes forward of the box) and a top flange with three
  gussets on MK-09. The FEA ran that braced version (50.0 / 66.9 / 93.5 Hz, up from 43.1 / 59.7 / 67.2; the frame no
  longer racks, and the first modes are the head swinging on the flange plate's lower part, below the beams).
  `"four_post_braced_front_g2"` answers that: its three gussets (8 mm) sit under the head's footprint, at y = -100.6
  (between the front bracket and the mirror block), -15 and 15 (-55 is taken by the input turret), and run down to the
  plate's bottom edge. The FEA found g2 no better (49.8 / 66.8 / 92.7 Hz: the head's centre of mass sits ~95 mm out
  from a plate held near its top), so `"four_post_braced_front_g3"` adds a 10 mm support plate against the head's far
  face (x 149.6), spanning both cross-beams with its own angle brackets, and moves the ±15 V supply behind the back
  post. The FEA gives g3 **62.0 / 100.6 / 179.4 Hz**, over the 60 Hz minimum, so **g3 is the default since round 3**
  and everything in this folder is on it: the full checks (all five states and the Thorlabs variant, 0 clashes, 0 beam
  hits), the renders, the STEP files and the progression. The real head's far face has no published mounting points,
  so the plate is a pad or strap (estimate). `P["gantry"]` selects `"four_post_braced_front_g3"` (default),
  `"four_post_braced_front"` (50.0 Hz), `"four_post_braced_front_g2"`, `"four_post"` (the FEA addendum's model, 43.1 Hz)
  or `"two_post"` (round 1, 13 Hz).
- **Not drawn:** the Lesker BX1212S (no STEP without a login); the gas plumbing outside the enclosure; O-ring grooves;
  the face seal under the gland; the half-shells' toggle clamps and their seam; wiring outside the enclosure.
- **Not run here:** FEA, CFD and thermal FE are in [`../analysis/`](../analysis/) (round 2 workers). The heat numbers in
  `out/checks.md` are `fast_track.py`'s lumped model.
- **The door's swing** is checked with the hinge axis estimated at the door's back top edge; the Saginaw concealed
  hinges' real axis may sit lower and further back, which would change the free angle by a few degrees.
