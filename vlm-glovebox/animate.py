"""Renders and animations of the VLM-tray glovebox (model.py), in byu-vcl #303's Kardex Shuttle XP 500.

Chapters (each a GIF in out/ and an MP4 in out/mp4/, as in byu-vcl vertical-lab):

* ``design``: the box goes together on a bare tray inside Kardex's height limit, then the shell turns see-through
* ``transfer``: tray G comes to the opening; the pallet comes out to the side; the UR10e on its MiR250 loads a jar;
  the antechamber cycles; the gantry weighs and stores the jar, seals an XRD air-sensitive holder and sends it out;
  the arm takes it; tray G goes home
* ``manual``: the occasional job by hand: the VLM holds the tray at the opening, the port covers open, the gloves
  go in, then everything closes again
* ``full``: the three MP4s joined

    xvfb-run -a python animate.py design transfer manual full
    PREVIEW=1 xvfb-run -a python animate.py transfer     # last frame of every sub-step, to /tmp/preview_*.png
    xvfb-run -a python animate.py stills                  # out/*.png
"""
from __future__ import annotations

import hashlib
import math
import os
import pickle
import subprocess
import sys
from pathlib import Path

import numpy as np

import vertical_lab

vertical_lab.ensure()

import cadquery as cq      # noqa: E402
import pyvista as pv       # noqa: E402

import lab as LAB          # noqa: E402  (byu-vcl vertical-lab)
import props as P          # noqa: E402
import scene as SC         # noqa: E402
import vlm as V            # noqa: E402
from scene import R, S, Scene, T  # noqa: E402

import model as M          # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SC.OUT = OUT               # scene.py would write next to itself otherwise
CACHE = HERE / ".cache"
FPS = SC.FPS
TITLE = "Automation glovebox on a VLM tray"
TRAY = "G"
HOME = "F2"                # tray G's storage slot: front column, above the opening
GREEN, AMBER, OFF, BLUE = (0.20, 0.85, 0.35), (0.98, 0.70, 0.10), (0.30, 0.32, 0.30), (0.25, 0.55, 0.95)
FLOOR_C = (0.965, 0.965, 0.96)
GHOST_VLM = {"vlm_skin": 0.16, "vlm_seam": 0.16, "vlm_bay": 0.22, "vlm_shutter": 0.35}
GHOST_GB = {"chamber shell": 0.14, "services cover": 0.16, "antechamber": 0.22, "outer door guide": 0.35,
            "inner door guide": 0.5, "window frame": 0.5}
DOOR_TRAVEL = 290.0
GX_HOME, GY_HOME = -90.0, 0.0
FINGER_OPEN = 76.0

# the mobile manipulator, parked in front of the opening's right half, square to it (byu-vcl animate.py's spacing)
AMR_XY = (760.0, -V.UNIT_D / 2 - V.SKIN - 50.0 - 30.0 - P.MIR["W"] / 2)
ARM_LOCAL = (0.0, 130.0)
CUPS_LOCAL = {"in": (-300.0, -150.0), "out": (300.0, -150.0)}     # two holders on the cabinet top
PARK_DEG = (-90.0, -150.0, 135.0, -75.0, -90.0, 0.0)             # byu-vcl animate.PARK_DEG: folded, facing the VLM


# ===================================================================================================== meshes
def _hash(*files) -> str:
    h = hashlib.sha256()
    for f in files:
        h.update(Path(f).read_bytes())
    return h.hexdigest()[:12]


def _mesh(shape, tol=1.0) -> pv.PolyData:
    if isinstance(shape, cq.Workplane):
        shape = shape.val() if len(shape.vals()) == 1 else cq.Compound.makeCompound(shape.vals())
    return LAB.to_mesh(shape, tol)


def _entry(mesh, mat, group):
    r, g, b, a, spec = M.MATERIALS[mat]
    return dict(mesh=mesh, color=(r, g, b), opacity=a, specular=spec, group=group, material=mat)


def gb_meshes() -> dict:
    """{name: entry} for the glovebox, the samples and the hotel's contents, cached on model.py."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"gb_{_hash(HERE / 'model.py', Path(__file__))}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    print("tessellating the glovebox", flush=True)
    out = {}
    allp = dict(M.parts())
    allp.update(M.frames())
    for name, (shape, mat, group) in allp.items():
        out[name] = _entry(_mesh(shape, 0.5 if group.startswith(("gb_finger", "gb_gz", "gb_sensor")) else 1.0), mat,
                           group)
    # the moving samples, each in its own frame
    for key, parts in (("jar", M.jar("gb_cap_al")), ("holder", M.holder()), ("dome", M.dome())):
        g = key.replace(" ", "_")
        for nm, (shape, mat) in parts.items():
            out[f"{key} {nm}"] = _entry(_mesh(shape, 0.3), mat, g)
    # what already sits in the hotel: jars in column 1 (row 1 is free for the incoming jar), sealed holders in column 2
    by: dict[str, list] = {}
    caps = ("gb_cap_mg", None, "gb_cap_si", "gb_cap_al")
    for row, (y, cap) in enumerate(zip(M.HOTEL_Y, caps)):
        if cap is not None:
            for nm, (shape, mat) in M.jar(cap).items():
                by.setdefault(mat, []).append(_mesh(shape.translate((M.HOTEL_X[0], y, M.HOTEL_TOP - 20)), 0.3))
        if row < 3:
            for src in (M.holder(), M.dome()):
                for nm, (shape, mat) in src.items():
                    z = M.HOTEL_TOP - 6 + (M.HOLDER["h"] if nm == "dome" else 0)
                    by.setdefault(mat, []).append(_mesh(shape.translate((M.HOTEL_X[1], y, z)), 0.3))
    for mat, ms in by.items():
        out[f"hotel items {mat}"] = _entry(pv.merge(ms) if len(ms) > 1 else ms[0], mat, "gb_hotel_items")
    path.write_bytes(pickle.dumps(out))
    return out


def vlm_meshes() -> dict:
    """byu-vcl's VLM with one tray, G, instead of A-C."""
    path = CACHE / f"vlm_{_hash(Path(V.__file__), Path(LAB.__file__))}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    print("tessellating the VLM", flush=True)
    V.TRAYS = {TRAY: dict(capacity_lb=1080, capacity_kg=490, kind="strong")}
    out = LAB._vlm_entries()
    path.write_bytes(pickle.dumps(out))
    return out


