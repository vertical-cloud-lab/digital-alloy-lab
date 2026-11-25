"""Round 7 (2026-11-25): the robot shop's machining story planned, checked and recorded for the video (issue #260, PR #266).

Sterling: "two mobile manipulators shown carrying out all machining steps, assembly (screwing fasteners in, placing
seals, tightening things), and showing where a human is absolutely necessary (e.g., the loading of the initial massive
block onto [the mill])", with time estimates. This plans every robot motion the shop chapters show, in the shop of
shop_cell.py rebuilt from cad/robotbuild/equipment.py's models (published drawings and spec sheets), and records each
clip frame by frame for cad/robotbuild/shop_chapters.py.

Checks, as shop_checks.py runs them (byu-vcl PR 318's rules):
  * FCL on meshes: each arm with its gripper or tool and the part it holds, against the machine, the fixtures, both MiRs
    and the other arm; every IK branch tried; RRT-Connect (cell.Checker.plan) with 0.5 deg edges; every finished one-arm
    segment re-checked at 0.2 deg (shop_checks.fine_audit); a handled part may touch its fixture, the deck or the jaws
    only up to 1.5 mm deep (cell.DEPTH_MM);
  * two-arm carries on a straight line sampled every 10 mm, both arms on their nearest IK branch (no jump over 10 deg);
  * static joint torques (shop_checks.joint_torques: UR's link masses, each loading only the joints upstream of it) at
    every recorded pose, and PR 318's tip-over check of each MiR (131 kg ballast plate) at the worst pose;
  * the person's lifts (vacuum tube lifter on a jib) are scripted, but the load's path is checked against the machine
    with FCL too.

Frames: shop frame (shop_cell), mm. Each clip is written to /tmp/robotbuild/traj/shop_<clip>.pkl (never committed):
    dict(clip, station, fps, frames=[dict(arms={A: dict(q, close, base, tool, mir)}, objs={name: 4x4},
         mach={...}, person={...}, meta={...})], objects={name: spec}, result={...})
and a summary of every plan to analysis/out/shop/shop_plan.json.

Run:  OMP_NUM_THREADS=1 /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/analysis/shop/shop_plan.py [clip ...]
"""
from __future__ import annotations

import copy
import json
import math
import pathlib
import pickle
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LPBF / "cad" / "robotbuild"))
import shop_cell as S  # noqa: E402
import shop_checks as K  # noqa: E402  (sets cell.STEP_RAD to 0.5 deg)
import cell as C  # noqa: E402
from cell import Arm, Body, Checker, Group, Tm, inv  # noqa: E402
import equipment as E  # noqa: E402

FPS = 12
TRAJ = pathlib.Path("/tmp/robotbuild/traj")
OUT = HERE.parent / "out" / "shop"
INCH = 25.4
RHO_AL = 2.70e-6

# ----------------------------------------------------------------------------------------------- the detailed shop
# Station poses are shop_cell.build_shop()'s, except: the wash and deburr bench moves 400 mm east (the ST-10's chip
# conveyor reaches 2183 mm right of its chuck face), and three stations are added: the jib crane with the vacuum tube
# lifter at the VF-4's left, the robots' tool stand, and the TIG welding table.
POSE = dict(vf4=(2600.0, 7000.0, 0.0), lathe=(6700.0, 7000.0, 0.0), wash=(10100.0, 7000.0, 0.0),
            measure=(11900.0, 7000.0, 0.0), bench=(14200.0, 7000.0, 0.0), receiving=(2400.0, 4000.0, 180.0),
            stock=(5600.0, 4000.0, 180.0), saw=(8600.0, 4000.0, 180.0), kit=(11400.0, 4000.0, 180.0),
            charge=(14000.0, 4000.0, 180.0), jib=(550.0, 6700.0, 0.0), tools=(12900.0, 4000.0, 180.0),
            tig=(16300.0, 7000.0, 0.0))
JIB = dict(under_boom=10 * 12 * INCH, span=10 * 12 * INCH)   # Gorbel WSJ360-500-10-10: 10 ft under the boom so it clears
                                                             # the VF-4's column hood (2740 mm); 10 ft span


