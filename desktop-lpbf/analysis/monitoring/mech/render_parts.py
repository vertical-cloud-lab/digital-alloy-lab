"""Render the monitoring hardware as drawn in the model (cad/monitoring_parts.py; monitoring/mechanics.md).

Builds lpbf_low with monitoring=True and writes five PNGs to analysis/out/monitoring/mech/:
  overview.png   the process module, monitoring parts in colour, the rest grey; guard and bridge posts hidden
  lw.png         the left-wall port, its purge and the Chronos 2.1-HD on its post
  lp.png         the steep lid port (LP), its boss and camera, and the cut-out in the optics bridge
  cage.png       the coaxial branch above the bridge: cubes 1-3, the camera arm, photodiodes A and B, the beam trap
  ae.png         a section through the build module at the waveguide: plate, heater block, break, piston head, rod, rod end,
                 the AE sensor on the rod end's back face

Run:  xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/mech/render_parts.py [name ...]
"""
from __future__ import annotations

import io
import pathlib
import sys

import numpy as np
import pyvista as pv
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "cad"))
import lpbf_low as M  # noqa: E402

pv.OFF_SCREEN = True
OUT = ROOT / "analysis" / "out" / "monitoring" / "mech"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1300, 860
HIDE = ("Laser guard", "Sliding guard", "OD 7+", "Guard door rail", "Guard-locking", "Guard frame", "Operator panel", "E-stop",
        "Key switch", "Emission indicator", "Reset button", "VLM tray", "Calibration", "Optics bridge posts")
MAT = dict(smooth_shading=True, specular=0.15, specular_power=12, ambient=0.28, diffuse=0.8)


def hex2rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


def tess(shape, tol=0.2, ang=0.3):
    vs, ts = shape.tessellate(tol, ang)
    if not ts:
        return None
    pts = np.array([(v.x, v.y, v.z) for v in vs], dtype=float)
    faces = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
    return pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


def mon(p):
    return "monitoring" in p.tags


def scene(parts, view, box=None, clip=None, grey_op=0.35, mon_op=1.0, hide=HIDE, keep=None, title="", recolour=None):
    pl = pv.Plotter(off_screen=True, window_size=(W, H), lighting="three lights")
    pl.set_background("#f7f9fb", top="#dfe6ee")
    for p in parts:
        if any(k in p.name for k in hide) or (keep and not keep(p)):
            continue
        bb = p.shape.BoundingBox()
        if box and (bb.xmax < box[0] or bb.xmin > box[1] or bb.ymax < box[2] or bb.ymin > box[3] or bb.zmax < box[4] or bb.zmin > box[5]):
            continue
        m = tess(p.shape)
        if m is None:
            continue
        if clip is not None:
            m = m.clip(normal=clip[0], origin=clip[1], invert=False)
            if not m.n_points:
                continue
        if mon(p):
            col, op = hex2rgb(p.color), (min(p.opacity, 0.6) if p.opacity < 1 else mon_op)
            if recolour:
                col = recolour(p) or col
            if p.color.lower() in ("#151719", "#25292e", "#2d3136"):
                col = tuple(0.15 + 0.85 * c for c in hex2rgb("#2b6cd2")) if "camera" in p.name.lower() and "lens" not in p.name.lower() else col
        else:
            col, op = (0.80, 0.82, 0.85), grey_op * p.opacity
        pl.add_mesh(m, color=col, opacity=op, **MAT)
        if mon(p) and op > 0.5:
            fe = m.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False, manifold_edges=False)
            if fe.n_points:
                pl.add_mesh(fe, color=(0.1, 0.1, 0.12), line_width=1.0, opacity=0.5)
    pl.camera_position = view
    pl.enable_anti_aliasing("ssaa")
    if title:
        pl.add_text(title, position="upper_left", font_size=11, color="#1d2733", font="arial")
    img = pl.screenshot(return_img=True)
    pl.close()
    return img


def save(img, name):
    im = Image.fromarray(img).convert("RGB")
    path = OUT / name
    q = im.quantize(colors=200, method=Image.Quantize.MEDIANCUT)
    q.save(path, optimize=True)
    if path.stat().st_size > 400_000:
        im.resize((im.width * 3 // 4, im.height * 3 // 4), Image.LANCZOS).quantize(colors=160).save(path, optimize=True)
    print(name, path.stat().st_size // 1024, "kB", flush=True)


def main(which):
    parts = M.build(include_tray=True, module="M50", monitoring=True)
    state_parts = parts
    if "overview" in which:
        save(scene(state_parts, [(-760, -720, 560), (-170, -10, 90), (0, 0, 1)], box=(-425, 330, -300, 260, -230, 420),
                   keep=lambda p: p.module == "process",
                   title="Monitoring hardware in the process module (colour); the rest grey. Guard and bridge posts hidden."), "overview.png")
    if "lw" in which:
        save(scene(state_parts, [(-520, -620, 260), (-250, -25, 40), (0, 0, 1)], box=(-430, -100, -200, 140, -170, 200),
                   title="LW: Ø40 x 4 window flat on the wall, clamp ring, purge, Chronos 2.1-HD on the sight line"), "lw.png")
    if "lp" in which:
        save(scene(state_parts, [(-330, 330, 430), (-50, 70, 185), (0, 0, 1)], box=(-150, 80, 0, 230, 100, 320),
                   title="LP at (-40, 60): boss with the window square to the line of sight, IMX296 camera, cut-out in the optics bridge"),
             "lp.png")
    if "cage" in which:
        save(scene(state_parts, [(-520, -480, 560), (-270, -60, 270), (0, 0, 1)], box=(-430, -110, -230, 140, 200, 340),
                   title="Coaxial branch as a 30 mm cage: cube 1 (DMSP1000), cube 2 (DMSP950, camera arm), cube 3 (DMLP805, PD-A, PD-B)"),
             "cage.png")
    if "ae" in which:
        import monitoring_parts as MPT
        y_cut = MPT.REPORT.get("AE", {}).get("waveguide_xy", (0.0, 3.03))[1]
        def ae_col(p):
            return (0.95, 0.35, 0.05) if "waveguide" in p.name else ((0.15, 0.4, 0.95) if "sensor" in p.name.lower() else None)
        save(scene(state_parts, [(-150, -260, -40), (-5, 10, -75), (0, 0, 1)], box=(-90, 90, -40, 70, -150, 2),
                   clip=((0, 1, 0), (0, y_cut, 0)), grey_op=0.55, recolour=ae_col,
                   keep=lambda p: "M50" in p.name or (mon(p) and ("AE " in p.name)) or "Z lift arm" in p.name or "Pot magnet" in p.name,
                   hide=HIDE + ("Gland-plate screws", "handle", "Zero-point"),
                   title="AE path, section at the waveguide: plate, heater block, break, piston head, rod, rod end; sensor on the rod end"),
             "ae.png")


if __name__ == "__main__":
    main(sys.argv[1:] or ["overview", "lw", "lp", "cage", "ae"])
