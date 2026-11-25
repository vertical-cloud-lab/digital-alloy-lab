# Electrical design of the desktop LPBF tray: supply, controls, safety chain, feedthroughs, wiring

Written 2026-11-22 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to
Sterling's question: "Have you considered what will be needed in terms of electrical? Do we need custom PCBs or no? Have you
been thorough in terms of both mechanical and electrical components?" Until now the electrical side was a few BOM lines
(C1-C6, S1-S9, H1-H2, A1, G6, G7, G9, M2, M6, T2) and notes in [`safety.md`](safety.md), [`heat.md`](heat.md),
[`modules.md`](modules.md), [`seals.md`](seals.md), [`real-parts.md`](real-parts.md) and [`robot-ops.md`](robot-ops.md).

Nothing here has been built, wired, or reviewed by a licensed electrician, BYU's LSO, EHS or Fire Marshal. Prices were read
on 2026-11-22 (UTC) from the pages linked in [`electrical-bom.csv`](electrical-bom.csv). A second opinion from Edison
(`r5-electrical-review`, [answer](edison/r5-electrical-review/answer.md)) is folded in and compared in §11.

| File | What it is |
|---|---|
| [`electrical-io.csv`](electrical-io.csv) | 95 devices and signals: signal type, voltage and current, controller and channel, connector, cable, chamber feedthrough, whether the model and the BOM have it |
| [`electrical-bom.csv`](electrical-bom.csv) | the electrical parts with part numbers, prices, URLs and fetch times, and the bom.csv line each one replaces or adds to |
| [`analysis/electrical/heater_loop.py`](analysis/electrical/heater_loop.py) → [`heater_loop.md`](analysis/out/electrical/heater_loop.md) | lumped thermal model fitted to the CalculiX runs, PI tuning, a dense build with and without a dwell, the SSR failing shorted |
| [`analysis/electrical/interlock_logic.py`](analysis/electrical/interlock_logic.py) → [`interlock.md`](analysis/out/electrical/interlock.md) | the safety logic as a function of every input, checked over all 16.8 M input combinations, plus 49 single faults |
| [`analysis/electrical/power_budget.py`](analysis/electrical/power_budget.py) → [`power.md`](analysis/out/electrical/power.md) | dock legs, inrush against the breakers, UPS runtime through a power cut, drawer heat, voltage drop, hermetic-pin heating, earth-leakage current |
| [`analysis/electrical/io_list.py`](analysis/electrical/io_list.py) → [`io_check.md`](analysis/out/electrical/io_check.md) | writes the I/O list and counts channels against the controllers |
| [`cad/electrical_parts.py`](cad/electrical_parts.py) | the electrical parts drawn in the main model since 2026-11-23 (§13): PB1, PB2, home and limit sensors, guard-position switch, two E-stops, dock PE contacts; the Pirani tee is in `lpbf_low.py` section 10 |
| [`cad/electrical.py`](cad/electrical.py) → [`enclosures.md`](analysis/out/electrical/enclosures.md) | separate model of the power box PB1 and the 12U rack with its 4U drawer, checked against the rack, tray rim, duct and operator panel |
| [`analysis/electrical/drawings.py`](analysis/electrical/drawings.py) | [single-line diagram](analysis/out/electrical/single_line.png), [interlock schematic](analysis/out/electrical/interlock.png), [panel layouts to scale](analysis/out/electrical/panels.png) |

## 0. The short answers