def station(key):
    return S.Station(key, POSE[key], [], {})


def shop_world(key, parts, st=None):
    """FCL items of a station's equipment parts in the shop frame."""
    st = st or station(key)
    return E.fcl_items(parts, st.M, prefix=f"{key}/")


# ----------------------------------------------------------------------------------------------- 3FG15 arm
class Arm3FG(Arm):
    """A UR12e with an ATI QC-11 tool plate and an OnRobot 3FG15 instead of the 2F-85: a 156 mm puck (75 mm long) and
    three fingers. External grip 4-152 mm, 10 kg force-fit (OnRobot). close 0 = fingers on a 152 mm circle, 1 = 4 mm.
    The TCP is 160 mm out from the flange (the finger pads' centre, est.)."""
    PUCK = (22.0, 97.0, 78.0)            # QC-11 plate + puck: z from, z to, radius (est. from the 156 mm class body)
    FING = (97.0, 187.0, 9.0, 10.0)      # fingers: z from, z to, half width, half depth (est.)

    def __init__(self, name, base, yaw_deg):
        super().__init__(name, base=base, yaw_deg=yaw_deg)
        for b in list(self.grip.values()):
            self.robot.remove(b.name)
        v, f = S.cyl(self.PUCK[2], (0, 0, self.PUCK[0] + 2.0), (0, 0, self.PUCK[1]), n=24)
        self.grip = {"puck": Body(f"{name}/gr/puck", v, f, kind="gripper", group="gripper", color="#3c4650")}
        fv, ff = C.box_mesh(-self.FING[2], self.FING[2], -self.FING[3], self.FING[3], self.FING[0], self.FING[1])
        for k in range(3):
            self.grip[f"finger{k}"] = Body(f"{name}/gr/finger{k}", fv, ff, kind="gripper", group="gripper", color="#9aa3ab")
        for b in self.grip.values():
            self.robot.add(b)

    def finger_r(self, close=None):
        c = self.close if close is None else close
        return 76.0 - c * 74.0 + self.FING[2]

    def tcp_mm(self, close=None):
        return 160.0 + (self.FING[1] - 187.0)

    def gap_mm(self, close=None):
        return 2 * (self.finger_r(close) - self.FING[2])

    def close_for_gap(self, gap):
        return float(np.clip((152.0 - gap) / 148.0, 0.0, 1.0))

    def place(self, q=None, close=None):
        if q is not None:
            self.q = np.asarray(q, float)
        if close is not None:
            self.close = float(close)
        F = self.fk()
        for k, b in self.links.items():
            b.place(self.base @ F[k])
        Wt = self.base @ F["tool0"]
        self.grip["puck"].place(Wt)
        r = self.finger_r()
        for k in range(3):
            a = math.radians(90 + 120 * k)
            self.grip[f"finger{k}"].place(Wt @ Tm(C.rot((0, 0, 1), math.degrees(a)), (r * math.cos(a), r * math.sin(a), 0.0)))
        if self.held is not None:
            hb, off = self.held
            hb.place(Wt @ self.tcp_off() @ off)
        return F


