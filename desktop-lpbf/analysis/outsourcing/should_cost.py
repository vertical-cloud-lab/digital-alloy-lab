"""Should-cost of every custom part of the desktop LPBF (issue #260, PR #266): made in BYU's shops vs outsourced, and the
make / outsource / buy-instead call for each, with the schedule effect.

Inputs (all in the repo):
  analysis/out/outsourcing/parts.csv     the 82 custom parts from export_parts.py (qty, material, envelope, process class)
  analysis/out/machining/hours.csv       CAM, setup, run, deburr + inspect hours per machined part (hours.py)
  analysis/out/machining/dfm.json        stock volume per machined part (dfm.py)
  outsourcing-quotes.csv                 the instant quotes recorded on 2026-11-22 (one row per attempt)
  tooling-bom.csv                        tools to buy for the in-house route ('buy for this job')

In-house cost = hours (4th-axis column of hours.csv) x RATE + stock (stock volume x density x price per kg) + finishing
that has to go out anyway (honing, passivation). The 'buy for this job' tooling is a one-off cost of the in-house route.
Outsourced cost = the instant quote x qty where one was shown; otherwise a labelled estimate:
  'fit'      the unit price predicted from in-house hours by a least-squares fit to the SendCutSend CNC quotes
             (only for 6061 parts inside SendCutSend's 8 x 8 x 12 in. billet limit);
  'jobshop'  hours x JOBSHOP_RATE x 1.2 + stock, for parts no instant service took (too big, 316L, weldments);
  'edison'   an Edison r5-outsourcing planning range (edison/r5-outsourcing/answer.md), not a quote.
Every number's source is in the 'basis' column of should_cost.csv.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/outsourcing/should_cost.py   (writes should_cost.csv / .json next to parts.csv)
"""
from __future__ import annotations

import csv
import json
import pathlib

import numpy as np

D = pathlib.Path(__file__).resolve().parents[2]
OUT = D / "analysis" / "out" / "outsourcing"

# Rates. RATE: BYU Prototype Manufacturing Lab (now the Physical Facilities Manufacturing Shop) labour for academic
# departments, $65/h ($85 non-academic, $95 off campus): pml.byu.edu/labor, seen only in search-result text
# (2026-11-22 05:30 UTC; the page itself blocked automated reads). Other university shops publish $59-100/h internal
# (Clemson, ASU, Iowa, Boise State; research.csv). JOBSHOP_RATE: midpoint of $75-150/h for 3-axis work (Fabcon 2026
# article; Edison r5 table 4). The ME Prototyping Lab is free to students: then RATE_FREE is 0 and only the hours count.
RATE, RATE_HIGH, RATE_FREE, JOBSHOP_RATE = 65.0, 95.0, 0.0, 110.0
SHOP_HOURS_PER_WEEK = 20.0     # assumption: one person's half-time on the VF-4 and lathe; sets the in-house queue length
# Stock price per kg. 6061: Speedy Metals 5-1/2 in. 6061-T651, 12 x 18 in., $1,860.51 for 121.3 lb = $33.8/kg
# (speedymetals.com p-2430, 2026-11-22 05:30 UTC). The others are estimates (labelled in the output).
PRICE_KG = {"6061-T6": 33.8, "MIC-6 cast tooling plate": 33.8, "316L": 45.0, "416 stainless": 40.0, "304": 40.0}
RHO = {"6061-T6": 2.70, "MIC-6 cast tooling plate": 2.70, "316L": 8.0, "416 stainless": 7.8, "304": 7.9, "Macor": 2.52}
STOCK_SOURCED = {"6061-T6", "MIC-6 cast tooling plate"}
HONE_USD = 400.0     # one bore to H7 / Ra 0.4: estimate from research.csv ($150-400) and Edison r5 ($250-750 minimum per job)
PASSIVATE_USD = 150.0  # 316L lot charge (Edison r5 table 4, $100-250 campus, $150-400 commercial; no published list found)
WELD_H = 3.0         # TIG of the module's three circumferential seams with back-purge, fixture and chill mandrel (estimate)

