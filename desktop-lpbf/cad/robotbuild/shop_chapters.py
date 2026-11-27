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
ONLY = {int(v) for v in os.environ.get("SHOP_ONLY_FRAMES", "").split(",") if v.strip()}
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
        if ONLY:                                  # SHOP_ONLY_FRAMES=a,b,c: render just those frames (quick stills)
            if self.n_in - 1 not in ONLY:
                return
            if self.n_in - 1 >= max(ONLY):
                img = scn.render(cam)
                self.ch.frame(img, caption, sub=sub, who=list(who), step=step, status=status, proc_s=proc_s, **kw)
                raise StopIteration

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
    """Two people (shop_scene's person and a second people.Person). Round 9: people.py's Gait locks the feet, so a body
    is moved by setting x, y and hd every frame along a path a person can walk (eased, under 1.3 m/s, under 12 deg a
    frame on the spot) and the feet step after it; place() puts someone somewhere new across a cut."""

    def __init__(self, scn):
        self.scn = scn
        self.p = [scn.person, scn.person2]
        self.st = [dict(x=0.0, y=0.0, hd=0.0, lean=0.0, placed=False) for _ in self.p]

    def show(self, a):
        for p in self.p:
            p.show(a)

    def place(self, i, x, y, hd=0.0):
        """Between shots only: where person i stands when the next shot opens (both feet planted, no steps)."""
        self.st[i].update(x=x, y=y, hd=hd, lean=0.0, placed=True)
        self.p[i].place(x=x, y=y, hd=hd, hands={"l": None, "r": None}, lean=0.0, look=None, palm={"l": None, "r": None},
                        grip={"l": 0.3, "r": 0.3})

    def step(self, i, x, y, hd, hands=None, look=None, lean=0.0, palm=None, grip=None):
        s = self.st[i]
        s.update(x=x, y=y, hd=hd, lean=lean)
        kw = dict(x=x, y=y, hd=hd, hands=hands or {"l": None, "r": None}, look=look, lean=lean)
        kw["palm"] = palm or {"l": None, "r": None}
        if grip is not None:
            kw["grip"] = grip
        self.p[i].set(**kw)

    def walk_to(self, w, targets, cam, caption, sub, step, speed=900.0, face=HD, settle=6):
        """Both turn towards their targets [(x, y)], walk there (heading along the way, eased in and out), turn to
        `face` (deg) and stand while their last steps settle."""
        starts = [(s["x"], s["y"]) for s in self.st]
        dist = [math.hypot(tx - sx, ty - sy) for (tx, ty), (sx, sy) in zip(targets, starts)]
        n = max(int(math.ceil(max(dist) / (speed / FPS) * 1.4)), 1)        # eased: the peak is ~1.4x the mean
        heads = [math.degrees(math.atan2(-(tx - sx), ty - sy)) if d_ > 30 else s["hd"]
                 for (tx, ty), (sx, sy), d_, s in zip(targets, starts, dist, self.st)]

        def turn(goal):
            h0 = [s["hd"] for s in self.st]
            nt = max(max(int(math.ceil(abs(_wrap(g_ - h_)) / 9.0)) for g_, h_ in zip(goal, h0)), 0)
            for k in range(nt):
                u = ease((k + 1) / nt)
                for i in range(2):
                    self.step(i, self.st[i]["x"], self.st[i]["y"], h0[i] + _wrap(goal[i] - h0[i]) * u)
                w.frame(self.scn, cam, caption, sub=sub, who=["person"], step=step, status="person")

        turn(heads)
        for k in range(n):
            u = ease((k + 1) / n)
            for i in range(2):
                sx, sy = starts[i]
                tx, ty = targets[i]
                self.step(i, sx + (tx - sx) * u, sy + (ty - sy) * u, heads[i])
            w.frame(self.scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
        turn(list(face))
        for k in range(settle):
            for i in range(2):
                self.step(i, self.st[i]["x"], self.st[i]["y"], self.st[i]["hd"])
            w.frame(self.scn, cam, caption, sub=sub, who=["person"], step=step, status="person")

    def step_back(self, w, cam, caption, sub, step, dist=420.0, n=20):
        """Both take a few steps back (the Gait backs them up), arms down."""
        st0 = [(s_["x"], s_["y"], s_["hd"]) for s_ in self.st]
        for k in range(n + 6):
            u = ease(min(1.0, (k + 1) / n))
            for i, (x0, y0, hd) in enumerate(st0):
                a = math.radians(hd)
                self.step(i, x0 + math.sin(a) * dist * u, y0 - math.cos(a) * dist * u, hd)
            w.frame(self.scn, cam, caption, sub=sub, who=["person"], step=step, status="person")


PERSON_RESULTS = {}


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
        q[ax] = hi[ax] if sx[ax] > 0 else lo[ax]
        q[ay] = (hi[ay] - f * (hi[ay] - lo[ay])) if sy[ay] > 0 else (lo[ay] + f * (hi[ay] - lo[ay]))
        q[az] = (lo[az] + fz * (hi[az] - lo[az])) if sz[az] > 0 else (hi[az] - fz * (hi[az] - lo[az]))
        pts.append(q)
    return pts


def reach_of(org, hd, lean, hands):
    """people.carry()'s reach rule: how far (mm) the harder of the two hands is beyond 470 mm of its shoulder (< 0:
    within reach) for a body at org (world x, y) facing hd (deg) and leaning `lean` (deg)."""
    a = math.radians(hd)
    right = np.array([math.cos(a), math.sin(a)])
    fwd = np.array([-math.sin(a), math.cos(a)])
    yp, zp = SS.people.HIP_PIVOT
    lr = math.radians(lean)
    sy = yp + (15.2 - yp) * math.cos(lr) + (1407.0 - zp) * math.sin(lr)
    sz = zp + (1407.0 - zp) * math.cos(lr) - 25.0
    worst = -1e9
    for s, sx in (("l", -1.0), ("r", 1.0)):
        h = np.asarray(hands[s], float)
        loc = np.array([(h[:2] - org) @ right, (h[:2] - org) @ fwd, h[2]])
        worst = max(worst, float(np.linalg.norm(loc - np.array([sx * 174.7, sy, sz]))) - 470.0)
    return worst


def lean_for(org, hands):
    """The lean (deg) people.py's person needs to put its palms this far from its body (the horizontal distance to the
    farther hand, at 0.95-1.15 m up): measured on the posed model (round 9: palms 400, 500, 600, 700, 800 mm ahead and
    120 mm to each side land within 15 mm at leans of about 10, 20, 30, 40, 50 deg)."""
    d = max(float(np.hypot(*(np.asarray(h, float)[:2] - org))) for h in hands.values())
    return float(np.interp(d, [420.0, 515.0, 612.0, 710.0, 809.0, 860.0], [10.0, 20.0, 30.0, 40.0, 50.0, 56.0]))


def pair_lift(w, scn, crew, name, spec, keys, kg, caption, sub, step, cam, hand_pts=None, check_items=None,
              fronts=None, M_st=None, walk_in=True, step_back=True, frames_per_m=60.0):
    """Two people side by side, facing the station's +y (into the VF-4), each holding one end of a load with both hands
    (round 8's team lift, round 9: the feet locked, the bodies kept off the load and the machine, the hands on the faces
    and not in them). keys: [(load pose in the station frame, seconds or None)] along which the load goes (eased per leg,
    the people following it: side-steps along x, a step or two along y, a lean as deep as the reach needs).
    fronts: [(station y, z from, z to, x from, x to)] the bodies' fronts stay behind between those heights where they
    stand within those x (the VF-4's face below its sill, the cart's near edge). hand_pts: {person: (hand l, hand r)} in the load's frame (default end_hands at the first pose)."""
    from scipy.spatial.transform import Rotation, Slerp
    M = Mst("vf4") if M_st is None else M_st
    yaw0 = math.degrees(math.atan2(M[1, 0], M[0, 0]))
    hds = [HD[0] + yaw0, HD[1] + yaw0]
    m, _ = scn.obj_mesh(spec)
    v = np.asarray(m.points, float)
    lo, hi = v.min(0), v.max(0)
    c_loc = (lo + hi) / 2
    half = (hi - lo) / 2
    P0 = keys[0][0]
    if hand_pts is None:
        hand_pts = {0: end_hands(m, P0, -1), 1: end_hands(m, P0, +1)}
    # person 0 stands on the -x side, its left hand on the near point; person 1 mirrored
    order = {0: ("l", "r"), 1: ("r", "l")}
    legs_ = list(zip(keys[:-1], keys[1:]))

    def leg_frames(a, b, secs):
        if secs is not None:
            return max(int(round(secs * FPS)), 2)
        d = float(np.linalg.norm(b[:3, 3] - a[:3, 3]))
        ang = float(np.degrees(np.arccos(np.clip((np.trace(a[:3, :3].T @ b[:3, :3]) - 1) / 2, -1, 1))))
        return max(int(round((d / 1000.0 * frames_per_m) + ang / 6.0)), 8)

    def world(p):
        return (M @ np.r_[p, 1.0])[:3]

    def stance(i, P, lean_prev=None):
        """Body origin (world), heading, lean and the hand targets (world) for load pose P (station)."""
        hw = [world(P[:3, :3] @ q + P[:3, 3]) for q in hand_pts[i]]
        hands = dict(zip(order[i], hw))
        mid = (hw[0] + hw[1]) / 2
        a = math.radians(hds[i])
        fwd = np.array([-math.sin(a), math.cos(a)])
        right = np.array([math.cos(a), math.sin(a)])
        inner = right if i == 0 else -right
        org = mid[:2] - 60.0 * inner - 330.0 * fwd
        # in the station frame: the body's front stays behind each front (y, z from, z to, x from, x to) it stands at:
        # the VF-4's face below the sill, the cart's near edge (below the hips, so the lean doesn't move it)
        Minv = np.linalg.inv(M)
        o_st = (Minv @ np.r_[org, 0.0, 1.0])[:3]
        for yl, z0_, z1_, x0_, x1_ in (fronts or ()):
            if x0_ - 260.0 <= o_st[0] <= x1_ + 260.0:
                lim = yl - 15.0 - SS.people.body_front(z0_, z1_, 0.0)
                if o_st[1] > lim:
                    o_st[1] = lim
        # off the load: the front of the body (at the load's heights) 30 mm behind its near face
        Pc = P[:3, :3] @ c_loc + P[:3, 3]
        corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        cw = corners @ P[:3, :3].T + P[:3, 3]
        y_near = float(cw[:, 1].min())
        zl, zh = float(cw[:, 2].min()), float(cw[:, 2].max())
        org = (M @ np.r_[o_st, 1.0])[:2]
        lean = lean_for(org, hands)
        fr = SS.people.body_front(zl - 40.0, zh + 40.0, lean)
        y_body_max = y_near - 30.0 - fr                 # the body (arms out of it) off the load's near face
        if o_st[1] > y_body_max and abs(float(Pc[0] - o_st[0])) < 300.0:
            o_st[1] = y_body_max
            org = (M @ np.r_[o_st, 1.0])[:2]
            lean = lean_for(org, hands)
        r = reach_of(org, hds[i], lean, hands)
        return org, hds[i], float(lean), hands, float(r)

    crew.show(1.0)
    scn.set_obj(name, M @ P0, spec)
    st0 = [stance(i, P0) for i in range(2)]
    if walk_in:
        crew.walk_to(w, [tuple(s_[0]) for s_ in st0], cam, caption, sub, step, face=hds)
    else:
        for i in range(2):
            crew.place(i, *st0[i][0], st0[i][1])
    n_reach, n_rel = 10, 10
    seq = [(0.0, 0, 0.0)] * 0
    gaps, clears, reaches, deep = [], [], [], []
    poses = []
    def via(p, s_, h, away, u):
        """A hand from where it hangs (u 0) to h (u 1) by way of a point 150 mm out from the end face (along `away`)
        at h's height: it comes in level, never through the load or what it stands on."""
        pre = np.asarray(h, float) + 150.0 * np.asarray(away, float)
        r = p.rest_hand(s_)
        if u < 0.55:
            return tuple(r + (pre - r) * ease(u / 0.55))
        return tuple(pre + (np.asarray(h, float) - pre) * ease((u - 0.55) / 0.45))

    def away_of(i, P):
        nrm = M[:3, :3] @ P[:3, :3] @ np.array([1.0, 0.0, 0.0])
        nrm = nrm * (1.0 if float(nrm @ (M[:3, :3] @ np.array([1.0, 0, 0]))) >= 0 else -1.0)
        return -nrm if i == 0 else nrm                  # the end face's outward normal (world)

    # reach in: the hands from where they hang to the load, the lean easing in
    for k in range(n_reach):
        u = (k + 1) / n_reach
        for i in range(2):
            org, hd, lean, hands, r = stance(i, P0)
            p = crew.p[i]
            aw = away_of(i, P0)
            tg = {s: via(p, s, hands[s], aw, u) for s in hands}
            crew.step(i, org[0], org[1], hd, hands=tg, look=tuple((np.asarray(hands["l"]) + hands["r"]) / 2),
                      lean=lean * ease(u), palm={"l": tuple(-aw), "r": tuple(-aw)}, grip={"l": 0.1, "r": 0.1})
            if u >= 1.0:
                Mbox0 = M @ P0 @ E.T(tuple(c_loc))
                seat_hands(p, hands, [(Mbox0, half)], away={"l": tuple(aw), "r": tuple(aw)})
        w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
    # the carry along the keys
    Pprev = P0
    for (Pa, _), (Pb, secs) in legs_:
        n = leg_frames(Pa, Pb, secs)
        sl = Slerp([0.0, 1.0], Rotation.from_matrix([Pa[:3, :3], Pb[:3, :3]]))
        for k in range(n):
            u = ease((k + 1) / n)
            P = np.eye(4)
            P[:3, :3] = sl(u).as_matrix()
            ca = Pa[:3, :3] @ c_loc + Pa[:3, 3]
            cb = Pb[:3, :3] @ c_loc + Pb[:3, 3]
            P[:3, 3] = ca + (cb - ca) * u - P[:3, :3] @ c_loc
            poses.append(M @ P)
            scn.set_obj(name, M @ P, spec)
            Mbox = M @ P @ E.T(tuple(c_loc))
            for i in range(2):
                org, hd, lean, hands, r = stance(i, P)
                away = away_of(i, P)
                p = crew.p[i]
                crew.step(i, org[0], org[1], hd, hands={s: tuple(v_) for s, v_ in hands.items()},
                          look=tuple((np.asarray(hands["l"]) + hands["r"]) / 2), lean=lean,
                          palm={"l": tuple(-away), "r": tuple(-away)}, grip={"l": 0.1, "r": 0.1})
                _, left, err = seat_hands(p, hands, [(Mbox, half)], away={"l": tuple(away), "r": tuple(away)})
                deep.append(left)
                gaps.append(err)
                reaches.append(r)
                cc = SS.people.carry_check(p, lo, hi, M @ P)
                clears.append(cc["body_clear_mm"])
            w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
        Pprev = Pb
    # let go: the hands back down, the lean out
    Pend = keys[-1][0]
    for k in range(n_rel):
        u = (k + 1) / n_rel
        for i in range(2):
            org, hd, lean, hands, r = stance(i, Pend)
            p = crew.p[i]
            aw = away_of(i, Pend)
            tg = {s: via(p, s, hands[s], aw, 1.0 - u) for s in hands}
            crew.step(i, org[0], org[1], hd, hands=tg, look=None, lean=lean * (1.0 - ease(u)),
                      palm={"l": tuple(-aw), "r": tuple(-aw)}, grip={"l": 0.1, "r": 0.1})
        w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
    for i in range(2):
        crew.step(i, crew.st[i]["x"], crew.st[i]["y"], crew.st[i]["hd"], lean=0.0)
    if step_back:
        crew.step_back(w, cam, caption, "they step back", step)
    res = dict(kg=round(kg, 2), team_guideline_kg=round(TEAM_KG, 1), under_guideline=bool(kg <= TEAM_KG),
               frames=len(poses) + n_reach + n_rel, glove_in_load_mm_max=round(max(deep), 2) if deep else None,
               palm_error_mm_max=round(max(gaps), 1) if gaps else None,
               reach_over_mm_max=round(max(reaches), 1) if reaches else None,
               body_clear_mm_min=round(min(clears), 1) if clears else None)
    if check_items is not None and poses:
        vf = (np.asarray(m.points, float), m.faces.reshape(-1, 4)[:, 1:].astype(np.int32))
        res.update(load_path_check(check_items, vf, poses[::2]))
    key = f"{step}: {caption}"
    while key in PERSON_RESULTS:
        key += " (again)"
    res["caption"] = caption
    res["sub"] = sub
    PERSON_RESULTS[key] = res
    print("pair lift", key, res, flush=True)
    return res


def carry_lift(w, scn, crew, name, spec, keys, kg, caption, sub, step, cam, ends=("-x", "+x"), grip=None, M_st=None,
               frames_per_m=55.0, walk_in=True, inset=None, z_below_top=None, clear=40.0):
    """Two people carrying a load by its two ends (people.carry: each stands outside one end, facing the load, its
    hands on the faces beside the end or under it): they walk to their stances, take hold, carry it along the keys
    [(load pose in M_st's frame, seconds or None)] (their stances rigid in the load's frame, so the Gait walks them
    with it: sideways, forwards or backwards), set it down, let go and step back."""
    from scipy.spatial.transform import Rotation, Slerp
    M = np.eye(4) if M_st is None else M_st
    m, _ = scn.obj_mesh(spec)
    v = np.asarray(m.points, float)
    lo, hi = v.min(0), v.max(0)
    c_loc = (lo + hi) / 2
    P0 = keys[0][0]
    keep = ("x", "y", "hd", "lean", "hands", "palm", "elbow", "bend", "grip", "look")

    def st_at(P):
        zh = None
        if z_below_top is not None:                   # the hands near the top edge, so the fingers stay off what
            cw = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
            zh = float(((M @ P)[:3, :3] @ cw.T).T[:, 2].max() + (M @ P)[2, 3]) - z_below_top   # it stands on
        return SS.people.carry(lo, hi, M @ P, ends=ends, grip=grip, inset=inset, z_hands=zh, clear=clear)

    half = (hi - lo) / 2

    def seat(i, d, P):
        """Round 9: each palm moved off the face it is on until the glove is outside the load (2.5 mm): one person's
        two hands on two opposite faces read, to the frame audit, as the load clamped inside the glove."""
        if not d.get("hands") or not d.get("palm"):
            return 0.0
        away = {s_: -np.asarray(d["palm"][s_], float) for s_ in d["hands"] if d["palm"].get(s_) is not None
                and not isinstance(d["palm"][s_], str)}
        if len(away) < 2:
            return 0.0
        _, left, _ = seat_hands(crew.p[i], {s_: np.asarray(h, float) for s_, h in d["hands"].items()},
                                [(M @ P @ E.T(tuple(c_loc)), half)], away=away)
        return left

    crew.show(1.0)
    scn.set_obj(name, M @ P0, spec)
    s0 = st_at(P0)
    if walk_in:
        # first to 450 mm behind each stance, then the last steps straight in along it (round 9: walking straight to
        # the stances brushed the load's corners)
        pre = []
        for s_ in s0:
            a = math.radians(s_["hd"])
            pre.append((s_["x"] - 450.0 * -math.sin(a), s_["y"] - 450.0 * math.cos(a)))
        crew.walk_to(w, pre, cam, caption, sub, step, face=[s_["hd"] for s_ in s0], settle=2)
        crew.walk_to(w, [(s_["x"], s_["y"]) for s_ in s0], cam, caption, sub, step, face=[s_["hd"] for s_ in s0],
                     speed=600.0)
    n_reach, n_rel = 10, 10
    clears, deep, reaches = [], [], []
    def via(p, s_, h, hd_, u):
        """A hand from where it hangs (u 0) to h (u 1) by way of a point 150 mm out from the load towards the body at
        h's height, so it comes in level and never through the load or what it stands on."""
        a = math.radians(hd_)
        back = -np.array([-math.sin(a), math.cos(a), 0.0])
        pre = np.asarray(h, float) + 150.0 * back
        r = p.rest_hand(s_)
        if u < 0.55:
            v_ = ease(u / 0.55)
            return tuple(r + (pre - r) * v_)
        v_ = ease((u - 0.55) / 0.45)
        return tuple(pre + (np.asarray(h, float) - pre) * v_)

    for k in range(n_reach):
        u = (k + 1) / n_reach
        for i in range(2):
            d = {kk: s0[i][kk] for kk in keep if kk in s0[i]}
            p = crew.p[i]
            d["hands"] = {s: via(p, s, h, s0[i]["hd"], u) for s, h in s0[i]["hands"].items()}
            d["lean"] = s0[i]["lean"] * ease(u)
            crew.st[i].update(x=d["x"], y=d["y"], hd=d["hd"])
            p.set(**d)
            seat(i, d, P0)
        w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
    poses = []
    for (Pa, _), (Pb, secs) in zip(keys[:-1], keys[1:]):
        dist = float(np.linalg.norm(Pb[:3, 3] - Pa[:3, 3]))
        ang = float(np.degrees(np.arccos(np.clip((np.trace(Pa[:3, :3].T @ Pb[:3, :3]) - 1) / 2, -1, 1))))
        n = max(int(round(secs * FPS)), 2) if secs is not None else max(int(round(dist / 1000.0 * frames_per_m
                                                                                     + ang / 6.0)), 8)
        sl = Slerp([0.0, 1.0], Rotation.from_matrix([Pa[:3, :3], Pb[:3, :3]]))
        for k in range(n):
            u = ease((k + 1) / n)
            P = np.eye(4)
            P[:3, :3] = sl(u).as_matrix()
            ca = Pa[:3, :3] @ c_loc + Pa[:3, 3]
            cb = Pb[:3, :3] @ c_loc + Pb[:3, 3]
            P[:3, 3] = ca + (cb - ca) * u - P[:3, :3] @ c_loc
            poses.append(M @ P)
            scn.set_obj(name, M @ P, spec)
            ss = st_at(P)
            for i in range(2):
                d = {kk: ss[i][kk] for kk in keep if kk in ss[i]}
                crew.st[i].update(x=d["x"], y=d["y"], hd=d["hd"])
                crew.p[i].set(**d)
                seat(i, d, P)
                cc = SS.people.carry_check(crew.p[i], lo, hi, M @ P)
                clears.append(cc["body_clear_mm"])
                deep.append(cc["hands_in_mm"])
                reaches.append(ss[i]["reach_mm"])
            w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
    Pend = keys[-1][0]
    se = st_at(Pend)
    for k in range(n_rel):
        u = (k + 1) / n_rel
        for i in range(2):
            d = {kk: se[i][kk] for kk in keep if kk in se[i]}
            p = crew.p[i]
            d["hands"] = {s: via(p, s, h, se[i]["hd"], 1.0 - u) for s, h in se[i]["hands"].items()}
            d["lean"] = se[i]["lean"] * (1.0 - ease(u))
            p.set(**d)
            seat(i, d, Pend)
        w.frame(scn, cam, caption, sub=sub, who=["person"], step=step, status="person")
    for i in range(2):
        crew.p[i].set(hands={"l": None, "r": None}, palm={"l": None, "r": None}, elbow={"l": None, "r": None},
                      bend={"l": False, "r": False}, lean=0.0)
    crew.step_back(w, cam, caption, "they step back", step)
    res = dict(kg=round(kg, 2), team_guideline_kg=round(TEAM_KG, 1), under_guideline=bool(kg <= TEAM_KG),
               frames=len(poses) + n_reach + n_rel, body_clear_mm_min=round(min(clears), 1) if clears else None,
               hands_in_load_mm_max=round(max(deep), 1) if deep else None,
               reach_over_mm_max=round(max(reaches), 1) if reaches else None, how="people.carry (round 9)")
    key = f"{step}: {caption}"
    while key in PERSON_RESULTS:
        key += " (again)"
    res["caption"] = caption
    res["sub"] = sub
    PERSON_RESULTS[key] = res
    print("carry lift", key, res, flush=True)
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


def trail_clear(tr, pos, r, lift=1.2, step=1.0):
    """Round 9 (for the frame audit): the path just run, drawn as a 0.9 mm tube, lifted `lift` mm along the tool axis
    (setup +z) so it lies on the cut floor rather than in it, and cut back to r + 1.5 mm from the tool's axis so it
    doesn't run inside the tool. tr, pos: setup coordinates. None if nothing is left."""
    tr = np.asarray(tr, float)
    seg = np.linalg.norm(np.diff(tr, axis=0), axis=1)
    if not len(seg) or seg.sum() < 1e-6:
        return None
    s = np.r_[0.0, np.cumsum(seg)]
    u = np.arange(0.0, s[-1] + 1e-9, step)
    pts = np.c_[[np.interp(u, s, tr[:, k]) for k in range(3)]].T
    keep = np.hypot(pts[:, 0] - pos[0], pts[:, 1] - pos[1]) > r + 1.5
    if keep.sum() < 2:
        return None
    # the part outside the tool, up to where the path last enters it
    last = int(np.flatnonzero(keep)[-1])
    first = last
    while first > 0 and keep[first - 1]:
        first -= 1
    pts = pts[first:last + 1]
    if len(pts) < 2:
        return None
    return pts + np.array([0.0, 0.0, lift])


def cut_program(w, scn, vf4, stock, names, part_obj, Q_of, cam, cap, seconds, step, a_end=None, remesh=1):
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
    # Round 8 (video_qa on the composed MP4): at 49-192x a fixed station camera saw the table jump to each sample's
    # tool position. The camera now rides on the table (CAM-simulation style): the shot is framed for the part's centre
    # under the spindle, and every frame adds the table's offset from there, so the part stays still and the spindle
    # moves over it. The loading, lifts and door shots keep their fixed station cameras.
    Q0 = Q_of(GS.Program(names[0]).a_deg)
    c0 = (stock.g.lo + stock.g.hi) / 2 if hasattr(stock.g, "hi") else np.zeros(3)
    q0 = Q0[:3, :3] @ c0 + Q0[:3, 3]
    ref = (-q0[0], E.VF4["spindle_y"] - q0[1])
    Mv = Mst("vf4")

    def tcam():
        d = Mv[:3, :3] @ np.array([vf4.state["table_x"] - ref[0], vf4.state["table_y"] - ref[1], 0.0])
        return [tuple(np.asarray(cam[0], float) + d), tuple(np.asarray(cam[1], float) + d), cam[2]]

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
                w.frame(scn, tcam(), cap, sub=f"{prog.src} line {prog.index_lines['home']}: G53 G00 Z0. (Z home "
                        f"before the index)", who=["machine"], step=step, status="pass",
                        proc_s=max(z0, 1.0) / (25400.0 / 60.0) / 4)
            a0 = vf4.state["a"]
            for i in range(8):
                vf4.set(a=a0 + (a - a0) * ease((i + 1) / 8))
                w.frame(scn, tcam(), cap, sub=f"{prog.src} line {prog.index_lines['a']}: M11, G00 A{a}., M10 (unclamp, "
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
                tr = trail_clear(tr, pos, GS.tools()[T]["d"] / 2)
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
            w.frame(scn, tcam(), cap, sub=f"{prog.src} line {ln}: T{T}, {label[:58]} | {factor:.0f}x time-lapse of "
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
        w.frame(scn, tcam(), cap, sub="Program end: Z home (rapid)", who=["machine"], step=step, status="pass",
                proc_s=max(z0, 1.0) / (25400.0 / 60.0) / 8)
    if a_end is not None and abs(vf4.state["a"] - a_end) > 0.1:
        a0 = vf4.state["a"]
        for i in range(8):
            vf4.set(a=a0 + (a_end - a0) * ease((i + 1) / 8))
            w.frame(scn, tcam(), cap, sub=f"{GS.HAAS}: M11, G00 A0., M10, M30 (the program's end; ~3 s, our estimate)",
                    who=["machine"], step=step, status="pass", proc_s=3.0 / 8)
    return tot_min


# ================================================================================================ clip playback
def play(w, scn, name, cam, sub=None, caption=None, hide=(), tool_override=None, obj_color=None, rev=False,
         cut=None, specs=None):
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
            scn.set_obj(o, M, (specs or {}).get(o, clip["objects"].get(o)), color=(obj_color or {}).get(o))
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
def box_depth(P, M, half):
    """How deep the points P (n, 3, world) are inside the box of half-extents `half` posed at M (its centre's frame):
    per point, the distance to the nearest face if inside, else 0; and that face's outward normal (world)."""
    loc = (np.asarray(P, float) - M[:3, 3]) @ M[:3, :3]
    h = np.asarray(half, float)
    gap = h - np.abs(loc)                                   # > 0 on all three axes: inside
    inside = (gap > 0).all(axis=1)
    k = np.argmin(gap, axis=1)
    idx = np.arange(len(loc))
    d = np.where(inside, gap[idx, k], 0.0)
    nrm = np.zeros_like(loc)
    nrm[idx, k] = np.sign(loc[idx, k])
    return d, nrm @ M[:3, :3].T


def seat_hands(p, hands, boxes, away, limit=0.8, iters=8, margin=2.5):
    """Round 9 (scene_audit: gloves 40-100 mm inside the jack's handle and the loads): put person p's palms where
    `hands` says ({side: world point or None}), then move a palm back along `away` ({side: world unit vector}, the
    side the hand comes from) while its glove reaches more than `limit` mm into any of the boxes [(M, half extents)]:
    a hand on a surface, not in it. people.py's IK aims the palm, but grounding the shoes and turning the palm move it
    10-40 mm, so each pass also re-aims the IK target by the palm's error. Returns (palm points reached, the deepest
    the glove is left inside (mm), the largest palm error left (mm))."""
    want = {k: (None if v is None else np.asarray(v, float)) for k, v in hands.items()}
    tg = {k: (None if v is None else v.copy()) for k, v in want.items()}
    left, err = 0.0, 0.0
    for it in range(iters):
        p.set(hands={k: (None if v is None else tuple(v)) for k, v in tg.items()})
        P = p.posed()["glove"][0]
        F = p.sc.gmat[p.group]
        side = np.where(((P - F[:3, 3]) @ F[:3, 0]) < 0.0, "l", "r")   # its local -x is its left
        worst, err, moved = 0.0, 0.0, False
        for sd in ("l", "r"):
            if want.get(sd) is None:
                continue
            e = want[sd] - p.hand_point(sd)
            err = max(err, float(np.linalg.norm(e)))
            deep = 0.0
            for M, half in boxes:                        # the box grown by `margin`: the glove's vertices stay that
                d, _ = box_depth(P[side == sd], M, np.asarray(half, float) + margin)   # far out (its edges cross less)
                if len(d):
                    deep = max(deep, float(d.max()))
            worst = max(worst, deep)
            step = np.asarray(away[sd], float) * (deep - 0.5 * limit) if deep > limit else np.zeros(3)
            want[sd] = want[sd] + step
            if np.linalg.norm(e) > 1.5 or deep > limit:
                tg[sd] = tg[sd] + e + step
                moved = True
        left = worst
        if not moved:
            break
    return want, round(left, 2), round(err, 1)


def chapter_20():
    """Receiving. Round 9 (round 8's audit: the pallet and a crate driven >100 mm into the stock rack's upright, the tray
    lifted through the box's shut flaps and tape, arm B's fingertips 42 mm in them, the person's gloves 59 mm inside the
    jack's handle): the pallet turned so the jack's forks run along its stringers (a GMA pallet's two-way entry), between
    its bottom boards, with the crates side by side on it; its path 350 mm clear of the rack; the flaps opened and the tape
    cut before the tray comes out; the person's hands on the handle's bar, not in it (seat_hands)."""
    w = Writer("20-receiving", "Receiving and unpacking")
    scn = Shop()
    context_vf4(scn)
    st = Mst("receiving")
    import shop_clips as SCL
    scn.add_parts("recv", E.placed(E.lift_table(760.0), E.T((0.0, 520.0, 0.0))), st)
    scn.add_parts("recvbox", SCL.recv_box_parts(0.0), st)
    # the pallet (48 in. along its x) turned so its x runs along the world's +y, the way it is pushed; the crates on it
    pal = E.pallet()
    pv_, pf_ = E.fcl_items(pal)[0][1]
    pal_spec = dict(kind="vf", v=pv_, f=pf_, color=E.C["wood"])
    R90 = E.Rz(90.0)
    X_PAL = 3700.0                       # world x of its centre: 280 mm clear of the lift table, 350 of the rack's base
    Y0, Y1 = 400.0, 2850.0               # world y of its centre, start and end
    LIFT = 20.0                          # the jack lifts it 20 mm
    crates = [("IPG laser crate (52 kg)", (-220.0, 0.0, 0.0), (760.0, 680.0, 380.0)),
              ("plate bundle (58 kg)", (380.0, 0.0, 0.0), (400.0, 720.0, 110.0)),
              ("chamber blank 13 x 9.5 x 5.5 in. 6061 (30.0 kg)", (380.0, 0.0, 110.0), (270.0, 360.0, 180.0))]
    PAL_TOP = 144.0

    def M_pal(y, z):
        return E.T((X_PAL, y, z), R90)

    # the jack: forks along its +x from the pump; set so the fork rollers drop between the pallet's 4th and 5th bottom
    # boards (pallet x 340-470) and the forks lie between its stringers; its x along the pallet's x
    JX = 404.6 - (48 * E.INCH - 60.0)    # the pump's x in the pallet's frame (the rollers at pallet x 404.6)
    HANDLE_DEG = 45.0                    # tilted back to the person (10 deg in round 8: the bar at 1.36 m)
    RAISE_UP = PAL_TOP - 16.0 + LIFT - 2.9 * E.INCH     # forks' top under the top boards with the pallet lifted 20 mm
    jack0, jm = E.pallet_jack(raise_mm=RAISE_UP, handle_deg=HANDLE_DEG)
    for k2, pp in jack0.items():
        scn.sc.add(f"jack/{k2}", pp.mesh, pp.color, group="jack")
    hb = np.array([jm["handle"][0], 0.0, jm["handle"][2]])        # the bar's centre (jack frame); 40 x 300 x 40 mm
    p = scn.person
    p.show(0.0)
    cam0 = [(1500.0, -2500.0, 7200.0), (8000.0, 6000.0, 600.0), (0, 0, 1)]
    for o, (nm, c, d) in enumerate(crates):              # on the jack, lifted, from the first frame
        scn.set_obj(f"crate {o}", M_pal(Y0, LIFT) @ E.T((c[0], c[1], PAL_TOP + c[2])),
                    dict(kind="box", b=(-d[0] / 2, d[0] / 2, -d[1] / 2, d[1] / 2, 0, d[2]), color=E.C["box"]))
    scn.set_obj("pallet", M_pal(Y0, LIFT), pal_spec)
    scn.sc.gmat["jack"] = M_pal(Y0, 0.0) @ E.T((JX, 0.0, 0.0))
    for i in range(int(6 * FPS)):
        w.frame(scn, cam0, "The robot shop: two UR12e arms on MiR250s, a VF-4 with a 4th axis, a lathe, a bandsaw",
                sub="north row: VF-4, ST-10 lathe, deburr and wash, measuring, bench; south row: receiving, stock, saw, "
                    "tools; a hypothetical layout (robot-shop.md)", who=[], step="", status="")
    cam = cam_at("receiving", (2600, -2600, 2600), (-1600, 1800, 600))
    cap = "Three crates over two arms' 22.4 kg: the person brings them in with a pallet jack"
    sub = ("the chamber blank (30.0 kg), the plate bundle (58 kg), the laser (52 kg); a 48 x 40 in. pallet, a 27 x 48 "
           "in. manual jack along its stringers")
    n_move, n_low = int(13 * FPS), 12
    p.show(1.0)
    seat = []
    walk = PersonWalk(p)
    for i in range(n_move + n_low):
        if i < n_move:
            s = ease((i + 1) / n_move)
            y, z, raise_ = Y0 + (Y1 - Y0) * s, LIFT, RAISE_UP
        else:                                            # at the end the release lever lowers the forks: the pallet lands
            u = ease((i - n_move + 1) / n_low)
            y, raise_ = Y1, RAISE_UP * (1.0 - u)
            z = max(0.0, raise_ - (RAISE_UP - LIFT))
            jk, _ = E.pallet_jack(raise_mm=raise_, handle_deg=HANDLE_DEG)
            scn.sc.set_mesh("jack/pallet jack forks", jk["pallet jack forks"].mesh)
        Mp = M_pal(y, z)
        scn.set_obj("pallet", Mp, pal_spec)
        for o, (nm, c, d) in enumerate(crates):
            scn.set_obj(f"crate {o}", Mp @ E.T((c[0], c[1], PAL_TOP + c[2])))
        Mj = M_pal(y, 0.0) @ E.T((JX, 0.0, 0.0))
        scn.sc.gmat["jack"] = Mj
        bar = Mj @ E.T(tuple(hb))
        back = (bar @ np.r_[-20.0, 0.0, 0.0, 1.0])[:3]            # the bar's face towards the person (world -y)
        hands = {"l": back + np.array([-110.0, -14.0, 0.0]), "r": back + np.array([110.0, -14.0, 0.0])}
        walk.to(X_PAL, float(back[1]) - 14.0 - 300.0, 0.0, grip={"l": 0.05, "r": 0.05},
                palm={"l": (0.0, 1.0, 0.0), "r": (0.0, 1.0, 0.0)}, look=tuple(np.r_[X_PAL, y + 900.0, 400.0]),
                lean=6.0)
        _, left, err = seat_hands(p, hands, [(bar, (20.0, 150.0, 20.0))],
                                  away={"l": (0.0, -1.0, 0.0), "r": (0.0, -1.0, 0.0)})
        seat.append((left, err))
        w.frame(scn, cam, cap, sub=sub, who=["person"], step="receiving", status="person")
    print("chapter 20: hands on the jack's bar: deepest left in it, largest palm error (mm):",
          max(v[0] for v in seat), max(v[1] for v in seat), flush=True)
    p.show(0.0)
    cam_t = cam_at("receiving", (-1700, -1500, 2000), (0, 420, 900))
    play(w, scn, "recv_tape", cam_t)
    # the cut: the flaps folded back and the tape cut (by a person: cardboard deforms; not planned), as the unbox clip
    # was planned
    scn.add_parts("recvbox", SCL.recv_box_parts(1.0), st)
    play(w, scn, "recv_unbox", cam_at("receiving", (1500, -1700, 2100), (0, 300, 900)),
         sub="4.0 kg tray with a 20 mm handle fin; the flaps were folded back after the cut (cardboard deforms: not "
             "planned for the arms); FCL, 0.2 deg audit")
    return w.close()


class PersonWalk:
    """One person's walk, frame by frame: to(x, y, hd, ...) moves the body there; people.py's Gait (round 9) plants the
    feet and steps them after the body (no phase, no amp)."""

    def __init__(self, p):
        self.p = p

    def to(self, x, y, hd, **kw):
        self.p.set(x=x, y=y, hd=hd, **kw)


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
    the loads between them are two-person lifts (no lifter); no camera moves within a shot.

    Round 9 (round 8's audit: a person's shoes, trousers and coat through the VF-4's front and table, the coats and
    gloves in the loads, the legs in the cart; the feet slid 0.9-1.2 m per stance): the cart stands against the VF-4's
    front left of the door, its long side along x, so the two people, side by side and facing the machine, take a load
    off it, side-step to the door and reach in, never with a leg under the cart or past the sill (pair_lift: the bodies
    behind the machine's face and the cart's edge, 30 mm off the load, the hands on its end faces and not in them, the
    lean as deep as the reach needs); people.py's Gait locks their feet."""
    w = Writer("30-machining-chamber", "Machining the chamber: the VF-4 and its 4th axis")
    scn = Shop()
    scn.add_person2()
    vf4 = VF4(scn)
    st = Mst("vf4")
    crew = Crew(scn)
    import shop_plan as SP
    check = SP.shop_world("vf4", E.vf4(door=1.0, table_x=-100.0)[0])
    cam_arm = cam_at("vf4", *CAM_VF4_ARM)
    cam_out = cam_at("vf4", (-1250.0, -2350.0, 2700.0), (-450.0, 250.0, 950.0))   # the door and the cart (fixed)
    cam_wide = cam_at("vf4", *CAM_WIDE)
    cam_in = cam_at("vf4", *CAM_IN_FLAT)
    CARTX, CARTY0, CARTY1, CARTH = (-1400.0, -800.0), -380.0, -40.0, 900.0     # station frame: x span, y span, top
    cart_parts = E.bench(CARTX[1] - CARTX[0], CARTY1 - CARTY0, CARTH)
    scn.add_parts("cart", cart_parts, st @ E.T(((CARTX[0] + CARTX[1]) / 2, CARTY0, 0.0)))
    cart_c = E.T(((CARTX[0] + CARTX[1]) / 2, (CARTY0 + CARTY1) / 2, 0.0))
    fronts = [(-4.0, 0.0, 880.0, -1564.0, 1564.0), (CARTY0, 0.0, 905.0, CARTX[0], CARTX[1])]
    fr = Stock("frame")
    kg_blank = fr.kg()
    M_tab = E.T((-100.0, 0, 0))
    rule = LIFT_RULE

    def lift_keys(P_a, P_b, up_a=60.0, up_b=40.0, flip=None):
        """The load's path from P_a to P_b (station frame): up, side-step to P_b's x outside the machine, in, down;
        flip: a rotation (3x3) applied up in the air at P_a's place first."""
        ca, cb = P_a[:3, 3], P_b[:3, 3]
        k = [(P_a, None), (E.T((0, 0, up_a)) @ P_a, 0.9)]
        Pa_up = E.T((0, 0, up_a)) @ P_a
        if flip is not None:
            c = Pa_up[:3, :3] @ fr_c + Pa_up[:3, 3]
            Pf = E.T(tuple(c)) @ E.T((0, 0, 0), flip) @ E.T(tuple(-c)) @ Pa_up
            k.append((Pf, 3.2))
            Pa_up = Pf
        z_up = max(ca[2] + up_a, cb[2] + up_b)
        y_out = min(ca[1], -260.0)
        Pd = Pa_up.copy()
        Pd[:3, 3] += np.array([cb[0] - ca[0], y_out - ca[1], z_up - ca[2] - up_a])
        k.append((Pd, None))
        Pi = P_b.copy()
        Pi[:3, 3] += np.array([0.0, 0.0, up_b])
        k.append((Pi, None))
        k.append((P_b, 0.9))
        return k

    def lift_keys_out(P_a, P_b, up_a=40.0, up_b=60.0):
        """The reverse: out of the machine, side-step to the cart, down."""
        ca, cb = P_a[:3, 3], P_b[:3, 3]
        Pa_up = E.T((0, 0, up_a)) @ P_a
        Po = Pa_up.copy()
        Po[:3, 3] += np.array([0.0, min(cb[1], -260.0) - ca[1], 0.0])
        Pc = P_b.copy()
        Pc[:3, 3] += np.array([0.0, 0.0, up_b])
        return [(P_a, None), (Pa_up, 0.9), (Po, None), (Pc, None), (P_b, 0.9)]

    # ---- F-S1: the programs' stock on the cart, the risers and edge clamps on the table
    vf4.fixtures("frame_B", "frameT", 0, rots=[["x", 180]])
    R_B = GS.rot_of("frame_B")
    P1 = vf4.M_setup @ E.T((0, 0, 0), R_B)
    vf4.set(table_x=-100.0, door=1.0)
    spec0 = fr.spec()
    m0 = scn.obj_mesh(spec0)[0]
    v0 = np.asarray(m0.points, float)
    fr_c = (v0.min(0) + v0.max(0)) / 2
    P_cart1 = rest_on(spec0, scn, cart_c, CARTH, R_B)
    scn.set_obj("load", st @ P_cart1, spec0)
    # overview first: the station, the cart with the stock; the two people walk in from the aisle (lesson 5)
    for i in range(2):
        pw = (st @ np.r_[-3600.0 + 520.0 * i, -1300.0 - 260.0 * i, 0.0, 1.0])[:3]
        crew.place(i, pw[0], pw[1], -90.0)
    crew.show(1.0)
    cap0 = "The chamber frame on the VF-4: three setups from the posted programs"
    sub0 = ("F-S0 (not shown): the 5.5 in. plate sawn and its core cut out by waterjet, the stock the programs start "
            f"from; {kg_blank:.1f} kg here")
    for i in range(int(2.0 * FPS)):
        w.frame(scn, cam_wide, cap0, sub=sub0, who=[], step="F-S1", status="")
    # ---- lift 1: cart -> risers (they walk in, in the overview's camera, then the door's)
    pair_lift(w, scn, crew, "load", spec0, lift_keys(P_cart1, M_tab @ P1), kg_blank,
              f"Two people set the {kg_blank:.1f} kg stock on the risers",
              f"{kg_blank:.1f} kg, a reach of ~0.6 m into the machine; {rule}", "F-S1", cam_out, check_items=check,
              fronts=fronts)
    scn.hide_obj("load")
    vf4.part("frame part", spec0, P1)
    crew.show(0.0)                                   # at the cut: they have gone (arm A docks where they stood)
    # ---- arm A tightens the four edge clamps (the planned clip), then the doors shut, same camera
    play(w, scn, "vf4_clamps", cam_arm, hide=("frame part",))
    # round 9: arm A's MiR drives off (to the lathe) before the doors shut: they shut through its arm in round 8
    if (load("drive_vf4c_lathe") or {}).get("result", {}).get("ok", False):
        play(w, scn, "drive_vf4c_lathe", cam_arm, hide=("frame part",))
    else:
        scn.show_arm("A", False)
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
    scn.hide_obj("frame part")
    scn.set_obj("load", st @ M_tab @ P1, spec1)
    capO = "Doors open: the clamps off, two people take the part out"
    P_cart2 = rest_on(spec1, scn, cart_c, CARTH, R_B)
    for i in range(18):
        vf4.set(door=ease((i + 1) / 18))
        w.frame(scn, cam_out, capO, sub="arm A loosened the clamps first (its planned path run back; not shown)",
                who=["machine"], step="F-S1", status="pass", proc_s=1.5 / 18)
    for i in range(2):                               # they come back from the aisle, in the same camera
        pw = (st @ np.r_[-2900.0 + 450.0 * i, -1500.0 - 200.0 * i, 0.0, 1.0])[:3]
        crew.place(i, pw[0], pw[1], 60.0)
    pair_lift(w, scn, crew, "load", spec1, lift_keys_out(M_tab @ P1, P_cart2), kg1, capO,
              f"{kg1:.1f} kg after F-S1; {rule}", "F-S1", cam_out, check_items=check, fronts=fronts)
    # ---- cut: the risers out, the dummy-floor plate in; lift 2b turns the part over onto it
    vf4.fixtures("frame_A", "frameT", 0, rots=[])
    R_A = GS.rot_of("frame_A")
    P2 = vf4.M_setup @ E.T((0, 0, 0), R_A)
    capF = "Two people turn it over onto the dummy-floor plate for F-S2"
    m1_ = scn.obj_mesh(spec1)[0]
    hp_flip = {0: end_hands(m1_, P_cart2, -1, fz=0.5, fy=(0.4, 0.6)), 1: end_hands(m1_, P_cart2, 1, fz=0.5, fy=(0.4, 0.6))}
    # the turn over: 180 deg about the line between their hands (the load's x), up over the cart
    keys2 = lift_keys(P_cart2, M_tab @ P2, up_a=160.0, flip=E.Rx(180.0))
    pair_lift(w, scn, crew, "load", spec1, keys2, kg1, capF,
              f"{kg1:.1f} kg, turned 180 deg about the line between their hands; the 18 M4 screws from below (not "
              f"shown); {rule}", "F-S2", cam_out, check_items=check, fronts=fronts, hand_pts=hp_flip)
    scn.hide_obj("load")
    vf4.part("frame part", spec1, P2)
    for i in range(18):
        vf4.set(door=1.0 - ease((i + 1) / 18))
        w.frame(scn, cam_out, "Doors shut; cycle start", sub="the auto door (option), ~1.5 s", who=["machine"],
                step="F-S2", status="pass", proc_s=1.5 / 18)
    crew.show(0.0)                                   # at the cut to the inside view
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
    capC = "Two people set the frame and its plate on the 4th axis"
    vf4.set(door=1.0)
    # round 9: the turn from flat onto the platter is 90 deg about the machine's Y (the frame's floor to the platter);
    # the faces two people at the door hold (the frame's ends, along X) don't stay level through it, so the lift is
    # cut: they are seen stepping back from the door with the frame on the platter
    PERSON_RESULTS[f"F-S3: {capC}"] = dict(kg=round(kg_frame + kg_plate, 2), team_guideline_kg=round(TEAM_KG, 1),
                                           under_guideline=bool(kg_frame + kg_plate <= TEAM_KG), shown=False,
                                           caption=capC, why="a 90 deg turn about Y: not drawn (a cut)")
    for i in range(2):                               # at the cut from the inside view: at the open door, done
        pw = (st @ np.r_[(-330.0 if i == 0 else 330.0) + 0.0, -200.0, 0.0, 1.0])[:3]
        crew.place(i, pw[0], pw[1], HD[i])
    crew.show(1.0)
    scn.set_obj("load", st @ P_to3, spec2)
    for i in range(int(1.5 * FPS)):
        w.frame(scn, cam_out, capC, sub="the HRT210 indexed to A 90 for loading (left wall up); the frame on its plate "
                "turned 90 deg onto the platter and bolted through the opening (not shown)", who=["person"],
                step="F-S3", status="person")
    crew.step_back(w, cam_out, capC, f"frame {kg_frame:.1f} kg + MIC-6 plate {kg_plate:.1f} kg, turned 90 deg onto "
                   f"the platter and bolted through the opening (the lift and the bolting not shown); {rule}", "F-S3",
                   dist=600.0, n=24)
    scn.hide_obj("load")
    for n in vf4.sc.members("vf4/rotfix"):
        vf4.sc.alpha[n] = 1.0
    vf4.part("frame part", fr.spec(), P3, rot=True)
    for i in range(18):
        vf4.set(door=1.0 - ease((i + 1) / 18))
        w.frame(scn, cam_out, "Doors shut; cycle start", sub="the auto door (option), ~1.5 s", who=["machine"],
                step="F-S3", status="pass", proc_s=1.5 / 18)
    crew.show(0.0)                                   # at the cut to the inside view
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
        show_cart = [n for n in scn.sc.actors if n.startswith("cart/")]
        for n in show_cart:
            scn.sc.alpha[n] = 0.0                    # the cart was wheeled away with the frame
        play(w, scn, "vf4_floor_load", cam_arm, hide=("floor part",),
             sub="the finished frame is off the rotary (not shown); arm A sets the floor plate's 5.0 kg blank on the "
                 "parallels")
        scn.hide_obj("floor part")
        vf4.part("floor part", fl.spec(), PF)
        if (load("drive_vf4f_lathe") or {}).get("result", {}).get("ok", False):
            play(w, scn, "drive_vf4f_lathe", cam_arm, hide=("floor part",))
        else:
            scn.show_arm("A", False)
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
    lp = E.st10(door=1.0, jaw_open=6.0)[0]
    shut_dx = E.ST10["panel_w"] - 20.0                 # the door slides right by this to shut (equipment.st10)
    for n_ in ("door", "door window"):                 # round 9: the door its own group, so it can shut and open
        q_ = lp[n_]
        lp[n_] = E.Part(q_.mesh, q_.color, q_.opacity, q_.collide, q_.M, "door")
    scn.add_parts("lathe", lp, Mst("lathe"))

    def lathe_door(u):
        """0 open .. 1 shut"""
        for n_ in ("door", "door window"):
            scn.sc.gmat[f"lathe/{n_}"] = Mst("lathe") @ E.T((shut_dx * u, 0.0, 0.0)) @ lp[n_].M
    scn.drop_context("saw")
    scn.add_parts("saw", E.s20a(head=1.0)[0], Mst("saw"))
    cam_v = cam_at("vf4", (-1300, -2300, 2200), (0, 450, 1050))
    play(w, scn, "vf4_vise_part", cam_v)
    # round 9: arm A's MiR drives on to the lathe in the same shot (pivot, drive, pivot; shop_clips.clip_drive, swept
    # with FCL), so the doors can shut behind it without a cut
    dc = load("drive_vf4_lathe")
    drove = dc is not None and (dc.get("result") or {}).get("ok", False)
    if drove:
        play(w, scn, "drive_vf4_lathe", cam_v)
        cam_v2 = cam_v
    else:
        scn.show_arm("A", False)                 # at the cut: arm A has driven off (its arm was in the door's path)
        cam_v2 = cam_at("vf4", *CAM_VF4_ARM)
    # the bracket cut in the vise: it has no posted program, so (round 8) no tool path is drawn: the doors shut and
    # the machine clock runs through the vise class's ~20 min, seen from outside in the same camera
    n_v = int(5 * FPS)
    for i in range(n_v):
        vf4.set(door=1.0 - ease(min(1.0, (i + 1) / 18)))
        w.frame(scn, cam_v2, "The bracket cut in the vise, doors shut",
                sub="time-lapse of about 20 min (setup_plan.json's vise class); no program is posted for it, so no tool "
                    "path is drawn", who=["machine"], step="vise class", status="pass",
                proc_s=(1.5 / 18) if i < 18 else (20 * 60.0 - 1.5) / (n_v - 18))
    if not drove:
        scn.show_arm("A", False)
    vf4.set(z=0.0, table_y=0.0)                  # the doors stay shut: the bracket is being cut
    play(w, scn, "saw_bar", cam_at("saw", (-2400, -2500, 2200), (-1300, 450, 900)))
    scn.show_arm("B", False)
    cam_l = cam_at("lathe", (-1600, -2300, 2000), (100, 300, 1000))
    play(w, scn, "lathe_slug", cam_l)
    # round 9 (P1): the lathe runs with its door shut (no posted program for the turned parts: only the clock), then
    # arm A takes the part out along the loading path run back (so checked as it was planned); the part drawn turned
    n_t = int(5 * FPS)
    for i in range(n_t + 36):
        if i < 18:
            lathe_door(ease((i + 1) / 18))
        elif i >= n_t + 18:
            lathe_door(1.0 - ease((i - n_t - 17) / 18))
        mid = 18 <= i < n_t + 18
        w.frame(scn, cam_l, "The slug turned, door shut" if i < n_t + 18 else "Door open: the part is done",
                sub="the lathe class's ~5 min a setup (shop_summary.json); no program is posted for the turned parts, "
                    "so no tool path is drawn" if mid or i < 18 else "the ST-10's auto door (option)",
                who=["machine"], step="lathe class", status="pass",
                proc_s=(5 * 60.0 - 3.0) / n_t if mid else 1.5 / 18)
    turned = dict(kind="steps", steps=[(0.0, 46.0, 27.0), (46.0, 66.0, 25.4), (66.0, 92.0, 19.0), (92.0, 100.0, 12.0)],
                  color="#cfd4d9")
    play(w, scn, "lathe_slug", cam_l, rev=True, specs={"bar slug": turned},
         caption="Arm A takes the turned part out: the loading path run back",
         sub="the planned, FCL-checked load reversed (the part is smaller than the slug it was cut from); the profile "
             "drawn is illustrative")
    lb = load("lathe_big")
    if lb is not None and (lb.get("result") or {}).get("ok", False):
        scn.add_parts("lathe", E.st10(door=1.0, jaw_open=33.0, jaw_deg=30.0)[0], Mst("lathe"))   # jaws opened, oriented
        play(w, scn, "lathe_big", cam_at("lathe", (1500, -2300, 2100), (100, 300, 1000)))   # a cut: its own camera
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
    scn.add_parts("wash", E.wash_deburr(basket=False)[0], Mst("wash"))   # round 9: the basket is the wash clip's object
    wc = load("wash")                                  # ... in the tank from the start, where the clip picks it up
    if wc is not None:
        for o, M in wc["frames"][0]["objs"].items():
            scn.set_obj(o, M, wc["objects"].get(o))
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
        w.frame(scn, cam_at("tig", (-3600, -4300, 3600), (0, 400, 900)), "Honing the 50.80 mm bore is sent out",
                sub="outsourced: a hone shop, about 10 working days (estimate) for one tube", who=["outsourced"],
                step="hone", status="pass", proc_s=1.0 / FPS, add=dict(outsourced_d=10.0 / (4 * FPS)))
    play(w, scn, "deburr", cam_at("wash", (1600, -1800, 2000), (450, 340, 1050)))
    # round 9: arm A's MiR drives on to the measuring station in the same shot (pivot, drive, pivot; FCL-swept)
    if (load("drive_deburr_measure") or {}).get("result", {}).get("ok", False):
        play(w, scn, "drive_deburr_measure", cam_at("wash", (1600, -1800, 2000), (450, 340, 1050)))
    else:
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


def plate_stand(top=900.0):
    """A narrow receiving stand for heavy stock (our estimate, not a catalogue item): two 50 mm square rails 120 mm apart
    on a welded frame, top at `top`, 600 mm long, so two people can stand at a block's ends and hold it by its sides."""
    rails = [E.box(x - 25, x + 25, -300, 300, top - 50, top) for x in (-60.0, 60.0)]
    legs = [E.box(x - 20, x + 20, y - 20, y + 20, 0, top - 50) for x in (-60.0, 60.0) for y in (-270.0, 270.0)]
    feet = [E.box(-85, 85, y - 25, y + 25, 0, 30) for y in (-270.0, 270.0)]
    return {"plate stand": E.Part(E.merge(rails + legs + feet), E.C["stand"])}


def chapter_29():
    """The stock (round 8, the lead's ask after Sterling's "Probably just a two person job for that part"): two people
    carry the chamber frame's plate as delivered, 13 x 9.5 x 5.5 in. 6061-T651, from a receiving stand onto a narrow
    cart, which takes it to the waterjet for its core. One fixed camera.

    Round 9 (round 8's audit: their gloves and coats inside the plate, over 100 mm; their legs in the cart): they hold it
    by its two ends as people.carry() stands them (each outside one end, facing it, the hands on the sides beside the
    end; the body 30 mm off the plate), so the stand and the cart, both narrower than the gap between them, pass between
    their feet; they side-step it to the cart, their feet locked (people.py's Gait)."""
    w = Writer("29-stock", "The stock: two people carry the 5.5 in. plate")
    scn = Shop()
    scn.add_person2()
    context_vf4(scn)
    crew = Crew(scn)
    # the scene frame: the receiving area (station y 520, as round 8's lift table), +y towards the wall; the aisle (and
    # the cart) at -y
    M29 = Mst("receiving") @ E.T((0.0, 520.0, 0.0))
    top = 900.0
    scn.add_parts("stand29", plate_stand(top), M29)
    cart_y = -1450.0
    scn.add_parts("cart29", E.bench(CART["w"], CART["d"], CART["h"]), M29 @ E.T((0.0, cart_y - CART["d"] / 2, 0.0)))
    L, W_, H = 13 * E.INCH, 9.5 * E.INCH, 5.5 * E.INCH
    kg = L * W_ * H * 2.70e-6                                        # 6061: 2.70 g/cm3
    kg15 = 15 * E.INCH * W_ * H * 2.70e-6
    spec = dict(kind="box", b=(-L / 2, L / 2, -W_ / 2, W_ / 2, 0.0, H), color="#c9ced3")
    P_from = E.T((0.0, 0.0, top))
    P_to = E.T((0.0, cart_y, CART["h"]))
    within = "within it, just" if kg <= TEAM_KG else "over it"
    cap = f"Two people carry the frame's plate: {kg:.1f} kg"
    sub = (f"13 x 9.5 x 5.5 in. 6061-T651 as delivered; 2/3 x (23 + 23) = {TEAM_KG:.1f} kg two-person guideline "
           f"(NIOSH, HSE L23): {within} (a 15 in. plate, {kg15:.1f} kg, would be over)")
    cam = [tuple((M29 @ np.r_[2700.0, -3600.0, 2700.0, 1.0])[:3]), tuple((M29 @ np.r_[0.0, -720.0, 850.0, 1.0])[:3]),
           (0, 0, 1)]                                            # from the aisle, high and to one side: both people,
                                                                 # the stand, the carry, the cart
    for i in range(2):
        pw = (M29 @ np.r_[-1500.0 + 3000.0 * i, -2600.0, 0.0, 1.0])[:3]
        crew.place(i, pw[0], pw[1], 0.0)
    crew.show(1.0)
    keys = [(P_from, None), (E.T((0.0, 0.0, top + 70.0)), 1.0), (E.T((0.0, cart_y, CART["h"] + 70.0)), None),
            (P_to, 1.0)]
    res = carry_lift(w, scn, crew, "plate", spec, keys, kg, cap, sub, "stock", cam, ends=("-x", "+x"), M_st=M29,
                     grip="side", inset=28.0, z_below_top=32.0)
    cap2 = "Next: its core cut out by waterjet, off site"
    sub2 = ("setup_plan.json F-S0: BYU's ME prototyping lab (the robot shop has no waterjet); the 274 x 184 mm core "
            "out as one slug, then F-S1 on the VF-4")
    for i in range(int(3.5 * FPS)):
        w.frame(scn, cam, cap2, sub=sub2, who=["person"], step="stock", status="person")
    del res
    return w.close()


CHAPTERS = {"20": chapter_20, "29": chapter_29, "30": chapter_30, "31": chapter_31, "32": chapter_32}


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
    if PERSON_RESULTS and EVERY == 1 and not STILL and not ONLY:     # round 8: the two-person lifts replace round 7's jib lifts
        prev_l = {}
        if pj.exists():
            prev_ = json.loads(pj.read_text())
            if "guideline" in prev_:                         # the round-8 file: keep the other chapters' lifts
                prev_l = prev_.get("lifts", {})
        prev_l.update(PERSON_RESULTS)
        pj.write_text(json.dumps(dict(
            what="chapters 29 and 30's two-person lifts (shop_chapters.team_lift): the load's mass against a two-person "
                 "guideline, the hands' largest gap to their grip points on the load (mm), and, at the VF-4, the load's "
                 "path against the machine (FCL; clear_mm, contact)",
            guideline=dict(single_person_kg=NIOSH_KG, team_factor=round(TEAM_FACTOR, 3), team_of_two_kg=round(TEAM_KG, 1),
                           sources=["NIOSH, Applications Manual for the Revised NIOSH Lifting Equation (DHHS (NIOSH) "
                                    "Publication No. 94-110, 1994): load constant 23 kg",
                                    "HSE L23, Manual Handling Operations Regulations 1992, guidance on team handling: "
                                    "a team of two can handle about two-thirds of the sum of their capabilities"]),
            lifts=prev_l), indent=1, default=str))
    if GFRAMES and EVERY == 1 and not STILL and not ONLY:   # every drawn cutter position: its program, line and time
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
