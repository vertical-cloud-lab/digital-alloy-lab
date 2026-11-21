"""Run the two-arm robotic build of the M50 desktop LPBF on the model and write the results (issue #260, PR #266).

One command re-runs everything on whatever cad/ holds (the chamber can change under it):
    OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/assembly/run_assembly.py [--only=M,C,F] [--no-render]
Writes analysis/out/assembly/: results.json, steps.md (the step table), sequence.json (for render_build.py), seals.json,
forces.json, and PNG/GIF renders (render_assembly.py, xvfb).

For every step of sequence.py:
  1. Part sweep: the moving part goes along its insertion path against everything already in its sub-assembly:
     analysis/ops/checks.path_check (FCL on 0.1 mm meshes; a contact only blocks if manifold3d finds > 0.5 mm3 shared and
     OpenCascade's exact boolean confirms it). Gives the smallest gap along the path and what blocks it.
  2. Arms: the actor's MiR docks at the station (it may slide along the bench), its TCP follows the part's insertion path
     (IK at every 3 mm, one branch held throughout, each frame checked with FCL on meshes: links, tool, D405, tool changer
     and held part against the cell, every part present and the other arm), and the move from its last pose to the start
     of the path is planned with cell.Checker.plan (straight joint line, else RRT-Connect, 1.5 deg edge checks). The
     part and the tool may touch the part's own seat only up to 1.5 mm deep (byu-vcl PR 318's round-11 rule).
  3. Screws: for each screw the screwdriver (with the screw on its bit) goes on the screw's axis; 12 roll angles x every
     IK branch are tried; the drive from the hole's mouth to the seat is checked frame by frame, then the move there planned.
  4. Flips and two-arm carries: the part's whole path (lift, turn, move, lower) with both arms' IK at every frame.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import sys
import time
import traceback

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cell2 as K  # noqa: E402  (puts ../robot, ../ops, ../../cad on sys.path)
import cell as C  # noqa: E402
import checks as CK  # noqa: E402
import sequence as SQ  # noqa: E402
import tooling as TL  # noqa: E402
from cell import Tm, inv, rot, Group, Body  # noqa: E402

OUT = HERE.parent / "out" / "assembly"
CAD = HERE.parents[1] / "cad"
DS = 3.0                       # mm between frames along a Cartesian path
JUMP = math.radians(20.0)      # a bigger joint step between frames is a branch flip: not a continuous path
PLAN_ITERS = int(os.environ.get("ASM_PLAN_ITERS", "1500"))
SCREW_PLAN_ITERS = int(os.environ.get("ASM_SCREW_PLAN_ITERS", "500"))
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.1f} s]", *a, flush=True)


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def frame_zx(z, x, p):
    z = unit(z)
    x = np.asarray(x, float) - np.dot(x, z) * z
    x = unit(x)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, np.cross(z, x), z, p
    return M


# ================================================================================================ the run state
class Run:
    def __init__(self, module="M50"):
        log("building the model and the ops scene")
        self.sc = CK.Scene(str(CAD), module, verbose=False)
        self.M = self.sc.M
        self.split_parts()
        self.cl = K.Cell(self.sc)
        self.asm = {}                 # sub-assembly -> set of object indices
        self.grp_of = {}              # object -> sub-assembly
        self.phase_of = {}            # sub-assembly -> phase
        self.done_screws = set()
        self.q = {"A": self.cl.A.park_q(), "B": self.cl.B.park_q()}
        self.rows = []
        self.frames = {}              # step id -> snapshot of the tightest frame, for the renders
        self.seq_json = []
        self.module_set = None

    # ---- objects
    def split_parts(self):
        """Parts drawn as one compound of several solids that the arms place one at a time: one object per solid."""
        sc = self.sc
        self.split = {}
        for key in ("Chamber legs", "Optics bridge posts", "Macor standoff rings", "Radiation shields"):
            i0 = sc.find(key, fasteners=False)[0]
            p = sc.parts[sc.objs[i0]["part"]]
            new = []
            for k, s in enumerate(p.shape.Solids()):
                V, F = CK.tess(s)
                sc.objs.append(dict(name=f"{p.name.split(' (')[0]} #{k + 1}", part=sc.objs[i0]["part"], item=None, key=None, pn="",
                                    shape=s, kind="part", V=V, F=F, bvh=CK.bvh(V, F), man=None))
                new.append(len(sc.objs) - 1)
            sc.objs[i0]["V"] = None            # the compound itself is no longer used
            self.split[key] = new
        sc.n = len(sc.objs)

    def resolve(self, keys, exclude=(), moved=False):
        sc = self.sc
        out = []
        for k in keys:
            if k == "@module":
                out += [i for i in self.module_objs() if i not in out]
            elif k == "@legs":
                out += self.split["Chamber legs"]
            elif k == "@posts":
                out += self.split["Optics bridge posts"]
            elif k in ("Macor standoff", "Radiation shields"):
                out += [i for i in self.split["Macor standoff rings" if k == "Macor standoff" else "Radiation shields"] if i not in out]
            elif k == "@chamberset":
                out += sorted(self.asm.get("chamber", ()))
            else:
                out += [i for i in sc.find(k, exclude=tuple(exclude)) if i not in out]
        out = [i for i in out if sc.objs[i]["V"] is not None]
        if not moved:
            out = [i for i in out if i not in self.grp_of]
        return out

    def module_objs(self):
        if self.module_set is None:
            self.module_set = [i for i in self.sc.group("module") if self.sc.objs[i]["V"] is not None and self.sc.objs[i].get("kind") != "tool"]
        return self.module_set

    def add(self, idx, grp, phase, state=None):
        for i in idx:
            old = self.grp_of.get(i)
            if old is not None and old != grp:
                self.asm[old].discard(i)
            self.asm.setdefault(grp, set()).add(i)
            self.grp_of[i] = grp
        self.phase_of[grp] = phase
        self.cl.put(idx, self.cl.T_phase(phase), state)

    def merge(self, src, dst):
        if src not in self.asm:
            return
        idx = sorted(self.asm.pop(src))
        for i in idx:
            self.grp_of[i] = dst
        self.asm.setdefault(dst, set()).update(idx)
        self.cl.put(idx, self.cl.T_phase(self.phase_of.get(dst, "upright")))

    def held_body(self, idx, name, state=None, extra=None):
        """One Body of the objects idx, vertices in the machine frame (at `state`), plus extra (v, f) in the same frame."""
        st = {} if state is None else state
        vs, fs, n = [], [], 0
        for i in idx:
            o = self.sc.objs[i]
            M = self.sc.pose(i, st)
            vs.append(o["V"] @ M[:3, :3].T + M[:3, 3])
            fs.append(o["F"] + n)
            n += len(o["V"])
        for v, f in (extra or []):
            vs.append(v)
            fs.append(f + n)
            n += len(v)
        V, F = np.vstack(vs), np.vstack(fs).astype(np.int32)
        if len(F) > 60000:
            V, F = C.decimate(V, F, 60000)
        return Body(name, V, F, kind="held", color="#e0a040")

    # ---- arms
    def arm(self, n):
        return self.cl.A if n == "A" else self.cl.B

    def other(self, n):
        return "B" if n == "A" else "A"

    def set_tool(self, n, tool, long_bit=None, tip_d=None):
        a = self.arm(n)
        if tool == "gripper+caps":
            caps, _ = TL.mesh("ring_caps")
            a.set_tool("gripper", caps=dict(name="ring caps", meshes=caps, grasp_z=31.9, inner_x=23.0, color="#d9b23a"))
        elif tool in ("screwdriver", "nutrunner", "nutrunner_angle"):
            a.set_tool(tool, extra_bit=float(long_bit or 0.0), tip_d=tip_d)
        elif tool in ("vacuum", "nozzle", "roller", "roller_n"):
            a.set_tool(tool)
        else:
            a.set_tool("gripper")

    def docks_for(self, x_world):
        return sorted(K.DOCKS.values(), key=lambda d: abs(d - x_world))[:3]

    def dock(self, n, x):
        if self.cl.dock[n] != x:
            self.cl.move_mir(n, x)
            self.q[n] = self.arm(n).park_q()
        self.arm(n).place(self.q[n])

    # ---- Cartesian path with one IK branch, checked frame by frame
    def follow(self, n, Ts, close, allow, seeds=None, exclude=(), dist_every=6):
        """Ts: list of TCP poses (world). Returns dict(ok, qs, hit, at, min_d, with)."""
        a = self.arm(n)
        chk = K.checker(self.cl, n, exclude)
        first = a.ik_all(Ts[0], seed=self.q[n])
        if seeds:
            first = seeds + first
        best = None
        for q0 in first[:10]:
            qs, prev, ok, hit, at = [], q0, True, None, None
            for k, T in enumerate(Ts):
                sols = a.ik_all(T, seed=prev)
                if not sols:
                    ok, hit, at = False, "no IK (out of reach or joint limit)", k
                    break
                q = sols[0]
                if k and np.abs(q - prev).max() > JUMP:
                    ok, hit, at = False, "IK branch flip (wrist or elbow passes a singularity)", k
                    break
                c = chk.collisions(q, close, allow, first=True)
                if c:
                    x = c[0]
                    ok, hit, at = False, f"{x[0]} hits {x[1]}" + (f" ({x[2]} mm deep)" if isinstance(x[2], float) else ""), k
                    break
                qs.append(q)
                prev = q
            score = (ok, len(qs))
            if best is None or score > best[0]:
                best = (score, qs, hit, at)
            if ok:
                break
        if best is None:
            return dict(ok=False, qs=[], hit="no IK at the start pose", at=0, min_d=None, with_=None)
        (ok, _), qs, hit, at = best
        md, mw = math.inf, None
        if qs:
            for k in list(range(0, len(qs), dist_every)) + [len(qs) - 1]:
                a.place(qs[k], close)
                rob = Group(list(a.grip.values()) + list(a.caps.values()) + ([a.held[0]] if a.held else []) +
                            [a.links["wrist3"], a.links["wrist2"], a.links["wrist1"], a.links["forearm"]])
                d, x, y = C.group_distance(rob, chk.sc.world, margin=25.0)
                if d < md and y is not None and (("held", y.name) not in allow and ("tool", y.name) not in allow):
                    md, mw = d, f"{x.name.split('/')[-1]} to {y.name[:50]}"
        return dict(ok=ok, qs=qs, hit=hit, at=at, min_d=None if md == math.inf else round(float(md), 1), with_=mw)

    def plan_to(self, n, q_goal, close, allow=frozenset(), exclude=()):
        chk = K.checker(self.cl, n, exclude)
        path, info = chk.plan(self.q[n], q_goal, close, allow=allow, iters=PLAN_ITERS)
        return path, info

    def snapshot(self, sid, n=None):
        A, B = self.cl.A, self.cl.B
        snap = dict(present={i: self.cl.where[i].tolist() for i in self.cl.where},
                    arms={k: dict(q=list(map(float, self.arm(k).q)), close=float(self.arm(k).close), tool=self.arm(k).tool_name,
                                  dock=self.cl.dock[k], caps=bool(self.arm(k).caps),
                                  held=None if self.arm(k).held is None else dict(v=None, name=self.arm(k).held[0].name,
                                                                                    M=self.arm(k).held[0].M.tolist()))
                          for k in ("A", "B")})
        self.frames[sid] = snap
        self.held_meshes = getattr(self, "held_meshes", {})
        for k in ("A", "B"):
            h = self.arm(k).held
            if h is not None:
                self.held_meshes[h[0].name] = (h[0].v, h[0].f)


# ================================================================================================ grasps
def auto_grasp(run, idx, T, d_w, state, tool):
    """Grasp frame (world) on the seated part: the tool comes from the side the part leaves by (d_w, world), fingers
    across its narrowest extent there."""
    sc = run.sc
    V = np.vstack([(sc.objs[i]["V"] @ (T @ sc.pose(i, state))[:3, :3].T + (T @ sc.pose(i, state))[:3, 3]) for i in idx])
    d = unit(d_w)
    s = V @ d
    smax = float(s.max())
    ext_d = float(smax - s.min())
    inset = min(14.0, 0.5 * ext_d) if tool not in ("vacuum", "nozzle") else 0.0
    sl = V[s > smax - max(2 * inset, 3.0)]
    c = 0.5 * (sl.min(0) + sl.max(0))
    c = c - d * (np.dot(c, d) - (smax - inset))
    z = -d
    cands = [unit(e) for e in np.eye(3) if abs(np.dot(e, z)) < 0.5]
    best = None
    for e in cands:
        w = float(np.ptp(sl @ e))
        if best is None or w < best[1]:
            best = (e, w)
    x, w = best
    return frame_zx(z, x, c), w, inset


def given_grasp(g, T):
    p = (T @ np.r_[np.asarray(g["point"], float), 1.0])[:3]
    z = T[:3, :3] @ np.asarray(g["z"], float)
    x = T[:3, :3] @ np.asarray(g["x"], float)
    return frame_zx(z, x, p)


def close_for(run, n, width, internal=False):
    a = run.arm(n)
    if a.tool_name != "gripper":
        return 0.0
    if internal:
        return a.close_for_gap(min(80.0, width))
    return a.close_for_gap(max(1.0, min(84.0, width)))


def contacts_at_seat(run, body, exclude=()):
    w = run.cl.world("A", exclude, other=False)
    g = Group([body])
    names = set()
    for x, y in C.group_hits(g, w):
        if y.kind in ("machine", "fixture"):
            names.add(y.name)
    return names


# ================================================================================================ steps
def path_list(run, st, idx):
    if st["path"] == "explode":
        lead = next((i for i in idx if run.sc.objs[i]["item"] is None), idx[0])
        ex = run.sc.parts[run.sc.objs[lead]["part"]].explode
        return [(0.0, 0.0, 0.0), tuple(float(v) for v in ex)]
    return [tuple(float(v) for v in p) for p in st["path"]]


def sweep(run, st, idx, path, state, rot_deg=None, present=None):
    sc = run.sc
    grp = st["grp"]
    pres = sorted(present if present is not None else run.asm.get(grp, set()))
    pres = [i for i in pres if i not in idx]
    if not pres:
        return dict(ok=True, min_gap=None, gap_with=None, note="nothing else in the sub-assembly yet")
    if rot_deg:
        pre = CK.rot((0, 0, 1), rot_deg)
        orig = sc.pose

        def posed(i, s, _o=orig):
            m = _o(i, s)
            return pre @ m if i in idx else m
        sc.pose = posed
        try:
            return CK.path_check(sc, state, pres + idx, idx, path, ds=1.0)
        finally:
            sc.pose = orig
    return CK.path_check(sc, state, pres + idx, idx, path, ds=1.0)


def dense(path, ds=DS):
    pts = [np.asarray(p, float) for p in path]
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = np.linalg.norm(b - a)
        n = max(1, int(math.ceil(L / ds)))
        out += [a + (b - a) * k / n for k in range(1, n + 1)]
    return out


def arm_place(run, st, idx, path, state, actor, tool, holdname, grasp=None, extra=None, internal=False, rot_deg=None):
    """The actor carries objects idx along the insertion path (reverse of `path`) to their seat; returns a result dict."""
    sc, cl = run.sc, run.cl
    T = cl.T_phase(st["phase"])
    if rot_deg:
        T_obj = T @ Tm(rot((0, 0, 1), rot_deg))
    else:
        T_obj = T
    d_w = T[:3, :3] @ unit(np.asarray(path[1], float) - np.asarray(path[0], float)) if len(path) > 1 else np.array([0, 0, 1.0])
    if grasp:
        G = given_grasp(grasp, T_obj)
        width, inset = float(grasp.get("width", 40.0)), 0.0
    else:
        G, width, inset = auto_grasp(run, idx, T_obj, d_w, state, tool)
    if tool.startswith("gripper") and not internal and width > 84.0:
        return dict(ok=False, why=f"part {width:.0f} mm across at the grasp: wider than the 2F-85's 85 mm stroke")
    body = run.held_body(idx, holdname, state, extra)
    # seat contacts (allowed up to 1.5 mm, PR 318) with the held part in place
    body.place(T_obj)
    dest = contacts_at_seat(run, body, exclude=idx)
    allow = frozenset([("held", n) for n in dest] + [("tool", n) for n in dest])
    off = inv(G) @ T_obj                      # TCP -> held body's (machine) frame
    best = None
    x_target = float(G[0, 3])
    for dk in run.docks_for(x_target):
        run.dock(actor, dk)
        a = run.arm(actor)
        run.set_tool(actor, tool)
        a.hold(body, off)
        close = close_for(run, actor, width, internal)
        a.close = close
        offs = dense(path[::-1])
        Ts = [T_obj @ Tm(p=o) @ inv(T_obj) @ G for o in offs]
        fr = run.follow(actor, Ts, close, allow, exclude=idx)
        if (not fr["ok"] and tool.startswith("gripper") and fr.get("at") and fr["at"] >= 2 and " hits " in (fr["hit"] or "")
                and (len(offs) - fr["at"]) * DS <= 45.0):
            # release short of the seat, close the fingers and push the part home on its back face (pick-insert-push)
            k = fr["at"] - 1
            z_tip = fingertip_reach(a)
            Gb = G @ Tm(p=(0.0, 0.0, -inset))                     # the part's back face, on the tool axis
            close_p = 1.0
            Tp = [T_obj @ Tm(p=o) @ inv(T_obj) @ Gb @ Tm(p=(0.0, 0.0, -(K.TC_H + z_tip))) @ a.tcp_local(close_p) for o in offs[k:]]
            a.hold(body, inv(Gb @ Tm(p=(0.0, 0.0, -(K.TC_H + z_tip))) @ a.tcp_local(close_p)) @ T_obj)
            fr2 = run.follow(actor, Tp, close_p, allow, exclude=idx)
            a.hold(body, off)
            if fr2["ok"]:
                fr = dict(ok=True, qs=fr["qs"] + fr2["qs"], hit=None, at=None, min_d=fr2["min_d"] if fr["min_d"] is None else
                          min(x for x in (fr["min_d"], fr2["min_d"]) if x is not None), with_=fr2["with_"] or fr["with_"],
                          push_mm=round((len(offs) - k) * DS, 0))
            elif st.get("drop_ok") and (len(offs) - fr["at"]) * DS <= float(st.get("drop_mm", 12.0)):
                fr = dict(ok=True, qs=fr["qs"], hit=None, at=None, min_d=fr["min_d"], with_=fr["with_"],
                          drop_mm=round((len(offs) - fr["at"]) * DS, 0))
            else:
                fr["hit"] = f"{fr['hit']}; pushed home instead, but {fr2['hit']}"
        if (not fr["ok"] and tool == "nozzle" and st.get("drop_ok") and fr.get("at") and " hits " in (fr["hit"] or "")
                and (len(offs) - fr["at"]) * DS <= float(st.get("drop_mm", 12.0))):
            # the nozzle lets go above the seat and the part drops the rest of the way onto its guide pin
            fr = dict(ok=True, qs=fr["qs"], hit=None, at=None, min_d=fr["min_d"], with_=fr["with_"],
                      drop_mm=round((len(offs) - fr["at"]) * DS, 0))
        res = dict(dock=dk, follow=fr)
        if fr["ok"]:
            # plan from where the arm is to the start of the path, carrying the part
            a.place(run.q[actor], close)
            path_q, info = run.plan_to(actor, fr["qs"][0], close, allow=allow, exclude=idx)
            res["plan"] = info
            res["plan_ok"] = path_q is not None
            if path_q is not None:
                best = res
                break
        if best is None or (res["follow"]["ok"] and not best["follow"]["ok"]) or \
                len(res["follow"]["qs"]) > len(best["follow"]["qs"]):
            best = res
    a = run.arm(actor)
    fr = best["follow"]
    if fr["qs"]:
        a.place(fr["qs"][-1], a.close)
        run.q[actor] = fr["qs"][-1]
    ok = fr["ok"] and best.get("plan_ok", False)
    why = "" if ok else (fr["hit"] if not fr["ok"] else f"approach: {best.get('plan', {}).get('reason', '?')}")
    if not fr["ok"] and fr["at"] is not None:
        why += f" at {fr['at'] * DS:.0f} mm along the insertion"
    return dict(ok=ok, why=why, dock=best["dock"], min_d=fr["min_d"], min_with=fr["with_"], dest=sorted(dest)[:4],
                planned=best.get("plan", {}).get("planned"), waypoints=best.get("plan", {}).get("waypoints"),
                grasp_width=round(width, 1), push_mm=fr.get("push_mm"), drop_mm=fr.get("drop_mm"))


_TIP = {}


def fingertip_reach(a):
    """How far the closed 2F-85's fingertips reach past the tool-changer face along the tool axis (mm)."""
    if "z" not in _TIP:
        G = __import__("ur_arm").gripper_fk(1.0)
        z = 0.0
        for k in ("left_finger_tip", "right_finger_tip"):
            b = a.stock.get(k)
            if b is None:
                continue
            v = b.v @ G[k][:3, :3].T + G[k][:3, 3]
            z = max(z, float(v[:, 2].max()))
        _TIP["z"] = z
    return _TIP["z"]


