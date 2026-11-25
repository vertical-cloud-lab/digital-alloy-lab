"""Manufacturing routes for the desktop LPBF's machined parts (issue #260, PR #266, round 7): where the 287.3 shop hours go,
labour cost and calendar days (daytime only) for four routes, the chamber alternatives, and catalogue swaps.

Sterling asked on 2026-11-25 whether 287.3 h is the chamber, what it costs and how long it takes in house against outsourced,
how others build chambers like this, whether to print the chamber, and whether standard parts would help. The answer and
tables are in robot-build/manufacturing-route.md; this script makes every number in them.

Inputs (all in the repo):
  analysis/out/machining/hours.csv          per-part CAM, setup, run, deburr + inspect hours (hours.py, round 6, 57 parts)
  analysis/out/machining/setup_plan.json    machine per part (VMC, or lathe + VMC)
  analysis/out/outsourcing/should_cost.csv  stock $ and the US outside prices of 2026-11-22 (SendCutSend etc. and estimates)
  robot-build/route-quotes.csv              the live quotes of 2026-11-25 (JLC3DP, JLCCNC; quotes_csv.py)
Outputs:
  robot-build/route-hours-by-part.csv       every part: group, machine, hours by activity, one-off / per-batch / per-machine
  robot-build/route-hours-by-group.csv      groups x activities
  robot-build/route-routes.csv              the routes: labour h and $, outside $, working and calendar days to a leak test
  robot-build/route-schedule.csv            every schedule bar (route, task, start, end low, end high, in working days)
  robot-build/route-chamber-options.csv     the chamber alternatives' decision table
  robot-build/route-standard-parts.csv      catalogue swaps, hours saved and what each costs the design
  robot-build/img/route-hours.png           hours by group and activity
  robot-build/img/route-gantt.png           schedules, PO to the first leak test
  /tmp/robotbuild/data/route.json           summary for the video's chapter 60 (and robot-build/route-summary.json, a copy)

Calendar model (stated assumptions, not measurements):
  - daytime only: 8 h a working day, 5 working days a week; calendar days = working days x 7/5. Holidays are not modelled:
    BYU's Thanksgiving and winter breaks would add about 2 and 6 working days to a schedule that spans them.
  - BYU purchase orders: an order of $3,500 or more from one vendor needs a PO, "ten days to two weeks plus shipping"
    (capstone.byu.edu, via the data worker's hud.json); stock is taken at hud.json's 12-20 calendar days (PO + McMaster).
  - CAM needs only the model, so it starts on day 0; setups wait for stock.
  - The module's honing loop: turn the body (1 wd), wait for the welder (2-5 wd), weld and bore (1 wd), ship (2 wd), hone
    3-6 weeks (15-30 wd: no honing shop publishes a lead time; outsourcing.md's estimate), ship back (2 wd).
  - Purchased parts needed for the leak test (pump, valves, gauges, seals, inserts) arrive in 12-22 calendar days
    (hud.json lines G2, G7, G8, B2, FX), never later than the custom parts here. The laser is not needed for a leak test.
  - Assembly to the first rate-of-rise test: 3-5 working days for two people (estimate).
Labour is costed at BYU's Prototype Manufacturing Lab academic rate, $65/h (pml.byu.edu/labor, seen only as a search
snippet; that path now redirects to Physical Facilities' Transportation & Manufacturing Services page, which publishes no
rate: fetched through the lab Pi 2026-11-25 05:33 UTC). $85/h (non-academic) and $95/h (off campus) are the sensitivities;
student labour in the ME prototyping lab is free but still takes the same hours.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/route/route_calcs.py
"""
from __future__ import annotations

import csv
import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]          # desktop-lpbf/
OUTM = ROOT / "analysis" / "out" / "machining"
RB = ROOT / "robot-build"
IMG = RB / "img"
TMPJSON = pathlib.Path("/tmp/robotbuild/data/route.json")

RATE, RATE_NONACAD, RATE_OFF = 65.0, 85.0, 95.0
HD, WK = 8.0, 5.0                                            # hours per working day, working days per week
CAL = 7.0 / 5.0
TOOLING_BUY = 3718.70                                        # machining.md round 6: tools to buy for this job
STOCK_WD = (9, 14)                                           # hud.json: stock 12-20 calendar days incl. BYU PO
PO_WD = (7, 10)                                              # 10-14 calendar days
BUY_WD = (9, 16)                                             # purchased leak-test parts, 12-22 calendar days
ASSY_WD = (3, 5)
HONE_LOOP_WD = (1 + 2 + 1 + 2 + 15 + 2, 1 + 5 + 1 + 2 + 30 + 2)   # 23-41 wd after stock arrives
HONE_USD = 400.0                                             # should_cost.py's estimate per bore (unquoted)
MODULE_SPECIALIST = (600.0, 1200.0, 1800.0)                  # Edison r5 planning range for a specialist-finished module body
FRAME_US = (4000.0, 7000.0, 10000.0)                         # Edison r5 turnkey frame range (US job shop)
FRAME_CN = (400.0, 800.0, 1500.0)                            # ESTIMATE: JLCCNC gives the frame a manual quote only
SS_UPLIFT = 123.46 / 32.98                                   # JLCCNC 304 vs 6061 for the overflow block (2026-11-22)
JLCCNC_SHIP = 746.51                                         # all 64 pieces, UPS DDP, 2026-11-25
WELD_H = 4.0                                                 # module weldment 3 h (outsourcing.md) + rod into rod end 1 h

GROUPS = [
    ("Chamber shell: frame, floor plate, lid, door", ("process_chamber_body", "chamber_floor_plate", "chamber_lid", "chamber_door")),
    ("Chamber fittings: drawer, windows, ports, feedthroughs, door hardware",
     ("cover_slide_drawer", "window_flange", "window_retaining", "camera_viewport", "camera_window_retaining", "recoater_feedthrough",
      "recoater_floating_bearing", "overflow_funnel", "draw_latch", "door_handle", "door_drive")),
    ("Build module M50 and its clamps", ("build_module_m50", "module_m50", "piston_head", "build_plate", "heater_block", "rod_end",
                                         "hollow_piston_rod", "macor", "striker", "zero_point", "field_stop")),
    ("Recoater", ("recoater_motor", "recoater_carriage", "recoater_arm", "blade_holder", "blade_cartridge", "recoater_sensor")),
    ("Powder dosing and overflow", ("metering_base", "reservoir_m", "overflow_jar")),
    ("Optics bridge and beam path", ("optics_bridge", "galvo_riser", "f_theta", "enclosed_beam")),
    ("Z stage and legs", ("z_mounting", "z_bracket", "z_lift", "z_sensor", "chamber_legs")),
    ("Base plates, stands, guard and robot aids", ("base_plate", "pb1_stand", "apriltag", "guard_door_handle")),
]
SHORT = {"Chamber shell: frame, floor plate, lid, door": "Chamber shell",
         "Chamber fittings: drawer, windows, ports, feedthroughs, door hardware": "Chamber fittings",
         "Build module M50 and its clamps": "Build module", "Recoater": "Recoater",
         "Powder dosing and overflow": "Powder dosing", "Optics bridge and beam path": "Optics",
         "Z stage and legs": "Z stage, legs", "Base plates, stands, guard and robot aids": "Base, guard, aids"}
