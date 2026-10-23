#!/usr/bin/env python3
"""Stills of the three units on the rePowder model (viz3d/), 1600 x 900.

The units are Onshape's parts (../exports/onshape_partstudio.step), moved onto the model by units.py; the machine is
viz3d/model.py, drawn with viz3d/scene.py, as in the atomizer animations.

    xvfb-run -a -s "-screen 0 1920x1080x24" python render.py      # -> ../renders/*.png
"""
from __future__ import annotations

import numpy as np
import pyvista as pv

import units as U
import model as M          # viz3d/model.py (units.py puts viz3d/ on the path)
import scene as S          # viz3d/scene.py

OUT = U.HERE.parent / "renders"
SIZE = (1600, 900)
UTILITIES = ("argon_cylinder", "argon_regulator", "argon_gauges", "vacuum_pump", "pump_sight_glass", "heat_exchanger",
             "hx_grille", "hx_display", "air_frl")
N_FRONT = U.unit(M.VIEWPORT_N)
POST = np.array([-90.0, 195.0])          # the top unit's post axis (x, y): Onshape's post_x and post rod

# views: (camera position, focal point, up)
OVERALL = [(-1450, -2650, 2150), (40, 0, 1180), (0, 0, 1)]
FRONT = [(-420, -900, 1330), (0, -205, 1060), (0, 0, 1)]
LEFT = [(-1150, -780, 1250), (-190, -10, 960), (0, 0, 1)]
TOP = [(-1050, -1250, 2150), (-30, -60, 1600), (0, 0, 1)]


def add_units(sc: S.Scene, ps: list[U.Piece], which=U.UNITS) -> None:
    """Each piece as an actor in group '<unit>:<step>'. The unit's parts (not its port) ride on '<unit>:unit'; the
    left unit and its sight glass ride on the door; the top unit's hub, arm, pod and box on 'top:swing'."""
    for k, p in enumerate(ps):
        if p.unit not in which:
            continue
        g = f"{p.unit}:{p.step}"
        sc.add(f"{g}:{k}", U.tess(p.shape), p.color, g, opacity=p.opacity, specular=0.25)
        if p.step != "port":
            sc.parent[g] = f"{p.unit}:unit"
    sc.parent["left:unit"] = "door"
    sc.parent["left:port"] = "door"
    for st in ("hub", "arm", "pod", "box"):
        sc.parent[f"top:{st}"] = "top:swing"
    sc.parent["top:swing"] = "top:unit"
    for g in ("front:unit", "left:unit", "top:unit", "top:swing"):
        sc.gmat.setdefault(g, np.eye(4))


def sight_line_mesh(radius=1.6) -> pv.PolyData:
    aim, up = U.sight_line()
    return pv.Line(aim, aim + up * 476.0).tube(radius=radius, n_sides=12)


def machine(sc: S.Scene, hide=(), ghost=None, pipes=True) -> None:
    S.load_machine(sc, hide=U.HIDE_IN_MODEL + tuple(hide), ghost=ghost, pipes=pipes)


def still(name, title, cam, caption, labels, hide=(), ghost=None, which=U.UNITS, extra=None, view_angle=30.0,
          pipes=True):
    sc = S.Scene(name, title, size=SIZE, gif=False, mp4=False)
    machine(sc, hide=hide, ghost=ghost, pipes=pipes)
    add_units(sc, U.pieces(), which)
    if extra:
        extra(sc)
    sc.cam = cam
    sc.view_angle = view_angle
    sc.caption = caption
    sc.labels = [(t, xyz, at, 1.0) for t, xyz, at in labels]
    img = sc.snap()
    OUT.mkdir(exist_ok=True)
    img.convert("RGB").save(OUT / f"{name}.png", optimize=True)
    sc.pl.close()
    print("wrote", name)


def red_line(sc):
    sc.add("sight", sight_line_mesh(), (0.85, 0.10, 0.10), "sight", ambient=0.6, specular=0.0)


