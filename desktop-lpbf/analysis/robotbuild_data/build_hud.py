"""Numbers for the robot-built video's cost, lead-time and time panels (issue #260, PR #266, round 7, 2026-11-25).

Sterling, 2026-11-25: "...I also want to see running cost as you show the categories (and treating the more expensive
items individually to give people a sense), and show a running total of used (i.e., eBay for the expensive laser
components for example) vs. new. I also want to see anticipated lead times for the various components ... I also want to
see time estimates for things like machining and assembly."

Nothing is fetched here: every number comes from a file in the repo, and the vendor lead times read on 2026-11-25 are in
leadtime-lookups.csv beside this script (URL and fetch time on every row).

Reads
  ../../bom.csv                        the machine, line by line (low = cheapest listed option, high = premium option)
  ../../cost/cost_scenarios.py         the repo's scenario rules (imported: read_bom, apply, read_cheaper)
  ../../cost/used-options.csv          used and new-surplus listings read on 2026-11-20, and the picks the totals use
  ../../cost/cheaper-equivalents.csv   same-spec catalogue swaps read on 2026-11-20
  ../../cad/render_build.py            the kit categories of the video's table tour (CATS, kind, kit_cat; parsed, not run)
  ../out/audit/model_tags.json         every model part with its BOM line: which lines are on the table, and where
  ../out/machining/hours.json          machining hours per part (CAM, setups, run, deburr and inspection)
  ../out/shop/timeline.json            the robot shop's hand-vs-robot timeline (older 48-part dfm.json basis)
  ../out/assembly/results.json, sequence.json   the two-arm assembly's checked steps
  leadtimes.py, leadtime-lookups.csv   new-part lead times and stock read from vendor pages on 2026-11-25, BYU's PO step
  ebay-recheck.csv                     the used picks re-read on 2026-11-25: still listed or ended, price, delivery to Provo

Writes
  ../../robot-build/hud.json           everything below, for the compositor (also copied to /tmp/robotbuild/data/hud.json);
                                       start with "tour" (display strings in tour order) and "headline"
  ../../robot-build/costs-leadtimes.csv   one row per category, item and BOM line, with source columns
  ../../robot-build/times.csv          machining per part, the robot-shop timeline, assembly per step, person steps

Things in the inputs that are stale, which this script reports rather than hides (hud.json "consistency"):
  * cost-scenarios.md's totals were written on 2026-11-20 for a $39k-113k BOM; bom.csv is now $76k-161k.
  * several used-options.csv base values predate bom.csv changes (L3, L6, G2, G7 Pirani, G9, T1, M2), so
    cost_scenarios.py's "used" totals mis-state those lines. USED_REBASE re-bases them on today's lines, and listings
    that ended by 2026-11-25 are dropped; cost_scenarios.py's own figures are written beside them.
  * 25 counted cheaper-equivalents rows replace parts no longer in their line; they are left out (consistency.cheaper_dropped).

Run from the repo root (standard library only):
    python desktop-lpbf/analysis/robotbuild_data/build_hud.py
"""
from __future__ import annotations

import ast
import csv
import datetime as dt
import json
import math
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parents[1]
OUT = LPBF / "robot-build"
TMP = pathlib.Path(os.environ.get("ROBOTBUILD", "/tmp/robotbuild")) / "data"
sys.path.insert(0, str(LPBF / "cost"))
import cost_scenarios as CS  # noqa: E402

BOM_ROWS = {r["id"]: r for r in csv.DictReader(open(LPBF / "bom.csv"))}
USED_ROWS = list(csv.DictReader(open(LPBF / "cost" / "used-options.csv")))
LOOKUPS = HERE / "leadtime-lookups.csv"

# ------------------------------------------------------------------ categories (the video's table tour)


def kit_categories():
    """CATS, kind() and kit_cat() from render_build.py, parsed with ast so they stay in step with the renderer."""
    tree = ast.parse((LPBF / "cad" / "render_build.py").read_text())
    ns: dict = {}
    cats = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("kind", "kit_cat"):
            exec(compile(ast.Module(body=[node], type_ignores=[]), "render_build.py", "exec"), ns)
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "CATS" for t in node.targets):
            cats = ast.literal_eval(node.value)
    return cats, ns["kind"], ns["kit_cat"]


CATS, KIND, KIT_CAT = kit_categories()
TAGS = json.load(open(LPBF / "analysis" / "out" / "audit" / "model_tags.json"))
RACK_U = next((int(m.group(1)) for p in TAGS for m in [re.search(r"rack frame \((\d+)U", p["part"])] if m), 12)
EXTRA_CATS = [
    ("offtable", "Bought, not on the table: powder glovebox, metal-dust vacuum, Class D extinguisher, room O2 monitor, "
                 "eyewear, laser power meter, calibration tools, optional meters"),
    ("services", "Services: machining of the custom parts (BYU shop hours or a job shop), and welding, boring and honing "
                 "of the build modules"),
]
CAT_TITLES = [(c, t.replace("{rack_u}", str(RACK_U))) for c, t in CATS] + EXTRA_CATS
ORDER = [c for c, _ in CAT_TITLES]


class _P:
    def __init__(self, d):
        self.name, self.tags, self.mat, self.mcm = d["part"], d.get("tags") or [], d.get("mat") or "", d.get("mcm") or ""


def table_placement():
    """{BOM line: {category: number of model parts}} as render_build lays them out (fasteners go in the seal zone)."""
    out: dict = {}
    for d in TAGS:
        p = _P(d)
        k = KIND(p)
        if k in ("context", "skip"):
            continue
        c = "seal" if k == "fastener" else KIT_CAT(p, k)
        out.setdefault(d.get("bom") or "", {}).setdefault(c, 0)
        out[d.get("bom") or ""][c] += 1
    return out


PLACED = table_placement()

# BOM line -> category. Chosen from PLACED (where the line's parts lie on the table, by cost not by count) and, for lines
# with no model part, from what the part is. Lines in SPLIT are divided between categories by component.
CAT_OF = {
    "L1": "optics", "L2": "optics", "L3": "optics", "L4": "optics", "L5": "optics", "L6": "optics", "L7": "optics",
    "S5": "optics", "T2": "optics",
    "C1": "elec", "C2": "elec", "C3": "elec", "C4": "elec", "C5": "elec", "C6": "elec", "M6": "elec", "S1": "elec",
    "S2": "elec", "S3": "elec", "S4": "elec", "H1": "elec", "H2": "elec", "H3": "elec", "A1": "elec", "D1": "elec",
    "D2": "elec", "E1": "elec", "E2": "elec", "E3": "elec", "E4": "elec",
    "B3": "elec",  # kit_cat has no keyword for the SCHUNK zero-point modules, so they fall to its default, "elec"
    "M1": "motion", "M2": "motion", "M3": "motion", "M4": "motion", "M5": "motion", "A3": "motion",
    "G2": "gas", "G3": "gas", "G4": "gas", "G5": "gas", "G6": "gas", "G7": "gas", "G9": "gas", "B4": "gas",
    "G8": "seal", "B2": "seal", "FX": "seal",
    "G1": "stock", "F4": "stock", "F5": "stock",
    "R1": "sheet",
    "F3": "frame",
    "P1": "offtable", "S6": "offtable", "S7": "offtable", "S8": "offtable", "T1": "offtable", "T3": "offtable",
    "E5": "offtable",
    "X1": "services",
}
# (category, low, high, what); the last entry of each takes the rest of the line
SPLIT = {
    "B1": [("stock", 793.0, 793.0, "tube, 316 bar, rod (fetched $693) and flange plate (~$100, estimate)"),
           ("services", None, None, "welding, boring, honing and machining of the three modules ($1,507-4,007, estimate)")],
    "S9": [("sheet", 508.06, 508.06, "7 x McMaster 88895K51 5052 sheet, 24 x 24 in., $72.58 each (guard panels, sliding door)"),
           ("frame", None, None, "12U rack ($250-650, estimate), 20 mm T-slot guard frame, brackets, nuts, wheels")],
    "A2": [("optics", 1356.0, 1612.0, "AR-coated cover slides: Edmund 36-299 x 12 + Cloudray PW02FS50X2 x 10 (consumables)"),
           ("sheet", 36.88, 36.88, "lift-out wall liners (McMaster 2317K278 sheet)"),
           ("offtable", None, None, "metal-dust vacuum, McMaster 5572N116 ($3,189.78)")],
}
# scenario deltas of these components go to a named split part (else the line's last split entry)
DELTA_CAT = {"A2:5572N116": "offtable", "S9:88895K51": "sheet"}

# ------------------------------------------------------------------ the four scenarios, re-based on today's bom.csv

CW_CHAIN = ["L1", "L3", "L5", "L6", "C1"]
USED_REBASE = {  # used-options.csv `replaces` key -> today's base for that component (low, high), and why
    "L3:collimator": dict(base=(0.0, 790.0), why="L3's high end is now the Jenoptik 1.5x expander ($790, Edmund 73-122, "
                          "read 2026-11-25), not the $512.24 expander of 2026-11-20"),
    "L6:lens": dict(base=(1011.78, 2500.0), why="L6's low end is now the Thorlabs FTH160-1064 ($1,011.78; its two spare "
                    "windows stay), not a $486 lens"),
    "G2:4396K21": dict(drop=True, why="the 4396K21 rotary vane is no longer in G2: both ends are dry scrolls now"),
    "G2:dry-scroll": dict(base=(3979.0, 5977.85), both=True, why="G2's low end is the Agilent IDP-3 at its $3,979 list and "
                          "its high end the Edwards nXDS6i at $5,977.85; the used IDP-3 ($1,284.58 shipped) replaces either"),
    "G7:pirani": dict(base=(455.0, 455.0), why="G7 now carries the Vacuum Research 902377 Pirani ($455), not a $300-800 "
                      "estimate"),
    "G9:dewpoint": dict(base=(1868.0, 2281.70), why="G9 is now the Vaisala DMT143 ($1,868-2,281.70), not a $1,000-2,500 "
                        "estimate"),
    "T1:power-sensor": dict(base=(2785.0, 2785.0), both=True, why="T1 is now the Gentec-EO UP55M-500W head + U-LINK "
                            "($2,785) at both ends; the used Ophir head + Nova II meter replaces both"),
    "M2:servo-1": dict(base=(265.0, 293.0), why="M2 is now 2 x $265-293; the open-box ClearPath replaces one of them"),
}
USED_EXTRA = [  # used-options.csv listings that cost_scenarios.py doesn't count because their line came later
    dict(key="D2:ups", line="D2", base=(1137.99, 2706.99), match="SMX1500RM2U",
         why="D2 (the UPS) entered bom.csv on 2026-11-22, after the used search: the refurbished APC SMX1500RM2U "
             "(1500 VA) covers the 705 W load tray_budget.md sizes, as either D2 option does"),
]


