"""Check a recorded assembly run as it will be drawn (rounds 9-10, issue #260, PR #266).

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/rec_check.py /tmp/robotbuild/traj/run15 [chamber|module] [--every=3]
        [--steps=F10a,F10f] [--out=analysis/out/assembly/rec_check_run15.json]

The planner checks each motion against its own world: the cell, the parts present and the other arm where the planner left it.
The renderer draws the recording. Where the two differ (a re-plan, an attempt that was not recorded, a tool the planner changed
but the recording did not), a checked motion can still be drawn through the other arm or a part. This replays the recording's
events exactly as cad/robotbuild/asm_render.py does (objects at the poses of their put events; a held object on the TCP at the
gripper opening it was attached at, re-anchored by a put while held; each arm's MiR x, tool and opening; a small jump between
two motions drawn as a move, a large one as a cut; a screw no arm could drive hidden) and checks, every --every samples of
every drawn arm motion, with the planner's own 0.1 mm meshes (the drawn meshes are decimated to 12,000 triangles):
  * arm-arm: every body of one arm (links, tool or gripper, wrist camera, tool changer, what it holds) against the other's;
  * arm-part: each arm's links, gripper, tool and camera against the parts present, the cell's fixtures and the long table
    (round 10: also against the step's own parts for the links and camera);
  * part-part (round 10): what an arm holds against the parts present, the fixtures and the long table (round 9 never checked
    a held part: the frame audit's 73 "part in part" pairs in chapter 41). Two parts at their designed relative pose (one
    machine frame) that overlap are the CAD's own overlap (an uncut groove), listed apart and not counted, as the audit does;
  * tool-own (round 10): a tool body (wand, ring pad, pin pusher, vacuum gripper, nozzle) against the part it carries or works
    on in the step, beyond the intended contact (1.5 mm);
  * grip (round 10): the 2F-85's fingers, knuckles and caps against the part they hold, deeper than the pads' 5 mm;
  * containment (round 10): every pair above whose boxes overlap but whose surfaces do not cross is tested for one body lying
    wholly inside the other (ray parity, cell.inside), and its depth is the translation that frees it (cell.depth);
  * seat (round 10): a part let go of more than 1.5 mm from the pose it is put on next (its designed seat), with the samples
    drawn in between; a part whose drawn pose at its step's end is more than 1.5 mm from its designed pose;
  * put (round 10): a put (a staged part, a merge, the trunnion's turn) into the long table or a fixture.
A pair counts when its translational penetration depth is over 1.5 mm (5 mm for grip). Not checked: the MiRs (the planner's
route check), the hoist's hook, the person (the renderer's).
"""
from __future__ import annotations

import json
import math
import pathlib
import pickle
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cell2 as K  # noqa: E402
import cell as C  # noqa: E402
from cell import Group, Tm  # noqa: E402

LIMIT = 1.5
GRIP_LIMIT = 5.0
JUMP_DEG = 5.0              # asm_render.JUMP_DEG: a smaller jump is drawn as a move
TOOLS = ("wand", "ringpad", "pinrod", "vacuum", "nozzle", "roller", "roller_n")


def load(traj, chapter):
    traj = pathlib.Path(traj)
    f = traj / f"asm_{chapter}.pkl"
    if f.exists():
        return pickle.load(open(f, "rb"))["events"]
    ev = []
    for c in sorted(traj.glob(f"asm_{chapter}.chunk*.pkl")):
        ev += pickle.load(open(c, "rb"))["events"]
    return ev


def _is_finger(name):
    return any(k in name for k in ("finger", "knuckle", "pad", "/cap/"))