**Custom PCBs: no.** Every function has an off-the-shelf part that is cheaper than the engineering time a board would take:
the SCANLAB RTC6 makes the scanner stream (SL2-100 to a basiCube 20 ordered in that version) and the laser timing, a Productivity1000 PLC reads the thermocouples and 4-20 mA
transmitters, a Banner XS26 safety controller runs the interlocks, a DC SSR and two contactors switch the heaters, and
DIN-rail breakouts, M12 cordsets and hermetic feedthroughs with their own connectors do the wiring (§5). The open and
lab-built LPBF machines we found agree: the ones that made a board (DTU's Teensy controller, OPAL) made it to *replace* a
scan card, and none put safety on it. A board is worth making only if the RTC6 is dropped for cost: a ~100 × 80 mm 4-layer
Teensy carrier would cost about $50 in boards and assembly plus ~$60 of parts, and weeks of firmware and timing work (§5).

**Thorough? Not yet, and these were the gaps.** Twenty of the 95 devices and signals have no bom.csv line and 37 are not
drawn in the model ([`io_check.md`](analysis/out/electrical/io_check.md)). The ones that change the design:

1. **There was no supply design.** No main disconnect, no branch protection, no 48 V servo supply, no place for the AC parts
   (the UPS only got a bom.csv line, D2, today). Now: a lockable main disconnect and four AC branches in a power
   box PB1 beside the rack (§1), drawn in the model since 2026-11-23 (§13.2).
2. **The 3U DIN drawer cannot hold the controls.** A safety controller with enough inputs (Banner SC26/XS26) stands 129 mm
   off its rail, and the 480 W DIN supplies 128.5 mm; a 3U drawer has ~120 mm clear. Make it **4U and the rack 12U (560 mm,
   still under the process module's 581.2 mm)**, and move the power parts to PB1 ([panels.png](analysis/out/electrical/panels.png)).
3. **The drawer would cook without a fan:** 72-147 W in a closed 3U box is 51-104 K above the air around it. With the power
   parts in PB1 (with its own 27 CFM filter fan) and an 80 mm fan in the drawer, the controls stay ≤ 10 K above ambient; in the Shuttle's worst case (43 °C, heat.md) that is
   53 °C against the safety controller's 55 °C ([`power.md`](analysis/out/electrical/power.md) §4).
4. **The galvo needs one 24 V (or 30 V) rail at ≤ 2.6-3 A, not ±15 V** (SCANLAB basiCube series data; the tray budget and
   Edison both assumed ±15 V).
5. **The servo bus needs two contactors in series.** ClearPath-SD has no safe torque off, and the interlock check failed with
   one ([`interlock.md`](analysis/out/electrical/interlock.md)).
6. **The 240 °C thermal cutoff is below its own holding rating.** The Cantherm RT240's holding temperature is 205 °C; the S25
   block runs at 216-221 °C and M50 at 205-206 °C in normal running. It will age and may open on its own. The latching limit
   (235 °C) trips 35-51 s after an SSR short on M50 and L75 and keeps the plate under 227 °C, but on S25 the block reaches
   the TCO's 240 °C in 4-5 s (§9.1). Replace the TCO with one rated above ~225 °C holding, or drop it. **Dropped 2026-11-23 (§13.4):** no catalogue cutoff holds 225 °C with a 24 V DC rating.
7. **A dense build trips any sensible limit without a dwell.** With more laser heat than the module loses, the plate drifts up
   (heat.md); the 235 °C limit tripped after 3-12 minutes in every dense case. The scan software's dwell (hold the next layer
   until the plate is within 3 K) keeps it at ~205 °C and costs 22-54 % more build time at the end of the stroke (§9.1).
8. **The sensors on the lid cannot be wired to a Pi in the rack.** The Pi HQ camera's CSI ribbon and the NFC and load-cell
   boards' I2C/SPI want ≤ 0.5 m. Put the Pi 5 in a small box (PB2) on the process module. **Drawn 2026-11-23 (§13.2):** a
   Hammond 1554JGY on the optics bridge, 0.19-0.22 m from the camera, the NFC antenna and the load cell.
9. **The chamber has an LED bar inside it and no feedthrough for it.** Move it outside a window, or add a 2-pin KF16 feedthrough.
   **Still open 2026-11-23 (§13.2):** with no new chamber port allowed, no existing opening can carry it; move the bar outside.
   **2026-11-25 ([`optics.md`](optics.md) §9.2):** put the bar outside, behind a new window low in the back wall, left of the
   inlet plenum. Then nothing electrical goes into the chamber and FT2 isn't needed. The window port isn't drawn yet.
10. **The rod-end connector is not real yet.** The drawn LEMO 1B misses the spec (seals.md), and no catalogue part carries 3
    type K pairs plus power. Six single-lead type K weld-ins (Ø6.27 mm sleeves) and one 4-pin 16 A copper weld-in (Ø12.62 mm)
    do it, but need a rod-end face ~28-30 mm across, not 24 (§6). **Drawn 2026-11-23 (§13.3):** a 72 × 16 mm face in one row (81 mm wide since round 6), because the rod end cannot grow in height or reach.
11. **Missing devices:** home and over-travel sensors on the recoater and Z, a guard-position sensor separate from the lock,
    two more E-stops, a chamber-at-ambient pressure switch, a Pirani gauge port, auto switches on the door actuator (A3's latch
    cylinders carry theirs), an air pressure switch, and a second plate-temperature channel for the door (electrical-io.csv). **Drawn 2026-11-23 (§13.2)** except the LED feedthrough, the chamber-at-ambient switch, the auto switches, the air pressure switch and the second plate channel.
12. **Earth leakage ~8 mA (estimate; ~9.3 mA with the nXDS6i's drive, §13.1).** Above 3.5 mA a plug-in machine needs reinforced protective earth: two PE contacts in
    the dock, and no 5 mA GFCI upstream (§8).

**Electrical BOM:** $11,359 in 94 lines ($1,177 of it estimates, $1,571 optional), not counting the RTC6 and the IPG cable
(quotes). Against today's bom.csv it is **+$8.0k at the low end and +$7.7k at the high end** (§10): the safety controller (+$2.1k),
the rod-end feedthroughs and thermocouple wiring (+$1.5k), the PLC (+$1.1k), the power box (+$0.9k) and the drawer (+$0.5k)
are most of it; the guard lock gets cheaper (−$0.4k).

## 1. Architecture

![Single-line diagram](analysis/out/electrical/single_line.png)

### 1.1 Supply and distribution

**Supply.** byu-vcl PR 318's dock: 208Y/120 V, L1 + L2 + N + PE, a 30 A two-pole breaker in the lab panel, so 24 A
continuous ([`tray_budget.md`](analysis/out/tray/tray_budget.md)). PR 318 uses a Stäubli CombiTac; its prices are on quote. The
priced equivalent is a Harting Han-Modular docking frame (floating frame $9.56, carrier $9.72; Han C 40 A modules $9.32 and
10 AWG contacts $4.05; Han DD 12-pin signal modules $7.82-8.07; DigiKey, read 05:45Z). Use whatever PR 318 settles on, with:
L1, L2, N at ≥ 30 A, **two leading PE contacts**, an RJ45 module, a 12-pin signal module (tray docked ×2, E-stop loop through the
dock, room-O2 relays ×2, VLM may move, robot signals) and the air line.

**Main disconnect.** The dock is not a disconnecting means (NFPA 79; Edison r5 point 1). Q0 is a lockable 3-pole 30 A rotary
switch at the front of PB1: Socomec SIRCO M Compact 22013003 (UL 98, 100 kA SCCR with 30 A class J fuses, $75) with the
147E1111 red/yellow handle, padlockable in OFF ($27), and a 150 mm shaft ($7) (AutomationDirect, read 06:03Z). ABB OT40F3
(UL 508, $75.05) + OHB45J6 handle ($72.22) and Eaton R5A3040U ($193.03, UL 508, SCCR 10/65 kA) are the alternatives.

**PB1, the power box.** A 16 × 12 × 6 in steel NEMA 12 enclosure on the tray at the left end, beside the rack (the tray has
223 mm free between the rack at x = −990 and the rim at x = −1213). [`cad/electrical.py`](cad/electrical.py) puts the 6 × 12 × 16 in box
there with its handle: no intersection, 16 mm from the rack's side panel and 53 mm from the tray rim
([`enclosures.md`](analysis/out/electrical/enclosures.md)); checked against the rack, rim, duct and operator panel only, not the full model). It holds the
disconnect, the branch breakers, the laser, pump and blower contactors, the UPS-backed DC supplies, the heater supply, SSR,
contactors K1 and K2, the CN708 on the door and the K8DT. The DC supplies sit here, not in the drawer, because their losses
(up to ~60 W) would overheat the drawer. A 27 CFM filter fan (Fandis FF12D24UN, $95) holds PB1 ~5 K above ambient.

| Branch | Breaker (UL 489 DIN) | Switched by | Load | Wire |
|---|---|---|---|---|
| Q1 | 2-pole 15 A, D curve | KM0 (PLC: 5 s after power-up, off between builds) | IPG YLR-500-U3, 208 V L1-L2, 1.7 kW / 1.9 kVA, rear terminal block (2012 YLR guide) | 14 AWG |
| Q2 | 2-pole 15 A, D curve, multiwire (handle-tied) | – | L1-N: UPS (120 V, 1,440 W); L2-N: heater supply LRS-350-24 | 14 AWG |
| Q3 | 2-pole 10 A, D curve (time-lag, Edwards) | KM1 (PLC) | dry scroll pump Edwards nXDS6i, 208 V L1-L2, 6 A rated, 260 W at ultimate (§13.1; was the 4396K21 rotary vane, 115 V 7 A) | 14 AWG, 2.3 m |
| Q4 | 1-pole 6 A, C curve | KM2 (PLC) | recirculation blower (≤ 230 W at its AC upper bound; G4 still open) | 16-14 AWG |

D curves on Q1 and Q2 because the laser, UPS and LRS-350 (60 A cold-start at 230 V, ~30 A at 120 V) each have inrush that a
B curve would trip on ([`power.md`](analysis/out/electrical/power.md) §2). **Closing Q0 energises the laser, UPS and heater
supply together: ~120 A peak against the dock breaker's lowest C-curve magnetic trip of 150 A.** That is why the laser gets a
contactor KM0 that the PLC closes after the rest has started.

**Legs:** worst real case (500 W CW, blower at its AC bound, UPS recharging) is **17.7 A on L1 and 14.0 A on L2, inside
24 A**. The pump never runs while the laser fires (PLC); with everything at rated at once L1 would see 23.7 A and L2 20.0 A (2026-11-23, with the nXDS6i at 208 V, §13.1).

### 1.2 What the UPS carries, and the DC rails

**UPS:** Eaton 5PX1500RTG2 (line-interactive, 1,500 VA / 1,500 W per ENERGY STAR, §13.1; 2U, 5-15P in, 8 × 5-15R; $1,137.99 at CDW, read 2026-11-22),
in bom.csv as D2 (added 2026-11-22). PR 318 standardises on the Vertiv GXT5LI-1500 (online, Li-ion, $2,706.99); either
works. A Network-M3 card ($462.99) lets the Pi start the power-cut sequence.

| Rail | Supply (location) | Backed? | Loads | Protection |
|---|---|---|---|---|
| 120 V AC | UPS outputs | yes | scan PC with the RTC6, the three DC supplies below | UPS |
| +24 V CTRL | Mean Well SDR-240-24, 10 A (PB1), $104.38 | yes | XS26 safety controller, guard lock, PLC and I/O, sensors, valves, ClearCore logic, stepper drive, fans, PB2 (Pi, NFC, load cell, camera), O₂ analyser, transmitters | Phoenix CBMC E4 4-channel electronic breaker, 1-10 A per channel ($122.41) |
| +48 V SERVO | Mean Well SDR-240-48, 5 A (PB1), $104.38 | yes | two ClearPath-SD (24-75 V, Teknic manual rev 3.30) | 10 A fuse; **K3A + K3B in series** from the safety controller |
| +24 V GALVO | Mean Well HDR-100-24, 3.8 A (PB1), $38.18 | yes | SCANLAB basiCube 20 (24 V, ≤ 2.6 A) | own supply, so servo and valve transients stay off the galvo |
| +5 V | Mean Well DDR-30G-5 (PB2), $35.36 | yes | Raspberry Pi 5 | from +24 V CTRL |
| +24 V HEAT | Mean Well LRS-350-24, 14.6 A (PB1), $34.81 | **no** | module heaters 100 / 150 / 250 W | 15 A fuse → K1 → K2 → SSR |

Unbacked: laser, pump, blower, heaters (PR 318's rule for heaters and pumps). On a power cut the build stops, the argon valves
close (they are normally closed), the safety controller, guard lock, PLC, O₂ analyser and Pi stay up, the PC saves and shuts
down at 120 s and the servos are disabled at 60 s. **The held load is ~63 W, which the UPS carries for ~5 h by a Peukert
estimate (4 × 12 V 9 Ah assumed: Eaton's page timed out)**, far past the 15 / 28 / 41 min the plate takes to cool to 50 °C
(power.md §3). At the rated 770 W backed load it would last ~17 min by the model, which ENERGY STAR's figures put 13-25 % optimistic (§13.1).

The 48 V bus is a choice: ClearPath-SD runs on 24-75 V and the manual puts the minimum at about 21.5 V; 48 V gives speed
headroom over 24 V and the recoater (≤ 100 mm/s on a 10 mm lead, 600 rpm) and Z axis need little. Teknic's own IPC-5 (75 V,
350 W, built-in regen control, $253) is the alternative if a fast axis ever regenerates into the bus.

### 1.3 Short-circuit current rating (Edison r5 point 2)

The tray's fault current is set by the lab panel and the branch run, neither known yet. With 10 kA at the panel and 15 m of
10 AWG to the dock plus the 2.7 m dock feeder, a bolted L-L fault at PB1 is about 208 V / 0.14 Ω ≈ 1.5 kA, and L-N about
0.9 kA; with only 5 m of branch it is ~3 kA. **So a panel SCCR of 5 kA covers any branch longer than ~2 m**, and the parts
chosen are rated higher (UL 489 breakers ≥ 10 kA as listed by makers; R5A3040U 10/65 kA). Mark PB1 "SCCR 5 kA" once BYU
Facilities give the panel's available fault current (NEC 409.110 and 670.3; UL 508A SB). Not computed: the exact UL 508A
supplement SB table for the DC supplies.

### 1.4 Where things go

| Place | What | Why there |
|---|---|---|
| **PB1** (tray, left of the rack) | Q0, Q1-Q4, KM0-KM2, K1, K2, SSR on a through-wall heat sink, CN708 (door), K8DT, LRS-350-24, SDR-240-24, SDR-240-48, HDR-100-24, PE bar | next to the largest loads (laser, UPS); heat and mains out of the control drawer; away from the filter on the right |
| **4U drawer** (rack, top) | XS26-2 + XS16si + XS2so, Productivity1000 (CPU + 8 modules), ClearCore, stepper drive, K3A/K3B, K4/K5, Ethernet switch, CBMC E4, 40 terminal blocks, 80 mm fan | low-voltage control only: ~46 W |
| **PB2** (process module, guard frame near the lid) | Raspberry Pi 5, PN532 NFC, NAU7802, Omron E3NX fibre amplifier, M12 junction | CSI, I2C and SPI need ≤ 0.5 m to the camera, antenna and load cell |
| **Gas module** | pump, blower, argon valves, pneumatic manifold, O₂ and dew-point box | as drawn |
| **Rack** | UPS (2U), laser (4U), scan PC (2U), drawer (4U): **12U, 560 mm** | the 4U drawer (§0 point 2) |

## 2. Devices and I/O

The full list is [`electrical-io.csv`](electrical-io.csv); the channel count is [`io_check.md`](analysis/out/electrical/io_check.md).

| Controller | Used / capacity |
|---|---|
| Productivity1000 DI (2 × P1-16ND3) | 20 / 32 |
| DO (P1-08TD2 × 4, sourcing 1 A) | 29 / 32 |
| Thermocouple (P1-04THM: control, edge, chamber wall, filter cake) | 4 / 4 |
| 4-20 mA in (P1-08ADL-1: O₂, dew point, absolute and differential pressure, two room O₂) | 6 / 8 |
| 0-10 V in / out (P1-04ADL-2: Pirani; P1-04DAL-2: blower speed) | 1 / 4, 1 / 4 |
| Safety inputs (XS26-2 26 + XS16si 16) | 31 / 42 |
| Safety outputs (XS26-2 4 + XS2so 4) | 6 / 8 |
| ClearCore | M-0 recoater, M-1 Z, M-2 dosing stepper drive, M-3 spare; IO-1..4 home and limit sensors |
| RTC6 | SL2-100 to the basiCube; LASERON (gate) and ANALOG OUT1 (power) to the laser |

**Devices the model does not draw** (37 rows, the main ones): the safety shutter's two position switches (L4 has no product
yet), home and over-travel sensors for the recoater and Z, the door actuator's and latch cylinders' auto switches, the drawbar
release cylinder and its switch, the air pressure switch and dump valve, the heater supply, SSR and contactors, the CN708 and
K8DT, the module fan (heat.md), the chamber-wall and filter-cake thermocouples, the differential pressure transmitter, the
chamber-at-ambient pressure switch, a Pirani gauge (and a KF16 port for it), the argon shutoff at the dock, the exhaust flow
switch, two E-stops, the guard-position sensor, the stack light and HOT lamp, PB1, PB2 and the Pi.

**Devices with no bom.csv line** (20 rows): the axis home and over-travel sensors, the door actuator's auto switches, the
drawbar cylinder and its switch, the air pressure switch and dump valve, the contactors K1-K5, the K8DT, the wall and cake
thermocouples, the chamber-at-ambient switch, the guard-position sensor, the HOT lamp, the Ethernet switch and the cabinet fans.
They are in [`electrical-bom.csv`](electrical-bom.csv). Since this note started, other work added bom.csv lines for the UPS (D2),
the dock (D1), the pneumatics (A3), the module fan (H3) and a Pirani gauge (G7); electrical-bom.csv keeps its own picks for
those as qty-0 alternatives so nothing is counted twice.

## 3. Controllers, and why

| Function | Choice | Price | Why | Alternatives |
|---|---|---|---|---|
| Scan and laser timing | **SCANLAB RTC6 Ethernet board** (in the 2U PC or beside it), basiCube 20 ordered in its **SL2-100** version | quote | laser on/off delays (1/64 µs steps) and skywriting in hardware, two 12-bit 0-10 V outputs, 16- and 8-bit digital I/O, a 15-pin D-sub laser connector; SCANLAB's Linux library (Debian, amd64) covers only the Ethernet board, so Linux means the Ethernet board, driven from Python through ctypes (no Python binding is supplied); the RTC6 speaks SL2-100 and needs an optional converter for XY2-100 heads; used by the IFSW research platform (Edison r5) and GE's M2-Open (RTC5) | Novanta ScanMaster Controller and JCZ DLC2-M4 ($1,785, EZCAD3 SDK, BOM C1) talk XY2-100 directly; Mesa 7I96S + LinuxCNC xy2mod ($149, needs a custom bitfile, Mesa forum); OPAL on a Teensy 4.0: "PRE ALPHA ... DO NOT USE THIS WITH OTHER LASERS THAN LASERPOINTERS" (README) |
| Motion | **Teknic ClearCore CLCR-4-13** + DIN-MNT | $105 + $21 | four step/dir axes made for ClearPath (HLFB read-back), 13 I/O, Ethernet, C++ SDK; 127 × 89 × 25 mm | Klipper on the Pi (BOM C3), Duet 3 |
| Stepper drive (dosing roller) | AutomationDirect SureStep STP-DRV-4830 (3 A/phase, 12-48 VDC) | $99 | step/dir from ClearCore M-2, 24 V; the STP-DRV-4035 is discontinued | – |
| Process I/O and heater PI | **AutomationDirect Productivity1000**: P1-540 CPU + 2 × P1-16ND3 + 4 × P1-08TD2 + P1-04THM + P1-08ADL-1 + P1-04ADL-2 + P1-04DAL-2 | $237 + modules ≈ $1,000 | 24 V industrial I/O, a 4-channel 16-bit thermocouple module, 4-20 mA in, PID with time-proportioned outputs, Ethernet with Modbus TCP for the Python supervisor, 17-21 mm modules | CLICK PLUS C2-03CPU-2 ($277) + C0-04THM ($217); Arduino Opta and Pi HATs have no thermocouple module and aren't industrial I/O |
| Safety | **Banner XS26-2 + XS16si + XS2so**, with four WEG CWBS9-33-30C03 contactors (K3A, K3B, K4, K5; mirror contacts, $108 each) | $1,093.01 + $464 + $370 | 42 safety inputs and 8 safety outputs (0.5-0.75 A) with test pulses and EDM; the logic in §4 needs 31 inputs and 6 outputs | SC26-2 ($904.01) has 26 inputs and is not expandable; Pilz PNOZ m B0 ($871.91, 20 inputs, 4 outputs at 2 A); the G9SE-201 in S1 has too few inputs (safety.md) |
| Heater switching | DC SSR Crydom D1D20 (20 A, 100 mΩ max) on an HS151 heat sink; K1 and K2 WEG CWBS12-33-30C03 safety contactors (mirror contacts, $120 each) | $93.36 + $49.32 + $240 | 10.4 A at up to 10.8 W; the D1D12 in H2 is a 12 A part | Crydom DRA1-CMXE100D10 DIN module ($107.20, 10 A: too close) |
| Independent limit | DwyerOmega CN708, latching, on the limit TC → K2 | $204.60 (H2) | own sensor, own relay, manual reset | – |
| Plate < 50 °C for the door | Omron K8DT-TH1CD on the edge TC | $240.25 | second, independent channel (with the PLC) for the guard unlock; it latches alarms by default (set it non-latching) and listed a 19-week lead time | the 67F bimetal of modules.md; SOLO SL4848-RR-D ($143, panel mount) |
| Supervisor | Raspberry Pi 5 in PB2 | BOM C2 | recipe, state machine, logging, REST API; camera, NFC and load cell next to it | the scan PC (then the camera needs USB or GigE) |

## 4. Safety and interlock logic

![Interlock schematic](analysis/out/electrical/interlock.png)

The safety controller owns every final element; the PLC, the Pi and the RTC6 only *request*. Two final elements per hazard:

| Hazard | Function | Final elements | Inputs that must all hold |
|---|---|---|---|
| Class 4 beam | laser interlock closed (emission possible) | **K4 + K5** in the laser's two-channel interlock loop (dry contacts, Cat 3 PL d, 500 ms in the 2012 YLR guide) **and the shutter** (power to open, spring closed, through K4 + K5 contacts) | 3 E-stops, guard closed, guard locked, key, room and Shuttle O₂ ≥ 19.5 %, limit healthy, robot at Safe Home, tray docked, PLC permissive (chamber O₂ < set point, pressure in window, module and cover slide present, galvo ready), manual reset, no latched fault |
| Opening the guard | unlock | spring-lock guard lock (power to unlock) | laser loop open, shutter closed on both switches, plate < 50 °C (K8DT and PLC), chamber at ambient (pressure switch) |
| Moving parts | 48 V servo bus | **K3A + K3B** in series | E-stops, guard closed and locked |
| Hot plate | heater power | **K1** (safety controller) **+ K2** (CN708, hard-wired) + the SSR | E-stops, limit healthy, room O₂, PLC permissive (O₂ under argon) |
| Argon | supply valve | 24 V through **both O₂-monitor relays and the exhaust flow switch** in series, no controller | room and Shuttle O₂ ≥ 19.5 %, exhaust proven |
| Robot | entry permitted | standard output to the UR (reduced mode lifts a safety plane at the guard opening, "normal mode only": check against UR's e-Series manual) | unlock conditions; the laser chain already needs the robot home |

**What the check found** ([`interlock.md`](analysis/out/electrical/interlock.md)). Over all 2²⁴ = 16.8 M combinations of
inputs, requests and state bits, the eight properties (laser only when every permissive holds; shutter only with the laser
loop closed; unlock only laser-off, shutter-closed, plate-cool, ambient; and so on) have **zero violations**, and every output
is reachable. The single-fault run (each channel stuck closed, stuck open or shorted to its twin; each contact welded; the
shutter stuck open; the laser ignoring its loop; the reset button stuck) **first failed twice**:
- one servo-bus contactor: welded, nothing safety-rated stopped the motors. **Fix: K3A + K3B in series**, both read back.
- the CN708 relay welded: the laser chain lost its over-temperature input with nobody noticing. **Fix: the PLC's own
  over-temperature (control and edge TCs) as a second, diverse input, and a cross-check that latches a fault if the CN708
  relay stays closed while the PLC reads over-temperature.**

Two more rules the model needed to pass: re-arming needs both shutter switches closed, and the laser's status outputs
(Ready, Emission ON) are read back so a laser that ignores its loop is caught. After the fixes **49 of 49 single faults pass**:
each is either safe on the next demand and detected, or already safe. Target **PL d, Category 3** for the laser function
(Edison r5 point 6 agrees); the devices' B10d/MTTFd values are not collected, so the PL is not computed.

**Spring lock or power to lock?** [`safety.md`](safety.md) §4.4 says "Use a power-to-lock design: a spring-lock switch
unlocks on power loss", which mixes the two terms. ISO 14119 prefers the spring-applied, power-released principle where the
hazard outlasts a power cut, and here the plate stays above 50 °C for 15-41 minutes and the chamber can be off ambient. **Use
a spring lock (IDEC HS5L-VC44M-G, 1,400 N, $254.19, replacing the out-of-stock Omron D4JL in S2)** with its manual release
on the guard for maintenance. With the UPS holding the lock ~5 h, a power-to-lock HS5L-VC7Y4M-G ($269.44) would also work,
but it would then depend on the UPS.

**Laser-specific rules:** manual reset after any trip or a power loss over 5 s (21 CFR 1040.10(f)(10)); emission lamps wired
through K4/K5 so they are lit whenever emission is possible; the galvo supply on the UPS and "galvo ready" in the PLC
permissive, so the mirrors are under control before emission and emission stops before galvo power goes (Edison r5 point 7).

## 5. Custom PCBs, function by function

| Function | Off-the-shelf part | Price | When a custom board would pay |
|---|---|---|---|
| Scanner link to the galvo | RTC6 over SL2-100 (quote); for XY2-100: Mesa 7I96S + LinuxCNC xy2mod ($149) | quote / $149 | only to replace the RTC6 (below) |
| Laser modulation and timing | RTC6 LASERON + ANALOG OUT1; IPG takes "CMOS to 24 VDC" on its gate (2012 guide) | in the RTC6 | never on its own: it has to move in step with the mirrors |
| Interlock logic | Banner XS26 safety controller | $1,927 | never: none of the lab-built machines put safety on a custom board (DTU used an ABB Pluto safety PLC) |
| Thermocouple inputs | P1-04THM (4 ch, 16-bit) | $172 | never; MAX31856 breakouts ($17.50) are non-isolated, which matters with a grounded heater block |
| Heater switching | D1D20 + HS151, two WEG CWBS12 contactors | $383 | never |
| Feedthrough wiring | the feedthroughs' own plugs; SMPW-K type K connectors; M12 L-coded cordsets ($51.72 + $65.36, H1) | – | never |
| Sensor breakouts on the lid | Pi 5 + Adafruit PN532 ($39.95) + SparkFun NAU7802 ($5.95) with Qwiic cables in PB2 | ~$50 | optional: a Pi HAT with the NFC chip, the load-cell ADC, 24 V → 5 V and M12 jacks would be tidier; ~$60-80 at JLCPCB with assembly; not needed |
| Laser and RTC6 connectors | AutomationDirect ZL-RTB-DB15 ($48.50) + ZL-DB15-CBL-2 ($16.50); the IPG side is a 24-pin connector in the 2012 guide, a round 25-pin plug in one manual and a 25-pin D-sub in RAYLASE's diagram: check the U3 before buying a breakout | ~$65 | never |
| Dock | Harting Han-Modular modules | ~$100 | never |

**If the RTC6 is dropped:** DTU's open PBF controller (Teensy 3.6 with XY2-100 drivers, a 10-bit 0-10 V DAC, a 24 V PWM
enable to 100 kHz and three 4-20 mA inputs) is the pattern. A 100 × 80 mm 4-layer board costs $14 for 10 at JLCPCB plus
$25.99 shipping (2-layer $5), or $248 for 6 at OSH Park; JLCPCB's economic assembly adds $9.71 per order plus $0.0016 per joint
(B5, read 05:35-05:52Z). With a Teensy 4.1 (~$30), isolated RS-422 drivers, a DAC and connectors, about **$110-150 per board**.
The board is cheap; laser on/off delay compensation, skywriting and 100 kHz updates are weeks of firmware and test, and OPAL
shows what happens without them.

**What the open and lab-built machines did** (research notes, 2026-11-22): OPAL and Les Wright's OPAL_PCB (Teensy 4.0 +
SN75174N line driver, transmit only, no interlock input); DTU OpenAM (custom Teensy board, safety on a separate ABB Pluto D20
whose contactor "physically break[s]" the laser trigger and motor drivers); NIST AMMT (custom FPGA, XY2-100 and power every
10 µs); MIT (NI cRIO analog outputs); Heriot-Watt (SCAPS USC-2 card); GE M2-Open (SCANLAB RTC5); TUM (RAYLASE with a PLC);
LSU (ScanMaster board + Arduino/GRBL); KU Leuven LMq (NI FPGA with a custom RS-485 scanner board). **None documented its heater
control**, and every one that described safety kept it off the custom electronics.

