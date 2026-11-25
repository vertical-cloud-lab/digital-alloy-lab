"""Vendor photos -> per-body finishes, front-panel layouts and silhouette fits of the OEM part models (issue #260).

    python desktop-lpbf/cad/oem/photo_fit.py            # everything below, from the photos in $OEM_PHOTOS (default /tmp/agentE/photos)

1. photo-manifest.csv   every photo used: part, vendor, source URL, sha256, pixel size, fetch time. The photos themselves are the
                        vendors' copyright and are NOT committed; they stay in /tmp (re-fetch them from the URLs).
2. finishes.json        per builder key (as in vendor_parts.SOURCES) and per visible body: median colour of a segmented region
                        (sRGB hex and linear RGB), metallic and roughness. Metallic is set from the material (bare metal 1.0,
                        anodised 0.5, paint/plastic/rubber/glass 0.0); the highlight chroma is reported as a check. Roughness is
                        a HEURISTIC from the region's highlight statistics: r = 0.15 + 2.5 * (share of pixels in the top half of
                        the luminance range) + 0.4 * (1 - specular contrast), clipped to 0.08-0.95. McMaster's images are renders,
                        so their colours are McMaster's render materials, not a measurement of the real finish.
3. layouts              front-panel features of the IPG YLR-U rack chassis (perspective photo rectified with a homography) and of
                        the Eaton 5PX G2 (orthographic front view in Eaton's datasheet), as fractions of the panel width/height.
4. silhouette fits      camera pose AND focal length solved by silhouette fitting: the vendor_parts model is tessellated, projected
                        through a pinhole camera (principal point at the image centre), filled triangle by triangle, and the pose
                        (Rodrigues vector, translation) and log focal length are optimised (Nelder-Mead, restarts) to maximise
                        the IoU with the photo's object mask. A focal-length profile (best IoU with f held fixed) shows how well
                        the silhouette pins down f. Outputs: analysis/out/oem/photo_fit.json and overlay_<part>.png, which show
                        ONLY the photo-derived mask outline against the model silhouette (no photo pixels).
Run under the memory cap: OMP_NUM_THREADS=1 /tmp/capmem 2 /tmp/venv/bin/python desktop-lpbf/cad/oem/photo_fit.py
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import json
import math
import os
import pathlib
import sys

import cv2
import numpy as np
from scipy.optimize import minimize

HERE = pathlib.Path(__file__).resolve().parent            # desktop-lpbf/cad/oem
CAD = HERE.parent
OUT = CAD.parent / "analysis" / "out" / "oem"
PH = pathlib.Path(os.environ.get("OEM_PHOTOS", "/tmp/agentE/photos"))
OV = pathlib.Path(os.environ.get("OEM_OVERLAYS", "/tmp/agentE/overlays"))

# --------------------------------------------------------------------------------------------
# Photos used (id -> builder key, file under PH, vendor, source URL override (else read from the slug's index.json), note)
# --------------------------------------------------------------------------------------------
PHOTOS = {
    "teknic_cpm231": ("clearpath_sd_231x", "teknic/img21.jpg", "Teknic", None, "gallery photo cpm_231_L_lg.jpg on the CPM-SDSK-2311S-RLN model page (ClearPath NEMA 23, 231x frame)"),
    "eaton_front": ("eaton_5px1500rtg2", "eaton_pdf/p0_x15.png", "Eaton", "https://assets.tripplite.com/product-pdfs/en/5px1500rtg2.pdf",
                    "front view embedded on page 1 of Eaton's 5PX1500RTG2 datasheet (extracted with PyMuPDF)"),
    "ipg_rack_card": ("ipg_ylr500_u3", "ipg_hi/card.png", "IPG Photonics",
                      "https://cdn.ipgphotonics.com/dd75a420-a632-4027-a1ca-b0200153b461/YLR_U_Rack_Card_cms_crd_2x.png?width=2000&format=png",
                      "YLR-U rack family card on IPG's ultra-compact laser page (YLR-1500-U, -3000-U, -6000-U; the 4U -6000-U is used)"),
    "mcm_4123K45": ("mcm_4123K45", "mcm_4123K45/img00.png", "McMaster-Carr", None, "product image (render)"),
    "mcm_4518K72": ("mcm_4518K72", "mcm_4518K72/img00.png", "McMaster-Carr", None, "product image (render)"),
    "mcm_5786N23": ("mcm_5786N23", "mcm_5786N23/img00.png", "McMaster-Carr", None, "product image (render)"),
    "mcm_6627T91": ("mcm_6627T91", "mcm_6627T91/img00.png", "McMaster-Carr", None, "product image (render)"),
    "mcm_6709K12": ("mcm_6709K12", "mcm_6709K12/img00.png", "McMaster-Carr", None, "product image (render)"),
    "mcm_4566N401": ("mcm_4566N401", "mcm_4566N401/img00.png", "McMaster-Carr", None, "product image (render)"),
    "mcm_5169K72": ("mcm_5169K72", "mcm_5169K72/img00.png", "McMaster-Carr",
                    "https://www.mcmaster.com/mvD/Contents/gfx/ImageCache/516/5169K72_d29df2b6-f3f2-4e58-bf9a-7bd86f0c4ef5@4x_1709241645.png?ver=ImageNotFound",
                    "product image (render)"),
    "mcm_3861N11": ("mcm_3861N11", "mcm_3861N11/img00.png", "McMaster-Carr",
                    "https://www.mcmaster.com/mvC/Contents/gfx/ImageCache/386/3861N11_450d82a6-929b-4c94-b383-a8c3f12b78a8@4x_76lla_1768238631.png?ver=ImageNotFound",
                    "product image (render)"),
    "mcm_4396K21": ("mcm_4396K21", "mcm_4396K21/img00.png", "McMaster-Carr", None, "product image (render)"),
    # round 6 (2026-11-25)
    "nxds_brochure_p1": ("edwards_nxds6i", "nxds/brochure_p1_150dpi.png", "Edwards",
                         "https://assets.testequity.com/te1/Documents/pdf/Edwards/Edwards_nXDS_Brochure_0425.pdf",
                         "cover photo of Edwards' nXDS brochure (rev 0425), page 1 rendered at 150 dpi with PyMuPDF; the fan end is under a translucent overlay"),
    "ipg_sm_family": ("ipg_ylr500_u3", "ipg/yls_sm_family_hero.png", "IPG Photonics",
                      "https://cdn.ipgphotonics.com/a55a8a0e-9911-4793-acae-b06c016526c8/YLS_SM_Family_Main_cms_hero_1x.png?disable=upscale&width=834&format=png",
                      "single-mode family render on IPG's 'Single-Mode Fiber Lasers' page; its 4U rack unit (front, lower centre) is used"),
    "eaton_front_2k": ("eaton_5px1500rtg2", "eaton/5PX1500RTG2_C_2000x2000_300dpi.jpeg", "Eaton",
                       "https://www.eaton.com/mdmfiles/PDM93866092/5PX1500RTG2_C/2000x2000_300dpi",
                       "straight-on product image on eaton.com's 5PX1500RTG2 SKU page (2000 x 2000 px)"),
    "eaton_r_2k": ("eaton_5px1500rtg2", "eaton/5PX1500RTG2_R_2000x2000_300dpi.jpeg", "Eaton",
                   "https://www.eaton.com/mdmfiles/PDM93866093/5PX1500RTG2_R/2000x2000_300dpi",
                   "three-quarter product image on eaton.com's 5PX1500RTG2 SKU page (2000 x 2000 px), no rack ears"),
}
# photos whose background is not near-white (GrabCut seeds fail): colours are read from hand-picked rectangles inside the part only
RECT_ONLY = {"nxds_brochure_p1"}
# per-photo cut (photo px polygon set to background): McMaster's 3861N11 image shows the coiled 36 in. lead, which the builder
# does not draw; everything left of the cable gland is cut
CUTS = {"mcm_3861N11": [(0, 0), (497, 0), (325, 297), (0, 297)]}   # a line square to the axis through the gland end (443, 94)

METALLIC = {"bare_metal": 1.0, "anodised": 0.5, "paint": 0.0, "plastic": 0.0, "rubber": 0.0, "lcd": 0.0, "printed": 0.0}

# Colour regions: photo id -> [(body, (x0, y0, x1, y1) in photo pixels or None = whole object mask, (Lmin, Lmax) CIE L*, max chroma or None, material)]
# Rectangles were picked on gridded zooms of each photo (cp_grid.png, eaton_grid.png, ipg_grid.png in $OEM_OVERLAYS).
REGIONS = {
    "teknic_cpm231": [
        ("flange (machined/cast aluminium front plate)", (300, 228, 345, 300), (55, 100), 12, "bare_metal"),
        ("body (black anodised extrusion)", (420, 262, 560, 500), (0, 45), None, "anodised"),
        ("rear housing (die-cast aluminium, fins)", (610, 262, 690, 450), (50, 100), 15, "bare_metal"),
        ("connectors (black plastic)", (505, 150, 560, 230), (0, 35), None, "plastic"),
        ("shaft (ground steel)", (235, 372, 300, 400), (40, 100), 12, "bare_metal"),
        ("rear cap (grey plastic)", (700, 140, 724, 220), (60, 100), 12, "plastic"),
    ],
    "eaton_front": [
        ("grille (perforated silver bezel, holes included)", (125, 216, 355, 286), (0, 100), None, "paint"),
        ("grille metal between holes", (125, 216, 355, 286), (62, 100), None, "paint"),
        ("display module surround (black)", (440, 212, 457, 268), (0, 30), None, "plastic"),
        ("LCD (lit, blue-white)", (395, 228, 430, 260), (0, 100), None, "lcd"),
        ("status light bar (blue)", (384, 281, 445, 286), (0, 100), 200, "plastic"),
        ("Eaton badge", (83, 239, 108, 262), (0, 100), None, "plastic"),
    ],
    "ipg_rack_card": [
        ("front panel, light area (left)", (60, 470, 190, 600), (60, 100), 15, "paint"),
        ("front panel, dark dot-pattern area", (420, 670, 640, 730), (0, 100), None, "paint"),
        ("blue swoosh stripe", (470, 580, 600, 586), (0, 100), None, "paint"),
        ("model label (black)", (420, 592, 520, 615), (0, 30), None, "paint"),
        ("rack handles (black)", (31, 520, 47, 660), (0, 35), None, "plastic"),
        ("chassis side (black)", (720, 520, 820, 600), (0, 100), None, "paint"),
    ],
    "mcm_4123K45": [
        ("lever grip (grey vinyl)", (30, 10, 300, 70), (0, 100), 10, "plastic"),
        ("body, end caps, tie bolts (cast 316 stainless)", (290, 330, 560, 600), (20, 100), 10, "bare_metal"),
        ("KF flanges (machined stainless)", (560, 420, 720, 560), (20, 100), 10, "bare_metal"),
    ],
    "mcm_4518K72": [("clamp (aluminium)", None, (0, 100), None, "bare_metal")],
    "mcm_5786N23": [("fitting (aluminium)", None, (0, 100), None, "bare_metal")],
    "mcm_4566N401": [("nut and flange (steel)", None, (0, 100), None, "bare_metal")],
    "mcm_6627T91": [("housing and end caps (black)", None, (0, 30), None, "paint"),
                    ("front face, pilot and shaft (aluminium/steel)", None, (55, 100), 12, "bare_metal")],
    "mcm_6709K12": [("steel block", None, (50, 100), 12, "bare_metal"), ("end caps and seals (black plastic)", None, (0, 30), None, "plastic")],
    "mcm_5169K72": [("housing (black)", None, (0, 35), None, "paint"), ("bail clips (steel wire)", None, (60, 100), 12, "bare_metal")],
    "mcm_3861N11": [("body and cable (black)", None, (0, 30), None, "plastic"), ("hex and thread (stainless)", None, (55, 100), 12, "bare_metal")],
    "mcm_4396K21": [("motor and handle grip (black)", None, (0, 30), None, "paint"), ("pump block and guard (aluminium)", None, (55, 100), 12, "bare_metal")],
    # round 6: rectangles picked on gridded zooms of each photo (nxds_photo_grid.png, ipg4u_grid.png, eaton_left/right.png)
    "nxds_brochure_p1": [
        ("housing and fins (painted cast aluminium)", (205, 1025, 455, 1175), (55, 100), 12, "paint"),
        ("base, side face (painted cast aluminium)", (217, 1237, 367, 1300), (55, 100), 12, "paint"),
        ("connector panel (light grey plate)", (405, 1350, 605, 1525), (70, 100), 12, "plastic"),
        ("inlet flange, NW25 (stainless)", (542, 806, 630, 887), (30, 100), 14, "bare_metal"),
        ("exhaust flange, NW25 (stainless)", (711, 1250, 817, 1375), (30, 100), 14, "bare_metal"),
        ("lifting eye (stainless)", (524, 712, 580, 775), (30, 100), 14, "bare_metal"),
        ("IEC inlet (black)", (267, 1331, 330, 1400), (0, 30), None, "plastic"),
        ("START key (green)", (365, 1365, 392, 1394), (0, 100), None, "plastic"),
        ("STOP key (red)", (365, 1412, 392, 1435), (0, 100), None, "plastic"),
    ],
    "ipg_sm_family": [
        ("4U front panel, light area", (455, 592, 468, 610), (60, 100), 15, "paint"),
        ("4U fan field (dark perforated)", (495, 597, 553, 630), (0, 100), None, "paint"),
        ("4U window (light grey)", (436, 585, 451, 618), (40, 100), 15, "plastic"),
        ("4U handles (black)", (411, 588, 416, 642), (0, 40), None, "plastic"),
        ("4U START (green)", (422, 587, 428, 592), (0, 100), None, "plastic"),
        ("4U mushroom (red)", (421, 599, 431, 606), (0, 100), None, "plastic"),
        ("4U chassis side (black)", (320, 570, 395, 635), (0, 45), None, "paint"),
    ],
    "eaton_front_2k": [
        ("grille (perforated silver, holes included)", (450, 870, 1100, 1120), (0, 100), None, "paint"),
        ("grille metal between holes", (450, 870, 1100, 1120), (62, 100), None, "paint"),
        ("bezel frame (dark grey)", (300, 842, 1450, 862), (0, 60), None, "plastic"),
        ("LCD module surround (black)", (1730, 880, 1785, 1060), (0, 30), None, "plastic"),
        ("LCD (lit)", (1580, 935, 1710, 1020), (0, 100), None, "lcd"),
        ("LED bar (blue)", (1530, 1132, 1780, 1139), (0, 100), 200, "plastic"),
        ("Eaton badge", (290, 955, 385, 1055), (70, 100), None, "plastic"),
        ("keys (dark grey)", (1525, 1082, 1567, 1122), (0, 45), None, "plastic"),
    ],
}


# Contact shadow under the ClearPath in Teknic's photo: GrabCut keeps it (it is as dark as the parts), so everything below the
# motor's bottom outline (picked on cp_grid.png: flange bottom, black body bottom, rear housing bottom, fins) is set as background.
SHADOW_CUT = {"img21.jpg": [(200, 560), (332, 548), (377, 556), (380, 522), (550, 502), (700, 452), (760, 440), (760, 682), (200, 682)]}


def load(path, pid=None):
    """-> (BGR uint8 image, object mask uint8 0/1). Alpha where the image has it, else GrabCut seeded by near-white = background.
    CUTS[pid] (a photo px polygon) is set to background."""
    im = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if im.ndim == 3 and im.shape[2] == 4:
        a = im[:, :, 3]
        bgr = im[:, :, :3].copy()
        bgr[a < 8] = 255
        mask = (a > 127).astype(np.uint8)
        if pid in CUTS:
            cv2.fillPoly(mask, [np.array(CUTS[pid], np.int32)], 0)
            mask = _clean(mask)
        return bgr, mask
    bgr = im[:, :, :3] if im.ndim == 3 else cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    m = np.full(g.shape, cv2.GC_PR_BGD, np.uint8)
    m[(g < 225) | (hsv[:, :, 1] > 40)] = cv2.GC_PR_FGD
    m[g < 120] = cv2.GC_FGD
    m[(g > 243) & (hsv[:, :, 1] < 20)] = cv2.GC_BGD
    cut = SHADOW_CUT.get(pathlib.Path(path).name)
    if cut:
        cv2.fillPoly(m, [np.array(cut, np.int32)], int(cv2.GC_BGD))
    bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, m, None, bg, fg, 5, cv2.GC_INIT_WITH_MASK)
    mask = np.isin(m, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    if cut:
        cv2.fillPoly(mask, [np.array(cut, np.int32)], 0)
    return bgr, _clean(mask)


def _clean(mask):
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        mask = (lab == k).astype(np.uint8)
    ff = mask.copy()                                   # fill holes
    h, w = ff.shape
    canvas = np.zeros((h + 2, w + 2), np.uint8)
    inv = (1 - ff).astype(np.uint8)
    cv2.floodFill(inv, canvas, (0, 0), 0)
    return np.maximum(mask, inv)


def srgb_to_linear(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def measure(bgr, mask, rect, Lr, cmax, material):
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(float)
    L, A, B = lab[:, :, 0] * 100.0 / 255.0, lab[:, :, 1] - 128.0, lab[:, :, 2] - 128.0
    C = np.hypot(A, B)
    sel = mask.astype(bool).copy()
    if rect is not None:
        r = np.zeros_like(sel)
        x0, y0, x1, y1 = rect
        r[y0:y1, x0:x1] = True
        sel &= r
    sel &= (L >= Lr[0]) & (L <= Lr[1])
    if cmax is not None:
        sel &= C <= cmax
    n = int(sel.sum())
    if n < 20:
        return dict(n_px=n, error="too few pixels")
    rgb = bgr[sel][:, ::-1].astype(float)
    med = np.median(rgb, axis=0)
    lin = srgb_to_linear(med)
    Y = srgb_to_linear(rgb) @ np.array([0.2126, 0.7152, 0.0722])
    p50, p99 = np.percentile(Y, 50), np.percentile(Y, 99)
    spec = float((p99 - p50) / max(p99, 1e-4))
    thr = p50 + 0.5 * (p99 - p50)
    share = float(np.mean(Y > thr))
    rough = float(np.clip(0.15 + 2.5 * share + 0.4 * (1.0 - spec), 0.08, 0.95))
    top = rgb[Y >= np.percentile(Y, 98)]
    tl = cv2.cvtColor(np.clip(top[None, :, ::-1], 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB)[0].astype(float)
    hchroma = float(np.median(np.hypot(tl[:, 1] - 128, tl[:, 2] - 128)))
    return dict(srgb_hex="#%02x%02x%02x" % tuple(int(round(v)) for v in med), linear_rgb=[round(float(v), 4) for v in lin],
                metallic=METALLIC[material], roughness=round(rough, 2), material=material, n_px=n,
                highlight_chroma=round(hchroma, 1), specular_contrast=round(spec, 3))


# --------------------------------------------------------------------------------------------
# Front-panel layouts
# --------------------------------------------------------------------------------------------
def ipg_layout():
    """IPG YLR-6000-U (4U) in the rack card photo: front-face corners and features picked on ipg_grid.png (photo px), mapped
    with a homography onto the 482.3 x 176.5 mm panel (u from the left ear, v down from the top)."""
    W, H = 482.3, 176.5
    src = np.float32([[50, 462], [700, 471], [700, 750], [50, 703]])
    dst = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    Hm = cv2.getPerspectiveTransform(src, dst)
    feats = {
        "LED POWER (green ring icon)": (113, 508), "LED EMISSION (triangle)": (115, 532), "LED ERROR (triangle)": (115, 552),
        "IPG logo, left end": (207, 492), "IPG logo, right end": (300, 510),
        "light panel: bottom edge at the left": (50, 630), "light panel: curve meets the top band": (300, 482),
        "light top band: lower edge at the right end": (690, 488),
        "blue swoosh: lower-left end": (350, 671), "blue swoosh: knee": (427, 582), "blue swoosh: right end (mid-line)": (700, 584),
        "model label box: top-left": (400, 590), "model label box: bottom-right": (637, 660),
        "left handle: top": (40, 494), "left handle: bottom": (40, 680), "right handle: top": (653, 508), "right handle: bottom": (653, 730),
    }
    out = {}
    for k, (x, y) in feats.items():
        p = cv2.perspectiveTransform(np.float32([[[x, y]]]), Hm)[0, 0]
        out[k] = dict(u_mm=round(float(p[0]), 1), v_mm=round(float(p[1]), 1), u_frac=round(float(p[0] / W), 3), v_frac=round(float(p[1] / H), 3))
    return dict(photo="ipg_rack_card", panel_mm=[W, H], note="handles stand proud of the panel, so their rectified u, v carry a parallax error of a few mm; "
                "the YLR-6000-U's 4U chassis styling is assumed to match the YLR-500-U3-SM", features=out)


def eaton_layout():
    """Eaton 5PX G2 front (orthographic view in the datasheet): object bbox x 40-459, y 209-290 px; features picked on eaton_grid.png."""
    x0, y0, w, h = 40.0, 209.0, 419.0, 81.0
    feats = {"perforated grille (silver, staggered round holes)": (43, 215, 361, 287), "Eaton badge (light grey)": (81, 237, 110, 264),
             "display module (black)": (362, 211, 458, 289), "LCD screen": (390, 219, 432, 262), "button row (5 keys: ESC, alarm, down, enter, power)": (383, 270, 442, 278),
             "status light bar (blue)": (381, 281, 447, 286), "green LED": (391, 222, 395, 226)}
    out = {}
    for k, (a, b, c, d) in feats.items():
        out[k] = dict(u0=round((a - x0) / w, 3), u1=round((c - x0) / w, 3), v0=round((b - y0) / h, 3), v1=round((d - y0) / h, 3))
    return dict(photo="eaton_front", frame="fractions of the front bezel's visible width (u, from the left) and height (v, from the top); "
                "bezel 419 x 81 px = 5.17:1 (datasheet body 436.88 x 86.36 = 5.06:1)", features=out)


# --------------------------------------------------------------------------------------------
# Silhouette fitting
# --------------------------------------------------------------------------------------------
TAG = os.environ.get("OEM_FIT_TAG", "")      # e.g. "_before": results go to fits_before and overlay_<key>_before.png


def model_mesh(key, **kw):
    """Tessellated builder. $OEM_VP names another vendor_parts.py (e.g. the one before a refinement, for 'before' fits);
    a builder without an 'ears' option is called with bodies=True and its rack ears dropped."""
    sys.path.insert(0, str(CAD))
    if os.environ.get("OEM_VP"):
        import importlib.util
        spec = importlib.util.spec_from_file_location("vp_alt", os.environ["OEM_VP"])
        VPm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(VPm)
    else:
        import vendor_parts as VPm
    try:
        s = getattr(VPm, key)(**kw)
    except TypeError:
        kw2 = {k: v for k, v in kw.items() if k != "ears"}
        d = getattr(VPm, key)(bodies=True, **kw2)
        d.pop("rack_ears", None)
        s = VPm._fuse(list(d.values()))
    vs, ts = s.tessellate(0.6, 0.6)
    return np.array([(v.x, v.y, v.z) for v in vs]), np.array(ts, dtype=np.int64)


def axes_to_rvec(zc, yc):
    """Rotation whose columns are the model axes expressed in camera coordinates: model z -> zc, model y -> ~yc."""
    z = np.asarray(zc, float); z /= np.linalg.norm(z)
    y = np.asarray(yc, float); y -= z * (y @ z); y /= np.linalg.norm(y)
    x = np.cross(y, z)
    R = np.stack([x, y, z], axis=1)
    return cv2.Rodrigues(R)[0].ravel()


def project(V, p, cxy):
    R = cv2.Rodrigues(np.asarray(p[:3], float))[0]
    Xc = V @ R.T + p[3:6]
    f = math.exp(p[6])
    z = np.maximum(Xc[:, 2], 1.0)
    return np.stack([f * Xc[:, 0] / z + cxy[0], f * Xc[:, 1] / z + cxy[1]], axis=1)


def silhouette(V, T, p, shape, cxy):
    R = cv2.Rodrigues(np.asarray(p[:3], float))[0]
    zc = V @ R[2] + p[5]
    if zc.min() < 0.3 * zc.mean() or not (5.0 < p[6] < 10.5):    # model near/behind the camera, or f outside 150-36000 px
        return None
    P = project(V, p, cxy)
    img = np.zeros(shape, np.uint8)
    pts = np.round(P[T] * 4).astype(np.int32)
    for tri in pts:            # one call per triangle: cv2.fillPoly on a list uses even-odd filling, so overlaps would cancel
        cv2.fillConvexPoly(img, tri, 1, lineType=cv2.LINE_8, shift=2)
    return img


def iou(a, b):
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 0.0


def fit(V, T, mask, p0, fixed_f=None, iters=900, restarts=4, seed=0, scale=0.5):
    """Maximise IoU over pose (+ log f unless fixed). Works on a downscaled mask; returns (params, IoU at full resolution)."""
    h, w = mask.shape
    ms = cv2.resize(mask, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_NEAREST).astype(bool)
    cxy_s = ((w * scale) / 2.0, (h * scale) / 2.0)

    def unpack(q):
        p = np.array(q, float)
        if fixed_f is not None:
            p = np.concatenate([p, [math.log(fixed_f)]])
        return p

    def cost(q):
        p = unpack(q).copy()
        p[6] += math.log(scale)
        sil = silhouette(V, T, p, ms.shape, cxy_s)
        return 1.0 if sil is None else 1.0 - iou(sil.astype(bool), ms)

    rng = np.random.default_rng(seed)
    q0 = np.array(p0[:6] if fixed_f is not None else p0, float)
    best = (cost(q0), q0)
    for k in range(restarts):
        qs = best[1].copy()
        if k:
            qs[:3] += rng.normal(0, 0.06, 3)
            qs[3:5] += rng.normal(0, 0.02, 2) * qs[5]
        step = np.array([0.05, 0.05, 0.05, 0.02 * qs[5], 0.02 * qs[5], 0.05 * qs[5]] + ([] if fixed_f is not None else [0.15]))
        simplex = np.vstack([qs] + [qs + np.eye(len(qs))[i] * step[i] for i in range(len(qs))])
        r = minimize(cost, qs, method="Nelder-Mead", options=dict(maxiter=iters, initial_simplex=simplex, xatol=1e-5, fatol=1e-6))
        if r.fun < best[0]:
            best = (r.fun, r.x)
    p = unpack(best[1])
    full = silhouette(V, T, p, mask.shape, (w / 2.0, h / 2.0)).astype(bool)
    return p, iou(full, mask.astype(bool)), full


def contour_dist(a, b):
    """Symmetric mean distance (px) between the outlines of masks a and b."""
    def edge(m):
        m = m.astype(np.uint8)
        return (m - cv2.erode(m, np.ones((3, 3), np.uint8))).astype(bool)
    ea, eb = edge(a), edge(b)
    da = cv2.distanceTransform((~eb).astype(np.uint8), cv2.DIST_L2, 5)
    db = cv2.distanceTransform((~ea).astype(np.uint8), cv2.DIST_L2, 5)
    return float(0.5 * (da[ea].mean() + db[eb].mean())), float(max(np.percentile(da[ea], 95), np.percentile(db[eb], 95)))


FITS = {   # photo id -> (builder key, builder kwargs, model z axis in camera coords, model y axis in camera coords, sensor note)
    "teknic_cpm231": ("clearpath_sd_231x", {}, (-0.85, 0.08, -0.52), (0.0, -1.0, 0.0)),
    "mcm_4123K45": ("mcm_4123K45", {"handle": "-x"}, (0.0, -1.0, 0.25), (0.25, 0.0, -1.0)),
    # round 6 (2026-11-25)
    "eaton_r_2k": ("eaton_5px1500rtg2", {"ears": False}, (0.0, -0.94, -0.34), (-0.3, 0.1, 0.95)),
    "mcm_5169K72": ("mcm_5169K72", {}, (0.0, -0.95, -0.3), (1.0, 0.0, 0.0)),
    "mcm_3861N11": ("mcm_3861N11", {}, (-0.9, -0.2, 0.3), (0.0, 1.0, 0.0)),
}


def run_fit(pid):
    key, kw, zc, yc = FITS[pid]
    bgr, mask = load(PH / PHOTOS[pid][1], pid)
    h, w = mask.shape
    V, T = model_mesh(key, **kw)
    from scipy.spatial.transform import Rotation as Rot
    ys, xs = np.nonzero(mask)
    mb = np.array([xs.min(), ys.min(), xs.max(), ys.max()], float)
    sc = 0.25
    msmall = cv2.resize(mask, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_NEAREST).astype(bool)
    f0 = 2500.0
    c = V.mean(axis=0)
    cands = []
    rots = list(Rot.random(400, random_state=7).as_rotvec()) + [axes_to_rvec(zc, yc)]
    for rv in rots:
        R = cv2.Rodrigues(np.asarray(rv, float))[0]
        Vc = (V - c) @ R.T
        D = f0 * np.ptp(V, axis=0).max() / max(np.ptp(xs), np.ptp(ys))
        for _ in range(2):                        # match the bbox size, then its centre (weak perspective)
            z = Vc[:, 2] + D
            u, v = f0 * Vc[:, 0] / z, f0 * Vc[:, 1] / z
            k = math.hypot(np.ptp(u), np.ptp(v)) / math.hypot(mb[2] - mb[0], mb[3] - mb[1])
            D *= k
        z = Vc[:, 2] + D
        u, v = f0 * Vc[:, 0] / z, f0 * Vc[:, 1] / z
        du = (mb[0] + mb[2]) / 2 - w / 2 - (u.min() + u.max()) / 2
        dv = (mb[1] + mb[3]) / 2 - h / 2 - (v.min() + v.max()) / 2
        t = np.array([du * D / f0, dv * D / f0, D]) - R @ c
        p0 = np.concatenate([np.asarray(rv, float), t, [math.log(f0)]])
        q = p0.copy(); q[6] += math.log(sc)
        sil = silhouette(V, T, q, msmall.shape, (w * sc / 2, h * sc / 2))
        if sil is not None:
            cands.append((iou(sil.astype(bool), msmall), p0))
    cands.sort(key=lambda a: -a[0])
    print(pid, "global search: best coarse IoU", [round(a[0], 3) for a in cands[:6]], flush=True)
    best = None
    for s0, p0 in cands[:3]:
        p, s, sil = fit(V, T, mask, p0, iters=300, restarts=1, scale=0.3)
        if best is None or s > best[1]:
            best = (p, s, sil)
    p, s, sil = best
    p, s, sil = fit(V, T, mask, p, iters=400, restarts=2, seed=2, scale=0.5)
    f = math.exp(p[6])
    prof = []
    for ff in (0.4, 0.7, 1.0, 1.5, 2.5):
        fx = f * ff
        q = p.copy()
        R = cv2.Rodrigues(q[:3])[0]
        c = R @ V.mean(axis=0) + q[3:6]
        q[3:6] = q[3:6] + c * (ff - 1.0) * np.array([1, 1, 1])        # move along the line of sight to keep the image size
        qq, si, _ = fit(V, T, mask, q, fixed_f=fx, iters=250, restarts=1, seed=3, scale=0.3)
        prof.append(dict(f_px=round(fx, 1), iou=round(si, 4)))
    sil = silhouette(V, T, p, mask.shape, (w / 2.0, h / 2.0)).astype(bool)
    md, p95 = contour_dist(sil, mask.astype(bool))
    R = cv2.Rodrigues(p[:3])[0]
    zc_obj = float((R @ V.mean(axis=0) + p[3:6])[2])
    mm_per_px = zc_obj / f
    diag = math.hypot(w, h)
    res = dict(photo=pid, builder=key, kwargs=kw, image_px=[w, h], iou=round(s, 4), f_px=round(f, 1),
               f_35mm_equiv_mm=round(f * 43.27 / diag, 1), principal_point="image centre (assumed)", rvec=[round(float(v), 4) for v in p[:3]],
               t_mm=[round(float(v), 1) for v in p[3:6]], object_distance_mm=round(zc_obj, 1), mm_per_px_at_object=round(mm_per_px, 4),
               contour_mean_px=round(md, 2), contour_p95_px=round(p95, 2), contour_mean_mm=round(md * mm_per_px, 2),
               f_profile=prof, mask_px=int(mask.sum()), model_px=int(sil.sum()))
    # committed overlay: outlines only (no photo pixels)
    can = np.full((h, w, 3), 255, np.uint8)
    po, mo = mask.astype(bool), sil
    can[po & ~mo] = (190, 215, 250)        # photo only: light orange
    can[mo & ~po] = (250, 225, 190)        # model only: light blue
    can[po & mo] = (235, 235, 235)
    for m, col in ((po, (0, 110, 230)), (mo, (200, 80, 0))):
        cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(can, cs, -1, col, 2)
    txt = [f"{key}: silhouette IoU {s:.3f}, f = {f:.0f} px ({res['f_35mm_equiv_mm']:.0f} mm equiv.)",
           f"outline distance mean {md:.1f} px ({md * mm_per_px:.2f} mm), p95 {p95:.1f} px",
           "orange = vendor photo mask outline, blue = vendor_parts model silhouette"]
    for i, tline in enumerate(txt):
        cv2.putText(can, tline, (10, 22 + 22 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 40, 40), 1, cv2.LINE_AA)
    sc = min(1.0, 900.0 / w)
    small = cv2.resize(can, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA)
    OUT.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT / f"overlay_{key}{TAG}.png"), small, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    # full overlay for viewing (photo pixels: /tmp only)
    OV.mkdir(parents=True, exist_ok=True)
    ov = bgr.copy()
    ov[mo] = (0.6 * ov[mo] + 0.4 * np.array([255, 140, 0])).astype(np.uint8)
    cs, _ = cv2.findContours(mo.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ov, cs, -1, (255, 60, 0), 2)
    cs, _ = cv2.findContours(po.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ov, cs, -1, (0, 140, 255), 1)
    cv2.imwrite(str(OV / f"photo_overlay_{key}{TAG}.jpg"), ov)
    print(json.dumps({k: res[k] for k in ("photo", "iou", "f_px", "f_35mm_equiv_mm", "contour_mean_px", "contour_mean_mm")}), flush=True)
    return res


# --------------------------------------------------------------------------------------------
def manifest():
    old = {}
    if (HERE / "photo-manifest.csv").exists():
        with open(HERE / "photo-manifest.csv", newline="") as fh:
            old = {r["id"]: r for r in csv.DictReader(fh)}
    rows = []
    for pid, (key, rel, vendor, url, note) in PHOTOS.items():
        f = PH / rel
        if not f.exists():
            if pid in old:                      # fetched in an earlier round and not in /tmp now: keep its row
                rows.append(old[pid])
            continue
        if url is None:
            idx = json.loads((f.parent / "index.json").read_text())
            url = next(i["src"] for i in idx["imgs"] if i.get("file") == f.name)
        im = cv2.imread(str(f), cv2.IMREAD_UNCHANGED)
        rows.append(dict(id=pid, part=key, vendor=vendor, url=url, sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                         px=f"{im.shape[1]}x{im.shape[0]}", fetched_utc=datetime.datetime.fromtimestamp(f.stat().st_mtime, datetime.UTC).strftime("%Y-%m-%dT%H:%MZ"),
                         note=note))
    rows += [r for k, r in old.items() if k not in PHOTOS]     # rows added by hand (the product videos of video_recon.py)
    with open(HERE / "photo-manifest.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def finishes():
    out = json.loads((HERE / "finishes.json").read_text()) if (HERE / "finishes.json").exists() else {}   # keeps earlier rounds'
    for pid, regs in REGIONS.items():
        key, rel = PHOTOS[pid][0], PHOTOS[pid][1]
        if not (PH / rel).exists():
            continue
        if pid in RECT_ONLY:
            bgr, mask = cv2.imread(str(PH / rel))[:, :, :3], None
            mask = np.ones(bgr.shape[:2], np.uint8)
        else:
            bgr, mask = load(PH / rel, pid)
        for body, rect, Lr, cmax, mat in regs:
            r = measure(bgr, mask, rect, Lr, cmax, mat)
            r.update(photo=pid, method=("median of the pixels in a hand-picked rectangle" if rect else "median over the whole object mask")
                     + f", L* {Lr[0]}-{Lr[1]}" + (f", chroma <= {cmax}" if cmax else ""))
            out.setdefault(key, {})[body] = r
    (HERE / "finishes.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["manifest", "finishes", "layouts", "fits"]
    res = json.loads((OUT / "photo_fit.json").read_text()) if (OUT / "photo_fit.json").exists() else {}
    if "manifest" in what:
        print(len(manifest()), "photos in photo-manifest.csv")
    if "finishes" in what:
        for k, v in finishes().items():
            for b, r in v.items():
                print(f"{k:22s} {b:50s} {r.get('srgb_hex')} lin {r.get('linear_rgb')} m {r.get('metallic')} r {r.get('roughness')} n {r.get('n_px')}")
    if "layouts" in what or not res.get("layouts"):
        res["layouts"] = dict(ipg_ylr500_u3=ipg_layout(), eaton_5px1500rtg2=eaton_layout())
    if "fits" in what:
        sel = [a for a in what if a in FITS] or list(FITS)
        old = {r["photo"]: r for r in res.get("fits", [])}
        for pid in sel:
            r = run_fit(pid)
            cur = json.loads((OUT / "photo_fit.json").read_text()) if (OUT / "photo_fit.json").exists() else res
            old = {q["photo"]: q for q in cur.get("fits" + TAG, [])}
            old[pid] = r
            cur["fits" + TAG] = [old[k] for k in FITS if k in old]
            cur.setdefault("layouts", res.get("layouts"))
            (OUT / "photo_fit.json").write_text(json.dumps(cur, indent=1))
            res = cur
    OUT.mkdir(parents=True, exist_ok=True)
    if "fits" not in what:
        (OUT / "photo_fit.json").write_text(json.dumps(res, indent=1))