def front_section(name="front_section"):
    """Cut through the HQ Camera's axis, square to the port's horizontal: machine and unit both clipped."""
    ps = U.pieces()
    hq = [p for p in ps if p.unit == "front" and p.name == "(bought) lens"][0].shape.Center()
    origin = np.array([hq.x, hq.y, hq.z])
    normal = U.unit(np.cross([0, 0, 1], N_FRONT))          # the port frame's x: cut square to it, keep +x
    sc = S.Scene(name, "Front port: section through the HQ Camera's axis", size=SIZE, gif=False, mp4=False)
    ms = M.meshes()
    keep = ("chamber", "chamber_slots", "platform", "furnace_body", "cabinet", "floor", "plate", "upper_sonotrode",
            "connector", "sonotrode", "door", "nozzle_holder", "graphite_seal", "nut")
    for nm in keep:
        m = ms[nm]
        cut = m["whole"].clip(normal=normal, origin=origin, invert=False)
        if cut.n_points:
            sc.add(nm, cut, m["color"], "static", opacity=m["opacity"])
    for k, p in enumerate(ps):
        if p.unit != "front":
            continue
        cut = U.tess(p.shape).clip(normal=normal, origin=origin, invert=False)
        if cut.n_points:
            sc.add(f"front:{k}", cut, p.color, "front", opacity=p.opacity)
    # the HQ Camera's and the wide camera's lines of sight, through the port glass to the plate
    plate = M.PLATE_C
    for nm, col in (("(bought) lens", (0.85, 0.1, 0.1)), ("(bought) Camera Module 3 lens", (0.95, 0.55, 0.1))):
        c = [p for p in ps if p.unit == "front" and p.name.split(" [")[0] == nm][0].shape.Center()
        a = np.array([c.x, c.y, c.z])
        sc.add("los:" + nm, pv.Line(a, plate).tube(radius=1.2, n_sides=10), col, "los", ambient=0.6, specular=0.0)
    sc.cam = [tuple(origin - normal * 620 + np.array([0, -150, 90])), (origin[0], -150, 1010), (0, 0, 1)]
    sc.caption = ("The cameras sit in the socket at the LED cover's 75 mm opening and look through it and the port "
                  "glass, down at the plate (red: the HQ Camera's axis to the plate; orange: the wide camera's).")
    def on_cut(name, shift=(0, 0, 0)):
        """A part's centre, moved along the port frame's y by shift[1] and z by shift[2], on the cut plane."""
        c = [p for p in ps if p.unit == "front" and p.name.split(" [")[0] == name][0].shape.Center()
        y_v = np.cross(N_FRONT, normal)
        q = np.array([c.x, c.y, c.z]) + y_v * shift[1] + N_FRONT * shift[2]
        return tuple(q - normal * ((q - origin) @ normal))
    sc.labels = [(t, xyz, at, 1.0) for t, xyz, at in (
        ("HQ Camera (M12) + 16 mm lens", tuple(origin), (0.04, 0.22)),
        ("AMAZEMET LED cover", on_cut("(machine) front port glass", (0, -72, 20)), (0.96, 0.62)),
        ("port nut and glass", on_cut("(machine) front port glass", (0, 18, 0)), (0.04, 0.42)),
        ("Pi 5", on_cut("(bought) Raspberry Pi 5", (0, 12, 0)), (0.96, 0.30)),
        ("5 in HDMI display, face plate", on_cut("(bought) 5 in HDMI display", (0, 25, 0)), (0.96, 0.16)),
        ("plate (measured set-up)", tuple(M.PLATE_C), (0.04, 0.84)),
        ("chamber", (origin[0], 60, 1125), (0.04, 0.10)))]
    img = sc.snap()
    img.convert("RGB").save(OUT / f"{name}.png", optimize=True)
    sc.pl.close()
    print("wrote", name)


