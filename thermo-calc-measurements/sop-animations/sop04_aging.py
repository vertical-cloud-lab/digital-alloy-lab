#!/usr/bin/env python3
"""SOP 04, animated (#262, PR #263): a fast property screen with Vickers hardness and eddy-current conductivity,
as-built and through an aging series; laser flash at a contract lab for the thermal-conductivity calibration.

    xvfb-run -a -s "-screen 0 1920x1080x24" python sop04_aging.py sop04_c2      # one chapter -> out/mp4/sop04_c2.mp4
    python sop04_aging.py join                                                 # out/mp4/sop04.mp4, sheet, GIF

Chapters (each its own render, so they run in parallel):

* ``sop04_c1``: the Checks (title card), the Samples: the polished XZ sections from SOP 03, flat coupons cut from one
  cube row, the 5 mm cube that is too small, the aging matrix and the reference alloys.
* ``sop04_c2``: the aging series at the furnace (Nabertherm NAT 15/65): batches by temperature, five boats, one per
  time, each to a water quench.
* ``sop04_c3``: Vickers hardness (ASTM E384) on the Mitutoyo HM-220: load, dwell, ten indents, spacing, both
  diagonals, single tracks at HV0.05, a line across the build height, Tabor as a screen only.
* ``sop04_c4``: eddy-current conductivity (%IACS): standards, temperature, frequency and penetration depth, three
  readings per face, the temperature correction.
* ``sop04_c5``: thermal conductivity by laser flash, at the contract lab, on 3-4 alloys; the Smith-Palmer fit.
* ``sop04_c6``: Analysis, Acceptance and the Open questions.

Data panels are computed with ../analysis/kinetics.py and ../analysis/conductivity.py on synthetic inputs and are
badged "synthetic example". ``PREVIEW=1`` renders only each sub-step's last frame (a contact sheet in /tmp).
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import stage as S  # noqa: E402
from stage import BENCH_H, R, T  # noqa: E402

import audit  # noqa: E402
import models_props as MP  # noqa: E402
import people  # noqa: E402  (vl/ is on the path once stage is imported)

sys.path.insert(0, str(HERE.parent / "analysis"))
import conductivity as CON  # noqa: E402
import kinetics as KIN  # noqa: E402

from PIL import Image, ImageDraw  # noqa: E402

TITLE = "SOP 04 · Hardness, conductivity and an aging series"
SYN = "synthetic example"


# ===================================================================================================== helpers
def unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


def frame_along(origin, d, up=(0.0, 0.0, 1.0)) -> np.ndarray:
    """A 4x4 whose x axis runs along d and z is as close to `up` as it can be, at `origin`."""
    d = unit(d)
    up = np.asarray(up, float)
    z = unit(up - (up @ d) * d)
    y = np.cross(z, d)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = d, y, z, origin
    return M


def along(path, u):
    """A point u (0-1) of the way along a polyline, by arc length."""
    pts = np.asarray(path, float)
    if len(pts) == 1:
        return pts[0]
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = min(max(u, 0.0), 1.0) * s[-1]
    i = min(int(np.searchsorted(s, t, side="right")) - 1, len(seg) - 1)
    f = (t - s[i]) / max(seg[i], 1e-9)
    return pts[i] + (pts[i + 1] - pts[i]) * f


def reparent(sc, group, parent):
    """Hang `group` on `parent` (or on nothing) without moving it in the world."""
    W = sc.world(group)
    if parent is None:
        sc.parent.pop(group, None)
        sc.gmat[group] = W
    else:
        sc.parent[group] = parent
        sc.gmat[group] = np.linalg.inv(sc.world(parent)) @ W


def drop_piece(rig, piece):
    """Take a piece of a Rig out of the scene (a model's own prop we draw differently)."""
    sc = rig.sc
    for n in rig.names.get(piece, []):
        sc.pl.remove_actor(sc.actors[n])
        for d in (sc.actors, sc.group_of, sc.alpha, sc.base_alpha):
            d.pop(n, None)
        sc.__dict__.get("_keep", {}).pop(n, None)
        sc.__dict__.get("_sent", {}).pop(n, None)
    rig.names[piece] = []


def fade(sc, names, a0, a1):
    def up(u):
        for n in names:
            sc.alpha[n] = a0 + (a1 - a0) * u
    return up


def setv(d, key, a, b):
    """update(u) setting d[key] from a to b (numbers)."""
    def up(u):
        d[key] = a + (b - a) * u
    return up


def call_at(u0, fn):
    """update(u) that calls fn() once, the first time u reaches u0."""
    done = []

    def up(u):
        if u >= u0 and not done:
            done.append(1)
            fn()
    return up


def add_model(sc, name, model, at, parent=None, tol=0.2):
    """A Model (props) as one scene group `name`, at `at` (4x4)."""
    ents = S.props(name, model, tol)
    S.add_entries(sc, ents, name, name, at=at, parent=parent)
    return name


def gauge(sc, key, value):
    g = [x for x in sc.gauges if x[0] != key]
    order = [k for k, _ in sc.gauges]
    if key in order:
        g.insert(order.index(key), (key, value))
    else:
        g.append((key, value))
    sc.gauges = g


# ------------------------------------------------------------------------------------------------- the operator
class Op:
    """A people.Person with a state we can tween: walk (phase follows distance, one cycle per 1016 mm), turn, lean,
    hands to points (or to rest), grips and gaze."""

    def __init__(self, sc, x, y, hd=0.0, name="op"):
        self.sc = sc
        self.p = people.Person(sc, name)
        self.s = dict(x=float(x), y=float(y), hd=float(hd), lean=0.0, phase=0.0, amp=0.0)
        self.hand = {"l": None, "r": None}
        self.grip = {"l": 0.3, "r": 0.3}
        self.palm = {"l": None, "r": None}
        self.look = None
        self.apply()

    def apply(self):
        self.p.set(x=self.s["x"], y=self.s["y"], hd=self.s["hd"], lean=self.s["lean"], phase=self.s["phase"],
                   amp=self.s["amp"], hands=dict(self.hand), grip=dict(self.grip), look=self.look,
                   palm=dict(self.palm))
        if os.environ.get("SOP04_DEBUG"):
            for side in ("l", "r"):
                if self.hand[side] is not None:
                    e = np.linalg.norm(self.p.hand_point(side) - np.asarray(self.hand[side], float))
                    if e > 25:
                        lab = self.sc.label
                        print(f"  reach {side}: {e:.0f} mm short at {lab!r} frame {self.sc.n}", flush=True)

    @staticmethod
    def place_for(hand, side="r", hd=0.0, dist=300.0):
        """Where to stand (x, y), facing hd, so that `hand` is `dist` mm straight ahead of that shoulder (in plan)."""
        sx = 174.7 if side == "r" else -174.7
        c, s = math.cos(math.radians(hd)), math.sin(math.radians(hd))
        f = np.array([-s, c])                                   # the facing direction
        sh = np.asarray(hand, float)[:2] - f * dist
        off = np.array([c * sx - s * 15.2, s * sx + c * 15.2])
        return float(sh[0] - off[0]), float(sh[1] - off[1])

    def shoulder(self, side="r", x=None, y=None, hd=None):
        x = self.s["x"] if x is None else x
        y = self.s["y"] if y is None else y
        hd = self.s["hd"] if hd is None else hd
        sx = 174.7 if side == "r" else -174.7
        c, s = math.cos(math.radians(hd)), math.sin(math.radians(hd))
        return np.array([x + c * sx - s * 15.2, y + s * sx + c * 15.2, 1407.0])

    @staticmethod
    def stand_for(hand, side="r", hd=0.0, reach=440.0):
        """Where to stand (x, y) so that `hand` is `reach` mm from that shoulder, straight ahead of it."""
        hand = np.asarray(hand, float)
        dz = 1407.0 - hand[2]
        dxy = math.sqrt(max(reach ** 2 - dz ** 2, 60.0 ** 2))
        sx = 174.7 if side == "r" else -174.7
        c, s = math.cos(math.radians(hd)), math.sin(math.radians(hd))
        off = np.array([c * sx - s * (15.2 + dxy), s * sx + c * (15.2 + dxy)])
        return float(hand[0] - off[0]), float(hand[1] - off[1])

    def go(self, x=None, y=None, hd=None, lean=None, r="keep", l="keep", look="keep", grip_r=None, grip_l=None,
           palm_r="keep", palm_l="keep"):
        """update(u): to the targets. A hand target is xyz, a callable u -> xyz (followed exactly), or None (rest)."""
        st = {}

        def up(u):
            s = self.s
            if not st:
                st.update(x0=s["x"], y0=s["y"], hd0=s["hd"], lean0=s["lean"], ph0=s["phase"],
                          x1=s["x"] if x is None else x, y1=s["y"] if y is None else y,
                          hd1=s["hd"] if hd is None else hd, lean1=s["lean"] if lean is None else lean,
                          g0=dict(self.grip), look0=self.look)
                st["dist"] = math.hypot(st["x1"] - st["x0"], st["y1"] - st["y0"])
                for side in ("r", "l"):
                    cur = self.hand[side]
                    st[side] = np.asarray(cur if cur is not None else self.p.rest_hand(side), float)
            s["x"] = st["x0"] + (st["x1"] - st["x0"]) * u
            s["y"] = st["y0"] + (st["y1"] - st["y0"]) * u
            s["hd"] = st["hd0"] + (st["hd1"] - st["hd0"]) * u
            s["lean"] = st["lean0"] + (st["lean1"] - st["lean0"]) * u
            d = st["dist"]
            s["phase"] = st["ph0"] + 2 * math.pi * d * u / 1016.0
            s["amp"] = min(1.0, d / 350.0) * math.sin(math.pi * u) ** 0.7 if d > 1 else 0.0
            for side, tgt in (("r", r), ("l", l)):
                if isinstance(tgt, str):
                    continue
                if tgt is None:
                    if u >= 0.999:
                        self.hand[side] = None
                    else:
                        rest = self.p.rest_hand(side)
                        self.hand[side] = st[side] + (rest - st[side]) * u
                elif callable(tgt):
                    self.hand[side] = np.asarray(tgt(u), float)
                else:
                    self.hand[side] = st[side] + (np.asarray(tgt, float) - st[side]) * u
            if grip_r is not None:
                self.grip["r"] = st["g0"]["r"] + (grip_r - st["g0"]["r"]) * u
            if grip_l is not None:
                self.grip["l"] = st["g0"]["l"] + (grip_l - st["g0"]["l"]) * u
            if not isinstance(palm_r, str) or palm_r == "down":
                self.palm["r"] = palm_r
            if not isinstance(palm_l, str) or palm_l == "down":
                self.palm["l"] = palm_l
            if not (isinstance(look, str) and look == "keep"):
                self.look = look(u) if callable(look) else look
            self.apply()
        return up


# ------------------------------------------------------------------------------------------------- the tongs
class Tongs:
    """The furnace tongs in the operator's right hand: the hand grips the handles (local x = 45); the jaws' middle
    goes where a step says, the tongs pointing `yaw` degrees right of straight ahead and 20 deg down (the jaws are
    bent so they are level then)."""
    GRIP = 45.0
    PITCH = MP.TONGS["bend"]

    def __init__(self, sc, op, at, yaw=25.0):
        inst, ents = S.get("tongs")
        self.sc, self.op, self.yaw = sc, op, yaw
        self.rig = S.Rig(sc, inst, ents, "tongs:", at=at)
        self.mid = np.array([*MP.tongs_jaw_mid(), 1.0])

    @property
    def group(self):
        return "tongs:body"

    def pose_for(self, tip, yaw=None, pitch=None):
        yaw = self.yaw if yaw is None else yaw
        p = math.radians(self.PITCH if pitch is None else pitch)
        a = math.radians(yaw)
        d = np.array([math.sin(a) * math.cos(p), math.cos(a) * math.cos(p), -math.sin(p)])
        M = frame_along(np.zeros(3), d)
        M[:3, 3] = np.asarray(tip, float) - (M @ self.mid)[:3]
        return M

    def hand_for(self, tip, yaw=None):
        return (self.pose_for(tip, yaw) @ np.array([self.GRIP, 0.0, 0.0, 1.0]))[:3]

    def set_tip(self, tip, yaw=None):
        M = self.pose_for(tip, yaw)
        self.sc.gmat[self.group] = M
        self.op.hand["r"] = (M @ np.array([self.GRIP, 0.0, 0.0, 1.0]))[:3]
        self.op.grip["r"] = 0.85

    def tip(self):
        return (self.sc.world(self.group) @ self.mid)[:3]

    def move(self, path, body=None, yaw=None):
        """update(u): the jaws along `path` (from where they are), the hand with them; `body` (an Op.go update)
        moves the operator in the same frame, first."""
        st = {}

        def up(u):
            if body is not None:
                body(u)
            if not st:
                st["path"] = [self.tip()] + [np.asarray(p, float) for p in path]
            self.set_tip(along(st["path"], u), yaw)
            self.op.apply()
        return up

    def jaws(self, v0, v1):
        return self.rig.move({"arm_a": (v0, v1)})


# ------------------------------------------------------------------------------------------------- panels
def _font(px, bold=False, mono=False):
    return S.font(px, bold=bold, mono=mono)


def badge(d, x, y, text="synthetic example", s=1.0):
    f = _font(13 * s, bold=True)
    w = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + w + 16 * s, y + 22 * s), 5 * s, fill=(255, 244, 214, 255),
                        outline=(190, 140, 40, 255))
    d.text((x + 8 * s, y + 3 * s), text, font=f, fill=(120, 80, 10))


