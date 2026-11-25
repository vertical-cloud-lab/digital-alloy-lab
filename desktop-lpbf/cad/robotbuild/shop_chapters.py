"""The robot shop's chapters of the robot-built video (round 7, issue #260, PR #266): 20-receiving, 30-machining-chamber,
31-machining-parts, 32-finishing, drawn with shop_scene.ShopScene from the planner's recordings
(analysis/shop/shop_clips.py -> /tmp/robotbuild/traj/shop_<clip>.pkl) plus the scripted parts: the person with the
pallet jack and with the vacuum tube lifter, the machines cutting (time-lapse with setup_plan.json's minutes), TIG.

Every robot motion shown is a recorded plan (FCL on meshes, 0.5 deg planning, 0.2 deg audit). The person's lifts are
scripted; the lifted load's path is checked against the machine with FCL here and written to
analysis/out/shop/shop_person.json.

Run (one chapter at a time, under the memory cap):
    OMP_NUM_THREADS=1 /tmp/capmem 3G xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python \
        desktop-lpbf/cad/robotbuild/shop_chapters.py 30 [--every N] [--still]
"""
from __future__ import annotations

import json
import math
import pathlib
import pickle
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shop_scene as SS  # noqa: E402  (puts analysis/robot and analysis/shop on the path)
from shop_scene import CM, E, S, Mst  # noqa: E402

FPS = CM.FPS
TRAJ = CM.TRAJ
LPBF = CM.LPBF
OUT = LPBF / "analysis" / "out" / "shop"
PLAN = json.loads((LPBF / "analysis" / "out" / "machining" / "setup_plan.json").read_text())
CH = SS.CHAMBER
EVERY = 1
STILL = False
SUMMARY = {}          # chapter -> clip -> dict(who, status, machine_h, robot_h, person_h, frames)


def load(clip):
    p = TRAJ / f"shop_{clip}.pkl"
    if not p.exists():
        return None
    with open(p, "rb") as fh:
        return pickle.load(fh)


def lerp(a, b, s):
    return a + (b - a) * s


def ease(s):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(s, 0.0), 1.0))


def cam_at(key, eye, focus, up=(0, 0, 1), pose=None):
    M = Mst(key, pose)
    e = (M @ np.r_[eye, 1.0])[:3]
    f = (M @ np.r_[focus, 1.0])[:3]
    return [tuple(e), tuple(f), up]


def orbit(cam, s, deg=8.0):
    """Swing the eye a few degrees about the focus (vertical axis) as s goes 0 -> 1."""
    e, f, up = np.array(cam[0]), np.array(cam[1]), cam[2]
    a = math.radians(deg * (s - 0.5))
    d = e - f
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1.0]])
    return [tuple(f + R @ d), tuple(f), up]


class Writer:
    """common.Chapter plus the counters: robot_h, person_h, machine_h added per frame from who and proc_s."""

    def __init__(self, name, title):
        self.ch = CM.Chapter(name, title)
        self.name = name
        self.n_in = 0
        self.tot = dict(machine_h=0.0, robot_h=0.0, person_h=0.0, cam_h=0.0, outsourced_d=0.0)
        self.clip = None

    def frame(self, scn, cam, caption, sub="", who=(), step="", status="", proc_s=1.0 / FPS, add=None, **kw):
        self.n_in += 1
        if (self.n_in - 1) % EVERY:
            return
        ps = proc_s * EVERY
        a = dict(add or {})
        who = list(who)
        if "robot A" in who or "robot B" in who:
            a.setdefault("robot_h", ps / 3600.0 * sum(1 for w in who if w.startswith("robot")))
        if "person" in who:
            a.setdefault("person_h", ps / 3600.0)
        if "machine" in who:
            a.setdefault("machine_h", ps / 3600.0)
        for k, v in a.items():
            self.tot[k] = self.tot.get(k, 0.0) + v
        img = scn.render(cam)
        self.ch.frame(img, caption, sub=sub, who=who, step=step, status=status, proc_s=ps, add=a, **kw)
        if self.clip is not None:
            s = SUMMARY.setdefault(self.name, {}).setdefault(self.clip, dict(who=set(), status=set(), machine_h=0.0,
                                                                              robot_h=0.0, person_h=0.0, frames=0, video_s=0.0))
            s["who"] |= set(who)
            if status:
                s["status"].add(status)
            for k in ("machine_h", "robot_h", "person_h"):
                s[k] += a.get(k, 0.0)
            s["frames"] += 1
            s["video_s"] += EVERY / FPS
        if STILL:
            raise StopIteration

    def close(self):
        self.ch.close()
        return self.ch.n


