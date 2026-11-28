"""Shared set-up for SOP 01's chapters (#262): the DSC bench, its instruments and props, the operator and the moves
the chapters reuse. ``sop01_dsc.py`` builds one chapter per SOP section from these.

Bench layout (x right, y away from the viewer, z up, mm; the bench top at z = 900): the micro riffle splitter and the
powder jar at the left, the microbalance and the crucibles left of centre, the STA in the middle right with its PC
to its right, the argon cylinder and the vacuum pump on the floor past the bench's right end.
"""
from __future__ import annotations

import math

import numpy as np

import stage as S
from stage import R, T

import common as LM
import models_dsc as M
import props as VP
from people import Person

BH = S.BENCH_H
# stations: (x, y) of each model's origin on the bench
RIF = (-1380.0, -170.0)
JAR = (-1200.0, -200.0)
BAL = (-760.0, -40.0)
TRAY = (-560.0, -230.0)           # the crucible tray
TOOLS = (-440.0, -250.0)          # tweezers and spatula lie here
BOTTLE = (-1000.0, 120.0)
CHIPS = (-1000.0, -230.0)         # the printed cube and its chip
STA = (120.0, 30.0)
STDS = (-260.0, -200.0)           # the calibration set
PC = (820.0, 40.0)
GAS = (1560.0, 220.0)             # the argon cylinder on the floor, past the bench end (x = 1300)
PUMP = (1560.0, -160.0)           # the vacuum pump on the floor
OP_Y = -720.0                     # where the operator stands, facing the bench (+y)
JAR_D, JAR_H, JAR_LID = 58.0, 76.0, 16.0      # the lab's 125 mL powder jar (vl/r8_store.py JARS)


def attach(sc, child: str, parent: str | None):
    """Re-parent a group, keeping where it is in the world."""
    w = sc.world(child)
    if parent is None:
        sc.parent.pop(child, None)
        sc.gmat[child] = w
    else:
        sc.parent[child] = parent
        sc.gmat[child] = np.linalg.inv(sc.world(parent)) @ w


def prop(sc, name: str, model, at, parent=None, tol=0.05):
    """A props() Model as its own group `name`, placed at 4x4 `at` (world, or in `parent`'s frame)."""
    ents = S.props(name, model, tol=tol)
    S.add_entries(sc, ents, name, name, at=at, parent=parent)
    return name


class Lab:
    """The bench and everything on it, in one scene. ``parts`` picks what to build (all by default)."""

    def __init__(self, sc, person: bool = True, parts=("riffle", "balance", "sta", "pc", "gas", "props")):
        self.sc = sc
        S.room(sc, x0=-1700.0, x1=1300.0)
        self.rig = {}
        if "riffle" in parts:
            self.rig["riffle"] = S.place(sc, "riffle_splitter", *RIF)
            self._jar()
        if "balance" in parts:
            self.rig["bal"] = S.place(sc, "microbalance", *BAL)
        if "sta" in parts:
            self.rig["sta"] = S.place(sc, "dsc_sta", *STA)
        if "gas" in parts:
            self.rig["gas"] = S.place(sc, "gas_supply", *GAS, z=0.0)
            self.rig["pump"] = S.place(sc, "vacuum_pump", *PUMP, z=0.0)
            self._hoses()
        if "pc" in parts:
            prop(sc, "pc", M.monitor_model(), T((PC[0], PC[1], BH)) @ R((0, 0, 1), -12))
        if "props" in parts:
            self._props()
        self.op = Op(sc) if person else None

    # ------------------------------------------------------------------------------------------- props
    def _jar(self):
        sc = self.sc
        self.jar = "jar"
        for part, (mesh, rgb, op) in VP.jar_parts(JAR_D, JAR_H, JAR_LID, fill=0.55).items():
            sc.add(f"jar/{part}", mesh, rgb, "jar", opacity=op, specular=0.5 if part == "glass" else 0.1)
        sc.gmat["jar"] = T((JAR[0], JAR[1], BH))

    def _props(self):
        sc = self.sc
        c = M.CRUCIBLE
        # the crucible tray: a small alumina-white block with six pockets (crucibles A, B, the reference, spares)
        tray = LM.Model("cru_tray", "crucible tray")
        blk = LM.box(-40, -18, 0, 40, 18, 8)
        self.tray_pts = []
        for i in range(6):
            x, y = -28 + 11.2 * i, 0.0
            blk = blk.cut(LM.cyl(c["od"] + 0.8, 3.0, x=x, y=y, z=5.0))
            self.tray_pts.append((TRAY[0] + x, TRAY[1] + y, BH + 5.0))
        tray.add("tray", blk, "dsc_dark")
        prop(sc, "tray", tray, T((TRAY[0], TRAY[1], BH)))
        self.cru = {}
        for k, nm in enumerate(("cruA", "cruB", "cruR")):
            prop(sc, nm, M.crucible_model(), T(self.tray_pts[k]))
            prop(sc, f"{nm}_lid", M.lid_model(), T(np.add(self.tray_pts[k + 3], (0, 0, 0.0))))
            self.cru[nm] = nm
        prop(sc, "tweezers", M.tweezers_model(), T((TOOLS[0], TOOLS[1], BH + 0.6)) @ R((0, 0, 1), 200))
        prop(sc, "spatula", M.spatula_model(), T((TOOLS[0] + 60, TOOLS[1] + 60, BH)) @ R((0, 0, 1), 195))
        prop(sc, "bottle", M.wash_bottle_model(), T((BOTTLE[0], BOTTLE[1], BH)) @ R((0, 0, 1), 20))
        prop(sc, "stds", M.standards_model(), T((STDS[0], STDS[1], BH)))
        prop(sc, "cube", M.cube_model(), T((CHIPS[0], CHIPS[1], BH)))
        prop(sc, "chip", M.chip_model(), T((CHIPS[0] + 25, CHIPS[1], BH)))

    def _hoses(self):
        """Gas line from the cylinder's regulator to the STA's inlet, and the vacuum hose from the pump: drawn in the
        world with their ends on the fittings (models publish them in GAS_POINTS / PUMP_POINTS / STA_POINTS). Both
        come up past the bench's end (x = 1300) and run along the back of the bench top to the STA."""
        sc = self.sc
        sta = self.rig["sta"]
        g = self.rig["gas"]
        pump = self.rig["pump"]
        a = g.world(M.GAS_POINTS["outlet"])
        b = sta.world(M.STA_POINTS["gas_in"])
        yb, zt = 355.0, BH + 4.0
        pts = [tuple(a), (a[0] - 140.0, a[1], a[2]), (1340.0, yb, a[2] - 120.0), (1340.0, yb, zt), (b[0], yb, zt),
               (b[0], yb, b[2]), tuple(b)]
        sc.add("hose/gas", S.to_mesh(LM.hose(pts, 6.0).val(), 0.3), S.MATERIALS["ptfe"][:3], "hoses", specular=0.1)
        a = pump.world(M.PUMP_POINTS["inlet"])
        b = sta.world(M.STA_POINTS["vac_port"])
        yv, zv = 335.0, BH + 12.0
        pts = [tuple(a), (a[0], a[1], a[2] + 80.0), (1360.0, yv, BH + 40.0), (1300.0, yv, zv), (b[0], yv, zv),
               (b[0], yv, b[2]), tuple(b)]
        sc.add("hose/vac", S.to_mesh(LM.hose(pts, 22.0).val(), 0.5), (0.12, 0.12, 0.13), "hoses", specular=0.2)


