"""Animated build and use of option B, from the parts as ordered to a run and removal, plus a collision check
of every move against the machine.

    xvfb-run -a -s "-screen 0 1920x1080x24" python cad/build_gif.py          # ~4 min
    writes cad/img/build_b.gif (and build_b.mp4 if ffmpeg is present) and cad/out/build_collisions.json

Chapters: 1 what is ordered (with prices from bom/), 2 machining (stock -> part), 3 tack and weld in the V-block
fixture, 4 leak test, 5 puck, liner and thermocouples, 6 shields in the cone and the cup clamped on,
7 a run (the pile and the temperatures from the thermal FEA), 8 unclamp, drop, slide out and cap.
Every part is the model in parts.py / mill_cam.py; nothing is a stand-in except the floor and the bench.
The collision check sweeps the moving cup (vessel, centring ring, over-pressure ring) along the install and
removal paths in 2 mm / 10 mm steps and intersects it exactly (OpenCascade) with the cone, its flange and the
open clamp.
"""

import json
import math
import sys
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cam"))
import params as P  # noqa: E402
import parts as PT  # noqa: E402
import viz  # noqa: E402

IMG = HERE / "img"
OUT = HERE / "out"
IMG.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
SIZE = (960, 720)
BENCH_Z = -P.Z_JOINT_FACE           # draw the bench chapters on the floor plane, out of the machine's way
OPEN = 110.0                         # clamp opening angle for install and removal
DROP = P.JOINT.recess_depth + 3.0    # drop that frees the centring ring from the cone flange's recess
SLIDE = (0.0, -1.0)                  # slide direction (toward the operator), checked below


def mesh(shape, tol=0.3):
    return viz.to_mesh(shape, tol)


def cut(m):
    try:
        c = m.clip_closed_surface(normal=(0, 1, 0), origin=(0, 0.01, 0))
        if c.n_points:
            return c
    except Exception:  # noqa: BLE001
        pass
    return m.clip(normal=(0, 1, 0), origin=(0, 0, 0), invert=False)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * t)


# ------------------------------------------------------------------------------------------- the parts
def b_parts():
    import cadquery as cq
    kf, b = P.JOINT, P.B
    prof, z = PT.option_b_vessel_profile()
    g = kf.ring_thk / 2
    out = {}
    # the weldment's pieces, each as it is ordered/made (same outline as the vessel, split at the welds)
    top = z["top"]
    stub = [p for p in prof if p[1] >= z["z_stub"] - 8.0 - 1e-6]
    out["stub"] = PT.revolve(PT.kf_flange_profile(kf, top, down=True, tube_len=b["stub_len"]))
    rt, R_o, R_i, rb = kf.tube_od / 2, z["R_o"], z["R_i"], kf.bore / 2
    red_top, red_bot = z["z_stub"], z["z_red"]
    out["reducer"] = PT.revolve([(rb, red_top), (rt, red_top), (rt, red_top - 8.0), (R_o, red_bot + 8.0),
                                 (R_o, red_bot), (R_i, red_bot), (R_i, red_bot + 8.0), (rb, red_top - 8.0)])
    out["tube"] = PT.tube(R_o, R_i, z["floor"], red_bot)
    out["disc"] = PT.revolve([(0, z["z_bot"]), (R_o - 0.5, z["z_bot"]), (R_o, z["z_bot"] + 0.5),
                              (R_o, z["floor"] - 1.0), (R_o - 1.0, z["floor"]), (0, z["floor"])])
    parts = {n: s for n, s, c, m in PT.option_b()}
    out["puck"] = next(s for n, s in parts.items() if "puck" in n)
    out["liner"] = next(s for n, s in parts.items() if "liner" in n)
    out["tc_top"] = next(s for n, s in parts.items() if "thermocouple (top)" in n)
    out["tc_bot"] = next(s for n, s in parts.items() if "thermocouple (bottom)" in n)
    out["band_top"] = next(s for n, s in parts.items() if "band clamp (top)" in n)
    out["band_bot"] = next(s for n, s in parts.items() if "band clamp (bottom)" in n)
    out["vessel"] = next(s for n, s in parts.items() if "vessel" in n)
    ring, oring = PT.kf_centring_ring(kf, 0.0)
    out["ring"], out["oring"], out["opr"] = ring, oring, PT.kf_overpressure_ring(0.0)
    out["cap"] = PT.kf_blank(kf, 0.0).rotate((0, 0, 0), (1, 0, 0), 180)
    # stock as bought
    out["stock_tube"] = PT.tube(R_o, R_i, 0, 304.8)
    out["stock_bar_disc"] = PT.tube(3.25 * 25.4 / 2, 0, 0, 19.0)
    out["stock_bar_puck"] = PT.tube(3.0 * 25.4 / 2, 0, 0, b["puck_h"] + 11.0)
    out["stock_liner"] = PT.tube(b["liner_od"] / 2, b["liner_od"] / 2 - b["liner_wall"], 0, 304.8)
    import mill_cam as MC
    out["fixture"] = MC.fixture_solid()
    out["fixture_stock"] = cq.Workplane("XY").box(MC.L + 5, MC.W, MC.STOCK_H, centered=(False, True, False)).val() \
        .translate((-2.5, 0, -MC.STOCK_H + 3.5))
    # weld beads at W1, W2 (horizontal axis in the fixture) and W3 (upright)
    def bead(r, zz):
        return (cq.Workplane("XZ").center(r + 0.3, zz).circle(1.4)
                .revolve(360, (-(r + 0.3), 0, 0), (-(r + 0.3), 1, 0)).val())
    out["w1"] = bead(rt, red_top)          # the stub's tube end meets the reducer's 2 in end
    out["w2"] = bead(R_o, red_bot)
    out["w3"] = bead(R_o, z["floor"] - 0.5)
    shield_r = P.CONE_TOP_D / 2 - 6.0
    out["shield"] = PT.tube(shield_r, 0.0, 0, 1.5)
    return out, z