## 6. Chamber feedthroughs

**Pin count.** The chamber needs very few electrical penetrations, because almost every powered device is outside it:

| Penetration | Pins | Where | Product |
|---|---|---|---|
| **FT1, module rod end** (×3 modules) | 2 power (10.4 A at 24 V on L75) + 3 type K pairs (control, edge, limit) | the rod end below the gland plate; the leads run down the hollow rod, which is open to the chamber gas | **Solid Sealing Technology: 3 × FA11631 (single Chromel lead) + 3 × FA11632 (single Alumel lead), Ø6.27 × 38 mm weld sleeves, −269 to 450 °C, $44 each; 1 × FA10443 (4 × 0.81 mm Cu, 16 A per pin, 2 kV, Ø12.62 × 24 mm sleeve, $92), two pins per pole** = $356 per module |
| FT2, LED bar (if it stays inside) | 2 power | chamber wall | SST FA11643 (2 × 27 A Cu on KF16, $108); better: move the LED bar outside a window (2026-11-25: behind a new low back-wall window, [`optics.md`](optics.md) §9.2) |
| Plate-up through-beam | optical | two M6 fibre heads in the side walls, O-ring under each head | whether the Omron E32-T61-S fibre leaks along its sheath is not known; ask Omron or use a vacuum fibre feedthrough |
| O₂ sample, pressure transducer, Pirani | – | gas and KF ports | the instruments seal on their own ports; the Pirani needs a KF16 port the model doesn't have |

