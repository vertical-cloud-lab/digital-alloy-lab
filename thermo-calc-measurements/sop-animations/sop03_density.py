"""SOP 03 (#262): Archimedes density, porosity and crack density of printed cubes, animated step by step.

    xvfb-run -a python sop03_density.py sop03_c1      # one chapter -> out/mp4/sop03_c1.mp4
    xvfb-run -a python sop03_density.py join          # out/mp4/sop03.mp4, out/sop03.json, contact sheet, preview GIF
    PREVIEW=1 xvfb-run -a python sop03_density.py sop03_c2   # the last frame of each sub-step -> /tmp/preview_sop03_c2.png

Chapters: c1 Samples (cut, label, clean, dry, the reference cube); c2 Archimedes set-up (balance and kit, water and
wetting agent, temperature, bubbles, tare); c3 Weighing (three times in air, three times in water, the result, the
uncertainty, the reference density, the time, acceptance); c4 Sections (XZ section, polish, stitched images, Otsu
porosity, pore type, cracks, time, acceptance); c5 Notes (open porosity; the printability map).

Models: models_density.py (the XPR225DR with its density kit, the Branson CPX2800H, the Memmert UN30, the AccuPyc II
1345, and the small things); SOP 02's LECO VC50 saw (models_track.py); byu-vcl's LECO MX400 press, PX500 polisher and
Keyence VHX-7000. Panels: sop03_panels.py (the repo's density_porosity.py on synthetic inputs).
"""
from __future__ import annotations

import math
import sys

import numpy as np

import stage as S
from stage import R, T

import models_density as MD
import sop03_panels as P

BH = S.BENCH_H
TITLE = "SOP 03 · Archimedes density, porosity and cracks"
PANEL = (0.685, 0.085, 0.30)          # top right, 30 % of the width
CHAPTERS: dict = {}


def chapter(name):
    def deco(f):
        CHAPTERS[name] = f
        return f
    return deco


# ============================================================================================ helpers
def cam_hold(sc, cam):
    sc.cam = [tuple(map(float, c)) for c in cam]


def prop(sc, name, model, at, parent=None, tol=0.05):
    ents = S.props(name, model, tol=tol)
    S.add_entries(sc, ents, name, name, at=at, parent=parent)
    return name


def names_of(sc, group):
    return [n for n, g in sc.group_of.items() if g == group]


def fade(sc, names, a0, a1):
    def up(u):
        for n in names:
            sc.alpha[n] = a0 + (a1 - a0) * u
    return up


def drop(sc, names):
    for n in list(names):
        a = sc.actors.pop(n, None)
        if a is None:
            continue
        sc.pl.remove_actor(a)
        for dct in (sc.group_of, sc.alpha, sc.base_alpha):
            dct.pop(n, None)
        sc.__dict__.get("_keep", {}).pop(n, None)
        sc.__dict__.get("_sent", {}).pop(n, None)


def drop_pieces(rig, pieces=(), match=None):
    for pc in pieces:
        drop(rig.sc, rig.names.get(pc, []))
        rig.names[pc] = []
    if match:
        for pc, ns in rig.names.items():
            gone = [n for n in ns if any(m in n for m in match)]
            drop(rig.sc, gone)
            rig.names[pc] = [n for n in ns if n not in gone]


def attach(sc, child, parent):
    w = sc.world(child)
    if parent is None:
        sc.parent.pop(child, None)
        sc.gmat[child] = w
    else:
        sc.parent[child] = parent
        sc.gmat[child] = np.linalg.inv(sc.world(parent)) @ w


def gauge(sc, items):
    def up(u):
        sc.gauges = [(k, v(u) if callable(v) else v) for k, v in items]
    return up


def audit_for(sc, allow=()):
    import audit
    return audit.Audit(sc, allow=list(allow))


def tool_pose(tip, yaw, pitch):
    """A tool whose tip is at its origin and handle along +x: the tip at `tip`, turned yaw about z, the handle raised
    `pitch` degrees."""
    return T(tip) @ R((0, 0, 1), yaw) @ R((0, 1, 0), -pitch)


def lerp_path(pts, u):
    pts = [np.asarray(p, float) for p in pts]
    if len(pts) == 1:
        return pts[0]
    s = min(max(u, 0.0), 1.0) * (len(pts) - 1)
    i = min(int(s), len(pts) - 2)
    return pts[i] + (pts[i + 1] - pts[i]) * (s - i)


class Tool:
    """A hand tool (tweezers, brush) moved by its tip along a path, the operator's hand following its grip; it can
    carry a cube between its tips."""

    def __init__(self, sc, name, model, op=None, grip_x=88.0, carry_off=(3.0, 0.0, -2.5)):
        self.sc, self.g, self.op, self.grip_x = sc, name, op, grip_x
        prop(sc, name, model, np.eye(4))
        self.tip, self.yaw, self.pitch = np.zeros(3), 0.0, 0.0
        self.carry, self.carry_off = None, np.asarray(carry_off, float)

    def put(self, tip, yaw, pitch, hand=True):
        self.tip, self.yaw, self.pitch = np.asarray(tip, float), float(yaw), float(pitch)
        M = tool_pose(self.tip, self.yaw, self.pitch)
        self.sc.gmat[self.g] = M
        self.sc.parent.pop(self.g, None)
        if self.carry is not None:
            off = R((0, 0, 1), self.yaw)[:3, :3] @ self.carry_off
            self.sc.gmat[self.carry] = T(self.tip + off)
            self.sc.parent.pop(self.carry, None)
        if hand and self.op is not None:
            g = (M @ np.r_[self.grip_x, 0.0, 9.0, 1.0])[:3]
            self.op.p.set(hands={"r": tuple(g)}, grip={"r": 0.75})

    def path(self, pts, yaw0=None, yaw1=None, pitch0=None, pitch1=None, hand=True):
        st = {}

        def up(u):
            if not st:
                st.update(y0=self.yaw if yaw0 is None else yaw0, p0=self.pitch if pitch0 is None else pitch0)
            y1 = st["y0"] if yaw1 is None else yaw1
            p1 = st["p0"] if pitch1 is None else pitch1
            self.put(lerp_path(pts, u), st["y0"] + (y1 - st["y0"]) * u, st["p0"] + (p1 - st["p0"]) * u, hand)
        return up


class Op:
    """The operator (people.Person), standing, walking in steps, reaching."""

    def __init__(self, sc, name="op", x=0.0, y=-620.0, hd=0.0):
        from people import Person
        self.Person = Person
        self.sc = sc
        self.p = Person(sc, name)
        self.x, self.y, self.hd, self.phase, self.lean = x, y, hd, 0.0, 0.0
        self.p.set(x=x, y=y, hd=hd, lean=0.0, phase=0.0, amp=0.0, hands={"l": None, "r": None})

    def set(self, **kw):
        for k in ("x", "y", "hd", "lean"):
            if k in kw:
                setattr(self, k, kw[k])
        self.p.set(**kw)

    def walk(self, x1, y1=None, hd1=None, look=None):
        y1 = self.y if y1 is None else y1
        st = {}

        def up(u):
            if not st:
                st.update(x0=self.x, y0=self.y, hd0=self.hd, ph0=self.phase)
                st["L"] = math.hypot(x1 - st["x0"], y1 - st["y0"])
            L = st["L"]
            d = L * u
            ph = st["ph0"] + 2 * math.pi * d / self.Person.STRIDE
            amp = min(1.0, d / 250.0, (L - d) / 250.0) if L > 1 else 0.0
            hd = st["hd0"] + ((hd1 if hd1 is not None else st["hd0"]) - st["hd0"]) * u
            self.x, self.y, self.hd, self.phase = st["x0"] + (x1 - st["x0"]) * u, st["y0"] + (y1 - st["y0"]) * u, hd, ph
            self.p.set(x=self.x, y=self.y, hd=hd, phase=ph, amp=max(0.0, amp), look=look)
        return up

    def reach(self, side, pts, lean=None, look=None, grip=None, palm=None):
        st = {}

        def up(u):
            if not st:
                st.update(l0=self.lean)
            tgt = None if pts is None else tuple(lerp_path(pts, u))
            kw = dict(hands={side: tgt})
            if lean is not None:
                self.lean = st["l0"] + (lean - st["l0"]) * u
                kw["lean"] = self.lean
            if look is not None:
                kw["look"] = look
            if grip is not None:
                kw["grip"] = {side: grip}
            if palm is not None:
                kw["palm"] = {side: palm}
            self.p.set(**kw)
        return up

    def body_names(self):
        return [n for n in self.p.names() if "glove" not in n]

    def show_body(self, a0, a1):
        names = self.body_names()

        def up(u):
            for n in names:
                self.sc.alpha[n] = a0 + (a1 - a0) * u
        return up


def W(rig, xyz, piece="body"):
    return tuple(float(v) for v in rig.world(xyz, piece))


def cached(fn):
    box_ = {}

    def f(u):
        k = round(float(u), 2)
        if k not in box_:
            if len(box_) > 60:
                box_.clear()
            box_[k] = fn(k)
        return box_[k]
    return f


def static(fn):
    box_ = {}

    def f(u):
        if "im" not in box_:
            box_["im"] = fn(1.0)
        return box_["im"]
    return f


