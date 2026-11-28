"""Shared loading and views for render.py and assembly.py: the rePowder model (viz3d/) plus the #151 parts."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "viz3d"))

import integration as I  # noqa: E402
import model as M  # noqa: E402
import scene as S  # noqa: E402

UTILITIES = ("argon_cylinder", "argon_regulator", "argon_gauges", "vacuum_pump", "pump_sight_glass", "heat_exchanger",
             "hx_grille", "hx_display", "air_frl")
REPLACED = ("cabinet", "side_door_r", "hmi_arm")   # integration.py's cabinet_open, door_r and hmi_arm2 stand in


def cam_at(focal, back, up=(0, 0, 1)):
    f = np.asarray(focal, float)
    return [tuple(f + np.asarray(back, float)), tuple(f), up]


# views: (camera position, focal point, up)
INTRO = cam_at((470, 160, 1230), (1750, -2050, 900))
HMI_FRONT = cam_at(I.hmi_pt((-10, -90, 90)), I.hmi_vec((-430, -760, 330)))
HMI_SIDE = cam_at(I.hmi_pt((0, -90, 110)), I.hmi_vec((-820, -330, 180)))
HMI_BACK = cam_at(I.hmi_pt((-30, 40, -20)), I.hmi_vec((380, 640, 260)))
PANEL = cam_at((480, 110, 1440), (-330, -640, 280))
DOOR = cam_at((450, 420, 1150), (1250, -420, 520))
TAP = cam_at((385, 420, 1150), (640, -230, 230))


def hinge_open(deg):
    return S.R((0, 0, 1), deg, (I.DOOR_HINGE[0], I.DOOR_HINGE[1], 0))


def shutter_pose(prefix: str, deg: float) -> np.ndarray:
    """Rotation of a camera's flip shutter about its hinge, in world coordinates (0 = closed over the lens)."""
    _, _, _, hp, ha = I.head()
    if prefix == "hmicam":
        ex, ey, ez = I.cam_axes(I.HMI_CAM_DIR_L)
        p_l = I.HMI_CAM_C_L + ex * hp[0] + ey * hp[1] + ez * hp[2]
        return S.R(I.hmi_vec(ex), deg, I.hmi_pt(p_l))
    ex, ey, ez = I.cam_axes(I.PANEL_CAM_DIR)
    p = I.PANEL_CAM_C + ex * hp[0] + ey * hp[1] + ez * hp[2]
    return S.R(ex, deg, p)


SHUTTER_OPEN = 105.0


def fov_meshes() -> dict[str, pv.PolyData]:
    """View cones: lens -> the corners of what each camera has to see (the HMI's active area, the GU 500's LCD)."""
    a, b = I.ACTIVE[0] / 2, I.ACTIVE[1] / 2
    hmi = [I.hmi_pt((sx * a, -20.6, sz * b)) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    apex_h = I.hmi_pt(I.HMI_CAM_C_L + I.HMI_CAM_DIR_L * 1.0)
    lx, ly, lz = I.LCD_C
    lcd = [np.array([lx + sx * I.LCD_SIZE[0] / 2, ly - 1.5, lz + sz * I.LCD_SIZE[1] / 2])
           for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    apex_p = I.PANEL_CAM_C + I.PANEL_CAM_DIR * 1.0

    def cone(apex, quad):
        pts = np.vstack([apex] + quad)
        faces = np.hstack([[3, 0, 1, 2], [3, 0, 2, 3], [3, 0, 3, 4], [3, 0, 4, 1]])
        return pv.PolyData(pts, faces)
    return {"fov_hmi": cone(apex_h, hmi), "fov_panel": cone(apex_p, lcd)}


def load(sc: S.Scene, interior=True, shutters_open=True) -> None:
    """The machine (utilities, pipes and the replaced cabinet hidden), the #151 parts and cables, the view cones."""
    S.load_machine(sc, hide=UTILITIES + REPLACED, pipes=False)
    for name, m in I.meshes().items():
        if not interior and m["group"] == "interior":
            continue
        sc.add(name, m["whole"], m["color"], m["group"], opacity=m["opacity"],
               **({"specular": 0.6, "specular_power": 40} if name.startswith("film") else {}))
    for name, r in I.cable_routes().items():
        sc.add(name, pv.Spline(np.array(r["pts"], float), 200).tube(radius=r["r"], n_sides=12), r["color"], r["group"],
               specular=0.2)
    x, y, z = I.X3_C
    x3 = [(x, y, z - 76), (x + 1, y, z - 120), (x + 6, y + 30, z - 175), (x + 14, 560, z - 215), (x + 16, 565, z - 240)]
    sc.add("x3_cable", pv.Spline(np.array(x3, float), 80).tube(radius=4.5, n_sides=12), (0.25, 0.26, 0.28), "x3_plug")
    for name, poly in fov_meshes().items():
        sc.add(name, poly, I.FOV, name, opacity=0.28, ambient=0.6, specular=0.0, smooth_shading=False)
        sc.add(name + "_edges", poly.extract_all_edges().tube(radius=0.8, n_sides=6), (0.85, 0.60, 0.05), name,
               ambient=0.5, specular=0.0)
    sc.parent["hmicam_shutter"] = "hmicam_head"
    sc.parent["panelcam_shutter"] = "panelcam_head"
    sc.parent["adc_lid"] = "adc"
    if shutters_open:
        sc.gmat["hmicam_shutter"] = shutter_pose("hmicam", SHUTTER_OPEN)
        sc.gmat["panelcam_shutter"] = shutter_pose("panelcam", SHUTTER_OPEN)
    for g in ("fov_hmi", "fov_panel"):
        sc.gmat.setdefault(g, np.eye(4))