def retreat(run, n, dist=60.0, near=(), names=()):
    """Release and back the tool off along its axis; the arm then counts as at that pose. `near`: objects the tool may
    still touch at the start (the part it just let go of), up to the 1.5 mm audit depth."""
    a = run.arm(n)
    a.release()
    a.place(run.q[n])
    T = a.tcp(run.q[n])
    Ts = [T @ Tm(p=(0, 0, -s)) for s in np.linspace(0, dist, 7)]
    allow = frozenset([("tool", run.sc.label(i)) for i in near] + [("tool", nm) for nm in names])
    fr = run.follow(n, Ts, a.close, allow, dist_every=99)
    if fr["qs"]:
        run.q[n] = fr["qs"][-1]
    return fr["ok"]


def go_park(run, n):
    a = run.arm(n)
    a.release()
    path, info = run.plan_to(n, a.park_q(), a.close)
    if path is not None:
        run.q[n] = a.park_q()
    else:
        run.q[n] = a.park_q()          # counted as a failed return; the next step starts from park anyway
    a.place(run.q[n])
    return path is not None


def do_place(run, st, row):
    sc = run.sc
    idx = run.resolve(st["keys"], st.get("exclude", ()), st.get("moved", False))
    if not idx:
        row.update(sweep="?", arm="?", why="no object matched")
        return
    state = dict(st.get("state", {}))
    units = [[i] for i in idx] if (st.get("per_solid") or st.get("per_part")) else [idx]
    if st.get("order") == "zdesc":          # build outward from the heater block (machine z decreasing)
        units.sort(key=lambda u: -float((sc.objs[u[0]]["V"] @ sc.pose(u[0], {})[:3, :3].T + sc.pose(u[0], {})[:3, 3])[:, 2].max()))
    if st.get("per_part"):
        by = {}
        for i in idx:
            by.setdefault(sc.objs[i]["part"], []).append(i)
        units = list(by.values())
    if st.get("merge"):
        run.merge(st["merge"], st["grp"])
    sw_all, arm_all, gaps, dmins, why, docks = [], [], [], [], [], set()
    for u in units:
        path = path_list(run, st, u)
        sw = sweep(run, st, u, path, state, st.get("rot"))
        sw_all.append(sw["ok"])
        if sw.get("min_gap") is not None:
            gaps.append((sw["min_gap"], sw.get("gap_with")))
        if not sw["ok"]:
            why.append(f"sweep: {sc.short(u[0])} blocked by {sw['blocked_by'][:50]} after {sw['at_s']} mm")
        actor = st.get("actor", "A")
        tool = st.get("tool", "gripper")
        extra = None
        if st.get("bullet"):
            (bv, bf), _ = TL.mesh("rod_bullet")
            # bullet on the rod's lower end: machine (0, 0, -117), pointing -z
            Mb = Tm(p=(0.0, 0.0, -117.0)) @ K.Rx(180.0)
            extra = [(bv @ Mb[:3, :3].T + Mb[:3, 3], bf)]
        r = arm_place(run, st, u, path, state, actor, tool, f"held:{st['id']}:{sc.short(u[0])[:30]}", st.get("grasp"),
                      extra, internal=bool(st.get("grasp", {}).get("internal")), rot_deg=st.get("rot"))
        arm_all.append(r["ok"])
        if not r["ok"]:
            why.append(f"arm {actor}: {r['why']}")
        if r.get("min_d") is not None:
            dmins.append((r["min_d"], r.get("min_with")))
        if r.get("push_mm"):
            why.append(f"released {r['push_mm']:.0f} mm short and pushed home with the closed fingers")
        if r.get("drop_mm"):
            why.append(f"released {r['drop_mm']:.0f} mm above its seat and let drop over its guide")
        if st.get("force"):
            row["force_pose"] = force_check(run, st, actor, path)
        docks.add(r.get("dock"))
        run.snapshot(f"{st['id']}:{len(arm_all)}")
        # seat it, then either keep holding it (another arm drives its screws) or let go
        if st.get("hold_for"):
            run.add(u, st["grp"], st["phase"], state)
            sub = hold_and_drive(run, st, u, actor)
            arm_all.append(sub["ok"])
            if not sub["ok"]:
                why.append(sub["why"])
            retreat(run, actor, near=u)
        else:
            retreat(run, actor)
            run.add(u, st["grp"], st["phase"], state)
        go_park(run, actor)
    gmin = min(gaps) if gaps else (None, None)
    dmin = min(dmins) if dmins else (None, None)
    row.update(sweep="PASS" if all(sw_all) else "FAIL", arm="PASS" if all(arm_all) else "FAIL", gap=gmin[0], gap_with=gmin[1],
               arm_clear=dmin[0], arm_clear_with=dmin[1], why="; ".join(why)[:400], docks=sorted(d for d in docks if d is not None),
               n_units=len(units))