def show_panel(sc, key, fn, rect=PANEL):
    sc.panel(key, fn, rect=rect, alpha=0.0)
    return sc.fade_panel(key, 0.0, 1.0)


# ============================================================================================ chapter 1: samples
SAW = (-1000.0, -30.0)
PLATE_AT = (-640.0, -230.0)
SIC_AT = (-390.0, -285.0)
TRAY_AT = (-400.0, -150.0)
BEAKER_AT = (-200.0, -280.0)
BATH = (90.0, -50.0)
OVEN = (780.0, 10.0)
DISH_AT = (380.0, -290.0)
REF_AT = (-355.0, -195.0)


@chapter("sop03_c1")
def c1():
    import models_track as MT
    sc = S.SOPScene("sop03_c1", TITLE)
    S.room(sc, -1700, 1400)
    saw = S.place(sc, "precision_saw", *SAW)
    bath = S.place(sc, "ultrasonic_bath", *BATH)
    oven = S.place(sc, "drying_oven", *OVEN)
    saw.set(specimen=0.0, slice=0.0)
    drop_pieces(saw, ("specimen", "slice"))
    bath.set(ripple=0.0)
    oven.set(warm=0.0)
    # the plate with its cubes, the tray, the SiC paper, the beaker of ethanol, the dish, the reference cube, wipes
    prop(sc, "plate", MD.build_plate(skip=("A1",)), T((*PLATE_AT, BH)))
    prop(sc, "tray", MD.cube_tray(), T((*TRAY_AT, BH)))
    prop(sc, "sic", MD.sic_paper(), T((*SIC_AT, BH)))
    prop(sc, "wipes", MD.wipes_box(), T((-180.0, 120.0, BH)))
    prop(sc, "dish", MD.al_dish(), T((*DISH_AT, BH)))
    prop(sc, "refcube", MD.ref_cube(), T((*REF_AT, BH)))
    bk = prop(sc, "beaker50", MD.beaker_small(), T((*BEAKER_AT, BH)))
    # the strip in the saw's vise and its cube (SOP 02's VC50: the blade in the y-z plane at x = bx)
    sp = MT.saw_points()
    bx, by, _ = sp["blade_centre"]
    g = MT._vc50(MT.VC50)
    sz0 = g["top"] + 5.0
    zc = sz0 + 5.0
    strip_at = T((bx - 1.0, by, zc))
    prop(sc, "strip", MD.plate_strip(), strip_at, parent=saw.group("arm"))
    prop(sc, "cutcube", MD.strip_cube(), strip_at, parent=saw.group("arm"))
    strip_names = names_of(sc, "strip") + names_of(sc, "cutcube")
    for n in strip_names:
        sc.alpha[n] = 0.0
    # cubes in the tray's wells (all but A1, which is cut on camera) and in the beaker later
    wells = {}
    for r in range(4):
        for c in range(5):
            lab = f"{'ABCD'[r]}{c + 1}"
            wells[lab] = (TRAY_AT[0] - 30 + 12 * c, TRAY_AT[1] - 18 + 12 * r, BH + 3.0)
    tray_cubes = []
    for lab, (x, y, z) in wells.items():
        nm = f"tc_{lab}"
        prop(sc, nm, MD.cube(remnant=0.4 if lab != "A1" else 0.4), T((x, y, z)))
        tray_cubes.append(nm)
    a1 = "tc_A1"
    for n in names_of(sc, a1):
        sc.alpha[n] = 0.0
    # cubes inside the beaker (shown once the tray is emptied into it)
    bcubes = []
    rng = np.random.default_rng(3)
    for i in range(20):
        a_, r_ = rng.uniform(0, 2 * math.pi), rng.uniform(0, 13)
        nm = f"bc_{i}"
        prop(sc, nm, MD.cube(), T((r_ * math.cos(a_), r_ * math.sin(a_), 1.5 + 5.2 * (i // 9))) @ R((0, 0, 1), rng.uniform(0, 90)),
             parent=bk)
        bcubes.append(nm)
    bc_names = [n for b in bcubes for n in names_of(sc, b)]
    for n in bc_names:
        sc.alpha[n] = 0.0
    dcubes = []
    for i in range(20):
        a_, r_ = rng.uniform(0, 2 * math.pi), rng.uniform(0, 17)
        nm = f"dc_{i}"
        prop(sc, nm, MD.cube(), T((DISH_AT[0] + r_ * math.cos(a_), DISH_AT[1] + r_ * math.sin(a_), BH + 0.4)) @
             R((0, 0, 1), rng.uniform(0, 90)), parent="dish")
        dcubes.append(nm)
    # dish cubes are given in world coordinates above: re-express them in the dish's frame
    for nm in dcubes:
        sc.gmat[nm] = np.linalg.inv(sc.world("dish")) @ sc.gmat[nm]
    dc_names = [n for b in dcubes for n in names_of(sc, b)]
    for n in dc_names:
        sc.alpha[n] = 0.0
    tw = Tool(sc, "tweezers", MD.tweezers())
    tw.put((-300.0, -330.0, BH + 1.1), 30.0, 0.0, hand=False)
    op = Op(sc, "op", x=-150.0, y=-650.0)
    tw.op = op
    au = audit_for(sc, allow=[("tc_*", "tray/*"), ("bc_*", "beaker50/*"), ("bc_*", "bc_*"), ("dc_*", "dish/*"),
                              ("dc_*", "dc_*"), ("strip/*", "precision_saw:arm*"), ("cutcube/*", "strip/*"),
                              ("cutcube/*", "precision_saw:*"), ("tweezers/*", "tc_*"), ("tweezers/*", "sic/*"),
                              ("tc_*", "sic/*"), ("op/*glove*", "tweezers/*"), ("beaker50/*", "ultrasonic_bath:basket*"),
                              ("beaker50/*", "ultrasonic_bath:water*"), ("op/*glove*", "beaker50/*"),
                              ("op/*glove*", "ultrasonic_bath:lid*"), ("ultrasonic_bath:lid*", "ultrasonic_bath:body*"),
                              ("op/*glove*", "drying_oven:door*"), ("op/*glove*", "dish/*"),
                              ("dish/*", "drying_oven:grid*"), ("op/*glove*", "drying_oven:body*"),
                              ("op/*glove*", "ultrasonic_bath:body*"), ("refcube/*", "*"),
                              ("ultrasonic_bath:basket*", "ultrasonic_bath:water*")])

    # ------------------------------------------------------------------------------------------- the plate
    sc.card(TITLE, ["Samples: cubes cut from the plate, cleaned, dried", "A wrought 6063 reference cube with every batch"],
            seconds=3.0, label="Samples", note="Draft SOP 03 (thermo-calc-measurements/sops). Set-up: DAL #144.")
    cam_hold(sc, S.look((-250.0, 0.0, BH + 250.0), 4300.0, -12.0, 14.0))
    plate_w = (PLATE_AT[0], PLATE_AT[1], BH + 22.0)
    sc.step("Samples", "Cubes printed on the P1 plate | 5 x 5 x 5 mm (#144), or 10 mm", 3.5, hold=1.0,
            cam_to=S.look((-500.0, -150.0, BH + 120.0), 1500.0, -18.0, 30.0),
            labels=[("P1 build plate, 4 x 5 cubes", plate_w, (0.20, 0.30))])
    sc.step("Samples", "Each cube keeps its plate position | A1 to D5", 4.0, hold=1.5,
            update=show_panel(sc, "plate", static(P.plate_map)),
            cam_to=S.look(plate_w, 520.0, -10.0, 48.0),
            labels=[("5 mm cube on 1.5 mm supports", (PLATE_AT[0] - 44.0, PLATE_AT[1] - 33.0, BH + 22.0), (0.22, 0.62))])
    # ------------------------------------------------------------------------------------------- cut
    vise_w = W(saw, (bx + 3.0, by, zc))
    sc.step("Samples · cut", "Cut each cube off at its supports | SOP 02's low-speed saw", 3.5, hold=0.5,
            update=S.together(sc.fade_panel("plate", 1.0, 0.0), saw.move({"cover": (0.0, 1.0)}),
                              fade(sc, strip_names, 0.0, 1.0)),
            cam_to=S.look(vise_w, 240.0, 52.0, 24.0),
            labels=[("strip of the plate, cube on its +x face", vise_w, (0.70, 0.30))])
    sc.step("Samples · cut", "Cover down; the arm lowers the strip | through the blade at its supports", 2.0, hold=0.2,
            update=saw.move({"cover": (1.0, 0.0)}))

    def drop_cube(u):
        if u > 0.82 and sc.parent.get("cutcube") is not None:
            attach(sc, "cutcube", None)
            st_drop["w0"] = sc.gmat["cutcube"].copy()
        if "w0" in st_drop:
            k = min(1.0, (u - 0.82) / 0.18)
            m = st_drop["w0"].copy()
            m[2, 3] -= 26.0 * k * k
            sc.gmat["cutcube"] = m
    st_drop = {}
    sc.step("Samples · cut", "Diamond blade, oil-cooled | the cube drops into the tray below", 5.0, hold=0.8,
            update=S.together(saw.move({"wheel": (0.0, 1.0), "arm": (0.0, 1.0), "~cover": (0.0, 0.9)}), drop_cube),
            cam_to=S.look(vise_w, 230.0, 62.0, 20.0))
    saw.set(**{"~cover": 0.0})
    for n in names_of(sc, "cutcube"):
        sc.alpha[n] = 0.0
    saw.set(arm=0.0, wheel=0.0)
    for n in strip_names:
        sc.alpha[n] = 0.0
    # ------------------------------------------------------------------------------------------- label
    tray_w = (TRAY_AT[0], TRAY_AT[1], BH + 8.0)
    sc.step("Samples · label", "Into a tray, one well per plate position | labelled A1 to D5", 3.5, hold=1.2,
            update=fade(sc, names_of(sc, a1), 0.0, 1.0),
            cam_to=S.look(tray_w, 330.0, -20.0, 55.0),
            labels=[("A1", wells["A1"], (0.30, 0.78)), ("D5", wells["D5"], (0.72, 0.22))])
    # ------------------------------------------------------------------------------------------- supports off
    op_w = (-470.0, -610.0)
    sc.step("Cleaning", "Then clean them | supports off, ethanol, dry", 2.5, hold=0.3,
            update=op.walk(op_w[0], op_w[1], 0.0, look=SIC_AT + (BH,)),
            cam_to=S.look((-420.0, -300.0, BH + 200.0), 1500.0, 50.0, 26.0))
    a1w = np.array(wells["A1"])
    sic_c = np.array([SIC_AT[0], SIC_AT[1], BH + 5.4])
    grab = a1w + (0, 0, 2.5)
    tw_park = (-300.0, -330.0, BH + 1.1)
    sc.step("Cleaning", "Tweezers take cube A1", 3.0, hold=0.2,
            update=S.together(op.reach("r", [op.p.hand_point("r"), (-330, -400, BH + 120)], lean=14.0,
                                       look=tuple(a1w)),
                              tw.path([tw_park, tw_park + np.array([0, 0, 40.0]), grab + (0, 0, 30.0), grab],
                                      yaw0=30.0, yaw1=60.0, pitch0=0.0, pitch1=35.0)),
            cam_to=S.look((-390.0, -230.0, BH + 20.0), 420.0, 40.0, 34.0))
    tw.carry = a1
    scrub = [sic_c + (0, 0, 2.5) + np.array([8 * math.cos(t), 6 * math.sin(2 * t), 0.0]) for t in
             np.linspace(0, 4 * math.pi, 17)]
    stubs = [n for n in names_of(sc, a1) if "d3_cube_cut" in n]
    sc.step("Cleaning · supports", "Grind off the support remnants | on 320-grit SiC paper", 5.0, hold=0.6,
            update=S.together(tw.path([grab, grab + (0, 0, 25.0), sic_c + (0, 0, 2.5) + (0, 0, 15.0)] + scrub,
                                      yaw1=60.0, pitch1=35.0),
                              lambda u: [sc.alpha.__setitem__(n, 1.0 - max(0.0, (u - 0.6) / 0.4)) for n in stubs]),
            cam_to=S.look(tuple(sic_c), 260.0, 30.0, 30.0),
            labels=[("320-grit SiC paper", tuple(sic_c + (40.0, -30.0, 0.0)), (0.75, 0.75))])
    # ------------------------------------------------------------------------------------------- ultrasonic
    bkw = np.array([BEAKER_AT[0], BEAKER_AT[1], BH])
    into = bkw + (0, 0, 40.0)
    sc.step("Cleaning · ultrasonic", "All cubes into a 50 mL beaker of ethanol", 3.5, hold=0.6,
            update=S.together(tw.path([sic_c + (0, 0, 2.5) + scrub[-1] - scrub[0], sic_c + (0, 0, 40.0), into + (0, 0, 30),
                                       into], yaw1=60.0, pitch1=50.0),
                              fade(sc, [n for nm in tray_cubes if nm != a1 for n in names_of(sc, nm)], 1.0, 0.0),
                              fade(sc, bc_names, 0.0, 1.0)),
            cam_to=S.look(tuple(bkw + (0, 0, 40.0)), 520.0, 20.0, 34.0),
            labels=[("50 mL beaker, ethanol", tuple(bkw + (21.0, 0.0, 40.0)), (0.75, 0.40))])
    for n in names_of(sc, a1):
        sc.alpha[n] = 0.0
    tw.carry = None
    tw.put(tw_park, 30.0, 0.0, hand=False)
    op.p.set(hands={"r": None})
    bp = MD.bath_points()
    knob = W(bath, bp["lid_knob"])
    sc.step("Cleaning · ultrasonic", "Lid off the Branson CPX2800H | 2.8 L, 40 kHz", 3.5, hold=0.3,
            update=S.together(op.walk(BATH[0] - 120.0, -610.0, 0.0, look=knob)),
            cam_to=S.look((BATH[0], BATH[1] - 40.0, BH + 160.0), 1250.0, 55.0, 36.0),
            labels=[("Branson CPX2800H", W(bath, (168.0, -152.0, 150.0)), (0.80, 0.30))])
    lid_side = np.array(knob) + (0, 0, 0)
    sc.step("Cleaning · ultrasonic", "", 2.5, hold=0.0,
            update=S.together(op.reach("r", [op.p.hand_point("r"), knob + np.array([0, 0, 40.0]), knob + np.array([0, 0, 12.0])],
                                       lean=10.0, look=knob),
                              lambda u: None))
    sc.substeps[-1]["caption"] = "Lid off the Branson CPX2800H | 2.8 L, 40 kHz"
    # carry the lid off to the right, set it down on the bench
    lid_rest = W(bath, (168.0 + 150.0, 0.0, -186.0), "body")

    def lid_hand(u):
        return np.array(sc.world(bath.group("lid")) @ np.r_[0.0, MD._cpx(MD.BATH)["tcy"], MD.BATH["deck"] + 24.0, 1.0])[:3]
    sc.step("Cleaning · ultrasonic", "Lid off the Branson CPX2800H | 2.8 L, 40 kHz", 3.0, hold=0.2,
            update=S.together(bath.move({"lid": (0.0, 1.0)}),
                              lambda u: op.p.set(hands={"r": tuple(lid_hand(u))}, look=tuple(lid_hand(u)))))
    sc.substeps[-1]["caption"] = "Lid off the Branson CPX2800H | 2.8 L, 40 kHz"
    # the beaker into the basket
    op.p.set(hands={"r": None})
    bas_in = np.array(W(bath, (0.0, MD._cpx(MD.BATH)["tcy"], MD.BATH["deck"] - MD.BATH["tank_d"] + 11.2)))
    grip_b = bkw + (0, -24.0, 40.0)
    sc.step("Cleaning · ultrasonic", "The beaker into the basket | water outside to the ethanol's level", 2.5, hold=0.0,
            update=S.together(op.walk(BEAKER_AT[0] + 60.0, -610.0, 0.0, look=tuple(bkw)),
                              op.reach("r", [op.p.hand_point("r"), grip_b + (0, -20, 30), grip_b], lean=12.0)))
    op.p.hold("r", bk)
    carry_up = np.array(op.p.hand_point("r"))
    sc.step("Cleaning · ultrasonic", "The beaker into the basket | water outside to the ethanol's level", 4.0, hold=0.3,
            update=S.together(op.walk(BATH[0] - 110.0, -610.0, 0.0, look=tuple(bas_in)),
                              op.reach("r", [carry_up, carry_up + (0, 0, 160.0),
                                             bas_in + (0, -24.0, 40.0) + (0, 0, 120.0), bas_in + (0, -24.0, 40.0)],
                                       lean=16.0)),
            cam_to=S.look(tuple(bas_in + (0, 0, 60.0)), 950.0, 55.0, 42.0))
    op.p.let_go("r", parent=bath.group("basket"))
    sc.step("Cleaning · ultrasonic", "Lid on, start: 5 min | the tank water cavitates at 40 kHz", 3.0, hold=0.2,
            update=S.together(bath.move({"lid": (1.0, 0.0)}),
                              lambda u: op.p.set(hands={"r": tuple(lid_hand(u))}, look=tuple(lid_hand(u)))))
    panel_w = W(bath, bp["panel"])
    sc.step("Cleaning · ultrasonic", "Lid on, start: 5 min | the tank water cavitates at 40 kHz", 4.5, hold=0.5,
            update=S.together(op.reach("r", [op.p.hand_point("r"), np.array(panel_w) + (0, -30, 30), np.array(panel_w) + (0, -12, 6)],
                                       lean=8.0, look=panel_w),
                              bath.move({"ripple": (0.0, 1.0), "~lid": (0.0, 1.0)}),
                              gauge(sc, [("sonicate", lambda u: f"40 kHz  {int(5 - 5 * u)}:{int((60 * (5 - 5 * u)) % 60):02d}")])),
            cam_to=S.look(tuple(bas_in + (0, 0, 80.0)), 800.0, 60.0, 40.0))
    # ------------------------------------------------------------------------------------------- dry
    sc.step("Cleaning · dry", "Lid off, the beaker out", 3.0, hold=0.0,
            update=S.together(bath.move({"ripple": (1.0, 0.0), "~lid": (1.0, 0.0), "lid": (0.0, 1.0)}),
                              gauge(sc, []), lambda u: op.p.set(hands={"r": tuple(lid_hand(u))}, look=tuple(lid_hand(u)))))
    sc.gauges = []
    # the beaker out of the basket and over to the dish, carried by its side (the hand follows it)
    attach(sc, bk, None)
    b0 = sc.gmat[bk].copy()
    dish_w = (DISH_AT[0], DISH_AT[1], BH + 10.0)
    over_dish = T((DISH_AT[0] - 34.0, DISH_AT[1], BH + 42.0))
    lifted = b0.copy()
    lifted[2, 3] += 150.0
    tipped = over_dish @ R((0, 1, 0), 105.0, pivot=(21.0, 0.0, 60.0))
    side = np.array([0.0, -24.0, 40.0, 1.0])

    def carry_beaker(poses, walk_to=None):
        mv = S.path_mover(sc, bk, poses)
        wk = op.walk(*walk_to, 0.0) if walk_to else None

        def up(u):
            mv(u)
            if wk is not None:
                wk(u)
            op.p.set(hands={"r": tuple((sc.gmat[bk] @ side)[:3])}, look=tuple(sc.gmat[bk][:3, 3]))
        return up
    sc.step("Cleaning · dry", "Lid off, the beaker out", 3.0, hold=0.0,
            update=carry_beaker([b0, lifted]))
    rest_l = sc.world(bath.group("lid"))
    sc.step("Cleaning · dry", "Cubes tipped into a 57 mm dish | the ethanol poured off", 4.0, hold=0.0,
            update=carry_beaker([lifted, T((DISH_AT[0] - 34.0, DISH_AT[1] - 60.0, BH + 160.0)), over_dish],
                                walk_to=(DISH_AT[0] - 160.0, -620.0)),
            cam_to=S.look(dish_w, 700.0, 45.0, 45.0))
    sc.step("Cleaning · dry", "Cubes tipped into a 57 mm dish | the ethanol poured off", 2.5, hold=0.2,
            update=S.together(carry_beaker([over_dish, tipped]), fade(sc, bc_names, 1.0, 0.0),
                              fade(sc, dc_names, 0.0, 1.0)),
            labels=[("57 mm aluminium dish", dish_w, (0.30, 0.30))])
    sc.step("Cleaning · dry", "Cubes tipped into a 57 mm dish | the ethanol poured off", 2.5, hold=0.4,
            update=carry_beaker([tipped, over_dish, T((DISH_AT[0] - 90.0, DISH_AT[1] + 30.0, BH))]))
    op.p.set(hands={"r": None})
    op_pts = MD.oven_points()
    handle = W(oven, op_pts["handle"])
    sc.step("Cleaning · dry", "Memmert UN30 drying oven | 32 L, door hinged on the right", 3.0, hold=0.2,
            update=S.together(op.walk(OVEN[0] - 380.0, -640.0, 0.0, look=handle),
                              op.reach("r", [op.p.hand_point("r"), np.array(handle) + (0, -40, 0), handle], lean=4.0)),
            cam_to=S.look((OVEN[0] - 100.0, -150.0, BH + 300.0), 2150.0, -14.0, 42.0),
            labels=[("Memmert UN30", W(oven, (292.0, -217.0, 600.0)), (0.80, 0.25))])
    hinge = np.array(W(oven, (MD.OVEN["W"] / 2, -MD.OVEN["D"] / 2, 0.0)))

    def handle_at(u):
        return np.array(sc.world(oven.group("door")) @ np.r_[op_pts["handle"][0], op_pts["handle"][1],
                                                            op_pts["handle"][2], 1.0])[:3]
    sc.step("Cleaning · dry", "Memmert UN30 drying oven | 32 L, door hinged on the right", 3.0, hold=0.2,
            update=S.together(oven.move({"door": (0.0, 0.62)}),
                              lambda u: op.p.set(hands={"r": tuple(handle_at(u))})))
    # carry the dish to the grid
    grid_w = np.array(W(oven, op_pts["grid"]))
    op.p.set(hands={"r": None})
    dish_grip = np.array(dish_w) + (0, -30.0, 6.0)
    sc.step("Cleaning · dry", "The dish onto the grid", 2.5, hold=0.0,
            update=S.together(op.walk(DISH_AT[0] - 10.0, -620.0, 0.0, look=dish_w),
                              op.reach("r", [op.p.hand_point("r"), dish_grip + (0, 0, 40), dish_grip], lean=14.0)),
            cam_to=S.look((OVEN[0] - 150.0, -170.0, BH + 260.0), 1800.0, -10.0, 45.0))
    op.p.hold("r", "dish")
    h0 = np.array(op.p.hand_point("r"))
    dst = grid_w + (0, -30.0, 6.0) + (0, -60.0, 0)
    sc.step("Cleaning · dry", "The dish onto the grid", 4.0, hold=0.2,
            update=S.together(op.walk(OVEN[0] - 200.0, -640.0, 0.0, look=tuple(grid_w)),
                              op.reach("r", [h0, h0 + (0, 0, 150.0), dst + (0, -120, 30.0), dst], lean=18.0)))
    op.p.let_go("r", parent=oven.group("grid"))
    sc.step("Cleaning · dry", "Door shut; 60 C for 30 min", 3.0, hold=0.2,
            update=S.together(op.reach("r", [op.p.hand_point("r"), dst + (0, -200, 20)], lean=6.0),
                              lambda u: None),
            cam_to=S.look((OVEN[0] - 60.0, -150.0, BH + 330.0), 2000.0, -10.0, 42.0))
    sc.step("Cleaning · dry", "Door shut; 60 C for 30 min", 3.0, hold=0.2,
            update=S.together(oven.move({"door": (0.62, 0.0)}),
                              lambda u: op.p.set(hands={"r": tuple(handle_at(u))})))
    knob = W(oven, op_pts["knob"])
    sc.step("Cleaning · dry", "Door shut; 60 C for 30 min | set on the turn-push knob", 4.0, hold=0.8,
            update=S.together(op.reach("r", [op.p.hand_point("r"), np.array(knob) + (0, -40, 0), knob], lean=2.0,
                                       look=knob),
                              oven.move({"warm": (0.0, 1.0)}),
                              gauge(sc, [("oven", lambda u: f"{20 + 40 * u:4.1f} C"),
                                         ("timer", lambda u: f"{int(30 - 30 * u):02d}:00")])),
            cam_to=S.look(knob, 950.0, 38.0, 18.0))
    sc.gauges = []
    # ------------------------------------------------------------------------------------------- reference
    ref_w = (REF_AT[0], REF_AT[1], BH + 2.5)
    op.p.set(hands={"r": None})
    sc.step("Samples · reference", "A wrought 6063 cube, same size | measured with every batch", 4.0, hold=1.5,
            update=S.together(op.walk(-300.0, -640.0, 0.0), gauge(sc, [])),
            cam_to=S.look(ref_w, 300.0, -25.0, 40.0),
            labels=[("6063 reference cube, 5 mm", ref_w, (0.30, 0.30))])
    sc.save()
    au.save()


# ============================================================================================ the balance station
BAL = (0.0, -30.0)
WATER_BTL = (-430.0, -250.0)
DROPPER = (-340.0, -300.0)
THERMO = (-300.0, -160.0)
DRY_DISH = (-250.0, -250.0)
BRUSH_AT = (230.0, -300.0)
PYC = (560.0, 40.0)
OP_BAL = (-300.0, -590.0)


def balance_station(sc, water=True):
    S.room(sc, -1300, 1300)
    bal = S.place(sc, "density_balance", BAL[0], BAL[1])
    bal.set(grid_pan=1.0, water=1.0 if water else 0.0, bubbles=0.0)
    drop_pieces(bal, ("grid_pan",))
    pyc = S.place(sc, "he_pycnometer", *PYC, rot_deg=-15.0)
    prop(sc, "water_btl", MD.water_bottle(), T((*WATER_BTL, BH)))
    prop(sc, "dropper", MD.dropper_bottle(), T((*DROPPER, BH)))
    prop(sc, "thermo_dig", MD.thermometer_digital(), T((*THERMO, BH)) @ R((0, 0, 1), 20.0))
    prop(sc, "wipes", MD.wipes_box(), T((380.0, -230.0, BH)) @ R((0, 0, 1), -10.0))
    prop(sc, "dish", MD.al_dish(), T((*DRY_DISH, BH)))
    cubes = []
    for i, (dx, dy) in enumerate([(-8, -6), (6, -9), (9, 7), (-6, 9), (0, 0), (-14, 2), (13, -1)]):
        nm = f"dc_{i}"
        prop(sc, nm, MD.cube(), T((DRY_DISH[0] + dx, DRY_DISH[1] + dy, BH + 0.4)) @ R((0, 0, 1), 17.0 * i))
        cubes.append(nm)
    prop(sc, "refcube", MD.ref_cube(), T((DRY_DISH[0] + 40.0, DRY_DISH[1] - 22.0, BH)))
    br = Tool(sc, "brush", MD.brush(), grip_x=95.0)
    br.put((BRUSH_AT[0], BRUSH_AT[1], BH + 2.7), 160.0, 0.0, hand=False)
    tw = Tool(sc, "tweezers", MD.tweezers())
    tw.put((BRUSH_AT[0] - 20.0, BRUSH_AT[1] - 40.0, BH + 1.1), 150.0, 0.0, hand=False)
    op = Op(sc, "op", x=OP_BAL[0], y=OP_BAL[1], hd=0.0)
    return bal, pyc, tw, br, op, cubes


def bp_world(bal, key):
    return np.array(W(bal, MD.balance_points()[key]))


def door_grip(bal, side="door_left"):
    p = MD.XPR
    g = MD._xpr(p)
    return np.array(W(bal, (-g["hw"] - 8.0, g["yf"] + 22.0, p["base_h"] + 22.0), side))


def top_grip(bal):
    p = MD.XPR
    g = MD._xpr(p)
    return np.array(W(bal, (0.0, g["yf"] + 15.0, p["Hcap"] + 2.0), "top_door"))


def follow(op, fn):
    """update(u): the right hand on the point fn(u) (world), e.g. a door's grip as the door slides."""
    def up(u):
        op.p.set(hands={"r": tuple(fn(u))})
    return up


def carry(sc, op, group, poses, grip, walk=None, look=None):
    """update(u): `group` through 4x4 poses, the right hand on its point `grip` (its own frame)."""
    mv = S.path_mover(sc, group, poses)
    g = np.r_[np.asarray(grip, float), 1.0]

    def up(u):
        mv(u)
        if walk is not None:
            walk(u)
        op.p.set(hands={"r": tuple((sc.gmat[group] @ g)[:3])}, look=look)
    return up


def balance_allow():
    return [("density_balance:kit*", "density_balance:*"), ("density_balance:bracket*", "density_balance:*"),
            ("density_balance:holder*", "density_balance:*"), ("density_balance:beaker*", "density_balance:*"),
            ("density_balance:water*", "density_balance:*"), ("density_balance:thermo*", "density_balance:*"),
            ("density_balance:bubbles*", "density_balance:*"), ("density_balance:door*", "density_balance:*"),
            ("density_balance:top_door*", "density_balance:*"),
            ("op/*glove*", "density_balance:door*"), ("op/*glove*", "density_balance:top_door*"),
            ("op/*glove*", "density_balance:terminal*"),
            ("op/*glove*", "tweezers/*"), ("op/*glove*", "brush/*"), ("op/*glove*", "dropper/*"),
            ("op/*glove*", "water_btl/*"), ("op/*glove*", "thermo_dig/*"),
            ("dc_*", "dish/*"), ("dc_*", "dc_*"), ("tweezers/*", "dc_*"), ("dc_*", "density_balance:*"),
            ("cbub/*", "*"), ("tweezers/*", "density_balance:water*"), ("brush/*", "density_balance:water*"),
            ("brush/*", "density_balance:bubbles*"), ("brush/*", "dc_*"), ("refcube/*", "*"),
            ("thermo_dig/*", "water_btl/*"), ("drop/*", "*"), ("stream/*", "*"),
            ("he_pycnometer:cup*", "he_pycnometer:*"), ("he_pycnometer:cap*", "he_pycnometer:*")]


# ============================================================================================ chapter 2: set-up
@chapter("sop03_c2")
def c2():
    import pyvista as pv
    sc = S.SOPScene("sop03_c2", TITLE)
    bal, pyc, tw, br, op, cubes = balance_station(sc, water=False)
    au = audit_for(sc, allow=balance_allow())
    p, g = MD.XPR, MD._xpr(MD.XPR)
    sc.card("Archimedes (ASTM B962-type)", ["The balance and its density kit, the water, its temperature, the tare"],
            seconds=3.0, label="Archimedes")
    cam_hold(sc, S.look((-50.0, -60.0, BH + 180.0), 3000.0, -12.0, 15.0))
    top_w = W(bal, (g["hw"], g["yf"], 230.0))
    sc.step("Archimedes · balance", "An analytical balance with a density kit | 0.1 mg or better", 3.5, hold=1.0,
            cam_to=S.look((0.0, -90.0, BH + 140.0), 1100.0, 38.0, 22.0),
            labels=[("Mettler Toledo XPR225DR", top_w, (0.80, 0.22))])
    sc.step("Archimedes · balance", "Use 0.01 mg for 5 mm cubes | each weighs only ~0.33 g", 4.0, hold=1.2,
            labels=[("XPR225DR: 0.01 mg (to 121 g)", top_w, (0.80, 0.22)),
                    ("density kit 30460852", W(bal, (0.0, g["py"], p["arm_z"] + 10)), (0.80, 0.45))])
    kit_c = W(bal, (0.0, g["py"], 100.0))
    sc.step("Archimedes · kit", "The beaker stands on a plate off the pan | not weighed", 4.0, hold=1.0,
            update=bal.move({"~door_right": (0.0, 1.0)}),
            cam_to=S.look(kit_c, 520.0, 48.0, 20.0),
            labels=[("support plate + beaker pan", W(bal, (40.0, g["py"] - 30.0, g["kit_z0"] + 6.0)), (0.80, 0.72)),
                    ("80 mm beaker", W(bal, (40.0, g["py"], 95.0)), (0.80, 0.52))])
    sc.step("Archimedes · kit", "The bracket hangs on the pan suspension | weighed: holder, basket, small pans", 4.5,
            hold=1.2,
            labels=[("bracket (weighed)", W(bal, (-40.0, g["py"] + 8.0, 120.0)), (0.22, 0.25)),
                    ("basket, immersed", W(bal, (p["basket_d"] / 2, g["py"], p["basket_z"])), (0.80, 0.66)),
                    ("small pan: the weighing in air", W(bal, (p["bpan_x"], g["py"] + p["bpan_dy"], 46.0)),
                     (0.80, 0.84))])
    # ------------------------------------------------------------------------------------------- water
    btl = np.array([WATER_BTL[0], WATER_BTL[1], BH])
    drp = np.array([DROPPER[0], DROPPER[1], BH])
    sc.step("Archimedes · water", "Distilled water | one drop of wetting agent per 250 mL", 3.0, hold=0.2,
            update=S.together(bal.move({"~door_right": (1.0, 0.0)}),
                              op.walk(-470.0, -610.0, 0.0, look=tuple(btl + (0, 0, 140)))),
            cam_to=S.look(tuple(btl + (60.0, 0.0, 110.0)), 800.0, 45.0, 30.0),
            labels=[("250 mL distilled water", tuple(btl + (35.0, 0.0, 80.0)), (0.78, 0.40)),
                    ("wetting agent", tuple(drp + (15.0, 0.0, 70.0)), (0.78, 0.62))])
    names_cap = [n for n in names_of(sc, "water_btl") if "d3_cap_blue" in n]
    d0 = sc.gmat["dropper"].copy()
    d_over = T(btl + (0.0, 0.0, 150.0)) @ R((0, 1, 0), 180.0) @ T((0.0, 0.0, -88.0))
    d_mid = T(drp + (0.0, 0.0, 120.0))
    dgrip = (0.0, -16.0, 40.0)
    sc.step("Archimedes · water", "Distilled water | one drop of wetting agent per 250 mL", 3.5, hold=0.0,
            update=S.together(fade(sc, names_cap, 1.0, 0.0),
                              carry(sc, op, "dropper", [d0, d_mid, d_over], dgrip, look=tuple(btl + (0, 0, 120)))))
    sc.add("drop/drop", pv.Sphere(radius=1.6, center=(0, 0, 0)), (0.85, 0.92, 0.97), "drop", opacity=0.8)
    tipw = np.array(sc.gmat["dropper"] @ np.r_[0.0, 0.0, 88.0, 1.0])[:3]

    def fall(u):
        sc.gmat["drop"] = T(tipw + (0, 0, -(tipw[2] - (BH + 102.0)) * u * u))
        sc.alpha["drop/drop"] = 1.0 if u < 0.97 else 0.0
    sc.step("Archimedes · water", "Distilled water | one drop of wetting agent per 250 mL", 1.6, hold=0.6,
            update=fall, cam_to=S.look(tuple(btl + (0.0, 0.0, 150.0)), 520.0, 45.0, 22.0))
    sc.alpha["drop/drop"] = 0.0
    sc.step("Archimedes · water", "Distilled water | one drop of wetting agent per 250 mL", 2.5, hold=0.0,
            update=carry(sc, op, "dropper", [d_over, d_mid, d0], dgrip))
    op.p.set(hands={"r": None})
    # temperature: the digital thermometer's probe in the water, 0.1 C
    th0 = sc.gmat["thermo_dig"].copy()
    probe_in = btl + (0.0, 0.0, 95.0)
    th_in = T(probe_in) @ R((0, 1, 0), 90.0) @ T((-110.0, 0.0, -8.0))
    th_up = th0.copy()
    th_up[2, 3] += 140.0
    tgrip = (-35.0, 0.0, 22.0)
    sc.step("Archimedes · temperature", "Its temperature, to 0.1 C | a digital probe in the water", 4.0, hold=0.4,
            update=S.together(carry(sc, op, "thermo_dig", [th0, th_up, th_in], tgrip),
                              gauge(sc, [("water", lambda u: "21.4 C" if u > 0.8 else "--.- C")])),
            cam_to=S.look(tuple(btl + (0.0, 0.0, 150.0)), 650.0, 45.0, 24.0),
            labels=[("probe thermometer, 0.1 C", tuple(probe_in + (0, 0, 150.0)), (0.78, 0.30))])
    sc.step("Archimedes · temperature", "21.4 C -> water 0.99791 g/cm3 | the script's Tanaka (2001) formula", 3.0,
            hold=1.0, update=carry(sc, op, "thermo_dig", [th_in, th_up, th0], tgrip))
    # fill the beaker through the open top door
    tg = top_grip(bal)
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 3.0,
            hold=0.0, update=S.together(op.walk(-300.0, -600.0, 0.0, look=tuple(tg)),
                                        op.reach("r", [op.p.hand_point("r"), tg + (0, -40, 30), tg], lean=10.0)),
            cam_to=S.look(tuple(np.array(kit_c) + (0, 0, 120.0)), 1000.0, 45.0, 34.0))
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 2.0,
            hold=0.0, update=S.together(bal.move({"top_door": (0.0, 1.0)}), follow(op, lambda u: top_grip(bal))))
    b0 = sc.gmat["water_btl"].copy()
    rim = np.array(W(bal, (-20.0, g["py"] - 10.0, p["Hcap"] + 70.0)))
    b_up = T((WATER_BTL[0], WATER_BTL[1], BH + 200.0))
    b_over = T(rim)
    b_tilt = T(rim) @ R((0, 1, 0), 112.0, pivot=(17.0, 0.0, 140.0))
    bgrip = (0.0, -36.0, 70.0)
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 3.5,
            hold=0.0, update=carry(sc, op, "water_btl", [b0, b_up, b_over], bgrip, look=tuple(kit_c)))
    spout = np.array(b_tilt @ np.r_[17.0, 0.0, 146.0, 1.0])[:3]
    top_w = W(bal, (0.0, g["py"], g["water_top"]))
    stream = pv.Cylinder(center=(0, 0, 0.5), direction=(0, 0, 1), radius=2.2, height=1.0, resolution=16)
    sc.add("stream/stream", stream, (0.64, 0.80, 0.92), "stream", opacity=0.55)
    sc.alpha["stream/stream"] = 0.0
    ln = float(spout[2] - top_w[2])

    def pour(u):
        a = min(1.0, u / 0.25)
        k = max(0.0, min(1.0, (u - 0.25) / 0.6))
        sc.gmat["water_btl"] = S.blend(b_over, b_tilt, S.ease(a)) if u < 0.92 else S.blend(b_tilt, b_over,
                                                                                         S.ease((u - 0.92) / 0.08))
        op.p.set(hands={"r": tuple((sc.gmat["water_btl"] @ np.r_[bgrip, 1.0])[:3])})
        on = 0.25 < u < 0.9
        sc.alpha["stream/stream"] = 1.0 if on else 0.0
        top = np.array(sc.gmat["water_btl"] @ np.r_[17.0, 0.0, 146.0, 1.0])[:3]
        sc.gmat["stream"] = T((top[0], top[1], top_w[2] - 20.0)) @ np.diag([1.0, 1.0, max(ln + 20.0, 1.0), 1.0])
        bal.set(water=k)
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 5.0,
            hold=0.3, update=pour, cam_to=S.look(tuple(np.array(kit_c) + (0, 0, 60.0)), 800.0, 50.0, 32.0))
    sc.alpha["stream/stream"] = 0.0
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 3.0,
            hold=0.0, update=carry(sc, op, "water_btl", [b_over, b_up, b0], bgrip))
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 2.5,
            hold=0.2, update=S.together(op.reach("r", [op.p.hand_point("r"), top_grip(bal) + (0, 0, 20)], lean=10.0)))
    sc.step("Archimedes · water", "Fill the beaker through the top door | >= 1 cm of water over the sample", 2.0,
            hold=0.2, update=S.together(bal.move({"top_door": (1.0, 0.0)}), follow(op, lambda u: top_grip(bal))))
    # bubbles on the basket: the left door, then a close-up of the fine brush
    bal.set(bubbles=1.0)
    gl = door_grip(bal)
    sc.step("Archimedes · bubbles", "Air bubbles on the basket | the left door open", 3.0, hold=0.2,
            update=op.reach("r", [op.p.hand_point("r"), gl + (0, -40, 0), gl], lean=6.0),
            cam_to=S.look(W(bal, (-40.0, g["py"] - 30.0, 120.0)), 900.0, 50.0, 28.0))
    sc.step("Archimedes · bubbles", "Air bubbles on the basket | the left door open", 2.5, hold=0.3,
            update=S.together(bal.move({"door_left": (0.0, 1.0)}), follow(op, lambda u: door_grip(bal))))
    # the close-up: the brush alone (the operator's hand is out of the frame)
    op.p.show(0.0)
    br.op = None
    bpt = np.array(W(bal, (0.0, g["py"] - 14.0, p["basket_z"] + 3.0)))
    axis = np.array([-0.5, 0.0, 0.866])                      # the tool's line in from the left door, 60 degrees
    cam_hold(sc, S.look(W(bal, (-10.0, g["py"] - 10.0, 80.0)), 280.0, 40.0, 16.0))
    br.put(bpt + 125.0 * axis, 180.0, 60.0, hand=False)
    sc.step("Archimedes · bubbles", "Brush them off with a fine brush", 2.5, hold=0.0,
            update=br.path([bpt + 125.0 * axis, bpt + 6.0 * axis], yaw1=180.0, pitch1=60.0, hand=False),
            labels=[("bubbles on the basket", W(bal, (14.0, g["py"] - 6.0, p["basket_z"] + 2.0)), (0.78, 0.70))])
    sweep = [bpt + 6.0 * axis] + [bpt + np.array([6 * math.cos(t), 6 * math.sin(t), 1.5]) for t in
                                  np.linspace(0, 2 * math.pi, 9)] + [bpt + 6.0 * axis]
    sc.step("Archimedes · bubbles", "Brush them off with a fine brush", 4.0, hold=0.4,
            update=S.together(br.path(sweep, yaw1=180.0, pitch1=60.0, hand=False), bal.move({"bubbles": (1.0, 0.0)})))
    sc.step("Archimedes · bubbles", "Brush them off with a fine brush", 2.0, hold=0.0,
            update=br.path([bpt + 6.0 * axis, bpt + 160.0 * axis], yaw1=180.0, pitch1=60.0, hand=False))
    br.put((BRUSH_AT[0], BRUSH_AT[1], BH + 2.7), 160.0, 0.0, hand=False)
    op.p.show(1.0)
    op.p.set(hands={"r": tuple(door_grip(bal))})
    cam_hold(sc, S.look(W(bal, (-40.0, g["py"] - 30.0, 120.0)), 900.0, 50.0, 28.0))
    sc.step("Archimedes · tare", "Door shut; tare with the basket in the water", 2.5, hold=0.0,
            update=S.together(bal.move({"door_left": (1.0, 0.0)}), follow(op, lambda u: door_grip(bal))))
    term = bp_world(bal, "terminal")
    sc.step("Archimedes · tare", "Door shut; tare with the basket in the water | reads 0.00000 g", 3.5, hold=1.5,
            update=S.together(op.reach("r", [op.p.hand_point("r"), term + (0, -30, 40), term + (0, 0, 10)], lean=10.0,
                                       look=tuple(term)),
                              gauge(sc, [("balance", lambda u: "0.00000 g" if u > 0.75 else "0.81642 g")])),
            cam_to=S.look(tuple(term + (0, 80, 60)), 800.0, 45.0, 38.0))
    sc.save()
    au.save()