class ArmVGP(Arm):
    """A UR12e with an ATI QC-11 tool plate and an OnRobot VGP20 electric vacuum gripper: 264 x 184 x 92 mm (datasheet)
    and four Ø36 cups (est.). For dry stock only: OnRobot's datasheet rules out wet CNC parts. TCP: the cups' face."""
    BODY = (24.0, 116.0, 92.0, 132.0)     # z from, z to, half widths x, y
    CUPS = (116.0, 136.0, 18.0, ((-50.0, -60.0), (-50.0, 60.0), (50.0, -60.0), (50.0, 60.0)))

    def __init__(self, name, base, yaw_deg):
        super().__init__(name, base=base, yaw_deg=yaw_deg)
        for b in list(self.grip.values()):
            self.robot.remove(b.name)
        z0, z1, hx, hy = self.BODY
        bv, bf = C.box_mesh(-hx, hx, -hy, hy, z0 + 2.0, z1)
        cz0, cz1, cr, xy = self.CUPS
        cups = C.merge([S.cyl(cr, (x, y, cz0), (x, y, cz1), n=16) for x, y in xy])
        self.grip = {"body": Body(f"{name}/gr/body", bv, bf, kind="gripper", group="gripper", color="#33373b"),
                     "cups": Body(f"{name}/gr/cups", *cups, kind="gripper", group="gripper", color="#1f2326")}
        for b in self.grip.values():
            self.robot.add(b)

    def tcp_mm(self, close=None):
        return self.CUPS[1]

    def gap_mm(self, close=None):
        return 0.0

    def close_for_gap(self, gap):
        return 0.0

    def place(self, q=None, close=None):
        if q is not None:
            self.q = np.asarray(q, float)
        if close is not None:
            self.close = float(close)
        F = self.fk()
        for k, b in self.links.items():
            b.place(self.base @ F[k])
        Wt = self.base @ F["tool0"]
        for b in self.grip.values():
            b.place(Wt)
        if self.held is not None:
            hb, off = self.held
            hb.place(Wt @ self.tcp_off() @ off)
        return F


class Arm3FGLong(Arm3FG):
    """The 3FG15 with custom fingertips 40 mm longer (ours: the robot may use custom tools), so its 156 mm puck stays
    above a 3-jaw chuck's jaws while a short disc is pushed into them."""
    FING = (97.0, 227.0, 9.0, 10.0)


def make_arm(name, base, yaw, gripper="2F-85"):
    if gripper == "3FG15":
        return Arm3FG(name, tuple(base), yaw)
    if gripper == "3FG15L":
        return Arm3FGLong(name, tuple(base), yaw)
    if gripper == "VGP20":
        return ArmVGP(name, tuple(base), yaw)
    return Arm(name, base=tuple(base), yaw_deg=yaw)


# ----------------------------------------------------------------------------------------------- clip recorder
class Clip:
    """Frames of one clip: arms (q, close, base, tool), MiR poses, objects' poses, machine and person state, meta."""

    def __init__(self, name, station_key, chapter):
        self.name, self.station, self.chapter = name, station_key, chapter
        self.frames = []
        self.state = dict(arms={}, mirs={}, objs={}, mach={}, person={})
        self.objects = {}           # name -> spec dict for the renderer (kind, dims or file, colour)
        self.result = {}
        self.meta = dict(caption="", sub="", who=[], step="", status="", proc_s=1.0 / FPS, add={})

    def set_arm(self, key, arm, tool="2F-85", mir=None, visible=True):
        self.state["arms"][key] = dict(q=np.asarray(arm.q, float).copy(), close=float(arm.close), base=arm.base.copy(),
                                       tool=tool, visible=visible)
        if mir is not None:
            self.state["mirs"][key] = mir

    def obj(self, name, M, spec=None):
        self.state["objs"][name] = np.asarray(M, float).copy()
        if spec is not None:
            self.objects[name] = spec

    def drop(self, name):
        self.state["objs"].pop(name, None)

    def frame(self, n=1, **meta):
        m = dict(self.meta)
        m.update(meta)
        for _ in range(max(1, int(n))):
            self.frames.append(dict(arms=copy.deepcopy(self.state["arms"]), mirs=copy.deepcopy(self.state["mirs"]),
                                    objs=copy.deepcopy(self.state["objs"]), mach=copy.deepcopy(self.state["mach"]),
                                    person=copy.deepcopy(self.state["person"]), meta=dict(m)))

    def seconds(self):
        return sum(f["meta"].get("proc_s", 1.0 / FPS) for f in self.frames)

    def save(self):
        TRAJ.mkdir(parents=True, exist_ok=True)
        path = TRAJ / f"shop_{self.name}.pkl"
        with open(path, "wb") as fh:
            pickle.dump(dict(clip=self.name, station=self.station, chapter=self.chapter, fps=FPS, frames=self.frames,
                             objects=self.objects, result=self.result), fh)
        return path