def force_check(run, st, actor, path):
    """Largest static force the actor can push along the insertion at its final pose (UR joint-torque limits, cell.max_force)."""
    a = run.arm(actor)
    T = run.cl.T_phase(st["phase"])
    d = -(T[:3, :3] @ unit(np.asarray(path[1], float) - np.asarray(path[0], float)))
    try:
        f = C.max_force(a, run.q[actor], d, p_world=a.tcp(run.q[actor])[:3, 3], tool_kg=K.TOOL_MASS.get(a.tool_name, 1.0) + K.TL.TC["mass"])
    except Exception:  # noqa: BLE001
        f = None
    return dict(kind=st["force"], max_push_N=None if f is None else round(f, 0))


def screw_targets(run, joint, pn=None, near=None):
    idx = run.sc.joint(joint, pn)
    idx = [i for i in idx if i not in run.done_screws]
    if near is not None:
        lo, hi = near
        out = []
        for i in idx:
            P = np.asarray(run.sc.objs[i]["P"], float)
            if np.all(P >= lo - 25.0) and np.all(P <= hi + 25.0):
                out.append(i)
        idx = out
    return idx


SD_MAX = TL.SCREWDRIVER["torque"][1]


def driver_for(run, i, phase, torque):
    """OnRobot Screwdriver unless the joint needs more than its 5 N m or the screw is driven upward (the OnRobot works
    downward or sideways only); then the inline nutrunner."""
    F0, c = CK.screw_frame(run.sc, i, {})
    into = -(run.cl.T_phase(phase)[:3, :3] @ F0[:3, 2])
    up = float(into[2]) > 0.17
    if up:
        return "nutrunner_angle", "upward"
    if (torque or 0.0) > SD_MAX:
        return "nutrunner", f"{torque} N m > {SD_MAX} N m"
    return "screwdriver", ""


