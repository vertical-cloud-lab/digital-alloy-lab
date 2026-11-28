"""Photo and video-frame measurements of the stock collection cup and its joint to the cone (issue 269).

Re-run:  python measure.py --photos <dir with the 4K photos and WhatsApp media> --frames <dir with video frames> [--fetch]

Inputs (not committed; the 4K photos are on issue 269, the WhatsApp media in the Nov 13 run record, the frames are
pulled from the lab's YouTube videos with --fetch, which needs yt-dlp and a route YouTube accepts):
  image-1795800846973-1.jpg   4K, Nov 17: cracked glass, guard, bottom plate + tie rods, 18 mm wrench
  image-1795800846956-0.jpg   4K, Nov 17: looking down the cup's top flange with the centring ring removed
  04-...cup_in_hand.jpg       WhatsApp, Nov 16: cup top with the KF centring ring and O-ring in place
  frames: tfb4fsVNIFI@42s, 1F9_4ccwhss@545s, 58wJ_Khwgyk@179s (see FRAMES)

What is automatic and what is read by hand:
  * ellipse fits (OpenCV fitEllipse inside RANSAC, on edge points found along rays from a guessed centre) for the
    flange, O-ring and centring-ring edges in photo 04 and for the bottom plate's outer edge in the 4K photo;
  * pixel readings taken off gridded zoom crops (wrench box-end opening, tie-rod width, glass silhouette, gasket band,
    plate rim) are the constants in READ below, each with the crop it came from.
Ratios of concentric circles in one plane carry the size; the scale comes from one standard part in the same plane.
"""
import argparse, json, math, os, subprocess, sys
import numpy as np
import cv2
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")

# ---------------------------------------------------------------------------------------------- standards (mm)
KF_FLANGE_OD = {"KF-25": 40.0, "KF-40": 55.0, "KF-50": 75.0}
# PNEUROP 6606 / ISO 2861 centring-ring O-rings, ID x cross-section (Precision Polymer Engineering's KF table)
KF_ORING = {"KF-25": (28.0, 5.0), "KF-40": (42.0, 5.0), "KF-50": (55.0, 5.0)}
ISO_K63 = dict(flange_od=95.0, oring=(75.57, 5.0))
WRENCH_BOX_OPENING = 18.3      # 18 mm 12-point box end: 18.0 across flats, 18.6 across points; mean of the contour

# ------------------------------------------------------------------------------- manual pixel readings (px)
# 4K photo image-1795800846973-1.jpg after EXIF rotation (3840 x 2160). Each read off a gridded zoom crop.
READ = dict(
    box_opening_major=154.0,  box_opening_major_pm=15.0,   # right end x=2684; left end hidden by a rod; the
                                                           # visible half (x 2563-2684, y 405-527) with the plate's
                                                           # axis ratio gives ~154 px along the major axis
    rod_FL_width=107.0, rod_FL_width_pm=8.0,               # front-left rod just above its nut, x 2230-2337 at y 1260
    nut_FL_silhouette=174.0,                               # same nut, x 2183-2357 (between AF and AC)
    glass_bottom_width=859.0, glass_bottom_width_pm=12.0,  # glass silhouette near the table, x 1145-2004 at y 1700
    glass_top_width=1078.0,                                # top rim outer silhouette, x 1013-2091
    glass_top_back_y=441.0, glass_top_front_y=1332.0,      # top rim ellipse, back and front outer edges
    glass_bottom_front_y=1795.0,
    glass_wall_top=64.0, glass_wall_top_pm=10.0,           # rim seen edge-on at its left extreme, x 1010-1074 at y 900
    gasket_band_outer=931.0, gasket_band_inner=794.0, gasket_pm=15.0,   # black gasket band, horizontal extents
    plate_rim_band=32.0, plate_rim_band_pm=8.0,            # chamfer + side of the plate at the front, y 1880-1912
    nut_rim_gap_mm=3.5, nut_rim_gap_pm=1.5,                # each plate nut's outer face sits 2-5 mm inside the rim
)
# Nov 13 cleaning video (boWsO0rxHvU) at 8:02, the cup upright on the bench seen obliquely from above (1280 x 720)
READ_BW = dict(kf_width=472.0, kf_face_minor=185.0, kf_face_yc=244.0,      # KF top face: x 503-975, y 152-335
               valve_flange_width=650.0, valve_flange_yc=540.0, pm=12.0,   # 4-bolt flange under the reducer
               reducer_large_width=390.0, reducer_depth_factor=0.95,      # reducer's large end, x 525-915
               depth_factor=0.93)                                          # lower flange ~7 % farther away (estimate)
