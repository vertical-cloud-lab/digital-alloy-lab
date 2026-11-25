"""Build desktop-lpbf/monitoring-bom.csv: the bought parts for monitoring.md §4's steps 0-8 (issue #260, PR 281).

Prices are list prices read on the vendors' own pages through the lab tunnel on 2026-11-25 (the lookups, with URL, UTC time,
stock or lead time and notes, are analysis/out/monitoring/fab/price_lookups_optics.csv and price_lookups_cameras.csv), used
listings read on eBay the same way, the closest instant quotes already in the repo for the custom parts
(hours_monitoring.csv), or labelled estimates. Nothing is a quote for this machine, and nothing was ordered.

Columns follow optics-bom.csv, plus the step (0-8 of monitoring.md §4), extended prices, stock or lead time, and the used
option. Totals per step: new (low / high) and with the used options taken where a listing exists.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/build_bom.py [--p1 CSV] [--p2 CSV]
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[2]
OUT = D / "analysis" / "out" / "monitoring" / "fab"
BOM = D / "monitoring-bom.csv"
LOOK = {"p1": OUT / "price_lookups_optics.csv", "p2": OUT / "price_lookups_cameras.csv"}
STEPS = {"0": "before machining: the ports' parts", "1": "clock and recorder", "2": "spectral check of the scan head",
         "3": "layer camera tuned", "4": "acoustic emission", "5": "two-colour coaxial", "6": "coaxial camera",
         "7": "side high-speed camera (and the steep lid camera)", "8": "cooling through solidification"}

# (id, step, group, element, source, qty, action, in_model, notes, used_keys)
#   source: ("p1"|"p2", key)  - a lookup row;  ("est", low, high, basis, part_number, vendor)  - an estimate;
#           ("custom", usd, basis)  - a custom part's outside price (hours_monitoring.csv)
SEL = [
    # ---------------- step 0: the ports (bought when the ports are cut; blanks are not needed if the windows go in) ---------
    ("M0-01", "0", "ports", "LW window: UV fused silica Ø40 x 4 mm, NIR I AR 600-1050 nm (no Ø38.1 mm NIR-coated catalogue window exists)",
     ("p1", "W1"), 1, "add; change the LW seat to Ø40.2 x 5.5 mm (frame_features.py has Ø38.3 x 6.5 for monitoring_spec's Ø38.1 x 5)",
     "not drawn", "Robinson's minimum for the Ø31 opening at 1 bar, F/S 10, is 2.4 mm (Edison r8-viewports): 4 mm is ample. "
     "Fit it from the start instead of making a blank (hours_monitoring.csv)", []),
    ("M0-02", "0", "ports", "LW cover slides, fused silica Ø30 x 1.5 mm (laser-head protective glass), 6 to start",
     ("p1", "W4-b"), 6, "add (consumable)", "not drawn",
     "6+ price $41.17 each. Edmund 22-695 (Ø30 x 1, $101; 6-25: $81) is the optical-grade option. Cloudray-type fibre-laser "
     "windows show ~GBP 7.30 each in a search snippet (eBay blocked the tunnel): check size and coating before relying on them. "
     "Measure how often a slide must change before stocking more (monitoring.md §6)", []),
    ("M0-03", "0", "ports", "BW window: rectangle ~57.7 x 26.7 x 3 mm, borosilicate or fused silica, corners chamfered 2 mm",
     ("est", 40.0, 120.0, "estimate (custom cut; no catalogue size)", "custom", "glass shop / Edmund custom"), 1, "add", "not drawn",
     "A light window only (no imaging): 3 mm fused silica has F/S ~16 over the 20.5 mm wide slot at 1 bar; borosilicate wants 3.6 mm "
     "for F/S 10. The seat is 58 x 27 x 4.5 mm (frame_features.py)", []),
    ("M0-04", "0", "custom (outsourced)", "LP blanking cap over the lid's Ø37 bore until the steep camera is bought (6061 1/4 in. plate, "
     "on the boss's face O-ring and screws)", ("custom", 14.01, "analogue: SendCutSend laser, the spacer ring, $14.01"), 1,
     "outsource", "not drawn", "monitoring_spec: the LP ships blanked", []),
    ("M0-05", "0", "ports", "(the LP window and slides are bought with the steep camera: M7-15, M7-16)", ("est", 0.0, 0.0, "-", "-", "-"),
     0, "note", "-", "", []),
    ("M0-06", "0", "ports", "FKM sheet 1/32 in. for the windows' flat gaskets and flat rings (LW, BW, LP)",
     ("est", 20.0, 40.0, "estimate (McMaster FKM sheet, not fetched)", "FKM 75A sheet, 1/32 in.", "McMaster-Carr"), 1, "add", "not drawn",
     "the layer camera's window uses the same 1 mm flat gasket (lpbf_low.py)", []),
    ("M0-07", "0", "ports", "FKM O-ring for the LP adapter boss's face seal on the lid (AS568-028 priced; size it to the groove)",
     ("p1", "O1-b"), 1, "add", "not drawn", "the layer camera's adapter uses a 2-030 on a groove of ID 42", []),
    ("M0-08", "0", "purge", "Needle valve for the LW slide purge, brass, 1/8 NPT", ("p1", "O2"), 1, "add", "not drawn", "", []),
    ("M0-09", "0", "purge", "Push-to-connect elbow, 1/4 in. tube x 1/8 NPT", ("p1", "O2-a"), 2, "add", "not drawn", "", []),
    ("M0-10", "0", "purge", "Push-to-connect tee, 1/4 in. tube (off the argon line)", ("p1", "O2-e"), 1, "add", "not drawn", "", []),
    ("M0-11", "0", "purge", "Polyurethane tube 1/4 in. OD, per ft", ("p1", "O2-c"), 10, "add", "not drawn", "", []),
    ("M0-12", "0", "purge", "SAE-4 (7/16-20) x 1/8 in. tube fitting, bored through, 316, with a 1/8 in. 316 tube bent and flattened as the nozzle",
     ("est", 40.0, 70.0, "estimate (Swagelok-class; not fetched)", "SS-200-1-4ST class, bored through", "Swagelok distributor"), 1,
     "add (replaces a machined nozzle)", "not drawn", "the frame's SAE-4 purge port and its Ø4 passage are programmed (cam_monitoring.json)", []),
    ("M0-13", "0", "custom (outsourced)", "LW window clamp ring, 6061 1/4 in. plate, Ø56, ID 31, 4 x Ø4.5",
     ("custom", 14.01, "analogue: SendCutSend laser, the 3/8 in. spacer ring, $14.01 (outsourcing-quotes.csv)"), 1, "outsource", "not drawn",
     "4.6 h on a lathe and mill in house (hours_monitoring.csv)", []),
    ("M0-14", "0", "custom (outsourced)", "BW window clamp frame, 6061 3/16 in. plate, ~76 x 46 with a 53 x 22 opening, 3 x Ø4.5",
     ("custom", 14.01, "analogue: SendCutSend laser, the spacer ring, $14.01"), 1, "outsource", "not drawn", "", []),
    ("M0-15", "0", "custom (outsourced)", "Cover-slide holders (LW on the left liner; LP), 316 sheet clips",
     ("custom", 22.85, "analogue: OSH Cut, a 316 liner, $22.85"), 2, "outsource with the liners", "not drawn", "", []),
    ("M0-16", "0", "fasteners", "M4 x 12 socket-head screws, A4 stainless, for the clamp ring and frame (7)",
     ("est", 5.0, 12.0, "estimate (not fetched)", "M4 x 12 A4 SHCS", "McMaster-Carr"), 1, "add", "not drawn", "", []),
    # ---------------- step 1: clock and recorder -----------------------------------------------------------------------
    ("M1-01", "1", "recorder", "Digitizer: PicoScope 4444, 4 differential inputs, 12/14-bit, 20 MHz, 400 MS/s, 256 MS memory",
     ("p2", "D1"), 1, "add", "not drawn",
     "Pico sells it with at least one probe; for single-ended BNC sources (photodiodes, AE preamp, laser gate, sync) use TA271 D9-BNC "
     "adaptors (M1-02). Pico's own store showed GBP 1,115 (~$1,460). Kit with 3 PicoConnect 441 + 1 TA271: $1,985 (3 in stock)",
     ["D1-u1"]),
    ("M1-02", "1", "recorder", "Pico TA271 D9-to-BNC single-ended adaptor", ("p2", "D1-c"), 4, "add", "not drawn", "", []),
    ("M1-03", "1", "recorder", "BNC M-M RG-58 cables, 48 in.", ("p1", "O3"), 6, "add", "not drawn", "", []),
    ("M1-04", "1", "recorder", "BNC tee F-M-F (sync line to the digitizer and the cameras)", ("p1", "O4"), 2, "add", "not drawn", "", []),
    ("M1-05", "1", "sync", "D-sub 25 to terminal block, DIN rail (the RTC6's extension port to the sync wiring)", ("p1", "O5"), 1, "add",
     "not drawn", "the RTC6's digital I/O comes with the board (SCANLAB: no separate I/O board price, quote-only)", []),
    ("M1-06", "1", "sync", "4-channel digital isolator boards, 5 V TTL (camera triggers and layer marks, isolated from the RTC6)",
     ("p1", "O6"), 2, "add", "not drawn", "functional isolation only; needs an isolated 5 V on the far side", []),
    ("M1-07", "1", "sync", "Sync breakout box: enclosure, 8 BNC bulkheads, 5 V isolated DC-DC",
     ("est", 40.0, 90.0, "estimate (not fetched)", "enclosure + BNC bulkheads", "various"), 1, "add (hand-drilled, 2.4 h)", "not drawn", "", []),
    ("M1-08", "1", "storage", "Data storage, 4 TB SSD (a fully instrumented build is 0.1-1 TB raw, monitoring.md §5.3)",
     ("est", 250.0, 400.0, "estimate (not fetched)", "4 TB NVMe/USB SSD", "various"), 1, "add", "not drawn", "", []),
    # ---------------- step 2: spectral check (borrow) -------------------------------------------------------------------
    ("M2-01", "2", "borrow", "Stabilised tungsten-halogen lamp 360-2600 nm (reference price; borrow)", ("p1", "R2"), 0, "borrow", "-", "", []),
    ("M2-02", "2", "borrow", "Compact spectrometer 200-1000 nm (reference price; borrow)", ("p1", "R1-b"), 0, "borrow", "-",
     "CCS200/M is superseded by CCT10", []),
    ("M2-03", "2", "borrow", "NIR spectrometer 900-1650 nm (reference price; borrow, or ask SCANLAB for the coating curve)",
     ("p1", "R3"), 0, "borrow", "-", "", []),
    # ---------------- step 3: layer camera tuned -------------------------------------------------------------------------
    ("M3-01", "3", "layer camera", "12 mm C-mount lens, f/1.8-16, 2/3 in. format (to run the Pi HQ at f/2-2.8)", ("p1", "L3"), 1,
     "add (replaces optics-bom O20's estimate)", "Layer camera (Pi HQ + C-mount lens)",
     "rated for 2.74 um pixels: softer than the Pi HQ's 1.55 um at pixel level. Edmund 86-570 (1.1 in., high resolution) is $835; "
     "Computar M1214-MP2 ($181.35) is softer still", []),
    ("M3-02", "3", "layer light", "White LED bar light 300 mm, 24 V, behind the back-wall window (raking light)", ("p1", "I5-a"), 1,
     "add (replaces optics-bom O23's estimate)", "not drawn",
     "constant-on; switch it from the PLC to fire the lights in turn. The strobe-capable L300 is $995.40", []),
    ("M3-03", "3", "layer light", "M12 4-pin cable 5 m for the light", ("p1", "I6-c"), 1, "add", "not drawn", "", []),
    ("M3-04", "3", "layer light", "Second (steep) light by the camera: 285 mm industrial LED strip, 12-30 V",
     ("p1", "I6"), 1, "add", "not drawn", "price from a search snippet (page did not render); a $20-60 LED bar also works", []),
    ("M3-05", "3", "layer light", "Two-channel 24 V switching for the lights (MOSFET or relay module on PLC outputs)",
     ("est", 15.0, 40.0, "estimate (not fetched)", "2-ch 24 V module", "various"), 1, "add", "not drawn", "", []),
    # ---------------- step 4: acoustic emission ---------------------------------------------------------------------------
    ("M4-01", "4", "AE", "AE sensor, high-temperature broadband (MISTRAS D9215 class; Seleznev 2022's sensor)",
     ("p2", "A1", ("est", 700.0, 1800.0, "quote-only; estimate, inside Edison's $1-3k for sensor + preamp (monitoring.md §4)",
                   "D9215 (or WSa / R15a)", "MISTRAS (quote)")), 1,
     "add", "not drawn", "quote-only; Edison r8-ae-waveguide: D9215 under the plate with Molykote 41 is the proven set-up at 200 C",
     ["A1-u2", "A1-u3"]),
    ("M4-02", "4", "AE", "AE preamplifier 20/40/60 dB (MISTRAS 2/4/6 class)",
     ("p2", "A2", ("est", 300.0, 900.0, "quote-only; estimate, inside Edison's $1-3k for sensor + preamp", "2/4/6 (or 0/2/4)",
                   "MISTRAS (quote)")), 1, "add", "not drawn",
     "a 28 V phantom-powered preamp needs a decoupler to feed the PicoScope (M4-03); MISTRAS's 5 V PreAmp One (eBay $449.95, new) "
     "runs from USB power", ["A2-u4", "A2-u5", "A2-u1"]),
    ("M4-03", "4", "AE", "Preamp power / decoupling box (28 V phantom to a plain BNC input)",
     ("p2", "A5", ("est", 0.0, 400.0, "estimate: $0 with a 5 V USB-powered preamp (MISTRAS PreAmp One), up to ~$400 for a decoupler",
                   "decoupler or none", "MISTRAS / Vallen (quote)")), 1, "add", "not drawn", "", []),
    ("M4-04", "4", "AE", "High-temperature couplant, Molykote 41 (to 288 C)", ("p1", "A3"), 1, "add", "not drawn", "", []),
    ("M4-05", "4", "AE", "Pencil leads 0.5 mm 2H for Hsu-Nielsen breaks (plus any 0.5 mm pencil)", ("p1", "A4"), 2, "add", "not drawn",
     "a Nielsen shoe is quote-only from AE suppliers; a PTFE guide ring made here does the same", []),
    ("M4-06", "4", "AE", "Waveguide option: 316 rod Ø2 mm x 1 ft (Edison: 1.5-2 mm, 150-250 mm, 10-20 N preload)", ("p1", "A1-a"), 1,
     "option", "not drawn", "", []),
    ("M4-07", "4", "AE", "Waveguide option: compression spring 302 SS for the preload", ("p1", "A2"), 2, "option", "not drawn", "", []),
    ("M4-08", "4", "AE", "SMA-to-BNC cable 48 in. (sensor or preamp to the digitizer)", ("p1", "O3-d"), 1, "add", "not drawn", "", []),
    ("M4-09", "4", "custom (outsourced)", "AE sensor clamp on the rod end, 6061 plate + spring",
     ("custom", 27.12, "analogue: SendCutSend laser, the 1/2 in. Z lift arm, $27.12"), 1, "outsource", "not drawn", "", []),
    # ---------------- step 5: two-colour coaxial ----------------------------------------------------------------------------
    ("M5-01", "5", "coaxial", "Second Si switchable-gain photodiode, 350-1100 nm", ("p1", "P1"), 1, "add", "not drawn",
     "0 in US stock at fetch ('Lead Time')", []),
    ("M5-02", "5", "coaxial", "Long-pass dichroic 805 nm, 25 x 36 mm (splits the 700 / 950 nm pair; the cube takes rectangles only)",
     ("p1", "D1-b"), 1, "add", "not drawn", "Ø1 in. DMLP805 is $331.76 but CM1-DCH/M takes only 25 x 36 mm optics", []),
    ("M5-03", "5", "coaxial", "30 mm cage cube with removable dichroic mount (cube 3)", ("p1", "C1"), 1, "add", "not drawn", "", []),
    ("M5-04", "5", "coaxial", "Band-pass 700 nm, 10 nm FWHM, Ø25 mm (pyrometer band 1)", ("p1", "F1"), 1, "add", "not drawn",
     "700 / 950 nm because 1064 nm galvo coatings block 750-875 nm (Edison r8-coaxial-radiometry; step 2 confirms)", []),
    ("M5-05", "5", "coaxial", "Band-pass 950 nm, 10 nm FWHM, Ø25 mm (pyrometer band 2)", ("p1", "F10"), 1, "add", "not drawn",
     "in stock overseas only: 3-4 week transfer", []),
    ("M5-06", "5", "coaxial", "Achromat f = 50 mm, Ø1 in., 650-1050 nm (onto the second photodiode)", ("p1", "P3"), 1, "add", "not drawn", "", []),
    ("M5-07", "5", "coaxial", "Cage rods 2 in., 4-pack", ("p1", "C2-d"), 2, "add", "not drawn", "", []),
    ("M5-08", "5", "coaxial", "SM1 cage plate CP33/M", ("p1", "C3"), 2, "add", "not drawn", "", []),
    ("M5-09", "5", "coaxial", "SM1 lens tube 1 in.", ("p1", "C4"), 2, "add", "not drawn", "", []),
    ("M5-10", "5", "coaxial", "SM1 retaining rings", ("p1", "C6-b"), 4, "add", "not drawn", "", []),
    ("M5-11", "5", "coaxial", "BNC cable 48 in.", ("p1", "O3"), 1, "add", "not drawn", "", []),
    # ---------------- step 6: coaxial camera ---------------------------------------------------------------------------------
    ("M6-01", "6", "coaxial camera", "Monochrome IMX296 global-shutter board for the Pi 5 (C/CS mount)", ("p2", "K2"), 1, "add", "not drawn",
     "at 950 nm a colour IMX296 (Raspberry Pi Global Shutter Camera, $50-55, often out of stock) sees nearly alike in all its colour "
     "pixels, so it can stand in after a flat-field", []),
    ("M6-02", "6", "coaxial camera", "Tube lens: achromat f = 75 mm, Ø1 in., 650-1050 nm (~7.4 um/px at the plate)", ("p1", "P3-b"), 1,
     "add", "not drawn", "", []),
    ("M6-03", "6", "coaxial camera", "Camera band: 950 nm, 10 nm FWHM (850 nm FBH850-10 if step 2 shows the scan head passes it)",
     ("p1", "F10"), 1, "add", "not drawn", "NIST's 850 nm band sits in the 750-875 nm stop band of standard galvo coatings", []),
    ("M6-04", "6", "coaxial camera", "50:50 plate beamsplitter 25 x 36 mm, 700-1100 nm (cube 2: camera branch)", ("p1", "D2-d"), 1, "add",
     "not drawn", "a plate splitter, not a dichroic: the camera and the pyrometer share 950 nm", []),
    ("M6-05", "6", "coaxial camera", "30 mm cage cube with removable dichroic mount (cube 2)", ("p1", "C1"), 1, "add", "not drawn", "", []),
    ("M6-06", "6", "coaxial camera", "SM1-to-C-mount adapter (external C-mount, internal SM1)", ("p1", "C5"), 1, "add", "not drawn", "", []),
    ("M6-07", "6", "coaxial camera", "SM1 lens tube 3 in. (tube lens to sensor)", ("p1", "C4-d"), 1, "add", "not drawn", "", []),
    ("M6-08", "6", "coaxial camera", "30 mm cage XY translator (centres the camera on the beam)", ("p1", "C7"), 1, "option", "not drawn",
     "0 in US stock at fetch", []),
    ("M6-09", "6", "coaxial camera", "Pi 5 camera cable 22-to-15-pin, 500 mm", ("p2", "K4"), 1, "add", "not drawn",
     "the Pi 5 in PB2 has two camera ports: the layer camera and this one", []),
    ("M6-10", "6", "custom (outsourced)", "Camera adapter plate (IMX296 board on a 30 mm cage plate)",
     ("custom", 10.0, "estimate: SendCutSend laser, small 1/8 in. 6061 part"), 1, "outsource or print", "not drawn", "", []),
    # ---------------- step 7: side high-speed camera, and the steep lid camera ------------------------------------------------
    ("M7-01", "7", "side camera", "Kron Chronos 2.1-HD, 8 GB, mono (4/3 in. sensor, 1920 x 1080 at 1,000 fps, 640 x 96 at 24,046 fps)",
     ("p2", "K5"), 1, "add", "Side high-speed camera (overlay only, render_monitoring.py)",
     "10 % anniversary sale price (regular $6,800); 16 GB $6,480, 32 GB $7,110; 1-3 business days. Two BNC trigger inputs / "
     "frame-strobe outputs and an isolated trigger on its AUX port; REST API", ["K5-u2", "K5-u1"]),
    ("M7-02", "7", "side camera", "Lens for full frame on the 4/3 in. sensor: Nikon F 50 mm f/1.8 (the camera takes F, EF, MFT or C mounts)",
     ("p2", "K8"), 1, "add", "not drawn", "2/3 in. C-mount lenses cover only the 640 x 96 crop", []),
    ("M7-03", "7", "side camera", "Longer lens: Nikon F 85 mm f/1.8 or a 105 mm macro (16 um/px class at 24 kfps)", ("p2", "K8-a"), 1,
     "add", "not drawn", "C-mount alternative for the cropped modes: Computar M7528-MP 75 mm, $246 (2/3 in.)", []),
    ("M7-04", "7", "side camera", "Band-pass 810 nm, 10 nm FWHM, Ø25 mm (with the 808 nm light)", ("p1", "F4"), 1, "add", "not drawn", "", []),
    ("M7-05", "7", "side camera", "Short-pass 950 nm (OD > 4 at 1070 nm), Ø25 mm, in front of the Chronos", ("p1", "F7"), 1, "add",
     "not drawn", "every camera needs OD >= 4-6 at 1070 nm (monitoring.md §6)", []),
    ("M7-06", "7", "side light", "810 nm mounted LED, 810 mW min, with a T-Cube driver and supply",
     ("p1", "I1"), 1, "add", "not drawn", "LED: no laser class. In stock overseas only. Driver LEDD1B $380.04 + KPS201 $43.15 (M7-07)", []),
    ("M7-07", "7", "side light", "LED driver 1.2 A (LEDD1B) + its 15 V supply (KPS201)", ("p1", "I2"), 1, "add", "not drawn",
     "+ KPS201 $43.15", []),
    ("M7-08", "7", "side light", "Alternative: 808 nm 0.8 W diode module with TTL (hobby grade, IEC Class 4, no interlock)",
     ("p1", "I4"), 0, "option (LSO review needed)", "not drawn", "freezes motion better than the LED; needs the LSO's approval", []),
    ("M7-09", "7", "side camera", "Kron BNC extension cable 4 m (trigger to the sync box)", ("p2", "D6"), 1, "add", "not drawn", "", []),
    ("M7-10", "7", "custom (outsourced)", "LW camera bracket, 6061 plate under a ball head",
     ("custom", 27.12, "analogue: SendCutSend laser, the Z lift arm, $27.12"), 1, "outsource", "not drawn", "", []),
    ("M7-11", "7", "steep lid camera", "Option: IMX296 board for the lid port (LP)", ("p2", "K2"), 1, "option", "not drawn", "", []),
    ("M7-12", "7", "steep lid camera", "Option: 50 mm C-mount lens f/2.8, 2/3 in. (11.4 um/px over ~17 x 15 mm)", ("p1", "L1-b"), 1,
     "option", "not drawn", "sale price (regular $450)", []),
    ("M7-13", "7", "steep lid camera", "Option: Raspberry Pi 5, 4 GB (the PB2 Pi's two camera ports are taken)", ("p2", "K3-b"), 1, "option",
     "not drawn", "", []),
    ("M7-14", "7", "custom (outsourced)", "Option: LP adapter boss (compound angle), SendCutSend CNC",
     ("custom", 379.48, "analogue: SendCutSend CNC, the layer camera's viewport adapter + boss, $379.48"), 1, "option", "not drawn",
     "7.1 h in house with a sine plate on the rotary (hours.csv)", []),
    ("M7-15", "7", "steep lid camera", "Option: LP window, UV fused silica Ø25.4 x 3 mm, uncoated (on the boss, square to the sight line)",
     ("p1", "W3-e"), 1, "option", "not drawn", "Edmund 25-310 (VIS-NIR AR, $120, 1 in stock) cuts the ghost reflections", []),
    ("M7-16", "7", "steep lid camera", "Option: LP cover slides, fused silica Ø24.4 x 2 mm (laser-head protective glass), 6 to start",
     ("p1", "W5-c"), 6, "option (consumable)", "not drawn",
     "6+ price $37.19 each; Edmund 19-837 Ø25 x 1 mm is $86. With a Ø37 bore in the lid the slide must sit in the boss or grow to Ø40-42", []),
    # ---------------- step 8: cooling through solidification -------------------------------------------------------------------
    ("M8-01", "8", "InGaAs coaxial", "InGaAs switchable-gain photodiode 800-1700 nm", ("p1", "P2"), 1, "add (route A)", "not drawn", "", []),
    ("M8-02", "8", "InGaAs coaxial", "Notch dichroic: reflects 1064 nm at 45 deg, transmits 350-1015 and 1140-1600 nm, 25 x 36 mm "
     "(replaces the DMSP1000, which reflects 1020-1550 nm back toward the laser)", ("p1", "D4"), 1, "add (route A)", "not drawn",
     "pulsed damage rating only (1 J/cm2 at 532 nm, 10 ns): ask Semrock for a CW rating at 1070 nm before it carries 500 W", []),
    ("M8-03", "8", "InGaAs coaxial", "Band-pass 1550 nm, 12 nm FWHM", ("p1", "F5"), 1, "add (route A)", "not drawn", "", []),
    ("M8-04", "8", "InGaAs coaxial", "NIR ND filter OD 2, SM1 mounted (pool brightness)", ("p1", "F9-b"), 1, "add (route A)", "not drawn", "", []),
    ("M8-05", "8", "InGaAs coaxial", "30 mm cage cube for the notch dichroic", ("p1", "C1"), 1, "add (route A)", "not drawn", "", []),
    ("M8-06", "8", "SWIR camera", "Route B: SWIR camera 640 x 512 class, InGaAs, GigE, hardware trigger (LUCID Triton TRI003S-WC)",
     ("p2", "K6-c"), 0, "option (route B)", "not drawn",
     "Edmund's price; LUCID's own page now hides prices (a search snippet showed $5,650). Alvium 1800 U-030 VSWIR: $7,600",
     ["K6-u8", "K6-u5", "K6-u2"]),
    ("M8-07", "8", "SWIR camera", "Route B: 50 mm SWIR C-mount lens 900-1700 nm", ("p1", "L4"), 0, "option (route B)", "not drawn", "", []),
]


def load(path):
    return {r["key"]: r for r in csv.DictReader(open(path))} if pathlib.Path(path).exists() else {}


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p1", default="/tmp/fab-e/prices/p1.csv")
    ap.add_argument("--p2", default="/tmp/fab-e/prices/p2.csv")
    a = ap.parse_args()
    src = {"p1": load(a.p1), "p2": load(a.p2)}
    for k, p in (("p1", a.p1), ("p2", a.p2)):  # keep the lookups next to the BOM
        if pathlib.Path(p).exists():
            LOOK[k].write_text(pathlib.Path(p).read_text())
    rows, missing = [], []
    for (rid, step, group, element, s, qty, action, in_model, notes, used_keys) in SEL:
        r = dict(id=rid, step=step, group=group, element=element, part_number="", vendor="", qty=qty, unit_low_usd=None,
                 unit_high_usd=None, ext_low_usd=None, ext_high_usd=None, price_basis="", url="", fetched_utc="", stock_lead="",
                 used_unit_usd=None, used_url="", used_fetched_utc="", used_condition="", action=action, in_model=in_model, notes=notes)
        if s[0] in ("p1", "p2"):
            lk = src[s[0]].get(s[1])
            fb = s[2] if len(s) > 2 else None          # a labelled estimate for a quote-only or unread line
            if lk is None or num(lk.get("unit_usd")) is None:
                basis = lk.get("basis") if lk else "not reached"
                r.update(part_number=(lk or {}).get("part_number", ""), vendor=(lk or {}).get("vendor", ""),
                         price_basis=("quote-only" if basis == "quote-only" else "not priced (%s)" % basis),
                         url=(lk or {}).get("url", ""), fetched_utc=(lk or {}).get("fetched_utc", ""),
                         stock_lead=(lk or {}).get("stock_or_lead", ""))
                if fb:
                    _, lo, hi, fbasis, pn, vendor = fb
                    r.update(unit_low_usd=lo, unit_high_usd=hi, price_basis=fbasis, part_number=r["part_number"] or pn,
                             vendor=r["vendor"] or vendor)
                if lk and lk.get("notes"):
                    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + lk["notes"][:300]
                missing.append(rid)
            else:
                u = num(lk["unit_usd"])
                r.update(part_number=lk["part_number"], vendor=lk["vendor"], unit_low_usd=u, unit_high_usd=u,
                         price_basis={"fetched": "fetched (list price)", "search-snippet": "search snippet (page did not show it)"}
                         .get(lk["basis"], lk["basis"]), url=lk["url"], fetched_utc=lk["fetched_utc"], stock_lead=lk["stock_or_lead"])
                if lk.get("price_note"):
                    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + "price: " + lk["price_note"][:160]
        elif s[0] == "est":
            _, lo, hi, basis, pn, vendor = s
            r.update(unit_low_usd=lo, unit_high_usd=hi, price_basis=basis, part_number=pn, vendor=vendor)
        elif s[0] == "custom":
            _, usd, basis = s
            r.update(unit_low_usd=usd, unit_high_usd=usd, price_basis=basis, part_number="custom (hours_monitoring.csv)",
                     vendor="SendCutSend / OSH Cut (analogue)", url="outsourcing-quotes.csv", fetched_utc="2026-11-22")
        # cheapest used listing
        best = None
        for uk in used_keys:
            lk = src["p2"].get(uk) or src["p1"].get(uk)
            if lk and num(lk.get("unit_usd")) is not None and (best is None or num(lk["unit_usd"]) < num(best["unit_usd"])):
                best = lk
        if best:
            r.update(used_unit_usd=num(best["unit_usd"]), used_url=best["url"], used_fetched_utc=best["fetched_utc"],
                     used_condition="%s: %s (%s)" % (best["stock_or_lead"], best["item"][:90], best["part_number"][:40]))
        if r["unit_low_usd"] is not None:
            r["ext_low_usd"] = round(r["unit_low_usd"] * qty, 2)
            r["ext_high_usd"] = round(r["unit_high_usd"] * qty, 2)
        rows.append(r)
    # totals per step: new (low, high); with the used listings taken where one exists (the cheapest; else the new low).
    # Options (action "option ..."), borrowed instruments and notes are left out and summed apart.
    def counted(r):
        return r["qty"] and not r["action"].startswith(("option", "borrow", "note"))

    tot = {}
    for st in STEPS:
        rs = [r for r in rows if r["step"] == st and counted(r)]
        lo = sum(r["ext_low_usd"] or 0 for r in rs)
        hi = sum(r["ext_high_usd"] or 0 for r in rs)
        used = sum((r["used_unit_usd"] * r["qty"]) if r["used_unit_usd"] is not None else (r["ext_low_usd"] or 0) for r in rs)
        q = [r["id"] for r in rs if r["unit_low_usd"] is None]
        est = [r["id"] for r in rs if "estimate" in (r["price_basis"] or "")]
        opts = [r for r in rows if r["step"] == st and r["action"].startswith("option")]
        tot[st] = dict(what=STEPS[st], new_low=round(lo, 2), new_high=round(hi, 2), with_used=round(used, 2), unpriced=q,
                       estimated=est, options=[r["id"] for r in opts],
                       options_usd=round(sum((r["unit_low_usd"] or 0) * (r["qty"] or 1) for r in opts), 2),
                       options_used_usd=round(sum(((r["used_unit_usd"] if r["used_unit_usd"] is not None else (r["unit_low_usd"] or 0))
                                                   * (r["qty"] or 1)) for r in opts), 2))
    cum = cum_used = 0.0
    trows = []
    for st, t in tot.items():
        cum += t["new_low"]
        cum_used += t["with_used"]
        t["cumulative_new_low"], t["cumulative_with_used"] = round(cum, 2), round(cum_used, 2)
        trows.append(dict(id="TOTAL-%s" % st, step=st, group="total", element="Step %s, %s: new $%s-%s; with used listings $%s%s%s"
                          % (st, t["what"], f"{t['new_low']:,.2f}", f"{t['new_high']:,.2f}", f"{t['with_used']:,.2f}",
                             ("; options not counted (%s): $%s new, $%s used" % (", ".join(t["options"]), f"{t['options_usd']:,.2f}",
                                                                                f"{t['options_used_usd']:,.2f}")) if t["options"] else "",
                             ("; not priced: " + ", ".join(t["unpriced"])) if t["unpriced"] else ""),
                          ext_low_usd=t["new_low"], ext_high_usd=t["new_high"], used_unit_usd=t["with_used"],
                          price_basis="sum of the counted lines; estimates in it: %s" % (", ".join(t["estimated"]) or "none"),
                          notes="cumulative after this step: new (low) $%s, with used listings $%s" % (f"{cum:,.2f}", f"{cum_used:,.2f}")))
    fields = list(rows[0].keys())
    with open(BOM, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows + trows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k, "")) for k in fields})
    (OUT / "bom_totals.json").write_text(json.dumps(dict(steps=tot, missing=missing), indent=1))
    for st, t in tot.items():
        print(st, t)
    print("missing", missing)


if __name__ == "__main__":
    main()