def drive_screw(run, i, phase, actor, long_bit=None, state=None, torque=None, force_driver=None):
    """Screwdriver with the screw on its bit, from the hole's mouth to the seat. Returns a result dict."""
    sc, cl = run.sc, run.cl
    st_ = state or {}
    T = cl.T_phase(phase)
    F0, c = CK.screw_frame(sc, i, st_)
    tool, tool_why = driver_for(run, i, phase, torque)
    if force_driver:
        tool, tool_why = force_driver, "chosen for this joint"
    s_hex = float(c.get("s", 3.0))
    L = float(c.get("L", 10.0))
    if c.get("kind") == "captive" or str(sc.objs[i].get("pn")) == "95966A705":
        L = 10.0                       # a captive screw already sits in its flange: only its last turns into the insert are driven
    engage = 0.6 * s_hex
    body = run.held_body([i], f"screw:{sc.short(i)[:30]}", st_)
    body.place(T)
    dest = contacts_at_seat(run, body, exclude=[i])
    allow = frozenset([("held", n) for n in dest] + [("tool", n) for n in dest])
    wd = CK.withdraw_check(sc, CK.World(sc, st_, [j for j in run.cl.where if j != i and run.grp_of.get(j) == run.grp_of.get(i, None)] or []), i)
    a = run.arm(actor)
    x_target = float((T @ F0)[0, 3])
    drivers = [tool] + {"screwdriver": (["nutrunner"] if (torque or 0) >= TL.NUTRUNNER["torque"][0] else []) + ["nutrunner_angle"],
                        "nutrunner": ["nutrunner_angle"], "nutrunner_angle": []}[tool]
    first_fail = None
    for tool in drivers:
        best = None
        n_plans = 0
        drive_ok = False
        for dk in run.docks_for(x_target)[:2]:
            n_plans = 0
            run.dock(actor, dk)
            run.set_tool(actor, tool, long_bit, tip_d=round(1.15 * s_hex + 0.2, 1))
            last = getattr(run, "last_roll", {}).get(actor, 0)
            for roll in sorted(range(0, 360, 30), key=lambda r: min(abs(r - last), 360 - abs(r - last))):
                Tt = T @ F0 @ Tm(p=(0, 0, -engage)) @ K.Rx(180.0) @ K.Rz(roll)
                off = inv(Tt) @ T                  # TCP -> screw body's machine frame
                a.hold(body, off)
                offs = np.linspace(L + 2.0, 0.0, max(2, int(math.ceil((L + 2.0) / DS)) + 1))
                Ts = [Tt @ Tm(p=(0, 0, -o)) for o in offs]      # tool z points into the hole: back off along -z
                fr = run.follow(actor, Ts, 0.0, allow, exclude=[i], dist_every=99)
                if fr["ok"]:
                    drive_ok = True
                    if n_plans >= 1:
                        continue
                    n_plans += 1
                    a.place(run.q[actor])
                    chk = K.checker(cl, actor, [i])
                    if chk.collisions(run.q[actor], 0.0, allow, first=True):
                        run.q[actor] = a.park_q()          # the last retreat left the arm touching something: start from park
                    # 1) straight from where the arm is (the previous screw's retreat), else 2) a taught-style approach: from a
                    # pre-approach pose 60 mm back along the screw axis (and, for the angle head, slid 220 mm out along the
                    # tool body, from under the plate), a checked Cartesian move in, and a plan only to the pre-approach pose
                    path_q, info = chk.plan(run.q[actor], fr["qs"][0], 0.0, allow=allow, iters=60)
                    if path_q is None:
                        T_s = Ts[0]
                        pre = [T_s @ Tm(p=(0, 0, -60.0 * k / 4)) for k in range(5)]
                        if tool == "nutrunner_angle":
                            fl = T_s @ inv(a.tcp_local())
                            dz = fl[:3, 2]
                            pre += [Tm(p=-dz * 220.0 * k / 8) @ pre[-1] for k in range(1, 9)]
                        fr_in = run.follow(actor, pre[::-1], 0.0, allow, exclude=[i], dist_every=99,
                                           seeds=[fr["qs"][0]])
                        if fr_in["ok"]:
                            a.place(run.q[actor])
                            path_q, info = chk.plan(run.q[actor], fr_in["qs"][0], 0.0, allow=allow, iters=SCREW_PLAN_ITERS)
                            if path_q is not None:
                                info = dict(info, via="pre-approach")
                        else:
                            info = dict(reason=f"no clear way in to the hole's mouth ({fr_in['hit']})")
                    if path_q is not None:
                        best = dict(ok=True, dock=dk, roll=roll, qs=fr["qs"], planned=info.get("planned"))
                        break
                    if best is None or best.get("why", "").startswith("no ") or not best.get("qs"):
                        best = dict(ok=False, dock=dk, roll=roll, qs=fr["qs"], why=f"approach: {info.get('reason')}")
                elif best is None or (not best["ok"] and len(fr["qs"]) > len(best.get("qs", []))):
                    best = dict(ok=False, dock=dk, roll=roll, qs=fr["qs"], why=fr["hit"])
            if best and best["ok"]:
                break

        if best and best["ok"]:
            break
        if first_fail is None:
            first_fail = (tool, (best or {}).get("why", ""))
    if first_fail and best and best["ok"]:
        tool_why = (tool_why + "; " if tool_why else "") + f"{first_fail[0]} blocked ({first_fail[1][:60]})"
    elif first_fail and len(drivers) > 1:
        best["why"] = f"{first_fail[0]}: {first_fail[1][:90]}; also no way with {', '.join(drivers[1:])}"
    if best["qs"]:
        run.q[actor] = best["qs"][-1]
        a.place(run.q[actor])
    run.last_roll = getattr(run, "last_roll", {})
    run.last_roll[actor] = best["roll"]
    # clearance of the screwdriver body to everything at the seat
    md = None
    if best["ok"]:
        chk = K.checker(cl, actor, [i])
        rob = Group(list(a.grip.values()) + [a.links["wrist3"], a.links["wrist2"], a.links["wrist1"], a.links["forearm"]])
        d, x, y = C.group_distance(rob, chk.sc.world, margin=40.0)
        if y is not None and d < math.inf:
            md = (round(float(d), 1), f"{x.name.split('/')[-1]} to {y.name[:50]}")
    run.snapshot(f"screw:{i}")
    return dict(ok=best["ok"], why=best.get("why", ""), dock=best["dock"], roll=best["roll"], withdraw=wd["ok"],
                withdraw_by=wd["blocked_by"], clear=md, hex=s_hex, L=L, tool=tool, tool_why=tool_why, drive_ok=drive_ok, dest=sorted(dest))


