"""CadQuery model of the bench for sieving atomized powder (docs/sieve-order.md), for the 3-D animation.

Everything is in millimetres, z up from the bench top, the operator stands at -y. Sizes:

* The 8 in stack bought on ME Order 13553 (McMaster-Carr 7969T19 cover, 7969T38 No. 60, 7969T46 No. 230, 7969T21
  pan; all 304 stainless, cloth included): 8 in (203.2 mm) frames, 2 in (50.8 mm) deep, which is also what each
  nested sieve adds to the stack. The 5/8 in skirt that nests in the sieve below, the 1.2 mm sheet and the rolled
  rim are the usual 8 in full-height frame, assumed: McMaster gives only diameter and depth. The cloth is drawn as a
  thin disc, since 63 and 250 um openings are far below the drawing's resolution (zoom.py draws the No. 230 at size).
* The rePowder powder container as drawn in #255's ``atomizer-training/viz3d/model.py`` (O130 x 202 mm with a top
  tube and a handle): its position was observed on video, its size was assumed there and is still not measured.
* Stand-ins, sized to the job: a 320 x 240 mm stainless tray, a flat 50 x 90 mm stainless scoop, 140 mm tweezers,
  100 mL glass jars (O50 x 80 mm, the "smaller jars" of #222), two O146 mm stainless funnels, a top-loading balance,
  the dish for pieces, and a copper ground bus bar on insulated standoffs with an earth lead off the back of the bench.
  The doser cartridge is the O25.0 mm auger tube from vertical-cloud-lab/powder-doser (PR #170).

Every part that powder touches is built from the same centre lines (``*_LINE``) and half thickness that dem.py
collides with, so the particles meet the surfaces that are drawn. ``parts()`` returns the named solids; ``meshes()``
tessellates them (whole, and halved at y = 0 for the cutaway) and caches them in ``.cache/``; ``colliders()`` lists
the DEM walls.

    python model.py      # builds and caches the meshes, prints the part list
"""
from __future__ import annotations

import hashlib
import math
import pickle
from dataclasses import dataclass, field
from pathlib import Path

import cadquery as cq
import numpy as np

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"

# ------------------------------------------------------------------------------------------ colours
STEEL = (0.80, 0.81, 0.83)
STEEL_DK = (0.60, 0.62, 0.65)
MESH_C = (0.50, 0.52, 0.56)
MESH_F = (0.42, 0.44, 0.48)
BENCH = (0.92, 0.91, 0.88)
GLASS = (0.72, 0.86, 0.94)
LID = (0.12, 0.12, 0.13)
PANEL = (0.95, 0.95, 0.96)
LCD = (0.25, 0.55, 0.95)
BLUE = (0.16, 0.36, 0.78)
WHITE = (0.96, 0.96, 0.96)
LABEL = (1.0, 1.0, 1.0)
COPPER = (0.78, 0.45, 0.28)
CREAM = (0.93, 0.90, 0.80)
CHUNK = (0.58, 0.60, 0.64)
EARTH = (0.20, 0.62, 0.25)

T_SHEET = 0.6              # half thickness of the stainless sheet (1.2 mm)

# ------------------------------------------------------------------------------------- the sieves
SIEVE_OD = 203.2           # 8 in
DEPTH = 50.8               # 2 in deep; also the nesting height
SKIRT_H = 15.9             # 5/8 in skirt (assumed)
RW = SIEVE_OD / 2 - T_SHEET            # frame wall centre line
RS = RW - 2 * T_SHEET - 0.5            # skirt centre line: 0.5 mm clear inside the frame below
LIP = 1.8                  # rolled rim, outwards
SIEVE_LINE = [(RS, 0.0), (RS, SKIRT_H), (RW, SKIRT_H), (RW, SKIRT_H + DEPTH - 2 * T_SHEET),
              (RW + LIP, SKIRT_H + DEPTH - 2 * T_SHEET)]
