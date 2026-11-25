"""Can the oblique monitoring ports be cut in the frame's setup C and the lid's setups, and what does a window that is not
square to the sight line cost optically? (issue #260, PR 281)

For each port of cad/monitoring_spec.py (read at run time):
  * how the sight line sits against the host face: angle to the face normal, and its split into a turn the 4th axis can
    take out and the tilt it can't (frame: A along the frame's z, so the azimuth about z is free and the elevation is
    not; lid: A along the lid's x, so the turn about x is free and the turn about y is not);
  * the round bore normal to the face that still passes the clear aperture across the wall (or lid): the "perpendicular
    port", cut at the existing index;
  * the depth difference across a window seat cut square to the sight line in the host face (if it exceeds the wall, a
    seat on the line of sight needs a boss or adapter, as the layer camera has);
  * the optics of a flat window left square to the face, i.e. tilted to the sight line by that angle: focus shift,
    astigmatism, sideways shift of the view, and the blur the astigmatism adds at the camera's object-side NA
    (tilted plane-parallel plate: Smith, Modern Optical Engineering, ch. on plane-parallel plates;
    astigmatism = t / sqrt(n^2 - sin^2 u) * (n^2 cos^2 u / (n^2 - sin^2 u) - 1); the blur at best focus is about
    astigmatism x NA). Fused silica n = 1.4525 at 850 nm (Malitson).

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/oblique_ports.py  (writes analysis/out/monitoring/fab/oblique_ports.json)
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import frame_features as FF  # noqa: E402

MS = FF.MS
N_FS = 1.4525
# object-side NA of the cameras planned for each port (monitoring.md §3, monitoring_spec): entrance pupil radius / distance
# from the pupil to the plate centre (sight line length + standoff + ~20 mm to the pupil, ASSUMED)
CAMERAS = {
    "LW": [("Chronos 2.1-HD + 50 mm at f/4", 50 / 4 / 2, 15 + 20), ("Chronos 2.1-HD + 75 mm at f/4", 75 / 4 / 2, 15 + 25),
           ("IMX296 + 50 mm at f/2.8", 50 / 2.8 / 2, 15 + 20)],
    "LP": [("IMX296 + 50 mm at f/2.8", 50 / 2.8 / 2, 15 + 20), ("IMX296 + 50 mm at f/4", 50 / 4 / 2, 15 + 20)],
    "BW": [],
}
PX = {"LW": "29 um/px (Chronos + 50 mm) to 10 um/px (IMX296 + 50 mm) across the view", "LP": "11.4 um/px (IMX296 + 50 mm)"}
HOST = {"LW": dict(normal=(1.0, 0, 0), wall=16.0, axis_free="z (frame setup C: A along the frame's z)"),
        "BW": dict(normal=(0, -1.0, 0), wall=16.0, axis_free="z (frame setup C: A along the frame's z)"),
        "LP": dict(normal=(0, 0, -1.0), wall=16.0, axis_free="x (the lid on the 4th axis along its x, setup_plan.json)")}


def plate(t, u_deg, n=N_FS):
    u = math.radians(u_deg)
    s2 = math.sin(u) ** 2
    root = math.sqrt(n * n - s2)
    ast = t / root * (n * n * math.cos(u) ** 2 / (n * n - s2) - 1.0)
    lateral = t * math.sin(u) * (1 - math.cos(u) / root)
    focus = t * (1 - math.cos(u) / root) / max(math.cos(u), 1e-9)   # sagittal focus shift along the line (approx.)
    return dict(astigmatism_mm=round(abs(ast), 3), lateral_shift_mm=round(lateral, 3), focus_shift_mm=round(focus, 3))


def main():
    out = {}
    for k, s in MS.VIEWPORTS.items():
        c = np.array(s["centre"], float)
        d = np.array(MS.axis_to_target(s["centre"]))
        h = HOST[k]
        nrm = np.array(h["normal"])
        tilt = math.degrees(math.acos(abs(float(d @ nrm))))
        if k in ("LW", "BW"):
            free = math.degrees(math.atan2(abs(d[1] if k == "LW" else d[0]), abs(d[0] if k == "LW" else d[1])))
            fixed = math.degrees(math.asin(abs(d[2])))
            free_what, fixed_what = "azimuth (turn about z)", "elevation (tilt toward the plate)"
            ax = 0 if k == "LW" else 1
            lo, hi = (-156.0, -140.0) if k == "LW" else (95.0, 111.0)
        else:
            free = math.degrees(math.atan2(abs(d[1]), abs(d[2])))           # about the lid's x
            fixed = math.degrees(math.atan2(abs(d[0]), math.hypot(d[1], d[2])))   # what is left, about y
            free_what, fixed_what = "turn about the lid's x", "turn about the lid's y"
            ax = 2
            lo, hi = 120.0, 136.0
        rc = s["clear_d"] / 2
        pts = FF.clear_points(c, d, rc, ax, lo, hi)
        a_lo, a_hi = FF.axis_at(c, d, ax, lo), FF.axis_at(c, d, ax, hi)
        mid = 0.5 * (a_lo + a_hi)
        other = [i for i in range(3) if i != ax]
        rr = np.hypot(pts[:, other[0]] - mid[other[0]], pts[:, other[1]] - mid[other[1]])
        perp_d = 2 * float(rr.max())
        win = s["window"]
        seat_d = win["d"] + 0.2
        seat_depth_var = seat_d * math.tan(math.radians(tilt))
        r = dict(host=("left wall" if k == "LW" else "back wall" if k == "BW" else "lid"), centre=s["centre"],
                 sight_axis=d.round(4).tolist(), angle_to_face_normal_deg=round(tilt, 2),
                 fourth_axis=dict(free_axis=h["axis_free"], takes_out_deg=round(free, 2), takes_out=free_what,
                                  leaves_deg=round(fixed, 2), leaves=fixed_what),
                 perpendicular_bore=dict(d_needed_mm=round(perp_d, 2), clear_d_mm=s["clear_d"], host_thickness_mm=h["wall"],
                                         note="round bore normal to the face that holds the clear cylinder on the sight line "
                                              "across the full thickness"),
                 seat_square_to_sight=dict(seat_d_mm=round(seat_d, 1), depth_difference_across_seat_mm=round(seat_depth_var, 1),
                                           fits_in_host=bool(seat_depth_var + 3.0 < h["wall"]),
                                           note="a window seat cut square to the sight line in the host face: its floor is "
                                                "this much deeper on one side than the other"),
                 window_square_to_face=dict(window=win, **plate(win["t"], tilt)))
        blur = []
        for name, pupil_r, extra in CAMERAS[k]:
            L = float(np.linalg.norm(c)) + extra
            na = pupil_r / L
            b = r["window_square_to_face"]["astigmatism_mm"] * na * 1000
            blur.append(dict(camera=name, object_na=round(na, 4), astigmatism_blur_um=round(b, 1)))
        if k == "LP":   # a thinner window flat on the lid: 2 mm (Robinson's 1.56 mm minimum for a 20 mm fused-silica aperture at 1 bar, F/S 10)
            r["window_square_to_face_2mm"] = plate(2.0, tilt)
            for b in blur:
                b["astigmatism_blur_um_2mm_window"] = round(r["window_square_to_face_2mm"]["astigmatism_mm"] * b["object_na"] * 1000, 1)
        r["blur"] = blur
        r["pixel_scale"] = PX.get(k)
        out[k] = r
    p = FF.OUT / "oblique_ports.json"
    p.write_text(json.dumps(out, indent=1))
    for k, r in out.items():
        print(k, r["angle_to_face_normal_deg"], r["fourth_axis"], r["perpendicular_bore"]["d_needed_mm"],
              r["seat_square_to_sight"], r["window_square_to_face"], r["blur"], r.get("window_square_to_face_2mm"))


if __name__ == "__main__":
    main()
