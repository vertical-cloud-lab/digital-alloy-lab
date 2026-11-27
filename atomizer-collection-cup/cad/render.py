"""Stills and GIFs of the collection cups (needs a display: run under xvfb-run).

    xvfb-run -a -s "-screen 0 1920x1080x24" python cad/render.py          # everything, ~3 min
    xvfb-run -a -s "-screen 0 1920x1080x24" python cad/render.py lineup   # one item

Writes cad/img/: lineup.png (the stock cup and options A, B and C under the cone, cut in half),
option_b_exploded.png, option_a_exploded.png, option_c_exploded.png, and assembly_b.gif (assemble,
hang under the cone, clamp, then unclamp, drop, slide out and cap).
"""

import math
import sys
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import params as P  # noqa: E402
import parts as PT  # noqa: E402
import viz  # noqa: E402

IMG = HERE / "img"
IMG.mkdir(exist_ok=True)
_cache = {}


def mesh(shape, tol=0.25):
    key = id(shape)
    if key not in _cache:
        _cache[key] = viz.to_mesh(shape, tol)
    return _cache[key]


def section(m):
    try:
        c = m.clip_closed_surface(normal=(0, 1, 0), origin=(0, 0.01, 0))
        if c.n_points:
            return c
    except Exception:  # noqa: BLE001
        pass
    return m.clip(normal=(0, 1, 0), origin=(0, 0, 0), invert=False)


def new_plotter(size):
    pl = viz.plotter(size)
    pl.remove_all_lights()
    pl.enable_lightkit()
    return pl


def draw(pl, parts, offset=(0, 0, 0), cut=True, glass_op=0.35):
    for name, shape, col, mat in parts:
        m = viz.to_mesh(shape, 0.25)
        if m is None or m.n_points == 0:
            continue
        if cut:
            m = section(m)
            if m.n_points == 0:
                continue
        m = m.translate(offset, inplace=False)
        op = glass_op if ("glass" in name or "quartz" in name) else 1.0
        pl.add_mesh(m, color=col, opacity=op, smooth_shading=True, specular=0.35, specular_power=15)


def floor(pl, x0, x1, z, y=(-150, 250)):
    plane = pv.Plane(center=((x0 + x1) / 2, (y[0] + y[1]) / 2, z), direction=(0, 0, 1),
                     i_size=x1 - x0, j_size=y[1] - y[0])
    pl.add_mesh(plane, color=(0.55, 0.57, 0.6), opacity=1.0)


def lineup():
    """Four cups side by side under copies of the cone, cut in half."""
    sets = [("Stock (glass, valve)", PT.stock_cup()), ("A: catalogue KF nipple", PT.option_a()),
            ("B: welded 316L (recommended)", PT.option_b()), ("C: quartz + spacer", PT.option_c())]
    pl = new_plotter((2400, 1250))
    dx = 330.0
    for i, (title, parts) in enumerate(sets):
        off = (i * dx, 0, 0)
        draw(pl, PT.cone_section() + PT.joint_hardware() + parts, offset=off)
        pl.add_point_labels([(i * dx, -60, 260)], [title], font_size=26, text_color="black",
                            shape_opacity=0.0, show_points=False, always_visible=True)
    floor(pl, -200, 3 * dx + 200, -P.Z_JOINT_FACE)
    pl.add_point_labels([(-160, -60, -P.Z_JOINT_FACE + 8)], [f"mat ({P.Z_JOINT_FACE:.0f} mm below the joint)"],
                        font_size=18, text_color=(0.2, 0.2, 0.2), shape_opacity=0.0, show_points=False,
                        always_visible=True)
    pl.camera_position = [(1.5 * dx, -1650, 60), (1.5 * dx, 0, -40), (0, 0, 1)]
    pl.camera.parallel_projection = True
    pl.camera.parallel_scale = 330
    pl.screenshot(str(IMG / "lineup.png"))
    pl.close()