def num(x):
    return CS.num(x)


RECHECK_CSV = HERE / "ebay-recheck.csv"   # the used picks re-read on 2026-11-25 (ebay_recheck.py, fetch_pages.py)


def recheck_for(url):
    """The 2026-11-25 re-read of a used listing (matched on its eBay item number or URL), or None."""
    if not RECHECK_CSV.exists():
        return None
    m = re.search(r"/itm/(\d+)", url or "")
    for r in csv.DictReader(open(RECHECK_CSV)):
        if (m and r["ebay_item"] == m.group(1)) or (not m and r["ebay_item"] == "(dealer site)" and
                                                     r["replaces"] in ("L5:head",) and "nextdayautomation" in (url or "")):
            return r
    return None


def live(r):
    rc = recheck_for(r["url"])
    return not rc or rc["status_2026_11_25"] == "still listed"


def used_cost(r):
    """A used listing's price + shipping + estimated extras, at its 2026-11-25 price where it was re-read."""
    rc = recheck_for(r["url"])
    price = num(rc["price_usd_now"]) if rc and num(rc["price_usd_now"]) is not None else num(r["price_usd"])
    return (price or 0.0) + (num(r["shipping_usd"]) or 0.0) + (num(r["extra_usd"]) or 0.0)


def read_used_rebased():
    """Like cost_scenarios.read_used(), with USED_REBASE applied, USED_EXTRA added and the listings that ended by
    2026-11-25 dropped (ebay-recheck.csv; the other end's pick then covers both ends). Returns (components, notes)."""
    comp, notes = {}, []
    dropped_low = set()
    for r in USED_ROWS:
        pick, key = r["pick"].strip(), r["replaces"]
        if not pick or not key:
            continue
        if not live(r):
            rc = recheck_for(r["url"])
            notes.append(dict(key=key, change=f"{pick} pick dropped: {r['item_as_listed'][:60]}",
                              why=f"{rc['status_2026_11_25']} on 2026-11-25 ({rc['notes'][:160]})"))
            if "low" in pick:
                dropped_low.add(key)
            continue
        fix = USED_REBASE.get(key, {})
        if fix.get("drop"):
            if key not in [n["key"] for n in notes]:
                notes.append(dict(key=key, change="dropped", why=fix["why"]))
            continue
        base = fix.get("base", (num(r["base_low_usd"]) or 0.0, num(r["base_high_usd"]) or 0.0))
        c = comp.setdefault(key, {"line": r["bom_line"], "base_low": base[0], "base_high": base[1], "low": None, "high": None})
        cost = used_cost(r)
        ends = ("low", "high") if fix.get("both") else tuple(e for e in ("low", "high") if e in pick)
        for end in ends:
            c[end] = (c[end] or 0.0) + cost if not fix.get("both") else cost
        if fix and key not in [n["key"] for n in notes]:
            notes.append(dict(key=key, change=f"base {num(r['base_low_usd'])}/{num(r['base_high_usd'])} -> {base[0]}/{base[1]}"
                              + (", applied at both ends" if fix.get("both") else ""), why=fix["why"]))
    for key in dropped_low:  # the remaining (high) pick covers the low end too
        c = comp.get(key)
        if c and c["low"] is None and c["high"] is not None:
            c["low"] = c["high"]
    for x in USED_EXTRA:
        r = next(r for r in USED_ROWS if x["match"] in r["item_as_listed"])
        cost = used_cost(r)
        comp[x["key"]] = {"line": x["line"], "base_low": x["base"][0], "base_high": x["base"][1], "low": cost, "high": cost}
        notes.append(dict(key=x["key"], change=f"added: {r['item_as_listed']} ${cost:,.2f}", why=x["why"]))
    return comp, notes


def bom_corpus(line):
    """Today's part numbers for a BOM line: its candidate text plus the current component tables."""
    text = BOM_ROWS[line]["candidate"] if line in BOM_ROWS else ""
    for r in csv.DictReader(open(LPBF / "electrical-bom.csv")):
        if (r.get("bom.csv line (replaces / adds to)") or "").split(" ")[0] == line:
            text += " " + r["part number"]
    if line == "FX":
        text += " " + " ".join(r["part_number"] for r in csv.DictReader(open(LPBF / "fasteners.csv")))
    if line == "G7":  # G7's McMaster subtotal is its mcmaster-parts.csv rows, less the 4277T52 and the 4518K73 it replaced
        text += " " + " ".join(r["part_number"] for r in csv.DictReader(open(LPBF / "mcmaster-parts.csv"))
                               if r["bom_line"].startswith("G7") and r["part_number"] not in ("4277T52", "4518K73"))
    # P1's low end is its alternative, McMaster 4083N11 ($1,693.76); H1 writes 3869K34 as "3869K35/34"
    return text + {"H1": " 3869K34", "P1": " 4083N11"}.get(line, "")


def read_cheaper_current():
    """cost_scenarios.read_cheaper(), keeping only rows whose replaced part is still in today's line."""
    keep, dropped = {}, []
    for r in csv.DictReader(open(LPBF / "cost" / "cheaper-equivalents.csv")):
        if r.get("counted", "").strip().lower() != "yes" or num(r["alt_line_usd"]) is None:
            continue
        line = r["bom_line"].split(",")[0].strip()
        toks = re.findall(r"\b\d{3,5}[A-Z]\d{1,4}\b|\b[A-Z0-9][A-Z0-9-]{4,}\b", r["base_part"])
        if not toks or not any(t in bom_corpus(line) for t in toks):
            dropped.append(dict(line=line, key=r["replaces"], base_part=r["base_part"][:60],
                                saving=round((num(r["base_line_usd"]) or 0) - (num(r["alt_line_usd"]) or 0), 2)))
            continue
        alt = num(r["alt_line_usd"])
        c = keep.setdefault(r["replaces"], {"line": r["bom_line"], "base_low": num(r["base_low_usd"]) or 0.0,
                                            "base_high": num(r["base_high_usd"]) or 0.0, "low": None, "high": None})
        for end in ("low", "high"):
            c[end] = alt if c[end] is None else min(c[end], alt)
    return keep, dropped


def cheaper_rows():
    """The counted cheaper-equivalents rows whose replaced part is still in today's line, for the item callouts."""
    out = []
    for r in csv.DictReader(open(LPBF / "cost" / "cheaper-equivalents.csv")):
        if r.get("counted", "").strip().lower() != "yes" or num(r["alt_line_usd"]) is None:
            continue
        line = r["bom_line"].split(",")[0].strip()
        toks = re.findall(r"\b\d{3,5}[A-Z]\d{1,4}\b|\b[A-Z0-9][A-Z0-9-]{4,}\b", r["base_part"])
        if not toks or not any(t in bom_corpus(line) for t in toks):
            continue
        out.append(dict(line=line, key=r["replaces"], replaces=r["base_part"], alt_vendor=r["alt_vendor"],
                        alt_part=r["alt_part_number"], base_usd=num(r["base_line_usd"]), alt_usd=num(r["alt_line_usd"]),
                        saving=round((num(r["base_line_usd"]) or 0) - (num(r["alt_line_usd"]) or 0), 2),
                        same_spec=r["same_spec"], lead_time_note=r["lead_time_note"], url=r["alt_url"],
                        fetched_utc=r["fetched_utc"], source="cost/cheaper-equivalents.csv"))
    out.sort(key=lambda o: -o["saving"])
    return out


CHEAPER_ROWS = cheaper_rows()


def at_spec(lines, sc_new, sc_used, used):
    """cost_scenarios.py's at-spec rule, per line: the CW chain at spec (new = the BOM's high end; used = the used picks,
    as that script takes them), the cheapest listed option everywhere else (the scenario's low end)."""
    new, ulo, uhi = {}, {}, {}
    keymap = {"L1": "L1:laser", "L3": "L3:collimator", "L5": "L5:head", "L6": "L6:lens", "C1": "C1:controller"}
    for k in lines:
        if k in keymap:
            new[k] = lines[k]["high"]
            u = used.get(keymap[k], {})
            lo = u.get("low") if u.get("low") is not None else (0.0 if k == "L3" else u.get("high"))
            hi = u.get("high") if u.get("high") is not None else lo
            ulo[k], uhi[k] = lo, hi
        elif k == "L2":
            new[k] = ulo[k] = uhi[k] = 0.0
        else:
            new[k] = sc_new[k][0]
            ulo[k] = uhi[k] = sc_used[k][0]
    return new, ulo, uhi


# ------------------------------------------------------------------ the expensive items, one by one

def used_row(match):
    r = next(r for r in USED_ROWS if match in r["item_as_listed"] or match in r["url"])
    cond = r["condition"]
    rc = recheck_for(r["url"])
    return dict(title=r["item_as_listed"], condition=cond, price=num(r["price_usd"]), shipping=num(r["shipping_usd"]),
                extra=num(r["extra_usd"]), extra_note=r["extra_note"], total=round(used_cost(r), 2),
                location=r["location"], returns=r["returns_warranty"], seller_type=r["seller_type"], url=r["url"],
                fetched_utc=r["fetched_utc"], verdict=r["verdict"], risks=r["checks_and_risks"],
                source="cost/used-options.csv (eBay, read through the lab Pi on 2026-11-20)",
                live=live(r),
                recheck=(dict(status=rc["status_2026_11_25"], price_now=num(rc["price_usd_now"]),
                              shipping=rc["shipping_as_listed"], delivery_to_provo=rc["delivery_to_84602_as_listed"],
                              days=[int(rc["days_to_provo_low"]), int(rc["days_to_provo_high"])]
                              if rc["days_to_provo_low"] else None,
                              returns=rc["returns_as_listed"], fetched_utc=rc["fetched_utc"], notes=rc["notes"],
                              source="analysis/robotbuild_data/ebay-recheck.csv") if rc else None))


