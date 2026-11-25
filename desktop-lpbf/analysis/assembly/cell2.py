"""Two UR12e arms on MiR250s at an assembly bench, for the robotic build of the desktop LPBF (issue #260, PR #266).

Built on ../robot/cell.py (byu-vcl PR 318's arm, gripper, D405, FCL meshes, IK branches, RRT-Connect, the 1.5 mm audit),
which is imported, not edited. What this module adds:
  * ArmT: a cell.Arm with an automatic tool changer between the flange and the tool, so it can carry the 2F-85 (with or
    without fingertip caps), a screwdriver, a vacuum gripper or a roller; the D405 stays on the arm side of the changer.
    IK and the held part use the active tool's TCP.
  * Cell: the floor, the bench, the fixtures (tooling.py), two MiR250s (800 x 580 x 300, 480 mm cabinet, 20 mm plate: the
    arm base 800 mm above the floor, as cell.py and PR 318) that dock at stations along the bench, a tool stand on each
    cabinet (PR 318: finger sets on a stand on the MiR), and the machine's parts posed per sub-assembly.
  * World(): what one arm can hit: the cell, every machine part present, and the other arm with its tool and held part.
    cell.Checker then runs unchanged on it (collisions, the depth audit, plan = straight joint line or RRT-Connect).

World frame: mm, z up, floor at z = 0. The bench runs along x; arm A docks on the front (y < 0), arm B on the back.
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
for p in (HERE, HERE.parent / "robot", HERE.parent / "ops", HERE.parents[1] / "cad"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import cell as C  # noqa: E402
import ur_arm  # noqa: E402
import tooling as TL  # noqa: E402
from cell import Body, Group, Tm, inv, rot, box_mesh  # noqa: E402

MIR = dict(C.MIR)                         # L 800 (along x), W 580, H 300, cabinet 480, plate 20
ARM_Z = MIR["H"] + MIR["cab_h"] + MIR["plate"]   # 800: arm base above the floor
ARM_OFF = 130.0                           # the arm sits 130 mm toward the work from the MiR's centre (cell.py)
BENCH = dict(x0=-1550.0, x1=-750.0, y0=-400.0, y1=400.0, top=760.0, t=40.0)
ARM_Y = 640.0                             # |y| of the arm bases: 240 mm off the bench edge, as PR 318 parks at the VLM face
Z_B = 1000.0                              # Fixture B: underside of the process base plate above the floor (screws from below with the angle-head nutrunner)
Z_P = 1000.0                              # Fixture P: underside of the chamber floor plate above the floor
# run 2: the chamber turns over in a trunnion positioner (station T, on the floor) instead of in the two arms; Fixture C left
STATIONS = dict(stack=-1400.0, body_inv=-1250.0, body_up=-1100.0, P=-350.0, T=350.0, B=1350.0)
DOCKS = dict(M=-1250.0, M2=-1400.0, M3=-1100.0, P=-350.0, PT=0.0, T=350.0, TB=850.0, B=1350.0, Bl=1130.0, Br=1570.0)
TC_H = TL.TC["h"]
# MiR250 + 131 kg ballast plate low in its base (byu-vcl PR 318); masses for the tip-over check (run_assembly.py)
MASS = dict(mir=94.0, ballast=131.0, cabinet=30.0, control_box=12.0, arm=33.5)     # MiR and UR datasheets; cabinet estimated


def Rx(deg):
    return Tm(rot((1, 0, 0), deg))


def Ry(deg):
    return Tm(rot((0, 1, 0), deg))


def Rz(deg):
    return Tm(rot((0, 0, 1), deg))


class MBody(Body):
    """A Body that reuses an FCL BVH built elsewhere (the ops scene's 0.1 mm meshes), to save memory."""

    def __init__(self, name, v, f, bvh, kind="machine", color="#b9c0c7"):
        import fcl
        self.name, self.kind, self.group, self.color = name, kind, "", color
        self.v, self.f = v, f
        self.geom = bvh
        self.obj = fcl.CollisionObject(bvh, fcl.Transform())
        self.M = np.eye(4)
        self.lo, self.hi = v.min(0), v.max(0)
        self._ero = None
        self.mat = None


# ------------------------------------------------------------------------------------------------ the arm with a tool changer
_TOOL_MESH = {}


def tool_mesh(name, extra_bit=0.0, tip_d=None):
    """((v, f), T_tcp) of an end effector in its mounting frame (the tool side of the changer)."""
    key = (name, float(extra_bit), tip_d)
    if key not in _TOOL_MESH:
        if name in ("screwdriver", "nutrunner", "nutrunner_angle"):
            _TOOL_MESH[key] = TL.mesh(name, float(extra_bit), float(tip_d or (3.0 if name == "screwdriver" else 5.8)))
        elif name == "vacuum":
            _TOOL_MESH[key] = TL.mesh("vacuum")
        elif name == "nozzle":
            _TOOL_MESH[key] = TL.mesh("nozzle")
        elif name in ("roller", "roller_n"):
            _TOOL_MESH[key] = TL.mesh("roller", 3.2 if name == "roller" else 1.4)
        else:
            raise KeyError(name)
    return _TOOL_MESH[key]


TOOL_MASS = dict(gripper=0.925, screwdriver=TL.SCREWDRIVER["mass"], nutrunner=TL.NUTRUNNER["mass"], nutrunner_angle=TL.NUT_ANGLE["mass"],
                 vacuum=TL.VAC["mass"], nozzle=TL.VAC["mass"] + 0.05, roller=0.35,
                 roller_n=0.35)


class ArmT(C.Arm):
    def __init__(self, name, x, side):
        y = -ARM_Y if side == "front" else ARM_Y
        super().__init__(name=name, base=(x, y, ARM_Z), yaw_deg=0.0 if side == "front" else 180.0)
        self.side = side
        self.cam = self.grip.pop("camera")
        (v, f), _ = TL.mesh("changer")
        self.fixed = {"camera": self.cam, "changer": Body(f"{name}/changer", v, f, kind="gripper", group="gripper", color="#3a3f45")}
        self.stock = dict(self.grip)
        self.tool_name = "gripper"
        self.tool_tcp = np.eye(4)
        self._rebuild()
        self.q = self.park_q()

    def _rebuild(self):
        self.robot = Group(list(self.links.values()) + list(self.grip.values()) + list(self.caps.values()) +
                           list(self.fixed.values()))

    def park_q(self):
        return np.radians([90.0, -110.0, 120.0, -100.0, -90.0, 0.0])

    def move_base(self, x):
        y = self.base[1, 3]
        self.base = Tm(rot((0, 0, 1), 0.0 if self.side == "front" else 180.0), (x, y, ARM_Z))

    # ---- tools
    def set_tool(self, name, caps=None, extra_bit=0.0, tip_d=None):
        for b in list(self.grip.values()) + list(self.caps.values()):
            self.robot.remove(b.name)
        self.caps, self.cap_spec = {}, None
        if name == "gripper":
            self.grip = dict(self.stock)
            if caps:
                C.Arm.set_caps(self, caps)
        else:
            (v, f), T = tool_mesh(name, extra_bit, tip_d)
            self.grip = {name: Body(f"{self.name}/tool/{name}", v, f, kind="tool", group="gripper", color="#c58b2b")}
            self.tool_tcp = np.asarray(T, float)
        self.tool_name = name
        self._rebuild()

    def tcp_local(self, close=None):
        if self.tool_name == "gripper":
            return Tm(p=(0.0, 0.0, TC_H + C.Arm.tcp_mm(self, close)))
        return Tm(p=(0.0, 0.0, TC_H)) @ self.tool_tcp

    def tcp_mm(self, close=None):
        return float(self.tcp_local(close)[2, 3])

    def tcp(self, q=None, close=None):
        return self.base @ self.fk(q)["tool0"] @ self.tcp_local(close)

    def place(self, q=None, close=None):
        if q is not None:
            self.q = np.asarray(q, float)
        if close is not None:
            self.close = float(close)
        F = self.fk()
        for k, b in self.links.items():
            b.place(self.base @ F[k])
        W0 = self.base @ F["tool0"]
        self.fixed["camera"].place(W0)
        self.fixed["changer"].place(W0 @ Tm(p=(0.0, 0.0, TC_H)))
        Wt = W0 @ Tm(p=(0.0, 0.0, TC_H))
        if self.tool_name == "gripper":
            G = ur_arm.gripper_fk(self.close)
            for k, b in self.grip.items():
                b.place(Wt @ G[k])
            for tip, b in self.caps.items():
                b.place(Wt @ G[tip])
        else:
            for b in self.grip.values():
                b.place(Wt)
        if self.held is not None:
            hb, off = self.held
            hb.place(W0 @ self.tcp_local() @ off)
        return F

    def hold(self, body, off):
        self.release()
        self.held = (body, off)
        self.robot.add(body)

    def release(self):
        if self.held is not None:
            self.robot.remove(self.held[0].name)
        self.held = None

    def ik_all(self, T_tcp_world, seed=None):
        seed = self.q if seed is None else np.asarray(seed, float)
        T06 = inv(self.base) @ np.asarray(T_tcp_world, float) @ inv(self.tcp_local())
        out = []
        for s in ur_arm._ik_analytic(C.MODEL, T06, q6_free=float(seed[5])):
            q = ur_arm._polish(C.MODEL, ur_arm._wrap_near(s, seed), T06)
            e = ur_arm._pose_err(ur_arm.fk(C.MODEL, q)["tool0"], T06)
            if np.linalg.norm(e[:3]) < 1e-3 and np.linalg.norm(e[3:]) < 1e-6:
                q = ur_arm._wrap_near(q, seed)
                if np.all(np.abs(q) <= ur_arm._LIMIT + 1e-9) and all(np.abs(q - o).max() > 1e-4 for o in out):
                    out.append(q)
        out.sort(key=lambda q: float(np.sum((q - seed) ** 2)))
        return out

    def self_hits(self):
        out = []
        grp = {k: [self.links[k]] for k in C.ARM_LINKS}
        grp["gripper"] = (list(self.grip.values()) + list(self.caps.values()) + list(self.fixed.values()) +
                          ([self.held[0]] if self.held else []))
        for a, b in self.self_pairs():
            for x in grp[a]:
                for y in grp[b]:
                    if C.hit(x.obj, y.obj):
                        out.append((x.name, y.name))
        return out

    def bodies(self):
        yield from self.links.values()
        yield from self.grip.values()
        yield from self.caps.values()
        yield from self.fixed.values()
        if self.held is not None:
            yield self.held[0]


# ------------------------------------------------------------------------------------------------ the cell
def mir_bodies(tag, x, side):
    """MiR250 body, cabinet, mounting plate and tool stand for an arm whose base is at x on `side`."""
    ya = -ARM_Y if side == "front" else ARM_Y
    s = -1.0 if side == "front" else 1.0
    yc = ya + s * ARM_OFF                    # MiR centre, 130 mm behind the arm base
    L, W, H, Cb = MIR["L"], MIR["W"], MIR["H"], MIR["cab_h"]
    out = [(f"{tag} MiR250", box_mesh(x - L / 2, x + L / 2, yc - W / 2, yc + W / 2, 30.0, H), "#3b4148"),
           (f"{tag} cabinet", box_mesh(x - L / 2 + 40, x + L / 2 - 40, yc - W / 2 + 30, yc + W / 2 - 30, H, H + Cb), "#3b4148"),
           (f"{tag} mounting plate", box_mesh(x - 170, x + 170, yc - W / 2 + 30, yc + W / 2 - 30, H + Cb, ARM_Z - 1.0), "#59616a")]
    # tool stand: hung on the cabinet's far face, below its top (run 1 had it on the top behind the arm base, where arm B's
    # upper arm met it in the second turn-over, F05)
    y_face = yc + s * (W / 2 - 30)
    out.append((f"{tag} tool stand", box_mesh(x - 170, x + 170, min(y_face, y_face + s * 170), max(y_face, y_face + s * 170),
                                               H + 40.0, H + Cb - 20.0), "#8a6d3b"))
    # round 7: the screw presenter on the cabinet top, 300 mm along x from the arm base (fetch.PRESENTER: a vibratory rail
    # presenter in the OHTAKE NJ / Weber SEV class, 250 x 130 x 150 mm envelope, an estimate)
    out.append((f"{tag} screw presenter", box_mesh(x + 300 - 125, x + 300 + 125, yc - 65, yc + 65, H + Cb, H + Cb + 150.0), "#4a6b8a"))
    return out


class Cell:
    def __init__(self, sc):
        """sc: the ops scene (checks.Scene) holding every machine object (parts, and one object per screw)."""
        self.sc = sc
        self.static = {}
        self._add_static()
        self.A = ArmT("A", DOCKS["T"], "front")
        self.B = ArmT("B", DOCKS["T"], "back")
        self.mir = {"A": [], "B": []}
        self.dock = {"A": None, "B": None}
        self.move_mir("A", DOCKS["T"])
        self.move_mir("B", DOCKS["T"])
        self.mbody = {}                      # machine object index -> MBody
        self.where = {}                      # machine object index -> 4x4 machine-to-world of its sub-assembly
        self.state = {}

    def _add(self, name, vf, color="#9aa1a8", kind="cell"):
        v, f = vf
        self.static[name] = Body(name, v, f, kind=kind, color=color)

    def _add_static(self):
        b = BENCH
        self._add("floor", box_mesh(-3000, 3000, -2500, 2500, -20.0, 0.0), "#d9d9d9")
        self._add("bench top", box_mesh(b["x0"], b["x1"], b["y0"], b["y1"], b["top"] - b["t"], b["top"]), "#7d8790")
        for x in (b["x0"] + 40, b["x1"] - 40):
            for y in (b["y0"] + 40, b["y1"] - 40):
                self._add(f"bench leg {x:.0f} {y:.0f}", box_mesh(x - 30, x + 30, y - 30, y + 30, 0.0, b["top"] - b["t"]), "#7d8790")
        # fixtures, posed in the world
        self.T_fix = {}
        TT = Tm(p=(STATIONS["T"], 0.0, TL.TRUNNION["h_axis"]))
        self.T_fix["T"] = TT
        self._add("Trunnion stands", self._tx(TL.mesh("trunnion_stands")[0], TT), "#c9a227", "fixture")
        v, f = TL.mesh("trunnion_jaws")[0]
        self.static["Trunnion jaws"] = Body("Trunnion jaws", v, f, kind="fixture", color="#d18a1f")
        self.static["Trunnion jaws"].place(TT)
        self.jaw_angle = 0.0
        TB = Tm(p=(STATIONS["B"], 0.0, Z_B + 175.0))
        self.T_fix["B"] = TB
        self._add("Fixture B (open stand)", self._tx(TL.mesh("fixture_B", Z_B)[0], TB), "#c9a227", "fixture")
        TP = Tm(p=(STATIONS["P"], 0.0, Z_P + 20.0))
        self.T_fix["P"] = TP
        self._add("Fixture P (floor-plate pedestal)", self._tx(TL.mesh("fixture_P", Z_P)[0], TP), "#c9a227", "fixture")
        T = Tm(p=(STATIONS["stack"], 0.0, b["top"] + 146.0))
        self._add("Stack nest", self._tx(TL.mesh("nest_stack")[0], T), "#c9a227", "fixture")
        T = Tm(p=(STATIONS["body_inv"], 0.0, b["top"] + 140.0))
        self._add("Module nest, upside down", self._tx(TL.mesh("nest_body_inv")[0], T), "#c9a227", "fixture")
        T = Tm(p=(STATIONS["body_up"], 0.0, b["top"] + 200.0))
        self._add("Module nest, upright", self._tx(TL.mesh("nest_body_up")[0], T), "#c9a227", "fixture")

    @staticmethod
    def _tx(vf, T):
        v, f = vf
        return (v @ T[:3, :3].T + T[:3, 3], f)

    # ---- phase transforms: machine frame -> world
    def T_phase(self, phase):
        b = BENCH
        if phase == "stack_inv":           # heater block's top face (machine z = -10) on the stack nest
            return Tm(p=(STATIONS["stack"], 0.0, b["top"] + 146.0 - 10.0)) @ Ry(180.0)
        if phase == "stack_up":            # upright stack held by the arm over the module nest (plate on it)
            return Tm(p=(STATIONS["stack"], 0.0, b["top"] + 40.0 + 130.0))
        if phase == "body_inv":            # module on its spigot face (machine z = 0)
            return Tm(p=(STATIONS["body_inv"], 0.0, b["top"] + 140.0)) @ Ry(180.0)
        if phase == "body_up":             # module upright, flange underside (machine z = -30) on the nest's posts
            return Tm(p=(STATIONS["body_up"], 0.0, b["top"] + 200.0))
        if phase == "chamber_up_P":        # floor plate's underside (machine z = -20) on Fixture P's column
            return self.T_fix["P"]
        if phase == "chamber_up_T":        # chamber upright in the trunnion's jaws, machine z 50 on the turn axis
            return self.T_fix["T"] @ Tm(p=(0.0, 0.0, -50.0))
        if phase == "chamber_inv":         # the trunnion turned 180 deg about x: chamber upside down
            return self.T_fix["T"] @ Rx(180.0) @ Tm(p=(0.0, 0.0, -50.0))
        if phase == "upright":             # process module on Fixture B
            return self.T_fix["B"]
        raise KeyError(phase)

    def move_mir(self, arm, x):
        a = self.A if arm == "A" else self.B
        for n in self.mir[arm]:
            self.static.pop(n, None)
        self.mir[arm] = []
        for n, vf, col in mir_bodies(arm, x, a.side):
            self._add(n, vf, col, "cell")
            self.mir[arm].append(n)
        a.move_base(x)
        a.place()
        self.dock[arm] = x

    # ---- machine objects
    def body(self, i):
        if i not in self.mbody:
            o = self.sc.objs[i]
            p = self.sc.parts[o["part"]]
            self.mbody[i] = MBody(self.sc.label(i), o["V"], o["F"], o["bvh"], color=p.color)
        return self.mbody[i]

    def put(self, idx, T_world_from_machine, state=None):
        """Objects idx are now in the cell, in a sub-assembly whose machine frame is at T (their state-dependent pose on top)."""
        st = self.state if state is None else state
        for i in idx:
            if self.sc.objs[i]["V"] is None:
                continue
            self.where[i] = np.asarray(T_world_from_machine, float)
            self.body(i).place(self.where[i] @ self.sc.pose(i, st))

    def take(self, idx):
        for i in idx:
            self.where.pop(i, None)

    def world(self, actor, exclude=(), other=True):
        """Everything arm `actor` can hit: static cell bodies, machine objects present, and the other arm."""
        g = Group(self.static.values())
        ex = set(exclude)
        for i in self.where:
            if i not in ex:
                g.add(self.mbody[i])
        if other:
            o = self.B if actor == "A" else self.A
            for b in o.bodies():
                g.add(b)
        return g


class View:
    """Duck-typed scene for cell.Checker: only .world is used."""

    def __init__(self, world):
        self.world = world


def checker(cell, arm_name, exclude=()):
    arm = cell.A if arm_name == "A" else cell.B
    return C.Checker(View(cell.world(arm_name, exclude)), arm)