# ===================================================================================================== state
STAGE_OF = {   # functional group -> assembly stage
    "gb_skid": "skid", "gb_chamber": "chamber", "gb_window": "chamber", "gb_cover_L": "chamber",
    "gb_cover_R": "chamber", "gb_sensor_L": "chamber", "gb_sensor_R": "chamber", "gb_door_in": "chamber",
    "gb_glove_L": "chamber", "gb_glove_R": "chamber", "gb_gx": "gantry", "gb_stations": "stations",
    "gb_hotel_items": "stations", "holder": "stations", "dome": "stations", "gb_ante": "ante", "gb_door_out": "ante",
    "gb_lock_lamp": "ante", "gb_pallet": "ante", "gb_services": "services", "gb_services_in": "services",
    "gb_dock": "dock",
}
STAGES = ("skid", "chamber", "gantry", "stations", "ante", "services", "dock")


def reparent(sc, group, new_parent):
    W = sc.world(group)
    if new_parent is None:
        sc.parent.pop(group, None)
        sc.gmat[group] = W
    else:
        sc.parent[group] = new_parent
        Wp = sc.world(new_parent)
        sc.gmat[group] = np.linalg.inv(Wp) @ W


class Box:
    """The glovebox in a scene: its moving groups and the state behind them."""

    def __init__(self, sc: Scene, data: dict, parent: str):
        self.sc = sc
        self.door_in = self.door_out = 0.0
        self.x_pal = M.X_LOCK
        self.gxyz = [GX_HOME, GY_HOME, M.PAD_UP]
        self.fingers = FINGER_OPEN
        self.cover = {"L": 0.0, "R": 0.0}
        self.glove = {s: [0.22, 0.0, 0.0] for s in "LR"}      # extension, yaw, droop
        self.ghost_f = 0.0
        self.lamp = GREEN
        self.status: dict[str, str] = {}
        self.ghost = {}
        for st in STAGES:
            sc.parent[f"st_{st}"] = parent
            sc.gmat[f"st_{st}"] = np.eye(4)
        for name, e in data.items():
            kw = {}
            if e["material"] in ("gb_led",):
                kw = dict(ambient=0.9, diffuse=0.2)
            if name in GHOST_GB:
                self.ghost[name] = GHOST_GB[name]
            sc.add(name, e["mesh"], e["color"], e["group"], opacity=e["opacity"], specular=e["specular"], **kw)
        for g, st in STAGE_OF.items():
            sc.parent[g] = f"st_{st}"
        for g, p in (("gb_gy", "gb_gx"), ("gb_gz1", "gb_gy"), ("gb_gz", "gb_gy"), ("gb_finger_L", "gb_gz"),
                     ("gb_finger_R", "gb_gz")):
            sc.parent[g] = p
        # the samples' starting places: the holder in the dome station's nest, the dome on its post
        sc.gmat["holder"] = T((M.STN["x"], M.STN["y"], M.STN_TOP - 7))
        sc.parent["dome"] = "st_stations"
        sc.gmat["dome"] = T((M.DOME_POST[0], M.DOME_POST[1], M.DOME_POST_TOP - (M.HOLDER["dome_r"] - 1.5)))
        self.apply()

    # ------------------------------------------------------------------------------------------------ apply
    def apply(self):
        sc = self.sc
        sc.gmat["gb_door_in"] = T((0, self.door_in * DOOR_TRAVEL, 0))
        sc.gmat["gb_door_out"] = T((0, self.door_out * DOOR_TRAVEL, 0))
        sc.gmat["gb_pallet"] = T((self.x_pal, M.PAL["y"], M.PAL_Z))
        gx, gy, pad = self.gxyz
        sc.gmat["gb_gx"] = T((gx, 0, 0))
        sc.gmat["gb_gy"] = T((0, gy, 0))
        sc.gmat["gb_gz1"] = T((0, 0, -(M.PAD_UP - pad) / 2))
        sc.gmat["gb_gz"] = T((0, 0, pad))
        sc.gmat["gb_finger_L"] = T((-(self.fingers / 2 + 7), 0, 0))
        sc.gmat["gb_finger_R"] = T((self.fingers / 2 + 7, 0, 0))
        for side, x in zip("LR", M.PORT_X):
            sx = -1 if side == "L" else 1
            hx, hy = x + sx * (M.COVER_R + 6), M.CH["y0"] - M.RING_OUT - 9
            sc.gmat[f"gb_cover_{side}"] = R((0, 0, 1), sx * 180.0 * self.cover[side], (hx, hy, 0))
            ext, yaw, droop = self.glove[side]
            sc.gmat[f"gb_glove_{side}"] = (T((x, M.CH["y0"] + 8, M.PORT_Z)) @ R((0, 0, 1), yaw) @
                                           R((1, 0, 0), -droop) @ S((1, ext, 1)))
            on = self.cover[side] < 0.02
            sc.color[f"port sensor {side}"] = GREEN if on else AMBER
            sc.ambient[f"port sensor {side}"] = 0.9
        sc.color["lock lamp"] = self.lamp
        sc.ambient["lock lamp"] = 0.9
        for n, gh in self.ghost.items():
            sc.base_alpha[n] = 1.0 + (gh - 1.0) * self.ghost_f
        sc.gauges = list(self.status.items())

    # ------------------------------------------------------------------------------------------------ moves
    def _lerp(self, attr, v1):
        v0 = getattr(self, attr)

        def up(u):
            setattr(self, attr, v0 + (v1 - v0) * u)
            self.apply()
        return up

    def door(self, which, f1):
        return self._lerp("door_in" if which == "in" else "door_out", f1)

    def pallet_to(self, x1):
        return self._lerp("x_pal", x1)

    def ghost_to(self, f1):
        return self._lerp("ghost_f", f1)

    def grip(self, w1):
        return self._lerp("fingers", w1)

    def g_to(self, x=None, y=None, pad=None):
        x0, y0, p0 = self.gxyz
        x1, y1, p1 = (x0 if x is None else x), (y0 if y is None else y), (p0 if pad is None else pad)

        def up(u):
            self.gxyz = [x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, p0 + (p1 - p0) * u]
            self.apply()
        return up

    def covers(self, f1):
        c0 = dict(self.cover)

        def up(u):
            for s in "LR":
                self.cover[s] = c0[s] + (f1 - c0[s]) * u
            self.apply()
        return up

    def gloves_to(self, ext=None, yaw=(None, None), droop=(None, None)):
        g0 = {s: list(v) for s, v in self.glove.items()}

        def up(u):
            for i, s in enumerate("LR"):
                e1 = g0[s][0] if ext is None else ext
                y1 = g0[s][1] if yaw[i] is None else yaw[i]
                d1 = g0[s][2] if droop[i] is None else droop[i]
                self.glove[s] = [g0[s][0] + (e1 - g0[s][0]) * u, g0[s][1] + (y1 - g0[s][1]) * u,
                                 g0[s][2] + (d1 - g0[s][2]) * u]
            self.apply()
        return up

    # ------------------------------------------------------------------------------------------------ gantry jobs
    def g_pick(self, sc, step, cap, item, xyz_grip, width, cam=None, labels=(), sec=1.0):
        x, y, z = xyz_grip
        sc.step(step, cap, sec, both(self.g_to(x=x, y=y, pad=M.PAD_UP), self.grip(width + 24)), hold=0.05,
                cam_to=cam, labels=labels)
        sc.step(step, cap, 0.7, self.g_to(pad=z), hold=0.05)
        sc.step(step, cap, 0.35, self.grip(width), hold=0.05)
        reparent(sc, item, "gb_gz")
        sc.step(step, cap, 0.7, self.g_to(pad=M.PAD_UP), hold=0.05)

    def g_place(self, sc, step, cap, item, xyz_grip, new_parent, cam=None, labels=(), sec=1.0, settle=None):
        x, y, z = xyz_grip
        sc.step(step, cap, sec, self.g_to(x=x, y=y), hold=0.05, cam_to=cam, labels=labels)
        sc.step(step, cap, 0.7, self.g_to(pad=z), hold=0.05)
        sc.step(step, cap, 0.35, self.grip(self.fingers + 24), hold=0.05)
        reparent(sc, item, new_parent)
        if settle is not None:
            settle()
        sc.step(step, cap, 0.7, self.g_to(pad=M.PAD_UP), hold=0.05)