def price_lines():
    """Running cost from bom/vendor-lookups.csv (the picks named in bom/README.md)."""
    import csv
    picks = [("McMaster-Carr", "4518K38", "KF-50 stub"), ("McMaster-Carr", "5237K471", "3x2 in reducer"),
             ("OnlineMetals", "4256", "3 in x 0.065 tube"), ("Speedy Metals", "p-2646", "3-1/4 in 316 bar"),
             ("McMaster-Carr", "11116N864", "liner tube"), ("Speedy Metals", "p-1872", "3 in 304 bar"),
             ("A&N Corporation (ANCORP)", "4000076", "over-pressure ring"),
             ("Auber Instruments", "TC-K-WS", "2 x thermocouple"), ("Auber Instruments", "SYL-2813AC", "2-ch meter")]
    rows = list(csv.DictReader(open(ROOT / "bom" / "vendor-lookups.csv")))
    out = []
    for vendor, pn, label in picks:
        r = next((r for r in rows if r["vendor"].startswith(vendor.split(" (")[0]) and pn in r["part_number"]), None)
        try:
            price = float(r["price_usd"]) if r else float("nan")
        except ValueError:
            price = float("nan")
        if label.startswith("2 x"):
            price *= 2
        out.append((label, price))
    return out


# ------------------------------------------------------------------------------------------- collisions
def collision_check(pt, z):
    import cadquery as cq
    kf = P.JOINT
    static = [("cone outlet flange + spigot", s) for n, s, c, m in PT.cone_section() if "flange" in n]
    static += [(n, s) for n, s, c, m in PT.cone_section() if "funnel" in n]
    clamp_open = PT.kf_clamp(kf, 0.0, open_deg=OPEN)
    moving = [("cup (vessel)", pt["vessel"]), ("centring ring", pt["ring"]), ("over-pressure ring", pt["opr"])]
    path = []
    for zz in np.arange(-120.0, 0.01, 4.0):            # rise straight up into the flange
        path.append(("rise", 0.0, zz))
    for zz in np.arange(0.0, -DROP - 0.01, -0.5):       # drop
        path.append(("drop", 0.0, zz))
    for s in np.arange(0.0, 160.01, 10.0):              # slide toward the operator
        path.append(("slide", s, -DROP))
    hits = []
    worst = {}
    results = {}
    for state, extra in (("clamp off", []), ("clamp left on, open %.0f deg" % OPEN, [("KF clamp, open", clamp_open)])):
        hits = _sweep(path, moving, static + extra)
        results[state] = dict(hits=len(hits), detail=hits[:40])
    res = dict(open_deg=OPEN, drop_mm=DROP, slide_dir=SLIDE, positions=len(path), states=results,
               note="rise: the cup alone (the ring is laid on its flange afterwards); drop and slide: cup + ring + "
                    "over-pressure ring together. Overlaps under 1 mm3 are contact, not interference.")
    (OUT / "build_collisions.json").write_text(json.dumps(res, indent=1) + "\n")
    return res