SEAL = ("process_chamber", "chamber_floor", "chamber_lid", "chamber_door", "window_flange", "cover_slide_drawer", "build_module",
        "module_m50_bottom", "camera_viewport", "metering_base", "overflow_funnel", "recoater_feedthrough", "recoater_floating")
STAINLESS = ("build_module_m50", "module_m50_bottom_flange", "rod_end", "overflow_funnel", "hollow_piston_rod", "striker")
# the hybrid: what stays at BYU (seal faces, and the module parts that will change in thermal testing), what becomes a
# catalogue part (machining.md lever 1, outsourcing.md "buy instead"), and the rest goes out
MAKE = ("process_chamber_body", "chamber_floor_plate", "chamber_lid", "chamber_door", "cover_slide_drawer", "build_module_m50",
        "module_m50_bottom_flange", "piston_head", "build_plate", "heater_block", "rod_end", "hollow_piston_rod")
BUY = {  # slug prefix: (catalogue replacement, h to adapt it here, $ estimate, what it costs the design)
    "window_flange": ("stock fused-silica viewport on a standard flange (Ø ~100 mm class); AR coat for 1070 nm to order", 1.0, 515.0,
                      "the lid's window seat becomes a standard port; the cover-slide drawer must still cover it: medium redesign"),
    "window_retaining": ("comes with the viewport", 0.0, 0.0, "none beyond the viewport"),
    "f_theta_adapter": ("Thorlabs SM-thread adapter if the lens's M85x1 has one; else keep custom", 1.0, 125.0,
                        "none if an adapter exists (not checked)"),
    "field_stop": ("Thorlabs SM2 iris or fixed aperture in a lens tube", 1.0, 105.0, "aperture swapped per module becomes a tube insert"),
    "enclosed_beam": ("Thorlabs SM1 lens tubes and couplers", 1.0, 100.0, "none"),
    "camera_window_retaining": ("Thorlabs SM1 retaining ring", 0.0, 0.0, "the boss needs an SM1 thread"),
    "recoater_motor_standoff": ("stock NEMA 23 standoff bracket", 0.0, 0.0, "none"),
    "recoater_motor_bracket": ("stock NEMA 23 bracket", 1.0, 95.0, "motor position follows the stock bracket's hole pattern"),
    "door_handle": ("catalogue pull handle", 1.0, 74.0, "check the robot's grip on a catalogue pull"),
    "guard_door_handle": ("catalogue pull handle on standoffs", 1.0, 74.0, "check the robot's grip"),
    "macor": ("stock ceramic (alumina or Macor) washers", 0.5, 72.0, "stand-off height set by stock thickness"),
    "striker": ("stock 430 / 416 stainless disc or washer", 0.5, 75.0, "none"),
}


def group_of(slug):
    for g, prefs in GROUPS:
        if slug.startswith(prefs):
            return g
    raise KeyError(slug)


def wd2cal(x):
    return x * CAL


def read_parts():
    plan = json.loads((OUTM / "setup_plan.json").read_text())["parts"]
    should = list(csv.DictReader((ROOT / "analysis" / "out" / "outsourcing" / "should_cost.csv").open()))
    quotes = [r for r in csv.DictReader((RB / "route-quotes.csv").open()) if r["service"].startswith("JLCCNC (bulk")]
    rows = []
    for r in csv.DictReader((OUTM / "hours.csv").open()):
        slug = r["slug"]
        key = slug[:38]
        sc = [s for s in should if s["file"][:38] == key or s["file"].startswith(key[:30])]
        q = [x for x in quotes if x["file"].startswith(key)]
        cn = None
        if q and all(x["usd_each"] for x in q):
            cn = sum(float(x["usd_each"]) * int(x["qty"]) for x in q)
            if slug.startswith(STAINLESS):
                cn *= SS_UPLIFT
        h = dict(cam=float(r["cam_h"]), setup=float(r["setup_h_4th"]), run=float(r["run_h"]), deburr=float(r["deburr_inspect_h"]))
        tot = float(r["total_h_4th"])
        in_h = sum(float(s["in_house_h"]) for s in sc) if sc else None
        us = sum(float(s["outsourced_usd"] or 0) for s in sc) if sc else None
        if us is None:   # parts added after 2026-11-22: outsourcing.md's fit to SendCutSend CNC, $ = -141 + 88.5 x hours
            us = max(30.0, -140.8 + 88.5 * tot)
        stock = sum(float(s["stock_usd"] or 0) for s in sc) if sc else 15.0
        rows.append(dict(part=r["part"], slug=slug, group=group_of(slug), machine=plan.get(slug, {}).get("machine", ""),
                         mat=r["mat"], setups=int(r["setups_4th_axis"]), **h, total=tot, total_3axis=float(r["total_h_3axis"]),
                         seal=slug.startswith(SEAL), us_usd=round(us, 2), cn_usd=round(cn, 2) if cn is not None else None,
                         stock_usd=round(stock, 2), should_cost_h=in_h,
                         one_off=h["cam"], per_batch=h["setup"], per_machine=round(h["run"] + h["deburr"], 2)))
    return rows


def hours_tables(rows):
    acts = ("cam", "setup", "run", "deburr")
    tot = {a: round(sum(r[a] for r in rows), 1) for a in acts}
    tot["total"] = round(sum(r["total"] for r in rows), 1)
    groups = []
    for g, _ in GROUPS:
        rs = [r for r in rows if r["group"] == g]
        d = dict(group=g, parts=len(rs), **{a: round(sum(r[a] for r in rs), 1) for a in acts})
        d["total"] = round(sum(r["total"] for r in rs), 1)
        d["share_pct"] = round(100 * d["total"] / tot["total"], 1)
        groups.append(d)
    top = sorted(rows, key=lambda r: -r["total"])[:10]
    shell = [r for r in rows if r["group"] == GROUPS[0][0]]
    body = [r for r in rows if r["slug"].startswith(("process_chamber_body", "chamber_floor_plate"))]
    module_body = [r for r in rows if r["slug"].startswith("build_module_m50")]
    small = [r for r in rows if r["total"] <= 4.0]
    fixed = sum(min(r["total"], r["cam"] + r["setup"] + r["deburr"]) for r in rows)
    split = dict(one_off_cam=tot["cam"], per_batch_setups=tot["setup"], per_machine_run_deburr=round(tot["run"] + tot["deburr"], 1))
    split.update({k + "_pct": round(100 * v / tot["total"], 1) for k, v in list(split.items())})
    second_machine_later = round(tot["setup"] + tot["run"] + tot["deburr"], 1)
    # sensitivity: robot-shop.md's "by hand" allowances (35 h of CAM for 48 parts, 20 min a setup), same cutting and deburr
    n_setups = sum(r["setups"] for r in rows)
    low = dict(cam=round(35.0 * len(rows) / 48, 1), setup=round(n_setups * 20 / 60, 1), run=tot["run"], deburr=tot["deburr"],
               setups=n_setups)
    low["total"] = round(low["cam"] + low["setup"] + low["run"] + low["deburr"], 1)
    two_together = round(tot["total"] + tot["run"] + tot["deburr"], 1)
    return dict(totals=tot, groups=groups, top10=[dict(part=r["part"], group=SHORT[r["group"]], total=r["total"], cam=r["cam"],
                                                       setup=r["setup"], run=r["run"], deburr=r["deburr"]) for r in top],
                chamber=dict(frame_floor_h=round(sum(r["total"] for r in body), 1),
                             frame_floor_pct=round(100 * sum(r["total"] for r in body) / tot["total"], 1),
                             shell_h=round(sum(r["total"] for r in shell), 1),
                             shell_pct=round(100 * sum(r["total"] for r in shell) / tot["total"], 1),
                             module_body_h=round(sum(r["total"] for r in module_body), 1),
                             shell_plus_module_body_h=round(sum(r["total"] for r in shell + module_body), 1),
                             shell_plus_module_body_pct=round(100 * sum(r["total"] for r in shell + module_body) / tot["total"], 1),
                             cutting_h_frame_floor=round(sum(r["run"] for r in body), 2)),
                small_parts=dict(n=len(small), h=round(sum(r["total"] for r in small), 1),
                                 cutting_h=round(sum(r["run"] for r in small), 2)),
                fixed_overhead_h=round(fixed, 1), split=split,
                second_machine_later_h=second_machine_later, two_machines_together_h=two_together, low_allowances=low)


