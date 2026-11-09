"""The corrosion setup built from scratch, as a video: every part laid out, then assembled.

Asked for on PR #180 (2026-11-09): take Ben's order list (Items to Order.txt) as the BOM, add
what the lab already has, and animate the build from the parts up. Each bought part is drawn at
the size its vendor publishes (parts_lib.DIMS; the quotes are in parts-check.md), so a part that
won't fit shows up here before it arrives. Writes build-from-scratch.mp4 (1280 x 720, 30 fps),
a GIF preview of the electrode cap, and one still per chapter.

What it shows, in order:
 1. The bought parts, one at a time, with what each one is for (blue: on Ben's order).
 2. What isn't on the order yet (amber).
 3. The H2D print, with both magnet pauses.
 4. Cutting the stock: steel slugs, brass pins, the PTFE blank, an alloy slice.
 5. A well lid: brass pins and copper-foil pads.
 6. The electrode cap: slugs, CPG-37 pins, the Pt coil on its carrier, the reference, the disc.
 7. The coupon tray: inserts, P75 pins, the bus, coupons, O-rings, lids and screws.
 8. The bench cell, with the graphite counter and the Ossila reference.
 9. Checking a sulfide stock with the CHEMets kit.
10. Everything on the CubXL deck, the capper setting the cap on S1, and the current path.
11. What the model caught.

Geometry: the printed parts are this PR's STL files (copper/cad, bom/cad), placed in their own
frames; the H2D plate is bom/h2d's layout; the deck positions are stirrers/deck_stir.py's. The
CubXL frame and head reuse copper/render_cubxl_cu.py, which needs the capper's three STEP files
(--capper-cad; see README.md for the pinned fetch).

    xvfb-run -a python render_build.py --capper-cad /tmp/byu-vcl-capper-cad --part 0/4   # one of 4 parts
    python render_build.py --assemble 4
    xvfb-run -a python render_build.py --capper-cad /tmp/byu-vcl-capper-cad --stills     # one PNG per chapter
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
AC = HERE.parent
REPO = AC.parent
CU_CAD = AC / "copper" / "cad"
BOM_CAD = AC / "bom" / "cad"
sys.path.insert(0, str(HERE))
import parts_lib as PL  # noqa: E402

W, H, FPS = 1280, 720, 30
OUT = HERE / "build-from-scratch.mp4"
SEG = HERE / "_segments"

ORANGE = (235, 104, 52)
STATUS = {
    "ordered": ("ON BEN'S ORDER", (37, 99, 235)),
    "printed": ("PRINTED ON THE H2D", (21, 128, 61)),
    "onhand": ("ALREADY IN THE LAB", (107, 114, 128)),
    "todo": ("NOT ORDERED YET", (180, 83, 9)),
    "quote": ("BEING QUOTED", (180, 83, 9)),
    "cut": ("CUT FROM STOCK", (37, 99, 235)),
}
COL = dict(pla="#ebe7de", pla2="#ddd7ca", fkm="#6e4128", brass="#caa64b", gold="#d9b54d", copper="#c8763f", steel="#8f9398",
           nickel="#c6c9cd", graphite="#3a3b3e", pt="#dedfe2", ptfe="#f8f8f5", glass="#d8eaf3", agcl="#6f6b66", silver="#c9ccd0",
           peek="#c8b28a", mat="#e6e5e0", cuni="#bda79e", nab="#c69c55", ded="#c08a62", c706="#c98e74", asw="#8fc0e6",
           water="#d6ebf7", mb="#2350a8", black="#262626", red="#c0392b", white="#f6f6f3", cable="#8f9296", wire_blue="#2d6cdf",
           deck="#e4ebee", solder="#b9bbbd", kcl="#eaf4f8", cardboard="#c9a978", amber="#e3a33b", tip="#f2f2ee")
INK, INK2, MUTED, PAPER = (11, 11, 11), (70, 69, 66), (137, 135, 129), (246, 245, 241)


# ----------------------------------------------------------------------------------------- maths
def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lin(u):
    return min(max(u, 0.0), 1.0)


def rotmat(rx, ry, rz):
    a, b, c = np.radians([rx, ry, rz])
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def T(x=0.0, y=0.0, z=0.0):
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def load(path, frame=(0, 0, 0)) -> pv.PolyData:
    m = pv.read(path).clean()
    m = m.compute_normals(auto_orient_normals=False, split_vertices=True, feature_angle=35)
    return m.translate(frame, inplace=False) if any(frame) else m


def stl(name):
    for d in (BOM_CAD, CU_CAD):
        if (d / f"{name}.stl").exists():
            return d / f"{name}.stl"
    raise FileNotFoundError(name)


# ----------------------------------------------------------------------------------------- engine
class Obj:
    """A mesh with keyframed pose (position, Euler rotation about a pivot, scale), opacity and colour."""

    def __init__(self, mesh, color, opacity=1.0, pivot=(0, 0, 0), show=(-1e9, 1e9), fade=0.35, **kw):
        self.mesh, self.color, self.opacity = mesh, color, opacity
        self.pivot = np.array(pivot, float)
        self.keys, self.ckeys, self.okeys, self.hl = [], [], [], []
        self.show, self.fade, self.kw = list(show), fade, kw
        self.actor = None

    def key(self, t, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.keys.append((t, np.array(pos, float), np.array(rot, float), np.array(scale, float)))
        self.keys.sort(key=lambda k: k[0])
        return self

    def move(self, t0, t1, p0, p1, r0=(0, 0, 0), r1=None, s0=(1, 1, 1), s1=None):
        self.key(t0, p0, r0, s0)
        self.key(t1, p1, r0 if r1 is None else r1, s0 if s1 is None else s1)
        return self

    def drop(self, t0, dz=25.0, dur=0.6, pos=(0, 0, 0), rot=(0, 0, 0)):
        """Appear at t0, falling dz into pos."""
        p = np.array(pos, float)
        self.show[0] = t0
        self.key(t0, p + (0, 0, dz), rot).key(t0 + dur, p, rot)
        return self

    def pose(self, t):
        ks = self.keys
        if not ks:
            return np.zeros(3), np.zeros(3), np.ones(3)
        if t <= ks[0][0]:
            return ks[0][1:]
        if t >= ks[-1][0]:
            return ks[-1][1:]
        for a, b in zip(ks, ks[1:]):
            if a[0] <= t <= b[0]:
                u = ease((t - a[0]) / max(b[0] - a[0], 1e-9))
                return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
        return ks[-1][1:]

    def matrix(self, t):
        p, r, s = self.pose(t)
        R = rotmat(*r) @ np.diag(s)
        M = np.eye(4)
        M[:3, :3] = R
        M[:3, 3] = p + self.pivot - R @ self.pivot
        return M

    def alpha(self, t):
        a0, a1 = self.show
        if t < a0 or t > a1:
            return 0.0
        if self.fade <= 0:
            a = 1.0
        else:
            a = min(1.0, (t - a0) / self.fade, (a1 - t) / self.fade)
        for t0, t1, o0, o1 in self.okeys:
            if t >= t0:
                a *= o0 + (o1 - o0) * ease((t - t0) / max(t1 - t0, 1e-9))
        return max(0.0, min(1.0, a))

    def colour(self, t):
        c = hexrgb(self.color) if isinstance(self.color, str) else np.array(self.color, float)
        for t0, t1, c1 in self.ckeys:
            if t >= t0:
                c = c + (hexrgb(c1) - c) * ease((t - t0) / max(t1 - t0, 1e-9))
        for t0, t1 in self.hl:
            if t0 <= t <= t1:
                u = min(1.0, (t - t0) / 0.25, (t1 - t) / 0.25)
                c = c + (np.array(ORANGE) / 255 - c) * 0.6 * max(u, 0)
        return c


class Shot:
    chapter = ""
    dur = 10.0
    depth_peel = False
    bg = "#f6f5f1"

    def __init__(self):
        self.objs, self.caps, self.tags, self.cards, self.cams, self.hooks, self.draw2d = {}, [], [], [], [], [], []
        self.build()

    def build(self):
        pass

    def add(self, key, mesh, color, **kw):
        o = Obj(mesh, color, **kw)
        self.objs[key] = o
        return o

    def cap(self, t0, t1, text):
        self.caps.append((t0, t1, text))

    def tag(self, t0, t1, anchor, text, off=(40, -40), small=False):
        self.tags.append((t0, t1, anchor, text, off, small))

    def card(self, t0, t1, title, status, lines, ident=""):
        self.cards.append((t0, t1, title, status, lines, ident))

    def cam(self, t, focal, dist, az, el):
        self.cams.append((t, np.array(focal, float), float(dist), float(az), float(el)))

    def setup(self, pl):
        for k, o in self.objs.items():
            kw = dict(smooth_shading=True, specular=0.25, specular_power=18)
            kw.update(o.kw)
            mesh = o.mesh
            if not kw["smooth_shading"] and "Normals" in mesh.point_data:
                mesh = mesh.copy()  # flat shading with a point-normal array renders black in this VTK
                mesh.point_data.remove("Normals")
            o.actor = pl.add_mesh(mesh, color=o.color, opacity=o.opacity, name=k, **kw)
        pl.camera.view_angle = 30.0

    def camera(self, t):
        cs = sorted(self.cams, key=lambda c: c[0])
        if t <= cs[0][0]:
            c = cs[0][1:]
        elif t >= cs[-1][0]:
            c = cs[-1][1:]
        else:
            for a, b in zip(cs, cs[1:]):
                if a[0] <= t <= b[0]:
                    u = ease((t - a[0]) / max(b[0] - a[0], 1e-9))
                    c = (a[1] + (b[1] - a[1]) * u, math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * u),
                         a[3] + (b[3] - a[3]) * u, a[4] + (b[4] - a[4]) * u)
                    break
        f, d, az, el = c
        az, el = math.radians(az), math.radians(el)
        pos = f + d * np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        return f, pos

    def apply(self, pl, t):
        for o in self.objs.values():
            a = o.alpha(t)
            if a <= 0.003:
                o.actor.SetVisibility(False)
                continue
            o.actor.SetVisibility(True)
            o.actor.user_matrix = o.matrix(t)
            o.actor.prop.opacity = o.opacity * a
            if o.ckeys or o.hl:
                o.actor.prop.color = tuple(o.colour(t))
        for h in self.hooks:
            h(pl, t)
        f, pos = self.camera(t)
        pl.camera.focal_point = tuple(f)
        pl.camera.position = tuple(pos)
        pl.camera.up = (0, 0, 1)
        pl.renderer.ResetCameraClippingRange()

    def anchor(self, a, t):
        if isinstance(a, str):
            o = self.objs[a]
            c = np.array(o.mesh.center, float)
            return (o.matrix(t) @ np.r_[c, 1.0])[:3]
        if isinstance(a, tuple) and len(a) == 2 and isinstance(a[0], str):
            o = self.objs[a[0]]
            return (o.matrix(t) @ np.r_[np.array(a[1], float), 1.0])[:3]
        return np.array(a, float)


# ----------------------------------------------------------------------------------------- 2D
_FONTS = {}


def font(size, bold=False):
    k = (size, bold)
    if k not in _FONTS:
        from matplotlib import font_manager
        path = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold" if bold else "normal"))
        _FONTS[k] = ImageFont.truetype(path, size)
    return _FONTS[k]


def wrap(d, text, fnt, width):
    out = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                out.append(cur)
                cur = w_
        out.append(cur)
    return out


def project(pl, xyz):
    r = pl.renderer
    r.SetWorldPoint(float(xyz[0]), float(xyz[1]), float(xyz[2]), 1.0)
    r.WorldToDisplay()
    x, y, _ = r.GetDisplayPoint()
    return x, H - y


def topbar(d, chapter, n=None):
    d.rectangle([0, 0, W, 34], fill=(252, 252, 251, 235))
    ft = font(18, True)
    title = "Building the corrosion setup from scratch"
    d.text((16, 7), title, font=ft, fill=INK)
    x = 16 + d.textlength(title, font=ft) + 12
    d.text((x, 10), ("·  " + chapter) if chapter else "", font=font(15), fill=INK2)
    d.text((W - 16, 10), "PR #180 · modelled, not built", font=font(13), fill=INK2, anchor="ra")


def caption_bar(d, text, size=17):
    f = font(size)
    lines = wrap(d, text, f, W - 40)
    hb = 14 + (size + 7) * len(lines)
    d.rectangle([0, H - hb, W, H], fill=(252, 252, 251, 236))
    for i, line in enumerate(lines):
        d.text((18, H - hb + 7 + (size + 7) * i), line, font=f, fill=INK)
    return hb


def chip(d, x, y, status, size=12):
    text, col = STATUS[status]
    f = font(size, True)
    w = d.textlength(text, font=f) + 16
    d.rounded_rectangle([x, y, x + w, y + size + 10], radius=(size + 10) // 2, fill=col + (255,))
    d.text((x + 8, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def side_card(d, title, status, lines, ident="", alpha=1.0, x0=W - 410, y0=50, wcard=390):
    a = int(240 * alpha)
    ft, fl = font(18, True), font(14)
    tl = wrap(d, title, ft, wcard - 28)
    body = []
    for ln in lines:
        body += [(ln.startswith("!"), s) for s in wrap(d, ln.lstrip("!"), fl, wcard - 40)] + [(None, "")]
    hcard = 22 + 24 * len(tl) + 30 + 19 * len(body)
    d.rounded_rectangle([x0, y0, x0 + wcard, y0 + hcard], radius=10, fill=(252, 252, 251, a), outline=(200, 198, 192, a), width=1)
    y = y0 + 12
    for s in tl:
        d.text((x0 + 14, y), s, font=ft, fill=INK + (int(255 * alpha),))
        y += 24
    w = chip(d, x0 + 14, y + 2, status)
    if ident:
        d.text((x0 + 22 + w, y + 4), ident, font=font(13, True), fill=INK2 + (int(255 * alpha),))
    y += 30
    for warn, s in body:
        if warn is None:
            y += 5
            continue
        if warn:
            d.text((x0 + 14, y), "!", font=font(14, True), fill=(200, 40, 30, int(255 * alpha)))
        d.text((x0 + 26, y), s, font=fl, fill=((170, 30, 20) if warn else INK2) + (int(255 * alpha),))
        y += 19


def tag_box(d, xy, text, anchor_xy, small=False, alpha=1.0):
    f = font(13 if small else 15, True)
    x, y = xy
    tw = d.textlength(text, font=f)
    a = int(255 * alpha)
    d.line([anchor_xy, (x, y)], fill=ORANGE + (a,), width=2)
    d.ellipse([anchor_xy[0] - 3.5, anchor_xy[1] - 3.5, anchor_xy[0] + 3.5, anchor_xy[1] + 3.5], fill=ORANGE + (a,))
    hh = 13 if small else 15
    d.rounded_rectangle([x - 6, y - hh - 5, x + tw + 6, y + 5], radius=5, fill=(252, 252, 251, int(235 * alpha)), outline=ORANGE + (a,), width=2)
    d.text((x, y - hh - 1), text, font=f, fill=INK + (a,))


def overlay(shot, pl, t, img):
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im, "RGBA")
    for fn in shot.draw2d:
        fn(d, t, pl)
    for t0, t1, anchor, text, off, small in shot.tags:
        if t0 <= t <= t1:
            al = min(1.0, (t - t0) / 0.3, (t1 - t) / 0.3)
            ax, ay = project(pl, shot.anchor(anchor, t))
            if -50 < ax < W + 50 and -50 < ay < H + 50:
                f = font(13 if small else 15, True)
                lx = min(max(ax + off[0], 14), W - 20 - d.textlength(text, font=f))
                ly = min(max(ay + off[1], 60), H - 80)
                tag_box(d, (lx, ly), text, (ax, ay), small, al)
    for t0, t1, title, status, lines, ident in shot.cards:
        if t0 <= t <= t1:
            al = min(1.0, (t - t0) / 0.25, (t1 - t) / 0.25)
            side_card(d, title, status, lines, ident, al)
    topbar(d, shot.chapter)
    for t0, t1, text in shot.caps:
        if t0 <= t <= t1:
            caption_bar(d, text)
            break
    return np.asarray(im.convert("RGB"))


def clock(d, x, y, text, sub=""):
    d.rounded_rectangle([x, y, x + 230, y + (58 if sub else 36)], radius=8, fill=(252, 252, 251, 235), outline=(200, 198, 192, 255))
    d.text((x + 12, y + 7), text, font=font(18, True), fill=INK)
    if sub:
        d.text((x + 12, y + 33), sub, font=font(13), fill=INK2)


def mat(w, h, z=0.0, color=COL["mat"], grid=10.0):
    m = pv.Plane(center=(0, 0, z), direction=(0, 0, 1), i_size=w, j_size=h, i_resolution=1, j_resolution=1).triangulate()
    lines = []
    for x in np.arange(-w / 2 + grid, w / 2, grid):
        lines.append(pv.Line((x, -h / 2, z + 0.02), (x, h / 2, z + 0.02)))
    for y in np.arange(-h / 2 + grid, h / 2, grid):
        lines.append(pv.Line((-w / 2, y, z + 0.02), (w / 2, y, z + 0.02)))
    return m, pv.merge(lines)


# ----------------------------------------------------------------------------------------- 1: bought parts
class Layout(Shot):
    """Parts appear one at a time on a mat, each with a numbered tag and a side card."""
    step = 1.5
    t_first = 0.8
    items = []  # filled by subclasses: (key, {name: (mesh, color, kw)}, pos, rot, card)

    def place_items(self, items):
        self.order = []
        for i, (key, meshes, pos, rot, card) in enumerate(items):
            t0 = self.t_first + i * self.step
            for name, (mesh, color, kw) in meshes.items():
                o = self.add(f"{key}:{name}", mesh, color, **kw)
                o.drop(t0, dz=18.0, dur=0.55, pos=pos, rot=rot)
            first = f"{key}:{next(iter(meshes))}"
            title, status, lines, ident = card
            t_next = self.t_first + (i + 1) * self.step if i + 1 < len(items) else self.dur
            self.card(t0 + 0.15, t_next, title, status, lines, ident)
            self.tag(t0 + 0.5, self.dur, first, f"{i + 1}", off=(18, -18), small=True)
            self.order.append(first)


def objset(*pairs):
    return {name: (mesh, color, dict(kw)) for name, mesh, color, kw in pairs}


class BoughtLong(Layout):
    chapter = "1  what was ordered: stock, electrodes, wire, the sulfide kit"
    step = 1.55

    def build(self):
        D = PL.DIMS
        m, g = mat(520, 330)
        self.add("mat", m, COL["mat"], specular=0.0, smooth_shading=False)
        self.add("grid", g, "#cfcdc6", line_width=1, lighting=False)
        drill = D["drill_rod"]
        drill_a = PL.rod_x(drill["d"], -240, -70)
        drill_b = PL.rod_x(drill["d"], -55, 120)
        brass = pv.merge([PL.rod_x(D["brass_rod"]["d"], -240, -240 + D["brass_rod"]["length"], y=k * 5.0) for k in range(3)])
        graph = pv.merge([PL.rod_x(10.0, -240, -140, y=k * 14.0) for k in range(2)])
        oss = PL.ossila_ref()
        oss_l = oss["glass"].bounds[5]
        coil = PL.belden_coil()
        spool = PL.wire_spool()
        sil = PL.wire_coil("silicone26", R=38.0)
        roll = PL.foil_roll()
        kit_w, kit_d, kit_h = D["chemets"]["box"]
        rot_lay = (0, 90, 0)
        items = [
            ("drill", objset(("a", drill_a, COL["steel"], dict(specular=0.6)), ("b", drill_b, COL["steel"], dict(specular=0.6))),
             (0, 130, 0), (0, 0, 0),
             ("O1 drill rod, 3 mm × 3 ft", "ordered",
              [f"McMaster 88625K62. Ø{drill['d']:.2f} × {drill['length']:.0f} mm (shown broken).",
               "Cut into 2 mm slugs: two in each electrode cap's skirt, for the lid's magnets to pull on."], "B10")),
            ("ptfe", objset(("rod", PL.rod_x(D["ptfe_rod"]["d"], -240, -240 + D["ptfe_rod"]["length"]), COL["ptfe"], dict(specular=0.2))),
             (0, 88, 0), (0, 0, 0),
             ("PTFE rod, 3/4 in", "ordered",
              [f"McMaster 8546K15. Ø{D['ptfe_rod']['d']:.2f} × {D['ptfe_rod']['length']:.0f} mm.",
               "A 6 mm slice is station S4's blank: same lid, no metal, for the carry-over blanks.",
               "Ø19.05 in the tray's 20.6 mm pocket: 0.78 mm of play a side (the CAD blank is Ø20)."], "B46")),
            ("brass", objset(("rods", brass, COL["brass"], dict(specular=0.7))), (0, 50, 0), (0, 0, 0),
             ("Brass rod, 1/16 in, 3 pack", "ordered",
              [f"K&S 8162. Ø{D['brass_rod']['d']:.3f} × {D['brass_rod']['length']:.0f} mm, three rods.",
               "Cut into 6 mm pins, two per lid: they carry each foil pad down through the lid to a spring pin in the tray.",
               "1.588 mm rod in the lid's 1.6 mm holes: it only grips if the printed hole comes out a little small."], "B12")),
            ("graphite", objset(("rods", graph, COL["graphite"], dict(specular=0.15))), (0, 5, 0), (0, 0, 0),
             ("Graphite rods, 10 × 100 mm, two", "ordered",
              [f"ChemicalStore GR4BAR10X100. Purity not stated.",
               "The bench cell's counter electrode, through the cover's 12.5 mm hole. Never in a deck well.",
               "Sterling asked whether graphite could also replace the Pt coil in the cap: Edison is checking."], "B22")),
            ("ossila", objset(*[(k, v, c, dict(opacity=op, specular=sp)) for k, v, c, op, sp in [
                ("glass", oss["glass"], COL["glass"], 0.45, 0.8), ("frit", oss["frit"], "#efe8d8", 1.0, 0.1),
                ("fill", oss["fill"], COL["kcl"], 0.5, 0.2), ("wire", oss["wire"], COL["silver"], 1.0, 0.6),
                ("agcl", oss["agcl"], COL["agcl"], 1.0, 0.1), ("cap", oss["cap"], COL["black"], 1.0, 0.3),
                ("pin", oss["pin"], COL["gold"], 1.0, 0.7)]]),
             (-110, -8, 4), (0, 90, 0),
             ("Master reference: fritted Ag/AgCl, 6 mm glass", "ordered",
              [f"Ossila C2015B1. Ø{D['ossila_ref']['d']:.0f} mm glass body, about {oss_l + D['ossila_ref']['cap_l']:.0f} mm long as drawn.",
               "Checks the cap's leak-free reference every night, and is the bench cell's reference (cover hole 6.5 mm).",
               "KCl filling solution is not included."], "B20")),
            ("belden", objset(("jacket", coil["jacket"], COL["cable"], dict(specular=0.2)),
                              *[(f"c{k}", m_, c, dict()) for k, (m_, c) in enumerate(coil["conductors"])],
                              ("drain", coil["drain"], COL["silver"], dict())), (-185, -80, 0), (0, 0, 0),
             ("Shielded cable, Belden 9534, 3 ft", "ordered",
              [f"ShowMeCables, by the foot. 4 × 24 AWG, foil shield and drain, Ø{D['belden9534']['od']:.1f} mm.",
               "From the tray's JST plug to the potentiostat: WE, RE, CE and a spare. Shield to the potentiostat's ground only."], "B17")),
            ("spool", objset(("spool", spool["spool"], "#d9d6cf", dict()), ("wire", spool["wire"], COL["wire_blue"], dict())),
             (-95, -80, 0), (0, 0, 0),
             ("Wire-wrap wire, 30 AWG, 200 m", "ordered",
              ["Adafruit 1446, blue.", "Inside the cap: the reference and the coil lead to the two spring pins, in the 0.6 mm grooves under the steel disc."], "B15")),
            ("silicone", objset(("coil", sil, COL["black"], dict(specular=0.3))), (-15, -80, 0), (0, 0, 0),
             ("Silicone wire, 26 AWG, 25 ft", "ordered",
              ["Adafruit 2517, black.", "The three bus wires in the tray's underside channels: WE, RE and CE."], "B16")),
            ("foil", objset(("core", roll["core"], COL["cardboard"], dict(specular=0.0)), ("foil", roll["foil"], COL["copper"], dict(specular=0.8))),
             (65, -85, 0), (0, 0, 0),
             ("Copper foil tape 3M 1181, 1/4 in × 18 yd", "ordered",
              [f"Digi-Key 1181 X 1/4\". {D['foil_1181']['width']:.2f} mm wide, conductive adhesive.",
               "Cut into the lids' reference and counter pads, each 2 mm wide at r 10–12 mm, with a tail to its brass pin."], "B11")),
            ("kit", objset(("box", PL.box(-kit_w / 2, -kit_d / 2, 0, kit_w / 2, kit_d / 2, kit_h), "#f1f1ee", dict(specular=0.1)),
                           ("label", PL.box(-kit_w / 2 + 10, -kit_d / 2 + 10, kit_h, kit_w / 2 - 10, kit_d / 2 - 10, kit_h + 0.3), "#2b5ca8", dict(specular=0.0))),
             (195, -70, 0), (0, 0, 0),
             ("CHEMets sulfide kit K-9510", "ordered",
              ["AquaPhoenix, 30 tests. Methylene blue, 0–1 and 1–10 mg/L.",
               "Checks the sulfide stocks at the start and end of each sulfide night. Not needed for the first, plain-seawater nights.",
               "Chapter 9 shows a test."], "B40")),
        ]
        self.dur = self.t_first + self.step * len(items) + 1.6
        self.place_items(items)
        self.cam(0, (115, 10, 0), 960, -95, 58)
        self.cam(self.dur, (115, 10, 0), 920, -86, 56)
        self.cap(0, self.dur, "Ben's order list, one line at a time (prices on the list; sizes from each vendor's page or datasheet)")


class BoughtSmall(Layout):
    chapter = "1  what was ordered: small parts"
    step = 1.2

    def build(self):
        D = PL.DIMS
        m, g = mat(170, 100, grid=5.0)
        self.add("mat", m, COL["mat"], specular=0.0, smooth_shading=False)
        self.add("grid", g, "#d3d1ca", line_width=1, lighting=False)
        items = []
        xs = [-70, -55, -37, -12]
        for x, size in zip(xs, ("006", "008", "010", "013")):
            dd = D[f"oring_{size}"]
            use = {"006": "the deck wells: one per lid, in a Ø7.30 × 1.40 mm counterbore",
                   "008": "the 0.157 cm² calibration lid (P04)", "010": "the 0.289 cm² calibration lid (P05)",
                   "013": "the bench cell's 0.92 cm² window"}[size]
            items.append((f"or{size}", objset(("ring", PL.oring(size), COL["fkm"], dict(specular=0.15))), (x, 28, 0), (0, 0, 0),
                          (f"O-ring AS568-{size}, FKM (Viton) 75, brown, 100", "ordered",
                           [f"The O-Ring Store FDABV75{size}. ID {dd['id']:.2f} × CS {dd['cs']:.2f} mm, OD {PL.oring_od(size):.2f}.",
                            f"For {use}."], {"006": "B01", "008": "B02", "010": "B03", "013": "B04"}[size])))
        cp = PL.cpg37()
        pp = PL.p75()
        items.append(("cpg", objset(("barrel", cp["barrel"], COL["gold"], dict(specular=0.8)), ("plunger", cp["plunger"], COL["gold"], dict(specular=0.8))),
                      (10, 32, 1.0), (0, 90, 0),
                      ("Spring pin Same Sky CPG-37-TH-TR, 10", "ordered",
                       [f"Digi-Key. Tiny: {D['cpg37']['free_h']:.2f} mm high above its Ø{D['cpg37']['flange_d']:.2f} flange, Ø{D['cpg37']['tail_d']:.2f} × {D['cpg37']['tail_l']:.2f} tail, {D['cpg37']['stroke']:.1f} mm stroke, 30 gf at {D['cpg37']['work_h']:.2f} mm.",
                        "Two in the electrode cap, onto the lid's pads. Under 0.4 N each, so the cap's 2 N of magnets can hold it down.",
                        "!The BOM's mounting note assumed a longer pin; chapter 6 has the hole it really needs."], "B06")))
        items.append(("p75", objset(("barrel", pp["barrel"], COL["gold"], dict(specular=0.8)), ("plunger", pp["plunger"], COL["silver"], dict(specular=0.8))),
                      (8, 22, 0.5), (0, 90, 0),
                      ("Pogo pins P75-B1, needle head, 2 × 10", "ordered",
                       [f"Adafruit 2430. {D['p75']['length']:.0f} mm long free, 13 mm pushed in; Ø{D['p75']['barrel_d']:.1f} body, Ø{D['p75']['plunger_d']:.1f} tip. Force not stated (one seller: 180 g).",
                        "Twelve in the tray (a WE pin under each pocket, two pad pins per station) and one in the bench cell's clamp.",
                        "!The tray and clamp CAD drew 11 mm pins (chapters 7 and 8)."], "B07")))
        mags = pv.merge([PL.magnet().translate((k * 5.0, 0, 0), inplace=False) for k in range(3)] + [PL.magnet().translate((5.0, 5.5, 0), inplace=False)])
        items.append(("mag", objset(("m", mags, COL["nickel"], dict(specular=0.9))), (45, 28, 0), (0, 0, 0),
                      ("Magnets, NdFeB N52, 4 × 2 mm, 250", "ordered",
                       ["totalElement D4X2MMN52-250PK.", "Two in each lid and two under each cup in the cup block, dropped in at the print's pauses: 20 in all."], "B08")))
        sc = PL.shcs_m3x8()
        items.append(("m3", objset(("head", sc["head"], "#b9bcbf", dict(specular=0.7)), ("shank", sc["shank"], "#b9bcbf", dict(specular=0.7)),
                                   ("socket", sc["socket"], "#3b3b3b", dict(lighting=False))), (-68, 2, 2.75), (0, 90, 0),
                      ("Socket head screws M3 × 8, 18-8, 100", "ordered",
                       [f"McMaster 91292A112. Head Ø{D['m3x8']['head_d']} × {D['m3x8']['head_h']} mm.",
                        "Two per lid into the tray's heat-set inserts (4.7 mm of thread engaged), four in the bench cell."], "B14")))
        items.append(("pt", objset(("coil", PL.pt_wire_coil(), COL["pt"], dict(specular=0.9))), (-40, 0, 0), (0, 0, 0),
                      ("Platinum wire 0.25 mm, 0.2 m", "ordered",
                       ["Advent PT543404: 99.95 % (the order list says 99.90 %), hard temper: anneal it in a flame before winding, or it springs open.",
                        "10 cm per coil, five turns on the carrier's legs: one coil for copper, one for aluminium.",
                        "$221: Sterling suggested a graphite rod instead; Edison is checking."], "B21")))
        rs = PL.resistor()
        items.append(("res", objset(("body", rs["body"], "#7fb1d9", dict(specular=0.4)), *[(f"b{k}", m_, c, dict()) for k, (m_, c) in enumerate(rs["bands"])],
                                    *[(f"l{k}", m_, COL["silver"], dict(specular=0.8)) for k, m_ in enumerate(rs["leads"])]),
                      (-8, 0, 0), (90, 0, 0),
                      ("Resistor 10 kΩ, 0.1 %, Yageo MFP-25BRD52-10K", "ordered",
                       ["Digi-Key. Half of the dummy cell: test the potentiostat through the tray's wiring, steppers on, before trusting a nanoamp."], "B26")))
        fc = PL.film_cap()
        items.append(("cap", objset(("body", fc["body"], "#3c6db0", dict(specular=0.3)), *[(f"l{k}", m_, COL["silver"], dict(specular=0.8)) for k, m_ in enumerate(fc["leads"])]),
                      (18, 0, 0), (90, 0, 0),
                      ("Film capacitor 1 µF, Panasonic ECQ-E1105KF", "ordered",
                       ["Digi-Key. The dummy cell's other half: with the 10 kΩ it gives a known impedance arc to check against."], "B26")))
        lf = PL.lf2_ref()
        items.append(("lf2", objset(("body", lf["body"], COL["peek"], dict(specular=0.3)), ("tip", lf["tip"], "#f1ede2", dict()), ("pin", lf["pin"], COL["gold"], dict(specular=0.8))),
                      (42, 2, 1.0), (0, 90, 0),
                      ("Leak-free Ag/AgCl reference, Ø2 × 16.6 mm", "quote",
                       ["Innovative Instruments LF-2, custom length (stock is 63 mm). Ben is getting a quote: under $300.",
                        "Rides in the electrode cap, tip 3.0 mm above the metal. Not on the order yet."], "B19")))
        ins = PL.heat_set_insert()
        items.append(("ins", objset(("a", ins, COL["brass"], dict(specular=0.7)), ("b", ins.translate((6, 0, 0), inplace=False), COL["brass"], dict(specular=0.7))),
                      (-70, -30, 0), (0, 0, 0),
                      ("Heat-set inserts M3 (from ME order 13518)", "onhand",
                       ["ruthex-type M3 × 5.7. Eight in the tray, four in the bench cell body."], "")))
        jst = PL.jst_xh4()
        items.append(("jst", objset(("h", jst["housing"], "#f2efe6", dict()), *[(f"p{k}", m_, COL["gold"], dict()) for k, m_ in enumerate(jst["pins"])],
                                    ("plug", jst["plug"], "#f2efe6", dict())), (-45, -30, 0), (0, 0, 0),
                      ("JST-XH 4-pin pair (from ME order 13518)", "onhand",
                       ["The tray's keyed disconnect at its back edge: WE, RE, CE and a spare."], "")))
        items.append(("disc", objset(("d", PL.steel_disc(), COL["steel"], dict(specular=0.6))), (-12, -30, 0), (0, 0, 0),
                      ("Steel discs 1 in × 1 mm, adhesive", "onhand",
                       ["From the capper module's stock (the vial caps use them). One on each electrode cap's top: what the capper's magnet lifts."], "B09")))
        self.dur = self.t_first + self.step * len(items) + 1.6
        self.place_items(items)
        self.cam(0, (24, 0, 0), 230, -96, 55)
        self.cam(self.dur, (24, 0, 0), 215, -86, 53)
        self.cap(0, self.dur, "Small parts at true size: the mat's grid is 5 mm")


class NotYet(Layout):
    chapter = "2  not on the order yet"
    step = 1.45

    def build(self):
        m, g = mat(640, 400, grid=20.0)
        self.add("mat", m, COL["mat"], specular=0.0, smooth_shading=False)
        self.add("grid", g, "#d3d1ca", line_width=1, lighting=False)
        asw = PL.bottle(150, 260, neck_d=45)
        na2s = PL.bottle(55, 95, neck_d=40)
        hno3 = PL.bottle(75, 190, neck_d=30)
        tub = PL.tube_05ml()
        tubes = {f"t{k}": (tub["body"].translate((k * 12.0, 0, 0), inplace=False), "#f3f3ef", dict(opacity=0.85)) for k in range(5)}
        film = PL.cyl(152.4, 0, 0.3, res=96)
        bars = pv.merge([PL.rod_x(25.4, -150, 155, y=k * 32.0) for k in range(2)])
        nab = PL.rod_x(25.4, -150, 0, y=64.0)
        items = [
            ("asw", objset(("b", asw["body"], "#eef4f6", dict(opacity=0.65, specular=0.5)), ("c", asw["cap"], "#2b5ca8", dict()),
                           ("liq", PL.cyl(70, 2, 190, res=48), COL["asw"], dict(opacity=0.5))), (-230, 70, 0), (0, 0, 0),
             ("Substitute ocean water, ASTM D1141, 4 L", "todo",
              ["Ricca 8363-1, without heavy metals (D1141's heavy-metal stock adds copper).", "Ben asked whether Chem Stores has a smaller size."], "B38")),
            ("na2s", objset(("b", na2s["body"], "#4b3a2a", dict(opacity=0.9)), ("c", na2s["cap"], "#f2f2ee", dict())), (-40, 95, 0), (0, 0, 0),
             ("Sodium sulfide nonahydrate, 100 g", "todo",
              ["Sigma 208043 (price an estimate). The sulfide master stock: fume hood.", "Not needed until the sulfide nights start."], "B39")),
            ("hno3", objset(("b", hno3["body"], "#f2efe6", dict(opacity=0.8)), ("c", hno3["cap"], "#d33f2f", dict())), (-115, 90, 0), (0, 0, 0),
             ("Nitric acid, TraceMetal grade, 500 mL", "todo",
              ["Fisher A509P500. 20 µL of 1 M into every ICP-MS tube. Ships as hazmat.", "Ben asked about Chem Stores."], "B41")),
            ("tubes", objset(*[(k, v[0], v[1], v[2]) for k, v in tubes.items()]), (-150, -40, 4), (0, 90, 0),
             ("0.5 mL Safe-Lock tubes, 500", "todo",
              ["Eppendorf 022363611. One per spot, for ICP-MS. The tube rack's holes are 8.2 mm for their 7.8 mm bodies.", "Ben asked about Chem Stores."], "B36")),
            ("film", objset(("f", film, "#d9d2c3", dict(specular=0.2))), (150, 40, 0), (0, 0, 0),
             ("Diamond lapping film 0.1 µm, 12 in, 3", "todo",
              ["PACE PDAA-01P12, $265. The polishing SOP's last step; copper needs its own film.",
               "Ben will ask whether the Prototyping lab has some."], "B29")),
            ("bars", objset(("cu", bars, COL["cuni"], dict(specular=0.6))), (-60, -150, 12.7), (0, 0, 0),
             ("Cu–Ni bars C71500 and C70600, 1 in round", "todo",
              ["OnlineMetals. The calibration alloys R1 and R3. Ben asked whether the lab has Cu–Ni stock.",
               "!A 1 in (25.4 mm) slice doesn't fit the tray's 20.6 mm pocket or the bench clamp's: mill four flats 20 mm across first (chapter 4)."], "B43/B44")),
            ("nab", objset(("b", nab, COL["nab"], dict(specular=0.6))), (-60, -150, 12.7), (0, 0, 0),
             ("NAB bar C95800, about 1 in", "quote",
              ["Atlas Bronze, by quote. Calibration alloy R2. Same 1 in fit as the Cu–Ni bars."], "B45")),
        ]
        self.dur = self.t_first + self.step * len(items) + 1.6
        self.place_items(items)
        self.cam(0, (120, -20, 50), 1050, -96, 42)
        self.cam(self.dur, (120, -20, 50), 1000, -86, 44)
        self.cap(0, self.dur, "Also needed, and not on this order: the electrolyte, the acid, the ICP-MS tubes, the polishing film and the alloys")


# ----------------------------------------------------------------------------------------- 3: the H2D print
class Print(Shot):
    chapter = "3  printing everything on the H2D"
    dur = 17.0

    def build(self):
        sys.path.insert(0, str(AC / "bom" / "h2d"))
        sys.path.insert(0, str(AC / "bom" / "a1-mini"))
        import make_h2d_plate as h2d  # noqa: E402
        plate = json.loads((AC / "bom" / "h2d" / "plate.json").read_text())
        self.sl = plate["slice"]
        bx, by = plate["bed_mm"][0], plate["bed_mm"][1]
        self.add("bed", PL.box(-8, -8, -8, bx + 8, by + 8, -0.4), "#2f3135", specular=0.3, smooth_shading=False)
        self.add("pei", PL.box(0, 0, -0.4, bx, by, -0.02), "#9a8556", specular=0.25, smooth_shading=False)
        self.parts = []
        for it in h2d.placed():
            tm = it["mesh"]
            faces = np.hstack([np.full((len(tm.faces), 1), 3), tm.faces]).ravel()
            pm = PL.fin(pv.PolyData(np.asarray(tm.vertices), faces), 35)
            key = f"part:{it['name']}"
            self.add(key, pm, COL["pla"], specular=0.15)
            self.parts.append(key)
        self.zmax = 90.2
        # magnets: lids (W frame pockets at r 10.3, 60 and 240 deg, z 3.6-5.6) and the cup block (seat 45, skin 0.4)
        self.mag1, self.mag2 = [], []
        k = 0
        for it in h2d.placed():
            if it["key"].startswith("lid_"):
                for ang in (60.0, 240.0):
                    x = it["x"] + 10.3 * math.cos(math.radians(ang))
                    y = it["y"] + 10.3 * math.sin(math.radians(ang))
                    o = self.add(f"mag1_{k}", PL.magnet(), COL["nickel"], specular=0.9, show=(4.6 + 0.12 * k, 1e9), fade=0.1)
                    o.key(4.6 + 0.12 * k, (x, y, 3.6 + 18), ).key(4.6 + 0.12 * k + 0.5, (x, y, 3.6))
                    self.mag1.append((x, y))
                    k += 1
            if it["key"] == "cup_block":
                k2 = 0
                for cx in (30.0, 60.0, 90.0):
                    for ang in (60.0, 240.0):
                        x = it["x"] + (cx - 60.0) + 10.3 * math.cos(math.radians(ang))
                        y = it["y"] + 10.3 * math.sin(math.radians(ang))
                        o = self.add(f"mag2_{k2}", PL.magnet(), COL["nickel"], specular=0.9, show=(11.6 + 0.2 * k2, 1e9), fade=0.1)
                        o.key(11.6 + 0.2 * k2, (x, y, 42.5 + 20)).key(11.6 + 0.2 * k2 + 0.5, (x, y, 42.5))
                        self.mag2.append((x, y))
                        k2 += 1
        import vtk
        self.plane = vtk.vtkPlane()
        self.plane.SetNormal(0, 0, -1)
        self.plane.SetOrigin(0, 0, 0)
        self.hooks.append(self.clip)
        # z(t): print progress with the two pauses
        self.zt = [(0.0, 0.0, 0.0), (4.2, 5.8, self.sl["pauses"][0]["elapsed_h"]), (7.6, 5.8, self.sl["pauses"][0]["elapsed_h"]),
                   (10.6, 44.8, self.sl["pauses"][1]["elapsed_h"]), (13.8, 44.8, self.sl["pauses"][1]["elapsed_h"]),
                   (15.8, self.zmax, self.sl["time_h"]), (17.0, self.zmax, self.sl["time_h"])]
        cx, cy = bx / 2, by / 2
        self.cam(0, (cx, cy - 10, 20), 620, -100, 48)
        self.cam(4.2, (cx - 20, 40, 5), 300, -95, 52)
        self.cam(7.6, (cx - 20, 40, 5), 300, -88, 50)
        self.cam(10.6, (110, 85, 30), 330, -100, 40)
        self.cam(13.8, (100, 80, 40), 260, -92, 42)
        self.cam(17.0, (cx, cy - 10, 30), 600, -80, 45)
        self.cap(0, 4.2, f"One plate, 28 pieces, in PLA: {self.sl['time_h']:.1f} h and {self.sl['filament_g']:.0f} g (Bambu Studio's estimate). Plain white, black or natural PLA: blue and green pigments are usually copper")
        self.cap(4.2, 7.6, "Pause 1, before z 5.8: two 4 × 2 mm magnets in each lid's pockets, same pole up, a drop of superglue each. Then Resume: the next layers seal them in")
        self.cap(7.6, 10.6, "Printing on to the cup block's pocket height")
        self.cap(10.6, 13.8, "Pause 2, before z 44.8: six magnets in the cup block, same pole up as the lids")
        self.cap(13.8, 17.0, "Done. Mark the 008 and 010 lids (the right end of the front row) before taking them off the plate: they look like the others")
        self.draw2d.append(self.clock2d)

    def ztime(self, t):
        for a, b in zip(self.zt, self.zt[1:]):
            if a[0] <= t <= b[0]:
                u = lin((t - a[0]) / max(b[0] - a[0], 1e-9))
                return a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
        return self.zt[-1][1], self.zt[-1][2]

    def setup(self, pl):
        super().setup(pl)
        for k in self.parts:
            self.objs[k].actor.mapper.AddClippingPlane(self.plane)

    def clip(self, pl, t):
        z, _ = self.ztime(t)
        self.plane.SetOrigin(0, 0, z + 0.001)

    def clock2d(self, d, t, pl):
        z, h = self.ztime(t)
        clock(d, 16, 46, f"{int(h)} h {int((h % 1) * 60):02d} min", f"layer z {z:.1f} mm of {self.zmax:.0f}")


# ----------------------------------------------------------------------------------------- 4: cutting the stock
class Stock(Shot):
    chapter = "4  cutting the stock"
    dur = 15.0

    def build(self):
        m, g = mat(260, 140, grid=10.0)
        self.add("mat", m, COL["mat"], specular=0.0, smooth_shading=False)
        self.add("grid", g, "#d3d1ca", line_width=1, lighting=False)
        D = PL.DIMS
        # (a) drill rod -> four 3 x 2 mm slugs
        self.add("drill", PL.rod_x(3.0, -120, -40, y=45), COL["steel"], specular=0.6, show=(0.0, 3.8))
        for k in range(4):
            o = self.add(f"slug{k}", PL.rod_x(3.0, 0, 2.0), COL["steel"], specular=0.6, show=(0.6 + 0.5 * k, 1e9))
            o.key(0.6 + 0.5 * k, (-40, 45, 0)).key(1.0 + 0.5 * k, (-28 + 6 * k, 30, 0))
        self.add("wheel", PL.cyl(14, -0.4, 0.4, res=48), "#6f6f6f", show=(0.4, 2.9)).key(0, (-41, 45, 18), (90, 0, 0))
        self.card(0.2, 3.6, "Steel slugs, Ø3 × 2 mm", "cut",
                  ["Four from the O1 rod: two for each electrode cap's skirt pockets (Ø3.05 × 2 mm), glued in.",
                   "Any 3 mm steel pin works: the rod is just the cheapest source."], "B10")
        # (b) brass rod -> 14 pins
        self.add("brass", PL.rod_x(D["brass_rod"]["d"], -120, -40, y=5), COL["brass"], specular=0.7, show=(3.6, 7.2))
        for k in range(14):
            o = self.add(f"pin{k}", PL.rod_x(D["brass_rod"]["d"], 0, 6.0), COL["brass"], specular=0.7, show=(3.9 + 0.2 * k, 1e9))
            o.key(3.9 + 0.2 * k, (-40, 5, 0)).key(4.3 + 0.2 * k, (-30 + 4.2 * k, -8, 0), (0, 0, 90))
        self.card(3.7, 7.2, "Brass pins, Ø1.59 × 6 mm", "cut",
                  ["Fourteen: two through each of the seven lids, flush with both faces.",
                   "!1/16 in rod is 1.588 mm; the lid's holes are drawn 1.6 mm. Print one lid first and check the pins grip; if loose, a drop of CA."], "B12")
        # (c) PTFE rod -> S4 blank
        ptfe_d = D["ptfe_rod"]["d"]
        self.add("ptfe", PL.rod_x(ptfe_d, -40, 0, y=-40), COL["ptfe"], show=(7.2, 15.0)).key(0, (60, 40, 0))
        o = self.add("blank", PL.cyl(ptfe_d / 2, 0, 6.0, res=64), COL["ptfe"], show=(7.6, 15.0))
        o.key(7.6, (60 + 0.0, 0, ptfe_d / 2 - 6), (0, 90, 0)).key(8.4, (80, -5, 0)).key(9.0, (80, -5, 0))
        q = 10.3
        outline = PL.box(-q, -q, 0, q, q, 0.6).extract_feature_edges()
        self.add("pocket", outline, "#d64545", line_width=3, lighting=False, show=(8.0, 10.6)).key(0, (80, -5, 0.2))
        self.card(7.4, 10.5, "S4 blank, Ø19.05 × 6 mm PTFE", "cut",
                  ["A 6 mm slice of the 3/4 in rod. In the 20.6 mm pocket (red) it has 0.78 mm of play a side, so the lid centres it, not the pocket.",
                   "The CAD drew it Ø20."], "B46")
        # (d) alloy bar -> slice -> four flats
        self.add("bar", PL.rod_x(25.4, -120, -30, y=-45), COL["cuni"], specular=0.6, show=(10.4, 15.0)).key(0, (0, 0, 0))
        sl = PL.cyl(12.7, 0, 6.0, res=96)
        o = self.add("slice", sl, COL["cuni"], specular=0.6, show=(10.8, 13.15), fade=0.2)
        o.key(10.8, (-24, -45, 12.7), (0, 90, 0)).key(11.6, (80, -5, 0)).key(13.2, (80, -5, 0))
        self.add("flatted", PL.flatted_disc(), COL["cuni"], specular=0.6, show=(13.25, 15.0), fade=0.2).key(0, (80, -5, 6.0))
        self.add("pocket2", outline, "#2a9d55", line_width=3, lighting=False, show=(13.0, 15.0)).key(0, (80, -5, 0.2))
        self.card(10.6, 15.0, "Alloy coupons from the 1 in bars", "todo",
                  ["!A 6 mm slice of a 1 in bar is Ø25.4 mm: it can't go in the tray's 20.6 mm pocket (red), or the bench clamp's.",
                   "Mill four flats 20 mm across (or turn it to Ø20). The flatted slice drops in (green). Then polish, SOP #258.",
                   "A 20 × 20 square won't come out of a 1 in bar: its diagonal is 28.3 mm."], "B43–B45")
        self.cam(0, (-30, 20, 0), 300, -95, 55)
        self.cam(3.6, (-30, 0, 0), 280, -90, 55)
        self.cam(7.2, (40, -10, 0), 250, -96, 52)
        self.cam(10.4, (40, -15, 0), 240, -90, 55)
        self.cam(15.0, (50, -15, 0), 220, -84, 57)
        self.cap(0, 15.0, "Before assembly: slugs, pins, the PTFE blank and the coupons come from the bought stock")


# ----------------------------------------------------------------------------------------- 5: the well lid
LID_FACE = 0.0


class Lid(Shot):
    chapter = "5  a well lid"
    dur = 15.5
    depth_peel = True

    def build(self):
        lid = load(stl("well_lid_v2_006"))
        o = self.add("lid", lid, COL["pla"], specular=0.2, pivot=(0, 0, 5.0))
        o.key(0.0, (0, 0, 0), (0, 0, -20)).key(1.6, (0, 0, 0), (0, 0, 0)).key(2.4, (0, 0, 0), (180, 0, 0)).key(5.6, (0, 0, 0), (180, 0, 0)).key(6.6, (0, 0, 0), (0, 0, 0))
        o.okeys.append((12.6, 13.2, 1.0, 0.35))
        o.okeys.append((15.0, 15.4, 1.0, 1.0 / 0.35))
        mags = load(CU_CAD / "lid_hold_magnets.stl")
        self.add("mags", mags, COL["nickel"], specular=0.9, show=(12.6, 1e9))
        # the O-ring test fit, lid upside down: counterbore faces up at z 0 -> flipped about z 5: counterbore at z 10
        ring = PL.oring("006")
        r = self.add("ring", ring, COL["fkm"], specular=0.15, show=(2.8, 5.6), fade=0.25)
        r.key(2.8, (0, 0, 22)).key(3.8, (0, 0, 10.0 - 1.78 + 0.38)).key(5.2, (0, 0, 10.0 - 1.78 + 0.38)).key(5.6, (0, 0, 22))
        # brass pins through the eyelet holes, flush: z 0..6
        for k, sx in enumerate((-10.0, 10.0)):
            p = self.add(f"bpin{k}", PL.cyl(PL.DIMS["brass_rod"]["d"] / 2, 0, 6.0, res=24), COL["brass"], specular=0.8, show=(7.0, 1e9))
            p.key(7.0, (sx, 15.0, 14.0)).key(8.0, (sx, 15.0, 0.0))
        pads = load(CU_CAD / "lid_pads.stl")
        p = self.add("pads", pads, COL["copper"], specular=0.8, show=(9.2, 1e9))
        p.key(9.2, (0, 0, 8.0)).key(10.0, (0, 0, 0.0))
        for k, sx in enumerate((-10.0, 10.0)):
            self.add(f"solder{k}", PL.fin(pv.Sphere(radius=0.9, center=(sx, 15.0, 6.1))), COL["solder"], specular=0.9, show=(10.8, 1e9))
        self.card(0.2, 2.4, "Well lid v2 (P03): 24 × 35 × 6 mm, with the Ø16 boss", "printed",
                  ["Two magnets already sealed in at r 10.3 mm (pause 1).", "Seven printed: five 006 lids, one 008 and one 010 for calibration."], "P03")
        self.card(2.4, 6.6, "The AS568-006 in the counterbore", "ordered",
                  ["Free: OD 6.46 × 1.78 mm. The counterbore is Ø7.30 × 1.40: the ring stands 0.38 mm proud and is squeezed 21 % when the lid is screwed down.",
                   "!It sits loose (0.42 mm of room a side), so it falls out when the lid is turned over. Set it on the coupon, centred on the spot, and lower the lid over it (chapter 7)."], "B01")
        self.card(6.6, 9.2, "Brass pins through the lid", "cut",
                  ["Pressed into the Ø1.6 holes at (±10, 15) mm, flush top and bottom. Below, a pogo pin in the tray pushes up on each."], "B12")
        self.card(9.2, 12.6, "Copper-foil pads (3M 1181)", "ordered",
                  ["Reference pad at −x, counter pad at +x: 2 mm wide at r 10–12 mm, ±30°, each trimmed from the 6.35 mm tape, with a tail to its brass pin.",
                   "Solder each tail to its pin top. The cap's spring pins land on the pads."], "B11")
        self.card(12.6, 15.5, "Inside: the two hold-down magnets", "ordered",
                  ["4 × 2 mm N52 under a 0.4 mm skin, at 60° and 240°. They pull on the cap's steel slugs: about 2 N to hold the cap down against its spring pins."], "B08")
        self.cam(0.0, (0, 0, 4), 95, -110, 40)
        self.cam(2.4, (0, 0, 6), 85, -100, 50)
        self.cam(5.6, (0, 0, 8), 70, -95, 62)
        self.cam(7.0, (0, 5, 4), 90, -100, 42)
        self.cam(12.6, (0, 2, 4), 85, -80, 48)
        self.cam(15.5, (0, 2, 4), 85, -70, 50)
        self.tag(3.9, 5.6, (0, 0, 10.6), "AS568-006, free size", off=(-260, -70))
        self.tag(7.8, 9.2, "bpin1", "brass pin, Ø1.59", off=(60, -50))
        self.tag(10.0, 12.6, (11.0, 0.0, 6.1), "counter pad (+x)", off=(60, -60))
        self.tag(10.0, 12.6, (-11.0, 0.0, 6.1), "reference pad (−x)", off=(-200, -60))
        self.cap(0, 15.5, "Seven lids, the same steps on each")


# ----------------------------------------------------------------------------------------- 6: the electrode cap
class Cap(Shot):
    chapter = "6  the electrode cap"
    dur = 26.0
    depth_peel = True

    def build(self):
        D = PL.DIMS
        piv = (0, 0, 8.0)
        flip = [(0.0, (0, 0, 0), (0, 0, 0)), (3.0, (0, 0, 0), (0, 0, 0)), (4.2, (0, 0, 0), (180, 0, 0)), (8.6, (0, 0, 0), (180, 0, 0)),
                (9.8, (0, 0, 0), (0, 0, 0))]

        def flipkeys(o):
            for t, p, r in flip:
                o.key(t, p, r)
            return o

        cap = flipkeys(self.add("cap", load(CU_CAD / "electrode_cap.stl"), COL["pla"], specular=0.2, pivot=piv))
        cap.okeys.append((9.8, 10.6, 1.0, 0.32))
        # drill #46 down the centre bore
        drill = PL.revolve([(0, 0), (1.03, 0.6), (1.03, 40), (0, 40)], 24)
        self.add("drill", drill, "#9da2a8", specular=0.8, show=(0.6, 2.8)).key(0.6, (0, 0, 30)).key(1.5, (0, 0, -3.5)).key(2.2, (0, 0, -3.5)).key(2.8, (0, 0, 30))
        # slugs into the skirt pockets (cap upside down: pockets face up)
        slugs = load(CU_CAD / "cap_hold_steel.stl")
        o = self.add("slugs", slugs, COL["steel"], specular=0.7, pivot=piv, show=(4.6, 1e9))
        o.key(4.6, (0, 0, 14), (180, 0, 0)).key(5.6, (0, 0, 0), (180, 0, 0)).key(8.6, (0, 0, 0), (180, 0, 0)).key(9.8, (0, 0, 0), (0, 0, 0))
        # CPG-37 pins at (+/-11, 0), plunger down toward the lid. Mid-stroke (1.50 mm working height) on a pad 0.07 mm
        # thick needs the flange's board face 1.57 mm up inside the skirt; the tail goes up a 1.6 mm hole.
        cp = PL.cpg37()
        self.flange_z = 0.07 + D["cpg37"]["work_h"]
        for k, sx in enumerate((-11.0, 11.0)):
            for part in ("barrel", "plunger"):
                m_ = cp[part].rotate_x(180, inplace=False).translate((sx, 0, self.flange_z), inplace=False)
                o = self.add(f"cpg{k}{part}", m_, COL["gold"], specular=0.8, pivot=piv, show=(6.4 + 0.3 * k, 1e9))
                o.key(6.4 + 0.3 * k, (0, 0, 14), (180, 0, 0)).key(7.4 + 0.3 * k, (0, 0, 0), (180, 0, 0)).key(8.6, (0, 0, 0), (180, 0, 0)).key(9.8, (0, 0, 0), (0, 0, 0))
        # the carrier with the Pt coil, off to the side, then up into the socket
        car = load(CU_CAD / "electrode_carrier.stl")
        side = np.array((34.0, 0, -6.0))
        o = self.add("carrier", car, "#d8d4ca", specular=0.2, show=(10.0, 1e9))
        o.key(10.0, side).key(14.6, side).key(16.2, (0, 0, 0))
        coil = load(CU_CAD / "pt_coil.stl")
        o = self.add("coil", coil, COL["pt"], specular=0.9, show=(10.4, 1e9), fade=0.1)
        o.key(10.4, side).key(14.6, side).key(16.2, (0, 0, 0))
        import vtk
        self.coilplane = vtk.vtkPlane()
        self.coilplane.SetNormal(0, 0, -1)
        self.hooks.append(self.wind)
        # the reference down the bore, tip 3.0 below the skirt
        lf = PL.lf2_ref()
        for part, col in (("body", COL["peek"]), ("tip", "#f1ede2"), ("pin", COL["gold"])):
            o = self.add(f"ref{part}", lf[part].translate((0, 0, -3.0), inplace=False), col, specular=0.4, show=(16.4, 1e9))
            o.key(16.4, (0, 0, 22)).key(18.4, (0, 0, 0))
        # wire-wrap leads in the recess floor (z 14.87), under the disc
        zf = 14.87 + 0.25
        wr = PL.DIMS["wirewrap"]["od"] / 2
        tail_top = self.flange_z + D["cpg37"]["tail_l"]
        w_ref = PL.tube_path([(0, 0, 13.6), (0, 0, zf), (-4, 0, zf), (-11, 0, zf), (-11, 0, tail_top)], wr, 10)
        w_ce = PL.tube_path([(2.625, 0, 7.3), (2.625, 0, zf), (6, 0, zf), (11, 0, zf), (11, 0, tail_top)], wr, 10)
        self.add("wref", w_ref, COL["wire_blue"], show=(19.0, 1e9))
        self.add("wce", w_ce, COL["wire_blue"], show=(19.6, 1e9))
        for k, (x, y) in enumerate(((0, 0), (-11, 0), (11, 0), (2.625, 0))):
            self.add(f"sold{k}", PL.fin(pv.Sphere(radius=0.6, center=(x, y, zf))), COL["solder"], specular=0.9, show=(20.2 + 0.15 * k, 1e9))
        disc = load(CU_CAD / "steel_disc.stl")
        self.add("disc", disc, COL["steel"], specular=0.6, show=(21.0, 1e9)).key(21.0, (0, 0, 18)).key(22.4, (0, 0, 0))
        self.card(0.2, 3.0, "Electrode cap (P01), printed", "printed",
                  ["First open the reference bore to 2.05 mm with a #46 drill (B47) in a pin vise, and the bottom 2.2 mm of the two pin holes to 1.3 mm for the CPG-37 barrels."], "P01")
        self.card(3.0, 6.3, "Steel slugs into the skirt", "cut",
                  ["Cap upside down. The two Ø3 × 2 mm slugs go into the skirt's pockets at r 10.3 mm, glued. Over a lid they sit right above its two magnets."], "B10")
        self.card(6.3, 9.8, "Two CPG-37 spring pins at (±11, 0)", "ordered",
                  ["Plunger toward the lid. 30 gf each at the 1.50 mm working height: the magnets hold about 2 N.",
                   "!The BOM says to open the holes to 1.3 mm and recess the flange 0.2 mm. The datasheet pin has a Ø2.00 flange and a Ø1.50 tail, and stands 2.20 mm free: recessed 0.2 mm it would need 1.9 mm of its 0.9 mm stroke and hold the cap 1 mm off the lid.",
                   "Instead: a Ø2.1 counterbore 1.57 mm deep for the flange and barrel, then Ø1.6 × 1.1 for the tail. Solder the wire to the tail first and thread it up the 1.0 mm hole."], "B06")
        self.card(9.8, 14.6, "The Pt coil on the carrier (P02)", "ordered",
                  ["10 cm of 0.25 mm Pt: five turns at r 2.6 mm on the carrier's three legs, 2.4–4.0 mm above the metal; the lead goes up the 0.6 mm hole.",
                   "One coil per alloy family: the 0.2 m buys two. Edison: keep Pt here rather than graphite."], "B21")
        self.card(14.6, 16.4, "Carrier into the cap's socket", "printed", ["The Ø5.95 plug presses into the Ø6.0 socket."], "P02")
        self.card(16.4, 18.9, "The leak-free reference down the bore", "quote",
                  ["Ø2.0 × 16.6 mm: tip 3.0 mm below the skirt, which puts it 3.0 mm above the metal when the cap sits on a lid.",
                   "Its top ends 1.3 mm under the disc. Seal it with neutral-cure RTV."], "B19")
        self.card(18.9, 21.0, "Leads in the grooves under the disc", "ordered",
                  ["30 AWG wire-wrap: reference to the −x pin, coil to the +x pin, up the pin holes and along the 0.6 mm grooves of the recess floor.",
                   "Adafruit doesn't publish the insulation's diameter: check it fits the 0.6 mm grooves."], "B15")
        self.card(21.0, 23.0, "The steel disc goes on last", "onhand",
                  ["1 in × 1 mm with its adhesive, into the Ø25.4 recess: the capper's magnet lifts the cap by it, as it lifts a vial cap."], "B09")
        self.card(23.0, 26.0, "The finished cap", "printed",
                  ["13.5 g. Carried, its lowest points are the carrier's legs, 35.8 mm under the carriage.", "Two are built: one in use, one spare."], "P01")
        self.tag(1.4, 2.8, ("drill", (0, 0, 20)), "#46 drill, Ø2.06", off=(60, -40))
        self.tag(12.0, 14.6, ("coil", (2.6, 0, -3.0)), "Pt coil, 5 turns", off=(60, 30))
        self.tag(18.4, 21.0, ("refbody", (0, 0, -1.5)), "reference tip, 3.0 mm out", off=(70, 40))
        self.cam(0.0, (0, 0, 8), 110, -105, 35)
        self.cam(3.0, (0, 0, 8), 100, -100, 50)
        self.cam(6.3, (0, 0, 8), 95, -90, 55)
        self.cam(9.8, (14, 0, 4), 120, -95, 25)
        self.cam(14.6, (16, 0, 2), 115, -90, 18)
        self.cam(16.4, (0, 0, 6), 100, -95, 22)
        self.cam(18.9, (0, 0, 12), 80, -95, 60)
        self.cam(23.0, (0, 0, 6), 95, -100, 20)
        self.cam(26.0, (0, 0, 6), 95, -60, 25)
        self.cap(0, 26.0, "Two caps are built; the steps are the same for each")

    def setup(self, pl):
        super().setup(pl)
        self.objs["coil"].actor.mapper.AddClippingPlane(self.coilplane)

    def wind(self, pl, t):
        # reveal the coil from the bottom up while it is wound (10.4-14.0 s); its local z runs -3.7..7.3
        u = lin((t - 10.4) / 3.6)
        z = -3.8 + 11.2 * u
        o = self.objs["coil"]
        M = o.matrix(t)
        self.coilplane.SetOrigin(0, 0, M[2, 3] + z)


# ----------------------------------------------------------------------------------------- 7: the coupon tray
SX = [185.0, 210.0, 235.0, 260.0]
SY = 240.0


class Tray(Shot):
    chapter = "7  the coupon tray, coupons and lids"
    dur = 28.0
    depth_peel = True

    def build(self):
        D = PL.DIMS
        cen = (222.5, 240.0, 10.0)
        flip = [(0, (0, 0, 0), (0, 0, 0)), (4.4, (0, 0, 0), (0, 0, 0)), (5.4, (0, 0, 22), (180, 0, 0)), (11.2, (0, 0, 22), (180, 0, 0)),
                (12.2, (0, 0, 0), (0, 0, 0))]

        def fk(o, t_show=None, extra=None):
            for t, p, r in flip:
                o.key(t, p, r)
            return o

        tray = fk(self.add("tray", load(CU_CAD / "coupon_tray.stl"), COL["pla"], specular=0.2, pivot=cen))
        tray.okeys.append((21.4, 22.0, 1.0, 0.28))
        # heat-set inserts at (sx, 240 +/- 14), tops flush at 19.5
        ins = PL.heat_set_insert()
        k = 0
        for sx in SX:
            for sg in (-1, 1):
                o = self.add(f"ins{k}", ins, COL["brass"], specular=0.7, pivot=(cen[0] - sx, cen[1] - (SY + sg * 14), cen[2] - 13.8), show=(1.2 + 0.25 * k, 1e9))
                base = np.array((sx, SY + sg * 14, 13.8))
                o.key(1.2 + 0.25 * k, base + (0, 0, 14)).key(1.7 + 0.25 * k, base)
                for t, p, r in flip[1:]:
                    o.key(t, base + p, r)
                k += 1
        # P75 pins from below: WE pin under each pocket (tip 1 mm above the floor, z 15), pad pins at (sx +/-10, 255), tip at 20.5
        pp = PL.p75()
        L = D["p75"]["length"]
        k = 0
        for sx in SX:
            for x, y, top in [(sx, SY, 15.0), (sx - 10, SY + 15, 20.5), (sx + 10, SY + 15, 20.5)]:
                for part, col in (("barrel", COL["gold"]), ("plunger", COL["silver"])):
                    base = np.array((x, y, top - L))
                    o = self.add(f"p75_{k}{part}", pp[part], col, specular=0.8, pivot=tuple(np.array(cen) - base), show=(5.6 + 0.12 * k, 1e9))
                    o.key(5.6 + 0.12 * k, base - (0, 0, 16), (0, 0, 0))
                    o.key(6.1 + 0.12 * k, base)
                    o.key(11.2, base)
                    for t, p, r in flip[3:]:
                        pass
                    # pins are added while the tray is upside down: give them the tray's flip from 11.2 to 12.2
                    o.keys = [(tt, pp_, rr, ss) for tt, pp_, rr, ss in o.keys]
                    flipped = (np.array((0, 0, 22.0)) + base, np.array((180.0, 0, 0)))
                    o.keys = [(5.6 + 0.12 * k, flipped[0] + (0, 0, 16), flipped[1], np.ones(3)),
                              (6.1 + 0.12 * k, flipped[0], flipped[1], np.ones(3)),
                              (11.2, flipped[0], flipped[1], np.ones(3)),
                              (12.2, base, np.zeros(3), np.ones(3))]
                k += 1
        self.n_p75 = k
        # bus wires in the underside channels (z 0-3) -> JST at the back edge (x 222.5, y 260) -> Belden
        zc = 1.2
        we = [(SX[0], SY, zc)] + [(x, SY, zc) for x in SX[1:]]
        bus_we = PL.tube_path([(SX[0], SY, zc), (SX[-1], SY, zc)], 0.7, 10)
        bus_re = PL.tube_path([(SX[0] - 10, 254.3, zc), (SX[-1] - 10, 254.3, zc)], 0.7, 10)
        bus_ce = PL.tube_path([(SX[0] + 10, 255.7, zc + 0.3), (SX[-1] + 10, 255.7, zc + 0.3)], 0.7, 10)
        exit_ = [PL.tube_path([(222.5 + dx, yb, zc), (222.5 + dx, 262, zc), (222.5 + dx, 268, zc)], 0.7, 10) for dx, yb in ((-1.2, SY), (0.0, 254.3), (1.2, 255.7))]
        wires = {"bus_we": (pv.merge([bus_we, exit_[0]]), "#202020"), "bus_re": (pv.merge([bus_re, exit_[1]]), "#7a3db8"),
                 "bus_ce": (pv.merge([bus_ce, exit_[2]]), "#c0392b")}
        for i, (kname, (m_, col)) in enumerate(wires.items()):
            o = self.add(kname, m_, col, specular=0.3, pivot=cen, show=(7.6 + 0.6 * i, 1e9))
            o.key(7.6, (0, 0, 22), (180, 0, 0)).key(11.2, (0, 0, 22), (180, 0, 0)).key(12.2, (0, 0, 0), (0, 0, 0))
        jst = PL.jst_xh4()
        jm = pv.merge([jst["housing"]] + jst["pins"] + [jst["plug"]]).rotate_x(90, inplace=False).translate((222.5, 268.5, 3.0), inplace=False)
        o = self.add("jst", jm, "#f2efe6", specular=0.2, pivot=cen, show=(9.4, 1e9))
        o.key(9.4, (0, 0, 22), (180, 0, 0)).key(11.2, (0, 0, 22), (180, 0, 0)).key(12.2, (0, 0, 0), (0, 0, 0))
        bel = PL.tube_path([(222.5, 285, 3.0), (222.5, 300, 4.0), (200, 330, 6.0), (150, 345, 6.0)], PL.DIMS["belden9534"]["od"] / 2, 18)
        o = self.add("belden", bel, COL["cable"], specular=0.2, pivot=cen, show=(10.0, 1e9))
        o.key(10.0, (0, 0, 22), (180, 0, 0)).key(11.2, (0, 0, 22), (180, 0, 0)).key(12.2, (0, 0, 0), (0, 0, 0))
        # coupons: S1 C71500, S2 C95800 NAB, S3 DED pad on a 3 mm shim, S4 PTFE blank
        cpn = load(CU_CAD / "coupon_20x20x6.stl")
        thin = cpn.scale((1, 1, 0.5), inplace=False)
        shim = load(CU_CAD / "shim_3mm.stl")
        specs = [("cuni", cpn, COL["cuni"], 0.0), ("nab", cpn, COL["nab"], 0.0), ("ded", thin, COL["ded"], 0.0), ("ptfe", load(CU_CAD / "ptfe_blank.stl"), COL["ptfe"], 0.0)]
        for i, (nm, mesh, col, _) in enumerate(specs):
            base = np.array((SX[i], SY, 20.0))
            t0 = 12.6 + 0.5 * i
            if nm == "ded":
                o = self.add("shim3", shim, COL["pla2"], show=(t0 - 0.3, 1e9))
                o.key(t0 - 0.3, (SX[i], SY, 14.0 + 20)).key(t0 + 0.2, (SX[i], SY, 14.0))
            o = self.add(f"cpn{i}", mesh, col, specular=0.6 if nm != "ptfe" else 0.1, show=(t0, 1e9))
            o.key(t0, base + (0, 0, 25)).key(t0 + 0.6, base)
        # O-rings set on each coupon, centred; then the lids, then two screws each
        ring = PL.oring("006")
        sq = PL.DIMS["oring_006"]
        lid = load(stl("well_lid_v2_006"))
        pads = load(CU_CAD / "lid_pads.stl")
        sc = PL.shcs_m3x8()
        for i in range(4):
            base = np.array((SX[i], SY, 20.0))
            t0 = 15.0 + 0.3 * i
            o = self.add(f"ring{i}", ring, COL["fkm"], specular=0.15, show=(t0, 1e9))
            o.key(t0, base + (0, 0, 15)).key(t0 + 0.5, base).key(18.0 + 0.4 * i, base).key(18.4 + 0.4 * i, base, scale=(1.0, 1.0, 1.40 / 1.78))
            t1 = 16.4 + 0.35 * i
            for part, mesh, col in (("lid", lid, COL["pla"]), ("pads", pads, COL["copper"])):
                o = self.add(f"lid{i}{part}", mesh, col, specular=0.2 if part == "lid" else 0.8, show=(t1, 1e9))
                o.key(t1, base + (0, 0, 30)).key(t1 + 0.7, base + (0, 0, 0.38)).key(18.0 + 0.4 * i, base + (0, 0, 0.38)).key(18.4 + 0.4 * i, base)
                if part == "lid":
                    o.okeys.append((21.4, 22.0, 1.0, 0.28))
            for sg in (-1, 1):
                for part in ("head", "shank", "socket"):
                    p0 = base + (0, sg * 14.0, 2.8)
                    o = self.add(f"scr{i}{sg}{part}", sc[part], "#b9bcbf" if part != "socket" else "#3b3b3b", specular=0.7, show=(17.4 + 0.4 * i, 1e9),
                                 lighting=part != "socket")
                    o.key(17.4 + 0.4 * i, p0 + (0, 0, 12), (0, 0, 0)).key(18.4 + 0.4 * i, p0 + (0, 0, 0.38), (0, 0, 720)).key(18.6 + 0.4 * i, p0, (0, 0, 800))
            for k2, sxp in enumerate((-10.0, 10.0)):
                o = self.add(f"lidpin{i}{k2}", PL.cyl(PL.DIMS["brass_rod"]["d"] / 2, 0, 6.0, res=20), COL["brass"], specular=0.8, show=(t1, 1e9))
                o.key(t1, base + (sxp, 15.0, 30)).key(t1 + 0.7, base + (sxp, 15.0, 0.38)).key(18.0 + 0.4 * i, base + (sxp, 15, 0.38)).key(18.4 + 0.4 * i, base + (sxp, 15, 0))
        self.card(0.2, 1.2, "Coupon tray (P06): 105 × 40 × 19.5 mm", "printed",
                  ["Four 20.6 mm pockets at x 185 / 210 / 235 / 260, y 240 on the deck. The pocket floors set every coupon face at deck z 20."], "P06")
        self.card(1.2, 4.4, "Eight M3 heat-set inserts", "onhand", ["Two per station at y ±14 mm, into the Ø4.0 holes, flush with the top."], "ME 13518")
        p75L = D["p75"]["length"]
        self.card(4.4, 7.6, "Twelve P75-B1 pogo pins, from below", "ordered",
                  ["A WE pin under each pocket, tip 1 mm above the floor so it presses the coupon's back; two pad pins per station, tips 1 mm above the top, under the lid's brass pins.",
                   f"!As bought they are {p75L:.2f} mm long; the tray CAD drew 11 mm pins. With the tip 1 mm above the pocket floor, a WE pin's tail ends {p75L - 15:.2f} mm below the tray's underside: the tray would stand on four pin tails. Raise the tray on 2 mm feet, or lower the pin and accept less stroke."],
                  "B07")
        self.card(7.6, 11.2, "The bus: three wires in the underside channels", "ordered",
                  ["Silicone 26 AWG: WE joins the four WE pins (y 240); RE the −x pad pins and CE the +x pad pins (y 255). They leave at x 222.5 for a JST-XH plug, then 3 ft of Belden 9534 to the potentiostat."],
                  "B16, B17")
        self.card(12.2, 15.0, "Coupons in their pockets", "todo",
                  ["S1 C71500 Cu–Ni, S2 C95800 NAB, S3 a DED pad, S4 the PTFE blank. A thinner piece sits on a 1 or 3 mm shim (P07) so its face is at z 20."], "")
        self.card(15.0, 21.4, "O-ring on the coupon, lid over it, two screws", "ordered",
                  ["Each AS568-006 goes on its coupon, centred on the spot to test. The lid's counterbore drops over it; two M3 × 8 into the inserts close the lid onto the coupon and squeeze the ring 1.78 → 1.40 mm (21 %).",
                   "The squeezed ring wets 0.101–0.126 cm², not the 0.066 of its ID: measure each spot's area afterwards."], "B01, B14")
        self.card(21.4, 28.0, "How each station connects", "printed",
                  ["WE: the pin under the pocket presses the coupon's back.", "RE and CE: the pad pins push up on the brass pins, which carry the foil pads on top. The cap's two spring pins will land on those pads."], "")
        self.tag(21.8, 28.0, ("p75_0barrel", (0, 0, 8)), "WE pin under S1", off=(-210, 50))
        self.tag(21.8, 28.0, ("p75_2barrel", (0, 0, 14)), "CE pad pin", off=(60, 40))
        self.tag(21.8, 28.0, ("p75_1barrel", (0, 0, 14)), "RE pad pin", off=(-170, -70))
        self.cam(0.0, (222, 240, 10), 300, -105, 42)
        self.cam(4.4, (222, 240, 10), 270, -95, 45)
        self.cam(5.4, (222, 245, 20), 260, -90, 50)
        self.cam(11.2, (222, 245, 20), 270, -80, 50)
        self.cam(12.2, (222, 240, 10), 260, -100, 45)
        self.cam(18.0, (222, 240, 15), 250, -90, 40)
        self.cam(21.4, (195, 245, 15), 120, -115, 22)
        self.cam(28.0, (195, 245, 15), 110, -75, 24)
        self.cap(0, 28.0, "The tray holds four stations; each lid seals one spot")


# ----------------------------------------------------------------------------------------- 8: the bench cell
class Bench(Shot):
    chapter = "8  the bench cell (calibration against a 1 cm² window)"
    dur = 16.0
    depth_peel = True

    def build(self):
        D = PL.DIMS
        self.add("clamp", load(stl("bench_cell_clamp")), COL["pla2"], specular=0.2)
        pp = PL.p75()
        L = D["p75"]["length"]
        for part, col in (("barrel", COL["gold"]), ("plunger", COL["silver"])):
            self.add(f"wepin{part}", pp[part], col, specular=0.8, show=(1.0, 1e9)).key(1.0, (0, 0, -6.0 + 1.0 - L - 15)).key(1.8, (0, 0, -6.0 + 1.0 - L))
        cpn = load(CU_CAD / "coupon_20x20x6.stl")
        self.add("cpn", cpn, COL["cuni"], specular=0.6, show=(2.2, 1e9)).key(2.2, (0, 0, 20)).key(2.9, (0, 0, 0))
        ring = PL.oring("013")
        self.add("ring", ring, COL["fkm"], specular=0.15, show=(3.4, 1e9)).key(3.4, (0, 0, 15)).key(4.0, (0, 0, 0)).key(5.6, (0, 0, 0)).key(6.2, (0, 0, 0), scale=(1, 1, 1.40 / 1.78))
        body = load(stl("bench_cell_body"))
        o = self.add("body", body, COL["pla"], specular=0.2, opacity=1.0, show=(4.2, 1e9))
        o.key(4.2, (0, 0, 60)).key(5.2, (0, 0, 0.38)).key(5.6, (0, 0, 0.38)).key(6.2, (0, 0, 0))
        o.okeys.append((8.0, 8.6, 1.0, 0.35))
        sc = PL.shcs_m3x8()
        for k, (x, y) in enumerate([(sx * 17.0, sy * 17.0) for sx in (-1, 1) for sy in (-1, 1)]):
            for part in ("head", "shank", "socket"):
                mesh = sc[part].rotate_x(180, inplace=False)
                o = self.add(f"scr{k}{part}", mesh, "#b9bcbf" if part != "socket" else "#3b3b3b", specular=0.7, show=(5.2 + 0.15 * k, 1e9),
                             lighting=part != "socket")
                o.key(5.2 + 0.15 * k, (x, y, -3.0 - 14)).key(6.2, (x, y, -3.0), (0, 0, 720))
        liq = PL.cyl(29.6, 8.0, 80.0, res=72)
        o = self.add("liq", liq, COL["asw"], opacity=0.45, specular=0.3, show=(6.6, 1e9), pivot=(0, 0, 8.0))
        o.key(6.6, (0, 0, 0), scale=(1, 1, 0.01)).key(8.0, (0, 0, 0), scale=(1, 1, 1))
        cover = load(stl("bench_cell_cover"))
        self.add("cover", cover, COL["pla"], specular=0.2, show=(8.4, 1e9)).key(8.4, (0, 0, 40)).key(9.2, (0, 0, 0))
        gr = PL.cyl(5.0, 0, 100.0, res=48)
        self.add("graphite", gr, COL["graphite"], specular=0.15, show=(9.6, 1e9)).key(9.6, (0, 12, 120)).key(10.8, (0, 12, 30.0))
        self.add("collar", PL.collar(), "#3f6db5", specular=0.2, show=(9.6, 1e9)).key(9.6, (0, 12, 120 + 63)).key(10.8, (0, 12, 93.0 + 0.02))
        oss = PL.ossila_ref()
        hang = 93.0 - oss["glass"].bounds[5]
        for part, (mesh, col, op) in {"glass": (oss["glass"], COL["glass"], 0.5), "frit": (oss["frit"], "#efe8d8", 1.0), "fill": (oss["fill"], COL["kcl"], 0.5),
                                      "wire": (oss["wire"], COL["silver"], 1.0), "agcl": (oss["agcl"], COL["agcl"], 1.0), "cap": (oss["cap"], COL["black"], 1.0),
                                      "pin": (oss["pin"], COL["gold"], 1.0)}.items():
            o = self.add(f"oss{part}", mesh, col, opacity=op, specular=0.5, show=(11.4, 1e9))
            o.key(11.4, (-14, -6, hang + 80)).key(12.6, (-14, -6, hang))
        self.hang = hang
        self.card(0.2, 2.2, "Bench cell clamp plate (P16) and one P75 pin", "printed",
                  ["The coupon pocket on top (20.6 mm), the WE pin up through its floor, four M3 × 8 from below in 5 mm counterbores.",
                   f"!The plate is 8 mm thick and the pin {D['p75']['length']:.0f} mm long: with its tip 1 mm above the pocket floor, its tail hangs 13 mm below the plate. Stand the cell on 15 mm feet, or wire the coupon's back another way."], "P16, B07")
        self.card(2.2, 4.2, "A reference coupon, face up", "todo", ["C71500 here, flatted to fit the 20.6 mm pocket (chapter 4)."], "B43")
        self.card(4.2, 6.6, "AS568-013 under the body's floor", "ordered",
                  ["ID 10.82 mm: a 0.92 cm² window, squeezed 21 % in the Ø15.22 × 1.40 counterbore by four M3 × 8 into the body's inserts."], "B04")
        self.card(6.6, 9.6, "250 mL of substitute seawater", "todo", ["The body (P15) is 60 mm inside, 90 mm tall. Leak-test it overnight with DI water first."], "P15")
        self.card(9.6, 11.4, "Graphite counter through the 12.5 mm hole", "ordered",
                  ["10 × 100 mm, purity not stated: leach it in hot dilute HNO₃ and run a blank first (Edison c2-01).",
                   "!Nothing in the cover sets its depth: it would slide down onto the floor, beside the window. A printed collar (drawn) hangs it 30 mm above the window."], "B22")
        self.card(11.4, 16.0, "Ossila reference through the 6.5 mm hole", "ordered",
                  [f"6 mm glass body; it hangs from its cap with the frit {self.hang + 3:.0f} mm above the window as drawn (length to be confirmed against Ossila's drawing).",
                   "The same electrode checks the cap's leak-free reference every night."], "B20")
        self.cam(0.0, (0, 0, 0), 150, -100, 35)
        self.cam(4.2, (0, 0, 10), 220, -95, 25)
        self.cam(8.0, (0, 0, 45), 330, -95, 22)
        self.cam(16.0, (0, 0, 55), 360, -70, 25)
        self.cap(0, 16.0, "The bulk cell the wells are calibrated against (copper protocol §5)")


# ----------------------------------------------------------------------------------------- 9: sulfide check
class Sulfide(Shot):
    chapter = "9  checking a sulfide stock: CHEMets K-9510"
    dur = 20.0
    depth_peel = True

    def build(self):
        D = PL.DIMS["chemets"]
        m, g = mat(240, 140, grid=10.0)
        self.add("mat", m, COL["mat"], specular=0.0, smooth_shading=False)
        self.add("grid", g, "#d3d1ca", line_width=1, lighting=False)
        r_cup, h_cup = D["cup_d"] / 2, D["cup_h"]
        cup = PL.revolve([(0, 0), (r_cup - 1, 0), (r_cup, h_cup), (r_cup - 0.8, h_cup), (r_cup - 1.8, 0.8), (0, 0.8)], 64)
        self.add("cup", cup, "#eef3f5", opacity=0.45, specular=0.6).key(0, (-20, 0, 0))
        fill_h = D["cup_ml"] * 1000 / (math.pi * (r_cup - 1.6) ** 2)
        mark = PL.revolve([(r_cup - 0.6 + fill_h / h_cup, fill_h), (r_cup + 0.2, fill_h), (r_cup + 0.2, fill_h + 0.6), (r_cup - 0.6, fill_h + 0.6)], 64)
        self.add("mark", mark, "#1f1f1f").key(0, (-20, 0, 0))
        liq = PL.cyl(r_cup - 1.9, 0.8, 0.8 + fill_h, res=64)
        o = self.add("liq", liq, COL["asw"], opacity=0.55, pivot=(0, 0, 0.8), show=(1.0, 1e9))
        o.key(1.0, (-20, 0, 0), scale=(1, 1, 0.01)).key(2.8, (-20, 0, 0), scale=(1, 1, 1))
        stock = PL.bottle(60, 120, neck_d=28)
        o = self.add("stock", stock["body"], "#f2efe6", opacity=0.7, pivot=(0, 0, 60), show=(0.2, 3.4))
        o.key(0.2, (55, 10, 0)).key(1.0, (10, 0, 70), (0, -110, 0)).key(2.8, (10, 0, 70), (0, -110, 0)).key(3.4, (55, 10, 0))
        act = PL.bottle(22, 60, neck_d=10)
        o = self.add("act", act["body"], "#f5f4ef", opacity=0.9, pivot=(0, 0, 50), show=(3.6, 6.4))
        o.key(3.6, (60, -30, 0)).key(4.4, (-20, 0, 60), (0, 180, 0)).key(5.8, (-20, 0, 60), (0, 180, 0)).key(6.4, (60, -30, 0))
        for k in range(2):
            drop = PL.fin(pv.Sphere(radius=1.2, center=(0, 0, 0)))
            o = self.add(f"drop{k}", drop, "#dfe9ef", show=(4.6 + 0.5 * k, 5.1 + 0.5 * k), fade=0.05)
            o.key(4.6 + 0.5 * k, (-20, 0, 58)).key(5.1 + 0.5 * k, (-20, 0, fill_h + 1))
        # the ampoule: glass body + tapered tip, tip down into the cup, snapped, fills, mixed, read
        ar, al, tl = D["ampoule_d"] / 2, D["ampoule_l"], D["tip_l"]
        amp = PL.revolve([(0, 0), (0.6, 0), (0.8, tl * 0.3), (ar - 0.3, tl), (ar, tl + 1.5), (ar, al - 2), (ar - 1.5, al), (0, al)], 40)
        o = self.add("amp", amp, COL["glass"], opacity=0.5, specular=0.9, pivot=(0, 0, al / 2), show=(6.6, 1e9))
        o.key(6.6, (70, 25, 4), (90, 0, 0)).key(7.6, (-20 + 6, 0, 2.0), (0, -8, 0)).key(10.4, (-20 + 6, 0, 2.0), (0, -8, 0))
        o.key(11.2, (-20 + 6, 0, 45), (0, 0, 0)).key(11.6, (-20 + 6, 0, 45), (180, 0, 0)).key(12.0, (-20 + 6, 0, 45), (0, 0, 0)).key(12.4, (-20 + 6, 0, 45), (180, 0, 0)).key(12.8, (-20 + 6, 0, 45), (0, 0, 0))
        o.key(15.6, (-20 + 6, 0, 45), (0, 0, 0)).key(16.6, (60, 0, 18), (0, 0, 0))
        inner = PL.cyl(ar - 0.6, tl + 1.6, al - 3.0, res=32)
        o2 = self.add("ampliq", inner, "#e9eef0", opacity=0.9, pivot=(0, 0, al / 2), show=(8.4, 1e9))
        for kk in o.keys:
            o2.keys.append(kk)
        o2.ckeys.append((9.0, 15.0, COL["mb"]))
        o2.okeys.append((8.4, 9.6, 0.05, 1.0 / 0.05))
        comp = PL.revolve([(9, 0), (16, 0), (16, 60), (9, 60)], 64)
        self.add("comp", comp, "#f4f4f0", opacity=0.5, specular=0.4, show=(15.6, 1e9)).key(15.6, (60, 0, 0))
        for k, c in enumerate(["#f1f4fa", "#cfdcf1", "#9db7e2", "#6a8fd0", "#3a64b6", "#1f418e"]):
            ang = math.radians(60 * k)
            sw = PL.cyl(2.6, 0, 52, res=24).translate((12.5 * math.cos(ang), 12.5 * math.sin(ang), 2), inplace=False)
            self.add(f"std{k}", sw, c, show=(15.6, 1e9)).key(15.6, (60, 0, 0))
        self.draw2d.append(self.timer)
        self.card(0.2, 3.4, "1  Fill the sample cup to the 25 mL mark", "ordered",
                  ["From the sulfide stock's bottle, not from the deck vial.",
                   "!The test takes 25 mL, and a deck stock is one 20 mL vial. Test the bottle each vial is filled from, and refill the vial from it."], "B40")
        self.card(3.4, 6.6, "2  Add 3 drops of activator, stir", "ordered", ["The kit's activator solution (A-9500 in the 2020 instructions, S-9500 in 2025), about 9 mL in its bottle."], "B40")
        self.card(6.6, 10.6, "3  Snap the ampoule's tip in the cup", "ordered",
                  ["Tip first into the cup, press it against the side: the tip breaks and the vacuum fills the ampoule, leaving a small bubble."], "B40")
        self.card(10.6, 15.6, "4  Mix, then wait for the colour", "ordered",
                  ["Invert a few times so the bubble runs end to end, wipe the ampoule dry, and read it at 5 minutes."], "B40")
        self.card(15.6, 20.0, "5  Read it on the comparator", "ordered",
                  ["The same ampoule reads either range: the round comparator C-9501 (0–1 mg/L, drawn) for the 0.1 mg/L stock, the flat C-9510 (1–10) for the 10 mg/L stock. Detection limit 0.05 mg/L.",
                   "30 ampoules at 4 tests a night: about 7 sulfide nights. It doesn't see copper or silver sulfides; thiosulfate, sulfite and oxidants interfere."], "B40")
        self.cam(0.0, (0, 0, 30), 300, -100, 30)
        self.cam(6.6, (-10, 0, 30), 230, -95, 22)
        self.cam(10.6, (-10, 0, 45), 230, -90, 20)
        self.cam(15.6, (30, 0, 30), 260, -88, 25)
        self.cam(20.0, (45, 0, 30), 220, -80, 28)
        self.cap(0, 20.0, "Sulfide escapes as H₂S and oxidises in air, so each stock is measured rather than trusted at its nominal value")

    def timer(self, d, t, pl):
        if 12.8 <= t <= 15.6:
            u = (t - 12.8) / 2.8
            clock(d, 16, 46, f"{int(5 * u)}:{int((5 * u % 1) * 60):02d} of 5:00", "colour developing")


# ----------------------------------------------------------------------------------------- 10: the deck
class Deck(Shot):
    chapter = "10  on the CubXL"
    dur = 30.0
    depth_peel = True

    def build(self):
        import importlib.util
        rc_path = AC / "copper" / "render_cubxl_cu.py"
        spec = importlib.util.spec_from_file_location("rcc", rc_path)
        rcc = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(AC / "copper"))
        spec.loader.exec_module(rcc)
        rcc.CAD = CAPPER_CAD
        spec2 = importlib.util.spec_from_file_location("deck_stir", AC / "stirrers" / "deck_stir.py")
        ds = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(ds)
        self.rcc, self.ds = rcc, ds
        shot = self

        class Shim:
            def __init__(self):
                self.groups = {}

            def add(self, key, mesh, group=None, **kw):
                col = kw.pop("color", "#cccccc")
                op = kw.pop("opacity", 1.0)
                shot.add(key, mesh, col, opacity=op, **kw)
                if group:
                    self.groups.setdefault(group, []).append(key)

        sh = Shim()
        rcc.Scene.build_frame(sh)
        tip_prof = [(0.0, 0.0), (0.45, 0.0), (2.6, 30.0), (2.9, 37.0), (3.3, 39.0), (0.0, 39.0)]
        sh.tip_mesh = rcc.revolve(tip_prof, 360, 0, res=24)
        sh.vial_cap_mesh = rcc.step_mesh("VialCap16mm", 1.5, 12)
        rcc.Scene.build_head(sh)
        self.groups = sh.groups
        self.head_keys = [k for k in self.objs if k.startswith("head:")]
        for k in ("head_tip", "head_tipliq", "carried_vcap"):
            self.objs[k].show = [1e9, 1e9]
        # modules, placed one at a time
        plan = []
        tray = load(CU_CAD / "coupon_tray.stl")
        plan.append(("tray", [("tray", tray, COL["pla"])], "Coupon tray with four stations", "printed"))
        cpn = load(CU_CAD / "coupon_20x20x6.stl")
        lid = load(stl("well_lid_v2_006"))
        pads = load(CU_CAD / "lid_pads.stl")
        sta = []
        for i, sx in enumerate(SX):
            col = [COL["cuni"], COL["nab"], COL["ded"], COL["ptfe"]][i]
            sta += [(f"cpn{i}", cpn.translate((sx, SY, 20), inplace=False), col), (f"lid{i}", lid.translate((sx, SY, 20), inplace=False), COL["pla"]),
                    (f"pads{i}", pads.translate((sx, SY, 20), inplace=False), COL["copper"])]
        plan.append(("stations", sta, "Coupons, O-rings and lids", "printed"))
        cup = load(stl("cup_block_3"))
        cupliq = pv.merge([PL.cyl(4.0, 8, 47, x, 245) for x in (30.0, 60.0)])
        plan.append(("cups", [("cup", cup, COL["pla"]), ("cupliq", cupliq, COL["asw"])], "Cup block: rinse 2 (ASW), rinse 1 (DI), park", "printed"))
        tr = load(stl("tube_rack_2x8"))
        tub = PL.tube_05ml()["body"]
        tubes = pv.merge([tub.translate((x, y, 30 - 28), inplace=False) for x in [176.0 + 12 * k for k in range(8)] for y in (28.0, 46.0)])
        plan.append(("tubes", [("rack", tr, COL["pla"]), ("tubes", tubes, "#f3f3ef")], "Tube rack and 0.5 mL tubes", "printed"))
        base = rcc.base
        racks = []
        for ri, rack in enumerate((base.TIP_RACK_1, ds.TIP_RACK_2)):
            rx0, ry0, rx1, ry1 = base.rack_rect(rack)
            racks.append((f"rack{ri}", PL.box(rx0, ry0, 0, rx1, ry1, 55), COL["pla2"]))
            racks.append((f"tips{ri}", pv.merge([sh.tip_mesh.translate((tx, ty, 27.0), inplace=False) for tx, ty in base.rack_tips(rack)]), COL["tip"]))
        plan.append(("racks", racks, "Tip racks 1 and 2, side by side", "onhand"))
        tw = PL.revolve([(13.4, 3), (15, 3), (15, 50), (13.4, 50)], 48).translate((385, 150, 0), inplace=False)
        twb = PL.cyl(22, 0, 3.0, 385, 150)
        plan.append(("tipwaste", [("tw", pv.merge([tw, twb]), COL["pla"])], "Tip waste cup", "printed"))
        holder = rcc.step_mesh("9VialHolder20mL_TightFit", 4.0, 8).rotate_z(180, inplace=False).translate((rcc.deck_cu.HOLDER_X, rcc.deck_cu.HOLDER_Y[0], 0), inplace=False)
        vials = []
        vv = PL.voa_vial(36)
        for nm, (vx, vy) in ds.HOLDER_STOCKS.items():
            col = COL["water"] if "DI" in nm else "#f1ede0"
            vials += [(f"v{nm}g", vv["glass"].translate((vx, vy, 0), inplace=False), COL["glass"]), (f"v{nm}l", vv["liquid"].translate((vx, vy, 0), inplace=False), col),
                      (f"v{nm}c", sh.vial_cap_mesh.translate((vx, vy, 71 - 0.5), inplace=False), "#e3e1da")]
        plan.append(("holder", [("holder", holder, COL["pla2"])] + vials, "9-position holder: DI water and 1 M HNO₃ only", "onhand"))
        st = PL.stir_module()
        stir = []
        for nm, y in zip(ds.STIR_NAMES, ds.STIR_Y):
            col = {"A": COL["asw"], "B": "#ece2b4", "C": "#e6d58a", "D": "#cfe0c8"}[nm]
            x = ds.STIR_X
            stir += [(f"s{nm}b", st["base"].translate((x, y, 0), inplace=False), "#3a3a3a"), (f"s{nm}f", st["fan"].translate((x, y, 0), inplace=False), "#555555"),
                     (f"s{nm}h", st["holder"].translate((x, y, 0), inplace=False), "#3a3a3a"),
                     (f"s{nm}g", vv["glass"].translate((x, y, ds.STIR_RIM - 57), inplace=False), COL["glass"]),
                     (f"s{nm}l", vv["liquid"].translate((x, y, ds.STIR_RIM - 57), inplace=False), col),
                     (f"s{nm}c", sh.vial_cap_mesh.translate((x, y, ds.STIR_RIM + 15 - 0.5), inplace=False), "#e3e1da")]
        plan.append(("stirrers", stir, "Four stir modules at x 76: ASW, ASW + 0.1 and + 10 mg/L S, spare", "onhand"))
        ez = PL.ezstat_box()
        ezm = [("ez", ez["body"].translate((-60, 300, 0), inplace=False), "#2f4a6b"), ("ezf", ez["face"].translate((-60, 300, 0), inplace=False), "#1b2b3e")]
        bel = PL.tube_path([(222.5, 268, 3), (222.5, 285, 4), (150, 300, 6), (40, 300, 8), (15, 300, 20)], PL.DIMS["belden9534"]["od"] / 2, 16)
        ezm.append(("bel", bel, COL["cable"]))
        plan.append(("ezstat", ezm, "EZstat-Pro (on loan) and the Belden cable to the tray", "onhand"))
        t = 2.4
        self.plan_t = []
        for grp, meshes, label, status in plan:
            for key, mesh, col in meshes:
                op = 0.35 if key.endswith("g") and key.startswith(("v", "s")) else 1.0
                o = self.add(f"mod:{grp}:{key}", mesh, col, opacity=op, specular=0.3, show=(t, 1e9))
                o.key(t, (0, 0, 40)).key(t + 0.7, (0, 0, 0))
            self.plan_t.append((t, grp, label, status))
            t += 1.35
        self.t_mods = t
        # the electrode cap: on the park cup, then carried to S1
        self.ecap = []
        for nm, stem, col in (("body", "electrode_cap", COL["pla"]), ("disc", "steel_disc", COL["steel"]), ("carrier", "electrode_carrier", "#d8d4ca"),
                              ("coil", "pt_coil", COL["pt"]), ("ref", "ag_agcl_ref", COL["peek"])):
            o = self.add(f"ecap:{nm}", load(CU_CAD / f"{stem}.stl"), col, specular=0.4, show=(t, 1e9))
            self.ecap.append(o)
        self.park = np.array((90.0, 245.0, 45.0))
        self.s1 = np.array((SX[0], SY, 26.0))
        self.t_cap = t
        # head path: park (236, 25, 122) -> over the park cup -> down -> up -> over S1 -> down -> up -> park
        hz = rcc.TRAVEL
        self.hp = [(0.0, (236, 25, hz)), (t + 0.8, (236, 25, hz)), (t + 2.6, (90, 245, hz)), (t + 3.4, (90, 245, 45 + 32)), (t + 4.0, (90, 245, 45 + 32)),
                   (t + 4.8, (90, 245, hz)), (t + 6.4, (SX[0], SY, hz)), (t + 7.2, (SX[0], SY, 26 + 32)), (t + 7.8, (SX[0], SY, 26 + 32)),
                   (t + 8.6, (SX[0], SY, hz)), (t + 10.0, (236, 25, hz))]
        self.t_pick, self.t_set = t + 3.4, t + 7.2
        self.hooks.append(self.move_head)
        self.dur = t + 10.0 + 6.5
        for i, (t0, grp, label, status) in enumerate(self.plan_t):
            t1 = self.plan_t[i + 1][0] if i + 1 < len(self.plan_t) else self.t_cap
            self.cards.append((t0 + 0.1, t1, label, status, [], ""))
        self.card(0.0, 2.4, "The CubXL, as it is", "onhand", ["Frame, gantry, and the head: electromagnetic capper, P20 pipette, camera."], "")
        self.card(self.t_cap, self.t_cap + 10.0, "The capper carries the cap like a vial cap", "printed",
                  ["Park cup → S1. On the lid, its two magnets clock it so the pins land on the pads; 180° also seats, and swaps RE and CE: set the index mark by hand at the park cup."], "")
        self.card(self.t_cap + 10.0, self.dur, "The current path", "ordered",
                  ["RE: EZstat-Pro → Belden → JST → bus → pad pin → brass pin → −x foil pad → CPG-37 → wire-wrap → leak-free reference.",
                   "CE: the same through the +x pad to the Pt coil.", "WE: the WE bus → the pin under the coupon."], "")
        self.cam(0.0, (180, 150, 40), 1050, -120, 38)
        self.cam(2.4, (180, 150, 30), 900, -110, 40)
        self.cam(self.t_mods, (180, 150, 30), 820, -95, 45)
        self.cam(self.t_cap + 1.5, (150, 225, 40), 440, -90, 58)
        self.cam(self.t_cap + 9.0, (165, 232, 30), 360, -96, 52)
        self.cam(self.t_cap + 10.6, (SX[0], SY, 30), 130, -110, 20)
        self.cam(self.dur, (SX[0], SY, 30), 120, -70, 22)
        # highlight the path
        hl0 = self.t_cap + 10.6
        for k in ("mod:ezstat:bel",):
            self.objs[k].hl.append((hl0, self.dur))
        for k in ("mod:stations:pads0", "ecap:ref", "ecap:coil"):
            self.objs[k].hl.append((hl0 + 1.0, self.dur))
        self.objs["mod:stations:lid0"].okeys.append((hl0 - 0.6, hl0, 1.0, 0.3))
        self.objs["mod:tray:tray"].okeys.append((hl0 - 0.6, hl0, 1.0, 0.3))
        self.objs["ecap:body"].okeys.append((hl0 - 0.6, hl0, 1.0, 0.3))
        self.cap(0, self.t_mods, "Everything goes on the deck in the positions of the stirrer layout (stirrers/README.md); re-jog each one")
        self.cap(self.t_mods, self.dur, "The capper sets the electrode cap on S1; the rest of a spot is in cubxl-cu-spot.mp4")

    def head_at(self, t):
        hp = self.hp
        if t <= hp[0][0]:
            return np.array(hp[0][1], float)
        for a, b in zip(hp, hp[1:]):
            if a[0] <= t <= b[0]:
                u = ease((t - a[0]) / max(b[0] - a[0], 1e-9))
                return np.array(a[1], float) + (np.array(b[1], float) - np.array(a[1], float)) * u
        return np.array(hp[-1][1], float)

    def move_head(self, pl, t):
        h = self.head_at(t)
        hx, hy, hz = h
        for k in self.head_keys:
            self.objs[k].actor.user_matrix = T(hx, hy, hz)
        for k in self.groups.get("gantry", []):
            self.objs[k].actor.user_matrix = T(0, hy, 0)
        for k in self.groups.get("xcar", []):
            self.objs[k].actor.user_matrix = T(hx, hy, 0)
        if t < self.t_pick:
            c = self.park
        elif t < self.t_set:
            c = h - (0, 0, 32.0)
        else:
            c = self.s1
        for o in self.ecap:
            o.actor.user_matrix = T(*c)


# ----------------------------------------------------------------------------------------- 2D cards
class Card2D(Shot):
    def setup(self, pl):
        pass

    def apply(self, pl, t):
        pass


class Title(Card2D):
    chapter = ""
    dur = 6.0

    def image(self, t):
        im = Image.new("RGB", (W, H), PAPER)
        d = ImageDraw.Draw(im, "RGBA")
        a = int(255 * min(1.0, t / 0.6, (self.dur - t) / 0.5))
        d.text((90, 150), "The corrosion setup, from the parts up", font=font(40, True), fill=INK + (a,))
        y = 220
        for line in wrap(d, "Every line of Ben's order list (9 Nov 2026), what still has to be ordered, the parts printed on the H2D, "
                            "and what the lab already has: laid out, then put together. Each bought part is drawn at the size its vendor "
                            "publishes, to catch parts that won't fit before they arrive.", font(21), W - 200):
            d.text((90, y), line, font=font(21), fill=INK2 + (a,))
            y += 31
        y += 20
        x = 90
        for s in ("ordered", "todo", "printed", "onhand"):
            x += chip(d, x, y, s, 14) + 14
        d.text((90, H - 90), "Nothing here has been built or tested. Positions follow the stirrer deck of 2026-11-06.", font=font(16), fill=MUTED + (a,))
        return np.asarray(im)


class Caught(Card2D):
    chapter = "11  what the model caught"
    dur = 14.0
    lines = []

    def image(self, t):
        im = Image.new("RGB", (W, H), PAPER)
        d = ImageDraw.Draw(im, "RGBA")
        topbar(d, self.chapter)
        d.text((60, 60), "Found by drawing each part at its catalogue size", font=font(28, True), fill=INK)
        y = 112
        for i, (head, body) in enumerate(self.lines):
            a = int(255 * min(1.0, max(0.0, (t - 0.4 - 0.5 * i) / 0.4)))
            d.text((60, y), f"{i + 1}.", font=font(17, True), fill=(200, 40, 30, a))
            d.text((88, y), head, font=font(17, True), fill=INK + (a,))
            y += 24
            for ln in wrap(d, body, font(15), W - 160):
                d.text((88, y), ln, font=font(15), fill=INK2 + (a,))
                y += 20
            y += 8
        return np.asarray(im)


CAUGHT = [
    ("The cap's CPG-37 pins need a different hole",
     "The BOM says open the holes to 1.3 mm and recess the flange 0.2 mm. The datasheet pin has a Ø2.00 flange and a Ø1.50 tail, and stands 2.20 mm free: "
     "that would bottom it out and hold the cap 1 mm off the lid. Cut a Ø2.1 counterbore 1.57 mm deep, then a Ø1.6 hole for the tail."),
    ("The P75-B1 pins are 16 mm long, not the CAD's 11 mm",
     "In the tray, each WE pin's tail ends 1 mm below the underside, so the tray stands on four pin tails: add 2 mm feet. "
     "In the bench cell the pin hangs 13 mm below the clamp plate: stand the cell on 15 mm feet."),
    ("A slice of a 1 in bar doesn't fit the 20.6 mm pockets",
     "C71500, C70600 and C95800 come as 1 in round. Mill four flats 20 mm across, or turn to Ø20, before polishing."),
    ("The sulfide test takes 25 mL; a deck stock is one 20 mL vial",
     "Test the bottle each vial is filled from, at the start and end of each sulfide night."),
    ("Graphite: yes for the bench cell, no for the cap (Edison c2-01)",
     "A commodity rod in the cap brings unstated Cu/Ni/Fe/Mn/Al, porosity and carry-over: keep the Pt coil. "
     "In the bench cell nothing sets the 10 mm rod's depth: hang it on a collar."),
    ("Smaller fits to try on the first print",
     "The O-ring is loose in its counterbore (6.46 in 7.30): set it on the coupon. Magnets are 4.00 ± 0.10 for Ø4.1 × 2.1 pockets. "
     "Brass rod is 1.588 for 1.6 holes. The Pt wire is hard temper: anneal it before winding."),
]


SHOTS = [Title, BoughtLong, BoughtSmall, NotYet, Print, Stock, Lid, Cap, Tray, Bench, Sulfide, Deck, Caught]
CAPPER_CAD = REPO / "modules" / "electromagnetic-capper" / "cad"


# ----------------------------------------------------------------------------------------- render
def render_shot(shot, sink, t_list):
    if isinstance(shot, Card2D):
        for t in t_list:
            sink(shot.image(t))
        return
    pv.global_theme.allow_empty_mesh = True
    pl = pv.Plotter(off_screen=True, window_size=(W, H), lighting="light_kit")
    pl.set_background(shot.bg)
    if shot.depth_peel:
        pl.enable_depth_peeling(number_of_peels=4)
    pl.enable_anti_aliasing("fxaa")
    shot.setup(pl)
    for t in t_list:
        shot.apply(pl, t)
        pl.render()
        img = pl.screenshot(return_img=True)
        if img.shape[0] != H or img.shape[1] != W:
            img = np.asarray(Image.fromarray(img).resize((W, H)))
        sink(overlay(shot, pl, t, img[:, :, :3]))
    pl.close()


def writer(path, fps=FPS):
    import imageio.v2 as imageio
    return imageio.get_writer(path, fps=fps, codec="libx264", quality=None, macro_block_size=1,
                              ffmpeg_params=["-crf", "20", "-pix_fmt", "yuv420p", "-preset", "medium"])


def main():
    global CAPPER_CAD
    ap = argparse.ArgumentParser()
    ap.add_argument("--capper-cad", type=Path, default=None)
    ap.add_argument("--part", default=None, help="i/n: render every n-th shot starting at i")
    ap.add_argument("--assemble", type=int, default=None)
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--only", default=None, help="comma-separated shot class names")
    ap.add_argument("--at", default=None, help="with --only: comma-separated times for stills")
    args = ap.parse_args()
    if args.capper_cad:
        CAPPER_CAD = args.capper_cad
    Caught.lines = CAUGHT
    if args.assemble:
        segs = [SEG / f"{i:02d}.mp4" for i in range(len(SHOTS))]
        lst = SEG / "list.txt"
        lst.write_text("".join(f"file '{s.name}'\n" for s in segs))
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(OUT)], check=True, cwd=SEG)
        make_gif()
        make_sheet(segs)
        return
    shots = [(i, S) for i, S in enumerate(SHOTS)]
    if args.only:
        names = args.only.split(",")
        shots = [(i, S) for i, S in shots if S.__name__ in names]
    if args.part:
        a, n = map(int, args.part.split("/"))
        # balance by duration: greedy over the shots, longest first
        est = sorted(((S.dur if S.dur else 10) * (1 if issubclass(S, Card2D) else 3), i) for i, S in shots)[::-1]
        bins = [[] for _ in range(n)]
        load_ = [0.0] * n
        for w_, i in est:
            j = int(np.argmin(load_))
            bins[j].append(i)
            load_[j] += w_
        shots = [(i, S) for i, S in shots if i in bins[a]]
    SEG.mkdir(exist_ok=True)
    for i, S in shots:
        shot = S()
        if args.stills or args.at:
            ts = [float(x) for x in args.at.split(",")] if args.at else [shot.dur * 0.62]
            for t in ts:
                frames = []
                render_shot(shot, frames.append, [t])
                (HERE / "_stills").mkdir(exist_ok=True)
                Image.fromarray(frames[0]).save(HERE / "_stills" / f"{i:02d}-{S.__name__.lower()}-{t:05.1f}.png")
            continue
        n = int(round(shot.dur * FPS))
        w_ = writer(SEG / f"{i:02d}.mp4")
        render_shot(shot, w_.append_data, [k / FPS for k in range(n)])
        w_.close()
        print(f"shot {i} {S.__name__}: {n} frames", flush=True)


SHEET_AT = {"BoughtLong": 0.93, "BoughtSmall": 0.93, "NotYet": 0.9, "Print": 0.4, "Stock": 0.95, "Lid": 0.75, "Cap": 0.62,
            "Tray": 0.85, "Bench": 0.93, "Sulfide": 0.9, "Deck": 0.97}


def make_sheet(segs):
    """One frame from each 3D chapter, 4 x 3, labelled; and chapters.json with the start times."""
    import imageio.v2 as imageio
    tiles, chapters, t = [], [], 0.0
    for S, seg in zip(SHOTS, segs):
        rd = imageio.get_reader(seg)
        n = rd.count_frames()
        chapters.append({"chapter": S.chapter or "title", "start_s": round(t, 1), "frames": n})
        t += n / FPS
        if S.__name__ in SHEET_AT:
            f = rd.get_data(int(n * SHEET_AT[S.__name__]) - 1)
            tiles.append((S.chapter, Image.fromarray(f).resize((480, 270), Image.LANCZOS)))
        rd.close()
    (HERE / "chapters.json").write_text(json.dumps({"total_s": round(t, 1), "fps": FPS, "chapters": chapters}, indent=1) + "\n")
    cols, pad, lab = 4, 8, 26
    rows = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * 480 + (cols + 1) * pad, rows * (270 + lab) + (rows + 1) * pad), PAPER)
    d = ImageDraw.Draw(sheet)
    for k, (ch, im) in enumerate(tiles):
        x = pad + (k % cols) * (480 + pad)
        y = pad + (k // cols) * (270 + lab + pad)
        d.text((x + 2, y + 4), ch.split("  ", 1)[0] + "  " + ch.split("  ", 1)[-1][:52], font=font(15, True), fill=INK)
        sheet.paste(im, (x, y + lab))
    sheet.save(HERE / "build-sheet.png", optimize=True)


def make_gif():
    """A GIF preview of chapter 6 (the electrode cap), 640 x 360 at 10 fps."""
    import imageio.v2 as imageio
    seg = SEG / f"{SHOTS.index(Cap):02d}.mp4"
    rd = imageio.get_reader(seg)
    frames = [np.asarray(Image.fromarray(f).resize((560, 315), Image.LANCZOS)) for k, f in enumerate(rd) if k % 3 == 0 and 15 <= k <= 750]
    imageio.mimsave(HERE / "build-cap.gif", frames, duration=100, loop=0)


if __name__ == "__main__":
    main()
