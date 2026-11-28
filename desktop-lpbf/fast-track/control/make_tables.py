"""Write io-list.csv and power-budget.csv (with circuit totals) for FT-1, and print the README's summary tables.

Run: python desktop-lpbf/fast-track/control/make_tables.py
Sources (short tags in the 'source' column):
  IPG24  IPG YLR-series user guide, 24-pin generation (pp. 43-45, 56-64), public copy at manualedistruzioni.it (20cai)
  LABEL  the laser's label in the eBay listing photo (lead, 2026-11-27): YLR-400-SM-EOS, Feb 2015, 1/N/PE 200-240 VAC 10 A
  RTC5   SCANLAB RTC5 manual Rev. 1.9 e (pp. 41-48, 204, 440, 557), public copy at manualedistruzioni.it (12dpa)
  RTC4   SCANLAB RTC4 manual Rev. 1.3 e (pp. 54, 107, 123, 130), manualslib.com 1581336
  HS     SCANLAB hurrySCAN 20/30 pin-out sheet (scanlab.de, 2020-10) and hurrySCAN brochure common specs
  G9SE   Omron G9SE-201 instruction sheet 4022078 and datasheet J198
  ZAB    Zaber X-VSR-E / X-LSM-E manuals and spec pages (read 2026-11-27)
  SOLO   AutomationDirect SOLO user manual and SL4848-VR cutsheet
  CN708  DwyerOmega CN708 manual M4628
  AO3000 Alpha Omega Series 3000 datasheet and manual (Instrumart)
  OX6    Macurco OX-6 user manual
  MW     Mean Well LRS-350 spec; WEG CWBS catalogue; Crydom D1D20 datasheet
  MCC    MCC 134 / MCC 128 electrical specifications and daqhats docs
  PI     Raspberry Pi 5 documentation; gpiozero pin factory docs
  THOR   Thorlabs PDA36A2 user guide; LDS12B (search snippet)
  AE     MISTRAS R15I-AST datasheet; Vallen DCPL2 (accessories catalogue 2026-01)
  PICO   Pico Technology PicoScope 4824A specifications
  DIGIKEY Digi-Key product page, read 2026-11-28 (../live-reads-2026-11-28.csv)
  EST    estimate
"""
from __future__ import annotations

import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

