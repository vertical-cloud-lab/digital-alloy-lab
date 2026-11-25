"""Chapters 40-assembly-module and 41-assembly-chamber of the robot-built video (issue #260, PR #266, round 7): the
two-arm assembly replayed from the recorded, collision-checked trajectories (analysis/assembly/run_assembly.py with
ASM_RECORD, record.py), on the shared look and frame contract (common.py).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python asm_render.py module|chamber [--max=N] [--fps=12]

Reads /tmp/robotbuild/traj/asm_scene.pkl (every object's mesh and its slot on the long table) and asm_<chapter>.pkl (the
event stream), writes /tmp/robotbuild/frames/40-assembly-module/ or 41-assembly-chamber/ (common.Chapter).

Time: every event carries its real-world duration (record.py's speeds); a frame stands for 1/12 s of it at real time, or
more in a time-lapse (drives, repeated screws, a person's long jobs), and the frame's `proc_s` and `sub` say which. The
`add` counters sum the robots' working time (robot_h: arm A and arm B separately added) and the persons'.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import pickle
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parents[1]
for p in (HERE, LPBF / "analysis" / "assembly", LPBF / "analysis" / "robot", LPBF / "cad"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
_VID = os.environ.get("ROBOTBUILD_VIDEO_DIR")
try:
    import pvscene  # noqa: E402
except ImportError:          # the video worker's people.py / pvscene.py / hall.py before the branches merge
    if _VID:
        sys.path.append(_VID)
    import pvscene  # noqa: E402
import common  # noqa: E402
import kit_table as KT  # noqa: E402

FPS = common.FPS
TRAJ = common.TRAJ
CHAP = {"module": ("40-assembly-module", "Assembly 1: the build module, by two UR12e on MiR250s"),
        "chamber": ("41-assembly-chamber", "Assembly 2: the chamber and the process module, by two UR12e on MiR250s")}
# time-lapse factors per event kind (real seconds per real second shown); the renderer may raise them to fit the budget
LAPSE = dict(drive=8.0, plan=1.5, cart=1.0, grip=1.0, screw=1.0, screw_rep=6.0, wait=40.0, turn=1.5, move2=1.5, tool=8.0)
SHOT = dict(wide=3600.0, mid=1500.0, close=650.0)


def poly(v, f):
    import pyvista as pv
    v = np.asarray(v, float)
    f = np.asarray(f, int)
    return pv.PolyData(v, np.c_[np.full(len(f), 3), f].ravel())


def Tm(p=(0.0, 0.0, 0.0)):
    m = np.eye(4)
    m[:3, 3] = p
    return m


def rot_axis(axis, deg, c=(0.0, 0.0, 0.0)):
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    t = math.radians(deg)
    K_ = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    R = np.eye(3) + math.sin(t) * K_ + (1 - math.cos(t)) * K_ @ K_
    M = np.eye(4)
    M[:3, :3] = R
    c = np.asarray(c, float)
    M[:3, 3] = c - R @ c
    return M


def smooth(s):
    return s * s * (3 - 2 * s)


class Replay:
    def __init__(self, chapter, lapse=None, people_ok=True):
        import cell2 as K
        import hall
        self.K = K
        self.chapter = chapter
        self.lapse = dict(LAPSE, **(lapse or {}))
        scn = pickle.load(open(TRAJ / "asm_scene.pkl", "rb"))
        self.objs = scn["objs"]
        self.ev = pickle.load(open(TRAJ / f"asm_{chapter}.pkl", "rb"))["events"]
        self.pl = common.plotter()
        self.sc = pvscene.PVScene(self.pl)
        sc = self.sc
        # ---- static: floor, bench and fixtures (cell2's static bodies), the long table, pallets and bins
        import pyvista as pv
        sc.add("floor", pv.Box(bounds=(-3500, 15500, -3000, 3000, -20, 0)).triangulate(), common.COL.get("floor", "#b9bdb8"),
               group="static", specular=0.05)
        cl_static = self._cell_static()
        for name, (v, f), col in cl_static:
            sc.add(f"st/{name}", poly(v, f), col, group="static", specular=0.2)
        for name, m, col in KT.table_meshes():
            sc.add(f"kt/{name}", m, col, group="static", specular=0.15)
        for it in KT.item_meshes():
            s = next((x for x in KT.slots() if x["key"] == it["key"]), None)
            if s is not None and s["support"] in ("pallet", "bin"):
                sc.add(f"kti/{it['key']}/{it['name'][:20]}", it["mesh"], it["color"], group="static", specular=0.25)
        # ---- objects (each its own group, moved per frame)
        self.T = {}
        for i, o in scn["objs"].items():
            sc.add(f"o{i}", poly(o["V"], o["F"]), o["color"], group=f"o{i}", specular=0.3, shown=False)
        for i, T in scn["table_T"].items():
            self.T[i] = np.asarray(T, float)
            sc.alpha[f"o{i}"] = 1.0
            sc.gmat[f"o{i}"] = self.T[i]
        # ---- arms and MiRs
        self.arm = {"A": K.ArmT("A", K.DOCKS["T"], "front"), "B": K.ArmT("B", K.DOCKS["T"], "back")}
        self.vis = {n: hall.ArmVis(sc, self.arm[n], n) for n in ("A", "B")}
        self.mir = {n: hall.MirVis(sc, n, "front" if n == "A" else "back") for n in ("A", "B")}
        self.tool_keys = {"A": [], "B": []}
        # fingertip caps: the ring caps (internal two-pin grip) and the tending robot's cranked plate fingers
        import tooling as TL0
        import eoat
        caps = {"ring": TL0.mesh("ring_caps")[0], "plate": eoat.plate_finger_spec()["meshes"]}
        for n in ("A", "B"):
            for kind, ms in caps.items():
                for tip, (v, f) in ms.items():
                    sc.add(f"{n}/cap/{kind}/{tip}", poly(v, f), "#d9b23a" if kind == "ring" else "#7f8c99", group=f"{n}/cap/{kind}/{tip}",
                           specular=0.3, shown=False)
        # hand tools held in the gripper (temporary objects in the run) are among self.objs
        # ---- the trunnion's jaws
        import tooling as TL
        (v, f), _ = TL.mesh("trunnion_jaws")
        sc.add("jaws", poly(v, f), "#d18a1f", group="jaws", specular=0.3)
        self.TT = Tm((K.STATIONS["T"], 0.0, TL.TRUNNION["h_axis"]))
        sc.gmat["jaws"] = self.TT
        self.jaw = 0.0
        # ---- a hoist hook and chain for the hoist-assisted lifts (drawn above the carried part)
        hook = pv.Box(bounds=(-30, 30, -12, 12, 0, 50)).triangulate().merge(pv.Cylinder(center=(0, 0, 1000), direction=(0, 0, 1), radius=4,
                                                                                          height=1900).triangulate())
        sc.add("hoist", hook, "#e2b007", group="hoist", specular=0.3, shown=False)
        # ---- a person for the person steps
        self.person = None
        if people_ok:
            try:
                import people
                self.person = people.Person(sc, "op")
                self.person.set(x=-2300.0, y=-1500.0, hd=60.0, amp=0.0)
                self.person.show(0.0)
            except Exception as e:   # noqa: BLE001
                print("no person:", e)
        # state
        self.st = {n: dict(q=self.arm[n].park_q(), x=float(K.DOCKS["T"]), close=0.0, tool="gripper", held=None) for n in ("A", "B")}
        self.cam_pos = None
        self.cam_foc = None

    def _cell_static(self):
        """cell2's floor-standing furniture (bench, fixtures, nests) without the MiRs, the floor and the moving jaws."""
        K = self.K
        import tooling as TL
        b = K.BENCH
        out = [("bench top", K.box_mesh(b["x0"], b["x1"], b["y0"], b["y1"], b["top"] - b["t"], b["top"]), "#7d8790")]
        for x in (b["x0"] + 40, b["x1"] - 40):
            for y in (b["y0"] + 40, b["y1"] - 40):
                out.append((f"bench leg {x:.0f} {y:.0f}", K.box_mesh(x - 30, x + 30, y - 30, y + 30, 0.0, b["top"] - b["t"]), "#7d8790"))
        tx = K.Cell._tx
        TT = Tm((K.STATIONS["T"], 0.0, TL.TRUNNION["h_axis"]))
        out.append(("Trunnion stands", tx(TL.mesh("trunnion_stands")[0], TT), "#c9a227"))
        out.append(("Fixture B", tx(TL.mesh("fixture_B", K.Z_B)[0], Tm((K.STATIONS["B"], 0.0, K.Z_B + 175.0))), "#c9a227"))
        out.append(("Fixture P", tx(TL.mesh("fixture_P", K.Z_P)[0], Tm((K.STATIONS["P"], 0.0, K.Z_P + 20.0))), "#c9a227"))
        out.append(("Stack nest", tx(TL.mesh("nest_stack")[0], Tm((K.STATIONS["stack"], 0.0, b["top"] + 146.0))), "#c9a227"))
        out.append(("Module nest inv", tx(TL.mesh("nest_body_inv")[0], Tm((K.STATIONS["body_inv"], 0.0, b["top"] + 140.0))), "#c9a227"))
        out.append(("Module nest up", tx(TL.mesh("nest_body_up")[0], Tm((K.STATIONS["body_up"], 0.0, b["top"] + 200.0))), "#c9a227"))
        return out

    # ------------------------------------------------------------------------------------------- state -> scene
    def set_arm(self, n, q=None, x=None, close=None, tool=None):
        s = self.st[n]
        if q is not None:
            s["q"] = np.asarray(q, float)
        if x is not None:
            s["x"] = float(x)
        if close is not None:
            s["close"] = float(close)
        if tool is not None:
            s["tool"] = tool
        a = self.arm[n]
        a.move_base(s["x"])
        a.q = s["q"]
        a.close = s["close"]
        self.mir[n].at(s["x"])
        self.vis[n].update()
        sc = self.sc
        F = a.fk()
        W0 = a.base @ F["tool0"]
        Wt = W0 @ Tm((0.0, 0.0, self.K.TC_H))
        grip_on = s["tool"].startswith("gripper") or s["tool"] in ("hand",)
        for nm in self.vis[n].names():
            if "/gr/" in nm and "camera" not in nm:
                sc.alpha[nm] = 1.0 if grip_on else 0.0
        cap = "ring" if s["tool"] == "gripper+caps" else ("plate" if s["tool"] == "gripper+plate" else None)
        import ur_arm
        G = ur_arm.gripper_fk(s["close"])
        for kind in ("ring", "plate"):
            for tip in ("left_finger_tip", "right_finger_tip"):
                k = f"{n}/cap/{kind}/{tip}"
                sc.alpha[k] = 1.0 if kind == cap else 0.0
                if kind == cap:
                    sc.gmat[k] = Wt @ G[tip]
        key = self.tool_key(n)
        for k in self.tool_keys[n]:
            sc.alpha[k] = 1.0 if k == key else 0.0
            if k == key:
                sc.gmat[k] = Wt
        # held objects ride on the TCP
        h = s["held"]
        if h is not None:
            T_tcp = a.tcp(s["q"], s["close"])
            Tsp = T_tcp @ rot_axis((0, 0, 1), h["spin_deg"]) if h.get("spin_deg") else T_tcp     # a screw turning with the bit
            for i in h["objs"]:
                if f"o{i}" in sc.actors:
                    sc.gmat[f"o{i}"] = Tsp @ h["off"]
                    sc.alpha[f"o{i}"] = 1.0

    def tool_key(self, n):
        """The actor of arm n's current end effector (made on first use; screwdrivers per bit length)."""
        s = self.st[n]
        t = s["tool"]
        if t.startswith("gripper") or t in ("hand", ""):
            return None
        sp = s.get("spec") or {}
        eb, td = float(sp.get("extra_bit", 0.0) or 0.0), sp.get("tip_d")
        key = f"{n}/tool/{t}/{eb:.0f}/{td}"
        if key not in self.sc.actors:
            try:
                (v, f), _ = self.K.tool_mesh(t, eb, td) if t in ("screwdriver", "nutrunner", "nutrunner_angle") else self.K.tool_mesh(t)
            except Exception as e:     # noqa: BLE001
                print("no tool mesh", t, e)
                return None
            self.sc.add(key, poly(v, f), common.COL["tool"], group=key, specular=0.4, shown=False)
            self.tool_keys[n].append(key)
        return key

    def put(self, objs, T):
        for i in objs:
            if f"o{i}" in self.sc.actors:
                self.sc.gmat[f"o{i}"] = np.asarray(T, float)
                self.sc.alpha[f"o{i}"] = 1.0

    def tcp(self, n):
        a = self.arm[n]
        return a.tcp(self.st[n]["q"], self.st[n]["close"])[:3, 3]

    # ------------------------------------------------------------------------------------------- camera
    def aim(self, focus, shot="mid", side="A", az=None, el=28.0, snap=False):
        side_az = {"A": -62.0, "B": 118.0, "C": -35.0}
        a = math.radians(side_az.get(side, -60.0) if az is None else az)
        R = SHOT.get(shot, shot) if isinstance(shot, str) else float(shot)
        e = math.radians(el)
        focus = np.asarray(focus, float)
        pos = focus + R * np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)])
        if self.cam_pos is None or snap:
            self.cam_pos, self.cam_foc = pos, focus
        else:
            k = 0.18
            self.cam_pos = self.cam_pos * (1 - k) + pos * k
            self.cam_foc = self.cam_foc * (1 - k) + focus * k

    def shot(self):
        self.sc.camera([self.cam_pos, self.cam_foc, (0, 0, 1)], view_angle=32.0)
        return self.sc.render()