def card_image(w, h, title, s=2.0, tag=SYN):
    """A white rounded panel with a title and a badge; returns (img, draw, top of the content)."""
    img = Image.new("RGBA", (int(w * s), int(h * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), 10 * s, fill=(255, 255, 255, 238),
                        outline=(150, 156, 166, 255), width=max(1, int(1.2 * s)))
    d.text((14 * s, 10 * s), title, font=_font(17 * s, bold=True), fill=(20, 22, 30))
    if tag:
        f = _font(13 * s, bold=True)
        badge(d, img.width - d.textlength(tag, font=f) - 30 * s, 10 * s, tag, s)
    return img, d, 40 * s


def fig_panel(draw_fn, w=5.2, h=3.2, dpi=150, title=None, tag=SYN):
    """A matplotlib panel: draw_fn(ax) on a white rounded card with a title and the badge."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0.13, 0.17, 0.83, 0.62 if title else 0.78])
    draw_fn(ax)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    im = S.fig_image(fig, dpi)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    s = dpi / 100.0
    d.rounded_rectangle((0, 0, out.width - 1, out.height - 1), 10 * s, fill=(255, 255, 255, 240),
                        outline=(150, 156, 166, 255), width=max(1, int(1.2 * s)))
    out.alpha_composite(im)
    if title:
        d.text((12 * s, 8 * s), title, font=_font(12.5 * s, bold=True), fill=(20, 22, 30))
    if tag:
        f = _font(9.5 * s, bold=True)
        tw = d.textlength(tag, font=f)
        x0 = out.width - tw - 22 * s
        d.rounded_rectangle((x0, 8 * s, x0 + tw + 12 * s, 26 * s), 4 * s, fill=(255, 244, 214, 255),
                            outline=(190, 140, 40, 255))
        d.text((x0 + 6 * s, 10.5 * s), tag, font=f, fill=(120, 80, 10))
    return out


# ------------------------------------------------------------------------------------------------- synthetic data
TEMPS = (300, 350, 400)
TIMES = MP.TIMES_H


def synthetic_aging():
    """HV(t) and rho(t) for a candidate alloy at 300/350/400 C, generated from an Arrhenius peak time (Q = 120
    kJ/mol) and a JMAK transformation (n = 1.1) - the inputs the analysis should recover. Seeded noise."""
    rng = np.random.default_rng(4)
    Q, n = 120e3, 1.1
    T = np.array(TEMPS, float) + 273.15
    tpk = 4.0 * np.exp(Q / KIN.R * (1 / T - 1 / (350 + 273.15)))          # h: 4 h at 350 C
    k = math.log(2) ** (1 / n) / (0.45 * tpk * 3600)                       # f = 0.5 near 0.45 t_peak
    t = np.array(TIMES)
    out = {}
    rho0, rinf = 5.10, 3.95                                                 # uOhm cm, as-built and fully aged
    for i, Tc in enumerate(TEMPS):
        f = KIN.jmak(t * 3600, k[i], n)
        rho = rho0 - (rho0 - rinf) * f + rng.normal(0, 0.012, t.size)
        x = np.log(t / tpk[i])
        hv = 118 + (38 - 6 * i) * np.exp(-0.5 * (x / 1.25) ** 2) - 9 * (1 / (1 + np.exp(-(x - 1.2))))
        hv += rng.normal(0, 1.2, t.size)
        out[Tc] = dict(t=t, rho=rho, hv=hv, f_true=f, tpk_true=tpk[i])
    return out, dict(Q=Q, n=n, k=k, tpk=tpk, rho0=rho0, rinf=rinf)


# ===================================================================================================== chapter 2
def c2():
    """The aging series at the furnace."""
    sc = S.SOPScene("sop04_c2", TITLE)
    S.room(sc, x0=-1700, x1=1500, depth=900)
    FX, FY = 150.0, 40.0                                     # the furnace on the bench
    fur = S.place(sc, "furnace_hinged", FX, FY, prefix="furnace:")
    drop_piece(fur, "load")                                  # its own tray of tensile coupons: ours is the rack
    BX, BY = -330.0, -130.0
    bath = S.place(sc, "quench_bath", BX, BY, prefix="bath:")
    TILE = (-330.0, -345.0)
    sc.add("tile", S.pv.Box(bounds=(TILE[0] - 100, TILE[0] + 100, TILE[1] - 100, TILE[1] + 100, BENCH_H,
                                    BENCH_H + 8)), (0.93, 0.92, 0.88), "tile", specular=0.05)
    rack = S.place(sc, "aging_rack", TILE[0], TILE[1] + 22.0, BENCH_H + 8.0, prefix="rack:", shadow=False)
    timer = add_model(sc, "timer", MP.lab_timer(), T((-1080.0, -330.0, BENCH_H)) @ R((0, 0, 1), 10))
    op = Op(sc, -900.0, -1000.0, 0.0)
    for n in op.p.names():                                   # heat-resistant gloves (tan aramid) over the nitrile
        if n.endswith("/glove"):
            sc.color[n] = (0.80, 0.66, 0.40)
    lie = frame_along((-960.0, -400.0, BENCH_H + 7.0), (1, 0, 0), up=(0, 1, 0))
    tongs = Tongs(sc, op, lie)
    YAW = tongs.yaw
    F = __import__("instruments").FURNACE
    yf = -F["D"] / 2
    cz = F["mouth_z0"] + (F["mouth_h"] - F["ch_h"]) / 2
    floor_z = BENCH_H + cz                                   # the chamber floor's top
    fz = cz + F["ch_h"] / 2
    handle_l = (-F["W"] / 2 + 52, yf - 56.0, fz)             # the palm, in front of the handle bar
    RK = MP.RACK
    rack_c = np.array([FX - 1.0, FY + yf + 30 + 20 + 3 + 172.0, floor_z])   # the tray's place on the chamber floor

    def handle_w(u=None):
        return fur.world(handle_l, "door")

    def tray_tab(base):                                      # the tray's tab (the jaws' middle) for a tray at base
        return np.asarray(base, float) + np.array([-15.0, -RK["D"] / 2 - 15, MP.TRAY_TAB_Z + RK["t"] / 2])

    def boat_tab(base, i):
        return np.asarray(base, float) + np.array([MP.BOAT_X[i], -RK["boat_d"] / 2 - RK["tab_l"] + 8,
                                                   RK["tab_z"] + 0.4])

    au = audit.Audit(sc, allow=[("op/glove", "furnace:door/chrome*"), ("op/glove", "tongs:*"), ("op/glove", "timer*"),
                                ("op/glove", "furnace:body/nat_screen*"), ("tongs:*", "rack:*"),
                                ("rack:boat*", "bath:body/p4_water*"), ("rack:boat*", "bath:basket*"),
                                ("rack:boat*", "rack:boat*"), ("bath:basket*", "bath:body/p4_water*"),
                                ("op/glove", "bath:basket*"), ("tongs:body/p4_steel_dk*", "tongs:arm_a*"),
                                ("tongs:*", "bath:body/p4_water*")])

    # ---------------------------------------------------------------- views
    V_ALL = S.look((-250, -200, BENCH_H + 250), 3500, az=-14, el=16)
    V_BENCH = S.look((-420, -330, BENCH_H + 150), 1700, az=-38, el=26)
    V_CTRL = S.look((FX + 20, FY + yf, BENCH_H + 110), 1100, az=32, el=12)
    V_DOOR = S.look((FX - 80, FY + yf - 150, BENCH_H + 250), 1900, az=-48, el=18)
    V_MOUTH = S.look((FX - 60, FY + yf - 40, BENCH_H + 260), 1500, az=-52, el=20)
    V_IN = S.look((FX - 20, FY + yf + 120, BENCH_H + cz + 30), 900, az=-38, el=30)
    V_BATH = S.look((BX + 60, BY - 120, BENCH_H + 180), 1500, az=-46, el=28)
    V_RACK = S.look((TILE[0] + 20, TILE[1], BENCH_H + 20), 560, az=-20, el=42)
    sc.cam = V_ALL

    # ---------------------------------------------------------------- matrix panel state
    state = dict(done=set(), batch=None, n=0)

    def mpanel(u):
        return matrix_image(state["done"], state["batch"])

    def bump():
        state["n"] += 1
        sc.panels["matrix"]["u"] = state["n"] / 1000.0

    def mark(*cells):
        def f():
            state["done"].update(cells)
            bump()
        return f

    def set_batch(b):
        def f():
            state["batch"] = b
            bump()
        return f

    gauge(sc, "furnace", "22 °C")
    gauge(sc, "timer", "--:--")

    # ---------------------------------------------------------------- the station, the matrix, the rack
    sc.step("Aging", "The aging station: furnace, water bath, rack, tongs | Nabertherm NAT 15/65: 470 x 790 x 460 mm, "
            "to 650 °C, ±5 °C", 3.0, None, hold=1.2,
            labels=[("Nabertherm NAT 15/65, forced convection", fur.world((0, yf, 420)), (0.78, 0.16)),
                    ("water bath, 20 °C tap water", (BX, BY - 100, BENCH_H + 210), (0.40, 0.20)),
                    ("aging rack on a ceramic tile", (TILE[0], TILE[1], BENCH_H + 20), (0.40, 0.70)),
                    ("tongs, 16 in", (-760, -400, BENCH_H + 10), (0.12, 0.78)),
                    ("lab timer", (-1080, -340, BENCH_H + 70), (0.10, 0.50))])
    sc.panel("matrix", mpanel, rect=(0.635, 0.085, 0.355), u=0.0, alpha=0.0)
    sc.step("Samples", "16 conditions per alloy: as-built, then 3 temperatures x 5 times", 3.0,
            S.together(sc.fade_panel("matrix", 0, 1), call_at(0.1, mark(("as-built", 0)))), hold=2.0,
            cam_to=V_BENCH)
    sc.step("Samples", "The rack: five boats, one per time | each boat: candidate, AlSi10Mg, 6063, Scalmalloy-type",
            3.0, None, hold=2.0, cam_to=V_RACK,
            labels=[("boat 1: 0.25 h", rack.world((MP.BOAT_X[0], -40, 16)), (0.16, 0.26)),
                    ("boat 5: 64 h", rack.world((MP.BOAT_X[4], -40, 16)), (0.58, 0.20)),
                    ("coupons 10 x 10 x 3 mm", rack.world((MP.BOAT_X[2], 13, 6)), (0.64, 0.70)),
                    ("tab for the tongs", rack.world((-15, -RK["D"] / 2 - 15, 9)), (0.18, 0.80))])
    # ---------------------------------------------------------------- set the furnace (left hand)
    ctrl = fur.world((70, yf - 2, F["scr_z"] + 2))
    tgt = ctrl + np.array([0, -75, 30])
    pc = Op.place_for(tgt, "l", 0.0, 230)
    pc = (pc[0], min(pc[1], -720.0))
    sc.step("Batch 1", "Batch 1: set the furnace to 300 °C", 3.4,
            op.go(x=pc[0], y=pc[1], lean=26, l=tgt, look=ctrl, grip_l=0.15), hold=0.3, cam_to=V_CTRL)
    sc.step("Batch 1", "Batch 1: set the furnace to 300 °C | wait until it holds 300 ± 5 °C", 3.0,
            S.together(op.go(l=ctrl + np.array([0, -62, 26])),
                       lambda u: gauge(sc, "furnace", f"{22 + (300 - 22) * u:.0f} °C"),
                       call_at(0.4, set_batch(300))), hold=0.8)
    # ---------------------------------------------------------------- open the door (left hand), step back
    h0 = handle_w()
    p0 = Op.place_for(h0, "l", -30.0, 330)
    sc.step("Batch 1", "Heat-resistant gloves on; open the door", 2.6,
            op.go(x=p0[0], y=min(p0[1], -720.0), hd=-30.0, lean=6, l=h0, look=h0, grip_l=0.8), hold=0.1,
            cam_to=V_DOOR)
    DOOR_OPEN = 0.62

    def door_swing(v0, v1, hd0, hd1):
        door = fur.move({"door": (v0, v1)})
        st = {}

        def up(u):
            if not st:
                st["a"] = (op.s["x"], op.s["y"])
                fur.set(door=v1)
                b = Op.place_for(handle_w(), "l", hd1, 330)
                st["b"] = (b[0], min(b[1], -720.0))
                fur.set(door=v0)
            door(u)
            op.s["x"] = st["a"][0] + (st["b"][0] - st["a"][0]) * u
            op.s["y"] = st["a"][1] + (st["b"][1] - st["a"][1]) * u
            op.s["hd"] = hd0 + (hd1 - hd0) * u
            dd = math.hypot(st["b"][0] - st["a"][0], st["b"][1] - st["a"][1])
            op.s["phase"] += 2 * math.pi * dd * (u - st.get("u", 0.0)) / 1016.0
            st["u"] = u
            op.s["amp"] = min(1.0, dd / 350.0) * math.sin(math.pi * u) ** 0.7
            op.hand["l"] = handle_w()
            op.grip["l"] = 0.8
            op.look = handle_w()
            op.apply()
        return up
    sc.step("Batch 1", "Heat-resistant gloves on; open the door", 2.6, door_swing(0.0, DOOR_OPEN, -30.0, -45.0),
            hold=0.1)
    sc.step("Batch 1", "Heat-resistant gloves on; open the door", 1.0, op.go(l=None, grip_l=0.3, lean=0), hold=0.2)
    # ---------------------------------------------------------------- the tongs
    g_lie = (lie @ np.array([Tongs.GRIP, 0, 0, 1]))[:3]
    pt = Op.place_for(g_lie + np.array([0, 0, 60]), "r", 0.0, 150)
    sc.step("Batch 1", "Pick up the tongs", 3.0,
            op.go(x=pt[0], y=min(pt[1], -720.0), hd=0.0, lean=24, r=g_lie + np.array([0, -10, 45]), look=g_lie,
                  grip_r=0.3), hold=0.1, cam_to=V_BENCH)
    sc.step("Batch 1", "Pick up the tongs", 0.8, op.go(r=g_lie + np.array([0, -4, 26]), grip_r=0.85), hold=0.1)
    up_pose = lie.copy()
    up_pose[:3, 3] += (0, 0, 200)
    up_pose = up_pose @ R((1, 0, 0), -90)                   # jaws now one above the other
    tab0 = tray_tab(rack.world((0, 0, 0)))
    held0 = tongs.pose_for(tab0 + np.array([-60, -80, 120]))
    off = np.array([Tongs.GRIP, 0, 0, 1])

    def carry_tongs(A, B, body=None):
        def up(u):
            if body is not None:
                body(u)
            M = S.blend(A, B, u)
            sc.gmat[tongs.group] = M
            op.hand["r"] = (M @ off)[:3]
            op.grip["r"] = 0.85
            op.apply()
        return up
    sc.step("Batch 1", "Pick up the tongs", 1.6, carry_tongs(lie, up_pose, op.go(lean=8)), hold=0.1)
    pr = Op.place_for(tongs.hand_for(tab0), "r", -YAW, 300)
    sc.step("Batch 1", "Grip the tray's tab", 2.6,
            carry_tongs(up_pose, held0, op.go(x=pr[0], y=min(pr[1], -720.0), hd=-YAW, lean=10, look=tab0)),
            hold=0.1, cam_to=S.look((TILE[0] - 20, TILE[1] - 80, BENCH_H + 80), 1000, az=-50, el=26))
    sc.step("Batch 1", "Grip the tray's tab", 1.4,
            S.together(tongs.jaws(0.0, 1.0), tongs.move([tab0 + np.array([0, -30, 0]), tab0])), hold=0.0)
    sc.step("Batch 1", "Grip the tray's tab", 0.7, tongs.jaws(1.0, 0.0), hold=0.1)
    reparent(sc, "rack:body", tongs.group)
    # ---------------------------------------------------------------- into the chamber
    tab_in = tray_tab(rack_c)
    front = tab_in + np.array([-math.sin(math.radians(YAW)) * 230, -math.cos(math.radians(YAW)) * 230, 20])
    lifted = tab0 + np.array([0, -20, 60])
    pf = Op.place_for(tongs.hand_for(front), "r", -YAW, 300)
    pin = Op.place_for(tongs.hand_for(tab_in), "r", -YAW, 330)
    sc.step("Batch 1", "Into the hot chamber, quickly", 3.2,
            tongs.move([lifted, front], body=op.go(x=pf[0], y=min(pf[1], -720.0), hd=-YAW, lean=8, look=front)),
            hold=0.0, cam_to=V_MOUTH)
    sc.step("Batch 1", "Into the hot chamber, quickly", 2.0,
            tongs.move([tab_in + np.array([0, 0, 12]), tab_in], body=op.go(x=pin[0], y=min(pin[1], -720.0),
                                                                          lean=14)), hold=0.0, cam_to=V_IN)
    sc.step("Batch 1", "Release; tongs out", 0.7, tongs.jaws(0.0, 1.0), hold=0.0)
    reparent(sc, "rack:body", None)
    sc.step("Batch 1", "Release; tongs out", 1.6,
            tongs.move([front + np.array([0, 0, 15])], body=op.go(x=pf[0], y=min(pf[1], -720.0), lean=6)), hold=0.0)
    sc.step("Batch 1", "Release; tongs out", 0.5, tongs.jaws(1.0, 0.0), hold=0.0)

    # ---------------------------------------------------------------- close the door, start the timer
    def close_door():
        hd_open = -45.0
        pd = Op.place_for(handle_w(), "l", hd_open, 330)
        a = sc.step("Batch 1", "Close the door; start the timer", 1.6,
                    S.together(op.go(x=pd[0], y=min(pd[1], -720.0), hd=hd_open, l=handle_w(), grip_l=0.8,
                                     look=handle_w()),
                               tongs.move([front + np.array([-120, -60, 60])])), hold=0.0, cam_to=V_DOOR)
        sc.step("Batch 1", "Close the door; start the timer", 2.2, door_swing(DOOR_OPEN, 0.0, hd_open, -30.0),
                hold=0.0)
        sc.step("Batch 1", "Close the door; start the timer", 0.8, op.go(l=None, grip_l=0.3), hold=0.0)
        return a
    close_door()
    key = (sc.world("timer") @ np.array([-20.0, -12.0, 18.0, 1.0]))[:3]
    ptm = Op.place_for(key + np.array([0, -60, 40]), "l", 0.0, 220)
    sc.step("Batch 1", "Close the door; start the timer", 3.0,
            S.together(op.go(x=ptm[0], y=min(ptm[1], -720.0), hd=0.0, lean=20, l=key + np.array([0, -60, 40]),
                             look=key, grip_l=0.2),
                       tongs.move([key + np.array([520, 40, 260])])), hold=0.0,
            cam_to=S.look((-900, -330, BENCH_H + 120), 1300, az=-30, el=22))
    sc.step("Batch 1", "Close the door; start the timer | 300 °C: 0.25, 1, 4, 16, 64 h", 1.2,
            S.together(op.go(l=key + np.array([0, -46, 34])), call_at(0.5, lambda: gauge(sc, "timer", "0:00 h"))),
            hold=0.6)
    sc.step("Batch 1", "Close the door; start the timer | 300 °C: 0.25, 1, 4, 16, 64 h", 0.8, op.go(l=None),
            hold=0.0)

    # ---------------------------------------------------------------- a time point: a boat out, into the water
    tray_base = rack_c.copy()
    water_top = BENCH_H + MP.BATH["water"]
    basket_floor = BENCH_H + MP.BATH["t"] + 4.0 + 2.0

    def time_point(i, t_h, quick=False):
        k = 0.65 if quick else 1.0
        tag = f"{t_h:g} h"
        gauge(sc, "timer", f"{t_h:g}:00 h" if t_h >= 1 else "0:15 h")
        h0 = handle_w()
        p0 = Op.place_for(h0, "l", -30.0, 330)
        sc.step("300 °C", f"{tag}: open the door", 2.4 * k,
                S.together(op.go(x=p0[0], y=min(p0[1], -720.0), hd=-30.0, lean=6, l=h0, look=h0, grip_l=0.8),
                           tongs.move([h0 + np.array([-380, 120, -60])])), hold=0.0, cam_to=V_DOOR)
        sc.step("300 °C", f"{tag}: open the door", 2.2 * k, door_swing(0.0, DOOR_OPEN, -30.0, -45.0), hold=0.0)
        sc.step("300 °C", f"{tag}: open the door", 0.7 * k, op.go(l=None, grip_l=0.3), hold=0.0)
        bt = boat_tab(tray_base, i)
        bf = bt + np.array([-math.sin(math.radians(YAW)) * 230, -math.cos(math.radians(YAW)) * 230, 25])
        pb = Op.place_for(tongs.hand_for(bt), "r", -YAW, 330)
        pbf = Op.place_for(tongs.hand_for(bf), "r", -YAW, 300)
        sc.step("300 °C", f"{tag}: boat {i + 1} out with the tongs", 2.4 * k,
                tongs.move([bf], body=op.go(x=pbf[0], y=min(pbf[1], -720.0), hd=-YAW, lean=8, look=bt)), hold=0.0,
                cam_to=V_MOUTH)
        sc.step("300 °C", f"{tag}: boat {i + 1} out with the tongs", 1.6 * k,
                S.together(tongs.jaws(0.0, 1.0), tongs.move([bt + np.array([0, 0, 12]), bt],
                                                            body=op.go(x=pb[0], y=min(pb[1], -720.0), lean=14))),
                hold=0.0, cam_to=V_IN)
        sc.step("300 °C", f"{tag}: boat {i + 1} out with the tongs", 0.6 * k, tongs.jaws(1.0, 0.0), hold=0.0)
        g = f"rack:boat{i}"
        reparent(sc, g, tongs.group)
        over = np.array([BX + 10, BY - 20, water_top + 140])
        pw = Op.place_for(tongs.hand_for(over), "r", -YAW, 300)
        sc.step("300 °C", f"{tag}: straight into the water, within seconds", 2.6 * k,
                tongs.move([bt + np.array([0, 0, 20]), bf + np.array([0, 0, 10]), over],
                           body=op.go(x=pw[0], y=min(pw[1], -720.0), hd=-YAW, lean=6, look=over)), hold=0.0,
                cam_to=V_BATH)
        sc.step("300 °C", f"{tag}: straight into the water, within seconds", 0.4, tongs.jaws(0.0, 1.0), hold=0.0)
        reparent(sc, g, None)
        W0 = sc.gmat[g].copy()
        dz_air = over[2] - water_top
        st = {}

        def drop(u):
            if not st:
                # the boat's floor is RK["t"] + 0.8 over its group's origin: land it on the basket's floor
                zb = (sc.world(g) @ np.array([0, 0, RK["t"], 1.0]))[2]
                st["dz"] = basket_floor + 0.3 - zb
            ua = 0.35                         # free fall through the air, then slower through the water
            fall_air = min(dz_air - 25.0, -st["dz"])
            if u < ua:
                z = -fall_air * (u / ua) ** 2
            else:
                z = -fall_air + (st["dz"] + fall_air) * ((u - ua) / (1 - ua)) ** 0.8
            M = W0.copy()
            M[2, 3] = W0[2, 3] + z
            sc.gmat[g] = M
        sc.step("300 °C", f"{tag}: quenched | the coupons are now frozen at {tag}", 1.4, drop, hold=0.3)
        reparent(sc, g, "bath:basket")
        sc.step("300 °C", f"{tag}: quenched | the coupons are now frozen at {tag}", 0.6,
                S.together(tongs.jaws(1.0, 0.0), call_at(0.5, mark((300, t_h)))), hold=0.4)
        hd_open = -45.0
        pd = Op.place_for(handle_w(), "l", hd_open, 330)
        sc.step("300 °C", f"{tag}: close the door", 2.0 * k,
                S.together(op.go(x=pd[0], y=min(pd[1], -720.0), hd=hd_open, l=handle_w(), grip_l=0.8,
                                 look=handle_w()), tongs.move([front + np.array([-260, -140, 60])])),
                hold=0.0, cam_to=V_DOOR)
        sc.step("300 °C", f"{tag}: close the door", 2.0 * k, door_swing(DOOR_OPEN, 0.0, hd_open, -30.0), hold=0.0)
        sc.step("300 °C", f"{tag}: close the door", 0.7 * k, op.go(l=None, grip_l=0.3), hold=0.2)

    time_point(0, 0.25)
    time_point(1, 1.0, quick=True)
    # 4, 16 and 64 h: the same steps (a cut)
    for i in (2, 3, 4):
        g = f"rack:boat{i}"
        reparent(sc, g, None)
        W0 = sc.world(g)
        dst = T((BX - 60 + 45 * (i - 2), BY + 20 - 30 * (i - 2), 0)) @ np.eye(4)
        M = W0.copy()
        zb = (W0 @ np.array([0, 0, RK["t"], 1.0]))[2]
        M[:3, 3] = (BX - 75 + 40 * (i - 2) - MP.BOAT_X[i] * 0, BY + 25 - 28 * (i - 2), W0[2, 3] +
                    (basket_floor + 2.0 + 3.0 * (i - 1) - zb))
        sc.gmat[g] = M
        reparent(sc, g, "bath:basket")
    gauge(sc, "timer", "64:00 h")
    sc.step("300 °C", "4, 16 and 64 h: the same, one boat each | (cut)", 3.0,
            S.together(call_at(0.2, mark((300, 4.0))), call_at(0.5, mark((300, 16.0))),
                       call_at(0.8, mark((300, 64.0)))), hold=1.5, cam_to=V_BATH)
    # ---------------------------------------------------------------- the basket out
    bail = bath.world((0, 0, MP.BATH["H"] + 45))
    pbk = Op.place_for(bail + np.array([0, -60, 30]), "l", 0.0, 260)
    sc.step("300 °C", "Lift the basket out: dry, label, measure", 2.6,
            op.go(x=pbk[0], y=min(pbk[1], -720.0), hd=0.0, lean=12, l=bail + np.array([0, -14, 22]), grip_l=0.85,
                  look=bail), hold=0.0)

    def lift(u):
        bath.set(basket=170.0 * u)
        op.hand["l"] = bath.world((0, 0, MP.BATH["H"] + 45), "basket") + np.array([0, -14, 22])
        op.apply()
    sc.step("300 °C", "Lift the basket out: dry, label, measure | to hardness (c3) and conductivity (c4)", 2.4,
            lift, hold=1.2)
    # ---------------------------------------------------------------- the other batches
    sc.step("350 °C", "Batch 2: 350 °C, the same way | five fresh boats", 3.0,
            S.together(call_at(0.1, set_batch(350)), lambda u: gauge(sc, "furnace", "350 °C"),
                       *[call_at(0.3 + 0.13 * j, mark((350, t))) for j, t in enumerate(TIMES)]),
            hold=1.0, cam_to=V_ALL)
    sc.step("400 °C", "Batch 3: 400 °C, the same way", 3.0,
            S.together(call_at(0.1, set_batch(400)), lambda u: gauge(sc, "furnace", "400 °C"),
                       *[call_at(0.3 + 0.13 * j, mark((400, t))) for j, t in enumerate(TIMES)]), hold=1.0)
    sc.step("250 °C", "Sc/Zr/Er alloys: add a 250 °C batch | 21 conditions for those", 3.0,
            S.together(call_at(0.1, set_batch(250)), lambda u: gauge(sc, "furnace", "250 °C"),
                       *[call_at(0.3 + 0.13 * j, mark((250, t))) for j, t in enumerate(TIMES)]), hold=1.0)
    sc.step("Open question", "Furnace capacity: one temperature per batch | 64 h per batch: about 3 days each", 3.0,
            call_at(0.1, set_batch(None)), hold=2.0)
    return sc, au, locals()


def matrix_image(done, batch, s=2.0):
    """The aging matrix: rows as-built, 250 (Sc/Zr/Er alloys only), 300, 350, 400 C; columns the five times."""
    W, H = 520, 300
    img, d, top = card_image(W, H, "Aging matrix · one alloy", s, tag=None)
    f, fb = _font(13 * s), _font(13 * s, bold=True)
    x0, y0 = 120 * s, top + 26 * s
    cw, ch = 74 * s, 34 * s
    for j, t in enumerate(TIMES):
        d.text((x0 + j * cw + 14 * s, top + 4 * s), f"{t:g} h", font=fb, fill=(40, 44, 52))
    rows = [("as-built", None), ("250 °C*", 250), ("300 °C", 300), ("350 °C", 350), ("400 °C", 400)]
    for i, (name, Tc) in enumerate(rows):
        y = y0 + i * ch
        col = (120, 124, 132) if Tc == 250 else (30, 32, 40)
        d.text((14 * s, y + 8 * s), name, font=fb if Tc == batch else f, fill=col)
        if Tc is None:
            ok = ("as-built", 0) in done
            d.rounded_rectangle((x0, y + 3 * s, x0 + cw - 6 * s, y + ch - 3 * s), 4 * s,
                                fill=(60, 110, 70) if ok else (238, 240, 243), outline=(170, 176, 184))
            continue
        for j, t in enumerate(TIMES):
            ok = (Tc, t) in done
            fill = (60, 110, 70) if ok else ((246, 238, 220) if Tc == batch else (238, 240, 243))
            if Tc == 250 and not ok:
                fill = (246, 246, 247)
            d.rounded_rectangle((x0 + j * cw, y + 3 * s, x0 + j * cw + cw - 6 * s, y + ch - 3 * s), 4 * s,
                                fill=fill, outline=(170, 176, 184))
    n = sum(1 for c in done if c[0] != 250)
    d.text((14 * s, H * s - 46 * s), f"{n} of 16 conditions done · * 250 °C only for Sc/Zr/Er alloys", font=f,
           fill=(60, 64, 72))
    d.text((14 * s, H * s - 26 * s), "references (6063, AlSi10Mg, Scalmalloy-type) go through the same matrix",
           font=_font(12 * s), fill=(90, 94, 102))
    return img


# ===================================================================================================== main
CHAPTERS = {"sop04_c2": c2}


def run(name):
    sc, au, _ = CHAPTERS[name]()
    sc.save()
    au.save()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["join"]:
        parts = sorted(CHAPTERS)
        S.join("sop04", parts)
        S.contact_sheet("sop04")
        S.preview_gif("sop04")
    else:
        for a in args:
            run(a)