def _sweep(path, moving, static):
    hits = []
    for phase, s, zz in path:
        dx, dy = SLIDE[0] * s, SLIDE[1] * s
        for mn, ms in moving:
            if mn != "cup (vessel)" and phase == "rise":
                continue                                # the ring is placed on the cup's flange after it rises
            m2 = ms.translate((dx, dy, zz))
            bb = m2.BoundingBox()
            for sn, ss in static:
                b2 = ss.BoundingBox()
                if (bb.xmax < b2.xmin or b2.xmax < bb.xmin or bb.ymax < b2.ymin or b2.ymax < bb.ymin
                        or bb.zmax < b2.zmin or b2.zmax < bb.zmin):
                    continue
                v = m2.intersect(ss).Volume()
                if v > 1.0:
                    hits.append(dict(phase=phase, slide=float(s), dz=float(zz), moving=mn, static=sn, mm3=round(v, 1)))
    return hits


# ---------------------------------------------------------------------------------------------- frames
class Scene:
    def __init__(self):
        self.pt, self.z = b_parts()
        self.M = {}
        for k, s in self.pt.items():
            self.M[k] = mesh(s)
        self.cone = [(mesh(s), c) for n, s, c, m in PT.cone_section()]
        self.clamp = {}
        self.prices = price_lines()

    def clamp_mesh(self, od):
        k = int(round(od / 5.0) * 5)
        if k not in self.clamp:
            self.clamp[k] = mesh(PT.kf_clamp(P.JOINT, 0.0, open_deg=k))
        return self.clamp[k]

    def plotter(self):
        pl = pv.Plotter(off_screen=True, window_size=SIZE)
        pl.set_background("white")
        pl.enable_anti_aliasing("ssaa")
        pl.remove_all_lights()
        pl.enable_lightkit()
        return pl


def add(pl, m, color, offset=(0, 0, 0), rot=None, section=False, opacity=1.0):
    if m is None:
        return
    mm = m.copy()
    if rot is not None:
        axis, ang, centre = rot
        mm = mm.rotate_vector(axis, ang, point=centre, inplace=False)
    mm = mm.translate(offset, inplace=False)
    if section:
        mm = cut(mm)
    pl.add_mesh(mm, color=color, smooth_shading=True, specular=0.35, specular_power=15, opacity=opacity)


def caption(pl, title, sub=""):
    import textwrap
    pl.add_text(title, position="upper_left", font_size=13, color="black")
    if sub:
        wrapped = "\n".join(textwrap.fill(line, 105) for line in sub.split("\n"))
        pl.add_text(wrapped, position=(12, 34 if "\n" in wrapped else 14), font_size=8, color=(0.2, 0.2, 0.2))


def scale_bar(pl, x, y, z, length=100.0):
    line = pv.Line((x, y, z), (x + length, y, z))
    pl.add_mesh(line, color="black", line_width=3)
    pl.add_point_labels([(x + length / 2, y, z + 6)], [f"{length:.0f} mm"], font_size=11, text_color="black",
                        shape_opacity=0.0, show_points=False, always_visible=True)