IO_COLS = ["id", "device", "signal", "type", "level", "connector / pin", "from", "to", "owner", "status", "source", "notes"]
# owner: SAFETY (hard-wired chain, no software), RTC (scan card), PC (supervisor on the PC), PI (Pi I/O node),
#        STANDALONE (own controller), REC (fast recorder), POWER
IO = [
    # ---------------------------------------------------------------- laser
    ("L-01", "IPG YLR-400-SM-EOS", "AC supply", "AC power", "200-240 VAC 1/N/PE, 10 A max (label)", "rear terminal block (24-pin generation: L1/L2/PE screw terminal)", "room circuit A: 208/240 V 2-pole 15 A breaker + lockable disconnect", "laser", "POWER", "label read; connector to check", "LABEL, IPG24 p. 42", "IPG: dedicated circuit, breaker <= 20 A, within reach, marked as the disconnect"),
    ("L-02", "IPG YLR-400-SM-EOS", "Interlock channel 1", "dry contact loop", "24 VDC from the laser, < 1 A; external contacts rated > 1 A / 24 VDC; < 500 ms (<= 1000 ms with one channel failed)", "24-pin: 1-4; EOS unit: INTERLOCK connector (map on arrival)", "G9SE-201 13-14", "laser", "SAFETY", "guide; EOS pin-out to measure", "IPG24 p. 43-44", "ISO 13849-1 Cat 3 PL d in the guide; potential-free contacts only"),
    ("L-03", "IPG YLR-400-SM-EOS", "Interlock channel 2", "dry contact loop", "as L-02", "24-pin: 2-3; EOS: INTERLOCK connector", "G9SE-201 23-24", "laser", "SAFETY", "guide; EOS pin-out to measure", "IPG24 p. 43-44", "one channel open: both must open before a restart"),
    ("L-04", "IPG YLR-400-SM-EOS", "Modulation (gate) +/-", "digital in", "CMOS to 24 VDC, 6 mA sink, 20 us; up to 50 kHz", "24-pin: 15/16; EOS: MODULATION INPUT (likely BNC)", "RTC5 LASER pin 2 LASERON (TTL, <= 20 mA, ref GND2 pin 10); RTC4: 9-pin pin 2", "laser", "RTC", "guide; EOS connector to measure", "IPG24 p. 44, RTC5 p. 46", "LASERON active high (set_laser_control bit 3 = 0); 5 V TTL is inside the 5-24 V range"),
    ("L-05", "IPG YLR-400-SM-EOS", "Analog power set point", "analog in", "1-10 V = 10-100 %, 1 mA sink, 100 us", "24-pin: 12 (signal) / 14 (isolated analog common)", "RTC5 LASER pin 8 ANALOG OUT1 (0-10 V, 12-bit, 5 mA, ref GND pin 14); RTC4: 9-pin pin 4 (10-bit; jumper to 0-10 V)", "laser", "RTC", "guide; EOS: may take power over RS-232 only (measure)", "IPG24 p. 44, RTC5 p. 47", "needs EEC (external control) over RS-232; below 1 V the laser holds its 10 % minimum"),
    ("L-06", "IPG YLR-400-SM-EOS", "Power monitor", "analog out", "0-5 V; 0-4 V = 0-Pnom; 11 mA source", "24-pin: 13 / 14", "laser", "PicoScope ch E", "REC", "guide", "IPG24 p. 44", "logs the delivered power at every vector"),
    ("L-07", "IPG YLR-400-SM-EOS", "RS-232", "serial", "57,600 8N1, 3-wire, CR-terminated ASCII", "24-pin: 5 Tx / 6 Rx / 7 common", "PC COM (USB-RS232)", "laser", "PC", "guide; EOS baud and port to check", "IPG24 p. 56", "EMON, EMOFF, STA, RERR, EEC, EMOD, DLE, ABN/ABF, RCT, ROP, RET, RMEC"),
    ("L-08", "IPG YLR-400-SM-EOS", "Remote key", "contact closure in", "5 or 24 VDC", "24-pin: 8-9", "operator key switch, third contact (NO)", "laser", "SAFETY", "guide", "IPG24 p. 44", "the laser's front keyswitch must be in REM"),
    ("L-09", "IPG YLR-400-SM-EOS", "Remote START", "momentary contact in", "24 VDC, 1 s", "24-pin: 10-11; EOS: RESET connector?", "LASER START push button (NO)", "laser", "SAFETY", "guide; EOS RESET connector to map", "IPG24 p. 44", "starts the main supply after the interlock closes"),
    ("L-10", "IPG YLR-400-SM-EOS", "Error/Ready", "digital out", "24 VDC source, 100 mA; low = error", "24-pin: 19 / common 20", "laser", "Pi GPIO 19 LASER_READY (opto)", "PI", "guide", "IPG24 p. 44", "low on any laser error, incl. high back reflection (STA bit 3)"),
    ("L-11", "IPG YLR-400-SM-EOS", "Power supply active", "digital out", "24 VDC source, 100 mA", "24-pin: 23 / 20", "laser", "Pi GPIO 15 LASER_PS_ACTIVE (opto) + amber LASER ARMED lamp", "PI", "guide", "IPG24 p. 44", "high while the diode supply is on: the beam is possible"),
    ("L-12", "IPG YLR-400-SM-EOS", "Emission ON", "digital out", "24 VDC source, 100 mA", "24-pin: 24 / 20", "laser", "Pi GPIO 16 LASER_EMISSION (opto) + red EMISSION lamp", "PI", "guide", "IPG24 p. 44", "the emission lamp on the frame (21 CFR 1040.10(f)(5))"),
    ("L-13", "IPG YLR-400-SM-EOS", "Back reflection", "status bit", "STA bit 3 'High Back Reflection Level'", "RS-232 (L-07)", "laser", "PC supervisor (polled at 5 Hz while scanning)", "PC", "guide; whether this unit has back-reflection protection: ask IPG with the serial", "IPG24 p. 63", "Edison round 2's top risk; fault BACK_REFLECTION"),
    ("L-14", "IPG YLR-400-SM-EOS", "E-stop out (8-pin)", "dry contacts", "< 250 VDC < 3 A", "8-pin: 1-4", "laser front E-stop", "spare (or in series with the machine E-stop)", "SAFETY", "guide", "IPG24 p. 45", "the laser's own E-stop already drops its supply"),
    ("L-15", "IPG YLR-400-SM-EOS", "Guide laser, emission enable, error reset, power on (pins 17, 18, 21, 22)", "digital in/out", "CMOS-24 V", "24-pin", "-", "not wired", "PC", "guide", "IPG24 p. 44", "done over RS-232 instead (ABN/ABF, EMON, RERR)"),
    # ---------------------------------------------------------------- scan card and head
    ("R-01", "SCANLAB RTC5 PCIe", "Scan head data (SL2-100)", "differential digital", "SL2-100, 20-bit", "SCAN HEAD D-sub 9 female", "RTC5", "SCANLAB XY2-100 converter (9-pin male -> 25-pin female), then a 25-pin cable to the head", "RTC", "datasheet", "RTC5 p. 41-43", "the RTC5 has no XY2-100 output of its own; the converter adds 10 us (laser delays raised by 10 us)"),
    ("R-01b", "SCANLAB RTC4 PCIe (alternative)", "Scan head data (XY2-100)", "differential digital", "XY2-100, 16-bit", "D-sub 25 female: CLOCK 1/14, SYNC 2/15, CHAN1 3/16, CHAN2 4/17, CHAN3 5/18, STATUS 6/19", "RTC4", "hurrySCAN DIGITAL IN (1:1 25-pin cable)", "RTC", "manual", "RTC4 p. 54", "drives the 2003 head directly"),
    ("R-02", "SCANLAB RTC5 PCIe", "Layer marker", "digital out", "LOW < 0.55 V, HIGH > 3.8 V, 20 mA", "LASER pin 12 DIGITAL OUT1 (GND pin 14)", "RTC5 (set_laser_pin_out_list 1 / 0 around each layer)", "PicoScope ch D", "RTC", "datasheet", "RTC5 p. 46, 204", "ties the recorder's clock to each layer; RTC4: EXTENSION 1 DIGITAL_OUT0 (write_io_port_list)"),
    ("R-03", "SCANLAB RTC5 PCIe", "LASERON copy", "digital out", "TTL", "LASER pin 2 (tee to the laser and the recorder)", "RTC5", "PicoScope ch C", "RTC", "datasheet", "RTC5 p. 46", "the same LASERON edges are in the card's own set_trigger4 trace: one time base"),
    ("R-04", "SCANLAB RTC5 PCIe", "/STOP", "digital in", "TTL active low, pull-up to 3.3 V, ref GND", "LASER pin 11", "K3 NC contact to GND (K3 coil on G9SE X1)", "RTC5", "SAFETY", "datasheet; K3 is an addition", "RTC5 p. 46", "when the chain opens the card stops its list in hardware too (G9SE X1 drops, K3 drops, /STOP low)"),
    ("R-05", "SCANLAB RTC5 PCIe", "BUSY OUT", "digital out", "TTL, ref GND", "LASER pin 4", "RTC5", "PicoScope ch F (optional)", "REC", "datasheet", "RTC5 p. 46", "-"),
    ("R-06", "SCANLAB RTC5 PCIe", "Head status (PowerOK, TempOK, PosAck X/Y)", "status word", "XY2-100 status via the converter", "via R-01", "head", "RTC5 (set_laser_control bits 16, 17, 19, 20, 28) + supervisor (get_head_status, 5 Hz)", "RTC", "datasheet", "RTC5 p. 266, 440", "the card suppresses LASERON on a head error by itself (RTC5 only)"),
    ("H-01", "SCANLAB hurrySCAN 25 (2003)", "Galvo supply", "DC power", "+/-(15 + 1.5) V DC, max 6 A per rail (20/25/30 family)", "POWER IN D-sub 9 male: -15 V pins 1, 2, 6; GND 3, 7, 8; +15 V 4, 5, 9", "2 x 15 V supplies in series (midpoint = GND)", "head", "POWER", "current pin-out sheet; check a 2003 head by continuity first", "HS", "fuse each rail; switch both rails together"),
    ("H-02", "SCANLAB hurrySCAN 25 (2003)", "XY2-100 data in", "differential digital", "XY2-100 16-bit", "DIGITAL IN D-sub 25 female (pins as R-01b)", "XY2-100 converter (RTC5) or RTC4", "head", "RTC", "current pin-out sheet", "HS", "-"),
    ("H-03", "SCANLAB hurrySCAN 25 (2003)", "Cooling water flow switch", "dry contact", "24 V via the Pi's opto input", "flow switch in the head's water return", "flow switch (NO, closed at flow)", "Pi GPIO 2 WATER_OK", "PI", "addition (estimate)", "HS (water 5 L/min, dp < 0.1 bar, p < 4 bar)", "the entrance aperture is water-cooled; fault COOLING_FAULT"),
    ("H-04", "SCANLAB hurrySCAN 25 (2003)", "Mirror air", "compressed air", "clean dry air, 20 L/min at dp < 2 bar", "push-in fitting", "lab air or N2 through a filter-regulator", "head", "STANDALONE", "brochure (family)", "HS", "not electrical"),
    # ---------------------------------------------------------------- safety chain
    ("S-01", "Omron G9SE-201", "Supply", "DC power", "24 VDC -15/+10 %, 3 W", "A1 (+), A2 (0 V)", "24 V CTRL", "G9SE", "SAFETY", "datasheet", "G9SE", "start >= 2 s after power-up"),
    ("S-02", "Omron G9SE-201", "Input channel 1", "dry contact chain", "24 V / 5 mA from the relay", "T11-T12", "E-stop NC1 - lid switch NC1 - beam-tube switch NC1 - key NO1 - TS tube 1 - TS window 1", "G9SE", "SAFETY", "datasheet", "G9SE", "one channel open alone latches a mismatch: both must open to clear it"),
    ("S-03", "Omron G9SE-201", "Input channel 2", "dry contact chain", "as S-02", "T21-T22", "the same devices' second contacts", "G9SE", "SAFETY", "datasheet", "G9SE", "-"),
    ("S-04", "Omron G9SE-201", "Manual reset + feedback loop", "momentary contact", "T32 OFF -> ON -> OFF, >= 250 ms", "T31-T32", "blue SAFETY RESET button (NO)", "G9SE", "SAFETY", "datasheet", "G9SE", "no external contactors on the laser path, so the loop is the button only"),
    ("S-05", "Omron G9SE-201", "Safety output 1", "relay NO", "30 VDC 5 A resistive, DC-13 24 V 1.5 A, min 24 V 4 mA", "13-14", "G9SE", "laser interlock channel 1 (L-02)", "SAFETY", "datasheet", "G9SE", "the laser's loop current is well inside 4 mA ... 1 A (measure)"),
    ("S-06", "Omron G9SE-201", "Safety output 2", "relay NO", "as S-05", "23-24", "G9SE", "laser interlock channel 2 (L-03)", "SAFETY", "datasheet", "G9SE", "-"),
    ("S-07", "Omron G9SE-201", "Status (aux) output", "PNP", "24 V, 100 mA; follows the safety outputs", "X1", "G9SE", "Pi GPIO 14 SAFETY_OK (opto) + K3 coil (RTC5 /STOP relay)", "PI", "datasheet", "G9SE", "not a safety output"),
    ("S-08", "E-stop (IDEC XW1E class, 3 NC blocks)", "E-stop", "3 x NC (direct opening)", "24 V", "NC1, NC2 to the chain; NC3 in K1's coil circuit", "operator panel", "G9SE T11/T21 chains + K1", "SAFETY", "part to choose", "EST", "NC3 drops the heater contactor K1 directly"),
    ("S-09", "Lid switch: Omron D4NS-2CF + D4DS-K operation key", "Lid closed", "2 NC direct opening + 1 NO", "24 V", "NC1, NC2 to the chain; NO to the Pi", "box side / key on the lid", "G9SE chains + Pi GPIO 3 LID_CLOSED", "SAFETY", "Omron catalogue CSM1235: slow-action 2NC/1NO, G1/2 conduit; Digi-Key Z4035-ND, 552 in stock, $79.27 (search snapshot 2026-11-27)", "G9SE, EST", "one switch: a stuck contact shows on the next lid opening (ftctl.interlock); two in series mask each other. Reed-type coded switches are not in the G9SE documents"),
    ("S-10", "Beam-tube switch (D4NS class)", "Beam tube in place", "2 NC direct opening", "24 V", "NC1, NC2 to the chain", "tube flange", "G9SE chains", "SAFETY", "part to choose", "EST", "opened only for service"),
    ("S-11", "Key switch (3 NO)", "Laser enable key", "2 NO to the chain + 1 NO to the laser", "24 V", "NO1, NO2; NO3 -> laser pins 8-9", "operator panel", "G9SE chains + laser remote key", "SAFETY", "part to choose", "EST", "-"),
    ("S-12", "Bimetal temperature switches, 4 x NC, 75 C: Sensata-Airpax 67L075 (TO-220)", "Stray beam (beam tube, window ring)", "NC thermal contact", "24 V", "2 on the beam tube, 2 on the window ring: one of each per channel", "-", "G9SE chains", "SAFETY", "Digi-Key 2026-11-28 (67F075 is the NO part: not that one)", "DIGIKEY", "the supervisor's thermocouples trip first (60-65 C); these are the backstop"),
    ("S-13", "K3 (24 VDC signal relay, 1 NC)", "Hardware list stop", "relay", "coil on G9SE X1", "NC between RTC5 LASER pin 11 (/STOP) and pin 14 (GND)", "G9SE X1", "RTC5 /STOP", "SAFETY", "addition", "RTC5 p. 46", "chain open -> /STOP low -> list stopped without software"),
    ("S-14", "Push buttons", "SAFETY RESET (blue), LASER START (white)", "momentary NO", "24 V", "-", "operator panel", "G9SE T31-T32; laser pins 10-11", "SAFETY", "part to choose", "EST", "-"),
    ("S-15", "Lamps 24 V LED", "LASER ARMED (amber), EMISSION (red), SAFE TO OPEN (green)", "lamp", "24 VDC <= 20 mA each", "-", "laser pin 23; laser pin 24; Pi BEACON relay", "frame", "PI", "part to choose", "EST", "emission lamp lit whenever the laser can emit"),
    # ---------------------------------------------------------------- heaters
    ("T-01", "Plate heaters 2 x 50 W, 24 V (McMaster 3714N36)", "Heater power", "DC power", "24 V, 2 x 2.08 A (11.5 ohm each)", "leads down the hollow rod", "SSR1 (Crydom D1D20)", "plate", "STANDALONE", "datasheet (McMaster)", "EST", "SSR1 on a heat sink: 0.039 ohm x 4.2 A^2 ~ 0.7 W"),
    ("T-02", "Block heaters 2 x 50 W, 24 V", "Heater power", "DC power", "24 V, 2 x 2.08 A", "block holes", "SSR2 (Crydom D1D20)", "well block", "STANDALONE", "datasheet", "EST", "-"),
    ("T-03", "Crydom D1D20 x 2", "SSR control", "DC in", "3.5-32 VDC, 15 mA max; output 1-72 VDC, 20 A (2 C/W heat sink); leakage 0.3 mA", "control +/-", "SOLO OUT1 (voltage pulse 14 V, 40 mA)", "SSR", "STANDALONE", "datasheet", "MW", "-"),
    ("T-04", "AutomationDirect SOLO SL4848-VR-D x 2", "PID plate / block", "controller", "24 VDC, 5 VA; type K in; OUT1 voltage pulse; RS-485 Modbus RTU", "PV 0x1000 (0x8002-0x8007 = sensor error), SV 0x1001 (0.1 C; P3-12 CoSH = ON)", "TC-P (plate) / TC-B (block)", "SSR1 / SSR2; Pi RS-485 (USB adapter), addresses 1 and 2", "STANDALONE", "datasheet", "SOLO", "control runs without the PC; sensor break -> output off"),
    ("T-05", "Type K thermocouples, ungrounded", "TC-P plate (PID), TC-L plate (limit), TC-B block (PID)", "thermocouple", "type K", "TC-P and TC-L down the rod; TC-B in the block", "plate / block", "SOLO plate, CN708, SOLO block", "STANDALONE", "addition: a TC in the plate for its PID (Edison round 2)", "EST", "the CN708's 24 V model takes ungrounded TCs only"),
    ("T-06", "DwyerOmega CN708", "Over-temperature limit", "limit controller", "24 VAC/VDC, 4 VA; type K; SPDT 16 A; latching (hoL), relay drops in alarm; TC break shows ooo (set c2 so the relay drops)", "relay NO in K2's coil circuit", "TC-L", "K2 coil", "STANDALONE", "datasheet", "CN708", "set point 240 C (estimate); manual reset at the front"),
    ("T-07", "K1: WEG CWBS12-33-30C03", "Heater bus enable", "contactor", "coil 24 VDC 5.8 W; DC-1 18 A at 24 V one pole; mirror aux contacts", "main NO in the +24 V heater bus; aux NO -> Pi", "24 V CTRL via E-stop NC3 and Pi relay HEAT_EN", "heater bus; Pi GPIO 7 K1_ON", "PI", "datasheet", "MW", "dropped by the E-stop, by software, and by the Pi's 5 s watchdog"),
    ("T-08", "K2: WEG CWBS12-33-30C03", "Heater limit", "contactor", "as K1", "main NO in series with K1; aux NO -> Pi", "24 V CTRL via the CN708 relay", "heater bus; Pi GPIO 20 LIMIT_OK", "STANDALONE", "datasheet", "MW, CN708", "-"),
    # ---------------------------------------------------------------- motion
    ("M-01", "Zaber X-VSR20A-E01 (piston)", "Supply", "DC power", "24-48 VDC, 0.95 A max", "2-pin screw terminal on the first stage", "48 V Zaber PS14S-48V37 (3.75 A)", "chain", "POWER", "datasheet", "ZAB", "power passes along the chain (M8 pin 1, 4 A max)"),
    ("M-02", "Zaber X-LSM100B-E03 (recoater)", "Supply", "DC power", "24-48 VDC, 0.35 A max", "via the daisy chain", "M-01", "chain", "POWER", "datasheet", "ZAB", "-"),
    ("M-03", "Zaber chain", "Data", "RS-232 (ASCII)", "115,200 8N1", "M8 4-pin Prev/Next: 1 power, 2 GND, 3 RX/TX, 4 TX/RX", "PC USB (Zaber X-USBDC or a USB-RS232 adapter)", "both stages", "PC", "datasheet", "ZAB", "warning flags F* are faults (STAGE_FAULT)"),
    # ---------------------------------------------------------------- gas and O2
    ("G-01", "Argon main valve (McMaster 8077K237, NC, 24 VDC)", "Argon on", "solenoid", "24 VDC, coil W not published (ASCO 8262: 10.6 W)", "DIN-A connector", "Pi relay ARGON (GPIO 17) via K4 (room-O2 relay)", "valve", "PI", "datasheet / coil power estimate", "EST", "purge and build flow set on the flowmeter (~27 L/min)"),
    ("G-02", "Argon low-flow valve (24 VDC NC) + needle valve", "Argon hold", "solenoid", "24 VDC ~10 W", "-", "Pi relay ARGON_LOW (GPIO 27) via K4", "valve", "PI", "addition (estimate)", "EST", "~5 L/min while cooling, saves ~1.3 m3 an hour"),
    ("G-03", "Vent valve (24 VDC NC)", "Air in after a build", "solenoid", "24 VDC ~10 W", "-", "Pi relay VENT (GPIO 22)", "valve", "PI", "addition (estimate)", "EST", "air through the inlet filter, ~10 L/min, after the plate is < 60 C"),
    ("G-04", "Trace-cell isolation valve (24 VDC NC)", "Trace O2 sample on", "solenoid", "24 VDC ~10 W", "-", "Pi relay TRACE_SAMPLE (GPIO 23)", "valve", "PI", "addition", "AO3000 (ranges up to 10,000 ppm)", "opened only below 1.5 % O2 so the trace cell never sees air"),
    ("G-05", "Alpha Omega Series 3000 (trace O2, electrochemical)", "Box O2, ppm", "4-20 mA", "0-10,000 ppm range; 18-32 VDC supply (terminals 29/30); 4-20 mA on 12/13", "250 ohm shunt -> MCC 128 ch 0", "analyzer", "Pi", "PI", "datasheet", "AO3000", "sample 0.5-1.0 L/min at 0.1-1.5 psig from the exhaust; no pump as standard (the box runs at 0.07-0.15 psig: marginal)"),
    ("G-06", "Percent O2 transmitter on the exhaust (2nd Macurco OX-6, 4-20 mA on)", "Box O2, %", "4-20 mA", "4-20 mA = 0-25 %; 12-32 VDC, 3 W", "MCC 128 ch 1", "transmitter", "Pi", "PI", "addition; datasheet", "OX6", "decides the heater start (< 1 %) and the lid (>= 19.5 %)"),
    ("G-07", "Macurco OX-6 (room O2)", "Room O2", "4-20 mA + relays", "4-20 mA = 0-25 %; alarm relay 0.5 A (19.5 % default)", "MCC 128 ch 2; alarm relay NC in K4's coil circuit", "monitor", "Pi + K4", "SAFETY", "datasheet", "OX6", "alarm opens K4, which closes both argon valves; a broken 4-20 mA loop reads NaN -> fault"),
    ("G-08", "K4 (24 VDC relay, 2 NO)", "Argon permitted", "relay", "coil 24 V via the OX-6 alarm relay", "NO1 feeds the argon valves' common; NO2 -> Pi", "OX-6", "G-01, G-02; Pi GPIO 21 ROOM_O2_OK", "SAFETY", "addition", "OX6", "the OX-6 relay (0.5 A) cannot carry both coils itself"),
    ("G-09", "Hopper vibration motor (12 V eccentric, QFF-130 class)", "Vibrator", "DC motor", "12 V <= 0.45 A (24 -> 12 V converter)", "-", "Pi relay VIBRATOR (GPIO 24)", "hopper", "PI", "estimate", "EST", "on only during the spread stroke"),
    # ---------------------------------------------------------------- monitoring and I/O node
    ("P-01", "Raspberry Pi 5 + MCC 134 + MCC 128", "I/O node", "computer", "5 V 5 A (27 W USB-C supply)", "Ethernet to the PC (direct link); RS-485 USB adapter", "-", "-", "PI", "datasheet", "PI, MCC", "MCC HATs use GPIO 8-11, 12, 13, 26: the pin map avoids them"),
    ("P-02", "MCC 134", "Thermocouples: window ring (ch 0), beam tube (1), box air (2), stage body (3)", "type K", "isolated inputs; open TC = -9999.0", "screw terminals", "TCs", "Pi", "PI", "datasheet", "MCC", "window ring catches cover-slide fouling (Edison round 2)"),
    ("P-03", "Relay interface (ULN2803A + 8 x 24 V DIN relays)", "Outputs", "relay", "3.3 V GPIO in, 24 V coils", "GPIO 17, 27, 22, 23, 24, 25, 4, 18", "Pi", "ARGON, ARGON_LOW, VENT, TRACE_SAMPLE, VIBRATOR, HEAT_EN, LEDS, BEACON", "PI", "part to choose", "EST", "all de-energised = safe (valves NC, heaters off)"),
    ("P-04", "Opto input board (8-ch, 24 V -> 3.3 V, PC817 class)", "Inputs", "opto", "24 V in; pulls the GPIO low when on", "GPIO 14, 15, 16, 19, 20, 21, 2, 3, 7 (7 needs dtoverlay=spi0-1cs)", "SAFETY_OK, LASER_PS_ACTIVE, LASER_EMISSION, LASER_READY, LIMIT_OK, ROOM_O2_OK, WATER_OK, LID_CLOSED, K1_ON", "Pi", "PI", "part to choose", "EST", "needs 9 channels: two 8-ch boards or one 16-ch"),
    ("P-05", "Raspberry Pi HQ camera (IMX477)", "Layer images", "CSI", "-", "Pi 5 CAM0", "camera", "Pi", "PI", "datasheet", "PI", "no external trigger (the Global Shutter camera has one); images are software-timed after each spread and scan"),
    ("P-06", "Raking LED bars (Basler 17x300 class)", "LEDs", "DC", "24 V, 18.4 W each (estimate: one bar)", "M8", "Pi relay LEDS (GPIO 4)", "LEDs", "PI", "datasheet", "EST", "on only while the camera captures"),
    ("P-07", "Thorlabs PDA36A2 (coaxial photodiode)", "Melt-pool light", "analog", "0-10 V into Hi-Z; +/-12 V from LDS12B", "BNC", "photodiode", "PicoScope ch A", "REC", "datasheet", "THOR", "gain to suit (e.g. 20 dB: 1 MHz bandwidth)"),
    ("P-08", "MISTRAS R15I-AST + Vallen DCPL2", "Acoustic emission", "analog (AC)", "28 V phantom, 25 mA; decoupler 28-30 VDC, 70 mA", "BNC", "AE sensor on the rod or block", "PicoScope ch B", "REC", "datasheet", "AE", "50-400 kHz"),
    ("P-09", "PicoScope 4824A", "Recorder", "8-ch 12-bit USB", "20 MS/s shared streaming", "BNC A-H", "A photodiode, B AE, C LASERON, D layer marker, E laser power monitor, F BUSY", "PC USB 3", "REC", "datasheet", "PICO", "one sample clock for all fast signals; LASERON + marker tie it to the RTC5 and the supervisor"),
]

