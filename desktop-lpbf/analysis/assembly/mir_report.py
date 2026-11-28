"""The MiRs' recorded base moves, as a differential-drive MiR250 makes them (round 8, issue #260, PR #266): reversing distance,
pivots, and the swept-footprint check of every leg (mir_route.py), from a run's recording (run_assembly.py with ASM_RECORD).

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/mir_report.py /tmp/robotbuild/traj/run13 [run 13 (round 9)]
Writes analysis/out/assembly/mir_drives.json.
"""
from __future__ import annotations

import json
import pathlib
import pickle
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "assembly"
sys.path.insert(0, str(HERE))


def events(d, chapter):
    f = d / f"asm_{chapter}.pkl"
    if f.exists():
        return pickle.load(open(f, "rb"))["events"]
    ev = []
    for c in sorted(d.glob(f"asm_{chapter}.chunk*.pkl")):
        ev += pickle.load(open(c, "rb"))["events"]
    return ev


def main(rec_dir, label="run 13 (round 9)"):
    import mir_route as MR
    d = pathlib.Path(rec_dir)
    drives = []
    for ch in ("module", "chamber"):
        for e in events(d, ch):
            if e["kind"] != "drive":
                continue
            rt = e.get("route") or {}
            legs = rt.get("legs") or []
            rev_legs = [abs(lg["x1"] - lg["x0"]) for lg in legs if lg["kind"] == "line" and lg.get("rev")]
            drives.append(dict(chapter=ch, step=e["step"], arm=e["arm"], x0=round(e["x0"], 1), x1=round(e["x1"], 1),
                               held=e.get("held"), ok=bool((e.get("check") or {}).get("ok", False)),
                               why=(e.get("check") or {}).get("why", ""), dur_s=e["dur"], route=bool(legs),
                               dist_mm=rt.get("dist_mm"), pivots=rt.get("n_pivots", 0), pivot_deg=rt.get("pivot_deg", 0.0),
                               reverse_mm=round(sum(rev_legs), 1), longest_reverse_mm=round(max(rev_legs), 1) if rev_legs else 0.0,
                               pivot_s=round(sum(lg["dur"] for lg in legs if lg["kind"] == "pivot"), 2),
                               turn_spots=[round(lg["x"]) for lg in legs if lg["kind"] == "pivot"][::2],
                               slide_reverse_mm=round(max(0.0, e["x0"] - e["x1"]), 1)))
    n = len(drives)
    fails = [x for x in drives if not x["ok"]]
    out = dict(
        note=f"Every recorded MiR base move of {label}: pivot, drive along the heading, pivot (mir_route.py). Each MiR docks "
             "heading +x; a move toward +x is one forward drive; a move toward -x of at most 0.5 m is a straight reverse (the "
             "docking leg); a longer one turns round at a clear spot (pivot 90 deg away from the bench, 130 mm out, pivot 90 deg), "
             "drives back along the return lane and turns in at a clear spot at or behind the dock. Every pose of every leg "
             "(pivots every 2 deg, straight legs every 20 mm) was checked with FCL for the MiR body, cabinet, mounting plate, tool "
             "stand, screw presenter and the parked arm with its tool and anything it held, against the bench, fixtures and "
             "nests, the trunnion, the machine parts in the cell, the other MiR and its arm where the recording has them, and "
             "the long table's top, legs, stretchers (round 9: a cross rail at each leg pair), nests, trays and the items still on "
             "it (round 9: a hose or line as the box of its coil, as it is drawn).",
        speeds=dict(drive="trapezoid 0.3 m/s^2, 1.0 m/s (MiR250 datasheet, as record.py)",
                    pivot=f"{MR.PIV_RATE:.0f} deg/s with {MR.T_PIV_RAMP} s to start and stop: an ESTIMATE (no published MiR250 pivot rate was found)",
                    dock="6 s to dock at a marker: estimate (record.py)"),
        footprint=dict(mir_mm="800 x 580 (+ the tool stand and screw presenter on the cabinet's far face: swept radius 588 mm)",
                       parked_arm="UR12e in park (cell2.ArmT.park_q), its tool and any held part: swept radius 475 mm from the MiR's centre",
                       lane_out_mm=MR.LANE_OUT, spot_step_mm=MR.SPOT_STEP, pivot_step_deg=MR.PIV_STEP, line_step_mm=MR.LINE_STEP),
        drives=n, with_route=sum(1 for x in drives if x["route"]), clear=n - len(fails),
        not_clear=[dict(step=x["step"], arm=x["arm"], why=x["why"]) for x in fails],
        reverse_total_mm=round(sum(x["reverse_mm"] for x in drives), 1),
        reverse_longest_leg_mm=max([x["longest_reverse_mm"] for x in drives] or [0.0]),
        reverse_legs=sum(1 for x in drives if x["reverse_mm"] > 0),
        round7_style_reverse_mm=round(sum(x["slide_reverse_mm"] for x in drives), 1),
        pivots=sum(x["pivots"] for x in drives), pivot_time_s=round(sum(x["pivot_s"] for x in drives), 1),
        drive_time_s=round(sum(x["dur_s"] for x in drives), 1),
        distance_m=round(sum(x["dist_mm"] or 0.0 for x in drives) / 1000.0, 1),
        round7_style_distance_m=round(sum(abs(x["x1"] - x["x0"]) for x in drives) / 1000.0, 1),
        turn_spots_used=sorted({s for x in drives for s in x["turn_spots"]}),
        list=drives)
    (OUT / "mir_drives.json").write_text(json.dumps(out, indent=1))
    print({k: out[k] for k in ("drives", "with_route", "clear", "reverse_total_mm", "reverse_longest_leg_mm", "reverse_legs",
                               "round7_style_reverse_mm", "pivots", "pivot_time_s", "distance_m", "round7_style_distance_m")})
    print("not clear:", out["not_clear"][:6])
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/robotbuild/traj/run13", *(sys.argv[2:3]))
