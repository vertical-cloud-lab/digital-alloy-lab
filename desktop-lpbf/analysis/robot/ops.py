"""Every tending job of the desktop LPBF, done by a UR12e (the UR10e, renamed) + Robotiq 2F-85 on a MiR250, simulated the way
byu-vcl PR 318 simulates its cell (round 14, commit 11d4410): FCL on the meshes as drawn (cell.py), every IK branch tried nearest
first, the straight joint line or else RRT-Connect (1.5 deg edges, shortcut), Cartesian lines for the approaches and the work itself,
and every frame audited: the gripper, its tools and a held part may touch the part being handled and that part's fixtures only up
to 1.5 mm deep; anything else the arm, the gripper, a tool or a held part touches is a collision at any depth; and everything else
that moves (doors, drawer, wings, reservoir, plate, module) is checked against everything else every frame ("movers").

Per job it reports pass/fail and the step that fails, the tightest clearance (FCL distance from the robot and what it holds to
everything it may not touch), peak static joint torque against the UR12e's limits, the forces the job needs against the arm's force
mode (100 N, Edison r3-robot-tending: UR10e spec) and PFL limits (50-250 N, UR safety configuration), the MiR250's tip-over margin
with PR 318's 131 kg ballast (PR 318's alloy_atomize.stability(), ported), and an estimated cycle time.

Run (one command; it rebuilds the model from cad/lpbf_low.py, so it re-runs on whatever the model is now):
    OMP_NUM_THREADS=1 /tmp/capmem 3 python desktop-lpbf/analysis/robot/ops.py                    # every job, M50 (+ S25, L75 for plate/module)
    python desktop-lpbf/analysis/robot/ops.py --jobs plate_drawbar --modules S25,M50,L75 --render
Writes analysis/out/robot/ops.json, ops.md, and with --render ops_<job>_<module>.gif (<= 60 frames, 480 px) and _tightest.png.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import cell as C  # noqa: E402
import eoat as E  # noqa: E402

OUT = HERE.parent / "out" / "robot"
REGION = ((-480.0, 730.0), (-600.0, 260.0), (-262.0, 420.0))
DEG = math.pi / 180.0

# timing (estimates, for the cycle time): joint moves at 60 deg/s on the largest joint, free lines at 150 mm/s, fine lines
# (in the chamber, in contact) at 30 mm/s, a grip or release 0.8 s, wrist twists at 45 deg/s
T_JOINT = 60.0 * DEG
V_FREE, V_FINE = 150.0, 30.0
T_GRIP = 0.8
FORCE_MODE_N = 100.0           # UR10e/UR12e force mode, Edison r3-robot-tending (UR10e spec: up to 100 N, accuracy 5.5 N)
PFL_N = (50.0, 250.0)          # UR safety configuration: force limit settable 50-250 N
GRIP_N = (20.0, 235.0)         # 2F-85 grip force range (Robotiq)
GRIPPER_KG = 0.925 + 0.3       # 2F-85 + coupling + D405 and bracket (PR 318: 1.2 kg)

# MiR250 + cabinet + arm masses, PR 318 (alloy_atomize.MASS, WHEELS, MU, DRIVE_SHARE)
MIR_MASS = dict(mir250=97.0, ur=33.3, control_box=12.0, cabinet=25.0)
UR_LINKS = (7.369, 13.051, 3.989, 2.1, 1.98, 0.615)
WHEELS = (325.0, 225.0)
MU, DRIVE_SHARE = 0.6, 0.5


# ------------------------------------------------------------------------------------------------ helpers
def R_of(approach, closing):
    return C.frame(approach, closing)


def T_of(R, p):
    return C.Tm(R, p)


def rotx(deg):
    return C.rot((1, 0, 0), deg)


def rotz(deg):
    return C.rot((0, 0, 1), deg)


def roty(deg):
    return C.rot((0, 1, 0), deg)


def part_mass(p, M):
    if p.mass_kg is not None:
        return float(p.mass_kg)
    rho = M.MAT.get(p.mat, {}).get("rho", 1000.0)
    try:
        return float(p.shape.Volume()) * 1e-9 * rho
    except Exception:  # noqa: BLE001
        return 0.0


# ------------------------------------------------------------------------------------------------ the cell for one module
class Cell:
    def __init__(self, module="M50"):
        import lpbf_low as M
        self.M = M
        self.module = module
        t0 = time.time()
        self.parts = M.build(module=module)
        self.byname = {p.name: p for p in self.parts}
        self.sc = C.Scene(self.parts, region=REGION, deck=True)
        for nm, (b, p) in list(self.sc.machine.items()):
            if any(k in nm for k in ("Build plate", "Heater block", "Plate rim wiper", "Build module", "Blade holder", "Recoater arm",
                                     "Recoater carriage block", "lid with robot handle", "Dovetail rails")):
                v, f = C.tess(p.shape, 0.05, 0.2)
                nb = C.Body(nm, v, f, kind="machine", group=p.group, color=p.color, mat=p.mat)
                nb.place(b.M)
                self.sc.world.add(nb)
                self.sc.machine[nm] = (nb, p)
        self.arm = C.Arm()
        self.ck = C.Checker(self.sc, self.arm)
        self.build_s = round(time.time() - t0, 1)
        print(f"[cell {module}] {len(self.sc.world.bodies)} bodies in {self.build_s} s", flush=True)

    def names(self, *subs, group=None):
        out = []
        for n, (b, p) in self.sc.machine.items():
            if group is not None and p.group != group:
                continue
            if all(s in n for s in subs):
                out.append(n)
        return out

    def name(self, *subs):
        n = self.names(*subs)
        if not n:
            raise KeyError(subs)
        return n[0]

    def group_names(self, group):
        return [n for n, (b, p) in self.sc.machine.items() if p.group == group]


# ------------------------------------------------------------------------------------------------ a job
class Fail(Exception):
    pass


class Job:
    """Builds the frames of one job step by step (planned joint moves, Cartesian lines, grips, machine moves), then audits them."""

    def __init__(self, cell: Cell, name, arm_x=0.0, caps=None, wand=False, state0=None, note=""):
        self.c, self.name, self.note = cell, name, note
        self.arm = cell.arm
        self.sc = cell.sc
        self.arm_x = arm_x
        self.arm.base = C.Tm(None, (arm_x, C.ARM_Y, C.AMR_TOP))
        self.sc.move_mir(arm_x)
        self.arm.held = None
        self.arm.set_caps(caps)
        self.tool_kg = GRIPPER_KG + (caps.get("mass_kg", 0.0) if caps else 0.0)
        self.wand = None
        self.wand_T0 = None          # the wand's pose in its cradle, while it is not held
        if wand:
            (v, f), tip = E.wand_mesh()
            self.wand = C.Body("wand (ATEX vacuum wand, collar, crevice tool)", v, f, kind="held", color="#30343a")
            self.arm.held = (self.wand, np.eye(4))
            self.wand_tip = tip
            self.tool_kg += E.WAND["mass_kg"]
        self.state = dict(state0 or {})
        self.ov = {}
        self.sc.set_state(self.state, self.ov)
        self.close = 0.0
        self.q = self.stow()
        self.frames = []
        self.steps = []
        self.hold = None            # dict(names, body, T0 (tcp at grasp), Tw {name: world pose at grasp}, kg)
        self.holds = []             # every hold, in order (the audit replays them)
        self.hold_idx = -1
        self.payload = 0.0
        self.failed = None

    # ---- poses
    def stow(self):
        """A compact pose over the MiR250, clear of everything (searched once per cell)."""
        cands = [[-90, -100, 120, -110, -90, 0], [-90, -110, 130, -110, -90, 0], [90, -80, -120, -70, 90, 0],
                 [-90, -80, 120, -130, -90, 0], [-90, -120, 140, -110, -90, 0], [-90, -60, 100, -130, -90, 0]]
        for c_ in cands:
            q = np.radians(c_)
            if self.c.ck.free(q, 0.0):
                return q
        return np.radians(cands[0])

    def tcp(self, q=None, close=None):
        return self.arm.tcp(self.q if q is None else q, self.close if close is None else close)

    def moved(self, d=(0.0, 0.0, 0.0), R=None, about=None):
        """The current TCP pose translated by d (world mm), or turned by R about the vertical axis through `about` (world mm)."""
        T = self.tcp()
        if R is not None:
            c = np.asarray(about, float)
            T = C.Tm(None, c) @ C.Tm(R) @ C.Tm(None, -c) @ T
        return C.Tm(T[:3, :3], T[:3, 3] + np.asarray(d, float))

    # ---- frames
    def _frame(self, label, dt, force=(0.0, 0.0, 0.0), allow=frozenset(), kind="move", s=None):
        self.frames.append(dict(q=self.q.copy(), close=self.close, state=dict(self.state), ov={k: v.copy() for k, v in self.ov.items()},
                                label=label, dt=dt, force=tuple(float(f) for f in force), allow=frozenset(allow), kind=kind,
                                payload=self.payload, held=(tuple(self.hold["names"]) if self.hold else ()), hold=self.hold_idx,
                                wand=bool(self.wand is not None and self.arm.held is not None and self.arm.held[0] is self.wand),
                                step=len(self.steps)))

    def _step(self, label, t0, n0, ok=True, why="", extra=None):
        self.steps.append(dict(label=label, ok=ok, why=why, frames=len(self.frames) - n0,
                               secs=round(sum(f["dt"] for f in self.frames[n0:]), 2), **(extra or {})))
        if not ok:
            self.failed = dict(step=label, why=why)
            raise Fail(f"{label}: {why}")

    def ik_near(self, T, seed):
        sols = self.arm.ik_all(T, seed)
        return sols

    # ---- step kinds
    def lookahead(self, q1, then):
        """Can the lines that follow (then = [(T, allow, close)]) be followed from q1 without a branch flip, out-of-reach or collision
        (sampled every 15 mm / 5 deg)? The planner's IK-branch choice uses it, so a branch that dead-ends a few lines later is skipped."""
        q = q1
        T0 = self.arm.tcp(q, self.close)
        for T, allow, close in then:
            d = float(np.linalg.norm(T[:3, 3] - T0[:3, 3]))
            ang = float(np.degrees(np.arccos(np.clip((np.trace(T0[:3, :3].T @ T[:3, :3]) - 1) / 2, -1, 1))))
            n = max(1, int(math.ceil(max(d / 15.0, ang / 5.0))))
            for i in range(1, n + 1):
                s_ = i / n
                Tm_ = C.Tm(C.slerp(T0[:3, :3], T[:3, :3], s_), T0[:3, 3] + (T[:3, 3] - T0[:3, 3]) * s_)
                sols = self.arm.ik_all(Tm_, q)
                if not sols or np.abs(sols[0] - q).max() > 0.6:
                    return False, f"line to {np.round(T[:3, 3])}: {'no IK' if not sols else 'branch flip'} at s = {s_:.2f}"
                q = sols[0]
                bad = self.c.ck.collisions(q, self.close if close is None else close, allow, first=True)
                if bad:
                    return False, f"line to {np.round(T[:3, 3])}: hits {bad[0][1]} at s = {s_:.2f}"
            T0 = T
        self.arm.place(self.q, self.close)
        return True, ""

    def goto(self, T, label, allow=frozenset(), close=None, then=()):
        """Planned joint move to a TCP pose: every IK branch nearest first, the first that is clear, that the following lines can be
        followed from (lookahead) and that the straight joint line or RRT-Connect reaches (byu-vcl collide.plan_joint_move)."""
        n0, t0 = len(self.frames), time.time()
        if close is not None:
            self.close = close
        self.sc.set_state(self.state, self.ov)
        sols = self.arm.ik_all(T, self.q)
        if not sols:
            self._step(label, t0, n0, False, "no IK solution (out of reach)")
        tried = []
        if then:
            good, rest = [], []
            for q1 in sols:
                ok, why = self.lookahead(q1, then)
                (good if ok else rest).append((q1, why))
            sols = [q for q, _ in good] + [q for q, _ in rest]
            tried += [dict(lookahead=w) for _, w in rest[:3]]
        for k, q1 in enumerate(sols):
            bad = self.c.ck.collisions(q1, self.close, allow, first=True)
            if bad:
                tried.append(dict(branch=k, why=f"goal pose hits {bad[0][1]}" if bad[0][2] != "self" else f"self-collision {bad[0][:2]}"))
                continue
            path, info = self.c.ck.plan(self.q, q1, self.close, allow, seed=k, iters=1500)
            if path is None:
                tried.append(dict(branch=k, why=info.get("reason", "no path")))
                continue
            dense = C.densify(path)
            for qa, qb in zip(dense[:-1], dense[1:]):
                self.q = qb
                self._frame(label, float(np.abs(qb - qa).max()) / T_JOINT, allow=allow, kind="plan")
            self._step(label, t0, n0, True, extra=dict(branch=k, branches=len(sols), planned=bool(info.get("planned")),
                                                       waypoints=len(path), tried=tried[:4]))
            return
        self._step(label, t0, n0, False, f"no clear branch or path: {tried[:3]}")

    def line(self, T1, label, allow=frozenset(), fine=True, step_mm=2.0, step_deg=1.5, state_fn=None, force=(0.0, 0.0, 0.0),
             close_fn=None, max_jump=0.35):
        """Cartesian straight line of the TCP to T1 (slerp in orientation); state_fn(s) -> (state updates, override updates) moves the
        machine (or a held part) along with it."""
        n0, t0 = len(self.frames), time.time()
        T0 = self.tcp()
        d = float(np.linalg.norm(T1[:3, 3] - T0[:3, 3]))
        ang = float(np.degrees(np.arccos(np.clip((np.trace(T0[:3, :3].T @ T1[:3, :3]) - 1) / 2, -1, 1))))
        n = max(1, int(math.ceil(max(d / step_mm, ang / step_deg))))
        v = V_FINE if fine else V_FREE
        for i in range(1, n + 1):
            s = i / n
            R = C.slerp(T0[:3, :3], T1[:3, :3], s)
            p = T0[:3, 3] + (T1[:3, 3] - T0[:3, 3]) * s
            if close_fn is not None:
                self.close = close_fn(s)
            sols = self.arm.ik_all(C.Tm(R, p), self.q)
            if not sols:
                self._step(label, t0, n0, False, f"no IK at s = {s:.2f} (out of reach)")
            q1 = sols[0]
            if np.abs(q1 - self.q).max() > max_jump:
                self._step(label, t0, n0, False, f"IK branch flip at s = {s:.2f} (joint jump {np.degrees(np.abs(q1 - self.q).max()):.0f} deg)")
            dt = max(d / n / v, np.abs(q1 - self.q).max() / T_JOINT, ang / n / 45.0)
            self.q = q1
            if state_fn is not None:
                st, ov = state_fn(s)
                self.state.update(st or {})
                self.ov.update(ov or {})
            self._frame(label, dt, force=force, allow=allow, kind="line", s=s)
        self._step(label, t0, n0, True, extra=dict(length_mm=round(d, 1), turn_deg=round(ang, 1)))

    def grip(self, gap, label, allow=frozenset(), n=5):
        n0, t0 = len(self.frames), time.time()
        c1 = self.arm.close_for_gap(gap)
        c0 = self.close
        for i in range(1, n + 1):
            self.close = c0 + (c1 - c0) * i / n
            self._frame(label, T_GRIP / n, allow=allow, kind="grip")
        self._step(label, t0, n0, True, extra=dict(gap_mm=round(gap, 2)))

    def machine(self, label, secs, state_fn=None, n=10, allow=None):
        """The robot holds still while the machine moves (a damper lowering the door, the latch cylinders, a release). It keeps the
        previous frame's allowances (a part still in the fingers stays allowed)."""
        n0, t0 = len(self.frames), time.time()
        if allow is None:
            allow = self.frames[-1]["allow"] if self.frames else frozenset()
        for i in range(1, n + 1):
            if state_fn is not None:
                st, ov = state_fn(i / n)
                self.state.update(st or {})
                self.ov.update(ov or {})
            self._frame(label, secs / n, allow=allow, kind="machine")
        self._step(label, t0, n0, True)

    # ---- holding machine parts
    def attach(self, names, label):
        """The robot now carries these machine parts: they become one held body that rides on the TCP."""
        T0 = self.tcp()
        Ti = C.inv(T0)
        vs, fs, n, kg = [], [], 0, 0.0
        Tw = {}
        for nm in names:
            b, p = self.sc.machine[nm]
            Tw[nm] = b.M.copy()
            v = (np.c_[b.v, np.ones(len(b.v))] @ (Ti @ b.M).T)[:, :3]
            vs.append(v)
            fs.append(b.f + n)
            n += len(v)
            kg += part_mass(p, self.c.M)
            self.sc.world.remove(nm)
        body = C.Body(f"held: {label}", np.vstack(vs), np.vstack(fs), kind="held", color="#c8a040")
        self.arm.held = (body, np.eye(4))
        self.hold = dict(names=list(names), body=body, T0=T0, Tw=Tw, kg=kg)
        self.holds.append(self.hold)
        self.hold_idx = len(self.holds) - 1
        self.payload = kg
        self.arm.place(self.q, self.close)

    def detach(self):
        """Put the carried parts back into the world where they now are (as overrides on their group poses)."""
        h = self.hold
        Tn = self.tcp()
        for nm in h["names"]:
            b, p = self.sc.machine[nm]
            Tnew = Tn @ C.inv(h["T0"]) @ h["Tw"][nm]
            Mg = C.loc_matrix(self.c.M.part_location(p, self.state))
            self.ov[nm] = Tnew @ C.inv(Mg)
            self.sc.world.add(b)
        self.arm.held = (self.wand, np.eye(4)) if self.wand is not None else None
        self.hold = None
        self.hold_idx = -1
        self.payload = 0.0
        self.sc.set_state(self.state, self.ov)

    def restore(self):
        """Put every held part back into the world (the audit and the next job start from the full scene)."""
        for h in self.holds:
            for nm in h["names"]:
                self.sc.world.add(self.sc.machine[nm][0])
        self.arm.held = None
        if self.wand is not None:
            self.sc.world.remove(self.wand.name)

    def set_wand(self, held):
        """The wand rides on the TCP, or lies in its cradle as a world body."""
        if self.wand is None:
            return
        if held:
            self.sc.world.remove(self.wand.name)
            self.arm.held = (self.wand, np.eye(4))
        else:
            if self.arm.held is not None and self.arm.held[0] is self.wand:
                self.arm.held = None
            if self.wand_T0 is not None:
                self.sc.world.add(self.wand)
                self.wand.place(self.wand_T0)