# kind: item = one purchasable unit; bundle = a BOM line of many parts. new_drawn = the part the model draws, new.
ITEMS = [
    dict(id="L1", line="L1", cat="optics", kind="item", name="Fiber laser, 500 W single-mode (IPG YLR-500-U3-SM-AC)",
         new_low=3300, new_high=23000, new_drawn=23000,
         new_src="IPG budgetary quote 2026-11-18, ~$23k rounded to $1k (quotes/ipg-ylr-500-u3-sm-ac.md); low end = a Raycus "
                 "estimate that isn't confirmed single-mode (bom.csv L1)",
         used=["M6860"], used_alt=["SEM-I-1676", "M6861", "YLR-400-WC 400W CW Fiber Laser - 1070nm (2019)"],
         risk="Try the $2,099.99 YLR-400-SM-EOS (US dealer, 'mint condition, all warranty seals in place', 30-day "
              "returns, seller pays return shipping) first, and test it inside the 30 days. The $1,299.99 unit from the same "
              "dealer has a cut fibre ('Laser cable was cut'): an IPG repair, not a $1.3k laser. The Korean YLR-500-AC takes "
              "no returns. No listing states hours, cooling or back-reflection protection: give IPG the serial number."),
    dict(id="L5", line="L5", cat="optics", kind="item", name="Galvo scan head (SCANLAB basiCube 20)",
         new_low=419, new_high=12000, new_drawn=12000,
         new_src="$12,000 is bom.csv L5's placeholder for a SCANLAB quote not yet requested (estimate); low end = a Sino-Galvo "
                 "marking head, under spec; Thorlabs QS20XY-Y1 is $5,893.56 new (bom.csv L5)",
         used=["SCANLAB hurrySCAN 25, 1500 W"], used_alt=["Intelliscan"],
         risk="Check the head's protocol (XY2-100 vs SL2-100) against the card, and its mirrors' CW rating at 1070 nm. "
              "Used heads need their own DC supply (~$150, estimate)."),
    dict(id="C1", line="C1", cat="elec", kind="item", name="Scan card (SCANLAB RTC6)",
         new_low=125, new_high=6065, new_drawn=6065,
         new_src="$6,000 is bom.csv C1's placeholder for a SCANLAB RTC6 quote (estimate) + $65 laser-connector breakout; low "
                 "end = open-source OPAL on a Teensy ($60, 'PRE ALPHA') + breakout",
         used=["Scanlab RTC5 PCIe"], used_alt=["RTC6 PCI EXpress"],
         risk="The used card is an RTC5 (PCIe), tested by the seller on an IPG YLR; it needs a Windows PC with a PCIe slot "
              "(C2 at its $600 end) and SCANLAB's driver and DLL: ask SCANLAB whether a second-hand card can register."),
    dict(id="L6", line="L6", cat="optics", kind="item", name="f-theta lens, f = 160 mm (Thorlabs FTH160-1064 + 2 windows)",
         new_low=1255.84, new_high=2500, new_drawn=1255.84,
         new_src="Thorlabs FTH160-1064 $1,011.78 + 2 x FTHW75-1064 $122.03 (read 2026-11-22, bom.csv L6); high = a Sill "
                 "lens qualified for 500 W CW ($2,500-6,000, quote)",
         used=["LINOS F-THETA-RONAR 4401-288-000-20 1064NM"], used_alt=["Linos F-Theta Ronar 4401-288-000-20 Lens f=254mm"],
         risk="The used lenses are f = 254 mm marking lenses with no CW rating: the spot grows ~1.6x and the optics bridge "
              "moves up. Fine for early tracks; not the drawn lens."),
    dict(id="L3", line="L3", cat="optics", kind="item", name="Collimator (IPG affixed 2.5 mm, with the laser)",
         new_low=0, new_high=790, new_drawn=0,
         new_src="IPG collimator price comes with the laser quote (not yet given: TBD); high = Jenoptik 1.5x expander, "
                 "Edmund 73-122, $790 (read 2026-11-25)",
         used=["P30-001277"], used_alt=[],
         risk="A used laser usually keeps its own output optics ($0); the eBay IPG collimator's beam diameter and connector "
              "aren't stated."),
    dict(id="L4", line="L4", cat="optics", kind="item", name="Safety shutter + beam dump (>= 500 W CW)",
         new_low=507.50, new_high=2000, new_drawn=2000,
         new_src="bom.csv L4: no catalogue shutter rated >= 500 W CW at 1070 nm was found (optics-bom.csv O3): quote; "
                 "$2,000 is an estimate",
         used=[], used_alt=[], risk="Buy new: it is a safety element."),
    dict(id="L2", line="L2", cat="optics", kind="item", name="Laser chiller (only for a water-cooled laser)",
         new_low=0, new_high=3000, new_drawn=0,
         new_src="bom.csv L2: the quoted IPG is forced-air cooled, so $0; up to $3,000 (estimate) if a water-cooled laser "
                 "is bought, e.g. the used YLR-400-WC fallback",
         used=[], used_alt=[], risk="Not searched used (cost-scenarios.md section 6)."),
    dict(id="G2", line="G2", cat="gas", kind="item", name="Dry scroll vacuum pump (Edwards nXDS6i)",
         new_low=3979, new_high=5977.85, new_drawn=5977.85,
         new_src="nXDS6i $5,977.85 at Marshall Scientific (list $9,603), read 2026-11-22; low = Agilent IDP-3 at its $3,979 "
                 "list (search snippet); the line adds $1,491.31 of filter and hoses (bom.csv G2)",
         used=["IDP3 Dry Scroll"], used_alt=["EDWARDS RV3", "TriScroll 300", "XDS10"],
         risk="Ask the seller for hours and tip-seal condition; a tip-seal kit may be needed (not priced). The $460.69 "
              "Edwards RV3 is an oil-sealed rotary vane (free returns): a budget route, not the dry pump drawn."),
    dict(id="G6", line="G6", cat="gas", kind="item", name="Trace O2 analyzer (Ntron Microx)",
         new_low=1271.07, new_high=2091, new_drawn=2091,
         new_src="Ntron Microx at Instrumart $1,694-2,091 (agent-sourced, bom.csv G6); low = SST OXY-FLEX-0-H at DigiKey "
                 "$1,271.07, which may be a percent-level sensor (cost-scenarios.md section 5 item 6)",
         used=["ALPHA OMEGA,SERIES 3000"], used_alt=["3190 | Teledyne"],
         risk="A used trace analyzer usually needs a new sensor cell (~$350, estimate) and a check of its lowest range "
              "(< 100 ppm)."),
    dict(id="G9", line="G9", cat="gas", kind="item", name="Dew-point transmitter (Vaisala DMT143)",
         new_low=1868, new_high=2281.70, new_drawn=2281.70,
         new_src="Selectum (a Vaisala distributor) $2,281.70, '2 Weeks Factory Lead Time', special order, non-returnable "
                 "(read 2026-11-22); $1,868 for one configuration (search snippet)",
         used=["Atlas Copco P1624896681"], used_alt=["MICHELL Easidew"],
         risk="Check the calibration date; recalibrate if it is old."),
    dict(id="G4", line="G4", cat="gas", kind="item", name="Sealed recirculation blower (gas-tight, ~100 L/min)",
         new_low=300, new_high=1500, new_drawn=1500,
         new_src="bom.csv G4: estimate; no gas-tight blower of this size was found (real-parts.md); 'this line is the "
                 "largest open purchase'",
         used=[], used_alt=["Regeniar R1102"],
         risk="Used regenerative blowers aren't shown to be gas-tight (cost-scenarios.md)."),
    dict(id="B3", line="B3", cat="elec", kind="item", name="Zero-point clamps (2 x SCHUNK VERO-S NSE-HT mini 88-20)",
         new_low=5770, new_high=6380, new_drawn=6380,
         new_src="NSE-HT $2,680 each at MROSupply (re-checked 2026-11-23) + 6 SPC-HT mini 20 pins (no published price, "
                 "$60-150 each, estimate) + stock and studs (estimate) (bom.csv B3)",
         used=[], used_alt=[], risk="Not searched used. kit_cat() puts these in the electronics zone of the table."),
    dict(id="S1", line="S1", cat="elec", kind="item", name="Safety controller (Banner XS26-2 + XS16si + XS2so) and contactors",
         new_low=2376.01, new_high=2376.01, new_drawn=2376.01,
         new_src="electrical-bom.csv (read 2026-11-22): XS26-2 $1,093.01, XS16si $464, XS2so $370, SC-USB2, 4 WEG "
                 "CWBS9-33-30C03 contactors $108 each",
         used=[], used_alt=[], risk="Buy safety parts new and traceable (cost-scenarios.md: used 'new' Omron relays from "
                                    "China are the counterfeit risk)."),
    dict(id="C5", line="C5", cat="elec", kind="bundle", name="PLC with thermocouple and 4-20 mA I/O (AutomationDirect Productivity1000)",
         new_low=1092.50, new_high=1092.50, new_drawn=1092.50,
         new_src="electrical-bom.csv (read 2026-11-22): P1-540 CPU + 8 I/O modules + terminal blocks",
         used=[], used_alt=[], risk="Not searched used."),
    dict(id="D2", line="D2", cat="elec", kind="item", name="UPS, 2U (Eaton 5PX1500RTG2)",
         new_low=1137.99, new_high=2706.99, new_drawn=1137.99,
         new_src="CDW $1,137.99 (Eaton, drawn) and $2,706.99 (Vertiv GXT5, the one tray_budget.md sizes), both 'Item "
                 "Backordered', read 2026-11-22",
         used=["SMX1500RM2U"], used_alt=[],
         risk="Refurbished UPS batteries: ask the refurbisher for the battery date, or budget new batteries."),
    dict(id="T1", line="T1", cat="offtable", kind="item", name="Laser power meter, 500 W (Gentec-EO UP55M head + U-LINK)",
         new_low=2785, new_high=2785, new_drawn=2785,
         new_src="Gentec-EO UP55M-500W-H12-D0 $1,969 + U-LINK $816 (read 2026-11-22/23, bom.csv T1)",
         used=["L1500W-LP1"], used_alt=[],
         risk="The used Ophir L1500W head comes from China and the Nova II meter from a US seller; recalibrate both."),
    dict(id="P1", line="P1", cat="offtable", kind="item", name="Powder glovebox (McMaster 4083N14)",
         new_low=1693.76, new_high=4305.48, new_drawn=4305.48,
         new_src="McMaster 4083N14 $4,305.48 with humidity meter and two gas ports; 4083N11 $1,693.76 (bom.csv P1)",
         used=[], used_alt=["MBRAUN"], cheaper="Cleatech 2100-2 with airlock, $2,135 at Lab Supply Network (acrylic; "
                                                  "cost/cheaper-equivalents.csv)",
         risk="Used inert gloveboxes were $3,000-7,875, so not cheaper (cost-scenarios.md)."),
    dict(id="A2v", line="A2", cat="offtable", kind="item", name="Metal-dust vacuum (McMaster 5572N116, NFPA 484)",
         new_low=3189.78, new_high=3189.78, new_drawn=3189.78,
         new_src="McMaster 5572N116 $3,189.78 (Class II Div 1/2, Groups E-G; needs 35 scfm air) (bom.csv A2)",
         used=[], used_alt=[], cheaper="Dynabrade 61470 at TA Industrial $2,787.53, very likely the same unit; confirm NFPA 484 "
                                       "(cost/cheaper-equivalents.csv)",
         risk="Buy new (combustible-dust equipment)."),
    dict(id="F4", line="F4", cat="stock", kind="item", name="MIC-6 cast plate, 5/8 x 24 x 72 in. (McMaster 86825K49)",
         new_low=1348.88, new_high=1498.88, new_drawn=1348.88,
         new_src="McMaster 86825K49 $1,348.88, one sheet nests both module base plates (read 2026-11-22); + up to $150 "
                 "waterjet (estimate)",
         used=[], used_alt=[], risk=""),
    dict(id="G1", line="G1", cat="stock", kind="bundle", name="Chamber stock: 6061-T651 5-1/2 in. frame blank and 1 in. / 3/4 in. plate",
         new_low=1323.41, new_high=1623.41, new_drawn=1323.41,
         new_src="frame blank 5-1/2 x 9.5 x 15 in. $590.89 (Midwest Steel & Aluminum, read 2026-11-22; McMaster stops at "
                 "4 in.), 89155K165 $267.02, 89155K155 $211.96, 2 draw latches $103.54; sheet and bar $150-450 (estimate)",
         used=[], used_alt=[], risk=""),
    dict(id="H1", line="H1", cat="elec", kind="bundle", name="Heater stacks, weld-in feedthroughs and thermocouples (3 modules)",
         new_low=3753.58, new_high=4273.58, new_drawn=3753.58,
         new_src="electrical-bom.csv (read 2026-11-22): McMaster cartridges and thermocouples; Solid Sealing FA11631 x 9 "
                 "and FA11632 x 9 at $44, FA10443 x 3 at $92 ($1,068 of weld-ins)",
         used=[], used_alt=[], risk=""),
    dict(id="G7", line="G7", cat="gas", kind="bundle", name="Valves, KF fittings, hoses and gauges",
         new_low=3889.50, new_high=4189.50, new_drawn=3889.50,
         new_src="McMaster subtotal $2,961.58 (read 2026-11-17/22) + Pirani $455 and adapters + relief and SAE adapter "
                 "estimates (bom.csv G7)",
         used=["PVG-500"], used_alt=["CVM211GBL"],
         risk="The KF-25 hoses (5 x 3497N23 across G2 and G7) are the biggest piece; Kurt J. Lesker's MHB-QF-B24 saves $825 "
              "new."),
    dict(id="X1", line="X1", cat="services", kind="bundle", name="Machining of the custom parts (193-208 shop hours)",
         new_low=7708, new_high=20770, new_drawn=7708,
         new_src="bom.csv X1: 193 h at $40/h (assumed in-house) to 208 h at $100/h (assumed job shop); not quoted",
         used=[], used_alt=[], risk="outsourcing.md's recommended split (152 h here, the rest to SendCutSend and JLCCNC) "
                                    "is $25,667 at $65/h including $3,695 of tools; not in bom.csv."),
    dict(id="B1s", line="B1", cat="services", kind="bundle", name="Build modules: welding, boring and honing (3 modules)",
         new_low=1507, new_high=4007, new_drawn=1507,
         new_src="bom.csv B1 notes: welding, boring, honing and machining $1,500-4,000 (estimates); honing has no "
                 "published price ($150-400 a bore, estimate, outsourcing.md)",
         used=[], used_alt=[], risk="No honing shop published a lead time: plan 3-6 weeks (estimate, outsourcing.md)."),
    dict(id="A1", line="A1", cat="elec", kind="bundle", name="Step-confirm sensors, NFC and load cell (incl. Omron fibre amplifier)",
         new_low=1527.82, new_high=1996, new_drawn=1527.82,
         new_src="electrical-bom.csv (read 2026-11-22); Omron E32-T61-S + E3NX-FA41 $900.12",
         used=[], used_alt=[], risk="E3NX-FA41 listed a 33-week factory lead time with 5 in stock (DigiKey, 2026-11-17)."),
    dict(id="M1", line="M1", cat="motion", kind="bundle", name="Recoater axis: ball screw, rail, Ferrotec feedthrough",
         new_low=1325.88, new_high=2345.88, new_drawn=1325.88,
         new_src="McMaster subtotal $815.88 (read 2026-11-17); Ferrotec SFL-006-NN $500-1,500 (no published price, estimate)",
         used=[], used_alt=[], risk=""),
    dict(id="M3", line="M3", cat="motion", kind="item", name="Z actuator (THK KR26, 2 mm lead)",
         new_low=923, new_high=1113, new_drawn=923,
         new_src="THK KR2602A-0110-0-01A0 $883 at Oriental Motor (a THK reseller) + belt and pulleys $40-80 (estimate)",
         used=[], used_alt=[], risk=""),
    dict(id="M2", line="M2", cat="motion", kind="item", name="2 servos (Teknic ClearPath-SD, NEMA 23)",
         new_low=530, new_high=586, new_drawn=530,
         new_src="Teknic CPM-SDSK-2311S-RLN $265-293 each (read 2026-11-20)",
         used=["CPM-SDSK-2310S-RQN"], used_alt=[], risk="The open-box unit is a 2310S, one size down from the 2311S drawn: "
                                                      "check its torque against the recoater and Z loads."),
    dict(id="T2", line="T2", cat="optics", kind="bundle", name="Melt-pool photodiode chain (Thorlabs)",
         new_low=2059.45, new_high=2409.45, new_drawn=2059.45,
         new_src="Thorlabs PDA36A2 $400.01, DMSP1000 $331.76, NF1064-44 $635.55, NB1-K14, FESH1000 (read 2026-11-13/23) + "
                 "mounts (estimate)", used=[], used_alt=[], risk=""),
    dict(id="A2s", line="A2", cat="optics", kind="bundle", name="Cover slides, AR-coated (consumables)",
         new_low=1356, new_high=1612, new_drawn=1356,
         new_src="Edmund 36-299 x 12 + Cloudray PW02FS50X2 x 10 trial (bom.csv A2)", used=[], used_alt=[], risk=""),
    dict(id="S9", line="S9", cat="frame", kind="bundle", name="12U rack, T-slot guard frame and guard panels",
         new_low=1136.35, new_high=1786.35, new_drawn=1136.35,
         new_src="McMaster guard parts $886.35 (read 2026-11-17/22); 12U rack $250-650 (estimate)", used=[], used_alt=[],
         risk=""),
    dict(id="D1", line="D1", cat="elec", kind="bundle", name="Tray dock and umbilicals (HARTING Han-Modular)",
         new_low=538.86, new_high=5627.60, new_drawn=538.86,
         new_src="HARTING frame and modules $261.26 (electrical-bom.csv E7) + estimates; high = a Staubli CombiTac "
                 "($1,500-5,000, estimate)", used=[], used_alt=[], risk=""),
    dict(id="A3", line="A3", cat="motion", kind="bundle", name="Door drive and latch pneumatics (SMC)",
         new_low=1139.43, new_high=1289.43, new_drawn=1139.43,
         new_src="electrical-bom.csv / audit-prices.csv (Motion, SMC; read 2026-11-22)", used=[], used_alt=[], risk=""),
    dict(id="S7", line="S7", cat="offtable", kind="item", name="Room O2-deficiency monitor (Macurco OX-6)",
         new_low=663, new_high=1275, new_drawn=663,
         new_src="Kele $663 (search extract), list $1,275 (bom.csv S7)", used=[], used_alt=[], risk="Buy new (life safety)."),
    dict(id="S8", line="S8", cat="offtable", kind="item", name="Class D extinguisher, 30 lb (McMaster 6435T23)",
         new_low=920.22, new_high=920.22, new_drawn=920.22, new_src="McMaster 6435T23 (bom.csv S8)", used=[], used_alt=[],
         risk="Buy new."),
]

