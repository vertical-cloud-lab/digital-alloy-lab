# Follow-up checks before buying and building (2026-11-20)

For [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to Sterling's
2026-11-20 request: run follow-up simulations and checks, get machining-aware software to look at the parts, add an
optional tooling BOM, run MuJoCo, powder-spreading simulations and theory, Edison second opinions and pain points from
similar systems, simulate every assembly, use, maintenance and swap operation, use real parts, make sure the seals
seal, use Shigley, heat transfer and CalculiX, and say what the machine costs used and with cheaper equivalents.

Nothing here has been built, quoted by a shop, or reviewed by BYU's Laser Safety Officer or EHS. Each note below has
its own sources, assumptions and re-run instructions.

## 0. Round 3 (2026-11-20 evening): the machinist's review, the robots, safety, and a full re-run

Sterling asked for four things on 2026-11-20:
- the UR12e aligned with byu-vcl PR 318, with whatever tools make each automated job work;
- answers to a BYU machinist's three concerns: the chamber block, the 5-axis look, and assembly collisions;
- two UR12e arms on MiR250s taking the build from boxes to a machine, and laser, gas and powder safety;
- then a re-run of every check, with Edison as a rubber duck.

Each line links its own note. Nothing here has been built, quoted by a shop or reviewed by BYU's LSO or EHS.

### What changed

1. **The chamber is now a through-frame plus a bolted floor plate** ([`chamber-construction.md`](chamber-construction.md)).
   - **Material:** the frame is cut from 5-1/2 in. 6061-T651 plate. Its core comes out as one 17 kg slug of reusable
     stock, and the walls are finished from both sides with a standard 3/4 in. end mill at 3.3:1, R10 corners. The
     block needed a 3/8 in. tool at 13:1. The leftover stock with standard tools is 1.05 cm³, against 29.1 cm³.
   - **Floor joint:** 3.53 mm FKM in a Parker gland at 24.9 % squeeze, 18 × M4 and 2 dowels. The Shigley separation
     factor is 3.2 to 9.5, including a +0.5 bar regulator fault.
   - **CalculiX:** yield SF 5.1 with the top open, 9.9 with the lid on, and 500 at +20 mbar.
   - **Rail holes:** tapped through the back wall from outside, with plugs on bonded washers, so no tool has to reach the
     inside face.
2. **Nothing needs 5-axis** ([`machining.md`](machining.md), [`setup_plan.json`](analysis/out/machining/setup_plan.json)).
   - With a 4th axis the 48 machined parts drop from 118 setups to 60. The frame goes from 6 to 3: bottom up, top up,
     then all four walls in one clamping on an HRT210 on a 2-1/2 in. riser.
   - **Still needing a special tool or a compound angle:** the lid's enclosed drawer slot (mill it open from the
     underside), the camera-adapter boss and the dovetail grooves.
3. **The machinist's "few hundred hours" is right.** Counted honestly, it is about 264 h for 48 parts (250 h with a 4th
   axis).
   - Only 28 h of that is cutting; CAM is 116 h and setups 99 h.
   - Buying stock parts, waterjetting the flat parts and standardising tools could bring it to about 150 h.
   - FreeCAD 1.0.2's CAM ran headless and wrote G-code: the frame cuts in 60 min and the floor plate in 58 min. CAMotics
     would not install, so the G-code isn't simulated.
4. **The video now shows scale and runs the mill the way the shop would** ([`build-sequence.md`](build-sequence.md)).
   - **Scale:** a soda can, a 300 mm rule, dimension lines, and a 1.75 m person on the room floor beside the tray.
   - **Mill:** the spindle is always vertical, and the part is clamped, flipped or indexed on the 4th axis. The animated
     cuts match the model's frame and floor plate to 0.000 % by volume.
5. **Two UR12e arms assembling the machine** ([`assembly.md`](assembly.md)): every part is swept along its insertion path,
   both arms are planned with RRT-Connect, and every move gets PR 318's 1.5 mm audit.
   - **Result after two iterations:** 63 of 79 checked steps pass, and 118 of 135 screws get a planned, collision-free
     approach.
   - **What it took:** a trunnion positioner for the turn-overs, an angle-head nutrunner for upward screws, a vacuum
     gripper and nozzle, and a reordered sequence.
   - **What still fails needs design changes:** a clamped rod-end cap instead of the weld, dowels pressed by the shop,
     locating pins on three bolted parts, a lever KF-40 clamp, and door clamps.
   - **Seals:** installed stretch is 1.4–2.7 %. Folding the two rod O-rings through the gland plate is the riskiest
     step (~34 % bending strain).
   - **Model fixes from it:** the lid gland's corners went from R4 to R13 (Parker's minimum is 10.6 mm), and the floor
     port got a 20° lead-in.
