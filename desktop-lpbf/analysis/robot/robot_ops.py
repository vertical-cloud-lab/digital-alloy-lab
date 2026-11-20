"""Robot tending in MuJoCo: a UR10e with a Robotiq 2F-85 on a MiR250 does every automated operation of the
low-profile desktop LPBF (cad/lpbf_low.py) on its VLM tray.

What it does
  * Builds the machine from the CAD (any copy: --cad), splits every part near the robot into convex pieces
    (convex hull when the part is nearly convex, CoACD otherwise; cached under --cache) and loads it into MuJoCo
    with the UR10e and the 2F-85 from google-deepmind/mujoco_menagerie (pinned commit, downloaded to --menagerie).
    Every part that moves in an operation (doors, drawer, reservoir, plate, blade holder, jar, liner, module) is a
    free body whose pose the script sets.
  * For each operation it walks a list of Cartesian waypoints (approach, grasp, act, retreat) in small steps:
    damped-least-squares IK on the six arm joints (warm-started, several seeds at the first pose), joint limits,
    reach margin, and the clearance between robot + gripper + held part and the machine (MuJoCo contacts with a
    40 mm margin, so the closest distance is reported, not only penetrations).
  * Joint torques: inverse dynamics of the arm along the timed path, plus the held part's weight and the push or
    pull force the step needs, against the UR10e's joint torque limits (330/330/150/56/56/56 N m in the menagerie
    model). For each force step it also reports the largest force the arm could apply in that direction.
  * Near-misses: the closest robot/gripper/held-part geom to machine-part pair of each operation is re-measured
    with FCL against a fine (0.05 mm) tessellation of the exact B-rep part.

Re-run (CoACD of every part ~45 min the first time, mostly threaded fasteners; ROBOT_HULL_ONLY=1 hulls uncached parts;
~16 min for all operations once cached):
  cp -r desktop-lpbf/cad /tmp/robot-work/cad    # or point --cad at the live model
  OMP_NUM_THREADS=1 MUJOCO_GL=egl /tmp/capmem 4 /tmp/venv/bin/python desktop-lpbf/analysis/robot/robot_ops.py --cad /tmp/robot-work/cad
  add --render for the GIFs and PNGs (EGL offscreen), --ops plate_exchange,drawer to run a subset.
Menagerie files (not committed): fetch_menagerie() downloads them to --menagerie at MENAGERIE_SHA.
Writes analysis/out/robot/robot_ops.json, robot_ops.md, and with --render the images.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import sys
import time
import urllib.request

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "robot"
MENAGERIE_SHA = "370c43965323c0944b433b202aac5058b5f907a9"   # google-deepmind/mujoco_menagerie main, 2026-11-10
MEN_FILES = ["universal_robots_ur10e/LICENSE", "universal_robots_ur10e/ur10e.xml"] + \
    [f"universal_robots_ur10e/assets/{n}.obj" for n in ("base_0", "base_1", "forearm_0", "forearm_1", "forearm_2", "forearm_3",
                                                         "shoulder_0", "shoulder_1", "shoulder_2", "upperarm_0", "upperarm_1",
                                                         "upperarm_2", "upperarm_3", "wrist1_0", "wrist1_1", "wrist1_2",
                                                         "wrist2_0", "wrist2_1", "wrist2_2", "wrist3")] + \
    ["robotiq_2f85/LICENSE", "robotiq_2f85/2f85.xml"] + \
    [f"robotiq_2f85/assets/{n}.stl" for n in ("base", "base_mount", "coupler", "driver", "follower", "pad", "silicone_pad", "spring_link")]

# ---------------------------------------------------------------------------------------------------------------
# Robot, gripper, cell assumptions (mm unless noted)
# ---------------------------------------------------------------------------------------------------------------
UR10E = dict(payload_kg=12.5, reach_mm=1300.0, tau_lim=(330.0, 330.0, 150.0, 56.0, 56.0, 56.0), arm_mm=612.7 + 571.6,
             ft_range_N=100.0)
GRIP = dict(stroke_mm=85.0, force_N=(20.0, 235.0), mass_kg=0.925)
TRAY_FRONT_Y = -432.0            # tray front edge (machine frame); the tray is 864 mm deep, centred on y = 0
LINTEL_Z = 695.0                 # Modula bay S product height above the tray (lowest of the three openings)
FINGER = dict(drop=45.0, blade_len=120.0, blade_t=10.0, crank=10.0, crank_len=40.0, thick=8.0)   # custom fingertip


def fetch_menagerie(dst: pathlib.Path):
    for f in MEN_FILES:
        p = dst / f
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/{MENAGERIE_SHA}/{f}"
        urllib.request.urlretrieve(url, p)


# ---------------------------------------------------------------------------------------------------------------
# Small rigid-transform helpers (metres inside MuJoCo, mm in the op definitions)
# ---------------------------------------------------------------------------------------------------------------
def rot_x(deg):
    t = math.radians(deg)
    return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])


def rot_y(deg):
    t = math.radians(deg)
    return np.array([[math.cos(t), 0, math.sin(t)], [0, 1, 0], [-math.sin(t), 0, math.cos(t)]])


def rot_z(deg):
    t = math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])


def grip_R(a, c):
    """Gripper base rotation: z = approach a, y = closing direction c, x = y cross z (the pads' 22 mm width)."""
    a = np.asarray(a, float) / np.linalg.norm(a)
    c = np.asarray(c, float)
    c = c - a * (c @ a)
    c /= np.linalg.norm(c)
    return np.column_stack([np.cross(c, a), c, a])


def T(R=None, p=(0, 0, 0)):
    M = np.eye(4)
    if R is not None:
        M[:3, :3] = R
    M[:3, 3] = p
    return M


def quat_of(R):
    q = np.zeros(4)
    import mujoco
    mujoco.mju_mat2Quat(q, np.ascontiguousarray(R).flatten())
    return q


def slerp_R(R0, R1, s):
    import mujoco
    q0, q1 = quat_of(R0), quat_of(R1)
    if q0 @ q1 < 0:
        q1 = -q1
    d = np.clip(q0 @ q1, -1, 1)
    th = math.acos(d)
    q = q0 if th < 1e-9 else (math.sin((1 - s) * th) * q0 + math.sin(s * th) * q1) / math.sin(th)
    q /= np.linalg.norm(q)
    R = np.zeros(9)
    mujoco.mju_quat2Mat(R, q)
    return R.reshape(3, 3)


def door_T(deg, hinge):
    """Pose (world from rest) of the drop-down door at `deg` (top edge forward, about +X through the hinge)."""
    hy, hz = hinge
    R = rot_x(deg)
    c = np.array([0, hy, hz])
    return T(R, c - R @ c)


# ---------------------------------------------------------------------------------------------------------------
# Machine geometry -> convex pieces
# ---------------------------------------------------------------------------------------------------------------
REGION = dict(x=(-560.0, 1010.0), y=(-470.0, 240.0))
HULL_ONLY = ("Guard frame", "Optics bridge posts", "Chamber legs", "rack frame", "Rack side", "Leveling", "UPS", "Fiber laser",
             "Scan +", "DIN-rail", "Dry scroll", "Trace O2", "Sealed side-channel", "Sealed cyclone", "Argon solenoid", "Argon pressure",
             "Z actuator", "Z bracket", "Z servo", "Recoater servo", "Recoater motor", "Base plate", "Lift-out wall liners")


def body_of(p):
    """Free body (moving in some operation) a part belongs to, or '' for the static machine."""
    n = p.name
    if "context" in p.tags:
        return None
    if n.startswith("Build plate"):
        return "plate"
    if n.startswith("Overflow jar") or n.startswith("Overflow clamp"):
        return "jar"
    if n.startswith("Lift-out wall liners"):
        return "liners"
    g = p.group
    if g == "recoater":
        return "holder" if ("Blade holder" in n or "recoater blade" in n) else "recoater"
    if g == "piston":
        return "piston"
    if g in ("gdoor", "door", "drawer", "zstage", "module"):
        return g
    if g == "cartridge":
        return "reservoir"
    return ""


def tess(shape, tol=0.25):
    import trimesh
    vs, ts = shape.tessellate(tol, 0.3)
    v = np.array([(q.x, q.y, q.z) for q in vs]) / 1000.0
    tm = trimesh.Trimesh(v, np.array(ts), process=True)
    tm.merge_vertices()
    return tm


def convex_pieces(name, shape, cache: pathlib.Path):
    import coacd
    import trimesh
    bb = shape.BoundingBox()
    key = hashlib.md5((name + f"{bb.xmin:.3f}{bb.ymin:.3f}{bb.zmin:.3f}{bb.xmax:.3f}{bb.ymax:.3f}{bb.zmax:.3f}" + f"{shape.Volume():.2f}").encode()).hexdigest()[:14]
    d = cache / key
    if d.exists() and (d / "done").exists():
        return sorted(d.glob("p*.stl"))
    d.mkdir(parents=True, exist_ok=True)
    pieces = []
    solids = list(shape.Solids()) or [shape]
    for s in solids:
        tm = tess(s)
        if len(tm.faces) == 0:
            continue
        hull = tm.convex_hull
        ratio = tm.volume / max(hull.volume, 1e-15) if tm.volume > 0 else 0.0
        if any(k in name for k in HULL_ONLY) or ratio > 0.9 or len(solids) > 40 or os.environ.get("ROBOT_HULL_ONLY"):
            if os.environ.get("ROBOT_HULL_ONLY") and ratio <= 0.9:
                print(f"    hull only (no CoACD): {name[:60]}", flush=True)
            pieces.append(hull)
            continue
        try:
            res = coacd.run_coacd(coacd.Mesh(tm.vertices, tm.faces), threshold=0.03, max_convex_hull=32, preprocess_mode="auto",
                                  resolution=2000, mcts_iterations=60, mcts_nodes=15, seed=1)
            pieces += [trimesh.Trimesh(v, f).convex_hull for v, f in res]
        except Exception:  # noqa: BLE001
            pieces.append(hull)
    for k, pc in enumerate(pieces):
        pc.export(d / f"p{k:03d}.stl")
    (d / "done").write_text("ok")
    return sorted(d.glob("p*.stl"))


def in_region(p):
    b = p.shape.BoundingBox()
    return not (b.xmax < REGION["x"][0] or b.xmin > REGION["x"][1] or b.ymax < REGION["y"][0] or b.ymin > REGION["y"][1])


# ---------------------------------------------------------------------------------------------------------------
# MuJoCo model
# ---------------------------------------------------------------------------------------------------------------
def hexrgba(c, a=1.0):
    return [int(c[1:3], 16) / 255, int(c[3:5], 16) / 255, int(c[5:7], 16) / 255, a]


def build_model(M, parts, men: pathlib.Path, cache: pathlib.Path, base_mm, fingers="stock", extra=()):
    """MjSpec with the machine (static body + free bodies), the UR10e on its mount and the 2F-85.
    fingers: 'stock' (menagerie pads) or 'custom' (stepped fingertips, FINGER). extra: (body, kind, size, pos) primitives."""
    import mujoco
    spec = mujoco.MjSpec()
    spec.compiler.degree = False
    spec.memory = 256 * 1024 * 1024
    spec.option.timestep = 0.002
    try:
        spec.visual.global_.offwidth = 1280
        spec.visual.global_.offheight = 960
    except AttributeError:
        pass
    wb = spec.worldbody
    lt = wb.add_light()
    lt.pos = [0.3, -1.6, 1.6]
    lt.dir = [-0.1, 0.8, -0.6]
    lt.diffuse = [0.7, 0.7, 0.7]
    lt2 = wb.add_light()
    lt2.pos = [-0.8, -0.6, 1.4]
    lt2.dir = [0.4, 0.3, -0.8]
    lt2.diffuse = [0.35, 0.35, 0.35]
    bodies = {"": wb}
    names = {}
    t0 = time.time()
    for i, p in enumerate(parts):
        bn = body_of(p)
        if bn is None or not in_region(p):
            continue
        if bn not in bodies and bn != "liners":
            b = wb.add_body()
            b.name = bn
            b.add_freejoint()
            bodies[bn] = b
        files = convex_pieces(p.name, p.shape, cache)
        rgba = hexrgba(p.color, max(0.35, p.opacity))
        for k, f in enumerate(files):
            mn = f"m{i}_{k}"
            me = spec.add_mesh()
            me.name = mn
            me.file = str(f)
            bk = bn
            if bn == "liners":                       # one free body per liner: back, left, right
                import trimesh
                cx_ = trimesh.load(f).centroid[0]
                bk = "liner_r" if cx_ > 0.1 else ("liner_l" if cx_ < -0.1 else "liner_b")
                if bk not in bodies:
                    b = wb.add_body()
                    b.name = bk
                    b.add_freejoint()
                    bodies[bk] = b
            g = bodies[bk].add_geom()
            g.name = f"p{i}_{k}"
            g.type = mujoco.mjtGeom.mjGEOM_MESH
            g.meshname = mn
            g.rgba = rgba
            g.density = 500.0 if bn else 0.0
            g.contype, g.conaffinity = 2, 1
        names[i] = (p.name, bn)
    print(f"  machine pieces ready in {time.time() - t0:.0f} s", flush=True)
    # tray, VLM lintel, MiR250 + robot cabinet (context boxes)
    zt = M.Z_TRAY / 1000
    for nm, size, pos, rgba in [
        ("tray", (1.225, 0.432, 0.012), (0, 0, zt - 0.012), [0.84, 0.86, 0.88, 1]),
        ("vlm_lintel", (1.3, 0.05, 0.15), (0, (TRAY_FRONT_Y - 50) / 1000, zt + LINTEL_Z / 1000 + 0.15), [0.75, 0.75, 0.8, 0.5]),
        ("mir250", (0.4, 0.29, 0.299), (base_mm[0] / 1000, base_mm[1] / 1000, base_mm[2] / 1000 - 0.3), [0.25, 0.27, 0.3, 1]),
    ]:
        g = wb.add_geom()
        g.name = nm
        g.type = mujoco.mjtGeom.mjGEOM_BOX
        g.size = list(size)
        g.pos = list(pos)
        g.rgba = rgba
        g.contype, g.conaffinity = (2, 1) if nm != "mir250" else (0, 0)
    for (bn, kind, size, pos, quat, rgba) in extra:
        b = bodies[bn]
        g = b.add_geom()
        g.name = f"extra_{bn}_{len(b.geoms)}"
        g.type = kind
        g.size = list(size)
        g.pos = list(pos)
        g.quat = list(quat)
        g.rgba = rgba
        g.density = 2700.0
        g.contype, g.conaffinity = 2, 1
    # robot and gripper
    robot = mujoco.MjSpec.from_file(str(men / "universal_robots_ur10e/ur10e.xml"))
    grip = mujoco.MjSpec.from_file(str(men / "robotiq_2f85/2f85.xml"))
    gb = grip.body("base")
    s = gb.add_site()
    s.name = "tcp_pad"
    s.pos = [0, 0, 0.1311]
    if fingers == "custom":
        F = FINGER
        for side in ("right", "left"):
            pad = grip.body(f"{side}_pad")
            sgn = 1.0 if side == "right" else -1.0          # pad frame x = sgn * base x (left side is turned 180 deg about z)
            for nm, (w0, w1), (z0, z1), dy in [
                ("drop", (-(F["drop"] + F["blade_t"] / 2), 11.0), (37.5 - 12.0, 37.5 + 8.0), 0.0),
                ("blade", (-(F["drop"] + F["blade_t"] / 2), -(F["drop"] - F["blade_t"] / 2)), (37.5 + 8.0, 37.5 + 8.0 + F["blade_len"] - F["crank_len"]), 0.0),
                ("crank", (-(F["drop"] + F["crank"] + F["blade_t"] / 2), -(F["drop"] - F["blade_t"] / 2)), (37.5 + 8.0 + F["blade_len"] - F["crank_len"], 37.5 + 8.0 + F["blade_len"]), 0.0)]:
                g = pad.add_geom()
                g.name = f"{side}_tip_{nm}"
                g.type = mujoco.mjtGeom.mjGEOM_BOX
                g.size = [abs(w1 - w0) / 2000, F["thick"] / 2000, (z1 - z0) / 2000]
                g.pos = [sgn * (w0 + w1) / 2000, -0.0026, (z0 + z1) / 2000]
                g.rgba = [0.75, 0.55, 0.2, 1]
                g.density = 2700.0
        s2 = gb.add_site()
        s2.name = "tcp_tip"           # grip centre of the cranked tip, set below once the pad's height is known
    site = robot.site("attachment_site")
    robot.attach(grip, site=site, prefix="g_")
    fr = wb.add_frame()
    fr.pos = [base_mm[0] / 1000, base_mm[1] / 1000, base_mm[2] / 1000]
    fr.quat = [0.7071068, 0, 0, 0.7071068]     # base turned so that the arm's zero-pan direction faces the machine
    spec.attach(robot, frame=fr, prefix="ur_")
    model = spec.compile()
    return spec, model, names


class Cell:
    """The compiled model plus the bookkeeping the ops need."""

    def __init__(self, M, parts, men, cache, base_mm, fingers, extra=()):
        import mujoco
        self.mj = mujoco
        self.M = M
        self.fingers = fingers
        self.spec, self.m, self.names = build_model(M, parts, men, cache, base_mm, fingers, extra)
        m = self.m
        self.d = mujoco.MjData(m)
        self.arm_j = [m.joint(f"ur_{n}").id for n in ("shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint")]
        self.arm_q = np.array([m.jnt_qposadr[j] for j in self.arm_j])
        self.arm_v = np.array([m.jnt_dofadr[j] for j in self.arm_j])
        self.lo = m.jnt_range[self.arm_j, 0].copy()
        self.hi = m.jnt_range[self.arm_j, 1].copy()
        self.free = {}
        for b in range(m.nbody):
            nm = m.body(b).name
            if m.body_jntnum[b] == 1 and m.jnt_type[m.body_jntadr[b]] == mujoco.mjtJoint.mjJNT_FREE:
                self.free[nm] = (b, m.jnt_qposadr[m.body_jntadr[b]])
        self.robot_bodies = {b for b in range(m.nbody) if m.body(b).name.startswith("ur_")}
        self.grip_bodies = {b for b in range(m.nbody) if m.body(b).name.startswith("ur_g_")}
        for g in range(m.ngeom):
            b = m.geom_bodyid[g]
            if b in self.robot_bodies:
                if m.geom_contype[g] or m.geom_conaffinity[g] or m.geom_group[g] == 3:
                    if m.geom_group[g] == 3 or m.geom_type[g] == mujoco.mjtGeom.mjGEOM_BOX:
                        m.geom_contype[g], m.geom_conaffinity[g] = 1, 2
                    else:
                        m.geom_contype[g], m.geom_conaffinity[g] = 0, 0
                m.geom_margin[g] = 0.04
        self.site_pad = m.site("ur_g_tcp_pad").id
        self.site = self.site_pad
        self.finger_table()
        if fingers == "custom":
            self.set_gap(50.0)
            mujoco.mj_kinematics(m, self.d)
            gbid = m.body("ur_g_base").id
            Rb = self.d.xmat[gbid].reshape(3, 3)
            pb = self.d.xpos[gbid]
            # the crank's grip centre: 20 mm in from the tip, centred on the crank's thickness, on the gripper axis
            pid = m.body("ur_g_right_pad").id
            pad_local = Rb.T @ (self.d.xpos[pid] - pb)
            F = FINGER
            z_tip = pad_local[2] + (37.5 + 8.0 + F["blade_len"] - 20.0) / 1000
            w_tip = -(F["drop"] + F["crank"]) / 1000
            sid = m.site("ur_g_tcp_tip").id
            m.site_pos[sid] = [w_tip, 0.0, z_tip]
            self.site_tip = sid
        self.pad_geoms = {g for g in range(m.ngeom) if m.geom_bodyid[g] in self.grip_bodies}
        gb_arr = np.array(m.geom_bodyid)
        self.body_geoms = {b: np.where(gb_arr == b)[0] for (b, qa) in self.free.values()}
        self.free_ids = set(self.body_geoms)
        self._held_now = []
        self.default_free = {}
        for nm, (b, qa) in self.free.items():
            self.default_free[nm] = np.array([0, 0, 0, 1, 0, 0, 0], float)

    # ---- gripper fingers: equilibrium joint values vs opening, from the menagerie model's own linkage ----
    def finger_table(self):
        mujoco = self.mj
        men = pathlib.Path(ARGS.menagerie)
        g = mujoco.MjModel.from_xml_path(str(men / "robotiq_2f85/2f85.xml"))
        gd = mujoco.MjData(g)
        g.opt.gravity[:] = 0
        rows = []
        for u in np.linspace(0, 255, 52):
            gd.ctrl[0] = u
            for _ in range(600):
                mujoco.mj_step(g, gd)
            rp = gd.geom("right_pad1")
            lp = gd.geom("left_pad1")
            Rb = gd.body("base").xmat.reshape(3, 3)
            gap = abs((rp.xpos - lp.xpos) @ Rb[:, 1]) - 2 * 0.004
            rows.append((gap * 1000, gd.qpos.copy()))
        rows.sort(key=lambda r: r[0])
        self.ftab_gap = np.array([r[0] for r in rows])
        self.ftab_q = np.array([r[1] for r in rows])
        self.fj = [self.m.joint(f"ur_g_{g.joint(k).name}").id for k in range(g.njnt)]
        self.fq = [self.m.jnt_qposadr[j] for j in self.fj]
        self.gap_range = (float(self.ftab_gap.min()), float(self.ftab_gap.max()))

    def set_gap(self, gap_mm):
        gap = np.clip(gap_mm, self.ftab_gap.min(), self.ftab_gap.max())
        q = np.array([np.interp(gap, self.ftab_gap, self.ftab_q[:, k]) for k in range(self.ftab_q.shape[1])])
        for k, a in enumerate(self.fq):
            self.d.qpos[a] = q[k]

    def set_body(self, name, Tw):
        if name not in self.free:
            return
        b, qa = self.free[name]
        self.d.qpos[qa:qa + 3] = Tw[:3, 3] / 1000.0
        self.d.qpos[qa + 3:qa + 7] = quat_of(Tw[:3, :3])

    def reset_bodies(self):
        for nm, (b, qa) in self.free.items():
            self.d.qpos[qa:qa + 7] = self.default_free[nm]

    # ---- IK ----
    def fk(self, q):
        self.d.qpos[self.arm_q] = q
        self.mj.mj_kinematics(self.m, self.d)
        self.mj.mj_comPos(self.m, self.d)
        return self.d.site_xpos[self.site].copy(), self.d.site_xmat[self.site].reshape(3, 3).copy()

    def ik(self, q0, p_mm, R, iters=250):
        mujoco = self.mj
        p = np.asarray(p_mm) / 1000.0
        q = q0.copy()
        jp = np.zeros((3, self.m.nv))
        jr = np.zeros((3, self.m.nv))
        lam = 0.02
        for it in range(iters):
            x, Rc = self.fk(q)
            ep = p - x
            Re = R @ Rc.T
            qe = quat_of(Re)
            if qe[0] < 0:
                qe = -qe
            er = 2 * qe[1:]
            if np.linalg.norm(ep) < 5e-5 and np.linalg.norm(er) < 5e-4:
                break
            mujoco.mj_jacSite(self.m, self.d, jp, jr, self.site)
            J = np.vstack([jp[:, self.arm_v], 0.5 * jr[:, self.arm_v]])
            e = np.concatenate([ep, 0.5 * er])
            dq = J.T @ np.linalg.solve(J @ J.T + lam ** 2 * np.eye(6), e)
            n = np.linalg.norm(dq)
            if n > 0.3:
                dq *= 0.3 / n
            q = np.clip(q + dq, self.lo, self.hi)
        x, Rc = self.fk(q)
        ep = np.linalg.norm(p - x) * 1000
        qe = quat_of(R @ Rc.T)
        er = math.degrees(2 * math.acos(min(1.0, abs(qe[0]))))
        return q, ep, er

    def seeds(self, p_mm):
        base = self.m.body("ur_base").id
        mujoco = self.mj
        mujoco.mj_kinematics(self.m, self.d)
        b = self.d.xpos[base] * 1000
        yaw = math.atan2(p_mm[1] - b[1], p_mm[0] - b[0])
        out = []
        for pan_off in (0.0, math.pi):
            for sl in (-0.6, -1.2, -1.9, -2.5):
                for el in (1.0, 1.8, 2.5, -1.0, -1.8):
                    for w1 in (-1.57, 0.0, -3.0):
                        for w2 in (1.57, -1.57):
                            out.append(np.array([yaw - math.pi / 2 + pan_off, sl, el, w1, w2, 0.0]))
        return out

    def ik_first(self, p_mm, R, prefer=None):
        best = None
        for s in self.seeds(p_mm):
            q, ep, er = self.ik(s, p_mm, R, iters=120)
            if ep < 0.5 and er < 0.3:
                q, ep, er = self.ik(q, p_mm, R, iters=200)
                score = self.posture_score(q) if prefer is None else prefer(q)
                if best is None or score < best[0]:
                    best = (score, q, ep, er)
        if best is None:
            q, ep, er = self.ik(self.seeds(p_mm)[0], p_mm, R, iters=400)
            return q, ep, er
        return best[1], best[2], best[3]

    def posture_score(self, q):
        """Prefer elbow-up postures with the elbow high (keeps the forearm off the tray and machine)."""
        self.fk(q)
        el = self.d.xpos[self.m.body("ur_forearm_link").id][2]
        wr = self.d.xpos[self.m.body("ur_wrist_1_link").id][2]
        lintel = (self.M.Z_TRAY + LINTEL_Z) / 1000 - 0.08
        over = max(0.0, el - lintel)
        return 10 * over - (el - wr) + 0.05 * np.sum(np.abs(q[3:]))

    # ---- clearance ----
    def clearance(self, held=(), ignore=(), ignore_all=()):
        """Smallest distance (mm) between robot / gripper / held bodies and the machine; list of the closest pairs.
        ignore: machine bodies the gripper may touch (the grasped part); ignore_all: machine bodies ignored for everyone."""
        mujoco = self.mj
        m, d = self.m, self.d
        held_ids = {self.free[h][0] for h in held if h in self.free}
        ign = {self.free[h][0] for h in ignore if h in self.free}
        ign_all = {self.free[h][0] for h in ignore_all if h in self.free}
        for ids in self._held_now:
            m.geom_contype[ids], m.geom_conaffinity[ids], m.geom_margin[ids] = 2, 1, 0.0
        self._held_now = [self.body_geoms[b] for b in held_ids]
        for ids in self._held_now:
            m.geom_contype[ids], m.geom_conaffinity[ids], m.geom_margin[ids] = 1, 2, 0.04
        mujoco.mj_kinematics(m, d)
        mujoco.mj_collision(m, d)
        best = {}
        for k in range(d.ncon):
            c = d.contact[k]
            g1, g2 = c.geom1, c.geom2
            b1, b2 = m.geom_bodyid[g1], m.geom_bodyid[g2]
            r1 = b1 in self.robot_bodies or b1 in held_ids
            r2 = b2 in self.robot_bodies or b2 in held_ids
            if r1 == r2:
                continue
            if r2:
                g1, g2, b1, b2 = g2, g1, b2, b1
            if b2 in ign_all:
                continue
            if b2 in ign and (b1 in self.grip_bodies or b1 in held_ids):
                continue
            if b1 in held_ids and b2 in held_ids:
                continue
            key = (g1, g2)
            if key not in best or c.dist < best[key]:
                best[key] = c.dist
        if not best:
            return 40.0, []
        pairs = sorted(best.items(), key=lambda kv: kv[1])[:6]
        return pairs[0][1] * 1000, [(self.geom_label(a), self.geom_label(b), round(v * 1000, 1), int(a), int(b)) for (a, b), v in pairs]

    def geom_label(self, g):
        m = self.m
        b = m.geom_bodyid[g]
        bn = m.body(b).name
        if bn.startswith("ur_"):
            return bn.replace("ur_g_", "gripper ").replace("ur_", "UR10e ") + (f" ({m.geom(g).name.replace('ur_g_', '')})" if "tip" in m.geom(g).name else "")
        nm = m.geom(g).name
        if nm.startswith("p"):
            i = int(nm[1:].split("_")[0])
            return self.names.get(i, (nm, ""))[0]
        return nm


# ---------------------------------------------------------------------------------------------------------------
# Operations: lists of frames
# ---------------------------------------------------------------------------------------------------------------
def line(label, p0, p1, R0, R1=None, step=4.0, **kw):
    """Frames along a straight TCP move (mm), with an optional rotation from R0 to R1 and per-frame extras."""
    R1 = R0 if R1 is None else R1
    n = max(2, int(math.ceil(np.linalg.norm(np.subtract(p1, p0)) / step)) + 1)
    ang = math.degrees(math.acos(np.clip((np.trace(R0.T @ R1) - 1) / 2, -1, 1)))
    n = max(n, int(ang / 2.0) + 2)
    out = []
    for k in range(n):
        s = k / (n - 1)
        f = dict(label=label, p=np.add(p0, s * np.subtract(p1, p0)), R=slerp_R(R0, R1, s), s=s)
        for key, v in kw.items():
            f[key] = v(s) if callable(v) else v
        out.append(f)
    return out


def held_follow(T_tcp_grasp, T_body_grasp):
    """Function mapping a TCP pose (p, R) to the held body's pose, keeping the grasp offset."""
    off = np.linalg.inv(T_tcp_grasp) @ T_body_grasp

    def f(p, R):
        return T(R, p) @ off
    return f


def op_frames(name, M, P, parts):
    """Frames for each operation. Each frame: label, p (mm), R, gap (mm), site ('pad'|'tip'), bodies {name: T}, held,
    ignore (machine bodies the gripper may touch), force (N, world vector the robot applies), mass (kg held)."""
    hinge = M.DOOR_HINGE
    G_OPEN = {"gdoor": T(p=(470.0, 0, 0))}
    D_OPEN = {"door": door_T(95.0, hinge)}
    frames = []

    def add(fs, **common):
        for f in fs:
            for k, v in common.items():
                f.setdefault(k, v)
            frames.append(f)

    if name == "guard_door":
        # as drawn the door has no handle: the frames use the fix (a Ø12 bar on 45 mm standoffs at x = -310)
        R = grip_R((0, 1, 0), (1, 0, 0))
        hx, hy, hz = -310.0, -317.0, 100.0
        st = dict(site="pad", held=(), ignore=("gdoor",), mass=0.0)
        add(line("approach", (hx, hy - 150, hz), (hx, hy, hz), R, gap=40.0), **st, bodies={})
        add(line("close on the handle", (hx, hy, hz), (hx, hy, hz), R, gap=lambda s: 40 - 28 * s), **st, bodies={})
        add(line("slide open 470 mm", (hx, hy, hz), (hx + 470, hy, hz), R, gap=12.0, step=10.0,
                 bodies=lambda s: {"gdoor": T(p=(470.0 * s, 0, 0))}, force=(30.0, 0, 0)), **st)
        add(line("release and retreat", (hx + 470, hy, hz), (hx + 470, hy - 150, hz), R, gap=40.0), **st, bodies=G_OPEN)
        add(line("slide closed (reverse)", (hx + 470, hy, hz), (hx, hy, hz), R, gap=12.0, step=10.0,
                 bodies=lambda s: {"gdoor": T(p=(470.0 * (1 - s), 0, 0))}, force=(-30.0, 0, 0)), **st)
    elif name == "chamber_door_open":
        R0 = grip_R((0, 1, 0), (0, 0, 1))
        h = np.array([0.0, -152.0, 95.0])
        st = dict(site="pad", held=(), ignore=("door",), mass=0.0)
        add(line("approach the handle", h + (0, -160, 0), h, R0, gap=40.0), **st, bodies=G_OPEN)
        add(line("close on the handle", h, h, R0, gap=lambda s: 40 - 28 * s), **st, bodies=G_OPEN)
        for k in range(1, 39):
            deg = 2.5 * k
            Td = door_T(deg, hinge)
            p = (Td @ np.append(h, 1))[:3]
            frames.append(dict(label="swing open on the handle", p=p, R=Td[:3, :3] @ R0, gap=12.0, site="pad", held=(), ignore=("door",),
                               bodies={**G_OPEN, "door": Td}, mass=0.0, deg=deg, force=tuple(Td[:3, :3] @ np.array([0, -10.0, 0]))))
    elif name == "chamber_door_close":
        Td = door_T(95.0, hinge)
        h = np.array([0.0, -152.0, 95.0])
        R0 = grip_R((0, 1, 0), (0, 0, 1))
        hw = (Td @ np.append(h, 1))[:3]
        st = dict(site="pad", held=(), ignore=("door",), mass=0.0)
        add(line("approach the handle (door open)", hw + (0, -160, 0), hw, R0, gap=40.0), **st, bodies={**G_OPEN, **D_OPEN})
        add(line("close on the handle", hw, hw, R0, gap=lambda s: 40 - 28 * s), **st, bodies={**G_OPEN, **D_OPEN})
        Rg = Td[:3, :3].T @ R0          # grasp orientation in the door's frame
        for k in range(1, 39):
            deg = 95.0 - 2.5 * k
            Tk = door_T(deg, hinge)
            p = (Tk @ np.append(h, 1))[:3]
            frames.append(dict(label="lift closed on the handle", p=p, R=Tk[:3, :3] @ Rg, gap=12.0, site="pad", held=(), ignore=("door",),
                               bodies={**G_OPEN, "door": Tk}, mass=0.0, deg=deg, force=tuple(Tk[:3, :3] @ np.array([0, 0, 12.0]))))
        # second strategy: push the door's outer face with closed fingertips (handle released)
        Rp = grip_R((0, 1, 0), (0, 0, 1))
        pf = np.array([0.0, -126.0, 60.0])
        for k in range(0, 39):
            deg = 95.0 - 2.5 * k
            Tk = door_T(deg, hinge)
            n = Tk[:3, :3] @ np.array([0, 1.0, 0])
            p = (Tk @ np.append(pf, 1))[:3] - n * 19.5
            frames.append(dict(label="push closed on the outer face", p=p, R=Tk[:3, :3] @ Rp, gap=0.0, site="pad", held=(), ignore=("door",),
                               bodies={**G_OPEN, "door": Tk}, mass=0.0, deg=deg, force=tuple(n * 15.0)))
    elif name == "plate_exchange":
        Rp = grip_R((0, 1, 0), (1, 0, 0))
        st = dict(site="tip", mass=0.06)
        base = {**G_OPEN, **D_OPEN, "piston": T(p=(0, 0, 8.0)), "zstage": T(p=(0, 0, 8.0))}
        plate0 = T(p=(0, 0, 8.0))
        zc = 6.0                                     # crank grip centre: crank z 1..11, the lip in the 1..4 groove
        pg = np.array([0.0, 0.0, zc])
        pre_hi = np.array([0.0, -110.0, zc + 9.0])   # tip over the 8 mm sill, then down inside the chamber
        add(line("approach over the sill", np.array([0.0, -420.0, zc + 9.0]), pre_hi, Rp, gap=68.0, step=6.0), **st, held=(), ignore=(), bodies={**base, "plate": plate0})
        add(line("down inside the chamber", pre_hi, pre_hi + (0, 25, -9), Rp, gap=68.0), **st, held=(), ignore=(), bodies={**base, "plate": plate0})
        add(line("in to the plate", pre_hi + (0, 25, -9), pg, Rp, gap=68.0), **st, held=(), ignore=(), bodies={**base, "plate": plate0})
        add(line("close on the groove", pg, pg, Rp, gap=lambda s: 68 - 17.5 * s), **st, held=(), ignore=("plate",), bodies={**base, "plate": plate0})
        # twist the bayonet 60 deg about the plate axis (-30 -> +30: approach skewed by -30 first)
        fol = held_follow(T(Rp, pg), plate0)
        tw = []
        for k in range(0, 31):
            deg = -30.0 + 2.0 * k
            Rz = rot_z(deg)
            p = Rz @ pg
            tw.append(dict(label="bayonet twist 60 deg", p=p, R=Rz @ Rp, gap=50.5, bodies={**base, "plate": T(Rz, (0, 0, 8.0))},
                           held=("plate",), ignore=("plate", "piston"), seat=True))
        # the gripper first rotates (plate still free on the block, open fingers) to -30 deg: done with open fingers
        pre = []
        for k in range(0, 16):
            deg = -2.0 * k
            Rz = rot_z(deg)
            pre.append(dict(label="skew to -30 deg (fingers open)", p=Rz @ pg, R=Rz @ Rp, gap=68.0, bodies={**base, "plate": plate0}, held=(), ignore=("plate",)))
        frames[:] = [f for f in frames if f["label"] != "close on the groove"]
        add(pre, **st)
        add(line("close on the groove", rot_z(-30) @ pg, rot_z(-30) @ pg, rot_z(-30) @ Rp, gap=lambda s: 68 - 17.5 * s), **st, held=(), ignore=("plate",), bodies={**base, "plate": plate0})
        add(tw, **st)
        Rz30 = rot_z(30.0)
        p30 = Rz30 @ pg
        fol = held_follow(T(Rz30 @ Rp, p30), T(Rz30, (0, 0, 8.0)))
        add(line("lift 16 mm off the block", p30, p30 + (0, 0, 16), Rz30 @ Rp, gap=50.5, step=1.0,
                 bodies=lambda s: {**base, "plate": fol(p30 + (0, 0, 16 * s), Rz30 @ Rp)}), **st, held=("plate",), ignore=("plate",), seat=True)
        pl = p30 + (0, 0, 16)
        pl0 = pg + (0, 0, 16)
        add(line("turn back square", pl, pl0, Rz30 @ Rp, Rp, gap=50.5,
                 bodies=lambda s: None), **st, held=("plate",), ignore=("plate",))
        # bodies for the turn-back frames: plate follows the TCP
        for f in frames:
            if f["label"] == "turn back square":
                f["bodies"] = {**base, "plate": fol(f["p"], f["R"])}
        add(line("out through the door", pl0, pl0 + (0, -420, 0), Rp, gap=50.5, step=6.0,
                 bodies=lambda s: None), **st, held=("plate",), ignore=("plate",))
        for f in frames:
            if f["label"] == "out through the door":
                f["bodies"] = {**base, "plate": fol(f["p"], f["R"])}
    elif name == "drawer":
        R = grip_R((0, 1, 0), (1, 0, 0))
        p0 = np.array([0.0, -138.75, 128.0])
        st = dict(site="pad", mass=0.17)
        base = {**G_OPEN, **D_OPEN}
        add(line("approach the pull tab", p0 + (0, -160, 0), p0, R, gap=56.0), **st, held=(), ignore=("drawer",), bodies=base)
        add(line("close on the tab's posts", p0, p0, R, gap=lambda s: 56 - 16 * s), **st, held=(), ignore=("drawer",), bodies=base)
        add(line("pull 120 mm", p0, p0 + (0, -120, 0), R, gap=40.0, step=4.0, bodies=lambda s: {**base, "drawer": T(p=(0, -120 * s, 0))},
                 force=(0, -20.0, 0)), **st, held=(), ignore=("drawer",))
        add(line("push home (seat the O-ring)", p0 + (0, -120, 0), p0, R, gap=40.0, step=4.0, bodies=lambda s: {**base, "drawer": T(p=(0, -120 * (1 - s), 0))},
                 force=(0, 350.0, 0)), **st, held=(), ignore=("drawer",))
    elif name in ("reservoir", "reservoir_stock"):
        site = "tip" if name == "reservoir" else "pad"
        R = grip_R((0, 1, 0), (1, 0, 0))
        zc = 253.0 if site == "tip" else 255.0
        yc = -24.0 if site == "tip" else -33.75
        p0 = np.array([-90.0, yc, zc])
        st = dict(site=site, mass=0.45)
        base = {**G_OPEN}
        add(line("approach the handle", p0 + (0, -260, 0), p0, R, gap=30.0, step=6.0), **st, held=(), ignore=("reservoir",), bodies=base)
        add(line("close on the handle fin", p0, p0, R, gap=lambda s: 30 - 22 * s), **st, held=(), ignore=("reservoir",), bodies=base)
        add(line("pull out over the detents and off the dock", p0, p0 + (0, -125, 0), R, gap=8.0, step=4.0,
                 bodies=lambda s: {**base, "reservoir": T(p=(0, -125 * s, 0))}, force=(0, -40.0, 0)), **st, held=("reservoir",), ignore=("reservoir",), seat=True)
        add(line("carry out of the optics-bridge slot", p0 + (0, -125, 0), p0 + (0, -330, 0), R, gap=8.0, step=6.0,
                 bodies=lambda s: {**base, "reservoir": T(p=(0, -125 - 205 * s, 0))}), **st, held=("reservoir",), ignore=("reservoir",))
    elif name == "overflow_jar":
        R = grip_R((0, 1, 0), (1, 0, 0))
        p0 = np.array([100.0, -10.0, -100.0])
        st = dict(site="pad", mass=0.45)
        base = {**G_OPEN, **D_OPEN}
        add(line("approach the jar under the chamber", p0 + (0, -300, 0), p0, R, gap=60.0, step=6.0), **st, held=(), ignore=("jar",), bodies=base)
        add(line("close on the jar", p0, p0, R, gap=lambda s: 60 - 19 * s), **st, held=(), ignore=("jar",), bodies=base)
        add(line("lower 6 mm off the KF-40 stub", p0, p0 + (0, 0, -6), R, gap=41.3, step=1.0, bodies=lambda s: {**base, "jar": T(p=(0, 0, -6 * s))}),
            **st, held=("jar",), ignore=("jar",), seat=True)
        add(line("out to the front", p0 + (0, 0, -6), p0 + (0, -330, -6), R, gap=41.3, step=6.0, bodies=lambda s: {**base, "jar": T(p=(0, -330 * s, -6))}),
            **st, held=("jar",), ignore=("jar",))
    elif name == "blade_cartridge":
        R = grip_R((0, 1, 0), (1, 0, 0))
        st = dict(site="tip", mass=0.12)
        rec = T(p=(106.0, 0, 0))                     # recoater driven to the middle: holder at x -9..9
        base = {**G_OPEN, **D_OPEN, "recoater": rec}
        h0 = rec
        pc = np.array([0.75, -38.0, 15.0])            # crank z 10..20 on the holder (z 3..34)
        add(line("approach over the sill", pc + (0, -380, 0), pc + (0, -60, 0), R, gap=36.0, step=6.0), **st, held=(), ignore=(), bodies={**base, "holder": h0})
        add(line("in to the holder", pc + (0, -60, 0), pc, R, gap=36.0), **st, held=(), ignore=("holder",), bodies={**base, "holder": h0})
        add(line("close on holder + blade", pc, pc, R, gap=lambda s: 36 - 16.5 * s), **st, held=(), ignore=("holder",), bodies={**base, "holder": h0})
        add(line("pull 10 mm out of the arm's pocket", pc, pc + (0, -10, 0), R, gap=19.5, step=1.0,
                 bodies=lambda s: {**base, "holder": T(p=(106.0, -10 * s, 0))}, force=(0, -40.0, 0)), **st, held=("holder",), ignore=("holder",), seat=True)
        add(line("lift 12 mm over the sill", pc + (0, -10, 0), pc + (0, -10, 12), R, gap=19.5, step=1.0,
                 bodies=lambda s: {**base, "holder": T(p=(106.0, -10, 12 * s))}), **st, held=("holder",), ignore=("holder",))
        add(line("out through the door", pc + (0, -10, 12), pc + (0, -380, 12), R, gap=19.5, step=6.0,
                 bodies=lambda s: {**base, "holder": T(p=(106.0, -10 - 370 * s, 12))}), **st, held=("holder",), ignore=("holder",))
    elif name == "liner":
        # right side liner, with the fixes the static check asks for (slot open to the back, pull tab at the front top)
        R = grip_R((0, 1, 0), (0, 0, 1))
        st = dict(site="tip", mass=0.06)
        base = {**G_OPEN, **D_OPEN}
        pt = np.array([130.0, -75.0, 104.0])
        add(line("approach the liner's tab", pt + (0, -350, 0), pt, R, gap=20.0, step=6.0), **st, held=(), ignore=("liner_r",), bodies=base)
        add(line("close on the tab", pt, pt, R, gap=lambda s: 20 - 19 * s), **st, held=(), ignore=("liner_r",), bodies=base)
        add(line("off the clips, 40 mm in along the ball screw, tilt 15 deg", pt, pt + (-40, 0, -8), R, rot_y(-15) @ R, gap=1.0,
                 bodies=lambda s: None), **st, held=("liner_r",), ignore=("liner_r",), seat=True)
        add(line("out through the door", pt + (-40, 0, -8), pt + (-40, -400, -8), rot_y(-15) @ R, gap=1.0, step=6.0,
                 bodies=lambda s: None), **st, held=("liner_r",), ignore=("liner_r",))
        fol = held_follow(T(R, pt), T())
        for f in frames:
            if f["bodies"] is None:
                f["bodies"] = {**base, "liner_r": fol(f["p"], f["R"])}
    elif name == "module_swap":
        hb = P["module_handle_bb"]
        R = grip_R((0, 1, 0), (1, 0, 0))
        ph = np.array([0.0, hb[3] - 2.0 - 18.75, (hb[4] + hb[5]) / 2])
        st = dict(site="pad", mass=P["module_mass"])
        zs = T(p=(0, 0, -45.0))
        base = {**G_OPEN, "zstage": zs}
        path = [np.array(q) for q in M.MODULE_PATH]
        add(line("approach the module handle", ph + (0, -300, 0), ph, R, gap=62.0, step=6.0), **st, held=(), ignore=("module",), bodies=base)
        add(line("close on the handle's side arms", ph, ph, R, gap=lambda s: 62 - 14 * s), **st, held=(), ignore=("module",), bodies=base)
        for a, b in zip(path[:-1], path[1:]):
            add(line(f"module path {tuple(int(v) for v in a)} -> {tuple(int(v) for v in b)}", ph + a, ph + b, R, gap=48.0, step=4.0,
                     bodies=lambda s, a=a, b=b: {**base, "module": T(p=a + s * (b - a)), "piston": T(p=a + s * (b - a)), "plate": T(p=a + s * (b - a))},
                     force=(0, 0, 0)), **st, held=("module", "piston", "plate"), ignore=("module",), seat=(a[2] == 0.0))
    return frames


OPS = ["guard_door", "chamber_door_open", "chamber_door_close", "plate_exchange", "drawer", "reservoir_stock", "reservoir",
       "overflow_jar", "blade_cartridge", "liner", "module_swap"]
FINGERS = {"plate_exchange": "custom", "reservoir": "custom", "blade_cartridge": "custom", "liner": "custom"}


# ---------------------------------------------------------------------------------------------------------------
# Running an operation
# ---------------------------------------------------------------------------------------------------------------
def run_op(cell: Cell, name, frames, record=False):
    mujoco = cell.mj
    m, d = cell.m, cell.d
    rows = []
    q = None
    traj = []
    for k, f in enumerate(frames):
        cell.site = cell.site_tip if f.get("site") == "tip" else cell.site_pad
        cell.reset_bodies()
        for bn, Tw in (f.get("bodies") or {}).items():
            cell.set_body(bn, Tw)
        cell.set_gap(f.get("gap", 40.0))
        if q is None:
            q, ep, er = cell.ik_first(f["p"], f["R"])
        else:
            q1, ep, er = cell.ik(q, f["p"], f["R"])
            if (ep > 0.5 or er > 0.3) or np.max(np.abs(q1 - q)) > 0.5:
                q2, ep2, er2 = cell.ik_first(f["p"], f["R"])
                jump = float(np.max(np.abs(q2 - q)))
                if ep2 < ep:
                    q1, ep, er = q2, ep2, er2
                    f["reconfigure_rad"] = jump
            q = q1
        cell.fk(q)
        clr, pairs = cell.clearance(held=f.get("held", ()), ignore=f.get("ignore", ()))
        sh = d.xpos[m.body("ur_upper_arm_link").id]
        wr = d.xpos[m.body("ur_wrist_1_link").id]
        reach = UR10E["arm_mm"] - np.linalg.norm(wr - sh) * 1000
        lim = float(np.min(np.minimum(q - cell.lo, cell.hi - q)))
        rows.append(dict(k=k, label=f["label"], ik_mm=round(float(ep), 3), ik_deg=round(float(er), 3), clear_mm=round(float(clr), 1), pairs=pairs,
                         reach_margin_mm=round(float(reach), 1), limit_margin_deg=round(math.degrees(lim), 1), q=[round(float(v), 5) for v in q],
                         deg=f.get("deg"), seat=bool(f.get("seat", False)), gap=f.get("gap"), force=f.get("force"), mass=f.get("mass", 0.0),
                         reconf=f.get("reconfigure_rad")))
        if record:
            traj.append(dict(q=q.copy(), qpos=d.qpos.copy()))
    return rows, traj


def torques(cell: Cell, rows, frames, speed=0.1):
    """Arm joint torques along the path: inverse dynamics (contacts off) + held weight + applied force; and the largest
    force the arm could apply along each force step's direction."""
    mujoco = cell.mj
    m, d = cell.m, cell.d
    saved = m.opt.disableflags
    m.opt.disableflags |= mujoco.mjtDisableBit.mjDSBL_CONTACT | mujoco.mjtDisableBit.mjDSBL_CONSTRAINT
    Q = np.array([r["q"] for r in rows])
    P = np.array([f["p"] for f in frames]) / 1000
    ds = np.r_[0, np.linalg.norm(np.diff(P, axis=0), axis=1)]
    dq = np.r_[0, np.max(np.abs(np.diff(Q, axis=0)), axis=1)]
    dt = np.maximum(ds / speed, dq / 0.8) + 0.02          # 0.1 m/s TCP, joints <= 0.8 rad/s
    t = np.cumsum(dt)
    peak = np.zeros(6)
    worst = None
    fmax = []
    lim = np.array(UR10E["tau_lim"])
    jp = np.zeros((3, m.nv))
    jr = np.zeros((3, m.nv))
    for k in range(len(rows)):
        km, kp = max(k - 1, 0), min(k + 1, len(rows) - 1)
        qd = (Q[kp] - Q[km]) / max(t[kp] - t[km], 1e-3)
        qdd = np.zeros(6)
        if 0 < k < len(rows) - 1:
            qdd = ((Q[kp] - Q[k]) / max(t[kp] - t[k], 1e-3) - (Q[k] - Q[km]) / max(t[k] - t[km], 1e-3)) / max((t[kp] - t[km]) / 2, 1e-3)
        d.qpos[:] = 0
        d.qvel[:] = 0
        d.qacc[:] = 0
        cell.reset_bodies()
        d.qpos[cell.arm_q] = Q[k]
        d.qvel[cell.arm_v] = qd
        d.qacc[cell.arm_v] = qdd
        mujoco.mj_inverse(m, d)
        tau = d.qfrc_inverse[cell.arm_v].copy()
        cell.site = cell.site_tip if frames[k].get("site") == "tip" else cell.site_pad
        mujoco.mj_jacSite(m, d, jp, jr, cell.site)
        J = jp[:, cell.arm_v]
        mass = rows[k]["mass"] or 0.0
        tau_static = tau + J.T @ (mass * np.array([0, 0, 9.81]))
        tau_all = tau_static.copy()
        F = rows[k]["force"]
        if F is not None:
            F = np.asarray(F, float)
            tau_all = tau_all + J.T @ F
            u = F / max(np.linalg.norm(F), 1e-9)
            a = np.abs(J.T @ u)
            room = lim - np.abs(tau_static)
            fm = float(np.min(np.where(a > 1e-6, room / np.maximum(a, 1e-9), np.inf)))
            fmax.append((rows[k]["label"], float(np.linalg.norm(F)), fm))
        ratio = np.abs(tau_all) / lim
        peak = np.maximum(peak, np.abs(tau_all))
        if worst is None or ratio.max() > worst[0]:
            worst = (float(ratio.max()), k, int(np.argmax(ratio)))
    m.opt.disableflags = saved
    per = {}
    for lab, need, fm in fmax:
        cur = per.get(lab)
        if cur is None or fm < cur[1]:
            per[lab] = (need, fm)
    return dict(peak_Nm=[round(float(v), 1) for v in peak], peak_ratio=round(worst[0], 3) if worst else 0.0,
                worst_joint=["base", "shoulder", "elbow", "wrist 1", "wrist 2", "wrist 3"][worst[2]] if worst else "",
                duration_s=round(float(t[-1]), 1),
                forces={k: dict(needed_N=round(v[0], 1), arm_can_N=round(v[1], 0)) for k, v in per.items()})


# ---------------------------------------------------------------------------------------------------------------
# Exact near-miss check (FCL against a fine tessellation of the B-rep part)
# ---------------------------------------------------------------------------------------------------------------
def exact_pair(cell: Cell, parts, row, frame):
    """Re-measure the closest pair of a frame: the robot-side geom (mesh/primitive, posed by MuJoCo) against the exact
    machine part, tessellated at 0.05 mm and posed as in the frame. Returns mm or None."""
    import fcl
    if not row["pairs"]:
        return None
    _, _, _, ga, gb = row["pairs"][0]
    m, d = cell.m, cell.d
    nm = m.geom(gb).name
    if not nm.startswith("p"):
        return None
    i = int(nm[1:].split("_")[0])
    p = parts[i]
    bn = body_of(p)
    Tw = np.eye(4)
    if bn and bn in (frame.get("bodies") or {}):
        Tw = frame["bodies"][bn]
    tm = tess(p.shape, 0.05)
    v = (Tw[:3, :3] @ (tm.vertices * 1000).T).T / 1000 + Tw[:3, 3] / 1000
    bvh = fcl.BVHModel()
    bvh.beginModel(len(v), len(tm.faces))
    bvh.addSubModel(v, tm.faces)
    bvh.endModel()
    o2 = fcl.CollisionObject(bvh, fcl.Transform())
    gt = m.geom_type[ga]
    R = d.geom_xmat[ga].reshape(3, 3)
    pos = d.geom_xpos[ga]
    sz = m.geom_size[ga]
    mj = cell.mj
    if gt == mj.mjtGeom.mjGEOM_BOX:
        g = fcl.Box(*(2 * sz))
    elif gt == mj.mjtGeom.mjGEOM_CAPSULE:
        g = fcl.Capsule(sz[0], 2 * sz[1])
    elif gt == mj.mjtGeom.mjGEOM_CYLINDER:
        g = fcl.Cylinder(sz[0], 2 * sz[1])
    elif gt == mj.mjtGeom.mjGEOM_MESH:
        mid = m.geom_dataid[ga]
        va, nv = m.mesh_vertadr[mid], m.mesh_vertnum[mid]
        fa, nf = m.mesh_faceadr[mid], m.mesh_facenum[mid]
        vv = m.mesh_vert[va:va + nv].astype(float)
        ff = m.mesh_face[fa:fa + nf].astype(np.int32)
        g = fcl.BVHModel()
        g.beginModel(len(vv), len(ff))
        g.addSubModel(vv, ff)
        g.endModel()
    else:
        return None
    o1 = fcl.CollisionObject(g, fcl.Transform(R, pos))
    req = fcl.DistanceRequest(enable_nearest_points=True)
    res = fcl.DistanceResult()
    dist = fcl.distance(o1, o2, req, res)
    return round(float(dist) * 1000, 2)


# ---------------------------------------------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------------------------------------------
def render_frames(cell: Cell, traj, path_gif, size=(480, 360), every=1, cam=None, png=None, max_frames=60):
    import mujoco
    from PIL import Image
    m, d = cell.m, cell.d
    r = mujoco.Renderer(m, size[1], size[0])
    opt = mujoco.MjvOption()
    opt.geomgroup[:] = 0
    opt.geomgroup[0] = 1
    opt.geomgroup[2] = 1
    c = mujoco.MjvCamera()
    c.lookat[:] = cam.get("lookat", (0.0, -0.25, 0.05)) if cam else (0.0, -0.25, 0.05)
    c.distance = cam.get("distance", 1.6) if cam else 1.6
    c.azimuth = cam.get("azimuth", -125.0) if cam else -125.0
    c.elevation = cam.get("elevation", -22.0) if cam else -22.0
    idx = list(range(0, len(traj), max(1, len(traj) // max_frames)))
    if idx[-1] != len(traj) - 1:
        idx.append(len(traj) - 1)
    imgs = []
    for k in idx:
        d.qpos[:] = traj[k]["qpos"]
        mujoco.mj_kinematics(m, d)
        r.update_scene(d, camera=c, scene_option=opt)
        imgs.append(Image.fromarray(r.render()))
    if png:
        for (k, pth) in png:
            d.qpos[:] = traj[min(k, len(traj) - 1)]["qpos"]
            mujoco.mj_kinematics(m, d)
            r2 = mujoco.Renderer(m, 720, 960)
            r2.update_scene(d, camera=c, scene_option=opt)
            Image.fromarray(r2.render()).save(pth)
            r2.close()
    if path_gif:
        pal = [im.convert("P", palette=Image.ADAPTIVE, colors=96) for im in imgs]
        pal[0].save(path_gif, save_all=True, append_images=pal[1:], duration=110, loop=0, optimize=True)
    r.close()


# ---------------------------------------------------------------------------------------------------------------
def summarize(name, rows, frames, tq, exact):
    ok_ik = all(r["ik_mm"] < 1.0 and r["ik_deg"] < 0.5 for r in rows)
    free = [r for r in rows if not r["seat"]]
    worst = min(free or rows, key=lambda r: r["clear_mm"])
    seat_min = min((r["clear_mm"] for r in rows if r["seat"]), default=None)
    unreach = sorted({r["label"] for r in rows if r["ik_mm"] >= 1.0 or r["ik_deg"] >= 0.5})
    hits = sorted({(r["label"], r["pairs"][0][0], r["pairs"][0][1]) for r in free if r["clear_mm"] < 0.0})
    return dict(op=name, frames=len(rows), ik_all=ok_ik, unreachable_steps=unreach, min_clear_mm=worst["clear_mm"], min_clear_step=worst["label"],
                min_clear_pair=worst["pairs"][0][:3] if worst["pairs"] else None, exact_mm=exact, seat_min_mm=seat_min,
                collisions=[dict(step=h[0], robot=h[1], machine=h[2]) for h in hits][:8],
                reach_margin_min_mm=min(r["reach_margin_mm"] for r in rows), limit_margin_min_deg=min(r["limit_margin_deg"] for r in rows),
                reconfigurations=[(r["label"], round(r["reconf"], 2)) for r in rows if r.get("reconf")][:4], torque=tq)


ARGS = None


def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--cad", default=str(HERE.parent.parent / "cad"))
    ap.add_argument("--menagerie", default="/tmp/robot-work/menagerie")
    ap.add_argument("--cache", default="/tmp/robot-work/mj")
    ap.add_argument("--ops", default=",".join(OPS))
    ap.add_argument("--base", default="0,-782,-212", help="robot base (mm, machine frame): x, y, z")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--tag", default="")
    ARGS = ap.parse_args()
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    cache = pathlib.Path(ARGS.cache)
    cache.mkdir(parents=True, exist_ok=True)
    men = pathlib.Path(ARGS.menagerie)
    fetch_menagerie(men)
    sys.path.insert(0, str(pathlib.Path(ARGS.cad).resolve()))
    import lpbf_low as M
    parts = M.build()
    print(f"{len(parts)} parts built in {time.time() - t0:.0f} s", flush=True)
    P = {}
    for p in parts:
        if p.name.startswith("Module") and "handle" in p.name:
            b = p.shape.BoundingBox()
            P["module_handle_bb"] = (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)
    P["module_mass"] = round(sum((p.mass_kg if p.mass_kg is not None else p.shape.Volume() * 1e-9 * M.MAT.get(p.mat, {}).get("rho", 1000))
                                for p in parts if p.group in ("module", "piston")), 2)
    base = tuple(float(v) for v in ARGS.base.split(","))
    ops = [o for o in ARGS.ops.split(",") if o]
    qy = (0.7071068, 0.7071068, 0, 0)
    extra = [("gdoor", 5, (0.006, 0.08, 0), (-0.310, -0.317, 0.100), (1, 0, 0, 0), [0.9, 0.6, 0.1, 1]),     # the guard-door handle fix: Ø12 bar
             ("gdoor", 5, (0.005, 0.0225, 0), (-0.310, -0.2945, 0.035), qy, [0.9, 0.6, 0.1, 1]),
             ("gdoor", 5, (0.005, 0.0225, 0), (-0.310, -0.2945, 0.165), qy, [0.9, 0.6, 0.1, 1])]
    cells = {}
    results = {}
    out_json = OUT / f"robot_ops{ARGS.tag}.json"
    prev = json.loads(out_json.read_text()) if out_json.exists() else {}
    for name in ops:
        fing = FINGERS.get(name, "stock")
        if fing not in cells:
            cells[fing] = Cell(M, parts, men, cache, base, fing, extra=extra)
            print(f"  model ({fing} fingers): {cells[fing].m.nbody} bodies, {cells[fing].m.ngeom} geoms; gap range {cells[fing].gap_range}", flush=True)
        cell = cells[fing]
        frames = op_frames(name, M, P, parts)
        t1 = time.time()
        rows, traj = run_op(cell, name, frames, record=ARGS.render)
        tq = torques(cell, rows, frames)
        free = [r for r in rows if not r["seat"]] or rows
        kmin = min(range(len(rows)), key=lambda k: rows[k]["clear_mm"] if not rows[k]["seat"] else 1e9)
        # exact re-measure at the tightest free frame
        cell.reset_bodies()
        for bn, Tw in (frames[kmin].get("bodies") or {}).items():
            cell.set_body(bn, Tw)
        cell.set_gap(frames[kmin].get("gap", 40.0))
        cell.fk(np.array(rows[kmin]["q"]))
        cell.clearance(held=frames[kmin].get("held", ()), ignore=frames[kmin].get("ignore", ()))
        try:
            ex = exact_pair(cell, parts, rows[kmin], frames[kmin])
        except Exception as e:  # noqa: BLE001
            ex = f"n/a ({e})"
        s = summarize(name, rows, frames, tq, ex)
        s["fingers"] = fing
        s["runtime_s"] = round(time.time() - t1, 1)
        s["steps"] = []
        for lab in dict.fromkeys(r["label"] for r in rows):
            rr = [r for r in rows if r["label"] == lab]
            w = min(rr, key=lambda r: r["clear_mm"])
            s["steps"].append(dict(step=lab, frames=len(rr), ik_ok=all(r["ik_mm"] < 1.0 and r["ik_deg"] < 0.5 for r in rr),
                                   min_clear_mm=w["clear_mm"], pair=w["pairs"][0][:2] if w["pairs"] else None, seat=rr[0]["seat"],
                                   reach_margin_mm=min(r["reach_margin_mm"] for r in rr),
                                   deg_range=[rr[0]["deg"], rr[-1]["deg"]] if rr[0]["deg"] is not None else None,
                                   ok_deg=[r["deg"] for r in rr if r["deg"] is not None and r["ik_mm"] < 1.0 and r["ik_deg"] < 0.5 and r["clear_mm"] >= 0.0]))
        results[name] = s
        print(f"  {name}: {len(rows)} frames, IK ok {s['ik_all']}, min clearance {s['min_clear_mm']} mm at '{s['min_clear_step']}' "
              f"({s['min_clear_pair']}), exact {ex}, torque ratio {tq['peak_ratio']} ({tq['worst_joint']}), {s['runtime_s']} s", flush=True)
        prev[name] = s
        out_json.write_text(json.dumps(dict(prev, _meta=dict(base_mm=base, menagerie_sha=MENAGERIE_SHA, cad=str(ARGS.cad),
                                                               module_mass_kg=P["module_mass"])), indent=1, default=float))
        if ARGS.render and traj:
            cams = {"plate_exchange": dict(lookat=(0.0, -0.2, 0.05), distance=1.25, azimuth=-118, elevation=-18),
                    "reservoir": dict(lookat=(-0.09, -0.25, 0.2), distance=1.3, azimuth=-120, elevation=-15),
                    "chamber_door_open": dict(lookat=(0.0, -0.3, 0.05), distance=1.5, azimuth=-110, elevation=-15)}
            cam = cams.get(name, dict(lookat=(0.0, -0.3, 0.05), distance=1.6, azimuth=-120, elevation=-18))
            gif = OUT / f"{name}.gif" if name in ("plate_exchange", "reservoir") else None
            pngs = [(kmin, OUT / f"{name}_tightest.png")]
            render_frames(cell, traj, gif, cam=cam, png=pngs)
            print(f"  rendered {name}", flush=True)
    print(f"done in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