def render(n_scale=1.0):
    S = Scene()
    M, z = S.M, S.z
    frames = []
    steel, dark, hot = PT.STEEL, PT.STEEL_DK, PT.STEEL_HOT
    kf = P.JOINT
    # ---- 1. what is ordered
    layout = [("stub", (0, 0, 0)), ("reducer", (110, 0, 0)), ("stock_tube", (230, 0, 0)), ("stock_bar_disc", (350, 0, 0)),
              ("stock_liner", (450, 0, 0)), ("stock_bar_puck", (560, 0, 0)), ("ring", (660, 0, 0)), ("opr", (660, 0, 0)),
              ("oring", (660, 0, 0))]
    labels = ["KF-50 stub", "3x2 reducer", "3 in tube", "3-1/4 bar", "2-3/4 tube", "3 in bar", "ring + OP ring"]
    total = 0.0
    n1 = int(20 * n_scale)
    for f in range(n1):
        t = f / max(n1 - 1, 1)
        k_show = int(round(t * (len(S.prices) - 1)))
        total = sum(p for _, p in S.prices[:k_show + 1] if not math.isnan(p))
        pl = S.plotter()
        for key, off in layout:
            m = M[key]
            # stand each part on the bench: shift so its lowest point sits on z = 0
            dz = -m.bounds[4]
            add(pl, m, steel if key not in ("oring",) else PT.FKM, (off[0], off[1], dz))
        for i, (lab, x) in enumerate(zip(labels, (0, 110, 230, 350, 450, 560, 660))):
            pl.add_point_labels([(x, -60, -12)], [lab], font_size=10, text_color="black", shape_opacity=0.0,
                                show_points=False, always_visible=True)
        lines = "\n".join(f"{lab:<20s} ${p:7.2f}" for lab, p in S.prices[:k_show + 1])
        pl.add_text(lines + f"\n{'running total':<20s} ${total:7.2f}", position="upper_right", font_size=8,
                    color="black", font="courier")
        scale_bar(pl, 0, -90, 0)
        caption(pl, "1  Order: catalogue parts and bar stock", "prices: public catalogue, 2026-11-27 (bom/)")
        pl.camera_position = [(340, -1150, 520), (340, 0, 80), (0, 0, 1)]
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 2. machining: stock -> parts
    pairs = [("stock_tube", "tube", (0, 0, 0), "saw + face to %.2f" % (z["z_red"] - z["floor"])),
             ("stock_bar_disc", "disc", (140, 0, 0), "turn: disc + 1x45 weld prep"),
             ("stock_bar_puck", "puck", (260, 0, 0), "turn: catch puck"),
             ("stock_liner", "liner", (380, 0, 0), "saw + face liner"),
             ("fixture_stock", "fixture", (560, 0, 0), "mill: V-block fixture")]
    n2 = int(24 * n_scale)
    for f in range(n2):
        t = f / max(n2 - 1, 1)
        pl = S.plotter()
        for a, b_, off, lab in pairs:
            ma, mb = M[a], M[b_]
            dza, dzb = -ma.bounds[4], -mb.bounds[4]
            ca = (ma.bounds[0] + ma.bounds[1]) / 2, (ma.bounds[2] + ma.bounds[3]) / 2
            cb = (mb.bounds[0] + mb.bounds[1]) / 2, (mb.bounds[2] + mb.bounds[3]) / 2
            if t < 0.5:
                add(pl, ma, (0.68, 0.70, 0.74), (off[0] - ca[0], -ca[1], dza), opacity=1.0 - 0.8 * ease(t / 0.5))
            add(pl, mb, steel if b_ != "fixture" else (0.80, 0.82, 0.86), (off[0] - cb[0], -cb[1], dzb),
                opacity=ease((t - 0.3) / 0.5))
            pl.add_point_labels([(off[0], -70, -12)], [lab], font_size=9, text_color="black", shape_opacity=0.0,
                                show_points=False, always_visible=True)
        scale_bar(pl, -40, -110, 0)
        caption(pl, "2  Machine: lathe and mill programs in cam/gcode/", "all checked by stock-removal simulation"
                " (lathe) and CAMotics (mill)")
        pl.camera_position = [(300, -1450, 700), (300, 0, 40), (0, 0, 1)]
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 3. fixture: lay the stub + reducer + tube in the V, tack, weld; then the disc, upright
    import mill_cam as MC
    ax_h = MC.axis_height()
    rot = ((0, 1, 0), -90.0, (0, 0, 0))     # part axis (z) -> fixture x; the sealing face at x = 0
    sealing = z["top"]

    def in_fixture(key, extra=(0, 0, 0)):
        # rotate about y so +z goes to -x, then move the sealing face to x = 0 at the axis height
        return M[key], (extra[0] + sealing, extra[1], ax_h + extra[2])
    n3 = int(36 * n_scale)
    for f in range(n3):
        t = f / max(n3 - 1, 1)
        pl = S.plotter()
        add(pl, M["fixture"], (0.80, 0.82, 0.86))
        lift = 120 * (1 - ease(t / 0.35))
        for key in ("stub", "reducer", "tube"):
            m, off = in_fixture(key, (0, 0, lift))
            add(pl, m, steel, off, rot=((0, 1, 0), -90.0, (0, 0, 0)))
        if t > 0.45:
            for wkey in ("w1", "w2"):
                m, off = in_fixture(wkey)
                add(pl, m, hot, off, rot=((0, 1, 0), -90.0, (0, 0, 0)), opacity=ease((t - 0.45) / 0.3))
        sub = ("lay the parts in the V; flange rim on a 0.64 mm folded shim" if t < 0.45 else
               "tack x3 per seam, then W1 and W2: TIG, argon back-purge")
        caption(pl, "3  Weld in the V-block fixture", sub)
        pl.camera_position = [(-420, -760, 520), (110, 0, 0), (0, 0, 1)]
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # upright: the disc goes on and W3
    n3b = int(14 * n_scale)
    for f in range(n3b):
        t = f / max(n3b - 1, 1)
        pl = S.plotter()
        for key in ("stub", "reducer", "tube", "w1", "w2"):
            add(pl, M[key], steel if not key.startswith("w") else hot, (0, 0, 0), section=True)
        add(pl, M["disc"], steel, (0, 0, -80 * (1 - ease(t / 0.5))), section=True)
        if t > 0.55:
            add(pl, M["w3"], hot, section=True, opacity=ease((t - 0.55) / 0.3))
        caption(pl, "3  Bottom disc: 1x45 prep into the tube end, W3", "section view")
        pl.camera_position = [(260, -900, -80), (0, 0, -130), (0, 0, 1)]
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 4. leak test
    n4 = int(12 * n_scale)
    for f in range(n4):
        t = f / max(n4 - 1, 1)
        pl = S.plotter()
        add(pl, M["vessel"], steel, section=True)
        add(pl, M["ring"], dark, section=True)
        add(pl, M["oring"], PT.FKM, section=True)
        add(pl, M["cap"], dark, (0, 0, kf.ring_thk / 2 + 60 * (1 - ease(t / 0.5)) + 0.0), section=True)
        add(pl, S.clamp_mesh(0 if t > 0.6 else OPEN), steel, section=True)
        caption(pl, "4  Leak test before first use", "blank + clamp on top: soap at +0.15 bar, then"
                " rate-of-rise from 10 mbar (procedure.md)")
        pl.camera_position = [(260, -900, -80), (0, 0, -120), (0, 0, 1)]
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 5. puck, liner, thermocouples
    n5 = int(18 * n_scale)
    for f in range(n5):
        t = f / max(n5 - 1, 1)
        pl = S.plotter()
        add(pl, M["vessel"], steel, section=True)
        add(pl, M["puck"], hot, (0, 0, 300 * (1 - ease(t / 0.35))), section=True)
        add(pl, M["liner"], (0.70, 0.72, 0.76), (0, 0, 320 * (1 - ease((t - 0.3) / 0.35))), section=True)
        if t > 0.65:
            for k in ("band_top", "band_bot", "tc_top", "tc_bot"):
                add(pl, M[k], dark if "band" in k else PT.BRASS_TC, opacity=ease((t - 0.65) / 0.3))
        caption(pl, "5  Puck, liner, thermocouples", "TCs to a 2-channel meter, alarm 120 C top / 450 C bottom")
        pl.camera_position = [(260, -900, -80), (0, 0, -120), (0, 0, 1)]
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 6. shields in the cone, then the cup goes on and the clamp closes
    cup_keys = ["vessel", "puck", "liner", "band_top", "band_bot", "tc_top", "tc_bot"]
    cup_cols = {"vessel": steel, "puck": hot, "liner": (0.70, 0.72, 0.76), "band_top": dark, "band_bot": dark,
                "tc_top": PT.BRASS_TC, "tc_bot": PT.BRASS_TC}
    z_shield = kf.ring_thk / 2 + P.CONE_OUTLET_LEN + P.CONE_H - 4.0
    n6 = int(40 * n_scale)
    th = load_thermal()
    for f in range(n6):
        t = f / max(n6 - 1, 1)
        pl = S.plotter()
        for m, c in S.cone:
            add(pl, m, c, section=True)
        add(pl, M["shield"], (0.88, 0.88, 0.9), (0, 0, z_shield + 200 * (1 - ease(t / 0.25))), section=True)
        rise = -40 * (1 - ease((t - 0.3) / 0.35))           # from just above the mat
        for k in cup_keys:
            add(pl, M[k], cup_cols[k], (0, 0, rise), section=True)
        if t > 0.65:
            add(pl, M["ring"], dark, section=True)
            add(pl, M["oring"], PT.FKM, section=True)
            add(pl, M["opr"], dark, section=True)
        away = 170.0 * (1 - ease((t - 0.68) / 0.1))      # the clamp is off until the ring is seated
        od = OPEN if t < 0.8 else OPEN * (1 - ease((t - 0.8) / 0.17))
        add(pl, S.clamp_mesh(od), steel, (away, 0, 0), section=True)
        floor_plane(pl)
        sub = ("AMAZEMET's shields go in the cone's mouth (always, and more than one for copper alloys)" if t < 0.3
               else "clamp OFF; lift the cup onto the outlet (two people); ring + O-ring + over-pressure ring;"
                    " clamp on, finger-tight")
        caption(pl, "6  Install under the cone", sub)
        pl.camera_position = [(420, -1100, 60), (0, -60, -110), (0, 0, 1)]
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 250
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 7. run: the pile, coloured by the thermal FEA, with the probe readings
    n7 = int(16 * n_scale)
    pile = pile_mesh(z)
    for f in range(n7):
        t = f / max(n7 - 1, 1)
        tt = 10 ** (1 + 2.5 * t)                      # 10 s .. ~3000 s on a log clock
        pl = S.plotter()
        for m, c in S.cone:
            add(pl, m, c, section=True)
        for k in cup_keys:
            add(pl, M[k], cup_cols[k], section=True)
        for k in ("ring", "opr"):
            add(pl, M[k], dark, section=True)
        add(pl, M["oring"], PT.FKM, section=True)
        add(pl, S.clamp_mesh(0), steel, section=True)
        Tp = np.interp(tt, th["t"], th["pile"])
        col = glow(Tp)
        add(pl, pile, col, section=True)
        floor_plane(pl)
        txt = (f"t = {tt:5.0f} s after 816 g of shot lands at 1050 C (thermal FEA case B_816)\n"
               f"pile (mean) {Tp:5.0f} C   floor {np.interp(tt, th['t'], th['bottom']):4.0f} C   "
               f"TC top {np.interp(tt, th['t'], th['tc_top']):3.0f} C   O-ring {np.interp(tt, th['t'], th['oring']):3.0f} C")
        caption(pl, "7  A bad run: the whole charge as shot", txt)
        pl.camera_position = [(420, -1100, 60), (0, -60, -110), (0, 0, 1)]
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 250
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    # ---- 8. remove: open, drop, slide out, cap
    n8 = int(30 * n_scale)
    for f in range(n8):
        t = f / max(n8 - 1, 1)
        pl = S.plotter()
        for m, c in S.cone:
            add(pl, m, c, section=True)
        od = OPEN * ease(t / 0.12)
        away = 170.0 * ease((t - 0.12) / 0.08)               # take the clamp off: open, it still blocks the flange
        add(pl, S.clamp_mesh(od), steel, (away, 0, 0), section=True)
        drop = -DROP * ease((t - 0.2) / 0.15)
        s = 260 * ease((t - 0.35) / 0.35)
        off = (SLIDE[0] * s, SLIDE[1] * s, drop)
        for k in cup_keys:
            add(pl, M[k], cup_cols[k], off, section=True)
        for k in ("ring", "opr"):
            add(pl, M[k], dark, off, section=True)
        add(pl, M["oring"], PT.FKM, off, section=True)
        if t > 0.75:
            add(pl, M["cap"], dark, (off[0], off[1], off[2] + kf.ring_thk / 2 + 80 * (1 - ease((t - 0.75) / 0.2))),
                section=True)
        floor_plane(pl)
        sub = (f"take the clamp off; drop {DROP:.0f} mm so the ring leaves the cone's recess; slide out toward you"
               if t < 0.75 else "KF blank + clamp on top to carry it under argon; cool below 60 C before opening")
        caption(pl, "8  Remove", sub)
        pl.camera_position = [(420, -1100, 60), (0, -60, -110), (0, 0, 1)]
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 250
        frames.append(pl.screenshot(return_img=True))
        pl.close()
    return frames