def reconcile():
    """The repo's other counts of the same work, and why they differ (numbers copied from the notes, with their dates)."""
    return [
        dict(source="hours.csv (machining.md round 6, phase 2; 2026-11-25)", parts=57, hours="287.3 (4th axis) / 302.3 (3-axis)",
             cam=132.1, setups="98.6 / 113.6", cutting=33.2, other="deburr + inspect 23.2",
             why="this note's basis"),
        dict(source="machining.md 48-part table (2026-11-20)", parts=48, hours="250 / 264", cam=116, setups="85 / 99", cutting=28,
             other="deburr + inspect 21",
             why="nine fewer parts: zero-point posts, plates and arms, the overflow jar's grip fin, draw-latch brackets, sensor brackets "
                 "and clamps, PB1 rails, the reservoir pull tab (added in rounds 4-6)"),
        dict(source="outsourcing.md 'make everything' (2026-11-22, model 9f45d80)", parts=82, hours="329", cam="", setups="", cutting="",
             other="268.2 h machined (50 rows, quantities multiplied) + 41.5 h sheet parts (18) + 19.0 h robot tooling (14)",
             why="counts sheet-metal parts and the robot's assembly tooling as well; its machined share (268 h) is the round-5 model"),
        dict(source="robot-shop.md 'by hand' (2026-11-20)", parts=48, hours="137 person-h", cam=35, setups="41 (118 x 20 min)",
             cutting=27.7, other="deburr 11.2, wash 5.6, measure 11.2, kitting 2.2, unboxing 1.8, stock prep 1.7",
             why="much smaller allowances: 0.7 h of CAM per part (hours.py 2.3 h) and 20 min per setup (hours.py 45-75 min, MMS "
                 "survey median 68-90 min)"),
        dict(source="Edison r7 robot-build review (2026-11-25), section 5", parts="one machine", hours="100-180 person-h machining; "
             "360-740 person-h the whole manual build", cam="", setups="", cutting="", other="Edison's estimates",
             why="an outside estimate of the same build"),
        dict(source="Edison r7 chamber-route review (2026-11-25), section 5", parts=57, hours="120-180 achievable", cam="25-85",
             setups="", cutting="", other="Edison's estimate with CAM templates (35-80 % less programming), fixture plates and selective "
                                       "outsourcing", why="what the same parts could take with templates and outsourcing"),
    ]


