"""Render the fast-track states (ft_model.py) and the steps between them.

Run (headless):  xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/fast-track/cad/ft_render.py [what ...]
  what: states, sections, steps, strip, monitoring, camera_view, thorlabs, door, gif (default: all, in that order)
Writes desktop-lpbf/fast-track/img/cad-*.png and cad-progression.gif.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ft_model as M  # noqa: E402

pv.OFF_SCREEN = True
IMG = HERE.parent / "img"
W, H = 1200, 860
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MAT = dict(smooth_shading=True, specular=0.3, specular_power=18, ambient=0.22, diffuse=0.85)
CONTEXT = ("Bench top", "Gantry", "PC with", "IPG YLR", "Process fibre", "Safety relay", "E-stop", "Key switch", "Argon regulator",
           "Exhaust HEPA", "Trace O2", "Rotary-vane", "KF-25 pump hose", "Digitizer", "Fibre bend restrictor", "Emission lamp")
ADDED, MOVED, REMOVED, KEPT = "#2bb24c", "#2b6cd2", "#d22b2b", "#c9ced4"
# MK-09's top flange and gussets, g3's far-side plate and its brackets, the head's supply: hidden with the head in the
# views from below
HEAD_MOUNTS = ("Head-plate", "Head far-side", "Far-side support", "+-15 V supply")


def hex2rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


def tess(shape, tol=0.3, ang=0.3):
    vs, ts = shape.tessellate(tol, ang)
    if not ts:
        return None
    pts = np.array([(v.x, v.y, v.z) for v in vs], dtype=float)
    faces = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
    return pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


def caption(img, text, sub="", legend=None):
    im = Image.fromarray(img)
    band = 48 if sub else 30
    out = Image.new("RGB", (im.width, im.height + band), "#26323f")
    out.paste(im, (0, band))
    d = ImageDraw.Draw(out)
    f1, f2 = ImageFont.truetype(FONT, 16), ImageFont.truetype(FONT, 12)
    d.text((10, 6), text, fill="#ffffff", font=f1)
    if sub:
        d.text((10, 28), sub, fill="#b8c4d0", font=f2)
    if legend:
        x = im.width - 10
        for lab, col in reversed(legend):
            w_ = d.textlength(lab, font=f2) + 26
            x -= w_
            d.rectangle((x, 9, x + 14, 23), fill=col)
            d.text((x + 18, 9), lab, fill="#ffffff", font=f2)
    return np.asarray(out)


def key(p):
    """A part's identity across states: its name (with long/short variants folded) and pid."""
    return p.name


def centre(shape):
    bb = shape.BoundingBox()
    return np.array([(bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, (bb.zmin + bb.zmax) / 2,
                     bb.xlen, bb.ylen, bb.zlen])


def diff(prev, cur):
    """Classify cur's parts against prev: added, moved, kept; and prev's parts that are removed."""
    pm = {key(p): p for p in prev}
    cm = {key(p): p for p in cur}
    cls = {}
    for k, p in cm.items():
        if k not in pm:
            cls[k] = "added"
        else:
            cls[k] = "moved" if np.abs(centre(p.shape) - centre(pm[k].shape)).max() > 0.5 else "kept"
    removed = [p for k, p in pm.items() if k not in cm]
    return cls, removed


def plotter(size=(W, H)):
    pl = pv.Plotter(off_screen=True, window_size=size, lighting="three lights")
    pl.set_background("#f7f9fb", top="#dce5ee")
    pl.enable_anti_aliasing("ssaa")
    return pl


def add_parts(pl, parts, colors=None, opac=None, clip=False, edges=True, hide=()):
    for p in parts:
        if any(h in p.name for h in hide):
            continue
        m = tess(p.shape)
        if m is None:
            continue
        if clip:
            m = m.clip(normal="-y", origin=(0, 0.0, 0), invert=True)
            if not m.n_points:
                continue
        col = hex2rgb(colors.get(key(p), p.color) if colors else p.color)
        o = (opac or {}).get(key(p), p.opacity)
        if clip:
            o = max(o, 0.85) if o > 0.3 else 0.35
        pl.add_mesh(m, color=col, opacity=o, **MAT)
        if edges and o > 0.3:
            fe = m.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False,
                                         manifold_edges=False)
            if fe.n_points:
                pl.add_mesh(fe, color=(0.12, 0.13, 0.15), line_width=1.0, opacity=0.45)


