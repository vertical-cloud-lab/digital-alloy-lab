"""One run in four stills, joined into a strip: Fig. enclosure (b) of the ONR YIP copper/DED proposal.

Sterling's Oct 27 review (digital-alloy-lab issue 212) asked for snapshots of this model in the order of a run, with
the charge in cups (byu-vcl #222 and #248, brought here in #179) instead of rods:

  (i)   a machined cup filled with powder, its plug beside it;
  (ii)  the plugged cups standing in the crucible, in place of the four rods at the end of 03_furnace_load (2a.9);
  (iii) the melt pool while the coil stirs it (05_melt, stirred as in the summary's R.1b);
  (iv)  mid-pour onto the ultrasonic plate (06_pour, partway through 5.6).

The cup and plug are the as-made sizes of ../../atomizer-charge/drawing/cup_plug.py: a 6063 cup, Ø.750 x 2.750 with a
1/2 in drill 2.25 deep, and its .5625 plug with the #60 vent, pressed in flush over the powder. They are revolved here in
CadQuery from that drawing's own half-profiles (cup_outline(), plug_halves()). The powder is drawn as steps.Powder draws
it. The cup charge is a variant of this script only (cup_charge()): steps.py and its animations are unchanged. Each
scene is set up with steps.py's own helpers, in the state its step leaves it; only the cameras are new, framed for a
panel about an inch tall.

    VIZ3D_CLEAN=1 xvfb-run -a -s "-screen 0 1920x1080x24" python proposal_strip.py         # the stills, then the strip
    VIZ3D_CLEAN=1 xvfb-run -a -s "-screen 0 1920x1080x24" python proposal_strip.py strip   # re-join the strip only

Writes out/proposal/{1_cup,2_charge,3_melt,4_pour}.png (1600 x 900, no text) and
../../near-term-submissions/onr-yip/figures-cu-ded/atomizer-sequence.png: the four side by side, 6.5 in (the
proposal's text width) by 1.05 in at 600 dpi, labelled (i)-(iv) in 8 pt Times New Roman.
"""
from __future__ import annotations

import math
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("VIZ3D_CLEAN", "1")      # no text in the stills: the figure's caption says what they show

import cadquery as cq  # noqa: E402
import numpy as np  # noqa: E402
import pyvista as pv  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import model as M  # noqa: E402
import steps as ST  # noqa: E402
from scene import FPS, MELT, OUT, Scene, ease, lighter, load_machine, set_cut  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "atomizer-charge" / "drawing"))
import cup_plug as CP  # noqa: E402

SIZE = (1600, 900)
STILLS = OUT / "proposal"
STRIP = REPO / "near-term-submissions" / "onr-yip" / "figures-cu-ded" / "atomizer-sequence.png"
NAMES = ("1_cup", "2_charge", "3_melt", "4_pour")

IN = CP.MM                       # the drawing is in inches; the model in mm
POWDER = (0.62, 0.63, 0.66)      # steps.Powder's colour; its cut face is lighter(POWDER, 0.25)
CUP_D = CP.STOCK_D * IN          # 19.05
PLUG_Z = (CP.CUP_L - CP.PLUG_L) * IN     # the plug's nose, pressed in flush; the powder comes up to it


# ------------------------------------------------------------------------------ the cup and plug
def cup_solid() -> cq.Shape:
    """The cup, bottom at z = 0, open end up: the upper half of the drawing's section, revolved about its axis."""
    top = [(x, y) for x, y in CP.cup_outline() if y >= 0]           # bottom corner ... bore ... drill point (x, 0)
    return M.lathe([(0.0, 0.0)] + [(y * IN, x * IN) for x, y in top])


def powder_solid() -> cq.Shape:
    """The powder, weighed and tapped down: from the drill point up to the plug's nose, a hair inside the bore."""
    r = CP.BORE_D / 2 * IN - 0.05
    x_full = (CP.CUP_L - CP.DEPTH) * IN
    x_apex = x_full - CP.point_h(CP.BORE_D) * IN
    return M.lathe([(0.0, x_apex + 0.05), (r, x_full + 0.05), (r, PLUG_Z), (0.0, PLUG_Z)])


def plug_solid(z0: float = 0.0) -> cq.Shape:
    """The plug, nose down at z0: the drawing's half-section (vent to OD) revolved, so the #60 vent goes through.
    Turned to its cup's bore, as in the drawing's assembly view."""
    upper, _ = CP.plug_halves(d=CP.BORE_D)
    return M.lathe([(y * IN, x * IN) for x, y in upper], z0)


