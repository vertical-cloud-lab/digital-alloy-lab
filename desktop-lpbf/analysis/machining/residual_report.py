"""Sort the chamber body's residual stock (cam_sim.py) into causes: pocket corners, floor coves, the band along the walls
that the holder keeps the tool out of, and small blind features (holes on inside faces).

Run after cam_sim.py:  /tmp/venv/bin/python desktop-lpbf/analysis/machining/residual_report.py
Writes desktop-lpbf/analysis/out/machining/residual_chamber.json.
"""
import json
import pathlib

import numpy as np
from scipy import ndimage

OUT = pathlib.Path(__file__).resolve().parents[3] / "desktop-lpbf" / "analysis" / "out" / "machining"
IX, IY, IZ = 140.0, 95.0, 120.0      # pocket half-widths and depth (lpbf_low.P)


def main():
    rep = {}
    for label in ("std", "std_long"):
        d = np.load(f"/tmp/mach-work/cam/res_process_chamber_body_{label}.npz")
        res, lo, p = d["res"], d["lo"], float(d["pitch"])
        idx = np.argwhere(res)
        xyz = lo + p * (idx + 0.5)
        x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
        inside = (np.abs(x) < IX + 0.5) & (np.abs(y) < IY + 0.5) & (z > -0.5) & (z < IZ + 0.5)
        dxw, dyw = IX - np.abs(x), IY - np.abs(y)
        corner = inside & (dxw < 12) & (dyw < 12)
        cove = inside & ~corner & (z < 6.0) & ((dxw < 6) | (dyw < 6))
        band = inside & ~corner & ~cove & ((dxw < 25) | (dyw < 25))
        other = ~(corner | cove | band)
        v = p ** 3
        cats = dict(pocket_corners=corner, floor_coves=cove, wall_band=band, other=other)
        out = {k: round(float(m.sum() * v), 0) for k, m in cats.items()}
        if band.any():
            out["wall_band_z_range"] = [round(float(z[band].min()), 1), round(float(z[band].max()), 1)]
            out["wall_band_max_thickness_mm"] = round(float(np.max(25 - np.minimum(dxw[band], dyw[band]))) - 0.0, 1)
        if corner.any():
            out["corner_z_range"] = [round(float(z[corner].min()), 1), round(float(z[corner].max()), 1)]
        # 'other' clusters with their centres
        om = np.zeros_like(res)
        oi = idx[other]
        om[tuple(oi.T)] = True
        lab, n = ndimage.label(om, structure=np.ones((3, 3, 3)))
        cl = []
        for i, s in enumerate(ndimage.find_objects(lab)):
            m = lab[s] == i + 1
            vol = float(m.sum() * v)
            if vol < 5:
                continue
            c = [round(float(lo[a] + p * (s[a].start + s[a].stop) / 2), 1) for a in range(3)]
            cl.append(dict(volume_mm3=round(vol, 1), centre=c, size=[round(p * (s[a].stop - s[a].start), 1) for a in range(3)]))
        out["other_clusters"] = sorted(cl, key=lambda r: -r["volume_mm3"])[:12]
        rep[label] = out
        print(label, {k: v for k, v in out.items() if k != "other_clusters"})
        for c in out["other_clusters"]:
            print("   ", c)
    (OUT / "residual_chamber.json").write_text(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
