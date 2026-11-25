"""Writes desktop-lpbf/electrical-io.csv (every powered or sensing device, its signal, controller channel, connector, cable and
feedthrough) and checks the channel counts against the controllers chosen in electrical.md §3.

Model check: each row says whether cad/lpbf_low.py / modules_low.py / automation.py draw the device (the part name is given)
and which bom.csv line carries it; rows with model = "no" or bom = "none" are the devices the model or the BOM lacks.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/electrical/io_list.py -> desktop-lpbf/electrical-io.csv,
     desktop-lpbf/analysis/out/electrical/io_check.md
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "out" / "electrical"

H = ["id", "device", "where (model part, module)", "in model", "bom line", "signal type", "voltage / current", "controller",
     "channel", "connector", "cable", "chamber feedthrough", "notes"]

# controller channel naming: PLC slot.point (Productivity1000: s1/s2 P1-16ND3, s3/s4 P1-16TD2, s5 P1-04THM, s6 P1-08ADL-1,
# s7 P1-04ADL-2, s8 P1-04DAL-2); XS = Banner XS26-2 IN1-IN26 + XS16si IN27-IN42, outputs O1-O4 (+ XS2so O5-O6);
# CC = Teknic ClearCore (M-0..M-3, IO-0..IO-5, DI-6..DI-8, A-9..A-12); RTC = SCANLAB RTC6; PI = Raspberry Pi 5 in PB2.
R = [
    # ---------------- laser and optics
    ["L-01", "Fibre laser IPG YLR-500-U3-SM-AC: AC input", "Fiber laser source (rack, 4U)", "yes", "L1", "AC power", "208 V L1-L2, 9.1 A max (1.9 kVA)", "PB1 Q1 + KM0", "Q1 2P D15", "rear 3-pin screw terminal L1/L2/PE (2012 YLR guide; U3 not confirmed)", "14 AWG 3c + PE, 0.5 m", "-", "KM0 lets the PLC stagger power-up and switch the laser off between builds (150 W of idle heat in the Shuttle)"],
    ["L-02", "Laser interlock channel 1", "laser interface connector", "yes", "L1", "dry-contact loop (laser-side source)", "24 V, > 1 A contacts (2012 guide)", "XS O1 -> K4", "K4 NO", "IPG 24-pin circular interface plug (2012 YLR guide); U3 pinout still owed by IPG", "shielded 18 AWG, 1 m", "-", "two-channel interlock, Cat 3 PL d per the 2012 guide, 500 ms response"],
    ["L-03", "Laser interlock channel 2", "laser interface connector", "yes", "L1", "dry-contact loop", "24 V", "XS O2 -> K5", "K5 NO", "IPG interface plug", "shielded, same cable", "-", ""],
    ["L-04", "Laser modulation / gate", "laser interface connector", "yes", "L1", "digital, 'CMOS to 24 VDC', ~11 mA", "5-24 V", "RTC6", "LASERON (laser connector, 15-pin D-sub)", "RTC6 D-sub 15 -> ZL-RTB-DB15 -> IPG plug (24-pin, round 25-pin or D-sub 25: sources differ)", "shielded twisted pair, 1.5 m", "-", "<= 100 kHz (U3 spec sheet); level to be matched to the U3 input"],
    ["L-05", "Laser analog power set point", "laser interface connector", "yes", "L1", "analog 0-10 V (1-10 V active in the 2012 guide)", "0-10 V", "RTC6", "ANALOG OUT1", "RTC6 D-sub 15 breakout", "shielded twisted pair, 1.5 m", "-", "single-ended: keep it short, one shield end, separate from servo cables (Edison r5)"],
    ["L-06", "Laser emission enable / guide laser", "laser interface connector", "yes", "L1", "digital in (laser)", "24 V", "PLC", "s3.1 (EE), s3.2 (guide)", "IPG plug", "shielded multi-core", "-", "standard functions, through K4/K5 for EE"],
    ["L-07", "Laser status: Ready, Emission ON, Error", "laser interface connector", "yes", "L1", "digital out (laser)", "24 V", "XS + PLC", "XS IN33-34 (Ready, Emission); PLC s1.1-1.3", "IPG plug", "shielded multi-core", "-", "read back so a laser that ignores its loop is caught (interlock_logic.py)"],
    ["L-08", "Laser Ethernet / RS-232 (monitoring, power read-back)", "laser rear panel", "yes", "L1", "Ethernet", "-", "PI / PC", "switch port", "RJ45", "Cat6 S/FTP", "-", ""],
    ["L-09", "QBH fibre-present / head interlock", "collimator on V-mount", "yes", "L1/L3", "laser-internal loop", "-", "laser", "-", "QBH connector", "-", "-", "IPG's own QBH interlock (confirm on the U3); stops emission if the fibre is pulled (safety.md 4.2)"],
    ["L-10", "Safety shutter coil (power to open, spring closed)", "Safety shutter + beam dump (process)", "yes", "L4", "24 V coil through K4 + K5 NO", "24 V, ~0.5-1 A pull-in (estimate)", "PLC request through K4+K5", "s3.3", "M12 A-coded 4-pin", "PUR 4x0.34 mm2, 1.6 m", "-", "no product chosen in L4: pick one with two position switches"],
    ["L-11", "Shutter closed switch A", "shutter", "no (no product)", "L4", "dry contact", "24 V test-pulsed", "XS", "IN23", "M12 (with L-12)", "PUR 4 x 0.34", "-", ""],
    ["L-12", "Shutter closed switch B", "shutter", "no (no product)", "L4", "dry contact", "24 V test-pulsed", "XS", "IN24", "M12", "PUR", "-", ""],
    ["L-13", "Galvo SCANLAB basiCube 20: power", "2-axis galvo scan head (process)", "yes", "L5", "DC power", "24 V single rail, <= 2.6 A (A1: basiCube series data, 24 V or 30 V variants)", "PB1 HDR-100-24", "-", "basiCube power connector", "2 x 18 AWG, 1.6 m", "-", "not +/-15 V (tray_budget.py and Edison r5 both assumed +/-15 V)"],
    ["L-14", "Galvo scanner link (SL2-100 with the RTC6; XY2-100 only through SCANLAB's converter)", "galvo", "yes", "L5/C1", "RS-422 differential", "-", "RTC6", "scan-head connector (9-pin D-sub on the RTC6)", "SCANLAB cable", "SCANLAB cable, 2-3 m, shielded twisted pairs", "-", "order the basiCube 20 in its SL2-100 version; keep away from servo power"],
    ["L-15", "Galvo status / ready", "galvo", "yes", "L5", "via XY2-100 status channel", "-", "RTC6 -> PLC", "RTC6 digital in", "-", "-", "-", "Edison r5: galvo powered and in position control before emission is permitted (PLC permissive)"],
    ["L-16", "Melt-pool photodiode Thorlabs PDA36A2", "not drawn", "no", "T2", "analog 0-10 V, 12 MHz bw", "+/-12 V supply (Thorlabs)", "RTC6 analog in / DAQ", "-", "BNC", "RG-58, 2 m", "-", "commissioning; coaxial port in the galvo not chosen"],
    # ---------------- motion
    ["M-01", "Recoater servo Teknic ClearPath-SD CPM-SDSK-2311S", "Recoater servo (process)", "yes", "M2", "DC power + step/dir/enable + HLFB", "48 V bus, 5 A peak (estimate)", "CC M-0", "M-0", "Molex Mini-Fit 8-pin (control), 4-pin (power)", "CPM-CABLE-CTRL-MU120 + CPM-CABLE-PWR-MS120 (3 m)", "-", "bus through K3A + K3B"],
    ["M-02", "Z servo ClearPath-SD (folded, belt 2:1)", "Z servo (process, under the floor)", "yes", "M2", "as M-01", "48 V", "CC M-1", "M-1", "Mini-Fit", "as M-01, plus 0.3 m loop for the 45 mm drop at a swap", "-", ""],
    ["M-03", "Dosing stepper McMaster 6627T91 (NEMA 17)", "Dosing stepper (lid)", "yes", "M4", "bipolar stepper", "24 V drive, ~1.7 A/phase (not read)", "SureStep STP-DRV-4035 <- CC M-2", "M-2 (step/dir/enable)", "4-pin M8 or flying leads", "shielded 4 x 20 AWG, 1.5 m", "-", ""],
    ["M-04", "Recoater home sensor (Turck BIM-M12E-AP4X-H1141 magnetic-field sensor, PNP NO)", "Recoater home and over-travel sensors (outside the back wall, on a post)", "yes", "E3", "PNP", "10-65 V (24 V), 10 mA", "CC", "IO-1", "M12 4-pin", "PUR 4 x 0.34", "- (sees the carriage's magnet through the 16 mm 6061 back wall)", "magnet on the carriage block's back face; 18 mm through aluminium and the 0.5 mm 316L liner, inside the sensor's 59-90 mm range with Turck's magnets (the drawn Ø12 x 3 disc is weaker: test)"],
    ["M-05", "Recoater far over-travel sensor (Turck BIM-M12E-AP4X-H1141)", "Recoater home and over-travel sensors (outside the back wall, on a post)", "yes", "E3", "PNP", "10-65 V (24 V)", "CC", "IO-2", "M12 4-pin", "PUR", "-", "10 mm past the end of spread (x_end + 10)"],
    ["M-06", "Z home (top) and lower limit: 2 x AutomationDirect KSE-AP-3F inductive M8, PNP NO, 3 mm flush", "Z home and lower-limit sensors (bracket on the Z actuator, flag on the carriage)", "yes", "E3", "PNP", "10-30 V (24 V)", "CC", "IO-3, IO-4", "M8 3-pin", "PUR", "-", "home at the +8 mm overtravel; the lower limit sits 14 mm below the flag's swap-release position, so the 45 mm release does not trip it"],
    ["M-07", "Door rotary actuator SMC CRQ2 size 20, open/close valve", "Door drive (process)", "yes", "A3", "5/2 solenoid valve", "24 V, 0.5 W", "PLC", "s3.4", "valve manifold DIN connector", "manifold multi-pin cable", "-", "plus two auto switches on the actuator"],
    ["M-08", "Door open / closed auto switches (D-M9B class)", "door actuator", "no", "none (A3 has the actuator only)", "PNP 2-wire / 3-wire", "24 V", "PLC", "s1.4, s1.5", "M8 3-pin", "PUR", "-", ""],
    ["M-09", "Draw-latch cylinders 2 x SMC CJ2/CQ2 20 mm, valve", "Draw-latch actuators (process)", "yes", "A3", "5/2 solenoid valve", "24 V, 0.5 W", "PLC", "s3.5", "manifold", "manifold cable", "-", "both cylinders on one valve"],
    ["M-10", "Latch-closed switches (on A3's CDQ2B20-15DZ-F7PS cylinders)", "draw latches", "no", "A3", "PNP 3-wire", "24 V", "PLC", "s1.6, s1.7", "M8", "PUR", "-", ""],
    ["M-11", "Plate drawbar release cylinder SMC CDQ2B40-10DCMZ, valve", "not drawn (hot-swap.md patch)", "no", "none", "5/2 solenoid valve", "24 V", "PLC", "s3.6", "manifold", "manifold cable", "-", "only if the drawbar plate is built"],
    ["M-12", "Drawbar released switch", "not drawn", "no", "none", "PNP", "24 V", "PLC", "s1.8", "M8", "PUR", "-", ""],
    ["M-13", "Air supply pressure switch (dock air)", "not drawn", "no", "none", "PNP", "24 V", "PLC", "s1.9", "M12", "PUR", "-", "no air -> no door/latch moves"],
    ["M-14", "Air dump / soft-start valve (LOTO of air)", "not drawn", "no", "none", "3/2 solenoid", "24 V", "PLC (through K3A aux)", "s3.7", "DIN", "-", "-", ""],
    ["M-15", "Zero-point release valve SMC VT307-5DZ1-01N (3/2 NC poppet, 24 V DC): air on opens both SCHUNK NSE-HT mini modules", "Zero-point release valve (under the floor, process)", "yes", "B4", "3/2 solenoid valve", "24 V DC", "PLC, permissive: plate < 50 C, chamber vented, Z arm holding the module", "s4.5", "valve DIN connector", "PUR 2c 0.5 mm2, ~1.5 m", "-", "round 6 (hot-swap.md 3.2a): air or power off leaves the module clamped (spring-locked); release on a robot-job or HMI request only, never during a build"],
    # ---------------- heated module
    ["H-01", "Cartridge heaters 2/3/5 x 50 W 24 V (McMaster 3714N36)", "Cartridge heaters M50 (module)", "yes", "H1", "DC power", "24 V, 4.2 / 6.3 / 10.4 A", "SSR D1D20 <- PLC s4.1 (1 s time-proportioning)", "s4.1", "rod end -> M12 L-coded 5-pin (Molex 1205020022 / 1205000300)", "16 AWG pair + PE, 1.7 m incl. 0.3 m service loop", "FT1 rod end: SST FA10443 4-pin 16 A Cu weld-in, 2 pins per pole", "PTFE/fibreglass leads inside the rod; no thermal cutoff (dropped 2026-11-23, heater_loop.md 5)"],
    ["H-02", "Thermocouple, control (type K, ungrounded)", "Type K thermocouples M50", "yes", "H1", "type K", "uV", "PLC", "s5.1 (P1-04THM)", "rod end -> SMPW-K (type K mini)", "type K extension, shielded twisted, 2 m", "FT1: SST FA11631 + FA11632 single Chromel / Alumel weld-ins", ""],
    ["H-03", "Thermocouple, edge (type K)", "Type K thermocouples M50", "yes", "H1", "type K", "uV", "PLC", "s5.2", "SMPW-K", "type K extension", "FT1: FA11631 + FA11632 (pair 2)", "PLC cross-checks control vs edge (> 15 K = fault)"],
    ["H-04", "Thermocouple, limit (type K)", "Type K thermocouples M50", "yes", "H1", "type K", "uV", "CN708 (latching) + K8DT (plate < 50 C)", "CN708 input; K8DT in parallel is NOT allowed: K8DT on the edge TC instead", "SMPW-K", "type K extension", "FT1: FA11631 + FA11632 (pair 3)", "the limit TC feeds only the CN708 (independence)"],
    ["H-05", "Thermal cutoff: dropped (was Cantherm RT240, 240 C)", "removed from the model 2026-11-23", "no (removed)", "H1 (removed)", "-", "-", "-", "-", "-", "-", "-", "no one-shot cutoff holds 225 C with a 24 V DC rating for 10.4 A (heater_loop.md 5); the CN708 limit (K2) and the PLC's over-temperature (K1) each stop an SSR short with the plate <= 227 C"],
    ["H-06", "Heater 24 V supply Mean Well LRS-350-24", "not drawn (in the 3U drawer envelope)", "no", "H2", "AC in / DC out", "120 V L2-N in; 24 V 14.6 A out", "PB1 Q2", "-", "screw terminals", "14 AWG in, 14 AWG out", "-", "unbacked"],
    ["H-07", "Heater SSR Crydom D1D20 (+ HS151 heat sink)", "not drawn", "no", "H2", "DC SSR", "3.5-32 V control; 20 A 100 V load", "PLC", "s4.1", "screw", "-", "-", "D1D12 (12 A) in H2 replaced by D1D20: 10.4 A on a 12 A part"],
    ["H-08", "K1 heater safety contactor (WEG CWBS12-33-30C03, mirror contacts, 24 VDC)", "not drawn", "no", "none", "contactor", "24 V coil; 12 A AC-3, poles in series on DC", "XS O5 (XS2so)", "O5; EDM -> IN35", "screw", "-", "-", ""],
    ["H-09", "K2 limit contactor (WEG CWBS12-33-30C03) driven by the CN708 relay", "not drawn", "no", "none", "contactor", "24 V coil", "CN708 relay (hard-wired)", "aux -> XS IN30, PLC s1.10", "screw", "-", "-", "the CN708's 15 A relay drives K2's coil, not the heater current"],
    ["H-10", "Limit controller DwyerOmega CN708 (latching, manual reset)", "not drawn", "no", "H2", "TC in, relay out", "24 V supply", "-", "-", "panel cutout 71 x 29 (PB1 door)", "-", "-", "set 235 C (heater_loop.md)"],
    ["H-11", "Plate < 50 C relay Omron K8DT-TH1CD on the edge TC (2nd channel for the door)", "not drawn", "no", "none", "TC in, SPDT relay", "24 V", "XS", "IN17 (ch A); PLC s1.11 / ch B from PLC output s4.2", "DIN", "type K ext.", "-", "replaces the 67F bimetal idea in modules.md"],
    ["H-12", "Module fan under the chamber floor (24 V, tach)", "not drawn (heat.md recommends)", "no", "H3", "DC fan + tach", "24 V, ~0.1-0.3 A", "PLC", "s4.3 (on), s1.12 (tach alarm)", "M8 / leads", "PUR 3c", "-", "heat.md: fixes the magnet and rod gland temperatures"],
    ["H-13", "Module present (inductive M12 PNP, PAM-AP-1H)", "Module-present sensor (under the floor)", "yes", "A1", "PNP", "24 V", "PLC", "s1.13", "M12 A 4-pin", "PUR 2 m", "-", "in the PLC permissive (beam must not fall through an empty port)"],
    # ---------------- chamber, lid, powder
    ["P-01", "Plate-up fibre through-beam Omron E32-T61-S + E3NX-FA41", "Plate-height through-beam (side walls)", "yes", "A1", "PNP from the amplifier", "24 V", "PLC", "s1.14", "amplifier in PB2", "glass fibres 2 m", "optical, through M6 heads with O-rings: leak along the fibre not checked", ""],
    ["P-02", "Overflow jar present (PAM-AP-1H)", "Overflow-jar present sensor", "yes", "A1", "PNP", "24 V", "PLC", "s1.15", "M12", "PUR", "-", ""],
    ["P-03", "Cover-slide drawer closed (PAM-AP-1H)", "Drawer-closed sensor (lid front)", "yes", "A1", "PNP", "24 V", "PLC", "s1.16", "M12", "PUR", "-", "in the PLC permissive: no lasing without the slide"],
    ["P-04", "Reservoir docked (PAM-AP-1H)", "Reservoir-docked sensor", "yes", "A1", "PNP", "24 V", "PLC", "s2.1", "M12", "PUR", "-", ""],
    ["P-05", "NFC reader PN532 (Adafruit 364) + antenna in the dock face", "NFC reader antenna (lid)", "yes", "A1", "I2C/SPI", "3.3-5 V", "PI", "I2C1", "JST / Qwiic", "< 0.5 m (I2C): the board sits in PB2 on the guard frame", "-", "cannot run from the rack: I2C/SPI over 1.5 m is unreliable"],
    ["P-06", "Load cell Laumas ALLUE3 + NAU7802 (SparkFun SEN-15242)", "Load cell (lid)", "yes", "A1", "bridge mV/V -> I2C", "5 V excitation", "PI", "I2C1 (0x2A)", "4-wire shielded 0.5 m (integral)", "< 0.5 m to PB2", "-", ""],
    ["P-07", "Layer camera Raspberry Pi HQ + C-mount lens", "Layer camera (lid, viewport)", "yes", "M6", "MIPI CSI-2", "3.3 V from the Pi", "PI", "CAM0", "CSI ribbon", "<= 0.5 m: Pi 5 in PB2, not in the rack", "-", ""],
    ["P-08", "Layer-light LED bar", "Layer-light LED bar (inside the chamber, right wall)", "yes", "M6", "DC LED", "24 V, ~0.3 A (estimate)", "PLC", "s4.4", "-", "PTFE 2 x 22 AWG inside", "needs FT2 (2-pin KF16, SST FA11643): not drawn, no existing chamber opening can carry it without pushing the vacuum valve through the guard (electrical.md 2026-11-23)", "recommend outside, behind the camera viewport or a window"],
    ["P-09", "Chamber wall thermocouple (outside surface)", "not drawn", "no", "none", "type K", "uV", "PLC", "s5.3", "SMPW-K", "type K ext.", "- (surface mount, outside)", "logs the chamber warm-up (heat.md)"],
    ["P-10", "Filter-cake thermocouple well (safety.md P8)", "not drawn", "no", "none", "type K in a closed well", "uV", "PLC", "s5.4", "SMPW-K", "type K ext.", "- (the well is the pressure boundary)", "for passivation"],
    # ---------------- gas
    ["G-01", "O2 analyser Ntron Microx (4-20 mA + alarm relays)", "Trace O2 analyzer + dew-point (gas module box)", "yes", "G6", "4-20 mA + 2 relays", "24 V, ~15-20 W (estimate)", "PLC", "s6.1 (mA), s2.2 (alarm)", "terminals", "shielded twisted 2c, 2.3 m", "-", "O2 < set point is in the PLC permissive (laser, heaters)"],
    ["G-02", "Dew-point transmitter (Vaisala DMT143 class)", "same box", "yes", "G9", "4-20 mA", "24 V", "PLC", "s6.2", "M8 / M12", "shielded", "-", ""],
    ["G-03", "Chamber absolute pressure 0-15 psia (3861N11)", "Pressure transducer (lid)", "yes", "G7", "4-20 mA", "24 V", "PLC", "s6.3", "coiled lead", "shielded 2c", "- (lid SAE-4 port)", "port mismatch noted in real-parts.md"],
    ["G-04", "Chamber differential pressure 0-10 inH2O (5539N26)", "not drawn", "no", "G7", "4-20 mA", "24 V", "PLC", "s6.4", "terminals", "shielded", "-", "overpressure control +5-20 mbar"],
    ["G-05", "Chamber-at-ambient pressure switch (+/-5 mbar)", "not drawn", "no", "none", "dry contact", "24 V", "XS", "IN31", "M12", "PUR", "-", "safety input for the guard unlock; the transmitter is not safety-rated"],
    ["G-06", "Pirani transmitter Vacuum Research 902377 (NW-16, 1-2000 mTorr, 0-10 V and 4-20 mA, 12-35 V DC < 100 mA)", "Pirani transmitter on the vacuum line (KF-25 tee on the isolation valve's pump side)", "yes", "G7", "0-10 V", "24 V, < 100 mA", "PLC", "s7.1", "RJ-45 (power and signal)", "shielded", "- (on the vacuum line: reads the chamber with the valve open)", "a leak-up test with the valve shut would need it on the chamber side"],
    ["G-07", "Argon NC solenoid, purge (8077K237)", "Argon solenoid manifold (gas)", "yes", "G7", "24 V coil", "~8 W held", "PLC via the O2/flow chain", "s3.8", "DIN 43650", "3c 18 AWG", "-", "24 V for both argon valves passes both O2-monitor relays and the exhaust flow switch in series"],
    ["G-08", "Argon NC solenoid, make-up", "manifold", "yes", "G7", "24 V coil", "~8 W", "PLC via the O2/flow chain", "s3.9", "DIN 43650", "3c", "-", ""],
    ["G-09", "Vent valve (to the vent header)", "manifold", "yes (envelope)", "G7", "24 V coil", "~8 W", "PLC", "s3.10", "DIN 43650", "3c", "-", ""],
    ["G-10", "Argon supply shutoff at the dock / cylinder (NC)", "not drawn (safety.md P5/P13)", "no", "safety-parts.csv SP4", "24 V coil", "~8 W", "hard-wired O2 chain", "-", "DIN 43650", "via the dock signal module", "-", ""],
    ["G-11", "Exhaust flow switch in the vent header", "not drawn (safety.md P6)", "no", "safety-parts.csv SP10", "dry contact", "24 V", "XS + valve chain", "IN32", "M12", "PUR", "-", ""],
    ["G-12", "Vacuum pump Edwards nXDS6i A73501983 (dry scroll, inverter drive)", "Dry scroll pump (gas)", "yes", "G2", "AC, 1-phase, auto-sensing 100-127 / 200-240 V", "208 V L1-L2, 6 A rms rated (10 A at 120 V); 260 W at ultimate", "PB1 Q3 (2P 10 A D, time-lag) + KM1 <- PLC", "s3.11", "IEC C14 inlet -> C13 cord to KM1", "14 AWG, 2.3 m", "-", "PLC never runs it while lasing; set Auto-run on (manual 5.5) or the pump stays off when KM1 closes; not on the UPS"],
    ["G-13", "Pump isolation valve 4123K45 (manual) or a powered KF angle valve", "Vacuum isolation valve (manual)", "yes", "G7", "manual (no signal)", "-", "-", "-", "-", "-", "-", "a position switch would let the PLC refuse a purge with the valve shut"],
    ["G-14", "Recirculation blower", "Sealed side-channel blower (gas)", "yes (envelope)", "G4", "AC motor or 24 V BLDC + 0-10 V speed", "120 V <= 230 W or 24 V 20-50 W", "PB1 Q4 + KM2; speed s8.1", "s3.12, s8.1", "-", "-", "-", "G4 product still open"],
    ["G-15", "Room / Shuttle O2 monitors (Macurco OX-6 class, relays)", "not on the tray", "no", "safety-parts.csv SP1/SP2", "relay contacts + 4-20 mA", "24 V", "XS (relays), PLC (mA)", "IN15, IN16; PLC s6.5, s6.6", "via the dock signal module", "shielded", "-", "one monitor per safety channel"],
    # ---------------- safety and operator
    ["S-01", "E-stop, rack operator panel (2 NC)", "E-stop (rack front post)", "yes", "S3", "2 NC, test-pulsed", "24 V", "XS", "IN1, IN2", "22 mm block", "PUR 4c", "-", ""],
    ["S-02", "E-stop, guard front (IDEC XW1E-BV402M-R in a 1-hole enclosure)", "E-stop enclosure, guard right side, near the front", "yes", "S3", "2 NC", "24 V", "XS", "IN3, IN4", "M12 8-pin", "PUR", "-", ""],
    ["S-03", "E-stop, gas module / dock side (IDEC XW1E-BV402M-R in a 1-hole enclosure)", "E-stop enclosure, front of the gas module's O2 box", "yes", "S3", "2 NC", "24 V", "XS", "IN5, IN6", "M12", "PUR", "-", ""],
    ["S-04", "Guard-position switch IDEC HS6B-12B05 (2NC + 1NO, separate from the lock)", "Guard-position switch (door rail, below the guard lock)", "yes (envelope)", "S2", "2 NC", "24 V", "XS", "IN7, IN8", "M12 8-pin", "PUR", "-", "ISO 14119: actuator separate from the lock; a coded non-contact sensor is the better choice"],
    ["S-05", "Guard lock IDEC HS5L-VC44M-G (spring lock, power to unlock)", "Guard-locking door switch (Omron D4JL drawn)", "yes", "S2", "solenoid + monitoring contacts", "24 V, ~0.25 A (estimate)", "XS O6 (unlock); monitoring IN9, IN10", "O6", "M20 cable gland / M12", "PUR 8c", "-", "replaces the out-of-stock D4JL; see electrical.md §4 on spring lock vs power to lock"],
    ["S-06", "Key switch (laser master, 2 channels)", "Key switch (rack panel)", "yes", "S4", "2 contacts", "24 V", "XS", "IN11, IN12", "22 mm block", "PUR", "-", "CFR 1040.10(f)(4)"],
    ["S-07", "Reset push-button (illuminated)", "Reset button (rack panel)", "yes", "S4", "NO, trailing edge", "24 V", "XS", "IN13", "22 mm", "PUR", "-", "CFR 1040.10(f)(10)"],
    ["S-08", "Emission indicator lamp (red, 24 V)", "Emission indicator (rack panel)", "yes", "S4", "lamp via K4+K5 aux", "24 V, 20 mA", "K4/K5 aux contacts", "-", "22 mm", "PUR", "-", "lit whenever emission is possible"],
    ["S-09", "Stack light (green/amber/red/buzzer) + beacon", "not drawn", "no", "S4 (1577T43)", "4 x DO", "24 V", "PLC", "s3.13-3.16", "M12", "PUR", "-", ""],
    ["S-10", "HOT lamp on the guard (plate > 50 C)", "not drawn (safety.md P4)", "no", "none", "DO", "24 V", "PLC (from K8DT)", "s4.9", "22 mm", "PUR", "-", ""],
    ["S-11", "Plate over-temperature from the PLC (diverse channel)", "-", "-", "-", "PNP output -> safety input", "24 V", "PLC -> XS", "s4.10 -> IN18", "-", "-", "-", "interlock_logic.py: needed so a welded CN708 relay is caught"],
    ["S-12", "PLC process permissive", "-", "-", "-", "PNP output -> safety input", "24 V", "PLC -> XS", "s4.11 -> IN19", "-", "-", "-", "chamber O2, pressure window, module/slide present, galvo ready"],
    ["S-13", "EDM: K1 mirror, K3A+K3B mirrors in series, K4+K5 mirrors in series", "-", "-", "-", "NC mirror contacts", "24 V", "XS", "IN35, IN36, IN37", "-", "-", "-", ""],
    ["S-14", "K3A / K3B 48 V servo-bus contactors (WEG CWBS9-33-30C03)", "not drawn", "no", "none", "contactor", "24 V coil", "XS", "O3, O4", "-", "-", "-", "ClearPath-SD has no safe torque off"],
    ["S-15", "K4 / K5 laser-loop contactors with mirror contacts (WEG CWBS9-33-30C03)", "not drawn", "no", "none", "relay 2NO+1NC", "24 V coil", "XS", "O1, O2", "DIN", "-", "-", ""],
    # ---------------- robot, VLM, dock, infrastructure
    ["R-01", "UR12e Safe Home (configurable safety output, 2 ch)", "on the MiR", "no", "robot-tooling.csv", "2 x 24 V", "24 V", "XS", "IN25, IN26", "via the dock signal module or a wireless safety link", "-", "-", "laser chain needs the robot home"],
    ["R-02", "Robot entry permitted -> UR reduced-mode input", "-", "-", "-", "standard output (pair)", "24 V", "PLC", "s4.12, s4.13", "dock signal module", "-", "-", "UR safety plane at the guard opening, 'normal mode only' (check against the UR e-Series manual)"],
    ["R-03", "Robot job request / done (UR standard I/O)", "-", "-", "-", "2 DI + 2 DO", "24 V", "PLC", "s2.3, s2.4 / s4.14, s4.15", "dock signal module", "-", "-", "or over Ethernet"],
    ["V-01", "Tray docked + VLM at rest (dock pins, 2 ch)", "Tray dock", "yes (envelope)", "D1", "2 contacts", "24 V", "XS", "IN21, IN22", "Han-Modular signal module", "-", "-", ""],
    ["V-02", "VLM may move (to the Kardex controller)", "-", "-", "D1", "standard output", "24 V", "PLC", "s4.16", "dock signal module", "-", "-", "Kardex interface not defined (heat.md, safety.md 9)"],
    ["V-03", "Dock power L1, L2, N, PE", "Tray dock", "yes (envelope)", "D1", "AC", "208Y/120 V, 30 A", "PB1 Q0", "-", "Han C 40 A contacts, PE leading (Harting)", "10 AWG 4c + PE, 2.7 m", "-", "two leading PE contacts, drawn on the dock face (protective-conductor current ~9 mA, estimate)"],
    ["V-04", "Dock Ethernet uplink", "Tray dock", "yes (envelope)", "D1", "Ethernet", "-", "switch", "uplink", "Han RJ45 module", "Cat6 S/FTP", "-", ""],
    ["U-01", "UPS Eaton 5PX1500RTG2 + Network-M3 card", "UPS (rack, 2U)", "yes", "D2 (the model tags it C6)", "AC in/out + status", "120 V L1-N in", "PB1 Q2; status -> PI over the network card", "-", "5-15P / 5-15R", "-", "-", "PI starts the power-cut sequence (power.md §3)"],
    ["U-02", "Scan PC (2U) with the RTC6 Ethernet board", "Scan + laser controller PC (rack)", "yes", "C1", "AC (UPS)", "120 V, 200 W", "UPS", "-", "IEC C14", "-", "-", ""],
    ["U-03", "Supervisor Raspberry Pi 5 (8 GB) in PB2", "PB2 process-module box (on the optics bridge)", "yes (envelope)", "C2", "5 V DC", "5 V 5 A from DDR-30G-5", "-", "-", "USB-C / terminals", "-", "-", "next to the camera, NFC and load cell"],
    ["U-04", "Ethernet switch AutomationDirect STRIDE SE2-SW8U", "DIN drawer", "yes (envelope)", "none", "24 V DC", "24 V, 0.2 A", "-", "-", "RJ45", "-", "-", ""],
    ["U-05", "Drawer fan 80 mm 24 V + PB1 filter fan 120 mm 24 V", "not drawn", "no", "none", "DC fans", "24 V, 0.1-0.3 A", "always on (CTRL rail)", "-", "leads", "-", "-", "power.md §4: the drawer needs ~26 CFM without them it runs 51-104 K above ambient"],
]


def main():
    path = ROOT / "electrical-io.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(H)
        w.writerows(R)
    # channel counts
    plc_di = sum(1 for r in R if r[7].startswith("PLC") for _ in [0] if "s1." in r[8] or "s2." in r[8])
    cnt = Counter()
    import re
    for r in R:
        ch = r[8]
        for m in re.findall(r"s(\d)\.(\d+)(?:-(\d)\.(\d+)|-(\d+))?", ch):
            slot = int(m[0])
            a = int(m[1])
            b = int(m[4]) if m[4] else (int(m[3]) if m[3] else a)
            cnt[slot] += (b - a + 1)
        for m in re.findall(r"IN(\d+)(?:-(\d+))?", ch):
            a = int(m[0])
            b = int(m[1]) if m[1] else a
            cnt["XS_in"] += b - a + 1
        for m in re.findall(r"\bO(\d)\b", ch):
            cnt["XS_out"] += 1
    cap = {1: 16, 2: 16, 3: 16, 4: 16, 5: 4, 6: 8, 7: 4, 8: 4, "XS_in": 42, "XS_out": 6}
    names = {1: "P1-16ND3 #1 (DI)", 2: "P1-16ND3 #2 (DI)", 3: "P1-16TD2 #1 (DO)", 4: "P1-16TD2 #2 (DO)", 5: "P1-04THM (TC)",
             6: "P1-08ADL-1 (4-20 mA)", 7: "P1-04ADL-2 (0-10 V)", 8: "P1-04DAL-2 (0-10 V out)", "XS_in": "XS26-2 + XS16si safety inputs",
             "XS_out": "XS26-2 + XS2so safety outputs"}
    L = ["# I/O count against the controllers", "", "Generated by [`analysis/electrical/io_list.py`](../../electrical/io_list.py) from [`electrical-io.csv`](../../../electrical-io.csv).", "",
         f"{len(R)} devices or signals; {sum(1 for r in R if r[3].startswith('no'))} not drawn in the model; {sum(1 for r in R if r[4].startswith('none'))} with no bom.csv line.", "",
         "| Module | Used | Capacity | Spare |", "|---|---|---|---|"]
    for k in cap:
        L.append(f"| {names[k]} | {cnt[k]} | {cap[k]} | {cap[k] - cnt[k]} |")
    L += ["", "ClearCore: M-0 recoater, M-1 Z, M-2 dosing stepper drive, M-3 spare; IO-1..IO-4 home and limit sensors (of 13 I/O)."]
    (OUT / "io_check.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
