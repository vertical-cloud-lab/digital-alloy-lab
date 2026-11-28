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
from models_props import box  # noqa: E402
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
        self.carry_r = False                 # the right hand holds the tongs: it moves with the body
        self.apply()

    def body_frame(self):
        c, s = math.cos(math.radians(self.s["hd"])), math.sin(math.radians(self.s["hd"]))
        M = np.eye(4)
        M[:2, :2] = [[c, -s], [s, c]]
        M[0, 3], M[1, 3] = self.s["x"], self.s["y"]
        return M

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
           palm_r="keep", palm_l="keep", via_r=None, via_l=None):
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
                if self.carry_r and isinstance(r, str) and self.hand["r"] is not None:
                    st["carry"] = np.linalg.inv(self.body_frame()) @ np.r_[self.hand["r"], 1.0]
            s["x"] = st["x0"] + (st["x1"] - st["x0"]) * u
            s["y"] = st["y0"] + (st["y1"] - st["y0"]) * u
            s["hd"] = st["hd0"] + (st["hd1"] - st["hd0"]) * u
            s["lean"] = st["lean0"] + (st["lean1"] - st["lean0"]) * u
            d = st["dist"]
            s["phase"] = st["ph0"] + 2 * math.pi * d * u / 1016.0
            s["amp"] = min(1.0, d / 350.0) * math.sin(math.pi * u) ** 0.7 if d > 1 else 0.0
            if "carry" in st:
                self.hand["r"] = (self.body_frame() @ st["carry"])[:3]
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
                    via = via_r if side == "r" else via_l
                    if via:
                        self.hand[side] = along([st[side]] + [np.asarray(v, float) for v in via]
                                                + [np.asarray(tgt, float)], u)
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

    def move(self, path, body=None, yaw=None, follow=None, ymax=-760.0):
        """update(u): the jaws along `path` (from where they are), the hand with them; `body` (an Op.go update)
        moves the operator in the same frame, first. follow=(hd, dist, lean): the operator walks so that the hand
        stays `dist` mm ahead of the right shoulder (starting from where they stand, so nothing jumps)."""
        st = {}
        op = self.op

        def up(u):
            if not st and "r" in op.p.held:
                op.p.let_go("r")
            if body is not None:
                body(u)
            if not st:
                st["path"] = [self.tip()] + [np.asarray(p, float) for p in path]
                if follow is not None:
                    hd, dist, lean = follow
                    h0 = self.hand_for(st["path"][0], yaw)
                    p0 = np.array(Op.place_for(h0, "r", hd, dist))
                    p0[1] = min(p0[1], ymax)
                    st.update(start=np.array([op.s["x"], op.s["y"]]), p0=p0, hd0=op.s["hd"], lean0=op.s["lean"],
                              last=np.array([op.s["x"], op.s["y"]]))
                    h1 = self.hand_for(st["path"][-1], yaw)
                    p1 = np.array(Op.place_for(h1, "r", hd, dist))
                    p1[1] = min(p1[1], ymax)
                    st["walk"] = float(np.linalg.norm(p1 - st["start"]))
            tip = along(st["path"], u)
            if follow is not None:
                hd, dist, lean = follow
                hand = self.hand_for(tip, yaw)
                pu = np.array(Op.place_for(hand, "r", hd, dist))
                pu[1] = min(pu[1], ymax)
                xy = pu + (1 - u) * (st["start"] - st["p0"])
                op.s["phase"] += 2 * math.pi * float(np.linalg.norm(xy - st["last"])) / 1016.0
                st["last"] = xy
                op.s.update(x=float(xy[0]), y=float(xy[1]), hd=st["hd0"] + (hd - st["hd0"]) * u,
                            lean=st["lean0"] + (lean - st["lean0"]) * u)
                op.s["amp"] = min(1.0, st["walk"] / 350.0) * math.sin(math.pi * u) ** 0.7
            self.set_tip(tip, yaw)
            op.apply()
            self.stick()
            if u >= 1.0:
                self.grab()
        return up

    def lower(self, hd=None):
        """update(u): the tongs to the right side, pointing 60 deg down and forward, the hand by the hip, so the
        left hand can work a door or a timer; they ride the body from then on."""
        st = {}
        op = self.op

        def low_pose():
            F = op.body_frame()
            d = F[:3, :3] @ unit(np.array([0.30, -0.10, 0.95]))         # held upright at the side, like a pole
            hand = (F @ np.array([300.0, 0.0, 1030.0, 1.0]))[:3]
            M = frame_along(np.zeros(3), d)
            M[:3, 3] = hand - M[:3, :3] @ np.array([self.GRIP, 0.0, 0.0])
            return M

        def up(u):
            if not st:
                if "r" in op.p.held:
                    op.p.let_go("r")
                st["a"] = self.sc.world(self.group).copy()
            M = S.blend(st["a"], low_pose(), u)
            self.sc.gmat[self.group] = M
            op.hand["r"] = (M @ np.array([self.GRIP, 0.0, 0.0, 1.0]))[:3]
            op.grip["r"] = 0.85
            op.apply()
            if u >= 1.0:
                self.grab()
        return up

    def grab(self):
        """From now on the tongs ride the right hand (until the next move)."""
        self.op.p.hold("r", self.group)
        self.op.carry_r = True

    def stick(self):
        """While the operator walks, the hand lags the IK target by a few cm: keep the tongs in the hand then."""
        a = self.op.s.get("amp", 0.0)
        if a > 0.02 and self.op.hand["r"] is not None:
            d = self.op.p.hand_point("r") - np.asarray(self.op.hand["r"], float)
            M = self.sc.gmat[self.group].copy()
            M[:3, 3] += d * min(1.0, a / 0.3)
            self.sc.gmat[self.group] = M

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
        badge(d, img.width - d.textlength(tag, font=f) - 30 * s, img.height - 32 * s, tag, s)
    return img, d, 40 * s


