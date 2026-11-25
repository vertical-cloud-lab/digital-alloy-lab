"""The hall of the robot-built desktop LPBF video, for the overview shots (00-intro, 10-parts, 50-integration): the long
parts table (common.LONG_TABLE) with every part on it as delivered (kit_table.py), the two-arm assembly bench with its
fixtures (analysis/assembly/cell2.py), the robot shop beside it (analysis/shop/shop_cell.py, moved by
common.SHOP_IN_HALL), the two UR12e arms each on a MiR250 (byu-vcl PR 318's meshes through analysis/robot/ur_arm.py and
cell2.ArmT, with the tool changer, 2F-85 and D405), a person (people.py) and a 355 ml soda can for scale.

    import hall
    h = hall.Hall()                      # everything; Hall(kit=False) for an empty table
    h.mir_to("A", x)                     # drive MiR A along its lane (the arm stays parked)
    img = h.sc.render(cam)               # cam = [position, focal point, up], mm

Frames are the hall's (common.py): mm, z up, the floor at z = 0; the bench and the long table run along x; MiR A works
from the front (y < 0), MiR B from the back.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
LPBF = HERE.parents[1]
for p in (HERE, LPBF / "analysis" / "assembly", LPBF / "analysis" / "robot", LPBF / "analysis" / "shop", LPBF / "cad"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import common  # noqa: E402
import pvscene  # noqa: E402

LT = common.LONG_TABLE
CAN = dict(d=66.0, h=122.0, color="#c8102e")       # a 355 ml (12 fl oz) can: 66 mm across, 122 mm tall


def poly(v, f):
    v = np.asarray(v, float)
    f = np.asarray(f, int)
    return pv.PolyData(v, np.c_[np.full(len(f), 3), f].ravel())


def Tm(p=(0.0, 0.0, 0.0), yaw_deg=0.0):
    m = np.eye(4)
    c, s = math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))
    m[:2, :2] = [[c, -s], [s, c]]
    m[:3, 3] = p
    return m


def merged_by_colour(items):
    """[(name, (v, f), colour)] -> {colour: one PolyData}: far fewer actors for the shop's and the bench's boxes."""
    out = {}
    for _, (v, f), col in items:
        if v is None or not len(f):
            continue
        out.setdefault(col, []).append(poly(v, f))
    return {c: (ms[0] if len(ms) == 1 else ms[0].merge(ms[1:])) for c, ms in out.items()}


class ArmVis:
    """The visual meshes of one cell2.ArmT (UR12e links, the tool changer, the 2F-85 and the D405), as pvscene groups
    that follow the arm's joint values (update())."""

    def __init__(self, sc, arm, tag):
        import cell as C
        import tooling as TL
        import ur_arm
        self.sc, self.arm, self.tag = sc, arm, tag
        self.C, self.TL, self.ur = C, TL, ur_arm
        for link, lst in ur_arm.arm_meshes(C.MODEL).items():
            for j, (m, c, s) in enumerate(lst):
                sc.add(f"{tag}/{link}/{j}", m, c, group=f"{tag}/{link}", specular=s)
        for part, lst in ur_arm.gripper_meshes().items():
            for j, (m, c, s) in enumerate(lst):
                sc.add(f"{tag}/gr/{part}/{j}", m, c, group=f"{tag}/gr/{part}", specular=s)
        (v, f), _ = TL.mesh("changer")
        sc.add(f"{tag}/changer", poly(v, f), "#3a3f45", group=f"{tag}/changer", specular=0.3)
        self.update()

    def update(self):
        a, sc, tag = self.arm, self.sc, self.tag
        F = a.fk()
        for link in self.C.ARM_LINKS:
            sc.gmat[f"{tag}/{link}"] = a.base @ F[link]
        W0 = a.base @ F["tool0"]
        th = self.TL.TC["h"]
        sc.gmat[f"{tag}/changer"] = W0 @ Tm((0.0, 0.0, th))
        Wt = W0 @ Tm((0.0, 0.0, th))
        G = self.ur.gripper_fk(a.close)
        for part, M in G.items():
            sc.gmat[f"{tag}/gr/{part}"] = W0 if part == "camera" else Wt @ M

    def names(self):
        return [n for n in self.sc.actors if n.startswith(self.tag + "/")]


