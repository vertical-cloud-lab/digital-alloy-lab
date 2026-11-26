"""The robot shop's chapters of the robot-built video (rounds 7 and 8, issue #260, PR #266): 20-receiving,
30-machining-chamber, 31-machining-parts, 32-finishing, drawn with shop_scene.ShopScene from the planner's recordings
(analysis/shop/shop_clips.py -> /tmp/robotbuild/traj/shop_<clip>.pkl) plus the scripted parts: the person with the
pallet jack, two people lifting, the machines cutting, TIG.

Round 8 (Sterling on round 7: "moonwalk, motion sickness, collisions and interference, dummy tool paths instead of real
ones"; "I don't think we have a vacuum chuck lift. Probably just a two person job for that part."):
* chapter 30 cuts the chamber with the posted programs (analysis/out/machining/gcode/, freecad_cam.py): gcode_sim.py
  parses and times them and cuts them out of the programs' stock; every cutting frame puts the tool where the program
  is at that frame's time (the table carrying the part in X and Y, the head in Z, the A index with Z home), the stock
  as the program has cut it so far, and the last ~0.2 m of path. Each frame's program and line go into the frame's
  sub and analysis/out/videoqa/gcode_frames.json (gcode_sim.py --verify-frames checks them);
* the jib and vacuum tube lifter are gone: the loads go in by two people (Crew, team_lift), with the mass and a
  two-person guideline in the caption; nobody moves without walking (gait phase 2 pi per Person.STRIDE walked);
* fixed cameras: no orbit or sway anywhere; cuts between shots; the overview first, then the working view.

Every robot motion shown is a recorded plan (FCL on meshes, 0.5 deg planning, 0.2 deg audit); no clip moves a MiR (all
parked). The two-person lifts are scripted; the load's path is checked against the machine with FCL here, and the hands'
gap to their grip points recorded, in analysis/out/shop/shop_person.json.

Run (one chapter at a time, under the memory cap; ROBOTBUILD_AUDIT=1 records every drawn frame for scene_audit):
    ROBOTBUILD_AUDIT=1 OMP_NUM_THREADS=1 /tmp/capmem 6G xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python \
        desktop-lpbf/cad/robotbuild/shop_chapters.py 30 [--every N] [--still]
"""
from __future__ import annotations

import json
import math
import os
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


class Writer:
    """common.Chapter plus the counters: robot_h, person_h, machine_h added per frame from who and proc_s."""

    def __init__(self, name, title):
        name = name + os.environ.get("SHOP_PREVIEW_SUFFIX", "")   # previews into their own folder (an auditor watches
        self.ch = CM.Chapter(name, title)                          # the real ones for their done files)
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
            if n == "tool":          # drawn per T number below (freecad_cam.json's tools), shown by show_tool()
                continue
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
        # the posted programs' tools (freecad_cam.json "tools": diameter, stick-out below the holder), on the head
        import gcode_sim as GS_
        ysp = E.VF4["spindle_y"]
        nose0 = E.VF4["table_z"] + E.VF4["nose_to_table"][1]
        for t, d in GS_.tools().items():
            L, r = d["length"], d["d"] / 2
            body = E.cyl((0, ysp, nose0 - 100 - L), (0, ysp, nose0 - 100), r, res=32)
            if d["shape"] == "drill":
                body = E.merge([E.cyl((0, ysp, nose0 - 100 - L + 0.6 * r), (0, ysp, nose0 - 100), r, res=24),
                                SS.pv.Cone(center=(0, ysp, nose0 - 100 - L + 0.3 * r), direction=(0, 0, 1),
                                           height=0.6 * r, radius=r, resolution=24).triangulate()])
            col = "#4a5058" if t == 1 else "#d9b44a"
            self.sc.add(f"vf4/tool/T{t}", body, col, group="vf4/tool")     # station frame, riding on the head
        self.sc.parent["vf4/tool"] = "vf4/head"
        self.sc.gmat["vf4/tool"] = np.eye(4)
        self.state = {}
        self.set(door=1.0, table_x=0.0, table_y=0.0, z=0.0, a=0.0, vise=False)
        self.show_tool(2)

    def show_tool(self, T):
        """The tool in the spindle: T (freecad_cam.json's numbering), the others in the carousel (not drawn)."""
        for n in self.sc.members("vf4/tool"):
            self.sc.alpha[n] = 1.0 if n == f"vf4/tool/T{T}" else 0.0
        self.state["tool"] = T

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
        self.M_setup = M_setup           # the CAM setup frame (the posted program's work frame) in the station frame
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


# ================================================================================================ two people lift
# Sterling (2026-11-26): "I don't think we have a vacuum chuck lift. Probably just a two person job for that part." The
# round-7 jib and tube lifter are gone: every load a person handled is a two-person lift now.
NIOSH_KG = 23.0              # the revised NIOSH lifting equation's load constant: one person, ideal lift (NIOSH 94-110)
TEAM_FACTOR = 2.0 / 3.0      # HSE L23 (guidance to the UK Manual Handling Operations Regulations): a team of two can
TEAM_KG = TEAM_FACTOR * 2 * NIOSH_KG   # handle about 2/3 of the sum of their individual capabilities -> 30.7 kg
LIFT_RULE = "two-person guideline 2/3 x (23 + 23) = 30.7 kg (NIOSH load constant, HSE L23 team rule)"
CART = dict(x=0.0, y=-640.0, w=340.0, d=600.0, h=900.0)   # station frame: a shop cart in front of the doors (est.)
Y_BODY_MAX = -150.0          # the people stay outside the enclosure's front (station y 0): body origin at most here
HD = (-20.0, 20.0)           # each person turned 20 deg in towards the load's end it holds
CAM_OUT = ((-750.0, -1800.0, 3150.0), (0.0, 330.0, 1000.0))       # the working view over the door (fixed)
CAM_WIDE = ((-4300.0, -6200.0, 4300.0), (300.0, 600.0, 900.0))     # the overview of the VF-4 station (fixed)