def both(*fs):
    def up(u):
        for f in fs:
            if f is not None:
                f(u)
    return up


# ===================================================================================================== sample geometry
JAR_GRIP = M.JAR["h"] - M.JAR["cap_h"] / 2           # grip height on the cap, above the jar's base
JAR_W = 2 * (M.JAR["r"] + 1.5)
HOLDER_GRIP = M.HOLDER["h"] / 2 + 2
HOLDER_W = 2 * M.HOLDER["r"]
DOME_GRIP = 9.0                                       # above the dome's rim
DOME_W = 2 * math.sqrt(M.HOLDER["dome_r"] ** 2 - DOME_GRIP ** 2)
NEST_Z = M.PAL["t"] - 5                               # a sample's base in a pallet nest, pallet frame
HOTEL_FREE = (M.HOTEL_X[0], M.HOTEL_Y[1], M.HOTEL_TOP - 20)


def nest(i, x_pal=None):
    """Base centre of pallet nest i in the tray frame."""
    x = M.X_IN if x_pal is None else x_pal
    return (x + M.NEST[i], M.PAL["y"], M.PAL_Z + NEST_Z)


# ===================================================================================================== chapter: design
def tray_only(vlm_data) -> dict:
    return {n: e for n, e in vlm_data.items() if e["group"] == f"tray_{TRAY}"}


ORB0 = dict(a=36.5, r=4300.0, h=2050.0, f=(0.0, 30.0, 300.0))
CAM_D0 = [(ORB0["f"][0] + ORB0["r"] * math.sin(math.radians(ORB0["a"])),
           ORB0["f"][1] - ORB0["r"] * math.cos(math.radians(ORB0["a"])), ORB0["h"]), ORB0["f"], (0, 0, 1)]


def orbit(sc, o0, o1):
    """Camera on a circle about a vertical axis through the focal point; angle, radius, height and focal blend."""
    def up(u):
        a = math.radians(o0["a"] + (o1["a"] - o0["a"]) * u)
        r = o0["r"] + (o1["r"] - o0["r"]) * u
        h = o0["h"] + (o1["h"] - o0["h"]) * u
        f = tuple(x + (y - x) * u for x, y in zip(o0["f"], o1["f"]))
        sc.cam = [(f[0] + r * math.sin(a), f[1] - r * math.cos(a), h), f, (0, 0, 1)]
    return up


ORB1 = dict(ORB0, a=-30.0)
ORB2 = dict(a=24.0, r=3300.0, h=1750.0, f=(60.0, 0.0, 330.0))


