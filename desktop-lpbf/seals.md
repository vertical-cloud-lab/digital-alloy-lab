# Sealing the gas envelope: every seal checked, what had to change, and what the model now has

Written 2026-11-20 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to
"make sure things that are meant to be sealed are sealed properly". Nothing here has been built or leak-tested.

| File | What it is |
|---|---|
| [`analysis/seals/seals.py`](analysis/seals/seals.py) | inventory of every seal and hole through the gas envelope; Parker gland checks with tolerances; closure forces; permeation and outgassing budget; pump-down; powder lift while pumping; rate-of-rise test → [`analysis/out/seals/seals.md`](analysis/out/seals/seals.md) |
| [`analysis/seals/door_seal_fea.py`](analysis/seals/door_seal_fea.py) | CalculiX: the door held at its latches and hinges against its own O-ring at +20 mbar → [`door_seal_fea.md`](analysis/out/seals/door_seal_fea.md) |
| [`analysis/mech/mech_checks.py`](analysis/mech/mech_checks.py) | the Z coupling's friction budget, screws and latches, chamber warm-up, cover-slide thermal lens → [`mech.md`](analysis/out/mech/mech.md) |

The machine has to hold two quite different states:
- **pumped to ~1 mbar** for the purge cycles, where the full atmosphere pushes in and leaks run inward;
- **+5 to +20 mbar of argon** for hours during a build. Here bulk leaks run outward, but O₂ and water still come in by
  permeation and back-diffusion. A closure that only the atmosphere was holding shut now has only its latches.

## 0. What the model now has (added 2026-11-20)

Every fix in §3 is now drawn in the low-profile model (`cad/lpbf_low.py`, `modules_low.py`, `module_params.py`, `joints.py`).
Each gland the model draws is registered in `lpbf_low.GLANDS`, and `analysis/seals/seals.py` checks every one of them (results:
[`seals.md` (results)](analysis/out/seals/seals.md), gland table). Part numbers, prices and sources are in
[`seal-parts.csv`](seal-parts.csv). O-rings are AS568 FKM (Viton) 75A, McMaster's 9464K family, read through the lab Pi on 2026-11-20.