- **Thermocouple-alloy pins**, not copper: a copper pin adds two Chromel-Cu and Alumel-Cu junctions whose difference reads as
  error whenever the two ends of the pin differ in temperature (Edison r5 point 4 agrees).
- **Copper power pins.** Ni-Fe glass-sealed pins (Accu-Glass Sub-C class, 1.02 mm) carry 10.4 A at ~1.4 W per pin in vacuum
  with no convection ([`power.md`](analysis/out/electrical/power.md) §6); two per pole halves the current but still sits above
  their 5 A rating. The FA10443's copper pins (16 A each) at 5.2 A avoid it.
- **No single catalogue part carries 3 type K pairs and power** (combined parts stop at 1 pair at Solid Sealing, 2 pairs at MDC
  on a 2.75 in. CF flange or Accu-Glass on KF50; research notes A2, 06:12Z). Hence separate parts.
- **Plug and flange limits:** Solid Sealing nylon plugs 218 °C, PEEK vacuum plugs 200 °C, SMPW connectors 180 °C, KF O-ring
  mounts 150 °C: all fine at the ~57-70 °C rod end (thermal.md), none usable at the heater block.
- **Alternatives:** two KF16 ports on a rod-end block: SST FA14198 (3 type K pairs on KF16, $309.50) + FA11643 (2 × 27 A Cu on
  KF16, $108), $417.50; or FA23474 (3 pairs, Ø22.1 mm weld flange, $265.50 without plug) + FA10594 (2 × 27 A, Ø18.97 mm sleeve,
  $57.50) on a ~Ø40 block; MDC 9391007 (1 TC pair + 2 × 15 A Cu, 3/4 in. weld sleeve, $212.52) with MDC 9311009 ($207.90; MDC
  parts showed 84-day lead times); Accu-Glass
  100791 (Thermo-D on KF40, $426) or 100801 (2 TC pairs + 2 power on KF50, $463, options-vendors.csv); MPF A0408-2-QF (2 type K
  pairs on KF16, $361.63, seal-parts.csv).
