#!/usr/bin/env python3
"""Layer light for the M6 layer camera: where the LED goes, and what each position shows (issue #260, optics.md §9.2).

For each candidate light position this script samples the source (an LED bar along its length, or a small window) and
every point of the three plates, and reports, from the model's geometry (cad/lpbf_low.py P block, section 7 and the
chamber openings):
  - the light's elevation above the plate and its azimuth against the recoat direction (+x, the direction streaks run);
  - the shadow a 100 um step casts (super-elevated edge, short-feed front, streak wall), in camera pixels, and how much of
    it the camera can see (the step hides part of its own shadow when the light comes from the camera's side);
  - the specular (mirror) direction against the camera: whether bare fused metal shows dark (dark field) or glares;
  - the facet tilt that glints into the camera (spatter and track ripples at that slope light up);
  - irradiance non-uniformity over the plate (Lambertian emitter, 1/d^2), and how much of the plate the light reaches
    past the parts in the chamber (dose chute, blade at park, gas knife, recoater screw), modelled as boxes.
Writes analysis/out/optics/layer_light.json / .md / .png.

Assumptions: the camera's pupil sits 50 mm up its line of sight from where it leaves the lid (layer_camera.py: lens front
at 43.3 mm); the 12 mm lens gives 26 um per pixel (layer_camera.md); emitters are Lambertian and aimed at the plate
centre; obstacles are axis-aligned boxes read off the model's code, not its B-rep.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "optics"
OUT.mkdir(parents=True, exist_ok=True)
import sys  # noqa: E402
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import lpbf_low as MODEL  # noqa: E402
import module_params as MPM  # noqa: E402

P_ = MODEL.P
IX, IY, LZ0, LZ1 = P_["ix"], P_["iy"], P_["lid_z0"], P_["lid_z1"]
CAM_P = np.array([75.0, -45.0, LZ1])                  # where the camera's line of sight leaves the lid's top face (section 7)
UP = CAM_P / np.linalg.norm(CAM_P)
CAM = CAM_P + 50.0 * UP                               # entrance pupil, ~50 mm up the line of sight
PX_UM = 26.0                                          # 12 mm C-mount lens on the IMX477 (layer_camera.md)
STEP_UM = 100.0                                       # a super-elevated edge, short-feed front or streak wall
PLATES = {"S25": 25.4 / 2, "M50": 50.8 / 2, "L75": 76.2 / 2}

# obstacles inside the chamber (x0, x1, y0, y1, z0, z1), from cad/lpbf_low.py section 7 and module_params.py
# The layer is imaged after the spread and after lasing, both with the blade at the end of its stroke (x_end, README §3.3:
# the recoater returns only at the start of the next layer); the holder is 18 x 31 mm plus the blade (section 6)
XD, XP, XE = MPM.X_DOSE, MPM.X_PARK, MPM.X_END
DY = P_["dose_y"]
OBST = {
    "dose chute": (XD - 6, XD + 6, -DY, DY, 37.0, LZ0),
    "blade holder at the end of the stroke": (XE - 9, XE + 10.5, -DY - 3, IY - 34, 0.0, 34.0),
    "gas knife": (-32.0, 32.0, -42.0, -36.0, LZ0 - 14, LZ0 - 8),
    "recoater ball screw and nut": (-IX, IX, P_["rc_screw_y"] - 8, P_["rc_screw_y"] + 8, P_["rc_screw_z"] - 8, P_["rc_screw_z"] + 8),
}


def bar(p0, p1, n=25):
    return np.linspace(p0, p1, n)


def window(c, r=10.0, n=13):
    """Points over a Ø2r window in the plane facing the plate centre."""
    c = np.asarray(c, float)
    ax = -c / np.linalg.norm(c)
    e1 = np.cross(ax, [0, 0, 1.0]); e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    pts = [c]
    for k in range(n - 1):
        a = 2 * math.pi * k / (n - 1)
        pts.append(c + r * 0.7 * (math.cos(a) * e1 + math.sin(a) * e2))
    return np.array(pts)


# light positions: name -> (points, where, note)
LIGHTS = {
    "A. inside, low on the right wall (round 4)": (bar((IX - 6, -45, 34), (IX - 6, 45, 34)), "inside",
        "LED bar on the +x wall, z 30-38 (trapped the right liner)"),
    "B. inside, lid underside (as drawn)": (bar((IX - 10, -45, LZ0 - 8), (IX - 10, 45, LZ0 - 8)), "inside",
        "LED bar x 126-134, z 112-120, along y (cad/lpbf_low.py section 7)"),
    "C. inside, low on the back wall": (bar((-45, IY - 6, 22), (45, IY - 6, 22)), "inside",
        "LED bar on the back wall under the ball screw, in front of the lower back liner"),
    "D. outside, new low window in the back wall, left of the inlet plenum": (window((-105.0, IY, 25.0)), "outside",
        "Ø20 clear window at x -105, z 25 (the plenum's flange covers x ±78, z < 40 outside; a KF40 flange there clears it); LED behind it"),
    "E. outside, new low window in the back wall, right of the inlet plenum": (window((105.0, IY, 25.0)), "outside",
        "Ø20 clear window at x +105, z 25"),
    "F. outside, new low window in the right wall": (window((IX, 10.0, 25.0)), "outside",
        "Ø20 clear window at y +10, z 25, under the vacuum-port adapter (z 42-98)"),
    "G. outside, through the camera's own window (beamsplitter)": (np.array([CAM]), "outside",
        "coaxial with the camera; the Ø20 aperture only passes light from on the camera's axis"),
}


def blocked(p, s):
    """True if the segment p -> s crosses any obstacle box (slab test)."""
    d = s - p
    for (x0, x1, y0, y1, z0, z1) in OBST.values():
        t0, t1 = 0.0, 1.0
        ok = True
        for a, lo, hi in ((0, x0, x1), (1, y0, y1), (2, z0, z1)):
            if abs(d[a]) < 1e-12:
                if p[a] < lo or p[a] > hi:
                    ok = False
                    break
            else:
                ta, tb = sorted(((lo - p[a]) / d[a], (hi - p[a]) / d[a]))
                t0, t1 = max(t0, ta), min(t1, tb)
                if t0 > t1:
                    ok = False
                    break
        if ok and t1 > 1e-6 and t0 < 1 - 1e-6:
            return True
    return False


def angle(u, v):
    return math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))))))


def analyse(src, r_plate):
    g = np.linspace(-r_plate, r_plate, 15)
    pts = [np.array([x, y, 0.0]) for x in g for y in g if x * x + y * y <= r_plate ** 2 + 1e-9]
    c_src = src.mean(axis=0)
    n_src = -c_src / np.linalg.norm(c_src)                  # emitters aimed at the plate centre
    rec = dict(elev=[], across=[], shadow_px=[], visible_px=[], spec_to_cam=[], glint_tilt=[], E=[], reach=[])
    for p in pts:
        to_c = CAM - p
        vis, E = 0, 0.0
        for s in src:
            if not blocked(p, s):
                vis += 1
                d = s - p
                dist = np.linalg.norm(d)
                cos_i = d[2] / dist
                cos_e = max(0.0, float(np.dot(-d / dist, n_src)))
                E += cos_i * cos_e / dist ** 2
        rec["reach"].append(vis / len(src))
        rec["E"].append(E)
        L = c_src - p
        Lh = math.hypot(L[0], L[1])
        el = math.degrees(math.atan2(L[2], Lh)) if Lh > 1e-9 else 90.0
        rec["elev"].append(el)
        rec["across"].append(abs(L[1]) / Lh if Lh > 1e-9 else 0.0)      # |sin| of the light's azimuth against x
        sh = STEP_UM / math.tan(math.radians(el)) if el < 89.9 else 0.0
        rec["shadow_px"].append(sh / PX_UM)
        # the part of the shadow hidden behind the step from the camera's side
        Ch = math.hypot(to_c[0], to_c[1])
        el_c = math.degrees(math.atan2(to_c[2], Ch))
        if Lh > 1e-9:
            sdir = -L[:2] / Lh                                   # shadow runs away from the light
            away = -to_c[:2] / Ch                                # ground hidden behind a step lies away from the camera
            cosd = float(np.dot(sdir, away))
            hidden = STEP_UM * max(0.0, cosd) / math.tan(math.radians(el_c))
            rec["visible_px"].append(max(0.0, sh - hidden) / PX_UM)
        else:
            rec["visible_px"].append(0.0)
        inc = (p - c_src) / np.linalg.norm(p - c_src)
        spec = inc * np.array([1, 1, -1.0])
        rec["spec_to_cam"].append(angle(spec, to_c))
        b = L / np.linalg.norm(L) + to_c / np.linalg.norm(to_c)
        rec["glint_tilt"].append(angle(b, np.array([0, 0, 1.0])))
    E = np.array(rec["E"])
    lit = E[E > 0]
    return dict(n=len(pts), elev=(min(rec["elev"]), max(rec["elev"])), across_mean=float(np.mean(rec["across"])),
                shadow_px=(min(rec["shadow_px"]), max(rec["shadow_px"])), visible_px=(min(rec["visible_px"]), max(rec["visible_px"])),
                spec_to_cam_min=min(rec["spec_to_cam"]), glint_tilt=(min(rec["glint_tilt"]), max(rec["glint_tilt"])),
                uniformity=float(lit.max() / lit.min()) if lit.size and lit.min() > 0 else float("inf"),
                reach_pct=100 * float(np.mean(np.array(rec["reach"]) > 0.5)))


res = dict(camera=dict(pupil=CAM.tolist(), line_of_sight_off_vertical_deg=math.degrees(math.acos(UP[2])),
                       azimuth_deg=math.degrees(math.atan2(UP[1], UP[0])), px_um=PX_UM),
           obstacles=OBST, lights={})
for name, (src, where, note) in LIGHTS.items():
    res["lights"][name] = dict(where=where, note=note, plates={pl: analyse(src, r) for pl, r in PLATES.items()})

# the main laser window: can a light outside the beam's envelope reach the plate through it? Sources on a ring r 23-45 mm at
# z 165-185 (between the window's retaining ring, top z 163, and the f-theta, bottom z 186): the Ø44 ring and the Ø42 bore stop them
ring_ok, tests, passing = 0, 0, []
for rs in (23.0, 30.0, 40.0, 45.0):
    for zs in (165.0, 175.0, 185.0):
        for xp in np.linspace(-38.1, 38.1, 9):
            tests += 1
            s, p = np.array([rs, 0.0, zs]), np.array([xp, 0.0, 0.0])
            ok = True
            for z_, r_ in ((163.0, 22.0), (P_["z_win0"] + P_["win_t"] + 0.75, 22.0), (136.0, 21.0), (P_["z_win0"], 21.0)):
                t = (z_ - p[2]) / (s[2] - p[2])
                if abs(p[0] + t * (s[0] - p[0])) > r_:
                    ok = False
            if ok:
                ring_ok += 1
                passing.append(dict(r_src=rs, z_src=zs, x_plate=float(xp), elev_deg=math.degrees(math.atan2(zs, rs - xp))))
res["laser_window"] = dict(rays_tested=tests, rays_passing=ring_ok, passing=passing,
                           note="LED on a ring r 23-45 mm at z 165-185 aimed at L75 plate points through the Ø44 retaining ring and Ø42 bore")
(OUT / "layer_light.json").write_text(json.dumps(res, indent=1, default=float))

L = ["# Layer light: what each LED position shows (`analysis/optics/layer_light.py`)", "",
     f"Camera: pupil at ({CAM[0]:.0f}, {CAM[1]:.0f}, {CAM[2]:.0f}), {res['camera']['line_of_sight_off_vertical_deg']:.1f}° off vertical, from the front-right "
     f"(azimuth {res['camera']['azimuth_deg']:.0f}° from +x); 12 mm lens, {PX_UM:.0f} µm per pixel. Streaks from a nicked blade run along x (the recoat "
     "direction), so light needs a y component to shadow them. 'Across streaks' is the mean |sin| of the light's azimuth against x (1 = straight "
     f"across). Shadow = what a {STEP_UM:.0f} µm step casts; 'visible' subtracts the part the step hides from the camera. 'Mirror to camera' is the "
     "smallest angle between the plate's mirror reflection of the light and the camera: well above ~10° means fused metal shows dark and powder bright "
     "(dark field); near 0 it glares. 'Glint tilt' is the facet slope that reflects the light into the camera. 'Uniformity' is the brightest over the "
     "dimmest lit point (Lambertian emitter, 1/d²). 'Reached' is the share of the plate that sees more than half of the source past the dose chute, "
     "the blade at park, the gas knife and the recoater screw.", "",
     "| Light | Plate | Elevation (°) | Across streaks | Shadow of 100 µm (px) | Visible to the camera (px) | Mirror to camera (°) | Glint tilt (°) | Uniformity | Reached (%) |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for name, d in res["lights"].items():
    for pl, a in d["plates"].items():
        L.append(f"| {name} | {pl} | {a['elev'][0]:.0f}–{a['elev'][1]:.0f} | {a['across_mean']:.2f} | {a['shadow_px'][0]:.1f}–{a['shadow_px'][1]:.1f} | "
                 f"{a['visible_px'][0]:.1f}–{a['visible_px'][1]:.1f} | {a['spec_to_cam_min']:.0f} | {a['glint_tilt'][0]:.0f}–{a['glint_tilt'][1]:.0f} | "
                 + (f"{a['uniformity']:.1f}" if a["reach_pct"] > 0 else "– (blocked)") + f" | {a['reach_pct']:.0f} |")
_rs = sorted({q["r_src"] for q in passing})
_xs = [q["x_plate"] for q in passing]
_el = [q["elev_deg"] for q in passing]
L += ["", f"Main laser window: {ring_ok} of {tests} rays from a light ring between the window's retaining ring and the f-theta (r 23–45 mm, z 165–185) "
      "reach the L75 plate through the Ø44 ring and the Ø42 bore" + (f": only from r = {', '.join(f'{r:.0f}' for r in _rs)} mm, onto x {min(_xs):.0f} to "
      f"{max(_xs):.0f} mm of the plate, at {min(_el):.0f}–{max(_el):.0f}° elevation. A light there sits against the beam's own envelope "
      "(the L75 edge ray passes r ≈ 19–26 mm at that height for k 0.33–0.63) and in the scattered 1070 nm light, and it lights only the far side. "
      "The window's aperture is the beam's, so it can't carry the light." if passing else "."), "",
      "Light positions: " + "; ".join(f"{k}: {v[2]}" for k, v in LIGHTS.items()) + "."]
(OUT / "layer_light.md").write_text("\n".join(L) + "\n")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.6, 4.6), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    names = list(res["lights"])
    lab = [n.split(".")[0] for n in names]
    lo = [res["lights"][n]["plates"]["L75"]["visible_px"][0] for n in names]
    hi = [res["lights"][n]["plates"]["L75"]["visible_px"][1] for n in names]
    y = np.arange(len(names))[::-1]
    COL = {"outside": "#2a78d6", "inside": "#eb6834"}       # dataviz categorical slots 1 and 2 (validated: CVD dE 24.7)
    for yy, a, b, n in zip(y, lo, hi, names):
        d = res["lights"][n]
        col = COL[d["where"]]
        blocked = d["plates"]["L75"]["reach_pct"] == 0
        label = n.split(". ", 1)[1]
        if blocked:   # hatched, and said in words: the blade holder stands between the light and the plate when the layer is imaged
            ax.barh(yy, b - a, left=a, height=0.36, color="#fcfcfb", edgecolor=col, hatch="////", lw=1.0)
            label += ": blocked by the blade holder while the layer is imaged"
        elif b - a < 0.05:
            label += ": 0 px (every shadow falls behind its step)"
        else:
            ax.barh(yy, b - a, left=a, height=0.36, color=col, lw=0)
        ax.text(max(b, 0) + 0.5, yy, label, va="center", fontsize=6.8, color="#52514e")
    ax.set_yticks(y, lab)
    ax.set_xlabel("shadow of a 100 µm step the camera sees, over the L75 plate (pixels, 26 µm each)", fontsize=8, color="#0b0b0b")
    ax.set_xlim(0, max(hi) * 2.6)
    ax.grid(axis="x", alpha=0.25, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    from matplotlib.patches import Patch
    ax.set_ylim(-0.7, len(names) - 0.4)
    ax.legend(handles=[Patch(color=COL["inside"], label="light inside the chamber"), Patch(color=COL["outside"], label="light outside, through a window")],
              fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2)
    ax.set_title("Layer light: how visible a 100 µm height step is to the camera", fontsize=8.5, color="#0b0b0b")
    fig.tight_layout()
    fig.savefig(OUT / "layer_light.png")
except Exception as e:  # figure is optional
    print("figure skipped:", e)

print((OUT / "layer_light.md").read_text())
