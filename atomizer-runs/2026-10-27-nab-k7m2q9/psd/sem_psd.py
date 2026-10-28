#!/usr/bin/env python3
"""Particle size and shape distribution of a powder from a folder of Thermo Fisher / FEI SEM TIFFs.

Written for the first NAB (C63000) lot, k7m2q9 (issue #225), and meant to run unchanged on later lots:

    python sem_psd.py IMAGE_DIR OUT_DIR [--include 'spherical*' ...] [--exclude 'annotated*' ...]

What it does, field by field and then pooled (see README.md next to this file for the reasoning):

1. Reads the pixel size, frame size, stage position and beam settings from the FEI metadata block
   (TIFF tag 34682). The databar below row `[Image] ResolutionY` is cropped off.
2. Segments: Gaussian denoise (sigma 1 px), a quadratic background surface fitted to carbon-tape pixels,
   a threshold k robust sigmas above it, hole filling, then marker-controlled watershed on the smoothed
   distance transform. Markers are maxima of log(distance) deeper than --h-rel, so the split criterion is
   relative: two touching spheres split, a teardrop or a sphere with a fused satellite does not.
3. Measures every region: projected-area equivalent circle diameter (ECD), Feret max/min, Crofton
   perimeter, ISO 9276-6 circularity, aspect ratio, solidity and convexity, and a circle fitted only to
   the boundary that borders background (a check on occluded spheres). ECD is corrected for the offset
   between the threshold contour and the half-maximum edge, measured in each field from round particles.
4. Registers fields that overlap (stage coordinates, refined by phase correlation), assigns each patch of
   stub to the finest-pixel field that covers it, and counts a particle only in the field whose patch
   holds its centroid, so no particle is counted twice.
5. Excludes particles that touch the frame and corrects for it with Miles-Lantuejoul (Horvitz-Thompson)
   weights, generalised to a union of fields and to field-dependent lower size limits:
   w = A_total / sum_i |R_i ∩ (F_i eroded by the particle's box)|.
6. Reports number- (q0) and volume-weighted (q3, weight w*d^3) D10/D50/D90 with particle- and
   field-level bootstrap 95 % intervals, shares in a size band and below a fines limit, shape statistics,
   per-field results, and figures.

Outputs in OUT_DIR: particles.csv, fields.csv, summary.json, summary.md, figures/*.png.
Requires numpy, scipy, scikit-image, tifffile, pandas, matplotlib, pillow.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import tifffile
from scipy import ndimage as ndi
from scipy.spatial import ConvexHull, QhullError
from skimage import filters, measure, morphology, segmentation, transform
from skimage.registration import phase_cross_correlation

VERSION = "1.0"


# ----------------------------------------------------------------------------------------------------
# Reading
# ----------------------------------------------------------------------------------------------------

def read_field(path: Path) -> dict:
    """Image (databar cropped) and the metadata the analysis needs, from an FEI/TFS TIFF."""
    with tifffile.TiffFile(path) as tif:
        meta = tif.fei_metadata
        raw = tif.pages[0].asarray()
    if not meta:
        raise ValueError(f"{path.name}: no FEI metadata (TIFF tag 34682); pixel size unknown")
    if raw.ndim == 3:
        raw = raw[..., 0]
    scan, image, stage = meta.get("Scan", {}), meta.get("Image", {}), meta.get("Stage", {})
    nx = int(image.get("ResolutionX", raw.shape[1]))
    ny = int(image.get("ResolutionY", raw.shape[0]))
    px_um = float(scan["PixelWidth"]) * 1e6
    py_um = float(scan.get("PixelHeight", scan["PixelWidth"])) * 1e6
    if abs(px_um - py_um) / px_um > 1e-3:
        raise ValueError(f"{path.name}: non-square pixels ({px_um} x {py_um} um)")
    beam, eb, det, user = meta.get("Beam", {}), meta.get("EBeam", {}), meta.get("Detectors", {}), meta.get("User", {})
    return {
        "field": path.stem,
        "file": path.name,
        "img": raw[:ny, :nx].astype(np.float32),
        "nx": nx,
        "ny": ny,
        "px_um": px_um,
        "hfw_um": float(scan.get("HorFieldsize", nx * px_um * 1e-6)) * 1e6,
        "stage_x_um": float(stage.get("StageX", 0.0)) * 1e6,
        "stage_y_um": float(stage.get("StageY", 0.0)) * 1e6,
        "stage_r": float(stage.get("StageR", 0.0)),
        "stage_t": float(stage.get("StageT", 0.0)),
        "scan_rotation": float(beam.get("ScanRotation", eb.get("ScanRotation", 0.0)) or 0.0),
        "hv_kV": float(eb.get("HV", beam.get("HV", 0.0)) or 0.0) / 1e3,
        "current_nA": float(eb.get("BeamCurrent", 0.0) or 0.0) * 1e9,
        "detector": f"{det.get('Name', '')} {det.get('Mode', '')}".strip(),
        "dwell_us": float(scan.get("Dwelltime", 0.0) or 0.0) * 1e6,
        "acquired": f"{user.get('Date', '')} {user.get('Time', '')}".strip(),
    }


def mask_annotations(img: np.ndarray, gray: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Find burned-in xT annotation text (solid strokes of one gray level) and inpaint it.

    Returns the inpainted image and the mask. Only for validation on annotated images; strokes thinner
    than 3 px (the measurement lines themselves) are not removed.
    """
    u8 = np.clip(img, 0, 255).astype(np.uint8)
    if gray is None:
        # the overlay colour is the gray level with the most solid 3x3 blocks
        best, best_n = None, 0
        for g in range(256):
            m = u8 == g
            if m.mean() < 0.002:
                continue
            n = int(morphology.binary_erosion(m, np.ones((3, 3), bool)).sum())
            if n > best_n:
                best, best_n = g, n
        gray = best
    if gray is None:
        return img, np.zeros(img.shape, bool)
    solid = morphology.opening(u8 == gray, np.ones((3, 3), bool))
    mask = morphology.dilation(solid, morphology.disk(2))
    out = img.copy()
    # fill masked pixels from the nearest unmasked pixel, then smooth inside the mask only
    idx = ndi.distance_transform_edt(mask, return_distances=False, return_indices=True)
    out = out[tuple(idx)]
    sm = filters.gaussian(out, sigma=2, preserve_range=True)
    out[mask] = sm[mask]
    return out, mask


# ----------------------------------------------------------------------------------------------------
# Segmentation
# ----------------------------------------------------------------------------------------------------