- **Model patch request (modules_low.py):** the compact route needs a rod-end face ~28-30 mm across for six Ø6.27 mm and one
  Ø12.62 mm sleeve (a rough layout, not drawn), in place of today's Ø24 rod end with a Ø12 boss. Check it against the Z arm,
  the pot magnet and the module's swap path.
- **Insulation inside:** the heater stack runs at 200-240 °C, the rod at ≤ 120 °C. Use the cartridges' own leads (fibreglass
  and PTFE on 3714N36), fibreglass-sheathed thermocouples (3871K606, 900 °F cable), and Kapton-insulated silver-plated copper
  hook-up wire (Accu-Glass 100712 class, 250 °C bakeable, 1e-10 Torr) where a joint is needed. No PVC or silicone in the hot
  zone. PTFE outgasses 4.2 × 10⁻⁵ → 1.5 × 10⁻⁶ (Edison's units) between 25 and 100 h after cleaning (Edison r5, warner2022).
  Potting compound in the hollow rod is no longer needed once the rod end is hermetic.

## 7. Wiring

| Run | Length (m, model + 20 %) | Current | Conductor | Drop |
|---|---|---|---|---|
| Dock → PB1 | 2.7 (feeder) | 24 A | 10 AWG | 0.1 % (0.8 m modelled) |
| PB1 → laser, UPS | 0.5-2.4 | 9.1 / 7.4 A | 14 AWG | ≤ 0.3 % |
| PB1 → pump | 2.3 | 7 A | 14 AWG | 0.1 % |
| Heater 24 V, PB1 → rod end (L75) | 1.7 incl. a 0.3 m loop | 10.4 A | **16 AWG** | 2.3 % (4.6 % of heater power); 18 AWG would lose 7.3 % |
| 48 V servo bus | 1.6 | 5 A peak | 18 AWG (Teknic CPM-CABLE-PWR) | 0.8 % |
| 24 V galvo | 1.6 | 2.6 A | 18 AWG | ~1 % |
| 24 V to the guard lock / gas module | 1.6-2.3 | 1-2 A | 22-20 AWG | ≤ 1.5 % |

- **Fusing:** each 24 V branch on its own CBMC E4 channel (1-10 A, set per load); the heater on a 15 A fuse ahead of K1 (sized
  for the supply's 14.6 A and the 16 AWG wire). safety.md asks for a fuse per heater leg (~2 × 2.1 A): with the cartridges'
  leads joined inside the block, one 15 A fuse plus the 16 AWG pair protects the wiring; per-leg fuses would need the legs
  brought out separately through more pins.
- **Signals:** thermocouples in shielded type K extension (TE THMWK-UL-20-1S-F-1, FEP, PLTC, $1.59/ft) with SMPW-K mini
  connectors; 4-20 mA in shielded twisted pairs; shields grounded at the drawer end only, at one star point. Keep thermocouple,
  4-20 mA and XY2-100 cables in a separate duct from the servo and 120/208 V cables (NFPA 79 / IEC 60204-1 separation; Edison
  r5 point 5). Scanner link on SCANLAB's shielded cable, 2-3 m (PC to head is ~1.3 m in the model): the RTC6 speaks SCANLAB's
  SL2-100 natively and needs an optional converter for XY2-100; the basiCube 20 is sold in SL2-100 and XY2-100 versions, so order
  SL2-100 (research notes, from the datasheets). SCANLAB gives no maximum length; RAYLASE recommends ≤ 20 m for XY2-100 and
  ≤ 25 m for SL2-100, far above the ~1.3 m here. The laser's analog input is
  single-ended: short, shielded, and grounded at the laser end.
- **Moving parts:** the Z axis moves the rod end 50 mm (slowly, once per layer) and drops 45 mm at a module swap: a 0.3 m
  service loop in PTFE-jacketed cable, or a short igus micro chain. At a swap the M12 L-coded and SMPW-K plugs at the rod end
  are unplugged (modules.md). The chamber door's actuator and latch cylinders carry only air lines and M8 auto-switch leads,
  fixed to the chamber. The drawer, reservoir and guard door carry no cables: their sensors and the guard lock are fixed and
  see the moving part. The fibre keeps its ≥ 100 mm bend radius (model).
- **Bend radii:** PUR sensor cordsets 10 × OD fixed, 15 × OD moving; chainflex-class cable 7.5-10 × OD in a chain; the 10 AWG
  feeder ≥ 6 × OD.

## 8. Grounding, bonding and the aluminium powder

- **Protective earth:** one PE bar in PB1, bonded to the tray frame and with a strap to each module's base plate (safety.md
  P9). The estimated protective-conductor current is ~8 mA (laser filter ~3.5 mA assumed, UPS, four supplies, pump, PC;
  power.md §7). IEC 60204-1 8.2.8: above 3.5 mA a plug-connected machine needs a warning and reinforced PE, above 10 mA a
  ≥ 10 mm² Cu conductor or a second PE conductor. **Use two PE contacts in the dock and two PE conductors in the feeder.** A
  5 mA GFCI upstream would trip; if the lab requires residual-current protection, it should be a 30 mA type.
- **Bonding for powder:** chamber (bare 6061, no anodize on a ground path: the vacuum SOP's ≤ 0.1 Ω check failed through an
  anodized bore, low-profile.md), lid, door, filter housing, cyclone, reservoir dock, drawer, pump and exchange pail to the PE
  bar. Check each to ≤ 0.1 Ω (the lab's SOP) with a 4-wire milliohm meter; NFPA 77 asks ≤ 10 Ω for all-metal paths (research
  notes B7). ESD wrist-strap point on PB1 and the drawer.
- **Class II, Group E.** (NFPA 484's 2022 edition was its last; it is now part of NFPA 660.) Aluminium is a Group E dust; where it "may be present" in hazardous quantities the location is
  Class II, Division 1, and NEC 502.100(A)(3) bars transformers and capacitors there (research notes B7; Edison r5 §2). So
  the plan is to keep the electronics out of any powder zone, not to rate them for it:
  - inside the chamber there are only the heaters, thermocouples and cutoff (sealed in the module) and, as drawn, the LED bar
    (move it out: [`optics.md`](optics.md) §9.2 puts it behind a low back-wall window). The heaters are off whenever the chamber is
    open to air (PLC permissive);
  - the filter housing gets a thermocouple well only; its service area is where dust in air is expected, so the power box PB1
    sits at the opposite (left) end of the tray, and the gas-module electrics near the filter (valves, pump motor, blower) go
    into the dust hazard analysis (DHA) the Fire Marshal will ask for;
  - cleaning uses the Class II Div 1 Groups E-G vacuum already in A2 (McMaster 5572N116); vendors recommend a wet immersion
    separator for aluminium (Ruwac, Nilfisk).

## 9. Simulations and checks: what changed the design

### 9.1 Heater loop ([`heater_loop.md`](analysis/out/electrical/heater_loop.md))

![Heater loop](analysis/out/electrical/heater_loop.png)

- **The lumped model** (plate + block, and a slow node for the bore wall, head and rod) reproduces the CalculiX heat-up and
  cool-down to 0.3-2.7 K RMS and the laser-heat steady states to ≤ 6 K.
- **PI with a feed-forward and the block cap** heats S25 / M50 / L75 to 200 °C in 2.3 / 3.3 / 4.0 min with no overshoot; the
  S25 block peaks at 224 °C under the 225 °C cap. Gains: Kp 0.08 / 0.15 / 0.15 duty per K, Ti 960 / 60 / 240 s (M50 sits at the
  edge of the grid searched). **The PLC must control on the block reading minus r_B × heater power** (S25 0.5 K/W, M50 0.09,
  L75 0.04): without that correction S25's plate runs 21 K hot once the laser takes over the heating.
- **Dense builds:** with no dwell the 235 °C limit tripped in 3-12 min in every module at the end of the stroke. With a dwell
  at +3 K the plate stays at ~205 °C (band 5-8 K) and the build takes 22 % (S25), 54 % (M50) and 51 % (L75) longer. **The dwell
  is a requirement on the scan software, not an option.** The module fan of heat.md cuts it.
- **SSR fails shorted** (full power from 200 °C): the limit trips after 35-40 s on M50 and 48-51 s on L75, with the plate
  ≤ 227 °C and the seals unchanged. With no protection at all the plate would reach 464-532 °C at the end of the stroke, the rod
  gland 231-250 °C (FKM 200 °C) and the magnet face 102-109 °C. On S25 the block reaches 240 °C in 4-5 s, before the limit
  thermocouple (2 s lag assumed) catches it. **Limit set point 235 °C**; replace the RT240 (holding 205 °C).

### 9.2 Interlock logic: §4.

### 9.3 Power ([`power.md`](analysis/out/electrical/power.md)): legs, inrush, UPS, drawer heat, voltage drop, pins and earth
leakage, all quoted above (§1, §6, §7, §8).

### 9.4 Not simulated

Ground loops and EMI (only the separation and shielding rules above), the RTC6's timing, the laser's own inrush (assumed 40 A),
fault-current coordination beyond §1.3, PL calculation, and the drawer's internal air path (one fan, sized by the energy
balance).

## 10. Electrical BOM

[`electrical-bom.csv`](electrical-bom.csv) lists each part with its price, URL and fetch time, and the bom.csv line it
replaces or adds to ([`bom_summary.md`](analysis/out/electrical/bom_summary.md), [`bom_proposed_rows.csv`](analysis/out/electrical/bom_proposed_rows.csv)).
**94 lines, $11,358.57** (of which $1,177.00 are estimates and $1,570.99 optional). Quotes not included: SCANLAB RTC6, IPG interface cable.

### 10.1 Proposed bom.csv rows (line totals, USD)

| id | change | old low / high | new low / high | delta low |
|---|---|---|---|---|
| C1 | adds the RTC6 laser-connector breakout (ZL-RTB-DB15 + ZL-DB15-CBL-2) | 60.00 / 6,000.00 | 125.00 / 6,065.00 | +65.00 |
| C3 | Teknic ClearCore CLCR-4-13 + DIN-MNT + 2 ClearPath cable sets + SureStep STP-DRV-4830 | 150.00 / 400.00 | 319.00 / 400.00 | +169.00 |
| C4 | Mean Well SDR-240-24 + SDR-240-48 + HDR-100-24 + DDR-30G-5 + Phoenix CBMC E4 (high: Teknic IPC-5 for the servo bus) | 151.10 / 151.10 | 404.71 / 553.33 | +253.61 |
| C5 | AutomationDirect Productivity1000: P1-540 + 2 P1-16ND3 + 4 P1-08TD2 + P1-04THM + P1-08ADL-1 + P1-04ADL-2 + P1-04DAL-2 + terminal blocks (replaces 2 MAX31856 boards) | 35.00 / 35.00 | 1,092.50 / 1,092.50 | +1,057.50 |
| C6 | 4U rack drawer (Middle Atlantic UD class) + PB2 box + 80 mm fan + DIN terminals, rail, duct, ferrules (replaces the 10 x 12 x 6 in enclosure) | 275.10 / 275.10 | 814.90 / 814.90 | +539.80 |
| S1 | Banner XS26-2 + XS16si + XS2so + SC-USB2 + 4 WEG CWBS9-33-30C03 (K3A, K3B, K4, K5) | 275.29 / 275.29 | 2,376.01 / 2,376.01 | +2,100.72 |
| S2 | IDEC HS5L-VC44M-G spring lock + HS9Z-A51 actuator + IDEC HS6B-12B05 guard-position switch (replaces Omron D4JL) | 803.42 / 803.42 | 389.24 / 389.24 | -414.18 |
| S3 | qty 2 -> 4: two more E-stops IDEC XW1E-BV402M-R with enclosures (guard front, gas module); line total shown | 153.34 / 153.34 | 276.58 / 276.58 | +123.24 |
| S4 | adds an amber HOT lamp ECX2053-24L | 367.15 / 467.15 | 373.40 / 473.40 | +6.25 |
| H1 | rod-end weld-in feedthroughs (per module 3 SST FA11631 + 3 FA11632 single type K leads + 1 FA10443 4-pin 16 A Cu), Kapton wire, shielded type K extension, SMPW-K, wall and cake TCs; drops the $50 potting and the $1,389 KF50 high option | 2,241.00 / 4,100.00 | 3,759.94 / 4,279.94 | +1,518.94 |
| H2 | Mean Well LRS-350-24 + Crydom D1D20 + HS151 + 2 WEG CWBS12-33-30C03 (K1, K2) + DwyerOmega CN708 + Omron K8DT-TH1CD | 324.63 / 770.00 | 862.34 / 862.34 | +537.71 |
| A1 | adds 12 Murrelektronik M12 PUR shielded cordsets, 5 m | 1,131.82 / 1,600.00 | 1,527.82 / 1,996.00 | +396.00 |
| A3 | adds a Metal Work 5U11S101 air pressure switch, a NITRA ARV-21 lockable dump valve and two D-M9B switches on the rotary actuator | 969.73 / 1,119.73 | 1,139.43 / 1,289.43 | +169.70 |
| E1 | NEW Power box PB1: Socomec 22013003 UL 98 disconnect + 147E1111 handle + shaft, 6 Eaton FAZ UL 489 MCBs, 3 WEG CWB9-11-30C03 contactors, overload, 16 x 12 x 6 in NEMA 12 enclosure, Fandis FF12D24UN filter fan | 0.00 / 0.00 | 925.00 / 925.00 | +925.00 |
| E2 | NEW AutomationDirect STRIDE SE3-SW8U Ethernet switch | 0.00 / 0.00 | 124.00 / 124.00 | +124.00 |
| E3 | NEW 4 inductive M8 home/over-travel sensors + a +/-5 mbar chamber-at-ambient pressure switch (estimates) | 0.00 / 0.00 | 200.00 / 200.00 | +200.00 |
| E4 | NEW bulk wire, braided bonding straps, ESD wrist strap | 0.00 / 0.00 | 190.16 / 190.16 | +190.16 |
| E5 | NEW, optional: FLIR Extech 380580 milliohm meter, Eaton NETWORK-M3 card, SST FA11643 LED-bar feedthrough | 0.00 / 0.00 | 0.00 / 1,570.99 | +0.00 |

**Net change to the machine BOM: +7,962.45 USD at the low end, +7,728.69 at the high end** (qty 1 per line; S3 and C5 change from qty 2 to a line total).

bom.csv itself is not edited here (another worker owns it): the rows above are the change to make.

## 11. Edison's second opinion (`r5-electrical-review`): where it agrees and where it doesn't

**Agrees and folded in:** the standards list (NFPA 79, UL 508A, NEC 670, IEC 60204-1, ISO 13849-1, ISO 14119, ISO 13850,
21 CFR 1040.10, ANSI Z136.1, NFPA 484, NEC 500/502); a lockable main disconnect, since the dock is not a disconnecting means;
an SCCR marked at the tray (§1.3); a contactor in series with the SSR, owned by the limit and the safety controller; type K
pins; shielded, separated signal wiring with one star point; the laser function as a whole chain to PL d Cat 3 with two
diverse final elements, the RTC6 gate being a convenience; a DHA, bonding and a Group E vacuum; KF hermetic feedthroughs and
PTFE/Kapton inside; a validated safety interface to the UR12e; and DIN-rail modules rather than custom boards.

**Disagrees or adds:**
- **The galvo is not ±15 V.** The basiCube 20 takes one 24 V (or 30 V) rail. Edison's sequencing point still holds and is in
  the PLC permissive.
- **First-pulse suppression** is a Q-switched-laser problem. The IPG YLR is CW with fast modulation (≤ 12 µs on/off, U3 spec
  sheet); the relevant numbers are its rise time and any turn-on overshoot, which IPG should state.
- **The 240 °C TCO is not a good third layer here** (Edison calls the layering good): its 205 °C holding rating is below
  normal block temperatures (§0 point 6).
- **Weld-in feedthroughs, not only KF flanges:** at the rod end a KF16 does not fit (seals.md); weld-in parts do, on a larger
  rod end.
- **Edison did not find** the 3U-drawer depth problem, the drawer heat, the CSI/I2C length limit, the second servo contactor,
  the S25 block-offset correction, or the dense-build trips; those came from the checks here.

## 12. Open items

- **IPG:** the YLR-500-U3 interface connector (the 2012 YLR guide says a 24-pin connector, a third-party manual a round 25-pin
  plug, RAYLASE's wiring diagram a 25-pin D-sub; same pin functions: interlock loops 1-4 and 2-3, analog 12/14, modulation
  15/16, guide 17, emission enable 18) and pinout, interlock voltage and response, gate level, AC inlet, inrush, earth-leakage current,
  rise time and back-reflection rating. The 2012 YLR guide is the closest public document; the U3 may differ (its U2 page lists
  "5 and 24 Volt Control Interfaces").
- **SCANLAB:** RTC6 price and the laser-connector pinout; basiCube 20 power connector and status signal.
- **Done 2026-11-23 (§13.1): vacuum pump changed after this note was written.** The completeness audit moved BOM line G2 to the dry scroll pump the model draws, an Edwards nXDS6i. The single-line diagram, the I/O list and `power_budget.py` still use the McMaster 4396K21 rotary-vane pump (115 V, 7 A). Re-run them with the nXDS6i's nameplate before the breaker and leg sizes are fixed.
- **Model patch requests** (most drawn on 2026-11-23, §13.2; still open: the LED bar, the chamber-at-ambient switch): 4U drawer and 12U rack (both drawn since, in 9297709); PB1 beside the rack; PB2 on the guard frame; rod-end block
  for the weld-in feedthroughs; LED bar outside the chamber; a KF16 Pirani port; recoater and Z home sensors; a guard-position
  sensor separate from the lock; E-stops on the guard front and the gas module.
- **Prices not fetched** (estimates in electrical-bom.csv, marked so): the 4U drawer (3U versions $217.80-286.20), the
  16 × 12 × 6 in enclosure, the PB2 box, the FA23474 plugs, SMPW-K connectors, the overload relay, the M8 home sensors, the
  chamber-at-ambient switch, the P1-04ADL-2, bulk wire and bonding straps; the RTC6 and the IPG interface cable are quotes.
- **Checks still to do:** a real SC26/XS26 program and its response times; PL calculation; the TCO replacement (dropped instead, §13.4); a UR safety
  configuration; the Kardex interface for "tray docked" and "VLM may move"; the DHA.

## 13. 2026-11-23: the electrical parts drawn, the dry scroll pump, the rod-end face and the cutoff

Done in round 5 of [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266). The model's new parts are in
[`cad/electrical_parts.py`](cad/electrical_parts.py) (one hook line at the end of `lpbf_low.build()`), the Pirani tee in
`lpbf_low.py` section 10, and the rod end in `modules_low.py`.

### 13.1 The single-line and the power budget on the Edwards nXDS6i, and one UPS everywhere

**The pump's electrical data** (Edwards nXDS instruction manual A73501880 issue I, Table 8 and 9, an Ideal Vacuum mirror read
22:28Z, and issue B §3.6.1): 100-127 V or 200-240 V ±10 %, single phase, 50/60 Hz, auto-sensing, with an integral controller
driving a three-phase motor; **continuous rating 10 A rms at 100-127 V and 6 A rms at 200-240 V**; supply protection 10 A;
"time-lag fuses should be used, as current transients can exceed the rated values"; an RCD of at least 30 mA "to avoid trip
during start up"; IEC C14 inlet; 26.2 kg. Edwards' catalogue page gives 260 W at ultimate and 170 W in standby (search
snippet; the page itself returned 403). Inrush and power factor are not published: 40 A for 10 ms (the drive's DC-bus
capacitors) and 0.6 are assumed.

