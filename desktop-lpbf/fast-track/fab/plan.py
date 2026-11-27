"""When the fab pieces are done, on a shop calendar, against the dates the study's progression network needs them (#260).

Need dates: cad/ft_progression.py's network, scenario A (stages on PCards, cube ordered on day 0). Each shop task of the
network ("deck plate and target stand made", "window stack and beam tube made", "FT-0 parts made", "FT-1 parts made",
"cube plates machined") is replaced by a fixed finish day; the need date is the latest finish that delays none of the
milestones, with the other shop tasks at the network's own finishes. Days are working days from the order (day 0).

Calendar: hours.py's pieces at the low, expected or high allowances, cut into a CAM task (no stock needed) and a floor
task (setups, machine, deburr and inspection; after its CAM, and after the stock arrives). Greedy list scheduling, 8 h
a working day, for one or two people who both program and cut, pieces taken in the order of the state that needs them.
  stock: McMaster on day 1 (the study's 1-2 days, early end); SendCutSend sheet and plate in hand on day 5 (5-6
         calendar days, PR 266's reads of 2026-11-22, not re-read); the cube's plates MK-13/14 when the cube arrives
         (day 11 in scenario A, early end).
  "plates out" sends FT-1's two flat plates (MK-15a/b) to SendCutSend as well: BYU then draws them (0.5 h on day 0)
         and receives and finishes them (counterbores, taps) after day 5. The S1 and S2 plates that hours.py's split
         also sends out (MK-01, MK-09a, MK-02c/d/e) would arrive on day 5, after S1's need date (day 4) and on S2's
         (day 5), so the calendar keeps them in house.
The sheet pieces (hopper walls, shield) go to SendCutSend in every case. The target plates MK-18b are cut in house
(bandsaw and mill from 1/8 in. plate; the anodising is outside and its lead time was not read).

    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/plan.py [hours.json] [outdir]   -> out/plan.json, out/plan.md
"""
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
import ft_progression as FP  # noqa: E402

OUT = HERE / "out"
DAY = 8.0
STATES = ("S1", "S2", "FT-0", "FT-1", "FT-1V")
SHOP = {"S1": "deck plate and target stand made", "S2": "window stack and beam tube made", "FT-0": "FT-0 parts made",
        "FT-1": "FT-1 parts made", "FT-1V": "cube plates machined"}
SCN = "A: stages on PCards, cube ordered on day 0"
MCMASTER_DAY, SCS_DAY = 1, 5
PLATES = {"MK-15a", "MK-15b"}
IN_HOUSE_SHEET = {"MK-18b"}


def need_dates():
    """Latest finish (working day) of each shop task that delays no milestone, early and late ends."""
    tasks = FP.tasks_for(SCN)
    base = FP.F.forward({k: (v[0], v[1], v[2]) for k, v in tasks.items()})
    ms = {m: base[m] for m in FP.MILESTONES}
    out = {}
    for end in (0, 1):                       # 0: early end of every range, 1: late end
        fixed = {s: base[SHOP[s]][2 + end] for s in STATES}
        for s in STATES:
            best = None
            for x in [i * 0.5 for i in range(0, 161)]:
                t = {k: (v[0], v[1], v[2]) for k, v in tasks.items()}
                for s2 in STATES:
                    if s2 == "FT-1V":
                        continue          # keeps its dependency on the cube's arrival
                    d = x if s2 == s else fixed[s2]
                    t[SHOP[s2]] = ((d, d), [], "fixed")
                if s == "FT-1V":
                    arr = base["cube frame and plates arrive (PO)"][2 + end]
                    if x < arr:
                        continue
                    t[SHOP[s]] = ((x - arr, x - arr), ["cube frame and plates arrive (PO)"], "fixed")
                f = FP.F.forward(t)
                if all(f[m][2 + end] <= ms[m][2 + end] + 1e-9 for m in FP.MILESTONES):
                    best = x
            out.setdefault(s, {})["early" if end == 0 else "late"] = best
            out[s]["network_finish_" + ("early" if end == 0 else "late")] = base[SHOP[s]][2 + end]
    out["_cube_arrives"] = [base["cube frame and plates arrive (PO)"][2], base["cube frame and plates arrive (PO)"][3]]
    out["_milestones_weeks"] = {m: [round(v[2] / 5, 1), round(v[3] / 5, 1)] for m, v in ms.items()}
    return out


def milestones(done_day):
    """The network's milestones (weeks, early end) with the shop tasks finishing on the given working days."""
    tasks = FP.tasks_for(SCN)
    t = {k: (v[0], v[1], v[2]) for k, v in tasks.items()}
    for s in STATES:
        d = done_day[s]
        t[SHOP[s]] = ((d, d), [], "fixed")
    f = FP.F.forward(t)
    return {m: round(f[m][2] / 5, 2) for m in FP.MILESTONES}


