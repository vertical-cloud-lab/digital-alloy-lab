#!/usr/bin/env python3
"""Compare sem_psd.py sizes with Ronnie's hand measurements burned into four of the k7m2q9 images.

    python validate_hand.py IMAGE_DIR OUT_DIR

The xT software draws each hand measurement as a thin, dark, anti-aliased line across the particle, with
its value as text (gray level 143) parallel to the line. For each value read off the images (table
below: value and the rough text centre in full-resolution pixels), this script

1. finds the text strokes near that centre and their direction u (principal axis);
2. finds the line: a segment parallel to u, as long as the value says, near the text, along which the
   image is darkest relative to a reference. Where the same field was also saved without annotations
   (`annotated` = `not annotated`, `annotated2` = `spherical_004`, same stage position) the reference
   is that plain image; otherwise (`3.2nA_005`, `3.2nA_006`) it is the image's own local mean;
3. takes the particle the segment crosses from sem_psd's segmentation (of the plain twin, or of the
   annotated image with its text inpainted) and reports its ECD, Feret diameters, its caliper width
   along the line, and the free-boundary circle fit, against the hand value;
4. writes hand_validation.csv and a gallery with the found line and the particle contour, which is the
   visual check that each line was found and assigned correctly.
"""

import argparse
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, measure

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sem_psd", HERE / "sem_psd.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

# (annotated image, plain twin or None, value um, approx text centre x, y in full-resolution pixels)
LABELS = [
    ("annotated", "not annotated", 128.2, 836, 300), ("annotated", "not annotated", 142.4, 1530, 280),
    ("annotated", "not annotated", 113.3, 1960, 260), ("annotated", "not annotated", 32.60, 830, 760),
    ("annotated", "not annotated", 58.52, 1170, 860), ("annotated", "not annotated", 45.86, 1824, 820),
    ("annotated", "not annotated", 79.77, 1680, 1010), ("annotated", "not annotated", 29.71, 2410, 960),
    ("annotated", "not annotated", 42.23, 2044, 1210), ("annotated", "not annotated", 29.58, 510, 1140),
    ("annotated", "not annotated", 85.85, 1060, 1410), ("annotated", "not annotated", 151.2, 1384, 1590),
    ("annotated2", "spherical_004", 39.28, 540, 260), ("annotated2", "spherical_004", 37.31, 2310, 114),
    ("annotated2", "spherical_004", 49.75, 1594, 340), ("annotated2", "spherical_004", 84.51, 864, 464),
    ("annotated2", "spherical_004", 113.5, 2710, 590), ("annotated2", "spherical_004", 137.7, 1080, 820),
    ("annotated2", "spherical_004", 40.49, 360, 1000), ("annotated2", "spherical_004", 63.23, 794, 1110),
    ("annotated2", "spherical_004", 176.8, 2030, 1000), ("annotated2", "spherical_004", 75.54, 1180, 1624),
    ("annotated2", "spherical_004", 116.4, 2384, 1584),
    ("3.2nA_006", None, 219.0, 1154, 194), ("3.2nA_006", None, 155.1, 1994, 224),
    ("3.2nA_006", None, 38.54, 514, 560), ("3.2nA_006", None, 53.82, 1104, 704),
    ("3.2nA_006", None, 123.6, 1494, 770), ("3.2nA_006", None, 115.5, 674, 834),
    ("3.2nA_006", None, 129.8, 2054, 924), ("3.2nA_006", None, 109.1, 2414, 1004),
    ("3.2nA_006", None, 68.99, 1474, 1304), ("3.2nA_006", None, 52.71, 834, 1364),
    ("3.2nA_006", None, 25.94, 484, 1530), ("3.2nA_006", None, 161.9, 1804, 1530),
    ("3.2nA_005", None, 219.0, 1194, 280), ("3.2nA_005", None, 155.1, 1890, 214),
    ("3.2nA_005", None, 38.54, 624, 604), ("3.2nA_005", None, 53.82, 1140, 734),
    ("3.2nA_005", None, 123.6, 1494, 790), ("3.2nA_005", None, 115.5, 764, 854),
    ("3.2nA_005", None, 129.8, 2000, 924), ("3.2nA_005", None, 109.1, 2314, 1004),
    ("3.2nA_005", None, 68.99, 1474, 1260), ("3.2nA_005", None, 52.71, 914, 1314),
    ("3.2nA_005", None, 25.94, 604, 1464), ("3.2nA_005", None, 161.9, 1774, 1470),
    ("3.2nA_005", None, 46.19, 1000, 1824), ("3.2nA_005", None, 30.45, 1530, 1920),
]
OVERLAY_GRAY = 143


