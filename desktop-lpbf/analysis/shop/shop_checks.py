"""Feasibility checks for two UR12e + 2F-85 arms on MiR250s making the desktop LPBF's parts (issue #260, PR #266).

What it does, per step class (see robot-shop.md):
  * payload: every stock piece and shipped box against the 2F-85's rating, one arm's net payload and two arms' together,
    and the static joint torques (cell.static_torques) at the poses the plans use;
  * FCL-checked motion plans with cell.py's Arm and Checker in this folder's own scene (shop_cell.ShopScene):
      P1  VF-4: one arm carries the chamber frame blank (version B) from its deck into the vise and back out;
      P2  lathe: one arm loads a 2-1/8 in. 6061 bar slug into the chuck;
      P3  VF-4: two arms hold the roughed chamber block (version A) in the vise and lift it out toward the door;
      P4  receiving: a cutter held in the gripper runs along a box's tape seam;
      P5  reach checks at the saw, wash tank, granite plate, kitting rack, bench and stock rack;
      P6  VF-4: two arms lift the optics bridge's 19.7 kg plate off a fixture plate by two lifting tabs;
  * MiR routes between stations (shop_cell.route / drive_time) and PR 318's tip-over check at the poses used;
  * the tightest moment of each plan (smallest clearance to anything not being handled) for the renders.

Run:  OMP_NUM_THREADS=1 /tmp/capmem 2 xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python \
          desktop-lpbf/analysis/shop/shop_checks.py [--no-render]          (about 3 min)
      ... shop_checks.py --refresh-payload    only the payload table, after dfm.json changes (seconds)
Writes desktop-lpbf/analysis/out/shop/shop_checks.json and the PNGs.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import shop_cell as S  # noqa: E402
import cell as C  # noqa: E402
from cell import Arm, Body, Checker, Group, Tm, densify, group_distance, inv  # noqa: E402

OUT = HERE.parent / "out" / "shop"
C.STEP_RAD = math.radians(0.5)       # plan and check edges every 0.5 deg (cell.py's default is 1.5 deg; a 1.5 deg step let
                                     # a forearm graze the lathe's door header between samples in the run of 22:42 UTC)
RHO = dict(al6061=2.70e-6, mic6=2.66e-6, ss316=8.0e-6)       # kg/mm^3
TOOL_KG = 1.3            # 2F-85 + coupling + D405 bracket at the flange (cell.static_torques default)
GRIP_KG = 5.0            # Robotiq 2F-85 rated payload (Edison r3-robot-tending; Robotiq spec)
ARM_KG = C.UR12E["payload_kg"]
JOINT_SPEED = math.radians(60.0)     # rad/s, a shop-floor tending speed with people about (assumption)
LIN_SPEED = 150.0                    # mm/s for guarded approach and retreat moves (assumption)


# ----------------------------------------------------------------------------------------------- small helpers
def T_at(p, z=(0, 0, -1), x=(1, 0, 0)):
    return Tm(C.frame(z, x), p)


def lift(T, dz=0.0, dx=0.0, dy=0.0):
    T2 = T.copy()
    T2[:3, 3] += (dx, dy, dz)
    return T2


def line(T0, T1, step=5.0):
    n = max(1, int(math.ceil(np.linalg.norm(T1[:3, 3] - T0[:3, 3]) / step)))
    out = []
    for i in range(n + 1):
        s = i / n
        T = np.eye(4)
        T[:3, :3] = C.slerp(T0[:3, :3], T1[:3, :3], s) if not np.allclose(T0[:3, :3], T1[:3, :3]) else T0[:3, :3]
        T[:3, 3] = T0[:3, 3] + (T1[:3, 3] - T0[:3, 3]) * s
        out.append(T)
    return out


def path_time(qs, close_moves=0):
    t = 0.0
    for a, b in zip(qs[:-1], qs[1:]):
        t += float(np.abs(np.asarray(b) - np.asarray(a)).max()) / JOINT_SPEED
    return t + 0.6 * close_moves


class Plan:
    """A recorded sequence of segments for one arm (or two), with checks and timing."""

    def __init__(self, name):
        self.name = name
        self.segments = []         # dict(kind, qs (list of q or (qa, qb)), close, note, ok, info)
        self.ok = True
        self.fail = None

    def add(self, kind, qs, close, note, ok=True, info=None, held=None, t=None):
        self.segments.append(dict(kind=kind, qs=qs, close=close, note=note, ok=ok, info=info or {}, held=held,
                                  t=t if t is not None else (path_time(qs) if qs and not isinstance(qs[0], tuple) else 0.0)))
        if not ok and self.ok:
            self.ok, self.fail = False, note

    def time_s(self):
        return float(sum(s["t"] for s in self.segments))


def home_pose(chk, arm, st, x_mir, close, arm_dx=None):
    """The carry pose: TCP 330 mm above the deck's centre, pointing down, elbow up (the first free IK branch)."""
    arm_dx = S.ARM_DX if arm_dx is None else arm_dx
    p = S.deck_point(st, x_mir, local=(110.0, 0.0), arm_dx=arm_dx) + np.array([0.0, 0.0, 330.0])
    seed = np.radians([0.0, -100.0, 110.0, -100.0, -90.0, 0.0])
    q, nb, why = ik_free(chk, arm, T_at(p, (0, 0, -1), st.R() @ np.array([1.0, 0, 0])), close, frozenset(), seed)
    return q


def joint_torques(arm, q, payload_kg=0.0, tool_kg=TOOL_KG, F_world=None):
    """Static joint torques (N m) holding pose q: UR10e/UR12e link masses (UR's dynamics table) placed as byu-vcl PR 318's
    stability() places them, the tool at the flange, the payload at the TCP, and an optional force (N) at the TCP.
    Each mass loads only the joints upstream of its link (cell.static_torques attaches every point to the flange, which
    loads the wrist joints with the arm's own links, so it is not used here)."""
    F = arm.fk(q)
    W = {k: arm.base @ F[k] for k in ("shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3", "tool0")}
    o = {k: W[k][:3, 3] for k in W}
    axes = [W[k][:3, 2] for k in ("shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3")]
    origins = [o[k] for k in ("shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3")]
    tcp = arm.tcp(q)[:3, 3]
    pts = [(UR_LINKS[0], o["shoulder"], 1), (UR_LINKS[1], (o["upper_arm"] + o["forearm"]) / 2, 2),
           (UR_LINKS[2], (o["forearm"] + o["wrist1"]) / 2, 3), (UR_LINKS[3], o["wrist1"], 4), (UR_LINKS[4], o["wrist2"], 5),
           (UR_LINKS[5], o["wrist3"], 6), (tool_kg, o["tool0"], 6), (payload_kg, tcp, 6)]
    g = np.array([0.0, 0.0, -9.81])
    tau = np.zeros(6)
    for m, p, n in pts:
        for j in range(n):
            tau[j] += float(np.cross(axes[j], (p - origins[j]) / 1000.0) @ (m * g))
    if F_world is not None:
        for j in range(6):
            tau[j] += float(np.cross(axes[j], (tcp - origins[j]) / 1000.0) @ np.asarray(F_world, float))
    return -tau


def tau_frac(arm, q, payload_kg=0.0, F_world=None):
    t = joint_torques(arm, q, payload_kg, TOOL_KG, F_world)
    return float(np.max(np.abs(t) / np.array(C.UR12E["tau_lim"])))


def push_limit(arm, q, direction, payload_kg=0.0, frac=1.0):
    """Largest force (N) at the TCP along `direction` before a joint reaches frac x its torque limit."""
    d = np.asarray(direction, float) / np.linalg.norm(direction)
    t0 = joint_torques(arm, q, payload_kg)
    t1 = joint_torques(arm, q, payload_kg, F_world=d) - t0
    lim = np.array(C.UR12E["tau_lim"]) * frac
    best = math.inf
    for i in range(6):
        if abs(t1[i]) < 1e-9:
            continue
        room = (lim[i] - t0[i]) / t1[i] if t1[i] > 0 else (-lim[i] - t0[i]) / t1[i]
        best = min(best, room)
    return float(best)


def ik_line(chk, arm, T_from, T_to, close, allow_from=frozenset(), allow_line=frozenset(), seed=None):
    """The first IK branch at T_from whose straight-line move to T_to is also clear: (q_from, qs, why)."""
    arm.close = close
    sols = arm.ik_all(T_from, seed)
    why = "no IK solution (out of reach)"
    for q in sols:
        if chk.collisions(q, close, allow_from):
            why = "every branch collides at the start"
            continue
        qs, info = cart(chk, arm, line(T_from, T_to), close, allow_line, q)
        if qs is not None:
            return q, qs, None
        why = info
    return None, None, why