# ============================================================================================ chapter 3: weighing
@chapter("sop03_c3")
def c3():
    import pyvista as pv
    sc = S.SOPScene("sop03_c3", TITLE)
    bal, pyc, tw, br, op, cubes = balance_station(sc, water=True)
    au = audit_for(sc, allow=balance_allow() + [("op/*glove*", "he_pycnometer:*")])
    p, g = MD.XPR, MD._xpr(MD.XPR)
    cube = cubes[4]                                  # cube A1, in the middle of the dish
    cw = np.array(sc.world(cube)[:3, 3])
    sc.card("Weighing: three times in air, three in water", ["Then the density, its uncertainty, the reference density"],
            seconds=3.0, label="Archimedes")
    cam_hold(sc, S.look((-50.0, -60.0, BH + 180.0), 2600.0, -12.0, 15.0))
    sc.gauges = [("balance", "0.00000 g")]
    gl = door_grip(bal)
    door_view = S.look(W(bal, (-40.0, g["py"] - 30.0, 110.0)), 950.0, 50.0, 28.0)
    sc.step("Archimedes · weighing", "Open the left door | cube A1 from the dish", 3.0, hold=0.0,
            update=op.reach("r", [op.p.hand_point("r"), gl + (0, -40, 0), gl], lean=6.0), cam_to=door_view)
    sc.step("Archimedes · weighing", "Open the left door | cube A1 from the dish", 2.5, hold=0.3,
            update=S.together(bal.move({"door_left": (0.0, 1.0)}), follow(op, lambda u: door_grip(bal))))
    # close-ups of the tweezers alone
    op.p.show(0.0)
    tw.op = None
    tpark = np.array(sc.world("tweezers")[:3, 3])
    grab = cw + (0, 0, 2.5)
    air = bp_world(bal, "air_pan") + (0, 0, 1.0)
    air_c = air + (0, 0, 2.5)
    door_in = np.array(W(bal, (-p["bpan_x"] - 70.0, g["py"] + p["bpan_dy"], 105.0)))
    cam_hold(sc, S.look(tuple(cw + (0, 0, 5.0)), 300.0, 30.0, 35.0))
    tw.put(grab + (0, 0, 40.0), 200.0, 40.0, hand=False)
    sc.step("Archimedes · in air", "Tweezers: cube A1 from the dish", 2.5, hold=0.0,
            update=tw.path([grab + (0, 0, 40.0), grab], yaw1=180.0, pitch1=30.0, hand=False))
    tw.carry = cube
    sc.step("Archimedes · in air", "Onto the bracket's small pan | through the left door", 4.0, hold=0.3,
            update=tw.path([grab, grab + (0, 0, 90.0), door_in + (-40.0, 0, 20.0), door_in, air_c + (0, 0, 10.0),
                            air_c], yaw1=180.0, pitch1=30.0, hand=False),
            cam_to=S.look(tuple(air + (10.0, 0, 12.0)), 300.0, 45.0, 22.0),
            labels=[("bracket's small pan", tuple(air), (0.78, 0.70))])
    tw.carry = None
    attach(sc, cube, bal.group("bracket"))
    sc.step("Archimedes · in air", "Onto the bracket's small pan | through the left door", 2.0, hold=0.0,
            update=tw.path([air_c, air_c + (0, 0, 20.0), door_in, door_in + (-90.0, 0, 40.0)], yaw1=180.0,
                           pitch1=30.0, hand=False))
    tw.put(tpark, 150.0, 0.0, hand=False)
    op.p.show(1.0)
    cam_hold(sc, door_view)
    sc.step("Archimedes · in air", "Door shut, read: 0.33412 g | three times, lifting it off between", 2.5, hold=0.0,
            update=S.together(bal.move({"door_left": (1.0, 0.0)}), follow(op, lambda u: door_grip(bal))))
    sc.panel("read", cached(P.readings), rect=PANEL, alpha=0.0, u=0.0)
    sc.step("Archimedes · in air", "Door shut, read: 0.33412 g | three times, lifting it off between", 4.0, hold=1.2,
            update=S.together(sc.fade_panel("read", 0.0, 1.0), sc.drive_panel("read", 0.0, 0.5),
                              gauge(sc, [("balance", lambda u: "0.33412 g" if u > 0.25 else "0.00000 g")])),
            cam_to=S.look(tuple(air + (0, 0, 40.0)), 650.0, 45.0, 26.0))
    sc.gauges = [("in air", "0.33412  0.33413  0.33411 g")]
    # into the water
    sc.step("Archimedes · in water", "Then into the basket, under the water", 2.5, hold=0.3,
            update=S.together(bal.move({"door_left": (0.0, 1.0)}), follow(op, lambda u: door_grip(bal))),
            cam_to=door_view)
    op.p.show(0.0)
    bas = np.array(W(bal, (0.0, g["py"] - 12.0, p["basket_z"] + 1.0)))
    bas_c = bas + (0, 0, 2.5)
    axis = np.array([-0.5, 0.0, 0.866])
    start = bas_c + 125.0 * axis
    cam_hold(sc, S.look(W(bal, (-20.0, g["py"] - 10.0, 80.0)), 330.0, 40.0, 18.0))
    tw.put(door_in + (-90.0, 0, 40.0), 180.0, 30.0, hand=False)
    sc.step("Archimedes · in water", "Then into the basket, under the water", 2.5, hold=0.0,
            update=tw.path([door_in + (-90.0, 0, 40.0), door_in, air_c + (0, 0, 10.0), air_c], yaw1=180.0,
                           pitch1=30.0, hand=False))
    attach(sc, cube, None)
    tw.carry = cube
    sc.step("Archimedes · in water", "Into the basket | at least 1 cm of water over it", 4.5, hold=0.4,
            update=tw.path([air_c, air_c + (0, 0, 60.0), start, bas_c + 30.0 * axis, bas_c], yaw1=180.0,
                           pitch1=60.0, hand=False),
            labels=[("holder basket, immersed", tuple(bas + (25.0, 0, 0)), (0.78, 0.70))])
    tw.carry = None
    attach(sc, cube, bal.group("holder"))
    cbub = []
    for i, (dx, dy, dz) in enumerate([(2.7, 0.6, 1.5), (-2.7, -1.2, 3.2), (0.8, 2.7, 4.0), (-1.0, -2.7, 1.2)]):
        nm = f"cbub/b{i}"
        sc.add(nm, pv.Sphere(radius=0.55, center=(dx, dy, dz)), (0.92, 0.95, 0.98), cube, opacity=0.7)
        cbub.append(nm)
    sc.step("Archimedes · in water", "Into the basket | at least 1 cm of water over it", 2.0, hold=0.0,
            update=tw.path([bas_c, bas_c + 160.0 * axis], yaw1=180.0, pitch1=60.0, hand=False))
    tw.put(tpark, 150.0, 0.0, hand=False)
    bpt = bas_c + (0, 0, 3.5)
    cam_hold(sc, S.look(tuple(bas_c + (0, 0, 8.0)), 210.0, 40.0, 14.0))
    br.put(bpt + 125.0 * axis, 180.0, 60.0, hand=False)
    sc.step("Archimedes · bubbles", "Bubbles on the cube: brush them off", 2.5, hold=0.0,
            update=br.path([bpt + 125.0 * axis, bpt + 4.0 * axis], yaw1=180.0, pitch1=60.0, hand=False))
    sweep = [bpt + 4.0 * axis] + [bpt + 4.0 * axis + np.array([0.0, 3.5 * math.sin(t), 2.5 * math.cos(t)]) for t in
                                  np.linspace(0, 2 * math.pi, 7)]
    sc.step("Archimedes · bubbles", "Bubbles on the cube: brush them off", 3.5, hold=0.3,
            update=S.together(br.path(sweep, yaw1=180.0, pitch1=60.0, hand=False), fade(sc, cbub, 1.0, 0.0)))
    sc.step("Archimedes · bubbles", "Bubbles on the cube: brush them off", 2.0, hold=0.0,
            update=br.path([sweep[-1], bpt + 160.0 * axis], yaw1=180.0, pitch1=60.0, hand=False))
    br.put((BRUSH_AT[0], BRUSH_AT[1], BH + 2.7), 160.0, 0.0, hand=False)
    op.p.show(1.0)
    cam_hold(sc, door_view)
    sc.step("Archimedes · in water", "Door shut, read: 0.20915 g | three times", 2.5, hold=0.0,
            update=S.together(bal.move({"door_left": (1.0, 0.0)}), follow(op, lambda u: door_grip(bal))))
    op.p.set(hands={"r": None})
    sc.step("Archimedes · in water", "Door shut, read: 0.20915 g | three times", 4.0, hold=1.2,
            update=S.together(sc.drive_panel("read", 0.5, 1.0), op.reach("r", [door_grip(bal), None], lean=0.0),
                              gauge(sc, [("in air", "0.33412  0.33413  0.33411 g"),
                                         ("in water", lambda u: "0.20915  0.20917  0.20914 g" if u > 0.3 else "...")])),
            cam_to=S.look(W(bal, (0.0, g["py"], 80.0)), 650.0, 45.0, 22.0))
    # ------------------------------------------------------------------------------------------- result
    sc.step("Archimedes · result", "density_porosity.py archimedes | 2.6660 g/cm3: 99.92 % of 2.668", 5.0, hold=2.0,
            update=S.together(sc.fade_panel("read", 1.0, 0.0), show_panel(sc, "res", static(P.result_panel))),
            cam_to=S.look((0.0, -100.0, BH + 130.0), 1100.0, 30.0, 22.0))
    sc.step("Archimedes · uncertainty", "+-0.1 % for a 5 mm cube at 0.1 mg | that is a good part's porosity", 4.5,
            hold=1.5, update=S.together(sc.fade_panel("res", 1.0, 0.0), show_panel(sc, "unc", static(P.uncertainty_panel))))
    sc.step("Archimedes · uncertainty", "Below 0.5 % porosity: 10 mm cubes | or a 0.01 mg balance", 4.0, hold=1.5)
    pyc_w = W(pyc, (0.0, MD.PYC["cap_y"], MD.PYC["H"] + 20.0))
    sc.step("Archimedes · reference density", "Best: He pycnometer, same powder | AccuPyc II 1345", 4.5, hold=1.2,
            update=S.together(sc.fade_panel("unc", 1.0, 0.0), show_panel(sc, "ref", static(P.refdens_panel)),
                              pyc.move({"cap": (0.0, 1.0)})),
            cam_to=S.look(pyc_w, 750.0, 35.0, 28.0),
            labels=[("He pycnometer: powder in a 10 cm3 cup", pyc_w, (0.22, 0.30))])
    sc.step("Archimedes · reference density", "Otherwise: Thermo-Calc's 20 C density | measured composition (SOP 05)",
            4.0, hold=1.2, update=pyc.move({"cap": (1.0, 0.0)}))
    sc.step("Archimedes · reference density", "Report which one you used", 2.5, hold=1.0)
    sc.step("Archimedes · time", "About 10 min per cube", 3.0, hold=1.0,
            update=sc.fade_panel("ref", 1.0, 0.0),
            cam_to=S.look((-80.0, -100.0, BH + 130.0), 1300.0, 25.0, 22.0))
    sc.step("Acceptance", "The 6063 reference reads >= 99.9 % | repeat weighings within 0.05 %", 5.0, hold=2.0,
            update=show_panel(sc, "acc", static(P.acceptance_panel)),
            cam_to=S.look((DRY_DISH[0] + 30.0, DRY_DISH[1] - 15.0, BH), 380.0, 30.0, 40.0),
            labels=[("6063 reference cube", (DRY_DISH[0] + 40.0, DRY_DISH[1] - 22.0, BH + 5.0), (0.25, 0.35))])
    sc.save()
    au.save()