# ================================================================================================ the VF-4 with its groups
class VF4:
    """The VF-4 in the scene with its moving groups: the doors, the table (with the vise, the HRT210 and its platter, the
    fixtures and the part on them), the head (Z). Built at the reference state (doors open, table at X 0 / Y 0, Z home)."""

    def __init__(self, scn):
        self.scn = scn
        self.sc = scn.sc
        self.M = Mst("vf4")
        parts, meta = E.vf4(door=1.0, table_x=0.0, with_vise=True, vise_open=92.0, with_hrt=True)
        self.meta = meta
        self.dwi = E.VF4["door_w"] / 2 + 40.0
        groups = {}
        for n, p in parts.items():
            if n.startswith(("left door", "right door")):
                g = "vf4/door L" if n.startswith("left") else "vf4/door R"
            elif n == "HRT210 platter":
                g = "vf4/platter"
            elif n.startswith(("vise", "Kurt")):
                g = "vf4/vise"
            elif p.group == "table":
                g = "vf4/table"
            elif p.group == "head":
                g = "vf4/head"
            elif n.startswith(("front panel", "front sill", "left wall", "Haas red")):
                g = "vf4/front"
            else:
                g = "vf4/static"
            groups.setdefault(g, []).append((n, p))
        for g, lst in groups.items():
            by = {}
            for n, p in lst:
                m = p.mesh.transform(p.M if g == "vf4/platter" else p.M, inplace=False)
                by.setdefault((p.color, p.opacity), []).append(m)
            for i, ((c, op), ms) in enumerate(by.items()):
                self.sc.add(f"{g}/{i}", E.merge(ms), c, group=g, opacity=op)
        # the platter turns about the A axis inside the table group; the vise rides on the table
        self.axis = np.array(meta["hrt_axis"], float)            # station frame at table X 0
        self.sc.parent["vf4/platter"] = "vf4/table"
        self.sc.parent["vf4/vise"] = "vf4/table"
        self.sc.parent["vf4/fixture"] = "vf4/table"
        self.sc.parent["vf4/rotfix"] = "vf4/platter"
        self.sc.gmat["vf4/platter"] = np.eye(4)
        self.sc.gmat["vf4/vise"] = np.eye(4)
        self.sc.gmat["vf4/fixture"] = np.eye(4)
        self.sc.gmat["vf4/rotfix"] = np.eye(4)
        for g in ("vf4/static", "vf4/front"):
            self.sc.gmat[g] = self.M
        self.state = {}
        self.set(door=1.0, table_x=0.0, table_y=0.0, z=0.0, a=0.0, vise=False)

    def set(self, door=None, table_x=None, table_y=None, z=None, a=None, vise=None, front_alpha=None):
        st = self.state
        for k, v in dict(door=door, table_x=table_x, table_y=table_y, z=z, a=a, vise=vise, front_alpha=front_alpha).items():
            if v is not None:
                st[k] = v
        d = 1.0 - st["door"]
        self.sc.gmat["vf4/door L"] = self.M @ E.T((d * self.dwi, 0, 0))
        self.sc.gmat["vf4/door R"] = self.M @ E.T((-d * self.dwi, 0, 0))
        self.sc.gmat["vf4/table"] = self.M @ E.T((st["table_x"], st["table_y"], 0.0))
        self.sc.gmat["vf4/head"] = self.M @ E.T((0, 0, -st["z"]))
        self.sc.gmat["vf4/platter"] = E.about(E.Rx(st["a"]), self.axis)
        for n in self.sc.members("vf4/vise"):
            self.sc.alpha[n] = 1.0 if st["vise"] else 0.0
        fa = st.get("front_alpha", 1.0)
        for g in ("vf4/front", "vf4/door L", "vf4/door R"):
            for n in self.sc.members(g):
                self.sc.alpha[n] = fa

    def fixtures(self, fc, part=None, k=None, rots=None, a_deg=0.0):
        """Show freecad_cam.FIXTURES[fc] (and the part's cut state k) on the table at the reference table position."""
        import shop_clips as SCL
        for g in ("vf4/fixture", "vf4/rotfix"):
            for n in self.sc.members(g):
                self.sc.remove(n)
        if fc is None:
            return None
        parts, meta, P, M_setup, m = SCL.vf4_setup(fc, table_x=0.0, k_state=k or 0, part=part or "frame", rots=rots,
                                                   a_deg=0.0)
        rot = fc.startswith("frame_C")
        fx = SCL.fixture_parts(fc, M_setup)
        Minv = np.linalg.inv(self.M)
        g = "vf4/rotfix" if rot else "vf4/fixture"
        Mt = np.linalg.inv(E.T((0, 0, 0)))
        by = {}
        for n, p in fx.items():
            by.setdefault(p.color, []).append(p.mesh.transform(p.M, inplace=False))
        for i, (c, ms) in enumerate(by.items()):
            self.sc.add(f"{g}/{i}", E.merge(ms), c, group=g)
        # the fixture group's meshes are in the station frame at table X 0: the table group adds M; the platter's group
        # turns about the axis (also in the station frame), so both parents are expressed in the station frame
        self.sc.gmat[g] = np.eye(4)
        del Minv, Mt
        return P          # the part's pose in the station frame (table X 0), for the part group

    def part(self, name, mesh_spec, P, rot=False, color="#cfd4d9"):
        g = f"obj/{name}"
        m, c = self.scn.obj_mesh(mesh_spec)
        self.sc.add(g, m, color or c, group=g)
        self.sc.parent[g] = "vf4/rotfix" if rot else "vf4/fixture"
        self.sc.gmat[g] = np.asarray(P, float)
        self.scn.objs[name] = mesh_spec

    def tool_tip_world(self):
        """The spindle tool's tip (station frame) at the current Z."""
        ysp = E.VF4["spindle_y"]
        nose = E.VF4["table_z"] + E.VF4["nose_to_table"][1] - self.state["z"]
        return np.array([0.0, ysp, nose - 100.0 - 60.0])


# ================================================================================================ scripted person scenes
JIB_MAST = np.array([1250.0, -850.0])            # VF-4 station frame: the low jib's mast, in front of the right front
                                                 # panel, clear of a docked MiR; its boom swings in through the doors


def jib_parts_at(target_xy, hook_z):
    """The machine-side jib pointed at a target (station xy) with the foot face at hook_z: (parts, yaw, r)."""
    d = np.asarray(target_xy, float) - JIB_MAST
    yaw = math.degrees(math.atan2(d[1], d[0]))
    r = float(np.linalg.norm(d))
    parts, m = E.jib_lifter(yaw=yaw, r=r, hook_z=hook_z, J=E.MACHINE_JIB)
    return parts, m


def draw_jib(scn, parts, M_station):
    """(Re)draw the jib's pieces (cheap boxes and cylinders) in the station frame."""
    Mm = M_station @ E.T((JIB_MAST[0], JIB_MAST[1], 0.0))
    for n, p in parts.items():
        scn.sc.add(f"jib/{n}", p.mesh.transform(Mm @ p.M, inplace=False), p.color, group="jib")
    scn.sc.gmat["jib"] = np.eye(4)