# ------------------------------------------------------------------------------------------------ the audit
def audit(job: Job, every_clear=3):
    """Re-check every frame the way byu-vcl's collide.Auditor does (round 11 rules), measure clearances, torques and stability."""
    c, sc, arm = job.c, job.sc, job.arm
    held_body = None
    rows = []
    prev_pose = {}
    baseline = {}
    worst_clear = (math.inf, None, None, None)
    peak_tau = (0.0, None, None)
    tip_min = (math.inf, None, None)
    job.restore()
    holding = -1
    for k, f in enumerate(job.frames):
        # what the robot holds at this frame: replay the job's holds (the held parts leave the world and ride on the TCP)
        if f["hold"] != holding:
            if holding >= 0:
                for nm in job.holds[holding]["names"]:
                    sc.world.add(sc.machine[nm][0])
            holding = f["hold"]
            if holding >= 0:
                for nm in job.holds[holding]["names"]:
                    sc.world.remove(nm)
                arm.held = (job.holds[holding]["body"], np.eye(4))
            else:
                arm.held = None
            prev_pose = {}
        if holding < 0:
            job.set_wand(f.get("wand", False))
        sc.set_state(f["state"], f["ov"])
        arm.place(f["q"], f["close"])
        hits = c.ck.collisions(f["q"], f["close"], f["allow"])
        coll = [(a, b, d) for a, b, d in hits]
        # movers: machine bodies that moved since the last frame, against everything else (not their own group)
        movers = []
        for nm, (b, p) in sc.machine.items():
            if nm not in sc.world.bodies:
                continue
            M_ = b.M
            moved = nm in prev_pose and not np.allclose(prev_pose[nm], M_, atol=1e-6)
            prev_pose[nm] = M_.copy()
            if not moved:
                baseline.pop(nm, None)
                continue
            if nm not in baseline:
                # contacts it had before it started moving are its baseline (a door on its hinge, a drawer in its slot)
                baseline[nm] = set()
                first = True
            else:
                first = False
            others = C.Group([o for on, o in sc.world.bodies.items() if on != nm and not
                              (on in sc.machine and sc.machine[on][1].group and sc.machine[on][1].group == p.group)])
            for x, y in C.group_hits(C.Group([b]), others):
                if first:
                    baseline[nm].add(y.name)
                    continue
                if y.name in baseline[nm]:
                    continue
                d = C.depth(x, y, upto=C.DEPTH_MM)
                if d > C.DEPTH_MM:
                    movers.append((nm, y.name, d))
            if not first:
                still = {y.name for _, y in C.group_hits(C.Group([b]), others)}
                baseline[nm] &= still
        # clearance: robot (and what it holds) to everything it may not touch
        if k % every_clear == 0 or k == len(job.frames) - 1:
            allowed = {n for kind, n in f["allow"]}
            world = C.Group([o for on, o in sc.world.bodies.items() if on not in allowed])
            robot = C.Group([b for b in arm.bodies() if b.group != "base"])
            d, a, b = C.group_distance(robot, world, margin=40.0)
            if d < worst_clear[0]:
                worst_clear = (d, a.name if a else None, b.name if b else None, k)
            f["clear"] = d
        # torques: gravity, tool, payload and the reaction of the force the robot applies
        F = np.asarray(f["force"], float)
        tau = C.static_torques(arm, f["q"], F_world=-F, payload_kg=f["payload"], tool_kg=job.tool_kg)
        pct = np.abs(tau) / np.asarray(C.UR12E["tau_lim"]) * 100.0
        j = int(np.argmax(pct))
        if pct[j] > peak_tau[0]:
            peak_tau = (float(pct[j]), j, k)
        if k % every_clear == 0 or np.linalg.norm(F) > 0:
            st = stability(job, f["q"], F, f["payload"])
            if st["factor"] < tip_min[0]:
                tip_min = (st["factor"], st, k)
        rows.append(dict(k=k, coll=[(a, b, d) for a, b, d in coll], movers=movers))
    job.restore()
    bad = [r for r in rows if r["coll"] or r["movers"]]
    return dict(frames=len(rows), frames_in_collision=len([r for r in rows if r["coll"]]),
                frames_movers=len([r for r in rows if r["movers"]]),
                first_bad=[dict(frame=r["k"], label=job.frames[r["k"]]["label"],
                                arm=[(a, b, (round(d, 1) if isinstance(d, float) else d)) for a, b, d in r["coll"][:3]],
                                movers=[(a, b, round(d, 1)) for a, b, d in r["movers"][:3]]) for r in bad[:6]],
                bad_frames=[r["k"] for r in bad],
                min_clearance_mm=(round(worst_clear[0], 1) if worst_clear[0] < math.inf else None),
                min_clearance_pair=[worst_clear[1], worst_clear[2]], min_clearance_frame=worst_clear[3],
                peak_torque_pct=round(peak_tau[0], 1), peak_torque_joint=["base", "shoulder", "elbow", "wrist 1", "wrist 2", "wrist 3"][peak_tau[1]]
                if peak_tau[1] is not None else None,
                tip=tip_min[1], tip_frame=tip_min[2])


