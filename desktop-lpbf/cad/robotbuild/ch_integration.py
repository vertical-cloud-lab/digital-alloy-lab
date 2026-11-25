"""Chapter 50-integration of the robot-built desktop LPBF video: the finished modules onto the VLM tray, the hoses and the
dock, and the leak check (about 75 s).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_integration.py

The scene ("the bay", mm, z up, the floor at z = 0) is lpbf_low.py's machine lifted so the VLM tray's floor is 857 mm
above the floor (byu-vcl PR 318's Kardex Shuttle XP 500: 2450 x 864 mm trays presented 100 mm behind the front face,
the 996 mm opening's header underside at 1829 mm; analysis/robot/cell.py's VLM numbers). The steps are sequence.py's
chapter 5, and every one of them is a person's:
  T01 the 84 kg process module off Fixture B onto the tray: a person and a lift table (84 kg is 3.4 times two UR12e
      payloads); the lift table drawn is the shop's scissor table (Vestil SCTAB-1000-2040-AC, 20 x 40 in, 1,000 lb,
      robot-shop-equipment.csv), turned so the module's 730 mm base sits along its 40 in. side;
  T02 the 19 in. rack and its units (UPS 23 kg, laser 40 kg, PC 8 kg, DIN drawer 9 kg): person + lift;
  T03 the gas module (scroll pump 26 kg, blower, filter, O2 box, argon manifold): person + lift;
  T04 KF-25 bellows, the vacuum valve, the argon and O2 lines: a person (hoses and wing-nut clamps);
  T05 the tray dock and the umbilicals: a person;
  T06 the leak check: the machine pumps down and holds, then the rate of rise (seals.md section 7).
The two arms stay parked at the VLM's face beside the opening (240 mm in front of it, as PR 318 parks them): none of
T01-T06 is planned for them, so no arm moves here. Times (proc_s) are estimates for a person with the lift and are shown time-lapsed; the
leak check's curve is the expected one (seals.md: pump-down to 1 mbar in about a minute, rise about 8e-4 mbar/min), not
a measurement.
"""
from __future__ import annotations

import hashlib
import math
import pickle
import sys
import time
from pathlib import Path

import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
CAD = HERE.parent
for p in (HERE, CAD):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import common  # noqa: E402
import hall as HL  # noqa: E402

FPS = common.FPS
NAME, TITLE = "50-integration", "Onto the VLM tray: rack, gas module, hoses, leak check"
TRAY_FLOOR = 857.0                       # byu-vcl PR 318: the presented tray's floor above the room floor
FACE_Y, SKIN = -532.0, 25.0              # the VLM's front face (machine frame y; the bay keeps x and y)
OPEN_X, HEADER_Z, TABLE_Z = 1250.0, 1829.0, 833.0
LIFT = dict(L=1016.0, W=508.0, base_h=110.0, top_t=45.0, lo=760.0)   # Vestil SCTAB-1000-2040-AC: 40 x 20 in platform
PERSON_KG = dict(module=84.0, rack=22.0, ups=23.0, laser=40.0, pump=26.2)


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return tuple(float(x) + (float(y) - float(x)) * u for x, y in zip(a, b))


def T(p):
    m = np.eye(4)
    m[:3, 3] = p
    return m


# ------------------------------------------------------------------------------------------------ the machine's meshes
def machine_meshes():
    """[(name, step, colour, opacity, explode, PolyData in the machine frame)] for every part of lpbf_low (M50), cached
    under /tmp/robotbuild/cache by the CAD's source hash."""
    h = hashlib.sha256()
    for f in sorted(CAD.glob("*.py")):
        h.update(f.read_bytes())
    path = common.ROOT / "cache" / f"integration-meshes-{h.hexdigest()[:16]}.pkl"
    if path.exists():
        raw = pickle.loads(path.read_bytes())
    else:
        import lpbf_low as M
        import render_low as R
        parts = M.build(module="M50")
        raw = []
        for p in parts:
            try:
                m = R.tess(p.shape, 0.4, 0.4)
            except Exception:                                        # noqa: BLE001
                m = None
            if m is None:
                continue
            raw.append((p.name, p.step, p.color, p.opacity, tuple(getattr(p, "explode", (0, 0, 0)) or (0, 0, 0)),
                        np.asarray(m.points, np.float32), np.asarray(m.faces)))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(pickle.dumps(raw))
    out = []
    for name, step, col, op, ex, P, F in raw:
        out.append((name, step, col, op, np.asarray(ex, float), pv.PolyData(np.asarray(P, float), F)))
    return out