def text_axis(img, cx, cy, radius=120):
    """Centroid and unit direction (x, y) of the overlay text strokes near (cx, cy)."""
    solid = ndi.binary_opening(np.rint(img) == OVERLAY_GRAY, np.ones((3, 3), bool))
    y0, y1 = max(cy - radius, 0), min(cy + radius, img.shape[0])
    x0, x1 = max(cx - radius, 0), min(cx + radius, img.shape[1])
    yy, xx = np.nonzero(solid[y0:y1, x0:x1])
    keep = np.hypot(yy + y0 - cy, xx + x0 - cx) < radius
    pts = np.stack([xx[keep] + x0, yy[keep] + y0], 1).astype(float)
    c = pts.mean(0)
    w, v = np.linalg.eigh(np.cov((pts - c).T))
    u = v[:, np.argmax(w)]
    return c, u / np.linalg.norm(u), solid


def find_line(signal, c, u, length_px, search_n=90, search_t=70, angles_deg=(-3, -2, -1, 0, 1, 2, 3)):
    """Centre and direction of the segment (given length, within a few degrees of u, near c) along which
    the mean of `signal` (dashed-line energy) is largest."""
    half = length_px / 2
    k = max(int(round(length_px)), 3)
    best = (-np.inf, None, None)
    t = np.arange(-search_t - half, search_t + half + 1, 1.0)
    for da in angles_deg:
        ca, sa = math.cos(math.radians(da)), math.sin(math.radians(da))
        uu = np.array([ca * u[0] - sa * u[1], sa * u[0] + ca * u[1]])
        n = np.array([-uu[1], uu[0]])
        for s in np.arange(-search_n, search_n + 1, 1.0):
            pts = c[None, :] + s * n[None, :] + t[:, None] * uu[None, :]
            prof = ndi.map_coordinates(signal, [pts[:, 1], pts[:, 0]], order=1, mode="nearest")
            run = np.convolve(prof, np.ones(k) / k, mode="valid")
            j = int(np.argmax(run))
            if run[j] > best[0]:
                best = (run[j], c + s * n + (t[j] + half) * uu, uu)
    return best[1], best[0], best[2]


