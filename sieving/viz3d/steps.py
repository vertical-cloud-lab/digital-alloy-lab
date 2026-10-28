"""The sieving procedure of docs/sieve-order.md as one 3-D animation, from the CadQuery model in model.py.

    xvfb-run -a -s "-screen 0 1920x1080x24" python steps.py              # out/sieving.gif, out/mp4/sieving.mp4
    PREVIEW=1 xvfb-run -a -s "-screen 0 1920x1080x24" python steps.py    # last frame of each sub-step, /tmp/preview_sieving.png

Same pipeline as #255's ``atomizer-training/viz3d`` (``scene.py`` is a copy of its Scene framework): parts move
along the paths an operator's hands would take them, and there is no operator figure. The powder is a DEM
(``dem.py``): it is poured, scooped, sieved and tipped out by the moving parts, and the readouts are what the
simulation holds where. The batch (100 g) and its split (75 % under 63 um, 22 % 63-250 um, 3 % over 250 um, after
Yankin et al. 2025's 75 % through 63 um) are an example, not a measurement. The magnified No. 230 is ``zoom.py``'s
DEM at real particle size; the bonding leads are ``cables.py``'s simulated cables.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw

import dem as D
import model as M
from scene import FPS, R, Scene, T, ease, lighter, window

CB = Z = None
if not os.environ.get("NO_CABLES"):
    import cables as CB
if not os.environ.get("NO_ZOOM"):
    import zoom as Z

STACK_GROUPS = ("pan", "s230", "s60", "cover")
SX, SY = M.STACK_XY
TX, TY = M.TRAY_C
FINE, COARSE, GRIT, PIECE = 0, 1, 2, 3
CLASS_R = {FINE: 1.2, COARSE: 1.7, GRIT: 2.4}
BATCH = 100.0                                   # g, example
SPLIT = {FINE: 0.75, COARSE: 0.22, GRIT: 0.03}  # by mass, example
RHO = 2.7e-3                                    # g/mm3, Al
POWDER = (0.70, 0.72, 0.76)
FALSE = {FINE: (0.20, 0.45, 0.85), COARSE: (0.95, 0.55, 0.15), GRIT: (0.30, 0.30, 0.33)}
HEAP = np.array([TX + 20.0, TY, 0.0])            # where the pour lands
CLIP_OPEN = 0.25                                 # alligator clips open about 3 mm at the tips: astride a 1-2 mm wall

CAM = {
    "bench": [(-40.0, -1250.0, 760.0), (60.0, 40.0, 40.0), (0, 0, 1)],
    "pour": [(-520.0, -640.0, 420.0), (-280.0, 60.0, 80.0), (0, 0, 1)],
    "tray": [(-300.0, -470.0, 330.0), (-200.0, 20.0, 10.0), (0, 0, 1)],
    "scoop": [(-120.0, -760.0, 470.0), (-40.0, 10.0, 80.0), (0, 0, 1)],
    "stack": [(150.0, -620.0, 330.0), (150.0, -10.0, 80.0), (0, 0, 1)],
    "stack_cut": [(150.0, -470.0, 210.0), (150.0, -10.0, 70.0), (0, 0, 1)],
    "unstack": [(160.0, -860.0, 520.0), (250.0, 40.0, 90.0), (0, 0, 1)],
    "jars": [(300.0, -700.0, 470.0), (380.0, 40.0, 110.0), (0, 0, 1)],
    "balance": [(300.0, -640.0, 420.0), (380.0, -40.0, 120.0), (0, 0, 1)],
    "final": [(120.0, -1250.0, 760.0), (180.0, 40.0, 50.0), (0, 0, 1)],
}


# --------------------------------------------------------------------------------- helpers
def lab(text, xyz, fx, fy):
    return (text, tuple(float(v) for v in xyz), (fx, fy))


def path(u, pts):
    """Piecewise-linear path through pts, eased per leg; u from 0 to 1 spread evenly over the legs."""
    pts = [np.asarray(p, float) for p in pts]
    n = len(pts) - 1
    k = min(int(u * n), n - 1)
    return pts[k] + (pts[k + 1] - pts[k]) * ease(u * n - k)


def load_parts(sc: Scene, hidden=()):
    """Add every model part. The stack's parts are added twice (whole and halved at its axis); set_cut() blends."""
    ms = M.meshes()
    sc.cut_f["*"] = 0.0
    for name, m in ms.items():
        if name.startswith("_"):
            continue
        shown = name not in hidden
        if name == "bench":
            sc.add(name, m["whole"], m["color"], m["group"], ambient=0.95, diffuse=0.05, specular=0.0,
                   smooth_shading=False, shown=shown)
        elif name == "label":
            sc.add(name, m["whole"], m["color"], m["group"], ambient=0.80, diffuse=0.30, specular=0.0,
                   smooth_shading=False, shown=shown)
        elif m["cut"] and m["half"] is not None:
            sc.add(name, m["half"], m["color"], m["group"], opacity=m["opacity"], shown=shown)
            if m["half_cut"] is not None:
                sc.add(name + "#cut", m["half_cut"], lighter(m["color"]), m["group"], opacity=m["opacity"],
                       smooth_shading=False, ambient=0.55, diffuse=0.5, specular=0.0, shown=shown)
            sc.add("w:" + name, m["whole"], m["color"], m["group"], opacity=m["opacity"], shown=shown)
            sc.cutrole.update({name: "half", name + "#cut": "half", "w:" + name: "whole"})
            sc.cut_f[m["group"]] = 0.0
        else:
            sc.add(name, m["whole"], m["color"], m["group"], opacity=m["opacity"], shown=shown, specular=0.5,
                   specular_power=30)
    for g in STACK_GROUPS:
        sc.parent[g] = "stack"
    for g in ("tweezer_a", "tweezer_b"):
        sc.parent[g] = "tweezers"
    return ms


