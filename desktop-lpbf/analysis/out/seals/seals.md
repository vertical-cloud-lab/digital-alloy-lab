# Seals, leaks and purge: results (from `analysis/seals/seals.py`)

Model: `cad/lpbf_low.build('M50', 'M')`. All forces in N, leaks in std cc/s (sccs) unless noted. Sources are listed at the end.

## Seal inventory (what the model now draws)

| Seal / penetration | Held by | In the model | Status | Note |
|---|---|---|---|---|
| Lid O-ring, FKM 75A 3.53 mm cord in a face gland 2.65 x 4.6 in the body's top face | 20 x M5 316 into helical inserts (metal-to-metal) | as before | **OK** | cord spliced into a ring: specify a vulcanized (hot) splice or a molded ring, never a glued joint, for vacuum |
| Door: 1.78 mm FKM 75A cord (McMaster 96515K123) in a half-dovetail groove, depth 1.32, 2.3 wide at the bottom, 24 deg undercut | 2 x McMaster 1807A61 draw latches (800 lb) on 6061 brackets bolted to the door's two ears, pointing forward, pulling strikes on the chamber's side faces (since 2026-11-23); the hinge holds the bottom edge (round pin holes, knuckles shimmed at assembly, since 2026-11-25; they were slotted so the door floated) | groove, cord, ears, latch brackets, latch bodies, strikes, hinge knuckles with round pin holes | **CHECK** | set each latch to ~0.75 kN and no more: the latches pull 12 mm outboard of the ears' tips, so more preload pries the door off its seal (door_seal_fea.md); the hinge pins need a close fit; the half-dovetail is overfilled at worst tolerance (gland table); the brackets' screws are not drawn (mech.md C); robot: a pneumatic clamp would go on the same brackets (not drawn) |
| Window: O-ring sandwich, 2-031 FKM under the Ø50.8 x 8 window, 1 mm FKM flat ring over it | retaining ring whose spigot bottoms metal-to-metal on the flange (6 x M3) | seat groove, both rings, stepped retaining ring | **OK** | squeeze set by geometry; the flat ring takes the window's thickness tolerance (FKM sheet not yet sourced) |
| Window flange to lid: 2-036 FKM face O-ring | 6 x M4 into helical inserts | groove + ring | **OK** |  |
| Cover-slide drawer: 2-033 FKM ring in a half-dovetail groove on the front plate | 2 quarter-turn latches (envelope; stud in the plate, receptacle in the lid) | groove, ring, latch studs and receptacles (envelope) | **CHECK** | no catalogue quarter-turn latch found that gives >= 0.4 kN in the 20 mm plate (McMaster 5210N21: 0.53 kN, needs a Ø22 hole; Southco E3 compact 450 N, Ø29 head) |
| Metering base to lid: 2-040 FKM face O-ring round the 12 x 100 dose slot | 4 x M4 | groove + ring | **OK** |  |
| Reservoir: 2-040 FKM face O-ring in the dock face round a 12 x 100 opening; one 30 x 112 mm base plate for S/M/L; O-ring-sealed lid on a welded top frame | dovetail-rail lips with a 2 deg ramp (robot push ~0.1 kN) + spring-plunger detent; lid on 2 x M3 | dock groove + ring, lips, single plate, top frame, lid groove + ring (2-023 / 2-030 / 2-042), shutter slot closed at both ends | **CHECK** | the ramps and the detent are not drawn; the shutter's drive through its closed slot (e.g. magnetic) is not designed |
| Metering-roller shaft: Ferrotec SSL-005-NN magnetic-fluid feedthrough, M8 x 1 nose, 2-012 FKM shoulder O-ring | its nut | feedthrough envelope, coupling, stepper moved back | **OK** | price not published; split of the 65.5 mm length assumed |
| Recoater screw, left wall: Ferrotec SFL-006-NN magnetic-fluid feedthrough on a 9 mm spacer ring (2 x 2-024) | its flange screws | feedthrough, spacer, 2 rings, clamp coupling in the wall bore, motor moved out | **OK** | price not published; bearing load rating to be checked against the screw's axial load |
| Recoater screw, right wall: blind bearing cap with a 2-020 FKM face O-ring | 4 x M4 | cap, groove, ring, screws | **OK** |  |
| KF-25 vacuum port: stub welded into a 304 adapter plate, 2-024 FKM face O-ring on the 6061 wall | 4 x M5 | plate, groove, ring, screws | **OK** | other KF stubs are welded to 316L parts (plenums, funnel) or machined in 6061 (side reservoir port) |
| Inlet (back wall) and outlet (under the floor) plenums, 316L on 6061: 2-044 FKM face O-rings | 9 x M4 and 6 x M4 (counterbored) | bolting flanges, grooves, rings, screws | **OK** | never welded (dissimilar metals) |
| Overflow funnel block (316L) under the floor: 2-042 FKM face O-ring | 4 x M4 (counterbored) | groove, ring, screws | **OK** |  |
| Argon in, O2 sample, pressure transducer, relief valve: SAE J1926 -4 (7/16-20) O-ring-boss ports, AS568-904 FKM | straight thread | ports (thread, 12 deg O-ring chamfer, Ø4 drilling); stems of the transducer and valve | **OK** | fittings McMaster 5182K862; transducer and relief valve must be ordered with SAE-4 male ends (not confirmed) |
| Through-beam fibre heads: M6 threaded heads into tapped holes, 2-010 FKM face O-rings | thread | tapped holes, grooves, rings, heads | **CHECK** | a fibre head with an M6 body and a sealing flange is not yet chosen |
| Camera: adapter to lid 2-022, Ø1 in. window on 2-017 + 1 mm FKM flat ring under a screwed retaining ring | screws (not drawn) | both grooves, rings, window, retaining ring; boss moved onto the line of sight | **OK** | the old Ø22 bore broke through the boss wall: fixed |
| Module spigot in the Ø96 floor port: FKM 2-238 radial, groove root Ø90.5 x 4.8 | radial; 2 captive M6 | groove and ring | **OK** |  |
| Gland plate on the welded collar: face groove 2.6 wide; 2-024 / 2-034 / 2-041 for S25 / M50 / L75 | 6 x M4 x 20 | groove, ring; plate 14 mm (was 10) | **OK** |  |
| Hollow rod through the gland plate: two Parker rod glands, groove Ø20.0, throat Ø15.93 (2-114; S25: 2-110, Ø13.64) | - | two grooves, two rings; rod labelled seamless and polished | **CHECK** | friction counts against the Z coupling (mech.md); measure break-out |
| Rod end: 316L block, the rod TIG-welded into its top; seven Solid Sealing weld-in feedthroughs TIG-welded at its 72 x 16 mm front face: 3 x FA11631 (Chromel) + 3 x FA11632 (Alumel) single-lead type K in Ø6.27 x 38 sleeves, 1 x FA10443 4-pin 16 A Cu in a Ø12.62 x 24 sleeve. The six type K sleeves sit 26 mm deep in blind bores joined to the rod bore by one Ø4 cross-drilling whose two ends are welded shut | welds (metal, glass-ceramic and welds: no elastomer) | block, rod socket, bores, cross-drilling, power pocket and channel, seven sleeves at the catalogue's diameters and lengths | **CHECK** | SST guarantees < 1e-10 atm cc/s He per part [13], so the seven parts are < 7e-10, far under the 1e-4 mbar L/s budget; the welds (7 sleeves + 2 cross-drilling plugs + the rod) set the real leak rate: helium-test the welded block before the module is assembled. SST designs its weld-ins to be welded on the vacuum side [13, 14]; here the welds are at the block's outer (air) face, so each type K sleeve's annulus in its 26 mm bore is a crevice open to the chamber gas (a slow virtual leak and a moisture trap; ~13 mm3 each at 0.05 mm clearance). Ask SST about the blind-bore weld, weld access and the weld side, and follow its pulsed-TIG procedure (heat sinks, segments <= 4 s) [14] |
| Blower, cyclone + HEPA housing, valves, hoses (KF-25 bellows) | KF clamps | unchanged | **CHECK** | the HEPA housing in the BOM (McMaster 5169K72) is 1/2 NPSC threaded and its gas-tightness is not stated; the blower must be specified gas-tight |
| O2 analyser sample loop | fittings | unchanged | **CHECK** | extractive analysers often have polymer tubing inside; return the sample to the loop, 316L lines, leak-check the analyser |