6. **Robot tending in PR 318's cell** ([`robot-ops.md`](robot-ops.md)): UR12e + 2F-85 + D405 on a MiR250 with the 131 kg
   ballast, FCL on meshes, IK branches, RRT-Connect, the 1.5 mm audit and the movers check.
   - **Result:** 10 of 12 jobs pass end to end on M50, counting the bayonet re-run below, and both plate exchanges also pass on S25 and L75.
   - **Pushing the door shut fails** from every one of 16 arm placements, so the door gets a rotary actuator. Its latches
     get air cylinders.
   - **The bayonet plate exchange** hit the thermal cutoff, which sat in the lugs' path. The cutoff is now lowered 1 mm, and
     the re-run passes on M50, S25 and L75.
   - **Still failing:** the build module swap (no reach past the hinge knuckles, or for the last 140 mm of its path; the
     fix is zero-point modules and a handle) and the overflow jar (its hose and the guard rail are in the way). The liners
     weren't run.
7. **A hypothetical robot shop** ([`robot-shop.md`](robot-shop.md)): payload limits it, not reach.
   - 44 of 48 parts start from ≤ 5 kg of stock. The 34.7 kg frame blank needs a person with a vacuum lifter, and it is
     still 15.7 kg after the core comes out, so two arms are needed.
   - The planned VF-4, lathe, two-arm and box moves pass, and the MiR keeps a 39.6 kg tip-over margin with the ballast.
   - **Time:** 137 person-hours by hand against 60–78 with the cell, not counting the months to set the cell up.
8. **Safety** ([`safety.md`](safety.md)).
   - **BYU's pages:** every one of BYU's 35 safety program pages needs a BYU login.
   - **Top gaps:** a fixed O₂ monitor (room and Shuttle), a limit on the argon a supply fault can release, a safety
     controller with enough inputs, and a filter-cake passivation and bag-out procedure.
   - **Laser:** the NHZ through the f-theta is 114 m, so eyewear needs OD ≥ 5.4 at full power.
   - **What's listed:** 33 parts and 14 design changes.
9. **Bugs found and fixed:**
   - the robot cell's torques: the wrists had been carrying the arm's own link weights, reading 228 % of a limit where
     the right figure is 21–31 %;
   - a held part kept riding in the arm's collision set after release;
   - moves after a grip dragged the part 2 mm sideways;
   - `thermal_laser.py` crashed on a NameError;
   - the shop study used a 13 in. frame blank where the final plan cuts a 15 in. one.

### The full re-run on the final model (2026-11-20 23:59 to 2026-11-21 02:15 UTC, [`analysis/rerun_all.sh`](analysis/rerun_all.sh))