def main(argv):
    traj = argv[0]
    chapters = [a for a in argv[1:2] if not a.startswith("--")] or ["module", "chamber"]
    opt = {a.split("=")[0][2:]: (a.split("=", 1)[1] if "=" in a else "1") for a in argv[1:] if a.startswith("--")}
    every = int(opt.get("every", 3))
    only_steps = set(x for x in opt.get("steps", "").split(",") if x)
    scn = pickle.load(open(pathlib.Path(traj) / "asm_scene.pkl", "rb"))
    import run_assembly as RA
    run = RA.Run()
    objs = {}
    for i in scn["objs"]:
        i = int(i)
        if i >= len(run.sc.objs) or run.sc.objs[i].get("V") is None:
            continue
        b = run.cl.body(i)
        b.name = f"o{i} {run.sc.label(i)[:50]}"
        objs[i] = b
    # the cell's static bodies (not the MiRs: their route is checked by the planner; not the floor) and the long table
    statics = {k: b for k, b in run.cl.static.items() if not (k.startswith("A ") or k.startswith("B ")) and k != "floor"}
    jaws = statics.get("Trunnion jaws")
    J0 = jaws.M.copy() if jaws is not None else None
    table = []
    try:
        import fetch as FE
        tb = FE.Table(run)
        table = list(tb.static) + [b for bs in tb.furn.values() for b in bs]
        for b in table:
            b.name = "kt/" + b.name
    except Exception as e:  # noqa: BLE001
        print("no long table model:", e)
    out = dict(traj=str(traj), every=every, limit_mm=LIMIT, grip_limit_mm=GRIP_LIMIT, chapters={})
    for chapter in chapters:
        ev = load(traj, chapter)
        if not ev:
            continue
        arms = {"A": K.ArmT("A", K.DOCKS["T"], "front"), "B": K.ArmT("B", K.DOCKS["T"], "back")}
        st = {n: dict(q=arms[n].park_q(), x=float(K.DOCKS["T"]), close=0.0, tool="gripper", held=None) for n in arms}
        pose = {int(i): np.asarray(T, float) for i, T in scn["table_T"].items()}
        designed = {}                        # object -> its last put pose (the planner's designed pose)
        released = {}                        # object -> (pose at its release, step, samples drawn since)
        present = set()                      # objects in the cell (not on the table)
        hidden = set()                       # screws no arm could drive: hidden until the person drives them
        failed = set()
        step, step_objs = "", set()
        pairs = {}
        seat_off = []
        if jaws is not None:
            jaws.place(J0)

        def rec(kind, a, b, d, where, contained=False):
            if only_steps and step not in only_steps:
                return
            key = (kind, a, b)
            r = pairs.setdefault(key, dict(kind=kind, a=a, b=b, step=step, worst=0.0, samples=0, steps=[], contained=False))
            if float(d) > r["worst"]:
                r["where"] = where
                r["step"] = step
            r["worst"] = max(r["worst"], float(d))
            r["samples"] += 1
            r["contained"] = r["contained"] or contained
            if step not in r["steps"]:
                r["steps"].append(step)

        def set_tool(n, tool, spec):
            a = arms[n]
            spec = spec or {}
            if tool in ("screwdriver", "nutrunner", "nutrunner_angle"):
                a.set_tool(tool, extra_bit=float(spec.get("extra_bit") or 0.0), tip_d=spec.get("tip_d"))
            elif tool in TOOLS:
                a.set_tool(tool)
            elif tool == "gripper+caps":
                import tooling as TL
                caps, _ = TL.mesh("ring_caps")
                a.set_tool("gripper", caps=dict(name="ring caps", meshes=caps, grasp_z=31.9, inner_x=23.0, color="#d9b23a"))
            elif tool == "gripper+plate":
                import eoat as E
                a.set_tool("gripper", caps=E.plate_finger_spec())
            else:
                a.set_tool("gripper")

        def place(n):
            s = st[n]
            a = arms[n]
            if abs(a.base[0, 3] - s["x"]) > 1e-6:
                a.move_base(s["x"])
            a.place(s["q"], s["close"])
            if s["held"] is not None:
                T = a.tcp(s["q"], s["held"]["close0"]) @ s["held"]["off"]
                for i in s["held"]["objs"]:
                    pose[i] = T

        def arm_bodies(n):
            a = arms[n]
            return list(a.links.values()) + list(a.fixed.values()) + list(a.grip.values()) + list(a.caps.values())

        def held_bodies(n):
            h = st[n]["held"]
            out_ = []
            if h is not None:
                for i in h["objs"]:
                    if i in objs and i not in hidden:
                        objs[i].place(pose[i])
                        out_.append(objs[i])
            return out_

        def same_frame(i, j):
            Ti, Tj = pose.get(i), pose.get(j)
            if Ti is None or Tj is None:
                return False
            return float(np.abs(Ti - Tj)[:3, 3].max()) < 0.5 and float(np.abs(Ti - Tj)[:3, :3].max()) < 1e-3

        def pair_depth(x, y, hitp):
            if hitp:
                return C.depth(x, y, upto=50.0), False
            if C.contained(x, y):
                return C.depth(x, y, upto=50.0), True
            return 0.0, False

        def test(gx, gy, fn, where):
            """fn(x, y) -> (kind, limit) or None to skip; records the pairs deeper than the limit (crossing or contained)."""
            missed = []
            hits = C.group_hits(gx, gy, missed=missed)
            for x, y, h in [(x, y, True) for x, y in hits] + [(x, y, False) for x, y in missed]:
                r = fn(x, y)
                if r is None:
                    continue
                kind, lim = r
                if not h and x.kind == "arm" and y.kind != "held":
                    continue              # an arm link wholly inside a part is not a case (it would cross first)
                d, cont = pair_depth(x, y, h)
                if d > lim:
                    rec(kind, x.name, y.name, d, where, cont)

        def world_bodies(n, include_own=False):
            held_all = set()
            for m in ("A", "B"):
                if st[m]["held"] is not None:
                    held_all |= set(st[m]["held"]["objs"])
            ws = []
            for i in present:
                if i in held_all or i in hidden or i not in objs:
                    continue
                if not include_own and i in step_objs:
                    continue
                objs[i].place(pose[i])
                ws.append(objs[i])
            return ws

        def check(n, where=""):
            if only_steps and step not in only_steps:
                return                       # --steps: replay the state, check only the chosen steps
            place("A")
            place("B")
            # arm against arm (with what they hold)
            gA = Group(arm_bodies("A") + held_bodies("A"))
            gB = Group(arm_bodies("B") + held_bodies("B"))
            test(gA, gB, lambda x, y: ("arm-arm", LIMIT), where)
            mine = arm_bodies(n)
            held = held_bodies(n)
            held_ids = set(st[n]["held"]["objs"]) if st[n]["held"] else set()
            tool_name = st[n]["tool"]
            # the arm against the parts present (not its own step's parts), the cell and the table
            w = Group(world_bodies(n) + list(statics.values()) + table)
            test(Group(mine), w, lambda x, y: ("arm-part", LIMIT), where)
            # the links and camera against the step's own parts too (round 10)
            own_ids = [i for i in step_objs if i in present and i not in held_ids and i in objs and i not in hidden]
            for i in own_ids:
                objs[i].place(pose[i])
            own = [objs[i] for i in own_ids]
            if own:
                def fn_own(x, y):
                    if x.kind == "arm" or "camera" in x.name or "changer" in x.name:
                        return ("arm-part", LIMIT)
                    if x.kind == "tool" and tool_name in TOOLS:
                        return ("tool-own", LIMIT)
                    if _is_finger(x.name) or x.kind == "gripper":
                        return ("grip", GRIP_LIMIT)
                    return None                 # a driver's bit in its screw: intended
                test(Group(mine), Group(own), fn_own, where)
            if held:
                # what it holds against the world
                def fn_held(x, y):
                    xi = int(x.name.split()[0][1:])
                    if y.name.startswith("o"):
                        yi = int(y.name.split()[0][1:])
                        if same_frame(xi, yi):
                            return None         # the CAD's own overlap at the designed relative pose
                    return ("part-part", LIMIT)
                test(Group(held), w, fn_held, where)
                # the tool and the fingers against what they hold
                def fn_tool(x, y):
                    if x.kind == "tool" and tool_name in TOOLS:
                        return ("tool-own", LIMIT)
                    if _is_finger(x.name) or (x.kind == "gripper" and "changer" not in x.name):
                        return ("grip", GRIP_LIMIT)
                    if x.kind == "arm" or "camera" in x.name or "changer" in x.name:
                        return ("arm-part", LIMIT)
                    return None
                test(Group(mine), Group(held), fn_tool, where)

        def check_put(objs_put, where):
            """A put into the long table or a fixture (not into parts: those are their designed poses)."""
            if only_steps and step not in only_steps:
                return
            bs = []
            for i in objs_put:
                if i in objs and i not in hidden:
                    objs[i].place(pose[i])
                    bs.append(objs[i])
            if bs:
                test(Group(bs), Group(list(statics.values()) + table), lambda x, y: ("put", LIMIT), where)
                # round 10: and against the parts already present in another frame (another sub-assembly, or one put
                # elsewhere): an overlap a put leaves stays drawn until the next put (round 9: the metering base 7 mm into the
                # reservoir rails for 500 frames). Parts held by an arm are checked as they move, not here.
                ids = set(objs_put)
                held_all = set()
                for m in ("A", "B"):
                    if st[m]["held"] is not None:
                        held_all |= set(st[m]["held"]["objs"])
                others = []
                for i in present:
                    if i in ids or i in held_all or i in hidden or i not in objs:
                        continue
                    objs[i].place(pose[i])
                    others.append(objs[i])
                if others:
                    def fn_put(x, y):
                        xi, yi = int(x.name.split()[0][1:]), int(y.name.split()[0][1:])
                        return None if same_frame(xi, yi) else ("put", LIMIT)
                    test(Group(bs), Group(others), fn_put, where)

        unplanned = set()
        last = {}
        for j, e in enumerate(ev):
            if e["kind"] in ("move", "screw") and e.get("arm") in ("A", "B"):
                last[e["arm"]] = j
            elif e["kind"] == "mark" and e.get("what") == "unplanned" and e.get("arm") in last:
                unplanned.add(last[e["arm"]])
        n_samples = 0

        def step_end():
            """The step's end: what it placed, drawn off its designed pose (the last put)."""
            if only_steps and step not in only_steps:
                return
            for i in sorted(step_objs):
                if i in designed and i in present and i not in hidden and not any(
                        st[m]["held"] is not None and i in st[m]["held"]["objs"] for m in ("A", "B")):
                    dd = float(np.linalg.norm(pose[i][:3, 3] - designed[i][:3, 3]))
                    if dd > LIMIT:
                        seat_off.append(dict(step=step, obj=i, name=objs[i].name if i in objs else str(i),
                                             kind="off its seat at its step's end", mm=round(dd, 1)))

        def tick(k=1):
            for i in list(released):
                p, s0, c = released[i]
                released[i] = (p, s0, c + k)

        for j_ev, e in enumerate(ev):
            k = e["kind"]
            n = e.get("arm")
            if k == "init":
                for m, a in e["arms"].items():
                    if a.get("q") is not None:
                        st[m]["q"] = np.asarray(a["q"], float)
                    if a.get("x") is not None:
                        st[m]["x"] = float(a["x"])
                    st[m]["close"] = float(a.get("close") or 0.0)
                    st[m]["tool"] = a.get("tool", "gripper")
                    set_tool(m, st[m]["tool"], {})
                for i, T in (e.get("present") or {}).items():
                    pose[int(i)] = np.asarray(T, float)
                    designed[int(i)] = pose[int(i)]
                    present.add(int(i))
            elif k == "step":
                if step:
                    step_end()
                step = e["id"]
                step_objs = set()
            elif k == "put":
                ids = [int(i) for i in e["objs"]]
                for i in ids:
                    if i in failed:
                        hidden.add(i)
                    T = np.asarray(e["T"], float)
                    if i in released:
                        p0, s0, c = released.pop(i)
                        dd = float(np.linalg.norm(p0[:3, 3] - T[:3, 3]))
                        ang = float(np.degrees(np.arccos(np.clip((np.trace(p0[:3, :3].T @ T[:3, :3]) - 1) / 2, -1, 1))))
                        if (dd > LIMIT or ang > 1.0) and (not only_steps or s0 in only_steps):
                            seat_off.append(dict(step=s0, obj=i, name=objs[i].name if i in objs else str(i),
                                                 kind="released off the pose it is put on next", mm=round(dd, 1),
                                                 deg=round(ang, 1), samples_drawn_off=c))
                    pose[i] = T
                    designed[i] = T
                    present.add(i)
                # a put of parts an arm holds re-anchors the hold (asm_render.Replay.put)
                for m in ("A", "B"):
                    h = st[m]["held"]
                    if h is not None and set(h["objs"]) & set(ids):
                        a = arms[m]
                        if abs(a.base[0, 3] - st[m]["x"]) > 1e-6:
                            a.move_base(st[m]["x"])
                        h["off"] = np.linalg.inv(a.tcp(st[m]["q"], h["close0"])) @ np.asarray(e["T"], float)
                check_put(ids, f"event {j_ev} put ({e.get('why', '')})")
            elif k == "take":
                for i in e["objs"]:
                    present.discard(int(i))
            elif k == "attach":
                st[n]["held"] = dict(objs=[int(i) for i in e["objs"]], off=np.asarray(e["off"], float), close0=float(st[n]["close"]))
                step_objs |= set(int(i) for i in e["objs"])
                for i in e["objs"]:
                    present.add(int(i))
                    released.pop(int(i), None)
                check(n, f"event {j_ev} attach arm {n}")
                n_samples += 1
            elif k == "detach":
                h = st[n]["held"]
                if h is not None:
                    place(n)
                    for i in h["objs"]:
                        released[i] = (pose[i].copy(), step, 0)
                st[n]["held"] = None
            elif k == "tool":
                st[n]["tool"] = e["tool"]
                set_tool(n, e["tool"], e.get("spec"))
            elif k == "grip":
                st[n]["close"] = float(e["c1"])
                if float(e["c1"]) > float(e["c0"]):
                    check(n, f"event {j_ev} grip arm {n} closes to {float(e['c1']):.2f}")
                    n_samples += 1
            elif k == "drive":
                st[n]["x"] = float(e["x1"])
            elif k == "jump":
                q0, q1 = np.asarray(st[n]["q"], float), np.asarray(e["to"], float)
                dq = float(np.degrees(np.max(np.abs(q1 - q0))))
                if dq <= JUMP_DEG:
                    for s in (0.25, 0.5, 0.75, 1.0):
                        st[n]["q"] = q0 + (q1 - q0) * s
                        check(n, f"event {j_ev} jump {dq:.1f} deg drawn as a move, arm {n} at {s:.2f}")
                        n_samples += 1
                        tick()
                st[n]["q"] = q1
            elif k in ("move", "screw"):
                if k == "screw":
                    step_objs.add(int(e["obj"]))
                    if not e.get("ok") and (e.get("q") is None or not len(e["q"])):
                        later = [x for x in ev[j_ev + 1:j_ev + 40] if x.get("step") == e.get("step") and x["kind"] == "screw"
                                 and x.get("obj") == e.get("obj") and x.get("ok")]
                        if not later:
                            failed.add(int(e["obj"]))
                            hidden.add(int(e["obj"]))
                if e.get("q") is None or not len(e["q"]):
                    continue
                if e.get("close") is not None:
                    st[n]["close"] = float(e["close"])
                Q = np.asarray(e["q"], float)
                if j_ev in unplanned:
                    st[n]["q"] = Q[-1]
                    continue
                idx = list(range(0, len(Q), every)) + [len(Q) - 1]
                for j in sorted(set(idx)):
                    st[n]["q"] = Q[j]
                    check(n, f"event {j_ev} {k}/{e.get('how', '')} arm {n} sample {j} of {len(Q)}")
                    n_samples += 1
                    tick()
                st[n]["q"] = Q[-1]
            elif k == "move2":
                QA, QB = np.asarray(e["qA"], float), np.asarray(e["qB"], float)
                st["A"]["close"], st["B"]["close"] = float(e["closeA"]), float(e["closeB"])
                for j in sorted(set(list(range(0, len(QA), every)) + [len(QA) - 1])):
                    st["A"]["q"], st["B"]["q"] = QA[j], QB[min(j, len(QB) - 1)]
                    check("A", f"event {j_ev} move2 sample {j} of {len(QA)}")
                    check("B", f"event {j_ev} move2 sample {j} of {len(QA)}")
                    n_samples += 1
                    tick()
            elif k == "turn":
                TT = np.asarray(e["TT"], float)
                Rm = TT @ Tm(C.rot((1, 0, 0), float(e["sign"]) * 180.0)) @ np.linalg.inv(TT)
                for i in e["objs"]:
                    pose[int(i)] = Rm @ np.asarray(e["T0"], float)
                    designed[int(i)] = pose[int(i)]
                if jaws is not None:
                    jaws.place(Rm @ jaws.M)
        if step:
            step_end()
        res = sorted(pairs.values(), key=lambda r: -r["worst"])
        for r in res:
            r["worst"] = round(r["worst"], 1)
        by_kind = {}
        for r in res:
            by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
        by_step = {}
        for r in res:
            d = by_step.setdefault(r["step"], dict(pairs=0, worst=0.0, kinds={}))
            d["pairs"] += 1
            d["worst"] = max(d["worst"], r["worst"])
            d["kinds"][r["kind"]] = d["kinds"].get(r["kind"], 0) + 1
        for s in seat_off:
            d = by_step.setdefault(s["step"], dict(pairs=0, worst=0.0, kinds={}))
            d["kinds"]["seat"] = d["kinds"].get("seat", 0) + 1
        out["chapters"][chapter] = dict(samples=n_samples, pairs=len(res), by_kind=by_kind,
                                        arm_arm=by_kind.get("arm-arm", 0), arm_part=by_kind.get("arm-part", 0),
                                        part_part=by_kind.get("part-part", 0), tool_own=by_kind.get("tool-own", 0),
                                        grip=by_kind.get("grip", 0), put=by_kind.get("put", 0),
                                        contained=sum(1 for r in res if r["contained"]),
                                        seat=seat_off, n_seat=len(seat_off), by_step=by_step, list=res)
        print(f"{chapter}: {n_samples} samples, {len(res)} pairs over the limits ({by_kind}); {len(seat_off)} seat findings", flush=True)
        for r in res[:80]:
            print(f"  {r['kind']:9s} {r['worst']:6.1f} mm x{r['samples']:4d} {'C' if r['contained'] else ' '} {r['a'][:40]:40s} "
                  f"{r['b'][:50]:50s} {','.join(r['steps'][:6])}  [{r.get('where', '')}]")
        for s in seat_off[:60]:
            print(f"  seat      {s['mm']:6.1f} mm {s.get('deg', '')} {s['step']:6s} {s['name'][:50]:50s} {s['kind']} "
                  f"{s.get('samples_drawn_off', '')}")
    if opt.get("out"):
        pathlib.Path(opt["out"]).write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main(sys.argv[1:])
