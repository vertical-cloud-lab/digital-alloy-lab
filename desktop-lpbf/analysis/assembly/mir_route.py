"""MiR250 base moves as a differential-drive base makes them: pivot, drive along the heading, pivot (round 8, issue #260, PR #266).

Sterling, 2026-11-26, on the round-7 video: "moonwalk". Round 7's MiRs slid along their lanes in x, in reverse half the time
(record.py's `drive` was only the base's x). A MiR250 is differential drive: it can pivot in place and drive along its heading;
it cannot slide sideways, and here it reverses only as a short docking leg (byu-vcl PR 318, lesson 2 of
notes/2026-11-26-byu-vcl-video-lessons.md).

Rules used by commit.goto() for every recorded base move:
  * every MiR docks heading +x, its arm on the bench side, as cell2 places it (at the bench, the fixtures and the long table);
  * a move toward +x is one forward drive along the lane (trapezoid 0.3 m/s^2, 1.0 m/s, the MiR250 datasheet's figures as used
    in record.py); no pivot;
  * a move toward -x of at most REV_MAX is a straight reverse: the docking leg;
  * a longer move toward -x turns round: at a clear spot the MiR pivots 90 deg away from the bench, drives LANE_OUT mm out,
    pivots 90 deg to face -x, drives forward along the return lane, and at a clear spot at or behind the dock turns back in the
    same way (pivot 90, LANE_OUT in, pivot 90 to +x), then drives forward to the dock (or reverses at most REV_MAX into it).
    The return lane is LANE_OUT further out because facing -x the tool stand and the screw presenter, hung on the cabinet's
    far face, are on the bench side: on the dock lane they would reach under the bench top and into the table legs.
  * Every pose of every leg is checked with FCL (cell.py) for the MiR body, cabinet, mounting plate, tool stand, screw
    presenter and the parked arm with its tool and anything it holds, against the cell (bench, fixtures, the machine parts
    present), the other MiR and its arm, and the long table (top, legs, nests, trays, the items still on it): pivots every
    PIV_STEP deg (about 20 mm of arc at the presenter's 588 mm radius), straight legs every 20 mm (fetch.DRIVE_STEP).
  * A clear spot is searched for along the lane in SPOT_STEP steps, nearest first; spots blocked by the MiR or its arm (not
    by a held part) are remembered per MiR, turn and lane, since the cell's furniture does not move.

Pivot rate: PIV_RATE deg/s with T_PIV_RAMP s to start and stop. This is an ESTIMATE: MiR publishes the MiR250's linear speed
and acceleration but no pivot rate that was found for this note.
"""
from __future__ import annotations

import math

import numpy as np

import cell2 as K
from cell import Body, Group, Tm, rot, hit

LANE_OUT = 130.0            # mm: the return lane, further from the bench (facing -x the stand and presenter are on the bench side)
REV_MAX = 500.0             # mm: the longest reverse, as a docking leg
SPOT_STEP = 100.0           # mm between candidate turning spots
SPOT_FWD = 4500.0           # mm: how far ahead (+x) a turn-out spot may be looked for
SPOT_BACK = 5000.0          # mm: how far behind the dock (-x) a turn-in spot may be looked for
PIV_STEP = 2.0              # deg between checked pivot poses
LINE_STEP = 20.0            # mm between checked poses on a straight leg
PIV_RATE, T_PIV_RAMP = 30.0, 0.5      # deg/s and s: ESTIMATE (no published MiR250 pivot rate)
MIR_A, MIR_V = 300.0, 1000.0          # mm/s^2, mm/s: MiR250 datasheet (record.py)
_BLOCKED = {}               # (arm, turn kind, x rounded) -> why: spots blocked by the MiR or the arm itself


def line_time(d):
    d = abs(float(d))
    if d < 1e-6:
        return 0.0
    d_acc = MIR_V ** 2 / MIR_A
    if d >= d_acc:
        return d / MIR_V + MIR_V / MIR_A
    return 2.0 * math.sqrt(d / MIR_A)


def pivot_time(dth_deg):
    a = abs(float(dth_deg))
    return 0.0 if a < 1e-6 else a / PIV_RATE + T_PIV_RAMP