class Jib:
    """The low machine-side jib with the JumboFlex, drawn once and moved by matrices: the boom turns about the mast, the
    trolley runs along it, the tube (a unit cylinder) stretches from the trolley to the lifter's head, and the head (the
    handle and a top foot, or a side foot on a tilt unit) sits at the pose it is given."""

    def __init__(self, scn, M_station):
        self.scn, self.sc = scn, scn.sc
        J = E.MACHINE_JIB
        self.J = J
        self.Mstation = M_station
        self.mode = "top"
        self.Mm = M_station @ E.T((JIB_MAST[0], JIB_MAST[1], 0.0))
        parts, m = E.jib_lifter(yaw=0.0, r=0.0, hook_z=0.0, J=J)
        for n in ("jib base plate", "jib mast", "vacuum blower", "vacuum hose up the mast"):
            p = parts[n]
            self.sc.add(f"jib/{n}", p.mesh.transform(self.Mm @ p.M, inplace=False), p.color, group="jib/static")
        self.sc.gmat["jib/static"] = np.eye(4)
        p = parts["jib boom (enclosed track)"]
        self.sc.add("jib/boom", p.mesh, p.color, group="jib/boom")
        ub = J["under_boom"]
        self.sc.add("jib/trolley", E.box(-90, 90, -80, 80, ub - 60, ub), "#3b4148", group="jib/trolley")
        self.sc.add("jib/tube", E.cyl((0, 0, 0), (0, 0, 1.0), 80.0, res=32), "#3b4148", group="jib/tube")
        handle = E.merge([E.box(-160, 160, -60, 60, 120, 260), E.cyl((-120, 0, 200), (-420, 0, 330), 18.0),
                          E.box(-450, -410, -130, 130, 320, 360)])          # the operating handle's bar, 260 mm wide
        foot_top = E.merge([E.box(-200, 200, -130, 130, 30, 120), E.box(-190, 190, -120, 120, 0, 30)])
        self.sc.add("jib/head", E.merge([handle, foot_top]), "#2f5f8a", group="jib/head")
        # the side foot on a 90 deg tilt unit: the pad's face in the head frame's x-z plane, facing -y... built so that
        # the pad's face is the head frame's origin and its normal is +y (into the part)
        side = E.merge([E.box(-160, 160, -40, 0, -70, 70), E.box(-40, 40, -140, -40, -30, 30),
                        E.box(-40, 40, -140, -100, 30, 260), E.cyl((0, -120, 260), (300, 0, 520), 18.0),
                        E.box(280, 320, -130, 130, 500, 540)])
        self.sc.add("jib/side head", side, "#2f5f8a", group="jib/side head")
        self.show(False)

    def show(self, on, mode="top"):
        """on: in use (mode's head shown); off: parked, the boom swung along the front panel to the right, the head up."""
        for n in self.sc.actors:
            if n.startswith("jib/"):
                a = 1.0
                if n == "jib/head" and (mode != "top" and on):
                    a = 0.0
                if n == "jib/side head" and (mode != "side" or not on):
                    a = 0.0
                self.sc.alpha[n] = a
        self.mode = mode if on else "top"
        if not on:
            self.set(E.T((JIB_MAST[0] + 1400.0, JIB_MAST[1] - 200.0, 1150.0), E.Rz(180.0)), 1410.0)

    def yaw_at(self, p_station):
        """The boom's yaw (deg, station frame) pointing at a station point."""
        d = np.asarray(p_station[:2], float) - JIB_MAST
        return math.degrees(math.atan2(d[1], d[0]))

    def set(self, M_head, attach_z):
        """M_head: the head's pose in the station frame (top mode: the foot's face centre, its x axis along the boom;
        side mode: the side pad's face centre); attach_z: where the tube meets the head (mm above the floor). Returns the
        handle's grip point (world) and the boom's yaw."""
        Mw = self.Mstation @ M_head
        p = np.linalg.inv(self.Mm) @ np.r_[Mw[:3, 3], 1.0]
        yaw = math.degrees(math.atan2(p[1], p[0]))
        r = float(np.hypot(p[0], p[1]))
        Mb = self.Mm @ E.T((0, 0, 0), E.Rz(yaw))
        self.sc.gmat["jib/boom"] = Mb
        self.sc.gmat["jib/trolley"] = Mb @ E.T((r, 0, 0))
        L = max(self.J["under_boom"] - 60.0 - attach_z, 10.0)
        self.sc.gmat["jib/tube"] = Mb @ E.T((r, 0, attach_z)) @ np.diag([1.0, 1.0, L, 1.0])
        self.sc.gmat["jib/head"] = Mw
        self.sc.gmat["jib/side head"] = Mw
        hp = Mw @ (np.r_[-430.0, 0.0, 340.0, 1.0] if self.mode == "top" else np.r_[300.0, 0.0, 520.0, 1.0])
        return hp[:3], yaw


def load_path_check(items, load_vf, poses):
    """FCL: the lifted load (and nothing else) along its scripted path against the machine's items: the smallest
    distance (mm) and the first contact, if any."""
    import cell as C
    W = C.Group([C.Body(n, *vf, kind="cell") for n, vf, c in items])
    b = C.Body("load", *load_vf, kind="held")
    best = (math.inf, None)
    hit = None
    for k, M in enumerate(poses):
        b.place(M)
        d, x, y = C.group_distance(C.Group([b]), W, margin=200.0)
        if d < best[0]:
            best = (d, y.name if y is not None else None)
        if d <= 0.0 and hit is None:
            hit = dict(sample=k, body=y.name if y is not None else None)
    return dict(clear_mm=round(best[0], 1) if best[0] < math.inf else None, nearest=best[1], contact=hit,
                samples=len(poses))


PERSON_RESULTS = {}


