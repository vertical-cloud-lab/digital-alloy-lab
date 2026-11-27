# Progression schedule (`ft_progression.py`)

Milestones in weeks (5 working days), earliest to latest:

| Milestone | A | B | C |
|---|---|---|---|
| S1 guide-laser and scanner checks | 1.4-3.8 | 1.4-3.8 | 1.4-3.8 |
| S2 FULL POWER INTO THE DUMP | 1.6-4.2 | 1.6-4.2 | 1.6-4.2 |
| FT-0 FIRST TRACKS | 1.9-5.2 | 1.9-5.2 | 1.9-5.2 |
| FT-1 FIRST COUPONS | 3.1-8.1 | 3.1-8.1 | 3.6-8.1 |
| FT-1V FIRST COUPONS (< 100 ppm) | 3.7-9.3 | 5.1-10.9 | 5.1-10.9 |

Scenarios: A: stages on PCards, cube ordered on day 0; B: stages on PCards, cube ordered after FT-0's O2 log; C: both stages on one Zaber PO, cube after the O2 log

Spend by the state that first needs each parts.csv line:

| State | Lines | Adds | Cumulative |
|---|---|---:|---:|
| S1 | L1, L2, L3, L4, L5, L5b, L6, L7, L10, L11, C1, E4, S2, MON4 | $6,271-10,710 | $6,271-10,710 |
| S2 | L8, L9, E1, S1, S5, S6, C2, C3, C4, MON6 | $3,140-4,006 | $9,411-14,716 |
| FT-0 | H1, H2, H3, H4, G1, G2, G3, G4, G5, G6, G7, G8, M4, S3, S4, F1, F2a, P1, MON1, MON2, MON3, MON7, MON8 | $11,322-21,784 | $20,733-36,500 |
| FT-1 | M1c, M2, M3, H5, C5, F2b, MON5 | $8,261-10,753 | $28,994-47,253 |
| FT-1V | E2, E3, E5, F2c | $11,700-13,826 | $40,694-61,079 |