def background_surface(sm: np.ndarray) -> tuple[np.ndarray, float, dict]:
    """Quadratic background fitted to pixels below the first histogram valley; robust sigma of residual."""
    ny, nx = sm.shape
    hist, _ = np.histogram(sm, bins=256, range=(0, 256))
    hs = ndi.gaussian_filter1d(hist.astype(float), 2)
    mode = int(np.argmax(hs))
    rising = np.nonzero(np.diff(hs[mode:]) > 0)[0]
    valley = mode + (int(rising[0]) if rising.size else 10)
    step = 8
    yy, xx = np.mgrid[0:ny:step, 0:nx:step]
    s = sm[::step, ::step]
    m = s < valley
    u, v = xx[m] / nx, yy[m] / ny
    X = np.stack([np.ones_like(u), u, v, u * u, v * v, u * v], 1)
    coef = np.linalg.lstsq(X, s[m], rcond=None)[0]
    for _ in range(2):  # one or two reweighting passes drop particle pixels that slipped in
        r = s[m] - X @ coef
        mad = np.median(np.abs(r - np.median(r))) * 1.4826
        keep = r < 3 * mad
        coef = np.linalg.lstsq(X[keep], s[m][keep], rcond=None)[0]
    V, U = np.mgrid[0:ny, 0:nx]
    U = U / nx
    V = V / ny
    bg = (coef[0] + coef[1] * U + coef[2] * V + coef[3] * U * U + coef[4] * V * V + coef[5] * U * V).astype(np.float32)
    r = (sm - bg)[::step, ::step][m]
    sigma = float(np.median(np.abs(r - np.median(r))) * 1.4826)
    return bg, sigma, {"bg_mode": mode, "bg_valley": valley, "bg_coef": [round(float(c), 3) for c in coef]}


def segment(img: np.ndarray, k_sigma: float = 5.0, h_rel: float = 0.15, smooth: float = 1.0,
            min_area_px: int = 12) -> tuple[np.ndarray, dict]:
    sm = filters.gaussian(img, sigma=smooth, preserve_range=True)
    bg, sigma, info = background_surface(sm)
    res = sm - bg
    fg = res > k_sigma * sigma
    fg = morphology.remove_small_objects(fg, max_size=min_area_px)
    fg = ndi.binary_fill_holes(fg)
    fg = morphology.opening(fg, morphology.disk(1))
    dist = ndi.distance_transform_edt(fg)
    dsm = filters.gaussian(dist, sigma=1.0, preserve_range=True)
    # relative depth criterion: a maximum survives if it rises h_rel (fractionally) above its saddle
    markers = measure.label(morphology.h_maxima(np.log1p(dsm), math.log1p(h_rel)))
    labels = segmentation.watershed(-dsm, markers, mask=fg)
    # drop specks that are smaller than the minimum area
    sizes = np.bincount(labels.ravel())
    small = np.nonzero(sizes < min_area_px)[0]
    small = small[small > 0]
    if small.size:
        labels[np.isin(labels, small)] = 0
    labels, _, _ = segmentation.relabel_sequential(labels)
    info.update({"sigma_bg": round(sigma, 3), "threshold_above_bg": round(k_sigma * sigma, 2),
                 "foreground_fraction": round(float(fg.mean()), 4)})
    return labels, {"sm": sm, "res": res, "bg": bg, **info}


def edge_offset(res: np.ndarray, labels: np.ndarray, threshold: float) -> tuple[float, int]:
    """Median radial offset (px) of the threshold contour outside the half-maximum edge.

    Uses isolated, round particles: the profile is averaged over angle, the rim peak inside the
    boundary is found, and the half-maximum crossing on the outer flank is located by interpolation.
    """
    offsets = []
    for p in measure.regionprops(labels):
        if not (300 <= p.area <= 60000):
            continue
        per = p.perimeter_crofton if hasattr(p, "perimeter_crofton") else p.perimeter
        if per <= 0 or 4 * math.pi * p.area / per ** 2 < 0.9:
            continue
        y0, x0, y1, x1 = p.bbox
        cy, cx = p.centroid
        R = math.sqrt(p.area / math.pi)
        a, b = int(cy - R - 10), int(cy + R + 11)
        c, d = int(cx - R - 10), int(cx + R + 11)
        if a < 0 or c < 0 or b > res.shape[0] or d > res.shape[1]:
            continue
        lab = labels[a:b, c:d]
        # isolated: nothing else within 6 px of this particle
        near = morphology.dilation(lab == p.label, morphology.disk(6))
        if np.any((lab > 0) & (lab != p.label) & near):
            continue
        yy, xx = np.mgrid[a:b, c:d]
        rr = np.hypot(yy - cy, xx - cx) - R
        vals = res[a:b, c:d]
        bins = np.arange(-8, 6.01, 0.5)
        prof = np.array([vals[(rr >= q - 0.25) & (rr < q + 0.25)].mean() for q in bins])
        inner = bins <= 0
        ipk = int(np.argmax(np.where(inner, prof, -np.inf)))
        peak = prof[ipk]
        base = np.median(prof[bins >= 3])
        half = base + 0.5 * (peak - base)
        if peak - base < 2 * threshold:
            continue
        for j in range(ipk, len(bins) - 1):
            if prof[j] >= half > prof[j + 1]:
                rh = bins[j] + (prof[j] - half) / (prof[j] - prof[j + 1]) * (bins[j + 1] - bins[j])
                offsets.append(-rh)  # threshold radius minus half-max radius
                break
    if len(offsets) < 10:
        return 0.0, len(offsets)
    return float(np.median(offsets)), len(offsets)


# ----------------------------------------------------------------------------------------------------
# Measurement
# ----------------------------------------------------------------------------------------------------

_ANGLES = np.deg2rad(np.arange(0, 180, 1.0))
_DIRS = np.stack([np.cos(_ANGLES), np.sin(_ANGLES)], 1)


def feret(coords: np.ndarray) -> tuple[float, float, float]:
    """Feret max, Feret min and convex-hull perimeter of a pixel set, using pixel corners."""
    corners = np.concatenate([coords + o for o in ((-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5))])
    try:
        hull = ConvexHull(corners)
    except QhullError:
        return 1.0, 1.0, 4.0
    pts = corners[hull.vertices]
    proj = pts @ _DIRS.T
    widths = proj.max(0) - proj.min(0)
    hp = np.roll(pts, -1, 0) - pts
    return float(widths.max()), float(widths.min()), float(np.hypot(hp[:, 0], hp[:, 1]).sum())


def free_boundary_circle(labels: np.ndarray, region, pad: int = 2) -> tuple[float, float]:
    """Circle fitted (Kasa) to the part of a region's boundary that borders background.

    Returns (diameter_px, free_fraction). For a sphere that is touching or partly hidden by a neighbour
    this recovers the full diameter; NaN if less than 40 % of the boundary is free.
    """
    y0, x0, y1, x1 = region.bbox
    a, b = max(y0 - pad, 0), min(y1 + pad, labels.shape[0])
    c, d = max(x0 - pad, 0), min(x1 + pad, labels.shape[1])
    lab = labels[a:b, c:d]
    me = lab == region.label
    edge = me & ~morphology.erosion(me, morphology.disk(1))
    if edge.sum() < 8:
        return float("nan"), 0.0
    bgnb = morphology.dilation(lab == 0, morphology.disk(1))
    free = edge & bgnb
    frac = free.sum() / edge.sum()
    if frac < 0.4 or free.sum() < 8:
        return float("nan"), float(frac)
    yy, xx = np.nonzero(free)
    A = np.stack([xx, yy, np.ones_like(xx)], 1).astype(float)
    bb = (xx.astype(float) ** 2 + yy.astype(float) ** 2)
    sol = np.linalg.lstsq(A, bb, rcond=None)[0]
    cx, cy = sol[0] / 2, sol[1] / 2
    r2 = sol[2] + cx ** 2 + cy ** 2
    if r2 <= 0:
        return float("nan"), float(frac)
    # boundary pixel centres sit ~0.5 px inside the region outline
    return 2 * (math.sqrt(r2) + 0.5), float(frac)


