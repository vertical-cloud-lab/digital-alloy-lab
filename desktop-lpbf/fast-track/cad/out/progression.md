# Progression schedule (`ft_progression.py`)

Milestones in weeks (5 working days), earliest to latest:

| Milestone | A | B | C |
|---|---|---|---|
| S1 guide-laser and scanner checks | 1.4-3.8 | 1.4-3.8 | 1.4-3.8 |
| S2 FULL POWER INTO THE DUMP | 1.6-4.2 | 1.6-4.2 | 1.6-4.2 |
| FT-0 FIRST TRACKS | 1.8-4.6 | 1.8-4.6 | 1.8-4.6 |
| FT-1 FIRST COUPONS | 3.2-6.6 | 3.2-6.6 | 3.6-6.8 |
| FT-1V FIRST COUPONS (< 100 ppm) | 3.8-7.8 | 5.2-8.8 | 5.2-8.8 |

Scenarios: A: stages on PCards, cube ordered on day 0; B: stages on PCards, cube ordered after FT-0's O2 log; C: both stages on one Zaber PO, cube after the O2 log

Spend by the state that first needs each parts.csv line:

| State | Lines | Adds | Cumulative |
|---|---|---:|---:|
| S1 | L1, L2, L3, L4, L5, L6, L7, L10, C1, E4, S2 | $6,081-10,280 | $6,081-10,280 |
| S2 | L8, L9, E1, S1 | $2,095-2,995 | $8,176-13,275 |
| FT-0 | H1, H2, H3, H4, G1, G2, G3, G4, G5, M4, C2, S3, S4, F1, F2a, P1 | $5,054-10,410 | $13,230-23,685 |
| FT-1 | M1b, M2, M3, F2b | $7,063-7,833 | $20,294-31,518 |
| FT-1V | E2, E3, E5, F2c | $11,435-13,170 | $31,729-44,688 |

