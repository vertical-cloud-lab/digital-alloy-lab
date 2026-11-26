"""Recording hooks for run_assembly.py (ASM_RECORD): turn each step's committed result into record.py events, with the
fetch from the long table and the screw presenter trips (fetch.py) planned in between (round 7, issue #260, PR #266).

The station results (pass/fail, clearances) are computed exactly as before; what this adds is planned and checked on its
own and reported in each row as `fetch` (PASS/FAIL/person/-) and `presenter` (screws whose presenter trip was planned).
"""
from __future__ import annotations

import math
import os

import numpy as np

import record as RECM
import fetch as FE
import mir_route as MR
from cell import Tm, inv  # noqa: F401

# estimated minutes for the steps a person does (or a machine), for the time line; not measured
PERSON_MIN = {"M09": 3.0, "C00": 6.0, "C09e": 3.0, "C15b": 4.0, "F02": 0.0, "F06b": 5.0, "F08": 1.0, "F12": 6.0, "F49": 6.0,
              "F53": 10.0, "F57b": 90.0, "F58": 8.0, "F59": 60.0, "T01": 15.0, "T02": 45.0, "T03": 45.0, "T04": 40.0, "T05": 20.0}
MACHINE_S = {"C11": 3.0, "T06": 1800.0}
STAGED = ("F01", "F54", "C00c")        # two-arm parts: a person stages them at the station on a cart (see dual())


def on():
    return RECM.REC is not None


def chapter_of(sid):
    return "module" if sid.startswith("M") else "chamber"


def begin(run, st):
    if not on():
        return
    R = RECM.REC
    if R.state["A"]["x"] is None:
        for n in ("A", "B"):
            R.set_x(n, run.cl.dock[n])
            R.state[n]["q"] = run.arm(n).park_q()
            R.tool(n, "gripper", tool_spec(run, n))
    R.begin(st, chapter_of(st["id"]))
    run._cur_st = st
    if st.get("bench_person"):
        what, minutes = st["bench_person"]
        R.wait(60.0 * minutes, who="person", what=what)


def end(run, row):
    if not on():
        return
    R = RECM.REC
    st = getattr(run, "_cur_st", None) or {}
    if st.get("inspect"):
        R.wait(30.0, who="person", what="check: " + st["inspect"])
        row["inspect"] = st["inspect"]
    R.end(row)
    R.save_summary(os.environ.get("ASM_SUMMARY", "/tmp/robotbuild/data/assembly.json"))


def note(run, st, row):
    if not on():
        return
    R = RECM.REC
    who = st.get("who", "")
    if st["id"] in MACHINE_S:
        R.wait(MACHINE_S[st["id"]], who="machine", what=st["label"])
    elif "person" in who:
        m = PERSON_MIN.get(st["id"], 5.0)
        R.wait(60.0 * m, who="person", what=st["label"])
        row["person_s"] = 60.0 * m
    elif "robot" in who:
        R.wait(10.0, who="robot", what=st["label"])


def park_if_needed(run, n):
    """If the recorded arm is not parked, plan it to park at its recorded dock (the planner itself teleports there)."""
    R = RECM.REC
    st = R.state[n]
    a = run.arm(n)
    park = a.park_q()
    if st["q"] is None or np.abs(np.asarray(st["q"]) - park).max() < 1e-3:
        st["q"] = park
        return True
    cl = run.cl
    x_pl, q_pl = cl.dock[n], run.q[n].copy()
    cl.move_mir(n, st["x"])
    run.q[n] = np.asarray(st["q"], float)
    a.place(run.q[n], st["close"])
    path, info = run.plan_to(n, park, st["close"])
    R.move(n, path if path is not None else [run.q[n], park], "plan")
    if path is None:
        R.mark("unplanned", arm=n, note="move to park not planned")
    cl.move_mir(n, x_pl)
    run.q[n] = q_pl
    a.place(q_pl)
    return path is not None