| Item | Now in the model | Parts (McMaster unless noted) | Check | Still open |
|---|---|---|---|---|
| 1. Reservoir | 2-040 face O-ring in the dock face round a 12 × 100 mm opening. One 30 × 112.4 mm base plate for S, M and L. Rail lips over the plate's edges. Welded 304 top frame with an O-ring-sealed lid on 2 × M3 in blind holes. Shutter slot closed at both ends. NFC antenna moved to the dock's side face. | 2-040 9464K825; lid rings 2-022 9464K492 (S), 2-030 9464K774 (M), 2-042 9464K849 (L); detent 85015A47 | dock O-ring 508 N at 25 %. With 2° ramps under the lips and μ 0.15, the push home is 94 N, pull-out 58 N, self-locking | the ramps and the detent are not drawn (0.5 mm over 15 mm); the shutter's drive through its closed slot (e.g. magnetic) is not designed; μ is assumed |
| 2. Door | 1.78 mm cord in a half-dovetail groove: 1.32 deep, 2.3 wide at the bottom, outer wall undercut 24°. Slotted (±0.6 mm) hinge holes. Two ears at mid-height carry the strikes. Two draw latches on the chamber's side faces, pulling straight back at the seal's centroid height | cord 96515K123 ($1.40/ft); latches 1807A61 (800 lb, adjustable grip) | each latch needs **725 N** of preload at +20 mbar for 25 % squeeze (328 N for 15 %), against a 3.56 kN rating. CalculiX: the door loses ≤ 34 µm of squeeze (margin 178 µm), and the hinges carry nothing ([`door_seal_fea.md`](analysis/out/seals/door_seal_fea.md)) | **the half-dovetail is overfilled**: 94 % nominal, 111 % at worst tolerance when warm, and its 1.71 mm face opening doesn't hold the smallest in-tolerance cord. See note (a) below. Splice: vulcanized, not McMaster's glue kit (9262N11). Robot clamps: see (b) |
| 3. Window | 2-031 under the window in a seat groove, a 1 mm FKM flat ring on top, and a retaining ring whose spigot bottoms metal-to-metal on the flange. 2-036 face O-ring from the flange to the lid. Flange bore Ø42 (the Ø36 field stop still limits the beam) | 2-031 9464K775; 2-036 9464K793 | both glands 25 % (19–31 %) | FKM sheet for the flat ring not sourced |
| 4. Drawer | 2-033 in a half-dovetail on the front plate. The plate is widened to ±64 mm. Two quarter-turn latch studs in the plate, receptacles in the lid between the lid screws. Drawer sensor moved | 2-033 9464K788 | 358 N to squeeze: 180 N per latch | the same overfill as the door. **No catalogue quarter-turn latch fits**: 5210N21 holds 0.53 kN but needs a Ø22 hole; Southco's E3 compact holds 450 N but has a Ø29 head; the 5009N12 holds only 0.36 kN. The latches are drawn as an envelope |
| 5. Spigot, gland plate | spigot groove root Ø90.5 × 4.8. Gland-plate groove 2.6 wide, sized per module so a standard ring sits on the inner wall at 1.5–3.3 % stretch | 2-238 9464K365; 2-024 9464K753 (S25), 2-034 9464K791 (M50), 2-041 9464K836 (L75) | spigot 21 % (17–25 %), ≤ 81 % fill. Gland plate up to 32.2 % squeeze at worst tolerance | gland plate: make it 1.35 deep (now 1.30) to stay under 32 % |
| 6. Rod gland | two Parker rod grooves Ø20.0, throat Ø15.93, 3.6 wide (S25: 2-110, Ø13.64). The gland plate is now **14 mm thick (was 10)** to hold them with 2.3 mm lands. Rod labelled seamless, polished Ra ≤ 0.2 µm | 2-114 9464K982; 2-110 9464K977; 6 × M4 × 20 (was × 16) | 21 % (16–25 %), ≤ 82 % fill at 110 °C | friction against the Z coupling (§4) |
| 7. Rod end | the end cap is now 19 mm (rod end 24 mm, was 14) with a side boss: Ø12 bore, 2-014 face O-ring, connector envelope | envelope: LEMO 1B hermetic receptacle HGG.1B.310 (M12 × 1) | – | **the LEMO part misses the spec** (2 A per contact, 1e-7 mbar·L/s). The parts that meet it are KF-16 feedthroughs: Accu-Glass 9C-K16 ($324, 9 pins, 5 A) for the heaters and MPF A0408-2-QF ($361.63, 2 type K pairs). They need a KF-16 port on the rod end, which doesn't fit the Ø22 cap. The 2-014 ring isn't confirmed at McMaster |
| 8. Shafts | recoater: Ferrotec SFL-006-NN magnetic-fluid feedthrough (Ø52 flange, Ø28 housing, 82 mm, 15 mm vacuum shaft) on a 9 mm spacer ring (2 × 2-024), with a clamp coupling to the screw inside the wall bore; the servo moved 41 mm outboard on a 25 mm standoff. Roller: Ferrotec SSL-005-NN (Ø16, M8 × 1 nose, 65.5 mm) with a 2-012 shoulder ring; stepper moved back | Ferrotec prices not published; Rigaku FD-F1-KF25-0250-LC $921.57 is a priced alternative | – | how the overall lengths split between flange, housing and air shaft is assumed. Check the axial load rating of the SFL-006 against the ball screw. 2-012 not confirmed |
| 9. Ports | argon in, O₂ sample, transducer and relief valve are SAE J1926 -4 (7/16-20) O-ring-boss ports (thread, 12° O-ring chamfer, Ø4 drilling). The vacuum port's KF-25 stub is welded into a 304 adapter plate, bolted with 4 × M5 over a 2-024 | fittings 5182K862 ($21.77); port O-rings AS568-904 5267T786 | – | the transducer and relief valve must come with SAE-4 male ends (not confirmed) |
| 10. Other holes | inlet plenum: a bolting flange, 9 × M4, 2-044. Outlet plenum: 10 mm flanges each side of the opening, 6 counterbored M4, 2-044. Overflow funnel: 4 counterbored M4, 2-042 (316L is never welded to 6061). Metering base on the lid: 2-040. Camera adapter: 2-022. Camera window: 2-017 plus an FKM flat ring under a screwed retaining ring. Fibre heads: M6 threaded heads with 2-010. Right recoater bearing: blind cap with 2-019. The side reservoir port is a KF-16 machined in the 6061 base | as listed | all 1.78 mm face glands: 25 % (19–31 %) | see (c). The camera boss now sits on the line of sight; the old Ø22 bore broke through its wall. Fibre head part not chosen |