# ============================================================================================ chapter 4: sections
@chapter("sop03_c4")
def c4():
    import pyvista as pv
    sc = S.SOPScene("sop03_c4", TITLE)
    S.room(sc, -1500, 1500)
    press = S.place(sc, "mount_press", -800.0, 20.0)
    pol = S.place(sc, "polisher", -150.0, 20.0)
    vhx = S.place(sc, "vhx", 700.0, 0.0)
    drop_pieces(vhx, ("carrier", "sample", "bar", "lift", "readout"), match=("turntable/r8c_steel",))
    pol.set(paper=0.0, cloth=1.0, glow=0.0, powder=0.0, alumina=0.0)
    # the cube and its XZ section plane, large on the bench in front
    cx, cy = 300.0, -260.0
    prop(sc, "secA", MD.cube(), T((cx - 0.02, cy, BH)))
    names_a = names_of(sc, "secA")
    plane = pv.Plane(center=(0, 0, 0), direction=(0, 1, 0), i_size=9.0, j_size=9.0)
    sc.add("cutplane/plane", plane, (0.15, 0.49, 0.88), "cutplane", opacity=0.35)
    sc.gmat["cutplane"] = T((cx, cy, BH + 2.5))
    sc.alpha["cutplane/plane"] = 0.0
    arrow = pv.Arrow(start=(0, 0, 0), direction=(0, 0, 1), scale=12.0, tip_length=0.25, tip_radius=0.08,
                     shaft_radius=0.025)
    sc.add("zarrow/arrow", arrow, (0.3, 0.3, 0.32), "zarrow")
    sc.gmat["zarrow"] = T((cx - 9.0, cy - 6.0, BH))
    # the mount, face up, on the VHX stage
    prop(sc, "mount", MD.section_mount(), T((0.0, -40.0, 232.0)), parent=vhx.group("turntable"))
    au = audit_for(sc, allow=[("mount/*", "vhx:turntable*"), ("mount/*", "vhx:table*"), ("vhx:table*", "vhx:turntable*"),
                              ("polisher:holder*", "polisher:cloth*"), ("polisher:holder*", "polisher:paper*"),
                              ("secA/*", "*"), ("cutplane/*", "*"), ("zarrow/*", "*")])
    sc.card("Sections: porosity, pore type and cracks", ["One cube per condition, cut along the build direction"],
            seconds=3.0, label="Sections")
    cam_hold(sc, S.look((0.0, 0.0, BH + 250.0), 4200.0, -12.0, 14.0))
    cube_w = (cx, cy, BH + 2.5)
    sc.step("Sections 1", "One cube per condition | sectioned parallel to the build direction (XZ)", 4.0, hold=0.5,
            cam_to=S.look(cube_w, 120.0, -30.0, 25.0),
            labels=[("build direction Z", (cx - 9.0, cy - 6.0, BH + 10.0), (0.25, 0.25))])
    sc.step("Sections 1", "One cube per condition | sectioned parallel to the build direction (XZ)", 3.0, hold=1.0,
            update=fade(sc, ["cutplane/plane"], 0.0, 1.0),
            labels=[("XZ plane", (cx + 4.5, cy, BH + 4.0), (0.75, 0.35)),
                    ("build direction Z", (cx - 9.0, cy - 6.0, BH + 10.0), (0.25, 0.25))])
    sc.step("Sections 1", "Hot-mounted, then polished as in SOP 02 | left unetched", 4.0, hold=0.5,
            update=S.together(fade(sc, ["cutplane/plane"], 1.0, 0.0), press.move({"closure": (0.0, 1.0)})),
            cam_to=S.look((-800.0, -50.0, BH + 350.0), 1300.0, -25.0, 18.0),
            labels=[("LECO MX400 press", (-800.0, -230.0, BH + 500.0), (0.25, 0.25))])
    sc.step("Sections 1", "Hot-mounted, then polished as in SOP 02 | left unetched", 3.0, hold=0.2,
            update=press.move({"closure": (1.0, 0.0)}))
    sc.step("Sections 1", "Polish to 1 um on the PX500 | no Keller's etch", 5.0, hold=0.5,
            update=pol.move({"head": (0.0, 1.0), "platen": (0.0, 1.0), "holder": (0.0, 1.0)}),
            cam_to=S.look((-150.0, -60.0, BH + 300.0), 1500.0, -25.0, 20.0),
            labels=[("LECO PX500", (-150.0 + 120.0, -330.0, BH + 300.0), (0.75, 0.25))])
    sc.step("Sections 1", "Polish to 1 um on the PX500 | no Keller's etch", 2.0, hold=0.2,
            update=pol.move({"head": (1.0, 0.0)}))
    stage_w = (700.0, -40.0, BH + 252.0)
    sc.step("Sections 2", "Stitch images at 50-100x | over the whole face", 4.0, hold=0.5,
            cam_to=S.look(stage_w, 900.0, -40.0, 22.0),
            labels=[("Keyence VHX-7000", (700.0 + 60.0, -40.0, BH + 450.0), (0.75, 0.22)),
                    ("mount, face up", stage_w, (0.25, 0.70))])
    sc.panel("tiles", cached(P.tiles_panel), rect=PANEL, alpha=0.0, u=0.0)
    sc.step("Sections 2", "Stitch images at 50-100x | 3 x 3 tiles in a serpentine", 6.0, hold=1.0,
            update=S.together(sc.fade_panel("tiles", 0.0, 1.0), sc.drive_panel("tiles", 0.0, 1.0)),
            cam_to=S.look(stage_w, 420.0, -55.0, 30.0))
    sc.step("Sections 3", "Porosity: Otsu threshold, pore area | Delesse: area fraction = volume fraction", 6.0,
            hold=2.0, update=S.together(sc.fade_panel("tiles", 1.0, 0.0), show_panel(sc, "otsu", static(P.otsu_panel))))
    sc.step("Sections 4", "Pore type: round (> ~0.8) = gas or keyhole | irregular, at tracks = lack of fusion", 6.0,
            hold=2.0, update=S.together(sc.fade_panel("otsu", 1.0, 0.0),
                                        show_panel(sc, "cls", static(lambda u: P.classes_panel(0.0)))))
    sc.step("Sections 5", "Cracks: traced length per area, mm/mm2 | only along build-direction grain boundaries",
            6.0, hold=2.0, update=S.together(sc.fade_panel("cls", 1.0, 0.0),
                                             show_panel(sc, "crk", static(P.cracks_panel))))
    sc.step("Sections 6", "About 1 h per batch of 8 sections | after polishing", 3.5, hold=1.0,
            update=sc.fade_panel("crk", 1.0, 0.0), cam_to=S.look(stage_w, 1300.0, -35.0, 20.0))
    sc.step("Acceptance", "Archimedes and image porosity agree | if not, look for open pores or bubbles", 6.0,
            hold=2.0, update=show_panel(sc, "agr", static(P.agreement_panel)))
    sc.save()
    au.save()