def fig_panel(draw_fn, w=5.2, h=3.2, dpi=150, title=None, tag=SYN):
    """A matplotlib panel: draw_fn(ax) on a white rounded card with a title and the badge."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0.13, 0.21, 0.80, 0.60 if title else 0.74])
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
        y0 = out.height - 26 * s
        d.rounded_rectangle((x0, y0, x0 + tw + 12 * s, y0 + 18 * s), 4 * s, fill=(255, 244, 214, 255),
                            outline=(190, 140, 40, 255))
        d.text((x0 + 6 * s, y0 + 2.5 * s), tag, font=f, fill=(120, 80, 10))
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
    # a check thermocouple: a fine type K wire through the door seal on the hinge side, its bead on the chamber floor
    # beside the tray's place, and its reader on the bench right of the furnace (Edison v3: start the soak only when
    # it is back at set point)
    TCR = (520.0, -330.0)
    add_model(sc, "tcr", MP.tc_reader(), T((TCR[0], TCR[1], BENCH_H)))
    cz_ = __import__("instruments").FURNACE
    zfl = BENCH_H + cz_["mouth_z0"] + (cz_["mouth_h"] - cz_["ch_h"]) / 2
    pts = np.array([(TCR[0], TCR[1], BENCH_H + 154), (TCR[0] - 40, TCR[1] + 10, BENCH_H + 60),
                    (TCR[0] - 110, TCR[1] - 20, BENCH_H + 1.2), (FX + 175, FY - 405, BENCH_H + 1.2),
                    (FX + 158, FY - 400, BENCH_H + 160), (FX + 158, FY - 380, zfl + 60),
                    (FX + 156, FY - 330, zfl + 30), (FX + 120, FY - 250, zfl + 4), (FX + 100, FY - 210, zfl + 1.2)])
    sp = S.pv.Spline(pts, 160)
    sc.add("tc/wire", sp.tube(radius=0.9, n_sides=8), (0.75, 0.62, 0.20), "tc", specular=0.2)
    sc.add("tc/bead", S.pv.Sphere(radius=1.6, center=tuple(pts[-1] + np.array([0, 0, 0.5]))), (0.55, 0.55, 0.57), "tc")
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
    handle_l = (-F["W"] / 2 + 52, yf - 115.0, fz)            # the palm, in front of the handle bar
    RK = MP.RACK
    rack_c = np.array([FX - 1.0, FY + yf + 30 + 20 + 3 + 172.0, floor_z + 0.5])   # the tray's place, chamber floor

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
                                ("tongs:*", "bath:body/p4_water*"), ("tc/*", "furnace:*")])

    # ---------------------------------------------------------------- views
    V_ALL = S.look((-300, -250, BENCH_H + 250), 3600, az=-10, el=16)
    V_BENCH = S.look((-420, -330, BENCH_H + 150), 1900, az=32, el=26)
    V_CTRL = S.look((FX + 20, FY + yf - 120, BENCH_H + 200), 1500, az=56, el=18)
    V_DOOR = S.look((FX - 130, FY + yf - 280, BENCH_H + 280), 2200, az=48, el=22)
    V_MOUTH = S.look((FX - 60, FY + yf + 20, BENCH_H + 250), 1700, az=24, el=27)
    V_IN = S.look((FX - 10, FY + yf + 150, BENCH_H + cz + 20), 1000, az=20, el=33)
    V_BATH = S.look((BX - 20, BY - 120, BENCH_H + 160), 1500, az=36, el=42)
    V_RACK = S.look((TILE[0] + 20, TILE[1], BENCH_H + 20), 560, az=-20, el=42)
    V_TONGS = S.look((-900, -560, BENCH_H + 200), 1600, az=60, el=30)
    V_TRAY = S.look((TILE[0] - 160, TILE[1] - 260, BENCH_H + 180), 1600, az=62, el=32)
    V_TIMER = S.look((-950, -480, BENCH_H + 200), 1500, az=-80, el=26)
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
                    ("lab timer", (-1080, -340, BENCH_H + 70), (0.10, 0.50)),
                    ("check thermocouple and reader", (520, -345, BENCH_H + 120), (0.86, 0.60))])
    sc.panel("matrix", mpanel, rect=(0.735, 0.085, 0.26), u=0.0, alpha=0.0)
    show_m, hide_m = sc.fade_panel("matrix", 0, 1), sc.fade_panel("matrix", 1, 0)
    sc.step("Samples", "16 conditions per alloy: as-built, then 3 temperatures x 5 times", 3.0,
            S.together(show_m, call_at(0.1, mark(("as-built", 0)))), hold=2.0,
            cam_to=V_BENCH)
    sc.step("Samples", "The rack: five boats, one per time | each boat: candidate, AlSi10Mg, 6063, Scalmalloy-type",
            3.0, hide_m, hold=2.0, cam_to=V_RACK,
            labels=[("boat 1: 0.25 h", rack.world((MP.BOAT_X[0], -40, 16)), (0.16, 0.26)),
                    ("boat 5: 64 h", rack.world((MP.BOAT_X[4], -40, 16)), (0.58, 0.20)),
                    ("coupons 10 x 10 x 3 mm", rack.world((MP.BOAT_X[2], 13, 6)), (0.64, 0.70)),
                    ("tab for the tongs", rack.world((-15, -RK["D"] / 2 - 15, 9)), (0.18, 0.80))])
    # ---------------------------------------------------------------- set the furnace (left hand)
    ctrl = fur.world((40, yf - 2, F["scr_z"] + 2))
    tgt = ctrl + np.array([0, -75, 30])
    pc = Op.place_for(tgt, "r", 0.0, 230)
    pc = (pc[0], min(pc[1], -760.0))
    sc.step("Batch 1", "Batch 1: set the furnace to 300 °C", 3.4,
            op.go(x=pc[0], y=pc[1], lean=26, r=tgt, look=ctrl, grip_r=0.15), hold=0.3, cam_to=V_CTRL)
    sc.step("Batch 1", "Batch 1: set the furnace to 300 °C | wait until it holds 300 ± 5 °C", 3.0,
            S.together(op.go(r=ctrl + np.array([0, -62, 26])),
                       lambda u: (gauge(sc, "furnace", f"{22 + (300 - 22) * u:.0f} °C"),
                                  gauge(sc, "check TC", f"{22 + (300 - 22) * u:.0f} °C")),
                       call_at(0.4, set_batch(300)), show_m), hold=0.8)
    # ---------------------------------------------------------------- open the door (left hand), step back
    h0 = handle_w()
    p0 = Op.place_for(h0, "l", -30.0, 430)
    sc.step("Batch 1", "Heat-resistant gloves on; open the door", 2.6,
            S.together(op.go(x=p0[0], y=min(p0[1], -760.0), hd=-30.0, lean=6, l=h0, r=None, look=h0, grip_l=0.8,
                             grip_r=0.3), hide_m), hold=0.1, cam_to=V_DOOR)
    DOOR_OPEN = 0.70

    def door_swing(v0, v1, hd0, hd1):
        door = fur.move({"door": (v0, v1)})
        st = {}

        def up(u):
            if not st:
                if op.carry_r and op.hand["r"] is not None:
                    st["carry"] = np.linalg.inv(op.body_frame()) @ np.r_[op.hand["r"], 1.0]
                st["a"] = (op.s["x"], op.s["y"])
                fur.set(door=v1)
                b = Op.place_for(handle_w(), "l", hd1, 430)
                st["b"] = (b[0], min(b[1], -760.0))
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
            if "carry" in st:
                op.hand["r"] = (op.body_frame() @ st["carry"])[:3]
            op.apply()
        return up
    sc.step("Batch 1", "Heat-resistant gloves on; open the door", 2.6, door_swing(0.0, DOOR_OPEN, -30.0, -45.0),
            hold=0.1)
    sc.step("Batch 1", "Heat-resistant gloves on; open the door", 1.0, op.go(l=None, grip_l=0.3, lean=0), hold=0.2)
    # ---------------------------------------------------------------- the tongs
    g_lie = (lie @ np.array([Tongs.GRIP, 0, 0, 1]))[:3]
    pt = Op.place_for(g_lie + np.array([0, 0, 60]), "r", 0.0, 150)
    sc.step("Batch 1", "Pick up the tongs", 3.0,
            op.go(x=pt[0], y=min(pt[1], -760.0), hd=0.0, lean=24, r=g_lie + np.array([0, -10, 80]), look=g_lie,
                  grip_r=0.3), hold=0.1, cam_to=V_TONGS)
    sc.step("Batch 1", "Pick up the tongs", 0.8, op.go(r=g_lie + np.array([0, -4, 80]), grip_r=0.85), hold=0.1)
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
            if u >= 1.0:
                tongs.grab()
        return up
    sc.step("Batch 1", "Pick up the tongs", 1.6, carry_tongs(lie, up_pose, op.go(lean=8)), hold=0.1)
    pr = Op.place_for(tongs.hand_for(tab0), "r", -YAW, 300)
    sc.step("Batch 1", "Grip the tray's tab", 2.6,
            carry_tongs(up_pose, held0, op.go(x=pr[0], y=min(pr[1], -760.0), hd=-YAW, lean=10, look=tab0)),
            hold=0.1, cam_to=V_TRAY)
    sc.step("Batch 1", "Grip the tray's tab", 1.4,
            S.together(tongs.jaws(0.0, 1.0), tongs.move([tab0 + np.array([0, -30, 0]), tab0])), hold=0.0)
    sc.step("Batch 1", "Grip the tray's tab", 0.7, tongs.jaws(1.0, 0.0), hold=0.1)
    reparent(sc, "rack:body", tongs.group)
    # ---------------------------------------------------------------- into the chamber
    tab_in = tray_tab(rack_c)
    front = tab_in + np.array([0.0, -290.0, 20.0])          # straight in front of its place: in along +y
    lifted = tab0 + np.array([0, -80, 70])
    pf = Op.place_for(tongs.hand_for(front), "r", -YAW, 300)
    pin = Op.place_for(tongs.hand_for(tab_in), "r", -YAW, 330)
    sc.step("Batch 1", "Into the hot chamber, quickly", 3.2,
            tongs.move([lifted, front], follow=(-YAW, 300, 8)), hold=0.0, cam_to=V_MOUTH)
    sc.step("Batch 1", "Into the hot chamber, quickly", 2.0,
            tongs.move([tab_in + np.array([0, 0, 12]), tab_in], follow=(-YAW, 330, 14)), hold=0.0, cam_to=V_IN)
    sc.step("Batch 1", "Release; tongs out", 0.7, tongs.jaws(0.0, 1.0), hold=0.0)
    reparent(sc, "rack:body", None)
    sc.step("Batch 1", "Release; tongs out", 1.6,
            tongs.move([front + np.array([0, 0, 15])], follow=(-YAW, 300, 6)), hold=0.0)
    sc.step("Batch 1", "Release; tongs out", 0.5, tongs.jaws(1.0, 0.0), hold=0.0)

    # ---------------------------------------------------------------- close the door, start the timer
    def close_door():
        hd_open = -45.0
        pd = Op.place_for(handle_w(), "l", hd_open, 430)
        a = sc.step("Batch 1", "Close the door; start the timer", 1.6,
                    S.together(op.go(x=pd[0], y=min(pd[1], -760.0), hd=hd_open, l=handle_w(), grip_l=0.8,
                                     look=handle_w()), tongs.lower()), hold=0.0, cam_to=V_DOOR)
        sc.step("Batch 1", "Close the door; start the timer", 2.2, door_swing(DOOR_OPEN, 0.0, hd_open, -30.0),
                hold=0.0)
        sc.step("Batch 1", "Close the door; start the timer", 0.8, op.go(l=None, grip_l=0.3), hold=0.0)
        return a
    close_door()
    key = (sc.world("timer") @ np.array([-20.0, -12.0, 18.0, 1.0]))[:3]
    ptm = Op.place_for(key + np.array([0, -60, 40]), "l", 0.0, 220)
    sc.step("Batch 1", "Close the door; start the timer", 3.0,
            op.go(x=ptm[0], y=min(ptm[1], -760.0), hd=0.0, lean=20, l=key + np.array([0, -60, 78]),
                  look=key, grip_l=0.2), hold=0.0, cam_to=V_TIMER)
    sc.step("Batch 1", "Start the clock when the check thermocouple is back at 300 °C", 1.6,
            S.together(lambda u: gauge(sc, "check TC", f"{262 + 38 * u:.0f} °C"),
                       op.go(l=key + np.array([0, -46, 72]))), hold=0.4)
    sc.step("Batch 1", "Start the clock when the check thermocouple is back at 300 °C | then 0.25, 1, 4, 16, 64 h",
            0.8, call_at(0.5, lambda: gauge(sc, "timer", "0:00 h")), hold=0.8)
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
        p0 = Op.place_for(h0, "l", -30.0, 430)
        sc.step("300 °C", f"{tag}: open the door", 2.4 * k,
                S.together(op.go(x=p0[0], y=min(p0[1], -760.0), hd=-30.0, lean=6, l=h0, look=h0, grip_l=0.8),
                           tongs.lower()), hold=0.0, cam_to=V_DOOR)
        sc.step("300 °C", f"{tag}: open the door", 2.2 * k, door_swing(0.0, DOOR_OPEN, -30.0, -45.0), hold=0.0)
        sc.step("300 °C", f"{tag}: open the door", 0.7 * k, op.go(l=None, grip_l=0.3), hold=0.0)
        bt = boat_tab(tray_base, i)
        bf = bt + np.array([0.0, -300.0, 25.0])             # straight out of the mouth first
        pb = Op.place_for(tongs.hand_for(bt), "r", -YAW, 330)
        pbf = Op.place_for(tongs.hand_for(bf), "r", -YAW, 300)
        sc.step("300 °C", f"{tag}: boat {i + 1} out with the tongs", 2.4 * k,
                S.together(op.go(look=bt), tongs.move([bf], follow=(-YAW, 300, 8))), hold=0.0, cam_to=V_MOUTH)
        sc.step("300 °C", f"{tag}: boat {i + 1} out with the tongs", 1.6 * k,
                S.together(tongs.jaws(0.0, 1.0), tongs.move([bt + np.array([0, 0, 12]), bt], follow=(-YAW, 330, 14))),
                hold=0.0, cam_to=V_IN)
        sc.step("300 °C", f"{tag}: boat {i + 1} out with the tongs", 0.6 * k, tongs.jaws(1.0, 0.0), hold=0.0)
        g = f"rack:boat{i}"
        reparent(sc, g, tongs.group)
        over = np.array([BX + 10, BY - 72, water_top + 140])
        pw = Op.place_for(tongs.hand_for(over), "r", -YAW, 300)
        sc.step("300 °C", f"{tag}: straight into the water, within seconds", 2.6 * k,
                S.together(op.go(look=over), tongs.move([bt + np.array([0, 0, 20]), bf + np.array([0, 0, 10]), over],
                                                         follow=(-YAW, 300, 6))), hold=0.0, cam_to=V_BATH)
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
                S.together(tongs.jaws(1.0, 0.0), call_at(0.5, mark((300, t_h))), show_m), hold=0.8)
        hd_open = -45.0
        pd = Op.place_for(handle_w(), "l", hd_open, 430)
        sc.step("300 °C", f"{tag}: close the door", 2.0 * k,
                S.together(op.go(x=pd[0], y=min(pd[1], -760.0), hd=hd_open, l=handle_w(), grip_l=0.8,
                                 look=handle_w()), tongs.lower(), hide_m), hold=0.0, cam_to=V_DOOR)
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
        M[:3, 3] = (BX - 75 + 40 * (i - 2) - MP.BOAT_X[i] * 0, BY + 36 - 26 * (i - 2), W0[2, 3] +
                    (basket_floor + 2.0 + 3.0 * (i - 1) - zb))
        sc.gmat[g] = M
        reparent(sc, g, "bath:basket")
    gauge(sc, "timer", "64:00 h")
    sc.step("300 °C", "4, 16 and 64 h: the same, one boat each | (cut)", 3.0,
            S.together(call_at(0.2, mark((300, 4.0))), call_at(0.5, mark((300, 16.0))),
                       call_at(0.8, mark((300, 64.0))), show_m), hold=1.5, cam_to=V_BATH)
    # ---------------------------------------------------------------- the basket out
    bail = bath.world((0, 0, MP.BATH["H"] + 45))
    pbk = Op.place_for(bail + np.array([0, -60, 30]), "l", 0.0, 260)
    sc.step("300 °C", "Lift the basket out: dry, label, measure", 2.6,
            S.together(op.go(x=pbk[0], y=min(pbk[1], -760.0), hd=0.0, lean=12, l=bail + np.array([0, -14, 22]),
                             grip_l=0.85, look=bail, via_l=[bail + np.array([0, -200, 60])]), hide_m), hold=0.0)

    def lift(u):
        bath.set(basket=170.0 * u)
        op.hand["l"] = bath.world((0, 0, MP.BATH["H"] + 45), "basket") + np.array([0, -14, 22])
        op.apply()
    sc.step("300 °C", "Lift the basket out: dry, label, measure | to hardness (c3) and conductivity (c4)", 2.4,
            lift, hold=1.2)
    # ---------------------------------------------------------------- the other batches
    sc.step("350 °C", "Batch 2: 350 °C, the same way | five fresh boats", 3.0,
            S.together(call_at(0.1, set_batch(350)), lambda u: gauge(sc, "furnace", "350 °C"), show_m,
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


# ===================================================================================================== chapter 3
def vickers_hv(F_kgf, d1_um, d2_um):
    """HV = 1.8544 F / d^2 (F in kgf, d the mean diagonal in mm), ASTM E384."""
    d = 0.5 * (d1_um + d2_um) / 1000.0
    return 1.8544 * F_kgf / d ** 2


def indent_image(u, s=2.0):
    """The indent as the camera sees it at 50x, with both diagonals measured (synthetic values)."""
    W, H = 330, 300
    img, d, top = card_image(W, H, "Indent at 50x: both diagonals", s)
    cx, cy, R = W * s / 2, top + 118 * s, 82 * s
    d.rectangle((cx - 150 * s, cy - 104 * s, cx + 150 * s, cy + 104 * s), fill=(176, 178, 182))
    for k in range(9):                                  # a few cell walls of the as-built microstructure, faint
        yy = cy - 100 * s + 25 * k * s
        d.line((cx - 150 * s, yy, cx + 150 * s, yy + 6 * s), fill=(166, 168, 172), width=max(1, int(s)))
    d.polygon([(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)], fill=(70, 72, 78))
    d.line((cx, cy - R, cx, cy + R), fill=(60, 60, 66), width=max(1, int(s)))
    d.line((cx - R, cy, cx + R, cy), fill=(60, 60, 66), width=max(1, int(s)))
    a = min(1.0, u * 2)
    b = min(1.0, max(0.0, u * 2 - 1))
    if a > 0:
        d.line((cx - R, cy, cx - R + 2 * R * a, cy), fill=(30, 110, 200), width=int(3 * s))
    if b > 0:
        d.line((cx, cy - R, cx, cy - R + 2 * R * b), fill=(200, 120, 20), width=int(3 * s))
    f = _font(13 * s, mono=True)
    d1, d2 = 86.2, 85.9
    hv = vickers_hv(0.5, d1, d2)
    d.text((14 * s, H * s - 58 * s), f"d1 {d1:.1f} um   d2 {d2:.1f} um", font=f, fill=(30, 40, 60))
    d.text((14 * s, H * s - 34 * s), f"HV0.5 = 1.8544 x 0.5 / d^2 = {hv:.0f}", font=_font(13.5 * s, bold=True),
           fill=(30, 60, 140))
    return img


def spacing_image(u, s=2.0):
    """The coupon face with ten indents, 2.5 d apart and from the edges (to scale, d = 86 um)."""
    W, H = 360, 290
    img, d, top = card_image(W, H, "10 indents, spacing >= 2.5 d", s)
    # the face: 10 x 10 mm XZ section (build direction up); a strip of it 3 mm wide is drawn
    x0, y0, sc_ = 20 * s, top + 16 * s, 100 * s          # px per mm
    w_mm, h_mm = 3.2, 1.6
    d.rectangle((x0, y0, x0 + w_mm * sc_, y0 + h_mm * sc_), fill=(186, 188, 192), outline=(120, 124, 130))
    dd = 0.086
    pitch = 0.30
    n = int(round(10 * min(1.0, u * 1.2)))
    for i in range(10):
        if i >= n:
            break
        cx = x0 + (0.25 + i * pitch) * sc_
        cy = y0 + 0.8 * sc_
        r = dd / 2 * sc_ * 1.41
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=(60, 62, 68))
    f = _font(12 * s)
    d.text((x0, y0 + h_mm * sc_ + 8 * s), "d = 86 um: neighbours >= 2.5 d = 0.22 mm apart (0.30 drawn),", font=f,
           fill=(40, 44, 52))
    d.text((x0, y0 + h_mm * sc_ + 26 * s), "and >= 2.5 d from any edge. To scale. Reject any that hit a pore.", font=f,
           fill=(40, 44, 52))
    return img


def hv_table_image(u, s=2.0):
    rng = np.random.default_rng(7)
    vals = np.round(124.0 + rng.normal(0, 2.4, 10), 1)
    W, H = 330, 300
    img, d, top = card_image(W, H, "HV0.5, one sample: mean ± SD", s)
    f = _font(13 * s, mono=True)
    for i, v in enumerate(vals):
        col, row = i // 5, i % 5
        d.text((22 * s + col * 150 * s, top + 6 * s + row * 24 * s), f"{i + 1:2d}  {v:6.1f}", font=f,
               fill=(30, 34, 42))
    m, sd = float(vals.mean()), float(vals.std(ddof=1))
    d.text((22 * s, top + 140 * s), f"mean {m:.1f} ± {sd:.1f} HV0.5", font=_font(15 * s, bold=True), fill=(30, 60, 140))
    ok = sd / m * 100
    d.text((22 * s, top + 166 * s), f"SD = {ok:.1f} % of the mean (accept < 5 %)", font=_font(13 * s),
           fill=(40, 100, 50))
    return img


def track_image(u, s=2.0):
    """Single tracks (SOP 02) in cross-section: one HV0.05 indent inside each fusion zone."""
    W, H = 380, 270
    img, d, top = card_image(W, H, "Single tracks: HV0.05, one per track", s)
    sub_y = top + 70 * s
    d.rectangle((14 * s, sub_y, W * s - 14 * s, H * s - 60 * s), fill=(150, 152, 156))
    scale = 0.40 * s                                      # px per um
    for k, (w_um, dep, P) in enumerate(((140, 80, 150), (160, 105, 200), (175, 140, 250), (190, 185, 300))):
        cx = 64 * s + k * 84 * s
        rx, ry = w_um / 2 * scale, dep * scale
        d.pieslice((cx - rx, sub_y - ry, cx + rx, sub_y + ry), 0, 180, fill=(196, 198, 202), outline=(110, 112, 118))
        d.chord((cx - rx, sub_y - 0.35 * ry, cx + rx, sub_y + 0.35 * ry), 180, 360, fill=(196, 198, 202))
        r = 28 / 2 * scale                                # HV0.05 at ~120 HV: diagonal d = 28 um
        iy = sub_y + 0.35 * ry
        d.polygon([(cx, iy - r), (cx + r, iy), (cx, iy + r), (cx - r, iy)], fill=(50, 52, 58))
        d.text((cx - 22 * s, sub_y - 0.35 * ry - 20 * s), f"{P} W", font=_font(11 * s), fill=(60, 64, 72))
    d.text((14 * s, H * s - 50 * s), "melt pools and d = 28 um to scale; one indent per track,", font=_font(12 * s),
           fill=(40, 44, 52))
    d.text((14 * s, H * s - 30 * s), "inside the fusion zone, away from its boundary", font=_font(12 * s),
           fill=(40, 44, 52))
    return img


def hv_line_image(u, s=2.0):
    def draw(ax):
        z = np.arange(0.3, 9.8, 0.5)
        rng = np.random.default_rng(11)
        hv = 121 + 4.5 * np.exp(-(9.7 - z) / 1.2) + rng.normal(0, 1.6, z.size)
        n = max(2, int(round(len(z) * min(1.0, u * 1.15))))
        ax.plot(z[:n], hv[:n], "o-", color="#1f4e8c", ms=4, lw=1.4)
        ax.set_xlim(0, 10)
        ax.set_ylim(110, 136)
        ax.set_xlabel("height in the build, mm (XZ section)")
        ax.set_ylabel("HV0.5")
    return fig_panel(draw, 5.0, 3.0, title="Auto-stage: a line across the build height")


def tabor_image(u, s=2.0):
    W, H = 400, 236
    img, d, top = card_image(W, H, "Tabor: a screen, not a strength", s, tag="computed")
    f, fb = _font(13.5 * s), _font(14 * s, bold=True)
    hv = 124.0
    H_MPa = 9.807 * hv
    d.text((16 * s, top + 8 * s), "σy ≈ H / 3, with H in MPa:", font=f, fill=(30, 34, 42))
    d.text((16 * s, top + 34 * s), f"H = 9.807 x {hv:.0f} HV = {H_MPa:.0f} MPa", font=_font(13.5 * s, mono=True),
           fill=(30, 34, 42))
    d.text((16 * s, top + 60 * s), f"σy ≈ {H_MPa / 3:.0f} MPa (screen only)", font=fb, fill=(30, 60, 140))
    d.text((16 * s, top + 96 * s), "Calibrate H / σy on our own tensile bars (#255)", font=f, fill=(150, 40, 30))
    d.text((16 * s, top + 120 * s), "before quoting MPa.", font=f, fill=(150, 40, 30))
    return img


def c3():
    """Vickers hardness on the Mitutoyo HM-220."""
    import r8_specimens as SP
    sc = S.SOPScene("sop04_c3", TITLE)
    S.room(sc, x0=-1500, x1=1500)
    HX, HY = 0.0, 20.0
    hv = S.place(sc, "hv_manual", HX, HY, prefix="hv:")
    P = MP.HV
    ax, ay = P["ax"]
    # the sample: the polished XZ section from SOP 03, in its 38.1 mm conductive hot mount, on the bench at first
    mount = "mount"
    for part, (mesh, rgb, spec) in SP.hot_mount("polished").items():
        sc.add(f"mount/{part}", mesh, rgb, mount, specular=spec)
    M_BENCH = T((-330.0, -250.0, BENCH_H))
    sc.gmat[mount] = M_BENCH
    op = Op(sc, -700.0, -980.0, 0.0)
    au = audit.Audit(sc, allow=[("op/glove", "mount/*"), ("mount/*", "hv:stage_x*"), ("op/glove", "hv:handwheel*"),
                                ("op/glove", "hv:body/p4_black*"), ("hv:indenter*", "mount/*")])
    tz = lambda v: BENCH_H + P["table"] - v                   # noqa: E731 the table's top at stage_z v
    LOAD, FOCUS = 60.0, MP.hv_focus_z(SP.FACE_Z)

    V_ALL = S.look((60, -60, BENCH_H + 300), 2600, az=28, el=18)
    V_SIDE = S.look((HX + ax, HY + ay - 40, BENCH_H + 270), 1350, az=58, el=22)
    V_STAGE = S.look((HX + ax, HY + ay, BENCH_H + 280), 560, az=40, el=24)
    V_CLOSE = S.look((HX + ax, HY + ay, BENCH_H + 280), 300, az=30, el=20)
    V_WHEEL = S.look((HX - 170, HY - 120, BENCH_H + 150), 1300, az=-64, el=22)
    sc.cam = V_ALL
    sc.card("Vickers hardness (ASTM E384)", ["HV0.5 or HV1, 10 s dwell, 10 indents per sample",
                                             "spacing at least 2.5 diagonals; report mean ± SD",
                                             "single tracks: HV0.05 in the fusion zone"], seconds=3.5,
            label="Vickers", note="Mitutoyo HM-220 Type D (AVPAK), as byu-vcl modelled it from Mitutoyo's catalogue")
    sc.step("Vickers", "Micro-Vickers: Mitutoyo HM-220 with AVPAK | 0.05 gf to 2 kgf; motorized turret and XY stage",
            3.2, None, hold=1.4,
            labels=[("motorized turret: indenter, 10x, 50x", hv.world((-75, -120, 367)), (0.14, 0.24)),
                    ("XY table, 130 x 130 mm", hv.world((-65, ay - 65, 252)), (0.14, 0.62)),
                    ("AVPAK PC and monitor", hv.world((270, 120, 500)), (0.82, 0.22)),
                    ("polished XZ section (SOP 03)", (M_BENCH @ np.array([0, 0, 20, 1]))[:3], (0.30, 0.80))])
    # lower the stage on its handwheel (left hand)
    wheel = hv.world((-MP.HV["W"] / 2 - 52, ay + 40, 90 + 46))
    pw = Op.place_for(wheel + np.array([-40, -40, 30]), "l", 20.0, 240)
    sc.step("Load", "Lower the stage on the handwheel", 2.6,
            op.go(x=pw[0], y=min(pw[1], -760.0), hd=20.0, lean=18, l=wheel + np.array([-30, 0, 20]), look=wheel,
                  grip_l=0.7), hold=0.1, cam_to=V_WHEEL)
    sc.step("Load", "Lower the stage on the handwheel | 60 mm: room for the mount and fingers", 2.4,
            S.together(hv.move({"stage_z": (0.0, LOAD), "handwheel": (0.0, 720.0)}),
                       op.go(l=lambda u: hv.world((-MP.HV["W"] / 2 - 52, ay + 40, 90 + 46), "handwheel")
                             + np.array([-30, 0, 20]))), hold=0.2)
    # the mount onto the table (right hand)
    grab = (M_BENCH @ np.array([0, -30, 44, 1]))[:3]
    pg = Op.place_for(grab, "r", 0.0, 250)
    sc.step("Load", "Set the mount on the table, face up", 2.4,
            op.go(x=pg[0], y=min(pg[1], -760.0), hd=0.0, lean=22, l=None, r=grab + np.array([0, -10, 20]), look=grab,
                  grip_r=0.4, grip_l=0.3), hold=0.0, cam_to=V_SIDE)
    sc.step("Load", "Set the mount on the table, face up", 0.6, op.go(r=grab, grip_r=0.9), hold=0.0)
    op.p.hold("r", mount)
    on_table = T((HX + ax, HY + ay, tz(LOAD)))
    path = [(M_BENCH @ np.array([0, 0, 0, 1]))[:3] + np.array([0, 0, 120]),
            on_table[:3, 3] + np.array([0, -140, 60]), on_table[:3, 3] + np.array([0, 0, 8]), on_table[:3, 3]]
    pt = Op.place_for(on_table[:3, 3] + np.array([0, -30, 44]), "r", 0.0, 330)

    def carry(u):
        st = carry.__dict__.setdefault("st", {})
        if not st:
            st["a"] = sc.world(mount)[:3, 3].copy()
            st["off"] = np.array([0, -30, 44])
        p = along([st["a"]] + path, u)
        op.p.let_go("r") if "r" in op.p.held else None
        sc.gmat[mount] = T(p)
        op.hand["r"] = p + st["off"]
        op.apply()
    sc.step("Load", "Set the mount on the table, face up", 2.6,
            S.together(op.go(x=pt[0], y=min(pt[1], -760.0), lean=16), carry), hold=0.0, cam_to=V_STAGE)
    reparent(sc, mount, "hv:stage_x")
    sc.step("Load", "Set the mount on the table, face up", 1.0,
            op.go(r=on_table[:3, 3] + np.array([0, -110, 60]), grip_r=0.3), hold=0.0)
    sc.step("Focus", "Raise the stage; focus with the 10x objective", 2.6,
            S.together(op.go(r=None, x=-650.0, y=-900.0, hd=-30.0, lean=4, look=hv.world((ax, ay, 300))),
                       hv.move({"stage_z": (LOAD, FOCUS), "turret": (0.0, 90.0)})), hold=0.6, cam_to=V_STAGE)
    # the test
    sc.panel("settings", lambda u: settings_image(), rect=(0.70, 0.09, 0.28), alpha=0.0)
    sc.step("Load", "Test force HV0.5 (4.903 N), dwell 10 s", 2.4, sc.fade_panel("settings", 0, 1), hold=1.8)
    sc.step("Indent", "Turret: indenter over the sample", 2.2,
            S.together(hv.move({"turret": (90.0, -90.0)}), sc.fade_panel("settings", 1, 0)), hold=0.2,
            cam_to=V_CLOSE)
    dent = "dent"
    sc.add("dent/indent", S.pv.Box(bounds=(-0.18, 0.18, -0.18, 0.18, -0.02, 0.01)).rotate_z(45, inplace=False),
           (0.12, 0.12, 0.13), dent, specular=0.1)
    sc.gmat[dent] = T((0, 0, SP.FACE_Z))
    sc.parent[dent] = mount
    sc.alpha["dent/indent"] = 0.0
    gauge(sc, "load", "HV0.5")
    sc.step("Indent", "Load on: 10 s dwell | 4.903 N on a 136° diamond pyramid", 1.2,
            hv.move({"indenter": (0.0, P["wd"])}), hold=0.0)

    def dwell(u):
        gauge(sc, "dwell", f"{10 * u:4.1f} s")
    sc.step("Indent", "Load on: 10 s dwell | 4.903 N on a 136° diamond pyramid", 3.0, dwell, hold=0.2)
    sc.step("Indent", "Unload; turret to the 50x objective", 2.0, hv.move({"indenter": (P["wd"], 0.0)}), hold=0.0)
    sc.step("Indent", "Unload; turret to the 50x objective", 1.8, hv.move({"turret": (-90.0, 0.0)}), hold=0.2)
    sc.gauges = [g for g in sc.gauges if g[0] not in ("dwell",)]
    sc.panel("indent", indent_image, rect=(0.66, 0.09, 0.32), alpha=0.0)
    sc.step("Measure", "Measure both diagonals; HV from their mean", 3.6,
            S.together(sc.fade_panel("indent", 0, 1), sc.drive_panel("indent", 0, 1)), hold=2.4)
    # ten indents
    dents = []
    for i in range(1, 10):
        nm = f"dent{i}/indent"
        sc.add(nm, S.pv.Box(bounds=(-0.18, 0.18, -0.18, 0.18, -0.02, 0.01)).rotate_z(45, inplace=False),
               (0.12, 0.12, 0.13), f"dent{i}", specular=0.1)
        sc.gmat[f"dent{i}"] = T((-1.2 * i, 0, SP.FACE_Z))
        sc.parent[f"dent{i}"] = mount
        sc.alpha[nm] = 0.0
        dents.append(nm)
    sc.panel("spacing", spacing_image, rect=(0.62, 0.09, 0.36), alpha=0.0)

    def ten(u):
        k = int(u * 9.999)
        hv.set(stage_x=0.30 * u * 9, turret=-90.0 * math.sin(math.pi * ((u * 9.0) % 1.0)) ** 2)
    sc.step("Spacing", "10 indents, each 2.5 diagonals clear | the stage steps 0.30 mm between them", 6.0,
            S.together(ten, sc.fade_panel("indent", 1, 0), sc.fade_panel("spacing", 0, 1),
                       sc.drive_panel("spacing", 0, 1)), hold=1.6)
    sc.panel("table", hv_table_image, rect=(0.68, 0.09, 0.30), alpha=0.0)
    sc.step("Report", "Report mean ± SD for each sample", 2.6,
            S.together(sc.fade_panel("spacing", 1, 0), sc.fade_panel("table", 0, 1)), hold=2.6, cam_to=V_STAGE)
    sc.panel("tracks", track_image, rect=(0.62, 0.09, 0.36), alpha=0.0)
    sc.step("Tracks", "Single tracks (SOP 02): HV0.05, one per track", 3.0,
            S.together(sc.fade_panel("table", 1, 0), sc.fade_panel("tracks", 0, 1)), hold=3.0)
    sc.panel("line", hv_line_image, rect=(0.60, 0.09, 0.38), alpha=0.0)
    sc.step("Report", "Auto-stage: map a line across the build height", 5.0,
            S.together(sc.fade_panel("tracks", 1, 0), sc.fade_panel("line", 0, 1), sc.drive_panel("line", 0, 1),
                       hv.move({"stage_y": (0.0, 9.0), "stage_x": (2.7, 2.7)})), hold=2.0, cam_to=V_SIDE)
    sc.panel("tabor", tabor_image, rect=(0.60, 0.09, 0.38), alpha=0.0)
    sc.step("Strength", "Tabor σy ≈ H/3 is only a screen | H = 9.807 x HV in MPa; calibrate on #255 bars", 3.2,
            S.together(sc.fade_panel("line", 1, 0), sc.fade_panel("tabor", 0, 1)), hold=3.2)
    sc.step("Time", "About 10 min per sample by hand | unattended with the auto-stage (AVPAK)", 3.0,
            sc.fade_panel("tabor", 1, 0), hold=2.0, cam_to=V_ALL)
    sc.step("Aging", "Then every aged coupon, the same way | 16 conditions per alloy, plus the references", 3.0,
            None, hold=2.0)
    return sc, au, locals()


def settings_image(s=2.0):
    W, H = 300, 200
    img, d, top = card_image(W, H, "AVPAK test settings", s, tag=None)
    f = _font(14 * s, mono=True)
    for i, (k, v) in enumerate((("method", "Vickers"), ("force", "HV0.5 · 4.903 N"), ("dwell", "10 s"),
                                ("indents", "10 per sample"), ("pitch", ">= 2.5 d"))):
        d.text((16 * s, top + 4 * s + i * 26 * s), f"{k:<8}", font=f, fill=(90, 94, 102))
        d.text((120 * s, top + 4 * s + i * 26 * s), v, font=f, fill=(20, 22, 30))
    return img


# ===================================================================================================== chapter 4
def delta_mm(iacs, f_hz):
    """Standard depth of penetration, delta = 1 / sqrt(pi f mu0 sigma) = 503 / sqrt(sigma[MS/m] f[Hz]) mm."""
    sigma = 58.0 * iacs / 100.0                      # MS/m (100 %IACS = 58.0 MS/m at 20 C)
    return 503.0 / math.sqrt(sigma * f_hz)


def depth_image(u, s=2.0):
    W, H = 400, 290
    img, d, top = card_image(W, H, "Frequency vs penetration depth", s, tag="computed")
    f, fb = _font(13 * s, mono=True), _font(13 * s, mono=True)
    d.text((16 * s, top + 2 * s), "f, kHz   δ at 25 %IACS   δ at 60 %IACS", font=_font(12.5 * s, bold=True),
           fill=(40, 44, 52))
    for i, fk in enumerate((60, 120, 240, 480, 960)):
        y = top + 26 * s + i * 25 * s
        a, b = delta_mm(25, fk * 1e3), delta_mm(60, fk * 1e3)
        if fk == 60:
            d.rounded_rectangle((10 * s, y - 3 * s, W * s - 10 * s, y + 21 * s), 4 * s, fill=(226, 238, 228))
        d.text((16 * s, y), f"{fk:5d}     {a:5.2f} mm       {b:5.2f} mm", font=f, fill=(20, 22, 30))
    d.text((16 * s, top + 160 * s), "δ = 1/sqrt(π f μ0 σ); 3 mm coupons: 3δ < 2 mm at 60 kHz", font=_font(12 * s),
           fill=(40, 44, 52))
    d.text((16 * s, top + 180 * s), "(Foerster: thickness >= 3δ; see the meter's table)", font=_font(12 * s),
           fill=(90, 94, 102))
    return img


def meter_screen_image(reading, s=2.0, T_C=20.4, tag=SYN):
    """The SIGMATEST's measuring screen, as in Foerster's photo: frequency and temperature, MS/m, %IACS, lift-off."""
    W, H = 250, 250
    img = Image.new("RGBA", (int(W * s), int(H * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), 8 * s, fill=(28, 32, 36, 245))
    g = (14, 92, 74)
    d.rectangle((10 * s, 10 * s, W * s - 10 * s, 34 * s), fill=g)
    d.text((16 * s, 13 * s), "60 kHz", font=_font(13 * s, bold=True), fill=(255, 255, 255))
    d.text((W * s - 92 * s, 13 * s), f"{T_C:.1f} °C", font=_font(13 * s, bold=True), fill=(255, 255, 255))
    d.rectangle((10 * s, 36 * s, W * s - 10 * s, 118 * s), fill=(250, 250, 250))
    ms = 58.0 * reading / 100.0
    d.text((22 * s, 52 * s), f"{ms:.2f}", font=_font(38 * s, bold=True), fill=(20, 20, 24))
    d.text((W * s - 62 * s, 40 * s), "MS/m", font=_font(11 * s), fill=(60, 60, 66))
    d.rectangle((10 * s, 120 * s, W * s - 10 * s, 186 * s), fill=(250, 250, 250))
    d.text((22 * s, 132 * s), f"{reading:.1f}", font=_font(30 * s, bold=True), fill=(20, 20, 24))
    d.text((W * s - 70 * s, 124 * s), "%IACS", font=_font(11 * s), fill=(60, 60, 66))
    d.rectangle((10 * s, 188 * s, W * s - 10 * s, 212 * s), fill=g)
    d.text((16 * s, 191 * s), "lift-off 12 um · comp. 20 °C on", font=_font(11 * s), fill=(255, 255, 255))
    if tag:
        f = _font(10 * s, bold=True)
        tw = d.textlength(tag, font=f)
        d.rounded_rectangle((W * s - tw - 24 * s, 218 * s, W * s - 10 * s, 238 * s), 4 * s, fill=(255, 244, 214),
                            outline=(190, 140, 40))
        d.text((W * s - tw - 17 * s, 221 * s), tag, font=f, fill=(120, 80, 10))
    return img


def readings_image(u, s=2.0):
    vals = [34.62, 34.55, 34.58, 34.49, 34.60, 34.53]
    W, H = 330, 270
    img, d, top = card_image(W, H, "Coupon 300 °C / 1 h: 3 readings a face", s)
    n = int(round(6 * min(1.0, u * 1.1)))
    f = _font(13.5 * s, mono=True)
    for i in range(n):
        face = "A" if i < 3 else "B"
        d.text((20 * s, top + 4 * s + i * 23 * s), f"face {face}  #{i % 3 + 1}   {vals[i]:.2f} %IACS", font=f,
               fill=(20, 22, 30))
    if n == 6:
        m, r = float(np.mean(vals)), max(vals) - min(vals)
        d.text((20 * s, top + 150 * s), f"mean {m:.2f} %IACS", font=_font(14 * s, bold=True), fill=(30, 60, 140))
        d.text((20 * s, top + 176 * s), f"repeats within {r:.2f} %IACS (accept <= 0.3)", font=_font(12.5 * s),
               fill=(40, 100, 50))
    return img


def tcorr_image(u, s=2.0):
    """conductivity.py iacs 34.6 --T 23.0 --slope 0.0114, computed with the repo's own functions."""
    rho = CON.iacs_to_resistivity(34.6)
    r20 = CON.to_20C(rho, 23.0, 0.0114)
    W, H = 470, 210
    img, d, top = card_image(W, H, "Room at 23.0 °C, not 20 ± 1: correct it", s, tag="computed")
    f = _font(12.5 * s, mono=True)
    d.rounded_rectangle((12 * s, top + 2 * s, W * s - 12 * s, top + 120 * s), 5 * s, fill=(30, 33, 38))
    lines = ["$ python conductivity.py iacs 34.6 --T 23.0 --slope 0.0114",
             "{", f'  "rho_uohm_cm": {rho:.4f},', f'  "rho_20C_uohm_cm": {r20:.4f}', "}"]
    for i, t in enumerate(lines):
        d.text((20 * s, top + 8 * s + i * 21 * s), t, font=f, fill=(210, 230, 210) if i else (240, 240, 240))
    d.text((14 * s, top + 128 * s), f"= {CON.resistivity_to_iacs(r20):.2f} %IACS at 20 °C. Record whether the "
           "meter's", font=_font(12 * s), fill=(40, 44, 52))
    d.text((14 * s, top + 146 * s), "own 20 °C compensation was on: then don't correct twice.",
           font=_font(12 * s), fill=(40, 44, 52))
    return img