What changes at each step (from the CAD model; moved = the part's bounding box shifted):

**S1 -> S2** (20 added, 1 moved, 2 removed, 12 unchanged)

- added: Water-cooled beam dump, 500 W (Thorlabs LB2L/M class, envelope) [L9]; Dump water lines [L9]; 304 NEMA 4X box, 16 x 12 x 8 in. (body) [E1]; Lid gasket, FKM cord [E1]; Box lid (the door), window bore [E1]; Continuous hinge [E1]; Lid clamps (4) [E1]; Inner clamp ring (MK-02) [MK-02]; Window ring (MK-02) [MK-02]; Window, Ø50.8 x 9.53 fused silica, 1064 V-coat [L8]; Window retaining flange (MK-02) [MK-02]; Cover-slide holder (MK-02) [MK-02]; Cover slide, Ø50 x 1 mm [L8]; Beam tube, long, with lens collar (MK-10) [MK-10]; Beam-tube interlock switch [S1]; Safety relay box: E-stop, key switch (S1) [S1]; E-stop [S1]; Key switch [S1]; Emission lamp [S1]; Coded lid switches (2) [S1]
- moved: Deck plate (MK-01) [MK-01]
- removed: Guide-laser target stand (MK-18) [MK-18]; Anodised target, 80 x 80 x 3 mm [MK-18]

**S2 -> FT-0** (18 added, 0 moved, 2 removed, 31 unchanged)

- added: Macor standoffs under the well block (4) [H4]; Well block, Ø40.00 bore (MK-03) [MK-03]; Substrate disc Ø39.8 x 6 (MK-05) [MK-05]; Heater plate Ø39.8 x 28 (MK-04) [MK-04]; Fibreglass rope wiper [H4]; Plate heaters, 2 x 1/4 x 1 in. [H1]; Piston rod (MK-06) [MK-06]; Rod gland plate, 2 O-rings (MK-07) [MK-07]; FT-0 rod collar (MK-17) [MK-17]; Overflow cup (MK-16) [MK-16]; Slot nozzle 45 x 4 mm (MK-11) [MK-11]; Exhaust collector (MK-11) [MK-11]; Argon feed tube to the nozzle [G3]; Exhaust hose to the HEPA [G3]; Film applicator, parked (M4) [M4]; Argon regulator and solenoid valve panel [G1]; Exhaust HEPA housing and check valve [G4]; Trace O2 analyzer (Alpha Omega 3000, envelope) [G5]
- moved: none
- removed: Water-cooled beam dump, 500 W (Thorlabs LB2L/M class, envelope) [L9]; Dump water lines [L9]

**FT-0 -> FT-1** (15 added, 0 moved, 2 removed, 47 unchanged)

- added: Well-block heaters, 2 x 50 W [H1]; Zaber X-LSQ075B-E01 recoater stage (body est.) [M1b]; X-LSQ carriage [M1b]; Carriage bracket and arm (MK-08) [MK-08]; Stage shield (MK-12) [MK-12]; Hopper, ~30 cm3 (MK-08) [MK-08]; Silicone-cord blade, 3 mm [M3]; Cord clamp (MK-08) [MK-08]; Vibration motor [M3]; Zaber X-VSR20A-E01 piston stage (footprint est.) [M2]; X-VSR20A platform [M2]; X-VSR20A lift column [M2]; Rod clamp (MK-15) [MK-15]; Piston-stage bracket plate and riser (MK-15) [MK-15]; 120 mm fan blowing on the enclosure [E4]
- moved: none
- removed: FT-0 rod collar (MK-17) [MK-17]; Film applicator, parked (M4) [M4]

**FT-1 -> FT-1V** (13 added, 36 moved, 8 removed, 18 unchanged)

- added: Ideal Vacuum 12 in. cube frame P107540 [E2]; Cube top plate, bored for the window ring (MK-13) [MK-13]; Cube bottom plate, bored for the rod gland (MK-14) [MK-14]; Cube front plate = door (hinge kit P106868) [E2]; Cube back plate (KF-25 feedthroughs) [E2]; Cube left plate (pump and gauge ports) [E2]; Cube right plate (argon in, exhaust, vent) [E2]; Door hinges (hinge kit) [E2]; KF-25 ports: pump, Pirani, argon, exhaust, 2 electrical feedthroughs [E3]; Rotary-vane pump (McMaster 4396K21 class, envelope est.) [E3]; KF-25 pump hose and valve [E3]; Beam tube, short, with lens collar (MK-10) [MK-10]; Piston rod, long, for the cube (MK-06) [MK-06]
- moved: Gantry cross-beam (clamped at the lens height) [E4]; Scan-head plate (MK-09) [MK-09]; SCANLAB hurrySCAN 25 (envelope) [L3]; f-theta lens f = 254 mm (envelope) [L4]; Collimator (L2 if the fibre has none) [L2]; Process fibre [L1]; +-15 V supply for the head (DIN, est.) [L6]; Deck plate (MK-01) [MK-01]; Window ring (MK-02) [MK-02]; Window, Ø50.8 x 9.53 fused silica, 1064 V-coat [L8]; Window retaining flange (MK-02) [MK-02]; Cover-slide holder (MK-02) [MK-02]; Cover slide, Ø50 x 1 mm [L8]; Beam-tube interlock switch [S1]; Macor standoffs under the well block (4) [H4]; Well block, Ø40.00 bore (MK-03) [MK-03]; Well-block heaters, 2 x 50 W [H1]; Substrate disc Ø39.8 x 6 (MK-05) [MK-05]; Heater plate Ø39.8 x 28 (MK-04) [MK-04]; Fibreglass rope wiper [H4]; Plate heaters, 2 x 1/4 x 1 in. [H1]; Overflow cup (MK-16) [MK-16]; Slot nozzle 45 x 4 mm (MK-11) [MK-11]; Exhaust collector (MK-11) [MK-11]; Argon feed tube to the nozzle [G3]; Exhaust hose to the HEPA [G3]; Zaber X-LSQ075B-E01 recoater stage (body est.) [M1b]; X-LSQ carriage [M1b]; Carriage bracket and arm (MK-08) [MK-08]; Stage shield (MK-12) [MK-12]; Hopper, ~30 cm3 (MK-08) [MK-08]; Silicone-cord blade, 3 mm [M3]; Cord clamp (MK-08) [MK-08]; Vibration motor [M3]; Coded lid switches (2) [S1]; 120 mm fan blowing on the enclosure [E4]
- removed: 304 NEMA 4X box, 16 x 12 x 8 in. (body) [E1]; Lid gasket, FKM cord [E1]; Box lid (the door), window bore [E1]; Continuous hinge [E1]; Lid clamps (4) [E1]; Inner clamp ring (MK-02) [MK-02]; Beam tube, long, with lens collar (MK-10) [MK-10]; Piston rod (MK-06) [MK-06]