def caliper(mask_coords, u):
    proj = mask_coords @ u
    return proj.max() - proj.min() + 1.0  # +1 px: pixel centres to outer edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows, crops = [], []
    cache = {}
    for ann, twin, value, cx, cy in LABELS:
        if ann not in cache:
            fa = sp.read_field(args.image_dir / f"{ann}.tif")
            # dashed-line energy: |annotated - plain twin|, or the annotated image's own high-pass magnitude
            _, tmask = sp.mask_annotations(fa["img"], OVERLAY_GRAY)
            if twin:
                ft = sp.read_field(args.image_dir / f"{twin}.tif")
                seg_img = ft["img"]
                signal = np.abs(fa["img"] - ft["img"])
            else:
                seg_img, _ = sp.mask_annotations(fa["img"], OVERLAY_GRAY)
                signal = np.abs(fa["img"] - filters.gaussian(fa["img"], sigma=1.5, preserve_range=True))
            signal = signal - ndi.median_filter(signal, size=15)
            signal[ndi.binary_dilation(tmask, iterations=3)] = 0
            labels, info = sp.segment(seg_img)
            delta, _ = sp.edge_offset(info["res"], labels, info["threshold_above_bg"])
            cache[ann] = (fa, seg_img, signal, labels, delta, {p.label: p for p in measure.regionprops(labels)})
        fa, seg_img, signal, labels, delta, props = cache[ann]
        px = fa["px_um"]
        c, u, _ = text_axis(fa["img"], cx, cy)
        L = value / px
        centre, score, u = find_line(signal, c, u, L)
        # particle under the middle half of the segment
        ts = np.linspace(-L / 4, L / 4, 25)
        pts = centre[None, :] + ts[:, None] * u[None, :]
        labs = labels[np.clip(pts[:, 1].round().astype(int), 0, labels.shape[0] - 1),
                      np.clip(pts[:, 0].round().astype(int), 0, labels.shape[1] - 1)]
        labs = labs[labs > 0]
        lab = int(np.bincount(labs).argmax()) if labs.size else 0
        rec = {"image": ann, "segmented_from": twin or f"{ann} (text inpainted)", "px_um": px, "hand_um": value,
               "line_x": round(float(centre[0]), 1), "line_y": round(float(centre[1]), 1),
               "line_angle_deg": round(math.degrees(math.atan2(u[1], u[0])), 1), "line_score": round(float(score), 2),
               "label": lab}
        if lab:
            p = props[lab]
            ecd = (2 * math.sqrt(p.area / math.pi) - 2 * delta) * px
            rim = p.image & ~ndi.binary_erosion(p.image)
            coords = np.argwhere(rim)[:, ::-1].astype(float)  # (x, y)
            fmax, fmin, _ = sp.feret(np.argwhere(rim).astype(float))
            dfit, free = sp.free_boundary_circle(labels, p)
            y0, x0, y1, x1 = p.bbox
            rec.update({"ecd_um": ecd, "feret_max_um": fmax * px, "feret_min_um": fmin * px,
                        "caliper_along_line_um": (caliper(coords, u) - 2 * delta) * px,
                        "circle_fit_um": dfit * px if np.isfinite(dfit) else np.nan,
                        "free_boundary_frac": free, "solidity": p.solidity,
                        "touches_edge": bool(y0 == 0 or x0 == 0 or y1 == labels.shape[0] or x1 == labels.shape[1])})
        rows.append(rec)
        crops.append((fa, seg_img, labels, lab, centre, u, L, value))
        print(f"{ann:10s} {value:7.2f}  line at ({centre[0]:.0f},{centre[1]:.0f}) score {score:6.2f}  "
              f"ECD {rec.get('ecd_um', float('nan')):7.2f}  caliper {rec.get('caliper_along_line_um', float('nan')):7.2f}", flush=True)
    df = pd.DataFrame(rows)
    df.round(3).to_csv(args.out_dir / "hand_validation.csv", index=False)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ncol = 8
    nrow = int(math.ceil(len(crops) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(2.1 * ncol, 2.25 * nrow))
    for ax in axes.ravel():
        ax.axis("off")
    for ax, (fa, img, labels, lab, centre, u, L, value), (_, r) in zip(axes.ravel(), crops, df.iterrows()):
        half = int(max(L * 0.9, 45))
        x, y = int(centre[0]), int(centre[1])
        a, b = max(y - half, 0), min(y + half, img.shape[0])
        c0, d0 = max(x - half, 0), min(x + half, img.shape[1])
        ax.imshow(np.clip(fa["img"][a:b, c0:d0], 0, 255), cmap="gray", vmin=40, vmax=220)
        if lab:
            ax.contour(labels[a:b, c0:d0] == lab, levels=[0.5], colors=["#00c8ff"], linewidths=0.8)
        p0, p1 = centre - u * L / 2, centre + u * L / 2
        ax.plot([p0[0] - c0, p1[0] - c0], [p0[1] - a, p1[1] - a], color="#ff4040", lw=0.8, ls="--")
        ax.set_title(f"{r['image']}: hand {value:g}\nECD {r.get('ecd_um', np.nan):.1f}, caliper "
                     f"{r.get('caliper_along_line_um', np.nan):.1f}", fontsize=6.5)
    fig.suptitle("Hand measurements (red dashed = located line, cyan = sem_psd particle); values in µm",
                 fontsize=10, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(args.out_dir / "hand_validation_gallery.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