Notes:
- **(a) Half-dovetails.** With a 1.78 mm cord at 26 % squeeze, a half-dovetail can't both hold the cord and stay under 90 % fill.
  - Holding the cord needs a face opening below 1.70 mm (the smallest cord in tolerance). With a 24° wall, the groove's area then gives 94 % fill nominal.
  - Options:
    - use a 2.62 mm cord in Parker's half-dovetail table. The door then needs about 2.1 kN, still under the 2.4 kN the atmosphere gives at vacuum, and about 1.05 kN per latch;
    - use a plain 1.32 × 2.6 groove and let gravity hold the cord. The door's face points up when it is open, but the drawer's doesn't.
- **(b) Robot clamps.** McMaster's 5174A35 pneumatic hold-down is 143 × 40 × 41 mm. It is rated 100 lb (0.445 kN), but only at its 40 psi maximum, so it is marginal against the 0.73 kN needed. DE-STA-CO's 802-U (890 N, $225, with the 8EA-109-1 reed sensor) is 191 mm long.
  - The left side face has 156 mm free in front of the feedthrough. The right side has only 80 mm (y −110 to −30) before the vacuum port's KF clamp.
  - So the room for pneumatic clamps is not there on the right side as drawn. Move the vacuum port back, or mount the clamp on a bracket at the front corner.
