#!/usr/bin/env python3
"""The three camera units from the Onshape export, placed on the rePowder model in viz3d/.

The Onshape Part Studio (../exports/onshape_partstudio.step) draws the units round a rough machine whose ports are
where the training-video frames put them. viz3d/model.py is the CadQuery model of the whole machine from
atomizer-training/viz3d/ (copied unchanged, see viz3d/README.md). Both use the same axes (x to the operator's right,
y away from the operator, z up from the floor, furnace axis at x = y = 0), but the model puts each window a little
elsewhere. So each unit is moved, rigidly, from its Onshape port to the model's:

- front: the port's axis, from where it leaves the chamber face (fp_x, fp_z, fp_tilt, fp_yaw), goes to the model's
  VIEWPORT / VIEWPORT_N. The model's own 12-sided flange and glass are left out, and the Onshape port nut, glass and
  AMAZEMET's LED cover and cable pod are drawn in their place, since those are what the socket fits.
- left: the sight glass ring's base on the door's outer face goes to the model's ring base on the door's raised
  panel. The Onshape ring (65 across, 30 proud) is drawn over the model's.
- top: the magnetic base and the post stay on the blue frame's top, which is in the same place in both. The hub,
  arm, camera pod and display box slide down the post (the detent collar sets that height) until the camera's line
  of sight passes through the centre of the model's lid window.

    python units.py      # prints the moves and checks every unit against the machine -> ../exports/placement.json
"""
from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "viz3d"))
sys.path.insert(1, str(HERE.parent / "onshape"))

import cadquery as cq                               # noqa: E402
import model as M                                   # noqa: E402  (viz3d/model.py)
from check import EXPORTS, read_named_solids        # noqa: E402
from variables import VARIABLES                     # noqa: E402

VAR = {name: value for name, value, _, _ in VARIABLES}
UNITS = ("front", "left", "top")

# the model's door sight glass: model.py builds it inside chamber_parts() as a ring 12 mm proud of the door's raised
# panel, at sight = (CH_X[0] - DOOR_T - 10, -45, 1060)
SIGHT_BASE = np.array([M.CH_X[0] - M.DOOR_T - 10.0, -45.0, 1060.0])

# the Onshape machine parts kept, because the units fit them; the rest of the machine comes from the model
FRONT_PORT = ("(machine) front port nut", "(machine) front port glass", "(machine) AMAZEMET LED cover and cable pod")
LEFT_PORT = ("(machine) door sight glass ring", "(machine) door sight glass")
HIDE_IN_MODEL = ("viewport_flange", "viewport_glass")      # replaced by FRONT_PORT


def unit(v) -> np.ndarray:
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def frame(origin, z, x) -> np.ndarray:
    """4 x 4 matrix of the right-handed frame at `origin` with z along `z` and x along `x` (made square to z)."""
    z = unit(z)
    x = unit(np.asarray(x, float) - z * (np.asarray(x, float) @ z))
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = x, np.cross(z, x), z, origin
    return m


def translate(v) -> np.ndarray:
    m = np.eye(4)
    m[:3, 3] = v
    return m


# ------------------------------------------------------------------------------------------------ the three moves
def front_move() -> np.ndarray:
    """Onshape's frontCS(out = 0), the port axis where it leaves the chamber face, onto the model's view port."""
    t, w = math.radians(VAR["fp_tilt"]), math.radians(VAR["fp_yaw"])
    n_o = np.array([-math.sin(w) * math.cos(t), -math.cos(w) * math.cos(t), math.sin(t)])
    f_o = frame([VAR["fp_x"], VAR["ch_front_y"], VAR["fp_z"]], n_o, np.cross([0, 0, 1], n_o))
    n_v = unit(M.VIEWPORT_N)
    o_v = M.VIEWPORT + n_v * (M.CH_Y[0] - M.VIEWPORT[1]) / n_v[1]       # where the model's axis crosses its face
    f_v = frame(o_v, n_v, np.cross([0, 0, 1], n_v))
    return f_v @ np.linalg.inv(f_o)


def left_move() -> np.ndarray:
    """The sight glass ring's base on Onshape's door face onto the model's ring base, on the door's raised panel."""
    o = np.array([VAR["ch_left_x"] - VAR["door_t"], VAR["lp_y"], VAR["lp_z"]])
    return translate(SIGHT_BASE - o)


def lid_window_onshape() -> np.ndarray:
    """lidFacet() in viewport_mounts.fs: the window centre on the lid's front facet."""
    a = math.radians(VAR["lid_facet_angle"])
    rb = VAR["lid_r"] * math.cos(math.radians(30))
    z1 = VAR["furn_top_z"] + VAR["lid_h1"]
    s = (VAR["tw_z"] - z1) / math.sin(a)
    return np.array([VAR["tw_x"], -rb, z1]) + np.array([0.0, math.cos(a), math.sin(a)]) * s


