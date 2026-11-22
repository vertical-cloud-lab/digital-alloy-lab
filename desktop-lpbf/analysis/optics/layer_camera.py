#!/usr/bin/env python3
"""Layer camera (BOM M6, Raspberry Pi HQ camera) from its mounted position in cad/lpbf_low.py (issue #260).

The model puts the camera's line of sight from cam_p = (75, -45, 136) (where it leaves the lid's top face) to the plate
centre. Along it: the lid's vertical Ø22 hole (z 120-136), the boss's Ø22 bore (to t = 32.3 mm along the axis), a Ø15
aperture (t 31.8-36.5) under the Ø1 in. window (t 36.5-39.5), a retaining ring with a Ø18 opening (t 40.3-43.3) and the
lens front at t = 43.3. This script traces rays from points on the three plates through a sampled entrance pupil and
those openings, and reports field of view, pixel footprint, depth of field, the Scheimpflug tilt and vignetting for
four lenses. Writes analysis/out/optics/layer_camera.json / .md / .png.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "optics"
OUT.mkdir(parents=True, exist_ok=True)

CAM_P = np.array([75.0, -45.0, 136.0])
UP = CAM_P / np.linalg.norm(CAM_P)              # from the plate centre toward the camera
DIST0 = float(np.linalg.norm(CAM_P))            # 161.7 mm from cam_p to the plate centre
TILT = math.degrees(math.acos(UP[2]))           # line of sight off the plate normal
E1 = np.cross(UP, [0, 0, 1.0]); E1 /= np.linalg.norm(E1)    # horizontal, across the line of sight
E2 = np.cross(E1, UP)                                          # in the tilt plane
T_FRONT = 43.27                                  # lens front along the axis from cam_p (model)
# Sony IMX477 (Raspberry Pi HQ camera): 4056 x 3040 px, 1.55 um, 6.287 x 4.712 mm
SENS = dict(px=1.55e-3, nx=4056, ny=3040, w=6.287, h=4.712)
PLATES = {"S25": 25.4 / 2, "M50": 50.8 / 2, "L75": 76.2 / 2}
LENSES = {"6 mm (Raspberry Pi CS-mount)": 6.0, "12 mm C-mount": 12.0, "16 mm (Raspberry Pi C-mount)": 16.0, "25 mm C-mount": 25.0}


VARIANTS = {
    "as drawn (vertical Ø22 lid hole, Ø22 bore, Ø15 aperture)": dict(lid="vertical", lid_r=11.0, bore_r=11.0, ap_r=7.5),
    "lid hole drilled on the line of sight, Ø22": dict(lid="axis", lid_r=11.0, bore_r=11.0, ap_r=7.5),
    "Ø30 on the line of sight through lid and boss, Ø20 aperture": dict(lid="axis", lid_r=15.0, bore_r=15.0, ap_r=10.0),
}


def openings_pass(P, Q, var=None):
    """True where the segment from plate point P to pupil point Q clears every opening. P, Q: (..., 3)."""
    var = var or next(iter(VARIANTS.values()))
    P, Q = np.broadcast_arrays(P, Q)
    d = Q - P
    ok = np.ones(P.shape[:-1], bool)
    if var["lid"] == "vertical":
        # lid hole: vertical, centred on (75, -45), z 120..136
        for z in np.linspace(120.0, 136.0, 9):
            s = (z - P[..., 2]) / d[..., 2]
            X = P + s[..., None] * d
            ok &= np.hypot(X[..., 0] - 75.0, X[..., 1] + 45.0) <= var["lid_r"]
        axis = ((0.0, 31.77, var["bore_r"]),)
    else:
        axis = ((-16.0 / UP[2], 0.0, var["lid_r"]), (0.0, 31.77, var["bore_r"]))
    # along-axis openings: (t0, t1, radius)
    for t0, t1, rad in axis + ((31.77, 36.52, var["ap_r"]), (36.52, 39.52, 12.7), (40.27, 43.27, 9.0)):
        for t in np.linspace(t0, t1, 5):
            # plane perpendicular to the axis at distance t from cam_p
            c = CAM_P + UP * t
            s = ((c - P) @ UP) / (d @ UP)
            X = P + s[..., None] * d
            rel = X - c
            ok &= np.linalg.norm(rel - (rel @ UP)[..., None] * UP, axis=-1) <= rad
    return ok


def project(P, E, v):
    """Pinhole projection of plate points onto the sensor (mm) behind the pupil E at image distance v."""
    rel = P - E
    depth = -(rel @ UP)                    # distance in front of the pupil along the axis
    return v * (rel @ E1) / depth, v * (rel @ E2) / depth, depth


res = dict(geometry=dict(cam_p=CAM_P.tolist(), tilt_deg=TILT, dist_cam_p_to_centre=DIST0, lens_front_t=T_FRONT),
           sensor=SENS, lenses=[])
th = np.linspace(0, 2 * np.pi, 72, endpoint=False)
for vname, var in VARIANTS.items():
  for lname, f in LENSES.items():
    for t_pupil in (T_FRONT + 10.0,):            # entrance pupil ~10 mm behind the lens front (assumed)
        E = CAM_P + UP * t_pupil
        u = DIST0 + t_pupil                      # pupil to plate centre
        v = 1 / (1 / f - 1 / u)
        m = v / u
        for N in (2.8, 4.0, 8.0):
            a = f / N / 2                        # entrance pupil radius
            # pupil samples
            rr = np.sqrt(np.linspace(0.02, 1, 12))[:, None] * a
            pp = np.linspace(0, 2 * np.pi, 16, endpoint=False)[None, :]
            Q = (E + (rr * np.cos(pp))[..., None] * E1 + (rr * np.sin(pp))[..., None] * E2).reshape(-1, 3)
            rec = dict(variant=vname, lens=lname, f_mm=f, N=N, pupil_t=t_pupil, u_mm=u, v_mm=v, mag=m,
                       px_on_plate_um=SENS["px"] / m * 1e3, px_along_tilt_um=SENS["px"] / m / math.cos(math.radians(TILT)) * 1e3,
                       fov_mm=[SENS["w"] / m, SENS["h"] / m],
                       airy_fwhm_on_plate_um=1.03 * 0.55e-3 * N / m * 1e3,
                       dof_total_mm=2 * N * (2 * SENS["px"]) * (m + 1) / m ** 2,
                       scheimpflug_deg=math.degrees(math.atan(m * math.tan(math.radians(TILT)))), plates={})
            for pl, R in PLATES.items():
                # edge points and the area grid
                edge = np.stack([R * np.cos(th), R * np.sin(th), np.zeros_like(th)], -1)
                g = np.linspace(-R, R, 21)
                X, Y = np.meshgrid(g, g)
                inside = X ** 2 + Y ** 2 <= R ** 2
                area = np.stack([X[inside], Y[inside], np.zeros(inside.sum())], -1)
                def trans(pts):
                    return openings_pass(pts[:, None, :], Q[None, :, :], var).mean(axis=1)
                te, ta = trans(edge), trans(area)
                xs, ys, dep = project(edge, E, v)
                in_frame_land = (np.abs(xs) <= SENS["w"] / 2) & (np.abs(ys) <= SENS["h"] / 2)
                in_frame_port = (np.abs(xs) <= SENS["h"] / 2) & (np.abs(ys) <= SENS["w"] / 2)
                depth_span = float(dep.max() - dep.min())
                blur_um = (2 * a) * (depth_span / 2) / u * 1e3      # object-side blur at the far/near edge, no tilt
                rec["plates"][pl] = dict(edge_transmission_min=float(te.min()), edge_transmission_mean=float(te.mean()),
                                         area_fraction_over_50pct=float((ta > 0.5).mean()), area_fraction_fully=float((ta > 0.99).mean()),
                                         fits_landscape=bool(in_frame_land.all()), fits_portrait=bool(in_frame_port.all()),
                                         depth_span_mm=depth_span, edge_defocus_blur_um=blur_um)
            res["lenses"].append(rec)

# where the line of sight sits in the lid hole
z_bot = 120.0
s = (z_bot - CAM_P[2]) / (-UP[2])
X = CAM_P - UP * s
res["geometry"]["axis_offset_in_lid_hole_at_z120_mm"] = float(math.hypot(X[0] - 75.0, X[1] + 45.0))
res["geometry"]["lid_hole_radius_mm"] = 11.0
(OUT / "layer_camera.json").write_text(json.dumps(res, indent=1))

L = ["# Layer camera from its mounted position (`analysis/optics/layer_camera.py`)", "",
     f"Line of sight {TILT:.1f}° off the plate normal, {DIST0:.1f} mm from the lid face to the plate centre; entrance pupil taken "
     "10 mm behind the lens front (assumed). Sensor IMX477, 1.55 µm pixels, 6.29 × 4.71 mm.", "",
     f"**The lid hole is vertical while the line of sight is tilted:** at the lid's underside (z 120) the axis is "
     f"{res['geometry']['axis_offset_in_lid_hole_at_z120_mm']:.1f} mm from the hole's centre, against an 11 mm radius.", "",
     "| Openings | Lens | N | Mag. | Pixel on plate, across / along tilt (µm) | Diffraction FWHM on plate (µm) | FOV (mm) | DOF, 2 px blur (mm) | Scheimpflug tilt (°) | S25 / M50 / L75: fits frame (land./port.) | edge light reaching the pupil, min (%) | plate area > 50 % lit (%) | edge blur without tilt (µm) |",
     "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in res["lenses"]:
    fits = " / ".join(("L" if p["fits_landscape"] else "–") + ("P" if p["fits_portrait"] else "–") for p in r["plates"].values())
    tr = " / ".join(f"{100*p['edge_transmission_min']:.0f}" for p in r["plates"].values())
    ar = " / ".join(f"{100*p['area_fraction_over_50pct']:.0f}" for p in r["plates"].values())
    bl = " / ".join(f"{p['edge_defocus_blur_um']:.0f}" for p in r["plates"].values())
    if r["variant"] != list(VARIANTS)[0] and not (r["f_mm"] in (12.0, 16.0) and r["N"] == 4.0):
        continue
    L.append(f"| {r['variant'].split(' (')[0]} | {r['lens']} | {r['N']} | {r['mag']:.4f} | {r['px_on_plate_um']:.1f} / {r['px_along_tilt_um']:.1f} | {r['airy_fwhm_on_plate_um']:.0f} | "
             f"{r['fov_mm'][0]:.0f} × {r['fov_mm'][1]:.0f} | {r['dof_total_mm']:.1f} | {r['scheimpflug_deg']:.1f} | {fits} | {tr} | {ar} | {bl} |")
(OUT / "layer_camera.md").write_text("\n".join(L) + "\n")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rec = [r for r in res["lenses"] if r["f_mm"] == 12.0 and r["N"] == 4.0][0]
    E = CAM_P + UP * rec["pupil_t"]
    a = rec["f_mm"] / rec["N"] / 2
    rr = np.sqrt(np.linspace(0.02, 1, 12))[:, None] * a
    pp = np.linspace(0, 2 * np.pi, 16, endpoint=False)[None, :]
    Q = (E + (rr * np.cos(pp))[..., None] * E1 + (rr * np.sin(pp))[..., None] * E2).reshape(-1, 3)
    g = np.linspace(-40, 40, 81)
    X, Y = np.meshgrid(g, g)
    pts = np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], -1)
    fig, axs = plt.subplots(1, 2, figsize=(9, 4.3), dpi=150)
    for ax, (vname, var) in zip(axs, [list(VARIANTS.items())[0], list(VARIANTS.items())[2]]):
        T = openings_pass(pts[:, None, :], Q[None, :, :], var).mean(axis=1).reshape(X.shape)
        im = ax.pcolormesh(X, Y, 100 * T, cmap="Greys_r", vmin=0, vmax=100, shading="auto")
        for pl, R in PLATES.items():
            ax.add_patch(plt.Circle((0, 0), R, fill=False, color="#c0504d", lw=1))
            ax.text(R * 0.72, R * 0.72, pl, color="#c0504d", fontsize=7)
        ax.plot([0, 75], [0, -45], color="#1f4e79", lw=0.8)
        ax.set_aspect("equal")
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.set_title(vname.split(" (")[0] if "drawn" in vname else "Ø30 bore on the line of sight, Ø20 aperture", fontsize=8)
    fig.colorbar(im, ax=axs, label="% of the pupil that sees the point (12 mm, f/4)")
    fig.suptitle("Layer camera: vignetting by the lid hole and the boss (camera toward +x, -y)", fontsize=9)
    fig.savefig(OUT / "layer_camera.png")
except Exception as e:
    print("figure skipped:", e)
print((OUT / "layer_camera.md").read_text())