def resample(qs, t_s):
    """Joint waypoints -> one q per frame over t_s seconds, evenly in the largest joint's angle."""
    qs = [np.asarray(q, float) for q in qs]
    n = max(1, int(round(t_s * FPS)))
    if len(qs) == 1:
        return [qs[0]] * n
    d = [0.0] + [float(np.abs(b - a).max()) for a, b in zip(qs[:-1], qs[1:])]
    cum = np.cumsum(d)
    L = cum[-1]
    out = []
    for i in range(1, n + 1):
        s = L * (0.5 - 0.5 * math.cos(math.pi * i / n))       # ease in and out
        k = int(np.searchsorted(cum, s, side="right")) - 1
        k = min(max(k, 0), len(qs) - 2)
        u = 0.0 if cum[k + 1] - cum[k] < 1e-12 else (s - cum[k]) / (cum[k + 1] - cum[k])
        out.append(qs[k] + (qs[k + 1] - qs[k]) * u)
    return out


# ----------------------------------------------------------------------------------------------- one arm's job
class Job:
    """One arm (and its MiR, docked at a station) working in that station's equipment, with cell.Checker."""

    def __init__(self, name, key, parts, x_mir, arm_dx=S.ARM_DX, gripper="2F-85", gap=S.DOCK_GAP, extra=(), others=(),
                 other_mirs=(), arm_key="A"):
        self.name, self.key, self.parts = name, key, parts
        self.st = station(key)
        self.x_mir, self.arm_dx, self.gap = x_mir, arm_dx, gap
        self.Mm = S.dock_frame(self.st, x_mir, gap)
        self.items = shop_world(key, parts, self.st) + list(extra)
        self.sc = S.ShopScene(self.items, mirs=[(self.Mm, arm_dx)] + list(other_mirs), others=others)
        base, yaw = S.arm_base_world(self.st, x_mir, gap, arm_dx)
        self.arm = make_arm(arm_key, base, yaw, gripper)
        self.gripper = gripper
        self.chk = Checker(self.sc, self.arm)
        self.plan = K.Plan(name)
        self.arm_key = arm_key
        self.payload = {}          # segment index -> kg held

    # ---- geometry
    def deck(self, local=(110.0, 0.0), z=0.0):
        return S.deck_point(self.st, self.x_mir, local=local, gap=self.gap, arm_dx=self.arm_dx) + np.array([0, 0, z])

    def T_world(self, p_local, R_local=None):
        """A pose given in the station frame -> shop frame."""
        return self.st.M @ Tm(R_local, p_local)

    def home(self, close):
        return K.home_pose(self.chk, self.arm, self.st, self.x_mir, close, arm_dx=self.arm_dx)

    def add_obstacle(self, name, vf, kind="fixture"):
        b = Body(name, *vf, kind=kind, color="#888888")
        self.sc.world.add(b)
        return b


def ik_line(chk, arm, T_from, T_to, close, allow_from=frozenset(), allow_line=frozenset(), seed=None):
    """shop_checks.ik_line, keeping every branch's reason: (q_from, qs, reasons)."""
    arm.close = close
    sols = arm.ik_all(T_from, seed)
    reasons = [] if sols else ["no IK solution (out of reach)"]
    for q in sols:
        col = chk.collisions(q, close, allow_from)
        if col:
            reasons.append(dict(start=[(a, b) for a, b, d in col[:2]]))
            continue
        qs, info = K.cart(chk, arm, K.line(T_from, T_to), close, allow_line, q)
        if qs is not None:
            return q, qs, None
        info = dict(info)
        if "hits" in info:
            info["hits"] = [(a, b) for a, b, d in info["hits"][:2]]
        reasons.append(info)
    return None, None, reasons


K_ik_line = ik_line


def seg_time(kind, qs, dist_mm=None):
    if kind == "linear" and dist_mm is not None:
        return max(0.4, dist_mm / K.LIN_SPEED)
    return K.path_time(qs) if qs and len(qs) > 1 else 0.0


