"""Multi-view reconstruction of the Teknic ClearPath from Teknic's own product video (issue #260, round 6, 2026-11-25).

Video: Teknic, "ClearPath: Teknic's Integrated Brushless Servo Motor, Drive and Encoder" (YouTube _SYhCRwacDs, linked from
teknic.com's ClearPath page), 1280 x 720. From 598.6 to 606.0 s the motor turns about a vertical axis in front of a fixed
camera on a white backdrop (a turntable shot of Teknic's own model), with the ClearPath logo and three lines of text as a
static overlay at the left. Treated as a camera orbiting a static motor: the overlay is masked out, the backdrop has no
features, so every SIFT feature is on the motor.

Stages (paths default to /tmp/oem/video; nothing from the video is written into the repo):

    /tmp/venv/bin/python desktop-lpbf/cad/oem/video_recon.py fetch    # yt-dlp through the lab tunnel (YouTube blocks the runner)
    /tmp/venv/bin/python desktop-lpbf/cad/oem/video_recon.py frames   # 74 frames at 10 fps + foreground masks
    /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/cad/oem/video_recon.py colmap    # COLMAP 3.12 on the CPU, 2 threads
    /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/cad/oem/video_recon.py analyze   # align, scale, distances, silhouettes, hull
    /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/cad/oem/video_recon.py aniso     # per-axis scale diagnostic (proportions)
    /tmp/venv/bin/python desktop-lpbf/cad/oem/video_recon.py report                   # video_recon.md from video_recon.json

Run with -I (or from another directory) so no stray module in the working directory shadows the standard library.
analyze writes analysis/out/oem/video_recon.json and two outline-only figures (no video pixels): video_recon_cloud.png
(the aligned cloud over our model, and the solved cameras) and video_recon_silhouettes.png (frame-mask outline vs. our
model's projected outline, through the solved cameras). On the shared 4-core runner (load ~20) analyze took ~15 min,
most of it the Nelder-Mead pose fit.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import pathlib
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]                                   # desktop-lpbf/
OUT = ROOT / "analysis" / "out" / "oem"
WORK = pathlib.Path(os.environ.get("OEM_VIDEO_DIR", "/tmp/oem/video"))
VIDEO_ID = "_SYhCRwacDs"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
VIDEO = WORK / "intro.mp4"
T0, DUR, FPS = 598.6, 7.4, 10                            # the turntable segment (s) and the sampling rate
MASK_T = (180, 200, 220)                                 # min-channel thresholds for the silhouette masks
MASK_T_PRIMARY = 220                                     # the only one that keeps the near-white silver flange and rear cover
MASK_T_COLMAP = 235

FLANGE_SQ = 59.10                                         # Teknic drawing D1171/M (vendor_parts.SOURCES["clearpath_sd_231x"])
BODY_L = 84.81
SHAFT_D = 9.50


def sh(cmd, log=None):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    with open(log, "w") if log else open(os.devnull, "w") as fh:
        r = subprocess.run([str(c) for c in cmd], stdout=fh if log else None, stderr=subprocess.STDOUT if log else None)
    if r.returncode:
        raise SystemExit(f"failed ({r.returncode}): {cmd[0]} {cmd[1] if len(cmd) > 1 else ''}")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ fetch / frames
def fetch():
    WORK.mkdir(parents=True, exist_ok=True)
    sh([sys.executable, "-m", "yt_dlp", "--proxy", "socks5://127.0.0.1:1080", "--js-runtimes", "node",
        "-f", "bv*[height<=720][ext=mp4]/bv*[height<=720]", "-o", str(VIDEO), "--", VIDEO_ID])
    print(VIDEO, sha256(VIDEO))


def _fg(img, T):
    """Foreground of a frame on the white backdrop: min channel < T, closed, the largest component (the motor; the logo and
    text overlay are separate components), holes filled."""
    import cv2
    g = img.min(axis=2)
    m = (g < T).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n < 2:
        return np.zeros_like(m)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    m = (lab == k).astype(np.uint8)
    ff = m.copy()
    h, w = m.shape
    fl = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, fl, (0, 0), 1)                     # background reachable from the corner
    return ((m > 0) | (ff == 0)).astype(np.uint8)


def frames():
    import cv2
    img_dir, mdir, sdir = WORK / "work" / "images", WORK / "work" / "masks_colmap", WORK / "work" / "masks"
    for d in (img_dir, mdir, sdir):
        d.mkdir(parents=True, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", T0, "-i", VIDEO, "-t", DUR, "-vf", f"fps={FPS}", img_dir / "f_%03d.png"])
    names = sorted(p.name for p in img_dir.glob("f_*.png"))
    boxes = []
    for nm in names:
        im = cv2.imread(str(img_dir / nm))
        fc = _fg(im, MASK_T_COLMAP)
        cv2.imwrite(str(mdir / (nm + ".png")), cv2.dilate(fc, np.ones((9, 9), np.uint8)) * 255)   # COLMAP: black = ignore
        for T in MASK_T:
            cv2.imwrite(str(sdir / f"{nm[:-4]}_T{T}.png"), _fg(im, T) * 255)
        ys, xs = np.nonzero(fc)
        boxes.append((nm, int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
    print(len(names), "frames; motor x", min(b[1] for b in boxes), "-", max(b[2] for b in boxes),
          "y", min(b[3] for b in boxes), "-", max(b[4] for b in boxes))


# ------------------------------------------------------------------------------------------------ COLMAP
COLMAP_ARGS = dict(
    feature_extractor=["--ImageReader.camera_model", "SIMPLE_RADIAL", "--ImageReader.single_camera", "1",
                       "--SiftExtraction.use_gpu", "0", "--SiftExtraction.num_threads", "2",
                       "--SiftExtraction.max_image_size", "1280", "--SiftExtraction.max_num_features", "8192"],
    exhaustive_matcher=["--SiftMatching.use_gpu", "0", "--SiftMatching.num_threads", "2", "--SiftMatching.guided_matching", "1"],
    mapper=["--Mapper.num_threads", "2", "--Mapper.ba_refine_principal_point", "0", "--Mapper.multiple_models", "0"],
)


def colmap():
    w = WORK / "work"
    db, sparse = w / "db.db", w / "sparse"
    if db.exists():
        db.unlink()
    sparse.mkdir(exist_ok=True)
    os.environ["OMP_NUM_THREADS"] = "2"
    sh(["colmap", "feature_extractor", "--database_path", db, "--image_path", w / "images",
        "--ImageReader.mask_path", w / "masks_colmap"] + COLMAP_ARGS["feature_extractor"], log=w / "log_features.txt")
    sh(["colmap", "exhaustive_matcher", "--database_path", db] + COLMAP_ARGS["exhaustive_matcher"], log=w / "log_matcher.txt")
    sh(["colmap", "mapper", "--database_path", db, "--image_path", w / "images", "--output_path", sparse]
       + COLMAP_ARGS["mapper"], log=w / "log_mapper.txt")
    models = sorted(p for p in sparse.iterdir() if p.is_dir())
    best = max(models, key=lambda p: (p / "images.bin").stat().st_size)
    txt = w / "sparse_txt"
    txt.mkdir(exist_ok=True)
    sh(["colmap", "model_converter", "--input_path", best, "--output_path", txt, "--output_type", "TXT"])
    print("model", best)


# ------------------------------------------------------------------------------------------------ analysis helpers
def qvec2rot(q):
    w, x, y, z = q
    return np.array([[1 - 2 * y * y - 2 * z * z, 2 * x * y - 2 * w * z, 2 * x * z + 2 * w * y],
                     [2 * x * y + 2 * w * z, 1 - 2 * x * x - 2 * z * z, 2 * y * z - 2 * w * x],
                     [2 * x * z - 2 * w * y, 2 * y * z + 2 * w * x, 1 - 2 * x * x - 2 * y * y]])


def read_model(d):
    cams, imgs, pts = {}, {}, {}
    for ln in open(d / "cameras.txt"):
        if ln.startswith("#") or not ln.strip():
            continue
        a = ln.split()
        cams[int(a[0])] = dict(model=a[1], w=int(a[2]), h=int(a[3]), params=[float(v) for v in a[4:]])
    lines = [ln for ln in open(d / "images.txt") if not ln.startswith("#")]
    for i in range(0, len(lines) - 1, 2):
        a = lines[i].split()
        if not a:
            continue
        q, t = np.array([float(v) for v in a[1:5]]), np.array([float(v) for v in a[5:8]])
        xy = lines[i + 1].split()
        n_obs = sum(1 for j in range(2, len(xy), 3) if xy[j] != "-1")
        imgs[int(a[0])] = dict(R=qvec2rot(q), t=t, cam=int(a[8]), name=a[9], n_obs=n_obs)
    for ln in open(d / "points3D.txt"):
        if ln.startswith("#") or not ln.strip():
            continue
        a = ln.split()
        pts[int(a[0])] = dict(X=np.array([float(v) for v in a[1:4]]), rgb=[int(v) for v in a[4:7]], err=float(a[7]),
                              track=(len(a) - 8) // 2)
    return cams, imgs, pts


def model_mesh(tol=0.2):
    sys.path.insert(0, str(ROOT / "cad"))
    import trimesh
    import vendor_parts as VP
    s = VP.clearpath_sd_231x()
    vs, ts = s.tessellate(tol, 0.3)
    return trimesh.Trimesh(np.array([v.toTuple() for v in vs]), np.array(ts), process=True)


def umeyama(src, dst, with_scale=True):
    """Similarity (s, R, t) minimising |s R src + t - dst|^2."""
    mu_s, mu_d = src.mean(0), dst.mean(0)
    a, b = src - mu_s, dst - mu_d
    U, S, Vt = np.linalg.svd(b.T @ a / len(src))
    D = np.eye(3)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        D[2, 2] = -1
    R = U @ D @ Vt
    s = (S * np.diag(D)).sum() / (a ** 2).sum() * len(src) if with_scale else 1.0
    return s, R, mu_d - s * R @ mu_s


def rotations24():
    import itertools
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((-1, 1), repeat=3):
            M = np.zeros((3, 3))
            for i, (p, s_) in enumerate(zip(perm, sg)):
                M[i, p] = s_
            if np.linalg.det(M) > 0:
                out.append(M)
    return out


def icp(P, tree, Q, s, R, t, iters=60, keep=0.9, with_scale=True):
    """Trimmed ICP (cloud P -> model samples Q, KD-tree `tree`), similarity or rigid. Returns s, R, t, trimmed mean distance."""
    for _ in range(iters):
        X = s * P @ R.T + t
        d, j = tree.query(X)
        k = d <= np.quantile(d, keep)
        ds, dR, dt = umeyama(X[k], Q[j[k]], with_scale)
        s, R, t = ds * s, dR @ R, ds * dR @ t + dt
    X = s * P @ R.T + t
    d, _ = tree.query(X)
    return s, R, t, float(np.mean(np.sort(d)[: int(keep * len(d))]))


def project(Xw, R, t, cam):
    f, cx, cy, k = cam["params"][:4]
    Xc = Xw @ R.T + t
    x, y = Xc[:, 0] / Xc[:, 2], Xc[:, 1] / Xc[:, 2]
    r2 = x * x + y * y
    return np.stack([f * x * (1 + k * r2) + cx, f * y * (1 + k * r2) + cy], 1), Xc[:, 2]


def silhouette(V2, F, shape):
    import cv2
    m = np.zeros(shape, np.uint8)
    P = np.round(V2 * 16).astype(np.int32)
    for tri in P[F]:
        cv2.fillConvexPoly(m, tri, 1, cv2.LINE_8, 4)          # one triangle per call: no even-odd cancellation
    return m


def iou(a, b):
    a, b = a > 0, b > 0
    return float((a & b).sum() / max((a | b).sum(), 1))


def perturb(Vm, q, c):
    """Model vertices moved by q = (rotation vector in deg, translation in mm, ln scale) about the point c (model frame)."""
    from scipy.spatial.transform import Rotation
    Rd = Rotation.from_rotvec(np.radians(q[:3])).as_matrix()
    return (Vm - c) @ Rd.T * math.exp(q[6]) + c + np.asarray(q[3:6]), Rd


def front_faces(Xw, F, R, t):
    """Faces of a closed mesh that face the camera (their union is the silhouette)."""
    tri = Xw[F]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    C = -R.T @ t
    return F[np.einsum("ij,ij->i", n, C - tri.mean(1)) > 0]


def splat(v2, shape):
    """Fast silhouette for the pose search: dense surface samples projected and closed (5 x 5), not triangle fills."""
    import cv2
    m = np.zeros(shape, np.uint8)
    u = np.round(v2).astype(int)
    ok = (u[:, 0] >= 0) & (u[:, 0] < shape[1]) & (u[:, 1] >= 0) & (u[:, 1] < shape[0])
    m[u[ok, 1], u[ok, 0]] = 1
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))


def fit_silhouettes(lo, A, views, cam, masks, fac=0.5, maxfev=500, steps=(2, 2, 2, 1.0, 1.0, 1.0, 0.01), S=None, free=range(7)):
    """7-DoF pose of our model (about its centroid) that maximises the mean silhouette IoU over the given views, starting
    from A = (s, R, t) (world -> model). Silhouettes are splats of the surface samples S at `fac` of full resolution."""
    from scipy.optimize import minimize
    sA, RA, tA = A
    c = lo.vertices.mean(0)
    small = [cv2_resize(m, fac) for m in masks]

    free = list(free)

    def full(x):
        q = np.zeros(7)
        q[free] = x
        return q

    def cost(x):
        Xm, _ = perturb(S, full(x), c)
        Xw = ((Xm - tA) @ RA) / sA
        tot = 0.0
        for (R, t), fm in zip(views, small):
            v2, _ = project(Xw, R, t, cam)
            tot += 1.0 - iou(splat(v2 * fac, fm.shape), fm)
        return tot / len(small)

    x0 = np.zeros(len(free))
    init = np.array([x0] + [x0 + np.eye(len(free))[k] * steps[f] for k, f in enumerate(free)])
    r = minimize(cost, x0, method="Nelder-Mead", options=dict(initial_simplex=init, maxfev=maxfev, xatol=0.05, fatol=1e-5))
    return full(r.x), 1.0 - cost(x0), 1.0 - r.fun, int(r.nfev)


def cv2_resize(m, fac):
    import cv2
    return cv2.resize(m, None, fx=fac, fy=fac, interpolation=cv2.INTER_NEAREST)


_KD = {}


def surf_dist(mesh, X):
    """Distance to the nearest of 1,000,000 points sampled evenly on the mesh (about 0.25 mm apart): it overestimates the
    true point-to-surface distance by about 0.1 mm at most. trimesh's exact closest_point was too slow on the shared runner."""
    import trimesh
    from scipy.spatial import cKDTree
    if id(mesh) not in _KD:
        _KD[id(mesh)] = cKDTree(np.asarray(trimesh.sample.sample_surface_even(mesh, 1000000, seed=3)[0]))
    return _KD[id(mesh)].query(X)[0] if len(X) else np.array([np.nan])