def beam(pl, state, opacity=0.35):
    cone = M.beam_cone(state, 0.0, M.P["lens_wd"])
    m = tess(cone, 0.5)
    pl.add_mesh(m, color=(1.0, 0.12, 0.12), opacity=opacity, smooth_shading=True)


ISO = dict(pos=(-1350, -1700, 1250), focal=(-60, 20, 120), view_angle=30)
ISO_WIDE = dict(pos=(-1650, -2300, 1500), focal=(-160, 20, 100), view_angle=30)
SEC = dict(pos=(-30, -1500, 170), focal=(-30, 40, 140), view_angle=30)
MON_VIEW = dict(pos=(-900, -1150, 700), focal=(-60, -10, 120), view_angle=30)
LOW = dict(pos=(-700, -900, -260), focal=(0, 30, -120), view_angle=30)


def cam(pl, v):
    pl.camera.position = v["pos"]
    pl.camera.focal_point = v["focal"]
    pl.camera.up = (0, 0, 1)
    pl.camera.view_angle = v["view_angle"]


def shot(pl):
    img = pl.screenshot(return_img=True)
    pl.close()
    return img


SUBS = {
    "S1": "deck on the support rails, target at the powder plane; hurrySCAN hung by its entrance face and held on its far "
          "face from both cross-beams (g3 gantry), lens axis at y -30",
    "S2": "Saginaw 16 x 12 x 8 in. box on the rails; window, split beam tube, D4NS-2CF tongue switches: Class 1; 1 kW dump at the plate",
    "FT-0": "well block, plate on a collar-held rod, argon nozzle; 48 mm spreader bar; layer camera, raking lights, TCs",
    "FT-1": "rod clamped in the rod-end block on the X-VSR20A; X-LSM100B, shield, arm and hopper-blade on the deck; AE sensor",
    "FT-1V": "deck cassette, gland, window stack and stages moved onto a 12 in. cube; cover slide on a drop tube; pump-purge",
}


def states():
    for s in M.STATES:
        parts = M.build(s)
        pl = plotter()
        add_parts(pl, parts)
        if s != "S1":
            beam(pl, s)
        cam(pl, ISO_WIDE if s in ("S1", "FT-1V") else ISO)
        img = caption(shot(pl), M.TITLES[s], SUBS[s])
        Image.fromarray(img).save(IMG / f"cad-{s.lower()}.png")
        print("wrote", f"cad-{s.lower()}.png")


def sections():
    for s in ("FT-0", "FT-1", "FT-1V"):
        parts = M.build(s)
        pl = plotter()
        add_parts(pl, parts, clip=True, hide=CONTEXT + ("Bench top", "T-slot base", "120 mm fan"))
        beam(pl, s, 0.3)
        cam(pl, SEC)
        img = caption(shot(pl), f"{s}: section through the plate (y = 0)",
                      "plate at the start of a build; red: the scanned-beam envelope over the Ø40 field")
        Image.fromarray(img).save(IMG / f"cad-section-{s.lower()}.png")
        print("wrote", f"cad-section-{s.lower()}.png")


STEP_TEXT = {
    ("S1", "S2"): "S1 -> S2: the box arrives; the deck goes into it, the target makes way for the dump",
    ("S2", "FT-0"): "S2 -> FT-0: well block, plate, rod, gland, nozzle and collector go in; argon, HEPA and O2 analyzer",
    ("FT-0", "FT-1"): "FT-0 -> FT-1: the stages arrive; collar off, rod to the X-VSR20A, recoater on the deck",
    ("FT-1", "FT-1V"): "FT-1 -> FT-1V: the cube arrives; everything on the deck moves across as one cassette",
}