# ------------------------------------------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------------------------------------------
def routes(rows, H):
    T = H["totals"]
    stock_all = sum(r["stock_usd"] for r in rows)
    make = [r for r in rows if r["slug"].startswith(MAKE)]
    buy = [r for r in rows if r["slug"].startswith(tuple(BUY))]
    out = [r for r in rows if r not in make and r not in buy]
    out_all = rows
    n_seal_out = sum(1 for r in out if r["seal"])
    drawings_all = sum(2.0 if r["seal"] else 0.5 for r in rows)            # ESTIMATE: a drawing per outsourced part
    receive_all = sum(1.0 if r["seal"] else 0.25 for r in rows)            # ESTIMATE: receiving inspection, inserts, rework
    drawings_out = sum(2.0 if r["seal"] else 0.5 for r in out)
    receive_out = sum(1.0 if r["seal"] else 0.25 for r in out)
    buy_adapt = sum(next(v[1] for k, v in BUY.items() if r["slug"].startswith(k)) for r in buy)
    buy_usd = sum(next(v[2] for k, v in BUY.items() if r["slug"].startswith(k)) for r in buy)

    def cn_price(rs, frame=FRAME_CN[1]):
        s = 0.0
        for r in rs:
            if r["slug"].startswith("process_chamber_body"):
                s += frame
            elif r["slug"].startswith("build_module_m50"):
                s += MODULE_SPECIALIST[1]
            elif r["slug"].startswith("base_plate_process"):   # manual quote; the gas plate's $194.03 scaled by area
                s += 194.03 * (730 * 480) / (590 * 550)
            elif r["cn_usd"] is None:
                raise ValueError("no JLCCNC price for " + r["slug"])
            else:
                s += r["cn_usd"]
        return s

    def us_price(rs):
        s = 0.0
        for r in rs:
            if r["slug"].startswith("process_chamber_body"):
                s += FRAME_US[1]
            elif r["slug"].startswith("build_module_m50"):
                s += MODULE_SPECIALIST[1]
            else:
                s += r["us_usd"]
        return s

    R = {}
    # (a) all in house ------------------------------------------------------------------------------------------
    a_h = T["total"] + WELD_H
    after_stock = T["setup"] + T["run"] + T["deburr"]
    for key, label, staff, hours_per_wd in (("a1", "All in house, one machinist (full-time)", 1, HD),
                                            ("a2", "All in house, two machinists (one programs, one runs)", 2, HD),
                                            ("a3", "All in house, shop shared: 20 h a week", 1, 4.0)):
        lo, hi = [], []
        for k in (0, 1):
            stock = STOCK_WD[k]
            if staff == 1:
                mach_end = max(T["total"] / hours_per_wd, stock + after_stock / hours_per_wd)
            else:
                mach_end = max(T["cam"] / HD, stock + after_stock / HD)
            hone = stock + HONE_LOOP_WD[k]
            ready = max(mach_end, hone, BUY_WD[k]) + ASSY_WD[k]
            (lo if k == 0 else hi).append(dict(mach_end=mach_end, hone=hone, ready=ready))
        R[key] = dict(label=label, labour_h=round(a_h, 1), labour_usd=round(a_h * RATE), labour_usd_95=round(a_h * RATE_OFF),
                      outside_usd=round(HONE_USD), materials_usd=round(stock_all + TOOLING_BUY),
                      mach_end_wd=[round(lo[0]["mach_end"], 1), round(hi[0]["mach_end"], 1)],
                      hone_back_wd=[lo[0]["hone"], hi[0]["hone"]],
                      ready_wd=[round(lo[0]["ready"], 1), round(hi[0]["ready"], 1)],
                      critical="machining" if lo[0]["mach_end"] >= lo[0]["hone"] else "honing loop")
    # (b) all outsourced ----------------------------------------------------------------------------------------
    b_h = drawings_all + receive_all
    for key, label, price, lead in (("b_cn", "All outsourced: JLCCNC (China) + a US specialist for the module", cn_price(out_all), (7, 9)),
                                    ("b_us", "All outsourced: US instant quotes + job shops", us_price(out_all), (4, 11))):
        lo_hi = []
        for k in (0, 1):
            draw = drawings_all / HD                                   # one engineer
            frame_lead = (FRAME_US_LEAD_WD[k] if key == "b_us" else lead[k] + 1)
            module_lead = MODULE_LEAD_WD[k]
            arrive = draw + PO_WD[k] + max(lead[k], frame_lead, module_lead)
            ready = arrive + (1, 2)[k] + ASSY_WD[k]
            lo_hi.append(dict(draw=draw, arrive=arrive, ready=ready, frame=frame_lead, module=module_lead))
        R[key] = dict(label=label, labour_h=round(b_h, 1), labour_usd=round(b_h * RATE), labour_usd_95=round(b_h * RATE_OFF),
                      outside_usd=round(price + (JLCCNC_SHIP if key == "b_cn" else 0.0)),
                      materials_usd=0, ready_wd=[round(lo_hi[0]["ready"], 1), round(lo_hi[1]["ready"], 1)],
                      drawings_wd=round(lo_hi[0]["draw"], 1), critical="the module weldment (welded, bored and honed outside)",
                      detail=lo_hi)
    # (c) hybrid ------------------------------------------------------------------------------------------------
    make_h = sum(r["total"] for r in make) + WELD_H
    make_after_stock = sum(r["setup"] + r["run"] + r["deburr"] for r in make)
    c_eng = drawings_out + receive_out
    c_h = make_h + buy_adapt + c_eng
    for key, label, price, lead in (("c_cn", "Hybrid: make the seal and module parts, buy 12 catalogue swaps, outsource the rest to JLCCNC",
                                     cn_price(out) + buy_usd + HONE_USD + JLCCNC_SHIP * 0.75, (7, 9)),   # shipping: ESTIMATE, ~3/4 of the weight
                                    ("c_us", "Hybrid with US instant quotes (SendCutSend etc.)", us_price(out) + buy_usd + HONE_USD, (4, 11))):
        lo_hi = []
        for k in (0, 1):
            stock = STOCK_WD[k]
            mach_end = max((make_h + buy_adapt) / HD, stock + (make_after_stock + buy_adapt) / HD)
            hone = stock + HONE_LOOP_WD[k]
            arrive = drawings_out / HD + PO_WD[k] + lead[k]
            ready = max(mach_end, hone, arrive + (1, 2)[k], BUY_WD[k]) + ASSY_WD[k]
            lo_hi.append(dict(mach_end=mach_end, hone=hone, arrive=arrive, ready=ready))
        R[key] = dict(label=label, labour_h=round(c_h, 1), labour_usd=round(c_h * RATE), labour_usd_95=round(c_h * RATE_OFF),
                      outside_usd=round(price), materials_usd=round(sum(r["stock_usd"] for r in make) + TOOLING_BUY),
                      make_parts=len(make), buy_parts=len(buy), out_parts=len(out), make_machining_h=round(make_h, 1),
                      ready_wd=[round(lo_hi[0]["ready"], 1), round(lo_hi[1]["ready"], 1)],
                      critical="honing loop", detail=lo_hi)
    # (d) robot shop --------------------------------------------------------------------------------------------
    R["d"] = dict(label="Robot shop: two UR12e on MiR250s tend the VF-4 and lathe (robot-shop.md)",
                  labour_h=[1430, 2850], labour_usd=[1430 * RATE, 2850 * RATE], outside_usd=round(HONE_USD),
                  equipment_usd=329339, materials_usd=round(stock_all + TOOLING_BUY),
                  in_cell_person_h=[60, 78], in_cell_person_h_note="robot-shop.md, 48 parts, with 35 h of CAM; excludes commissioning",
                  commissioning_h=[1230, 2470], commissioning_weeks=[20, 40],
                  ready_wd=[round(20 * WK + 7 + ASSY_WD[0], 1), round(40 * WK + 7 + ASSY_WD[1], 1)],
                  critical="commissioning the cell (Edison r7 robot-build review, section 5: estimates)")
    for v in R.values():
        lh = v["labour_h"] if isinstance(v["labour_h"], list) else [v["labour_h"], v["labour_h"]]
        fixed = v["outside_usd"] + (v.get("materials_usd") or 0) + (v.get("equipment_usd") or 0)
        v["total_usd_at_65"] = [round(h * RATE + fixed) for h in lh]
        v["total_usd_at_95"] = [round(h * RATE_OFF + fixed) for h in lh]
        v["total_usd_labour_free"] = round(fixed)
        v["ready_cal_days"] = [round(wd2cal(x)) for x in v["ready_wd"]]
        v["ready_weeks"] = [round(wd2cal(x) / 7.0, 1) for x in v["ready_wd"]]
    extras = dict(stock_usd=round(stock_all), tooling_usd=TOOLING_BUY, drawings_all_h=drawings_all, receive_all_h=receive_all,
                  drawings_out_h=drawings_out, receive_out_h=receive_out, buy_adapt_h=buy_adapt, buy_usd=buy_usd,
                  n_make=len(make), n_buy=len(buy), n_out=len(out), n_seal_out=n_seal_out,
                  cn_all_parts_usd=round(cn_price(out_all)), us_all_parts_usd=round(us_price(out_all)),
                  cn_out_usd=round(cn_price(out)), us_out_usd=round(us_price(out)),
                  make_list=[r["part"][:60] for r in make], buy_list=[r["part"][:60] for r in buy], out_list=[r["part"][:60] for r in out])
    return R, extras


FRAME_US_LEAD_WD = (15, 30)        # ESTIMATE: a job shop machining the frame, 3-6 weeks
MODULE_LEAD_WD = (20, 40)          # ESTIMATE: a specialist turns, welds, bores and hones the module, 4-8 weeks


