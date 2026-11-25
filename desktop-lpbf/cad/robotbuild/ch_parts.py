"""Chapter 10-parts of the robot-built desktop LPBF video: the long-table tour, category by category, with the running
cost (new against used) and the lead times on screen (about 2 minutes).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_parts.py
    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_parts.py meta      # numbers only: rewrite meta.jsonl

Two stages, so the numbers can change without re-rendering the 3-D:
  1. render: the camera runs along the long table (hall.py with kit_table.py's layout, stock mode: machined parts as
     their blanks), one zone of kit_table.CAT_ORDER after another, and closes in on each big item (a fixed list, BIG,
     found on the table by name). Each frame's metadata records only the shot (phase, category, item).
  2. meta: reads the cost and lead-time data (hud(): the data worker's /tmp/robotbuild/data/hud.json, or, until that
     exists, a provisional set built here from bom.csv, cost/used-options.csv and rough lead times) and rewrites every
     frame's caption, cost panel and lead panel from the shot list. Run alone with `meta`.

No project time passes in this chapter (proc_s 0; the clocks are hidden).
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402

FPS = common.FPS
LT = common.LONG_TABLE
NAME, TITLE = "10-parts", "The parts: cost and lead time"
CAT_ORDER = ["stock", "sheet", "motion", "gas", "optics", "elec", "seal", "frame"]      # kit_table.CAT_ORDER
CAT_TITLE = dict(
    stock="Stock to machine: 6061 and MIC-6 plate and bar, 316 bar and tube, Macor",
    sheet="Sheet to cut, bend and weld: 304 / 316L sheet, 5052 guard panels",
    motion="Motion: rails, ball screws, servos, the Z actuator, hinges, latches",
    gas="Vacuum and gas: KF parts, valves, pump, blower, filter, O2 and dew point",
    optics="Laser and optics: fiber laser, galvo, f-theta lens, collimator, shutter, windows",
    elec="Electronics, heaters and sensors: UPS, PC and scan card, DIN drawer, heaters",
    seal="Seals and fasteners: FKM O-rings, seals, screws, inserts and pins",
    frame="Frames: the 19 in. rack, the guard frame, levelling mounts",
)
# the big items: (key, slot-name match on kit_table, BOM ids, on-screen name)
BIG = [
    ("baseplate", "Base plate, process module", ["F4"], "MIC-6 cast plate for both module base plates"),
    ("laser", "Fiber laser source", ["L1"], "Fiber laser, 500 W single-mode (IPG YLR-500)"),
    ("galvo", "2-axis galvo scan head", ["L5"], "2-axis galvo scan head"),
    ("ftheta", "f-theta lens", ["L6"], "F-theta lens"),
    ("collimator", "Collimator", ["L3"], "Collimator (2.5 mm, IPG)"),
    ("shutter", "Safety shutter + beam dump", ["L4"], "Safety shutter + beam dump"),
    ("controller", "Scan + laser controller PC", ["C1", "C2"], "Scan card (RTC6) + controller PC"),
    ("ups", "UPS", ["D2"], "UPS (2U, in the rack)"),
    ("safety", "DIN-rail drawer", ["S1"], "Safety controller and final elements"),
    ("zeropoint", "Zero-point clamping modules", ["B3"], "Zero-point module clamps (SCHUNK VERO-S)"),
    ("pump", "Dry scroll pump", ["G2"], "Dry scroll vacuum pump"),
    ("o2", "Trace O2 analyzer", ["G6", "G9"], "Trace O2 analyzer + dew-point sensor"),
    ("blower", "Sealed side-channel blower", ["G4"], "Recirculation blower"),
    ("rackframe", "19 in. rack frame", ["S9"], "12U rack (22 kg), guard frame and panels"),
]
CW_CHAIN = ("L1", "L3", "L5", "L6", "C1")     # at spec, these are the specified parts (the BOM's high end)
# the long leads, after the zones: what sets the date the parts are all in (hud.json headline and lead_times)
LONG = [
    ("guardswitch", "Guard-position switch IDEC", ["S2"], "IDEC HS6B guard-position switch"),
    ("relay", "Power box PB1", ["H2"], "Omron K8DT plate-temperature relay (in the power box)"),
    ("laserlead", "Fiber laser source", ["L1"], "Fiber laser (IPG YLR-500)"),
    ("honing", "Build module M50", ["B1s"], "Build module: welded, bored and honed outside"),
]
# BOM line -> the kit category its cost is shown under (provisional hud only; X1, the machining, is left out: the
# robot shop makes those parts in chapters 30-32)
BOM_CAT = dict(
    G1="stock", F4="stock", F5="stock", B1="stock", T3="stock",
    R1="sheet", A2="sheet",
    M1="motion", M2="motion", M3="motion", M4="motion", M5="motion", A3="motion",
    G2="gas", G3="gas", G4="gas", G5="gas", G6="gas", G7="gas", G9="gas", P1="gas", B4="gas", S7="gas",
    L1="optics", L2="optics", L3="optics", L4="optics", L5="optics", L6="optics", L7="optics", T1="optics", T2="optics",
    S5="optics", S6="optics",
    C1="elec", C2="elec", C3="elec", C4="elec", C5="elec", C6="elec", H1="elec", H2="elec", H3="elec", D1="elec",
    D2="elec", E1="elec", E2="elec", E3="elec", E4="elec", E5="elec", A1="elec", M6="elec", S1="elec", S2="elec",
    S3="elec", S4="elec", B3="elec",
    G8="seal", B2="seal", FX="seal",
    F3="frame", S9="frame", S8="frame",
)
# provisional lead times, weeks [low, high], new and used (None: no used option): rough, replaced by hud.json
LEAD_PROV = dict(
    L1=([10, 12], [0.4, 1.0]), L3=([10, 12], [0.4, 1.0]), L5=([4, 8], [0.4, 1.0]), L6=([2, 6], [0.4, 1.0]),
    L4=([4, 8], None), C1=([4, 8], [0.4, 1.0]), D2=([0.4, 1.0], [0.4, 1.0]), S1=([1, 3], None), B3=([4, 8], None),
    G2=([2, 6], [0.4, 1.0]), G6=([2, 6], [0.4, 1.0]), G4=([2, 6], None),
)


# ================================================================================================ the numbers
def _bom():
    sys.path.insert(0, str(common.LPBF / "cost"))
    import cost_scenarios as CS
    lines = CS.read_bom()
    used = CS.apply(lines, CS.read_used())
    items = {r["id"]: r for r in csv.DictReader(open(common.LPBF / "bom.csv"))}
    return lines, used, items


def provisional_hud():
    """Cost by kit category and the big items, from bom.csv and cost/used-options.csv (cost_scenarios.apply: each used
    pick replaces its component where it is cheaper); lead times are rough placeholders (LEAD_PROV). Same shape as
    adapt()'s."""
    lines, used, items = _bom()
    cats = []
    for c in CAT_ORDER:
        ids = [k for k, v in BOM_CAT.items() if v == c and k in lines]
        new = [sum(lines[k]["low"] for k in ids), sum(lines[k]["high"] for k in ids)]
        us = sorted([sum(used[k][0] for k in ids), sum(used[k][1] for k in ids)])
        big_ids = [b[2][0] for b in BIG if _cat_of(b[0]) == c]
        cats.append(dict(key=c, title=CAT_TITLE[c], new=new, used=us, bom=ids, items=big_ids, on_table=True))
    if "X1" in lines:
        cats.append(dict(key="services", title="Services: machining the custom parts, if bought", bom=["X1"], items=[],
                         new=[lines["X1"]["low"], lines["X1"]["high"]], used=[lines["X1"]["low"], lines["X1"]["high"]],
                         on_table=False))
    big = []
    for key, match, ids, label in BIG:
        new = [sum(lines[k]["low"] for k in ids), sum(lines[k]["high"] for k in ids)]
        us = sorted([sum(used[k][0] for k in ids), sum(used[k][1] for k in ids)])
        ln, lu = LEAD_PROV.get(ids[0], (None, None))
        big.append(dict(key=ids[0], name=label, short=short(ids[0], label), bom=ids, cat=_cat_of(key), new=new,
                        used=us if us != new else None, used_label="used", lead_new=ln, lead_used=lu, note=""))
    lead = [dict(name=b["short"], new=b["lead_new"], used=b["lead_used"], long=bool(b["lead_new"] and b["lead_new"][1] >= 6))
            for b in big if b["lead_new"]]
    tn = [sum(c["new"][0] for c in cats), sum(c["new"][1] for c in cats)]
    tu = [sum(c["used"][0] for c in cats), sum(c["used"][1] for c in cats)]
    return dict(source="provisional (video worker): bom.csv + cost/used-options.csv; lead times rough", cats=cats,
                big=big, lead=lead, excluded={}, totals=dict(new=tn, used=tu))