def tess(shape: cq.Shape, tol=0.02, ang=0.08, split_cut=False):
    """model.tess() with a finer angular tolerance: these parts fill the frame, and model.tess's 0.3 rad would show
    facets on their outlines."""
    body, cut = [], []
    for f in shape.Faces():
        verts, tris = f.tessellate(tol, ang)
        if not tris:
            continue
        p = pv.PolyData(np.array([(v.x, v.y, v.z) for v in verts], float),
                        np.hstack([[3, *t] for t in tris]).astype(np.int64))
        bb = f.BoundingBox()
        if split_cut and f.geomType() == "PLANE" and abs(bb.ymin) < 1e-4 and abs(bb.ymax) < 1e-4:
            cut.append(p)
        else:
            body.append(p)

    def merge(ps):
        if not ps:
            return None
        m = pv.merge(ps, merge_points=False) if len(ps) > 1 else ps[0]
        return m.compute_normals(split_vertices=True, feature_angle=40, auto_orient_normals=False)
    return (merge(body), merge(cut)) if split_cut else merge(body)


def add_part(sc, name, shape, color, group, half=False, powder=False):
    """Add a part as load_machine() does: halved at y = 0 with its cut face tinted lighter, or whole. Powder takes
    steps.Powder's look."""
    look = dict(specular=0.05, ambient=0.3) if powder else {}
    cut_look = dict(ambient=0.6, specular=0.0) if powder else dict(ambient=0.55, diffuse=0.5, specular=0.0)
    if not half:
        sc.add(name, tess(shape), color, group, **look)
        return
    body, cut = tess(M.halve(shape), split_cut=True)
    sc.add(name, body, color, group, **look)
    if cut is not None:
        sc.add(name + "#cut", cut, lighter(color, 0.25 if powder else 0.45), group, smooth_shading=False, **cut_look)


# ------------------------------------------------------------------------------ the cup charge
CUP_ANGLES = M.SLUG_ANGLES        # where the rods stand, clear of the lever
CUP_RING = M.CRUCIBLE_ID / 2 - CUP_D / 2 - 0.5     # 18.5 mm: the rods' 20 mm would put a Ø19 cup into the wall


def cup_seat(k: int) -> np.ndarray:
    """Where cup k stands: on the floor cone's outer edge, as the rods do, its bottom just clear of the cone."""
    a = math.radians(CUP_ANGLES[k])
    z = M.Z_CR + M.floor_z(CUP_RING + CUP_D / 2) + 0.2
    return np.array([CUP_RING * math.cos(a), CUP_RING * math.sin(a), z])


def cup_charge(sc):
    """The charge as four plugged cups instead of 03_furnace_load's four rods: each stands where a rod stands (pulled
    in 1.5 mm, see CUP_RING), plug up, as the drawing's assembly view says. The rods are hidden. Not cut away, like the
    rods: groups cup0..cup3 move as the rods' slug0..slug3 do."""
    cup, powder, plug = cup_solid(), powder_solid(), plug_solid(PLUG_Z)
    meshes = [(n, tess(s), c) for n, s, c in (("cup", cup, M.ALU), ("powder", powder, POWDER), ("plug", plug, M.ALU))]
    for k in range(4):
        sc.show(sc.members(f"slug{k}"), 0.0)
        g = f"cup{k}"
        for n, mesh, c in meshes:
            sc.add(f"{n}{k}", mesh.translate(cup_seat(k), inplace=False), c, g,
                   **(dict(specular=0.05, ambient=0.3) if n == "powder" else {}))


# ------------------------------------------------------------------------------ helpers
def run(sc, seconds, update, hold=0.0, live=True):
    """Advance a scene through one sub-step without rendering it: update(e) every frame with e eased, as Scene.step()
    does, then the hold (live: update(1) every frame, so particles keep moving)."""
    frames = max(1, int(round(seconds * FPS)))
    for i in range(1, frames + 1):
        update(ease(i / frames))
        sc.n += 1
    for _ in range(int(round(hold * FPS)) if live else 0):
        update(1.0)
        sc.n += 1


def snap(sc, name, cam, view_angle=30.0):
    sc.cam = cam
    sc.view_angle = view_angle
    img = sc.snap().convert("RGB")
    sc.pl.close()
    STILLS.mkdir(parents=True, exist_ok=True)
    img.save(STILLS / f"{name}.png", optimize=True)
    print("wrote", (STILLS / f"{name}.png").relative_to(HERE), flush=True)


