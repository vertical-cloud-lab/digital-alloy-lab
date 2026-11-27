"""Chapters 40-assembly-module and 41-assembly-chamber of the robot-built video (issue #260, PR #266, round 7): the
two-arm assembly replayed from the recorded, collision-checked trajectories (analysis/assembly/run_assembly.py with
ASM_RECORD, record.py), on the shared look and frame contract (common.py).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python asm_render.py module|chamber [--max=N] [--fps=12]

Reads /tmp/robotbuild/traj/asm_scene.pkl (every object's mesh and its slot on the long table) and asm_<chapter>.pkl (the
event stream), writes /tmp/robotbuild/frames/40-assembly-module/ or 41-assembly-chamber/ (common.Chapter).

Time: every event carries its real-world duration (record.py's speeds); a frame stands for 1/12 s of it at real time, or
more in a time-lapse (drives, repeated screws, a person's long jobs), and the frame's `proc_s` and `sub` say which. The
`add` counters sum the robots' working time (robot_h: arm A and arm B separately added) and the persons'.

Round 8 (Sterling, 2026-11-26: "moonwalk, motion sickness, collisions and interference"):
  * Fixed tripods (the camera rig, RIG / cam_def): a few per place in the cell (the bench from its end and from above each
    lane, Fixture P and the trunnion, Fixture B), three set up wherever a MiR stops at the parts table, a wide view of the
    cell, and one down each lane for drives. Pass 1 plays the chapter without drawing and records where the work is in every
    frame; the shot for a step at a place is the least occluded of that place's tripods (rays to points round the work, cast
    a few times per step), a shot shorter than MIN_SHOT is merged into a neighbour that also shows its work, and pass 2 draws.
    The camera never moves inside a shot; a cut is forced wherever something moved without being drawn (a fetch not shown,
    a jump in the recording), always to a different tripod. Each frame's meta has `cam`.
  * MiRs move as recorded by mir_route.py: pivot, drive along the heading, pivot (route legs in the drive event).
  * Every arm motion is drawn (round 7's capped mode cut transit moves, so arms jumped inside a shot); the chapter's first
    DRIVE_SHOW drives to and from the table and first PICK_SHOW picks are drawn, later ones are an ellipsis: checked and
    timed, not drawn, with a cut and a line saying so. A pick the planner could not plan, or a move it could not plan, is
    never animated: a card says what failed and who does it instead (a person brings the part; the person is drawn).
  * Slices: ASM_PART=k/n (by frames), ASM_RANGE=lo:hi, or ASM_STEPS=<first step>:<step after the last> with ASM_RANGE_IDX=k,
    and ASM_CUTS=<step,...> (a forced cut at each, the same in every slice) so a chapter can be rendered slice by slice while
    the planner is still writing its chunks (record.py). ASM_UPTO=<step> stops before that step (41 stops before T01: the
    integration chapter draws T01-T06). ASM_PLAN_ONLY=1: pass 1 only, the frame and shot plan to <data>/<chapter>-plan.json.
    ASM_PICK=n,m,...: draw only those frames (a look at stills before a full render).

Round 9 (2026-11-27; round 8's frame audit and camera check; Sterling: "showing where a human is absolutely necessary"):
  * The seal steps' hand tools go back to their stand when their step ends (the recording has no "take" for them, so round 8
    left one inside the module from frame 2792 to the end). Objects are drawn at the scene file's 12,000 triangles (2,500
    closed bores and counterbores). A put of parts an arm still holds re-anchors the hold, so they stay where the planner
    seated them (M19's heater stack sat 2.4 mm off its bore for 500 frames). The hoist hook is drawn at the planner's points.
  * The person walks in from the aisle beside the cell to a spot that is clear on the floor plan (MiRs with their tool stands
    and presenters, arms, bench, fixtures, table, parts in the cell) and out of the place's tripods' lines of sight, and out
    again, their feet locked by people.py's Gait (W1, round 9) at 450 mm/s; after a failed step they set each part the arms
    could not (it appears in its seat as their hands reach it) and drive each screw no arm could, with a hand driver (5 min a
    part, 1 min a screw, time-lapsed), status "person".
  * Camera: a cut is forced only where something jumped; a fetch not shown holds the shot when the MiR and arm come back to
    where they were; small arm jumps (<= 5 deg) are drawn as a labelled reposition; slice boundaries are soft (README).

Round 10 (2026-11-27; round 9's frame audit and walk check):
  * The person's heading follows people.py's convention (0 = facing +y): round 9 passed atan2(dy, dx), so they walked in and
    out sideways (the Gait side-stepped at up to 675 mm/s and dragged the planted foot: 34 mm a stance in 40 and 41) and
    stood side-on to the work. Back-to-back person jobs: they turn round where they stand instead of being put back at the
    aisle turned 180 deg in one frame (205-383 mm of "slip" in 41).
  * The person's spot and poses are checked in 3-D against everything drawn, with the frame audit's own measure
    (Replay.person_hits: scene_audit.py's translational depth, 1.5 mm): spots in tiers (walked to within reach, put in
    place within reach, then anywhere clear), the hands on the part's outside 25 mm or more off its surface (palms down
    over its top, on its front or sides, one hand), the hand driver 120-200 mm up the screw's axis, leaning in to reach.
    A spot may stand in some of the place's tripods' sight lines; the person's frames are then shot from another. Round 9
    aimed the hands at the part's centre (a hand 28 mm in the chamber body) and found no spot at all round Fixture B.
  * A failed placement: every part the arm left more than 1.5 mm off its seat (or never drew) is set by the person (round 9:
    only those more than 50 mm off, so F57's beam tube, 9 mm short, was put in its seat with no one drawn doing it).
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
MAX_TRI = int(os.environ.get("ASM_MAX_TRI", "12000"))    # per object, for drawing only (round 9: the scene file's own 12,000;
                                                         # round 8's 2,500 closed bores and counterbores, so tools and screws
                                                         # in them read as tens of mm deep in the frame audit)


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


def face_hd(dx, dy):
    """people.py's heading (deg about z, 0 = facing +y, forward (-sin hd, cos hd)) of a person facing along (dx, dy).
    Round 10: round 9 used atan2(dy, dx), 90 deg off: the person walked in and out sideways (people.py's Gait side-stepped
    at up to 675 mm/s, outran its steps and dragged the planted foot: walk.py's 34 mm a stance in 40 and 41) and stood
    side-on to the work, reaching across their body."""
    return math.degrees(math.atan2(-float(dx), float(dy)))


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
        self.temp_tools, self.retired = set(), set()     # round 9: the seal steps' hand tools, and those back in their stand
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
            self.temp_tools.add(i)
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
        # ---- the person's screwdriver (round 9: a person drives the screws no arm could): tip at the origin, along +z
        drv = pv.Cylinder(center=(0, 0, 55), direction=(0, 0, 1), radius=2.5, height=110).triangulate().merge(
            pv.Cylinder(center=(0, 0, 160), direction=(0, 0, 1), radius=14, height=100, resolution=16).triangulate())
        sc.add("op/tool/screwdriver", drv, "#c0392b", group="op/tool", specular=0.3, shown=False)
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
        if hasattr(K, "T_blade_nest"):      # round 10 (W2, F26a-F27): the blade cartridge's two-pin bench nest
            out.append(("Blade nest", tx(TL.mesh("nest_blade")[0], K.T_blade_nest()), "#c9a227"))
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
            T_tcp = a.tcp(s["q"], h.get("close0", s["close"]))
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
            if i in self.retired:          # a hand tool back in its stand stays there
                continue
            if f"o{i}" in self.sc.actors:
                self.sc.gmat[f"o{i}"] = np.asarray(T, float)
                self.sc.alpha[f"o{i}"] = 1.0
        # round 9: a put of parts an arm still holds (seated, then held while the other arm drives the first screws; a flip;
        # a carry) re-anchors the hold at the put, so they stay where the planner seated them. Round 8 kept riding them on the
        # drawn TCP until the release and left them there: M19's heater stack sat 2.4 mm off its bore's axis for 500 frames
        # (the frame audit read the piston head 53 mm deep), until the next put of the module
        for n in ("A", "B"):
            h = self.st[n]["held"]
            if h is not None and set(h["objs"]) & set(objs):
                a = self.arm[n]
                T_tcp = a.tcp(self.st[n]["q"], h.get("close0", self.st[n]["close"]))
                if h.get("spin_deg"):
                    T_tcp = T_tcp @ rot_axis((0, 0, 1), h["spin_deg"])
                h["off"] = np.linalg.inv(T_tcp) @ np.asarray(T, float)

    def tcp(self, n):
        a = self.arm[n]
        return a.tcp(self.st[n]["q"], self.st[n]["close"])[:3, 3]

    def retire_tools(self, idx=None):
        """Round 9: the seal steps' hand tools (ring loader, spigot mandrel and pusher) go back to the stand when the step that
        used them ends, or at a "take" event: hidden for good. Round 8 drew them where they were last put until the chapter's
        end, so after the module's flips (M26, M28) they stood up to 78 mm inside it (the recording has no "take" for them)."""
        for i in (self.temp_tools if idx is None else idx):
            if i not in self.temp_tools:
                continue
            k = f"o{i}"
            if self.sc.alpha.get(k, 0.0) > 0.0 or idx is not None:
                self.sc.alpha[k] = 0.0
                self.retired.add(i)
            for n in ("A", "B"):
                h = self.st[n]["held"]
                if h is not None and i in h["objs"]:
                    h["objs"] = [j for j in h["objs"] if j != i]
                    if not h["objs"]:
                        self.st[n]["held"] = None

    # ------------------------------------------------------------------------------------------- the person (round 9)
    # Round 8 put the person on the spot for a person's job or a pick no arm could plan, wherever that was: their legs stood in
    # MiR A's tool stand (chapter 41, frames 429-452, 3881-3904, 4384-4419), and they appeared and vanished inside a shot. Now
    # the person's spot is checked clear on the floor plan (MiRs with their tool stands and presenters, both arms, the bench,
    # fixtures, table and pallets, the parts in the cell), and they walk in from the aisle beside the cell and out again,
    # their feet locked (people.py's Gait, round 9), never through a MiR.
    PERSON_R = 330.0              # clearance of a standing person's centre from anything (shoulders, elbows, a step), mm
    PERSON_R_SPOT = 240.0         # round 10: of the spot they work from (their body is then checked in 3-D), mm
    AISLE = 2700.0                # |y| of the aisle the person comes from: under the side tripods, out of their pictures
    # round 10: the person's posed body checked against everything drawn, with the frame audit's own measure (scene_audit.py:
    # python-fcl, translational penetration depth over 1.5 mm). Round 9 aimed the hands at the part's centre and checked only
    # the floor plan, so a hand stood 28 mm in the chamber body where the person set a part (chapter 41, frames 6078-6092)
    SKIP_PERSON = ("iris", "sclera", "brow", "hair")
    OWN_MM = 10.0                 # how far the hands may reach into the part they set or the screw they drive (the fingers
                                  # curl past the palm's target; scene_audit allows 25 mm), mm

    def _geom(self, name):
        """scene_audit.Geom of an actor's mesh as drawn (its own coordinates), cached by the mesh object and its version."""
        import audit_rec
        import scene_audit as SA
        from vtk.util.numpy_support import vtk_to_numpy
        cache = self.__dict__.setdefault("_geoms", {})
        actor = self.sc.actors[name]
        poly = actor.GetMapper().GetInput() if actor.GetMapper() is not None else None
        if poly is None or poly.GetNumberOfPoints() == 0:
            return None
        key = (id(poly), int(poly.GetMTime()))
        g = cache.get(name)
        if g is None or g[0] != key:
            V = vtk_to_numpy(poly.GetPoints().GetData()).astype(float)
            F = audit_rec._faces(poly)
            if not len(F):
                return None
            g = cache[name] = (key, SA.Geom(V, F, name))
        return g[1]

    def person_hits(self, P, own=(), own_mm=None, extra=(), limit=None):
        """Round 10: [(the person's part or extra actor, what it is in, depth mm)] for every pair deeper than the audit's 1.5 mm
        between the person as posed now (and `extra` actors, e.g. their hand driver) and anything drawn (opacity >= 0.3; not
        the floor). `own`: actor names (the part they set, the screw they drive) the hands, forearms and driver may reach
        into up to own_mm. Stops at `limit` hits."""
        import scene_audit as SA
        fcl = SA._fcl()
        own_mm = self.OWN_MM if own_mm is None else float(own_mm)
        sc = self.sc
        mine = []
        for part, (V, F) in P.posed().items():
            if part in self.SKIP_PERSON or not len(F):
                continue
            g = SA.Geom(np.asarray(V, float), np.asarray(F, np.int32), f"{P.n}/{part}")
            mine.append((f"{P.n}/{part}", g, np.eye(4)))
        for nm in extra:
            g = self._geom(nm)
            if g is not None and sc.alpha.get(nm, 0.0) > 0.0:
                mine.append((nm, g, sc.world(sc.group_of[nm])))
        if not mine:
            return []
        boxes = [SA.world_box(g.corners, M) for _, g, M in mine]
        lo = np.min([b[0] for b in boxes], axis=0) - 5.0
        hi = np.max([b[1] for b in boxes], axis=0) + 5.0
        skip = set(extra) | {"floor"}
        groups = set(getattr(P, "groups", ()))
        out = []
        for name in list(sc.actors):
            if name in skip or sc.group_of.get(name) in groups or name.startswith(f"{P.n}/"):
                continue
            if sc.alpha.get(name, 1.0) * sc.base_alpha.get(name, 1.0) < SA.OPAQUE or sc.alpha.get(name, 1.0) <= 0.02:
                continue
            g = self._geom(name)
            if g is None:
                continue
            Mo = sc.world(sc.group_of[name])
            olo, ohi = SA.world_box(g.corners, Mo)
            if np.any(olo > hi) or np.any(ohi < lo):
                continue
            ob = None
            for (pn, pg, Mp), (plo, phi) in zip(mine, boxes):
                if np.any(olo > phi) or np.any(ohi < plo):
                    continue
                if ob is None:
                    ob = fcl.CollisionObject(g.model(), fcl.Transform(Mo[:3, :3].astype(float), Mo[:3, 3].astype(float)))
                oa = fcl.CollisionObject(pg.ero(), fcl.Transform(Mp[:3, :3].astype(float), Mp[:3, 3].astype(float)))
                ca, cb = 0.5 * (plo + phi), 0.5 * (olo + ohi)
                d = SA.tdepth(fcl, oa, Mp, ob, ca, cb, need=SA.DEPTH_MM, ga=pg, gb=g, Mb=Mo, swallow=True, refine=True)
                if d <= SA.DEPTH_MM:
                    continue
                hand = pn.endswith(("/glove", "/forearm", "/skin")) or pn in extra
                if name in own and hand and d <= own_mm:
                    continue
                out.append((pn, name, round(float(d), 1)))
                if limit and len(out) >= limit:
                    return out
        return out

    def _static_boxes(self):
        if getattr(self, "_sboxes", None) is None:
            out = []
            for name, actor in self.sc.actors.items():
                if self.sc.group_of.get(name) != "static" or name == "floor":
                    continue
                b = actor.GetMapper().GetInput().GetBounds() if actor.GetMapper() is not None else None
                if b is None or b[4] > 1900.0 or b[5] < 40.0:
                    continue
                out.append((b[0], b[2], b[1], b[3]))
            self._sboxes = out
        return self._sboxes

    def floor_boxes(self):
        """2-D boxes (x0, y0, x1, y1) of what a person on the floor could walk into now."""
        out = list(self._static_boxes())
        for n in ("A", "B"):
            s = self.st[n]
            for _, (v, f), _ in self.K.mir_bodies(n, s["x"], "front" if n == "A" else "back"):
                v = np.asarray(v, float)
                out.append((v[:, 0].min(), v[:, 1].min(), v[:, 0].max(), v[:, 1].max()))
            a = self.arm[n]
            a.move_base(s["x"])
            a.place(s["q"], s["close"])
            for b in list(a.links.values()) + list(a.grip.values()):
                w = b.v @ b.M[:3, :3].T + b.M[:3, 3]
                out.append((w[:, 0].min(), w[:, 1].min(), w[:, 0].max(), w[:, 1].max()))
            self.set_arm(n)                  # the arm as drawn again (place() above moved its bodies)
        for i, o in self.objs.items():
            k = f"o{i}"
            if self.sc.alpha.get(k, 0.0) <= 0.0 or i in self.T and np.allclose(self.sc.gmat.get(k, np.eye(4)), self.T[i]):
                continue                     # hidden, or still in its slot on the long table (the table's box covers it)
            V = o.get("V")
            if V is None or not len(V):
                continue
            lo, hi = np.asarray(V, float).min(0), np.asarray(V, float).max(0)
            C = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
            M = self.sc.gmat.get(k, np.eye(4))
            w = C @ M[:3, :3].T + M[:3, 3]
            if w[:, 2].min() > 1900.0:
                continue
            out.append((w[:, 0].min(), w[:, 1].min(), w[:, 0].max(), w[:, 1].max()))
        return out

    @staticmethod
    def _clear_pts(P, boxes, r):
        """Round 10 (vectorised): is every point of P (m x 2) at least r from every box (x0, y0, x1, y1)?"""
        if not len(boxes):
            return True
        B = np.asarray(boxes, float)
        P = np.atleast_2d(np.asarray(P, float))
        dx = np.maximum(np.maximum(B[None, :, 0] - P[:, None, 0], 0.0), P[:, None, 0] - B[None, :, 2])
        dy = np.maximum(np.maximum(B[None, :, 1] - P[:, None, 1], 0.0), P[:, None, 1] - B[None, :, 3])
        return bool(np.all(dx * dx + dy * dy >= r * r))

    @classmethod
    def _clear(cls, p, boxes, r):
        return cls._clear_pts([p], boxes, r)

    def _clear_path(self, pts, boxes, r, step=60.0):
        P = []
        for a, b in zip(pts[:-1], pts[1:]):
            a, b = np.asarray(a, float), np.asarray(b, float)
            n = max(1, int(np.linalg.norm(b - a) / step))
            P += [a + (b - a) * k / n for k in range(n + 1)]
        return self._clear_pts(P, boxes, r) if P else True

    def mir_room_moves(self, work, reach=1500.0):
        """Round 10: [(arm, x along its lane)] a MiR could back off to, to make room for a person working at `work`: MiRs within
        `reach` of the work along x whose arm is parked (park pose, nothing held), moved 900-1300 mm away along their own lane
        (x in -1400..2150), the lane between clear of the cell's static bodies on the floor plan."""
        out = []
        wx = float(work[0])
        static = self._static_boxes()
        for n in ("A", "B"):
            s = self.st[n]
            if s.get("pose") is not None or s["held"] is not None or abs(float(s["x"]) - wx) > reach:
                continue
            if float(np.max(np.abs(np.asarray(s["q"], float) - np.asarray(self.arm[n].park_q(), float)))) > 0.05:
                continue
            x0 = float(s["x"])
            for dx in (-900.0, 900.0, -1300.0, 1300.0):
                x1 = x0 + dx
                if not -1400.0 <= x1 <= 2150.0:
                    continue
                ok = True
                for u in np.linspace(0.0, 1.0, 7):
                    for _, (v, f), _ in self.K.mir_bodies(n, x0 + (x1 - x0) * u, "front" if n == "A" else "back"):
                        v = np.asarray(v, float)
                        b = (v[:, 0].min(), v[:, 1].min(), v[:, 0].max(), v[:, 1].max())
                        if any(not (b[2] < x0_ or x1_ < b[0] or b[3] < y0_ or y1_ < b[1]) for x0_, y0_, x1_, y1_ in static):
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    out.append((n, x1))
        return out

    @staticmethod
    def _seg_d(p, a, b):
        """Distance from p to segment ab (2-D) and where along it (0 at a, 1 at b)."""
        p, a, b = np.asarray(p, float), np.asarray(a, float), np.asarray(b, float)
        d = b - a
        t = float(np.clip(np.dot(p - a, d) / max(float(np.dot(d, d)), 1e-9), 0.0, 1.0))
        return float(np.linalg.norm(p - (a + t * d))), t

    def _blocks_view(self, pts, work, cams, r=520.0):
        """Would a person at any of pts stand in a tripod's line of sight to the work (within r of it, between the two)?"""
        for c in cams:
            for q in pts:
                d, t = self._seg_d(q, c, work)
                if d < r and 0.05 < t < 0.97:
                    return True
        return False

    def person_spot(self, work, side, cams=(), relaxed=False):
        """(spot (x, y), aisle point (x, +-AISLE)) for a person working at `work` (x, y) from side A (y < 0) or B: the nearest
        spot whose floor is clear by PERSON_R and whose straight walk in from the aisle is clear too, out of the lines of sight
        from the place's tripods `cams` (x, y) to the work (round 9: a person in front of the bench's tripod hid the work). None
        if there is none."""
        c = self.person_spots(work, side, cams, relaxed)
        return None if not c else (c[0]["spot"], c[0]["aisle"])

    def person_spots(self, work, side, cams=(), relaxed=False, blocked_ok=False, n=40, rmax=None):
        """Round 10: the candidate spots, best first: dicts with spot, aisle (the aisle point the walk starts from), cost and
        `blocked` (the place's tripods whose line of sight to the work the person stands in). blocked_ok: a spot may block some
        of the place's tripods (not all); the person's frames are then shot from one it does not block (round 9 had no spot
        at all for F18's screw at Fixture B, where both MiRs dock: every clear spot stood in some tripod's view)."""
        boxes = self.floor_boxes()
        wx, wy = float(work[0]), float(work[1])
        names = list(cams)
        cxy = [tuple(map(float, cam_def(c)[0][:2])) for c in names]
        out = []
        why = {}
        for s in ((-1.0, 1.0) if side == "A" else (1.0, -1.0)):
            for r in (450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 825.0, 900.0, 1000.0, 1100.0, 1350.0, 1650.0, 2000.0):
                if rmax is not None and r > rmax:
                    continue
                for ang in range(-85, 86, 5):
                    a = math.radians(ang)
                    x, y = wx + r * math.sin(a), wy + s * r * math.cos(a)
                    # round 10: a spot may be up to 150 mm across the bench's centre line (round 9: at least 250 mm on the
                    # person's side), so past a station's end, between Fixture B and the table, counts (the floor check keeps
                    # them out of the bench and fixtures)
                    if s * y < -150.0 or s * y > self.AISLE - 300.0:
                        why["y"] = why.get("y", 0) + 1
                        continue
                    # round 10: the spot itself needs less floor clearance (PERSON_R_SPOT): person_job checks the standing
                    # body against everything drawn (person_hits) before it is used
                    if not self._clear((x, y), boxes, self.PERSON_R_SPOT - (40.0 if relaxed else 0.0)):
                        why["floor"] = why.get("floor", 0) + 1
                        continue
                    if not relaxed and not self._clear_path([(x, s * self.AISLE), (x, y + s * min(250.0, s * (s * self.AISLE - y)))],
                                                            boxes, self.PERSON_R - 60.0):
                        why["walk"] = why.get("walk", 0) + 1
                        continue
                    walk = [(x, y + (s * self.AISLE - y) * u) for u in (0.0, 0.25, 0.5, 0.75)]
                    blocked = [nm for nm, c in zip(names, cxy) if self._blocks_view(walk, (wx, wy), [c])]
                    if blocked and (not blocked_ok or len(blocked) == len(names)):
                        why["view"] = why.get("view", 0) + 1
                        continue
                    if CAM_MIN and any(math.hypot(x - c[0], y - c[1]) < CAM_MIN for c in cxy):
                        why["cam_min"] = why.get("cam_min", 0) + 1
                        continue                 # ASM_PERSON_CAM_MIN: not right under a tripod (filling the picture)
                    cost = r + 3.0 * abs(ang) + (0.0 if s == (-1.0 if side == "A" else 1.0) else 1500.0) + 700.0 * len(blocked)
                    free = [c for c in names if c not in blocked]
                    if free and not any(in_view(c, (x, y, 1000.0), margin=0.8) for c in free):
                        cost += 900.0            # seen from none of the place's tripods: only if nothing else is clear
                    out.append(dict(cost=cost, spot=(x, y), aisle=(x, s * self.AISLE), blocked=blocked, r=r, ang=ang))
        out.sort(key=lambda d: d["cost"])
        self.last_spot_why = why
        return out[:n]

    @staticmethod
    def walk_seq(pts, hd0, hd_end, v=450.0, turn=10.0):
        """Per frame (x, y, heading): turn on the spot (at most `turn` deg a frame) to each leg's heading, walk the leg eased in
        and out (mean v mm/s, so at most 1.5 v), and at the end turn to hd_end. Round 9: v = 450 mm/s (at most 675): on this
        eased profile people.py's Gait keeps every planted foot still (0.0 mm stance slip, 0 overreach frames; at 850 mm/s,
        peak 1.3 m/s, the steps could not keep up and the planted foot slid up to 0.5 m a stance, measured with walk.py)."""
        out = []
        hd = float(hd0)

        def turn_to(h1):
            nonlocal hd
            d = ((h1 - hd + 180.0) % 360.0) - 180.0
            n = int(math.ceil(abs(d) / turn))
            for k in range(1, n + 1):
                out.append((x, y, hd + d * k / n))
            hd = hd + d
        x, y = pts[0]
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 1.0:
                continue
            turn_to(face_hd(x1 - x0, y1 - y0))
            n = max(2, int(math.ceil(L / v * FPS)))
            for k in range(1, n + 1):
                u = smooth(k / n)
                x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                out.append((x, y, hd))
        turn_to(hd_end)
        return out

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
PICK_SHOW = int(os.environ.get("ASM_PICK_SHOW", "2"))     # round 9: 2, the visits whose drives are drawn (round 8: 8, so
                                                           # visits 3-8 cut to the table and back: two forced cuts each)
DRIVE_LAPSE = 6.0
TABLE_X = 2200.0
JUMP_DEG = float(os.environ.get("ASM_JUMP_DEG", "5.0"))
# ASM_DRIVE_HOLD=1 (chapter 41, round 9): a short MiR hop between the cell's docks (drawn, continuous) joins the shot before or
# after it instead of a 1-2 s wide shot between two cuts; the caption says where the MiR drives
DRIVE_HOLD = os.environ.get("ASM_DRIVE_HOLD", "0") == "1"
# ASM_PERSON_CAM_MIN=<mm> (chapter 40's re-render, round 9): the person's spot at least this far (on the floor) from each of the
# place's tripods, so they don't fill the picture (chapter 41 was drawn without it: 0)
CAM_MIN = float(os.environ.get("ASM_PERSON_CAM_MIN", "0") or 0.0)
# round 10: how many of the best spots person_job tries (each: the standing body and the job's poses checked)
NSPOT = int(os.environ.get("ASM_PERSON_SPOTS", "24"))
# round 10: the person's spots and poses, once searched, are kept: pass 2 reuses pass 1's, and with ASM_PERSON_CACHE=<file.json>
# every slice of a chapter shares them (keyed by step, the job's number in the chapter, side and work point; delete the file
# when the recording changes)
_PCACHE = None


def person_cache():
    global _PCACHE
    if _PCACHE is None:
        _PCACHE = {}
        f = os.environ.get("ASM_PERSON_CACHE")
        if f and os.path.exists(f):
            try:
                _PCACHE.update(json.loads(pathlib.Path(f).read_text()))
            except Exception as e:      # noqa: BLE001
                print("person cache unreadable:", e, flush=True)
    return _PCACHE


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


def person_cache_put(key, val):
    val = _jsonable(val)
    person_cache()[key] = val
    f = os.environ.get("ASM_PERSON_CACHE")
    if not f:
        return
    try:
        cur_ = json.loads(pathlib.Path(f).read_text()) if os.path.exists(f) else {}
        cur_[key] = val
        tmp = f"{f}.{os.getpid()}.tmp"
        pathlib.Path(tmp).write_text(json.dumps(cur_))
        os.replace(tmp, f)
    except Exception as e:              # noqa: BLE001
        print("person cache not written:", e, flush=True)


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
            if e["kind"] in ("move", "grip", "tool") and xs.get(e.get("arm"), 0.0) > TABLE_X:   # round 9: a tool change at
                # the table belongs to the visit (round 8 drew it alone: a 0.5 s shot at the table between two cuts)
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
    if k == "cell" and len(loc) > 1:      # a MiR driving between the cell's docks: the wide view, or down its lane
        return ["cell", f"lane_{loc[1]}"]
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
    """plan: per frame dict(loc, key, work, force, bound); scores: {key: {cam: [blocked fractions]}} -> per frame camera name.

    Round 9: the plan is cut into segments at the slice boundaries (ASM_CUTS, `bound`) and each segment's shots are chosen
    from what lies in it and the camera before it only, so a slice drawn before the planner has finished gets the frames the
    whole chapter would; unlike round 8's forced cut there, the camera may stay the same across a boundary."""
    n = len(plan)
    cams = [None] * n
    starts = [0] + [i for i in range(1, n) if plan[i].get("bound")] + [n]
    prev = None
    for a, b in zip(starts[:-1], starts[1:]):
        if b > a:
            seg = _choose_segment(plan, scores, a, b, prev)
            cams[a:b] = seg
            prev = seg[-1]
    return cams


def _choose_segment(plan, scores, i0, i1, prev):
    groups = []                                  # [start, end, key, loc, cam]
    for i in range(i0, i1):
        p = plan[i]
        if groups and groups[-1][2] == p["key"] and not p.get("force"):
            groups[-1][1] = i + 1
        else:
            groups.append([i, i + 1, p["key"], p["loc"], None])
    prev0 = prev
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
            alt = [c for c in ("cell", f"lane_{g[3][1]}" if g[3][0] in ("cell", "lane") and len(g[3]) > 1 else "PT", "B", "bench")
                   if c != prev]
            best = (0.0, alt[0])
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
    if shots and prev0 is not None and shots[0][2] != prev0 and shots[0][1] - shots[0][0] < MIN_SHOT and \
            not plan[shots[0][0]].get("force") and ok_from(prev0, shots[0]):
        shots[0][2] = prev0                      # round 9: a short shot after a slice boundary carries on the camera before it
        if len(shots) > 1 and shots[1][2] == prev0 and not plan[shots[1][0]].get("force"):
            shots[0] = [shots[0][0], shots[1][1], prev0, shots[0][3] + shots[1][3]]
            del shots[1]
    changed = True
    while changed:
        changed = False
        for k, sh in enumerate(shots):
            if sh[1] - sh[0] >= MIN_SHOT or len(shots) == 1:
                continue
            if k == 0 and prev0 is not None and sh[2] == prev0 and not plan[sh[0]].get("force"):
                continue                         # it continues the shot before the boundary: not short on screen
            forced = bool(plan[sh[0]].get("force"))
            before = shots[k - 1][2] if k > 0 else prev0
            for j in (k - 1, k + 1):
                if not (0 <= j < len(shots)) or (j == k + 1 and plan[shots[j][0]].get("force")):
                    continue
                if forced and (j == k - 1 or shots[j][2] == before):
                    continue                     # round 9: a forced cut may join the next shot if that still changes the camera
                if ok_from(shots[j][2], sh):
                    o = shots[j]
                    lo, hi = min(o[0], sh[0]), max(o[1], sh[1])
                    shots[j] = [lo, hi, o[2], (o[3] + sh[3]) if j < k else (sh[3] + o[3])]
                    del shots[k]
                    changed = True
                    break
            if changed:
                break
            # round 9: a short shot opened by a forced cut and followed by the camera before it (the cut can't join it): the
            # next shot may take this one's camera instead, if that camera is one of its place's tripods and sees its work
            j = k + 1
            if forced and j < len(shots) and shots[j][2] == before and not plan[shots[j][0]].get("force") and \
                    sh[2] in place_cands(shots[j][3][0][3]) and ok_from(sh[2], shots[j]):
                o = shots[j]
                shots[k] = [sh[0], o[1], sh[2], sh[3] + o[3]]
                del shots[j]
                changed = True
                break
    # neighbours with the same camera after the merges
    out = []
    for sh in shots:
        if out and out[-1][2] == sh[2] and not plan[sh[0]].get("force"):
            out[-1][1] = sh[1]
        else:
            out.append(list(sh[:3]))
    cams = [None] * (i1 - i0)
    for a, b, c in out:
        for i in range(a, b):
            cams[i - i0] = c
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
            last_move[e["arm"]]["unplanned_note"] = e.get("note") or ""
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
                      f"{(' forced: ' + str(plan[i0]['force'])) if plan[i0].get('force') else ''}", flush=True)
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
    if os.environ.get("ASM_PICK_PERSON") == "1":
        # round 10 (a test of the person's frames): draw only the frames the person is in, and the frame before each run of
        # them (so walk.py starts a new track there)
        global PICK
        PICK = set()
        for i, p in enumerate(plan):
            if p.get("person"):
                PICK.update((max(0, i - 1), i))
        print(f"{name}: drawing the {len(PICK)} frames with the person (ASM_PICK_PERSON)", flush=True)
    if PICK is not None:
        part, k_ = "pick", "pick"
    if os.environ.get("ASM_PLAN_ONLY") == "1":
        import json as _j
        pf = [i for i, p in enumerate(plan) if p.get("person")]
        runs_ = []
        for i in pf:
            if runs_ and i == runs_[-1][1] + 1:
                runs_[-1][1] = i
            else:
                runs_.append([i, i])
        out = dict(chapter=name, frames=tot_frames, shots=st,
                   steps={p["step"]: i for i, p in reversed(list(enumerate(plan)))},
                   person=runs_)                  # round 10: the frames the person is drawn in (first, last)
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
    away = {}                            # arm -> where its MiR and arm were when a fetch not shown began (round 9)
    pend = dict(screws=[], parts=[], failed=set())   # round 9: what the person does at the end of a failed step
    pstate = dict(on=False, n=-1, out_n=None, out_at=None, fit=None, blocked=None)   # the person: shown, the last frame their
    # feet were brought to; round 10: the frame after they last walked out and where (out_n, out_at: a job right after starts
    # from there), the job's checked poses (fit) and the tripods their spot blocks (blocked)

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
        if any(not a_["drawn"] for a_ in away.values()):
            force = "away"                 # the first frame drawn while a MiR is away on a drive not shown: it is gone from its
            for a_ in away.values():       # dock (or now at the table), so this frame is a cut (round 9: only then)
                a_["drawn"] = True
        force = force or last["force"]
        bound = cur["id"] in CUTS and not cur.get("emitted")
        # round 9: a slice boundary (ASM_CUTS) is a soft boundary: no shot-plan decision reaches across it (so every slice's
        # frames are the chapter's own), but the camera may stay as it is across it (round 8 forced a cut at each)
        cur["emitted"] = True
        last["loc"], last["force"] = loc, False
        if rp.person is not None and pstate["on"] and pstate["n"] != tot["n"]:
            rp.person.set(frame=tot["n"])  # the feet settle while the person stands (explicit clock: no render hook)
            pstate["n"] = tot["n"]
        key = (cur["id"], loc)
        if pstate["on"] and pstate.get("blocked"):
            # round 10: the person stands in some of the place's tripods' lines of sight (no spot clear of all): their frames
            # are a group of their own, shot from a tripod they don't block
            key = (cur["id"], loc, "person")
            if scores is not None and key not in scores:
                scores[key] = {c: [1.0 if c in pstate["blocked"] else 0.0] for c in place_cands(loc)}
        if plan is not None:
            plan.append(dict(loc=loc, key=key, work=None if work is None else np.asarray(work, float).copy(),
                             force=force, bound=bound, step=cur["id"], person=bool(pstate["on"])))
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

    def person_job(work, side, job_frames, loc, fit=None):
        """Round 9: the person walks in from the aisle to a clear spot by `work`, job_frames() draws the job (the person standing
        there), and they walk back out. True if the slice ended.

        Round 10: the spot is the best candidate (Replay.person_spots) where the person, standing and in the job's poses (`fit`:
        the hands on the part they set, the driver on the screw), is clear of everything drawn by the frame audit's own measure
        (Replay.person_hits); if no spot is clear of every tripod's line of sight, one that blocks some of them (not all) is
        used and the person's frames are shot from a tripod it doesn't block. Back to back with the last person job (no frame
        between them), the person turns round where they stand and walks to the new spot: round 9 put them back at the aisle,
        turned 180 deg in one frame (walk.py read it as 205-383 mm of stance-foot slip, chapter 41 frames 3204, 13283, 13457)."""
        P = rp.person
        if P is None:
            return job_frames()
        look = (float(work[0]), float(work[1]), float(work[2]) if len(work) > 2 else 950.0)
        cams_ = place_cands(loc)
        back = pstate.get("out_n") == tot["n"] and pstate.get("out_at") is not None
        # the spots, in tiers: walked to from the aisle, within reach of the work (a job with the hands: 780 mm), out of the
        # place's tripods' sight lines or blocking some of them (costlier); put in place across a cut, within reach; then,
        # if nothing within reach is clear, anywhere clear (the job drawn from there)
        rmax = 780.0 if fit is not None else None     # people.py's right hand reaches 525-575 mm forward at 1.1-1.25 m
        # upright, 750-800 mm leaning 28 deg (/tmp/r10/w3/reach_test.py)
        tiers = [dict(cams=cams_, blocked_ok=True, rmax=rmax)]
        if rmax is not None:
            tiers.append(dict(cams=cams_, blocked_ok=True, rmax=rmax, relaxed=True))
            tiers.append(dict(cams=cams_, blocked_ok=True))
        tiers.append(dict(cams=cams_, blocked_ok=True, relaxed=True))
        choice, worst, tried, why_all = None, None, 0, {}
        # the search is deterministic: pass 2, and every other slice of the chapter, reuse pass 1's choice (person_cache)
        pstate["jobs"] = pstate.get("jobs", 0) + 1
        ckey = (f"{cur['id']}|{pstate['jobs']}|{side}|{int(fit is not None)}|" +
                ",".join(f"{v:.0f}" for v in look))
        hit = person_cache().get(ckey)
        if hit is not None:
            choice = (dict(hit["c"]), hit["data"])
            tiers = []
        def search(tiers_, mir=None):
            nonlocal tried, worst
            for tier in tiers_:
                cands = rp.person_spots(work[:2], side, **tier)
                for k_, v_ in getattr(rp, "last_spot_why", {}).items():
                    why_all[k_] = why_all.get(k_, 0) + v_
                for c in cands[:NSPOT]:
                    tried += 1
                    c["relaxed"] = bool(tier.get("relaxed"))
                    c["mir"] = mir
                    xs, ys = c["spot"]
                    P.place(x=xs, y=ys, hd=face_hd(look[0] - xs, look[1] - ys), look=look, frame=tot["n"])
                    data = None
                    if fit is not None:
                        hits, data = fit(P)               # the whole body in the job's poses (reach first: cheap)
                    else:
                        hits = rp.person_hits(P, limit=2)  # standing there
                    if not hits:
                        return (c, data)
                    if mir is None and (worst is None or len(hits) < len(worst[1]) or
                                        (len(hits) == len(worst[1]) and max(h[2] for h in hits) < max(h[2] for h in worst[1]))):
                        worst = ((c, data), hits)
            return None
        if tiers:
            choice = search(tiers[:2] if rmax is not None else tiers)
            if choice is None and rmax is not None:
                # round 10: nothing within reach with the MiRs where they are (both docked round Fixture B: the F18 screw
                # round 9 could not draw anyone at): a MiR whose arm is parked backs off along its lane to make room, then
                # comes back after the person has gone (drawn, labelled; its lane checked clear on the floor plan)
                for n_, x1_ in rp.mir_room_moves(work):
                    x0_ = rp.st[n_]["x"]
                    rp.set_arm(n_, x=x1_)
                    choice = search(tiers[:2], mir=(n_, float(x0_), float(x1_)))
                    rp.set_arm(n_, x=x0_)
                    if choice is not None:
                        break
            if choice is None and rmax is not None:
                choice = search(tiers[2:])
        if choice is None and worst is None:
            print(f"   {cur['id']}: no spot for the person by {np.round(np.asarray(work, float), 0).tolist()} "
                  f"({why_all}): the job is drawn without them", flush=True)
            return job_frames()
        if choice is None:
            choice = worst[0]
            if fit is not None and choice[1] is None:
                xs, ys = choice[0]["spot"]
                P.place(x=xs, y=ys, hd=face_hd(look[0] - xs, look[1] - ys), look=look, frame=tot["n"])
                choice = (choice[0], fit(P)[1])
            print(f"   {cur['id']}: no spot of {tried} keeps the person clear and in reach; the least bad: {worst[1][:3]} "
                  f"(spots ruled out: {why_all})", flush=True)
            if os.environ.get("ASM_PERSON_DEBUG") == "1":
                wx_, wy_ = float(work[0]), float(work[1])
                near_ = [tuple(round(v) for v in b) for b in rp.floor_boxes()
                         if b[0] - 1300 < wx_ < b[2] + 1300 and b[1] - 1300 < wy_ < b[3] + 1300]
                print(f"   floor boxes within 1.3 m of the work: {near_}", flush=True)
        c, data = choice
        if hit is None:
            person_cache_put(ckey, dict(c=c, data=data))
        relaxed = c["relaxed"]
        pstate["fit"] = data
        pstate["blocked"] = list(c["blocked"]) or None
        if plan is not None and hit is None:    # where the person was put, and how (the log)
            print(f"   {cur['id']}: person at ({c['spot'][0]:.0f}, {c['spot'][1]:.0f}) for the work at "
                  f"({look[0]:.0f}, {look[1]:.0f}, {look[2]:.0f}), r {c['r']:.0f} mm, {'relaxed, ' if relaxed else ''}"
                  f"blocks {c['blocked'] or 'no tripod'}; back to back: {back}; poses: "
                  f"{[(d_['name'], round(d_['reach'])) for d_ in (data or [])]}"
                  f"{'; MiR %s makes room: x %.0f -> %.0f' % tuple(c['mir']) if c.get('mir') else ''}", flush=True)
        (xs, ys), (xa, ya) = c["spot"], c["aisle"]
        hd_job = face_hd(look[0] - xs, look[1] - ys)
        mir = c.get("mir")

        def mir_drive(n_, x0_, x1_, out_):
            """A MiR makes room for the person along its lane (or comes back to its dock): drawn at about 0.35 m/s, eased."""
            d_ = abs(x1_ - x0_)
            nf_ = max(24, int(round(d_ / 350.0 * FPS)))
            txt_ = (f"MiR {n_} backs off {d_ / 1000:.1f} m along its lane to make room for the person (its arm parked; not in "
                    "the planner's recording, the lane clear on the floor plan)" if out_ else
                    f"MiR {n_} drives back {d_ / 1000:.1f} m to its dock")
            for f_ in range(nf_):
                rp.set_arm(n_, x=x0_ + (x1_ - x0_) * smooth((f_ + 1) / nf_))
                if emit(cur["label"], txt_ + " (real time)", [f"robot {n_}"], add={"robot_h": 1.0 / FPS / 3600.0}, loc=loc):
                    return True
            rp.set_arm(n_, x=x1_)
            return False

        def the_job():
            if relaxed:
                # no clear walk in from the aisle (both MiRs docked round the station): the person is put on the spot,
                # across a cut each way (round 9: F18's screw had no person at all)
                P.show(1.0)
                P.place(x=xs, y=ys, hd=hd_job, look=look, frame=tot["n"])
                pstate.update(on=True, n=tot["n"])
                last["force"] = "person put in place"
                r_ = job_frames()
                P.show(0.0)
                pstate.update(on=False, out_n=None, out_at=None, fit=None, blocked=None)
                last["force"] = "person gone"
                return r_
            hd_in = face_hd(xs - xa, ys - ya)
            legs_in = [(xa, ya), (xs, ys)]
            h0 = hd_in
            P.show(1.0)
            if back and pstate["out_at"][1] * ya > 0.0 and abs(pstate["out_at"][0] - xa) < 4000.0:
                # still standing at the aisle where the last job left them: turn round and walk along the aisle and in
                x0, y0, h0 = pstate["out_at"]
                P.place(x=x0, y=y0, hd=h0, look=look, frame=tot["n"])        # where they stand (no move: the feet stay)
                legs_in = [(x0, y0), (xa, ya), (xs, ys)]
            else:
                if back:
                    # back to back but on the other side of the cell: out of the picture for a frame, then from that aisle
                    P.show(0.0)
                    pstate["on"] = False
                    if emit(cur["label"], "a person walks over from the aisle (real time)", ["person"], status="person",
                            loc=loc):
                        return True
                    P.show(1.0)
                P.place(x=xa, y=ya, hd=hd_in, look=look, frame=tot["n"])
            pstate.update(on=True, n=tot["n"])
            for legs, hs, h1, txt in ((legs_in, h0, hd_job, "a person walks over from the aisle"),
                                      (None, 0.0, 0.0, ""),
                                      ([(xs, ys), (xa, ya)], hd_job, hd_in + 180.0, "the person walks back to the aisle")):
                if legs is None:
                    if job_frames():
                        return True
                    continue
                for x, y, h in rp.walk_seq(legs, hs, h1):
                    P.set(x=x, y=y, hd=h, look=look, frame=tot["n"])
                    pstate["n"] = tot["n"]
                    if emit(cur["label"], txt + " (real time)", ["person"], add={"person_h": 1.0 / FPS / 3600.0},
                            status="person", loc=loc):
                        return True
            P.show(0.0)
            pstate.update(on=False, out_n=tot["n"], out_at=(float(P.st["x"]), float(P.st["y"]), float(P.st["hd"])), fit=None,
                          blocked=None)
            return False
        if mir is not None and mir_drive(mir[0], float(mir[1]), float(mir[2]), True):
            return True
        if the_job():
            return True
        if mir is not None:
            if mir_drive(mir[0], float(mir[2]), float(mir[1]), False):
                return True
            pstate["out_n"] = None                 # frames since the walk-out: the next job is not back to back
        return False

    def obj_world(i, M=None):
        o = rp.objs.get(i) or {}
        V = np.asarray(o.get("V"), float) if o.get("V") is not None else np.zeros((1, 3))
        M = np.asarray(rp.sc.gmat.get(f"o{i}", np.eye(4)) if M is None else M, float)
        return V @ M[:3, :3].T + M[:3, 3]

    def seat_off(i, M0, T1):
        """How far (mm) object i drawn at M0 is from its seat T1: the largest move of its bounding box's corners."""
        if M0 is None:
            return 1e9
        V = np.asarray((rp.objs.get(i) or {}).get("V"), float) if (rp.objs.get(i) or {}).get("V") is not None else None
        if V is None or not len(V):
            return float(np.linalg.norm(np.asarray(M0, float)[:3, 3] - np.asarray(T1, float)[:3, 3]))
        lo_, hi_ = V.min(0), V.max(0)
        C = np.array([[x, y, z] for x in (lo_[0], hi_[0]) for y in (lo_[1], hi_[1]) for z in (lo_[2], hi_[2])])
        M0, T1 = np.asarray(M0, float), np.asarray(T1, float)
        return float(np.max(np.linalg.norm((C @ M0[:3, :3].T + M0[:3, 3]) - (C @ T1[:3, :3].T + T1[:3, 3]), axis=1)))

    def screw_axis(i):
        """(head point, unit axis out of the hole) of a screw as it sits: its long axis by PCA, the head the fatter end."""
        W = obj_world(i)
        c = W.mean(0)
        if len(W) < 3:
            return c, np.array([0.0, 0.0, 1.0])
        u = np.linalg.svd(W - c, full_matrices=False)[2][0]
        t = (W - c) @ u
        r = np.linalg.norm((W - c) - np.outer(t, u), axis=1)
        hi, lo = t > 0.6 * t.max(), t < 0.6 * t.min()
        if lo.any() and hi.any() and r[lo].mean() > r[hi].mean():
            u = -u
        return c + u * float(np.abs(t).max()), u

    def place_driver(P, h, u):
        """The hand driver in the person's right hand, pointing at the screw: its bit on the head when the hand is close
        enough, else the handle in the hand and the bit towards the screw (never left floating)."""
        hp = np.asarray(P.hand_point("r"), float)
        dv = hp - h
        L_ = float(np.linalg.norm(dv))
        zz = dv / L_ if L_ > 1e-6 else u
        tip = h if L_ <= 260.0 else hp - 160.0 * zz
        xx = np.cross(zz, [0.0, 0.0, 1.0]) if abs(zz[2]) < 0.9 else np.cross(zz, [1.0, 0.0, 0.0])
        xx /= np.linalg.norm(xx)
        Rt = np.eye(4)
        Rt[:3, 0], Rt[:3, 1], Rt[:3, 2], Rt[:3, 3] = xx, np.cross(zz, xx), zz, tip
        rp.sc.gmat["op/tool"] = Rt

    def part_hand_cands(P, W):
        """Round 10: hand targets for setting a part whose points (world, at its seat) are W, from where the person stands:
        on its outside, 25 mm or more off its surface (people.py's fingers curl past the palm's target), best first: both
        palms down over its top, nearer its front edge, higher; both on its front face; on its two sides; one hand over its
        top or front. Round 9 aimed both palms at the part's centre (a hand 28 mm in the chamber body round it)."""
        p = np.array([P.st["x"], P.st["y"], 0.0])
        c = 0.5 * (W.min(0) + W.max(0))
        f = np.array([c[0] - p[0], c[1] - p[1], 0.0])
        f /= max(float(np.linalg.norm(f)), 1e-6)
        r = np.array([f[1], -f[0], 0.0])                       # the person's right
        u, v, z = (W - p) @ f, (W - p) @ r, W[:, 2]
        near, far, vmin, vmax, zlo, ztop = float(u.min()), float(u.max()), float(v.min()), float(v.max()), float(z.min()), \
            float(z.max())
        cu, cv = 0.5 * (near + far), 0.5 * (vmin + vmax)
        hw = min(90.0, 0.35 * (vmax - vmin) + 20.0)
        zm = max(zlo + 0.5 * (ztop - zlo), ztop - 60.0)

        def at(a, b, zz):
            q = p + f * a + r * b
            return (float(q[0]), float(q[1]), float(zz))
        out = []
        for a, dz in ((cu, 25.0), (near + min(45.0, 0.3 * (far - near)), 25.0), (cu, 60.0), (near + 20.0, 110.0)):
            out.append(("top", {"l": at(a, cv - hw, ztop + dz), "r": at(a, cv + hw, ztop + dz)}, {"l": "down", "r": "down"}))
        fwd = tuple(map(float, f))
        out.append(("front", {"l": at(near - 30.0, cv - hw, zm), "r": at(near - 30.0, cv + hw, zm)}, {"l": fwd, "r": fwd}))
        if vmax - vmin < 420.0:
            out.append(("sides", {"l": at(cu, vmin - 30.0, zm), "r": at(cu, vmax + 30.0, zm)},
                        {"l": tuple(map(float, r)), "r": tuple(map(float, -r))}))
        out.append(("one hand, top", {"l": None, "r": at(near + min(45.0, 0.3 * (far - near)), cv, ztop + 30.0)},
                    {"l": None, "r": "down"}))
        out.append(("one hand, front", {"l": None, "r": at(near - 30.0, cv, zm)}, {"l": None, "r": fwd}))
        out.append(("one hand, high", {"l": None, "r": at(near, cv, ztop + 120.0)}, {"l": None, "r": "down"}))
        return out

    def fit_jobs(jobs):
        """Round 10: fit(P) for person_job: for each of the person's jobs, the first hand pose (part_hand_cands; for a screw the
        driver held 150, 200 or 120 mm up its axis) whose posed body, hands and driver are clear of everything drawn (the part
        set, at its seat, and the screw driven may be touched by the hands up to Replay.OWN_MM). Returns (hits of the worst job,
        [pose per job])."""
        def fit(P):
            poses, worst = [], []
            for kind, objs, T in jobs:
                keep = {i: (rp.sc.gmat.get(f"o{i}"), rp.sc.alpha.get(f"o{i}", 0.0)) for i in objs}
                for i in objs:                     # checked where it will be: in its seat
                    if kind == "part":
                        rp.sc.gmat[f"o{i}"] = np.asarray(T, float)
                    rp.sc.alpha[f"o{i}"] = 1.0
                own = {f"o{i}" for i in objs}
                best = None
                if kind == "part":
                    W = np.vstack([obj_world(i, T) for i in objs])
                    cands = [(nm, hands, palm, None) for nm, hands, palm in part_hand_cands(P, W)]
                else:
                    h, u = screw_axis(objs[0])
                    cands = [(f"driver {d:.0f} mm", {"r": tuple(map(float, h + d * u)), "l": None}, {"l": None, "r": None},
                              (h, u)) for d in (150.0, 200.0, 120.0)]
                done_ = False
                for nm, hands, palm, hu in cands:
                    for lean in (0.0, 15.0, 28.0):      # round 10: leaning in from the hips to reach further (people.py)
                        P.set(hands=hands, palm=palm, lean=lean, frame=tot["n"])
                        extra = ()
                        if hu is not None:
                            rp.sc.alpha["op/tool/screwdriver"] = 1.0
                            place_driver(P, *hu)
                            extra = ("op/tool/screwdriver",)
                        tgt = [np.asarray(v, float) for v in hands.values() if v is not None]
                        if hu is not None:
                            # a screw: the right hand on the driver's handle (110-210 mm up from its bit), the bit on the
                            # head (place_driver: the hand within 260 mm of it)
                            L_ = float(np.linalg.norm(np.asarray(P.hand_point("r"), float) - hu[0]))
                            reach = max(0.0, 110.0 - L_, L_ - 230.0)
                        else:
                            reach = max(float(np.linalg.norm(np.asarray(P.hand_point(s), float) - np.asarray(hands[s], float)))
                                        for s in ("l", "r") if hands.get(s) is not None)
                        if reach > 80.0:
                            rp.sc.alpha["op/tool/screwdriver"] = 0.0
                            if best is None or (1, True, 0.0, reach, lean) < best[0]:
                                best = ((1, True, 0.0, reach, lean),
                                        dict(name=nm + (f", leaning {lean:.0f} deg" if lean else ""), hands=hands, palm=palm,
                                             look=tuple(np.mean(tgt, axis=0)), reach=reach, lean=lean), [])
                            continue                    # out of reach: lean further, or the next pose (no check needed)
                        hits = rp.person_hits(P, own=own, extra=extra, limit=3)
                        rp.sc.alpha["op/tool/screwdriver"] = 0.0
                        score = (len(hits), reach > 80.0, max([h_[2] for h_ in hits], default=0.0), reach, lean)
                        if best is None or score < best[0]:
                            best = (score, dict(name=nm + (f", leaning {lean:.0f} deg" if lean else ""), hands=hands, palm=palm,
                                                look=tuple(np.mean(tgt, axis=0)), reach=reach, lean=lean), hits)
                        if not hits and reach <= 80.0:
                            done_ = True
                            break
                    if done_:
                        break
                for i, (M0, a0) in keep.items():
                    if M0 is not None:
                        rp.sc.gmat[f"o{i}"] = M0
                    rp.sc.alpha[f"o{i}"] = a0
                poses.append(best[1])
                bad = list(best[2]) + ([("hand", "out of reach", round(best[1]["reach"], 1))] if best[1]["reach"] > 80.0 else [])
                if len(bad) > len(worst):
                    worst = bad
            P.set(hands={"l": None, "r": None}, palm={"l": None, "r": None}, lean=0.0, frame=tot["n"])
            return worst, poses
        return fit

    def person_fix():
        """Round 9 (the coordinator: "showing where a human is absolutely necessary"): after a failed step, the person walks
        in, sets each part the arms could not (it appears in its seat as their hands reach it) and drives each screw they
        could not (a screwdriver in the right hand; the screw appears as the bit reaches its hole), time-lapsed to the
        estimates the clocks count (5 min a step, 1 min a screw), and walks out. Round 10: the hands on the part's outside,
        the spot and the poses checked against everything drawn (fit_jobs, person_job)."""
        jobs = [("part", objs, T) for objs, T in pend["parts"]] + [("screw", [i], None) for i in pend["screws"]]
        pts = []
        yside = 0.0
        for kind, objs, T in jobs:
            if kind == "part":
                pts.append(np.vstack([obj_world(i, T) for i in objs]).mean(0))
                yside += float(pts[-1][1])
            else:
                h, u = screw_axis(objs[0])
                pts.append(h + 120.0 * u)
                yside += float(h[1]) + 400.0 * float(u[1])     # round 10: from the side the screw's head faces
        work = np.mean(pts, axis=0)
        side_p = "B" if yside > 0.0 else "A"                   # round 9 always came from side A
        loc = loc_of_x(float(work[0])) if float(work[0]) <= TABLE_X else ("table", round(float(work[0]) / 100.0) * 100.0, "A")
        P = rp.person
        n_s = sum(1 for j in jobs if j[0] == "screw")
        n_p = sum(1 for j in jobs if j[0] == "part")
        what = ", ".join(x for x in ((f"sets {n_p} part{'s' if n_p > 1 else ''}" if n_p else ""),
                                     (f"drives {n_s} screw{'s' if n_s > 1 else ''}" if n_s else "")) if x)

        def job():
            poses = pstate.get("fit") or [None] * len(jobs)
            for (kind, objs, T), pose in zip(jobs, poses):
                secs = 300.0 if kind == "part" else 60.0
                nfj = 36 if kind == "part" else 24
                hu = screw_axis(objs[0]) if kind == "screw" else None
                if pose is None:                   # no person drawn (no spot)
                    pose = dict(hands={"l": None, "r": None}, palm={"l": None, "r": None}, look=tuple(work))
                if hu is not None:
                    rp.sc.alpha["op/tool/screwdriver"] = 1.0
                for f in range(nfj):
                    if P is not None and pstate["on"]:
                        P.set(hands=pose["hands"], palm=pose["palm"], look=pose["look"], lean=float(pose.get("lean", 0.0)),
                              frame=tot["n"])
                        pstate["n"] = tot["n"]
                        if hu is not None:
                            place_driver(P, *hu)
                    elif hu is not None:
                        rp.sc.alpha["op/tool/screwdriver"] = 0.0
                    if f == 3:                       # the hands have reached it: the part is in its seat, the screw in
                        for i in objs:               # its hole
                            if kind == "part":
                                rp.put([i], T)
                            rp.sc.alpha[f"o{i}"] = 1.0
                    sub = (f"a person {'sets it in its seat' if kind == 'part' else 'drives the screw with a hand driver'}: "
                           f"the arms could not ({'5 min a part' if kind == 'part' else '1 min a screw'}, estimate; shown "
                           f"x{secs / (nfj / FPS):.0f})")
                    if emit(cur["label"], sub, ["person"], proc=secs / nfj, add={"person_h": secs / nfj / 3600.0},
                            status="person", loc=loc):
                        return True
                rp.sc.alpha["op/tool/screwdriver"] = 0.0
                if P is not None:
                    P.set(hands={"l": None, "r": None}, palm={"l": None, "r": None}, lean=0.0, frame=tot["n"])
            return False
        for _ in range(int(FPS * 2.0)):
            if emit(cur["label"], f"a person is needed: {what}", ["person"], status="person", loc=loc):
                return True
        return person_job(tuple(work), side_p, job, loc, fit=fit_jobs(jobs))

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
            rp.retire_tools()              # the hand tools of the step before are back in their stand
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
                txt = ("pick at the parts table NOT planned" + (f" ({why_f})" if why_f else "") if row.get("fetch") == "FAIL"
                       else "a person stages the part at the station") + ": a person brings it and puts it in the gripper (estimate 2 min)"
                loc0 = here(n0)

                def card(txt=txt, loc0=loc0):
                    for _ in range(int(FPS * 4.0)):
                        if emit(cur["label"], txt, ["person"], status="person", loc=loc0):
                            return True
                    return False
                stop = person_job(rp.tcp(n0), n0, card, loc0)
            continue
        if k == "step_end":
            if cur["status"] in ("fail",) or e.get("status") == "fail":
                why = (e.get("row") or {}).get("why") or ""
                for _ in range(int(FPS * 2.5)):
                    stop = emit(cur["label"], f"FAILED: {why[:110]}", [], status="fail")
                    if stop:
                        break
            if not stop and (pend["screws"] or pend["parts"]):
                stop = person_fix()
            pend["screws"], pend["parts"], pend["failed"] = [], [], set()
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
                if e["x1"] > TABLE_X and e["x0"] <= TABLE_X:
                    away[n] = dict(x=float(e["x0"]), q=np.array(rp.st[n]["q"], copy=True), tool=rp.st[n]["tool"], drawn=False)
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
                # round 9: a fetch not shown is cut out only if something changed in the picture: round 8 cut at every one
                # (chapter 41: 10.3 jumps a minute). If nothing was drawn while the MiR was away and it is back at the same dock
                # with the arm in the same pose (only the part now in the gripper), the shot holds through the ellipsis.
                if e["x1"] <= TABLE_X:
                    a0 = away.pop(n, None)
                    same = (a0 is not None and not a0["drawn"] and abs(float(e["x1"]) - a0["x"]) < 1.0
                            and float(np.max(np.abs(rp.st[n]["q"] - a0["q"]))) < 1e-3)
                    if same and a0["tool"] != rp.st[n]["tool"]:      # the tool was changed at the MiR's stand on the way
                        note["txt"] += f"; {rp.st[n]['tool'].replace('_', ' ')} fitted at the MiR's tool stand"
                    if not same:
                        last["force"] = ("return" if a0 is None else
                                         f"return dx {abs(float(e['x1']) - a0['x']):.0f} dq "
                                         f"{float(np.degrees(np.max(np.abs(rp.st[n]['q'] - a0['q'])))):.1f} "
                                         f"tool {a0['tool']}->{rp.st[n]['tool']} drawn {a0['drawn']}")
            elif k in ("move", "screw") and e.get("q") is not None and len(e["q"]):
                rp.set_arm(n, q=np.asarray(e["q"][-1], float), close=e.get("close"))
                if e.get("unplanned"):
                    # round 9: the badge says FAIL only if the step failed (M26 passed; only its move back to park had no
                    # checked path, and round 8's card showed a FAIL badge on it)
                    nt = str(e.get("unplanned_note") or "").replace(" not planned", "")
                    txt = (f"arm {n}'s {nt}: no checked path, so not shown (the arm is cut to where it ends)" if nt else
                           f"NOT PLANNED: no checked path for arm {n}'s move here; not shown")
                    st_u = "fail" if step_status(cur["id"], cur.get("failed")) == "fail" else ""
                    for _ in range(int(FPS * 1.5)):
                        stop = emit(cur["label"], txt, who, status=st_u, loc=here(n))
                        if stop:
                            break
                    last["force"] = "unplanned"
            elif k == "tool":
                rp.st[n]["spec"] = e.get("spec") or {}
                rp.set_arm(n, tool=e["tool"])
            carry["s"] += float(e["dur"])
            carry["robot"] += float(e["dur"])
            continue
        if k == "jump":
            # the recording's next motion does not start where the arm is: never drawn as a jump inside a shot. Round 9: a
            # small one (up to JUMP_DEG on every joint: the module chapter's are 2.2-3.5 deg) is drawn as a short, labelled
            # move (not planned; the frame audit checks it like everything drawn); a larger one is a cut, as before
            q0 = np.array(rp.st[n]["q"], copy=True)
            q1 = np.asarray(e["to"], float)
            dq = float(np.degrees(np.max(np.abs(q1 - q0)))) if q0.shape == q1.shape else 1e9
            if dq <= JUMP_DEG:
                nj = max(4, int(math.ceil(dq / 0.75)))
                for f in range(nj):
                    rp.set_arm(n, q=q0 + (q1 - q0) * smooth((f + 1) / nj))
                    stop = emit(cur["label"], f"arm {n} repositions by {dq:.1f} deg (between two checked paths; not planned)",
                                [f"robot {n}"], proc=0.4 / nj, add={"robot_h": 0.4 / nj / 3600.0}, loc=here(n))
                    if stop:
                        break
                continue
            rp.set_arm(n, q=q1)
            last["force"] = f"jump {dq:.1f} deg"
            continue
        if k == "put":
            fs = [i for i in e["objs"] if i in pend["failed"]]
            if fs:                                        # a screw no arm could drive: in its hole, hidden until the person
                rp.put(fs, e["T"])                         # drives it
                for i in fs:
                    rp.sc.alpha[f"o{i}"] = 0.0
                    pend["screws"].append(i)
            rest = [i for i in e["objs"] if i not in pend["failed"]]
            if rest and step_status(cur["id"], cur.get("failed")) == "fail" and e.get("why") != "staged" and \
                    rows.get(cur["id"], {}).get("row", {}).get("arm") not in ("PART", None):
                # a failed placement: what the arm did not seat is set by the person. Round 10: everything it left more than
                # 1.5 mm off its seat (its box's corners), or never drew; round 9 counted only what was more than 50 mm off,
                # and put the rest in its seat as if the arm had (F57's beam tube, 9 mm short: no person was drawn). A part an
                # arm still holds stays in its hold (re-anchored at the put, as in round 9)
                T1 = np.asarray(e["T"], float)
                late = []
                held_now = {j for n_ in ("A", "B") if rp.st[n_]["held"] is not None for j in rp.st[n_]["held"]["objs"]}
                pending = {j for objs_, _ in pend["parts"] for j in objs_}
                # round 10 (W1's record.py puts a released part on its seat at once, why "seated", and the step's own put
                # follows): a part already left for the person stays where the arm left it until the person sets it
                rest = [i for i in rest if i not in pending]
                for i in rest:
                    k_ = f"o{i}"
                    if k_ not in rp.sc.actors or rp.objs.get(i, {}).get("kind") in FASTENERS or i in held_now:
                        continue
                    M0 = rp.sc.gmat.get(k_)
                    if rp.sc.alpha.get(k_, 0.0) > 0.0 and M0 is not None and seat_off(i, M0, T1) <= 1.5:
                        continue
                    late.append(i)
                if late:
                    pend["parts"].append((late, T1))
                    rest = [i for i in rest if i not in late]
                    print(f"   {cur['id']}: the person sets {len(late)} part(s) the arm left off their seats (mm): "
                          f"{[(i, round(seat_off(i, rp.sc.gmat.get(f'o{i}'), T1), 1)) for i in late][:6]}", flush=True)
                    for i in late:
                        k_ = f"o{i}"
                        M0 = rp.sc.gmat.get(k_)
                        if not (rp.sc.alpha.get(k_, 0.0) > 0.0 and M0 is not None and
                                float(np.linalg.norm(np.asarray(M0)[:3, 3] - T1[:3, 3])) < 600.0):
                            rp.put([i], T1)
                            rp.sc.alpha[k_] = 0.0              # far from its seat or not drawn: appears as the person sets it
            if rest:
                rp.put(rest, e["T"])
        elif k == "take":
            rp.retire_tools([i for i in e["objs"] if i in rp.temp_tools])
            for i in e["objs"]:
                if rp.objs.get(i, {}).get("kind") == "tool" and f"o{i}" in rp.sc.actors:
                    rp.sc.alpha[f"o{i}"] = 0.0         # a hand tool goes back to the stand
        elif k == "attach":
            # round 9: the hold keeps the fingers' closure it was taken at: the 2F-85's TCP moves as its fingers open, and
            # round 8 let a held part ride that (M19's stack ended 2.4 mm off its bore when arm A opened to let go)
            rp.st[n]["held"] = dict(objs=e["objs"], off=np.asarray(e["off"], float), close0=float(rp.st[n]["close"]))
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
            away.pop(n, None)                     # drawn: the MiR is seen leaving or coming back
            rt = e.get("route")
            chk = e.get("check") or {}
            loc = ("lane", n) if max(e["x0"], e["x1"]) > TABLE_X else ("cell", n)
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
                    where = ("to the parts table" if e["x1"] > TABLE_X else ("back to the bench" if e["x0"] > TABLE_X else
                                                                            "to the next dock"))
                    if rt.get("n_pivots"):
                        sub = (f"MiR {n}: pivot, drive, pivot: {rt['dist_mm'] / 1000:.1f} m and {rt['n_pivots']} pivots {where} "
                               f"({e['dur']:.0f} s: 1 m/s, 0.3 m/s2; pivots 30 deg/s, estimate{lapse_txt(per)})")
                    else:
                        rev = any(lg.get("rev") for lg in rt["legs"])
                        sub = (f"MiR {n} {'reverses' if rev else 'drives forward'} {rt['dist_mm'] / 1000:.1f} m {where} "
                               f"({e['dur']:.0f} s with docking{lapse_txt(per)})")
                else:
                    sub = f"MiR {n} drives {abs(e['x1'] - e['x0']) / 1000:.1f} m ({e['dur']:.0f} s{lapse_txt(per)})"
                if chk and not chk.get("ok", True):
                    sub += f"; NOT CLEAR: {chk.get('why', '')[:60]}"
                mp = rp.sc.gmat.get(f"mir{n}")
                wk = (np.asarray(mp, float)[:3, 3] + np.array([0.0, rp.yc0(n), 400.0]) if mp is not None and
                      rp.st[n].get("pose") is not None else np.array([float(rp.st[n]["x"]) + 350.0, rp.yc0(n), 400.0]))
                if DRIVE_HOLD and loc[0] == "cell":
                    wk = None          # a hop between the cell's docks may stay on the work's tripod (no cut either side)
                stop = emit(cur["label"], sub, who, proc=per, add={"robot_h": per / 3600.0}, loc=loc, work=wk,
                            status="fail" if (chk and not chk.get("ok", True)) else None)
                if stop:
                    break
            rp.st[n]["pose"] = None
            rp.set_arm(n, x=e["x1"])
            # round 9: no forced cut after a drawn drive (nothing jumped; round 8 cut back to the work after every one, so a
            # short hop between docks was two cuts and a 1-2 s shot)
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
                        if e.get("obj") is not None:
                            pend["failed"].add(int(e["obj"]))       # a person drives it after the step (round 9)
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
                    # round 9: the hook where the planner put and checked it (commit.hoist_hook: its bottom 300 mm over the
                    # carried part's top, over its footprint); round 8 drew it at the arms' midpoint + 60 mm, 50 mm into the
                    # build module. Without the planner's points it is not drawn.
                    hk = e.get("hook")
                    if hk is not None and len(hk) == len(QA):
                        rp.sc.alpha["hoist"] = 1.0
                        rp.sc.gmat["hoist"] = Tm(tuple(float(c) for c in np.asarray(hk)[j]))
                    else:
                        rp.sc.alpha["hoist"] = 0.0
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

            def job(e=e, wh=wh, nf=nf, per=per, loc=loc):
                for f in range(nf):
                    sub = (f"{e.get('what', '')[:80]} ({e['dur'] / 60:.0f} min, estimate{lapse_txt(per)})" if wh == "person" else
                           f"{e.get('what', '')[:80]} ({e['dur']:.0f} s)")
                    if emit(cur["label"], sub, [wh] if wh in ("person", "machine") else ["robot A"], proc=per,
                            add={"person_h": per / 3600.0} if wh == "person" else ({"robot_h": per / 3600.0} if wh == "robot" else None),
                            status="person" if wh == "person" else None, loc=loc):
                        return True
                return False
            if wh == "person" and rp.person is not None:
                # where the job is: the station of the place (the arm's tool over Fixture P or the trunnion), or the MiR's
                # stop at the table
                t0 = rp.tcp(n0)
                xp = {"bench": -1250.0, "B": 1350.0}.get(loc[0], float(t0[0]) if loc[0] == "PT" else float(rp.st[n0]["x"]))
                yp = 0.0 if loc[0] != "table" else (-300.0 if n0 == "A" else 300.0)
                stop = person_job((xp, yp, 950.0), "A", job, loc)
            else:
                stop = job()
    return tot


CHAP_TITLE = {k: v[1] for k, v in CHAP.items()}
FASTENERS = ("shcs", "fhcs", "set", "insert", "dowel", "plunger")
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