## Gland checks: every gland the model draws (Parker ORD 5700, AS568 tolerance, ±0.05 mm machining, FKM swell with temperature)

Stretch is the ring's ID onto the groove's inner wall (face), the groove root (radial) or the rod. Half-dovetail fill uses the trapezoid's area. Verdict flags squeeze outside 15-32 %, fill above 90 % at worst tolerance when warm, or stretch above 5 %.

| Gland | Closure | Ring (McMaster) | CS | depth × width | stretch | squeeze nom (min–max) % | fill nom / worst cold / worst warm % | Verdict |
|---|---|---|---|---|---|---|---|---|
| lid | chamber lid (20 x M5) | 3.53 mm cord | 3.53 | 2.65 × 4.60 | 0.0 % | 25 (21–28) | 80 / 88 / 89 at 70 °C | OK |
| spigot | module spigot in the floor port | 2-238 (9464K365) | 3.53 | 2.75 × 4.80 | 2.3 % | 21 (17–25) | 73 / 79 / 81 at 60 °C | OK |
| gland_plate_M50 | gland plate on the welded collar (M50) | 2-034 (9464K791) | 1.78 | 1.30 × 2.60 | 1.5 % | 26 (20–32) | 73 / 84 / 85 at 60 °C | **squeeze > 32 % at tolerance** |
| rod_M50 | hollow rod through the gland plate (M50) | 2-114 (9464K982) | 2.62 | 2.06 × 3.60 | 2.2 % | 21 (16–25) | 71 / 78 / 82 at 110 °C | OK |
| overflow_funnel | overflow funnel block (316L) under the floor | 2-042 (9464K849) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 50 °C | **fill > 90 % at worst tolerance, warm** |
| floor | chamber floor plate on the frame (18 x M4) | cord | 3.53 | 2.65 × 4.60 | 0.0 % | 25 (21–28) | 80 / 88 / 89 at 60 °C | OK |
| inlet_plenum | inlet plenum (316L) on the back wall (6061) | 2-044 (9464K865) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| outlet_plenum | outlet plenum (316L) under the floor (6061) | 2-044 (9464K865) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| vacuum_port | KF-25 vacuum-port adapter plate on the right wall | 2-024 (9464K753) | 1.78 | 1.32 × 2.30 | 2.5 % | 25 (19–31) | 80 / 93 / 93 at 40 °C | **fill > 90 % at worst tolerance, warm** |
| fibre_heads | threaded fibre heads in the side walls | 2-010 (9464K372) | 1.78 | 1.32 × 2.30 | 2.1 % | 25 (19–31) | 80 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| recoater_feedthrough | recoater feedthrough flange on the left wall | 2-024 (9464K753) | 1.78 | 1.32 × 2.30 | 2.5 % | 25 (19–31) | 80 / 93 / 93 at 40 °C | **fill > 90 % at worst tolerance, warm** |
| recoater_cap | blind bearing cap on the right wall | 2-019 (9464K478) | 1.78 | 1.32 × 2.30 | 2.2 % | 25 (19–31) | 80 / 93 / 94 at 40 °C | **fill > 90 % at worst tolerance, warm** |
| window_lower | window on its seat | 2-031 (9464K775) | 1.78 | 1.32 × 2.30 | 1.7 % | 25 (19–31) | 81 / 93 / 96 at 80 °C | **fill > 90 % at worst tolerance, warm** |
| window_flange | window flange on the lid | 2-036 (9464K793) | 1.78 | 1.32 × 2.30 | 2.6 % | 25 (19–31) | 80 / 93 / 94 at 60 °C | **fill > 90 % at worst tolerance, warm** |
| drawer | cover-slide drawer on the lid's front face | 2-033 (9464K788) | 1.78 | 1.32 × 2.30 (face 1.71) | 2.0 % | 26 (20–32) | 94 / 109 / 111 at 60 °C | **overfilled at worst tolerance, warm; face opening does not retain the cord** |
| metering_base | metering base on the lid (4 x M4) | 2-040 (9464K825) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| reservoir_dock | reservoir base plate on the dock face (wedge rails + detent) | 2-040 (9464K825) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| roller_feedthrough | roller feedthrough in the metering base | 2-012 (not confirmed) | 1.78 | 1.32 × 2.30 | 2.7 % | 25 (19–31) | 80 / 93 / 93 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| reservoir_lid_M | reservoir M lid on its top frame | 2-030 (9464K774) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| camera_adapter | camera adapter on the lid | 2-030 (9464K774) | 1.78 | 1.32 × 2.30 | 2.4 % | 25 (19–31) | 80 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| door | chamber door | cord | 1.78 | 1.32 × 2.30 (face 1.71) | 0.0 % | 26 (20–32) | 94 / 109 / 111 at 60 °C | **overfilled at worst tolerance, warm; face opening does not retain the cord** |
| gland_plate_S25 | gland plate on the welded collar (S25) | 2-024 (9464K753) | 1.78 | 1.30 × 2.60 | 1.5 % | 26 (20–32) | 73 / 84 / 85 at 60 °C | **squeeze > 32 % at tolerance** |
| rod_S25 | hollow rod through the gland plate (S25) | 2-110 (9464K977) | 2.62 | 2.06 × 3.60 | 3.6 % | 20 (16–24) | 71 / 78 / 81 at 110 °C | OK |
| gland_plate_L75 | gland plate on the welded collar (L75) | 2-041 (9464K836) | 1.78 | 1.30 × 2.60 | 3.3 % | 26 (20–32) | 72 / 83 / 84 at 60 °C | OK |
| rod_L75 | hollow rod through the gland plate (L75) | 2-114 (9464K982) | 2.62 | 2.06 × 3.60 | 2.2 % | 21 (16–25) | 71 / 78 / 82 at 110 °C | OK |
| reservoir_lid_S | reservoir S lid on its top frame | 2-022 (9464K492) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |
| reservoir_lid_L | reservoir L lid on its top frame | 2-042 (9464K849) | 1.78 | 1.32 × 2.30 | 2.0 % | 25 (19–31) | 81 / 93 / 94 at 45 °C | **fill > 90 % at worst tolerance, warm** |