PAN_LINE = [(0.0, T_SHEET), (RW, T_SHEET), (RW, DEPTH - T_SHEET), (RW + LIP, DEPTH - T_SHEET)]
COVER_SKIRT = 10.0
COVER_LINE = [(RS, 0.0), (RS, COVER_SKIRT), (RW + LIP, COVER_SKIRT)]
COVER_TOP = [(0.0, COVER_SKIRT), (RS, COVER_SKIRT)]
MESH_R = RW - T_SHEET - 0.1
MESH_T = 0.25              # cloth half thickness
MESH_DZ = SKIRT_H + T_SHEET + MESH_T   # cloth centre above the skirt's bottom edge

STACK_XY = (150.0, -20.0)
ORDER = ("pan", "s230", "s60")          # bottom to top
SKIRT_Z = {"s230": DEPTH - (SKIRT_H - T_SHEET), "s60": 2 * DEPTH - (SKIRT_H - T_SHEET)}   # skirt bottoms, stacked
MESH_Z = {"pan": 2 * T_SHEET, "s230": SKIRT_Z["s230"] + MESH_DZ, "s60": SKIRT_Z["s60"] + MESH_DZ}
TOP_RIM_Z = 3 * DEPTH                   # 152.4: rim of the No. 60, where the cover sits
COVER_Z = TOP_RIM_Z - (COVER_SKIRT - T_SHEET)
SIEVE_LABEL = {"s60": "No. 60 (250 µm)", "s230": "No. 230 (63 µm)", "pan": "pan"}

# ------------------------------------------------------------------------------- other things
TRAY_C = (-230.0, 0.0)
TRAY_W, TRAY_D, TRAY_H = 320.0, 240.0, 18.0
CONT_R, CONT_H = 65.0, 202.0           # #255's assumed powder container (not measured)
CONT_LINE = [(0.0, 1.0), (54.0, 1.0), (64.0, 11.0), (64.0, 190.0), (44.0, 200.0), (44.0, 228.0)]
CONT_T = 1.0
CONT_XY = (-470.0, 170.0)
DISH_XY = (-30.0, 215.0)
DISH_LINE = [(0.0, 0.6), (27.0, 0.6), (32.0, 11.0), (33.5, 11.5)]
JAR_R, JAR_H = 25.0, 80.0              # 100 mL jar
JAR_LINE = [(0.0, 1.0), (23.6, 1.0), (23.6, 70.0), (21.6, 74.0), (21.6, JAR_H)]
JAR_T = 1.0
FUNNEL_LINE = [(7.0, 0.0), (7.0, 28.0), (70.0, 98.0), (73.0, 98.0)]
FUNNEL_SEAT = JAR_H + JAR_T - 42.2 + 0.3   # funnel base above the jar's base: its cone rests on the lip
BAL_XY = (420.0, -70.0)
BAL_W, BAL_D, BAL_H = 190.0, 210.0, 42.0
BAL_PAN_R, BAL_PAN_Z = 60.0, BAL_H + 10.0
JAR_Z = {"coarse": 0.0, "print": BAL_PAN_Z + 2.0}
JAR_XY = {"coarse": (390.0, 185.0), "print": BAL_XY}
DOSER_XY = (560.0, 180.0)
DOSER_R, DOSER_L = 12.5, 100.0         # O25.0 auger tube (powder-doser PR #170)
COVER_PARK = (190.0, 215.0)            # where the cover waits while the No. 60 is filled
SIEVE_PARK = {"s60": (700.0, 165.0), "s230": (690.0, -125.0)}     # where each sieve goes once it is emptied
SCOOP_REST = (-215.0, -215.0)          # scoop origin (front edge, bottom centre) at rest, pointing +x
SCOOP_L, SCOOP_W, SCOOP_WALL, SCOOP_BACK = 90.0, 50.0, 16.0, 20.0
TWEEZ_REST = (-60.0, -200.0)           # tweezer tips at rest, pointing -x
TWEEZ_L, TWEEZ_GAP = 140.0, 12.0
BUS_Y, BUS_X0, BUS_X1, BUS_Z = 300.0, -500.0, 40.0, 30.0
GROUND_PTS = {"container": (-460.0, BUS_Y, BUS_Z), "tray": (-330.0, BUS_Y, BUS_Z),   # ring lugs, screwed down
              "pan": (15.0, BUS_Y, BUS_Z)}

