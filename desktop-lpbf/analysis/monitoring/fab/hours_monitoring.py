"""Shop hours and outside prices for the monitoring hardware's custom parts and features (issue #260, PR 281).

Same rules as analysis/machining/hours.py (CAM 0.5 h + 0.6 h per setup + 0.015 h per hole, +1 h for a lathe-and-mill part;
setups 0.75 h; deburr and inspect 0.25 h, 1 h with a sealing face), applied to:
  * features added to parts that are already made (frame, lid, optics bridge, liners, heater block): no new setup, so only
    the holes' CAM time, a stated allowance for each new non-circular feature (FEATURE_CAM_H, an estimate: hours.py has no
    rule for adding to a proven program), the run time, and the inspection of any new sealing face;
  * the new small parts (clamp rings, adapter boss, nozzle, holders, mounts, waveguide parts).
Run time: the frame's new features from cam_monitoring.json (FreeCAD recount of the posted G-code, or CAMotics' time with
the VF-4 rapids when it has run) plus the operations nobody programs (taps, the SAE-4 port tool) at stated minutes; the
rest are estimates at hours.py's conservative rates (16 cm3/min roughing, 40 cm2/min finishing).
Outside prices are the closest instant quotes already in the repo (outsourcing-quotes.csv, 2026-11-22: SendCutSend's laser
and CNC, JLCCNC) for a part of the same kind and size, labelled "analogue"; none of the monitoring parts has been quoted.
In-house cost uses should_cost.py's $65/h (BYU's shop rate for academic departments).

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/hours_monitoring.py   (writes hours_monitoring.json/.csv)
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "desktop-lpbf" / "analysis" / "machining"))
import hours as H  # noqa: E402  (cam_h, setup_h: the repo's hours rules)

OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "monitoring" / "fab"
RATE = 65.0                  # $/h, should_cost.py RATE (BYU shop, academic departments)
FEATURE_CAM_H = 0.25         # h to program and prove one new non-circular feature in an existing program (ASSUMED)
TAP_MIN = 0.4                # min per tapped M4 hole, incl. approach (ASSUMED; setup_plan.py times taps from Haas charts)
PORT_TOOL_MIN = 1.0          # min for the SAE-4 port tool (spot face, O-ring cone, 7/16-20 thread) (ASSUMED)
TC_MIN = 4.2 / 60            # VF-4 tool to tool (hours.py)

# outside-price analogues (outsourcing-quotes.csv rows, 2026-11-22, qty 1; price shown before any manufacturability review)
ANALOGUE = {
    "scs_ring": (14.01, "SendCutSend laser, 6061 3/8 in.: the recoater feedthrough spacer ring (a flat ring, ~$14; 10 = $8.96 each)"),
    "scs_arm": (27.12, "SendCutSend laser, 6061 1/2 in.: the Z lift arm ($27.12)"),
    "scs_cnc_boss": (379.48, "SendCutSend CNC, 6061: the layer camera's viewport adapter + boss, a compound-angle part ($379.48; 2 = $219.48 each)"),
    "scs_cnc_ring": (257.0, "SendCutSend CNC, 6061: the camera window retaining ring ($257, should_cost.csv)"),
    "osh_liner": (22.85, "OSH Cut, 316 sheet 0.036 in.: a lift-out liner ($22.85)"),
    "jlc_304": (79.18, "JLCCNC, SUS304, ISO 2768-m: the overflow block, a much bigger part ($79.18 without threads; + ~$26 UPS)"),
}


def part(name, where, kind, n_setups=0, holes=0, lathe=False, run_min=0.0, seal=False, extra_cam_h=0.0, deburr_h=None,
         make_call="make", outside=None, outside_note="", buy_instead=None, note="", step="0"):
    """one row: hours by hours.py's rules (new parts) or the add-on rule (features on existing parts)"""
    if kind == "feature":
        cam = 0.015 * holes + extra_cam_h
        setup = 0.0
        deb = deburr_h if deburr_h is not None else (0.25 if seal else 0.0)
    else:
        cam = H.cam_h(n_setups, holes, lathe) + extra_cam_h
        setup = H.setup_h(n_setups, False)
        deb = deburr_h if deburr_h is not None else (1.0 if seal else 0.25)
    run = run_min / 60.0
    tot = cam + setup + run + deb
    o_usd = ANALOGUE[outside][0] if outside in ANALOGUE else outside
    return dict(item=name, step=step, where=where, kind=kind, setups=n_setups, holes=holes, lathe=lathe, seal=seal,
                cam_h=round(cam, 2), setup_h=round(setup, 2), run_h=round(run, 2), deburr_inspect_h=round(deb, 2),
                total_h=round(tot, 2), in_house_usd=round(tot * RATE, 0),
                outside_usd=o_usd, outside_basis=(ANALOGUE[outside][1] if outside in ANALOGUE else outside_note),
                buy_instead=buy_instead, call=make_call, note=note)