def do_screws(run, st, row, near=None, actor=None):
    idx = screw_targets(run, st["joint"], st.get("pn"), near)
    if not idx:
        row.update(sweep="-", arm="-", why="all screws of this joint were already driven (with the part held)")
        return []
    actor = actor or st.get("actor", "A")
    per = []
    for i in idx:
        r = drive_screw(run, i, st["phase"], actor, st.get("long_bit"), torque=st.get("torque_Nm"), force_driver=st.get("driver"))
        r["arm"] = actor
        if not r["ok"] and not st.get("holder_busy"):
            other = run.other(actor)
            r2 = drive_screw(run, i, st["phase"], other, st.get("long_bit"), torque=st.get("torque_Nm"), force_driver=st.get("driver"))
            if r2["ok"]:
                r2["arm"] = other
                r2["tool_why"] = (r2.get("tool_why", "") + f"; arm {actor} could not ({r['why'][:60]})").strip("; ")
                retreat(run, other, 30.0, names=r2.get("dest", ()))
                r = r2
            run.arm(other).release()               # never leave a screw hanging on the other arm's bit
            go_park(run, other)
        per.append((i, r))
        log(f"   {run.sc.short(i)[-12:]}: {'ok' if r['ok'] else ('drive clear, approach not planned' if r['drive_ok'] else r['why'][:80])}")
        retreat(run, actor, 30.0, names=r.get("dest", ()))
        run.add([i], st["grp"], st["phase"])
        run.done_screws.add(i)
    go_park(run, actor)
    nok = sum(1 for _, r in per if r["ok"])
    ndrive = sum(1 for _, r in per if r["drive_ok"])
    nwd = sum(1 for _, r in per if not r["withdraw"])
    clears = [r["clear"] for _, r in per if r.get("clear")]
    fails = [f"{run.sc.short(i)[-6:]}: {r['why'][:90]}" for i, r in per if not r["ok"]]
    row.update(sweep="PASS" if nwd == 0 else "FAIL", arm="PASS" if nok == len(per) else ("FAIL" if nok == 0 else "PART"),
               n=len(per), n_ok=nok, n_drive=ndrive, arm_clear=min(clears)[0] if clears else None, arm_clear_with=min(clears)[1] if clears else None,
               why=("; ".join(fails[:3]) + (f" (+{len(fails) - 3} more)" if len(fails) > 3 else ""))[:400],
               docks=sorted({r["dock"] for _, r in per}), hex=per[0][1]["hex"], screw_L=per[0][1]["L"],
               driver=sorted({r["tool"] for _, r in per}), driver_why=sorted({r["tool_why"] for _, r in per if r["tool_why"]}),
               per_screw=[dict(screw=run.sc.label(i), ok=r["ok"], why=r.get("why", ""), dock=r["dock"], roll=r["roll"],
                               withdraw=r["withdraw"], clear=r.get("clear"), drive_ok=r["drive_ok"], driver=r["tool"], arm=r.get("arm"),
                               note=r.get("tool_why", "")) for i, r in per])
    return per


def hold_and_drive(run, st, u, holder):
    """The arm that placed u keeps it at its seat (gripper closed on it) while the other arm drives the joint's screws near it."""
    sc = run.sc
    lo = np.min([sc.objs[i]["V"].min(0) for i in u], axis=0)
    hi = np.max([sc.objs[i]["V"].max(0) for i in u], axis=0)
    M = sc.pose(u[0], {})
    lo, hi = (M[:3, :3] @ lo + M[:3, 3]), (M[:3, :3] @ hi + M[:3, 3])
    lo, hi = np.minimum(lo, hi), np.maximum(lo, hi)
    a = run.arm(holder)
    a.release()                    # the part is in the world now; the closed gripper stays round it
    tq = next((x.get("torque_Nm") for x in SQ.steps() if x.get("joint") == st["hold_for"]), None)
    sub = dict(id=st["id"] + "h", joint=st["hold_for"], phase=st["phase"], grp=st["grp"], actor=run.other(holder), torque_Nm=tq,
               holder_busy=True)
    row = {}
    per = do_screws(run, sub, row, near=(lo, hi), actor=run.other(holder))
    run.sub_rows = getattr(run, "sub_rows", [])
    row.update(id=sub["id"], label=f"{st['label'][:60]}: screws of {st['hold_for']} driven while arm {holder} holds it", do="screws",
               joint=st["hold_for"], actor=run.other(holder), holder=holder)
    run.sub_rows.append(row)
    ok = all(r["ok"] for _, r in per) if per else True
    return dict(ok=ok, why="" if ok else f"held-part screws: {row.get('why', '')[:150]}")


def do_flip(run, st, row):
    """Single-arm turn-over: grasp from the front (tool along world y), lift, roll 180 deg about the tool axis, move, lower."""
    sc, cl = run.sc, run.cl
    grp = st["grp"]
    idx = sorted(run.asm.get(grp, set()))
    T0 = cl.T_phase(st["frm"])
    actor = st["actor"]
    if st["to"] == "handoff":
        T1 = cl.T_phase("body_up") @ Tm(p=(0.0, 0.0, 235.0))
    else:
        T1 = cl.T_phase(st["to"])
    zg = -60.0 if grp == "body" else -41.0          # tube between flange and collar / the piston head
    G_m = frame_zx((0.0, 1.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 0.0, zg))     # from the front, fingers across x, TCP on the axis
    width = 56.8 if grp == "body" else 50.2
    body = run.held_body(idx, f"held:{st['id']}", {})
    cl.take(idx)
    lift = 320.0
    frames = []
    for s in np.linspace(0, 1, 12):
        frames.append(Tm(p=(0, 0, lift * s)) @ T0)
    Tl = Tm(p=(0, 0, lift)) @ T0
    G0 = Tl @ G_m
    for s in np.linspace(0, 1, 37)[1:]:
        R = Tm(p=G0[:3, 3]) @ Tm(rot((0, 1, 0), 180.0 * s)) @ Tm(p=-G0[:3, 3])
        frames.append(R @ Tl)
    Tr = frames[-1]
    T1l = Tm(p=(0, 0, lift)) @ T1
    for s in np.linspace(0, 1, 25)[1:]:
        Ti = Tr.copy()
        Ti[:3, 3] = Tr[:3, 3] * (1 - s) + T1l[:3, 3] * s
        frames.append(Ti)
    for s in np.linspace(0, 1, 12)[1:]:
        frames.append(Tm(p=(0, 0, lift * (1 - s))) @ T1)
    best = None
    for dk in run.docks_for(float((T0 @ G_m)[0, 3])):
        run.dock(actor, dk)
        run.set_tool(actor, "gripper")
        a = run.arm(actor)
        a.hold(body, inv(G_m))
        close = close_for(run, actor, width)
        a.close = close
        Ts = [F @ G_m for F in frames]
        nest = {"body_up": "Module nest, upright", "body_inv": "Module nest, upside down", "stack_inv": "Stack nest"}
        seat = [nest[k] for k in (st["frm"], st["to"]) if k in nest]
        allow_f = frozenset([("held", n) for n in seat] + [("tool", n) for n in seat])
        fr = run.follow(actor, Ts, close, allow_f, dist_every=8)
        if fr["ok"]:
            a.place(run.q[actor], close)
            p, info = run.plan_to(actor, fr["qs"][0], close, allow=allow_f)
            fr["plan_ok"] = p is not None
            fr["plan"] = info
        if best is None or (fr["ok"] and fr.get("plan_ok")) or len(fr["qs"]) > len(best[1]["qs"]):
            best = (dk, fr)
        if fr["ok"] and fr.get("plan_ok"):
            break
    dk, fr = best
    a = run.arm(actor)
    if fr["qs"]:
        run.q[actor] = fr["qs"][-1]
        a.place(run.q[actor], a.close)
    ok = fr["ok"] and fr.get("plan_ok", False)
    why = "" if ok else (fr["hit"] or f"approach: {fr.get('plan', {}).get('reason')}")
    run.snapshot(st["id"])
    taker_ok = None
    if st.get("taker"):
        # arm B takes the stack from above at the hand-off pose, by an internal grip in the block's bayonet socket
        tk = st["taker"]
        b = run.arm(tk)
        best_t = None
        for dk2 in run.docks_for(float(T1[0, 3])):
            run.dock(tk, dk2)
            run.set_tool(tk, "gripper")
            Gb = T1 @ frame_zx((0, 0, -1.0), (0, 1.0, 0), (0.0, 0.0, -17.0))     # fingers across y: clear of A's across x
            allow = frozenset([("tool", body.name)])
            sols = b.ik_all(Gb, seed=run.q[tk])
            chk = K.checker(cl, tk)
            for q in sols:
                cc = chk.collisions(q, b.close_for_gap(50.2), allow, first=True)
                if not cc:
                    best_t = (dk2, q)
                    break
            if best_t:
                break
        taker_ok = best_t is not None
        if best_t:
            run.q[tk] = best_t[1]
            b.place(best_t[1], b.close_for_gap(50.2))
        if not taker_ok:
            why += "; arm B finds no collision-free grasp at the hand-off"
        run.snapshot(st["id"] + "-handoff")
        retreat_ok = True
        a.release()
        go_park(run, actor)
        if taker_ok:
            run.q[tk] = best_t[1]
        cl.put(idx, T1)
        for i in idx:
            run.cl.where[i] = T1
        run.phase_of[grp] = "handoff"
    else:
        a.release()
        run.add(idx, grp, st["to"])
        retreat(run, actor)
        go_park(run, actor)
    row.update(sweep="-", arm="PASS" if ok and taker_ok in (None, True) else "FAIL", why=why[:300], docks=[dk],
               arm_clear=fr["min_d"], arm_clear_with=fr["with_"], mass_kg=None)