def goto(run, n, x, held_world=None):
    """The recorded MiR n drives to dock x (its arm parked first); the drive swept against the cell and the table."""
    R = RECM.REC
    st = R.state[n]
    if st["x"] is None:
        R.set_x(n, x)
        return True, ""
    if abs(st["x"] - x) < 1e-6:
        return True, ""
    park_if_needed(run, n)
    cl = run.cl
    a = run.arm(n)
    x_pl, q_pl = cl.dock[n], run.q[n].copy()
    x0 = st["x"]
    # round 8: pivot, drive along the heading, pivot (mir_route.py), every pose swept against the cell, the long table and the
    # other MiR and arm where the recording has them (not where the planner last left them)
    o = "B" if n == "A" else "A"
    so = R.state[o]
    x_po, q_po = cl.dock[o], run.q[o].copy()
    rt, why_rt = None, ""
    try:
        if so["x"] is not None:
            cl.move_mir(o, so["x"])
        run.arm(o).place(np.asarray(so["q"], float) if so["q"] is not None else run.arm(o).park_q())
        lo, hi = min(x0, x) - MR.SPOT_BACK - 900.0, max(x0, x) + MR.SPOT_FWD + 900.0
        world = cl.world(n)
        for k in list(world.bodies):
            if k.startswith(f"{n} "):          # its own MiR, cabinet, plate, stand and presenter move with it
                world.remove(k)
        if getattr(run, "table", None) is not None:
            for b in run.table.world(lo, hi).bodies.values():
                world.add(b)
        rt = MR.plan(run, n, x0, x, a.park_q(), st["close"], world)
    except Exception as e:  # noqa: BLE001
        why_rt = f"route planner error: {type(e).__name__}: {e}"[:200]
        rt = None
    finally:
        cl.move_mir(o, x_po)
        run.arm(o).place(q_po)
    if rt is not None and rt.get("legs"):
        ok, why = rt["ok"], rt["why"]
    else:
        ok, why = False, (rt or {}).get("why") or why_rt or "no route"
    R.drive(n, x, check=dict(ok=ok, why=why), route=rt if (rt is not None and rt.get("legs")) else None)
    cl.move_mir(n, x_pl)
    run.q[n] = q_pl
    a.place(q_pl)
    return ok, why


def tool_spec(run, n):
    a = run.arm(n)
    return dict(caps=bool(a.caps), cap_spec=(a.cap_spec or {}).get("name") if isinstance(getattr(a, "cap_spec", None), dict) else None)


def place(run, st, idx, actor, tool, best, body, off, G, T_obj, close, state, row):
    """A part placed by arm_place: fetch it from the table, then the planner's approach and insertion."""
    if not on():
        return
    R = RECM.REC
    cl = run.cl
    a = run.arm(actor)
    fr = best["follow"]
    dk = best["dock"]
    fetch_res = "-"
    tbl = getattr(run, "table", None)
    slot = tbl.slot_of(idx) if tbl is not None else None
    x_pl, q_pl = cl.dock[actor], run.q[actor].copy()
    held_pl = a.held
    if slot is not None and st["id"].split(":")[0] in STAGED:
        fetch_res = "person"
    multi = bool(st.get("per_solid") or st.get("per_part"))
    if slot is not None and multi and getattr(run, "_tray_step", None) == st["id"]:
        # the step's later pieces: the arm brought the whole kit tray (or nest) over on its MiR deck with the first one
        fetch_res = "tray"
    if slot is not None and (st.get("moved") or st.get("merge")):
        slot = None                    # a sub-assembly moved from its nest: nothing comes from the table
    if slot is not None and fetch_res == "-":
        G_rel = inv(T_obj) @ G
        # after run 10 (2026-11-26): plan the pick with the part as it lies on the table: only the objects in this slot, and
        # none of the extras fitted at the station. In run 10 M13's held body carried its PEEK rod bullet (a tool fitted at the
        # station) 20 mm into the table top, and C00a's the overflow funnel that a person fits on the bench in C00 (62 mm)
        on_slot = [i for i in idx if tbl.on.get(i) is slot]
        body_t = run.held_body(on_slot, f"held:{st['id']}:table", state, None) if on_slot and hasattr(run, "held_body") else body
        pk = FE.pick_plan(run, actor, on_slot or idx, body_t, off, G_rel, close, tool, slot)
        cl.move_mir(actor, x_pl)
        a.release()
        if held_pl is not None:
            a.hold(*held_pl)
        a.place(q_pl, close)
        if pk["ok"]:
            ok1, why1 = goto(run, actor, pk["x"])
            R.tool(actor, tool, tool_spec(run, actor))
            R.move(actor, pk["to_item"], "plan", close=0.0)
            R.move(actor, pk["in_"], "cart", close=0.0, seat_mm=10.0)
            R.grip(actor, close)
            R.attach(actor, idx, off, state, name=st["id"])
            R.mark("pick", arm=actor, slot=slot["key"])
            R.move(actor, pk["up"], "cart")
            R.move(actor, pk["to_park"], "plan")
            ok2, why2 = goto(run, actor, dk)
            fetch_res = "PASS" if (ok1 and ok2) else "FAIL"
            if multi:
                run._tray_step = st["id"]
            if not (ok1 and ok2):
                row["fetch_why"] = (why1 or why2)[:200]
        else:
            fetch_res = "FAIL"
            row["fetch_why"] = f"pick at the table ({slot['key']}): {pk['why']}"[:200]
        tbl.remove(idx)
    if fetch_res in ("-", "FAIL", "person", "tray"):
        # no table pick recorded: the part appears in the gripper at park (a cut in the video)
        if tbl is not None:
            tbl.remove(idx)
        goto(run, actor, dk)
        R.tool(actor, tool, tool_spec(run, actor))
        R.grip(actor, close)
        R.attach(actor, idx, off, state, name=st["id"])
        if fetch_res == "person":
            R.wait(120.0, who="person", what="stages the part at the station on a cart")
    row["fetch"] = "PASS" if fetch_res == "tray" else fetch_res
    path = best.get("path")
    if path is not None:
        R.move(actor, path, "plan", close=close)
    if fr["qs"]:
        R.move(actor, fr["qs"], "cart", close=close, seat_mm=10.0)


