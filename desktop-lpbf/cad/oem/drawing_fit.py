"""Orthographic silhouette check of a builder against the vendor's dimension drawing (issue #260, round 6, 2026-11-25).

    python desktop-lpbf/cad/oem/drawing_fit.py <drawing.pdf>      # default: /tmp/oem/vendor/nxds_shopify/nXDS-6i_10i_15i_20i.pdf

The Edwards nXDS has no public CAD, but its dimension drawing shows the pump in six orthographic views (Provac's nXDS
6i/10i/15i/20i sheet, page 3; URL and sha256 in cad/vendor-cad-manifest.csv). For each view this script:
1. renders the page at 300 dpi and crops the view to the part's own outline (crop boxes below, in PDF points, picked so
   no dimension line closes a loop with the outline);
2. segments the part: dark line pixels, closed 5 px, background flood-filled from the crop border, opened 7 px to drop
   the extension lines, largest component kept;
3. projects the tessellated builder orthographically in the same view direction, fills it triangle by triangle, and fits
   scale and offset to maximise the IoU (Nelder-Mead from the bounding-box match). The top row is drawn at 432 mm =
   545 px at 110 dpi (3.441 px/mm at 300 dpi), so its fitted scale is a check on the model's size; the bottom row is
   drawn smaller and its scale is fitted;
4. reports the IoU, the symmetric outline distance (mean and P95, in mm at the fitted scale) and, for comparison, the same
   for the envelope the builder replaces (at the same scale, offset fitted).
Outputs: analysis/out/oem/drawing_fit.json and drawing_fit_<view>.png (outlines only: no vendor pixels).
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import cv2
import numpy as np
from scipy.optimize import minimize

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parent
OUT = CAD.parent / "analysis" / "out" / "oem"
sys.path.insert(0, str(CAD))
import vendor_parts as VP  # noqa: E402

DPI = 300
PT = DPI / 72.0
S_TOP = 590.8 / 432.0                        # px/mm of the top row at 300 dpi: the side view's 432 dimension spans 590.8 px
# view -> (crop box in PDF points (x0, y0, x1, y1), screen-right axis, screen-up axis, nominal px/mm or None = fitted)
VIEWS = {
    "front (fan end)": ((82.0, 236.0, 183.0, 343.0), (0, 1, 0), (0, 0, 1), S_TOP),
    "side (exhaust side)": ((233.0, 236.0, 378.0, 343.0), (1, 0, 0), (0, 0, 1), S_TOP),
    "side (back)": ((404.0, 239.0, 551.0, 343.0), (-1, 0, 0), (0, 0, 1), S_TOP),
    "rear (motor end)": ((54.0, 423.0, 152.0, 525.0), (0, -1, 0), (0, 0, 1), S_TOP),
    "top": ((195.0, 430.0, 338.0, 525.0), (1, 0, 0), (0, 1, 0), S_TOP),
}


def page_image(pdf, page=3):
    import pymupdf
    d = pymupdf.open(pdf)
    pix = d[page - 1].get_pixmap(dpi=DPI)
    im = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
    return cv2.cvtColor(im[:, :, :3], cv2.COLOR_RGB2BGR)


# extension lines that close a loop with the part's outline inside a crop: erased (line pixels set to background) before
# the fill, as PDF-point rectangles. Front view: the 149 dimension's line above the exhaust flange, and the base line that
# runs past the feet to the 285/145 and 160/286/302 dimensions.
ERASE = {"front (fan end)": [(84.5, 236.0, 87.6, 285.0), (82.0, 339.3, 103.0, 343.0), (167.0, 339.3, 183.0, 343.0)]}


def view_mask(im, box, erase=()):
    x0, y0, x1, y1 = (int(round(v * PT)) for v in box)
    crop = im[y0:y1, x0:x1]
    g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    s = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[:, :, 1]
    lines = ((g < 150) & (s < 90)).astype(np.uint8)
    for ex0, ey0, ex1, ey1 in erase:
        lines[max(0, int(ey0 * PT) - y0):max(0, int(ey1 * PT) - y0), max(0, int(ex0 * PT) - x0):max(0, int(ex1 * PT) - x0)] = 0
    lines = cv2.morphologyEx(lines, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    h, w = lines.shape
    pad = np.zeros((h + 2, w + 2), np.uint8)
    pad[1:-1, 1:-1] = lines
    ff = pad.copy()
    cv2.floodFill(ff, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 2)
    obj = (ff[1:-1, 1:-1] != 2).astype(np.uint8)
    obj = cv2.morphologyEx(obj, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(obj)
    if n > 1:
        obj = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    return obj


def mesh(shape, tol=0.4):
    vs, ts = shape.tessellate(tol, 0.5)
    return np.array([(v.x, v.y, v.z) for v in vs]), np.array(ts, np.int64)


def raster(V, T, r, u, s, t, shape):
    P = np.stack([V @ np.asarray(r, float), -(V @ np.asarray(u, float))], axis=1) * s + np.asarray(t, float)
    img = np.zeros(shape, np.uint8)
    pts = np.round(P[T] * 4).astype(np.int32)
    for tri in pts:                     # one triangle per call (a list fill is even-odd and would cancel overlaps)
        cv2.fillConvexPoly(img, tri, 1, lineType=cv2.LINE_8, shift=2)
    return img


def iou(a, b):
    a, b = a.astype(bool), b.astype(bool)
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 0.0


def outline_dist(a, b):
    def edge(m):
        m = m.astype(np.uint8)
        return (m - cv2.erode(m, np.ones((3, 3), np.uint8))).astype(bool)
    ea, eb = edge(a), edge(b)
    da = cv2.distanceTransform((~eb).astype(np.uint8), cv2.DIST_L2, 5)
    db = cv2.distanceTransform((~ea).astype(np.uint8), cv2.DIST_L2, 5)
    return float(0.5 * (da[ea].mean() + db[eb].mean())), float(max(np.percentile(da[ea], 95), np.percentile(db[eb], 95)))


def fit(V, T, r, u, mask, s0, fit_scale=True):
    ys, xs = np.nonzero(mask)
    pr = np.stack([V @ np.asarray(r, float), -(V @ np.asarray(u, float))], axis=1)
    if s0 is None:                       # scale from the bounding boxes
        s0 = 0.5 * ((np.ptp(xs) + 1) / np.ptp(pr[:, 0]) + (np.ptp(ys) + 1) / np.ptp(pr[:, 1]))
    c_img = np.array([(xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0])
    c_mod = np.array([(pr[:, 0].min() + pr[:, 0].max()) / 2.0, (pr[:, 1].min() + pr[:, 1].max()) / 2.0])
    t0 = c_img - s0 * c_mod

    def unpack(q):
        return (s0 * math.exp(q[2]) if fit_scale else s0), t0 + q[:2]

    def cost(q):
        s, t = unpack(q)
        return 1.0 - iou(raster(V, T, r, u, s, t, mask.shape), mask)

    q0 = np.zeros(3 if fit_scale else 2)
    simplex = np.vstack([q0] + [q0 + np.eye(len(q0))[i] * (6.0 if i < 2 else 0.03) for i in range(len(q0))])
    res = minimize(cost, q0, method="Nelder-Mead", options=dict(maxiter=260, initial_simplex=simplex, xatol=0.05, fatol=1e-5))
    s, t = unpack(res.x)
    sil = raster(V, T, r, u, s, t, mask.shape)
    return s, t, sil


def old_envelope():
    """The 'Dry scroll pump (<= 0.3 mbar, 6 m3/h class)' envelope of lpbf_low.py before round 6, in the nXDS6i's local frame
    (the pump is placed at world (557, 150, z_base1) with no rotation)."""
    ox, oy, oz = 557.0, 150.0, -160.0
    g0 = -160.0
    env = VP._fuse([VP._rbox(560 - ox, 980 - ox, 40 - oy, 290 - oy, g0 - oz, g0 + 270 - oz, 10),
                    VP._cyl(16, (640 - ox, 165 - oy, g0 + 270 - oz), (0, 0, 1), 20),
                    VP._cyl(14, (980 - ox, 120 - oy, g0 + 60 - oz), (1, 0, 0), 25)])
    return env


def overlay(mask, sil, title, path):
    h, w = mask.shape
    can = np.full((h + 40, w, 3), 255, np.uint8)
    po, mo = mask.astype(bool), sil.astype(bool)
    sub = can[40:]
    sub[po & ~mo] = (190, 215, 250)
    sub[mo & ~po] = (250, 225, 190)
    sub[po & mo] = (235, 235, 235)
    for m, col in ((po, (0, 110, 230)), (mo, (200, 80, 0))):
        cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(sub, cs, -1, col, 2)
    for i, line in enumerate(title):
        cv2.putText(can, line, (6, 16 + 16 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (40, 40, 40), 1, cv2.LINE_AA)
    return can


def main(pdf):
    im = page_image(pdf)
    new = VP.edwards_nxds6i()
    Vn, Tn = mesh(new)
    Vo, To = mesh(old_envelope())
    res, tiles = {}, []
    for name, (box, r, u, snom) in VIEWS.items():
        mask = view_mask(im, box, ERASE.get(name, ()))
        # headline: at the drawing's own scale, offset fitted (the model's size is then tested too); the free-scale fit is a check
        s, t, sil = fit(Vn, Tn, r, u, mask, snom, fit_scale=False)
        md, p95 = outline_dist(sil, mask)
        sf, tf, silf = fit(Vn, Tn, r, u, mask, snom, fit_scale=True)
        row = dict(crop_pt=list(box), mask_px=int(mask.sum()), iou=round(iou(sil, mask), 4), scale_px_per_mm=round(s, 4),
                   outline_mean_mm=round(md / s, 2), outline_p95_mm=round(p95 / s, 2),
                   iou_free_scale=round(iou(silf, mask), 4), free_scale_vs_drawing=round(sf / s, 4))
        so, to, silo = fit(Vo, To, r, u, mask, s, fit_scale=False)
        mdo, p95o = outline_dist(silo, mask)
        row.update(before_iou=round(iou(silo, mask), 4), before_outline_mean_mm=round(mdo / s, 2), before_outline_p95_mm=round(p95o / s, 2))
        res[name] = row
        print(name, json.dumps(row), flush=True)
        tiles.append(overlay(mask, sil, [f"{name}: IoU {row['iou']:.3f} (before {row['before_iou']:.3f})",
                                         f"outline mean {row['outline_mean_mm']:.1f} mm; orange = drawing, blue = model"], None))
    OUT.mkdir(parents=True, exist_ok=True)
    hmax = max(t_.shape[0] for t_ in tiles)
    row1 = [cv2.copyMakeBorder(t_, 0, hmax - t_.shape[0], 0, 8, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t_ in tiles[:3]]
    row2 = [cv2.copyMakeBorder(t_, 0, hmax - t_.shape[0], 0, 8, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t_ in tiles[3:]]
    w1, w2 = sum(t_.shape[1] for t_ in row1), sum(t_.shape[1] for t_ in row2)
    W = max(w1, w2)
    grid = np.vstack([cv2.copyMakeBorder(np.hstack(row1), 0, 0, 0, W - w1, cv2.BORDER_CONSTANT, value=(255, 255, 255)),
                      cv2.copyMakeBorder(np.hstack(row2), 0, 0, 0, W - w2, cv2.BORDER_CONSTANT, value=(255, 255, 255))])
    sc = min(1.0, 1600.0 / grid.shape[1])
    grid = cv2.resize(grid, (int(grid.shape[1] * sc), int(grid.shape[0] * sc)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(OUT / "drawing_fit_edwards_nxds6i.png"), grid, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    summary = dict(builder="edwards_nxds6i", drawing=str(pdf).split("/")[-1], page=3, dpi=DPI, top_row_px_per_mm=round(S_TOP, 4),
                   views=res, mean_iou=round(float(np.mean([v["iou"] for v in res.values()])), 4),
                   mean_before_iou=round(float(np.mean([v["before_iou"] for v in res.values()])), 4))
    p = OUT / "drawing_fit.json"
    allres = json.loads(p.read_text()) if p.exists() else {}
    allres["edwards_nxds6i"] = summary
    p.write_text(json.dumps(allres, indent=1))
    print("mean IoU", summary["mean_iou"], "before", summary["mean_before_iou"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/oem/vendor/nxds_shopify/nXDS-6i_10i_15i_20i.pdf")