def person_lift(w, scn, vf4, name, load_name, load_spec, P_from, P_to, kg, caption, sub, step, fc_to=None,
                M_obj_from=None, tilt=None, n_frames=None, check_items=None, cam=None, rot_to=False, flip=False):
    """The person guides the low jib's tube lifter: the foot comes down on the load at P_from (station frame), lifts it,
    swings it in through the doors and sets it at P_to. The load's pose follows the foot. Returns the FCL check."""
    from scipy.spatial.transform import Rotation, Slerp
    M = Mst("vf4")
    jib = scn.jib
    p = scn.person
    p.show(1.0)
    m, _ = scn.obj_mesh(load_spec)
    v = np.asarray(m.points)
    side = flip
    jib.show(True, "side" if side else "top")

    def grip_point(P):
        """Station point where the head meets the load: the top face's centre (top), or the -x end face's centre (side:
        the turning unit turns the load about x, so the pad stays on that face)."""
        vw = (v @ P[:3, :3].T) + P[:3, 3]
        c = (vw.min(0) + vw.max(0)) / 2
        return np.array([c[0], c[1], vw[:, 2].max()]) if not side else np.array([vw[:, 0].min(), c[1], c[2]])

    g_from, g_to = grip_point(P_from), grip_point(P_to)
    lift_z = max(g_from[2], g_to[2]) + 130.0
    door_y = -260.0                                         # in front of the doors, while it swings round
    keys = [(0.00, g_from + [0, 0, 260.0]), (0.12, g_from), (0.20, g_from), (0.34, np.r_[g_from[:2], lift_z]),
            (0.58, np.array([g_to[0] - 250.0, door_y, lift_z])), (0.80, np.r_[g_to[:2], lift_z]), (0.90, g_to),
            (0.95, g_to), (1.00, g_to + [0, 0, 220.0])]
    hold_s = (0.20, 0.90)
    n = n_frames or int(24 * FPS)
    poses = []

    # The person stays on the aisle side of the pad (station -y), 950 mm from the pad's centre, facing it; the head is
    # turned so its operating handle (430 mm from the pad, 340 mm up) points at the person: hands on the handle bar,
    # 520 mm in front of the person, never under the boom (checked below with FCL).
    D_PERSON = 950.0
    R_head = E.Rz(90.0)                                     # head -x (the handle) -> station -y (the person)
    R_from = P_from[:3, :3]
    R_to = P_to[:3, :3]
    sl = Slerp([0.0, 1.0], Rotation.from_matrix([R_from, R_to]))
    import cell as C
    W_static = None
    if check_items is not None:
        W_static = [C.Body(nm, *vf, kind="cell") for nm, vf, c in check_items]
    person_hits, person_min = [], math.inf
    for i in range(n):
        s = i / (n - 1)
        for (s0, p0), (s1, p1) in zip(keys[:-1], keys[1:]):
            if s0 <= s <= s1:
                u = ease((s - s0) / max(s1 - s0, 1e-9))
                g = p0 + (p1 - p0) * u
                break
        held = hold_s[0] <= s <= hold_s[1]
        turn = ease((s - 0.34) / (0.80 - 0.34))             # the turning/tilting unit works during the carry
        R_load = sl(turn).as_matrix() if held else (R_from if s < hold_s[0] else R_to)
        R_rel = R_load @ R_from.T if s <= hold_s[1] else R_to @ R_from.T    # the head turns with the load it holds
        if side:
            Mh = E.T(tuple(g), R_rel @ E.Rz(-90.0))         # side pad on the -x face, facing +x, turning with the load
            attach = g[2] + 380.0
        else:
            Mh = E.T(tuple(g), R_head)
            attach = g[2] + 260.0
        hp, yaw = jib.set(Mh, attach)
        if held:
            # the load hangs on the head: its grip point at the head, turned by the unit
            c_off = (P_from[:3, :3].T @ (g_from - P_from[:3, 3]))       # the grip point in the load's own frame
            P = E.T(tuple(g - R_load @ c_off), R_load)
            poses.append(M @ P)
        else:
            P = P_from if s < hold_s[0] else P_to
        scn.set_obj(load_name, M @ P, load_spec)
        # the person: on the aisle side of the pad, outside the enclosure's front (station y <= -380), facing +y
        st_xy = np.array([g[0] + (60.0 if side else 0.0), min(g[1] - D_PERSON, -380.0)])
        pw = (M @ np.r_[st_xy[0], st_xy[1], 0.0, 1.0])[:3]
        reach = float(np.hypot(hp[0] - pw[0], hp[1] - pw[1]))
        lean = float(np.clip((reach - 470.0) / 10.0, 0.0, 32.0))
        p.set(x=pw[0], y=pw[1], hd=0.0, amp=0.0, hands={"l": tuple(hp + [-95, 0, 0]), "r": tuple(hp + [95, 0, 0])},
              look=tuple(hp + [0, 0, -250]), lean=lean)
        if W_static is not None and i % 12 == 0:           # the posed person against the machine, the lifter and the load
            scn.sc.apply()
            body = [C.Body(f"person/{k}", P_, F_, kind="arm") for k, (P_, F_) in p.posed().items()]
            lifter = []
            for nm in ("jib/head", "jib/side head", "jib/tube", "jib/boom"):
                if nm in scn.sc.actors and scn.sc.alpha.get(nm, 0) > 0.02:
                    a = scn.sc.actors[nm]
                    mesh = a.GetMapper().GetInput()
                    pts = np.asarray(SS.pv.wrap(mesh).points, float)
                    Mg = scn.sc.world(scn.sc.group_of[nm])
                    fv = SS.pv.wrap(mesh).faces.reshape(-1, 4)[:, 1:].astype(np.int32)
                    lifter.append(C.Body(nm, pts @ Mg[:3, :3].T + Mg[:3, 3], fv, kind="cell"))
            lv = (np.asarray(m.points, float), m.faces.reshape(-1, 4)[:, 1:].astype(np.int32))
            lb = C.Body("load", *lv, kind="cell")
            lb.place(M @ P)
            Wd = C.Group(W_static + lifter + [lb])
            hits = C.group_hits(C.Group(body), Wd)
            for x_, y_ in hits:                             # the hands on the handle bar touch it on purpose
                if "glove" in x_.name and y_.name in ("jib/head", "jib/side head"):
                    continue
                person_hits.append((i, x_.name, y_.name))
            d_, _, _ = C.group_distance(C.Group(body), Wd, margin=300.0)
            person_min = min(person_min, d_)
        w.frame(scn, cam if cam is not None else cam_at("vf4", *CAM_PERSON), caption,
                sub=sub, who=["person"], step=step, status="person")
    res = dict(kg=kg, frames=n, person_contacts=len(person_hits), person_first=person_hits[:3],
               person_min_clear_mm=round(person_min, 1) if person_min < math.inf else None)
    if check_items is not None and poses:
        vf = (np.asarray(m.points, float), m.faces.reshape(-1, 4)[:, 1:].astype(np.int32))
        res.update(load_path_check(check_items, vf, poses[::3]))
    PERSON_RESULTS[name] = res
    print("person lift", name, res, flush=True)
    jib.show(False)
    p.show(0.0)
    return res


CAM_PERSON = ((-2300.0, -3500.0, 3500.0), (-250.0, -250.0, 900.0))   # three-quarter view from the front left, above
                                                                      # (the jib's mast stands at the right)


# ================================================================================================ machining time-lapse
def op_minutes(setup_id, n_ops, removed):
    """Spread a setup's minutes (setup_plan.json, its ops' sum) over the cut states by removed volume^0.5."""
    for part in ("frame", "floor"):
        for s in PLAN[part]["setups"]:
            if s["id"] == setup_id:
                tot = sum((o.get("minutes") or 0.0) for o in s["ops"])
                break
        else:
            continue
        break
    else:
        tot = 10.0
    w = np.sqrt(np.maximum(np.asarray(removed, float), 0.05))
    return tot, list(tot * w / w.sum())


def cut_states(w, scn, vf4, rows, part_name, P_ref, rot, setup_id, minutes_extra=0.0, seconds=12.0, cap="", sub0="",
               a_of=None):
    """The VF-4 cutting a setup: doors shut, the table under the spindle, the tool tracing each op's region while the
    machine clock runs (time-lapse), the part switching to each op's cut state; then doors open."""
    tot, mins = op_minutes(setup_id, len(rows), [r.get("removed_cm3", 1.0) for r in rows])
    if minutes_extra:
        mins = [minutes_extra if r["key"].startswith("TR") else m for r, m in zip(rows, mins)]
        tot = sum(mins)
    cam_in = cam_at("vf4", *CAM_VF4_IN)
    n_total = int(seconds * FPS)
    # doors shut (auto door: ~3 s)
    for i in range(18):
        vf4.set(door=1.0 - ease((i + 1) / 18))
        w.frame(scn, cam_at("vf4", *CAM_VF4_ARM), cap, sub="Auto door shuts; cycle start",
                who=["machine"], step=setup_id, status="pass", proc_s=1.0 / FPS)
    vf4.set(front_alpha=0.0)
    ty = E.VF4["spindle_y"] - (E.VF4["table_front_y"] + E.VF4["table_W"] / 2)
    for i in range(12):
        u = ease((i + 1) / 12)
        vf4.set(table_y=ty * u, z=300.0 * u)
        w.frame(scn, cam_in, cap, sub=sub0, who=["machine"], step=setup_id, status="pass", proc_s=0.5)
    for r, mn in zip(rows, mins):
        n = max(10, int(round(n_total * mn / max(tot, 1e-6))))
        mesh_after = dict(kind="state", part=r["part"], k=r["k"])
        if a_of is not None and r.get("index_deg") is not None and r["index_deg"] != vf4.state["a"]:
            a0, a1 = vf4.state["a"], float(r["index_deg"])
            for i in range(10):
                vf4.set(a=a0 + (a1 - a0) * ease((i + 1) / 10), z=300.0)
                w.frame(scn, cam_in, cap, sub=f"A axis to {a1:.0f} deg (Z home first)", who=["machine"], step=setup_id,
                        status="pass", proc_s=1.0)
        for i in range(n):
            s = (i + 0.5) / n
            ang = 2 * math.pi * s * 2.0
            dx, dy = 150.0 * math.cos(ang), 105.0 * math.sin(ang)
            vf4.set(table_x=-dx, table_y=ty - dy, z=360.0 + 25.0 * math.sin(6 * ang))
            if i == n // 2:
                scn.objs.pop(part_name, None)
                vf4.part(part_name, mesh_after, P_ref, rot=rot)
            w.frame(scn, cam_in, cap, sub=f"{r['label'][:110]} | {mn:.1f} min", who=["machine"], step=setup_id, status="pass",
                    proc_s=mn * 60.0 / n)
    for i in range(12):
        u = ease((i + 1) / 12)
        vf4.set(table_x=0.0, table_y=ty * (1 - u), z=300.0 * (1 - u))
        w.frame(scn, cam_in, cap, sub="Done: Z home, table to the load position", who=["machine"], step=setup_id,
                status="pass", proc_s=0.5)
    vf4.set(front_alpha=1.0)
    for i in range(18):
        vf4.set(door=ease((i + 1) / 18))
        w.frame(scn, cam_at("vf4", *CAM_VF4_ARM), cap, sub="Auto door opens", who=["machine"],
                step=setup_id, status="pass", proc_s=1.0 / FPS)
    return tot