PW_COLS = ["circuit", "load", "supply", "V", "typical_W", "max_W", "max_A_at_supply", "basis", "source", "notes"]
PW = [
    # circuit A: the laser
    ("A: 208/240 V 1-phase, 15 A 2-pole", "IPG YLR-400-SM-EOS", "direct", 208, 1400, 2080, 10.0, "label 200-240 V 10 A; typical: 400 W out at ~30 % wall-plug + fans (estimate)", "LABEL, EST", "idle ~150 W (PR 266 estimate); IPG wants a breaker <= 20 A and a disconnect within reach"),
    # circuit B: everything else at 120 V
    ("B: 120 V, 20 A", "PC with the RTC5 (or RTC4) + monitor", "direct", 120, 200, 400, 3.3, "estimate", "EST", "-"),
    ("B: 120 V, 20 A", "Scan head +/-15 V (2 x 15 V 7 A supplies)", "2 x Mean Well LRS-100-15 class", 120, 60, 200, 1.7, "max 6 A a rail (brochure); typical while marking (estimate)", "HS, EST", "a galvo draws its peaks in accelerations"),
    ("B: 120 V, 20 A", "Heaters 4 x 50 W via SSRs", "Mean Well LRS-350-24 (88 %)", 120, 70, 230, 6.8, "typical: ~56 W held at 200 C (study 3.5) + losses; max: all four on + PSU loss; 6.8 A is the PSU's rated input at 115 V", "MW, study", "60 A cold-start inrush; no PFC"),
    ("B: 120 V, 20 A", "24 V CTRL: G9SE 3 W, 2 x SOLO 10 VA, CN708 4 VA, K1 + K2 11.6 W, K3 + K4 ~2 W, AO3000 ~10 W, 2 x OX-6 6 W, 4 valves ~40 W (ARGON + one more at a time: ~20 W), lamps 3 W, fan 5 W, LEDs 18 W, vibrator 6 W, opto/relay boards ~4 W", "Mean Well SDR-240-24 class (24 V 10 A)", 120, 70, 140, 1.4, "sum of the items (datasheets where read, else estimate)", "G9SE, SOLO, CN708, MW, AO3000, OX6, EST", "-"),
    ("B: 120 V, 20 A", "Zaber stages (both)", "Zaber PS14S-48V37 (48 V 3.75 A)", 120, 20, 70, 0.7, "max 0.95 + 0.35 A at 48 V (Zaber) + supply loss", "ZAB", "-"),
    ("B: 120 V, 20 A", "Raspberry Pi 5 + HATs + camera", "27 W USB-C supply", 120, 10, 27, 0.3, "Pi docs: ~25 W ceiling", "PI", "-"),
    ("B: 120 V, 20 A", "Photodiode (LDS12B), AE decoupler (28 V), PicoScope (USB)", "own adapters", 120, 10, 15, 0.2, "LDS12B ~6 W; DCPL2 70 mA at 28 V", "THOR, AE", "-"),
    # circuit C: only if the laser is water-cooled
    ("C: 120 V, 15-20 A (only if the laser is water-cooled)", "Recirculating chiller ~1.4 kW cooling (TEYU CW-5200 class)", "direct", 110, 570, 790, 6.7, "CW-5200: 0.57-0.79 kW, 0.5-6.7 A at 110 V (vendor page)", "EST", "ThermoFlex 900 asks for its own 15 A circuit"),
]