What changed:
- **The pump runs at 208 V across L1-L2** (6 A), as the laser does, instead of 120 V on L2 (10 A): Q3 becomes a **2-pole 10 A
  D-curve** breaker (Eaton FAZ-D10-2-NA, priced as its 15 A sibling), the time-lag type Edwards asks for. The 7 A motor overload
  relay goes: the pump's own controller protects its motor. The cord is an IEC C13 to KM1 in PB1.
- **Legs** ([`power.md`](analysis/out/electrical/power.md) §1): purge 9.5 / 9.8 A (L1 / L2), building worst 17.7 / 14.0 A,
  everything at rated at once 23.7 / 20.0 A (was 20.7 A on L2 with the rotary vane): all inside 24 A. The pump still never
  runs while the laser fires.
- **Inrush:** 40 A against Q3's lowest magnetic trip of 100 A, 2.5× (§2 of power.md). It is not switched by Q0 (KM1 is open
  at power-up), so the 120 A at Q0 closing does not change.
- **Not on the UPS.** It could run from the 5PX's sine-wave output at ultimate (260 W), but its 6-10 A rating at full inlet
  flow would take most of the UPS, and during a power cut it has no job: the argon valves close and the build stops. Its
  factory default is to stay off when power returns (manual §5.5), which is what an unattended restart wants; **set Auto-run on
  (hold START for 8 s, or over serial) or the pump will not start when KM1 closes**, or wire the PLC to the pump's own start
  input instead.