RACK_FRONT = ("Operator panel", "E-stop", "Key switch", "Emission indicator", "Reset button")
UNITS = [("UPS (", "ups"), ("Fiber laser source", "laser"), ("Scan + laser controller", "pc"), ("DIN-rail drawer", "din")]


def group_of(name, step):
    """Which move a part arrives with."""
    if "VLM tray" in name:
        return "tray"
    if "Base plate, process" in name or "Leveling mounts, process" in name:
        return "proc"
    if "Base plate, gas" in name or "Leveling mounts, gas" in name:
        return "gasbase"
    if "19 in. rack frame" in name:
        return "rack"
    for key, g in UNITS:
        if key in name:
            return g
    if "Rack side panels" in name or name.startswith(RACK_FRONT):
        return "rackrest"
    if step in (3, 4, 5, 6, 7, 8, 9, 12):
        return "proc"
    if step == 10:
        return "gas:" + name.split(" (")[0]
    if step == 11:
        return "hoses"
    if step == 13:
        return "dock"
    return "proc"


# ------------------------------------------------------------------------------------------------ the bay
def vlm_meshes():
    """The Kardex's front around the opening, its sides, and the dark bay behind the presented tray (bay frame)."""
    out = []
    y0, y1 = FACE_Y, FACE_Y + SKIN
    X = 1950.0
    top = 3600.0
    light, dark, band = "#e3e6ea", "#3c4249", "#9aa3ad"
    for b in [(-X, -OPEN_X, y0, y1, 0, top), (OPEN_X, X, y0, y1, 0, top), (-OPEN_X, OPEN_X, y0, y1, HEADER_Z, top),
              (-OPEN_X, OPEN_X, y0, y1, 0, TABLE_Z - 30.0)]:
        out.append(("vlm front", pv.Box(bounds=b).triangulate(), light))
    out.append(("vlm header band", pv.Box(bounds=(-X, X, y0 - 4.0, y0, HEADER_Z, HEADER_Z + 95.0)).triangulate(), band))
    out.append(("vlm access table", pv.Box(bounds=(-OPEN_X, OPEN_X, y0 - 60.0, -432.0, TABLE_Z - 30.0, TABLE_Z)).triangulate(),
                "#b9c0c7"))
    for sx in (-1, 1):
        out.append(("vlm side", pv.Box(bounds=(sorted([sx * X, sx * (X - 30.0)]) + [y0, 3000.0, 0.0, top])).triangulate(), light))
    # the bay behind the opening: dark walls, so the tray reads against them
    out.append(("vlm bay", pv.Box(bounds=(-OPEN_X, OPEN_X, 700.0, 740.0, TABLE_Z - 30.0, HEADER_Z)).triangulate(), dark))
    for sx in (-1, 1):
        out.append(("vlm bay", pv.Box(bounds=(sorted([sx * OPEN_X, sx * (OPEN_X - 20.0)]) + [y1, 740.0, TABLE_Z - 30.0,
                                                                                            HEADER_Z])).triangulate(), dark))
    out.append(("vlm bay", pv.Box(bounds=(-OPEN_X, OPEN_X, y1, 740.0, HEADER_Z - 20.0, HEADER_Z)).triangulate(), dark))
    out.append(("vlm bay", pv.Box(bounds=(-OPEN_X, OPEN_X, y1, 740.0, TABLE_Z - 60.0, TABLE_Z - 30.0)).triangulate(), dark))
    return out