def design(data):
    sc = Scene("glovebox_design", TITLE)
    sc.cam = list(CAM_D0)
    floor = pv.Plane(center=(0, 0, -1), direction=(0, 0, 1), i_size=9000, j_size=9000)
    sc.add("floor", floor, FLOOR_C, "floor", ambient=1.0, diffuse=0.0, specular=0.0, smooth_shading=False)
    for name, e in tray_only(data["vlm"]).items():
        sc.add(name, e["mesh"], e["color"], e["group"], opacity=e["opacity"])
    sc.gmat[f"tray_{TRAY}"] = np.eye(4)
    sc.color[f"tray {TRAY} lamp"] = GREEN
    # Kardex's envelope: the tray inside its rim, 727.5 mm of product height
    env = pv.Box(bounds=(-M.TRAY_W / 2 + 12, M.TRAY_W / 2 - 12, -M.TRAY_D / 2, M.TRAY_D / 2 - 12, M.T_FLOOR,
                         M.T_FLOOR + M.MAX_GOODS_H))
    sc.add("envelope", env, (0.85, 0.25, 0.20), "envelope", opacity=0.10, specular=0.0, shown=False)
    sc.add("envelope edges", env.extract_feature_edges().tube(radius=4), (0.85, 0.25, 0.20), "envelope", shown=False)
    gb = Box(sc, data["gb"], f"tray_{TRAY}")
    sc.parent["jar"] = "st_stations"
    sc.gmat["jar"] = T(HOTEL_FREE)
    drop = {st: 900.0 for st in STAGES}

    def stage_in(st):
        def up(u):
            sc.gmat[f"st_{st}"] = T((0, 0, drop[st] * (1 - u)))
            for n, g in sc.group_of.items():
                if _stage_of(sc, g) == st:
                    sc.alpha[n] = min(1.0, u * 2.5)
        return up

    for st in STAGES:
        sc.gmat[f"st_{st}"] = T((0, 0, drop[st]))
        for n, g in sc.group_of.items():
            if _stage_of(sc, g) == st:
                sc.alpha[n] = 0.0
    gb.status = {}
    n = 10
    W = lambda x, y, z: (x, y, z)    # noqa: E731  (tray frame = world here)
    sc.step(f"1/{n}", "The VLM's tray: 2450 x 864 mm, and Kardex lets 727.5 mm of goods through the opening. A stock "
            "glovebox is 1.8 to 2 m tall, so this one is drawn to the tray (red box: the envelope).", 2.0,
            lambda u: sc.show(["envelope", "envelope edges"], u), hold=1.2, still=False,
            labels=[("Kardex Shuttle XP 500 tray\n2450 x 864 mm", W(900, -432, 40), (0.70, 0.86)),
                    ("727.5 mm product height\nthrough the opening", W(-1213, -432, 730), (0.07, 0.25))])
    sc.step(f"2/{n}", "A low skid on anti-vibration pads, bolted to the tray: the VLM accelerates the tray, and the "
            "box is lifted on and off as one piece.", 1.6, stage_in("skid"), hold=0.6)
    sc.step(f"3/{n}", "The chamber: 1352 x 732 x 667 mm inside (660 L), 2 mm 304 stainless. A full-width window and two "
            "8 in glove ports, capped by hinged covers while the box runs on its own.", 2.0, stage_in("chamber"),
            hold=1.6, labels=[("glove ports, capped\n(cover sensors interlock the VLM)", W(160, -425, 490),
                               (0.62, 0.18)),
                              ("polycarbonate window", W(-600, -400, 600), (0.08, 0.22))])
    sc.step(f"4/{n}", "Inside, a ceiling-hung XYZ gantry with a two-finger gripper. Its z axis telescopes, so 300 mm of "
            "stroke fits under a 715 mm roof.", 1.8, stage_in("gantry"), hold=1.4,
            labels=[("XYZ gantry, telescopic z", W(-90, 0, 600), (0.25, 0.14))])
    sc.step(f"5/{n}", "On the deck: a sample hotel, an automation weigh module under a draft ring, and a station that "
            "seals XRD air-sensitive holders with their domes.", 1.8, stage_in("stations"), hold=1.6,
            labels=[("sample hotel", W(-650, 90, 120), (0.08, 0.30)),
                    ("weigh module", W(-330, 170, 170), (0.30, 0.15)),
                    ("dome station", W(-60, 110, 110), (0.55, 0.12))])
    sc.step(f"6/{n}", "The antechamber (17.6 L), with sliding gates at both ends and a pallet on rails through it. The "
            "pallet comes out to the side, onto a landing inside the tray's footprint. A dry pump sits underneath.",
            2.0, stage_in("ante"), hold=1.6,
            labels=[("antechamber, 17.6 L", W(760, -210, 500), (0.72, 0.16)),
                    ("landing: the arm loads here", W(1085, -210, 310), (0.80, 0.42)),
                    ("dry scroll pump", W(760, -220, 150), (0.86, 0.62))])
    sc.step(f"7/{n}", "The services bay: a dual-column purifier and blower, O2 and H2O analysers, the PLC and an HMI "
            "with an e-stop. The box regenerates one column while it runs on the other.", 1.8, stage_in("services"),
            hold=1.4, labels=[("services bay: purifier, blower,\nanalysers, PLC, HMI", W(-990, -392, 520),
                               (0.06, 0.30))])
    sc.step(f"8/{n}", "A gas dock on the tray's back rim, beside its power socket: argon in and exhaust out, through "
            "dry-break couplings that would meet the slot and the opening as the power does (to ask Kardex).", 1.6,
            stage_in("dock"), hold=1.6, labels=[("gas dock", W(890, 412, 140), (0.82, 0.20))])
    sc.step(f"9/{n}", "715 mm tall, 12.5 mm under Kardex's limit; 2400 x 844 mm, inside the tray's rim. About 340 kg "
            "(model.py's estimate): a strong tray (490 kg), not a medium one (360 kg).", 3.0,
            orbit(sc, ORB0, ORB1), hold=1.4)
    sc.step(f"10/{n}", "See-through: the gantry, the stations, the pallet in the lock and the purifier columns.", 2.6,
            both(gb.ghost_to(1.0), lambda u: sc.show(["envelope", "envelope edges"], 1 - u), orbit(sc, ORB1, ORB2)),
            hold=0.4, still=True)
    # a quick demo: the outer gate opens and the pallet comes out to the side and back
    cap = "The pallet comes out to the side when the outer gate opens. Nothing crosses the tray's front edge."
    sc.step(f"10/{n}", cap, 0.8, gb.door("out", 1.0), hold=0.1)
    sc.step(f"10/{n}", cap, 1.4, gb.pallet_to(M.X_OUT), hold=0.8)
    sc.step(f"10/{n}", cap, 1.4, gb.pallet_to(M.X_LOCK), hold=0.1)
    sc.step(f"10/{n}", cap, 0.8, gb.door("out", 0.0), hold=1.0)
    sc.save()


