"""Build desktop-lpbf/monitoring-bom.csv: the bought parts for monitoring.md §4's steps 0-8 (issue #260, PR 281).

Prices are list prices read on the vendors' own pages through the lab tunnel on 2026-11-25 (the lookups, with URL, UTC time,
stock or lead time and notes, are analysis/out/monitoring/fab/price_lookups_optics.csv and price_lookups_cameras.csv), used
listings read on eBay the same way, the closest instant quotes already in the repo for the custom parts
(hours_monitoring.csv), or labelled estimates. Nothing is a quote for this machine, and nothing was ordered.

Columns follow optics-bom.csv, plus the step (0-8 of monitoring.md §4), extended prices, stock or lead time, and the used
option. Totals per step: new (low / high) and with the used options taken where a listing exists.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/build_bom.py [--p1 CSV] [--p2 CSV] [--mo optics-parts.csv]
     (defaults: the committed lookups and desktop-lpbf/monitoring/optics-parts.csv, the optics worker's file)
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[2]
OUT = D / "analysis" / "out" / "monitoring" / "fab"
BOM = D / "monitoring-bom.csv"
LOOK = {"p1": OUT / "price_lookups_optics.csv", "p2": OUT / "price_lookups_cameras.csv"}
SCSQ = "analysis/out/monitoring/fab/quotes/sendcutsend_quotes.csv"
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
     "on the boss's face O-ring and screws)", ("custom", 11.44, "SendCutSend instant quote (2 = $9.15, 10 = $7.21 each; arrives Nov 30)",
                                              SCSQ, "2026-11-25T07:49Z"), 1,
     "outsource", "not drawn", "monitoring_spec: the LP ships blanked; its window and slides come with the steep camera (M7-17, M7-18)", []),
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
     ("custom", 9.83, "SendCutSend instant quote (2 = $7.86, 10 = $6.68 each; arrives Nov 30)", SCSQ, "2026-11-25T07:45Z"), 1,
     "outsource", "not drawn", "4.6 h on a lathe and mill in house (hours_monitoring.csv)", []),
    ("M0-14", "0", "custom (outsourced)", "BW window clamp frame, 6061 3/16 in. plate, ~76 x 49 with a 53 x 22.5 opening, 3 x Ø4.5",
     ("custom", 9.87, "SendCutSend instant quote (2 = $7.89, 10 = $6.18 each; arrives Nov 30)", SCSQ, "2026-11-25T07:47Z"), 1,
     "outsource", "not drawn", "the quoted outline is a stand-in: it needs fitting above the frame's bottom edge", []),
    ("M0-15", "0", "custom (outsourced)", "Cover-slide holders (LW on the left liner; LP), 316 sheet clips",
     ("custom", 22.85, "analogue: OSH Cut, a 316 liner, $22.85"), 2, "outsource with the liners", "not drawn", "", []),
    ("M0-17", "0", "coax safety (now)", "Beam trap on cube 1's far port, 30 mm cage, 5 W CW (the DMSP1000 passes 0.3-0.6 W of the "
     "forward beam)", ("tl", "BTC30"), 1, "add now", "not drawn",
     "optics-parts.csv MO2 (optics worker): a Class 4 stray beam exists today wherever cube 1's -y face is open; it estimated $100-200 "
     "for a BTC30-class trap", []),
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
    ("M1-09", "1", "recorder", "Alternative digitizer: NI USB-6366, 8 simultaneous 16-bit inputs at 2 MS/s each", ("p2", "D3"), 1,
     "option (alternative to M1-01)", "not drawn", "NI shows a 16-17 week lead time; confirm the BNC variant before ordering",
     ["D3-u1", "D3-u2"]),
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
    ("M3-06", "3", "layer camera", "Second 1070 nm blocker behind the FESH0950 (for video during lasing)", ("mo", "MO38"), 1, "add",
     "Layer camera (Pi HQ + C-mount lens)", "", []),
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
    # ---------------- step 5: two-colour coaxial (the optics worker's parts: monitoring/optics-parts.csv) -------------------
    ("M5-01", "5", "coaxial", "Shared 1070 nm blocker after cube 1: short-pass 1000 nm (replaces the NF1064-44, which would cut 700 nm)",
     ("mo", "MO3"), 1, "add", "not drawn", "", []),
    ("M5-02", "5", "coaxial", "Cube 3 dichroic: long-pass 805 nm, Ø1 in. (reflects < 790 nm to photodiode A, passes > 825 nm to B)",
     ("mo", "MO5"), 1, "add", "not drawn", "", []),
    ("M5-03", "5", "coaxial", "Photodiode A band: 700 nm, 40 nm FWHM", ("mo", "MO6"), 1, "add", "not drawn", "", []),
    ("M5-04", "5", "coaxial", "Photodiode B band: 900 nm, 40 nm FWHM", ("mo", "MO7"), 1, "add", "not drawn", "", []),
    ("M5-05", "5", "coaxial", "Photodiode B, Si switchable gain (A is the existing optics-bom O15)", ("mo", "MO8"), 1, "add", "not drawn",
     "my read 2026-11-25T06:44Z: 0 in US stock, 'Lead Time' (price_lookups_optics.csv P1)", []),
    ("M5-06", "5", "coaxial", "Photodiode lens f = 50 mm achromat (one exists as O18)", ("mo", "MO9"), 1, "add", "not drawn", "", []),
    ("M5-07", "5", "coaxial", "Field stops, 500 um pinholes, one per photodiode", ("mo", "MO10"), 2, "add", "not drawn", "", []),
    ("M5-08", "5", "coaxial", "30 mm cage cube for a round Ø1 in. dichroic (C4W + B4C/M + FFM1): cube 3", ("mo", "MO14"), 1, "add",
     "not drawn", "CM1-DCH/M ($205.91) takes only 25 x 36 mm optics", []),
    ("M5-09", "5", "coaxial", "Cage plates, rods and lens tubes for the branch (typical counts)", ("mo", "MO15"), 1, "add", "not drawn", "", []),
    ("M5-10", "5", "coaxial", "BNC cable 48 in. (photodiode B to the digitizer)", ("p1", "O3"), 1, "add", "not drawn", "", []),
    # ---------------- step 6: coaxial camera -------------------------------------------------------------------------------------
    ("M6-01", "6", "coaxial camera", "Cube 2 dichroic: short-pass 950 nm, Ø1 in. (reflects 955-990 nm to the camera)", ("mo", "MO4"), 1, "add",
     "not drawn", "the camera band sits above the galvo coatings' 750-875 nm stop band", []),
    ("M6-02", "6", "coaxial camera", "Monochrome IMX296 board for the Pi 5 (C/CS mount, trigger input)", ("mo", "MO11"), 1, "add", "not drawn",
     "the Raspberry Pi Global Shutter Camera (colour) was out of stock at all five resellers checked", []),
    ("M6-03", "6", "coaxial camera", "Tube lens f = 75 mm achromat (7.4 um/px)", ("mo", "MO12"), 1, "add", "not drawn", "", []),
    ("M6-04", "6", "coaxial camera", "Second 1070 nm blocker in the camera arm (short-pass 1000 nm)", ("mo", "MO13"), 1, "add", "not drawn", "", []),
    ("M6-05", "6", "coaxial camera", "30 mm cage cube for a round Ø1 in. dichroic: cube 2", ("mo", "MO14"), 1, "add", "not drawn", "", []),
    ("M6-06", "6", "coaxial camera", "SM1-to-C-mount adapter (external C-mount, internal SM1) for the camera", ("p1", "C5"), 1, "add", "not drawn",
     "not in optics-parts.csv", []),
    ("M6-07", "6", "coaxial camera", "Pi 5 camera cable 22-to-15-pin, 500 mm", ("p2", "K4"), 1, "add", "not drawn",
     "the Pi 5 in PB2 has two camera ports: the layer camera and this one", []),
    ("M6-08", "6", "coaxial camera", "30 mm cage XY translator (centres the camera on the beam)", ("p1", "C7"), 1, "option", "not drawn",
     "0 in US stock at fetch", []),
    ("M6-09", "6", "custom (outsourced)", "Camera adapter plate (IMX296 board on a 30 mm cage plate)",
     ("custom", 10.0, "estimate: SendCutSend laser, small 1/8 in. 6061 part (the three parts quoted today were $9.83-11.44)"), 1,
     "outsource or print", "not drawn", "", []),
    # ---------------- step 7: side high-speed camera, and the steep lid camera ---------------------------------------------------
    ("M7-01", "7", "side camera", "Kron Chronos 2.1-HD, 8 GB, mono (4/3 in. sensor; 24,046 fps at 640 x 96)", ("mo", "MO26"), 1, "add",
     "Side high-speed camera (overlay only, render_monitoring.py)",
     "Kron's page also showed a 10 % anniversary sale, $6,120 for 8 GB, at 2026-11-25T06:58Z (price_lookups_cameras.csv K5); 1-3 "
     "business days. Two BNC trigger inputs / frame-strobe outputs, an isolated AUX trigger, a REST API", ["K5-u2", "K5-u1"]),
    ("M7-02", "7", "side camera", "50 mm C-mount lens focusing at 176 mm (MOD 100 mm), 400-1000 nm coating", ("mo", "MO27"), 1, "add",
     "not drawn", "2/3 in. image circle: it covers the cropped high-rate modes, not the 4/3 in. sensor's full 19.2 x 10.8 mm frame "
     "(for full frame see M7-09)", []),
    ("M7-03", "7", "side camera", "Camera filter: 850 nm, 10 nm FWHM", ("mo", "MO28"), 1, "add", "not drawn", "", []),
    ("M7-04", "7", "side camera", "Second 1070 nm blocker (short-pass 1000 nm)", ("mo", "MO29"), 1, "add", "not drawn", "", []),
    ("M7-05", "7", "side light", "850 nm LED, 2.7 W minimum, through LP or BW", ("mo", "MO30"), 1, "add", "not drawn", "", []),
    ("M7-06", "7", "side light", "LED driver with pulse mode", ("mo", "MO31"), 1, "add", "not drawn",
     "my reads: an 810 nm mounted LED (M810L5, $304.15) with an LEDD1B ($380.04) costs a sixth of this pair but gives less light", []),
    ("M7-07", "7", "side camera", "Kron BNC extension cable 4 m (trigger to the sync box)", ("p2", "D6"), 1, "add", "not drawn", "", []),
    ("M7-08", "7", "custom (outsourced)", "LW camera bracket, 6061 plate under a ball head",
     ("custom", 27.12, "analogue: SendCutSend laser, the Z lift arm, $27.12"), 1, "outsource", "not drawn", "", []),
    ("M7-09", "7", "side camera", "Option: full-frame lens, Nikon F 50 mm f/1.8G (order the Chronos with the F mount)", ("p2", "K8"), 1, "option",
     "not drawn", "a G lens has no aperture ring: check that Kron's F mount sets the aperture, or buy the D version", ["K8-u1"]),
    ("M7-10", "7", "side light", "Option: 808 nm 10 W fibre-coupled source, pulses from 10 us (Class 4: LSO review first)", ("mo", "MO32"), 1,
     "option", "not drawn", "", []),
    ("M7-11", "7", "side camera", "Option: Chronos 1.4 (1 us minimum exposure)", ("mo", "MO33"), 1, "option", "not drawn",
     "my read: $4,050 for 8 GB on the 10 % sale (price_lookups_cameras.csv K5-c)", []),
    ("M7-12", "7", "steep lid camera", "Option: monochrome IMX296 board for the lid port (LP)", ("mo", "MO35"), 1, "option", "not drawn", "", []),
    ("M7-13", "7", "steep lid camera", "Option: 50 mm C-mount lens, MOD 100 mm", ("mo", "MO36"), 1, "option", "not drawn", "", []),
    ("M7-14", "7", "steep lid camera", "Option: filters, 850 nm 10 nm bandpass + 1070 nm short-pass", ("mo", "MO37"), 1, "option", "not drawn", "", []),
    ("M7-15", "7", "steep lid camera", "Option: Raspberry Pi 5, 4 GB (the PB2 Pi's two camera ports are taken)", ("p2", "K3-b"), 1, "option",
     "not drawn", "", []),
    ("M7-16", "7", "custom (outsourced)", "Option: LP adapter boss (compound angle), SendCutSend CNC",
     ("custom", 379.48, "analogue: SendCutSend CNC, the layer camera's viewport adapter + boss, $379.48"), 1, "option", "not drawn",
     "7.1 h in house with a sine plate on the rotary (hours.csv)", []),
    ("M7-17", "7", "steep lid camera", "Option: LP window, UV fused silica Ø25.4 x 3 mm, uncoated (on the boss, square to the sight line)",
     ("p1", "W3-e"), 1, "option", "not drawn", "Edmund 25-310 (VIS-NIR AR, $120, 1 in stock) cuts the ghost reflections", []),
    ("M7-18", "7", "steep lid camera", "Option: LP cover slides, fused silica Ø24.4 x 2 mm (laser-head protective glass), 6 to start",
     ("p1", "W5-c"), 6, "option (consumable)", "not drawn",
     "6+ price $37.19 each; Edmund 19-837 Ø25 x 1 mm is $86. With a Ø37 bore in the lid the slide must sit in the boss or grow to Ø40-42", []),
    # ---------------- step 8: cooling through solidification -------------------------------------------------------------------
    ("M8-01", "8", "InGaAs coaxial", "Route A: InGaAs photodiode behind the DMSP1000 (1625-1725 nm leaks through it at 3-30 %)",
     ("mo", "MO16"), 1, "add (route A)", "not drawn", "", []),
    ("M8-02", "8", "InGaAs coaxial", "Route A: two 1070 nm blockers, long-pass 1250 nm", ("mo", "MO17"), 2, "add (route A)", "not drawn", "", []),
    ("M8-03", "8", "InGaAs coaxial", "Route A: lens f = 100 mm, 1050-1700 nm AR, and a 1.0 mm pinhole", ("mo", "MO18"), 1, "add (route A)",
     "not drawn", "", []),
    ("M8-04", "8", "InGaAs coaxial", "Route A: fourth cube in the camera arm with a ~1180 nm dichroic (DMLP1180 / DMSP1180 class)",
     ("mo", "MO19", ("est", 602.50, 602.50, "estimate from optics-parts.csv MO19's note: a Ø1 in. dichroic $331.76 + a cube $270.74",
                     "DMLP1180 / DMSP1180 class + cube", "Thorlabs")), 1, "add (route A)", "not drawn",
     "curve not read: check it splits 955-990 nm from 1600-1750 nm", []),
    ("M8-05", "8", "InGaAs coaxial", "Route A: the shared FESH1000 moves into the two Si photodiode arms (it blocks 1550-1650 nm)",
     ("mo", "MO20"), 2, "add (route A)", "not drawn", "", []),
    ("M8-06", "8", "InGaAs coaxial", "Not recommended: notch dichroic NFD01-1064 in place of the DMSP1000 (no CW rating)", ("mo", "MO23"), 1,
     "option (not recommended)", "not drawn", "", []),
    # route B, the optics worker's choice (monitoring/optics.md §0 item 6): the SWIR camera in the coaxial camera arm, in place of
    # the IMX296, working off the 1600-1750 nm the DMSP1000 lets through and the DMSP950 reflects into that arm
    ("M8-07", "8", "SWIR camera", "Route B: coaxial SWIR camera in the camera arm (Alvium 1800 U-030 VSWIR, IMX991 InGaAs, 5 um)",
     ("mo", "MO21"), 1, "option (route B)", "not drawn",
     "optics.md §0 item 6: sees ~860 K at 500 us (core saturated) and 990-1,030 K with the core in range; replaces the IMX296 "
     "(M6-02) in the arm", []),
    ("M8-08", "8", "SWIR camera", "Route B: tube lens f = 100 mm, 1050-1700 nm AR (8 um/px)", ("mo", "MO22"), 1, "option (route B)",
     "not drawn", "", []),
    ("M8-09", "8", "SWIR camera", "Route B: two 1070 nm blockers, long-pass 1250 nm, in front of the SWIR camera", ("mo", "MO17"), 2,
     "option (route B)", "not drawn", "the same part as route A's M8-02", []),
    # route C, monitoring.md §2.3's first idea: an off-axis SWIR camera through the LW window (no used Alvium was found; this
    # class has used listings)
    ("M8-10", "8", "SWIR camera", "Route C: off-axis SWIR camera at LW, 640 x 512 class, InGaAs, GigE, hardware trigger (LUCID Triton TRI003S-WC)",
     ("p2", "K6-c"), 1, "option (route C)", "not drawn",
     "Edmund's price; LUCID's own pages now hide prices (a search snippet showed $5,650)",
     ["K6-u5", "K6-u7", "K6-u8"]),
    ("M8-11", "8", "SWIR camera", "Route C: 50 mm SWIR C-mount lens 900-1700 nm", ("p1", "L4"), 1, "option (route C)", "not drawn", "", []),
    ("M8-12", "8", "SWIR camera", "Route C: NIR ND filter OD 2, SM1 mounted (the pool is ~240x brighter than 600 C metal at 1.55 um)",
     ("p1", "F9-b"), 1, "option (route C)", "not drawn", "", []),
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
    # the committed lookups by default; pass fresh lookup files (same columns) to re-price, and they are copied next to the BOM
    ap.add_argument("--p1", default=str(LOOK["p1"]))
    ap.add_argument("--p2", default=str(LOOK["p2"]))
    ap.add_argument("--mo", default=str(D / "monitoring" / "optics-parts.csv"),
                    help="the optics worker's coaxial, side and lid camera parts (prices taken from it, not re-read)")
    a = ap.parse_args()
    src = {"p1": load(a.p1), "p2": load(a.p2), "mo": {r["id"]: r for r in csv.DictReader(open(a.mo))} if pathlib.Path(a.mo).exists() else {},
           "tl": {r["part_number"]: r for r in csv.DictReader(open(OUT / "stock_reads_thorlabs.csv"))}
           if (OUT / "stock_reads_thorlabs.csv").exists() else {}}
    # stock or lead time by part number, from every read (Thorlabs stock reads first, then the two lookup files)
    stock = {}
    for k in ("p2", "p1"):
        for lk in src[k].values():
            pn = (lk.get("part_number") or "").split(" (")[0].strip()
            if pn and lk.get("stock_or_lead") and num(lk.get("unit_usd")) is not None:
                stock.setdefault(pn, "%s (%s)" % (lk["stock_or_lead"][:60], lk["fetched_utc"]))
    for t in src["tl"].values():
        stock[t["part_number"]] = "%s (%s)" % (t["stock_or_lead"], t["fetched_utc"])
    stock["Chronos 2.1-HD"] = stock.get("CR21-1.0-8M-FNL", "in stock; lead time 1-3 business days (Kron store, 2026-11-25T06:58Z)")
    stock["CAM-IMX296RAW (mono)"] = "add to cart shown, stock not stated (inno-maker.com, 2026-11-25)"
    for k, p in (("p1", a.p1), ("p2", a.p2)):  # keep the lookups next to the BOM
        if pathlib.Path(p).exists() and pathlib.Path(p).resolve() != LOOK[k].resolve():
            LOOK[k].write_text(pathlib.Path(p).read_text())
    rows, missing = [], []
    for (rid, step, group, element, s, qty, action, in_model, notes, used_keys) in SEL:
        r = dict(id=rid, step=step, group=group, element=element, part_number="", vendor="", qty=qty, unit_low_usd=None,
                 unit_high_usd=None, ext_low_usd=None, ext_high_usd=None, price_basis="", price_source="", url="", fetched_utc="",
                 stock_lead="",
                 used_unit_usd=None, used_url="", used_fetched_utc="", used_condition="", action=action, in_model=in_model, notes=notes)
        if s[0] == "tl":
            t = src["tl"].get(s[1])
            r.update(part_number=t["part_number"], vendor="Thorlabs", unit_low_usd=num(t["list_usd"]), unit_high_usd=num(t["list_usd"]),
                     price_basis="fetched (list price)", price_source="stock_reads_thorlabs.csv " + s[1], url=t["url"],
                     fetched_utc=t["fetched_utc"], stock_lead=t["stock_or_lead"])
        elif s[0] == "mo":
            mo = src["mo"].get(s[1])
            fb = s[2] if len(s) > 2 else None
            if mo is None:
                r.update(price_basis="not reached (optics-parts.csv %s missing)" % s[1])
                missing.append(rid)
            else:
                r.update(part_number=mo["part_number"], vendor=mo["vendor"], url=mo["url"], fetched_utc=mo["fetched_utc"],
                         price_source="optics-parts.csv %s (optics worker)" % s[1])
                u = num(mo["unit_usd"])
                est = re.findall(r"\$?([0-9][0-9,.]*)\s*-\s*\$?([0-9][0-9,.]*)", mo["price_basis"])
                if u is not None:
                    r.update(unit_low_usd=u, unit_high_usd=u, price_basis=mo["price_basis"])
                elif est:
                    r.update(unit_low_usd=num(est[0][0]), unit_high_usd=num(est[0][1]), price_basis=mo["price_basis"])
                elif fb:
                    _, lo, hi, fbasis, pn, vendor = fb
                    r.update(unit_low_usd=lo, unit_high_usd=hi, price_basis=fbasis)
                else:
                    r.update(price_basis=mo["price_basis"] or "not priced")
                    missing.append(rid)
                if mo.get("notes"):
                    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + "optics-parts.csv: " + mo["notes"][:240]
        elif s[0] in ("p1", "p2"):
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
                    r.update(unit_low_usd=lo, unit_high_usd=hi, price_basis=fbasis, part_number=r["part_number"] or pn, price_source="estimate (quote-only)",
                             vendor=r["vendor"] or vendor)
                if lk and lk.get("notes"):
                    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + lk["notes"][:300]
                missing.append(rid)
            else:
                u = num(lk["unit_usd"])
                r["price_source"] = ("price_lookups_optics.csv " if s[0] == "p1" else "price_lookups_cameras.csv ") + s[1]
                r.update(part_number=lk["part_number"], vendor=lk["vendor"], unit_low_usd=u, unit_high_usd=u,
                         price_basis={"fetched": "fetched (list price)", "search-snippet": "search snippet (page did not show it)"}
                         .get(lk["basis"], lk["basis"]), url=lk["url"], fetched_utc=lk["fetched_utc"], stock_lead=lk["stock_or_lead"])
                if lk.get("price_note"):
                    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + "price: " + lk["price_note"][:160]
        elif s[0] == "est":
            _, lo, hi, basis, pn, vendor = s
            r.update(unit_low_usd=lo, unit_high_usd=hi, price_basis=basis, part_number=pn, vendor=vendor, price_source="estimate")
        elif s[0] == "custom":
            if len(s) > 3:   # an instant quote for this part
                _, usd, basis, url, when = s
                r.update(unit_low_usd=usd, unit_high_usd=usd, price_basis="quote (instant, online): " + basis,
                         price_source="quotes/sendcutsend_quotes.csv",
                         part_number="custom (flat_parts_dxf.py)", vendor="SendCutSend", url=url, fetched_utc=when,
                         stock_lead="arrives as soon as Mon Nov 30")
            else:            # the closest instant quote for a similar part (outsourcing-quotes.csv, 2026-11-22)
                _, usd, basis = s
                r.update(unit_low_usd=usd, unit_high_usd=usd, price_basis=basis, part_number="custom (hours_monitoring.csv)",
                         price_source="hours_monitoring.csv (analogue quote)",
                         vendor="SendCutSend / OSH Cut (analogue)", url="outsourcing-quotes.csv", fetched_utc="2026-11-22")
        if r["price_source"].startswith("optics-parts.csv") and not r["stock_lead"]:
            parts_ = [x.strip() for x in re.split(r"\s\+\s|,", r["part_number"]) if x.strip()]
            got = ["%s: %s" % (x, stock[x]) for x in parts_ if x in stock]
            if got:
                r["stock_lead"] = "; ".join(got)
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
