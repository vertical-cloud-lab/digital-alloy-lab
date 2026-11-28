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
BEFORE_R6 = pathlib.Path("/tmp/oem/vendor_parts_before.py")         # round 6: git show 4b2232e:desktop-lpbf/cad/vendor_parts.py

FALLBACK = {   # assumed finishes: (sRGB hex, metallic, roughness)
    "default": ("#8a8f96", 0.0, 0.5),
    "ipg_ylr500_u3": {"chassis": ("#1f2124", 0.0, 0.55), "front_panel": ("#c9ccd0", 0.6, 0.35), "control_strip": ("#4a4e54", 0.0, 0.5),
                      "display": ("#9fc7e6", 0.0, 0.1), "fan_grille": ("#111214", 0.0, 0.6), "start_button": ("#2fae4a", 0.0, 0.3),
                      "estop": ("#c8231e", 0.0, 0.3), "key_switch": ("#c0c3c7", 1.0, 0.25), "handles": ("#16171a", 0.0, 0.45)},
    "eaton_5px1500rtg2": {"chassis": ("#202226", 0.0, 0.55), "rack_ears": ("#2a2c30", 0.3, 0.5), "bezel": ("#3b3e44", 0.0, 0.5),
                          "badge": ("#d9dadc", 0.8, 0.3), "grille": ("#b9bcc0", 0.8, 0.4), "lcd_module": ("#141518", 0.0, 0.35),
                          "lcd_screen": ("#5aa0e0", 0.0, 0.1), "led_bar": ("#1e7be0", 0.0, 0.2), "keys": ("#111017", 0.0, 0.3)},
    # round 6 (2026-11-25): bodies the photos do not show
    "edwards_nxds6i": {"feet": ("#1b1c1e", 0.0, 0.8), "fan_guard": ("#3a3d42", 0.0, 0.6)},
    "filter_train_5169K72": {"stand": ("#b9c0c7", 0.6, 0.5)},
    "envelope": {"body": ("#8a8f96", 0.0, 0.5)},
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
    # round 6: the IPG 4U single-mode front and the Eaton 2000 px front (cad/oem/photo_fit.py, photos ipg_sm_family, eaton_front_2k)
    "ipg_ylr500_u3": {"chassis": "4U chassis side (black)", "front_panel": "4U front panel, light area", "fan_field": "4U fan field (dark perforated)",
                      "display": "4U window (light grey)", "handles": "4U handles (black)", "start_button": "4U START (green)",
                      "estop": "4U mushroom (red)", "fan_grille": "front panel, dark dot-pattern area"},
    "eaton_5px1500rtg2": {"grille": "grille (perforated silver, holes included)", "lcd_module": "LCD module surround (black)",
                          "lcd_screen": "LCD (lit)", "led_bar": "LED bar (blue)", "badge": "Eaton badge", "bezel": "bezel frame (dark grey)",
                          "keys": "keys (dark grey)"},
    "edwards_nxds6i": {"housing": "housing and fins (painted cast aluminium)", "cowl": "housing and fins (painted cast aluminium)",
                       "base": "base, side face (painted cast aluminium)", "connector_panel": "connector panel (light grey plate)",
                       "inlet": "inlet flange, NW25 (stainless)", "exhaust": "exhaust flange, NW25 (stainless)", "lifting_eye": "lifting eye (stainless)"},
    "transmitter_on_sae4": {"adapter": ("mcm_3861N11", "hex and thread (stainless)"), "hex_and_thread": ("mcm_3861N11", "hex and thread (stainless)"),
                            "body": ("mcm_3861N11", "body and cable (black)"), "cable_gland": ("mcm_3861N11", "body and cable (black)")},
    "filter_train_5169K72": {"housing": ("mcm_5169K72", "housing (black)"), "lid": ("mcm_5169K72", "housing (black)"),
                             "bail_clips": ("mcm_5169K72", "bail clips (steel wire)"), "plumbing": ("mcm_5786N23", "fitting (aluminium)")},
    "clearpath_sd_231x": {"body": "body (black anodised extrusion)", "flange": "flange (machined/cast aluminium front plate)",
                          "fins": "rear housing (die-cast aluminium, fins)", "connectors": "connectors (black plastic)", "shaft": "shaft (ground steel)"},
    "mcm_6627T91": {"body": "housing and end caps (black)", "front": "front face, pilot and shaft (aluminium/steel)"},
    "mcm_6709K12": {"body": "steel block", "caps": "end caps and seals (black plastic)"},
    "mcm_4566N401": {"body": "nut and flange (steel)"},
    "mcm_4123K45": {"body": "body, end caps, tie bolts (cast 316 stainless)", "flanges": "KF flanges (machined stainless)", "grip": "lever grip (grey vinyl)"},
    "mcm_4518K72": {"body": "clamp (aluminium)"},
    "mcm_5786N25": {"body": ("mcm_5786N23", "fitting (aluminium)")},          # same alloy and finish as the KF-25 fitting
    "mcm_3861N11": {"body": "body and cable (black)", "hex": "hex and thread (stainless)", "hex_and_thread": "hex and thread (stainless)",
                    "cable_gland": "body and cable (black)"},
    "mcm_5169K72": {"body": "housing (black)", "housing": "housing (black)", "lid": "housing (black)", "bail_clips": "bail clips (steel wire)"},
}
ZONES = {      # key -> f(cell centres Nx3) -> array of zone names (local frames as in vendor_parts)
    "clearpath_sd_231x": lambda c: np.where(c[:, 2] > 0.01, "shaft", np.where(c[:, 2] > -6.05, "flange", np.where(c[:, 1] > 29.6, "connectors",
                                            np.where(c[:, 2] < -75.0, "fins", "body")))),
    "mcm_6627T91": lambda c: np.where(c[:, 2] > -0.01, "front", "body"),
    "mcm_6709K12": lambda c: np.where(np.abs(c[:, 0]) > 19.45, "caps", "body"),
    "mcm_4123K45": lambda c: np.where(c[:, 2] > 80.0, "grip", np.where((c[:, 0] < 18.0) | (c[:, 0] > 106.2), "flanges", "body")),
}
ZONES_BEFORE = {"mcm_3861N11": lambda c: np.where(c[:, 2] < 9.0, "hex", "body")}   # round 5's one-body transmitter


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