def _num_pair(v):
    if v is None:
        return None
    if isinstance(v, dict):
        lo = v.get("low", v.get("lo", v.get("min")))
        hi = v.get("high", v.get("hi", v.get("max", lo)))
        return None if lo is None else sorted([float(lo), float(hi if hi is not None else lo)])
    if isinstance(v, (list, tuple)):
        return sorted([float(v[0]), float(v[-1])]) if len(v) else None
    try:
        return [float(v), float(v)]
    except (TypeError, ValueError):
        return None


SHORT = dict(L1="Fiber laser 500 W", L5="Galvo scan head", C1="Scan card (RTC6)", L6="F-theta lens", L3="Collimator",
             L4="Safety shutter", L2="Laser chiller", D2="UPS (2U)", G2="Scroll pump", G6="O2 analyzer",
             G9="Dew-point sensor", G4="Blower", G7="Valves, KF, gauges", B3="Zero-point clamps", S1="Safety controller",
             T1="Power meter", T2="Photodiode chain", H1="Heater stacks", M1="Recoater axis", M2="Servos", M3="Z actuator",
             A3="Door pneumatics", F4="MIC-6 plate", G1="Chamber stock", D1="Tray dock", P1="Glovebox",
             A2v="Metal-dust vacuum", A2s="Cover slides", S7="Room O2 monitor", S8="Class D extinguisher",
             A1="Step sensors, NFC", C5="PLC + TC inputs", S9="Rack + guard frame", X1="Machining (shop)",
             B1s="Weld, bore, hone", S2="Guard switch (IDEC)", H2="Heater relay (Omron)", E1="Power box PB1",
             C4="DC supplies", M4="Metering drive", M5="Blade cartridges", G3="Argon supply", G5="Filter train",
             G8="Seals", S4="Key switch, lamp", S5="Viewing window", S6="Laser eyewear", F3="Levelling mounts",
             F5="Optics bridge", H3="Cooling fan", B1="Build modules", B2="Module seals", C2="Supervisor PC",
             C3="Motion controller", C6="Control drawer", E2="Ethernet switch", E3="Home sensors", E4="Wire, straps",
             E5="Options (meter, card)", R1="Reservoirs", M6="Layer camera", A2="Liners, consumables", B4="Release air",
             S3="E-stops", T3="Calibration tools", L7="Chamber window")