def measure_field(f: dict, labels: np.ndarray, delta_px: float) -> pd.DataFrame:
    px = f["px_um"]
    ny, nx = labels.shape
    rows = []
    for p in measure.regionprops(labels):
        y0, x0, y1, x1 = p.bbox
        area = float(p.area)
        per = float(p.perimeter_crofton)
        im = p.image
        rim = im & ~ndi.binary_erosion(im)
        fmax, fmin, _ = feret(np.argwhere(rim).astype(float))
        # convex perimeter with the same (Crofton) estimator as the perimeter, so convexity <= 1 is not biased
        pconv = float(measure.perimeter_crofton(p.image_convex, 4))
        ecd_raw = 2 * math.sqrt(area / math.pi)
        dfit, free = free_boundary_circle(labels, p)
        rows.append({
            "field": f["field"],
            "label": p.label,
            "px_um": px,
            "cx_px": p.centroid[1],
            "cy_px": p.centroid[0],
            "bbox_w_px": x1 - x0,
            "bbox_h_px": y1 - y0,
            "touches_edge": bool(y0 == 0 or x0 == 0 or y1 == ny or x1 == nx),
            "area_px": area,
            "perimeter_px": per,
            "ecd_raw_um": ecd_raw * px,
            "ecd_um": max(ecd_raw - 2 * delta_px, 0.5) * px,
            "feret_max_um": fmax * px,
            "feret_min_um": fmin * px,
            "circle_fit_um": dfit * px if np.isfinite(dfit) else np.nan,
            "free_boundary_frac": free,
            "circularity": min(2 * math.sqrt(math.pi * area) / per, 1.0) if per > 0 else np.nan,
            "form_factor": min(4 * math.pi * area / per ** 2, 1.0) if per > 0 else np.nan,
            "aspect_ratio": fmin / fmax if fmax > 0 else np.nan,
            "solidity": float(p.solidity),
            "convexity": min(pconv / per, 1.0) if per > 0 else np.nan,
        })
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------------------------
# Field geometry: registration, counting regions, edge-correction weights
# ----------------------------------------------------------------------------------------------------

def field_rect(f: dict) -> tuple[float, float, float, float]:
    w, h = f["nx"] * f["px_um"], f["ny"] * f["px_um"]
    return f["gx0"], f["gy0"], f["gx0"] + w, f["gy0"] + h