def stability(job: Job, q, F_applied, payload_kg):
    """byu-vcl PR 318 alloy_atomize.stability(), on this cell: the force (along the applied force's line, on the robot it is the
    reaction) that tips the MiR250 + ballast + cabinet + arm about its weakest support edge, and the factor over the job's force;
    with no force, the margin of the centre of gravity inside the support rectangle."""
    arm = job.arm
    H, CH = C.MIR["H"], C.MIR["cab_h"]
    mx, my, mz = job.arm_x, C.MIR_Y, C.FLOOR_Z               # MiR-local origin: its centre on the floor
    F = arm.fk(q)
    pos = {k: (arm.base @ F[k])[:3, 3] - np.array([mx, my, mz]) for k in ("base", "shoulder", "upper_arm", "forearm", "wrist1",
                                                                            "wrist2", "wrist3", "tool0")}
    tcp = arm.tcp(q)[:3, 3] - np.array([mx, my, mz])
    items = [(MIR_MASS["mir250"], (0.0, 0.0, 120.0)), (MIR_MASS["control_box"], (0.0, 0.0, H + 150.0)),
             (MIR_MASS["cabinet"], (0.0, 0.0, H + CH / 2)), (C.BALLAST["kg"], (0.0, 0.0, H + C.BALLAST["T"] / 2)),
             (MIR_MASS["ur"] - sum(UR_LINKS), pos["base"]), (UR_LINKS[0], pos["shoulder"]),
             (UR_LINKS[1], (pos["upper_arm"] + pos["forearm"]) / 2), (UR_LINKS[2], (pos["forearm"] + pos["wrist1"]) / 2),
             (UR_LINKS[3], pos["wrist1"]), (UR_LINKS[4], pos["wrist2"]), (UR_LINKS[5], pos["wrist3"]),
             (job.tool_kg, pos["tool0"]), (payload_kg, tcp)]
    m = sum(k for k, _ in items)
    G = sum(k * np.asarray(p, float) for k, p in items) / m
    Wt = m * 9.81
    ax, ay = WHEELS
    Fn = float(np.linalg.norm(F_applied))
    Fl = -np.asarray(F_applied, float) / Fn if Fn > 1e-9 else None
    best = (math.inf, None)
    edges = {"+x": ((ax, -ay), (1, 0)), "-x": ((-ax, ay), (-1, 0)), "+y": ((ax, ay), (0, 1)), "-y": ((-ax, -ay), (0, -1))}
    cog_margin = min(ax - abs(G[0]), ay - abs(G[1]))
    for nm, (a, u) in edges.items():
        A_ = np.array([a[0], a[1], 0.0])
        u = np.array([u[0], u[1], 0.0])
        e = np.cross((0, 0, 1.0), u)
        keep = Wt * float(-(G - A_) @ u)
        if Fl is None:
            continue
        arm_F = float(np.cross(tcp - A_, Fl) @ e)
        if arm_F > 1e-6:
            t = keep / arm_F
            if t < best[0]:
                best = (t, nm)
    slide = (MU * DRIVE_SHARE * Wt / float(np.hypot(Fl[0], Fl[1]))) if (Fl is not None and np.hypot(Fl[0], Fl[1]) > 1e-6) else math.inf
    tips = best[0]
    factor = min(tips, slide) / Fn if Fn > 1e-9 else cog_margin / 100.0      # no force: margin in units of 100 mm
    return dict(mass_kg=round(m, 1), cog_mm=[round(float(x)) for x in G], cog_margin_mm=round(float(cog_margin), 0),
                force_N=round(Fn, 1), tips_at_N=(round(tips) if tips < math.inf else None), tips_about=best[1],
                slides_at_N=(round(slide) if slide < math.inf else None), factor=round(float(factor), 2))


