# Completeness audit: every part in the model against the BOM (2026-11-22)

For [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to Sterling's
question: "Have you been thorough in terms of both mechanical and electrical components? And optical of course".
This note covers the mechanical and whole-machine side. The electrical design and the optics audit are separate notes.
Nothing here has been built, quoted by a shop or reviewed by BYU's LSO or EHS.

## Short answer

**Before this audit, no.** The model's part list (`analysis/out/mass.json`, 223 parts) was checked part by part
against `bom.csv` and the part-number lists. At the start of the audit (bom.csv as committed in `cc1e0a1`):
- **87** parts were real parts with a vendor price and **26** were custom parts costed in a BOM line;
- **70** parts were in no bom.csv line at all, and **29** contradicted their BOM line;
- the BOM still described the tall model's welded box, 30 mm T-slot cabinet and ball-screw piston (G1, S9, M3), and
  the model tagged parts with lines that did not exist (D1, F3, F4, F5).

**Now:** 117 priced, 4 real but unpriced, 22 generic, 65 custom, **2 missing** and **12 inconsistent**. The BOM total
goes from **$39,440 – $112,978** to **$57,941 – $144,841**. $7,708 – $20,770 of the rise is line X1, the machining no
line costed before. Without X1 the total is $50,233 – $124,071.

## How it was checked

[`analysis/audit/completeness.py`](analysis/audit/completeness.py) reads:
- the part list in `analysis/out/mass.json`;
- each part's own BOM tag and part number (`bom`, `mcm` in `cad/lpbf_low.py`), dumped to
  [`analysis/out/audit/model_tags.json`](analysis/out/audit/model_tags.json) from a snapshot of `cc1e0a1`.

It maps every part to a bom.csv line and to rows of `mcmaster-parts.csv`, `fasteners.csv`, `seal-parts.csv`,
`vendor-parts.csv`, `safety-parts.csv`, `robot-tooling.csv`, `assembly-tooling.csv`, `options-*.csv`,
`plate-materials.csv`, `vendor-lookups.csv` and this audit's [`analysis/audit/audit-prices.csv`](analysis/audit/audit-prices.csv).
- **By part number** where the name or tag has one (McMaster `\d{4,5}[A-Z]\d{1,4}`, AS568 dash numbers `2-xxx`, vendor
  part numbers).
- **By an explicit table** in the script for the rest. Each entry names the line and a keyword that the line's text must
  contain, so a stale line fails the check.
- **Model-vs-BOM rules** flag a part as inconsistent when the model and its line (or another analysis) disagree.
- **Custom parts** come from `analysis/out/machining/hours.csv` (48 machined parts) and the sheet parts of
  `cad/render_build.kind()`.

Any CSV named on the command line is read as an extra purchase list. That is how `electrical-bom.csv` and
`optics-bom.csv` are folded in when they exist. Re-run:

```bash
python desktop-lpbf/analysis/audit/completeness.py --bom desktop-lpbf/analysis/out/audit/bom_before.csv --no-audit-prices --tag before
python desktop-lpbf/analysis/audit/completeness.py [desktop-lpbf/electrical-bom.csv desktop-lpbf/optics-bom.csv]
python desktop-lpbf/analysis/audit/completeness.py --dump-tags SNAPSHOT_REPO   # re-dump the model's tags (CadQuery, ~25 s)
```

## The gaps that matter most

1. **No gas-tight recirculation blower exists in the BOM (G4).**
   - The CFD needs 140-200 L/min at 1.5-3 kPa through a sealed loop (`gas-flow.md`).
   - G4 is still a $300-1,500 estimate. The model's envelope is labelled ~100 L/min, which is the pre-CFD figure.
   - This is the one purchase the gas loop cannot work without.
2. **Machining was not costed.** Of the 249.5 h in `hours.csv`, 177.7 h belonged to parts that no line costed: the
   chamber group, base plates, optics bridge, recoater and Z parts, and the robot hardware.
   - X1 now carries them, plus 15-30 h for the sheet parts, at an **assumed** $40-100/h. No shop has quoted.
   - The build modules, metering base, blade holder and reservoir lids are left out of X1: their lines already carry
     machining.
3. **The vacuum pump changes price class.**
   - The model draws a 26 kg dry scroll. G2 had priced the $587.53 McMaster 4396K21 rotary-vane pump.
   - G2 is now an Edwards nXDS6i ($5,977.85, Marshall Scientific; 26.2 kg, 0.02 mbar) or an Agilent IDP-3 ($3,979 list,
     search snippet).
   - `analysis/out/tray/tray_budget.md` still uses the 4396K21's 7 A at 115 V.
4. **Three decisions are still open in the model.**
   - **Cooling:** chilled-water lines run to a laser that IPG quotes as air-cooled (`heat.md` says decide first).
   - **UPS:** the model draws an Eaton 5PX1500RTG2 ($1,137.99) but the tray budget sizes a Vertiv GXT5LI-1500
     ($2,706.99). D2 lists both.
   - **Rack:** the model's 11U rack, 515 mm tall, has no catalogue match. McMaster's 7648K62 cabinet is 10U and
     495 mm tall ($609.03). Its next size is 30 in. tall, and its open racks start at 24U. So either the 3U DIN drawer
     becomes 2U or the rack is a custom frame.
5. **For the optics audit:**
   - L6 still specifies f = 254 mm, while the model uses the Thorlabs FTH160-1064 (f = 160 mm).
   - The IPG 5 mm collimator in the model and L3 gives ~48 µm at f = 160 mm, not 75 µm. `low-profile.md` §2 calls for a
     ~3.2 mm beam.
   - The camera window (Ø1 in., 1070 nm blocking coating) is in no line.
   - The Ø2 in. × 8 mm main window has no part number: L7 names a Ø1 in. WG41050-C.
6. **For the electrical design:**
   - No 2U scan/laser PC is chosen (C1 is the RTC6 card).
   - C6 is a NEMA wall box, but the model draws a 3U DIN-rail drawer.
   - The model tags the UPS C6.
   - A1's load cell is 3 kg; the model's label says 2 kg.
7. **Vacuum feedthroughs and connectors have no price.**
   - The two Ferrotec magnetic-fluid feedthroughs (SFL-006-NN on the recoater, SSL-005-NN on the roller) have no
     published price. They are estimated at $500-1,500 and $400-1,000, against Rigaku's $921.57 alternative.
   - The drawn LEMO 1B rod-end connector fails the seal spec (`seal-parts.csv`).
8. **Chamber stock.**
   - McMaster sells no 6061 plate thicker than 4 in., so the 5-1/2 in. frame blank has to come from a plate distributor.
   - Midwest Steel & Aluminum stocks it, but its price calculator did not load. The blank is estimated at $400-800.
9. **Small parts with no catalogue match:**
   - the drawer's quarter-turn latches (`seals.md`);
   - a 316 SS 0.5 psi relief with an FKM seat (McMaster's stainless reliefs start at 25 psi);
   - an SAE-4 adapter for the 3861N11 transmitter;
   - KF-25 adapters for the HEPA housing's 1/2 NPSC ports and for the blower;
   - two shaft couplings, Dowty-type bonded washers and 1 mm FKM sheet;
   - the CombiTac tray half (no public price; D1 estimates $1,500-5,000).
10. **Smaller fit notes:**
    - The optics posts are drawn 60 × 60 × 5 mm. McMaster's nearest is 2-1/2 × 1/4 in. (6546K31).
    - THK's KR26 rail is nominally 26 mm wide, against the 46 × 28 mm Z envelope.
    - The SMC door actuator weighs 0.60 kg, against the 0.3 kg the model assumes.
    - The hinge is labelled 1151A87 but drawn as custom knuckles.
    - H1's 2317K275 shim is 0.13 mm thick, against the 0.3 mm shields the model draws.

## What changed in bom.csv

- **Rewritten for the low-profile model:**
  - G1 chamber: through-frame stock, floor, lid and door blanks, latches;
  - G2 dry scroll pump;
  - G7 Pirani, 316 relief and SAE-4 adapters; G8 seals from `seal-parts.csv`; G9 Vaisala DMT143;
  - M1 Ferrotec feedthrough; M2 ClearPath part number; M3 THK KR26 Z actuator; M4 roller feedthrough and overflow jar;
    M5 HSS blank; M6 Pi HQ camera and 16 mm lens (Adafruit);
  - S9 rack, 20 mm guard frame and sliding door;
  - S7 the fixed Macurco OX-6 room O2 monitor that `safety-parts.csv` SP1 asks for, in place of the portable 18995T81;
  - G4 a note only: still no gas-tight blower;
  - B2 wipers and bore seals; R1 the KF-16 blank (estimate).
- **Added:** F3 levelling mounts, F4 MIC-6 base plates, F5 optics bridge, H3 module fan (`heat.md`), A3 pneumatics,
  D1 dock and umbilicals, D2 UPS, X1 machining.
- **Not touched:** C1-C6, S1-S4, H2, A1, L1-L7, S5, S6, T1 and T2, which are the electrical and optics lines.
- **Sources:** every fetched price is in [`analysis/audit/audit-prices.csv`](analysis/audit/audit-prices.csv), with its
  URL and UTC time. The prices were read on 2026-11-22 between 05:35 and 05:56 UTC, McMaster's through the lab tunnel.
  Estimates are marked "ESTIMATE" there and "estimate" in `price_basis`.
- **Stale rows left in place:** the tall model's rows in `mcmaster-parts.csv` still exist. These are the G1, S9 and M3
  rows, the 9572K33 V-ring, the 1165N11 cord and the 4277T52 nylon relief. Their lines now say they no longer apply.
  They show up in the reverse table below as rows with no model part.


## Counts by status (generated)

| Status | Before (bom.csv at the start of this audit) | Now |
|---|---|---|
| real part priced | 87 | 117 |
| real part unpriced | 3 | 4 |
| generic | 7 | 22 |
| custom | 26 | 65 |
| missing from BOM | 70 | 2 |
| inconsistent | 29 | 12 |
| excluded | 1 | 1 |
| **total** | 223 | 223 |

Model tags with no bom.csv line: RA1, RA2, RA3, RA4, RA5, RA6, RA7. BOM total now $57,941 - $144,841. Extra purchase lists read: none.


## BOM lines this audit changed (generated from [`analysis/out/audit/bom_before.csv`](analysis/out/audit/bom_before.csv), the BOM at the start)

| Line | Item now | Was (USD, qty x unit) | Now (USD) | Candidate now |
|---|---|---|---|---|
| M1 | Recoater axis (less servo) | 881 – 2,481 | 1,326 – 2,346 | McMaster 4566N101 M12 x 10 mm lead screw (cut) + 4566N401 nut, 6709K33 rail + 6709K12 carriage, 6446K781 coupling; Ferrotec SFL-006-NN magnetic-fluid feedthr... |
| M2 | Servo motors | 530 – 972 | 530 – 586 | Teknic ClearPath-SD CPM-SDSK-2311S-RLN (recoater and Z; vendor-parts.csv) |
| M3 | Z stage (less servo): integrated actuator under the floor | 752 – 852 | 923 – 1,113 | THK KR2602A-0110-0-01A0 KR26 actuator, 2 mm lead, 110 mm stroke (Oriental Motor, a THK reseller: $883.00); GT2/HTD belt and two pulleys; custom Z flange, bel... |
| M4 | Metering base, roller drive and overflow | 282 – 682 | 776 – 1,851 | McMaster 6627T91 NEMA 17 stepper; Ferrotec SSL-005-NN feedthrough (5 mm shaft; drawn); 5-to-5 mm coupling; custom metering base and roller; overflow jar from... |
| M5 | Recoater blade cartridges | 127 – 527 | 275 – 675 | McMaster 2634T15 HSS flat stock (hard blade, the model's default) + 1187N14 3 mm silicone cord (compliant); custom quick-swap holders |
| M6 | Layer camera + lighting | 100 – 300 | 152 – 242 | Raspberry Pi HQ camera (Adafruit 4561) + 16 mm C-mount lens (Adafruit 4562); oblique 24 V LED bar (not chosen) |
| G1 | Process chamber: through-frame, floor plate, lid, door and their small parts | 2,435 – 6,435 | 1,133 – 1,833 | 6061-T651 plate 5-1/2 in. cut to 15 x 9.5 in. from a plate distributor (frame blank; McMaster stops at 4 in.), McMaster 89155K165 1 in. plate (floor), 89155K... |
| G2 | Vacuum pump | 2,079 – 5,491 | 5,470 – 7,469 | Edwards nXDS6i dry scroll (A73501983; 0.02 mbar, 6.8 m3/h, 26.2 kg) + McMaster 3394N12 KF-25 inlet filter + 2 x 3497N23 KF-25 hose |
| G7 | Valves / fittings / gauges | 3,281 – 3,781 | 3,680 – 3,980 | McMaster: 3861N11 0-15 psia + 5539N26 0-10 inH2O transmitters, 2 x 8077K237 24 V NC solenoids, 4123K45 KF-25 ball valve, 7833K76 needle valve, KF-25/40 alumi... |
| G8 | Chamber, module and port seals | 16 – 16 | 231 – 291 | McMaster 96515K127 0.139 in. cord (10 ft), 96515K123 0.070 in. cord (3 ft), 16 packs of 9464K AS568 rings and 5267T786 port rings (seal-parts.csv), 9262N11 s... |
| G9 | Dew-point / moisture sensor | 1,000 – 2,500 | 1,868 – 2,282 | Vaisala DMT143 (Selectum, a Vaisala distributor: $2,281.70) |
| S7 | Room O2-deficiency monitor | 459 – 459 | 663 – 1,275 | Macurco OX-6 fixed O2 monitor (0-25 % O2, 4-20 mA, 2 relays, LED): $663 (Kele, search extract; list $1,275) |
| S9 | Rack, guard frame, guard panels and sliding guard door | 2,009 – 2,309 | 1,583 – 1,833 | McMaster 7648K62 steel 19 in. cabinet (10U inside, 495 x 533 x 622 mm) + 7648K69 back panel; 20 mm T-slot 5537T101 x 4 (8 ft), corner brackets 5537T935 x 24,... |
| F3 | Levelling mounts (process and gas modules) | new line | 61 – 61 | McMaster 5537T983 |
| F4 | Module base plates (process and gas) | new line | 1,349 – 1,499 | McMaster 86825K49 5/8 in. MIC-6, 24 x 72 in. (one sheet nests both plates) |
| F5 | Optics bridge, posts and beam-path mounts | new line | 796 – 896 | McMaster 89155K86 (bridge), 6546K31 (posts); 3/8 in. 6061 offcuts for the riser, ring and aperture |
| H3 | Module cooling fan under the floor | new line | 44 – 74 | McMaster 1939K12 |
| B2 | Module seals, clamping and Z coupling | 81 – 218 | 111 – 318 | McMaster 9464K982, 95966A705 + 91065A610, 91732A782, 5679K95, 89095K23, 6435K35; 2-238 FKM (same family as 9464K367, not fetched) |
| R1 | Reservoirs S / M / L (38 / 97 / 233 cm3) with shutters | 473 – 1,273 | 493 – 1,313 | McMaster 8983K56 sheet, 8969T3 springs, 85015A47 plungers |
| A3 | Pneumatic door drive and latch actuators, valves and air prep; robot handles and tags | new line | 970 – 1,120 | SMC CDRQ2BS20-180 rotary actuator, 2 x CDQ2B20-15DZ-F7PS cylinders, SS5Y3-45FD-05U-N7 manifold + 2 x SY3140-5LOZ valves, 4 x AS2201F-01-06S speed controllers... |
| D1 | Tray dock (tray half) and umbilicals | new line | 1,728 – 5,628 | Staubli CombiTac (frame, housing, power, signal, air, fluid modules: configurator or sales office, no public price); 1/4 in. 316 tube for the argon line; 1-1... |
| D2 | UPS (2U, in the rack) | new line | 1,138 – 2,707 | Eaton 5PX1500RTG2 (1440 VA / 1440 W, line-interactive; CDW $1,137.99) |
| X1 | Machining and fabrication of the custom parts not costed elsewhere | new line | 7,708 – 20,770 | BYU ME Prototyping Lab (Haas VF-4 + HRT210) or a job shop |

BOM total: $39,440 – $112,978 before, $57,941 – $144,841 now.


## Every model part (generated; also in [`analysis/out/audit/model_vs_bom.csv`](analysis/out/audit/model_vs_bom.csv))

Fasteners (tag `fastener`, all McMaster and all in `fasteners.csv` / line FX) are counted above but listed only in the CSV.

| Status | Part | Kind | BOM line | Part numbers | Note |
|---|---|---|---|---|---|
| inconsistent | DIN-rail drawer: 24 V supply, safety relay, ClearCore, Pi 5 (3U) | bought | – | – | contents in C3, C4, S1, C2; model tag C3 does not cover it; model draws a 3U 19 in. DIN-rail drawer; C6 is a McMaster 7812K14 NEMA wall box |
| inconsistent | Load cell (single-point, 2 kg, carries the dock rails: reservoir inventory) | bought | A1 | ALLUE3 | model label 2 kg; A1 lists a 3 kg Laumas ALLUE3 |
| inconsistent | Chilled-water supply + return to the laser | bought | D1 | – | model runs chilled water to the laser; the quoted IPG YLR-500-U3-SM-AC is air-cooled (L2), and heat.md says decide water vs air first |
| inconsistent | UPS (Eaton 5PX1500RTG2, 2U) | bought | D2 | 5PX1500RTG2 | model tag is C6 (controls enclosure), which has no UPS; model draws an Eaton 5PX1500RTG2; analysis/out/tray/tray_budget.md sizes the UPS as a Vertiv GXT5LI-1500 |
| inconsistent | Door hinge knuckles on the chamber (304 SS) | custom (machined) | G1 | 1151A87 | not in machining/hours.csv; model labels the hinge McMaster 1151A87 but draws custom 304 knuckles; the real 1151A87 is a 3 x 3 in. two-leaf lift-off hinge (real-parts.md) |
| inconsistent | Door hinge leaves + knuckles (304 SS, slotted pin holes: floating hinge) | custom (machined) | G1 | 1151A87 | not in machining/hours.csv; model labels the hinge McMaster 1151A87 but draws custom 304 knuckles; the real 1151A87 is a 3 x 3 in. two-leaf lift-off hinge (real-parts.md) |
| inconsistent | Sealed side-channel blower (gas-tight, ~100 L/min) | bought | G4 | – | no gas-tight blower of this size found (real-parts.md); model label says ~100 L/min; the CFD needs 140-200 L/min at 1.5-3 kPa (gas-flow.md, G4 spec) |
| inconsistent | Hermetic connector M50 on the rod end (hermetic receptacle, LEMO 1B envelope (HGG.1B.310)) | bought | H1 | HGG.1B.310.CLLPV | seal-parts.csv: the drawn LEMO 1B receptacle fails the spec; the Accu-Glass 9C-K16 that meets it needs a KF-16 port on the rod end |
| inconsistent | Radiation shields M50 (2 x 0.3 mm polished 316, clamped between the Macor rings) | custom (sheet) | H1 | 2317K275 | model's shields are 0.3 mm; H1's 2317K275 shim is 0.005 in. (0.13 mm) |
| inconsistent | Collimator (IPG, 5 mm beam, 128 mm + 78 mm strain relief) on V-mount | bought | L3 | – | not priced by IPG yet; low-profile.md §2: f = 160 mm needs a ~3.2 mm beam for the 75 um spot; the model and L3 keep IPG's 5 mm collimator (sized for f = 254 mm; ~48 um at f = 160) |
| inconsistent | f-theta lens, f = 160 mm (Thorlabs FTH160-1064) | bought | L6 | FTH160-1064 | model uses f = 160 mm (Thorlabs FTH160-1064, $1,011.78 in vendor-lookups.csv); L6 still specifies f = 254 mm |
| inconsistent | 19 in. rack frame (11U, 515 mm tall) | bought | S9 | 7648K62 | model draws an 11U rack 515 mm tall; S9's McMaster 7648K62 cabinet is 10U (no catalogue 11U rack that low was found) |
| missing from BOM | Camera window (Ø1 in. x 3 mm fused silica, 1070 nm blocking coating) | bought | – | – | no BOM line has a Ø1 in. window with a 1070 nm blocking coating; model tag M6 does not cover it |
| missing from BOM | Scan + laser controller PC (2U) | bought | – | – | C1 is the RTC6 card; no 2U PC is chosen; model tag C1 does not cover it |
| generic | Bore seal M50 (aramid felt + carbon-filled PTFE scraper) | bought | B2 | – | carbon-filled PTFE / aramid felt: no stock part number chosen |
| generic | Plate rim wiper M50 (carbon-filled PTFE split ring; keeps powder out of the hot gap) | bought | B2 | – | carbon-filled PTFE / aramid felt: no stock part number chosen |
| generic | Argon supply from the dock | bought | D1 | – |  |
| generic | Pump exhaust to the dock | bought | D1 | – |  |
| generic | Tray dock (CombiTac-type, mates sideways) | bought | D1 | – |  |
| generic | Drawer latch receptacles in the lid (2 x quarter-turn latch) | bought | G1 | – | seals.md: no catalogue quarter-turn latch fits the 20 mm plate |
| generic | Drawer latches: 2 x quarter-turn latch studs (envelope) | bought | G1 | – | seals.md: no catalogue quarter-turn latch fits the 20 mm plate |
| generic | Blower inlet (KF-25) | bought | G7 | – | adapters to the filter's 1/2 NPSC ports / the blower not chosen |
| generic | Blower outlet (KF-25) | bought | G7 | – | adapters to the filter's 1/2 NPSC ports / the blower not chosen |
| generic | Filter inlet (KF-25) | bought | G7 | – | adapters to the filter's 1/2 NPSC ports / the blower not chosen |
| generic | Filter outlet (KF-25) | bought | G7 | – | adapters to the filter's 1/2 NPSC ports / the blower not chosen |
| generic | O2 sample line (1/8 in. 316L) | bought | G7 | – |  |
| generic | Overpressure relief valve (316 SS, FKM seat, +34 mbar; SAE-4 O-ring-boss port) | bought | G7 | – |  |
| generic | Camera window flat ring (FKM 75A sheet, 1.0 mm, squeezed to 0.75) | bought | G8 | – | FKM sheet: part number not confirmed (seal-parts.csv) |
| generic | Rail-hole bonded seal washers (4 x M4, 316 ring + FKM lip, Dowty type; seal the through-tapp... | bought | G8 | – | Dowty-type M4 washer: no part number chosen |
| generic | Window clamp ring, upper (FKM 75A sheet, 1.0 mm, squeezed to 0.75) | bought | G8 | – | FKM sheet: part number not confirmed (seal-parts.csv) |
| generic | Safety shutter + beam dump | bought | L4 | – | no shutter chosen (L4: quote) |
| generic | Ø2 in. fused-silica window, 8 mm, AR 1064 | bought | L7 | – | L7 names a Ø1 in. Thorlabs WG41050-C; the model's Ø2 in. x 8 mm window has no part number |
| generic | Recoater shaft coupling (clamp type, 6 to 8 mm, in the wall bore) | bought | M1 | – |  |
| generic | Roller drive coupling (5 mm to 5 mm) | bought | M4 | – |  |
| generic | Layer-light LED bar | bought | M6 | – |  |
| generic | Side reservoir port (KF-16 flange machined in the 6061 base, blanked; reserved for a >= 500 ... | bought | R1 | – | KF-16 blank: no part number |
| real part unpriced | Hermetic-connector O-ring M50 (FKM 75A 2-014, face seal under the flange) | bought | G8 | 2-014 |  |
| real part unpriced | Roller feedthrough O-ring (FKM 75A 2-012, under the housing's shoulder) | bought | G8 | 2-012 |  |
| real part unpriced | Recoater fixed bearing: magnetic-fluid rotary feedthrough Ferrotec SFL-006-NN on the left wa... | bought | M1 | SFL-006-NN |  |
| real part unpriced | Roller shaft: magnetic-fluid rotary feedthrough Ferrotec SSL-005-NN in the metering base (M8... | bought | M4 | SSL-005-NN |  |
| real part priced | Drawer-closed sensor (inductive M12, on the lid's front face, sees the plate's end) | bought | A1 | PAM-AP-1H |  |
| real part priced | Module-present sensor (inductive M12, under the floor, sees the module flange) | bought | A1 | PAM-AP-1H |  |
| real part priced | NFC reader antenna (in the dock's side face, reads the tag on the reservoir plate's edge) | bought | A1 | 364 |  |
| real part priced | Overflow-jar present sensor (inductive M12, PNP) | bought | A1 | PAM-AP-1H |  |
| real part priced | Plate-height through-beam (M6 threaded fibre heads in the side walls, z +5 mm) | bought | A1 | E32-T61-S |  |
| real part priced | Reservoir-docked sensor (inductive M12, at the back of the dock) | bought | A1 | PAM-AP-1H |  |
| real part priced | Cover slide (Ø2 in. x 3 mm fused silica, consumable) | bought | A2 | 25-250 |  |
| real part priced | Door drive: pneumatic rotary actuator on the hinge axis, SMC CRQ2 size 20 class (~1.8 N m at... | bought | A3 | 6597K124 CDRQ2BS20-180 |  |
| real part priced | Draw-latch actuators: 2 x Ø20 compact air cylinders (SMC CJ2/CQ2 class, 157 N at 0.5 MPa) th... | bought | A3 | CDQ2B20-15DZ-F7PS |  |
| real part priced | Pot magnet (NdFeB in a steel cup, Ø25 x 7, 44 lbf, holds the rod's striker) | bought | B2 | 5679K95 | heat.md: swap the NdFeB cup for SmCo |
| real part priced | Leveling mounts, gas module (McMaster 5537T983: Ø25 base, M8 stem threaded up through the pl... | bought | F3 | 5537T983 |  |
| real part priced | Leveling mounts, process module (McMaster 5537T983: Ø25 base, M8 stem threaded up through th... | bought | F3 | 5537T983 |  |
| real part priced | Draw latches on the chamber's side faces (2 x McMaster 1807A61, 304 SS, 3.6 kN rated, preloa... | bought | G1 | 1807A61 |  |
| real part priced | Draw-latch strikes on the door's ears (1807A61 strike plates) | bought | G1 | 1807A61 |  |
| real part priced | Dry scroll pump (≤ 0.3 mbar, 6 m3/h class) | bought | G2 | A73501983 |  |
| real part priced | Pump inlet (KF-25) | bought | G2 | 4518K49 | the nXDS6i inlet is NW25; only the 4396K21 alternative needs a flare-to-NPT adapter + 4518K49 |
| real part priced | Argon pressure regulator + flowmeter | bought | G3 | 78595A5 |  |
| real part priced | Sealed cyclone + HEPA housing (316L, valves off for passivation) | bought | G5 | 5169K72 | cyclone stage not chosen |
| real part priced | Trace O2 analyzer + dew-point transmitter (panel box) | bought | G6 | Microx | dew-point transmitter is line G9 |
| real part priced | Argon line (1/4 in. 316L) | bought | G7 | 89785K824 |  |
| real part priced | Argon solenoid manifold (purge / make-up / vent) | bought | G7 | 8077K237 | custom manifold block not costed |
| real part priced | Gas-loop + vacuum hoses (KF-25 SS bellows) | bought | G7 | 3497N23 | real-parts.md: routed lengths not matched to the 24 in. hose |
| real part priced | Inlet plenum port (KF-25) | bought | G7 | 5786N23 |  |
| real part priced | Outlet plenum port (KF-25) | bought | G7 | 5786N23 |  |
| real part priced | Overflow clamp (KF-40) | bought | G7 | 4518K73 |  |
| real part priced | Overflow port (KF-40) | bought | G7 | 5786N25 |  |
| real part priced | Pressure transducer (7/16-20 SAE-4 O-ring-boss port) | bought | G7 | 3861N11 |  |
| real part priced | Vacuum isolation valve (McMaster 4123K45 KF-25 manual ball valve) | bought | G7 | 4123K45 |  |
| real part priced | Vacuum port (KF-25, stub welded into the adapter plate) | bought | G7 | 5786N23 |  |
| real part priced | Camera adapter O-ring (FKM 75A 2-022, face seal on the lid) | bought | G8 | 2-022 |  |
| real part priced | Camera window O-ring (FKM 75A 2-017, under the window) | bought | G8 | 2-017 |  |
| real part priced | Door O-ring (FKM 75A 1.78 mm cord, vulcanized splice, in a half-dovetail groove) | bought | G8 | 96515K123 |  |
| real part priced | Drawer O-ring (FKM 75A 2-033 in a half-dovetail groove, seals on the lid's front face) | bought | G8 | 2-033 |  |
| real part priced | Fibre-head O-rings (2 x FKM 75A 2-010, face seals) | bought | G8 | 2-010 |  |
| real part priced | Floor O-ring (FKM 75A, 3.53 mm cord, vulcanized splice, 25 % squeeze; face seal in the floor... | bought | G8 | 96515K127 |  |
| real part priced | Inlet plenum O-ring (FKM 75A 2-044, face seal on the back wall) | bought | G8 | 2-044 |  |
| real part priced | Lid O-ring (FKM 75A, 3.53 mm cord, 25 % squeeze) | bought | G8 | 96515K127 |  |
| real part priced | Metering-base O-ring on the lid (FKM 75A 2-040, round the dose slot) | bought | G8 | 2-040 |  |
| real part priced | Metering-base dock-face O-ring (FKM 75A 2-040, seals the reservoir's base plate) | bought | G8 | 2-040 |  |
| real part priced | Module M50 gland-plate O-ring (FKM 75A 2-034, face seal on the tube end and collar) | bought | G8 | 2-034 |  |
| real part priced | Outlet plenum O-ring (FKM 75A 2-044, face seal under the floor) | bought | G8 | 2-044 |  |
| real part priced | Overflow funnel O-ring (FKM 75A 2-042, face seal under the floor) | bought | G8 | 2-042 |  |
| real part priced | Recoater bearing-cap O-ring (FKM 75A 2-019) | bought | G8 | 2-019 |  |
| real part priced | Recoater feedthrough O-rings (2 x FKM 75A 2-024, spacer to wall and to flange) | bought | G8 | 2-024 |  |
| real part priced | Reservoir M lid O-ring (FKM 75A 2-030) | bought | G8 | 2-030 |  |
| real part priced | Rod O-rings M50 in the bottom flange (2 x FKM 75A 2-114, dynamic rod glands) | bought | G8 | 2-114 |  |
| real part priced | Spigot O-ring (FKM 75A 2-238, radial seal in the floor port; groove root Ø90.5 x 4.8) | bought | G8 | 2-238 |  |
| real part priced | Vacuum port adapter O-ring (FKM 75A 2-024) | bought | G8 | 2-024 |  |
| real part priced | Window O-ring, lower (FKM 75A 2-031, under the window) | bought | G8 | 2-031 |  |
| real part priced | Window-flange O-ring (FKM 75A 2-036, face seal on the lid) | bought | G8 | 2-036 |  |
| real part priced | Cartridge heaters M50 (3 x 50 W, 24 V, Ø6 x 22) | bought | H1 | 3714N36 |  |
| real part priced | Thermal cutoff M50 (240 C, in series with the heaters) | bought | H1 | RT240 | model tag H2; the RT240 is costed in H1 |
| real part priced | Type K thermocouples M50 (control, edge, limit; 0.04 in. ungrounded, 316 sheath) | bought | H1 | 3871K606 |  |
| real part priced | Fiber laser source, 500 W single-mode, IPG YLR-500-U3-SM-AC (4U) | bought | L1 | YLR-500-U3-SM-AC |  |
| real part priced | Process fiber (armoured, ≥ 100 mm bend radius) | bought | L1 | YLR-500-U3-SM-AC | comes fitted to the laser |
| real part priced | 2-axis galvo scan head (SCANLAB basiCube 20) | bought | L5 | basiCube 20 |  |
| real part priced | Recoater ball nut (flange on the +x face) | bought | M1 | 4566N401 |  |
| real part priced | Recoater ball screw (M12, 10 mm lead) | bought | M1 | 4566N101 |  |
| real part priced | Recoater carriage (15 mm rail) | bought | M1 | 6709K12 |  |
| real part priced | Recoater guide rail (15 mm, 260 mm) | bought | M1 | 6709K33 |  |
| real part priced | Recoater servo (ClearPath-SD, NEMA 23) | bought | M2 | CPM-SDSK-2311S-RLN |  |
| real part priced | Z servo (ClearPath-SD, NEMA 23, folded) | bought | M2 | CPM-SDSK-2311S-RLN |  |
| real part priced | Z actuator body (KR-class U-rail, 2 mm lead, 100 mm stroke class) | bought | M3 | KR2602A-0110-0-01A0 | the carriage is part of the actuator |
| real part priced | Z carriage | bought | M3 | KR2602A-0110-0-01A0 | the carriage is part of the actuator |
| real part priced | Dosing stepper (NEMA 17) | bought | M4 | 6627T91 |  |
| real part priced | Overflow jar (KF-40 half nipple, 90 mm, ~120 cm3 + blank) | bought | M4 | 4518K42 |  |
| real part priced | HSS recoater blade (1.5 mm, wide nose) | bought | M5 | 2634T15 9011K104 | cut from M2 HSS sheet |
| real part priced | Layer camera (Pi HQ + C-mount lens) | bought | M6 | 4561 |  |
| real part priced | Guard-locking door switch (Omron D4JL) | bought | S2 | D4JL-4NFA-C5-NPT |  |
| real part priced | E-stop | bought | S3 | XA1E-BV3U02-R |  |
| real part priced | Emission indicator | bought | S4 | 7545K316 |  |
| real part priced | Key switch | bought | S4 | 6749K3 |  |
| real part priced | Reset button | bought | S4 | 6749K201 |  |
| real part priced | OD 7+ viewing window (1070 nm, polycarbonate) | bought | S5 | LW1P1/M |  |
| real part priced | Guard door rail (top + bottom) | bought | S9 | 5537T353 | rails are the frame's own 20 mm T-slot; McMaster 5537T353 rollers |
| real part priced | Guard frame (20 mm T-slot) | bought | S9 | 5537T101 |  |
| custom | Lift-out wall liners (0.5 mm 316L, back + sides, spring clips) | custom (sheet) | A2 | 2317K278 |  |
| custom | AprilTag plates (2 x tag36h11, 56 mm, on the guard's front-left post: wrist-camera re-regist... | custom (machined) | A3 | – |  |
| custom | Blade-cartridge grip fin (6061, 4 mm, on the holder's front end) | custom (machined) | A3 | – |  |
| custom | Door drive bracket (6061, 4 mm, flanged onto the chamber's left side face) | custom (machined) | A3 | – | not in machining/hours.csv |
| custom | Door drive shaft and disc (Ø6 D-shaft keyed into a 6061 disc screwed to the door's left edge) | custom (machined) | A3 | – | not in machining/hours.csv |
| custom | Drawer latch wing head, left (26 mm wing on the quarter-turn stud: the robot turns it 90 deg) | custom (machined) | A3 | – | not in machining/hours.csv |
| custom | Drawer latch wing head, right (26 mm wing on the quarter-turn stud: the robot turns it 90 deg) | custom (machined) | A3 | – | not in machining/hours.csv |
| custom | Guard-door handle for the robot (Ø12 x 130 bar on two Ø10 standoffs, 6061) | custom (machined) | A3 | – |  |
| custom | Liner pull tabs (316L, 2 mm, 12 mm off each side liner, spot-welded) | custom (machined) | A3 | – | not in machining/hours.csv |
| custom | Build module M50: spigot, flange, honed 316L cylinder (Ø50.8 bore, 3 mm wall) and bottom col... | custom (machined) | B1 | – |  |
| custom | Build plate M50 (Ø50.5 x 10, 6061-T6; bayonet spigot, gripper groove) | custom (machined) | B1 | – |  |
| custom | Hollow piston rod M50 (5/8 in. x 0.065 in. seamless 316, polished Ra <= 0.2 um where it runs... | custom (machined) | B1 | – |  |
| custom | Module M50 bottom flange: gland plate (316L, bolted to the welded collar; two FKM 2-114 rod ... | custom (machined) | B1 | 2-114 |  |
| custom | Module M50 handle (6061, screwed under the gland plate; for a hand or a gripper) | custom (machined) | B1 | – |  |
| custom | Piston head M50 (6061-T6, cool side of the break; Tier B: 316L with a water channel) | custom (machined) | B1 | – |  |
| custom | Rod end M50: end cap with a side boss for the hermetic connector (316L, rod welded in) | custom (machined) | B1 | – |  |
| custom | Striker disc M50 (416 stainless, on the pot magnet) | custom (machined) | B2 | 89095K23 |  |
| custom | Umbilical duct along the back edge | custom (sheet) | D1 | – |  |
| custom | Base plate, gas module (MIC-6, 15 mm) | custom (machined) | F4 | – |  |
| custom | Base plate, process module (MIC-6, 15 mm) | custom (machined) | F4 | – |  |
| custom | Enclosed beam tube | custom (machined) | F5 | – |  |
| custom | Field-stop aperture (Ø36, passive beam limit) | custom (machined) | F5 | – |  |
| custom | Galvo riser plate (6061, 10 mm) | custom (machined) | F5 | – |  |
| custom | Optics bridge (6061, 25 mm) | custom (machined) | F5 | – |  |
| custom | Optics bridge posts (60 x 60 x 5 square 6061 tube, 10 mm end caps TIG-welded in) | custom (machined) | F5 | – |  |
| custom | f-theta adapter ring (6061, M85x1 internal thread, bolted under the bridge) | custom (machined) | F5 | – |  |
| custom | Camera viewport adapter + boss (6061; Ø1 in. window, 1070 nm blocking filter; FKM face O-rin... | custom (machined) | G1 | – |  |
| custom | Camera window retaining ring (bottoms metal-to-metal on the boss) | custom (machined) | G1 | – |  |
| custom | Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal groove, latch ears) | custom (machined) | G1 | – |  |
| custom | Chamber floor plate (6061-T6, 20 mm, bolted under the frame; floor O-ring gland, module port... | custom (machined) | G1 | – |  |
| custom | Chamber legs (6061, 30 x 30) | custom (machined) | G1 | – |  |
| custom | Chamber lid (6061-T6, 16 mm, cover-slide drawer slot) | custom (machined) | G1 | – |  |
| custom | Cover-slide drawer (6061, robot pull tab, half-dovetail seal groove) | custom (machined) | G1 | – |  |
| custom | Cross-flow inlet plenum + nozzle (316L, bolted flange) | custom (sheet) | G1 | – | model tag G4 (blower), which does not cost them |
| custom | Cross-flow outlet plenum under the floor (316L, flat over the module path, bolted flange) | custom (sheet) | G1 | – | model tag G4 (blower), which does not cost them |
| custom | Door handle | custom (machined) | G1 | – |  |
| custom | Gas knife (cover-slide purge, 316L) | custom (sheet) | G1 | – |  |
| custom | Hinge pins (Ø5, 316) | custom (machined) | G1 | – | not in machining/hours.csv |
| custom | Process chamber body (6061-T6 through-frame from 5.5 in. plate, R10 inside corners; floor pl... | custom (machined) | G1 | – |  |
| custom | Vacuum port adapter plate (304, 8 mm, FKM face O-ring) | custom (machined) | G1 | – | machined 304; not in analysis/out/machining/hours.csv |
| custom | Window flange (6061, two FKM O-ring grooves) | custom (machined) | G1 | – |  |
| custom | Window retaining ring (spigot bottoms metal-to-metal: squeeze set by geometry) | custom (machined) | G1 | – |  |
| custom | Heater block M50 (6061-T6, bayonet socket) | custom (machined) | H1 | – |  |
| custom | Macor standoff rings M50 (3 standoffs x 3 rings, Ø8, cut from 8489K75 rod; thermal break) | custom (machined) | H1 | 8489K75 | cut from 8489K75 rod |
| custom | Recoater arm (6061, 40 x 14 web) | custom (machined) | M1 | – |  |
| custom | Recoater carriage block (6061) | custom (machined) | M1 | – |  |
| custom | Recoater feedthrough spacer ring (6061, 9 mm, FKM face O-rings both sides) | custom (machined) | M1 | – |  |
| custom | Recoater floating bearing housing (blind cap, FKM face O-ring) | custom (machined) | M1 | – |  |
| custom | Recoater motor bracket | custom (machined) | M1 | – |  |
| custom | Recoater motor standoff | custom (machined) | M1 | – |  |
| custom | Z bracket + fold-back belt housing (2:1) | custom (machined) | M3 | – |  |
| custom | Z lift arm (6061, 12 mm, pot-magnet coupling) | custom (machined) | M3 | – |  |
| custom | Z mounting flange (bolted under the floor) | custom (machined) | M3 | – |  |
| custom | Dose chute (316L) | custom (sheet) | M4 | – |  |
| custom | Metering base (6061, fluted roller over a 100 mm dose line, two FKM face O-rings) | custom (machined) | M4 | – |  |
| custom | Overflow funnel block (316L, bolted, FKM face O-ring) | custom (machined) | M4 | – |  |
| custom | Blade holder (6061, 18 x 31, quick-swap) | custom (machined) | M5 | – |  |
| custom | Dovetail rails for the reservoirs (lips pull the plate onto the dock O-ring) | custom (machined) | R1 | – | machined 316L; not in hours.csv |
| custom | Reservoir M (97 cm3, 304 SS wedge hopper, 70 mm outlet for the M50 module; same 30 x 112 mm ... | custom (sheet) | R1 | – |  |
| custom | Reservoir M lid with robot handle (grip plane z = 258 for every size; FKM O-ring face seal o... | custom (machined) | R1 | – |  |
| custom | Reservoir M shutter (shown open, as docked; in a slot closed at both ends, springs shut when... | custom (sheet) | R1 | – |  |
| custom | Operator panel box (on the rack's front post) | custom (sheet) | S4 | – |  |
| custom | Laser guard panels (1.5 mm aluminium) | custom (sheet) | S9 | 88895K51 | cut from 5052 sheet |
| custom | Rack side panels (vented) | custom (sheet) | S9 | – | vented sheet panels |
| custom | Sliding guard door (aluminium) | custom (sheet) | S9 | – |  |
| excluded | Reservoir M powder | excluded | – | – | powder feedstock, not a machine part; model tag R1 does not cover it |

## bom.csv lines and the model (generated)

| Line | Item | Model parts mapped | Why none |
|---|---|---|---|
| L1 | Fiber laser source | 2 |  |
| L2 | Laser chiller | **none** | no chiller for the air-cooled IPG unit |
| L3 | Collimator / beam expander | 1 |  |
| L4 | Safety shutter + beam dump | 1 |  |
| L5 | 2-axis galvo scan head | 1 |  |
| L6 | F-theta lens | 1 |  |
| L7 | Chamber laser window + sacrificial cover slide | 1 |  |
| C1 | Scan + laser controller | **none** | the model draws no scan PC (C1 is a card) |
| C2 | Supervisor computer | **none** | inside the drawn DIN-rail drawer |
| C3 | Motion controller | **none** | inside the drawn DIN-rail drawer |
| C4 | 24 V DC supply | **none** | inside the drawn DIN-rail drawer |
| C5 | Thermocouple interface | **none** | inside the drawn DIN-rail drawer |
| C6 | Controls enclosure | **none** | the model draws a 3U drawer, not this wall box |
| M1 | Recoater axis (less servo) | 12 |  |
| M2 | Servo motors | 2 |  |
| M3 | Z stage (less servo): integrated actuator under the floor | 5 |  |
| M4 | Metering base, roller drive and overflow | 7 |  |
| M5 | Recoater blade cartridges | 2 |  |
| M6 | Layer camera + lighting | 2 |  |
| G1 | Process chamber: through-frame, floor plate, lid, door and their small parts | 22 |  |
| G2 | Vacuum pump | 2 |  |
| G3 | Argon supply | 1 |  |
| G4 | Recirculation blower | 1 |  |
| G5 | Filter train | 1 |  |
| G6 | O2 analyzer | 1 |  |
| G7 | Valves / fittings / gauges | 16 |  |
| G8 | Chamber, module and port seals | 26 |  |
| G9 | Dew-point / moisture sensor | **none** | inside the drawn O2 / dew-point panel box (G6) |
| S1 | Safety relay | **none** | inside the drawn DIN-rail drawer |
| S2 | Guard-locking door interlock | 1 |  |
| S3 | E-stop | 1 |  |
| S4 | Key switch + emission indicator + manual reset | 4 |  |
| S5 | Laser-safe viewing window | 1 |  |
| S6 | Laser safety eyewear (service/alignment) | **none** | PPE |
| S7 | Room O2-deficiency monitor | **none** | room safety |
| S8 | Class D extinguisher | **none** | room safety |
| S9 | Rack, guard frame, guard panels and sliding guard door | 6 |  |
| F3 | Levelling mounts (process and gas modules) | 2 |  |
| F4 | Module base plates (process and gas) | 2 |  |
| F5 | Optics bridge, posts and beam-path mounts | 6 |  |
| P1 | Glovebox | **none** | off the tray |
| T1 | Laser power sensor | **none** | commissioning tool |
| T2 | Melt-pool photodiode | **none** | not drawn |
| H1 | Heater stacks for the three build modules | 7 |  |
| H2 | Heater power, switching and independent limit | **none** | inside the drawn DIN-rail drawer |
| H3 | Module cooling fan under the floor | **none** | not drawn yet (heat.md) |
| B1 | Three build modules (Ø25 / Ø50 / Ø75): cylinders, spigot-flanges, pistons, plates, hollow rods | 7 |  |
| B2 | Module seals, clamping and Z coupling | 7 |  |
| R1 | Reservoirs S / M / L (38 / 97 / 233 cm3) with shutters | 5 |  |
| A1 | Step-confirm sensors, reservoir ID and weighing | 7 |  |
| A2 | Cleaning and consumables | 2 |  |
| A3 | Pneumatic door drive and latch actuators, valves and air prep; robot handles and tags | 10 |  |
| D1 | Tray dock (tray half) and umbilicals | 5 |  |
| D2 | UPS (2U, in the rack) | 1 |  |
| FX | Screws, helical inserts, dowels, set screws, retainers and disc springs | 38 |  |
| X1 | Machining and fabrication of the custom parts not costed elsewhere | **none** | labour |

## Purchase-list rows that no model part uses (generated; full list in [`analysis/out/audit/purchase_vs_model.csv`](analysis/out/audit/purchase_vs_model.csv))

Most of these are expected: stock for the custom parts (a plate or bar has no part in the model to carry its part number), tools and fixtures (`assembly-tooling.csv`), the robot cell (`robot-tooling.csv`), room safety and PPE (`safety-parts.csv`), alternatives with qty 0, sizes for the S25 and L75 modules (the model draws M50), and the lab's other plate materials. The stale ones are the tall model's rows in `mcmaster-parts.csv` named above.

| File | Rows with no model part |
|---|---|
| assembly-tooling.csv | 26 |
| audit-prices.csv | 25 |
| fasteners.csv | 3 |
| mcmaster-parts.csv | 43 |
| options-mcmaster.csv | 18 |
| options-vendors.csv | 21 |
| plate-materials.csv | 11 |
| robot-tooling.csv | 27 |
| safety-parts.csv | 28 |
| seal-parts.csv | 13 |
| vendor-lookups.csv | 29 |
| vendor-parts.csv | 2 |

