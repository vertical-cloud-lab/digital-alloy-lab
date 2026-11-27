"""Chapter 50-integration of the robot-built desktop LPBF video: the finished modules onto the VLM tray, the hoses and the
dock, and the leak check (about 85 s).

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

Round 8 (Sterling, 2026-11-26: "moonwalk, motion sickness, collisions and interference"): fixed cameras or slow drifts,
cuts between them, every shot at least 4 s. Round 9 (2026-11-27): people.py locks the stance foot (its Gait), so the person
now walks on screen: from the lift table's handle round its end to push the module, along the access table to the hoses
and the dock, and back from the tray for the leak check (walk.py checks every stance); a place change that a time-lapse
covers (the lift table reloaded) is still a cut. The process fiber is lpbf_low.py's round-9 route (laser rear panel, the
rack's side slot, R 75-77) and appears with the hoses at T04, once the laser is in; the rack frame is 580 mm, so the 4U
drawer slides in under its top rails. Loads slide 26 mm over the tray floor (its rim is
20 mm high) and settle; the lift table stands in front of the VLM's access table (its platform can't pass over it); the
person stands 850 mm in front of the tray's edge at the access table, or behind the lift table, and pushes on the guard
frame's posts, the rack's posts, the units' front panels and the base plates' edges with the fingertips (people.py's wrists
don't bend, so the palm stays 135 mm off what it pushes, the fingers flat). The frames are recorded with ROBOTBUILD_AUDIT=1 and checked by
scene_audit.py (collisions over 1.5 mm) and walk.py (foot slip, gliding).
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
import people  # noqa: E402

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
    if name.startswith("Process fiber"):        # round 9: connected once the laser is in, with the hoses and lines (T04);
        return "hoses"                          # with the process module it stood in the rack's path as the rack came in
    if "Base plate, process" in name or "Leveling mounts, process" in name:
        return "proc"
    if "Base plate, gas" in name or "Leveling mounts, gas" in name:
        return "gasbase"
    if "19 in. rack frame" in name:
        return "rack"
    for key, g in UNITS:
        if key in name:
            return g
    if name.startswith("E-stop") and "gas module" in name:      # on the O2 box's front: it comes with the O2 box
        return "gas:Trace O2 analyzer + dew-point transmitter"
    if name.startswith("E-stop") and "guard" in name:           # on the process module's guard
        return "proc"
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


def lift_handle():
    """The lift table's push handle on its -x end (on the base, so it doesn't rise): two uprights and a bar at 990 mm."""
    L, Wd = LIFT["L"], LIFT["W"]
    x = -L / 2 - 60.0
    parts = []
    for y in (-Wd / 2 + 40.0, Wd / 2 - 40.0):
        parts.append(pv.Cylinder(center=(x, y, 525.0), direction=(0, 0, 1), radius=14.0, height=930.0, resolution=16))
        parts.append(pv.Cylinder(center=(x + 30.0, y, 80.0), direction=(1, 0, 0), radius=14.0, height=60.0, resolution=16))
    parts.append(pv.Cylinder(center=(x, 0.0, 990.0), direction=(0, 1, 0), radius=14.0, height=Wd - 80.0 + 28.0,
                             resolution=16))
    m = parts[0].triangulate()
    return m.merge([q.triangulate() for q in parts[1:]])


# ------------------------------------------------------------------------------------------------ the person
def wrap(a):
    return (a + 180.0) % 360.0 - 180.0


class Mover:
    """Moves people.Person along a path, one pose a frame (round 9). Since round 9 people.py locks the feet itself (its
    Gait plants each foot on a footprint and steps it when the body moves away; walk.py checks it), so a walk here is
    only the body's path: turn on the spot towards the leg (the feet step round), walk it with an ease in and out at a
    careful 0.66 m/s, turn to the heading wanted. Every method is a generator that poses the person and yields once per
    frame; ``place`` is for a cut."""

    V = 55.0             # mm a frame (0.66 m/s): a careful walk in a machine bay
    TURN_STEP = 6.0      # deg a frame turning on the spot (72 deg/s: the feet take a step every ~0.6 s)

    def __init__(self, op, x, y, hd):
        self.op, self.x, self.y, self.hd = op, float(x), float(y), float(hd)
        self.arm = dict(hands={"l": None, "r": None}, lean=0.0, look=None, grip={"l": 0.3, "r": 0.3},
                        palm={"l": None, "r": None})
        self.walked = 0.0

    def place(self, x, y, hd):
        """Across a cut only: both feet planted at the new place."""
        self.x, self.y, self.hd = float(x), float(y), float(hd)
        self.op.place(x=self.x, y=self.y, hd=self.hd, **self.arm)

    def pose(self, **kw):
        for k, v in kw.items():
            if k in ("hands", "grip", "palm"):
                self.arm[k] = dict(self.arm[k], **v)
            else:
                self.arm[k] = v
        self.op.set(x=self.x, y=self.y, hd=self.hd, **self.arm)

    def turn_to(self, hd1, **kw):
        d = wrap(hd1 - self.hd)
        n = int(math.ceil(abs(d) / self.TURN_STEP))
        h0 = self.hd
        for k in range(n):
            self.hd = h0 + d * ease((k + 1) / n)
            self.pose(**kw)
            yield
        self.hd = h0 + d
        self.pose(**kw)

    def walk_path(self, pts, hd_end=None, v=None, face=None, **kw):
        """Walk through the waypoints pts [(x, y)] on a smooth curve (Catmull-Rom), heading along it (or keeping `face`
        for a few side or back steps), easing in and out; then turn to hd_end."""
        v = v or self.V
        P = np.array([(self.x, self.y)] + [tuple(p) for p in pts], float)
        keep = [0] + [i for i in range(1, len(P)) if np.linalg.norm(P[i] - P[i - 1]) > 1.0]
        P = P[keep]
        if len(P) >= 2:
            E = np.r_[[2 * P[0] - P[1]], P, [2 * P[-1] - P[-2]]]
            C = []
            for i in range(1, len(E) - 2):
                p0, p1, p2, p3 = E[i - 1], E[i], E[i + 1], E[i + 2]
                for t in np.linspace(0.0, 1.0, 24, endpoint=False):
                    C.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
            C.append(P[-1])
            C = np.array(C)
            seg = np.linalg.norm(np.diff(C, axis=0), axis=1)
            s_c = np.r_[0.0, np.cumsum(seg)]
            L = float(s_c[-1])
            t0 = C[min(3, len(C) - 1)] - C[0]
            head0 = math.degrees(math.atan2(-t0[0], t0[1])) if face is None else face
            if abs(wrap(head0 - self.hd)) > 4.0:
                yield from self.turn_to(head0, **kw)
            n = max(8, int(math.ceil(L / v)) + 10)              # eased over 10 frames each end (0.8 s): the feet keep up
            w = np.array([min(1.0, (k + 1) / 10.0, (n - k) / 10.0) for k in range(n)])
            s_k = np.cumsum(w / w.sum() * L)
            for s in s_k:
                x = float(np.interp(s, s_c, C[:, 0]))
                y = float(np.interp(s, s_c, C[:, 1]))
                if face is None:
                    j = min(int(np.searchsorted(s_c, s)), len(C) - 1)
                    tg = C[min(j + 1, len(C) - 1)] - C[max(j - 1, 0)]
                    if np.linalg.norm(tg) > 1e-6:
                        self.hd = self.hd + wrap(math.degrees(math.atan2(-tg[0], tg[1])) - self.hd)
                self.walked += math.hypot(x - self.x, y - self.y)
                self.x, self.y = x, y
                self.pose(**kw)
                yield
        if hd_end is not None and abs(wrap(hd_end - self.hd)) > 1.0:
            yield from self.turn_to(hd_end, **kw)
        self.pose(**kw)

    def walk_to(self, x1, y1, hd_end=None, v=None, face=None, **kw):
        yield from self.walk_path([(x1, y1)], hd_end=hd_end, v=v, face=face, **kw)

    def stand(self, n, **kw):
        for _ in range(n):
            self.pose(**kw)
            yield


def nearest(sc, group, p):
    """The point of a group's drawn meshes (world) nearest p: where a hand goes, so it rests on something drawn."""
    best, bd = None, 1e18
    M = sc.world(group)
    p = np.asarray(p, float)
    for nm in sc.members(group):
        P = np.asarray(sc.actors[nm].GetMapper().GetInput().GetPoints().GetData())
        if not len(P):
            continue
        W = P @ M[:3, :3].T + M[:3, 3]
        i = int(np.argmin(np.sum((W - p) ** 2, axis=1)))
        d = float(np.sum((W[i] - p) ** 2))
        if d < bd:
            best, bd = W[i], d
    return tuple(best) if best is not None else tuple(p)


