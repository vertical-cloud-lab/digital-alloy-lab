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
    try:
        import pvscene  # noqa: E402
    except ImportError:      # timing only (plan_frames): no drawing
        pvscene = None
import common  # noqa: E402
import kit_table as KT  # noqa: E402

FPS = common.FPS
TRAJ = pathlib.Path(os.environ.get("ASM_TRAJ", str(common.TRAJ)))     # the recorded run to replay
CHAP = {"module": ("40-assembly-module", "Assembly 1: the build module, by two UR12e on MiR250s"),
        "chamber": ("41-assembly-chamber", "Assembly 2: the chamber and the process module, by two UR12e on MiR250s")}
# time-lapse factors per event kind (real seconds per real second shown); the renderer may raise them to fit the budget
LAPSE = dict(drive=8.0, plan=1.5, cart=1.0, grip=1.0, screw=1.0, screw_rep=6.0, wait=40.0, turn=1.5, move2=1.5, tool=8.0)
SHOT = dict(wide=3600.0, mid=1500.0, close=650.0)
MAX_TRI = int(os.environ.get("ASM_MAX_TRI", "2500"))     # per object, for drawing only


def load_events(chapter):
    """The chapter's recorded events: asm_<chapter>.pkl, or (round 8) while the planner is still running, the per-step chunks
    record.py writes as it goes (asm_<chapter>.chunk<k>.pkl, in order)."""
    f = TRAJ / f"asm_{chapter}.pkl"
    if f.exists():
        return pickle.load(open(f, "rb"))["events"]
    ev = []
    for c in sorted(TRAJ.glob(f"asm_{chapter}.chunk*.pkl")):
        ev += pickle.load(open(c, "rb"))["events"]
    if not ev:
        raise FileNotFoundError(f)
    print(f"{chapter}: {len(ev)} events from the planner's chunks (the run is not finished)", flush=True)
    return ev


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
        self.ev = load_events(chapter)
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
        # the pallets' and bins' contents from kit_table's mesh cache (building it here would load the whole model: run
        # `python kit_table.py --meshes` first; without it the pallets and bins are drawn empty)
        if os.environ.get("ASM_KIT_ITEMS", "1") == "1" and list((KT.CACHE).glob(f"kit-meshes-finished-{KT._hash()}.pkl")):
            sup = {x["key"]: ("coil" if x.get("coil") else x["support"]) for x in KT.slots()}
            for it in KT.item_meshes():
                if sup.get(it["key"]) in ("pallet", "bin", "coil"):
                    sc.add(f"kti/{it['key']}/{it['name'][:20]}", it["mesh"], it["color"], group="static", specular=0.25)
        else:
            print("kit item meshes not cached: pallets and bins drawn empty", flush=True)
        # ---- objects (each its own group, moved per frame)
        self.T = {}
        for i, o in scn["objs"].items():
            V, F = o["V"], o["F"]
            if len(F) > MAX_TRI:           # software rendering (llvmpipe + SSAA): the frame time follows the triangle count
                import cell as C0
                V, F = C0.decimate(np.asarray(V, float), np.asarray(F, np.int64), MAX_TRI)
            sc.add(f"o{i}", poly(V, F), o["color"], group=f"o{i}", specular=0.3, shown=False)
        # the seal steps' hand tools (run_assembly.add_temp_obj) are made after the scene was saved: draw them from tooling.py,
        # in the machine frame the run gave them (the ring loader's tube tip at the deeper rod groove, machine z -96, pointing up)
        import tooling as TLh
        unknown = []
        for e in self.ev:
            if e["kind"] in ("attach", "put"):
                for i in e["objs"]:
                    if i not in scn["objs"] and i not in [u[0] for u in unknown]:
                        unknown.append((i, e["step"]))
        seen_m17 = 0
        for i, sid in unknown:
            name, M = None, np.eye(4)
            if sid == "M12":
                name = "ring_loader"
                M = Tm((0.0, 0.0, -96.0)) @ np.diag([1.0, -1.0, -1.0, 1.0])
            elif sid == "M17":
                name = "spigot_mandrel" if seen_m17 == 0 else "spigot_pusher"
                seen_m17 += 1
            if name is None:
                continue
            (v, f), _ = TLh.mesh(name)
            v = np.asarray(v, float) @ M[:3, :3].T + M[:3, 3]
            sc.add(f"o{i}", poly(v, f), common.COL["tool"], group=f"o{i}", specular=0.4, shown=False)
            self.objs[i] = dict(name=name, part=-1, kind="tool", V=v, F=f, color=common.COL["tool"])
        coil_parts = {i for x in KT.slots() if x.get("coil") for i in x["part_indices"]}
        for i, T in scn["table_T"].items():
            self.T[i] = np.asarray(T, float)
            # hoses and lines lie on the table coiled (kit_table draws the coil); the object is their fitted shape
            sc.alpha[f"o{i}"] = 0.0 if scn["objs"].get(i, {}).get("part") in coil_parts else 1.0
            sc.gmat[f"o{i}"] = self.T[i]
        # ---- arms and MiRs
        self.arm = {"A": K.ArmT("A", K.DOCKS["T"], "front"), "B": K.ArmT("B", K.DOCKS["T"], "back")}
        self.vis = {n: hall.ArmVis(sc, self.arm[n], n) for n in ("A", "B")}
        self.mir = {n: hall.MirVis(sc, n, "front" if n == "A" else "back") for n in ("A", "B")}
        self.tool_keys = {"A": [], "B": []}
        # fingertip caps: the ring caps (internal two-pin grip) and the tending robot's cranked plate fingers
        import tooling as TL0
        import eoat
        caps = {"ring": TL0.mesh("ring_caps")[0], "plate": eoat.plate_finger_spec()["meshes"]}
        for n in ("A", "B"):
            for kind, ms in caps.items():
                for tip, (v, f) in ms.items():
                    sc.add(f"{n}/cap/{kind}/{tip}", poly(v, f), "#d9b23a" if kind == "ring" else "#7f8c99", group=f"{n}/cap/{kind}/{tip}",
                           specular=0.3, shown=False)
        # hand tools held in the gripper (temporary objects in the run) are among self.objs
        # ---- the trunnion's jaws
        import tooling as TL
        (v, f), _ = TL.mesh("trunnion_jaws")
        sc.add("jaws", poly(v, f), "#d18a1f", group="jaws", specular=0.3)
        self.TT = Tm((K.STATIONS["T"], 0.0, TL.TRUNNION["h_axis"]))
        sc.gmat["jaws"] = self.TT
        self.jaw = 0.0
        # ---- a hoist hook and chain for the hoist-assisted lifts (drawn above the carried part)
        hook = pv.Box(bounds=(-30, 30, -12, 12, 0, 50)).triangulate().merge(pv.Cylinder(center=(0, 0, 1000), direction=(0, 0, 1), radius=4,
                                                                                          height=1900).triangulate())
        sc.add("hoist", hook, "#e2b007", group="hoist", specular=0.3, shown=False)
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
        if tool is not None:
            s["tool"] = tool
        a = self.arm[n]
        if s.get("pose") is not None:
            # round 8: the MiR mid-route (pivot, drive along its heading, pivot): its body and the arm's base as one pose
            T = self.pose_T(n, *s["pose"])
            a.base = T @ self.base_ref(n)
            self.sc.gmat[f"mir{n}"] = T
            self.mir[n].x = float(s["pose"][0])
        else:
            a.move_base(s["x"])
            self.mir[n].at(s["x"])
        a.q = s["q"]
        a.close = s["close"]
        self.vis[n].update()
        sc = self.sc
        F = a.fk()
        W0 = a.base @ F["tool0"]
        Wt = W0 @ Tm((0.0, 0.0, self.K.TC_H))
        grip_on = s["tool"].startswith("gripper") or s["tool"] in ("hand",)
        for nm in self.vis[n].names():
            if "/gr/" in nm and "camera" not in nm:
                sc.alpha[nm] = 1.0 if grip_on else 0.0
        cap = "ring" if s["tool"] == "gripper+caps" else ("plate" if s["tool"] == "gripper+plate" else None)
        import ur_arm
        G = ur_arm.gripper_fk(s["close"])
        for kind in ("ring", "plate"):
            for tip in ("left_finger_tip", "right_finger_tip"):
                k = f"{n}/cap/{kind}/{tip}"
                sc.alpha[k] = 1.0 if kind == cap else 0.0
                if kind == cap:
                    sc.gmat[k] = Wt @ G[tip]
        key = self.tool_key(n)
        for k in self.tool_keys[n]:
            sc.alpha[k] = 1.0 if k == key else 0.0
            if k == key:
                sc.gmat[k] = Wt
        # held objects ride on the TCP
        h = s["held"]
        if h is not None:
            T_tcp = a.tcp(s["q"], s["close"])
            Tsp = T_tcp @ rot_axis((0, 0, 1), h["spin_deg"]) if h.get("spin_deg") else T_tcp     # a screw turning with the bit
            for i in h["objs"]:
                if f"o{i}" in sc.actors:
                    sc.gmat[f"o{i}"] = Tsp @ h["off"]
                    sc.alpha[f"o{i}"] = 1.0

    def yc0(self, n):
        return (-1.0 if n == "A" else 1.0) * (self.K.ARM_Y + self.K.ARM_OFF)

    def base_ref(self, n):
        import cell as C0
        return C0.Tm(C0.rot((0, 0, 1), 0.0 if n == "A" else 180.0), (0.0, (-1.0 if n == "A" else 1.0) * self.K.ARM_Y, self.K.ARM_Z))

    def pose_T(self, n, x, y, th):
        """MiR n's centre at (x, y), heading th deg from +x; the bodies and the arm base as drawn at x = 0 on the dock lane."""
        return Tm((x, y, 0.0)) @ rot_axis((0, 0, 1), th) @ Tm((0.0, -self.yc0(n), 0.0))

    def snapshot(self):
        return dict(G={k: np.array(v, copy=True) for k, v in self.sc.gmat.items()}, A=dict(self.sc.alpha),
                    st={n: {k: (np.array(v, copy=True) if isinstance(v, np.ndarray) else v) for k, v in self.st[n].items()}
                        for n in ("A", "B")}, jaw=self.jaw)

    def restore(self, snap):
        self.sc.gmat.clear()
        self.sc.gmat.update({k: np.array(v, copy=True) for k, v in snap["G"].items()})
        self.sc.alpha.clear()
        self.sc.alpha.update(snap["A"])
        self.jaw = snap["jaw"]
        for n in ("A", "B"):
            self.st[n] = {k: (np.array(v, copy=True) if isinstance(v, np.ndarray) else v) for k, v in snap["st"][n].items()}
            self.set_arm(n)

    def tool_key(self, n):
        """The actor of arm n's current end effector (made on first use; screwdrivers per bit length)."""
        s = self.st[n]
        t = s["tool"]
        if t.startswith("gripper") or t in ("hand", ""):
            return None
        sp = s.get("spec") or {}
        eb, td = float(sp.get("extra_bit", 0.0) or 0.0), sp.get("tip_d")
        key = f"{n}/tool/{t}/{eb:.0f}/{td}"
        if key not in self.sc.actors:
            try:
                (v, f), _ = self.K.tool_mesh(t, eb, td) if t in ("screwdriver", "nutrunner", "nutrunner_angle") else self.K.tool_mesh(t)
            except Exception as e:     # noqa: BLE001
                print("no tool mesh", t, e)
                return None
            self.sc.add(key, poly(v, f), common.COL["tool"], group=key, specular=0.4, shown=False)
            self.tool_keys[n].append(key)
        return key

    def put(self, objs, T):
        for i in objs:
            if f"o{i}" in self.sc.actors:
                self.sc.gmat[f"o{i}"] = np.asarray(T, float)
                self.sc.alpha[f"o{i}"] = 1.0

    def tcp(self, n):
        a = self.arm[n]
        return a.tcp(self.st[n]["q"], self.st[n]["close"])[:3, 3]

    # ------------------------------------------------------------------------------------------- camera
    def aim(self, focus, shot="mid", side="A", az=None, el=None, snap=False):
        # down the bench's axis from +x, a little to the working arm's side and from above: between the two lanes, so neither
        # MiR nor parked arm stands between the camera and the work
        side_az = {"A": 14.0, "B": -14.0, "C": 0.0}       # just past the bench axis, on the side away from the working arm
        if el is None:
            el = {"wide": 24.0, "mid": 44.0, "close": 56.0}.get(shot, 40.0)
        fx = float(np.asarray(focus)[0])
        if az is None:
            az = side_az.get(side, 0.0)
            if fx > 2400.0:
                # at the parts table: from across the table, above it, so the arm reaching over from its lane faces the camera
                az = {"A": 62.0, "B": -62.0}.get(side, 0.0)
                el = max(el, 44.0)
            elif fx < 600.0:
                # the bench, Fixture P and the trunnion: from the -x end (from +x the trunnion's stands stand in the way)
                az = 180.0 - az
                if fx > 0.0:
                    el = max(el, 50.0)        # the trunnion, over Fixture P
        a = math.radians(az)
        R = SHOT.get(shot, shot) if isinstance(shot, str) else float(shot)
        e = math.radians(el)
        focus = np.asarray(focus, float)
        pos = focus + R * np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)])
        if self.cam_pos is None or snap or np.linalg.norm(focus - self.cam_foc) > 900.0 or \
                np.linalg.norm(pos - self.cam_pos) > 2500.0:
            self.cam_pos, self.cam_foc = pos, focus           # a cut, not a pan across the cell
        else:
            k = 0.3
            self.cam_pos = self.cam_pos * (1 - k) + pos * k
            self.cam_foc = self.cam_foc * (1 - k) + focus * k

    def shot(self):
        self.sc.camera([self.cam_pos, self.cam_foc, (0, 0, 1)], view_angle=32.0)
        return self.sc.render()

    # ------------------------------------------------------------------------------------------- occlusion-aware views
    def _table_occ(self, focus):
        """The parts still on the long table within 1.5 m of a pick's work point (run 10: with only the arms, MiRs and
        fixtures as occluders, a pick's camera could stand behind the tall parts on the table)."""
        out = []
        for i, T in self.T.items():
            o = self.objs.get(i)
            if o is None or o.get("V") is None or self.sc.alpha.get(f"o{i}", 1.0) == 0.0:
                continue
            V = np.asarray(o["V"], float) @ np.asarray(T)[:3, :3].T + np.asarray(T)[:3, 3]
            c = V.mean(0)
            if c[0] < 2400.0 or abs(c[0] - focus[0]) > 1500.0 or np.linalg.norm(c - focus) < 150.0:
                continue
            out.append((V, np.asarray(o["F"])))
        return out

    def _occluders(self, focus=None):
        """One vtkOBBTree over both arms (links and gripper), both MiRs and the cell's fixtures, as they stand now (and the
        parts on the long table near a pick there)."""
        import vtk
        vs, fs, n0 = [], [], 0
        for n in ("A", "B"):
            a = self.arm[n]
            s = self.st[n]
            a.move_base(s["x"])
            a.place(s["q"], s["close"])
            for b in list(a.links.values()) + list(a.grip.values()):
                vs.append(b.v @ b.M[:3, :3].T + b.M[:3, 3])
                fs.append(b.f + n0)
                n0 += len(b.v)
            for _, (v, f), _ in self.K.mir_bodies(n, s["x"], "front" if n == "A" else "back"):
                vs.append(np.asarray(v, float))
                fs.append(np.asarray(f) + n0)
                n0 += len(v)
        if not hasattr(self, "_static_occ"):
            self._static_occ = [(np.asarray(v, float), np.asarray(f)) for _, (v, f), _ in self._cell_static()]
        extra = self._table_occ(np.asarray(focus, float)) if focus is not None and float(focus[0]) > 2400.0 else []
        for v, f in list(self._static_occ) + extra:
            vs.append(v)
            fs.append(f + n0)
            n0 += len(v)
        V, F = np.vstack(vs), np.vstack(fs).astype(np.int64)
        pd = poly(V, F)
        tree = vtk.vtkOBBTree()
        tree.SetDataSet(pd)
        tree.BuildLocator()
        self._occ_keep = pd
        return tree

    def best_view(self, focus, dist, prefer_az, els=(30.0, 45.0), r_pts=45.0):
        """(az, el) of the camera at `dist` from `focus` that sees the most of ~20 points round the work point: 12 azimuths x
        the elevations, rays to each point cast against the arms, tools, MiRs and fixtures (vtkOBBTree)."""
        import vtk
        focus = np.asarray(focus, float)
        tree = self._occluders(focus)
        pts = [focus]
        for k in range(8):
            a = 2 * math.pi * k / 8
            pts.append(focus + r_pts * np.array([math.cos(a), math.sin(a), 0.0]))
        for k in range(6):
            a = 2 * math.pi * k / 6 + 0.4
            pts.append(focus + r_pts * np.array([0.7 * math.cos(a), 0.7 * math.sin(a), 0.7]))
        for z in (-1.0, 1.0):
            pts.append(focus + np.array([0.0, 0.0, z * r_pts]))
        best = None
        hit_pts = vtk.vtkPoints()
        for el in els:
            e = math.radians(el)
            for k in range(12):
                az = prefer_az + 30.0 * k
                a = math.radians(az)
                cam = focus + dist * np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)])
                if cam[2] < 300.0:
                    continue
                blocked = 0
                for P in pts:
                    hit_pts.Reset()
                    if tree.IntersectWithLine(cam.tolist(), P.tolist(), hit_pts, None):
                        dmin = min(np.linalg.norm(np.array(hit_pts.GetPoint(j)) - cam) for j in range(hit_pts.GetNumberOfPoints()))
                        if dmin < np.linalg.norm(P - cam) - 12.0:
                            blocked += 1
                dev = min(abs(((az - prefer_az + 180.0) % 360.0) - 180.0), 180.0) / 180.0
                score = blocked + 0.6 * dev + (0.2 if el < 40.0 else 0.0)
                if best is None or score < best[0]:
                    best = (score, az % 360.0, el, blocked)
        return best