def set_cut(sc: Scene, f: float, groups=STACK_GROUPS):
    for g in groups:
        sc.cut_f[g] = f


def show_group(sc: Scene, group: str, a: float):
    for n in sc.members(group):
        sc.alpha[n] = a


# ------------------------------------------------------------------------------------ the powder
def fill_container(rng) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Parcels for the batch on a loose lattice inside the container (model coordinates), sizes shuffled, and the
    pieces in among them; DEM.settle drops them into a bed."""
    n = {k: int(round(BATCH * SPLIT[k] / (RHO * 4 / 3 * math.pi * CLASS_R[k] ** 3))) for k in CLASS_R}
    cls = np.concatenate([np.full(n[k], k) for k in (FINE, COARSE, GRIT)])
    rng.shuffle(cls)
    s = 5.0
    cx, cy = M.CONT_XY
    sites = []
    for k, z in enumerate(np.arange(4.0, 190.0, s)):          # staggered layers, so nothing lands in a column
        o = 0.5 * s * (k % 2)
        for x in np.arange(-52.0, 52.1, s):
            for y in np.arange(-52.0, 52.1, s):
                if (x + o) ** 2 + (y + o) ** 2 < 52.0 ** 2:
                    sites.append((cx + x + o, cy + y + o, z))
    sites = np.array(sites)
    npc = len(M.PIECE_R)
    # the pieces at every 9th site in the first part of the bed, their face neighbours left empty
    pick = np.arange(40, 40 + 9 * 60, 60)[:npc] * 3
    taken = np.zeros(len(sites), bool)
    for p in pick:
        taken[np.linalg.norm(sites - sites[p], axis=1) < s * 1.01] = True
    free = np.nonzero(~taken)[0][:len(cls)]
    x = np.vstack([sites[free], sites[pick]]) + rng.uniform(-0.6, 0.6, (len(free) + npc, 3))
    r = np.concatenate([[CLASS_R[c] for c in cls], M.PIECE_R])
    cls = np.concatenate([cls, np.full(npc, PIECE)])
    return x, r, cls


class Powder:
    """The DEM, its drawing (one glyph actor per size class, the pieces as meshes) and its bookkeeping."""

    def __init__(self, sc: Scene, seed=3):
        self.sc = sc
        rng = np.random.default_rng(seed)
        x, r, cls = fill_container(rng)
        self.sim = D.DEM(x, r, cls)
        for c in M.colliders():
            self.sim.add(D.Collider(**c))
        self.sim.compile()
        self.mass = self.sim.m.copy()
        self.pieces = np.nonzero(cls == PIECE)[0]
        self.agit = 0.15
        self.cut = 0.0
        self.colour_f = 0.0                     # 0: all powder grey, 1: false colour by size
        self.sphere = pv.Icosphere(radius=1.0, nsub=1)
        style = dict(smooth_shading=True, specular=0.25, specular_power=14, ambient=0.25, diffuse=0.85)
        for k in (FINE, COARSE, GRIT):
            sc.add(f"pw{k}", pv.PolyData(np.zeros((1, 3))), POWDER, "static", **style)
        for j, mesh in enumerate(M.meshes()["_pieces"]):
            sc.add(f"piece{j}", mesh, M.CHUNK, f"piece{j}", specular=0.4, specular_power=20)
        self.settle()
        self.draw()

    def world(self):
        return {c.group: self.sc.world(c.group) for c in self.sim.colliders}

    def settle(self, seconds=1.6):
        """Drop the parcels into a bed: nearly frictionless at first so they pack, then with friction to rest."""
        w = self.world()
        mu, cmu = self.sim.mu, self.sim.cMu.copy()
        for f in range(int(seconds * FPS)):
            slick = f < seconds * FPS * 0.6
            self.sim.mu = 0.05 if slick else mu
            self.sim.cMu[:] = 0.05 if slick else cmu
            self.sim.advance(1.0 / FPS, w, 0.0)
        self.sim.mu, self.sim.cMu[:] = mu, cmu
        self.sim.v[:] = 0.0

    def tick(self, seconds=1.0 / FPS, agit=None):
        self.sim.advance(seconds, self.world(), self.agit if agit is None else agit)
        self.draw()

    def draw(self):
        x, cls = self.sim.x, self.sim.cls
        hide = np.zeros(len(x), bool)
        if self.cut > 0.5:         # the stack is cut open: drop the parcels in its front half
            d = np.hypot(x[:, 0] - SX, x[:, 1] - SY)
            hide = (x[:, 1] < SY) & (d < M.SIEVE_OD / 2 + 3) & (x[:, 2] < 175)
        for k in (FINE, COARSE, GRIT):
            sel = (cls == k) & ~hide
            name = f"pw{k}"
            if sel.any():
                pts = pv.PolyData(x[sel])
                pts["s"] = self.sim.r[sel]
                self.sc.set_mesh(name, pts.glyph(geom=self.sphere, scale="s", orient=False))
                self.sc.alpha[name] = 1.0
            else:
                self.sc.alpha[name] = 0.0
            self.sc.color[name] = tuple(a + (b - a) * self.colour_f for a, b in zip(POWDER, FALSE[k]))
        for j, i in enumerate(self.pieces):
            self.sc.gmat[f"piece{j}"] = T(x[i])

    def where(self, test) -> dict:
        """Grams of each class whose parcel centre passes test(x) (a boolean array function)."""
        sel = test(self.sim.x)
        return {k: float(self.mass[sel & (self.sim.cls == k)].sum()) for k in (FINE, COARSE, GRIT, PIECE)}

    def in_sieve(self, group: str, lo=-3.0, hi=60.0) -> dict:
        """Grams on a sieve (or in the pan), in that part's frame: inside the frame, between lo and hi above the cloth."""
        Mw = np.linalg.inv(self.sc.world(group))
        z0 = M.MESH_Z[group]

        def test(x):
            q = x @ Mw[:3, :3].T + Mw[:3, 3]
            return (np.hypot(q[:, 0] - SX, q[:, 1] - SY) < M.RW) & (q[:, 2] > z0 + lo) & (q[:, 2] < z0 + hi)
        return self.where(test)

    def activate(self, test):
        self.sim.act[:] = test(self.sim.x)