# ------------------------------------------------------------------------------------------------ the jobs
GT = 515.0            # guard-door travel


def door_T(deg, M):
    """4x4 of the door group at `deg` (rotation about +x through the hinge axis, as lpbf_low.group_location)."""
    hy, hz = M.DOOR_HINGE
    return C.Tm(None, (0, hy, hz)) @ C.Tm(rotx(deg)) @ C.Tm(None, (0, -hy, -hz))


def allow_of(*names, kind="tool"):
    return frozenset((kind, n) for n in names)


def job_guard_door(cell: Cell, arm_x=300.0, yaw=0.0):
    """Slide the laser guard's door 515 mm open by the new bar handle, and back closed (guard lock released by the cell first)."""
    j = Job(cell, "guard_door", arm_x=arm_x)
    h = cell.name("Guard-door handle")
    door = cell.names(group="gdoor")
    al = allow_of(h, *door)
    R = rotz(yaw) @ R_of((0, 1, 0), (1, 0, 0))
    hx, hy, hz = -312.0, -318.5, 105.0
    back = -90.0 * R[:, 2]
    j.goto(T_of(R, np.array((hx, hy, hz)) + back), "to the handle", close=j.arm.close_for_gap(40.0),
           then=[(T_of(R, (hx, hy, hz)), al, None), (T_of(R, (hx + GT, hy, hz)), al, None)])
    j.line(T_of(R, (hx, hy, hz)), "in round the bar", allow=al, fine=False)
    j.grip(12.3, "close on the Ø12 bar", allow=al)
    j.line(T_of(R, (hx + GT, hy, hz)), f"slide the door {GT:.0f} mm open", allow=al, fine=False, step_mm=5.0,
           state_fn=lambda s: ({"gdoor": GT * s}, None), force=(30.0, 0, 0))
    j.grip(40.0, "let go", allow=al)
    j.line(T_of(R, np.array((hx + GT, hy, hz)) + back), "back off", allow=al, fine=False)
    return j


def job_guard_door_close(cell: Cell, arm_x=300.0, yaw=0.0):
    j = Job(cell, "guard_door_close", arm_x=arm_x, state0={"gdoor": GT})
    h = cell.name("Guard-door handle")
    door = cell.names(group="gdoor")
    al = allow_of(h, *door)
    R = rotz(yaw) @ R_of((0, 1, 0), (1, 0, 0))
    hx, hy, hz = -312.0 + GT, -318.5, 105.0
    back = -90.0 * R[:, 2]
    j.goto(T_of(R, np.array((hx, hy, hz)) + back), "to the handle", close=j.arm.close_for_gap(40.0),
           then=[(T_of(R, (hx, hy, hz)), al, None), (T_of(R, (hx - GT, hy, hz)), al, None)])
    j.line(T_of(R, (hx, hy, hz)), "in round the bar", allow=al, fine=False)
    j.grip(12.3, "close on the bar", allow=al)
    j.line(T_of(R, (hx - GT, hy, hz)), "slide it closed", allow=al, fine=False, step_mm=5.0,
           state_fn=lambda s: ({"gdoor": GT * (1 - s)}, None), force=(-30.0, 0, 0))
    j.grip(40.0, "let go", allow=al)
    j.line(T_of(R, np.array((hx - GT, hy, hz)) + back), "back off", allow=al, fine=False)
    return j


DOOR_OPEN = 95.0
DOOR_TIP = 11.6          # the door's centre of mass passes over the hinge here: past it the door falls open, short of it, shut


def job_chamber_door_open(cell: Cell, damper=True, arm_x=0.0, **kw):
    """Latch cylinders throw the draw latches open; the robot pulls the handle 20 deg (past the balance point), lets go and backs
    off up and away; the damper lowers the door to 95 deg."""
    M = cell.M
    j = Job(cell, "chamber_door_open", arm_x=arm_x, state0={"gdoor": GT})
    hname = cell.name("Door handle")
    door = cell.group_names("door")
    al = allow_of(hname, *door)
    hcen = np.array([0.0, -152.0, 95.0])                 # the handle bar's centre (Ø12 along x)
    R0 = R_of((0, 1, 0), (0, 0, 1))                      # approach +y, fingers close along z on the bar
    j.machine("draw-latch cylinders throw both latches open", 1.5)
    j.goto(T_of(R0, hcen + (0, -90, 0)), "to the door handle", close=j.arm.close_for_gap(40.0))
    j.line(T_of(R0, hcen), "in round the bar", allow=al)
    j.grip(12.3, "close on the bar", allow=al)
    a1 = 20.0
    Td = door_T(a1, M)
    j.line(Td @ T_of(R0, hcen), f"pull the door to {a1:.0f} deg (balance {DOOR_TIP} deg)", allow=al, step_deg=1.0,
           state_fn=lambda s: ({"door": a1 * s}, None), force=tuple(Td[:3, :3] @ np.array([0, -15.0, 0])))
    j.grip(40.0, "let go", allow=al)
    Tr = Td @ T_of(R0, hcen)
    Tr1 = C.Tm(Tr[:3, :3], Tr[:3, 3] - 70.0 * Tr[:3, 2])
    j.line(Tr1, "straight off the bar (faster than the damped door follows)", allow=al, fine=False)
    j.line(C.Tm(Tr[:3, :3], Tr1[:3, 3] + np.array([0, -40.0, 90.0])), "up and away from the door's arc", allow=al, fine=False)
    secs = 3.0 if damper else 0.45
    j.machine(f"the door lowers itself to {DOOR_OPEN:.0f} deg on the damper", secs, n=15,
              state_fn=lambda s: ({"door": a1 + (DOOR_OPEN - a1) * s}, None))
    return j


def job_chamber_door_close(cell: Cell, arm_x=0.0, a_end_=8.0, tilt=20.0, **kw):
    """Take the door's lift lug from the front (with the door hanging open it sticks out level from the free edge), lift the door on
    it past its balance point to ~8 deg, let go: the door settles onto its seal by its own weight; the latch cylinders pull it home."""
    M = cell.M
    j = Job(cell, "chamber_door_close", arm_x=arm_x, state0={"gdoor": GT, "door": DOOR_OPEN})
    a_end = a_end_
    lug = cell.name("Door lift lug")
    door = cell.group_names("door")
    al = allow_of(lug, *door)
    cy = cell.M.P["cy"]
    pl = np.array([-137.0, -cy - 7.5, 105.0])              # the lug's centre, door shut (x -150..-124, z 96..114, 15 thick)
    T95 = door_T(DOOR_OPEN, M)
    # grasp in the door's frame: at 95 deg the approach is level (+y world), the fingers close across the lug's 4 mm (world z)
    a_w = np.array([0.0, math.cos(math.radians(tilt)), -math.sin(math.radians(tilt))])
    a_loc = T95[:3, :3].T @ a_w
    c_loc = T95[:3, :3].T @ np.cross((1.0, 0.0, 0.0), a_w)
    G_loc = T_of(C.frame(a_loc, c_loc), pl)
    gl = 15.3
    th = [(T95 @ G_loc, al, None), (door_T(50.0, M) @ G_loc, al, j.arm.close_for_gap(gl)), (door_T(a_end, M) @ G_loc, al, j.arm.close_for_gap(gl))]
    j.goto(T95 @ G_loc @ C.Tm(None, (0, 0, -60.0)), "to the lug at the open door's free edge", close=j.arm.close_for_gap(32.0), then=th)
    j.line(T95 @ G_loc, "in round the lug", allow=al)
    j.grip(gl, "close on the lug (15 mm)", allow=al)
    n = int(round((DOOR_OPEN - a_end) / 2.0))
    for k in range(1, n + 1):
        a0 = DOOR_OPEN + (a_end - DOOR_OPEN) * (k - 1) / n
        a1 = DOOR_OPEN + (a_end - DOOR_OPEN) * k / n
        Tk = door_T(a1, M) @ G_loc
        F = door_T(a1, M)[:3, :3] @ np.array([0, 0, 12.0])
        j.line(Tk, "lift the door on its lug", allow=al, step_deg=1.0,
               state_fn=lambda s, a0=a0, a1=a1: ({"door": a0 + (a1 - a0) * s}, None), force=tuple(F))
    j.grip(32.0, "let go short of shut (the door settles by its weight)", allow=al)
    T_end = door_T(a_end, M) @ G_loc
    j.line(T_end @ C.Tm(None, (0, 0, -60.0)), "back off", allow=al, fine=False)
    j.machine("the door settles onto its seal; the latch cylinders pull it home", 2.5, n=8,
              state_fn=lambda s: ({"door": a_end * (1 - s)}, None))
    return j


def job_chamber_door_powered(cell: Cell, arm_x=0.0, **kw):
    """The fix for closing: the door's rotary actuator lifts it from 95 deg to shut in 2 s while the robot waits at its stow pose over
    the MiR (the movers check sees the door's sweep against everything, the parked arm included); then the latch cylinders."""
    j = Job(cell, "chamber_door_powered", arm_x=arm_x, state0={"gdoor": GT, "door": DOOR_OPEN})
    j.machine("the door actuator closes the door (95 -> 0 deg)", 2.0, n=24, state_fn=lambda s: ({"door": DOOR_OPEN * (1 - s)}, None))
    j.machine("latch cylinders throw both latches shut", 1.5)
    return j


