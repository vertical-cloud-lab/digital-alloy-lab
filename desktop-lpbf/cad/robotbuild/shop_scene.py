"""The robot shop drawn for the round-7 chapters: equipment.py's models at their shop poses, the two UR12e + MiR250s,
the tools, the parts in their cut states and the person, all in one pvscene.PVScene so that every moving thing is a group
with a 4x4 (issue #260, PR #266). shop_chapters.py drives it frame by frame from the planner's recordings
(/tmp/robotbuild/traj/shop_<clip>.pkl).

Frames: the shop frame of analysis/shop/shop_cell.py (mm, z up); hall = shop + common.SHOP_IN_HALL.
"""
from __future__ import annotations

import math
import os
import pathlib
import sys

import numpy as np
import pyvista as pv

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parents[1]
for p in (HERE, LPBF / "analysis" / "robot", LPBF / "analysis" / "shop"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import common as CM  # noqa: E402
import equipment as E  # noqa: E402

try:                                    # the video worker's person (byu-vcl PR 318's MakeHuman), once merged
    import pvscene  # noqa: E402
    import people  # noqa: E402
except ImportError:                     # until the merge: the copy fetched from that worker's branch
    sys.path.insert(0, "/tmp/robotbuild/vendor_video")
    import pvscene  # noqa: E402
    import people  # noqa: E402
import ur_arm  # noqa: E402
import shop_cell as S  # noqa: E402

MODEL = "ur10e"
CHAMBER = pathlib.Path("/tmp/robotbuild/cache/shop/chamber")
POSE = dict(vf4=(2600.0, 7000.0, 0.0), lathe=(6700.0, 7000.0, 0.0), wash=(10100.0, 7000.0, 0.0),
            measure=(11900.0, 7000.0, 0.0), bench=(14200.0, 7000.0, 0.0), receiving=(2400.0, 4000.0, 180.0),
            stock=(5600.0, 4000.0, 180.0), saw=(8600.0, 4000.0, 180.0), kit=(11400.0, 4000.0, 180.0),
            charge=(14000.0, 4000.0, 180.0), tools=(12900.0, 4000.0, 180.0), tig=(16300.0, 7000.0, 0.0))


def Mst(key, pose=None):
    x, y, yaw = pose or POSE[key]
    return E.T((x, y, 0.0), E.Rz(yaw))


def rgb(c):
    if isinstance(c, str):
        c = c.lstrip("#")
        return tuple(int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return tuple(c)


def _spec_key(spec):
    """What identifies an object's mesh (arrays left out)."""
    return tuple((k, str(v)) for k, v in sorted(spec.items()) if k not in ("v", "f"))


def vf_mesh(v, f):
    f = np.asarray(f, np.int64)
    return pv.PolyData(np.asarray(v, float), np.c_[np.full(len(f), 3), f].ravel())


class ShopScene:
    """The shop in a PVScene. Static equipment is merged by colour per station; moving pieces are groups."""

    def __init__(self, size=(CM.W, CM.H), context=True):
        self.pl = CM.plotter(size)
        if os.environ.get("SHOP_AA", "fxaa") == "fxaa":   # the shared look's SSAA costs 2.3x the render time; on the
            try:                                           # shared runner the shop's ~5000 frames use FXAA instead
                self.pl.disable_anti_aliasing()
                self.pl.enable_anti_aliasing("fxaa")
            except Exception:  # noqa: BLE001
                pass
        self.sc = pvscene.PVScene(self.pl)
        self.sc.add("floor", pv.Plane(center=(8000, 6000, -1), i_size=30000, j_size=20000), CM.FLOOR, specular=0.0)
        self.stations = {}
        self.arms = {}
        self.objs = {}
        self.person = None
        if context:
            self.add_context()

    # ------------------------------------------------------------------------------------------- equipment
    def add_parts(self, key, parts, M, moving=(), alpha_names=()):
        """Static parts merged by colour into one actor each; parts named in `moving` (or with a group) get their own
        group `key/name` (world matrix = M @ part.M, updated by move())."""
        by_col = {}
        for n, p in parts.items():
            if n in moving or (p.group and p.group not in ("",)):
                g = f"{key}/{n}"
                self.sc.add(g, p.mesh, p.color, group=g, opacity=p.opacity)
                self.sc.gmat[g] = M @ p.M
                continue
            if p.opacity < 1.0 or n in alpha_names:
                g = f"{key}/{n}"
                self.sc.add(g, p.mesh.transform(M @ p.M, inplace=False), p.color, group=f"{key}/static", opacity=p.opacity)
                continue
            by_col.setdefault(p.color, []).append(p.mesh.transform(M @ p.M, inplace=False))
        for i, (c, ms) in enumerate(by_col.items()):
            self.sc.add(f"{key}/static {i}", E.merge(ms), c, group=f"{key}/static")
        self.sc.gmat.setdefault(f"{key}/static", np.eye(4))
        self.stations[key] = dict(parts=parts, M=M)

    def move(self, key, name, M_local):
        """Pose a moving part: its station matrix @ M_local (M_local replaces the part's own M)."""
        st = self.stations[key]
        self.sc.gmat[f"{key}/{name}"] = st["M"] @ M_local

    def add_context(self):
        """The rest of the shop, static and lightly detailed, so every shot sits in a room."""
        self.add_parts("lathe_ctx", E.st10(door=0.0)[0], Mst("lathe"))
        self.add_parts("saw_ctx", E.s20a(head=1.0)[0], Mst("saw"))
        self.add_parts("wash_ctx", E.wash_deburr()[0], Mst("wash"))
        self.add_parts("measure_ctx", E.granite_station()[0], Mst("measure"))
        self.add_parts("tools_ctx", E.tool_stand()[0], Mst("tools"))
        self.add_parts("rack_ctx", E.cantilever_rack()[0], Mst("stock"))
        self.add_parts("tig_ctx", E.tig_station()[0], Mst("tig"))
        bench = E.bench(1830.0, 760.0, 900.0)
        self.add_parts("bench_ctx", bench, Mst("bench"))

    def drop_context(self, key):
        """Hide a context station (when the shot's own, detailed copy stands there)."""
        for n, g in list(self.sc.group_of.items()):
            if n.startswith(f"{key}_ctx/"):
                self.sc.alpha[n] = 0.0

    # ------------------------------------------------------------------------------------------- robots
    def add_arm(self, key, tool="2F-85"):
        sc = self.sc
        for link, lst in ur_arm.arm_meshes(MODEL).items():
            for i, (m, c, s) in enumerate(lst):
                sc.add(f"arm{key}/{link}/{i}", m, c, group=f"arm{key}/{link}", specular=s)
        for part, lst in ur_arm.gripper_meshes().items():
            for i, (m, c, s) in enumerate(lst):
                sc.add(f"arm{key}/gr/{part}/{i}", m, c, group=f"arm{key}/gr/{part}", specular=s)
        for i, (m, c, s) in enumerate(ur_arm.camera_meshes()):
            sc.add(f"arm{key}/cam/{i}", m, c, group=f"arm{key}/cam", specular=s)
        # the other tools on the QC-11 plate, shown when in use (tool0 frame)
        plate = E.cyl((0, 0, 0), (0, 0, 22), 32.0)
        sc.add(f"arm{key}/qc", plate, "#9aa3ab", group=f"arm{key}/qc")
        p3, _ = E.gripper_3fg15(120.0)
        sc.add(f"arm{key}/3fg/body", E.cyl((0, 0, 24), (0, 0, 97), 78.0, res=40), "#3c4650", group=f"arm{key}/3fg")
        for k in range(3):
            sc.add(f"arm{key}/3fg/f{k}", E.box(-9, 9, -10, 10, 97, 187), "#9aa3ab", group=f"arm{key}/3fg/f{k}")
            sc.add(f"arm{key}/3fg/f{k}x", E.box(-9, 9, -10, 10, 187, 227), "#d9b23a", group=f"arm{key}/3fg/f{k}")
        sc.add(f"arm{key}/vgp/body", E.box(-92, 92, -132, 132, 24, 116), "#33373b", group=f"arm{key}/vgp")
        sc.add(f"arm{key}/vgp/cups", E.merge([E.cyl((x, y, 116), (x, y, 136), 18.0, res=20)
                                             for x, y in ((-50, -60), (-50, 60), (50, -60), (50, 60))]), "#1f2326",
               group=f"arm{key}/vgp")
        # round 9 (lesson 7, "a held part must be held by something drawn"): the tools the 2F-85 holds by a 20 mm fin,
        # drawn in the TCP frame (z along the approach) as shop_clips plans them: the nut runner (NUT_RUNNER: body r 22
        # from 20 to 160 mm, a 1/4 in. hex extension r 8 to 262 mm) and the safety knife's holder (20 x 16 x 80 mm, its
        # blade retracted into the holder's tip). Named under gr/ (they ride on the flange with the gripper).
        fin = E.box(-10.0, 10.0, -20.0, 20.0, -24.0, 22.0)
        sc.add(f"arm{key}/gr/xrunner/0", E.merge([fin, E.cyl((0, 0, 20), (0, 0, 160), 22.0, res=24)]), "#e0a526",
               group=f"arm{key}/gr/xrunner")
        sc.add(f"arm{key}/gr/xrunner/1", E.cyl((0, 0, 160), (0, 0, 262), 8.0, res=12), "#8a9199",
               group=f"arm{key}/gr/xrunner")
        sc.add(f"arm{key}/gr/xknife/0", E.box(-10, 10, -8, 8, -38, 42), "#e63946", group=f"arm{key}/gr/xknife")
        sc.add(f"arm{key}/gr/xknife/1", E.box(-0.6, 0.6, -6, 6, 42, 47), "#c9ced3", group=f"arm{key}/gr/xknife")
        # its MiR250 + cabinet + deck (shop_cell.mir_items, PR 318's sizes)
        self.arms[key] = dict(tool=tool, mir_dx=None)
        self.set_tool(key, tool)

    def set_mir(self, key, M, arm_dx):
        sc = self.sc
        a = self.arms[key]
        if a.get("mir_dx") != arm_dx:
            for n in [n for n in sc.actors if n.startswith(f"mir{key}/")]:
                sc.alpha[n] = 0.0
            for i, (name, (v, f), c) in enumerate(S.mir_items(arm_dx)):
                sc.add(f"mir{key}/{arm_dx:.0f}/{i}", vf_mesh(v, f), c, group=f"mir{key}")
            a["mir_dx"] = arm_dx
            for n in [n for n in sc.actors if n.startswith(f"mir{key}/{arm_dx:.0f}/")]:
                sc.alpha[n] = 1.0
        sc.gmat[f"mir{key}"] = np.asarray(M, float)

    def set_tool(self, key, tool):
        sc = self.sc
        show = dict(gr=tool in ("2F-85", "nut runner", "cutter"), fg=tool in ("3FG15", "3FG15L"), vgp=tool == "VGP20")
        for n in sc.actors:
            if n.startswith(f"arm{key}/gr/xrunner"):
                sc.alpha[n] = 1.0 if tool == "nut runner" else 0.0
            elif n.startswith(f"arm{key}/gr/xknife"):
                sc.alpha[n] = 1.0 if tool == "cutter" else 0.0
            elif n.startswith(f"arm{key}/gr/"):
                sc.alpha[n] = 1.0 if show["gr"] else 0.0
            elif n.startswith(f"arm{key}/3fg"):
                sc.alpha[n] = 1.0 if show["fg"] and (tool == "3FG15L" or not n.endswith("x")) else 0.0
            elif n.startswith(f"arm{key}/vgp"):
                sc.alpha[n] = 1.0 if show["vgp"] else 0.0
            elif n.startswith(f"arm{key}/qc"):
                sc.alpha[n] = 0.0 if show["gr"] else 1.0
        self.arms[key]["tool"] = tool

    def set_arm(self, key, q, close, base, tool=None, visible=True):
        sc = self.sc
        if tool is not None and tool != self.arms[key]["tool"]:
            self.set_tool(key, tool)
        F = ur_arm.fk(MODEL, q)
        base = np.asarray(base, float)
        for link in ur_arm.LINKS:
            sc.gmat[f"arm{key}/{link}"] = base @ F[link]
        W0 = base @ F["tool0"]
        G = ur_arm.gripper_fk(min(max(close, 0.0), 1.0))
        for part in G:
            g = f"arm{key}/gr/{part}"
            if g in sc.gmat or any(n.startswith(g + "/") for n in sc.actors):
                sc.gmat[g] = W0 @ G[part]
        Wt = W0 @ E.T((0.0, 0.0, ur_arm.tcp_mm(min(max(close, 0.0), 1.0))))
        sc.gmat[f"arm{key}/gr/xrunner"] = Wt
        sc.gmat[f"arm{key}/gr/xknife"] = Wt
        sc.gmat[f"arm{key}/cam"] = W0
        sc.gmat[f"arm{key}/qc"] = W0
        sc.gmat[f"arm{key}/3fg"] = W0
        sc.gmat[f"arm{key}/vgp"] = W0
        r = 76.0 - min(max(close, 0.0), 1.0) * 74.0 + 9.0
        for k in range(3):
            a = math.radians(90 + 120 * k)
            sc.gmat[f"arm{key}/3fg/f{k}"] = W0 @ E.T((r * math.cos(a), r * math.sin(a), 0.0), E.Rz(math.degrees(a)))
        if not visible:
            for n in sc.actors:
                if n.startswith((f"arm{key}/", f"mir{key}/")):
                    sc.alpha[n] = 0.0

    # ------------------------------------------------------------------------------------------- objects
    def obj_mesh(self, spec):
        k = spec.get("kind")
        if k == "state":
            return pv.read(str(CHAMBER / f"{spec['part']}_{spec['k']}.vtp")), spec.get("color", "#cfd4d9")
        if k == "file":
            return pv.read(spec["path"]), spec.get("color", "#cfd4d9")
        if k == "box":
            return E.box(*spec["b"]), spec.get("color", "#cfd4d9")
        if k == "boxes":
            return E.merge([E.box(*b) for b in spec["boxes"]]), spec.get("color", "#cfd4d9")
        if k == "cyl":
            return E.cyl((0, 0, 0), (spec["L"], 0, 0), spec["r"], res=40), spec.get("color", "#cfd4d9")
        if k == "steps":                  # a turned part: [(x from, x to, radius)] along its x axis
            return E.merge([E.cyl((a, 0, 0), (b, 0, 0), r, res=40) for a, b, r in spec["steps"]]), \
                spec.get("color", "#cfd4d9")
        if k == "vf":
            return vf_mesh(spec["v"], spec["f"]), spec.get("color", "#cfd4d9")
        if k == "tray":
            L, W, H = spec["L"], spec["W"], spec["H"]
            m = E.merge([E.open_box(-L / 2, L / 2, -W / 2, W / 2, 0, H, 3.0), E.box(-10, 10, -40, 40, H, H + 60)])
            return m, spec.get("color", "#2b6cb0")
        if k == "parts":
            ps = E.wash_deburr()[0] if spec["station"] == "wash" else {}
            return E.merge([ps[n].mesh.transform(ps[n].M, inplace=False) for n in spec["names"]]), "#9aa3ab"
        raise ValueError(spec)

    def set_obj(self, name, M, spec=None, color=None):
        sc = self.sc
        g = f"obj/{name}"
        if name not in self.objs:
            if spec is None:
                return
            m, c = self.obj_mesh(spec)
            sc.add(g, m, color or c, group=g)
            self.objs[name] = spec
        elif spec is not None and spec is not self.objs[name] and _spec_key(spec) != _spec_key(self.objs[name]):
            m, c = self.obj_mesh(spec)
            sc.add(g, m, color or c, group=g)
            self.objs[name] = spec
        sc.parent.pop(g, None)                 # a world pose: not riding on a machine group any more
        sc.gmat[g] = np.asarray(M, float)
        sc.alpha[g] = 1.0

    def hide_obj(self, name):
        if name in self.objs:
            self.sc.alpha[f"obj/{name}"] = 0.0

    # ------------------------------------------------------------------------------------------- person
    def add_person(self, name="op", gloves=None):
        self.person = people.Person(self.sc, name, gloves=gloves)
        return self.person

    def render(self, cam):
        return self.sc.render(cam)
