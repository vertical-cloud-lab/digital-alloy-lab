"""Timeline for the fast-track video: fixed cameras, parts that come in and leave along checked paths, stage motions, and
the overlay data of every frame.

A chapter is built by calling Timeline's methods in order; each advances a cursor (seconds). `state(t)` folds every event
into the drawn state at time t: for each actor whether it is drawn, its translation (placement + stage motion), a per-axis
scale (the lift column), its opacity and colour, and the effect meshes (beam, scan vectors, powder, coupons). render.py
draws the states; audit.py checks them.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

import plan as PL

FPS = 30
W3, H3 = 1440, 1080                 # the 3-D picture; the 480 px panel to its right is drawn by compose.py


# ------------------------------------------------------------------------------------------------ cameras
@dataclass
class Cam:
    pos: tuple
    focal: tuple
    angle: float = 30.0
    up: tuple = (0.0, 0.0, 1.0)
    name: str = ""

    def basis(self):
        p, f = np.asarray(self.pos, float), np.asarray(self.focal, float)
        fw = (f - p) / np.linalg.norm(f - p)
        r = np.cross(fw, np.asarray(self.up, float))
        r /= np.linalg.norm(r)
        u = np.cross(r, fw)
        return p, fw, r, u

    def ndc(self, P):
        """Normalised device coordinates (x, y in [-1, 1] on screen) and depth of points P (n, 3)."""
        p, fw, r, u = self.basis()
        d = np.asarray(P, float) - p
        z = d @ fw
        th = math.tan(math.radians(self.angle) / 2)
        zz = np.where(z > 1e-6, z, 1e-6)
        return np.c_[(d @ r) / (zz * th * W3 / H3), (d @ u) / (zz * th)], z

    def sees(self, lo, hi, margin=0.02):
        """Is any of the box [lo, hi] on screen?"""
        C = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        xy, z = self.ndc(C)
        if np.all(z <= 1e-6):
            return False
        if np.any(z <= 1e-6):
            return True
        x0, y0 = xy.min(0)
        x1, y1 = xy.max(0)
        m = 1 + margin
        return not (x1 < -m or x0 > m or y1 < -m or y0 > m)


def lerp_cam(a, b, s):
    s = 0.5 - 0.5 * math.cos(math.pi * min(max(s, 0.0), 1.0))
    L = lambda x, y: tuple(float(p + (q - p) * s) for p, q in zip(x, y))  # noqa: E731
    return Cam(L(a.pos, b.pos), L(a.focal, b.focal), a.angle + (b.angle - a.angle) * s, a.up, a.name)


# ------------------------------------------------------------------------------------------------ motion profiles
def trapezoid(L, v, a):
    """Duration of a rest-to-rest move of length L at peak speed v and acceleration a, and its position function."""
    if L <= 1e-9:
        return 0.0, (lambda t: 0.0)
    ta = v / a
    if a * ta * ta >= L:                      # triangle: never reaches v
        ta = math.sqrt(L / a)
        T = 2 * ta

        def s(t):
            t = min(max(t, 0.0), T)
            return 0.5 * a * t * t if t <= ta else L - 0.5 * a * (T - t) ** 2
        return T, s
    T = 2 * ta + (L - a * ta * ta) / v

    def s(t):
        t = min(max(t, 0.0), T)
        if t <= ta:
            return 0.5 * a * t * t
        if t >= T - ta:
            return L - 0.5 * a * (T - t) ** 2
        return 0.5 * a * ta * ta + v * (t - ta)
    return T, s


@dataclass
class Path:
    """Legs between offsets, each a trapezoid move, with a pause between legs."""
    way: list
    speeds: list
    accel: list
    pause: float = 0.25
    legs: list = field(default_factory=list)
    T: float = 0.0

    def __post_init__(self):
        t = 0.0
        self.legs = []
        for k, (a, b) in enumerate(zip(self.way[:-1], self.way[1:])):
            a, b = np.asarray(a, float), np.asarray(b, float)
            L = float(np.linalg.norm(b - a))
            T, s = trapezoid(L, self.speeds[k], self.accel[k])
            self.legs.append((t, t + T, a, b, L, s))
            t += T + (self.pause if k < len(self.way) - 2 else 0.0)
        self.T = t

    def at(self, t):
        if not self.legs:
            return np.asarray(self.way[-1], float)
        for (t0, t1, a, b, L, s) in self.legs:
            if t <= t1:
                if t < t0:
                    return a
                return a + (b - a) * (s(t - t0) / L if L > 0 else 1.0)
        return self.legs[-1][3]


HAND_V, HAND_A = 800.0, 2000.0       # carrying a part by hand, mm/s and mm/s^2 (estimate)
SEAT_V, SEAT_A = 90.0, 400.0         # the last leg, setting it down or sliding it home (estimate)


SEAT_MM = 25.0                       # the slow part of the last leg


def hand_path(way, seat_v=SEAT_V, reverse=False):
    """Carried at hand speed, set down (or, reversed, lifted off) slowly over the last SEAT_MM of the last leg."""
    way = [np.asarray(w, float) for w in way]
    if reverse:
        way = way[::-1]
    a, b = way[-2], way[-1]
    L = float(np.linalg.norm(b - a))
    if L > 2 * SEAT_MM:
        way = way[:-1] + [b + (a - b) * SEAT_MM / L, b]
    n = len(way) - 1
    sp = [HAND_V] * n
    ac = [HAND_A] * n
    sp[-1], ac[-1] = seat_v, SEAT_A
    if reverse:
        way, sp, ac = way[::-1], sp[::-1], ac[::-1]
    return Path([tuple(w) for w in way], sp, ac, pause=0.0 if L > 2 * SEAT_MM else 0.15)


# ------------------------------------------------------------------------------------------------ actors and state
@dataclass
class Actor:
    name: str
    V: np.ndarray
    F: np.ndarray
    color: str
    opacity: float = 1.0
    pid: str = ""
    kind: str = "part"          # part | room | person
    solid: bool = True
    edges: bool = True
    group: str = ""             # "recoater" | "piston" | "column" (the lift column, scaled) | ""
    label: str = ""             # the model's part name


class Timeline:
    def __init__(self, chapter, title, actors, present):
        self.chapter, self.title = chapter, title
        self.actors = dict(actors)               # name -> Actor
        self.present0 = set(present)             # drawn at t = 0
        self.t = 0.0
        self.events = []                         # (t0, t1, fn(state, t))
        self.shots = []                          # [t0, t1, cam, name]
        self.over = []                           # (t0, t1, key, value)
        self.world = PL.World()
        for n in present:
            a = self.actors[n]
            if a.solid and a.kind != "person":
                self.world.put(n, a.V, a.F)
        self.notes = []                          # planner results, for the README
        self.cam = None
        self._off = {}                           # translations of moved parts that are not in the planner's world

    # --- shots and captions
    def shot(self, cam, name=""):
        if self.shots:
            self.shots[-1][1] = self.t
        self.cam = cam
        self.shots.append([self.t, None, cam, name or cam.name])

    def drift(self, cam_to, dur):
        """A slow camera move inside a shot (kept under 1/7 of the frame width a second)."""
        a = self.cam
        t0 = self.t
        self.shots[-1][1] = t0
        self.shots.append([t0, t0 + dur, ("drift", a, cam_to, t0, dur), "drift"])
        self.cam = cam_to
        self.shots.append([t0 + dur, None, cam_to, cam_to.name])

    def overlay(self, key, value, t0=None, t1=None):
        self.over.append((self.t if t0 is None else t0, t1, key, value))

    def caption(self, main, sub=""):
        self.overlay("caption", (main, sub))

    def wait(self, s):
        self.t += s

    # --- state at time t
    def base(self):
        st = {}
        for n, a in self.actors.items():
            st[n] = dict(vis=n in self.present0, off=np.zeros(3), stage=np.zeros(3), scale=None, op=a.opacity,
                         color=a.color)
        st["_fx"] = {}
        return st

    def state(self, t):
        st = self.base()
        for (t0, t1, fn) in self.events:
            fn(st, t)
        return st

    def overlay_at(self, t):
        out = {}
        for (t0, t1, k, v) in self.over:
            if t >= t0 and (t1 is None or t < t1):
                out[k] = v
        return out

    def cam_at(self, t):
        cur = None
        for (t0, t1, c, name) in self.shots:
            if t >= t0 and (t1 is None or t < t1):
                cur = (c, name)
        if cur is None:
            return self.shots[0][2], self.shots[0][3]
        c, name = cur
        if isinstance(c, tuple) and c[0] == "drift":
            _, a, b, t0, dur = c
            return lerp_cam(a, b, (t - t0) / dur), name
        return c, name

    def end(self, hold=0.0):
        self.t += hold
        if self.shots:
            self.shots[-1][1] = self.t
        return self.t

    # --- parts: in, out, moved
    def _trim(self, names, path, entering):
        """Start (entering) or end (leaving) the path where the group comes into or goes out of the picture."""
        cam = self.cam
        lo = np.min([self.actors[n].V.min(0) for n in names], axis=0)
        hi = np.max([self.actors[n].V.max(0) for n in names], axis=0)
        way = [np.asarray(w, float) for w in path]
        if not entering:
            way = way[::-1]
        a, b = way[0], way[1]
        L = float(np.linalg.norm(b - a))
        u = (b - a) / max(L, 1e-9)
        s_vis = L
        for s in np.arange(0.0, L, 10.0):
            p = a + u * s
            if cam.sees(lo + p, hi + p):
                s_vis = s
                break
        s0 = max(0.0, s_vis - 30.0)
        way[0] = a + u * s0
        if not entering:
            way = way[::-1]
        return [tuple(w) for w in way]

    def _spend_and_label(self, names, verb):
        pids = []
        for n in names:
            a = self.actors[n]
            if a.pid and a.pid not in pids:
                pids.append(a.pid)
        return [(self.actors[n].label or n, self.actors[n].pid) for n in names], pids

    def insert(self, names, prefs=None, way=None, seat_v=SEAT_V, ignore=(), verb="adding", gap=0.25, label=None):
        names = [n for n in names if n in self.actors]
        if not names:
            return None
        grp = [n for n in names if self.actors[n].solid]
        for n in grp:
            if n not in self.world.g:
                self.world.put(n, self.actors[n].V, self.actors[n].F)
        if way is None:
            how, way = PL.plan(self.world, grp, prefs=prefs, ignore=ignore)
        else:
            bad = PL.check(self.world, grp, way, ignore)
            how = "given"
            if bad:
                self.notes.append(dict(t=round(self.t, 2), names=names, path=way, collision=str(bad[0])))
                print(f"  ! {self.chapter}: given path for {names[0]} collides: {bad[0]}", flush=True)
        way_full = [tuple(map(float, w)) for w in way]
        way_vis = self._trim(names, way_full, entering=True)
        P = hand_path(way_vis, seat_v)
        t0, t1 = self.t, self.t + P.T
        self.notes.append(dict(t=round(t0, 2), what=verb, names=names, how=how, path=way_full, seconds=round(P.T, 2)))

        end = np.asarray(way_full[-1], float)

        def fn(st, t, names=names, P=P, t0=t0, t1=t1, end=end):
            for n in names:
                s = st[n]
                if t < t0:
                    continue                      # hidden unless drawn from the start or still there from before
                elif t < t1:
                    s["vis"] = True
                    s["off"] = P.at(t - t0)
                else:
                    s["vis"] = True
                    s["off"] = end.copy()
        self.events.append((t0, t1, fn))
        for n in grp:
            self.world.move(n, end)
        for n in names:
            if n not in self.world.g:
                self._off[n] = end.copy()
        lab, pids = self._spend_and_label(names, verb)
        self.overlay("adding", (verb, label or lab), t0, t1 + 0.8)
        self.t = max(t0 + 0.5, t1 + gap)
        return P

    def remove(self, names, prefs=None, way=None, verb="taking out", gap=0.25, label=None, seat_v=SEAT_V):
        """way: from the place (0, 0, 0) out of the scene (the reverse of an insertion path)."""
        names = [n for n in names if n in self.actors]
        if not names:
            return None
        grp = [n for n in names if self.actors[n].solid]
        base = {n: self.world.t.get(n, np.zeros(3)).copy() for n in grp}
        if way is None:
            how, w_in = PL.plan(self.world, grp, prefs=prefs, ignore=ignore_of(grp))
            way = w_in[::-1]
        else:
            how = "given"
            bad = PL.check(self.world, grp, way, ())
            if bad:
                self.notes.append(dict(t=round(self.t, 2), names=names, path=way, collision=str(bad[0])))
                print(f"  ! {self.chapter}: given removal path for {names[0]} collides: {bad[0]}", flush=True)
        way_full = [tuple(map(float, w)) for w in way]
        way_vis = self._trim(names, way_full, entering=False)
        P = hand_path(way_vis, seat_v, reverse=True)
        t0, t1 = self.t, self.t + P.T
        self.notes.append(dict(t=round(t0, 2), what=verb, names=names, how=how, path=way_full, seconds=round(P.T, 2)))
        start = {n: (self.actors_off(n)) for n in names}

        def fn(st, t, names=names, P=P, t0=t0, t1=t1, start=start):
            for n in names:
                s = st[n]
                if t < t0:
                    continue
                if t < t1:
                    s["vis"] = True
                    s["off"] = start[n] + P.at(t - t0)
                else:
                    s["vis"] = False
        self.events.append((t0, t1, fn))
        for n in grp:
            self.world.drop(n)
        lab, _ = self._spend_and_label(names, verb)
        self.overlay("adding", (verb, label or lab), t0, t1 + 0.8)
        self.t = t1 + gap
        return P

    def actors_off(self, n):
        return self.world.t[n].copy() if n in self.world.t else self._off.get(n, np.zeros(3)).copy()

    def move(self, names, way, v=30.0, a=100.0, verb="moving", gap=0.3, label=None, check=True, overlay=True):
        """Shift parts already in the scene by the offsets of `way` (relative to where they are now)."""
        names = [n for n in names if n in self.actors]
        grp = [n for n in names if self.actors[n].solid and n in self.world.g]
        start = {n: self.actors_off(n) for n in names}
        if check:
            bad = []
            for off in PL.samples(way):
                for m, o, d in self.world.hits(grp, off):
                    bad.append((tuple(np.round(off, 1)), m, o, d))
                    break
                if bad:
                    break
            if bad:
                self.notes.append(dict(t=round(self.t, 2), names=names, path=way, collision=str(bad[0])))
                print(f"  ! {self.chapter}: move of {names[0]} collides: {bad[0]}", flush=True)
        P = Path([tuple(map(float, w)) for w in way], [v] * (len(way) - 1), [a] * (len(way) - 1))
        t0, t1 = self.t, self.t + P.T

        def fn(st, t, names=names, P=P, t0=t0, t1=t1, start=start):
            for n in names:
                s = st[n]
                if t < t0:
                    continue
                s["off"] = start[n] + P.at(min(t - t0, P.T))
        self.events.append((t0, t1, fn))
        end = np.asarray(way[-1], float)
        for n in names:
            if n in self.world.g:
                self.world.move(n, start[n] + end)
            else:
                self._off[n] = start[n] + end
        if overlay:
            lab, _ = self._spend_and_label(names, verb)
            self.overlay("adding", (verb, label or lab), t0, t1 + 0.8)
        self.notes.append(dict(t=round(t0, 2), what=verb, names=names, how="move", path=[tuple(map(float, w)) for w in way],
                               seconds=round(P.T, 2)))
        self.t = t1 + gap
        return P

    def stage(self, names, fn_off, t0, t1, scale_fn=None, scale_names=()):
        """A stage motion between t0 and t1 (absolute): fn_off(t) -> offset added to the placement; held after t1."""
        def fn(st, t, names=names, fn_off=fn_off, t0=t0, t1=t1):
            if t < t0:
                return
            tt = min(t, t1)
            o = np.asarray(fn_off(tt), float)
            for n in names:
                st[n]["stage"] = o
            if scale_fn is not None:
                for n in scale_names:
                    st[n]["scale"] = scale_fn(tt)
        self.events.append((t0, t1, fn))

    def fx(self, fn, t0, t1=None):
        """An effect: fn(st, t) sets st['_fx'][name] = dict(kind, data, color, opacity, solid)."""
        self.events.append((t0, t1 if t1 is not None else 1e9, fn))

    def paint(self, name, color, t0, t1=None):
        def fn(st, t):
            if t >= t0 and (t1 is None or t < t1):
                st[name]["color"] = color
        self.events.append((t0, t1 or 1e9, fn))

    def morph(self, name, V1, t0, t1, V0=None):
        """Blend an actor's vertices from V0 (default: as built) to V1 (same triangles) between t0 and t1, eased (a cable
        following its ends)."""
        V0 = self.actors[name].V if V0 is None else np.asarray(V0, np.float32)

        def fn(st, t, V0=V0, V1=np.asarray(V1, np.float32)):
            if t < t0:
                return
            s = min(1.0, (t - t0) / max(t1 - t0, 1e-9))
            s = 0.5 - 0.5 * math.cos(math.pi * s)
            st[name]["morph"] = (round(s, 3), V0 + (V1 - V0) * s)
        self.events.append((t0, t1, fn))
        if name in self.world.g:
            self.world.put(name, V1, self.actors[name].F, self.world.t[name])

    def fade(self, name, op, t0, t1=None):
        def fn(st, t):
            if t >= t0 and (t1 is None or t < t1):
                st[name]["op"] = op
        self.events.append((t0, t1 or 1e9, fn))


def ignore_of(grp):
    return ()