| Check | Script | Result on the final model | Against the committed result |
|---|---|---|---|
| Interference, exact booleans | `interference.py` | **0** for M50, S25 and L75: 224 parts, 5 states and 8 motion sweeps each | unchanged; the floor plate's 8 designed contacts were added to the allowlist |
| Robot tending, bayonet plate | `robot/ops.py` | **passes** on M50, S25 and L75, with a 0.6–0.7 mm closest pass and 33 % peak torque | was failing: its lugs hit the thermal cutoff, now lowered 1 mm |
| Mass | `mass_budget.py` | 268.2 kg on the tray; the process module is 87.7 kg and tips at 0.69 g | +0.6 kg (the tending features) |
| Tray power and heat | `tray/tray_budget.py` | unchanged | identical |
| Seals | `seals/seals.py` | every gland OK, including the new floor gland (25 % squeeze, 80 % fill); the lid cord path is 955 mm with R13 corners | permeation O₂ 1.76 → 2.20 ppm/h (+0.44 from the floor cord); make-up argon for 10 ppm 37.5 → 46.8 sccm |
| Door as a seal carrier (CalculiX) | `seals/door_seal_fea.py` | 1.78 mm cord: O-ring 1401 N, 34 µm of squeeze lost, latch 724 N each | the same to 0.1 µm |
| Mechanical checks | `mech/mech_checks.py` | door latches 724 N each, SF 4.9 against 3.56 kN; the hinges carry about 0 | the committed 410 N / 314 N split predated moving the latches to the seal's centroid height (the door FEA already had 724 N) |
| Hot-swap joint sizing | `hotswap/joint_calcs.py` | the same conclusions | numbers within 2 %, from the refreshed temperatures |
| Hot-swap FEA (CalculiX) | `hotswap/hotswap_fea.py` | M50 re-run: plate lugs 42.3 MPa, flange 126.4 MPa | within 1.5 %. The L75 half was cut off by the runner's memory (the 10 GB cap ran out). The parts it checks are unchanged this round except 9 mm³ of heater block, so its committed L75 numbers stand |
| Structural FEA (CalculiX) | `fea/fea.py` | chamber frame + floor plate cases 1, 1b and 1f (the chamber study); door SF 38; Z lift arm tilt 7.0 µm; window SF 45 | **Z arm tilt is 7.0 µm, not 3.8 µm** (still under 10 µm): the old figure predated the seal round's changes. Cases 2, 4 and 6 (lid, recoater, bridge) hit the memory cap in meshing or rendering; their parts are unchanged this round (identical volumes), so their committed results stand |
| Module thermal (CalculiX) | `thermal_module.py` | plate, block and seal temperatures within 1 °C | **the magnet face runs 6–8 °C cooler at build end (56–58 °C).** The rod grew from 77 to 91 mm two rounds ago and this hadn't been re-run |
| Laser heat in the module | `thermal_laser.py` | the same conclusion: dense layouts drive the plate past 200 °C, and the fan or water sleeve fixes it | the magnet column is a few °C cooler (the same rod change). A NameError that stopped the script writing its JSON is fixed |
| MuJoCo | `mujoco_check.py` | every contact is a designed joint or a convex-decomposition artefact (the exact check is clear). The unlatched door stays shut to 11°, then reaches 1.71 m/s at the edge with no damping. The tray in transit doesn't slide or tilt up to 2 m/s² | the same picture; the door now has a rotary actuator ([`robot-ops.md`](robot-ops.md)) |
| Hand operations | `ops/run_ops.py` | M50 81 pass / 2 warn / 40 fail; S25 and L75 8 / 0 / 3 | was 78 / 1 / 40. The floor plate's steps pass. New warning: hex keys reach the 18 floor screws, but no torque screwdriver fits, so use a torque-limiting hex key |
| CFD (OpenFOAM, coarse) | `cfd/` | identical to the committed coarse case: 122 metrics, 0.00 % ([`rerun_coarse_2026-11-21.json`](analysis/out/cfd/rerun_coarse_2026-11-21.json)) | the gas volume the CFD meshes didn't change; the R10 corners are below its rectilinear mesh |
| DEM (LIGGGHTS) | `powder/dem_spread.py` | the baseline case reproduces every number exactly | its inputs (blade, powder) are unchanged |
| Machining | `machining/` | the chamber study re-ran cam_sim, per_setup, dfm, setup_plan and FreeCAD CAM | §0.2–0.3 above |
| Two-arm assembly | `assembly/run_assembly.py` | 63 of 79 steps pass; 118 of 135 screws get a planned approach | the first pass was 47 / 26 and 91 |
| Robot shop | `shop/shop_checks.py` | payload table refreshed from the final part list | frame blank corrected to the 15 in. one |

The memory cap matters on this 15 GB runner: two earlier runs on this branch died of OOM. Every step ran under
`/tmp/capmem`, and `rerun_all.sh` re-runs any step by name.

### Edison

The four rubber-duck tasks the stopped run had submitted are fetched with their full trajectories: chamber construction,
robotic O-ring assembly, robot tending, and safety (`edison/r3-*`).

From 22:28 UTC Edison refused new tasks with HTTP 402 (out of credit), so no further rubber-duck passes ran. The next query
is written and waiting in [`edison/r4-frame-floor-review/`](edison/r4-frame-floor-review/).

## 1. What changes what we buy or draw, most urgent first

