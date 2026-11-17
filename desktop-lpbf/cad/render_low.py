"""Render the low-profile desktop LPBF (lpbf_low.py) to PNGs and GIFs.

Run (headless):  xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/cad/render_low.py [what ...]
  what: stills, assembly, motion, turntable, cycle (default: all)
Writes to desktop-lpbf/cad/img/low/.
"""
from __future__ import annotations

import math
import pathlib
import sys
import time

import numpy as np
import pyvista as pv
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lpbf_low as M  # noqa: E402

pv.OFF_SCREEN = True
OUT = pathlib.Path(__file__).resolve().parent / "img" / "low"
W, H = 1400, 900
GW, GH = 820, 520

SECTION_HIDE = ("Laser guard", "Sliding guard", "OD 7+", "Guard door rail", "Guard-locking", "Guard frame", "Operator panel",
                "E-stop", "Key switch", "Emission indicator", "Reset button")


def hex2rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


def tess(shape, tol=0.3, ang=0.35):
    vs, ts = shape.tessellate(tol, ang)
    if not ts:
        return None
    pts = np.array([(v.x, v.y, v.z) for v in vs], dtype=float)
    faces = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
    return pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


def loc_matrix(loc):
    t = loc.wrapped.Transformation()
    m = np.eye(4)
    for i in range(3):
        for j in range(4):
            m[i, j] = t.Value(i + 1, j + 1)
    return m


MAT = dict(smooth_shading=True, specular=0.12, specular_power=10, ambient=0.25, diffuse=0.8)


class Scene:
    def __init__(self, parts, size, edges=True):
        self.parts = parts
        self.pl = pv.Plotter(off_screen=True, window_size=size, lighting="three lights")
        self.pl.set_background("#f7f9fb", top="#dfe6ee")
        self.actors = {}
        for i, p in enumerate(parts):
            m = tess(p.shape)
            if m is None:
                continue
            col = hex2rgb(p.color)
            a = self.pl.add_mesh(m, color=col, opacity=p.opacity, **MAT)
            e = None
            if edges and p.opacity > 0.3:
                fe = m.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False, manifold_edges=False)
                if fe.n_points:
                    e = self.pl.add_mesh(fe, color=(0.12, 0.13, 0.15), line_width=1.0, opacity=0.45)
            s = None
            if p.section:
                c = m.clip(normal="-y", origin=(0, 0, 0), invert=True)
                if c.n_points:
                    s = self.pl.add_mesh(c, color=col, opacity=max(p.opacity, 0.6), **MAT)
                    s.SetVisibility(False)
                else:
                    s = "empty"
            self.actors[i] = (a, e, s, p)
        self.pl.enable_anti_aliasing("ssaa")
        self.dyn = {}

    def set(self, visible=None, state=None, opacity=None, section=False, explode=None):
        state = state or {}
        for i, (a, e, s, p) in self.actors.items():
            vis = True if visible is None else bool(visible(p))
            m = np.eye(4)
            if p.group and state.get(p.group, 0.0) != 0.0:
                m = loc_matrix(M.group_location(p.group, state[p.group]))
            if explode is not None:
                off = explode(p)
                m = m.copy()
                m[:3, 3] += off
            op = p.opacity if opacity is None else opacity(p)
            cut = section and s is not None and s != "empty"
            hide = section and (any(k in p.name for k in SECTION_HIDE) or s == "empty")
            a.SetVisibility(vis and not cut and not hide)
            a.user_matrix = m
            a.prop.opacity = op
            if e is not None:
                e.SetVisibility(vis and not cut and not hide and op > 0.3)
                e.user_matrix = m
            if s is not None and s != "empty":
                s.SetVisibility(vis and cut)
                s.user_matrix = m

    def put(self, key, mesh, **kw):
        if key in self.dyn:
            self.pl.remove_actor(self.dyn.pop(key))
        if mesh is not None and mesh.n_points:
            self.dyn[key] = self.pl.add_mesh(mesh, **kw)

    def title(self, text, size=12):
        self.pl.add_text(text, position="upper_left", font_size=size, color="#1d2733", name="title", font="arial")

    def cam(self, pos, focal, up=(0, 0, 1), view_angle=30.0, parallel=False):
        # toggle the projection on the VTK camera directly: PyVista's disable_parallel_projection() moves the camera
        # to parallel_scale / sin(view_angle / 2) from the focal point
        self.pl.camera.parallel_projection = bool(parallel)
        self.pl.camera_position = [pos, focal, up]
        self.pl.camera.view_angle = view_angle

    def shot(self):
        self.pl.render()
        return self.pl.screenshot(return_img=True)