def model_occupancy(mesh, gx, gy, gz):
    """Inside test of a closed mesh at the grid's voxel centres, one z section at a time (trimesh's ray-based contains()
    needs more than the 2-3 GB cap). Within 1 % of the exact volume at 1 mm."""
    from shapely import contains_xy
    from shapely.ops import unary_union
    XX, YY = np.meshgrid(gx, gy, indexing="ij")
    occ = np.zeros((len(gx), len(gy), len(gz)), bool)
    for k, sec in enumerate(mesh.section_multiplane(plane_origin=[0, 0, 0], plane_normal=[0, 0, 1], heights=gz)):
        if sec is None:
            continue
        p = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, gz[k]), np.ones(XX.size)]
        p2 = (np.linalg.inv(sec.metadata["to_3D"]) @ p.T).T
        occ[:, :, k] = contains_xy(unary_union(sec.polygons_full), p2[:, 0], p2[:, 1]).reshape(XX.shape)
    return occ


# ------------------------------------------------------------------------------------------------ analysis
def analyze():
    import cv2
    import trimesh
    from scipy.spatial import cKDTree

    w = WORK / "work"
    cams, imgs, pts = read_model(w / "sparse_txt")
    cam = cams[next(iter(cams))]
    f_px, cx, cy, k1 = cam["params"][:4]
    res = dict(video=dict(url=VIDEO_URL, youtube_id=VIDEO_ID, file=VIDEO.name, sha256=sha256(VIDEO) if VIDEO.exists() else None,
                          title="ClearPath: Teknic's Integrated Brushless Servo Motor, Drive and Encoder (Teknic)",
                          linked_from="https://teknic.com/products/clearpath-brushless-dc-servo-motors/",
                          segment_s=[T0, round(T0 + DUR, 2)], fps_sampled=FPS, frame_px=[cam["w"], cam["h"]]),
               colmap=dict(version="3.12.6 (Ubuntu apt build, no CUDA)", args=COLMAP_ARGS, camera_model=cam["model"]))
    n_frames = len(list((w / "images").glob("f_*.png")))
    errs = np.array([p["err"] for p in pts.values()])
    tracks = np.array([p["track"] for p in pts.values()])
    # 35 mm equivalent: the diagonal of a 36 x 24 frame (43.27 mm) over the image diagonal
    f35 = f_px * 43.27 / math.hypot(cam["w"], cam["h"])
    res["sfm"] = dict(frames=n_frames, registered=len(imgs), points3D=len(pts), mean_track_length=round(float(tracks.mean()), 2),
                      mean_reprojection_error_px=round(float(errs.mean()), 3), median_reprojection_error_px=round(float(np.median(errs)), 3),
                      f_px=round(f_px, 1), f_35mm_equiv_mm=round(f35, 1), cx=round(cx, 1), cy=round(cy, 1), k1=round(k1, 5),
                      mean_observations_per_image=round(float(np.mean([i["n_obs"] for i in imgs.values()])), 1))
    C = {i: -im["R"].T @ im["t"] for i, im in imgs.items()}          # camera centres (world)

    # turntable check: camera centres on a circle; the rotation angle each frame
    Cc = np.array([C[i] for i in sorted(C)])
    cen = Cc.mean(0)
    _, _, Vt = np.linalg.svd(Cc - cen)
    ax = Vt[2]
    plane_rms = float(np.sqrt(np.mean(((Cc - cen) @ ax) ** 2)))
    rad = np.linalg.norm((Cc - cen) - np.outer((Cc - cen) @ ax, ax), axis=1)
    e1, e2 = Vt[0], Vt[1]
    ang = np.unwrap(np.arctan2((Cc - cen) @ e2, (Cc - cen) @ e1))
    res["sfm"]["orbit"] = dict(arc_deg=round(float(np.degrees(ang.max() - ang.min())), 1),
                               radius_cv_pct=round(float(rad.std() / rad.mean() * 100), 2),
                               out_of_plane_rms_over_radius_pct=round(plane_rms / float(rad.mean()) * 100, 2))

    # clean cloud
    P = np.array([p["X"] for p in pts.values()])
    keep = (errs < 2.0) & (tracks >= 3)
    P = P[keep]
    tr = cKDTree(P)
    dk, _ = tr.query(P, 9)
    md = dk[:, 1:].mean(1)
    P = P[md < md.mean() + 2.5 * md.std()]
    res["cloud"] = dict(points_kept=int(len(P)), filter="reprojection error < 2 px, track >= 3, kNN(8) mean-distance outliers > mean + 2.5 sd removed")

    mesh = model_mesh(0.2)
    lo = model_mesh(0.6)
    Q = np.asarray(trimesh.sample.sample_surface(mesh, 300000, seed=1)[0])
    qt = cKDTree(Q)
    order = sorted(imgs, key=lambda i: imgs[i]["name"])
    mk = {i: cv2.imread(str(w / "masks" / f"{imgs[i]['name'][:-4]}_T{MASK_T_PRIMARY}.png"), 0) for i in order}
    print("cloud", len(P), "points", flush=True)

    # 1) turntable frame: the orbit axis, pointing up in the frames, and the point all the optical axes pass closest to
    up = -imgs[order[0]]["R"].T @ np.array([0.0, 1.0, 0.0])
    axu = ax if ax @ up > 0 else -ax
    M_, b_ = np.zeros((3, 3)), np.zeros(3)
    for i in order:
        d_ = imgs[i]["R"].T @ np.array([0.0, 0.0, 1.0])
        Pm = np.eye(3) - np.outer(d_, d_)
        M_ += Pm
        b_ += Pm @ C[i]
    X0 = np.linalg.solve(M_, b_)
    # 2) the motor lies with its shaft level and the connector block on top, as in the video: model +y = the orbit axis.
    #    The turn about that axis is scanned in 10 deg steps by silhouette IoU; the scale starts from the cloud's height.
    hh = (P - X0) @ axu
    s0 = (52.3 + 29.55) / float(np.percentile(hh, 99.5) - np.percentile(hh, 0.5))
    cm = (lo.bounds[0] + lo.bounds[1]) / 2
    e1 = np.cross(axu, [1.0, 0.0, 0.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(axu, e1)

    def pose(th, s_):
        mx = math.cos(th) * e1 + math.sin(th) * e2
        R0 = np.stack([mx, axu, np.cross(mx, axu)])
        return s_, R0, cm - s_ * R0 @ X0

    Sfit = np.asarray(trimesh.sample.sample_surface_even(lo, 120000, seed=4)[0])

    def mean_iou(A, ids, fac=0.5):
        Xw = ((Sfit - A[2]) @ A[1]) / A[0]
        tot = 0.0
        for i in ids:
            fm = cv2_resize(mk[i], fac)
            v2, _ = project(Xw, imgs[i]["R"], imgs[i]["t"], cam)
            tot += iou(splat(v2 * fac, fm.shape), fm)
        return tot / len(ids)

    sub = order[::6]
    scan = sorted(((mean_iou(pose(math.radians(dg), s0 * f_), sub), dg, f_) for dg in range(0, 360, 10) for f_ in (0.6, 0.7, 0.8, 0.9, 1.0, 1.15)),
                  reverse=True)
    print("turn scan (IoU, deg, scale factor):", [tuple(round(v, 3) for v in r) for r in scan[:5]], flush=True)
    A0 = pose(math.radians(scan[0][1]), s0 * scan[0][2])
    fit_ids = order[::3]
    views = [(imgs[i]["R"], imgs[i]["t"]) for i in fit_ids]
    c0 = lo.vertices.mean(0)
    A_sil, nfev_tot, iou_first = A0, 0, None
    # upright: the motor lies shaft-level with the block up in every frame, so only the turn about the vertical (model y)
    # is free, with translation and scale; a free 3-D rotation tipped the model shaft-up to fit the distorted cloud better
    for steps, mf in (([0, 8, 0, 3.0, 3.0, 3.0, 0.05], 250), ([0, 2, 0, 1.0, 1.0, 1.0, 0.01], 150)):
        q, i0_, i1_, nfev = fit_silhouettes(lo, A_sil, views, cam, [mk[i] for i in fit_ids], maxfev=mf, steps=steps, S=Sfit,
                                            free=(1, 3, 4, 5, 6))
        iou_first = i0_ if iou_first is None else iou_first
        nfev_tot += nfev
        _, Rd = perturb(lo.vertices[:1], q, c0)
        s_d, t_d = math.exp(q[6]), np.asarray(q[3:6])
        sA_, RA_, tA_ = A_sil
        A_sil = (sA_ / s_d, Rd.T @ RA_, Rd.T @ (tA_ - c0 - t_d) / s_d + c0)
        print("silhouette fit", round(i0_, 4), "->", round(i1_, 4), nfev, "evaluations", flush=True)
        np.save(WORK / "work" / "pose_silhouette.npy", np.concatenate([[A_sil[0]], A_sil[1].ravel(), A_sil[2]]))
    res["alignment"] = dict(
        method="turntable frame (orbit axis = model +y, connector block up), turn about it scanned in 10 deg steps x 6 scales by "
               "silhouette IoU on every 6th view, then Nelder-Mead over 5 DoF (turn about the vertical, translation, scale; the model "
               "kept upright) on the T220 masks of "
               f"every 3rd view ({len(fit_ids)}), half resolution, silhouettes splatted from 120,000 surface samples, two passes, "
               f"{nfev_tot} evaluations",
        turn_scan_best=[round(scan[0][0], 4), scan[0][1], scan[0][2]], fit_mean_iou_before=round(iou_first, 4), fit_mean_iou_after=round(i1_, 4),
        silhouette_scale_mm_per_unit=round(float(A_sil[0]), 4),
        rejected_free_rotation="an earlier run with the 3-D rotation free as well tipped the model shaft-up within one "
                               "350-evaluation pass (mean IoU 0.76 on the fitted views, not converged); the frames show the shaft "
                               "level, so the rotation is held upright",
        rejected="unconstrained start (centroid + principal axes, 24 axis rotations, trimmed ICP with scale): best trimmed mean 1.11 mm "
                 "at 84.4 mm per unit, but a median silhouette IoU of 0.53 at that pose, so it converged on a wrong fit of the sparse cloud")

    # 3) the cloud at the silhouette pose; the known dimensions measured in it; ICP from there
    def dims(X):
        fl = X[(X[:, 2] > -6.0) & (X[:, 2] < 0.0) & (np.abs(X[:, 0]) < 40) & (np.abs(X[:, 1]) < 40)]
        fw = [float(np.percentile(fl[:, k], 99.5) - np.percentile(fl[:, k], 0.5)) if len(fl) > 20 else None for k in (0, 1)]
        shp = X[(X[:, 2] > 3.0) & (X[:, 2] < 19.0) & (np.hypot(X[:, 0], X[:, 1]) < 8.0)]
        sd = float(2 * np.median(np.hypot(shp[:, 0], shp[:, 1]))) if len(shp) > 10 else None
        return dict(flange_plate_points=int(len(fl)), flange_width_x_y_mm=[round(v, 2) if v else None for v in fw],
                    shaft_points=int(len(shp)), shaft_d_mm=round(sd, 2) if sd else None,
                    rear_z_p0_5_mm=round(float(np.percentile(X[:, 2], 0.5)), 2), front_z_p99_5_mm=round(float(np.percentile(X[:, 2], 99.5)), 2))

    sS, RS, tS = A_sil
    XS = sS * P @ RS.T + tS
    res["scale"] = dict(at_silhouette_pose=dims(XS), flange_drawing_mm=FLANGE_SQ, shaft_drawing_mm=SHAFT_D, rear_drawing_mm=-BODY_L)
    variants = {"silhouette_pose": A_sil}
    s1, R1, t1, _ = icp(P, qt, Q, sS, RS, tS, iters=60, keep=0.9, with_scale=False)
    variants["rigid_icp_silhouette_scale"] = (s1, R1, t1)
    fw = [v for v in res["scale"]["at_silhouette_pose"]["flange_width_x_y_mm"] if v]
    if fw:
        s_fl = sS * FLANGE_SQ / float(np.mean(fw))
        res["scale"]["flange_scale_vs_silhouette_scale_pct"] = round((s_fl / sS - 1) * 100, 2)
        tF = tS + (sS - s_fl) * (RS @ P.mean(0))
        s2, R2, t2, _ = icp(P, qt, Q, s_fl, RS, tF, iters=60, keep=0.9, with_scale=False)
        variants["flange_scaled_rigid_icp"] = (s2, R2, t2)
    s3, R3, t3, _ = icp(P, qt, Q, sS, RS, tS, iters=60, keep=0.9, with_scale=True)
    variants["similarity_icp"] = (s3, R3, t3)
    res["scale"]["similarity_icp_vs_silhouette_scale_pct"] = round((s3 / sS - 1) * 100, 2)
    res["distance"] = {}
    for nm, (sv, Rv, tv) in variants.items():
        d = surf_dist(mesh, sv * P @ Rv.T + tv)
        res["distance"][nm] = dict(scale=round(float(sv), 5), mean_mm=round(float(d.mean()), 3), median_mm=round(float(np.median(d)), 3),
                                   p95_mm=round(float(np.percentile(d, 95)), 3), max_mm=round(float(d.max()), 2),
                                   within_0_5mm_pct=round(float((d <= 0.5).mean() * 100), 1),
                                   within_1mm_pct=round(float((d <= 1.0).mean() * 100), 1),
                                   within_2mm_pct=round(float((d <= 2.0).mean() * 100), 1))
        print(nm, res["distance"][nm], flush=True)
    prim = "flange_scaled_rigid_icp" if "flange_scaled_rigid_icp" in variants else "rigid_icp_silhouette_scale"
    res["primary"] = prim

    # 4) silhouettes over every solved view, at the silhouette pose and at the primary ICP pose
    res["silhouette"], per = {"views": len(order)}, [dict(name=imgs[i]["name"]) for i in order]
    for pn in ("silhouette_pose", prim):
        sv, Rv, tv = variants[pn]
        Vw_ = ((lo.vertices - tv) @ Rv) / sv
        acc = {}
        for i, row in zip(order, per):
            v2, _ = project(Vw_, imgs[i]["R"], imgs[i]["t"], cam)
            ms = silhouette(v2, lo.faces, (cam["h"], cam["w"]))
            for T in MASK_T:
                if pn != "silhouette_pose" and T != MASK_T_PRIMARY:
                    continue
                fm = mk[i] if T == MASK_T_PRIMARY else cv2.imread(str(w / "masks" / f"{imgs[i]['name'][:-4]}_T{T}.png"), 0)
                acc.setdefault(f"T{T}", []).append(iou(ms, fm))
                row[f"{pn}_T{T}"] = round(acc[f"T{T}"][-1], 4)
            yb = int(np.nonzero(ms.any(1))[0].max()) + 2          # the backdrop shadow lies under the motor: cut below our model
            a_, b_ = ms.copy(), mk[i].copy()
            a_[yb:], b_[yb:] = 0, 0
            acc.setdefault("T220_shadow_rows_cut", []).append(iou(a_, b_))
            row[f"{pn}_T220_shadow_rows_cut"] = round(acc["T220_shadow_rows_cut"][-1], 4)
        res["silhouette"][pn] = {k: dict(median=round(float(np.median(v)), 4), min=round(float(np.min(v)), 4), max=round(float(np.max(v)), 4),
                                         mean=round(float(np.mean(v)), 4)) for k, v in acc.items()}
        print("silhouettes", pn, {k: v["median"] for k, v in res["silhouette"][pn].items()}, flush=True)
    res["silhouette"]["per_view"] = per
    A_cloud = variants[prim]
    sA, RA, tA = A_sil                                                 # the hull and the overlays use the silhouette pose
    Vw = ((lo.vertices - tA) @ RA) / sA

    # visual hull from the solved cameras and the T200 masks, in the model frame (1 mm voxels)
    pitch, marg = 1.0, 8.0
    b0, b1 = np.floor(lo.bounds[0] - marg), np.ceil(lo.bounds[1] + marg)
    gx, gy, gz = [np.arange(b0[a], b1[a], pitch) + pitch / 2 for a in range(3)]
    occ = model_occupancy(lo, gx, gy, gz)                              # our model at the voxel centres (1 mm)
    G = np.stack(np.meshgrid(gx, gy, gz, indexing="ij"), -1).reshape(-1, 3)
    Gw = ((G - tA) @ RA) / sA
    votes = np.zeros(len(G), np.int32)
    for i in order:
        im = imgs[i]
        fm = cv2.imread(str(w / "masks" / f"{im['name'][:-4]}_T{MASK_T_PRIMARY}.png"), 0)
        fm = cv2.dilate(fm, np.ones((3, 3), np.uint8))
        v2, z = project(Gw, im["R"], im["t"], cam)
        u = np.round(v2).astype(int)
        ok = (u[:, 0] >= 0) & (u[:, 0] < cam["w"]) & (u[:, 1] >= 0) & (u[:, 1] < cam["h"]) & (z > 0)
        hit = np.zeros(len(G), bool)
        hit[ok] = fm[u[ok, 1], u[ok, 0]] > 0
        votes += hit
    occ_model = occ.reshape(-1)
    n_v = len(order)
    hulls = {"all_views": votes == n_v, "95pct_views": votes >= math.ceil(0.95 * n_v)}
    hull_stats = {}
    for hn, hm in hulls.items():
        hv, it_ = float(hm.sum() * pitch ** 3), float((hm & occ_model).sum() * pitch ** 3)
        hull_stats[hn] = dict(hull_volume_cm3=round(hv / 1e3, 1), volume_iou=round(it_ / (hv + float(occ_model.sum()) - it_), 4),
                              model_inside_hull_pct=round(it_ / float(occ_model.sum()) * 100, 1))
    inside = hulls["95pct_views"]
    hull_vol, model_vol = float(inside.sum() * pitch ** 3), float(occ_model.sum() * pitch ** 3)
    inter = float((inside & occ_model).sum() * pitch ** 3)
    H = inside.reshape(len(gx), len(gy), len(gz))
    pad = np.pad(H, 1)
    nb = sum(np.roll(pad, sh_, ax_)[1:-1, 1:-1, 1:-1] for ax_ in range(3) for sh_ in (-1, 1))
    surf = G[(H & (nb < 6)).reshape(-1)]
    dh = surf_dist(mesh, surf)
    dm, _ = cKDTree(surf).query(Q[::10]) if len(surf) else (np.array([np.nan]), None)
    res["visual_hull"] = dict(pitch_mm=pitch, mask=f"T{MASK_T_PRIMARY} dilated 1 px", views=len(order), variants=hull_stats,
                              kept="voxels inside the mask in >= 95 % of the solved views", hull_volume_cm3=round(hull_vol / 1e3, 1),
                              model_volume_cm3_voxels=round(model_vol / 1e3, 1), model_volume_cm3_exact=round(mesh.volume / 1e3, 1),
                              volume_iou=round(inter / (hull_vol + model_vol - inter), 4) if hull_vol else 0.0,
                              hull_to_model_mean_mm=round(float(np.mean(dh)), 2), hull_to_model_p95_mm=round(float(np.percentile(dh, 95)), 2),
                              model_to_hull_mean_mm=round(float(np.mean(dm)), 2), model_to_hull_p95_mm=round(float(np.percentile(dm, 95)), 2),
                              chamfer_mean_mm=round(float((np.mean(dh) + np.mean(dm)) / 2), 2))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "video_recon.json").write_text(json.dumps(res, indent=1))
    figures(res, X=A_cloud[0] * P @ A_cloud[1].T + A_cloud[2], mesh=mesh, imgs=imgs, cam=cam, order=order, Vw=Vw, lo=lo, A=(sA, RA, tA), hull=surf)
    print(json.dumps({k: v for k, v in res.items() if k not in ("silhouette",)}, indent=1))
    print(json.dumps({k: v for k, v in res["silhouette"].items() if k != "per_view"}, indent=1))


def figures(res, X, mesh, imgs, cam, order, Vw, lo, A, hull):
    import cv2
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sA, RA, tA = A
    w = WORK / "work"
    # 1) the aligned cloud over our model (three orthographic views), coloured by distance; cameras in the model frame
    import trimesh
    d = surf_dist(mesh, X)
    S = trimesh.sample.sample_surface(mesh, 60000, seed=2)[0]
    Cm = np.array([sA * RA @ (-imgs[i]["R"].T @ imgs[i]["t"]) + tA for i in order])
    fig, axs = plt.subplots(1, 4, figsize=(17, 4.6), gridspec_kw=dict(width_ratios=[1, 1, 1, 1.25]))
    for a_, (i, j, ttl) in zip(axs[:3], [(0, 1, "end view (x, y)"), (0, 2, "side (x, z)"), (1, 2, "side (y, z)")]):
        a_.scatter(S[:, i], S[:, j], s=0.05, c="#b8b8b8", rasterized=True)
        sc = a_.scatter(X[:, i], X[:, j], s=2.0, c=np.clip(d, 0, 3), cmap="viridis", vmin=0, vmax=3, rasterized=True)
        a_.set_aspect("equal")
        a_.set_title(ttl, fontsize=10)
        a_.set_xlabel("xyz"[i] + " (mm)")
        a_.set_ylabel("xyz"[j] + " (mm)")
    fig.colorbar(sc, ax=axs[2], label="distance to our model (mm)", fraction=0.046)
    a_ = axs[3]
    a_.scatter(S[:, 0], S[:, 2], s=0.05, c="#b8b8b8", rasterized=True)
    a_.plot(Cm[:, 0], Cm[:, 2], ".-", color="#c0392b", ms=3, lw=0.6)
    a_.set_aspect("equal")
    a_.set_title("solved cameras (red), model frame, x-z", fontsize=10)
    dd = res["distance"][res["primary"]]
    fig.suptitle(f"Teknic video, COLMAP: {res['sfm']['registered']}/{res['sfm']['frames']} frames, {res['cloud']['points_kept']} points; "
                 f"cloud to our clearpath_sd_231x(): median {dd['median_mm']} mm, {dd['within_1mm_pct']} % within 1 mm", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "video_recon_cloud.png", dpi=110)
    plt.close(fig)
    # 2) outline-only silhouette overlays (no video pixels): frame-mask outline (black) and our model's outline (red)
    pick = [order[int(k)] for k in np.linspace(0, len(order) - 1, 6)]
    tiles = []
    for i in pick:
        im = imgs[i]
        fm = cv2.imread(str(w / "masks" / f"{im['name'][:-4]}_T{MASK_T_PRIMARY}.png"), 0)
        v2, _ = project(Vw, im["R"], im["t"], cam)
        ms = silhouette(v2, lo.faces, fm.shape)
        canvas = np.full(fm.shape + (3,), 255, np.uint8)
        c1, _ = cv2.findContours((fm > 0).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c2, _ = cv2.findContours(ms, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(canvas, c1, -1, (0, 0, 0), 3)
        cv2.drawContours(canvas, c2, -1, (40, 40, 220), 2)
        row = next(r for r in res["silhouette"]["per_view"] if r["name"] == im["name"])
        cv2.putText(canvas, f"{im['name']}  IoU {row['silhouette_pose_T220']:.3f}", (560, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        tiles.append(canvas[:, 520:1280])
    grid = np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])])
    cv2.imwrite(str(OUT / "video_recon_silhouettes.png"), cv2.resize(grid, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))


def _clean_cloud(pts):
    from scipy.spatial import cKDTree
    errs = np.array([p["err"] for p in pts.values()])
    tracks = np.array([p["track"] for p in pts.values()])
    P = np.array([p["X"] for p in pts.values()])[(errs < 2.0) & (tracks >= 3)]
    dk, _ = cKDTree(P).query(P, 9)
    md = dk[:, 1:].mean(1)
    return P[md < md.mean() + 2.5 * md.std()], errs


def _per_axis(X, Q, qt):
    D, b = np.ones(3), np.zeros(3)
    for _ in range(60):
        d, j = qt.query(X * D + b)
        k = d <= np.quantile(d, 0.9)
        for ax_ in range(3):
            D[ax_], b[ax_] = np.linalg.lstsq(np.c_[X[k, ax_], np.ones(k.sum())], Q[j[k], ax_], rcond=None)[0]
    return D


def fixedf():
    """Focal-length test: the mapper re-run on the same features and matches with f held fixed and k1 = 0
    (`colmap mapper ... --Mapper.ba_refine_focal_length 0 --Mapper.ba_refine_extra_params 0`, the database's camera set to
    f). Each model given as label:f_px:txt_dir is compared with our model the same way: the first run's silhouette pose is
    carried over through a similarity fitted to the 74 camera centres, refitted on the silhouettes (upright, 5 DoF, every
    6th view, 150 evaluations), then the per-axis scales, the flange and shaft, the cloud distances (rigid ICP at the
    flange scale) and the silhouette IoU over all views. Writes analysis/out/oem/video_recon_fixedf.json."""
    import cv2
    import trimesh
    from scipy.spatial import cKDTree
    w = WORK / "work"
    _, imgs0, _ = read_model(w / "sparse_txt")
    a0 = np.load(w / "pose_silhouette.npy")
    A0 = (a0[0], a0[1:10].reshape(3, 3), a0[10:13])
    C0 = {im["name"]: -im["R"].T @ im["t"] for im in imgs0.values()}
    mesh, lo = model_mesh(0.2), model_mesh(0.6)
    Q = np.asarray(trimesh.sample.sample_surface_even(mesh, 300000, seed=5)[0])
    qt = cKDTree(Q)
    Sfit = np.asarray(trimesh.sample.sample_surface_even(lo, 120000, seed=4)[0])
    out = dict(date="2026-11-25", method=fixedf.__doc__.split("\n\n")[0].replace("\n", " "), runs={})
    if (OUT / "video_recon_fixedf.json").exists():                    # keep runs analysed in earlier calls
        out["runs"] = json.loads((OUT / "video_recon_fixedf.json").read_text()).get("runs", {})
    for arg in sys.argv[2:]:
        label, fpx, d_ = arg.split(":")
        cams, imgs, pts = read_model(pathlib.Path(d_))
        cam = cams[next(iter(cams))]
        P, errs = _clean_cloud(pts)
        order = sorted(imgs, key=lambda i: imgs[i]["name"])
        C = np.array([-imgs[i]["R"].T @ imgs[i]["t"] for i in order])
        cen = C.mean(0)
        _, _, Vt = np.linalg.svd(C - cen)
        rad = np.linalg.norm((C - cen) - np.outer((C - cen) @ Vt[2], Vt[2]), axis=1)
        ang = np.unwrap(np.arctan2((C - cen) @ Vt[1], (C - cen) @ Vt[0]))
        Cn = {imgs[i]["name"]: -imgs[i]["R"].T @ imgs[i]["t"] for i in order}
        names = [n for n in Cn if n in C0]
        X0c, X1c = np.array([C0[n] for n in names]), np.array([Cn[n] for n in names])
        sT, RT, tT = umeyama(X0c, X1c)                                 # first run's world -> this run's world
        resid = np.linalg.norm(sT * X0c @ RT.T + tT - X1c, axis=1)
        sA, RA, tA = A0
        A = (sA / sT, RA @ RT.T, tA - (sA / sT) * RA @ RT.T @ tT)
        mk = {i: cv2.imread(str(w / "masks" / f"{imgs[i]['name'][:-4]}_T{MASK_T_PRIMARY}.png"), 0) for i in order}
        fit_ids = order[::6]
        q, i0_, i1_, nfev = fit_silhouettes(lo, A, [(imgs[i]["R"], imgs[i]["t"]) for i in fit_ids], cam, [mk[i] for i in fit_ids],
                                            maxfev=150, steps=[0, 3, 0, 2.0, 2.0, 2.0, 0.03], S=Sfit, free=(1, 3, 4, 5, 6))
        c0 = lo.vertices.mean(0)
        _, Rd = perturb(lo.vertices[:1], q, c0)
        s_d, t_d = math.exp(q[6]), np.asarray(q[3:6])
        sS, RS, tS = A[0] / s_d, Rd.T @ A[1], Rd.T @ (A[2] - c0 - t_d) / s_d + c0
        XS = sS * P @ RS.T + tS
        D = _per_axis(XS, Q, qt)
        fl = XS[(XS[:, 2] > -6.0) & (XS[:, 2] < 0.0) & (np.abs(XS[:, 0]) < 40) & (np.abs(XS[:, 1]) < 40)]
        fw = [float(np.percentile(fl[:, k], 99.5) - np.percentile(fl[:, k], 0.5)) for k in (0, 1)] if len(fl) > 20 else []
        shp = XS[(XS[:, 2] > 3.0) & (XS[:, 2] < 19.0) & (np.hypot(XS[:, 0], XS[:, 1]) < 8.0)]
        s_fl = sS * FLANGE_SQ / float(np.mean(fw)) if fw else sS
        s2, R2, t2, _ = icp(P, qt, Q, s_fl, RS, tS + (sS - s_fl) * (RS @ P.mean(0)), iters=60, keep=0.9, with_scale=False)
        dd = surf_dist(mesh, s2 * P @ R2.T + t2)
        Vw = ((lo.vertices - tS) @ RS) / sS
        ious = []
        for i in order:
            v2, _ = project(Vw, imgs[i]["R"], imgs[i]["t"], cam)
            ious.append(iou(silhouette(v2, lo.faces, (cam["h"], cam["w"])), mk[i]))
        run = dict(f_px=round(cam["params"][0], 1), k1=round(cam["params"][3], 5) if len(cam["params"]) > 3 else None,
                   f_35mm_equiv_mm=round(cam["params"][0] * 43.27 / math.hypot(cam["w"], cam["h"]), 1),
                   registered=len(imgs), points3D=len(pts), mean_reprojection_error_px=round(float(errs.mean()), 3),
                   orbit=dict(arc_deg=round(float(np.degrees(ang.max() - ang.min())), 1), radius_cv_pct=round(float(rad.std() / rad.mean() * 100), 2)),
                   camera_transfer_residual_pct_of_radius=round(float(np.median(resid) / rad.mean() * 100), 1),
                   silhouette_refit=dict(views=len(fit_ids), evaluations=nfev, mean_iou_before=round(i0_, 4), mean_iou_after=round(i1_, 4)),
                   silhouette_iou_all_views_T220=dict(median=round(float(np.median(ious)), 4), min=round(float(np.min(ious)), 4),
                                                      max=round(float(np.max(ious)), 4)),
                   per_axis_scale=dict(x=round(float(D[0]), 4), y=round(float(D[1]), 4), z=round(float(D[2]), 4)),
                   per_axis_spread_pct=round(float((D.max() / D.min() - 1) * 100), 1),
                   flange_width_x_y_mm=[round(v, 2) for v in fw], flange_points=int(len(fl)),
                   shaft_d_mm=round(float(2 * np.median(np.hypot(shp[:, 0], shp[:, 1]))), 2) if len(shp) > 10 else None,
                   cloud_to_model_flange_scaled_rigid_icp=dict(mean_mm=round(float(dd.mean()), 3), median_mm=round(float(np.median(dd)), 3),
                                                              p95_mm=round(float(np.percentile(dd, 95)), 3),
                                                              within_0_5mm_pct=round(float((dd <= 0.5).mean() * 100), 1),
                                                              within_1mm_pct=round(float((dd <= 1.0).mean() * 100), 1)))
        out["runs"][label] = run
        print(label, json.dumps(run), flush=True)
        (OUT / "video_recon_fixedf.json").write_text(json.dumps(out, indent=1))


def aniso():
    """Per-axis scale of the cloud against our model, from the silhouette pose: trimmed ICP that solves a scale and an
    offset for each model axis (x across the flange, y up through the connector block, z along the shaft). A Euclidean
    reconstruction gives three equal scales; the spread is how far the solved cameras distort the motor."""
    import trimesh
    from scipy.spatial import cKDTree
    w = WORK / "work"
    cams, imgs, pts = read_model(w / "sparse_txt")
    errs = np.array([p["err"] for p in pts.values()])
    tracks = np.array([p["track"] for p in pts.values()])
    P = np.array([p["X"] for p in pts.values()])[(errs < 2.0) & (tracks >= 3)]
    dk, _ = cKDTree(P).query(P, 9)
    md = dk[:, 1:].mean(1)
    P = P[md < md.mean() + 2.5 * md.std()]
    a = np.load(w / "pose_silhouette.npy")
    s, R, t = a[0], a[1:10].reshape(3, 3), a[10:13]
    mesh = model_mesh(0.2)
    Q = np.asarray(trimesh.sample.sample_surface_even(mesh, 300000, seed=5)[0])
    qt = cKDTree(Q)
    X = s * P @ R.T + t
    D, b = np.ones(3), np.zeros(3)
    for _ in range(60):
        Y = X * D + b
        d, j = qt.query(Y)
        k = d <= np.quantile(d, 0.9)
        for ax_ in range(3):
            A_ = np.c_[X[k, ax_], np.ones(k.sum())]
            D[ax_], b[ax_] = np.linalg.lstsq(A_, Q[j[k], ax_], rcond=None)[0]
    d, _ = qt.query(X * D + b)
    out = dict(per_axis_scale=dict(x=round(float(D[0]), 4), y=round(float(D[1]), 4), z=round(float(D[2]), 4)),
               spread_pct=round(float((D.max() / D.min() - 1) * 100), 1),
               distance_after=dict(median_mm=round(float(np.median(d)), 3), within_0_5mm_pct=round(float((d <= 0.5).mean() * 100), 1),
                                   within_1mm_pct=round(float((d <= 1.0).mean() * 100), 1)),
               note="diagnostic only: per-axis scales are not a valid correction of a reconstruction")
    r = json.loads((OUT / "video_recon.json").read_text())
    r["anisotropy"] = out
    (OUT / "video_recon.json").write_text(json.dumps(r, indent=1))
    print(out)


def report():
    """analysis/out/oem/video_recon.md from video_recon.json."""
    r = json.loads((OUT / "video_recon.json").read_text())
    v, sf, sc, cl, al = r["video"], r["sfm"], r["scale"], r["cloud"], r["alignment"]
    dist, si, vh, prim = r["distance"], r["silhouette"], r["visual_hull"], r["primary"]
    L = []
    a = L.append
    a("# ClearPath from Teknic's product video: COLMAP reconstruction against `clearpath_sd_231x()` (round 6, 2026-11-25)")
    a("")
    a("Made by [`cad/oem/video_recon.py`](../../../cad/oem/video_recon.py); every number is in [`video_recon.json`](video_recon.json).")
    a("Nothing from the video is committed: frames, masks and the COLMAP workspace stay in `/tmp/oem/video`. The two figures show")
    a("only outlines, our model and the reconstructed points.")
    a("")
    dP, sP = dist[prim], si["silhouette_pose"]["T220"]
    a(f"**Result:** COLMAP solved all {sf['registered']} frames of a turntable shot ({sf['orbit']['arc_deg']}° of the motor seen), but the")
    a("reconstruction does not keep the motor's proportions: fitting one scale per axis spreads them by "
      f"{r['anisotropy']['spread_pct'] if 'anisotropy' in r else '?'} %. So our model")
    a(f"fits it only to a median silhouette IoU of {sP['median']} over all {si['views']} views, with {dP['within_1mm_pct']} % of the points within 1 mm")
    a(f"and {dP['within_0_5mm_pct']} % within 0.5 mm. That is not a measurement of our model to 0.5 mm. The likely cause is the focal length,")
    a("which a narrow-angle turntable shot fixes poorly.")
    a("")
    a("## Video")
    a("")
    a(f"- Teknic, \"{v['title'].split(' (')[0]}\", YouTube [`{v['youtube_id']}`]({v['url']}), linked from")
    a(f"  [Teknic's ClearPath page]({v['linked_from']}). Fetched with yt-dlp through the lab tunnel, since YouTube asks the runner")
    a(f"  to sign in. 1280 × 720, 29.97 fps, sha256 `{v['sha256']}`.")
    a(f"- **Segment:** {v['segment_s'][0]}–{v['segment_s'][1]} s. The motor turns about a vertical axis in front of a fixed camera on")
    a("  a white backdrop, from shaft-left through the rear to nearly shaft-on. It is a turntable render of Teknic's own 3D model,")
    a("  not footage of a real unit. The ClearPath logo and three lines of text sit over the left of the frame and stay still.")
    a(f"- **Frames:** {sf['frames']} at {v['fps_sampled']} fps, full frame. Each frame's foreground is the largest connected region")
    a("  darker than the backdrop (minimum RGB channel below a threshold), closed and hole-filled. The overlay text is a separate")
    a("  region, so it drops out. COLMAP got that mask at threshold 235, dilated 4 px, so all its features are on the motor.")
    a("- **First video tried:** \"ClearPath-SD (Step and Direction) Series Overview\" (`-gigcf7ZzAQ`, the SD page's video). It")
    a("  shows the motor only in still poses, so it has no multi-view segment.")
    a("")
    a("## COLMAP")
    a("")
    a("COLMAP 3.12.6 (Ubuntu's build, no CUDA), under the 3 GB cap with 2 threads:")
    a("- SIFT on the CPU, up to 8,192 features per frame at full resolution (585–2,524 found, median 1,572);")
    a("- exhaustive matching with guided matching;")
    a("- the incremental mapper, with one SIMPLE_RADIAL camera for all frames and the principal point fixed at the image centre.")
    a("")
    a("| | |")
    a("|---|---|")
    a(f"| Registered frames | **{sf['registered']} of {sf['frames']}** |")
    a(f"| 3D points | {sf['points3D']:,} (mean track {sf['mean_track_length']} frames) |")
    a(f"| Reprojection error | mean {sf['mean_reprojection_error_px']} px, median {sf['median_reprojection_error_px']} px |")
    a(f"| Focal length | {sf['f_px']} px, {sf['f_35mm_equiv_mm']} mm in 35 mm terms (horizontal field of view "
      f"{2 * math.degrees(math.atan(640 / sf['f_px'])):.1f}°) |")
    a(f"| Radial distortion k1 | {sf['k1']}. A render has none, so this is a first sign that the intrinsics absorb an error |")
    a(f"| Solved camera path | an arc of {sf['orbit']['arc_deg']}° round the motor, in one plane (out-of-plane RMS "
      f"{sf['orbit']['out_of_plane_rms_over_radius_pct']} % of the radius). Its radius varies {sf['orbit']['radius_cv_pct']} % (1 sd), where a fixed "
      "camera and a turntable give a circle: a second sign of the distortion |")
    a("")
    a("Dense MVS (`patch_match_stereo`) needs CUDA, so it was not run. A visual hull from the solved cameras stands in for it.")
    a("")
    a("## Alignment, scale and distances")
    a("")
    a(f"- **Cloud:** {cl['points_kept']:,} points after filtering ({cl['filter']}).")
    a(f"- **Rejected start:** {al['rejected']}.")
    if "rejected_free_rotation" in al:
        a(f"- **Rejected free rotation:** {al['rejected_free_rotation']}.")
    a(f"- **Alignment used:** {al['method']}. Mean IoU over those views: {al['fit_mean_iou_before']} → {al['fit_mean_iou_after']}.")
    sp = sc["at_silhouette_pose"]
    fw = sp["flange_width_x_y_mm"]
    a(f"- **Known dimensions measured in the cloud** at that pose:")
    a(f"  - flange plate (z −6 to 0): {sp['flange_plate_points']} points spanning {fw[0]} × {fw[1]} mm (0.5–99.5 percentiles), against the")
    a(f"    drawing's {sc['flange_drawing_mm']} mm square;")
    a(f"  - shaft: {sp['shaft_d_mm']} mm across from {sp['shaft_points']} points (drawing {sc['shaft_drawing_mm']} mm);")
    a(f"  - the cloud runs from z {sp['rear_z_p0_5_mm']} to {sp['front_z_p99_5_mm']} (0.5 and 99.5 percentiles); the drawing runs from the pin")
    a(f"    tips at {sc['rear_drawing_mm']} to the shaft end at +20.57.")
    if "flange_scale_vs_silhouette_scale_pct" in sc:
        a(f"  - Scaling the cloud so the flange measures 59.10 changes the silhouette scale by {sc['flange_scale_vs_silhouette_scale_pct']:+} %;")
    a(f"  - letting ICP choose the scale changes it by {sc['similarity_icp_vs_silhouette_scale_pct']:+} %.")
    if "anisotropy" in r:
        an = r["anisotropy"]
        ps = an["per_axis_scale"]
        a(f"- **Proportions:** fitting a separate scale on each model axis (diagnostic only) gives x {ps['x']}, y {ps['y']}, z {ps['z']}: a")
        a(f"  {an['spread_pct']} % spread. A Euclidean reconstruction gives three equal scales, so the cloud's proportions differ from")
        a(f"  the motor's. With those scales, the median distance would be {an['distance_after']['median_mm']} mm and")
        a(f"  {an['distance_after']['within_1mm_pct']} % of points would be within 1 mm.")
    a("")
    a("**Cloud to our model's surface** (distance to the nearest of 1,000,000 points sampled on it, about 0.25 mm apart, so up to")
    a("about 0.1 mm high):")
    a("")
    a("| Pose and scale | Mean | Median | P95 | Within 0.5 mm | Within 1 mm | Within 2 mm |")
    a("|---|---|---|---|---|---|---|")
    names = dict(silhouette_pose="Silhouette fit, no ICP", rigid_icp_silhouette_scale="Rigid ICP, silhouette scale",
                 flange_scaled_rigid_icp="Rigid ICP, scale set by the flange (59.10 mm)", similarity_icp="ICP with free scale")
    for k_, nm in names.items():
        if k_ in dist:
            d_ = dist[k_]
            b_ = "**" if k_ == prim else ""
            a(f"| {nm} | {d_['mean_mm']} | {d_['median_mm']} | {d_['p95_mm']} | {b_}{d_['within_0_5mm_pct']} %{b_} | "
              f"{b_}{d_['within_1mm_pct']} %{b_} | {d_['within_2mm_pct']} % |")
    a("")
    a("## Silhouettes through the solved cameras")
    a("")
    a(f"Our model is projected through each of the {si['views']} solved cameras (with k1, filled one triangle at a time) and compared")
    a("with that frame's foreground mask. The silver flange and rear cover are nearly white where they catch the light, so the")
    a("mask depends on the threshold: 220 keeps them, lower thresholds cut into them. The backdrop's soft shadow under the motor is")
    a("darker than 220, so the T220 mask also takes in a band of shadow. The \"shadow rows cut\" line drops the rows below our")
    a("model's lowest point in both masks.")
    a("")
    a("| Pose | Mask | Median IoU | Min | Max |")
    a("|---|---|---|---|---|")
    for pn, lab in (("silhouette_pose", "Silhouette fit"), (prim, names.get(prim, prim))):
        for k_, x_ in si[pn].items():
            a(f"| {lab} | {k_.replace('_', ' ')} | {x_['median']} | {x_['min']} | {x_['max']} |")
    a("")
    a("[`video_recon_silhouettes.png`](video_recon_silhouettes.png): six of the views, the frame mask's outline in black and our")
    a("model's in red, at the silhouette-fit pose.")
    a("")
    a("## Visual hull")
    a("")
    a(f"Voxels of {vh['pitch_mm']} mm in our model's frame (silhouette-fit pose) are kept where they project inside the mask")
    a(f"({vh['mask']}) in at least 95 % of the solved views. A visual hull can't see concavities, so it is an outer bound: the gaps")
    a("between the pin fins, the connector pockets and the steps between the flange and the body all stay filled. The shadow")
    a("band adds to its bottom.")
    a("")
    a("| Hull | Volume (cm³) | IoU with our model | Our model inside the hull |")
    a("|---|---|---|---|")
    for hn, hs in vh["variants"].items():
        a(f"| {hn.replace('_', ' ').replace('pct', ' %')} | {hs['hull_volume_cm3']} | {hs['volume_iou']} | {hs['model_inside_hull_pct']} % |")
    a(f"| our model | {vh['model_volume_cm3_exact']} (exact) | | |")
    a("")
    a(f"Surface distances, ≥ 95 % hull: hull to model mean {vh['hull_to_model_mean_mm']} mm (P95 {vh['hull_to_model_p95_mm']}), model to")
    a(f"hull mean {vh['model_to_hull_mean_mm']} mm (P95 {vh['model_to_hull_p95_mm']}); chamfer (mean of the two) {vh['chamfer_mean_mm']} mm.")
    a("")
    a("## What this does and does not show")
    a("")
    a("- The video is Teknic's render of its own CAD. So at best this checks our builder against Teknic's model by a second route;")
    a("  the STEP comparison in [`cad_compare.md`](cad_compare.md) is the first, and the better one (IoU 0.661). It says nothing about")
    a("  how a real unit differs from Teknic's CAD, and the intrinsics are those of a virtual camera.")
    a("- The solve is self-consistent (sub-pixel reprojection error, all frames registered), but its proportions are off, and k1 is")
    a("  large for a render. A narrow field of view (about 27°) and an object that only turns about one axis leave the focal length")
    a("  weakly fixed, and an error in it stretches the reconstruction. Fixing f to candidate values and re-running the mapper")
    a("  would test that; it was not run (about 15 min per mapper run on the shared runner).")
    a("- The sparse points sit where SIFT finds texture: the pin fins, the connector block, the cover screws, the flange's edges and")
    a("  holes, and the body's ribs. Smooth faces have few points, so the distance numbers weight those features.")
    a("- Not done: dense MVS (needs CUDA) and a NeRF or Gaussian splat (not quick on 4 shared CPU cores).")
    a("- [`video_recon_cloud.png`](video_recon_cloud.png): the aligned cloud over our model in three views, coloured by distance,")
    a("  and the solved camera path.")
    fx = OUT / "video_recon_fixedf.json"
    if fx.exists():
        F = json.loads(fx.read_text())
        a("")
        a(f"## Focal-length test ({F['date']})")
        a("")
        a("To test whether the distortion comes from a mis-solved focal length, the mapper was re-run on the same features and")
        a("matches with f held fixed and k1 = 0 (a render has no lens distortion). 1778 px is a 50 mm lens on a 36 mm-wide sensor,")
        a("a common default in 3D render tools; 4010 and 6000 px are 1.5 and 2.25 × the self-calibrated f. Each mapper run took 6.5-9.3 min.")
        a("Each model was compared with ours the same way: the first")
        a("run's pose carried over through the camera centres, refitted on the silhouettes (upright, every 6th view), then the per-axis")
        a("scales, the flange, the distances (rigid ICP at the flange scale) and the IoU over all views.")
        a("")
        a("| f (px) | k1 | Registered | Points | Reproj. (px) | Orbit radius sd | Per-axis scales x / y / z | Spread | Flange (mm) | "
          "Median IoU, all views | Within 1 mm |")
        a("|---|---|---|---|---|---|---|---|---|---|---|")
        for lab, ru in F["runs"].items():
            pa = ru["per_axis_scale"]
            fwm = " × ".join(f"{v:.1f}" for v in ru["flange_width_x_y_mm"]) if ru["flange_width_x_y_mm"] else "–"
            a(f"| {ru['f_px']:.0f} ({lab}) | {ru['k1']} | {ru['registered']} | {ru['points3D']:,} | {ru['mean_reprojection_error_px']} | "
              f"{ru['orbit']['radius_cv_pct']} % | {pa['x']} / {pa['y']} / {pa['z']} | **{ru['per_axis_spread_pct']} %** | {fwm} | "
              f"{ru['silhouette_iou_all_views_T220']['median']} | {ru['cloud_to_model_flange_scaled_rigid_icp']['within_1mm_pct']} % |")
        for lab, ru in F["runs"].items():
            if ru.get("note"):
                a("")
                a(f"f {ru['f_px']:.0f}: {ru['note']}.")
        if F.get("conclusion"):
            a("")
            a(F["conclusion"])
    (OUT / "video_recon.md").write_text("\n".join(L) + "\n")
    print("wrote", OUT / "video_recon.md")


if __name__ == "__main__":
    {"fetch": fetch, "frames": frames, "colmap": colmap, "analyze": analyze, "aniso": aniso, "fixedf": fixedf,
     "report": report}[sys.argv[1]]()