# ------------------------------------------------------------------------------------- primitives
V = cq.Vector


def box(x0, x1, y0, y1, z0, z1) -> cq.Shape:
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, pnt=V(x0, y0, z0))


def cyl(r, h, base=(0, 0, 0), d=(0, 0, 1)) -> cq.Shape:
    return cq.Solid.makeCylinder(r, h, V(*base), V(*d))


def sphere(r, c=(0, 0, 0)) -> cq.Shape:
    return cq.Workplane("XY").sphere(r).val().translate(V(*c))


def lathe(pts, z0=0.0, x=0.0, y=0.0) -> cq.Shape:
    """Revolve a closed half-profile of (r, z) points about the z axis, then move it."""
    wp = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))
    return wp.val().translate(V(x, y, z0))


def fuse(*shapes) -> cq.Shape:
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.clean()


def shell(line, t, x=0.0, y=0.0, z0=0.0) -> cq.Shape:
    """The solid that dem.py collides with: each segment of a centre line in (r, z) thickened by t on both sides
    and run on by t at its ends (so corners close), revolved about z and moved to (x, y, z0)."""
    out = []
    pts = [np.asarray(p, float) for p in line]
    for a, b in zip(pts[:-1], pts[1:]):
        d = (b - a) / np.linalg.norm(b - a)
        nrm = np.array([-d[1], d[0]])
        a2, b2 = a - d * t, b + d * t
        quad = [a2 + nrm * t, b2 + nrm * t, b2 - nrm * t, a2 - nrm * t]
        quad = [(max(0.0, float(q[0])), float(q[1])) for q in quad]
        out.append(lathe(quad))
    return fuse(*out).translate(V(x, y, z0))


def torus(R, r, c=(0, 0, 0)) -> cq.Shape:
    return cq.Solid.makeTorus(R, r, V(*c), V(0, 0, 1))


# ------------------------------------------------------------------------------------------- parts
@dataclass
class Part:
    name: str
    shape: cq.Shape
    color: tuple
    group: str = "static"
    opacity: float = 1.0
    cut: bool = True               # halve it in cutaway views
    tol: float = 0.3
    tags: tuple = field(default_factory=tuple)


def container(x: float, y: float) -> cq.Shape:
    """#255's powder container: a stainless can with a top tube and a handle on the tube. Assumed size."""
    body = shell(CONT_LINE, CONT_T, x, y)
    handle = fuse(box(x - 8, x + 8, y - 88, y - 44.5, CONT_H + 5, CONT_H + 21),
                  box(x - 4, x + 85, y - 100, y - 88, CONT_H + 7, CONT_H + 19))
    return fuse(body, handle)


def jar_lid(x: float, y: float, z0: float = 0.0) -> cq.Shape:
    r = JAR_R - 1.4
    z = JAR_H + JAR_T + 0.2
    return lathe([(0, z), (r, z), (r, z + 8.6), (r - 1.2, z + 9.2), (0, z + 9.2)], z0, x, y)


def scoop_shape() -> cq.Shape:
    """Flat stainless scoop in its own frame: front edge at x = 0, bowl back to x = -90, 50 wide, a handle."""
    t = 2 * T_SHEET
    L, W, H, B = SCOOP_L, SCOOP_W, SCOOP_WALL, SCOOP_BACK
    s = fuse(box(-L, 0, -W / 2, W / 2, 0, t),
             box(-L, 0, -W / 2, -W / 2 + t, 0, H), box(-L, 0, W / 2 - t, W / 2, 0, H),
             box(-L, -L + t, -W / 2, W / 2, 0, B))
    handle = cyl(4.0, 115.0, (-L + 1.0, 0, B - 4.0), (-math.cos(math.radians(22)), 0, math.sin(math.radians(22))))
    return fuse(s, handle)