1. **Decide air- or water-cooled before ordering the laser** ([`heat.md`](heat.md) §2). The quoted IPG
   YLR-500-U3-SM-AC is forced-air cooled, rated 10–35 °C, and dumps ~1.2 kW. Running inside the VLM, a build puts
   1.2–2.7 kW into the Shuttle, more than all six trays of Shuttle 1 idling. Either buy the water-cooled unit and size a
   chiller for it (the shared ThermoFlex 900 is too small), or duct the air-cooled unit's exhaust out of the Shuttle.
   It is a 10–12 week order, so this comes first. A used, returnable 400 W YLR-400-SM at $2,100 is also on the table
   ([`cost-scenarios.md`](cost-scenarios.md)).
2. **The build module needs a way to shed the laser's heat** ([`heat.md`](heat.md) §1, CalculiX).
   - A dense layout's absorbed beam power (81–111 W on M50/L75) is more than the module loses at 200 °C (52–97 W), so
     the heater switches off and the plate drifts: about 290 °C by the end of the stroke as drawn.
   - That pushes the NdFeB coupling past 80 °C and the rod gland past 150 °C. The block's 240 °C cutoff trips first,
     but it only cuts heaters that are already off.
   - **Fix:** a fan on the module under the floor (magnet 29 °C, rod gland ≤ 75 °C), or a water-cooled sleeve (plate
     within ~7 K of 200 °C); SmCo instead of NdFeB; a plate over-temperature trip on laser enable; an interlayer dwell in
     the scan software.
   - Edison's second opinion agrees: AlSi10Mg over-ages at 200 °C within ~10 h, so hold the plate within about ±10 °C.
3. **The gas flow misses its target** ([`gas-flow.md`](gas-flow.md), OpenFOAM).
   - At the design point (115 L/min) no part of the plate reaches 2.5 m/s: a thin wall jet at 1.5 m/s mean, 3 mm up.
     One slow vortex fills the chamber and passes under the cover slide. The drawn gas knife can't reach the slide.
   - **Fix (simulated):** perforated plates in both slots, a 35 mm outlet channel with a KF-40 port, and 140–200 L/min.
     These give 2.6–3.3 m/s over the whole Ø75 plate. The blower spec (BOM G4) becomes 140–200 L/min at 1.5–3 kPa.
     [`real-parts.md`](real-parts.md) found no compact gas-tight blower even at the old 60 L/min (the nearest, a KNF
     N 630.1.2, weighs 45 kg), so G4 needs a decision.
4. **Seals are now drawn, three details are still open** ([`seals.md`](seals.md)). Every closure and penetration has a
   real seal in the model, and the sweeps are clean. Still open:
   - the door and drawer half-dovetail grooves overfill at worst tolerance: use a 2.62 mm cord or a plain groove;
   - no catalogue quarter-turn latch gives the drawer its 0.4 kN;
   - the hermetic rod-end feedthrough that meets the spec needs a KF-16 port, which the Ø22 cap can't take.
5. **Two features can't be machined as drawn, and the bore needs outsourced honing** ([`machining.md`](machining.md)):
   - the lid's enclosed cover-slide drawer slot;
   - two back-wall rail inserts outside the door opening;
   - the Ø50.8 H7 bore needs honing, and no BYU shop lists a honing machine.

   Everything else can be made at BYU (Haas VF-4, and the Physical Facilities shop's lathe, TIG and wire EDM); the
   gas-module base plate needs a re-position or a waterjet outline.
6. **Jobs done every build that still fail** ([`operations.md`](operations.md), re-checked on the final model,
   9e6464a):
   - the overflow jar can't come out, on S25, M50 and L75;
   - the right draw latch, new with the real latches, sits behind the front-right optics post where no hand reaches;
   - the beam tube, now on the galvo's real axis, blocks the hand from the reservoir handle (the reservoir itself
     still slides out with 0.85 mm to spare).

   The guard door now clears the right latch, and the L75 module swap passes. Still failing: window service means
   removing the scan head, the gland plate and its rod O-rings are trapped on the welded rod end, the liners are
   captive, and the assembly order changes in 12 places.
7. **Real parts didn't all fit the envelopes they replaced** ([`real-parts.md`](real-parts.md); fixed in the model,
   §3):
   - the laser is 4U, so the rack becomes 11U;
   - the real KF-25 ball valve and the collimator poke through the guard;
   - the galvo's beam axis is 25 mm off;
   - the f-theta needs an adapter ring.