class Op:
    """The operator (people.Person) with where they stand, and update(u) makers for walking and reaching."""

    def __init__(self, sc, name="person", x=-1380.0, y=OP_Y, hd=0.0):
        self.sc = sc
        self.p = Person(sc, name)
        self.x, self.y, self.hd = x, y, hd
        self.phase = 0.0
        self.lean = 0.0
        self.hands = {"l": None, "r": None}
        self.look = None
        self.p.set(x=x, y=y, hd=hd, lean=0.0, phase=0.0, amp=0.0, hands=dict(self.hands))

    def set(self, **kw):
        for k in ("x", "y", "hd", "lean", "look"):
            if k in kw:
                setattr(self, k, kw[k])
        if "hands" in kw:
            self.hands.update(kw["hands"])
        self.p.set(**kw)

    def walk(self, x1, y1=None, hd1=None, look=None):
        """update(u): walk in steps to (x1, y1), turning to hd1; the gait's phase follows the distance walked."""
        y1 = self.y if y1 is None else y1
        st = {}

        def up(u):
            if not st:
                st.update(x0=self.x, y0=self.y, hd0=self.hd, ph0=self.phase)
                st["L"] = math.hypot(x1 - st["x0"], y1 - st["y0"])
            L = st["L"]
            x = st["x0"] + (x1 - st["x0"]) * u
            y = st["y0"] + (y1 - st["y0"]) * u
            d = L * u
            ph = st["ph0"] + 2 * math.pi * d / Person.STRIDE
            amp = min(1.0, d / 250.0, (L - d) / 250.0) if L > 1 else 0.0
            hd = st["hd0"] + ((hd1 if hd1 is not None else st["hd0"]) - st["hd0"]) * u
            self.x, self.y, self.hd, self.phase = x, y, hd, ph
            self.p.set(x=x, y=y, hd=hd, phase=ph, amp=max(0.0, amp), look=look)
        return up

    def reach(self, side, path, lean=None, look=None, palm=None, grip=None):
        """update(u): the `side` hand along `path` (a list of world points, or a function u -> point; None = rest),
        leaning from the current lean to `lean`."""
        st = {}

        def up(u):
            if not st:
                st.update(lean0=self.lean)
            if callable(path):
                tgt = path(u)
            elif path is None:
                tgt = None
            else:
                pts = np.asarray(path, float)
                s = min(max(u, 0.0), 1.0) * (len(pts) - 1)
                i = min(int(s), len(pts) - 2)
                tgt = pts[i] + (pts[i + 1] - pts[i]) * (s - i)
            kw = dict(hands={side: None if tgt is None else tuple(tgt)})
            if lean is not None:
                self.lean = st["lean0"] + (lean - st["lean0"]) * u
                kw["lean"] = self.lean
            if look is not None:
                kw["look"] = look(u) if callable(look) else look
            if palm is not None:
                kw["palm"] = {side: palm}
            if grip is not None:
                kw["grip"] = {side: grip}
            self.hands[side] = kw["hands"][side]
            self.p.set(**kw)
        return up

    def hand(self, side="r"):
        return self.p.hand_point(side)

    def hold(self, side, group):
        self.p.hold(side, group)

    def let_go(self, side, parent=None):
        self.p.let_go(side, parent)


def tilt_about(point, axis, deg):
    return R(axis, deg, point)