def release(run, n, qs_back, opened=True):
    """retreat(): let go (the gripper opens a little), then back off along the tool axis."""
    if not on():
        return
    R = RECM.REC
    st = R.state[n]
    if st["held"] is not None:
        if run.arm(n).tool_name == "gripper" and opened:
            R.grip(n, max(0.0, st["close"] - 0.12))
        R.detach(n)
    if qs_back:
        R.move(n, qs_back, "cart")


def park(run, n, path):
    if not on():
        return
    R = RECM.REC
    a = run.arm(n)
    if path is not None:
        R.move(n, path, "plan")
    else:
        R.move(n, [run.q[n], a.park_q()], "plan")
        R.mark("unplanned", arm=n, note="move to park not planned")
    R.state[n]["q"] = a.park_q()


def screw(run, i, actor, best, tool, long_bit, tip_d, torque, L, s_hex, row_acc):
    """drive_screw(): presenter trip, the planner's approach, the rundown."""
    if not on():
        return
    R = RECM.REC
    a = run.arm(actor)
    dk = best["dock"]
    if not best.get("ok"):
        if getattr(run, "_hold_trial", False):
            return                     # round 8: a screw the holding pair could not drive is left for the joint's own step
        R.screw(actor, i, None, L, 0.7, torque, tool, False, best.get("why", ""))     # shown as a failed screw, no motion
        return
    goto(run, actor, dk)
    R.tool(actor, tool, dict(extra_bit=float(long_bit or 0.0), tip_d=float(tip_d)))
    st = R.state[actor]
    q_from = np.asarray(st["q"], float) if st["q"] is not None else a.park_q()
    target = best.get("pre_qs", [None])[0] if best.get("pre_qs") else (best["qs"][0] if best.get("qs") else None)
    off = best.get("off")
    pres_ok = False
    if target is not None and best.get("ok"):
        q_pl = run.q[actor].copy()
        held = a.held
        a.release()
        tr = FE.presenter_trip(run, actor, q_from, np.asarray(target, float))
        if held is not None:
            a.hold(*held)
        a.place(q_pl)
        if tr["ok"]:
            pres_ok = True
            R.move(actor, tr["to"], "plan")
            R.move(actor, tr["down"], "cart")
            R.attach(actor, [i], off, {}, name=f"screw {i}")
            R.move(actor, tr["up"], "cart")
            R.move(actor, tr["on"], "plan")
        else:
            row_acc.setdefault("presenter_fail", []).append(tr["why"][:80])
    if not pres_ok:
        R.attach(actor, [i], off, {}, name=f"screw {i}")
        if best.get("path") is not None:
            R.move(actor, best["path"], "plan")
        elif target is not None:
            R.move(actor, [q_from, np.asarray(target, float)], "plan")
            R.mark("unplanned", arm=actor, note="approach to the screw not planned")
    if best.get("pre_qs"):
        R.move(actor, best["pre_qs"], "cart")
    d = float(run.sc.FS.CATALOG[run.sc.objs[i]["pn"]].get("d", 4.0))
    pitch = {3.0: 0.5, 4.0: 0.7, 5.0: 0.8, 6.0: 1.0}.get(round(d), 0.7)
    R.screw(actor, i, best.get("qs"), L, pitch, torque, tool, best.get("ok", False), best.get("why", ""))
    row_acc["presenter_ok"] = row_acc.get("presenter_ok", 0) + int(pres_ok)