# ------------------------------------------------------------------------------------------------ timing (round 8)
# Each step's events are sped up together so the step fits its budget (seconds of video); never slower than real time. Every
# arm motion is drawn (round 7's capped mode cut transit moves, so an arm jumped inside a shot). MiR drives: the chapter's first
# DRIVE_SHOW drives to and from the parts table are drawn in full (pivot, drive, pivot) at DRIVE_LAPSE; the later ones are an
# ellipsis: not drawn, their time carried by the clocks, and the camera always cuts across them (the MiR is somewhere else after
# the cut, never jumping inside a shot). Drives between the cell's docks are always drawn.
# *_rep: the second and later screws of a step (the presenter trip, the approach, the run-down, the retreat): a labelled
# time-lapse, every motion still drawn, at least two frames each
KW = dict(drive=10.0, tool=4.0, plan=2.0, cart=1.0, grip=1.0, screw=1.0, screw_rep=4.0, plan_rep=8.0, cart_rep=5.0, wait=40.0,
          turn=1.0, move2=1.0)
BUDGET = dict(place=6.0, screws=5.0, seal=12.0, flip=8.0, dual=10.0, rotate=6.0, note=3.0)
MIN_FRAMES = dict(grip=3, tool=6, wait=24, drive=12, plan=5, cart=5, screw=8, screw_rep=3, plan_rep=2, cart_rep=2, turn=36, move2=24)
MIN_TABLE = dict(MIN_FRAMES, plan=10, cart=10, grip=5)     # a pick at the table: its shot lasts about 4 s
CLOSE_STEPS = ("seal",)
DRIVE_SHOW = int(os.environ.get("ASM_DRIVE_SHOW", "4"))
# the chapter's first PICK_SHOW visits to the parts table show the pick (the later ones, like the later drives, are an ellipsis:
# checked and timed, not drawn; the next frames say so)
PICK_SHOW = int(os.environ.get("ASM_PICK_SHOW", "8"))
DRIVE_LAPSE = 6.0
TABLE_X = 2200.0


