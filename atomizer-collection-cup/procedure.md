# Build, leak test and use: option B (welded 316L cup)

How to make, check and run the lab-built cup in `README.md`. The numbers come from `params.py`, the drawings in
`cad/drawings/`, the CAM in `cam/` and the analyses in `analysis/`. Steps marked **(measure)** need a person at
the machine before anything is ordered or cut.

## 0. Before ordering: three measurements

1. **(measure)** The room under the cone: the distance from the cone's KF sealing face to the mat, with the
   cone latched. B is drawn 250 mm long, assuming about 300 mm of room (`Z_JOINT_FACE`, never measured). The cup
   must clear the mat by at least 25 mm, plus the 5 mm drop needed to remove it. If the room is smaller,
   shorten the 3 in body tube (`B["body_len"]`). Each 10 mm off the tube costs about 42 cm³ of capacity.
2. **(measure)** The cone's flange OD (74.9 mm for KF-50), and the size stamped on the clamp. `dims/` reads
   KF-50 from the photos, with medium-high confidence.
3. **(check)** That AMAZEMET's cone shields are in the lab: thin discs about 200 mm across that lie in the cone's
   mouth (training video 5, 2:15–3:05). The design relies on them. AMAZEMET: one for aluminium, more for
   copper alloys.

## 1. Order

The parts list is `BOM.md`; alternatives and stock levels are in `bom/README.md`. McMaster lines deliver in 1–3
working days. Lesker's 316L stub is not stocked, so use a 304L stub (A&N 4000126, Lesker QF50-200-SST or
McMaster 4518K38). 304L welds to 316L with ER316L filler.

## 2. Machine

| Part | Machine | Program | Check |
|---|---|---|---|
| End cap Ø76.2 × 20, 316L: 8 mm floor, 12 mm rim at the tube's wall, R6 inside corner | lathe (blind pocket) | `cam/gcode/B_bottom_cap_op1.nc`, `_op2.nc` | `cam/out/lathe_B_bottom_cap.png` |
| Body tube 3 in × 0.065, faced to length | lathe (spider in the bore) | `B_body_tube_op1/2.nc` | `lathe_B_body_tube.png` |
| Liner 2-3/4 in × 0.065 304, faced to length | lathe (collet or soft jaws) | `B_liner_op1/2.nc` | `lathe_B_liner.png` |
| Catch puck Ø70 × 25, 304 (or OFHC Cu for copper alloys), 6×45° underneath to clear the R6 corner | lathe | `B_puck_op1/2.nc` | `lathe_B_puck.png` |
| Weld-alignment V-block, 6061 | mill, 2 setups | `fixture_op1.nc`, `fixture_op2.nc` | CAMotics, `cam/out/mill_fixture_sections.png` |

The programs are Haas/LinuxCNC-style metric G-code. Prove them out in the shop's own CAM or simulator, at the
shop's own speeds and feeds, before the first cut. The tools assumed are listed in `cam/lathe_cam.py` and
`cam/mill_cam.py`. Deburr everything. The liner must drop into the 72.9 mm bore freely: the gap is 1.5 mm a
side, and the FEA shows at least 1.2 mm of it left when hot.

## 3. Weld (TIG, a person qualified on thin stainless)

1. Clean every part with acetone, inside and out. Use stainless-only brushes.
2. Fold a 0.025 in (0.64 mm) stainless shim to 90° and lay it in the V at the flange end. Lay the stub, reducer
   and tube in the V, with the flange rim on the shim and the sealing face flush with the block's end. Tube and
   flange now share an axis (`cam/mill_cam.py`: axis 17.88 mm above the top face). Strap the tube down on the
   four M6 holes.
3. **Back-purge:** tape over the flange bore and the tube's open end, feed argon at 5–10 L/min through a hole in
   one tape and vent through the other, and purge for at least 2 min (about 10 volume changes) before striking
   an arc. Keep the purge on until each weld is below about 300 °C.
4. Tack each seam three times, 120° apart. W1 is the stub's end to the reducer's 2 in end, at 19.05 mm from the
   sealing face. W2 is the reducer's 3 in end to the tube, at 120.65 mm, over the fixture's slot.