def lid_window_model() -> np.ndarray:
    """hood_parts() in model.py: the window centre on the hood's front facet."""
    c30 = math.cos(math.pi / 6)
    return np.array([0.0, -(M.HOOD_R0 + M.HOOD_R1) * c30 / 2, M.HOOD_Z0 + M.HOOD_H1 + M.HOOD_H2 / 2])


def top_drop() -> float:
    """How far (mm, negative = down) the arm slides on the post so that the camera's line, unchanged in direction,
    passes through the model's lid window."""
    a_o = np.array([0.0, 0.0, VAR["aim_z"]])
    u = unit(lid_window_onshape() - a_o)
    w = lid_window_model()
    return float(w[2] - (a_o[2] + w[1] / u[1] * u[2]))


def top_move() -> np.ndarray:
    return translate([0.0, 0.0, top_drop()])


def sight_line() -> tuple[np.ndarray, np.ndarray]:
    """(aim point on the furnace axis, unit vector up the line to the camera), on the model."""
    a_o = np.array([0.0, 0.0, VAR["aim_z"]])
    u = unit(lid_window_onshape() - a_o)
    return a_o + np.array([0.0, 0.0, top_drop()]), u


MOVES = {"front": front_move, "left": left_move, "top": top_move}


# ------------------------------------------------------------------------------------------------ parts
def colour(name: str) -> tuple[tuple[float, float, float], float]:
    n = name.lower()
    if "glass" in n or "window" in n:
        return (0.55, 0.80, 0.95), 0.55
    if "amazemet" in n:
        return (0.33, 0.34, 0.37), 1.0
    if n.startswith("(machine)"):
        return (0.76, 0.77, 0.79), 1.0
    if "face plate" in n or "detent collar" in n:
        return (0.93, 0.47, 0.10), 1.0
    if "(print)" in n:
        return (0.16, 0.16, 0.18), 1.0
    if "screen" in n:
        return (0.12, 0.30, 0.62), 1.0
    if "lens" in n or "connector" in n or "display" in n or "magnetic" in n:
        return (0.06, 0.06, 0.07), 1.0
    if "camera" in n or "raspberry pi 5" in n:
        return (0.07, 0.45, 0.22), 1.0
    if "cooler" in n:
        return (0.30, 0.31, 0.34), 1.0
    if "extrusion" in n or "post rod" in n:
        return (0.80, 0.81, 0.83), 1.0
    return (0.80, 0.81, 0.83), 1.0


def unit_of(name: str, shape) -> str | None:
    m = re.match(r"(FRONT|LEFT|TOP)\b", name)
    if m:
        return m.group(1).lower()
    base = name.split(" [")[0]
    if base in FRONT_PORT:
        return "front"
    if base in LEFT_PORT:
        return "left"
    if name.startswith("(bought)"):
        bb = shape.BoundingBox()
        if bb.zmin >= 1590:
            return "top"
        return "left" if bb.xmax < -140 else "front"
    return None             # the rest of Onshape's rough machine: the model replaces it


def step_of(u: str, name: str) -> str:
    """The assembly step a part belongs to (assembly.py moves each step's parts together)."""
    n = name.lower()
    if n.startswith("(machine)"):
        return "port"
    if u == "front":
        for key, words in (("socket", ("socket",)), ("face", ("face plate",)), ("hq", ("hq camera", "(bought) lens")),
                           ("wide", ("camera module 3",)), ("pi", ("pi 5",)), ("display", ("display",))):
            if any(w in n for w in words):
                return key
    if u == "left":
        for key, words in (("collar", ("collar",)), ("face", ("face plate",)), ("cam", ("camera module 3",)),
                           ("pi", ("pi 5",)), ("display", ("display",))):
            if any(w in n for w in words):
                return key
    if u == "top":
        for key, words in (("base", ("magnetic base",)), ("post", ("post rod",)), ("collar", ("detent collar",)),
                           ("hub", ("hub",)), ("arm", ("extrusion",)), ("pod", ("camera pod", "hq camera", "(bought) lens"))):
            if any(w in n for w in words):
                return key
        return "box"
    raise ValueError(f"no step for {u}: {name}")


@dataclass
class Piece:
    name: str                 # Onshape's part name ("[k]" when one part has several solids)
    unit: str                 # front | left | top
    step: str                 # assembly step, see step_of()
    shape: cq.Shape           # placed on the model
    color: tuple
    opacity: float


