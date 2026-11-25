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
        self.tool_act = {}
        for n in ("A", "B"):
            for t in ("screwdriver", "nutrunner", "nutrunner_angle", "vacuum", "nozzle", "roller", "roller_n"):
                try:
                    (v, f), _ = K.tool_mesh(t)
                except Exception:      # noqa: BLE001
                    continue
                sc.add(f"{n}/tool/{t}", poly(v, f), common.COL["tool"], group=f"{n}/tool/{t}", specular=0.4, shown=False)
            self.caps = {}
        # hand tools held in the gripper (temporary objects in the run) are among self.objs
        # ---- the trunnion's jaws
        import tooling as TL
        (v, f), _ = TL.mesh("trunnion_jaws")
        sc.add("jaws", poly(v, f), "#d18a1f", group="jaws", specular=0.3)
        self.TT = Tm((K.STATIONS["T"], 0.0, TL.TRUNNION["h_axis"]))
        sc.gmat["jaws"] = self.TT
        self.jaw = 0.0
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
        if tool is not None and tool != s["tool"]:
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
        grip_on = s["tool"].startswith("gripper") or s["tool"] in ("gripper+caps", "gripper+plate", "hand")
        for nm in self.vis[n].names():
            if "/gr/" in nm and "camera" not in nm:
                sc.alpha[nm] = 1.0 if grip_on else 0.0
        for t in ("screwdriver", "nutrunner", "nutrunner_angle", "vacuum", "nozzle", "roller", "roller_n"):
            k = f"{n}/tool/{t}"
            if k in sc.actors:
                sc.alpha[k] = 1.0 if s["tool"] == t else 0.0
                sc.gmat[k] = Wt
        # held objects ride on the TCP
        h = s["held"]
        if h is not None:
            T_tcp = a.tcp(s["q"], s["close"])
            for i in h["objs"]:
                if f"o{i}" in sc.actors:
                    M = T_tcp @ h["off"] @ h.get("pose", {}).get(i, np.eye(4))
                    if h.get("spin") is not None:
                        M = M @ h["spin"].get(i, np.eye(4))
                    sc.gmat[f"o{i}"] = M
                    sc.alpha[f"o{i}"] = 1.0

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