What changes at each step (from the CAD model; moved = the part's bounding box shifted):

**S1 -> S2** (26 added, 1 moved, 2 removed, 18 unchanged)

- added: Water-cooled beam dump, 1 kW (EKSMA 990-0820 class, envelope) [L9]; Dump water lines [L9]; Saginaw SCE-16EL1208SSLP 304 box, 16 x 12 x 8 in. (body) [E1]; Poured-in-place door gasket [E1]; Box door (the lid): window bore, camera port [E1]; Quarter-turn latch [E1]; Concealed hinges (2) [E1]; Panel studs (4, on the floor) [E1]; Deck clamps on the panel studs (MK-23) [MK-23]; Stud nuts (4) [MK-23]; Inner clamp ring (MK-02) [MK-02]; Window ring (MK-02) [MK-02]; Window, Ø50.8 x 9.53 fused silica, 1064 V-coat [L8]; Window retaining flange (MK-02) [MK-02]; Window-stack screws, M4 x 12 flat head, flush [MK-02]; Cover-slide holder, Ø44 opening (MK-02) [MK-02]; Cover slide, Ø50 x 1 mm [L8]; Beam-tube lens collar, clamped on the lens (MK-10) [MK-10]; Beam tube centre section, split, long (MK-10) [MK-10]; Beam-tube interlock switch (on the collar; actuator on the centre section) [S1]; Surface thermocouples: beam tube, window ring (MON6) [MON6]; Safety relay box: E-stop, key switch (S1) [S1]; E-stop [S1]; Key switch [S1]; Emission lamp [S1]; Coded lid switches (2) [S1]
- moved: Deck plate (MK-01) [MK-01]
- removed: Guide-laser target stand (MK-18) [MK-18]; Anodised target, 80 x 80 x 3 mm [MK-18]

**S2 -> FT-0** (37 added, 0 moved, 2 removed, 43 unchanged)

- added: Macor standoffs under the well block (4) [H4]; Well block, Ø40.00 bore (MK-03) [MK-03]; Substrate disc Ø39.8 x 6 (MK-05) [MK-05]; Heater plate Ø39.8 x 24 (MK-04) [MK-04]; Fibreglass rope wiper [H4]; Plate heaters, 2 x Ø6 x 20, 50 W [H1]; Plate thermocouple, 1/16 in. type K (MON6) [MON6]; Well-block thermocouple, 1/16 in. type K (MON6) [MON6]; Piston rod (MK-06) [MK-06]; Potted lead plug, vacuum epoxy (MK-06) [MK-06]; Rod gland plate, 2 O-rings (MK-07) [MK-07]; Gland screws M5 x 25 with bonded seals (4) [MK-07]; FT-0 rod collar (MK-17) [MK-17]; FT-0 lead terminal bracket (MK-17) [MK-17]; Lead terminal block, 6-way pluggable [H2]; Lead pigtail, 4 heater + 2 TC wires [H3]; Overflow cup (MK-16) [MK-16]; Slot nozzle 45 x 4 mm (MK-11) [MK-11]; Exhaust collector (MK-11) [MK-11]; Argon feed tube to the nozzle [G3]; Exhaust hose to the HEPA [G3]; FT-0 spreader bar, 48 mm, ground edge, parked (M4) [M4]; Well-block heater and TC leads [H3]; IP68 cable glands M16 (2, back wall) [H3]; Box-air thermocouple and fitting (MON6) [MON6]; Camera port ring with a Ø1 in. window and cover slide (MK-19) [MK-19]; Camera port window, Ø25.4 x 3 fused silica [MK-19]; Layer camera: Pi HQ, C-mount lens, FESH1000 (MON1) [MON1]; Camera post, arm and foot (MK-20) [MK-20]; Raking light from -x, 15 deg: LED, condenser tube (MON2) [MON2]; Light port ring and window (MK-21, MON2) [MK-21]; Raking light from -y, 30 deg: LED, condenser tube (MON3) [MON3]; Light port ring and window (MK-21, MON3) [MK-21]; Digitizer, PicoScope 4824A class (MON8, envelope est.) [MON8]; Argon regulator and solenoid valve panel [G1]; Exhaust HEPA housing and check valve [G4]; Trace O2 analyzer (Alpha Omega 3000, envelope) [G5]
- moved: none
- removed: Water-cooled beam dump, 1 kW (EKSMA 990-0820 class, envelope) [L9]; Dump water lines [L9]

**FT-0 -> FT-1** (22 added, 1 moved, 4 removed, 75 unchanged)

- added: Well-block heaters, 4 x Ø6 x 20, 50 W [H1]; Zaber X-LSM100B-E03 recoater stage [M1c]; X-LSM carriage [M1c]; Carriage bracket and arm (MK-08) [MK-08]; Stage shield (MK-12) [MK-12]; Hopper, ~30 cm3 (MK-08) [MK-08]; Silicone-cord blade, 3 mm [M3]; Cord clamp (MK-08) [MK-08]; Vibration motor [M3]; Recoater M8 data and power cable [M1c]; Rod-end block: clamp, lead pocket, AE face (MK-15) [MK-15]; Rod clamp screw M4 [MK-15]; Lead terminal block, 6-way pluggable, on the rod-end block [H2]; AE sensor on the rod-end block, R15I-AST class (MON5) [MON5]; AE cable to the decoupler (MON5) [MON5]; Heater and TC cable to the controller (H2) [H2]; Zaber X-VSR20A-E01 piston stage [M2]; X-VSR20A platform [M2]; Piston-stage bracket plate and riser (MK-15) [MK-15]; Bracket-plate screws to the base rails, M6 (4) [MK-15]; X-VSR20A M8 cable [M2]; 120 mm fan blowing on the enclosure [E4]
- moved: Lead pigtail, 4 heater + 2 TC wires [H3]
- removed: FT-0 rod collar (MK-17) [MK-17]; FT-0 lead terminal bracket (MK-17) [MK-17]; Lead terminal block, 6-way pluggable [H2]; FT-0 spreader bar, 48 mm, ground edge, parked (M4) [M4]

**FT-1 -> FT-1V** (15 added, 56 moved, 13 removed, 29 unchanged)

- added: Ideal Vacuum 12 in. cube frame P107540 (face opening est.) [E2]; Cube top plate, bored for the window ring and the camera port (MK-13) [MK-13]; Cube bottom plate, bored for the rod gland (MK-14) [MK-14]; Cube front plate = door (hinge kit P106868), light port [E2]; Cube back plate (KF-25 feedthroughs) [E2]; Cube left plate (pump and gauge ports), light port [E2]; Cube right plate (argon in, exhaust, vent) [E2]; Door hinges (hinge kit) [E2]; KF-25 ports: pump, Pirani, argon, exhaust, 2 electrical feedthroughs [E3]; Rotary-vane pump (McMaster 4396K21 class, envelope est.) [E3]; KF-25 pump hose and valve [E3]; Deck screws into the bottom plate, M6 (4) [MK-14]; Cover-slide drop tube from the top plate (MK-02) [MK-02]; Beam tube centre section, split, short (MK-10) [MK-10]; Piston rod, long, for the cube (MK-06) [MK-06]
- moved: Gantry cross-beam (clamped at the head height) [E4]; SCANLAB hurrySCAN 25 (20/30 housing, drawing) [L3]; LINOS F-Theta-Ronar f = 254 mm (datasheet) [L4]; Scan-head flange plate (MK-09) [MK-09]; Flange-to-beam angle brackets (MK-09) [MK-09]; hurrySCAN input turret (focusing lens; by eye from listing photos) [L3]; hurrySCAN 45 deg input-mirror block (goniometer; by eye from listing photos) [L3]; Collimator (L2 if the fibre has none) [L2]; Process fibre [L1]; +-15 V supply for the head (DIN, est.) [L6]; Head cables and hoses (DB-9, DB-25, water, air) [L7]; Photodiode branch on the mirror block: FESH1000, bandpass, AC254-050-B, pinhole, PDA36A2 (MON4) [MON4]; Deck plate (MK-01) [MK-01]; Window ring (MK-02) [MK-02]; Window, Ø50.8 x 9.53 fused silica, 1064 V-coat [L8]; Window retaining flange (MK-02) [MK-02]; Window-stack screws, M4 x 12 flat head, flush [MK-02]; Cover-slide holder, Ø44 opening (MK-02) [MK-02]; Cover slide, Ø50 x 1 mm [L8]; Beam-tube lens collar, clamped on the lens (MK-10) [MK-10]; Beam-tube interlock switch (on the collar; actuator on the centre section) [S1]; Surface thermocouples: beam tube, window ring (MON6) [MON6]; Macor standoffs under the well block (4) [H4]; Well block, Ø40.00 bore (MK-03) [MK-03]; Well-block heaters, 4 x Ø6 x 20, 50 W [H1]; Substrate disc Ø39.8 x 6 (MK-05) [MK-05]; Heater plate Ø39.8 x 24 (MK-04) [MK-04]; Fibreglass rope wiper [H4]; Plate heaters, 2 x Ø6 x 20, 50 W [H1]; Plate thermocouple, 1/16 in. type K (MON6) [MON6]; Well-block thermocouple, 1/16 in. type K (MON6) [MON6]; Overflow cup (MK-16) [MK-16]; Slot nozzle 45 x 4 mm (MK-11) [MK-11]; Exhaust collector (MK-11) [MK-11]; Argon feed tube to the nozzle [G3]; Exhaust hose to the HEPA [G3]; Well-block heater and TC leads [H3]; Zaber X-LSM100B-E03 recoater stage [M1c]; X-LSM carriage [M1c]; Carriage bracket and arm (MK-08) [MK-08]; Stage shield (MK-12) [MK-12]; Hopper, ~30 cm3 (MK-08) [MK-08]; Silicone-cord blade, 3 mm [M3]; Cord clamp (MK-08) [MK-08]; Vibration motor [M3]; Recoater M8 data and power cable [M1c]; Camera port ring with a Ø1 in. window and cover slide (MK-19) [MK-19]; Camera port window, Ø25.4 x 3 fused silica [MK-19]; Layer camera: Pi HQ, C-mount lens, FESH1000 (MON1) [MON1]; Camera post, arm and foot (MK-20) [MK-20]; Raking light from -x, 15 deg: LED, condenser tube (MON2) [MON2]; Light port ring and window (MK-21, MON2) [MK-21]; Raking light from -y, 30 deg: LED, condenser tube (MON3) [MON3]; Light port ring and window (MK-21, MON3) [MK-21]; Coded lid switches (2) [S1]; 120 mm fan blowing on the enclosure [E4]
- removed: Saginaw SCE-16EL1208SSLP 304 box, 16 x 12 x 8 in. (body) [E1]; Poured-in-place door gasket [E1]; Box door (the lid): window bore, camera port [E1]; Quarter-turn latch [E1]; Concealed hinges (2) [E1]; Panel studs (4, on the floor) [E1]; Deck clamps on the panel studs (MK-23) [MK-23]; Stud nuts (4) [MK-23]; Inner clamp ring (MK-02) [MK-02]; Beam tube centre section, split, long (MK-10) [MK-10]; Piston rod (MK-06) [MK-06]; IP68 cable glands M16 (2, back wall) [H3]; Box-air thermocouple and fitting (MON6) [MON6]

## Order of work at the upgrade steps

Both steps start the same way: plate to the top of its stroke, heaters off and cool, substrate off, the beam tube's two half-shells off sideways (two toggle clamps), and the box door open (24 deg, the free angle with the layer camera on the door).

**FT-0 -> FT-1** (inside the box, it stays on the rails):

1. Under the box: the stage, its riser and bracket plate in from the front onto the base rails, the rod-end block on the stage's platform; the FT-0 lead terminal bracket off.
2. Inside: the FT-0 collar off the rod; the rod clamped in the rod-end block (22 mm of rod in it), the pigtail on its terminal block.
3. The recoater stage, shield, arm and hopper bolted onto the deck; the four block heaters in; the M8 cable out through the back-wall gland.

**FT-1 -> FT-1V** (the box comes off; the gland plate hangs 12 mm below the support rails' tops, so it comes off first and the box needs no lift):

1. Unwire the pigtail at the rod-end block (or unplug a circular plug of 12 mm or less: the gland's bore is 12.9 mm), loosen the rod clamp, and lift the heater plate with its 84.6 mm rod straight up out of the bore (103.6 mm of lift).
2. Deck clamps off (4 stud nuts), the recoater's M8 and the well block's leads unplugged at the glands; the cassette out through the door opening.
3. Stage to the bottom of its stroke (the block is then 23 mm under the gland, 3 mm at the top); unbolt the gland plate (4 x M5 from below) and take it out sideways.
4. Unbolt the box from the support rails and slide it forward off them.
5. The cube onto the rails (its underside lands where the box's was; the X-VSR20A stays), the gland onto its bottom plate, the cassette in through a face opening of at least 247 mm (or the bare deck edge-on and the cassette built inside), M6 deck screws.
6. The long rod's plate assembly (105.6 mm rod; a second assembly made ahead, or the leads re-potted) down through the bore and the gland into the rod-end block; window stack on the top plate, the cover-slide drop tube, the short half-shells; the cross-beam and optics up 21.0 mm.