def load_path_check(items, load_vf, poses):
    """FCL: the lifted load (and nothing else) along its path against the machine's items: the smallest distance (mm)
    and the first contact, if any."""
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


def _wrap(a):
    return (a + 180.0) % 360.0 - 180.0


class Crew:
    """Two people (shop_scene's person and a second people.Person). Nobody translates without walking: the gait phase
    advances 2 pi per people.Person.STRIDE mm walked (backwards when the body moves against its heading), amp > 0
    while moving; a turn on the spot is small steps (the feet travel ~0.25 m per radian); otherwise they stand."""

    def __init__(self, scn):
        self.scn = scn
        self.p = [scn.person, scn.person2]
        self.st = [dict(x=0.0, y=0.0, hd=0.0, phase=0.0, amp=0.0, lean=0.0, placed=False) for _ in self.p]
        self.log = []                                         # (who, moved_mm, phase_step, amp)

    def show(self, a):
        for p in self.p:
            p.show(a)

    def place(self, i, x, y, hd=0.0):
        """Between shots only: where person i stands when the next shot opens."""
        self.st[i].update(x=x, y=y, hd=hd, amp=0.0, lean=0.0, placed=True)
        self.p[i].set(x=x, y=y, hd=hd, amp=0.0, phase=self.st[i]["phase"], hands={"l": None, "r": None}, lean=0.0,
                      look=None)

    def step(self, i, x, y, hd, hands=None, look=None, lean=0.0):
        s = self.st[i]
        dx, dy = x - s["x"], y - s["y"]
        d = math.hypot(dx, dy)
        dh = abs(_wrap(hd - s["hd"]))
        fwd = (-math.sin(math.radians(s["hd"])), math.cos(math.radians(s["hd"])))
        sign = 1.0 if dx * fwd[0] + dy * fwd[1] >= -1e-9 else -1.0
        moved = d + 250.0 * math.radians(dh)
        dph = sign * 2 * math.pi * moved / SS.people.Person.STRIDE
        s["phase"] += dph
        amp = 1.0 if d > 3.0 else (0.45 if dh > 0.3 else (0.25 if d > 0.3 else 0.0))
        s.update(x=x, y=y, hd=hd, amp=amp, lean=lean)
        p = self.p[i]
        p.set(x=x, y=y, hd=hd, amp=amp, phase=s["phase"], hands=hands or {"l": None, "r": None}, look=look, lean=lean)
        if hands:
            # people.py grounds the shoes after the arm IK, so a walking body's bob (30-45 mm) moves the hands off
            # their targets: aim again, less the error of the first pose (the bob doesn't depend on the arms)
            fix = {}
            for sd, tgt in hands.items():
                if tgt is not None:
                    e = p.hand_point(sd) - np.asarray(tgt, float)
                    fix[sd] = tuple(np.asarray(tgt, float) - e) if np.linalg.norm(e) > 3.0 else tgt
            if any(fix[sd] is not hands[sd] for sd in fix):
                p.set(hands=fix)
        self.log.append((i, round(d, 2), round(dph, 4), amp))

    def walk_to(self, w, targets, cam, caption, sub, step, speed=900.0, face=HD):
        """Both turn towards their targets [(x, y)] (small steps), walk there (heading along the way), then turn on
        the spot to `face` (deg)."""
        starts = [(s["x"], s["y"]) for s in self.st]
        dist = [math.hypot(tx - sx, ty - sy) for (tx, ty), (sx, sy) in zip(targets, starts)]
        n = max(int(math.ceil(max(dist) / (speed / FPS))), 1)
        heads = [math.degrees(math.atan2(-(tx - sx), ty - sy)) if d_ > 1 else s["hd"]
                 for (tx, ty), (sx, sy), d_, s in zip(targets, starts, dist, self.st)]

        def turn(goal):
            h0 = [s["hd"] for s in self.st]
            nt = max(max(int(abs(_wrap(g_ - h_)) / 12.0) for g_, h_ in zip(goal, h0)), 0)
            for k in range(nt):
                u = (k + 1) / nt
                for i in range(2):
                    self.step(i, self.st[i]["x"], self.st[i]["y"], h0[i] + _wrap(goal[i] - h0[i]) * u)
                w.frame(self.scn, cam, caption, sub=sub, who=["person"], step=step, status="person")

        turn(heads)
        for k in range(n):
            u = (k + 1) / n
            for i in range(2):
                sx, sy = starts[i]
                tx, ty = targets[i]
                self.step(i, sx + (tx - sx) * u, sy + (ty - sy) * u, heads[i])
            w.frame(self.scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
        turn(list(face))
        for i in range(2):
            self.step(i, self.st[i]["x"], self.st[i]["y"], face[i])


PERSON_RESULTS = {}


def stance_xy(i, mid):
    """Person i's body origin (station x, y) and lean for hands around `mid` (station): turned HD[i] in towards its
    end of the load, the hands 60 mm to its inner side and 380 mm ahead; never past Y_BODY_MAX (outside the machine),
    leaning to reach."""
    a = math.radians(HD[i])
    fwd = np.array([-math.sin(a), math.cos(a)])
    right = np.array([math.cos(a), math.sin(a)])
    inner = right if i == 0 else -right
    b = np.asarray(mid, float)[:2] - 60.0 * inner - 380.0 * fwd
    if b[1] > Y_BODY_MAX:
        b = b - fwd * (b[1] - Y_BODY_MAX) / fwd[1]
    reach = float((np.asarray(mid, float)[:2] - b) @ fwd)
    # people.Person's arms are 520 mm shoulder to palm: probed, a lean of 40 deg reaches 600 mm ahead at 0.95-1.1 m,
    # 55 deg 760 mm (gaps under 15 mm); so the lean grows with the reach and with how low the hands are
    z = float(np.asarray(mid, float)[2]) if len(mid) > 2 else 1000.0
    lean = float(np.clip(36.0 + 0.09 * (reach - 380.0) + 0.08 * (1000.0 - z), 32.0, 56.0))
    return b[0], b[1], lean


def end_hands(m, P, side, fz=0.45, fy=(0.15, 0.42)):
    """Two hand points (load frame) on the load's end face that faces station -x (side -1, the left person) or +x
    (side +1), at fz of its height, at fy of its depth from the face nearest the people (station -y), at pose P."""
    v = np.asarray(m.points, float)
    lo, hi = v.min(0), v.max(0)
    R = P[:3, :3]
    sx = R.T @ np.array([float(side), 0.0, 0.0])         # station +-x in the load's frame
    ax = int(np.argmax(np.abs(sx)))
    sy = R.T @ np.array([0.0, -1.0, 0.0])                 # station -y (the people) in the load's frame
    ay = int(np.argmax(np.abs(sy)))
    sz = R.T @ np.array([0.0, 0.0, 1.0])
    az = int(np.argmax(np.abs(sz)))
    pts = []
    for f in fy:
        q = (lo + hi) / 2
        q = q.copy()
        q[ax] = (hi[ax] + 4.0) if sx[ax] > 0 else (lo[ax] - 4.0)
        q[ay] = (hi[ay] - f * (hi[ay] - lo[ay])) if sy[ay] > 0 else (lo[ay] + f * (hi[ay] - lo[ay]))
        q[az] = (lo[az] + fz * (hi[az] - lo[az])) if sz[az] > 0 else (hi[az] - fz * (hi[az] - lo[az]))
        pts.append(q)
    return pts


def team_lift(w, scn, crew, name, spec, P_from, P_to, kg, caption, sub, step, cam=None, hand_pts=None, lift_mm=70.0,
              check_items=None, n_move=None, walk_from=None, hide_after=True):
    """Two people lift a load from P_from to P_to (station-frame poses of the load's own frame) together: they walk
    to their ends of it, put both hands on it, lift, carry it (walking forward, leaning to reach), set it down and let
    go. The load turns from P_from's to P_to's orientation during the carry (slerp). hand_pts: {person: (left hand,
    right hand)} in the load's frame (default: the end faces at P_from, see end_hands)."""
    from scipy.spatial.transform import Rotation, Slerp
    M = Mst("vf4")
    cam = cam or cam_at("vf4", *CAM_OUT)
    m, _ = scn.obj_mesh(spec)
    if hand_pts is None:
        hand_pts = {0: end_hands(m, P_from, -1), 1: end_hands(m, P_from, +1)}
    v = np.asarray(m.points, float)
    c_loc = (v.min(0) + v.max(0)) / 2
    R0, R1 = P_from[:3, :3], P_to[:3, :3]
    sl = Slerp([0.0, 1.0], Rotation.from_matrix([R0, R1]))
    c0 = P_from[:3, :3] @ c_loc + P_from[:3, 3]
    c1 = P_to[:3, :3] @ c_loc + P_to[:3, 3]
    carry_z = max(c0[2], c1[2]) + lift_mm
    n_move = n_move or int(max(4.5, np.linalg.norm(c1[:2] - c0[:2]) / 240.0) * FPS)
    keys = [(0.0, c0), (0.14, np.r_[c0[:2], carry_z]), (0.84, np.r_[c1[:2], carry_z]), (1.0, c1)]

    def centre(s):
        for (s0, p0), (s1, p1) in zip(keys[:-1], keys[1:]):
            if s0 <= s <= s1:
                return p0 + (p1 - p0) * ease((s - s0) / max(s1 - s0, 1e-9))
        return keys[-1][1]

    def pose(s):
        R = sl(ease((s - 0.14) / 0.70)).as_matrix() if s > 0.14 else R0
        c = centre(s)
        return E.T(tuple(c - R @ c_loc), R)

    def hands_world(P):
        return [tuple(P[:3, :3] @ q + P[:3, 3] for q in hand_pts[i]) for i in range(2)]

    def stance(i, hw):
        return stance_xy(i, (np.asarray(hw[0]) + np.asarray(hw[1])) / 2)

    def world(p):
        return (M @ np.r_[p, 1.0])[:3]

    crew.show(1.0)
    scn.set_obj(name, M @ P_from, spec)
    hw0 = hands_world(P_from)
    st0 = [stance(i, hw0[i]) for i in range(2)]
    if walk_from is not None:
        for i in range(2):
            if not crew.st[i]["placed"]:
                pw = world(np.array([walk_from[i][0], walk_from[i][1], 0.0]))
                crew.place(i, pw[0], pw[1], 0.0)
    crew.walk_to(w, [tuple(world(np.array([s_[0], s_[1], 0.0]))[:2]) for s_ in st0], cam, caption, sub, step)
    poses = []
    n_reach, n_rel = 8, 8
    total = n_reach + n_move + n_rel
    gaps, gap_at = [], []
    for k in range(total):
        if k < n_reach:
            s, u = 0.0, ease((k + 1) / n_reach)
        elif k < n_reach + n_move:
            s, u = (k - n_reach + 1) / n_move, 1.0
        else:
            s, u = 1.0, 1.0 - ease((k - n_reach - n_move + 1) / n_rel)
        P = pose(s)
        if 0.0 < s < 1.0:
            poses.append(M @ P)
        scn.set_obj(name, M @ P, spec)
        hw = hands_world(P)
        for i in range(2):
            x, y, lean = stance(i, hw[i])
            pw = world(np.array([x, y, 0.0]))
            p = crew.p[i]
            tgt = {}
            for side, q in zip(("l", "r"), hw[i]):
                qw = world(q)
                rest = p.rest_hand(side)
                tgt[side] = tuple(qw) if u >= 1.0 else tuple(rest + (qw - rest) * u)
            crew.step(i, pw[0], pw[1], HD[i], hands=tgt, look=tuple(world((hw[i][0] + hw[i][1]) / 2)),
                      lean=lean * (u if (k < n_reach or k >= n_reach + n_move) else 1.0))
            if u >= 1.0:
                for side, q in zip(("l", "r"), hw[i]):
                    gaps.append(float(np.linalg.norm(p.hand_point(side) - world(q))))
                    gap_at.append((round(gaps[-1], 1), k, round(s, 3), i, side, round(lean, 1)))
        w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
    res = dict(kg=round(kg, 2), team_guideline_kg=round(TEAM_KG, 1), under_guideline=bool(kg <= TEAM_KG),
               frames=total, hand_gap_mm_max=round(max(gaps), 1) if gaps else None,
               hand_gap_mm_p95=round(float(np.percentile(gaps, 95)), 1) if gaps else None,
               worst=sorted(gap_at, reverse=True)[:4])
    if check_items is not None and poses:
        vf = (np.asarray(m.points, float), m.faces.reshape(-1, 4)[:, 1:].astype(np.int32))
        res.update(load_path_check(check_items, vf, poses[::2]))
    key = f"{step}: {caption}"
    while key in PERSON_RESULTS:
        key += " (again)"
    res["caption"] = caption
    res["sub"] = sub
    PERSON_RESULTS[key] = res
    print("team lift", key, res, flush=True)
    return res


# ================================================================================================ the cut, from the G-code
import gcode_sim as GS  # noqa: E402

GFRAMES = []                 # one row per drawn cutting frame: chapter frame, program, line, time, position
GMIN = {}                    # chapter -> the programs' minutes it ran (the machine clock)


class Stock:
    """A part's in-process stock from the posted programs (gcode_sim): occupancy on a 1 mm grid in the part frame."""

    def __init__(self, part, res=1.0):
        self.part = part
        self.g = GS.make_grid(part, res)
        self.occ = GS.stock0(part, self.g)
        self.n = 0

    def kg(self, occ=None):
        return float((self.occ if occ is None else occ).sum()) * self.g.h ** 3 / 1e6 * 2.70

    def mesh(self, occ=None):
        m = GS.occ_mesh(self.occ if occ is None else occ, self.g)
        return m.compute_normals(split_vertices=False, consistent_normals=False, auto_orient_normals=False)

    def spec(self, extra_mesh=None, occ=None):
        """Save the current stock (plus an optional extra mesh, e.g. the plate it sits on) and return a file spec."""
        self.n += 1
        path = pathlib.Path("/tmp/robotbuild/cache/shop/gcode") / f"{self.part}_{self.n}.vtp"
        path.parent.mkdir(parents=True, exist_ok=True)
        m = self.mesh(occ)
        if extra_mesh is not None:
            m = E.merge([m, extra_mesh])
        m.save(str(path))
        return dict(kind="file", path=str(path))


def tool_len(T):
    return GS.tools()[T]["length"]


def vf4_for(Q, rot_s, g, T):
    """The VF-4's axes for the work point g (setup frame) of a part whose station pose at table X 0 / Y 0 is Q: the
    table carries the part in X and Y (under the spindle), the head moves Z (the tool tip at the point)."""
    m = rot_s.T @ np.asarray(g, float)
    q = Q[:3, :3] @ m + Q[:3, 3]
    tx = -q[0]
    ty = E.VF4["spindle_y"] - q[1]
    z = E.VF4["table_z"] + E.VF4["nose_to_table"][1] - 100.0 - tool_len(T) - q[2]
    return tx, ty, z


def cut_program(w, scn, vf4, stock, names, part_obj, Q_of, cam, cap, seconds, step, a_end=None, remesh=3):
    """Run the posted programs `names` (one setup, or the four A indexes of F-S3) on the VF-4: the cutter at the
    program's position every frame (time-lapse at the real minutes), the table and head moving as a VMC's do, the
    stock cut by the program (gcode_sim, re-meshed every `remesh` frames), and the last ~0.2 m of path drawn.
    Q_of(a): the part's station pose at table 0 for A index a (or None). Returns the minutes run."""
    sc = scn.sc
    g_obj = f"obj/{part_obj}"
    g_trail = f"obj/{part_obj} trail"
    parent = sc.parent.get(g_obj)
    P_part = sc.gmat[g_obj]
    tot_min = 0.0
    tool_now = None
    for name, secs in zip(names, seconds):
        prog = GS.Program(name)
        a = prog.a_deg
        Q = Q_of(a)
        ax = Q[:3, :3] @ prog.rot.T @ np.array([0.0, 0.0, 1.0])   # the tool axis must be the station's vertical
        if ax[2] < 0.999:
            raise RuntimeError(f"{name}: tool axis {ax} in the station frame is not vertical")
        if a is not None and abs(vf4.state["a"] - a) > 0.1:      # the index move: Z home (G53 G0 Z0), then A
            z0 = vf4.state["z"]
            for i in range(4):
                vf4.set(z=z0 * (1 - ease((i + 1) / 4)))
                w.frame(scn, cam, cap, sub=f"{prog.src} line {prog.index_lines['home']}: G53 G00 Z0. (Z home "
                        f"before the index)", who=["machine"], step=step, status="pass",
                        proc_s=max(z0, 1.0) / (25400.0 / 60.0) / 4)
            a0 = vf4.state["a"]
            for i in range(8):
                vf4.set(a=a0 + (a - a0) * ease((i + 1) / 8))
                w.frame(scn, cam, cap, sub=f"{prog.src} line {prog.index_lines['a']}: M11, G00 A{a}., M10 (unclamp, "
                        f"index, clamp: ~3 s, our estimate)", who=["machine"], step=step, status="pass",
                        proc_s=3.0 / 8)
        cut = GS.Cutter(prog, stock.g, stock.occ)
        n = max(int(round(secs * FPS)), 12)
        factor = prog.total_s / (n / FPS)
        for k in range(n):
            t = (k + 1) / n * prog.total_s
            cut.advance(t)
            pos, i = prog.at(t)
            T = int(prog.tool[i])
            if T != tool_now:
                vf4.show_tool(T)
                tool_now = T
            tx, ty, z = vf4_for(Q, prog.rot, pos, T)
            vf4.set(table_x=tx, table_y=ty, z=z)
            if k % remesh == 0 or k == n - 1:
                sc.set_mesh(g_obj, stock.mesh(cut.occupancy()))
            tr = prog.trail(t)
            if tr is not None:
                pts = tr @ prog.rot          # setup -> part frame (the rows of rot are the setup axes)
                tube = SS.pv.lines_from_points(pts).tube(radius=0.9, n_sides=8)
                if g_trail not in sc.actors:
                    sc.add(g_trail, tube, "#ff7a1a", group=g_trail, specular=0.0)
                    if parent is not None:
                        sc.parent[g_trail] = parent
                else:
                    sc.set_mesh(g_trail, tube)
                sc.gmat[g_trail] = P_part
                sc.alpha[g_trail] = 1.0
            elif g_trail in sc.actors:
                sc.alpha[g_trail] = 0.0
            ln = int(prog.line[i])
            label = prog.ops[int(prog.op[i])]
            GFRAMES.append(dict(chapter=w.name, chapter_frame=w.n_in, program=prog.src, setup=name, line=ln,
                                t_s=round(t, 2), work_xyz=[round(float(c), 3) for c in pos], tool=T, op=label,
                                table_xy=[round(tx, 1), round(ty, 1)], head_z=round(z, 1),
                                in_travel=bool(-635.0 <= tx <= 635.0 and -5.0 <= ty <= 513.0 and -1.0 <= z <= 636.0)))
            w.frame(scn, cam, cap, sub=f"{prog.src} line {ln}: T{T}, {label[:58]} | {factor:.0f}x time-lapse of "
                    f"{prog.total_s / 60:.1f} min", who=["machine"], step=step, status="pass",
                    proc_s=prog.total_s / n)
        cut.finish()
        occ, freed = GS.drop_free(cut.occupancy())
        stock.occ = occ
        sc.set_mesh(g_obj, stock.mesh())
        if g_trail in sc.actors:
            sc.alpha[g_trail] = 0.0
        tot_min += prog.total_s / 60.0
        if freed:
            print(name, "slugs dropped (cm3)", [round(v * stock.g.h ** 3 / 1000, 1) for v in freed], flush=True)
    z0 = vf4.state["z"]
    for i in range(8):
        vf4.set(z=z0 * (1 - ease((i + 1) / 8)))
        w.frame(scn, cam, cap, sub="Program end: Z home (rapid)", who=["machine"], step=step, status="pass",
                proc_s=max(z0, 1.0) / (25400.0 / 60.0) / 8)
    if a_end is not None and abs(vf4.state["a"] - a_end) > 0.1:
        a0 = vf4.state["a"]
        for i in range(8):
            vf4.set(a=a0 + (a_end - a0) * ease((i + 1) / 8))
            w.frame(scn, cam, cap, sub=f"{GS.HAAS}: M11, G00 A0., M10, M30 (the program's end; ~3 s, our estimate)",
                    who=["machine"], step=step, status="pass", proc_s=3.0 / 8)
    return tot_min


# ================================================================================================ clip playback
def play(w, scn, name, cam, sub=None, caption=None, hide=(), tool_override=None, obj_color=None, rev=False,
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
        w.frame(scn, cam, c, proc_s=ps, **meta)          # a fixed camera: no orbit, no sway (lesson 5)
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
        self.person2 = None

    def add_person2(self):
        """A second person (two-person lifts), in an olive T-shirt so the two can be told apart."""
        self.person2 = SS.people.Person(self.sc, "op2", coat=SS.people._rgb("#6b7f4e"))
        self.person2.show(0.0)
        return self.person2

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
        w.frame(scn, [(1500.0, -2500.0, 7200.0), (8000.0, 6000.0, 600.0), (0, 0, 1)],
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
        # round 8: the person pushes the jack, facing the way it goes (world +y; round 7 faced -y and slid backwards
        # with a forward gait); the gait phase follows the distance walked, amp > 0 whenever the body moves
        ds = 2500.0 * (s - (ease((i - 1) / (14 * FPS - 1)) if i else 0.0))
        p.set(x=hx[0], y=hx[1] - 420.0, hd=0.0, amp=min(1.0, 0.3 + ds / 40.0) if ds > 0.3 else 0.0,
              phase=2 * math.pi * 2500.0 * s / people_stride(), hands={"l": tuple(hx + [-80, 0, 0]), "r": tuple(hx + [80, 0, 0])},
              look=tuple(hx + [0, 1500, -400]), lean=8.0)
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


CAM_VF4_ARM = ((900.0, -2600.0, 2400.0), (0.0, 300.0, 1050.0))        # front, a little right, ~2.4 m up: the MiR in the foreground, the jib out of the shot
CAM_VF4_IN = ((560.0, 160.0, 1650.0), (-60.0, 720.0, 1020.0))         # inside the enclosure, for the cutting


def rest_on(spec, scn, M_base, z_top, R=np.eye(3)):
    """The pose that sets a mesh (turned by R) on a surface at z_top, centred over M_base's origin."""
    m, _ = scn.obj_mesh(spec)
    v = np.asarray(m.points) @ R.T
    c = (v.min(0) + v.max(0)) / 2
    return M_base @ E.T((-c[0], -c[1], z_top - v[:, 2].min()), R)


CAM_IN_FLAT = ((880.0, -260.0, 1820.0), (-40.0, 760.0, 1050.0))    # through the (hidden) front: the table under the spindle
CAM_IN_ROT = ((760.0, -240.0, 1860.0), (-120.0, 760.0, 1130.0))    # the same, for the rotary setup


def plate_mesh():
    """The dummy-floor plate (1 in. MIC-6, 312 x 222, flush with the frame) in the frame's model frame: under its
    bottom face (z -3.9), as freecad_cam.FIXTURES has it."""
    return E.box(-156.0, 156.0, -111.0, 111.0, -3.9 - 25.4, -3.9)


def chapter_30():
    """The chamber frame's three setups on the VF-4 from the posted programs (gcode_sim.py), the floor plate's first;
    the loads between them are two-person lifts (no lifter); no camera moves within a shot."""
    w = Writer("30-machining-chamber", "Machining the chamber: the VF-4 and its 4th axis")
    scn = Shop()
    scn.add_person2()
    vf4 = VF4(scn)
    st = Mst("vf4")
    crew = Crew(scn)
    import shop_plan as SP
    check = SP.shop_world("vf4", E.vf4(door=1.0, table_x=-100.0)[0])
    cam_arm = cam_at("vf4", *CAM_VF4_ARM)
    cam_out = cam_at("vf4", *CAM_OUT)
    cam_wide = cam_at("vf4", *CAM_WIDE)
    cam_in = cam_at("vf4", *CAM_IN_FLAT)
    cart_parts = E.bench(CART["w"], CART["d"], CART["h"])
    scn.add_parts("cart", cart_parts, st @ E.T((CART["x"], CART["y"] - CART["d"] / 2, 0.0)))
    cart_names = [n for n in scn.sc.actors if n.startswith("cart/")]

    def show_cart(a):
        for n in cart_names:
            scn.sc.alpha[n] = a

    fr = Stock("frame")
    kg_blank = fr.kg()
    M_tab = E.T((-100.0, 0, 0))
    rule = LIFT_RULE
    # ---- F-S1: the programs' stock on the cart, the risers and edge clamps on the table
    vf4.fixtures("frame_B", "frameT", 0, rots=[["x", 180]])
    R_B = GS.rot_of("frame_B")
    P1 = vf4.M_setup @ E.T((0, 0, 0), R_B)
    vf4.set(table_x=-100.0, door=1.0)
    spec0 = fr.spec()
    cart_top = E.T((CART["x"], CART["y"] + CART["d"] / 2 - 160.0, 0.0))
    P_cart1 = rest_on(spec0, scn, cart_top, CART["h"], R_B)
    scn.set_obj("load", st @ P_cart1, spec0)
    # overview first: the station, the cart with the stock; the two people walk in from the aisle (lesson 5)
    hw = [end_hands(scn.obj_mesh(spec0)[0], P_cart1, -1), end_hands(scn.obj_mesh(spec0)[0], P_cart1, 1)]
    for i, sx in enumerate((-1.0, 1.0)):
        pw = (st @ np.r_[-3600.0 + 520.0 * i, -700.0 - 260.0 * i, 0.0, 1.0])[:3]
        crew.place(i, pw[0], pw[1], -90.0)
    crew.show(1.0)
    cap0 = "The chamber frame on the VF-4: three setups from the posted programs"
    sub0 = ("F-S0 (not shown): the 5.5 in. plate sawn and its core cut out by waterjet, the stock the programs start "
            f"from; {kg_blank:.1f} kg here")
    targets = []
    for i in range(2):
        mid = (P_cart1[:3, :3] @ ((hw[i][0] + hw[i][1]) / 2) + P_cart1[:3, 3])
        x, y, _ = stance_xy(i, mid)
        targets.append(tuple((st @ np.r_[x, y, 0.0, 1.0])[:2]))
    crew.walk_to(w, targets, cam_wide, cap0, sub0, "F-S1", speed=850.0)
    for i in range(int(1.0 * FPS)):
        w.frame(scn, cam_wide, cap0, sub=sub0, who=["person"], step="F-S1", status="person")
    # ---- lift 1: cart -> risers
    team_lift(w, scn, crew, "load", spec0, P_cart1, M_tab @ P1, kg_blank,
              f"Two people set the {kg_blank:.1f} kg stock on the risers",
              f"{kg_blank:.1f} kg, a reach of ~0.6 m into the machine; {rule}", "F-S1", cam=cam_out,
              check_items=check)
    scn.hide_obj("load")
    vf4.part("frame part", spec0, P1)
    crew.show(0.0)
    show_cart(0.0)
    # ---- arm A tightens the four edge clamps (the planned clip), then the doors shut, same camera
    play(w, scn, "vf4_clamps", cam_arm, hide=("frame part",))
    for i in range(18):
        vf4.set(door=1.0 - ease((i + 1) / 18))
        w.frame(scn, cam_arm, "Doors shut; cycle start", sub="the auto door (option), ~1.5 s", who=["machine"],
                step="F-S1", status="pass", proc_s=1.5 / 18)
    scn.show_arm("A", False)
    vf4.set(front_alpha=0.0)
    # ---- F-S1: frame_B.ngc
    capB = "F-S1: the bottom up, cut by frame_B.ngc as posted"
    m1 = cut_program(w, scn, vf4, fr, ["frame_B"], "frame part", lambda a: P1, cam_in, capB, [8.5], "F-S1")
    vf4.set(table_x=-100.0, table_y=0.0)
    vf4.set(front_alpha=1.0)
    kg1 = fr.kg()
    spec1 = fr.spec()
    # ---- doors open; lift 2a: off the risers onto the cart (the clamps loosened by arm A, the same path run back)
    show_cart(1.0)
    for i in range(2):
        mid = ((M_tab @ P1)[:3, :3] @ ((end_hands(scn.obj_mesh(spec1)[0], M_tab @ P1, -1 if i == 0 else 1)[0])) +
               (M_tab @ P1)[:3, 3])
        pw = (st @ np.r_[mid[0] + (-240.0 if i == 0 else 240.0) * 1.6, -1500.0, 0.0, 1.0])[:3]
        crew.place(i, pw[0], pw[1], 0.0)
    crew.show(1.0)
    scn.hide_obj("frame part")
    scn.set_obj("load", st @ M_tab @ P1, spec1)
    capO = "Doors open: the clamps off, two people take the part out"
    for i in range(18):
        vf4.set(door=ease((i + 1) / 18))
        w.frame(scn, cam_out, capO, sub="arm A loosened the clamps first (its planned path run back; not shown)",
                who=["machine"], step="F-S1", status="pass", proc_s=1.5 / 18)
    P_cart2 = rest_on(spec1, scn, cart_top, CART["h"], R_B)
    team_lift(w, scn, crew, "load", spec1, M_tab @ P1, P_cart2, kg1, capO, f"{kg1:.1f} kg after F-S1; {rule}", "F-S1",
              cam=cam_out, check_items=check)
    # ---- cut: the risers out, the dummy-floor plate in; lift 2b turns the part over onto it
    vf4.fixtures("frame_A", "frameT", 0, rots=[])
    R_A = GS.rot_of("frame_A")
    P2 = vf4.M_setup @ E.T((0, 0, 0), R_A)
    capF = "Two people turn it over onto the dummy-floor plate for F-S2"
    m1_ = scn.obj_mesh(spec1)[0]
    hp_flip = {0: end_hands(m1_, P_cart2, -1, fz=0.5, fy=(0.33, 0.67)),
               1: end_hands(m1_, P_cart2, 1, fz=0.5, fy=(0.33, 0.67))}
    team_lift(w, scn, crew, "load", spec1, P_cart2, M_tab @ P2, kg1, capF,
              f"{kg1:.1f} kg, turned 180 deg about the line between their hands; the 18 M4 screws from below (not "
              f"shown); {rule}", "F-S2", cam=cam_wide, check_items=check, n_move=int(5.5 * FPS), hand_pts=hp_flip)
    scn.hide_obj("load")
    vf4.part("frame part", spec1, P2)
    for i in range(int(2.0 * FPS)):
        w.frame(scn, cam_wide, capF, sub="the people step clear", who=["person"], step="F-S2", status="person")
    crew.show(0.0)
    show_cart(0.0)
    for i in range(18):
        vf4.set(door=1.0 - ease((i + 1) / 18))
        w.frame(scn, cam_wide, "Doors shut; cycle start", sub="the auto door (option), ~1.5 s", who=["machine"],
                step="F-S2", status="pass", proc_s=1.5 / 18)
    vf4.set(front_alpha=0.0)
    capA = "F-S2: the top down, cut by frame_A.ngc as posted"
    m2 = cut_program(w, scn, vf4, fr, ["frame_A"], "frame part", lambda a: P2, cam_in, capA, [13.0], "F-S2")
    vf4.set(table_x=-100.0, table_y=0.0)
    vf4.set(front_alpha=1.0)
    # ---- lift 3: the frame on its dummy-floor plate onto the HRT210's platter, turned to A 90 (left wall up)
    kg_frame = fr.kg()
    kg_plate = 312.0 * 222.0 * 25.4 * 2.70e-6
    spec2 = fr.spec(extra_mesh=plate_mesh())
    vf4.fixtures(None)
    scn.hide_obj("frame part")
    M_tab3 = E.T((40.0, 0, 0))                       # the table moved so the rotary is in reach (the plate rides on it)
    scn.set_obj("load", st @ M_tab3 @ P2, spec2)
    vf4.set(table_x=40.0, a=90.0)
    vf4.fixtures("frame_C0", "frameT", 0, rots=[["y", 90], ["x", -90]])
    R_C0 = GS.rot_of("frame_C0")
    P3 = vf4.M_setup @ E.T((0, 0, 0), R_C0)
    for n in vf4.sc.members("vf4/rotfix"):           # the plate on the platter comes with the load
        vf4.sc.alpha[n] = 0.0
    axis = np.array(vf4.axis, float)
    Q_at = lambda a: E.about(E.Rx(a), axis) @ P3    # noqa: E731
    P_to3 = E.T((40.0, 0, 0)) @ Q_at(90.0)
    for i in range(2):
        crew.place(i, *(st @ np.r_[(-700.0 if i == 0 else 500.0), -1500.0, 0.0, 1.0])[:2], 0.0)
    crew.show(1.0)
    show_cart(0.0)
    capC = "Two people set the frame and its plate on the 4th axis"
    for i in range(18):
        vf4.set(door=ease((i + 1) / 18))
        w.frame(scn, cam_out, capC, sub="the HRT210 indexed to A 90 for loading (left wall up)", who=["machine"],
                step="F-S3", status="pass", proc_s=1.5 / 18)
    m2_ = scn.obj_mesh(spec2)[0]
    hp_rot = {0: end_hands(m2_, M_tab3 @ P2, -1, fz=0.25), 1: end_hands(m2_, M_tab3 @ P2, 1, fz=0.8)}
    team_lift(w, scn, crew, "load", spec2, M_tab3 @ P2, P_to3, kg_frame + kg_plate, capC,
              f"frame {kg_frame:.1f} kg + MIC-6 plate {kg_plate:.1f} kg, turned 90 deg onto the platter; 4 bolts "
              f"through the opening (not shown); {rule}", "F-S3", cam=cam_out, check_items=check,
              n_move=int(5.5 * FPS), hand_pts=hp_rot)
    scn.hide_obj("load")
    for n in vf4.sc.members("vf4/rotfix"):
        vf4.sc.alpha[n] = 1.0
    vf4.part("frame part", fr.spec(), P3, rot=True)
    for i in range(int(1.5 * FPS)):
        w.frame(scn, cam_out, capC, sub="the people step clear", who=["person"], step="F-S3", status="person")
    crew.show(0.0)
    for i in range(18):
        vf4.set(door=1.0 - ease((i + 1) / 18))
        w.frame(scn, cam_out, "Doors shut; cycle start", sub="the auto door (option), ~1.5 s", who=["machine"],
                step="F-S3", status="pass", proc_s=1.5 / 18)
    vf4.set(front_alpha=0.0)
    capR = "F-S3: the four walls on the HRT210, frame_C_haas.nc as posted"
    m3 = cut_program(w, scn, vf4, fr, ["frame_C0", "frame_C90", "frame_C180", "frame_C270"], "frame part", Q_at,
                     cam_at("vf4", *CAM_IN_ROT), capR, [7.0, 2.5, 3.0, 3.0], "F-S3", a_end=0.0)
    vf4.set(front_alpha=1.0)
    GMIN[w.name] = {"F-S1 (frame_B)": round(m1, 2), "F-S2 (frame_A)": round(m2, 2), "F-S3 (frame_C)": round(m3, 2)}
    # ---- the floor plate's first setup: arm A (VGP20) loads P-S1 (the planned clip), then floor_A.ngc
    if os.environ.get("CH30_FLOOR", "1") != "0":
        scn.hide_obj("frame part")
        vf4.fixtures(None)
        fl = Stock("floor")
        vf4.set(table_x=-100.0, table_y=0.0, a=0.0, door=1.0)
        vf4.fixtures("floor_A", "floor", 0, rots=[])
        PF = vf4.M_setup @ E.T((0, 0, 0), GS.rot_of("floor_A"))
        play(w, scn, "vf4_floor_load", cam_arm, hide=("floor part",),
             sub="the finished frame is off the rotary (not shown); arm A sets the floor plate's 5.0 kg blank on the "
                 "parallels")
        scn.hide_obj("floor part")
        vf4.part("floor part", fl.spec(), PF)
        for i in range(18):
            vf4.set(door=1.0 - ease((i + 1) / 18))
            w.frame(scn, cam_arm, "Doors shut; cycle start", sub="the auto door (option), ~1.5 s", who=["machine"],
                    step="P-S1", status="pass", proc_s=1.5 / 18)
        scn.show_arm("A", False)
        vf4.set(front_alpha=0.0)
        cut_program(w, scn, vf4, fl, ["floor_A"], "floor part", lambda a: PF, cam_in,
                    "P-S1: the floor plate's top, floor_A.ngc as posted", [10.0], "P-S1")
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
    # the other 55 parts' hours (shop_summary.json: every part's machine / robot / person hours by motion class, less
    # the chamber frame and floor plate that chapter 30 shows); the time-lapse spreads them over these frames
    rest = dict(machine_h=0.0, robot_h=0.0, person_h=0.0, cam_h=0.0)
    try:
        sm = json.loads((OUT / "shop_summary.json").read_text())
        for r in sm["parts"]:
            if r["part"].startswith(("Process chamber body", "Chamber floor plate")):
                continue
            rest["machine_h"] += r["machine_h"]
            rest["robot_h"] += r["robot_h"]
            rest["person_h"] += r["person_h"] - (r.get("cam_h") or 0.0)
            rest["cam_h"] += r.get("cam_h") or 0.0
    except Exception:  # noqa: BLE001
        pass
    span_s = max(rest["machine_h"], 0.1) * 3600.0
    for i in range(n):
        w.frame(scn, [(8000.0, -1500.0, 7800.0), (8200.0, 6000.0, 600.0), (0, 0, 1)],
                "The other 55 parts, by motion class: each setup reuses its class's planned motion",
                sub=f"{tot.get('setups_with_4th_axis', 67)} setups with the 4th axis (setup_plan.json); time-lapse: "
                    f"{rest['machine_h']:.0f} h of cutting, {rest['robot_h']:.1f} h of arm time, {rest['person_h']:.0f} "
                    f"person-hours besides {rest['cam_h']:.0f} h of CAM (shop_summary.json, estimates)",
                who=["machine", "robot A", "robot B"], step="all parts", status="pass", proc_s=span_s / n,
                add={k: v / n for k, v in rest.items()})
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
    if PERSON_RESULTS and EVERY == 1 and not STILL:     # round 8: the two-person lifts replace round 7's jib lifts
        pj.write_text(json.dumps(dict(
            what="chapter 30's two-person lifts (shop_chapters.team_lift): the load's mass against a two-person "
                 "guideline, the hands' largest gap to their grip points on the load (mm), and the load's path "
                 "against the VF-4 (FCL; clear_mm, contact)",
            guideline=dict(single_person_kg=NIOSH_KG, team_factor=round(TEAM_FACTOR, 3), team_of_two_kg=round(TEAM_KG, 1),
                           sources=["NIOSH, Applications Manual for the Revised NIOSH Lifting Equation (DHHS (NIOSH) "
                                    "Publication No. 94-110, 1994): load constant 23 kg",
                                    "HSE L23, Manual Handling Operations Regulations 1992, guidance on team handling: "
                                    "a team of two can handle about two-thirds of the sum of their capabilities"]),
            lifts=PERSON_RESULTS), indent=1, default=str))
    if GFRAMES and EVERY == 1 and not STILL:   # every drawn cutter position: its program, line and time
        gj = LPBF / "analysis" / "out" / "videoqa" / "gcode_frames.json"
        gj.parent.mkdir(parents=True, exist_ok=True)
        prev = json.loads(gj.read_text()) if gj.exists() else {}
        for ch in sorted(set(r["chapter"] for r in GFRAMES)):
            rows = [r for r in GFRAMES if r["chapter"] == ch]
            prev[ch] = dict(
                what="every frame that draws the VF-4 cutting: the cutter is at the position the posted program has at "
                     "that frame's time (gcode_sim.Program.at: interpolated on the chord of the program line given), "
                     "the table and head at the axes that put it there (vf4_for)",
                frames=len(rows), programs=sorted(set(r["program"] for r in rows)), minutes=GMIN.get(ch),
                out_of_travel=sum(1 for r in rows if not r["in_travel"]),
                lines_per_program={p: len(set(r["line"] for r in rows if r["program"] == p))
                                   for p in sorted(set(r["program"] for r in rows))},
                rows=rows)
        gj.write_text(json.dumps(prev, indent=0))
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
