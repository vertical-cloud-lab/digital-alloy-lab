"""Check a recorded assembly run as it will be drawn (round 9, issue #260, PR #266).

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/rec_check.py /tmp/robotbuild/traj/run13 [chamber|module] [--every=3]
        [--out=analysis/out/assembly/rec_check_run13.json]

The planner checks each motion against its own world: the cell, the parts present and the other arm where the planner left it.
The renderer draws the recording: the other arm where the recording left it. Where the two differ (a re-plan, an attempt that
was not recorded, a tool the planner changed but the recording did not), a checked motion can still be drawn through the other
arm or a part. Round 8's frame audit found such pairs (two nutrunners 31 mm into each other, a wrist through a screw). This
replays the recording's events exactly as asm_render.py does (objects at the poses of their put events, held objects on the
TCP, each arm's MiR x, tool and gripper opening) and checks, every --every samples of every arm motion:
  * arm against arm: every body of one arm (links, tool or gripper, wrist camera, tool changer, what it holds) against every
    body of the other;
  * each arm (links, tool or gripper with its fingers, wrist camera) against the parts present: not what it holds, not the
    parts it places or the screw it drives in this step, which touch their seats and the fingers by design (--fingers=0: the
    links, tool bodies and camera only).
A pair counts when its translational penetration depth (cell.depth) is over 1.5 mm. Objects are the planner's own meshes
(run_assembly.Run), not the decimated meshes the renderer draws. Like the planner's FCL check, it sees surfaces crossing, not
a body wholly inside another.
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
from cell import Body, Group, Tm  # noqa: E402

LIMIT = 1.5


def load(traj, chapter):
    traj = pathlib.Path(traj)
    f = traj / f"asm_{chapter}.pkl"
    if f.exists():
        return pickle.load(open(f, "rb"))["events"]
    ev = []
    for c in sorted(traj.glob(f"asm_{chapter}.chunk*.pkl")):
        ev += pickle.load(open(c, "rb"))["events"]
    return ev


def main(argv):
    traj = argv[0]
    chapters = [a for a in argv[1:2] if not a.startswith("--")] or ["module", "chamber"]
    opt = {a.split("=")[0][2:]: a.split("=", 1)[1] for a in argv[1:] if a.startswith("--") and "=" in a}
    every = int(opt.get("every", 3))
    fingers = opt.get("fingers", "1") == "1"      # the fingers and fingertips too (not against the part placed or held in the step)
    scn = pickle.load(open(pathlib.Path(traj) / "asm_scene.pkl", "rb"))
    # the planner's own meshes (0.1 mm tessellation, run_assembly.Run's objects after its split): the drawn meshes are decimated to
    # 12,000 triangles, which closes counterbores and holes that a socket or a bit sits in
    import run_assembly as RA
    run = RA.Run()
    objs = {}
    for i in scn["objs"]:
        i = int(i)
        if run.sc.objs[i].get("V") is None:
            continue
        b = run.cl.body(i)
        b.name = f"o{i} {run.sc.label(i)[:50]}"
        objs[i] = b
    out = dict(traj=str(traj), every=every, limit_mm=LIMIT, chapters={})
    for chapter in chapters:
        ev = load(traj, chapter)
        if not ev:
            continue
        arms = {"A": K.ArmT("A", K.DOCKS["T"], "front"), "B": K.ArmT("B", K.DOCKS["T"], "back")}
        st = {n: dict(q=arms[n].park_q(), x=float(K.DOCKS["T"]), close=0.0, tool="gripper", held=None) for n in arms}
        pose = {int(i): np.asarray(T, float) for i, T in scn["table_T"].items()}
        present = set()                      # objects in the cell (not on the table)
        step, step_objs = "", set()
        pairs = {}

        def set_tool(n, tool, spec):
            a = arms[n]
            spec = spec or {}
            if tool in ("screwdriver", "nutrunner", "nutrunner_angle"):
                a.set_tool(tool, extra_bit=float(spec.get("extra_bit") or 0.0), tip_d=spec.get("tip_d"))
            elif tool in ("vacuum", "nozzle", "roller", "roller_n", "wand", "ringpad", "pinrod"):
                a.set_tool(tool)
            else:
                a.set_tool("gripper")

        def place(n):
            s = st[n]
            a = arms[n]
            if abs(a.base[0, 3] - s["x"]) > 1e-6:
                a.move_base(s["x"])
            a.place(s["q"], s["close"])
            if s["held"] is not None:
                T = a.tcp(s["q"], s["close"]) @ s["held"]["off"]
                for i in s["held"]["objs"]:
                    pose[i] = T

        def bodies(n, links_only=False):
            a = arms[n]
            out_ = list(a.links.values()) + list(a.fixed.values())
            for k, b in a.grip.items():
                if links_only and ("finger" in k or "knuckle" in k or "pad" in k):
                    continue
                out_.append(b)
            if not links_only:
                out_ += list(a.caps.values())
                h = st[n]["held"]
                if h is not None:
                    for i in h["objs"]:
                        if i in objs:
                            objs[i].place(pose[i])
                            out_.append(objs[i])
            return out_

        def check(n, kind_, where=""):
            place("A")
            place("B")
            gA, gB = Group(bodies("A")), Group(bodies("B"))
            for x, y in C.group_hits(gA, gB):
                d = C.depth(x, y, upto=50.0)
                if d > LIMIT:
                    key = ("arm-arm", x.name, y.name)
                    r = pairs.setdefault(key, dict(kind="arm-arm", a=x.name, b=y.name, step=step, worst=0.0, samples=0, steps=[]))
                    if float(d) > r["worst"]:
                        r["where"] = where
                    r["worst"] = max(r["worst"], float(d))
                    r["samples"] += 1
                    if step not in r["steps"]:
                        r["steps"].append(step)
            held = set(st[n]["held"]["objs"]) if st[n]["held"] else set()
            w = Group()
            for i in present:
                if i in held or i in step_objs or i not in objs:
                    continue
                objs[i].place(pose[i])
                w.add(objs[i])
            mine = [b for b in (bodies(n, links_only=not fingers)) if not b.name.startswith("o")]     # not what it holds
            for x, y in C.group_hits(Group(mine), w):
                d = C.depth(x, y, upto=50.0)
                if d > LIMIT:
                    key = ("arm-part", x.name, y.name)
                    r = pairs.setdefault(key, dict(kind="arm-part", a=x.name, b=y.name, step=step, worst=0.0, samples=0, steps=[]))
                    if float(d) > r["worst"]:
                        r["where"] = where
                    r["worst"] = max(r["worst"], float(d))
                    r["samples"] += 1
                    if step not in r["steps"]:
                        r["steps"].append(step)

        # a move the planner could not plan is followed by an "unplanned" mark: asm_render.py does not draw it, so it is not checked
        unplanned = set()
        last = {}
        for j, e in enumerate(ev):
            if e["kind"] in ("move", "screw") and e.get("arm") in ("A", "B"):
                last[e["arm"]] = j
            elif e["kind"] == "mark" and e.get("what") == "unplanned" and e.get("arm") in last:
                unplanned.add(last[e["arm"]])
        n_samples = 0
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
                    set_tool(m, a.get("tool", "gripper"), {})
                for i, T in (e.get("present") or {}).items():
                    pose[int(i)] = np.asarray(T, float)
                    present.add(int(i))
            elif k == "step":
                step = e["id"]
                step_objs = set()
            elif k == "put":
                for i in e["objs"]:
                    pose[int(i)] = np.asarray(e["T"], float)
                    present.add(int(i))
            elif k == "take":
                for i in e["objs"]:
                    present.discard(int(i))
            elif k == "attach":
                st[n]["held"] = dict(objs=[int(i) for i in e["objs"]], off=np.asarray(e["off"], float))
                step_objs |= set(int(i) for i in e["objs"])
                for i in e["objs"]:
                    present.add(int(i))
            elif k == "detach":
                if st[n]["held"] is not None and e.get("T") is not None:
                    for i in st[n]["held"]["objs"]:
                        pose[i] = np.asarray(e["T"], float)
                st[n]["held"] = None
            elif k == "tool":
                st[n]["tool"] = e["tool"]
                set_tool(n, e["tool"], e.get("spec"))
            elif k == "grip":
                st[n]["close"] = float(e["c1"])
            elif k == "drive":
                st[n]["x"] = float(e["x1"])
            elif k == "jump":
                st[n]["q"] = np.asarray(e["to"], float)
            elif k in ("move", "screw"):
                if k == "screw":
                    step_objs.add(int(e["obj"]))
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
                    check(n, k, f"event {j_ev} {k}/{e.get('how', '')} arm {n} sample {j} of {len(Q)}")
                    n_samples += 1
                st[n]["q"] = Q[-1]
            elif k == "move2":
                QA, QB = np.asarray(e["qA"], float), np.asarray(e["qB"], float)
                st["A"]["close"], st["B"]["close"] = float(e["closeA"]), float(e["closeB"])
                for j in sorted(set(list(range(0, len(QA), every)) + [len(QA) - 1])):
                    st["A"]["q"], st["B"]["q"] = QA[j], QB[min(j, len(QB) - 1)]
                    check("A", k, f"event {j_ev} move2 sample {j} of {len(QA)}")
                    n_samples += 1
            elif k == "turn":
                TT = np.asarray(e["TT"], float)
                Rm = TT @ Tm(C.rot((1, 0, 0), float(e["sign"]) * 180.0)) @ np.linalg.inv(TT)
                for i in e["objs"]:
                    pose[int(i)] = Rm @ np.asarray(e["T0"], float)
        res = sorted(pairs.values(), key=lambda r: -r["worst"])
        for r in res:
            r["worst"] = round(r["worst"], 1)
        out["chapters"][chapter] = dict(samples=n_samples, pairs=len(res), arm_arm=sum(1 for r in res if r["kind"] == "arm-arm"),
                                        arm_part=sum(1 for r in res if r["kind"] == "arm-part"), list=res)
        print(f"{chapter}: {n_samples} samples, {len(res)} pairs over {LIMIT} mm")
        for r in res[:40]:
            print(f"  {r['kind']:8s} {r['worst']:6.1f} mm x{r['samples']:4d}  {r['a'][:40]:40s} {r['b'][:50]:50s} {','.join(r['steps'][:6])}  "
                  f"[{r.get('where', '')}]")
    if opt.get("out"):
        pathlib.Path(opt["out"]).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