8. **Powder spreading:** zero the blade gap at temperature, because the 200 °C plate stack grows ~112 µm. Start
   layers at ~2 × D90 (about 120 µm), spread at 50 mm/s, and sieve the overflow, which comes out coarse
   ([`powder-spreading.md`](powder-spreading.md), LIGGGHTS DEM).
9. **A robot can't do any of the automated jobs end to end yet** ([`robot-ops.md`](robot-ops.md), MuJoCo,
   UR10e + Robotiq 2F-85). The arm's strength and reach are never the limit: peak joint torque is at most 39 %, and the
   reach margin is ≥ 342 mm. What it would grip is the limit:
   - the stock 2F-85 reaches only ~60 mm past its housing, so in-chamber work needs stepped, cranked fingertips;
   - the plate's grip groove is level with the door sill, so the gripper needs a two-step approach, or the plate has
     to rise ~16 mm instead of 8 mm for exchange;
   - the guard door has no handle;
   - the chamber door needs ~1.4 kN to seat and the drawer 350 N, against a cobot's ~100 N force mode, so both need
     clamps that pull them home;
   - the blade (2 × M3) and the module (2 × M6 thumb screws) need tool-free holds, as [`hot-swap.md`](hot-swap.md)
     already recommends;
   - the liners are captive on the ball screw.

   The paths are straight-line moves without a collision-aware planner, so the arm collisions it found are postures,
   not proof that a job is impossible.
10. **Cost** ([`cost-scenarios.md`](cost-scenarios.md)):

    | Scenario | Low | High |
    |---|---:|---:|
    | Baseline, all new (`bom.csv`) | $39,440 | $112,978 |
    | Used major parts | $36,655 | $71,884 |
    | Cheaper same-spec catalogue parts | $34,168 | $105,324 |
    | Both | $31,711 | $65,002 |

    At the design's spec (a CW single-mode laser, a real scan head and card), the machine is about $79k all new and
    $34–40k with used majors plus cheaper catalogue parts.

## 2. What was run

| Workstream | Tools | Note | Headline |
|---|---|---|---|
| Heat: laser into the module, machine into the VLM | CalculiX (54 axisymmetric runs), energy balance against byu-vcl PR 318's dock and Shuttle budget | [`heat.md`](heat.md), [`laser_heat.md`](analysis/out/thermal/laser_heat.md), [`tray_budget.md`](analysis/out/tray/tray_budget.md) | §1 items 1–2 |
| Seals | Parker gland checks on 29 glands, closure forces, CalculiX door, permeation, pump-down | [`seals.md`](seals.md) | §1 item 4 |
| Machining | OpenCAMLib toolpaths, a voxel stock-removal simulation over six setups, DFM rules over 37 parts | [`machining.md`](machining.md) | §1 item 5; optional tooling BOM: [`tooling-bom.csv`](tooling-bom.csv), machines: [`machines.csv`](machines.csv) |
| Gas flow | OpenFOAM v2406, k-ω SST, 173k and 427k cells, Lagrangian spatter and condensate | [`gas-flow.md`](gas-flow.md) | §1 item 3 |
| Powder spreading | theory (Hamaker, Bond number, gap/D90), LIGGGHTS DEM, 11 runs | [`powder-spreading.md`](powder-spreading.md) | §1 item 8 |
| Hand operations | 21 operations, 154 steps, exact booleans, real tool shapes on 93 screws | [`operations.md`](operations.md) | §1 item 6 |
| Robot operations | MuJoCo 4.0.1, menagerie UR10e + Robotiq 2F-85, IK, convex-piece clearances, joint torques with payload and push forces, 11 operations | [`robot-ops.md`](robot-ops.md) | §1 item 9 |
| Real parts | 18 bought parts drawn to published dimensions, 11 checked against vendor CAD | [`real-parts.md`](real-parts.md) | §1 item 7 |
| Cost | live listings and catalogue prices through the lab Pi | [`cost-scenarios.md`](cost-scenarios.md) | §1 item 10 |
| Second opinions | Edison `LITERATURE_HIGH` ×5 | [`edison/followup-*/`](edison/) | design review, sealing and O₂, powder spreading, lab-built LPBF lessons, laser heat |
| Pain points | 59 sourced incidents and lessons from similar and adjacent systems | [`notes/2026-11-20-pain-points.md`](notes/2026-11-20-pain-points.md) | each turned into a check or change |
| Shigley-style checks | Z-coupling friction, ball screw, screws and latches, chamber warm-up, cover-slide thermal lens | [`analysis/out/mech/mech.md`](analysis/out/mech/mech.md) | carried into `seals.md` §4 |

