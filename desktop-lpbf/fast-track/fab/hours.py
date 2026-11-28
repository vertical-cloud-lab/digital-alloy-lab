"""Shop hours per piece, per state and for an outsourced split (#260, PR 294 round 2).

Per piece: CAM programming + setups + machine time + deburr/inspect, with PR 266's allowances
(desktop-lpbf/analysis/machining/hours.py, quoted in tools.ALLOW):
  CAM     0.5 h + 0.6 h per mill setup + 0.015 h per hole, +1 h if it is also turned; a lathe-only piece 0.25 h
          (a sketch for the lathe hand); sheet parts 0.5 h (flat pattern and drawing for the vendor)
  setups  0.75 h per mill setup in a vise; 1.25 h if the blank is over 200 mm (PR 266 used 300 mm: the 260 mm deck
          and the 275 mm head plate do not go in a vise either); 0.5 h per lathe setup (estimate); a batch shares
          its setups
  machine mill: the posted programs' recount (cam.json: feeds as programmed, rapids at 25.4 m/min) + 4.2 s per tool
          change + 12 s per rigid-tapped hole (estimate) + 10 min of boring head on the 40 H7 bore (estimate);
          lathe: parts.py's feed-and-length estimates; manual steps as listed per piece (estimates)
  deburr  0.25 h a piece (+0.05 h for each extra in a batch), 1 h for a piece with a sealing face
The low bound uses robot-shop.md's smaller allowances (0.7 h of CAM a piece, 20 min a setup), as PR 266 did; 0.7 h a
piece is also about what reviewing and proving out this folder's programs would take at 0.25 h a mill setup.
The high bound keeps the expected CAM and deburr and takes: setups at 1.5 h (the top of the 68-90 min median of
Modern Machine Shop's survey that PR 266's hours.py cites), 2.0 h on a blank over 200 mm, 1.0 h a lathe setup;
FreeCAD's own cycle time in place of the recount; lathe and hand steps x 1.5; and the three tight-fit pieces (MK-03's
H7 bore, MK-07's rod gland, MK-02a's window seat) made twice (setups, machine and inspection again, CAM reused).

    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/hours.py   -> out/hours.csv, out/hours.json, out/hours.md
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tools as T  # noqa: E402

OUT = HERE / "out"
STATES = ("S1", "S2", "FT-0", "FT-1", "FT-1V")
STUDY = {"FT-0": (10, 15), "FT-1": (25, 40), "FT-1V": (30, 48)}       # fast_track.py / parts.csv F2a-c
A = T.ALLOW
HIGH = dict(setup_vise=1.5, setup_large=2.0, setup_lathe=1.0, est_factor=1.5)
REMAKE = {"MK-03", "MK-07", "MK-02a"}      # tightest fits: made twice in the high case
LATHE_SETUPS = {"MK-03s": 2, "MK-04": 2, "MK-05": 2, "MK-06a": 2, "MK-06b": 2, "MK-07": 1, "MK-10a": 2, "MK-10b": 2,
                "MK-02f": 2, "MK-20a": 2, "MK-20c": 2}
# outsourced split: sheet parts and flat plates go out; turned, sealing and precision pieces stay in
OUT_SHEET = {"MK-08a", "MK-08b", "MK-12", "MK-18b", "MK-17b"}
OUT_PLATE = {"MK-01", "MK-09a", "MK-09d", "MK-09f", "MK-15a", "MK-15b", "MK-02c", "MK-02d", "MK-02e"}
# what BYU still does on an outsourced plate: (setups, minutes of machine time) for c'bores, c'sinks and taps
PLATE_SECONDARY = {"MK-01": "4 c'bores and 15 taps by hand after SendCutSend cuts the profile and drills",
                   "MK-09a": "4 c'bores, 6 c'sinks, 8 taps (one setup and hand taps)",
                   "MK-09d": "12 c'bores (one setup)", "MK-09f": "4 c'bores, 4 taps (one setup)", "MK-15a": "4 c'bores", "MK-15b": "8 taps by hand (both faces)",
                   "MK-02c": "11 taps by hand", "MK-02d": "slide pocket 1.2 deep (one mill setup)", "MK-02e": "none"}


# round 3: a "reviewed" case, the CAM review's sensitivity (review-r3.md section 4) per piece. It takes the programs
# as written, fixed and proven out, and a machinist on the floor:
#   setups   a piece's first mill setup 0.75 h (1.25 h over 200 mm), its further setups 0.25-0.5 h, 0.5 h a lathe setup
#   CAM      0.25 h a mill setup to review and prove out; 0.25 h a lathe-only piece
#   machine  the set's mill time x 1.08-1.16 (acceleration, tool changes, spindle starts: the review's recount)
#   lathe and hand work: the set's estimates x 1.5-3; deburr and inspection, sheet and bought parts as the set
#   extras   fixtures 4-8 h, loading the tools 1-2.5 h, sawing blanks 2-4 h, CAM fixes 3-6 h: 10-20 h on v1's 57 mill
#            setups to FT-1, so 10/57-20/57 h a mill setup here (scaled with the setups; round 3 made some of the CAM
#            fixes, the rest are kept in: ramp entries into pockets and profiles, setup sheets, a Haas post, prove-out)
#   student  a student doing half the setups, lathe and hand work and deburring at 1.7-2.0 x a machinist's time
# Low and high here are the two ends of each range above. It reproduces the review's v1 figures: 76.8-97.7 h
# (machinist) and 92.3-125.0 h (with a student) to FT-1. An estimate, like the allowances: no piece has been timed.
REVIEWED = dict(first_setup=0.75, first_setup_large=1.25, next_setup=(0.25, 0.5), lathe_setup=0.5,
                cam_per_mill_setup=0.25, cam_lathe_only=0.25, mill_factor=(1.08, 1.16), est_factor=(1.5, 3.0),
                extras_per_mill_setup=(10.0 / 57, 20.0 / 57), student_share=0.5, student_extra=(0.7, 1.0))


def reviewed_hours(r):
    """the reviewed case for one hours row: machinist (low, high), machinist and student (low, high), and its parts"""
    R = REVIEWED
    if r["route"] == "buy" or r["route"].startswith("sheet"):
        t = r["total_h"]
        return dict(mach=(t, t), stu=(t, t), setups=(0.0, 0.0), cam=0.0, extras=(0.0, 0.0))
    n_mill, n_lathe = r["mill_setups"], r["lathe_setups"]
    first = (R["first_setup_large"] if r["large"] else R["first_setup"]) if n_mill else 0.0
    su = [first + max(0, n_mill - 1) * ns + n_lathe * R["lathe_setup"] for ns in R["next_setup"]]
    cam = R["cam_per_mill_setup"] * n_mill if n_mill else (R["cam_lathe_only"] if n_lathe else 0.0)
    mill = [r["machine_min"] / 60 * f for f in R["mill_factor"]]
    lh = [(r["lathe_min"] + r["manual_min"]) / 60 * f for f in R["est_factor"]]
    deb = r["deburr_h"]
    ex = [n_mill * e for e in R["extras_per_mill_setup"]]
    mach = [su[i] + cam + mill[i] + lh[i] + deb + ex[i] for i in (0, 1)]
    stu = [mach[i] + R["student_share"] * (su[i] + lh[i] + deb) * R["student_extra"][i] for i in (0, 1)]
    return dict(mach=tuple(mach), stu=tuple(stu), setups=tuple(su), cam=cam, extras=tuple(ex))


def piece_hours(p, cam_setups):
    pid = p["pid"]
    qty = p["qty"]
    route = p["route"]
    n_mill = len(p["setups"])
    holes = p["n_holes"]
    taps = sum(h["n"] for h in p["holes"] if h["kind"] == "tap")
    lathe_min = sum(m for _, m in p["lathe"]) * (qty if pid not in ("MK-05",) else qty)
    if pid == "MK-05":
        lathe_min = sum(m for _, m in p["lathe"]) * qty
    manual_min = sum(m for _, m in p["manual"])
    n_lathe = LATHE_SETUPS.get(pid, 0)
    sheet = route.startswith("sheet")
    buy = route == "buy"
    bb = p["blank"]["box"] if p.get("blank") and p["blank"]["type"] == "box" else None
    large = bb is not None and max(bb[1] - bb[0], bb[3] - bb[2]) > 200.0
    prog_min = sum(s["total_min"] * s.get("repeat", 1) for s in cam_setups)       # repeat: an indexed feature
    tool_changes = sum(s["tool_changes"] * s.get("repeat", 1) for s in cam_setups)
    fc_min = sum(s["freecad_cycle_min"] * s.get("repeat", 1) for s in cam_setups)
    mill_min = prog_min + tool_changes * A["tool_change_s"] / 60 + taps * A["tap_s_per_hole"] / 60
    if pid == "MK-03":
        mill_min += A["bore_head_min"]
    mill_min_total = mill_min * qty
    if buy:
        cam = setups = run = 0.0
        deb = 0.1
    elif sheet:
        cam, setups, run = 0.5, 0.0, manual_min / 60.0
        deb = 0.25
    else:
        cam = (A["cam_base"] + A["cam_per_setup"] * n_mill + A["cam_per_hole"] * holes +
               (A["cam_lathe"] if n_mill and n_lathe else 0.0)) if n_mill else (0.25 if n_lathe else 0.0)
        setups = n_mill * (A["setup_large"] if large else A["setup_vise"]) + n_lathe * 0.5
        run = (mill_min_total + lathe_min + manual_min) / 60.0
        deb = (A["deburr_seal"] if p["seal"] else A["deburr"]) + 0.05 * (qty - 1)
    total = cam + setups + run + deb
    # high: longer setups, FreeCAD's cycle time, estimates x 1.5, the tight-fit pieces made twice
    fc_mill_min = (fc_min + tool_changes * A["tool_change_s"] / 60 + taps * A["tap_s_per_hole"] / 60 +
                   (A["bore_head_min"] if pid == "MK-03" else 0.0)) * qty
    if buy:
        high = deb
    elif sheet:
        high = cam + manual_min * HIGH["est_factor"] / 60.0 + deb
    else:
        su_hi = n_mill * (HIGH["setup_large"] if large else HIGH["setup_vise"]) + n_lathe * HIGH["setup_lathe"]
        run_hi = (fc_mill_min + (lathe_min + manual_min) * HIGH["est_factor"]) / 60.0
        high = cam + (su_hi + run_hi + deb) * (2 if pid in REMAKE else 1)
    low = 0.0
    if not buy:
        low = (0.5 if sheet else A["low_cam_per_part"] if (n_mill or n_lathe) else 0.0) + \
              (n_mill + n_lathe) * A["low_setup"] + run + deb
    # outsourced split
    if pid in OUT_SHEET:
        byu_out, how = 0.5 + 0.25 + manual_min / 60.0, "SendCutSend: laser-cut and bent"
    elif pid in OUT_PLATE:
        sec = PLATE_SECONDARY[pid]
        n_sec = 0 if sec == "none" else 1
        byu_out = 0.5 + 0.25 + n_sec * A["setup_vise"] + taps * A["hand_tap_s_per_hole"] / 60 / 60
        how = "SendCutSend (plate: profile and holes; 6061 up to 1/2 in.); BYU: " + sec
    else:
        byu_out, how = total, "in house"
    return dict(pid=pid, mk=p["mk"], name=p["name"], state=p["state"], qty=qty, route=route, stock=p["stock"],
                stock_pn=p["stock_pn"], mill_setups=n_mill, lathe_setups=n_lathe, holes=holes, tapped=taps,
                cam_h=round(cam, 2), setup_h=round(setups, 2), program_min=round(prog_min * qty, 1),
                freecad_min=round(fc_min * qty, 1), machine_min=round(mill_min_total, 1), lathe_min=round(lathe_min, 1),
                manual_min=round(manual_min, 1), run_h=round(run, 2), deburr_h=round(deb, 2), total_h=round(total, 2),
                low_h=round(low, 2), high_h=round(high, 2), split=how, byu_h_split=round(byu_out, 2), seal=p["seal"], large=large)


def main():
    spec = json.loads((pathlib.Path("/tmp/ft-fab") / "pieces.json").read_text())
    cam = json.loads((OUT / "cam.json").read_text())
    by = {}
    for s in cam["setups"]:
        by.setdefault(s["pid"], []).append(s)
    rows = [piece_hours(p, by.get(p["pid"], [])) for p in spec["pieces"]]
    # per state (the state that first needs each piece) and cumulative (the machine)
    st = {s: dict(h=0.0, low=0.0, high=0.0, split=0.0, prog=0.0, cam=0.0, n=0) for s in STATES}
    for r in rows:
        d = st[r["state"]]
        d["h"] += r["total_h"]
        d["low"] += r["low_h"]
        d["high"] += r["high_h"]
        d["cam"] += r["cam_h"]
        d["split"] += r["byu_h_split"]
        d["prog"] += r["program_min"]
        d["n"] += 1
    cum, c = {}, dict(h=0.0, low=0.0, high=0.0, split=0.0, cam=0.0)
    for s in STATES:
        for k in c:
            c[k] += st[s][k]
        cum[s] = dict(c)
    with open(OUT / "hours.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # round 3: the reviewed case (machinist; machinist and student), per state and cumulative
    rv_st = {s: dict(machinist_low=0.0, machinist_high=0.0, student_low=0.0, student_high=0.0, mill_setups=0,
                     lathe_setups=0) for s in STATES}
    rv_pc = {}
    for r in rows:
        q = reviewed_hours(r)
        d = rv_st[r["state"]]
        d["machinist_low"] += q["mach"][0]
        d["machinist_high"] += q["mach"][1]
        d["student_low"] += q["stu"][0]
        d["student_high"] += q["stu"][1]
        d["mill_setups"] += r["mill_setups"]
        d["lathe_setups"] += r["lathe_setups"]
        rv_pc[r["pid"]] = dict(machinist=[round(v, 2) for v in q["mach"]], student=[round(v, 2) for v in q["stu"]])
    rv_cum, c2 = {}, {k: 0.0 for k in rv_st["S1"]}
    for s in STATES:
        for k in c2:
            c2[k] += rv_st[s][k]
        rv_cum[s] = dict(c2)
    reviewed = dict(basis="round 3: review-r3.md section 4's sensitivity per piece (hours.py REVIEWED); an estimate",
                    allowances=REVIEWED, by_state={s: {k: round(v, 2) for k, v in rv_st[s].items()} for s in STATES},
                    cumulative={s: {k: round(v, 2) for k, v in rv_cum[s].items()} for s in STATES}, pieces=rv_pc)
    out = dict(method=__doc__.split("\n\n")[1], rate_usd_h=T.RATE_USD_H, pieces=rows,
               by_state={s: {k: round(v, 2) for k, v in st[s].items()} for s in STATES},
               cumulative={s: {k: round(v, 2) for k, v in cum[s].items()} for s in STATES}, study=STUDY,
               high_allowances=dict(HIGH, remake=sorted(REMAKE)), reviewed=reviewed)
    (OUT / "hours.json").write_text(json.dumps(out, indent=1))
    # markdown
    L = ["| Piece | What | State | Qty | Route | Mill / lathe setups | Holes (tapped) | Program min | CAM h | Setups h "
         "| Machine h | Deburr h | Low h | **Expected h** | High h |",
         "|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        L.append("| %s | %s | %s | %d | %s | %d / %d | %d (%d) | %.1f | %.2f | %.2f | %.2f | %.2f | %.1f | **%.1f** | %.1f |" % (
            r["pid"], r["name"], r["state"], r["qty"], r["route"], r["mill_setups"], r["lathe_setups"], r["holes"],
            r["tapped"], r["program_min"], r["cam_h"], r["setup_h"], r["run_h"], r["deburr_h"], r["low_h"],
            r["total_h"], r["high_h"]))
    L += ["", "| State | Pieces | Low / expected / high h | Cumulative low / expected / high h | Study "
          "| Cumulative at $%d/h, low / expected / high | Outsourced split, BYU h (cumulative) |" % T.RATE_USD_H,
          "|---|---:|---|---|---|---|---:|"]
    for s in STATES:
        stu = STUDY.get(s)
        L.append("| %s | %d | %.1f / %.1f / %.1f | %.1f / **%.1f** / %.1f | %s | $%s / %s / %s | %.1f (%.1f) |" % (
            s, st[s]["n"], st[s]["low"], st[s]["h"], st[s]["high"], cum[s]["low"], cum[s]["h"], cum[s]["high"],
            ("%d-%d h" % stu) if stu else "-",
            *[format(int(round(cum[s][k_] * T.RATE_USD_H, -1)), ",") for k_ in ("low", "h", "high")],
            st[s]["split"], cum[s]["split"]))
    L += ["", "Round 3, the reviewed case (review-r3.md section 4 per piece; programs fixed and proven out):", "",
          "| State | Mill / lathe setups (cumulative) | Machinist, cumulative h | Machinist and student, cumulative h "
          "| The set's low / expected / high, cumulative h |", "|---|---|---|---|---|"]
    for s in STATES:
        a = rv_cum[s]
        L.append("| %s | %d / %d | %.1f-%.1f | %.1f-%.1f | %.1f / %.1f / %.1f |" % (
            s, a["mill_setups"], a["lathe_setups"], a["machinist_low"], a["machinist_high"], a["student_low"],
            a["student_high"], cum[s]["low"], cum[s]["h"], cum[s]["high"]))
    (OUT / "hours.md").write_text("\n".join(L) + "\n")
    for s in STATES:
        print("%-6s n %2d  %.1f h (low %.1f, high %.1f)  cumulative %.1f h (low %.1f, high %.1f) = $%.0f   split %.1f "
              "(cum %.1f)" % (s, st[s]["n"], st[s]["h"], st[s]["low"], st[s]["high"], cum[s]["h"], cum[s]["low"],
                              cum[s]["high"], cum[s]["h"] * T.RATE_USD_H, st[s]["split"], cum[s]["split"]))
    for s in STATES:
        a = rv_cum[s]
        print("%-6s reviewed (cumulative): machinist %.1f-%.1f h, with a student %.1f-%.1f h (%d mill setups)" % (
            s, a["machinist_low"], a["machinist_high"], a["student_low"], a["student_high"], a["mill_setups"]))


if __name__ == "__main__":
    main()