def do_dual(run, st, row):
    """Both arms carry one part (or the chamber assembly) along its path; with flip=True the part also turns over about y."""
    sc, cl = run.sc, run.cl
    idx = run.resolve(st["keys"], moved=bool(st.get("flip") or st.get("whole")))
    if st.get("flip") or st.get("whole"):
        idx = sorted(run.asm.get("chamber", set()))
    elif st.get("moved"):
        idx = [i for i in idx]
    T1 = cl.T_phase(st["phase"])
    body = run.held_body(idx, f"held:{st['id']}", {})
    # mass of what is carried
    mass = 0.0
    seen = set()
    for i in idx:
        p = sc.parts[sc.objs[i]["part"]]
        if sc.objs[i]["item"] is None and p.name not in seen:
            seen.add(p.name)
            mass += float(p.mass_kg) if p.mass_kg else float(p.shape.Volume() * 1e-9 * run.M.MAT.get(p.mat, {}).get("rho", 2700))
        elif sc.objs[i]["item"] is not None:
            mass += float(sc.FS.mass_g(sc.objs[i]["pn"])) / 1000.0
    cl.take(idx)
    frames = carry_frames(cl, st)
    jaws_open = None
    if st.get("frm") == "chamber_up_T" and "Trunnion jaws" in cl.static:
        jaws_open = cl.static.pop("Trunnion jaws")            # the positioner opens its jaws (pneumatic) before the arms lift
    gA = given_grasp(st["grasps"]["A"], np.eye(4))
    gB = given_grasp(st["grasps"]["B"], np.eye(4))
    # the part's seat (what it rests on or slides over at the end, e.g. dowels in a slip fit) may be touched up to 1.5 mm deep
    body.place(T1)
    dest = contacts_at_seat(run, body, exclude=idx)
    if st.get("frm"):
        body.place(cl.T_phase(st["frm"]))
        dest |= contacts_at_seat(run, body, exclude=idx)
    seat_allow = [("held", n) for n in dest] + [("tool", n) for n in dest]
    best = None
    dock_sets = ([(st["docks"], st["docks"])] if st.get("docks") else
                 [("TB", "TB")] if st.get("flip") else [("Br", "Bl"), ("B", "B"), ("Bl", "Br"), ("B", "Bl"), ("Br", "B")])
    cl.A.release()
    cl.B.release()
    for dA, dB in dock_sets:
        run.dock("A", K.DOCKS[dA])
        run.dock("B", K.DOCKS[dB])
        run.set_tool("A", "gripper")
        run.set_tool("B", "gripper")
        A, B = cl.A, cl.B
        A.hold(body, inv(gA))
        cA, cB = A.close_for_gap(float(st.get("grip_gap", 16.0 if "Base plate" in st["label"] or "bridge" in st["label"].lower() else 30.0))), None
        cB = cA
        A.close, B.close = cA, cB
        qa, qb = None, None
        ok, why, k_end = True, "", 0
        allowA = frozenset(seat_allow)
        allowB = frozenset([("tool", body.name)] + seat_allow)
        chkA = K.checker(cl, "A")
        md = math.inf
        mw = None
        # both arms' IK at the first frame: try branch pairs
        TA0, TB0 = frames[0] @ gA, frames[0] @ gB
        solsA = A.ik_all(TA0, seed=run.q["A"])
        solsB = B.ik_all(TB0, seed=run.q["B"])
        pair = None
        for qa0 in solsA[:8]:
            A.place(qa0, cA)
            if chkA.collisions(qa0, cA, allowA, first=True):
                continue
            chkB = K.checker(cl, "B")
            for qb0 in solsB[:8]:
                if not chkB.collisions(qb0, cB, allowB, first=True):
                    pair = (qa0, qb0)
                    break
            if pair:
                break
        if pair is None:
            res = dict(ok=False, why="no collision-free pair of arm poses at the start of the carry", k=0)
        else:
            qa, qb = pair
            qsA, qsB = [qa], [qb]
            for k, F in enumerate(frames[1:], 1):
                sa = A.ik_all(F @ gA, seed=qa)
                sb = B.ik_all(F @ gB, seed=qb)
                if not sa or not sb:
                    ok, why, k_end = False, f"no IK for arm {'A' if not sa else 'B'}", k
                    break
                if np.abs(sa[0] - qa).max() > JUMP or np.abs(sb[0] - qb).max() > JUMP:
                    ok, why, k_end = False, f"IK branch flip for arm {'A' if np.abs(sa[0] - qa).max() > JUMP else 'B'}", k
                    break
                qa, qb = sa[0], sb[0]
                B.place(qb, cB)
                ca = K.checker(cl, "A").collisions(qa, cA, allowA, first=True)
                if ca:
                    ok, why, k_end = False, f"arm A: {ca[0][0]} hits {ca[0][1]}", k
                    break
                cb = K.checker(cl, "B").collisions(qb, cB, allowB, first=True)
                if cb:
                    ok, why, k_end = False, f"arm B: {cb[0][0]} hits {cb[0][1]}", k
                    break
                qsA.append(qa)
                qsB.append(qb)
                if k % 10 == 0:
                    rob = Group([body] + list(A.grip.values()) + list(B.grip.values()))
                    d, x, y = C.group_distance(rob, cl.world("A", other=False), margin=40.0)
                    if y is not None and d < md and y.kind != "machine" or (y is not None and d < md and k < len(frames) - 8):
                        md, mw = d, f"{x.name.split('/')[-1][:30]} to {y.name[:50]}"
            res = dict(ok=ok, why=why, k=k_end, qsA=qsA, qsB=qsB)
        res["docks"] = (dA, dB)
        res["md"] = (md, mw)
        if best is None or res["ok"] or res.get("k", 0) > best.get("k", 0):
            best = res
        if res["ok"]:
            break
    A, B = cl.A, cl.B
    if best.get("qsA"):
        run.q["A"], run.q["B"] = best["qsA"][-1], best["qsB"][-1]
        A.place(run.q["A"], A.close)
        B.place(run.q["B"], B.close)
    run.snapshot(st["id"])
    # mid-carry snapshot for the flip render
    if best.get("qsA") and len(best["qsA"]) > 40:
        k = len(best["qsA"]) // 2
        A.place(best["qsA"][k], A.close)
        B.place(best["qsB"][k], B.close)
        run.snapshot(st["id"] + "-mid")
        A.place(run.q["A"], A.close)
        B.place(run.q["B"], B.close)
    run.dual_paths = getattr(run, "dual_paths", {})
    run.dual_paths[st["id"]] = dict(frames=[f.tolist() for f in frames[: len(best.get("qsA", []))]], qsA=[list(map(float, q)) for q in best.get("qsA", [])],
                                    qsB=[list(map(float, q)) for q in best.get("qsB", [])], body=body.name)
    A.release()
    if jaws_open is not None:
        cl.static["Trunnion jaws"] = jaws_open
    if st.get("merge"):
        run.merge(st["merge"], st["grp"]) if st["merge"] != "chamber" else None
    run.add(idx, st["grp"], st["phase"])
    for n in ("A", "B"):
        retreat(run, n)
        go_park(run, n)
    md, mw = best["md"]
    tip = tipover(mass / 2.0, 0.0)
    row.update(sweep="-", arm="PASS" if best["ok"] else "FAIL", why=(best.get("why") or "")[:300],
               docks=list(best["docks"]), mass_kg=round(mass, 2), arm_clear=None if md == math.inf else round(float(md), 1),
               arm_clear_with=mw, tip_margin=tip)


def carry_frames(cl, st):
    """World poses of the carried part, frame by frame: straight down its path, or (flip) lifted 450 mm, turned 180 deg
    about y while it crosses to the target fixture, and lowered."""
    T1 = cl.T_phase(st["phase"])
    frames = []
    path = [np.asarray(p, float) for p in st["path"]]
    if st.get("flip"):
        T0 = cl.T_phase(st["frm"])
        cg = np.array(st.get("cg", (0.0, 0.0, -60.0)), float)
        c0 = (T0 @ np.r_[cg, 1])[:3]
        c1 = (T1 @ np.r_[cg, 1])[:3]
        R0 = Tm(T0[:3, :3])

        def Tob(theta, c):
            return Tm(p=c) @ Tm(rot((0, 1, 0), theta)) @ R0 @ Tm(p=-cg)
        H = 450.0
        for s in np.linspace(0, 1, 16):
            frames.append(Tob(0.0, c0 + np.array([0, 0, H * s])))
        for s in np.linspace(0, 1, 61)[1:]:
            frames.append(Tob(180.0 * s, c0 * (1 - s) + c1 * s + np.array([0, 0, H])))
        for s in np.linspace(0, 1, 26)[1:]:
            frames.append(Tob(180.0, c1 + np.array([0, 0, H * (1 - s)])))
    elif st.get("frm"):
        # straight carry between two fixtures, the same way up: lift, cross, lower
        T0 = cl.T_phase(st["frm"])
        H = float(st.get("lift", 120.0))
        n = 1 + int(np.linalg.norm(T1[:3, 3] - T0[:3, 3]) / 10.0)
        for s_ in np.linspace(0, 1, 13):
            frames.append(Tm(p=(0, 0, H * s_)) @ T0)
        for s_ in np.linspace(0, 1, n + 1)[1:]:
            Ti = T0.copy()
            Ti[:3, 3] = T0[:3, 3] * (1 - s_) + T1[:3, 3] * s_ + np.array([0, 0, H])
            frames.append(Ti)
        for s_ in np.linspace(0, 1, 13)[1:]:
            frames.append(Tm(p=(0, 0, H * (1 - s_))) @ T1)
    else:
        for o in dense(path[::-1], 5.0):
            frames.append(T1 @ Tm(p=o))
    return frames