def grams(d, keys=(FINE, COARSE, GRIT)) -> float:
    return sum(d[k] for k in keys)


# ------------------------------------------------------------------------------- leads and zoom
class Leads:
    """The three bonding leads as simulated cables (cables.py): an alligator clip on the container, the tray and the
    pan, a ring lug under a screw on the bus bar."""

    def __init__(self, sc: Scene):
        self.sc = sc
        self.cables = {}
        if CB is None:
            return
        cx, cy = M.CONT_XY
        tx, ty = M.TRAY_C
        a = math.radians(140.0)
        rad = np.array([math.cos(a), math.sin(a), 0.0])
        rim = M.RW + M.T_SHEET
        # (part group, the clip in that part's model coordinates, lead length)
        self.clips = {
            "container": ("container", CB.clip_matrix([cx, cy + 44.0, 223.0 + M.CONT_Z0], [0, 0.6, 0.8], [0, 1, 0]),
                          470.0),
            "tray": ("tray", CB.clip_matrix([tx - 100.0, ty + M.TRAY_D / 2, M.TRAY_H - 6.0], [0, 0.9, 0.44],
                                            [0, 1, 0]), 280.0),
            "pan": ("pan", CB.clip_matrix([SX + rim * rad[0], SY + rim * rad[1], M.DEPTH - 7.0], rad + [0, 0, -0.25],
                                          [0, 0, 1]), 560.0),
        }
        self.lugs = {k: CB.clip_matrix(M.GROUND_PTS[k], [0, -1, 0], [0, 0, 1]) for k in self.clips}
        for i, (k, (g, Mc, length)) in enumerate(self.clips.items()):
            a_, ad = CB.lead_end(sc.world(g) @ Mc)
            b_, bd = CB.lead_end(self.lugs[k], lug=True)
            cab = CB.Cable(a_, b_, length, radius=1.6, seed=i)
            cab.settle(a_, b_, ad, bd, self.obstacles(), seconds=3.0)
            self.cables[k] = cab
            sc.add(f"lead_{k}", cab.polydata(), CB.GREEN, "static", specular=0.3, specular_power=20)
            for nm, mesh, col in CB.clip_parts(CLIP_OPEN):
                sc.add(f"clip_{k}_{nm}", mesh, col, f"clip_{k}", specular=0.4)
            for nm, mesh, col in CB.lug_parts():
                sc.add(f"lug_{k}_{nm}", mesh.transform(self.lugs[k], inplace=False), col, "static", specular=0.4)
            sc.gmat[f"clip_{k}"] = sc.world(g) @ Mc

    def obstacles(self):
        sc = self.sc
        tx, ty = M.TRAY_C
        rs = M.RW + M.T_SHEET + M.LIP + M.T_SHEET
        cx, cy = M.CONT_XY
        bx, by = M.BAL_XY
        jx, jy = M.JAR_XY["coarse"]
        return [("plane", 0.0),
                ("box", np.eye(4), (tx - M.TRAY_W / 2, ty - M.TRAY_D / 2, 0.0), (tx + M.TRAY_W / 2, ty + M.TRAY_D / 2,
                                                                              M.TRAY_H)),
                ("cyl", sc.world("pan") @ T((SX, SY, 0.0)), rs, 0.0, M.DEPTH),
                ("cyl", sc.world("s230") @ T((SX, SY, M.SKIRT_Z["s230"])), rs, -0.6, M.SKIRT_H + M.DEPTH),
                ("cyl", sc.world("s60") @ T((SX, SY, M.SKIRT_Z["s60"])), rs, -0.6, M.SKIRT_H + M.DEPTH),
                ("cyl", sc.world("cover") @ T((SX, SY, M.COVER_Z)), rs, -0.6, 18.0),
                ("cyl", sc.world("container") @ T((cx, cy, M.CONT_Z0)), M.CONT_R, 0.0, 229.0),
                ("box", np.eye(4), (M.BUS_X0, M.BUS_Y - 10, 0.0), (M.BUS_X1, M.BUS_Y + 10, M.BUS_Z)),
                ("cyl", T((*M.DISH_XY, 0.0)), 34.2, 0.0, 12.2),
                ("box", np.eye(4), (bx - M.BAL_W / 2, by - M.BAL_D / 2, 0.0), (bx + M.BAL_W / 2, by + M.BAL_D / 2,
                                                                               M.BAL_PAN_Z + 2.0)),
                ("cyl", T((jx, jy, 0.0)), M.JAR_R, 0.0, M.JAR_H + 1.0)]

    def update(self):
        if CB is None:
            return
        obs = self.obstacles()
        for k, cab in self.cables.items():
            g, Mc, _ = self.clips[k]
            W = self.sc.world(g) @ Mc
            self.sc.gmat[f"clip_{k}"] = W
            a_, ad = CB.lead_end(W)
            b_, bd = CB.lead_end(self.lugs[k], lug=True)
            cab.step(a_, b_, ad, bd, obs)
            self.sc.set_mesh(f"lead_{k}", cab.polydata())

    def penetration(self) -> dict:
        """Each lead's deepest point inside any part, mm."""
        obs = self.obstacles()
        return {k: cab.penetration(obs) for k, cab in self.cables.items()}