def to_location(m: np.ndarray) -> cq.Location:
    from OCP.gp import gp_Trsf
    t = gp_Trsf()
    t.SetValues(*[float(m[i, j]) for i in range(3) for j in range(4)])
    return cq.Location(t)


def pieces() -> list[Piece]:
    """Every Onshape part the render uses, moved onto the model."""
    out = []
    for name, shape in read_named_solids(EXPORTS / "onshape_partstudio.step"):
        u = unit_of(name, shape)
        if u is None:
            continue
        st = step_of(u, name)
        m = MOVES[u]()
        if u == "top" and st in ("base", "post"):
            m = np.eye(4)                   # they stay on the frame's top
        c, op = colour(name)
        out.append(Piece(name, u, st, shape.moved(to_location(m)), c, op))
    return out


def tess(shape, tol=0.15):
    import pyvista as pv
    v, t = shape.tessellate(tol, 0.25)
    pts = np.array([[p.x, p.y, p.z] for p in v])
    m = pv.PolyData(pts, np.hstack([[3, *tri] for tri in t]))
    return m.compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


# ------------------------------------------------------------------------------------------------ checks
def clearances(ps: list[Piece]) -> dict:
    """Every unit part against every model part near it: the smallest gap per unit, and any overlap."""
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps

    machine = [p for p in M.parts() if p.name not in HIDE_IN_MODEL]
    res = {}
    for u in UNITS:
        mine = [p for p in ps if p.unit == u and p.step != "port"]
        best, hits = (math.inf, "", ""), []
        for p in mine:
            bb = p.shape.BoundingBox()
            for q in machine:
                qb = q.shape.BoundingBox()
                if (bb.xmin - 60 > qb.xmax or qb.xmin - 60 > bb.xmax or bb.ymin - 60 > qb.ymax or qb.ymin - 60 > bb.ymax
                        or bb.zmin - 60 > qb.zmax or qb.zmin - 60 > bb.zmax):
                    continue
                d = BRepExtrema_DistShapeShape(p.shape.wrapped, q.shape.wrapped)
                d.Perform()
                gap = d.Value() if d.IsDone() else math.nan
                if gap < best[0]:
                    best = (gap, p.name, q.name)
                if gap < 1e-6:
                    op = BRepAlgoAPI_Common(p.shape.wrapped, q.shape.wrapped)
                    op.Build()
                    g = GProp_GProps()
                    BRepGProp.VolumeProperties_s(op.Shape(), g)
                    if g.Mass() > 0.01:
                        hits.append({"unit_part": p.name, "model_part": q.name, "overlap_mm3": round(g.Mass(), 2)})
        res[u] = {"nearest_model_part": best[2], "unit_part": best[1], "gap_mm": round(best[0], 1),
                  "interference": hits}
    return res


def main() -> None:
    ps = pieces()
    fm = front_move()
    w_o, w_v = lid_window_onshape(), lid_window_model()
    aim, up = sight_line()
    n_v = unit(M.VIEWPORT_N)
    report = {
        "model": "viz3d/model.py (atomizer-training/viz3d/model.py at 7ec59ab, unchanged; VIZ3D_STACK=measured)",
        "moves": {
            "front": {"matrix": np.round(fm, 4).tolist(),
                      "onshape_port": [VAR["fp_x"], VAR["ch_front_y"], VAR["fp_z"]],
                      "model_port": np.round(M.VIEWPORT + n_v * (M.CH_Y[0] - M.VIEWPORT[1]) / n_v[1], 1).tolist(),
                      "onshape_axis_tilt_yaw_deg": [VAR["fp_tilt"], VAR["fp_yaw"]],
                      "model_axis_tilt_yaw_deg": [round(math.degrees(math.asin(n_v[2])), 1),
                                                  round(math.degrees(math.atan2(-n_v[0], -n_v[1])), 1)]},
            "left": {"translation_mm": np.round(left_move()[:3, 3], 1).tolist(),
                     "onshape_sight_glass": [VAR["lp_y"], VAR["lp_z"]], "model_sight_glass": SIGHT_BASE[1:].tolist()},
            "top": {"arm_lowered_mm": round(-top_drop(), 1),
                    "onshape_lid_window": np.round(w_o, 1).tolist(), "model_lid_window": np.round(w_v, 1).tolist(),
                    "aim_point": np.round(aim, 1).tolist(),
                    "line_below_horizontal_deg": round(math.degrees(math.asin(up[2])), 1)},
        },
        "clearances": clearances(ps),
    }
    path = EXPORTS / "placement.json"
    path.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
