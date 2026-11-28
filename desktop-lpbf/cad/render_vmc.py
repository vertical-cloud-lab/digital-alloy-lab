"""The machine the parts are cut on, for the machining chapter of render_build.py: a Haas VF-4 table and spindle, a
6 in. machine vise and a Haas HRT210 4th-axis rotary table with a tailstock.

Why: the first animation moved the cutter round a fixed part, which reads as 5-axis machining. A BYU machinist noted the
shop has 4-axis mills but no 5-axis. Here the spindle is always vertical (a VMC), and the part is re-clamped in a vise or
indexed about the rotary's horizontal A axis between operations, which is how the shop would run it.

Published dimensions used (Haas, fetched 2026-11-20 22:27-22:31 UTC through the lab Pi):
  VF-4  table 1321 x 495 mm, 5 T-slots 16 mm wide on 80 mm centres; travels 1270 / 508 / 635 mm; spindle nose to table
        107-742 mm; CT40 / BT40, 8100 rpm; max tool Ø89 mm.        https://www.haascnc.com/machines/vertical-mills/vf-series/models/medium/vf-4.html
  HRT210 platter Ø210 mm, centre height 152.40 mm, 6 T-slots at 60 deg, 77.1 kg on the platter with a tailstock.
        https://www.haascnc.com/machines/rotaries-indexers/rotary-tables/models/hrt210.html
The vise is drawn to a common 6 in. class (152 mm jaws, 44 mm jaw height, 229 mm max opening), and the rotary's housing and
the tailstock to proportions, not to a drawing. The spindle head is a box: only the nose, holder and tool matter here.
"""
from __future__ import annotations

import math

import numpy as np
import pyvista as pv

TABLE = dict(L=1321.0, W=495.0, t=90.0, slots=5, slot_w=16.0, slot_pitch=80.0, slot_d=14.0)
HRT210 = dict(platter_d=210.0, centre_h=152.4, platter_t=28.0)
VISE6 = dict(jaw_w=152.4, jaw_h=44.5, open_max=229.0, L=420.0, H=100.0)
COL = dict(table="#5b646d", slot="#3e454c", vise="#2f5f8a", jaw="#9aa3ab", rotary="#2d3136", platter="#8e979f",
           head="#d8dce0", holder="#3a3f45", nut="#9aa3ab", tool="#d9b44a")


def table(z_top=0.0, cx=0.0, cy=0.0):
    """[(mesh, colour)]: the VF-4 table, top at z_top, with its five T-slots along X."""
    L, W, t = TABLE["L"], TABLE["W"], TABLE["t"]
    body = pv.Box((cx - L / 2, cx + L / 2, cy - W / 2, cy + W / 2, z_top - t, z_top - 0.5))
    top_strips, slots = [], []
    n, p = TABLE["slots"], TABLE["slot_pitch"]
    ys = [cy + (k - (n - 1) / 2) * p for k in range(n)]
    edges = [cy - W / 2] + sum([[y - TABLE["slot_w"] / 2, y + TABLE["slot_w"] / 2] for y in ys], []) + [cy + W / 2]
    for a, b in zip(edges[0::2], edges[1::2]):
        top_strips.append(pv.Box((cx - L / 2, cx + L / 2, a, b, z_top - 0.5, z_top)))
    for y in ys:
        slots.append(pv.Box((cx - L / 2, cx + L / 2, y - TABLE["slot_w"] / 2, y + TABLE["slot_w"] / 2, z_top - TABLE["slot_d"], z_top - 0.5)))
    return [(body, COL["table"]), (top_strips[0].merge(top_strips[1:]), COL["table"]), (slots[0].merge(slots[1:]), COL["slot"])]


def vise(at=(0.0, 0.0, 0.0), opening=150.0, axis="x"):
    """[(mesh, colour)]: a 6 in. vise on the table at `at` (centre of its base), jaws closing along `axis` ('x' or 'y'),
    `opening` mm between the jaws. Returns also the jaw-top z through `vise_jaw_top`."""
    x, y, z = map(float, at)
    L, H, jw, jh = VISE6["L"], VISE6["H"], VISE6["jaw_w"], VISE6["jaw_h"]
    o = float(np.clip(opening, 0.0, VISE6["open_max"]))
    base = pv.Box((-L / 2, L / 2, -jw / 2 - 8, jw / 2 + 8, 0.0, H - jh))
    fixed = pv.Box((L / 2 - 70, L / 2 - 70 + 45, -jw / 2 - 8, jw / 2 + 8, H - jh, H + 2))
    fixed_jaw = pv.Box((L / 2 - 70 - 10, L / 2 - 70, -jw / 2, jw / 2, H - jh, H))
    mx = L / 2 - 80 - o
    moving = pv.Box((mx - 60, mx - 10, -jw / 2 - 8, jw / 2 + 8, H - jh, H + 2))
    moving_jaw = pv.Box((mx - 10, mx, -jw / 2, jw / 2, H - jh, H))
    screw = pv.Cylinder(center=(-L / 2 - 30, 0, H - jh - 20), direction=(1, 0, 0), radius=12, height=60)
    pieces = [(base, COL["vise"]), (fixed, COL["vise"]), (moving, COL["vise"]), (fixed_jaw, COL["jaw"]), (moving_jaw, COL["jaw"]),
              (screw, COL["jaw"])]
    R = np.eye(4)
    if axis == "y":
        R[:3, :3] = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    out = []
    for m, c in pieces:
        m = m.transform(R, inplace=False).translate((x, y, z), inplace=False)
        out.append((m, c))
    return out