# ================================================================================================ clip playback
def play(w, scn, name, cam, sub=None, caption=None, orbit_deg=6.0, hide=(), tool_override=None, obj_color=None, rev=False,
         cut=None):
    """Play a recorded clip: arms, MiRs, objects per frame; the clip's own meta unless overridden."""
    clip = load(name)
    if clip is None:
        print("missing clip", name)
        return None
    w.clip = name
    frames = clip["frames"][::-1] if rev else clip["frames"]
    keys = set()
    for fr in frames:
        keys |= set(fr["arms"])
    for k in ("A", "B"):
        scn.show_arm(k, k in keys)
    n = len(frames)
    keep = range(n)
    skipped_s = 0.0
    if cut is not None:                  # (s kept at the start, s kept at the end): the middle is cut, its time is not
        a_, b_ = int(cut[0] * FPS), int(cut[1] * FPS)
        if a_ + b_ < n:
            keep = list(range(a_)) + list(range(n - b_, n))
            skipped_s = (n - a_ - b_) / FPS
    for j, i in enumerate(keep):
        fr = frames[i]
        for k, a in fr["arms"].items():
            scn.set_arm(k, a["q"], a["close"], a["base"], tool_override or a["tool"])
        for k, m in fr["mirs"].items():
            scn.set_mir(k, m["M"], m["arm_dx"])
        for o, M in fr["objs"].items():
            if o in hide:
                continue
            scn.set_obj(o, M, clip["objects"].get(o), color=(obj_color or {}).get(o))
        meta = dict(fr["meta"])
        c = caption or meta.pop("caption", "")
        meta.pop("caption", None)
        if sub is not None:
            meta["sub"] = sub
        meta.pop("proc_s", None)
        meta.pop("add", None)
        ps = 1.0 / FPS
        if skipped_s and cut is not None and j == int(cut[0] * FPS):
            ps += skipped_s              # the cut's real time goes on the first frame after it
            meta["sub"] = f"(cut: {skipped_s:.0f} s of the same moves on the other clamps) " + meta.get("sub", "")
        w.frame(scn, orbit(cam, i / max(n - 1, 1), orbit_deg), c, proc_s=ps, **meta)
    w.clip = None
    return clip


# ================================================================================================ the scene
class Shop(SS.ShopScene):
    def __init__(self):
        super().__init__()
        self.add_arm("A")
        self.add_arm("B")
        self.show_arm("A", False)
        self.show_arm("B", False)
        self.add_person("op")
        self.person.show(0.0)

    def show_arm(self, key, on):
        for n in self.sc.actors:
            if n.startswith((f"arm{key}/", f"mir{key}/")):
                if on:
                    if n.startswith(f"mir{key}/") and self.arms[key].get("mir_dx") is not None:
                        self.sc.alpha[n] = 1.0 if f"/{self.arms[key]['mir_dx']:.0f}/" in n else 0.0
                    elif not n.startswith(f"mir{key}/"):
                        self.sc.alpha[n] = 1.0
                else:
                    self.sc.alpha[n] = 0.0
        if on:
            self.set_tool(key, self.arms[key]["tool"])

    def clear_objs(self, keep=()):
        for o in list(self.objs):
            if o not in keep:
                self.hide_obj(o)


def add_long_table(scn, x0=2600.0, x1=6500.0):
    """common.LONG_TABLE in the shop frame, with kit_table.py's slots near the kitting shot drawn as boxes (their bboxes
    from kit_slots.json), so arm A sets the floor plate among the other parts."""
    import shop_clips as SCL
    LT = CM.LONG_TABLE
    dy = -float(CM.SHOP_IN_HALL[1])
    top = E.box(LT["x0"], LT["x1"], LT["y0"] + dy, LT["y1"] + dy, LT["top"] - LT["t"], LT["top"])
    legs = E.merge([E.box(x - 30, x + 30, y - 30, y + 30, 0, LT["top"] - LT["t"])
                    for x in np.arange(LT["x0"] + 100, LT["x1"], 1500.0) for y in (LT["y0"] + dy + 60, LT["y1"] + dy - 60)])
    scn.sc.add("long table top", top, "#d8d2c4", group="static")
    scn.sc.add("long table legs", legs, "#6b7078", group="static")
    ks = SCL.kit_slots()
    if ks:
        items = [E.box(b[0], b[1], b[2] + dy, b[3] + dy, b[4], b[5]) for s_ in ks["slots"] for b in [s_["bbox"]]
                 if x0 <= b[0] <= x1 and s_["key"] != "C00a" and s_.get("support") != "pallet" and b[5] - b[4] > 2]
        if items:
            scn.sc.add("kit items", E.merge(items), "#aab2ba", group="static")


def context_vf4(scn):
    parts, meta = E.vf4(door=0.0, table_x=0.0, with_vise=False, with_hrt=True)
    scn.add_parts("vf4_ctx", parts, Mst("vf4"))


