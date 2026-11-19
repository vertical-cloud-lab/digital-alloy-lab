"""Animated build of the low-profile desktop LPBF (lpbf_low.py, M50 module), from the parts as they arrive to the
finished machine on its VLM tray (issue #260, PR #266).

Chapters, each written as its own GIF, plus one MP4 of the whole run:
  1-kit        what arrives: stock for the machined parts, sheet for the welded parts, and the bought parts, by kind
  2-machining  the chamber body hogged out of a 6061-T6 block one operation at a time; the build module's spigot,
               flange and cylinder turned, cut and bored, TIG-welded and honed; the heater block, plate and piston
               head turned and drilled; then every other machined and sheet-metal part as one batch
  3-module     the heated build module: cartridges, thermocouples and cutoff into the block, Macor break and shields,
               piston head and seals, screws, the plate twisted onto its bayonet, the stack into the bore, the gland
               flange screwed on, rod end and striker
  4-process    the process module: base and feet, legs, chamber, plenums and overflow, Z stage, recoater (rail
               screws), the build module in along its swap path and its thumb screws, the lid on its O-ring with 20 M5
               screws in a star pattern, window stack, dosing and reservoir, door, optics bridge and scan head, guard
  5-tray       rack units in and screwed, the gas and vacuum module, hoses and lines, the tray dock; a closing orbit

What is drawn here and not in lpbf_low.py: stock blanks (part bounding box plus a machining allowance, rounded up to a
stock size), cutting tools, weld beads and most screws. The model has no fasteners except the lid screws and the
module's captive screws, so the other screws mark where a joint is bolted, not a drawn hole pattern.

Run (headless):  xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/cad/render_build.py [chapter ...] [--quick]
  chapter: kit machining module process tray (default: all).  --quick: a few frames per step, for checking views.
Writes desktop-lpbf/cad/img/build/<n>-<chapter>.gif and build.mp4.
"""
from __future__ import annotations

import math
import pathlib
import shutil
import subprocess
import sys
import time

import cadquery as cq
import numpy as np
import pyvista as pv
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lpbf_low as M  # noqa: E402
import module_params as MP  # noqa: E402
import render_low as R  # noqa: E402

pv.OFF_SCREEN = True
OUT = HERE / "img" / "build"
GW, GH = 880, 540
QUICK = "--quick" in sys.argv
INCH = 25.4
STOCK_COL = "#cfd4d9"      # mill-finish stock
SS_STOCK = "#b4bcc4"
TOOL_COL = "#d9b44a"       # TiN-coated cutter
HOLDER_COL = "#3a3f45"


def hexc(h):
    return R.hex2rgb(h) if isinstance(h, str) else h


def nf(n):
    """frames for a step (fewer with --quick)."""
    return max(2, n // 4) if QUICK else n


# ------------------------------------------------------------------ small matrix helpers
def T(v):
    m = np.eye(4)
    m[:3, 3] = v
    return m


def rot3(axis, deg):
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    t = math.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def Rax(axis, deg, c=(0, 0, 0)):
    m = np.eye(4)
    m[:3, :3] = rot3(axis, deg)
    c = np.asarray(c, float)
    m[:3, 3] = c - m[:3, :3] @ c
    return m


def align(n):
    """3x3 rotation taking +z to the unit vector n."""
    z = np.array([0.0, 0.0, 1.0])
    n = np.asarray(n, float) / np.linalg.norm(n)
    v, c = np.cross(z, n), float(np.dot(z, n))
    if np.linalg.norm(v) < 1e-9:
        return np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K / (1 + c)


def ease(t):
    return R.ease(t)


def bbox(shape):
    b = shape.BoundingBox()
    return np.array([b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax])


def up(v, step):
    return step * math.ceil(v / step - 1e-9)


# ------------------------------------------------------------------ meshes drawn here
def screw_template(d, L):
    k = d
    head = pv.Cylinder(center=(0, 0, k / 2), direction=(0, 0, 1), radius=0.75 * d, height=k, resolution=20)
    shank = pv.Cylinder(center=(0, 0, -L / 2), direction=(0, 0, 1), radius=0.48 * d, height=L, resolution=12)
    body = (head + shank).triangulate()
    hexp = pv.Polygon(center=(0, 0, k + 0.03), radius=0.38 * d, normal=(0, 0, 1), n_sides=6).triangulate()
    return body, hexp


def end_mill(d, flute=None, holder_d=None):
    """Tip at the origin, spindle along +z."""
    flute = flute or 2.5 * d
    hd = holder_d or max(28.0, 1.8 * d)
    m1 = pv.Cylinder(center=(0, 0, flute / 2), direction=(0, 0, 1), radius=d / 2, height=flute, resolution=20)
    m2 = pv.Cylinder(center=(0, 0, flute + 15), direction=(0, 0, 1), radius=d / 2 * 0.95, height=30, resolution=20)
    m3 = pv.Cone(center=(0, 0, flute + 42), direction=(0, 0, -1), height=24, radius=hd / 2, resolution=24)
    m4 = pv.Cylinder(center=(0, 0, flute + 70), direction=(0, 0, 1), radius=hd / 2, height=34, resolution=24)
    return [(m1, TOOL_COL), (m2, "#9aa3ab"), ((m3 + m4).triangulate(), HOLDER_COL)]


def drill(d, L=60.0):
    tip = pv.Cone(center=(0, 0, d * 0.3), direction=(0, 0, -1), height=d * 0.6, radius=d / 2, resolution=16)
    body = pv.Cylinder(center=(0, 0, d * 0.6 + L / 2), direction=(0, 0, 1), radius=d / 2, height=L, resolution=16)
    chuck = pv.Cylinder(center=(0, 0, d * 0.6 + L + 12), direction=(0, 0, 1), radius=max(9.0, d), height=24, resolution=20)
    return [((tip + body).triangulate(), TOOL_COL), (chuck, HOLDER_COL)]


def lathe_tool():
    """Insert tip at the origin, shank along +x."""
    ins = pv.Box((0, 10, -5, 5, -2, 2))
    shank = pv.Box((10, 90, -10, 10, -10, 10))
    return [(ins, TOOL_COL), (shank, HOLDER_COL)]


def arc_tube(r, z, phi_deg, rad=1.6, c=(0, 0, 0)):
    n = max(3, int(phi_deg / 6) + 2)
    th = np.radians(np.linspace(0, phi_deg, n))
    pts = np.c_[c[0] + r * np.cos(th), c[1] + r * np.sin(th), np.full(n, z)]
    return pv.Spline(pts, n * 2).tube(radius=rad, n_sides=10)


def coil(R_ring, r_tube, turns=1, pitch=0.0):
    n = 120 * max(1, int(turns))
    th = np.linspace(0, 2 * math.pi * turns, n)
    pts = np.c_[R_ring * np.cos(th), R_ring * np.sin(th), pitch * th / (2 * math.pi)]
    return pv.Spline(pts, n).tube(radius=r_tube, n_sides=12)


# ------------------------------------------------------------------ the stage
class Stage:
    """The model's parts (all added once, shown and moved per frame) plus extra meshes; a frame list."""

    def __init__(self, parts, size=(GW, GH)):
        self.parts = parts
        self.sc = R.Scene(parts, size)
        self.pl = self.sc.pl
        self.frames = []
        self.extra = {}
        self.shown = set()
        self.mat = {}
        self.opac = {}
        self.hidden = set()          # parts never drawn in this animation (replaced by drawn screws)

    def find(self, *keys, exclude=()):
        return [i for i, p in enumerate(self.parts) if any(k in p.name for k in keys) and not any(x in p.name for x in exclude)]

    def apply(self):
        for i, (a, e, s, p) in self.sc.actors.items():
            v = i in self.shown and i not in self.hidden
            m = self.mat.get(i, np.eye(4))
            op = self.opac.get(i, p.opacity)
            a.SetVisibility(v)
            a.user_matrix = m
            a.prop.opacity = op
            if e is not None:
                e.SetVisibility(v and op > 0.3)
                e.user_matrix = m
            if s is not None and s != "empty":
                s.SetVisibility(False)

    def add(self, key, mesh, color, opacity=1.0, edges=False, glow=False, **kw):
        self.remove(key)
        if mesh is None or mesh.n_points == 0:
            return
        props = dict(R.MAT)
        if glow:
            props.update(ambient=1.0, diffuse=0.0, specular=0.0)
        props.update(kw)
        acts = [self.pl.add_mesh(mesh, color=hexc(color), opacity=opacity, **props)]
        if edges:
            fe = mesh.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False, manifold_edges=False)
            if fe.n_points:
                acts.append(self.pl.add_mesh(fe, color=(0.12, 0.13, 0.15), line_width=1.0, opacity=0.45))
        self.extra[key] = acts

    def add_multi(self, key, pieces):
        """pieces: [(mesh, color)] drawn as one movable group."""
        self.remove(key)
        acts = []
        for mesh, col in pieces:
            acts.append(self.pl.add_mesh(mesh, color=hexc(col), **R.MAT))
        self.extra[key] = acts

    def remove(self, key):
        for a in self.extra.pop(key, []):
            self.pl.remove_actor(a)

    def clear_extra(self, prefix=""):
        for k in [k for k in self.extra if k.startswith(prefix)]:
            self.remove(k)

    def move(self, key, m):
        for a in self.extra.get(key, []):
            a.user_matrix = m

    def show_extra(self, key, v=True):
        for a in self.extra.get(key, []):
            a.SetVisibility(v)

    def caption(self, text, sub=""):
        self.pl.add_text(text, position="upper_left", font_size=11, color="#1d2733", name="title", font="arial")
        self.pl.add_text(sub or " ", position="lower_left", font_size=10, color="#46535f", name="sub", font="arial")

    def cam(self, focal, dist, az, el):
        self.sc.cam(R.orbit(focal, dist, az, el), focal)

    def shot(self, n=1):
        self.apply()
        img = self.sc.shot()
        for _ in range(n):
            self.frames.append(img)