5. Weld W1 and W2, rolling the part in the V. Use full penetration on 1.65 mm wall: pulsed DCEN, about 40–60 A,
   with a 1/16 in ER316L rod, or autogenous with a good fit-up. Keep the heat input at or below about 0.5 kJ/mm
   (Edison's final check), and weld in short balanced segments. For W1, which is 19 mm from the sealing face,
   clamp a copper chill block round the flange.
6. Stand the part upright, fit the end cap's rim to the tube's end (both square), purge again and weld W3. W3 is
   wall to wall like W2, 20 mm above the bottom. The cap's turned R6 inside corner takes the floor's thermal
   stress, so don't add a fillet bead inside.
7. Check the inside: full penetration, no sugaring (oxidised root) and no drop-through. Pickle or passivate the
   welds, using citric or nitric gel or the shop's usual process.
8. Check the sealing face is flat (straight edge and a 0.05 mm feeler) and the O-ring area is unscratched. Check
   the bore runs true to the flange within about 0.3 mm TIR; above about 0.5 mm the centring ring may not seat.
   Dye-penetrant check the three welds if the shop has it.

## 4. Leak and pressure test

| Test | How | Pass |
|---|---|---|
| Proof (hydrostatic, once) | the welded body alone, without the KF seal: fill with water, cap with a blank and a code-rated clamp, 1.2 bar gauge for 10 min. That is 1.5 × an MAWP of +0.8 bar, the chamber's relief setting; the ASME VIII-1 minimum is 1.3 ×. Then drain, dry and passivate | no drop on a gauge, no weep. Edison prefers this to a pneumatic proof test |
| Bench soap test | KF-50 blank with a gas port (or a KF-50 to KF-16 reducer and a fitting) on top, centring ring, **over-pressure ring**, clamp. Argon at +0.3 bar from a regulator. Snoop on W1–W3 and the joint, then rinse and dry | no bubbles in 2 min |
| Assembled, optional | same set-up at about +0.9 bar (1.1 × MAWP), staged, behind a barrier | no change in a sealed-off gauge |
| On the machine: rate of rise | cup installed, chamber pumped to full vacuum, pump valved off, gauge logged for 5 min. Record a baseline the first time and trend against it; some furnace-to-chamber leak through the graphite seals is normal | Edison's project-specific targets for 10–20 L: under about 0.04 mbar/min (gross, 10⁻² mbar·L/s), and about 0.004 mbar/min to purge well. A leak big enough to explain the Nov 13 O₂ readings rises about 25–30 mbar/min |
| On the machine: soap at overpressure | chamber at its normal +150 mbar | no bubbles at the joint or welds |
| AMAZEMET's one-minute rule | after a refill above +50 mbar, with the sensor's argon bleed flowing (blue cabinet) | O₂ below 1000 ppm within a minute and falling steadily |

The FEA's stresses in this cup are tiny at these pressures: 6.8 MPa at +1.2 bar and 5.7 MPa under full vacuum,
against a yield of 172 MPa. The joint is the weak point. Standard KF rings are rated by Pfeiffer and Edwards
only to about 1.5 bar absolute, while the relief opens at about 1.8 bar absolute. So the over-pressure ring
(A&N 4000076, 50 psig) is part of the design and is not optional.

## 5. Fit out

1. Drop the puck in, then the liner, which stands on the puck.
2. Thermocouples (Auber TC-K-WS washer probes) under stainless worm clamps:
   - **top**, on the stub's straight tube between the flange hub and W1 (a 10 mm band);
   - **bottom**, 6 mm above the outside of the floor.

   The top clamp may have a zinc-plated screw, which is rated 121 °C. The bottom clamp must be all stainless.
   Keep the fibreglass leads (316 °C) off the hot wall.
3. Connect both to the 2-channel meter (Auber SYL-2813AC). Each channel's relay drives the buzzer. A washer
   probe outside the wall lags the inside by tens of degrees in a fast transient. If the lab can log the two
   channels (any USB type K logger), keep the traces with each run's record; a rate-of-rise trend catches what a
   fixed set point misses.
4. Hang a stainless safety lanyard from the cup to the frame, slack, so a failed clamp or burned O-ring can't
   drop the cup (Edison's final check).

| Channel | Alarm | What the FEA says it means |
|---|---|---|
| Top | **120 °C** | With the pile on the puck, the top stays at 27–51 °C even for 816 g of shot. 120 °C means hot metal is held near the joint, the Nov 13 failure mode. **This alarm can't save the O-ring.** With 25 g of shot fused in the bore under the joint, the O-ring passes 150 °C in 3 s and the alarm sounds at 7 s. It tells you to stop the pour and replace the O-ring. The protection is the geometry (nothing to hang up on) and the shields. |
| Bottom | **150 °C** | Shot is in the cup. It sounds about 2 min after the metal lands (119 s for 816 g of shot, 136 s for 400 g). A good run's powder (816 g arriving at 400 °C) peaks at 86 °C, so the alarm marks a bad run after the fact; hold the cup until it cools. **The stop rule during the pour stays visual:** if the plate isn't making powder within 20–30 s, close the sealing rod. |

## 6. Install

1. Shields in the cone's mouth: at least one for aluminium, and for copper alloys as many as AMAZEMET advises.
2. **Take the clamp off; don't leave it hanging open.** The collision check (`cad/out/build_collisions.json`)
   shows a hinged KF clamp opened to 110° still blocks the cup's flange, 38 interferences along the path. With
   the clamp off, the path is clear.
3. With two people (AMAZEMET's advice), lift the cup straight up under the outlet. Seat the centring ring
   (stainless, FKM O-ring), put the over-pressure ring around the O-ring, then fit the clamp finger-tight.
   The hand calculation gives about 1.8 kN of clamping at finger-tight, against 0.84 kN of separating force at
   +1.2 bar.
4. Check the cup hangs straight, the safety lanyard is clipped, and the thermocouple leads are clear of the door
   and the frame.

## 7. Run limits

- Charge: B takes a full 1.1 kg charge. With the whole 816 g Nov 13 charge arriving as shot and piling on the
  puck, the FEA puts the O-ring at 44 °C and the floor at 348 °C (pile conductivity 2–20 W/m K: 42–45 °C). The
  joint O-ring is the only seal in the cup, and the pile stays 160+ mm below it. Option A, if used in the
  meantime, takes about 120 g of copper-alloy shot before its bottom O-ring passes 150 °C (220 g to 200 °C).
- The O₂ hard stop and the plate stop rule from the Nov 13 analysis still apply. This cup survives a bad run;
  it doesn't make one good.
- Don't add a splash plate, valve or any ledge inside the top of this cup. The Nov 13 seat burned because hot
  shot piled on the splash plate and valve right under the seal. In B the bore only widens below the joint.

## 8. After the run

1. Wait until the bottom thermocouple reads below 60 °C before you open anything. After a full charge of shot
   the bottom thermocouple still reads about 150 °C an hour later (FEA). After a good powder run it reads about
   70 °C at an hour and falls from there.
2. Take the clamp off, drop the cup 5 mm so the centring ring leaves the cone's 2 mm recess, slide it out
   toward you, and fit a KF-50 blank and clamp on top to carry it.
3. Empty it by inverting over a sieve or a tray; the puck and liner come out too. Look at the liner and puck.
   Replace them if metal is welded on or they no longer drop in. Self-mated stainless can gall in argon, so keep
   the edges rounded and the 1.5 mm gap. Don't use hydrocarbon anti-seize: it would end up in the powder.
4. If the top thermocouple went over 150 °C, replace the O-ring. Edison's review notes FKM takes a compression
   set above about 200 °C.

## 9. What each check is based on

| Claim | Where |
|---|---|
| Seal and wall temperatures for 100–816 g of shot | `analysis/thermal.py`, `analysis/out/thermal_summary.md` |
| Stresses: pressure, vacuum, the hot floor | `analysis/structural.py`, `analysis/out/structural_summary.md` |
| Clamp force, buckling, flat-head thickness, clearances when hot | `analysis/handcalcs.py`, `analysis/out/handcalcs.md` |
| Install and removal paths | `cad/build_gif.py`, `cad/out/build_collisions.json` |
| Interfaces | `dims/README.md` (photos and video frames), `bom/vendor_dims.json` (vendor drawings) |
| Design review and precedents | `edison/` |