def short(item_id, name):
    return SHORT.get(item_id) or re.split(r" \(|, ", name or str(item_id))[0]


def _days_to_wk(d):
    p = _num_pair(d)
    return None if p is None else [p[0] / 7.0, p[1] / 7.0]


def adapt(raw):
    """The data worker's hud.json (build_hud.py) in this chapter's shape, lead times in weeks. Read: categories [{cat,
    title, lines, new, used, items, on_table}], items [{id, line, cat, name, new_low, new_high, used_best, new_src,
    lead: {new: {days, text}, used: {days, text}}, hud: {lead_new, lead_used}}], and lead_times: {lines: {line: {item,
    days_new, days_used, short_new, short_used}}} (or the first version's lead_times.table)."""
    out = dict(source="hud.json (data worker, " + str(raw.get("generated_utc", "")) + ")", cats=[], big=[], lead=[],
               excluded={}, schedule=(raw.get("lead_times") or {}).get("schedule"),
               risks=(raw.get("lead_times") or {}).get("risks") or [])
    for c in raw.get("categories") or []:
        key = c.get("cat") or c.get("key")
        out["cats"].append(dict(key=key, title=c.get("title") or CAT_TITLE.get(key, key), new=_num_pair(c.get("new")),
                                used=_num_pair(c.get("used")), bom=c.get("lines") or [], items=c.get("items") or [],
                                on_table=c.get("on_table", key in CAT_ORDER),
                                spec_new=_num_pair(c.get("spec_new")), spec_used=_num_pair(c.get("spec_used"))))
    out["headline"] = raw.get("headline") or {}
    lt = raw.get("lead_times") or {}
    lines = lt.get("lines") or {}
    table = lt.get("table") or {}
    for x in raw.get("items") or []:
        iid, line = x.get("id"), x.get("line") or x.get("id")
        ln = lu = None
        tn = tu = ""
        L = x.get("lead") or {}
        if L.get("new"):
            ln, tn = _days_to_wk(L["new"].get("days")), L["new"].get("text") or ""
        if L.get("used"):
            lu, tu = _days_to_wk(L["used"].get("days")), L["used"].get("text") or ""
        if ln is None and line in lines:
            ln, tn = _days_to_wk(lines[line].get("days_new")), lines[line].get("short_new") or ""
        if lu is None and line in lines and lines[line].get("days_used"):
            lu, tu = _days_to_wk(lines[line].get("days_used")), lines[line].get("short_used") or ""
        row = table.get(iid) or table.get(line) or []
        if ln is None and len(row) > 0 and row[0]:
            ln, tn = _days_to_wk(row[0][1]), row[0][0]
        if lu is None and len(row) > 1 and row[1]:
            lu, tu = _days_to_wk(row[1][1]), row[1][0]
        hudx = x.get("hud") or {}
        ub = x.get("used_best")
        lo_, hi_ = x.get("new_low"), x.get("new_high")
        spec = (hi_ if line in CW_CHAIN else lo_) if lo_ is not None else None
        out["big"].append(dict(key=iid, name=x.get("name") or iid, short=short(iid, x.get("name")), bom=[line],
                               spec_new=None if spec is None else [float(spec), float(spec)],
                               cat=x.get("cat"), new=_num_pair([x.get("new_low"), x.get("new_high")]),
                               used=None if ub is None else [float(ub), float(ub)], used_label="used",
                               lead_new=ln, lead_used=lu, lead_note=hudx.get("lead_new") or tn,
                               used_note=(hudx.get("lead_used") if ub is not None else "") or tu,
                               note=x.get("new_src") or ""))
    out["lines"] = {line: dict(short=short(line, v.get("item")), new=_days_to_wk(v.get("days_new")),
                               used=_days_to_wk(v.get("days_used")) if v.get("days_used") else None,
                               short_new=v.get("short_new") or "", short_used=v.get("short_used") or "")
                    for line, v in lines.items()}
    if lines:
        for line, v in lines.items():
            new = _days_to_wk(v.get("days_new"))
            used = _days_to_wk(v.get("days_used")) if v.get("days_used") else None
            if new is None and used is None:
                continue
            out["lead"].append(dict(name=short(line, v.get("item")), new=new, used=used,
                                    long=bool(new is not None and new[1] >= 6.0), line=line))
    else:
        for b in out["big"]:
            if b["lead_new"] is not None or b["lead_used"] is not None:
                out["lead"].append(dict(name=b["short"], new=b["lead_new"], used=b["lead_used"],
                                        long=bool(b["lead_new"] is not None and b["lead_new"][1] >= 6.0), line=b["key"]))
    tot = (raw.get("totals") or {}).get("scenarios") or {}
    out["totals"] = dict(new=_num_pair(tot.get("new")), used=_num_pair(tot.get("used")))
    return out


