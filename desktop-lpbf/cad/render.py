"""Render the desktop LPBF model to PNGs and assembly / build-cycle GIFs.

Run (headless):  xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/cad/render.py [what ...]
  what: stills, assembly, turntable, cycle (default: all)
Writes to desktop-lpbf/cad/img/.
"""
from __future__ import annotations

import math
import pathlib
import sys
import time

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lpbf_model as M  # noqa: E402

pv.OFF_SCREEN = True
OUT = pathlib.Path(__file__).resolve().parent / "img"
W, H = 1200, 900           # stills
GW, GH = 760, 570          # GIF frames

# parts cut at y = 0 in the section views (keep y > 0)
SECTION_KEYS = ("Process chamber body", "Chamber floor plate", "Floor O-ring", "Chamber lid", "Lid O-ring", "Lid screws", "Window flange", "fused-silica window",
                "Window retaining ring", "Field-stop", "Cover-slide", "Gas knife", "Dose chute", "Dosing block",
                "Hopper", "Load cell", "Build cylinder", "Build plate", "Piston (", "Piston seal", "Overflow",
                "Deck plate", "Cross-flow outlet", "Rod clamp", "Z lift arm", "Blade holder", "Silicone-cord")
# parts hidden in the section views
SECTION_HIDE = ("Chamber door", "Door O-ring", "Door hinges", "Draw latches", "Door handle", "Laser guard", "Guard door",
                "OD 7+", "Guard-locking", "T-slot frame", "Gusset", "Leveling", "Operator panel", "E-stop", "Key switch",
                "Emission indicator", "Reset button", "Stack light", "Fiber laser", "Chiller", "Process fiber", "Outlet plenum KF",
                "O2 sample", "Gas-loop hoses", "Trace O2", "Argon", "DIN", "24 V", "Safety relay", "Motion controller",
                "Supervisor", "Scan + laser", "Terminal", "Controls enclosure", "Enclosure back", "Chamber dP", "Galvo plate",
                "Recirculation HEPA", "Recirculation blower", "Pump line", "Pump-line filter", "Vacuum pump", "Pump isolation")


_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def caption(img, text, sub=""):
    """Put a dark header band with the caption above a rendered frame."""
    im = Image.fromarray(img)
    band = 44 if sub else 30
    out = Image.new("RGB", (im.width, im.height + band), "#26323f")
    out.paste(im, (0, band))
    d = ImageDraw.Draw(out)
    try:
        f1, f2 = ImageFont.truetype(_FONT, 15), ImageFont.truetype(_FONT, 11)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    d.text((10, 6), text, fill="#ffffff", font=f1)
    if sub:
        d.text((10, 26), sub, fill="#b8c4d0", font=f2)
    return np.asarray(out)


def hex2rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


def tess(shape, tol=0.25, ang=0.3):
    vs, ts = shape.tessellate(tol, ang)
    if not ts:
        return None
    pts = np.array([(v.x, v.y, v.z) for v in vs], dtype=float)
    faces = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
    return pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


def clip_y(m, y0=0.0):
    c = m.clip(normal="-y", origin=(0, y0, 0), invert=True)
    return c if c.n_points else None


def has(name, keys):
    return any(k in name for k in keys)


MAT = dict(smooth_shading=True, specular=0.35, specular_power=18, ambient=0.2, diffuse=0.85)