def kind_key(e, rep):
    k = e["kind"]
    if k == "move":
        return "plan" if e.get("how") == "plan" else "cart"
    if k == "screw":
        return "screw" if rep == 0 else "screw_rep"
    return k


def drive_shown(e, count):
    """Is this drive drawn? (count: drives to or from the table drawn so far in the chapter)"""
    if max(e["x0"], e["x1"]) <= TABLE_X:
        return True                       # a hop between the cell's docks
    return count < DRIVE_SHOW


def plan_frames(events, scale=1.0):
    """Frames per event: {id(event): (n_frames, real seconds per frame)}; n = 0: not drawn (its time goes to the next frame)."""
    out = {}
    cur, buf = None, []
    shown = [0]

    def close_step(do, buf):
        if not buf:
            return
        nscrew = sum(1 for e, kk in buf if e["kind"] == "screw")
        B = BUDGET.get(do, 4.0) * scale
        if nscrew:
            B = max(B, scale * min(18.0, 3.0 + 1.1 * nscrew))
        w = sum(float(e.get("dur", 0.0)) / KW.get(kk, 1.0) for e, kk in buf if kk != "drive")
        f = max(1.0, w / max(B, 0.5))
        for e, kk in buf:
            d = float(e.get("dur", 0.0))
            if d <= 0:
                continue
            if kk == "drive":
                if not drive_shown(e, shown[0]):
                    out[id(e)] = (0, d)
                    continue
                if max(e["x0"], e["x1"]) > TABLE_X:
                    shown[0] += 1
                n = int(round(d * FPS / DRIVE_LAPSE))
                n = int(min(max(n, MIN_FRAMES["drive"] if max(e["x0"], e["x1"]) <= TABLE_X else 30), 96))
            elif e.get("unplanned"):
                out[id(e)] = (0, d)       # not checked: not drawn (a card says so)
                continue
            elif at_table.get(id(e)) and at_table[id(e)] > PICK_SHOW:
                out[id(e)] = (0, d)       # a later pick at the table: an ellipsis
                continue
            else:
                n = int(round(d * FPS / (KW.get(kk, 1.0) * f)))
                n = max(n, (MIN_TABLE if at_table.get(id(e)) else MIN_FRAMES).get(kk, 2))
            out[id(e)] = (n, d / n)
    reps = {}
    xs = {}
    at_table = {}
    visits = [0]
    for e in events:
        if e["kind"] == "step":
            close_step(cur, buf)
            cur, buf = e.get("do"), []
            reps = {}
            continue
        if e["kind"] == "drive":
            if e["x1"] > TABLE_X and e["x0"] <= TABLE_X:
                visits[0] += 1
            xs[e["arm"]] = e["x1"]
        if e.get("dur", 0.0) and e["kind"] in ("move", "drive", "grip", "tool", "screw", "turn", "move2", "wait"):
            r = reps.get(e.get("arm"), 0) if e["kind"] == "screw" else 0
            if e["kind"] == "screw":
                reps[e.get("arm")] = r + 1
            if e["kind"] in ("move", "grip") and xs.get(e.get("arm"), 0.0) > TABLE_X:
                at_table[id(e)] = visits[0]
            kk = kind_key(e, r)
            if kk in ("plan", "cart") and reps.get(e.get("arm"), 0) >= 1 and cur == "screws":
                kk += "_rep"                 # after the step's first screw
            buf.append((e, kk))
    close_step(cur, buf)
    return out