## 3. Design changes: in the model now, and still to draw

**In the model now** (exact-boolean sweeps: 0 interferences in all 5 states and 8 motion sweeps for M50/M, S25/S and
L75/L; the machine is still 581.2 mm above the tray):
- every seal fix listed in [`seals.md`](seals.md) §0, with real O-rings, cord, latches, feedthroughs and fittings
  ([`seal-parts.csv`](seal-parts.csv));
- 17 of the 63 bought-part entries now drawn to published dimensions ([`real-parts.md`](real-parts.md)): the recoater
  and Z servos, dosing stepper, recoater rail, carriage and ball nut, KF-25 ports, the KF-40 overflow jar and clamp,
  f-theta lens, galvo, collimator, vacuum valve, the 4U laser and the UPS;
- the fit changes those parts forced: an 11U rack (515 mm), the guard widened on both sides for the collimator and the
  valve, the beam line moved to the galvo's real input on a 10 mm riser, a 16 mm lens adapter ring, the Z servo's
  connector to the front;
- the guard door now slides 515 mm, so it clears the door opening (re-checked: passes; [`operations.md`](operations.md)).

**Still to draw**, each with the note that sizes it:

| Change | Why | Note |
|---|---|---|
| A fan or water-cooled sleeve on the module under the floor; SmCo coupling magnet; plate over-temperature trip on laser enable | laser heat | [`heat.md`](heat.md) |
| Water-cooled laser and chiller, or a ducted exhaust | VLM heat | [`heat.md`](heat.md) |
| Perforated inlet and outlet slots, 35 mm outlet channel with KF-40, ~20 mm floor slot or a lip, a purge out of the slide recess instead of the gas knife | gas flow | [`gas-flow.md`](gas-flow.md) |
| Drawer slot opened from the lid's underside; rail inserts within \|x\| ≤ 100 mm; pocket corners R ≥ 9.6 mm; thicker webs at the lid inserts, heater block and piston head; full-depth insert holes | machining | [`machining.md`](machining.md) |
| A removal path for the overflow jar; the right draw latch on the front face or the optics post moved outboard; a reservoir handle reachable past the beam tube; window screws on a bolt circle outside the lens; the chute and gas knife hung from the walls; slotted liner holes and a two-piece back liner; a split gland plate at the rod end; the lens and its adapter ring fitted to the bridge on the bench | hand operations | [`operations.md`](operations.md) |
| 2.62 mm cord or plain grooves on the door and drawer; a drawer latch; KF-16 rod-end feedthrough | seals | [`seals.md`](seals.md) |
| A handle on the guard door; pneumatic clamps that pull the chamber door and drawer home; stepped fingertips; plate exchange height ~+16 mm, or a two-step approach; tool-free blade and module holds | robot tending | [`robot-ops.md`](robot-ops.md), [`hot-swap.md`](hot-swap.md) |
| A hot touch-off or plate-height sensor to zero the gap at temperature; a strain gauge on the blade holder for jam detection | powder spreading | [`powder-spreading.md`](powder-spreading.md) |

## 4. Not done

- **Re-checks on the final model are partial.** The hand-operation check was re-run on the final model (all of M50;
  the swap and overflow jobs on S25 and L75). The robot check was re-run for six of its eleven operations; the
  reservoir, blade, liner and module-swap rows are from the 13:54 UTC model. The interference sweeps, mass budget and
  STEP are on the final model. Their scripts take the CAD path as an argument,
  so they can be re-run on the current model: `operations.md` and `robot-ops.md` give the commands.
- Not yet real in the model: the pump and HEPA housing (builders exist; the gas-loop hoses need re-routing to their
  real ports), the pressure transmitter (the lid port is now SAE-4, the BOM's transmitter is 1/4 NPT), the door
  hardware, solenoids, regulator and small sensors.
- No shop quotes, no blower curve, no measurements.
- The DEM uses a softened contact stiffness, so its absolute packing figures are lower bounds.
- The CFD variants ran on the coarse mesh only.
- The tray budget's galvo, PC, servo and instrument draws are estimates.