def write():
    with (HERE / "io-list.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(IO_COLS)
        for r in IO:
            assert len(r) == len(IO_COLS), r[0]
            w.writerow(r)
    totals = {}
    for r in PW:
        c = r[0].split(":")[0]
        t = totals.setdefault(c, dict(typical_W=0.0, max_W=0.0, max_A=0.0, V=r[3]))
        t["typical_W"] += r[4]
        t["max_W"] += r[5]
        t["max_A"] += r[6]
    with (HERE / "power-budget.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(PW_COLS)
        for r in PW:
            assert len(r) == len(PW_COLS), r[1]
            w.writerow(r)
        for c, t in totals.items():
            w.writerow([f"{c}: TOTAL", "", "", t["V"], round(t["typical_W"]), round(t["max_W"]), round(t["max_A"], 1),
                        "sum of the rows above", "", ""])
    return totals


def summary(totals) -> str:
    own = {}
    for r in IO:
        own[r[8]] = own.get(r[8], 0) + 1
    lines = ["| Owner | Rows |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in sorted(own.items())]
    lines += ["", "| Circuit | Typical W | Max W | Max A at the supply voltage |", "|---|---:|---:|---:|"]
    for c, t in totals.items():
        lines.append(f"| {c} | {t['typical_W']:.0f} | {t['max_W']:.0f} | {t['max_A']:.1f} A at {t['V']} V |")
    return "\n".join(lines)


if __name__ == "__main__":
    tot = write()
    print(f"io-list.csv: {len(IO)} rows; power-budget.csv: {len(PW)} loads")
    print(summary(tot))