def ik_free(chk, arm, T, close, allow=frozenset(), seed=None):
    """First collision-free IK branch for a TCP pose (nearest the seed first); (q, n_branches, why)."""
    arm.close = close
    sols = arm.ik_all(T, seed)
    why = None
    for q in sols:
        col = chk.collisions(q, close, allow)
        if not col:
            return q, len(sols), None
        why = why or [(a, b, d) for a, b, d in col[:3]]
    return None, len(sols), why or "no IK solution (out of reach)"


def cart(chk, arm, Ts, close, allow=frozenset(), seed=None, max_jump=math.radians(8.0)):
    """Straight-line Cartesian move: IK at every 5 mm sample, nearest branch, no joint jump > max_jump, all free."""
    q = np.asarray(seed if seed is not None else arm.q, float)
    qs = [q]
    arm.close = close
    for T in Ts[1:]:
        sols = arm.ik_all(T, q)
        if not sols:
            return None, dict(reason="out of reach", at=T[:3, 3].round(1).tolist())
        qn = sols[0]
        if np.abs(qn - q).max() > max_jump:
            return None, dict(reason="IK branch jump", at=T[:3, 3].round(1).tolist(),
                              jump_deg=float(np.degrees(np.abs(qn - q).max())))
        col = chk.collisions(qn, close, allow)
        if col:
            return None, dict(reason="collision", at=T[:3, 3].round(1).tolist(), hits=[(a, b, d) for a, b, d in col[:3]])
        qs.append(qn)
        q = qn
    return qs, dict(n=len(qs))


def clearance(chk, arm, q, close, exclude=()):
    """Smallest distance (mm) from the arm, gripper and held part to any world body not named in `exclude`."""
    arm.place(q, close)
    W = Group([b for n, b in chk.sc.world.bodies.items()
               if not any(e in n for e in tuple(exclude) + ("arm mounting plate",))])
    R = Group([b for b in arm.bodies() if not b.name.endswith("/base")])
    d, a, b = group_distance(R, W, margin=150.0)
    return float(d), (a.name if a else None), (b.name if b else None)


def touch_ok(s, part_name):
    """What a segment may touch on purpose (its allow list, by its note): excluded from the clearance."""
    n = s["note"]
    ex = [part_name]
    if any(k in n for k in ("deck", "lift", "onto", "down")):
        ex.append("parts deck")
    if "vise" in n:
        ex.append("vise body")
    if "jaws" in n or "chuck" in n:
        ex.append("chuck jaw")
    return tuple(ex)


def tightest(chk, arm, plan, exclude_by_seg, kinds=("joint", "linear")):
    """Walk every segment of a plan (densified) and return the smallest clearance and where."""
    best = (math.inf, None, None, None, None)
    for k, s in enumerate(plan.segments):
        if not s["qs"] or isinstance(s["qs"][0], tuple) or s["kind"] not in kinds:
            continue
        if s["held"] is not None:
            arm.held = s["held"]
            if arm.held[0].name not in arm.robot.bodies:
                arm.robot.add(arm.held[0])
        else:
            if arm.held is not None:
                arm.robot.remove(arm.held[0].name)
            arm.held = None
        ex = exclude_by_seg(s)
        qs = densify(s["qs"], math.radians(3.0)) if len(s["qs"]) > 1 else s["qs"]
        for q in qs[::2]:
            d, a, b = clearance(chk, arm, q, s["close"], ex)
            if d < best[0]:
                best = (d, a, b, k, np.asarray(q).tolist())
    return dict(clear_mm=round(best[0], 1), robot_body=best[1], world_body=best[2], segment=best[3], q=best[4])


def attach(arm, body, T_part):
    """Hold `body` (posed at T_part) in the gripper: offset = TCP^-1 * part."""
    off = inv(arm.tcp()) @ T_part
    arm.held = (body, off)
    arm.robot.add(body)
    return arm.held


def detach(arm):
    if arm.held is not None:
        arm.robot.remove(arm.held[0].name)
    arm.held = None


# ----------------------------------------------------------------------------------------------- parts
FRAME_B = dict(L=330.2, W=241.3, H=139.7, core=(274.0, 184.0))   # the chamber worker's blank: 13 x 9.5 x 5.5 in. plate,
                                                                   # its 274 x 184 core out as one slug first (dfm.json)


def frame_blank_B():
    """Chamber version B: the through-frame's blank with its core out (28 mm walls left for the finish cuts).
    Part frame: centre of the bottom face."""
    L, W, H = FRAME_B["L"], FRAME_B["W"], FRAME_B["H"]
    cx, cy = FRAME_B["core"]
    vf = S.frame_ring(-L / 2, L / 2, -W / 2, W / 2, 0, H, -cx / 2, cx / 2, -cy / 2, cy / 2)
    return vf, (L * W - cx * cy) * H * RHO["al6061"]


def roughed_block_A():
    """Chamber version A after the pocket is roughed (outside not yet faced): 13 x 9.5 x 6 in. block with a
    280 x 190 x 120 mm pocket."""
    vf = S.pocketed_block(-165.1, 165.1, -120.65, 120.65, 0, 152.4, 25.1, 32.4)
    vol = 330.2 * 241.3 * 152.4 - 280.0 * 190.0 * 120.0
    return vf, vol * RHO["al6061"]


def slug():
    """2-1/8 in. 6061 bar slug, 100 mm long (heater block, build plate and piston head are turned from it and parted
    off). Part frame: chuck end centre, axis along +x."""
    vf = S.cyl(27.0, (0, 0, 0), (100.0, 0, 0), n=32)
    return vf, math.pi * 27.0 ** 2 * 100.0 * RHO["al6061"]