def schedule(R, H):
    """Bars for the Gantt: (route, task, kind, start, end_lo, end_hi) in working days."""
    T = H["totals"]
    S = []

    def add(route, task, kind, start, lo, hi, note=""):
        S.append(dict(route=route, task=task, kind=kind, start_wd=round(start, 1), end_lo_wd=round(lo, 1), end_hi_wd=round(hi, 1), note=note))

    for key in ("a1", "a2", "a3"):
        r = R[key]
        add(key, "stock and tools (BYU PO)", "order", 0, STOCK_WD[0], STOCK_WD[1], "hud.json: 12-20 calendar days")
        if key == "a2":
            add(key, "CAM (programmer)", "cam", 0, T["cam"] / HD, T["cam"] / HD)
            add(key, "setups, cutting, deburr (operator)", "make", STOCK_WD[0], r["mach_end_wd"][0], r["mach_end_wd"][1])
        else:
            rate = HD if key == "a1" else 4.0
            add(key, "CAM, then setups, cutting, deburr (one person)", "make", 0, r["mach_end_wd"][0], r["mach_end_wd"][1],
                f"{T['total']} h at {rate:g} h a working day")
        add(key, "module: weld, bore, hone outside", "outside", STOCK_WD[0] + 1, r["hone_back_wd"][0], r["hone_back_wd"][1],
            "honing 3-6 weeks: estimate, no shop publishes one")
        add(key, "assembly and first leak test", "assy", r["ready_wd"][0] - ASSY_WD[0], r["ready_wd"][0], r["ready_wd"][1])
    for key in ("b_cn", "b_us"):
        r = R[key]
        d0, d1 = r["detail"]
        add(key, "drawings for every part (engineer)", "cam", 0, d0["draw"], d1["draw"], "estimate: 2 h per seal part, 0.5 h per other")
        add(key, "BYU PO", "order", d0["draw"], d0["draw"] + PO_WD[0], d1["draw"] + PO_WD[1], "10-14 calendar days")
        src = "JLCCNC 7 days + UPS 2-4 business days" if key == "b_cn" else "SendCutSend 5-15 days; frame at a job shop 3-6 weeks (estimate)"
        add(key, "parts made outside", "outside", d0["draw"] + PO_WD[0], d0["draw"] + PO_WD[0] + max(7 if key == "b_cn" else 4, d0["frame"]),
            d1["draw"] + PO_WD[1] + max(9 if key == "b_cn" else 11, d1["frame"]), src)
        add(key, "module weldment at a specialist, honed", "outside", d0["draw"] + PO_WD[0], d0["draw"] + PO_WD[0] + MODULE_LEAD_WD[0],
            d1["draw"] + PO_WD[1] + MODULE_LEAD_WD[1], "4-8 weeks: estimate")
        add(key, "receive, inspect, assemble, first leak test", "assy", r["ready_wd"][0] - ASSY_WD[0] - 1, r["ready_wd"][0], r["ready_wd"][1])
    for key in ("c_cn", "c_us"):
        r = R[key]
        d0, d1 = r["detail"]
        add(key, "stock and tools (BYU PO)", "order", 0, STOCK_WD[0], STOCK_WD[1])
        add(key, "make 12 seal and module parts (one machinist)", "make", 0, d0["mach_end"], d1["mach_end"])
        add(key, "drawings, PO, parts made outside", "outside", 0, d0["arrive"], d1["arrive"])
        add(key, "module: weld, bore, hone outside", "outside", STOCK_WD[0] + 1, d0["hone"], d1["hone"])
        add(key, "assembly and first leak test", "assy", r["ready_wd"][0] - ASSY_WD[0], r["ready_wd"][0], r["ready_wd"][1])
    r = R["d"]
    add("d", "commission the cell (Edison: 1,230-2,470 person-h)", "cam", 0, 20 * WK, 40 * WK, "Edison r7 robot-build review, section 5")
    add("d", "cell machining (20 h a day)", "make", 20 * WK, 20 * WK + 7, 40 * WK + 7, "robot-shop.md: about 7 days")
    add("d", "assembly and first leak test", "assy", 20 * WK + 7, r["ready_wd"][0], r["ready_wd"][1])
    return S


