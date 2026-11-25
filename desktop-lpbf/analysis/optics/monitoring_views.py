#!/usr/bin/env python3
"""Where in-situ monitoring sensors can see the plate from, checked on the model (issue #260, monitoring.md).

A candidate viewport is a Ø20 window bore through the lid, a chamber wall or the door, drilled on its line of sight to the plate
centre (like the layer camera's, optics.md §8.5). For each candidate, in the lasing state (recoater at the end of its stroke, doors,
drawer and reservoir closed), this script

  1. builds the sight volume from the Ø20 aperture on the outer face to the whole plate: the convex hull of the aperture disc and
     the plate disc, which is exactly the set of straight rays between them. It is intersected with every part in or on the
     chamber (manifold3d, meshed at a 0.2 mm chord). The host part (lid, chamber body or door) and the liner the bore passes
     through are left out: the bore is cut through them;
  2. if a part cuts that volume, it checks a Ø6 pupil (a small camera lens near f/4-8) at the aperture centre to 17 points on
     the plate (the centre and rings at half and full radius), and reports the fraction seen;
  3. outside, grows a cylinder (camera plus lens) along the line of sight from 15 mm off the outer face (the window's adapter)
     until it touches a part, for the longest camera of each diameter that fits.

Plates: M50 (Ø50.8) and L75 (Ø76.2) at z = 0 (the powder surface), both on one meshed model (the L75 build: every part above the
floor is the same for all modules). It also checks a Ø6 pupil and a Ø40 aperture to the plate centre. The coaxial path through the
galvo is not a viewport and is treated in monitoring.md. Writes analysis/out/monitoring/views.json, views.md and views.png.

    /tmp/venv/bin/python desktop-lpbf/analysis/optics/monitoring_views.py [--step 20]      # ~4 min at 20 mm (453 ports)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import manifold3d as mf
import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "monitoring"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import lpbf_low as M  # noqa: E402

TOL = 0.2                       # tessellation chord (mm): sight lines, not fits
AP_R = 10.0                     # Ø20 window aperture, as the layer camera's
PUPIL_R = 3.0                   # Ø6 pupil for the per-point check
Z_TARGET = 0.3                  # plate disc just above the powder surface, so the floor and plate never touch the hull
STANDOFF = 15.0                 # window adapter between the outer face and the camera
CAMERAS = {"Ø44 (machine-vision camera + C-mount lens)": 22.0, "Ø80 (long-distance microscope or high-speed camera)": 40.0}
L_MAX = 500.0
PLATES = {"M50": 50.8 / 2, "L75": 76.2 / 2}
STATE = {"recoater": M.MOTION["recoater"]["hi"]}      # lasing: blade parked at the end of its stroke (x 91-109)
VOL_EPS = 0.05                  # mm3


def vol(m):
    return float(m.volume() if hasattr(m, "volume") else m.get_volume())


def to_manifold(shape):
    ms = []
    for s in (list(shape.Solids()) or [shape]):
        vs, ts = s.tessellate(TOL, 0.3)
        if not ts:
            continue
        tm = trimesh.Trimesh(np.array([(p.x, p.y, p.z) for p in vs]), np.array(ts, dtype=np.int64), process=True)
        tm.merge_vertices(digits_vertex=4)
        tm.remove_unreferenced_vertices()
        if tm.volume < 0:
            tm.invert()
        m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(tm.vertices, dtype=np.float32), tri_verts=np.asarray(tm.faces, dtype=np.uint32)))
        if m.status() != mf.Error.NoError or m.is_empty():
            m = mf.Manifold.hull_points(np.asarray(tm.vertices, dtype=np.float32))
        ms.append(m)
    if not ms:
        return None
    return mf.Manifold.batch_boolean(ms, mf.OpType.Add) if len(ms) > 1 else ms[0]


def loc_matrix(loc):
    t = loc.wrapped.Transformation()
    m = np.eye(4)
    for i in range(3):
        for j in range(4):
            m[i, j] = t.Value(i + 1, j + 1)
    return m


def meshed(module):
    parts = M.build(include_tray=False, module=module)
    out = []
    for p in parts:
        if "calibration" in p.tags or "context" in p.tags:
            continue
        m = to_manifold(p.shape)
        if m is None:
            continue
        loc = M.part_location(p, STATE)
        if loc is not None:
            m = m.transform(loc_matrix(loc)[:3, :].astype(np.float32))
        b = m.bounding_box()
        out.append(dict(name=p.name, man=m, lo=np.array(b[:3]), hi=np.array(b[3:])))
    return out


def basis(n):
    a = np.cross(n, [0.0, 0.0, 1.0])
    if np.linalg.norm(a) < 1e-6:
        a = np.cross(n, [1.0, 0.0, 0.0])
    a /= np.linalg.norm(a)
    return a, np.cross(n, a)


def disc(c, n, r, k=24):
    a, b = basis(n)
    t = np.linspace(0, 2 * math.pi, k, endpoint=False)
    return c + r * (np.outer(np.cos(t), a) + np.outer(np.sin(t), b))


def hull(*point_sets):
    return mf.Manifold.hull_points(np.vstack(point_sets).astype(np.float32))


def hits(shape, parts, skip):
    b = shape.bounding_box()
    lo, hi = np.array(b[:3]), np.array(b[3:])
    found = []
    for q in parts:
        if any(s in q["name"] for s in skip):
            continue
        if np.any(q["hi"] < lo) or np.any(q["lo"] > hi):
            continue
        v = vol(shape ^ q["man"])
        if v > VOL_EPS:
            found.append((q["name"], v))
    return found


def cylinder(p0, d, r, L):
    c = mf.Manifold.cylinder(L, r, r, 32)
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(z, d)
    s, cth = np.linalg.norm(v), float(z @ d)
    if s < 1e-9:
        R = np.eye(3) if cth > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        k = v / s
        K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
        R = np.eye(3) + s * K + (1 - cth) * K @ K
    T = np.hstack([R, p0.reshape(3, 1)])
    return c.transform(T.astype(np.float32))


def plate_points(R):
    pts = [np.array([0.0, 0.0, Z_TARGET])]
    for rr in (R / 2, R):
        for k in range(8):
            a = 2 * math.pi * k / 8
            pts.append(np.array([rr * math.cos(a), rr * math.sin(a), Z_TARGET]))
    return pts


P = M.P
FACES = {
    # face: (host part to skip, liner to skip, fixed coordinate, grid builder) -- outer faces of the lid, walls and door
    "lid": dict(skip=("Chamber lid",), n=np.array([0.0, 0.0, 1.0])),
    "back wall (+y)": dict(skip=("Process chamber body", "back upper", "back lower"), n=np.array([0.0, 1.0, 0.0])),
    "right wall (+x)": dict(skip=("Process chamber body", "liner, right"), n=np.array([1.0, 0.0, 0.0])),
    "left wall (-x)": dict(skip=("Process chamber body", "liner, left"), n=np.array([-1.0, 0.0, 0.0])),
    "door (-y)": dict(skip=("Chamber door",), n=np.array([0.0, -1.0, 0.0])),
}
OUTSIDE_SKIP = ("Process chamber body", "Chamber lid", "Chamber floor plate", "Chamber door", "Lid O-ring", "Floor O-ring", "Door O-ring")


def candidates(step):
    cx, cy, lz1 = P["cx"], P["cy"], P["lid_z1"]
    door_y = -cy - 15.0                     # door's outer face (15 mm door on the front face)
    c = []
    for x in np.arange(-140, 140.1, step):
        for y in np.arange(-100, 100.1, step):
            c.append(("lid", np.array([x, y, lz1])))
    for x in np.arange(-130, 130.1, step):
        for z in np.arange(10, 110.1, step):
            c.append(("back wall (+y)", np.array([x, cy, z])))
            c.append(("door (-y)", np.array([x, door_y, z])))
    for y in np.arange(-90, 90.1, step):
        for z in np.arange(10, 110.1, step):
            c.append(("right wall (+x)", np.array([cx, y, z])))
            c.append(("left wall (-x)", np.array([-cx, y, z])))
    return c


def evaluate(parts, face, p_out):
    """Sight volumes from the Ø20 aperture at p_out to the L75 and M50 plates, and to the plate centre with a Ø20 and a Ø40 aperture.
    The parts above z = 0 are the same for every module, so one meshed model serves both plates."""
    skip = FACES[face]["skip"]
    tgt = np.array([0.0, 0.0, Z_TARGET])
    d_in = tgt - p_out
    dist = float(np.linalg.norm(d_in))
    d_in /= dist
    up = np.array([0.0, 0.0, 1.0])
    out = dict(face=face, port=[round(float(v), 1) for v in p_out], dist_to_centre=round(dist, 1),
               elevation_deg=round(math.degrees(math.asin(max(-1.0, min(1.0, -d_in[2])))), 1),
               azimuth_deg=round(math.degrees(math.atan2(p_out[1], p_out[0])), 1))
    for mod, R in PLATES.items():
        blockers = hits(hull(disc(p_out, d_in, AP_R), disc(tgt, up, R, 48)), parts, skip)
        seen = 1.0
        if blockers:
            names = {b[0] for b in blockers}
            sub = [q for q in parts if q["name"] in names]
            ok = 0
            for t in plate_points(R):
                cone = hull(disc(p_out, (t - p_out) / np.linalg.norm(t - p_out), PUPIL_R, 16), disc(t, up, 0.2, 8))
                ok += not hits(cone, sub, skip)
            seen = ok / 17.0
        out[f"{mod}_seen"] = round(seen, 3)
        out[f"{mod}_blockers"] = sorted({b[0][:70] for b in blockers})
    for ap in (AP_R, 2 * AP_R):
        cone = hull(disc(p_out, d_in, ap), disc(tgt, up, 0.2, 8))
        out[f"centre_clear_d{2 * ap:.0f}"] = not hits(cone, parts, skip)
    return out


def outside(parts, p_out, face):
    """Longest camera of each diameter that fits on the line of sight. A Ø30 adapter tube runs from the outer face to the camera's
    start, which is far enough out that the camera's whole front face is >= 5 mm off the host face."""
    d = p_out - np.array([0.0, 0.0, Z_TARGET])
    d /= np.linalg.norm(d)
    cos_t = abs(float(d @ FACES[face]["n"]))
    sin_t = math.sqrt(max(0.0, 1 - cos_t ** 2))
    skip = OUTSIDE_SKIP + FACES[face]["skip"]
    res = {}
    for label, r in CAMERAS.items():
        s0 = max(STANDOFF, (5.0 + r * sin_t) / max(cos_t, 0.05))
        adapter = hits(cylinder(p_out - d * 5.0, d, AP_R + 5.0, s0 + 5.0), parts, skip)
        if adapter:
            res[label] = dict(standoff=round(s0, 0), max_len=0.0, first_hit=sorted({f[0][:60] for f in adapter})[:3], blocked_at="adapter")
            continue
        p0 = p_out + d * s0
        h = hits(cylinder(p0, d, r, L_MAX), parts, skip)
        if not h:
            res[label] = dict(standoff=round(s0, 0), max_len=L_MAX, first_hit=None)
            continue
        lo, hi, first = 0.0, L_MAX, h
        while hi - lo > 5.0:
            mid = 0.5 * (lo + hi)
            hm = hits(cylinder(p0, d, r, mid), parts, skip)
            if hm:
                hi, first = mid, hm
            else:
                lo = mid
        res[label] = dict(standoff=round(s0, 0), max_len=round(lo, 0), first_hit=sorted({f[0][:60] for f in first})[:3])
    return res