def pick_place(job, part, kg, T_from, T_to, G, close_open, close_grip, allow_from=(), allow_to=(), up_from=120.0,
               up_to=120.0, release_note="gripper opens", grip_note="close", iters=5000, q_start=None, return_home=True,
               approach_to=None, via=None):
    """The P1 sequence, generalised: home -> above the part at T_from -> down -> grip -> up -> RRT-Connect to above
    T_to -> down -> release -> up -> home. G: part frame -> TCP. allow_*: world names the held part may touch (1.5 mm).
    approach_to: (dx, dy, dz) of the approach into T_to instead of straight down (e.g. along a spindle axis)."""
    arm, chk, plan = job.arm, job.chk, job.plan
    part.place(T_from)
    job.sc.world.add(part)
    q_home = job.home(close_open) if q_start is None else np.asarray(q_start, float)
    if q_home is None:
        plan.add("ik", [], close_open, "carry pose over the deck", ok=False)
        return None
    arm.q = q_home.copy()
    T_pick = T_from @ G
    allow_pick = frozenset({("tool", part.name)} | {("tool", a) for a in allow_from})
    q_pre, qs_down, why = ik_line(chk, arm, K.lift(T_pick, up_from), T_pick, close_open, allow_pick, allow_pick, q_home)
    if q_pre is None:
        plan.add("ik", [], close_open, f"above {part.name} at the pick", ok=False, info=dict(why=str(why)[:900]))
        return None
    path, info = chk.plan(q_home, q_pre, close_open, allow_pick, iters=iters)
    plan.add("joint", path or [], close_open, "home -> above the part", ok=path is not None, info=info)
    if path is None:
        return None
    plan.add("linear", qs_down, close_open, f"down {up_from:.0f} mm onto the part", t=up_from / K.LIN_SPEED)
    q_pick = qs_down[-1]
    plan.add("grip", [q_pick], close_grip, grip_note, t=0.8)
    job.sc.world.remove(part.name)
    arm.place(q_pick, close_grip)
    held = K.attach(arm, part, T_from)
    allow_lift = frozenset({("held", a) for a in allow_from})
    qs, info = K.cart(chk, arm, K.line(T_pick, K.lift(T_pick, up_from)), close_grip, allow_lift, q_pick)
    plan.add("linear", qs or [], close_grip, f"lift {up_from:.0f} mm", ok=qs is not None, info=info, held=held,
             t=up_from / K.LIN_SPEED)
    job.payload[len(plan.segments) - 1] = kg
    if qs is None:
        return None
    q_up = qs[-1]
    T_place = T_to @ G
    a = np.array(approach_to if approach_to is not None else (0.0, 0.0, up_to), float)
    T_pre = K.lift(T_place, dz=a[2], dx=a[0], dy=a[1])
    allow_place = frozenset({("held", x) for x in allow_to})
    qs_via = None
    if via is not None:
        # a staging pose outside the machine (T_pre moved by `via`), then straight in to T_pre and on to the place pose
        T_via = K.lift(T_pre, dz=via[2], dx=via[0], dy=via[1])
        arm.close = close_grip
        reasons = []
        q_above = None
        for qv in arm.ik_all(T_via, q_up):
            colv = chk.collisions(qv, close_grip, frozenset())
            if colv:
                reasons.append(f"via pose collides: {[(a_, b_) for a_, b_, d_ in colv[:2]]}")
                continue
            q1, i1 = K.cart(chk, arm, K.line(T_via, T_pre), close_grip, frozenset(), qv)
            if q1 is None:
                reasons.append(str(i1)[:160])
                continue
            q2, i2 = K.cart(chk, arm, K.line(T_pre, T_place), close_grip, allow_place, q1[-1])
            if q2 is None:
                reasons.append(str(i2)[:160])
                continue
            q_above, qs_via, qs_in = qv, q1, q2
            break
        if q_above is None:
            plan.add("ik", [], close_grip, "staging pose outside the machine", ok=False, info=dict(why=str(reasons)[:900]),
                     held=held)
            return None
    else:
        q_above, qs_in, why = ik_line(chk, arm, T_pre, T_place, close_grip, frozenset(), allow_place, q_up)
        if q_above is None:
            plan.add("ik", [], close_grip, "above the place pose with the part", ok=False, info=dict(why=str(why)[:900]),
                     held=held)
            return None
    t0 = time.time()
    path, info = chk.plan(q_up, q_above, close_grip, frozenset(), iters=iters)
    info["plan_s"] = round(time.time() - t0, 1)
    plan.add("joint", path or [], close_grip, "carry to the staging pose" if via is not None else
             "carry to above the place pose", ok=path is not None, info=info, held=held)
    job.payload[len(plan.segments) - 1] = kg
    if path is None:
        return None
    if qs_via is not None:
        d = float(np.linalg.norm(via))
        plan.add("linear", qs_via, close_grip, f"straight in {d:.0f} mm through the door", held=held, t=d / 250.0)
        job.payload[len(plan.segments) - 1] = kg
    plan.add("linear", qs_in, close_grip, f"in {float(np.linalg.norm(a)):.0f} mm to the place pose", held=held,
             t=float(np.linalg.norm(a)) / K.LIN_SPEED)
    job.payload[len(plan.segments) - 1] = kg
    q_place = qs_in[-1]
    plan.add("release", [q_place], close_grip, release_note, t=1.5)
    K.detach(arm)
    part.place(T_to)
    job.sc.world.add(part)
    allow_rel = frozenset({("tool", part.name)})
    if via is not None:          # empty gripper: up 60 mm off the part, then straight back out of the door
        T_up = K.lift(T_place, 60.0)
        qs, info = K.cart(chk, arm, K.line(T_place, T_up), close_open, allow_rel, q_place)
        plan.add("linear", qs or [], close_open, "up 60 mm off the part", ok=qs is not None, info=info, t=60.0 / K.LIN_SPEED)
        if qs is None:
            return dict(q_place=q_place, q_home=q_home, held=held)
        T_out = K.lift(T_up, dz=via[2], dx=via[0] + a[0], dy=via[1] + a[1])
        qs, info = K.cart(chk, arm, K.line(T_up, T_out), close_open, frozenset(), qs[-1])
        plan.add("linear", qs or [], close_open, "straight back out of the door", ok=qs is not None, info=info,
                 t=float(np.linalg.norm(via)) / 250.0)
    else:
        qs, info = K.cart(chk, arm, K.line(T_place, T_pre), close_open, allow_rel, q_place)
        plan.add("linear", qs or [], close_open, "back out", ok=qs is not None, info=info,
                 t=float(np.linalg.norm(a)) / K.LIN_SPEED)
    if qs is None or not return_home:
        return dict(q_place=q_place, q_home=q_home, held=held)
    path, info = chk.plan(qs[-1], q_home, close_open, frozenset(), iters=iters)
    plan.add("joint", path or [], close_open, "out to home", ok=path is not None, info=info)
    return dict(q_place=q_place, q_home=q_home, held=held)