class MirVis:
    """A MiR250 with PR 318's cabinet and mounting plate (cell2.mir_bodies), its light strip and lidar windows, as one
    group that drives along x on its lane."""

    def __init__(self, sc, tag, side):
        import cell2 as K
        self.sc, self.tag, self.side = sc, tag, side
        cols = {"MiR250": common.COL["mir"], "cabinet": common.COL["cabinet"], "mounting plate": "#59616a",
                "tool stand": "#8a6d3b"}
        for name, (v, f), _ in K.mir_bodies(tag, 0.0, side):
            key = next((k for k in cols if k in name), "MiR250")
            sc.add(f"mir{tag}/{name}", poly(v, f), cols[key], group=f"mir{tag}", specular=0.2)
        s = -1.0 if side == "front" else 1.0
        yc = s * (K.ARM_Y + K.ARM_OFF)
        L, Wd = K.MIR["L"], K.MIR["W"]
        strip = pv.Box(bounds=(-L / 2 - 2, L / 2 + 2, yc - Wd / 2 - 2, yc + Wd / 2 + 2, 150.0, 175.0))
        sc.add(f"mir{tag}/light strip", strip.triangulate(), "#e8eef5", group=f"mir{tag}", specular=0.1)
        top = pv.Box(bounds=(-L / 2 + 2, L / 2 - 2, yc - Wd / 2 + 2, yc + Wd / 2 - 2, 296.0, 302.0))
        sc.add(f"mir{tag}/top", top.triangulate(), common.COL["mir_top"], group=f"mir{tag}", specular=0.1)
        self.x = 0.0

    def at(self, x):
        self.x = float(x)
        self.sc.gmat[f"mir{self.tag}"] = Tm((self.x, 0.0, 0.0))