class Cable:
    """The probe's cable, redrawn every frame: out of the meter's socket, along the bench, up to the probe."""

    def __init__(self, sc, name, socket, out_dir, probe_group, radius=2.6):
        self.sc, self.name, self.g = sc, name, probe_group
        self.socket, self.out = np.asarray(socket, float), unit(out_dir)
        self.r = radius
        sc.add(name, self.mesh(), (0.10, 0.10, 0.11), "cable", specular=0.2)
        sc.frame_hooks.insert(0, self)

    def points(self):
        Mw = self.sc.world(self.g)
        top = (Mw @ np.array([0, 0, MP.PROBE_LEN, 1.0]))[:3]
        up = Mw[:3, 2]
        s0 = self.socket
        z0 = BENCH_H + self.r + 0.5
        side = np.array([1.0, 0.0, 0.0])
        a = s0 + self.out * 45
        b = np.array([s0[0] + 70, s0[1] + 80, z0])
        c = np.array([s0[0] + 140, s0[1] - 60, z0])
        e = np.array([top[0] + 120, top[1] - 30, z0])
        f = top + up * 70 + side * 30
        pts = [s0, a, b, c, e, f, top]
        return np.array(pts)

    def mesh(self):
        pts = self.points()
        sp = S.pv.Spline(pts, 120)
        p = np.asarray(sp.points)
        p[:, 2] = np.maximum(p[:, 2], BENCH_H + self.r + 0.3)
        sp.points = p
        return sp.tube(radius=self.r, n_sides=10)

    def __call__(self, sc):
        sc.set_mesh(self.name, self.mesh())