def _stage_of(sc, g):
    while g in sc.parent:
        if g.startswith("st_"):
            return g[3:]
        g = sc.parent[g]
    return g[3:] if g.startswith("st_") else None


# ===================================================================================================== chapter: in the VLM
class Lab:
    """The VLM around the glovebox: tray G's place, the extractor, the shutter, the arm."""

    def __init__(self, sc: Scene, data: dict, at_open=False):
        self.sc = sc
        self.where = "open" if at_open else HOME
        self.tray = list(V.SLOTS[self.where])
        self.lift_z = V.SLOTS["open"][1]
        self.shutter = 0.0
        self.skin_f = 0.0
        floor = pv.Plane(center=(0, -600, -1), direction=(0, 0, 1), i_size=16000, j_size=14000)
        sc.add("floor", floor, FLOOR_C, "floor", ambient=1.0, diffuse=0.0, specular=0.0, smooth_shading=False)
        shadow = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=V.UNIT_W + 900, j_size=V.UNIT_D + 900)
        sc.add("floor shadow", shadow, (0.90, 0.90, 0.895), "floor", ambient=1.0, diffuse=0.0, specular=0.0,
               smooth_shading=False)
        self.ghost = {}
        for name, e in data["vlm"].items():
            kw = {}
            if e["material"] in GHOST_VLM:
                self.ghost[name] = GHOST_VLM[e["material"]]
            if e["material"] in ("vlm_skin", "vlm_bay"):
                kw = dict(specular=0.05, ambient=0.35)
            if e["material"] == "vlm_led":
                kw = dict(ambient=0.9, diffuse=0.2)
            sc.add(name, e["mesh"], e["color"], e["group"], opacity=e["opacity"], **kw)
        self.gb = Box(sc, data["gb"], f"tray_{TRAY}")
        self._amr()
        self.apply()

    def _amr(self):
        import robot as RB
        sc = self.sc
        for name, (mesh, col) in P.mir250().items():
            kw = dict(ambient=0.8) if "light" in name else {}
            sc.add(f"amr/{name}", mesh, col, "amr", **kw)
        holder, seat = P.buffer_holder()
        self.cup = {}
        for k, (x, y) in CUPS_LOCAL.items():
            sc.add(f"amr/cup {k}", holder.translate((x, y, P.AMR_TOP - 20), inplace=False), P.RACK_C, "amr")
            # the jar stands in its cup; the sealed holder stands on top of the other one
            self.cup[k] = (x, y, P.AMR_TOP - 20 + (seat[2] if k == "in" else P.HOLDER_H + 36.0))
        sc.gmat["amr"] = T((*AMR_XY, 0))
        self.robot = RB.Robot(sc, "ur10e", "amr", T((*ARM_LOCAL, P.AMR_TOP)), q0=PARK_DEG)
        self.q_park = np.radians(PARK_DEG)
        # the jar the arm brings, in its cup on the cabinet
        sc.parent["jar"] = "amr"
        sc.gmat["jar"] = T(self.cup["in"])

    # --------------------------------------------------------------------------------------------- state
    def apply(self):
        sc = self.sc
        y, z = self.tray
        sc.gmat[f"tray_{TRAY}"] = T((0, y, z))
        on = self.where is not None
        sc.color[f"tray {TRAY} lamp"] = GREEN if on else OFF
        sc.ambient[f"tray {TRAY} lamp"] = 0.9 if on else 0.2
        sc.gmat["lift"] = T((0, 0, self.lift_z))
        Lb = max(1.0, V.Z_TOP_IN + 140 - (self.lift_z + 40))
        sc.gmat["belts"] = T((0, 0, self.lift_z + 40)) @ S((1, 1, Lb))
        sc.gmat["shutter"] = T((0, 0, self.shutter * (V.Z_OPEN_TOP - V.Z_SILL + 10)))
        for n, gh in self.ghost.items():
            sc.base_alpha[n] = 1.0 + (gh - 1.0) * self.skin_f
        if self.robot.held is not None:
            self.robot.set()
        st = "at the opening, powered" if self.where == "open" else (
            f"stored ({self.where}), powered" if self.where else "moving, unpowered")
        self.gb.status["Tray G"] = st
        self.gb.apply()

    def _lerp(self, attr, v1, idx=None, carry=False):
        v0 = getattr(self, attr) if idx is None else getattr(self, attr)[idx]

        def up(u):
            v = v0 + (v1 - v0) * u
            if idx is None:
                setattr(self, attr, v)
            else:
                getattr(self, attr)[idx] = v
            if carry:
                self.tray[1] = self.lift_z
            self.apply()
        return up

    def skin(self, f1):
        return self._lerp("skin_f", f1)

    def fetch(self, label, cap, cam=None):
        sc = self.sc
        ys, zs = V.SLOTS[self.where]
        yt, zt = V.SLOTS["open"]
        sc.step(label, cap, max(0.6, abs(self.lift_z - zs) / 1333), self._lerp("lift_z", zs), hold=0.1, cam_to=cam)
        self.where = None
        self.apply()
        sc.step(label, cap, 2.0, self._lerp("tray", 0.0, idx=0), hold=0.1)
        sc.step(label, cap, max(0.6, abs(zs - zt) / 1333), self._lerp("lift_z", zt, carry=True), hold=0.1)
        sc.step(label, cap, 0.6, self._lerp("shutter", 1.0), hold=0.0)
        sc.step(label, cap, 2.0, self._lerp("tray", yt, idx=0), hold=0.0)
        sc.step(label, cap, 0.6, self._lerp("shutter", 0.0), hold=0.0)
        self.where = "open"
        self.apply()

    def store(self, label, cap, cam=None):
        sc = self.sc
        ys, zs = V.SLOTS[HOME]
        self.where = None
        self.apply()
        sc.step(label, cap, 0.6, self._lerp("shutter", 1.0), hold=0.0, cam_to=cam)
        sc.step(label, cap, 2.0, self._lerp("tray", 0.0, idx=0), hold=0.0)
        sc.step(label, cap, 0.6, self._lerp("shutter", 0.0), hold=0.1)
        sc.step(label, cap, max(0.6, abs(self.lift_z - zs) / 1333), self._lerp("lift_z", zs, carry=True), hold=0.1)
        sc.step(label, cap, 2.0, self._lerp("tray", ys, idx=0), hold=0.0)
        self.where = HOME
        self.apply()