# ------------------------------------------------------------------------------------------------ timing
# relative time-lapse weight per event kind inside a step (drives and tool changes go faster than the work itself)
KW = dict(drive=10.0, tool=6.0, plan=1.5, cart=1.0, grip=1.0, screw=1.0, screw_rep=4.0, wait=30.0, turn=1.0, move2=1.0)
# seconds of video a step gets at most (its events are sped up together to fit; never slower than real time)
BUDGET = dict(place=3.6, screws=4.0, seal=10.0, flip=6.0, dual=6.0, rotate=5.0, note=2.5)
CLOSE_STEPS = ("seal",)


def kind_key(e, rep):
    k = e["kind"]
    if k == "move":
        return "plan" if e.get("how") == "plan" else "cart"
    if k == "screw":
        return "screw" if rep == 0 else "screw_rep"
    return k


def plan_frames(events, scale=1.0):
    """Frames per event: each step's events are sped up together so the step fits its budget (BUDGET x scale)."""
    out = {}
    cur, buf = None, []

    def close_step(sid, do, buf):
        if not buf:
            return
        w = sum(float(e.get("dur", 0.0)) / KW.get(kk, 1.0) for e, kk in buf)
        B = BUDGET.get(do, 4.0) * scale
        if do == "screws":
            B = scale * min(10.0, 2.0 + 0.6 * sum(1 for e, kk in buf if e["kind"] == "screw"))
        f = max(1.0, w / max(B, 0.5))
        for e, kk in buf:
            d = float(e.get("dur", 0.0))
            if d <= 0:
                continue
            n = int(round(d * FPS / (KW.get(kk, 1.0) * f)))
            if e["kind"] in ("grip", "tool"):
                n = max(n, 3)
            elif e["kind"] == "wait":
                n = max(n, 18)
            else:
                n = max(n, 2)
            out[id(e)] = (n, d / n)
    reps = {}
    for e in events:
        if e["kind"] == "step":
            close_step(cur[0] if cur else None, cur[1] if cur else None, buf)
            cur, buf = (e["id"], e.get("do")), []
            reps = {}
            continue
        if e.get("dur", 0.0) and e["kind"] in ("move", "drive", "grip", "tool", "screw", "turn", "move2", "wait"):
            r = reps.get(e.get("arm"), 0) if e["kind"] == "screw" else 0
            if e["kind"] == "screw":
                reps[e.get("arm")] = r + 1
            buf.append((e, kind_key(e, r)))
    close_step(cur[0] if cur else None, cur[1] if cur else None, buf)
    return out