# ------------------------------------------------------------------------------------------------ the chapter
def main():
    t0 = time.time()
    pl = HL.pvscene.plotter()
    sc = HL.pvscene.PVScene(pl)
    sc.add("floor", pv.Plane(center=(0.0, 0.0, -1.0), i_size=16000.0, j_size=16000.0), common.FLOOR, specular=0.0)
    for k, (nm, m, col) in enumerate(vlm_meshes()):
        sc.add(f"{nm}/{k}", m, col, specular=0.15, ambient=0.45 if col == "#e3e6ea" else 0.22)
    Z0 = TRAY_FLOOR - (-212.0)                           # machine z -> bay z (lpbf_low.Z_TRAY = -212)
    groups, bounds = {}, {}
    for k, (name, step, col, op, xpl, mesh) in enumerate(machine_meshes()):
        g = group_of(name, step)
        groups.setdefault(g, []).append(name)
        m = mesh.translate((0.0, 0.0, Z0), inplace=False)
        b = np.array(m.bounds)
        bounds[g] = b if g not in bounds else np.r_[np.minimum(bounds[g][::2], b[::2]),
                                                     np.maximum(bounds[g][1::2], b[1::2])][[0, 3, 1, 4, 2, 5]]
        sc.add(f"m/{k} {name.split(' (')[0].replace('/', '-')[:48]}", m, col, group=g, opacity=op, specular=0.3)
    print(f"machine: {sum(len(v) for v in groups.values())} parts in {len(groups)} moves, {time.time() - t0:.0f} s",
          flush=True)
    gas_groups = sorted(g for g in groups if g.startswith("gas:"))

    def show(g, a):
        for n in sc.members(g):
            sc.alpha[n] = float(a)
    for g in groups:
        if g != "tray":
            show(g, 0.0)
    lt_h = [None]

    def lift_at(x, y, h, shown=True):
        if lt_h[0] is None or abs(h - lt_h[0]) > 0.5:
            b, a = lift_meshes(h)
            sc.add("lift/body", b, "#2f6db5", group="lift", specular=0.3)
            sc.add("lift/arms", a, "#5f6870", group="lift", specular=0.3)
            sc.add("lift/handle", lift_handle(), "#3d4247", group="lift", specular=0.3)
            lt_h[0] = h
        sc.gmat["lift"] = T((x, y, 0.0))
        for nm in ("lift/body", "lift/arms", "lift/handle"):
            sc.alpha[nm] = 1.0 if shown else 0.0
    # the robots, parked at the VLM face (PR 318: arm base 240 mm in front of it)
    import cell2 as K
    for tag, x in (("A", -2550.0), ("B", 2550.0)):
        arm = K.ArmT(tag, x, "front")                    # both on the VLM's face, the arm towards it
        arm.move_base(x)
        arm.q = arm.park_q()
        arm.place()
        HL.ArmVis(sc, arm, "r" + tag)
        mv = HL.MirVis(sc, "r" + tag, "front")
        mv.at(x)
        shift = (FACE_Y - 240.0) - (-K.ARM_Y)           # cell2's front lane (arm at y = -640) to 240 mm off the face
        sc.gmat["shift" + tag] = T((0.0, shift, 0.0))
        for g in list(sc.gmat):
            if g.startswith(("r" + tag + "/", "mirr" + tag)):
                sc.parent[g] = "shift" + tag
    op = people.Person(sc, "op", gloves=True)
    ch = common.Chapter(NAME, TITLE)

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

    def shot(cam0, cam1, gen, n_min, caption, sub, step, secs, labels=(), who=("person",), status="person"):
        """Render a frame per yield of `gen` (and at least n_min frames, the person as last posed): the camera drifts from
        cam0 to cam1 over the first n_min frames, then holds (a fixed shot when they are the same). `secs` of person time
        are spread over n_min frames (rescale_meta() then makes each step's total hud.json's)."""
        gen = iter(gen) if gen is not None else iter(())
        i, live = 0, True
        while True:
            if live:
                try:
                    next(gen)
                except StopIteration:
                    live = False
            if not live and i >= n_min:
                break
            u = ease(min(1.0, i / max(1, n_min - 1)))
            c = [lerp(cam0[0], cam1[0], u), lerp(cam0[1], cam1[1], u), (0.0, 0.0, 1.0)]
            frame(c, caption, sub, list(who), step, status=status, proc_s=secs / n_min,
                  add=dict(person_h=secs / n_min / 3600.0) if "person" in who else None, labels=labels)
            i += 1
        return i

    # ---------------------------------------------------------------- where things are (bay frame)
    ly = -600.0 - LIFT["W"] / 2       # lift table centre: its far edge 8 mm in front of the VLM's access table (y -592;
                                      # its platform, 815-860 mm, can't pass over the table's 803-833)
    y_back = ly - LIFT["W"] / 2 - 230.0   # the person behind the lift table (toes 80 mm off its base)
    y_front = -850.0                  # the person at the access table (toes ~130 mm off the VLM's front skin, legs clear of
                                      # the table: the round-8 audit found shoes and thighs in them at -745)
    LIP = 26.0                        # loads slide with their feet 26 mm over the tray floor: the tray's rim is 20 mm high
    h0, h1 = LIFT["lo"], TRAY_FLOOR + LIP
    FWD = (0.0, 1.0, 0.0)             # palms turned to the load
    TIP = 135.0                       # people.py's wrists don't bend, so the fingers point along the forearm: the palm's
                                      # centre stays this far in front of the face pushed, the fingertips on it (the round-8
                                      # audit found fingers 70-100 mm inside the loads with the palm 16 mm off, 40 at 105 mm)
    REACH = {"chest": 640.0, "low": 570.0}

    def push(pl_, pr_, **kw):
        return dict(hands={"l": pl_, "r": pr_}, palm={"l": FWD, "r": FWD}, grip={"l": 0.05, "r": 0.05}, **kw)   # flat fingers

    def free(**kw):
        return dict(hands={"l": None, "r": None}, palm={"l": None, "r": None}, grip={"l": 0.3, "r": 0.3}, **kw)

    def check_reach(who, pts):
        """Warn when a hand target is beyond the reach used here, measured from its own shoulder (190 mm to the side)."""
        c, s_ = math.cos(math.radians(m.hd)), math.sin(math.radians(m.hd))
        for side, p in zip(("l", "r"), pts):
            sx = -190.0 if side == "l" else 190.0
            sh = (m.x + sx * c, m.y + sx * s_)
            d = math.hypot(p[0] - sh[0], p[1] - sh[1])
            lim = REACH["chest"] if p[2] > 1050.0 else REACH["low"]
            if d > lim + 1.0:
                print(f"  reach: {who} {side} {d:.0f} mm ahead of the shoulder (limit {lim:.0f})", flush=True)

    # ---------------------------------------------------------------- T01: the process module, person + lift table
    xm = -55.0                                            # the process module's base plate centre (x)
    POST = {"l": -410.0, "r": 300.0}                      # the guard frame's front posts (x); their front face y = -265
    off0 = ly - (-25.0)                                   # the module rides on the lift table, centred on it
    lift_at(xm, ly, h0)
    sc.gmat["proc"] = T((0.0, off0, h0 - TRAY_FLOOR))
    show("proc", 1.0)
    hx = xm - LIFT["L"] / 2 - 60.0                        # the handle's bar (x)
    m = Mover(op, hx - 320.0, ly, -90.0)                  # at the handle, facing the table (+x)
    grip = dict(hands={"l": (hx - 30.0, ly + 150.0, 990.0 + 34.0), "r": (hx - 30.0, ly - 150.0, 990.0 + 34.0)},
                palm={"l": "down", "r": "down"}, grip={"l": 0.35, "r": 0.35})
    m.pose(lean=6.0, look=(xm, ly, 1000.0), **grip)
    a1 = cam_at((0.0, -450.0, 1050.0), 5600.0, -32.0, 19.0)
    b1 = cam_at((0.0, -450.0, 1050.0), 5380.0, -28.0, 19.0)
    labs1 = [("VLM tray, 857 mm", (900.0, -300.0, TRAY_FLOOR)), ("lift table", (xm + 300.0, ly - 200.0, LIFT["lo"]))]
    shot(a1, b1, None, 6 * FPS, "T01: the 84 kg process module to the VLM tray: a person and a lift table",
         "84 kg is 3.4 times two UR12e payloads. Kardex tray 2450 x 864 mm, floor 857 mm up; both arms parked beside "
         "the opening (sequence.py: T01-T05 are person steps)", "T01", 120.0, labels=labs1)
    c2 = cam_at((-300.0, -850.0, 1000.0), 4300.0, 30.0, 16.0)      # from the right: the person at the handle stays in view
    c2b = cam_at((-300.0, -850.0, 1000.0), 4200.0, 27.0, 16.0)

    def raise_lift(n):
        for i in range(n):
            u = ease(i / (n - 1))
            h = h0 + (h1 - h0) * u
            lift_at(xm, ly, h)
            sc.gmat["proc"] = T((0.0, off0, h - TRAY_FLOOR))
            m.pose(look=(xm, ly, h + 150.0), **grip)
            yield
    shot(c2, c2b, raise_lift(4 * FPS), 5 * FPS, "T01: the lift table raises the module over the tray's rim",
         "The shop's scissor table (Vestil SCTAB-1000-2040-AC, 20 x 40 in, 1,000 lb; robot-shop-equipment.csv), turned so "
         "the 730 mm base sits along its 40 in. side; its platform 26 mm over the tray floor, clear of the 20 mm rim", "T01",
         180.0)
    # round 9: the person walks (on screen, feet locked) from the handle round the table's end to behind it, puts both hands
    # on the guard frame's front posts at chest height and pushes as far as the arms reach
    zp = 1150.0 + LIP

    def post_pts(off, z=zp):
        return {s: (x, -265.0 + off - TIP, z) for s, x in POST.items()}
    st = {}

    def reach(tg, n, lean0, lean1, look):
        """Ease both hands from where they hang to tg {"l", "r"} over n frames, leaning from lean0 to lean1."""
        r0 = {s: np.asarray(op.rest_hand(s), float) for s in ("l", "r")}
        for i in range(n):
            u = ease((i + 1) / n)
            h_ = {s: tuple(r0[s] + (np.asarray(tg[s], float) - r0[s]) * u) for s in ("l", "r")}
            m.pose(lean=lean0 + (lean1 - lean0) * u, look=look, **push(h_["l"], h_["r"]))
            yield

    def push_lift():
        m.pose(lean=0.0, **free())
        yield from m.stand(3)
        # round the lift table's -x end (its corner at x -563, y -1108; the handle's uprights at x -623), 0.3 m off it
        yield from m.walk_path([(-850.0, -1330.0), (-420.0, -1470.0), (xm, -265.0 + off0 - TIP - 260.0)], hd_end=0.0,
                               look=(xm, -300.0, 1100.0))
        yield from reach(post_pts(off0), 8, 0.0, 4.0, (xm, -265.0 + off0 + 400.0, 1150.0))
        yield from m.stand(4)
        far = (m.y + REACH["chest"]) - (-265.0 - TIP)       # the offset at which the hands are REACH ahead
        n = int(3.2 * FPS)
        for i in range(n):
            u = ease((i + 1) / n)
            off = off0 + (far - off0) * u
            sc.gmat["proc"] = T((0.0, off, LIP))
            q = post_pts(off)
            m.pose(lean=4.0 + 14.0 * u, look=(xm, -265.0 + off + 400.0, 1150.0), **push(q["l"], q["r"]))
            yield
        check_reach("T01 push", post_pts(far).values())
        st["off"] = far
    c3 = cam_at((-100.0, -800.0, 1050.0), 4100.0, -36.0, 16.0)
    shot(c3, cam_at((-100.0, -800.0, 1050.0), 4000.0, -34.0, 16.0), push_lift(), 5 * FPS,
         "T01: the person pushes the module off the lift table onto the tray",
         "It slides on its four levelling mounts (McMaster 5537T983), over the rim; from behind the table the arms reach "
         "this far", "T01", 240.0)
    # cut: the lift table rolled away; from the access table the last 0.15 m, the module down on the tray floor
    lift_at(3200.0, -2600.0, LIFT["lo"], shown=False)
    sc.gmat["proc"] = T((0.0, -150.0, 0.0))
    m.place(xm, y_front, 0.0)
    pp = post_pts(-150.0, 1150.0)
    m.pose(lean=8.0, look=(xm, 0.0, 1100.0), **push(pp["l"], pp["r"]))

    def push_home():
        yield from m.stand(8)
        n = int(2.2 * FPS)
        for i in range(n):
            u = ease((i + 1) / n)
            off = -150.0 * (1.0 - u)
            sc.gmat["proc"] = T((0.0, off, 0.0))
            q = post_pts(off, 1150.0)
            m.pose(lean=8.0 + 10.0 * u, look=(xm, 0.0, 1100.0), **push(q["l"], q["r"]))
            yield
        check_reach("T01 home", post_pts(0.0, 1150.0).values())
        for _ in range(10):
            yield
        m.pose(lean=0.0, look=(xm, 0.0, 1100.0), **free())
    c4 = cam_at((-100.0, -350.0, 1050.0), 3500.0, -24.0, 20.0)
    shot(c4, cam_at((-100.0, -350.0, 1050.0), 3400.0, -21.0, 20.0), push_home(), 5 * FPS,
         "T01: the process module on the VLM tray",
         "Pushed home from the access table and levelled on its mounts (sequence.py T01: person + hoist or lift table)",
         "T01", 600.0)
    sc.gmat["proc"] = np.eye(4)
    # ---------------------------------------------------------------- T02: the rack, then its units
    rb = bounds["rack"]
    xr = 0.5 * (rb[0] + rb[1])
    RPOST = {"l": rb[0] + 15.0, "r": rb[1] - 15.0}

    def rpost(off, z):
        return {s: (x, rb[2] + off - TIP, z) for s, x in RPOST.items()}
    lift_at(xr, ly, h1)
    roff0 = ly
    sc.gmat["rack"] = T((0.0, roff0, LIP))
    show("rack", 1.0)
    m.place(xr + 40.0, rb[2] + roff0 - TIP - 260.0, 0.0)
    q = rpost(roff0, 1180.0 + LIP)
    m.pose(lean=4.0, look=(xr, rb[2] + roff0 + 400.0, 1150.0), **push(q["l"], q["r"]))

    def push_rack():
        yield from m.stand(6)
        far = (m.y + REACH["chest"]) - (rb[2] - TIP)
        n = int(3.0 * FPS)
        for i in range(n):
            u = ease((i + 1) / n)
            off = roff0 + (far - roff0) * u
            sc.gmat["rack"] = T((0.0, off, LIP))
            q = rpost(off, 1180.0 + LIP)
            m.pose(lean=4.0 + 14.0 * u, look=(xr, rb[2] + off + 400.0, 1150.0), **push(q["l"], q["r"]))
            yield
        check_reach("T02 push", rpost(far, 1180.0 + LIP).values())
    c5 = cam_at((-650.0, -800.0, 1150.0), 3500.0, -40.0, 14.0)
    shot(c5, cam_at((-650.0, -800.0, 1150.0), 3400.0, -37.0, 14.0), push_rack(), 5 * FPS,
         "T02: the 12U rack (22 kg) onto the tray's left end, from the lift table",
         "19 in. 4-post rack, 580 mm tall: the UPS, laser, PC and DIN drawer go in it next", "T02", 300.0)
    lift_at(3200.0, -2600.0, LIFT["lo"], shown=False)
    RH = 100.0                        # the rack's front feet just inside the tray's rim
    sc.gmat["rack"] = T((0.0, -RH, 0.0))
    m.place(xr + 40.0, y_front, 0.0)
    q = rpost(-RH, 1180.0)
    m.pose(lean=6.0, look=(xr, 0.0, 1150.0), **push(q["l"], q["r"]))

    def rack_home():
        yield from m.stand(8)
        n = int(2.0 * FPS)
        for i in range(n):
            u = ease((i + 1) / n)
            off = -RH * (1.0 - u)
            sc.gmat["rack"] = T((0.0, off, 0.0))
            q = rpost(off, 1180.0)
            m.pose(lean=6.0 + 10.0 * u, look=(xr, 0.0, 1150.0), **push(q["l"], q["r"]))
            yield
        check_reach("T02 home", rpost(0.0, 1180.0).values())
        for _ in range(8):
            yield
        m.pose(lean=0.0, **free())
    c6 = cam_at((-650.0, -450.0, 1150.0), 3100.0, -48.0, 16.0)       # from the left: the person doesn't hide the rack
    c6b = cam_at((-650.0, -450.0, 1150.0), 3050.0, -46.0, 16.0)
    shot(c6, c6b, rack_home(), 5 * FPS, "T02: the rack pushed home from the access table",
         "Then levelled; the units slide in on the rack's rails", "T02", 300.0)
    sc.gmat["rack"] = np.eye(4)
    # the units: each rests on the rails 120 mm out and is pushed home, palms on its front
    SLIDE = 120.0
    for g, kg, label in (("ups", 23.0, "UPS (Eaton 5PX, 2U), 23 kg"), ("laser", 40.0, "fiber laser (IPG YLR-500, 4U), 40 kg"),
                         ("pc", 8.0, "controller PC with the RTC6 (2U), 8 kg"), ("din", 9.0, "DIN-rail drawer (4U), 9 kg")):
        if g not in groups:
            continue
        b = bounds[g]
        zc = min(0.5 * (b[4] + b[5]), b[5] - 20.0)
        sc.gmat[g] = T((0.0, -SLIDE, 0.0))
        show(g, 1.0)

        def unit_in(g=g, b=b, zc=zc):
            # the hands where the unit's front really is (the nearest drawn point to each), 16 mm in front of it
            # on the unit's front panel (its bounding box's front, inside the rack's ears), fingertips on it
            pts = {s: np.array([x, b[2] - SLIDE - TIP, zc]) for s, x in (("l", b[0] + 90.0), ("r", b[1] - 90.0))}

            def at(dy):
                return {s: tuple(p + (0.0, dy, 0.0)) for s, p in pts.items()}
            h_ = at(0.0)
            for i in range(6):
                m.pose(lean=14.0 + 2.0 * i, look=(xr, b[2], zc), **push(h_["l"], h_["r"]))
                yield
            n = int(1.5 * FPS)
            for i in range(n):
                u = ease((i + 1) / n)
                sc.gmat[g] = T((0.0, -SLIDE * (1.0 - u), 0.0))
                h_ = at(SLIDE * u)
                m.pose(lean=24.0 + 6.0 * u, look=(xr, b[2], zc), **push(h_["l"], h_["r"]))
                yield
            check_reach(f"T02 {g}", at(SLIDE).values())
            sc.gmat[g] = np.eye(4)
            for _ in range(4):
                yield
            m.pose(lean=0.0, **free())
        shot(c6b, c6b, unit_in(), int(2.6 * FPS), f"T02: the {label} slides into the rack",
             "Pushed home on the rack's rails from the lift table: " +
             ("over a UR12e's 12.5 kg payload" if kg > 12.5 else
              "light enough for an arm, but the rails and cage nuts need a person's hands (not planned for the arms)"),
             "T02", 420.0)
    show("rackrest", 1.0)
    # ---------------------------------------------------------------- T03: the gas module
    gb = bounds["gasbase"]
    xg = 0.5 * (gb[0] + gb[1])
    goff0 = ly - 0.5 * (gb[2] + gb[3])

    def gplate(off, z):
        return {"l": (gb[0] + 80.0, gb[2] + off - TIP, z), "r": (gb[1] - 80.0, gb[2] + off - TIP, z)}
    lift_at(xg, ly, h1)
    sc.gmat["gasbase"] = T((0.0, goff0, LIP))
    show("gasbase", 1.0)
    m.place(xg, gb[2] + goff0 - TIP - 240.0, 0.0)
    zg = 909.0 + LIP + 8.0            # round 9: 10 mm higher on the plate's edge (round 8's gloves brushed the lift's platform)
    q = gplate(goff0, zg)
    m.pose(lean=16.0, look=(xg, gb[2] + goff0 + 300.0, 950.0), **push(q["l"], q["r"]))

    def push_gas():
        yield from m.stand(6)
        far = (m.y + REACH["low"]) - (gb[2] - TIP)
        far = min(far, -278.0 - (gb[3] - 18.0) - 10.0)   # its studs, 26 mm up, stop short of the guard door's rail
        n = int(2.5 * FPS)
        for i in range(n):
            u = ease((i + 1) / n)
            off = goff0 + (far - goff0) * u
            sc.gmat["gasbase"] = T((0.0, off, LIP))
            q = gplate(off, zg)
            m.pose(lean=16.0 + 18.0 * u, look=(xg, gb[2] + off + 300.0, 950.0), **push(q["l"], q["r"]))
            yield
        check_reach("T03 push", gplate(far, zg).values())
    c7 = cam_at((650.0, -800.0, 1050.0), 3500.0, -22.0, 17.0)
    shot(c7, cam_at((650.0, -800.0, 1050.0), 3400.0, -25.0, 17.0), push_gas(), 4 * FPS,
         "T03: the gas module's MIC-6 base plate onto the tray's right end", "On its four levelling mounts, from the lift "
         "table; then pushed home from the access table and levelled", "T03", 600.0)
    lift_at(3200.0, -2600.0, LIFT["lo"], shown=False)
    sc.gmat["gasbase"] = np.eye(4)
    m.place(xg - 60.0, y_front, 0.0)
    m.pose(lean=0.0, look=(xg, 0.0, 1050.0), **free())
    c8 = cam_at((700.0, -300.0, 1050.0), 3000.0, 32.0, 24.0)        # from the right: the person (x 635) beside the parts
    # the gas parts whose front the person reaches from the access table slide in, palms on them; the rest (and the
    # fittings) are fitted in place, shown appearing in the time-lapse
    for g in gas_groups:
        b = bounds[g]
        nm = g.split(":", 1)[1]
        heavy = "pump" in nm.lower()
        small = any(k in nm.lower() for k in ("inlet", "outlet", "manifold", "regulator"))
        reach_ok = math.hypot(0.5 * (b[0] + b[1]) - (xg - 60.0), b[2] - TIP - y_front) <= REACH["low"] and not small
        xc = 0.5 * (b[0] + b[1])
        zc = min(0.5 * (b[4] + b[5]), 1080.0)
        GS = 120.0                    # set down from this high onto the base plate

        def gas_in(g=g, b=b, xc=xc, zc=zc, reach_ok=reach_ok):
            if not reach_ok:
                for i in range(8):
                    show(g, (i + 1) / 8.0)
                    m.pose(look=(xc, 0.5 * (b[2] + b[3]), zc))
                    yield
                return
            sc.gmat[g] = T((0.0, 0.0, GS))
            show(g, 1.0)
            hw = max(25.0, min(110.0, 0.5 * (b[1] - b[0]) - 25.0))
            pts = {s: np.array([x, b[2] - TIP, zc]) for s, x in (("l", xc - hw), ("r", xc + hw))}

            def at(dz):
                return {s: tuple(p + (0.0, 0.0, dz)) for s, p in pts.items()}
            h_ = at(GS)
            for i in range(6):
                m.pose(lean=12.0 + 2.0 * i, look=(xc, b[2], zc), **push(h_["l"], h_["r"]))
                yield
            n = int(1.4 * FPS)
            for i in range(n):
                u = ease((i + 1) / n)
                sc.gmat[g] = T((0.0, 0.0, GS * (1.0 - u)))
                h_ = at(GS * (1.0 - u))
                m.pose(lean=22.0 + 6.0 * u, look=(xc, b[2], zc), **push(h_["l"], h_["r"]))
                yield
            check_reach(f"T03 {nm}", at(0.0).values())
            sc.gmat[g] = np.eye(4)
            m.pose(lean=0.0, **free())
        if small:
            continue
        shot(c8, c8, gas_in(), int(2.2 * FPS), f"T03: {nm}" + (" (26 kg)" if heavy else ""),
             "Gas module: dry scroll pump, sealed blower, cyclone + HEPA, O2 / dew-point box, argon manifold and "
             "regulator (their screws are not drawn)", "T03", 600.0 if heavy else 240.0)

    def fittings():
        for g in gas_groups:
            nm = g.split(":", 1)[1].lower()
            if any(k in nm for k in ("inlet", "outlet", "manifold", "regulator")):
                for i in range(6):
                    show(g, (i + 1) / 6.0)
                    yield
    shot(c8, c8, fittings(), int(4.0 * FPS), "T03: inlets, outlets, the argon manifold and regulator fitted",
         "Time-lapse: fittings are a person's job (wrenches, thread sealant)", "T03", 600.0)
    # ---------------------------------------------------------------- T04, T05: hoses and lines, the dock
    c9 = cam_at((250.0, -250.0, 1100.0), 3700.0, -12.0, 30.0)
    c9b = cam_at((700.0, -200.0, 1100.0), 3300.0, 18.0, 26.0)
    for g, cap, sub, secs, step, spots in (
            ("hoses", "T04: the process fiber, KF-25 bellows, valve, gas lines",
             "The fiber runs from the laser's back through the rack to the collimator (bends 75 mm; IPG's minimum 70); "
             "hoses and wing-nut clamps are a person's job (sequence.py T04); shown fitted in the time-lapse", 2700.0, "T04",
             (350.0,)),
            ("dock", "T05: the tray dock, the umbilicals and the power box",
             "Power, Ethernet, argon, water and exhaust mate sideways at the tray's back-right corner", 1200.0, "T05",
             (950.0,))):
        if g not in groups:
            continue

        def fit(g=g, spots=spots):
            for k, xs in enumerate(spots):
                # round 9: along the access table on screen (side-steps for a short move, a walk for a long one)
                m.pose(lean=0.0, look=(xs, 0.0, 1050.0), **free())
                yield from m.stand(4)
                yield from m.walk_to(xs, y_front, hd_end=0.0, face=0.0 if abs(xs - m.x) < 450.0 else None,
                                     v=38.0 if abs(xs - m.x) < 450.0 else None, look=(xs, 0.0, 1050.0))
                if k == 0:
                    for i in range(8):
                        show(g, (i + 1) / 8.0)
                        yield
                tgt = nearest(sc, g, (xs, y_front + REACH["chest"], 1100.0))
                if math.hypot(tgt[0] - m.x, tgt[1] - m.y) > REACH["chest"] - 20.0:   # out of reach here: look, no touch
                    yield from m.stand(14, look=tgt)
                    continue
                for i in range(int(2.0 * FPS)):
                    m.pose(lean=18.0, look=tgt, hands={"l": (tgt[0] - 60.0, tgt[1] - TIP, tgt[2]),
                                                       "r": (tgt[0] + 30.0, tgt[1] - TIP, tgt[2] + 15.0)},
                           palm={"l": FWD, "r": FWD})
                    yield
                m.pose(lean=0.0, **free())
        shot(c9 if g == "hoses" else c9b, c9 if g == "hoses" else c9b, fit(), 5 * FPS, cap, sub, step, secs)
    # ---------------------------------------------------------------- T06: the leak check
    def step_back():
        # round 9: on screen: backs away 0.8 m from the tray, still facing the machine, and turns a little to watch it
        m.pose(lean=0.0, look=(0.0, -100.0, 1100.0), **free())
        yield from m.stand(6)
        yield from m.walk_to(m.x - 250.0, -1650.0, hd_end=-20.0, face=-10.0, v=32.0, look=(0.0, -100.0, 1100.0))
        while True:
            m.pose(look=(0.0, -100.0, 1100.0))
            yield
    sb = step_back()
    ts = list(np.linspace(0.0, 75.0, 151))

    def p_of(t):
        if t <= 1.2:
            return 1000.0 * math.exp(-t / 1.2 * math.log(1000.0))          # to 1 mbar in 1.2 min (seals.md: 0.9-1.2)
        if t <= 64.0:
            return max(0.05, 1.0 * math.exp(-(t - 1.2) / 6.0))             # down to the scroll pump's ~0.05 mbar
        return 0.05 + 8e-4 * (t - 64.0)                                   # valve closed: 8e-4 mbar/min expected
    ps = [p_of(t) for t in ts]
    c10 = cam_at((-50.0, -400.0, 1150.0), 3500.0, -24.0, 20.0)
    c10b = cam_at((-50.0, -400.0, 1150.0), 3350.0, -20.0, 20.0)
    n = 10 * FPS
    for i in range(n):
        next(sb)
        u = i / (n - 1)
        k = int(round(u * (len(ts) - 1)))
        t_min = ts[k]
        phase = "pumping down" if t_min < 1.2 else ("holding at <= 1 mbar" if t_min < 64.0 else "valve closed: rate of rise")
        val = f"{ps[k]:.3g} mbar at {t_min:.0f} min"
        verdict = ""
        if t_min >= 74.0:
            val = "rise 8e-4 mbar/min"
            verdict = "pass"
        frame([lerp(c10[0], c10b[0], ease(u)), lerp(c10[1], c10b[1], ease(u)), (0, 0, 1)],
              f"T06: the leak check, {phase}",
              "After >= 1 h at <= 1 mbar the valve closes; the Pirani must rise < 1e-3 mbar/min over 10 min "
              "(seals.md section 7). Expected, not measured",
              ["machine"], "T06", status=verdict or "", proc_s=75.0 * 60.0 / n, add=dict(machine_h=75.0 / 60.0 / n),
              chart=dict(title="Chamber pressure, expected", x=ts, y=ps, now=k, ylog=True, xlabel="minutes",
                         ylabel="mbar", xticks=[0, 15, 30, 45, 60, 75], ref=1.0, ref_label="1 mbar",
                         value=val, verdict=verdict))
    # ---------------------------------------------------------------- a last look (cut)
    n = 5 * FPS
    c11 = cam_at((0.0, -200.0, 1100.0), 5600.0, -40.0, 18.0)
    c11b = cam_at((0.0, -200.0, 1100.0), 5400.0, -37.0, 18.0)
    for i in range(n):
        next(sb)
        u = ease(i / (n - 1))
        frame([lerp(c11[0], c11b[0], u), lerp(c11[1], c11b[1], u), (0, 0, 1)],
              "The desktop LPBF on its VLM tray, ready for its first build",
              "Process module, 12U rack and gas module side by side on one 2450 x 864 mm tray; the tray goes back "
              "into the Kardex", [], "", status="", proc_s=0.0)
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s) in {time.time() - t0:.0f} s", flush=True)