def main() -> None:
    aim, up = U.sight_line()
    still("overall", "rePowder viewport cameras on the lab's model of the machine", OVERALL,
          "Front (HQ + wide) on AMAZEMET's LED cover, left on the door's sight glass, top on a swing arm over the lid "
          "window. Machine: atomizer-training/viz3d's CadQuery model (measured stack); units: the Onshape design.",
          [("front: HQ + Camera Module 3 Wide,\nPi 5, 5 in HDMI display", tuple(M.VIEWPORT + N_FRONT * 140), (0.97, 0.55)),
           ("left: Camera Module 3 Wide, Pi 5,\n5 in Touch Display 2 (on the door)", (-200, -40, 1040), (0.03, 0.58)),
           ("top: HQ Camera + 16 mm lens, Pi 5,\n2.8 in DSI, on a 2020 swing arm", (-10, -200, 1720), (0.97, 0.16)),
           ("magnetic base and post\non the blue frame", (-90, 195, 1640), (0.03, 0.14)),
           ("lid window", tuple(U.lid_window_model()), (0.03, 0.34))],
          hide=UTILITIES, extra=red_line)
    still("front_unit", "Front port: HQ + wide on AMAZEMET's LED cover", FRONT,
          "A 12-sided socket slides 15 mm over the LED cover, keyed by the cable pod and held by an M6 ball plunger; "
          "HQ Camera (M12) + Camera Module 3 Wide, Pi 5, 5 in HDMI display facing the operator.",
          [("socket + tray (PETG)", tuple(M.VIEWPORT + N_FRONT * 100 + np.array([-80, 0, -30])), (0.03, 0.62)),
           ("face plate over the 5 in HDMI display", tuple(M.VIEWPORT + N_FRONT * 120 + np.array([0, 0, 45])), (0.97, 0.18)),
           ("cable pod (6 o'clock)", tuple(M.VIEWPORT + N_FRONT * 70 + np.array([0, 0, -85])), (0.97, 0.72)),
           ("chamber door", (M.CH_X[0] - 20, -90, 900), (0.03, 0.80))],
          hide=UTILITIES, which=("front", "left"))
    front_section()
    still("left_unit", "Left port: one camera on the door's sight glass", LEFT,
          "A split collar clamps the sight glass ring with one M4 screw; Camera Module 3 Wide on its axis, Pi 5 behind "
          "it, 5 in Touch Display 2 facing the operator. The side view of nozzle and plate; the unit rides on the door.",
          [("collar + tray (PETG)", (-185, -118, 1030), (0.03, 0.66)),
           ("face plate over the 5 in Touch Display 2", (-214, -20, 1075), (0.03, 0.22)),
           ("door (3 star knobs)", (M.CH_X[0] - 25, 60, 880), (0.97, 0.60)),
           ("ultrasonic stack, 45° (measured)", tuple(M.on_axis(260)), (0.97, 0.80)),
           ("front unit", tuple(M.VIEWPORT + N_FRONT * 120), (0.97, 0.25))],
          hide=UTILITIES, which=("front", "left"))

    def top_extra(sc):
        red_line(sc)
    still("top_unit", "Top: the lid window, from a swing arm", TOP,
          "HQ Camera + 16 mm lens (hot mirror, ND) on the line from the melt through the lid window (red), about 66° "
          "below horizontal; a 2020 arm on a post and magnetic base swings clear on a ball-plunger detent.",
          [("camera pod: HQ Camera, 16 mm lens", (0, -215, 1700), (0.97, 0.40)),
           ("display box: Pi 5 + 2.8 in DSI", (20, -300, 1790), (0.97, 0.20)),
           ("hub + detent collar on a 5/8 in post", (-90, 195, 1775), (0.03, 0.20)),
           ("switchable magnetic base", (-90, 195, 1625), (0.03, 0.40)),
           ("lid window (to the melt)", tuple(U.lid_window_model()), (0.03, 0.62)),
           ("aim point in the crucible", tuple(aim), (0.97, 0.74))],
          hide=UTILITIES, which=("top",), extra=top_extra,
          ghost={"hood": 0.25, "hood_window": 0.4, "hood_hot_label": 0.4, "hood_knob": 0.4, "furnace_body": 0.22,
                 "top_insulation": 0.25, "oring": 0.3})


if __name__ == "__main__":
    main()