def box(x0, x1, y0, y1, z0, z1):
    return mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def lens_and_body(parts, port, face, lens_r, lens_len, body_r, skip_extra=()):
    """A lens (cylinder) then a camera body (cylinder) on the port's line of sight: is the lens clear, and how long can the body be."""
    p = np.array(port, float)
    t = np.array([0.0, 0.0, Z_TARGET])
    d = p - t
    d /= np.linalg.norm(d)
    cos_t = abs(float(d @ FACES[face]["n"]))
    sin_t = math.sqrt(max(0.0, 1 - cos_t ** 2))
    s0 = max(STANDOFF, (5.0 + lens_r * sin_t) / max(cos_t, 0.05))
    skip = OUTSIDE_SKIP + FACES[face]["skip"] + tuple(skip_extra)
    lens = hits(cylinder(p + d * s0, d, lens_r, lens_len), parts, skip)
    free, first = 0.0, None
    for L in range(20, 401, 10):
        h = hits(cylinder(p + d * (s0 + lens_len), d, body_r, L), parts, skip)
        if h:
            first = sorted({n[:60] for n, _ in h})[:3]
            break
        free = float(L)
    return dict(port=list(port), face=face, standoff=round(s0), lens=f"Ø{2 * lens_r:.0f} x {lens_len}", lens_clear=not lens,
                lens_hits=sorted({n[:60] for n, _ in lens})[:3], body=f"Ø{2 * body_r:.0f}", body_len_free=free, body_first_hit=first,
                lens_front_to_plate_centre=round(float(np.linalg.norm(p - t)) + s0), skipped=list(skip_extra))