def hud():
    p = common.DATA / "hud.json"
    if p.exists():
        try:
            h = adapt(json.loads(p.read_text()))
            if h["cats"]:
                return h
            print("ch_parts: hud.json has no categories I can read; using the provisional numbers", flush=True)
        except Exception as e:                                   # noqa: BLE001
            print(f"ch_parts: hud.json unreadable ({e!r}); using the provisional numbers", flush=True)
    return provisional_hud()


# ================================================================================================ the 3-D
def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return tuple(float(x) + (float(y) - float(x)) * u for x, y in zip(a, b))


def view(focal, dist, az, el, shift=0.15):
    """A camera on hall.orbit, moved sideways so the subject sits left of centre (the panels take the right 30 %)."""
    import hall as HL
    pos = np.array(HL.orbit(focal, dist, az, el))
    f = np.array(focal, float)
    d = f - pos
    right = np.cross(d / np.linalg.norm(d), (0.0, 0.0, 1.0))
    right /= max(np.linalg.norm(right), 1e-9)
    s = shift * 0.953 * np.linalg.norm(d) * right
    return [tuple(pos + s), tuple(f + s)]


def _seg_hits_box(p0, p1, b, pad=15.0):
    """Does the segment p0-p1 pass through box b = (x0, x1, y0, y1, z0, z1) grown by pad (slab test)?"""
    t0, t1 = 0.0, 1.0
    d = np.asarray(p1, float) - np.asarray(p0, float)
    for k in range(3):
        lo, hi = b[2 * k] - pad, b[2 * k + 1] + pad
        if abs(d[k]) < 1e-9:
            if p0[k] < lo or p0[k] > hi:
                return False
            continue
        a, c = (lo - p0[k]) / d[k], (hi - p0[k]) / d[k]
        if a > c:
            a, c = c, a
        t0, t1 = max(t0, a), min(t1, c)
        if t0 > t1:
            return False
    return True