def boss_row():
    """the LP adapter boss: the layer camera's boss as hours.csv has it (same kind of part: compound-angle bore and boss,
    window seat on the line of sight, face O-ring on the lid), 4th-axis column"""
    hp = REPO / "desktop-lpbf" / "analysis" / "out" / "machining" / "hours.csv"
    rows = [r for r in csv.DictReader(open(hp)) if r["slug"].startswith("camera_viewport_adapter")]
    r = rows[0]
    out = part("LP adapter boss (compound angle; window seat on the line of sight; face O-ring on the lid), 6061", "new", "part",
               n_setups=int(r["setups_4th_axis"]), holes=int(r["holes"]), seal=True, make_call="outsource (CNC)",
               outside="scs_cnc_boss", step="7",
               note="hours as the layer camera's boss in hours.csv (4th-axis column: a sine plate on the rotary); SendCutSend CNC priced that part")
    out.update(cam_h=float(r["cam_h"]), setup_h=float(r["setup_h_4th"]), run_h=float(r["run_h"]), deburr_inspect_h=float(r["deburr_inspect_h"]))
    out["total_h"] = round(out["cam_h"] + out["setup_h"] + out["run_h"] + out["deburr_inspect_h"], 2)
    out["in_house_usd"] = round(out["total_h"] * RATE, 0)
    return out