- **Earth leakage:** the pump's inverter drive is now counted at 2.0 mA (estimate), so the total is ~9.3 mA (power.md §7): still
  under 10 mA, and the two PE contacts in the dock stay.

**The UPS is now one model everywhere.** The model's 2U unit, bom.csv D2, power_budget.py and electrical.md were already the
Eaton 5PX1500RTG2; **[`tray_budget.py`](analysis/tray/tray_budget.py) still used byu-vcl PR 318's Vertiv GXT5LI-1500** and is
changed. ENERGY STAR's UPS listing of the 5PX1500RTG2 (data.energystar.gov dataset ifxy-2uty, read 22:48Z): 1,500 VA /
1,500 W line-interactive, **98.6 % efficient at 50 and 75 % load, 98.4 % at 100 %, battery runtime 14 min at 50 % and 7 min
at 100 %** (VRLA). The Peukert model in power_budget.py gives 7.9 and 17.5 min at those loads, 13-25 % optimistic; for the
63 W held through a power cut it gives ~5 h, and even with no low-rate gain at all (the ~175 Wh ENERGY STAR's two points imply)
the held load lasts **167 min**, against 41 min for the L75 plate to cool to 50 °C. The tray budget's backed branch is 684 W
rated against 1,500 W. Both budgets also now carry the galvo on its real 24 V rail (≤ 2.6 A through the HDR-100-24, 69 W), not
±15 V.

Re-run: [`power.md`](analysis/out/electrical/power.md), [`tray_budget.md`](analysis/out/tray/tray_budget.md),
[`single_line.png`](analysis/out/electrical/single_line.png) and the other two drawings (only the labels changed).

### 13.2 Parts drawn in the model

| Part | Real part | Where (model mm) | Mount |
|---|---|---|---|
| PB1 power box | 16 × 12 × 6 in steel NEMA 12 (McMaster 7812K class, E1-10 estimate); Socomec 147E1111 handle on its 150 mm shaft; Fandis FF12D24UN fan and grille on the door | x −1160 to −1008 (16 mm left of the rack's side panel), y −300 to 5, on two 15 mm rails on the tray: where `cad/electrical.py` checked it | rails bolted to the tray (tray holes not drawn) |
| PB2 process-module box | Hammond 1554JGY, 160 × 90 × 60.5 mm polycarbonate, IP66 | on the optics bridge behind the galvo, x −40 to 120, y 75 to 165: **0.19-0.22 m in a straight line** from the layer camera, the NFC antenna and the load cell, so the CSI ribbon and the I2C cables stay under 0.5 m | 4 × M4 × 10 (McMaster 92290A144) through two tabs into tapped holes cut in the optics bridge (joints.py helpers) |
| Z home (top) and lower limit | 2 × AutomationDirect KSE-AP-3F, M8 PNP NO, 3 mm flush ($33.50) | bracket on the actuator body's −x side; a 2 mm steel flag on the carriage, 1 mm from the sensor faces | the home sensor sees the flag at the +8 mm overtravel; **the lower one is 14 mm below the flag's swap-release position, so the 45 mm release does not trip it** (electrical-io.csv M-06) |
| Recoater home and far over-travel | 2 × Turck BIM-M12E-AP4X-H1141 magnetic-field sensors (59 mm range with Turck's DMR20-10-4 magnet, 90 mm with the DMR31-15-5; datasheet read 22:48Z) | **outside the chamber's back wall**, at the park position and 10 mm past the end of spread, on two 20 mm T-slot posts bolted to the process base plate (M5 × 25, holes cut through the plate) | they see a magnet bonded into the carriage block's back face through the 16 mm 6061 wall and the 0.5 mm 316L liner, 18 mm in all: no chamber port and no hole in the frame (its machining is frozen). The drawn Ø12 × 3 magnet is a stand-in; test the switching distance through the wall |
| Guard-position switch | IDEC HS6B-12B05 (2NC + 1NO), separate from the lock (ISO 14119) | on the door rail at x 181-200, z 176-240: between the lock above it and the door handle, which reaches x 197-209 below z 170 with the door open | envelope; tongue on the door not drawn |
| Two more E-stops | IDEC XW1E-BV402M-R in 1-hole yellow enclosures (70 mm class, estimate) | guard right side near its front corner (x 312-382, y −250 to −180); front of the gas module's O₂ box (x 870-940, y −310 to −240) | rivnuts in the guard panel; the O₂ box's face |
| Pirani gauge | Vacuum Research 902377 (NW-16, 1-2000 mTorr, 0-10 V and 4-20 mA, 12-35 V DC < 100 mA, RJ-45; $455.00, read 22:46Z) on a McMaster 4518K21 KF-25 tee and a 4518K521 KF-25 to KF-16 reducer, two 4518K72 clamps | **at the vacuum port, on the isolation valve's pump-side flange**, the tee's run through the guard's right panel where the vacuum hose passed, the gauge up at x 336; the vacuum hose now starts at the tee | KF clamps; the tee's ends use the real ISO-KF flange profile. The tee's 38.1 mm centre-to-face is assumed (McMaster's drawing did not render) |
| Dock PE contacts | two leading PE contacts on the dock's face (HARTING Han PE module 09 14 001 3071 if the dock is Han-Modular; D1 carries PR 318's CombiTac) | dock face, y 346-394, z −101 to −93 | in the dock's face plate |

**The Pirani sits on the pump side of the valve, not the chamber side.** With the valve open, as in every purge, it reads the
chamber through 0.1 m of KF-25, which is the purge check it is for. A leak-up test with the valve shut would need it on the
chamber side; a tee there pushes the 124 mm valve 76 mm or more through the guard's right panel (the guard was sized for the
valve). The chamber-side option stays open for whoever next moves the valve.

**The LED feedthrough is not drawn.** No chamber port may be added this round, and the only opening the LED bar's two leads could
share is the vacuum port, on the chamber side of the isolation valve, which has the same problem: a KF-25 cross there moves the
valve through the guard. **Move the LED bar outside**, behind the camera viewport or a window (electrical.md §0 point 9 already
preferred that); the FA11643 KF16 feedthrough stays an optional line (E5). **2026-11-25 ([`optics.md`](optics.md) §9.2):** the
camera viewport doesn't work: its Ø20 aperture only passes light along the camera's own axis, which needs a beamsplitter and
shows no shadows. The recommendation is a new window low in the back wall, left of the inlet plenum.

