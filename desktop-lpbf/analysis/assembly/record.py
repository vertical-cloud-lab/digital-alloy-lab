"""Trajectory recorder for the two-arm build (run_assembly.py with ASM_RECORD=<dir>), round 7 (issue #260, PR #266).

Sterling, 2026-11-25: the assembly shown being carried out **by** two UR12e on MiR250s, with every part fetched from the
long table. run_assembly.py tries several docks, rolls and tools per step and keeps the best; this module records only
the committed motion, in order, so a renderer can replay the build frame by frame:

  move    one arm's joint vectors (n x 6) along a checked Cartesian path or a planned joint path (RRT-Connect / straight)
  drive   one MiR's x along its lane (the arm parked; anything it holds rides along), MiR250: 0.3 m/s^2, 1.0 m/s
  grip    the 2F-85 closing or opening (close fraction)
  tool    a tool change at the MiR's tool stand (ATI QC-21): gripper, screwdriver, nutrunner, vacuum, nozzle, roller
  attach  objects (run's object indices) start riding on an arm: off = TCP -> the sub-assembly's machine frame, state
  detach  objects let go, left at a world pose
  put     objects placed (world pose of their machine frame) without an arm: the starting table, merges, the trunnion
  turn    the trunnion's jaws and the chamber turning about x (degrees per frame)
  screw   a screw driven: the arm's frames along the rundown, the screw advancing with the bit, the torque
  step    a step marker (id, label, who, status, sub) and per-step totals
Real time: every event gets a duration from the motion and the speeds below (labelled estimates where not computed). The
renderer samples the stream at its own rate (real time 1/12 s a frame, or a time-lapse).

Speeds and times (estimates, cobot practice; not measured on this cell):
  joint moves     <= 60 deg/s per joint (a third of the UR12e's 180 deg/s wrist limit) and <= 250 mm/s at the TCP,
                  plus 0.4 s to accelerate and stop
  insertions      50 mm/s along the checked Cartesian path, 10 mm/s for the last 10 mm
  screw rundown   the thread length at 300 rpm (pitch x 5 per s), then 1.0 s torque and hold (screwdriver controllers)
  gripper         0.8 s to close or open (2F-85 at 150 mm/s over ~40 mm, plus settling)
  tool change     8 s (to the stand on the MiR, unlock, lock, back): estimate
  MiR drive       trapezoid at 0.3 m/s^2 and 1.0 m/s (MiR250 datasheet), plus 6 s to dock at a marker: estimate
"""
from __future__ import annotations

import math
import os
import pathlib
import pickle
import time

import numpy as np

V_JOINT = math.radians(60.0)
V_TCP = 250.0
V_INSERT, V_SEAT = 50.0, 10.0
T_RAMP = 0.4
T_GRIP = 0.8
T_TOOL = 8.0
MIR_A, MIR_V, T_DOCK = 300.0, 1000.0, 6.0          # mm/s^2, mm/s, s
SCREW_RPM = 300.0
T_TORQUE = 1.0


def drive_time(d_mm):
    d = abs(float(d_mm))
    if d < 1e-6:
        return 0.0
    d_acc = MIR_V ** 2 / MIR_A                        # accelerate and brake: 3.33 m at 1 m/s
    if d >= d_acc:
        return d / MIR_V + MIR_V / MIR_A + T_DOCK
    return 2.0 * math.sqrt(d / MIR_A) + T_DOCK


def joint_time(qs, tcp=None, cart=False, seat_mm=0.0):
    """Seconds for a joint path qs (n x 6); tcp (n x 3) for the Cartesian speed limit; cart: an insertion (50 mm/s)."""
    qs = np.asarray(qs, float)
    if len(qs) < 2:
        return 0.0
    dq = np.abs(np.diff(qs, axis=0)).max(axis=1)
    t_j = float(dq.sum() / V_JOINT)
    t_c = 0.0
    if tcp is not None:
        d = np.linalg.norm(np.diff(np.asarray(tcp, float), axis=0), axis=1)
        L = float(d.sum())
        if cart:
            s = min(seat_mm, L)
            t_c = (L - s) / V_INSERT + s / V_SEAT
        else:
            t_c = L / V_TCP
    return max(t_j, t_c) + T_RAMP