## Closure forces (FKM 75A: E = 7.05 MPa from Gent; Lindley load per length)

| Closure | Seal | Squeeze force | Parker Fig. 2-x range at 25 % | Available |
|---|---|---|---|---|
| Lid | 3.53 mm, 955 mm long, 25 % | 4006 N (4.19 N/mm) | 2.14e+03–9.20e+03 N | 20 × M5: ≥ 48 kN; vacuum 5907 N |
| Door, before (3.53 mm cord) | 3.53 mm, 662 mm long, 25 % | 2778 N (4.19 N/mm) | 1.48e+03–6.38e+03 N | vacuum 2445 N |
| Door, now (1.78 mm cord) at 25 % | 1.78 mm, 662 mm long, 25 % | 1401 N (2.11 N/mm) | 882–2.44e+03 N | vacuum 2445 N seats it; at +20 mbar each 1807A61 needs **725 N** of preload (rated 3558 N) if the door were rigid |
| Door, CalculiX (door_seal_fea.md) | the door bends between its two latches | case D1200: 1.20 kN per latch, squeeze 15.2-22.0 %; case E750: 0.75 kN per latch, squeeze 23.6-25.8 % | – | the latch preload to set is in door_seal_fea.md |
| Door, now, at 15 % | 1.78 mm, 662 mm long, 15 % | 609 N (0.92 N/mm) | – | each latch needs 328 N at +20 mbar |
| Drawer (2-033 in a half-dovetail) | 1.78 mm, 169 mm long, 25 % | 358 N (2.11 N/mm) | 225–622 N | each of 2 quarter-turn latches needs 180 N; the drawn envelope has no rating yet |
| Reservoir on the dock (2-040) | 1.78 mm, 240 mm long, 25 % | 508 N (2.11 N/mm) | 320–884 N | 2 deg ramps, mu 0.15: push home 94 N, pull out 58 N, self-locking |
| Reservoir L lid (2-042) | 1.78 mm, 271 mm long, 25 % | 573 N (2.11 N/mm) | 360–996 N | 2 × M3 into the top frame: ≥ 1.7 kN |
| Window (2-031 under the window) | 1.78 mm, 148 mm long, 25 % | 314 N (2.11 N/mm) | 197–545 N | +20 mbar lifts 3.3 N vs weight 0.35 N; the retaining ring bottoms on metal |

