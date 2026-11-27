#!/usr/bin/env python3
"""Cross-check sem_psd.py's watershed segmentation against a pretrained Cellpose model on one field.

    python cellpose_crosscheck.py IMAGE.tif OUT_DIR [--diameter-um 47] [--model cyto3]

Cellpose (generalist cyto3 model, no fine-tuning) segments the same databar-cropped image. Masks are
matched to sem_psd's by intersection over union (IoU >= 0.5); the script reports the match rate both
ways, the ECD agreement of matched particles, and number-weighted D10/D50/D90 from each method (simple
counts of particles not touching the frame, no edge weights, so the two are compared like for like).
Cellpose has no published benchmark on metal-powder SEM images, so this is a consistency check, not a
reference. Requires cellpose 3.x and torch.
"""

import argparse
import importlib.util
import json
import math
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sem_psd", HERE / "sem_psd.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


def ecd_table(labels, px_um, delta_px=0.0):
    from skimage import measure
    out = {}
    ny, nx = labels.shape
    for p in measure.regionprops(labels):
        y0, x0, y1, x1 = p.bbox
        edge = y0 == 0 or x0 == 0 or y1 == ny or x1 == nx
        out[p.label] = (max(2 * math.sqrt(p.area / math.pi) - 2 * delta_px, 0.5) * px_um, edge, p.area)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--diameter-um", type=float, default=47.0, help="typical particle diameter for Cellpose")
    ap.add_argument("--model", default="cyto3")
    ap.add_argument("--min-px", type=float, default=10.0)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    f = sp.read_field(args.image)
    px = f["px_um"]
    lab_ws, info = sp.segment(f["img"])
    delta, _ = sp.edge_offset(info["res"], lab_ws, info["threshold_above_bg"])

    from cellpose import models
    t0 = time.time()
    model = models.Cellpose(gpu=False, model_type=args.model)
    img8 = np.clip(f["img"], 0, 255).astype(np.uint8)
    masks, _, _, _ = model.eval(img8, diameter=args.diameter_um / px, channels=[0, 0])
    t_cp = time.time() - t0

    ws, cp = ecd_table(lab_ws, px, delta), ecd_table(masks, px)
    # IoU matching through the joint histogram of label pairs
    a, b = lab_ws.ravel().astype(np.int64), masks.ravel().astype(np.int64)
    m = (a > 0) & (b > 0)
    pair, inter = np.unique(a[m] * (int(b.max()) + 1) + b[m], return_counts=True)
    pa, pb = pair // (int(b.max()) + 1), pair % (int(b.max()) + 1)
    area_a = np.bincount(a, minlength=int(a.max()) + 1)
    area_b = np.bincount(b, minlength=int(b.max()) + 1)
    iou = inter / (area_a[pa] + area_b[pb] - inter)
    ok = iou >= 0.5
    matched = [(int(x), int(y), float(z)) for x, y, z in zip(pa[ok], pb[ok], iou[ok])]

    def keep(t):
        return {k: v for k, v in t.items() if not v[1] and v[0] >= args.min_px * px}

    ws_k, cp_k = keep(ws), keep(cp)
    mk = [(x, y, z) for x, y, z in matched if x in ws_k and y in cp_k]
    d_ws = np.array([ws_k[x][0] for x, _, _ in mk])
    d_cp = np.array([cp_k[y][0] for _, y, _ in mk])
    rel = d_cp / d_ws - 1

    def dq(t):
        d = np.array([v[0] for v in t.values()])
        return [float(v) for v in np.percentile(d, [10, 50, 90])]

    res = {
        "image": args.image.name, "px_um": px, "cellpose_model": args.model,
        "cellpose_diameter_px": args.diameter_um / px, "cellpose_seconds": round(t_cp, 1),
        "n_watershed": len(ws_k), "n_cellpose": len(cp_k), "n_matched_iou50": len(mk),
        "watershed_matched_frac": len(mk) / max(len(ws_k), 1), "cellpose_matched_frac": len(mk) / max(len(cp_k), 1),
        "median_iou": float(np.median([z for _, _, z in mk])) if mk else None,
        "ecd_rel_diff_cellpose_vs_watershed_median": float(np.median(rel)) if len(rel) else None,
        "ecd_rel_diff_iqr": [float(np.percentile(rel, 25)), float(np.percentile(rel, 75))] if len(rel) else None,
        "number_D10_D50_D90_watershed": dq(ws_k), "number_D10_D50_D90_cellpose": dq(cp_k),
    }
    (args.out_dir / "cellpose_crosscheck.json").write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res, indent=2))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from skimage import segmentation
    h, w = lab_ws.shape
    y0, x0 = h // 2 - 350, w // 2 - 500
    crop = np.clip(f["img"][y0:y0 + 700, x0:x0 + 1000], 0, 255)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
    for ax, lab, nm in ((axes[0], lab_ws, "sem_psd watershed"), (axes[1], masks, f"Cellpose {args.model} (pretrained)")):
        rgb = np.stack([crop / 255] * 3, -1)
        bnd = segmentation.find_boundaries(lab[y0:y0 + 700, x0:x0 + 1000], mode="inner")
        rgb[bnd] = [0, 0.8, 1.0]
        ax.imshow(rgb)
        ax.set_title(nm, loc="left", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(args.out_dir / "cellpose_crosscheck.png", dpi=130)


if __name__ == "__main__":
    main()