# ================================================================================================ chapters
def chapter_20():
    w = Writer("20-receiving", "Receiving and unpacking")
    scn = Shop()
    context_vf4(scn)
    st = Mst("receiving")
    rp = load("recv_tape")
    # the receiving area: lift table and box, three heavy crates on a pallet coming in
    import shop_clips as SCL
    scn.add_parts("recv", SCL.recv_parts(0.0), st)
    crates = [("chamber blank 13 x 9.5 x 5.5 in. 6061 (30.0 kg)", (360, 270, 180)), ("plate bundle (58 kg)", (720, 400, 110)),
              ("IPG laser crate (52 kg)", (760, 680, 380))]
    pal = E.pallet()
    M_pal0 = st @ E.T((-1900.0, 3600.0, 0.0))
    M_pal1 = st @ E.T((-1900.0, 1100.0, 0.0))
    jack, jm = E.pallet_jack()
    p = scn.person
    for i in range(int(6 * FPS)):
        w.frame(scn, orbit([(1500.0, -2500.0, 7200.0), (8000.0, 6000.0, 600.0), (0, 0, 1)], i / (6 * FPS), 12.0),
                "The robot shop: two UR12e arms on MiR250s, a VF-4 with a 4th axis, a lathe, a bandsaw",
                sub="north row: VF-4, ST-10 lathe, deburr and wash, measuring, bench; south row: receiving, stock, saw, "
                    "tools; a hypothetical layout (robot-shop.md)", who=[], step="", status="")
    for i in range(int(14 * FPS)):
        s = ease(i / (14 * FPS - 1))
        Mp = M_pal0 @ E.T((0, -2500.0 * s, 0)) @ np.linalg.inv(M_pal0) @ M_pal0
        scn.set_obj("pallet", Mp, dict(kind="vf", v=E.fcl_items(pal)[0][1][0], f=E.fcl_items(pal)[0][1][1], color=E.C["wood"]))
        z = 144.0
        x = -460.0
        for j, (nm, (L, W_, H)) in enumerate(crates):
            scn.set_obj(f"crate {j}", Mp @ E.T((x + L / 2, -150.0 + j * 0.0, z)) if j < 2 else Mp @ E.T((200.0, 0.0, z)),
                        dict(kind="box", b=(-L / 2, L / 2, -W_ / 2, W_ / 2, 0, H), color=E.C["box"]))
            if j == 0:
                x += L + 20.0
        Mj = Mp @ E.T((0.0, 610.0, 0.0)) @ E.T((0, 0, 0), E.Rz(-90.0))
        for k2, pp in jack.items():
            scn.sc.add(f"jack/{k2}", pp.mesh, pp.color, group="jack") if i == 0 else None
        scn.sc.gmat["jack"] = Mj @ E.T((-1250.0, 0, 0))
        hx = (Mj @ E.T((-1250.0, 0, 0)) @ np.r_[jm["handle"][0], 0, jm["handle"][2], 1.0])[:3]
        p.show(1.0)
        p.set(x=hx[0], y=hx[1] - 420.0, hd=180.0, amp=1.0 if 0.05 < s < 0.95 else 0.0,
              phase=2 * math.pi * 2500.0 * s / people_stride(), hands={"l": tuple(hx + [-80, 0, 0]), "r": tuple(hx + [80, 0, 0])},
              look=tuple(hx + [0, -1500, -200]), lean=8.0)
        w.frame(scn, cam_at("receiving", (2600, -2600, 2600), (-1600, 1800, 600)), "Three crates over two arms' 22.4 kg: "
                "the person brings them in with a pallet jack", sub="the chamber blank (30.0 kg), the plate bundle (58 kg), "
                "the laser (52 kg); a 48 x 40 in. pallet, a 27 x 48 in. manual jack", who=["person"], step="receiving",
                status="person")
    p.show(0.0)
    for k2 in list(scn.sc.actors):
        if k2.startswith("jack/"):
            scn.sc.alpha[k2] = 1.0
    cam = cam_at("receiving", (-1700, -1500, 2000), (0, 420, 900))
    play(w, scn, "recv_tape", cam)
    play(w, scn, "recv_unbox", cam_at("receiving", (1500, -1700, 2100), (0, 300, 900)))
    del rp
    return w.close()


def people_stride():
    return SS.people.Person.STRIDE


CAM_VF4_ARM = ((1850.0, -1900.0, 2050.0), (-60.0, 250.0, 1050.0))     # right front, ~2 m up, looking down ~22 deg
CAM_VF4_IN = ((560.0, 160.0, 1650.0), (-60.0, 720.0, 1020.0))         # inside the enclosure, for the cutting


def rest_on(spec, scn, M_base, z_top, R=np.eye(3)):
    """The pose that sets a mesh (turned by R) on a surface at z_top, centred over M_base's origin."""
    m, _ = scn.obj_mesh(spec)
    v = np.asarray(m.points) @ R.T
    c = (v.min(0) + v.max(0)) / 2
    return M_base @ E.T((-c[0], -c[1], z_top - v[:, 2].min()), R)