## Permeation (Parker §3.12.1) into the argon loop

Arrhenius temperature scaling with E_a = 37 kJ/mol (Parker's He pair; the N₂ pair gives 58).

| Seal | T (°C) | O₂ (sccs) | H₂O (sccs) |
|---|---|---|---|
| lid | 50 | 9.39e-07 | 8.45e-06 |
| spigot (2-238) | 56 | 4.52e-07 | 4.07e-06 |
| gland_plate_M50 (2-034) | 60 | 2.62e-07 | 2.36e-06 |
| rod_M50 (2-114) | 117 | 6.44e-07 | 5.81e-06 |
| overflow_funnel (2-042) | 50 | 2.64e-07 | 2.38e-06 |
| floor (cord) | 60 | 1.41e-06 | 1.27e-05 |
| inlet_plenum (2-044) | 45 | 2.45e-07 | 2.20e-06 |
| outlet_plenum (2-044) | 45 | 2.45e-07 | 2.20e-06 |
| vacuum_port (2-024) | 40 | 5.93e-08 | 5.34e-07 |
| fibre_heads (2-010) | 45 | 1.24e-08 | 1.12e-07 |
| recoater_feedthrough (2-024) | 40 | 5.93e-08 | 5.34e-07 |
| recoater_cap (2-019) | 40 | 4.28e-08 | 3.86e-07 |
| window_lower (2-031) | 60 | 2.15e-07 | 1.93e-06 |
| window_flange (2-036) | 60 | 2.94e-07 | 2.65e-06 |
| drawer (2-033) | 50 | 1.63e-07 | 1.46e-06 |
| metering_base (2-040) | 45 | 1.88e-07 | 1.69e-06 |
| reservoir_dock (2-040) | 45 | 1.88e-07 | 1.69e-06 |
| roller_feedthrough (2-012) | 45 | 2.52e-08 | 2.27e-07 |
| reservoir_lid_M (2-030) | 45 | 1.06e-07 | 9.59e-07 |
| camera_adapter (2-030) | 45 | 1.07e-07 | 9.63e-07 |
| SAE-4 port O-rings (4 x 3-904) | 45 | 8.97e-08 | 8.08e-07 |
| door (cord) | 45 | 5.26e-07 | 4.73e-06 |
| KF-25 (7) + KF-40 (2) + KF-16 (1) centering rings | 35 | 4.49e-07 | 4.05e-06 |
| **Total** | | **6.98e-06** | **6.29e-05** |

Gas envelope 11.3 L (chamber 6.4, hoses 1.5, filter housing 2.3, plenums and blower 1.1).
Permeation alone adds **2.19 ppm O₂/h** and 19.71 ppm H₂O/h with no make-up flow.
Outgassing of 4605 cm² of bare Al and 18 cm² of exposed FKM after ~1 h: 3.68e-05 + 2.34e-05 mbar·L/s, **19 ppm H₂O/h**, falling roughly as 1/t.
150 g of powder holding 150 ppm (new, Karl Fischer [11]) to 300 ppm water by mass carries 22–45 mg: **2486–4971 ppmv** in the loop if a 200 °C plate drives it off.

Make-up argon to hold the targets at steady state: 46.5 sccm for 10 ppm O₂ against permeation; 58 sccm for a −40 °C dew point against wall and seal outgassing.

Other leak sources (air at 1 atm, mbar·L/s; vendor-typical ranges):

| Source | Range | Fix |
|---|---|---|
| 2 rotary shafts through elastomer V-rings / lip seals (recoater screw, metering roller) | 1.00e-05–1.00e-03 | magnetic-fluid feedthrough (helium leak < 1e-10 mbar L/s class) or a magnetic coupling through a can (zero leak) |
| rod gland, 2 x 2-114 reciprocating | 1.00e-06–1.00e-04 | edge-welded bellows over the rod |
| rod end: 7 weld-in feedthroughs (SST: each < 1e-10 atm cc/s He [13]) and their welds; the potted stranded leads it replaced were 1e-5 to 1e-2 | 7.00e-10–1.00e-09 | helium-test the welded rod-end block before the module is assembled and accept < 1e-9 mbar L/s (the upper value): the welds, not the parts, set it |
| threaded NPT ports (5-8 joints) | 1.00e-06–1.00e-03 | O-ring boss / VCR / KF |
| gas-tight side-channel blower, shaft seal | 1.00e-04–1.00e-03 | hermetic (canned / magnetic-drive) blower |

## Vacuum purge

Pump 4396K21: 1.42 L/s displacement; through two KF-25 bellows S_eff = 1.42 L/s at 800 mbar, 1.40 at 10 mbar, 1.28 at 1 mbar. **Pump-down to 1 mbar: 0.9 min**; time constant at atmosphere 8.0 s.

| Cycle (pump to 1 mbar, back-fill Ar 5.0) | O₂, ideal (ppm) |
|---|---|
| 1 | 207.81 |
| 2 | 1.20 |
| 3 | 1.00 |
| 4 | 1.00 |

### Powder beds while pumping (Kozeny–Carman k = 4.01e-12 m², Klinkenberg slip; U_mf = 2.8 mm/s)

| Bed | depth (mm) | Δp / bed weight at 1 atm | at 10 mbar | τ = V/S needed for ≤ 0.3 (s) |
|---|---|---|---|---|
| reservoir L (56 mm of powder) | 56 | 0.59 | 0.19 | 16 |
| build cylinder, end of build (40 mm) | 40 | 0.42 | 0.14 | 11 |
| overflow jar (90 mm) | 90 | 0.95 | 0.31 | 25 |
| reservoir M (40 mm) | 40 | 0.42 | 0.14 | 11 |

**Soft pump:** the overflow jar needs τ ≥ 25 s, i.e. ≤ 0.44 L/s (27 std L/min) until ~100 mbar: a metering valve of Cv ≥ 0.14 beside the main valve. Pump-down then takes ~1.6 min to 1 mbar. metering valve with Cv >= this in parallel with the KF-25 valve; open the main valve below ~100 mbar. Back-fill through the same limit (the flowmeter-regulator 78595A5 set <= 25 L/min) and a sintered diffuser.


Reservoir before the dock seal and lid seal were drawn (open to the room through the powder column): at +20 mbar, **299 sccm of argon leaves through the powder** at 8.9 mm/s superficial velocity, against a minimum fluidization velocity of 2.8 mm/s. Pumping down, room air comes in at ~9431 sccm.

## Rate-of-rise acceptance test

Leak budget 1.00e-04 mbar·L/s in 11.3 L is a rise of 5.33e-04 mbar/min; outgassing after ~1 h adds 3.21e-04 mbar/min. isolate at <= 1 mbar after >= 1 h pumping; read a Pirani or capacitance gauge for 10 min.

## Sources

1. Parker O-Ring Handbook ORD 5700: Design Chart 4-3 (face glands), Design Table 4-2 (static radial glands), §3.11 vacuum sealing and Table 3-20 (finish), §3.12.1 leak-rate approximation and Fig. 3-11 (Q), Table 3-24 (permeability), Figs. 2-4..2-6 (compression load). https://nfc.arizona.edu/sites/default/files/2022-02/parker_o-ring_handbook.pdf
2. Lindley, P. B. (1967). Compression characteristics of laterally-unrestrained rubber O-rings. J. Inst. Rubber Ind. 1, 209-213 (F/L = d E (1.25 e^1.5 + 50 e^6)); as used in e.g. https://doi.org/10.1016/j.triboint.2019.106062
3. Gent, A. N. (1958). On the relation between indentation hardness and Young's modulus. Trans. IRI 34, 46-57 (E [MPa] = 0.0981 (56 + 7.62336 S) / (0.137505 (254 - 2.54 S)))
4. Marco Rubber, O-ring permeation (FKM: H2O 40e-8 std cc cm/cm2 s bar): https://www.marcorubber.com/o-ring-permeation.htm
5. O'Hanlon, J. F. A User's Guide to Vacuum Technology, 3rd ed. (Wiley, 2003), Table 4.5 and App. C.5: outgassing of unbaked Al ~6e-9 and Viton A ~1e-6 Torr L/s/cm2 after 1 h; and Ch. 2-3 (viscous conductance, C = 135 d^4 p/L for air)
6. Kozeny-Carman permeability k = d^2 e^3 / (180 (1-e)^2); Klinkenberg (1941) slip k_a = k (1 + b/p), b = 4 c lambda p / r with c ~ 1 (API Drilling and Production Practice, 200-213)
7. Ergun minimum fluidization: U_mf = (rho_p - rho_g) g d^2 e^3 / (150 mu (1 - e)) for small particles (Kunii & Levenspiel, Fluidization Engineering, 2nd ed., Ch. 3)
8. McMaster-Carr 4396K21 (3 cfm, 1e-2 Torr) and the parts in ../../mcmaster-parts.csv, read through the lab Pi 2026-11-17
9. Airgas/Linde argon 5.0 (UHP) typical limits: O2 <= 1-2 ppm, H2O <= 1-3 ppm
10. Sturm et al. (2004), Permeation of atmospheric gases through polymer O-rings used in flasks for air sampling, J. Geophys. Res. 109, D04309, https://doi.org/10.1029/2003JD004073: Viton O2 1.0-1.1e-15 and H2O ~220e-15 m2/(s hPa) (= 1.05e-8 and 2.2e-6 std cc cm/(cm2 s bar)); via Edison
11. Lubkowitz et al. (2024): new AlSi10Mg powder 0.015 wt% moisture (Karl Fischer); Van Cauwenbergh et al. (2019): AlSi7Mg0.6 powder 45 +/- 11 ppm H, parts 13 +/- 4 ppm; via Edison, desktop-lpbf/edison/followup-sealing-o2/answer.md
12. Pauzon et al. (2021), control of residual oxygen in LPBF (TruPrint 1000): a zirconia lambda probe read +50 ppm where an electrochemical cell read +700 ppm (H2 cross-sensitivity); leak-plus-outgassing drift ~1.7 ppm O2/min; via Edison
13. Solid Sealing Technology, General Product Specifications: every hermetic part helium leak-tested, guaranteed < 1e-10 atm cc/s He; 'weldable feedthroughs are designed to have the adapter welded on the vacuum side of flanges or chambers'. https://www.solidsealing.com/img/documents/SST_General_Product_Specifications-406829.pdf (linked from the FA11631 page; read 2026-11-25 through the lab Pi). FA11631: 10 V, -269 to 450 C, 3500 psig, weld mount, $44 (https://www.solidsealing.com/products/1851/)
14. Solid Sealing Technology NS13003, 26482 circular connectors, welding instructions: mating hardware 304 or 316; 'preferred orientation is with the weld on the vacuum side'; pulsed TIG 20-25 A, heat sinks on both sides, tack welds, segments of 3-4 s (never over 4 s), inert gas on the far side. https://www.solidsealing.com/img/resources/NS13003_887844.pdf (read 2026-11-25; SST lists no sheet for the single-lead and 4-pin weld-ins)