def job_drawer(cell: Cell, arm_x=0.0, **kw):
    """Turn both wing heads 90 deg (unlock), pull the drawer out by its tab and on out of the lid (it goes to the MiR's rack: the
    robot swaps the whole drawer with a spare whose cover slide is clean), push it back in, turn the wings back (the cams pull it
    onto its O-ring)."""
    j = Job(cell, "drawer", arm_x=arm_x, state0={"gdoor": GT, "door": DOOR_OPEN})
    dr = cell.group_names("drawer")
    wl, wr = cell.name("wing head, left"), cell.name("wing head, right")
    tab = cell.name("Cover-slide drawer (6061")
    Rw = R_of((0, 1, 0), (0, 0, 1))                       # approach +y, fingers close along z across the 4 mm wing
    zq, yh = 128.0, -141.0                                  # TCP 14.5 mm in front of the wing: the pads' tips stop 3 mm short of the front plate
    turned = {}

    def wings_at(d, lift=0.0):
        """Overrides for the wings already turned, riding with the drawer pulled d (mm, negative out) and lifted."""
        out = {}
        for nm_, (x_, deg_) in turned.items():
            q_ = np.array([x_, yh + d, zq + lift])
            out[nm_] = C.Tm(None, (0, 0, lift)) @ C.Tm(None, q_) @ C.Tm(C.rot((0, 1, 0), deg_)) @ C.Tm(None, -q_) @ C.Tm(None, (0, 0, -lift)) \
                if lift else C.Tm(None, q_) @ C.Tm(C.rot((0, 1, 0), deg_)) @ C.Tm(None, -q_)
        return out
    for nm, x in ((wl, -51.0), (wr, 51.0)):
        alw = allow_of(nm, *dr)
        p = np.array([x, yh, zq])
        Rot_ = C.Tm(None, p) @ C.Tm(C.rot((0, 1, 0), 90.0)) @ C.Tm(None, -p)
        j.goto(T_of(Rw, p + (0, -80, 0)), f"to the {('left' if x < 0 else 'right')} wing", close=j.arm.close_for_gap(16.0),
               then=[(T_of(Rw, p), alw, None), (Rot_ @ T_of(Rw, p), alw, j.arm.close_for_gap(4.3))])
        j.line(T_of(Rw, p), "round the wing", allow=alw)
        j.grip(4.3, "close across the wing", allow=alw)
        Rot = C.Tm(None, p) @ C.Tm(C.rot((0, 1, 0), 90.0)) @ C.Tm(None, -p)

        def stw(s, nm=nm, p=p):
            Tw = C.Tm(None, p) @ C.Tm(C.rot((0, 1, 0), 90.0 * s)) @ C.Tm(None, -p)
            return None, {nm: Tw}
        j.line(Rot @ T_of(Rw, p), "turn it 90 deg (cam off)", allow=alw, step_deg=3.0, state_fn=stw, force=(0, 0, 0))
        turned[nm] = (x, 90.0)
        j.grip(16.0, "let go", allow=alw)
        j.line(Rot @ T_of(Rw, p + (0, -80, 0)), "back off", allow=alw, fine=False)
    # the tab: grip the outer faces of its two side posts (x +/-20)
    Rt = R_of((0, 1, 0), (1, 0, 0))
    pt = np.array([0.0, -143.0, 128.0])                     # the pads' tips stop 3-5 mm short of the drawer's front plate
    alt = allow_of(*dr)
    j.goto(T_of(Rt, pt + (0, -80, 0)), "to the pull tab", close=j.arm.close_for_gap(56.0),
           then=[(T_of(Rt, pt), alt, None), (T_of(Rt, pt + (0, -175, 0)), alt, j.arm.close_for_gap(40.3))])
    j.line(T_of(Rt, pt), "round the tab's posts", allow=alt)
    j.grip(40.3, "close on the posts", allow=alt)
    soft = frozenset(("soft", n) for n in cell.names("Drawer O-ring"))
    j.line(T_of(Rt, pt + (0, -120, 0)), "pull 120 mm (O-ring breakaway ~20 N)", allow=alt | soft, step_mm=4.0,
           state_fn=lambda s: ({"drawer": -120.0 * s}, wings_at(-120.0 * s)), force=(0, -20.0, 0))
    j.line(T_of(Rt, pt + (0, -175, 0)), "on out of the lid", allow=alt | soft, step_mm=4.0,
           state_fn=lambda s: ({"drawer": -120.0 - 55.0 * s}, wings_at(-120.0 - 55.0 * s)), force=(0, -5.0, 0))

    def carry(s):
        d, up = -175.0 - 105.0 * s, 40.0 * s
        ov = {n: C.Tm(None, (0, 0, up)) for n in dr}
        for n_, T_ in wings_at(d).items():
            ov[n_] = C.Tm(None, (0, 0, up)) @ T_
        return {"drawer": d}, ov
    j.line(T_of(Rt, pt + (0, -195, 40)), "lift it clear of the lid (on to the MiR's drawer rack)", allow=alt, fine=False,
           state_fn=lambda s: carry(s * 20.0 / 105.0) if False else ({"drawer": -175.0 - 20.0 * s}, {**{n: C.Tm(None, (0, 0, 40.0 * s)) for n in dr},
                                                                     **{n_: C.Tm(None, (0, 0, 40.0 * s)) @ T_ for n_, T_ in wings_at(-175.0 - 20.0 * s).items()}}))
    # the spare goes in the same way back: the frames above, reversed (same poses, so the same audit), then the wings back
    return j


def job_plate(cell: Cell, mode="drawbar", arm_x=0.0, **kw):
    """Take the build plate out through the open door with the plate fingers and bring it out (the new plate goes in on the same
    path, reversed). mode "drawbar": the machine's release cylinder opens the ball lock and the plate lifts straight off;
    "bayonet": skew -30 deg with open fingers, grip, twist 60 deg, lift."""
    M = cell.M
    caps = E.plate_finger_spec()
    j = Job(cell, f"plate_{mode}", arm_x=arm_x, caps=caps, state0={"gdoor": GT, "door": DOOR_OPEN, "piston": M.MP.Z_P_MAX})
    plate = cell.name("Build plate")
    wiper = cell.name("Plate rim wiper")
    block = cell.name("Heater block")
    held = [plate, wiper]
    fix = [block, cell.name("Build module")]
    al = allow_of(*held, *fix) | allow_of(*fix, kind="held")
    pd = M.MP.MODULES[cell.module]["plate_d"]
    zg = 2.5                                             # groove centre at exchange height (+8): z 1..4
    R = R_of((0, 1, 0), (1, 0, 0))
    open_gap = pd + 6.0
    j.goto(T_of(R, (0, -260, zg + 9.5)), "to the door (lips 9.5 mm up, over the 8 mm sill)", close=j.arm.close_for_gap(open_gap),
           then=[(T_of(R, (0, 0, zg + 9.5)), al, None), (T_of(R, (0, 0, zg)), al, None), (T_of(R, (0, -300, zg + 20.0)), al, None)])
    j.line(T_of(R, (0, 0, zg + 9.5)), "in over the sill, the plate between the blades", allow=al, step_mm=3.0)
    j.line(T_of(R, (0, 0, zg)), "down beside the plate to the groove", allow=al, step_mm=1.0)
    if mode == "bayonet":
        # 60 deg in two 30 deg twists with a regrasp: one 60 deg twist (-30 -> +30) swings the blades into the door opening's sides
        for k in range(2):
            j.line(C.Tm(rotz(-15.0)) @ T_of(R, (0, 0, zg)), "skew -15 deg about the plate's axis (fingers open)", allow=al, step_deg=2.0)
            j.grip(pd - 3.0 + 0.1, "close the lips into the rim groove", allow=al)
            j.attach(held, "build plate")
            j.line(j.moved(R=rotz(30.0), about=(0, 0, 0)), f"twist the plate 30 deg ({'half' if k == 0 else 'lugs at their slots'})",
                   allow=al, step_deg=2.0, force=(0, 0, 0))
            if k == 0:
                j.detach()
                j.grip(pd + 6.0, "open", allow=al)
        j.line(j.moved((0, 0, 20.0)), "lift 20 mm off the block", allow=al, step_mm=1.0, force=(0, 0, 5.0))
        j.line(j.moved(R=rotz(-15.0), about=(0, 0, 0)), "turn back square", allow=al, step_deg=2.0)
    else:
        # the drawbar is not drawn yet (patch request): the drawn plate stands in for it turned 60 deg, its bayonet lugs in their
        # entry slots, so it lifts straight off as a pull stud would
        j.ov.update({n: C.Tm(rotz(60.0)) for n in held})
        j.sc.set_state(j.state, j.ov)
        j.grip(pd - 3.0 + 0.1, "close the lips into the rim groove", allow=al)
        j.machine("release cylinder pushes the drawbar: ball lock open", 1.0)
        j.attach(held, "build plate")
        j.line(j.moved((0, 0, 20.0)), "lift 20 mm: pull stud out of the ball lock", allow=al, step_mm=1.0, force=(0, 0, 5.0))
    j.line(j.moved((0, -300.0, 0)), "out over the sill and the open door", allow=al, step_mm=3.0)
    j.line(j.moved((0, -30.0, 100.0)), "up clear of the machine (to the MiR's plate rack)", allow=al, fine=False)
    return j