# Make / outsource / buy-instead, with the reason, by slug prefix (first match wins). Categories of reason:
# capability, tolerance and finish, lead time, cost, risk.
CALLS = [
    ("process_chamber_body", "make (buy the cut blank)", "capability + tolerance and finish",
     "No instant service takes it (SendCutSend CNC stops at 8 x 8 x 12 in.). It carries the lid gland, the floor rebate and every port; "
     "keep the seal faces and their rework on campus. Buy the 5-1/2 in. blank cut to size and have the core waterjetted."),
    ("chamber_floor_plate", "make", "tolerance and finish + cost",
     "Seal faces and the Ø96 H7 module port; SendCutSend CNC quoted $1,076 (Dec 7) against ~$660 in house. Keep it with the frame."),
    ("chamber_lid", "make", "tolerance and finish",
     "Gland, window seat and the drawer slot that is still drawn enclosed: an online DFM check is likely to bounce it; fix the slot first."),
    ("chamber_door", "make", "tolerance and finish",
     "Half-dovetail seal groove (special cutter) and the hinge/latch datums; the quote does not cover the dovetail."),
    ("cover_slide_drawer", "make", "tolerance and finish", "Half-dovetail seal groove; sliding fit to the lid slot."),
    ("build_module_m", "outsource (specialist)", "capability",
     "Honing to H7 / Ra 0.4 after welding: no BYU shop hones. Turn and weld in house, then send out for boring and honing, or buy the "
     "finished weldment from a cylinder shop."),
    ("module_m50_bottom_flange", "make", "capability + cost", "Lathe part with internal grooving; 316L stock is cheap and the tools are in the BOM."),
    ("window_flange", "buy instead", "cost + risk", "machining.md lever 1: a stock fused-silica viewport replaces the flange and ring."),
    ("window_retaining", "buy instead", "cost", "machining.md lever 1: part of the stock viewport."),
    ("f_theta_adapter", "buy instead", "cost", "machining.md lever 1: Thorlabs SM-series adapter; the M85 x 1 thread is the costly bit."),
    ("field_stop", "buy instead", "cost", "machining.md lever 1: Thorlabs SM-series aperture."),
    ("enclosed_beam_tube", "buy instead", "cost", "machining.md lever 1: Thorlabs SM-series lens tube."),
    ("camera_window_retaining", "buy instead", "cost", "machining.md lever 1: Thorlabs SM1 retaining ring."),
    ("recoater_motor_standoff", "buy instead", "cost", "machining.md lever 1: stock NEMA 23 bracket."),
    ("recoater_motor_bracket", "buy instead", "cost", "machining.md lever 1: stock NEMA 23 bracket."),
    ("door_handle", "buy instead", "cost", "machining.md lever 1: catalogue pull."),
    ("guard_door_handle", "buy instead", "cost", "machining.md lever 1: catalogue pull."),
    ("macor", "buy instead", "cost + risk", "machining.md lever 1: stock ceramic washers; Macor chips and dusts on a shared lathe."),
    ("striker", "buy instead", "cost", "machining.md lever 1: a stock 416 or 430 disc."),
    ("hollow_piston_rod", "make", "capability", "Cut and polish bought seamless tube; welded into the rod end in house."),
    ("base_plate", "outsource the profile, drill in house", "capability + cost",
     "Wider than the VF-4's Y travel (gas plate) and past SendCutSend's CNC limit; buy the profile cut (SendCutSend $666-690 in 1/2 in. "
     "MIC-6 or 5/8 in. 6061) or order MIC-6 cut to size, then drill and tap on the mill."),
    ("optics_bridge_6061", "make (buy plate at 1 in.)", "capability",
     "605 x 370 mm, past SendCutSend's CNC limit and its 3/4 in. cutting limit; waterjet the windows on campus, mill the datums."),
    ("optics_bridge_posts", "make", "capability", "6061 tube with TIG-welded caps: the campus weld shop and the mill."),
    ("overflow_funnel", "outsource", "cost", "316L, simple: JLCCNC showed $79-123 in 304 (316L not in its instant list); confirm 316L by request."),
    ("rod_end", "make", "capability", "Small 316L lathe part with the rod welded in; the weld and the hermetic boss stay on campus."),
    ("heater_block", "make", "tolerance and finish + risk",
     "Bayonet socket with an internal groove (lathe); the online quote cannot see the undercut and the part will iterate in thermal tests."),
    ("build_plate", "make", "tolerance and finish + risk", "Bayonet lugs to +/-0.02 mm on the lathe; iterates with the heater block."),
    ("piston_head", "make", "risk", "Radial seal grooves (lathe) and thin webs still to fix; iterates with the module."),
    ("camera_viewport", "outsource", "capability",
     "Compound-angle boss: a 5-axis job; SendCutSend CNC quoted $379 (Nov 30). Check that their 3-axis process can hold it, or turn the boss as a separate part."),
]
# Robot assembly tooling (assembly-tooling.csv lines C1-C9): process, in-house hours and material (its ESTIMATE column)
TOOLING = {
    "spigot_mandrel": ("lathe (acetal)", 1.0, 40.0), "spigot_pusher": ("lathe (acetal tube)", 1.0, 40.0),
    "rod_bullet": ("lathe (PEEK)", 0.5, 25.0), "ring_loader": ("slotted stainless tube + plunger", 1.5, 60.0),
    "roller_3p2": ("aluminium fork + PTFE wheel + spring", 1.5, 125.0), "roller_1p4": ("aluminium fork + PTFE wheel + spring", 1.5, 125.0),
    "ring_caps_left": ("print + steel pins", 0.5, 7.5), "ring_caps_right": ("print + steel pins", 0.5, 7.5),
    "fixture_C": ("aluminium plate + strips, mill", 3.0, 180.0), "fixture_P": ("steel tube and plate, weld", 2.0, 150.0),
    "fixture_B": ("steel tube and plate, weld", 3.0, 250.0), "nest_body_inv": ("print or machine", 1.0, 20.0),
    "nest_body_up": ("print or machine", 1.0, 20.0), "nest_stack": ("print or machine", 1.0, 20.0),
}
# Catalogue parts that replace a machined one (machining.md lever 1). Prices are ESTIMATES, not fetched this run, except
# the McMaster 5537T419 pull ($8.64, from safety-parts.csv); each takes about 1 h to adapt (machining.md).
BUY_INSTEAD = {
    "window_flange": (450.0, "estimate: stock fused-silica viewport (covers the flange and the ring)"),
    "window_retaining": (0.0, "part of the stock viewport"), "f_theta_adapter": (60.0, "estimate: Thorlabs SM-series thread adapter"),
    "field_stop": (40.0, "estimate: Thorlabs SM-series iris or aperture"), "enclosed_beam_tube": (35.0, "estimate: Thorlabs SM-series lens tube"),
    "camera_window_retaining": (10.0, "estimate: Thorlabs SM1 retaining ring"),
    "recoater_motor_bracket": (30.0, "estimate: stock NEMA 23 bracket (covers the standoff)"), "recoater_motor_standoff": (0.0, "part of the NEMA 23 bracket"),
    "door_handle_1": (8.64, "McMaster 5537T419 pull, $8.64 (safety-parts.csv)"), "door_handle_2": (0.0, "part of the pull"),
    "guard_door_handle_for_the_robot_12_x_130_bar_on_two_10_stand_1": (8.64, "McMaster 5537T419 pull, $8.64 (safety-parts.csv)"),
    "guard_door_handle_for_the_robot_12_x_130_bar_on_two_10_stand_2": (0.0, "part of the pull"),
    "macor": (7.5, "estimate: stock ceramic washers, $15 for the 9 rings"), "striker": (10.0, "estimate: stock 416 or 430 disc"),
}
SHEET_CALL = ("outsource", "capability + cost + lead time",
              "Laser-cut sheet: no campus fibre laser for metal; SendCutSend and OSH Cut price these at $4-140 each with 5-6 day delivery.")
