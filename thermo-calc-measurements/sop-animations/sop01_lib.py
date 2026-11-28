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
# stations: (x, y) of each model's origin on the bench (the front edge is at y = -380, the wall at y = +382)
RIF = (-1450.0, -200.0)
JAR = (-1330.0, -265.0)
PAN_SPOT = (-1060.0, -290.0)      # where the split half is set down, left of the balance
TRAY = (-960.0, -170.0)           # the crucible tray
TRAY_STA = (-110.0, -300.0)       # ... and where it goes beside the STA
TOOLS = (-900.0, -320.0)          # tweezers and spatula lie here
BOTTLE = (-1260.0, -110.0)
CHIPS = (-1185.0, -255.0)         # the printed cube and its chip, on a wipe
BAL = (-800.0, -110.0)
STDS = (-300.0, -250.0)           # the calibration set
STA = (250.0, 0.0)
PC = (960.0, 60.0)
GAS = (1560.0, 220.0)             # the argon cylinder on the floor, past the bench end (x = 1300)
PUMP = (1560.0, -170.0)           # the vacuum pump on the floor
OP_Y = -650.0                     # where the operator stands, facing the bench (+y)
OP_Y_STA = -600.0                 # ... at the STA, a step closer (its sensor is 280 mm behind its front)
STA_OP_X = STA[0] - 106.5 - 150.0  # ... and a little left of the sensor, between it and the tray
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
            prop(sc, "pc", M.monitor_model(), T((PC[0], PC[1], BH)) @ R((0, 0, 1), -8))
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
        # the crucible tray: a dark block with eight pockets (crucibles A, B, the reference R, C for a chip; lids)
        tray = LM.Model("cru_tray", "crucible tray")
        blk = LM.box(-46, -18, 0, 46, 18, 8)
        self.pocket = []
        for i in range(8):
            x, y = -38.5 + 11.0 * i, 0.0
            blk = blk.cut(LM.cyl(c["od"] + 1.0, 3.0, x=x, y=y, z=5.0))
            self.pocket.append(np.array((TRAY[0] + x, TRAY[1] + y, BH + 5.0)))
        tray.add("tray", blk, "dsc_dark")
        prop(sc, "tray", tray, T((TRAY[0], TRAY[1], BH)))
        for k, nm in enumerate(("cruA", "cruB", "cruR", "cruC")):
            prop(sc, nm, M.crucible_model(), T(self.pocket[k]))
            prop(sc, f"{nm}_lid", M.lid_model(), T(self.pocket[k + 4]))
            # what each crucible holds, hidden until it is filled: powder, a sintered cake, the melt, the bead
            self._contents(nm)
        prop(sc, "tweezers", M.tweezers_model(), self.tw_rest())
        prop(sc, "spatula", M.spatula_model(), T((TOOLS[0] + 20, TOOLS[1] + 45, BH)) @ R((0, 0, 1), 160))
        prop(sc, "bottle", M.wash_bottle_model(), T((BOTTLE[0], BOTTLE[1], BH)) @ R((0, 0, 1), 20))
        prop(sc, "stds", M.standards_model(), T((STDS[0], STDS[1], BH)))
        wipe = LM.Model("wipe", "lint-free wipe")
        wipe.add("wipe", LM.box(-55, -40, 0, 55, 40, 0.3), "dsc_paper")
        prop(sc, "wipe", wipe, T((CHIPS[0] + 12, CHIPS[1], BH)))
        prop(sc, "cube", M.cube_model(), T((CHIPS[0], CHIPS[1], BH + 0.3)))
        prop(sc, "chip", M.chip_model(), T((CHIPS[0] + 25, CHIPS[1], BH + 0.3)))
        pt = LM.Model("pt_cru", "Pt/Rh crucible 85 uL")
        pt.add("pt", M.crucible_model("dsc_pt").parts[0].shape, "dsc_pt")
        prop(sc, "ptcru", pt, T((TRAY[0] + 60.0, TRAY[1] - 10.0, BH)))
        sc.show([n for n in sc.actors if n.startswith("ptcru/")], 0.0)
        # the split half that is carried to the balance: a copy of the splitter's right pan with its powder, hidden
        inst, _ = S.get("riffle_splitter")
        ents = S.props("pan_carry", inst.pieces["pan_r"]) + S.props("pan_carry_powder", inst.pieces["split_r"])
        self.pan_names = S.add_entries(sc, ents, "pan_carry", "pan_carry")
        sc.show(self.pan_names, 0.0)

    def tw_rest(self):
        return T((TOOLS[0], TOOLS[1], BH + 0.6)) @ R((0, 0, 1), 200)

    def tray_world(self, k):
        """Pocket k's floor point in the world, wherever the tray is now."""
        loc = self.pocket[k] - np.array((TRAY[0], TRAY[1], BH))
        return (self.sc.world("tray") @ np.r_[loc, 1.0])[:3]

    def _contents(self, nm):
        """Powder bed, sintered cake, melt and bead in crucible `nm` (its frame: base at the origin), all hidden."""
        sc = self.sc
        c = M.CRUCIBLE
        ri = c["od"] / 2 - c["wall"]
        fl = c["floor"]
        import pyvista as pv
        bed = pv.Cylinder(center=(0, 0, fl + 0.9), direction=(0, 0, 1), radius=ri - 0.05, height=1.8, resolution=40)
        cake = pv.Cylinder(center=(0, 0, fl + 0.75), direction=(0, 0, 1), radius=ri - 0.35, height=1.5, resolution=40)
        bead = pv.Sphere(radius=1.75, center=(0, 0, fl + 1.05), theta_resolution=40, phi_resolution=30)
        bead.points[:, 2] = np.maximum(bead.points[:, 2], fl + 0.02)          # flat where it sits on the floor
        P = S.MATERIALS
        sc.add(f"{nm}/bed", bed, P["al_powder"][:3], nm, specular=0.02)
        sc.add(f"{nm}/cake", cake, (0.52, 0.53, 0.55), nm, specular=0.05)
        sc.add(f"{nm}/melt", bead.copy(), M.MATERIALS["dsc_hot"][:3], nm, specular=0.3, ambient=0.6, diffuse=0.5)
        sc.add(f"{nm}/bead", bead, M.MATERIALS["dsc_bead"][:3], nm, specular=0.85)
        for k in ("bed", "cake", "melt", "bead"):
            sc.alpha[f"{nm}/{k}"] = 0.0

    def fill(self, nm, **a):
        """Set what crucible `nm` shows: fill(nm, bed=1, cake=0, melt=0, bead=0)."""
        for k, v in a.items():
            self.sc.alpha[f"{nm}/{k}"] = float(v)

    def _hoses(self):
        """The argon line from the regulator along the wall to the STA's inlet on its left side, and the vacuum hose
        from the pump up past the bench's end and along the back of the bench top to the port on the STA's right."""
        sc = self.sc
        sta = self.rig["sta"]
        g = self.rig["gas"]
        pump = self.rig["pump"]
        a = g.world(M.GAS_POINTS["outlet"])
        b = sta.world(M.STA_POINTS["gas_in"])
        zw, yw = BH + 300.0, 368.0
        xl = b[0] - 40.0
        pts = [tuple(a), (a[0], a[1] + 60.0, a[2]), (1340.0, yw, zw + 40.0), (1340.0, yw, zw), (xl, yw, zw)]
        sc.add("hose/gas_pipe", S.to_mesh(LM.hose(pts, 8.0).val(), 0.3), (0.62, 0.64, 0.66), "hoses", specular=0.5)
        pts = [(xl, yw, zw), (xl, yw, BH + 6.0), (xl, b[1], BH + 6.0), (xl, b[1], b[2]), tuple(b)]
        sc.add("hose/gas", S.to_mesh(LM.hose(pts, 6.0).val(), 0.3), S.MATERIALS["ptfe"][:3], "hoses", specular=0.1)
        a = pump.world(M.PUMP_POINTS["inlet"])
        b = sta.world(M.STA_POINTS["vac_port"])
        yv = 268.0
        pts = [tuple(a), (a[0], a[1], a[2] + 90.0), (1350.0, yv, BH + 60.0), (1290.0, yv, BH + 12.0),
               (b[0] + 60.0, yv, BH + 12.0), (b[0] + 60.0, yv, b[2]), (b[0] + 2.0, b[1], b[2])]
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