# ------------------------------------------------------------------ lead times (leadtimes.py beside this script)
sys.path.insert(0, str(HERE))
import leadtimes as LTM  # noqa: E402


def load_lookups():
    if not LOOKUPS.exists():
        return []
    return list(csv.DictReader(open(LOOKUPS)))


# ------------------------------------------------------------------ times


def machining_times():
    h = json.load(open(LPBF / "analysis" / "out" / "machining" / "hours.json"))
    rows = []
    for p in h["parts"]:
        rows.append(dict(part=p["part"], mat=p["mat"], setups_3axis=p["setups_3axis"], setups_4th=p["setups_4th_axis"],
                         holes=p["holes"], cam_h=p["cam_h"], setup_h_3axis=p["setup_h_3axis"], setup_h_4th=p["setup_h_4th"],
                         run_h=p["run_h"], run_h_vendor=p.get("run_h_vendor"), run_h_program=p.get("run_h_program"),
                         deburr_inspect_h=p["deburr_inspect_h"], total_h_3axis=p["total_h_3axis"],
                         total_h_4th=p["total_h_4th"], special=p.get("special", "")))
    return dict(totals=h["totals"], parts=rows, method=h["method"], chamber=h["new_body"],
                source="analysis/out/machining/hours.json (hours.py; CAM hours are an estimate with no published rule)")