class Hall:
    def __init__(self, pl=None, kit="stock", shop=True, bench=True, robots=True, person=True, size=(common.W, common.H)):
        """kit: "stock" (every part as delivered: machined parts as their blanks), "finished", or None (empty table)."""
        self.pl = pl if pl is not None else common.plotter(size)
        self.sc = pvscene.PVScene(self.pl)
        self.kit_items = []                  # kit_table.py's layout (what is on the long table), when loaded
        self.kt = None
        self.labels3d = {}                   # name -> 3-D point, for screen labels
        self._floor()
        if not (kit and self.load_kit(kit)):
            self._long_table()
        if bench:
            self._bench()
        if shop:
            self._shop()
        self.arms, self.mirs = {}, {}
        if robots:
            self._robots()
        self.can_xyz = (LT["x0"] + 520.0, LT["y0"] + 150.0, LT["top"])
        self._can(self.can_xyz)
        self.person = None
        if person:
            import people
            self.person = people.Person(self.sc, "op")
            self.person.set(x=LT["x0"] - 450.0, y=-150.0, hd=-90.0, amp=0.0, look=(LT["x0"] + 800.0, -100.0, 900.0))

    # ------------------------------------------------------------------------------------------- the room
    def _floor(self):
        sc = self.sc
        sc.add("floor", pv.Plane(center=(6000.0, -4000.0, -1.0), i_size=30000.0, j_size=22000.0, i_resolution=1,
                                 j_resolution=1), common.FLOOR, specular=0.0)
        tape = []
        y_out = 640.0 + 130.0 + 290.0 + 60.0               # the lanes' outer edges: arm 640, MiR centre +130, half 290
        for y in (-y_out, y_out):
            tape.append(pv.Box(bounds=(-2600.0, LT["x1"] + 900.0, y - 25.0, y + 25.0, 0.0, 1.5)))
        for x in (-2600.0, LT["x1"] + 900.0):
            tape.append(pv.Box(bounds=(x - 25.0, x + 25.0, -y_out, y_out, 0.0, 1.5)))
        sy = common.SHOP_IN_HALL[1]
        for y in (4000.0 + sy - 40.0, 7000.0 + sy + 40.0):  # the shop's aisle (shop_cell.AISLE)
            tape.append(pv.Box(bounds=(600.0, 15400.0, y - 25.0, y + 25.0, 0.0, 1.5)))
        sc.add("floor tape", tape[0].merge(tape[1:]).triangulate(), "#e3b505", specular=0.0)

    def _long_table(self):
        sc = self.sc
        x0, x1, y0, y1, top, t = LT["x0"], LT["x1"], LT["y0"], LT["y1"], LT["top"], LT["t"]
        sc.add("long table top", pv.Box(bounds=(x0, x1, y0, y1, top - t, top)).triangulate(), common.COL["table"],
               specular=0.15)
        legs, rails = [], []
        n = int(round((x1 - x0) / 1500.0))
        for k in range(n + 1):
            x = x0 + 40.0 + k * (x1 - x0 - 80.0) / n
            for y in (y0 + 40.0, y1 - 40.0):
                legs.append(pv.Box(bounds=(x - 25.0, x + 25.0, y - 25.0, y + 25.0, 0.0, top - t)))
        for y in (y0 + 40.0, y1 - 40.0):
            rails.append(pv.Box(bounds=(x0 + 15.0, x1 - 15.0, y - 20.0, y + 20.0, top - t - 70.0, top - t)))
            rails.append(pv.Box(bounds=(x0 + 15.0, x1 - 15.0, y - 15.0, y + 15.0, 140.0, 180.0)))
        sc.add("long table legs", legs[0].merge(legs[1:] + rails).triangulate(), common.COL["table_leg"], specular=0.3)
        self.labels3d["long table"] = ((x0 + x1) / 2, y0, top)

    def _bench(self):
        import cell2 as K
        sc = self.sc
        self.cell = K.Cell(None)                     # the static bench, fixtures and the two arms (cell2's frame)
        items = [(n, (b.v @ b.M[:3, :3].T + b.M[:3, 3], b.f), b.color) for n, b in self.cell.static.items()
                 if n != "floor" and not n.startswith(("A ", "B "))]
        for k, (col, m) in enumerate(merged_by_colour(items).items()):
            sc.add(f"bench/{k}", m, col, specular=0.25)
        self.labels3d["assembly bench"] = (-1150.0, -400.0, K.BENCH["top"])
        self.labels3d["trunnion"] = (K.STATIONS["T"], 0.0, 1300.0)
        self.labels3d["Fixture B"] = (K.STATIONS["B"], 0.0, K.Z_B + 200.0)

    def _shop(self):
        import shop_cell as S
        sc = self.sc
        self.shop = S.build_shop()
        off = common.SHOP_IN_HALL
        items = []
        for st in self.shop.values():
            for name, (v, f), col in st.world_items():
                items.append((name, (np.asarray(v, float) + off, f), col))
        for k, (col, m) in enumerate(merged_by_colour(items).items()):
            sc.add(f"shop/{k}", m, col, specular=0.25)
        for key, text in (("vf4", "Haas VF-4 + HRT210"), ("lathe", "CNC lathe"), ("saw", "bandsaw"),
                          ("wash", "deburr + wash"), ("measure", "measuring"), ("receiving", "receiving"),
                          ("stock", "stock racks"), ("kit", "kitting rack")):
            st = self.shop[key]
            p = st.to_world((0.0, 600.0, 1500.0)) + off
            self.labels3d[text] = tuple(p)

    def _robots(self):
        cl = self.cell if hasattr(self, "cell") else None
        if cl is None:
            import cell2 as K
            cl = self.cell = K.Cell(None)
        for tag, arm, side in (("A", cl.A, "front"), ("B", cl.B, "back")):
            arm.q = arm.park_q()
            arm.close = 0.0
            self.arms[tag] = ArmVis(self.sc, arm, tag)
            self.mirs[tag] = MirVis(self.sc, tag, side)
        self.mir_to("A", LT["x0"] + 900.0)
        self.mir_to("B", 350.0)

    def mir_to(self, tag, x, q=None):
        """MiR `tag` with its arm base at x along its lane; the arm parked (or at q)."""
        arm = self.arms[tag].arm
        arm.move_base(float(x))
        if q is not None:
            arm.q = np.asarray(q, float)
        arm.place()
        self.arms[tag].update()
        self.mirs[tag].at(float(x))

    def _can(self, xyz):
        x, y, z = xyz
        body = pv.Cylinder(center=(x, y, z + CAN["h"] / 2), direction=(0, 0, 1), radius=CAN["d"] / 2,
                           height=CAN["h"], resolution=48)
        self.sc.add("soda can", body.triangulate(), CAN["color"], specular=0.7)
        top = pv.Cylinder(center=(x, y, z + CAN["h"] + 0.5), direction=(0, 0, 1), radius=CAN["d"] / 2 - 4.0,
                          height=1.5, resolution=48)
        self.sc.add("soda can top", top.triangulate(), "#c9ced3", specular=0.8)

    # ------------------------------------------------------------------------------------------- the parts
    def load_kit(self, mode="stock"):
        """The long table with every part on it, from kit_table.py (the assembly worker's layout: the table, nests,
        trays, bins, pallets and every item); False if kit_table can't be loaded."""
        kt = kit_table()
        if kt is None:
            return False
        try:
            ms = kt.meshes(mode=mode)
        except Exception as e:                                  # noqa: BLE001
            print(f"hall: kit_table.meshes failed ({e!r}); the long table is empty", flush=True)
            return False
        for k, m in enumerate(ms):
            nm = f"kit/{m['key']}/{k}"
            self.sc.add(nm, m["mesh"], m["color"], group="kit", specular=0.3 if m["key"] != "table" else 0.15)
        self.kit_items = ms
        self.kt = kt
        self.labels3d["long table"] = ((LT["x0"] + LT["x1"]) / 2, LT["y0"], LT["top"])
        return True

    # ------------------------------------------------------------------------------------------- labels
    def labels(self, names):
        """[[x_px, y_px, text]] for the named 3-D points that are in front of the camera and on screen."""
        out = []
        for n in names:
            p = self.labels3d.get(n)
            if p is None:
                continue
            (x, y), = common.project(self.pl, [p])
            if 0 <= x <= common.W and 70 <= y <= common.H - 20:
                out.append([round(x, 1), round(y, 1), n])
        return out