def run(chapter, max_frames=None, budget_s=None):
    rp = Replay(chapter)
    name, title = CHAP[chapter]
    ch = common.Chapter(name, title)
    steps = {}
    rows = {}
    # the step table (status, why) from the events
    for e in rp.ev:
        if e["kind"] == "step_end":
            rows[e["id"]] = e
    cur = dict(id="", label="", status="", actor="A")
    tot = dict(robot_s=0.0, person_s=0.0, n=0)
    screws_seen = {}

    def emit(caption, sub="", who=(), proc=1.0 / FPS, add=None, status=None):
        img = rp.shot()
        meta = dict(sub=sub, who=list(who), step=cur["id"], status=status if status is not None else cur["status"], proc_s=round(proc, 4))
        if add:
            meta["add"] = add
        ch.frame(img, caption, **meta)
        tot["n"] += 1
        return max_frames is not None and tot["n"] >= max_frames

    def status_of(sid):
        e = rows.get(sid)
        return "" if e is None else e["status"]

    def focus_for(n):
        p = rp.tcp(n)
        return p

    stop = False
    for e in rp.ev:
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
            rp.aim(focus_for("A"), "wide", "A", snap=True)
            continue
        if k == "step":
            cur = dict(id=e["id"], label=e["label"], status=status_of(e["id"]), actor=e.get("actor") or "A", do=e.get("do"))
            continue
        if k == "step_end":
            continue
        n = e.get("arm")
        if n == "A+B":
            n = None
        side = n or cur.get("actor") or "A"
        if side not in ("A", "B"):
            side = "A"
        who = [f"robot {side}"] if k not in ("wait", "turn") else []
        dur = float(e.get("dur", 0.0))
        if k == "put":
            rp.put(e["objs"], e["T"])
        elif k == "attach":
            h = dict(objs=e["objs"], off=np.asarray(e["off"], float))
            rp.st[n]["held"] = h
            rp.set_arm(n)
        elif k == "detach":
            rp.st[n]["held"] = None
        elif k == "tool":
            rp.set_arm(n, tool=e["tool"])
            if dur > 0:
                for f in range(max(1, int(round(dur * FPS / rp.lapse["tool"])))):
                    rp.aim(focus_for(n), "mid", side)
                    stop = emit(cur["label"], f"tool change at the MiR's tool stand: {e['tool']} (ATI QC-21; {dur:.0f} s, estimate)",
                                who, proc=rp.lapse["tool"] / FPS, add={"robot_h": rp.lapse["tool"] / FPS / 3600.0})
                    if stop:
                        break
        elif k == "grip":
            nf = max(2, int(round(dur * FPS)))
            for f in range(nf):
                s = smooth((f + 1) / nf)
                rp.set_arm(n, close=e["c0"] + (e["c1"] - e["c0"]) * s)
                rp.aim(focus_for(n), "close", side)
                stop = emit(cur["label"], "2F-85 " + ("closes" if e["c1"] > e["c0"] else "opens"), who, add={"robot_h": 1.0 / FPS / 3600.0})
                if stop:
                    break
        elif k == "drive":
            lap = rp.lapse["drive"]
            nf = max(2, int(round(dur * FPS / lap)))
            for f in range(nf):
                s = smooth((f + 1) / nf)
                x = e["x0"] + (e["x1"] - e["x0"]) * s
                rp.set_arm(n, x=x)
                foc = np.array([x, (-1 if n == "A" else 1) * 640.0, 900.0])
                rp.aim(foc, "wide", side, el=24.0)
                chk = e.get("check") or {}
                sub = f"MiR {n} drives {abs(e['x1'] - e['x0']) / 1000:.1f} m along its lane ({dur:.0f} s at 1 m/s; x{lap:.0f} time-lapse)"
                if chk and not chk.get("ok", True):
                    sub += f"; sweep: {chk.get('why', '')[:60]}"
                stop = emit(cur["label"], sub, who, proc=lap / FPS, add={"robot_h": lap / FPS / 3600.0})
                if stop:
                    break
        elif k in ("move", "screw"):
            Q = e.get("q")
            if Q is None or len(Q) == 0:
                if k == "screw":
                    stop = emit(cur["label"], f"screw {e.get('obj')}: no collision-free way to drive it ({e.get('why', '')[:70]})",
                                who, status="fail")
                continue
            Q = np.asarray(Q, float)
            if k == "screw":
                key = (cur["id"], n)
                rep = screws_seen.get(key, 0)
                screws_seen[key] = rep + 1
                lap = rp.lapse["screw"] if rep == 0 else rp.lapse["screw_rep"]
            else:
                lap = rp.lapse["plan"] if e.get("how") == "plan" else rp.lapse["cart"]
            nf = max(2, int(round(dur * FPS / lap)))
            # resample Q by arc length in joint space
            d = np.r_[0.0, np.cumsum(np.abs(np.diff(Q, axis=0)).max(axis=1))]
            L = d[-1] if d[-1] > 0 else 1.0
            for f in range(nf):
                s = smooth((f + 1) / nf) * L
                j = int(np.searchsorted(d, s, side="right") - 1)
                j = min(max(j, 0), len(Q) - 2) if len(Q) > 1 else 0
                if len(Q) > 1:
                    t = (s - d[j]) / max(d[j + 1] - d[j], 1e-9)
                    q = Q[j] * (1 - t) + Q[j + 1] * t
                else:
                    q = Q[0]
                if k == "screw" and rp.st[n]["held"] is not None:
                    # the screw turns with the bit as it advances: one turn per pitch
                    ang = 360.0 * (f + 1) / nf * (e["L"] / max(e["pitch"], 0.1))
                    rp.st[n]["held"]["spin"] = {}
                rp.set_arm(n, q=q, close=e.get("close"))
                shot = "close" if (k == "screw" or e.get("how") == "cart") else "mid"
                rp.aim(focus_for(n), shot, side)
                if k == "screw":
                    sub = (f"{e['tool']}: M{'' if not e.get('pitch') else {0.5: 3, 0.7: 4, 0.8: 5, 1.0: 6}.get(round(e['pitch'], 1), '')} screw "
                           f"advances {e['L']:.0f} mm, then {e['torque'] or 0:.1f} N m ({dur:.0f} s"
                           + (f"; x{lap:.0f} time-lapse)" if lap > 1 else ")"))
                elif e.get("how") == "plan":
                    sub = "planned move (RRT-Connect / straight joint line, collision-checked)" + (f" x{lap:.1f}" if lap > 1 else "")
                else:
                    sub = "checked straight-line move" + (" carrying the part" if e.get("held") else "")
                stop = emit(cur["label"], sub, who, proc=lap / FPS, add={"robot_h": lap / FPS / 3600.0})
                if stop:
                    break
        elif k == "move2":
            QA, QB = np.asarray(e["qA"], float), np.asarray(e["qB"], float)
            lap = rp.lapse["move2"]
            nf = max(2, int(round(dur * FPS / lap)))
            for f in range(nf):
                j = min(len(QA) - 1, int(round(smooth((f + 1) / nf) * (len(QA) - 1))))
                rp.set_arm("A", q=QA[j], close=e["closeA"])
                rp.set_arm("B", q=QB[j], close=e["closeB"])
                foc = 0.5 * (rp.tcp("A") + rp.tcp("B"))
                rp.aim(foc, "mid", "C")
                stop = emit(cur["label"], "both arms carry it together (checked frame by frame)", ["robot A", "robot B"], proc=lap / FPS,
                            add={"robot_h": 2 * lap / FPS / 3600.0})
                if stop:
                    break
        elif k == "turn":
            lap = rp.lapse["turn"]
            nf = max(2, int(round(dur * FPS / lap)))
            T0 = np.asarray(e["T0"], float)
            TT = np.asarray(e["TT"], float)
            for f in range(nf):
                th = e["sign"] * 180.0 * smooth((f + 1) / nf)
                Rm = TT @ rot_axis((1, 0, 0), th) @ np.linalg.inv(TT)
                rp.put(e["objs"], Rm @ T0)
                rp.sc.gmat["jaws"] = Rm @ rp.sc.gmat.get("jaws_base", rp.TT) if "jaws_base" in rp.sc.gmat else Rm @ rp.TT
                rp.aim(TT[:3, 3], "mid", "A", az=-50.0)
                stop = emit(cur["label"], "the trunnion turns the chamber over (both arms parked)", ["machine"], proc=lap / FPS)
                if stop:
                    break
            rp.sc.gmat["jaws_base"] = rp.sc.gmat["jaws"] @ np.linalg.inv(rp.TT) @ rp.TT
        elif k == "wait":
            lap = rp.lapse["wait"] if dur > 60 else 1.0
            nf = max(6, int(round(dur * FPS / lap)))
            wh = e.get("who", "person")
            if wh == "person" and rp.person is not None:
                rp.person.show(1.0)
                rp.person.set(x=-1900.0 if cur["id"].startswith("M") else 900.0, y=-1250.0, hd=90.0, amp=0.0)
            for f in range(nf):
                rp.aim(np.array([-1300.0 if cur["id"].startswith("M") else 700.0, -300.0, 1000.0]), "mid", "A")
                stop = emit(cur["label"], f"{e.get('what', '')[:80]} ({dur / 60:.0f} min, estimate; x{lap:.0f})" if wh == "person" else
                            e.get("what", "")[:90], [wh] if wh in ("person", "machine") else ["robot A"], proc=lap / FPS,
                            add={"person_h": lap / FPS / 3600.0} if wh == "person" else None,
                            status="person" if wh == "person" else None)
                if stop:
                    break
            if rp.person is not None:
                rp.person.show(0.0)
        # jumps, marks, takes: no frames
    ch.close()
    print(f"{name}: {tot['n']} frames ({tot['n'] / FPS / 60:.1f} min)")
    return tot


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mx = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--max=")), None)
    run(args[0] if args else "module", max_frames=mx)
