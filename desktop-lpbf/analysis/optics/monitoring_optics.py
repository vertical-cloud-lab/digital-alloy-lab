#!/usr/bin/env python3
"""In-situ monitoring options: resolution, field, depth of field, temperature floors and data rates (issue #260, monitoring.md).

Numbers only. The ports and the room for each camera come from monitoring_views.py and the checks in monitoring.md §3; the beam
path from optics.md. Every vendor figure is listed with its source in monitoring.md. Writes analysis/out/monitoring/optics.json
and optics.md.

    python desktop-lpbf/analysis/optics/monitoring_optics.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "monitoring"
OUT.mkdir(parents=True, exist_ok=True)

C2 = 14388.0          # second radiation constant, µm K


def n_fs(lam_um):
    """Fused silica (Malitson 1965)."""
    l2 = lam_um ** 2
    return math.sqrt(1 + 0.6961663 * l2 / (l2 - 0.0684043 ** 2) + 0.4079426 * l2 / (l2 - 0.1162414 ** 2) + 0.8974794 * l2 / (l2 - 9.896161 ** 2))


def planck(lam_um, T):
    """Relative spectral radiance (Wien-Planck), arbitrary units."""
    return lam_um ** -5 / (math.exp(C2 / (lam_um * T)) - 1)


def true_from_apparent(T_app_C, lam_um, eps):
    """Single-band (brightness) temperature to true temperature for emissivity eps (Wien)."""
    Ta = T_app_C + 273.15
    return 1 / (1 / Ta + lam_um / C2 * math.log(eps)) - 273.15


R = {}

# ---------------------------------------------------------------- 1. coaxial camera through the f-theta and galvo (de-scanned)
F1 = 160.0                      # FTH160-1064
D_PUP = 25.4 * math.cos(math.radians(45))   # the Ø1 in. dichroic at 45° limits the return beam to ~18 mm in one axis (galvo: 20 mm)
NA = D_PUP / 2 / F1
lam0, lam_c, half_band = 1.070, 0.850, 0.020
df_1070_850 = F1 * (n_fs(lam_c) - n_fs(lam0)) / (n_fs(lam0) - 1)              # the 850 nm focus sits this much closer to the lens
df_band = F1 * (n_fs(lam_c - half_band) - n_fs(lam_c + half_band)) / (n_fs(lam_c) - 1)
coax = dict(
    f_theta_mm=F1, pupil_mm=round(D_PUP, 1), NA=round(NA, 4),
    rayleigh_um=round(0.61 * lam_c / NA, 1),
    focal_shift_1070_to_850_mm=round(df_1070_850, 2),
    band_850pm20_focal_spread_mm=round(df_band, 3),
    band_blur_um_full_NA=round(1e3 * NA * df_band, 1),
    band_blur_um_at_NA_0p03=round(1e3 * 0.03 * df_band, 1),
    lateral_colour_at_L75_edge_um=round(1e3 * df_1070_850 * 38.1 / F1, 0),
    lateral_colour_at_M50_edge_um=round(1e3 * df_1070_850 * 25.4 / F1, 0),
    note="singlet estimate for an all-fused-silica f-theta used off its 1064 nm design; the real lens corrects some of it",
)
cams = {  # pixel (µm), ROI used, frame rate at that ROI, source
    "Raspberry Pi Global Shutter (IMX296)": dict(px=3.45, roi=(128, 96), fps=536, src="community measurement on a Pi 5 (Hermann-SW gist); 60 fps at 1456 x 1088"),
    "Kron Chronos 2.1-HD": dict(px=10.0, roi=(640, 96), fps=24046, src="Kron product page: 640 x 96 at 24,046 fps; 1920 x 1080 at 1,000 fps"),
    "Mikrotron EoSens 3CL (NIST AMMT's)": dict(px=8.0, roi=(120, 120), fps=10000, src="Lane & Yeung 2020, Table 1"),
}
coax["cameras_at_8um_per_px"] = {}
for k, c in cams.items():
    m = c["px"] / 8.0
    f2 = F1 * m
    coax["cameras_at_8um_per_px"][k] = dict(magnification=round(m, 3), tube_lens_f_mm=round(f2, 0),
                                            field_mm=[round(c["roi"][0] * 8e-3, 2), round(c["roi"][1] * 8e-3, 2)], fps=c["fps"],
                                            sensor_refocus_mm=round(m ** 2 * df_1070_850, 2), source=c["src"])
R["coaxial_camera"] = coax

# ---------------------------------------------------------------- 2. off-axis cameras at the ports monitoring_views.py found
def offaxis(label, wd_mm, elev_deg, f_mm, px_um, n_px, f_number, lam_um=0.81):
    m = f_mm / (wd_mm - f_mm)                # thin lens, object distance ~ working distance from the lens's front principal plane
    obj_px = px_um / m
    pupil = f_mm / f_number
    na = pupil / 2 / wd_mm
    blur_c = 2 * obj_px                      # 2-pixel blur circle on the object
    dof_geo = 2 * blur_c * 1e-3 * wd_mm / pupil          # mm, total
    dof_diff = lam_um * 1e-3 / na ** 2                   # mm
    dof = dof_geo + dof_diff
    tilt = 90.0 - elev_deg                   # angle between the line of sight and the plate normal
    band = dof / math.sin(math.radians(tilt)) if tilt > 1 else float("inf")
    return dict(case=label, wd_mm=wd_mm, elevation_deg=elev_deg, lens_f_mm=f_mm, f_number=f_number, magnification=round(m, 3),
                um_per_px_across=round(obj_px, 1), um_per_px_along_view=round(obj_px / math.sin(math.radians(elev_deg)), 1),
                field_mm_across=round(n_px[0] * obj_px * 1e-3, 1), field_mm_along_view=round(n_px[1] * obj_px * 1e-3 / math.sin(math.radians(elev_deg)), 1),
                rayleigh_um=round(0.61 * lam_um / na, 1), depth_of_field_mm=round(dof, 2), in_focus_band_on_plate_mm=round(band, 2))


R["off_axis"] = [
    offaxis("left wall (-156, -20, 40), Chronos 2.1-HD, 50 mm lens, full frame", 195.0, 14.2, 50.0, 10.0, (1920, 1080), 4.0),
    offaxis("left wall, Chronos 2.1-HD, 50 mm lens, 640 x 96 at 24 kfps", 195.0, 14.2, 50.0, 10.0, (640, 96), 4.0),
    offaxis("left wall, Chronos 2.1-HD, 75 mm lens at f/4, 640 x 96 at 24 kfps", 195.0, 14.2, 75.0, 10.0, (640, 96), 4.0),
    offaxis("left wall, Pi GS (IMX296), 50 mm C-mount lens, 128 x 96 at ~536 fps", 195.0, 14.2, 50.0, 3.45, (128, 96), 4.0),
    offaxis("lid (-60, -80, 136) through a bridge cut-out, Pi GS, 50 mm lens, full frame", 215.0, 53.6, 50.0, 3.45, (1456, 1088), 5.6),
    offaxis("for comparison: Infinity K2 DistaMax + CF-1 at 215 mm (1.28x), Chronos: does not fit (0.5 m long)", 215.0, 53.6, 215.0 * 1.28 / 2.28, 10.0, (640, 96), 5.0),
]
# the K2 row: thin-lens f chosen so m = 1.28 at 215 mm; its NA is the vendor's 0.088, so recompute those two fields
k2 = R["off_axis"][-1]
k2["magnification"] = 1.28
k2["um_per_px_across"] = round(10.0 / 1.28, 1)
k2["rayleigh_um"] = round(0.61 * 0.81 / 0.088, 1)
k2["depth_of_field_mm"] = round(0.81e-3 / 0.088 ** 2 + 2 * 2 * 7.8e-3 / (2 * 0.088), 2)
k2["in_focus_band_on_plate_mm"] = round(k2["depth_of_field_mm"] / math.sin(math.radians(90 - 53.6)), 2)

# ---------------------------------------------------------------- 3. layer camera through the existing lid port (33° off vertical)
WD_LAYER = 205.0   # lens to plate centre: 161.7 mm to the lid face + ~43 mm to the lens front (layer_camera.py)
layer = []
for label, f_mm, px, npx, fno in [("as drawn: Pi HQ (IMX477) + 12 mm, f/4", 12.0, 1.55, (4056, 3040), 4.0),
                                   ("20 MP 1 in. sensor (2.4 µm) + 25 mm, f/2.8", 25.0, 2.4, (5472, 3648), 2.8),
                                   ("20 MP 1 in. sensor (2.4 µm) + 50 mm, f/2.8", 50.0, 2.4, (5472, 3648), 2.8)]:
    m = f_mm / (WD_LAYER - f_mm)
    pupil = f_mm / fno
    na = pupil / 2 / WD_LAYER
    layer.append(dict(case=label, um_per_px=round(px / m, 1), field_mm=[round(npx[0] * px / m * 1e-3, 0), round(npx[1] * px / m * 1e-3, 0)],
                      pupil_mm=round(pupil, 1), rayleigh_um_550nm=round(0.61 * 0.55 / na, 1),
                      fits_window_aperture=pupil <= 20.0))
R["layer_camera"] = layer

# ---------------------------------------------------------------- 4. what a thermal sensor can see on aluminium
eps_list = (0.1, 0.2, 0.35)
R["si_band_camera_floor"] = {f"{fl} °C apparent at 0.80 µm": {f"eps {e}": round(true_from_apparent(fl, 0.80, e), 0) for e in eps_list}
                             for fl in (575, 625, 750)}
# signal from solid metal at 600 °C relative to a 1,800 K melt pool, per band
R["dynamic_range_melt_pool_vs_600C"] = {f"{lam} µm": round(planck(lam, 1800.0) / planck(lam, 873.15), 0) for lam in (0.70, 0.90, 1.55, 4.0)}
R["al_solidification_range_C"] = {"6061": [582, 652], "7075": [477, 635], "AlSi10Mg": [557, 596]}

# ---------------------------------------------------------------- 5. data rates, per hour of lasing
streams = {
    "scan commands, XYPT-style (x, y as int32; power, trigger as int16) at 100 kHz": 100e3 * 12,
    "two coaxial photodiodes, 16-bit, 200 kS/s each": 2 * 200e3 * 2,
    "acoustic emission, 1 channel, 16-bit, 2 MS/s (continuous)": 2e6 * 2,
    "coaxial camera, Pi GS 128 x 96, 10-bit packed, 536 fps": 128 * 96 * 1.25 * 536,
    "coaxial camera, 120 x 120, 8-bit, 10 kHz (NIST AMMT)": 120 * 120 * 10e3,
    "off-axis Chronos 2.1-HD 640 x 96, 12-bit, 24 kfps (into its RAM: 32 GB lasts 14 s)": 640 * 96 * 1.5 * 24046,
    "layer camera video, 2028 x 1520, H.264 ~15 Mbit/s": 15e6 / 8,
}
R["data_rate_GB_per_hour_of_lasing"] = {k: round(v * 3600 / 1e9, 1) for k, v in streams.items()}
R["layer_images_GB_per_500_layers"] = {
    "Pi HQ 12.3 MP, 12-bit raw (~18.5 MB), 2 lights x before/after = 4 per layer": round(4 * 500 * 4056 * 3040 * 1.5 / 1e9, 1),
    "20 MP, 12-bit raw (~30 MB), 4 per layer": round(4 * 500 * 5472 * 3648 * 1.5 / 1e9, 1),
}
chronos_ram_s = 32e9 / (640 * 96 * 1.5 * 24046)
R["chronos_32GB_record_s_at_640x96_24kfps"] = round(chronos_ram_s, 0)


def md():
    L = ["# In-situ monitoring: optics and data numbers (generated by analysis/optics/monitoring_optics.py)", ""]
    c = R["coaxial_camera"]
    L += ["## Coaxial camera through the f-theta and galvo", "",
          f"- Return pupil {c['pupil_mm']} mm (the Ø1 in. dichroic at 45°), NA {c['NA']}: Rayleigh {c['rayleigh_um']} µm at 850 nm.",
          f"- 850 nm focuses {c['focal_shift_1070_to_850_mm']} mm off the 1070 nm focus (fused-silica singlet estimate): refocus the camera, not the lens.",
          f"- An 850 ± 20 nm band spreads focus over {c['band_850pm20_focal_spread_mm']} mm: {c['band_blur_um_full_NA']} µm blur at full NA, "
          f"{c['band_blur_um_at_NA_0p03']} µm stopped to NA 0.03. A ±5 nm filter cuts it four-fold.",
          f"- Lateral colour moves the 850 nm view off the 1070 nm spot by ~{c['lateral_colour_at_M50_edge_um']:.0f} µm at the M50 edge and "
          f"~{c['lateral_colour_at_L75_edge_um']:.0f} µm at the L75 edge: map the spot's position in the frame against galvo angle.", "",
          "| camera | magnification | tube lens f (mm) | field at 8 µm/px (mm) | frame rate | sensor refocus (mm) |", "|---|---:|---:|---|---:|---:|"]
    for k, v in c["cameras_at_8um_per_px"].items():
        L.append(f"| {k} | {v['magnification']} | {v['tube_lens_f_mm']:.0f} | {v['field_mm'][0]} × {v['field_mm'][1]} | {v['fps']:,} | {v['sensor_refocus_mm']} |")
    L += ["", "## Off-axis cameras", "",
          "| case | µm/px across / along the view | field across × along (mm) | Rayleigh (µm) | depth of field (mm) | in-focus band on the plate (mm) |",
          "|---|---|---|---:|---:|---:|"]
    for o in R["off_axis"]:
        L.append(f"| {o['case']} | {o['um_per_px_across']} / {o['um_per_px_along_view']} | {o['field_mm_across']} × {o['field_mm_along_view']} | "
                 f"{o['rayleigh_um']} | {o['depth_of_field_mm']} | {o['in_focus_band_on_plate_mm']} |")
    L += ["", "## Layer camera through the existing lid port", "", "| case | µm/px | field (mm) | pupil (mm) | Rayleigh at 550 nm (µm) | pupil ≤ Ø20 window |",
          "|---|---:|---|---:|---:|---|"]
    for o in R["layer_camera"]:
        L.append(f"| {o['case']} | {o['um_per_px']} | {o['field_mm'][0]:.0f} × {o['field_mm'][1]:.0f} | {o['pupil_mm']} | {o['rayleigh_um_550nm']} | {'yes' if o['fits_window_aperture'] else 'no'} |")
    L += ["", "## Thermal sensing on aluminium", "",
          "Lowest true temperature a 0.80 µm camera (Optris PI 08M band) can show, from its apparent-temperature floor:", "",
          "| apparent floor | " + " | ".join(f"ε = {e}" for e in eps_list) + " |", "|---|" + "---:|" * len(eps_list)]
    for k, v in R["si_band_camera_floor"].items():
        L.append(f"| {k} | " + " | ".join(f"{t:.0f} °C" for t in v.values()) + " |")
    L += ["", "Signal from a 1,800 K melt pool over solid metal at 600 °C, per band (the dynamic range one detector must span):", ""]
    L += [f"- {k}: {v:,.0f}×" for k, v in R["dynamic_range_melt_pool_vs_600C"].items()]
    L += ["", "Solidification ranges (solidus, liquidus, °C): " + "; ".join(f"{k} {v[0]}–{v[1]}" for k, v in R["al_solidification_range_C"].items()), "",
          "## Data rates", "", "| stream | GB per hour of lasing |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in R["data_rate_GB_per_hour_of_lasing"].items()]
    L += ["", "| layer images | GB per 500 layers |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in R["layer_images_GB_per_500_layers"].items()]
    L += ["", f"A 32 GB Chronos 2.1-HD records {R['chronos_32GB_record_s_at_640x96_24kfps']:.0f} s at 640 × 96 and 24 kfps."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    (OUT / "optics.json").write_text(json.dumps(R, indent=1) + "\n")
    (OUT / "optics.md").write_text(md())
    print(md())