class Rec:
    def __init__(self, out_dir, run):
        self.dir = pathlib.Path(out_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.run = run
        self.events = []
        self.chapter = None
        self.state = {n: dict(q=None, x=None, tool="gripper", close=0.0, held=None) for n in ("A", "B")}
        self.step = None
        self.steps = []
        self.t0 = time.time()

    # ---------------------------------------------------------------- bookkeeping
    def _ev(self, kind, **kw):
        kw["kind"] = kind
        if getattr(self, "mute", False):        # a fast-forwarded step (run_assembly ASM_FF_UNTIL): nothing is recorded
            return kw
        kw["step"] = self.step["id"] if self.step else ""
        self.events.append(kw)
        if self.step is not None:
            self.step["t"] += float(kw.get("dur", 0.0))
            who = kw.get("arm")
            if who in ("A", "B") and kw.get("dur"):
                self.step["robot_s"][who] += float(kw["dur"])
        return kw

    def begin(self, st, chapter):
        if chapter != self.chapter:
            self.flush()
            self.chapter = chapter
            # the chapter starts from the arms' current state
            self.events.append(dict(kind="init", step=st["id"], arms={n: dict(self.state[n], q=None if self.state[n]["q"] is None else
                                                                               list(map(float, self.state[n]["q"])))
                                                                        for n in ("A", "B")},
                                    present=self.present()))
        self.step = dict(id=st["id"], label=st.get("label", ""), do=st.get("do"), who=[], t=0.0, robot_s={"A": 0.0, "B": 0.0},
                         person_s=0.0, status="", notes=[])
        self._ev("step", id=st["id"], label=st.get("label", ""), do=st.get("do"), actor=st.get("actor"), dur=0.0)

    def end(self, row):
        if self.step is None:
            return
        s = self.step
        arm = str(row.get("arm", ""))
        if row.get("do") == "note":
            who = row.get("who") or ""
            s["status"] = "person" if "person" in who else ("machine" if "machine" in who else "robot")
            s["who"] = ["person"] if "person" in who else ["machine"] if "machine" in who else ["robot A"]
            s["person_s"] = max(s["person_s"], float(row.get("person_s", 0.0) or 0.0))   # the wait event already counted it
        else:
            s["status"] = "pass" if arm in ("PASS", "-") and str(row.get("sweep", "PASS")) in ("PASS", "-", "?") else \
                ("fail" if arm in ("FAIL", "ERROR", "PART") or str(row.get("sweep")) == "FAIL" else "pass")
            s["who"] = [f"robot {n}" for n in ("A", "B") if s["robot_s"][n] > 0.0] + (["person"] if s["person_s"] > 0.0 else [])
        s["why"] = str(row.get("why", ""))[:300]
        s["fetch"] = row.get("fetch")
        self._ev("step_end", id=s["id"], status=s["status"], dur=0.0, row={k: row.get(k) for k in
                                                                            ("sweep", "arm", "why", "gap", "arm_clear", "n", "n_ok",
                                                                             "driver", "fetch", "fetch_why", "who", "method")})
        self._dump_chunk()
        self.steps.append(dict(id=s["id"], label=s["label"], do=s["do"], who=s["who"], seconds=round(s["t"], 1),
                               robot_A_s=round(s["robot_s"]["A"], 1), robot_B_s=round(s["robot_s"]["B"], 1),
                               person_s=round(s["person_s"], 1), status=s["status"], why=s["why"][:200], chapter=self.chapter,
                               fetch=s.get("fetch")))
        self.step = None

    def present(self):
        cl = self.run.cl
        return {int(i): np.asarray(cl.where[i], float).copy() for i in cl.where}

    # ---------------------------------------------------------------- motion
    def _tcp(self, n, qs, close=None):
        a = self.run.arm(n)
        return np.array([a.tcp(q, close)[:3, 3] for q in qs])

    def move(self, n, qs, kind="plan", close=None, seat_mm=0.0, densify=True):
        """A committed joint path of arm n (a planned path's waypoints are densified at 1.5 deg)."""
        if qs is None or len(qs) == 0:
            return
        qs = [np.asarray(q, float) for q in qs]
        if densify and kind == "plan" and len(qs) >= 2:
            import cell as C
            qs = C.densify(qs, math.radians(2.0))
        st = self.state[n]
        if st["q"] is not None and np.abs(qs[0] - st["q"]).max() > 1e-3:
            # not continuous with what was recorded: say so (the renderer cuts here)
            self._ev("jump", arm=n, frm=list(map(float, st["q"])), to=list(map(float, qs[0])), dur=0.0)
        close = st["close"] if close is None else float(close)
        Q = np.array(qs)
        tcp = self._tcp(n, Q, close)
        dur = joint_time(Q, tcp, cart=(kind != "plan"), seat_mm=seat_mm)
        self._ev("move", arm=n, q=Q.astype(np.float32), close=close, how=kind, dur=round(dur, 2),
                 held=None if st["held"] is None else st["held"]["name"])
        st["q"] = Q[-1].copy()

    def drive(self, n, x1, check=None, route=None):
        """route (round 8, mir_route.plan): the legs (pivot / line, each with its duration) the MiR drives, pivot-drive-pivot;
        None: no route was found, so the renderer must not animate this move (it cuts, and says so)."""
        st = self.state[n]
        x0 = st["x"]
        st["x"] = float(x1)
        if x0 is None or abs(float(x1) - x0) < 1e-6:
            return
        dur = (float(route["dur"]) + T_DOCK) if route else drive_time(x1 - x0)
        self._ev("drive", arm=n, x0=float(x0), x1=float(x1), dur=round(dur, 2), check=check, route=route,
                 held=None if st["held"] is None else st["held"]["name"])

    def set_x(self, n, x):
        if self.state[n]["x"] is None:
            self.state[n]["x"] = float(x)

    def grip(self, n, close):
        st = self.state[n]
        if abs(float(close) - st["close"]) < 1e-4:
            return
        self._ev("grip", arm=n, c0=float(st["close"]), c1=float(close), dur=T_GRIP)
        st["close"] = float(close)

    def tool(self, n, name, spec=None):
        st = self.state[n]
        key = (name, tuple(sorted((spec or {}).items())))
        if st.get("tool_key") == key:
            return
        first = st.get("tool_key") is None
        st["tool"], st["tool_key"] = name, key
        self._ev("tool", arm=n, tool=name, spec=dict(spec or {}), dur=0.0 if first else T_TOOL)

    def attach(self, n, objs, off, state=None, name="", T_world=None):
        self.state[n]["held"] = dict(objs=[int(i) for i in objs], name=name)
        self._ev("attach", arm=n, objs=[int(i) for i in objs], off=np.asarray(off, float), state=dict(state or {}), name=name, dur=0.0)

    def detach(self, n, T_world=None):
        h = self.state[n]["held"]
        if h is None:
            return
        self.state[n]["held"] = None
        self._ev("detach", arm=n, objs=h["objs"], T=None if T_world is None else np.asarray(T_world, float), dur=0.0)

    def put(self, idx, T, state=None, why=""):
        self._ev("put", objs=[int(i) for i in idx], T=np.asarray(T, float), state=dict(state or {}), why=why, dur=0.0)

    def take(self, idx):
        self._ev("take", objs=[int(i) for i in idx], dur=0.0)

    def turn(self, objs, T0, TT, sign, n=37, extra=None):
        dur = 180.0 / 30.0 + 2.0                       # 30 deg/s on the positioner, plus clamping: estimate
        self._ev("turn", objs=[int(i) for i in objs], T0=np.asarray(T0, float), TT=np.asarray(TT, float), sign=float(sign), n=n,
                 dur=round(dur, 1), extra=extra)

    def screw(self, n, i, qs, L, pitch, torque, tool, ok, why=""):
        Q = np.array([np.asarray(q, float) for q in qs]) if qs is not None and len(qs) else None
        t_run = (L / max(pitch * SCREW_RPM / 60.0, 0.1)) if L else 0.0
        dur = t_run + T_TORQUE
        self._ev("screw", arm=n, obj=int(i), q=None if Q is None else Q.astype(np.float32), L=float(L or 0.0), pitch=float(pitch),
                 torque=torque, tool=tool, ok=bool(ok), why=why[:120], dur=round(dur, 2))
        if Q is not None:
            self.state[n]["q"] = Q[-1].copy()

    def wait(self, dur, who="person", what=""):
        self._ev("wait", who=who, what=what, dur=float(dur))
        if self.step is not None and who == "person":
            self.step["person_s"] += float(dur)

    def mark(self, what, **kw):
        self._ev("mark", what=what, dur=0.0, **kw)

    # ---------------------------------------------------------------- output
    def _dump_chunk(self):
        """Round 8: after every step, the chapter's new events go to asm_<chapter>.chunk<k>.pkl, so the renderer can draw the
        steps already planned while the planner works on the rest (asm_render.py reads the chunks when the full file is absent)."""
        if self.chapter is None:
            return
        k0 = getattr(self, "_dumped", 0)
        if k0 >= len(self.events):
            return
        n = getattr(self, "_chunk_n", 0)
        f = self.dir / f"asm_{self.chapter}.chunk{n:04d}.pkl"
        tmp = f.with_suffix(".tmp")
        pickle.dump(dict(chapter=self.chapter, events=self.events[k0:]), open(tmp, "wb"))
        tmp.rename(f)
        self._dumped, self._chunk_n = len(self.events), n + 1

    def flush(self):
        self._dumped, self._chunk_n = 0, 0
        if self.chapter is None or not self.events:
            self.events = []
            return
        f = self.dir / f"asm_{self.chapter}.pkl"
        pickle.dump(dict(chapter=self.chapter, events=self.events, made=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                         speeds=dict(V_JOINT_deg_s=60.0, V_TCP=V_TCP, V_INSERT=V_INSERT, V_SEAT=V_SEAT, T_GRIP=T_GRIP, T_TOOL=T_TOOL,
                                     MIR_A=MIR_A, MIR_V=MIR_V, T_DOCK=T_DOCK, SCREW_RPM=SCREW_RPM)),
                    open(f, "wb"))
        self.events = []

    def save_summary(self, path):
        import json
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        tot_r = sum(s["robot_A_s"] + s["robot_B_s"] for s in self.steps)
        tot_p = sum(s["person_s"] for s in self.steps)
        p.write_text(json.dumps(dict(
            note="Real-world time per assembly step (issue #260, round 7): robot motion from the recorded, collision-checked "
                 "trajectories at the speeds in analysis/assembly/record.py (estimates where marked there: tool changes 8 s, "
                 "MiR docking 6 s, screw torque phase 1 s, gripper 0.8 s); persons' times are estimates per step. 'seconds' is "
                 "the step's elapsed time (both arms can work at once, so robot_A_s + robot_B_s can exceed it).",
            robot_h=round(tot_r / 3600.0, 2), person_h=round(tot_p / 3600.0, 2), steps=self.steps), indent=1))


REC = None


def start(run):
    global REC
    d = os.environ.get("ASM_RECORD")
    if d:
        REC = Rec(d, run)
    return REC
