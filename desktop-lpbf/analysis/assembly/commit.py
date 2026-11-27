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
        bench = [i for i in idx if tbl.on.get(i) is not None and tbl.on.get(i) is not slot
                 and tbl.on[i].get("step") in tbl.KT.NOTE_KEYS]          # fitted in a person's bench step (kit_table.NOTE_KEYS)
        if bench:
            # round 9 (for run 15): the part carries pieces a person fitted on the bench in an earlier step (C00a's floor plate
            # with the overflow funnel, C00). Picking it from the table drew those pieces, which lie in their own slot, under it
            # and through the table top (round 9's frame audit, chapter 41 frames 277-280): it comes from the bench, staged
            fetch_res = "person"
        body_t = run.held_body(on_slot, f"held:{st['id']}:table", state, None) if on_slot and hasattr(run, "held_body") else body
        pk = FE.pick_plan(run, actor, on_slot or idx, body_t, off, G_rel, close, tool, slot) if not bench else \
            dict(ok=False, why="from the bench, staged by a person")
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
        elif bench:
            fetch_res = "person"
            row["fetch_why"] = "from the bench with the pieces fitted there (staged by a person), not from the table"
        else:
            fetch_res = "FAIL"
            row["fetch_why"] = f"pick at the table ({slot['key']}): {pk['why']}"[:200]
        tbl.remove(idx)
    if st.get("lift_aid") and best.get("T_start") is not None:
        # round 9 (run 14, F54): a person brings the part on the hoist to the start of its path; the arm comes to it empty with
        # the gripper open (planned so in arm_place), closes on it and guides it down; the hook hangs over it throughout
        if tbl is not None:
            tbl.remove(idx)
        goto(run, actor, dk)
        R.tool(actor, tool, tool_spec(run, actor))
        R.wait(120.0, who="person", what="brings the part on the hoist to the start of its path")
        R.put(idx, best["T_start"], state, why="on the hoist")
        n0 = len(R.events)
        if best.get("path") is not None:
            R.move(actor, best["path"], "plan", close=0.0)
        hook_static(run, R, body, best["T_start"], n0)
        R.grip(actor, close)
        R.attach(actor, idx, off, state, name=st["id"])
        n1 = len(R.events)
        k = fr.get("push_at")
        if fr["qs"] and k:
            # the last few mm pushed home with the closed fingers on its back face, as arm_place checked it (as below)
            R.move(actor, fr["qs"][:k], "cart", close=close, seat_mm=0.0)
            h1 = hook_moves(run, R, actor, body, off, n1)
            R.grip(actor, max(0.0, close - 0.12))
            R.detach(actor)
            R.grip(actor, float(fr.get("push_close", 1.0)))
            R.attach(actor, idx, fr["push_off"], state, name=st["id"])
            n2 = len(R.events)
            R.move(actor, fr["qs"][k:], "cart", close=float(fr.get("push_close", 1.0)), seat_mm=10.0)
            h2 = hook_moves(run, R, actor, body, fr["push_off"], n2)
            row["hoist_hook"] = dict(clear=h1[0] and h2[0], why=h1[1] or h2[1], above_mm=HOOK_ABOVE)
        elif fr["qs"]:
            R.move(actor, fr["qs"], "cart", close=close, seat_mm=10.0)
            hook_moves(run, R, actor, body, off, n1, res=row)
        row["fetch"] = "person"
        return
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
    k = fr.get("push_at")
    if fr["qs"] and k:
        # round 9 (pick-insert-push): in with the part held, let go short of the seat, close the fingers, then push it home on
        # its back face with the closed fingertips, as arm_place checked it (the part rides on the closed fingers' TCP)
        R.move(actor, fr["qs"][:k], "cart", close=close, seat_mm=0.0)
        R.grip(actor, max(0.0, close - 0.12))
        R.detach(actor)
        R.grip(actor, float(fr.get("push_close", 1.0)))
        R.attach(actor, idx, fr["push_off"], state, name=st["id"])
        R.move(actor, fr["qs"][k:], "cart", close=float(fr.get("push_close", 1.0)), seat_mm=10.0)
    elif fr["qs"]:
        R.move(actor, fr["qs"], "cart", close=close, seat_mm=10.0)


def _place_moves(R, actor, path, fr, close):
    if path is not None:
        R.move(actor, path, "plan", close=close)
    if fr["qs"]:
        R.move(actor, fr["qs"], "cart", close=close, seat_mm=10.0)


def hook_static(run, R, body, T, n0):
    """Round 9 (run 14): the hook over a part hanging on the hoist at T, on every move recorded since n0 (the arm's approach)."""
    v = np.asarray(body.v, float)
    w = v @ np.asarray(T, float)[:3, :3].T + np.asarray(T, float)[:3, 3]
    lo, hi = w.min(0), w.max(0)
    p = np.array([0.5 * (lo[0] + hi[0]), 0.5 * (lo[1] + hi[1]), hi[2] + HOOK_ABOVE], np.float32)
    for e in R.events[n0:]:
        if e.get("kind") == "move" and e.get("q") is not None:
            e["hook"] = np.repeat(p[None, :], len(e["q"]), axis=0)
            e["hook_clear"] = True