def to_global(f: dict, col: np.ndarray, row: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return f["gx0"] + col * f["px_um"], f["gy0"] + row * f["px_um"]


def overlap(r1, r2) -> float:
    w = min(r1[2], r2[2]) - max(r1[0], r2[0])
    h = min(r1[3], r2[3]) - max(r1[1], r2[1])
    return max(w, 0) * max(h, 0)


def place_fields(fields: list[dict], sx: int, sy: int) -> None:
    """Global frame in um, x right and y down in image orientation, from stage position and signs."""
    for f in fields:
        w, h = f["nx"] * f["px_um"], f["ny"] * f["px_um"]
        f["gx0"] = sx * f["stage_x_um"] - w / 2
        f["gy0"] = sy * f["stage_y_um"] - h / 2


def pair_shift(fa: dict, fb: dict, common_px: float) -> tuple[float, float, float] | None:
    """Residual (dx, dy) in um that best aligns fb onto fa in their predicted overlap, and a quality."""
    ra, rb = field_rect(fa), field_rect(fb)
    x0, y0 = max(ra[0], rb[0]), max(ra[1], rb[1])
    x1, y1 = min(ra[2], rb[2]), min(ra[3], rb[3])
    margin = 60.0  # um of slack so a few-pixel stage error is still inside the crop
    if (x1 - x0) < 4 * margin or (y1 - y0) < 4 * margin:
        return None

    def crop(f, ax0, ay0, ax1, ay1):
        sc = f["px_um"] / common_px
        key = round(common_px, 6)
        cache = f.setdefault("_rescaled", {})
        if key not in cache:
            cache[key] = transform.rescale(f["img"], sc, anti_aliasing=sc < 1, preserve_range=True) if abs(sc - 1) > 1e-3 else f["img"]
        im = cache[key]
        c0 = int(round((ax0 - f["gx0"]) / common_px)); r0 = int(round((ay0 - f["gy0"]) / common_px))
        c1 = int(round((ax1 - f["gx0"]) / common_px)); r1 = int(round((ay1 - f["gy0"]) / common_px))
        return im[max(r0, 0):r1, max(c0, 0):c1]

    a = crop(fa, x0 + margin, y0 + margin, x1 - margin, y1 - margin)
    b = crop(fb, x0 + margin, y0 + margin, x1 - margin, y1 - margin)
    n0, n1 = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
    if n0 < 64 or n1 < 64:
        return None
    a, b = a[:n0, :n1], b[:n0, :n1]
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    shift, _, _ = phase_cross_correlation(a, b, upsample_factor=4, normalization=None)
    sb = ndi.shift(b, shift, order=1, mode="nearest")
    m = int(max(abs(shift[0]), abs(shift[1]))) + 2
    if n0 - 2 * m < 32 or n1 - 2 * m < 32:
        return None
    ncc = float(np.corrcoef(a[m:-m, m:-m].ravel(), sb[m:-m, m:-m].ravel())[0, 1])
    # shifting b by `shift` reproduces a, so a feature at a-pixel y sits at b-pixel y - shift: b's origin
    # (placed at the same predicted global position as a's crop) is off by +shift
    return shift[1] * common_px, shift[0] * common_px, ncc


def register_fields(fields: list[dict], log) -> list[dict]:
    """Pick stage-axis signs and refine overlapping fields by phase correlation. Returns pair records."""
    best = None
    pairs_all = [(i, j) for i in range(len(fields)) for j in range(i + 1, len(fields))]
    for sx in (1, -1):
        for sy in (1, -1):
            place_fields(fields, sx, sy)
            scores = []
            for i, j in pairs_all:
                if overlap(field_rect(fields[i]), field_rect(fields[j])) <= 0:
                    continue
                cp = max(fields[i]["px_um"], fields[j]["px_um"]) * 2
                r = pair_shift(fields[i], fields[j], cp)
                if r is not None:
                    scores.append(r[2] - 0.002 * math.hypot(r[0], r[1]))
            score = float(np.mean(scores)) if scores else -1
            log(f"  stage sign test sx={sx:+d} sy={sy:+d}: {len(scores)} overlapping pairs, score {score:.3f}")
            if best is None or score > best[0]:
                best = (score, sx, sy)
    _, sx, sy = best
    place_fields(fields, sx, sy)
    records = []
    # refine: fields in acquisition-independent priority order, each aligned to already-placed neighbours
    order = sorted(range(len(fields)), key=lambda k: (fields[k]["px_um"], fields[k]["field"]))
    placed = [order[0]]
    for k in order[1:]:
        shifts = []
        for i in placed:
            if overlap(field_rect(fields[i]), field_rect(fields[k])) <= 0:
                continue
            cp = max(fields[i]["px_um"], fields[k]["px_um"])
            r = pair_shift(fields[i], fields[k], cp)
            if r is not None:
                records.append({"a": fields[i]["field"], "b": fields[k]["field"], "dx_um": round(r[0], 2),
                                "dy_um": round(r[1], 2), "ncc": round(r[2], 3)})
                if r[2] > 0.3 and math.hypot(r[0], r[1]) < 100:
                    shifts.append(r[:2])
        if shifts:
            dx, dy = np.median(np.array(shifts), 0)
            fields[k]["gx0"] += dx
            fields[k]["gy0"] += dy
            fields[k]["reg_shift_um"] = (round(float(dx), 2), round(float(dy), 2))
        placed.append(k)
    for f in fields:
        f["stage_sign"] = (sx, sy)
    return records


def counting_regions(fields: list[dict], grid_um: float) -> None:
    """For each field, a raster (in its own frame, cells of grid_um) of the patch it owns."""
    order = sorted(range(len(fields)), key=lambda k: (fields[k]["px_um"], fields[k]["acq_order"]))
    for rank, k in enumerate(order):
        f = fields[k]
        w, h = f["nx"] * f["px_um"], f["ny"] * f["px_um"]
        nxg, nyg = int(math.ceil(w / grid_um)), int(math.ceil(h / grid_um))
        xs = f["gx0"] + (np.arange(nxg) + 0.5) * grid_um
        ys = f["gy0"] + (np.arange(nyg) + 0.5) * grid_um
        X, Y = np.meshgrid(xs, ys)
        own = np.ones((nyg, nxg), bool)
        for j in order[:rank]:
            r = field_rect(fields[j])
            own &= ~((X >= r[0]) & (X < r[2]) & (Y >= r[1]) & (Y < r[3]))
        f["priority"] = rank
        f["own"] = own
        f["own_cum"] = np.pad(own.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
        f["grid_um"] = grid_um
        f["own_area_um2"] = float(own.sum()) * grid_um ** 2


def admissible_area(f: dict, bw_um: float, bh_um: float) -> float:
    """Area of the field's own patch where a particle with this box fits entirely inside the frame."""
    g = f["grid_um"]
    w, h = f["nx"] * f["px_um"], f["ny"] * f["px_um"]
    if bw_um >= w or bh_um >= h:
        return 0.0
    ny_, nx_ = f["own"].shape
    c0 = int(math.ceil(bw_um / 2 / g)); c1 = int(math.floor((w - bw_um / 2) / g))
    r0 = int(math.ceil(bh_um / 2 / g)); r1 = int(math.floor((h - bh_um / 2) / g))
    c0, r0 = max(c0, 0), max(r0, 0)
    c1, r1 = min(c1, nx_), min(r1, ny_)
    if c1 <= c0 or r1 <= r0:
        return 0.0
    S = f["own_cum"]
    n = S[r1, c1] - S[r0, c1] - S[r1, c0] + S[r0, c0]
    return float(n) * g * g


# ----------------------------------------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------------------------------------

def wquantile(x: np.ndarray, w: np.ndarray, qs) -> np.ndarray:
    """Weighted quantiles by linear interpolation of the cumulative weight at particle mid-steps."""
    o = np.argsort(x)
    x, w = x[o], w[o]
    cw = np.cumsum(w)
    p = (cw - 0.5 * w) / cw[-1]
    return np.interp(qs, p, x)


def boot_ci(x, w, qs, groups=None, n_boot=2000, seed=0):
    """Percentile bootstrap: resample particles, or whole fields when groups is given."""
    rng = np.random.default_rng(seed)
    out = np.empty((n_boot, len(qs)))
    if groups is None:
        n = len(x)
        for b in range(n_boot):
            i = rng.integers(0, n, n)
            out[b] = wquantile(x[i], w[i], qs)
    else:
        ug = np.unique(groups)
        idx = {g: np.nonzero(groups == g)[0] for g in ug}
        for b in range(n_boot):
            pick = rng.choice(ug, len(ug), replace=True)
            i = np.concatenate([idx[g] for g in pick])
            out[b] = wquantile(x[i], w[i], qs)
    return np.percentile(out, 2.5, 0), np.percentile(out, 97.5, 0)


def boot_share(x, w, lo, hi, groups=None, n_boot=2000, seed=1):
    rng = np.random.default_rng(seed)
    vals = np.empty(n_boot)
    inb = (x >= lo) & (x < hi)
    if groups is None:
        n = len(x)
        for b in range(n_boot):
            i = rng.integers(0, n, n)
            vals[b] = w[i][inb[i]].sum() / w[i].sum()
    else:
        ug = np.unique(groups)
        idx = {g: np.nonzero(groups == g)[0] for g in ug}
        for b in range(n_boot):
            i = np.concatenate([idx[g] for g in rng.choice(ug, len(ug), replace=True)])
            vals[b] = w[i][inb[i]].sum() / w[i].sum()
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def describe(v: np.ndarray, w: np.ndarray | None = None) -> dict:
    v = np.asarray(v, float)
    w = np.ones_like(v) if w is None else np.asarray(w, float)
    ok = np.isfinite(v)
    v, w = v[ok], w[ok]
    q = wquantile(v, w, [0.1, 0.25, 0.5, 0.75, 0.9])
    return {"n": int(len(v)), "mean": float(np.average(v, weights=w)), "p10": float(q[0]), "q1": float(q[1]),
            "median": float(q[2]), "q3": float(q[3]), "p90": float(q[4]), "iqr": float(q[3] - q[1])}


# ----------------------------------------------------------------------------------------------------
# Figures
# ----------------------------------------------------------------------------------------------------

CLASS_COLORS = {  # RGB
    "counted": (0, 200, 255),
    "flagged": (255, 170, 0),
    "edge": (150, 150, 150),
    "duplicate": (210, 80, 255),
    "below_cut": (255, 60, 60),
}


def overlay_rgb(f: dict, labels: np.ndarray, cls: dict[int, str], scale: float = 1.0) -> np.ndarray:
    img = np.clip(f["img"], 0, 255).astype(np.uint8)
    rgb = np.stack([img] * 3, -1)
    bnd = segmentation.find_boundaries(labels, mode="inner")
    if scale != 1.0:
        bnd = morphology.dilation(bnd, morphology.disk(max(int(round(1 / scale)) - 1, 0))) if scale < 1 else bnd
    lab_b = np.where(bnd, labels, 0)
    lut = np.zeros((labels.max() + 1, 3), np.uint8)
    for lb, c in cls.items():
        lut[lb] = CLASS_COLORS[c]
    m = lab_b > 0
    rgb[m] = lut[lab_b[m]]
    if scale != 1.0:
        rgb = (transform.rescale(rgb, scale, channel_axis=-1, anti_aliasing=True, preserve_range=True)).astype(np.uint8)
    return rgb


def make_figures(df: pd.DataFrame, summary: dict, fields: list[dict], label_maps: dict, outdir: Path,
                 band: tuple[float, float], fines: float, overlay_field: str | None, log) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    figdir = outdir / "figures"
    figdir.mkdir(parents=True, exist_ok=True)
    made = []
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titlesize": 10, "axes.titleweight": "bold", "savefig.dpi": 160})
    C_NUM, C_VOL, C_BAND = "#2a6fdb", "#d1495b", "#e9c46a"
    use = df[df["included"]].copy()
    d = use["ecd_um"].to_numpy()
    w = use["weight"].to_numpy()
    wv = w * d ** 3

    # --- size distribution: density in ln d and cumulative ---
    lo = max(np.floor(np.log10(d.min()) * 10) / 10, 0.5)
    hi = np.ceil(np.log10(d.max()) * 10) / 10
    bins = 10 ** np.arange(lo, hi + 0.05, 0.05)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, ww, col, nm, key in ((axes[0], w, C_NUM, "Number-weighted, q0", "number"),
                                 (axes[1], wv, C_VOL, "Volume-weighted, q3", "volume")):
        hist, e = np.histogram(d, bins=bins, weights=ww)
        dens = hist / hist.sum() / np.diff(np.log(e))
        ax.axvspan(*band, color=C_BAND, alpha=0.25, lw=0, label=f"DED cut {band[0]:g}–{band[1]:g} µm")
        ax.stairs(dens, e, fill=True, color=col, alpha=0.35)
        ax.stairs(dens, e, color=col, lw=1.2)
        ax.set_xscale("log")
        ax.set_xlabel("Equivalent circle diameter (µm)")
        ax.set_ylabel("Density per ln(d)")
        ax2 = ax.twinx()
        o = np.argsort(d)
        cum = np.cumsum(ww[o]) / ww.sum()
        ax2.plot(d[o], 100 * cum, color="#333333", lw=1.4)
        ax2.set_ylim(0, 100)
        ax2.set_ylabel("Cumulative (%)")
        ax2.spines["top"].set_visible(False)
        s = summary["size"][key]
        for qn, ls in (("D10", ":"), ("D50", "--"), ("D90", ":")):
            ax.axvline(s[qn]["value"], color="#333333", lw=0.9, ls=ls)
            ax.text(s[qn]["value"], ax.get_ylim()[1] * 0.97, f" {qn} {s[qn]['value']:.0f}", fontsize=7.5,
                    va="top", ha="left", color="#333333")
        ax.set_title(f"{nm}  (n = {summary['n_counted']:,})", loc="left")
        ax.legend(loc="upper left", frameon=False, fontsize=7.5, bbox_to_anchor=(0, 0.88))
    fig.tight_layout()
    p = figdir / "size_distribution.png"
    fig.savefig(p)
    plt.close(fig)
    made.append(p.name)

    # --- shape vs size ---
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    ax = axes[0]
    flagged = use["flag"] != ""
    ax.scatter(use.loc[~flagged, "ecd_um"], use.loc[~flagged, "circularity"], s=3, alpha=0.35, color=C_NUM,
               lw=0, label="spherical")
    ax.scatter(use.loc[flagged, "ecd_um"], use.loc[flagged, "circularity"], s=7, alpha=0.8, color="#f4a261",
               lw=0, label="flagged (irregular / satellite / agglomerate)")
    ax.axvspan(*band, color=C_BAND, alpha=0.2, lw=0)
    pxs = sorted({f["px_um"] for f in fields})
    ax.axvline(summary["settings"]["shape_min_px"] * max(pxs), color="#555555", ls="--", lw=0.8)
    ax.text(summary["settings"]["shape_min_px"] * max(pxs), 0.42,
            f" {summary['settings']['shape_min_px']} px\n (shape limit)", fontsize=7, color="#555555")
    ax.set_xscale("log")
    ax.set_ylim(0.4, 1.01)
    ax.set_xlabel("Equivalent circle diameter (µm)")
    ax.set_ylabel("Circularity  2√(πA)/P")
    ax.set_title("Circularity against size", loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="lower right", markerscale=3)
    ax = axes[1]
    shp = use[use["shape_ok"]]
    for col, nm, c in (("circularity", "Circularity", "#2a6fdb"), ("aspect_ratio", "Aspect ratio (Fmin/Fmax)", "#2a9d8f"),
                       ("solidity", "Solidity", "#d1495b"), ("convexity", "Convexity", "#8d6cab")):
        v = shp[col].dropna().to_numpy()
        hb = np.linspace(0.5, 1.0, 51)
        hh, e = np.histogram(v, bins=hb, weights=shp.loc[shp[col].notna(), "weight"])
        ax.stairs(hh / hh.sum(), e, color=c, lw=1.3, label=f"{nm}: median {np.median(v):.3f}")
    ax.set_xlabel("Descriptor value")
    ax.set_ylabel("Fraction of particles")
    ax.set_title(f"ISO 9276-6 shape descriptors (particles ≥ {summary['settings']['shape_min_px']} px)", loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout()
    p = figdir / "shape.png"
    fig.savefig(p)
    plt.close(fig)
    made.append(p.name)

    # --- per-field D50 and field map ---
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axes[0]
    for f in fields:
        r = field_rect(f)
        ax.add_patch(plt.Rectangle((r[0] / 1e3, r[1] / 1e3), (r[2] - r[0]) / 1e3, (r[3] - r[1]) / 1e3, fill=False,
                                   lw=1.2, color=C_NUM if f["px_um"] < 0.8 else C_VOL))
        ax.text((r[0] + r[2]) / 2e3, (r[1] + r[3]) / 2e3, f["field"].replace("spherical", "sph"), fontsize=6.5,
                ha="center", va="center")
    allr = np.array([field_rect(f) for f in fields])
    ax.set_xlim(allr[:, 0].min() / 1e3 - 0.2, allr[:, 2].max() / 1e3 + 0.2)
    ax.set_ylim(allr[:, 3].max() / 1e3 + 0.2, allr[:, 1].min() / 1e3 - 0.2)
    ax.set_aspect("equal")
    ax.set_xlabel("Stub x (mm)")
    ax.set_ylabel("Stub y (mm)")
    ax.set_title("Field positions (blue 200x, red 133–150x)", loc="left")
    ax = axes[1]
    pf = pd.DataFrame(summary["per_field"])
    pf = pf[pf["n_counted"] > 0].sort_values("px_um")
    y = np.arange(len(pf))
    ax.errorbar(pf["D50_number_um"], y, xerr=[pf["D50_number_um"] - pf["D50_number_lo"], pf["D50_number_hi"] - pf["D50_number_um"]],
                fmt="o", color=C_NUM, ms=4, label="number D50")
    ax.errorbar(pf["D50_volume_um"], y + 0.15, xerr=[pf["D50_volume_um"] - pf["D50_volume_lo"], pf["D50_volume_hi"] - pf["D50_volume_um"]],
                fmt="s", color=C_VOL, ms=4, label="volume D50")
    ax.set_yticks(y + 0.075)
    ax.set_yticklabels([f"{a} (n={b})" for a, b in zip(pf["field"], pf["n_counted"])], fontsize=7.5)
    ax.set_xlabel("D50 (µm), 95 % bootstrap interval")
    ax.set_title("Field-to-field spread", loc="left")
    ax.legend(frameon=False, fontsize=7.5)
    fig.tight_layout()
    p = figdir / "fields.png"
    fig.savefig(p)
    plt.close(fig)
    made.append(p.name)

    # --- overlays ---
    for f in fields:
        if f["field"] not in label_maps:
            continue
        sub = df[df["field"] == f["field"]]
        cls = dict(zip(sub["label"], sub["class"]))
        rgb = overlay_rgb(f, label_maps[f["field"]], cls, scale=0.5)
        Image.fromarray(rgb).save(figdir / f"overlay_{f['field'].replace(' ', '_')}.png", optimize=True)
        made.append(f"overlay_{f['field'].replace(' ', '_')}.png")
    if overlay_field and overlay_field in label_maps:
        f = next(ff for ff in fields if ff["field"] == overlay_field)
        sub = df[df["field"] == f["field"]]
        cls = dict(zip(sub["label"], sub["class"]))
        full = overlay_rgb(f, label_maps[f["field"]], cls, scale=1.0)
        h, wd = full.shape[:2]
        crop = full[h // 2 - 400: h // 2 + 400, wd // 2 - 600: wd // 2 + 600]
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.5, 1.5]})
        axes[0].imshow(overlay_rgb(f, label_maps[f["field"]], cls, scale=0.5))
        axes[0].add_patch(plt.Rectangle(((wd // 2 - 600) / 2, (h // 2 - 400) / 2), 600, 400, fill=False, color="w", lw=1))
        axes[0].set_title(f"{f['field']}: {f['px_um']:.3f} µm/px, {int((sub['class'] == 'counted').sum())} counted", loc="left")
        axes[1].imshow(crop)
        axes[1].set_title("Centre crop at full resolution", loc="left")
        for ax in axes:
            ax.set_xticks([]); ax.set_yticks([])
        handles = [plt.Line2D([], [], color=np.array(c) / 255, lw=3, label=k) for k, c in CLASS_COLORS.items()]
        axes[1].legend(handles=handles, loc="lower right", fontsize=7, framealpha=0.85)
        fig.tight_layout()
        p = figdir / "overlay_example.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        made.append(p.name)
    log(f"  figures: {', '.join(made)}")
    return made


# ----------------------------------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------------------------------

def classify(df: pd.DataFrame, args) -> pd.DataFrame:
    """Flags for shape outliers. Flagged particles stay in the distribution and are listed separately."""
    flag = np.full(len(df), "", dtype=object)
    shape_ok = df["ecd_um"] / df["px_um"] >= args.shape_min_px
    irregular = shape_ok & ((df["aspect_ratio"] < args.ar_flag) | (df["solidity"] < args.solidity_flag))
    agglom = shape_ok & ((df["solidity"] < args.agglomerate_solidity) | (df["aspect_ratio"] < args.agglomerate_ar))
    flag[irregular.to_numpy()] = "irregular"
    flag[agglom.to_numpy()] = "agglomerate_or_elongated"
    over = df["ecd_um"] > args.band[1]
    flag = np.where(over & (flag == ""), "oversize", np.where(over, flag + "+oversize", flag))
    df["flag"] = flag
    df["shape_ok"] = shape_ok
    return df


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("image_dir", type=Path, help="folder of FEI/TFS .tif images")
    ap.add_argument("out_dir", type=Path, help="folder for particles.csv, summary and figures")
    ap.add_argument("--include", nargs="*", default=["*.tif", "*.tiff"], help="glob(s) of fields to size")
    ap.add_argument("--exclude", nargs="*", default=[], help="glob(s) of files to skip (annotated, close-ups)")
    ap.add_argument("--max-px-um", type=float, default=2.0,
                    help="skip fields coarser than this; close-ups are skipped by --min-hfw-um")
    ap.add_argument("--min-hfw-um", type=float, default=1000.0, help="skip close-ups narrower than this")
    ap.add_argument("--k-sigma", type=float, default=5.0, help="threshold, robust sigmas above background")
    ap.add_argument("--h-rel", type=float, default=0.15, help="relative depth of a distance maximum to split")
    ap.add_argument("--min-px", type=float, default=10.0, help="lower size limit, pixels across (ECD)")
    ap.add_argument("--shape-min-px", type=float, default=20.0, help="lower size limit for shape statistics")
    ap.add_argument("--band", nargs=2, type=float, default=[50.0, 200.0], help="size band to report (um)")
    ap.add_argument("--fines", type=float, default=20.0, help="report the share below this size (um)")
    ap.add_argument("--ar-flag", type=float, default=0.80, help="flag irregular if Fmin/Fmax below this")
    ap.add_argument("--solidity-flag", type=float, default=0.93, help="flag irregular if solidity below this")
    ap.add_argument("--agglomerate-solidity", type=float, default=0.85)
    ap.add_argument("--agglomerate-ar", type=float, default=0.60)
    ap.add_argument("--no-edge-correction", action="store_true", help="skip the edge offset correction of ECD")
    ap.add_argument("--no-dedupe", action="store_true", help="treat fields as independent (no overlap removal)")
    ap.add_argument("--mask-annotations", action="store_true", help="inpaint burned-in xT annotation text")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--overlay-field", default=None, help="field for the overlay figure (default: first)")
    ap.add_argument("--save-labels", action="store_true", help="also write label images (.npz)")
    args = ap.parse_args(argv)
    args.band = tuple(args.band)

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / "run.log", "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")

    t0 = time.time()
    paths = sorted(p for p in args.image_dir.iterdir() if p.suffix.lower() in (".tif", ".tiff"))
    paths = [p for p in paths if any(fnmatch.fnmatch(p.name, g) for g in args.include)
             and not any(fnmatch.fnmatch(p.name, g) for g in args.exclude)]
    fields = []
    for p in paths:
        f = read_field(p)
        if f["hfw_um"] < args.min_hfw_um or f["px_um"] > args.max_px_um:
            log(f"skip {p.name}: HFW {f['hfw_um']:.0f} um, {f['px_um']:.3f} um/px (close-up or too coarse)")
            continue
        fields.append(f)
    if not fields:
        log("no fields to size")
        return 1
    # acquisition order (date and time string from the metadata) breaks ties in field priority
    def acq_key(f):
        try:
            return time.mktime(time.strptime(f["acquired"], "%m/%d/%Y %I:%M:%S %p"))
        except ValueError:
            return 0.0
    for k, f in enumerate(sorted(fields, key=acq_key)):
        f["acq_order"] = k
    log(f"sem_psd {VERSION}: {len(fields)} fields: " + ", ".join(f["field"] for f in fields))

    frames, label_maps = [], {}
    for f in fields:
        t1 = time.time()
        if args.mask_annotations:
            f["img"], amask = mask_annotations(f["img"])
            f["annotation_px"] = int(amask.sum())
        labels, info = segment(f["img"], k_sigma=args.k_sigma, h_rel=args.h_rel)
        delta, n_iso = (0.0, 0) if args.no_edge_correction else edge_offset(info["res"], labels, info["threshold_above_bg"])
        f.update({k: v for k, v in info.items() if k not in ("sm", "res", "bg")})
        f["edge_offset_px"] = round(delta, 3)
        f["edge_offset_n"] = n_iso
        df = measure_field(f, labels, delta)
        frames.append(df)
        label_maps[f["field"]] = labels
        log(f"  {f['field']}: {f['px_um']:.4f} um/px, threshold bg+{info['threshold_above_bg']:.1f}, "
            f"{len(df)} regions, edge offset {delta:+.2f} px from {n_iso} round particles, {time.time() - t1:.1f} s")
        if args.save_labels:
            np.savez_compressed(out / f"labels_{f['field'].replace(' ', '_')}.npz", labels=labels.astype(np.int32))
    df = pd.concat(frames, ignore_index=True)

    # --- geometry ---
    if len(fields) > 1 and not args.no_dedupe:
        log("registering fields")
        reg = register_fields(fields, log)
        for r in reg:
            log(f"  {r['b']} vs {r['a']}: residual shift ({r['dx_um']:+.1f}, {r['dy_um']:+.1f}) um, NCC {r['ncc']:.2f}")
    else:
        reg = []
        x = 0.0
        for f in fields:  # lay fields side by side so they never overlap
            f["gx0"], f["gy0"] = x, 0.0
            x += f["nx"] * f["px_um"] + 1000
            f["stage_sign"] = (0, 0)
    grid = min(f["px_um"] for f in fields) * 4
    counting_regions(fields, grid)
    fmap = {f["field"]: f for f in fields}
    gx = np.empty(len(df)); gy = np.empty(len(df)); owned = np.zeros(len(df), bool)
    for name, sub in df.groupby("field"):
        f = fmap[name]
        x, y = to_global(f, sub["cx_px"].to_numpy(), sub["cy_px"].to_numpy())
        gx[sub.index], gy[sub.index] = x, y
        c = np.clip(((x - f["gx0"]) / f["grid_um"]).astype(int), 0, f["own"].shape[1] - 1)
        r = np.clip(((y - f["gy0"]) / f["grid_um"]).astype(int), 0, f["own"].shape[0] - 1)
        owned[sub.index] = f["own"][r, c]
    df["gx_um"], df["gy_um"] = gx, gy
    df["in_own_patch"] = owned
    df["min_um_field"] = df["px_um"] * args.min_px
    df["below_cut"] = df["ecd_um"] < df["min_um_field"]

    # lower size limit per field: a particle of size d is only countable in fields that resolve it
    a_total = sum(f["own_area_um2"] for f in fields)
    weights = np.full(len(df), np.nan)
    for i, row in enumerate(df.itertuples()):
        if row.touches_edge or not row.in_own_patch or row.below_cut:
            continue
        bw, bh = row.bbox_w_px * row.px_um, row.bbox_h_px * row.px_um
        adm = sum(admissible_area(f, bw, bh) for f in fields if row.ecd_um >= f["px_um"] * args.min_px)
        weights[i] = a_total / adm if adm > 0 else np.nan
    df["weight"] = weights
    df = classify(df, args)
    cls = np.where(df["touches_edge"], "edge",
          np.where(~df["in_own_patch"], "duplicate",
          np.where(df["below_cut"], "below_cut",
          np.where(df["flag"].isin(["", "oversize"]), "counted", "flagged"))))
    df["class"] = cls
    df["included"] = df["weight"].notna()

    # cross-field repeatability: particles seen whole in two fields (matched by position and size)
    matches = []
    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            a = df[(df["field"] == fields[i]["field"]) & ~df["touches_edge"] & ~df["below_cut"]]
            b = df[(df["field"] == fields[j]["field"]) & ~df["touches_edge"] & ~df["below_cut"]]
            if a.empty or b.empty or overlap(field_rect(fields[i]), field_rect(fields[j])) <= 0:
                continue
            from scipy.spatial import cKDTree
            tb = cKDTree(b[["gx_um", "gy_um"]].to_numpy())
            dd, jj = tb.query(a[["gx_um", "gy_um"]].to_numpy(), distance_upper_bound=15.0)
            for (ia, ra), dist_, jb in zip(a.iterrows(), dd, jj):
                if not np.isfinite(dist_):
                    continue
                rb = b.iloc[jb]
                if dist_ < max(5.0, 0.25 * ra["ecd_um"]) and abs(ra["ecd_um"] - rb["ecd_um"]) < 0.3 * ra["ecd_um"]:
                    matches.append({"field_a": ra["field"], "field_b": rb["field"], "d_a": ra["ecd_um"], "d_b": rb["ecd_um"],
                                    "sep_um": dist_})
    mt = pd.DataFrame(matches)

    # --- statistics ---
    use = df[df["included"]]
    d = use["ecd_um"].to_numpy()
    w = use["weight"].to_numpy()
    g = use["field"].to_numpy()
    qs = [0.1, 0.5, 0.9]
    summary = {
        "tool": f"sem_psd.py {VERSION}",
        "image_dir": str(args.image_dir),
        "settings": {k: (list(v) if isinstance(v, tuple) else (str(v) if isinstance(v, Path) else v))
                     for k, v in vars(args).items()},
        "n_regions": int(len(df)),
        "n_counted": int(len(use)),
        "n_edge_excluded": int(df["touches_edge"].sum()),
        "n_duplicate_excluded": int(((~df["in_own_patch"]) & ~df["touches_edge"]).sum()),
        "n_below_cut": int((df["below_cut"] & ~df["touches_edge"] & df["in_own_patch"]).sum()),
        "area_analysed_mm2": a_total / 1e6,
        "size": {},
        "shares": {},
    }
    for key, ww in (("number", w), ("volume", w * d ** 3)):
        val = wquantile(d, ww, qs)
        plo, phi = boot_ci(d, ww, qs, n_boot=args.n_boot, seed=0)
        flo, fhi = boot_ci(d, ww, qs, groups=g, n_boot=args.n_boot, seed=0) if len(np.unique(g)) > 2 else (plo * np.nan, phi * np.nan)
        summary["size"][key] = {qn: {"value": float(v), "ci_particles": [float(a), float(b)], "ci_fields": [float(c), float(e)]}
                                for qn, v, a, b, c, e in zip(("D10", "D50", "D90"), val, plo, phi, flo, fhi)}
        summary["size"][key]["span"] = float((val[2] - val[0]) / val[1])
        for nm, lo_, hi_ in (("band", args.band[0], args.band[1]), ("fines", 0.0, args.fines),
                             ("above_band", args.band[1], np.inf)):
            inb = (d >= lo_) & (d < hi_)
            share = float(ww[inb].sum() / ww.sum())
            ci_p = boot_share(d, ww, lo_, hi_, n_boot=args.n_boot)
            ci_f = boot_share(d, ww, lo_, hi_, groups=g, n_boot=args.n_boot) if len(np.unique(g)) > 2 else (np.nan, np.nan)
            summary["shares"].setdefault(nm, {"range_um": [lo_, None if not np.isfinite(hi_) else hi_]})[key] = {
                "share": share, "ci_particles": list(ci_p), "ci_fields": list(ci_f), "n_particles": int(inb.sum())}
    shp = use[use["shape_ok"]]
    summary["shape"] = {c: describe(shp[c], shp["weight"]) for c in
                        ("circularity", "form_factor", "aspect_ratio", "solidity", "convexity")}
    summary["shape"]["n"] = int(len(shp))
    flags = use["flag"].value_counts().to_dict()
    summary["flags"] = {k if k else "none": int(v) for k, v in flags.items()}
    summary["flagged_number_share"] = float(w[use["flag"].isin(["irregular", "agglomerate_or_elongated", "irregular+oversize",
                                                                 "agglomerate_or_elongated+oversize"]).to_numpy()].sum() / w.sum())
    nonflag = (use["flag"].isin(["", "oversize"])).to_numpy()
    summary["size_excluding_flagged"] = {
        key: dict(zip(("D10", "D50", "D90"), map(float, wquantile(d[nonflag], ww[nonflag], qs))))
        for key, ww in (("number", w), ("volume", w * d ** 3))}
    cf = use["circle_fit_um"].to_numpy()
    okc = np.isfinite(cf)
    dd_ = np.where(okc, cf, d)
    summary["size_circle_fit"] = {
        key: dict(zip(("D10", "D50", "D90"), map(float, wquantile(dd_, ww, qs))))
        for key, ww in (("number", w), ("volume", w * dd_ ** 3))}
    summary["size_no_edge_offset_correction"] = {
        key: dict(zip(("D10", "D50", "D90"), map(float, wquantile(use["ecd_raw_um"].to_numpy(), ww, qs))))
        for key, ww in (("number", w), ("volume", w * use["ecd_raw_um"].to_numpy() ** 3))}
    summary["largest_particles"] = use.nlargest(8, "ecd_um")[["field", "label", "ecd_um", "circle_fit_um", "circularity",
                                                              "aspect_ratio", "solidity", "flag", "cx_px", "cy_px"]].round(3).to_dict("records")
    if not mt.empty:
        rel = (mt["d_b"] - mt["d_a"]) / ((mt["d_a"] + mt["d_b"]) / 2)
        summary["cross_field_matches"] = {"n": int(len(mt)), "mean_rel_diff": float(rel.mean()),
                                          "sd_rel_diff": float(rel.std()), "median_sep_um": float(mt["sep_um"].median()),
                                          "pairs": mt.groupby(["field_a", "field_b"]).size().reset_index(name="n").to_dict("records")}
    summary["registration"] = reg
    per_field = []
    for f in fields:
        sub = use[use["field"] == f["field"]]
        rec = {"field": f["field"], "px_um": f["px_um"], "n_regions": int((df["field"] == f["field"]).sum()),
               "n_counted": int(len(sub)), "edge_offset_px": f["edge_offset_px"]}
        if len(sub) >= 20:
            dn, wn = sub["ecd_um"].to_numpy(), sub["weight"].to_numpy()
            for key, ww in (("number", wn), ("volume", wn * dn ** 3)):
                v = wquantile(dn, ww, [0.5])[0]
                lo_, hi_ = boot_ci(dn, ww, [0.5], n_boot=500, seed=2)
                rec[f"D50_{key}_um"], rec[f"D50_{key}_lo"], rec[f"D50_{key}_hi"] = float(v), float(lo_[0]), float(hi_[0])
            rec["band_number_share"] = float(wn[(dn >= args.band[0]) & (dn < args.band[1])].sum() / wn.sum())
        per_field.append(rec)
    summary["per_field"] = per_field
    summary["fields"] = [{k: v for k, v in f.items() if k not in ("img", "own", "own_cum", "_rescaled")} for f in fields]
    summary["runtime_s"] = round(time.time() - t0, 1)

    # --- write ---
    cols = ["field", "label", "class", "flag", "included", "weight", "ecd_um", "ecd_raw_um", "circle_fit_um",
            "feret_max_um", "feret_min_um", "circularity", "form_factor", "aspect_ratio", "solidity", "convexity",
            "area_px", "perimeter_px", "px_um", "cx_px", "cy_px", "gx_um", "gy_um", "bbox_w_px", "bbox_h_px",
            "touches_edge", "in_own_patch", "below_cut", "shape_ok", "free_boundary_frac"]
    df[cols].round(4).to_csv(out / "particles.csv", index=False)
    pd.DataFrame(summary["fields"]).drop(columns=["bg_coef"], errors="ignore").to_csv(out / "fields.csv", index=False)
    if not mt.empty:
        mt.round(3).to_csv(out / "cross_field_matches.csv", index=False)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")
    overlay_field = args.overlay_field or fields[0]["field"]
    make_figures(df, summary, fields, label_maps, out, args.band, args.fines, overlay_field, log)
    write_summary_md(summary, out)
    log(f"done in {time.time() - t0:.0f} s: {summary['n_counted']} particles counted")
    return 0


def write_summary_md(s: dict, out: Path) -> None:
    def ci(x, k="ci_particles", fmt="{:.1f}"):
        a, b = x[k]
        if a is None or (isinstance(a, float) and math.isnan(a)):
            return "n/a"
        return f"{fmt.format(a)}–{fmt.format(b)}"
    L = [f"# Particle size and shape summary ({s['tool']})", "",
         f"- Fields: {', '.join(f['field'] for f in s['fields'])}",
         f"- Area analysed: {s['area_analysed_mm2']:.2f} mm² (union of fields, overlaps counted once)",
         f"- Regions segmented: {s['n_regions']:,}; counted: **{s['n_counted']:,}**; excluded: {s['n_edge_excluded']:,} touching the frame, "
         f"{s['n_duplicate_excluded']:,} in a patch owned by another field, {s['n_below_cut']:,} below {s['settings']['min_px']:g} px", "",
         "## Size (equivalent circle diameter, µm)", "",
         "| Weighting | D10 | D50 | D90 | Span |", "|---|---|---|---|---|"]
    for key in ("number", "volume"):
        z = s["size"][key]
        L.append(f"| {key} | {z['D10']['value']:.1f} ({ci(z['D10'])}; fields {ci(z['D10'], 'ci_fields')}) | "
                 f"{z['D50']['value']:.1f} ({ci(z['D50'])}; fields {ci(z['D50'], 'ci_fields')}) | "
                 f"{z['D90']['value']:.1f} ({ci(z['D90'])}; fields {ci(z['D90'], 'ci_fields')}) | {z['span']:.2f} |")
    L += ["", "95 % intervals: particle bootstrap, then field (cluster) bootstrap.", "", "## Shares", "",
          "| Range | By number | By volume |", "|---|---|---|"]
    for nm, z in s["shares"].items():
        rng = z["range_um"]
        lab = f"{rng[0]:g}–{rng[1]:g} µm" if rng[1] is not None else f"> {rng[0]:g} µm"
        if nm == "fines":
            lab = f"< {rng[1]:g} µm"
        L.append(f"| {lab} | {100 * z['number']['share']:.1f} % ({100 * z['number']['ci_particles'][0]:.1f}–{100 * z['number']['ci_particles'][1]:.1f}) | "
                 f"{100 * z['volume']['share']:.1f} % ({100 * z['volume']['ci_particles'][0]:.1f}–{100 * z['volume']['ci_particles'][1]:.1f}) |")
    L += ["", f"## Shape (ISO 9276-6), {s['shape']['n']:,} particles ≥ {s['settings']['shape_min_px']:g} px", "",
          "| Descriptor | Median | IQR | P10 | P90 |", "|---|---|---|---|---|"]
    for c in ("circularity", "form_factor", "aspect_ratio", "solidity", "convexity"):
        z = s["shape"][c]
        L.append(f"| {c} | {z['median']:.3f} | {z['q1']:.3f}–{z['q3']:.3f} | {z['p10']:.3f} | {z['p90']:.3f} |")
    L += ["", f"Flags among counted particles: {s['flags']}", ""]
    (out / "summary.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