def tool_passes(job, tool_body, waypoints, close, allow=(), q_start=None, iters=5000, dwell=(), push_dir=None, kg=0.3):
    """A tool held in the gripper (tool_body, posed in the TCP frame) visits a list of Cartesian moves:
    waypoints = [(label, T_approach, T_work)] -> RRT to the approach, straight in, dwell, straight out."""
    arm, chk, plan = job.arm, job.chk, job.plan
    held = None
    q = None
    if q_start is not None:
        q = np.asarray(q_start, float)
    else:
        # start with the tool in hand 250 mm above the first approach, on the first branch that is clear with the tool
        T0 = K.lift(waypoints[0][1], 250.0)
        arm.close = close
        for qc in arm.ik_all(T0, job.home(close) if job.home(close) is not None else arm.q):
            arm.place(qc, close)
            if held is None:
                held = K.attach(arm, tool_body, arm.tcp())
            if not chk.collisions(qc, close, frozenset()):
                q = qc
                break
    if q is None:
        plan.add("ik", [], close, "start pose with the tool in hand", ok=False)
        return None
    arm.q = q.copy()
    arm.place(q, close)
    if held is None:
        held = K.attach(arm, tool_body, arm.tcp())
    plan.add("dwell", [q], close, "tool in hand", held=held, t=0.5)
    allow_w = frozenset({("held", a) for a in allow} | {("tool", a) for a in allow})
    for i, (label, T_app, T_work) in enumerate(waypoints):
        q_a, qs_in, why = ik_line(chk, arm, T_app, T_work, close, frozenset(), allow_w, q)
        if q_a is None:
            plan.add("ik", [], close, f"{label}: approach", ok=False, info=dict(why=str(why)[:900]), held=held)
            return None
        path, info = chk.plan(q, q_a, close, frozenset(), iters=iters)
        plan.add("joint", path or [], close, f"{label}: to the approach", ok=path is not None, info=info, held=held)
        job.payload[len(plan.segments) - 1] = kg
        if path is None:
            return None
        dist = float(np.linalg.norm(T_work[:3, 3] - T_app[:3, 3]))
        plan.add("linear", qs_in, close, f"{label}: in {dist:.0f} mm", held=held, t=dist / 60.0)
        job.payload[len(plan.segments) - 1] = kg
        plan.add("dwell", [qs_in[-1]], close, f"{label}: {dwell[i] if i < len(dwell) else 'work'}",
                 held=held, t=(dwell[i][1] if i < len(dwell) and isinstance(dwell[i], tuple) else 1.5))
        qs_out = qs_in[::-1]
        plan.add("linear", qs_out, close, f"{label}: out {dist:.0f} mm", held=held, t=dist / K.LIN_SPEED)
        q = qs_out[-1]
    q_home = job.home(close)
    if q_home is not None:
        path, info = chk.plan(q, q_home, close, frozenset(), iters=iters)
        plan.add("joint", path or [], close, "back to the carry pose", ok=path is not None, info=info, held=held)
    return dict(held=held)