# training video 6 (tfb4fsVNIFI) at 0:40, low side view of the lower half (1280 x 720 frame)
READ_T6 = dict(plate_width=560.0, guard_width=380.0, guard_height=393.0, pm=15.0)   # x 220-780; x 313-693; y 227-620
# depth correction: the glass's bottom centre sits ~19 mm nearer the camera than the plate centre (about 3 %)
GLASS_DEPTH_FACTOR = 1.03

FRAMES = {  # id, seconds, crop box (x0, y0, x1, y1) on the 1280 x 720 frame; crops are hardware only (no faces)
    "t6_container_side": ("tfb4fsVNIFI", 40, (0, 0, 1280, 720)),
    "t4_joint_mounted": ("1F9_4ccwhss", 545, (300, 230, 1000, 720)),
    "t5_cone_shield": ("58wJ_Khwgyk", 179, (300, 120, 1000, 720)),
    "t5_shield_in_hand": ("58wJ_Khwgyk", 135, (470, 420, 900, 720)),
    "t5_container_profile": ("58wJ_Khwgyk", 34, (500, 140, 1010, 600)),
    "bw_cup_top_bench": ("boWsO0rxHvU", 482, (380, 100, 1110, 720)),
}


def load(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def ray_points(ch, guess, band, n=360, sign=0, smooth=1.5, arc=(0, 360)):
    """Edge points along rays from a guessed ellipse's centre: on each ray, the largest radial derivative within
    +-band of the guess (sign>0 dark->bright going outward, sign<0 bright->dark, 0 either)."""
    (cx, cy), (A, B), ang = guess
    a, b, th = A / 2, B / 2, math.radians(ang)
    g = cv2.GaussianBlur(ch.astype(np.float32), (0, 0), smooth)
    pts = []
    for t in np.linspace(math.radians(arc[0]), math.radians(arc[1]), n, endpoint=False):
        d = np.array([math.cos(t), math.sin(t)])
        dl = np.array([d[0] * math.cos(th) + d[1] * math.sin(th), -d[0] * math.sin(th) + d[1] * math.cos(th)])
        rg = 1.0 / math.sqrt((dl[0] / a) ** 2 + (dl[1] / b) ** 2)
        rs = np.arange(rg * (1 - band), rg * (1 + band), 0.5)
        xs, ys = cx + rs * d[0], cy + rs * d[1]
        ok = (xs > 1) & (ys > 1) & (xs < ch.shape[1] - 2) & (ys < ch.shape[0] - 2)
        if ok.sum() < 10:
            continue
        xs, ys = xs[ok], ys[ok]
        v = cv2.remap(g, xs.astype(np.float32).reshape(1, -1), ys.astype(np.float32).reshape(1, -1),
                      cv2.INTER_LINEAR).ravel()
        dv = np.gradient(v)
        k = int(np.argmax(dv) if sign > 0 else np.argmin(dv) if sign < 0 else np.argmax(np.abs(dv)))
        pts.append((xs[k], ys[k]))
    return np.array(pts, np.float32)


def resid(P, e):
    (cx, cy), (A, B), ang = e
    a, b, th = A / 2, B / 2, math.radians(ang)
    x, y = P[:, 0] - cx, P[:, 1] - cy
    xr, yr = x * math.cos(th) + y * math.sin(th), -x * math.sin(th) + y * math.cos(th)
    rho = np.sqrt(xr ** 2 + yr ** 2) + 1e-9
    return rho - 1.0 / np.sqrt((xr / rho / a) ** 2 + (yr / rho / b) ** 2)


def fit_ransac(P, tol=2.0, iters=1500, seed=0):
    rng = np.random.default_rng(seed)
    best, bestin = None, None
    for _ in range(iters):
        try:
            e = cv2.fitEllipse(P[rng.choice(len(P), 6, replace=False)])
        except cv2.error:
            continue
        inl = np.abs(resid(P, e)) < tol
        if bestin is None or inl.sum() > bestin.sum():
            best, bestin = e, inl
    e = cv2.fitEllipse(P[bestin])
    return e, bestin, float(np.sqrt(np.mean(resid(P[bestin], e) ** 2)))


def fit_iter(ch, guess, band, sign, arc=(0, 360), tol=2.0, smooth=1.5, n=360):
    e = guess
    for _ in range(3):
        P = ray_points(ch, e, band, n=n, sign=sign, smooth=smooth, arc=arc)
        e, inl, rms = fit_ransac(P, tol=tol)
        band = max(band * 0.6, 0.015)
    return e, int(inl.sum()), len(P), rms


def major(e):
    return max(e[1])


def minor(e):
    return min(e[1])


def draw(img, e, col, t=2):
    (cx, cy), (A, B), ang = e
    cv2.ellipse(img, ((float(cx), float(cy)), (float(A), float(B)), float(ang)), col, t, cv2.LINE_AA)


def label(img, txt, xy, col=(255, 255, 255), s=0.8, t=2):
    cv2.putText(img, txt, xy, cv2.FONT_HERSHEY_SIMPLEX, s, (0, 0, 0), t + 3, cv2.LINE_AA)
    cv2.putText(img, txt, xy, cv2.FONT_HERSHEY_SIMPLEX, s, col, t, cv2.LINE_AA)


def save_jpg(img, name, max_w=1400, max_kb=195):
    if img.shape[1] > max_w:
        img = cv2.resize(img, (max_w, int(img.shape[0] * max_w / img.shape[1])), interpolation=cv2.INTER_AREA)
    os.makedirs(IMG, exist_ok=True)
    for q in (88, 80, 72, 64, 56, 48):
        ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, q])
        if len(buf) < max_kb * 1024:
            break
    open(os.path.join(IMG, name), "wb").write(buf.tobytes())