def c4():
    """Eddy-current conductivity with the SIGMATEST 2.070."""
    sc = S.SOPScene("sop04_c4", TITLE)
    S.room(sc, x0=-1500, x1=1500)
    MX, MY = 200.0, -130.0
    meter = S.place(sc, "eddy_meter", MX, MY, prefix="eddy:")
    E = MP.EDDY
    # the mat the coupons and standards lie on (a non-conductive cutting mat), the coupons, a 5 mm cube
    sc.add("mat", S.pv.Box(bounds=(-420, 60, -365, -205, BENCH_H, BENCH_H + 2)), (0.20, 0.34, 0.30), "mat",
           specular=0.05)
    zt = BENCH_H + 2.0
    STD = T((-300.0, -290.0, zt))
    reparent(sc, "eddy:standards", None)
    sc.gmat["eddy:standards"] = STD
    coupons = []
    for i in range(4):
        g = f"cp{i}"
        add_model(sc, g, MP.coupon(), T((-130.0 + 32 * i, -300.0, zt)))
        coupons.append(g)
    add_model(sc, "cube5", Model5(), T((30.0, -300.0, zt)))
    sc.add("thermo", S.pv.Box(bounds=(-1, 1, -1, 1, -1, 1)), (1, 1, 1), "thermo", opacity=0.0)
    add_model(sc, "thermometer", MP.thermometer(), T((-640.0, 120.0, BENCH_H)) @ R((0, 0, 1), 20))
    op = Op(sc, -700.0, -1050.0, 0.0)
    probe = "eddy:probe"
    reparent(sc, probe, None)
    P_REST = T((MX - 215.0, MY - 70.0, BENCH_H + 9.5)) @ R((0, 1, 0), 90)     # lying on the bench, tip to +x
    sc.gmat[probe] = P_REST
    sock = meter.world(MP.eddy_lemo())
    cable = Cable(sc, "cable/probe", sock, (0, 1, 0), probe)
    au = audit.Audit(sc, allow=[("op/glove", "eddy:probe*"), ("eddy:probe*", "cp*"), ("eddy:probe*", "eddy:standards*"),
                                ("cable*", "*"), ("op/glove", "cp*"), ("cp*", "mat")])

    V_ALL = S.look((-120, -160, BENCH_H + 200), 2300, az=34, el=22)
    V_SIDE = S.look((-120, -260, BENCH_H + 80), 1100, az=62, el=30)
    V_CLOSE = S.look((-100, -300, BENCH_H + 20), 360, az=58, el=26)
    V_STD = S.look((-300, -290, BENCH_H + 20), 420, az=56, el=30)
    V_THERMO = S.look((-640, 120, BENCH_H + 60), 700, az=-15, el=12)
    sc.cam = V_ALL
    sc.card("Eddy-current conductivity (%IACS)", ["the meter's standards bracket 25-60 %IACS",
                                                  "20 ± 1 °C, or record T and correct it",
                                                  "δ well under the thickness; 3 readings per face"], seconds=3.5,
            label="Conductivity", note="Foerster SIGMATEST 2.070 (211 x 102 x 40 mm, 0.62 kg), registered to "
                                       "Foerster's photo and video")
    sc.step("Conductivity", "Eddy-current meter, probe, standards, coupons | Foerster SIGMATEST 2.070: "
            "60-960 kHz, 1-112 %IACS", 3.2, None, hold=1.6,
            labels=[("Foerster SIGMATEST 2.070", meter.world((0, 60, 42)), (0.80, 0.18)),
                    ("pencil probe, 8 mm head", (sc.world(probe) @ np.array([0, 0, 60, 1]))[:3], (0.80, 0.52)),
                    ("standards ≈ 26 and ≈ 59 %IACS", (STD @ np.array([0, 0, 10, 1]))[:3], (0.16, 0.64)),
                    ("aged coupons, 10 x 10 x 3 mm", (-80, -300, zt + 3), (0.36, 0.84))])
    # ------------------------------------------------------------------ samples: the 5 mm cube
    sc.step("Samples", "Flat coupons: at least 10 x 10 mm, 2 mm thick", 2.6, None, hold=1.2,
            cam_to=S.look((0, -300, BENCH_H + 10), 380, az=20, el=36),
            labels=[("coupon 10 x 10 x 3 mm", (-34, -300, zt + 3), (0.22, 0.30)),
                    ("5 mm cube (SOP 03)", (30, -300, zt + 5), (0.76, 0.30))])
    # a ghost of the 8 mm head's field over each: the coupon holds it, the cube does not
    for nm, x, wsz in (("foot_c", -34.0, 10.0), ("foot_k", 30.0, 5.0)):
        ring = S.pv.Disc(center=(0, 0, 0), inner=4.0, outer=4.6, c_res=48)
        sc.add(f"{nm}/ring", ring, (0.85, 0.30, 0.20), nm, specular=0.0)
        sc.gmat[nm] = T((x, -300, zt + (3.05 if wsz == 10 else 5.05)))
        sc.alpha[f"{nm}/ring"] = 0.0
    sc.step("Samples", "A 5 mm cube is too small for most probes | use a 5 mm head, or a four-point probe on "
            "the polished face", 3.0, fade(sc, ["foot_c/ring", "foot_k/ring"], 0, 1), hold=2.4,
            labels=[("8 mm head: fits the 10 mm coupon", (-34, -296, zt + 3), (0.22, 0.30)),
                    ("overhangs the 5 mm cube: edge error", (30, -296, zt + 5), (0.74, 0.30))])
    sc.step("Samples", "A 5 mm cube is too small for most probes | use a 5 mm head, or a four-point probe on "
            "the polished face", 0.8, fade(sc, ["foot_c/ring", "foot_k/ring"], 1, 0), hold=0.0)
    # ------------------------------------------------------------------ temperature
    gauge(sc, "room", "20.4 °C")
    gauge(sc, "comp.", "20 °C on")
    sc.step("Temperature", "Measure at 20 ± 1 °C | coupons and standards rest on the bench first", 3.0, None,
            hold=1.6, cam_to=V_THERMO,
            labels=[("room thermometer: 20.4 °C", (-640, 110, BENCH_H + 90), (0.70, 0.26))])
    sc.step("Temperature", "Record whether the meter's compensation is on | it normalises to 20 °C from the "
            "probe's own sensor", 3.0, None, hold=1.4, cam_to=V_ALL)

    # ------------------------------------------------------------------ the probe in the hand
    def probe_pose(p, lift=0.0):
        return T((p[0], p[1], p[2] + lift))

    def hand_for_probe(M):
        return (M @ np.array([-18.0, -24.0, 72.0, 1.0]))[:3]

    def probe_to(path_pts, lift_end=0.0, grip_side=True):
        st = {}

        def up(u):
            if not st:
                st["a"] = sc.world(probe)[:3, 3].copy()
                st["R0"] = sc.world(probe).copy()
            p = along([st["a"]] + [np.asarray(q, float) for q in path_pts], u)
            M = S.blend(st["R0"], T(p), min(1.0, u * 2.5))
            M[:3, 3] = p
            sc.gmat[probe] = M
            op.hand["r"] = hand_for_probe(M)
            op.grip["r"] = 0.75
            op.apply()
        return up
    # pick it up
    pr0 = (P_REST @ np.array([0, 0, 0, 1]))[:3]
    grip0 = (P_REST @ np.array([0, 0, 55, 1]))[:3] + np.array([0, -20, 30])
    pp = Op.place_for(grip0, "r", 0.0, 230)
    sc.step("Calibration", "Probe in hand, held square to the surface", 2.6,
            op.go(x=pp[0], y=min(pp[1], -680.0), lean=18, r=grip0, look=grip0, grip_r=0.5), hold=0.0,
            cam_to=V_SIDE)
    std_lo = (STD @ np.array([-23.0, 0, 10.0, 1]))[:3]
    std_hi = (STD @ np.array([23.0, 0, 10.0, 1]))[:3]
    ps = Op.place_for(hand_for_probe(T(std_lo)), "r", 0.0, 230)
    sc.step("Calibration", "Probe in hand, held square to the surface", 2.6,
            S.together(op.go(x=ps[0], y=min(ps[1], -680.0), lean=20),
                       probe_to([pr0 + np.array([0, 0, 60]), std_lo + np.array([0, 0, 40])])), hold=0.0,
            cam_to=V_STD)
    sc.panel("screen", lambda u: meter_screen_image(25.9 if u < 0.5 else 58.6), rect=(0.74, 0.09, 0.22), alpha=0.0)
    sc.step("Calibration", "Standards at the start of each session | low ≈ 26 %IACS (brass)", 2.0,
            S.together(probe_to([std_lo]), sc.fade_panel("screen", 0, 1)), hold=1.8)
    sc.step("Calibration", "Standards at the start of each session | high ≈ 59 %IACS (Al 99.5)", 2.4,
            S.together(probe_to([std_lo + np.array([0, 0, 30]), std_hi + np.array([0, 0, 30]), std_hi]),
                       call_at(0.5, lambda: sc.panels["screen"].update(u=1.0))), hold=1.8)
    sc.panel("depth", depth_image, rect=(0.62, 0.09, 0.36), alpha=0.0)
    sc.step("Frequency", "Pick 60 kHz: δ well under the 3 mm coupon", 3.0,
            S.together(sc.fade_panel("screen", 1, 0), sc.fade_panel("depth", 0, 1),
                       probe_to([std_hi + np.array([0, 0, 40])])), hold=3.0)
    # three readings on face A, then on face B
    cpos = (sc.world("cp1") @ np.array([0, 0, MP.COUPON[2], 1]))[:3]
    sc.panel("reads", readings_image, rect=(0.70, 0.09, 0.28), alpha=0.0)
    pc = Op.place_for(hand_for_probe(T(cpos)), "r", 0.0, 230)
    sc.step("Measure", "Three readings on each face", 2.4,
            S.together(sc.fade_panel("depth", 1, 0), op.go(x=pc[0], y=min(pc[1], -680.0)),
                       probe_to([cpos + np.array([0, 0, 40])])), hold=0.0, cam_to=V_CLOSE)
    body = [n for n in op.p.names() if not n.endswith("/glove")]

    def press(k, u0, u1):
        return lambda u: None
    seq = []
    for k in range(3):
        seq.append(probe_to([cpos]))
        seq.append(probe_to([cpos + np.array([0, 0, 25])]))
    sc.step("Measure", "Three readings on each face | face A", 0.8,
            S.together(sc.fade_panel("reads", 0, 1), fade(sc, body, 1.0, 0.25), seq[0]), hold=0.5)
    sc.panels["reads"]["u"] = 1 / 6 - 1e-3
    for k in range(1, 3):
        sc.step("Measure", "Three readings on each face | face A", 0.6, seq[2 * k - 1], hold=0.0)
        sc.step("Measure", "Three readings on each face | face A", 0.6,
                S.together(seq[2 * k], sc.drive_panel("reads", k / 6, (k + 1) / 6 - 1e-3)), hold=0.4)
    # turn the coupon over (left hand), the probe lifted
    sc.step("Measure", "Turn the coupon over", 1.0, probe_to([cpos + np.array([0, 0, 60])]), hold=0.0)
    cp = "cp1"
    grabp = cpos + np.array([-14, -6, 14])
    pl = Op.place_for(grabp, "l", 0.0, 220)
    sc.step("Measure", "Turn the coupon over", 1.6, op.go(x=pl[0], y=min(pl[1], -680.0), l=grabp, grip_l=0.8),
            hold=0.0)
    C0 = sc.world(cp).copy()
    C1 = T(C0[:3, 3] + np.array([0, 0, MP.COUPON[2]])) @ R((1, 0, 0), 180)

    def flip(u):
        up_ = np.array([0, 0, 30.0 * math.sin(math.pi * u)])
        M = S.blend(C0, C1, u)
        M[:3, 3] += up_
        sc.gmat[cp] = M
        op.hand["l"] = grabp + up_
        op.apply()
    sc.step("Measure", "Turn the coupon over", 1.6, flip, hold=0.0)
    sc.step("Measure", "Three readings on each face | face B", 1.0, op.go(l=None, grip_l=0.3), hold=0.0)
    for k in range(3):
        sc.step("Measure", "Three readings on each face | face B", 0.6,
                probe_to([cpos + np.array([0, 0, 25])]) if k else probe_to([cpos + np.array([0, 0, 25])]), hold=0.0)
        sc.step("Measure", "Three readings on each face | face B", 0.6,
                S.together(probe_to([cpos]), sc.drive_panel("reads", (3 + k) / 6, (4 + k) / 6 - (1e-3 if k < 2 else 0))),
                hold=0.4)
    sc.step("Acceptance", "Repeats within 0.3 %IACS: accept", 2.0, probe_to([cpos + np.array([0, 0, 50])]), hold=2.0)
    sc.panel("tcorr", tcorr_image, rect=(0.55, 0.09, 0.43), alpha=0.0)
    sc.step("Temperature", "Off 20 ± 1 °C? Record T and correct", 3.0,
            S.together(sc.fade_panel("reads", 1, 0), sc.fade_panel("tcorr", 0, 1), fade(sc, body, 0.25, 1.0)),
            hold=3.4, cam_to=V_SIDE)
    sc.step("Time", "About 2 min per sample | the same for all 16 conditions and the references", 3.0,
            sc.fade_panel("tcorr", 1, 0), hold=2.0, cam_to=V_ALL)
    sc.step("Open question", "An eddy-current meter on campus (NDE, aerospace)? | if not, a used handheld unit is the "
            "cheapest high-throughput buy", 3.6, None, hold=2.4)
    return sc, au, locals()