def tweezer_prong(side: float) -> cq.Shape:
    """One prong of a pair of tweezers, tip at the origin and the body back along -x, on the side y = side * gap / 2;
    the two prongs meet at the back."""
    s, g = side, TWEEZ_GAP / 2
    p = cq.Workplane("XY").polyline([(0, s * (g - 0.6)), (-TWEEZ_L, s * 0.4), (-TWEEZ_L, s * 1.6),
                                     (0, s * (g + 0.6))]).close()
    return p.extrude(5.0).val()


def balance(x: float, y: float) -> list[Part]:
    P = []
    body = cq.Workplane("XY").box(BAL_W, BAL_D, BAL_H).edges("|Z").fillet(8).val().translate(V(x, y, BAL_H / 2))
    P.append(Part("balance_body", body, PANEL, "balance", cut=False, tol=0.6))
    P.append(Part("balance_display", box(x - 60, x + 60, y - BAL_D / 2 - 0.6, y - BAL_D / 2 + 1.0, 12, 30), LCD,
                  "balance", cut=False, tol=0.5))
    P.append(Part("balance_pedestal", cyl(16, BAL_PAN_Z - BAL_H, (x, y, BAL_H)), STEEL_DK, "balance", cut=False))
    P.append(Part("balance_pan", cyl(BAL_PAN_R, 2.0, (x, y, BAL_PAN_Z)), STEEL, "balance", cut=False, tol=0.4))
    return P


def doser_tube(x: float, y: float) -> list[Part]:
    """The doser's cartridge: the O25.0 auger tube with its screw-on cap, standing on end for scale."""
    r = DOSER_R
    return [Part("doser_tube", fuse(cyl(r, DOSER_L - 14, (x, y, 0)), cyl(r - 0.5, 14, (x, y, DOSER_L - 14))), WHITE,
                 "doser", cut=False, tol=0.2),
            Part("doser_band", cyl(r + 0.6, 22, (x, y, 30)).cut(cyl(r - 1, 24, (x, y, 29))), BLUE, "doser", cut=False,
                 tol=0.2),
            Part("doser_cap", fuse(cyl(13.2, 9, (x, y, DOSER_L - 2)), cyl(10, 3, (x, y, DOSER_L + 7))), BLUE, "doser",
                 cut=False, tol=0.2)]


def piece_shape(rng: np.random.Generator, r0: float) -> cq.Shape:
    """An unatomized piece, a splat or bead of a few millimetres: a sphere with one or two lobes fused on, all inside
    a sphere of r0 about the origin (the DEM sphere that stands for it)."""
    parts = [sphere(0.82 * r0)]
    for _ in range(rng.integers(1, 3)):
        d = rng.normal(0, 1, 3)
        d[2] *= 0.4
        d /= np.linalg.norm(d)
        rl = rng.uniform(0.42, 0.55) * r0
        parts.append(sphere(rl, d * (0.97 * r0 - rl)))
    return fuse(*parts)


PIECE_R = (3.2, 2.6, 3.6, 2.9, 3.4, 2.7, 3.0)      # the DEM spheres that stand for the pieces