class Base:
    """MiR n's bodies and its parked arm, posed at (x, y, heading) of the MiR's centre; checks against a world Group."""

    def __init__(self, run, n, q, close, world):
        self.run, self.n = run, n
        cl = run.cl
        self.a = run.arm(n)
        self.side = self.a.side
        self.s = -1.0 if self.side == "front" else 1.0          # outward (away from the bench) in y
        self.yc0 = self.s * (K.ARM_Y + K.ARM_OFF)               # the dock lane's centre line
        self.yaw0 = 0.0 if self.side == "front" else 180.0
        self.base_ref = Tm(rot((0, 0, 1), self.yaw0), (0.0, self.s * K.ARM_Y, K.ARM_Z))
        self.mir = [Body(f"{n} {nm.split(' ', 1)[1]}", v, f, kind="cell") for nm, (v, f), _c in K.mir_bodies(n, 0.0, self.side)]
        self.q, self.close = np.asarray(q, float), close
        self.world = world
        self.names, self.lo, self.hi = world.boxes()
        keep = [k for k, nm in enumerate(self.names) if nm != "floor"]
        self.names = [self.names[k] for k in keep]
        self.lo, self.hi = self.lo[keep], self.hi[keep]
        self.saved_base = self.a.base.copy()

    def T(self, x, y, th_deg):
        return Tm(p=(x, y, 0.0)) @ Tm(rot((0, 0, 1), th_deg)) @ Tm(p=(0.0, -self.yc0, 0.0))

    def check(self, x, y, th):
        """None if clear, else (what hits, what it hits, by_robot) where by_robot: the MiR or the arm, not a held part."""
        T = self.T(x, y, th)
        for b in self.mir:
            b.place(T)
        self.a.base = T @ self.base_ref
        self.a.place(self.q, self.close)
        held = self.a.held[0] if self.a.held is not None else None
        for b in self.mir + list(self.a.bodies()):
            l, h = b.box()
            ov = np.nonzero(np.all((l[None, :] <= self.hi) & (self.lo <= h[None, :]), axis=1))[0]
            for j in ov:
                y_ = self.world.bodies[self.names[j]]
                if hit(b.obj, y_.obj):
                    return (b.name.split("/")[-1], y_.name[:60], b is not held)
        return None

    def restore(self):
        self.a.base = self.saved_base
        self.a.place(self.run.q[self.n])

    # ---- legs
    def pivot(self, x, y, th0, th1):
        k = max(1, int(math.ceil(abs(th1 - th0) / PIV_STEP)))
        for i in range(k + 1):
            th = th0 + (th1 - th0) * i / k
            c = self.check(x, y, th)
            if c:
                return c + (f"pivot at x {x:.0f}, {th:.0f} deg",)
        return None

    def line(self, x0, y0, x1, y1, th):
        d = math.hypot(x1 - x0, y1 - y0)
        k = max(1, int(math.ceil(d / LINE_STEP)))
        for i in range(k + 1):
            x, y = x0 + (x1 - x0) * i / k, y0 + (y1 - y0) * i / k
            c = self.check(x, y, th)
            if c:
                return c + (f"driving at x {x:.0f}, y {y:.0f}",)
        return None

    # ---- the turn-round at a spot: out (from the dock lane, facing +x, to the return lane facing -x) or in (the reverse)
    def turn(self, x, kind):
        """The three legs of a turn at x; -> (legs, None) or (None, hit)."""
        s = self.s
        yi, yo = self.yc0, self.yc0 + s * LANE_OUT
        # facing outward is heading -90 deg (front, y < 0) or +90 deg (back): the MiR turns away from the bench
        out = -90.0 if s < 0 else 90.0
        if kind == "out":
            seq = [("pivot", x, yi, 0.0, out), ("line", x, yi, x, yo, out), ("pivot", x, yo, out, 2 * out)]
        else:
            seq = [("pivot", x, yo, 2 * out, 3 * out), ("line", x, yo, x, yi, 3 * out), ("pivot", x, yi, 3 * out, 4 * out)]
        legs = []
        for lg in seq:
            if lg[0] == "pivot":
                c = self.pivot(lg[1], lg[2], lg[3], lg[4])
                legs.append(dict(kind="pivot", x=lg[1], y=lg[2], th0=lg[3], th1=lg[4], dur=round(pivot_time(lg[4] - lg[3]), 2)))
            else:
                c = self.line(lg[1], lg[2], lg[3], lg[4], lg[5])
                legs.append(dict(kind="line", x0=lg[1], y0=lg[2], x1=lg[3], y1=lg[4], th=lg[5], rev=False,
                                 dur=round(line_time(math.hypot(lg[3] - lg[1], lg[4] - lg[2])), 2)))
            if c:
                return None, c
        return legs, None

    def find_turn(self, x_from, kind, cands):
        """The first clear turn among the candidate spots (in order). -> (x, legs, tried, why_first)"""
        why_first, tried = None, 0
        for xs in cands:
            key = (self.n, kind, round(xs / 10.0), self.a.tool_name)
            if key in _BLOCKED:
                continue
            tried += 1
            legs, c = self.turn(xs, kind)
            if legs is not None:
                return xs, legs, tried, why_first
            if why_first is None:
                why_first = f"{c[0]} hits {c[1]} ({c[3]})"
            if c[2] and self.held_is_none_or_robot(c):
                _BLOCKED[key] = c
        return None, None, tried, why_first

    def held_is_none_or_robot(self, c):
        # remember only blocks by furniture that never moves: the bench, fixtures, the long table's top and legs
        w = c[1]
        return any(w.startswith(p) for p in ("bench", "Trunnion stands", "Fixture", "Stack nest", "Module nest",
                                             "long table top", "long table leg"))