def exploded(which):
    if which == "b":
        parts = PT.joint_hardware() + PT.option_b(explode=0.0)
        stack = [("B: catch puck (304)", -110), ("B: sacrificial liner (304)", -245), ("joint: centring ring", 40),
                 ("joint: O-ring", 40), ("joint: over-pressure ring", 40), ("joint: KF clamp", 85)]
        labels = {"B: welded 316L vessel": "316L weldment: KF-50 stub + 3x2 in reducer\n+ 3 in tube + 8 mm floor (W1-W3)",
                  "B: sacrificial liner (304)": "304 liner, 2-3/4 x 0.065 (drops in, sacrificial)",
                  "B: catch puck (304)": "304 catch puck (sits on the floor)",
                  "joint: centring ring": "centring ring + FKM O-ring (AS568-330)",
                  "joint: over-pressure ring": "over-pressure ring (A&N 4000076)",
                  "joint: KF clamp": "existing KF clamp (finger-tight)",
                  "B: thermocouple band clamp (top)": "type K washer TC under a band (top)",
                  "B: thermocouple band clamp (bottom)": "type K washer TC under a band (bottom)"}
    elif which == "a":
        parts = PT.joint_hardware() + PT.option_a()
        stack = [("A: KF-50 blank", -120), ("A: bottom clamp", -80), ("A: bottom centring ring", -95),
                 ("A: bottom O-ring", -95), ("A: catch puck", -150), ("A: sacrificial liner", -40),
                 ("joint: centring ring", 45), ("joint: O-ring", 45)]
        labels = {"A: KF-50 full nipple": "KF-50 full nipple (catalogue)",
                  "A: KF-50 blank": "KF-50 blank", "A: bottom clamp": "KF-50 clamp",
                  "A: bottom centring ring (stainless)": "stainless centring ring + FKM O-ring",
                  "A: catch puck (304)": "304 catch puck", "A: sacrificial liner (304)": "304 liner",
                  "joint: KF clamp": "existing KF clamp"}
    else:
        parts = PT.joint_hardware() + PT.option_c()
        stack = [("C: 304 entrance sleeve", 120), ("C: 304 bottom pan", -60)]
        labels = {"C: valve-delete spacer (316L, machined)": "316L valve-delete spacer (machined)",
                  "C: 304 entrance sleeve": "304 sleeve over the top seal and glass rim",
                  "C: 304 bottom pan": "304 pan over the bottom seal",
                  "glass tube (fused quartz)": "fused-quartz tube", "C: top glass seal (FKM)": "FKM seals"}
    pl = new_plotter((1300, 1500))
    pts, txt = [], []
    for name, shape, col, mat in parts:
        dz = 0.0
        for key, d in stack:
            if name.startswith(key):
                dz = d
        m = viz.to_mesh(shape, 0.25)
        m = section(m).translate((0, 0, dz), inplace=False)
        op = 0.35 if ("glass" in name or "quartz" in name) else 1.0
        pl.add_mesh(m, color=col, opacity=op, smooth_shading=True, specular=0.35)
        if name in labels:
            b = m.bounds
            pts.append((b[1] + 4, 0, (b[4] + b[5]) / 2))
            txt.append(labels[name])
    pl.add_point_labels(pts, txt, font_size=20, text_color="black", shape_color="white", shape_opacity=0.8,
                        point_color="black", point_size=8, always_visible=True)
    pl.camera_position = [(260, -1300, -60), (60, 0, -150 if which == "b" else -120), (0, 0, 1)]
    pl.camera.parallel_projection = True
    pl.camera.parallel_scale = 330 if which == "b" else 260
    pl.screenshot(str(IMG / f"option_{which}_exploded.png"))
    pl.close()