def merge_fails(ev, ev_fail, steps):
    """Chapter events with, before each step in `steps`, the failed attempt recorded by an earlier run (status fail)."""
    by = {}
    cur = None
    for e in ev_fail:
        if e["kind"] == "step":
            cur = e["id"]
            if cur in steps:
                by[cur] = [dict(e, failed_run=True)]
            continue
        if cur in by:
            by[cur].append(dict(e, failed_run=True))
    out = []
    for e in ev:
        if e["kind"] == "step" and e["id"] in by:
            out.append(dict(kind="snapshot", step=e["id"]))
            out += by[e["id"]]
            out.append(dict(kind="restore", step=e["id"]))
        out.append(e)
    return out


# ------------------------------------------------------------------------------------------------ the camera rig (round 8)
# Sterling, 2026-11-26: "motion sickness" (round 7's camera picked a new best view for nearly every motion: 84-103 jumps a
# minute, steady for 0.2-0.4 s). Now: a few fixed tripod shots per place in the cell; a shot is chosen per step at a place
# (the least occluded of the place's tripods, rays from the camera to points round the work, cast once per step), held, and
# changed only by a cut; a shot shorter than MIN_SHOT is merged into a neighbour that also shows its work. The camera never
# moves inside a shot. The chapter opens on the wide view of the whole cell (lesson 5: the overview first, then the work).
TABLE_ZONES = (3900.0, 6900.0, 9900.0, 12900.0)
MIN_SHOT = int(os.environ.get("ASM_MIN_SHOT", str(4 * 12)))


def rig():
    R = {"cell": ((-3900.0, -4700.0, 4600.0), (900.0, 0.0, 500.0), 46.0),
         "bench": ((-3450.0, 280.0, 2300.0), (-1150.0, 0.0, 950.0), 30.0),
         "bench_A": ((-1250.0, -2700.0, 3300.0), (-1250.0, 0.0, 950.0), 34.0),
         "bench_B": ((-1250.0, 2700.0, 3300.0), (-1250.0, 0.0, 950.0), 34.0),
         "PT": ((-1700.0, -380.0, 2700.0), (0.0, 0.0, 1050.0), 38.0),
         "PT_A": ((0.0, -3000.0, 3300.0), (0.0, 0.0, 1050.0), 38.0),
         "PT_B": ((0.0, 3000.0, 3300.0), (0.0, 0.0, 1050.0), 38.0),
         "B": ((3200.0, 380.0, 2600.0), (1350.0, 0.0, 1250.0), 34.0),
         "B_end": ((-300.0, -380.0, 2800.0), (1350.0, 0.0, 1250.0), 34.0),
         "B_A": ((1350.0, -2900.0, 3200.0), (1350.0, 0.0, 1200.0), 34.0),
         "B_B": ((1350.0, 2900.0, 3200.0), (1350.0, 0.0, 1200.0), 34.0),
         # MiR drives: from above the bench's far end, looking down the lane to the far end of the table
         "lane_A": ((-4600.0, -3000.0, 3400.0), (4500.0, -450.0, 200.0), 44.0),
         "lane_B": ((-4600.0, 3000.0, 3400.0), (4500.0, 450.0, 200.0), 44.0)}
    return R


RIG = rig()


def cam_def(name):
    """(position, focal point, view angle) of a tripod. The table's tripods are set up where the MiR stops for the pick
    ("T@<x><arm>[_hi|_end]"): fixed for the whole shot, like the others."""
    if name in RIG:
        return RIG[name]
    if name.startswith("T@"):
        body, _, var = name[2:].partition("_")
        n = body[-1]
        x = float(body[:-1])
        s = -1.0 if n == "A" else 1.0
        if var == "hi":            # over the arm's own lane, from behind its MiR
            return ((x - 300.0, s * 2900.0, 3300.0), (x, s * 150.0, 950.0), 38.0)
        if var == "end":           # along the table's edge, from further along it
            return ((x + 2600.0, s * 1700.0, 2200.0), (x, s * 350.0, 1000.0), 38.0)
        return ((x + 300.0, -s * 2500.0, 2700.0), (x, s * 300.0, 1000.0), 38.0)      # from across the table
    raise KeyError(name)


def place_cands(loc):
    k = loc[0]
    if k == "bench":
        return ["bench", "bench_A", "bench_B"]
    if k == "PT":
        return ["PT", "PT_A", "PT_B"]
    if k == "B":
        return ["B", "B_end", "B_A", "B_B"]
    if k == "table":
        b = f"T@{loc[1]:.0f}{loc[2]}"
        return [b, b + "_hi", b + "_end"]
    if k == "lane":
        return [f"lane_{loc[1]}"]
    return ["cell"]


def loc_of_x(x):
    if x < -700.0:
        return ("bench",)
    if x < 850.0:
        return ("PT",)
    return ("B",)


def in_view(cam, P, margin=0.88, far=9500.0):
    pos, foc, va = cam_def(cam)
    pos, foc, P = np.asarray(pos, float), np.asarray(foc, float), np.asarray(P, float)
    f = foc - pos
    f /= np.linalg.norm(f)
    r = np.cross(f, (0.0, 0.0, 1.0))
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    d = P - pos
    z = float(d @ f)
    if z <= 200.0 or z > far:
        return False
    t = math.tan(math.radians(va / 2.0))
    return abs(float(d @ u) / (z * t)) < margin and abs(float(d @ r) / (z * t * common.W / common.H)) < margin