# ============================================================================================ chapter 5: notes
@chapter("sop03_c5")
def c5():
    sc = S.SOPScene("sop03_c5", TITLE)
    bal, pyc, tw, br, op, cubes = balance_station(sc, water=True)
    op.p.show(0.0)
    au = audit_for(sc, allow=balance_allow())
    p, g = MD.XPR, MD._xpr(MD.XPR)
    sc.card("Notes", ["Open surface porosity; combining tracks and cubes"], seconds=3.0, label="Notes")
    kit_c = W(bal, (0.0, g["py"], 90.0))
    cam_hold(sc, S.look(kit_c, 1100.0, -25.0, 20.0))
    sc.panel("open", cached(P.open_pore_panel), rect=PANEL, alpha=0.0, u=0.0)
    sc.step("Notes", "Open surface pores fill with water | Archimedes then reads high", 6.0, hold=1.5,
            update=S.together(sc.fade_panel("open", 0.0, 1.0), sc.drive_panel("open", 0.0, 1.0)),
            cam_to=S.look(kit_c, 420.0, -40.0, 18.0))
    sc.step("Notes", "If sections show them | coat the cube, or oil-impregnate it", 4.0, hold=1.5)
    sc.step("Notes", "Combine with SOP 02's tracks | tracks: keyhole and balling; cubes: lack of fusion", 6.0, hold=1.5,
            update=S.together(sc.fade_panel("open", 1.0, 0.0), show_panel(sc, "map", static(P.printability_panel))),
            cam_to=S.look(kit_c, 900.0, -20.0, 20.0))
    sc.step("Notes", "Crack density gives the hot-cracking axis", 4.0, hold=2.5,
            cam_to=S.look((0.0, -60.0, BH + 180.0), 2200.0, -15.0, 14.0))
    sc.save()
    au.save()


def join():
    parts = [f"sop03_c{i}" for i in range(1, 6)]
    print(S.join("sop03", parts))
    print(S.contact_sheet("sop03"))
    print(S.preview_gif("sop03"))


if __name__ == "__main__":
    for arg in sys.argv[1:] or list(CHAPTERS):
        if arg == "join":
            join()
        else:
            CHAPTERS[arg]()