def chapter_30():
    w = Writer("30-machining-chamber", "Machining the chamber: the VF-4 and its 4th axis")
    scn = Shop()
    vf4 = VF4(scn)
    st = Mst("vf4")
    scn.jib = Jib(scn, st)
    import shop_plan as SP
    rows = json.loads((CH / "states.json").read_text())["rows"]
    rT = [r for r in rows if r.get("part") == "frameT" and "k" in r]
    rF = [r for r in rows if r.get("part") == "floor" and "k" in r]
    check = SP.shop_world("vf4", E.vf4(door=1.0, table_x=-100.0)[0])
    cam_arm = cam_at("vf4", *CAM_VF4_ARM)
    # ---- F-S1: the person loads the 30 kg blank with the tube lifter onto the risers
    P1 = vf4.fixtures("frame_B", "frameT", 0, rots=[["x", 180]])
    vf4.set(table_x=-100.0, door=1.0)
    M_tab = E.T((-100.0, 0, 0))
    pal_M = E.T((-700.0, -1450.0, 0.0))
    pal = E.fcl_items(E.pallet())[0][1]
    scn.set_obj("pallet", st @ pal_M, dict(kind="vf", v=pal[0], f=pal[1], color=E.C["wood"]))
    blank_spec = dict(kind="state", part="frameT", k=0)
    P_from = rest_on(blank_spec, scn, pal_M, 144.0, E.Rx(180.0))
    P_to = M_tab @ P1
    person_lift(w, scn, vf4, "F-S1 load", "frame part", blank_spec, P_from, P_to, 30.05,
                "A person loads the 30 kg blank onto the risers with a vacuum tube lifter",
                "13 x 9.5 x 5.5 in. 6061, 30.0 kg (34.7 kg at 15 in.): over two arms' 22.4 kg, and robots on two bases "
                "shouldn't share a load over ~10 kg (Edison r7); Schmalz JumboFlex 50 on a low jib", "F-S1",
                check_items=check)
    scn.hide_obj("frame part")
    vf4.part("frame part", blank_spec, P1)
    # ---- arm A tightens the four edge clamps
    play(w, scn, "vf4_clamps", cam_arm, hide=("frame part",))
    scn.show_arm("A", False)
    # ---- F-S1 cutting: the trepan's lower half + the plan's F-S1 ops
    s1 = [r for r in rT if r.get("setup") == "F-S1"]
    cut_states(w, scn, vf4, s1, "frame part", P1, False, "F-S1", minutes_extra=7.0, seconds=14.0,
               cap="F-S1 on the VF-4: trepan the core's lower half, face the bottom, the lower outside and opening, holes",
               sub0="time-lapse at setup_plan.json's minutes (vendor feeds, 60 %); the 7 min trepan is our estimate")
    # ---- arm A loosens the clamps (the same plan, reversed)
    play(w, scn, "vf4_clamps", cam_arm, hide=("frame part",), rev=True, cut=(7.0, 2.0),
         caption="Arm A loosens the clamps (the same planned path, run back)")
    scn.show_arm("A", False)
    # ---- the flip onto the dummy-floor plate: the person (22.8 kg)
    k1 = s1[-1]["k"]
    spec1 = dict(kind="state", part="frameT", k=k1)
    P_from2 = M_tab @ P1
    P2 = vf4.fixtures("frame_A", "frameT", k1, rots=[])
    P_to2 = M_tab @ P2
    person_lift(w, scn, vf4, "F-S1 to F-S2 flip", "frame part", spec1, P_from2, P_to2, 22.8,
                "The person turns the part over onto the dummy-floor plate for F-S2",
                "about 22.8 kg with the core still attached: the lifter's turning unit, a pad on the end face; then the "
                "person fits the 18 M4 screws from below", "F-S2", flip=True, check_items=check, n_frames=int(22 * FPS))
    scn.hide_obj("frame part")
    vf4.part("frame part", spec1, P2)
    s2 = [r for r in rT if r.get("setup") == "F-S2"]
    cut_states(w, scn, vf4, s2, "frame part", P2, False, "F-S2", minutes_extra=7.0, seconds=14.0,
               cap="F-S2: the trepan's upper half frees the core; face the top, the upper outside and opening, lid gland",
               sub0="time-lapse at setup_plan.json's minutes; the lid gland's 1/8 in. tool is most of it")
    # ---- the freed core (13 kg): the person lifts it out with the lifter onto the pallet
    core_spec = dict(kind="file", path=str(CH / "frameT_core.vtp"))
    vf4.part("core", core_spec, P2)
    k2 = s2[-1]["k"]
    spec2 = dict(kind="state", part="frameT", k=k2)
    scn.objs.pop("frame part", None)
    vf4.part("frame part", spec2, P2)
    person_lift(w, scn, vf4, "core out", "core", core_spec, M_tab @ P2, rest_on(core_spec, scn, pal_M, 144.0), 13.0,
                "The person lifts the freed core out: 13 kg of reusable 6061",
                "235.9 x 145.9 x 139.7 mm; over ~10 kg, so the lifter rather than two arms on two bases (Edison r7)",
                "F-S2", check_items=check, n_frames=int(18 * FPS))
    # ---- F-S3: the frame + plate unit onto the HRT210 (10 kg, turned 90 deg: the person), A indexing
    s3 = [r for r in rT if r.get("setup") == "F-S3"]
    P3 = vf4.fixtures("frame_C0", "frameT", k2, rots=[["y", 90], ["x", -90]])
    tab3 = E.T((40.0, 0, 0))
    person_lift(w, scn, vf4, "F-S3 onto the rotary", "frame part", spec2, M_tab @ P2, tab3 @ P3, 10.0,
                "The person sets the frame and its fixture plate on the 4th axis",
                "frame 5.3 kg + MIC-6 plate 4.7 kg, turned 90 deg onto the HRT210's platter with the lifter's tilt unit; "
                "4 bolts through the opening", "F-S3", check_items=check, n_frames=int(18 * FPS))
    scn.hide_obj("frame part")
    vf4.set(table_x=40.0)
    vf4.part("frame part", spec2, P3, rot=True)
    cut_states(w, scn, vf4, s3, "frame part", P3, True, "F-S3", seconds=14.0, a_of=True,
               cap="F-S3 on the HRT210: the four walls in one clamping, A 0 / 90 / 180 / 270",
               sub0="time-lapse at setup_plan.json's minutes; Z home, unclamp, index, clamp as in frame_C_haas.nc")
    vf4.set(a=0.0)
    # ---- the floor plate: arm A (VGP20) loads P-S1, then the top side is cut
    scn.hide_obj("frame part")
    scn.hide_obj("core")
    PF = vf4.fixtures("floor_A", "floor", 0, rots=[])
    vf4.set(table_x=-100.0)
    play(w, scn, "vf4_floor_load", cam_arm, hide=("floor part",))
    scn.hide_obj("floor part")
    vf4.part("floor part", dict(kind="state", part="floor", k=0), PF)
    scn.show_arm("A", False)
    fP1 = [r for r in rF if r.get("setup") == "P-S1"]
    cut_states(w, scn, vf4, fP1, "floor part", PF, False, "P-S1", seconds=10.0,
               cap="P-S1: the floor plate's top: face, pad, gland, port, slots, dowels",
               sub0="time-lapse at setup_plan.json's minutes")
    return w.close()


def chapter_31():
    w = Writer("31-machining-parts", "Machining the other parts: vise, lathe, saw")
    scn = Shop()
    vf4 = VF4(scn)
    vf4.set(table_x=-E.TABLE_LAYOUT["vise"], vise=True)
    scn.drop_context("lathe")
    scn.add_parts("lathe", E.st10(door=1.0, jaw_open=6.0)[0], Mst("lathe"))
    scn.drop_context("saw")
    scn.add_parts("saw", E.s20a(head=1.0)[0], Mst("saw"))
    play(w, scn, "vf4_vise_part", cam_at("vf4", (-1300, -2300, 2200), (0, 450, 1050)))
    scn.show_arm("A", False)
    # the bracket cut in the vise (time-lapse, the vise class's setup time from setup_plan: a representative part)
    for i in range(int(6 * FPS)):
        s = i / (6 * FPS)
        vf4.set(door=max(0.0, 1.0 - 3 * s), z=300.0 + 40 * math.sin(12 * s), table_y=200.0 * min(1.0, 3 * s))
        w.frame(scn, cam_at("vf4", (-520.0, 120.0, 1720.0), (60.0, 760.0, 1010.0)), "The bracket cut in the vise",
                sub="time-lapse: a vise part's setup, about 20 min of cutting (setup_plan.json's class)", who=["machine"],
                step="vise class", status="pass", proc_s=20 * 60.0 / (6 * FPS))
    vf4.set(door=1.0, z=0.0, table_y=0.0)
    play(w, scn, "saw_bar", cam_at("saw", (-2400, -2500, 2200), (-1300, 450, 900)))
    scn.show_arm("B", False)
    play(w, scn, "lathe_slug", cam_at("lathe", (-1600, -2300, 2000), (100, 300, 1000)))
    lb = load("lathe_big")
    if lb is not None and (lb.get("result") or {}).get("ok", False):
        scn.add_parts("lathe", E.st10(door=1.0, jaw_open=33.0, jaw_deg=30.0)[0], Mst("lathe"))   # jaws opened, oriented
        play(w, scn, "lathe_big", cam_at("lathe", (-1600, -2300, 2000), (100, 300, 1000)))
    scn.show_arm("A", False)
    # the rest of the parts: the machine clock runs through setup_plan's other setups by motion class
    tot = PLAN["totals"]
    n = int(10 * FPS)
    hours = 287.3
    for i in range(n):
        w.frame(scn, orbit([(8000.0, -1500.0, 7800.0), (8200.0, 6000.0, 600.0), (0, 0, 1)], i / n, 10.0),
                "The other 54 parts, by motion class: each setup reuses its class's planned motion",
                sub=f"setup_plan.json: {tot.get('setups_with_4th_axis', 67)} setups with the 4th axis; vise, lathe, plate, "
                    "rotary and saw classes", who=["machine", "robot A", "robot B"], step="all parts", status="pass",
                proc_s=hours * 3600.0 / n * 0.0 + 1.0 / FPS)
    return w.close()