class Scene:
    def __init__(self, parts, size, edges=True, flat=False):
        self.parts = parts
        self.pl = pv.Plotter(off_screen=True, window_size=size, lighting="three lights")
        if flat:
            self.pl.set_background("#eef2f6")
        else:
            self.pl.set_background("#f7f9fb", top="#dce5ee")
        self.actors = {}
        t0 = time.time()
        for p in parts:
            m = tess(p.shape)
            if m is None:
                continue
            col = hex2rgb(p.color)
            a = self.pl.add_mesh(m, color=col, opacity=p.opacity, **MAT)
            e = None
            if edges and p.opacity > 0.3:
                fe = m.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False, manifold_edges=False)
                if fe.n_points:
                    e = self.pl.add_mesh(fe, color=(0.12, 0.13, 0.15), line_width=1.0, opacity=0.5)
            s = None
            if has(p.name, SECTION_KEYS):
                cm = clip_y(m)
                if cm is not None:
                    s = self.pl.add_mesh(cm, color=col, opacity=max(p.opacity, 0.6), **MAT)
                    s.SetVisibility(False)
                else:
                    s = "empty"          # entirely in front of the cut: hide in section views
            self.actors[p.name] = (a, e, s, p)
        print(f"tessellated {len(self.actors)} parts in {time.time() - t0:.1f} s")
        self.pl.enable_anti_aliasing("ssaa")
        self.dyn = {}

    def set(self, visible=None, offsets=None, opacity=None, section=False):
        for name, (a, e, s, p) in self.actors.items():
            vis = True if visible is None else bool(visible(p))
            off = (0, 0, 0) if offsets is None else offsets(p)
            op = p.opacity if opacity is None else opacity(p)
            cut = section and s is not None
            hide = section and (has(p.name, SECTION_HIDE) or s == "empty")
            s = None if s == "empty" else s
            a.SetVisibility(vis and not cut and not hide)
            a.position = off
            a.prop.opacity = op
            if e is not None:
                e.SetVisibility(vis and not cut and not hide and op > 0.3)
                e.position = off
            if s is not None:
                s.SetVisibility(vis and cut)
                s.position = off

    def put(self, key, mesh, **kw):
        """Add or replace a dynamic actor (powder, part, beam ...)."""
        if key in self.dyn:
            self.pl.remove_actor(self.dyn.pop(key))
        if mesh is not None and mesh.n_points:
            self.dyn[key] = self.pl.add_mesh(mesh, **kw)

    def clear_dyn(self):
        for k in list(self.dyn):
            self.pl.remove_actor(self.dyn.pop(k))

    def title(self, text, sub=""):
        self.caption = (text, sub)

    def cam(self, pos, focal, up=(0, 0, 1), view_angle=30.0):
        self.pl.camera_position = [pos, focal, up]
        self.pl.camera.view_angle = view_angle

    def shot(self):
        self.pl.render()
        img = self.pl.screenshot(return_img=True)
        cap = getattr(self, "caption", None)
        return caption(img, *cap) if cap else img


def orbit(focal, dist, az_deg, el_deg):
    """Camera position: az 0 = straight in front (-y), positive az swings to the right (+x)."""
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


FOCAL = (-80.0, 0.0, 10.0)
AZ, EL, DIST = 32.0, 20.0, 2950.0


# --------------------------------------------------------------------------------------------
def stills(parts):
    sc = Scene(parts, (W, H))
    sc.cam(orbit(FOCAL, DIST, AZ, EL), FOCAL)
    Image.fromarray(sc.shot()).save(OUT / "overview.png")
    sc.set(visible=lambda p: p.step != 13)
    Image.fromarray(sc.shot()).save(OUT / "overview-open.png")
    # back view, no guard
    sc.cam(orbit(FOCAL, DIST, 180 + 35, 18), FOCAL)
    Image.fromarray(sc.shot()).save(OUT / "overview-back.png")
    # exploded view
    clutter = ("front column", "Operator", "E-stop", "Key switch", "Emission", "Reset", "Stack light")
    sc.set(visible=lambda p: p.step not in (12, 13) and not has(p.name, clutter), offsets=lambda p: tuple(0.9 * e for e in p.explode))
    sc.cam(orbit(FOCAL, DIST * 1.25, AZ, EL), FOCAL)
    Image.fromarray(sc.shot()).save(OUT / "exploded.png")
    # chamber section
    f2 = (0.0, 10.0, 40.0)
    sc.set(section=True)
    sc.cam(orbit(f2, 1050, -22, 12), f2)
    Image.fromarray(sc.shot()).save(OUT / "section.png")
    print("stills done")