# ------------------------------------------------------------------------------ the four stills
def still_cup():
    """(i) The cup, cut through its axis like the drawing's section, filled with powder up to where the plug's nose
    goes; the plug stands beside it, nose down, ready to press in. No floor, as in render.py's clean hero still."""
    sc = Scene("p1_cup", "", size=SIZE, gif=False, mp4=False)
    add_part(sc, "cup", cup_solid(), M.ALU, "cup", half=True)
    add_part(sc, "powder", powder_solid(), POWDER, "cup", half=True, powder=True)
    add_part(sc, "plug", plug_solid().translate(cq.Vector(27.0, 4.0, 0.0)), M.ALU, "plug")
    snap(sc, NAMES[0], [(-95, -205, 118), (12, 6, 33), (0, 0, 1)], view_angle=19)


def still_charge():
    """(ii) The end of 03_furnace_load's 2a.9 with the cup charge: lid open, crucible, holder and nut on, insulation
    and thermocouple in, the sealing rod down on the lever, the chamber door still open, the furnace cut away."""
    sc = Scene("p2_charge", "", size=SIZE, gif=False, mp4=False)
    load_machine(sc, cut=ST.FURNACE_CUT + ("chamber",), hide=ST.UTILITY_NAMES, pipes=False, defer=True)
    for g in ST.STACK:                       # the stack goes in after the furnace (02_stack)
        sc.show(sc.members(g), 0.0)
    ST.hood(sc, 110)
    ST.lever(sc, 0.0)
    ST.rod_lift(sc, 0.0)
    ST.door(sc, 100)
    for c in range(3):
        ST.clamp(sc, c, 0.0)
    set_cut(sc, 1.0)
    cup_charge(sc)
    snap(sc, NAMES[1], [(-150, -420, 1515), (0, 0, 1262), (0, 0, 1)], view_angle=30)


def still_melt():
    """(iii) 05_melt once the charge is a pool (4.3, ~800 °C, the coil on), with the surface stirred as the summary
    shows it (stir_height): two-thirds of the way through a pulse, as the surge up the rod peaks."""
    sc = Scene("p3_melt", "", size=SIZE, gif=False, mp4=False)
    load_machine(sc, cut=ST.FURNACE_CUT, hide=tuple(n for n in ST.UTILITY_NAMES if n != "air_frl"), pipes=("air",),
                 defer=True)
    pool = ST.Pool(sc, half=True, level=36)
    ST.add_gas(sc, half=True, furnace=0.7, chamber=0.0)
    for k in range(4):
        sc.show(sc.members(f"slug{k}"), 0.0)
    ST.heat(sc, 800, 1.0)
    ST.rod_lift(sc, -1.5)                    # the rod sinks a little as the charge gives way (4.2)
    set_cut(sc, 1.0)
    sc.n = int(round(0.64 * ST.STIR_PERIOD * FPS))       # frame 11 at 15 fps: 0.67 of a pulse
    pool.set(36, stir=1.0)
    snap(sc, NAMES[2], [(-150, -430, 1395), (0, 0, 1262), (0, 0, 1)], view_angle=30)