def shop_timeline():
    t = json.load(open(LPBF / "analysis" / "out" / "shop" / "timeline.json"))
    keep = ("n_parts", "n_pieces", "setups", "cut_h", "setup_h_hand", "robot_changeover_s", "total_hand_person_h",
            "total_shop_person_h", "total_shop_person_h_cautious", "shop_machine_h", "days_hand", "days_shop")
    return dict({k: t[k] for k in keep}, rows=t["rows"], not_included=t["not_included"],
                basis=f"analysis/out/shop/timeline.json, from the older dfm.json of {t['dfm_json_mtime_utc']} "
                      "(48 parts, 27.7 h cutting); hours.json (57 parts) supersedes its CAM and setup hours")


# Real-world seconds per assembly step: ESTIMATES (results.json's "seconds" is the checker's compute time, not a duration)
ASM = dict(place_s=30.0, insert_mm_s=10.0, screw_s=15.0, screw_setup_s=20.0, tool_change_s=15.0, seal_s=90.0, flip_s=30.0,
           dual_s=60.0, rotate_s=20.0, machine_s=10.0)
# person steps (minutes, estimate): by step id; failed robot steps fall back to a person at these minutes
PERSON_MIN = {
    "M09": (10, "felt strip and split PTFE scraper wrapped into the head's groove"),
    "C00": (10, "overflow funnel on the bench: O-ring, block and four M4 screws"),
    "C02": (5, "dowel and diamond pin pressed in with an arbor press (1,644 N; the arm pushes 149 N)"),
    "C09e": (5, "M5 push-in elbows and a temporary release-air line"),
    "C15b": (5, "overflow-jar sensor and its bracket on the bench"),
    "F06b": (10, "release-air tube routed from the valve to both zero-point modules"),
    "F08": (1, "KF-40 toggle clamp round the jar's flange"),
    "F12": (10, "through-beam fibre heads threaded into the side walls"),
    "F49": (10, "pressure transducer and relief valve into their SAE-4 ports, with a wrench"),
    "F53": (10, "f-theta lens threaded into its ring over the shim stack (strap wrench)"),
    "F58": (15, "armoured process fiber routed to the collimator"),
    "F59": (180, "Class 1 laser guard: T-slot frame, panels, door rail, sliding door, guard lock, operator panel"),
    "T01": (30, "process module (84 kg) onto the VLM tray with a hoist; levelling mounts"),
    "T02": (60, "rack units: UPS 23 kg, laser 40 kg, PC, DIN drawer (lift)"),
    "T03": (60, "gas module: pump 26 kg, blower, filter, O2 box, argon manifold (lift)"),
    "T04": (60, "KF bellows, vacuum valve, argon and O2 lines, release air"),
    "T05": (45, "tray dock and umbilicals"),
    "F02": (0, "levelling mounts go on in T01"),
}
FAIL_MIN = 5.0          # a failed robot step done by a person instead (estimate), per step; screws: 1 min each
PARTS_PER_TRIP = 4      # parts a MiR brings from the long table per trip, in a tote (estimate)
TRIP_S = 2 * (25.0 + 30.0 + 15.0)   # two legs, two dockings, two AprilTag registrations (analysis/shop/timeline.py)
SHOP_NOTES_MIN = {"M02": (3, "three M3 helical inserts, in the shop after tapping"),
                  "M25": (120, "seven weld-in feedthroughs TIG-welded into the rod end (welder)")}


def path_len(wps):
    return sum(math.dist(a, b) for a, b in zip(wps, wps[1:])) if wps and len(wps) > 1 else 0.0


def chapter_of(step_id):
    return {"M": "40-assembly-module", "C": "41-assembly-chamber", "F": "41-assembly-chamber",
            "T": "50-integration"}.get(step_id[0], "other")


def assembly_times():
    res = json.load(open(LPBF / "analysis" / "out" / "assembly" / "results.json"))["rows"]
    seq = {s["id"]: s for s in json.load(open(LPBF / "analysis" / "out" / "assembly" / "sequence.json"))["steps"]}
    rows, last_tool = [], None
    for r in res:
        sid, do = r["id"], r["do"]
        who = r.get("who") or ""
        st = "pass"
        robot_s = person_min = 0.0
        why = ""
        if do == "note":
            if who.startswith("person"):
                person_min, why = PERSON_MIN.get(sid, (10, "person step (estimate)"))
                st = "person"
            elif who == "machine shop":
                person_min, why = SHOP_NOTES_MIN.get(sid, (10, "machine shop"))
                st = "shop"
            elif who == "machine":
                robot_s = 3600.0 if sid == "T06" else ASM["machine_s"]
                why = "leak check: rate of rise from <= 1 mbar and O2 drift (estimate 1 h)" if sid == "T06" else "machine"
                st = "machine"
            else:  # robot with a custom bit, e.g. F40
                robot_s, why = 2 * ASM["screw_s"], "robot (custom bit)"
        else:
            tool = r.get("tool")
            if tool and tool != last_tool and do in ("place", "screws", "seal"):
                robot_s += ASM["tool_change_s"]
                last_tool = tool
            if do == "place":
                robot_s += ASM["place_s"] + path_len(seq.get(sid, {}).get("waypoints") or []) / ASM["insert_mm_s"]
            elif do == "screws":
                n_ok = r.get("n_ok") or 0
                n = r.get("n") or 0
                robot_s += (ASM["screw_setup_s"] + ASM["screw_s"] * n_ok) if n else 0.0
                if n and n_ok < n:
                    person_min += (n - n_ok) * 1.0
                    st = "fail" if n_ok == 0 else "part"
                    why = f"{n - n_ok} of {n} screws by a person (1 min each, estimate)"
            elif do == "seal":
                robot_s += ASM["seal_s"]
            elif do == "flip":
                robot_s += ASM["flip_s"]
            elif do == "dual":
                robot_s += ASM["dual_s"]
            elif do == "rotate":
                robot_s += ASM["rotate_s"]
            if "FAIL" in (r.get("arm"), r.get("sweep")) or "TOO MUCH FORCE" in (r.get("why") or ""):
                st = "fail"
                person_min += PERSON_MIN.get(sid, (FAIL_MIN, ""))[0]
                why = (r.get("why") or "")[:160]
        rows.append(dict(step=sid, chapter=chapter_of(sid), label=r["label"], do=do, actor=r.get("actor") or who,
                         status=st, robot_s=round(robot_s, 1), person_min=round(person_min, 1),
                         checker_compute_s=r.get("seconds"), note=why))
    chapters = {}
    for x in rows:
        c = chapters.setdefault(x["chapter"], dict(steps=0, robot_s=0.0, person_min=0.0, fail=0, person_steps=0))
        c["steps"] += 1
        c["robot_s"] = round(c["robot_s"] + x["robot_s"], 1)
        c["person_min"] = round(c["person_min"] + x["person_min"], 1)
        c["fail"] += x["status"] in ("fail", "part")
        c["person_steps"] += x["status"] in ("person", "shop")
    # MiR trips to the long table: the parts each chapter places, PARTS_PER_TRIP to a tote, each trip two legs, two
    # dockings and two registrations (timeline.py's 25 s, 30 s and 15 s: estimates)
    for ch, c in chapters.items():
        n = sum(1 for x in rows if x["chapter"] == ch and x["do"] in ("place", "seal", "dual"))
        c["fetch_trips"] = math.ceil(n / PARTS_PER_TRIP)
        c["fetch_s"] = c["fetch_trips"] * TRIP_S
    tot = dict(steps=len(rows), robot_h=round(sum(x["robot_s"] for x in rows) / 3600, 2),
               fetch_h=round(sum(c["fetch_s"] for c in chapters.values()) / 3600, 2),
               person_h=round(sum(x["person_min"] for x in rows) / 60, 2),
               fail_steps=sum(x["status"] in ("fail", "part") for x in rows),
               person_steps=sum(x["status"] in ("person", "shop") for x in rows))
    return dict(rows=rows, chapters=chapters, totals=tot, assumptions=dict(ASM, parts_per_trip=PARTS_PER_TRIP, trip_s=TRIP_S),
                method="ESTIMATES, not measurements: results.json's 'seconds' is the checker's compute time. Robot time = "
                       f"{ASM['place_s']:.0f} s per placement + the insertion path from sequence.json at "
                       f"{ASM['insert_mm_s']:.0f} mm/s, {ASM['screw_setup_s']:.0f} s + {ASM['screw_s']:.0f} s a screw, "
                       f"{ASM['seal_s']:.0f} s an O-ring or cord, {ASM['flip_s']:.0f} s a flip, {ASM['dual_s']:.0f} s a "
                       f"two-arm carry, {ASM['tool_change_s']:.0f} s a tool change; MiR trips to the long table are "
                       f"counted per chapter ({PARTS_PER_TRIP} parts a trip, {TRIP_S:.0f} s a round trip). Person minutes "
                       "per step are listed in build_hud.py (PERSON_MIN), 1 min per screw the arm couldn't drive and "
                       f"{FAIL_MIN:.0f} min per failed placement.")


# ------------------------------------------------------------------ main