# --------------------------------------------------------------------------------------------
def assembly_gif(parts, frames_per_step=9):
    sc = Scene(parts, (GW, GH), flat=True)
    f = (-30.0, 0.0, 10.0)
    sc.cam(orbit(f, 2550, AZ, EL), f)
    frames = []
    n_steps = max(M.STEPS)
    for s in range(1, n_steps + 1):
        for k in range(frames_per_step):
            t = ease((k + 1) / (frames_per_step - 2))

            def vis(p, s=s):
                return p.step <= s

            def off(p, s=s, t=t):
                return tuple((1 - t) * e for e in p.explode) if p.step == s else (0, 0, 0)

            def opa(p, s=s, t=t):
                return p.opacity * (0.25 + 0.75 * t) if p.step == s else p.opacity
            sc.set(visible=vis, offsets=off, opacity=opa)
            sc.title(f"Step {s}/{n_steps}: {M.STEPS[s]}", "Desktop LPBF concept, issue #260 (CadQuery model: desktop-lpbf/cad/lpbf_model.py)")
            frames.append(sc.shot())
    sc.title("Assembled: ~6 L vacuum-purged chamber, fixed galvo + f-theta, Ø53 mm plate, Class 1 guard",
             "Desktop LPBF concept, issue #260 (CadQuery model: desktop-lpbf/cad/lpbf_model.py)")
    frames.append(sc.shot())
    save_gif(frames, OUT / "assembly.gif", ms=110, hold_last=18)


def turntable_gif(parts, n=36):
    sc = Scene(parts, (GW, GH), flat=True)
    sc.title("Desktop LPBF concept with the laser guard removed", "CadQuery model: desktop-lpbf/cad/lpbf_model.py")
    sc.set(visible=lambda p: p.step not in (12, 13))
    f = (-40.0, 0.0, 20.0)
    frames = []
    for i in range(n):
        sc.cam(orbit(f, 2500, AZ + 360 * i / n, 18), f)
        frames.append(sc.shot())
    save_gif(frames, OUT / "turntable.gif", ms=100, hold_last=0)


# --------------------------------------------------------------------------------------------
# Build cycle: dose -> spread -> lase -> piston down -> recoater back.  Layers exaggerated for visibility.
L = 4.0                     # shown layer thickness (mm); real layers are 0.02-0.06 mm
N0 = 4                      # layers already built when the GIF starts
R = M.P["plate_d"] / 2
COUPONS = [("box", (-16, -6, 0), (10, 12)), ("cyl", (8, 0, 0), 5.0), ("box", (-2, -18, 0), (14, 3))]
POWDER = dict(color=hex2rgb("#5d6268"), smooth_shading=False, specular=0.05, ambient=0.3, diffuse=0.8)


def prism(poly_xy, z0, z1):
    """Closed prism from a 2-D polygon (list of (x, y), counter-clockwise) between z0 and z1."""
    if z1 - z0 < 1e-3 or len(poly_xy) < 3:
        return None
    pts = np.array([(x, y, z0) for x, y in poly_xy], float)
    face = np.r_[len(pts), np.arange(len(pts))]
    return pv.PolyData(pts, face).extrude((0, 0, z1 - z0), capping=True).triangulate()


def half_disc(r, cx=0.0, xmax=None, n=48):
    """Back half (y >= 0) of a disc of radius r centred on (cx, 0), optionally cut at x <= xmax."""
    if xmax is not None and xmax <= cx - r:
        return []
    t0 = 0.0 if xmax is None or xmax >= cx + r else math.acos((xmax - cx) / r)
    arc = [(cx + r * math.cos(a), r * math.sin(a)) for a in np.linspace(t0, math.pi, n)]
    poly = arc + [(cx - r, 0.0)]
    poly.append((cx + r if xmax is None or xmax >= cx + r else xmax, 0.0))
    return poly