def tw(xyz) -> np.ndarray:
    """A tray-frame point, tray G at the opening, in world coordinates."""
    return np.array([xyz[0], V.Y_OPEN + xyz[1], V.Z_OPEN + xyz[2]])


def amr_w(xyz) -> np.ndarray:
    return np.array([AMR_XY[0] + xyz[0], AMR_XY[1] + xyz[1], xyz[2]])


def down(p, spin=0.0):
    return P.tcp_frame(np.asarray(p, float), (0, 0, -1), spin)


def lifted(M4, dz):
    out = M4.copy()
    out[2, 3] += dz
    return out


def closure_for(width):
    """2F-85 closure (0 open .. 1 closed) that brings the pads `width` mm apart (byu-vcl ur_arm's pad geometry)."""
    import ur_arm

    def gap(c):
        G = ur_arm.gripper_fk(c)
        a = G["left_finger_tip"] @ np.array([-25.26, 0, 31.9, 1.0])
        b = G["right_finger_tip"] @ np.array([25.26, 0, 31.9, 1.0])
        return abs(a[0] - b[0])
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gap(mid) > width else (lo, mid)
    return (lo + hi) / 2


def line(rb, M4):
    try:
        return rb.line_to(M4)
    except ValueError as e:          # the line would flip the arm: a joint move instead (reported)
        print("  line move ->", e, "; joint move instead", flush=True)
        return rb.joint_to(Tw=M4)


def arm_pick(L, step, cap, group, M_grasp, close, cam=None, labels=(), up=160.0, sec=1.8):
    rb, sc = L.robot, L.sc
    M_pre = lifted(M_grasp, up)
    sc.step(step, cap, sec, both(rb.joint_to(Tw=M_pre), rb.grip_to(0.0)), hold=0.05, cam_to=cam, labels=labels)
    sc.step(step, cap, 0.9, line(rb, M_grasp), hold=0.05)
    sc.step(step, cap, 0.45, rb.grip_to(close), hold=0.05)
    rb.grasp(group)
    sc.step(step, cap, 0.9, line(rb, M_pre), hold=0.05)


def arm_place(L, step, cap, M_place, new_parent, cam=None, labels=(), up=160.0, sec=1.8):
    rb, sc = L.robot, L.sc
    M_pre = lifted(M_place, up)
    sc.step(step, cap, sec, rb.joint_to(Tw=M_pre), hold=0.05, cam_to=cam, labels=labels)
    sc.step(step, cap, 0.9, line(rb, M_place), hold=0.05)
    sc.step(step, cap, 0.45, rb.grip_to(0.0), hold=0.05)
    rb.release(new_parent)
    sc.step(step, cap, 0.9, line(rb, M_pre), hold=0.05)


CAM_WIDE = [(7570, -6720, 4790), (0, -250, 1800), (0, 0, 1)]
# high and nearly square to the opening: over the parked arm, under the header, clear of the OPTIC panel
CAM_OPEN = [(600, -5600, 2900), (150, -1300, 1250), (0, 0, 1)]
CAM_ARM = [(950, -3800, 2950), (800, -1300, 1150), (0, 0, 1)]
CAM_LOCK = [(1150, -3400, 2500), (700, -1250, 1200), (0, 0, 1)]
CAM_IN = [(-250, -3050, 2900), (-60, -1080, 1020), (0, 0, 1)]
CAM_MANUAL = [(-1500, -4300, 1900), (-150, -1300, 1180), (0, 0, 1)]