# ------------------------------------------------------------------------------------------------------------------
# Chamber alternatives and catalogue swaps
# ------------------------------------------------------------------------------------------------------------------
def chamber_options(rows):
    body = [r for r in rows if r["slug"].startswith(("process_chamber_body", "chamber_floor_plate"))]
    body_h = round(sum(r["total"] for r in body), 1)
    stock = 1860.51 + 267.02 + 150.0             # Speedy Metals 12 x 18 x 5-1/2 in. blank, McMaster 89155K165, waterjet (outsourcing.md)
    post_h = (10.0, 14.0)                         # ESTIMATE: finishing a printed body (see the note)
    machined = stock + body_h * RATE
    p316 = 4826.37 + 270.0 + sum(post_h) / 2 * RATE          # live quote + shipping (estimate) + finishing at $65/h
    pal = 2916.58 + 200.0 + (sum(post_h) / 2 - 2) * RATE
    v2a = (f"workable: ${p316 - machined:,.0f} more than machining at $65/h (${p316:,.0f} against ${machined:,.0f}) for "
           f"{body_h - post_h[1]:.0f}-{body_h - post_h[0]:.0f} h less shop time")
    v2b = (f"workable: about the same money as machining at $65/h (${pal:,.0f} against ${machined:,.0f}) for "
           f"{body_h - post_h[1] + 2:.0f}-{body_h - post_h[0] + 2:.0f} h less shop time; a backup if the VF-4 queue is the bottleneck, "
           "after a design-for-AM pass and a first-article helium test")
    return [
        dict(option="1. Machined 6061 through-frame + bolted floor plate (the design now)",
             body_cost_usd=f"{round(stock + body_h * RATE):,} at BYU (stock ${stock:,.0f} + {body_h} h x $65); outside: floor $83.68 "
                           f"(JLCCNC), frame manual quote (estimate $400-1,500), US job shop $4,000-10,000 (Edison r5)",
             lead_time="3-4 days on the VF-4 inside the shop queue; JLCCNC 6-7 days + 2-4 days UPS",
             in_house_h=f"{body_h} (frame 16.2 + floor 8.7); CAM for both is already programmed and simulated (machining.md round 6)",
             vacuum_o2="designed for it: 1 mbar holds, rate of rise < 1e-3 mbar/min; 1-2 ppm O2 in theory after 3 cycles "
                       "(vacuum-and-purge.md)",
             design_changes="none", risk="low: programs checked in CAMotics and for holder collisions; one more face seal (the floor O-ring)",
             verdict="keep"),
        dict(option="2a. Printed 316L by LPBF, frame + floor as one body, seal faces, bores and threads machined after",
             body_cost_usd="$4,826.37 (JLC3DP live quote, before review) + ~$270 UPS DDP (estimate from its $180-453 shipping lines) "
                           f"+ {post_h[0]:g}-{post_h[1]:g} h of finishing at BYU; outside the China route: $13-35k in the US "
                           "(helper's estimate from AMPower rates)",
             lead_time="3-day build + review + 2-4 business days UPS: about 1.5-2 weeks (JLC3DP; 'about 5 days production' on its blog)",
             in_house_h=f"{post_h[0]:g}-{post_h[1]:g} (estimate: CAM 3-4, three setups 4.5, finishing cuts in 316L 2-4, inspect 1); "
                        f"saves {body_h - post_h[1]:.0f}-{body_h - post_h[0]:.0f} h",
             vacuum_o2="more than enough: machined LPBF 316L reaches the 1e-9 mbar.L/s detection limit (Romanescu 2023) and outgasses "
                       "like wrought 316L (LAL Orsay, IPAC'19); 16 mm walls need no HIP (Edison r7); one seal fewer, so permeation drops "
                       "0.45 ppm O2/h",
             design_changes="add 1-1.5 mm stock on every seal face, bore and datum; stress-relieve on the plate (JLC3DP lists no "
                            "stress relief: ask); door opening's 220 mm top edge and the horizontal bores need supports or "
                            "self-supporting shapes; the floor O-ring and its 18 screws go; 21.8 kg instead of 7.4 kg "
                            "(the VLM tray load, the robot's payload and the module's heat path change)",
             risk="medium: distortion over 312 mm (+/-0.4 % = +/-1.2 mm as built; Edison: <0.5 mm after stress relief); "
                  "a sub-surface pore opened by facing a land (helium check after machining); price subject to review; "
                  "316L machines slower than 6061",
             verdict=v2a),
        dict(option="2b. Printed aluminium by LPBF (JLC3DP 'Aluminum 6061'; AlSi10Mg elsewhere), one body, machined after",
             body_cost_usd="$2,916.58 (JLC3DP live, before review) + shipping; US AlSi10Mg $8-25k (estimate)",
             lead_time="about 1.5-2 weeks (as 2a)",
             in_house_h=f"{post_h[0] - 2:g}-{post_h[1] - 2:g} (estimate; aluminium finishes faster than 316L)",
             vacuum_o2="as 2a: an AlSi10Mg cold-atom chamber with a 2.5 mm skin held < 1e-10 mbar (Cooper et al. 2021)",
             design_changes="as 2a, at 7.3 kg; check what alloy JLC3DP's 'Aluminum 6061' is (it states 172 W/m.K, 15 % "
                            "elongation, service <= 150 C: fine for walls that stay under 60 C)",
             risk="medium: as 2a; a new material at that vendor",
             verdict=v2b),
        dict(option="3. DED (wire-arc or laser-wire) 316L walls on a 316L floor plate, machined all over",
             body_cost_usd="$4,000-12,000 including machining (helper's estimate); Edison $3,000-8,000 + significant machining",
             lead_time="4-8 weeks (estimate); no instant quote anywhere",
             in_house_h="no saving: every face is machined from 0.7-1.8 mm of stock per side, in 316L",
             vacuum_o2="less documented; porosity 0.1-0.5 % (Edison r7): needs a helium test, maybe impregnation",
             design_changes="near-net walls with stock everywhere; heavy (316L)",
             risk="high for a one-off: quote-only vendors, rough surface (Ra > 20 um), distortion",
             verdict="no"),
        dict(option="4. Welded box from cut plate (316L or 5083), seal faces machined after welding",
             body_cost_usd="$1,200-3,500 (Edison r7 estimate: plate, cutting, 8-15 h of TIG, post-weld machining); SendCutSend cuts "
                           "6061 to 0.75 in., 304/5052 to 0.5 in., 316 to 0.25 in., no 5083; its welding excludes 6061 and is 'not "
                           "watertight or gas-tight'",
             lead_time="2-4 weeks (estimate), plus a qualified welder's queue",
             in_house_h="about the same as now: 8-15 h welding + the same top, bottom and wall setups after welding (estimate 20-33 h)",
             vacuum_o2="fine if the welds are sound and helium-tested; Meyer Tool: under 0.5 ft3 with walls of 0.5 in. or more, "
                       "machining from plate is usually cheapest (this body is 0.23 ft3)",
             design_changes="corner welds instead of R10 corners; post-weld stress relief; 6061 HAZ drops to ~110 MPa",
             risk="medium-high: 0.5-2 mm distortion (Edison r3), weld porosity in aluminium, a welder BYU would have to qualify",
             verdict="no: the same machining plus weld risk (chamber-construction.md option 4)"),
        dict(option="5. Catalogue vacuum chamber, modified",
             body_cost_usd="Ideal Vacuum 6 x 12 x 12 in. short cube kit P109160 $4,150.04 (sale; 291 x 291 x 138 mm inside, "
                           "~336 x 336 x 184 outside); LACO 12 in. cube with door $5,850; Lesker BX1212S $7,995",
             lead_time="Ideal Vacuum 'arrives 2026-12-24'; welded cubes 6-8 weeks",
             in_house_h="5 of its 6 plates re-machined (door, slots, ports, window, recoater bores): roughly 15-25 h (estimate)",
             vacuum_o2="certified to ~1e-8 mbar.L/s; fine",
             design_changes="nothing fits the 312 x 222 footprint: the gas envelope grows from 6.4 L to ~11.7 L, the VLM tray "
                            "layout, recoater, gas slots and module port all move; the front door is a full 12 x 12 face",
             risk="low for the vacuum, high for the redesign",
             verdict="no (as in chamber-construction.md option 6)"),
        dict(option="6. Purge-only enclosure (no vacuum): extrusion or sheet with gaskets",
             body_cost_usd="$500-1,500 for extrusion, panels and gaskets (estimate); the ports, window and recoater bores still need "
                           "machined plates",
             lead_time="1-2 weeks (catalogue extrusion and SendCutSend panels)",
             in_house_h="10-15 h (estimate): no glands or Ra 0.8 lands, but the same ports",
             vacuum_o2="what flow-purged machines reach: EOS M 290 measured 731 +/- 98 ppm in argon; MySint100 0.1 %; TruPrint 1000 "
                       "<= 3,000 ppm (100 ppm optional); purge-only gloveboxes 0.5 % (Ossila). Flow-purging 11.3 L to 100 ppm "
                       "takes ~86 L if perfectly mixed, 2-3 times that in practice; no water is pulled out of the powder",
             design_changes="drop the pump and the 1 mbar requirement; argon ~170-260 L a purge (2-3 times the ideal 86 L) and 2-5 L/min while building "
                            "(SLM 125 2 L/min, Aconity < 5 L/min) against ~34 L of back-fill (3 x 11.3 L) and ~50 sccm now",
             risk="process risk, not build risk: hydrogen porosity in aluminium from powder water (Van Cauwenbergh 2019: "
                  "a vacuum pre-cycle gave 13 +/- 4 ppm H in parts against 45 +/- 11 ppm in the powder)",
             verdict="no for an aluminium-screening machine; it saves ~10 h and the pump"),
        dict(option="7. Bolted box of six flat plates, O-rings in every joint",
             body_cost_usd="6 waterjet plates (~$300-600, estimate) + machining",
             lead_time="as option 1",
             in_house_h="about 28 h (estimate: six plates at ~4.5 h of CAM, setups and inspection each): no saving",
             vacuum_o2="eight three-way O-ring junctions: the leak risk the frame avoids",
             design_changes="glands on every edge", risk="medium-high", verdict="no (chamber-construction.md option 5)"),
        dict(option="8. Casting (A356 sand cast from a printed mould, or investment-cast 316)",
             body_cost_usd="$4,500-12,000 one-off with a pattern (Edison r7); a printed sand mould ~EUR 450 at EUR 9/L (helper's "
                           "estimate) + pouring + machining; impregnation $50-200",
             lead_time="6-12 weeks (Edison r7 estimate); every foundry is quote-only",
             in_house_h="about the same machining as now (every face and port)",
             vacuum_o2="castings are more porous than plate (Meyer Tool): vacuum impregnation and a helium test",
             design_changes="draft angles, wall thickness for casting", risk="high for one part", verdict="no"),
    ]