def job_reservoir(cell: Cell, arm_x=-90.0, roll=0.0, **kw):
    """Pull the reservoir off the dock (40 N over its three detents) by its handle fin with the plate fingers, and carry it out of
    the optics bridge's slot to the front; the full one goes in the same way back."""
    caps = E.plate_finger_spec(E.RESERVOIR_FINGERS)
    j = Job(cell, "reservoir", arm_x=arm_x, caps=caps, state0={"gdoor": GT})
    res = cell.group_names("cartridge")
    lid = cell.name("lid with robot handle")
    al = allow_of(*res)
    xd = cell.M.P["x_dose"]
    R = R_of((0, 1, 0), (1, 0, 0)) @ C.rot((0, 0, 1), roll)      # roll 180: the caps' step goes up, the camera is underneath
    p = np.array([xd, -18.0, 252.0 if roll == 0 else 255.0])     # lips on the handle fin (fin z 248..258, 8 mm thick)
    j.goto(T_of(R, p + (0, -230, 0)), "to the reservoir's handle, in front of the bridge slot", close=j.arm.close_for_gap(16.0),
           then=[(T_of(R, p), al, None), (T_of(R, p + (0, -330, 0)), al, j.arm.close_for_gap(8.1))])
    j.line(T_of(R, p), "in along the slot, the blades either side of the fin", allow=al, step_mm=3.0)
    j.grip(8.1, "close on the fin", allow=al)
    j.attach(res, "reservoir")
    dock = allow_of(*cell.names("Dovetail rails"), *cell.names("Metering base"), *cell.names("Load cell"), kind="held") | \
        frozenset(("soft", n) for n in cell.names("dock-face O-ring"))
    j.line(j.moved((0, -125.0, 0)), "pull 125 mm off the dock (40 N over the detents)", allow=dock | al, step_mm=3.0, force=(0, -40.0, 0))
    j.line(j.moved((0, -205.0, 0)), "carry it out of the bridge slot and the guard", allow=al, step_mm=4.0)
    j.line(j.moved((0, -30.0, -60.0)), "lower it towards the MiR's rack", allow=al, fine=False)
    return j


def job_blade(cell: Cell, arm_x=0.0, **kw):
    """Drive the recoater to the middle, take the blade cartridge (holder + blade) by its fin with the plate fingers, pull it 10 mm
    out of the arm's pocket (two ball plungers, 40 N), lift 12 mm over the sill and out through the door."""
    caps = E.plate_finger_spec()
    off = 106.0
    j = Job(cell, "blade_cartridge", arm_x=arm_x, caps=caps, state0={"gdoor": GT, "door": DOOR_OPEN, "recoater": off, "piston": -2.0})
    holder = cell.name("Blade holder")
    blade = cell.name("HSS recoater blade")
    fin = cell.name("Blade-cartridge grip fin")
    held = [holder, blade, fin] + cell.names("Blade screws")
    al = allow_of(*held, cell.name("Recoater arm"))
    R = R_of((0, 1, 0), (1, 0, 0))
    p = np.array([0.0, -71.0, 22.0])                      # lips on the fin (x -2..2 with the recoater at +106, y -73..-53, z 18..34)
    j.goto(T_of(R, p + (0, -230, 0)), "to the door", close=j.arm.close_for_gap(12.0),
           then=[(T_of(R, p), al, None), (T_of(R, p + (0, -300, 12)), al, j.arm.close_for_gap(4.1))])
    j.line(T_of(R, p), "in over the sill, blades either side of the fin", allow=al, step_mm=3.0)
    j.grip(4.1, "close on the fin", allow=al)
    j.attach(held, "blade cartridge")
    alh = al | allow_of(cell.name("Recoater arm"), cell.name("Recoater carriage block"), *cell.names("Chamber floor plate"),
                        *cell.names("Build module"), *cell.names("Process chamber body"), kind="held")
    j.line(j.moved((0, -10.0, 0)), "pull 10 mm out of the arm's pocket (40 N over the plungers)", allow=alh, step_mm=1.0, force=(0, -40.0, 0))
    j.line(j.moved((0, 0, 12.0)), "lift 12 mm (the blade's edge over the sill)", allow=alh, step_mm=1.0)
    j.line(j.moved((0, -290.0, 0)), "out through the door", allow=al, step_mm=3.0)
    j.line(j.moved((0, -30.0, 88.0)), "up clear (to the MiR's tool rack)", allow=al, fine=False)
    return j


def job_module(cell: Cell, arm_x=0.0, tilt=25.0, roll=0.0, **kw):
    """Release the module (twist-lock or zero-point clamps, see the patch requests) and the Z arm, then carry the module by its
    handle along the model's own extraction path (MODULE_PATH: down 40, forward under the plenum, up under the hinges, over the
    guard sill and out)."""
    M = cell.M
    st0 = {"zstage": M.MP.ZSTAGE_RELEASE, "gdoor": GT}
    j = Job(cell, "module_swap", arm_x=arm_x, state0=st0)
    mod = cell.names(group="module")
    pis = [n for n, (b, p) in cell.sc.machine.items() if "in_module" in p.tags]
    held = sorted(set(mod) | set(pis))
    hd = cell.name("handle (6061, screwed under the gland plate")
    b, p = cell.sc.machine[hd]
    lo, hi = b.box()
    # the side arms' outer faces are at x = +/-24; take them from the front, the gripper tilted 25 deg down so its housing rides
    # over the guard's bottom rail
    pg = np.array([0.0, (lo[1] + hi[1]) / 2 + 4.0, lo[2] + 5.0])
    a = np.array([0.0, math.cos(math.radians(tilt)), -math.sin(math.radians(tilt))])
    R = R_of(a, (1, 0, 0)) @ C.rot((0, 0, 1), roll)
    al = allow_of(*held)
    j.machine("module clamps open; the Z arm drops 45 mm off the rod end", 2.0)
    path_ = [np.array(q) for q in M.MODULE_PATH]
    j.goto(T_of(R, pg - a * 90), "to the module handle", close=j.arm.close_for_gap(60.0),
           then=[(T_of(R, pg), al, None)] + [(T_of(R, pg + q_), al, j.arm.close_for_gap(48.3)) for q_ in path_[1:]])
    j.line(T_of(R, pg), "round the handle's side arms", allow=al)
    j.grip(48.3, "close on the side arms", allow=al)
    j.attach(held, "build module")
    path = [np.array(q) for q in M.MODULE_PATH]
    fixtures = allow_of(*cell.names("Process chamber body"), *cell.names("Locating dowel"), *cell.names("helical inserts"),
                        *cell.names("thumb screw"), kind="held") | frozenset(("soft", n) for n in cell.names("Spigot O-ring"))
    for k, (pa, pb) in enumerate(zip(path[:-1], path[1:])):
        F = (0, 0, -158.0) if k == 0 else (0, 0, 0)       # the first 40 mm: the 2-238 O-ring's 132 N plus the module's weight
        j.line(T_of(R, pg + pb), f"module path {tuple(int(v) for v in pa)} -> {tuple(int(v) for v in pb)}",
               allow=(al | fixtures) if k == 0 else al, step_mm=3.0, force=F)
    j.line(T_of(R, pg + path[-1] + (0, -60, 60)), "up and out (to the MiR's module rack)", allow=al, fine=False)
    return j


def job_overflow(cell: Cell, skip_note="", arm_x=100.0, **kw):
    """The overflow jar as drawn: open the KF-40 clamp, lower the jar 6 mm off the stub, and out to the front."""
    j = Job(cell, "overflow_jar", arm_x=arm_x, state0={"gdoor": GT})
    jar = cell.name("Overflow jar")
    al = allow_of(jar, *cell.names("Overflow clamp"))
    R = R_of((0, 1, 0), (1, 0, 0))
    p = np.array([100.0, 0.0, -110.0])
    j.goto(T_of(R, p + (0, -260, 0)), "to the jar under the chamber", close=j.arm.close_for_gap(62.0))
    j.line(T_of(R, p), "in to the jar", allow=al, step_mm=3.0)
    j.grip(55.2, "close on the jar", allow=al)
    j.attach([jar], "overflow jar")
    j.line(T_of(R, p + (0, 0, -6)), "lower 6 mm off the KF-40 stub", allow=al | allow_of(*cell.names("Overflow port"), kind="held"), step_mm=1.0)
    j.line(T_of(R, p + (0, -300, -6)), "out to the front", allow=al, step_mm=3.0)
    return j