def bed_mesh(z0, z1, xmax=None):
    return prism(half_disc(R, 0.0, xmax), z0, z1)


def coupon_mesh(z0, z1):
    ms = []
    for kind, (x, y, _), d in COUPONS:
        if kind == "box":
            ya, yb = max(y, 0.0), y + d[1]
            if yb > ya:
                ms.append(prism([(x, ya), (x + d[0], ya), (x + d[0], yb), (x, yb)], z0, z1))
        else:
            ms.append(prism(half_disc(d, x), z0, z1))
    ms = [m for m in ms if m is not None]
    if not ms:
        return None
    m = ms[0].merge(ms[1:]) if len(ms) > 1 else ms[0]
    return m.translate((0, -0.3, 0), inplace=False)


def wedge(x_front, length, height, y1=30.0):
    """Powder pile in front of the blade (back half, y >= 0): triangular prism, toe at x_front + length."""
    if height < 0.05 or length < 0.05:
        return None
    xa, xb = x_front, x_front + length
    pts = np.array([[xa, 0, 0], [xb, 0, 0], [xa, 0, height], [xa, y1, 0], [xb, y1, 0], [xa, y1, height]], float)
    faces = np.hstack([[3, 0, 1, 2], [3, 3, 5, 4], [4, 0, 3, 4, 1], [4, 0, 2, 5, 3], [4, 1, 4, 5, 2]])
    return pv.PolyData(pts, faces).triangulate()


def hatch_path(n_pts=40):
    """Scan points for one layer: zig-zag over each coupon's cross-section."""
    pts = []
    for kind, (x, y, _), d in COUPONS:
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
    # resample to n_pts evenly along the path
    seg = np.array(pts)
    dist = np.r_[0, np.cumsum(np.linalg.norm(np.diff(seg, axis=0), axis=1))]
    s = np.linspace(0, dist[-1], n_pts)
    return np.c_[np.interp(s, dist, seg[:, 0]), np.interp(s, dist, seg[:, 1])]