def transfer(data):
    sc = Scene("glovebox_transfer", TITLE)
    sc.cam = list(CAM_WIDE)
    L = Lab(sc, data)
    gb = L.gb
    gb.status.update({"Box": "Ar, O2 < 1 ppm, H2O < 1 ppm", "Lock": "argon, idle", "Pallet": "in the lock"})
    L.apply()
    n = 12
    w_jar = closure_for(JAR_W)
    w_hold = closure_for(HOLDER_W)

    sc.step(f"1/{n}", "The glovebox lives on tray G, in slot F2 of the Shuttle XP 500. In its slot it has power, so the "
            "purifier keeps the argon under 1 ppm of O2 and H2O.", 1.2, None, hold=1.6)
    sc.step(f"1/{n}", "The glovebox lives on tray G, in slot F2 of the Shuttle XP 500. In its slot it has power, so the "
            "purifier keeps the argon under 1 ppm of O2 and H2O.", 1.2, L.skin(1.0), hold=0.6)
    cap = ("A transfer is requested. The extractor brings tray G to the opening. There is no power in transit, so the "
           "box rides sealed, valves shut, a few mbar over ambient.")
    L.fetch(f"2/{n}", cap, cam=CAM_OPEN)
    gb.status["Pallet"] = "in the lock"
    sc.step(f"2/{n}", "At the opening, power and the gas dock reconnect. The PLC checks O2, H2O, pressure, and that both "
            "port covers are on, before it opens anything.", 1.4, None, hold=1.0,
            labels=[("tray G at the opening", tw((-500, -432, 720)), (0.20, 0.20)),
                     ("UR10e on a MiR250", amr_w((0, 130, 1300)), (0.80, 0.22))])
    cap = "The outer gate slides open and the pallet runs out to the side, onto the landing inside the tray's footprint."
    sc.step(f"3/{n}", cap, 0.8, both(gb.door("out", 1.0), lambda u: gb.status.update(Lock="outer gate open")),
            hold=0.1, cam_to=CAM_ARM)
    gb.status["Pallet"] = "out on the landing"
    sc.step(f"3/{n}", cap, 1.6, gb.pallet_to(M.X_OUT), hold=0.4)
    cap = ("The UR10e brings a capped jar of Al powder (from the multi-doser or the atomizer) and sets it in the pallet's "
           "front nest. The landing's light grid tells the PLC when the arm is clear.")
    jar_cup = amr_w(L.cup["in"])
    arm_pick(L, f"4/{n}", cap, "jar", down(jar_cup + (0, 0, JAR_GRIP)), w_jar)
    pal_out = tw(nest(0, M.X_OUT))
    arm_place(L, f"4/{n}", cap, down(pal_out + (0, 0, JAR_GRIP)), "gb_pallet")
    sc.step(f"4/{n}", cap, 1.6, L.robot.joint_to(q1=L.q_park), hold=0.2)
    cap = "The pallet runs back into the lock and the outer gate shuts on its seal."
    gb.status["Pallet"] = "in the lock"
    sc.step(f"5/{n}", cap, 1.6, gb.pallet_to(M.X_LOCK), hold=0.1, cam_to=CAM_LOCK)
    sc.step(f"5/{n}", cap, 0.8, gb.door("out", 0.0), hold=0.3)
    cap = ("Three evacuate and argon-refill cycles, about 2 min each with a 6 m3/h dry pump. Shown sped up. Air never "
           "reaches the chamber.")
    gb.lamp = AMBER
    for i in range(3):
        gb.status["Lock"] = f"cycle {i + 1}/3: evacuating, 0.1 mbar"
        sc.step(f"6/{n}", cap, 0.9, gb.ghost_to(min(1.0, 0.35 * (i + 1))), hold=0.1)
        gb.status["Lock"] = f"cycle {i + 1}/3: argon refill, 1013 mbar"
        sc.step(f"6/{n}", cap, 0.9, None, hold=0.1)
    gb.lamp = GREEN
    gb.status["Lock"] = "argon, ready"
    sc.step(f"6/{n}", cap, 0.6, gb.ghost_to(1.0), hold=0.4)
    cap = "The inner gate opens and the pallet runs into the chamber, under the gantry."
    sc.step(f"7/{n}", cap, 0.8, gb.door("in", 1.0), hold=0.1, cam_to=CAM_IN)
    gb.status["Pallet"] = "in the chamber"
    sc.step(f"7/{n}", cap, 1.6, gb.pallet_to(M.X_IN), hold=0.3)
    cap = "The gantry weighs the jar under the draft ring (the blower pauses while it weighs) ..."
    jar_in = nest(0)
    gb.g_pick(sc, f"8/{n}", cap, "jar", (jar_in[0], jar_in[1], jar_in[2] + JAR_GRIP), JAR_W)
    gb.g_place(sc, f"8/{n}", cap, "jar", (M.BAL["x"], M.BAL["y"], M.BAL_PAN + JAR_GRIP), "gb_stations")
    gb.status["Balance"] = "25.4127 g"
    sc.step(f"8/{n}", cap, 0.6, None, hold=0.9)
    cap = "... and puts it away in the sample hotel."
    gb.g_pick(sc, f"9/{n}", cap, "jar", (M.BAL["x"], M.BAL["y"], M.BAL_PAN + JAR_GRIP), JAR_W)
    gb.status.pop("Balance", None)
    gb.g_place(sc, f"9/{n}", cap, "jar", (HOTEL_FREE[0], HOTEL_FREE[1], HOTEL_FREE[2] + JAR_GRIP), "gb_stations")
    cap = ("An XRD air-sensitive holder, filled earlier, gets its dome, so the powder stays under argon all the way "
           "to the diffractometer on tray D.")
    rim = M.DOME_POST_TOP - (M.HOLDER["dome_r"] - 1.5)
    gb.g_pick(sc, f"10/{n}", cap, "dome", (M.DOME_POST[0], M.DOME_POST[1], rim + DOME_GRIP), DOME_W)
    stn = (M.STN["x"], M.STN["y"], M.STN_TOP - 7 + M.HOLDER["h"])
    gb.g_place(sc, f"10/{n}", cap, "dome", (stn[0], stn[1], stn[2] + DOME_GRIP), "holder")
    gb.g_pick(sc, f"10/{n}", cap, "holder", (stn[0], stn[1], M.STN_TOP - 7 + HOLDER_GRIP), HOLDER_W)
    b = nest(1)
    gb.g_place(sc, f"10/{n}", cap, "holder", (b[0], b[1], b[2] + HOLDER_GRIP), "gb_pallet")
    sc.step(f"10/{n}", cap, 0.9, gb.g_to(x=GX_HOME, y=GY_HOME), hold=0.1)
    cap = ("Out: the pallet goes back to the lock and the inner gate shuts. The lock is already argon, so the outer gate "
           "opens without a cycle.")
    gb.status["Pallet"] = "in the lock"
    sc.step(f"11/{n}", cap, 1.6, gb.pallet_to(M.X_LOCK), hold=0.1, cam_to=CAM_ARM)
    sc.step(f"11/{n}", cap, 0.8, gb.door("in", 0.0), hold=0.1)
    gb.status["Lock"] = "outer gate open"
    sc.step(f"11/{n}", cap, 0.8, both(gb.door("out", 1.0), gb.ghost_to(0.0)), hold=0.1)
    gb.status["Pallet"] = "out on the landing"
    sc.step(f"11/{n}", cap, 1.6, gb.pallet_to(M.X_OUT), hold=0.2)
    cap = "The arm takes the sealed holder to its cabinet, for the XRD. The pallet goes back in and the lock is cycled."
    hb = tw(nest(1, M.X_OUT))
    arm_pick(L, f"11/{n}", cap, "holder", down(hb + (0, 0, HOLDER_GRIP)), w_hold)
    arm_place(L, f"11/{n}", cap, down(amr_w(L.cup["out"]) + (0, 0, HOLDER_GRIP)), "amr")
    sc.step(f"11/{n}", cap, 1.4, both(L.robot.joint_to(q1=L.q_park), gb.pallet_to(M.X_LOCK)), hold=0.1)
    gb.status["Pallet"] = "in the lock"
    gb.lamp = AMBER
    gb.status["Lock"] = "evacuate and refill"
    sc.step(f"11/{n}", cap, 0.8, gb.door("out", 0.0), hold=0.6)
    gb.lamp = GREEN
    gb.status["Lock"] = "argon, idle"
    cap = "Tray G goes home to F2. Back in its slot it has power again, and the purifier restarts."
    L.store(f"12/{n}", cap, cam=CAM_WIDE)
    sc.step(f"12/{n}", cap, 0.8, None, hold=1.4, still=True)
    sc.save()