def rescale_meta():
    """Make each person step's time on the clocks the data worker's estimate (hud.json times.assembly, person_min for
    T01-T05), so the clocks and the summary's charts agree; the frames keep their share of the step. T06 keeps the
    75 min of seals.md's test (>= 1 h held at <= 1 mbar, then 10 min of reading)."""
    import json
    hud = common.DATA / "hud.json"
    path = common.FRAMES / NAME / "meta.jsonl"
    if not hud.exists() or not path.exists():
        return
    rows = ((json.loads(hud.read_text()).get("times") or {}).get("assembly") or {}).get("rows") or []
    want = {r["step"]: float(r.get("person_min") or 0) * 60.0 for r in rows
            if str(r.get("step", "")).startswith("T") and r["step"] != "T06" and r.get("person_min")}
    meta = [json.loads(x) for x in path.read_text().splitlines()]
    have = {}
    for m in meta:
        have[m.get("step", "")] = have.get(m.get("step", ""), 0.0) + float(m.get("proc_s") or 0.0)
    for m in meta:
        st = m.get("step", "")
        if st in want and have.get(st, 0) > 0:
            k = want[st] / have[st]
            m["proc_s"] = float(m.get("proc_s") or 0.0) * k
            if m.get("add"):
                m["add"] = {a: v * k for a, v in m["add"].items()}
    path.write_text("".join(json.dumps(m) + "\n" for m in meta))
    print(f"{NAME}: person steps rescaled to hud.json: " + ", ".join(f"{k} {v / 60:.0f} min" for k, v in want.items()),
          flush=True)


if __name__ == "__main__":
    if "meta" not in sys.argv[1:]:
        main()
    rescale_meta()
