# Build, test and use: option B (316L cup on a 3 in tri-clamp)

How to make, check and run the lab-built cup in `README.md`. The numbers come from `params.py`, the drawings in
`cad/drawings/`, the CAM in `cam/` and the analyses in `analysis/` (`analysis/out/*_summary.md`). Steps marked
**(measure)** need a person at the machine before anything is ordered or cut.

B comes in two welded parts:
- **The upper part** is the KF-50 stub, the 3×2 in reducer and a 3 in tri-clamp ferrule. It stays clamped on the
  cone's KF-50 outlet, with the centring ring and over-pressure ring, between runs.
- **The pot** is a 3 in ferrule, the 3 in tube and the turned end cap, with a catch puck and a liner inside. It
  hangs from the upper part on a 3 in tri-clamp, comes off after every run, and is carried away capped.

The puck (Ø70) and liner (Ø69.85) go in and out through the pot's 72.9 mm ferrule. They could not go through the
47.5 mm KF neck, which is why the cup splits.

## 0. Before ordering: three checks

1. **(measure)** The room under the cone: the distance from the cone's KF sealing face to the mat, with the cone
   latched. B is drawn 250 mm long, assuming about 300 mm of room (`Z_JOINT_FACE`, never measured). The pot must
   clear the mat by at least 25 mm, plus the few mm it drops to come off. If the room is smaller, shorten the
   pot's tube (`B["body_len"]`). Each 10 mm costs about 35 cm³ of capacity, and the pile then sits closer to the
   tri-clamp gasket.
2. **(measure)** The cone's flange OD (74.9 mm for KF-50), and the size stamped on the clamp. `dims/` reads KF-50
   from the photos, with medium-high confidence.
3. **(check)** That AMAZEMET's cone shields are in the lab: thin discs about 200 mm across that lie in the cone's
   mouth (training video 5, 2:15–3:05). The design relies on them. AMAZEMET: one for aluminium, more for
   copper alloys.

## 1. Order

The parts list is `BOM.md`, and alternatives are in `bom/README.md`.
- **KF stub:** Lesker's 316L stub isn't stocked. Use a 304L stub (A&N 4000126 or Lesker QF50-200-SST) or
  McMaster's 304 stub 4518K38; any of these welds to 316L with ER316L.
- **Sanitary parts:** the 3 in ferrules, clamp, PTFE gaskets and caps (B13, B24–B27) are standard 3-A / ASME BPE
  items. They weren't priced here.

## 2. Machine

| Part | Machine | Program | Check |
|---|---|---|---|
| End cap Ø76.2 × 20, 316/316L: 8 mm floor, 12 mm rim at the tube's wall, R6 inside corner | lathe (blind pocket) | `cam/gcode/B_bottom_cap_op1.nc`, `_op2.nc` | `cam/out/lathe_B_bottom_cap.png` |
| Pot tube, 3 in × 0.065, faced square to 82.35 | lathe (spider in the bore) | `B_body_tube_op1/2.nc` | `lathe_B_body_tube.png` |
| Liner, 2-3/4 in × 0.065 304, faced to length | lathe (collet or soft jaws) | `B_liner_op1/2.nc` | `lathe_B_liner.png` |
| Catch puck Ø70 × 25, 304; 6×45° underneath (clears the R6), 2×45° on top | lathe | `B_puck_op1/2.nc` | `lathe_B_puck.png` |
| Weld-alignment V-block, 6061 | mill, 2 setups | `fixture_op1.nc`, `fixture_op2.nc` | CAMotics, `cam/out/mill_fixture_sections.png` |

The programs are Haas/LinuxCNC-style metric G-code. Prove them out in the shop's own CAM or simulator, at the
shop's own speeds and feeds, before the first cut. Deburr everything. The liner must drop into the pot freely: the
gap is 1.5 mm a side when cold, and the FEA leaves at least 1.1 mm when hot.

## 3. Weld (TIG, by a person qualified on thin stainless)

1. Clean every part with acetone, inside and out. Use stainless-only brushes.
2. **Upper part:** stub + reducer + ferrule.
   - Fold a 0.025 in (0.64 mm) stainless shim to 90° and lay it in the V-block at the flange end.
   - Lay the stub and reducer in the V, with the flange rim on the shim at the block's x = 0 end. The reducer's
     3 in end rests in the V.
   - Fit the ferrule to the reducer's 3 in end, face outward. It overhangs the block's far end: its 90.9 mm
     flange is wider than the V, so the block is only 120 mm long.
3. **Back-purge** each part:
   - tape over the open ends, feed argon at 5–10 L/min through a hole in one tape, and vent through the other;
   - purge at least 2 min (about 10 volume changes) before striking an arc;
   - keep the purge on until each weld is below about 300 °C.
4. Tack each seam three times, 120° apart.
   - W1: the stub's end to the reducer's 2 in end, 19.05 mm from the sealing face.
   - W2a: the reducer's 3 in end to the ferrule.