def lift_meshes(h):
    """A scissor lift table, platform top at h (bay frame, its own x along the 40 in. side), centred on the origin."""
    L, Wd = LIFT["L"], LIFT["W"]
    base = pv.Box(bounds=(-L / 2, L / 2, -Wd / 2, Wd / 2, 0.0, LIFT["base_h"]))
    top = pv.Box(bounds=(-L / 2, L / 2, -Wd / 2, Wd / 2, h - LIFT["top_t"], h))
    arms = []
    z0, z1 = LIFT["base_h"], h - LIFT["top_t"]
    for y in (-Wd / 2 + 30.0, Wd / 2 - 30.0):
        for a, b in (((-L / 2 + 60, z0), (L / 2 - 60, z1)), ((-L / 2 + 60, z1), (L / 2 - 60, z0))):
            p0, p1 = np.array([a[0], y, a[1]]), np.array([b[0], y, b[1]])
            d = p1 - p0
            arms.append(pv.Cylinder(center=(p0 + p1) / 2, direction=d, radius=18.0, height=float(np.linalg.norm(d)),
                                    resolution=12).triangulate())
    return base.triangulate().merge(top.triangulate()), arms[0].merge(arms[1:])


# ------------------------------------------------------------------------------------------------ the chapter
def main():
    import people
    t0 = time.time()
    pl = common.plotter()
    sc = HL.pvscene.PVScene(pl)
    sc.add("floor", pv.Plane(center=(0.0, 0.0, -1.0), i_size=16000.0, j_size=16000.0), common.FLOOR, specular=0.0)
    for k, (nm, m, col) in enumerate(vlm_meshes()):
        sc.add(f"{nm}/{k}", m, col, specular=0.15, ambient=0.45 if col == "#e3e6ea" else 0.22)
    Z0 = TRAY_FLOOR - (-212.0)                           # machine z -> bay z (lpbf_low.Z_TRAY = -212)
    groups = {}
    ex = {}
    zmin = {}
    for k, (name, step, col, op, xpl, mesh) in enumerate(machine_meshes()):
        g = group_of(name, step)
        groups.setdefault(g, []).append(name)
        ex.setdefault(g, xpl)
        m = mesh.translate((0.0, 0.0, Z0), inplace=False)
        zmin[g] = min(zmin.get(g, 1e9), float(m.bounds[4]))
        sc.add(f"m/{k}", m, col, group=g, opacity=op, specular=0.3)
    print(f"machine: {sum(len(v) for v in groups.values())} parts in {len(groups)} moves, {time.time() - t0:.0f} s",
          flush=True)
    gas_groups = sorted(g for g in groups if g.startswith("gas:"))

    def show(g, on):
        for n in sc.members(g):
            sc.alpha[n] = 1.0 if on else 0.0
    for g in groups:
        if g != "tray":
            show(g, False)
    # the lift table
    lt_h = [LIFT["lo"]]
    body, arms = lift_meshes(LIFT["lo"])
    sc.add("lift/body", body, "#2f6db5", group="lift", specular=0.3)
    sc.add("lift/arms", arms, "#5f6870", group="lift", specular=0.3)

    def lift_at(x, y, h):
        if abs(h - lt_h[0]) > 0.5:
            b, a = lift_meshes(h)
            sc.add("lift/body", b, "#2f6db5", group="lift", specular=0.3)
            sc.add("lift/arms", a, "#5f6870", group="lift", specular=0.3)
            lt_h[0] = h
        sc.gmat["lift"] = T((x, y, 0.0))
    # the robots, parked at the VLM face (PR 318: arm base 240 mm in front of it)
    import cell2 as K
    for tag, x in (("A", -2550.0), ("B", 2550.0)):
        arm = K.ArmT(tag, x, "front")                    # both on the VLM's face, the arm towards it
        arm.move_base(x)
        arm.q = arm.park_q()
        arm.place()
        av = HL.ArmVis(sc, arm, "r" + tag)
        mv = HL.MirVis(sc, "r" + tag, "front")
        mv.at(x)
        shift = (FACE_Y - 240.0) - (-K.ARM_Y)           # cell2's front lane (arm at y = -640) to 240 mm off the face
        sc.gmat["shift" + tag] = T((0.0, shift, 0.0))
        for g in list(sc.gmat):
            if g.startswith(("r" + tag + "/", "mirr" + tag)):
                sc.parent[g] = "shift" + tag
    op = people.Person(sc, "op", gloves=True)
    ch = common.Chapter(NAME, TITLE)
    clock = dict(t=0.0)

    def frame(cam, caption, sub, who, step, status="person", proc_s=0.0, add=None, labels=(), chart=None, va=30.0):
        img = sc.render(cam, va)
        labs = []
        for text, p in labels:
            (x, y), = common.project(pl, [p])
            if 0 <= x <= common.W and 70 <= y <= common.H - 30:
                labs.append([round(x, 1), round(y, 1), text])
        meta = dict(sub=sub, who=who, step=step, status=status, proc_s=proc_s, labels=labs)
        if add:
            meta["add"] = add
        if chart:
            meta["chart"] = chart
        ch.frame(img, caption, **meta)

    def cam_at(f, d, az, el):
        return [HL.orbit(f, d, az, el), f, (0.0, 0.0, 1.0)]

    # 1. the empty tray at the face of the VLM; the process module waits on the lift table
    ym_final = -25.0                                     # the process module's base-plate centre on the tray (y)
    xm = -55.0
    ly = -432.0 - LIFT["W"] / 2 - 10.0                   # lift table centre: its far edge 10 mm short of the tray's
    feet0 = LIFT["lo"]                                   # module feet on the platform at its transport height
    sc.gmat["proc"] = T((0.0, ly - ym_final, feet0 - TRAY_FLOOR))
    show("proc", True)
    lift_at(xm, ly, LIFT["lo"])
    py = ly - LIFT["W"] / 2 - 380.0
    op.set(x=xm + 520.0, y=py + 120.0, hd=-15.0, amp=0.0, hands={"l": None, "r": None}, look=(xm, ly, 1100.0))
    F1 = (0.0, -300.0, 1000.0)
    c1 = cam_at(F1, 5600.0, -32.0, 20.0)
    c2 = cam_at(F1, 5000.0, -22.0, 18.0)
    n = 5 * FPS
    for i in range(n):
        u = ease(i / (n - 1))
        frame([lerp(c1[0], c2[0], u), lerp(c1[1], c2[1], u), (0, 0, 1)],
              "T01: the 84 kg process module to the VLM tray: a person and a lift table",
              "84 kg is 3.4 times two UR12e payloads. Kardex tray 2450 x 864 mm, floor 857 mm up; both arms parked "
              "beside the opening (sequence.py: T01-T05 are person steps)",
              ["person"], "T01", proc_s=0.0, labels=[("VLM tray, 857 mm", (900.0, -300.0, TRAY_FLOOR)),
                                                                   ("lift table", (xm + 300.0, ly - 200.0, LIFT["lo"]))])
    # 2. up to the tray's height, then pushed onto it
    n = 4 * FPS
    for i in range(n):
        u = ease(i / (n - 1))
        h = LIFT["lo"] + (TRAY_FLOOR + 3.0 - LIFT["lo"]) * u
        lift_at(xm, ly, h)
        sc.gmat["proc"] = T((0.0, ly - ym_final, h - TRAY_FLOOR))
        op.set(hands={"r": (xm + 330.0, py + 380.0, 1050.0), "l": None}, look=(xm, ly, h + 200.0))
        frame(c2, "T01: the lift table raises the module to the tray's floor (857 mm)",
              "The shop's scissor table (Vestil SCTAB-1000-2040-AC, 20 x 40 in, 1,000 lb; robot-shop-equipment.csv), "
              "turned so the 730 mm base sits along its 40 in. side", ["person"], "T01",
              proc_s=180.0 / n, add=dict(person_h=180.0 / n / 3600.0))
    # walk behind it and push it in
    n = 2 * FPS
    p0 = (xm + 520.0, py + 120.0)
    p1 = (xm, py - 60.0)
    for i in range(n):
        u = ease(i / (n - 1))
        x, y = lerp(p0, p1, u)
        op.set(x=x, y=y, hd=-15.0 * (1 - u), amp=0.8 * math.sin(math.pi * u), phase=2 * math.pi * 900.0 * u / people.Person.STRIDE,
               hands={"l": None, "r": None}, look=(xm, ly + 300.0, 1000.0))
        frame(c2, "T01: the person pushes the module off the lift table onto the tray",
              "It slides on its four levelling mounts (McMaster 5537T983); the mounts are threaded down on the tray",
              ["person"], "T01", proc_s=60.0 / n, add=dict(person_h=60.0 / n / 3600.0))
    d_push = ym_final - ly
    n = 5 * FPS
    back = -265.0 - (-25.0)                              # base plate's back edge from its centre (y)
    c3 = cam_at((0.0, -200.0, 1000.0), 4300.0, -50.0, 16.0)
    for i in range(n):
        u = ease(i / (n - 1))
        yc = ly + d_push * u
        sc.gmat["proc"] = T((0.0, yc - ym_final, 3.0 * (1 - u)))
        edge = yc + back
        stand = min(edge - 520.0, ly - LIFT["W"] / 2 - 70.0)  # behind the lift table, reaching over it at the end
        op.set(x=xm, y=stand, hd=0.0, amp=0.5 if edge - 520.0 < stand + 1.0 else 0.0,
               phase=2 * math.pi * (900.0 + min(d_push * u, 380.0)) / people.Person.STRIDE,
               lean=18.0 + 14.0 * max(0.0, u - 0.5) * 2, hands={"l": (xm - 220.0, edge - 12.0, 925.0), "r": (xm + 220.0, edge - 12.0, 925.0)},
               look=(xm, edge + 300.0, 950.0))
        frame([lerp(c2[0], c3[0], u), lerp(c2[1], c3[1], u), (0, 0, 1)],
              "T01: the process module on the VLM tray",
              f"Pushed {d_push:.0f} mm in on its mounts; then levelled (sequence.py T01: person + hoist or lift table)",
              ["person"], "T01", proc_s=600.0 / n, add=dict(person_h=600.0 / n / 3600.0))
    # 3. the rack and its units, with the lift table
    op.set(amp=0.0, lean=0.0, hands={"l": None, "r": None})
    xr = (-990.0 - 430.0) / 2
    c4 = cam_at((-700.0, -250.0, 1150.0), 3500.0, -38.0, 14.0)
    lift_at(xr, ly, TRAY_FLOOR + 3.0)
    show("rack", True)
    n = 3 * FPS
    for i in range(n):
        u = ease(i / (n - 1))
        sc.gmat["rack"] = T((0.0, (ly - 0.0) * (1 - u), 3.0 * (1 - u)))
        op.set(x=xr + 80.0, y=ly - LIFT["W"] / 2 - 420.0 + 300.0 * u, hd=0.0, amp=0.5 * math.sin(math.pi * u),
               phase=2 * math.pi * 300.0 * u / people.Person.STRIDE, lean=12.0 * u,
               hands={"l": (xr - 150.0, -300.0 + (ly) * (1 - u) - 15.0, 1250.0),
                      "r": (xr + 150.0, -300.0 + (ly) * (1 - u) - 15.0, 1250.0)} if u > 0.2 else {"l": None, "r": None},
               look=(xr, -100.0, 1200.0))
        frame([lerp(c3[0], c4[0], u), lerp(c3[1], c4[1], u), (0, 0, 1)],
              "T02: the 12U rack (22 kg) onto the tray's left end, from the lift table",
              "19 in. 4-post rack, 560 mm tall: the UPS, laser, PC and DIN drawer go in it next",
              ["person"], "T02", proc_s=600.0 / n, add=dict(person_h=600.0 / n / 3600.0))
    for g, kg, label in (("ups", 23.0, "UPS (Eaton 5PX, 2U), 23 kg"), ("laser", 40.0, "fiber laser (IPG YLR-500, 4U), 40 kg"),
                         ("pc", 8.0, "controller PC with the RTC6 (2U), 8 kg"), ("din", 9.0, "DIN-rail drawer (4U), 9 kg")):
        if g not in groups:
            continue
        show(g, True)
        e = np.array(ex.get(g, (0.0, -400.0, 0.0)), float)
        if np.linalg.norm(e) < 1:
            e = np.array([0.0, -400.0, 0.0])
        lift_at(xr, ly, zmin.get(g, TRAY_FLOOR) - 2.0)
        n = int(2.5 * FPS)
        for i in range(n):
            u = ease(i / (n - 1))
            sc.gmat[g] = T(tuple(e * (1 - u)))
            op.set(x=xr + 40.0, y=-532.0 - 560.0 + 0.0 * u, hd=0.0, lean=14.0, amp=0.0,
                   hands={"l": (xr - 160.0, -300.0 + e[1] * (1 - u) - 20.0, 1000.0),
                          "r": (xr + 160.0, -300.0 + e[1] * (1 - u) - 20.0, 1000.0)},
                   look=(xr, -250.0, 1000.0))
            who = ["person"]
            frame(c4, f"T02: the {label} slides into the rack",
                  "On the lift table at the slot's height: " + ("over a UR12e's 12.5 kg payload" if kg > 12.5 else
                                                                 "light enough for an arm, but the rack's slides and cage "
                                                                 "nuts need a person's hands (not planned for the arms)"),
                  who, "T02", proc_s=420.0 / n, add=dict(person_h=420.0 / n / 3600.0))
    show("rackrest", True)
    # 4. the gas module
    xg = (400.0 + 990.0) / 2
    c5 = cam_at((650.0, -200.0, 1100.0), 3400.0, -20.0, 18.0)
    lift_at(xg, ly, TRAY_FLOOR + 3.0)
    show("gasbase", True)
    n = int(2.5 * FPS)
    for i in range(n):
        u = ease(i / (n - 1))
        sc.gmat["gasbase"] = T((0.0, ly * (1 - u), 0.0))
        op.set(x=xg - 60.0, y=-532.0 - 600.0, hd=0.0, lean=14.0, amp=0.0,
               hands={"l": (xg - 250.0, -250.0 + ly * (1 - u) - 15.0, 935.0), "r": (xg + 250.0, -250.0 + ly * (1 - u) - 15.0, 935.0)},
               look=(xg, -200.0, 950.0))
        frame([lerp(c4[0], c5[0], u), lerp(c4[1], c5[1], u), (0, 0, 1)],
              "T03: the gas module's MIC-6 base plate onto the tray's right end", "On its four levelling mounts",
              ["person"], "T03", proc_s=300.0 / n, add=dict(person_h=300.0 / n / 3600.0))
    for g in gas_groups:
        show(g, True)
        nm = g.split(":", 1)[1]
        heavy = "pump" in nm.lower()
        n = int((2.2 if heavy else 1.0) * FPS)
        for i in range(n):
            u = ease(i / (n - 1))
            sc.gmat[g] = T((0.0, -450.0 * (1 - u), 0.0))
            op.set(x=xg - 60.0, y=-532.0 - 600.0, hd=0.0, lean=14.0, amp=0.0,
                   hands={"l": (xg - 120.0, -480.0 - 450.0 * (1 - u) + 200.0, 1000.0),
                          "r": (xg + 120.0, -480.0 - 450.0 * (1 - u) + 200.0, 1000.0)},
                   look=(xg, -200.0, 1000.0))
            frame(c5, f"T03: {nm}" + (" (26 kg, from the lift table)" if heavy else ""),
                  "Gas module: dry scroll pump, sealed blower, cyclone + HEPA, O2 / dew-point box, argon manifold "
                  "and regulator (their screws are not drawn)", ["person"], "T03",
                  proc_s=(600.0 if heavy else 240.0) / n, add=dict(person_h=(600.0 if heavy else 240.0) / n / 3600.0))
    # 5. hoses and lines, then the dock
    c6 = cam_at((300.0, -100.0, 1100.0), 3800.0, -10.0, 30.0)
    lift_at(3000.0, -3000.0, LIFT["lo"])                  # the lift table rolled away
    for g, cap, sub, secs, step in (
            ("hoses", "T04: KF-25 bellows, the vacuum valve, the argon and O2 lines",
             "Hoses and wing-nut clamps are a person's job (deformable parts; sequence.py T04)", 2700.0, "T04"),
            ("dock", "T05: the tray dock, the umbilicals and the power box",
             "Power, Ethernet, argon, water and exhaust mate sideways at the tray's back-right corner", 1200.0, "T05")):
        if g not in groups:
            continue
        show(g, True)
        e = np.array(ex.get(g, (0.0, 0.0, 200.0)), float)
        if np.linalg.norm(e) < 1:
            e = np.array([0.0, 0.0, 200.0])
        n = 4 * FPS
        for i in range(n):
            u = ease(i / (n - 1))
            sc.gmat[g] = T(tuple(e * (1 - u)))
            op.set(x=250.0 + 400.0 * math.sin(math.pi * u), y=-532.0 - 520.0, hd=0.0, lean=20.0, amp=0.0,
                   hands={"l": (250.0 + 400.0 * math.sin(math.pi * u) - 120.0, -420.0, 1050.0),
                          "r": (250.0 + 400.0 * math.sin(math.pi * u) + 120.0, -420.0, 1050.0)},
                   look=(300.0, -200.0, 1000.0))
            frame([lerp(c5[0], c6[0], u), lerp(c5[1], c6[1], u), (0, 0, 1)] if g == "hoses" else c6, cap, sub,
                  ["person"], step, proc_s=secs / n, add=dict(person_h=secs / n / 3600.0))
    # 6. the leak check: pump down, hold, isolate, the rate of rise (expected values, seals.md section 7)
    op.set(x=-1300.0 + 2600.0, y=-1700.0, hd=-30.0, lean=0.0, amp=0.0, hands={"l": None, "r": None},
           look=(0.0, -100.0, 1100.0))
    ts = list(np.linspace(0.0, 75.0, 151))

    def p_of(t):
        if t <= 1.2:
            return 1000.0 * math.exp(-t / 1.2 * math.log(1000.0))          # to 1 mbar in 1.2 min (seals.md: 0.9-1.2)
        if t <= 64.0:
            return max(0.05, 1.0 * math.exp(-(t - 1.2) / 6.0))             # down to the scroll pump's ~0.05 mbar
        return 0.05 + 8e-4 * (t - 64.0)                                   # valve closed: 8e-4 mbar/min expected
    ps = [p_of(t) for t in ts]
    c7 = cam_at((-50.0, -100.0, 1150.0), 2600.0, -18.0, 22.0)
    n = 10 * FPS
    for i in range(n):
        u = i / (n - 1)
        k = int(round(u * (len(ts) - 1)))
        t_min = ts[k]
        phase = "pumping down" if t_min < 1.2 else ("holding at <= 1 mbar" if t_min < 64.0 else "valve closed: rate of rise")
        val = f"{ps[k]:.3g} mbar at {t_min:.0f} min"
        verdict = ""
        if t_min >= 74.0:
            val = "rise 8e-4 mbar/min"
            verdict = "pass"
        frame([lerp(c6[0], c7[0], ease(u * 3)), lerp(c6[1], c7[1], ease(u * 3)), (0, 0, 1)],
              f"T06: the leak check, {phase}",
              "After >= 1 h at <= 1 mbar the valve closes and the Pirani is read for 10 min; pass under 1e-3 mbar/min "
              "(seals.md section 7). Expected values, not a measurement; then the O2 drift at +20 mbar argon",
              ["machine"], "T06", status=verdict or "", proc_s=75.0 * 60.0 / n, add=dict(machine_h=75.0 / 60.0 / n),
              chart=dict(title="Chamber pressure, expected", x=ts, y=ps, now=k, ylog=True, xlabel="minutes",
                         ylabel="mbar", xticks=[0, 15, 30, 45, 60, 75], ref=1.0, ref_label="1 mbar",
                         value=val, verdict=verdict))
    # 7. a last look
    n = 5 * FPS
    c8 = cam_at((0.0, -100.0, 1100.0), 5200.0, -40.0, 18.0)
    for i in range(n):
        u = ease(i / (n - 1))
        frame([lerp(c7[0], c8[0], u), lerp(c7[1], c8[1], u), (0, 0, 1)],
              "The desktop LPBF on its VLM tray, ready for its first build",
              "Process module, 12U rack and gas module side by side on one 2450 x 864 mm tray; the tray goes back "
              "into the Kardex", [], "", status="", proc_s=0.0)
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s) in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
