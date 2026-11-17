"""Renders for the heated build modules, the reservoirs and the automation features (lpbf_low.py + modules_low.py).

Run (headless):  xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/cad/render_modules.py
Writes to desktop-lpbf/cad/img/modules/.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lpbf_low as M  # noqa: E402
import module_params as MP  # noqa: E402
import modules_low as ML  # noqa: E402
import render_low as R  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "img" / "modules"
W, H = 1400, 900
GW, GH = 860, 560
HIDE = R.SECTION_HIDE


class Scene(R.Scene):
    """render_low.Scene, posed with lpbf_low.part_location (Z stage follows the piston, the module carries its stack)."""

    def set(self, visible=None, state=None, opacity=None, section=False, explode=None):
        state = state or {}
        for i, (a, e, s, p) in self.actors.items():
            vis = True if visible is None else bool(visible(p))
            loc = M.part_location(p, state)
            m = np.eye(4) if loc is None else R.loc_matrix(loc)
            if explode is not None:
                m = m.copy()
                m[:3, 3] += explode(p)
            op = p.opacity if opacity is None else opacity(p)
            cut = section and s is not None and s != "empty"
            hide = section and (any(k in p.name for k in HIDE) or s == "empty")
            a.SetVisibility(vis and not cut and not hide)
            a.user_matrix = m
            a.prop.opacity = op
            if e is not None:
                e.SetVisibility(vis and not cut and not hide and op > 0.3)
                e.user_matrix = m
            if s is not None and s != "empty":
                s.SetVisibility(vis and cut)
                s.user_matrix = m


def collect(fn, *args):
    """Run one of the modules_low builders into a fresh part list."""
    parts = []

    def add(name, shape, color, step, explode=(0, 0, 0), **kw):
        parts.append(M.Part(name, shape, color, step, tuple(float(e) for e in explode), **kw))
    fn(M, add, *args)
    return parts


def shifted(parts, dx=0.0, dy=0.0, dz=0.0, section=True):
    out = []
    for p in parts:
        q = M.Part(p.name, p.shape.translate(M.V(dx, dy, dz)), p.color, p.step, p.explode, group=p.group, bom=p.bom, mat=p.mat,
                   opacity=p.opacity, section=section, tags=p.tags)
        out.append(q)
    return out


def label(sc, pts, texts, size=15):
    sc.pl.add_point_labels(pts, texts, font_size=size, text_color="#1d2733", shape=None, show_points=False, always_visible=True)


def three_modules():
    parts, labs = [], []
    for k, (key, dx) in enumerate((("S25", -150.0), ("M50", 0.0), ("L75", 170.0))):
        parts += shifted(collect(ML.add_build_module, key), dx)
        m = MP.MODULES[key]
        labs.append(((dx, -60.0, 40.0), f"{key}: Ø{m['plate_d']:.1f} plate, {m['heaters']} x {m['heater_w']:.0f} W"))
    sc = Scene(parts, (W, H))
    sc.set(section=True)
    f = (10.0, 0.0, -55.0)
    sc.cam(R.orbit(f, 560, -10, 12), f)
    label(sc, [p for p, _ in labs], [t for _, t in labs])
    sc.title("Three build modules, one floor port: spigot, honed 316L cylinder, heated plate stack (cut at y = 0)", 12)
    Image.fromarray(sc.shot()).save(OUT / "three-modules.png")


def stack_exploded():
    parts = collect(ML.add_build_module, "M50")
    keep = [p for p in parts if p.group == "piston"]
    order = ["Build plate", "Heater block", "Cartridge heaters", "Type K", "Thermal cutoff", "Radiation shields", "Macor standoffs",
             "Piston head", "Bore seal", "Hollow piston rod", "Rod end", "Striker"]
    lift = {"Build plate": 150, "Heater block": 100, "Cartridge heaters": 60, "Type K": 60, "Thermal cutoff": 60, "Radiation shields": 30,
            "Macor standoffs": 15, "Piston head": 0, "Bore seal": 0, "Hollow piston rod": -30, "Rod end": -60, "Striker": -75}
    out = []
    for p in keep:
        dz = next((v for k, v in lift.items() if p.name.startswith(k)), 0)
        out += shifted([p], 0, 0, dz, section=False)
    sc = Scene(out, (W, H))
    sc.set()
    f = (0.0, 0.0, 20.0)
    sc.cam(R.orbit(f, 640, -28, 16), f)
    sc.title("M50 heated plate stack, exploded: plate (bayonet), heater block (2 x 40 W, 3 type K, 240 C cutoff),\n"
             "2 shields, 3 Macor standoffs, piston head + bore seal, hollow rod, potted cable exit, 430 striker", 11)
    Image.fromarray(sc.shot()).save(OUT / "heater-stack-exploded.png")


def reservoirs():
    parts, labs = [], []
    for key, dx in (("S", -110.0), ("M", -40.0), ("L", 50.0)):
        parts += shifted(collect(ML.add_reservoir, key, 0.0, 0.0), dx, section=False)
        r = MP.RESERVOIRS[key]
        labs.append(((dx, -70.0, 85.0), f"{key}: {r['vol_cm3']:.0f} cm³, {r['slot']:.0f} mm outlet"))
    sc = Scene(parts, (W, H))
    sc.set()
    f = (-25.0, 0.0, 30.0)
    sc.cam(R.orbit(f, 620, -30, 24), f)
    label(sc, [p for p, _ in labs], [t for _, t in labs])
    sc.title("Reservoirs on one dock: wedge (plane-flow) hoppers, 35° walls, shutters shown open; handles all at z = 258", 12)
    Image.fromarray(sc.shot()).save(OUT / "reservoirs.png")


def machine_stills():
    parts = M.build(module="L75")
    sc = Scene(parts, (W, H))
    f = (0.0, 0.0, -40.0)
    sc.set(section=True, state={"piston": -20.0})
    sc.cam(R.orbit(f, 980, -18, 6), f)
    sc.title("L75 module in the chamber (section at y = 0, piston at -20 mm): heated plate stack, magnet coupling, Z stage", 12)
    Image.fromarray(sc.shot()).save(OUT / "heated-module-section.png")
    vis = lambda p: not any(k in p.name for k in HIDE)
    sc.set(visible=vis, state={"gdoor": 470.0, "door": 95.0, "piston": MP.Z_P_MAX, "drawer": -120.0, "cartridge": -125.0})
    f2 = (-20.0, -60.0, 70.0)
    sc.cam(R.orbit(f2, 1500, 20, 16), f2)
    sc.title("Robot-facing: door down, plate 8 mm proud for a gripper, cover-slide drawer and reservoir slid out", 12)
    Image.fromarray(sc.shot()).save(OUT / "automation-open.png")


def module_swap_gif():
    parts = M.build(module="L75")
    sc = Scene(parts, (GW, GH))
    vis = lambda p: not any(k in p.name for k in HIDE[:2] + ("Sliding guard", "OD 7+"))
    f = (0.0, -120.0, -60.0)
    frames = []
    seq = [({"gdoor": 470.0}, "zstage", 0.0, MP.ZSTAGE_RELEASE, 10, "Collar on the rod, thumb screws out; the Z arm drops 45 mm and the magnet lets go"),
           ({"gdoor": 470.0, "zstage": MP.ZSTAGE_RELEASE}, "module", 0.0, M.MOTION["module"]["hi"], 34,
            "The module drops 40 mm out of the port, slides forward under the outlet plenum and lifts over the guard sill")]
    for base, g, a, b, n, txt in seq:
        for k in range(n + 1):
            st = dict(base)
            st[g] = a + (b - a) * R.ease(k / n)
            sc.set(visible=vis, state=st)
            sc.cam(R.orbit(f, 1250, -38, 6), f)
            sc.title(txt, 11)
            frames.append(sc.shot())
    R.save_gif(frames, OUT / "module-swap.gif", ms=100, hold_last=12)


def automation_gif():
    parts = M.build(module="M50")
    sc = Scene(parts, (GW, GH))
    vis = lambda p: not any(k in p.name for k in HIDE[2:])
    f = (0.0, -40.0, 60.0)
    st = {}
    frames = []
    seq = [("gdoor", 0.0, 470.0, 8, "Guard door slides open (laser off, plate < 50 C, chamber at 1 atm)"),
           ("door", 0.0, 95.0, 10, "Chamber door drops down"),
           ("piston", 0.0, MP.Z_P_MAX, 8, "Plate rises 8 mm proud of the floor; a through-beam confirms it; gripper twists the bayonet"),
           ("piston", MP.Z_P_MAX, 0.0, 6, "New plate seated, back to z = 0"),
           ("drawer", 0.0, -120.0, 8, "Cover-slide drawer pulls out of the lid's front edge"),
           ("drawer", -120.0, 0.0, 6, "Fresh cover slide in"),
           ("cartridge", 0.0, -125.0, 8, "Reservoir slides out on its dovetail (shutter springs shut)"),
           ("cartridge", -125.0, 0.0, 6, "Next reservoir docks: the shutter opens, the NFC tag is read"),
           ("door", 95.0, 0.0, 8, "Door up, latched; purge")]
    for g, a, b, n, txt in seq:
        for k in range(n + 1):
            st[g] = a + (b - a) * R.ease(k / n)
            sc.set(visible=vis, state=dict(st))
            sc.cam(R.orbit(f, 1200, 24, 18), f)
            sc.title(txt, 11)
            frames.append(sc.shot())
    R.save_gif(frames, OUT / "automation.gif", ms=100, hold_last=10)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    what = sys.argv[1:] or ["three", "stack", "reservoirs", "machine", "swap", "automation"]
    fns = {"three": three_modules, "stack": stack_exploded, "reservoirs": reservoirs, "machine": machine_stills,
           "swap": module_swap_gif, "automation": automation_gif}
    for w in what:
        fns[w]()
        print("done", w, flush=True)
