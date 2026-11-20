# Follow-up checks before buying and building (2026-11-20)

For [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to Sterling's
2026-11-20 request: run follow-up simulations and checks, get machining-aware software to look at the parts, add an
optional tooling BOM, run MuJoCo, powder-spreading simulations and theory, Edison second opinions and pain points from
similar systems, simulate every assembly, use, maintenance and swap operation, use real parts, make sure the seals
seal, use Shigley, heat transfer and CalculiX, and say what the machine costs used and with cheaper equivalents.

Nothing here has been built, quoted by a shop, or reviewed by BYU's Laser Safety Officer or EHS. Each note below has
its own sources, assumptions and re-run instructions.

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