def Model5():
    """A 5 mm printed cube (SOP 03)."""
    from common import Model
    m = Model("p4_cube5", "5 mm cube")
    m.add("cube", box(-2.5, -2.5, 0, 2.5, 2.5, 5.0), "p4_asbuilt")
    return m


# ===================================================================================================== chapter 5
L_DISC = 2.5e-3                    # m


def parker(t, alpha, L=L_DISC, n=30):
    """Rear-face rise of an adiabatic slab after a flash (Parker 1961), normalised 0-1."""
    t = np.asarray(t, float)
    out = np.ones_like(t)
    for k in range(1, n):
        out += 2 * (-1) ** k * np.exp(-k * k * math.pi ** 2 * alpha * t / L ** 2)
    return np.clip(out, 0, None)


ALPHA = 58.0e-6                    # m2/s, a synthetic Al-alloy disc


def thermogram_image(u, s=2.0):
    def draw(ax):
        t = np.linspace(0, 0.10, 400)
        y = parker(t, ALPHA)
        rng = np.random.default_rng(3)
        n = max(2, int(len(t) * min(1.0, u * 1.1)))
        ax.plot(t[:n] * 1000, (y + rng.normal(0, 0.012, t.size))[:n], color="#1f4e8c", lw=1.2)
        t_half = 0.1388 * L_DISC ** 2 / ALPHA
        if u > 0.7:
            ax.axvline(t_half * 1000, color="#b0302a", lw=1, ls="--")
            ax.text(t_half * 1000 + 2, 0.15, f"t½ = {t_half * 1000:.1f} ms", color="#b0302a", fontsize=8)
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.1, 1.15)
        ax.set_xlabel("time after the flash, ms")
        ax.set_ylabel("rear-face rise, norm.")
    return fig_panel(draw, 5.0, 3.0, title="IR detector: the rear face warms")