def k(x):
    return f"${x / 1000:,.1f}k" if abs(x) >= 1000 else f"${x:,.0f}"


def main():
    lines = CS.read_bom()
    used, used_notes = read_used_rebased()
    cheap, cheap_dropped = read_cheaper_current()
    sc = {"new": CS.apply(lines), "used": CS.apply(lines, used), "cheaper": CS.apply(lines, cheap),
          "both": CS.apply(lines, used, cheap)}
    # the repo's own script as it stands (stale bases), for the consistency note
    cs_used, cs_cheap = CS.read_used(), CS.read_cheaper()
    cs = {"new": CS.apply(lines), "used": CS.apply(lines, cs_used), "cheaper": CS.apply(lines, cs_cheap),
          "both": CS.apply(lines, cs_used, cs_cheap)}
    spec_new, spec_ulo, spec_uhi = at_spec(lines, sc["new"], sc["used"], used)

    # split each line into categories, for every scenario
    def cat_parts(line, scen):
        lo, hi = sc[scen][line]
        if line not in SPLIT:
            return {CAT_OF[line]: [lo, hi]}
        out, base_lo, base_hi = {}, lines[line]["low"], lines[line]["high"]
        fixed_lo = fixed_hi = 0.0
        for cat, a, b, _ in SPLIT[line][:-1]:
            out[cat] = [a, b]
            fixed_lo += a
            fixed_hi += b
        last = SPLIT[line][-1][0]
        out[last] = [base_lo - fixed_lo, base_hi - fixed_hi]
        # scenario deltas: to DELTA_CAT's part if named, else to the last part
        d_lo, d_hi = lo - base_lo, hi - base_hi
        named = [key for key in list(used) + list(cheap) if key.startswith(line + ":") and key in DELTA_CAT]
        tgt = DELTA_CAT[named[0]] if named else last
        out[tgt] = [out[tgt][0] + d_lo, out[tgt][1] + d_hi]
        return out

    cats = {c: dict(cat=c, title=t, lines=[], new=[0.0, 0.0], used=[0.0, 0.0], cheaper=[0.0, 0.0], both=[0.0, 0.0],
                    spec_new=0.0, spec_used=[0.0, 0.0], on_table=c not in ("offtable", "services"))
            for c, t in CAT_TITLES}
    for line in lines:
        parts = {s: cat_parts(line, s) for s in sc}
        for cat in parts["new"]:
            C = cats[cat]
            C["lines"].append(line)
            for s in sc:
                C[s][0] += parts[s][cat][0]
                C[s][1] += parts[s][cat][1]
        # at spec: the line's share goes where its low end goes (the CW chain lines are not split)
        if line in SPLIT:
            shares = parts["new"]
            tot_lo = sum(v[0] for v in shares.values()) or 1.0
            for cat, v in shares.items():
                f = v[0] / tot_lo
                cats[cat]["spec_new"] += spec_new[line] * f
                cats[cat]["spec_used"][0] += spec_ulo[line] * f
                cats[cat]["spec_used"][1] += spec_uhi[line] * f
        else:
            C = cats[CAT_OF[line]]
            C["spec_new"] += spec_new[line]
            C["spec_used"][0] += spec_ulo[line]
            C["spec_used"][1] += spec_uhi[line]

    # lead times for every line, then per item and per category; the schedule they set
    leads = LTM.lead_rows(BOM_ROWS)
    sched = LTM.schedule(leads, BOM_ROWS)

    def lead_of(line):
        r = leads[line]
        return dict(new=dict(text=r["new_text"], days=r["days_new"], days_vendor=r["days_new_vendor"], po=r["po_new"],
                             source=r["new_source"], basis=r["new_basis"]),
                    used=dict(text=r["used_text"], days=r["days_used"], source=r["used_source"]) if r["used_text"] else None,
                    faster_new=dict(text=r["alt_text"], days=r["days_alt"], source=r["alt_source"]) if r["alt_text"] else None)

    # items: attach used listings, lead times, and order them by price within each category
    items = []
    for it in ITEMS:
        x = dict(it)
        # listings still up on 2026-11-25 first: an ended pick moves to used_alt, and the next live listing leads
        primary = [used_row(m) for m in it["used"]]
        alts = [used_row(m) for m in it["used_alt"]]
        lead_u = [u for u in primary if u["live"]]
        if primary and not lead_u:  # every pick ended: the next live alternative takes over
            lead_u = [u for u in alts if u["live"]][:1]
        x["used"] = lead_u
        x["used_alt"] = [u for u in primary + alts if u not in lead_u]
        x["used_best"] = x["used"][0]["total"] if x["used"] else None
        x["bom_line_new"] = [round(lines[it["line"]]["low"], 2), round(lines[it["line"]]["high"], 2)]
        x["lead"] = lead_of(it["line"])
        r = leads[it["line"]]
        if it["kind"] == "bundle":  # a bundle's used value is its line's used scenario, not one listing
            ub = sc["used"][it["line"]][0] if it["line"] not in SPLIT else None
            used_txt = k(ub) if ub is not None and ub < lines[it["line"]]["low"] - 1 else "buy new"
        else:
            used_txt = k(x["used_best"]) if x["used_best"] is not None else "buy new"
        new_txt = (k(it["new_drawn"]) if it["new_drawn"] else
                   "$0 (air-cooled laser)" if it["line"] == "L2" else "with the laser (price TBD)")
        # same-spec catalogue alternatives for the item's line (counted rows whose part is still in the line)
        x["cheaper_options"] = [o for o in CHEAPER_ROWS if o["line"] == it["line"] and o["saving"] > 0
                                and (it["line"] not in SPLIT or o["key"] not in DELTA_CAT or DELTA_CAT[o["key"]] == it["cat"])]
        lead_used = r["short_used"] if used_txt != "buy new" else "buy new"
        x["hud"] = dict(name=it["name"], new=new_txt, used=used_txt, lead_new=r["short_new"],
                        lead_new_days=r["days_new"], lead_used=lead_used, lead_used_days=r["days_used_route"],
                        callout=f"{it['name']}: new {new_txt}, {r['short_new']}"
                                + (f" | used {used_txt}, {r['short_used']}" if used_txt != "buy new" else " | buy new"))
        items.append(x)
    order_ix = {c: i for i, c in enumerate(ORDER)}
    items.sort(key=lambda x: (order_ix[x["cat"]], -x["new_drawn"], -x["new_high"]))
    for c in cats.values():
        c["items"] = [x["id"] for x in items if x["cat"] == c["cat"]]
        # a split line's lead time is its main part's (the last split entry), so it counts only in that category
        ls = [leads[ln] for ln in dict.fromkeys(c["lines"]) if ln not in SPLIT or SPLIT[ln][-1][0] == c["cat"]]

        def longest(key, swaps=False):
            best = None
            for r in ls:
                d = r["days_alt"] if (swaps and r["days_alt"] and r["line"] in ("S2", "H2")) else r[key]
                if d and (best is None or d[1] > best[0][1]):
                    best = (d, r)
            return best
        n_as, n_sw, u = longest("days_new"), longest("days_new", swaps=True), longest("days_used_route")
        c["lead"] = dict(
            new_as_chosen=dict(line=n_as[1]["line"], item=n_as[1]["item"], days=n_as[0], text=n_as[1]["new_text"],
                               short=n_as[1]["short_new"], source=n_as[1]["new_source"]) if n_as else None,
            new_longest=dict(line=n_sw[1]["line"], item=n_sw[1]["item"], days=n_sw[0], text=n_sw[1]["new_text"],
                             short=n_sw[1]["short_new"], source=n_sw[1]["new_source"]) if n_sw else None,
            used_longest=dict(line=u[1]["line"], item=u[1]["item"], days=u[0],
                              text=u[1]["used_text"] or u[1]["new_text"],
                              short=u[1]["short_used"] if u[1]["days_used"] else u[1]["short_new"],
                              source=u[1]["used_source"] or u[1]["new_source"]) if u else None,
            unknown=[r["line"] for r in ls if not r["days_new"]])

    # running totals in tour order
    run = dict(new=[0.0, 0.0], used=[0.0, 0.0], cheaper=[0.0, 0.0], both=[0.0, 0.0], spec_new=0.0, spec_used=[0.0, 0.0])
    cat_list = []
    for c in ORDER:
        C = cats[c]
        for s in ("new", "used", "cheaper", "both"):
            run[s] = [run[s][0] + C[s][0], run[s][1] + C[s][1]]
        run["spec_new"] += C["spec_new"]
        run["spec_used"] = [run["spec_used"][0] + C["spec_used"][0], run["spec_used"][1] + C["spec_used"][1]]
        C = {kk: (([round(v[0], 2), round(v[1], 2)] if isinstance(v, list) and v and isinstance(v[0], float) else
                   round(v, 2) if isinstance(v, float) else v)) for kk, v in C.items()}
        C["lines"] = list(dict.fromkeys(C["lines"]))
        C["run"] = {s: ([round(v[0], 2), round(v[1], 2)] if isinstance(v, list) else round(v, 2)) for s, v in run.items()}
        lu = C["lead"]
        C["hud"] = dict(
            title=C["title"].split(":")[0], new=k(C["spec_new"]), used=rng(C["spec_used"]),
            run_new=k(C["run"]["spec_new"]), run_used=rng(C["run"]["spec_used"]),
            range_new=rng(C["new"]), range_used=rng(C["used"]),
            lead_new=(f"{fmt_days(lu['new_longest']['days'])} ({lu['new_longest']['line']}: {lu['new_longest']['short']})"
                      if lu["new_longest"] else "TBD"),
            lead_used=(f"{fmt_days(lu['used_longest']['days'])} ({lu['used_longest']['line']}: {lu['used_longest']['short']})"
                       if lu["used_longest"] else ""),
            lead_new_as_chosen=(f"{fmt_days(lu['new_as_chosen']['days'])} ({lu['new_as_chosen']['line']}: "
                                f"{lu['new_as_chosen']['short']})" if lu["new_as_chosen"] else "TBD"),
            lead_unknown=" ".join(lu["unknown"]))
        if c == "services":
            C["hud"]["lead_new"] = C["hud"]["lead_used"] = (
                "SendCutSend 5-15 d; BYU shop queue 7.6 wk (outsourcing split) to 16.4 wk (all in house); honing loop 3-6 wk "
                "(estimate)")
        ukeys = sorted({key for key, v in used.items() if v["line"].split(",")[0] in C["lines"]})
        C["source"] = (f"bom.csv lines {' '.join(C['lines'])}"
                       + (" (split by component: " + ", ".join(f"{ln} {w}" for ln in C["lines"] if ln in SPLIT
                                                              for cat, _, _, w in SPLIT[ln] if cat == c) + ")"
                          if any(ln in SPLIT for ln in C["lines"]) else "")
                       + (f"; used: cost/used-options.csv picks {' '.join(ukeys)} (re-read 2026-11-25, ebay-recheck.csv)"
                          if ukeys else "; no used route")
                       + "; lead times: leadtimes.py from leadtime-lookups.csv (2026-11-25)")
        cat_list.append(C)

    tot = {s: [round(sum(v[0] for v in sc[s].values()), 2), round(sum(v[1] for v in sc[s].values()), 2)] for s in sc}
    tot_cs = {s: [round(sum(v[0] for v in cs[s].values()), 2), round(sum(v[1] for v in cs[s].values()), 2)] for s in cs}
    spec = dict(new=round(sum(spec_new.values()), 2), used=[round(sum(spec_ulo.values()), 2), round(sum(spec_uhi.values()), 2)],
                cw_chain_new=round(sum(spec_new[x] for x in CW_CHAIN), 2),
                cw_chain_used=[round(sum(spec_ulo[x] for x in CW_CHAIN), 2), round(sum(spec_uhi[x] for x in CW_CHAIN), 2)])
    hud = dict(
        generated_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        what="Cost, lead-time and time numbers for the robot-built desktop LPBF video (issue #260, PR #266, round 7)",
        how_to_show=("Tour the categories in the order of 'categories'. For each, show hud.new (at spec, all new) against "
                     "hud.used (the used picks where a sensible listing exists, new elsewhere) and the running totals "
                     "hud.run_new / hud.run_used; hud.range_new / hud.range_used are the BOM's full low-high ranges. Call "
                     "out the category's 'items' in order with their hud.new, hud.used, hud.lead_new and hud.lead_used. "
                     "'offtable' and 'services' are not on the table: show them as text rows at the end of the tour."),
        definitions=dict(
            new="bom.csv low-high: low = cheapest listed option on every line (some under spec: a PRC laser, a marking "
                "galvo, open-source OPAL), high = the premium option",
            used="'Used majors': the 13 used picks of cost/used-options.csv re-based on today's bom.csv (USED_REBASE) plus "
                 "a refurbished UPS for D2; for each component and end, the cheaper of new and used",
            cheaper="cost/cheaper-equivalents.csv's counted same-spec swaps whose replaced part is still in today's line",
            both="used + cheaper, the cheaper one per component",
            spec_new="cost_scenarios.py's at-spec rule: the CW optics chain (L1, L3, L5, L6, C1) at its BOM high end, the "
                     "cheapest listed option on every other line (L2 = 0: the quoted IPG is air-cooled)",
            spec_used="the same with the used CW chain (low pick to high pick) and the used scenario's low end elsewhere",
            days="calendar days from placing the order to the part at BYU: ship time + transit, + 10-14 days for a BYU "
                 "purchase order when one vendor's order is $3,500 or more"),
        categories=cat_list,
        items=items,
        totals=dict(scenarios=tot, at_spec=spec, cost_scenarios_py_as_is=tot_cs,
                    cost_scenarios_md_text=dict(baseline=[39440, 112978], used=[36655, 71884], cheaper=[34168, 105324],
                                                both=[31711, 65002], written="2026-11-20 (bom.csv has grown since)")),
        consistency=dict(used_rebase=used_notes, cheaper_dropped=cheap_dropped,
                         note="cost-scenarios.md's totals ($39,440-112,978 baseline) predate the 2026-11-22..25 BOM rounds; "
                              "running cost/cost_scenarios.py on today's bom.csv gives 'cost_scenarios_py_as_is', whose "
                              "used and cheaper rows carry 2026-11-20 base values; this file re-bases them"),
        placed_on_table={kk: v for kk, v in sorted(PLACED.items())},
        lead_times=dict(lines=leads, schedule=sched, risks=LTM.LEAD_RISKS,
                        lookups="desktop-lpbf/analysis/robotbuild_data/leadtime-lookups.csv",
                        n_lookup_rows=len(load_lookups())),
    )
    hud["times"] = dict(machining=machining_times(), robot_shop=shop_timeline(), assembly=assembly_times())
    # the two things the compositor needs first: the tour (display strings only) and the headline numbers
    by_id = {x["id"]: x for x in items}
    hud["tour"] = [dict(cat=C["cat"], on_table=C["on_table"], **C["hud"],
                        items=[dict(id=i, **by_id[i]["hud"]) for i in C["items"]]) for C in cat_list]
    R = sched["routes"]
    mt, asm = hud["times"]["machining"]["totals"], hud["times"]["assembly"]["totals"]
    hud["headline"] = dict(
        cost_at_spec=dict(new=spec["new"], used=spec["used"], saving=[round(spec["new"] - spec["used"][1], 2),
                                                                      round(spec["new"] - spec["used"][0], 2)]),
        cost_bom_range=dict(new=tot["new"], used=tot["used"], cheaper=tot["cheaper"], both=tot["both"]),
        cw_chain=dict(new=spec["cw_chain_new"], used=spec["cw_chain_used"]),
        weeks=dict(
            new_as_chosen=dict(parts=R["new"]["parts_in_hand_wk"], set_by=R["new"]["set_by"], ready=R["new"]["ready_split_wk"]),
            new=dict(parts=R["new_with_swaps"]["parts_in_hand_wk"], set_by=R["new_with_swaps"]["set_by"],
                     ready_split=R["new_with_swaps"]["ready_split_wk"],
                     ready_all_in_house=R["new_with_swaps"]["ready_all_in_house_wk"]),
            used=dict(parts=R["used"]["parts_in_hand_wk"], set_by=R["used"]["set_by"], ready_split=R["used"]["ready_split_wk"],
                      ready_all_in_house=R["used"]["ready_all_in_house_wk"]),
            saved_by_used_split=[round(R["new_with_swaps"]["ready_split_wk"][0] - R["used"]["ready_split_wk"][0], 1),
                                 round(R["new_with_swaps"]["ready_split_wk"][1] - R["used"]["ready_split_wk"][1], 1)],
            note="new = as chosen but with S2's HS6B and H2's K8DT swapped for stocked parts; 'split' = outsourcing.md's "
                 "recommended make/buy split (152 shop hours at BYU), 'all in house' = 329 h at BYU"),
        machining_h=dict(with_4th_axis=mt["total_h_4th"], three_axis=mt["total_h_3axis"], cam=mt["cam_h"],
                         setups_4th=mt["setup_h_4th"], setups_3axis=mt["setup_h_3axis"], cutting=mt["run_h"],
                         deburr_inspect=mt["deburr_inspect_h"], parts=mt["parts"]),
        assembly=dict(steps=asm["steps"], robot_h=asm["robot_h"], mir_fetch_h=asm["fetch_h"], person_h=asm["person_h"],
                      failed_or_partial=asm["fail_steps"], person_or_shop_steps=asm["person_steps"],
                      basis="estimates (results.json's seconds are compute time)"),
        po_rule="BYU: purchases of $3,500 or more from one vendor need a purchase order: 'Allow ten days to two weeks "
                "PLUS shipping time' (capstone.byu.edu/purchase-orders, read 2026-11-25); under $3,500 a PCard")

    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    js = json.dumps(hud, indent=1, default=str)
    (OUT / "hud.json").write_text(js)
    (TMP / "hud.json").write_text(js)
    write_costs_csv(cat_list, items, leads, lines, sc)
    write_times_csv(hud["times"], sched)
    print(f"categories: {len(cat_list)}, items: {len(items)}")
    for C in cat_list:
        print(f"  {C['cat']:9s} new {C['new'][0]:>9,.0f}-{C['new'][1]:>9,.0f}  used {C['used'][0]:>9,.0f}-{C['used'][1]:>9,.0f}"
              f"  spec {C['spec_new']:>9,.0f} / {C['spec_used'][0]:>8,.0f}-{C['spec_used'][1]:>8,.0f}  run spec "
              f"{C['run']['spec_new']:>9,.0f} / {C['run']['spec_used'][0]:>8,.0f}-{C['run']['spec_used'][1]:>8,.0f}"
              f"  lead {C['hud']['lead_new']} / {C['hud']['lead_used']}")
    print("totals", tot)
    print("cost_scenarios.py as is", tot_cs)
    print("at spec", spec)
    for name, r in sched["routes"].items():
        print(f"  {name:15s} parts {r['parts_in_hand_wk']} wk set by {r['set_by']}; fab split {r['fabrication_split_wk']}, "
              f"all {r['fabrication_all_in_house_wk']}; ready split {r['ready_split_wk']}, all {r['ready_all_in_house_wk']}; "
              f"next {[(n['line'], n['wk']) for n in r['next'][:4]]}; unknown {r['unknown']}")
    a = hud["times"]["assembly"]
    print("assembly", a["totals"], {c: (v["robot_s"], v["person_min"]) for c, v in a["chapters"].items()})