def plan(run, n, x0, x1, q, close, world):
    """Route of MiR n from dock x0 to dock x1 (both heading +x). -> dict(ok, why, legs, rev_mm, pivots, dist_mm, dur)."""
    B = Base(run, n, q, close, world)
    y = B.yc0
    try:
        dx = x1 - x0
        if dx >= 0.0 or -dx <= REV_MAX:
            rev = dx < 0.0
            c = B.line(x0, y, x1, y, 0.0)
            legs = [dict(kind="line", x0=x0, y0=y, x1=x1, y1=y, th=0.0, rev=rev, dur=round(line_time(dx), 2))]
            return _out(legs, c)
        # turn out: at x0, or ahead (+x, forward), or behind by at most REV_MAX (a reverse docking leg)
        cands_out = [x0] + [x0 + k * SPOT_STEP for k in range(1, int(SPOT_FWD / SPOT_STEP) + 1)]
        cands_out += [x0 - k * SPOT_STEP for k in range(1, int(REV_MAX / SPOT_STEP) + 1)]
        cands_out.sort(key=lambda v: (abs(v - x0) if v >= x0 else 2.0 * abs(v - x0)))
        cands_out = [v for v in cands_out if v > x1 + 2 * REV_MAX]        # it must turn before the dock it goes to
        xo, legs_o, tried_o, why_o = B.find_turn(x0, "out", cands_out)
        if xo is None:
            return dict(ok=False, why=f"no clear spot to turn out within {SPOT_FWD:.0f} mm ahead ({tried_o} tried; first: {why_o})",
                        legs=None)
        # turn in: at x1, or behind it (-x, then forward to the dock), or ahead by at most REV_MAX (reverse into the dock)
        cands_in = [x1] + [x1 - k * SPOT_STEP for k in range(1, int(SPOT_BACK / SPOT_STEP) + 1)]
        cands_in += [x1 + k * SPOT_STEP for k in range(1, int(REV_MAX / SPOT_STEP) + 1)]
        cands_in.sort(key=lambda v: (abs(v - x1) if v <= x1 else 2.0 * abs(v - x1)))
        cands_in = [v for v in cands_in if v < xo - 2 * SPOT_STEP]
        xi, legs_i, tried_i, why_i = B.find_turn(x1, "in", cands_in)
        if xi is None:
            return dict(ok=False, why=f"no clear spot to turn in within {SPOT_BACK:.0f} mm behind the dock ({tried_i} tried; "
                                      f"first: {why_i})", legs=None)
        yo = y + B.s * LANE_OUT
        th_back = 2 * (-90.0 if B.s < 0 else 90.0)
        legs = []
        if abs(xo - x0) > 1e-6:
            legs.append(dict(kind="line", x0=x0, y0=y, x1=xo, y1=y, th=0.0, rev=xo < x0, dur=round(line_time(xo - x0), 2)))
        legs += legs_o
        legs.append(dict(kind="line", x0=xo, y0=yo, x1=xi, y1=yo, th=th_back, rev=False, dur=round(line_time(xo - xi), 2)))
        legs += legs_i
        if abs(x1 - xi) > 1e-6:
            legs.append(dict(kind="line", x0=xi, y0=y, x1=x1, y1=y, th=2 * th_back, rev=xi > x1, dur=round(line_time(x1 - xi), 2)))
        # check the straight legs (the turns were checked by find_turn)
        c = None
        for lg in legs:
            if lg["kind"] == "line" and abs(lg["y1"] - lg["y0"]) < 1e-6:
                c = B.line(lg["x0"], lg["y0"], lg["x1"], lg["y1"], lg["th"])
                if c:
                    break
        return _out(legs, c)
    finally:
        B.restore()


def _out(legs, c):
    rev = sum(abs(lg["x1"] - lg["x0"]) for lg in legs if lg["kind"] == "line" and lg.get("rev"))
    dist = sum(math.hypot(lg["x1"] - lg["x0"], lg["y1"] - lg["y0"]) for lg in legs if lg["kind"] == "line")
    piv = sum(abs(lg["th1"] - lg["th0"]) for lg in legs if lg["kind"] == "pivot")
    dur = sum(lg["dur"] for lg in legs)
    return dict(ok=c is None, why="" if c is None else f"{c[0]} hits {c[1]} ({c[3]})", legs=legs, rev_mm=round(rev, 1),
                dist_mm=round(dist, 1), pivot_deg=round(piv, 1), n_pivots=sum(1 for lg in legs if lg["kind"] == "pivot"),
                dur=round(dur, 2))