def dual(run, st, best, frames, body, idx, gA, gB, cA, cB):
    """Two-arm carry: both arms planned from park to their grasps (the part where it starts, in the world), close, the
    carry frame by frame, then let go (the retreats are recorded by retreat())."""
    if not on():
        return None
    R = RECM.REC
    cl = run.cl
    dA, dB = best["docks"]
    import cell2 as K
    xA, xB = K.DOCKS[dA], K.DOCKS[dB]
    res = {}
    if st.get("lift_aid"):
        R.wait(180.0, who="person", what="rigs the hoist's lifting bar on the part (Edison r7: a rated lifting device over ~10 kg)")
    elif st["id"] in STAGED:
        R.wait(120.0, who="person", what="stages the part at the station on a cart")
    for n, x in (("A", xA), ("B", xB)):
        goto(run, n, x)
        R.tool(n, "gripper", tool_spec(run, n))
    if not best.get("qsA"):
        return dict(approach="no carry")
    # plan each arm from park to its start pose, the part at its start pose as an obstacle (tool contact allowed)
    from cell import Body
    q0 = {"A": best["qsA"][0], "B": best["qsB"][0]}
    ok_all = True
    saved = {n: (cl.dock[n], run.q[n].copy(), run.arm(n).held) for n in ("A", "B")}
    for n in ("A", "B"):
        cl.move_mir(n, {"A": xA, "B": xB}[n])
        run.arm(n).release()
    tmp = Body("carried part (start)", body.v, body.f, kind="machine")
    tmp.place(frames[0])
    cl.static["__carried"] = tmp
    try:
        for n in ("A", "B"):
            o = "B" if n == "A" else "A"
            a = run.arm(n)
            run.arm(o).place(run.arm(o).park_q() if n == "A" else q0["A"], (cA if o == "A" else cB) if n == "B" else 0.0)
            run.q[n] = a.park_q()
            a.place(run.q[n], 0.0)
            path, info = run.plan_to(n, q0[n], 0.0, allow=frozenset([("tool", "carried part (start)")]))
            if path is None:
                ok_all = False
                R.move(n, [a.park_q(), q0[n]], "plan", close=0.0)
                R.mark("unplanned", arm=n, note=f"approach to the carry: {info.get('reason')}")
            else:
                R.move(n, path, "plan", close=0.0)
            R.grip(n, cA if n == "A" else cB)
    finally:
        cl.static.pop("__carried", None)
        for n in ("A", "B"):
            d_, q_, h_ = saved[n]
            cl.move_mir(n, d_)
            run.q[n] = q_
            if h_ is not None:
                run.arm(n).hold(*h_)
    R.attach("A", idx, inv(run.arm("A").tcp(best["qsA"][0], cA)) @ frames[0], {}, name=st["id"])
    QA, QB = np.array(best["qsA"]), np.array(best["qsB"])
    tcpA = np.array([run.arm("A").tcp(q, cA)[:3, 3] for q in QA])
    dur = RECM.joint_time(QA, tcpA, cart=True) * 1.5            # a two-arm carry runs slower: 1.5x (estimate)
    R._ev("move2", arm="A+B", qA=QA.astype(np.float32), qB=QB.astype(np.float32), closeA=cA, closeB=cB, dur=round(dur, 2),
          frames=np.array(frames[:len(QA)], np.float32), lift_aid=bool(st.get("lift_aid")))
    if st.get("lift_aid") and R.step is not None:
        R.step["person_s"] += dur
    R.state["A"]["q"], R.state["B"]["q"] = QA[-1].copy(), QB[-1].copy()
    if R.step is not None:
        R.step["robot_s"]["B"] += dur
    # B lets go first (its own retreat is recorded by retreat()); the part is released by A
    return dict(approach="PASS" if ok_all else "FAIL")


def flip(run, st, actor, fr, body_idx, G_m, close, T0, plan_path):
    """Single-arm turn-over: approach (planned holding the module), close, the turn frames, let go."""
    if not on():
        return
    R = RECM.REC
    dk = run.cl.dock[actor]
    goto(run, actor, dk)
    R.tool(actor, "gripper", tool_spec(run, actor))
    if plan_path is not None:
        R.move(actor, plan_path, "plan", close=0.0)
    R.grip(actor, close)
    off = inv(G_m)
    R.attach(actor, body_idx, off, {}, name=st["id"])
    if fr["qs"]:
        R.move(actor, fr["qs"], "cart", close=close)


def rotate(run, idx, T0, TT, sign):
    if not on():
        return
    RECM.REC.turn(idx, T0, TT, sign)


def roller(run, n, dk, plan_path, qs):
    if not on():
        return
    R = RECM.REC
    goto(run, n, dk)
    R.tool(n, "roller", {})
    if plan_path is not None:
        R.move(n, plan_path, "plan")
    if qs:
        R.move(n, qs, "cart", seat_mm=0.0)