def chapter_32():
    w = Writer("32-finishing", "Finishing: welding, honing, deburring, washing, measuring, kitting")
    scn = Shop()
    context_vf4(scn)
    scn.drop_context("wash")
    scn.add_parts("wash", E.wash_deburr()[0], Mst("wash"))
    scn.drop_context("measure")
    scn.add_parts("measure", E.granite_station()[0], Mst("measure"))
    # ---- TIG: the person welds the build module's body (316L tube to its flanges)
    p = scn.person
    p.show(1.0)
    stt = Mst("tig")
    tz = 36 * E.INCH
    body = E.merge([E.tube((0, 0, 0), (0, 0, 180), 38.0, 25.4), E.tube((0, 0, 0), (0, 0, 12), 60.0, 25.4)])
    scn.sc.add("tig/body", body, "#b8bec4", group="tig/body")
    scn.sc.gmat["tig/body"] = stt @ E.T((0, 450, tz), E.Rx(90.0))
    for i in range(int(10 * FPS)):
        s = i / (10 * FPS)
        a = 2 * math.pi * s
        tip = (stt @ np.r_[60 * math.cos(a), 450 + 0.0, tz + 60 * math.sin(a) + 60, 1.0])[:3]
        p.set(x=stt[0, 3], y=stt[1, 3] - 350.0, hd=0.0, amp=0.0, hands={"r": tuple(tip + [0, -80, 60]), "l": tuple(tip + [-150, -60, 0])},
              look=tuple(tip), lean=18.0)
        glow = E.cyl((0, 0, 0), (0, 0, 2), 9.0 + 4 * math.sin(40 * a))
        scn.sc.add("tig/arc", glow.transform(E.T(tuple(tip)), inplace=False), "#bfe3ff", group="static")
        w.frame(scn, cam_at("tig", (-1500, -1700, 1900), (0, 400, 950)), "A person TIG-welds the build module's body",
                sub="316L tube to its flanges: welding stays with a person (fixtures, fit-up, a certified welder)",
                who=["person"], step="weld", status="person", proc_s=90 * 60.0 / (10 * FPS))
    scn.sc.alpha["tig/arc"] = 0.0
    p.show(0.0)
    # ---- honing goes out
    for i in range(int(4 * FPS)):
        w.frame(scn, cam_at("tig", (-1500, -1700, 1900), (0, 400, 950)), "Honing the 50.80 mm bore is sent out",
                sub="outsourced: a hone shop, about 10 working days (estimate) for one tube", who=["outsourced"],
                step="hone", status="pass", proc_s=1.0 / FPS, add=dict(outsourced_d=10.0 / (4 * FPS)))
    play(w, scn, "deburr", cam_at("wash", (1600, -1800, 2000), (450, 340, 1050)))
    scn.show_arm("A", False)
    play(w, scn, "wash", cam_at("wash", (-200, -2000, 2200), (-500, 340, 950)), hide=())
    scn.show_arm("B", False)
    mc = load("measure")
    if mc is not None and not (mc.get("result") or {}).get("ok", False):
        play(w, scn, "measure", cam_at("measure", (-1500, -1800, 2100), (0, 250, 950)),
             caption="Arm A can't carry a part onto the granite: no collision-free path",
             sub="RRT-Connect from two docking positions: the plate's top is 114 mm above the arm's base, so the upper arm "
                 "sweeps through it; fix: a lower inspection table or a robot-loadable gauge. The person sets it down")
    else:
        play(w, scn, "measure", cam_at("measure", (-1300, -1500, 1900), (0, 250, 950)))
    scn.show_arm("A", False)
    # the person reads the bore gauge
    p.show(1.0)
    stm = Mst("measure")
    for i in range(int(8 * FPS)):
        s = i / (8 * FPS)
        g = (stm @ np.r_[-20.0, 145.0, 36 * E.INCH + 40, 1.0])[:3]
        p.set(x=g[0] + 150.0, y=g[1] - 650.0, hd=0.0, amp=0.0, hands={"r": tuple(g + [0, -40, 140 + 10 * math.sin(6 * s)]),
                                                                    "l": tuple(g + [-120, -60, 60])},
              look=tuple(g), lean=22.0)
        w.frame(scn, cam_at("measure", (-1300, -1500, 1900), (0, 250, 950)), "A person gauges the port and the seal faces",
                sub="dial bore gauge (35-60 mm, 0.01 mm) and height gauge: the arms place parts but can't read them",
                who=["person"], step="measure", status="person", proc_s=4 * 60.0 / (8 * FPS))
    p.show(0.0)
    add_long_table(scn)
    play(w, scn, "kit", [(5300.0, 10250.0, 2350.0), (3650.0, 11650.0, 900.0), (0, 0, 1)])
    return w.close()


CHAPTERS = {"20": chapter_20, "30": chapter_30, "31": chapter_31, "32": chapter_32}


def main(argv):
    global EVERY, STILL
    argv = list(argv)
    if "--every" in argv:
        i = argv.index("--every")
        EVERY = int(argv[i + 1])
        del argv[i:i + 2]
    STILL = "--still" in argv
    args = [a for a in argv if not a.startswith("--")]
    t0 = time.time()
    for k in args or list(CHAPTERS):
        t1 = time.time()
        try:
            n = CHAPTERS[k]()
        except StopIteration:
            n = 1
        print(f"chapter {k}: {n} frames in {time.time() - t1:.0f} s", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    pj = OUT / "shop_person.json"
    old = json.loads(pj.read_text()) if pj.exists() else {}
    old.update(PERSON_RESULTS)
    pj.write_text(json.dumps(old, indent=1, default=str))
    sj = CM.DATA / "shop_frames.json"
    CM.DATA.mkdir(parents=True, exist_ok=True)
    prev = json.loads(sj.read_text()) if sj.exists() else {}
    for ch, clips in SUMMARY.items():
        prev[ch] = {c: dict(who=sorted(v["who"]), status=sorted(v["status"]), machine_h=round(v["machine_h"], 3),
                            robot_h=round(v["robot_h"], 4), person_h=round(v["person_h"], 4), frames=v["frames"],
                            video_s=round(v["video_s"], 1)) for c, v in clips.items()}
    sj.write_text(json.dumps(prev, indent=1))
    print(f"done in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