def piece_tasks(rows, case, plates_out, cube_day):
    """(pid, state, cam_h, floor_h, floor_ready_h) per piece, for case 'low', 'exp' or 'high'."""
    L = []
    order = {s: i for i, s in enumerate(STATES)}
    for r in sorted(rows, key=lambda r: (order[r["state"]], r["pid"])):
        pid = r["pid"]
        sheet = r["route"].startswith("sheet")
        if r["route"] == "buy":
            continue
        if case == "low":
            cam = 0.5 if sheet else 0.7
            tot = r["low_h"]
        elif case == "exp":
            cam, tot = r["cam_h"], r["total_h"]
        else:
            cam, tot = r["cam_h"], r["high_h"]
        ready = MCMASTER_DAY * DAY
        if sheet and pid not in IN_HOUSE_SHEET:
            ready = SCS_DAY * DAY
        if plates_out and pid in PLATES:
            cam, tot, ready = 0.5, r["byu_h_split"], SCS_DAY * DAY
        if pid in ("MK-13", "MK-14", "MK-21c"):             # machined in the cube's own plates
            ready = cube_day * DAY
        L.append((pid, r["state"], cam, max(tot - cam, 0.0), ready))
    return L


def simulate(tasks, people):
    """Greedy list scheduling: each free person takes the first task (in list order) that is ready."""
    free = [0.0] * people
    cam_done, done, log = {}, {}, []
    todo = [("cam", t) for t in tasks] + [("floor", t) for t in tasks]
    prio = {}
    for i, t in enumerate(tasks):
        prio[("cam", t[0])] = 2 * i
        prio[("floor", t[0])] = 2 * i + 1
    todo.sort(key=lambda k: prio[(k[0], k[1][0])])
    while todo:
        w = min(range(people), key=lambda i: free[i])
        now = free[w]
        best, best_t = None, None
        for kind, t in todo:
            rdy = 0.0 if kind == "cam" else (max(cam_done[t[0]], t[4]) if t[0] in cam_done else None)
            if rdy is None:
                continue
            start = max(now, rdy)
            if best is None or start < best_t - 1e-9 or (abs(start - best_t) < 1e-9 and
                                                          prio[(kind, t[0])] < prio[(best[0], best[1][0])]):
                best, best_t = (kind, t), start
        kind, t = best
        dur = t[2] if kind == "cam" else t[3]
        end = best_t + dur
        free[w] = end
        if kind == "cam":
            cam_done[t[0]] = end
        else:
            done[t[0]] = end
        log.append(dict(who=w, kind=kind, pid=t[0], state=t[1], start=round(best_t, 2), end=round(end, 2)))
        todo.remove(best)
    by_state = {}
    for pid, st, *_ in tasks:
        by_state[st] = max(by_state.get(st, 0.0), done[pid])
    return by_state, log


def main():
    hp = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / "hours.json"
    od = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else OUT
    if not hp.is_absolute():
        hp, od = HERE / hp, (HERE / od if not od.is_absolute() else od)
    rows = json.loads(hp.read_text())["pieces"]
    need = need_dates()
    cube_day = int(need["_cube_arrives"][0])
    base_ms = milestones({s: need[s]["network_finish_early"] for s in STATES})
    res = []
    runs = [(c, n, False) for c in ("low", "exp", "high") for n in (1, 2, 3)] + [("exp", 1, True), ("exp", 2, True)]
    for case, people, plates_out in runs:
        bys, log = simulate(piece_tasks(rows, case, plates_out, cube_day), people)
        fin = {s: round(bys[s] / DAY, 2) for s in STATES}
        late = {s: round(max(0.0, fin[s] - need[s]["early"]), 2) for s in STATES}
        res.append(dict(case=case, people=people, plates_out=plates_out, done_day=fin, late_days=late,
                        milestones_weeks=milestones(fin),
                        log=log if (case, people, plates_out) == ("exp", 2, False) else None))
    (od / "plan.json").write_text(json.dumps(dict(method=__doc__.split("\n\n")[1], need=need,
                                                   network_milestones_weeks=base_ms, runs=res), indent=1))
    names = {"low": "low", "exp": "expected", "high": "high"}
    short = ["S1", "S2", "FT-0", "FT-1", "FT-1V"]
    L = ["| Hours | People | FT-1 plates | Pieces done, working day (need): S1 | S2 | FT-0 | FT-1 | FT-1V | "
         "Milestones, weeks: S1 / S2 / FT-0 tracks / FT-1 coupons / FT-1V coupons |",
         "|---|---:|---|---|---|---|---|---|---|"]
    for r in res:
        cells = []
        for s in STATES:
            d, n = r["done_day"][s], need[s]["early"]
            cells.append(("**%.1f** (%g)" if d > n + 1e-9 else "%.1f (%g)") % (d, n))
        ms = [r["milestones_weeks"][m] for m in FP.MILESTONES]
        msb = [base_ms[m] for m in FP.MILESTONES]
        mtxt = " / ".join(("**%.1f**" if round(a_, 1) > round(b_, 1) else "%.1f") % a_ for a_, b_ in zip(ms, msb))
        L.append("| %s | %d | %s | %s | %s |" % (names[r["case"]], r["people"], "out" if r["plates_out"] else "in house",
                                                  " | ".join(cells), mtxt))
    L.append("| *network as drawn* | | | %s | %s |" % (
        " | ".join("%g" % need[s]["network_finish_early"] for s in STATES),
        " / ".join("%.1f" % base_ms[m] for m in FP.MILESTONES)))
    (od / "plan.md").write_text("\n".join(L) + "\n")
    print("need (early, late):", {s: (need[s]["early"], need[s]["late"]) for s in short}, "cube", need["_cube_arrives"])
    print("\n".join(L))


if __name__ == "__main__":
    main()