# ----------------------------------------------------------------------------------------------- P1: VF-4 vise, one arm
def plan_vf4_single(shop, x_mir=None, door_w=None):
    st = shop["vf4"]
    vf_part, kg = frame_blank_B()
    P = dict(S.VF4, door_w=door_w or S.VF4["door_w"])
    items, meta = S.vf4_items(P, vise_open=241.3 + 20.0)
    world_items = [(f"vf4/{n}", S.xf(vf, st.M), c) for n, vf, c in items]
    xc, yc, tz = meta["vise_centre"]
    vise_x = xc
    if x_mir is None:
        x_mir = vise_x - S.ARM_DX
    Mm = S.dock_frame(st, x_mir)
    sc = S.ShopScene(world_items, mirs=[(Mm, S.ARM_DX)])
    base, yaw = S.arm_base_world(st, x_mir)
    arm = Arm("A", base=tuple(base), yaw_deg=yaw)
    chk = Checker(sc, arm)
    plan = Plan("P1 VF-4: chamber frame blank (version B) from the deck into the vise and out")
    part = Body("frame blank B", *vf_part, kind="held", color=S.COL["part"])
    # part on the deck: long axis along the MiR, centred on the deck
    pd = S.deck_point(st, x_mir, local=(110.0, 0.0))
    T_deck = Tm(st.R(), pd)
    # part in the vise: on the vise body, 10 mm in front of the fixed jaw
    jaw_y = meta["vise_jaw_back_y"]
    T_vise = st.M @ Tm(None, (vise_x, jaw_y - 10.0 - FRAME_B["W"] / 2, meta["vise_floor_z"]))
    wall = (FRAME_B["L"] - FRAME_B["core"][0]) / 2                          # 28.1 mm
    G = Tm(C.frame((0, 0, -1), (1, 0, 0)), (FRAME_B["L"] / 2 - wall / 2, 0.0, FRAME_B["H"] - 30.0))   # +x end wall
    c_grip = arm.close_for_gap(wall)
    c_open = arm.close_for_gap(wall + 30.0)
    # 0. home: carry pose over the deck
    part.place(T_deck)
    sc.world.add(part)
    q_home = home_pose(chk, arm, st, x_mir, c_open)
    if q_home is None:
        plan.add("ik", [], c_open, "carry pose over the deck", ok=False)
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    arm.q = q_home.copy()
    T_pick = T_deck @ G
    allow_pick = {("tool", part.name)}
    q_pre, qs_down, why = ik_line(chk, arm, lift(T_pick, 120), T_pick, c_open, allow_pick, allow_pick, q_home)
    if q_pre is None:
        plan.add("ik", [], c_open, "above the part on the deck", ok=False, info=dict(why=str(why)))
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    path, info = chk.plan(q_home, q_pre, c_open, allow_pick)
    plan.add("joint", path or [], c_open, "home -> above the part on the deck", ok=path is not None, info=info)
    if path is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    qs, info = qs_down, dict(n=len(qs_down))
    plan.add("linear", qs or [], c_open, "down 120 mm onto the end wall", ok=qs is not None, info=info,
             t=120 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    q_pick = qs[-1]
    plan.add("grip", [q_pick], c_grip, f"close on the {wall:.0f} mm wall", t=0.8)
    # pick up
    sc.world.remove(part.name)
    arm.place(q_pick, c_grip)
    held = attach(arm, part, T_deck)
    allow_deck = {("held", "mir0/parts deck")}
    qs, info = cart(chk, arm, line(T_pick, lift(T_pick, 150)), c_grip, allow_deck, q_pick)
    plan.add("linear", qs or [], c_grip, "lift 150 mm off the deck", ok=qs is not None, info=info, held=held, t=150 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    q_up = qs[-1]
    T_place = T_vise @ G
    allow_vise = {("held", "vf4/vise body")}
    q_above, qs_lower, why = ik_line(chk, arm, lift(T_place, 120), T_place, c_grip, frozenset(), allow_vise, q_up)
    if q_above is None:
        plan.add("ik", [], c_grip, "above the vise with the part", ok=False, info=dict(why=str(why)), held=held)
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    t0 = time.time()
    path, info = chk.plan(q_up, q_above, c_grip, frozenset(), iters=4000)
    info["plan_s"] = round(time.time() - t0, 1)
    plan.add("joint", path or [], c_grip, "carry through the door to 120 mm above the vise", ok=path is not None, info=info,
             held=held)
    if path is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    qs, info = qs_lower, dict(n=len(qs_lower))
    plan.add("linear", qs or [], c_grip, "lower 120 mm into the open vise", ok=qs is not None, info=info, held=held,
             t=120 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    q_place = qs[-1]
    plan.add("vise", [q_place], c_grip, "pneumatic vise closes (machine M-code); gripper opens", t=1.5)
    detach(arm)
    part.place(T_vise)
    sc.world.add(part)
    allow_rel = {("tool", part.name)}
    qs, info = cart(chk, arm, line(T_place, lift(T_place, 120)), c_open, allow_rel, q_place)
    plan.add("linear", qs or [], c_open, "retreat 120 mm up", ok=qs is not None, info=info, t=120 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    path, info = chk.plan(qs[-1], q_home, c_open, frozenset(), iters=4000)
    plan.add("joint", path or [], c_open, "out of the machine to home", ok=path is not None, info=info)
    ctx = dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg, part=part, T_vise=T_vise, T_deck=T_deck, held=held,
               q_place=q_place, q_pick=q_pick, meta=meta, station=st, x_mir=x_mir)
    return plan, ctx


def S_LIN():
    return LIN_SPEED


# ----------------------------------------------------------------------------------------------- P2: lathe chuck
def plan_lathe(shop, x_mir=None):
    st = shop["lathe"]
    vf_part, kg = slug()
    items, meta = S.lathe_items(jaw_r=27.0 + 6.0)
    world_items = [(f"lathe/{n}", S.xf(vf, st.M), c) for n, vf, c in items]
    _, yc, zc = meta["chuck_face"]
    if x_mir is None:
        x_mir = 150.0 - S.ARM_DX
    Mm = S.dock_frame(st, x_mir)
    sc = S.ShopScene(world_items, mirs=[(Mm, S.ARM_DX)])
    base, yaw = S.arm_base_world(st, x_mir)
    arm = Arm("A", base=tuple(base), yaw_deg=yaw)
    chk = Checker(sc, arm)
    plan = Plan("P2 lathe: 2-1/8 in. 6061 slug from the deck into the chuck")
    part = Body("bar slug 2-1/8 in. x 100", *vf_part, kind="held", color=S.COL["part"])
    pd = S.deck_point(st, x_mir, local=(110.0, 0.0))
    T_deck = Tm(st.R(), pd + np.array([0.0, 0.0, 27.0]))                     # lying in a V-cradle, axis along the MiR
    T_chuck = st.M @ Tm(None, (5.0, yc, zc))                                 # chuck end 5 mm off the chuck face
    G = Tm(C.frame((0, 0, -1), (0, 1, 0)), (75.0, 0.0, 0.0))     # from above, fingers across the bar, 25 mm from its outer end
    c_grip = arm.close_for_gap(54.0)
    c_open = arm.close_for_gap(80.0)
    part.place(T_deck)
    sc.world.add(part)
    q_home = home_pose(chk, arm, st, x_mir, c_open)
    if q_home is None:
        plan.add("ik", [], c_open, "carry pose over the deck", ok=False)
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    arm.q = q_home.copy()
    allow_pick = {("tool", part.name)}
    T_pick = T_deck @ G                                                 # from above: the slug lies on the deck
    q_pre, qs_down, why = ik_line(chk, arm, lift(T_pick, 100), T_pick, c_open, allow_pick, allow_pick, q_home)
    if q_pre is None:
        plan.add("ik", [], c_open, "100 mm above the slug on the deck", ok=False, info=dict(why=str(why)))
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    path, info = chk.plan(q_home, q_pre, c_open, allow_pick)
    plan.add("joint", path or [], c_open, "home -> 100 mm above the slug (deck)", ok=path is not None, info=info)
    if path is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    qs, info = qs_down, dict(n=len(qs_down))
    plan.add("linear", qs or [], c_open, "down 100 mm round the slug's top (deck)", ok=qs is not None, info=info,
             t=100 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    q_pick = qs[-1]
    plan.add("grip", [q_pick], c_grip, "close on Ø54", t=0.8)
    sc.world.remove(part.name)
    arm.place(q_pick, c_grip)
    held = attach(arm, part, T_deck)
    qs, info = cart(chk, arm, line(T_pick, lift(T_pick, 130)), c_grip, {("held", "mir0/parts deck")}, q_pick)
    plan.add("linear", qs or [], c_grip, "lift 130 mm off the deck", ok=qs is not None, info=info, held=held, t=130 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    q_up = qs[-1]
    T_tcp_chuck = T_chuck @ G
    into = st.R() @ np.array([1.0, 0, 0]) * 70.0
    T_pre = lift(T_tcp_chuck, dx=into[0], dy=into[1])                  # lined up on the axis, 70 mm short of the jaws
    outd = st.R() @ np.array([0.0, -1.0, 0]) * 450.0
    T_door = lift(T_pre, dx=outd[0], dy=outd[1])                        # the same, 450 mm out in front of the door
    # every IK branch at the door whose straight move in is clear, then the first that RRT-Connect reaches from the deck
    arm.close = c_grip
    path, info, qs = None, dict(reason="no IK branch at the door with a clear straight move in"), None
    t0 = time.time()
    for qd in arm.ik_all(T_door, q_up):
        if chk.collisions(qd, c_grip, frozenset()):
            continue
        qs_in, _ = cart(chk, arm, line(T_door, T_pre, step=5.0), c_grip, frozenset(), qd)
        if qs_in is None:
            continue
        path, info = chk.plan(q_up, qd, c_grip, frozenset(), iters=2500)
        if path is not None:
            qs = qs_in
            break
    info["plan_s"] = round(time.time() - t0, 1)
    plan.add("joint", path or [], c_grip, "carry the slug to the front of the door, level with the spindle axis",
             ok=path is not None, info=info, held=held)
    if path is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    plan.add("linear", qs, c_grip, "straight in 450 mm through the door onto the spindle axis", ok=True,
             info=dict(n=len(qs)), held=held, t=450 / 250.0)
    q_pre_in = qs[-1]
    allow_jaws = {("held", f"lathe/chuck jaw {k}") for k in (1, 2, 3)}
    qs, info = cart(chk, arm, line(T_pre, T_tcp_chuck), c_grip, allow_jaws, q_pre_in)
    plan.add("linear", qs or [], c_grip, "push 70 mm along the spindle axis into the open jaws", ok=qs is not None,
             info=info, held=held, t=70 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    q_in = qs[-1]
    plan.add("chuck", [q_in], c_grip, "chuck closes (foot pedal / M-code); gripper opens", t=1.5)
    detach(arm)
    part.place(T_chuck)
    sc.world.add(part)
    T_upc = lift(T_tcp_chuck, 100)
    qs, info = cart(chk, arm, line(T_tcp_chuck, T_upc), c_open, {("tool", part.name)}, q_in)
    plan.add("linear", qs or [], c_open, "up 100 mm off the slug", ok=qs is not None, info=info, t=100 / S_LIN())
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    qs, info = cart(chk, arm, line(T_upc, lift(T_door, 100)), c_open, frozenset(), qs[-1])
    plan.add("linear", qs or [], c_open, "straight back 450 mm out of the door", ok=qs is not None, info=info,
             t=450 / 250.0)
    if qs is None:
        return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg)
    path, info = chk.plan(qs[-1], q_home, c_open, frozenset(), iters=6000)
    plan.add("joint", path or [], c_open, "out of the lathe to home", ok=path is not None, info=info)
    return plan, dict(arm=arm, chk=chk, sc=sc, items=world_items, kg=kg, part=part, held=held, q_in=q_in, station=st,
                      T_deck=T_deck, T_chuck=T_chuck)


# ----------------------------------------------------------------------------------------------- P3: two arms
def two_arm_hold(shop, door_w=None, pull=420.0):
    """Version A's roughed chamber block (about 15 kg) held by both arms on its end walls in the VF-4 vise, then
    lifted 150 mm and drawn 450 mm toward the door on a straight line. Both MiRs docked side by side at the door."""
    st = shop["vf4"]
    vf_part, kg = roughed_block_A()
    P = dict(S.VF4, door_w=door_w or S.VF4["door_w"])
    items, meta = S.vf4_items(P, vise_open=241.3 + 20.0)
    world_items = [(f"vf4/{n}", S.xf(vf, st.M), c) for n, vf, c in items]
    xc, yc, tz = meta["vise_centre"]
    # MiR A (deck on its left, arm at +190) and MiR B (arm at -190, deck on its right), 100 mm apart
    xa = xc - 450.0 - 190.0 + 200.0
    xb = xa + 900.0
    Ma, Mb = S.dock_frame(st, xa), S.dock_frame(st, xb)
    base_a, yaw = S.arm_base_world(st, xa, arm_dx=+190.0)
    base_b, _ = S.arm_base_world(st, xb, arm_dx=-190.0)
    A = Arm("A", base=tuple(base_a), yaw_deg=yaw)
    B = Arm("B", base=tuple(base_b), yaw_deg=yaw)
    scA = S.ShopScene(world_items, mirs=[(Ma, +190.0), (Mb, -190.0)], others=[B])
    scB = S.ShopScene(world_items, mirs=[(Ma, +190.0), (Mb, -190.0)], others=[A])
    chkA, chkB = Checker(scA, A), Checker(scB, B)
    part = Body("roughed block A", *vf_part, kind="held", color=S.COL["part"])
    jaw_y = meta["vise_jaw_back_y"]
    T0 = st.M @ Tm(None, (xc, jaw_y - 10.0 - 120.65, meta["vise_floor_z"]))
    wall = 25.1
    GA = Tm(C.frame((0, 0, -1), (1, 0, 0)), (-165.1 + wall / 2, 0.0, 152.4 - 30.0))
    GB = Tm(C.frame((0, 0, -1), (-1, 0, 0)), (165.1 - wall / 2, 0.0, 152.4 - 30.0))
    c_grip = A.close_for_gap(wall)
    B.close = c_grip
    door_dir = st.R() @ np.array([0.0, -1.0, 0.0])
    poses = line(T0, lift(T0, 150), step=10.0)
    PULL = pull            # 1251 mm door: at 440 mm arm B's upper arm meets the right jamb (run of 2026-11-20 22:42 UTC)
    poses += line(lift(T0, 150), lift(T0, 150, dx=float(door_dir[0] * PULL), dy=float(door_dir[1] * PULL)), step=10.0)[1:]
    A.q = np.radians([90.0, -60.0, 100.0, -130.0, -90.0, 0.0])
    B.q = np.radians([90.0, -120.0, -100.0, -50.0, 90.0, 0.0])
    res = dict(kg=round(kg, 2), per_arm_kg=round(kg / 2, 2), steps=[], ok=True)
    allowA = {("held", b.name) for b in B.grip.values()}
    first_hits = []
    qa_prev = qb_prev = None
    best = (math.inf, None)
    worst_tau = [0.0, 0.0]
    for k, Tp in enumerate(poses):
        TA, TB = Tp @ GA, Tp @ GB
        A.close = B.close = c_grip
        if qa_prev is None:
            # search all branch pairs for the first pose
            solsA, solsB = A.ik_all(TA), B.ik_all(TB)
            pair = None
            for qa in solsA:
                for qb in solsB:
                    part.place(Tp)
                    A.place(qa, c_grip)
                    A.held = (part, inv(A.tcp()) @ Tp)
                    A.robot.add(part)
                    B.place(qb, c_grip)
                    ca = chkA.collisions(qa, c_grip, allowA | {("held", "vf4/vise body")})
                    B.place(qb, c_grip)
                    cb = [c for c in chkB.collisions(qb, c_grip, frozenset()) if "roughed block" not in c[1]]
                    A.place(qa, c_grip)
                    if not ca and not cb:
                        pair = (qa, qb)
                        break
                    first_hits.append([(x, y) for x, y, _ in (ca + cb)[:2]])
                    A.robot.remove(part.name)
                    A.held = None
                if pair:
                    break
            if pair is None:
                res.update(ok=False, fail="no collision-free IK pair holding the block in the vise",
                           branches=(len(solsA), len(solsB)), hits=first_hits[:6])
                return res, dict(A=A, B=B, items=world_items, part=part, mirs=[(Ma, 190.0), (Mb, -190.0)])
            qa_prev, qb_prev = pair
            q_first = pair
            continue
        sa = A.ik_all(TA, qa_prev)
        sb = B.ik_all(TB, qb_prev)
        if not sa or not sb:
            res.update(ok=False, fail=f"out of reach at step {k}")
            break
        qa, qb = sa[0], sb[0]
        if max(np.abs(qa - qa_prev).max(), np.abs(qb - qb_prev).max()) > math.radians(10):
            res.update(ok=False, fail=f"IK branch jump at step {k}")
            break
        part.place(Tp)
        B.place(qb, c_grip)
        ca = chkA.collisions(qa, c_grip, allowA | ({("held", "vf4/vise body")} if k < 3 else set()))
        cb = [c for c in chkB.collisions(qb, c_grip, frozenset()) if "roughed block" not in c[1]]
        A.place(qa, c_grip)
        if ca or cb:
            res.update(ok=False, fail=f"collision at step {k}: {(ca or cb)[:2]}")
            break
        qa_prev, qb_prev = qa, qb
        if k % 4 == 0:
            for i, (arm, q) in enumerate(((A, qa), (B, qb))):
                worst_tau[i] = max(worst_tau[i], tau_frac(arm, q, kg / 2))
            # clearance of either arm to the machine (the vise and the part excluded)
            B.place(qb, c_grip)
            dA = clearance(chkA, A, qa, c_grip, exclude=("vise", "roughed block", "B/gr/"))
            part.place(Tp)
            dB = clearance(chkB, B, qb, c_grip, exclude=("vise", "A/gr/"))
            A.place(qa, c_grip)
            if dB[0] < dA[0]:
                dA = dB
            if dA[0] < best[0]:
                best = (dA[0], dict(k=k, bodies=dA[1:], qa=qa.tolist(), qb=qb.tolist()))
        res["steps"].append(k)
    res["n_steps"] = len(poses)
    res["door_w"] = P["door_w"]
    res["pull_mm"] = pull
    ctx_q = dict(qa=qa_prev, qb=qb_prev)
    res["tau_frac_max"] = [round(x, 3) for x in worst_tau]
    res["tightest"] = dict(clear_mm=round(best[0], 1), **(best[1] or {}))
    return res, dict(A=A, B=B, items=world_items, part=part, mirs=[(Ma, 190.0), (Mb, -190.0)], q_first=q_first,
                     q_last=ctx_q, T0=T0, kg=kg)


# ----------------------------------------------------------------------------------------------- P6: two arms, a plate
def two_arm_plate(shop, door_w=None, pull=400.0):
    """The optics bridge's 1.25 in. stock plate (376 x 611 mm, 19.7 kg) held by both arms from above on two bolted-on
    lifting tabs (20 x 60 x 50 mm, one at each end: our addition, a robot handle), set on a 500 x 380 x 40 mm fixture
    plate (vacuum or zero-point) on the VF-4 table centred in the door, lifted 150 mm and drawn toward the door.
    (Pinching the plate's edges with the tool level fails: every IK pair puts arm A's upper arm into the panel under
    the door and the chip trough, run of 2026-11-20 23:05 UTC.)"""
    st = shop["vf4"]
    L, W, T = 611.0, 376.0, 31.75
    kg = L * W * T * RHO["al6061"]
    P = dict(S.VF4, door_w=door_w or S.VF4["door_w"], load_dx=0.0)
    items, meta = S.vf4_items(P, with_vise=False, with_hrt=False, fixture=(500.0, 380.0, 40.0))
    world_items = [(f"vf4/{n}", S.xf(vf, st.M), c) for n, vf, c in items]
    xt, yc, tz = meta["table_centre"]
    xa = xt - 260.0 - 190.0
    xb = xt + 260.0 + 190.0
    Ma, Mb = S.dock_frame(st, xa), S.dock_frame(st, xb)
    base_a, yaw = S.arm_base_world(st, xa, arm_dx=+190.0)
    base_b, _ = S.arm_base_world(st, xb, arm_dx=-190.0)
    A = Arm("A", base=tuple(base_a), yaw_deg=yaw)
    B = Arm("B", base=tuple(base_b), yaw_deg=yaw)
    scA = S.ShopScene(world_items, mirs=[(Ma, +190.0), (Mb, -190.0)], others=[B])
    scB = S.ShopScene(world_items, mirs=[(Ma, +190.0), (Mb, -190.0)], others=[A])
    chkA, chkB = Checker(scA, A), Checker(scB, B)
    tab_x = L / 2 - 40.0
    part = Body("bridge plate", *S.merge([S.box(-L / 2, L / 2, -W / 2, W / 2, 0.0, T),
                                          S.box(-tab_x - 10, -tab_x + 10, -30, 30, T, T + 50),
                                          S.box(tab_x - 10, tab_x + 10, -30, 30, T, T + 50)]), kind="held", color=S.COL["part"])
    T0 = st.M @ Tm(None, (xt, yc, tz + 40.0))
    GA = Tm(C.frame((0, 0, -1), (1, 0, 0)), (-tab_x, 0.0, T + 30.0))     # from above, fingers across the tab
    GB = Tm(C.frame((0, 0, -1), (-1, 0, 0)), (tab_x, 0.0, T + 30.0))
    c_grip = A.close_for_gap(20.0)
    door_dir = st.R() @ np.array([0.0, -1.0, 0.0])
    poses = line(T0, lift(T0, 150), step=10.0)
    poses += line(lift(T0, 150), lift(T0, 150, dx=float(door_dir[0] * pull), dy=float(door_dir[1] * pull)), step=10.0)[1:]
    res = dict(kg=round(kg, 2), per_arm_kg=round(kg / 2, 2), door_w=P["door_w"], pull_mm=pull, ok=True)
    allowA = {("held", b.name) for b in B.grip.values()} | {("held", "vf4/fixture plate")}
    qa_prev = qb_prev = None
    best = (math.inf, None)
    worst_tau = [0.0, 0.0]
    for k, Tp in enumerate(poses):
        TA, TB = Tp @ GA, Tp @ GB
        A.close = B.close = c_grip
        part.place(Tp)
        if qa_prev is None:
            pair, hits = None, []
            for qa in A.ik_all(TA, np.radians([90.0, -60.0, 100.0, -130.0, -90.0, 0.0])):
                for qb in B.ik_all(TB, np.radians([90.0, -120.0, -100.0, -50.0, 90.0, 0.0])):
                    A.place(qa, c_grip)
                    A.held = (part, inv(A.tcp()) @ Tp)
                    if part.name not in A.robot.bodies:
                        A.robot.add(part)
                    B.place(qb, c_grip)
                    ca = chkA.collisions(qa, c_grip, allowA)
                    B.place(qb, c_grip)
                    cb = [c for c in chkB.collisions(qb, c_grip, frozenset()) if part.name not in c[1]]
                    A.place(qa, c_grip)
                    if not ca and not cb:
                        pair = (qa, qb)
                        break
                    hits.append([(x, y) for x, y, _ in (ca + cb)[:2]])
                if pair:
                    break
            if pair is None:
                res.update(ok=False, fail="no collision-free IK pair holding the plate on the fixture", hits=hits[:6])
                return res, dict(A=A, B=B, items=world_items, part=part, mirs=[(Ma, 190.0), (Mb, -190.0)])
            qa_prev, qb_prev = pair
            q_first = pair
            continue
        sa, sb = A.ik_all(TA, qa_prev), B.ik_all(TB, qb_prev)
        if not sa or not sb:
            res.update(ok=False, fail=f"out of reach at step {k}")
            break
        qa, qb = sa[0], sb[0]
        if max(np.abs(qa - qa_prev).max(), np.abs(qb - qb_prev).max()) > math.radians(10):
            res.update(ok=False, fail=f"IK branch jump at step {k}")
            break
        B.place(qb, c_grip)
        ca = chkA.collisions(qa, c_grip, allowA)
        cb = [c for c in chkB.collisions(qb, c_grip, frozenset()) if part.name not in c[1]]
        A.place(qa, c_grip)
        if ca or cb:
            res.update(ok=False, fail=f"collision at step {k}: {[(x, y) for x, y, _ in (ca or cb)[:2]]}")
            break
        qa_prev, qb_prev = qa, qb
        if k % 3 == 0:
            for i, (arm, q) in enumerate(((A, qa), (B, qb))):
                worst_tau[i] = max(worst_tau[i], tau_frac(arm, q, kg / 2))
            dA = clearance(chkA, A, qa, c_grip, exclude=("fixture plate", "bridge plate", "B/gr/"))
            part.place(Tp)
            dB = clearance(chkB, B, qb, c_grip, exclude=("fixture plate", "A/gr/"))
            A.place(qa, c_grip)
            d = dA if dA[0] <= dB[0] else dB
            if d[0] < best[0]:
                best = (d[0], dict(k=k, bodies=d[1:], qa=qa.tolist(), qb=qb.tolist()))
    res["n_steps"] = len(poses)
    res["tau_frac_max"] = [round(x, 3) for x in worst_tau]
    res["tightest"] = dict(clear_mm=round(best[0], 1), **(best[1] or {}))
    if qa_prev is not None:
        res["stability_A"] = stability(A, q_first[0], Ma, kg / 2)
        res["stability_B"] = stability(B, q_first[1], Mb, kg / 2)
    return res, dict(A=A, B=B, items=world_items, part=part, mirs=[(Ma, 190.0), (Mb, -190.0)], q_first=q_first, kg=kg)


# ----------------------------------------------------------------------------------------------- P4: box seam
def box_seam(shop):
    st = shop["receiving"]
    items, meta = S.receiving_items(S.BOXES)
    world_items = [(f"recv/{n}", S.xf(vf, st.M), c) for n, vf, c in items]
    # the first box on the lift table
    name, L, W, H, kg = [b for b in S.BOXES if b[4] <= 11.0][0]
    x_mir = -480.0 + L / 2 - S.ARM_DX
    Mm = S.dock_frame(st, x_mir)
    sc = S.ShopScene(world_items, mirs=[(Mm, S.ARM_DX)])
    base, yaw = S.arm_base_world(st, x_mir)
    arm = Arm("A", base=tuple(base), yaw_deg=yaw)
    chk = Checker(sc, arm)
    cutter = Body("box cutter holder", *S.box(-10, 10, -8, 8, -60, 38), kind="held", color="#e63946")
    # the blade (55 mm below the TCP, 8 mm into the box) is meant to cut, so only its holder is collision-checked
    c_grip = arm.close_for_gap(20.0)
    arm.q = np.radians([0.0, -110.0, 120.0, -100.0, -90.0, 0.0])
    top = 760.0 + H
    y_mid = 120.0 + W / 2
    p0 = st.to_world((-480.0 + 15.0, y_mid, top))
    p1 = st.to_world((-480.0 + L - 15.0, y_mid, top))
    seam_dir = (p1 - p0) / np.linalg.norm(p1 - p0)
    # blade 8 mm into the box (tape + flap edge), tool z down, cutter length along the seam
    Tc0 = T_at(p0 + np.array([0, 0, 47.0]), z=(0, 0, -1), x=np.cross([0, 0, 1.0], seam_dir))
    Tc1 = T_at(p1 + np.array([0, 0, 47.0]), z=(0, 0, -1), x=np.cross([0, 0, 1.0], seam_dir))
    arm.close = c_grip
    q0, nb, why = ik_free(chk, arm, lift(Tc0, 60), c_grip, frozenset(), arm.q)
    res = dict(box=name, seam_mm=round(float(np.linalg.norm(p1 - p0)), 1), ok=False)
    if q0 is None:
        res.update(fail=f"no IK above the seam start: {why}")
        return res, dict(arm=arm, items=world_items)
    arm.place(q0, c_grip)
    held = attach(arm, cutter, arm.tcp() @ Tm(None, (0, 0, 0)))
    allow = {("held", f"recv/box: {name}")}
    qs1, info1 = cart(chk, arm, line(lift(Tc0, 60), Tc0), c_grip, allow, q0)
    if qs1 is None:
        res.update(fail=f"plunge: {info1}")
        return res, dict(arm=arm, items=world_items)
    qs2, info2 = cart(chk, arm, line(Tc0, Tc1, step=5.0), c_grip, allow, qs1[-1])
    res.update(ok=qs2 is not None, info=info2 if qs2 is None else dict(n=len(qs2)), t_s=round(res["seam_mm"] / 100.0 + 2.0, 1))
    if qs2 is not None:
        res["tau_frac_max"] = round(max(tau_frac(arm, q, 0.2) for q in qs2[::10]), 3)
        # force the cutter can push along the seam at the midpoint, at half the joint torque limits
        res["push_along_seam_N_half_torque"] = round(push_limit(arm, qs2[len(qs2) // 2], seam_dir, 0.2, frac=0.5), 0)
    return res, dict(arm=arm, items=world_items, qs=(qs1 or []) + (qs2 or []), held=held, mirs=[(Mm, S.ARM_DX)])


# ----------------------------------------------------------------------------------------------- P5: reach checks
def reach_checks(shop):
    """IK + collision at the working points of the other stations, with the 2F-85 pointing down (or as noted)."""
    out = []

    def one(key, label, local_pts, x_mir, z_tool=(0, 0, -1), x_tool=(1, 0, 0), payload=1.0, allow_prefix=None, gap=S.DOCK_GAP):
        st = shop[key]
        world_items = st.world_items()
        Mm = S.dock_frame(st, x_mir, gap)
        sc = S.ShopScene(world_items, mirs=[(Mm, S.ARM_DX)])
        base, yaw = S.arm_base_world(st, x_mir, gap)
        arm = Arm("A", base=tuple(base), yaw_deg=yaw)
        chk = Checker(sc, arm)
        arm.q = np.radians([0.0, -110.0, 120.0, -100.0, -90.0, 0.0])
        c = arm.close_for_gap(40.0)
        for lp in local_pts:
            pw = st.to_world(lp)
            zt = st.R() @ np.asarray(z_tool, float)
            xt = st.R() @ np.asarray(x_tool, float)
            allow = frozenset((("tool", n) for n in sc.world.bodies if allow_prefix and allow_prefix in n))
            q, nb, why = ik_free(chk, arm, T_at(pw, zt, xt), c, allow, arm.q)
            row = dict(station=st.name, what=label, point_local=[round(v) for v in lp], dock_gap_mm=gap,
                       reach_mm=round(float(np.linalg.norm(pw - base)), 0), branches=nb, ok=q is not None)
            if q is None:
                row["why"] = str(why)[:200]
            else:
                row["tau_frac"] = round(tau_frac(arm, q, payload), 3)
                d = clearance(chk, arm, q, c, exclude=(allow_prefix,) if allow_prefix else ())
                row["clear_mm"] = round(d[0], 1)
                row["nearest"] = d[2]
                arm.q = q
            out.append(row)

    one("saw", "bar on the saw bed, at the blade line", [(0.0, 400.0, 790.0), (-600.0, 450.0, 790.0)], 150.0,
        allow_prefix="saw bed")
    one("wash", "basket handle in the ultrasonic tank", [(-510.0, 335.0, 1095.0)], -320.0, x_tool=(1, 0, 0),
        allow_prefix="basket handle")
    one("wash", "part held against the deburr brush (tool level, into the station)", [(30.0, 215.0, 1050.0)], 520.0,
        z_tool=(0, 1, 0), x_tool=(0, 0, 1))
    one("measure", "part on the granite plate", [(0.0, 300.0, 902.0 + 60.0), (-150.0, 450.0, 902.0 + 60.0)], 190.0)
    one("measure", "height gauge scriber (as a person would work it)", [(170.0, 345.0, 1060.0)], 190.0, z_tool=(0, 1, 0),
        x_tool=(0, 0, 1), allow_prefix="scriber")
    one("kit", "handle tab of the tote on each rack shelf", [(300.0, 20.0, z + 100.0) for z in (600.0, 1050.0, 1500.0)],
        40.0, z_tool=(0, 1, 0), x_tool=(1, 0, 0), payload=5.0, allow_prefix="tote handle")
    one("kit", "handle tab, MiR parked 450 mm off the rack", [(300.0, 20.0, z + 100.0) for z in (600.0, 1050.0, 1500.0)],
        40.0, z_tool=(0, 1, 0), x_tool=(1, 0, 0), payload=5.0, allow_prefix="tote handle", gap=450.0)
    one("bench", "assembly point on the bench, 500 mm in", [(-300.0, 500.0, 960.0), (300.0, 300.0, 960.0)], -100.0)
    one("stock", "bar on the cantilever arms (bottom, middle, top)", [(0.0, 200.0, z + 110.0) for z in (450.0, 950.0, 1450.0)],
        540.0, z_tool=(0, 1, 0), x_tool=(0, 0, 1), payload=5.0, allow_prefix="bar stock")
    return out


# ----------------------------------------------------------------------------------------------- MiR stability
# byu-vcl PR 318 (alloy_atomize.stability, commit 11d4410): masses, the 131 kg ballast plate under the cabinet, the
# support rectangle at the corner casters (estimated there: MiR doesn't publish wheel positions), mu = 0.6
MASS = dict(mir250=97.0, ur12e=33.3, control_box=12.0, cabinet=25.0, gripper=TOOL_KG)
UR_LINKS = (7.369, 13.051, 3.989, 2.1, 1.98, 0.615)
BALLAST_KG, BALLAST_T = 7.85e-6 * 760.0 * 550.0 * 40.0, 40.0
WHEELS = (325.0, 225.0)


def stability(arm, q, Mmir, payload_kg=0.0, F_ext=(0.0, 0.0, 0.0), accel=0.0, ballast=True, extra=()):
    """Tip margin of one MiR250 + cabinet + UR12e at joints q with payload_kg at the TCP: the worst edge's restoring
    moment (N m, > 0 = stays down), the extra kg at the TCP that would tip it, and the CoG. accel (m/s^2) adds the
    MiR's own acceleration as a horizontal inertial load toward the worst edge."""
    inv0 = inv(Mmir)
    F = arm.fk(q)
    pos = {k: (inv0 @ arm.base @ F[k])[:3, 3] for k in ("base", "shoulder", "upper_arm", "forearm", "wrist1", "wrist2",
                                                        "wrist3", "tool0")}
    tcp = (inv0 @ arm.tcp(q))[:3, 3]
    H = S.MIR["H"]
    items = [(MASS["mir250"], (0.0, 0.0, 120.0)), (MASS["control_box"], (0.0, 0.0, H + 150.0)),
             (MASS["cabinet"], (0.0, 0.0, H + S.MIR["cab_h"] / 2)),
             (MASS["ur12e"] - sum(UR_LINKS), pos["base"]), (UR_LINKS[0], pos["shoulder"]),
             (UR_LINKS[1], (pos["upper_arm"] + pos["forearm"]) / 2), (UR_LINKS[2], (pos["forearm"] + pos["wrist1"]) / 2),
             (UR_LINKS[3], pos["wrist1"]), (UR_LINKS[4], pos["wrist2"]), (UR_LINKS[5], pos["wrist3"]),
             (MASS["gripper"], pos["tool0"]), (payload_kg, tcp)] + [(k, np.asarray(p, float)) for k, p in extra]
    if ballast:
        items.append((BALLAST_KG, (0.0, 0.0, H + BALLAST_T / 2)))
    m = sum(k for k, _ in items)
    Gc = sum(k * np.asarray(p, float) for k, p in items) / m
    ax, ay = WHEELS
    worst = None
    for name, a, u in (("+x", (ax, 0), (1, 0)), ("-x", (-ax, 0), (-1, 0)), ("+y", (0, ay), (0, 1)), ("-y", (0, -ay), (0, -1))):
        u = np.array([u[0], u[1], 0.0])
        A_ = np.array([a[0], a[1], 0.0])
        keep = m * 9.81 * float(-(Gc - A_) @ u) / 1000.0                     # N m
        keep -= m * accel * Gc[2] / 1000.0                                     # inertial load toward this edge
        lever_tcp = float((tcp - A_) @ u)                                      # mm beyond the edge (> 0 = outside)
        extra = keep / (9.81 * lever_tcp / 1000.0) if lever_tcp > 1.0 else None
        row = dict(edge=name, restoring_Nm=round(keep, 1), tcp_beyond_edge_mm=round(lever_tcp, 0),
                   extra_kg_to_tip=round(extra, 1) if extra is not None else None)
        if worst is None or keep < worst["restoring_Nm"]:
            worst = row
    return dict(mass_kg=round(m, 1), cog_mm=[round(float(x)) for x in Gc], tcp_mm=[round(float(x)) for x in tcp],
                payload_kg=round(payload_kg, 2), accel_ms2=accel, ballast=ballast, worst=worst)


def stability_cases(ctxs):
    """PR 318's tip check at the poses this study uses, with and without the 131 kg plate, and driving at 0.3 m/s^2."""
    out = {}
    if "P1" in ctxs and "q_place" in ctxs["P1"][1]:
        plan, ctx = ctxs["P1"]
        arm, st, kg = ctx["arm"], ctx["station"], ctx["kg"]
        Mm = S.dock_frame(st, ctx["x_mir"])
        for bal in (True, False):
            out[f"P1 frame blank in the vise ({kg:.1f} kg), ballast={bal}"] = stability(arm, ctx["q_place"], Mm, kg, ballast=bal)
        # full horizontal reach toward the machine with the arm's whole net payload
        base_l = (inv(Mm) @ np.r_[arm.base[:3, 3], 1.0])[:3]
        for reach in (900.0, 1100.0):
            p = (Mm @ np.r_[base_l[0], base_l[1] + reach, base_l[2] + 150.0, 1.0])[:3]
            arm.close = 0.0
            sols = arm.ik_all(T_at(p, (0, 0, -1), st.R() @ np.array([1.0, 0, 0])), ctx["q_place"])
            if sols:
                for bal in (True, False):
                    out[f"one arm, {ARM_KG - TOOL_KG:.1f} kg at {reach:.0f} mm out toward the machine, ballast={bal}"] = \
                        stability(arm, sols[0], Mm, ARM_KG - TOOL_KG, ballast=bal)
        # driving with the blank on the deck, arm in its carry pose (PR 318: 0.3 m/s^2)
        q_home = plan.segments[0]["qs"][0] if plan.segments and plan.segments[0]["qs"] else ctx["q_place"]
        deck_l = (inv(Mm) @ np.r_[ctx["T_deck"][:3, 3] + np.array([0, 0, 63.5]), 1.0])[:3]
        for a in (0.3, 1.0):
            out[f"driving at {a} m/s^2 with the blank on the deck"] = stability(arm, q_home, Mm, 0.0, accel=a,
                                                                                 extra=[(kg, deck_l)])
    if "P3" in ctxs:
        r, ctx = ctxs["P3"]
        if ctx.get("q_first"):
            (Ma, dxa), (Mb, dxb) = ctx["mirs"]
            qa, qb = ctx["q_first"]
            out[f"P3 arm A, half the block ({r['per_arm_kg']} kg), in the vise"] = stability(ctx["A"], qa, Ma, r["per_arm_kg"])
            out[f"P3 arm B, half the block ({r['per_arm_kg']} kg), in the vise"] = stability(ctx["B"], qb, Mb, r["per_arm_kg"])
            ql = ctx.get("q_last") or {}
            if ql.get("qa") is not None:
                out["P3 arm A at the end of the draw"] = stability(ctx["A"], ql["qa"], Ma, r["per_arm_kg"])
                out["P3 arm B at the end of the draw"] = stability(ctx["B"], ql["qb"], Mb, r["per_arm_kg"])
    return out


# ----------------------------------------------------------------------------------------------- payload table
def payload_table():
    """Every machined part's stock (dfm.json) and the shipped boxes against the gripper, one arm and two arms."""
    src = HERE.parent / "out" / "machining" / "dfm.json"
    dfm = json.loads(src.read_text())["parts"]
    dens = dict(al6061=2.70, mic6=2.66, ss316l=8.0, macor=2.52, steel=7.75)
    net = ARM_KG - TOOL_KG
    rows = []
    for p in dfm:
        sc = p["stock_cm3"] or 0.0
        kg_s = dens.get(p["mat"], 7.8) * sc / 1000.0
        kg_p = dens.get(p["mat"], 7.8) * p["volume_cm3"] / 1000.0
        if not sc:          # tube or weldment: use the part (+30 %) as the stock estimate
            kg_s = kg_p * 1.3
        if p["slug"].startswith("process_chamber_body") and "through_frame" in p["slug"]:
            # version B as dfm.json lists it: the stock is the blank with its core already out
            full = FRAME_B["L"] * FRAME_B["W"] * FRAME_B["H"] * RHO["al6061"]
            rows.append(dict(part="Chamber frame (version B): 13 x 9.5 x 5.5 in. plate as delivered", mat=p["mat"],
                             stock="13 x 9.5 x 5.5 in. plate", n=1, stock_kg=round(full, 2), part_kg=round(kg_p, 2),
                             setups=None, machine=p["machine"], time_min=None))
            rows.append(dict(part="Chamber frame (version B): its 274 x 184 mm core, cut out as one slug", mat=p["mat"],
                             stock="", n=1, stock_kg=round(full - kg_s, 2), part_kg=None, setups=None, machine="",
                             time_min=None))
        n_set = len(p["setups"]) if p.get("setups") else max(1, round(p["time_min"]["setup"] / 20.0))
        rows.append(dict(part=p["name"], mat=p["mat"], stock=p["stock"], n=p["n_pieces"], stock_kg=round(kg_s, 2),
                         part_kg=round(kg_p, 2), setups=n_set, machine=p["machine"], time_min=p.get("time_total_min")))
    # version A (the one-block chamber of the first machining review, no longer in dfm.json once B replaced it)
    vb = [("Chamber body (version A): 13 x 9.5 x 6 in. block as delivered", 330.2 * 241.3 * 152.4 * RHO["al6061"]),
          ("Chamber body (version A) after the pocket is roughed", (330.2 * 241.3 * 152.4 - 280 * 190 * 120) * RHO["al6061"]),
          ("Chamber body (version A), finished (first machining review)", 7.36)]
    for name, kg in vb:
        rows.append(dict(part=name, mat="al6061", stock="", n=1, stock_kg=round(kg, 2), part_kg=None, setups=None,
                         machine="3-axis VMC", time_min=None, version_a=True))
    import re
    for r in rows:
        m = re.match(r"\u00d8([0-9.]+) in\. bar", r["stock"] or "")
        r["bar_od_mm"] = round(float(m.group(1)) * 25.4, 1) if m else None
        r["od_grip_2F85"] = None if not m else ("pass" if float(m.group(1)) * 25.4 <= 82.0 else
                                                "fail: OD over the 85 mm stroke (OnRobot 3FG15 grips 4-152 mm)")
        k = r["stock_kg"]
        r["gripper_2F85"] = "pass" if k <= GRIP_KG else "fail"
        r["one_arm"] = "pass" if k <= net else "fail"
        r["two_arms"] = "pass" if k <= 2 * net else "fail"
        r["verdict"] = ("one arm, 2F-85" if k <= GRIP_KG else "one arm, heavier gripper" if k <= net
                        else "two arms, rigid grasp" if k <= 2 * net else "person + hoist")
    boxes = []
    for name, L, W, H, kg in S.BOXES:
        boxes.append(dict(box=name, size_mm=[L, W, H], kg=kg,
                          verdict=("one arm, 2F-85" if kg <= GRIP_KG else "one arm, heavier gripper or slide" if kg <= net
                                   else "two arms" if kg <= 2 * net else "person + pallet jack or hoist")))
    return dict(net_per_arm_kg=round(net, 2), gripper_kg=GRIP_KG, parts=rows, boxes=boxes,
                dfm_json_mtime_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(src.stat().st_mtime)))


# ----------------------------------------------------------------------------------------------- main
# ----------------------------------------------------------------------------------------------- routes
FLOW = [("receiving", "table"), ("stock", "centre"), ("saw", "centre"), ("vf4", "centre"), ("lathe", "centre"),
        ("vf4", "centre"), ("wash", "centre"), ("measure", "centre"), ("kit", "centre"), ("bench", "left")]


def route_table(shop):
    """MiR legs of one part's flow through the shop (receiving -> rack -> saw -> mill -> lathe -> mill -> wash ->
    measure -> kitting -> bench), with the drive times of shop_cell.drive_time()."""
    legs = []
    for a, b in zip(FLOW[:-1], FLOW[1:]):
        poly = S.route(shop, a, b)
        t, L = S.drive_time(poly)
        legs.append(dict(frm=f"{shop[a[0]].name} ({a[1]})", to=f"{shop[b[0]].name} ({b[1]})", m=round(L, 1), s=round(t, 1),
                         poly=[[round(float(v)) for v in p] for p in poly]))
    tot_t = sum(l["s"] for l in legs)
    tot_m = sum(l["m"] for l in legs)
    return dict(drive=S.MIR_DRIVE, aisle=S.AISLE, legs=legs, total_m=round(tot_m, 1), total_s=round(tot_t, 1),
                docking_s=30.0, n_docks=len(legs),
                note="lanes at y = 5000 and 6000 mm in a 3 m aisle; MiR250: two robots pass in 3000 mm (default fields)")


def fine_audit(chk, arm, plan, step_deg=0.2):
    """Re-check every joint and linear segment at 0.2 deg steps (the planner checks at 0.5 deg): colliding samples."""
    bad = []
    for k, sg in enumerate(plan.segments):
        if not sg["qs"] or isinstance(sg["qs"][0], tuple) or len(sg["qs"]) < 2:
            continue
        if sg["held"] is not None:
            arm.held = sg["held"]
            if arm.held[0].name not in arm.robot.bodies:
                arm.robot.add(arm.held[0])
        else:
            if arm.held is not None:
                arm.robot.remove(arm.held[0].name)
            arm.held = None
        n = 0
        for q in densify(sg["qs"], math.radians(step_deg)):
            col = [c for c in chk.collisions(q, sg["close"], allow_for(sg)) if c[0] != c[1]]
            if col:
                n += 1
                if n == 1:
                    bad.append(dict(segment=k, note=sg["note"], first=[(a, b, d) for a, b, d in col[:2]]))
        if n:
            bad[-1]["samples"] = n
    return bad


def allow_for(sg):
    """The contacts a segment is allowed (as its plan used them), from its note."""
    n = sg["note"]
    out = set()
    if "deck" in n or "lift" in n:
        out |= {("held", "mir0/parts deck"), ("tool", "mir0/parts deck")}
    if "vise" in n:
        out |= {("held", "vf4/vise body")}
    if "jaws" in n:
        out |= {("held", f"lathe/chuck jaw {k}") for k in (1, 2, 3)}
    for nm in ("frame blank B", "bar slug 2-1/8 in. x 100"):
        out |= {("tool", nm)}
    return frozenset(out)


def summarize(plan):
    return dict(name=plan.name, ok=plan.ok, fail=plan.fail, time_s=round(plan.time_s(), 1),
                segments=[dict(kind=s["kind"], note=s["note"], ok=s["ok"], t_s=round(s["t"], 1),
                               info={k: (v if isinstance(v, (int, float, str, bool, type(None))) else str(v)[:300])
                                     for k, v in s["info"].items()}) for s in plan.segments])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--refresh-payload", action="store_true",
                    help="only recompute the payload table from the current dfm.json into the existing shop_checks.json")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.refresh_payload:
        path = OUT / "shop_checks.json"
        res = json.loads(path.read_text())
        res["payload"] = payload_table()
        res["payload_refreshed_utc"] = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
        path.write_text(json.dumps(res, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
        print("payload refreshed:", len(res["payload"]["parts"]), "rows")
        return
    shop = S.build_shop()
    res = dict(run_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()))
    t0 = time.time()
    res["payload"] = payload_table()
    only = a.only.split(",") if a.only else ["P1", "P2", "P3", "P4", "P5"]
    ctxs = {}
    if "P1" in only:
        plan, ctx = plan_vf4_single(shop)
        r = summarize(plan)
        if plan.ok:
            r["tightest"] = tightest(ctx["chk"], ctx["arm"], plan, lambda s: touch_ok(s, "frame blank"))
            r["tightest_transit"] = tightest(ctx["chk"], ctx["arm"], plan, lambda s: touch_ok(s, "frame blank"),
                                             kinds=("joint",))
        r["part_kg"] = round(ctx["kg"], 2)
        if plan.ok:
            r["fine_audit_0p2deg"] = fine_audit(ctx["chk"], ctx["arm"], plan)
        res["P1_vf4_single_arm"] = r
        ctxs["P1"] = (plan, ctx)
        print("P1", r["ok"], r["fail"], r.get("tightest_transit"), r.get("fine_audit_0p2deg"), round(time.time() - t0), "s", flush=True)
        tq = {}
        if "q_place" in ctx:
            for kg in (2.0, 5.0, 7.5, 10.0, 11.2, 12.5, 15.0, 20.0, 25.0, 33.0):
                tq[str(kg)] = round(tau_frac(ctx["arm"], ctx["q_place"], kg), 3)
        res["torque_frac_at_vise_by_payload_kg"] = tq
    if "P2" in only:
        plan, ctx = plan_lathe(shop)
        r = summarize(plan)
        if plan.ok:
            r["tightest"] = tightest(ctx["chk"], ctx["arm"], plan, lambda s: touch_ok(s, "bar slug"))
            r["tightest_transit"] = tightest(ctx["chk"], ctx["arm"], plan, lambda s: touch_ok(s, "bar slug"),
                                             kinds=("joint",))
        r["part_kg"] = round(ctx["kg"], 2)
        if plan.ok:
            r["fine_audit_0p2deg"] = fine_audit(ctx["chk"], ctx["arm"], plan)
        res["P2_lathe"] = r
        ctxs["P2"] = (plan, ctx)
        print("P2", r["ok"], r["fail"], r.get("tightest_transit"), r.get("fine_audit_0p2deg"), round(time.time() - t0), "s", flush=True)
    if "P1" in only:
        plan_b, ctx_b = plan_vf4_single(shop, door_w=1251.0)
        rb = summarize(plan_b)
        if plan_b.ok:
            rb["tightest_transit"] = tightest(ctx_b["chk"], ctx_b["arm"], plan_b, lambda s: touch_ok(s, "frame blank"),
                                              kinds=("joint",))
            rb["fine_audit_0p2deg"] = fine_audit(ctx_b["chk"], ctx_b["arm"], plan_b)
        res["P1_vf4_single_arm_door_1251"] = rb
        ctxs["P1b"] = (plan_b, ctx_b)
        print("P1 (1251 mm door)", rb["ok"], rb["fail"], rb.get("tightest_transit"), rb.get("fine_audit_0p2deg"), flush=True)
    if "P3" in only:
        r, ctx = two_arm_hold(shop, pull=450.0)
        res["P3_two_arms"] = r
        ctxs["P3"] = (r, ctx)
        r2, _ = two_arm_hold(shop, door_w=1251.0, pull=420.0)
        res["P3_two_arms_door_1251"] = r2
        print("P3 (1251 mm door)", r2["ok"], r2.get("fail"), r2.get("tightest"), flush=True)
        print("P3", r["ok"], r.get("fail"), r.get("tightest"), r.get("tau_frac_max"), round(time.time() - t0), "s", flush=True)
    if "P6" in only or not a.only:
        r, ctx = two_arm_plate(shop)
        res["P6_two_arms_plate"] = r
        ctxs["P6"] = (r, ctx)
        print("P6", r["ok"], r.get("fail"), r.get("tightest"), r.get("tau_frac_max"), round(time.time() - t0), "s", flush=True)
        r2, _ = two_arm_plate(shop, door_w=1251.0)
        res["P6_two_arms_plate_door_1251"] = r2
        print("P6 (1251 mm door)", r2["ok"], r2.get("fail"), r2.get("tightest", {}).get("clear_mm"), flush=True)
    if "P4" in only:
        r, ctx = box_seam(shop)
        res["P4_box_seam"] = r
        ctxs["P4"] = (r, ctx)
        print("P4", r, round(time.time() - t0), "s", flush=True)
    if "P5" in only:
        res["P5_reach"] = reach_checks(shop)
        for row in res["P5_reach"]:
            print("P5", row["station"], row["what"], row["ok"], row.get("clear_mm"), row.get("nearest"), row.get("tau_frac"),
                  row.get("why", "")[:80], flush=True)
    res["routes"] = route_table(shop)
    print("ROUTES", res["routes"]["total_m"], "m", res["routes"]["total_s"], "s", flush=True)
    res["stability"] = stability_cases(ctxs)
    for k, v in res["stability"].items():
        print("STAB", k, v["mass_kg"], v["worst"], flush=True)
    res["run_s"] = round(time.time() - t0, 1)
    path = OUT / ("shop_checks.json" if not a.only else f"shop_checks_{a.only.replace(',', '_')}.json")
    path.write_text(json.dumps(res, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    print("wrote", path, res["run_s"], "s")
    if not a.no_render:
        import shop_figs
        shop_figs.render_all(shop, ctxs, res)


if __name__ == "__main__":
    main()