def rng(v):
    return k(v[0]) if abs(v[0] - v[1]) < 1 else f"{k(v[0])}-{k(v[1])}"


def fmt_days(d, basis=""):
    if not d:
        return "quote only" if basis == "quote" else "TBD"
    lo, hi = d
    if hi >= 21:
        return f"{lo / 7:.0f}-{hi / 7:.0f} wk" if round(lo / 7) != round(hi / 7) else f"{hi / 7:.0f} wk"
    return f"{lo}-{hi} d" if lo != hi else f"{lo} d"


def write_costs_csv(cat_list, items, leads, lines, sc):
    cols = ["row", "id", "category", "name", "bom_lines", "new_low_usd", "new_high_usd", "new_as_drawn_usd", "used_low_usd",
            "used_high_usd", "cheaper_low_usd", "cheaper_high_usd", "both_low_usd", "both_high_usd", "spec_new_usd",
            "spec_used_low_usd", "spec_used_high_usd", "run_spec_new_usd", "run_spec_used_low_usd", "run_spec_used_high_usd",
            "run_new_low_usd", "run_new_high_usd", "run_used_low_usd", "run_used_high_usd", "price_source",
            "used_listing", "used_condition", "used_returns", "used_seller_type", "used_location", "used_url",
            "used_fetched_utc", "used_status_2026_11_25", "used_price_2026_11_25", "used_delivery_to_provo", "lead_new", "lead_new_days_low", "lead_new_days_high", "lead_new_po", "lead_new_source",
            "lead_used", "lead_used_days_low", "lead_used_days_high", "lead_used_source", "faster_new_option", "risk"]
    rows = []
    for C in cat_list:
        ln, lu = C["lead"]["new_longest"], C["lead"]["used_longest"]
        rows.append(dict(row="category", id=C["cat"], category=C["cat"], name=C["title"], bom_lines=" ".join(C["lines"]),
                         new_low_usd=C["new"][0], new_high_usd=C["new"][1], used_low_usd=C["used"][0],
                         used_high_usd=C["used"][1], cheaper_low_usd=C["cheaper"][0], cheaper_high_usd=C["cheaper"][1],
                         both_low_usd=C["both"][0], both_high_usd=C["both"][1], spec_new_usd=C["spec_new"],
                         spec_used_low_usd=C["spec_used"][0], spec_used_high_usd=C["spec_used"][1],
                         run_spec_new_usd=C["run"]["spec_new"], run_spec_used_low_usd=C["run"]["spec_used"][0],
                         run_spec_used_high_usd=C["run"]["spec_used"][1], run_new_low_usd=C["run"]["new"][0],
                         run_new_high_usd=C["run"]["new"][1], run_used_low_usd=C["run"]["used"][0],
                         run_used_high_usd=C["run"]["used"][1],
                         price_source="bom.csv; cost/used-options.csv and cost/cheaper-equivalents.csv via build_hud.py",
                         lead_new=(f"longest: {ln['line']} {ln['item']}: {ln['text']}" if ln else "TBD"),
                         lead_new_days_low=ln["days"][0] if ln else "", lead_new_days_high=ln["days"][1] if ln else "",
                         lead_new_source=ln["source"] if ln else "",
                         lead_used=(f"longest: {lu['line']} {lu['item']}: {lu['text']}" if lu else ""),
                         lead_used_days_low=lu["days"][0] if lu else "", lead_used_days_high=lu["days"][1] if lu else "",
                         lead_used_source=lu["source"] if lu else "",
                         risk=("no stated lead time: " + " ".join(C["lead"]["unknown"])) if C["lead"]["unknown"] else ""))
    for x in items:
        u = x["used"][0] if x["used"] else {}
        L = x["lead"]
        rows.append(dict(row="item", id=x["id"], category=x["cat"], name=x["name"], bom_lines=x["line"],
                         new_low_usd=x["new_low"], new_high_usd=x["new_high"], new_as_drawn_usd=x["new_drawn"],
                         used_low_usd=x["used_best"] if x["used_best"] is not None else "",
                         used_high_usd=max([v["total"] for v in x["used"]], default=""),
                         price_source=x["new_src"], used_listing=u.get("title", ""), used_condition=u.get("condition", ""),
                         used_returns=u.get("returns", ""), used_seller_type=u.get("seller_type", ""),
                         used_location=u.get("location", ""), used_url=u.get("url", ""),
                         used_fetched_utc=u.get("fetched_utc", ""), used_status_2026_11_25=(u.get("recheck") or {}).get("status", "not re-read" if u else ""), used_price_2026_11_25=(u.get("recheck") or {}).get("price_now") or "", used_delivery_to_provo=(u.get("recheck") or {}).get("delivery_to_provo", ""),
                         lead_new=L["new"]["text"], lead_new_days_low=(L["new"]["days"] or ["", ""])[0],
                         lead_new_days_high=(L["new"]["days"] or ["", ""])[1], lead_new_po=L["new"]["po"],
                         lead_new_source=L["new"]["source"],
                         lead_used=L["used"]["text"] if L["used"] else "",
                         lead_used_days_low=(L["used"]["days"] or ["", ""])[0] if L["used"] else "",
                         lead_used_days_high=(L["used"]["days"] or ["", ""])[1] if L["used"] else "",
                         lead_used_source=L["used"]["source"] if L["used"] else "",
                         faster_new_option=(L["faster_new"]["text"] if L["faster_new"] else ""),
                         cheaper_low_usd="", risk=x.get("risk", "") + (" Cheaper new: " + x["cheaper"] if x.get("cheaper") else "")))
    for line, r in leads.items():
        rows.append(dict(row="line", id=line, category=CAT_OF.get(line, ""), name=r["item"], bom_lines=line,
                         new_low_usd=round(lines[line]["low"], 2), new_high_usd=round(lines[line]["high"], 2),
                         used_low_usd=round(sc["used"][line][0], 2), used_high_usd=round(sc["used"][line][1], 2),
                         cheaper_low_usd=round(sc["cheaper"][line][0], 2), cheaper_high_usd=round(sc["cheaper"][line][1], 2),
                         both_low_usd=round(sc["both"][line][0], 2), both_high_usd=round(sc["both"][line][1], 2),
                         price_source="bom.csv " + line, lead_new=r["new_text"],
                         lead_new_days_low=(r["days_new"] or ["", ""])[0], lead_new_days_high=(r["days_new"] or ["", ""])[1],
                         lead_new_po=r["po_new"], lead_new_source=r["new_source"], lead_used=r["used_text"],
                         lead_used_days_low=(r["days_used"] or ["", ""])[0], lead_used_days_high=(r["days_used"] or ["", ""])[1],
                         lead_used_source=r["used_source"], faster_new_option=r["alt_text"]))
    with open(OUT / "costs-leadtimes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: (round(r[c], 2) if isinstance(r.get(c), float) else r.get(c, "")) for c in cols})


def write_times_csv(times, sched):
    cols = ["section", "id", "name", "chapter", "material", "cam_h", "setup_h_3axis", "setup_h_4th", "run_h",
            "deburr_inspect_h", "total_h_3axis", "total_h_4th", "robot_s", "person_min", "status", "basis", "note"]
    rows = []
    m = times["machining"]
    src = "analysis/out/machining/hours.json"
    for p in m["parts"]:
        rows.append(dict(section="machining", id="", name=p["part"], material=p["mat"], cam_h=p["cam_h"],
                         setup_h_3axis=p["setup_h_3axis"], setup_h_4th=p["setup_h_4th"], run_h=p["run_h"],
                         deburr_inspect_h=p["deburr_inspect_h"], total_h_3axis=p["total_h_3axis"],
                         total_h_4th=p["total_h_4th"], basis=src + " (estimates: CAM rule, setups, removal rates)",
                         note=p.get("special", "")))
    t = m["totals"]
    rows.append(dict(section="machining total", id="", name=f"{t['parts']} parts, {t['setups_3axis']} setups (3-axis) / "
                     f"{t['setups_4th']} (4th axis)", cam_h=t["cam_h"], setup_h_3axis=t["setup_h_3axis"],
                     setup_h_4th=t["setup_h_4th"], run_h=t["run_h"], deburr_inspect_h=t["deburr_inspect_h"],
                     total_h_3axis=t["total_h_3axis"], total_h_4th=t["total_h_4th"], basis=src))
    s = times["robot_shop"]
    for r in s["rows"]:
        rows.append(dict(section="robot shop", name=r["step"], person_min=round(r["shop_person_h"] * 60, 1),
                         robot_s=round(r["shop_machine_or_robot_h"] * 3600, 0),
                         basis=f"analysis/out/shop/timeline.json (by hand: {r['hand_person_h']} person-h)", note=r["note"]))
    for r in times["assembly"]["rows"]:
        rows.append(dict(section="assembly", id=r["step"], name=r["label"], chapter=r["chapter"], robot_s=r["robot_s"],
                         person_min=r["person_min"], status=r["status"],
                         basis="estimate (build_hud.py ASM and PERSON_MIN); checked step from analysis/out/assembly/results.json",
                         note=r["note"]))
    for c, v in times["assembly"]["chapters"].items():
        rows.append(dict(section="assembly chapter", id=c, name=f"{v['steps']} steps, {v['fail']} failed or partial, "
                         f"{v['person_steps']} person or shop steps", chapter=c, robot_s=v["robot_s"],
                         person_min=v["person_min"], basis="sum of the assembly rows (estimates)"))
        rows.append(dict(section="assembly fetch", id=c, name=f"{v['fetch_trips']} MiR trips to the long table",
                         chapter=c, robot_s=v["fetch_s"], basis="estimate (PARTS_PER_TRIP, TRIP_S in build_hud.py)"))
    for name, r in sched["routes"].items():
        rows.append(dict(section="schedule", id=name, name=f"bought parts in hand {r['parts_in_hand_wk'][0]}-"
                         f"{r['parts_in_hand_wk'][1]} wk (set by {r['set_by']}: {r['set_by_item']}); ready "
                         f"{r['ready_split_wk'][0]}-{r['ready_split_wk'][1]} wk on the outsourcing split, "
                         f"{r['ready_all_in_house_wk'][0]}-{r['ready_all_in_house_wk'][1]} wk all in house",
                         basis="leadtimes.py (vendor statements in leadtime-lookups.csv; transit, PO and fabrication as "
                               "stated there)", note=f"critical: {r['critical_split']} (split) / {r['critical_all_in_house']} "
                                                     f"(all in house); no stated lead: {' '.join(r['unknown'])}"))
    with open(OUT / "times.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


if __name__ == "__main__":
    main()
