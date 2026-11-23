"""Renders for the OEM-part refinement and the logos (issue #260, oem-parts.md). Own script: render_low.py / render_build.py
are not touched (another run edits them).

    xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/cad/oem/render_oem.py [logos] [parts]

- logos: close-ups of the VCL lockup deboss on the chamber door and the BYU block Y on the 4U drawer (builds the M50 model once).
- parts: every refined bought part, before (vendor_parts.py at 0dbb5a3) and after (this tree), each body in its measured finish.
Finishes come from cad/oem/finishes.json (measured from vendor photos: base colour in linear RGB, metallic, roughness); bodies not in it
fall back to FALLBACK below (the colours the model used, marked "assumed"). pyvista's Phong shading stands in for PBR: specular strength
and power are mapped from metallic and roughness, and the linear colour is converted back to sRGB for display.
Writes desktop-lpbf/cad/img/oem/.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

import cadquery as cq
import numpy as np
import pyvista as pv

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parent
sys.path.insert(0, str(CAD))
import vendor_parts as VP  # noqa: E402

pv.OFF_SCREEN = True
OUT = CAD / "img" / "oem"
BEFORE = pathlib.Path("/tmp/agentE/before_vp/vendor_parts.py")     # git show 0dbb5a3:desktop-lpbf/cad/vendor_parts.py

FALLBACK = {   # assumed finishes: (sRGB hex, metallic, roughness)
    "default": ("#8a8f96", 0.0, 0.5),
    "ipg_ylr500_u3": {"chassis": ("#1f2124", 0.0, 0.55), "front_panel": ("#c9ccd0", 0.6, 0.35), "control_strip": ("#4a4e54", 0.0, 0.5),
                      "display": ("#9fc7e6", 0.0, 0.1), "fan_grille": ("#111214", 0.0, 0.6), "start_button": ("#2fae4a", 0.0, 0.3),
                      "estop": ("#c8231e", 0.0, 0.3), "key_switch": ("#c0c3c7", 1.0, 0.25), "handles": ("#16171a", 0.0, 0.45)},
    "eaton_5px1500rtg2": {"chassis": ("#202226", 0.0, 0.55), "rack_ears": ("#2a2c30", 0.3, 0.5), "bezel": ("#3b3e44", 0.0, 0.5),
                          "badge": ("#d9dadc", 0.8, 0.3), "grille": ("#b9bcc0", 0.8, 0.4), "lcd_module": ("#141518", 0.0, 0.35),
                          "lcd_screen": ("#5aa0e0", 0.0, 0.1), "led_bar": ("#1e7be0", 0.0, 0.2)},
}


def finishes():
    f = HERE / "finishes.json"
    return json.loads(f.read_text()) if f.exists() else {}


def srgb(lin):
    lin = np.clip(np.asarray(lin, float), 0, 1)
    return tuple(np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055))


def hex2rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


# our body names -> the measured entries of finishes.json (photo-fork names); zones split a one-body part's mesh by cell centre
ALIAS = {
    "ipg_ylr500_u3": {"chassis": "chassis side (black)", "front_panel": "front panel, light area (left)",
                      "fan_grille": "front panel, dark dot-pattern area", "handles": "rack handles (black)"},
    "eaton_5px1500rtg2": {"grille": "grille (perforated silver bezel, holes included)", "lcd_module": "display module surround (black)",
                          "lcd_screen": "LCD (lit, blue-white)", "led_bar": "status light bar (blue)", "badge": "Eaton badge"},
    "clearpath_sd_231x": {"body": "body (black anodised extrusion)", "flange": "flange (machined/cast aluminium front plate)",
                          "fins": "rear housing (die-cast aluminium, fins)", "connectors": "connectors (black plastic)", "shaft": "shaft (ground steel)"},
    "mcm_6627T91": {"body": "housing and end caps (black)", "front": "front face, pilot and shaft (aluminium/steel)"},
    "mcm_6709K12": {"body": "steel block", "caps": "end caps and seals (black plastic)"},
    "mcm_4566N401": {"body": "nut and flange (steel)"},
    "mcm_4123K45": {"body": "body, end caps, tie bolts (cast 316 stainless)", "flanges": "KF flanges (machined stainless)", "grip": "lever grip (grey vinyl)"},
    "mcm_4518K72": {"body": "clamp (aluminium)"},
    "mcm_5786N25": {"body": ("mcm_5786N23", "fitting (aluminium)")},          # same alloy and finish as the KF-25 fitting
    "mcm_3861N11": {"body": "body and cable (black)", "hex": "hex and thread (stainless)"},
    "mcm_5169K72": {"body": "housing (black)"},
}
ZONES = {      # key -> f(cell centres Nx3) -> array of zone names (local frames as in vendor_parts)
    "clearpath_sd_231x": lambda c: np.where(c[:, 2] > 0.01, "shaft", np.where(c[:, 2] > -6.05, "flange", np.where(c[:, 1] > 29.6, "connectors",
                                            np.where(c[:, 2] < -75.0, "fins", "body")))),
    "mcm_6627T91": lambda c: np.where(c[:, 2] > -0.01, "front", "body"),
    "mcm_6709K12": lambda c: np.where(np.abs(c[:, 0]) > 19.45, "caps", "body"),
    "mcm_4123K45": lambda c: np.where(c[:, 2] > 80.0, "grip", np.where((c[:, 0] < 18.0) | (c[:, 0] > 106.2), "flanges", "body")),
    "mcm_3861N11": lambda c: np.where(c[:, 2] < 9.0, "hex", "body"),
}


def finish_for(key, body):
    F = finishes()
    a = ALIAS.get(key, {}).get(body)
    k2, name = a if isinstance(a, tuple) else (key, a)
    e = F.get(k2, {}).get(name) if name else F.get(key, {}).get(body)
    if e and "linear_rgb" in e:
        return srgb(e["linear_rgb"]), float(e.get("metallic", 0.0)), float(e.get("roughness", 0.5)), f"measured: {k2} / {name or body}"
    fb = FALLBACK.get(key, {})
    h, m, r = (fb.get(body) if isinstance(fb, dict) else None) or FALLBACK["default"]
    return hex2rgb(h), m, r, "assumed"


def phong(m, r):
    return dict(smooth_shading=True, ambient=0.22, diffuse=0.78 - 0.25 * m, specular=0.08 + 0.55 * m * (1 - r) + 0.15 * (1 - r),
                specular_power=4 + 60 * (1 - r) ** 2)


def tess(shape, tol=0.05, ang=0.2):
    vs, ts = shape.tessellate(tol, ang)
    if not ts:
        return None
    pts = np.array([(v.x, v.y, v.z) for v in vs], float)
    faces = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
    return pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=30, auto_orient_normals=False)


def load_before():
    spec = importlib.util.spec_from_file_location("vp_before", BEFORE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# builder key -> (callable on a vendor_parts module, label); bodies=True where the builder offers named bodies
PARTS = [
    ("ipg_ylr500_u3", lambda m: m.ipg_ylr500_u3, "IPG YLR-500-U3 (4U)"),
    ("eaton_5px1500rtg2", lambda m: m.eaton_5px1500rtg2, "Eaton 5PX1500RTG2 (2U)"),
    ("clearpath_sd_231x", lambda m: m.clearpath_sd_231x, "Teknic ClearPath CPM-SDSK-231x"),
    ("mcm_6627T91", lambda m: m.mcm_6627T91, "McMaster 6627T91 NEMA 17"),
    ("mcm_6709K12", lambda m: m.mcm_6709K12, "McMaster 6709K12 carriage"),
    ("mcm_4566N401", lambda m: m.mcm_4566N401, "McMaster 4566N401 ball nut"),
    ("mcm_4123K45", lambda m: (lambda: m.mcm_4123K45("-x")), "McMaster 4123K45 KF-25 valve"),
    ("mcm_4518K72", lambda m: (lambda: m.kf_wing_clamp(25)), "McMaster 4518K72 KF-25 clamp"),
    ("mcm_5786N25", lambda m: (lambda: m.kf_weld_stub(40)), "McMaster 5786N25 KF-40 stub"),
    ("mcm_3861N11", lambda m: m.mcm_3861N11, "McMaster 3861N11 transmitter"),
    ("mcm_5169K72", lambda m: m.mcm_5169K72, "McMaster 5169K72 filter housing"),
]


def bodies_of(fn):
    try:
        d = fn(bodies=True)
        if isinstance(d, dict):
            return d
    except TypeError:
        pass
    return {"body": fn()}


def add_part(pl, key, fn, offset=(0, 0, 0)):
    used = {}
    for body, shp in bodies_of(fn).items():
        mesh = tess(shp)
        if mesh is None:
            continue
        if body == "body" and key in ZONES:
            zone = ZONES[key](np.asarray(mesh.cell_centers().points))
            subs = [(z, mesh.extract_cells(np.where(zone == z)[0]).extract_surface()) for z in np.unique(zone)]
        else:
            subs = [(body, mesh)]
        for z, sm in subs:
            if sm.n_cells == 0:
                continue
            rgb, m, r, src = finish_for(key, z)
            used[z] = src
            sm = sm.compute_normals(split_vertices=True, feature_angle=30, auto_orient_normals=False)
            pl.add_mesh(sm.translate(offset, inplace=False), color=rgb, **phong(m, r))
    return used


def view_for(shape):
    b = shape.BoundingBox()
    c = np.array([(b.xmin + b.xmax) / 2, (b.ymin + b.ymax) / 2, (b.zmin + b.zmax) / 2])
    d = max(b.xlen, b.ylen, b.zlen)
    return c, d


def parts_grid():
    OUT.mkdir(parents=True, exist_ok=True)
    before = load_before() if BEFORE.exists() else None
    tiles, report = [], {}
    for key, get, label in PARTS:
        row = []
        for tag, mod in (("before", before), ("after", VP)):
            if mod is None:
                continue
            fn = get(mod)
            shape = fn()
            c, d = view_for(shape)
            pl = pv.Plotter(off_screen=True, window_size=(640, 480), lighting="none")
            pl.set_background("#f4f6f8", top="#d9e0e8")
            used = add_part(pl, key, fn)
            pl.add_light(pv.Light(position=tuple(c + np.array([-1.2, -2.0, 1.6]) * d), focal_point=tuple(c), intensity=0.95))
            pl.add_light(pv.Light(position=tuple(c + np.array([2.0, -0.6, 0.4]) * d), focal_point=tuple(c), intensity=0.35))
            pl.add_light(pv.Light(position=tuple(c + np.array([0.3, 1.5, 1.0]) * d), focal_point=tuple(c), intensity=0.25))
            pl.camera.focal_point = tuple(c)
            pl.camera.position = tuple(c + np.array([-0.9, -1.7, 0.75]) * d * 1.25)
            pl.camera.up = (0, 0, 1)
            pl.camera.view_angle = 30
            pl.add_text(f"{label}: {tag}", position="upper_left", font_size=9, color="#222222")
            img = pl.screenshot(return_img=True)
            pl.close()
            row.append(img)
            report.setdefault(key, {})[tag] = used
        tiles.append(np.hstack(row))
    for i in range(0, len(tiles), 4):
        grid = np.vstack(tiles[i:i + 4])
        pv.wrap(grid)  # noqa: B018 (keeps pyvista import used)
        from PIL import Image
        Image.fromarray(grid).resize((grid.shape[1] * 3 // 4, grid.shape[0] * 3 // 4), Image.LANCZOS).quantize(colors=160).save(OUT / f"before_after_{i // 4 + 1}.png", optimize=True)
    (OUT / "finish_sources.json").write_text(json.dumps(report, indent=1))
    print("parts grid:", len(tiles), "parts")


def logos():
    import lpbf_low as M
    import logos as L
    OUT.mkdir(parents=True, exist_ok=True)
    parts = M.build(include_tray=False, fasteners=False)   # light build: the debosses do not depend on the fasteners
    # vcl: the bare deboss in the door's 6061 under a raking light; y: the deboss filled with BYU navy (#1e3158, one of the brand
    # guide's three colours for the block Y), as suggested for the drawer panel
    yc = L.LAST["y"]["centre_xz"]
    shots = {"vcl": dict(focus=(0.0, -126.0, 50.0), cam=(-120.0, -520.0, 140.0), keep=("Chamber", "Door", "Draw-latch", "Hinge", "Base plate, process"),
                         size=(1400, 800), angle=34, fill=None),
             "y": dict(focus=(yc[0] + 40.0, -274.0, yc[1]), cam=(-150.0, -420.0, 110.0),
                       keep=("DIN-rail drawer", "Scan + laser", "19 in. rack", "Rack side", "Fiber laser"), size=(1400, 800), angle=30, fill="#1e3158")}
    from PIL import Image
    for key, s in shots.items():
        if s["fill"]:
            for fc in L.LAST[key]["faces"]:          # paint fill: the deboss floor, 0.05 mm proud of it
                m = tess(fc.translate(cq.Vector(0, -0.05, 0)), tol=0.02)
                if m is not None:
                    s.setdefault("fill_meshes", []).append(m)
        pl = pv.Plotter(off_screen=True, window_size=s["size"], lighting="none")
        pl.set_background("#eef1f4", top="#cfd8e2")
        for p in parts:
            if not p.name.startswith(s["keep"]) or "context" in p.tags:
                continue
            mesh = tess(p.shape, tol=0.03 if p.name == L.LAST[key]["part"] else 0.3)
            if mesh is None:
                continue
            col = hex2rgb(p.color)
            if p.name == L.LAST[key]["part"]:
                pl.add_mesh(mesh, color=col, smooth_shading=True, ambient=0.18, diffuse=0.85, specular=0.35, specular_power=30)
            else:
                pl.add_mesh(mesh, color=col, opacity=min(p.opacity, 1.0), smooth_shading=True, ambient=0.25, diffuse=0.75, specular=0.1)
        for m in s.get("fill_meshes", []):
            pl.add_mesh(m, color=hex2rgb(s["fill"]), smooth_shading=False, ambient=0.3, diffuse=0.7, specular=0.05)
        f = np.array(s["focus"])
        pl.add_light(pv.Light(position=tuple(f + np.array([-420.0, -160.0, 120.0])), focal_point=tuple(f), intensity=1.0, positional=True, cone_angle=60))   # raking light
        pl.add_light(pv.Light(position=tuple(f + np.array([300.0, -500.0, 300.0])), focal_point=tuple(f), intensity=0.35))
        pl.camera.focal_point = tuple(f)
        pl.camera.position = tuple(f + np.array(s["cam"]))
        pl.camera.up = (0, 0, 1)
        pl.camera.view_angle = s["angle"]
        img = pl.screenshot(return_img=True)
        pl.close()
        Image.fromarray(img).quantize(colors=200).save(OUT / f"logo_{key}.png", optimize=True)
        print("wrote", OUT / f"logo_{key}.png")


if __name__ == "__main__":
    what = sys.argv[1:] or ["logos", "parts"]
    if "parts" in what:
        parts_grid()
    if "logos" in what:
        logos()