def fits(parts):
    """Room for the specific instruments monitoring.md proposes (lasing state, M50)."""
    out = {"boxes": [], "cameras": []}
    for label, b in [
        ("coaxial camera branch from the photodiode chain toward the front (-y)", (-230, -170, -200, -62, 240, 300)),
        ("coaxial chain extended along -x (second photodiode, InGaAs channel)", (-400, -254, -60, 10, 240, 300)),
        ("coaxial branch straight up (+z)", (-235, -165, -60, 10, 297, 362)),
        ("folded arm for a Chronos-class coaxial camera, front-left above the bridge", (-420, -200, -170, -70, 244, 335)),
    ]:
        h = hits(box(*b), parts, ())
        out["boxes"].append(dict(what=label, box=list(b), hits=[(n[:60], round(v, 1)) for n, v in h][:5]))
    for port, face, extra in [((-156.0, -10.0, 50.0), "left wall (-x)", ()), ((-156.0, -30.0, 30.0), "left wall (-x)", ()),
                              ((-60.0, -80.0, 136.0), "lid", ("Optics bridge (6061",))]:
        for lens_len in (60, 100):
            out["cameras"].append(lens_and_body(parts, port, face, 30.0, lens_len, 60.0, extra))
    return out


def figure(rows, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    faces = list(FACES)
    fig, axs = plt.subplots(1, len(faces), figsize=(4.2 * len(faces), 4.4))
    big = "Ø80 (long-distance microscope or high-speed camera)"
    for ax, face in zip(axs, faces):
        xs = [r for r in rows if r["face"] == face]
        for r in xs:
            x, y, z = r["port"]
            u, v = {"lid": (x, y), "back wall (+y)": (x, z), "door (-y)": (x, z), "right wall (+x)": (y, z), "left wall (-x)": (y, z)}[face]
            L = (r.get("outside") or {}).get(big, {}).get("max_len", 0.0)
            if r["L75_seen"] >= 0.99:
                c = "#1a9850" if L >= 250 else ("#91cf60" if L >= 120 else "#fee08b")
            elif r["M50_seen"] >= 0.99:
                c = "#fc8d59"
            else:
                c = "#d73027" if r["L75_seen"] < 0.5 else "#f4a582"
            ax.scatter([u], [v], c=c, s=60, marker="s", edgecolors="none")
        ax.set_title(face, fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlabel({"lid": "x (mm)", "back wall (+y)": "x (mm)", "door (-y)": "x (mm)"}.get(face, "y (mm)"))
        ax.set_ylabel("y (mm)" if face == "lid" else "z (mm)")
        ax.grid(alpha=0.3)
    from matplotlib.patches import Patch
    leg = [Patch(color="#1a9850", label="sees all of L75; Ø80 camera >= 250 mm fits"),
           Patch(color="#91cf60", label="sees all of L75; Ø80 camera 120-250 mm"),
           Patch(color="#fee08b", label="sees all of L75; < 120 mm for a Ø80 camera"),
           Patch(color="#fc8d59", label="sees all of M50 only"),
           Patch(color="#f4a582", label="sees >= half of L75"),
           Patch(color="#d73027", label="sees < half of L75")]
    fig.legend(handles=leg, loc="lower center", ncol=3, fontsize=9, frameon=False)
    fig.suptitle("Candidate Ø20 viewports, lasing state: what each sees of the plate and how long a Ø80 camera fits outside", fontsize=11)
    fig.tight_layout(rect=(0, 0.1, 1, 0.95))
    fig.savefig(path, dpi=130)


def write_md(rep, path):
    rows = rep["rows"]
    big, small = list(CAMERAS)
    L = ["# Candidate viewports for in-situ monitoring (generated by analysis/optics/monitoring_views.py)", "",
         f"State: {rep['state']}. Ø{rep['aperture_d']:.0f} window aperture on the outer face; per-point check with a Ø{rep['pupil_d']:.0f} pupil; "
         f"grid step {rep['step']:.0f} mm; plate surface at z = 0. Camera lengths start after the adapter (standoff).", ""]
    for face in FACES:
        xs = [r for r in rows if r["face"] == face]
        ok = [r for r in xs if r["L75_seen"] >= 0.99]
        okm = [r for r in xs if r["M50_seen"] >= 0.99]
        L += [f"## {face}: {len(ok)} of {len(xs)} see all of L75, {len(okm)} all of M50", ""]
        L += ["| port (x, y, z) | elevation | to plate centre | L75 / M50 seen | centre clear Ø20 / Ø40 | Ø44 camera | Ø80 camera | first part hit (Ø80) |",
              "|---|---:|---:|---:|---|---:|---:|---|"]
        key = lambda r: (-(r["L75_seen"] >= 0.99), -((r.get("outside") or {}).get(big, {}).get("max_len", 0.0)), -r["L75_seen"])
        for r in sorted(xs, key=key)[:8]:
            o = r.get("outside") or {}
            ob, os_ = o.get(big, {}), o.get(small, {})
            L.append(f"| {tuple(r['port'])} | {r['elevation_deg']:.1f}° | {r['dist_to_centre']:.0f} mm | {r['L75_seen']:.2f} / {r['M50_seen']:.2f} | "
                     f"{'yes' if r['centre_clear_d20'] else 'no'} / {'yes' if r['centre_clear_d40'] else 'no'} | "
                     f"{os_.get('max_len', '–')} | {ob.get('max_len', '–')} | {', '.join(ob.get('first_hit') or []) or '–'} |")
        bl = {}
        for r in xs:
            for b in r["L75_blockers"]:
                bl[b] = bl.get(b, 0) + 1
        L += ["", "Parts that most often cut the L75 sight volume: " + "; ".join(f"{k} ({v})" for k, v in sorted(bl.items(), key=lambda t: -t[1])[:6]), ""]
    path.write_text("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", type=float, default=20.0)
    ap.add_argument("--fits-only", action="store_true", help="only the instrument fits (fits.json), not the port grid")
    args = ap.parse_args()
    if args.fits_only:
        f = fits(meshed("M50"))
        (OUT / "fits.json").write_text(json.dumps(f, indent=1) + "\n")
        print(json.dumps(f, indent=1))
        return
    t0 = time.time()
    rep = dict(state="lasing: recoater at the end of its stroke, doors, drawer and reservoir closed", aperture_d=2 * AP_R,
               pupil_d=2 * PUPIL_R, standoff_min=STANDOFF, step=args.step, cameras=CAMERAS, model_module="L75")
    cands = candidates(args.step)
    parts = meshed("L75")
    print(f"[{time.time() - t0:6.1f} s] {len(parts)} parts meshed; {len(cands)} candidate ports", flush=True)
    rows = []
    for i, (face, p) in enumerate(cands):
        r = evaluate(parts, face, p)
        if r["M50_seen"] >= 0.99 or r["centre_clear_d20"]:
            r["outside"] = outside(parts, p, face)
        rows.append(r)
        if i % 100 == 0:
            print(f"[{time.time() - t0:6.1f} s] {i}/{len(cands)}", flush=True)
    rep["rows"] = rows
    (OUT / "views.json").write_text(json.dumps(rep, indent=1) + "\n")
    write_md(rep, OUT / "views.md")
    figure(rows, OUT / "views.png")
    print(f"[{time.time() - t0:6.1f} s] wrote views.json, views.md, views.png", flush=True)


if __name__ == "__main__":
    main()