def tipover(payload_kg, push_N, reach_mm=1100.0, push_h_mm=1000.0):
    """Margin against tipping a MiR250 + 131 kg ballast + cabinet + arm (masses in cell2.MASS) about the near edge of its
    580 mm width, with payload_kg at reach_mm out from the arm base and push_N horizontal at push_h_mm above the floor.
    Returns the ratio of the restoring to the overturning moment (> 1 is stable)."""
    m = K.MASS
    W = 580.0 / 2.0
    arm_off = K.ARM_OFF
    stab = (m["mir"] + m["ballast"] + m["cabinet"] + m["control_box"]) * 9.81 * W + m["arm"] * 9.81 * (W - arm_off)
    over = payload_kg * 9.81 * max(0.0, reach_mm + arm_off - W) + push_N * push_h_mm
    return round(stab / max(over, 1e-9), 1)


def do_rotate(run, st, row):
    """The trunnion turns its jaws and the sub-assembly 180 deg about x; both arms parked. Every frame: the turning chamber and
    jaws against the cell, everything placed and both arms (FCL on meshes), as PR 318's movers check."""
    cl = run.cl
    grp = st["grp"]
    idx = sorted(run.asm.get(grp, set()))
    T0 = cl.T_phase(st["frm"])
    for n in ("A", "B"):
        go_park(run, n)
    body = run.held_body(idx, f"turning:{st['id']}", {})
    jaws = cl.static.pop("Trunnion jaws")
    J0 = jaws.M.copy()
    cl.take(idx)
    TT = cl.T_fix["T"]
    sign = float(st.get("sign", 1.0))
    hits, worst = [], None
    md = math.inf
    for th in np.linspace(0.0, 180.0, 37):
        R = TT @ Tm(rot((1, 0, 0), sign * th)) @ inv(TT)
        body.place(R @ T0)
        jaws.place(R @ J0)
        w = cl.world("A", other=True)
        for b in cl.A.bodies():
            w.add(b)
        mov = Group([body, jaws])
        hh = [(x.name, y.name) for x, y in C.group_hits(mov, w) if not (x is jaws and y.name.startswith("Trunnion stands"))]
        if hh:
            hits.append((round(float(th)), hh[0]))
        if int(th) % 30 == 0:
            d, x, y = C.group_distance(mov, w, margin=60.0)
            if y is not None and d < md and not y.name.startswith("Trunnion stands"):
                md, worst = d, f"{x.name[:20]} to {y.name[:40]}"
    jaws.place(TT @ Tm(rot((1, 0, 0), sign * 180.0)) @ inv(TT) @ J0)
    cl.static["Trunnion jaws"] = jaws
    run.add(idx, grp, st["to"])
    run.snapshot(st["id"])
    row.update(sweep="-", arm="PASS" if not hits else "FAIL", why="" if not hits else f"at {hits[0][0]} deg: {hits[0][1][0][:30]} hits {hits[0][1][1][:50]}",
               arm_clear=None if md == math.inf else round(float(md), 1), arm_clear_with=worst, mass_kg=None)


def do_note(run, st, row):
    row.update(sweep="-", arm="-", who=st["who"], why=st["why"])


# ================================================================================================ seals
def do_seal(run, st, row):
    m = st["method"]
    if m == "ring":
        idx = run.resolve(st["keys"])
        path = [tuple(map(float, p)) for p in st["path"]]
        # the ring goes into a loose part on a nest; the sweep is against that part only, in the machine frame
        parent = {"gland_plate_M50": "bottom flange: gland plate", "outlet_plenum": "outlet plenum", "overflow_funnel": "Overflow funnel block",
                  "inlet_plenum": "inlet plenum", "window_flange": "Window flange", "window_lower": "Window flange", "metering_base": "Metering base",
                  "camera_adapter": "Camera viewport"}.get(st["ring"])
        par = run.sc.find(parent, fasteners=False) if parent else []
        sw = sweep(run, st, idx, path, {}, present=par)
        arm = "-"
        why = "" if sw["ok"] else f"blocked by {sw['blocked_by'][:50]}"
        if par and all(i in run.cl.where for i in par):
            r = arm_place(run, st, idx, path, {}, st["actor"], "gripper+caps", f"held:{st['id']}",
                          grasp=None, internal=True)
            arm = "PASS" if r["ok"] else "FAIL"
            why += r["why"]
            row.update(arm_clear=r.get("min_d"), arm_clear_with=r.get("min_with"), docks=[r.get("dock")])
            retreat(run, st["actor"])
            go_park(run, st["actor"])
        run.add(idx, st["grp"], st["phase"])
        row.update(sweep="PASS" if sw["ok"] else "FAIL", gap=sw.get("min_gap"), gap_with=sw.get("gap_with"), arm=arm, why=why,
                   method="ring placed into its groove by the 2F-85 with pin caps (internal 2-point grip), then rolled down")
    elif m == "loader":
        idx = run.resolve(st["keys"])
        (lv, lf), _ = TL.mesh("ring_loader")
        # tube tip at the deeper groove (machine z -96), tube pointing +z, grip block below
        Ml = Tm(p=(0.0, 0.0, -96.0)) @ K.Rx(180.0)
        v = lv @ Ml[:3, :3].T + Ml[:3, 3]
        body_fake = dict(V=v, F=lf)
        tool_idx = add_temp_obj(run, "Ring loader (tool)", v, lf)
        path = [(0.0, 0.0, 0.0), (0.0, 0.0, -110.0)]
        sw = sweep(run, st, [tool_idx], path, {})
        r = arm_place(run, st, [tool_idx], path, {}, st["actor"], "gripper", f"held:{st['id']}:loader",
                      grasp=dict(point=(0.0, 0.0, -96.0 - TL.LOADER_GRASP[2]), z=(0, 0, 1.0), x=(1.0, 0, 0)))
        retreat(run, st["actor"])
        go_park(run, st["actor"])
        run.cl.take([tool_idx])
        run.add(idx, st["grp"], st["phase"])
        row.update(sweep="PASS" if sw["ok"] else "FAIL", gap=sw.get("min_gap"), gap_with=sw.get("gap_with"),
                   arm="PASS" if r["ok"] else "FAIL", why=("" if sw["ok"] else f"loader blocked by {sw.get('blocked_by')}; ") + r["why"],
                   arm_clear=r.get("min_d"), arm_clear_with=r.get("min_with"), docks=[r.get("dock")],
                   method="ring folded into the loader's slotted tube, pushed through the Ø15.93 throat, released into the groove")
    elif m == "mandrel":
        idx = run.resolve(st["keys"])
        (mv, mf), _ = TL.mesh("spigot_mandrel")
        (pv, pf), _ = TL.mesh("spigot_pusher")
        mand = add_temp_obj(run, "Spigot mandrel (tool)", mv, mf)
        # 1) arm B puts the mandrel on the spigot (from above), lets go
        st_b = dict(st, actor=st["holder"], phase="body_up", grp="body")
        sw1 = sweep(run, st_b, [mand], [(0, 0, 0), (0, 0, 80)], {})
        r1 = arm_place(run, st_b, [mand], [(0, 0, 0), (0, 0, 80)], {}, st["holder"], "gripper", f"held:{st['id']}:mandrel",
                       grasp=dict(point=TL.MANDREL_GRASP, z=(0, 0, -1.0), x=(1.0, 0, 0)))
        run.add([mand], "body", "body_up")
        retreat(run, st["holder"])
        go_park(run, st["holder"])
        # 2) the ring is laid on the cone (not modelled as a shape); 3) arm A strokes the pusher down over the mandrel
        push = add_temp_obj(run, "Spigot pusher (tool)", pv, pf)
        sw2 = sweep(run, st_b, [push], [(0, 0, 0), (0, 0, 60)], {})
        r2 = arm_place(run, st_b, [push], [(0, 0, 0), (0, 0, 60)], {}, st["actor"], "gripper", f"held:{st['id']}:pusher",
                       grasp=dict(point=TL.PUSHER_GRASP, z=(0, 0, -1.0), x=(1.0, 0, 0)))
        run.snapshot(st["id"])
        retreat(run, st["actor"])
        go_park(run, st["actor"])
        run.cl.take([mand, push])
        for t in (mand, push):
            run.asm["body"].discard(t)
            run.grp_of.pop(t, None)
        run.add(idx, st["grp"], st["phase"])
        ok = r1["ok"] and r2["ok"]
        row.update(sweep="PASS" if (sw1["ok"] and sw2["ok"]) else "FAIL", gap=min([g for g in (sw1.get("min_gap"), sw2.get("min_gap")) if g is not None], default=None),
                   arm="PASS" if ok else "FAIL", why=(r1["why"] + " " + r2["why"]).strip(),
                   arm_clear=min([d for d in (r1.get("min_d"), r2.get("min_d")) if d is not None], default=None),
                   docks=[r1.get("dock"), r2.get("dock")],
                   method="2-238 stretched 9.4 % over an acetal mandrel (cone + 0.45 mm sleeve over the spigot's top edge), pushed into "
                          "the groove by a sleeve that stops on the mandrel")
    elif m == "roller":
        idx = run.resolve(st["keys"])
        r = roller_traverse(run, st)
        run.add(idx, st["grp"], st["phase"])
        row.update(sweep="-", arm="PASS" if r["ok"] else "FAIL", why=r["why"], arm_clear=r.get("min_d"), arm_clear_with=r.get("with"),
                   docks=r.get("docks"),
                   method="3.53 mm cord laid in by arm B at the midpoints, ends and quarter points, then rolled home by arm A's PTFE wheel "
                          "(Adebola et al. 2024's binary order), splice at the back-right corner")