# ------------------------------------------------------------------------------------------------ photo 04: KF size
def kf_size(path):
    img = load(path)
    b, g, r = [c.astype(np.float32) for c in cv2.split(img)]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    red = (r - b) * 2 + 128          # the brown O-ring stands out in R - B
    C = (365, 540)
    specs = {  # name: channel, guess axes, band, sign, arc (the flange skips the lower right: lever and a nut)
        "flange_od": (gray, (505, 488), 0.05, 0, (180, 400)),
        "oring_od": (red, (419, 405), 0.05, -1, (0, 360)),
        "oring_inner_visible": (red, (372, 360), 0.05, +1, (0, 360)),
        "ring_bore": (gray, (319, 308), 0.06, +1, (0, 360)),
    }
    fits = {}
    for k, (ch, ax, band, sign, arc) in specs.items():
        fits[k] = fit_iter(ch, (C, ax, 0), band, sign, arc, tol=1.5, smooth=1.2)
    F = major(fits["flange_od"][0])
    ratios = {k: major(v[0]) / F for k, v in fits.items()}
    cand = {}
    for name, od in KF_FLANGE_OD.items():
        oid, cs = KF_ORING[name]
        cand[name] = (oid + 2 * cs) / od
    cand["ISO-K 63"] = (ISO_K63["oring"][0] + 2 * ISO_K63["oring"][1]) / ISO_K63["flange_od"]
    dbg = img.copy()
    cols = {"flange_od": (255, 80, 0), "oring_od": (0, 230, 0), "oring_inner_visible": (0, 230, 255),
            "ring_bore": (255, 0, 255)}
    for k, (e, *_r) in fits.items():
        draw(dbg, e, cols[k], 2)
    crop = dbg[250:830, 60:680].copy()
    crop = cv2.resize(crop, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
    y = 34
    for k in fits:
        label(crop, f"{k}: {ratios[k]:.3f} x flange", (12, y), cols[k], 0.75, 2)
        y += 32
    label(crop, f"O-ring OD/flange OD {ratios['oring_od']:.3f}: KF-50 {cand['KF-50']:.3f}, KF-40 {cand['KF-40']:.3f}",
          (12, crop.shape[0] - 20), (255, 255, 255), 0.7, 2)
    save_jpg(crop, "01_photo04_kf50_ellipses.jpg", max_w=990)
    return fits, ratios, cand


# ------------------------------------------------------------------------------------- 4K photo: bottom plate, glass
def plate_and_glass(path):
    img = load(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    e, nin, n, rms = fit_iter(gray, ((2835, 1300), (1450, 1200), 0), 0.035, 0, tol=3.0, smooth=2.0, n=720)
    P = major(e)
    tilt = math.degrees(math.acos(minor(e) / P))
    R = READ
    s_wrench = R["box_opening_major"] / WRENCH_BOX_OPENING            # px/mm behind the plate
    s_rod12 = R["rod_FL_width"] / 12.0                                 # px/mm in front of it, if the rods are 12 mm
    s_plate = 0.5 * (s_wrench + s_rod12)
    s_pm = max(abs(s_wrench - s_rod12) / 2, s_plate * 0.05)
    out = dict(plate_major_px=P, plate_minor_px=minor(e), plate_fit_rms_px=rms, plate_inliers=f"{nin}/{n}",
               view_tilt_deg=tilt, scale_wrench_px_per_mm=s_wrench, scale_rod12_px_per_mm=s_rod12,
               scale_plate_px_per_mm=s_plate, scale_pm=s_pm)
    out["plate_od"] = P / s_plate
    out["plate_od_pm"] = out["plate_od"] * math.hypot(s_pm / s_plate, 0.01)
    out["rod_d_from_wrench"] = R["rod_FL_width"] / s_wrench
    out["rod_d_pm"] = out["rod_d_from_wrench"] * math.hypot(R["box_opening_major_pm"] / R["box_opening_major"],
                                                            R["rod_FL_width_pm"] / R["rod_FL_width"])
    out["nut_silhouette_over_rod"] = R["nut_FL_silhouette"] / R["rod_FL_width"]
    ratio_g = R["glass_bottom_width"] / (GLASS_DEPTH_FACTOR * P)
    out["glass_od_over_plate"] = ratio_g
    out["glass_od"] = ratio_g * out["plate_od"]
    out["glass_od_pm"] = out["glass_od"] * math.hypot(out["plate_od_pm"] / out["plate_od"], 0.02)
    out["glass_wall"] = R["glass_wall_top"] / R["glass_top_width"] * out["glass_od"]
    out["glass_wall_pm"] = out["glass_wall"] * math.hypot(R["glass_wall_top_pm"] / R["glass_wall_top"], 0.08)
    # glass length from the two rim ellipses (weak-perspective): h/OD = dy / (mean major * sin(tilt)).
    # LOW CONFIDENCE: the top rim is ~25 % nearer the camera than the bottom, which this model ignores.
    top_minor = R["glass_top_front_y"] - R["glass_top_back_y"]
    gt = math.acos(top_minor / R["glass_top_width"])
    yc_top = 0.5 * (R["glass_top_front_y"] + R["glass_top_back_y"])
    yc_bot = R["glass_bottom_front_y"] - 0.5 * R["glass_bottom_width"] * top_minor / R["glass_top_width"]
    mean_major = 0.5 * (R["glass_top_width"] + R["glass_bottom_width"])
    out["glass_len_over_od"] = (yc_bot - yc_top) / (mean_major * math.sin(gt))
    out["glass_len"] = out["glass_len_over_od"] * out["glass_od"]
    out["gasket_band_od"] = R["gasket_band_outer"] / P * out["plate_od"]
    out["gasket_band_id"] = R["gasket_band_inner"] / P * out["plate_od"]
    out["bolt_circle"] = out["plate_od"] - 2 * (18.0 / 2 / math.cos(math.radians(15)) + R["nut_rim_gap_mm"])
    out["bolt_circle_pm"] = math.hypot(out["plate_od_pm"], 2 * R["nut_rim_gap_pm"])
    T6 = READ_T6
    out["guard_od_t6"] = T6["guard_width"] / T6["plate_width"] * out["plate_od"]
    out["guard_h_t6"] = T6["guard_height"] / T6["plate_width"] * out["plate_od"]
    B = READ_BW
    s_kf = B["kf_width"] / 75.0
    tilt_kf = math.acos(B["kf_face_minor"] / B["kf_width"])
    out["valve_flange_od"] = B["valve_flange_width"] / (s_kf * B["depth_factor"])
    out["kf_face_to_valve_flange_top"] = (B["valve_flange_yc"] - B["kf_face_yc"]) / (math.sin(tilt_kf) * s_kf * (1 + B["depth_factor"]) / 2)
    out["reducer_large_od"] = B["reducer_large_width"] / (s_kf * B["reducer_depth_factor"])
    out["plate_rim_t"] = R["plate_rim_band"] / math.sin(math.radians(tilt)) / (s_plate * 1.03)
    out["plate_rim_t_pm"] = out["plate_rim_t"] * math.hypot(R["plate_rim_band_pm"] / R["plate_rim_band"], 0.06)
    # annotated crops
    dbg = img.copy()
    draw(dbg, e, (255, 80, 0), 4)
    cv2.line(dbg, (2230, 1260), (2337, 1260), (0, 255, 255), 4)
    cv2.line(dbg, (2394, 1250), (3325, 1250), (0, 230, 0), 3)
    cv2.line(dbg, (2475, 1290), (3269, 1290), (0, 160, 255), 3)
    c = dbg[560:2080, 1950:3780].copy()
    label(c, f"plate OD fit: major {P:.0f} px -> {out['plate_od']:.0f} +- {out['plate_od_pm']:.0f} mm", (30, 60),
          (255, 160, 60), 1.4, 3)
    label(c, f"rod {R['rod_FL_width']:.0f} px -> {out['rod_d_from_wrench']:.1f} mm (wrench scale)", (30, 115),
          (0, 255, 255), 1.4, 3)
    label(c, f"gasket band {out['gasket_band_od']:.0f} / {out['gasket_band_id']:.0f} mm", (30, 170), (0, 230, 0), 1.4, 3)
    save_jpg(c, "02_k1_bottom_plate_fit.jpg", max_w=1200)
    c = img[300:640, 2470:2800].copy()
    cv2.circle(c, (2684 - 2470, 495 - 300), 6, (0, 0, 255), -1)
    cv2.line(c, (2530 - 2470, 495 - 300), (2684 - 2470, 495 - 300), (0, 255, 255), 2)
    label(c, "18 mm box end: ~154 px", (8, 30), (0, 255, 255), 0.8, 2)
    save_jpg(c, "03_k1_wrench_box_end.jpg", max_w=660)
    g = img.copy()
    cv2.line(g, (1013, 900), (2091, 900), (255, 160, 60), 4)
    cv2.line(g, (1145, 1700), (2004, 1700), (0, 230, 0), 4)
    cv2.line(g, (1010, 960), (1074, 960), (0, 255, 255), 6)
    c = g[250:1900, 880:2230].copy()
    label(c, f"top rim {R['glass_top_width']:.0f} px (nearer the camera)", (20, 50), (255, 160, 60), 1.3, 3)
    label(c, f"bottom {R['glass_bottom_width']:.0f} px -> OD {out['glass_od']:.0f} mm", (20, 1520), (0, 230, 0), 1.3, 3)
    label(c, f"wall {out['glass_wall']:.1f} mm", (20, 760), (0, 255, 255), 1.3, 3)
    save_jpg(c, "04_k1_glass_spans.jpg", max_w=1000)
    return out


def top_view(path):
    img = load(path)
    c = img[950:3500, 0:2160].copy()
    for txt, xy, col in [("KF-50 sealing face (centring ring removed)", (40, 230), (255, 160, 60)),
                         ("counterbore step for the ring's spigot", (40, 640), (0, 255, 255)),
                         ("burnt EPDM valve seat (white, ~20 mm tall)", (40, 1060), (255, 255, 255)),
                         ("splash plate: curved strip, notch at each end", (40, 1500), (0, 230, 0))]:
        label(c, txt, xy, col, 2.0, 4)
    save_jpg(c, "05_k0_top_view_annotated.jpg", max_w=800)


def frames(frames_dir):
    done = []
    for name, (vid, t, box) in FRAMES.items():
        p = os.path.join(frames_dir, f"{vid}_{t}.jpg")
        if not os.path.exists(p):
            print("missing frame", p, "(run with --fetch)")
            continue
        im = cv2.imread(p)
        x0, y0, x1, y1 = box
        c = im[y0:y1, x0:x1].copy()
        label(c, f"youtu.be/{vid}?t={t}", (10, c.shape[0] - 14), (255, 255, 255), 0.7, 2)
        save_jpg(c, f"{6 + len(done):02d}_{name}.jpg", max_w=1000)
        done.append(name)
    return done


def fetch(frames_dir, proxy=None):
    """Pull the single frames with yt-dlp + ffmpeg (720p is what these uploads offer)."""
    os.makedirs(frames_dir, exist_ok=True)
    for name, (vid, t, box) in FRAMES.items():
        mp4 = os.path.join(frames_dir, f"{vid}_{t}.mp4")
        cmd = ["yt-dlp", "-q", "-f", "bv*[height<=1080][ext=mp4]", "--download-sections", f"*{t}-{t + 2}",
               "-o", mp4, f"https://www.youtube.com/watch?v={vid}"]
        if proxy:
            cmd[1:1] = ["--proxy", proxy]
        subprocess.run(cmd, check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-frames:v", "1", "-q:v", "2",
                        os.path.join(frames_dir, f"{vid}_{t}.jpg")], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default="/tmp/github-images")
    ap.add_argument("--media", default="/tmp/an/atomizer-runs/2026-11-13/amazemet-chat/media")
    ap.add_argument("--frames", default="/tmp/meas/fr")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--proxy", default=None, help="http proxy for yt-dlp and ffmpeg (an http:// URL)")
    a = ap.parse_args()
    if a.fetch:
        fetch(a.frames, a.proxy)
    fits, ratios, cand = kf_size(os.path.join(a.media, "04-2026-11-16_1432_gage_photo2_cup_in_hand.jpg"))
    print("photo 04 (KF centring ring in place):")
    for k, (e, nin, n, rms) in fits.items():
        print(f"  {k:20s} major {major(e):6.1f} px  minor {minor(e):6.1f}  inliers {nin}/{n}  rms {rms:.2f} px"
              f"  ratio to flange {ratios[k]:.4f}")
    print("  O-ring OD / flange OD, nominal:", {k: round(v, 3) for k, v in cand.items()})
    r = ratios["oring_od"]
    print(f"  if KF-50 flange 75 mm: O-ring OD {75 * r:.1f}, visible O-ring inner edge {75 * ratios['oring_inner_visible']:.1f},"
          f" ring bore {75 * ratios['ring_bore']:.1f} mm")
    print(f"  if the O-ring is the standard 55 x 5 (OD 65): flange OD {65 / r:.1f} mm")
    pg = plate_and_glass(os.path.join(a.photos, "image-1795800846973-1.jpg"))
    print("4K photo (bottom plate, glass, wrench):")
    for k, v in pg.items():
        print(f"  {k:28s} {v:.3f}" if isinstance(v, float) else f"  {k:28s} {v}")
    top_view(os.path.join(a.photos, "image-1795800846956-0.jpg"))
    print("frames:", frames(a.frames))


if __name__ == "__main__":
    main()