- **(c) Gland fill.** Every new face gland uses Parker's gas and vacuum width for 1.78 mm (2.3 mm). With the AS568 cross-section tolerance (±0.076 mm) and ±0.05 mm machining, it fills to 93–95 % at worst tolerance when warm.
  - That is not an overfill, but it is above the 90 % this note uses as a margin.
  - Widening to 2.6 mm (Parker's liquid column) brings it to about 86 %, as done for the gland plate. This is not yet applied to the other grooves.
- **Interference:** 0 interferences in all 5 static states and all 8 motion sweeps, for M50/M, L75/L and S25/S
  ([`interference.md`](analysis/out/interference.md), [`variants/`](analysis/out/variants/); about 3 min each).
  - The 0.00 mm "gaps" are designed contacts: the reservoir plate on the dock O-ring, the drawer studs in their receptacles, the striker on the magnet.
  - In reality the reservoir plate rides 0.5 mm higher until it reaches the ramps. The sweep moves it at the docked height, touching the ring.
- **Mass:** the tray load is 266.4 kg (was 264.5 kg). The process module is 84.2 kg (was 82.3 kg).
- **Changed by the seals:**
  - the gland plate (14 mm) and the rod end (24 mm) make the rod 14 mm longer, so the Z stage hangs 14 mm lower. Its lowest point is 10 mm above the tray;
  - the module now rises at y −158 (was −170), so the L75 handle clears the guard's bottom front rail;
  - the module's last move out of the guard is now at z +4 (was −10), so the rod end clears the guard's sill rail.

## 1. Short answer (the review that led to §0, before the fixes were drawn)

**Three things would stop the machine purging or holding its atmosphere as drawn:**

1. **The reservoir is open to the room.** Its lid is a loose plate, nothing seals it to the metering base, and its shutter is a powder gate, not a gas seal. The powder column and the roller clearance are an open path into the chamber.
   - At +20 mbar, Darcy flow through 40 mm of powder over the 8 × 70 mm slot carries **~300 sccm of argon out**. That is a superficial velocity of 8.9 mm/s, three times the 2.8 mm/s that fluidizes 38 µm Al powder, so the reservoir would bubble and vent.
   - Pumping down, **~9 L/min of room air** is pulled through the powder: the purge can't get below a few hundred mbar, and the powder is dragged into the roller.
   - Fix: an FKM face seal on the dock face around the slot, an O-ring-sealed reservoir lid, and a clamp that pulls the reservoir down onto the dock seal (§3).
2. **The window isn't held down.** It sits loose on its O-ring with a 2 mm gap under the retaining ring. At +20 mbar the window carries 3.3 N upward against its 0.35 N weight, so it lifts and the seal opens. The window flange also has no seal to the lid.
   - Fix: clamp the window between two O-rings, with the retaining ring bottoming metal-to-metal so the squeeze is set by the geometry, and add a face O-ring under the flange.
3. **The rod-end "potted cable exit" leaks along the strands.** Stranded heater and thermocouple leads wick gas along the strands through any potting compound.
   - Fix: a glass-to-metal hermetic connector in the rod end cap, or solid pins potted with their insulation stripped.

**Closures whose holding force was never sized:**

4. **The door.**
   - Squeezing its 3.53 mm FKM 75A cord 25 % along the 669 mm seal takes ~2.8 kN (Lindley's relation with Gent's modulus, within Parker's chart range of 1.5–6.4 kN). That is more than the 2.4 kN the atmosphere puts on the door at full vacuum, which seats it at ~23 %.
   - During a build only the latches hold it. At +20 mbar they must each carry **~800 N to keep 25 %**, or ~350 N to keep 15 %. The FEA had sized them for 60 N.
   - CalculiX shows the 15 mm door itself is stiff enough: **≤ 26 µm of squeeze lost** at the top centre, against 350 µm of margin.
   - The groove as drawn (2.8 deep × 4.0 wide) is not the specified 2.65 × 4.6. It fills to 97 % at worst-case tolerance when warm.
5. **The cover-slide drawer.** Its O-ring needs ~350 N to squeeze, but nothing clamps the drawer, and +20 mbar pushes it out.

**Grooves to correct:**

6. **The spigot's 2-238 radial groove** (root Ø90.2, 3.6 mm wide) is **overfilled at worst tolerance (101 %)**, and its squeeze is light (13–21 %).
   - Make it root Ø90.5 × 4.8 wide: 17–25 % squeeze, ≤ 81 % fill.
7. **The gland plate's 1.78 mm face groove** (2.4 wide) reaches 94 % fill. Widen it to 2.6 mm.
8. **The rod gland has no grooves drawn.** Specify two 2-114 grooves (Ø20.0, throat Ø15.93) and a seamless, polished rod. Their friction is the problem in §4.

**Penetrations with no seal drawn:**
- the metering base on the lid;
- the camera adapter and its window;
- the inlet and outlet plenums (316L on 6061: bolt and O-ring, never weld);
- the right-hand recoater bearing housing, whose bore is open to the room;
- the through-beam fibre heads in both side walls;
- the KF stubs where they meet the body.

**Seals that work, but are the wrong kind for vacuum:**
- **The two rotary shafts** (recoater screw, metering roller) run in PTFE V-rings. A V-ring is a dirt excluder, not a vacuum seal. Use magnetic-fluid feedthroughs, or a magnetic coupling through a sealed can.
- **NPT threads into 6061** (argon inlet, O₂ sample, transducer, relief valve) leak at vacuum and gall. Use O-ring-boss (SAE J1926 / ISO 1179) ports, VCR or KF.

**What is fine:** the lid (20 × M5 give ≥ 48 kN against the 4.1 kN the O-ring needs), the KF joints, the FKM choice, the body machined from solid (no welds to leak), and the permeation budget (§5).

## 2. Every seal and penetration

The full table, with status and the reason for each, is the first table of [`seals.md` (results)](analysis/out/seals/seals.md).
Before the fixes it had 21 rows: 2 OK, 7 CHECK (works, but a number needs fixing), 5 FIX (won't seal or won't hold as drawn) and
7 MISSING (a hole through the envelope with no seal drawn). With the fixes drawn (§0) it has 22 rows:
- **OK:** 14;
- **CHECK:** 8. Drawn, with an open item: the door and drawer half-dovetails, the drawer latches, the reservoir's ramps and shutter drive,
  the rod glands' friction, the rod-end connector, the fibre heads, and the gas loop and O₂ analyser (unchanged);
- **FIX** and **MISSING:** none.

## 3. The fixes, closure by closure

| Closure | Change | Why |
|---|---|---|
| Reservoir | 1.78 mm FKM face O-ring in the dock face round the slot; O-ring-sealed lid; a cam or toggle clamp (or the robot's push plus a detent cam) that pulls the reservoir down onto the seal; dock shutter stays a powder gate | removes the open path; the reservoir becomes part of the envelope and is purged with it |
| Door | 1.78 mm FKM cord in a half-dovetail groove (Parker: depth 1.32, width 2.3), so the cord stays put when the door opens; floating hinges (slotted holes); latches set to ≥ 0.4 kN each; for the robot, two pneumatic over-centre clamps with a clamp-closed sensor | halves the squeeze force (1.4 kN at 25 %), so vacuum seats it fully and two latches hold it at +20 mbar |
| Window | O-ring sandwich (1.78 mm under, a thin FKM or PTFE ring over), retaining ring screwed to a metal stop; a face O-ring between flange and lid | +20 mbar lifts a floating window |
| Drawer | 1.78 mm cord in a half-dovetail on the drawer face; two quarter-turn cam latches (or a robot-pushed toggle) giving ≥ 0.4 kN | nothing holds the drawer against its own seal |
| Spigot | groove root Ø90.5, width 4.8 | overfill at tolerance; light squeeze |
| Gland plate | groove width 2.6 | 94 % fill |
| Rod | two 2-114 grooves, seamless polished 316 rod (or an edge-welded bellows) | grooves not drawn; friction (§4) |
| Rod end | hermetic connector | stranded leads leak |
| Shafts | magnetic-fluid feedthroughs (or magnetic couplings) | V-rings don't seal vacuum |
| Ports | O-ring-boss or VCR/KF instead of NPT | thread leaks and galling |
| Plenums, metering base, camera, right bearing, fibre heads | face O-rings and a blind bearing cap | holes with no seal |

## 4. The Z coupling and the rod seals

The rod gland and the bore seal have friction, and the pot magnet has to pull the piston down against it every layer
([`mech.md`](analysis/out/mech/mech.md) §A):
- **two 2-114 rod O-rings:** 28–43 N running (Parker Fig. 5-9, 75A, oil basis), and up to ~190 N to break away after a dwell. That allows for running dry in argon and Parker's 3× break-out after a rest;
- **the bore seal and the rim wiper:** another 13–80 N (assumed; to be measured);
- **the magnet:** rated 196 N on thick mild steel, but on a 430 SS striker at 68 °C with a little debris it gives ~74–138 N.

So the margin is 0.5–3.8 running and **0.2–0.5 after a dwell**. If the plate sticks while the arm drops, the magnet lets
go, the plate isn't lowered, and the blade drags the next layer over the part.

The coupling has to be rigid in both directions; [`hot-swap.md`](hot-swap.md) already recommends a switched, fail-safe
coupling. On the seal side, a single rod O-ring with an edge-welded bellows outside it, or PTFE-capped rod seals, cuts the
friction by 2–5×. Measure the break-out force on the first module before trusting any number here.

## 5. Leak, permeation and outgassing budget

From [`seals.md` (results)](analysis/out/seals/seals.md):
- **The envelope is 11.3 L:**
  - chamber 6.4 L;
  - HEPA housing 2.3 L;
  - hoses 1.5 L;
  - plenums and blower 1.1 L.
- **Permeation through every FKM seal adds 1.7 ppm O₂/h and 2.7 ppm H₂O/h**, using Parker's leak-rate approximation, Arrhenius-scaled to each seal's temperature. 35 sccm of Ar 5.0 make-up flow holds 10 ppm O₂ against it, about 2 L/h.
- **Wall outgassing dominates the water** (unbaked 6061 and FKM after ~1 h, O'Hanlon): ~19 ppm H₂O/h, falling roughly as 1/t. ~33 sccm of make-up holds a −40 °C dew point against it.
- **The powder can swamp all of that.** 150 g holding 50–300 ppm water by mass carries 8–45 mg, which is 830–5,000 ppmv in the loop if a 200 °C plate drives it off.
  - So dry the powder (vacuum oven) and load it dry.
  - Fit the dew-point sensor (BOM line G9).
  - Budget either a purifier (molecular sieve plus a getter) on the loop, or a larger make-up bleed while heating.
- **Real leaks, not permeation, decide the O₂.** A single elastomer rotary seal at 1e-4 mbar·L/s, held at vacuum, lets in ~6 ppm O₂/h; at 1e-3, 60 ppm/h. Hence the feedthroughs in §3.

## 6. Purge and the powder

- **Pump-down.** The McMaster 4396K21 (3 cfm, 1.42 L/s) through two KF-25 bellows reaches 1 mbar in **~1 min**.
- **Two cycles reach ~1 ppm O₂ in theory**, at the limit of Ar 5.0 purity. Plan three, with a hold at ≤ 1 mbar, to drain the powder's pores and the walls.
- **Pumping that fast lifts powder.** At atmospheric pressure the pump-down time constant is 8 s. The gas leaving a powder bed then pushes on it with 0.42 × the bed's weight for a 40 mm bed, 0.59 for the L reservoir and **0.95 for the 90 mm overflow jar** (Kozeny–Carman, Klinkenberg slip).
  - **Throttle the first stage:** a needle-valve bypass ("soft pump") that keeps τ = V/S ≥ 25 s until ~100 mbar. Pump-down grows to ~3 min.
  - **Throttle the back-fill too**, with a diffuser, so the argon inrush doesn't blow the bed.

## 7. Acceptance test: rate of rise

- **Method.** After ≥ 1 h at ≤ 1 mbar, close the pump valve and log the pressure for 10 min with a Pirani or capacitance gauge. The 0–15 psia transmitter in the BOM can't resolve this.
- **Expected rise:**
  - the leak budget of 1e-4 mbar·L/s gives 5e-4 mbar/min;
  - outgassing at that time adds about 3e-4 mbar/min.
- **Pass:** the rise is under ~1e-3 mbar/min. A larger rise is a leak; find it with an argon or helium spray and a leak detector.

## Sources

Listed at the end of [`analysis/out/seals/seals.md`](analysis/out/seals/seals.md) and [`analysis/out/mech/mech.md`](analysis/out/mech/mech.md):
- Parker ORD 5700: design charts, leak-rate approximation, friction;
- Lindley and Gent: O-ring load;
- O'Hanlon: outgassing and conductance;
- Kozeny–Carman, Klinkenberg and Ergun: powder beds.