def k_image(u, s=2.0):
    t_half = 0.1388 * L_DISC ** 2 / ALPHA
    alpha = 0.1388 * L_DISC ** 2 / t_half
    rho, cp = 2670.0, 900.0
    k = alpha * rho * cp
    W, H = 430, 230
    img, d, top = card_image(W, H, "k = α · ρ · cp", s)
    f = _font(13.5 * s, mono=True)
    rows = [f"α  = 0.1388 L²/t½ = {alpha * 1e6:.1f} mm²/s", f"ρ  = {rho:.0f} kg/m³   (Archimedes, SOP 03)",
            f"cp = {cp:.0f} J/(kg K)  (DSC, SOP 01)", f"k  = {k:.0f} W/(m K)"]
    for i, r in enumerate(rows):
        d.text((18 * s, top + 6 * s + i * 28 * s), r, font=f if i < 3 else _font(14.5 * s, bold=True, mono=True),
               fill=(20, 22, 30) if i < 3 else (30, 60, 140))
    return img


SP_ALLOYS = [("AlSi10Mg as-built", 31.0), ("candidate, 400 °C 16 h", 38.0), ("AlSi10Mg aged", 41.5),
             ("6063-T6", 53.0)]


def smith_palmer_data():
    rng = np.random.default_rng(5)
    rho = np.array([CON.iacs_to_resistivity(v) for _, v in SP_ALLOYS])
    k = np.array([CON.wiedemann_franz_k(r, A=0.92, B=9.0) for r in rho]) + rng.normal(0, 1.5, rho.size)
    A, B = CON.fit_smith_palmer(rho, k)
    return rho, k, A, B


def smith_palmer_image(u, s=2.0):
    rho, k, A, B = smith_palmer_data()

    def draw(ax):
        x = CON.L0 * 293.15 / (rho * 1e-8)
        ax.plot(x, k, "o", color="#1f4e8c", ms=6, label="laser flash, 4 alloys")
        if u > 0.4:
            xx = np.linspace(x.min() * 0.9, x.max() * 1.05, 50)
            ax.plot(xx, A * xx + B, "-", color="#b0302a", lw=1.4, label=f"fit: A = {A:.2f}, B = {B:.1f} W/(m K)")
        ax.set_xlabel("L0 T / ρ, W/(m K)")
        ax.set_ylabel("k, W/(m K)")
        ax.legend(fontsize=7, frameon=False, loc="upper left")
    return fig_panel(draw, 5.0, 3.0, title="Smith-Palmer: k = A L0 T / ρ + B (fit_smith_palmer)")


def k_from_iacs_image(u, s=2.0):
    rho, k, A, B = smith_palmer_data()
    W, H = 400, 250
    img, d, top = card_image(W, H, "Then k from %IACS, for the rest", s)
    f = _font(13 * s, mono=True)
    d.text((18 * s, top + 2 * s), "coupon            %IACS   k, W/(m K)", font=_font(12.5 * s, bold=True),
           fill=(40, 44, 52))
    for i, (name, v) in enumerate((("300 °C 0.25 h", 33.1), ("300 °C 4 h", 36.8), ("350 °C 16 h", 40.2),
                                   ("400 °C 64 h", 44.9), ("as-built", 30.4))):
        kk = CON.wiedemann_franz_k(CON.iacs_to_resistivity(v), A=A, B=B)
        d.text((18 * s, top + 26 * s + i * 24 * s), f"{name:<16} {v:5.1f}   {kk:6.0f}", font=f, fill=(20, 22, 30))
    return img