def clear_view(target, slots, me, d, prefs):
    """The (az, el) of `prefs` (in order of preference) whose sight line to `target` crosses the fewest other items'
    boxes (kit_table slots), so a close-up is not hidden behind a panel standing on its edge."""
    import hall as HL
    best, best_n = prefs[0], None
    for az, el in prefs:
        cam = np.array(HL.orbit(target, d, az, el))
        if cam[1] < -2600.0:                                   # the shop's north row stands beyond y = -2686
            continue
        n = 0
        for s in slots:
            if s is me:
                continue
            b = s["bbox"]
            if b[5] - b[4] < 25.0 and max(b[1] - b[0], b[3] - b[2]) < 80.0:
                continue                                       # small, low parts don't hide anything
            if _seg_hits_box(cam, target, b):
                n += 1
        if best_n is None or n < best_n:
            best, best_n = (az, el), n
        if n == 0:
            break
    return best


def render():
    import hall as HL
    t0 = time.time()
    h = HL.Hall(kit="stock")
    if h.kt is None:
        raise SystemExit("ch_parts: kit_table.py is needed (set KIT_TABLE_DIR until it is merged)")
    h.mir_to("A", 1500.0)                    # both MiRs at the bench, out of the tour's way
    h.mir_to("B", 350.0)
    if h.person is not None:
        h.person.set(x=LT["x0"] - 480.0, y=40.0, hd=-90.0, amp=0.0, look=(LT["x0"] + 600.0, 0.0, 900.0))
    kt = h.kt
    zones = {z["category"]: z for z in kt.zones()}
    slots = kt.slots()
    print(f"hall + kit in {time.time() - t0:.0f} s; zones {list(zones)}", flush=True)
    ch = common.Chapter(NAME, TITLE)
    AZ, EL = 200.0, 38.0
    cam = view((LT["x0"] + 2500.0, 0.0, 860.0), 9000.0, 215.0, 34.0, shift=0.12)
    labels3d = {}

    def frames(n, cam0, cam1, shot, labels=()):
        for i in range(n):
            u = ease(i / max(1, n - 1))
            c = [lerp(cam0[0], cam1[0], u), lerp(cam0[1], cam1[1], u), (0.0, 0.0, 1.0)]
            img = h.sc.render(c, 30.0)
            labs = []
            for text, p in labels:
                (x, y), = common.project(h.pl, [p])
                if 0 <= x <= 880 and 70 <= y <= common.H - 30:
                    labs.append([round(x, 1), round(y, 1), text])
            ch.frame(img, "", shot=dict(shot, u=round(i / max(1, n - 1), 3)), labels=labs, proc_s=0.0, no_clock=True)
        return cam1

    def closeup(cam, s, label, shot, hold=3.0):
        """Fly to a slot's item (a camera no other item hides, clear_view) and hold on it."""
        bb = np.asarray(s["bbox"], float)
        c = ((bb[0] + bb[1]) / 2, (bb[2] + bb[3]) / 2, (bb[4] + bb[5]) / 2)
        size = max(bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4])
        d = max(1100.0, 3.2 * size)
        prefs = [(AZ - 10.0, 30.0), (AZ - 10.0, 45.0), (AZ + 20.0, 35.0), (AZ - 40.0, 35.0), (AZ + 40.0, 40.0),
                 (AZ - 70.0, 40.0), (0.0, 35.0), (-25.0, 40.0), (25.0, 40.0), (AZ - 10.0, 60.0)]
        az_i, el_i = clear_view(c, slots, s, d, prefs)
        near = view(c, d, az_i, el_i, shift=0.16)
        lab = [(label.split(" (")[0], (c[0], c[1], bb[5]))]
        cam = frames(int(1.6 * FPS), cam, near, shot, lab)
        near2 = view(c, d * 0.93, az_i + 8.0, max(25.0, el_i - 2.0), shift=0.16)
        frames(int(hold * FPS), near, near2, shot, lab)
        return near2

    # the opening: the whole table from behind lane B
    c_open = view(((LT["x0"] + LT["x1"]) / 2, 400.0, 600.0), 11500.0, 200.0, 36.0, shift=0.12)
    cam = frames(int(2.5 * FPS), cam, c_open, dict(phase="open"))
    cam = frames(int(4.0 * FPS), c_open, c_open, dict(phase="open"))
    for cat in CAT_ORDER:
        z = zones.get(cat)
        if z is None:
            continue
        x0, x1 = z["x0"], z["x1"]
        w = x1 - x0
        dist = 2900.0 if w < 2500 else 3300.0
        a = view((x0 + min(0.25 * w, 600.0), 0.0, 880.0), dist, AZ, EL)
        b = view((x1 - min(0.25 * w, 600.0), 0.0, 880.0), dist, AZ + 8.0, EL - 2.0)
        lab = [(CAT_TITLE[cat].split(":")[0], (x0 + 0.5 * w, LT["y1"], LT["top"]))]
        cam = frames(int(1.6 * FPS), cam, a, dict(phase="cat", cat=cat), lab)
        cam = frames(int((6.5 if w > 2500 else 4.5) * FPS), a, b, dict(phase="cat", cat=cat), lab)
        for key, match, ids, label in BIG:
            s = next((s for s in slots if match.lower() in s["name"].lower()), None)
            if s is None or s["category"] != cat:
                continue
            cam = closeup(cam, s, label, dict(phase="item", cat=cat, item=key))
    # the long leads: what sets the date
    for key, match, ids, label in LONG:
        s = next((s for s in slots if match.lower() in s["name"].lower()), None)
        if s is None:
            continue
        cam = closeup(cam, s, label, dict(phase="long", item=key), hold=3.6)
    c_close = view(((LT["x0"] + LT["x1"]) / 2, 400.0, 600.0), 12500.0, 196.0, 40.0, shift=0.12)
    cam = frames(int(2.5 * FPS), cam, c_close, dict(phase="close"))
    frames(int(8.0 * FPS), c_close, c_close, dict(phase="close"))
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s) in {time.time() - t0:.0f} s", flush=True)