def main():
    cm = json.loads((OUT / "cam_monitoring.json").read_text()) if (OUT / "cam_monitoring.json").exists() else {}
    rc = cm.get("recount", {})
    lw_min = rc.get("LW_added_min", 2.46)
    bw_min = rc.get("mon_C180_BW_min", 5.05)
    cs = cm.get("camotics", {}).get("setups", {})
    if cs.get("frame_C90") and cs.get("mon_C180"):
        # CAMotics' cutting time with the VF-4's rapids; the LW share is the new C90 minus the old C90's 0.34 min
        # (analysis/out/machining/camotics/camotics_sim.json, frame_C90 with_vf4_rapids_min)
        lw_min = round(cs["frame_C90"]["time"]["with_vf4_rapids_min"] - 0.34, 2)
        bw_min = cs["mon_C180"]["time"]["with_vf4_rapids_min"]
    lw_extra = 4 * TAP_MIN + PORT_TOOL_MIN + 2 * TC_MIN       # 4 M4 taps, the purge port tool, 2 more tool changes
    bw_extra = 3 * TAP_MIN + 2 * TC_MIN
    rows = [
        # --- features on parts that are made anyway -------------------------------------------------------------------
        part("LW port in the left wall: Ø38.3 x 6.5 window seat, Ø31 bore, 4 x M4, SAE-4 purge port + Ø4 passage",
             "chamber frame, setup C at A90 (programmed, simulated, holder-checked)", "feature", holes=8, run_min=lw_min + lw_extra,
             seal=True, extra_cam_h=FEATURE_CAM_H, note="programmed time %.2f min + %.2f min of taps, port tool and tool changes" % (lw_min, lw_extra),
             step="0"),
        part("BW port in the back wall: 58 x 27 R4 window seat 4.5 deep, 51.2 x 20.5 obround slot, 3 x M4",
             "chamber frame, setup C at A180 (programmed, simulated, holder-checked)", "feature", holes=3, run_min=bw_min + bw_extra,
             seal=True, extra_cam_h=2 * FEATURE_CAM_H,
             note="programmed time %.2f min + %.2f min of taps and tool changes; two non-circular features" % (bw_min, bw_extra), step="0"),
        part("LP port in the lid: Ø37 bore normal to the lid, adapter face O-ring groove, 4 x M4 for the adapter boss",
             "chamber lid, its existing +z setup (not programmed)", "feature", holes=6, run_min=1.0 + 1.3 + 0.4 + 4 * TAP_MIN + 2 * TC_MIN,
             seal=True, extra_cam_h=FEATURE_CAM_H,
             note="estimates: bore 1.0 min (as the LW bore), groove 1.3 min (scaled from the lid gland's 35 min), 4 holes", step="0"),
        part("Optics-bridge cut-out for the LP camera (obround ~74 x 45 through 25 mm)", "optics bridge, its existing +z setup",
             "feature", holes=0, run_min=4.7 + 1.5, extra_cam_h=FEATURE_CAM_H, deburr_h=0.1,
             note="75 cm3 at 16 cm3/min + 60 cm2 of wall at 40 cm2/min; re-run the bridge FEA (case 6b, 128 Hz) before cutting", step="0"),
        part("Liner openings: Ø27 hole in the left liner; the lower back liner's left piece starts at x -90.8 (was -130.5)",
             "lift-out liners (sheet, outsourced anyway)", "feature", holes=0, run_min=0.0, deburr_h=0.0, make_call="outsource (with the liners)",
             outside=0.0, outside_note="a change to the DXF of a part already outsourced (OSH Cut / SendCutSend): about $0", step="0"),
        part("AE waveguide hole Ø2.5 through the heater block and piston head (only for the waveguide option)",
             "heater block, piston head: existing setups", "feature", holes=2, run_min=1.0, deburr_h=0.0, step="4"),
        # --- new parts ------------------------------------------------------------------------------------------------
        part("LW window clamp ring, 6061, Ø56 x 6.35, ID 31, 4 x Ø4.5 on Ø48", "new", "part", n_setups=2, holes=4, lathe=True,
             run_min=8.0, make_call="outsource (laser-cut plate)", outside="scs_ring",
             note="a flat ring: cut from 1/4 in. plate it needs no lathe; the plate's own face bottoms on the wall", step="0"),
        part("LW blanking disc in place of the window until the camera is bought (Ø38.1 x 5, 6061)", "new", "part", n_setups=1, lathe=True,
             run_min=5.0, make_call="buy instead", buy_instead="fit the Ø38.1 x 5 window from the start: it costs about what the blank does",
             step="0"),
        part("LW purge nozzle inside the chamber", "new", "part", n_setups=2, holes=1, lathe=True, run_min=8.0,
             make_call="buy instead", buy_instead="1/8 in. 316 tube through a bored-through SAE-4 x 1/8 in. tube fitting, bent and flattened at the tip (estimate $40-70)",
             outside="jlc_304", step="0"),
        part("LW cover-slide holder (Ø30 x 1 slide) on the left liner", "new", "part", n_setups=1, holes=2, run_min=3.0,
             make_call="outsource (sheet clip with the liner)", outside="osh_liner", step="0"),
        part("LW camera bracket (flat 6061 plate under a ball head or tilt mount; the camera's line is set by the head)", "new", "part",
             n_setups=1, holes=6, run_min=10.0, make_call="outsource (laser-cut plate)", outside="scs_arm", step="7"),
        part("BW window clamp frame, 6061 3/16 in., ~76 x 46 with a 53 x 22 opening, 3 x Ø4.5", "new", "part", n_setups=1, holes=3,
             run_min=8.0, make_call="outsource (laser-cut plate)", outside="scs_ring", step="0"),
        boss_row(),
        part("LP window retaining ring", "new", "part", n_setups=2, holes=1, lathe=True, run_min=2.0, make_call="buy instead",
             buy_instead="Thorlabs SM1 retaining ring or a laser-cut ring (should_cost.py: estimate $10)", outside="scs_cnc_ring", step="7"),
        part("LP cover-slide holder", "new", "part", n_setups=1, holes=2, run_min=3.0, make_call="outsource (sheet clip)",
             outside="osh_liner", step="7"),
        part("AE sensor clamp on the rod end (spring-loaded, 6061)", "new", "part", n_setups=2, holes=4, run_min=10.0,
             make_call="outsource (laser-cut plate) + bought spring", outside="scs_arm", step="4"),
        part("AE waveguide: Ø2 mm 316 rod, tip faced and polished; spring-loaded cool-end holder (PEEK or 6061)", "new", "part",
             n_setups=2, holes=1, lathe=True, run_min=12.0, make_call="make", outside="jlc_304",
             note="only if the bench test picks the waveguide (monitoring.md §5.4)", step="4"),
        part("Coaxial camera adapter plate (IMX296 board on a 30 mm cage plate)", "new", "part", n_setups=1, holes=6, run_min=4.0,
             make_call="outsource (laser-cut plate) or print", outside=10.0, outside_note="estimate: SendCutSend laser, 1/8 in. 6061 (smallest parts were $3.55-14)",
             step="6"),
        part("Sync breakout box (bought enclosure, 6-8 BNC bulkheads drilled)", "new", "part", n_setups=1, holes=8, run_min=10.0,
             make_call="make (hand-drilled)", step="1"),
    ]
    tot = lambda rs, k: round(sum(r[k] or 0 for r in rs), 2)  # noqa: E731
    feats = [r for r in rows if r["kind"] == "feature"]
    news = [r for r in rows if r["kind"] == "part"]
    made = [r for r in rows if r["call"].startswith("make")]
    out_rows = [r for r in rows if r["call"].startswith("outsource")]
    buy_rows = [r for r in rows if r["call"].startswith("buy")]
    summary = dict(
        rate_usd_h=RATE,
        features_on_existing_parts=dict(total_h=tot(feats, "total_h"), in_house_usd=tot(feats, "in_house_usd")),
        new_parts_all_made_in_house=dict(total_h=tot(news, "total_h"), in_house_usd=tot(news, "in_house_usd"), n=len(news)),
        recommended=dict(
            in_house_h=round(tot(made, "total_h") + tot([r for r in feats if not r["call"].startswith("make")], "total_h"), 2),
            outsourced_usd=round(sum((r["outside_usd"] or 0) for r in out_rows), 2),
            outsourced_items=len(out_rows), bought_instead=len(buy_rows),
            note="features on the frame, lid, bridge and heater block stay in house (they ride on setups the shop runs anyway); "
                 "flat parts go to a laser service, the compound-angle boss to SendCutSend CNC, rings and the nozzle are bought"),
        frame_programmed_run_min=dict(before=65.1, added_LW=round(lw_min, 2), added_BW=round(bw_min, 2),
                                      after=round(65.1 + lw_min + bw_min, 1),
                                      note="machining.md round 6: 65.1 min (63.1 cutting + tool changes + A indexes); taps not programmed"),
        machine_totals_h=dict(before_4th_axis=287.3, before_3axis=302.3,
                              note="machining.md phase 2 (57 parts); the monitoring adds the rows here"))
    res = dict(method=__doc__.split("\n\n")[1], summary=summary, rows=rows)
    (OUT / "hours_monitoring.json").write_text(json.dumps(res, indent=1))
    with open(OUT / "hours_monitoring.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(json.dumps(summary, indent=1))
    for r in rows:
        print(f"{r['total_h']:5.2f} h ${r['in_house_usd']:5.0f} | {r['call']:34s} | {r['outside_usd']} | {r['item'][:80]}")


if __name__ == "__main__":
    main()