def steps():
    for a, b in zip(M.STATES[:-1], M.STATES[1:]):
        prev, cur = M.build(a), M.build(b)
        cls, removed = diff(prev, cur)
        colors, opac = {}, {}
        for p in cur:
            k = key(p)
            c = cls[k]
            if c == "added":
                colors[k] = ADDED
                if p.opacity < 1:
                    opac[k] = 0.2
            elif c == "moved":
                colors[k] = MOVED
            else:
                colors[k] = KEPT
                opac[k] = min(p.opacity, 0.55) if p.opacity < 1 else 0.9
        pl = plotter()
        add_parts(pl, cur, colors, opac, edges=True)
        for p in removed:
            m = tess(p.shape)
            if m is not None:
                pl.add_mesh(m, color=hex2rgb(REMOVED), opacity=0.16, **MAT)
        cam(pl, ISO_WIDE if b in ("S2", "FT-1V") else ISO)
        n_add = sum(1 for v in cls.values() if v == "added")
        n_mov = sum(1 for v in cls.values() if v == "moved")
        img = caption(shot(pl), STEP_TEXT[(a, b)], f"{n_add} parts added, {n_mov} moved, {len(removed)} removed "
                      f"(kept parts in grey)",
                      legend=[("added", ADDED), ("moved", MOVED), ("removed", REMOVED), ("kept", KEPT)])
        Image.fromarray(img).save(IMG / f"cad-step-{a.lower()}-to-{b.lower()}.png")
        print("wrote", f"cad-step-{a.lower()}-to-{b.lower()}.png")


