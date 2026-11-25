"""Completeness audit: every part in the model against its purchase record (issue #260).

Reads the model's own BOM tags as its part list (since 2026-11-25; mass and material from analysis/out/mass.json, written by
analysis/mass_budget.py, where the names match) (analysis/out/audit/model_tags.json: each part's `bom` line, `mcm` part number, material and tags, dumped from
cad/lpbf_low.build() by `--dump-tags`). Maps every part to a bom.csv line and to a row in the part-number lists, or to
the custom-part list (analysis/out/machining/hours.csv and the sheet parts of cad/render_build.kind()), and gives it one
status:

  real part priced     a real part number, with a price read from a vendor (a purchase-list row or a fetched/quoted BOM line)
  real part unpriced   a real part number (vendor and model named), no price published or read
  generic              no part number: an envelope, a "class" part, or a line that is only an estimate
  custom               machined, sheet, welded or printed by the lab; its stock and work are in a BOM line
  missing from BOM     no bom.csv line covers it (it may still be in robot-tooling.csv, safety-parts.csv, ...)
  inconsistent         the model and the BOM (or another analysis) disagree on what the part is
  excluded             not a purchase part (the powder in the reservoir)

It also lists the reverse: bom.csv lines and purchase-list rows that no model part maps to.

Usage (from the repo root):
  python desktop-lpbf/analysis/audit/completeness.py [extra.csv ...]          # current bom.csv
  python desktop-lpbf/analysis/audit/completeness.py --bom OLD.csv --no-audit-prices --tag before
  python desktop-lpbf/analysis/audit/completeness.py --dump-tags SNAPSHOT_REPO  # rebuild model_tags.json (CadQuery)

Extra CSVs (e.g. electrical-bom.csv, optics-bom.csv) are read as purchase lists: any part number in a row is indexed,
with its price if a price column is found. Outputs: analysis/out/audit/model_vs_bom[_TAG].csv, purchase_vs_model[_TAG].csv,
summary[_TAG].json, and (current run only) the tables in desktop-lpbf/completeness-audit.md below its hand-written head
(analysis/audit/completeness-head.md).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import pathlib
import re
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parent.parent
OUT = LPBF / "analysis" / "out" / "audit"

MCM = re.compile(r"\b\d{4,5}[A-Z]\d{1,4}\b")
DASH = re.compile(r"\b2-(\d{3})\b")
PLACEHOLDER = re.compile(r"^(?:[A-Z]+|[A-Z0-9]+_[A-Z0-9_]+)$")   # 'TSLOT', 'KF40_WELD' ... are model placeholders, not PNs

STATUSES = ["real part priced", "real part unpriced", "generic", "custom", "missing from BOM", "inconsistent", "excluded"]

# ------------------------------------------------------------------ explicit map for parts whose name has no part number
# (name regex, bom line, keyword the line must contain to cover the part, kind override, part numbers, note)
# kind: 'custom' (machined/sheet/weld), 'generic' (no part number), 'bought' (pn given), 'excluded', None (automatic)
MAP = [
    (r"^19 in\. rack frame", "S9", r"\brack\b", "generic", [], "12U open frame, 560 mm tall: not chosen (StarTech 4POSTRACK12U class, price not shown)"),
    (r"^Rack side panels", "S9", r"side panel", "custom", [], "vented sheet panels"),
    (r"^UPS \(Eaton 5PX1500RTG2", "D2", r"5PX1500RTG2", "bought", ["5PX1500RTG2"], "model tag is C6 (controls enclosure), which has no UPS"),
    (r"^Fiber laser source", "L1", r"YLR-500", "bought", ["YLR-500-U3-SM-AC"], ""),
    (r"^Process fiber", "L1", r"YLR-500", "bought", ["YLR-500-U3-SM-AC"], "comes fitted to the laser"),
    (r"^Scan \+ laser controller PC", "C1", r"\bPC\b|industrial PC|computer", "generic", [], "C1 is the RTC6 card; no 2U PC is chosen"),
    (r"^DIN-rail drawer", "C6", r"drawer", "generic", [], "contents in C3, C4, S1, C2"),
    (r"^Chamber legs", "G1", r"\blegs?\b", "custom", [], ""),
    (r"^Z mounting flange", "M3", r"flange", "custom", [], ""),
    (r"^Z actuator body|^Z carriage", "M3", r"actuator", "bought", ["KR2602A-0110-0-01A0"], "the carriage is part of the actuator"),
    (r"^Z bracket \+ fold-back belt", "M3", r"belt", "custom", [], ""),
    (r"^Z servo|^Recoater servo", "M2", r"ClearPath", "bought", ["CPM-SDSK-2311S-RLN"], ""),
    (r"^Z lift arm", "M3", r"lift arm", "custom", [], ""),
    (r"^Pot magnet", "B2", r"magnet", "bought", ["5679K95"], "heat.md: swap the NdFeB cup for SmCo"),
    # since 2026-11-23 the rod end is a 316L block with seven Solid Sealing weld-ins (electrical.md 13.3); they replace the hermetic connector
    # and its O-ring, and there is no thermal cutoff (13.4). This entry comes before B1's "^Rod end M50", which would take the weld-ins as custom.
    (r"^Rod end M50 feedthroughs, welded in", "H1", r"FA11631", "bought", ["FA11631", "FA11632", "FA10443"],
     "3 x FA11631 + 3 x FA11632 single-lead type K and 1 x FA10443 4-pin power per module: electrical-bom.csv E6-01..03"),
    (r"^Build module M50|^Module M50 bottom flange|^Module M50 handle|^Build plate M50|^Piston head M50|^Hollow piston rod M50|^Rod end M50",
     "B1", r"module", "custom", [], ""),
    (r"^Plate rim wiper M50|^Bore seal M50", "B2", r"wiper|felt", "generic", [], "carbon-filled PTFE / aramid felt: no stock part number chosen"),
    (r"^Heater block M50", "H1", r"heater", "custom", [], ""),
    (r"^Cartridge heaters M50", "H1", r"3714N36", "bought", ["3714N36"], ""),
    (r"^Type K thermocouples M50", "H1", r"3871K606", "bought", ["3871K606"], ""),
    (r"^Macor standoff rings", "H1", r"8489K75", "custom", ["8489K75"], "cut from 8489K75 rod"),
    (r"^Radiation shields M50", "H1", r"2317K275|shim", "custom", ["2317K275"], ""),
    (r"^Striker disc M50", "B2", r"striker|416", "custom", ["89095K23"], ""),
    (r"^Overflow funnel block", "M4", r"overflow", "custom", [], ""),
    (r"^Overflow port \(KF-40", "G7", r"5786N25|weld", "bought", ["5786N25"], "KF-40 weld stub cut to 42 mm (round 5)"),
    (r"^Overflow jar \(KF-40", "M4", r"cup|half nipple", "custom", ["4518K42"], "KF-40 flange (4518K42 half nipple cut to 6 mm) welded into a 316L cup (rounds 5-6)"),
    (r"^Zero-point clamping modules", "B3", r"[Zz]ero-point", "bought", ["1460874"], "SCHUNK NSE-HT mini 88-20 V1 (round 6, B3)"),
    (r"^Overflow clamp \(KF-40", "G7", r"100318805|toggle|KF-40", "bought", ["100318805"], "MKS 100318805 KF-40 toggle clamp (round 5)"),
    (r"present sensor \(inductive M12|^Drawer-closed sensor|^Reservoir-docked sensor", "A1", r"PAM-AP-1H", "bought", ["PAM-AP-1H"], ""),
    (r"^Process chamber body", "G1", r"through-frame|5-1/2 in\.|5\.5 in\.", "custom", [], ""),
    (r"^Chamber floor plate", "G1", r"floor plate", "custom", [], ""),
    (r"^(Floor|Lid) O-ring \(FKM 75A, 3\.53 mm cord", "G8", r"96515K127|0\.139", "bought", ["96515K127"], ""),
    (r"^Door O-ring \(FKM 75A 1\.78 mm cord", "G8", r"96515K123|0\.070 in\.", "bought", ["96515K123"], ""),
    (r"^Cross-flow (inlet|outlet) plenum", "G1", r"plenum", "custom", [], "model tag G4 (blower), which does not cost them"),
    (r"^(Inlet|Outlet) plenum port \(KF-25\)|^Vacuum port \(KF-25", "G7", r"5786N23|weld ports", "bought", ["5786N23"], ""),
    (r"^Vacuum port adapter plate", "G1", r"adapter plate|port adapter", "custom", [], "machined 304; not in analysis/out/machining/hours.csv"),
    (r"^Layer-light LED bar", "M6", r"LED", "generic", [], ""),
    (r"^Lift-out wall liner", "A2", r"2317K278|liner", "custom", ["2317K278"], ""),
    (r"^Plate-height through-beam", "A1", r"E32-T61-S", "bought", ["E32-T61-S"], ""),
    (r"^Recoater carriage block|^Recoater arm|^Recoater feedthrough spacer|^Recoater floating bearing|^Recoater motor (standoff|bracket)",
     "M1", r"recoater", "custom", [], ""),
    (r"^Blade holder", "M5", r"holder", "custom", [], ""),
    (r"^Recoater fixed bearing: magnetic-fluid", "M1", r"Ferrotec|magnetic-fluid", "bought", ["SFL-006-NN"], ""),
    (r"^Recoater shaft coupling", "M1", r"coupling", "generic", [], ""),
    (r"^Chamber lid \(", "G1", r"\blid\b", "custom", [], ""),
    (r"^Window flange|^Window retaining ring|^Camera viewport adapter|^Camera window retaining ring", "G1", r"window flange|viewport", "custom", [], ""),
    (r"^Cover-slide drawer \(", "G1", r"cover-slide drawer", "custom", [], ""),
    (r"^Gas knife", "G1", r"gas knife", "custom", [], ""),
    (r"^Door handle$", "G1", r"door handle", "custom", [], ""),
    (r"^Hinge pins", "G1", r"pins", "custom", [], ""),
    # round 6 (2026-11-25, optics worker): the window and the cover slide are drawn as the BOM's Edmund parts
    (r"^Ø2 in\. fused-silica window", "L7", r"38-990", "bought", ["38-990"], "Edmund 38-990, Ø50.8 x 9.53 mm (optics-bom.csv O11)"),
    (r"^Window clamp ring|^Camera window flat ring", "G8", r"seal-parts|FKM sheet", "generic", [], "FKM sheet: part number not confirmed (seal-parts.csv)"),
    (r"^Field-stop aperture|^f-theta adapter ring|^Galvo riser plate|^Enclosed beam tube|^Optics bridge", "F5", r"optics bridge", "custom", [], ""),
    (r"^Cover slide \(", "A2", r"36-299", "bought", ["36-299"], "Edmund 36-299, Ø50 x 2 mm (optics-bom.csv O12)"),
    (r"^Drawer latches: 2 x quarter-turn|^Drawer latch receptacles", "G1", r"quarter-turn", "generic", [], "seals.md: no catalogue quarter-turn latch fits the 20 mm plate"),
    (r"^Dose chute", "M4", r"chute|dosing", "custom", [], ""),
    (r"^Metering base \(", "M4", r"metering", "custom", [], ""),
    (r"^NFC reader antenna", "A1", r"Adafruit 364", "bought", ["364"], ""),
    (r"^Dovetail rails for the reservoirs", "R1", r"reservoir", "custom", [], "machined 316L; not in hours.csv"),
    (r"^Roller shaft: magnetic-fluid", "M4", r"Ferrotec|SSL-005", "bought", ["SSL-005-NN"], ""),
    (r"^Roller drive coupling", "M4", r"coupling", "generic", [], ""),
    (r"^Side reservoir port \(KF-16", "R1", r"KF-16", "generic", [], "KF-16 blank: no part number"),
    (r"^Reservoir M \(|^Reservoir M shutter|^Reservoir M lid with", "R1", r"reservoir", "custom", [], ""),
    (r"^Reservoir M powder", "", "", "excluded", [], "powder feedstock, not a machine part"),
    (r"^Load cell \(single-point", "A1", r"ALLUE3", "bought", ["ALLUE3"], ""),
    (r"^Layer camera \(Pi HQ", "M6", r"HQ camera", "bought", ["4561"], ""),
    (r"^Camera window \(Ø1 in\.", "M6", r"camera window|blocking", "generic", ["FESH0950", "FESH0900"], "no BOM line has a Ø1 in. window with a 1070 nm blocking coating (optics-bom.csv O21 proposes a plain window + a Thorlabs short-pass filter)"),
    (r"^Pressure transducer \(7/16-20", "G7", r"3861N11", "bought", ["3861N11"], ""),
    (r"^Module-cooling fan", "H3", r"fan", "bought", ["1939K12"], ""),
    (r"^Overpressure relief valve \(316", "G7", r"relief", "bought", ["RELIEF316"], ""),
    (r"^Chamber door \(", "G1", r"\bdoor\b", "custom", [], ""),
    (r"^Draw-latch brackets on the door", "G1", r"\bdoor\b", "custom", [], "two 6061 brackets that carry the latches on the door (2026-11-23)"),
    (r"^Reservoir [SML] pull tab", "R1", r"reservoir|hopper", "custom", [], "6061 fin, extends the lid handle (2026-11-23)"),
    (r"^Door hinge", "G1", r"hinge", "custom", [], ""),
    (r"^Draw latches on the door|^Draw-latch strikes", "G1", r"1807A61", "bought", ["1807A61"], ""),
    (r"^f-theta lens, f = 160", "L6", r"FTH", "bought", ["FTH160-1064"], ""),
    (r"^2-axis galvo scan head", "L5", r"basiCube", "bought", ["basiCube 20"], ""),
    (r"^Safety shutter \+ beam dump", "L4", r"shutter", "generic", [], "no shutter chosen (L4: quote)"),
    (r"^Collimator \(IPG", "L3", r"IPG.{0,40}collimator", "generic", [], "custom-diameter IPG collimator: not priced by IPG yet"),
    (r"^Dry scroll pump", "G2", r"pump", "bought", ["A73501983"], ""),
    (r"^Pump inlet \(KF-25\)", "G2", r"NW25|4518K49|flare", "bought", ["4518K49"], "the nXDS6i inlet is NW25; only the 4396K21 alternative needs a flare-to-NPT adapter + 4518K49"),
    (r"^Sealed cyclone \+ HEPA housing", "G5", r"5169K72", "bought", ["5169K72"], "cyclone stage not chosen"),
    (r"^(Filter|Blower) (inlet|outlet) \(KF-25\)", "G7", r"KF-25", "generic", [], "adapters to the filter's 1/2 NPSC ports / the blower not chosen"),
    (r"^Sealed side-channel blower", "G4", r"blower", "generic", [], "no gas-tight blower of this size found (real-parts.md)"),
    (r"^Trace O2 analyzer \+ dew-point", "G6", r"Microx", "bought", ["Microx"], "dew-point transmitter is line G9"),
    (r"^Argon solenoid manifold", "G7", r"8077K237", "bought", ["8077K237"], "custom manifold block not costed"),
    (r"^Argon pressure regulator", "G3", r"78595A5", "bought", ["78595A5"], ""),
    (r"^Vacuum isolation valve", "G7", r"4123K45", "bought", ["4123K45"], ""),
    (r"^Gas-loop \+ vacuum hoses", "G7", r"3497N23", "bought", ["3497N23"], "real-parts.md: routed lengths not matched to the 24 in. hose"),
    (r"^Argon line \(1/4 in\. 316L\)", "G7", r"89785K824", "bought", ["89785K824"], ""),
    (r"^O2 sample line \(1/8 in\.", "G7", r"1/8 in\.", "generic", [], ""),
    (r"^Guard frame \(20 mm T-slot\)", "S9", r"T-slot", "bought", ["5537T101"], ""),
    (r"^Laser guard panels", "S9", r"panel", "custom", ["88895K51"], "cut from 5052 sheet"),
    (r"^Sliding guard door", "S9", r"sliding", "custom", [], ""),
    (r"^Guard door rail", "S9", r"sliding|roller", "bought", ["5537T353"], "rails are the frame's own 20 mm T-slot; McMaster 5537T353 rollers"),
    (r"^OD 7\+ viewing window", "S5", r"LW1P1|OD", "bought", ["LW1P1/M"], ""),
    (r"^Guard-locking door switch", "S2", r"D4JL", "bought", ["D4JL-4NFA-C5-NPT"], ""),
    (r"^Operator panel box", "S4", r"operator (box|panel)|panel box|enclosure|box", "custom", [], ""),
    (r"^E-stop$", "S3", r"XA1E", "bought", ["XA1E-BV3U02-R"], ""),
    (r"^Key switch$", "S4", r"6749K3", "bought", ["6749K3"], ""),
    (r"^Emission indicator$", "S4", r"7545K316", "bought", ["7545K316"], ""),
    (r"^Reset button$", "S4", r"6749K201", "bought", ["6749K201"], ""),
    (r"^Tray dock \(CombiTac", "D1", r"CombiTac", "bought", ["COMBITAC"], ""),
    (r"^Umbilical duct", "D1", r"duct", "custom", [], ""),
    (r"^Chilled-water supply", "D1", r"chilled", "generic", [], ""),
    (r"^Argon supply from the dock", "D1", r"argon", "generic", [], ""),
    (r"^Pump exhaust to the dock", "D1", r"exhaust", "generic", [], ""),
    (r"^Leveling mounts", "F3", r"5537T983", "bought", ["5537T983"], ""),
    (r"^Base plate, (process|gas) module", "F4", r"MIC-6", "custom", [], ""),
    (r"^Guard-door handle for the robot|^Door drive bracket|^Door drive shaft and disc|^Drawer latch wing head|^Blade-cartridge grip fin|^AprilTag plates|^Liner pull tab",
     "A3", r"guard-door handle|wing heads|AprilTag", "custom", [], ""),
    (r"^Door drive: pneumatic rotary actuator", "A3", r"CDRQ2|CRQ2", "bought", ["CDRQ2BS20-180"], ""),
    (r"^Draw-latch actuators", "A3", r"CDQ2|CQ2", "bought", ["CDQ2B20-15DZ-F7PS"], ""),
    (r"^Rail-hole bonded seal washers", "G8", r"bonded", "generic", [], "Dowty-type M4 washer: no part number chosen"),
    (r"^HSS recoater blade", "M5", r"blade", "bought", ["2634T15"], "cut from M2 HSS sheet"),
]

# ------------------------------------------------------------------ model vs BOM checks: (name regex, check(bom, ctx) -> note or "")
def _t(bom, i):
    return bom.get(i, {}).get("_text", "")


RULES = [
    (r"^Dry scroll pump", lambda b, c: "" if "scroll" in b.get("G2", {}).get("candidate", "").lower() else
     "model draws a dry scroll pump; G2's candidate is the McMaster 4396K21 rotary-vane pump (tray_budget.md also uses 4396K21)"),
    (r"^Sealed side-channel blower \(gas-tight, ~100 L/min\)", lambda b, c:
     "model label says ~100 L/min; the CFD needs 140-200 L/min at 1.5-3 kPa (gas-flow.md, G4 spec)" if "140" in _t(b, "G4") else ""),
    (r"^Chilled-water supply", lambda b, c: "model runs chilled water to the laser; the quoted IPG YLR-500-U3-SM-AC is air-cooled (L2), "
     "and heat.md says decide water vs air first" if re.search(r"air[- ]cooled", _t(b, "L2"), re.I) else ""),
    (r"^UPS \(Eaton", lambda b, c: "model draws an Eaton 5PX1500RTG2; analysis/out/tray/tray_budget.md sizes the UPS as a Vertiv GXT5LI-1500"
     if "GXT5LI" in c["tray"] else ""),
    (r"^f-theta lens, f = 160", lambda b, c: "" if "160" in _t(b, "L6") else
     "model uses f = 160 mm (Thorlabs FTH160-1064, $1,011.78 in vendor-lookups.csv); L6 still specifies f = 254 mm"),
    (r"^Collimator \(IPG, 5 mm beam", lambda b, c: "" if re.search(r"3\.2 mm", _t(b, "L3")) else
     "low-profile.md §2: f = 160 mm needs a ~3.2 mm beam for the 75 um spot; the model and L3 keep IPG's 5 mm collimator (sized for f = 254 mm; ~48 um at f = 160)"),
    (r"^19 in\. rack frame \(11U", lambda b, c: "model draws an 11U rack 515 mm tall; S9's McMaster 7648K62 cabinet is 10U (no catalogue 11U rack that low was found)"
     if "10U" in _t(b, "S9") else ""),
    (r"^Guard frame \(20 mm", lambda b, c: "" if "20 mm" in _t(b, "S9") else "model draws 20 mm T-slot; S9 lists 30 mm 5537T97 for the old cabinet"),
    (r"^Sliding guard door|^Guard door rail", lambda b, c: "" if re.search(r"slid", _t(b, "S9"), re.I) else
     "model's guard door slides; S9 lists rail-to-rail hinges (5537T847) for a swinging door"),
    (r"^Z actuator body|^Z carriage", lambda b, c: "" if re.search(r"actuator", _t(b, "M3"), re.I) else
     "model draws an integrated actuator; M3 lists a 6638K11 ball screw on a 6709K33 rail for the tall model's piston"),
    (r"^Process chamber body|^Chamber floor plate|^Chamber lid \(|^Chamber door \(", lambda b, c:
     "G1 still describes the tall model's welded 1/2 in. 89155K135 box" if re.search(r"Welded 1/2 in", _t(b, "G1")) else ""),
    (r"^(Floor|Lid) O-ring \(FKM 75A|^Door O-ring \(FKM 75A", lambda b, c:
     "model uses FKM 75A cord; G8 lists 0.070 in. 90A cord 1165N11" if ("90A" in _t(b, "G8") and "75A" not in _t(b, "G8")) else ""),
    (r"^Door hinge", lambda b, c: "model labels the hinge McMaster 1151A87 but draws custom 304 knuckles; the real 1151A87 is a 3 x 3 in. "
     "two-leaf lift-off hinge (real-parts.md)" if c["mcm"] == "1151A87" else ""),
    (r"^Radiation shields M50 \(2 x 0\.3 mm", lambda b, c: "model's shields are 0.3 mm; H1's 2317K275 shim is 0.005 in. (0.13 mm)"
     if "2317K275" in _t(b, "H1") else ""),
    (r"^Overpressure relief valve \(316 SS", lambda b, c: "" if re.search(r"316[^,;]*relief|relief[^,;]*316", _t(b, "G7"), re.I) else
     "model's relief is 316 SS with an FKM seat on an SAE-4 port; G7 lists the nylon/Buna-N 4277T52 (low-profile.md §3 says replace it)"),
    (r"^Pressure transducer \(7/16-20 SAE-4", lambda b, c: "" if "SAE" in _t(b, "G7") else
     "lid port is SAE-4 (7/16-20); G7's 3861N11 needs an adapter (vendor-parts.csv)"),
    (r"^Rod end M50 feedthroughs, welded in", lambda b, c: "bom.csv H1's spec still says 'potted cable exit'; its candidate column and the model have "
     "the weld-in rod end (electrical.md 13.3)" if re.search(r"potted cable exit", b.get("H1", {}).get("spec", ""), re.I) else ""),
    (r"^Heater block M50|^Cartridge heaters M50", lambda b, c: "bom.csv H1 still buys a thermal cutoff, which the model no longer has (electrical.md 13.4)"
     if re.search(r"RT240", b.get("H1", {}).get("candidate", "")) else ""),
    (r"^Load cell \(single-point, 2 kg", lambda b, c: "model label 2 kg; A1 lists a 3 kg Laumas ALLUE3" if "3 kg" in _t(b, "A1") else ""),
    (r"^O2 sample line \(1/8 in\.", lambda b, c: "" if "1/8 in." in _t(b, "G7") + _t(b, "G6") else
     "model draws a 1/8 in. O2 sample line; G7 lists only 1/4 in. 316 tube (89785K824) for the argon and O2 lines"),
    (r"^DIN-rail drawer", lambda b, c: "" if "drawer" in _t(b, "C6").lower() else
     "model draws a 3U 19 in. DIN-rail drawer; C6 is a McMaster 7812K14 NEMA wall box"),
    (r"^HSS recoater blade", lambda b, c: ("" if "HSS" in b.get("M5", {}).get("candidate", "") else "model blade is HSS; M5 lists 9011K104 18-8 shim (low-profile.md §5)")
     or ("the model's part-number tag is still 9011K104, the 18-8 shim, though the part is named HSS" if c["mcm"] == "9011K104" else "")),
    (r"^Recoater shaft coupling \(clamp type, 6 to 8 mm", lambda b, c: "" if re.search(r"6 mm", _t(b, "M1")) else
     "drawn coupling is 6 to 8 mm (the Ferrotec SFL-006 has a 6 mm shaft); M1 lists 6446K781, 3/8 in. x 8 mm"),
]

# ------------------------------------------------------------------ helpers
def num(x):
    """A price from a cell: 12.5, '$293 (2311S), ...', 'approx. $23k'; None for 'not published', 'quote (BOM L5)'."""
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return None if (isinstance(x, float) and math.isnan(x)) else float(x)
    s = str(x).strip().replace(",", "")
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*$", s) or re.search(r"\$\s*(\d+(?:\.\d+)?)(k?)", s, re.I) or re.match(r"\s*(\d+(?:\.\d+)?)\b", s)
    if not m:
        return None
    v = float(m.group(1))
    if m.lastindex and m.lastindex >= 2 and m.group(2).lower() == "k":
        v *= 1000
    return v


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def kind_of(tag):
    """cad/render_build.kind() on the dumped tags: 'stock', 'sheet', 'fastener', 'context' or 'bought'."""
    n, mat, mcm, tags = tag["part"], tag["mat"], tag["mcm"] or "", tag["tags"]
    if "context" in tags:
        return "context"
    if "fastener" in tags:
        return "fastener"
    sheet_keys = ("inlet plenum +", "outlet plenum under", "liners", "Dose chute", "Gas knife", "Reservoir M (", "Reservoir M shutter",
                  "Radiation shields", "Laser guard panels", "Sliding guard door", "Rack side panels", "Umbilical duct", "Operator panel box")
    if any(k in n for k in sheet_keys):
        return "sheet"
    if mat in ("al6061", "mic6", "macor") and not mcm.startswith(("KF", "9572", "TSLOT", "SHEET")):
        return "stock"
    if "feedthroughs, welded in" in n:
        return "bought"                    # the rod end's Solid Sealing weld-ins (316L sleeves, but bought parts)
    if mat == "ss316l" and any(k in n for k in ("Build module", "bottom flange", "Rod end", "Hollow piston rod", "Overflow funnel")):
        return "stock"
    if "Striker" in n:
        return "stock"
    return "bought"


def dump_tags(snapshot, dest):
    sys.path.insert(0, str(pathlib.Path(snapshot) / "desktop-lpbf" / "cad"))
    import lpbf_low as M  # noqa: E402
    parts = M.build()
    rows = [dict(part=p.name, bom=p.bom, mcm=p.mcm, mat=p.mat, module=p.module, tags=list(p.tags)) for p in parts]
    dest.write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(f"{len(rows)} parts -> {dest}")


# ------------------------------------------------------------------ purchase index
LINK_COLS = ("bom_line", "in_bom", "bom line", "bom.csv line (replaces / adds to)")
PN_COLS = ("part_number", "part number", "part", "product", "candidate", "pn", "mpn", "manufacturer_part_number")
PRICE_COLS = ("unit_price_usd", "price_usd", "price_per_pack_usd", "unit_usd", "unit_low_usd", "price", "unit_price")
BASIS_COLS = ("price_note", "price_basis", "price basis", "part_number", "part number")
ID_COLS = ("id", "line", "key", "bom_line")
WHOLESALE = ("fasteners.csv", "seal-parts.csv")   # no per-row link: covered by the bom line that cites the file


def pns_in(text):
    out = set(MCM.findall(text or ""))
    for m in DASH.finditer(text or ""):
        out.add("2-" + m.group(1))
    for m in re.finditer(r"AS568-(\d{3})", text or ""):
        out.add("2-" + m.group(1))
    return out


def build_index(files, bom):
    """pn -> list of rows {file, id, pn, price, desc, costed_by}."""
    cites = defaultdict(set)
    for i, r in bom.items():
        for f in re.split(r"[;,\s]+", (r.get("source", "") + " " + r.get("price_basis", ""))):
            if f.endswith(".csv"):
                cites[pathlib.Path(f).name].add(i)
    idx, rows_all = defaultdict(list), []
    for path in files:
        name = path.name
        try:
            rows = read_csv(path)
        except Exception as e:  # noqa: BLE001
            print(f"skip {path}: {e}")
            continue
        for k, r in enumerate(rows):
            text = " ".join(str(v) for v in r.values() if v)
            pn_raw = next((r[c] for c in PN_COLS if r.get(c)), "")
            pns = pns_in(pn_raw) | pns_in(text if name in ("vendor-parts.csv",) else pn_raw)
            for tok in re.split(r"\s*(?:[;+]|\s/\s|\bx\d+\b|\(|\))\s*", pn_raw or ""):
                tok = tok.strip()
                if tok and not MCM.fullmatch(tok) and len(tok) >= 3 and not re.search(r"\s{2,}|^(not|each|qty)", tok, re.I) and len(tok) < 40:
                    pns.add(tok)
            for word in re.findall(r"[A-Za-z0-9][A-Za-z0-9./-]{4,}", pn_raw or ""):
                if re.search(r"\d", word) and re.search(r"[A-Za-z]", word):
                    pns.add(word.rstrip(".,"))       # vendor part numbers inside free text ('Eaton 5PX1500RTG2')
            if name == "seal-parts.csv":
                pns |= pns_in(r.get("size", ""))
            price = next((num(r[c]) for c in PRICE_COLS if r.get(c) not in (None, "")), None)
            praw = " ".join(str(r.get(c) or "") for c in PRICE_COLS + BASIS_COLS)
            no_price = price is None and bool(re.search(r"not (published|found|quoted|priced|confirmed|read)|request a quote|no public price", praw + " " + str(r.get("sold_as") or ""), re.I))
            qty = num(r.get("qty", "")) if r.get("qty", "") not in ("", None) else None
            rid = next((r[c] for c in ID_COLS if r.get(c)), f"row{k + 2}")
            link = next((r[c] for c in LINK_COLS if r.get(c)), "")
            costed_by = ""
            lk = re.match(r"\s*([A-Z]{1,2}\d{1,2})\b", link or "")
            if lk and lk.group(1) in bom and not link.lower().startswith("replaces") and (qty is None or qty > 0):
                costed_by = lk.group(1)
            elif name in WHOLESALE and cites.get(name):
                costed_by = sorted(cites[name])[0]
            elif name not in ("mcmaster-parts.csv", "options-mcmaster.csv", "options-vendors.csv", "plate-materials.csv", "audit-prices.csv"):
                for i, b in bom.items():
                    if any(p and len(p) >= 4 and p in b["_text"] for p in pns):
                        costed_by = i
                        break
            if name.endswith("-bom.csv") and not costed_by:
                costed_by = f"{name}:{rid}"   # extra purchase lists (electrical-bom.csv, optics-bom.csv) are their own lines
            desc = next((r[c] for c in ("description_as_listed", "item", "element", "device", "description", "used_for") if r.get(c)), "")
            rec = dict(file=name, id=rid, pns=sorted(pns), price=price, no_price=no_price, qty=qty, desc=desc[:110], costed_by=costed_by,
                       link=(lk.group(1) if lk else ""), used=False)
            rows_all.append(rec)
            for p in pns:
                idx[p.upper()].append(rec)
    return idx, rows_all


def cited_files(r):
    return {pathlib.Path(c).name for c in re.split(r"[;,\s]+", r.get("source", "") + " " + r.get("price_basis", "")) if c.endswith(".csv")}


def reason_for(rec, bom, old=None):
    """Why a purchase row has no model part (a guess from the file, qty and its line's text). `old` is the BOM at the
    start of the audit: a line that cited the file then and does not now has retired the row."""
    f = rec["file"]
    if f == "plate-materials.csv":
        return "plate-material options (study)"
    if f == "assembly-tooling.csv":
        return "tool or fixture"
    if f == "robot-tooling.csv":
        return "robot cell"
    if f == "safety-parts.csv":
        return "room safety, PPE or option"
    if rec["qty"] == 0:
        return "alternative (qty 0)"
    line = rec["link"] if rec["link"] in bom else ""
    if line and f not in WHOLESALE:
        b = bom[line]
        if old and line in old and f in cited_files(old[line]) and f not in cited_files(b):
            return f"stale: line {line} no longer cites {f}"
        for sent in re.split(r"(?<=[.;|])\s+", b.get("notes", "")):
            if any(q in sent for q in rec["pns"]) and re.search(r"no longer|moved to|replaces|replace[ds]? (it|them)|without the", sent, re.I):
                return f"stale: line {line}'s notes retire it"
        if any(q in b.get("alternative", "") for q in rec["pns"]):
            return f"alternative in line {line}"
    if re.search(r"sheet|plate|bar\b|rod\b|tube|tubing|disc|shim|stock", rec["desc"], re.I):
        return "stock for custom parts"
    return ""


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("extra", nargs="*", help="extra purchase CSVs (electrical-bom.csv, optics-bom.csv)")
    ap.add_argument("--bom", default=str(LPBF / "bom.csv"))
    ap.add_argument("--tag", default="")
    ap.add_argument("--no-audit-prices", action="store_true")
    ap.add_argument("--dump-tags", metavar="SNAPSHOT_REPO")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    tags_path = OUT / "model_tags.json"
    if a.dump_tags:
        dump_tags(a.dump_tags, tags_path)
        return

    mass = json.loads((LPBF / "analysis/out/mass.json").read_text())["parts"]
    tags = {t["part"]: t for t in json.loads(tags_path.read_text())}
    # 2026-11-25: the part list is the model's own (model_tags.json, dumped from the current model), not mass.json's, which
    # lags behind renamed and new parts until mass_budget.py is re-run; mass and material still come from mass.json where
    # the name (or its first 40 characters) matches. Context parts (the VLM tray) are not purchases.
    by_name = {p["part"]: p for p in mass}
    mass = []
    for n, tg in tags.items():
        if "context" in tg.get("tags", []):
            continue
        p = by_name.get(n) or next((q for k, q in by_name.items() if k[:40] == n[:40]), None) or {}
        mass.append(dict(part=n, module=p.get("module", tg.get("module", "")), material=p.get("material", tg.get("mat", "")), mass_kg=p.get("mass_kg")))
    bom = {}
    for r in read_csv(a.bom):
        r["_text"] = " ".join(r.get(c, "") for c in ("item", "spec", "candidate", "alternative", "notes"))
        bom[r["id"]] = r
    files = [LPBF / f for f in ("mcmaster-parts.csv", "fasteners.csv", "seal-parts.csv", "vendor-parts.csv", "safety-parts.csv",
                                "robot-tooling.csv", "assembly-tooling.csv", "options-mcmaster.csv", "options-vendors.csv",
                                "plate-materials.csv", "vendor-lookups.csv")]
    if not a.no_audit_prices and (HERE / "audit-prices.csv").exists():
        files.append(HERE / "audit-prices.csv")
    files += [pathlib.Path(x).resolve() for x in a.extra]
    idx, prow = build_index(files, bom)
    machined = {r["part"] for r in read_csv(LPBF / "analysis/out/machining/hours.csv")}
    tray_txt = (LPBF / "analysis/out/tray/tray_budget.md").read_text() if (LPBF / "analysis/out/tray/tray_budget.md").exists() else ""

    out, line_parts = [], defaultdict(list)
    for p in mass:
        n = p["part"]
        t = tags.get(n, dict(part=n, bom="", mcm="", mat="", tags=[]))
        k = kind_of(t)
        mcm = t.get("mcm") or ""
        pns = pns_in(n)
        if mcm and not PLACEHOLDER.match(mcm):
            pns.add(mcm.replace("Ferrotec ", ""))
        entry = next((e for e in MAP if re.search(e[0], n)), None)
        line, kw, kover, note = t.get("bom", ""), None, None, ""
        if entry:
            _, eline, kw, kover, epns, note = entry
            line = eline if eline or kover == "excluded" else line
            pns |= set(epns)
        kind = {"stock": "custom (machined)", "sheet": "custom (sheet)", "fastener": "fastener", "bought": "bought"}.get(k, k)
        if kover == "custom" and kind == "bought":
            kind = "custom (machined)"
        if kover == "excluded":
            kind = "excluded"
        # purchase rows for the part numbers
        hits = []
        first = list(entry[4]) if entry else []
        for q in first + sorted(x for x in pns if x not in first):   # the explicit map's part numbers first
            for rec in idx.get(q.upper(), []):
                hits.append(rec)
                rec["used"] = True
        costed = sorted([h for h in hits if h["costed_by"]], key=lambda h: h["costed_by"] != line)   # the model's own line first
        covered_by = ""
        names_pn = [i for i, b in bom.items() if any(len(q) >= 4 and q in b["_text"] for q in pns)]
        if entry and line in bom and (not kw or re.search(kw, bom[line]["_text"], re.I)):
            covered_by = line                       # explicit map: the line must say it
        elif costed:
            covered_by = costed[0]["costed_by"]     # a purchase row for one of its part numbers is costed by a line
        elif names_pn:
            covered_by = names_pn[0]                # a line names one of its part numbers
        elif not entry and not pns and line in bom:
            covered_by = line                       # no part number, no map: trust the model's tag
        priced_rows = [h for h in costed if h["price"] is not None] or [h for h in hits if h["price"] is not None and covered_by]
        basis = bom.get(covered_by, {}).get("price_basis", "") if covered_by in bom else "extra list"
        bom_names_pn = covered_by in bom and any(len(q) >= 4 and q in bom[covered_by]["_text"] for q in pns)
        rule_notes = [f(bom, dict(tray=tray_txt, mcm=mcm)) for rx, f in RULES if re.search(rx, n)]
        rule_notes = [x for x in rule_notes if x]
        real_pns = [q for q in pns if q.upper() not in ("RACK", "ZACT", "KF40HN", "RELIEF316", "TSLOT20", "DOORTRACK", "COMBITAC",
                                                       "PUMP", "SMC-CYL20", "HSSBLANK", "PI-HQ", "IPG-COLLIMATOR")]
        if kind == "excluded":
            status = "excluded"
        elif rule_notes:
            status = "inconsistent"
        elif not covered_by:
            status = "missing from BOM"
        elif kind.startswith("custom"):
            status = "custom"
        elif kover == "generic" or not pns:
            status = "generic"
        elif priced_rows:
            status = "real part priced"
        elif [h for h in hits if h.get("no_price")]:
            status = "real part unpriced"             # a purchase list says the vendor publishes no price
        elif bom_names_pn and re.search(r"fetched|quote", basis, re.I) and real_pns:
            status = "real part priced"             # the BOM line names it and was priced from a vendor
        elif [h for h in hits if h["price"] is None]:
            status = "real part unpriced"
        elif real_pns or bom_names_pn:
            status = "real part unpriced"
        else:
            status = "generic"
        price = priced_rows[0]["price"] if priced_rows else None
        refs = sorted({f"{h['file']}:{h['id']}" for h in hits})[:4]
        if not covered_by:
            mt = t.get("bom", "")
            why = f"model tag {mt} has no bom.csv line" if mt and mt not in bom else (f"model tag {mt} does not cover it" if mt else "no model tag")
            note = (note + "; " if note else "") + why
        if machined and kind == "custom (machined)" and not any(n[:40] == m[:40] for m in machined) and "not in" not in note:
            note = (note + "; " if note else "") + "not in machining/hours.csv"
        row = dict(part=n, module=p["module"], material=p["material"], mass_kg=p["mass_kg"], kind=kind, model_bom_tag=t.get("bom", ""),
                   model_mcm=mcm, part_numbers=" ".join(sorted(real_pns)), bom_line=covered_by, purchase_refs=" ".join(refs),
                   unit_price_usd="" if price is None else round(price, 2), status=status, note="; ".join([note] + rule_notes).strip("; "))
        out.append(row)
        if covered_by:
            line_parts[covered_by].append(n)

    sfx = f"_{a.tag}" if a.tag else ""
    with open(OUT / f"model_vs_bom{sfx}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    # reverse: bom lines and purchase rows with no model part
    old_bom = {r["id"]: r for r in read_csv(OUT / "bom_before.csv")} if (OUT / "bom_before.csv").exists() else None
    rev = []
    for i, b in bom.items():
        rev.append(dict(kind="bom.csv line", file="bom.csv", id=i, part_numbers="", item=b["item"][:110],
                        model_parts=len(line_parts.get(i, [])), costed_by=i, reason=""))
    for rec in prow:
        if not rec["used"]:
            rev.append(dict(kind="purchase row", file=rec["file"], id=rec["id"], part_numbers=" ".join(rec["pns"])[:80], item=rec["desc"],
                            model_parts=0, costed_by=rec["costed_by"], reason=reason_for(rec, bom, old_bom)))
    with open(OUT / f"purchase_vs_model{sfx}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rev[0].keys()))
        w.writeheader()
        w.writerows(rev)

    cnt = Counter(r["status"] for r in out)
    lo = sum(float(b["qty"]) * float(b["unit_low_usd"]) for b in bom.values())
    hi = sum(float(b["qty"]) * float(b["unit_high_usd"]) for b in bom.values())
    summary = dict(bom=str(a.bom), parts=len(out), by_status={s: cnt.get(s, 0) for s in STATUSES},
                   by_kind=dict(Counter(r["kind"] for r in out)), bom_lines=len(bom),
                   bom_lines_without_model_part=[i for i in bom if not line_parts.get(i)],
                   model_tags_without_bom_line=sorted({r["model_bom_tag"] for r in out if r["model_bom_tag"] and r["model_bom_tag"] not in bom}),
                   bom_total_usd=[round(lo), round(hi)], extra=[str(x) for x in a.extra])
    (OUT / f"summary{sfx}.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary["by_status"]), "| BOM total", summary["bom_total_usd"], "| tags w/o line", summary["model_tags_without_bom_line"])
    if not a.tag:
        write_md(out, rev, summary)


def write_md(out, rev, summary):
    head = (HERE / "completeness-head.md")
    before = OUT / "summary_before.json"
    lines = [head.read_text().rstrip() + "\n" if head.exists() else "# Completeness audit\n"]
    lines.append("\n## Counts by status (generated)\n")
    b = json.loads(before.read_text())["by_status"] if before.exists() else {}
    only = OUT / "summary_bomonly.json"
    o = json.loads(only.read_text())["by_status"] if (summary["extra"] and only.exists()) else None
    extra_names = ", ".join(pathlib.Path(x).name for x in summary["extra"])
    head_row = "| Status | Before (bom.csv at the start of this audit) | Now, bom.csv |" + (f" Now, bom.csv + {extra_names} |" if o else "")
    lines.append(head_row)
    lines.append("|---|---|---|" + ("---|" if o else ""))
    for st in STATUSES:
        lines.append(f"| {st} | {b.get(st, 0)} | {(o or summary['by_status'])[st]} |" + (f" {summary['by_status'][st]} |" if o else ""))
    lines.append(f"| **total** | {sum(b.values())} | {summary['parts']} |" + (f" {summary['parts']} |" if o else ""))
    lines.append(f"\nModel tags with no bom.csv line: {', '.join(summary['model_tags_without_bom_line']) or 'none'}. "
                 f"BOM total now ${summary['bom_total_usd'][0]:,} - ${summary['bom_total_usd'][1]:,}. "
                 f"Extra purchase lists read: {', '.join(pathlib.Path(x).name for x in summary['extra']) or 'none'}.\n")
    order = {s: i for i, s in enumerate(["inconsistent", "missing from BOM", "generic", "real part unpriced", "real part priced", "custom", "excluded"])}
    bb = OUT / "bom_before.csv"
    if bb.exists():
        old = {r["id"]: r for r in read_csv(bb)}
        new = {r["id"]: r for r in read_csv(LPBF / "bom.csv")}
        ch = [i for i in new if i not in old or any(old[i].get(c) != new[i].get(c) for c in ("item", "candidate", "qty", "unit_low_usd", "unit_high_usd"))]
        if ch:
            def rng(r):
                q = float(r["qty"])
                return f"{q * float(r['unit_low_usd']):,.0f} – {q * float(r['unit_high_usd']):,.0f}"
            lines.append("\n## BOM lines this audit changed (generated from [`analysis/out/audit/bom_before.csv`](analysis/out/audit/bom_before.csv), the BOM at the start)\n")
            lines.append("| Line | Item now | Was (USD, qty x unit) | Now (USD) | Candidate now |")
            lines.append("|---|---|---|---|---|")
            for i in ch:
                r = new[i]
                was = rng(old[i]) if i in old else "new line"
                cand = r["candidate"] if len(r["candidate"]) < 160 else r["candidate"][:157] + "..."
                lines.append(f"| {i} | {r['item']} | {was} | {rng(r)} | {cand} |")
            lo0 = sum(float(r["qty"]) * float(r["unit_low_usd"]) for r in old.values())
            hi0 = sum(float(r["qty"]) * float(r["unit_high_usd"]) for r in old.values())
            lines.append(f"\nBOM total: ${lo0:,.0f} – ${hi0:,.0f} before, ${summary['bom_total_usd'][0]:,} – ${summary['bom_total_usd'][1]:,} now.\n")
    lines.append("\n## Every model part (generated; also in [`analysis/out/audit/model_vs_bom.csv`](analysis/out/audit/model_vs_bom.csv))\n")
    lines.append("Fasteners (tag `fastener`, all McMaster and all in `fasteners.csv` / line FX) are counted above but listed only in the CSV.\n")
    lines.append("| Status | Part | Kind | BOM line | Part numbers | Note |")
    lines.append("|---|---|---|---|---|---|")
    for r in sorted(out, key=lambda r: (order[r["status"]], r["bom_line"], r["part"])):
        if r["kind"] == "fastener" and r["status"] == "real part priced":
            continue
        nm = r["part"] if len(r["part"]) < 95 else r["part"][:92] + "..."
        lines.append(f"| {r['status']} | {nm} | {r['kind']} | {r['bom_line'] or '–'} | {r['part_numbers'] or '–'} | {r['note'] or ''} |")
    lines.append("\n## bom.csv lines and the model (generated)\n")
    why = {"L2": "no chiller for the air-cooled IPG unit", "C1": "the model draws no scan PC (C1 is a card)",
           "C2": "inside the drawn DIN-rail drawer", "C3": "inside the drawn DIN-rail drawer", "C4": "inside the drawn DIN-rail drawer",
           "C5": "inside the drawn DIN-rail drawer", "C6": "the model draws a 3U drawer, not this wall box",
           "G9": "inside the drawn O2 / dew-point panel box (G6)", "S1": "inside the drawn DIN-rail drawer",
           "S6": "PPE", "S7": "room safety", "S8": "room safety", "P1": "off the tray", "T1": "commissioning tool",
           "T2": "not drawn", "H2": "inside the drawn DIN-rail drawer", "H3": "not drawn yet (heat.md)", "X1": "labour"}
    lines.append("| Line | Item | Model parts mapped | Why none |")
    lines.append("|---|---|---|---|")
    for r in rev:
        if r["kind"] == "bom.csv line":
            lines.append(f"| {r['id']} | {r['item']} | {r['model_parts'] or '**none**'} | {why.get(r['id'], '') if not r['model_parts'] else ''} |")
    cnt = Counter(r["file"] for r in rev if r["kind"] == "purchase row")
    lines.append("\n## Purchase-list rows that no model part uses (generated; full list in "
                 "[`analysis/out/audit/purchase_vs_model.csv`](analysis/out/audit/purchase_vs_model.csv))\n")
    lines.append("Most of these are expected: stock for the custom parts (a plate or bar has no part in the model to carry its part "
                 "number), tools and fixtures (`assembly-tooling.csv`), the robot cell (`robot-tooling.csv`), room safety and PPE "
                 "(`safety-parts.csv`), alternatives with qty 0, sizes for the S25 and L75 modules (the model draws M50), and the "
                 "lab's other plate materials. The stale ones are the tall model's rows in `mcmaster-parts.csv` named above.\n")
    rc = Counter((r["file"], r["reason"] or "other") for r in rev if r["kind"] == "purchase row")
    lines.append("| File | Rows with no model part | By reason (a guess from the file, qty and the line's text) |")
    lines.append("|---|---|---|")
    for f, c in sorted(cnt.items()):
        why = "; ".join(f"{k[1]} {v}" for k, v in sorted(rc.items()) if k[0] == f)
        lines.append(f"| {f} | {c} | {why} |")
    stale = [r for r in rev if r["kind"] == "purchase row" and r["reason"].startswith("stale")]
    if stale:
        lines.append("\nRows their own BOM line has retired (the tall model's parts, and parts moved to other lines):\n")
        lines.append("| File | Line | Part numbers | Item |")
        lines.append("|---|---|---|---|")
        for r in stale:
            lines.append(f"| {r['file']} | {r['costed_by']} | {r['part_numbers']} | {r['item']} |")
    lines.append("")
    (LPBF / "completeness-audit.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
