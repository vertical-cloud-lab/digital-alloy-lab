"""Honest hours per machined part: CAM programming, setups, machine run, deburr and inspection, before and after the chamber
redesign (chamber-construction.md), and what each saving lever is worth.

There is no credible published rule for CAM hours (the search for one found none), so CAM time is a stated estimate:
  CAM = 0.5 h + 0.6 h per setup + 0.015 h per hole (+ 1 h for a lathe-and-mill part, + 8 h for the old block's deep pocket:
        long-tool strategies, rest machining of the R5 corners and coves, holder checks at 120 mm).
Setups: the count from setup_plan.json (3-axis, or with a 4th axis where it swings inside an HRT210 and saves a setup), at
  0.75 h each for parts that fit a vise and 1.25 h for parts over 300 mm (fixture plate, toe clamps, probing); the first rotary
  setup 1.5 h. Modern Machine Shop's survey median is 68-90 min per setup (last good part to first good part).
Run: dfm.py's conservative model (16 cm3/min roughing in 6061, 3 in 316L; 40 / 10 cm2/min finishing; per-hole times) for every
  part, and for the chamber also setup_plan.py's vendor-feed model (Helical / Haas data, 60 % efficiency).
Deburr and inspect: 0.25 h a part, 1 h for a part with a sealing face.
The 'before' column is the 37-part review in machining.md (dfm.json at 2026-11-20 14:00-22:00 UTC, the block chamber body).

Run: /tmp/venv/bin/python desktop-lpbf/analysis/machining/hours.py   (reads dfm.json and setup_plan.json; writes hours.json, hours.csv)
"""
from __future__ import annotations

import csv
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[3] / "desktop-lpbf" / "analysis" / "out" / "machining"
SEAL = ("process_chamber", "chamber_floor", "chamber_lid", "chamber_door", "window_flange", "cover_slide_drawer", "build_module", "bottom_flange",
        "camera_viewport", "metering_base", "overflow_funnel", "recoater_feedthrough_spacer", "recoater_floating_bearing")
LATHE = ("build_plate", "heater_block", "piston_head", "window_flange", "window_retaining", "field_stop", "rod_end", "striker", "bottom_flange",
         "macor", "recoater_floating_bearing", "recoater_motor_standoff", "build_module", "f_theta_adapter", "camera_window_retaining")
# the block chamber body before the redesign (machining.md and its dfm.json): 6 setups, 47 holes, 930 min by the dfm model
OLD_BODY = dict(setups=6, holes=47, run_min=930.0, run_min_vendor=(210, 300), large=True, deep_pocket=True)   # vendor feeds: chamber-construction.md
OLD_TOTAL = dict(parts=37, run_h=63.0)


def cam_h(n_setups, n_holes, lathe=False, deep=False):
    return 0.5 + 0.6 * n_setups + 0.015 * n_holes + (1.0 if lathe else 0.0) + (8.0 if deep else 0.0)


def setup_h(n, large, rotary=False):
    return n * (1.25 if large else 0.75) + (0.75 if rotary else 0.0)


def main():
    dfm = {r["slug"]: r for r in json.loads((OUT / "dfm.json").read_text())["parts"]}
    plan = json.loads((OUT / "setup_plan.json").read_text())
    rows = []
    for slug, p in plan["parts"].items():
        d = dfm.get(slug, {})
        n_holes = len(d.get("holes", []))
        large = max(p["bbox_mm"]) > 300
        lathe = any(k in slug for k in LATHE)
        n3, n4 = p["n3"], p.get("n4_used", p["n3"])
        seal = any(slug.startswith(k) for k in SEAL)
        run = d.get("time_total_min", 0.0) - d.get("time_min", {}).get("setup", 0.0)     # dfm's machine time without its own setup allowance
        if slug.startswith("process_chamber_body"):
            n3, n4 = 6, 3                                  # top, bottom, 4 walls; or top, bottom + one rotary clamping (setup_plan F-S1..F-S3)
            run_v = plan["frame"]["run_minutes_on_mill"]
        elif slug.startswith("chamber_floor_plate"):
            n3 = n4 = 2
            run_v = plan["floor"]["run_minutes_on_mill"]
        else:
            run_v = None
        r = dict(part=p["name"][:90], slug=slug, mat=p["mat"], setups_3axis=n3, setups_4th_axis=n4, holes=n_holes,
                 cam_h=round(cam_h(n3, n_holes, lathe), 1), setup_h_3axis=round(setup_h(n3, large), 1),
                 setup_h_4th=round(setup_h(n4, large, n4 < n3), 1), run_h=round(run / 60.0, 2),
                 run_h_vendor=round(run_v / 60.0, 2) if run_v else None, deburr_inspect_h=1.0 if seal else 0.25,
                 special=p.get("special", ""))
        r["total_h_3axis"] = round(r["cam_h"] + r["setup_h_3axis"] + r["run_h"] + r["deburr_inspect_h"], 1)
        r["total_h_4th"] = round(r["cam_h"] + r["setup_h_4th"] + r["run_h"] + r["deburr_inspect_h"], 1)
        rows.append(r)
    old_body = dict(part="Process chamber body, BEFORE (one 13 x 9.5 x 6 in. block, 120 mm pocket)", setups_3axis=6,
                    cam_h=round(cam_h(6, 47, deep=True), 1), setup_h_3axis=round(setup_h(6, True), 1), run_h=round(OLD_BODY["run_min"] / 60.0, 1),
                    run_h_vendor=[x / 60.0 for x in OLD_BODY["run_min_vendor"]], deburr_inspect_h=1.0)
    old_body["total_h_3axis"] = round(old_body["cam_h"] + old_body["setup_h_3axis"] + old_body["run_h"] + old_body["deburr_inspect_h"], 1)
    fr = [r for r in rows if r["slug"].startswith(("process_chamber_body", "chamber_floor_plate"))]
    new_body = dict(cam_h=sum(r["cam_h"] for r in fr), setup_h=sum(r["setup_h_4th"] for r in fr) + 0.5, run_h=sum(r["run_h"] for r in fr),
                    run_h_vendor=sum(r["run_h_vendor"] or 0 for r in fr) + 0.75, deburr_inspect_h=2.0,
                    note="frame + floor plate; setups include 0.5 h on the waterjet; vendor run time adds 45 min of waterjet")
    new_body["total_h"] = round(new_body["cam_h"] + new_body["setup_h"] + new_body["run_h"] + new_body["deburr_inspect_h"], 1)
    tot = {k: round(sum(r[k] for r in rows), 1) for k in ("cam_h", "setup_h_3axis", "setup_h_4th", "run_h", "deburr_inspect_h", "total_h_3axis", "total_h_4th")}
    tot["parts"] = len(rows)
    tot["setups_3axis"] = sum(r["setups_3axis"] for r in rows)
    tot["setups_4th"] = sum(r["setups_4th_axis"] for r in rows)
    out = dict(method=__doc__.split("\n\n")[1], old_body=old_body, new_body=new_body, totals=tot, parts=rows)
    (OUT / "hours.json").write_text(json.dumps(out, indent=1))
    with open(OUT / "hours.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("old body", old_body)
    print("new body", new_body)
    print("totals", tot)


if __name__ == "__main__":
    main()