Checks of these parts: see §13.5.

### 13.3 The rod end: an 81 × 16 mm feedthrough face (72 mm until round 6)

The rod end is now a 316L block with the rod TIG-welded into its top and **seven weld-in feedthroughs welded at its front (−y)
face**: Solid Sealing Technology 3 × FA11631 (Chromel) + 3 × FA11632 (Alumel) single-lead type K, Ø6.27 × 38 mm sleeves, and one
FA10443 4-pin 16 A copper weld-in, Ø12.62 × 24 mm (2 pins per heater pole). The gas boundary at the rod end is now metal,
glass/ceramic and welds, with no O-ring; the LEMO 1B envelope, its O-ring and its gland entry are gone.

**The face is 72 × 16 mm in one row, not the ~30 mm square this note asked for, because the rod end cannot grow in height or
reach.** Above: at the +8 mm plate-exchange overtravel the cap is 2.5 mm under the gland plate, and in front of the rod the
handle's two M4 screw heads hang 8 mm below it (joints.py; at y −13, −26 and −38 on S25, M50 and L75), so in front of the cap the
block stops at zc + 17 (zc: the striker's underside), 2 mm under those heads. Below: the Z arm, and on the module's way out
(MODULE_PATH) the striker clears the guard's bottom rail by 3 mm. Forward: on the way out the module rises at y −190, just behind
that rail, so nothing may stand more than ~50 mm in front of the rod. A first layout (48 × 20 mm, two rows of three type K
sleeves standing 35 mm proud) failed both of the last two in the S25 sweep: 120 mm³ into the handle screws at the overtravel and
320 mm³ into the rail on the way out. So:
- the power sleeve sits in the middle of the face at zc + 9, 21 mm proud, over a small pocket and a channel into the rod bore;
- the six type K sleeves sit in one row at zc + 10.5, x = ±11.85, ±26.16 and ±34.83 (±12.5, ±21.5, ±30.5 on a 72 mm block until
  round 6; see the note below), **26 mm deep in blind bores** with their welds at the face and 12 mm proud; one Ø4 cross-drilling at y +2 joins the bores' ends to the rod bore (its two ends welded shut);
- 2.4-3.1 mm between sleeves and to the face's edges, ≥ 1.9 mm of wall over the striker's pocket.

**Check with Solid Sealing that the single-lead parts can be welded at the face of a blind bore, and the weld access, before
machining the block.** Everything stays inside the base plate's slot (x ±56), so it passes at the bottom of the stroke and on the
way out; the plugs (SMPW-K, M12) come off at a module swap.

**Round 6 (2026-11-25): the block is 81 mm wide.** The round-5 block stopped a torque screwdriver reaching 3 of the gland
plate's 6 M4 screws (hand operations A1.20 and M7.1). The gland plate's screws now sit on the arc behind the block, and the
type K sleeves spread to x ±11.85, ±26.16 and ±34.83, which leaves an 8 mm gap under the handle's two M4 screws for a straight
driver. A1.20 and M7.1 pass 6 of 6 on S25, M50 and L75 ([`assembly.md`](assembly.md), [`operations.md`](operations.md)).

### 13.4 The thermal cutoff: dropped

The RT240's 205 °C holding temperature is below S25's 216-221 °C running block and the 225 °C block cap. A replacement needs a
holding temperature ≥ 225 °C **and** a 24 V DC rating for 4.2 / 6.2 / 10.4 A. The best found (research notes, 22:31-22:49Z):

| Cutoff | Tf / Th (°C) | DC rating | Verdict |
|---|---|---|---|
| Cantherm RT240 (the old part) | 240 / 205 | – | holds below the running block |
| Therm-O-Disc Microtemp G4, 257 °C | 257 / 220 | 5 A at 24 V DC | 5 K short on holding, and too small for M50 and L75 |
| Cantherm SDF DF280S | 280 / 230 | AC ratings only (250 V 10 A); UL, VDE, CCC "applied for" | holds, but no DC rating and no listing |
| ATC Semitec PEPI H-8 (bimetal one-shot, 250-280 °C) | – | 10 A at 250 V AC (2013 news item) | may not be made any more |

**So it is dropped** ([`heater_loop.md`](analysis/out/electrical/heater_loop.md) §4-5, re-run): with an SSR failing shorted,
the latching limit (CN708 on its own thermocouple, K2) trips after **6 s on S25 with the plate at 209-211 °C** (the block peaks
at 245 °C), **35-40 s on M50 (plate 223-224 °C) and 48-51 s on L75 (plate 227 °C)**, the seals unchanged. The PLC's
over-temperature on the control and edge thermocouples (K1 through the safety controller, the diverse input the interlock check
added in §4) reads thermocouples in the same block with the same lag, so it is a second channel with the same numbers; the
interlock check's 49 single faults already include the CN708 failing. The cases with both channels failed show what each
cutoff would have added: the RT240 opens first on S25 in normal fault handling (4-5 s, the nuisance a one-shot part makes); a
257 °C part opens after 10 s on S25 (plate 216-217 °C) and 68-96 s on M50/L75 (plate 244-248 °C); a 280 °C part after
20-152 s with the plate at 232-271 °C. The model has no cutoff part or pocket now (its place, kept in `block_layout()` as
`tco`, is free); bom.csv H1 drops the six RT240s ($6.36). `module_params.TCO_A` (240 °C), which thermal_module.py still
reports blocks against, is not changed here.

### 13.5 Checks

- **Interference.** The full sweep (`interference.py`) ran once, for S25, on the first rod-end layout: besides the two rod-end
  hits of §13.3 it found the re-routed vacuum hose clipping the pump by 0.57 mm³, fixed by keeping the hose's old via-point at
  (400, 70, 60). All three are fixed; **the full sweeps of the final geometry (M50, S25, L75) did not run before the deadline**: the
  shared heavy-job queue held them for 15-20 min each and the M50 run was stopped by its time limit before writing its report. The
  committed `interference.md` and `variants/` reports are therefore still the 2026-11-22 ones. What was checked on the final
  geometry instead, with exact OpenCascade booleans (a script under /tmp, not committed): every part this round added or changed
  (PB1 and its handle, fan and stand, PB2 and its screws, the Z and recoater sensors, flag, magnet, posts and clamps, the
  guard-position switch, the E-stops, the Pirani tee, reducer, gauge and clamps, the dock PE contacts, the rod end and its
  feedthroughs) against every other part, in 22 states (piston at both ends, Z released, recoater at both ends and mid-way, guard
  door open and half-way, chamber door open, 12 points along the module's swap path): **no interference in M50, S25 or L75**
  without fasteners on the first rod-end layout; the final rod end and the re-routed vacuum hose, with all fasteners, against every part in the same 22 states (the swap path sampled at 12 points including the rise at y −190): **no interference in S25 or M50** (L75 not re-run: its handle screws sit at y −38, in front of the sleeves, and 5 mm above them at the overtravel). The contacts found are designed ones, now listed in `interference.py`'s
  JOINTS: the magnet in the carriage block, the tee on the valve and the hose, the tee through the guard panel where the hose went
  (as the hose did), sensors in their clamps, and so on.
- **I/O list** ([`io_check.md`](analysis/out/electrical/io_check.md)): 95 devices and signals; **30 not drawn (was 37)**, 16 with
  no bom.csv line (was 20). Channel counts are unchanged. **interlock_logic.py was not re-run:** no input changed (the cutoff
  was never one of its inputs; the guard-position switch and the E-stops were already).
- **Electrical BOM** ([`electrical-bom.csv`](electrical-bom.csv), [`bom_summary.md`](analysis/out/electrical/bom_summary.md)):
  102 lines, **$11,845.92** ($1,610.01 estimates, $1,570.99 optional). bom.csv rows changed: **E1 $925.00 → $914.00** (Q3 2P D10,
  no overload relay), **E3 $200.00 → $517.00** (real sensors and mounts), **C6 $814.90 → $794.90** (PB2 a Hammond 1554JGY),
  **H1 −$6.36** (no cutoffs), **G7 +$201.35** (the Pirani tee, reducer and clamps): **+$480.99** on the machine. bom_build.py's
  "proposed rows" table now compares against a bom.csv that already has the 2026-11-22 changes, so its C1, S3, S4, A1, A3 and
  H1-high deltas count those twice; only the five rows above were changed in bom.csv.
- **Mass** ([`mass.md`](analysis/out/mass.md), re-run): **288.9 kg on the tray (was 268.8)**, against 490 kg (Kardex) and 500 kg (Modula): PB1 and its stand add 17.2 kg to the tray, the process module 2.7 kg (90.7 kg; tip-over margin 0.68 g, was 0.69), the gas module 0.2 kg.

Not done: cable routes; a test of the magnetic sensors through the back wall; the tee's and the E-stop enclosures' catalogue
drawings (envelopes from nominal sizes); McMaster prices for the tee and reducer (estimates from other vendors); the PB1 tray
holes.