def assembly_gif(n=120):
    """Puck and liner drop in, the cup rises onto the cone, the clamp closes; then the reverse and a cap."""
    kf = P.JOINT
    frames = []
    cone = PT.cone_section()
    cone_m = [(viz.to_mesh(s, 0.3), c) for _, s, c, _ in cone]
    vessel = [p for p in PT.option_b(with_liner=False, with_puck=False)]
    puck = [p for p in PT.option_b() if "puck" in p[0]]
    liner = [p for p in PT.option_b() if "liner" in p[0]]
    ring = [p for p in PT.joint_hardware() if "ring" in p[0]]
    cap = [("KF-50 blank (transport cap)", PT.kf_blank(kf, 0.0).rotate((0, 0, 0), (1, 0, 0), 180), PT.STEEL, "304")]

    def m_of(parts):
        return [(section(viz.to_mesh(s, 0.3)), c) for _, s, c, _ in parts]

    vm, pm, lm, rm = m_of(vessel), m_of(puck), m_of(liner), m_of(ring)
    clamp_cache = {}

    def clamp_mesh(open_deg):
        k = round(open_deg)
        if k not in clamp_cache:
            clamp_cache[k] = section(viz.to_mesh(PT.kf_clamp(kf, 0.0, open_deg=k), 0.3))
        return clamp_cache[k]

    cap_m = section(viz.to_mesh(cap[0][1], 0.3))
    ease = lambda t: 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))  # noqa: E731
    # timeline (fractions of n): 0-.15 puck in; .15-.3 liner in; .3-.5 rise to the cone; .5-.6 clamp;
    # .6-.68 hold; .68-.76 unclamp; .76-.84 drop; .84-.92 slide out; .92-1 cap on
    for f in range(n):
        t = f / (n - 1)
        pl = new_plotter((900, 1000))
        for m, c in cone_m:
            pl.add_mesh(section(m), color=c, smooth_shading=True, specular=0.3)
        lift = -260 * (1 - ease((t - 0.3) / 0.2))      # cup starts 260 mm low
        drop = -12 * ease((t - 0.76) / 0.08)
        slide = 420 * ease((t - 0.84) / 0.08)
        off = np.array([slide, 0, lift + drop])
        if t < 0.15:
            p_off = off + [0, 0, 260 * (1 - ease(t / 0.15))]
        else:
            p_off = off
        if t < 0.3:
            l_off = off + [0, 0, 300 * (1 - ease((t - 0.15) / 0.15))]
        else:
            l_off = off
        for m, c in vm:
            pl.add_mesh(m.translate(off, inplace=False), color=c, smooth_shading=True, specular=0.35)
        for m, c in pm:
            pl.add_mesh(m.translate(p_off, inplace=False), color=c, smooth_shading=True)
        if t >= 0.15 or True:
            for m, c in lm:
                pl.add_mesh(m.translate(l_off, inplace=False), color=c, smooth_shading=True, opacity=1.0)
        ring_off = np.array([0, 0, 0]) if t < 0.76 else off * [0, 0, 0]
        for m, c in rm:
            pl.add_mesh(m.translate(ring_off, inplace=False), color=c, smooth_shading=True)
        if t < 0.5:
            od = 120
        elif t < 0.6:
            od = 120 * (1 - ease((t - 0.5) / 0.1))
        elif t < 0.68:
            od = 0
        else:
            od = 120 * ease((t - 0.68) / 0.08)
        pl.add_mesh(clamp_mesh(od), color=PT.STEEL, smooth_shading=True, specular=0.35)
        if t > 0.92:
            k = ease((t - 0.92) / 0.08)
            pl.add_mesh(cap_m.translate(off + [0, 0, 120 * (1 - k) - kf.ring_thk / 2 - 0.0], inplace=False),
                        color=PT.STEEL_DK, smooth_shading=True)
        floor(pl, -250, 650, -P.Z_JOINT_FACE)
        step = ("puck in" if t < 0.15 else "liner in" if t < 0.3 else "lift onto the cone" if t < 0.5 else
                "close the clamp" if t < 0.6 else "run" if t < 0.68 else "open the clamp" if t < 0.76 else
                f"drop {kf.ring_thk + 3:.0f} mm to clear the ring" if t < 0.84 else "slide out" if t < 0.92
                else "KF blank on top to carry it")
        pl.add_text(f"Option B: {step}", position="upper_left", font_size=14, color="black")
        pl.camera_position = [(380, -1250, -40), (130, 0, -110), (0, 0, 1)]
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 300
        img = pl.screenshot(return_img=True)
        pl.close()
        frames.append(img[::2, ::2])
    imageio.mimsave(IMG / "assembly_b.gif", frames, duration=0.08, loop=0)


if __name__ == "__main__":
    what = sys.argv[1:] or ["lineup", "b", "a", "c", "gif"]
    if "lineup" in what:
        lineup()
    for w in ("a", "b", "c"):
        if w in what:
            exploded(w)
    if "gif" in what:
        assembly_gif()
    print("rendered", what)