def hook_moves(run, R, n, body, off, n0, res=None):
    """Round 9 (run 14): the hoist's hook over a part arm n carries in a hoist-assisted place: for each move event recorded since
    index n0, e["hook"] (one point per joint sample, the hook's bottom, HOOK_ABOVE over the part's top) and e["hook_clear"]
    (the hook and its chain against the cell, the parts and both arms, checked every 4th sample)."""
    a = run.arm(n)
    o = "B" if n == "A" else "A"
    ok_all, why_all = True, ""
    for e in R.events[n0:]:
        if e.get("kind") != "move" or e.get("arm") != n or e.get("q") is None:
            continue
        Q = np.asarray(e["q"], float)
        frames = [a.tcp(q, e.get("close")) @ off for q in Q]
        QA = Q if n == "A" else [run.q["A"]] * len(Q)
        QB = Q if n == "B" else [run.q["B"]] * len(Q)
        h = hoist_hook(run, body, frames, QA, QB, e.get("close") if n == "A" else run.arm("A").close,
                       e.get("close") if n == "B" else run.arm("B").close, skip_arm=n)
        e["hook"] = np.asarray(h["p"], np.float32)
        e["hook_clear"] = h["clear"]
        if not h["clear"] and ok_all:
            ok_all, why_all = False, h["why"]
    if res is not None:
        res["hoist_hook"] = dict(clear=ok_all, why=why_all, above_mm=HOOK_ABOVE)
    return ok_all, why_all


def release(run, n, qs_back, opened=True, seat=None):
    """retreat(): let go (the gripper opens a little), then back off along the tool axis. Round 10, seat = (objects, T, state):
    the objects let go of are put on their designed pose at once (see run_assembly.retreat)."""
    if not on():
        return
    R = RECM.REC
    st = R.state[n]
    if st["held"] is not None:
        if run.arm(n).tool_name == "gripper" and opened:
            R.grip(n, max(0.0, st["close"] - 0.12))
        R.detach(n)
        if seat is not None and seat[0]:
            R.put(seat[0], seat[1], seat[2], why="seated")
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
    hook = None
    if st.get("lift_aid"):
        hook = hoist_hook(run, body, frames[:len(QA)], QA, QB, cA, cB)
        res["hook"] = dict(clear=hook["clear"], why=hook["why"], above_mm=HOOK_ABOVE)
    R._ev("move2", arm="A+B", qA=QA.astype(np.float32), qB=QB.astype(np.float32), closeA=cA, closeB=cB, dur=round(dur, 2),
          frames=np.array(frames[:len(QA)], np.float32), lift_aid=bool(st.get("lift_aid")),
          hook=None if hook is None else np.asarray(hook["p"], np.float32), hook_clear=None if hook is None else hook["clear"])
    if st.get("lift_aid") and R.step is not None:
        R.step["person_s"] += dur
    R.state["A"]["q"], R.state["B"]["q"] = QA[-1].copy(), QB[-1].copy()
    if R.step is not None:
        R.step["robot_s"]["B"] += dur
    # B lets go first (its own retreat is recorded by retreat()); the part is released by A
    return dict(approach="PASS" if ok_all else "FAIL", hook=res.get("hook"))


HOOK_ABOVE = 300.0      # mm: the hoist's hook above the carried part's top (a lifting bar on two slings; estimate)
HOOK_BOX = (30.0, 12.0, 50.0)   # half-x, half-y, height of the hook as asm_render draws it; the chain is a Ø8 line up to z 2900


def hoist_hook(run, body, frames, QA, QB, cA, cB, skip_arm=None):
    """Round 9: where the hoist's hook is in each frame of a hoist-assisted carry (lift_aid), and whether it and its chain are
    clear. The hook hangs HOOK_ABOVE mm over the top of the carried part, over the centre of its footprint, on a lifting bar
    whose slings go to the part (eye bolts in tapped holes of its top face): it is never inside the part. The hook and the
    chain (a vertical line up to z 2900) are checked with FCL against the cell, the parts present and both arms at that frame.
    Round 8 drew the hook 60 mm over the midpoint of the arms' TCPs, which for the chamber carried by two legs (F05b) put it
    50 mm into the build module (chapter 41, frames 3297-3376). -> dict(p=(n, 3) hook points (bottom of the hook), clear, why)"""
    import cell2 as K
    from cell import Body, box_mesh, hit
    cl = run.cl
    v = np.asarray(body.v, float)
    v = v[:: max(1, len(v) // 4000)]
    pts, clear, why = [], True, ""
    hx, hy, hh = HOOK_BOX
    for k, F in enumerate(frames):
        w = v @ np.asarray(F, float)[:3, :3].T + np.asarray(F, float)[:3, 3]
        lo, hi = w.min(0), w.max(0)
        p = np.array([0.5 * (lo[0] + hi[0]), 0.5 * (lo[1] + hi[1]), hi[2] + HOOK_ABOVE])
        pts.append(p)
        if not clear or (k % 4 and k != len(frames) - 1):
            continue
        hook_b = Body("hoist hook", *box_mesh(p[0] - hx, p[0] + hx, p[1] - hy, p[1] + hy, p[2], p[2] + hh), kind="tool")
        chain = Body("hoist chain", *box_mesh(p[0] - 4.0, p[0] + 4.0, p[1] - 4.0, p[1] + 4.0, p[2] + hh, 2900.0), kind="tool")
        hook_b.place(np.eye(4))
        chain.place(np.eye(4))
        cl.A.place(QA[k], cA)
        cl.B.place(QB[k], cB)
        world = cl.world("A", other=True)
        for b in list(cl.A.bodies()):
            world.add(b)
        for x in (hook_b, chain):
            for y in world.bodies.values():
                if y.name == "floor" or y is body or y.name.startswith("held:"):
                    continue
                if skip_arm is not None and y.name.startswith(f"{skip_arm}/gr/") and "finger" in y.name:
                    continue            # the guiding arm's fingers on the part's edge, under the lifting bar
                if hit(x.obj, y.obj):
                    clear, why = False, f"{x.name} meets {y.name[:50]} at frame {k}"
                    break
            if not clear:
                break
    return dict(p=np.array(pts), clear=clear, why=why)


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