def orbit(focal, dist, az_deg, el_deg):
    az, el = math.radians(az_deg), math.radians(el_deg)
    return (focal[0] + dist * math.cos(el) * math.sin(az), focal[1] - dist * math.cos(el) * math.cos(az),
            focal[2] + dist * math.sin(el))


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def save_gif(frames, path, ms=90, colors=200, hold_last=14):
    frames = frames + [frames[-1]] * hold_last
    sample = np.concatenate([f[::3, ::3] for f in frames[:: max(1, len(frames) // 16)]], axis=0)
    pal = Image.fromarray(sample).quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    ims = [Image.fromarray(f).quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=ms, loop=0, optimize=False, disposal=1)
    print(f"wrote {path.name}: {len(ims)} frames, {path.stat().st_size / 1e6:.2f} MB")


def opening_planes(sc):
    """Translucent planes at the VLM opening heights, over the tray."""
    ox, oy = M.TRAY["outer"][0] / 2, M.TRAY["outer"][1] / 2
    cols = ["#d22b2b", "#f0a020", "#2b6cd2"]
    for k, (nm, h) in enumerate(M.OPENINGS.items()):
        z = M.Z_TRAY + h
        pl = pv.Plane(center=(0, 0, z), direction=(0, 0, 1), i_size=2 * ox, j_size=2 * oy)
        sc.put(f"plane{k}", pl, color=hex2rgb(cols[k]), opacity=0.10, ambient=1.0, diffuse=0.0)
        edge = pv.Box((-ox, ox, -oy, oy, z, z)).extract_feature_edges()
        sc.put(f"edge{k}", pv.Line((-ox, -oy, z), (ox, -oy, z)), color=hex2rgb(cols[k]), line_width=3)
        sc.pl.add_point_labels([(-ox + 10, -oy, z + 6)], [f"{nm}: {h:.1f} mm"], font_size=14, text_color=cols[k],
                               shape=None, show_points=False, always_visible=True, name=f"lab{k}")


FOCAL = (0.0, 0.0, 60.0)


def stills(parts):
    OUT.mkdir(parents=True, exist_ok=True)
    sc = Scene(parts, (W, H))
    # whole tray, guard closed, with the opening planes
    f = (110.0, 0.0, 40.0)
    sc.set()
    opening_planes(sc)
    sc.cam(orbit(f, 3900, 28, 20), f)
    Image.fromarray(sc.shot()).save(OUT / "tray-overview.png")
    for k in range(3):
        for key in (f"plane{k}", f"edge{k}"):
            sc.put(key, None)
        sc.pl.remove_actor(f"lab{k}")
    # front elevation (parallel projection) with the opening heights
    sc.set()
    opening_planes(sc)
    sc.cam((110, -6000, 150), (110, 0, 150), parallel=True)
    sc.pl.camera.parallel_scale = 720
    Image.fromarray(sc.shot()).save(OUT / "front-elevation.png")
    for k in range(3):
        for key in (f"plane{k}", f"edge{k}"):
            sc.put(key, None)
        sc.pl.remove_actor(f"lab{k}")
    # process module, guard hidden
    sc.set(visible=lambda p: not any(k in p.name for k in SECTION_HIDE))
    sc.cam(orbit(FOCAL, 1500, 30, 22), FOCAL)
    Image.fromarray(sc.shot()).save(OUT / "process-module-open.png")
    # doors open, cartridge out, recoater mid-stroke
    sc.set(visible=lambda p: not any(k in p.name for k in SECTION_HIDE), state={"door": 95.0, "cartridge": -125.0, "recoater": 100.0, "gdoor": 470.0})
    sc.cam(orbit(FOCAL, 1400, 18, 18), FOCAL)
    Image.fromarray(sc.shot()).save(OUT / "process-module-doors-open.png")
    # back
    sc.set(visible=lambda p: not any(k in p.name for k in SECTION_HIDE))
    sc.cam(orbit((150, 0, 0), 2600, 205, 24), (150, 0, 0))
    Image.fromarray(sc.shot()).save(OUT / "back.png")
    # section at y = 0
    f2 = (0.0, 10.0, 40.0)
    sc.set(section=True)
    sc.cam(orbit(f2, 1100, -20, 10), f2)
    Image.fromarray(sc.shot()).save(OUT / "section.png")
    print("stills done")


def assembly_gif(parts, frames_per_step=8):
    sc = Scene(parts, (GW, GH))
    f = (110.0, 0.0, 20.0)
    sc.cam(orbit(f, 3600, 28, 22), f)
    frames = []
    n = max(M.STEPS)
    for s in range(1, n + 1):
        for k in range(frames_per_step):
            t = ease((k + 1) / (frames_per_step - 2))
            sc.set(visible=lambda p, s=s: p.step <= s,
                   explode=lambda p, s=s, t=t: np.array(p.explode) * (1 - t) if p.step == s else np.zeros(3),
                   opacity=lambda p, s=s, t=t: p.opacity * (0.25 + 0.75 * t) if p.step == s else p.opacity)
            sc.cam(orbit(f, 3600, 28, 22), f)
            sc.title(f"Step {s}/{n}: {M.STEPS[s]}", 11)
            frames.append(sc.shot())
    sc.cam(orbit(f, 3600, 28, 22), f)
    sc.title("Low-profile desktop LPBF on a VLM tray: 564 mm tall, three modules side by side", 11)
    frames.append(sc.shot())
    save_gif(frames, OUT / "assembly.gif", ms=110, hold_last=18)


def motion_gif(parts):
    sc = Scene(parts, (GW, GH))
    hide = lambda p: not any(k in p.name for k in SECTION_HIDE[2:])   # keep guard panels, hide nothing else
    frames = []
    seq = [("gdoor", 0.0, 470.0, "Guard door slides right (guard lock released only when the laser is off)"),
           ("door", 0.0, 95.0, "Chamber door drops down on its bottom hinge (O-ring face seal, toggle latches)"),
           ("cartridge", 0.0, -125.0, "Hopper cartridge slides out to the front on its dovetail (robot handle)"),
           ("cartridge", -125.0, 0.0, "... and back in"),
           ("door", 95.0, 0.0, "Door closes"),
           ("recoater", 0.0, M.MOTION["recoater"]["hi"], "Recoater: park to end of spread"),
           ("piston", 0.0, -M.P["stroke"], "Build piston: full 40 mm stroke"),
           ("piston", -M.P["stroke"], 0.0, ""),
           ("recoater", M.MOTION["recoater"]["hi"], 0.0, ""),
           ("gdoor", 470.0, 0.0, "Guard door closes")]
    state = {}
    f = (40.0, -40.0, 40.0)
    sc.cam(orbit(f, 1500, 24, 16), f)
    for g, a, b, cap in seq:
        for k in range(12):
            state[g] = a + (b - a) * ease((k + 1) / 12)
            sc.set(state=dict(state), visible=lambda p: "Laser guard panels" not in p.name and "Guard frame" not in p.name)
            sc.cam(orbit(f, 1500, 24, 16), f)
            sc.title(cap, 11)
            frames.append(sc.shot())
    save_gif(frames, OUT / "motion.gif", ms=80, hold_last=8)


def turntable_gif(parts, n=36):
    sc = Scene(parts, (GW, GH))
    sc.set(visible=lambda p: not any(k in p.name for k in SECTION_HIDE) and "VLM tray" not in p.name and p.module != "tray")
    f = (0.0, 0.0, 60.0)
    frames = []
    for i in range(n):
        sc.cam(orbit(f, 3000, 20 + 360 * i / n, 20), f)
        frames.append(sc.shot())
    save_gif(frames, OUT / "turntable.gif", ms=100, hold_last=0)


# --------------------------------------------------------------------------------------------
# Build cycle in section: piston down, recoater back, dose, spread, lase. Layers exaggerated ~100x.
LAY = 4.0
R_PL = M.P["plate_d"] / 2
COUPONS = [("box", (-16, -6), (10, 12)), ("cyl", (8, 0), 5.0), ("box", (-2, -18), (14, 3))]
POWDER = dict(color=hex2rgb(M.C["powder"]), smooth_shading=False, specular=0.05, ambient=0.25, diffuse=0.8)


def _clip(m):
    c = m.clip(normal="-y", origin=(0, 0, 0), invert=True)
    return c if c.n_points else None


def bed_mesh(z0, z1, xmax=None):
    if z1 - z0 < 1e-3:
        return None
    m = pv.Cylinder(center=(0, 0, (z0 + z1) / 2), direction=(0, 0, 1), radius=R_PL, height=z1 - z0, resolution=72).triangulate()
    if xmax is not None:
        if xmax <= -R_PL:
            return None
        if xmax < R_PL:
            m = m.clip(normal="x", origin=(xmax, 0, 0), invert=True)
    return _clip(m)


def coupon_mesh(z0, z1):
    ms = []
    for kind, (x, y), d in COUPONS:
        if z1 - z0 < 1e-3:
            continue
        if kind == "box":
            ms.append(pv.Box((x, x + d[0], y, y + d[1], z0, z1)).triangulate())
        else:
            ms.append(pv.Cylinder(center=(x, y, (z0 + z1) / 2), direction=(0, 0, 1), radius=d, height=z1 - z0, resolution=48).triangulate())
    if not ms:
        return None
    m = ms[0].merge(ms[1:]) if len(ms) > 1 else ms[0]
    return _clip(m)


def wedge(x_front, length, height, y0=-30.0, y1=30.0):
    if height < 0.05 or length < 0.05:
        return None
    xa, xb = x_front, x_front + length
    pts = np.array([[xa, y0, 0], [xb, y0, 0], [xa, y0, height], [xa, y1, 0], [xb, y1, 0], [xa, y1, height]], float)
    faces = np.hstack([[3, 0, 1, 2], [3, 3, 5, 4], [4, 0, 3, 4, 1], [4, 0, 2, 5, 3], [4, 1, 4, 5, 2]])
    return _clip(pv.PolyData(pts, faces).triangulate())


def hatch_path(n_pts=36):
    pts = []
    for kind, (x, y), d in COUPONS:
        if kind == "box":
            w, h = d
            rows = max(3, int(h / 2.5))
            for r in range(rows):
                yy = y + (r + 0.5) * h / rows
                xs = (x, x + w) if r % 2 == 0 else (x + w, x)
                pts += [(xs[0], yy), (xs[1], yy)]
        else:
            for r in range(5):
                yy = y - d + (r + 0.5) * 2 * d / 5
                hw = math.sqrt(max(d * d - (yy - y) ** 2, 0))
                xs = (x - hw, x + hw) if r % 2 == 0 else (x + hw, x - hw)
                pts += [(xs[0], yy), (xs[1], yy)]
    seg = np.array(pts)
    dist = np.r_[0, np.cumsum(np.linalg.norm(np.diff(seg, axis=0), axis=1))]
    t = np.linspace(0, dist[-1], n_pts)
    return np.c_[np.interp(t, dist, seg[:, 0]), np.interp(t, dist, seg[:, 1])]


def cycle_gif(parts, layers=2):
    sc = Scene(parts, (GW, GH))
    f = (0.0, 20.0, 60.0)
    xp, xe, xd = M.P["x_park"], M.P["x_end"], M.P["x_dose"]
    blade_off = 10.5                                   # blade front face relative to the carriage centre
    path = hatch_path(36)
    frames = []
    state = {"ovf": 2.0}

    def draw(n, dz, xb, spread_x=None, pile=None, lase_i=None, caption=""):
        sc.set(section=True, state={"recoater": xb - xp, "piston": -dz})
        sc.cam(orbit(f, 1050, -20, 12), f)
        zp = -dz
        sc.put("bed", bed_mesh(zp, zp + n * LAY), **POWDER)
        sc.put("layer", bed_mesh(zp + n * LAY, zp + (n + 1) * LAY, spread_x) if spread_x is not None else None, **POWDER)
        sc.put("coupons", coupon_mesh(zp, zp + n * LAY), color=hex2rgb("#d9dde0"), smooth_shading=False, specular=0.4, ambient=0.25)
        sc.put("hot", coupon_mesh(zp + n * LAY, zp + (n + 1) * LAY) if lase_i is not None else None, color=hex2rgb(M.C["hot"]), smooth_shading=False, ambient=0.6)
        sc.put("pile", pile, **POWDER)
        if lase_i is not None:
            x, y = path[lase_i]
            zt = zp + (n + 1) * LAY
            sc.put("beam", pv.Line((0, 0, M.P["z_lens0"]), (x, y, zt)).tube(radius=0.9), color=hex2rgb(M.C["beam"]), ambient=1.0, diffuse=0.0, specular=0.0)
            sc.put("spot", pv.Sphere(radius=2.6, center=(x, y, zt + 0.5)), color=(1.0, 0.95, 0.55), ambient=1.0, diffuse=0.0)
        else:
            sc.put("beam", None)
            sc.put("spot", None)
        sc.title(caption, 11)
        frames.append(sc.shot())

    n = 3
    for layer in range(layers):
        tag = f"Layer {n + 1} (layer thickness exaggerated ~100x)"
        for k in range(6):
            draw(n, n * LAY + LAY * ease((k + 1) / 6), xe, caption=f"{tag}: build piston steps down one layer")
        dz = (n + 1) * LAY
        for k in range(9):
            draw(n, dz, xe + (xp - xe) * ease((k + 1) / 9), caption=f"{tag}: recoater returns over the lowered bed")
        vol = math.pi * R_PL * R_PL * LAY * 1.6
        for k in range(6):
            draw(n, dz, xp, pile=wedge(xd - 6, 12, 9.0 * ease((k + 1) / 6)), caption=f"{tag}: the metering roller drops one dose in front of the blade")
        for k in range(18):
            xb = xp + (xe - xp) * ease((k + 1) / 18)
            front = xb + blade_off
            used = 0.0 if front < -R_PL else min(1.0, (min(front, R_PL) + R_PL) / (2 * R_PL))
            left = max(vol * (1 - used / 1.6), 0)
            ph = left / (0.5 * 14.0 * 60) if left > 0 else 0
            if front > M.P["ovf_x0"]:
                ph = max(ph * (1 - (front - M.P["ovf_x0"]) / 20), 0)
            pile = wedge(front, 14.0, min(ph, 12.0)) if front < M.P["ovf_x1"] else None
            draw(n, dz, xb, spread_x=front, pile=pile, caption=f"{tag}: HSS blade spreads the layer, excess into the overflow")
        for i in range(len(path)):
            draw(n, dz, xe, spread_x=R_PL + 1, lase_i=i, caption=f"{tag}: galvo scans the coupons through the window (f = 160 mm)")
        n += 1
        draw(n, dz, xe, caption=f"Layer {n} done; argon cross-flow (back to front) clears the plume")
    save_gif(frames, OUT / "build-cycle.gif", ms=85, hold_last=10)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    what = sys.argv[1:] or ["stills", "assembly", "motion", "turntable", "cycle"]
    parts = M.build()
    t0 = time.time()
    if "stills" in what:
        stills(parts)
    if "assembly" in what:
        assembly_gif(parts)
    if "motion" in what:
        motion_gif(parts)
    if "turntable" in what:
        turntable_gif(parts)
    if "cycle" in what:
        cycle_gif(parts)
    print(f"render time {time.time() - t0:.0f} s")