def vise_jaw_centre(at=(0.0, 0.0, 0.0), opening=150.0, axis="x"):
    """The point midway between the jaws at the jaw tops, and the jaw-top z."""
    x, y, z = map(float, at)
    L, H = VISE6["L"], VISE6["H"]
    c = L / 2 - 80 - opening / 2
    return (np.array([x + c, y, z + H]) if axis == "x" else np.array([x, y + c, z + H])), z + H


def rotary(at=(0.0, 0.0, 0.0), angle_deg=0.0, tail_x=None):
    """[(mesh, colour)] fixed parts and [(mesh, colour)] platter (turning with angle_deg about +x) of an HRT210 standing on the
    table with its A axis along +x at height at[2] + 152.4; `at` is the platter face centre projected on the table.
    tail_x: x of the tailstock's centre point (None: no tailstock)."""
    x, y, z = map(float, at)
    ch, pd, pt = HRT210["centre_h"], HRT210["platter_d"], HRT210["platter_t"]
    zc = z + ch
    housing = pv.Box((x - pt - 210, x - pt, y - 125, y + 125, z, zc + 125))
    foot = pv.Box((x - pt - 230, x - pt + 10, y - 150, y + 150, z, z + 18))
    motor = pv.Box((x - pt - 330, x - pt - 210, y - 70, y + 70, z + 30, zc + 60))
    fixed = [(housing, COL["rotary"]), (foot, COL["rotary"]), (motor, COL["rotary"])]
    platter = pv.Cylinder(center=(x - pt / 2, y, zc), direction=(1, 0, 0), radius=pd / 2, height=pt, resolution=64)
    slots = []
    for k in range(6):
        a = math.radians(60 * k)
        d = np.array([0, math.cos(a), math.sin(a)])
        c = np.array([x + 0.6, y, zc]) + d * 62
        s = pv.Box((-0.8, 0.8, -6, 6, -32, 32))
        Rk = np.eye(4)
        Rk[:3, :3] = _rx(60 * k)
        slots.append(s.transform(Rk, inplace=False).translate(c, inplace=False))
    turning = [(platter, COL["platter"]), (slots[0].merge(slots[1:]), COL["slot"])]
    if tail_x is not None:
        tb = pv.Box((tail_x + 20, tail_x + 160, y - 70, y + 70, z, zc + 45))
        tf = pv.Box((tail_x + 10, tail_x + 190, y - 95, y + 95, z, z + 16))
        quill = pv.Cylinder(center=(tail_x + 10, y, zc), direction=(1, 0, 0), radius=22, height=40)
        cone = pv.Cone(center=(tail_x - 15, y, zc), direction=(1, 0, 0), height=30, radius=16, resolution=32)
        fixed += [(tb, COL["rotary"]), (tf, COL["rotary"]), (quill, COL["jaw"]), (cone, COL["jaw"])]
    Mrot = rot_about_x(angle_deg, (x, y, zc))
    turning = [(m.transform(Mrot, inplace=False), c) for m, c in turning]
    return fixed, turning, np.array([x, y, zc])


def _rx(deg):
    a = math.radians(deg)
    return np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])


def rot_about_x(deg, c):
    M = np.eye(4)
    M[:3, :3] = _rx(deg)
    c = np.asarray(c, float)
    M[:3, 3] = c - M[:3, :3] @ c
    return M


def spindle(tool_d=19.05, stick=60.0, flute=None, holder="CT40"):
    """[(mesh, colour)] of the spindle nose, a CT40 holder with an ER32 nut and a flat end mill, in a local frame with
    the tool tip at the origin pointing down (-z). stick: tool length out of the collet nut."""
    flute = flute or min(stick - 8.0, 3.0 * tool_d)
    r = tool_d / 2
    tool_shank = pv.Cylinder(center=(0, 0, flute + (stick - flute) / 2), direction=(0, 0, 1), radius=r, height=stick - flute, resolution=32)
    tool_flute = pv.Cylinder(center=(0, 0, flute / 2), direction=(0, 0, 1), radius=r, height=flute, resolution=32)
    nut = pv.Cylinder(center=(0, 0, stick + 12), direction=(0, 0, 1), radius=25, height=24, resolution=48)
    body = pv.Cylinder(center=(0, 0, stick + 24 + 30), direction=(0, 0, 1), radius=22, height=60, resolution=48)
    flange = pv.Cylinder(center=(0, 0, stick + 24 + 60 + 8), direction=(0, 0, 1), radius=31.75, height=16, resolution=48)
    nose = pv.Cylinder(center=(0, 0, stick + 24 + 60 + 16 + 40), direction=(0, 0, 1), radius=70, height=80, resolution=48)
    head = pv.Box((-160, 160, -230, 140, stick + 24 + 60 + 16 + 80, stick + 24 + 60 + 16 + 520))
    return [(tool_flute, COL["tool"]), (tool_shank, "#b9c0c7"), (nut, COL["nut"]), (body, COL["holder"]), (flange, COL["holder"]),
            (nose, "#c3c9cf"), (head, COL["head"])]