WELDED_SHEET = ("outsource the cut-and-bent pieces, weld in house", "capability",
                "316L sheet weldment: the online services cut and bend single pieces (OSH Cut could not process the welded assembly); "
                "TIG with back-purge on campus, then machine the flange faces.")
PRINT_CALL = ("make", "cost + lead time", "Lab-made robot tooling (assembly-tooling.csv C1-C9): lathe, plate, tube or print; "
              "JLC3DP's resin price for the mandrel ($26 + $17-23 shipping, 2-3 weeks) is for scale.")
DEFAULT_CALL = ("outsource", "cost + lead time",
                "Simple 6061 part with no seal face: SendCutSend CNC at $48-435 delivered in 6-8 days costs less than the "
                "~3.5 h of CAM, setups and inspection it takes here at $65/h, and frees the mill for the seal parts.")


def call_for(slug, kind):
    if kind == "printed":
        return PRINT_CALL
    if kind == "sheet":
        return WELDED_SHEET if any(k in slug for k in ("plenum", "dose_chute", "gas_knife", "reservoir_m_97")) else SHEET_CALL
    for k, c, why, note in CALLS:
        if slug.startswith(k) or k in slug:
            return c, why, note
    return DEFAULT_CALL


def main():
    parts = list(csv.DictReader(open(OUT / "parts.csv")))
    hours = {r["slug"]: r for r in csv.DictReader(open(D / "analysis" / "out" / "machining" / "hours.csv"))}
    alias = {"door_drive_bracket": "door_damper_bracket", "door_drive_shaft": "door_damper_shaft"}
    dfm = {r["slug"]: r for r in json.loads((D / "analysis" / "out" / "machining" / "dfm.json").read_text())["parts"]}
    quotes = list(csv.DictReader(open(D / "outsourcing-quotes.csv")))
    tooling = sum(float(r["line_usd"] or 0) for r in csv.DictReader(open(D / "tooling-bom.csv")) if r["flag"] == "buy for this job")

    def hrow(slug):
        if slug in hours:
            return hours[slug]
        for a, b in alias.items():
            if slug.startswith(a):
                return next((v for k, v in hours.items() if k.startswith(b)), None)
        return None

    # pick the quote used for each file: SendCutSend CNC for machined parts, the sheet quote for sheet parts
    best = {}
    for q in quotes:
        if not q["unit_usd"]:
            continue
        f = q["part"]
        prio = {"SendCutSend CNC": 0, "SendCutSend": 1, "OSH Cut": 2, "JLCCNC": 3, "JLC3DP": 4}.get(q["service"], 9)
        if "thickness check" in q["material_and_process_as_quoted"] or "for scale only" in q["material_and_process_as_quoted"]:
            prio += 5
        if f not in best or prio < best[f][0] or (prio == best[f][0] and float(q["unit_usd"]) < float(best[f][1]["unit_usd"])):
            best[f] = (prio, q)

    # fit: SendCutSend CNC unit price vs in-house hours (qty-1 quotes only)
    xs, ys = [], []
    for f, (_, q) in best.items():
        if q["service"] != "SendCutSend CNC" or q["qty"] not in ("1", 1):
            continue
        p = next((r for r in parts if r["file"] == f), None)
        h = hrow(p["slug"]) if p else None
        if h:
            xs.append(float(h["total_h_4th"]))
            ys.append(float(q["unit_usd"]))
    A = np.vstack([np.ones(len(xs)), xs]).T
    coef, *_ = np.linalg.lstsq(A, np.array(ys), rcond=None)
    r2 = 1 - np.sum((A @ coef - ys) ** 2) / np.sum((np.array(ys) - np.mean(ys)) ** 2)

    rows = []
    for p in parts:
        slug, f, kind, mat = p["slug"], p["file"], p["kind"], p["material"]
        qty = int(p["qty_per_machine"])
        h = hrow(slug) if kind == "stock" else None
        # in-house hours: machined parts from hours.csv (one program and setups per part number, + run per piece);
        # sheet parts: 1.5 h per piece (layout, shear/saw, brake, deburr; estimate) + 2 h of TIG for the welded ones; printed: 0.5 h
        if h:
            hrs = float(h["total_h_4th"]) + (qty - 1) * (float(h["run_h"]) + float(h["deburr_inspect_h"]))
            hbasis = "hours.csv (4th-axis column)"
        elif kind == "sheet":
            hrs = 1.5 * qty + (2.0 if any(k in slug for k in ("plenum", "dose_chute", "gas_knife", "reservoir_m_97")) else 0.0)
            hbasis = "estimate: 1.5 h a piece (+2 h TIG for the welded ones)"
        else:
            tk = TOOLING.get(f.replace("tooling_", ""), ("print", 0.5, 10.0))
            hrs = tk[1]
            hbasis = f"assembly-tooling.csv estimate ({tk[0]})"
        # stock
        d = dfm.get(slug, {})
        if mat == "Macor":
            stock, sbasis = 148.0 / 2, "Macor 0.5 in. x 12 in. rod $147.99 (Zoro, search text), half a rod"
        elif kind == "printed":
            stock, sbasis = TOOLING.get(f.replace("tooling_", ""), ("", 0, 10.0))[2], "assembly-tooling.csv ESTIMATE column (material)"
        elif slug.startswith("process_chamber_body"):
            stock = 1860.51 + 150.0
            sbasis = "Speedy Metals 5-1/2 in. 6061-T651 12 x 18 in. piece $1,860.51 (published, freight extra) + ~$150 waterjet core (estimate)"
        elif kind == "sheet":
            stock = float(p["volume_cm3"]) * RHO.get(mat, 2.7) / 1000 * qty * 1.5 * (12.0 if mat in ("316L", "304") else 8.0)
            sbasis = "sheet: part mass x 1.5 for the nest x $8/kg (Al) or $12/kg (stainless) (estimate)"
        else:
            vol = float(d.get("stock_cm3") or float(p["volume_cm3"]) * 2.0)
            kg = vol * RHO.get(mat, 2.7) / 1000 * qty
            stock = kg * PRICE_KG.get(mat, 40.0)
            sbasis = ("dfm.json stock x $33.8/kg (Speedy Metals 5-1/2 in. plate)" if mat in STOCK_SOURCED
                      else f"dfm.json stock x ${PRICE_KG.get(mat, 40.0):.0f}/kg (estimate)")
        extra, ebasis = 0.0, ""
        if slug.startswith("build_module_m"):
            extra, ebasis = HONE_USD + PASSIVATE_USD + WELD_H * RATE, "honing sent out + passivation lot + 3 h TIG"
        in_house = hrs * RATE + stock + extra
        # outsourced
        q = best.get(f, (None, None))[1]
        if q:
            out = float(q["unit_usd"]) * qty
            obasis = f"quote: {q['service']} ${float(q['unit_usd']):.2f} x {qty} ({q['fetched_utc']})"
            lead = q["lead_time"]
        elif slug.startswith("build_module_m"):
            out, obasis, lead = 1200.0, "edison: specialist finished cylinder $600-1,800 each (Edison r5 table 2), midpoint", "3-6 weeks (estimate)"
        elif slug.startswith("base_plate_process"):
            out = 689.66 * (730 * 480) / (590 * 550)
            obasis, lead = "scaled by area from the SendCutSend quote for the gas-module plate (6061 5/8 in., $689.66)", "about 9 days"
        elif kind == "sheet" and any(k in slug for k in ("plenum", "dose_chute", "gas_knife", "reservoir_m_97")):
            out = 60.0 * qty
            obasis = ("estimate: cut and bend only, $60 a part (OSH Cut priced the 171 x 94 mm 316 liner at $22.85; x2.5 for bends and "
                      "more pieces); a welded plenum from a fab shop is $500-2,000 (Edison r5 table 2)")
            lead = "about 1-2 weeks"
        elif kind == "sheet":
            dims = sorted((float(x) for x in p["envelope_mm"].split(" x ")), reverse=True)
            area = dims[0] * dims[1] / 1e6
            if mat in ("316L", "304"):
                out, obasis = 25.0 * qty, "estimate: like OSH Cut's $22.85 for the 171 x 94 mm 316 liner"
            else:
                out = (22.0 + 142.0 * area) * qty * (1.5 if "vented" in slug else 1.0)
                obasis = ("estimate: $22 + $142/m² from SendCutSend's 5052 0.063 in. quotes ($58.57 for 0.253 m², $76.81 for 0.385 m²)"
                          + ("; x1.5 for the vent slots" if "vented" in slug else ""))
            lead = "about 1 week (SendCutSend's delivered dates were 5-6 days out)"
        elif slug.startswith("process_chamber_body"):
            out, obasis, lead = 7000.0, "edison: turnkey job shop $4,000-10,000+ (Edison r5 table 2), midpoint", "4-8 weeks (estimate)"
        elif kind == "stock" and mat == "6061-T6" and max(float(x) for x in p["envelope_mm"].split(" x ")) <= 304.8 and h:
            out = (coef[0] + coef[1] * float(h["total_h_4th"])) * (1.0 if qty == 1 else 0.6 * qty)
            obasis = f"fit: ${coef[0]:.0f} + ${coef[1]:.0f}/h x in-house hours (SendCutSend CNC, n = {len(xs)}, R² = {r2:.2f})"
            lead = "about 1 week (SendCutSend CNC delivered dates were 6-15 days out)"
        elif kind == "printed" and TOOLING.get(f.replace("tooling_", ""), ("print",))[0].startswith("print"):
            out, obasis, lead = 26.2 / 288.0 * float(p["volume_cm3"]) + 17.1, "scaled: JLC3DP $26.20 for 288 cm³ of resin + $17.10 shipping", "2-3 weeks"
        else:
            out = hrs * JOBSHOP_RATE * 1.2 + stock + extra
            obasis = f"jobshop: {hrs:.1f} h x ${JOBSHOP_RATE:.0f}/h x 1.2 + stock"
            lead = "2-4 weeks (estimate)"
        c, why, note = call_for(slug, kind)
        if c == "buy instead":
            key = next((k for k in BUY_INSTEAD if f.startswith(k) or k in f), None)
            cat, cbasis = BUY_INSTEAD.get(key, (25.0, "estimate"))
            rec, rbasis = cat + (1.0 * RATE if cat else 0.0), cbasis + (" + 1 h to adapt" if cat else "")
        elif c.startswith("make") or c.startswith("outsource (specialist)"):
            rec, rbasis = in_house, "in house" + (" (honing and passivation bought in)" if extra else "")
        elif c.startswith("outsource the profile"):
            rec, rbasis = out + 0.5 * hrs * RATE, "profile quote + half the in-house hours (drill and tap)"
        elif c.startswith("outsource the cut-and-bent"):
            rec, rbasis = out + 2.0 * RATE, "cut-and-bend + 2 h TIG in house"
        else:
            rec, rbasis = out, "outsourced"
        hrec = {"buy instead": 1.0 if rec else 0.0}.get(c, 0.0)
        if c.startswith("make") or c.startswith("outsource (specialist)"):
            hrec = hrs
        elif c.startswith("outsource the profile"):
            hrec = 0.5 * hrs
        elif c.startswith("outsource the cut-and-bent"):
            hrec = 2.0
        rows.append(dict(part=p["part"][:80], file=f, kind=kind, material=mat, qty=qty, process=p["process"],
                         in_house_h=round(hrs, 1), in_house_usd=round(in_house), stock_usd=round(stock), outsourced_usd=round(out),
                         cheaper="in house" if in_house < out else "outsourced", call=c, reason=why, note=note,
                         recommended_usd=round(rec), recommended_in_house_h=round(hrec, 1), recommended_basis=rbasis, lead_outsourced=lead, basis_hours=hbasis, basis_stock=sbasis, basis_outsourced=obasis, extra=ebasis))

    def tot(sel, key):
        return round(sum(r[key] for r in rows if sel(r)))
    make = lambda r: r["call"].startswith("make")
    summary = dict(
        rate_usd_h=RATE, jobshop_rate_usd_h=JOBSHOP_RATE, tooling_buy_usd=round(tooling, 2), n_parts=len(rows),
        fit=dict(intercept=round(coef[0], 1), per_hour=round(coef[1], 1), n=len(xs), r2=round(r2, 3)),
        all_in_house=dict(hours=tot(lambda r: True, "in_house_h"), usd=tot(lambda r: True, "in_house_usd") + round(tooling),
                          usd_at_95=round(sum(r["in_house_h"] * RATE_HIGH + r["in_house_usd"] - r["in_house_h"] * RATE for r in rows) + tooling),
                          usd_labour_free=round(sum(r["in_house_usd"] - r["in_house_h"] * RATE for r in rows) + tooling)),
        all_outsourced=dict(usd=tot(lambda r: True, "outsourced_usd")),
        quoted_parts=sum(1 for r in rows if r["basis_outsourced"].startswith("quote")),
        recommended=dict(
            make_hours=tot(make, "in_house_h"), in_house_hours=tot(lambda r: True, "recommended_in_house_h"), make_usd=tot(make, "in_house_usd") + round(tooling),
            outsource_usd=tot(lambda r: not make(r), "recommended_usd"),
            n_make=sum(1 for r in rows if make(r)), n_out=sum(1 for r in rows if not make(r))),
    )
    summary["recommended"]["total_usd"] = summary["recommended"]["make_usd"] + summary["recommended"]["outsource_usd"]
    summary["recommended"]["by_call"] = {c: dict(n=sum(1 for r in rows if r["call"] == c), usd=round(sum(r["recommended_usd"] for r in rows if r["call"] == c)),
                                              hours_in_house=round(sum(r["in_house_h"] for r in rows if r["call"] == c and make(r)), 1))
                                         for c in sorted({r["call"] for r in rows})}
    summary["weeks_in_house_all"] = round(summary["all_in_house"]["hours"] / SHOP_HOURS_PER_WEEK, 1)
    summary["weeks_in_house_recommended"] = round(summary["recommended"]["in_house_hours"] / SHOP_HOURS_PER_WEEK, 1)
    with open(OUT / "should_cost.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (OUT / "should_cost.json").write_text(json.dumps(dict(summary=summary, method=__doc__.split("\n\n")[1], parts=rows), indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