def cycle_gif(parts, layers=2):
    sc = Scene(parts, (GW, GH), flat=True)
    f = (-12.0, 10.0, 18.0)
    sc.cam(orbit(f, 440, -16, 12), f, view_angle=30)
    xp, xe, xd = M.P["x_park"], M.P["x_end"], M.P["x_dose"]
    lens_z = M.P["lens_wd"]
    frames = []
    hot = hex2rgb(M.C["hot"])
    part_col = hex2rgb(M.C["part"])
    ovf_h = 2.0
    path = hatch_path(36)

    def draw(n, dz, xb, spread_x=None, pile=None, lase_i=None, hot_top=False, caption=""):
        """n: completed layers; dz: piston drop; xb: blade x; spread_x: new layer present for x < spread_x."""
        sc.set(section=True, offsets=lambda p: (xb - xp, 0, 0) if p.group == "recoater" else
               ((0, 0, -dz) if p.group == "piston" else (0, 0, 0)))
        zp = -dz
        sc.put("bed", bed_mesh(zp, zp + n * L), **POWDER)
        sc.put("layer", bed_mesh(zp + n * L, zp + (n + 1) * L, spread_x) if spread_x is not None else None, **POWDER)
        sc.put("coupons", coupon_mesh(zp, zp + n * L), color=part_col, smooth_shading=False, specular=0.4, ambient=0.25)
        if lase_i is not None or hot_top:
            sc.put("hot", coupon_mesh(zp + n * L, zp + (n + 1) * L), color=hot, smooth_shading=False, ambient=0.6)
        else:
            sc.put("hot", None)
        sc.put("pile", pile, **POWDER)
        zj = -20 - 16 - 70
        sc.put("ovf", prism(half_disc(19.0, 70.0), zj, zj + ovf_h), **POWDER)
        if lase_i is not None:
            x, y = path[lase_i]
            zt = zp + (n + 1) * L
            sc.put("beam", pv.Line((0, 0, lens_z), (x, y, zt)).tube(radius=1.3), color=hex2rgb(M.C["beam"]), ambient=1.0, diffuse=0.0, specular=0.0)
            sc.put("beam_in", pv.Line((-300, 0, M.P["beam_z"]), (0, 0, M.P["beam_z"])).tube(radius=1.2), color=hex2rgb(M.C["beam"]), ambient=1.0, diffuse=0.0)
            sc.put("spot", pv.Sphere(radius=2.6, center=(x, y, zt + 0.5)), color=(1.0, 0.95, 0.55), ambient=1.0, diffuse=0.0)
            arrows = [pv.Arrow(start=(xa, 72, 8), direction=(0, -1, 0), scale=64, tip_length=0.18, tip_radius=0.06, shaft_radius=0.02)
                      for xa in (-28, -10, 8, 26)]
            sc.put("flow", arrows[0].merge(arrows[1:]), color=(0.35, 0.62, 0.95), opacity=0.75, ambient=0.5)
        else:
            for k in ("beam", "beam_in", "spot", "flow"):
                sc.put(k, None)
        sc.title(caption, "Section at y = 0 through the chamber and build cylinder; layer thickness exaggerated ~100x")
        frames.append(sc.shot())

    n = N0
    for layer in range(layers):
        tag = f"Layer {n + 1}"
        # piston down one layer, recoater still parked at the right after the last spread
        for k in range(6):
            draw(n, n * L + L * ease((k + 1) / 6), xe, caption=f"{tag}: build piston steps down one layer")
        dz = (n + 1) * L
        for k in range(9):
            draw(n, dz, xe + (xp - xe) * ease((k + 1) / 9), caption=f"{tag}: recoater returns over the lowered bed")
        # dose: fluted roller drops a line of powder in front of the blade
        vol = math.pi * R * R * L * 1.6           # dose factor 1.6
        for k in range(6):
            hgt = 9.0 * ease((k + 1) / 6)
            draw(n, dz, xp, pile=wedge(xd - 6, 12, hgt), caption=f"{tag}: hopper meters one dose (load cell weighs it)")
        # spread
        nfr = 18
        for k in range(nfr):
            xb = xp + (xe - xp) * ease((k + 1) / nfr)
            front = xb + 7
            used = 0.0 if front < -R else min(1.0, (min(front, R) + R) / (2 * R))
            left = max(vol * (1 - used / 1.6) - (0 if front < M.P["ovf_x0"] else vol), 0)
            plen = 14.0
            ph = left / (0.5 * plen * 60) if left > 0 else 0
            if front > M.P["ovf_x0"]:
                ph = max(ph * (1 - (front - M.P["ovf_x0"]) / 20), 0)
            pile = wedge(front, plen, min(ph, 12.0)) if front < M.P["ovf_x1"] else None
            if front > M.P["ovf_x0"]:
                ovf_h = min(ovf_h + 0.35, 14)
            draw(n, dz, xb, spread_x=front, pile=pile, caption=f"{tag}: compliant blade spreads the layer, excess to overflow")
        # lase
        for i in range(len(path)):
            draw(n, dz, xe, spread_x=R + 1, lase_i=i, caption=f"{tag}: galvo scans the coupons through the window; argon cross-flow (blue) sweeps the plume")
        n += 1
        draw(n, dz, xe, spread_x=None, hot_top=False, caption=f"Layer {n} done")
    save_gif(frames, OUT / "build-cycle.gif", ms=85, hold_last=10)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    what = sys.argv[1:] or ["stills", "assembly", "turntable", "cycle"]
    parts = M.build()
    t0 = time.time()
    if "stills" in what:
        stills(parts)
    if "assembly" in what:
        assembly_gif(parts)
    if "turntable" in what:
        turntable_gif(parts)
    if "cycle" in what:
        cycle_gif(parts)
    print(f"render time {time.time() - t0:.0f} s")