# --------------------------------------------------------------------------------------------
# round 6 (2026-11-25): the parts refined in round 6, before (the model's envelope or the builder at 4b2232e) and after
# --------------------------------------------------------------------------------------------
def _cylz(r, z0, h, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


def env_pump():
    """lpbf_low.py's 'Dry scroll pump' envelope before round 6, in edwards_nxds6i()'s frame (pump placed at (557, 150, z_base1))."""
    sys.path.insert(0, str(HERE))
    import drawing_fit
    return drawing_fit.old_envelope()


def env_transducer():
    """lpbf_low.py's 'Pressure transducer' envelope before round 6, in transmitter_on_sae4()'s frame (z = 0 on the lid)."""
    return _cylz(5.5, -9.0, 9.0).fuse(_cylz(7.9, 0.0, 12.0)).fuse(_cylz(11.0, 12.0, 52.0)).clean()


def env_filter():
    """lpbf_low.py's 'Sealed cyclone + HEPA housing' envelope before round 6, in filter_train_5169K72()'s frame."""
    s = _cylz(55.0, 20.0, 220.0).fuse(_cylz(58.0, 240.0, 14.0)).fuse(_cylz(58.0, 20.0, 14.0))
    return s.fuse(cq.Solid.makeBox(60, 60, 20, cq.Vector(-30, -30, 0))).clean()


PARTS_R6 = [   # key, before callable, after callable, label
    ("edwards_nxds6i", lambda b: env_pump, lambda a: a.edwards_nxds6i, "Edwards nXDS6i dry scroll pump"),
    ("transmitter_on_sae4", lambda b: env_transducer, lambda a: a.transmitter_on_sae4, "Lid pressure transmitter (3861N11 on SAE-4 adapter)"),
    ("filter_train_5169K72", lambda b: env_filter, lambda a: a.filter_train_5169K72, "HEPA filter: 5169K72 on KF-25 adapters"),
    ("mcm_3861N11", lambda b: b.mcm_3861N11, lambda a: a.mcm_3861N11, "McMaster 3861N11 transmitter"),
    ("mcm_5169K72", lambda b: b.mcm_5169K72, lambda a: a.mcm_5169K72, "McMaster 5169K72 filter housing"),
    ("ipg_ylr500_u3", lambda b: b.ipg_ylr500_u3, lambda a: a.ipg_ylr500_u3, "IPG YLR-500-U3 (4U)"),
    ("eaton_5px1500rtg2", lambda b: b.eaton_5px1500rtg2, lambda a: a.eaton_5px1500rtg2, "Eaton 5PX1500RTG2 (2U)"),
]


def parts_r6():
    OUT.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("vp_before_r6", BEFORE_R6)
    before = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(before)
    tiles, report = [], {}
    for key, getb, geta, label in PARTS_R6:
        row = []
        for tag, fn in (("before", getb(before)), ("after", geta(VP))):
            shape = fn()
            c, d = view_for(shape)
            pl = pv.Plotter(off_screen=True, window_size=(640, 480), lighting="none")
            pl.set_background("#f4f6f8", top="#d9e0e8")
            if fn in (env_pump, env_transducer, env_filter):
                mesh = tess(shape)
                rgb, m, r, src = finish_for("envelope", "body")
                pl.add_mesh(mesh, color=rgb, **phong(m, r))
                used = {"body": "the model's envelope (assumed grey)"}
            else:
                if tag == "before" and key in ZONES_BEFORE:
                    ZONES[key] = ZONES_BEFORE[key]
                used = add_part(pl, key, fn)
                ZONES.pop(key, None) if key in ZONES_BEFORE else None
            pl.add_light(pv.Light(position=tuple(c + np.array([-1.2, -2.0, 1.6]) * d), focal_point=tuple(c), intensity=0.95))
            pl.add_light(pv.Light(position=tuple(c + np.array([2.0, -0.6, 0.4]) * d), focal_point=tuple(c), intensity=0.35))
            pl.add_light(pv.Light(position=tuple(c + np.array([0.3, 1.5, 1.0]) * d), focal_point=tuple(c), intensity=0.25))
            pl.camera.focal_point = tuple(c)
            pl.camera.position = tuple(c + np.array([-0.9, -1.7, 0.75]) * d * 1.25)
            pl.camera.up = (0, 0, 1)
            pl.camera.view_angle = 30
            pl.add_text(f"{label}: {tag}", position="upper_left", font_size=9, color="#222222")
            row.append(pl.screenshot(return_img=True))
            pl.close()
            report.setdefault(key, {})[tag] = used
        tiles.append(np.hstack(row))
    from PIL import Image
    for i in range(0, len(tiles), 4):
        grid = np.vstack(tiles[i:i + 4])
        Image.fromarray(grid).resize((grid.shape[1] * 3 // 4, grid.shape[0] * 3 // 4), Image.LANCZOS).save(   # not quantized: a 160-colour palette greyed the small operators
            OUT / f"before_after_r6_{i // 4 + 1}.png", optimize=True)
    (OUT / "finish_sources_r6.json").write_text(json.dumps(report, indent=1))
    print("round-6 parts grid:", len(tiles), "parts")


if __name__ == "__main__":
    what = sys.argv[1:] or ["logos", "parts"]
    if "parts_r6" in what:
        parts_r6()
    if "parts" in what:
        parts_grid()
    if "logos" in what:
        logos()