def job_vacuum(cell: Cell, arm_x=0.0, **kw):
    """Chamber cleaning with the ATEX vacuum's wand: in through the open door, the crevice tool 3 mm over the floor in three lanes
    across the chamber, out again (byu-vcl PR 318's atom_vacuum: the arm stays outside, only the wand goes in)."""
    M = cell.M
    j = Job(cell, "vacuum_clean", arm_x=arm_x, wand=False, state0={"gdoor": GT, "door": DOOR_OPEN, "piston": 0.0})
    (v, f), tip = E.wand_mesh()
    j.wand = C.Body("wand (ATEX vacuum wand, collar, crevice tool)", v, f, kind="held", color="#30343a")
    j.wand_tip = tip
    # the wand lies in its cradle on the MiR's cabinet top, along y, fin up: TCP over the fin, pointing down, fingers across it
    top = C.FLOOR_Z + C.MIR["H"] + C.MIR["cab_h"]
    wx = j.arm_x - 260.0
    # the wand lies in its cradle pointing at the VLM (+y), its axis 39 mm over the cabinet top, the fin up; the gripper takes the fin
    # level from behind, as it will hold it in the chamber (tool z +y, tool y down, fingers across the fin)
    Rc = R_of((0, 1, 0), (1, 0, 0))
    p_fin = np.array([wx, C.MIR_Y, top + 75.0 + E.WAND["axis_y"]])
    Tcr = T_of(Rc, p_fin)
    j.sc.world.add(j.wand)
    j.wand.place(Tcr)
    j.wand_T0 = Tcr
    j.goto(Tcr @ C.Tm(None, (0, 0, -70.0)), "to the wand in its cradle", close=j.arm.close_for_gap(40.0),
           allow=allow_of(j.wand.name), then=[(Tcr, allow_of(j.wand.name), None)])
    j.line(Tcr, "in round the wand's fin", fine=False, allow=allow_of(j.wand.name))
    j.grip(30.3, "close on the fin (30 mm)", allow=allow_of(j.wand.name))
    j.sc.world.remove(j.wand.name)
    # the wand's mesh is in the TCP frame of the grip, so it simply rides on the TCP from here on
    j.wand_held_from = len(j.frames)
    j.arm.held = (j.wand, np.eye(4))
    j.tool_kg += E.WAND["mass_kg"]
    j.line(C.Tm(Tcr[:3, :3], Tcr[:3, 3] + np.array([0, 0, 80.0])), "lift it out of the cradle", fine=False,
           allow=allow_of(*[n for n in j.sc.world.bodies if n.startswith("MiR250 wand cradle")], kind="held"))
    tip = j.wand_tip                                     # in the TCP frame
    beta = 0.0                                           # the wand level, 30 mm over the floor
    a = np.array([0.0, math.cos(math.radians(beta)), -math.sin(math.radians(beta))])
    R = R_of(a, (1, 0, 0))

    def T_for(tip_world, yaw=0.0):
        Rw = rotz(yaw) @ R
        return C.Tm(Rw, np.asarray(tip_world, float) - Rw @ tip)
    # x >= -60: the dose chute hangs 37 mm over the floor at x -96..-84 (|y| <= 50), so the strip under it (the recoater's park and
    # dose zone) is out of the level wand's reach
    lanes = [(-55.0, (-60.0, 70.0)), (0.0, (70.0, -60.0)), (50.0, (-60.0, 70.0))]     # y <= 50: the recoater's ball screw is at y 72, z 40
    z = 3.0                                              # the nozzle's mouth 3 mm over the floor
    j.goto(T_for((lanes[0][1][0], -260.0, z + 40)), "to the door with the wand", close=j.arm.close_for_gap(30.3))
    for ly, (x0, x1) in lanes:
        yaw0 = yaw1 = 0.0
        j.line(T_for((x0, ly, z + 30), yaw0), f"in to the lane y = {ly:.0f}", fine=False, step_mm=5.0)
        j.line(T_for((x0, ly, z), yaw0), "down to 3 mm over the floor", step_mm=2.0)
        j.line(T_for((x1, ly, z), yaw1), f"sweep the lane y = {ly:.0f}", step_mm=4.0)
        j.line(T_for((x1, ly, z + 30), yaw1), "up", step_mm=3.0)
    x_last = lanes[-1][1][1]
    j.line(T_for((x_last, -200.0, z + 30)), "straight back out through the door", fine=False, step_mm=5.0)
    j.line(T_for((0.0, -300.0, 60.0)), "clear of the machine", fine=False, step_mm=5.0)
    return j


def job_liner(cell: Cell, arm_x=0.0, **kw):
    """The right side liner, with its screw hole slotted to the back edge and 15 mm shorter at the front (patch): lips on its pull
    tab, slide it 26 mm forward along the wall (off the ball screw), in 30 mm off the wall, roll 30 deg, out through the door."""
    caps = E.plate_finger_spec()
    j = Job(cell, "liner_right", arm_x=arm_x, caps=caps, state0={"gdoor": GT, "door": DOOR_OPEN})
    tab = cell.name("Liner pull tabs")
    liner = cell.name("Lift-out wall liners")
    held = [tab, liner]
    al = allow_of(*held, cell.name("Process chamber body"))
    ix = cell.M.P["ix"]
    # the tab plate: x 125.4..127.4, y -70..-46, z 92..108 (right); approach +y with a slight yaw so the blades reach past the opening
    xc = 126.4
    R = R_of((0, 1, 0), (1, 0, 0))
    p = np.array([xc, -58.0, 100.0])
    yaw = -8.0
    Rr = rotz(yaw) @ R
    j.goto(C.Tm(Rr, p + rotz(yaw) @ np.array([0, -230.0, 0])), "to the door", close=j.arm.close_for_gap(16.0))
    j.line(C.Tm(Rr, p), "in to the liner's tab", allow=al, step_mm=3.0)
    j.grip(2.1, "close on the tab", allow=al)
    j.attach(held, "liners (right liner + tabs)")
    j.line(C.Tm(Rr, p + (0, -26, 0)), "slide 26 mm forward along the wall (off the screw)", allow=al | allow_of(cell.name("Process chamber body"), kind="held"),
           step_mm=1.0, force=(0, -20.0, 0))
    return j


_SIDES = [dict(arm_x=-450.0), dict(arm_x=450.0), dict(arm_x=-300.0), dict(arm_x=300.0), dict(arm_x=-600.0), dict(arm_x=600.0), dict(arm_x=0.0)]
VARIANTS = {
    "guard_door": [dict(arm_x=450.0), dict(arm_x=300.0), dict(arm_x=300.0, yaw=-30.0), dict(arm_x=-450.0), dict(arm_x=150.0, yaw=-40.0)],
    "guard_door_close": [dict(arm_x=450.0), dict(arm_x=300.0), dict(arm_x=300.0, yaw=-30.0), dict(arm_x=-450.0), dict(arm_x=150.0, yaw=-40.0)],
}
for _k in ("chamber_door_open", "drawer", "plate_drawbar", "plate_bayonet", "reservoir", "blade_cartridge",
           "module_swap", "overflow_jar", "vacuum_clean", "liner_right"):
    VARIANTS[_k] = [dict(v) for v in _SIDES]
VARIANTS["reservoir"] = [dict(arm_x=x, roll=0.0) for x in (-390.0, 210.0, -540.0, 360.0, -240.0, -90.0)]
VARIANTS["module_swap"] = [dict(arm_x=x, tilt=t, roll=r) for r in (180.0, 0.0) for t in (40.0, 25.0) for x in (-300.0, 250.0, -70.0)]
VARIANTS["chamber_door_close"] = [dict(arm_x=x, tilt=t) for t in (-45.0, -30.0, -60.0, 20.0) for x in (-450.0, -300.0, 0.0, 300.0)]
VARIANTS["plate_bayonet"] = [dict(arm_x=x) for x in (450.0, -450.0, 300.0, -300.0, 600.0)]
VARIANTS["plate_drawbar"] = [dict(arm_x=x) for x in (450.0, -450.0, 300.0, -300.0, 600.0)]
VARIANTS["overflow_jar"] = [dict(arm_x=x) for x in (100.0, 550.0, -350.0)]

JOBS = {
    "guard_door": job_guard_door,
    "guard_door_close": job_guard_door_close,
    "chamber_door_open": job_chamber_door_open,
    "chamber_door_close": job_chamber_door_close,
    "chamber_door_powered": job_chamber_door_powered,
    "plate_drawbar": lambda c, **kw: job_plate(c, "drawbar", **kw),
    "plate_bayonet": lambda c, **kw: job_plate(c, "bayonet", **kw),
    "drawer": job_drawer,
    "reservoir": job_reservoir,
    "blade_cartridge": job_blade,
    "module_swap": job_module,
    "overflow_jar": job_overflow,
    "vacuum_clean": job_vacuum,
    "liner_right": job_liner,
}