class Magnifier:
    """zoom.py's real-scale DEM of the No. 230 cloth, drawn as a round inset with a leader to the cloth."""

    def __init__(self, sc: Scene, px=300):
        self.sc, self.px = sc, px
        self.z = Z.Zoom(size_px=px, seed=1) if Z is not None else None
        self.a = 0.0
        self.anchor = np.array([SX + 30.0, SY + 30.0, M.MESH_Z["s230"]])
        self.centre = (0.80, 0.42)            # inset centre, as a fraction of the frame

    def __call__(self, base: np.ndarray) -> np.ndarray:
        if self.z is None or self.a <= 0.02:
            return base
        img = Image.fromarray(base).convert("RGBA")
        W, H = img.size
        k = H / 720.0
        size = int(round(self.px * k))
        inset = self.z.render().resize((size, size), Image.LANCZOS)
        if self.a < 1.0:
            al = np.asarray(inset).copy()
            al[..., 3] = (al[..., 3] * self.a).astype(np.uint8)
            inset = Image.fromarray(al)
        cx, cy = self.centre[0] * W, self.centre[1] * H
        ax, ay = self.sc.project(self.sc.world("s230")[:3, :3] @ self.anchor + self.sc.world("s230")[:3, 3])
        d = ImageDraw.Draw(img, "RGBA")
        a8 = int(200 * self.a)
        ang = math.atan2(ay * H - cy, ax * W - cx)
        ex, ey = cx + math.cos(ang) * size / 2, cy + math.sin(ang) * size / 2
        d.line([(ex, ey), (ax * W, ay * H)], fill=(40, 40, 46, a8), width=max(1, int(round(2 * k))))
        rr = 7 * k
        d.ellipse((ax * W - rr, ay * H - rr, ax * W + rr, ay * H + rr), outline=(40, 40, 46, a8),
                  width=max(1, int(round(2 * k))))
        img.alpha_composite(inset, (int(round(cx - size / 2)), int(round(cy - size / 2))))
        return np.asarray(img.convert("RGB"))

    def advance(self, agit=1.0, tap=False):
        if self.z is not None:
            self.z.advance(1.0 / FPS, agitation=agit, tap=tap)


# ------------------------------------------------------------------------------- the animation
class Stop(Exception):
    pass


def anim_sieving():
    sc = Scene("sieving", "Sieving atomized powder: 8 in stack, No. 60 / 230 / pan (#222)")
    last = int(os.environ.get("STEPS", "99"))          # stop after this many sub-steps (for quick looks)
    step0 = sc.step

    def step(*a, **kw):
        step0(*a, **kw)
        if len(sc.substeps) >= last:
            raise Stop
    sc.step = step
    try:
        return _sieving(sc)
    except Stop:
        return sc.save()
    except Exception:
        if os.environ.get("PREVIEW"):
            sc.save()
        raise