# ================================================================================================ the metadata
def write_meta():
    d = common.FRAMES / NAME
    rows = [json.loads(x) for x in (d / "meta.jsonl").read_text().splitlines()]
    H = hud()
    cats = {c["key"]: c for c in H["cats"]}
    big = {b["key"]: b for b in H["big"]}
    order = [c for c in CAT_ORDER if c in cats]
    extra = [c["key"] for c in H["cats"] if c["key"] not in CAT_ORDER]      # off the table, services: added at the end
    n_cats = len(order)
    lead_rows = sorted(H["lead"], key=lambda r: -max((r["new"] or [0, 0])[1], (r["used"] or [0, 0])[1]))
    common.DATA.mkdir(parents=True, exist_ok=True)
    (common.DATA / "hud_panel.json").write_text(json.dumps(dict(source=H["source"], lead=lead_rows), indent=1))
    prov = H["source"].startswith("provisional")
    hl = H.get("headline") or {}
    at_spec = any(c.get("spec_new") for c in H["cats"])
    src_note = "Provisional numbers (bom.csv, cost/used-options.csv; rough lead times)." if prov else \
        "Prices: bom.csv and eBay / surplus listings; lead times: catalogue pages and quotes, BYU's PO time included."
    foot = ("at spec: the laser chain as specified, the cheapest listed option elsewhere; used: eBay, surplus"
            if at_spec else "solid: low end, tint: up to the high end; used = eBay and surplus where sensible")

    def pair(v):
        return v if v is not None else [0.0, 0.0]

    def new_of(c):
        return c.get("spec_new") or c.get("new")

    def used_of(c):
        return c.get("spec_used") or c.get("used") or new_of(c)

    def running(keys, frac):
        """Running totals over categories `keys`, the last one counted in at `frac` (0-1)."""
        rn, ru = [0.0, 0.0], [0.0, 0.0]
        for k, c in enumerate(keys):
            f = frac if k == len(keys) - 1 else 1.0
            un, uu = pair(new_of(cats[c])), pair(used_of(cats[c]))
            rn = [rn[0] + f * un[0], rn[1] + f * un[1]]
            ru = [ru[0] + f * uu[0], ru[1] + f * uu[1]]
        return rn, ru

    def item_new(b):
        return b.get("spec_new") or b.get("new")

    def items_of(cat, hl_key=None):
        ids = cats[cat].get("items") or []
        its = [big[i] for i in ids if i in big]
        its.sort(key=lambda b: -pair(item_new(b))[1])
        if hl_key in big and big[hl_key] not in its:
            its.insert(0, big[hl_key])
        if hl_key:
            its.sort(key=lambda b: b["key"] != hl_key)
        return [dict(name=b["name"], new=item_new(b), used=b["used"], used_label=b.get("used_label", "used"),
                     lead_new=b["lead_new"], lead_used=b["lead_used"], hl=(b["key"] == hl_key)) for b in its[:4]]

    def item_row(b, on=True):
        return dict(name=b["name"], new=item_new(b), used=b["used"], used_label=b.get("used_label", "used"),
                    lead_new=b["lead_new"], lead_used=b["lead_used"], hl=on)

    big_of = {b[0]: b[2][0] for b in BIG + LONG}            # 3-D close-up key -> hud item key (its BOM id)
    lines = H.get("lines") or {}
    for key, match, ids, label in BIG + LONG:               # close-ups that are not hud items: a lead-time risk
        i = ids[0]
        if i in big:
            continue
        risk = next((r for r in H.get("risks") or [] if r.get("line") == i), None)
        ln = lines.get(i) or {}
        if risk is None and not ln:
            continue
        usd = float(risk["usd"]) if risk and risk.get("usd") else None
        big[i] = dict(key=i, name=(risk or {}).get("part") or label, short=ln.get("short") or short(i, label), bom=[i],
                      cat=_cat_of(key), new=[usd, usd] if usd else None, spec_new=[usd, usd] if usd else None, used=None,
                      used_label="used", lead_new=ln.get("new"), lead_used=ln.get("used"),
                      lead_note=(risk or {}).get("stated") or ln.get("short_new", ""),
                      used_note=(risk or {}).get("action") or "", note="")
    wk = hl.get("weeks") or {}
    tn, tu = running(order + extra, 1.0)
    out, seen = [], {}
    for m in rows:
        sh = m.get("shot") or {}
        ph, cat, item = sh.get("phase"), sh.get("cat"), sh.get("item")
        key = (ph, cat, item)
        seen[key] = seen.get(key, -1) + 1
        t_in = seen[key] / FPS                                   # seconds into this shot (both its moves)
        lead = dict(rows=lead_rows, highlight=[])
        if ph == "open":
            cap = "Every part of one machine, as it arrives, on 12 m of table"
            sub = "Machined parts are still stock blanks; parts over the UR12e's 12.5 kg wait on pallets for a person " \
                  "and a lift. " + src_note
            cost = dict(cat="", n_cats=n_cats, run_new=[0, 0], run_used=[0, 0], items=[], foot=foot,
                        note="new at spec against used where a sensible listing exists" if at_spec else "")
        elif ph in ("cat", "item") and cat in cats:
            c = cats[cat]
            ci = order.index(cat)
            frac = min(1.0, t_in / 1.2) if ph == "cat" else 1.0
            rn, ru = running(order[:ci + 1], frac)
            hid = big_of.get(item) if item else None
            cost = dict(cat=c["title"].split(":")[0], cat_no=ci + 1, n_cats=n_cats, new=new_of(c), used=used_of(c),
                        run_new=rn, run_used=ru, items=items_of(cat, hid), foot=foot)
            if ph == "cat":
                cap = c["title"]
                sub = _cat_sub(c, at_spec)
                lead["highlight"] = [big[i]["short"] for i in (c.get("items") or []) if i in big]
            else:
                b = big.get(hid)
                if b is None:
                    cap, sub = c["title"], _cat_sub(c, at_spec)
                else:
                    cap = _item_caption(b, item_new(b))
                    sub = _item_sub(b)
                    lead["highlight"] = [b["short"]]
        elif ph == "long":
            hid = big_of.get(item)
            b = big.get(hid)
            cap, sub = _long_caption(item, b, H, wk)
            cost = dict(cat="What sets the date the parts are in", n_cats=n_cats, cat_no=n_cats, new=tn, used=tu,
                        run_new=tn, run_used=tu, items=[item_row(b)] if b and b.get("new") else [], foot=foot)
            lead["highlight"] = [b["short"]] if b else []
        else:                                                    # the close: what is not on the table, the totals, the date
            k = min(1.0, t_in / 1.5)
            keys = order + extra
            rn, ru = running(keys, k) if extra else running(order, 1.0)
            bom = (hl.get("cost_bom_range") or {}).get("new") or (H.get("totals") or {}).get("new")
            cost = dict(cat="The whole machine" + (" at spec" if at_spec else ""), cat_no=n_cats, n_cats=n_cats,
                        new=tn, used=tu, run_new=rn, run_used=ru, items=[], foot=foot,
                        note=(f"BOM range, cheapest to premium option on every line: new {_m(bom)}" if bom else ""))
            if t_in < 4.0:
                cap = f"The whole machine at spec: {_m(tn)} new, {_m(tu)} with used parts where it makes sense"
                cw = hl.get("cw_chain") or {}
                sub = ("Off the table and services included. " +
                       (f"The laser, scan head, lens, collimator and scan card alone: {_m(cw.get('new'))} new, "
                        f"{_m(cw.get('used'))} used" if cw else ""))
            else:
                nw, uw = wk.get("new") or {}, wk.get("used") or {}
                if nw and uw:
                    cap = (f"Ready to assemble: {_wk(nw.get('ready_split'))} bought new, {_wk(uw.get('ready_split'))} "
                           "with the majors bought used")
                    sub = (f"Bought new, the laser sets the date (all parts in {_wk(nw.get('parts'))}); bought used, the "
                           f"fabrication does (parts in {_wk(uw.get('parts'))}). Assumes the two slow parts are swapped")
                else:
                    cap = "When the parts are in"
                    sub = "See the lead-time panel"
            lead["highlight"] = [r["name"] for r in lead_rows if r.get("long")]
        nm = dict(m)
        nm.update(caption=cap, sub=sub, who=["supplier"], cost=cost, lead=lead, chapter=TITLE, proc_s=0.0, no_clock=True)
        out.append(nm)
    (d / "meta.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    print(f"{NAME}: meta for {len(out)} frames from {H['source']}", flush=True)


def _long_caption(key, b, H, wk):
    """The long-lead beat's caption and subtitle for one close-up."""
    risks = {r.get("line"): r for r in H.get("risks") or []}
    if key == "guardswitch":
        r = risks.get("S2") or {}
        cap = "The longest lead as chosen: a $123 guard-position switch, 27 weeks + the purchase order"
        sub = ((r.get("stated") or "Digi-Key: not kept in stock; 27 weeks") + ". "
               + (r.get("action") or "Swap it for a stocked switch before ordering"))
    elif key == "relay":
        r = risks.get("H2") or {}
        cap = "Next: the Omron K8DT plate-temperature relay, out of stock until March 2027 (19 weeks)"
        sub = (r.get("action") or "Use a stocked thermostat, or order it on day one")
    elif key == "laserlead":
        nw = (wk.get("new") or {}).get("parts")
        cap = ("The laser: 12-15 weeks new (IPG, 10-12 wk after the order + BYU's PO), about a week used (eBay)")
        sub = ("A returnable 400 W IPG YLR-400-SM, $2,100 + freight, ships the same day: under BYU's $3,500 PO line. "
               + (f"Bought new, it sets the date: every part in {_wk(nw)}" if nw else ""))
    else:
        cap = "Honing the build-module bores is sent out: 3-6 weeks (estimate)"
        sub = ("Welded, bored and honed outside (BOM B1s); the honing loop sets the date for the in-house and hybrid "
               "routes (route.json)")
    return cap, sub


def _cat_of(key):
    """The kit category a big item is found under on the table (kit_table's slot category)."""
    return dict(laser="optics", galvo="optics", ftheta="optics", collimator="optics", shutter="optics",
                controller="elec", ups="elec", safety="elec", zeropoint="elec", pump="gas", o2="gas",
                blower="gas", guardswitch="elec", rackframe="frame", baseplate="stock").get(key)


def _m(v):
    import panels as P
    return P.money_range(v)


def _wk(v):
    import panels as P
    return P.weeks(v)


def _cat_sub(c, at_spec=False):
    if at_spec and c.get("spec_new"):
        s = f"at spec {_m(c['spec_new'])} new"
        su = c.get("spec_used")
        if su and su != c["spec_new"]:
            s += f", {_m(su)} with used parts where sensible"
        if c.get("new") and c["new"] != c["spec_new"]:
            s += f"; BOM range {_m(c['new'])}"
    else:
        s = f"new {_m(c['new'])}"
        if c.get("used") and c["used"] != c["new"]:
            s += f", with used parts where sensible {_m(c['used'])}"
    if c.get("bom"):
        s += "   (BOM " + ", ".join(c["bom"][:9]) + (" ..." if len(c["bom"]) > 9 else "") + ")"
    return s


def _item_caption(b, new=None):
    new = new or b["new"]
    s = f"{b['short']}: new {_m(new)}"
    if b.get("lead_new"):
        s += f", {_wk(b['lead_new'])}"
    if b.get("used"):
        s += f"; used {_m(b['used'])}"
        if b.get("lead_used"):
            s += f", {_wk(b['lead_used'])}"
    return s


def _item_sub(b):
    parts = [b["name"]]
    if b.get("new") and b.get("spec_new") and b["new"] != b["spec_new"]:
        parts.append(f"BOM range {_m(b['new'])}")
    if b.get("lead_note"):
        parts.append("new: " + b["lead_note"])
    if b.get("used_note"):
        parts.append("used: " + b["used_note"])
    elif not b.get("used"):
        parts.append("no used option counted")
    return "; ".join(parts)


if __name__ == "__main__":
    if "meta" not in sys.argv[1:]:
        render()
    write_meta()