def kit_table():
    """kit_table.py (the assembly worker's): from this folder, or from $KIT_TABLE_DIR until it is merged here."""
    import os
    extra = os.environ.get("KIT_TABLE_DIR")
    if extra and extra not in sys.path:
        sys.path.append(extra)
    try:
        import kit_table as kt
        return kt
    except Exception as e:                                      # noqa: BLE001
        print(f"hall: no kit_table ({e!r})", flush=True)
        return None


def orbit(focal, dist, az_deg, el_deg):
    az, el = math.radians(az_deg), math.radians(el_deg)
    return (focal[0] + dist * math.cos(el) * math.sin(az), focal[1] - dist * math.cos(el) * math.cos(az),
            focal[2] + dist * math.sin(el))


if __name__ == "__main__":
    import time
    t = time.time()
    h = Hall()
    print(f"hall built in {time.time() - t:.1f} s, {len(h.sc.actors)} actors", flush=True)
    from PIL import Image
    for k, cam in enumerate([
        [orbit((6000.0, -4000.0, 0.0), 21000.0, -20.0, 50.0), (6000.0, -4000.0, 0.0), (0, 0, 1)],
        [orbit((1500.0, 0.0, 700.0), 5200.0, -35.0, 25.0), (1500.0, 0.0, 700.0), (0, 0, 1)],
    ]):
        t = time.time()
        img = h.sc.render(cam)
        Image.fromarray(img).save(f"/tmp/robotbuild/hall_{k}.png")
        print(f"frame {k}: {time.time() - t:.1f} s", flush=True)