5. Weld, rolling the part in the V.
   - Full penetration on 1.65 mm wall: pulsed DCEN at about 40–60 A, with a 1/16 in ER316L rod or autogenous with
     a good fit-up.
   - Keep the heat input at or below about 0.5 kJ/mm, in short balanced segments (Edison's final check).
   - Clamp a copper chill round the KF flange for W1, and round the ferrule's face for W2a.
6. **Pot:** ferrule + tube + end cap.
   - Lay the tube and end cap in the V (no shim; both are 76.2 OD), with the ferrule overhanging the x = 0 end.
   - W2b: the ferrule to the tube's top, chill on the ferrule face.
   - W3: the tube's bottom to the end cap's rim, wall to wall, 20 mm above the bottom. The cap's turned R6 inside
     corner takes the floor's thermal stress, so don't add a fillet bead inside.
7. Check the inside of every weld with a borescope: full penetration, no sugaring, no drop-through. Then pickle or
   passivate the welds.
8. **Faces and alignment:**
   - Check the KF sealing face and both ferrule faces are flat (straight edge and a 0.05 mm feeler), unscratched,
     and free of weld spatter.
   - The bore must run true to the KF flange within about 0.3 mm TIR; above about 0.5 mm the centring ring may
     not seat.
   - Dye-penetrant check the welds if the shop has it.

## 4. Pressure and leak tests

MAWP is set at +0.8 bar gauge, the chamber's relief setting.

| Test | How | Pass |
|---|---|---|
| Hydro proof, once per welded part | **Pot:** water-fill, close it with the 3 in tri-clamp cap with a port (B13), a gasket and the clamp. **Upper part:** the same cap at the bottom, and the KF-50 blank (B9) with the centring ring, the over-pressure ring (B7, rated 50 psig) and a clamp on top. Pressurise to 1.2 bar gauge (1.5 × MAWP; the ASME VIII-1 minimum is 1.3 ×) through the B14b rig, which includes a relief valve set at about 1.5 bar. Hold 10 min, then drain, dry and passivate | no drop on the gauge, no weep. Edison prefers this to a pneumatic proof test |
| Bench soap test | the same closures, with argon at +0.3 bar from a regulator. Snoop on every weld and joint, then rinse and dry | no bubbles in 2 min |
| On the machine: rate of rise | cup installed, chamber pumped to full vacuum, pump valved off, gauge logged for 5 min. Record a baseline the first time and trend against it; some furnace-to-chamber leak through the graphite seals is normal | Edison's project-specific targets for 10–20 L are about 0.04 mbar/min (gross) and 0.004 mbar/min to purge well. If the HMI can't resolve that, the baseline trend still shows a Nov-13-size leak, which climbs about 25–30 mbar/min |
| On the machine: soap at overpressure | chamber at its normal +150 mbar | no bubbles at the KF joint, the tri-clamp or the welds |
| AMAZEMET's one-minute rule | after a refill above +50 mbar, with the sensor's argon bleed flowing (blue cabinet) | O₂ below 1000 ppm within a minute and falling steadily |

The FEA's stresses at these pressures are small: 9.5 MPa at +1.2 bar and 9.0 MPa under full vacuum, against a
172 MPa yield. The joints are the weak points.
- **KF joint:** standard KF rings are rated by Pfeiffer and Edwards only to about 1.5 bar absolute, and the relief
  opens at about 1.8 bar absolute. So the over-pressure ring is part of the design, not optional.
- **Tri-clamp:** sanitary clamps are pressure-rated (McMaster's: 450 psi).
- **Written ratings:** ask the KF vendor for its rating with the over-pressure ring (Edison's final check).

## 5. Fit out (on the bench)

1. Put the puck in the pot, chamfered side down, then the liner, which stands on it.
2. **Thermocouples:** Auber TC-K-WS washer probes, each under an all-stainless worm clamp with a band about 9 mm
   wide (B12).
   - **Top:** on the stub's straight tube, centred between the flange hub and W1. This stays on the upper part.
   - **Bottom:** on the end cap's rim, 13.5 mm up from the bottom face (clear of W3 at 20 mm). This one comes off
     with the pot.

   Keep the fibreglass leads (316 °C) off the hot wall. Use a mini connector on the bottom lead so the pot can be
   unplugged.
3. Connect both to the 2-channel meter (Auber SYL-2813AC, in a fused enclosure: B15b). Each channel's relay
   drives the buzzer. A washer probe outside the wall lags the inside in a fast transient. Log both channels if
   the lab can (any USB type K logger), and keep the traces with the run record.

| Channel | Alarm | What the FEA says it means |
|---|---|---|
| Top | **120 °C** | With the pile in the pot, the top stays at 26–46 °C even for 816 g of shot. 120 °C means hot metal is held near the KF joint, the Nov 13 failure mode. **It can't save the O-ring:** with 25 g of shot fused in the bore just under the joint, the O-ring passes 150 °C at 3 s and this alarm sounds at 4 s. Stop the pour, and replace the O-ring afterwards. |
| Bottom | **150 °C** | Shot is in the pot. It sounds 144 s after 816 g lands and 165 s after 400 g. A good run's powder (816 g arriving at 400 °C) peaks at 87 °C. 100 g of shot peaks at 107 °C, so no alarm doesn't prove there was no shot. **The stop rule during the pour stays visual:** if the plate isn't making powder within 20–30 s, close the sealing rod. |

## 6. Install

**Once** (and after any work on the KF joint): the upper part.
1. Shields in the cone's mouth: at least one for aluminium, more for copper alloys as AMAZEMET advises.
2. **Take the KF clamp off; don't leave it hanging open.** The collision check (`cad/out/build_collisions.json`)
   shows a hinged clamp opened to 110° still blocks the flange.
3. Two people: lift the upper part straight up under the outlet. Seat the centring ring (stainless, FKM O-ring),
   fit the over-pressure ring round the O-ring, and close the KF clamp finger-tight. The hand calculation gives
   about 1.8 kN of clamping, against 0.84 kN of separating force at +1.2 bar.

**Every run:** the pot.

4. Pot fitted out (step 5). Fresh PTFE gasket on the ferrule if the last run was a bad one.
5. Lift the pot under the upper part, fit the gasket, close the 3 in tri-clamp, and plug in the bottom
   thermocouple.
6. Hang a stainless safety lanyard from the pot to the frame, slack, so a failed clamp can't drop it (Edison).
7. Check the pot hangs straight and the leads are clear of the door and the frame.

## 7. Run limits

- **KF O-ring:** B keeps it at 26 / 30 / 40 °C for 100 / 400 / 816 g of shot on the puck.
- **Gasket, the limit:** the tri-clamp gasket reaches 47 / 116 / 263 °C. It passes 200 °C at about 640 g of shot,
  so FKM is fine to about 630 g and **PTFE (260 °C) to about 800 g**.
  - With the shields in and the stop rule kept, a bad run shouldn't put the whole charge into the cup.
  - If it does, replace the gasket. It's a $3 part, and the joint is a sanitary one, not the chamber's seal.
- **Charge size:** 816 g, the Nov 13 charge, is the largest case run. Larger charges hold proportionally more
  heat.
- **Option A, if used in the meantime:** it takes about 120 g of copper-alloy shot before its bottom O-ring passes
  150 °C (`README.md`).
- **Still in force:** the O₂ hard stop and the plate stop rule from the Nov 13 analysis. This cup survives a bad
  run; it doesn't make one good.
- **Nothing inside the top:** don't add a splash plate, valve or any ledge inside the upper part. The Nov 13 seat
  burned because hot shot piled on a splash plate and valve right under the seal. In B the bore only widens below
  the KF joint.

## 8. After the run

1. Wait until the bottom thermocouple reads **below 60 °C** before you open anything.
   - After a full charge of shot, the FEA's bottom thermocouple still reads about 156 °C an hour later.
   - After a good powder run it reads about 72 °C at an hour, and falls from there.
2. Unplug the bottom thermocouple and unclip the lanyard. Open the tri-clamp, lower the pot (a few mm clears the
   gasket), and fit the plain 3 in cap (B27) to carry it under argon. The upper part stays on the cone.
3. Empty the pot over a sieve or tray; the puck and liner come out with the powder.
   - If metal is welded on, replace the puck or liner.
   - If the shot fused into a lump, it comes out through the 72.9 mm opening, or with the liner.
   - Self-mated stainless can gall in argon, so keep the edges rounded and the 1.5 mm gap. Don't use hydrocarbon
     anti-seize: it would end up in the powder.
4. **Replace parts after alarms:**
   - **Top alarm sounded:** replace the KF O-ring. In a hang-up the O-ring runs hotter than that thermocouple.
   - **Bottom alarm sounded:** replace the tri-clamp gasket. Look at the liner and the end cap.

## 9. What each check is based on

| Claim | Where |
|---|---|
| Seal, gasket and wall temperatures for 100–816 g of shot, a good run and a hang-up | `analysis/thermal.py`, `analysis/out/thermal_summary.md` |
| Energy conservation and the pile's mass in the model | `analysis/energy_check.py`, `analysis/out/energy_B_816.json` |
| Stresses: pressure, vacuum, the hot pot | `analysis/structural.py`, `analysis/out/structural_summary.md` |
| Clamp force, buckling, flat-head thickness, hot clearances | `analysis/handcalcs.py`, `analysis/out/handcalcs.md` |
| Install and removal paths at the KF joint | `cad/build_gif.py`, `cad/out/build_collisions.json` |
| Interfaces | `dims/README.md` (photos and video frames), `bom/vendor_dims.json` (vendor drawings) |
| Design review and precedents | `edison/` |