def merge_fails(ev, ev_fail, steps):
    """Chapter events with, before each step in `steps`, the failed attempt recorded by an earlier run (status fail)."""
    by = {}
    cur = None
    for e in ev_fail:
        if e["kind"] == "step":
            cur = e["id"]
            if cur in steps:
                by[cur] = [dict(e, failed_run=True)]
            continue
        if cur in by:
            by[cur].append(dict(e, failed_run=True))
    out = []
    for e in ev:
        if e["kind"] == "step" and e["id"] in by:
            out.append(dict(kind="snapshot", step=e["id"]))
            out += by[e["id"]]
            out.append(dict(kind="restore", step=e["id"]))
        out.append(e)
    return out


def run(chapter, max_frames=None, scale=1.0, fail_pkl=None, fail_steps=()):
    rp = Replay(chapter)
    name, title = CHAP[chapter]
    ev = rp.ev
    if fail_pkl and fail_steps:
        ev_f = pickle.load(open(fail_pkl, "rb"))["events"]
        ev = merge_fails(ev, ev_f, set(fail_steps))
    nfr = plan_frames(ev, scale)
    tot_frames = sum(n for n, _ in nfr.values())
    print(f"{name}: {len(ev)} events -> about {tot_frames} frames ({tot_frames / FPS / 60:.1f} min)", flush=True)
    ch = common.Chapter(name, title)
    rows = {}
    for e in ev:
        if e["kind"] == "step_end" and not e.get("failed_run"):
            rows[e["id"]] = e
    cur = dict(id="", label="", status="", actor="A", do="", t=0.0, failed=False)
    tot = dict(n=0)
    snap = {}

    def emit(caption, sub="", who=(), proc=1.0 / FPS, add=None, status=None):
        img = rp.shot()
        st = status if status is not None else cur["status"]
        meta = dict(sub=sub, who=list(who), step=cur["id"], status=st, proc_s=round(proc, 4))
        if add:
            meta["add"] = add
        ch.frame(img, caption, **meta)
        tot["n"] += 1
        cur["t"] += proc
        return max_frames is not None and tot["n"] >= max_frames

    def step_status(sid, failed_run):
        if failed_run:
            return "fail"
        e = rows.get(sid)
        if e is None:
            return ""
        s = e["status"]
        if s == "pass" and sid in fail_steps:
            return "redesign"
        return s

    def lapse_txt(real_per_frame):
        x = real_per_frame * FPS
        return "" if x < 1.3 else f"; x{x:.0f} time-lapse"

    stop = False
    for e in ev:
        if stop:
            break
        k = e["kind"]
        if k == "init":
            for n, a in e["arms"].items():
                if a.get("q") is not None:
                    rp.st[n]["q"] = np.asarray(a["q"], float)
                if a.get("x") is not None:
                    rp.st[n]["x"] = float(a["x"])
                rp.st[n]["tool"] = a.get("tool", "gripper")
                rp.set_arm(n)
            for i, T in e["present"].items():
                rp.put([i], T)
            rp.aim(rp.tcp("A"), "wide", "A", snap=True)
            continue
        if k == "snapshot":
            snap = dict(G={kk: v.copy() for kk, v in rp.sc.gmat.items()}, A={kk: v for kk, v in rp.sc.alpha.items()},
                        st={n: dict(rp.st[n]) for n in ("A", "B")})
            continue
        if k == "restore":
            if snap:
                rp.sc.gmat.update(snap["G"])
                rp.sc.alpha.update(snap["A"])
                for n in ("A", "B"):
                    rp.st[n] = dict(snap["st"][n])
                    rp.set_arm(n)
            continue
        if k == "step":
            failed = bool(e.get("failed_run"))
            label = e["label"]
            if failed:
                label = "[first attempt, round 6 design] " + label
            elif e["id"] in fail_steps:
                label = "[redesigned, round 7] " + label
            cur = dict(id=e["id"], label=label, status=step_status(e["id"], failed), actor=e.get("actor") or "A", do=e.get("do"),
                       t=0.0, failed=failed)
            continue
        if k == "step_end":
            if cur["status"] in ("fail",) or e.get("status") == "fail":
                why = (e.get("row") or {}).get("why") or ""
                for _ in range(int(FPS * 2.5)):
                    stop = emit(cur["label"], f"FAILED: {why[:110]}", [], status="fail")
                    if stop:
                        break
            continue
        n = e.get("arm")
        if n == "A+B":
            n = None
        side = n or cur.get("actor") or "A"
        if side not in ("A", "B"):
            side = "A"
        who = [f"robot {side}"]
        nf, per = nfr.get(id(e), (0, 1.0 / FPS))
        if k == "put":
            rp.put(e["objs"], e["T"])
        elif k == "take":
            for i in e["objs"]:
                if rp.objs.get(i, {}).get("kind") == "tool" and f"o{i}" in rp.sc.actors:
                    rp.sc.alpha[f"o{i}"] = 0.0         # a hand tool goes back to the stand
        elif k == "attach":
            rp.st[n]["held"] = dict(objs=e["objs"], off=np.asarray(e["off"], float))
            rp.set_arm(n)
        elif k == "detach":
            rp.st[n]["held"] = None
        elif k == "tool":
            rp.st[n]["spec"] = e.get("spec") or {}
            rp.set_arm(n, tool=e["tool"])
            for f in range(nf):
                rp.aim(rp.tcp(n), "mid", side)
                stop = emit(cur["label"], f"tool change at the MiR's stand: {e['tool']} (ATI QC-21; {e['dur']:.0f} s, estimate)",
                            who, proc=per, add={"robot_h": per / 3600.0})
                if stop:
                    break
        elif k == "grip":
            for f in range(nf):
                s = smooth((f + 1) / nf)
                rp.set_arm(n, close=e["c0"] + (e["c1"] - e["c0"]) * s)
                rp.aim(rp.tcp(n), "close" if cur["do"] in CLOSE_STEPS else "mid", side)
                stop = emit(cur["label"], "2F-85 " + ("closes" if e["c1"] > e["c0"] else "opens"), who, proc=per,
                            add={"robot_h": per / 3600.0})
                if stop:
                    break
        elif k == "drive":
            for f in range(nf):
                s = smooth((f + 1) / nf)
                x = e["x0"] + (e["x1"] - e["x0"]) * s
                rp.set_arm(n, x=x)
                rp.aim(np.array([x, (-1 if n == "A" else 1) * 500.0, 950.0]), "wide", side, el=22.0)
                chk = e.get("check") or {}
                sub = (f"MiR {n} drives {abs(e['x1'] - e['x0']) / 1000:.1f} m "
                       + ("to the parts table" if e["x1"] > 2000 else "back to the bench")
                       + f" ({e['dur']:.0f} s at 0.3 m/s2, 1 m/s{lapse_txt(per)})")
                if chk and not chk.get("ok", True):
                    sub += f"; sweep: {chk.get('why', '')[:50]}"
                stop = emit(cur["label"], sub, who, proc=per, add={"robot_h": per / 3600.0})
                if stop:
                    break
        elif k in ("move", "screw"):
            Q = e.get("q")
            if Q is None or len(Q) == 0:
                if k == "screw":
                    for _ in range(int(FPS * 1.0)):
                        stop = emit(cur["label"], f"screw not driven: {e.get('why', '')[:90]}", who, status="fail")
                continue
            Q = np.asarray(Q, float)
            d = np.r_[0.0, np.cumsum(np.abs(np.diff(Q, axis=0)).max(axis=1))] if len(Q) > 1 else np.array([0.0])
            L = d[-1] if d[-1] > 0 else 1.0
            in_table = rp.st[n]["x"] > 2000.0
            for f in range(nf):
                s = smooth((f + 1) / nf) * L
                if len(Q) > 1:
                    j = int(min(max(np.searchsorted(d, s, side="right") - 1, 0), len(Q) - 2))
                    t = (s - d[j]) / max(d[j + 1] - d[j], 1e-9)
                    q = Q[j] * (1 - t) + Q[j + 1] * t
                else:
                    q = Q[0]
                if k == "screw" and rp.st[n]["held"] is not None:
                    # the screw turns with the bit as it runs down: one turn per pitch (drawn at most 2 turns a frame)
                    turns = e["L"] / max(e["pitch"], 0.1)
                    rp.st[n]["held"]["spin_deg"] = (360.0 * min(turns * (f + 1) / nf, 2.0 * (f + 1))) % 360.0
                rp.set_arm(n, q=q, close=e.get("close"))
                if k == "screw":
                    shot = "close"
                elif in_table:
                    shot = "mid"
                elif e.get("how") == "cart" or cur["do"] in CLOSE_STEPS:
                    shot = "close"
                else:
                    shot = "mid"
                rp.aim(rp.tcp(n), shot, side)
                if k == "screw":
                    msz = {0.5: 3, 0.7: 4, 0.8: 5, 1.0: 6}.get(round(float(e.get("pitch", 0.7)), 1), "")
                    sub = (f"{e['tool']}: M{msz} screw runs down {e['L']:.0f} mm and is torqued to {float(e.get('torque') or 0):.1f} N m "
                           f"({e['dur']:.0f} s{lapse_txt(per)})")
                elif in_table and e.get("how") == "cart":
                    sub = "pick at the parts table (checked against the table, its nest and the neighbouring parts)"
                elif e.get("how") == "plan":
                    sub = f"planned move, collision-checked{lapse_txt(per)}"
                else:
                    sub = "checked straight-line move" + (" with the part" if e.get("held") else "") + lapse_txt(per)
                stop = emit(cur["label"], sub, who, proc=per, add={"robot_h": per / 3600.0})
                if stop:
                    break
        elif k == "move2":
            QA, QB = np.asarray(e["qA"], float), np.asarray(e["qB"], float)
            for f in range(nf):
                j = min(len(QA) - 1, int(round(smooth((f + 1) / nf) * (len(QA) - 1))))
                rp.set_arm("A", q=QA[j], close=e["closeA"])
                rp.set_arm("B", q=QB[j], close=e["closeB"])
                mid = 0.5 * (rp.tcp("A") + rp.tcp("B"))
                rp.aim(mid, "mid", "C")
                if e.get("lift_aid"):
                    rp.sc.alpha["hoist"] = 1.0
                    rp.sc.gmat["hoist"] = Tm((float(mid[0]), float(mid[1]), float(mid[2]) + 60.0))
                    stop = emit(cur["label"], f"a small hoist takes the load (person at its pendant); both arms guide it along the checked path"
                                f"{lapse_txt(per)}", ["robot A", "robot B", "person"], proc=per,
                                add={"robot_h": 2 * per / 3600.0, "person_h": per / 3600.0})
                else:
                    stop = emit(cur["label"], f"both arms carry it together, checked frame by frame{lapse_txt(per)}", ["robot A", "robot B"],
                                proc=per, add={"robot_h": 2 * per / 3600.0})
                if stop:
                    break
            rp.sc.alpha["hoist"] = 0.0
        elif k == "turn":
            T0 = np.asarray(e["T0"], float)
            TT = np.asarray(e["TT"], float)
            J0 = rp.sc.gmat["jaws"].copy()
            for f in range(nf):
                th = e["sign"] * 180.0 * smooth((f + 1) / nf)
                Rm = TT @ rot_axis((1, 0, 0), th) @ np.linalg.inv(TT)
                rp.put(e["objs"], Rm @ T0)
                rp.sc.gmat["jaws"] = Rm @ J0
                rp.aim(TT[:3, 3], "mid", "A", az=-50.0)
                stop = emit(cur["label"], "the trunnion turns the chamber over; both arms parked", ["machine"], proc=per)
                if stop:
                    break
        elif k == "wait":
            wh = e.get("who", "person")
            if wh == "person" and rp.person is not None:
                rp.person.show(1.0)
                xp = -1900.0 if cur["id"].startswith("M") else 900.0
                rp.person.set(x=xp, y=-1150.0, hd=90.0, amp=0.0, look=(xp, -200.0, 950.0))
            foc = np.array([-1300.0 if cur["id"].startswith("M") else 700.0, -500.0, 1000.0])
            for f in range(nf):
                rp.aim(foc, "mid", "A")
                sub = (f"{e.get('what', '')[:80]} ({e['dur'] / 60:.0f} min, estimate{lapse_txt(per)})" if wh == "person" else
                       f"{e.get('what', '')[:80]} ({e['dur']:.0f} s)")
                stop = emit(cur["label"], sub, [wh] if wh in ("person", "machine") else ["robot A"], proc=per,
                            add={"person_h": per / 3600.0} if wh == "person" else ({"robot_h": per / 3600.0} if wh == "robot" else None),
                            status="person" if wh == "person" else None)
                if stop:
                    break
            if rp.person is not None:
                rp.person.show(0.0)
    ch.close()
    print(f"{name}: {tot['n']} frames ({tot['n'] / FPS / 60:.1f} min)", flush=True)
    return tot


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = {a.split("=")[0][2:]: (a.split("=", 1)[1] if "=" in a else "1") for a in sys.argv[1:] if a.startswith("--")}
    run(args[0] if args else "module", max_frames=int(opt["max"]) if "max" in opt else None, scale=float(opt.get("scale", 1.0)),
        fail_pkl=opt.get("fails"), fail_steps=tuple(x for x in opt.get("fail_steps", "").split(",") if x))