def strip():
    tiles = []
    for s in M.STATES:
        im = Image.open(IMG / f"cad-{s.lower()}.png")
        tiles.append(im.resize((im.width // 2, im.height // 2), Image.LANCZOS))
    w = sum(t.width for t in tiles[:3])
    rows = [tiles[:3], tiles[3:]]
    out = Image.new("RGB", (w, tiles[0].height * 2), "#ffffff")
    y = 0
    for r in rows:
        x = (w - sum(t.width for t in r)) // 2
        for t in r:
            out.paste(t, (x, y))
            x += t.width
        y += tiles[0].height
    out.save(IMG / "cad-progression.png")
    print("wrote cad-progression.png")


def gif():
    """Each state built up from the one before: removed parts fade out, added parts drop in."""
    frames = []
    gw, gh = 760, 560
    prev, prev_mesh = None, {}
    for s in M.STATES:
        cur = M.build(s)
        mesh = {key(p): tess(p.shape, 0.6, 0.4) for p in cur}
        if prev is None:
            seq = [({}, [], 1.0)] * 3
        else:
            cls, removed = diff(prev, cur)
            seq = []
            for f in range(6):
                t = (f + 1) / 6
                off = {k: (0, 0, 260 * (1 - t) ** 2) for k, c in cls.items() if c == "added"}
                seq.append((off, removed if f < 3 else [], t))
        for off, rem, t in seq:
            pl = plotter((gw, gh))
            for p in cur:
                m = mesh[key(p)]
                if m is None:
                    continue
                o = off.get(key(p))
                if o:
                    m = m.translate(o, inplace=False)
                pl.add_mesh(m, color=hex2rgb(p.color), opacity=p.opacity, **MAT)
            for p in rem:
                m = prev_mesh.get(key(p))
                if m is not None:
                    pl.add_mesh(m, color=hex2rgb(REMOVED), opacity=0.3, **MAT)
            cam(pl, ISO_WIDE)
            frames.append(Image.fromarray(caption(shot(pl), M.TITLES[s])))
        frames += [frames[-1]] * 10
        prev, prev_mesh = cur, mesh
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=160) for f in frames]
    pal[0].save(IMG / "cad-progression.gif", save_all=True, append_images=pal[1:], duration=120, loop=0, optimize=True)
    print("wrote cad-progression.gif", len(frames), "frames")


def monitoring():
    """Close-ups of FT-1: the monitoring parts (purple) above the box, and the drive and lead routing under it."""
    parts = M.build("FT-1")
    mon = "#8a4fbf"
    colors = {key(p): (mon if p.sub == "monitoring" else KEPT) for p in parts}
    opac = {key(p): (1.0 if p.sub == "monitoring" else (0.18 if p.opacity < 1 else 0.45)) for p in parts}
    pl = plotter()
    add_parts(pl, parts, colors, opac, hide=("Bench top", "PC with", "IPG YLR", "Safety relay", "E-stop", "Key switch",
                                             "Argon regulator", "Exhaust HEPA", "Trace O2", "Gantry uprights"))
    beam(pl, "FT-1", 0.25)
    cam(pl, MON_VIEW)
    img = caption(shot(pl), "FT-1 monitoring (purple): layer camera, two raking lights, coaxial photodiode, AE, thermocouples",
                  "MON1 camera through its own door port; MON2/MON3 lights through wall ports; MON4 photodiode behind "
                  "the head's input-mirror block; MON5 AE on the rod-end block (below)")
    Image.fromarray(img).save(IMG / "cad-monitoring-ft-1.png")
    pl = plotter()
    add_parts(pl, parts, hide=("Bench top", "PC with", "IPG YLR", "Safety relay", "E-stop", "Key switch", "Argon regulator",
                               "Exhaust HEPA", "Trace O2", "Gantry", "SCANLAB", "LINOS", "Scan-head", "Flange-to-beam",
                               "hurrySCAN", "Collimator", "Photodiode", "Process fibre", "Fibre bend", "Head cables")
                         + HEAD_MOUNTS)
    cam(pl, LOW)
    img = caption(shot(pl), "FT-1 under the box: rod-end block with the potted plug's pigtail and terminal block, AE sensor, "
                  "X-VSR20A (Zaber STEP)", "the rod's lower end is potted flush, so the rod lifts out through the gland")
    Image.fromarray(img).save(IMG / "cad-under-ft-1.png")
    print("wrote cad-monitoring-ft-1.png, cad-under-ft-1.png")


def camera_view():
    """What the layer camera sees (hopper parked at the right), rendered from its lens front with its field."""
    for st in ("FT-1", "FT-1V"):
        parts = M.build(st)
        c = M.camera_geometry(st)
        pos = tuple(c["W"][i] + 30.0 * c["u"][i] for i in range(3))
        pl = plotter((900, 680))
        add_parts(pl, parts, hide=("Layer camera", "Camera post", "Camera port", "Box door", "Cube top plate",
                                   "Window, ", "Cover slide,"), edges=False)
        pl.camera.position = pos
        pl.camera.focal_point = (0.0, 0.0, M.levels(st)["dz"])
        pl.camera.up = (0, 0, 1)
        pl.camera.view_angle = float(2 * np.degrees(np.arctan(c["field_mm"][1] / 2 / c["dist_mm"])))
        img = caption(shot(pl), f"{st}: the layer camera's view ({c['f_mm']:.0f} mm lens, {c['tilt_deg']:.1f} deg off "
                      f"vertical, {c['um_px_across']:.1f} um/px)", "hopper parked at the right; the IMX477's short-side field")
        Image.fromarray(img).save(IMG / f"cad-camera-view-{st.lower()}.png")
        print("wrote", f"cad-camera-view-{st.lower()}.png")


def door():
    """FT-1 with the beam tube's centre section off and the box door open (the fix for round 1's captive tube)."""
    parts = M.build("FT-1", lid_open=True)
    pl = plotter()
    add_parts(pl, parts, hide=CONTEXT + ("120 mm fan",))
    cam(pl, MON_VIEW)
    img = caption(shot(pl), f"FT-1 with the box door open {M.P['door_open_deg']:g} deg: the beam tube's two half-shells "
                  "come off sideways first", "the collar stays clamped on the lens; Ø50 spigots inside the section's ends "
                  "locate it on the window flange and under the collar; the camera rides on the door")
    Image.fromarray(img).save(IMG / "cad-door-open-ft-1.png")
    print("wrote cad-door-open-ft-1.png")


def thorlabs():
    parts = M.build("FT-1", piston="thorlabs")
    pl = plotter()
    add_parts(pl, parts, hide=("Bench top", "PC with", "IPG YLR", "Gantry", "SCANLAB", "LINOS", "Scan-head", "hurrySCAN",
                               "Collimator", "Photodiode", "Process fibre", "Fibre bend", "Head cables", "Flange-to-beam")
                         + HEAD_MOUNTS)
    cam(pl, LOW)
    img = caption(shot(pl), "FT-1 with the PCard route's piston stage: Thorlabs MTS50/M-Z8 on end (Thorlabs STEP)",
                  "tower plate on the bracket plate, the stage's lower end through a cut-out; L-arm to the same rod-end block")
    Image.fromarray(img).save(IMG / "cad-ft-1-thorlabs.png")
    print("wrote cad-ft-1-thorlabs.png")


def gantry():
    """The head's mounts on the default gantry, seen from the far (+x) side: MK-09 on the entrance face, and g3's
    support plate on the far face (hidden behind the head in the iso views)."""
    parts = M.build("FT-1")
    far = ("Head far-side", "Far-side support")
    colors, opac = {}, {}
    for p in parts:
        k = key(p)
        if any(f in p.name for f in far):
            colors[k] = ADDED
        elif p.pid == "MK-09":
            colors[k] = "#e0a030"
        elif p.sub == "frame":
            colors[k], opac[k] = KEPT, 0.55
    pl = plotter()
    add_parts(pl, parts, colors, opac, hide=("Bench top", "PC with", "IPG YLR", "Safety relay", "E-stop", "Key switch",
                                             "Argon regulator", "Exhaust HEPA", "Trace O2", "Digitizer", "120 mm fan"))
    cam(pl, dict(pos=(1050, -760, 900), focal=(40, 10, 360), view_angle=30))
    img = caption(shot(pl), f"FT-1: the head's mounts on the default gantry (P['gantry'] = \"{M.P['gantry']}\"), from the +x side",
                  "amber: MK-09 flange plate on the entrance face, top flange on both cross-beams, gussets under the head; "
                  "green: the 10 mm support plate on the far face and its angle brackets (g3)",
                  legend=[("MK-09", "#e0a030"), ("g3 far-side plate", ADDED)])
    Image.fromarray(img).save(IMG / "cad-gantry-g3.png")
    print("wrote cad-gantry-g3.png")


def cassette_in():
    """FT-1V's cassette carried halfway in through the cube's door at mid-height of the opening, and (green, faint)
    where it ends up: down in the bottom face's pocket, which is as big as the face opening (ft_cassette.py)."""
    import ft_cassette as K
    parts = M.build("FT-1V")
    cas = [p for p in parts if p.group != "piston" and not p.name.startswith(K.LOOSE)
           and (p.sub in ("cassette", "recoater") or p.name.startswith(K.ON_DECK))]
    L = M.levels("FT-1V")
    h = max(p.shape.BoundingBox().zmax for p in cas) - L["floor_top"]
    lift = K.HALF_IN - h / 2                                   # underside at mid-height of the opening, less half its height
    dy = -M.P["cube_frame"] / 2 - 10.0                         # the deck's centre 10 mm outside the door's plane
    keep = ("Ideal Vacuum 12", "Cube bottom plate", "Cube back plate", "Cube left plate", "Cube right plate")
    pl = plotter()
    add_parts(pl, [p for p in parts if p.name.startswith(keep)], opac={key(p): 0.55 for p in parts})
    for p in cas:
        m = tess(p.shape)
        if m is None:
            continue
        pl.add_mesh(m.translate((0.0, dy, lift), inplace=False), color=hex2rgb(p.color), opacity=1.0, **MAT)
        pl.add_mesh(m, color=hex2rgb(ADDED), opacity=0.22, **MAT)
    xc, yc = M.P["deck_c"]
    cam(pl, dict(pos=(xc - 620, yc - 980, L["cube_c"] + 560), focal=(xc, yc - 90, L["cube_c"] - 40), view_angle=30))
    img = caption(shot(pl), f"FT-1V: the cassette (245 x 245 x {h:.1f} mm) carried in through the cube's door at "
                  "mid-height of the opening", "green, faint: where it ends up, in the bottom face's pocket, which is as "
                  "big as the face opening (266 mm est.): so the opening must be >= 245 mm + clearance (ft_cassette.py)")
    Image.fromarray(img).save(IMG / "cad-cassette-into-cube.png")
    print("wrote cad-cassette-into-cube.png")


if __name__ == "__main__":
    IMG.mkdir(exist_ok=True)
    what = sys.argv[1:] or ["states", "sections", "steps", "strip", "monitoring", "camera_view", "thorlabs", "door", "gantry",
                            "cassette_in", "gif"]
    for w in what:
        globals()[w]()
