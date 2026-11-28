# Bought parts drawn as envelopes or generic shapes in `lpbf_low.build()`

Written by `cad/vendor_parts.py inventory`. Tier A: within 100 mm of the chamber or moving; B: rest of the process
module (optics bridge, guard); C: gas module; D: rack and tray. Ranked by tier, then by bounding-box volume.
Status: **done** = a real-part builder is in `vendor_parts.py`; env = still an envelope or generic shape; checked =
already drawn to the vendor's CAD.

| Rank | Tier | Part | Status | Real part / why not | BOM | Size (mm) | Box (L) | To chamber (mm) |
|---|---|---|---|---|---|---|---|---|
| 1 | A | Guard frame (20 mm T-slot) | env | simplified 20 mm profile; BOM S9 lists 30 mm 5537T97 | S9 | 730 x 480 x 526 | 184.349 | 0 |
| 2 | A | Gas-loop + vacuum hoses (KF-25 SS bellows) | env | McMaster 3497N23 is a 24 in. hose; routed lengths not matched | G7 | 1012 x 427 x 342 | 147.649 | 0 |
| 3 | A | Vacuum isolation valve (McMaster 4123K45 KF-25 manual ball valve) | **done** | McMaster 4123K45 (straight ball valve, not an angle valve) | G7 | 200 x 65 x 124 | 1.627 | 0 |
| 4 | A | Draw latches on the door's latch brackets, pointing forward (2 x McMaster 1807A61, 304 SS, 3.6 kN rated, preload set to ~0.75 kN) | env | 1807A61 (CAD fetched): real latch is 135.5 x 44 x 30.5 mm, drawn here as 24 x 12 x 18 | G1 | 356 x 80 x 44 | 1.264 | 16 |
| 5 | A | Recoater servo (ClearPath-SD, NEMA 23) | **done** | Teknic CPM-SDSK-2311S-RLN | M2 | 105 x 59 x 82 | 0.51 | 80 |
| 6 | A | Z servo (ClearPath-SD, NEMA 23, folded) | **done** | Teknic CPM-SDSK-2311S-RLN | M2 | 82 x 59 x 103 | 0.497 | 64 |
| 7 | A | Overflow jar grip fin (6061: tab on the cup, riser at x 117-125, I-section grip block at y -156 to -126, z -65 to -25, for the 2F-85) | env | KF-40 half nipple: no part number in the BOM | M4 | 56 x 86 x 100 | 0.482 | 5 |
| 8 | A | f-theta lens, f = 160 mm (Thorlabs FTH160-1064) | **done** | Thorlabs FTH160-1064 | L6 | 90 x 90 x 50 | 0.407 | 50 |
| 9 | A | Calibration power head on the plate (Gentec-EO UP55M-500W-H12-D0, water-cooled 500 W, aperture z 95; calibration state only) | **done** | Gentec-EO UP55M-500W-H12-D0 (89 x 89 x 43, page dimensions) | T1 | 89 x 104 x 43 | 0.398 | 0 |
| 10 | A | Overflow clamp (KF-40 toggle, MKS 100318805; lever to the front) | **done** | McMaster 4518K73 | G7 | 84 x 124 x 19 | 0.197 | 52 |
| 11 | A | Overflow jar (KF-40 flange on a 2.5 in. 316L cup, 47 mm, ~104 cm3, welded bottom) | env | KF-40 half nipple: no part number in the BOM | M4 | 64 x 64 x 47 | 0.19 | 62 |
| 12 | A | Layer camera (Pi HQ + C-mount lens) | env | Raspberry Pi HQ camera + C-mount lens: not drawn yet | M6 | 54 x 45 x 61 | 0.148 | 28 |
| 13 | A | Dosing stepper (NEMA 17) | **done** | McMaster 6627T91 | M4 | 42 x 74 x 43 | 0.135 | 7 |
| 14 | A | Z actuator body (KR-class U-rail, 2 mm lead, 100 mm stroke class) | env | 'KR-class' actuator: not in the BOM (M3 lists 6638K11 + 6709K33 + 6709K12) | M3 | 46 x 28 x 99 | 0.128 | 82 |
| 15 | A | Door hinge leaves + knuckles (304 SS, round pin holes: the hinge holds the door's bottom edge on its land) | env | labelled 1151A87 but drawn as custom knuckles; 1151A87 is a 3 x 3 in. two-leaf hinge (CAD fetched) | G1 | 200 x 12 x 48 | 0.115 | 15 |
| 16 | A | Door hinge knuckles on the chamber (304 SS, shimmed at assembly so the shut door's land just touches) | env | as above | G1 | 224 x 27 x 14 | 0.085 | 0 |
| 17 | A | Pressure transducer (7/16-20 SAE-4 O-ring-boss port; McMaster 3861N11 on an SAE-4 x 1/4 NPT adapter) | **done** | McMaster 3861N11 on an SAE-4 x 1/4 NPT adapter (transmitter_on_sae4, round 6; the adapter's dimensions are assumed) | G7 | 27 x 29 x 83 | 0.065 | 0 |
| 18 | A | Plate-height through-beam (M6 threaded fibre heads in the side walls, z +5 mm) | env | Omron E32-T61-S: not drawn yet | A1 | 356 x 13 x 13 | 0.06 | 0 |
| 19 | A | Recoater guide rail (15 mm, 260 mm) | **done** | McMaster 6709K33 (no CAD offered for the cut length: drawn to the listing) | M1 | 260 x 15 x 15 | 0.059 | 0 |
| 20 | A | Recoater ball nut (flange on the +x face) | **done** | McMaster 4566N401 | M1 | 43 x 30 x 40 | 0.052 | 0 |
| 21 | A | Recoater carriage (15 mm rail) | **done** | McMaster 6709K12 | M1 | 62 x 23 x 34 | 0.049 | 0 |
| 22 | A | Recoater ball screw (M12, 10 mm lead) | env | McMaster 4566N101: kept as a Ø12 rod (CAD fetched; helical thread not redrawn) | M1 | 311 x 12 x 12 | 0.045 | 0 |
| 23 | A | Inlet plenum port (KF-25) | **done** | McMaster 5786N23 | G7 | 40 x 26 x 40 | 0.041 | 26 |
| 24 | A | Outlet plenum port (KF-25) | **done** | McMaster 5786N23 | G7 | 40 x 40 x 26 | 0.041 | 45 |
| 25 | A | Z carriage | env | part of the KR-class actuator envelope | M3 | 42 x 10 x 40 | 0.017 | 93 |
| 26 | A | Vacuum port (KF-25, stub welded into the adapter plate) | **done** | McMaster 5786N23 | G7 | 10 x 40 x 40 | 0.016 | 8 |
| 27 | A | Side reservoir port (KF-16 flange machined in the 6061 base, blanked; reserved for a >= 500 cm3 reservoir beside the chamber with an auger) | env | KF-16 blank: no part number | R1 | 18 x 30 x 30 | 0.016 | 13 |
| 28 | A | Overpressure relief valve (316 SS, FKM seat, +34 mbar; SAE-4 O-ring-boss port) | env | McMaster 4277T52: page needs a set-pressure choice before CAD; not fetched | G7 | 18 x 18 x 47 | 0.015 | 0 |
| 29 | A | Module-present sensor (inductive M12, under the floor, sees the module flange) | env | AutomationDirect PAM-AP-1H: not drawn yet | A1 | 32 x 22 x 12 | 0.008 | 0 |
| 30 | A | Load cell (single-point, 2 kg, carries the dock rails: reservoir inventory) | env | Laumas ALLUE3: not drawn yet | M4 | 13 x 12 x 44 | 0.007 | 0 |
| 31 | A | Layer-light LED bar (on the lid's underside, along the right wall) | env | no part number | M6 | 8 x 90 x 8 | 0.006 | 0 |
| 32 | A | Pot magnet (NdFeB in a steel cup, Ø25 x 7, 44 lbf, holds the rod's striker) | env | McMaster 5679K95: CAD fetched; 7 mm cup drawn, 9 mm of extra parts in McMaster's model not resolved | B2 | 25 x 25 x 7 | 0.004 | 121 |
| 33 | A | Overflow-jar present sensor (inductive M12, PNP) | env | AutomationDirect PAM-AP-1H (M12 x 45): not drawn yet | A1 | 30 x 12 x 12 | 0.004 | 84 |
| 34 | A | Drawer-closed sensor (inductive M12, on the lid's front face, sees the plate's end) | env | AutomationDirect PAM-AP-1H: not drawn yet | A1 | 30 x 12 x 12 | 0.004 | 1 |
| 35 | A | Reservoir-docked sensor (inductive M12, at the back of the dock) | env | AutomationDirect PAM-AP-1H: not drawn yet | A1 | 12 x 30 x 12 | 0.004 | 52 |
| 36 | A | NFC reader antenna (in the dock's side face, reads the tag on the reservoir plate's edge) | env | Adafruit 364 board: not drawn | A1 | 2 x 19 x 18 | 0.001 | 22 |
| 37 | B | Leveling mounts, process module (McMaster 5537T983: Ø25 base, M8 stem threaded up through the plate) | checked | McMaster 5537T983: drawn to McMaster's CAD dimensions (volume checked here) | F3 | 695 x 445 x 52 | 16.082 | 140 |
| 38 | B | 2-axis galvo scan head (SCANLAB basiCube 20) | **done** | SCANLAB basiCube 20 | L5 | 155 x 130 x 122 | 2.458 | 105 |
| 39 | B | Collimator (IPG affixed, 2.5 mm beam: 96 µm at f = 160; housing drawn as the 5 mm unit, 128 mm + 78 mm strain relief) on V-mount | env | IPG 2.5 mm affixed collimator: no IPG drawing, drawn as the 5 mm unit's housing | L3 | 206 x 40 x 50 | 0.412 | 103 |
| 40 | B | E-stop enclosure, guard right side, near the front (1-hole yellow, 70 x 70 x 70 mm class) | env | IDEC XA1E-BV3U02-R: not drawn | S3 | 70 x 70 x 70 | 0.343 | 170 |
| 41 | B | Coaxial photodiode chain (SM1 tube: FESH1000 short-pass, NF1064-44 notch, AC254-050-B lens; Thorlabs PDA36A2) | env | Thorlabs PDA36A2 + SM1 tube: envelope assumed | T2 | 77 x 71 x 60 | 0.332 | 102 |
| 42 | B | Safety shutter + beam dump | env | no product chosen (BOM L4: quote) | L4 | 64 x 60 x 61 | 0.234 | 100 |
| 43 | B | Coaxial-monitoring dichroic (Thorlabs DMSP1000, 45 deg: reflects 1070 nm into the galvo, passes 520-985 nm) in a 30 mm cage cube | env | Thorlabs DMSP1000 in a 30 mm cage cube: cube size assumed | T2 | 42 x 42 x 56 | 0.098 | 100 |
| 44 | B | Fold mirror (Thorlabs NB1-K14, Ø1 in. Nd:YAG laser-line mirror, 45 deg) in a 30 mm cage cube | env | Thorlabs NB1-K14 in a 30 mm cage cube: cube size assumed | T2 | 42 x 42 x 56 | 0.098 | 100 |
| 45 | B | E-stops IDEC XW1E-BV402M-R, guard right side, near the front (40 mm mushroom, 2 NC) | env | IDEC XA1E-BV3U02-R: not drawn | S3 | 26 x 40 x 40 | 0.042 | 241 |
| 46 | B | Guard-locking door switch (Omron D4JL) | env | Omron D4JL-4NFA-C5-NPT: not drawn yet | S2 | 19 x 17 x 90 | 0.029 | 203 |
| 47 | C | Dry scroll pump (Edwards nXDS6i, A73501983: 432 x 282 x 302 mm, NW25 inlet and exhaust) | **done** | Edwards nXDS6i A73501983 (edwards_nxds6i, round 6, from Edwards' dimension drawing; no CAD is public) | G2 | 432 x 279 x 302 | 36.399 | 401 |
| 48 | C | Leveling mounts, gas module (McMaster 5537T983: Ø25 base, M8 stem threaded up through the plate) | checked | McMaster 5537T983: drawn to McMaster's CAD dimensions (volume checked here) | F3 | 555 x 515 x 52 | 14.863 | 297 |
| 49 | C | Sealed side-channel blower (gas-tight, ~100 L/min) | env | no gas-tight blower of this size found (KNF N 630.1.2 SP.9 E is 569 x 296 x 315, 45 kg) | G4 | 200 x 180 x 230 | 8.28 | 444 |
| 50 | C | Sealed cyclone + HEPA housing (McMaster 5169K72 + 9179K14 HEPA element on KF-25 adapters and elbows; cyclone stage not chosen) | **done** | McMaster 5169K72 + 9179K14 on KF-25 adapters and elbows (filter_train_5169K72, round 6; adapters, elbows and stand assumed) | G5 | 121 x 219 x 239 | 6.34 | 254 |
| 51 | C | Trace O2 analyzer + dew-point transmitter (panel box) | env | Ntron Microx (panel 96 x 96 x 90) + Vaisala DMT143 (Ø28 x 91.6): not drawn yet | G6 | 150 x 160 x 210 | 5.04 | 674 |
| 52 | C | Argon solenoid manifold (purge / make-up / vent) | env | McMaster 8077K237 x 2 (CAD fetched) on a custom block: not drawn yet | G7 | 115 x 130 x 82 | 1.226 | 273 |
| 53 | C | E-stop enclosure, front of the gas module's O2 box (1-hole yellow, 70 x 70 x 70 mm class) | env | IDEC XA1E-BV3U02-R: not drawn | S3 | 70 x 70 x 70 | 0.343 | 726 |
| 54 | C | Argon pressure regulator + flowmeter | env | McMaster 78595A5 (CAD fetched, 91 MB): not drawn yet | G3 | 44 x 44 x 100 | 0.194 | 324 |
| 55 | C | E-stops IDEC XW1E-BV402M-R, front of the gas module's O2 box (40 mm mushroom, 2 NC) | env | IDEC XA1E-BV3U02-R: not drawn | S3 | 40 x 26 x 40 | 0.042 | 756 |
| 56 | C | Pump inlet (KF-25) | **done** | McMaster 5786N23-type KF-25 stub on the nXDS6i's NW25 inlet (round 6) | G7 | 40 x 40 x 20 | 0.032 | 606 |
| 57 | C | Filter inlet (KF-25) | **done** | KF-25 stub on the inlet elbow (round 6) | G7 | 40 x 40 x 20 | 0.032 | 297 |
| 58 | C | Filter outlet (KF-25) | **done** | KF-25 stub on the outlet elbow (round 6) | G7 | 20 x 40 x 40 | 0.032 | 374 |
| 59 | C | Blower inlet (KF-25) | env | follows the blower | G7 | 20 x 40 x 40 | 0.032 | 429 |
| 60 | C | Blower outlet (KF-25) | env | follows the blower | G7 | 40 x 40 x 20 | 0.032 | 524 |
| 61 | D | 19 in. rack frame (12U, 560 mm tall) | env | no rack chosen; S9 lists 30 mm T-slot for the old cabinet | S9 | 560 x 600 x 560 | 188.16 | 274 |
| 62 | D | Rack side panels (vented) | env | sheet, no part number | S9 | 564 x 600 x 540 | 182.736 | 272 |
| 63 | D | Fiber laser source, 500 W single-mode, IPG YLR-500-U3-SM-AC (4U) | **done** | IPG YLR-500-U3-SM-AC (4U) | L1 | 482 x 557 x 176 | 47.432 | 313 |
| 64 | D | DIN-rail drawer: 24 V supply, safety relay, ClearCore, Pi 5 (4U: the safety controller stands 129 mm off its rail) | env | contents chosen (C3, C4, S1) but no drawer/enclosure: BOM C6 is a McMaster 7812K14 wall box | C3 | 483 x 534 x 176 | 45.305 | 314 |
| 65 | D | Process fiber (armoured, ≥ 100 mm bend radius) | env | IPG delivery cable (Ø8.5 per IPG's QBH drawing; drawn Ø10) | L1 | 220 x 384 x 299 | 25.256 | 227 |
| 66 | D | Scan + laser controller PC (2U) | env | no PC chosen (BOM C1 is a SCANLAB RTC6 card, quote) | C1 | 483 x 534 x 87 | 22.395 | 313 |
| 67 | D | UPS (Eaton 5PX1500RTG2, 2U) | **done** | Eaton 5PX1500RTG2 | C6 | 483 x 451 x 86 | 18.798 | 323 |
| 68 | D | Tray dock (CombiTac-type, mates sideways) | env | CombiTac-type: no part number | D1 | 108 x 80 x 140 | 1.21 | 973 |
| 69 | D | E-stop | env | IDEC XA1E-BV3U02-R: not drawn | S3 | 40 x 22 x 40 | 0.035 | 350 |
| 70 | D | Key switch | env | McMaster 6749K3: not drawn | S4 | 26 x 14 x 26 | 0.009 | 354 |
| 71 | D | Emission indicator | env | McMaster 7545K316 + 7545K7: not drawn | S4 | 22 x 10 x 22 | 0.005 | 355 |
| 72 | D | Reset button | env | McMaster 6749K201: not drawn | S4 | 22 x 10 x 22 | 0.005 | 355 |
