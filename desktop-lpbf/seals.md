# Sealing the gas envelope: every seal checked, and what has to change

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

## 1. Short answer

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
It has 21 rows:
- **OK:** 2;
- **CHECK:** 7. They work, but a number needs fixing;
- **FIX:** 5. They won't seal or won't hold as drawn;
- **MISSING:** 7. A hole through the envelope with no seal drawn.

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