# ------------------------------------------------------------------------------------------------ rendering
def render(job: Job, gif_path, png_path=None, size=(480, 360), max_frames=60, still_frame=None, cam=None):
    """GIF of the job (<= max_frames, evenly spaced) and a still of one frame, offscreen with pyvista."""
    import imageio.v2 as imageio
    import pyvista as pv
    pv.OFF_SCREEN = True
    sc, arm = job.sc, job.arm
    job.restore()
    pl = pv.Plotter(off_screen=True, window_size=list(size))
    pl.set_background("#f4f5f6")
    actors = {}
    lo = np.array([-470.0, -620.0, -260.0])
    hi = np.array([420.0, 260.0, 420.0])

    def add(b, color, opacity=1.0):
        m = pv.PolyData(b.v, np.c_[np.full(len(b.f), 3), b.f].ravel())
        a = pl.add_mesh(m, color=color, opacity=opacity, smooth_shading=False, show_edges=False)
        actors[b.name] = (a, b)
    for nm, b in sc.world.bodies.items():
        blo, bhi = b.box()
        if np.any(bhi < lo) or np.any(blo > hi):
            continue
        if nm.startswith("VLM") and "table" not in nm and "post" not in nm:
            continue
        op = 0.25 if ("guard panels" in nm or "Rack side" in nm or "window" in nm.lower() or "Sliding guard door" in nm) else 1.0
        add(b, b.color if b.color.startswith("#") else "#b9c0c7", op)
    for b in arm.bodies():
        add(b, b.color if b.kind != "arm" else "#8f9aa5")
    for h in job.holds:
        add(h["body"], "#c8a040")
    if job.wand is not None and job.wand.name not in actors:
        add(job.wand, "#30343a")
    pl.camera_position = cam or [(-1150.0, -1500.0, 900.0), (0.0, -200.0, 40.0), (0, 0, 1)]
    pl.camera.view_angle = 30.0
    n = len(job.frames)
    idx = sorted(set(np.linspace(0, n - 1, min(max_frames, n)).astype(int).tolist()))
    frames_png = []

    def pose(k):
        f = job.frames[k]
        hold = f["hold"]
        for i, h in enumerate(job.holds):
            a, b = actors[h["body"].name]
            a.SetVisibility(i == hold)
            for nm in h["names"]:
                if nm in actors:
                    actors[nm][0].SetVisibility(i != hold)
        if hold >= 0:
            arm.held = (job.holds[hold]["body"], np.eye(4))
        else:
            arm.held = None
            job.set_wand(f.get("wand", False))
        sc.set_state(f["state"], f["ov"])
        arm.place(f["q"], f["close"])
        for nm, (a, b) in actors.items():
            a.user_matrix = b.M
    for k in idx:
        pose(k)
        pl.render()
        frames_png.append(pl.screenshot(return_img=True))
    imageio.mimsave(gif_path, frames_png, duration=0.12, loop=0)
    if png_path is not None and still_frame is not None:
        pose(still_frame)
        pl.window_size = [960, 720]
        pl.render()
        pl.screenshot(png_path)
    pl.close()
    job.restore()


# ------------------------------------------------------------------------------------------------ main
FOR_MODULES = {"plate_drawbar", "plate_bayonet", "module_swap"}


def run_job(cell, name, render_dir=None):
    """Try the job's variants (MiR position along the opening, approach) in order; keep the first that passes, else the best."""
    best = None
    tries = []
    for v in VARIANTS.get(name, [{}]):
        r = run_variant(cell, name, v, None)
        tries.append(dict(variant=v, ok=r.get("ok"), failed_step=r.get("failed_step"),
                          bad_frames=(r.get("audit") or {}).get("frames_in_collision")))
        if best is None or score(r) > score(best):
            best = r
        if r.get("ok"):
            break
    if render_dir is not None:
        best = run_variant(cell, name, best.get("variant", {}), render_dir)
    best["variants_tried"] = tries
    return best


def score(r):
    if r.get("ok"):
        return 1e9
    a = r.get("audit") or {}
    return (1e6 if r.get("planned_to_end") else 0) - 10 * (a.get("frames_in_collision", 1e5) + a.get("frames_movers", 0))


def run_variant(cell, name, variant, render_dir=None):
    t0 = time.time()
    job = None
    try:
        job = JOBS[name](cell, **variant)
        built = True
    except Fail as e:
        built = False
        print(f"  {name}: FAIL while planning: {e}", flush=True)
    except Exception as e:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        return dict(job=name, module=cell.module, variant=variant, ok=False, error=repr(e))
    if job is None:
        return dict(job=name, module=cell.module, variant=variant, ok=False, error="job not built")
    t1 = time.time()
    a = audit(job)
    secs = round(sum(f["dt"] for f in job.frames), 1)
    forces = [float(np.linalg.norm(f["force"])) for f in job.frames]
    ok = built and a["frames_in_collision"] == 0 and a["frames_movers"] == 0
    res = dict(job=name, module=cell.module, variant=variant, ok=ok, planned_to_end=built, failed_step=job.failed, steps=job.steps,
               arm_x=job.arm_x, n_frames=len(job.frames), robot_time_s=secs, max_force_N=round(max(forces), 1) if forces else 0.0,
               force_mode_N=FORCE_MODE_N, payload_kg=round(max((f["payload"] for f in job.frames), default=0.0), 3),
               tool_kg=round(job.tool_kg, 2), audit=a, plan_s=round(t1 - t0, 1), audit_s=round(time.time() - t1, 1), note=job.note)
    print(f"  {name} [{cell.module}]: {'PASS' if ok else 'FAIL'}; {len(job.frames)} frames, {a['frames_in_collision']} arm / "
          f"{a['frames_movers']} movers frames bad; clearance {a['min_clearance_mm']} mm {a['min_clearance_pair']}; torque "
          f"{a['peak_torque_pct']} % ({a['peak_torque_joint']}); {secs} s; plan {res['plan_s']} s, audit {res['audit_s']} s", flush=True)
    if not ok and a["first_bad"]:
        for b in a["first_bad"][:3]:
            print("     ", b, flush=True)
    if render_dir is not None:
        try:
            still = a["bad_frames"][0] if a["bad_frames"] else (a["min_clearance_frame"] or 0)
            stem = f"ops_{name}_{cell.module}"
            render(job, render_dir / f"{stem}.gif", render_dir / f"{stem}_tightest.png", still_frame=still)
            res["gif"] = f"{stem}.gif"
            res["still"] = f"{stem}_tightest.png"
            res["still_frame"] = still
        except Exception as e:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            res["render_error"] = repr(e)
    return res


LABEL = {"guard_door": "Guard door open (515 mm)", "guard_door_close": "Guard door close", "chamber_door_open": "Chamber door open",
         "chamber_door_close": "Chamber door close by the robot", "chamber_door_powered": "Chamber door close by its actuator", "plate_drawbar": "Plate out, drawbar", "plate_bayonet": "Plate out, bayonet",
         "drawer": "Cover-slide drawer out (whole drawer)", "reservoir": "Reservoir off the dock and out", "blade_cartridge": "Blade cartridge out",
         "module_swap": "Build module out", "overflow_jar": "Overflow jar out (as drawn)", "vacuum_clean": "Chamber vacuum (3 lanes)",
         "liner_right": "Right liner (slotted)"}


def write_md(results, path):
    L = ["# Robot jobs: planner and audit results", "",
         "Generated by `analysis/robot/ops.py` (byu-vcl PR 318's method: IK branches + lookahead, RRT-Connect, 1.5 mm audit, movers). "
         "Clearance is the FCL distance from the robot, its tools and what it holds to everything it may not touch; torque is the peak "
         "static joint torque against the UR12e's limits; the tip factor is the MiR250's tip-or-slide force over the job's force "
         "(or the centre of gravity's margin in 100 mm when no force acts).", "",
         "| Job | Module | MiR arm x (mm) | Result | Failing step / first collision | Frames bad (arm / movers) | Min clearance (mm), pair | "
         "Peak torque | Max force (N) | Payload (kg) | Tip factor | Robot time (s) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        a = r.get("audit") or {}
        fb = ""
        if r.get("failed_step"):
            fb = f"{r['failed_step']['step']}: {r['failed_step']['why'][:140]}"
        elif a.get("first_bad"):
            b = a["first_bad"][0]
            hit = (b["arm"] or b["movers"])[0] if (b["arm"] or b["movers"]) else ""
            fb = f"{b['label']}: {hit}"
        tip = a.get("tip") or {}
        pair = " / ".join(str(x)[:38] for x in (a.get("min_clearance_pair") or []) if x)
        L.append(f"| {LABEL.get(r['job'], r['job'])} | {r['module']} | {r.get('arm_x', '')} | {'**pass**' if r.get('ok') else 'fail'} | {fb} | "
                 f"{a.get('frames_in_collision', '')} / {a.get('frames_movers', '')} | {a.get('min_clearance_mm', '')}, {pair} | "
                 f"{a.get('peak_torque_pct', '')} % {a.get('peak_torque_joint', '') or ''} | {r.get('max_force_N', '')} | {r.get('payload_kg', '')} | "
                 f"{tip.get('factor', '')} | {r.get('robot_time_s', '')} |")
    pathlib.Path(path).write_text("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default=",".join(j for j in JOBS if j not in ("chamber_door_close", "liner_right")))
    ap.add_argument("--modules", default="M50,S25,L75")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [j for j in args.jobs.split(",") if j]
    results = []
    t0 = time.time()
    for module in args.modules.split(","):
        todo = [j for j in jobs if module == "M50" or j in FOR_MODULES]
        if not todo:
            continue
        cell = Cell(module)
        for name in todo:
            results.append(run_job(cell, name, OUT if args.render else None))
            (OUT / f"ops{args.tag}.json").write_text(json.dumps(dict(results=results, runtime_s=round(time.time() - t0, 1)),
                                                                   indent=1, default=str))
            write_md(results, OUT / f"ops{args.tag}.md")
        del cell
    print(f"done in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