def standard_parts(rows):
    out = []
    for r in rows:
        for k, (what, adapt, usd, cost) in BUY.items():
            if r["slug"].startswith(k):
                out.append(dict(part=r["part"][:80], replacement=what, hours_now=r["total"], hours_after=adapt,
                                hours_saved=round(r["total"] - adapt, 1), catalogue_usd_est=usd, design_cost=cost, call="swap"))
    extra = [  # further swaps that cost the design more, and the parts where a catalogue part would make it worse
        ("Chamber legs, PB1 stand rails, zero-point posts", "cut-to-length precision ground bar or 80/20 extrusion, drilled",
         ("chamber_legs", "pb1_stand", "zero_point_posts"), 1.5, "legs and posts become saw-cut and drilled bar; slots or holes move to "
         "suit extrusion", "swap"),
        ("Optics bridge posts (welded 60 x 60 tube)", "80/20 1515-class extrusion posts with end plates",
         ("optics_bridge_posts",), 2.0, "stiffness of the bridge support to be re-checked (the beam path is aligned to it)", "consider"),
        ("Draw-latch brackets, door drive bracket, shaft and disc", "toggle latches with their own keepers; a catalogue D-bore hub",
         ("draw_latch", "door_drive"), 1.0, "latch force and the door seal's squeeze must be re-checked", "consider"),
        ("AprilTag plates", "printed tags on stock aluminium sheet, bonded", ("apriltag",), 0.3, "none", "swap"),
        ("Base plates (MIC-6)", "MIC-6 cut to size by the supplier + a waterjet profile; drill here", ("base_plate",), None,
         "none (outsourcing.md's hybrid)", "swap"),
        ("Chamber shell, cover-slide drawer, module body and gland plate, metering base, camera boss, heater block, build plate",
         "none that keeps the design", ("process_chamber_body", "chamber_floor_plate", "chamber_lid", "chamber_door",
                                        "cover_slide_drawer", "build_module_m50", "module_m50_bottom", "metering_base",
                                        "camera_viewport", "heater_block", "build_plate"), None,
         "a catalogue cube or box chamber changes the footprint, gas volume and every port (option 5); KF / ISO stubs would have "
         "to be welded to a box (option 4); the module's honed bore and spigot, the bayonet heater and plate, the drawer's "
         "dovetail seal and the doser have no catalogue equivalents", "keep custom"),
    ]
    for name, what, prefs, adapt_each, cost, call in extra:
        rs = [r for r in rows if r["slug"].startswith(prefs)]
        now = round(sum(r["total"] for r in rs), 1)
        if adapt_each is None:
            after = round(now / 2, 1) if call == "swap" else now
        else:
            after = round(adapt_each * len(rs), 1)
        out.append(dict(part=name, replacement=what, hours_now=now, hours_after=after, hours_saved=round(now - after, 1),
                        catalogue_usd_est="", design_cost=cost, call=call))
    return out


# ------------------------------------------------------------------------------------------------------------------
# Figures
# ------------------------------------------------------------------------------------------------------------------
PAL = dict(cam="#257de0", setup="#f47230", run="#00b894", deburr="#f2a600", assy="#ee7fac",
           order="#f2a600", make="#00b894", outside="#f47230")
TXT, TXT2, GRID = "#191919", "#666666", "#e6e6e6"


def fig_hours(H, path):
    gs = sorted(H["groups"], key=lambda g: g["total"])
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=130)
    acts = [("cam", "CAM programming"), ("setup", "setups"), ("run", "cutting"), ("deburr", "deburr + inspect")]
    for i, g in enumerate(gs):
        x = 0.0
        for a, lab in acts:
            w = g[a]
            ax.barh(i, w, left=x, height=0.62, color=PAL[a], edgecolor="white", linewidth=1.5, label=lab if i == 0 else None)
            if w >= 6:
                ax.text(x + w / 2, i, f"{w:.0f}", ha="center", va="center", fontsize=8, color=TXT)
            x += w
        ax.text(x + 1.5, i, f"{g['total']:.0f} h  ({g['parts']} parts, {g['share_pct']:.0f} %)", va="center", fontsize=8.5, color=TXT)
    ax.set_yticks(range(len(gs)), [SHORT[g["group"]] for g in gs], fontsize=9, color=TXT)
    ax.set_xlabel("shop hours (hours.py, 4th axis where it helps)", fontsize=9, color=TXT2)
    ax.set_xlim(0, max(g["total"] for g in gs) * 1.45)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    T = H["totals"]
    ax.set_title(f"Where the {T['total']:.1f} h go: CAM {T['cam']:.0f} h, setups {T['setup']:.0f} h, cutting {T['run']:.0f} h, "
                 f"deburr + inspect {T['deburr']:.0f} h (57 parts)", fontsize=10.5, color=TXT, loc="left")
    ax.legend(loc="lower right", fontsize=8.5, frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_gantt(R, S, path):
    order = [("a1", "a) In house, 1 machinist"), ("a2", "a) In house, 2 machinists"), ("a3", "a) In house, shared 20 h/wk"),
             ("b_cn", "b) All outsourced (JLCCNC)"), ("c_cn", "c) Hybrid (JLCCNC)"), ("d", "d) Robot shop")]
    kinds = [("order", "ordering (BYU PO, stock)"), ("cam", "programming / drawings / commissioning"),
             ("make", "machining at BYU"), ("outside", "made or honed outside"), ("assy", "assembly + first leak test")]
    fig, axes = plt.subplots(len(order), 1, figsize=(11, 10.5), dpi=130, sharex=True,
                             gridspec_kw=dict(height_ratios=[len([s for s in S if s["route"] == k]) + 0.6 for k, _ in order]))
    xmax = 20.0
    for ax, (key, title) in zip(axes, order):
        bars = [s for s in S if s["route"] == key]
        for i, s in enumerate(bars):
            y = len(bars) - 1 - i
            x0, lo, hi = (wd2cal(s[k]) / 7.0 for k in ("start_wd", "end_lo_wd", "end_hi_wd"))
            col = PAL[s["kind"]]
            if x0 >= xmax - 0.5:              # starts off the chart (the robot shop after commissioning): text only
                ax.text(xmax - 0.1, y, f"{s['task']}: weeks {x0:.0f}-{hi:.0f}, off this chart  →", ha="right", va="center",
                        fontsize=7.5, color=TXT)
                continue
            if s["kind"] == "assy" and hi > lo:   # two separate bars: the low case, and the high case (hatched)
                dur = lo - x0
                ax.barh(y, dur, left=x0, height=0.6, color=col, edgecolor="white", linewidth=1.2)
                hd = dur * ASSY_WD[1] / ASSY_WD[0]
                ax.barh(y, min(hd, xmax - (hi - hd)), left=hi - hd, height=0.6, color=col, alpha=0.35, hatch="////",
                        edgecolor="white", linewidth=0.0)
            else:
                ax.barh(y, max(min(lo, xmax) - x0, 0.05), left=x0, height=0.6, color=col, edgecolor="white", linewidth=1.2)
                if hi > lo:
                    ax.barh(y, min(hi, xmax) - min(lo, xmax), left=min(lo, xmax), height=0.6, color=col, alpha=0.35, hatch="////",
                            edgecolor="white", linewidth=0.0)
            if hi > xmax:
                ax.text(xmax - 0.1, y + 0.42, f"{s['task']}: to week {lo:.0f}-{hi:.0f}  →", ha="right", va="center", fontsize=7.5,
                        color=TXT)
                continue
            lab = s["task"] + (f"  ({lo:.1f}-{hi:.1f} wk)" if hi - lo > 0.05 else f"  ({lo:.1f} wk)")
            ax.text(min(max(hi, lo), xmax) + 0.15, y, lab, va="center", fontsize=7.5, color=TXT)
        r = R[key]
        lo_w, hi_w = r["ready_weeks"]
        ax.set_ylim(-0.7, len(bars) - 0.3 + (0.35 if key == "d" else 0))
        ax.set_yticks([])
        span = f"{lo_w:.0f}" if round(lo_w) == round(hi_w) else f"{lo_w:.0f}-{hi_w:.0f}"
        ax.set_title(f"{title}: first leak test in {span} weeks", fontsize=9.5, color=TXT, loc="left", pad=3)
        ax.axvspan(83 / 7.0, 105 / 7.0, color="#cccccc", alpha=0.35, linewidth=0)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
    axes[0].text(94 / 7.0, axes[0].get_ylim()[1] - 0.2, "new IPG laser arrives\n(weeks 12-15, hud.json)", ha="center", va="top",
                 fontsize=7.5, color=TXT2)
    axes[-1].set_xlim(0, xmax)
    axes[-1].set_xlabel("calendar weeks from the purchase order (daytime work only: 8 h a day, 5 days a week; holidays not counted)",
                        fontsize=8.5, color=TXT2)
    handles = [Patch(color=PAL[k], label=l) for k, l in kinds] + [Patch(facecolor="#999999", alpha=0.35, hatch="////", label="low to high estimate")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("PO to the first leak test, by route (route_calcs.py; bars are estimates, see manufacturing-route.md)",
                 fontsize=11, color=TXT, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.05, 1, 0.97))
    fig.savefig(path)
    plt.close(fig)


def write_csv(path, rows):
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()})