def parts() -> list[Part]:
    P = []
    P.append(Part("bench", box(-560, 880, -300, 330, -18, 0), BENCH, "static", cut=False, tol=2.0))
    # grounded stainless tray
    tx, ty = TRAY_C
    t = 2 * T_SHEET
    tray = box(tx - TRAY_W / 2, tx + TRAY_W / 2, ty - TRAY_D / 2, ty + TRAY_D / 2, 0, TRAY_H).cut(
        box(tx - TRAY_W / 2 + t, tx + TRAY_W / 2 - t, ty - TRAY_D / 2 + t, ty + TRAY_D / 2 - t, t, TRAY_H + 1))
    P.append(Part("tray", tray, STEEL, "tray", cut=False, tol=0.5))
    # ground bus bar on two insulated standoffs, and the earth lead that leaves the bench at the back
    P.append(Part("bus_bar", box(BUS_X0, BUS_X1, BUS_Y - 10, BUS_Y + 10, BUS_Z - 6, BUS_Z), COPPER, "static",
                  cut=False, tol=0.3))
    for k, xs in enumerate((BUS_X0 + 25, BUS_X1 - 25)):
        P.append(Part(f"standoff{k}", cyl(8.0, BUS_Z - 6, (xs, BUS_Y, 0)), CREAM, "static", cut=False, tol=0.3))
    # the sieve stack, assembled, pan on the bench
    sx, sy = STACK_XY
    P.append(Part("pan", shell(PAN_LINE, T_SHEET, sx, sy), STEEL, "pan", tol=0.25))
    for name in ("s230", "s60"):
        P.append(Part(name, shell(SIEVE_LINE, T_SHEET, sx, sy, SKIRT_Z[name]), STEEL, name, tol=0.25))
        P.append(Part(name + "_mesh", cyl(MESH_R, 2 * MESH_T, (sx, sy, MESH_Z[name] - MESH_T)),
                      MESH_F if name == "s230" else MESH_C, name, tol=0.6))
    cov = fuse(shell(COVER_LINE, T_SHEET, sx, sy, COVER_Z), shell(COVER_TOP, T_SHEET, sx, sy, COVER_Z),
               cyl(7, 4, (sx, sy, COVER_Z + COVER_SKIRT + T_SHEET)), cyl(11, 3, (sx, sy, COVER_Z + COVER_SKIRT + 4.6)))
    P.append(Part("cover", cov, STEEL, "cover", tol=0.25))
    # the powder container in its place beside the tray
    P.append(Part("container", container(*CONT_XY), STEEL, "container", cut=False, tol=0.5))
    # scoop and tweezers, built in their own frames and placed at rest
    sxr, syr = SCOOP_REST
    P.append(Part("scoop", scoop_shape().translate(V(sxr, syr, 0.0)), STEEL, "scoop", cut=False, tol=0.3))
    wx, wy = TWEEZ_REST
    for side, nm in ((1.0, "tweezer_a"), (-1.0, "tweezer_b")):
        pr = tweezer_prong(side).translate(V(wx, wy, 0.0))
        P.append(Part(nm, pr, STEEL_DK, nm, cut=False, tol=0.2))
    # dish for the pieces, jars with funnels and lids, balance, doser cartridge
    P.append(Part("dish", shell(DISH_LINE, T_SHEET, *DISH_XY), STEEL, "dish", cut=False, tol=0.3))
    for name in ("coarse", "print"):
        (x, y), z0 = JAR_XY[name], JAR_Z[name]
        P.append(Part(f"jar_{name}", shell(JAR_LINE, JAR_T, x, y, z0), GLASS, f"jar_{name}", opacity=0.40, cut=False,
                      tol=0.3))
        P.append(Part(f"lid_{name}", jar_lid(x, y, z0), LID, f"lid_{name}", cut=False, tol=0.3))
        P.append(Part(f"funnel_{name}", shell(FUNNEL_LINE, T_SHEET, x, y, z0 + FUNNEL_SEAT), STEEL, f"funnel_{name}",
                      cut=False, tol=0.3))
    P += balance(*BAL_XY)
    P += doser_tube(*DOSER_XY)
    x, y = JAR_XY["print"]
    P.append(Part("label", box(x - 14, x + 14, y - JAR_R - 0.4, y - JAR_R + 0.6, JAR_Z["print"] + 22,
                               JAR_Z["print"] + 44), LABEL, "label", cut=False, tol=0.3))
    return P


def piece_meshes() -> list:
    """The pieces as meshes about the origin (dem.py moves them)."""
    rng = np.random.default_rng(7)
    return [tess(piece_shape(rng, r), 0.15) for r in PIECE_R]