def choose_shots(plan, scores):
    """plan: per frame dict(loc, key, work, force); scores: {key: {cam: [blocked fractions]}} -> per frame camera name."""
    n = len(plan)
    groups = []                                  # [start, end, key, loc, cam]
    for i, p in enumerate(plan):
        if groups and groups[-1][2] == p["key"] and not p.get("force"):
            groups[-1][1] = i + 1
        else:
            groups.append([i, i + 1, p["key"], p["loc"], None])
    prev = None
    for g in groups:
        cands = place_cands(g[3])
        sc = scores.get(g[2], {})
        forced = bool(plan[g[0]].get("force"))
        best = None
        for rank, c in enumerate(cands):
            if forced and c == prev:
                continue                         # a forced cut (something moved off screen) must change the camera
            v = sc.get(c)
            s = (float(np.mean(v)) if v else 0.5) + 0.08 * rank
            if best is None or s < best[0]:
                best = (s, c)
        if best is None:
            best = (0.0, "cell" if prev != "cell" else ("bench" if g[3][0] != "bench" else "PT"))
        g[4] = best[1]
        prev = g[4]
    # shots: groups with one camera merged
    shots = []
    for g in groups:
        if shots and shots[-1][2] == g[4] and not plan[g[0]].get("force"):
            shots[-1][1] = g[1]
            shots[-1][3].append(g)
        else:
            shots.append([g[0], g[1], g[4], [g]])

    def ok_from(cam, sh):
        pts = [plan[i]["work"] for i in range(sh[0], sh[1]) if plan[i]["work"] is not None]
        if not pts:
            return True
        if any(not in_view(cam, P) for P in pts[::max(1, len(pts) // 6)]):
            return False
        for g in sh[3]:
            v = scores.get(g[2], {}).get(cam)
            if v and float(np.mean(v)) > 0.45:
                return False
        return True
    changed = True
    while changed:
        changed = False
        for k, sh in enumerate(shots):
            if sh[1] - sh[0] >= MIN_SHOT or len(shots) == 1:
                continue
            if plan[sh[0]].get("force"):
                continue
            for j in (k - 1, k + 1):
                if 0 <= j < len(shots) and not (j == k + 1 and plan[shots[j][0]].get("force")) and ok_from(shots[j][2], sh):
                    o = shots[j]
                    lo, hi = min(o[0], sh[0]), max(o[1], sh[1])
                    shots[j] = [lo, hi, o[2], (o[3] + sh[3]) if j < k else (sh[3] + o[3])]
                    del shots[k]
                    changed = True
                    break
            if changed:
                break
    # neighbours with the same camera after the merges
    out = []
    for sh in shots:
        if out and out[-1][2] == sh[2] and not plan[sh[0]].get("force"):
            out[-1][1] = sh[1]
        else:
            out.append(list(sh[:3]))
    cams = [None] * n
    for a, b, c in out:
        for i in range(a, b):
            cams[i] = c
    return cams


def shot_stats(cams):
    runs = []
    for c in cams:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
        else:
            runs.append([c, 1])
    L = [r[1] / FPS for r in runs]
    mins = len(cams) / FPS / 60.0
    return dict(frames=len(cams), shots=len(runs), median_s=round(float(np.median(L)), 2) if L else 0.0,
                mean_s=round(float(np.mean(L)), 2) if L else 0.0, cuts_per_min=round((len(runs) - 1) / mins, 2) if mins else 0.0,
                under_4s=sum(1 for x in L if x < 4.0), cams=sorted({r[0] for r in runs}))


# ------------------------------------------------------------------------------------------------ playback
def route_pose(rt, t):
    """(x, y, heading) of the MiR centre t s into the route (legs: pivot / line, each eased); None after the last leg."""
    for lg in rt["legs"]:
        d = float(lg["dur"])
        if t <= d or lg is rt["legs"][-1]:
            u = smooth(min(max(t / d, 0.0), 1.0)) if d > 0 else 1.0
            if lg["kind"] == "pivot":
                return (lg["x"], lg["y"], lg["th0"] + (lg["th1"] - lg["th0"]) * u)
            return (lg["x0"] + (lg["x1"] - lg["x0"]) * u, lg["y0"] + (lg["y1"] - lg["y0"]) * u, lg["th"])
        t -= d
    return None


def run(chapter, max_frames=None, scale=1.0, fail_pkl=None, fail_steps=(), fail_notes=None):
    """fail_notes: {step id: what failed in an earlier run}: shown (status redesign) before the redesigned step is played."""
    fail_notes = dict(fail_notes or {})
    fail_steps = tuple(fail_steps) + tuple(k for k in fail_notes if k not in fail_steps)
    rp = Replay(chapter)
    name, title = CHAP[chapter]
    ev = rp.ev
    if fail_pkl and fail_steps:
        ev_f = pickle.load(open(fail_pkl, "rb"))["events"]
        ev = merge_fails(ev, ev_f, set(fail_steps))
    # a move the planner could not plan is followed by an "unplanned" mark: not drawn, a card says so
    last_move = {}
    for e in ev:
        if e["kind"] == "move":
            last_move[e.get("arm")] = e
        elif e["kind"] == "mark" and e.get("what") == "unplanned" and e.get("arm") in last_move:
            last_move[e["arm"]]["unplanned"] = True
    # ASM_UPTO=<step id>: stop before this step (the chunks of a run still going may end inside a step's fetch)
    upto = os.environ.get("ASM_UPTO")
    if upto:
        k = next((i for i, e in enumerate(ev) if e["kind"] == "step" and e["id"] == upto), None)
        if k is not None:
            ev = ev[:k]
    nfr = plan_frames(ev, scale)
    snap0 = rp.snapshot()
    print(f"{name}: {len(ev)} events", flush=True)
    # pass 1: what each frame shows (no drawing) -> the shots; pass 2: draw the slice
    plan, scores = [], {}
    _play(rp, ev, nfr, fail_notes, fail_steps, plan=plan, scores=scores, max_frames=max_frames)
    cams = choose_shots(plan, scores)
    st = shot_stats(cams)
    print(f"{name}: {len(plan)} frames ({len(plan) / FPS / 60:.1f} min); shots: {st}", flush=True)
    if os.environ.get("ASM_SHOTS_VERBOSE") == "1":
        i0 = 0
        for i in range(1, len(cams) + 1):
            if i == len(cams) or cams[i] != cams[i0]:
                print(f"   {i0:5d} {i - i0:4d} fr {(i - i0) / FPS:5.1f} s  {cams[i0]:9s} {plan[i0]['step']:6s} {plan[i0]['loc']}"
                      f"{' forced' if plan[i0].get('force') else ''}", flush=True)
                i0 = i
    rp.restore(snap0)
    lo, hi, part, k_ = 0, 10 ** 9, None, None
    tot_frames = len(plan)
    if os.environ.get("ASM_PART"):
        k_, n_ = (int(x) for x in os.environ["ASM_PART"].split("/"))
        lo = int(tot_frames * k_ / n_)
        hi = int(tot_frames * (k_ + 1) / n_) if k_ < n_ - 1 else 10 ** 9
        part = "part"
    if os.environ.get("ASM_RANGE"):
        lo, hi = (int(x) for x in os.environ["ASM_RANGE"].split(":"))
        part, k_ = "range", os.environ.get("ASM_RANGE_IDX", "range")
    if os.environ.get("ASM_STEPS"):            # ASM_STEPS=<first step>:<step after the last> (by id), with ASM_RANGE_IDX
        a_, b_ = os.environ["ASM_STEPS"].split(":")
        fi = [i for i, p in enumerate(plan) if p["step"] == a_] if a_ else [0]     # "" : from the chapter's opening
        lo = fi[0] if fi else tot_frames
        fj = [i for i, p in enumerate(plan) if p["step"] == b_] if b_ else []
        hi = fj[0] if fj else (10 ** 9 if not b_ else tot_frames)
        part, k_ = "steps", os.environ.get("ASM_RANGE_IDX", "steps")
    if PICK is not None:
        part, k_ = "pick", "pick"
    if os.environ.get("ASM_PLAN_ONLY") == "1":
        import json as _j
        out = dict(chapter=name, frames=tot_frames, shots=st,
                   steps={p["step"]: i for i, p in reversed(list(enumerate(plan)))})
        (common.DATA / f"{name}-plan.json").parent.mkdir(parents=True, exist_ok=True)
        (common.DATA / f"{name}-plan.json").write_text(_j.dumps(out, indent=1))
        print(f"{name}: plan only, {tot_frames} frames", flush=True)
        return dict(n=tot_frames)
    ch = common.Chapter(f"{name}.part{k_}" if part else name, title)
    ch.n = lo
    tot = _play(rp, ev, nfr, fail_notes, fail_steps, cams=cams, ch=ch, lo=lo, hi=hi, max_frames=max_frames)
    ch.close()
    (ch.dir / "shots.json").write_text(json.dumps(dict(stats=st, lo=lo, hi=min(hi, tot_frames), total=tot_frames)))
    print(f"{name}: {tot['n']} frames played, {tot['drawn']} drawn ({lo}..{min(hi, tot_frames)})", flush=True)
    return tot


def _play(rp, ev, nfr, fail_notes, fail_steps, plan=None, scores=None, cams=None, ch=None, lo=0, hi=10 ** 9, max_frames=None):
    """Plays the events. Pass 1 (plan is a list): records, per frame, where the work is (and the tripods' occlusion once per
    step at a place); nothing is drawn. Pass 2 (cams): draws frames lo..hi-1 with the chosen tripod."""
    drawing = cams is not None
    rows = {}
    for e in ev:
        if e["kind"] == "step_end" and not e.get("failed_run"):
            rows[e["id"]] = e
    cur = dict(id="", label="", status="", actor="A", do="", t=0.0, failed=False)
    tot = dict(n=0, drawn=0)
    snap = {}
    carry = dict(s=0.0, robot=0.0)
    note = dict(txt="", left=0)          # a short note carried onto the next frames' second line (an ellipsis, a jump)
    fetch_t = {}                         # arm -> seconds of a fetch not shown so far (drive out and the pick)
    last = dict(loc=("cell",), force=False)
    scored = {}

    def score(key, loc, work):
        """Occlusion of each of the place's tripods for the work point, at most 3 samples per step and place."""
        if scores is None or work is None or scored.get(key, 0) >= 3:
            return
        scored[key] = scored.get(key, 0) + 1
        import vtk
        try:
            tree = rp._occluders(work)
        except Exception:   # noqa: BLE001
            return
        work = np.asarray(work, float)
        pts = [work] + [work + 45.0 * np.array([math.cos(a), math.sin(a), 0.3]) for a in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
        hp = vtk.vtkPoints()
        d = scores.setdefault(key, {})
        for c in place_cands(loc):
            cam = np.asarray(cam_def(c)[0], float)
            blocked = 0
            for P in pts:
                hp.Reset()
                if tree.IntersectWithLine(cam.tolist(), P.tolist(), hp, None):
                    dmin = min(np.linalg.norm(np.array(hp.GetPoint(j)) - cam) for j in range(hp.GetNumberOfPoints()))
                    if dmin < np.linalg.norm(P - cam) - 15.0:
                        blocked += 1
            d.setdefault(c, []).append(blocked / len(pts))

    def emit(caption, sub="", who=(), proc=1.0 / FPS, add=None, status=None, loc=None, work=None, force=False):
        st_ = status if status is not None else cur["status"]
        if carry["s"] > 0.0:            # motions not drawn: their real time goes with this frame
            proc += carry["s"]
            if carry["robot"] > 0.0:
                add = dict(add or {})
                add["robot_h"] = add.get("robot_h", 0.0) + carry["robot"] / 3600.0
            carry["s"] = carry["robot"] = 0.0
        if note["left"] > 0:
            sub = (sub + "; " if sub else "") + note["txt"]
            note["left"] -= 1
        if loc is None:
            loc = last["loc"]
        force = force or last["force"]
        if cur["id"] in CUTS and not cur.get("emitted"):
            force = True                   # a slice boundary (ASM_CUTS): the same cut in every slice's plan
        cur["emitted"] = True
        last["loc"], last["force"] = loc, False
        if plan is not None:
            plan.append(dict(loc=loc, key=(cur["id"], loc), work=None if work is None else np.asarray(work, float).copy(),
                             force=force, step=cur["id"]))
        if drawing and lo <= tot["n"] < hi and (PICK is None or tot["n"] in PICK):
            pos, foc, va = cam_def(cams[tot["n"]])
            rp.sc.camera([pos, foc, (0.0, 0.0, 1.0)], view_angle=va)
            img = rp.sc.render()
            meta = dict(sub=sub, who=list(who), step=cur["id"], status=st_, proc_s=round(proc, 4), cam=cams[tot["n"]])
            if add:
                meta["add"] = add
            if PICK is not None:
                ch.n = tot["n"]
            ch.frame(img, caption, **meta)
            tot["drawn"] += 1
        tot["n"] += 1
        cur["t"] += proc
        return (max_frames is not None and tot["n"] >= max_frames) or (drawing and tot["n"] >= hi)

    def step_status(sid, failed_run):
        if failed_run:
            return "fail"
        e = rows.get(sid)
        if e is None:
            return ""
        s = e["status"]
        if s == "pass" and sid in fail_steps:
            return "redesign"
        return s

    def lapse_txt(real_per_frame):
        x = real_per_frame * FPS
        return "" if x < 1.3 else f"; shown x{x:.0f}"

    def here(n):
        """Where arm n works now: at the table where its MiR stopped (the tripods are set up there), else the place in the
        cell under its tool."""
        xm = rp.st[n]["x"]
        if xm > TABLE_X:
            return ("table", round(xm / 100.0) * 100.0, n)
        return loc_of_x(float(rp.tcp(n)[0]))

    stop = False
    for i_ev, e in enumerate(ev):
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
                rp.st[n]["pose"] = None
                rp.set_arm(n)
            for i, T in e["present"].items():
                rp.put([i], T)
            if tot["n"] == 0:
                # the overview first: the whole cell and the near end of the table, both robots parked
                for _ in range(int(FPS * 4.0)):
                    stop = emit(CHAP_TITLE.get(rp.chapter, ""), "the assembly bench, Fixtures P and B, the trunnion, both MiR250 + "
                                "UR12e and the long parts table", [], proc=0.0, loc=("cell",))
                    if stop:
                        break
            continue
        if k == "snapshot":
            snap = dict(G={kk: v.copy() for kk, v in rp.sc.gmat.items()}, A={kk: v for kk, v in rp.sc.alpha.items()},
                        st={n: dict(rp.st[n]) for n in ("A", "B")})
            continue
        if k == "restore":
            if snap:
                rp.sc.gmat.update(snap["G"])
                rp.sc.alpha.update(snap["A"])
                for n in ("A", "B"):
                    rp.st[n] = dict(snap["st"][n])
                    rp.set_arm(n)
            continue
        if k == "step":
            failed = bool(e.get("failed_run"))
            label = e["label"]
            if failed:
                label = "[first attempt, earlier design] " + label
            elif e["id"] in fail_steps:
                label = "[redesigned] " + label
            cur = dict(id=e["id"], label=label, status=step_status(e["id"], failed), actor=e.get("actor") or "A", do=e.get("do"),
                       t=0.0, failed=failed)
            n0 = cur["actor"] if cur["actor"] in ("A", "B") else "A"
            if not failed and e["id"] in fail_notes:
                what, _, fix = str(fail_notes[e["id"]]).partition("Round 7:")
                txt = "FAILED in an earlier run: " + what.strip().rstrip(".") + (". Now: " + fix.strip() if fix else "")
                for _ in range(int(FPS * 3.0)):
                    stop = emit(e["label"], txt[:178], [f"robot {n0}"], status="redesign", loc=here(n0))
                    if stop:
                        break
            row = (rows.get(e["id"]) or {}).get("row") or {}
            if not failed and row.get("fetch") in ("FAIL", "person"):
                # the pick at the table was not planned (or a person stages the part): not animated as if it worked. A person
                # brings the part to the station and puts it in the gripper (a card; the person is drawn there)
                why_f = (row.get("fetch_why") or "")[:70]
                if rp.person is not None:
                    xm = rp.st[n0]["x"]
                    yp = (-1.0 if n0 == "A" else 1.0) * 1450.0
                    rp.person.show(1.0)
                    rp.person.set(x=xm - 650.0, y=yp, hd=(40.0 if n0 == "A" else -40.0), amp=0.0, look=(xm, yp * 0.5, 1000.0))
                txt = ("pick at the parts table NOT planned" + (f" ({why_f})" if why_f else "") if row.get("fetch") == "FAIL"
                       else "a person stages the part at the station") + ": a person brings it and puts it in the gripper (estimate 2 min)"
                for _ in range(int(FPS * 4.0)):
                    stop = emit(cur["label"], txt, ["person"], status="person", loc=here(n0))
                    if stop:
                        break
                if rp.person is not None:
                    rp.person.show(0.0)
            continue
        if k == "step_end":
            if cur["status"] in ("fail",) or e.get("status") == "fail":
                why = (e.get("row") or {}).get("why") or ""
                for _ in range(int(FPS * 2.5)):
                    stop = emit(cur["label"], f"FAILED: {why[:110]}", [], status="fail")
                    if stop:
                        break
            continue
        n = e.get("arm")
        if n == "A+B":
            n = None
        side = n or cur.get("actor") or "A"
        if side not in ("A", "B"):
            side = "A"
        who = [f"robot {side}"]
        nf, per = nfr.get(id(e), (0, 1.0 / FPS))
        if nf == 0 and float(e.get("dur", 0.0)) > 0.0 and k in ("grip", "drive", "move", "screw", "tool"):
            # not drawn: jump to where the motion ends, keep its time for the next frame drawn, and cut there
            if k == "grip":
                rp.set_arm(n, close=e["c1"])
            elif k == "drive":
                rp.st[n]["pose"] = None
                rp.set_arm(n, x=e["x1"])
                rt = e.get("route") or {}
                if e["x1"] > TABLE_X:
                    fetch_t[n] = float(e["dur"])
                    note["txt"] = (f"MiR {n} drove to the parts table ({e['dur']:.0f} s: " +
                                   (f"{rt.get('n_pivots', 0)} pivots, {rt.get('dist_mm', 0) / 1000:.1f} m; " if rt else "") + "not shown)")
                else:
                    tt = fetch_t.pop(n, 0.0) + float(e["dur"])
                    note["txt"] = (f"arm {n} fetched it from the parts table: drive, pick and drive back {tt:.0f} s, "
                                   + ("each leg pivot-drive-pivot, " if rt else "") + "checked, not shown")
                note["left"] = 36
                last["force"] = True
            elif k in ("move", "screw") and e.get("q") is not None and len(e["q"]):
                rp.set_arm(n, q=np.asarray(e["q"][-1], float), close=e.get("close"))
                if e.get("unplanned"):
                    for _ in range(int(FPS * 1.5)):
                        stop = emit(cur["label"], f"NOT PLANNED: no checked path for arm {n}'s move here; not shown", who,
                                    status="fail", loc=here(n))
                        if stop:
                            break
                    last["force"] = True
            elif k == "tool":
                rp.st[n]["spec"] = e.get("spec") or {}
                rp.set_arm(n, tool=e["tool"])
            carry["s"] += float(e["dur"])
            carry["robot"] += float(e["dur"])
            continue
        if k == "jump":
            # the recording's next motion does not start where the arm is: never drawn as a jump inside a shot
            rp.set_arm(n, q=np.asarray(e["to"], float))
            last["force"] = True
            continue
        if k == "put":
            rp.put(e["objs"], e["T"])
        elif k == "take":
            for i in e["objs"]:
                if rp.objs.get(i, {}).get("kind") == "tool" and f"o{i}" in rp.sc.actors:
                    rp.sc.alpha[f"o{i}"] = 0.0         # a hand tool goes back to the stand
        elif k == "attach":
            rp.st[n]["held"] = dict(objs=e["objs"], off=np.asarray(e["off"], float))
            rp.set_arm(n)
        elif k == "detach":
            rp.st[n]["held"] = None
        elif k == "tool":
            rp.st[n]["spec"] = e.get("spec") or {}
            rp.set_arm(n, tool=e["tool"])
            for f in range(nf):
                stop = emit(cur["label"], f"tool change at the MiR's stand: {e['tool']} (ATI QC-21; {e['dur']:.0f} s, estimate)",
                            who, proc=per, add={"robot_h": per / 3600.0}, loc=here(n))
                if stop:
                    break
        elif k == "grip":
            for f in range(nf):
                s = smooth((f + 1) / nf)
                rp.set_arm(n, close=e["c0"] + (e["c1"] - e["c0"]) * s)
                stop = emit(cur["label"], "2F-85 " + ("closes" if e["c1"] > e["c0"] else "opens"), who, proc=per,
                            add={"robot_h": per / 3600.0}, loc=here(n), work=rp.tcp(n))
                if stop:
                    break
        elif k == "drive":
            rt = e.get("route")
            chk = e.get("check") or {}
            loc = ("lane", n) if max(e["x0"], e["x1"]) > TABLE_X else ("cell",)
            T_all = float(e["dur"])
            for f in range(nf):
                t = T_all * (f + 1) / nf
                if rt:
                    rp.st[n]["pose"] = route_pose(rt, t)
                    rp.set_arm(n)
                else:
                    rp.st[n]["pose"] = None
                    rp.set_arm(n, x=e["x0"] + (e["x1"] - e["x0"]) * smooth((f + 1) / nf))
                if rt:
                    sub = (f"MiR {n}: pivot, drive, pivot, {rt['dist_mm'] / 1000:.1f} m and {rt['n_pivots']} pivots "
                           + ("to the parts table" if e["x1"] > TABLE_X else ("back to the bench" if e["x0"] > TABLE_X else "along the bench"))
                           + f" ({e['dur']:.0f} s: 1 m/s, 0.3 m/s2; pivots 30 deg/s, estimate{lapse_txt(per)})")
                else:
                    sub = f"MiR {n} drives {abs(e['x1'] - e['x0']) / 1000:.1f} m ({e['dur']:.0f} s{lapse_txt(per)})"
                if chk and not chk.get("ok", True):
                    sub += f"; NOT CLEAR: {chk.get('why', '')[:60]}"
                stop = emit(cur["label"], sub, who, proc=per, add={"robot_h": per / 3600.0}, loc=loc,
                            status="fail" if (chk and not chk.get("ok", True)) else None)
                if stop:
                    break
            rp.st[n]["pose"] = None
            rp.set_arm(n, x=e["x1"])
            last["force"] = True                  # cut after a drive, back to the work
        elif k in ("move", "screw"):
            Q = e.get("q")
            if Q is None or len(Q) == 0:
                if k == "screw":
                    later = [x for x in ev[i_ev + 1:i_ev + 40] if x.get("step") == e.get("step") and x["kind"] == "screw"
                             and x.get("obj") == e.get("obj") and x.get("ok")]
                    if later:
                        o = later[0].get("arm") or ("B" if n == "A" else "A")
                        why_s = str(e.get("why", "")).replace("approach: ", "").split(" (")[0][:70]
                        for _ in range(int(FPS * 1.0)):
                            stop = emit(cur["label"], f"arm {n} can't reach this screw ({why_s}); arm {o} drives it", who, loc=here(n))
                    else:
                        for _ in range(int(FPS * 1.5)):
                            stop = emit(cur["label"], f"screw not driven: {e.get('why', '')[:90]}", who, status="fail", loc=here(n))
                continue
            Q = np.asarray(Q, float)
            d = np.r_[0.0, np.cumsum(np.abs(np.diff(Q, axis=0)).max(axis=1))] if len(Q) > 1 else np.array([0.0])
            L = d[-1] if d[-1] > 0 else 1.0
            in_table = rp.st[n]["x"] > TABLE_X
            # where this motion's work is: where it ends (the part seated, the screw home, the pick)
            q_keep = rp.st[n]["q"].copy()
            rp.st[n]["q"] = Q[-1]
            w_end = rp.tcp(n).copy()
            loc = here(n)
            rp.st[n]["q"] = q_keep
            o = "B" if n == "A" else "A"
            holding = rp.st[o]["held"] is not None and k == "screw"
            if k == "screw" or e.get("how") == "cart":
                score((cur["id"], loc), loc, w_end)
            for f in range(nf):
                s = smooth((f + 1) / nf) * L
                if len(Q) > 1:
                    j = int(min(max(np.searchsorted(d, s, side="right") - 1, 0), len(Q) - 2))
                    t = (s - d[j]) / max(d[j + 1] - d[j], 1e-9)
                    q = Q[j] * (1 - t) + Q[j + 1] * t
                else:
                    q = Q[0]
                if k == "screw" and rp.st[n]["held"] is not None:
                    turns = e["L"] / max(e["pitch"], 0.1)
                    rp.st[n]["held"]["spin_deg"] = (360.0 * min(turns * (f + 1) / nf, 2.0 * (f + 1))) % 360.0
                rp.set_arm(n, q=q, close=e.get("close"))
                if k == "screw":
                    msz = {0.5: 3, 0.7: 4, 0.8: 5, 1.0: 6}.get(round(float(e.get("pitch", 0.7)), 1), "")
                    sub = (f"{e['tool']}: M{msz} screw runs down {e['L']:.0f} mm and is torqued to {float(e.get('torque') or 0):.1f} N m "
                           f"({e['dur']:.0f} s{lapse_txt(per)})")
                    if holding:
                        sub = f"arm {o} holds the part while arm {n} drives; " + sub
                elif in_table and e.get("how") == "cart":
                    sub = "pick at the parts table (checked against the table, its nest and the neighbouring parts)"
                elif e.get("how") == "plan":
                    sub = f"planned move, collision-checked{lapse_txt(per)}"
                else:
                    sub = "checked straight-line move" + (" with the part" if e.get("held") else "") + lapse_txt(per)
                stop = emit(cur["label"], sub, (who + [f"robot {o}"]) if holding else who, proc=per,
                            add={"robot_h": (2 if holding else 1) * per / 3600.0}, loc=loc, work=w_end)
                if stop:
                    break
        elif k == "move2":
            QA, QB = np.asarray(e["qA"], float), np.asarray(e["qB"], float)
            rp.set_arm("A", q=QA[-1], close=e["closeA"])
            rp.set_arm("B", q=QB[-1], close=e["closeB"])
            mid_end = 0.5 * (rp.tcp("A") + rp.tcp("B"))
            loc = loc_of_x(float(mid_end[0]))
            score((cur["id"], loc), loc, mid_end)
            for f in range(nf):
                j = min(len(QA) - 1, int(round(smooth((f + 1) / nf) * (len(QA) - 1))))
                rp.set_arm("A", q=QA[j], close=e["closeA"])
                rp.set_arm("B", q=QB[j], close=e["closeB"])
                mid = 0.5 * (rp.tcp("A") + rp.tcp("B"))
                if e.get("lift_aid"):
                    rp.sc.alpha["hoist"] = 1.0
                    rp.sc.gmat["hoist"] = Tm((float(mid[0]), float(mid[1]), float(mid[2]) + 60.0))
                    stop = emit(cur["label"], f"a small hoist takes the load (person at its pendant); both arms guide it along the checked path"
                                f"{lapse_txt(per)}", ["robot A", "robot B", "person"], proc=per,
                                add={"robot_h": 2 * per / 3600.0, "person_h": per / 3600.0}, loc=loc, work=mid)
                else:
                    stop = emit(cur["label"], f"both arms carry it together, checked frame by frame{lapse_txt(per)}", ["robot A", "robot B"],
                                proc=per, add={"robot_h": 2 * per / 3600.0}, loc=loc, work=mid)
                if stop:
                    break
            rp.sc.alpha["hoist"] = 0.0
        elif k == "turn":
            T0 = np.asarray(e["T0"], float)
            TT = np.asarray(e["TT"], float)
            J0 = rp.sc.gmat["jaws"].copy()
            for f in range(nf):
                th = e["sign"] * 180.0 * smooth((f + 1) / nf)
                Rm = TT @ rot_axis((1, 0, 0), th) @ np.linalg.inv(TT)
                rp.put(e["objs"], Rm @ T0)
                rp.sc.gmat["jaws"] = Rm @ J0
                stop = emit(cur["label"], "the trunnion turns the chamber over; both arms parked", ["machine"], proc=per, loc=("PT",),
                            work=TT[:3, 3])
                if stop:
                    break
        elif k == "wait":
            wh = e.get("who", "person")
            n0 = cur["actor"] if cur["actor"] in ("A", "B") else "A"
            loc = here(n0)
            if wh == "person" and rp.person is not None:
                rp.person.show(1.0)
                xp = {"bench": -1250.0, "PT": 0.0, "B": 1350.0}.get(loc[0], float(rp.st[n0]["x"]))
                rp.person.set(x=xp - 500.0, y=-1300.0, hd=70.0, amp=0.0, look=(xp, -200.0, 950.0))
            for f in range(nf):
                sub = (f"{e.get('what', '')[:80]} ({e['dur'] / 60:.0f} min, estimate{lapse_txt(per)})" if wh == "person" else
                       f"{e.get('what', '')[:80]} ({e['dur']:.0f} s)")
                stop = emit(cur["label"], sub, [wh] if wh in ("person", "machine") else ["robot A"], proc=per,
                            add={"person_h": per / 3600.0} if wh == "person" else ({"robot_h": per / 3600.0} if wh == "robot" else None),
                            status="person" if wh == "person" else None, loc=loc)
                if stop:
                    break
            if rp.person is not None:
                rp.person.show(0.0)
    return tot


CHAP_TITLE = {k: v[1] for k, v in CHAP.items()}
# ASM_PICK=12,340,...: draw only these frames (a look at stills before a full render), into <chapter>.partpick/ with the
# frame numbers as file names (not for merging)
PICK = {int(x) for x in os.environ["ASM_PICK"].split(",")} if os.environ.get("ASM_PICK") else None
# ASM_CUTS=F10a,F31: a cut at each of these steps' first frame, so a chapter can be rendered in slices (ASM_STEPS) while the
# planner is still running: nothing in the shot plan reaches across a forced cut, so each slice's frames are the same as the
# whole chapter's would be (give every slice the same ASM_CUTS)
CUTS = {x for x in os.environ.get("ASM_CUTS", "").split(",") if x}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = {a.split("=")[0][2:]: (a.split("=", 1)[1] if "=" in a else "1") for a in sys.argv[1:] if a.startswith("--")}
    run(args[0] if args else "module", max_frames=int(opt["max"]) if "max" in opt else None, scale=float(opt.get("scale", 1.0)),
        fail_pkl=opt.get("fails"), fail_steps=tuple(x for x in opt.get("fail_steps", "").split(",") if x),
        fail_notes=json.loads(pathlib.Path(opt["fail_notes"]).read_text()) if "fail_notes" in opt else None)