class Screws:
    """A set of screws that drive in along their axes, spinning, one after another."""

    def __init__(self, st, key, items, d, L, color="#a9b1b9", order=None):
        body, hexp = screw_template(d, L)
        self.st, self.d, self.L = st, d, L
        self.items = []
        for j, (P, n) in enumerate(items):
            a = st.pl.add_mesh(body, color=hexc(color), **R.MAT)
            h = st.pl.add_mesh(hexp, color=(0.08, 0.08, 0.09), ambient=0.4)
            self.items.append((a, h, np.asarray(P, float), np.asarray(n, float) / np.linalg.norm(n)))
        self.order = order or list(range(len(self.items)))
        self.last = [np.eye(4)] * len(self.items)
        st.extra[key] = [x for it in self.items for x in it[:2]]
        self.set_all(0.0, visible=False)

    def set_one(self, j, u, visible=True):
        a, h, P, n = self.items[j]
        if u < 0.3:                      # approach along the axis, no spin
            off, spin = self.L + 40.0 * (1 - u / 0.3), 0.0
        else:
            w = (u - 0.3) / 0.7
            off, spin = self.L * (1 - w), 330.0 * w
        m = np.eye(4)
        m[:3, :3] = align(n) @ rot3((0, 0, 1), spin)
        m[:3, 3] = P + n * off
        self.last[j] = m
        for x in (a, h):
            x.user_matrix = m
            x.SetVisibility(visible)

    def shift(self, m):
        """Move every (seated) screw by m, e.g. with the sub-assembly they hold."""
        for j, (a, h, P, n) in enumerate(self.items):
            for x in (a, h):
                x.user_matrix = m @ self.last[j]

    def set_all(self, u, visible=True):
        for j in range(len(self.items)):
            self.set_one(j, u, visible)

    def drive(self, frames_each=6, overlap=0.5, shoot=None):
        """Drive every screw in `order`; shoot() renders one frame. Screws start `overlap` of a screw apart."""
        n = len(self.order)
        stride = max(1, int(round(frames_each * (1 - overlap))))
        total = stride * (n - 1) + frames_each
        if QUICK:
            total = min(total, 4)
        for f in range(total):
            for k, j in enumerate(self.order):
                if QUICK:
                    u = (f + 1) / total
                else:
                    u = (f + 1 - k * stride) / frames_each
                if u <= 0:
                    self.set_one(j, 0.0, visible=False)
                else:
                    self.set_one(j, min(u, 1.0))
            shoot()


def star_order(points):
    """Indices of bolts around a ring in a star (cross) tightening pattern: each next bolt opposite the last."""
    c = np.mean(points, axis=0)
    ang = [math.atan2(p[1] - c[1], p[0] - c[0]) for p in points]
    ring = list(np.argsort(ang))
    n = len(ring)
    order, used = [], set()
    step = [0, n // 2, n // 4, 3 * n // 4, n // 8, 5 * n // 8, 3 * n // 8, 7 * n // 8]
    for base in range(n):
        for s in step:
            k = (base + s) % n
            if k not in used:
                used.add(k)
                order.append(int(ring[k]))
    return order[:n]


# ------------------------------------------------------------------ classification and stock
def kind(p):
    """'stock' (machined from bar, block or plate), 'sheet' (cut, bent and welded), 'bought', 'context' or 'skip'."""
    n = p.name
    if "context" in p.tags:
        return "context"
    if any(k in n for k in ("Lid screws", "Captive M6")):
        return "skip"
    sheet_keys = ("plenum", "liners", "Dose chute", "Gas knife", "Reservoir M (", "Reservoir M shutter", "Radiation shields",
                  "Laser guard panels", "Sliding guard door", "Rack side panels", "Umbilical duct", "Operator panel box",
                  "Overflow funnel")
    if any(k in n for k in sheet_keys):
        return "sheet"
    if p.mat in ("al6061", "mic6", "macor") and not p.mcm.startswith(("KF", "9572", "TSLOT", "SHEET")):
        return "stock"
    if p.mat == "ss316l" and any(k in n for k in ("Build module", "bottom flange", "Rod end", "Hollow piston rod", "dowel")):
        return "stock"
    if "Striker" in n or "Hinge pins" in n:
        return "stock"
    return "bought"


ROUND_KEYS = ("Build plate", "Heater block", "Piston head", "Window flange", "Window retaining", "Field-stop", "Hollow piston rod",
              "Rod end", "Striker", "bottom flange", "Macor", "Recoater floating bearing", "Recoater fixed bearing",
              "Recoater motor standoff", "Roller shaft seal", "Hinge pins", "dowel")


def stock_blank(p):
    """(cq shape, label) for the stock a part is machined from (one blank per solid of a compound)."""
    sols = p.shape.Solids()
    if len(sols) > 1:
        bl = [_blank(s, p.name) for s in sols]
        return M.comp([b for b, _ in bl]), bl[0][1]
    return _blank(p.shape, p.name)


def _blank(shape, name):
    class _P:
        pass
    p = _P()
    p.shape, p.name = shape, name
    b = bbox(p.shape)
    dx, dy, dz = b[1] - b[0], b[3] - b[2], b[5] - b[4]
    c = ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2)
    if any(k in p.name for k in ROUND_KEYS):
        # axis = the longest-symmetric direction: these parts are all turned about z, except bearing housings (x)
        if any(k in p.name for k in ("Recoater floating", "Recoater fixed", "Recoater motor standoff", "Hinge pins")):
            D = up(max(dy, dz) + 3.0, INCH / 8)
            L = dx + 4.0
            s = M.cyl(D / 2, (b[0] - 2.0, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2), "x", L)
            return s, f"Ø{D / INCH:.3g} in. bar"
        D = up(max(dx, dy) + 3.0, INCH / 8)
        L = dz + 4.0
        s = M.cyl(D / 2, (c[0], c[1], b[4] - 2.0), "z", L)
        return s, f"Ø{D / INCH:.3g} in. bar"
    t = min(dx, dy, dz)
    # plate: thinnest dimension rounded up to a stock thickness, the others get a saw allowance
    thick = [x * INCH for x in (0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0)]
    tt = next((x for x in thick if x >= t + 1.5), t + 3.0)
    ext = [dx + 6.0, dy + 6.0, dz + 6.0]
    k = int(np.argmin([dx, dy, dz]))
    ext[k] = tt
    lo = [b[0] - (ext[0] - dx) / 2, b[2] - (ext[1] - dy) / 2, b[4] - (ext[2] - dz) / 2]
    s = M.box(lo[0], lo[0] + ext[0], lo[1], lo[1] + ext[1], lo[2], lo[2] + ext[2])
    return s, f"{tt / INCH:.3g} in. plate"


def sheet_blank(p):
    b = bbox(p.shape)
    dx, dy, dz = b[1] - b[0], b[3] - b[2], b[5] - b[4]
    area = max(p.shape.Area() / 2.0, 1.0)
    w = math.sqrt(area * max(dx, dy) / max(min(dx, dy), 1.0))
    h = area / w
    cx, cy = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2
    return M.box(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, b[4], b[4] + 1.5)


def tess(shape, tol=0.4):
    try:
        return R.tess(shape, tol, 0.4)
    except Exception:
        return None