def manual(data):
    sc = Scene("glovebox_manual", TITLE)
    sc.cam = list(CAM_MANUAL)
    L = Lab(sc, data, at_open=True)
    gb = L.gb
    L.skin_f = 1.0
    gb.status.update({"Box": "Ar, O2 < 1 ppm, H2O < 1 ppm", "Mode": "automatic"})
    L.apply()
    n = 4
    cap = ("Now and then a job needs hands: a jar that won't open, a spill, a new fixture. The operator asks for "
           "manual mode at the VLM's panel. Tray G stays at the opening and the VLM won't move it while a cover is off.")
    gb.status["Mode"] = "manual: VLM locked"
    sc.step(f"1/{n}", cap, 1.2, None, hold=2.4,
            labels=[("port covers, interlocked", tw((-90, -425, 520)), (0.25, 0.18))])
    cap = "The covers swing flat against the window. The gloves stay inside the box the whole time; only the caps open."
    sc.step(f"2/{n}", cap, 1.6, gb.covers(1.0), hold=0.4)
    cap = "Hands in: two 8 in butyl gloves, over the deck's left half (the gantry parks right while they are in)."
    sc.step(f"3/{n}", cap, 1.0, gb.g_to(x=M.GX[1] - 40), hold=0.0)
    sc.step(f"3/{n}", cap, 1.6, gb.gloves_to(ext=1.0, yaw=(8.0, -6.0), droop=(14.0, 16.0)), hold=0.3)
    for yaw, droop in (((18.0, 4.0), (22.0, 20.0)), ((-4.0, -14.0), (10.0, 24.0)), ((8.0, -6.0), (14.0, 16.0))):
        sc.step(f"3/{n}", cap, 1.2, gb.gloves_to(yaw=yaw, droop=droop), hold=0.1)
    cap = "Hands out, covers on. Both sensors read closed, so the VLM may move the tray again, and the box is back in "\
          "automatic."
    sc.step(f"4/{n}", cap, 1.4, gb.gloves_to(ext=0.22, yaw=(0.0, 0.0), droop=(0.0, 0.0)), hold=0.1)
    sc.step(f"4/{n}", cap, 1.6, gb.covers(0.0), hold=0.2)
    gb.status["Mode"] = "automatic"
    sc.step(f"4/{n}", cap, 1.0, gb.g_to(x=GX_HOME), hold=1.6, still=True)
    sc.save()


# ===================================================================================================== stills
def stills(data):
    """A few high-resolution stills, no text."""
    from PIL import Image
    shots = []

    def shot(name, build):
        sc = Scene(f"_still_{name}", "", gif=False, mp4=False)
        build(sc)
        img = sc.render_base()
        Image.fromarray(img).save(OUT / f"{name}.png", optimize=True)
        sc.pl.close()
        shots.append(name)

    def bare(sc, ghost=0.0, pallet=None, door=0.0):
        floor = pv.Plane(center=(0, 0, -1), direction=(0, 0, 1), i_size=9000, j_size=9000)
        sc.add("floor", floor, FLOOR_C, "floor", ambient=1.0, diffuse=0.0, specular=0.0, smooth_shading=False)
        for name, e in tray_only(data["vlm"]).items():
            sc.add(name, e["mesh"], e["color"], e["group"], opacity=e["opacity"])
        sc.gmat[f"tray_{TRAY}"] = np.eye(4)
        gb = Box(sc, data["gb"], f"tray_{TRAY}")
        sc.parent["jar"] = "st_stations"
        sc.gmat["jar"] = T(HOTEL_FREE)
        gb.ghost_f, gb.door_out = ghost, door
        if pallet is not None:
            gb.x_pal = pallet
        gb.apply()
        return gb

    def front(sc):
        bare(sc)
        sc.cam = [(1700, -3300, 1500), (0, 0, 330), (0, 0, 1)]

    def cutaway(sc):
        bare(sc, ghost=1.0, pallet=M.X_OUT, door=1.0)
        sc.cam = [(2000, -2800, 1900), (80, 0, 300), (0, 0, 1)]

    def back(sc):
        bare(sc, ghost=1.0)
        sc.cam = [(-1900, 2900, 1900), (0, 0, 300), (0, 0, 1)]

    def in_vlm(sc):
        L = Lab(sc, data, at_open=True)
        L.skin_f = 1.0
        L.gb.door_out, L.gb.x_pal = 1.0, M.X_OUT
        sc.parent["jar"] = "gb_pallet"
        sc.gmat["jar"] = T((M.NEST[0], 0, NEST_Z))
        L.apply()
        sc.cam = [(950, -4400, 2800), (350, -1250, 1250), (0, 0, 1)]

    for name, f in (("glovebox_front", front), ("glovebox_cutaway", cutaway), ("glovebox_back", back),
                    ("glovebox_in_vlm", in_vlm)):
        shot(name, f)
    print("stills:", ", ".join(shots))


# ===================================================================================================== main
def join(names, out_name):
    lst = OUT / "mp4" / "_join.txt"
    lst.write_text("".join(f"file '{(OUT / 'mp4' / (n + '.mp4')).resolve()}'\n" for n in names))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", str(OUT / "mp4" / f"{out_name}.mp4")], check=True)
    lst.unlink()


def main(argv):
    OUT.mkdir(exist_ok=True)
    data = {"gb": gb_meshes(), "vlm": vlm_meshes()}
    for a in argv or ["design", "transfer", "manual", "full"]:
        if a == "design":
            design(data)
        elif a == "transfer":
            transfer(data)
        elif a == "manual":
            manual(data)
        elif a == "stills":
            stills(data)
        elif a == "full":
            join(["glovebox_design", "glovebox_transfer", "glovebox_manual"], "glovebox_full")
        else:
            raise SystemExit(f"unknown chapter {a}")


if __name__ == "__main__":
    main(sys.argv[1:])