def floor_plane(pl):
    plane = pv.Plane(center=(0, -80, -P.Z_JOINT_FACE), direction=(0, 0, 1), i_size=520, j_size=520)
    pl.add_mesh(plane, color=(0.80, 0.81, 0.83))



def pile_mesh(z):
    b = P.B
    r = b["liner_od"] / 2 - b["liner_wall"] - 0.2
    zz = z["floor"] + 0.2 + b["puck_h"] + 0.2
    h = 816e-3 / (P.SHOT["rho"] * 0.6 * math.pi * (r * 1e-3) ** 2) * 1e3
    return viz.to_mesh(PT.tube(r, 0, zz, zz + h), 0.4)


def glow(T):
    """Rough blackbody-ish colour of hot metal by temperature (C), for the animation only."""
    stops = [(25, (0.45, 0.40, 0.38)), (450, (0.45, 0.30, 0.25)), (600, (0.55, 0.12, 0.05)), (750, (0.85, 0.20, 0.04)),
             (900, (1.0, 0.45, 0.08)), (1050, (1.0, 0.75, 0.30))]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if T <= t1:
            k = (T - t0) / (t1 - t0)
            return tuple(a + max(0.0, k) * (b - a) for a, b in zip(c0, c1))
    return stops[-1][1]


def load_thermal():
    p = ROOT / "analysis" / "out" / "thermal" / "B_816" / "result.json"
    r = json.loads(p.read_text())
    s = r["series"]
    t = np.array(s["N_PILE"]["t"])
    return {"t": t, "pile": np.array(s["N_PILE"]["T"]), "bottom": np.interp(t, s["BOTTOM_CENTRE"]["t"], s["BOTTOM_CENTRE"]["T"]),
            "tc_top": np.interp(t, s["TC_TOP"]["t"], s["TC_TOP"]["T"]), "oring": np.interp(t, s["N_ORING"]["t"], s["N_ORING"]["T"])}


def main(argv):
    n_scale = float(argv[0]) if argv else 1.0
    pt, z = b_parts()
    col = collision_check(pt, z)
    print("collision check:", {k: v["hits"] for k, v in col["states"].items()}, "over", col["positions"], "positions",
          flush=True)
    frames = render(n_scale)
    small = [f[::1, ::1] for f in frames]
    imageio.mimsave(IMG / "build_b.gif", [f[::2, ::2] for f in small], duration=0.11, loop=0)
    try:
        imageio.mimsave(IMG / "build_b.mp4", small, fps=10, codec="libx264", quality=7, macro_block_size=8)
    except Exception as ex:  # noqa: BLE001
        print("mp4 skipped:", ex)
    print("frames", len(frames))


if __name__ == "__main__":
    main(sys.argv[1:])