def halfspace_keep(R_shape, axis, s):
    """The part of the removed volume the tool has not reached yet, when it has gone fraction s along axis."""
    b = bbox(R_shape)
    pad = 2.0
    lo, hi = b[0::2] - pad, b[1::2] + pad
    k = "xyz".index(axis[-1])
    sign = -1 if axis[0] == "-" else 1
    if sign < 0:   # tool moves toward -axis from the top: keep below the cut level
        cut = b[2 * k + 1] - s * (b[2 * k + 1] - b[2 * k])
        hi = hi.copy()
        hi[k] = cut
    else:
        cut = b[2 * k] + s * (b[2 * k + 1] - b[2 * k])
        lo = lo.copy()
        lo[k] = cut
    if hi[k] - lo[k] < 1e-3:
        return None, cut
    keep = M.box(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
    try:
        return R_shape.intersect(keep), cut
    except Exception:
        return None, cut


def zigzag(f, b, axis):
    """A raster position over the removed volume's footprint for frame f."""
    u = (f * 0.29) % 1.0
    v = (f * 0.113) % 1.0
    tri = lambda x: 1 - abs(2 * x - 1)  # noqa: E731
    k = "xyz".index(axis[-1])
    others = [i for i in range(3) if i != k]
    pos = np.zeros(3)
    for i, w in zip(others, (tri(u), tri(v))):
        lo, hi = b[2 * i], b[2 * i + 1]
        m = min(6.0, (hi - lo) / 4)
        pos[i] = lo + m + w * (hi - lo - 2 * m)
    return pos, k


def machine_op(st, key, before, after, axis, tool, frames, color, caption, sub, cam, spin=None, tool_offset=0.0):
    """Animate one operation: `before` -> `after` (cq shapes); the removed volume shrinks along `axis` while a tool
    rides the cut. tool: 'mill' (end mill along the cut axis), 'drill', 'lathe', 'jet' or None. spin: rotate everything
    about the z axis through (x, y) = spin (a lathe)."""
    removed = None
    try:
        removed = before.cut(after)
    except Exception:
        pass
    am = tess(after)
    st.add(key, am, color, edges=True)
    rb = bbox(removed) if removed is not None else bbox(before)
    tool_pieces = None
    if tool == "mill":
        d = float(np.clip(min(rb[1] - rb[0], rb[3] - rb[2], rb[5] - rb[4]) * 0.5, 3.0, 16.0))
        tool_pieces = end_mill(d)
    elif tool == "drill":
        tool_pieces = drill(5.0)
    elif tool == "lathe":
        tool_pieces = lathe_tool()
    elif tool == "jet":
        tool_pieces = [(pv.Cylinder(center=(0, 0, 40), direction=(0, 0, 1), radius=6, height=80), HOLDER_COL),
                       (pv.Line((0, 0, 0), (0, 0, -30)).tube(radius=0.8), "#7fd3ff")]
    if tool_pieces:
        st.add_multi(key + "-tool", tool_pieces)
    st.caption(caption, sub)
    for f in range(frames):
        s = ease((f + 1) / frames)
        rest, cut = (None, 0.0)
        if removed is not None and s < 1.0:
            rest, cut = halfspace_keep(removed, axis, s)
        st.add(key + "-rest", tess(rest) if rest is not None else None, STOCK_COL if color != SS_STOCK else SS_STOCK)
        if tool_pieces:
            pos, k = zigzag(f, rb, axis)
            done = s >= 1.0
            pos[k] = cut if not done else (rb[2 * k + 1] + 30 if axis[0] == "-" else rb[2 * k] - 30)
            if tool == "lathe":
                m = T((rb[1] + 0.5, (rb[2] + rb[3]) / 2, cut if not done else rb[5] + 20))
            elif tool == "jet":
                pos[2] = rb[5] + 3.0
                m = T(pos)
            else:
                n = np.zeros(3)
                n[k] = 1.0 if axis[0] == "-" else -1.0     # spindle points away from the material
                m = np.eye(4)
                m[:3, :3] = align(n)
                m[:3, 3] = pos + n * tool_offset
            st.move(key + "-tool", m)
        if spin is not None:
            mr = Rax((0, 0, 1), 47.0 * f, (spin[0], spin[1], 0))
            st.move(key, mr)
            st.move(key + "-rest", mr)
        cam(f / max(1, frames - 1))
        st.shot()
    st.remove(key + "-rest")
    st.remove(key + "-tool")
    if spin is not None:
        st.move(key, np.eye(4))
    return am


# ------------------------------------------------------------------ chapter 1: what arrives
CATS = [
    ("stock", "Stock to machine: 6061-T6 and MIC-6 plate and bar, 316 bar, tube and plate, Macor rod"),
    ("sheet", "Sheet to cut, bend and TIG-weld: 304 / 316L sheet and shim, 5052 guard panels"),
    ("motion", "Motion: rails, ball screws, servos, stepper, Z actuator, magnet, hinges, latches"),
    ("gas", "Vacuum and gas: KF fittings, clamps, valves, hoses, pump, blower, filter, O2 / dew point, argon"),
    ("optics", "Laser and optics: 500 W fiber laser, galvo, f-theta lens, collimator, shutter, windows, fiber"),
    ("elec", "Electronics, heaters and sensors: UPS, PC, DIN drawer, cartridges, thermocouples, sensors, camera"),
    ("seal", "Seals and fasteners: FKM O-rings and cord, felt and PTFE seals, screws"),
    ("frame", "Frames: 10U rack, T-slot guard frame, levelling mounts"),
]


def kit_cat(p, k):
    n = p.name
    if k in ("stock",):
        return "stock"
    if k == "sheet":
        return "sheet"
    if any(x in n for x in ("rack frame", "Guard frame", "Leveling", "Guard door rail")):
        return "frame"
    if p.mat == "fkm" or any(x in n for x in ("O-ring", "Bore seal", "wiper", "Locating dowel")):
        return "seal"
    if any(x in n for x in ("laser source", "galvo", "f-theta", "Collimator", "shutter", "window", "Cover slide", "fiber",
                            "OD 7+", "Enclosed beam")):
        return "optics"
    if any(x in n for x in ("rail", "carriage", "ball screw", "ball nut", "servo", "stepper", "Z actuator", "Pot magnet",
                            "Hinge", "hinge", "latch", "Draw-latch", "Z carriage", "blade")):
        return "motion"
    if any(x in n for x in ("KF", "Overflow jar", "pump", "blower", "HEPA", "O2", "Argon", "valve", "hoses", "line",
                            "Pressure transducer", "relief", "Overflow clamp", "exhaust", "Chilled")):
        return "gas"
    return "elec"


def kit_layout(st, z0=0.0):
    """Lay every part (or its stock / sheet blank / a coil for hoses) out on the floor, packed by category.
    Returns {part index: offset 4x4} for parts drawn as themselves, and the extra meshes it added."""
    items = {c: [] for c, _ in CATS}
    for i, p in enumerate(st.parts):
        k = kind(p)
        if k in ("context", "skip"):
            continue
        c = kit_cat(p, k)
        b = bbox(p.shape)
        long_thin = any(x in p.name for x in ("hoses", "Argon line", "O2 sample", "Process fiber", "Chilled-water", "Argon supply",
                                              "Pump exhaust"))
        if long_thin:
            r = 13.0 if "hoses" in p.name else 6.0 if "Chilled" in p.name else 4.0 if "fiber" in p.name else 3.2
            ring = 150.0 if r > 5 else 110.0
            mesh = coil(ring, r, turns=3, pitch=2.2 * r)
            mb = np.array(mesh.bounds)
            items[c].append(dict(i=i, mesh=mesh, color=p.color, b=mb, what="coil"))
            continue
        if k == "stock":
            s, lab = stock_blank(p)
            items[c].append(dict(i=i, shape=s, color=SS_STOCK if p.mat == "ss316l" or "Striker" in p.name else STOCK_COL,
                                 b=bbox(s), what="stock", label=lab))
        elif k == "sheet":
            s = sheet_blank(p)
            items[c].append(dict(i=i, shape=s, color=SS_STOCK if p.mat.startswith("ss") else STOCK_COL, b=bbox(s), what="sheet"))
        else:
            items[c].append(dict(i=i, b=b, what="part"))
    # pack each category into a zone (shelves), then the zones into rows
    gap = 25.0
    zones = []
    for c, title in CATS:
        its = sorted(items[c], key=lambda it: -(it["b"][3] - it["b"][2]))
        Wz = 1250.0 if c in ("stock", "frame", "gas") else 950.0
        x = y = 0.0
        row_h = 0.0
        for it in its:
            w, h = it["b"][1] - it["b"][0], it["b"][3] - it["b"][2]
            if x > 0 and x + w > Wz:
                x, y = 0.0, y + row_h + gap
                row_h = 0.0
            it["at"] = (x, y)
            x += w + gap
            row_h = max(row_h, h)
        zw = max([it["at"][0] + it["b"][1] - it["b"][0] for it in its] + [200.0])
        zh = y + row_h
        zones.append(dict(c=c, title=title, items=its, w=zw, h=zh))
    # zones in rows across ~4.6 m
    X = Y = 0.0
    rowh = 0.0
    for z in zones:
        if X > 0 and X + z["w"] > 4600.0:
            X, Y = 0.0, Y + rowh + 260.0
            rowh = 0.0
        z["at"] = (X, Y)
        X += z["w"] + 260.0
        rowh = max(rowh, z["h"])
    total_w = max(z["at"][0] + z["w"] for z in zones)
    total_h = max(z["at"][1] + z["h"] for z in zones)
    offs, labels = {}, []
    x_shift, y_shift = -total_w / 2, -total_h / 2
    for z in zones:
        zx, zy = z["at"][0] + x_shift, z["at"][1] + y_shift
        # y grows toward the back: put the first row at the front
        for it in z["items"]:
            tx, ty = zx + it["at"][0], zy + it["at"][1]
            b = it["b"]
            d = np.array([tx - b[0], ty - b[2], z0 - b[4]])
            it["off"] = d
            if it["what"] == "part":
                offs[it["i"]] = T(d)
        labels.append(((zx, zy - 60.0, z0 + 5.0), z["title"].split(":")[0]))
    return zones, offs, labels, (total_w, total_h)


def chapter_kit(st):
    st.shown.clear()
    st.mat.clear()
    zones, offs, labels, (tw, th) = kit_layout(st)
    print(f"kit layout {tw:.0f} x {th:.0f} mm")
    floor = pv.Plane(center=(0, 0, -1.0), direction=(0, 0, 1), i_size=tw + 900, j_size=th + 900)
    st.add("kit-floor", floor, "#e9edf1", ambient=0.5)
    for z in zones:
        for it in z["items"]:
            if it["what"] == "part":
                continue
            mesh = it.get("mesh")
            if mesh is None:
                mesh = tess(it["shape"])
            if mesh is None:
                continue
            mesh = mesh.translate(it["off"], inplace=False)
            st.add(f"kit-{it['i']}", mesh, it["color"], edges=it["what"] != "coil")
            st.show_extra(f"kit-{it['i']}", False)
    focal = (0.0, 0.0, 0.0)
    dist = 1.15 * max(tw / 0.873, th / 0.536)
    shown_extra = []
    for zi, z in enumerate(zones):
        for it in z["items"]:
            if it["what"] == "part":
                st.shown.add(it["i"])
                st.mat[it["i"]] = offs[it["i"]]
            else:
                shown_extra.append(f"kit-{it['i']}")
                st.show_extra(f"kit-{it['i']}", True)
        lab = labels[zi]
        st.pl.add_point_labels([lab[0]], [lab[1]], font_size=13, text_color="#1d2733", shape=None, show_points=False,
                               always_visible=True, name=f"kitlab{zi}")
        st.caption("1  What arrives: stock, sheet and bought parts for one machine (M50 module)", z["title"])
        st.cam(focal, dist, 4 + zi * 0.5, 62)
        st.shot(1 if QUICK else 4)
    for f in range(nf(28)):
        t = f / max(1, nf(28) - 1)
        st.caption("1  What arrives: stock, sheet and bought parts for one machine (M50 module)",
                   "Grey blocks and bars are stock for the custom parts; everything else arrives finished")
        st.cam(focal, dist * (1 - 0.25 * ease(t)), 8 + 20 * ease(t), 62 - 18 * ease(t))
        st.shot()
    for zi in range(len(zones)):
        st.pl.remove_actor(f"kitlab{zi}")
    st.clear_extra("kit-")
    st.shown.clear()
    st.mat.clear()


# ------------------------------------------------------------------ chapter 2: machining
def chamber_ops():
    P = M.P
    ix, iy, cx, cy, fl, lz0 = P["ix"], P["iy"], P["cx"], P["cy"], P["floor"], P["lid_z0"]
    box, cyl, rbox = M.box, M.cyl, M.rbox
    stock = box(-165.1, 165.1, -120.65, 120.65, -fl - 6.2, lz0 + 6.2)        # 13 x 9.5 x 6 in. 6061-T6 block
    s1 = rbox(-cx, cx, -cy, cy, -fl, lz0, 8)
    pocket = cq.Workplane("XY").box(2 * ix, 2 * iy, lz0 + 1, centered=False).edges("|Z").fillet(5.0).edges("<Z").fillet(5.0).val()
    s2 = s1.cut(pocket.translate(cq.Vector(-ix, -iy, 0)))
    s3 = s2.cut(box(-110, 110, -cy - 1, -iy + 1, 8.0, 100.0)).cut(box(-MP.INLET_HALF, MP.INLET_HALF, iy - 1, cy + 1, 4, 12))
    f = s3.cut(box(-MP.OUTLET_HALF, MP.OUTLET_HALF, MP.OUTLET_Y[0], MP.OUTLET_Y[1], -fl - 1, 1))
    f = f.cut(cyl(P["port_d"] / 2, (0, 0, -fl - 1), "z", fl + 2))
    for sx in (-1, 1):
        f = f.cut(cyl(3.0, (sx * MP.SCREW_X, 0, -fl - 1), "z", 13.0)).cut(cyl(3.0, (0, sx * MP.DOWEL_Y, -fl - 1), "z", 11.0))
    s4 = f.cut(box(P["ovf_x0"], P["ovf_x1"], -52, 52, -fl - 1, 1))
    g = s4
    for sx in (-1, 1):
        g = g.cut(cyl(1.6, (sx * (ix - 1), 0, 5.0), "x" if sx > 0 else "-x", P["wall"] + 2))
    ry_, rz_ = P["rc_screw_y"], P["rc_screw_z"]
    g = g.cut(cyl(9, (-cx - 1, ry_, rz_), "x", P["wall"] + 2)).cut(cyl(9, (ix - 1, ry_, rz_), "x", P["wall"] + 2))
    g = g.cut(cyl(12.7, (ix - 1, 0, 70), "x", P["wall"] + 2)).cut(cyl(3.2, (100, iy - 1, 100), "y", P["wall"] + 2))
    s5 = g.cut(cyl(3.2, (ix - 1, -40, 18), "x", P["wall"] + 2))
    gw, gd = P["gland_w"], P["gland_d"]
    s6 = s5.cut(rbox(-ix - 3 - gw, ix + 3 + gw, -iy - 3 - gw, iy + 3 + gw, lz0 - gd, lz0 + 1, 6).cut(
        rbox(-ix - 3, ix + 3, -iy - 3, iy + 3, lz0 - gd - 1, lz0 + 2, 4)))
    return [
        (stock, s1, "-z", "mill", "Face and square the block to 312 x 222 x 140 mm, 8 mm corners"),
        (s1, s2, "-z", "mill", "Rough and finish the 280 x 190 x 120 mm pocket: 5 mm corners, 5 mm coves at the floor"),
        (s2, s3, "+y", "mill", "Flip to the front: 220 x 92 mm door opening; from the back, the 120 x 8 mm cross-flow inlet slot"),
        (s3, s4, "+z", "mill", "Flip over: Ø96 module port, outlet and overflow slots, dowel and insert holes in the floor"),
        (s4, s5, "+x", None, "Side bores: recoater screw, KF-25 vacuum port, argon and O2 ports, through-beam fibres"),
        (s5, s6, "-z", "mill", "Lid O-ring face gland, 4.6 x 2.65 mm (Parker), on the top face"),
    ]


def chapter_machining(st):
    st.shown.clear()
    st.mat.clear()
    table = pv.Box((-420, 420, -260, 260, -60, -26))
    # --- the chamber body, op by op ---
    ops = chamber_ops()
    final = st.parts[st.find("Process chamber body")[0]].shape
    try:
        dv = abs(ops[-1][1].Volume() - final.Volume()) / final.Volume()
        print(f"chamber ops reproduce the model's body to {100 * dv:.3f} % in volume")
    except Exception:
        pass
    st.add("table", table, "#59626b")
    stock_mesh = tess(ops[0][0])
    st.add("chamber", stock_mesh, STOCK_COL, edges=True)
    focal = (0.0, 0.0, 60.0)
    st.caption("2  Machining: the process chamber body from one block of 6061-T6",
               "Stock: 13 x 9.5 x 6 in. 6061-T6 block (or a welded 5/8 in. plate box, finish-machined)")
    for f in range(nf(10)):
        st.cam(focal, 1150, -30 + f, 26)
        st.shot()
    cams = {"-z": (-28, 30), "+y": (-12, 8), "+z": (-30, -32), "+x": (62, 12)}
    az0 = -18
    for k, (before, after, axis, tool, cap) in enumerate(ops):
        az, el = cams[axis]
        def cam(t, az=az, el=el):
            st.cam(focal, 1050, az + 10 * t, el)
        st.show_extra("table", axis != "+z")       # seen from below for the floor op
        machine_op(st, "chamber", before, after, axis, tool, nf(14), STOCK_COL,
                   "2  Machining: the process chamber body from one block of 6061-T6", f"Op {k + 1}/{len(ops)}: {cap}", cam)
        st.show_extra("table", True)
    st.caption("2  Machining: the process chamber body from one block of 6061-T6",
               "Bead-blast, no anodize inside (anodized Al outgasses 41-68x more water); 6.4 L inside")
    for f in range(nf(12)):
        st.cam(focal, 1050, az0 + 3 * f, 22)
        st.shot()
    st.remove("chamber")
    st.remove("table")

    # --- the build module body: spigot from bar, flange from plate, cylinder from tube; TIG-weld; hone ---
    body = st.parts[st.find("Build module M50")[0]].shape
    zf = -MP.FLOOR_T
    zfb = zf - MP.FLANGE_T
    big = 300.0
    spig = body.intersect(M.box(-big, big, -big, big, zf, 1.0))
    flange = body.intersect(M.box(-big, big, -big, big, zfb, zf))
    tube = body.intersect(M.box(-big, big, -big, big, -400, zfb))
    tb = bbox(tube)
    spig_stock = M.cyl(2 * INCH, (0, 0, zf - 3.0), "z", MP.FLOOR_T + 6.0)                       # 4 in. 316 bar (9260K5)
    fl_stock = M.box(-70, 70, -62, 62, zfb, zfb + 0.5 * INCH)                                  # 1/2 in. 316 plate
    tube_stock = M.tube(2.25 * INCH / 2, 2.25 * INCH / 2 - 0.25 * INCH, (0, 0, tb[4] - 4.0), "z", tb[5] - tb[4] + 4.0)
    sep = {"spig": np.array([0, 0, 140.0]), "flange": np.array([0, 0, 60.0]), "tube": np.array([0, 0, -40.0])}
    focal = (0.0, 0.0, -10.0)
    cap0 = "2  Machining: the M50 build module's spigot, flange and cylinder (316L)"
    st.caption(cap0, "Stock: 4 in. 316 bar (McMaster 9260K5), 1/2 in. 316 plate, 2-1/4 x 1/4 in. 316 tube (11119N55)")
    st.add("m-spig", tess(spig_stock).translate(sep["spig"], inplace=False), SS_STOCK, edges=True)
    st.add("m-fl", tess(fl_stock).translate(sep["flange"], inplace=False), SS_STOCK, edges=True)
    st.add("m-tube", tess(tube_stock).translate(sep["tube"], inplace=False), SS_STOCK, edges=True)
    for f in range(nf(8)):
        st.cam(focal + np.array([0, 0, 40]), 820, -30, 22)
        st.shot()
    st.remove("m-spig")

    def camf(t):
        st.cam(focal + np.array([0, 0, 40]), 820, -30 + 8 * t, 22)

    def shifted(shape, v):
        return shape.translate(cq.Vector(*v))

    machine_op(st, "m-spig", shifted(spig_stock, sep["spig"]), shifted(spig, sep["spig"]), "-z", "lathe", nf(12), SS_STOCK,
               cap0, "Lathe: turn the spigot from the bar: Ø95.8 OD with its O-ring groove, Ø50.8 bore (rough), faces", camf, spin=(0, 0))
    st.add("m-spig", tess(shifted(spig, sep["spig"])), "#a2abb3", edges=True)
    st.remove("m-fl")
    machine_op(st, "m-fl", shifted(fl_stock, sep["flange"]), shifted(flange, sep["flange"]), "+x", "jet", nf(10), SS_STOCK,
               cap0, "Waterjet the Ø100 flange with its two screw tabs and dowel lugs; ream the dowel holes", camf)
    st.add("m-fl", tess(shifted(flange, sep["flange"])), "#a2abb3", edges=True)
    st.remove("m-tube")
    machine_op(st, "m-tube", shifted(tube_stock, sep["tube"]), shifted(tube, sep["tube"]), "-z", "lathe", nf(12), SS_STOCK,
               cap0, "Lathe: bore the tube from 1.75 to ~50.5 mm and turn the OD to 56.8 mm (3 mm wall)", camf, spin=(0, 0))
    st.add("m-tube", tess(shifted(tube, sep["tube"])), "#a2abb3", edges=True)
    # stack
    for f in range(nf(8)):
        t = ease((f + 1) / nf(8))
        st.move("m-spig", T(-sep["spig"] * t))
        st.move("m-fl", T(-sep["flange"] * t))
        st.move("m-tube", T(-sep["tube"] * t))
        st.caption(cap0, "Stack on a fixture: spigot, flange and tube on one mandrel so the bores line up")
        camf(0.5)
        st.shot()
    # weld: two circumferential seams
    seams = [(28.6, zfb - 0.2), (48.2, zf - 0.2)]     # tube OD under the flange; spigot OD on the flange
    torch = [(pv.Cylinder(center=(0, 0, 45), direction=(0, 0, 1), radius=7, height=60), HOLDER_COL),
             (pv.Cone(center=(0, 0, 8), direction=(0, 0, -1), height=16, radius=7), "#c96f2a")]
    st.add_multi("torch", torch)
    nw = nf(16)
    for f in range(nw):
        t = (f + 1) / nw
        for j, (r, z) in enumerate(seams):
            phi = float(np.clip(t * 2 - j, 0, 1)) * 360.0
            if phi > 0:
                st.add(f"weld{j}", arc_tube(r, z, phi, 1.5), "#ff9a3c", glow=(phi < 360))
                if phi < 360:
                    a = math.radians(phi)
                    m = np.eye(4)
                    m[:3, :3] = align((math.cos(a) * 0.6, math.sin(a) * 0.6, 0.8))
                    m[:3, 3] = (r * math.cos(a), r * math.sin(a), z)
                    st.move("torch", m)
        st.caption(cap0, "TIG-weld the flange to the tube and the spigot to the flange (316L filler), then stress-relieve")
        camf(0.5 + 0.2 * t)
        st.shot()
    st.remove("torch")
    for j in range(2):
        st.add(f"weld{j}", arc_tube(seams[j][0], seams[j][1], 360.0, 1.5), "#8f8a80")
    # hone
    hone = [(pv.Cylinder(center=(0, 0, 0), direction=(0, 0, 1), radius=24.8, height=30, resolution=24), "#6b5b45"),
            (pv.Cylinder(center=(0, 0, 120), direction=(0, 0, 1), radius=6, height=210), HOLDER_COL)]
    st.add_multi("hone", hone)
    for a in st.extra.get("m-tube", []) + st.extra.get("m-spig", []) + st.extra.get("m-fl", []):
        a.prop.opacity = 0.45
    zb = bbox(body)
    nh = nf(16)
    for f in range(nh):
        z = zb[5] - 15 - (zb[5] - zb[4] - 30) * (0.5 - 0.5 * math.cos(f / nh * 4 * math.pi))
        st.move("hone", Rax((0, 0, 1), 37 * f) @ T((0, 0, z)))
        st.caption(cap0, "Hone the bore after welding: Ø50.80 H7, Ra <= 0.4 µm, so the plate keeps its 0.15 mm gap")
        camf(0.7)
        st.shot()
    st.remove("hone")
    for k in ("m-spig", "m-fl", "m-tube", "weld0", "weld1"):
        st.remove(k)

    # --- heater block, plate and piston head: turn then drill, side by side ---
    names = [("Heater block M50", -110.0), ("Build plate M50", 0.0), ("Piston head M50", 110.0)]
    cap1 = "2  Machining: heater block, build plate and piston head (6061-T6 from 2-1/4 in. bar)"
    shapes = []
    for nm, x in names:
        p = st.parts[st.find(nm)[0]]
        b = bbox(p.shape)
        sh = p.shape.translate(cq.Vector(x, 0, -(b[4] + b[5]) / 2))
        bb = bbox(sh)
        stock = M.cyl(2.25 * INCH / 2, (x, 0, bb[4] - 2.5), "z", bb[5] - bb[4] + 5.0)
        env = M.cyl((bb[1] - bb[0]) / 2, (x, 0, bb[4]), "z", bb[5] - bb[4])
        shapes.append((nm, x, sh, stock, env))
    focal = (0.0, 0.0, 0.0)

    def camh(t):
        st.cam(focal, 400, -20 + 10 * t, 30)

    for j, (nm, x, sh, stock, env) in enumerate(shapes):
        st.add(f"h{j}", tess(stock), STOCK_COL, edges=True)
    for j, (nm, x, sh, stock, env) in enumerate(shapes):
        st.remove(f"h{j}")
        machine_op(st, f"h{j}", stock, env, "-z", "lathe", nf(8), STOCK_COL, cap1,
                   f"Lathe: face and turn {nm.split(' M50')[0].lower()} to size", camh, spin=(x, 0))
    for j, (nm, x, sh, stock, env) in enumerate(shapes):
        st.remove(f"h{j}")
        axis = "+z" if "Heater" in nm or "Piston" in nm else "-z"
        sub = {"Heater block M50": "Mill: drill 3 cartridge bores Ø6.1 and 3 thermocouple holes from below; bayonet socket from the top",
               "Build plate M50": "Mill: bayonet spigot and lugs underneath, rim groove for the gripper and the PTFE wiper",
               "Piston head M50": "Mill: bore-seal groove, rod socket, lead pockets under the heaters"}[nm]
        machine_op(st, f"h{j}", env, sh, axis, "drill" if axis == "+z" else "mill", nf(10), STOCK_COL, cap1, sub, camh)
        st.add(f"h{j}", tess(sh), "#b9c0c7", edges=True)
    for f in range(nf(6)):
        camh(1.0)
        st.shot()
    for j in range(3):
        st.remove(f"h{j}")

    # --- batch: every other machined part and every sheet part ---
    done = ("Process chamber body", "Build module M50", "Heater block", "Build plate", "Piston head")
    batch = [(i, p) for i, p in enumerate(st.parts) if kind(p) in ("stock", "sheet") and not any(k in p.name for k in done)]
    # lay them out in a grid on a bench, at their own size
    gap = 40.0
    x = y = 0.0
    rowh = 0.0
    lay = []
    for i, p in sorted(batch, key=lambda ip: -(bbox(ip[1].shape)[3] - bbox(ip[1].shape)[2])):
        b = bbox(p.shape)
        w, h = b[1] - b[0], b[3] - b[2]
        if x > 0 and x + w > 1900:
            x, y, rowh = 0.0, y + rowh + gap, 0.0
        lay.append((i, p, np.array([x - b[0], y - b[2], -b[4]])))
        x += w + gap
        rowh = max(rowh, h)
    W, Hh = 1900.0, y + rowh
    cap2 = "2  Machining: the other custom parts (CNC mill and lathe), and the sheet parts (laser-cut, bent, TIG-welded)"
    blanks = []
    for i, p, off in lay:
        o = off - np.array([W / 2, Hh / 2, 0])
        if kind(p) == "stock":
            s, _ = stock_blank(p)
        else:
            s = sheet_blank(p)
        blanks.append((i, p, o, s))
        mb = tess(s)
        if mb is not None:
            st.add(f"b{i}", mb.translate(o, inplace=False), SS_STOCK if p.mat.startswith("ss") else STOCK_COL, edges=True)
    nb = nf(14)
    for f in range(nb):
        t = ease((f + 1) / nb)
        for i, p, o, s in blanks:
            if f == nb // 2:
                st.remove(f"b{i}")
                st.shown.add(i)
                st.mat[i] = T(o)
            elif f < nb // 2:
                for a in st.extra.get(f"b{i}", []):
                    a.prop.opacity = 1.0 - 0.6 * (f / (nb / 2))
        st.caption(cap2, "Base plates (MIC-6), legs, lid, door, optics bridge and posts, Z parts, recoater parts, window "
                         "stack, dosing parts, reservoir, liners, plenums, guard panels")
        st.cam((0, 0, 0), 3900 - 500 * t, -10 + 20 * t, 50)
        st.shot()
    for f in range(nf(8)):
        st.cam((0, 0, 0), 3400, 10 + f, 50)
        st.shot()
    for i, p, o, s in blanks:
        st.remove(f"b{i}")
    st.shown.clear()
    st.mat.clear()


# ------------------------------------------------------------------ chapter 3: the build module
def screw_items_from_solids(shape, face, n, sel=None):
    """One screw per solid of a compound, at the solid's centre on its `face` ('zmin', 'zmax', 'ymin', ...)."""
    out = []
    for s in shape.Solids():
        b = bbox(s)
        if sel and not sel(b):
            continue
        c = np.array([(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2])
        ax = "xyz".index(face[0])
        c[ax] = b[2 * ax] if face.endswith("min") else b[2 * ax + 1]
        out.append((c, n))
    return out


def fly(st, idxs, frames, frm, cam, caption, sub, xf=None, extra=None):
    """Parts idxs fly in from offset frm (3-vector or callable(i) -> 4x4 at t=0) to place."""
    for i in idxs:
        st.shown.add(i)
    for f in range(frames):
        t = ease((f + 1) / frames)
        for i in idxs:
            if xf is not None:
                st.mat[i] = xf(i, t)
            else:
                v = np.asarray(frm(i) if callable(frm) else frm, float)
                st.mat[i] = T(v * (1 - t))
            st.opac[i] = st.parts[i].opacity * (0.35 + 0.65 * t)
        if extra:
            extra(t)
        st.caption(caption, sub)
        cam(t)
        st.shot()
    for i in idxs:
        st.opac.pop(i, None)
        if xf is None:
            st.mat.pop(i, None)


def chapter_module(st):
    st.shown.clear()
    st.mat.clear()
    cap = "3  Assembly: the heated M50 build module"

    def cam(t, d=300, az=-35, el=18, fz=125.0):
        st.cam((0.0, 0.0, fz), d, az + 12 * t, el)

    F = st.find
    blk, cart, tc, tco = F("Heater block M50"), F("Cartridge heaters M50"), F("Type K thermocouples M50"), F("Thermal cutoff M50")
    mac, shd, head, seal = F("Macor standoffs M50"), F("Radiation shields M50"), F("Piston head M50"), F("Bore seal M50")
    rod, rodend, strk = F("Hollow piston rod M50"), F("Rod end M50"), F("Striker disc M50")
    plate, wiper = F("Build plate M50"), F("Plate rim wiper M50")
    body, oring, bfl, handle = F("Build module M50"), F("Spigot O-ring"), F("Module M50 bottom flange"), F("Module M50 handle")
    lift = np.array([0, 0, 170.0])          # the piston stack is built above the cylinder, then lowered in
    stack = blk + cart + tc + tco + mac + shd + head + seal + rod + plate + wiper

    def rise(dz):
        return lambda i, t: T(lift + np.array([0, 0, dz * (1 - t)]))

    fly(st, blk, nf(8), None, lambda t: cam(0.1 * t), cap, "Heater block (6061-T6) with its bayonet socket", xf=rise(110))
    fly(st, cart, nf(10), None, lambda t: cam(0.1 + 0.1 * t, el=6), cap,
        "3 x 50 W, 24 V cartridge heaters (McMaster 3714N36) slide up into their Ø6.1 bores", xf=rise(-90))
    fly(st, tc + tco, nf(10), None, lambda t: cam(0.2 + 0.1 * t, el=6), cap,
        "Type K thermocouples (control, edge, limit; McMaster 3871K606) and the 240 °C thermal cutoff", xf=rise(-100))
    fly(st, mac + shd, nf(10), None, lambda t: cam(0.3 + 0.1 * t, el=10), cap,
        "Thermal break: three Macor standoffs (cut from 8489K75 rod) and two polished 316 radiation shields", xf=rise(-70))
    fly(st, head, nf(10), None, lambda t: cam(0.4 + 0.1 * t, el=10), cap, "Piston head: the cool side of the break", xf=rise(-80))
    mc = st.parts[mac[0]].shape
    hb = bbox(st.parts[head[0]].shape)
    items = [(np.array([c[0], c[1], hb[4]]) + lift, (0, 0, -1)) for c, _ in screw_items_from_solids(mc, "zmin", (0, 0, -1))]
    sc = Screws(st, "s-stack", items, 3.0, 20.0)
    st.caption(cap, "M3 screws up through the piston head into the standoffs and the block")
    sc.drive(nf(7), 0.5, lambda: (cam(0.5, el=-10), st.shot()))

    def seal_xf(i, t):
        s_ = 0.86 + 0.14 * t
        return T(lift + np.array([0, 0, -40 * (1 - t)])) @ np.diag([s_, s_, 1.0, 1.0])
    fly(st, seal, nf(8), None, lambda t: cam(0.55), cap, "Bore seal: aramid felt and a carbon-filled PTFE scraper, stretched into its groove", xf=seal_xf)
    fly(st, rod, nf(8), None, lambda t: cam(0.6, d=520, fz=95), cap, "Hollow 316 piston rod; the heater and thermocouple leads run down inside it",
        xf=rise(-120))
    fly(st, wiper, nf(6), None, lambda t: cam(0.65, d=520, fz=110), cap, "PTFE rim wiper snapped onto the plate", xf=rise(90))

    def plate_xf(i, t):
        drop = np.array([0, 0, 60 * (1 - min(1.0, t / 0.6))])
        tw = 60.0 * (1 - max(0.0, (t - 0.6) / 0.4))      # lugs enter the slots 60 deg off, then turn to lock
        return T(lift + drop) @ Rax((0, 0, 1), tw)
    fly(st, plate, nf(14), None, lambda t: cam(0.7 + 0.1 * t, d=400, el=30, fz=150), cap,
        "Build plate onto the bayonet (graphite foil between), turned 60° to lock", xf=plate_xf)
    fly(st, body, nf(10), (0, 0, -140), lambda t: cam(0.8, d=700, fz=40), cap,
        "Welded and honed module body: spigot, flange and Ø50.8 cylinder")
    fly(st, bfl + handle, nf(8), (0, 0, -80), lambda t: cam(0.8, d=700, el=4, fz=0), cap,
        "Bottom flange with its double FKM rod gland (2-114) and the front handle")
    nw = nf(10)
    for f in range(nw):
        phi = 360.0 * (f + 1) / nw
        st.add("weld-bf", arc_tube(28.6, -92.0, phi, 1.4), "#ff9a3c" if phi < 360 else "#8f8a80", glow=phi < 360)
        st.caption(cap, "TIG-welded to the tube (the piston goes in and out through the top, so the gland is serviced from there)")
        cam(0.85, d=600, el=-8, fz=-40)
        st.shot()

    def oring_xf(i, t):
        s_ = 0.9 + 0.1 * t
        return T((0, 0, 40 * (1 - t))) @ np.diag([s_, s_, 1.0, 1.0])
    fly(st, oring, nf(8), None, lambda t: cam(0.85, d=650, fz=20), cap, "FKM 2-238 O-ring into the spigot's groove", xf=oring_xf)
    nl = nf(16)
    for f in range(nl):
        t = ease((f + 1) / nl)
        for i in stack:
            st.mat[i] = T(lift * (1 - t))
        sc.shift(T(-lift * t))
        st.caption(cap, "The heater stack goes into the bore from the top; the rod passes down through the gland")
        cam(0.9, d=650, fz=60 - 60 * t)
        st.shot()
    for i in stack:
        st.mat.pop(i, None)
    fly(st, rodend + strk, nf(10), (0, 0, -80), lambda t: cam(0.95, d=620, el=-12, fz=-80), cap,
        "Rod end: leads potted out of a side exit (Torr Seal); the 416 striker disc for the Z stage's pot magnet")
    st.caption(cap, "Done: the module leaves and returns as one unit; S25 and L75 modules are built the same way")
    n = nf(16)
    for f in range(n):
        st.cam((0.0, 0.0, -45.0), 640, -20 + 180 * f / n, 14)
        st.shot()
    st.clear_extra("s-")
    st.clear_extra("weld")
    st.shown.clear()
    st.mat.clear()


# ------------------------------------------------------------------ chapter 4: the process module
def chapter_process(st):
    st.shown.clear()
    st.mat.clear()
    F = st.find
    cap = "4  Assembly: the process module"
    focal = np.array([0.0, 0.0, 20.0])

    def cam(t, d=1500, az=-28, el=24, f=None, daz=10):
        st.cam(np.asarray(f if f is not None else focal, float), d, az + daz * t, el)

    def ex(i):
        return np.asarray(st.parts[i].explode, float)

    base, feet = F("Base plate, process"), F("Leveling mounts, process")
    fly(st, feet + base, nf(10), (0, 0, 250), lambda t: cam(t, 1900, el=30), cap, "MIC-6 base plate (cut to size, Z window milled) on four levelling mounts")
    bases = (-370.0, 290.0, -265.0, 215.0)
    zb1 = M.P["z_base1"]
    items = [((x, y, zb1), (0, 0, 1)) for x in (bases[0] + 30, bases[1] - 30) for y in (bases[2] + 30, bases[3] - 30)]
    Screws(st, "s-feet", items, 8.0, 24.0, order=[0, 3, 1, 2]).drive(nf(6), 0.5, lambda: (cam(0.5, 2000, el=32), st.shot()))
    legs = F("Chamber legs")
    fly(st, legs, nf(8), ex, lambda t: cam(0.6, 1800), cap, "Chamber legs (6061, 30 x 30), bolted from under the base plate")
    ch = F("Process chamber body")
    fly(st, ch, nf(12), ex, lambda t: cam(0.7, 1600), cap, "Chamber body onto the legs")
    under = F("outlet plenum", "Outlet plenum port", "Overflow funnel", "Overflow port", "Overflow jar", "Overflow clamp",
              "Overflow-jar present", "Module-present sensor", "Locating dowel")
    fly(st, under, nf(12), ex, lambda t: cam(t, 1300, az=-20, el=-14), cap,
        "Under the floor: cross-flow outlet plenum, overflow funnel and KF-40 jar, dowel pins, sensors")
    inside = F("Lift-out wall liners", "Layer-light", "Plate-height through-beam", "inlet plenum", "Inlet plenum port", "Vacuum port")
    fly(st, inside, nf(12), ex, lambda t: cam(t, 1300, az=-24, el=40), cap,
        "Lift-out 316L wall liners, LED bar, through-beam fibres; inlet plenum and KF-25 ports welded on")
    # recoater
    rail = F("Recoater guide rail")
    fly(st, rail, nf(8), ex, lambda t: cam(t, 900, az=-8, el=38), cap, "Recoater: 15 mm guide rail on the back wall (McMaster 6709K33)")
    items = [((x, 80.0, M.P["rc_rail_z"]), (0, -1, 0)) for x in (-120, -80, -40, 0, 40, 80, 120)]
    Screws(st, "s-rail", items, 4.0, 12.0).drive(nf(5), 0.6, lambda: (cam(0.6, 800, az=-8, el=34), st.shot()))
    rec = F("Recoater carriage (", "Recoater ball screw", "Recoater ball nut", "Recoater carriage block", "Recoater fixed bearing",
            "Recoater floating bearing", "Recoater motor standoff", "Recoater servo", "Recoater motor bracket", "Recoater arm")
    fly(st, rec, nf(14), ex, lambda t: cam(t, 1000, az=-10, el=36), cap,
        "Carriage, M12 ball screw (4566N101) through the side-wall bores and its bearings, ball nut, ClearPath servo")
    hold = F("Blade holder", "HSS recoater blade")
    fly(st, hold, nf(8), ex, lambda t: cam(t, 800, az=-30, el=36), cap, "Quick-swap blade holder and the HSS blade")
    items = [((-115.0, y, 20.0), (-1, 0, 0)) for y in (-35.0, 0.0, 35.0)]
    Screws(st, "s-blade", items, 3.0, 10.0).drive(nf(5), 0.5, lambda: (cam(0.7, 700, az=-50, el=30), st.shot()))
    # Z stage under the floor
    zst = F("Z mounting flange", "Z actuator", "Z bracket", "Z servo", "Z carriage", "Z lift arm", "Pot magnet")
    fly(st, zst, nf(14), ex, lambda t: cam(t, 1200, az=-40, el=-12, f=(0, 40, -90)), cap,
        "Folded Z stage hung from the chamber floor: actuator, 2:1 belt fold, servo, lift arm with the pot magnet")
    items = [((-33.0, 66.0, -30.0), (0, 0, -1)), ((90.0, 97.0, -30.0), (0, 0, -1)), ((-33.0, 94.0, -30.0), (0, 0, -1)),
             ((30.0, 97.0, -30.0), (0, 0, -1))]
    Screws(st, "s-z", items, 5.0, 14.0, order=[0, 3, 1, 2]).drive(nf(5), 0.5, lambda: (cam(0.6, 1000, az=-40, el=-16, f=(0, 40, -90)), st.shot()))
    # the build module comes in along its swap path (reverse), then the arm rises and the magnet takes the striker
    mod = [i for i, p in enumerate(st.parts) if p.group in ("module", "piston") and "Captive" not in p.name]
    st.shown.update(mod)
    L = M.MOTION["module"]["hi"]
    nm_ = nf(22)
    for f in range(nm_):
        t = ease((f + 1) / nm_)
        loc = R.loc_matrix(M.group_location("module", L * (1 - t)))
        for i in mod:
            st.mat[i] = loc
        for i in F("Z carriage", "Z lift arm", "Pot magnet"):
            st.mat[i] = T((0, 0, MP.ZSTAGE_RELEASE))
        st.caption(cap, "The M50 module goes in along its swap path: in under the chamber, up into the Ø96 floor port")
        cam(t, 1100, az=-34, el=-4, f=(0, -80, -60), daz=14)
        st.shot()
    for i in mod:
        st.mat.pop(i, None)
    items = [((s * MP.SCREW_X, 0.0, -MP.FLOOR_T - MP.FLANGE_T), (0, 0, -1)) for s in (-1, 1)]
    Screws(st, "s-thumb", items, 6.0, 20.0, color="#c9ced3").drive(nf(7), 0.3, lambda: (cam(0.8, 900, az=-30, el=-18, f=(0, 0, -60)), st.shot()))
    nz = nf(8)
    for f in range(nz):
        t = ease((f + 1) / nz)
        for i in F("Z carriage", "Z lift arm", "Pot magnet"):
            st.mat[i] = T((0, 0, MP.ZSTAGE_RELEASE * (1 - t)))
        st.caption(cap, "Captive M6 screws pull the flange up to the floor (dowels locate it); the Z arm rises and its magnet takes the striker")
        cam(0.9, 900, az=-30, el=-18, f=(0, 0, -60))
        st.shot()
    for i in F("Z carriage", "Z lift arm", "Pot magnet"):
        st.mat.pop(i, None)
    # gas knife and chute under the lid line, then the lid
    pre = F("Gas knife", "Dose chute", "Lid O-ring")
    fly(st, pre, nf(10), ex, lambda t: cam(t, 1200, az=-20, el=46), cap, "Gas knife and dose chute; the FKM cord pressed into the lid gland")
    lid = F("Chamber lid (")
    fly(st, lid, nf(10), ex, lambda t: cam(t, 1200, az=-20, el=46), cap, "Lid (6061-T6, 16 mm) onto the O-ring")
    lid_items = [(np.array([c[0], c[1], M.P["lid_z1"]]), (0, 0, 1)) for c, _ in
                 screw_items_from_solids(st.parts[F("Lid screws")[0]].shape, "zmin", (0, 0, 1))]
    order = star_order(np.array([c for c, _ in lid_items]))
    Screws(st, "s-lid", lid_items, 5.0, 16.0, order=order).drive(nf(5), 0.6,
                                                                 lambda: (cam(0.5, 1000, az=-16, el=55), st.shot()))
    win = F("Field-stop", "Window flange", "Window O-ring", "Ø2 in. fused-silica window", "Window retaining ring")
    fly(st, win, nf(12), ex, lambda t: cam(t, 700, az=-20, el=48, f=(0, 0, 130)), cap,
        "Window stack: field stop, flange, FKM O-ring, Ø2 in. fused-silica window, retaining ring")
    items = [((44 * math.cos(math.radians(a)), 44 * math.sin(math.radians(a)), 163.0), (0, 0, 1)) for a in range(30, 360, 60)]
    Screws(st, "s-win", items, 3.0, 12.0, order=[0, 3, 1, 4, 2, 5]).drive(nf(5), 0.5, lambda: (cam(0.5, 600, az=-20, el=50, f=(0, 0, 140)), st.shot()))
    drw = F("Cover-slide drawer", "Cover slide (", "Drawer O-ring", "Drawer-closed sensor")
    fly(st, drw, nf(10), ex, lambda t: cam(t, 800, az=-30, el=30, f=(0, -60, 120)), cap,
        "Cover-slide drawer slides into the lid's front edge (fused-silica slide, FKM seal)")
    dose = F("Metering base", "NFC reader", "Dovetail rails", "Roller shaft seal", "Dosing stepper", "Side reservoir port",
             "Reservoir-docked sensor", "Load cell")
    fly(st, dose, nf(12), ex, lambda t: cam(t, 800, az=-40, el=40, f=(-90, 0, 170)), cap,
        "Dosing: metering base with its fluted roller and stepper, dovetail dock on a load cell, NFC reader")
    items = [((x, y, 180.0), (0, 0, 1)) for x in (-99.0, -81.0) for y in (-55.0, 55.0)]
    Screws(st, "s-dose", items, 4.0, 14.0, order=[0, 3, 1, 2]).drive(nf(5), 0.5, lambda: (cam(0.6, 700, az=-40, el=44, f=(-90, 0, 170)), st.shot()))
    res = [i for i, p in enumerate(st.parts) if p.group == "cartridge"]
    fly(st, res, nf(12), None, lambda t: cam(t, 800, az=-40, el=30, f=(-90, -40, 200)), cap,
        "Reservoir M (97 cm³) slides in on the dovetail; the dock's cam opens its shutter",
        xf=lambda i, t: T((0, -160 * (1 - t), 0)))
    for i in res:
        st.mat.pop(i, None)
    top = F("Camera viewport", "Layer camera", "Pressure transducer", "Overpressure relief")
    fly(st, top, nf(10), ex, lambda t: cam(t, 900, az=-10, el=40), cap, "Layer camera on its viewport, pressure transducer, relief valve")
    # door: hinges, then the door swings shut from open
    hk = F("Door hinge knuckles on the chamber", "Hinge pins", "Draw-latch keepers")
    fly(st, hk, nf(8), ex, lambda t: cam(t, 1000, az=-12, el=12, f=(0, -100, 40)), cap, "Hinge knuckles and latch keepers on the chamber front")
    door = [i for i, p in enumerate(st.parts) if p.group == "door"]
    st.shown.update(door)
    nd = nf(16)
    for f in range(nd):
        t = ease((f + 1) / nd)
        ang = M.P["door_open_deg"] * (1 - t)
        m = R.loc_matrix(M.group_location("door", ang)) if ang > 0 else np.eye(4)
        for i in door:
            st.mat[i] = T((0, -200 * (1 - min(1.0, 2 * t)), 0)) @ m if t < 0.5 else m
        st.caption(cap, "Drop-down door on its hinges (FKM face seal), closed with two 800 lb draw latches")
        cam(t, 1000, az=-12, el=12, f=(0, -100, 40))
        st.shot()
    for i in door:
        st.mat.pop(i, None)
    hl = st.parts[F("Door hinge leaves")[0]].shape
    items = screw_items_from_solids(hl, "ymin", (0, -1, 0), sel=lambda b: (b[5] - b[4]) > 20)
    items = [(c + np.array([dx, 0, 4.0]), n) for c, n in items for dx in (-6.0, 6.0)]
    if items:
        Screws(st, "s-hinge", items, 4.0, 10.0).drive(nf(5), 0.5, lambda: (cam(0.8, 800, az=-12, el=10, f=(0, -120, 20)), st.shot()))
    # optics bridge
    posts = F("Optics bridge posts")
    fly(st, posts, nf(8), ex, lambda t: cam(t, 1700, az=-30, el=26, f=(-50, 0, 60)), cap, "Optics bridge posts (60 x 60 x 5 square tube) on the base plate")
    bridge = F("Optics bridge (")
    fly(st, bridge, nf(10), ex, lambda t: cam(t, 1700, az=-30, el=30, f=(-50, 0, 120)), cap, "Optics bridge (6061, 25 mm): first mode 133 Hz in the FEA")
    pb = st.parts[posts[0]].shape
    items = []
    for c, _ in screw_items_from_solids(pb, "zmax", (0, 0, 1)):
        for dx in (-22, 22):
            for dy in (-22, 22):
                items.append((np.array([c[0] + dx, c[1] + dy, M.P["z_bridge1"]]), (0, 0, 1)))
    Screws(st, "s-bridge", items, 6.0, 30.0).drive(nf(4), 0.6, lambda: (cam(0.5, 1500, az=-30, el=40, f=(-50, 0, 150)), st.shot()))
    galvo = F("2-axis galvo")
    fly(st, galvo, nf(10), ex, lambda t: cam(t, 1100, az=-25, el=30, f=(-60, 0, 230)), cap, "2-axis galvo scan head on the bridge")
    lens = F("f-theta lens")

    def lens_xf(i, t):
        return T((0, 0, -60 * (1 - t))) @ Rax((0, 0, 1), 540 * (1 - t))
    fly(st, lens, nf(12), None, lambda t: cam(t, 900, az=-25, el=12, f=(0, 0, 200)), cap,
        "f = 160 mm f-theta lens threads up into the galvo through the bridge", xf=lens_xf)
    for i in lens:
        st.mat.pop(i, None)
    beam = F("Enclosed beam tube", "Safety shutter", "Collimator", "Process fiber")
    fly(st, beam, nf(12), ex, lambda t: cam(t, 1300, az=-30, el=30, f=(-150, 0, 230)), cap,
        "Beam tube, safety shutter and beam dump, collimator (QBH) on its V-mount, armoured process fiber")
    guard = F("Guard frame", "Laser guard panels", "Guard door rail", "Sliding guard door", "OD 7+", "Guard-locking", "Operator panel box",
              "E-stop", "Key switch", "Emission indicator", "Reset button")
    fly(st, guard, nf(14), ex, lambda t: cam(t, 2200, az=-26, el=24, f=(0, 0, 80)), cap,
        "Class 1 laser guard: T-slot frame, 1.5 mm aluminium panels, sliding door with an OD 7+ window, guard lock")


# ------------------------------------------------------------------ chapter 5: rack, gas, dock; finale
def chapter_tray(st):
    F = st.find
    cap = "5  Assembly: rack and gas modules, hoses and the tray dock"
    if not st.shown:      # run on its own: the process module is already built
        st.hidden.difference_update(F("Lid screws", "Captive M6"))
        st.shown.update(i for i, p in enumerate(st.parts) if p.step <= 9 or p.step == 12)
        st.shown.difference_update(F("Rack side panels", "19 in. rack", "UPS", "Fiber laser source", "Scan + laser", "DIN-rail",
                                     "Operator panel", "E-stop", "Key switch", "Emission", "Reset"))

    def ex(i):
        return np.asarray(st.parts[i].explode, float)

    def cam(t, d=3600, az=20, el=26, f=(0, 0, 40), daz=10):
        st.cam(np.asarray(f, float), d, az + daz * t, el)

    tray = F("VLM tray")
    fly(st, tray, nf(10), (0, 0, -260), lambda t: cam(t, 3800, az=20, el=30), cap, "The finished process module stands on the VLM tray (2450 x 864 mm)")
    rack = F("19 in. rack frame")
    fly(st, rack, nf(8), (0, 0, 300), lambda t: cam(t, 2200, az=-30, el=22, f=(-700, 0, 40)), cap, "10U 19 in. rack on the left of the tray")
    units = F("UPS (", "Fiber laser source", "Scan + laser controller", "DIN-rail drawer")
    for i in units:
        fly(st, [i], nf(7), ex, lambda t: cam(0.3, 2000, az=-26, el=16, f=(-700, -100, 40)), cap,
            "Rack: " + st.parts[i].name.split(" (")[0] + {"L1": " (quoted IPG YLR-500-U3-SM-AC is 4U and air-cooled; drawn 3U)"}.get(st.parts[i].bom, ""))
        b = bbox(st.parts[i].shape)
        items = [((x, -274.0, z), (0, -1, 0)) for x in (b[0] + 9, b[1] - 9) for z in (b[4] + 9, b[5] - 9)]
        Screws(st, f"s-r{i}", items, 6.0, 12.0, order=[0, 3, 1, 2]).drive(nf(4), 0.6, lambda: (cam(0.3, 1900, az=-26, el=14, f=(-700, -150, 40)), st.shot()))
    rest = F("Rack side panels", "Operator panel", "E-stop", "Key switch", "Emission indicator", "Reset button")
    fly(st, [i for i in rest if i not in st.shown], nf(8), ex, lambda t: cam(t, 2200, az=-30, el=20, f=(-700, 0, 40)), cap,
        "Vented side panels; operator panel with E-stop, key switch, emission lamp and reset")
    gasb = F("Base plate, gas", "Leveling mounts, gas")
    fly(st, gasb, nf(8), ex, lambda t: cam(t, 2400, az=24, el=28, f=(700, 0, 0)), cap, "Gas and vacuum module: MIC-6 base on levelling mounts")
    items = [((x, y, M.P["z_base1"]), (0, 0, 1)) for x in (430.0, 960.0) for y in (-220.0, 270.0)]
    Screws(st, "s-gfeet", items, 8.0, 24.0, order=[0, 3, 1, 2]).drive(nf(4), 0.5, lambda: (cam(0.4, 2300, az=24, el=30, f=(700, 0, 0)), st.shot()))
    gas = [i for i, p in enumerate(st.parts) if p.step == 10 and i not in gasb]
    fly(st, gas, nf(16), ex, lambda t: cam(t, 2400, az=24, el=28, f=(700, 0, 0)), cap,
        "Dry scroll pump, sealed blower, cyclone + HEPA housing, O2 / dew-point box, argon manifold and regulator")
    hoses = [i for i, p in enumerate(st.parts) if p.step == 11]
    fly(st, hoses, nf(14), ex, lambda t: cam(t, 2600, az=10, el=34, f=(350, 0, 20)), cap,
        "KF-25 bellows for the gas loop and vacuum, vacuum valve, 1/4 in. argon and 1/8 in. O2 sample lines")
    dock = [i for i, p in enumerate(st.parts) if p.step == 13]
    fly(st, dock, nf(12), ex, lambda t: cam(t, 3600, az=18, el=30), cap, "Tray dock (power, Ethernet, argon, water, exhaust) and umbilicals")
    st.shown.update(i for i in range(len(st.parts)) if st.parts[i].step <= 13)
    st.caption("The desktop LPBF on its VLM tray: 564 mm tall, three modules side by side", "From stock and parts to a finished machine")
    n = nf(36)
    for f in range(n):
        st.cam((110.0, 0.0, 40.0), 3700, 28 + 360 * f / n, 22)
        st.shot()
    st.clear_extra("s-")


# ------------------------------------------------------------------ main
CHAPTERS = [("kit", chapter_kit), ("machining", chapter_machining), ("module", chapter_module), ("process", chapter_process),
            ("tray", chapter_tray)]


def main(argv):
    want = [a for a in argv if not a.startswith("--")] or [c for c, _ in CHAPTERS]
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    parts = M.build(module="M50")
    print(f"{len(parts)} parts in {time.time() - t0:.1f} s")
    st = Stage(parts)
    st.hidden.update(st.find("Lid screws", "Captive M6"))
    all_frames = []
    for k, (name, fn) in enumerate(CHAPTERS):
        if name not in want:
            continue
        t1 = time.time()
        st.frames = []
        fn(st)
        path = OUT / f"{k + 1}-{name}{'-quick' if QUICK else ''}.gif"
        R.save_gif(st.frames, path, ms=110, colors=200, hold_last=10)
        print(f"{name}: {len(st.frames)} frames in {time.time() - t1:.0f} s")
        all_frames += st.frames + [st.frames[-1]] * 10
        if QUICK:
            Image.fromarray(st.frames[len(st.frames) // 2]).save(OUT / f"{k + 1}-{name}-mid-quick.png")
    if not QUICK and len(want) == len(CHAPTERS) and shutil.which("ffmpeg"):
        tmp = pathlib.Path("/tmp/render-build-frames")
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir()
        for j, fr in enumerate(all_frames):
            Image.fromarray(fr).save(tmp / f"{j:05d}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "9", "-i", str(tmp / "%05d.png"), "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-crf", "24", "-movflags", "+faststart", str(OUT / "build.mp4")], check=True)
        print(f"wrote build.mp4: {(OUT / 'build.mp4').stat().st_size / 1e6:.1f} MB, {len(all_frames)} frames")
    print(f"total {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