def c5():
    """Thermal conductivity by laser flash, at the contract lab."""
    sc = S.SOPScene("sop04_c5", TITLE)
    S.room(sc, x0=-1500, x1=1500)
    LX, LY = 120.0, 0.0
    lfa = S.place(sc, "laser_flash", LX, LY, prefix="lfa:")
    L = MP.LFA
    (wx, wy), run = MP.lfa_measure_xy()
    H = L["base_h"]
    zc = H - 58.0
    # our lab's part: discs, graphite spray, on a sheet far to the left (off the contract lab's shots)
    sc.add("sheet", S.pv.Box(bounds=(-1360, -1080, -300, -120, BENCH_H, BENCH_H + 0.5)), (0.97, 0.97, 0.95), "sheet",
           specular=0.0)
    discs, coated, shipped = [], [], []
    dish_c = lfa.world((wx + 150.0, wy - 10.0, H + 2.0))
    sc.add("dish/card", S.pv.Box(bounds=(-36, 36, -30, 30, 0, 0.6)), (0.97, 0.97, 0.95), "dish", specular=0.0)
    sc.gmat["dish"] = T(dish_c)
    for i in range(4):
        at = T((-1300.0 + 50 * i, -210.0, BENCH_H + 0.5))
        add_model(sc, f"disc{i}", MP.lfa_disc(False), at)
        add_model(sc, f"discg{i}", MP.lfa_disc(True), at)
        for n in sc.members(f"discg{i}"):
            sc.alpha[n] = 0.0
        add_model(sc, f"ship{i}", MP.lfa_disc(True), T(dish_c + np.array([(i % 2 - 0.5) * 26, (i // 2 - 0.5) * 26,
                                                                            0.6])))
        discs.append(f"disc{i}")
        coated.append(f"discg{i}")
        shipped.append(f"ship{i}")
    add_model(sc, "spray", MP.spray_can(), T((-1000.0, -140.0, BENCH_H)))
    op = Op(sc, -700.0, -1150.0, 0.0)
    for n in op.p.names():
        if n.endswith("/glove"):
            sc.color[n] = (0.20, 0.20, 0.22)            # the contract lab's black nitrile
    tw = add_model(sc, "tweezers", MP.tweezers(), T(dish_c + np.array([60.0, -30.0, 0.6])))
    au = audit.Audit(sc, allow=[("op/glove", "lfa:lid*"), ("tweezers*", "ship*"), ("ship*", "lfa:changer*"),
                                ("ship*", "dish*"), ("dish*", "lfa:body*"), ("tweezers*", "dish*"),
                                ("tweezers*", "lfa:changer*"), ("disc*", "sheet"),
                                ("lfa:internals*", "lfa:body*"), ("lfa:internals*", "lfa:changer*"),
                                ("lfa:internals*", "ship*"), ("beam/*", "lfa:*"), ("beam/*", "ship*")])
    well = lfa.world((wx, wy, H))
    V_ALL = S.look((LX - 150, LY - 100, BENCH_H + 300), 2400, az=24, el=20)
    V_LFA = S.look((LX, LY - 80, BENCH_H + 280), 1500, az=32, el=24)
    V_WELL = S.look(tuple((well + dish_c) / 2 + np.array([0, 0, -40])), 430, az=22, el=50)
    V_CUT = S.look((LX + L["tower_x"], LY + 30, BENCH_H + 250), 1150, az=58, el=12)
    V_DISCS = S.look((-1220, -210, BENCH_H + 10), 520, az=-10, el=48)
    sc.cam = V_DISCS
    sc.card("Thermal conductivity by laser flash (ASTM E1461)",
            ["sent out: NETZSCH contract testing, 3-4 alloys spanning the range",
             "k = α · ρ · cp; then Smith-Palmer for the rest from %IACS"], seconds=3.5, label="Laser flash",
            note="NETZSCH LFA 717 HyperFlash: no published dimensions; width estimated, proportions fitted to "
                 "NETZSCH's video")
    sc.step("Laser flash", "Discs: 12.7 mm across, 2.5 mm thick | 3-4 alloys spanning 30-55 %IACS", 3.2, None,
            hold=1.6, labels=[("12.7 x 2.5 mm discs, 4 alloys", (-1225, -210, BENCH_H + 3), (0.30, 0.30)),
                              ("graphite spray", (-1000, -140, BENCH_H + 150), (0.78, 0.30))])
    sc.step("Laser flash", "Graphite on both faces, thin | black and even, about 5 μm", 3.0,
            S.together(fade(sc, [n for g in coated for n in sc.members(g)], 0, 1),
                       fade(sc, [n for g in discs for n in sc.members(g)], 1, 0)), hold=1.6)
    sc.cam = V_ALL
    sc.card("Sent to the contract lab", ["NETZSCH contract testing (Burlington, MA): ISO/IEC 17025 scope covers",
                                         "flash diffusivity of metals (ASTM E1461); standard size 12.7 mm"],
            seconds=3.0, label="Laser flash")
    sc.step("Laser flash", "NETZSCH LFA 717 HyperFlash | xenon flash, LN2-cooled IR detector, 16 samples",
            3.0, None, hold=1.6, cam_to=V_LFA,
            labels=[("IR detector in its LN2 tower", lfa.world((L["tower_x"], L["tower_y"], H + 200)), (0.80, 0.16)),
                    ("loading lid over the sample changer", lfa.world((wx, wy - 60, H + 12)), (0.16, 0.30)),
                    ("our four discs", dish_c + np.array([0, 0, 4]), (0.84, 0.46)),
                    ("touch display", lfa.world((0, -L["D"] / 2 - 12, H - 40)), (0.80, 0.70))])
    # the technician opens the lid (right hand on its knob)
    knob = lambda u=None: lfa.world((wx, wy - L["open_d"] / 2 + 12, H + 20), "lid")   # noqa: E731
    pk = Op.place_for(knob() + np.array([0, -40, 30]), "r", 0.0, 380)
    over = lfa.world((wx, -L["D"] / 2 - 40, H + 70))
    sc.step("Load", "Open the lid over the sample changer", 2.6,
            op.go(x=pk[0], y=min(pk[1], -760.0), lean=4, r=over, look=knob(), grip_r=0.4), hold=0.0)
    sc.step("Load", "Open the lid over the sample changer", 1.0, op.go(r=knob() + np.array([0, -30, 30]), grip_r=0.6),
            hold=0.0)

    def lid_up(u):
        lfa.set(lid=u)
        op.hand["r"] = knob() + np.array([0, -30, 30])
        op.apply()
    sc.step("Load", "Open the lid over the sample changer", 1.8, lid_up, hold=0.0)
    sc.step("Load", "Open the lid over the sample changer", 1.2, op.go(r=over + np.array([0, -80, 0]), grip_r=0.3),
            hold=0.0)
    sc.step("Load", "Open the lid over the sample changer", 0.8, op.go(r=None), hold=0.2)
    # the discs into holder 1 with tweezers (a close-up of the tweezers alone)
    holder = [(-33.0 - 11.0, -24.0 - 11.0), (-33.0 + 11.0, -24.0 - 11.0), (-33.0 - 11.0, -24.0 + 11.0),
              (-33.0 + 11.0, -24.0 + 11.0)]
    sc.step("Load", "Four discs into holder 1, with tweezers", 2.0, None, hold=0.2, cam_to=V_WELL)
    for i, g in enumerate(shipped):
        dst = lfa.world((wx + holder[i][0], wy + holder[i][1], zc + 3.0), "changer")
        src = sc.world(g)[:3, 3].copy()

        def carry(u, g=g, dst=dst, src=src):
            path = [src, src + np.array([0, 0, 40]), dst + np.array([0, 0, 75]), dst]
            p = along(path, u)
            sc.gmat[g] = T(p)
            sc.gmat[tw] = T(p + np.array([6.35, 0, 1.25])) @ R((0, 0, 1), 15) @ R((0, 1, 0), -50)
        sc.step("Load", "Four discs into holder 1, with tweezers", 2.2 if i < 2 else 1.4, carry, hold=0.2)
        reparent(sc, g, "lfa:changer")
    park = T(dish_c + np.array([60.0, -30.0, 0.6]))
    st_tw = {}

    def tw_home(u):
        if not st_tw:
            st_tw["a"] = sc.world(tw).copy()
            st_tw["up"] = st_tw["a"].copy()
            st_tw["up"][2, 3] += 90.0
            st_tw["over"] = park.copy()
            st_tw["over"][2, 3] += 90.0
        if u < 0.35:
            sc.gmat[tw] = S.blend(st_tw["a"], st_tw["up"], u / 0.35)
        elif u < 0.75:
            sc.gmat[tw] = S.blend(st_tw["up"], st_tw["over"], (u - 0.35) / 0.4)
        else:
            sc.gmat[tw] = S.blend(st_tw["over"], park, (u - 0.75) / 0.25)
    sc.step("Load", "Four discs into holder 1, with tweezers", 1.0, tw_home, hold=0.2)
    sc.step("Load", "Close the lid; the changer runs back under the detector", 1.4,
            op.go(x=pk[0], r=over, grip_r=0.4), hold=0.0, cam_to=V_LFA)
    sc.step("Load", "Close the lid; the changer runs back under the detector", 0.8,
            op.go(r=knob() + np.array([0, -30, 30]), grip_r=0.6), hold=0.0)

    def lid_down(u):
        lfa.set(lid=1 - u)
        op.hand["r"] = knob() + np.array([0, -30, 30])
        op.apply()
    sc.step("Load", "Close the lid; the changer runs back under the detector", 1.6, lid_down, hold=0.0)
    sc.step("Load", "Close the lid; the changer runs back under the detector", 2.4,
            S.together(op.go(r=over + np.array([0, -120, 0]), grip_r=0.3), lfa.move({"changer": (0.0, run)})),
            hold=0.4)
    # the cutaway: flash below, sample in the middle, detector above
    sc.step("Load", "Close the lid; the changer runs back under the detector", 1.8,
            op.go(r=None, x=pk[0] - 400, y=-1150, grip_r=0.3), hold=0.0)
    sc.step("Flash", "Cutaway: flash below, sample, IR detector above", 3.0,
            lfa.move({"~body": (0.0, 1.0), "~lid": (0.0, 1.0), "internals": (0.0, 1.0)}), hold=1.2, cam_to=V_CUT,
            labels=[("IR detector, LN2-cooled", lfa.world((wx, L["tower_y"], H + 55)), (0.80, 0.16)),
                    ("disc in its holder", lfa.world((wx, L["tower_y"], zc + 6)), (0.82, 0.50)),
                    ("xenon flash lamp", lfa.world((wx, L["tower_y"], L["plinth_h"] + 100)), (0.80, 0.80))])
    beam = "beam"
    bz0, bz1 = L["plinth_h"] + 110, zc - 2
    sc.add("beam/light", S.pv.Cylinder(center=(0, 0, (bz0 + bz1) / 2), direction=(0, 0, 1), radius=7.0,
                                       height=bz1 - bz0, resolution=24), (1.0, 0.96, 0.86), beam, opacity=0.45,
           specular=0.0, ambient=0.8)
    sc.gmat[beam] = lfa.world((wx, L["tower_y"], 0)) @ np.eye(4) if False else T(lfa.world((wx, L["tower_y"], 0)))
    sc.alpha["beam/light"] = 0.0
    sc.panel("thermo", thermogram_image, rect=(0.60, 0.09, 0.38), alpha=0.0)
    sc.step("Flash", "A 1 ms xenon flash heats the front face", 1.0,
            S.together(fade(sc, ["beam/light"], 0, 1), sc.fade_panel("thermo", 0, 1)), hold=0.0)
    sc.step("Flash", "The detector follows the rear face | half-rise time t½ gives α", 3.6,
            S.together(fade(sc, ["beam/light"], 1, 0), sc.drive_panel("thermo", 0, 1)), hold=2.4)
    sc.panel("k", k_image, rect=(0.58, 0.09, 0.40), alpha=0.0)
    sc.step("Thermal conductivity", "k = α · ρ · cp for each alloy", 3.0,
            S.together(sc.fade_panel("thermo", 1, 0), sc.fade_panel("k", 0, 1)), hold=3.0)
    sc.panel("sp", smith_palmer_image, rect=(0.58, 0.09, 0.40), alpha=0.0)
    sc.step("Thermal conductivity", "Fit Smith-Palmer A and B on these alloys", 3.4,
            S.together(sc.fade_panel("k", 1, 0), sc.fade_panel("sp", 0, 1), sc.drive_panel("sp", 0, 1)), hold=3.0,
            cam_to=V_LFA)
    sc.panel("kiacs", k_from_iacs_image, rect=(0.62, 0.09, 0.36), alpha=0.0)
    sc.step("Thermal conductivity", "Then k from %IACS for everything else | an input to the AM Module", 3.0,
            S.together(sc.fade_panel("sp", 1, 0), sc.fade_panel("kiacs", 0, 1),
                       lfa.move({"~body": (1.0, 0.0), "~lid": (1.0, 0.0), "internals": (1.0, 0.0)})), hold=3.0)
    sc.step("Time", "Laser flash: a few alloys, sent out once | eddy current: 2 min a sample, in house", 3.0,
            sc.fade_panel("kiacs", 1, 0), hold=2.0, cam_to=V_ALL)
    return sc, au, locals()


# ===================================================================================================== chapter 6
COLS = {300: "#1f4e8c", 350: "#c07a12", 400: "#b0302a"}


def aging_curves_image(u, s=2.0):
    data, truth = synthetic_aging()

    def draw(ax):
        ax2 = ax.twinx()
        for Tc, d in data.items():
            ax.plot(d["t"], d["hv"], "o-", color=COLS[Tc], ms=4, lw=1.3, label=f"{Tc} °C")
            i = int(np.argmax(d["hv"]))
            ax.plot(d["t"][i], d["hv"][i], "*", color=COLS[Tc], ms=11)
            ax2.plot(d["t"], d["rho"], "s--", color=COLS[Tc], ms=3, lw=0.8, alpha=0.6)
        ax.set_xscale("log")
        ax.set_xlabel("aging time, h")
        ax.set_ylabel("HV0.5 (solid)")
        ax2.set_ylabel("ρ, μΩ cm (dashed)")
        ax.legend(fontsize=7, frameon=False, loc="lower left")
        for sp in ("top",):
            ax2.spines[sp].set_visible(False)
    return fig_panel(draw, 5.2, 3.1, title="Aging curves: HV(t) and ρ(t) at each temperature")


def arrhenius_image(u, s=2.0):
    data, truth = synthetic_aging()
    T = np.array(TEMPS, float) + 273.15
    tpk = []
    for Tc in TEMPS:
        d = data[Tc]
        i = int(np.argmax(d["hv"]))
        # refine the peak with a parabola in log t through the three points round the maximum
        j = min(max(i, 1), len(d["t"]) - 2)
        x = np.log(d["t"][j - 1:j + 2])
        a, b, _ = np.polyfit(x, d["hv"][j - 1:j + 2], 2)
        tpk.append(float(np.exp(-b / (2 * a))) if a < 0 else float(d["t"][i]))
    tpk = np.array(tpk)
    res = KIN.arrhenius(T, 1.0 / (tpk * 3600))

    def draw(ax):
        ax.plot(1000 / T, np.log(1 / (tpk * 3600)), "o", color="#1f4e8c", ms=6)
        xx = np.linspace(1000 / T.max() * 0.98, 1000 / T.min() * 1.02, 20)
        ax.plot(xx, res["lnA"] - res["Q_kJ_mol"] * 1000 / KIN.R * xx / 1000, "-", color="#b0302a", lw=1.3)
        ax.set_xlabel("1000 / T, 1/K")
        ax.set_ylabel("ln (1 / t_peak), 1/s")
        ax.text(0.04, 0.10, f"Q = {res['Q_kJ_mol']:.0f} kJ/mol (arrhenius)\ninput 120", transform=ax.transAxes,
                fontsize=8, color="#b0302a")
    return fig_panel(draw, 5.0, 3.0, title="Time to peak hardness → Arrhenius Q")


def jmak_image(u, s=2.0):
    data, truth = synthetic_aging()
    fits = {}

    def draw(ax):
        tt = np.geomspace(0.1, 100, 80)
        for Tc, d in data.items():
            f = CON.aging_fraction(d["rho"], rho_0=truth["rho0"], rho_inf=truth["rinf"])
            fit = KIN.fit_jmak(d["t"] * 3600, f)
            fits[Tc] = fit
            ax.plot(d["t"], f, "o", color=COLS[Tc], ms=4)
            ax.plot(tt, KIN.jmak(tt * 3600, fit["k_per_s"], fit["n"]), "-", color=COLS[Tc], lw=1.2,
                    label=f"{Tc} °C: n = {fit['n']:.2f}")
        ax.set_xscale("log")
        ax.set_xlabel("aging time, h")
        ax.set_ylabel("f = (ρ0 − ρ) / (ρ0 − ρ∞)")
        ax.legend(fontsize=7, frameon=False, loc="upper left")
    return fig_panel(draw, 5.0, 3.0, title="Fraction transformed from ρ, fitted with JMAK (fit_jmak)")


def prisma_image(u, s=2.0):
    data, truth = synthetic_aging()

    def draw(ax):
        t = np.geomspace(0.05, 200, 200)
        for Tc in TEMPS:
            tp = truth["tpk"][TEMPS.index(Tc)]
            x = np.log(t / tp)
            ys = 300 + (120 - 14 * TEMPS.index(Tc)) * np.exp(-0.5 * (x / 1.4) ** 2)
            ax.plot(t, ys, "-", color=COLS[Tc], lw=1.1, label=f"predicted, {Tc} °C")
            d = data[Tc]
            ax.plot(d["t"], d["hv"] * 9.807 / 3 * 0.84, "o", color=COLS[Tc], ms=3.5)
        ax.set_xscale("log")
        ax.set_xlabel("aging time, h")
        ax.set_ylabel("yield strength, MPa")
        ax.legend(fontsize=6.5, frameon=False, loc="lower left")
        ax.text(0.98, 0.95, "points: HV, Tabor-calibrated", transform=ax.transAxes, fontsize=7, ha="right",
                color="#444")
    return fig_panel(draw, 5.0, 3.0, title="Against TC-PRISMA for the measured composition",
                     tag="synthetic stand-in for TC-PRISMA")


def resistivity_parity_image(u, s=2.0):
    def draw(ax):
        calc = np.array([5.05, 3.92, 4.60, 3.55, 3.30])
        rng = np.random.default_rng(9)
        meas = calc * (1 + rng.normal(0.02, 0.03, calc.size))
        names = ["as-built", "aged", "as-built", "aged", "6063-T6"]
        mk = ["o", "s", "o", "s", "^"]
        for c, m, n, k in zip(calc, meas, names, mk):
            ax.plot(c, m, k, color="#1f4e8c", ms=6)
        ax.plot([3, 5.5], [3, 5.5], "--", color="#888", lw=1)
        ax.set_xlabel("Thermo-Calc, predicted phases, μΩ cm")
        ax.set_ylabel("measured (eddy current), μΩ cm")
        ax.text(0.04, 0.88, "o as-built   □ fully aged   △ 6063-T6", transform=ax.transAxes, fontsize=7)
    return fig_panel(draw, 4.6, 3.0, title="Resistivity vs Thermo-Calc's property model")


def c6():
    """Analysis, acceptance and the open questions, over the finished matrix of coupons."""
    sc = S.SOPScene("sop04_c6", TITLE)
    S.room(sc, x0=-1500, x1=1500)
    sc.add("mat", S.pv.Box(bounds=(-260, 260, -330, 20, BENCH_H, BENCH_H + 2)), (0.20, 0.34, 0.30), "mat",
           specular=0.05)
    zt = BENCH_H + 2.0
    rows = [("as-built", [None]), ("300 °C", TIMES), ("350 °C", TIMES), ("400 °C", TIMES)]
    for r, (name, ts) in enumerate(rows):
        for c, t in enumerate(ts):
            add_model(sc, f"m{r}_{c}", MP.coupon(), T((-180.0 + 70 * c, -60.0 - 70 * r, zt)))
    meter = S.place(sc, "eddy_meter", 420.0, -120.0, prefix="eddy:")
    for piece, M in (("probe", T((330.0, -260.0, BENCH_H + 9.5)) @ R((0, 1, 0), 90)),
                     ("standards", T((560.0, -250.0, BENCH_H)))):
        reparent(sc, f"eddy:{piece}", None)
        sc.gmat[f"eddy:{piece}"] = M
    au = audit.Audit(sc, allow=[])
    V0 = S.look((0, -170, BENCH_H), 1200, az=-15, el=48)
    V1 = S.look((0, -170, BENCH_H), 1000, az=15, el=55)
    sc.cam = V0
    sc.card("Analysis", ["HV(t) and ρ(t) at each temperature", "time to peak → Arrhenius Q; JMAK on ρ → n, k(T)",
                         "compare with TC-PRISMA and Thermo-Calc's resistivity"], seconds=3.5, label="Analysis",
            note="all data on screen are synthetic examples, computed with analysis/kinetics.py and conductivity.py")
    labels = [("as-built", (-180, -60, zt + 3), (0.12, 0.26))] + [
        (n, (-180, -60 - 70 * r, zt + 3), (0.12, 0.26 + 0.14 * r)) for r, (n, _) in enumerate(rows) if r]
    sc.step("Analysis", "16 conditions per alloy, each with HV and %IACS", 3.0, None, hold=1.4, labels=labels)
    for key, fn, cap, sub in (("curves", aging_curves_image, "HV(t) and ρ(t) at each temperature",
                               "the peak (star) moves earlier as T rises"),
                              ("arr", arrhenius_image, "Time to peak gives an Arrhenius Q", "kinetics.arrhenius"),
                              ("jmak", jmak_image, "f from ρ, fitted with JMAK: n and k(T)",
                               "conductivity.aging_fraction, kinetics.fit_jmak"),
                              ("prisma", prisma_image, "Compare with TC-PRISMA, measured composition",
                               "strength vs time, peak time vs T; matrix solute vs predicted"),
                              ("parity", resistivity_parity_image, "As-built and aged ρ vs Thermo-Calc",
                               "the property model on the predicted phase assemblage")):
        sc.panel(key, fn, rect=(0.30, 0.10, 0.44), alpha=0.0)
        sc.step("Analysis", f"{cap} | {sub}", 1.2, sc.fade_panel(key, 0, 1), hold=4.2,
                cam_to=V1 if key in ("arr", "prisma") else V0)
        sc.step("Analysis", f"{cap} | {sub}", 0.8, sc.fade_panel(key, 1, 0), hold=0.0)
    sc.card("Acceptance", ["hardness SD under 5 % on dense material",
                           "conductivity repeat readings within 0.3 %IACS",
                           "the references reproduce their tempers: a 6063 peak near the T6 schedule"],
            seconds=4.5, label="Acceptance")
    sc.card("Open questions", ["Is there an eddy-current meter on campus (an NDE or aerospace lab)?",
                               "If not, a used handheld unit is the cheapest high-throughput instrument on the list.",
                               "Furnace capacity for 16 conditions per alloy: batch by temperature."],
            seconds=5.0, label="Open questions")
    return sc, au, locals()


# ===================================================================================================== chapter 1
def checks_card(sc):
    sc.card("SOP 04 · Hardness and eddy-current conductivity, as-built and aged",
            ["Checks: yield strength (General Model Library; TC-PRISMA peak and over-aged)",
             "precipitation kinetics (TC-PRISMA; TTP as times to peak hardness)",
             "electrical resistivity (property model); solute left in solution after LPBF",
             "thermal conductivity: an AM Module input"], seconds=6.0, label="Checks",
            note="Draft SOP: thermo-calc-measurements/sops/04-hardness-conductivity-aging.md (#262)")


def c1():
    """The checks and the samples."""
    import r8_specimens as SP
    sc = S.SOPScene("sop04_c1", TITLE)
    S.room(sc, x0=-1500, x1=1500)
    zt = BENCH_H
    # the polished XZ sections from SOP 03
    for i in range(3):
        for part, (mesh, rgb, spec) in SP.hot_mount("polished").items():
            sc.add(f"xz{i}/{part}", mesh, rgb, f"xz{i}", specular=spec)
        sc.gmat[f"xz{i}"] = T((-520.0 + 55 * i, -120.0, zt))
    # one cube row on the plate, and the coupons cut from it (they appear when the caption says so)
    add_model(sc, "row", MP.cube_row(8), T((-120.0, -110.0, zt + 12.0)))
    cps = []
    for i in range(8):
        for k in range(3):
            g = f"cut{i}_{k}"
            add_model(sc, g, MP.coupon(), T((-160.0 + 26 * i, -205.0 - 14 * k, zt)))
            for n in sc.members(g):
                sc.alpha[n] = 0.0
            cps.append(g)
    add_model(sc, "cube5", Model5(), T((150.0, -205.0, zt)))
    # the references: a 6063 bar end and its coupons, printed AlSi10Mg and Scalmalloy-type coupons
    sc.add("bar/6063", S.pv.Cylinder(center=(0, 0, 13), direction=(1, 0, 0), radius=13.0, height=150.0,
                                     resolution=48), MP.MATERIALS["p4_coupon_6063"][:3], "bar", specular=0.6)
    sc.gmat["bar"] = T((380.0, -110.0, zt))
    for j, (x, mat) in enumerate(((330.0, "p4_coupon_6063"), (370.0, "p4_coupon"), (410.0, "p4_coupon"))):
        add_model(sc, f"ref{j}", MP.coupon(mat), T((x, -205.0, zt)))
    au = audit.Audit(sc, allow=[])
    V0 = S.look((-100, -150, zt + 40), 1100, az=-10, el=34)
    V_XZ = S.look((-465, -120, zt + 20), 380, az=-15, el=42)
    V_ROW = S.look((-50, -160, zt + 10), 520, az=0, el=46)
    V_REF = S.look((370, -160, zt + 10), 460, az=10, el=44)
    sc.cam = V0
    checks_card(sc)
    sc.step("Samples", "Samples for SOP 04", 2.6, None, hold=1.0,
            labels=[("polished XZ sections (SOP 03)", (-465, -120, zt + 20), (0.14, 0.30)),
                    ("one cube row, 10 mm cubes", (-120, -110, zt + 24), (0.46, 0.22)),
                    ("references", (380, -150, zt + 20), (0.84, 0.30))])
    sc.step("Samples", "Hardness: the polished XZ sections from SOP 03 | 38 mm conductive mounts, build "
            "direction up the face", 3.2, None, hold=1.6, cam_to=V_XZ)
    sc.step("Samples", "Conductivity: flat coupons, at least 10 x 10 mm, 2 mm thick", 3.0, None, hold=0.6,
            cam_to=V_ROW, labels=[("one cube row: the same build history", (-120, -110, zt + 24), (0.30, 0.24))])
    sc.step("Samples", "Cut from one cube row, so the build history is shared | three 3 mm coupons per 10 mm cube",
            3.0, fade(sc, [n for g in cps for n in sc.members(g)], 0, 1), hold=1.8,
            labels=[("coupons 10 x 10 x 3 mm", (-100, -220, zt + 3), (0.30, 0.78))])
    sc.step("Samples", "A 5 mm cube is too small for most probes | a small probe head, or a four-point probe",
            3.0, None, hold=1.8, cam_to=S.look((110, -200, zt + 5), 300, az=10, el=40),
            labels=[("5 mm cube (SOP 03)", (150, -205, zt + 5), (0.70, 0.30)),
                    ("10 x 10 x 3 mm coupon", (22, -233, zt + 3), (0.24, 0.30))])
    sc.panel("matrix", lambda u: matrix_image({("as-built", 0)}, None), rect=(0.60, 0.09, 0.38), alpha=0.0)
    sc.step("Samples", "Aging matrix: as-built, 300, 350 and 400 °C | 0.25, 1, 4, 16, 64 h, water quench: "
            "16 conditions", 3.0, sc.fade_panel("matrix", 0, 1), hold=3.0, cam_to=V0)
    sc.step("Samples", "Sc/Zr/Er alloys: add 250 °C", 2.4, None, hold=2.0)
    sc.step("Reference", "References through the same matrix | wrought 6063-T5/T6, printed AlSi10Mg, "
            "Scalmalloy-type", 3.0, sc.fade_panel("matrix", 1, 0), hold=2.4, cam_to=V_REF,
            labels=[("6063 bar stock", (380, -110, zt + 26), (0.30, 0.22)),
                    ("6063", (330, -205, zt + 3), (0.22, 0.70)), ("AlSi10Mg", (370, -205, zt + 3), (0.50, 0.80)),
                    ("Scalmalloy-type", (410, -205, zt + 3), (0.78, 0.70))])
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
CHAPTERS = {"sop04_c1": c1, "sop04_c2": c2, "sop04_c3": c3, "sop04_c4": c4, "sop04_c5": c5,
            "sop04_c6": c6}


def run(name):
    tot = [0.0]
    orig_step, orig_card = S.SOPScene.step, S.SOPScene.card

    def step(self, label, caption, seconds, update=None, hold=1.2, *a, **k):
        tot[0] += seconds + hold
        return orig_step(self, label, caption, seconds, update, hold, *a, **k)

    def card(self, heading, lines=(), seconds=3.0, *a, **k):
        tot[0] += seconds
        return orig_card(self, heading, lines, seconds, *a, **k)
    S.SOPScene.step, S.SOPScene.card = step, card
    sc, au, _ = CHAPTERS[name]()
    print(f"{name}: about {tot[0] + sc.intro:.0f} s of video", flush=True)
    import json as _j
    Path(f"/tmp/sop04/{name}_steps.json").write_text(_j.dumps(sc.substeps))
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