def colliders() -> list[dict]:
    """The DEM walls: dicts for dem.Collider, in each part's model coordinates."""
    def at(x, y, z=0.0):
        m = np.eye(4)
        m[:3, 3] = (x, y, z)
        return m
    sx, sy = STACK_XY
    tx, ty = TRAY_C
    hw, hd, t = TRAY_W / 2 - T_SHEET, TRAY_D / 2 - T_SHEET, T_SHEET
    tray = [((tx, ty, t), (1, 0, 0), (0, 1, 0), hw, hd),
            ((tx - hw, ty, TRAY_H / 2), (0, 1, 0), (0, 0, 1), hd, TRAY_H / 2),
            ((tx + hw, ty, TRAY_H / 2), (0, 1, 0), (0, 0, 1), hd, TRAY_H / 2),
            ((tx, ty - hd, TRAY_H / 2), (1, 0, 0), (0, 0, 1), hw, TRAY_H / 2),
            ((tx, ty + hd, TRAY_H / 2), (1, 0, 0), (0, 0, 1), hw, TRAY_H / 2)]
    L, W, H, B = SCOOP_L, SCOOP_W, SCOOP_WALL, SCOOP_BACK
    scoop = [((-L / 2, 0, t), (1, 0, 0), (0, 1, 0), L / 2, W / 2),
             ((-L / 2, -W / 2 + t, H / 2), (1, 0, 0), (0, 0, 1), L / 2, H / 2),
             ((-L / 2, W / 2 - t, H / 2), (1, 0, 0), (0, 0, 1), L / 2, H / 2),
             ((-L + t, 0, B / 2), (0, 1, 0), (0, 0, 1), W / 2, B / 2)]
    wx, wy = TWEEZ_REST
    C = [dict(name="bench", group="static", kind="plates", elems=[((150, 15, -5.0), (1, 0, 0), (0, 1, 0), 720, 315)],
              half=5.0, mu=0.5),
         dict(name="tray", group="tray", kind="plates", elems=tray, half=T_SHEET, mu=0.45),
         dict(name="container", group="container", kind="lathe", elems=CONT_LINE, half=CONT_T, base=at(*CONT_XY),
              mu=0.35),
         dict(name="scoop", group="scoop", kind="plates", elems=scoop, half=T_SHEET, base=at(*SCOOP_REST), mu=0.40),
         dict(name="pan", group="pan", kind="lathe", elems=PAN_LINE, half=T_SHEET, base=at(sx, sy), mu=0.40),
         dict(name="dish", group="dish", kind="lathe", elems=DISH_LINE, half=T_SHEET, base=at(*DISH_XY), mu=0.45)]
    for name in ("s230", "s60"):
        C.append(dict(name=name, group=name, kind="lathe", elems=SIEVE_LINE, half=T_SHEET,
                      base=at(sx, sy, SKIRT_Z[name]), mu=0.40))
        # the cloth: fines (class 0) cross the No. 230; fines and 63-250 um (classes 0, 1) cross the No. 60
        C.append(dict(name=name + "_mesh", group=name, kind="lathe", elems=[(0.0, MESH_DZ), (MESH_R, MESH_DZ)],
                      half=MESH_T, base=at(sx, sy, SKIRT_Z[name]), mu=0.45,
                      pass_mask=0b001 if name == "s230" else 0b011, rate=1.0))
    C.append(dict(name="cover", group="cover", kind="lathe", elems=COVER_LINE, half=T_SHEET,
                  base=at(sx, sy, COVER_Z), mu=0.40))
    C.append(dict(name="cover_top", group="cover", kind="lathe", elems=COVER_TOP, half=T_SHEET,
                  base=at(sx, sy, COVER_Z), mu=0.40))
    for name in ("coarse", "print"):
        (x, y), z0 = JAR_XY[name], JAR_Z[name]
        C.append(dict(name=f"jar_{name}", group=f"jar_{name}", kind="lathe", elems=JAR_LINE, half=JAR_T,
                      base=at(x, y, z0), mu=0.35))
        C.append(dict(name=f"funnel_{name}", group=f"funnel_{name}", kind="lathe", elems=FUNNEL_LINE, half=T_SHEET,
                      base=at(x, y, z0 + FUNNEL_SEAT), mu=0.30))
    C.append(dict(name="balance_pan", group="balance", kind="lathe",
                  elems=[(0.0, BAL_PAN_Z + 1.0), (BAL_PAN_R, BAL_PAN_Z + 1.0)], half=1.0, mu=0.4,
                  base=at(*BAL_XY)))
    # tweezer prongs: a thin plate along the 60 mm nearest each tip, in the prong's frame
    for side, nm in ((1.0, "tweezer_a"), (-1.0, "tweezer_b")):
        g = TWEEZ_GAP / 2
        slope = (g - 1.0) / TWEEZ_L
        u = np.array([-1.0, -side * slope, 0.0])
        C.append(dict(name=nm, group=nm, kind="plates",
                      elems=[((wx - 30.0, wy + side * (g - 30.0 * slope), 2.5), u, (0, 0, 1), 30.0, 2.5)], half=0.6,
                      mu=0.3))
    return C