def still_pour():
    """(iv) 06_pour run without rendering through 5.1-5.5 (vibration on, draining pressure, rod up, a turbo push) and
    3 s into 5.6, steady atomizing: the stream on the plate, droplets off it, powder gathering in the container."""
    sc = Scene("p4_pour", "", size=SIZE, gif=False, mp4=False)
    load_machine(sc, cut=ST.FURNACE_CUT + ST.CHAMBER_CUT, ghost={"stack_cover": 0.35}, hide=ST.UTILITY_NAMES,
                 pipes=False, defer=True)
    for k in range(4):
        sc.show(sc.members(f"slug{k}"), 0.0)
    pool = ST.Pool(sc, half=True, level=36)
    powder = ST.Powder(sc, half=True, level=0)
    ST.add_stream(sc)
    ST.add_film(sc)
    spray = ST.Particles(sc, "spray", (0.40, 0.41, 0.46), size=5.5)
    drops = ST.Particles(sc, "drops", MELT, size=7.0, slowmo=0.35)
    ST.heat(sc, 795, 1.0)
    ST.add_gas(sc, half=True, furnace=0.7, chamber=0.7)
    set_cut(sc, 1.0)
    st = dict(level=36.0)

    def rod_up(u):                           # 5.4
        ST.rod_lift(sc, 12 * ST.window(u, 0.0, 0.3))
        ST.stream(sc, 1.0 if u > 0.3 else 0.0, 1.0, ST.window(u, 0.3, 0.6))
        ST.film(sc, u > 0.6)
        if 0.6 < u < 0.95 and sc.n % max(1, 3 * FPS // 15) == 0:
            drops.emit_drops(2, M.IMPACT + np.array([0, 0, 3]), M.PLATE_UP * 250 + M.STACK_DIR * 500)
        drops.step()
        ST.shake(sc, True)

    def turbo(u):                            # 5.5
        ST.stream(sc, 1.0, 1.0 + 0.8 * math.sin(math.pi * u))
        spray.emit_spray(ST.per_frame(int(18 * ST.window(u, 0.3, 1.0))))
        spray.step()
        drops.step()
        st["level"] -= 0.12 * ST.PER_FRAME
        pool.set(st["level"])
        ST.shake(sc, True)

    def atomize(u, rate=28):                 # 5.6
        ST.stream(sc, 1.0, 1.0)
        spray.emit_spray(ST.per_frame(rate))
        spray.step()
        drops.step()
        st["level"] = max(-12.0, st["level"] - 0.085 * ST.PER_FRAME)
        pool.set(st["level"])
        powder.set(3 + 55 * min(1.0, spray.landed / 5200))
        ST.shake(sc, True)

    for seconds, hold in ((3.0, 1.2), (2.5, 1.0), (2.0, 1.0)):    # 5.1-5.3: gauges and the vibration only
        run(sc, seconds, lambda u: ST.shake(sc, True), hold=hold)
    run(sc, 3.0, rod_up, hold=1.0)
    run(sc, 2.5, turbo, hold=1.0)
    run(sc, 3.0, atomize)
    snap(sc, NAMES[3], [(330, -940, 1290), (-5, 0, 1000), (0, 0, 1)], view_angle=30)


# ------------------------------------------------------------------------------ the strip
DPI = 600
STRIP_W, STRIP_H = round(6.5 * DPI), round(1.05 * DPI)    # the proposal's text width; about an inch tall
GAP = 30                                                    # 0.05 in between panels
LABEL_PT = 8


def times() -> str:
    """Times New Roman, as the proposal is set (ttf-mscorefonts-installer); Liberation Serif has the same metrics."""
    for pat in ("Times New Roman", "Liberation Serif"):
        try:
            out = subprocess.run(["fc-match", "-f", "%{file}|%{family}", pat], capture_output=True, text=True,
                                 check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            continue
        path, fam = out.split("|", 1)
        if pat.split()[0] in fam:
            return path
    raise SystemExit("no Times New Roman (or Liberation Serif) font found")


def strip():
    n = len(NAMES)
    pw = (STRIP_W - GAP * (n - 1)) // n
    W = pw * n + GAP * (n - 1)
    out = Image.new("RGB", (W, STRIP_H), "white")
    d = ImageDraw.Draw(out)
    font_path = times()
    f = ImageFont.truetype(font_path, round(LABEL_PT / 72 * DPI))
    edge = (176, 180, 186)
    for k, name in enumerate(NAMES):
        im = Image.open(STILLS / f"{name}.png").convert("RGB")
        cw = round(im.height * pw / STRIP_H)                   # the centre of each still, at the panel's aspect
        x0 = (im.width - cw) // 2
        tile = im.crop((x0, 0, x0 + cw, im.height)).resize((pw, STRIP_H), Image.LANCZOS)
        x = k * (pw + GAP)
        out.paste(tile, (x, 0))
        d.rectangle((x, 0, x + pw - 1, STRIP_H - 1), outline=edge, width=3)
        label = f"({'i ii iii iv'.split()[k]})"
        m = round(0.035 * DPI)
        tb = d.textbbox((0, 0), label, font=f)
        d.rectangle((x + 3, 3, x + m + tb[2] + round(0.02 * DPI), m + tb[3] + round(0.015 * DPI)), fill="white")
        d.text((x + m, m), label, font=f, fill="black")
    STRIP.parent.mkdir(parents=True, exist_ok=True)
    out.save(STRIP, dpi=(DPI, DPI), optimize=True)
    print(f"wrote {STRIP.name}: {W} x {STRIP_H} px = {W / DPI:.3f} x {STRIP_H / DPI:.3f} in at {DPI} dpi "
          f"(labels: {Path(font_path).name})")


STILL_FNS = {"1_cup": still_cup, "2_charge": still_charge, "3_melt": still_melt, "4_pour": still_pour}

if __name__ == "__main__":
    args = sys.argv[1:]
    if args != ["strip"]:
        for name in (args or NAMES):
            STILL_FNS[name]()
    if not args or args == ["strip"]:
        strip()