def audit(job):
    """shop_checks.fine_audit at 0.2 deg with this job's allow lists (from the notes), plus the worst torque per kg."""
    bad = []
    arm, chk = job.arm, job.chk
    worst = 0.0
    world = job.sc.world.bodies
    parked_M = {n: b.M.copy() for n, b in world.items()}      # where each part was finally put (restored after)
    for k, sg in enumerate(job.plan.segments):
        if not sg["qs"] or isinstance(sg["qs"][0], tuple) or len(sg["qs"]) < 2:
            continue
        parked = None
        if sg["held"] is not None:
            arm.held = sg["held"]
            if arm.held[0].name not in arm.robot.bodies:
                arm.robot.add(arm.held[0])
            if arm.held[0].name in world:              # the same body sits in the world where it was put down later:
                parked = world.pop(arm.held[0].name)   # while held it is part of the robot, not an obstacle
        else:
            if arm.held is not None:
                arm.robot.remove(arm.held[0].name)
            arm.held = None
        allow = job_allow(job, sg)
        n = 0
        for q in C.densify(sg["qs"], math.radians(0.2)):
            col = [c for c in chk.collisions(q, sg["close"], allow) if c[0] != c[1]]
            if col:
                n += 1
                if n == 1:
                    bad.append(dict(segment=k, note=sg["note"], first=[(a, b, d) for a, b, d in col[:2]]))
        if n:
            bad[-1]["samples"] = n
        kg = job.payload.get(k, 0.0)
        for q in sg["qs"][:: max(1, len(sg["qs"]) // 6)]:
            worst = max(worst, K.tau_frac(arm, q, kg))
        if parked is not None:
            world[parked.name] = parked
            parked.place(parked_M[parked.name])
    if arm.held is not None:
        arm.robot.remove(arm.held[0].name)
        arm.held = None
    return bad, worst


TRANSIT_SKIP = ("parts deck", "deck blocks", "parallel", "riser", "dummy-floor", "fixture plate", "vise", "jaw", "chuck",
                "lift table", "box:", "infeed", "saw bed", "tank", "basket", "granite", "long table", "slot ", "brush",
                "deburr spindle", "clamp")   # what a held part is set on or taken from: the transit's figure is the machine


def transit_clearance(job):
    """Smallest distance (mm) from the arm, its gripper or tool and the held part to anything else, over the joint-space
    (RRT-Connect) segments, densified at 1 deg: the moves through the door, not the planned contacts."""
    arm, chk = job.arm, job.chk
    world = job.sc.world.bodies
    parked_M = {n: b.M.copy() for n, b in world.items()}
    best = (math.inf, None, None, None)
    for k, sg in enumerate(job.plan.segments):
        if sg["kind"] != "joint" or not sg["qs"] or len(sg["qs"]) < 2:
            continue
        parked = None
        if sg["held"] is not None:
            arm.held = sg["held"]
            if arm.held[0].name not in arm.robot.bodies:
                arm.robot.add(arm.held[0])
            parked = world.pop(arm.held[0].name, None)
        elif arm.held is not None:
            arm.robot.remove(arm.held[0].name)
            arm.held = None
        for q in C.densify(sg["qs"], math.radians(1.0))[::2]:
            d, a, b = K.clearance(chk, arm, q, sg["close"], exclude=TRANSIT_SKIP)
            if d < best[0]:
                best = (d, a, b, sg["note"])
        if parked is not None:
            world[parked.name] = parked
            parked.place(parked_M[parked.name])
    if arm.held is not None:
        arm.robot.remove(arm.held[0].name)
        arm.held = None
    return dict(clear_mm=round(best[0], 1), robot_body=best[1], world_body=best[2], segment=best[3])


def job_allow(job, sg):
    """What a segment was planned to touch: the held part's fixture/deck (1.5 mm rule) and the tool on its target."""
    out = set()
    for n, b in job.sc.world.bodies.items():
        if b.kind == "held" or any(k in n for k in (
                "parts deck", "vise", "riser", "parallel", "fixture", "jaw", "dummy-floor", "lift table", "deck blocks", "box:",
                "saw bed", "infeed", "shuttle", "brush", "spindle", "basket", "tank", "granite", "tote", "long table", "platter",
                "clamp", "chuck")):
            out.add(("held", n))
            out.add(("tool", n))
    return frozenset(out)


def record_job(clip, job, akey, tool="2F-85", meta_by_seg=None, objs_follow=None):
    """Turn a planned job into frames: each segment resampled at real time; the held part follows the TCP."""
    arm = job.arm
    for k, sg in enumerate(job.plan.segments):
        if not sg["qs"] or isinstance(sg["qs"][0], tuple):
            continue
        m = (meta_by_seg or {}).get(k) or (meta_by_seg or {}).get("*") or {}
        t = max(sg["t"], 1.0 / FPS)
        if sg["kind"] in ("grip", "release", "dwell", "vise", "chuck"):
            n = max(1, int(round(t * FPS)))
            q0 = np.asarray(sg["qs"][0], float)
            c0 = arm.close
            for i in range(n):
                c = c0 + (sg["close"] - c0) * (i + 1) / n if sg["kind"] in ("grip", "release") else sg["close"]
                arm.place(q0, c)
                _held_follow(clip, arm, sg, objs_follow)
                clip.set_arm(akey, arm, tool)
                clip.frame(**m)
            continue
        for q in resample(sg["qs"], t):
            arm.place(q, sg["close"])
            _held_follow(clip, arm, sg, objs_follow)
            clip.set_arm(akey, arm, tool)
            clip.frame(**m)


def _held_follow(clip, arm, sg, objs_follow):
    if sg.get("held") is not None:
        hb, off = sg["held"]
        name = (objs_follow or {}).get(hb.name, hb.name)
        clip.obj(name, arm.base @ arm.fk()["tool0"] @ arm.tcp_off() @ off)


def summarize(job, extra=None):
    bad, worst = audit(job)
    r = dict(name=job.name, ok=job.plan.ok and not bad, fail=job.plan.fail, time_s=round(job.plan.time_s(), 1),
             gripper=job.gripper, fine_audit_0p2deg=bad, worst_torque_frac=round(worst, 3),
             segments=[dict(kind=s["kind"], note=s["note"], ok=s["ok"], t_s=round(s["t"], 1),
                            info={k: (v if isinstance(v, (int, float, str, bool, type(None))) else str(v)[:200])
                                  for k, v in s["info"].items()}) for s in job.plan.segments])
    if extra:
        r.update(extra)
    return r