# ----------------------------------------------------------------------------------------- meshing
def _poly(shape: cq.Shape, tol: float):
    import pyvista as pv
    verts, tris = shape.tessellate(tol, 0.3)
    if not tris:
        return None
    pts = np.array([(v.x, v.y, v.z) for v in verts], float)
    faces = np.hstack([[3, *t] for t in tris]).astype(np.int64)
    return pv.PolyData(pts, faces)


def tess(shape: cq.Shape, tol: float = 0.3, split_cut: bool = False):
    """PyVista mesh of a CadQuery shape. With split_cut, returns (body, cut faces lying on y = 0)."""
    import pyvista as pv
    body, cut = [], []
    for f in shape.Faces():
        p = _poly(f, tol)
        if p is None:
            continue
        if split_cut and f.geomType() == "PLANE":
            bb = f.BoundingBox()
            if abs(bb.ymin - STACK_XY[1]) < 1e-4 and abs(bb.ymax - STACK_XY[1]) < 1e-4:
                cut.append(p)
                continue
        body.append(p)

    def merge(ps):
        if not ps:
            return None
        m = pv.merge(ps, merge_points=False) if len(ps) > 1 else ps[0]
        return m.compute_normals(split_vertices=True, feature_angle=40, auto_orient_normals=False)

    return (merge(body), merge(cut)) if split_cut else merge(body)


def halve(shape: cq.Shape) -> cq.Shape:
    """Keep the back half of the stack, y >= its axis (the camera looks from -y, so the cut faces point at it)."""
    return shape.cut(box(-3000, 3000, -3000, STACK_XY[1], -3000, 3000))


def _source_hash() -> str:
    return hashlib.sha1(Path(__file__).read_bytes()).hexdigest()[:12]


def meshes(force: bool = False) -> dict:
    """{name: dict(whole, half, half_cut, color, group, opacity, cut, gone)} (cached)."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"meshes_{_source_hash()}.pkl"
    if path.exists() and not force:
        return pickle.loads(path.read_bytes())
    out = {}
    for p in parts():
        whole = tess(p.shape, p.tol)
        half = half_cut = None
        gone = False
        if p.cut:
            try:
                h = halve(p.shape)
                if h.isValid() and h.Volume() > 1e-3:
                    half, half_cut = tess(h, p.tol, split_cut=True)
                else:
                    gone = True
            except Exception as exc:  # noqa: BLE001
                print("halve failed:", p.name, exc)
        out[p.name] = dict(whole=whole, half=half, half_cut=half_cut, color=p.color, group=p.group,
                           opacity=p.opacity, cut=p.cut, gone=gone)
    out["_pieces"] = piece_meshes()
    path.write_bytes(pickle.dumps(out))
    return out


if __name__ == "__main__":
    import time
    t = time.time()
    m = meshes(force=True)
    print(f"{len(m)} parts in {time.time() - t:.0f} s")
    for k, v in m.items():
        if k.startswith("_"):
            continue
        print(f"  {k:18s} {v['group']:12s} {v['whole'].n_cells if v['whole'] is not None else 0:7d} tris"
              f"{'  (cutaway)' if v['half'] is not None else ''}")