_TEMP = {}


def add_temp_obj(run, name, V, F):
    """A tool drawn as a temporary model object (machine frame), so the sweep and the arm checks see it."""
    sc = run.sc
    if name in _TEMP:
        return _TEMP[name]
    sc.objs.append(dict(name=name, part=next(i for i, p in enumerate(sc.parts) if p.name.startswith("Build module")), item=None, key=None,
                        pn="", shape=None, kind="tool", V=np.asarray(V, float), F=np.asarray(F, np.int64), bvh=CK.bvh(V, F), man=None))
    sc.n = len(sc.objs)
    i = sc.n - 1
    # its pose must not follow the module's motion group: override in pose()
    orig = sc.pose

    def posed(j, st, _o=orig, _i=i):
        return np.eye(4) if j == _i else _o(j, st)
    sc.pose = posed
    _TEMP[name] = i
    return i


def roller_traverse(run, st):
    """The roller follows the gland's centre line (rounded rectangle) once round, pressing the cord home: the front half by
    arm A, the back half by arm B."""
    P = run.M.P
    ix, iy = P["ix"], P["iy"]
    if st.get("ring") == "floor":
        FR = run.M.FRAME
        gt = FR["gland_t"]
        hx, hy, r = ix + gt + P["gland_w"] / 2, iy + gt + P["gland_w"] / 2, FR["r_in"] + gt + P["gland_w"] / 2
        z = 0.0 - P["gland_d"] + P["oring_cs"]
    else:
        hx, hy, r = ix + 3.3 + P["gland_w"] / 2, iy + 3.3 + P["gland_w"] / 2, 4.3 + P["gland_w"] / 2
        z = P["lid_z0"] - P["gland_d"] + P["oring_cs"]
    pts, tans = [], []
    # straight runs and corner arcs, counter-clockwise from the front-left corner
    seq = []
    for (cx, cy, a0) in ((hx - r, -hy + r, -90.0), (hx - r, hy - r, 0.0), (-hx + r, hy - r, 90.0), (-hx + r, -hy + r, 180.0)):
        seq.append((cx, cy, a0))
    for k, (cx, cy, a0) in enumerate(seq):
        # arc
        for a in np.linspace(a0, a0 + 90.0, 7):
            t = math.radians(a)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
            tans.append((-math.sin(t), math.cos(t)))
        # straight to the next arc's start
        nx, ny, na = seq[(k + 1) % 4]
        t1 = math.radians(na)
        p0 = np.array(pts[-1])
        p1 = np.array((nx + r * math.cos(t1), ny + r * math.sin(t1)))
        L = np.linalg.norm(p1 - p0)
        d = (p1 - p0) / max(L, 1e-9)
        for s in np.linspace(0, L, max(2, int(L / 6.0)))[1:-1]:
            q = p0 + d * s
            pts.append(tuple(q))
            tans.append(tuple(d))
    T = run.cl.T_phase(st["phase"])
    Ts = []
    for (x, y), (tx, ty) in zip(pts, tans):
        Tm_ = frame_zx((0, 0, -1.0), (tx, ty, 0.0), (x, y, z))
        Ts.append(T @ Tm_)
    best = None
    # the arm works from the front for the front half and the back arm for the back half
    halves = {"A": [k for k, (x, y) in enumerate(pts) if y <= 0], "B": [k for k, (x, y) in enumerate(pts) if y > 0]}
    out = dict(ok=True, why="", docks=[], min_d=None, with_=None)
    for n, ks in halves.items():
        if not ks:
            continue
        # contiguous runs in order
        ks = sorted(ks)
        segs, cur = [], [ks[0]]
        for k in ks[1:]:
            if k == cur[-1] + 1:
                cur.append(k)
            else:
                segs.append(cur)
                cur = [k]
        segs.append(cur)
        for seg in segs:
            done = False
            for dk in run.docks_for(float(np.mean([Ts[k][0, 3] for k in seg]))):
                run.dock(n, dk)
                run.set_tool(n, "roller")
                fr = run.follow(n, [Ts[k] for k in seg], 0.0, frozenset(), dist_every=10)
                if fr["ok"]:
                    run.arm(n).place(run.q[n])
                    p, info = run.plan_to(n, fr["qs"][0], 0.0)
                    if p is not None:
                        run.q[n] = fr["qs"][-1]
                        run.arm(n).place(run.q[n])
                        out["docks"].append(dk)
                        if fr["min_d"] is not None and (out["min_d"] is None or fr["min_d"] < out["min_d"]):
                            out["min_d"], out["with"] = fr["min_d"], fr["with_"]
                        done = True
                        run.snapshot(f"{st['id']}:{n}:{seg[0]}")
                        break
                last = fr
            if not done:
                out["ok"] = False
                out["why"] += f"arm {n} on points {seg[0]}-{seg[-1]}: {last['hit'] or 'approach plan failed'}; "
            retreat(run, n, 40.0)
            go_park(run, n)
    return out


# ================================================================================================ main
ONLY = []


def main(argv):
    only = None
    for a in argv:
        if a.startswith("--only="):
            only = a.split("=", 1)[1].split(",")
            ONLY[:] = only
    OUT.mkdir(parents=True, exist_ok=True)
    run = Run()
    log(f"scene ready: {run.sc.n} objects")
    steps = SQ.steps("M50")
    for st in steps:
        if only and not any(st["id"].startswith(o) for o in only):
            continue
        row = dict(id=st["id"], label=st["label"], do=st["do"], tool=st.get("tool"), actor=st.get("actor"), holder=st.get("holder"),
                   phase=st.get("phase"), joint=st.get("joint"))
        t = time.time()
        try:
            {"place": do_place, "screws": do_screws, "seal": do_seal, "flip": do_flip, "dual": do_dual, "note": do_note,
             "rotate": do_rotate}[st["do"]](run, st, row)
        except Exception as e:  # noqa: BLE001
            row.update(arm="ERROR", why=f"{type(e).__name__}: {e}"[:300])
            traceback.print_exc()
        row["seconds"] = round(time.time() - t, 1)
        run.rows.append(row)
        for sr in getattr(run, "sub_rows", []):
            run.rows.append(sr)
        run.sub_rows = []
        log(st["id"], row.get("sweep"), row.get("arm"), row.get("gap"), row.get("arm_clear"), (row.get("why") or "")[:160])
        save(run)
    save(run, final=True)
    log("done")


TAG = os.environ.get("ASM_TAG", "")


def save(run, final=False):
    name = f"results{TAG}.json" if not ONLY else f"results_{'_'.join(ONLY)}{TAG}.json"
    (OUT / name).write_text(json.dumps(dict(rows=run.rows, generated_s=round(time.time() - T0, 1)), indent=1, default=str))
    if final:
        import pickle
        pickle.dump(dict(frames=run.frames, held=getattr(run, "held_meshes", {}), dual=getattr(run, "dual_paths", {})),
                    open(f"/tmp/asm/frames{TAG}.pkl" if not ONLY else f"/tmp/asm/frames_{'_'.join(ONLY)}{TAG}.pkl", "wb"))


if __name__ == "__main__":
    main(sys.argv[1:])