def main():
    rows = read_parts()
    H = hours_tables(rows)
    R, X = routes(rows, H)
    S = schedule(R, H)
    C = chamber_options(rows)
    P = standard_parts(rows)
    IMG.mkdir(parents=True, exist_ok=True)
    write_csv(RB / "route-hours-by-part.csv", [dict(part=r["part"], group=SHORT[r["group"]], machine=r["machine"], material=r["mat"],
                                                    setups_4th=r["setups"], cam_h=r["cam"], setup_h=r["setup"], cutting_h=r["run"],
                                                    deburr_inspect_h=r["deburr"], total_h=r["total"], total_h_3axis=r["total_3axis"],
                                                    one_off_h=r["one_off"], per_batch_h=r["per_batch"], per_machine_h=r["per_machine"],
                                                    seal_part=r["seal"], us_outside_usd=r["us_usd"], jlccnc_usd=r["cn_usd"],
                                                    stock_usd=r["stock_usd"]) for r in sorted(rows, key=lambda r: -r["total"])])
    write_csv(RB / "route-hours-by-group.csv", H["groups"])
    route_rows = []
    for k, v in R.items():
        route_rows.append(dict(route=k, label=v["label"], labour_h=v["labour_h"], labour_usd_at_65=v["labour_usd"],
                               outside_usd=v["outside_usd"], materials_and_tools_usd=v.get("materials_usd", ""),
                               equipment_usd=v.get("equipment_usd", ""), total_usd_at_65=v["total_usd_at_65"],
                               total_usd_at_95=v["total_usd_at_95"], total_usd_labour_free=v["total_usd_labour_free"],
                               ready_working_days=v["ready_wd"],
                               ready_calendar_days=v["ready_cal_days"], ready_weeks=v["ready_weeks"], critical_path=v["critical"]))
    write_csv(RB / "route-routes.csv", route_rows)
    write_csv(RB / "route-schedule.csv", S)
    write_csv(RB / "route-chamber-options.csv", C)
    write_csv(RB / "route-standard-parts.csv", P)
    fig_hours(H, IMG / "route-hours.png")
    fig_gantt(R, S, IMG / "route-gantt.png")
    swaps = [p for p in P if p["call"] == "swap"]
    summary = dict(
        generated_by="desktop-lpbf/analysis/route/route_calcs.py", note="manufacturing-route.md (round 7); estimates labelled there",
        hours=dict(total_4th=H["totals"]["total"], cam=H["totals"]["cam"], setups=H["totals"]["setup"], cutting=H["totals"]["run"],
                   deburr_inspect=H["totals"]["deburr"], parts=len(rows), chamber=H["chamber"], split=H["split"],
                   fixed_overhead_h=H["fixed_overhead_h"], small_parts=H["small_parts"],
                   second_machine_later_h=H["second_machine_later_h"], two_machines_together_h=H["two_machines_together_h"],
                   low_allowances=H["low_allowances"],
                   top10=H["top10"], groups=[dict(group=SHORT[g["group"]], h=g["total"], pct=g["share_pct"]) for g in H["groups"]]),
        routes={k: dict(label=v["label"], labour_h=v["labour_h"], labour_usd=v["labour_usd"], outside_usd=v["outside_usd"],
                        materials_usd=v.get("materials_usd"), equipment_usd=v.get("equipment_usd"),
                        total_usd_at_65=v["total_usd_at_65"], total_usd_at_95=v["total_usd_at_95"],
                        total_usd_labour_free=v["total_usd_labour_free"],
                        calendar_days_to_leak_test=v["ready_cal_days"], weeks_to_leak_test=v["ready_weeks"], critical=v["critical"])
                for k, v in R.items()},
        chamber_share=dict(frame_floor_h=H["chamber"]["frame_floor_h"], frame_floor_pct=H["chamber"]["frame_floor_pct"],
                           shell_h=H["chamber"]["shell_h"], shell_pct=H["chamber"]["shell_pct"]),
        chamber_options=[dict(option=c["option"], cost=c["body_cost_usd"][:140], lead=c["lead_time"][:80], verdict=c["verdict"]) for c in C],
        standard_parts=dict(swaps=len(swaps), hours_saved=round(sum(p["hours_saved"] for p in swaps), 1)),
        quotes=dict(jlc3dp_frame_316l=2833.47, jlc3dp_body_316l=4826.37, jlc3dp_frame_al=1716.66, jlc3dp_body_al=2916.58,
                    jlc3dp_build_days=3, jlccnc_62_pieces_qty1=2437.49, jlccnc_lead_days="7 + 2-4 UPS",
                    jlccnc_lid=64.99, jlccnc_floor=83.68, jlccnc_door=33.74, jlccnc_frame="manual quote"),
        laser_weeks=dict(new_ipg=[round(83 / 7, 1), round(105 / 7, 1)], used=[0.4, 1.1]),
        extras=X)
    (RB / "route-summary.json").write_text(json.dumps(summary, indent=1))
    TMPJSON.parent.mkdir(parents=True, exist_ok=True)
    TMPJSON.write_text(json.dumps(summary, indent=1))
    T = H["totals"]
    print(f"total {T['total']} h: CAM {T['cam']} ({100 * T['cam'] / T['total']:.0f} %), setups {T['setup']}, cutting {T['run']}, "
          f"deburr {T['deburr']}")
    print("chamber:", H["chamber"])
    print("split:", H["split"], "second machine later", H["second_machine_later_h"], "two together", H["two_machines_together_h"])
    print("fixed overhead", H["fixed_overhead_h"], "small parts", H["small_parts"], "low allowances", H["low_allowances"])
    for g in H["groups"]:
        print(f"  {SHORT[g['group']]:18s} {g['parts']:3d} parts {g['total']:6.1f} h {g['share_pct']:5.1f} %  CAM {g['cam']:5.1f} "
              f"setup {g['setup']:5.1f} run {g['run']:5.1f} deburr {g['deburr']:4.1f}")
    for k, v in R.items():
        print(f"{k:5s} {v['labour_h']} h, ${v['labour_usd']}, outside ${v['outside_usd']}, mat {v.get('materials_usd')}, "
              f"ready {v['ready_wd']} wd = {v['ready_cal_days']} d = {v['ready_weeks']} wk; {v['critical']}")
    print("extras", {k: v for k, v in X.items() if not k.endswith("_list")})
    print("swaps", len(swaps), "saved h", round(sum(p["hours_saved"] for p in swaps), 1))


if __name__ == "__main__":
    main()