def _sieving(sc):
    sc.cam = CAM["bench"]
    sc.swatches = [(0.10, 0.55, 0.25), *FALSE.values(), M.COPPER, (0.95, 0.55, 0.15), (0.20, 0.45, 0.85)]
    load_parts(sc, hidden=("label", "lid_coarse", "lid_print"))
    pw = Powder(sc)
    leads = Leads(sc)
    mag = Magnifier(sc)
    sc.inset = mag
    sim = pw.sim

    def gauges(**kv):
        names = {"batch": "Batch", "s60": "No. 60", "s230": "No. 230", "pan": "Pan", "tray": "Tray",
                 "balance": "Balance", "coarse": "Coarse jar", "print": "Print jar", "status": ""}
        sc.gauges = [(names[k], v) for k, v in kv.items() if v is not None]

    cable_mm = []

    def tick(agit=None, mag_on=False, tap=False):
        pw.tick(agit=agit)
        leads.update()
        cable_mm.append(leads.penetration())
        if mag_on:
            mag.advance(1.0, tap)

    on_tray = lambda x: (np.abs(x[:, 0] - TX) < M.TRAY_W / 2) & (np.abs(x[:, 1] - TY) < M.TRAY_D / 2) & (x[:, 2] < 60)
    gauges(batch=f"{BATCH:.0f} g (example)", status="leads on: container, tray, pan")

    # 1 · pour out ------------------------------------------------------------------------------------------
    cx, cy = M.CONT_XY
    mouth = np.array([cx, cy, 229.0 + M.CONT_Z0])
    to_tray = HEAP - np.array([cx, cy, 0.0])
    to_tray[2] = 0
    to_tray /= np.linalg.norm(to_tray)
    axis = np.array([-to_tray[1], to_tray[0], 0.0])        # tipping about this turns the top towards the tray
    over = HEAP + np.array([0.0, 0.0, 64.0]) - to_tray * 10.0

    def cont_pose(p, ang):
        return T(p - mouth) @ R(axis, ang, mouth)

    def pour(u):
        # up first (tipped, the can's bottom swings 237 mm below its mouth), over the tray tipping to 95 degrees,
        # then down to the pour height only once the bottom is above the mouth
        p = path(window(u, 0.0, 0.40), [mouth, mouth + (0, 0, 75), over + (0, 0, 240)])
        ang = 95.0 * window(u, 0.12, 0.40) + 70.0 * window(u, 0.40, 0.55)
        if u > 0.40:
            p = over + np.array([0, 0, 240.0]) * (1 - window(u, 0.40, 0.55))
        if u > 0.62:                                     # a few taps on the container to get the last of it out
            ang += 5.0 * math.sin(2 * math.pi * 3.0 * (u - 0.62) * 9.0) * (1 - window(u, 0.85, 1.0))
        sc.gmat["container"] = cont_pose(p, ang)
        tick()
        tray = grams(pw.where(on_tray))
        gauges(batch=f"{BATCH:.0f} g (example)", tray=f"{tray:5.1f} g", status="tipping out onto the tray")
    sc.step("1 · pour out", "After a run, with the dust settled: every lead clipped on first, then tip the container "
            "out onto the grounded stainless tray, never over paper or plastic (NFPA 484). The heap is mostly powder "
            "with a few unatomized pieces in it.", 9.0, pour, hold=0.6, cam_to=CAM["pour"], live=True,
            labels=[lab("powder container (size assumed, #255)", over + (0, 0, 150), 0.06, 0.28),
                    lab("bonding lead and clip", (M.TRAY_C[0] - 100, M.TRAY_C[1] + M.TRAY_D / 2 + 20, 20), 0.10, 0.62),
                    lab("ground bus bar", (-300, M.BUS_Y, M.BUS_Z), 0.62, 0.20)])

    # 2 · container back, pieces out --------------------------------------------------------------------------
    sim.act[:] = True
    tip0 = np.array([M.TWEEZ_REST[0], M.TWEEZ_REST[1], 2.5])
    dish = np.array([M.DISH_XY[0], M.DISH_XY[1], 30.0])
    state = {}

    def exposed():
        """The pieces on the tray under the least powder, nearest the dish first: the ones a hand would see."""
        x, r = sim.x, sim.r
        cover = []
        for j, i in enumerate(pw.pieces):
            if not on_tray(x[i:i + 1])[0]:
                continue
            d = np.hypot(x[:, 0] - x[i, 0], x[:, 1] - x[i, 1])
            above = (d < r[i] + r) & (x[:, 2] > x[i, 2] + 0.5 * r[i])
            cover.append((int(above.sum()), j))
        cover.sort()
        out = [j for _, j in cover[:4]]
        out.sort(key=lambda j: np.linalg.norm(x[pw.pieces[j], :2] - dish[:2]))
        return out

    def tweez_pose(p, yaw, pitch, grip):
        Mw = T(p - tip0) @ R((0, 0, 1), yaw, tip0) @ R((0, 1, 0), pitch, tip0)
        sc.gmat["tweezers"] = Mw
        for side, g in ((1.0, "tweezer_a"), (-1.0, "tweezer_b")):
            back = tip0 + np.array([-M.TWEEZ_L, side * 1.0, 0.0])
            sc.gmat[g] = R((0, 0, 1), -side * grip, back)

    def picks(u):
        if "order" not in state:
            state["order"] = exposed()
        w = window(u, 0.0, 0.24)                        # the pour in reverse: up, untip over the tray, home
        sc.gmat["container"] = cont_pose(path(w, [over, over + (0, 0, 240), mouth + (0, 0, 75), mouth]),
                                         165.0 - 70.0 * window(w, 0.0, 0.33) - 95.0 * window(w, 0.33, 0.70))
        order = state["order"]
        n = max(1, len(order))
        t = window(u, 0.12, 0.96) * n
        k = min(int(t), n - 1)
        f = t - k
        yaw, pitch = 90.0, 50.0
        if order:
            i = pw.pieces[order[k]]
            if "target" not in state or state.get("k") != k:
                state["k"], state["target"] = k, sim.x[i].copy()
                state["grip"] = math.degrees(math.atan((M.TWEEZ_GAP / 2 - sim.r[i] - 0.7) / M.TWEEZ_L))
            P = state["target"]
            if f < 0.30:
                p = path(f / 0.30, [tip0 + (0, 0, 60) if k == 0 else dish + (0, 0, 30), P + (0, 0, 50), P])
                grip = 0.0
            elif f < 0.40:
                p, grip = P, state["grip"] * window(f, 0.30, 0.40)
                if f > 0.36:
                    sim.held[i] = True
            elif f < 0.85:
                p, grip = path((f - 0.40) / 0.45, [P, P + (0, 0, 60), dish + (0, 0, 40), dish]), state["grip"]
            else:
                p, grip = dish, state["grip"] * (1 - window(f, 0.85, 0.93))
                if f > 0.88:
                    sim.held[i] = False
            if sim.held[i]:
                sim.v[i] = (p - sim.x[i]) * FPS
            if u > 0.96:
                p = path(window(u, 0.96, 1.0), [p, tip0])
        else:
            p, grip = tip0, 0.0
        if u <= 0.12:
            p = path(window(u, 0.0, 0.12), [tip0, tip0 + (0, 0, 60)])
            pitch = 50.0 * window(u, 0.0, 0.12)
            yaw = 90.0 * window(u, 0.0, 0.12)
        if u > 0.96:
            pitch = 50.0 * (1 - window(u, 0.96, 1.0))
            yaw = 90.0 * (1 - window(u, 0.96, 1.0))
        tweez_pose(p, yaw, pitch, grip)
        tick()
    sc.step("2 · pieces out", "Container back. Pick the pieces out with tweezers: splats, beads and anything over a "
            "few millimetres go to the dish. They are feedstock again (TA 04:50), not waste.", 7.0, picks, hold=0.6,
            cam_to=CAM["tray"], live=True,
            labels=[lab("pieces: back into the next charge", (*M.DISH_XY, 14), 0.62, 0.20)])
    for i in pw.pieces:
        sim.held[i] = False

    # 3 · cover off, scoop onto the No. 60 -------------------------------------------------------------------------
    rest = np.array([M.SCOOP_REST[0], M.SCOOP_REST[1], 0.0])
    cover_park = np.array([M.COVER_PARK[0] - SX, M.COVER_PARK[1] - SY, -(M.COVER_Z - M.T_SHEET) + 0.02])
    cover_high = np.array([cover_park[0], cover_park[1], 60.0])     # across at the lifted height, then straight down
    drop = np.array([SX - 30.0, SY, M.TOP_RIM_Z + 40.0])

    def scoop_pose(p, pitch):
        sc.gmat["scoop"] = T(p - rest) @ R((0, 1, 0), pitch, rest)

    def scoop(u):
        sc.gmat["cover"] = T(path(window(u, 0.0, 0.12), [(0, 0, 0), (0, 0, 60), cover_high, cover_park]))
        passes = ((HEAP[1] - 2.0, 1.2), (HEAP[1] + 40.0, 1.2))
        n = len(passes)
        t = window(u, 0.10, 1.0) * n
        k = min(int(t), n - 1)
        f = t - k
        y, z = passes[k]
        x0, x1 = HEAP[0] - 70.0, HEAP[0] + 40.0
        start = np.array([x0, y, z + 0.05])
        if f < 0.10:
            p = path(f / 0.10, [rest if k == 0 else drop, start + (0, 0, 70), start])
            pitch = 12.0 * window(f, 0.0, 0.10)
        elif f < 0.30:
            p, pitch = start + np.array([x1 - x0, 0.0, 0.0]) * window(f, 0.10, 0.30), 12.0 - 6.0 * window(f, 0.10, 0.30)
        elif f < 0.36:
            p, pitch = np.array([x1, y, z + 0.05]), 6.0 * (1 - window(f, 0.30, 0.36))
        elif f < 0.70:                # carried slowly, tilted back a little once clear, so the load sits at the back
            p = path((f - 0.36) / 0.34, [np.array([x1, y, z + 0.05]), np.array([x1 + 20, y, 120.0]),
                                         drop + (-30, 0, 30), drop])
            pitch = -6.0 * window(f, 0.39, 0.46)
        else:
            p = drop
            pitch = -6.0 + 68.0 * window(f, 0.70, 0.82) + 4.0 * math.sin(2 * math.pi * 4.0 * f) * window(f, 0.78, 0.84)
            pitch -= 62.0 * window(f, 0.90, 1.0)
        scoop_pose(p, pitch)
        tick()
        g60 = grams(pw.in_sieve("s60"))
        gauges(batch=f"{BATCH:.0f} g (example)", tray=f"{grams(pw.where(on_tray)):5.1f} g", s60=f"{g60:5.1f} g",
               status="about 35-40 g a pass on an 8 in No. 230")
    sc.step("3 · onto the No. 60", "Cover off. A conductive scoop carries the powder to the top sieve, the No. 60 "
            "(250 µm): it scalps what the tweezers missed and keeps the No. 230 below it clean. An 8 in No. 230 takes "
            "about 35-40 g a pass (DIN 66165's 26 cm³), so a 100 g run is three passes.", 15.0, scoop, hold=0.4,
            cam_to=CAM["scoop"], live=True,
            labels=[lab("No. 60 (250 µm)", (SX + 95, SY - 30, M.MESH_Z["s60"] + 20), 0.78, 0.30),
                    lab("No. 230 (63 µm)", (SX + 95, SY - 30, M.MESH_Z["s230"] + 20), 0.78, 0.46),
                    lab("pan", (SX + 95, SY - 30, 20), 0.78, 0.62)])

    def lid_on(u):
        scoop_pose(path(window(u, 0.0, 0.5), [drop, drop + (-60, 0, 30), rest + (0, 0, 80), rest]), 0.0)
        sc.gmat["cover"] = T(path(window(u, 0.35, 0.95), [cover_park, cover_high, (0, 0, 60), (0, 0, 0)]))
        tick()
    sc.step("3 · cover on", "Cover on before anything is shaken: fine aluminium is a combustible dust and the cover "
            "is the containment.", 3.0, lid_on, hold=0.4, cam_to=CAM["stack"], live=True,
            labels=[lab("cover", (SX, SY, M.TOP_RIM_Z + 8), 0.68, 0.22)])

    # 4 · sieve ------------------------------------------------------------------------------------------------
    sieve_s = 10.0
    in_stack = lambda x: np.hypot(x[:, 0] - SX, x[:, 1] - SY) < M.SIEVE_OD / 2 + 8
    pw.activate(in_stack)
    state["t"] = 0.0

    def sieve(u):
        t = state["t"]
        state["t"] += 1.0 / FPS
        amp = 5.0 * window(u, 0.0, 0.08) * (1 - window(u, 0.94, 1.0))
        w = 2 * math.pi * 2.2 * t
        k = int(t * FPS)
        tap = 0 < u < 0.94 and k % 9 == 0
        dz = 1.5 if (k % 9) in (1, 2) and u < 0.94 else 0.0
        sc.gmat["stack"] = T((amp * math.cos(w), amp * math.sin(w), dz))
        set_cut(sc, window(u, 0.0, 0.10))
        pw.cut = window(u, 0.0, 0.10)
        pw.colour_f = window(u, 0.05, 0.20)
        mag.a = window(u, 0.12, 0.22)
        sc.notes = [("No. 230 at real size, slow motion: 63 µm openings, 44 µm wire\n"
                     "blue < 63 µm goes through, orange 63-250 µm stays; bar 100 µm",
                     (mag.centre[0] - 0.08, mag.centre[1] + 0.25), mag.a)]
        tick(agit=5.0 * (amp > 0.5), mag_on=u > 0.12, tap=tap)
        g = {k_: pw.in_sieve(k_) for k_ in ("s60", "s230", "pan")}
        gauges(batch=f"{BATCH:.0f} g (example)", s60=f"{grams(g['s60']):5.1f} g", s230=f"{grams(g['s230']):5.1f} g",
               pan=f"{grams(g['pan']):5.1f} g", status="by hand: circles and taps, ~3 min")
    sc.step("4 · sieve", "Rotate the stack in a flat circle and tap the frame, about 3 minutes (here in time-lapse). "
            "Cut open: grit stays on the No. 60, 63-250 µm on the No. 230, and under 63 µm, the print fraction, falls "
            "to the pan. Inset: the No. 230 at real size.", sieve_s, sieve, hold=1.2, cam_to=CAM["stack_cut"],
            live=True, still=True,
            labels=[lab("> 250 µm", (SX - 60, SY + 40, M.MESH_Z["s60"] + 3), 0.10, 0.37),
                    lab("63-250 µm", (SX - 60, SY + 40, M.MESH_Z["s230"] + 3), 0.10, 0.52),
                    lab("< 63 µm: print fraction", (SX - 60, SY + 40, 4), 0.10, 0.70)])
    mag.a = 0.0
    sc.notes = []

    # 5 · unstack --------------------------------------------------------------------------------------------------
    sc.gmat["stack"] = np.eye(4)

    def rim(group, ang_deg, z):
        a = math.radians(ang_deg)
        return np.array([SX + (M.RW + 0.6) * math.cos(a), SY + (M.RW + 0.6) * math.sin(a), z])

    def tip_matrix(rim_pt, target, ang, axis_=(0, 1, 0)):
        """Carry a part so `rim_pt` on its rim sits at `target`, tipped `ang` degrees about a horizontal axis there."""
        return T(target - rim_pt) @ R(axis_, ang, rim_pt)

    def unstack(group, top_z, target, park, t0=0.0, extra=None):
        """Lift a sieve (or the pan) by its +x rim, tip it on the way over so it arrives already leaning, pour at 75
        then 135 degrees with `target` the low point of its rim, and come back the same way before setting it down at
        `park`."""
        r0 = rim(group, 0.0, top_z)       # the +x rim point: the sieve tips towards +x about it
        base = 0.0 if group == "pan" else M.SKIRT_Z[group] - M.T_SHEET
        pk = r0 + np.array([park[0] - SX, park[1] - SY, -base])
        pre = target + np.array([-60.0, 0.0, 110.0])
        a0, a1 = t0 + 0.30 * (1 - t0), t0 + 0.68 * (1 - t0)

        def update(u):
            if extra is not None:
                extra(u)
            if u < a1:
                v = window(u, t0, a0)
                carry = path(v, [r0, r0 + (0, 0, 90), pre, target])
                ang = 40.0 * ease(min(1.0, max(0.0, 3 * v - 1))) + 35.0 * ease(min(1.0, max(0.0, 3 * v - 2)))
                # wait for the powder to run to the low point of the rim, tap, then on to 135: at 105 the frame's
                # wall under the rim is still a 15 degree ledge, flatter than the powder's angle of friction
                ang += 60.0 * window(u, a0 + 0.12, a0 + 0.22)
                ang += 3.0 * math.sin(2 * math.pi * 6.0 * u) * (window(u, a0 + 0.04, a0 + 0.06) - window(u, a1 - 0.05, a1))
            else:
                v = window(u, a1, 1.0)
                carry = path(v, [target, pre, pk + (0, 0, 230), pk + (0, 0, 40), pk])   # set down slowly
                ang = 135.0 - 95.0 * ease(min(1.0, 3 * v)) - 40.0 * ease(min(1.0, max(0.0, 3 * v - 1)))
            sc.gmat[group] = tip_matrix(r0, carry, ang)
            pw.activate(lambda x: ~on_tray(x))
            tick()
        return update

    def lift_cover(u):
        set_cut(sc, 1.0 - window(u, 0.0, 0.10))
        pw.cut = 1.0 - window(u, 0.0, 0.10)
        sc.gmat["cover"] = T(path(window(u, 0.0, 0.22), [(0, 0, 0), (0, 0, 60), cover_high, cover_park]))

    over_dish = np.array([M.DISH_XY[0] + 14.0, M.DISH_XY[1], 52.0])
    s60_top = M.TOP_RIM_Z
    sc.step("5 · No. 60", "Cover off, then the No. 60: what it held joins the pieces in the dish.", 6.0,
            unstack("s60", s60_top, over_dish, M.SIEVE_PARK["s60"], t0=0.24, extra=lift_cover), hold=0.4, cam_to=CAM["unstack"],
            live=True)

    in_jar = lambda name: (lambda x: (np.hypot(x[:, 0] - M.JAR_XY[name][0], x[:, 1] - M.JAR_XY[name][1]) < M.JAR_R)
                           & (x[:, 2] > M.JAR_Z[name]) & (x[:, 2] < M.JAR_Z[name] + M.JAR_H))

    def coarse_gauge(u):
        gauges(batch=f"{BATCH:.0f} g (example)", s230=f"{grams(pw.in_sieve('s230')):5.1f} g",
               **{"coarse": f"{grams(pw.where(in_jar('coarse'))):5.1f} g"}, status="63-250 µm: re-atomize (E6, #222)")
    jx, jy = M.JAR_XY["coarse"]
    over_coarse = np.array([jx - 14.0, jy, M.JAR_Z["coarse"] + M.FUNNEL_SEAT + 98.0 + 26.0])
    sc.step("5 · No. 230", "The No. 230 next, through the funnel into its own jar: 63-250 µm, too coarse for the bed. "
            "Keep it; it can be re-atomized (E6 in #222).", 6.0,
            unstack("s230", 2 * M.DEPTH, over_coarse, M.SIEVE_PARK["s230"], extra=coarse_gauge), hold=0.4,
            cam_to=CAM["jars"], live=True, labels=[lab("63-250 µm", (jx, jy - 30, 40), 0.20, 0.30)])

    px_, py_ = M.JAR_XY["print"]
    over_print = np.array([px_ - 14.0, py_, M.JAR_Z["print"] + M.FUNNEL_SEAT + 98.0 + 26.0])
    in_print = lambda x: (np.hypot(x[:, 0] - px_, x[:, 1] - py_) < M.JAR_R) & (x[:, 2] > M.JAR_Z["print"]) & \
        (x[:, 2] < M.JAR_Z["print"] + M.JAR_H)

    def print_gauge(u):
        g = grams(pw.where(in_print))
        gauges(batch=f"{BATCH:.0f} g (example)", pan=f"{grams(pw.in_sieve('pan')):5.1f} g", balance=f"{g:5.1f} g",
               status="jar and funnel tared")
    sc.step("5 · pan", "The pan holds the print fraction, under 63 µm. It goes through the funnel into a jar already "
            "tared on the balance. Weigh every fraction: the yield says how many runs a print needs.", 7.0,
            unstack("pan", M.DEPTH, over_print, (SX, SY), extra=print_gauge), hold=1.0, cam_to=CAM["balance"],
            live=True, labels=[lab("< 63 µm: print fraction", (px_, py_ - 30, M.JAR_Z["print"] + 50), 0.20, 0.26)])

    # 6 · lids, label, and the rest of the heap ----------------------------------------------------------------------
    def finish(u):
        for j in ("coarse", "print"):
            sc.gmat[f"funnel_{j}"] = T((0, 0, 120.0 * window(u, 0.0, 0.40)))
            show_group(sc, f"funnel_{j}", 1.0 - window(u, 0.30, 0.40))
            sim.colliders[sim.index[f"funnel_{j}"]].on = u < 0.40
            sc.gmat[f"lid_{j}"] = T((0, 0, 80.0 * (1 - window(u, 0.40, 0.70))))
            show_group(sc, f"lid_{j}", 1.0 if u > 0.40 else 0.0)
        show_group(sc, "label", window(u, 0.70, 0.85))
        pw.activate(lambda x: ~on_tray(x))
        tick()
        g = grams(pw.where(in_print))
        gauges(batch=f"{BATCH:.0f} g (example)", **{"print": f"{g:5.1f} g"}, tray=f"{grams(pw.where(on_tray)):5.1f} g",
               status="then the next pass")
    sc.step("6 · label, store, repeat", "Lids on, a 6-character ID on the print jar (#249), the jar into the "
            "desiccant box. Then the next 35-40 g from the tray. The print jar is what feeds the doser's 25 mm "
            "cartridge: the Sep 30 clog was unsieved powder.", 4.5, finish, hold=2.0, cam_to=CAM["final"],
            labels=[lab("doser cartridge, Ø25 mm tube", (M.DOSER_XY[0], M.DOSER_XY[1] - 14, 60), 0.80, 0.30),
                    lab("6-character ID (#249)", (px_, py_ - 26, M.JAR_Z["print"] + 36), 0.80, 0.55)])
    info = sc.save()
    audit_path = M.HERE / "out" / "audit_frames.pkl"
    if not os.environ.get("PREVIEW"):
        import pickle
        audit_path.write_bytes(pickle.dumps(dict(record=sc.record, fps=FPS, cable_mm=cable_mm)))
    return info


ANIMS = {"sieving": anim_sieving}

if __name__ == "__main__":
    for name in (sys.argv[1:] or list(ANIMS)):
        ANIMS[name]()
