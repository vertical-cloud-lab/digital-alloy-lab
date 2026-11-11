# rePowder ultrasonic atomizer: SOP checklist

AMAZEMET rePowder (induction furnace over an ultrasonic atomization chamber), 154 CB. A terse
run-day checklist built on Gage's notes in
[#251](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/251), checked against the
Sep 29–30 training videos and the lab's runs from Oct 2 to Nov 5. The reasons behind each step,
video timestamps and the run records are under [Sources](#sources).

**Who.** Only people trained on the machine (Gage, Ronnie, Sterling) handle the transducer, the
ultrasonic stack and parts inside the machine. Others help outside the enclosure
([#160](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/160),
[#161](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/161)).

HMI buttons are in **bold**. Pressures are as the HMI shows them, relative to the room.

## Safety (every run)

1. Check that the ground wire is attached before every start.
2. Wear gloves whenever you touch the machine (skin oils mark the parts, and powder).
3. Wear hearing protection while the ultrasonics or the induction generator run.
4. Put on the full-face P3 respirator before opening the chamber or handling powder.
5. Never open the chamber above atmospheric pressure: vent first.
6. Never clean with compressed air once powder has been in the machine: fine powder can ignite.
   Keep the Class D extinguisher at hand.
7. Never drop, wet or overheat the transducer. Carry the stack by the housing, keep the protective
   cover on, and keep the ultrasonic cable (about 1000 V) off the floor.
8. Keep at most two argon or nitrogen cylinders in the booth, not manifolded, and no dewar. Anything
   more needs the College of Engineering industrial hygienist's OK first.

## Start Up

1. Turn on the recording cameras; free up phone storage.
2. Put on gloves and the lab coat.
3. Check the ground wire. Look the machine over: leaks, damaged wires, clean inside and out.
4. Check the oil in the vacuum pump (sight glass, between min and max).
5. Check the water level in the heat exchanger.
6. Check the argon: note the cylinder pressure, set the regulator to 8 bar (116 psi). An Al run uses
   about 100–160 psi, a copper run 300–350 psi.
7. Open the chilled-water lines about 20°. Without them the atomizer runs only until heat builds
   up, then shuts itself down.
8. Open the compressed-air valve (the ultrasonics will not run without air).
9. Turn on the atomizer with the big red switch. Log in to the HMI, open the program, and wait about
   10 s for the furnace to connect.

## Configuring the Ultrasonic Tower

Pick the booster to suit the plate:

| Booster | Plate | Powder | Scan reads |
| --- | --- | --- | --- |
| 1:1.5 (amplifying) | Carbon fibre. The only booster carbon fibre works on; it cracks metal plates | Coarsest, easiest | ~40.1 kHz |
| 1:1 | Metal (Mo) | Middle | ~40.0–40.2 kHz |
| 1.5:1 (reverse) | Mo only. With carbon fibre it dripped and never atomized (Oct 8) | Finest | ~39.6 kHz |

1. Choose the booster. Orient it in the housing so the wide flange matches the seal and then the
   connection point on the atomizer.
2. Check that the housing's O-ring is in. Bolt on the housing with its 4 bolts, until stiff; no
   extra force.
3. Clean the threads and the two double-threaded connectors with IPA.
4. With the connectors, hand-twist the transducer (very expensive, don't drop it) onto the outer
   end, then the long lower sonotrode onto the chamber-facing end of the booster.
5. Torque in the soft-jaw vise with a second wrench counter-holding: transducer to booster
   **65 N·m**, booster to lower sonotrode **60 N·m**. Righty-tighty for all three joints; the
   wrench clicks at the set torque.
6. Bolt the protective cover over the transducer. Plug in and lock the cable, connect the air line,
   and hang the cable on its holder.
7. Run a frequency scan: one peak, between 39,500 and 40,500 Hz (table above). If not, take apart,
   clean and re-torque.
8. Place the protective plate inside the atomizer.
9. Put the seal over the lower sonotrode and onto the housing flange. Insert the lower sonotrode
   into the atomizer and hand-tighten the seal clamp.
10. Hand-twist the double-threaded connector all the way into the lower sonotrode.
11. Slide the plate onto the connector. Check for flat, gap-free contact with the lower sonotrode.
12. Hand-twist on the upper sonotrode.
13. Torque the upper sonotrode to the lower at **50 N·m** (two 17 mm wrenches).
14. Orient the plate perpendicular to the hatch it is attached to.
15. Set the height with the Mo gauge plate so the plate sits between the Sharpie lines on the upper
    sonotrode ([#164](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/164)). Log
    the setting.
16. Rescan, then wet-test with a few drops of IPA: the whole plate should atomize. If only half of
    it works, the plate is cracked: replace it.
17. With the door open, check that the stream will land high on the plate and centred, clear of the
    upper sonotrode. For copper on a W-coated plate, aim at the tip.
18. Wipe the seals with IPA and close the hatch.

## Loading the Furnace

If the furnace is being rebuilt, do it before the stack goes in: the graphite nut under the
crucible is reached through the chamber door.

1. Nozzle: look for light through the bore, and lift any globs off the outlet with tweezers. If it
   is closed, drill it out by hand. Graphite 0.5 mm is standard; use 0.7 mm for Al-Si-Mg or alloys
   that clog.
2. Crucible boron-nitride coated: a thin coat, sprayed the night before, dry.
3. Rebuild: nozzle in its holder white side up; crucible snug but never forced (graphite cracks);
   graphite seal, bottom insulation, crucible into the coil, graphite nut on from below. Line the
   crucible's thermocouple hole up with the thermocouple at the back right.
4. Line the side insulation's hole up with the thermocouple port, and bend the thermocouple close to
   the crucible. Push the top insulation ring in so its rim doesn't catch the silica insulation.
5. Sealing rod: the tip must be clean and smooth. Stand it on the nozzle, swing the lever down, put
   the safety pin in, and press **Sealing Rod** so it is down.
6. Splash disc in the container's top flange; collection cup clamped on with its valve open; catch
   bowl in the chamber.
7. Charge: clean it with IPA and weigh it. At most 20 mm across; 250–300 g for Al.
8. Clean the furnace seal and the surface it touches with IPA. Close the lid and adjust the latch
   until nothing hisses.

## Atomizer Trial

Material and ultrasonic system prepared and loaded.

### Cold purge

1. Make sure the green light in the bottom-left corner is on. If not, flip the red switch (left of
   the light-gray control panel) down, then up.
2. Press **Pressure Control**.
3. Press **Vacuum Pump**.
4. Press **Gas Wash**.
5. When it finishes, press **Melting Pressure**.
6. Turn off **Pressure Control**.
7. Turn on **Vacuum Pump** and **Vacuum Valve**; wait for about −850 mbar.
8. Press **Protective Gas** to bring in argon until −100 mbar, then turn it off.
9. Press **Vacuum Pump** and **Vacuum Valve** again; wait for about −850 mbar.
10. Press **Pressure Control**; wait for 150 mbar.
11. Turn on the large red switch on the heat exchanger. Open the chilled-water valves about 30°.
    Wait until the low-flow warning goes away.
12. Hearing protection on.

### 250 °C wash

13. Set 250 °C first (the setpoint keeps its last value), then press **Generator Start**. Heating
    begins. Wait for 250 °C.
14. Press **Vacuum Pump**, then **Gas Wash**. When it finishes, press **Melting Pressure**.
15. Turn off **Pressure Control**. Press **Vacuum Pump** and **Vacuum Valve** to purge the
    chamber; wait for about −850 mbar.
16. Press **Pressure Control**.

### 500 °C wash

17. Set 500 °C; wait for it.
18. Press **Vacuum Pump**, then **Gas Wash**. When it finishes, press **Melting Pressure**.
19. Turn off **Pressure Control**. Press **Vacuum Pump** and **Vacuum Valve**; wait for −850 mbar.
20. Press **Pressure Control**. At 150 mbar, read **Oxygen Accurate**: the low 20s (ppm) is ideal.
21. Above 29 ppm, purge the furnace and the atomizing chamber again (steps 18–20).

### Melt

22. Set 840 °C (copper: see [Copper Alloys](#copper-alloys-nab-630-bronze)).
23. When the rods start to sink, drop to 800 °C.
24. Once it is all molten, hold 2 minutes to mix. No longer: it only oxidizes.

### Atomize

25. Turn on **Transducer Cooling**.
26. Press **Ultrasonic Scan**: one peak, just above 40 kHz (about 39.6 kHz with the 1.5:1 booster).
27. Set the amplitude: 90, read on the HMI's number. Note it.
28. Press **Ultrasonic Start**. The vibration must be on before any melt comes out.
29. Press **Graining Pressure** (0.19 bar) and **Sealing Rod**. It begins to atomize.
30. Watch the plate the whole pour. Check that it is catching the stream; this is a trim, since the
    position was set before closing. Use **Turbo Pump** as needed to:
    1. push more flow onto the plate to start atomizing (on carbon fibre, hold it from the start
       until the plate is plainly atomizing);
    2. correct the stream's direction;
    3. push out the nozzle if it clogs, especially at the end.
31. Raise the amplitude only if it is not atomizing. Note any change made mid-pour.
32. Keep an eye on the generator display: if it trips, heating stops and the nozzle freezes.

### End of run

33. When the crucible is empty, give a last **Turbo Pump** to clear the nozzle, then quickly press
    **Sealing Rod**, **Melting Pressure**, **Generator Stop** and **Ultrasonic Start** (turns the
    ultrasonics off).
34. Turn off **Transducer Cooling**. Set the temperature to 250 °C: Generator Stop already stopped
    the heating, and this is prep for the next run.
35. Write the run log now ([Run Log](#run-log)). The machine keeps none.

## Cooldown and Shut Down

1. Wait until about 400 °C; then the graphite is safe in air (above 500 °C it degrades fast).
2. Turn off **Melting Pressure**.
3. Respirator on. Turn off **Pressure Control**, then press **Vent Valve**. Open the chamber, and
   the furnace for faster cooling.
4. Note the argon cylinder pressure and close the cylinder valve. A cylinder left open leaks empty.
5. At about 100 °C, turn off the heat exchanger and close the chilled water, then the compressed
   air, then turn off the atomizer.
6. Close the furnace lid against dust.

## Powder Collection and Cleaning

Respirator, gloves and lab coat.

1. Lay the laminated paper under the chamber opening to catch powder.
2. Brush powder off the plate, cone, view port and catch bowl into the collection cup with the
   anti-static brushes. Let the dust settle.
3. Remove the collection cup, pour the powder into a jar, and clean the cup.
4. Label the jar with a new 6-character code and add a row to the Excel sheet.
5. Collect, bag and label the splashes from the splash plate. Weigh the powder, splashes, catch-bowl
   metal and crucible leftovers separately. Un-atomized metal is feedstock, not waste.
6. Clean the chamber door, sonotrode and plate. Take the plate off if it is cracked or the metal won't
   lift off. Never grind a plate; keep each plate to one alloy and log its condition.
7. Clean the chamber, view port, crucible and crucible stand, and the splash plate and cone down to
   the cup. Vacuum with the ATEX vacuum, then wipe. Never compressed air.
8. Once the furnace can be touched: slag out, nozzle checked or drilled, furnace rebuilt.
9. Wipe every seal and the surface it touches with IPA before closing (chamber door, collection
   chamber, cup, furnace).
10. Reattach the cup with its valve open.
11. Wipe the screens and handles with IPA.
12. Sweep outside the yellow lines. Sweepings go in the Solid Material Waste bucket and full vacuum
    liners in the labelled metal bucket; request a Risk Management pickup when one is full.
13. Store the jar and the leftover metal in the closet.
14. Upload the day's videos to YouTube as "M/D/YYYY Atomizer Run Video #" in the Atomizer Runs
    playlist, and post the links in
    [#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159).

## Copper Alloys (NAB, 630 bronze)

What changes from the Al procedure, from the Oct 27, Oct 28 and Nov 5 runs
([#219](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219)):

1. Use the copper set: its own crucible, nozzle and sealing rod. Keep copper and Al residues apart
   (Al with copper oxide is a thermite pair).
2. Fit a new hBN 0.5 mm nozzle and a new W-coated carbon-fibre plate for every run; 1:1.5 booster,
   amplitude 90.
3. BN-coat the crucible in light passes in the fume hood, dry it overnight, and cure it empty under
   argon before the run (a fresh coat smoked at 500 °C).
4. Melt at 1300 °C, the hard maximum. Hold 2 minutes after the reading is back at 1300 °C.
5. Aim the stream at the plate's tip. Hold **Turbo Pump** from the start of the pour until it is
   plainly atomizing. If metal piles up, move the stream to a fresh spot.
6. NAB powder contains Ni (a skin sensitizer): gloves for all powder handling.
7. Do the full clean (about 1 h) before the next Al run, and keep separate sieves for each alloy
   family.

## Run Log

Post one entry per run in [#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159):

1. Date and run number; operator.
2. Alloy (check the name), form and weighed mass of the charge.
3. Plate (material, size, ID, use count), booster, nozzle, gauge-plate setting.
4. Scan frequency; amplitude at the start and any change.
5. O₂ after each wash, before the pour, and after it.
6. Melt and hold temperatures; hold time.
7. Graining and turbo pressures, set and displayed.
8. Argon cylinder pressure at the start and the end.
9. What happened; weights of powder, splashes and leftovers; the powder's 6-character code; video
   links.

## Troubleshooting

| Symptom | Do |
| --- | --- |
| Vacuum stops near −850 mbar | Normal: at our altitude the gauge bottoms out near −0.85 bar. |
| "Pressure crucible" warning | Normal so far. It means a small chamber-to-furnace leak through the graphite seals; if it persists, swap the sealing rod or crucible. |
| Chamber won't pump down (Oct 20) | Usually the collection cup's flange or valve: wipe with IPA, re-clamp. |
| Low-flow warning | Heat exchanger on; chilled-water valves open. |
| "Water too cold" | Close the chilled-water valve a little. |
| Ultrasonics refuse; "no air pressure" | Compressed air on. |
| Scan off range or with two peaks | A short burst of vibration, then rescan; otherwise take the stack apart, clean the threads, re-torque. |
| Melt pours but nothing atomizes; HMI reads 0 Hz, 0 W (Oct 6) | **Ultrasonic Start** wasn't pressed. Vibration on before the sealing rod. |
| Stream lands on the upper sonotrode (Oct 6) | Pull the stack back. Next time check the landing with the door open. |
| Steady drips onto a carbon-fibre plate, no powder (Oct 8) | The 1.5:1 booster with carbon fibre doesn't work: use a Mo plate, or the 1:1.5 booster. |
| Melt shoots past the plate (Oct 2) | Lower the graining pressure; move the plate closer and higher. |
| Thin stream gathers on the plate | The plate is too cold: **Turbo Pump** to push more on. |
| Copper won't start atomizing (Oct 28) | Turbo from the start; new plate and nozzle; aim at the tip; full 2-minute hold. |
| Stream bends | Oxide at the nozzle: steer with the plate; purge better next time. |
| Nozzle clogs | **Turbo Pump** pulses. Once cool, drill it out by hand. |
| Temperature falls mid-pour, nozzle freezes (Nov 5) | The generator tripped. Watch its display through the pour. |
| O₂ stays at 45–70 ppm (Oct 8) | More 500 °C washes; check the seals. |
| O₂ climbs during the run | A leak: re-clean the seals; another 500 °C wash next time. |
| Argon cylinder empty early (Oct 20) | Close the cylinder after every run; leak-check the regulator with soapy water. |
| Furnace lid hisses | Adjust the latch. |
| Smoke at 500 °C | A fresh, uncured BN coat: cure it before the run. |

## Maintenance

1. Daily: coolant level, a look for cooling leaks, a look over the furnace, cabinet and seals.
2. Weekly: pump oil, ISO-KF clamps tight, the control cabinet.
3. Every 20 h of running: safety filter, flapper-valve seals, vacuum-pump filter.
4. Monthly: dust, loose screws, the chamber mechanism.
5. Every 2 months or so: the HEPA filter, into a metal tray with sand (fine dust can self-ignite).
6. Quarterly: lubricate the chamber hinges.
7. Yearly: fans, coolant, pump oil, a whole-system leak check.

## Sources

- Gage's notes: [#251](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/251). The
  run-day split between operators:
  [#143](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/143#issuecomment-6353378605).
- The detailed SOP from the training videos, with a timestamped link for each step, and the
  manual's rules and maintenance schedule:
  [`atomizer-training/sop.md`](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/93fdb547ce49/atomizer-training/sop.md),
  [`manual.md`](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/93fdb547ce49/atomizer-training/manual.md)
  and [`equipment.md`](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/93fdb547ce49/atomizer-training/equipment.md)
  (PR [#178](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/178)). The training
  videos' transcripts and timestamp log: PR [#173](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/173).
- Run records:
  [#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159) (run log);
  [Oct 6](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/7ec59ab1f6df/atomizer-training/runs/2026-10-06.md);
  [Oct 8](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/308f3c2df548/atomizer-runs/2026-10-08/README.md);
  [Oct 20](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/5d1cf0c7fec3/atomizer-runs/2026-10-20/README.md)
  and [Oct 21](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/5d1cf0c7fec3/atomizer-runs/2026-10-21/README.md);
  copper on [Oct 27–28](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/413e717e0a4b/atomizer-runs/2026-10-28/README.md),
  the [630 bronze run plan](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/25cc027c0120/atomizer-runs/2026-10-630-bronze-run-plan.md)
  and [#219](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219).
- Plate height: [#164](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/164).
  Transducer handling: [#161](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/161).
  Al cups and plugs: [#156](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/156).
